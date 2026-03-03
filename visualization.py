import tkinter as tk
import random
import math

BG      = "#2d0a1f"
PANEL   = "#3d0f2a"
CARD    = "#4a1235"
BAR_DEF = "#6b2545"
COMPARE = "#f59e0b"
ACTIVE  = "#f472b6"
DONE    = "#86efac"
TEXT    = "#fce7f3"
DIM     = "#9d4e6e"

ACCENT = {"Quick": "#fb7185", "Merge": "#c084fc",
          "Heap":  "#60a5fa", "Count": "#34d399"}
COMPLEXITY = {"Quick": "O(n log n)", "Merge": "O(n log n)",
              "Heap":  "O(n log n)", "Count": "O(n + k)"}

# ── GENERATORS ───────────────────────────────────────────────────────────────

def quick_sort_gen(arr):
    a = arr[:]
    def qs(lo, hi):
        if lo >= hi: return
        pivot, i = a[hi], lo
        for j in range(lo, hi):
            yield a[:], [j, hi], [], 0
            if a[j] <= pivot:
                a[i], a[j] = a[j], a[i]
                yield a[:], [], [i, j], 0
                i += 1
        a[i], a[hi] = a[hi], a[i]
        yield a[:], [], [i, hi], 0
        yield from qs(lo, i - 1)
        yield from qs(i + 1, hi)
    yield from qs(0, len(a) - 1)
    yield a[:], [], list(range(len(a))), 0

def merge_sort_gen(arr):
    a = arr[:]
    def ms(lo, hi):
        if lo >= hi: return
        mid = (lo + hi) // 2
        yield from ms(lo, mid)
        yield from ms(mid + 1, hi)
        L, R = a[lo:mid+1], a[mid+1:hi+1]
        i = j = 0; k = lo
        while i < len(L) and j < len(R):
            yield a[:], [lo+i, mid+1+j], [], 0
            if L[i] <= R[j]: a[k] = L[i]; i += 1
            else: a[k] = R[j]; j += 1
            yield a[:], [], [k], 0; k += 1
        while i < len(L): a[k] = L[i]; i += 1; yield a[:], [], [k], 0; k += 1
        while j < len(R): a[k] = R[j]; j += 1; yield a[:], [], [k], 0; k += 1
    yield from ms(0, len(a) - 1)
    yield a[:], [], list(range(len(a))), 0

def heap_sort_gen(arr):
    a = arr[:]
    n = len(a)
    def heapify(size, root):
        largest, l, r = root, 2*root+1, 2*root+2
        cmp_idx = [root] + ([l] if l < size else []) + ([r] if r < size else [])
        yield a[:], cmp_idx, [], size
        if l < size and a[l] > a[largest]: largest = l
        if r < size and a[r] > a[largest]: largest = r
        if largest != root:
            a[root], a[largest] = a[largest], a[root]
            yield a[:], [], [root, largest], size
            yield from heapify(size, largest)
    for i in range(n // 2 - 1, -1, -1):
        yield from heapify(n, i)
    for i in range(n - 1, 0, -1):
        a[0], a[i] = a[i], a[0]
        yield a[:], [], [0, i], i
        yield from heapify(i, 0)
    yield a[:], [], list(range(n)), 0

def count_sort_gen(arr):
    a = arr[:]
    mx = max(a)
    cnt = [0] * (mx + 1)
    for i in range(len(a)):
        cnt[a[i]] += 1
        yield a[:], [i], [], 0
    for i in range(1, mx + 1): cnt[i] += cnt[i - 1]
    out = [0] * len(a)
    for i in range(len(a) - 1, -1, -1):
        out[cnt[a[i]] - 1] = a[i]; cnt[a[i]] -= 1
        tmp = a[:]
        for k, v in enumerate(out):
            if v: tmp[k] = v
        yield tmp, [], [max(0, cnt[a[i]])], 0
    for i in range(len(a)): a[i] = out[i]
    yield a[:], [], list(range(len(a))), 0

GENERATORS = {"Quick": quick_sort_gen, "Merge": merge_sort_gen,
              "Heap":  heap_sort_gen,  "Count": count_sort_gen}

# ── APP ──────────────────────────────────────────────────────────────────────

class App:
    def __init__(self, root):
        self.root = root
        self.root.title("Sorting Visualizer")
        self.root.configure(bg=BG)
        self.root.geometry("980x620")
        self.root.resizable(False, False)

        self.algo      = "Quick"
        self.array     = []
        self.generator = None
        self.paused    = False
        self.running   = False
        self.steps     = 0

        self._build()
        self.new_array()

    def _build(self):
        # top bar
        top = tk.Frame(self.root, bg=PANEL, height=55)
        top.pack(fill="x")
        top.pack_propagate(False)
        tk.Label(top, text="Sorting", bg=PANEL, fg=TEXT,
                 font=("Courier", 20, "bold")).pack(side="left", padx=7, pady=10)
        tk.Label(top, text="Visualizer", bg=PANEL, fg=TEXT,
                 font=("Courier", 20, "bold")).pack(side="left", pady=10)
        self.status_lbl = tk.Label(top, text="READY", bg=PANEL, fg=DIM,
                                   font=("Courier", 13))
        self.status_lbl.pack(side="right", padx=20)
        self.steps_lbl = tk.Label(top, text="steps: 0", bg=PANEL, fg=DIM,
                                  font=("Courier", 13))
        self.steps_lbl.pack(side="right", padx=10)

        # algo row
        ar = tk.Frame(self.root, bg=BG)
        ar.pack(fill="x", padx=16, pady=(10, 0))
        tk.Label(ar, text="ALGORITHM", bg=BG, fg=DIM,
                 font=("Courier", 11)).pack(side="left", padx=(0, 12))
        self.abtns = {}
        for name in ["Quick", "Merge", "Heap", "Count"]:
            b = tk.Button(ar, text=f"{name} Sort", bg=CARD, fg=DIM,
                          relief="flat", font=("Courier", 12, "bold"),
                          cursor="hand2", padx=16, pady=7,
                          command=lambda n=name: self._pick(n))
            b.pack(side="left", padx=4)
            self.abtns[name] = b
        self.cplx_lbl = tk.Label(ar, text="", bg=BG, fg=DIM, font=("Courier", 11))
        self.cplx_lbl.pack(side="left", padx=14)
        self._pick("Quick")

        # array label
        af = tk.Frame(self.root, bg=CARD, height=44)
        af.pack(fill="x", padx=16, pady=(8, 0))
        af.pack_propagate(False)
        self.arr_lbl = tk.Label(af, text="", bg=CARD, fg=TEXT,
                                font=("Courier", 12), anchor="w")
        self.arr_lbl.pack(fill="x", padx=10, pady=7)

        # canvas
        self.canvas = tk.Canvas(self.root, bg=BG, highlightthickness=0,
                                width=980, height=300)
        self.canvas.pack(pady=2)

        # legend
        leg = tk.Frame(self.root, bg=BG)
        leg.pack(pady=(2, 0))
        for col, lbl in [(COMPARE, "Comparing"), (ACTIVE, "Swapping"),
                         (DONE, "Sorted"), (BAR_DEF, "Default")]:
            tk.Label(leg, text="■", bg=BG, fg=col,
                     font=("Courier", 14)).pack(side="left", padx=3)
            tk.Label(leg, text=lbl, bg=BG, fg=DIM,
                     font=("Courier", 11)).pack(side="left", padx=(0, 14))

        # bottom controls
        bot = tk.Frame(self.root, bg=PANEL, height=62)
        bot.pack(fill="x", side="bottom")
        bot.pack_propagate(False)

        def btn(txt, cmd, fg, bg):
            return tk.Button(bot, text=txt, command=cmd, bg=bg, fg=fg,
                             activebackground=bg, activeforeground=fg,
                             relief="flat", font=("Courier", 11, "bold"),
                             padx=16, pady=8, cursor="hand2")

        btn("NEW ARRAY", self.new_array, BG,    TEXT).pack(side="left", padx=10, pady=10)
        btn("START",     self.start,     "#000", ACCENT["Quick"]).pack(side="left", padx=4, pady=10)
        self.pbtn = btn("PAUSE", self.toggle_pause, "#000", "#f59e0b")
        self.pbtn.pack(side="left", padx=4, pady=10)
        reset_btn = tk.Button(bot, text="RESET", command=self.reset,
                              bg="#000000", fg=DIM, activebackground="#111111",
                              activeforeground=DIM,
                              relief="flat", font=("Courier", 11, "bold"),
                              padx=16, pady=8, cursor="hand2")
        reset_btn.pack(side="left", padx=4, pady=10)

        tk.Label(bot, text="SIZE", bg=PANEL, fg=DIM,
                 font=("Courier", 10)).pack(side="left", padx=(20, 2))
        self.size_sl = tk.Scale(bot, from_=10, to=50, orient="horizontal",
                                bg=PANEL, fg=TEXT, highlightthickness=0,
                                troughcolor=CARD, length=90, showvalue=True, width=10)
        self.size_sl.set(28)
        self.size_sl.pack(side="left")

        tk.Label(bot, text="  SPEED", bg=PANEL, fg=DIM,
                 font=("Courier", 10)).pack(side="left", padx=(14, 2))
        self.spd_sl = tk.Scale(bot, from_=1, to=100, orient="horizontal",
                               bg=PANEL, fg=TEXT, highlightthickness=0,
                               troughcolor=CARD, length=100, showvalue=False, width=10)
        self.spd_sl.set(20)
        self.spd_sl.pack(side="left")
        self.spd_lbl = tk.Label(bot, text="med", bg=PANEL, fg=DIM, font=("Courier", 10))
        self.spd_lbl.pack(side="left", padx=6)
        self.spd_sl.bind("<Motion>", lambda _: self._spd_upd())

    # ── helpers ──────────────────────────────

    def _pick(self, name):
        if self.running: return
        self.algo = name
        ac = ACCENT[name]
        for n, b in self.abtns.items():
            b.config(bg=ac if n == name else CARD,
                     fg="#000" if n == name else DIM)
        self.cplx_lbl.config(text=COMPLEXITY[name])

    def _spd_upd(self):
        v = self.spd_sl.get()
        self.spd_lbl.config(text="slow" if v < 34 else ("med" if v < 67 else "fast"))

    def _arr_txt(self, arr):
        self.arr_lbl.config(text="[ " + "  ".join(str(v) for v in arr) + " ]")

    # ── draw bars ────────────────────────────

    def _draw_bars(self, arr, cmp, act):
        c = self.canvas
        c.delete("all")
        if not arr: return
        W, H = 950, 290
        n, mx = len(arr), max(arr)
        bw  = W / n
        gap = max(1, bw * 0.14)
        ac  = ACCENT[self.algo]
        all_done = len(act) == n

        for i, v in enumerate(arr):
            x0 = 14 + i * bw + gap / 2
            x1 = 14 + (i + 1) * bw - gap / 2
            bh = max(4, (v / mx) * (H - 24))
            y0, y1 = H - bh, H
            color = (DONE if all_done else
                     ACTIVE if i in act else
                     COMPARE if i in cmp else BAR_DEF)
            c.create_rectangle(x0, y0, x1, y1, fill=color, outline="")
            if bw > 16:
                fs = max(7, min(10, int(bw * 0.55)))
                c.create_text((x0+x1)/2, y0-5, text=str(v),
                              fill=DIM if color == BAR_DEF else color,
                              font=("Courier", fs))

        self.steps_lbl.config(text=f"steps: {self.steps}")
        self._arr_txt(arr)

    # ── draw heap tree ────────────────────────

    def _draw_heap(self, arr, cmp, act, heap_size):
        c = self.canvas
        c.delete("all")
        if not arr: return

        size = min(heap_size, 31) if heap_size > 1 else len(arr)
        W, H = 950, 290
        depth = max(1, math.floor(math.log2(size)))
        nodes = []

        for i in range(size):
            d   = math.floor(math.log2(i + 1))
            pos = i - (2**d - 1)
            tot = 2**d
            x   = (W / (tot + 1)) * (pos + 1) + 14
            y   = 26 + d * ((H - 60) / (depth + 1))
            nodes.append((i, x, y, arr[i]))

        # edges
        for i, x, y, v in nodes:
            if i > 0:
                pi  = (i - 1) // 2
                px, py = nodes[pi][1], nodes[pi][2]
                c.create_line(px, py, x, y, fill=CARD, width=2)

        # nodes
        ac = ACCENT["Heap"]
        for i, x, y, v in nodes:
            fill   = ac      if i in act else COMPARE if i in cmp else "#1e1e2e"
            stroke = ac      if i in act else COMPARE if i in cmp else "#334155"
            c.create_oval(x-17, y-17, x+17, y+17, fill=fill, outline=stroke, width=2)
            c.create_text(x, y, text=str(v), fill=TEXT, font=("Courier", 9, "bold"))

        # sorted strip at bottom
        sorted_part = arr[heap_size:] if heap_size < len(arr) else []
        if sorted_part:
            sw = W / len(arr)
            for idx, val in enumerate(sorted_part):
                ri = heap_size + idx
                x0 = 14 + ri * sw
                x1 = x0 + sw - 2
                c.create_rectangle(x0, H - 14, x1, H, fill=DONE, outline="")

        self.steps_lbl.config(text=f"steps: {self.steps}")
        self._arr_txt(arr)

    # ── controls ─────────────────────────────

    def new_array(self):
        if self.running: return
        n = self.size_sl.get()
        self.array = [random.randint(5, 99) for _ in range(n)]
        self.steps = 0
        self.steps_lbl.config(text="steps: 0")
        self.status_lbl.config(text="READY", fg=DIM)
        self._draw_bars(self.array, [], [])

    def start(self):
        if self.running or not self.array: return
        self.generator = GENERATORS[self.algo](self.array[:])
        self.running   = True
        self.paused    = False
        self.steps     = 0
        self.pbtn.config(text="PAUSE")
        self.status_lbl.config(text=f"{self.algo.upper()} SORT", fg=ACCENT[self.algo])
        self._animate()

    def toggle_pause(self):
        if not self.running: return
        self.paused = not self.paused
        self.pbtn.config(text="RESUME" if self.paused else "PAUSE")
        if not self.paused: self._animate()

    def reset(self):
        self.running   = False
        self.paused    = False
        self.generator = None
        self.steps     = 0
        self.pbtn.config(text="PAUSE")
        self.new_array()

    def _animate(self):
        if self.paused or not self.running: return
        try:
            arr, cmp, act, hs = next(self.generator)
            self.array  = arr
            self.steps += 1
            if self.algo == "Heap":
                self._draw_heap(arr, cmp, act, hs if hs > 0 else len(arr))
            else:
                self._draw_bars(arr, cmp, act)
            delay = max(5, 500 - self.spd_sl.get() * 5)
            self.root.after(delay, self._animate)
        except StopIteration:
            self._draw_bars(self.array, [], list(range(len(self.array))))
            self.running = False
            self.status_lbl.config(text="SORTED", fg=DONE)


if __name__ == "__main__":
    root = tk.Tk()
    App(root)
    root.mainloop()