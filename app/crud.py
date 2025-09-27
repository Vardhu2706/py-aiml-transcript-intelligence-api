from sqlalchemy.orm import Session
from uuid import UUID

from app import models

def create_transcript(db: Session, raw_text: str = None, structured=None):
    t = models.Transcript(raw_text=raw_text, structured=structured)
    db.add(t)
    db.commit()
    db.refresh(t)
    return t

def create_job(db: Session, transcript_id):
    j = models.Job(transcript_id=transcript_id)
    db.add(j)
    db.commit()
    db.refresh(j)
    return j

def update_job_status(db: Session, job_id, status: str, error=None):
    j = db.query(models.Job).filter(models.Job.id==job_id).first()
    if not j:
        return None
    j.status = status
    if error:
        j.error = error
    db.add(j)
    db.commit()
    db.refresh(j)
    return j

def store_insights(db: Session, transcript_id, insights: dict, model_meta: dict | None = None):
    s = models.Insight(transcript_id=transcript_id, insights=insights, model_meta=model_meta)
    db.add(s)
    db.commit()
    db.refresh(s)
    return s

def get_insights(db: Session, transcript_id):
    return db.query(models.Insight).filter(models.Insight.transcript_id==transcript_id).all()