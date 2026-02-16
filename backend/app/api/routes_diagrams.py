from flask import Blueprint, jsonify, request

from ..extensions import db
from ..models.diagram import ProjectDiagram
from ..models.project import Project
from ..services.ai.provider_router import get_ai_provider
from ..services.diagrams.mermaid_generator import build_mermaid_diagrams

bp = Blueprint("diagrams", __name__, url_prefix="/api/projects")


@bp.post("/<int:project_id>/diagrams/generate")
def generate_diagrams(project_id: int):
    project = Project.query.get_or_404(project_id)
    payload = request.get_json() or {}
    project_title = payload.get("project_title") or project.title

    provider = get_ai_provider()
    spec = provider.generate_diagram_spec(project_title)
    diagrams = build_mermaid_diagrams(project_title, spec)

    ProjectDiagram.query.filter_by(project_id=project.id).delete()
    for item in diagrams:
        db.session.add(
            ProjectDiagram(
                project_id=project.id,
                diagram_type=item["diagram_type"],
                mermaid_code=item["mermaid_code"],
                version=1,
            )
        )
    db.session.commit()

    return jsonify({"diagrams": diagrams})
