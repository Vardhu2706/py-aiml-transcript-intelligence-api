from keybert import KeyBERT
from sentence_transformers import SentenceTransformer

# lightweight embedding model
_EMBED_MODEL_NAME = "all-MiniLM-L6-v2"

_embed_model = SentenceTransformer(_EMBED_MODEL_NAME)
_kw_model = KeyBERT(model=_embed_model)

def extract_topics(text: str, top_n: int = 6):
    """
    Return a list of keyphrases (strings). Uses MMR for diversity.
    """
    if not text or len(text.strip()) < 10:
        return []
    keywords = _kw_model.extract_keywords(
        text,
        keyphrase_ngram_range=(1, 3),
        stop_words="english",
        use_mmr=True,
        diversity=0.6,
        top_n=top_n,
    )
    # keywords is list of (phrase, score)
    return [k for k, _ in keywords]
