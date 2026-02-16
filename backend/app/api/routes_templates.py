from flask import Blueprint, jsonify, request

from ..extensions import db
from ..models.template import Template

bp = Blueprint("templates", __name__, url_prefix="/api/templates")


@bp.get("")
def list_templates():
    templates = Template.query.order_by(Template.name.asc()).all()
    return jsonify(
        {
            "items": [
                {
                    "id": t.id,
                    "name": t.name,
                    "type": t.type,
                    "style": t.style_jsonb,
                    "cover": t.cover_jsonb,
                    "is_system": t.is_system,
                }
                for t in templates
            ]
        }
    )


@bp.post("/custom")
def create_custom_template():
    payload = request.get_json() or {}
    template = Template(
        name=payload.get("name", "Custom Template"),
        type="custom",
        style_jsonb=payload.get("style", {}),
        cover_jsonb=payload.get("cover", {}),
        is_system=False,
    )
    db.session.add(template)
    db.session.commit()
    return jsonify({"id": template.id, "name": template.name}), 201
