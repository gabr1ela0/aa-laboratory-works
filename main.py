import time
import random
from collections import defaultdict, deque
import matplotlib.pyplot as plt


class Graph:
    def __init__(self, vertices):
        self.V = vertices
        self.graph = defaultdict(list)

    def addEdge(self, u, v):
        self.graph[u].append(v)
        self.graph[v].append(u)

    def DFSUtil(self, v, visited):
        visited.add(v)

        for neighbour in self.graph[v]:
            if neighbour not in visited:
                self.DFSUtil(neighbour, visited)

    def DFS(self, start):
        visited = set()
        self.DFSUtil(start, visited)

    def BFS(self, start):
        visited = set()
        queue = deque()

        visited.add(start)
        queue.append(start)

        while queue:
            node = queue.popleft()

            for neighbour in self.graph[node]:
                if neighbour not in visited:
                    visited.add(neighbour)
                    queue.append(neighbour)


def generate_graph(n, edges_per_node=3):
    g = Graph(n)

    for i in range(n):
        for _ in range(edges_per_node):
            v = random.randint(0, n - 1)

            if v != i:
                g.addEdge(i, v)

    return g


values = [10, 50, 100, 200, 300, 400, 500]

dfs_times = []
bfs_times = []

print("Nodes\tDFS Time\tBFS Time")

for n in values:

    g = generate_graph(n)

    # DFS timing
    start = time.perf_counter()
    g.DFS(0)
    dfs_time = time.perf_counter() - start

    # BFS timing
    start = time.perf_counter()
    g.BFS(0)
    bfs_time = time.perf_counter() - start

    dfs_times.append(dfs_time)
    bfs_times.append(bfs_time)

    print(f"{n}\t\t{dfs_time:.8f}\t{bfs_time:.8f}")


# 1️⃣ DFS Execution Time Graph
plt.figure()
plt.plot(values, dfs_times, marker='o')
plt.xlabel("Number of Nodes")
plt.ylabel("Execution Time (seconds)")
plt.title("DFS Execution Time vs Number of Nodes")
plt.grid()
plt.show()


# 2️⃣ BFS Execution Time Graph
plt.figure()
plt.plot(values, bfs_times, marker='o')
plt.xlabel("Number of Nodes")
plt.ylabel("Execution Time (seconds)")
plt.title("BFS Execution Time vs Number of Nodes")
plt.grid()
plt.show()


# 3️⃣ DFS vs BFS Comparison Graph
plt.figure()
plt.plot(values, dfs_times, marker='o', label="DFS")
plt.plot(values, bfs_times, marker='o', label="BFS")
plt.xlabel("Number of Nodes")
plt.ylabel("Execution Time (seconds)")
plt.title("DFS vs BFS Execution Time Comparison")
plt.legend()
plt.grid()
plt.show()