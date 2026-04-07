import heapq


def dijkstra(graph, start):
    """
    graph: adjacency list where graph[u] = [(v1, w1), (v2, w2), ...]
    start: starting node
    returns: shortest distance from start to all other nodes
    """
    n = len(graph)
    distances = [float('inf')] * n
    distances[start] = 0
    visited = [False] * n
    heap = [(0, start)]  # (distance, node)

    while heap:
        current_distance, u = heapq.heappop(heap)
        if visited[u]:
            continue
        visited[u] = True

        for v, weight in graph[u]:
            if distances[u] + weight < distances[v]:
                distances[v] = distances[u] + weight
                heapq.heappush(heap, (distances[v], v))

    return distances


def floyd_warshall(graph):
    """
    graph: adjacency matrix where graph[i][j] = weight or float('inf') if no edge
    returns: matrix of shortest distances between all pairs of nodes
    """
    n = len(graph)
    dist = [row[:] for row in graph]  # copy the matrix

    for k in range(n):
        for i in range(n):
            for j in range(n):
                if dist[i][k] + dist[k][j] < dist[i][j]:
                    dist[i][j] = dist[i][k] + dist[k][j]

    return dist

def generate_sparse_graph(n):
    """Few edges (~n edges)"""
    graph_list = [[] for _ in range(n)]
    graph_matrix = [[float('inf')] * n for _ in range(n)]

    for i in range(n):
        graph_matrix[i][i] = 0

    for _ in range(n):  # ~n edges
        u = random.randint(0, n - 1)
        v = random.randint(0, n - 1)
        if u != v:
            w = random.randint(1, 10)
            graph_list[u].append((v, w))
            graph_matrix[u][v] = w

    return graph_list, graph_matrix

def generate_dense_graph(n):
    """Many edges (~n^2 edges)"""
    graph_list = [[] for _ in range(n)]
    graph_matrix = [[float('inf')] * n for _ in range(n)]

    for i in range(n):
        graph_matrix[i][i] = 0

    for i in range(n):
        for j in range(n):
            if i != j:
                w = random.randint(1, 10)
                graph_list[i].append((j, w))
                graph_matrix[i][j] = w

    return graph_list, graph_matrix

graph_dijkstra = [
    [(1, 4), (2, 1)],  # edges from node 0
    [(3, 1)],           # edges from node 1
    [(1, 2), (3, 5)],   # edges from node 2
    []                  # edges from node 3
]

inf = float('inf')
graph_floyd_warshall = [
    [0, 4, 1, inf],
    [inf, 0, inf, 1],
    [inf, 2, 0, 5],
    [inf, inf, inf, 0]
]

print("Dijkstra shortest paths from node 0:", dijkstra(graph_dijkstra, 0))

distances_fw = floyd_warshall(graph_floyd_warshall)
print("Floyd–Warshall all-pairs shortest paths:")
for row in distances_fw:
    print(row)