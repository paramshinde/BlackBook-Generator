from ..extensions import db


class ProjectScreenshot(db.Model):
    __tablename__ = "project_screenshots"

    id = db.Column(db.Integer, primary_key=True)
    project_id = db.Column(db.Integer, db.ForeignKey("projects.id"), nullable=False, index=True)
    file_url = db.Column(db.String(500), nullable=False)
    caption = db.Column(db.String(255), nullable=False, default="")
    figure_no = db.Column(db.String(50), nullable=False, default="")
    display_order = db.Column(db.Integer, nullable=False, default=1)

    project = db.relationship("Project", back_populates="screenshots")
