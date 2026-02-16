def _safe_name(name: str) -> str:
    return name.replace(" ", "_")


def build_mermaid_diagrams(project_title: str, spec: dict) -> list[dict]:
    title = _safe_name(project_title or "Project")

    return [
        {
            "diagram_type": "ER Diagram",
            "mermaid_code": f"erDiagram\n    STUDENT ||--o{{ {title.upper()}_RECORD : creates\n    {title.upper()}_RECORD {{\n      string id\n      string title\n      string status\n    }}",
        },
        {
            "diagram_type": "Class Diagram",
            "mermaid_code": "classDiagram\n    class ProjectService\n    class ExportService\n    ProjectService --> ExportService",
        },
        {
            "diagram_type": "Sequence Diagram",
            "mermaid_code": "sequenceDiagram\n    actor Student\n    Student->>UI: Enter project data\n    UI->>API: Save document JSON\n    API-->>UI: Preview HTML",
        },
        {
            "diagram_type": "Use Case Diagram",
            "mermaid_code": "flowchart LR\n    student([Student]) --> uc1((Generate Black Book))\n    guide([Guide]) --> uc2((Review Output))",
        },
    ]
