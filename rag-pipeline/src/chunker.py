"""Split PDFs into chunks for embedding.

Each chunk is CHUNK_PAGES pages with CHUNK_OVERLAP page overlap.
Extracts both raw PDF bytes (for Gemini Embedding 2) and text (for generation context).
"""

import fitz  # PyMuPDF
from pathlib import Path
from src.config import CHUNK_PAGES, CHUNK_OVERLAP, SCHEMES_DIR
from src.schema import Chunk


def chunk_pdf(pdf_path: Path) -> list[Chunk]:
    """Split a PDF into overlapping page-based chunks.

    Returns Chunk objects with both raw PDF bytes and extracted text.
    """
    doc = fitz.open(str(pdf_path))
    total_pages = doc.page_count
    scheme_id = pdf_path.stem  # filename without extension
    chunks = []

    start = 0
    while start < total_pages:
        end = min(start + CHUNK_PAGES, total_pages)

        # Extract text from chunk pages
        text_parts = []
        for page_num in range(start, end):
            page_text = doc[page_num].get_text()
            if page_text.strip():
                text_parts.append(f"[Page {page_num + 1}]\n{page_text}")

        text = "\n\n".join(text_parts)

        # Extract raw PDF bytes for this page range
        try:
            chunk_doc = fitz.open()  # empty doc
            chunk_doc.insert_pdf(doc, from_page=start, to_page=end - 1)
            pdf_bytes = chunk_doc.tobytes()
            chunk_doc.close()
        except RuntimeError:
            # Some PDFs (e.g., image-only) fail insert_pdf — use empty bytes
            pdf_bytes = b""

        if text.strip():  # skip empty chunks
            chunk_id = f"{scheme_id}_p{start + 1}-{end}"
            chunks.append(Chunk(
                chunk_id=chunk_id,
                scheme_id=scheme_id,
                source_pdf=pdf_path.name,
                page_start=start + 1,  # 1-indexed
                page_end=end,
                text=text,
                pdf_bytes=pdf_bytes,
            ))

        # Advance with overlap
        step = CHUNK_PAGES - CHUNK_OVERLAP
        if step < 1:
            step = 1
        start += step

    doc.close()
    return chunks


def chunk_all_pdfs() -> list[Chunk]:
    """Chunk all PDFs in the schemes directory."""
    all_chunks = []
    for pdf_path in sorted(SCHEMES_DIR.glob("*.pdf")):
        chunks = chunk_pdf(pdf_path)
        print(f"  {pdf_path.name}: {len(chunks)} chunks")
        all_chunks.extend(chunks)
    return all_chunks
