from datetime import datetime

from ..extensions import db


class PlagiarismReport(db.Model):
    __tablename__ = "plagiarism_reports"

    id = db.Column(db.Integer, primary_key=True)
    project_id = db.Column(db.Integer, db.ForeignKey("projects.id"), nullable=False, index=True)
    overall_score = db.Column(db.Float, nullable=False)
    flagged_jsonb = db.Column(db.JSON, nullable=False, default=list)
    suggestions_jsonb = db.Column(db.JSON, nullable=False, default=list)
    created_at = db.Column(db.DateTime, default=datetime.utcnow, nullable=False)
