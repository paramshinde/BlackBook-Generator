from datetime import datetime

from ..extensions import db


class AIJob(db.Model):
    __tablename__ = "ai_jobs"

    id = db.Column(db.Integer, primary_key=True)
    project_id = db.Column(db.Integer, db.ForeignKey("projects.id"), nullable=False, index=True)
    section_key = db.Column(db.String(100), nullable=False)
    provider = db.Column(db.String(50), nullable=False, default="gemini")
    model = db.Column(db.String(100), nullable=False, default="gemini-2.5-flash-lite")
    status = db.Column(db.String(20), nullable=False, default="completed")
    input_hash = db.Column(db.String(128), nullable=False)
    output_jsonb = db.Column(db.JSON, nullable=False, default=dict)
    created_at = db.Column(db.DateTime, default=datetime.utcnow, nullable=False)
    completed_at = db.Column(db.DateTime, nullable=True)
