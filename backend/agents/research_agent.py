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
    product_name = ctx["product_name"]
    cat = ctx["category"]
    audience = ctx["audience"]
    problem = ctx["problem"]
    a, b, c = ctx["competitors_list"]

    market_research = {
        "executive_summary": f"**{product_name}** enters the market as a disruptive **{cat}** targeting a critical friction point: {problem}. The segment shows high-growth indicators driven by modern UX expectations and API-first integrations.",
        "market_trends": [
            "AI & Self-Service: Customers demand automated insights over raw data dashboards.",
            "Privacy Regulation: GDPR and CCPA require transparent, encrypted data governance.",
            "Hyper-Personalisation: Algorithms and interfaces must adapt to individual user behaviour."
        ],
        "market_sizing": {
            "tam": "$12.5 B",
            "sam": "$2.4 B",
            "som": "$85 M",
            "rationale": f"Calculated based on global {cat} demand patterns and initial GTM focus on {audience}."
        },
        "swot": {
            "strengths": ["Modern architecture", "AI-first design", "Rapid iteration cycle"],
            "weaknesses": ["Early brand recognition", "Dependence on third-party APIs"],
            "opportunities": [f"Growing demand for automated toolchains among {audience}"],
            "threats": ["Fast followers from incumbents", "Commoditisation of AI features"]
        }
    }

    competitors = [
        {
            "name": a,
            "strengths": ["Large user base", "Brand trust"],
            "weaknesses": ["Legacy UX", "Slow onboarding"],
            "differentiation": "10× faster setup, zero-config defaults"
        },
        {
            "name": b,
            "strengths": ["Rich integrations", "Workflow engine"],
            "weaknesses": ["High licence cost", "Bloated UI"],
            "differentiation": "Modular pricing, lightweight client"
        },
        {
            "name": c,
            "strengths": ["Broad feature set", "Aggressive marketing"],
            "weaknesses": ["Steep learning curve", "Poor mobile UX"],
            "differentiation": "AI-guided onboarding, responsive design"
        }
    ]

    return {
        "market_research": market_research,
        "competitors": competitors
    }

async def run_research_agent(idea: str, api_key: str = None) -> dict:
    start_time = time.perf_counter()
    status = "completed"

    if not api_key:
        print("[research_agent] No API key configured. Falling back to mock generator.")
        res = _generate_mock_research(idea)
        res["status"] = status
        res["duration_ms"] = int((time.perf_counter() - start_time) * 1000)
        return res

    try:
        client = genai.Client(api_key=api_key)
        
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
        search_findings = await google_search(search_prompt, api_key)
        print("[research_agent] Grounding search complete. Extracted competitor information.")

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
            return output
        
        # Fallback parsing
        from services.gemini_service import _extract_and_parse_json
        parsed = _extract_and_parse_json(response.text)
        validated = ResearchOutput(**parsed)
        output = validated.model_dump()
        output["status"] = status
        output["duration_ms"] = duration_ms
        return output
    except Exception as exc:
        print(f"[research_agent] Error: {exc}. Falling back to mock research.")
        res = _generate_mock_research(idea)
        res["status"] = "failed"
        res["duration_ms"] = int((time.perf_counter() - start_time) * 1000)
        return res
