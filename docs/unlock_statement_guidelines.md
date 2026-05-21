# Unlock Statement Guidelines

This document defines rules and heuristics for producing vivid, realistic, and personalized `unlock_statement` values for each milestone. Follow these rules in the generator module to ensure quality, emotional resonance, and low repetition.

## Goals

- Create short, vivid sentences that enable future-self visualization.
- Personalize using only input profile fields (no invented facts).
- Avoid repetition across milestones by varying audience, setting, artifact, and emotion.
- Respect language and length constraints (English vs Hindi).

## Construction Template

- Core structure: [Action / Artifact] + [Context / Audience] + [Emotional outcome].
- Example: "You'll demo a deployed REST API to a recruiter and feel calm and confident explaining the architecture."

## Components

- Action / Artifact: a concrete deliverable the user can create or an observable behavior (e.g., "deploy a demo", "reach 40 WPM typing", "complete short certification").
- Context / Audience: who witnesses or is affected (recruiter, hiring manager, interviewer, local employer, team lead).
- Emotional outcome: a brief phrase capturing feeling (confident, calm, proud, relieved).

## Language & Length

- English: target 8–30 words. Use clear nouns and active verbs. Avoid nested clauses.
- Hindi: target 8–20 words. Use short sentences and encouraging phrasing.

## Anti-Repetition Rules

- Ensure `unlock_statement` values are unique across the 7 milestones.
- Vary one of these axes between milestones: Artifact, Audience, or Emotion. If two statements share >60% token overlap, consider them duplicates.
- If a generated statement is too similar, replace the Audience or Emotion or shift focus to a different artifact.

## Personalization Constraints

- Use fields: `target_role`, `skills` (first skill preferred), `location`, and `current_role` to ground statements.
- Never reference employers, universities, or achievements not present in the input.
- If `skills` is empty, use neutral phrases like "your first project" or "basic workplace tasks".

## Urgency & Tone

- For compressed/urgent paths, prefer short, high-energy verbs ("complete", "ship", "apply") and emphasis on quick outcomes.
- For relaxed pacing, emphasize steady growth and learning ("build", "improve", "solidify").

## Testing Guidance

- Unit test examples should include English and Hindi outputs, checking length, uniqueness, and absence of hallucinated facts.
- Integration tests should validate that statements change across milestones and reflect `icp_type` and `language`.

## Examples

- ICP-A / English: "You'll demo a GitHub-hosted full-stack app to a recruiter and explain its architecture calmly."
- ICP-B / Hindi: "आप पहले महीने में 40 शब्द/मिनट टाइपिंग की निडरता हासिल करेंगे, जिससे इंटरव्यू में आत्मविश्वास बढ़ेगा।"
