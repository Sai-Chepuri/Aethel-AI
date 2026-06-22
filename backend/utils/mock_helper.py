import re

def get_mock_context(idea: str):
    clean = re.sub(r"['\"]", "", idea).strip()

    # 1. Derive product name dynamically
    name_match = (
        re.search(r"called\s+([A-Za-z0-9 _-]+)", clean, re.I)
        or re.search(r"named?\s+([A-Za-z0-9 _-]+)", clean, re.I)
        or re.search(r"^([A-Za-z0-9 _-]{3,25})", clean)
    )
    if name_match:
        product_name = name_match.group(1).strip().title()
    else:
        words = clean.split()
        product_name = " ".join(w.capitalize() for w in words[:3])
        if not product_name.endswith("App") and not product_name.endswith("Platform") and not product_name.endswith("System"):
            product_name += " Tech"

    # 2. Category selection
    lower = clean.lower()

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

    # 3. Category Database
    MOCK_DB = {
        "ai": {
            "cat": "AI-Powered Automation System",
            "audience": "Developers, Product Teams & Enterprise Operations",
            "problem": "time-consuming manual analysis, high operational friction, and slow task execution pipelines",
            "trends": [
                "Agentic Workflows: Shifting from static chatbots to autonomous, goal-oriented agent networks.",
                "LLM Security & Guardrails: Tightening data-privacy requirements for LLM prompt injections.",
                "Custom Grounding: High enterprise demand for localized context injection over raw base models."
            ],
            "tam": "$28.5 B", "sam": "$7.4 B", "som": "$190 M",
            "sizing_rationale": "Sized using B2B developer tool license rates and early target GTM adoption within Fortune 500 product orgs.",
            "strengths": ["Autonomous context parsing", "Low API latency wrappers", "No-code workflow design"],
            "weaknesses": ["Model bias fallbacks required", "Dependency on upstream LLM API limits"],
            "opportunities": ["Custom enterprise local deployments", "Expanding integrations to Slack and Jira"],
            "threats": ["Rapid imitation by massive LLM providers", "Downward pricing pressure on inference costs"],
            "competitors": [
                {"name": "OpenAI Enterprise", "strengths": ["Massive model capabilities", "Strong brand trust"], "weaknesses": ["High subscription cost", "Generic templates"], "differentiation": "10x cheaper customized workflows with domain caching"},
                {"name": "Anthropic Claude API", "strengths": ["Large context window", "Advanced reasoning"], "weaknesses": ["High prompt latency", "No workflow visualizer"], "differentiation": "Visual pipeline editor with zero-code debugging"},
                {"name": "Copy.ai / Jasper", "strengths": ["Established GTM templates", "Aggressive marketing"], "weaknesses": ["Shallow data security", "Poor workflow logic"], "differentiation": "SOC-2 compliant workflow memory and custom grounding tools"}
            ],
            "personas": [
                {
                    "name": "Sarah Jenkins", "role": "Lead Software Engineer", "age": "29",
                    "goals": ["Automate code compliance audits", "Reduce review backlogs by 40%", "Accelerate PR approval speeds"],
                    "pain_points": ["Reviewing boilerplate logs manually", "Inconsistent linting across teams", "High license costs for custom tooling"],
                    "user_scenario": "Sarah is preparing a hotfix release. She triggers the code reviewer tool from her CLI. It highlights security flaws in 4 seconds and suggests inline patches, letting her merge the fix safely before the release window closes."
                },
                {
                    "name": "Marcus Chen", "role": "VP of Engineering & Security", "age": "42",
                    "goals": ["Secure proprietary IP", "Reduce infrastructure spend by 20%", "Enforce global auditing benchmarks"],
                    "pain_points": ["High API bill overruns", "Upstream model down-times", "Lack of granular RBAC"],
                    "user_scenario": "Marcus conducts a quarterly audit. He reviews the tool's compliance logs, exports them to a secure PDF for the board, and enforces access control keys so that only validated developers can write inline fixes."
                }
            ],
            "purpose_scope": "Define MVP specs for an AI-powered agentic review and code generation environment to eliminate software iteration bottlenecks.",
            "goals_success_criteria": [
                {"objective": "Rapid response", "measurable_target": "Inline context audits in < 5 seconds"},
                {"objective": "Accuracy", "measurable_target": "Zero-configuration true positives rate > 92%"},
                {"objective": "Compliance", "measurable_target": "Full compliance with SOC-2 guidelines"}
            ],
            "functional_requirements": [
                "CLI prompt and visual console input interfaces.",
                "Custom JSON configuration maps for project-level guardrails.",
                "One-click patch implementation applying edits directly."
            ],
            "non_functional_requirements": [
                "API keys stored in secure hardware security modules (HSMs).",
                "Fallback parsing logic triggers dynamically if LLMs output raw markdown."
            ],
            "user_stories": [
                {"story_id": "US-01", "user_role": "Developer", "action": "trigger codebase scans", "benefit": "I receive clean, validated code recommendations in seconds"},
                {"story_id": "US-02", "user_role": "Manager", "action": "audit audit logs", "benefit": "I can certify model security and prevent credentials leakage"}
            ],
            "acceptance_criteria": [
                {"story_id": "US-01", "scenarios": ["Given a valid prompt, When the trigger is pulled, Then a validated JSON recommendation block is returned."]},
                {"story_id": "US-02", "scenarios": ["Given an admin session, When auditing compliance, Then system lists all outbound prompts with masked secrets."]}
            ],
            "roadmap": [
                {"phase_name": "Phase 1: MVP Core", "focus": "Fast API integration, basic visual reviewer, and secure configuration storage.", "milestones": ["FastAPI core engine setup", "Semantic file scanner", "Copy & Export hooks"], "timeline": "Weeks 1-4"},
                {"phase_name": "Phase 2: Integrations", "focus": "GitHub Actions and VS Code extensions for developer workflow cohesion.", "milestones": ["CI/CD action integration", "Visual Studio Code plugin", "OAuth2 auth integration"], "timeline": "Months 2-3"},
                {"phase_name": "Phase 3: Custom Models", "focus": "Deploying self-hosted private models and custom training fine-tunes.", "milestones": ["Fine-tuned local weights", "Docker local hosting script", "Jira automation hooks"], "timeline": "Months 4-6"}
            ],
            "mermaid_gantt": "gantt\n    title AI Tool release\n    dateFormat YYYY-MM-DD\n    section MVP Core\n    Core Setup :2026-07-01, 10d\n    UI Reviewer :after a1, 15d\n    section Integrations\n    CI/CD Hooks :2026-07-26, 20d",
            "risks": [
                {"description": "Upstream API outages", "category": "Technical", "impact": "High", "probability": "Medium", "mitigation": "Configure local smaller fallback models to parse basic inputs offline."},
                {"description": "Rapid API price dropping", "category": "Market", "impact": "Medium", "probability": "High", "mitigation": "Structure billing on workflow utility values instead of direct token markups."}
            ],
            "kpis": {
                "acquisition": [
                    {"metric": "Sign-up conversion", "target": "> 15%", "notes": "From landing page tool specs"},
                    {"metric": "Customer Acquisition Cost (CAC)", "target": "< $20", "notes": "Target developer acquisition cost"}
                ],
                "activation": [
                    {"metric": "First execution", "target": "< 60s", "notes": "Time from registration to first scan"},
                    {"metric": "Integration completion", "target": "> 75%", "notes": "Linking IDE/CI/CD tool"}
                ],
                "retention": [
                    {"metric": "Weekly active rate (WAU)", "target": "> 40%", "notes": "Weekly active developers returning"},
                    {"metric": "Monthly retention (M1)", "target": "> 60%", "notes": "Developers retaining after month 1"}
                ],
                "revenue": [
                    {"metric": "ARPU Pro", "target": "$39/mo", "notes": "Basic developer subscription pricing"},
                    {"metric": "Enterprise contract value", "target": "> $12k/yr", "notes": "For custom grounded servers"}
                ]
            }
        },
        "pet": {
            "cat": "Smart PetTech Platform",
            "audience": "Pet Owners, Dog Trainers & Veterinarians",
            "problem": "difficulty tracking pet health metrics, identifying sudden hydration/pain anomalies, and sharing health records with vets",
            "trends": [
                "Humanization of Pets: Pet owners demand the same standard of medical data for animals as humans.",
                "IoT Wearables for Animals: Micro-sensors embedded in collars tracking heart rate, activity, and sleep.",
                "Telehealth Integration: Rapid diagnostic sharing from smart collar to telehealth veterinary portals."
            ],
            "tam": "$9.5 B", "sam": "$1.8 B", "som": "$65 M",
            "sizing_rationale": "Based on global smart collar sales and premium pet subscription attach rates in urban demographics.",
            "strengths": ["Dual GPS and LTE cellular trackers", "Waterproof and rugged design", "Vet-endorsed baseline algorithms"],
            "weaknesses": ["High hardware manufacturing costs", "Heavy battery consumption with GPS enabled"],
            "opportunities": ["Direct partnerships with pet insurance networks", "Expanding tracker collar designs to cats"],
            "threats": ["Low battery life frustration", "Established smart tag competitors"],
            "competitors": [
                {"name": "Whistle Smart Collar", "strengths": ["Established brand", "Rich sleep metrics"], "weaknesses": ["Slow GPS refresh", "Bulky collar attachment"], "differentiation": "Ultra-lightweight design tailored specifically for cats and small dogs"},
                {"name": "Fi Smart Collar", "strengths": ["Exceptional battery life", "Sleek metal build"], "weaknesses": ["Limited health tracking", "Expensive subscription"], "differentiation": "Focuses on advanced hydration alerts and direct vet data sharing"},
                {"name": "FitBark Activity Monitor", "strengths": ["Low upfront price", "WiFi sync"], "weaknesses": ["No cellular GPS tracker", "Plastic build quality"], "differentiation": "Rugged armor shell with multi-carrier LTE failover tracking"}
            ],
            "personas": [
                {
                    "name": "Bella Davidson", "role": "Dedicated Cat/Dog Owner", "age": "31",
                    "goals": ["Ensure pet safety while at work", "Track pet hydration level", "Share health trends during checkups"],
                    "pain_points": ["Fear of pet escaping", "Not knowing when pet is in pain", "Heavy veterinary bills"],
                    "user_scenario": "Bella leaves her Golden Retriever at home. She gets a phone alert showing low hydration. She calls her pet-sitter immediately to refill the water bowl, preventing dehydration issues."
                },
                {
                    "name": "Dr. Dave Miller", "role": "Veterinary Practitioner", "age": "45",
                    "goals": ["Get clinical-grade health logs", "Identify pain indicators early", "Reduce diagnostic discovery times"],
                    "pain_points": ["Owners misremembering pet behaviors", "Incomplete diagnostic context", "Short checkup windows"],
                    "user_scenario": "Dave reviews a pet's dashboard before a checkup. The collar metrics show a sudden drop in joint activity. He diagnoses early arthritis immediately, saving time and diagnostic costs."
                }
            ],
            "purpose_scope": "Define MVP for a smart collar system tracking activity, location, and hydration metrics, transmitting findings to a pet health dashboard.",
            "goals_success_criteria": [
                {"objective": "Safety tracking", "measurable_target": "GPS tracking accurate to < 5 meters"},
                {"objective": "Battery efficiency", "measurable_target": "Over 30 days of battery life per charge"},
                {"objective": "Health insights", "measurable_target": "Hydration drop alerts triggered within 15 mins"}
            ],
            "functional_requirements": [
                "Bluetooth syncing and cellular LTE communication modules.",
                "Interactive maps showing real-time pet location boundaries.",
                "One-click health PDF report export for vet consults."
            ],
            "non_functional_requirements": [
                "Waterproofing standard of IP68.",
                "Secure data transmission with AES-256 encryption."
            ],
            "user_stories": [
                {"story_id": "US-01", "user_role": "Pet Owner", "action": "set virtual geofence boundaries", "benefit": "I get instant mobile alerts if my pet escapes the yard"},
                {"story_id": "US-02", "user_role": "Vet", "action": "access weekly sleep & activity charts", "benefit": "I can identify abnormal behaviors before clinical symptoms develop"}
            ],
            "acceptance_criteria": [
                {"story_id": "US-01", "scenarios": ["Given an active geofence, When the collar crosses the boundary, Then a push notification is sent in under 10 seconds."]},
                {"story_id": "US-02", "scenarios": ["Given an authorized vet view, When loading the history, Then show a chart of daily sleep hours."]}
            ],
            "roadmap": [
                {"phase_name": "Phase 1: MVP Tracker", "focus": "Basic Bluetooth sync, step counter, geo-fencing, and manual veterinarian reports.", "milestones": ["Hardware prototype validation", "iOS Bluetooth sync app", "Geofence alert triggers"], "timeline": "Weeks 1-4"},
                {"phase_name": "Phase 2: Hydration & Cellular", "focus": "Cellular LTE integration, automatic hydration sensors, and push notifications.", "milestones": ["LTE cellular firmware update", "Hydration monitoring algorithms", "Push alert engines"], "timeline": "Months 2-3"},
                {"phase_name": "Phase 3: Vet API", "focus": "Veterinary management software integrations and pet insurance partnerships.", "milestones": ["Vet portal API endpoint", "Insurance discounts calculation", "Anomalous health models"], "timeline": "Months 4-6"}
            ],
            "mermaid_gantt": "gantt\n    title Smart Collar release\n    dateFormat YYYY-MM-DD\n    section MVP Core\n    App Bluetooth Sync :2026-07-01, 12d\n    Geofence Alerts    :after a1, 10d",
            "risks": [
                {"description": "GPS battery drain", "category": "Technical", "impact": "High", "probability": "High", "mitigation": "Configure GPS to pulse only when pet exits pre-configured home WiFi ranges."},
                {"description": "High cellular costs", "category": "Project", "impact": "Medium", "probability": "Medium", "mitigation": "Negotiate global multi-carrier IoT roaming agreements to fix LTE rates."}
            ],
            "kpis": {
                "acquisition": [
                    {"metric": "Hardware sales conversion", "target": "> 8%", "notes": "Pet community ads"},
                    {"metric": "Social referral index", "target": "> 1.5x", "notes": "Shares within pet groups"}
                ],
                "activation": [
                    {"metric": "Collar registration", "target": "> 95%", "notes": "Unboxing app connection"},
                    {"metric": "First week sync rate", "target": "> 90%", "notes": "Initial week metrics synced"}
                ],
                "retention": [
                    {"metric": "Weekly sync rate", "target": "> 80%", "notes": "Active collars returning metrics"},
                    {"metric": "Monthly subscriber retention", "target": "> 95%", "notes": "GPS tracking subscription renewals"}
                ],
                "revenue": [
                    {"metric": "Subscription attach", "target": "> 70%", "notes": "GPS tracking sub attach rate"},
                    {"metric": "Average order value (LTV)", "target": "> $180", "notes": "Combined hardware + subscription"}
                ]
            }
        },
        "food": {
            "cat": "Sustainable FoodTech Platform",
            "audience": "Eco-Conscious Consumers, Families & Local Home Cooks",
            "problem": "single-use packaging waste, high food delivery fees, and lack of transparency in local ingredient sourcing",
            "trends": [
                "Zero-Waste Packaging: Consumers demand insulated, reusable containers over plastic boxes.",
                "Hyperlocal Cook Marketplaces: Shift from massive ghost kitchens to local community home-cooks.",
                "Circular Economy: Delivery networks that collect empty packaging on their next route."
            ],
            "tam": "$18.2 B", "sam": "$3.5 B", "som": "$120 M",
            "sizing_rationale": "Sized via organic meal market shares and container subscription yields in metropolitan pilot cities.",
            "strengths": ["Insulated zero-waste container fleet", "Low-emissions delivery routes", "Transparent cook auditing"],
            "weaknesses": ["High packaging collection logistics", "Cook onboarding and health audits overhead"],
            "opportunities": ["Corporate lunch partnerships", "Partnerships with organic grocery suppliers"],
            "threats": ["Intense competition from food giants", "Health regulation compliance complexity"],
            "competitors": [
                {"name": "Uber Eats", "strengths": ["Massive driver network", "Huge merchant list"], "weaknesses": ["Massive plastic waste", "High service fees"], "differentiation": "Zero service fees, zero plastic waste, focused on home-cooked meals"},
                {"name": "HelloFresh", "strengths": ["Predictable meal kits", "Bulk sourcing pricing"], "weaknesses": ["Required cooking effort", "Excess shipping boxes"], "differentiation": "Fully cooked meals delivered in local reusable containers"},
                {"name": "DoorDash", "strengths": ["Aggressive merchant partnerships", "DashPass loyalty"], "weaknesses": ["Single-use container waste", "High merchant commissions"], "differentiation": "Circular model returning clean containers for credits"}
            ],
            "personas": [
                {
                    "name": "Hannah Abbott", "role": "Busy Working Parent", "age": "34",
                    "goals": ["Feed family healthy meals", "Reduce household plastic waste", "Order food under 30 minutes"],
                    "pain_points": ["Guilt from plastic packaging waste", "Fast-food options are unhealthy", "Cooking takes too much time"],
                    "user_scenario": "Hannah orders dinner. It arrives in custom heated lunchboxes. The family eats, packs the containers back into the delivery bag, and places it on the porch for morning pickup."
                },
                {
                    "name": "Chef Leo Rossi", "role": "Artisan Home Cook", "age": "48",
                    "goals": ["Monetize culinary skills", "Access eco-friendly customers", "Get predictable orders"],
                    "pain_points": ["Commercial kitchen rents are high", "Marketing costs are prohibitive", "Single-use packing supplies cost"],
                    "user_scenario": "Leo receives dinner orders. The platform supplies sanitized reusable containers. He packs his organic lasagna, prints delivery slips, and hands them to the zero-waste courier."
                }
            ],
            "purpose_scope": "Define MVP specs for a food delivery marketplace connecting local cooks with users using reusable, collectable packaging.",
            "goals_success_criteria": [
                {"objective": "Waste reduction", "measurable_target": "Zero plastic waste packaging (99% reusable)"},
                {"objective": "Delivery speed", "measurable_target": "Average order arrival time < 40 minutes"},
                {"objective": "Retention", "measurable_target": "Container return rate > 95% within 7 days"}
            ],
            "functional_requirements": [
                "Cook catalog with dietary and allergen filters.",
                "Packaging pickup scheduling module inside cart flow.",
                "Circular logistics route optimizer for delivery couriers."
            ],
            "non_functional_requirements": [
                "Packaging sanitation matches state FDA food code rules.",
                "App performance degrades gracefully in low-bandwidth cellular environments."
            ],
            "user_stories": [
                {"story_id": "US-01", "user_role": "Customer", "action": "filter dishes by zero-waste status", "benefit": "I can buy dinner guilt-free without generating waste"},
                {"story_id": "US-02", "user_role": "Delivery Partner", "action": "scan container barcodes", "benefit": "I can register container handoffs and update logistics in real-time"}
            ],
            "acceptance_criteria": [
                {"story_id": "US-01", "scenarios": ["Given a food selection, When checkout is complete, Then schedule a return container pickup."]},
                {"story_id": "US-02", "scenarios": ["Given a courier checkout, When they scan the container code, Then the return ledger updates."]}
            ],
            "roadmap": [
                {"phase_name": "Phase 1: Local Pilots", "focus": "Core cook listings, insulated packaging logistics, and basic courier app.", "milestones": ["Sanitized container design", "Cook portal launch", "Local delivery courier routing"], "timeline": "Weeks 1-4"},
                {"phase_name": "Phase 2: Subscriptions", "focus": "Lunch subscriptions, zero-waste return credits, and automatic geolocator pickups.", "milestones": ["Zero-waste credit system", "Weekly dinner subscriptions", "Automated courier routing"], "timeline": "Months 2-3"},
                {"phase_name": "Phase 3: Scale Operations", "focus": "Expanding to corporate campus wellness plans and organic supply chain feeds.", "milestones": ["Corporate catering platform", "Organic ingredients supplier hub", "Logistics machine learning model"], "timeline": "Months 4-6"}
            ],
            "mermaid_gantt": "gantt\n    title FoodTech release\n    dateFormat YYYY-MM-DD\n    section MVP Core\n    Container Sanitation :2026-07-01, 10d\n    Cook App listings   :after a1, 15d",
            "risks": [
                {"description": "Lost container overhead", "category": "Project", "impact": "High", "probability": "Medium", "mitigation": "Hold a refundable card deposit that charges if containers are not returned in 14 days."},
                {"description": "FDA compliance audits", "category": "Legal", "impact": "High", "probability": "Low", "mitigation": "Build centralized industrial wash facilities with logged temperature compliance."}
            ],
            "kpis": {
                "acquisition": [
                    {"metric": "Customer acquisition cost", "target": "< $12", "notes": "Social referral loop"},
                    {"metric": "App click-through rate", "target": "> 5%", "notes": "Eco-friendly marketing hooks"}
                ],
                "activation": [
                    {"metric": "First delivery order", "target": "> 75%", "notes": "Conversion of app installs"},
                    {"metric": "Account link completion", "target": "> 90%", "notes": "Customer profile registration"}
                ],
                "retention": [
                    {"metric": "Repeat order rate", "target": "> 55%", "notes": "Monthly active diners"},
                    {"metric": "M1 user retention", "target": "> 40%", "notes": "Monthly recurring diners returning"}
                ],
                "revenue": [
                    {"metric": "Subscription attach", "target": "> 30%", "notes": "Zero-waste pass monthly attach"},
                    {"metric": "Average order size", "target": "> $28", "notes": "Urban order value basket size"}
                ]
            }
        },
        "finance": {
            "cat": "Automated Fintech Application",
            "audience": "Gen Z Savers, Retail Investors & Students",
            "problem": "complex investment barriers, hidden banking transaction fees, and poor financial literacy tools",
            "trends": [
                "Micro-Budgeting & Investing: Users demand round-up savings models over manual bank transfers.",
                "AI Financial Coaches: Machine learning categorizing expenses and providing personalized wealth tips.",
                "Open Banking APIs: Rapid, secure account links via Plaid, bypassing card network overhead."
            ],
            "tam": "$14.5 B", "sam": "$2.8 B", "som": "$90 M",
            "sizing_rationale": "Calculated from open banking adapter usage and retail investor registration volumes in target markets.",
            "strengths": ["Automated Plaid bank account links", "AI spending categorisation", "Zero-commission fractional stocks"],
            "weaknesses": ["Low initial deposit asset sizes", "High dependency on external brokerage API rails"],
            "opportunities": ["High-yield savings account products", "Automated subscription auditing features"],
            "threats": ["Traditional banks duplicating features", "Stricter SEC cryptocurrency regulations"],
            "competitors": [
                {"name": "Robinhood", "strengths": ["Huge options list", "Sleek user experience"], "weaknesses": ["No budgeting tool", "Gamification scrutiny"], "differentiation": "Roundups focused strictly on passive budgeting and saving goals"},
                {"name": "Mint / Copilot", "strengths": ["Detailed budgeting", "Clean interfaces"], "weaknesses": ["No investment execution", "Mint shutdown disruption"], "differentiation": "Combines budgeting insights directly with automated fractional purchases"},
                {"name": "Acorns", "strengths": ["Established roundup model", "Retirement portfolios"], "weaknesses": ["High monthly subscription", "No manual stock picks"], "differentiation": "Offers hybrid manual-passive investing with zero fees for students"}
            ],
            "personas": [
                {
                    "name": "Zoe Miller", "role": "Recent College Graduate", "age": "23",
                    "goals": ["Build an emergency savings fund", "Start investing with $10/week", "Track monthly streaming subs"],
                    "pain_points": ["Living paycheck-to-paycheck", "Investing jargon is confusing", "Manual bank transfers are forgotten"],
                    "user_scenario": "Zoe buys a coffee for $3.50. The app rounds the purchase to $4.00, automatically placing $0.50 into her S&P 500 fractional portfolio, growing her assets passively."
                },
                {
                    "name": "Arthur Pendelton", "role": "Budget Coordinator", "age": "36",
                    "goals": ["Reduce subscription bloat", "Keep household expenses transparent", "Optimize family budget pools"],
                    "pain_points": ["Hidden monthly subscription renewals", "Manual spreadsheets take too long", "Fragmented joint accounts"],
                    "user_scenario": "Arthur receives a notifications warning of a streaming price hike next week. He hits 'Cancel Sub' in the app. The tool automates the cancellation request instantly."
                }
            ],
            "purpose_scope": "Define MVP specs for a micro-saving platform rounding transactions and placing savings into passive fractional ETFs.",
            "goals_success_criteria": [
                {"objective": "Passive savings", "measurable_target": "Average passive savings of > $40/month per user"},
                {"objective": "Linking friction", "measurable_target": "Plaid bank links completed in < 45 seconds"},
                {"objective": "Engagement", "measurable_target": "Weekly app open rate > 60%"}
            ],
            "functional_requirements": [
                "Plaid account sync and transactional roundup engine.",
                "Fractional investment broker ledger integrations.",
                "AI subscription auditor detecting recurrent bill patterns."
            ],
            "non_functional_requirements": [
                "Compliance with PCI-DSS Level 1 security standards.",
                "Double-entry bookkeeping for transaction log ledgers."
            ],
            "user_stories": [
                {"story_id": "US-01", "user_role": "Saver", "action": "link my checking card via Plaid", "benefit": "my transaction cents are automatically rounded up to investments"},
                {"story_id": "US-02", "user_role": "Saver", "action": "set spending thresholds", "benefit": "I receive warnings before subscriptions renew and overdraw my balance"}
            ],
            "acceptance_criteria": [
                {"story_id": "US-01", "scenarios": ["Given a card link, When transactions are posted, Then calculate roundup and transfer to brokerage."]},
                {"story_id": "US-02", "scenarios": ["Given an active sub, When renew date is within 3 days, Then trigger push alert warning."]}
            ],
            "roadmap": [
                {"phase_name": "Phase 1: Plaid Roundup", "focus": "Plaid transactional adapters, automatic roundup engine, and fractional broker links.", "milestones": ["Plaid API setup", "Roundup calculation module", "Brokerage API partnership"], "timeline": "Weeks 1-4"},
                {"phase_name": "Phase 2: Budget AI", "focus": "Spending categorization models, subscription alerts, and recurring savings plans.", "milestones": ["AI spending classifier", "Subscription cancel flows", "Recurring budget vault"], "timeline": "Months 2-3"},
                {"phase_name": "Phase 3: High-Yield Vaults", "focus": "Joint accounts, high-yield savings vaults, and automated custom portfolio buckets.", "milestones": ["High-yield savings vault", "Joint account permissions", "Asset rebalancing engine"], "timeline": "Months 4-6"}
            ],
            "mermaid_gantt": "gantt\n    title Fintech release\n    dateFormat YYYY-MM-DD\n    section MVP Core\n    Plaid Link Setup    :2026-07-01, 10d\n    Roundup calculation :after a1, 15d",
            "risks": [
                {"description": "Regulatory SEC compliance", "category": "Legal", "impact": "High", "probability": "Medium", "mitigation": "Partner with registered FINRA broker-dealers for custody and transaction execution."},
                {"description": "Low customer asset sizes", "category": "Project", "impact": "Medium", "probability": "High", "mitigation": "Offer high-yield vaults and direct payroll deposit options to increase wallet share."}
            ],
            "kpis": {
                "acquisition": [
                    {"metric": "App store conversion", "target": "> 10%", "notes": "Finance category landing"},
                    {"metric": "Customer Acquisition Cost (CAC)", "target": "< $15", "notes": "Paid advertising campaigns"}
                ],
                "activation": [
                    {"metric": "Plaid link success", "target": "> 85%", "notes": "Registered users linking cards"},
                    {"metric": "First Roundup deposit", "target": "> 75%", "notes": "Completed initial spare change transaction"}
                ],
                "retention": [
                    {"metric": "M1 active rate", "target": "> 45%", "notes": "Active card transaction roundups"},
                    {"metric": "Churn rate", "target": "< 5%", "notes": "Percentage of unlinked cards monthly"}
                ],
                "revenue": [
                    {"metric": "Fee-free sub attach", "target": "$2.99/mo", "notes": "Premium features charge subscription"},
                    {"metric": "Broker fee rebates", "target": "Avg $0.20/trade", "notes": "Rebate shares from fractional transaction routes"}
                ]
            }
        },
        "health": {
            "cat": "Human Health & Wellness Platform",
            "audience": "Stress-Conscious Individuals, Yoga Instructors & Executives",
            "problem": "high daily stress, fragmented health trackers, and poor sleep optimization tools",
            "trends": [
                "Mindfulness & Sleep: Consumers demand sleep quality trackers integrating with wearable bio-data.",
                "Corporate Health Plans: Companies subsidizing mindfulness platforms for employee wellness.",
                "AI Guided Meditation: Audio content adapting dynamically to the user's stress level."
            ],
            "tam": "$16.5 B", "sam": "$4.1 B", "som": "$110 M",
            "sizing_rationale": "Derived from global meditation platform market growth rates and wearable integration attach volumes.",
            "strengths": ["Apple Health and Google Fit bio-data sync", "Bio-feedback customized audio generation", "Clinical-grade stress tracking"],
            "weaknesses": ["Higher user churn rates after initial use", "Wearable API sensor access dependency"],
            "opportunities": ["Direct integrations with corporate HR software", "Wearable sleep quality correlation tools"],
            "threats": ["Large mental wellness app incumbents", "Inaccurate smart watch readings causing user distrust"],
            "competitors": [
                {"name": "Headspace", "strengths": ["Strong visual branding", "Rich animation library"], "weaknesses": ["Static content packages", "Generic audio voices"], "differentiation": "Mindfulness sessions adjust dynamically based on real-time wearable heart-rate logs"},
                {"name": "Calm", "strengths": ["Celebrity sleep stories", "Aggressive B2B partnerships"], "weaknesses": ["Expensive tiers", "Limited bio-metrics integration"], "differentiation": "Direct correlation analysis between sleep trends and daytime stress metrics"},
                {"name": "Whoop / Apple Health", "strengths": ["Exceptional hardware sensors", "Deep bio-metric logs"], "weaknesses": ["No guided mindfulness sessions", "Raw data overload"], "differentiation": "Combines raw bio-data directly with actionable guided meditation sessions"}
            ],
            "personas": [
                {
                    "name": "Olivia Vance", "role": "Corporate Executive", "age": "38",
                    "goals": ["Reduce anxiety during workdays", "Improve deep sleep time", "Track heart-rate variability (HRV) trends"],
                    "pain_points": ["Chronic stress causing fatigue", "Lack of time for long sessions", "Overwhelmed by health data charts"],
                    "user_scenario": "Olivia enters a high-pressure boardroom. The app detects a spike in her Apple Watch HRV. It triggers a silent prompt suggesting a 2-minute breathing session, calming her instantly."
                },
                {
                    "name": "Ethan Hughes", "role": "Meditation & Yoga Coach", "age": "29",
                    "goals": ["Create customized patient scripts", "Monitor patient stress recovery", "Expand online coaching brand"],
                    "pain_points": ["Static recording tools are boring", "No quantitative client progress metrics", "Client churn is high"],
                    "user_scenario": "Ethan reviews his client's recovery dashboard. He observes high stress levels on Tuesday nights and updates her meditation prescription, increasing retention by 20%."
                }
            ],
            "purpose_scope": "Define MVP specs for a mindfulness app analyzing wearable bio-metrics and delivering adaptive sleep and stress guided audio.",
            "goals_success_criteria": [
                {"objective": "Anxiety reduction", "measurable_target": "Reported anxiety levels drop by > 25% in 3 weeks"},
                {"objective": "Wearable sync", "measurable_target": "Wearable data sync rate > 98%"},
                {"objective": "Sleep quality", "measurable_target": "Avg. deep sleep duration improves by 20 mins"}
            ],
            "functional_requirements": [
                "Wearable API integrations (HealthKit, Fit API).",
                "Adaptive audio player with pitch and speed modulation.",
                "Custom stress/recovery dashboard tracker."
            ],
            "non_functional_requirements": [
                "HIPAA data privacy compliance rules enforced.",
                "Audio streaming bandwidth consumption optimized."
            ],
            "user_stories": [
                {"story_id": "US-01", "user_role": "User", "action": "sync my wearable metrics", "benefit": "I receive guided meditation audio adapted to my daily stress recovery score"},
                {"story_id": "US-02", "user_role": "Coach", "action": "assign audio tracks to client profiles", "benefit": "I can track client recovery rates and modify prescriptions"}
            ],
            "acceptance_criteria": [
                {"story_id": "US-01", "scenarios": ["Given an active watch sync, When heart rate spikes, Then trigger a notification suggesting a breathing track."]},
                {"story_id": "US-02", "scenarios": ["Given a trainer view, When looking at metrics, Then highlight high-stress days."]}
            ],
            "roadmap": [
                {"phase_name": "Phase 1: Audio Core", "focus": "Mindfulness audio catalog, manual stress logging, and basic custom playlists.", "milestones": ["Audio streaming engine setup", "Manual stress checkins", "Playlists custom selector"], "timeline": "Weeks 1-4"},
                {"phase_name": "Phase 2: Wearable SDK", "focus": "Apple HealthKit and Google Fit integrations, and automated bio-feedback triggers.", "milestones": ["HealthKit SDK integration", "Stress detection model", "Adaptive audio player update"], "timeline": "Months 2-3"},
                {"phase_name": "Phase 3: AI Audio Gen", "focus": "Generative voice synthesis, B2B corporate health dashboards, and recovery projections.", "milestones": ["Generative audio synthesizer", "Corporate dashboard portal", "Stress prediction algorithm"], "timeline": "Months 4-6"}
            ],
            "mermaid_gantt": "gantt\n    title HealthApp release\n    dateFormat YYYY-MM-DD\n    section MVP Core\n    Audio Player Core  :2026-07-01, 10d\n    Manual logs engine :after a1, 15d",
            "risks": [
                {"description": "Bio-data privacy compliance", "category": "Legal", "impact": "High", "probability": "High", "mitigation": "Anonymize all bio-metric logs on client side before cloud database storage."},
                {"description": "High user churn", "category": "Project", "impact": "Medium", "probability": "High", "mitigation": "Implement daily streaks and micro-habit triggers to build retention."}
            ],
            "kpis": {
                "acquisition": [
                    {"metric": "Install rate", "target": "> 12%", "notes": "Social referral loops"},
                    {"metric": "Customer cost (CAC)", "target": "< $10", "notes": "Content marketing focused"}
                ],
                "activation": [
                    {"metric": "Bio sync completion", "target": "> 70%", "notes": "Users linking wearable bio-data"},
                    {"metric": "First session completion", "target": "> 85%", "notes": "Completes first meditation audio track"}
                ],
                "retention": [
                    {"metric": "WAU active rate", "target": "> 35%", "notes": "Active users returning daily"},
                    {"metric": "Month-1 Retention (M1)", "target": "> 30%", "notes": "Retained users in week 5"}
                ],
                "revenue": [
                    {"metric": "Pro tier attach", "target": "$12.99/mo", "notes": "Guided session catalog access fee"},
                    {"metric": "Enterprise LTV", "target": "> $1.2k/account", "notes": "Average annual value for corporate employee plans"}
                ]
            }
        },
        "education": {
            "cat": "Interactive EdTech Platform",
            "audience": "Students, Lifelong Learners & Language Instructors",
            "problem": "rigid curriculum structures, lack of interactive speech feedback, and expensive learning options",
            "trends": [
                "Gamification of Learning: Users demand gamified rewards and micro-learning quests.",
                "AI Speech Assessment: Voice model grading pronunciation in real-time.",
                "Bite-sized mobile micro-learning: 5-minute interactive lessons replacing long course videos."
            ],
            "tam": "$22.5 B", "sam": "$5.4 B", "som": "$140 M",
            "sizing_rationale": "Sized via global language and micro-learning app market volumes in target consumer demographics.",
            "strengths": ["AI-driven speech analysis engine", "Bite-sized interactive micro-quests", "Gamified rewards system"],
            "weaknesses": ["Content localization costs", "High user churn in self-paced learning models"],
            "opportunities": ["Corporate language-training accounts", "Direct integration with school curriculum portals"],
            "threats": ["Highly established gamified incumbents", "Free video learning channels cannibalizing users"],
            "competitors": [
                {"name": "Duolingo", "strengths": ["Excellent gamification", "Strong viral loops"], "weaknesses": ["Repetitive content", "Weak grammar explanations"], "differentiation": "Focuses on deep conversational grammar guides and real-time speech audits"},
                {"name": "Coursera", "strengths": ["Certified university courses", "Professional reputation"], "weaknesses": ["Expensive courses", "Rigid lecture formats"], "differentiation": "Bite-sized micro-quests (5 minutes) that fit into daily commutes"},
                {"name": "Quizlet / Udemy", "strengths": ["Massive crowdsourced flashcard decks", "Cheap course platform"], "weaknesses": ["Inconsistent quality", "No active evaluation technology"], "differentiation": "Uses advanced audio analysis to grade pronunciation and direct speech flow"}
            ],
            "personas": [
                {
                    "name": "Maya Lin", "role": "Language Student", "age": "21",
                    "goals": ["Prepare for overseas internships", "Improve conversation pronunciation", "Maintain daily study streaks"],
                    "pain_points": ["Grammar rules are boring", "No one to practice speaking with", "Long lectures cause burnout"],
                    "user_scenario": "Maya sits on the train. She opens LangQuest, completes a 5-minute dialogue quest, speaks into the mic, gets marked 'Excellent Pronunciation', and maintains her 45-day study streak."
                },
                {
                    "name": "Prof. Karl Keller", "role": "Language Instructor", "age": "52",
                    "goals": ["Assign micro-homework tasks", "Monitor student speaking errors", "Create custom curriculum decks"],
                    "pain_points": ["Grading speech files manually takes hours", "Poor student homework completion rates", "No metrics on pronunciation errors"],
                    "user_scenario": "Karl reviews his class dashboard. He identifies common errors in pronunciation, updates the course deck, and sends a gamified quest to his class in 2 minutes."
                }
            ],
            "purpose_scope": "Define MVP specs for a gamified micro-learning platform analyzing speaking patterns and delivering dialogue quests.",
            "goals_success_criteria": [
                {"objective": "Active retention", "measurable_target": "Daily streak retention rate > 30%"},
                {"objective": "Audio grading", "measurable_target": "Speech grading returned in < 2 seconds"},
                {"objective": "Progress speed", "measurable_target": "Conversational score improves by 15% in 4 weeks"}
            ],
            "functional_requirements": [
                "Bite-sized quest manager and reward logic.",
                "AI speech scoring module with audio capture hooks.",
                "Student performance dashboard with mistake logs."
            ],
            "non_functional_requirements": [
                "Compliance with COPPA children data protection rules.",
                "Audio compression formats fit cellular limits."
            ],
            "user_stories": [
                {"story_id": "US-01", "user_role": "Student", "action": "record conversation answers", "benefit": "I receive automated pronunciation feedback and progress marks"},
                {"story_id": "US-02", "user_role": "Teacher", "action": "assign homework decks", "benefit": "I can monitor mistakes across the class and adjust lessons"}
            ],
            "acceptance_criteria": [
                {"story_id": "US-01", "scenarios": ["Given an audio file, When speech analyzer finishes, Then return a marked score list."]},
                {"story_id": "US-02", "scenarios": ["Given a student dashboard, When mistakes exceed threshold, Then tag lessons for review."]}
            ],
            "roadmap": [
                {"phase_name": "Phase 1: Quest Engine", "focus": "Bite-sized curriculum databases, manual answer scoring, and gamified reward systems.", "milestones": ["Quest database schemas", "Gamified score manager", "Manual grading dashboard"], "timeline": "Weeks 1-4"},
                {"phase_name": "Phase 2: Speech AI", "focus": "Speech grading integration, microphone recording app, and mistake review lists.", "milestones": ["Speech analyzer SDK link", "Mic recording interface", "Incorrect answer vaults"], "timeline": "Months 2-3"},
                {"phase_name": "Phase 3: Class Hub", "focus": "Teacher dashboards, custom content generators, and multiplayer challenges.", "milestones": ["Teacher admin portal", "Dialogue generation tool", "Competitive battle lobby"], "timeline": "Months 4-6"}
            ],
            "mermaid_gantt": "gantt\n    title EdTech release\n    dateFormat YYYY-MM-DD\n    section MVP Core\n    Quest Database Core :2026-07-01, 10d\n    Gamified Rewards    :after a1, 15d",
            "risks": [
                {"description": "Student retention loss", "category": "Project", "impact": "High", "probability": "High", "mitigation": "Integrate daily micro-challenges and competitive streaks with push notifications."},
                {"description": "Content translation scale", "category": "Technical", "impact": "Medium", "probability": "Medium", "mitigation": "Build automated content generator modules powered by calibrated LLM engines."}
            ],
            "kpis": {
                "acquisition": [
                    {"metric": "Daily signups", "target": "> 500/day", "notes": "Social referral loops"},
                    {"metric": "Ad conversion rate", "target": "> 4%", "notes": "Target student marketing"}
                ],
                "activation": [
                    {"metric": "First quest completion", "target": "> 80%", "notes": "App installs starting quest 1"},
                    {"metric": "Streak activation rate", "target": "> 60%", "notes": "Completing three consecutive days"}
                ],
                "retention": [
                    {"metric": "D7 active retention", "target": "> 35%", "notes": "Users return after 7 days"},
                    {"metric": "D30 Active Streak share", "target": "> 15%", "notes": "Percentage maintaining 30-day streak"}
                ],
                "revenue": [
                    {"metric": "Ad-free pass sub", "target": "$9.99/mo", "notes": "Gamified infinite hearts pass"},
                    {"metric": "Classroom license sales", "target": "> $400/yr", "notes": "School classroom subscription tier"}
                ]
            }
        },
        "ecommerce": {
            "cat": "Hyperlocal Vendor E-commerce Platform",
            "audience": "Artisanal Merchants, Local Sellers & Convenience Shoppers",
            "problem": "high transactional commissions, lack of logistics tracking for local orders, and complex shop setup tools",
            "trends": [
                "D2C Local Sourcing: High consumer demand for direct delivery from neighborhood artisans.",
                "Instant Delivery Logistics: Same-day shipping using decentralized courier networks.",
                "No-Code Vendor Onboarding: Simple shop setup flows optimized for mobile screens."
            ],
            "tam": "$35.2 B", "sam": "$8.5 B", "som": "$250 M",
            "sizing_rationale": "Sized via regional logistics transaction fees and artisan platform signup statistics.",
            "strengths": ["Mobile-first vendor catalog setup", "Hyperlocal courier matching algorithms", "Granular real-time shipment map tracking"],
            "weaknesses": ["Logistics network bootstrap challenges", "Higher per-delivery costs for rural locations"],
            "opportunities": ["Corporate gifting catalog integrations", "Regional distribution node centers"],
            "threats": ["Massive ecommerce giants duplicating features", "Driver/Courier network labor shortages"],
            "competitors": [
                {"name": "Shopify", "strengths": ["Rich developer app ecosystem", "Massive global scale"], "weaknesses": ["Complex setups", "No built-in courier network"], "differentiation": "Features mobile-first instant store setups and built-in local delivery couriers"},
                {"name": "Etsy", "strengths": ["Large artisan customer base", "Established brand name"], "weaknesses": ["High merchant fees", "No local delivery tracking"], "differentiation": "Focuses strictly on hyperlocal next-day delivery using tracked courier loops"},
                {"name": "Amazon Seller Central", "strengths": ["Exceptional warehousing network", "Prime delivery speed"], "weaknesses": ["Extremely high commissions", "Impersonal listing designs"], "differentiation": "Direct developer storefronts with zero commissions and localized vendor branding"}
            ],
            "personas": [
                {
                    "name": "Clara Higgins", "role": "Local Artisan Shop Owner", "age": "28",
                    "goals": ["Build a digital storefront under 5 mins", "Access neighborhood customers", "Track local delivery couriers"],
                    "pain_points": ["High transactional fee markups", "Complicated design tool setups", "No tracking for local couriers"],
                    "user_scenario": "Clara finishes a batch of candles. She snaps a photo on her phone, inputs 'Handmade Lavender Candle, $12', and lists it. Within 20 minutes, a local buyer orders it, and a courier picks it up."
                },
                {
                    "name": "Tim Vance", "role": "Convenience Shopper", "age": "32",
                    "goals": ["Support neighborhood businesses", "Receive orders on the same day", "View live map shipment delivery status"],
                    "pain_points": ["Slow shipping times", "High service fee markup costs", "Generic mass-produced options"],
                    "user_scenario": "Tim needs a birthday gift. He browses Clara's shop, orders same-day shipping, tracks the courier live on a map, and gets the candle in 90 minutes."
                }
            ],
            "purpose_scope": "Define MVP specs for a hyperlocal mobile-first marketplace connecting local vendors with shoppers using local couriers.",
            "goals_success_criteria": [
                {"objective": "Onboarding speed", "measurable_target": "Vendor shop setup completed in < 5 minutes"},
                {"objective": "Delivery times", "measurable_target": "Local delivery completed in < 2 hours average"},
                {"objective": "Merchant costs", "measurable_target": "Merchant transaction fees kept under 2.5%"}
            ],
            "functional_requirements": [
                "Mobile-first vendor store builder interface.",
                "Live map delivery tracking module integrating Google Maps.",
                "Automated merchant balance payouts engine."
            ],
            "non_functional_requirements": [
                "Secure payments processing via Stripe SDK integrations.",
                "Database scaling optimized for high geospatial query volumes."
            ],
            "user_stories": [
                {"story_id": "US-01", "user_role": "Vendor", "action": "list products via app photos", "benefit": "I can launch a digital storefront instantly without complex web building"},
                {"story_id": "US-02", "user_role": "Shopper", "action": "track my order on a live map", "benefit": "I know exactly when my delivery courier will arrive at the door"}
            ],
            "acceptance_criteria": [
                {"story_id": "US-01", "scenarios": ["Given an uploaded photo, When item details are submitted, Then the shop listing updates in < 3 seconds."]},
                {"story_id": "US-02", "scenarios": ["Given an active delivery, When courier coordinates update, Then the shopper map refits."]}
            ],
            "roadmap": [
                {"phase_name": "Phase 1: Vendor Core", "focus": "Mobile catalog builders, Stripe payment integrations, and manual dispatch couriers.", "milestones": ["Store setup interfaces", "Stripe payment flow", "Manual delivery dispatch"], "timeline": "Weeks 1-4"},
                {"phase_name": "Phase 2: Live Logistics", "focus": "Live courier map integrations, route optimization, and push notification builders.", "milestones": ["Courier map tracker app", "Geospatial query routing", "Courier alert engines"], "timeline": "Months 2-3"},
                {"phase_name": "Phase 3: Inventory AI", "focus": "AI demand forecasting, automated merchant discounts, and cross-district scaling.", "milestones": ["AI merchant sales insights", "Automatic discount engine", "Cross-city shipping ledger"], "timeline": "Months 4-6"}
            ],
            "mermaid_gantt": "gantt\n    title Ecom release\n    dateFormat YYYY-MM-DD\n    section MVP Core\n    Vendor Catalog Core :2026-07-01, 10d\n    Stripe Payment Link :after a1, 15d",
            "risks": [
                {"description": "Courier network bootstrap", "category": "Project", "impact": "High", "probability": "High", "mitigation": "Partner with regional gig-economy delivery networks during initial expansion phases."},
                {"description": "Stripe payment fraud", "category": "Technical", "impact": "High", "probability": "Medium", "mitigation": "Integrate Radar security checkers on checkout routes to block card testing."}
            ],
            "kpis": {
                "acquisition": [
                    {"metric": "Merchant signups", "target": "> 100/month", "notes": "Local vendor craft fairs"},
                    {"metric": "Shopper acquisition cost (CAC)", "target": "< $8", "notes": "Targeted local delivery vouchers"}
                ],
                "activation": [
                    {"metric": "First shop listing", "target": "> 90%", "notes": "Registered merchants adding products"},
                    {"metric": "First completed checkout", "target": "> 70%", "notes": "App installs making their first purchase"}
                ],
                "retention": [
                    {"metric": "Active buyer share", "target": "> 40%", "notes": "Shoppers ordering monthly"},
                    {"metric": "Merchant retention", "target": "> 95%", "notes": "Active merchants maintaining active catalogs"}
                ],
                "revenue": [
                    {"metric": "Merchant yield", "target": "2.5% fee", "notes": "Platform fee on payment routes"},
                    {"metric": "Delivery surcharge margin", "target": "> 15%", "notes": "Profit margin on automated courier matching fees"}
                ]
            }
        },
        "saas": {
            "cat": "B2B SaaS Productivity Platform",
            "audience": "Project Managers, Operations Leads & Remote Teams",
            "problem": "inefficient cross-functional workflows, fragmented team collaboration files, and slow status reporting routines",
            "trends": [
                "Asynchronous Collaboration: Teams moving away from meetings towards document-based status updates.",
                "No-Code Workflow Builders: Users customizing task states without engineering assistance.",
                "AI Project Summaries: Automated status updates compiled from work logs in real-time."
            ],
            "tam": "$24.5 B", "sam": "$6.2 B", "som": "$170 M",
            "sizing_rationale": "Sized based on regional per-user SaaS license pricing and target team adoption benchmarks.",
            "strengths": ["Custom no-code workflow builders", "Real-time collaborative document editor", "Automated project reporting templates"],
            "weaknesses": ["Integration setup overhead for large teams", "Steeper initial feature learning curves"],
            "opportunities": ["Direct integrations with corporate directories (SSO)", "Expanding templates marketplace for workflows"],
            "threats": ["Massive software conglomerates bundle deals", "Downward pricing pressure from low-cost tools"],
            "competitors": [
                {"name": "Atlassian Jira", "strengths": ["Deep software dev focus", "Massive scale and customization"], "weaknesses": ["Extremely complex UI", "Very slow load speeds"], "differentiation": "Features lightweight interfaces (load < 1s) and zero-config default workflows"},
                {"name": "Monday.com", "strengths": ["Exceptional visual layouts", "Aggressive B2B marketing"], "weaknesses": ["High per-user price tiers", "Clunky document editor"], "differentiation": "Combines visual task tracking directly inside collaborative docs"},
                {"name": "ClickUp", "strengths": ["Massive list of features", "Aggressive free tiers"], "weaknesses": ["Bloated interfaces", "Frequent system lagging"], "differentiation": "Focuses strictly on targeted workflow speed and AI project summaries"}
            ],
            "personas": [
                {
                    "name": "Sarah Jenkins", "role": "Operations Lead / Project Manager", "age": "29",
                    "goals": ["Centralize operational work updates", "Reduce reporting times by 40%", "Share interactive progress charts"],
                    "pain_points": ["Constantly checking five tools", "Manual email updates are slow", "Read-only seats are expensive"],
                    "user_scenario": "Sarah is running late. She gets a client request for project status. She opens the app, copies a read-only progress chart link, and shares it in 10 seconds."
                },
                {
                    "name": "Marcus Chen", "role": "VP of Technology & Systems", "age": "42",
                    "goals": ["Secure data asset storage", "Maintain compliance records", "Audit team license seats usage"],
                    "pain_points": ["Proprietary lock-in formats", "Hidden API rate overruns", "No granular access controls"],
                    "user_scenario": "Marcus conducts a quarterly software review. He logs into the admin portal, runs compliance exports, audits access roles, and saves $4k/month in license overhead."
                }
            ],
            "purpose_scope": "Define MVP requirements for a collaborative workspace compiling documents, task logs, and automated status reports.",
            "goals_success_criteria": [
                {"objective": "System efficiency", "measurable_target": "Average page load speeds < 1.0 seconds"},
                {"objective": "Onboarding speed", "measurable_target": "Workspace setups completed in < 3 clicks"},
                {"objective": "Licensing value", "measurable_target": "Admin overhead savings of > 20% compared to Jira"}
            ],
            "functional_requirements": [
                "Visual interactive Kanban and Gantt timeline boards.",
                "Real-time rich text document collaboration editor.",
                "Automated status export systems (PDF and Markdown)."
            ],
            "non_functional_requirements": [
                "Data storage fully encrypted in transit and at rest.",
                "High availability architecture aiming for 99.9% uptime."
            ],
            "user_stories": [
                {"story_id": "US-01", "user_role": "Manager", "action": "build visual task state flows", "benefit": "my team stays aligned without manual meetings"},
                {"story_id": "US-02", "user_role": "Coordinator", "action": "export dashboard statuses", "benefit": "I can share reports instantly with clients"}
            ],
            "acceptance_criteria": [
                {"story_id": "US-01", "scenarios": ["Given task boards, When item states change, Then active dashboard analytics refresh."]},
                {"story_id": "US-02", "scenarios": ["Given a progress view, When clicking export status, Then compile a clean Markdown report."]}
            ],
            "roadmap": [
                {"phase_name": "Phase 1: Workspace Core", "focus": "Kanban board modules, collaborative document editing, and basic exports.", "milestones": ["Kanban board framework", "Collaborative editor setup", "Markdown export hooks"], "timeline": "Weeks 1-4"},
                {"phase_name": "Phase 2: Automation", "focus": "No-code workflow automations, custom fields, and email notification bridges.", "milestones": ["No-code workflow trigger", "Custom field database", "Email bridge scheduler"], "timeline": "Months 2-3"},
                {"phase_name": "Phase 3: AI Reporting", "focus": "AI status summarizer engines, enterprise SSO (SAML), and API integrations.", "milestones": ["AI status compilation", "SAML SSO configuration", "Public developer API keys"], "timeline": "Months 4-6"}
            ],
            "mermaid_gantt": "gantt\n    title SaaS release\n    dateFormat YYYY-MM-DD\n    section MVP Core\n    Workspace Kanban    :2026-07-01, 12d\n    Collaborative Docs :after a1, 10d",
            "risks": [
                {"description": "Data leakage", "category": "Technical", "impact": "High", "probability": "Low", "mitigation": "Enforce strict role-based access control (RBAC) and data classification layers."},
                {"description": "Competitor pricing pressure", "category": "Market", "impact": "Medium", "probability": "Medium", "mitigation": "Offer free read-only collaborator seats to reduce entry barriers."}
            ],
            "kpis": {
                "acquisition": [
                    {"metric": "Team signup conversion", "target": "> 18%", "notes": "Workspace creations conversion"},
                    {"metric": "Paid conversion rate", "target": "> 6%", "notes": "From organic organic search"}
                ],
                "activation": [
                    {"metric": "Invite conversion", "target": "> 60%", "notes": "First team invites accepted"},
                    {"metric": "First project created", "target": "> 85%", "notes": "Registered organizations adding workspaces"}
                ],
                "retention": [
                    {"metric": "WAU active share", "target": "> 50%", "notes": "Team members returning weekly"},
                    {"metric": "Monthly subscriber retention", "target": "> 97%", "notes": "Enterprise contract renewals"}
                ],
                "revenue": [
                    {"metric": "Standard license", "target": "$9/user/mo", "notes": "Basic team subscription plan"},
                    {"metric": "Expansion rate margin", "target": "> 15% increase", "notes": "Adding collaborators to active hubs"}
                ]
            }
        }
    }

    # Fetch corresponding database data
    db = MOCK_DB[key]

    # Customize mock data based on input keywords
    def customize_mock_data(data, product_name: str, key: str, idea_text: str):
        lower_idea = idea_text.lower()
        
        # PetTech specific customizations
        is_cat = any(w in lower_idea for w in ["cat", "feline", "kitty", "kittens", "kitten"])
        is_dog = any(w in lower_idea for w in ["dog", "canine", "puppy", "puppies", "pup"])
        is_bowl = any(w in lower_idea for w in ["bowl", "feeder", "food", "diet", "feed", "eat"])
        is_collar = any(w in lower_idea for w in ["collar", "gps", "location", "tracker", "leash"])
        
        # AI specific customizations
        is_figma = "figma" in lower_idea
        is_jira = "jira" in lower_idea
        is_security = any(w in lower_idea for w in ["security", "vulnerability", "audit", "compliance"])
        
        # FoodTech specific customizations
        is_vegan = any(w in lower_idea for w in ["vegan", "plant-based", "vegetarian"])
        is_grocery = any(w in lower_idea for w in ["grocery", "groceries", "supermarket"])

        def replacer(text: str) -> str:
            if not isinstance(text, str):
                return text
            
            # Replace placeholder name first
            text = text.replace("{product_name}", product_name)
            
            # Customizations for Pet
            if key == "pet":
                if is_cat and not is_dog:
                    text = text.replace("Dog", "Cat").replace("dog", "cat")
                    text = text.replace("Golden Retriever", "Siamese Cat")
                if is_bowl and not is_collar:
                    text = text.replace("collar system", "smart bowl").replace("collar tracker", "smart bowl")
                    text = text.replace("smart collar", "smart bowl").replace("smart collars", "smart bowls")
                    text = text.replace("collar", "smart bowl").replace("collars", "smart bowls")
                    text = text.replace("GPS tracking", "diet tracking").replace("GPS", "diet sensor")
                    text = text.replace("geofence", "feeding schedule").replace("virtual geofence", "feeding schedule")
                    text = text.replace("escapes the yard", "over-eats or misses a meal")
                    text = text.replace("escaping", "over-eating")
                    text = text.replace("activity, location, and hydration", "food intake, eating speed, and diet health")
                    text = text.replace("activity", "dietary intake").replace("step counter", "weight scale sensor")
            
            # Customizations for AI
            elif key == "ai":
                if is_figma:
                    text = text.replace("code reviewer", "Figma design auditor").replace("code compliance", "UI/UX consistency")
                    text = text.replace("developer", "designer").replace("Developer", "Designer")
                    text = text.replace("PR approval", "design handoff").replace("PR", "design")
                    text = text.replace("VS Code", "Figma").replace("codebase", "design files")
                elif is_security:
                    text = text.replace("workflow tool", "automated security auditor").replace("code reviewer", "security auditor")
                    
            # Customizations for Food
            elif key == "food":
                if is_vegan:
                    text = text.replace("local ingredient", "local vegan ingredient").replace("home cooks", "vegan home cooks")
                if is_grocery:
                    text = text.replace("food delivery marketplace", "grocery delivery marketplace").replace("food delivery", "grocery delivery")
            
            return text

        def recurse(node):
            if isinstance(node, dict):
                return {k: recurse(v) for k, v in node.items()}
            elif isinstance(node, list):
                return [recurse(x) for x in node]
            elif isinstance(node, str):
                return replacer(node)
            return node

        return recurse(data)

    db = customize_mock_data(db, product_name, key, clean)
    cat = db["cat"]
    audience = db["audience"]
    problem = db["problem"]
    trends = db["trends"]
    tam, sam, som = db["tam"], db["sam"], db["som"]
    rationale = db["sizing_rationale"]
    strengths, weaknesses = db["strengths"], db["weaknesses"]
    opportunities, threats = db["opportunities"], db["threats"]
    competitors = db["competitors"]
    personas = db["personas"]
    purpose_scope = db["purpose_scope"]
    goals_success_criteria = db["goals_success_criteria"]
    functional_requirements = db["functional_requirements"]
    non_functional_requirements = db["non_functional_requirements"]
    user_stories = db["user_stories"]
    acceptance_criteria = db["acceptance_criteria"]
    roadmap_phases = db["roadmap"]
    mermaid_gantt = db["mermaid_gantt"]
    risks = db["risks"]
    kpis = db["kpis"]

    # Construct the return items
    market_research = {
        "executive_summary": f"**{product_name}** enters the market as a disruptive **{cat}** targeting a critical friction point: {problem}. The segment shows high-growth indicators driven by modern UX expectations and API-first integrations.",
        "market_trends": trends,
        "market_sizing": {
            "tam": tam,
            "sam": sam,
            "som": som,
            "rationale": f"Calculated based on global {cat} demand patterns and initial GTM focus on {audience}. {rationale}"
        },
        "swot": {
            "strengths": strengths,
            "weaknesses": weaknesses,
            "opportunities": opportunities,
            "threats": threats
        }
    }

    # Custom Competitors Analysis
    competitor_list = []
    for c in competitors:
        competitor_list.append({
            "name": c["name"],
            "strengths": c["strengths"],
            "weaknesses": c["weaknesses"],
            "differentiation": f"For {product_name}: {c['differentiation']}."
        })

    # Custom Personas
    persona_list = []
    for p in personas:
        persona_list.append({
            "name": p["name"],
            "role": p["role"],
            "age": p["age"],
            "goals": p["goals"],
            "pain_points": p["pain_points"],
            "user_scenario": p["user_scenario"].replace("{product_name}", f"**{product_name}**")
        })

    # Custom PRD
    prd = {
        "purpose_scope": purpose_scope.replace("{product_name}", f"**{product_name}**"),
        "goals_success_criteria": goals_success_criteria,
        "functional_requirements": functional_requirements,
        "non_functional_requirements": non_functional_requirements
    }

    # Custom Roadmap
    roadmap = {
        "phases": [],
        "mermaid_gantt": mermaid_gantt.replace("{product_name}", product_name)
    }
    for phase in roadmap_phases:
        roadmap["phases"].append({
            "phase_name": phase["phase_name"],
            "focus": phase["focus"],
            "milestones": phase["milestones"],
            "timeline": phase["timeline"]
        })

    # Custom source attributions
    sources = [
        f"https://www.crunchbase.com/organization/{competitor_list[0]['name'].lower().replace(' ', '-')}",
        f"https://www.crunchbase.com/organization/{competitor_list[1]['name'].lower().replace(' ', '-')}",
        f"https://www.crunchbase.com/organization/{competitor_list[2]['name'].lower().replace(' ', '-')}",
        f"https://www.gartner.com/reviews/market/{key}-solutions",
        f"https://www.techcrunch.com/search/{key}-startup"
    ]

    return {
        "product_name": product_name,
        "category": cat,
        "audience": audience,
        "problem": problem,
        "competitors_list": [c["name"] for c in competitor_list],
        
        # Centralized plan data
        "market_research": market_research,
        "competitors": competitor_list,
        "personas": persona_list,
        "prd": prd,
        "user_stories": user_stories,
        "acceptance_criteria": acceptance_criteria,
        "roadmap": roadmap,
        "risks": risks,
        "kpis": kpis,
        "source_attributions": sources
    }
