from datetime import datetime, timedelta
from memora.models import Concept

def update_memory(concept: Concept, feedback: str, now: datetime) -> Concept:

    #1. Update interval days:
    if feedback == "again":
        new_interval_days = 1
        mastery_delta = -0.15

    elif feedback == "hard":
        new_interval_days = max(1, int(round(concept.interval_days * 1.5)))
        mastery_delta = -0.05

    elif feedback == "good":
        new_interval_days = max(1, int(round(concept.interval_days * 2)))
        mastery_delta = +0.10

    elif feedback == "easy":
        new_interval_days = max(1, int(round(concept.interval_days * 4)))
        mastery_delta = +0.20

    else:
        raise ValueError(f"Unknown feedback: {feedback}")

    concept.interval_days = new_interval_days

    #2. Update due_at

    concept.due_at = now + timedelta(days = new_interval_days)

    #3. Update mastery
    concept.mastery = min(1.0, max(0.0, concept.mastery + mastery_delta))

    #4. Update last_review_at
    concept.last_review_at = now

    return concept

def adjust_feedback(feedback: str, self_report: str | None) -> str:
    levels = ["again", "hard", "good", "easy"]
    i = levels.index(feedback)

    if self_report == "too_hard":
        return levels[max(0, i - 1)]
    elif self_report == "too_easy":
        return levels[min(3, i + 1)]
    else:
        return feedback
