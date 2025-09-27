import re
import spacy

_nlp = spacy.load("en_core_web_sm")

SPEAKER_RE = re.compile(r'^[A-Za-z ]{1,40}:\s*$')  # lines like "John:" or "Meeting Chairman:"

def is_trivial_sentence(sent_text: str):
    s = sent_text.strip()
    if not s:
        return True
    # drop "Name:" fragments
    if SPEAKER_RE.match(s):
        return True
    # drop super short fragments (< 3 tokens or only punctuation)
    tokens = [t for t in s.split() if t.strip()]
    if len(tokens) < 3:
        return True
    return False

def clean_text_for_pipeline(text: str):
    # optionally remove repeated speaker tags and clean garbage punctuation
    lines = text.splitlines()
    cleaned_lines = []
    for ln in lines:
        ln = ln.strip()
        # remove only speaker label prefixes like "John: "
        ln = re.sub(r'^[A-Za-z ]{1,40}:\s*', '', ln)
        if not is_trivial_sentence(ln):
            cleaned_lines.append(ln)
    return " ".join(cleaned_lines)
