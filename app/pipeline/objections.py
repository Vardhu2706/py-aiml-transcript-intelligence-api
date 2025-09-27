from transformers import pipeline
from app.pipeline.device import get_device
import spacy

device = 0 if get_device() == "cuda" else -1
# lighter MNLI model - good balance for zero-shot
MODEL_NAME = "valhalla/distilbart-mnli-12-1"

_classifier = pipeline("zero-shot-classification", model=MODEL_NAME, device=device)

# ensure spaCy sentence splitter
try:
    _nlp = spacy.load("en_core_web_sm")
except Exception:
    import spacy
    spacy.cli.download("en_core_web_sm")
    _nlp = spacy.load("en_core_web_sm")

CANDIDATES = [
    "budget concern",
    "pricing concern",
    "too expensive",
    "timeline concern",
    "not interested",
    "technical limitation",
    "resource constraint",
    "priority conflict"
]

def detect_objections(text: str, threshold: float = 0.7):
    """
    Returns list of objection detections:
    [{"sentence": "...", "labels": [("budget concern", 0.89), ...]}, ...]
    """
    if not text or not text.strip():
        return []
    objections = []
    doc = _nlp(text)
    for sent in doc.sents:
        s = sent.text.strip()
        if len(s.split()) < 4:
            continue
        out = _classifier(s, candidate_labels=CANDIDATES, multi_label=True)
        high = [(lab, sc) for lab, sc in zip(out["labels"], out["scores"]) if sc >= threshold]
        if high:
            objections.append({"sentence": s, "labels": high})
    return objections
