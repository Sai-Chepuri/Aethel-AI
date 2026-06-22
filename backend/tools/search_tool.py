from google import genai
from google.genai import types

async def google_search(query: str, api_key: str) -> str:
    """
    Perform a web search using the Google Search grounding tool via Gemini.
    
    This abstracts the search tool call from the agent.
    """
    client = genai.Client(api_key=api_key)
    response = await client.aio.models.generate_content(
        model="gemini-2.5-flash",
        contents=query,
        config=types.GenerateContentConfig(
            tools=[{"google_search": {}}]
        )
    )
    return response.text
