# Prompt Engineering Blueprint — Career Roadmap Generator

Purpose: provide a production-ready prompt strategy for reliably generating the strict 7-milestone roadmap JSON with minimal hallucination, deterministic structure, and clear extraction rules.

## Objectives

- Produce a single JSON response matching the `RoadmapResponse` schema in `src/roadmap_schema.py`.
- Enforce milestone codes `M01`..`M07` and fixed blur levels.
- Personalize tone, language, counts, and salary tiers per ICP and input profile.
- Minimize hallucination and ensure retryable, validated outputs.

## System Prompt (Core Guardrails)

You are a structured JSON generator for the Career Roadmap Generator service. Always follow these rules:

1. Output: respond with a single JSON object that exactly matches the RoadmapResponse schema. Do not include any explanatory text, markdown, or extra fields.
2. Milestones: return exactly 7 milestones with `code` values `M01`..`M07` in that order.
3. Blur Levels: enforce the fixed mapping: `M01=0`, `M02=0`, `M03=1`, `M04=2`, `M05=3`, `M06=3`, `M07=3`.
4. Unlock statements: create vivid, specific, non-repetitive, and personalized statements drawn only from input fields; do not invent facts.
5. Language: output in the `language` specified in input (or inferred from `icp_type`).
6. No hallucinations: never assert unprovided personal facts (employment, degrees, employers). If needed, use neutral phrasing or request clarification through structured errors.
7. Validation: ensure all counts are integers >= 0, titles and unlock statements are unique, and no extra fields appear.

## User Prompt Template (runtime prompt builder)

Provide the model a minimal, structured instruction plus the user profile JSON. Example (programmatically constructed):

SYSTEM: [system prompt guards from above]

USER:

---BEGIN USER PROFILE JSON---
{user_profile_json}
---END USER PROFILE JSON---

INSTRUCTIONS:
1) Based only on the profile above, generate a single JSON object matching the RoadmapResponse schema.
2) Use persona rules: if `icp_type` is `ICP-A` prefer English technical templates; if `ICP-B` prefer Hindi practical templates.
3) Follow urgency compression and counts heuristics from the personalization strategy.
4) Do not include any commentary. Only return the JSON.

## Output Rules (explicit)

- The top-level JSON must be exactly: { "milestones": [ ... ] }
- Each milestone object must have only the fields: `code`, `title`, `salary_tier`, `unlock_statement`, `blur_level`, `scenario_count`, `assessment_count`, `mock_interview_count`.
- Titles: unique, 3-10 words recommended, avoid punctuation that breaks parsers.
- Unlock statements: 8–30 words for English, 8–20 words for Hindi; must be emotionally vivid and tied to input.
- Numeric counts: small integers; apply urgency compression before emitting.

## JSON Enforcement Instructions (parsing & extraction)

1. Wrap the JSON response with an explicit delimiter to help extraction (e.g., start with `<<ROADMAP_JSON>>` then the JSON, then `<<END_ROADMAP_JSON>>`).
2. After model response, parse the delimited section. If parse fails or schema validation fails, retry with a strict follow-up prompt asking only for corrected JSON, including the validation errors.
3. Maximum of 3 retries with exponential backoff. On final failure, return structured error to caller with model output for debugging.

## Hallucination Prevention Strategies

- Use conservative system prompt guards (see System Prompt).
- Provide few-shot examples (1–2) showing correct JSON for both ICP-A and ICP-B.
- Set model sampling to deterministic settings (low temperature / equivalent).
- Post-validate with Pydantic (`RoadmapResponse`) and reject any response that doesn't validate.
- When missing input data (e.g., empty `skills`), use predefined role-safe defaults rather than inventing personal history.

## Milestone Logic (how to assemble milestones)

1. M01–M02 (concrete): baseline skills, quick wins, immediate artifacts. For ICP-A: DSA streaks, simple project; ICP-B: typing, Excel, CV draft.
2. M03 (early validation): public portfolio, short certification, or local credential; first applications.
3. M04 (proof): deployment, internship/freelance contract, interview loop entry.
4. M05–M07 (scaling): negotiation, role transition, retention strategies, and growth milestones.

Implementation notes:
- For each milestone, compute counts from persona baselines then multiply by urgency compression factor.
- Derive `salary_tier` conservatively using `target_role`, `experience_months`, and `location` mapping.

## Unlock Statement Logic (construction rules)

1. Base string = actionable artifact + audience + emotional state. Template: "You will [action/artifact] in [context], and you'll feel [emotion]."
2. Use specific verbs for ICP-A (deploy, implement, debug, present) and simpler verbs for ICP-B (complete, practice, feel confident).
3. Do not reference unprovided facts; use placeholders like "your first project" rather than naming companies.
4. Ensure uniqueness by including different artifacts or audiences across milestones.

## Retry & Error Handling Prompts

On schema validation failure, send a focused follow-up prompt:

"The previous response failed JSON schema validation because: {error_list}. Please return only the corrected JSON object matching the schema, with no explanations."

If the model returns extra fields, instruct: "Remove all fields except the exact schema fields. Return only the JSON."

## Few-shot Examples (for model priming)

- Include one concise example for ICP-A (English) and one for ICP-B (Hindi) demonstrating exact JSON structure, not more than 2–3 milestones (abbreviated), then instruct model to expand to full 7.

## Determinism, Tokens & Safety

- Use deterministic sampling options (temperature=0 or model equivalent) to reduce variability.
- Keep prompt length minimal but include required rules and one-shot examples.
- Do not request or output sensitive PII beyond the provided name; mask or omit if accidentally introduced.

## Testing & Monitoring

- Unit tests: for prompt builder templates, ensure generated prompts include injected profile and rules.
- Integration tests: mock Claude responses (valid and malformed) and assert pipeline handles retries and validation.
- Logging: store raw model outputs and parsed JSON for debugging, with redaction of sensitive fields.

## Versioning & Prompt Management

- Store system and example prompts in `prompts/` directory with semantic versioning (e.g., `system_v1.txt`, `few_shot_icp_a_v1.json`).
- Keep prompt builder modular so you can swap system prompt and few-shot examples without code changes.

---

This blueprint should be used by `src/prompt_builder.py` (next) to construct runtime prompts per request.
