from datetime import datetime, timedelta
from memora.models import Concept

QUALITY_MAP: dict[str, int] = {
    "again": 1,
    "hard": 2,
    "good": 4,
    "easy": 5,
}

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

def update_memory_sm2(concept: Concept, feedback: str, now: datetime) -> Concept:
    """Update concept using SM-2 algorithm.
    
    SM-2 core rules:
    - EF' = EF + (0.1 - (5-q) * (0.08 + (5-q) * 0.02)), clamp >= 1.3
    - I(1) = 1, I(2) = 6, I(n) = I(n-1) * EF' for n >= 3
    - If q < 3: reset interval to 1 (start over)
    """

    q = QUALITY_MAP[feedback]

    new_ef = concept.ease_factor + (0.1 - (5-q) * (0.08 + (5-q) * 0.02))
    new_ef = max(1.3, new_ef)

    if q < 3:
        new_interval_days = 1
        if q == 2:
            mastery_delta = -0.05
        if q == 1:
            mastery_delta = -0.15
    else:
        if q == 4:
            mastery_delta = +0.10
        if q == 5:
            mastery_delta = +0.20

        if concept.last_review_at is None:
            new_interval_days = 1
        elif concept.interval_days == 1:
            new_interval_days = 6
        else:
            new_interval_days = int(round(concept.interval_days * new_ef))

    concept.ease_factor = new_ef
    concept.interval_days = new_interval_days

    #2. Update due_at

    concept.due_at = now + timedelta(days = new_interval_days)

    #3. Update mastery
    concept.mastery = min(1.0, max(0.0, concept.mastery + mastery_delta))

    #4. Update last_review_at
    concept.last_review_at = now

    return concept