from flask import Blueprint, jsonify, request

from ..extensions import db
from ..models.project import Project
from ..models.version import ProjectVersion
from ..models.user import User

bp = Blueprint("versions", __name__, url_prefix="/api/projects")


def _default_user_id() -> int:
    user = User.query.filter_by(email="student@blackbook.local").first()
    return user.id if user else 1


@bp.post("/<int:project_id>/versions")
def create_version(project_id: int):
    project = Project.query.get_or_404(project_id)
    payload = request.get_json() or {}

    version = ProjectVersion(
        project_id=project.id,
        snapshot_jsonb=payload.get("snapshot") or project.document_json,
        created_by=_default_user_id(),
        note=payload.get("note", "Manual snapshot"),
    )
    db.session.add(version)
    db.session.commit()

    return jsonify({"version_id": version.id, "created_at": version.created_at.isoformat()})


@bp.get("/<int:project_id>/versions")
def list_versions(project_id: int):
    Project.query.get_or_404(project_id)
    versions = ProjectVersion.query.filter_by(project_id=project_id).order_by(ProjectVersion.created_at.desc()).all()
    return jsonify(
        {
            "items": [
                {"id": v.id, "note": v.note, "created_at": v.created_at.isoformat()}
                for v in versions
            ]
        }
    )


@bp.post("/<int:project_id>/versions/<int:version_id>/restore")
def restore_version(project_id: int, version_id: int):
    project = Project.query.get_or_404(project_id)
    version = ProjectVersion.query.filter_by(project_id=project.id, id=version_id).first_or_404()
    project.document_json = version.snapshot_jsonb
    db.session.commit()
    return jsonify({"status": "restored", "version_id": version.id})
