# System Architecture — Career Roadmap Generator

This document describes the backend workflow, module separation, API flow, and implementation notes for a production-style Career Roadmap Generator microservice.

## High-level workflow

Input JSON
 ↓
Validation (Pydantic `InputProfile`)
 ↓
Prompt Builder (`prompt_builder.py`) — assemble system + user prompt + few-shot
 ↓
Claude API client (`claude_client.py`) with retries, timeout
 ↓
JSON Extraction / Parser (`extractor.py`) — extract delimited JSON block
 ↓
Schema Validation (Pydantic `RoadmapResponse`)
 ↓
Post-processing (counts rounding, salary-tier finalization)
 ↓
Final Output (HTTP response)

## Recommended folder layout

- `src/`
  - `main.py` — FastAPI app and routes
  - `schemas.py` — input Pydantic models (already present)
  - `roadmap_schema.py` — output Pydantic models (already present)
  - `prompt_builder.py` — build system+user prompt programmatically
  - `claude_client.py` — HTTP client wrapper with retries/backoff
  - `extractor.py` — robust JSON extraction helpers
  - `personalization.py` — rules & heuristics (from `docs/personalization_strategy.md`)
  - `utils.py` — logging, metrics helpers
  - `tests/` — unit and integration tests

## Module responsibilities

- `main.py` (API layer)
  - Validate incoming request using `InputProfile`.
  - Call `generate_roadmap()` service function.
  - Return `RoadmapResponse` or structured error JSON.
- `prompt_builder.py`
  - Build system prompt from `docs/prompt_engineering_blueprint.md`.
  - Inject user profile JSON, few-shot examples, and enforcement rules.
- `claude_client.py`
  - Send prompt to Claude endpoint (HTTP/REST wrapper), with deterministic settings (low temperature equivalent).
  - Implement retry policy (max 3 attempts), exponential backoff, and per-call timeout.
  - Respect rate limits and surface soft errors for retry logic.
- `extractor.py`
  - Pull delimited JSON (`<<ROADMAP_JSON>>...<<END_ROADMAP_JSON>>`) or fall back to first top-level JSON object.
  - Sanitize model output (strip control chars) before JSON parse attempt.
- `roadmap_schema.py`
  - Validate parsed JSON using strict Pydantic model; reject extra fields.
- `personalization.py`
  - Encapsulate ICP-A/B rules, urgency compression, count heuristics, and salary-tier mapping.

## API endpoints (minimal)

- `POST /v1/roadmap` — generate roadmap
  - Request: `InputProfile` JSON
  - Response: 200 `{ "milestones": [...] }` or 4xx/5xx structured error
  - Query params: `validate_only=true` (optional) to return only validation result
- `GET /health` — readiness/ liveness check

## Error handling & retries

- Input Validation: return 400 with `{ "error": "validation_error", "details": {...} }`.
- Model call failures: retry up to `MAX_RETRIES=3`; on persistent failure return 502 with diagnostics (model output, attempt metadata).
- Malformed JSON: attempt up to 3 extraction + schema-validate retries; log raw outputs and validation errors.
- Auto-fail conditions (see `docs/input_schema.md` + `docs/output_schema.md`) return 422/500 depending on context.

## Operational concerns

- Timeouts: overall request timeout should be bounded (e.g., 15–30s). Claude call timeout shorter (e.g., 10s).
- Concurrency: run API with async FastAPI + Uvicorn/Gunicorn with workers. Use an async HTTP client (`httpx`) in `claude_client.py`.
- Rate limiting & queueing: protect downstream Claude API with a local rate limiter and optional work queue for bursts.
- Logging & observability: structured logs (JSON), capture raw model responses (redact PII), emit metrics: request_count, error_count, validation_failures, avg_latency.
- Secrets: store API keys in `.env` and environment variables (`CLAUDE_API_KEY`, `ENV=prod`, `MAX_RETRIES`).

## Testing strategy

- Unit tests: validators, prompt builder, extractor, personalization heuristics.
- Integration tests: mock `claude_client` responses (valid JSON, malformed, extra fields) and assert pipeline retry and validation behavior.
- Golden tests: sample inputs for ICP-A and ICP-B with expected `RoadmapResponse` structure (not content-exact, but schema-valid and rule-compliant).

## Deployment notes

- Containerize with Docker; include health checks and readiness probes.
- Use CI to run tests and linting; store prompt versions and examples in `prompts/` for reproducibility.
- Consider caching frequent prompt outputs for identical inputs to reduce cost.

## Security & privacy

- Redact or avoid logging sensitive PII beyond `name` where necessary.
- Validate and sanitize all inputs.

---

This architecture document should guide implementation of the `src/` modules and operational setup.
