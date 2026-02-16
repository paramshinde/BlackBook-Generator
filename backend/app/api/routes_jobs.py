from flask import Blueprint, jsonify

from ..models.export_job import ExportJob

bp = Blueprint("jobs", __name__, url_prefix="/api")


@bp.get("/jobs/<int:job_id>")
def get_job(job_id: int):
    job = ExportJob.query.get_or_404(job_id)
    return jsonify(
        {
            "id": job.id,
            "project_id": job.project_id,
            "status": job.status,
            "export_type": job.export_type,
            "output_url": job.output_url,
            "error": job.error,
        }
    )
