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
    heap = [(0, start)]

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
    dist = [row[:] for row in graph]

    for k in range(n):
        for i in range(n):
            for j in range(n):
                if dist[i][k] + dist[k][j] < dist[i][j]:
                    dist[i][j] = dist[i][k] + dist[k][j]

    return dist


def generate_sparse_graph(n):
    """
    Sparse graph: guaranteed connected backbone (n-1 edges as a chain),
    then a few extra random edges — total ~n edges.
    """
    graph_list = [[] for _ in range(n)]
    graph_matrix = [[float('inf')] * n for _ in range(n)]
    for i in range(n):
        graph_matrix[i][i] = 0

    # Guarantee connectivity via a simple chain: 0->1->2->...->n-1
    nodes = list(range(n))
    random.shuffle(nodes)
    for i in range(n - 1):
        u, v = nodes[i], nodes[i + 1]
        w = random.randint(1, 10)
        graph_list[u].append((v, w))
        graph_matrix[u][v] = w

    # Add a few extra random edges to reach ~n total edges
    extra = int(n * 0.3)
    added = 0
    attempts = 0
    while added < extra and attempts < n * 10:
        u = random.randint(0, n - 1)
        v = random.randint(0, n - 1)
        if u != v and graph_matrix[u][v] == float('inf'):
            w = random.randint(1, 10)
            graph_list[u].append((v, w))
            graph_matrix[u][v] = w
            added += 1
        attempts += 1

    return graph_list, graph_matrix


def generate_dense_graph(n):
    """
    Dense graph: all possible directed edges (~n^2 edges).
    """
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


def measure_time(func, *args, runs=5):
    """Average execution time over multiple runs for accuracy."""
    total = 0
    for _ in range(runs):
        start = time.perf_counter()
        func(*args)
        total += time.perf_counter() - start
    return total / runs


# Larger sizes make the O(n^3) curve of Floyd-Warshall clearly visible
sizes = [10, 30, 50, 70, 100, 200, 300]

dijkstra_sparse_times = []
dijkstra_dense_times = []
fw_sparse_times = []
fw_dense_times = []

print(f"{'n':>6} | {'D Sparse':>12} | {'D Dense':>12} | {'FW Sparse':>12} | {'FW Dense':>12}")
print("-" * 65)

for n in sizes:
    g_list_s, g_matrix_s = generate_sparse_graph(n)
    g_list_d, g_matrix_d = generate_dense_graph(n)

    # Fewer averaging runs for large n to keep total runtime reasonable
    runs = max(1, 5 - sizes.index(n) // 3)

    ds = measure_time(dijkstra, g_list_s, 0, runs=runs)
    dd = measure_time(dijkstra, g_list_d, 0, runs=runs)
    fs = measure_time(floyd_warshall, g_matrix_s, runs=runs)
    fd = measure_time(floyd_warshall, g_matrix_d, runs=runs)

    dijkstra_sparse_times.append(ds)
    dijkstra_dense_times.append(dd)
    fw_sparse_times.append(fs)
    fw_dense_times.append(fd)

    print(f"{n:>6} | {ds:>12.6f} | {dd:>12.6f} | {fs:>12.6f} | {fd:>12.6f}")

# Two subplots: sparse comparison and dense comparison
fig, (ax1, ax2) = plt.subplots(1, 2, figsize=(14, 6))

ax1.plot(sizes, dijkstra_sparse_times, marker='o', label="Dijkstra")
ax1.plot(sizes, fw_sparse_times, marker='s', label="Floyd-Warshall")
ax1.set_title("Sparse Graph")
ax1.set_xlabel("Number of nodes")
ax1.set_ylabel("Execution time (seconds)")
ax1.legend()
ax1.grid(True)

ax2.plot(sizes, dijkstra_dense_times, marker='o', label="Dijkstra")
ax2.plot(sizes, fw_dense_times, marker='s', label="Floyd-Warshall")
ax2.set_title("Dense Graph")
ax2.set_xlabel("Number of nodes")
ax2.set_ylabel("Execution time (seconds)")
ax2.legend()
ax2.grid(True)

plt.suptitle("Dijkstra vs Floyd-Warshall", fontsize=14)
plt.tight_layout()
plt.show()