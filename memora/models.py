from dataclasses import dataclass
from datetime import datetime
from typing import Optional

@dataclass
class Concept:
    id: int
    title: str
    mastery: float
    interval_days: int
    due_at: datetime
    last_review_at: Optional[datetime] = None

@dataclass
class ReviewEvent:
    concept_id: int
    timestamp:datetime
    feedback:str