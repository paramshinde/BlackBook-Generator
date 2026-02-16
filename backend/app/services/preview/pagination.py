import math


def paginate_sections(sections: list[dict], chars_per_page: int = 3200) -> int:
    total_chars = sum(len((s.get("content") or "")) for s in sections)
    return max(1, math.ceil(total_chars / chars_per_page))
