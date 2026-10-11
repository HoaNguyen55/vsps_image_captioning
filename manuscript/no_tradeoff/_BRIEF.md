# Brief: methods that raise recall WITHOUT losing precision/F1 (Pareto, no trade-off)

## Context (read first)
Project VSPS: Vietnamese image captioning on KTVIC (UIT). Pipeline: Qwen2.5-VL-7B proposes typed
propositions -> Vintern-1B verifies each (3-state SUPPORTED/UNCERTAIN/REJECTED) -> selected SUPPORTED
props rendered by templates -> QLoRA SFT of Qwen2.5-VL-7B on those captions -> single-pass captioner.
Problem in the previous paper: the SFT model is more precise than zero-shot but recalls fewer objects,
so object F1 trails zero-shot (KTVIC test, object P/R/F1: VSPS 41.5/36.7/39.0, v2 38.1/42.2/40.1,
zero-shot Qwen2.5-VL-7B 31.6/57.1/40.7). Recall is lost (a) at verification (~41% entities UNCERTAIN
under untuned thresholds), (b) at proposal (entity cap 8), (c) in template rendering.
The user wants a direction that has NO precision<->recall trade-off versus the previous paper:
recall up AND precision not down (Pareto-dominant), so F1 strictly beats both old VSPS and zero-shot.

Existing literature notes, do NOT redo, only extend:
.paper_work/research_wall/01_hallucination_mitigation_sota.md, 03_grounding_for_recall.md,
06_verifier_precision.md, 07_rl_verifiable_rewards.md, 09_synthetic_data_engines.md.

## What to deliver
A markdown report at the path given in your task. For each method:
- full citation, venue + year, and a working link (arXiv abs / CVF / ACL Anthology / OpenReview / official GitHub);
- the exact numbers showing BOTH a precision-side metric (CHAIR_s/CHAIR_i, AMBER CHAIR, Object HalBench
  response/mention rate, FaithScore...) AND a recall/coverage-side metric (AMBER Cover, recall,
  object coverage, CAPTURE, detail score, caption length/#objects) improving or staying equal at once,
  with the baseline they compare to; copy numbers from the paper's tables, cite table number;
- whether code/weights exist; GPU cost; whether it applies to a 7B VLM on one RTX 3090 (24 GB);
- how it maps onto the VSPS pipeline stage (proposal, verification, rendering, training, decoding);
- a "trade-off check": does the paper itself show any loss (length, recall, general benchmarks)? Say so.

Rank by: evidence of Pareto improvement (both sides measured) > feasibility on 1x3090 > novelty vs VSPS.
Prefer 2024-2026 peer-reviewed venues (CVPR, ICCV, ECCV, NeurIPS, ICLR, ICML, ACL, EMNLP, NAACL, AAAI,
TPAMI, TMM, TIP) or arXiv papers with released code. Mark anything you could not verify as UNVERIFIED.
Never invent numbers; if a table is not accessible, say so.

## Hard rules
- PRIVACY: never put any email address, name or personal data of the user in any request
  (no mailto= parameters, no email in User-Agent, no form submissions).
- Read-only on the repo except your one output file. Do not run git commands. No GPU / ssh.
- Keep the report under ~2,500 words; end with a 5-line "Top picks for VSPS" list.
