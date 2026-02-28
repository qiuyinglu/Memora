# Memora
Memora is an adaptive learning system designed to support long-term memory through structured knowledge representation, spaced repetition, and feedback-driven review.

## Features
- Concept-based learning: Concepts are the core units of knowledge, each with a unique ID, title, mastery level, interval days, due date, last review date, and ease factor.
- Review events: Each review of a concept is logged with a timestamp, feedback, and self-assessed difficulty.
- Spaced repetition: The system schedules reviews based on the SM-2 Algorithm, adjusting intervals and difficulty based on user feedback.
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
| ease_factor | float | Ease factor for SM-2 scheduling (default 2.5) |

### ReviewEvent
| Field Name | Type | Description |
|------------|------|-------------|
| concept_id | int | ID of the reviewed concept |
| timestamp  | datetime | Time of the review |
| feedback   | str | User feedback (again, hard, good, easy) |
| time_spent_seconds | Optional[int] | Time spent on the review in seconds |
| self_report | Optional[str] | User's self-assessment of difficulty (too_hard, okay, too_easy) |

## Scheduling Algorithm

### V0 Scheduler (Original)
The algorithm maps feedback to a difficulty score and adjusts the concept's properties accordingly.

| Feedback | Mastery Δ | Interval Rule |
|----------|-----------|---------------|
| again    | -0.15     | interval_days = 1|
| hard     | -0.05     | interval_days * 1.5|
| good     | +0.10     | interval_days * 2|
| easy     | +0.20     | interval_days * 4|

### SM-2 Scheduler (Current)
The SM-2 algorithm uses the ease factor (EF) to adjust intervals based on user performance, based on the SuperMemo-2 algorithm by P.A. Wozniak (1990).

| Feedback | Quality Score |
|----------|---------------|
| again    | 1             |
| hard     | 2             |
| good     | 4             |
| easy     | 5             |

**Ease Factor (EF) update:**

EF' = EF + (0.1 - (5 - q) x (0.08 + (5 - q) x 0.02))

EF is clamped to a minimum of 1.3.

**Interval update:**

| Review Count | Interval Rule |
|--------------|---------------|
| 1            | 1 day         |
| 2            | 6 days        |
| >2           | previous_interval x EF |



### Self-report Adjustment
If the user provides a self-report, the feedback is adjusted one level up or down before scheduling:
- 'too_hard' -> feedback downgraded one level (e.g., good -> hard)
- 'too_easy' -> feedback upgraded one level (e.g., hard -> good)
- 'okay' or skipped-> no change

## Algorithm Design Decisions
### Why SM-2 over V0
The V0 algorithm was a simple, intuitive approach to spaced repetition, but it lacked the adaptability and empirical validation of the SM-2 algorithm. V0 applies fixed multipliers to all concepts regardless of difficulty, which means a concept you struggle with gets the same interval growth as one you find easy. 

The SM-2 developed by P.A. Wozniak in 1990 is based on extensive research[Wozniak, P.A. (1990)](https://super-memory.com/english/ol/sm2.htm) and has been widely adopted in the spaced repetition tools. The adoption of ease factor (EF) allows the system to adapt to the difficulty of each concept, providing a more personalized learning experience.
The feedback mapping is set to be more conservative (e.g., 'hard' maps to a fail-like score of 2 instead of a pass-like score of 3) to align with the SM-2 rule of "if in doubt, repeat"(when q < 3, interval days will set to 1 and the review will be repeated).

### Why Adjacency List + DFS for Knowledge Graph
An adjacency list is chosen over an adjacency matrix because the prerequisite graph is sparse, most concepts have only a few prerequisites, making O(V + E) space more efficient than O(V^2). 
For cycle detection, depth-first search (DFS) with a three-color marking scheme(unvisited, visiting, visited) is a standard method with O(V + E) time complexity.
`add_edge()` uses an add-then-rollback strategy that when adding a new edge, we first add it to the graph and then run cycle detection. If a cycle is detected, we remove the edge and reject the addition. This allows us to maintain the integrity of the DAG while allowing for dynamic updates.


## Knowledge Graph
Concepts are connected by prerequisite relationships, forming a directed acyclic graph (DAG). The edge from A to B means the source concept is a prerequisite for the target concept. When scheduling reviews, the system can prioritize concepts that are prerequisites for others, ensuring a more coherent learning path.

**Cycle Detection**: The system includes a cycle detection implemented using depth-first search (DFS) with O(V + E) complexity to prevent circular dependencies in the knowledge graph.

**Topological Sort**: The system can perform a topological sort of the concepts using depth-first search (DFS) with O(V + E) complexity based on their prerequisite relationships to determine an optimal review order.

**Study Order**: A study order can be generated by performing a topological sort on the knowledge graph, ensuring that all prerequisites are reviewed before their dependent concepts.

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
│   ├── graph.py
│   ├── analytics.py
│   ├── models.py
│   ├── scheduler.py
│   ├── storage.py
│   ├── seed.py
│   ├── simulation.py
│   ├── data/
│   │   ├── concepts.json
│   │   ├── reviews.jsonl
│   │   └── graph.json
│   └── tests/
│       ├── test_scheduler.py
│       ├── test_storage.py
│       ├── test_graph.py
│       └── test_analytics.py
```

## Roadmap
- [x] SM-2 algorithm (EF-based interval scheduling)
- [x] Knowledge graph with prerequisite relationships
- [x] Learning analytics (mastery trends, review history)
- [x] Simulation experiments (V0 vs SM-2)

## Simulation: SM-2 vs V0
```
 === SM-2 vs V0 Simulation Results ===
Concepts: 50, Days: 30

Metric                       V0       SM-2
------------------------------------------
Total Reviews               245        302
Avg Mastery                0.38       0.46
Min Mastery                0.05       0.10
Overdue Count                 9          4

```

SM-2 shows higher average mastery, higher minimum mastery, and fewer overdue reviews compared to V0, demonstrating improved scheduling efficiency and learning outcomes.

## Limitations
- Currently lacks a GUI interface, only CLI is available.
- Simulation uses random feedback, not real user data.
- No multi-device synchronization, all data is stored locally.
- Testing covers core logic but lacks integration tests.
- Currently doesn't support multimedia content (e.g., images, audio) for concepts, which could enhance learning for certain subjects.
- The system does not currently implement a review history visualization, which could help users track their progress over time.
- The DAG structure does not currently support detecting the dependency relationship automatically from the concept title, which could be a useful feature for users who are not sure how to structure their knowledge graph.

