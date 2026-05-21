# Career Roadmap Generator — Problem Understanding

## Short Summary

- Challenge: Build a production-style AI microservice (“Career Roadmap Generator”) that accepts a structured JSON user profile and returns a strictly validated, deeply personalized 7-milestone career roadmap JSON (exactly `M01`–`M07`) suitable for frontend rendering.
- Key constraints: Output must be valid JSON, follow a fixed milestone schema (only required fields), enforce fixed blur levels, and adapt content by ICP, language, urgency, and skills while minimizing hallucinations.

## Purpose of the Roadmap Generator

- Primary goal: Produce emotionally motivating, role-specific, actionable 7-step career roadmaps that frontend apps can render directly.
- User groups: Support two ICPs: ICP-A (high_wage, English, technical careers) and ICP-B (low_wage, Hindi, practical/confidence-building careers).
- Behavioral goals: Personalization (role, skills, urgency), deterministic structure, vivid unlock statements, progressive abstraction (blur levels), and language/style switching.

## Understanding of Evaluation Rubric

- Schema correctness: Output must validate against the Pydantic schema; no extra or missing fields.
- Milestone count & codes: Exactly 7 milestones labeled `M01`→`M07`.
- Blur-level rules: `M01=0`, `M02=0`, `M03=1`, `M04=2`, `M05-M07=3` — strictly enforced.
- Unlock statements quality: Vivid, specific, emotionally motivating, personalized, non-repetitive.
- Content relevance: Milestones match target role, skills, urgency, and ICP (technical projects for software roles; practical steps for gig/support roles).
- Language & tone: Correct language (English/Hindi) and tone for ICP.
- Robustness: Handles edge cases, retries malformed model output, and limits hallucination.
- Determinism & safety: Prompting and post-processing must reduce nondeterministic hallucinations; system should include retry/backoff and validation.

## Identification of Auto-Fail Conditions

- Invalid JSON: Any response that is not parseable JSON.
- Wrong milestone count: Fewer or more than 7 milestones.
- Invalid or extra fields: Missing any required field (`code`, `title`, `salary_tier`, `unlock_statement`, `blur_level`, `scenario_count`, `assessment_count`, `mock_interview_count`) or presence of unknown fields.
- Incorrect blur levels: Any milestone not using the fixed blur values.
- Duplicate titles or repetitive unlocks: Non-unique milestone titles or repeated/near-identical unlock statements.
- Wrong language/tone for ICP: ICP-A receives Hindi output or ICP-B receives English-only technical tone.
- Hallucinated personal facts: Invented education/employment details not present in input.
- No retry/validation: System returns raw model output without schema validation or retry on malformed JSON.
- Unsafe or disallowed content: Any harmful, discriminatory, or privacy-violating statements.

## Outcome / System Contract

- Input → Output pipeline: Validate input → build dynamic prompt (ICP, language, urgency) → call Claude with guarded prompt → extract JSON → validate against strict Pydantic schema → retry up to N times on malformed JSON → return final roadmap.
- Milestone contract: Exactly 7 milestones `M01`–`M07`, each with only the required fields and blur levels enforced.
- Personalization contract: Content must reflect `target_role`, `current_role`, `skills`, `urgency`, and ICP type (tone, complexity, salary tiers), switching language and progression logic accordingly.
- Quality guarantees: Vivid unlock statements, no hallucinations, deterministic prompt templates, test coverage for edge cases, and clear error responses for auto-fail conditions.

If this README looks good, next steps are: scaffold a FastAPI project and add Pydantic schemas.
