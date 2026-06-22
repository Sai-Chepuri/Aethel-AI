"""
Unit test for POST /generate — validates request/response contract.
Calls generate_product_plan() directly (no HTTP, no server needed).
"""
import sys, os, asyncio

sys.path.insert(0, os.path.join(os.path.dirname(__file__)))
os.chdir(os.path.dirname(__file__))

from schemas.response_schema import ProductPlanResponse, GenerateResponse
from models.product_idea import ProductIdea
from orchestrator.product_orchestrator import generate_product_plan

async def run():
    # ── 1. Input model validates correctly ───────────────────────────────────
    idea = ProductIdea(idea="A fintech app for micro-investing spare change")
    assert idea.idea == "A fintech app for micro-investing spare change"
    print("✓ ProductIdea(idea=...) instantiates correctly")

    # ── 2. generate_product_plan returns all required fields ─────────────────
    plan_data = await generate_product_plan(idea.idea)
    expected = {
        "market_research",
        "competitors",
        "personas",
        "prd",
        "user_stories",
        "acceptance_criteria",
        "roadmap",
        "risks",
        "kpis",
        "research_status",
        "research_duration_ms",
        "persona_status",
        "persona_duration_ms",
        "prd_status",
        "prd_duration_ms",
        "roadmap_status",
        "roadmap_duration_ms",
        "risk_status",
        "risk_duration_ms",
        "metrics_status",
        "metrics_duration_ms"
    }
    assert set(plan_data.keys()) == expected, f"Unexpected keys: {plan_data.keys()}"
    print("✓ generate_product_plan() returns all 9 fields")

    # ── 3. ProductPlanResponse validates the returned dict ────────────────────
    plan = ProductPlanResponse(**plan_data)
    assert len(plan.market_research.executive_summary) > 20
    assert len(plan.competitors) >= 2
    assert len(plan.personas) >= 2
    assert len(plan.prd.functional_requirements) >= 2
    assert len(plan.user_stories) >= 2
    assert len(plan.acceptance_criteria) >= 2
    assert len(plan.roadmap.phases) >= 2
    assert len(plan.risks) >= 2
    assert len(plan.kpis.acquisition) >= 2
    print("✓ ProductPlanResponse(**plan_data) validates correctly")

    # ── 4. GenerateResponse wraps plan under 'result' key ────────────────────
    response = GenerateResponse(result=plan)
    serialised = response.model_dump()
    assert list(serialised.keys()) == ["result"], \
        f"Expected top-level key 'result', got: {list(serialised.keys())}"
    assert set(serialised["result"].keys()) == expected
    print("✓ GenerateResponse serialises to {\"result\": {...}}")

    # ── 5. JSON Extraction & Error Handling ───────────────────────────────────
    from services.gemini_service import _extract_and_parse_json

    # Test direct JSON
    assert _extract_and_parse_json('{"key": "value"}') == {"key": "value"}

    # Test Markdown code block format
    assert _extract_and_parse_json('```json\n{"key": "value"}\n```') == {"key": "value"}

    # Test Markdown code block without json tag
    assert _extract_and_parse_json('```\n{"key": "value"}\n```') == {"key": "value"}

    # Test JSON wrapped in text
    assert _extract_and_parse_json('Plan data: {"key": "value"} End of file.') == {"key": "value"}

    # Test invalid JSON raises ValueError
    try:
        _extract_and_parse_json('invalid string')
        assert False, "Should have raised ValueError"
    except ValueError:
        pass

    print("✓ JSON extraction and error handling logic validates correctly")

    # ── 6. Save Output Utility ────────────────────────────────────────────────
    from utils.save_output import save_generated_plan
    import json
    
    saved_path = save_generated_plan(plan_data)
    assert os.path.exists(saved_path), f"Saved file does not exist: {saved_path}"
    with open(saved_path, "r", encoding="utf-8") as f:
        loaded_data = json.load(f)
    assert loaded_data == plan_data, "Loaded data does not match original plan data"
    print("✓ save_generated_plan() utility successfully writes output JSON")

    # Remove the test-created JSON file to keep outputs clean
    try:
        os.remove(saved_path)
    except Exception:
        pass

    # ── 7. Report ─────────────────────────────────────────────────────────────
    print()
    print("Response shape:")
    print(f"  Top-level keys : {list(serialised.keys())}")
    print(f"  result keys    : {sorted(serialised['result'].keys())}")
    print()
    print("All assertions passed ✓")

asyncio.run(run())
