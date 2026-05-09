"""
LLM integration using google-genai SDK.
"""

from google import genai
from pydantic import BaseModel
import json

from app.core.config import settings

# Initialize the Gemini client
# Note: google-genai SDK uses `api_key` argument for synchronous and asynchronous clients
if settings.GEMINI_API_KEY:
    client = genai.Client(api_key=settings.GEMINI_API_KEY)
else:
    client = None


class AIResponse(BaseModel):
    content: str


def get_financial_advice(prompt: str) -> str:
    """
    Get general financial advice or specific analysis from Gemini.
    """
    if not client:
        return "AI features are not configured. Please set GEMINI_API_KEY."

    try:
        response = client.models.generate_content(
            model=settings.GEMINI_MODEL,
            contents=prompt,
        )
        return response.text or "Mohon maaf, tidak ada balasan dari AI."
    except Exception as e:
        print(f"Gemini API Error: {e}")
        return "Mohon maaf, saat ini AI tidak dapat memproses permintaan Anda."

async def get_financial_advice_async(prompt: str) -> str:
    """
    Get financial advice using async request (requires async capable client or wrapper).
    The google-genai SDK provides an async client: `client.aio`.
    """
    if not client:
        return "AI features are not configured. Please set GEMINI_API_KEY."

    try:
        response = await client.aio.models.generate_content(
            model=settings.GEMINI_MODEL,
            contents=prompt,
        )
        return response.text or "Mohon maaf, tidak ada balasan dari AI."
    except Exception as e:
        print(f"Gemini API Error: {e}")
        return "Mohon maaf, saat ini AI tidak dapat memproses permintaan Anda."
