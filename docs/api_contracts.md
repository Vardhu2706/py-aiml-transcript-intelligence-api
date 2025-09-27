# API Contracts — Transcript Intelligence API

## Base URL
```
http://localhost:8000/api/v1
```

---

## Health Check

### `GET /health`
**Response**
```json
{ "status": "ok" }
```

---

## Create Transcript

### `POST /transcripts`
Upload a new transcript for analysis.

**Request**
```json
{
  "text": "John: We will send the proposal by 10/10/2025. Jane: The budget is tight and might be too expensive."
}
```

**Response**
```json
{
  "transcript_id": "076eee0a-8ffe-4fe5-8a1b-fcf3afb0765b",
  "job_id": "4a81904c-bb59-43c5-9628-609423ee5cb4"
}
```

---

## Check Job Status

### `GET /jobs/{job_id}`

**Response**
```json
{
  "job_id": "4a81904c-bb59-43c5-9628-609423ee5cb4",
  "status": "done"
}
```

Possible values: `queued`, `running`, `done`, `failed`

---

## Get Transcript Insights

### `GET /transcripts/{transcript_id}`

**Response**
```json
{
  "transcript_id": "076eee0a-8ffe-4fe5-8a1b-fcf3afb0765b",
  "insights": {
    "sentiment": {
      "label": "positive",
      "score": 0.98,
      "model": "distilbert-base-uncased-finetuned-sst-2-english"
    },
    "action_items": [
      {
        "owner": "John",
        "verb": "send",
        "object": "proposal",
        "due": "2025-10-10",
        "text": "We will send the proposal by 10/10/2025."
      }
    ],
    "objections": [
      {
        "sentence": "The budget is tight and might be too expensive.",
        "labels": [["objection", 0.92]]
      }
    ],
    "topics": ["proposal", "budget", "customer support"],
    "summary": "John agreed to send the proposal by October 10, 2025, but Jane raised budget concerns."
  }
}
```

---

## Error Responses

### 400 Bad Request
```json
{ "detail": "Invalid request" }
```

### 404 Not Found
```json
{ "detail": "Transcript not found" }
```

### 500 Internal Server Error
```json
{ "detail": "Unexpected error occurred" }
```
