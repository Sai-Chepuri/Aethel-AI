import os
import json
import time
from google import genai
from google.genai import types
from schemas.response_schema import RiskOutput
from utils.mock_helper import get_mock_context

def _get_prompt(idea: str, prd_and_roadmap_context: dict) -> str:
    current_dir = os.path.dirname(os.path.abspath(__file__))
    prompt_path = os.path.join(current_dir, "..", "prompts", "risk_prompt.txt")
    with open(prompt_path, "r", encoding="utf-8") as f:
        template = f.read()

    ctx_str = json.dumps(prd_and_roadmap_context, indent=2)
    return template.format(idea=idea, prd_and_roadmap_context=ctx_str)

def _generate_mock_risks(idea: str) -> dict:
    ctx = get_mock_context(idea)
    return {
        "risks": ctx["risks"]
    }

async def run_risk_agent(idea: str, prd_and_roadmap_context: dict, api_key: str = None) -> dict:
    start_time = time.perf_counter()
    status = "completed"

    if not api_key:
        print("[risk_agent] No API key configured. Falling back to mock generator.")
        res = _generate_mock_risks(idea)
        res["status"] = status
        res["duration_ms"] = int((time.perf_counter() - start_time) * 1000)
        return res

    try:
        client = genai.Client(api_key=api_key)
        prompt_content = _get_prompt(idea, prd_and_roadmap_context)
        response = await client.aio.models.generate_content(
            model="gemini-2.5-flash",
            contents=prompt_content,
            config=types.GenerateContentConfig(
                response_mime_type="application/json",
                response_schema=RiskOutput
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
        validated = RiskOutput(**parsed)
        output = validated.model_dump()
        output["status"] = status
        output["duration_ms"] = duration_ms
        return output
    except Exception as exc:
        print(f"[risk_agent] Error: {exc}. Falling back to mock risks.")
        res = _generate_mock_risks(idea)
        res["status"] = "failed"
        res["duration_ms"] = int((time.perf_counter() - start_time) * 1000)
        return res
