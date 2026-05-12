"""
Lab 4 - Visualization of Dijkstra's and Floyd-Warshall's algorithms.
"""

import heapq
import random
import matplotlib.pyplot as plt
import networkx as nx

DEEP_PURPLE     = "#7C3AED"   # currently processing / active
MEDIUM_PURPLE   = "#A78BFA"   # visited / finalized
LAVENDER        = "#EDE9FE"   # unvisited / inactive
DARK_TEXT       = "#1E1B4B"
EDGE_DEFAULT    = "#D1D5DB"   # light gray
EDGE_HIGHLIGHT  = "#7C3AED"   # bold purple
GRAY_TEXT       = "#9CA3AF"

NUM_NODES   = 8
NUM_EDGES   = 14
SOURCE      = 0
PAUSE_DIJK  = 1.2
PAUSE_FW    = 1.5

def build_graph(n=NUM_NODES, m=NUM_EDGES, seed=7):
    rng = random.Random(seed)
    G = nx.Graph()
    G.add_nodes_from(range(n))

    # Spanning tree backbone to guarantee connectivity
    nodes = list(range(n))
    rng.shuffle(nodes)
    for i in range(1, n):
        u, v = nodes[i - 1], nodes[i]
        G.add_edge(u, v, weight=rng.randint(1, 20))

    # Fill up to m edges with random extras
    while G.number_of_edges() < m:
        u, v = rng.sample(range(n), 2)
        if not G.has_edge(u, v):
            G.add_edge(u, v, weight=rng.randint(1, 20))

    return G



def draw_graph(ax, G, pos, node_colors, edge_colors, edge_widths):
    """Render one frame of the graph on a given axis."""
    ax.clear()
    ax.set_facecolor("white")

    nx.draw_networkx_edges(
        G, pos, ax=ax,
        edge_color=edge_colors, width=edge_widths,
    )
    nx.draw_networkx_nodes(
        G, pos, ax=ax,
        node_color=node_colors, node_size=900,
        edgecolors=DARK_TEXT, linewidths=1.2,
    )
    nx.draw_networkx_labels(
        G, pos, ax=ax,
        font_color="white", font_weight="bold", font_size=11,
    )
    edge_labels = {(u, v): d["weight"] for u, v, d in G.edges(data=True)}
    nx.draw_networkx_edge_labels(
        G, pos, edge_labels=edge_labels, ax=ax,
        font_color=DARK_TEXT, font_size=8,
        bbox=dict(boxstyle="round,pad=0.15", fc="white", ec="none", alpha=0.85),
    )
    ax.set_axis_off()


def draw_distance_table(ax, distances, finalized, just_updated, current=None):
    """Right-hand panel for Dijkstra — table of distances."""
    ax.clear()
    ax.set_facecolor("white")
    ax.set_axis_off()

    cell_text = []
    cell_colors = []
    for node in range(len(distances)):
        d = distances[node]
        d_str = "∞" if d == float("inf") else str(d)
        cell_text.append([str(node), d_str])

        # Color the distance cell based on state
        if node in just_updated:
            color = DEEP_PURPLE
        elif node in finalized:
            color = MEDIUM_PURPLE
        else:
            color = GRAY_TEXT
        cell_colors.append([DARK_TEXT, color])

    table = ax.table(
        cellText=cell_text,
        colLabels=["Node", "Distance from 0"],
        loc="center",
        cellLoc="center",
        colWidths=[0.3, 0.5],
    )
    table.auto_set_font_size(False)
    table.set_fontsize(11)
    table.scale(1, 1.6)

    # Style header
    for j in range(2):
        c = table[(0, j)]
        c.set_facecolor(LAVENDER)
        c.set_text_props(color=DARK_TEXT, weight="bold")

    # Recolor data cells
    for i in range(len(distances)):
        for j in range(2):
            cell = table[(i + 1, j)]
            cell.set_facecolor("white")
            cell.set_edgecolor(LAVENDER)
            cell.set_text_props(color=cell_colors[i][j])

    ax.set_title("Distances", color=DARK_TEXT, fontsize=12)



# Dijkstra visualization
def run_dijkstra_visual(G, pos):
    n = G.number_of_nodes()
    distances = [float("inf")] * n
    distances[SOURCE] = 0
    finalized = set()
    parent = [-1] * n
    heap = [(0, SOURCE)]

    fig, (ax_g, ax_t) = plt.subplots(1, 2, figsize=(14, 6),
                                     gridspec_kw={"width_ratios": [2, 1]})
    fig.patch.set_facecolor("white")

    # initial state
    node_colors = [LAVENDER] * n
    edge_colors = [EDGE_DEFAULT] * G.number_of_edges()
    edge_widths = [1.2] * G.number_of_edges()

    draw_graph(ax_g, G, pos, node_colors, edge_colors, edge_widths)
    draw_distance_table(ax_t, distances, finalized, just_updated=set())
    plt.suptitle("Dijkstra — Initial state. Source = node 0, all distances = ∞",
                 color=DARK_TEXT, fontsize=13)
    plt.tight_layout()
    plt.pause(PAUSE_DIJK)

    edge_list = list(G.edges())

    while heap:
        d, u = heapq.heappop(heap)
        if u in finalized:
            continue
        finalized.add(u)
        print(f"Processing node {u}, distance {d}")

        # Relax neighbors and track which were updated this round
        just_updated = set()
        relaxed_edges = []
        for v in G.neighbors(u):
            w = G[u][v]["weight"]
            if distances[u] + w < distances[v]:
                distances[v] = distances[u] + w
                parent[v] = u
                heapq.heappush(heap, (distances[v], v))
                just_updated.add(v)
                relaxed_edges.append((u, v))

        # Build node coloring
        node_colors = []
        for k in range(n):
            if k == u:
                node_colors.append(DEEP_PURPLE)
            elif k in finalized:
                node_colors.append(MEDIUM_PURPLE)
            else:
                node_colors.append(LAVENDER)

        # Edge coloring
        edge_colors = []
        edge_widths = []
        for (a, b) in edge_list:
            if (a, b) in relaxed_edges or (b, a) in relaxed_edges:
                edge_colors.append(EDGE_HIGHLIGHT)
                edge_widths.append(3.0)
            else:
                edge_colors.append(EDGE_DEFAULT)
                edge_widths.append(1.2)

        draw_graph(ax_g, G, pos, node_colors, edge_colors, edge_widths)
        draw_distance_table(ax_t, distances, finalized, just_updated, current=u)
        plt.suptitle(f"Dijkstra — Processing node {u}, relaxing edges to neighbors",
                     color=DARK_TEXT, fontsize=13)
        plt.tight_layout()
        plt.pause(PAUSE_DIJK)

    # highlight shortest path tree
    sp_edges = set()
    for v in range(n):
        if parent[v] != -1:
            sp_edges.add(tuple(sorted((v, parent[v]))))

    node_colors = [MEDIUM_PURPLE] * n
    edge_colors = []
    edge_widths = []
    for (a, b) in edge_list:
        if tuple(sorted((a, b))) in sp_edges:
            edge_colors.append(EDGE_HIGHLIGHT)
            edge_widths.append(3.0)
        else:
            edge_colors.append(EDGE_DEFAULT)
            edge_widths.append(1.2)

    draw_graph(ax_g, G, pos, node_colors, edge_colors, edge_widths)
    draw_distance_table(ax_t, distances, finalized=set(range(n)), just_updated=set())
    plt.suptitle("Dijkstra — Complete! Shortest distances from node 0 found.",
                 color=DARK_TEXT, fontsize=13)
    plt.tight_layout()
    plt.pause(PAUSE_DIJK)
    plt.close(fig)

    return distances


# Floyd-Warshall visualization
def draw_matrix(ax, dist, updated_now, updated_before):
    """Right-hand panel for Floyd-Warshall — V x V distance matrix."""
    ax.clear()
    ax.set_facecolor("white")
    ax.set_axis_off()

    n = len(dist)
    cell_text = []
    for i in range(n):
        row = []
        for j in range(n):
            v = dist[i][j]
            row.append("∞" if v == float("inf") else str(v))
        cell_text.append(row)

    table = ax.table(
        cellText=cell_text,
        rowLabels=[str(i) for i in range(n)],
        colLabels=[str(j) for j in range(n)],
        loc="center",
        cellLoc="center",
    )
    table.auto_set_font_size(False)
    table.set_fontsize(9)
    table.scale(1, 1.3)

    # Color header row + column
    for j in range(n):
        c = table[(0, j)]
        c.set_facecolor(LAVENDER)
        c.set_text_props(color=DARK_TEXT, weight="bold")
    for i in range(n):
        c = table[(i + 1, -1)]
        c.set_facecolor(LAVENDER)
        c.set_text_props(color=DARK_TEXT, weight="bold")

    # Color data cells
    for i in range(n):
        for j in range(n):
            cell = table[(i + 1, j)]
            if (i, j) in updated_now:
                cell.set_facecolor(LAVENDER)
                cell.set_text_props(color=DEEP_PURPLE, weight="bold")
            elif (i, j) in updated_before:
                cell.set_facecolor(MEDIUM_PURPLE)
                cell.set_text_props(color="white")
            else:
                cell.set_facecolor("white")
                cell.set_text_props(color=DARK_TEXT)
            cell.set_edgecolor(LAVENDER)

    ax.set_title("Distance matrix", color=DARK_TEXT, fontsize=12)


def run_floyd_warshall_visual(G, pos):
    n = G.number_of_nodes()

    # Build initial distance matrix from the undirected graph
    INF = float("inf")
    dist = [[INF] * n for _ in range(n)]
    for i in range(n):
        dist[i][i] = 0
    for u, v, data in G.edges(data=True):
        dist[u][v] = data["weight"]
        dist[v][u] = data["weight"]

    fig, (ax_g, ax_m) = plt.subplots(1, 2, figsize=(14, 6),
                                     gridspec_kw={"width_ratios": [1, 1.2]})
    fig.patch.set_facecolor("white")

    updated_before = set()
    edge_list = list(G.edges())

    for k in range(n):
        updated_now = set()
        for i in range(n):
            for j in range(n):
                if dist[i][k] + dist[k][j] < dist[i][j]:
                    dist[i][j] = dist[i][k] + dist[k][j]
                    updated_now.add((i, j))

        print(f"Floyd-Warshall: intermediate k={k}, {len(updated_now)} cells updated")

        node_colors = [DEEP_PURPLE if v == k else LAVENDER for v in range(n)]
        edge_colors = [EDGE_DEFAULT] * len(edge_list)
        edge_widths = [1.2] * len(edge_list)

        draw_graph(ax_g, G, pos, node_colors, edge_colors, edge_widths)
        draw_matrix(ax_m, dist, updated_now, updated_before)
        plt.suptitle(
            f"Floyd-Warshall — Intermediate node k = {k}. "
            f"Checking if paths through {k} are shorter.",
            color=DARK_TEXT, fontsize=13,
        )
        plt.tight_layout()
        plt.pause(PAUSE_FW)

        updated_before |= updated_now

    # Final frame
    node_colors = [MEDIUM_PURPLE] * n
    edge_colors = [EDGE_DEFAULT] * len(edge_list)
    edge_widths = [1.2] * len(edge_list)
    draw_graph(ax_g, G, pos, node_colors, edge_colors, edge_widths)
    draw_matrix(ax_m, dist, updated_now=set(), updated_before=updated_before)
    plt.suptitle("Floyd-Warshall — Complete! All-pairs shortest paths found.",
                 color=DARK_TEXT, fontsize=13)
    plt.tight_layout()
    plt.show()

    return dist

if __name__ == "__main__":
    G = build_graph()
    # Spring layout computed ONCE — nodes must never move
    pos = nx.spring_layout(G, seed=42)

    print("Dijkstra")
    dijkstra_dist = run_dijkstra_visual(G, pos)
    print("Final Dijkstra distances:", dijkstra_dist)

    print("\nFloyd-Warshall")
    fw_dist = run_floyd_warshall_visual(G, pos)
    print("Floyd-Warshall row from node 0:", fw_dist[0])
