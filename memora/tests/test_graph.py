from memora.models import Concept
from memora.graph import build_graph, add_edge, has_cycle
from datetime import datetime, timedelta

def make_concept(id):
    return Concept(id=id, title=f"C{id}", mastery=0.5, interval_days=1,
                   due_at=datetime.now(), last_review_at=None, ease_factor=2.5)

def test_build_graph_all_keys_present():
    concept_1 = make_concept(1)
    concept_2 = make_concept(2)
    concept_3 = make_concept(3)
    concepts = {1: concept_1, 2: concept_2, 3: concept_3}
    
    graph = build_graph(concepts)
    assert len(graph) == 3
    assert all(v == [] for v in graph.values())

def test_add_edge_success_with_cycle_check():
    concept_1 = make_concept(1)
    concept_2 = make_concept(2)
    concept_3 = make_concept(3)
    concepts = {1: concept_1, 2: concept_2, 3: concept_3}
    
    graph = build_graph(concepts)
    assert add_edge(graph, 1, 2) is True
    assert add_edge(graph, 2, 3) is True
    assert add_edge(graph, 3, 1) is False  

def test_add_edge_rejects_cycle():
    concept_1 = make_concept(1)
    concept_2 = make_concept(2)
    concepts = {1: concept_1, 2: concept_2}
    
    graph = build_graph(concepts)
    add_edge(graph, 1, 2)

    assert add_edge(graph, 2, 1) is False
    assert graph[2] == []

def test_has_cycle_empty_graph():
    concept_1 = make_concept(1)
    concept_2 = make_concept(2)
    concept_3 = make_concept(3)
    concepts = {1: concept_1, 2: concept_2, 3: concept_3}
    
    graph = build_graph(concepts)
    assert has_cycle(graph) is False