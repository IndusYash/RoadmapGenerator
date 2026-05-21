from typing import List, Optional
import random
import re

from .schemas import InputProfile


def _word_set(s: str) -> set:
    tokens = re.findall(r"\w+", s.lower())
    return set(tokens)


def _is_similar(a: str, b: str, threshold: float = 0.6) -> bool:
    A = _word_set(a)
    B = _word_set(b)
    if not A or not B:
        return False
    overlap = len(A & B) / max(len(A), len(B))
    return overlap >= threshold


def _trim_to_word_limit(s: str, max_words: int) -> str:
    words = s.split()
    if len(words) <= max_words:
        return s
    return " ".join(words[:max_words]) + "..."


EN_TEMPLATES = [
    "You'll {action} and be able to {audience_action} with confidence.",
    "You'll {action} for a recruiter and explain the key choices calmly.",
    "You'll {action} in public and feel confident discussing it in interviews.",
    "You'll {action} that clearly shows your fit for {target} to hiring teams.",
]

HI_TEMPLATES = [
    "आप {action_hi} और इंटरव्यू में आत्मविश्वास से इसके बारे में बात कर पाएंगे।",
    "आप {action_hi} करेंगे, जिससे लोकल नियोक्ता के साथ बातचीत आसान होगी।",
    "आप {action_hi} कर के दिखाएंगे और इससे आपका आत्मविश्वास बढ़ेगा।",
]


def _choose_action(profile: InputProfile, idx: int, lang: str) -> (str, str):
    # Return (action_en, action_hi)
    skill = profile.skills[0] if profile.skills else None
    target = profile.target_role or "your target role"

    if profile.icp_type == "ICP-A":
        actions_en = [
            f"complete a small {skill or 'project'} and push it to GitHub",
            f"deploy a demo and prepare a short architecture walkthrough",
            f"write a clear README and demo that highlights {skill or 'your skills'}",
            f"submit applications and present your project in first-round interviews",
        ]
        actions_hi = [
            f"टाइपिंग और ऑफिस टूल्स में अभ्यास करके 40 शब्द/मिनट पर पहुंचना",
            f"एक छोटा प्रमाणपत्र पूरा करना और इसे रिज्यूमे में जोड़ना",
            f"स्थानीय नियोक्ताओं के लिए आवेदन करके साक्षात्कार अभ्यास करना",
        ]
    else:
        actions_en = [
            f"reach a steady typing and office-tools speed that helps local job applications",
            f"complete a short practical certification and add it to your resume",
            f"practice interviews with local employers and improve your confidence",
        ]
        actions_hi = [
            f"टाइपिंग की गति बढ़ाकर स्थानीय आवेदन के लिए तैयार होना",
            f"एक छोटा प्रमाणपत्र पूरा कर के रिज्यूमे मजबूत करना",
            f"नौकरी के लिए आवेदन करके साक्षात्कार अभ्यास करना",
        ]

    # Choose based on milestone index to vary artifacts
    en = actions_en[min(idx, len(actions_en) - 1)]
    hi = actions_hi[min(idx, len(actions_hi) - 1)]
    return en, hi


def generate_unlock_statement(
    profile: InputProfile,
    idx: int,
    existing_statements: Optional[List[str]] = None,
    language: Optional[str] = None,
    max_attempts: int = 6,
) -> str:
    """Generate a single unlock statement for a milestone index.

    existing_statements: list of other unlocks to avoid repetition.
    language: 'en' or 'hi' (defaults to profile.language)
    """
    if language is None:
        language = profile.language or ("en" if profile.icp_type == "ICP-A" else "hi")
    existing = existing_statements or []

    attempts = 0
    stmt = ""
    while attempts < max_attempts:
        attempts += 1
        if language == "hi":
            action_en, action_hi = _choose_action(profile, idx, language)
            tmpl = random.choice(HI_TEMPLATES)
            action_text = action_hi
            stmt = tmpl.format(action_hi=action_text)
            # Ensure Hindi length
            stmt = _trim_to_word_limit(stmt, 20)
        else:
            action_en, action_hi = _choose_action(profile, idx, language)
            tmpl = random.choice(EN_TEMPLATES)
            audience_action = random.choice([
                "explain it to a recruiter",
                "discuss it confidently in interviews",
                "walk through the architecture for hiring teams",
            ])
            stmt = tmpl.format(action=action_en, audience_action=audience_action, target=profile.target_role)
            stmt = _trim_to_word_limit(stmt, 30)

        # Anti-hallucination: do not include company/unprovided facts
        # naive check: avoid words like 'Google', 'Microsoft', etc.
        forbidden = ["google", "microsoft", "facebook", "amazon", "uber"]
        if any(f in stmt.lower() for f in forbidden):
            continue

        # Anti-repetition: ensure not too similar to existing ones
        similar = False
        for ex in existing:
            if _is_similar(stmt, ex):
                similar = True
                break
        if similar:
            # try again with a different template/audience
            continue

        # Final sanitization: trim whitespace and return
        return stmt.strip()

    # If unable to find a non-repetitive variant, enforce uniqueness deterministically.
    if language == "hi":
        candidate = (stmt or "आप इस चरण में स्पष्ट प्रगति महसूस करेंगे।").strip()
        forced = f"{candidate} (चरण {idx + 1})"
    else:
        candidate = (stmt or "You will feel clear progress at this milestone.").strip()
        forced = f"{candidate} (Milestone {idx + 1})"

    # As a final guard, if still too similar, include target role token.
    if any(_is_similar(forced, ex) for ex in existing):
        role = profile.target_role or "your target role"
        if language == "hi":
            forced = f"{forced} - {role}"
        else:
            forced = f"{forced} - {role}"

    return forced


if __name__ == "__main__":
    from .schemas import InputProfile

    p = InputProfile(
        icp_type="ICP-A",
        name="Aisha",
        current_role="Student",
        target_role="Software Engineer",
        urgency_months=3,
        skills=["python", "backend"],
        language="en",
    )
    s = generate_unlock_statement(p, 1, existing_statements=["You'll complete a small project and push to GitHub and explain it."])
    print(s)
