# worker/celery_app.py
from celery import Celery
from app.config import settings

# Create celery app with consistent broker/backend
celery = Celery(
    "worker",
    broker=settings.redis_url,
    backend=settings.redis_url,
    include=["worker.tasks", "app.tasks"],  # optional but helpful
)

# Correctly route the named task to the 'transcripts' queue
celery.conf.task_routes = {
    "worker.tasks.analyze_transcript_tasks": {"queue": "transcripts"}
}

# Optionally set default queue name, though the above route should be enough
celery.conf.task_default_queue = "default"

@celery.task(name="worker.tasks.analyze_transcript_tasks")
def analyze_transcript_task(transcript_id, job_id):
    # import here to avoid circular imports
    from app.tasks import analyze_transcript
    analyze_transcript(transcript_id, job_id)