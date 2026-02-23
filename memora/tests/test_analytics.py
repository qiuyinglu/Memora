from memora.models import Concept
from datetime import datetime, timedelta
from memora.analytics import compute_concept_stats, get_struggling_concepts

def make_concept(id, title, mastery, days_until_due):
    return Concept(
        id=id, title=title, mastery=mastery, interval_days=1,
        due_at=datetime.now() + timedelta(days=days_until_due),
        last_review_at=None, ease_factor=2.5
    )

def test_compute_stats_counts_reviews():
    concept = make_concept(1, "Test Concept", 0.5, 0)
    reviews = [
        {"concept_id": 1, "timestamp": datetime.now() - timedelta(days=3), "feedback": "good"},
        {"concept_id": 1, "timestamp": datetime.now() - timedelta(days=2), "feedback": "hard"},
        {"concept_id": 1, "timestamp": datetime.now(), "feedback": "easy"},
    ]
    stats = compute_concept_stats({1: concept}, reviews)
    assert stats[1]["review_count"] == 3

def test_compute_stats_overdue_detection():
    concept = make_concept(1, "Test Concept", 0.5, -1)  # Due yesterday
    reviews = [{"concept_id": 1, "timestamp": datetime.now() - timedelta(days=3), "feedback": "good"},
        {"concept_id": 1, "timestamp": datetime.now() - timedelta(days=2), "feedback": "hard"},
        {"concept_id": 1, "timestamp": datetime.now(), "feedback": "easy"},
        ]
    stats = compute_concept_stats({1: concept}, reviews)
    assert stats[1]["is_overdue"] == True

def test_struggling_concepts_sorted_by_mastery():
    concepts = {
        1: make_concept(1, "Concept A", 0.8, 0),
        2: make_concept(2, "Concept B", 0.1, 0),
        3: make_concept(3, "Concept C", 0.5, 0),
    }
    reviews = [
        {"concept_id": 1, "timestamp": datetime.now() - timedelta(days=3), "feedback": "good"},
        {"concept_id": 2, "timestamp": datetime.now() - timedelta(days=2), "feedback": "hard"},
        {"concept_id": 3, "timestamp": datetime.now(), "feedback": "easy"},
    ]
    stats = compute_concept_stats(concepts, reviews)
    struggling = get_struggling_concepts(stats, top_n=3)

    assert struggling[0]["current_mastery"] == 0.1
