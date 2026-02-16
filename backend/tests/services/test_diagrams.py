from app.services.diagrams.mermaid_generator import build_mermaid_diagrams


def test_mermaid_generation():
    diagrams = build_mermaid_diagrams("Smart Attendance", {})
    assert len(diagrams) == 4
    assert any(d["diagram_type"] == "ER Diagram" for d in diagrams)
