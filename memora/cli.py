from datetime import datetime
from memora.seed import make_sample_concepts
from memora.scheduler import update_memory
from pathlib import Path
from memora.storage import save_concepts, load_concepts


def main():
    concepts = load_concepts()
    if not concepts:
        concepts = make_sample_concepts()
        save_concepts(concepts)


    due = []
    for c in concepts.values():
        if c.due_at <= datetime.now():
            due.append(c)

    if not due:
        print("No concepts due.")
        return

    target = min(due, key=lambda x: x.mastery)

    print("REVIEWING", format_concept(target))
    feedback = input("feedback (again/hard/good/easy) ").strip().lower()
    now = datetime.now()

    update_memory(target, feedback, now)

    print(f"AFTER Concept(id: {target.id}), title: {target.title}, mastery: {target.mastery:.2f}, interval_days: {target.interval_days}, due_at: {target.due_at.date()}, last review at: {target.last_review_at.date() if target.last_review_at else "Never"}")
    save_concepts(concepts)

def format_concept(c):
    return (f"id={c.id} title={c.title} mastery={c.mastery:.2f} "
    f"interval={c.interval_days} due={c.due_at.date()} "
    f"last_review={(c.last_review_at.date() if c.last_review_at else 'Never')}")

if __name__ == "__main__":
    main()