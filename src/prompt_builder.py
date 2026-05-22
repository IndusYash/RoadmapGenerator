import json
from pathlib import Path
from typing import Tuple, Dict, Any

from .schemas import InputProfile


ROOT = Path(__file__).resolve().parents[1]
SYSTEM_PROMPT_PATH = ROOT / "prompts" / "system_prompt_v1.txt"


def load_system_prompt() -> str:
    return SYSTEM_PROMPT_PATH.read_text(encoding="utf-8")


def _urgency_band_and_factor(urgency_months: int) -> Tuple[str, float]:
    if urgency_months <= 1:
        return "immediate", 1.6
    if urgency_months <= 3:
        return "high", 1.3
    if urgency_months <= 6:
        return "medium", 1.0
    return "low", 0.7


def sanitize_profile(profile: InputProfile) -> Dict[str, Any]:
    # Keep only allowed fields and convert to simple types
    data = {
        "icp_type": profile.icp_type,
        "name": profile.name,
        "current_role": profile.current_role,
        "target_role": profile.target_role,
        "urgency_months": int(profile.urgency_months),
        "skills": profile.skills or [],
        "language": profile.language,
        "experience_months": int(profile.experience_months) if profile.experience_months is not None else None,
        "location": profile.location,
    }
    return data


def build_prompt(profile: InputProfile) -> Tuple[str, str]:
    """Return (system_prompt, user_prompt) ready to send to the model.

    The user_prompt contains a sanitized JSON block and a small few-shot example.
    """
    system = load_system_prompt()
    sanitized = sanitize_profile(profile)
    band, factor = _urgency_band_and_factor(int(profile.urgency_months))

    # Build user-facing JSON block
    user_profile_json = json.dumps(sanitized, ensure_ascii=False)

    # Small inline few-shot examples (abbreviated) to show structure — two short examples
    few_shot = {
        "examples": [
            {
                "icp_type": "ICP-A",
                "language": "en",
                "note": "Abbreviated example — real output should expand to 7 milestones",
                "milestones_sample": [
                    {
                        "code": "M01",
                        "title": "Project scaffold",
                        "phase": 1,
                        "target_month": 1,
                        "expected_completion": "By the end of Month 1",
                        "estimated_duration_weeks": 4,
                        "salary_tier": "entry",
                        "unlock_statement": "You'll demo a simple full-stack app and explain its architecture.",
                        "blur_level": 0,
                        "scenario_count": 2,
                        "assessment_count": 2,
                        "mock_interview_count": 0,
                    }
                ],
            },
            {
                "icp_type": "ICP-B",
                "language": "hi",
                "note": "Abbreviated example — real output should expand to 7 milestones",
                "milestones_sample": [
                    {
                        "code": "M01",
                        "title": "Typing confidence",
                        "phase": 1,
                        "target_month": 1,
                        "expected_completion": "महीने 1 के अंत तक",
                        "estimated_duration_weeks": 4,
                        "salary_tier": "entry",
                        "unlock_statement": "आप पहले महीने में 40 शब्द/मिनट टाइपिंग की निडरता हासिल करेंगे।",
                        "blur_level": 0,
                        "scenario_count": 1,
                        "assessment_count": 1,
                        "mock_interview_count": 0,
                    }
                ],
            },
        ]
    }

    user_prompt = (
        "---BEGIN USER PROFILE JSON---\n"
        f"{user_profile_json}\n"
        "---END USER PROFILE JSON---\n\n"
        "CONTEXT:\n"
        f"urgency_band: {band}\n"
        f"urgency_compression_factor: {factor}\n\n"
        "FEW_SHOT_EXAMPLES (abbreviated):\n"
        f"{json.dumps(few_shot, ensure_ascii=False)}\n\n"
        "INSTRUCTIONS:\n"
        "Using only the provided profile and the system prompt rules, generate a single JSON object matching the RoadmapResponse schema. "
        "Start the JSON with <<ROADMAP_JSON>> and end with <<END_ROADMAP_JSON>>. Return only the JSON delimited by those markers."
    )

    return system, user_prompt


if __name__ == "__main__":
    # Quick local example
    sample = {
        "icp_type": "ICP-A",
        "name": "Aisha Sharma",
        "current_role": "Final-year Student",
        "target_role": "Software Engineer",
        "urgency_months": 6,
        "skills": ["python", "data-structures"],
        "language": "en",
        "experience_months": 0,
        "location": "Bengaluru",
    }
    profile = InputProfile(**sample)
    sys, user = build_prompt(profile)
    print("SYSTEM PROMPT (truncated):")
    print(sys[:400])
    print("\nUSER PROMPT: \n")
    print(user)
