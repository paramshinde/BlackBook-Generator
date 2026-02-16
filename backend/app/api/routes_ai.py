import hashlib
from datetime import datetime

from flask import Blueprint, jsonify, request

from ..extensions import db
from ..models.ai_job import AIJob
from ..models.project import Project
from ..models.section import ProjectSection
from ..services.ai.provider_router import get_ai_provider

bp = Blueprint("ai", __name__, url_prefix="/api/projects")


@bp.post("/<int:project_id>/sections/<section_key>/improve")
def improve_section(project_id: int, section_key: str):
    project = Project.query.get_or_404(project_id)
    payload = request.get_json() or {}
    content = payload.get("content", "")
    target_words = int(payload.get("target_words", 220))

    provider = get_ai_provider()
    result = provider.improve_section(section_key, content, target_words)

    checksum = hashlib.sha256(f"{section_key}:{content}".encode("utf-8")).hexdigest()
    job = AIJob(
        project_id=project.id,
        section_key=section_key,
        provider="gemini",
        model="gemini-2.5-flash-lite",
        status="completed",
        input_hash=checksum,
        output_jsonb=result,
        completed_at=datetime.utcnow(),
    )
    db.session.add(job)

    section = ProjectSection.query.filter_by(project_id=project.id, section_key=section_key).first()
    if not section:
        section = ProjectSection(project_id=project.id, section_key=section_key)
        db.session.add(section)

    section.plain_text = result.get("improved_text", content)
    section.content_jsonb = {"text": result.get("improved_text", content)}
    section.ai_last_enhanced_at = datetime.utcnow()

    db.session.commit()
    return jsonify(result)
