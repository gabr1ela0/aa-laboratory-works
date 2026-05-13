import heapq
import random
import matplotlib.pyplot as plt
import matplotlib.patches as mpatches
import networkx as nx
from matplotlib.widgets import Button

BG            = "#0F0E17"
PANEL_BG      = "#1A1825"
PURPLE_BRIGHT = "#A855F7"
PURPLE_MID    = "#7C3AED"
PURPLE_DARK   = "#4C1D95"
LAVENDER      = "#2E2B3F"
AMBER         = "#F59E0B"
AMBER_GLOW    = "#FCD34D"
GREEN_ACCEPT  = "#10B981"
RED_REJECT    = "#EF4444"
RED_LIGHT     = "#7F1D1D"
EDGE_DEFAULT  = "#2D2B3D"
TEXT_BRIGHT   = "#E2E8F0"
TEXT_DIM      = "#94A3B8"

NUM_NODES  = 8
NUM_EDGES  = 14
BASE_DELAY = 1.0

SPEED_STEPS  = [0.25, 0.5, 1.0, 2.0, 4.0]
SPEED_LABELS = ["0.25", "0.5", "1", "2", "4"]

state = {
    "multiplier": 1.0,
    "paused":     False,
    "reset":      False,
    "replay":     False,
}

# Graph axes band
GRAPH_BOTTOM = 0.30
GRAPH_TOP    = 0.87
GRAPH_H      = GRAPH_TOP - GRAPH_BOTTOM


def build_graph(n=NUM_NODES, m=NUM_EDGES):
    rng = random.Random(random.randint(0, 99999))
    G   = nx.Graph()
    G.add_nodes_from(range(n))
    nodes = list(range(n))
    rng.shuffle(nodes)
    for i in range(1, n):
        G.add_edge(nodes[i-1], nodes[i], weight=rng.randint(1, 20))
    while G.number_of_edges() < m:
        u, v = rng.sample(range(n), 2)
        if not G.has_edge(u, v):
            G.add_edge(u, v, weight=rng.randint(1, 20))
    return G


class UnionFind:
    def __init__(self, n):
        self.parent = list(range(n))
        self.rank   = [0] * n

    def find(self, x):
        while self.parent[x] != x:
            self.parent[x] = self.parent[self.parent[x]]
            x = self.parent[x]
        return x

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


def draw_subplot(ax, G, pos, node_colors, node_sizes, edge_styles,
                 node_borders, subtitle, info_lines):
    ax.clear()
    ax.set_facecolor(PANEL_BG)
    ax.set_axis_off()

    glow_edges = [
        (u, v) for (u, v) in G.edges()
        if edge_styles.get(tuple(sorted((u, v))), (None,))[0]
        in (PURPLE_BRIGHT, GREEN_ACCEPT, AMBER_GLOW)
    ]
    if glow_edges:
        nx.draw_networkx_edges(G, pos, ax=ax, edgelist=glow_edges,
                               edge_color=PURPLE_MID, width=9.0,
                               alpha=0.22, style="solid")

    by_style = {}
    for u, v in G.edges():
        key = tuple(sorted((u, v)))
        c, w, s = edge_styles.get(key, (EDGE_DEFAULT, 1.0, "solid"))
        by_style.setdefault((c, w, s), []).append((u, v))
    for (c, w, s), edges in by_style.items():
        nx.draw_networkx_edges(G, pos, ax=ax, edgelist=edges,
                               edge_color=c, width=w, style=s,
                               alpha=1.0 if s == "solid" else 0.55)

    nx.draw_networkx_nodes(G, pos, ax=ax, node_color=node_colors,
                           node_size=node_sizes, edgecolors=node_borders,
                           linewidths=2.0)
    nx.draw_networkx_labels(G, pos, ax=ax, font_color=TEXT_BRIGHT,
                            font_weight="bold", font_size=11)
    edge_labels = {(u, v): d["weight"] for u, v, d in G.edges(data=True)}
    nx.draw_networkx_edge_labels(G, pos, edge_labels=edge_labels, ax=ax,
                                 font_color=TEXT_BRIGHT, font_size=8,
                                 bbox=dict(boxstyle="round,pad=0.18",
                                           fc=PANEL_BG, ec=EDGE_DEFAULT,
                                           alpha=0.85))
    # Subtitle badge at top of axes only — no info lines inside axes
    ax.text(0.5, 0.97, subtitle,
            transform=ax.transAxes, ha="center", va="top",
            color=TEXT_BRIGHT, fontsize=10, fontweight="bold",
            bbox=dict(boxstyle="round,pad=0.3", fc=PANEL_BG,
                      ec=EDGE_DEFAULT, alpha=0.85, linewidth=0.5))

def kruskal_steps(G):
    n  = G.number_of_nodes()
    uf = UnionFind(n)
    mst, rejected, total = set(), set(), 0
    for u, v, data in sorted(G.edges(data=True), key=lambda e: e[2]["weight"]):
        w   = data["weight"]
        cur = tuple(sorted((u, v)))
        if uf.union(u, v):
            mst.add(cur); total += w
            yield {"current": cur, "weight": w, "accepted": True,
                   "mst": set(mst), "rejected": set(rejected),
                   "total": total, "done": len(mst) == n - 1}
            if len(mst) == n - 1:
                return
        else:
            rejected.add(cur)
            yield {"current": cur, "weight": w, "accepted": False,
                   "mst": set(mst), "rejected": set(rejected),
                   "total": total, "done": False}


def prim_steps(G, start=0):
    n = G.number_of_nodes()
    visited, mst, total = {start}, set(), 0
    heap = []
    for v in G.neighbors(start):
        heapq.heappush(heap, (G[start][v]["weight"], start, v))

    yield {"current_node": start, "current_edge": None, "weight": 0,
           "visited": set(visited), "mst": set(mst),
           "candidates": {tuple(sorted((s, t))) for w, s, t in heap},
           "total": total, "done": False}

    while heap and len(visited) < n:
        while heap:
            w, u, v = heapq.heappop(heap)
            if v not in visited:
                break
        else:
            break
        visited.add(v)
        cur = tuple(sorted((u, v)))
        mst.add(cur); total += w
        for x in G.neighbors(v):
            if x not in visited:
                heapq.heappush(heap, (G[v][x]["weight"], v, x))
        candidates = {tuple(sorted((s, t))) for ww, s, t in heap
                      if t not in visited}
        yield {"current_node": v, "current_edge": cur, "weight": w,
               "visited": set(visited), "mst": set(mst),
               "candidates": candidates, "total": total,
               "done": len(visited) == n}


def kruskal_styles(st, G):
    n, es = G.number_of_nodes(), {}
    for u, v in G.edges():
        key = tuple(sorted((u, v)))
        if key in st["mst"]:
            es[key] = (PURPLE_BRIGHT, 3.0, "solid")
        elif key in st["rejected"] and key != st["current"]:
            es[key] = (RED_LIGHT, 1.2, "dashed")
        else:
            es[key] = (EDGE_DEFAULT, 1.0, "solid")
    if st["current"]:
        es[st["current"]] = (GREEN_ACCEPT, 3.5, "solid") if st["accepted"] \
                             else (RED_REJECT, 3.5, "solid")
    in_mst = {a for a, b in st["mst"]} | {b for a, b in st["mst"]}
    nc = [PURPLE_BRIGHT if v in in_mst else LAVENDER for v in G.nodes()]
    ns = [1000 if v in in_mst else 750 for v in G.nodes()]
    nb = [PURPLE_MID    if v in in_mst else EDGE_DEFAULT for v in G.nodes()]
    if st.get("done"):
        title = "Kruskal  Complete!"
    elif st["accepted"]:
        u, v = st["current"]
        title = f"Kruskal  ({u}-{v}) w={st['weight']}  accepted"
    else:
        u, v = st["current"]
        title = f"Kruskal  ({u}-{v}) w={st['weight']}  cycle!"
    info = [f"MST weight so far: {st['total']}",
            f"Edges accepted: {len(st['mst'])} / {n-1}"]
    return nc, ns, es, nb, title, info


def prim_styles(st, G):
    n, es = G.number_of_nodes(), {}
    for u, v in G.edges():
        key = tuple(sorted((u, v)))
        if key in st["mst"]:
            es[key] = (PURPLE_BRIGHT, 3.0, "solid")
        elif key in st["candidates"]:
            es[key] = (AMBER, 1.8, "dashed")
        else:
            es[key] = (EDGE_DEFAULT, 1.0, "solid")
    if st["current_edge"] and not st.get("done"):
        es[st["current_edge"]] = (AMBER_GLOW, 3.5, "solid")
    nc, ns, nb = [], [], []
    for v in G.nodes():
        if v == st["current_node"] and not st.get("done"):
            nc.append(AMBER_GLOW); ns.append(1100); nb.append(AMBER)
        elif v in st["visited"]:
            nc.append(PURPLE_BRIGHT); ns.append(1000); nb.append(PURPLE_MID)
        else:
            nc.append(LAVENDER); ns.append(750); nb.append(EDGE_DEFAULT)
    if st.get("done"):
        title = "Prim  Complete!"
    elif st["current_edge"] is None:
        title = f"Prim  Starting at node {st['current_node']}"
    else:
        u, v = st["current_edge"]
        title = f"Prim  Node {st['current_node']} via ({u}-{v}) w={st['weight']}"
    info = [f"MST weight so far: {st['total']}",
            f"Nodes visited: {len(st['visited'])} / {n}"]
    return nc, ns, es, nb, title, info


def final_styles(mst_edges, total, label, G):
    es = {tuple(sorted((u, v))): (
              (PURPLE_BRIGHT, 3.0, "solid") if tuple(sorted((u, v))) in mst_edges
              else (EDGE_DEFAULT, 1.0, "solid"))
          for u, v in G.edges()}
    nc = [PURPLE_BRIGHT] * G.number_of_nodes()
    ns = [1000]          * G.number_of_nodes()
    nb = [PURPLE_MID]    * G.number_of_nodes()
    return nc, ns, es, nb, f"{label}  Complete!", [f"Total MST weight: {total}"]


def add_legend(fig):
    patches = [
        mpatches.Patch(color=PURPLE_BRIGHT, label="MST edge / visited node"),
        mpatches.Patch(color=GREEN_ACCEPT,  label="Kruskal: accepted"),
        mpatches.Patch(color=RED_REJECT,    label="Kruskal: rejected (cycle)"),
        mpatches.Patch(color=AMBER_GLOW,    label="Prim: current edge/node"),
        mpatches.Patch(color=AMBER,         label="Prim: candidate edges"),
        mpatches.Patch(color=LAVENDER,      label="Unvisited node"),
    ]
    fig.legend(handles=patches, loc="lower center", ncol=3,
               facecolor=PANEL_BG, edgecolor=EDGE_DEFAULT,
               labelcolor=TEXT_BRIGHT, fontsize=9,
               bbox_to_anchor=(0.5, 0.01),
               bbox_transform=fig.transFigure)


def animate(fig, ax_k, ax_p, G, pos, verdict_obj, pause_btn,info_k1, info_k2, info_p1, info_p2):
    """Run one full animation on the given G/pos. Returns 'replay','reset','done'."""
    state["paused"] = False
    pause_btn.label.set_text("|| Pause")
    fig.canvas.draw_idle()

    k_gen  = kruskal_steps(G)
    p_gen  = prim_steps(G, start=0)
    last_k = last_p = None
    k_done = p_done = False
    verdict_obj.set_text("")

    while not (k_done and p_done):
        if state["reset"]:
            return "reset"
        if state["replay"]:
            state["replay"] = False
            return "replay"

        if state["paused"]:
            plt.pause(0.05)
            continue

        if not k_done:
            try:
                last_k = next(k_gen)
                if last_k.get("done"):
                    k_done = True
            except StopIteration:
                k_done = True

        if not p_done:
            try:
                last_p = next(p_gen)
                if last_p.get("done"):
                    p_done = True
            except StopIteration:
                p_done = True

        if last_k is not None:
            args = (final_styles(last_k["mst"], last_k["total"], "Kruskal", G)
                    if k_done else kruskal_styles(last_k, G))
            draw_subplot(ax_k, G, pos, *args)

        if last_p is not None:
            args = (final_styles(last_p["mst"], last_p["total"], "Prim", G)
                    if p_done else prim_styles(last_p, G))
            draw_subplot(ax_p, G, pos, *args)

        if last_k is not None:
            args = (final_styles(last_k["mst"], last_k["total"], "Kruskal", G)
                    if k_done else kruskal_styles(last_k, G))
            nc, ns, es, nb, subtitle, info_lines = args
            draw_subplot(ax_k, G, pos, nc, ns, es, nb, subtitle, [])
            # Write info below the panel
            info_k1.set_text(info_lines[0] if len(info_lines) > 0 else "")
            info_k2.set_text(info_lines[1] if len(info_lines) > 1 else "")

        if last_p is not None:
            args = (final_styles(last_p["mst"], last_p["total"], "Prim", G)
                    if p_done else prim_styles(last_p, G))
            nc, ns, es, nb, subtitle, info_lines = args
            draw_subplot(ax_p, G, pos, nc, ns, es, nb, subtitle, [])
            info_p1.set_text(info_lines[0] if len(info_lines) > 0 else "")
            info_p2.set_text(info_lines[1] if len(info_lines) > 1 else "")

        plt.pause(BASE_DELAY / state["multiplier"])

    # Final frame
    if last_k and last_p:
        k_total, p_total = last_k["total"], last_p["total"]
        draw_subplot(ax_k, G, pos,
                     *final_styles(last_k["mst"], k_total, "Kruskal", G))
        draw_subplot(ax_p, G, pos,
                     *final_styles(last_p["mst"], p_total, "Prim", G))
        verdict = (
            f"Both algorithms found the same MST  -  Total weight = {k_total}"
            if k_total == p_total
            else f"Kruskal weight = {k_total}   |   Prim weight = {p_total}"
        )
        verdict_obj.set_text(verdict)

    plt.pause(0.1)
    return "done"


def run():
    while True:
        state.update({"reset": False, "replay": False,
                      "paused": False})

        G   = build_graph()
        pos = nx.spring_layout(G, seed=random.randint(0, 9999))

        fig = plt.figure(figsize=(17, 9), facecolor=BG)

        ax_k = fig.add_axes([0.02, GRAPH_BOTTOM, 0.46, GRAPH_H])
        ax_p = fig.add_axes([0.52, GRAPH_BOTTOM, 0.46, GRAPH_H])
        for ax in (ax_k, ax_p):
            ax.set_facecolor(PANEL_BG)

            # Info strips — figure text BELOW each panel, in the gap between
            # GRAPH_BOTTOM (0.30) and the button row (~0.19).
            # Centre of left panel:  0.02 + 0.46/2 = 0.25
            # Centre of right panel: 0.52 + 0.46/2 = 0.75
            INFO_Y1 = GRAPH_BOTTOM - 0.03  # first line (e.g. "Edges accepted")
            INFO_Y2 = GRAPH_BOTTOM - 0.065  # second line (e.g. "MST weight")

            info_k1 = fig.text(0.25, INFO_Y1, "", color=TEXT_DIM, fontsize=9,
                               ha="center", va="top")
            info_k2 = fig.text(0.25, INFO_Y2, "", color=TEXT_DIM, fontsize=9,
                               ha="center", va="top")
            info_p1 = fig.text(0.75, INFO_Y1, "", color=TEXT_DIM, fontsize=9,
                               ha="center", va="top")
            info_p2 = fig.text(0.75, INFO_Y2, "", color=TEXT_DIM, fontsize=9,
                               ha="center", va="top")

        # ── Button layout ─────────────────────────────────────────────────
        # Buttons row centred in the strip y=0.11..0.17
        # Sizes:
        #   speed buttons: w=0.042 (narrow — just fits "0.25")
        #   pause / replay / new: w=0.07
        # Gaps: 0.005 between speed, 0.012 between groups

        BH       = 0.034
        BY       = 0.148   # bottom of button row
        SPW      = 0.044   # speed button width
        ACW      = 0.068   # action button width (pause/replay/new)
        SG       = 0.005   # gap between speed buttons
        AG       = 0.014   # gap between groups / action buttons

        speed_block = 5 * SPW + 4 * SG
        row_w       = speed_block + AG + ACW + AG + ACW + AG + ACW
        left        = (1.0 - row_w) / 2.0

        # Speed buttons
        speed_axes = []
        for i in range(5):
            x = left + i * (SPW + SG)
            speed_axes.append(fig.add_axes([x, BY, SPW, BH]))

        # Action buttons
        x_pause  = left + speed_block + AG
        x_replay = x_pause  + ACW + AG
        x_new    = x_replay + ACW + AG
        ax_pause  = fig.add_axes([x_pause,  BY, ACW, BH])
        ax_replay = fig.add_axes([x_replay, BY, ACW, BH])
        ax_new    = fig.add_axes([x_new,    BY, ACW, BH])

        # Speed label
        fig.text(left - 0.006, BY + BH / 2, "Speed:",
                 color=TEXT_DIM, fontsize=9, ha="right", va="center")

        # Build speed buttons
        speed_btns = []
        for i, ax in enumerate(speed_axes):
            active = (SPEED_STEPS[i] == state["multiplier"])
            btn = Button(ax, SPEED_LABELS[i],
                         color=PURPLE_BRIGHT if active else PURPLE_DARK,
                         hovercolor=PURPLE_MID)
            btn.label.set_color(TEXT_BRIGHT)
            btn.label.set_fontsize(8)

            def on_speed(_, idx=i):
                state["multiplier"] = SPEED_STEPS[idx]
                for j, b in enumerate(speed_btns):
                    col = PURPLE_BRIGHT if j == idx else PURPLE_DARK
                    b.ax.set_facecolor(col)
                    b.color = col
                fig.canvas.draw_idle()

            btn.on_clicked(on_speed)
            speed_btns.append(btn)

        # Pause button
        pause_btn = Button(ax_pause, "|| Pause",
                           color=PURPLE_DARK, hovercolor=PURPLE_MID)
        pause_btn.label.set_color(TEXT_BRIGHT)
        pause_btn.label.set_fontsize(8)

        def on_pause(_):
            state["paused"] = not state["paused"]
            pause_btn.label.set_text(
                "> Resume" if state["paused"] else "|| Pause")
            fig.canvas.draw_idle()

        pause_btn.on_clicked(on_pause)

        # Replay button (same graph, same layout, restart animation)
        replay_btn = Button(ax_replay, "Replay",
                            color=PURPLE_DARK, hovercolor=PURPLE_MID)
        replay_btn.label.set_color(TEXT_BRIGHT)
        replay_btn.label.set_fontsize(8)
        replay_btn.on_clicked(lambda _: state.update({"replay": True,
                                                       "paused": False}))

        # New Graph button
        new_btn = Button(ax_new, "New Graph",
                         color=PURPLE_DARK, hovercolor=PURPLE_MID)
        new_btn.label.set_color(TEXT_BRIGHT)
        new_btn.label.set_fontsize(8)
        new_btn.on_clicked(lambda _: state.update({"reset": True}))

        # ── Figure text ───────────────────────────────────────────────────
        fig.text(0.5, 0.955,
                 "Minimum Spanning Tree - Kruskal  vs  Prim",
                 color=TEXT_BRIGHT, fontsize=14, fontweight="bold",
                 ha="center", va="top")

        verdict_obj = fig.text(
            0.5, GRAPH_TOP + 0.004, "",
            color=AMBER_GLOW, fontsize=10, fontweight="bold",
            ha="center", va="bottom")

        add_legend(fig)

        # ── Animation loop with replay support ────────────────────────────
        while True:
            result = animate(fig, ax_k, ax_p, G, pos,
                             verdict_obj, pause_btn,
                             info_k1, info_k2, info_p1, info_p2)
            if result == "replay":
                # Restart animation on same G/pos — don't rebuild figure
                continue
            elif result == "reset":
                plt.close(fig)
                break
            else:
                # "done" — wait for user action
                while plt.fignum_exists(fig.number) \
                        and not state["reset"] and not state["replay"]:
                    plt.pause(0.15)
                if state["replay"]:
                    state["replay"] = False
                    continue   # rerun animate on same graph
                if state["reset"]:
                    plt.close(fig)
                break

        if not state["reset"]:
            break   # window closed normally


if __name__ == "__main__":
    try:
        run()
    except KeyboardInterrupt:
        plt.close("all")