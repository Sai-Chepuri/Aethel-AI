from pydantic import BaseModel

# --- Market Research ---
class MarketSizing(BaseModel):
    tam: str
    sam: str
    som: str
    rationale: str

class SWOTAnalysis(BaseModel):
    strengths: list[str]
    weaknesses: list[str]
    opportunities: list[str]
    threats: list[str]

class MarketResearch(BaseModel):
    executive_summary: str
    market_trends: list[str]
    market_sizing: MarketSizing
    swot: SWOTAnalysis

# --- Competitors ---
class Competitor(BaseModel):
    name: str
    strengths: list[str]
    weaknesses: list[str]
    differentiation: str

# --- Personas ---
class UserPersona(BaseModel):
    name: str
    role: str
    age: str
    goals: list[str]
    pain_points: list[str]
    user_scenario: str

# --- PRD ---
class GoalsAndSuccessCriteria(BaseModel):
    objective: str
    measurable_target: str

class PRD(BaseModel):
    purpose_scope: str
    goals_success_criteria: list[GoalsAndSuccessCriteria]
    functional_requirements: list[str]
    non_functional_requirements: list[str]

# --- User Stories ---
class UserStory(BaseModel):
    story_id: str
    user_role: str
    action: str
    benefit: str

# --- Acceptance Criteria ---
class AcceptanceCriteria(BaseModel):
    story_id: str
    scenarios: list[str]

# --- Roadmap ---
class RoadmapPhase(BaseModel):
    phase_name: str
    focus: str
    milestones: list[str]
    timeline: str

class Roadmap(BaseModel):
    phases: list[RoadmapPhase]
    mermaid_gantt: str

# --- Risks ---
class ProductRisk(BaseModel):
    description: str
    category: str
    impact: str
    probability: str
    mitigation: str

# --- KPIs ---
class KPIMetric(BaseModel):
    metric: str
    target: str
    notes: str

class KPIs(BaseModel):
    acquisition: list[KPIMetric]
    activation: list[KPIMetric]
    retention: list[KPIMetric]
    revenue: list[KPIMetric]


class ProductPlanResponse(BaseModel):
    market_research: MarketResearch
    competitors: list[Competitor]
    personas: list[UserPersona]
    prd: PRD
    user_stories: list[UserStory]
    acceptance_criteria: list[AcceptanceCriteria]
    roadmap: Roadmap
    risks: list[ProductRisk]
    kpis: KPIs

    # Agent execution metadata
    research_status: str = "completed"
    research_duration_ms: int = 0
    persona_status: str = "completed"
    persona_duration_ms: int = 0
    prd_status: str = "completed"
    prd_duration_ms: int = 0
    roadmap_status: str = "completed"
    roadmap_duration_ms: int = 0
    risk_status: str = "completed"
    risk_duration_ms: int = 0
    metrics_status: str = "completed"
    metrics_duration_ms: int = 0
    execution_trace: list[str] = []
    source_attributions: list[str] = []



class GenerateResponse(BaseModel):
    """Top-level envelope for POST /generate.

    Wraps the full product plan under a single ``result`` key::

        {"result": {"market_research": {...}, "personas": [...], ...}}
    """

    result: ProductPlanResponse


# --- Modular Agent Outputs ---
class ResearchOutput(BaseModel):
    market_research: MarketResearch
    competitors: list[Competitor]
    status: str = "completed"
    duration_ms: int = 0
    source_attributions: list[str] = []

class PersonaOutput(BaseModel):
    personas: list[UserPersona]
    status: str = "completed"
    duration_ms: int = 0

class PRDOutput(BaseModel):
    prd: PRD
    user_stories: list[UserStory]
    acceptance_criteria: list[AcceptanceCriteria]
    status: str = "completed"
    duration_ms: int = 0

class RoadmapOutput(BaseModel):
    roadmap: Roadmap
    status: str = "completed"
    duration_ms: int = 0

class RiskOutput(BaseModel):
    risks: list[ProductRisk]
    status: str = "completed"
    duration_ms: int = 0

class MetricsOutput(BaseModel):
    kpis: KPIs
    status: str = "completed"
    duration_ms: int = 0


