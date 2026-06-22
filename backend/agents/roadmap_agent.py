import os
import json
import time
from google import genai
from google.genai import types
from schemas.response_schema import RoadmapOutput
from utils.mock_helper import get_mock_context

def _get_prompt(idea: str, prd_context: dict) -> str:
    current_dir = os.path.dirname(os.path.abspath(__file__))
    prompt_path = os.path.join(current_dir, "..", "prompts", "roadmap_prompt.txt")
    with open(prompt_path, "r", encoding="utf-8") as f:
        template = f.read()

    prd_str = json.dumps(prd_context, indent=2)
    return template.format(idea=idea, prd_context=prd_str)

def _generate_mock_roadmap(idea: str) -> dict:
    ctx = get_mock_context(idea)
    product_name = ctx["product_name"]

    roadmap = {
        "phases": [
            {
                "phase_name": "Phase 1: MVP",
                "focus": "Core content generator engine, polished dark-mode dashboard, text exports.",
                "milestones": ["FastAPI backend with mock fallback", "Semantic HTML5 dashboard UI", "Copy & Export features"],
                "timeline": "Weeks 1-4"
            },
            {
                "phase_name": "Phase 2: Collaboration",
                "focus": "User accounts, team collaboration workspace, and strategy templates.",
                "milestones": ["Social login / magic-link auth", "Secure read-only share URLs", "Gantt chart visualiser"],
                "timeline": "Months 2-3"
            },
            {
                "phase_name": "Phase 3: Scale",
                "focus": "Deep AI capabilities, enterprise integrations, global reach.",
                "milestones": ["AI chat assistant panel", "Native Slack & Jira extensions", "Localised UI in 6 languages"],
                "timeline": "Months 4-6"
            }
        ],
        "mermaid_gantt": f"""gantt
    title {product_name} Release Timeline
    dateFormat  YYYY-MM-DD
    section Phase 1 · MVP
    Architecture & Design         :a1, 2026-07-01, 10d
    Core Generator + Dashboard UI :after a1, 15d
    Beta Testing (50 users)       :2026-07-25, 7d
    section Phase 2 · Growth
    Auth & Team Workspaces        :2026-08-01, 20d
    Share Links & RBAC            :2026-08-15, 10d
    section Phase 3 · Scale
    AI Chat Assistant Panel       :2026-09-01, 20d
    Slack / Jira Integrations     :2026-09-15, 15d
    i18n (6 languages)            :2026-10-01, 20d"""
    }

    return {
        "roadmap": roadmap
    }

async def run_roadmap_agent(idea: str, prd_context: dict, api_key: str = None) -> dict:
    start_time = time.perf_counter()
    status = "completed"

    if not api_key:
        print("[roadmap_agent] No API key configured. Falling back to mock generator.")
        res = _generate_mock_roadmap(idea)
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
                response_schema=RoadmapOutput
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
        validated = RoadmapOutput(**parsed)
        output = validated.model_dump()
        output["status"] = status
        output["duration_ms"] = duration_ms
        return output
    except Exception as exc:
        print(f"[roadmap_agent] Error: {exc}. Falling back to mock roadmap.")
        res = _generate_mock_roadmap(idea)
        res["status"] = "failed"
        res["duration_ms"] = int((time.perf_counter() - start_time) * 1000)
        return res
