import config
import os
import json
import time
from google import genai
from google.genai import types
from schemas.response_schema import PRDOutput
from utils.mock_helper import get_mock_context

def _get_prompt(idea: str, market_research_context: dict, personas_context: dict) -> str:
    current_dir = os.path.dirname(os.path.abspath(__file__))
    prompt_path = os.path.join(current_dir, "..", "prompts", "prd_prompt.txt")
    with open(prompt_path, "r", encoding="utf-8") as f:
        template = f.read()

    mr_str = json.dumps(market_research_context, indent=2)
    p_str = json.dumps(personas_context, indent=2)
    return template.format(idea=idea, market_research_context=mr_str, personas_context=p_str)

def _generate_mock_prd(idea: str) -> dict:
    ctx = get_mock_context(idea)
    return {
        "prd": ctx["prd"],
        "user_stories": ctx["user_stories"],
        "acceptance_criteria": ctx["acceptance_criteria"]
    }

async def run_prd_agent(idea: str, market_research_context: dict, personas_context: dict) -> dict:
    start_time = time.perf_counter()
    status = "completed"

    try:
        client = genai.Client(api_key=os.getenv("GEMINI_API_KEY"))
        prompt_content = _get_prompt(idea, market_research_context, personas_context)
        response = await client.aio.models.generate_content(
            model="gemini-2.5-flash",
            contents=prompt_content,
            config=types.GenerateContentConfig(
                response_mime_type="application/json",
                response_schema=PRDOutput
            )
        )
        duration_ms = int((time.perf_counter() - start_time) * 1000)
        if hasattr(response, "parsed") and response.parsed:
            output = response.parsed.model_dump()
            output["status"] = status
            output["duration_ms"] = duration_ms
            return output
        
        # Fallback parsing
        from services.gemini_service import _extract_and_parse_json
        parsed = _extract_and_parse_json(response.text)
        validated = PRDOutput(**parsed)
        output = validated.model_dump()
        output["status"] = status
        output["duration_ms"] = duration_ms
        return output
    except Exception as exc:
        print(f"[prd_agent] Error: {exc}. Falling back to mock PRD.")
        res = _generate_mock_prd(idea)
        res["status"] = "failed"
        res["duration_ms"] = int((time.perf_counter() - start_time) * 1000)
        return res
