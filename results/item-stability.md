---
title: "Item-level stability of choice verdicts"
type: analysis
run: main
created: 2026-11-08
author: Yusuke Takahashi
data: runs/main/ (receipts), frozen/v1/ (plan)
scripts: scripts/retention.py, scripts/mcnemar_kyle.py, scripts/margin_strata.py
tags: [position-bias, retention, repeatability, decision-models]
---

# Item-level stability of choice verdicts

The slot tables average over presentations. This note reads the same receipts one item at a time: haystack arm, choice format, 1,814 items with one correct response, 4 Williams orderings x 2 byte-identical repeats = 8 presentations per item. 90% percentile intervals from a cluster bootstrap over items, 10,000 resamples, seed 20261009.

## Repeat agreement, order agreement, retention

Columns (item-level, %): accuracy at the first presentation (ordering 0, repeat 1); mean accuracy over all 8; share of ordering pairs where the two repeats pick the same response; share of items with the same pick in all 4 orderings; first-presentation successes lost at the identical repeat / in >=1 other ordering; retention (first-presentation successes correct in all 7 others); items wrong at first / wrong at least once; relative growth of that failure set; items wrong in all 8.

| Model | Items | acc_first | acc_mean | repeat_agree | order_agree | flip_repeat | flip_order | retention | fail_first | fail_any | fail_growth | always_wrong |
|---|---:|---:|---:|---:|---:|---:|---:|---:|---:|---:|---:|---:|
| Jev 1.13 | 1,814 | 81.1 [79.6, 82.6] | 81.0 [79.7, 82.3] | 97.9 [97.6, 98.2] | 80.6 [79.1, 82.1] | 1.4 [0.9, 1.9] | 11.3 [10.0, 12.7] | 87.2 [85.8, 88.7] | 18.9 [17.4, 20.4] | 29.2 [27.5, 31.0] | 55.0 [47.2, 63.8] | 10.3 [9.1, 11.5] |
| Jev 1.14 | 1,814 | 81.5 [80.0, 83.0] | 81.6 [80.2, 82.9] | 97.5 [97.2, 97.9] | 81.5 [80.0, 83.0] | 0.9 [0.5, 1.4] | 10.4 [9.1, 11.7] | 88.0 [86.6, 89.4] | 18.5 [17.0, 20.0] | 28.3 [26.5, 30.0] | 52.7 [45.1, 61.2] | 10.4 [9.2, 11.6] |
| OpenAI Decisions | 1,814 | 78.1 [76.5, 79.7] | 78.4 [77.1, 79.7] | 100.0 [100.0, 100.0] | 66.9 [65.0, 68.7] | 0.0 [0.0, 0.0] | 18.9 [17.2, 20.6] | 81.1 [79.4, 82.8] | 21.9 [20.3, 23.5] | 36.7 [34.8, 38.5] | 67.5 [59.2, 76.9] | 8.2 [7.1, 9.2] |
| Clef-flash | 1,814 | 63.1 [61.2, 64.9] | 62.9 [61.3, 64.6] | 98.6 [98.4, 98.8] | 64.8 [63.0, 66.6] | 0.6 [0.3, 1.0] | 20.8 [18.8, 22.8] | 78.4 [76.4, 80.4] | 36.9 [35.1, 38.8] | 50.6 [48.6, 52.5] | 36.9 [32.6, 41.6] | 23.8 [22.2, 25.5] |
| Microsoft-Decision-1 | 1,814 | 70.7 [69.0, 72.4] | 70.4 [68.9, 71.9] | 97.8 [97.5, 98.1] | 69.1 [67.3, 70.8] | 1.2 [0.7, 1.7] | 18.2 [16.5, 20.0] | 80.8 [79.0, 82.6] | 29.3 [27.6, 31.0] | 42.8 [40.9, 44.7] | 46.3 [40.7, 52.4] | 17.0 [15.5, 18.5] |
| SubQ Snap | 1,814 | 79.1 [77.5, 80.7] | 78.8 [77.3, 80.2] | 100.0 [100.0, 100.0] | 79.3 [77.7, 80.9] | 0.0 [0.0, 0.0] | 11.1 [9.7, 12.4] | 88.9 [87.6, 90.3] | 20.9 [19.3, 22.5] | 29.7 [27.9, 31.4] | 42.0 [35.7, 48.7] | 13.7 [12.5, 15.0] |
| Rune | 1,814 | 69.5 [67.7, 71.3] | 69.9 [68.3, 71.4] | 97.1 [96.7, 97.5] | 69.2 [67.4, 71.0] | 1.3 [0.9, 1.9] | 17.8 [16.0, 19.5] | 81.0 [79.2, 82.8] | 30.5 [28.7, 32.3] | 43.7 [41.8, 45.6] | 43.4 [38.1, 49.1] | 17.7 [16.2, 19.2] |

Mean accuracy is within 0.3 pp of first-presentation accuracy for every arm, while 18-33% of items receive a different pick in at least one ordering. The two deterministic arms (OpenAI Decisions, SubQ Snap) have 100% repeat agreement and still change their pick across orderings on 33% and 21% of items.

## Reordering versus resending (McNemar)

Paired on items: pick at (ordering 0, repeat 1) versus the identical repeat, and versus one other ordering (ordering 1, repeat 1). McNemar exact test on the discordant counts; Holm correction across the seven arms. Right-hand columns restrict to items correct at the first presentation.

| Model | Items | Pick changed on repeat | Pick changed on one reordering | McNemar b/c | p (Holm) | Items correct first | Lost on repeat | Lost on one reordering | b/c | p (Holm) |
|---|---:|---:|---:|---:|---:|---:|---:|---:|---:|---:|
| Jev 1.13 | 1,814 | 2.2% | 10.3% | 171/25 | 6.1e-28 | 1,472 | 1.4% | 5.2% | 71/15 | 7.1e-10 |
| Jev 1.14 | 1,814 | 2.3% | 9.9% | 154/16 | 3.3e-29 | 1,478 | 0.9% | 5.0% | 66/6 | 1.5e-13 |
| OpenAI Decisions | 1,814 | 0.0% | 21.0% | 381/0 | 2.8e-114 | 1,417 | 0.0% | 10.0% | 142/0 | 2.5e-42 |
| Clef-flash | 1,814 | 1.5% | 20.3% | 354/12 | 8.3e-88 | 1,144 | 0.6% | 12.1% | 134/3 | 3e-35 |
| Microsoft-Decision-1 | 1,814 | 2.3% | 18.5% | 311/17 | 2.1e-70 | 1,283 | 1.2% | 9.8% | 119/8 | 8.4e-26 |
| SubQ Snap | 1,814 | 0.0% | 12.2% | 221/0 | 2.4e-66 | 1,435 | 0.0% | 6.0% | 86/0 | 1e-25 |
| Rune | 1,814 | 3.1% | 17.5% | 284/24 | 4.3e-57 | 1,261 | 1.3% | 9.2% | 107/8 | 9.2e-23 |

## Order changes by probability margin

Items binned by the margin between the top two probabilities at the first presentation. Per band: n, share whose pick changes in >=1 of the other three orderings (repeat 1), share whose pick changes on the identical repeat.

| Model | margin 0.0–0.1: n / reorder change / repeat change | margin 0.1–0.3: n / reorder change / repeat change | margin 0.3–0.6: n / reorder change / repeat change | margin 0.6–1.0: n / reorder change / repeat change |
|---|---|---|---|---|
| Jev 1.13 | 156 / 72.4% / 23.1% | 307 / 48.5% / 1.3% | 368 / 19.6% / 0.0% | 983 / 1.8% / 0.0% |
| Jev 1.14 | 188 / 70.7% / 20.2% | 298 / 44.6% / 1.0% | 366 / 16.4% / 0.0% | 962 / 0.9% / 0.0% |
| OpenAI Decisions | 101 / 89.1% / 0.0% | 165 / 78.8% / 0.0% | 236 / 66.5% / 0.0% | 1285 / 15.7% / 0.0% |
| Clef-flash | 134 / 80.6% / 5.2% | 225 / 76.0% / 6.2% | 435 / 52.9% / 1.1% | 1020 / 12.7% / 0.1% |
| Microsoft-Decision-1 | 133 / 83.5% / 21.1% | 222 / 67.1% / 4.1% | 371 / 49.6% / 1.1% | 1088 / 10.8% / 0.1% |
| SubQ Snap | 127 / 72.4% / 0.0% | 232 / 60.8% / 0.0% | 415 / 26.7% / 0.0% | 1040 / 3.1% / 0.0% |
| Rune | 71 / 87.3% / 40.8% | 127 / 79.5% / 16.5% | 224 / 67.9% / 3.1% | 1392 / 17.5% / 0.0% |

## Limits

Secondary and descriptive except where a test is named. Choice format only. The frozen verdict rule is unchanged.
