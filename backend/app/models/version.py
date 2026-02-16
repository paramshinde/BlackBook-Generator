from datetime import datetime

from ..extensions import db


class ProjectVersion(db.Model):
    __tablename__ = "project_versions"

    id = db.Column(db.Integer, primary_key=True)
    project_id = db.Column(db.Integer, db.ForeignKey("projects.id"), nullable=False, index=True)
    snapshot_jsonb = db.Column(db.JSON, nullable=False)
    created_by = db.Column(db.Integer, db.ForeignKey("users.id"), nullable=False)
    created_at = db.Column(db.DateTime, default=datetime.utcnow, nullable=False)
    note = db.Column(db.String(255), nullable=False, default="Manual snapshot")

    project = db.relationship("Project", back_populates="versions")
