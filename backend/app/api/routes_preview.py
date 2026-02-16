from flask import Blueprint, jsonify, request
from marshmallow import ValidationError

from ..models.project import Project
from ..schemas.document_schema import DocumentSchema
from ..services.preview.html_renderer import render_document_html

bp = Blueprint("preview", __name__, url_prefix="/api/projects")
doc_schema = DocumentSchema()


@bp.post("/<int:project_id>/preview/render")
def render_preview(project_id: int):
    Project.query.get_or_404(project_id)
    payload = request.get_json() or {}
    document = payload.get("document", {})
    template_settings = payload.get("templateSettings", {})

    try:
        doc_schema.load(document)
    except ValidationError:
        # tolerate partial docs during typing
        pass

    html = render_document_html(document, template_settings)
    return jsonify({"html": html})
