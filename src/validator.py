import json
from typing import Any, Dict, List, Tuple, Union

from pydantic import ValidationError

from .roadmap_schema import RoadmapResponse, BLUR_MAP


class ValidationResult:
    def __init__(self, valid: bool, errors: List[str] = None, roadmap: RoadmapResponse = None):
        self.valid = valid
        self.errors = errors or []
        self.roadmap = roadmap

    def to_dict(self) -> Dict[str, Any]:
        return {"valid": self.valid, "errors": self.errors}


def validate_roadmap_input(raw: Union[str, Dict[str, Any]]) -> ValidationResult:
    """Validate raw JSON string or dict against the RoadmapResponse schema.

    Returns ValidationResult with errors if invalid.
    """
    data = None
    errors: List[str] = []

    # 1) Parse if string
    if isinstance(raw, str):
        try:
            data = json.loads(raw)
        except Exception as e:
            return ValidationResult(False, errors=[f"json_decode_error: {e}"])
    elif isinstance(raw, dict):
        data = raw
    else:
        return ValidationResult(False, errors=["input_must_be_json_string_or_dict"])

    # 2) Basic structural checks
    if "milestones" not in data:
        return ValidationResult(False, errors=["missing_field: milestones"])
    if not isinstance(data["milestones"], list):
        return ValidationResult(False, errors=["milestones_must_be_list"])
    if len(data["milestones"]) != 7:
        return ValidationResult(False, errors=[f"milestone_count_error: expected 7, got {len(data['milestones'])}"])

    # 3) Pydantic validation
    try:
        roadmap = RoadmapResponse(**data)
    except ValidationError as e:
        # flatten error messages
        for err in e.errors():
            loc = ".".join([str(x) for x in err.get("loc", [])])
            msg = err.get("msg", "")
            errors.append(f"validation_error at {loc}: {msg}")
        return ValidationResult(False, errors=errors)

    # 4) Additional checks: blur levels consistency (already enforced but double-check)
    for m in roadmap.milestones:
        expected = BLUR_MAP.get(m.code)
        if expected is None:
            errors.append(f"unexpected_milestone_code: {m.code}")
        elif m.blur_level != expected:
            errors.append(f"blur_level_mismatch for {m.code}: expected {expected}, got {m.blur_level}")

    if errors:
        return ValidationResult(False, errors=errors)

    return ValidationResult(True, errors=[], roadmap=roadmap)
