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


class GenerateResponse(BaseModel):
    """Top-level envelope for POST /generate.

    Wraps the full product plan under a single ``result`` key::

        {"result": {"market_research": {...}, "personas": [...], ...}}
    """

    result: ProductPlanResponse
