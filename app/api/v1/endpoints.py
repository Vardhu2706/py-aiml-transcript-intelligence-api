from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from uuid import UUID

from app.schemas import UploadRequest, UploadResponse, JobStatus, InsightResponse
from app.db import get_db
from app import crud, models
from worker.celery_app import analyze_transcript_task

router = APIRouter()

@router.post("/transcripts", response_model=UploadResponse)
async def upload_transcript(payload: UploadRequest, db: Session=Depends(get_db)):
    if not payload.text and not payload.segments:
        raise HTTPException(status_code=400, detail="text or segments required")
    structured = [s.model_dump() for s in payload.segments] if payload.segments else None
    t = crud.create_transcript(db, raw_text=payload.text, structured=structured)
    job = crud.create_job(db, t.id)
    
    analyze_transcript_task.delay(str(t.id), str(job.id))
    return UploadResponse(transcript_id=t.id, job_id=job.id)

@router.get("/jobs/{job_id}", response_model=JobStatus)
async def get_job(job_id: UUID, db: Session = Depends(get_db)):
    j = db.query(models.Job).filter(models.Job.id==job_id).first()
    if not j:
        raise HTTPException(status_code=404, detail='job not found')
    return JobStatus(job_id=j.id, status=j.status)

@router.get("/transcripts/{transcript_id}", response_model=InsightResponse)
async def get_transcript(transcript_id: UUID, db: Session = Depends(get_db)):
    insights = crud.get_insights(db, transcript_id)
    if not insights:
        raise HTTPException(status_code=404, detail="insights not found")
    
    latest = insights[-1]
    return InsightResponse(transcript_id=transcript_id, insights=latest.insights)