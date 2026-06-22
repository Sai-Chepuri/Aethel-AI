import os
import json
import time
from google import genai
from google.genai import types
from schemas.response_schema import PersonaOutput
from utils.mock_helper import get_mock_context

def _get_prompt(idea: str, market_research_context: dict) -> str:
    current_dir = os.path.dirname(os.path.abspath(__file__))
    prompt_path = os.path.join(current_dir, "..", "prompts", "persona_prompt.txt")
    with open(prompt_path, "r", encoding="utf-8") as f:
        template = f.read()
    
    mr_str = json.dumps(market_research_context, indent=2)
    return template.format(idea=idea, market_research_context=mr_str)

def _generate_mock_personas(idea: str) -> dict:
    ctx = get_mock_context(idea)
    product_name = ctx["product_name"]

    personas = [
        {
            "name": "Sarah Jenkins",
            "role": "Operations Lead / Digital PM",
            "age": "29",
            "goals": ["Speed", "Clarity", "Stakeholder visibility"],
            "pain_points": [
                "Constantly context-switching between five different tools.",
                "Manual status reports consume 4+ hours per week.",
                "Pricing tiers charge for read-only collaborator seats."
            ],
            "user_scenario": f"Sarah is en route to a client meeting. A Slack message asks for updated product specs. She opens **{product_name}** on her phone, finds the relevant plan in under five seconds, copies a read-only share link, and pastes it into the thread — all before the meeting starts."
        },
        {
            "name": "Marcus Chen",
            "role": "VP of Product & Engineering",
            "age": "42",
            "goals": ["Security", "Compliance", "Predictable licensing"],
            "pain_points": [
                "Vendors export data in proprietary formats, creating lock-in risk.",
                "Undocumented API rate limits break internal reporting pipelines.",
                "No granular role-based access control (RBAC) for audit workflows."
            ],
            "user_scenario": f"Marcus is preparing for a board-level security audit. He logs into **{product_name}**, generates a SOC-2-ready compliance report with one click, restricts his auditor to read-only access via a scoped API token, and exports the entire dataset as open JSON."
        }
    ]

    return {
        "personas": personas
    }

async def run_persona_agent(idea: str, market_research_context: dict, api_key: str = None) -> dict:
    start_time = time.perf_counter()
    status = "completed"

    if not api_key:
        print("[persona_agent] No API key configured. Falling back to mock generator.")
        res = _generate_mock_personas(idea)
        res["status"] = status
        res["duration_ms"] = int((time.perf_counter() - start_time) * 1000)
        return res

    try:
        client = genai.Client(api_key=api_key)
        prompt_content = _get_prompt(idea, market_research_context)
        response = await client.aio.models.generate_content(
            model="gemini-2.5-flash",
            contents=prompt_content,
            config=types.GenerateContentConfig(
                response_mime_type="application/json",
                response_schema=PersonaOutput
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
        validated = PersonaOutput(**parsed)
        output = validated.model_dump()
        output["status"] = status
        output["duration_ms"] = duration_ms
        return output
    except Exception as exc:
        print(f"[persona_agent] Error: {exc}. Falling back to mock personas.")
        res = _generate_mock_personas(idea)
        res["status"] = "failed"
        res["duration_ms"] = int((time.perf_counter() - start_time) * 1000)
        return res
