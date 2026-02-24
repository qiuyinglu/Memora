from datetime import datetime, timedelta
import time
from memora.models import Concept, ReviewEvent
from memora.seed import make_sample_concepts
from memora.scheduler import adjust_feedback, update_memory_sm2
from memora.storage import save_concepts, load_concepts, append_review_event, save_graph, load_graph
from memora.analytics import load_reviews, compute_concept_stats, get_struggling_concepts
from memora.graph import build_graph, add_edge, topological_sort, recommended_study_order, print_graph

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
        print("4. View stats")
        print("5. Study order recommendation")
        print("6. Show knowledge graph")
        print("7. Quit")

        #User's input
        choice = input("Choose: ").strip()

        if choice == "1":
            do_review(concepts)
        elif choice == "2":
            add_concept(concepts)
        elif choice == "3":
            list_concepts(concepts)
        elif choice == "4":
            view_stats(concepts)
        elif choice == "5":
            show_study_order(concepts)
        elif choice == "6":
            show_graph(concepts)
        elif choice == "7":
            print("Goodbye!")
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

    start_time = time.time()
    target = min(due, key=lambda x: x.mastery)

    #Review and collect feedbacks
    print("REVIEWING", format_concept(target))

    valid_feedbacks = {"again", "hard", "good", "easy"}
    while True:
        feedback = input("feedback (again/hard/good/easy) ").strip().lower()
        if feedback in valid_feedbacks:
            break
        print("Invalid input. Please enter: again / hard / good / easy")

    valid_reports = {"too_hard", "okay", "too_easy", ""}
    while True:
        raw = input("Self report (too_hard / okay / too_easy), or Enter to skip: ").strip()
        if raw in valid_reports:
            self_report = raw or None
            break
        print("Invalid input. Please enter: too_hard / okay / too_easy, or press Enter")

    end_time = time.time()
    time_spent = int(end_time - start_time)
    now = datetime.now()
    adjusted = adjust_feedback(feedback, self_report)

    update_memory_sm2(target, adjusted, now)

    #Print result
    print(f"AFTER Concept(id: {target.id}), title: {target.title}, mastery: {target.mastery:.2f}, interval_days: {target.interval_days}, due_at: {target.due_at.date()}, last review at: {target.last_review_at.date() if target.last_review_at else "Never"}")

    event = ReviewEvent(target.id, now, feedback, time_spent, self_report)
    append_review_event(event)
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

def view_stats(concepts):
    """Display per-concept statistics and struggling concepts."""

    reviews = load_reviews()
    stats = compute_concept_stats(concepts, reviews)
    struggling = get_struggling_concepts(stats)
    print("=== Concept Stats ===")
    for concept_id, s in stats.items():
        avg_str = f"{s['avg_time_seconds']:.1f}s" if s['avg_time_seconds'] is not None else "N/A"
        print(f"{concept_id}: {s['title']} | Reviews: {s['review_count']} | "
              f"Avg Time: {avg_str} | Mastery: {s['current_mastery']:.2f} | "
              f"Overdue: {'Yes' if s['is_overdue'] else 'No'}")

    print("\n=== Most Struggling Concepts ===")
    for s in struggling:
        print(f"{s['title']} | Mastery: {s['current_mastery']:.2f} | Reviews: {s['review_count']} \n")

def show_study_order(concepts):
    graph = load_graph()

    if not graph:
        graph = build_graph(concepts)
        save_graph(graph)

    order = recommended_study_order(concepts, graph)
    print("=== Recommended Study Order ===")
    for i, c in enumerate(order, 1):
        status = "⚠️ OVERDUE" if c.due_at < datetime.now() else ""
        print(f" {i}. {c.title} (mastery={c.mastery:.2f}) {status} \n")

def show_graph(concepts):
    graph = load_graph()
    if not graph:
        graph = build_graph(concepts)
        save_graph(graph)
    print_graph(concepts, graph)

if __name__ == "__main__":
        main()