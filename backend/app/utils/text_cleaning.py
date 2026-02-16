import re


def normalize_whitespace(text: str) -> str:
    return re.sub(r"\s+", " ", text).strip()


def to_academic_tone_fallback(text: str) -> str:
    cleaned = text.strip()
    if not cleaned:
        return cleaned
    if not cleaned.endswith("."):
        cleaned += "."
    return f"This section presents {cleaned[0].lower() + cleaned[1:]}"
