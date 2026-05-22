"""
FastAPI HTTP wrapper for the AI Career Roadmap Generator pipeline.

Exposes:
  POST /generate-roadmap  →  runs the full AI pipeline and returns a validated
                              RoadmapResponse JSON.

Run with:
  uvicorn api:app --reload --port 8000

The React frontend (port 5173) is whitelisted in CORS origins.
"""

from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel, Field, validator
from typing import List, Optional, Literal
import asyncio
import logging

from src.main import run_pipeline

logger = logging.getLogger(__name__)
logging.basicConfig(level=logging.INFO)

app = FastAPI(
    title="AI Career Roadmap Generator",
    description="Generates a personalized 7-milestone career roadmap powered by AI.",
    version="1.0.0",
)

# Allow local Vite dev server and common production origins
app.add_middleware(
    CORSMiddleware,
    allow_origins=[
        "http://localhost:5173",
        "http://127.0.0.1:5173",
        "http://localhost:3000",
    ],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


# ---------------------------------------------------------------------------
# Request / Response models (mirrors src/schemas.py for the HTTP layer)
# ---------------------------------------------------------------------------

ICPType = Literal["ICP-A", "ICP-B"]
Language = Literal["en", "hi"]


class GenerateRoadmapRequest(BaseModel):
    name: str = Field(..., min_length=1, max_length=120)
    icp_type: ICPType
    current_role: Optional[str] = Field(None, max_length=120)
    target_role: str = Field(..., min_length=1, max_length=120)
    urgency_months: int = Field(..., ge=0, le=60)
    skills: List[str] = Field(default_factory=list)
    experience_months: Optional[int] = Field(None, ge=0, le=600)
    language: Optional[Language] = None
    location: Optional[str] = Field(None, max_length=120)

    @validator("skills", pre=True)
    def normalize_skills(cls, v):
        if not v:
            return []
        return [s.strip().lower() for s in v if isinstance(s, str) and s.strip()]

    class Config:
        extra = "ignore"


# ---------------------------------------------------------------------------
# Routes
# ---------------------------------------------------------------------------


@app.get("/health")
async def health():
    """Simple liveness check."""
    return {"status": "ok"}


@app.post("/generate-roadmap")
async def generate_roadmap_endpoint(request: GenerateRoadmapRequest):
    """
    Run the full AI pipeline and return a validated roadmap.

    The pipeline will use Claude AI if an API key is configured in .env,
    otherwise it falls back to the deterministic local milestone generator.
    """
    try:
        roadmap = await run_pipeline(request.dict())
        return roadmap
    except ValueError as e:
        raise HTTPException(status_code=422, detail=str(e))
    except Exception as e:
        logger.exception("Pipeline failed")
        raise HTTPException(status_code=500, detail=f"Roadmap generation failed: {str(e)}")
