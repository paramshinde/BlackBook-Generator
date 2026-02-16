import os
from datetime import datetime

from flask import Blueprint, current_app, jsonify

from ..extensions import db
from ..models.export_job import ExportJob
from ..models.project import Project
from ..services.export.docx_builder import build_docx
from ..services.export.pdf_builder import convert_docx_to_pdf
from ..services.export.zip_builder import build_zip

bp = Blueprint("exports", __name__, url_prefix="/api/projects")


def _create_job(project_id: int, export_type: str) -> ExportJob:
    job = ExportJob(project_id=project_id, export_type=export_type, status="completed", created_at=datetime.utcnow())
    db.session.add(job)
    db.session.commit()
    return job


@bp.post("/<int:project_id>/exports/docx")
def export_docx(project_id: int):
    project = Project.query.get_or_404(project_id)
    job = _create_job(project.id, "docx")

    out_dir = os.path.join(current_app.config["UPLOAD_DIR"], "exports")
    out_file = os.path.join(out_dir, f"project_{project.id}_{job.id}.docx")
    build_docx(project.document_json or {}, {"margins": {}}, out_file)

    job.output_url = out_file
    db.session.commit()
    return jsonify({"job_id": job.id, "status": "completed", "output_url": out_file})


@bp.post("/<int:project_id>/exports/pdf")
def export_pdf(project_id: int):
    project = Project.query.get_or_404(project_id)
    job = _create_job(project.id, "pdf")

    out_dir = os.path.join(current_app.config["UPLOAD_DIR"], "exports")
    docx_file = os.path.join(out_dir, f"project_{project.id}_{job.id}.docx")
    build_docx(project.document_json or {}, {"margins": {}}, docx_file)
    pdf_file = convert_docx_to_pdf(docx_file, out_dir)

    job.output_url = pdf_file
    db.session.commit()
    return jsonify({"job_id": job.id, "status": "completed", "output_url": pdf_file})


@bp.post("/<int:project_id>/exports/zip")
def export_zip(project_id: int):
    project = Project.query.get_or_404(project_id)
    job = _create_job(project.id, "zip")

    out_dir = os.path.join(current_app.config["UPLOAD_DIR"], "exports")
    bundle_dir = os.path.join(out_dir, f"bundle_{project.id}_{job.id}")
    os.makedirs(bundle_dir, exist_ok=True)

    zip_file = os.path.join(out_dir, f"project_{project.id}_{job.id}.zip")
    build_zip(bundle_dir, zip_file, {"project_id": project.id, "title": project.title})

    job.output_url = zip_file
    db.session.commit()
    return jsonify({"job_id": job.id, "status": "completed", "output_url": zip_file})
