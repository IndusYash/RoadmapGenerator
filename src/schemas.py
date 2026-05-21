from typing import List, Optional, Literal
from pydantic import BaseModel, Field, validator, conint, constr


ICPType = Literal["ICP-A", "ICP-B"]
Language = Literal["en", "hi"]


class InputProfile(BaseModel):
    icp_type: ICPType = Field(..., description="Persona bucket: ICP-A or ICP-B")
    name: constr(min_length=1, max_length=120) = Field(...)
    current_role: Optional[constr(max_length=120)] = None
    target_role: constr(min_length=1, max_length=120) = Field(...)
    urgency_months: conint(ge=0, le=60) = Field(..., description="0 means immediate/high urgency")
    skills: List[constr(min_length=1, max_length=80)] = Field(default_factory=list)
    language: Optional[Language] = None
    experience_months: Optional[conint(ge=0, le=600)] = None
    location: Optional[constr(max_length=120)] = None

    @validator("language", pre=True, always=True)
    def set_language_from_icp(cls, v, values):
        if v in ("en", "hi"):
            return v
        icp = values.get("icp_type")
        return "en" if icp == "ICP-A" else "hi"

    @validator("skills", pre=True)
    def normalize_skills(cls, v):
        if v is None:
            return []
        out = []
        seen = set()
        for s in v:
            if not isinstance(s, str):
                continue
            token = s.strip()
            if not token:
                continue
            token_lower = token.lower()
            if token_lower in seen:
                continue
            seen.add(token_lower)
            out.append(token_lower)
        return out

    @validator("target_role", pre=True)
    def normalize_role(cls, v):
        if not isinstance(v, str):
            raise ValueError("target_role must be a string")
        t = v.strip()
        # simple normalizations
        t = t.replace("swe", "Software Engineer").replace("software eng", "Software Engineer")
        return t

    class Config:
        extra = "ignore"
