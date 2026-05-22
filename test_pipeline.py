import asyncio
import json
import logging
from src.main import run_pipeline, sample_input
from src.validator import validate_roadmap_input
from src.milestone_generator import generate_roadmap
from src.schemas import InputProfile

logging.basicConfig(level=logging.INFO)

async def test():
    profile = {
        "icp_type": "ICP-A",
        "name": "YASH",
        "current_role": "FINAL YEAR STUDENT",
        "target_role": "AI ENGINEER",
        "urgency_months": 12,
        "skills": ["PYTHON"],
        "language": "en",
        "experience_months": 0,
        "location": "NOIDA",
    }
    print("--- 1. Testing Fallback Generation directly ---")
    try:
        profile_obj = InputProfile(**profile)
        roadmap = generate_roadmap(profile_obj)
        print("Fallback generation succeeded!")
        print("Generated fields sample:", json.dumps(roadmap.model_dump()["milestones"][0], indent=2, ensure_ascii=False))
        
        # Verify validation
        rv = validate_roadmap_input(roadmap.model_dump())
        print("Fallback validation result:", rv.valid, "errors:", rv.errors)
    except Exception as e:
        print("Fallback generation/validation failed with exception:", e)

    print("\n--- 2. Testing Validation with 'Milestone X' format and new fields ---")
    mock_llm_output = {
        "milestones": [
            {
                "code": f"Milestone {i}",
                "title": f"Title {i}",
                "phase": 1 if i <= 2 else (2 if i <= 4 else 3),
                "target_month": i,
                "expected_completion": f"By the end of Month {i}",
                "estimated_duration_weeks": 4,
                "salary_tier": "entry",
                "unlock_statement": f"You will unlock unique achievement {i} and walk through the architecture.",
                "blur_level": [0, 0, 1, 2, 3, 3, 3][i-1],
                "scenario_count": 2,
                "assessment_count": 2,
                "mock_interview_count": 1
            }
            for i in range(1, 8)
        ]
    }
    
    rv = validate_roadmap_input(mock_llm_output)
    print("Mock LLM validation result:", rv.valid, "errors:", rv.errors)
    if rv.valid:
        print("Normalized code in output matches standard format (M01):", [m.code for m in rv.roadmap.milestones])

    print("\n--- 3. Running Full Pipeline ---")
    try:
        res = await run_pipeline(profile)
        print("Pipeline result sample (first milestone):")
        print(json.dumps(res["milestones"][0], indent=2, ensure_ascii=False))
    except Exception as e:
        print("Pipeline run failed with exception:", e)

if __name__ == "__main__":
    asyncio.run(test())
