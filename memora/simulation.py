import random
from datetime import datetime, timedelta
from memora.models import Concept
from memora.scheduler import update_memory, update_memory_sm2


def generate_feedback() -> str:
    """
    Distribution: again=10%, hard=20%, good=50%, easy=20%
    """
    feedback_list = ["again", "hard", "good", "easy"]
    random_feedback = random.choices(feedback_list, weights=[10, 20, 50, 20], k=1)[0]
    return random_feedback

def make_concept(concept_id: int, now: datetime) -> Concept:
    return Concept(concept_id, f"Concept_{concept_id}", 0, 1, now, None)

def make_concepts(n:int, now:datetime) -> list[Concept]:
    return [make_concept(i, now) for i in range(1, n + 1)]

def simulate_one_algorithm(scheduler_fn, n_concepts: int, n_days: int, start: datetime) -> dict:
    concepts = make_concepts(n_concepts, start)
    total_reviews = 0

    for day in range(n_days):
        today = start + timedelta(days=day)

        for concept in concepts:
            if concept.due_at <= today:
                feedback = generate_feedback()
                scheduler_fn(concept, feedback, today)
                total_reviews += 1

    #Collect data after the simulation ends
    final_masteries = [c.mastery for c in concepts]
    overdue_count = sum(1 for c in concepts if c.due_at <= start + timedelta(days=n_days))

    return {
        "total_reviews": total_reviews,
        "avg_mastery": sum(final_masteries) / len(final_masteries),
        "min_mastery": min(final_masteries),
        "overdue_count": overdue_count,
    }

def run_simulation(n_concepts: int = 50, n_days: int = 30) -> None:
    """Run V0 vs SM-2 simulation and print comparison table"""
    start = datetime.now()

    v0_status = simulate_one_algorithm(update_memory, n_concepts, n_days, start)
    sm2_status = simulate_one_algorithm(update_memory_sm2, n_concepts, n_days, start)

    print("\n === SM-2 vs V0 Simulation Results ===")
    print(f"Concepts: {n_concepts}, Days: {n_days}\n")

    print(f"{'Metric': <20} {'V0': >10} {'SM-2':>10}")
    print("-" * 42)

    print(f"{'Total Reviews':<20} {v0_status['total_reviews']:>10} {sm2_status['total_reviews']:>10}")
    print(f"{'Avg Mastery':<20} {v0_status['avg_mastery']:>10.2f} {sm2_status['avg_mastery']:>10.2f}")
    print(f"{'Min Mastery':<20} {v0_status['min_mastery']:>10.2f} {sm2_status['min_mastery']:>10.2f}")
    print(f"{'Overdue Count':<20} {v0_status['overdue_count']:>10} {sm2_status['overdue_count']:>10}")

if __name__ == "__main__":
    run_simulation()

