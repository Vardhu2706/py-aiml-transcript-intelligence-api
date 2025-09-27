import re

def normalize_whitespace(text: str):
    return re.sub(r"\s+", ' ', text).strip()