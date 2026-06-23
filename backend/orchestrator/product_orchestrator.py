import sys
import os

# Ensure backend directory is in python path so imports work correctly
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from agents.research_agent import run_research_agent
from agents.persona_agent import run_persona_agent
from agents.prd_agent import run_prd_agent
from agents.roadmap_agent import run_roadmap_agent
from agents.risk_agent import run_risk_agent
from agents.metrics_agent import run_metrics_agent
from agents.evaluation_agent import run_evaluation_agent

async def generate_product_plan(idea: str) -> dict:
    """
    Orchestrate the generation of a complete product plan using a sequence of specialized agents.
    
    1. Research Agent: Analyzes market & competitors.
    2. Persona Agent: Designs target user personas based on research.
    3. PRD Agent: Drafts product requirements, user stories, and acceptance criteria based on research and personas.
    4. Roadmap Agent: Outlines a release timeline based on PRD requirements.
    5. Risk Agent: Identifies risks and mitigation strategies.
    6. Metrics Agent: Formulates success KPIs.
    """
    import asyncio

    # 1. Run Research Agent
    research_res = await run_research_agent(idea)
    
    # 2. Run Persona Agent (utilizing Research output)
    personas_res = await run_persona_agent(idea, research_res)
    
    # 3. Run PRD Agent (utilizing Research and Persona outputs)
    prd_res = await run_prd_agent(idea, research_res, personas_res)
    
    # Define parallel branches after PRD is ready
    async def run_roadmap_and_risks_branch():
        roadmap_result = await run_roadmap_agent(idea, prd_res)
        prd_and_roadmap_context = {
            "prd": prd_res.get("prd"),
            "roadmap": roadmap_result.get("roadmap")
        }
        risks_result = await run_risk_agent(idea, prd_and_roadmap_context)
        return roadmap_result, risks_result

    async def run_metrics_branch():
        return await run_metrics_agent(idea, prd_res)

    # Run the independent Roadmap+Risks sequence in parallel with the Metrics Agent
    (roadmap_res, risks_res), metrics_res = await asyncio.gather(
        run_roadmap_and_risks_branch(),
        run_metrics_branch()
    )
    
    # Merge context and run the Evaluation Agent sequentially
    plan_context = {
        "market_research": research_res.get("market_research"),
        "competitors": research_res.get("competitors"),
        "personas": personas_res.get("personas"),
        "prd": prd_res.get("prd"),
        "roadmap": roadmap_res.get("roadmap"),
        "risks": risks_res.get("risks"),
        "kpis": metrics_res.get("kpis")
    }
    
    print("[orchestrator] Running Evaluation Agent on compiled strategy...")
    evaluation_res = await run_evaluation_agent(idea, plan_context)
    
    print("[orchestrator] Agent execution complete. Aggregating results...")
    
    # Compile final plan structure matching ProductPlanResponse
    full_plan = {
        "market_research": research_res.get("market_research"),
        "competitors": research_res.get("competitors"),
        "personas": personas_res.get("personas"),
        "prd": prd_res.get("prd"),
        "user_stories": prd_res.get("user_stories"),
        "acceptance_criteria": prd_res.get("acceptance_criteria"),
        "roadmap": roadmap_res.get("roadmap"),
        "risks": risks_res.get("risks"),
        "kpis": metrics_res.get("kpis"),
        "evaluation": evaluation_res.get("evaluation"),

        # Agent execution metadata
        "research_status": research_res.get("status", "completed"),
        "research_duration_ms": research_res.get("duration_ms", 0),
        "persona_status": personas_res.get("status", "completed"),
        "persona_duration_ms": personas_res.get("duration_ms", 0),
        "prd_status": prd_res.get("status", "completed"),
        "prd_duration_ms": prd_res.get("duration_ms", 0),
        "roadmap_status": roadmap_res.get("status", "completed"),
        "roadmap_duration_ms": roadmap_res.get("duration_ms", 0),
        "risk_status": risks_res.get("status", "completed"),
        "risk_duration_ms": risks_res.get("duration_ms", 0),
        "metrics_status": metrics_res.get("status", "completed"),
        "metrics_duration_ms": metrics_res.get("duration_ms", 0),
        "evaluation_status": evaluation_res.get("status", "completed"),
        "evaluation_duration_ms": evaluation_res.get("duration_ms", 0),
        "source_attributions": research_res.get("source_attributions", []),

        # Trace of execution sequence
        "execution_trace": [
            f"Research Agent execution: status={research_res.get('status', 'completed')}, duration={research_res.get('duration_ms', 0)}ms",
            f"Persona Agent execution: status={personas_res.get('status', 'completed')}, duration={personas_res.get('duration_ms', 0)}ms",
            f"PRD Agent execution: status={prd_res.get('status', 'completed')}, duration={prd_res.get('duration_ms', 0)}ms",
            f"Roadmap Agent execution: status={roadmap_res.get('status', 'completed')}, duration={roadmap_res.get('duration_ms', 0)}ms",
            f"Risk Agent execution: status={risks_res.get('status', 'completed')}, duration={risks_res.get('duration_ms', 0)}ms",
            f"Metrics Agent execution: status={metrics_res.get('status', 'completed')}, duration={metrics_res.get('duration_ms', 0)}ms",
            f"Evaluation Agent execution: status={evaluation_res.get('status', 'completed')}, duration={evaluation_res.get('duration_ms', 0)}ms"
        ]
    }
    
    return full_plan
