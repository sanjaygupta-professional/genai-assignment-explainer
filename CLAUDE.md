# CLAUDE.md

This file provides guidance to Claude Code (claude.ai/code) when working with code in this repository.

## Project Overview

Interactive study guides for a DBA Gen AI course (GGU/upGrad Course 8919), plus a working RAG + Knowledge Graph backend (SamarthSchool) built as the group assignment deliverable.

Two major parts:
1. **Static HTML site** — self-contained HTML files (no build system, no bundler) with inline `<style>` and `<script>`. Deployed to Vercel.
2. **`rag-pipeline/`** — Python 3.12 RAG + KG pipeline for Indian disability welfare schemes. Uses Gemini 2.0, Qdrant, Kuzu graph DB, and a FastAPI server with Twilio WhatsApp integration.

## Architecture — Static Site

### Page Types

**Explainers** (`assignment1.html`, `group-assignment.html`, `rag-pipeline-story.html`): Single-scroll pages with fixed header, section nav, collapsible accordion sections, rubric breakdowns. CSS is fully inline in `<style>`.

**Workbooks** (`*-workbook.html`): Sidebar + main content layout. Link `workbook-shared.css` for shared layout/typography. JS at the bottom handles sidebar highlighting (`IntersectionObserver`), progress bar, and page budget — adjust `PAGE_WEIGHTS` array for new sections.

**Playgrounds** (`rag-infra-playground.html`): Tool-style interactive pages with configuration controls and live preview panels. Fully self-contained.

### Hindi Translations (`hi/`)

Every page has a Hindi counterpart in `hi/`. Pages use `hreflang` alternates (`<link rel="alternate" hreflang="hi" href="hi/...">`). Hindi pages use Noto Sans Devanagari as primary font. When adding/modifying an English page, update the corresponding `hi/` page too.

### Other Root Files

| File | Purpose |
|---|---|
| `create_pitch_deck.py` | Generates SamarthSchool pitch deck PPTX (`python-pptx`) |
| `generate_docx.py` | Generates Assignment 1 Word doc from workbook HTML (`python-docx`, `cairosvg`) |
| `group-assignment-report.md` | SamarthSchool group assignment written report |
| `images/diagrams/` | SVG diagrams (e.g., RAG pipeline architecture) |
| `images/screenshots/` | App screenshots for DOCX embedding |
| `outputs/` | Generated artifacts (DOCX, PPTX, diagram PNGs) — not committed |

## Architecture — RAG Pipeline (`rag-pipeline/`)

### Running the Pipeline

```bash
cd rag-pipeline

# Setup
cp .env.example .env          # add GOOGLE_API_KEY
pip install -r requirements.txt  # uses python3.12

# Extract scheme metadata from PDFs via Gemini
python3.12 scripts/extract_schemes.py

# Ingest: embed PDFs into Qdrant + build Knowledge Graph
python3.12 scripts/ingest.py              # full ingestion
python3.12 scripts/ingest.py --text-only  # text embeddings only (faster)
python3.12 scripts/ingest.py --kg-only    # rebuild KG only

# Query
python3.12 scripts/query.py "What schemes are available for a child with autism?"
python3.12 scripts/query.py --interactive  # REPL mode
python3.12 scripts/demo.py                 # pre-scripted demo queries

# WhatsApp server
uvicorn src.server:app --host 127.0.0.1 --port 8000
# Expose via: cloudflared tunnel --url http://localhost:8000
```

### Pipeline Module Layout

| Module | Role |
|---|---|
| `src/config.py` | Centralized config — paths, model IDs, API key loading from `.env` |
| `src/chunker.py` | Splits PDFs into page-range chunks |
| `src/embedder.py` | Gemini Embedding 2 (`gemini-embedding-2-preview`, 768 dims) |
| `src/vectorstore.py` | Qdrant collection management and upsert |
| `src/knowledge_graph.py` | Kuzu graph DB — scheme/eligibility/benefit nodes and relationships |
| `src/retriever.py` | Hybrid retrieval: vector similarity + KG confirmation |
| `src/generator.py` | Gemini 2.0 Flash generation with retrieved context |
| `src/pipeline.py` | Orchestrator tying retrieval + generation |
| `src/server.py` | FastAPI: `/whatsapp` (Twilio webhook), `/query` (direct API), `/health` |
| `src/whatsapp_formatter.py` | Formats Action Guide output for WhatsApp (1600 char limit) |
| `src/hindi_labels.py` | Hindi UI labels for multilingual output |
| `src/schema.py` | Pydantic models / data schemas |

### Key Config Values (in `src/config.py`)

- Embedding model: `gemini-embedding-2-preview` (768 dimensions)
- Generation model: `gemini-2.0-flash`
- Chunk size: 5 pages, 1 page overlap
- Rate limiting: 1.5s between embedding API calls
- Data: `data/schemes/` (source PDFs), `data/qdrant_db/`, `data/kuzu_db/`

### Environment Variables

| Variable | Required | Source |
|---|---|---|
| `GOOGLE_API_KEY` | Yes | `rag-pipeline/.env` |
| `TWILIO_ACCOUNT_SID` | WhatsApp only | `rag-pipeline/.env.twilio` |
| `TWILIO_AUTH_TOKEN` | WhatsApp only | `rag-pipeline/.env.twilio` |

## Design System (DesignArena)

All pages use the same visual language. CSS custom properties are defined identically across files:

- **Fonts**: Playfair Display (headings), Inter (body) — Google Fonts
- **Palette**: warm/earthy — cream `#F7F6F5`, teal `#487265`, sage `#A0C3C4`, gold `#D4C68B`, copper `#BC976A`
- **Layout**: `--max-w: 780px` (explainers), `--sidebar-w: 220px` (workbooks), `--header-h: 55px`
- **Style rules**: no box-shadows, `border-radius: 12px` on cards, 1px solid borders, rounded pills for tags

When creating new pages, copy the `:root` CSS variables block from an existing page rather than inventing new colors.

## Adding New Pages

### New Workbook
1. Copy an existing workbook HTML file as template
2. Keep `<link rel="stylesheet" href="workbook-shared.css">` — do not inline the shared styles
3. Adjust `PAGE_WEIGHTS` array in the inline JS for the new sections
4. Update `index.html` card grid
5. Create matching `hi/` translation with Noto Sans Devanagari font

### New Explainer
1. Copy `assignment1.html` or `group-assignment.html` as template (styles are fully inline)
2. Keep the DesignArena CSS variables block identical
3. Update `index.html` card grid
4. Create matching `hi/` translation

## Deployment

Static file hosting — no build step. Push to `main`.

- **Vercel**: auto-deploys from GitHub (project ID in `.vercel/project.json`)
- Files are served as-is; any `.html` file at the root is a routable page
- The `rag-pipeline/` backend is **not** deployed via Vercel — it runs separately on the server
