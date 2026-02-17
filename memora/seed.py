from datetime import datetime, timedelta
from memora.models import Concept

def make_sample_concepts() -> dict[int, Concept]:
    now = datetime.now()
    samples = [
        Concept(1, "Design-Bid-Build", 0.2, 2, now - timedelta(days=1), None),
        Concept(2, "Design-Build", 0.5, 3, now - timedelta(days=3), None),
        Concept(3, "Concrete", 0.1, 4, now + timedelta(days=2), None),
        Concept(4, "Steel", 0.1, 2, now + timedelta(days=3), None),
        Concept(5, "Column", 0.3, 3, now + timedelta(days=4), None)
    ]

    result = {}
    for c in samples:
        result[c.id] = c


    return result