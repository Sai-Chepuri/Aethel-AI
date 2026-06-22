import os
import json
import time
from google import genai
from google.genai import types
from schemas.response_schema import MetricsOutput
from utils.mock_helper import get_mock_context

def _get_prompt(idea: str, prd_context: dict) -> str:
    current_dir = os.path.dirname(os.path.abspath(__file__))
    prompt_path = os.path.join(current_dir, "..", "prompts", "metrics_prompt.txt")
    with open(prompt_path, "r", encoding="utf-8") as f:
        template = f.read()

    prd_str = json.dumps(prd_context, indent=2)
    return template.format(idea=idea, prd_context=prd_str)

def _generate_mock_metrics(idea: str) -> dict:
    ctx = get_mock_context(idea)
    return {
        "kpis": ctx["kpis"]
    }

async def run_metrics_agent(idea: str, prd_context: dict, api_key: str = None) -> dict:
    start_time = time.perf_counter()
    status = "completed"

    if not api_key:
        print("[metrics_agent] No API key configured. Falling back to mock generator.")
        res = _generate_mock_metrics(idea)
        res["status"] = status
        res["duration_ms"] = int((time.perf_counter() - start_time) * 1000)
        return res

    try:
        client = genai.Client(api_key=api_key)
        prompt_content = _get_prompt(idea, prd_context)
        response = await client.aio.models.generate_content(
            model="gemini-2.5-flash",
            contents=prompt_content,
            config=types.GenerateContentConfig(
                response_mime_type="application/json",
                response_schema=MetricsOutput
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
        validated = MetricsOutput(**parsed)
        output = validated.model_dump()
        output["status"] = status
        output["duration_ms"] = duration_ms
        return output
    except Exception as exc:
        print(f"[metrics_agent] Error: {exc}. Falling back to mock metrics.")
        res = _generate_mock_metrics(idea)
        res["status"] = "failed"
        res["duration_ms"] = int((time.perf_counter() - start_time) * 1000)
        return res
