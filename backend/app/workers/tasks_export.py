from datetime import datetime

from ..extensions import db
from ..models.export_job import ExportJob


def mark_export_completed(job_id: int, output_url: str):
    job = ExportJob.query.get(job_id)
    if not job:
        return
    job.status = "completed"
    job.output_url = output_url
    job.completed_at = datetime.utcnow()
    db.session.commit()
