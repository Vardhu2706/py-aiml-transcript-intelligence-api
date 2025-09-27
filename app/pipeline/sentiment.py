from typing import List, Dict, Any, Optional
from transformers import pipeline
from app.pipeline.device import get_device
import spacy

device = 0 if get_device() == "cuda" else -1
MODEL_NAME = "distilbert-base-uncased-finetuned-sst-2-english"

# instantiate once per process
_sentiment = pipeline("sentiment-analysis", model=MODEL_NAME, device=device)

# ensure spaCy model available
try:
    _nlp = spacy.load("en_core_web_sm")
except Exception:
    import spacy
    spacy.cli.download("en_core_web_sm")
    _nlp = spacy.load("en_core_web_sm")


def _score_sentence(sent_text: str) -> Dict[str, Any]:
    out = _sentiment(sent_text[:1000])
    lab = out[0]["label"].lower()
    score = out[0]["score"]
    polarity = score if lab == "positive" else -score
    return {"label": lab, "score": polarity, "raw": out[0], "text": sent_text.strip()}


def analyze_sentiment(text: str, segments: Optional[List[Dict[str, Any]]] = None) -> Dict[str, Any]:
    """
    If `segments` (list of {"speaker","text",...}) provided, returns per-speaker summary.
    Otherwise returns sentence-level scores and an aggregated score.
    """
    if segments:
        by_speaker = {}
        for seg in segments:
            spk = seg.get("speaker", "unknown")
            s = seg.get("text", "") or ""
            doc = _nlp(s)
            sent_scores = []
            for sent in doc.sents:
                t = sent.text.strip()
                if not t:
                    continue
                sent_scores.append(_score_sentence(t))
            if sent_scores:
                by_speaker.setdefault(spk, []).extend(sent_scores)

        speaker_summary = {}
        for spk, reslist in by_speaker.items():
            # weight by sentence length
            total_weight = sum(max(len(r["text"].split()), 1) for r in reslist)
            weighted = sum(r["score"] * max(len(r["text"].split()), 1) for r in reslist)
            avg_score = weighted / total_weight if total_weight > 0 else 0.0
            label = "positive" if avg_score > 0.05 else ("negative" if avg_score < -0.05 else "neutral")
            speaker_summary[spk] = {"score": avg_score, "label": label, "n_sentences": len(reslist)}
        overall = sum(v["score"] for v in speaker_summary.values()) / len(speaker_summary) if speaker_summary else 0.0
        overall_label = "positive" if overall > 0.05 else ("negative" if overall < -0.05 else "neutral")
        return {"label": overall_label, "score": overall, "by_speaker": speaker_summary, "model": MODEL_NAME}

    # fallback: unsplit text into sentences and score
    doc = _nlp(text or "")
    by_sentence = []
    for sent in doc.sents:
        t = sent.text.strip()
        if not t:
            continue
        # skip trivial short fragments
        if len(t.split()) < 3:
            continue
        by_sentence.append(_score_sentence(t))
    if not by_sentence:
        return {"label": "neutral", "score": 0.0, "by_sentence": [], "model": MODEL_NAME}
    # length-weighted average
    total_weight = sum(max(len(s["text"].split()), 1) for s in by_sentence)
    weighted = sum(s["score"] * max(len(s["text"].split()), 1) for s in by_sentence)
    avg = weighted / total_weight if total_weight > 0 else 0.0
    label = "positive" if avg > 0.05 else ("negative" if avg < -0.05 else "neutral")
    return {"label": label, "score": avg, "by_sentence": by_sentence, "model": MODEL_NAME}
