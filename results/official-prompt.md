---
title: "Official-prompt re-run: the anti-position-bias sentence restored"
type: analysis
run: official-prompt
created: 2026-11-08
author: Yusuke Takahashi
plan: plans/official-prompt-v1.md
data: runs/official-prompt/jev113/, runs/official-prompt/jev114/ (receipts, SHA256SUMS)
script: scripts/official_prompt_rerun.py
tags: [prompt, position-bias, decision-models]
---

# Official-prompt re-run

The v1 choice prompt removed one sentence from RewardBench 2's official four-way judge prompt: "Avoid any position biases and ensure that the order in which the responses were presented does not influence your decision." (docs/prompts.md, change 1). This run re-sends the 14,920 choice/haystack requests of the frozen v1 plan with that sentence restored in its official place after "...provide a short explanation." Nothing else changes: the rebuild of the unmodified bodies matches all 14,920 frozen SHA-256 hashes. The plan and endpoints were frozen before any live request. Arms: jev-1.14.0 and jev-1.13.0 (pinned; both returned as requested), TypeSafe public API, 8 workers. Every request answered on the first attempt. List-price cost USD 1.42 per arm.

## Results (paired with the v1 arm of the same model, same items)

| | Jev 1.14 v1 | Jev 1.14 official | Jev 1.13 v1 | Jev 1.13 official |
|---|---:|---:|---:|---:|
| Correct chosen, slot 1 . 2 . 3 . 4 (%) | 80.5 . 83.3 . 80.6 . 81.6 | 76.1 . 79.0 . 76.5 . 77.2 | 81.0 . 83.5 . 78.0 . 81.1 | 77.0 . 79.2 . 74.0 . 76.7 |
| P1 choice primacy, slot 1 - middle (pp) | -1.7 | -1.7 [-2.6, -0.7] | +0.2 | +0.4 [-0.6, +1.4] |
| P2 choice recency, slot 4 - middle (pp) | -0.5 | -0.5 [-1.3, +0.4] | +0.2 | +0.1 [-0.7, +1.0] |
| Slot 2 - slot 3 (pp) | +2.7 [+1.7, +3.7] | +2.5 [+1.5, +3.4] | +5.5 [+4.3, +6.6] | +5.3 [+4.2, +6.3] |
| Paired change in slot 2 - slot 3 (pp) | | -0.2 [-0.7, +0.3] | | -0.2 [-0.8, +0.3] |
| Pick changed on one reordering (%) | 9.9 | 9.9 | 10.3 | 10.3 |
| Lost to reorder (% of first-presentation successes) | 10.4 | 10.3 | 11.3 | 11.1 |
| Pick changed with margin >= 0.6 (%) | 0.9 | 0.9 | 1.8 | 1.8 |
| Accuracy, all 8 presentations (%) | 81.6 | 77.1 | 81.0 | 76.6 |
| Paired change in accuracy (pp) | | -4.3 [-5.0, -3.6] | | -4.2 [-4.9, -3.5] |
| Verdict agreement with v1 arm (%) | | 92.7 | | 92.9 |

90% percentile intervals from a cluster bootstrap over items (10,000 resamples, seed 20261009).

## Reading

- The sentence does not change the position pattern or the item-level order sensitivity of either Jev version. Under the frozen verdict rule both official-prompt arms are order-blind.
- It lowers accuracy by about 4 pp on the same items, in both versions, with the two arms agreeing on about 93% of individual verdicts.

## Limits

Choice format only; two arms of one provider. The other v1 providers accept the same body unchanged (`scripts/official_prompt_rerun.py --provider rune|msd1|subq|clef-flash`) and were not run here.
