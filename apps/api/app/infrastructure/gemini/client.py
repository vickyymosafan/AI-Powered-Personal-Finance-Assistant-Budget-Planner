"""
Gemini AI Client — Infrastructure layer
"""

from google import genai

from app.core.config import settings


class GeminiClient:
    """Wrapper for Google Gemini API"""

    def __init__(self):
        self._client = genai.Client(api_key=settings.GEMINI_API_KEY)
        self._model = settings.GEMINI_MODEL

    async def generate(
        self,
        prompt: str,
        system_instruction: str = "",
        temperature: float = 0.7,
    ) -> str:
        """Generate text response from Gemini"""
        config = genai.types.GenerateContentConfig(
            temperature=temperature,
            system_instruction=system_instruction or None,
        )

        response = await self._client.aio.models.generate_content(
            model=self._model,
            contents=prompt,
            config=config,
        )

        return response.text or ""

    async def generate_structured(
        self,
        prompt: str,
        system_instruction: str = "",
    ) -> str:
        """Generate structured (JSON) response"""
        config = genai.types.GenerateContentConfig(
            temperature=0.3,
            response_mime_type="application/json",
            system_instruction=system_instruction or None,
        )

        response = await self._client.aio.models.generate_content(
            model=self._model,
            contents=prompt,
            config=config,
        )

        return response.text or ""


# Singleton
gemini_client = GeminiClient()
