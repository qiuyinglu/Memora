import json
from dataclasses import asdict
from datetime import datetime
from pathlib import Path

from  memora.models import Concept, ReviewEvent

DATA_DIR = Path(__file__).parent / "data"
CONCEPTS_FILE = DATA_DIR / "concepts.json"
REVIEWS_FILE = DATA_DIR / "reviews.jsonl"

def _concept_to_dict(c: Concept) -> dict:
    d = asdict(c)

    d["due_at"] = c.due_at.isoformat()
    d["last_review_at"] = c.last_review_at.isoformat() if c.last_review_at else None

    return d

def save_concepts(concepts: dict[int, Concept], file_path: Path | None=None) -> None:
    if file_path is None:
        file_path = CONCEPTS_FILE
    file_path.parent.mkdir(parents=True, exist_ok=True)

    payload = [_concept_to_dict(c) for c in concepts.values()]
    file_path.write_text(json.dumps(payload, ensure_ascii=False, indent=2), encoding="utf-8")

def append_review_event(event: ReviewEvent) -> None:
    DATA_DIR.mkdir(parents=True, exist_ok=True)
    record = {
        "concept_id": event.concept_id,
        "timestamp": event.timestamp.isoformat(),
        "feedback": event.feedback,
        "time_spent_seconds": event.time_spent_seconds,
        "self_report": event.self_report,
    }

    with REVIEWS_FILE.open("a", encoding="utf-8") as f:
        f.write(json.dumps(record, ensure_ascii=False) + "\n")

def load_concepts(file_path: Path | None = None) -> dict[int, Concept]:
    #Check if the file exist
    if file_path is None:
        file_path = CONCEPTS_FILE

    if not file_path.exists():
        return {}
        
    data = json.loads(file_path.read_text(encoding="utf-8"))

    conceptDict = {}
    for d in data:
        d["due_at"] = datetime.fromisoformat(d["due_at"])
        d["last_review_at"] = datetime.fromisoformat(d["last_review_at"]) if d["last_review_at"] else None
        c = Concept(**d)
        conceptDict[c.id] = c

    return conceptDict

