from transformers import pipeline
from app.pipeline.device import get_device
import math

device = 0 if get_device() == "cuda" else -1
MODEL_NAME = "sshleifer/distilbart-cnn-12-6"

# instantiate once
_summarizer = pipeline("summarization", model=MODEL_NAME, device=device)

def _chunk_text(text: str, max_words: int = 400):
    words = text.split()
    if len(words) <= max_words:
        return [text]
    chunks = []
    for i in range(0, len(words), max_words):
        chunks.append(" ".join(words[i:i+max_words]))
    return chunks

def summarize_text(text: str, max_length: int = 150, min_length: int = 30) -> str:
    text = (text or "").strip()
    if not text:
        return ""
    chunks = _chunk_text(text, max_words=400)
    results = []
    for c in chunks:
        out = _summarizer(c, max_length=max_length, min_length=min_length, do_sample=False)
        results.append(out[0]["summary_text"].strip())
    return " ".join(results)
