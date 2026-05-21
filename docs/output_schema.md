# Career Roadmap Generator — Output Roadmap Schema

This document defines the strict JSON response schema returned by the Roadmap Generator.

## Top-level structure

{
  "milestones": [ ... 7 milestone objects ... ]
}

## Milestone object (exact fields, no extras)

- `code` (string) — milestone code: `M01` .. `M07` (required)
- `title` (string) — unique, short title for the milestone (required)
- `salary_tier` (string) — user- and location-calibrated tier (e.g., `entry`, `mid`, `senior`, or localized descriptors) (required)
- `unlock_statement` (string) — vivid, specific motivational statement personalized to the user (required)
- `blur_level` (integer) — fixed mapping: `M01=0`, `M02=0`, `M03=1`, `M04=2`, `M05=3`, `M06=3`, `M07=3` (required)
- `scenario_count` (integer >= 0) — number of real-world scenarios to practice (required)
- `assessment_count` (integer >= 0) — number of assessments or quizzes suggested (required)
- `mock_interview_count` (integer >= 0) — number of mock interviews suggested (required)

No additional fields are allowed. Response must be valid JSON and must include exactly 7 milestones in order.

## Validation rules

- Exactly 7 milestones must be present.
- `code` values must be `M01`..`M07` in order and unique.
- `blur_level` must match the fixed mapping for each code.
- `title` values must be non-empty and unique.
- `unlock_statement` must be non-empty and unique across milestones.
- All counts must be integers >= 0.
- Any unknown or extra fields cause validation failure.

## Error handling

- If the model returns malformed JSON or a schema violation occurs, the service must retry extraction and/or return a structured 500/502 error indicating validation failure with details.
