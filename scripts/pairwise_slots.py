#!/usr/bin/env python3
"""Pairwise slot contrasts for the order-blind v1 choice arm.

Reads the frozen plan (frozen/v1) and the committed receipts (runs/main)
and reports, for every model arm, the share of correct picks by slot and
all six pairwise slot differences with cluster-bootstrap intervals over
items. It uses the same resampling as the preregistered analysis:
10,000 resamples, seed 20261009, percentile 90% intervals, items with
exactly one correct response (``standard`` and ``ref``), haystack arm,
choice format, both repeats and all four orderings pooled.

The preregistered endpoints compare slot 1 and slot 4 with the pooled
middle (slots 2 and 3). This script adds the contrasts that pooling
hides, in particular slot 2 minus slot 3.

Usage:
    python3 scripts/pairwise_slots.py [--arms jev,jev114,...] [--resamples N] [--out results/pairwise-slots.md]

Only the standard library is used.
"""
import argparse
import glob
import json
import os
import random
from collections import defaultdict

ARMS = {
    "jev": "Jev 1.13",
    "jev114": "Jev 1.14",
    "decisions": "OpenAI Decisions",
    "clef-flash": "Clef-flash",
    "msd1": "Microsoft-Decision-1",
    "subq": "SubQ Snap",
    "rune": "Rune",
}
PAIRS = [(0, 1), (0, 2), (0, 3), (1, 2), (1, 3), (2, 3)]


def load_items(root):
    items = {}
    with open(os.path.join(root, "frozen/v1/items.jsonl")) as f:
        for line in f:
            it = json.loads(line)
            items[it["key"]] = it
    return items


def load_requests(root):
    req = {}
    with open(os.path.join(root, "frozen/v1/requests.jsonl")) as f:
        for line in f:
            r = json.loads(line)
            if r["format"] == "choice" and r["arm"] == "haystack" and r["kind"] in ("standard", "ref"):
                req[r["id"]] = r
    return req


def extract_choice(raw):
    if not isinstance(raw, dict):
        return None
    if "result" in raw and isinstance(raw["result"], dict):
        raw = raw["result"]
    answers = raw.get("answers")
    try:
        if isinstance(answers, dict):
            return answers["evaluation"].get("choice")
        if isinstance(answers, list) and answers:
            return answers[0].get("choice")
    except (KeyError, AttributeError, TypeError):
        return None
    return None


def load_answers(root, arm, wanted):
    ans = {}
    for path in sorted(glob.glob(os.path.join(root, "runs/main", arm, "*.jsonl"))):
        with open(path) as f:
            for line in f:
                x = json.loads(line)
                rid = x.get("request_id")
                if rid in wanted and x.get("ok"):
                    ans[rid] = extract_choice(x.get("raw"))
    return ans


def per_item_counts(items, req, ans):
    per = defaultdict(lambda: [[0, 0] for _ in range(4)])
    for rid, r in req.items():
        it = items[r["item"]]
        correct = [c["code"] for c in it["candidates"] if c.get("correct")]
        if len(correct) != 1:
            continue
        slot = r["state_order"].index(correct[0])
        cell = per[r["item"]][slot]
        cell[0] += int(ans.get(rid) == correct[0])
        cell[1] += 1
    return per


def slot_rates(per, keys):
    tot = [[0, 0] for _ in range(4)]
    for k in keys:
        for s in range(4):
            tot[s][0] += per[k][s][0]
            tot[s][1] += per[k][s][1]
    return [t[0] / t[1] if t[1] else float("nan") for t in tot]


def bootstrap(per, resamples, seed):
    keys = list(per)
    point = slot_rates(per, keys)
    rng = random.Random(seed)
    draws = {p: [] for p in PAIRS}
    for _ in range(resamples):
        sample = rng.choices(keys, k=len(keys))
        rates = slot_rates(per, sample)
        for i, j in PAIRS:
            draws[(i, j)].append(rates[i] - rates[j])
    out = {}
    for p, d in draws.items():
        d.sort()
        lo = d[int(0.05 * resamples)]
        hi = d[int(0.95 * resamples) - 1]
        out[p] = (point[p[0]] - point[p[1]], lo, hi)
    return point, out, len(keys)


def fmt_pp(x):
    return f"{100 * x:+.1f}"


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--root", default=".")
    ap.add_argument("--arms", default=",".join(ARMS))
    ap.add_argument("--resamples", type=int, default=10000)
    ap.add_argument("--seed", type=int, default=20261009)
    ap.add_argument("--out", default=None)
    args = ap.parse_args()

    items = load_items(args.root)
    req = load_requests(args.root)
    rows = []
    for arm in args.arms.split(","):
        ans = load_answers(args.root, arm, req)
        if not ans:
            print(f"# {arm}: no receipts found, skipped")
            continue
        per = per_item_counts(items, req, ans)
        point, ci, n = bootstrap(per, args.resamples, args.seed)
        rows.append((arm, ARMS.get(arm, arm), n, point, ci))

    lines = []
    lines.append("| Model | Items | Correct chosen, slot 1 · 2 · 3 · 4 | 1 − 2 | 1 − 3 | 1 − 4 | 2 − 3 | 2 − 4 | 3 − 4 |")
    lines.append("|---|---:|---|---|---|---|---|---|---|")
    for arm, label, n, point, ci in rows:
        slots = " · ".join(f"{100 * p:.1f}" for p in point) + "%"
        cells = []
        for p in PAIRS:
            est, lo, hi = ci[p]
            cell = f"{fmt_pp(est)} [{fmt_pp(lo)}, {fmt_pp(hi)}]"
            if lo > 0.03 or hi < -0.03:
                cell = f"**{cell}**"
            cells.append(cell)
        lines.append(f"| {label} | {n:,} | {slots} | " + " | ".join(cells) + " |")
    table = "\n".join(lines)
    print(table)
    if args.out:
        with open(args.out, "w") as f:
            f.write(table + "\n")


if __name__ == "__main__":
    main()
