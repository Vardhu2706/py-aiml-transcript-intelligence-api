import uuid
from sqlalchemy import Column, String, DateTime, Text, JSON
from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy.sql import func

from app.db import Base

class Transcript(Base):
    __tablename__ = 'transcripts'
    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    raw_text = Column(Text, nullable=True)
    structured = Column(JSON, nullable=True)
    created_at = Column(DateTime(timezone=True), server_default=func.now())
    
class Job(Base):
    __tablename__ = 'jobs'
    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    transcript_id = Column(UUID(as_uuid=True))
    status = Column(String, default='queued')
    created_at = Column(DateTime(timezone=True), server_default=func.now())
    started_at = Column(DateTime(timezone=True), nullable=True)
    completed_at = Column(DateTime(timezone=True), nullable=True)
    error = Column(Text, nullable=True)
    
class Insight(Base):
    __tablename__ = 'insights'
    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    transcript_id = Column(UUID(as_uuid=True))
    insights = Column(JSON, nullable=False)
    model_meta = Column(JSON, nullable=True)
    created_at = Column(DateTime(timezone=True), server_default=func.now())
