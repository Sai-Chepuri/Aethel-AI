import os
import re
import json
from typing import Dict

from google import genai
from google.genai import types
from pydantic import BaseModel


# ---------------------------------------------------------------------------
# Internal structured schema — maps exactly to ProductPlan response fields
# ---------------------------------------------------------------------------

from schemas.response_schema import ProductPlanResponse
_ProductPlanSchema = ProductPlanResponse


# ---------------------------------------------------------------------------
# System prompt shared by both the live and any future fine-tuned path
# ---------------------------------------------------------------------------

_SYSTEM_PROMPT = (
    "You are a world-class Product Management expert. "
    "Take the product idea provided and generate a comprehensive, highly detailed "
    "product launch package. "
    "For every field write detailed, professional, structured Markdown — "
    "use headings, subheadings, bullet points, and tables where appropriate. "
    "Be highly specific to the product idea. "
    "Do NOT use generic placeholders. "
    "All content must be ready to present to stakeholders."
)


# ---------------------------------------------------------------------------
# Public entry point
# ---------------------------------------------------------------------------

async def generate_product_plan(idea: str) -> Dict[str, any]:
    """
    Generate a structured product plan for the given idea.

    Uses the google-genai SDK with gemini-2.5-flash when GEMINI_API_KEY is
    configured; otherwise falls back to the high-quality local mock generator.

    Args:
        idea: Plain-text product idea / concept.

    Returns:
        Dict matching ProductPlanResponse.
    """
    api_key = os.getenv("GEMINI_API_KEY", "").strip()

    if api_key:
        # If API key is configured, call the live SDK (which retries once and extracts JSON).
        # We propagate any error so that the API returns the error object to the client.
        return await _generate_with_sdk(idea, api_key)

    return _generate_mock_plan(idea)


def _load_prompt_template(idea: str) -> str:
    """Load the prompt template from backend/prompts/product_plan_prompt.txt and format it."""
    try:
        current_dir = os.path.dirname(os.path.abspath(__file__))
        prompt_path = os.path.join(current_dir, "..", "prompts", "product_plan_prompt.txt")
        if os.path.exists(prompt_path):
            with open(prompt_path, "r", encoding="utf-8") as f:
                template = f.read()
            return template.format(idea=idea)
    except Exception as exc:
        print(f"[gemini_service] Error loading prompt template: {exc}")
    
    # Fallback default user prompt
    return f"Generate a complete product plan for the following product idea: \"{idea}\""


# ---------------------------------------------------------------------------
# Live Gemini path (google-genai SDK)
# ---------------------------------------------------------------------------

def _extract_and_parse_json(text: str) -> dict:
    """Helper to extract and parse JSON from Gemini's response text."""
    trimmed = text.strip()
    # Try parsing directly first
    try:
        return json.loads(trimmed)
    except json.JSONDecodeError:
        pass

    # Attempt to extract JSON from Markdown code blocks (e.g. ```json ... ```)
    markdown_match = re.search(
        r"```(?:json)?\s*(\{.*?\})\s*```", trimmed, re.DOTALL | re.IGNORECASE
    )
    if markdown_match:
        try:
            return json.loads(markdown_match.group(1).strip())
        except json.JSONDecodeError:
            pass

    # Find first '{' and matching final '}'
    brace_match = re.search(r"(\{.*\})", trimmed, re.DOTALL)
    if brace_match:
        try:
            return json.loads(brace_match.group(1).strip())
        except json.JSONDecodeError:
            pass

    raise ValueError("Response text does not contain valid JSON.")


# ---------------------------------------------------------------------------
# Live Gemini path (google-genai SDK)
# ---------------------------------------------------------------------------

async def _generate_with_sdk(idea: str, api_key: str) -> Dict[str, any]:
    """Call Gemini 2.5 Flash via the official google-genai async SDK with retries and extraction."""

    client = genai.Client(api_key=api_key)

    user_prompt = _load_prompt_template(idea)

    last_error = None
    for attempt in range(1, 3):
        try:
            print(f"[gemini_service] Live generation attempt {attempt}/2...")
            response = await client.aio.models.generate_content(
                model="gemini-2.5-flash",
                contents=user_prompt,
                config=types.GenerateContentConfig(
                    system_instruction=_SYSTEM_PROMPT,
                    response_mime_type="application/json",
                    response_schema=_ProductPlanSchema,
                ),
            )

            # Check if SDK parsed it automatically
            if hasattr(response, "parsed") and response.parsed:
                return response.parsed.model_dump()

            # Fall back to text parsing if response.parsed is not available or validation failed
            text = response.text
            if not text:
                raise ValueError("Received an empty response from Gemini API.")

            parsed_data = _extract_and_parse_json(text)
            validated = _ProductPlanSchema(**parsed_data)
            return validated.model_dump()

        except Exception as exc:
            last_error = exc
            print(f"[gemini_service] Attempt {attempt}/2 failed: {exc}")
            if attempt < 2:
                continue

    raise ValueError(f"Failed to generate a valid product plan matching the schema: {last_error}")


# ---------------------------------------------------------------------------
# Local mock generator (no API key required)
# ---------------------------------------------------------------------------

def _generate_mock_plan(idea: str) -> Dict[str, any]:
    """
    Produce a high-quality, category-aware product plan without an API call.
    Detects product category from keywords and customises every section.
    """
    clean = re.sub(r"['\"]", "", idea).strip()

    # Derive a short product name -----------------------------------------------
    name_match = (
        re.search(r"called\s+([A-Za-z0-9 _-]+)", clean, re.I)
        or re.search(r"named?\s+([A-Za-z0-9 _-]+)", clean, re.I)
        or re.search(r"^([A-Za-z0-9 _-]{3,25})", clean)
    )
    if name_match:
        product_name = name_match.group(1).strip().title()
    else:
        product_name = " ".join(w.capitalize() for w in clean.split()[:3]) + " App"

    # Category detection --------------------------------------------------------
    lower = clean.lower()

    if any(k in lower for k in ["ai", "gpt", "llm", "model", "intelligence"]):
        cat, audience = "AI-Powered System", "Developers, Enterprises & Creators"
        problem = "time-consuming manual analysis, high cognitive load, and slow content workflows"
        comp = ("OpenAI Enterprise", "Anthropic Claude", "Copy.ai / Jasper")
    elif any(k in lower for k in ["food", "restaurant", "cook", "delivery", "meal"]):
        cat, audience = "FoodTech Service", "Busy Urban Dwellers & Families"
        problem = "difficulty finding healthy meals, long prep times, and high delivery fees"
        comp = ("Uber Eats", "HelloFresh", "DoorDash")
    elif any(k in lower for k in ["finance", "money", "budget", "invest", "crypto"]):
        cat, audience = "Fintech Application", "Retail Investors & Budget-Conscious Individuals"
        problem = "complex portfolio management, hidden fees, and poor financial literacy tools"
        comp = ("Robinhood", "Mint / Copilot", "Acorns")
    elif any(k in lower for k in ["fit", "health", "gym", "workout", "pet", "wellness"]):
        cat, audience = "Health & Wellness Platform", "Health Enthusiasts & Active Individuals"
        problem = "fragmented trackers, no personalised plans, and low long-term motivation"
        comp = ("MyFitnessPal", "Strava", "Whoop / Apple Health")
    elif any(k in lower for k in ["educat", "school", "learn", "course", "student"]):
        cat, audience = "EdTech Platform", "Students, Lifelong Learners & Educators"
        problem = "rigid course structures, lack of interactive feedback, and high tuition costs"
        comp = ("Duolingo", "Coursera", "Quizlet / Udemy")
    elif any(k in lower for k in ["shop", "store", "sell", "commerce", "marketplace"]):
        cat, audience = "E-commerce Marketplace", "Online Vendors & Convenience Seekers"
        problem = "complex checkout flows, high transaction fees, and poor supplier transparency"
        comp = ("Shopify", "Etsy", "Amazon Seller Central")
    else:
        cat, audience = "SaaS Platform", "Business Professionals & Teams"
        problem = "inefficient workflows and lack of centralised collaboration tooling"
        comp = ("Atlassian Jira", "Monday.com", "ClickUp")

    a, b, c = comp

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

    risks = [
        {
            "description": "Incumbents replicating features",
            "category": "Market",
            "impact": "High",
            "probability": "Medium",
            "mitigation": "Build strong data-portability and developer integration hooks to lock-in utility."
        },
        {
            "description": "API rate limiting/outages",
            "category": "Technical",
            "impact": "High",
            "probability": "High",
            "mitigation": "Graceful offline and cache fallbacks (mock engines) as implemented in MVP."
        },
        {
            "description": f"Slow adoption by {audience}",
            "category": "Project",
            "impact": "Medium",
            "probability": "Low",
            "mitigation": "Run early beta programs (50+ users) to align UI and value-add before public launch."
        },
        {
            "description": "Compliance & GDPR hurdles",
            "category": "Legal",
            "impact": "High",
            "probability": "Medium",
            "mitigation": "Store all customer API keys server-side; do not log user prompts on persistent DBs."
        }
    ]

    kpis = {
        "acquisition": [
            {"metric": "Visitor -> Generator conversion", "target": "> 12%", "notes": "Landing page CTA click-through"},
            {"metric": "Customer Acquisition Cost (CAC)", "target": "< $18", "notes": "Blended paid + organic"},
            {"metric": "Organic traffic share", "target": "> 45%", "notes": "SEO + referrals"}
        ],
        "activation": [
            {"metric": "Time-to-Value (TTV)", "target": "< 90 s", "notes": "First plan rendered in under 90s"},
            {"metric": "First-day export rate", "target": "> 60%", "notes": "Users copying/downloading on day 1"},
            {"metric": "Onboarding completion", "target": "> 85%", "notes": "Completing 3-step tour"}
        ],
        "retention": [
            {"metric": "Month-1 retention (M1)", "target": "> 28%", "notes": "Users returning in week 5+"},
            {"metric": "Weekly Active Users (WAU)", "target": "Growing MoM", "notes": "Absolute count"},
            {"metric": "Avg. session duration", "target": "> 8 min", "notes": "Time spent reviewing plans"}
        ],
        "revenue": [
            {"metric": "ARPU", "target": "$29 / month", "notes": "Pro tier subscription"},
            {"metric": "LTV / CAC ratio", "target": "> 3.5×", "notes": "Healthy unit economics threshold"},
            {"metric": "Seat expansion rate", "target": "> 15%", "notes": "Users adding >= 3 collaborators"}
        ]
    }

    return {
        "market_research": market_research,
        "competitors": competitors,
        "personas": personas,
        "prd": prd,
        "user_stories": user_stories,
        "acceptance_criteria": acceptance_criteria,
        "roadmap": roadmap,
        "risks": risks,
        "kpis": kpis,
    }
