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
    product_name = ctx["product_name"]
    cat = ctx["category"]

    prd = {
        "purpose_scope": f"This PRD defines the MVP requirements for **{product_name}** ({cat}). It guides cross-functional teams through design, engineering, and QA phases.",
        "goals_success_criteria": [
            {"objective": "Fast time-to-value", "measurable_target": "First meaningful output in < 90 seconds"},
            {"objective": "Performance", "measurable_target": "LCP < 2.0 s, INP < 150 ms"},
            {"objective": "Accessibility", "measurable_target": "WCAG 2.1 AA compliance"}
        ],
        "functional_requirements": [
            "Resizable textarea with live character count.",
            "One-click quick-fill templates for common categories.",
            "Nine named tabs with smooth transitions.",
            "Copy Section and Export Full Plan buttons."
        ],
        "non_functional_requirements": [
            "Security: All API keys stored server-side.",
            "Performance: 99th-percentile server response < 5 s.",
            "Resilience: Graceful fallback to local mock if API is unavailable."
        ]
    }

    user_stories = [
        {
            "story_id": "US-01",
            "user_role": "Sarah",
            "action": "submit my idea in plain text",
            "benefit": "I instantly receive a structured execution outline"
        },
        {
            "story_id": "US-02",
            "user_role": "Sarah",
            "action": "filter outputs by category or timeline",
            "benefit": "I can focus on immediate actionable items without clutter"
        },
        {
            "story_id": "US-03",
            "user_role": "Marcus",
            "action": "view security settings and exports",
            "benefit": "I can download system states for executive reports"
        },
        {
            "story_id": "US-04",
            "user_role": "Developer",
            "action": "access standard API keys and endpoints",
            "benefit": "my team can integrate outputs into automated pipelines"
        }
    ]

    acceptance_criteria = [
        {
            "story_id": "US-01",
            "scenarios": [
                "Given the user is on the console, When they enter a valid concept and click Forge, Then progress checklist animates and the 9-tab dashboard is populated."
            ]
        },
        {
            "story_id": "US-02",
            "scenarios": [
                "Given a plan has been generated, When the user clicks any inactive tab, Then that tab becomes active and displays the correct Markdown content."
            ]
        },
        {
            "story_id": "US-03",
            "scenarios": [
                "Given a plan is loaded, When the user clicks Export Full Plan, Then a .md file is compiled containing all 9 sections in sequence and downloaded."
            ]
        }
    ]

    return {
        "prd": prd,
        "user_stories": user_stories,
        "acceptance_criteria": acceptance_criteria
    }

async def run_prd_agent(idea: str, market_research_context: dict, personas_context: dict, api_key: str = None) -> dict:
    start_time = time.perf_counter()
    status = "completed"

    if not api_key:
        print("[prd_agent] No API key configured. Falling back to mock generator.")
        res = _generate_mock_prd(idea)
        res["status"] = status
        res["duration_ms"] = int((time.perf_counter() - start_time) * 1000)
        return res

    try:
        client = genai.Client(api_key=api_key)
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
