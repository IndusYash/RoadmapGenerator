from typing import Optional
from .schemas import InputProfile


def infer_language(profile: InputProfile) -> str:
    """Return 'en' or 'hi' based on profile.language or icp_type inference."""
    if profile.language in ("en", "hi"):
        return profile.language
    return "en" if profile.icp_type == "ICP-A" else "hi"


def is_hindi_text(s: str) -> bool:
    # crude check: presence of Devanagari characters
    for ch in s:
        if '\u0900' <= ch <= '\u097F':
            return True
    return False
