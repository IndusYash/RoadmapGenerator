from typing import List, Dict, Any
from .schemas import InputProfile
from .roadmap_schema import Milestone, RoadmapResponse, BLUR_MAP
from .unlock_generator import generate_unlock_statement
from .i18n import infer_language


TIERS = ["entry", "junior", "mid", "senior", "stable"]


BASE_COUNTS = {
    "ICP-A": {
        # per milestone baseline for medium urgency
        "scenario": [2, 2, 3, 3, 4, 3, 2],
        "assessment": [2, 3, 4, 3, 4, 3, 2],
        "mock": [0, 1, 2, 3, 4, 3, 2],
    },
    "ICP-B": {
        "scenario": [1, 1, 2, 2, 2, 1, 1],
        "assessment": [1, 2, 2, 3, 2, 1, 1],
        "mock": [0, 0, 1, 1, 2, 1, 1],
    },
}


URGENCY_BAND = [(1, 1.6), (3, 1.3), (6, 1.0), (999, 0.7)]


def _urgency_factor(urgency_months: int) -> float:
    for max_months, factor in URGENCY_BAND:
        if urgency_months <= max_months:
            return factor
    return 1.0


def _derive_base_tier(profile: InputProfile) -> int:
    exp = profile.experience_months or 0
    if exp < 12:
        base = 0
    elif exp < 36:
        base = 1
    else:
        base = 2
    # Slight role difficulty heuristic: technical target -> raise base by 1
    tgt = (profile.target_role or "").lower()
    if any(k in tgt for k in ["engineer", "developer", "software", "data"]):
        base = min(len(TIERS) - 1, base + 0)
    return int(base)


def _tier_for_milestone(base_idx: int, step: int) -> str:
    idx = min(len(TIERS) - 1, base_idx + step)
    return TIERS[idx]


def _choose_title(profile: InputProfile, idx: int) -> str:
    target = profile.target_role or "your target role"
    if profile.icp_type == "ICP-A":
        titles = [
            f"Skill baseline for {target}",
            "Minimum viable project",
            "Public portfolio and first applications",
            "Technical validation (internship / contract)",
            "Interview loop and negotiation",
            "Secure your first salaried role",
            "Stabilize and grow in role",
        ]
    else:
        titles = [
            "Basic workplace skills",
            "Practical short credential",
            "Apply and practice locally",
            "First short-term job / contract",
            "Stabilize income and confidence",
            "Improve at-the-job skills",
            "Long-term role stability",
        ]
    return titles[idx]


def _build_unlock_statement(profile: InputProfile, idx: int) -> str:
    # Use first skill if available, otherwise use target role
    skill = (profile.skills[0] if profile.skills else None)
    target = profile.target_role or "the target role"
    if profile.icp_type == "ICP-A":
        templates = [
            lambda: f"You'll complete a small {skill or 'project'} on GitHub and explain its core flow to recruiters.",
            lambda: f"You'll have a working demo and a polished README that highlights why you're fit for {target}.",
            lambda: f"You'll submit applications and discuss your project architecture in first-round interviews confidently.",
            lambda: f"You'll complete a real-world task (internship or freelance) and describe the trade-offs you made.",
            lambda: f"You'll pass targeted technical interviews and discuss system design decisions without hesitation.",
            lambda: f"You'll receive an offer for an entry/junior {target} role and negotiate terms clearly.",
            lambda: f"You'll be working in a salaried {target} role, applying structured growth plans monthly.",
        ]
    else:
        templates = [
            lambda: f"आप पहले महीने में टाइपिंग और ऑफिस टूल्स में आत्मविश्वास हासिल करेंगे, जिससे लोकल जॉब आवेदन आसान होंगे।",
            lambda: f"आप एक छोटा प्रमाणपत्र पूरा कर लेंगे और इसे रिज्यूमे में जोड़कर स्थानीय नियोक्ताओं को दिखा सकेंगे।",
            lambda: f"आप स्थानीय नियोक्ताओं के लिए आवेदन करके साक्षात्कार अभ्यास के दौरान सहज महसूस करेंगे।",
            lambda: f"आप एक छोटी अवधि का काम या अनुबंध हासिल करेंगे और इसे अपने अनुभव के रूप में प्रस्तुत कर पाएंगे।",
            lambda: f"आप अपनी आय को स्थिर करने के लिए सरल बातचीत और नौकरी-प्रस्ताव पर आत्मविश्वास से चर्चा कर पाएंगे।",
            lambda: f"आप रोज़मर्रा के कार्यों में सुधार कर पाएंगे और काम में बेहतर प्रदर्शन दिखा पाएंगे।",
            lambda: f"आप एक स्थिर वेतनभोगी भूमिका में टिके रहेंगे और बढ़ने की योजना बनाएंगे।",
        ]

    stmt = templates[idx]()
    # Ensure not too long — trim if necessary
    if len(stmt.split()) > 40:
        stmt = ' '.join(stmt.split()[:40]) + '...'
    return stmt


def generate_roadmap(profile: InputProfile) -> RoadmapResponse:
    """Generate a 7-milestone roadmap adapted to the InputProfile.

    Returns a validated RoadmapResponse.
    """
    factor = _urgency_factor(int(profile.urgency_months))
    base_tier_idx = _derive_base_tier(profile)

    persona = profile.icp_type if profile.icp_type in BASE_COUNTS else "ICP-A"
    base = BASE_COUNTS[persona]

    milestones = []

    # step offsets for salary progression
    salary_steps = [0, 0, 1, 1, 2, 2, 3]

    # Calculate target months distributed across urgency_months
    urgency = max(1, int(profile.urgency_months))
    target_months = [max(1, min(urgency, int(round((i + 1) * urgency / 7)))) for i in range(7)]

    # Calculate phases
    phases = [1, 1, 2, 2, 3, 3, 4]

    for i in range(7):
        code = f"M0{i+1}"
        title = _choose_title(profile, i)
        salary_tier = _tier_for_milestone(base_tier_idx, salary_steps[i])

        # counts from baseline, scaled by urgency factor
        scen = max(0, int(round(base["scenario"][i] * factor)))
        assess = max(0, int(round(base["assessment"][i] * factor)))
        mock = max(0, int(round(base["mock"][i] * factor)))

        blur = BLUR_MAP.get(code, 3)

        # generate unlock statement with anti-repetition checks
        lang = infer_language(profile)
        existing = [m.unlock_statement for m in milestones]
        unlock = generate_unlock_statement(profile, i, existing_statements=existing, language=lang)

        # Calculate new timeline fields
        target_month = target_months[i]
        phase = phases[i]
        if lang == "hi":
            expected_completion = f"महीने {target_month} के अंत तक"
        else:
            expected_completion = f"By the end of Month {target_month}"

        prev_month = 0 if i == 0 else target_months[i - 1]
        month_diff = target_month - prev_month
        if month_diff == 0:
            estimated_duration_weeks = 2
        else:
            estimated_duration_weeks = max(1, month_diff * 4)

        m = Milestone(
            code=code,
            title=title,
            phase=phase,
            target_month=target_month,
            expected_completion=expected_completion,
            estimated_duration_weeks=estimated_duration_weeks,
            salary_tier=salary_tier,
            unlock_statement=unlock,
            blur_level=blur,
            scenario_count=scen,
            assessment_count=assess,
            mock_interview_count=mock,
        )
        milestones.append(m)

    roadmap = RoadmapResponse(milestones=milestones)
    return roadmap


if __name__ == "__main__":
    # quick local manual test
    sample = {
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
    p = InputProfile(**sample)
    r = generate_roadmap(p)
    print(r.json(indent=2, ensure_ascii=False))
