# A-T3: one-judge reads required by CC-183 W11 (coordinator runs the judge; nothing is spawned from here)

Two separate reads, one judge each, reversible tier (bar 90). Tier 1 does not start until both are GO and the
prereg is finalised (PREREG §9). Each read gives a verdict and a list of fixes. Give the judge the files, not this
author's conclusions.

## Read 1: the Gemma-3 / Aya decode path

There is no new decoder. Gemma-3 and Aya decode through the unchanged harness, and the read checks that this is
safe.

**Files (sha256 at writing):**

- `scripts/a_t3/a_t3.py`: functions `register`, `registry`, `build_registry`, `in_models`, `guard`, `stage`,
  `coco_url`, `valsha_set`, `bad_names`.
- `scripts/a_t3/a_t3_job.sh`.
- `scripts/lb/decode_hf_vlm.py` (e2de1881, pinned, unchanged): `load`, `make_generate`, `decode_run`,
  `check_snapshot`.
- `manuscript/prereg/2026-10-29_l1b/l1b_registry.json` (cd210a7c), key `models.gemma3_4b`.
- `manuscript/prereg/2026-10-30_c_t1/c_t1_registry.json` (09e6f90a), key `models.aya_vision_8b`.

**Questions:**

1. With venv-lb (transformers 4.57.6), do `AutoProcessor` and `AutoModelForImageTextToText` load Gemma-3-4B-it and
   Aya-Vision-8B at the pinned revisions with `trust_remote_code=False`?
   - Does left padding plus `apply_chat_template` (one image + text per conversation, `padding=True`) batch
     correctly at the registered batch sizes (gemma 8, aya 2)?
   - Is the "first EOS" cut right for both? Check that the eos_token_id lists in their generation_config.json are
     respected.
2. Is any model-specific setting silently left at a default that differs from A-N2's treatment of the other
   families? Examples: Gemma pan-and-scan off, Aya tiling, bf16.
3. Gemma rule (PREREG §4). It is in only if `G3_gemma` and its 4 null hashes are filled before finalisation;
   otherwise it is out for all tiers. Is this enforced by `pins_complete` / `in_models`, and is a late fill
   impossible? Note that SOURCES pins the l1b registry sha.
4. Aya drop/move rule (§4). Is it fully pre-written? Specifically:
   - the job never fetches a gated model;
   - the M1 run uses the m3 branch of `guard`, which scans only the A-T3 staging dir.
5. Guard (W8):
   - m4 refuses val2017 ids, file names and annotation names anywhere under `$NCS_DATA/datasets`, and val2017
     shas in the A-T3 staging dir;
   - it fails closed without the m3-made sha list.

   Is the id-only scan outside the staging dir acceptable? `stage` fetches only from `train2017/`.
6. Can the job's cap/ledger/lock logic leave a decode unrecorded or double-counted? Compare with A-T1's job.

## Read 2: the A registry (`a_t3_registry.json`)

**Files:**

- `manuscript/prereg/2026-10-30_a_t3/a_t3_registry.json` (built by `a_t3.py registry`, checked by
  `registry --check`).
- Sources:
  - `manuscript/prereg/2026-10-19_a_n2_lvlm_gold_ladder.json` (d5714e2b);
  - the l1b registry (cd210a7c);
  - the c_t1 registry (09e6f90a).
- `PREREG.md` §4 (table, Gemma rule, Aya rule, model-set rule).

**Questions:**

1. Is each model block identical to its source, and is each revision the CC-183 W10 pin? The pins are InternVL3
   259a3b64, LLaVA-OV 0d506805, Idefics3 fddb4ff7, Gemma-3 093f9f38 and Aya d7601ac8.
2. Families. Check the LLM family of each model against the model cards or config.json at the pin: Qwen2.5, Qwen2,
   Llama-3.1, Gemma 3, Command R7B. The vision encoders are marked "verify at pin": confirm or correct them. Is
   "families outside A's main Qwen-VL set; two of the five LLMs are Qwen-family" accurate wording?
3. With Gemma out today, the in-set is 4 models / 8 runs. Is ≥ 3 models (p50.MIN_MODELS) still the right floor for
   a slope across runs?
4. Is the model set fixed before tier 1, and identical across tiers, with no outcome-dependent path in? Look in
   particular at the tier-1 score that waits for Aya.

5. **Deviation (PREREG §1).** r7 puts the W2 near-dup drops on the dev side. This draft drops dev↔test
   near-duplicates from the test side, so that D1/D2 are final before M2 expires. Accept or reject. If rejected,
   `neardup` runs dev-side on m3 before `stage`.

**Also, optional for either read:** the D1 premise margin (2.098 vs 2) and whether N_TEST_PLAN = 3,500 is a sound
fixed planning bound.
