import os
from dotenv import load_dotenv

# Load env variables (supporting local development via .env)
load_dotenv()

# Centralized validation of required environment variables
GEMINI_API_KEY = os.getenv("GEMINI_API_KEY")

if not GEMINI_API_KEY or not GEMINI_API_KEY.strip():
    raise ValueError(
        "Critical Error: GEMINI_API_KEY environment variable is missing. "
        "Please provide the GEMINI_API_KEY in your system environment "
        "or define it in a local .env file."
    )

# Clean/Normalize API key value
GEMINI_API_KEY = GEMINI_API_KEY.strip()

def get_gemini_api_key() -> str:
    """Return the validated Gemini API key."""
    return GEMINI_API_KEY
