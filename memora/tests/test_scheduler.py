from memora.models import Concept
from memora.scheduler import update_memory
from datetime import datetime, timedelta
import pytest

def test_again_resets_interval_to_1():
    now = datetime.now()
    concept = Concept(1, "Design-Bid-Build", 0.2, 2, now - timedelta(days=1), None)
    update_memory(concept, "again", now)
    assert concept.interval_days == 1

def test_mastery_clamp_at_zero():
    now = datetime.now()
    concept = Concept(1, "Design-Bid-Build", 0.05, 2, now - timedelta(days=1), None)
    update_memory(concept, "again", now)
    assert concept.mastery == 0.00

def test_invalid_feedback_raises_error():
    now = datetime.now()
    concept = Concept(1, "DBB", 0.4, 2, now - timedelta(days=1), None)
    with pytest.raises(ValueError):
        update_memory(concept, "excellent", now)


def test_again_decreases_mastery():
    now = datetime.now()
    concept = Concept(1, "Beam", 0.50, 2, now - timedelta(days=1), None)
    update_memory(concept, "again", now)
    assert concept.mastery == 0.35

def test_good_doubles_interval():
    now = datetime.now()
    concept = Concept(1, "Bee Engineer", 0.05, 4, now - timedelta(days=1), None)
    update_memory(concept, "good", now)
    assert concept.interval_days == 8

def test_mastery_clamp_at_one():
    now = datetime.now()
    concept = Concept(1, "Sheathing", 0.95, 2, now - timedelta(days=1), None)
    update_memory(concept, "easy", now)
    assert concept.mastery == 1.00
