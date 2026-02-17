from datetime import datetime, timedelta
from pathlib import Path
from memora.models import Concept
from memora.storage import save_concepts, load_concepts

def test_save_and_load_roundtrip(tmp_path):
    # 1. create test data.
    now = datetime.now()
    original = {
        1: Concept(1, "Column", 0.3, 8, now, now - timedelta(days=1))
    }

    # 2. save to temp file.
    test_file = tmp_path / "test_concepts.json"
    save_concepts(original, test_file)

    # 3. load it back.
    loaded = load_concepts(test_file)

    # 4. assert

    assert len(loaded) == 1
    assert loaded[1].id == original[1].id
    assert loaded[1].title == original[1].title
    assert loaded[1].mastery == original[1].mastery
    assert loaded[1].interval_days == original[1].interval_days
    assert loaded[1].due_at == original[1].due_at
    assert loaded[1].last_review_at == original[1].last_review_at




