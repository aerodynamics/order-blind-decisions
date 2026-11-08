#!/usr/bin/env python3
"""Does order sensitivity concentrate where the model is uncertain?
Per item: margin = p(top1) - p(top2) at the first presentation (o0,r1).
Items binned by margin into four fixed bands; per band: share of items whose pick changes
in >=1 of the other three orderings (repeat 1), and share whose pick changes on the identical repeat."""
import sys, json, glob, os
from collections import defaultdict
sys.path.insert(0, os.path.dirname(__file__))
from retention import load, ARMS
root = sys.argv[1]; items, req = load(root)
def probs(raw):
    if isinstance(raw.get("result"), dict): raw = raw["result"]
    a = raw.get("answers"); a = a["evaluation"] if isinstance(a, dict) else a[0]
    p = a.get("probabilities")
    if isinstance(p, dict): return a.get("choice"), sorted(p.values(), reverse=True)
    if isinstance(p, list):
        vals = [x["probability"] if isinstance(x, dict) else x[1] for x in p]
        return a.get("choice"), sorted(vals, reverse=True)
    return a.get("choice"), None
BANDS = [(0,0.1),(0.1,0.3),(0.3,0.6),(0.6,1.01)]
print("| Model | " + " | ".join(f"margin {lo:.1f}–{min(hi,1):.1f}: n / reorder change / repeat change" for lo,hi in BANDS) + " |")
print("|---|" + "---|"*len(BANDS))
for arm, label in ARMS.items():
    rec = {}
    for pth in sorted(glob.glob(os.path.join(root,"runs/main",arm,"*.jsonl"))):
        for l in open(pth):
            x = json.loads(l); rid = x.get("request_id")
            if rid in req and x.get("ok"):
                try: rec[rid] = probs(x["raw"])
                except Exception: pass
    grid = defaultdict(dict)
    for rid, r in req.items():
        if rid in rec: grid[r["item"]][(r["ordering"], r["repeat"])] = rec[rid]
    band = defaultdict(lambda: [0,0,0])
    for k, g in grid.items():
        if len(g) != 8 or g[(0,1)][1] is None or len(g[(0,1)][1]) < 2: continue
        m = g[(0,1)][1][0] - g[(0,1)][1][1]
        pick0 = g[(0,1)][0]
        chg = any(g[(o,1)][0] != pick0 for o in range(1,4)); rep = g[(0,2)][0] != pick0
        for i,(lo,hi) in enumerate(BANDS):
            if lo <= m < hi: band[i][0]+=1; band[i][1]+=chg; band[i][2]+=rep
    cells = []
    for i in range(len(BANDS)):
        n,c,r = band[i]
        cells.append(f"{n} / {100*c/n:.1f}% / {100*r/n:.1f}%" if n else "—")
    print(f"| {label} | " + " | ".join(cells) + " |")
