#!/usr/bin/env python3
"""McNemar exact tests on the order-blind receipts: does reordering change the pick more often
than resending the identical request? Per item: pick at (o0,r1) vs (o0,r2) [repeat] and vs (o1,r1)
[one reordering, same repeat index]. Also the correctness version restricted to items correct at (o0,r1).
Holm correction across the seven arms. Shares are item-level."""
import sys, json, glob, os
from collections import defaultdict
from scipy.stats import binomtest
sys.path.insert(0, os.path.dirname(__file__))
from retention import load, answers, extract_choice, ARMS
root = sys.argv[1]
items, req = load(root)
res = []
for arm in ARMS:
    ans = answers(root, arm, req)
    grid = defaultdict(dict); cc = {}
    for rid, r in req.items():
        it = items[r["item"]]; c = [x["code"] for x in it["candidates"] if x.get("correct")]
        if len(c) != 1: continue
        cc[r["item"]] = c[0]; grid[r["item"]][(r["ordering"], r["repeat"])] = ans.get(rid)
    # pick-change version
    b = c_ = 0; n = 0; nrep = nord = 0
    # correctness version (items correct at first)
    b2 = c2 = 0; n2 = 0; lrep = lord = 0
    for k, g in grid.items():
        if len(g) != 8: continue
        n += 1
        rep = g[(0,1)] != g[(0,2)]; ord_ = g[(0,1)] != g[(1,1)]
        nrep += rep; nord += ord_
        if ord_ and not rep: b += 1
        if rep and not ord_: c_ += 1
        if g[(0,1)] == cc[k]:
            n2 += 1
            lr = g[(0,2)] != cc[k]; lo = g[(1,1)] != cc[k]
            lrep += lr; lord += lo
            if lo and not lr: b2 += 1
            if lr and not lo: c2 += 1
    p1 = binomtest(min(b,c_), b+c_, 0.5).pvalue if b+c_ else 1.0
    p2 = binomtest(min(b2,c2), b2+c2, 0.5).pvalue if b2+c2 else 1.0
    res.append((ARMS[arm], n, nrep/n, nord/n, b, c_, p1, n2, lrep/n2, lord/n2, b2, c2, p2))
def holm(ps):
    m=len(ps); order=sorted(range(m), key=lambda i: ps[i]); out=[0]*m; run=0
    for rank,i in enumerate(order):
        run=max(run, min(1,(m-rank)*ps[i])); out[i]=run
    return out
h1 = holm([r[6] for r in res]); h2 = holm([r[12] for r in res])
print("| Model | Items | Pick changed on repeat | Pick changed on one reordering | McNemar b/c | p (Holm) | Items correct first | Lost on repeat | Lost on one reordering | b/c | p (Holm) |")
print("|---|---:|---:|---:|---:|---:|---:|---:|---:|---:|---:|")
for i,r in enumerate(res):
    print(f"| {r[0]} | {r[1]:,} | {100*r[2]:.1f}% | {100*r[3]:.1f}% | {r[4]}/{r[5]} | {h1[i]:.2g} | {r[7]:,} | {100*r[8]:.1f}% | {100*r[9]:.1f}% | {r[10]}/{r[11]} | {h2[i]:.2g} |")
