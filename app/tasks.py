import time
from uuid import UUID
from typing import Optional

from app.pipeline.sentiment import analyze_sentiment
from app.pipeline.action_item_extractor import extract_action_items
from app.pipeline.objections import detect_objections
from app.pipeline.topics import extract_topics
from app.pipeline.summarizer import summarize_text
from app import crud, models
from app.db import SessionLocal

# Optional: update these strings when you change models
SUMMARIZER_MODEL = "sshleifer/distilbart-cnn-12-6"
SENTIMENT_MODEL = "distilbert-base-uncased-finetuned-sst-2-english"
ACTION_MODEL = "spaCy-en-core-web-sm (rules)"
OBJECTION_MODEL = "facebook/bart-large-mnli (zero-shot)"
TOPICS_MODEL = "all-MiniLM-L6-v2 (KeyBERT)"

def _now():
    return time.time()

def analyze_transcript(transcript_id: str, job_id: str):
    """
    Main pipeline runner (called by Celery task wrapper).
    - Converts ids to UUIDs
    - Loads transcript
    - Runs pipeline components (timed)
    - Persists insights + model_meta
    - Updates job status
    """
    db = SessionLocal()
    start_ts = _now()
    per_component_times = {}
    try:
        # Normalize ids to UUID objects
        t_id = UUID(transcript_id) if not isinstance(transcript_id, UUID) else transcript_id
        j_id = UUID(job_id) if not isinstance(job_id, UUID) else job_id

        # Mark job started
        crud.update_job_status(db, j_id, "processing")

        # Load transcript using ORM by primary key
        transcript = db.get(models.Transcript, t_id)
        if transcript is None:
            raise ValueError(f"Transcript not found: {t_id}")

        # Build text and optionally keep segments for per-speaker analysis
        segments = transcript.structured or None
        if transcript.raw_text:
            text = transcript.raw_text
        else:
            segments = transcript.structured or []
            text = " ".join(seg.get("text", "") for seg in segments)

        # ========== Run components with timing ==========
        t0 = _now()
        # sentiment: pass segments if available so it can compute per-speaker sentiment
        try:
            sentiment = analyze_sentiment(text, segments=segments) if segments else analyze_sentiment(text)
        except TypeError:
            # fallback if analyze_sentiment had no segments param (backwards compatible)
            sentiment = analyze_sentiment(text)
        per_component_times["sentiment"] = _now() - t0

        t0 = _now()
        actions = extract_action_items(text)
        per_component_times["action_items"] = _now() - t0

        t0 = _now()
        objections = detect_objections(text)
        per_component_times["objections"] = _now() - t0

        t0 = _now()
        topics = extract_topics(text)
        per_component_times["topics"] = _now() - t0

        t0 = _now()
        summary = summarize_text(text)
        per_component_times["summarizer"] = _now() - t0

        overall_time = _now() - start_ts

        insights = {
            "sentiment": sentiment,
            "action_items": actions,
            "objections": objections,
            "topics": topics,
            "summary": summary,
        }

        # Build a richer model_meta
        model_meta = {
            "pipeline_version": "phase2-v1",
            "runtimes": per_component_times,
            "total_time_s": overall_time,
            "components": {
                "summarizer": {"model": SUMMARIZER_MODEL},
                "sentiment": {"model": SENTIMENT_MODEL},
                "action_items": {"model": ACTION_MODEL},
                "objections": {"model": OBJECTION_MODEL},
                "topics": {"model": TOPICS_MODEL},
            },
            "timestamp": time.strftime("%Y-%m-%dT%H:%M:%SZ", time.gmtime())
        }

        # Persist insights + model metadata
        crud.store_insights(db, t_id, insights, model_meta=model_meta)

        # Mark job done
        crud.update_job_status(db, j_id, "done")
    except Exception as e:
        # Mark job failed with the error, then re-raise for logs
        try:
            crud.update_job_status(db, job_id, "failed", error=str(e))
        except Exception:
            pass
        raise
    finally:
        db.close()
