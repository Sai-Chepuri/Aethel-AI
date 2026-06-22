import re

def get_mock_context(idea: str):
    clean = re.sub(r"['\"]", "", idea).strip()

    # Derive a short product name
    name_match = (
        re.search(r"called\s+([A-Za-z0-9 _-]+)", clean, re.I)
        or re.search(r"named?\s+([A-Za-z0-9 _-]+)", clean, re.I)
        or re.search(r"^([A-Za-z0-9 _-]{3,25})", clean)
    )
    if name_match:
        product_name = name_match.group(1).strip().title()
    else:
        product_name = " ".join(w.capitalize() for w in clean.split()[:3]) + " App"

    # Category detection
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

    return {
        "product_name": product_name,
        "category": cat,
        "audience": audience,
        "problem": problem,
        "competitors_list": comp
    }
