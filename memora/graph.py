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

def topological_sort(graph: dict[int, list[int]]) -> list[int]:
    WHITE, GRAY, BLACK = 0, 1, 2
    color = {node: WHITE for node in graph.keys()}
    result = []

    def dfs(node):
        color[node] = GRAY
        for neighbor in graph[node]:
            if color[neighbor] == WHITE:
                dfs(neighbor)
        color[node] = BLACK
        result.append(node)

    for node in graph:
        if color[node] == WHITE:
            dfs(node)

    result.reverse()
    return result

def recommended_study_order(
        concepts: dict[int, Concept],
        graph: dict[int, list[int]]
) -> list[Concept]:
    id_list = topological_sort(graph)
    return [concepts[cid] for cid in id_list]

def print_graph(concepts: dict[int, Concept], graph: dict[int, list[int]]) -> None:
    print("=== Knowledge Graph ===")
    total_edges = sum(len(v) for v in graph.values())
    for node_id, neighbors in graph.items():
        neighbor_strs = [f"{concepts[n].title} ({n})" for n in neighbors]
        neighbor_text = ", ".join(neighbor_strs)
        title = concepts[node_id].title
        if neighbors:
            print(f"{title}({node_id}) → {neighbor_text}")
        else:
            print(f"{title}({node_id}) → (no dependents)")

    print(f"Total: {len(concepts)} concepts, {total_edges} edges \n")
