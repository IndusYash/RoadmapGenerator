# Validation, Testing & Execution Plan

This document captures schema validation rules, edge-case handling strategies, the testing framework and scenarios, retry/error handling logic, and an implementation timeline with work distribution for the Career Roadmap Generator.

## 1. Schema Validation Rules

- Use Pydantic models (`src/schemas.py` and `src/roadmap_schema.py`) as the single source of truth.
- Input validation (pre-call): validate `InputProfile` before building prompts.
  - Required fields: `icp_type` (`ICP-A`|`ICP-B`), `name`, `target_role`, `urgency_months`.
  - Normalization: trim strings, lowercase skills, infer `language`.
- Output validation (post-call): validate parsed JSON against `RoadmapResponse`.
  - Enforce exactly 7 milestones, codes `M01`..`M07` in order, blur-level mapping, unique `title` and `unlock_statement`, counts >= 0.
- Log validation failures with structured diagnostics: which field, expected vs actual, raw model output snippet.

## 2. Edge-case Handling Strategy

- Malformed / non-JSON model output:
  - Extraction: attempt to extract delimited JSON block (`<<ROADMAP_JSON>>...<<END_ROADMAP_JSON>>`).
  - Fallback: attempt to locate the first top-level JSON object in text.
  - Retry: re-prompt up to 3 times with focused instruction to return only valid JSON; include prior validation errors.
  - Final: if still invalid, return 502 with diagnostic info and the last model output (redacted as needed).

- Empty or weak user profiles:
  - If required fields missing: return 400 with structured validation error and suggestions (e.g., "provide target_role").
  - If `skills` empty: use safe defaults based on `target_role` (from `personalization.py`) and note in logs that defaults were used.
  - If `target_role` unrealistic/unrecognized: return 422 with suggested normalized roles; allow a `normalize_only` query param.

- Very short urgency (0-1 months): treat as high-compression path. Flag in output metadata (internal) that milestones were compressed.

- Mixed-language inputs:
  - If `language` conflicts with `icp_type` (e.g., `ICP-A` + `hi`), prefer explicit `language` but include consistency checks in logs.
  - If `name` contains multiple scripts, preserve it but avoid using script-specific assumptions in unlock statements.

- Weak profiles (little info): follow conservative strategy — produce safe, low-risk milestones focused on skill-building and clarification steps.

## 3. Testing Framework & Test Scenarios

- Test stack:
  - `pytest` for unit/integration tests.
  - `httpx` + `pytest-asyncio` for FastAPI integration tests.
  - `respx` or local mocking for `claude_client` responses.

- Unit tests:
  - Validators: ensure `InputProfile` normalization and `RoadmapResponse` validators catch errors.
  - `prompt_builder`: confirm prompts include required guards and injected profile JSON.
  - `personalization` heuristics: counts and salary-tier mapping tests across ICPs and urgency bands.
  - `extractor`: JSON extraction from varied model output formats.

- Integration tests:
  - Happy path ICP-A and ICP-B with mocked valid Claude responses that match expected schema.
  - Malformed JSON responses: ensure retries and final error codes.
  - Extra-field responses from model: ensure they're rejected and retried.
  - Rate-limit and timeout tests: ensure graceful handling and errors.

- Golden tests / contract tests:
  - Fixed seed prompts with deterministic Claude mock to assert stable counts, blur levels, and field presence.

- Test scenarios (examples):
  1. ICP-A, final-year student, urgency=3, skills provided -> expect technical milestones and English unlock statements.
  2. ICP-B, gig worker, urgency=2, no skills -> expect Hindi milestones, conservative `salary_tier`, defaults used for skills.
  3. Malformed response (model returns free text) -> system retries and then returns 502 with diagnostics.
  4. Mixed language: `icp_type=ICP-B` but `language=en` -> output should be English but tone adapted to ICP-B.
  5. Duplicate titles in model output -> Pydantic validator raises; system retries.

## 4. Retry & Error Handling Logic

- Claude call retry policy:
  - Max attempts: 3 (initial + 2 retries).
  - Backoff: exponential backoff (e.g., 0.5s, 1s, 2s) with jitter.
  - Retries triggered on: network errors, 5xx from model API, or malformed JSON requiring regeneration.

- JSON extraction & validation retries:
  - After first parse failure or schema validation failure, send a focused repair prompt with the exact validation errors and ask the model to return only corrected JSON.
  - Keep a running log of attempts and include it in the final diagnostic on failure.

- Error responses to caller:
  - 400: input validation errors (missing required fields, type mismatches).
  - 422: domain validation (unrealistic target_role normalization needed).
  - 502: model or extraction failure after retries (include anonymized model output and validation errors).
  - 500: internal server errors.

## 5. Output Consistency Checks

- Post-validate with `RoadmapResponse`.
- Additional checks:
  - Ensure titles and unlock statements are not near-duplicates (use simple similarity checks like token overlap ratio > 0.8).
  - Check counts are within persona-specific safe ranges; if not, clamp to safe bounds and log.
  - Confirm language script (basic check) matches `language` where applicable.

## 6. Multilingual Edge Cases

- Ensure prompt few-shot examples include Hindi examples for `ICP-B` to prime structure and expected lengths.
- For Hindi outputs, check UTF-8 handling and ensure unlocking statements length rules use word counts appropriate for Hindi.
- If user provides mixed-language skills, normalize skill tokens but keep language-specific phrasing for unlock statements.

## 7. Observability & Monitoring

- Metrics to capture:
  - request_count, success_count, validation_failures, model_retries, avg_latency, extraction_failures.
- Logs:
  - Store raw model outputs (redacted) for failed cases; include prompt version and attempt count.
- Alerts:
  - High rate of extraction failures or validation failures triggers a PagerDuty alert.

## 8. Development Milestones & Timeline (suggested)

- Week 1: scaffold FastAPI, add Pydantic schemas, prompt builder, and smoke tests.
- Week 2: implement `claude_client` with retry/backoff and `extractor` helpers; add unit tests for validators and extractor.
- Week 3: integrate end-to-end generation with mocked Claude responses; add integration tests and golden tests for ICP-A/B.
- Week 4: implement real Claude integration (using safe sandbox keys), add logging/metrics, and run load tests.
- Week 5: polish error handling, add CI, write README and usage examples, finalize documentation.

## 9. Work Distribution (roles)

- Backend Engineer: implement API, client, extractor, testing harness.
- Prompt Engineer: finalize system prompt, few-shot examples, and tuning.
- QA/Tester: write test cases, run golden tests, validate multilingual outputs.
- DevOps: containerize, set up CI, observability, and rate-limiting.

## 10. Acceptance Criteria

- All unit tests and integration tests pass in CI.
- API returns valid `RoadmapResponse` for sample ICP-A and ICP-B inputs.
- System handles malformed JSON by retrying and returns structured diagnostic on failure.
- Logs capture enough context to debug failed generations without storing sensitive PII.

---

This plan should be used to drive the next implementation sprints and to build robust test coverage for the Career Roadmap Generator.
