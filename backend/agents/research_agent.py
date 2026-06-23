import config
import os
import time
from google import genai
from google.genai import types
from schemas.response_schema import ResearchOutput
from utils.mock_helper import get_mock_context

def _get_prompt(idea: str, search_findings: str) -> str:
    current_dir = os.path.dirname(os.path.abspath(__file__))
    prompt_path = os.path.join(current_dir, "..", "prompts", "research_prompt.txt")
    with open(prompt_path, "r", encoding="utf-8") as f:
        template = f.read()
    return template.format(idea=idea, search_findings=search_findings)

def _generate_mock_research(idea: str) -> dict:
    ctx = get_mock_context(idea)
    return {
        "market_research": ctx["market_research"],
        "competitors": ctx["competitors"],
        "source_attributions": ctx["source_attributions"]
    }

async def run_research_agent(idea: str) -> dict:
    start_time = time.perf_counter()
    status = "completed"

    try:
        client = genai.Client(api_key=os.getenv("GEMINI_API_KEY"))
        
        # Step 1: Perform Google Search Grounding to find competitors, positioning, and differentiators
        print("[research_agent] Step 1: Performing Google Search Grounding for competitor analysis...")
        search_prompt = (
            f"Search Google to identify the top 5 competitors for the following product idea:\n"
            f"\"{idea}\"\n\n"
            f"For each competitor, extract and analyze:\n"
            f"1. Their market positioning (who they target, core message).\n"
            f"2. Their key differentiators (strengths, weaknesses, and unique advantages)."
        )
        from tools.search_tool import google_search
        search_res = await google_search(search_prompt)
        search_findings = search_res["text"]
        sources = search_res["sources"]
        print(f"[research_agent] Grounding search complete. Extracted {len(sources)} competitor source links.")

        # Step 2: Pass findings to Gemini to generate the final structured JSON research report
        print("[research_agent] Step 2: Generating structured research report matching response schema...")
        prompt_content = _get_prompt(idea, search_findings)
        response = await client.aio.models.generate_content(
            model="gemini-2.5-flash",
            contents=prompt_content,
            config=types.GenerateContentConfig(
                response_mime_type="application/json",
                response_schema=ResearchOutput
            )
        )
        duration_ms = int((time.perf_counter() - start_time) * 1000)
        
        if hasattr(response, "parsed") and response.parsed:
            output = response.parsed.model_dump()
            output["status"] = status
            output["duration_ms"] = duration_ms
            output["source_attributions"] = sources
            return output
        
        # Fallback parsing
        from services.gemini_service import _extract_and_parse_json
        parsed = _extract_and_parse_json(response.text)
        validated = ResearchOutput(**parsed)
        output = validated.model_dump()
        output["status"] = status
        output["duration_ms"] = duration_ms
        output["source_attributions"] = sources
        return output
    except Exception as exc:
        print(f"[research_agent] Error: {exc}. Falling back to mock research.")
        res = _generate_mock_research(idea)
        res["status"] = "failed"
        res["duration_ms"] = int((time.perf_counter() - start_time) * 1000)
        return res
