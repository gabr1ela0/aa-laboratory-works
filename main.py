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

graph = [
    [(1, 4), (2, 1)],  # edges from node 0
    [(3, 1)],           # edges from node 1
    [(1, 2), (3, 5)],   # edges from node 2
    []                  # edges from node 3
]

print("Dijkstra shortest paths from node 0:", dijkstra(graph, 0))