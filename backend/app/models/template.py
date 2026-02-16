from ..extensions import db


class Template(db.Model):
    __tablename__ = "templates"

    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(120), nullable=False, unique=True)
    type = db.Column(db.String(20), nullable=False)
    style_jsonb = db.Column(db.JSON, nullable=False, default=dict)
    cover_jsonb = db.Column(db.JSON, nullable=False, default=dict)
    is_system = db.Column(db.Boolean, nullable=False, default=False)
