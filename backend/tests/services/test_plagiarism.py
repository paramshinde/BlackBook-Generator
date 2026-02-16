from app.services.plagiarism.similarity_engine import compute_similarity_report


def test_plagiarism_report_shape():
    doc = {
        "sections": [
            {"id": "intro", "content": "hello world " * 30},
            {"id": "scope", "content": "hello world scope " * 15},
        ]
    }
    report = compute_similarity_report(doc)
    assert "originality_percentage" in report
    assert "flagged_sections" in report
