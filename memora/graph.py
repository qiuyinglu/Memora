from memora.models import Concept


def build_graph(concepts: dict[int, Concept]) -> dict[int, list[int]]:
    return {cid: [] for cid in concepts.keys()}

def has_cycle(graph: dict[int, list[int]]) -> bool:
    #Initialize white color for every node.
    WHITE, GRAY, BLACK = 0, 1, 2
    color = {node: WHITE for node in graph.keys()}

    def dfs(node):
        color[node] = GRAY
        for neighbor in graph[node]:
            if color[neighbor] == GRAY: #Has cycle
                return True
            if color[neighbor] == WHITE:
                if dfs(neighbor):
                    return True
        color[node] = BLACK
        return False

    # Run DFS for every unvisited nodes
    for node in graph:
        if color[node] == WHITE:
            if dfs(node):
                return True
    return False

def add_edge(graph: dict[int, list[int]], from_id: int, to_id: int) -> bool:
    graph[from_id].append(to_id)

    if has_cycle(graph):
        graph[from_id].remove(to_id)
        return False
    return True

