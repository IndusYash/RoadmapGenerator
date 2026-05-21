import json
import re
import logging
from typing import Any, Tuple

logger = logging.getLogger(__name__)


DELIM_START = "<<ROADMAP_JSON>>"
DELIM_END = "<<END_ROADMAP_JSON>>"


def _strip_markdown_fences(text: str) -> str:
    # Remove triple-backtick fences and leading language hints like ```json
    fence_pattern = re.compile(r"```(?:json|json\n)?\n?(.*?)```", re.DOTALL | re.IGNORECASE)
    def _repl(m):
        return m.group(1)
    text = fence_pattern.sub(_repl, text)
    # Also remove any single-line code fences
    text = re.sub(r"`([^`]*)`", r"\1", text)
    return text


def _sanitize_control_chars(text: str) -> str:
    # Replace CR with LF and remove other non-printable control chars except tab/newline
    text = text.replace("\r\n", "\n").replace("\r", "\n")
    # remove control chars except \n, \t
    text = re.sub(r"[\x00-\x08\x0B\x0C\x0E-\x1F]", "", text)
    return text


def _extract_delimited(text: str) -> Tuple[str, bool]:
    start = text.find(DELIM_START)
    end = text.find(DELIM_END)
    if start != -1 and end != -1 and end > start:
        content = text[start + len(DELIM_START) : end]
        # Check for extra text outside delimiters
        extra = (text[:start].strip() != "") or (text[end + len(DELIM_END) :].strip() != "")
        return content.strip(), extra
    return "", False


def _find_first_json_object(text: str) -> str:
    # Find the first '{' and attempt to parse a balanced JSON object, taking care of strings
    idx = text.find("{")
    if idx == -1:
        raise ValueError("No JSON object found")

    i = idx
    depth = 0
    in_str = False
    escape = False
    while i < len(text):
        ch = text[i]
        if ch == '"' and not escape:
            in_str = not in_str
        if not in_str:
            if ch == '{':
                depth += 1
            elif ch == '}':
                depth -= 1
                if depth == 0:
                    return text[idx : i + 1]
        if ch == '\\' and not escape:
            escape = True
        else:
            escape = False
        i += 1

    raise ValueError("Unbalanced JSON braces")


def parse_model_response(raw_text: str) -> Tuple[Any, str, bool]:
    """Attempt to extract JSON from model output.

    Returns (parsed_obj, raw_json_string, had_extra_text_outside_delimiters)
    """
    if not isinstance(raw_text, str):
        raise ValueError("raw_text must be a string")

    text = _sanitize_control_chars(raw_text)
    text = _strip_markdown_fences(text)

    # 1) Try explicit delimiters
    content, had_extra = _extract_delimited(text)
    errors = []
    if content:
        try:
            parsed = json.loads(content)
            return parsed, content, had_extra
        except Exception as e:
            errors.append(f"delimited_json_parse_error: {e}")

    # 2) Try whole-text JSON parse
    try:
        parsed = json.loads(text)
        return parsed, text, False
    except Exception as e:
        errors.append(f"whole_text_json_parse_error: {e}")

    # 3) Try to find the first JSON object substring
    try:
        obj_str = _find_first_json_object(text)
        parsed = json.loads(obj_str)
        # Check if there was extra text outside the found object
        before = text[: text.find(obj_str)].strip()
        after = text[text.find(obj_str) + len(obj_str) :].strip()
        had_extra = bool(before or after)
        return parsed, obj_str, had_extra
    except Exception as e:
        errors.append(f"first_object_parse_error: {e}")

    # 4) Try to find first JSON array
    arr_idx = text.find("[")
    if arr_idx != -1:
        # naive approach: find matching bracket
        i = arr_idx
        depth = 0
        in_str = False
        escape = False
        while i < len(text):
            ch = text[i]
            if ch == '"' and not escape:
                in_str = not in_str
            if not in_str:
                if ch == '[':
                    depth += 1
                elif ch == ']':
                    depth -= 1
                    if depth == 0:
                        arr_str = text[arr_idx : i + 1]
                        try:
                            parsed = json.loads(arr_str)
                            before = text[:arr_idx].strip()
                            after = text[i + 1 :].strip()
                            had_extra = bool(before or after)
                            return parsed, arr_str, had_extra
                        except Exception as e:
                            errors.append(f"array_parse_error: {e}")
            if ch == '\\' and not escape:
                escape = True
            else:
                escape = False
            i += 1

    # If all attempts failed, raise with collected errors
    logger.debug("JSON extraction errors: %s", errors)
    raise ValueError("Failed to extract JSON from model response: " + "; ".join(errors))
