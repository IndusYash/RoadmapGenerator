# Career Roadmap Generator — Input JSON Schema

This document defines the stable, validated input JSON structure the service expects.

## JSON Example

{
  "icp_type": "ICP-A",
  "name": "Aisha Sharma",
  "current_role": "Final-year Student",
  "target_role": "Software Engineer",
  "urgency_months": 6,
  "skills": ["python", "data-structures"],
  "language": "en",
  "experience_months": 0,
  "location": "Bengaluru"
}

## Field Definitions

- `icp_type` (required)
  - Type: string
  - Accepted values: `ICP-A`, `ICP-B`
  - Description: Primary persona bucket. `ICP-A` => high_wage (English-first, technical). `ICP-B` => low_wage (Hindi-first, practical).

- `name` (required)
  - Type: string
  - Validation: non-empty; max length 120

- `current_role` (optional)
  - Type: string | null
  - Validation: max length 120

- `target_role` (required)
  - Type: string
  - Validation: non-empty; max length 120
  - Notes: If unclear or unrealistic, system will attempt to normalize or request clarification.

- `urgency_months` (required)
  - Type: integer
  - Accepted range: 0..60
  - Semantics: number of months until user wants to hit target; 0 means immediate/very high urgency.

- `skills` (optional)
  - Type: array of strings
  - Validation: each skill non-empty; duplicates removed; max 50 items
  - Behavior: Empty list allowed; system will fall back to default starter skills for `target_role`.

- `language` (optional)
  - Type: string
  - Accepted values: `en`, `hi`
  - Default: inferred from `icp_type` if missing (`ICP-A` -> `en`, `ICP-B` -> `hi`).

- `experience_months` (optional)
  - Type: integer
  - Range: 0..600
  - Notes: helps calibrate milestone difficulty.

- `location` (optional)
  - Type: string
  - Notes: used to localize salary tiers and job-market phrasing.

## Validation Rules Summary

- Required fields: `icp_type`, `name`, `target_role`, `urgency_months`.
- `icp_type` must be `ICP-A` or `ICP-B`.
- `language` must be `en` or `hi` when provided; otherwise inferred.
- `urgency_months` must be integer between 0 and 60.
- `skills` may be empty; duplicates will be removed and items trimmed.
- Any unknown fields are ignored but logged.

## Normalization & Preprocessing

- Trim whitespace and lowercase skill tokens.
- Map common role name synonyms (e.g., `SWE`, `software eng` -> `Software Engineer`).
- If `target_role` is missing or clearly unrealistic, service will return a validation error with suggestions.

## Error Responses (validation)

- 400 Bad Request with JSON: `{ "error": "validation_error", "details": { ... } }` for schema violations.

---

Save this file as `docs/input_schema.md` and use `src/schemas.py` for the Pydantic model.
