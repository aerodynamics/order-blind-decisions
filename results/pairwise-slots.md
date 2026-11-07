---
title: "Pairwise slot contrasts in the choice arm"
type: analysis
run: main
created: 2026-11-07
author: Yusuke Takahashi
data: runs/main/ (receipts), frozen/v1/ (plan)
script: scripts/pairwise_slots.py
tags: [primacy, recency, serial-position, position-bias, decision-models]
---

# Pairwise slot contrasts in the choice arm

The preregistered endpoints compare slot 1 and slot 4 with the pooled middle (slots 2 and 3). Pooling the middle hides any difference between slots 2 and 3. This note reports all six pairwise slot differences for the seven model arms, computed from the committed receipts with the same resampling as the main analysis.

## Method

- **Data.** Haystack arm, choice format, items with exactly one correct response (`standard` and `ref`; 1,814 items), both repeats and all four Williams orderings pooled. Same selection as endpoints P1 and P2.
- **Outcome.** Share of requests in which the correct response is chosen, by the slot it occupied.
- **Intervals.** 90% percentile intervals from a cluster bootstrap over items, 10,000 resamples, seed `20261009`.
- **Reference line.** The preregistered ±3 pp margin is used only as a reading aid. **Bold** marks intervals that lie entirely outside ±3 pp. No verdict is attached: these are secondary, descriptive contrasts, not corrected for multiple comparisons.
- **Reproduce.** `python3 scripts/pairwise_slots.py --out results/pairwise-slots.md` from the repository root, after `runs/` is present. Standard library only; about 90 s.

## Results

| Model | Items | Correct chosen, slot 1 · 2 · 3 · 4 | 1 − 2 | 1 − 3 | 1 − 4 | 2 − 3 | 2 − 4 | 3 − 4 |
|---|---:|---|---|---|---|---|---|---|
| Jev 1.13 | 1,814 | 81.0 · 83.5 · 78.0 · 81.1% | -2.5 [-3.7, -1.4] | +3.0 [+1.7, +4.2] | -0.1 [-1.4, +1.2] | **+5.5 [+4.3, +6.6]** | +2.4 [+1.3, +3.5] | -3.1 [-4.1, -2.0] |
| Jev 1.14 | 1,814 | 80.5 · 83.3 · 80.6 · 81.6% | -2.8 [-3.8, -1.7] | -0.1 [-1.3, +1.1] | -1.1 [-2.3, +0.2] | +2.7 [+1.7, +3.7] | +1.7 [+0.7, +2.8] | -1.0 [-2.1, +0.1] |
| OpenAI Decisions | 1,814 | 83.1 · 75.8 · 78.8 · 75.9% | **+7.3 [+5.8, +8.9]** | +4.3 [+2.8, +5.9] | **+7.2 [+5.5, +8.9]** | -3.0 [-4.5, -1.5] | -0.1 [-1.6, +1.4] | +2.9 [+1.5, +4.2] |
| Clef-flash | 1,814 | 60.6 · 65.0 · 60.2 · 64.9% | -4.4 [-6.0, -2.8] | +0.4 [-1.2, +1.9] | -4.3 [-5.9, -2.6] | **+4.8 [+3.3, +6.2]** | +0.1 [-1.2, +1.4] | **-4.6 [-6.0, -3.3]** |
| Microsoft-Decision-1 | 1,814 | 72.1 · 74.0 · 67.9 · 66.3% | -1.9 [-3.3, -0.6] | +4.2 [+2.8, +5.7] | **+5.8 [+4.2, +7.4]** | **+6.2 [+4.8, +7.6]** | **+7.7 [+6.3, +9.1]** | +1.5 [+0.3, +2.8] |
| SubQ Snap | 1,814 | 83.9 · 77.1 · 76.5 · 77.1% | **+6.8 [+5.6, +7.9]** | **+7.4 [+6.3, +8.6]** | **+6.8 [+5.6, +8.0]** | +0.6 [-0.5, +1.8] | +0.0 [-1.0, +1.0] | -0.6 [-1.7, +0.5] |
| Rune | 1,814 | 74.1 · 70.4 · 67.9 · 67.1% | +3.6 [+2.3, +5.0] | **+6.1 [+4.8, +7.5]** | **+7.0 [+5.5, +8.4]** | +2.5 [+1.2, +3.9] | +3.3 [+2.0, +4.7] | +0.8 [-0.4, +2.0] |

Values are percentage points, slot *i* minus slot *j*, with 90% intervals in brackets. The slot shares differ from the main report's slot table by at most 0.2 pp, from receipt handling.

## Reading

- **Jev 1.13.** The slot-1 and slot-4 contrasts against the pooled middle are near zero, as the main report states. Between the middle slots, however, slot 2 is chosen correctly 5.5 pp more often than slot 3 [+4.3, +6.6], and slot 2 exceeds every other slot. The curve is a zigzag (2 and 4 above 1 and 3), not a flat line.
- **Jev 1.14.** The same contrast is about half as large, +2.7 pp [+1.7, +3.7], and the other pairwise differences are within ±3 pp. The curve is close to flat.
- **Clef-flash** shows the same zigzag as Jev 1.13: slots 2 and 4 above 1 and 3, with 2 − 3 at +4.8 pp and 3 − 4 at −4.6 pp.
- **OpenAI Decisions and SubQ Snap** are raised at slot 1 only; their three slot-1 contrasts are all positive and the remaining contrasts are small. This is the pattern the preregistered primacy endpoint is built to detect.
- **Rune and Microsoft-Decision-1** decline across slots. Rune's decline is roughly monotone (slot 1 highest, slot 4 lowest). Microsoft-Decision-1's first two slots sit together above the last two.

Three shapes therefore appear in the same data: a first-slot preference, a monotone decline, and a zigzag. The preregistered endpoints detect the first two. The zigzag cancels in a slot-1-versus-middle or slot-4-versus-middle comparison and is visible only in the pairwise contrasts.

## Relation to the frozen verdict

The frozen verdict rule is unchanged by this note. Both Jev versions pass it. The pairwise contrasts show that passing it does not imply equal treatment of every slot; for Jev 1.13 the slot 2 − slot 3 difference exceeds the margin that the rule applies to the other contrasts. An independent audit of Jev 1.13 on pairwise comparisons (Agrawal and Mamidi, [arXiv:2611.06384](https://arxiv.org/abs/2611.06384)) reports a second-position preference across three tasks, up to 6.11 pp on summaries, consistent with the slot-2 effect here.

## Limits

- Secondary and descriptive; six contrasts per arm with no multiple-comparison correction.
- Choice format only. The rubric formats are not analyzed here.
- The Williams square balances which response occupies each slot, so the contrasts are not confounded with response identity, but they share the main study's limits (one benchmark, K = 4, adapted prompts).
