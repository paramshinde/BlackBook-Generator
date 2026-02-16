from datetime import datetime

from ..extensions import db
from ..models.ai_job import AIJob
from ..services.ai.provider_router import get_ai_provider


def run_section_improvement(ai_job_id: int, section_title: str, content: str, target_words: int = 200):
    provider = get_ai_provider()
    output = provider.improve_section(section_title, content, target_words)

    record = AIJob.query.get(ai_job_id)
    if not record:
        return output

    record.output_jsonb = output
    record.status = "completed"
    record.completed_at = datetime.utcnow()
    db.session.commit()
    return output
