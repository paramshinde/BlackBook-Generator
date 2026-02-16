from datetime import datetime

from ..extensions import db


class ProjectSection(db.Model):
    __tablename__ = "project_sections"

    id = db.Column(db.Integer, primary_key=True)
    project_id = db.Column(db.Integer, db.ForeignKey("projects.id"), nullable=False, index=True)
    section_key = db.Column(db.String(100), nullable=False)
    content_jsonb = db.Column(db.JSON, nullable=False, default=dict)
    plain_text = db.Column(db.Text, nullable=False, default="")
    ai_last_enhanced_at = db.Column(db.DateTime, nullable=True)

    project = db.relationship("Project", back_populates="sections")

    __table_args__ = (db.UniqueConstraint("project_id", "section_key", name="uq_project_section"),)
