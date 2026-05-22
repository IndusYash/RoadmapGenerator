"""
Central orchestration for the Career Roadmap Generator.

Pipeline:
  Input JSON -> Prompt Builder -> Claude API Client -> Response Extractor -> Schema Validator -> Final Output

This script attempts a full end-to-end run. If the Claude API is not configured or the model output
is malformed, it falls back to the local deterministic `milestone_generator` to ensure a valid roadmap
is produced (useful for development and testing).

Responsibilities of modules:
- prompt_builder: constructs system + user prompt from InputProfile
- claude_client: sends prompt to Anthropic Claude and returns raw text
- extractor: extracts JSON object from model text (delimiters, code fences, fallback)
- validator: validates parsed JSON against RoadmapResponse
- milestone_generator: deterministic local generator used as fallback

Run as a script for a single sample input. In production this logic should be exposed via an API layer.
"""

import asyncio
import json
import logging
from typing import Any, Dict, Optional

from .schemas import InputProfile
from .prompt_builder import build_prompt
from .claude_client import ClaudeClient, ClaudeClientError
from .extractor import parse_model_response
from .validator import validate_roadmap_input
from .milestone_generator import generate_roadmap

logger = logging.getLogger(__name__)
logging.basicConfig(level=logging.WARNING)
logging.getLogger("httpx").setLevel(logging.WARNING)


async def run_pipeline(profile_data: Dict[str, Any]) -> Dict[str, Any]:
    """Run the pipeline end-to-end and return the final validated roadmap dict.

    Steps:
    1. Validate and normalize input into InputProfile (Pydantic)
    2. Build prompts (system + user)
    3. Send to Claude (if configured)
    4. Extract JSON from model response
    5. Validate roadmap JSON against schema
    6. If any step fails, fall back to local deterministic generator
    """
    # 1) Validate input profile
    try:
        profile = InputProfile(**profile_data)
    except Exception as e:
        logger.exception("InputProfile validation failed")
        raise

    # 2) Build prompts
    system_prompt, user_prompt = build_prompt(profile)

    # 3) Prepare Claude client
    client = ClaudeClient()

    raw_model_text = None
    parsed = None

    # If no API key configured, skip model call and use fallback
    if not client.api_key:
        logger.info("No model API key configured; using local generator fallback.")
    else:
        try:
            # 4) Call Claude API
            raw_model_text = await client.send_prompt(system_prompt, user_prompt, temperature=0.0, max_tokens=1200)
            logger.debug("Received raw model output (truncated): %s", raw_model_text[:300].replace('\n', ' '))

            # 5) Extract JSON from the model response
            parsed, raw_json_str, had_extra = parse_model_response(raw_model_text)
            logger.debug("Extracted JSON from model (had_extra=%s)", had_extra)

            # 6) Validate extracted JSON
            result = validate_roadmap_input(parsed)
            if result.valid:
                logger.info("Model-generated roadmap validated successfully.")
                return result.roadmap.model_dump()
            else:
                main_cause = f"Schema validation failed: {result.errors}"
                logger.warning("Pipeline Error: Failed to validate model-generated roadmap. Main Cause: %s. Continuing with fallback generator.", main_cause)
                # fall through to fallback
        except ClaudeClientError as e:
            main_cause = f"Model API client error ({e})"
            logger.warning("Pipeline Error: Model call failed. Main Cause: %s. Continuing with fallback generator.", main_cause)
        except Exception as e:
            main_cause = f"Unexpected execution or JSON extraction failure ({e})"
            logger.warning("Pipeline Error: Extraction or orchestration failed. Main Cause: %s. Continuing with fallback generator.", main_cause)

    # Fallback deterministic generation
    try:
        logger.info("Generating deterministic roadmap fallback using `milestone_generator`.")
        roadmap = generate_roadmap(profile)
        # validate the generated roadmap as dict
        rv = validate_roadmap_input(roadmap.model_dump())
        if not rv.valid:
            logger.error("Fallback generated roadmap failed validation: %s", rv.errors)
            raise RuntimeError("Fallback generation produced invalid roadmap")
        logger.info("Fallback roadmap validated successfully.")
        return rv.roadmap.model_dump()
    except Exception as e:
        logger.exception("Fallback generation failed: %s", e)
        raise


def sample_input() -> Dict[str, Any]:
    return {
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


def _ask(prompt: str, default: Optional[str] = None) -> str:
    if default is not None:
        raw = input(f"{prompt} [{default}]: ").strip()
        return raw if raw else default
    return input(f"{prompt}: ").strip()


def _ask_int(prompt: str, default: int) -> int:
    while True:
        raw = _ask(prompt, str(default))
        try:
            return int(raw)
        except ValueError:
            print("Please enter a valid integer.")


def collect_user_input() -> Dict[str, Any]:
    """Collect input profile from terminal prompts.

    Data flow:
    - Terminal responses -> normalized dict -> InputProfile validation in run_pipeline().
    """
    print("Enter roadmap inputs (press Enter to accept defaults):")

    icp_type = _ask("icp_type (ICP-A or ICP-B)", "ICP-A")
    name = _ask("name", "Aisha Sharma")
    current_role = _ask("current_role", "Final-year Student")
    target_role = _ask("target_role", "Software Engineer")
    urgency_months = _ask_int("urgency_months", 6)
    skills_raw = _ask("skills (comma separated)", "python, data-structures")
    language = _ask("language (en or hi)", "en")
    experience_months = _ask_int("experience_months", 0)
    location = _ask("location", "Bengaluru")

    skills = [s.strip() for s in skills_raw.split(",") if s.strip()]

    return {
        "icp_type": icp_type,
        "name": name,
        "current_role": current_role,
        "target_role": target_role,
        "urgency_months": urgency_months,
        "skills": skills,
        "language": language,
        "experience_months": experience_months,
        "location": location,
    }


def main():
    # Input now comes from terminal prompts so users can run without editing code.
    profile = collect_user_input()
    roadmap = asyncio.run(run_pipeline(profile))
    # Print final validated roadmap JSON
    print(json.dumps(roadmap, ensure_ascii=False, indent=2))


if __name__ == "__main__":
    main()
