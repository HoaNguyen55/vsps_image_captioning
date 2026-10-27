# K2 Gate 0/0b dev pilot rule: the target ceiling of gold-edited self-distillation (CC-119 ruling 4)

**Status: DRAFT, not committed.** Written 2026-10-27. No output of this pilot exists. No GPU was used, and no caption, prediction or test file was opened. Before any output, the judge panel reads this rule and `scripts/grl/k2_gate0.{py,sh}`, and the gatekeeper commits them. `EXPECT_HEAD` in `k2_gate0.sh` is that commit.

**What this measures.** Gate 0 asks whether the K2 target exists on dev: if val gold edits the zero-shot captions, how far does CHAIR_i fall, and how much recall and length survive? Val gold edits val captions, so **the numbers are a ceiling of the target only. They are never reported as a method result** (CC-119 ruling 4). K2 Gate 1 stays HELD until W9–W13 and W19–W23 are committed (ruling 5). The name "G-VSPS" is dropped (W23); the method is K2, gold-edited self-distillation, citing FAIR as prior work.

Sibling: `PILOT_RULE.md` (G-RL). Shared code: `common.py` (guard, isolation, staging, gold, id lists) and `reward.py` (matchers, negation/hedge rules).

## 1. Authority

| Source | What it fixes |
|---|---|
| CC-119 ruling 4, W1–W8, W19–W21 | this pilot: val 924 only, the frozen SESOIs, the STOP conditions, the M3 hygiene and the disclosures |
| CC-119 ruling 8 (PD-GR-3) | on M3: K2 Gate 0/0b first, then K2 Gate 1 when approved, then the G-RL pilot (`gate0.sh` and `gate1.sh` check this) |
| PI-1026r(3), PI-1026s | the first CC-119-approved pilot runs on M3 now; date-only gates do not bind (CC-118 r2/r3 are amended for this pilot) |
| PI-1026aa | Q5 YES: the backbone's own gold-edited captions may be K2 training text (training data, never evidence, no MT COCO); Q6: M4 only after a Gate 1 GO |
| CC-124 r2, W1, W2, W8 | 5 GPU-h ceiling (amends CC-119 r4); cost NOT-RUN is never a negative pilot; tmux + lock + m3_clear controls; operator order |
| PI-1026u | Q1: K1/K2/K6 and G-RL are one MT4 paper; KV-4,224 is its one-look test. Q2: the Gate-1 pool is 2,402. Q4: K1+K6 is the registered primary, and K2 is promoted only on a Gate-1 GO. Q7: G1′ on OIV7 val is the fallback |

## 2. Frozen now (W1, W3, W4, W5, W21)

| Item | Value |
|---|---|
| SESOIs (W1) | **CHAIR_i −3.0**, **recall margin −2.0**. PROPOSAL l.101's `min(3.0, 0.5 × gain)` is struck. No SESOI moves after Gate 0 |
| Model | Qwen/Qwen3-VL-8B-Instruct @ 0c351dd, the 14 snapshot files pinned by the B-N1 registration (sha 9ff02dc2), at `/root/ncs-data/models/Qwen3-VL-8B-Instruct-0c351dd`; bf16, sdpa, batch 4, `min_pixels` 262,144, `max_pixels` 1,048,576 |
| Decoder | `scripts/lb/decode_hf_vlm.py` unchanged (sha e2de1881, B-N1's pin), `/root/venv-lb` (freeze 685ffe2a: torch 2.5.1+cu121, transformers 4.57.6). Greedy (`do_sample=False`, `num_beams=1`) |
| Prompt | `evaluate.py` PROMPTS["detailed"] (sha 0addb5dd), Vietnamese |
| `max_new_tokens` (W3) | frozen by the probe (§4): the smallest of 256 / 384 / 512 / 768 / 1024 that cuts < 10% of probe captions (J3's < 10% cap-hit target). The same value binds the zero-shot comparator, the teacher and the student in every later K2 stage. 160 is excluded: it cuts 99.7% (CC-119 W3) |
| Truncated final clause (W3) | on a cap-hit caption, the last unit is dropped unless it ends in . ! ? (`untruncate`), before both editing and scoring, for every row |
| Editor (W5) | units = maximal runs ending at . , ; : ! ? or a newline. A unit is deleted if it names a COCO-80 class (matcher v1: `score_coco_probe.py` d11db7e1 with `coco80_vi.json` 926e0857) absent from the image's gold, or if it fails the language check (CJK or out-of-script characters, `clean_supervision` 01f17200). A trailing , ; : becomes "." |
| Gold (W21) | one definition: COCO-2014 instance classes, i.e. `gold_instances.json` (sha 42c100f5), the G-RL reward's gold. It is used for the editor, the scorer, G1 and later KV. CHAIR_i under instances ∪ reference classes (val references, matcher v2, as B's object_prf) is reported as a diagnostic only |
| Scorer (W20) | matcher v2. A class named only in a negated or hedged unit (`reward.NEG_RE`, `clean_supervision.HEDGE_RE`) is a hallucination and never a true positive, as in `grl/reward.py`. CHAIR_i = Σ hallucinated / Σ mentioned classes (pooled, ×100); R = Σ tp / Σ |gold| (×100). Paired image bootstrap B = 2,000, `default_rng(0)` |
| Length rule (W4) | one rule everywhere: mean words ≥ 90% of zero-shot (replaces 75% and ±25%) |

## 3. Data and isolation (W6, W19)

- **Scored set:** the full UIT-ViIC val 924 (`uitviic_val.tsv`, sha 338252e1).
- **Probe set:** the first 40 UT-2,402 train ids of the seed-0 schedule, decoded at 1024 tokens for length and rate only. No val image is decoded before the freeze, and the probe captions are never scored.
- **ID and hash asserts (W19), before the val decode** (`k2_gate0.val_ids_ok`): the manifest is exactly val-924 and has
  - 0 ids in Karpathy val or test, or in any exclusion.json source;
  - 0 ids in `cen_coco_kval` / `cen_coco_test`;
  - 0 image sha256 in C-EN's three test-side records (`coco_test`, `coco_kval`, `nocaps_val`.sha256.tsv), which covers NoCaps val.

  `id_counts.py` pins the id half: val ∩ cen lists = 0, UT-2,402 ∩ cen lists = 0, and train-2,695 ∩ `cen_coco_kval` = 132 and ∩ `cen_coco_test` = 133, as the judges found.
- **PROPOSAL l.104 corrected:** "No KV image is decoded" holds for KV-4,224 only in the proposal's wording. In this design **no Karpathy-val image is decoded at all**. The 130 UT ∩ KV ids are outside the Gate-1 pool (PI-1026u Q2) and are never staged.
- **M3 isolation (W6; CC-120, CC-121; C-EN has priority).** `common.guard` runs before every GPU stage. It refuses to proceed unless all of the following hold:
  - C-EN's three test-side hash records are complete (the hash-only pass writes no bytes);
  - no protected set is staged (`$NCS_DATA/datasets/cen_{coco_test,coco_kval,nocaps_val}/` absent, i.e. C-EN's cleanup has deleted it);
  - no C-EN process is running;
  - the GPU is idle;
  - HEAD equals the commit and the tracked tree is clean;
  - no image under `/root/{outputs,queue,ncs-data,vsps}` is a test image or unidentifiable.
- **Lock and controls (CC-124 W1, ruling 3).** `k2_gate0.sh` (and the G-RL runners) refuse to start outside a tmux session (`$TMUX`), hold `/root/outputs/grl_pilot/RUNNING` for the whole run and refuse to start if it exists. The three real controls:
  - C-EN → pilot: `cen_chain.sh:42` tmux exclusivity (C-EN PREREG l.129, committed at 30514a7) refuses to start any chain-driven C-EN step (feats, stage_coco, stage_nocaps) while any tmux session exists. It binds at code level because the runners require `$TMUX`.
  - pilot → C-EN: `common.m3_clear` before every GPU stage, plus the RUNNING lock for the whole run.
  - operator: no cen_chain step and no direct `cen_fetch.py --stage` is started while RUNNING exists.

  `cen_job.sh`, `cen_chain.sh` and `cen_fetch.py` are not edited before this commit (C-EN PREREG §13). A lock check at `cen_fetch.py` `if a.stage:` (l.406, the single writer of `cen_<set>/images`) is required at the next C-EN code amendment, and in any case before any G-RL Gate 1 run while C-EN is unfinished, because Gate 1's G-RL stage lasts about 20 h and the guard runs only at stage starts.
- **Operator checklist and order (CC-124 W8, ruling 10).** Order on M3: (1) the pilot commit, M3 at `EXPECT_HEAD`; (2) a C-EN step whenever one is ready (C-EN precedence); (3) K2 Gate 0/0b (probe + val decode, one tmux run, one lock, 5 GPU-h ceiling) in the first window in which no C-EN step is running or ready to start; (4) G-RL Gate 0 at 7B after K2 is decided; (5) the W22 probe per CC-124 ruling 9; Gate 1 HELD. Before starting: M3 at `EXPECT_HEAD` with a clean tree; `memory.done.json` at 30514a7 present (recorded 112,320, refused 2); no `cen*` tmux session; `m3_clear` passes; the runner is started inside tmux; the window and the reason are logged in WORKFLOW_LOG. The C-EN test-side hash pass stored no bytes (`done.json` `stored = false`), so CC-119 r4's "test bytes deleted" is met by the records; the operative condition is `m3_clear` + the tmux rule.

## 4. Steps (`scripts/grl/k2_gate0.sh`)

1. Selftests: `common`, `reward`, `k2_gate0` and the LB decoder's own `--selftest`. Then the venv-lb freeze check, guard, staging (shared with G-RL) and guard again.
2. **Probe** (GPU): 40 UT train images at 1024 new tokens. Decoder lines are time-stamped; GPU memory is polled every second.
3. **Freeze** (CPU, `k2_gate0.py freeze`):
   - `max_new_tokens` as in §2;
   - s/img = the probe's slice-to-slice rate (model loading and the batch-1 parity pass excluded), scaled by decode steps per batch slice at the frozen value;
   - projected Gate 0 GPU-h = 924 × s/img / 3600 + 0.1 h;
   - **cap = ⌈1.2 × projected⌉ to 0.1 GPU-h**.
   - **NOT RUN (cost) → TO-PI** if no ladder value cuts < 10%, or if the cap exceeds the **5 GPU-h ceiling**. CC-124 ruling 2 amends CC-119 r4's 2 GPU-h: that figure was computed at 160 tokens (1.36 GPU-h), which CC-119 W3 forbids, and CC-119 l.55 itself says the cap comes from the probe. At 5 GPU-h the freeze admits 256 and 384 at the all-hit bound, 512 depending on the measured slice lengths, and refuses 768 and above; expected spend is about 2.5–4.5 GPU-h.
4. **Gate 0** (GPU): val 924 at the frozen value, under `timeout` = cap. A cap timeout (124) is NOT RUN (cost) → TO-PI; any other non-zero exit is NOT RUN (fault) → TO-PI; neither is a negative pilot; no rerun (CC-125 X3).
5. **Score and decide** (CPU, `k2_gate0.py score`): untruncate, edit, score both rows, apply the STOP rules.

## 5. STOP conditions (any one fires a STOP)

| | Condition (edit − zero-shot on val 924) |
|---|---|
| (a) | the edit lowers R by > 1.0 |
| (b) | the edit lowers CHAIR_i by < 5.0. PROPOSAL l.100's reason ("matcher error") is struck under W2: v1 ⊂ v2 in rules, so the gate cannot detect matcher error. The v1 = v2 agreement share is reported instead |
| (c) Gate 0b | edited mean words < 90% of zero-shot (W4) |
| (d) | **STOP-only (W1):** the ceiling (CHAIR_i drop) < 2 × SESOI = 6.0, or the bootstrap 95% half-width of ΔCHAIR_i ≥ 3.0, or that of ΔR ≥ 2.0. It can only stop; it never loosens a SESOI |
| (e) W20 | more than half of the CHAIR_i drop comes from negated or hedged mentions: 1 − (drop with unasserted mentions excluded) / (drop) > 0.5 |
| freeze (**NOT RUN, cost → TO-PI**) | no `max_new_tokens` ≤ 1024 cuts < 10%, or the cap exceeds 5 GPU-h |
| cap (**NOT RUN, cost → TO-PI**) | the val decode does not finish inside the cap (exit 124) |

**Two STOP classes (CC-124 W2).** A freeze or cap outcome is a cost artefact: `STOP.md` and `gate0_decide.json` carry `verdict: NOT-RUN`, `class: cost -> TO-PI`; it goes to the PI, is never a negative K2 pilot and never triggers the K1 + K6 fallback below. Only (a)–(e), reached on scored output, are negative pilots.

(d) binds more tightly than (b) whenever (b) alone would pass. Both stay as written.

**On a negative-pilot STOP, (a)–(e) (W8):** `STOP.md` with the measured values. No rerun, no tuned retry, no second look. G1's headline falls back to K1 + K6 (PI-1026u Q4), and the K2 rows become a disclosed negative pilot. **On NOT RUN (cost):** `STOP.md` labelled as such, the PI decides (rent time or stop); nothing is reported as a pilot result. **On GO:** the ceiling exists. That licenses only the drafting of the K2 Gate 1 rule (W9–W13, W19–W23), not a run.

## 6. Reported in `gate0_decide.json` (numbers only)

- Zero-shot and edited CHAIR_i and R.
- The diagnostics: unasserted mentions excluded, negation-blind, and union gold.
- The deltas and their bootstrap half-widths.
- The share of the drop from unasserted mentions, the number of deleted units, and the share of them that are negated or hedged (W20).
- `p1_truncation_frontier` (§6b): verdict, Gap_ceiling with CI, the frontier points, check T, matched-count F1, cap-hit share.
- CC-124 W9 diagnostic: the count of deleted units whose only gold-absent v1 class is a LEX_V2-rewritten dining-table hit (*ghi bàn / bàn thắng / bóng bàn*). The editor stays v1 (CC-119 r4).
- Mean words, Vietnamese-only share, v1 = v2 share (W2), `max_new_tokens`, cap-hit share (W3), wall s/img, peak GPU memory (W8), the freeze record, the decode sha, and the frozen SESOIs.

The label "TARGET CEILING ONLY" is written into the file.

## 6b. Registered secondary analysis P1: the truncation frontier (Ken K14 P1)

**Status.** Registered here, before any output, as a secondary analysis with its own verdict. It runs on CPU over the same val-924 zero-shot decodes and edited targets that Gate 0 produces (data labelled "shared with Gate 0 (W7)"). It changes nothing in Gate 0: not (a)–(e), not the SESOIs, not the cap or the ceiling. Source: `manuscript/ken/K14_PROPOSALS_2026-10-27.md` §P1 (l.65–123). Ken's three motivating sources are cited as he names them: *Less is More*, Fig. 5 (a truncation baseline); the attention-heads paper (recall 0.78 → 0.70); LURE (hallucinations sit late in the caption). **K14 gives no identifier for any of the three**; they go through the non-Ken identifier and claim check (CC-114 W10 pattern) before any paper cites them, and no claim here rests on them.

**Why.** G1 compares K2 with the *uncut* zero-shot at a recall margin of −2.0. A zero-shot caption cut short also loses CHAIR_i as it loses recall. If cutting alone reaches "−3.0 CHAIR_i at −2.0 recall", G1 as written can be met by a trivial baseline. P1 tests this before any K2 GPU time.

**Frontier (fixed now).**
- Each zero-shot caption (post-W3 decode, after `untruncate`) is cut to its first k clauses, k = 1, 2, …, k_max, with exactly the pinned editor's clause splitter (`units`, W5). A caption with fewer than k clauses stays whole, so k = k_max is the uncut set.
- For each k: corpus recall R_k and CHAIR_i,k under the W21 gold and the W20 scorer.
- The frontier is the piecewise-linear curve through (R_k, CHAIR_i,k). Its value at a target recall R* is the linear interpolation between the two k that bracket R*; equal recalls take the first k that reaches R*; outside [R_1, R_max] the end point is used and `frontier_clamped` is set.
- Word-percentage truncation may be reported as a secondary curve. It is never used for the verdict.

**Measures.**
- **Gap_ceiling** = CHAIR_i(frontier at R_edited) − CHAIR_i(edited), where "edited" is the K2 target set, the student's ceiling. Paired image bootstrap (B = 2,000, `default_rng(0)`, the Gate 0 resample), frontier and edited on the same draw; the 95% half-width is reported.
- **Check T:** does any k < k_max satisfy ΔR ≥ −2.0 and ΔCHAIR_i ≤ −3.0 against the uncut zero-shot (point estimates)? That is, does truncation alone meet G1 as written.
- Beside them: R_edited, both CHAIR_i values, the frontier points by k, matched-count F1 of edited and zero-shot (Paper A's matched prefix on the asserted v2 classes, cited as a tool), mean words and the cap-hit share (W3).

**Verdict (pre-fixed; `k2_gate0.p1_frontier`).**
| | |
|---|---|
| **P1-GO** | Gap_ceiling ≥ 6.0 (2 × SESOI, the W1 logic) and half-width < 3.0 |
| **P1-NO-GO** | Gap_ceiling < 6.0. `P1_VERDICT.md` carries: "K2 headline under G1 not safe: ceiling does not clear the truncation frontier by 2×SESOI". Gate 0 itself is not stopped |
| P1-INCONCLUSIVE | Gap_ceiling ≥ 6.0 but half-width ≥ 3.0 (not resolvable on val 924), or the frontier was clamped (R_edited outside [R_1, R_max]: not a same-recall comparison; CC-125) |
| P1-ERROR | P1 raised (CC-125 X1): Gate 0's record is written first and stands; `P1_VERDICT.md` says "P1-ERROR (not run)" |
| **Flag** | if T is true: "G1 comparator must become the frontier", for the judge, whatever the gap |

The verdict and the flag are written to `P1_VERDICT.md` and into `gate0_decide.json` under `p1_truncation_frontier`. One look; no rerun. A P1-NO-GO or a T flag goes to the judge panel together with Gate 0's result; it feeds the K2 Gate 1 rule and the MT4 fixed sequence (Ken proposes H-P1 after H2), and nothing here is a method result.

## 7. Disclosures (W7)

- Val 924 was used before:
  - as B's WiSE-FT gate set;
  - for B's adapter decodes (`data/results/uitviic_ind_val/`);
  - as the G-RL pilot's dev set (`PILOT_RULE.md`).

  All 924 images are COCO train2014, so exposure during pretraining is possible.
- **Shared decodes:** none. G-RL's zero-shot val decode uses Qwen2.5-VL-7B at 160 tokens through `evaluate.py`. This pilot's uses Qwen3-VL-8B at the frozen value through the LB decoder. The settings differ, so neither decode serves the other (CC-119 ruling 8), and each is labelled with its model and settings.
- The editor (v1) and the scorer (v2) share the lexicon. The edit therefore removes exactly the mentions that v1 flags. This is why (b) is a size check, not a validity check (W2).
- Training text policy (PD-GR-2, PI-1026aa Q5 YES): the backbone's own gold-edited captions may be K2 training text, disclosed as training data, never evidence, no MT COCO; no training happens in Gate 0. Nothing here is AI-labelled evidence.

## 8. Planning cost

- Measured anchor: 5.29 s/img at 160 tokens (`step1_dev300_guard.json`, KTVIC dev300 detailed, Qwen3-VL-8B), which gives about 1.36 GPU-h for 924 images at 160.
- At a larger frozen value the probe sets the figure. If the cap would exceed 5 GPU-h, Gate 0 is NOT RUN (cost) at the freeze and goes to the PI. At the all-hit bound: 256 → 2.8, 384 → 4.1, 512 → 5.4, 768 → 8.0 GPU-h (CC-124 l.33); with real slice lengths 256–384 projects to about 2.3–4.1.
- Probe: about 0.1–0.2 GPU-h.
