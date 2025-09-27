from typing import List, Optional
from pydantic import BaseModel
from uuid import UUID

class Segment(BaseModel):
    speaker: Optional[str]
    text: str
    start: Optional[float]
    
class UploadRequest(BaseModel):
    text: Optional[str]
    segments: Optional[List[Segment]]
    
class UploadResponse(BaseModel):
    transcript_id: UUID
    job_id: UUID
    
class JobStatus(BaseModel):
    job_id: UUID
    status: str
    
class InsightResponse(BaseModel):
    transcript_id: UUID
    insights: dict