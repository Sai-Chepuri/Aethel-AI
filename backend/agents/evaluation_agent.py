import config
import os
import json
import time
from google import genai
from google.genai import types
from schemas.response_schema import ProductEvaluation
from utils.mock_helper import get_mock_context

def _get_prompt(idea: str, plan_context: dict) -> str:
    current_dir = os.path.dirname(os.path.abspath(__file__))
    prompt_path = os.path.join(current_dir, "..", "prompts", "evaluation_prompt.txt")
    with open(prompt_path, "r", encoding="utf-8") as f:
        template = f.read()
    
    return template.format(
        idea=idea,
        market_research=json.dumps(plan_context.get("market_research", {}), indent=2),
        competitors=json.dumps(plan_context.get("competitors", []), indent=2),
        personas=json.dumps(plan_context.get("personas", []), indent=2),
        prd=json.dumps(plan_context.get("prd", {}), indent=2),
        roadmap=json.dumps(plan_context.get("roadmap", {}), indent=2),
        risks=json.dumps(plan_context.get("risks", []), indent=2),
        kpis=json.dumps(plan_context.get("kpis", {}), indent=2)
    )

def _generate_mock_evaluation(idea: str) -> dict:
    ctx = get_mock_context(idea)
    product_name = ctx.get("product_name", "The product")
    category = ctx.get("category", "strategy plan")
    
    # Determine the category key based on keywords
    lower = idea.lower()
    if any(k in lower for k in ["ai", "gpt", "llm", "model", "intelligence", "agent", "automation"]):
        key = "ai"
    elif any(k in lower for k in ["pet", "dog", "cat", "animal", "vet", "collar", "leash"]):
        key = "pet"
    elif any(k in lower for k in ["food", "restaurant", "cook", "delivery", "meal", "eat", "grocery"]):
        key = "food"
    elif any(k in lower for k in ["finance", "money", "budget", "invest", "crypto", "wallet", "savings"]):
        key = "finance"
    elif any(k in lower for k in ["fit", "health", "gym", "workout", "wellness", "sleep", "mindfulness", "meditate", "yoga"]):
        key = "health"
    elif any(k in lower for k in ["educat", "school", "learn", "course", "student", "class", "tutor"]):
        key = "education"
    elif any(k in lower for k in ["shop", "store", "sell", "commerce", "marketplace", "vendor", "retail"]):
        key = "ecommerce"
    else:
        key = "saas"

    critiques = {
        "pet": {
            "alignment": {
                "score": 9,
                "strengths": [
                    f"Directly addresses pet owner anxiety regarding health metrics for {product_name}.",
                    "Integrates veterinary sharing goals directly into the PRD requirements."
                ],
                "improvement_areas": [
                    "Could offer more options for cat owners in the initial Phase 1 launch.",
                    "Persona goals focus heavily on urban users."
                ]
            },
            "feasibility": {
                "score": 7,
                "strengths": [
                    "Phased release structure separates hardware/sensor validation from cloud API features.",
                    "Proper mitigation strategies for GPS battery consumption."
                ],
                "improvement_areas": [
                    "Initial LTE cellular roaming cost assumptions are highly optimistic.",
                    "IP68 hardware waterproofing is expensive to prototype in Week 4."
                ]
            },
            "completeness": {
                "score": 8,
                "strengths": [
                    "All user stories include detailed acceptance criteria scenarios.",
                    "KPI metrics list comprehensive activation targets."
                ],
                "improvement_areas": [
                    "Needs direct SLA targets for data sync frequencies.",
                    "Lacks concrete marketing acquisition channels."
                ]
            },
            "overall_recommendations": [
                "Establish veterinary clinic partnerships to test the PDF export reporting early.",
                "Build a local WiFi-only tracking prototype before finalizing expensive cellular firmware.",
                "Offer pre-sales discounts to pet insurance networks to subsidize customer acquisition costs."
            ]
        },
        "ai": {
            "alignment": {
                "score": 9,
                "strengths": [
                    f"Strong focus on eliminating operational bottlenecks for developers using {product_name}.",
                    "Direct alignment with developer scenarios and audit logging security requirements."
                ],
                "improvement_areas": [
                    "Prompt validation requirements could be expanded for enterprise compliance.",
                    "Sarah Jenkins persona could detail more command-line interactions."
                ]
            },
            "feasibility": {
                "score": 8,
                "strengths": [
                    "Builds on lightweight API wrapper layers in Phase 1 before scaling self-hosted models.",
                    "Excellent mitigation of pricing pressure through workflow utility billing."
                ],
                "improvement_areas": [
                    "Model bias mitigation requires complex offline rules engine logic.",
                    "Phase 3 fine-tuning depends on custom training data pipelines."
                ]
            },
            "completeness": {
                "score": 9,
                "strengths": [
                    "Comprehensive coverage of security guardrails and SOC-2 standard targets.",
                    "AARRR KPIs contain precise metric goals (e.g. < 60s first execution)."
                ],
                "improvement_areas": [
                    "Missing detailed API error handling stories.",
                    "Acceptance criteria could specify CLI flag behaviors."
                ]
            },
            "overall_recommendations": [
                "Open-source the CLI runner to foster early community adoption and developer trust.",
                "Implement tight token spending guardrails per API key to prevent runaway test billings.",
                "Integrate with popular developer chat clients (like Slack or Teams) to hook notifications early."
            ]
        },
        "saas": {
            "alignment": {
                "score": 8,
                "strengths": [
                    f"Good alignment with the B2B SaaS target audience requirements for {product_name}.",
                    "Addresses standard core platform requirements in PRD."
                ],
                "improvement_areas": [
                    "Strategy is slightly generic and could address niche workflow customisation.",
                    "Target persona could specify job functions in more detail."
                ]
            },
            "feasibility": {
                "score": 8,
                "strengths": [
                    "Phased release structure relies on standard web technology stacks.",
                    "No immediate custom hardware or heavy computing dependencies."
                ],
                "improvement_areas": [
                    "Over-reliance on rapid developer execution schedules in Phase 1.",
                    "High initial customer acquisition costs (CAC) might disrupt funding timelines."
                ]
            },
            "completeness": {
                "score": 8,
                "strengths": [
                    "Standard functional requirements and non-functional requirements are fully documented.",
                    "KPIs map clearly to standard product dashboard indicators."
                ],
                "improvement_areas": [
                    "Roadmap phases do not include marketing launch milestones.",
                    "Risk mitigation could list regulatory compliance considerations."
                ]
            },
            "overall_recommendations": [
                "Define a narrow initial niche segment to pilot the platform rather than general B2B.",
                "Implement self-serve onboarding guides to minimize activation friction.",
                "Establish customer advisory councils with early sign-ups to direct Phase 2 requirements."
            ]
        }
    }
    
    category_data = critiques.get(key, critiques["saas"])
    
    def replace_strings(node):
        if isinstance(node, dict):
            return {k: replace_strings(v) for k, v in node.items()}
        elif isinstance(node, list):
            return [replace_strings(x) for x in node]
        elif isinstance(node, str):
            return node.replace("{product_name}", product_name).replace("{category}", category)
        return node
        
    return {
        "evaluation": replace_strings(category_data)
    }

async def run_evaluation_agent(idea: str, plan_context: dict) -> dict:
    start_time = time.perf_counter()
    status = "completed"
    
    try:
        client = genai.Client(api_key=os.getenv("GEMINI_API_KEY"))
        prompt_content = _get_prompt(idea, plan_context)
        from utils.gemini_client import generate_content_with_fallback
        response = await generate_content_with_fallback(
            client,
            prompt_content,
            types.GenerateContentConfig(
                response_mime_type="application/json",
                response_schema=ProductEvaluation
            )
        )
        duration_ms = int((time.perf_counter() - start_time) * 1000)
        
        if hasattr(response, "parsed") and response.parsed:
            output = response.parsed.model_dump()
            return {
                "evaluation": output,
                "status": status,
                "duration_ms": duration_ms
            }
            
        # Fallback parsing
        from services.gemini_service import _extract_and_parse_json
        parsed = _extract_and_parse_json(response.text)
        validated = ProductEvaluation(**parsed)
        return {
            "evaluation": validated.model_dump(),
            "status": status,
            "duration_ms": duration_ms
        }
    except Exception as exc:
        print(f"[evaluation_agent] Error: {exc}. Falling back to mock evaluation.")
        res = _generate_mock_evaluation(idea)
        res["status"] = "failed"
        res["duration_ms"] = int((time.perf_counter() - start_time) * 1000)
        return res
