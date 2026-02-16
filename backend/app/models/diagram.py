from ..extensions import db


class ProjectDiagram(db.Model):
    __tablename__ = "project_diagrams"

    id = db.Column(db.Integer, primary_key=True)
    project_id = db.Column(db.Integer, db.ForeignKey("projects.id"), nullable=False, index=True)
    diagram_type = db.Column(db.String(100), nullable=False)
    mermaid_code = db.Column(db.Text, nullable=False)
    svg_url = db.Column(db.String(500), nullable=True)
    version = db.Column(db.Integer, nullable=False, default=1)

    project = db.relationship("Project", back_populates="diagrams")
