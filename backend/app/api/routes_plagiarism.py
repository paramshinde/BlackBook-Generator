from flask import Blueprint, jsonify, request

from ..extensions import db
from ..models.plagiarism_report import PlagiarismReport
from ..models.project import Project
from ..services.plagiarism.similarity_engine import compute_similarity_report

bp = Blueprint("plagiarism", __name__, url_prefix="/api/projects")


@bp.post("/<int:project_id>/plagiarism/check")
def check_plagiarism(project_id: int):
    project = Project.query.get_or_404(project_id)
    payload = request.get_json() or {}
    document = payload.get("document") or project.document_json or {}

    result = compute_similarity_report(document)
    report = PlagiarismReport(
        project_id=project.id,
        overall_score=result["overall_similarity"],
        flagged_jsonb=result.get("flagged_sections", []),
        suggestions_jsonb=result.get("rewrite_suggestions", []),
    )
    db.session.add(report)
    db.session.commit()

    return jsonify(result)
