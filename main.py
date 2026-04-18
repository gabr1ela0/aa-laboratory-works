import heapq
import time
import random
import matplotlib.pyplot as plt
from collections import defaultdict


# Union-Find for Kruskal
class UnionFind:
    def __init__(self, n):
        self.parent = list(range(n))
        self.rank = [0] * n

    def find(self, x):
        if self.parent[x] != x:
            self.parent[x] = self.find(self.parent[x])
        return self.parent[x]

    def union(self, x, y):
        rx, ry = self.find(x), self.find(y)
        if rx == ry:
            return False
        if self.rank[rx] < self.rank[ry]:
            rx, ry = ry, rx
        self.parent[ry] = rx
        if self.rank[rx] == self.rank[ry]:
            self.rank[rx] += 1
        return True


# Kruskal's Algorithm
def kruskal(n, edges):
    edges = sorted(edges)
    uf = UnionFind(n)
    mst_weight = 0
    mst_edges = []
    for weight, u, v in edges:
        if uf.union(u, v):
            mst_weight += weight
            mst_edges.append((u, v, weight))
            if len(mst_edges) == n - 1:
                break
    return mst_weight, mst_edges


# Prim's Algorithm
def prim(n, adj):
    visited = [False] * n
    min_heap = [(0, 0, -1)]
    mst_weight = 0
    mst_edges = []
    while min_heap:
        weight, u, parent = heapq.heappop(min_heap)
        if visited[u]:
            continue
        visited[u] = True
        mst_weight += weight
        if parent != -1:
            mst_edges.append((parent, u, weight))
        for edge_weight, v in adj[u]:
            if not visited[v]:
                heapq.heappush(min_heap, (edge_weight, v, u))
    return mst_weight, mst_edges


# Generates a random connected graph with roughly 2*n edges
def generate_graph(n, max_weight=100):
    edges = []
    adj = defaultdict(list)
    nodes = list(range(n))
    random.shuffle(nodes)

    # Guarantee connectivity with a spanning chain
    for i in range(1, n):
        u, v = nodes[i - 1], nodes[i]
        w = random.randint(1, max_weight)
        edges.append((w, u, v))
        adj[u].append((w, v))
        adj[v].append((w, u))

    # Add roughly n extra random edges
    for _ in range(n):
        u = random.randint(0, n - 1)
        v = random.randint(0, n - 1)
        if u != v:
            w = random.randint(1, max_weight)
            edges.append((w, u, v))
            adj[u].append((w, v))
            adj[v].append((w, u))

    return edges, adj


def demo_small_graph():
    print("DEMO on a small graph with 7 nodes")
    raw_edges = [
        (2, 0, 1), (3, 0, 3), (3, 1, 2), (4, 1, 3),
        (5, 1, 4), (6, 2, 4), (7, 3, 4), (4, 3, 5),
        (6, 4, 5), (5, 4, 6), (8, 5, 6)
    ]
    n = 7
    adj = defaultdict(list)
    for w, u, v in raw_edges:
        adj[u].append((w, v))
        adj[v].append((w, u))

    k_weight, k_edges = kruskal(n, raw_edges)
    print(f"Kruskal MST weight: {k_weight}")
    print("Kruskal edges:", [(u, v, w) for u, v, w in k_edges])

    p_weight, p_edges = prim(n, adj)
    print(f"Prim MST weight: {p_weight}")
    print("Prim edges:", [(u, v, w) for u, v, w in p_edges])
    print()





