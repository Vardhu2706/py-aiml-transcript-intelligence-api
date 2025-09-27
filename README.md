# Transcript Intelligence API

A backend service that analyzes meeting transcripts and extracts structured insights such as sentiment, action items, objections, topics, and summaries.

## 🚀 Features
- Upload raw transcript text and get structured insights back
- Asynchronous processing with **Celery** and **Redis**
- Data persisted in **Postgres**
- NLP models:
  - Sentiment: `distilbert-base-uncased-finetuned-sst-2-english`
  - Summarization: `sshleifer/distilbart-cnn-12-6`
  - Topics: `all-MiniLM-L6-v2` + KeyBERT
  - Objections: Zero-shot classification
- JSON output with `sentiment`, `action_items`, `objections`, `topics`, and `summary`

---

## 🛠️ Tech Stack
- [FastAPI](https://fastapi.tiangolo.com/) — REST API
- [Celery](https://docs.celeryq.dev/) — async task queue
- [Redis](https://redis.io/) — Celery broker
- [Postgres](https://www.postgresql.org/) — database
- [SQLAlchemy](https://www.sqlalchemy.org/) — ORM
- [Transformers](https://huggingface.co/transformers/) — NLP models
- [Sentence-Transformers](https://www.sbert.net/) — embeddings
- [KeyBERT](https://github.com/MaartenGr/KeyBERT) — keyword extraction
- Docker Compose (infra containers)

---

## ⚡ Quickstart

### 1. Clone & create venv
```bash
git clone <repo-url>
cd transcript_intelligence_api
python -m venv .venv
.\.venv\Scripts\activate
pip install -r requirements.txt
```

### 2. Start infra (Postgres + Redis)
```bash
make start-infra
```

### 3. Run Celery worker (Terminal A)
```powershell
make worker
```

### 4. Run FastAPI (Terminal B)
```powershell
make api
```

### 5. Verify
- API docs → http://localhost:8000/docs  
- Health check → GET http://localhost:8000/health  

---

## 📡 Example

**POST /api/v1/transcripts**

Request:
```json
{
  "text": "John: We will send the proposal by 10/10/2025. Jane: The budget is tight and might be too expensive."
}
```

Response:
```json
{
  "transcript_id": "076eee0a-8ffe-4fe5-8a1b-fcf3afb0765b",
  "insights": {
    "sentiment": {
      "label": "positive",
      "score": 0.9897,
      "model": "distilbert-base-uncased-finetuned-sst-2-english"
    },
    "action_items": [],
    "objections": [
      "budget is tight",
      "too expensive"
    ],
    "topics": ["proposal", "budget", "john", "jane"],
    "summary": "John: We will send the proposal by 10/10/2025. Jane: The budget is tight and might be too expensive."
  }
}
```

---

## 📂 Project Structure

```
├── app/ # FastAPI application
│ ├── api/ # API endpoints (v1/endpoints.py etc.)
│ ├── pipeline/ # NLP pipeline modules (sentiment, topics, etc.)
│ ├── utils/ # helper functions
│ ├── config.py # app settings
│ ├── crud.py # DB access layer
│ ├── db.py # DB session / engine
│ ├── main.py # FastAPI entrypoint
│ ├── models.py # SQLAlchemy models
│ ├── schemas.py # Pydantic schemas
│ └── tasks.py # task submission to Celery
├── docker/ # Docker-related scripts/configs
├── docs/ # project documentation
│ ├── api_contracts.md
│ └── design.md
├── scripts/ # helper/test scripts
│ └── test_model.py
├── tests/ # unit/integration tests
├── worker/ # Celery worker
│ ├── celery_app.py
│ ├── run_worker.sh
│ └── tasks.py
├── .env.example # sample environment variables
├── .gitignore
├── docker-compose.yml # services (postgres, redis, api, worker)
├── Dockerfile # FastAPI service image
├── Makefile # helper commands
├── README.md # project readme
├── requirements.txt # base dependencies
└── requirements-dev.txt # dev dependencies
```

---

## 🧭 Roadmap
- [ ] Add Alembic migrations
- [ ] Improve action-item and objection detection
- [ ] Add monitoring/metrics (Prometheus + Grafana)
- [ ] Deployment configs (Cloud Run / K8s)
- [ ] Optional frontend (charts, transcript highlighting)

---

## ⚠️ Limitations
- Current ML models are off-the-shelf; accuracy varies
- No migrations (tables auto-created)
- No production security hardening yet
