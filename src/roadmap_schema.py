from typing import List
from pydantic import BaseModel, Field, validator, conint, constr


BLUR_MAP = {
    "M01": 0,
    "M02": 0,
    "M03": 1,
    "M04": 2,
    "M05": 3,
    "M06": 3,
    "M07": 3,
}


class Milestone(BaseModel):
    code: constr(pattern=r"^M0[1-7]$")
    title: constr(min_length=1, max_length=200)
    salary_tier: constr(min_length=1, max_length=80)
    unlock_statement: constr(min_length=10, max_length=1000)
    blur_level: conint(ge=0, le=3)
    scenario_count: conint(ge=0)
    assessment_count: conint(ge=0)
    mock_interview_count: conint(ge=0)

    class Config:
        extra = "forbid"


class RoadmapResponse(BaseModel):
    milestones: List[Milestone] = Field(..., min_length=7, max_length=7)

    @validator("milestones")
    def validate_milestones(cls, v: List[Milestone]):
        # Ensure codes are exactly M01..M07 in order
        expected_codes = [f"M0{i}" for i in range(1, 8)]
        codes = [m.code for m in v]
        if codes != expected_codes:
            raise ValueError(f"milestone codes must be exactly {expected_codes} in order; got {codes}")

        # Unique titles
        titles = [m.title.strip().lower() for m in v]
        if len(set(titles)) != len(titles):
            raise ValueError("milestone titles must be unique")

        # Unique unlock statements and non-generic checks
        unlocks = [m.unlock_statement.strip() for m in v]
        if len(set(unlocks)) != len(unlocks):
            raise ValueError("unlock_statement values must be unique across milestones")

        # Blur level mapping
        for m in v:
            expected_blur = BLUR_MAP.get(m.code)
            if expected_blur is None:
                raise ValueError(f"unexpected milestone code: {m.code}")
            if m.blur_level != expected_blur:
                raise ValueError(f"blur_level for {m.code} must be {expected_blur} (got {m.blur_level})")

        return v

    class Config:
        extra = "forbid"
