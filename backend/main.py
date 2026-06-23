import os
from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from fastapi.staticfiles import StaticFiles
from dotenv import load_dotenv

from models.product_idea import ProductIdea
from schemas.response_schema import ProductPlanResponse, GenerateResponse
from orchestrator.product_orchestrator import generate_product_plan


# Load env variables
load_dotenv()

app = FastAPI(
    title="Aethel AI API",
    description="Backend API for generating structured product strategy blueprints.",
    version="1.0.0"
)

# CORS configuration
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # Adjust in production
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# POST /generate — primary endpoint
@app.post("/generate", response_model=GenerateResponse)
async def generate_plan(payload: ProductIdea):
    try:
        api_key = (payload.apiKey or "").strip() or os.getenv("GEMINI_API_KEY", "").strip() or None
        plan_data = await generate_product_plan(payload.idea, api_key=api_key)
        
        # Save output using save_output utility
        try:
            from utils.save_output import save_generated_plan
            save_generated_plan(plan_data)
        except Exception as save_err:
            print(f"[main] Warning: Failed to save generated plan: {save_err}")
            
        return GenerateResponse(result=ProductPlanResponse(**plan_data))
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

# POST /api/generate — browser-client compatibility alias
@app.post("/api/generate", response_model=GenerateResponse)
async def generate_plan_compat(payload: ProductIdea):
    return await generate_plan(payload)

# Serve static frontend files
# Calculate the absolute path of public/ relative to main.py
current_dir = os.path.dirname(os.path.realpath(__file__))
public_dir = os.path.abspath(os.path.join(current_dir, "..", "public"))

if os.path.exists(public_dir):
    app.mount("/", StaticFiles(directory=public_dir, html=True), name="public")
else:
    print(f"Warning: Public static directory not found at {public_dir}")
