from datetime import datetime

from ..extensions import db


class Project(db.Model):
    __tablename__ = "projects"

    id = db.Column(db.Integer, primary_key=True)
    owner_id = db.Column(db.Integer, db.ForeignKey("users.id"), nullable=False, index=True)
    title = db.Column(db.String(255), nullable=False)
    guide_name = db.Column(db.String(255), default="")
    tech_stack_json = db.Column(db.JSON, nullable=False, default=list)
    template_id = db.Column(db.Integer, db.ForeignKey("templates.id"), nullable=True)
    status = db.Column(db.String(50), nullable=False, default="draft")
    document_json = db.Column(db.JSON, nullable=False, default=dict)
    created_at = db.Column(db.DateTime, default=datetime.utcnow, nullable=False)
    updated_at = db.Column(db.DateTime, default=datetime.utcnow, onupdate=datetime.utcnow, nullable=False)

    owner = db.relationship("User", back_populates="projects")
    sections = db.relationship("ProjectSection", back_populates="project", cascade="all, delete-orphan")
    diagrams = db.relationship("ProjectDiagram", back_populates="project", cascade="all, delete-orphan")
    code_files = db.relationship("ProjectCodeFile", back_populates="project", cascade="all, delete-orphan")
    screenshots = db.relationship("ProjectScreenshot", back_populates="project", cascade="all, delete-orphan")
    versions = db.relationship("ProjectVersion", back_populates="project", cascade="all, delete-orphan")
    template = db.relationship("Template")
