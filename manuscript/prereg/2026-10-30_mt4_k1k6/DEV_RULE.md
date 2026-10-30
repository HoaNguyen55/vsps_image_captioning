# MT4 Branch K1+K6 dev rule: tier 1 on val 924, tier-2 rehearsal on T2-2000, one KV look on M1

**Status.** DEV RULE v3, committed 2026-10-30 by the gatekeeper under CC-175 round 2 (GO 92, tier 1 only), CC-188 W1/W4 and CC-189. Written blind:
- no K1 or K6 adapter exists;
- no K1/K6/base8_s decode exists on any set;
- no T2-2000 image has been fetched, featured or decoded;
- no KV-4,224 image has been staged and no KV prediction exists.

Nothing here binds until the gatekeeper commits this file (renamed `DEV_RULE.md`) with `scripts/mt4_k1k6/` after the
judge read (CC-175). No K1/K6 GPU step runs before that commit (CC-174 r5).

**Two commits, two tiers (CC-175 r3, J-6).**
- `DEV_RULE.md` plus the §8 cost amendment license **tier 1 only**. Committing them freezes this gate text before
  any K1 output exists.
- **MT4 PREREG AMENDMENT_2** must be committed at the irreversible tier (PI-1029o) **before the first tier-2 step**:
  any T2 image, any confirmatory training. GATES `AMEND2` holds its LOG id. Its content is the T2 gate of §6 and its
  outcomes, the K1+K6 freeze mechanics of §7, and the KV gold and scorer pins. Nothing else.
- **Fallback, written now:** if AMENDMENT_2 is not committed before the first tier-2 step, Branch K1+K6 is HELD →
  TO-PI. There is no KV look without the gate, ever.

**Label.** DEV RULE for MT4 Branch K1+K6 (MT4 PREREG §5 l.95 "its own dev rule"). Tiers 1 and 2 are DEV and are
never reported as results. Tier 3 is the PREREG's one confirmatory look and is gated by this rule.

**What binds and why (CC-174 r1, r2).**
- The K2 Gate 1 decision is NO-GO, anchored at sha256 `6987b911…3d05bc` (`2026-10-28_k2_gate1/gate1_decide.sha256`,
  commit 3014545).
- MT4 PREREG §0 row 2 therefore binds **Branch K1+K6** (PI-1026u Q4). K2 gets no KV look of any kind (PREREG l.21,
  STOP.md).
- This branch is a **2027 Q2 journal paper (target about 07/2027)**, not a Q1 vehicle (CC-188 r3; PI default YES on CC-188 Q3, which overrules PI-1029h Q3's 05/2028).
- Pre-written framing, unchanged (PREREG l.106): K1 is the strong baseline and the data/backbone axis, not a method claim.

**Sources.** MT4 PREREG §1–§3, §5 (l.88–l.106), §8 (l.128–l.145); MT4 AMENDMENT_1 A3 and A5; K2 Gate 1 RULE §2, §7
and l.296; W25 RULE §1–§5; CANDIDATES_2026-10-26 l.117–l.128 and l.183–l.192; CC-174 r1, r5 and W2, W3; CC-169 W3 (gate
ids); PI-1029n (three tiers), PI-1029m (aim for PASS), PI-1026v (full splits).

## 1. The three tiers and their sets

| Tier | Set | Role | May select? |
|---|---|---|---|
| 1 dev-explore | **UIT-ViIC val 924** (COCO train2014, gold = `gold_instances.json` 42c100f5) | fixes (a) N_SHORT and (c) epochs, checks (d) | yes, by the §5 rule only |
| 2 dev-confirm | **T2-2000** (below) | runs the exact registered H-B1/H-B2 analysis once, plus the simulated P(PASS on KV) | **never**: it only licenses or blocks the KV look |
| 3 test | **KV-4,224** (PREREG §1, pin 86d93863) | the one confirmatory look, on M1 only | no |

**T2-2000, carved now (`k1k6.py lists`, ids only, laptop).** Karpathy restval (30,504 COCO val2014 images):
- minus `exclusion.json` (29,770 left);
- minus every UIT-ViIC id, train, val and test (28,913; matches `id_counts` `restval_minus_refused_minus_uitviic_train`);
- minus A-touched ids (25,791);
- minus every integer id in any id list under `manuscript/prereg/` (5,437 more), except C-EN's training-side memory
  list `cen_memory_allowed.tsv`. "Id list" means the first column of every `.txt`/`.tsv` and every all-integer list
  inside every `.json` (the `.json` input was added by CC-188 W1; see the re-carve note below);
- leaves 20,354 candidates, of which the **2,000 with the smallest sha256("mt4_k1k6_t2_2026-10-30:" + id)** form T2.

The result is `t2_ids.txt`, sha256 `298ae5e1aa327e99…c3c69ac1`, with the counts in `k1k6_lists.json`.

**Re-carve (CC-188 W1, 2026-10-30).** The first carve (sha `9f0e0c0b…bd1fce`, 04:37 VN) predates A-T3 (committed
dbb74f4, 10:02 VN) and scanned only `.txt`/`.tsv` lists. It shared 397 distinct ids with A-T3: 257 with
`2026-10-30_a_t3/val2017_ids.txt`, 68 with D1, 69 with D2 and 3 with smoke (`a_t3_lists.json`). The collision was found
before any T2 output existed: no T2 image was fetched, featured or decoded, and no MT4 K1/K6 output exists on the laptop
or in the machine mirrors. The re-carve uses the same salt, the same steps and the same sampler; the only change is
that `prereg_int_ids` also reads the integer id lists inside `.json` files, which brings in A-T3's D1, D2, smoke and W2
drops (`a_t3_w2_dev_drops.json`) and the id lists of the other studies. Of the old 2,000 ids, 1,585 stay in T2.
Re-verified after the re-carve: 0 overlap of T2 with every id list under `manuscript/prereg/` (every integer token in
`.txt`/`.tsv`/`.csv`, every integer or digit string in any `.json` list, and every digit `.json` key), except the
disclosed C-EN memory list below; 0 with the `data/` subset lists (`*_ids*`, `*lists*`, `*split*`, `*subset*`); and 0
with every image id in the prediction and gold files under `data/results/` and the machine mirrors' `outputs/`.

Why T2:
- It is not val 924. T2 has no Vietnamese reference and has never been decoded or scored by any group model, so no
  choice was ever made on it.
- It comes from the same source as KV: Karpathy val and restval are both COCO val2014, split at random by Karpathy.
  The two sets share their distribution, and T2's gold comes from the same `instances_val2014.json` (pin e1b4d1bc).
- Its 2,000 images are no K1 training image (UIT-ViIC ids are removed) and are added to the W25-K1 sets (§4).

**Disclosure.** All 2,000 T2 images are in C-EN's English retrieval memory, so paper C may retrieve their English COCO
captions as in-context examples. Nothing is scored on them there. No K1, K6 or base8_s system ever sees them before
tier 2.

**The T2 bytes are kept off the machine during tier 1.** Tier 1's guard adds the T2 ids to the refused set, so no T2
image can exist on M1 while anything is being selected.

## 2. PREREG §5 l.95 items (a)–(d), and (e), fixed now

| Item | Fixed value | Changed by tier 1? |
|---|---|---|
| **(a) short `max_new_tokens`** | **160**, the default of `evaluate.py`. One pre-written fallback: if any tier-1 short decode has more than 1.0% cap hits, tiers 2 and 3 use **256**. Detailed mode uses 512 (PREREG §2) | only by the cap-hit rule |
| **(b) decode path** (K1, K6, base8_s) | The K2 student path (K2 RULE §2, W7): venv-q3 (freeze 2bb7397e); 4-bit NF4 double quant with bf16 compute; sdpa; LoRA r16, α32, language tower only. The adapter's state is loaded into a fresh LoRA, **not merged**; then eval, KV cache on, left padding. Decoding is greedy with batch 4, `min_pixels` 262,144 and `max_pixels` 1,048,576 (B-N1 processor kwargs), through `decode_hf_vlm` generate / slices / writer. **base8_s** = the same loaded net with its fresh LoRA left in place (`lora_B` = 0 asserted). Prompts: `PROMPTS["short"]` and `PROMPTS["detailed"]` (0addb5dd). K6 uses the same path on Qwen3-VL-4B | no |
| **(c) training mix and epochs** | **Target reading of l.91 (CC-175 W5).** PREREG l.91 says "(fuse multi-reference targets), short mode" and cites CANDIDATES l.117, which reads: "Short mode uses one human reference per sample. Detailed mode uses B's fuse2 multi-reference targets." fuse2 is a detailed-mode target (`build_gold_sft.fused`). K1 is short mode, so K1 trains on single human references, cycled so that every reference is used (PI Q2 of CC-175: default YES, binding before the first tier-1 training step). There is no target grid: it would exceed 100 GPU-h. The planning pair of §6 is fuse2-vs-P1, not this recipe. **Mix:** the natural union of KTVIC train (3,769 images), UT-2,402 minus the 10 K2-W25 ids (2,392) and OpenViIC train (9,088), minus the W25-K1 exclusions (§4). That is 15,249 images before W25-K1. There is no re-weighting. **One example per image per epoch:** the e-th time an image comes up in the `train.schedule(keys, E × n, seed)` order, it gets reference (e + seed) mod n_refs, so the references are cycled across epochs (`k1k6.example_plan`). Short mode only. **Trainer:** the K2 Gate 1 loop verbatim (labels −100 over the prompt; AdamW at lr 1e-4, weight decay 0, constant; 8 micro-batches of 1 per step; no clipping; last checkpoint), with the LoRA initialisation and the example order seeded by `seed`. **Epochs E\*:** chosen by tier 1 from {1, 2, 3} | E\* only |
| **(d) language gate (short-mode CJK leakage)** | A short caption **fails** if `k2_gate0.language_ok` is false (`clean_supervision.CJK_RE` / `OUT_OF_SCRIPT_RE`, sha 01f17200). A trained system (each K1 seed, K6) whose failing share is above **2.0%** cannot be selected (tier 1) or pass (tier 2). Failing captions are scored as written: there is no filtering and no decode-time constraint, so the path stays identical across systems. base8_s's share is reported and never gates (its 0.03 on dev300 is a different set and matcher) | no |
| **(e) the short metric, reconciled** (PREREG l.94 with §1 l.31) | Mentions = `k2_gate0.row`, matcher v2. A negated or hedged class is a mention and never a TP (§1). Per image: tp = \|A ∩ G\| and men = \|A ∪ U\|. P = Σtp / Σmen; R = the mean of the per-image recall over images with gold; F1 is their harmonic mean (`object_prf.prf`). Every caption passes `untruncate` first | no |

## 3. Systems and seeds

| System | Backbone | Seeds | Tier 1 | Tier 2 | KV |
|---|---|---|---|---|---|
| base8_s | Qwen3-VL-8B @0c351dd, fresh zero LoRA | 1 decode per mode | short | short + detailed | short + detailed |
| K1 explore | 8B | **seed 0**, one 3-epoch run saving checkpoints e1–e3 | short | — | never (PILOT_RULE §6) |
| **K1** | 8B | **1, 2** (PREREG M4 default 2) | — | short | short; detailed (seed 1, descriptive) |
| **K6** | **Qwen3-VL-4B-Instruct @ebb281ec70b05090aa6165b016eac8ec08e71b17** (pinned now, PREREG l.92) | **1** | — | short + detailed | short + detailed, if kept (§6) |

- The 4B pins are both LFS shas (`k1k6.SNAP_4B_LFS`: 30a01a05…, 046296a2…) and the LoRA trainable-parameter count:
  36 × 917,504 = 33,030,144 (from config: hidden 2,560, MLP 9,728, 8 KV heads × 128).
- The 8B count is w22_sft's 43,646,976.
- Confirmatory adapters are new runs at E\*. Tier-2 decodes those exact adapters, and the same files go to KV. So
  tier 2 rehearses the systems that are tested, not stand-ins.
- K6 has one seed (J-4).

## 4. W25 on the K1 pools (PREREG l.34, l.96; CC-119 W25)

- **XM3600 (J-3, CC-153 r4).** XM3600 is matched by **C1 only**: byte identity against `exclusion.json`
  `image_sha256` (`xm3600_all_images` and every other list). No XM byte is read. The code is `w25k1_decide`'s
  `sha_lists`, counted per list. This narrows PREREG l.96's W25 requirement for XM. Paper sentence: "Training images
  were compared with the XM3600 test images by file hash only (exact copies), not by perceptual or copy-detection
  similarity."
- **Rule:** W25 RULE §3 unchanged. An image is excluded if C1 (byte-identical) ∨ C2 (min(pHash, dHash) ≤ 10 with the
  mirrored hashes, and SSCD ≥ 0.5) ∨ C3 (SSCD > 0.75) holds against at least one image of any set below. The code is
  `w25.rule` and `build_memory.near` with the SSCD weights 9f26bd4c (`k1k6.py w25k1`).
- **Pool side:** KTVIC train 3,769 and OpenViIC train 9,088 are new features. UT-2,402 reuses `feats_ut.npz`
  (17d3ebf0, the W25 output), for the sets W25 did not cover.
- **Against:**

  | Set | Features |
  |---|---|
  | KV-5,000 | C-EN `feats_coco_kval.npz` 9783f7a6, reused |
  | OIV7 val (41,164) | the 72 W25 `oiv7_parts` plus C-EN `feats_nocaps_val.npz` b69dac29, reused |
  | KTVIC test (558) | new |
  | UIT-ViIC test (231) | new |
  | OpenViIC test (2,001) | new |
  | **T2-2000** | new (fetched to tmpfs as in W25 §5) |
  | XM3600 | see J-3 |

  This covers CANDIDATES l.120's 401 KTVIC-test images inside OpenViIC train.
- **Where:** the laptop, CPU only, in a venv-cenfeat clone (freeze 1a639a50). Every test-side image is already on the
  laptop and never goes to M1. It uses 0 GPU-h; its wall cap of 5.4 h is charged to the test line anyway, as §5 l.96
  asks.
- **Outputs:**
  - `w25k1_excluded_keys.txt` and `w25k1_decide.json` (one writer, O_EXCL);
  - the feature files are never committed;
  - no one looks at a pair.
- **HOLD:** the job refuses every tier until `w25k1_excluded_keys.txt` is committed and GATES `W25K1` holds a LOG id.

## 5. Tier 1 (dev-explore on val 924; `k1k6.t1_rule`, selftested)

- **Steps:**
  1. a 40-image detailed timing probe of base8_s on the K2 probe ids (training images);
  2. the K1 explore run (seed 0, 3 epochs, checkpoints e1–e3);
  3. short decodes of base8_s, e1, e2 and e3 on val 924 at N_SHORT = 160.
- **(a):** if any of the four has more than 1% cap hits, `n_short` = 256 for tiers 2–3.
- **(c) E\*:** among the checkpoints with language-fail share ≤ 2% and point ΔP ≥ −1.0 over base8_s, take the largest
  point ΔF1. A checkpoint within 0.5 F1 of the best with fewer epochs wins. If none qualifies, the verdict is
  **T1_FAIL**: no tier 2, TO-PI.
- **Futility (CC-175 N5, adopted now, before any tier-1 output).** If the best qualifying point ΔF1 is below +2.0
  (the SESOI), the verdict is also T1_FAIL. Tier 2 could not pass H-B1, and the stop saves about 39 GPU-h.
- `t1_select.json` (O_EXCL) and `rates.json` (the measured rates) are written, and `caps.json` is recomputed from them
  (§8).
- The gatekeeper commits `t1_select.json` **and `caps.json`** and fills GATES `T1` before tier 2. Tier 2 refuses unless
  both equal their HEAD copies (W4).

## 6. Tier 2 (dev-confirm on T2-2000; `k1k6.hyp`, `p_pass`, `t2_rule`, selftested)

- **Which systems:** those the committed `caps.json` keeps (`k1k6.systems_of`). A stage cut by the ladder is skipped,
  and its system is absent from tier 2 and KV. A cut K6 reads "H-B2 not tested (cost)" (W2).
- **Steps:** train K1 seeds 1–2 and K6 seed 1 at E\*. Then stage T2 (each image's own `coco_url` from the pinned `instances_val2014.json`, as `common.stage`; every sha checked against the
  refused shas). Then decode T2: short for base8_s, K1 s1, K1 s2 and K6; detailed for base8_s and K6.
- **The registered analysis, verbatim.** `hyp()` is the function the KV scorer calls (PREREG §3, §5):
  - paired image bootstrap, B = 2,000, `default_rng(0)`, one draw shared by every system, percentile CIs;
  - K1 seeds pooled per image;
  - **H-B1** holds when point ΔF1 ≥ +2.0, CI lower > 0 and ΔP CI lower > −1.0;
  - **H-B2** holds when K6's ΔF1 CI lower > 0 and detailed ΔCHAIR_i CI upper < 0;
  - fixed sequence: H-B1, then H-B2.
- **Predicted P(PASS on KV) by simulation (`p_pass`).** A two-level bootstrap of the T2 rows, R = 2,000:
  1. draw a T2-sized resample (uncertainty about the effect);
  2. draw a 4,224-image sample from it (KV sampling);
  3. read the H's in their registered forms, with CI bounds at point ∓ 1.96 · SE_KV and SE_KV = the T2 bootstrap SE ×
     √(2,000 / 4,224).

  All systems share every draw, so P(H-B1 ∧ H-B2) is a joint frequency, not a bound.
- **Verdict (`t2_decide.json`, one writer).**
  - **T2_PASS** iff all three hold: H-B1 holds on T2; every K1 seed's language-fail share is ≤ 2%; **P(H-B1 on KV) ≥
    0.98**. Only then is the KV look licensed.
  - **K6 enters the KV kept set** iff also: H-B2 holds on T2; K6's language-fail share is ≤ 2%; **P(H-B1 ∧ H-B2) ≥
    0.98**. Otherwise K6 is not decoded on KV, and H-B2 reads "not tested (K6 failed the tier-2 rehearsal)" (J-5).
  - **T2_FAIL** gives no KV look, ever, for this branch. The result is reported briefly as a dev result (PI-1029m) and
    goes TO-PI under the pivot rule.
- The gatekeeper anchors `t2_decide.json` in `t2_decide.sha256` and fills GATES `T2`.

**Planning power, computed now on existing dev outputs (`power_planning.json`; planning only, no rule reads it).**
- **Inputs:** the only paired short decodes with COCO instance gold on hand, Qwen2.5-VL P1 vs fuse2 SFT on val 924
  (`uitviic_ind_val`, shas 47f3e0ba / 6120c566), scored by the T2 scorer.
- **Observed:** ΔF1 +5.67, ΔP −0.17; per-image SD 14.9 (F1) and 7.6 (P).
- **Two-level bootstrap at that effect:** P(H-B1 on KV) = **0.986** with n2 = 924.
- **With T2 = 2,000:** P ≥ 0.98 needs a T2 point ΔF1 of about **≥ +2.83** with ΔP near 0.
  - The ΔP non-inferiority term caps P at 0.998, at the observed ΔP.
  - At a T2 point of +2.5, P ≈ 0.89.
  - At n2 = 924, P ≥ 0.98 needs about +3.1 and is capped at 0.985.
- That is why T2 has 2,000 images.
- CANDIDATES expects ΔF1 of +10 to +16 (prior 0.85). At such an effect the gate is not the binding risk; precision and
  the language gate are.
- These numbers are not K1's (another backbone and pair) and set no threshold.
- **Caveat (N6).** The planning SD comes from an SFT-vs-SFT pair on another backbone. It may understate the
  per-image variance of base-vs-K1, so the +2.83 figure is a planning value only. The rule computes P from the T2
  rows themselves.

## 7. Tier 3: the one KV look, M1 only, only after an anchored T2_PASS

- **Licence (`kv_ready`, selftested).** All of these must hold:
  - `/root/.vsps_machine_id` = m3, the m3 role, i.e. M1 (A5);
  - every GATES field is a LOG id;
  - `t2_decide.json`'s sha equals the committed anchor;
  - its verdict is T2_PASS;
  - no `mt4_k1k6_decide.json` exists.

  Any failure exits nonzero before staging.
- **Staging and guard.** Tier 3 stages KV-4,224 into `k1k6_kv/` only. It runs after `kv4224.txt` (pin 86d93863) is
  committed by its own `id_counts.py` change (PREREG §1, open item O-1).
  - This is the guard amendment PREREG l.43 asks for: in tier 3 only, a KV-4,224 id may exist only under `k1k6_kv/`.
    Every other refused id and sha is still refused.
  - The images are deleted after the decodes, and the deletion is logged.
- **Decodes:** the kept H set (short: base8_s, K1 s1, K1 s2 and K6 if kept; detailed: base8_s and K6 if kept).
- **The descriptive K1 s1 detailed row** (no H) is not in the kept set and is decoded **last**, only from what is left
  of the line. It never displaces K6 or K1 seed 2, and a short remainder or a cap hit skips it without a cost stop.
  This is scheduling, not a ladder change (W2).
  - Each file's line `SHA  FILE  SYSTEM  UTC` is appended to `KV_PRED_SUMS` by code, fsynced.
  - Nobody opens a KV prediction (PREREG §2).
- **Freeze (A3's mechanics with D_K).**
  - The first line per system counts. Another sha for a kept system halts the freeze (FAULT → PI), also after D_K.
  - Lines out of order, or earlier than the T2 anchor, halt it too (N1, A3 parity). Times are UTC via
    `calendar.timegm`.
  - Lines after D_K, or outside the kept set, are descriptive.
  - The freeze instant is min(the line that completes the kept set + 24 h, D_K).
  - `kvscore` refuses before that instant.
  - A missing seed of an H system makes that H NOT-RUN and stops the sequence: base8_s or a K1 seed missing gives
    H-B1 NOT-RUN. A missing short or detailed K6 row, or a missing detailed base8_s row, gives H-B2 NOT-RUN only. The
    descriptive row never affects either (W1).
- **Commit-at-HEAD (W3, W7).**
  - `kv_ready` reads GATES.json and `t2_decide.sha256` through `git show HEAD:`. An untracked or modified copy never
    licenses the look (selftested).
  - `kvscore` reads `kv_gold.json` only if it equals its HEAD copy, checks `kv4224.txt` against 86d93863, and records
    its own sha.
- **Score:** `kvscore` writes `mt4_k1k6_decide.json` once (O_EXCL). It calls the same `hyp()` on the frozen files, with
  `kv_gold.json`, which is built by id before the freeze and read only by the scorer. That write is the look.

## 8. Cost-only amendment (PREREG §8 l.145): planning rates, caps and the Branch K1+K6 freeze date

**This section is MT4 PREREG §8 l.145's one cost-only amendment for Branch K1+K6.** It is committed with DEV_RULE.md before any K1 training, after the one-judge diff read CC-189. It changes no H, threshold, SESOI, matcher, gold, test set, freeze rule (it sets D_K under §5 l.96), binding branch or H-system seed count. AMENDMENT_1 is not a cost-only amendment (AMENDMENT_1 l.3), so this is the first and only one.

**Text for the gatekeeper's one cost-only amendment, committed before the first K1 training step (tier 1).**

- **The freeze date.** **D_K = 2027-02-28T12:00:00Z** (epoch 1803816000; `k1k6.D_K`; CC-189 r4, overruling CC-175 J-7's 2026-12-31 before any K1 training). It is the Branch K1+K6 freeze date
  of §5 l.96 and §9, set before any K1 training and before any KV prediction exists. A step whose timeout would end
  after D_K is HELD (`left` exit 4).
- **Planning rates.** None is a K2 Gate 1 number (W2):

  | Rate | Value | Source |
  |---|---|---|
  | training | 0.454 s/example × 1.25 | W22-SFT C1 64-token rate × CPU allowance |
  | short decode | 0.55 s/img × 2.0 | CANDIDATES §3 × NF4 planning factor |
  | detailed decode | 3.25 s/img × 2.0 | Gate 0 bf16 × NF4 planning factor |

  The 4B model is priced at the 8B rate until measured.
- **Mechanical re-pricing (the only use of measured rates).** After tier 1, `k1k6.py plan --rates rates.json --t1
  t1_select.json` recomputes every later cap from:
  - the measured tier-1 s/example;
  - the maximum measured short s/img;
  - the probe's detailed s/img.

  The formula is fixed here: projection = n × rate / 3600 + 0.1 h load; cap = ceil(1.2 × projection) to 0.1. The
  re-pricing writes `caps.json` and is committed with `t1_select.json`. It changes no H, threshold, set, freeze rule,
  branch or H-system seed count.
- **Projection at planning rates** (`plan()`; total 76.5 h projected, **92.6 h capped ≤ 100 test line**; GPU-only about
  72 h):

  | Block | Caps (h) |
  |---|---|
  | Tier 1: K1 explore run 8.8, four val decodes 4 × 0.5, probe 0.3 | 11.1 |
  | W25-K1 (laptop CPU, charged) | 5.4 |
  | Confirmatory training: K1 s1, K1 s2, K6 s1, 8.8 each | 26.4 |
  | Tier 2: four short decodes 4 × 0.9, two detailed 2 × 4.5 | 12.6 |
  | KV H rows: four short 4 × 1.7, two detailed 2 × 9.3, staging/cleanup 2.4 | 27.8 |
  | KV descriptive K1 detailed (last, from what is left; W2) | 9.3 |
  | **Total** | **92.6** |

- **Ladder (PREREG l.144, unchanged, applied by code):**
  1. cut K6 (training, T2 and KV rows);
  2. then K1 seed 2.

  base8_s is never cut. If the H systems alone do not fit, the result is **NOT-RUN (cost) → TO-PI** before any
  confirmatory training.
- **Ledger:** the `k2_gate1` rules. The job seeds the M1 ledger once with the W25-K1 charge (`w25k1 19440`, the 5.4 h
  cap), so `left` stops at the true line of 94.6 GPU-h for GPU steps (W8).
  - Fsynced start lines log the timeout.
  - An open start is charged its full timeout before a retry (exit 6).
  - Every decode attempt starts from zero.
  - Exit 124 is NOT-RUN (cost), never a negative result.
- **English arm** (PREREG §6: K1-EN and base8_s-EN, ≤ 30 GPU-h): its own line. It is not part of this rule and never
  delays H-B1.

## 9. K2 Gate 1 in MT4 text: only as a negative dev pilot (CC-174 W2, RULE l.296)

- Gate 1 numbers enter MT4 K1+K6 text **only** through the RULE l.296 sentence.
- `k1k6.py nogo` fills that sentence from the anchored file: it refuses unless the sha is 6987b911 and the verdict is
  NO-GO.
- No Gate 1 rate, delta or timing feeds any cap, power figure or threshold here.
- There is no K2 KV arm, rerun or tuning (STOP.md).

> "On the development set, the gold-edited student did not meet the pre-registered gate (failed: G1, G3, G4, G6;
> ΔCHAIR_i −2.57, Δrecall +4.65, gap to the truncation frontier +2.57). Per the rule, K2 was not run on the test set; it
> is reported as a negative development pilot, and the paper's headline rests on K1 + K6."

(The frontier was clamped high, so the gap equals −ΔCHAIR_i by construction, RULE §7. The paper states this beside
the sentence, without a further number.)

## 10. Gate ids and HOLDs (CC-169 W3 lesson)

- `GATES.json` (this folder) has the keys `W25K1`, `COST`, `T1`, `AMEND2` and `T2`.
- Each value must fully match `l1b.py`'s guard pattern `(OPS|CC|PI)-\d{4}[A-Za-z0-9-]*`. That means a **LOG line id**
  such as `OPS-1030c`. A ruling id such as `CC-175` or `CC-168` never matches, and the selftest asserts both cases.
- Gate fields are read **from HEAD only** (`git show`): an uncommitted GATES.json counts as empty (W3).
- The job HOLDs a tier until its gates are filled (tier 1: W25K1 and COST; tier 2: + T1 and AMEND2; tier 3: + T2) and
  the matching file is committed at HEAD:
  - `w25k1_excluded_keys.txt`;
  - `DEV_RULE.md` and its pins in this folder's `SHA256SUMS` (`t2_ids.txt` 298ae5e1, `k1k6_lists.json`,
    `power_planning.json`; the gatekeeper adds `DEV_RULE.md`, `t2_gold.json`, `kv_gold.json`, `caps.json` when built);
    `t2_ids.txt` is also pinned in code (W7);
  - `t1_select.json` and `caps.json`, each checked by sha against the M1 copy;
  - `t2_gold.json`;
  - `t2_decide.sha256`.

## 11. Machine, data and hygiene (setup_gpu.sh / K2 job patterns)

- **Machine:**
  - M1 (the m3 role) only; `GPU=m4` is refused (selftested).
  - One tmux session, one lock, committed clean HEAD.
  - The venv-q3 freeze 2bb7397e plus `pip check`; the 8B `snapcheck`; the 4B LFS pins.
  - `setup_gpu.sh` adds the 4B snapshot (hub rev ebb281ec) next to the 8B one; that is open item O-2.
- **Pool staging:** `k1k6_pool/` holds `ktvic/` and `openviic/`, train images and train annotation files only, copied
  from the laptop by the gatekeeper. `uitviic/` is a symlink to the staged UT pool.
- **Guard amendment (tiers 1–3).** `common.scan` refuses non-COCO file names. `k1k6.scan_k1` accepts one only under
  `k1k6_pool/`, and only if its sha256 is in the pool manifest. It is otherwise `common.scan` unchanged (selftested).
  KTVIC/OpenViIC/UIT-ViIC test images can never be on M1.
- **Text:**
  - caption text (references and predictions) is read only by code;
  - every printed line and record is numbers, ids and shas;
  - no OpenViIC/KTVIC/UIT-ViIC caption text is in any repo file (this file and the code: 0 caption strings).

## 12. Disclosures for the paper

- **Val 924:** it was reused for selection (tier 1), adding to its earlier uses (PREREG §7).
- **T2:** carved from restval as in §1; it sits in C-EN's retrieval memory.
- **Overlaps:** UT-2,402's 88 A-touched and 857 restval ids are training-side facts.
- **W25-K1:** its exclusion counts are reported per set.
- **Cost:** W25-K1 ran on CPU; its hours are charged to the test line by choice.
- **Tier-2 limits:** the P(PASS) is a planning-style prediction. It is conditional on the registered seeds, and the
  bootstrap covers images only (PREREG §3, W9).
- **K6:** it has one seed. If it failed tier 2, it is reported as "not tested".
- **Text:** the l.296 sentence (§9), and the PREREG l.106 framing.

## 13. Judge items (defaults written; ranked options for CC-175)

- **J-1 T2 source.**
  1. Restval T2-2000, as written (default).
  2. A disjoint second 2,000 for a replication of tier 2 (PI-1029n "ideally two sets"): +12.6 h of caps, giving 105.2 >
     100. It fits only if the descriptive K1 detailed KV row (9.3 h) is dropped.
  3. A val-924 split. Refused by CC-174 W3.
- **J-2 language gate.**
  1. Score as written, gate trained systems at ≤ 2% (default).
  2. A decode-time CJK `bad_words_ids` on every system, which changes the pinned path.
  3. Filter failing captions before scoring, which hides errors.
- **J-3 W25 vs XM3600.** CC-153 r4 refuses XM bytes for non-C use.
  1. C1 only, by `exclusion.json` `xm3600_all_images` shas, with no XM byte read (default).
  2. A full C2/C3 pass on the laptop under a C-owner ruling.
- **J-4 K6 seeds.**
  1. One seed (default; the ladder cuts K6 as one unit).
  2. Two seeds: +25.2 h of caps (training 8.8, T2 5.4, KV 11.0), giving 117.8 > 100, so ladder step 1 would cut K6
     itself.
- **J-5 K6 kept by tier 2.**
  1. K6 enters KV only after its own rehearsal passes (default: the three-tier rule).
  2. K6 enters KV whenever K1 passes. This contradicts PI-1029n for H-B2.
- **J-6 binding route (ruled by CC-175 r3).** MT4 PREREG AMENDMENT_2 at the irreversible tier, **before tier 2**.
  Tier 1 runs on the committed DEV_RULE. See the Status block.
- **J-7 freeze date D_K = 2027-02-28T12:00Z** (CC-189 r4 overrules CC-175 J-7's 2026-12-31; the options below are the historical CC-175 text).
  1. As written (default; it leaves room for A-T1/C-T1 first and L1 tier-2 preemption, CC-174 r5).
  2. 2026-12-15.
- **J-8 E\* grid.** {1, 2, 3} from one seed-0 run (default) vs a fixed E = 2 with no tier-1 selection.

## 14. Open items before tier 1

- **O-1.** `kv4224.txt` writer: one entry in `id_counts.py` `lists`, judged separately; needed before tier 3 only.
- **O-2.** `setup_gpu.sh`: fetch Qwen3-VL-4B @ebb281ec into `/root/ncs-data/models/Qwen3-VL-4B-Instruct-ebb281e` and
  check its two LFS shas. Needed before tier 2 (K6).
- **O-3.** The W25-K1 laptop venv (venv-cenfeat clone, freeze 1a639a50) and its run; GATES `W25K1`.
- **O-4.** The cost-only amendment = §8 of this file. The gatekeeper commits it and fills GATES `COST`.
- **O-5.** `instances_val2014.json` (pin e1b4d1bc) on M1 under `coco_probe/annotations`: used by `k1k6.py gold --set t2|kv` and `stage` (the source of every `coco_url`; no host is written in repo files).
- **O-6.** AMENDMENT_2 (J-6) and its irreversible-tier review, before tier 2. Missing means HELD → TO-PI.
- **O-7.** `k1k6_lists.json` records the sha of the `k1k6.py` that wrote it. The gatekeeper regenerates it (ids and
  `t2_ids.txt` are unchanged) after the last code edit and re-pins it.
  k1k6_lists.json was written by k1k6.py 5b73fb81 (CC-188 W1 re-carve); the later edit changed only D_K (CC-189 W3). T2 ids and their pin 298ae5e1 are unchanged; `lists` is never rerun.
- **O-8 (operator, from CC-175).** Re-stage the UIT-ViIC images on M1 (deleted at 20:02Z), and end the `coco_fetch`
  tmux session before tier 1 (the job refuses while another tmux session exists).
- **CC-175 round 2 (GO 92, tier 1 only).** R2-1 is done: `kvscore` passes the anchored `t2_decide.json` time as
  `not_before`. R2-2 (N3, below) is due before tier 2. R2-3 is O-8.
- **Not adopted now (N3):** matcher v1 beside v2 on T2 and KV is descriptive. It is added to `hyp()`'s report before
  tier 2, with no gating role.

## Amendments

(none)
