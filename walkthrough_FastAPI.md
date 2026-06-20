# Walkthrough — ProductForge AI FastAPI Backend

## Summary

The Python FastAPI backend for **ProductForge AI** has been fully built, tested, and verified. It runs as a standalone server at `http://127.0.0.1:8000` and is compatible with the existing frontend dashboard.

---

## Project Structure

```
backend/
├── main.py                    # FastAPI app, CORS, routing, static file mount
├── .env                       # Environment config (PORT, GEMINI_API_KEY)
├── requirements.txt           # Python package dependencies
├── models/
│   └── product_idea.py        # Pydantic input model (request body)
├── schemas/
│   └── response_schema.py     # Pydantic output model (response body)
└── services/
    └── gemini_service.py      # Gemini API client + local mock generator
```

---

## Files Created

### [product_idea.py](file:///Users/monish_ch/Desktop/Agentic%20AI/Kaggle%20Course/ProductForge%20AI/backend/models/product_idea.py)
Pydantic model that validates the incoming JSON request:
```python
class ProductIdea(BaseModel):
    idea: str = Field(..., min_length=1, ...)
```
Pydantic enforces a non-empty `idea` string, returning a structured `422 Unprocessable Entity` if the field is missing.

### [response_schema.py](file:///Users/monish_ch/Desktop/Agentic%20AI/Kaggle%20Course/ProductForge%20AI/backend/schemas/response_schema.py)
Pydantic model that defines and validates the outgoing response:
```python
class ProductPlan(BaseModel):
    marketResearch: str
    personas: str
    prd: str
    roadmap: str
    kpis: str
```

### [gemini_service.py](file:///Users/monish_ch/Desktop/Agentic%20AI/Kaggle%20Course/ProductForge%20AI/backend/services/gemini_service.py)
Service layer with two generation strategies:
- **Gemini API path**: Uses `httpx.AsyncClient` to call the Gemini `gemini-2.5-flash` model with a structured `responseSchema`, requesting clean JSON-shaped markdown for each section.
- **Mock fallback path**: An intelligent keyword-based generator that auto-detects the product category (AI, FoodTech, Fintech, EdTech, E-commerce, Health & Wellness, or default SaaS) and produces a fully tailored product plan with no external dependencies.

### [main.py](file:///Users/monish_ch/Desktop/Agentic%20AI/Kaggle%20Course/ProductForge%20AI/backend/main.py)
Main FastAPI application that:
- Loads `.env` via `python-dotenv`
- Applies `CORSMiddleware` (open in development)
- Exposes `POST /generate` (canonical per spec)
- Exposes `POST /api/generate` (backward-compatible with the Node.js frontend)
- Mounts the `public/` directory as static files to serve the dashboard UI

---

## Verification Results

| Test | Result |
| :--- | :--- |
| Python syntax check (`py_compile`) | ✅ All 4 files passed |
| `POST /generate` → valid idea | ✅ Returns 5-key JSON (`marketResearch`, `personas`, `prd`, `roadmap`, `kpis`) |
| `POST /api/generate` → valid idea | ✅ Identical response shape |
| `POST /generate` → missing `idea` field | ✅ Returns `422` with structured error detail |
| `GET /docs` (Swagger UI) | ✅ HTTP 200 |

---

## How to Start the Backend

```bash
# From the project root
source .venv/bin/activate
cd backend
uvicorn main:app --host 127.0.0.1 --port 8000 --reload
```

> The `--reload` flag enables hot-reloading when source files change — ideal for development.

- **API**: [http://127.0.0.1:8000/generate](http://127.0.0.1:8000/generate)
- **Swagger Docs**: [http://127.0.0.1:8000/docs](http://127.0.0.1:8000/docs)
- **ReDoc**: [http://127.0.0.1:8000/redoc](http://127.0.0.1:8000/redoc)
- **Dashboard UI**: [http://127.0.0.1:8000](http://127.0.0.1:8000) (served from `public/`)

## Optional: Enable Gemini API

Add your key to `backend/.env`:
```env
GEMINI_API_KEY=your-actual-api-key-here
```
The service will automatically switch from the mock engine to live Gemini generation on the next restart.
