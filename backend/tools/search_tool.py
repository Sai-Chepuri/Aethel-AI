from google import genai
from google.genai import types

async def google_search(query: str, api_key: str) -> dict:
    """
    Perform a web search using the Google Search grounding tool via Gemini.
    
    This abstracts the search tool call from the agent.
    Returns a dictionary containing:
      - "text": The main response text from the search.
      - "sources": A list of source URIs used for attribution.
    """
    client = genai.Client(api_key=api_key)
    response = await client.aio.models.generate_content(
        model="gemini-2.5-flash",
        contents=query,
        config=types.GenerateContentConfig(
            tools=[{"google_search": {}}]
        )
    )
    
    sources = []
    try:
        if response.candidates and response.candidates[0].grounding_metadata:
            metadata = response.candidates[0].grounding_metadata
            if metadata.grounding_chunks:
                for chunk in metadata.grounding_chunks:
                    if chunk.web and chunk.web.uri:
                        sources.append(chunk.web.uri)
    except Exception as e:
        print(f"[search_tool] Warning: Failed to extract grounding metadata: {e}")
        
    return {
        "text": response.text,
        "sources": sorted(list(set(sources)))
    }
