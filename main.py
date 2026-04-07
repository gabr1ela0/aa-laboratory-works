import heapq
import random
import time
import matplotlib.pyplot as plt


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

sizes = [10, 30, 50, 70, 100]

dijkstra_sparse_times = []
dijkstra_dense_times = []
fw_sparse_times = []
fw_dense_times = []

for n in sizes:
    print(f"Testing n = {n}")

    # Sparse graph
    g_list, g_matrix = generate_sparse_graph(n)

    start = time.time()
    dijkstra(g_list, 0)
    dijkstra_sparse_times.append(time.time() - start)

    start = time.time()
    floyd_warshall(g_matrix)
    fw_sparse_times.append(time.time() - start)

    # Dense graph
    g_list, g_matrix = generate_dense_graph(n)

    start = time.time()
    dijkstra(g_list, 0)
    dijkstra_dense_times.append(time.time() - start)

    start = time.time()
    floyd_warshall(g_matrix)
    fw_dense_times.append(time.time() - start)

plt.figure()

plt.plot(sizes, dijkstra_sparse_times, label="Dijkstra Sparse")
plt.plot(sizes, dijkstra_dense_times, label="Dijkstra Dense")
plt.plot(sizes, fw_sparse_times, label="Floyd-Warshall Sparse")
plt.plot(sizes, fw_dense_times, label="Floyd-Warshall Dense")

plt.xlabel("Number of nodes")
plt.ylabel("Execution time (seconds)")
plt.title("Algorithm performance comparison")

plt.legend()
plt.grid()

plt.show()