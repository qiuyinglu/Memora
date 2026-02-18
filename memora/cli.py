from datetime import datetime, timedelta

from memora.models import Concept
from memora.seed import make_sample_concepts
from memora.scheduler import update_memory
from pathlib import Path
from memora.storage import save_concepts, load_concepts


def main():
    concepts = load_concepts()

    #if there is not concepts
    if not concepts:
        concepts = make_sample_concepts()
        save_concepts(concepts)

    run_menu(concepts)




def format_concept(c):
    return (f"id={c.id} title={c.title} mastery={c.mastery:.2f} "
            f"interval={c.interval_days} due={c.due_at.date()} "
            f"last_review={(c.last_review_at.date() if c.last_review_at else 'Never')}")

def run_menu(concepts):
    while True:

        print("=== Welcome to Memora ^_^ ===")
        print("1. Review due concepts")
        print("2. Add new concept")
        print("3. List all concepts")
        print("4. Quit")

        #User's input
        choice = input("Choose: ").strip()

        if choice == "1":
            do_review(concepts)
        elif choice == "2":
            add_concept(concepts)
        elif choice == "3":
            list_concepts(concepts)
        elif choice == "4":
            break
        else:
            print("Invalid choice.")


def do_review(concepts):
    #Copy the dued concepts into a due list
    due = []
    for c in concepts.values():
        if c.due_at <= datetime.now():
            due.append(c)

    if not due:
        print("No concepts due. \n")
        return

    target = min(due, key=lambda x: x.mastery)

    print("REVIEWING", format_concept(target))
    feedback = input("feedback (again/hard/good/easy) ").strip().lower()
    now = datetime.now()

    update_memory(target, feedback, now)

    print(f"AFTER Concept(id: {target.id}), title: {target.title}, mastery: {target.mastery:.2f}, interval_days: {target.interval_days}, due_at: {target.due_at.date()}, last review at: {target.last_review_at.date() if target.last_review_at else "Never"}")
    save_concepts(concepts)

def add_concept(concepts):
    new_id = max(concepts.keys()) + 1
    title = input("Title: ").strip()
    now = datetime.now()

    new_concept = Concept(new_id, title, 0.0, 1, now + timedelta(days=1), None)
    concepts[new_id] = new_concept
    save_concepts(concepts)

    print(f"Added: '{title}'(id={new_id}), due tomorrow.")

def list_concepts(concepts):
    for c in concepts.values():
        print(format_concept(c))


if __name__ == "__main__":
        main()