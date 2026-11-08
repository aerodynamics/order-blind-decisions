#!/usr/bin/env python3
"""Item-level stability of choice verdicts: repeat agreement, order agreement, retention.

Companion to pairwise_slots.py. Same data: haystack arm, choice format,
items with exactly one correct response, 4 Williams orderings x 2 byte-identical
repeats = 8 presentations per item.

Reported per model arm (item-level, so each item counts once):
  acc_first        accuracy at presentation (ordering 0, repeat 1)
  acc_mean         mean accuracy over all 8 presentations (what the slot tables average)
  repeat_agree     share of (ordering) pairs where repeat 1 and repeat 2 pick the same response
  order_agree      share of items whose picked response is identical across all 4 orderings (repeat 1)
  flip_repeat      share of items correct at first presentation but wrong at its byte-identical repeat
  flip_order       share of items correct at first presentation but wrong in >=1 other ordering (repeat 1)
  retention        share of items correct at first presentation that stay correct in all 7 others
  fail_first       share of items wrong at first presentation
  fail_any         share of items wrong in >=1 of 8 presentations
  fail_growth      (fail_any - fail_first) / fail_first   [Song et al. 2026 style]
  always_wrong     share of items wrong in all 8

Bootstrap: 90% percentile intervals over items, 10,000 resamples, seed 20261009.
"""
import argparse, glob, json, os, random
from collections import defaultdict

ARMS = {"jev":"Jev 1.13","jev114":"Jev 1.14","decisions":"OpenAI Decisions","clef-flash":"Clef-flash",
        "msd1":"Microsoft-Decision-1","subq":"SubQ Snap","rune":"Rune","official":"Jev 1.14 (official prompt)","official113":"Jev 1.13 (official prompt)"}

def extract_choice(raw):
    if not isinstance(raw, dict): return None
    if isinstance(raw.get("result"), dict): raw = raw["result"]
    a = raw.get("answers")
    try:
        if isinstance(a, dict): return a["evaluation"].get("choice")
        if isinstance(a, list) and a: return a[0].get("choice")
    except Exception: return None
    return None

def load(root):
    items = {json.loads(l)["key"]: json.loads(l) for l in open(os.path.join(root,"frozen/v1/items.jsonl"))}
    req = {}
    for l in open(os.path.join(root,"frozen/v1/requests.jsonl")):
        r = json.loads(l)
        if r["format"]=="choice" and r["arm"]=="haystack" and r["kind"] in ("standard","ref"):
            req[r["id"]] = r
    return items, req

def answers(root, arm, wanted):
    ans = {}
    for p in sorted(glob.glob(os.path.join(root,"runs/main",arm,"*.jsonl"))):
        for l in open(p):
            x = json.loads(l)
            if x.get("request_id") in wanted and x.get("ok"):
                ans[x["request_id"]] = extract_choice(x.get("raw"))
    return ans

def per_item(items, req, ans):
    grid = defaultdict(dict)   # item -> (ordering, repeat) -> (pick, correct_bool)
    correct_code = {}
    for rid, r in req.items():
        it = items[r["item"]]
        cc = [c["code"] for c in it["candidates"] if c.get("correct")]
        if len(cc) != 1: continue
        correct_code[r["item"]] = cc[0]
        pick = ans.get(rid)
        grid[r["item"]][(r["ordering"], r["repeat"])] = (pick, pick == cc[0])
    rows = {}
    for k, g in grid.items():
        if len(g) != 8: continue
        c = {key: v[1] for key, v in g.items()}
        p = {key: v[0] for key, v in g.items()}
        first = c[(0,1)]
        rows[k] = dict(
            acc_first=first,
            acc_mean=sum(c.values())/8,
            repeat_agree=sum(p[(o,1)]==p[(o,2)] for o in range(4))/4,
            order_agree=len({p[(o,1)] for o in range(4)})==1,
            flip_repeat=first and not c[(0,2)],
            flip_order=first and any(not c[(o,1)] for o in range(1,4)),
            retention=first and all(c.values()),
            fail_first=not first,
            fail_any=not all(c.values()),
            always_wrong=not any(c.values()),
        )
    return rows

def stats(rows, keys):
    n = len(keys); s = defaultdict(float)
    for k in keys:
        for m, v in rows[k].items(): s[m] += float(v)
    out = {m: s[m]/n for m in s}
    nfirst = sum(rows[k]["acc_first"] for k in keys) or 1
    out["flip_repeat"] = s["flip_repeat"]/nfirst
    out["flip_order"]  = s["flip_order"]/nfirst
    out["retention"]   = s["retention"]/nfirst
    out["fail_growth"] = (s["fail_any"]-s["fail_first"])/(s["fail_first"] or 1)
    return out

def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--root", default=".")
    ap.add_argument("--arms", default=",".join(ARMS))
    ap.add_argument("--resamples", type=int, default=10000)
    ap.add_argument("--seed", type=int, default=20261009)
    ap.add_argument("--out", default=None)
    a = ap.parse_args()
    items, req = load(a.root)
    cols = ["acc_first","acc_mean","repeat_agree","order_agree","flip_repeat","flip_order","retention","fail_first","fail_any","fail_growth","always_wrong"]
    lines = ["| Model | Items | " + " | ".join(cols) + " |", "|---|---:|" + "---:|"*len(cols)]
    for arm in a.arms.split(","):
        ans = answers(a.root, arm, req)
        if not ans: print(f"# {arm}: no receipts"); continue
        rows = per_item(items, req, ans); keys = list(rows)
        pt = stats(rows, keys)
        rng = random.Random(a.seed); draws = defaultdict(list)
        for _ in range(a.resamples):
            b = stats(rows, rng.choices(keys, k=len(keys)))
            for m in cols: draws[m].append(b[m])
        cells = []
        for m in cols:
            d = sorted(draws[m]); lo = d[int(0.05*a.resamples)]; hi = d[int(0.95*a.resamples)-1]
            cells.append(f"{100*pt[m]:.1f} [{100*lo:.1f}, {100*hi:.1f}]")
        lines.append(f"| {ARMS.get(arm,arm)} | {len(keys):,} | " + " | ".join(cells) + " |")
    table = "\n".join(lines); print(table)
    if a.out: open(a.out,"w").write(table+"\n")

if __name__ == "__main__":
    main()
