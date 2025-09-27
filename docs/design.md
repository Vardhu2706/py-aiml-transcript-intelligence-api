# Design Document — Transcript Intelligence API

## Overview
The Transcript Intelligence API is a backend service for analyzing meeting transcripts.  
It extracts structured insights such as sentiment, action items, objections, topics, and summaries.  

The system is designed as a distributed architecture with separation of concerns between API handling, asynchronous task processing, data persistence, and NLP pipelines.

---

## Architecture

```mermaid
flowchart TD
    Client[Client (Insomnia / cURL)] -->|HTTP| API[FastAPI Service]
    API -->|Enqueue Task| Redis[(Redis Broker)]
    Worker[Celery Worker] -->|Consume Task| Redis
    Worker -->|Persist Insights| Postgres[(Postgres DB)]
    API -->|Fetch Results| Postgres
```

### Components
- **FastAPI Service**:  
  Handles HTTP requests, enqueues transcripts for processing, retrieves analysis results.

- **Celery Worker**:  
  Executes NLP pipelines asynchronously, stores results in Postgres.

- **Redis**:  
  Acts as message broker for Celery.

- **Postgres**:  
  Stores transcripts, jobs, and analysis insights.

- **NLP Pipelines**:  
  - Sentiment analysis → DistilBERT (HuggingFace)
  - Summarization → DistilBART
  - Topic extraction → MiniLM + KeyBERT
  - Objection detection → Zero-shot classification

---

## Data Flow

1. **Transcript Upload**  
   Client POSTs transcript text to `/api/v1/transcripts`.  
   → API saves transcript record in DB.  
   → API enqueues job to Redis.

2. **Job Processing**  
   Celery worker picks up job from Redis.  
   → Runs NLP pipelines on transcript.  
   → Saves structured insights in Postgres.

3. **Result Retrieval**  
   Client polls `/api/v1/jobs/{job_id}` until job is done.  
   → Then fetches insights via `/api/v1/transcripts/{id}`.

---

## Database Schema

### transcripts
- `id` (UUID, PK)
- `text` (TEXT)
- `created_at` (TIMESTAMP)

### jobs
- `id` (UUID, PK)
- `transcript_id` (FK → transcripts.id)
- `status` (enum: queued, running, done, failed)
- `created_at` (TIMESTAMP)
- `updated_at` (TIMESTAMP)

### insights
- `id` (UUID, PK)
- `transcript_id` (FK → transcripts.id)
- `data` (JSONB) — sentiment, action_items, objections, topics, summary

---

## Non-Goals
- No frontend (PoC backend only)
- No migrations (tables auto-created)
- No authentication/authorization yet

---

## Future Improvements
- Alembic migrations for schema evolution
- Deployment configs (Cloud Run, K8s)
- Monitoring with Prometheus + Grafana
- Frontend UI with charts & transcript highlighting
- Fine-tuned NLP models for action items/objections
