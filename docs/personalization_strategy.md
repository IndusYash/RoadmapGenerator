# Personalization Strategy — Career Roadmap Generator

Purpose: define deterministic rules and heuristics the generator uses to adapt roadmaps for ICP-A and ICP-B, language choice, urgency, salary progression, tone, and unlock-statement construction.

## High-level rules

- Language: use `language` input when present; otherwise infer from `icp_type` (`ICP-A` -> `en`, `ICP-B` -> `hi`).
- No invented facts: avoid referencing details not present in input. Use placeholders or ask for clarification when needed.
- Determinism: use templates, clear mapping tables, and numeric scaling factors so outputs are reproducible.

## ICP-A behavior (high_wage, English-first)

- Audience: final-year engineering students aiming for software/product roles.
- Content focus:
  - Technical foundations (DSA, system design), portfolio projects, deployment, GitHub presence, internships, interview loops.
  - Milestones emphasize measurable artifacts: project repo, deployed demo, 2-3 algorithm practice streaks, coding interview score targets.
- Counts and intensity:
  - scenario_count: 2–6 depending on milestone (project milestones have more scenarios).
  - assessment_count: 4–12 across milestones; interviews-focused milestones have higher counts.
  - mock_interview_count: 3–8 for mid/late milestones; early milestones 0–2.
- Unlock-statement style: precise, technical, confidence-forward (example: "You'll demo a deployed REST API handling 5k daily users and explain the architecture to recruiters").

## ICP-B behavior (low_wage, Hindi-first)

- Audience: gig/support workers transitioning to stable salaried roles.
- Content focus:
  - Practical workplace skills (Excel, Google Workspace, basic communication), confidence-building, reliable short-term credentials, local job search tactics.
  - Milestones emphasize quick wins: typing speed, 1–2 certifications, mock interviews framed as conversation practice.
- Counts and intensity:
  - scenario_count: 1–4, focused on real-world tasks (fill forms, respond to clients).
  - assessment_count: 1–6; prioritize short checkpoint quizzes and micro-tasks.
  - mock_interview_count: 0–4; emphasize role-plays and confidence drills.
- Language & tone: Use Hindi-first phrasing when `language=hi`. Keep sentences short, use encouraging language, and avoid heavy technical jargon.
  - Unlock-statement example (Hindi): "आप पहले महीने में 40 शब्द/मिनट टाइपिंग की निडरता हासिल करके स्थानीय ऑफिस जॉब के लिए आत्मविश्वास महसूस करेंगे।"

## Urgency adaptation (compression rules)

- Define `urgency_months` bands: `0-1` (immediate), `2-3` (high), `4-6` (medium), `7+` (low).
- Compression factors (scale effort and counts):
  - immediate (0-1): factor=1.6 (intensive); shorten milestone time horizons and increase counts by ~+50%.
  - high (2-3): factor=1.3; compress sequencing, increase assessments and mocks moderately.
  - medium (4-6): factor=1.0; normal pacing.
  - low (7+): factor=0.7; spread milestones out and lower intensity.
- Implementation: multiply base `scenario_count`, `assessment_count`, `mock_interview_count` by factor (rounding to nearest integer, minimums applied).

## Salary progression & `salary_tier`

- Map `target_role` + `experience_months` + `location` to coarse tiers: `entry`, `junior`, `mid`, `senior`, `stable`.
- Heuristics:
  - If `experience_months` < 12 => `entry` or `junior` depending on role difficulty.
  - For ICP-A targeting software roles, use `entry` -> `junior` progression across M01->M04 and `mid` by M05 if projects + interviews succeed.
  - For ICP-B, use descriptive tiers (`entry`, `stable`) and local phrasing (e.g., "स्थानीय स्थिर वेतन") to avoid misleading salary numbers.
- `salary_tier` should be conservative and framed as an achievable next step rather than a precise salary number.

## Tone differences

- ICP-A: aspirational, precise, metric-driven, English-first. Use active verbs and concrete deliverables (e.g., "deploy", "optimize", "pass on-site interview").
- ICP-B: supportive, stepwise, practical, Hindi-first. Use encouraging pronouns, simpler verbs, and local job-market examples.

## Milestone content mapping

- M01–M02 (blur_level 0): Concrete, immediate tasks (skills baseline, quick wins). For ICP-A: small coding project, DSA streak. For ICP-B: typing, Excel basics, local resume.
- M03 (blur_level 1): Early projects and small interviews/applications; start public portfolio or short certification.
- M04 (blur_level 2): Real-world validation (internship, freelance contract, deployed project, or hiring process entry).
- M05–M07 (blur_level 3): Broader career outcomes, scaling skills, negotiation, role transition and retention strategies.

## Unlock-statement construction rules

- Always tie to an observable artifact or behavior drawn from input (e.g., `target_role`, `skills`, `location`).
- Use sensory/emotional language: mention audience (recruiter, hiring manager), setting (interview, demo), and emotion (confident, calm).
- Avoid generic endings: no "You completed this milestone." Instead: "You'll confidently explain your first backend project to a recruiter without hesitation."
- For ICP-B (Hindi): keep 12–20 words, include a concrete outcome (e.g., typing speed, number of forms filled, certification obtained).

## Counts heuristic (algorithm)

- Base counts by ICP and milestone type (example baseline for medium urgency):
  - Technical (ICP-A): M01( scenarios=2, assessments=2, mocks=0 ), M02(2,3,1), M03(3,4,2), M04(3,3,3), M05(4,4,4), M06(3,3,3), M07(2,2,2)
  - Practical (ICP-B): M01(1,1,0), M02(1,2,0), M03(2,2,1), M04(2,3,1), M05(2,2,2), M06(1,1,1), M07(1,1,1)
- Apply urgency compression factor then enforce minimums (scenario>=0, assessment>=0, mock>=0).

## Anti-hallucination & safety

- Only reference input fields. If prompting base requires a clarification, include a structured question step instead of guessing.
- Do not fabricate employer names, past employers, degrees, or outcomes.
- Use conservative, achievable language for salary tiers and outcomes.

## Examples (short)

- ICP-A (en, urgency=3): M03 unlock: "You'll demo a GitHub-hosted full-stack project and discuss its architecture in interviews."
- ICP-B (hi, urgency=2): M02 unlock: "आप पहले महीने में 40 शब्द/मिनट टाइपिंग की निडरता हासिल करेंगे, जिससे लोकल ऑफिस इंटरव्यू में आत्मविश्वास बढ़ेगा।"

---

This strategy document should be referenced by the prompt builder and roadmap generator to ensure consistent, testable personalization behavior.
