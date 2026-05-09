"""Test Gemini Connection."""
import asyncio
from app.core.llm import get_financial_advice_async

async def main():
    prompt = "Halo, saya sedang membuat aplikasi Personal Finance. Berikan saya saran keuangan 1 kalimat saja."
    print("Mengirim request ke Gemini...")
    response = await get_financial_advice_async(prompt)
    print("=== RESPONS GEMINI ===")
    print(response)

if __name__ == "__main__":
    asyncio.run(main())
