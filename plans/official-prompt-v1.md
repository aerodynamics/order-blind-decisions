---
title: "Official-prompt re-run (prompt-restoration check)"
type: plan
status: frozen 2026-11-08 before any live request
author: Yusuke Takahashi
script: scripts/official_prompt_rerun.py
---

# Official-prompt re-run

**Question.** Does the slot-2 preference and the item-level order sensitivity of Jev survive when the one
sentence removed from RewardBench 2's official four-way prompt is restored?

**Change.** Exactly one: the sentence "Avoid any position biases and ensure that the order in which the
responses were presented does not influence your decision." is reinserted after "...provide a short
explanation.", where RewardBench 2 and MT-Bench place it. Everything else is the frozen v1 choice/haystack
plan (1,814 standard + ref items, 4 Williams orderings x 2 byte-identical repeats = 14,920 requests). The
rebuild of the unmodified bodies matches all 14,920 frozen SHA-256 hashes.

**Models.** jev-1.14.0 (pinned) and jev-1.13.0 via TypeSafe; Rune via Fireworks; Microsoft-Decision-1 via OpenRouter; SubQ Snap; Clef-flash via Cloudflare Workers AI. All take the Jev-shaped body unchanged. OpenAI Decisions is deferred (body adapter).

**Endpoints (fixed before the run).**
1. Preregistered P1/P2 (slot 1 - middle, slot 4 - middle) with the v1 +-3 pp rule and 90% item bootstrap.
2. Pairwise slot contrasts; the slot 2 - slot 3 contrast is the primary secondary endpoint.
3. Item-level: order agreement, lost-to-reorder vs lost-to-repeat, McNemar exact test.
4. Paired comparison with the v1 arm of the same model on the same items: difference in slot 2 - slot 3
   and in lost-to-reorder, 90% item bootstrap.

**Prediction.** The sentence changes the slot 2 - slot 3 contrast and the reorder-change rate by less than
the v1 repeat noise; if it removes them, the paper reports that the v1 effects were prompt-dependent.

**Budget.** USD 5 cap in the runner; expected about USD 1.5 per model.
