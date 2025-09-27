# worker/tasks.py
# small shim so Celery (which tries to import worker.tasks by default)
# finds the task names we registered in worker.celery_app

# Re-export the Celery task object defined in worker.celery_app
from worker.celery_app import analyze_transcript_task  # noqa: F401
