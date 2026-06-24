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

# CORS configuration
raw_origins = os.getenv("ALLOWED_ORIGINS", "")
if raw_origins.strip():
    ALLOWED_ORIGINS = [o.strip() for o in raw_origins.split(",") if o.strip()]
else:
    # Default local development origins
    ALLOWED_ORIGINS = [
        "http://localhost:3000",
        "http://127.0.0.1:3000",
        "http://localhost:5000",  # Firebase Hosting emulator default
        "http://127.0.0.1:5000",
        "http://localhost:8000",  # FastAPI default
        "http://127.0.0.1:8000",
    ]

def get_allowed_origins() -> list:
    """Return the list of allowed CORS origins."""
    return ALLOWED_ORIGINS
