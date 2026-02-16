from datetime import datetime

from ..extensions import db


class ExportJob(db.Model):
    __tablename__ = "export_jobs"

    id = db.Column(db.Integer, primary_key=True)
    project_id = db.Column(db.Integer, db.ForeignKey("projects.id"), nullable=False, index=True)
    export_type = db.Column(db.String(20), nullable=False)
    status = db.Column(db.String(20), nullable=False, default="queued")
    output_url = db.Column(db.String(500), nullable=True)
    error = db.Column(db.Text, nullable=True)
    created_at = db.Column(db.DateTime, default=datetime.utcnow, nullable=False)
    completed_at = db.Column(db.DateTime, nullable=True)
