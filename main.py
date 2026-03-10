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

    # BFS implementation
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