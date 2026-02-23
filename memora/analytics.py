import json
from datetime import datetime
from pathlib import Path
from memora.models import Concept
from collections import defaultdict

def load_reviews(file_path: Path | None = None) -> list[dict]:
    DATA_DIR = Path(__file__).parent / "data"
    REVIEWS_FILE = DATA_DIR / "reviews.jsonl"
    #Check if the file exist
    if file_path is None:
        file_path = REVIEWS_FILE

    if not file_path.exists():
        return []

    reviews = []
    for line in file_path.read_text(encoding="utf-8").splitlines():
        if line.strip():
            row = json.loads(line)
            row["timestamp"] = datetime.fromisoformat(row["timestamp"])
            reviews.append(row)
    return reviews

def compute_concept_stats(
    concepts: dict[int, Concept],
    reviews: list[dict]
) -> dict[int, dict]:
    """Compute per-concept statistics.
    
    Returns dict keyed by concept_id, each value is a dict with:
        - "title": str
        - "review_count": int (total reviews for this concept)
        - "avg_time_seconds": float | None (average time_spent, None if no time data)
        - "current_mastery": float
        - "is_overdue": bool (due_at < now and not yet reviewed since)
    """
    
    # Group reviews by concept_id
    grouped = defaultdict(list)
    for r in reviews:
        grouped[r["concept_id"]].append(r)

    stats = {}
    now = datetime.now()
    for concept_id, concept in concepts.items():
        concept_reviews = grouped.get(concept_id, [])
        review_count = len(concept_reviews)

        time_values = [r.get("time_spent_seconds") for r in concept_reviews if r.get("time_spent_seconds") is not None]
        avg_time_seconds = sum(time_values) / len(time_values) if time_values else None

        is_overdue = concept.due_at < now

        stats[concept_id] = {
            "title": concept.title,
            "review_count": review_count,
            "avg_time_seconds": avg_time_seconds,
            "current_mastery": concept.mastery,
            "is_overdue": is_overdue,
        }

    return stats

def get_struggling_concepts(
        concept_stats: dict[int, dict],
        top_n: int = 5
    ) -> list[dict]:
    

    sorted_items = sorted(concept_stats.values(), key=lambda x: (x["current_mastery"], -x["review_count"]))
    return sorted_items[:top_n]

    


    
