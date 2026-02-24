from memora.models import Concept
from memora.graph import build_graph, add_edge, has_cycle, topological_sort, recommended_study_order
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

def test_topological_sort_respects_order():
    """Prerequisite nodes must appear before their dependents."""
    g = {1: [2], 2: [3], 3: []}
    order = topological_sort(g)
    assert order.index(1) < order.index(2)
    assert order.index(2) < order.index(3)

def test_topological_sort_no_edges():
    g = {1: [], 2: [], 3: []}
    order = topological_sort(g)

    assert set(order) == {1, 2, 3}

def test_recommended_study_order_returns_concepts():
    concept_1 = make_concept(1)
    concept_2 = make_concept(2)
    concept_3 = make_concept(3)
    concepts = {1: concept_1, 2: concept_2, 3: concept_3}
    g = {1: [2], 2: [3], 3: []}
    order = recommended_study_order(concepts,g)
    ids = [c.id for c in order]

    assert all(isinstance(c, Concept) for c in order)
    assert ids.index(1) < ids.index(2) < ids.index(3)
