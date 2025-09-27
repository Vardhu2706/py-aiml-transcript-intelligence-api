import spacy
from spacy.matcher import Matcher
from dateparser import parse as parse_date

# load spaCy
try:
    nlp = spacy.load("en_core_web_sm")
except Exception:
    import spacy
    spacy.cli.download("en_core_web_sm")
    nlp = spacy.load("en_core_web_sm")

matcher = Matcher(nlp.vocab)

# pattern: modal/future or keywords that usually indicate an action
modal_verbs = [
    {"LEMMA": {"IN": ["will", "shall", "need", "should", "must", "plan", "schedule", "assign", "follow", "send", "deliver", "email"]}}
]
# imperative: verb at sentence start
imperative = [{"POS": "VERB", "IS_ALPHA": True}]

matcher.add("ACTION_MODAL", [modal_verbs])
matcher.add("ACTION_IMP", [imperative])


def extract_action_items(text: str):
    """
    Return list of dicts:
    {"text": str, "owner": Optional[str], "verb": Optional[str], "object": Optional[str], "due": Optional[str]}
    """
    doc = nlp(text)
    items = []
    for sent in doc.sents:
        s = sent.text.strip()
        if len(s.split()) < 3:
            continue
        sent_doc = nlp(s)
        matches = matcher(sent_doc)
        if not matches:
            continue

        # owner detection - look for PERSON or nsubj
        owner = None
        for ent in sent_doc.ents:
            if ent.label_ in ("PERSON", "ORG"):
                owner = ent.text
                break
        if owner is None:
            for tok in sent_doc:
                if tok.dep_ in ("nsubj", "nsubjpass"):
                    owner = tok.text
                    break

        # verb and object extraction heuristics
        verb = None
        obj = None
        for tok in sent_doc:
            if tok.pos_ == "VERB":
                verb = tok.lemma_
                break
        # collect direct objects / prepositional objects
        obj_tokens = [tok.text for tok in sent_doc if tok.dep_ in ("dobj", "pobj", "attr")]
        if obj_tokens:
            obj = " ".join(obj_tokens)

        # date extraction
        due = None
        for ent in sent_doc.ents:
            if ent.label_ in ("DATE", "TIME"):
                due = ent.text
                try:
                    parsed = parse_date(due)
                    if parsed:
                        due = parsed.date().isoformat()
                except Exception:
                    pass
                break

        items.append({
            "text": s,
            "owner": owner,
            "verb": verb,
            "object": obj if obj else None,
            "due": due
        })

    # post-filter to prune noisy items
    return _post_filter(items)


def _post_filter(items):
    good = []
    modal_keywords = {"will", "shall", "need", "should", "must", "plan", "schedule", "assign", "send", "deliver", "email"}
    for it in items:
        txt = (it.get("text") or "").lower()
        has_modal = any(k in txt for k in modal_keywords)
        has_obj = bool(it.get("object"))
        has_date = bool(it.get("due"))
        verb = (it.get("verb") or "").lower() if it.get("verb") else ""
        # heuristics
        if has_modal or has_date or (has_obj and verb and verb not in {"be", "say", "let", "have"}):
            good.append(it)
    return good