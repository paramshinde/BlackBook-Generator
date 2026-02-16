from flask import Blueprint, jsonify, request
from marshmallow import ValidationError

from ..extensions import db
from ..models.project import Project
from ..models.template import Template
from ..models.user import User
from ..schemas.project_schema import ProjectCreateSchema, ProjectPatchSchema

bp = Blueprint("projects", __name__, url_prefix="/api/projects")
create_schema = ProjectCreateSchema()
patch_schema = ProjectPatchSchema()


def _get_or_create_default_user():
    user = User.query.filter_by(email="student@blackbook.local").first()
    if not user:
        user = User(name="Default Student", email="student@blackbook.local", role="student")
        user.set_password("blackbook123")
        db.session.add(user)
        db.session.commit()
    return user


def _serialize_project(project: Project):
    return {
        "id": project.id,
        "title": project.title,
        "guide_name": project.guide_name,
        "status": project.status,
        "template_id": project.template_id,
        "document": project.document_json,
        "created_at": project.created_at.isoformat(),
        "updated_at": project.updated_at.isoformat(),
    }


@bp.post("")
def create_project():
    payload = request.get_json() or {}
    try:
        data = create_schema.load(payload)
    except ValidationError as err:
        return jsonify({"errors": err.messages}), 400

    user = _get_or_create_default_user()
    template_name = data.get("template", "ieee")
    template = Template.query.filter_by(name=template_name).first()

    project = Project(
        owner_id=user.id,
        title=data["title"],
        guide_name=data.get("guide_name") or "",
        status="draft",
        template_id=template.id if template else None,
        document_json={},
    )
    db.session.add(project)
    db.session.commit()

    return jsonify(_serialize_project(project)), 201


@bp.get("/<int:project_id>")
def get_project(project_id: int):
    project = Project.query.get_or_404(project_id)
    return jsonify(_serialize_project(project))


@bp.patch("/<int:project_id>")
def patch_project(project_id: int):
    project = Project.query.get_or_404(project_id)
    payload = request.get_json() or {}
    try:
        data = patch_schema.load(payload)
    except ValidationError as err:
        return jsonify({"errors": err.messages}), 400

    if "title" in data:
        project.title = data["title"]
    if "guide_name" in data:
        project.guide_name = data["guide_name"]
    if "status" in data:
        project.status = data["status"]
    if "document" in data:
        project.document_json = data["document"]

    db.session.commit()
    return jsonify(_serialize_project(project))


@bp.post("/<int:project_id>/autosave")
def autosave(project_id: int):
    project = Project.query.get_or_404(project_id)
    payload = request.get_json() or {}
    document = payload.get("document", {})
    project.document_json = document
    db.session.commit()
    return jsonify({"status": "saved", "project_id": project.id})
