from ..extensions import db


class ProjectCodeFile(db.Model):
    __tablename__ = "project_code_files"

    id = db.Column(db.Integer, primary_key=True)
    project_id = db.Column(db.Integer, db.ForeignKey("projects.id"), nullable=False, index=True)
    filename = db.Column(db.String(255), nullable=False)
    language = db.Column(db.String(80), nullable=False, default="text")
    content_text = db.Column(db.Text, nullable=False)
    image_url = db.Column(db.String(500), nullable=True)
    line_count = db.Column(db.Integer, nullable=False, default=0)

    project = db.relationship("Project", back_populates="code_files")
