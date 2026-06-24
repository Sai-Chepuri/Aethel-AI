from typing import Any
from google import genai

async def generate_content_with_fallback(client: genai.Client, contents: Any, config: Any) -> Any:
    """
    Attempt to generate content using gemini-2.5-flash first.
    If it fails, fall back to gemini-2.5-pro.
    """
    try:
        return await client.aio.models.generate_content(
            model="gemini-2.5-flash",
            contents=contents,
            config=config
        )
    except Exception as exc:
        print(f"[gemini_client] Warning: gemini-2.5-flash failed ({exc}). Retrying with gemini-2.5-pro...")
        return await client.aio.models.generate_content(
            model="gemini-2.5-pro",
            contents=contents,
            config=config
        )
