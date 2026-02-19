# Memora
Memora is an adaptive learning system designed to support long-term memory through structured knowledge representation, spaced repetition, and feedback-driven review.

## Features
- Concept-based learning: Concepts are the core units of knowledge, each with a unique ID, title, mastery level, interval days, due date and last review date.
- Review events: Each review of a concept is logged with a timestamp, feedback, and self-assessed difficulty.
- Spaced repetition: The system schedules reviews based on the V0 scheduler, adjusting intervals and difficulty based on user feedback.
- CLI interface: Users can add concepts, review due items, and view the concept list through a command-line interface.
- Data persistence: All data is stored in JSON Lines format for easy access and analysis.

## Data Model

### Concept
| Field Name | Type | Description |
|------------|------|-------------|
| id     | int | Unique identifier for the concept |
| title  | str | Title of the concept |
| mastery | float | Mastery Level (0.0 - 1.0) |
| interval_days | int | Interval in days until next review |
| due_at | datetime | Next review date |
| last_review_at | datetime | Last review date |

### ReviewEvent
| Field Name | Type | Description |
|------------|------|-------------|
| concept_id | int | ID of the reviewed concept |
| timestamp  | datetime | Time of the review |
| feedback   | str | User feedback (again, hard, good, easy) |
| time_spent_seconds | Optional[int] | Time spent on the review in seconds |
| self_report | Optional[str] | User's self-assessment of difficulty (too_hard, okay, too_easy) |

## Scheduling Algorithm
The algorithm maps feedback to a difficulty score and adjusts the concept's properties accordingly.

| Feedback | Mastery Δ | Interval Rule |
|----------|-----------|---------------|
| again    | -0.15     | interval_days = 1|
| hard     | -0.05     | interval_days * 1.5|
| good     | +0.10     | interval_days * 2|
| easy     | +0.20     | interval_days * 4|

### Self-report Adjustment
If the user provides a self-report, the feedback is adjusted one level up or down before scheduling:
- 'too_hard' -> feedback downgraded one level (e.g., good → hard)
- 'too_easy' -> feedback upgraded one level (e.g., hard → good)
- 'okay' or skipped-> no change

## How to Run

**Setup (Windows)**
```ps1
Set-ExecutionPolicy -ExecutionPolicy RemoteSigned -Scope CurrentUser
.\.venv\Scripts\activate.ps1
```

```bash
python main.py
```

## How to Test

```bash
# From the project root:
$env:PYTHONPATH = "."; python -m pytest memora/tests/ -v
```

## Project Structure

```
memora/
├── main.py
├── memora/
│   ├── cli.py
│   ├── models.py
│   ├── scheduler.py
│   ├── storage.py
│   ├── seed.py
│   ├── data/
│   │   ├── concepts.json
│   │   └── reviews.jsonl
│   └── tests/
│       ├── test_scheduler.py
│       └── test_storage.py
```

## Roadmap
- [ ] SM-2 algorithm (EF-based interval scheduling)
- [ ] Knowledge graph with prerequisite relationships
- [ ] Learning analytics (mastery trends, review history)


