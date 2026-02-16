import re
from collections import Counter


def _tokens(text: str) -> list[str]:
    return [t for t in re.findall(r"[a-zA-Z0-9]+", text.lower()) if len(t) > 2]


def compute_similarity_report(document: dict) -> dict:
    sections = document.get("sections", [])
    joined = "\n".join(s.get("content", "") for s in sections)
    tokens = _tokens(joined)
    counts = Counter(tokens)

    repeated = [{"token": token, "count": count} for token, count in counts.items() if count > 10]
    suspicious = []
    for section in sections:
        text = section.get("content", "")
        unique_ratio = len(set(_tokens(text))) / max(1, len(_tokens(text)))
        if unique_ratio < 0.45 and len(text) > 180:
            suspicious.append(
                {
                    "section_id": section.get("id"),
                    "reason": "Low lexical diversity",
                    "score": round((1 - unique_ratio) * 100, 2),
                }
            )

    originality = max(0.0, 100 - min(85, len(repeated) * 1.2 + len(suspicious) * 7))
    return {
        "overall_similarity": round(100 - originality, 2),
        "originality_percentage": round(originality, 2),
        "flagged_sections": suspicious,
        "top_repeated_terms": repeated[:20],
        "rewrite_suggestions": [
            "Add concrete implementation details and dataset specifics.",
            "Replace repeated phrases with section-specific evidence.",
        ],
    }
