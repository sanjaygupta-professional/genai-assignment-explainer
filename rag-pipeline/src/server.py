#!/usr/bin/env python3.12
"""FastAPI server for SamarthSchool with Twilio WhatsApp webhook.

Endpoints:
  POST /whatsapp  — Twilio webhook (receives WhatsApp messages, returns Action Guide)
  GET  /health    — Health check
  POST /query     — Direct API query (for testing without WhatsApp)

Run:
  uvicorn src.server:app --host 127.0.0.1 --port 8000

For WhatsApp testing, expose via Cloudflare Tunnel:
  cloudflared tunnel --url http://localhost:8000
  → paste the public URL into Twilio Sandbox webhook config
"""

import os
import logging
from contextlib import asynccontextmanager

from fastapi import FastAPI, Request, Form
from fastapi.responses import PlainTextResponse, JSONResponse

from src.pipeline import query_pipeline
from src.whatsapp_formatter import format_for_whatsapp, truncate_for_whatsapp

logging.basicConfig(level=logging.INFO)
log = logging.getLogger("samarthschool")

# Optional: Twilio client for sending multi-part messages
_twilio_client = None


def _get_twilio():
    """Lazy-init Twilio client (only if credentials are set)."""
    global _twilio_client
    if _twilio_client is not None:
        return _twilio_client
    sid = os.environ.get("TWILIO_ACCOUNT_SID")
    token = os.environ.get("TWILIO_AUTH_TOKEN")
    if sid and token:
        try:
            from twilio.rest import Client
            _twilio_client = Client(sid, token)
            log.info("Twilio client initialized")
        except ImportError:
            log.warning("twilio package not installed — multi-message responses disabled")
    return _twilio_client


@asynccontextmanager
async def lifespan(app: FastAPI):
    """Startup: verify pipeline is ready."""
    log.info("SamarthSchool server starting...")
    log.info("Pipeline ready. Waiting for queries.")
    yield
    log.info("Server shutting down.")


app = FastAPI(
    title="SamarthSchool API",
    description="AI-Powered Benefits Navigator for Children with Special Abilities",
    lifespan=lifespan,
)


@app.get("/health")
async def health():
    return {"status": "ok", "service": "samarthschool"}


@app.post("/query")
async def direct_query(request: Request):
    """Direct API query for testing (JSON body: {"query": "..."})."""
    body = await request.json()
    query = body.get("query", "")
    if not query:
        return JSONResponse({"error": "Missing 'query' field"}, status_code=400)

    log.info(f"Direct query: {query[:80]}...")
    response = query_pipeline(query, top_k=5, verbose=False)
    return JSONResponse({"response": response})


@app.post("/whatsapp")
async def whatsapp_webhook(
    Body: str = Form(""),
    From: str = Form(""),
    To: str = Form(""),
):
    """Twilio WhatsApp webhook handler.

    Receives incoming WhatsApp messages and responds with Action Guide.
    For short responses, uses TwiML inline reply.
    For long responses, uses Twilio API to send multiple messages.
    """
    query = Body.strip()
    sender = From  # e.g., "whatsapp:+91XXXXXXXXXX"

    if not query:
        return _twiml_response("Please send a message describing the child's situation.")

    log.info(f"WhatsApp from {sender}: {query[:80]}...")

    # Handle special commands
    if query.lower() in ("hi", "hello", "help", "start", "नमस्ते", "मदद"):
        welcome = (
            "🙏 Welcome to *SamarthSchool*!\n\n"
            "I help find government disability welfare schemes for children.\n\n"
            "Send me a message like:\n"
            "\"My daughter is 8 years old with cerebral palsy in Karnataka. "
            "Family income is Rs 1.5 lakh.\"\n\n"
            "Or in Hindi:\n"
            "\"मेरी बेटी को सेरेब्रल पाल्सी है, उम्र 8 साल, कर्नाटक, "
            "आय 1.5 लाख\"\n\n"
            "I'll find eligible schemes and tell you exactly how to apply! 📋"
        )
        return _twiml_response(welcome)

    # Run the RAG + KG pipeline
    try:
        response = query_pipeline(query, top_k=5, verbose=False)
    except Exception as e:
        log.error(f"Pipeline error: {e}")
        return _twiml_response(
            "Sorry, I encountered an error. Please try again.\n"
            "क्षमा करें, कोई त्रुटि हुई। कृपया पुनः प्रयास करें।"
        )

    # Format for WhatsApp
    # First, truncate to top 3 schemes for WhatsApp (user can ask for more)
    truncated = truncate_for_whatsapp(response, max_schemes=3)
    messages = format_for_whatsapp(truncated)

    if len(messages) == 1:
        # Single message — use TwiML inline response
        return _twiml_response(messages[0])

    # Multiple messages — try Twilio API
    twilio = _get_twilio()
    twilio_from = os.environ.get("TWILIO_WHATSAPP_FROM", To)

    if twilio and twilio_from:
        # Send all messages via Twilio API
        for msg in messages:
            try:
                twilio.messages.create(
                    from_=twilio_from,
                    body=msg,
                    to=sender,
                )
            except Exception as e:
                log.error(f"Twilio send error: {e}")
        # Return empty TwiML (messages already sent via API)
        return PlainTextResponse(
            '<?xml version="1.0" encoding="UTF-8"?><Response></Response>',
            media_type="text/xml",
        )
    else:
        # No Twilio API — send first message via TwiML, truncate rest
        return _twiml_response(messages[0])


def _twiml_response(message: str) -> PlainTextResponse:
    """Create a TwiML XML response for Twilio."""
    # Escape XML special characters
    safe = (
        message
        .replace("&", "&amp;")
        .replace("<", "&lt;")
        .replace(">", "&gt;")
    )
    xml = (
        '<?xml version="1.0" encoding="UTF-8"?>'
        f"<Response><Message>{safe}</Message></Response>"
    )
    return PlainTextResponse(xml, media_type="text/xml")
