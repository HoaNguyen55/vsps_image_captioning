# Paper B+D, BD-T1: tier-1 dev-explore for a registered single-look confirmation of the forward two-panel gap (DRAFT v2.1, after CC-171a GO 92%)

Status: DRAFT v2.1, 2026-10-30, after CC-171 (GO-with-fixes 91%; W1–W5, N1–N7) and CC-171a (GO-with-fixes 92%; X1–X4, N-a–N-d), see §10. Nothing has been
trained, decoded or scored under this file. CPU only so far: the SSCD scan `bd_t1_sscd.py` (W5), `bd_t1.py lists`
(ids and image sha256 only) and a laptop `build_gold_sft.py` run whose output stayed outside the repo (sha256 pins only).
Everything below is AI opinion. Binding: PI-1029n (H confirmation only under the three-tier method), PI-1029q (datasets
public), PI-1029r (fit the paper's storyline; no new section), the full-splits rule, one look per test set, no caption
text in the repo, no new human labels.

## 0. Why this experiment (storyline fit first)

B+D's spine (PI-1029p, Option A) is "what training-data gains measure, on development data, with two reference
panels". All five reviewers marked the evidence tier as the weak point (BD_META_REVIEW item 5): 187 dev images, one
backbone, D0's KTVIC side known from B-1, KTVIC test closed. The AC's coordinator item 4 / response item 5 asks for
exactly this: a registered single-look confirmation of the forward gap on data no adapter has seen, KTVIC test
excluded. A PASS lands in the existing §5.4–5.5 and Table 5.2 (one new column, "held-out confirmation") and changes
the "development data" qualifier in the abstract and §7.1 to "development data, confirmed once on held-out images".
No new section.

### 0.1 Candidates (ranked by fit, then P(PASS), then reviewer gain)

| # | Candidate | Fit | Tier-3 set | P(PASS) prior | Reviewer gain | Tier-1 GPU-h |
|---|---|---|---|---|---|---|
| **BD-1 (chosen; CC-171 91%)** | Forward gap on H: KTVIC-train images outside dev300 whose only OpenViIC copies are in the **official OpenViIC dev split** (686 after W5); new forward adapters trained on a pool that excludes H | exact (item 5) | H_dev, defined by official split membership, not by a hash draw | P(PASS at the look | reached) high, but P(reaching the look) ≈ 0.6 under the 0.98 gate even if the effect is real (CC-171a X2) | correctness +0.5, contribution +0.25 (the tier objection goes) | about 10.2 (cap 15) |
| BD-2 (CC-171 25%) | Same design, H = 500 images drawn by sha256 from KTVIC-train ∩ OV-train-only (CC-158 / B pivots plan; CC-171 overrules it: 506 of the 533 OV files left after B-R1 are in C's retrieval memory) | exact | a hash carve-out of official train | about the same | the same, minus the "carve-out" objection | about 10.5 |
| BD-3 | Reverse-direction (OpenViIC-trained) confirmation | weaker: the reverse gap was ASYMMETRIC, CI spans 0 | H as BD-1 | below 0.3 | low; reviewers asked for the forward gap only | about 7 |

BD-1 ranks above BD-2 because its test set is an intersection of two official splits (KTVIC train × OpenViIC dev),
used whole (minus pre-fixed, disclosed near-duplicate exclusions), so it meets the full-splits rule without a sampled carve-out, and it is larger (686 vs 500). Its one
extra risk, that the O panel on H is OpenViIC-dev captions while the tier-1 O panel is OpenViIC-train captions, is
rehearsed by tier 2 on T2 (§2), which has the same panel source. BD-3 is dropped: low P(PASS) and not asked for.

Not candidates: an English analogue (COCO / Flickr30K panels) would need a new section (PI-1029r); KTVIC test and
OpenViIC test are spent (B-F1; Paper C's OV-test look); UIT-ViIC has one panel only.

## 1. Sets (fixed now, ids only; `manuscript/prereg/2026-10-30_bd_t1/bd_t1_lists.json`, sha256 b6bbce8f2fa1934c76dcc6005a2d69ff196e8686aa0bd9cc2614d5603b985a17)

Built by `scripts/bd_t1/bd_t1.py lists` from `data/ktvic_openviic_refs.json` `_pairs.train` (4eb02cc4…, split labels
only), the B-1 pool and dev300 id files, the KTVIC train image bytes and the SSCD exclusions (`bd_t1_sscd.json`, sha256
13b9288c7aa3ab9c77f5a66e7ab7879268b75678b8d8f481d63832216c66c885). No OpenViIC annotation file was opened except the
OpenViIC test annotation, which `bd_t1_sscd.py` loaded and used only for its keys (file names) (N-d).

| Set | Tier | Definition | n | ids sha256 |
|---|---|---|---|---|
| T1 | 1 | D0's 187 dev300 images with an OpenViIC-train copy (D0 RULE §2) | 187 | ba506945… |
| T2 | 2 | dev300 ids whose matched OpenViIC copies are all in OpenViIC dev, minus SSCD near-copies of spent test images | 53 | 328472c8… |
| H | 3 | B-1 pool ids (KTVIC train minus dev300) whose matched OpenViIC copies are all in OpenViIC dev, minus SSCD near-copies of spent test images | 686 | 4c6ef9f3… |
| pool | train | B-1 pool minus the 696 H candidates minus 30 pool ids near an H candidate or a dev300 image (shared OpenViIC file 9, min(pHash, dHash) ≤ 10 with mirror 10, SSCD cosine ≥ 0.5 another 11) | 2,743 | — |

- **W5 (CC-171): SSCD near-copy scan** (`scripts/bd_t1/bd_t1_sscd.py`; match_openviic.py's sscd_disc_mixup
  descriptor and small_288 preprocessing unchanged; C's pinned weights; laptop CPU, once). Disclosed departure (N-b):
  the rule is SSCD cosine ≥ 0.5 **alone**, not match_openviic's "hash AND SSCD" pairing rule; it removes more images
  and catches mirrored copies; fixed before any score: (a) 20 pool images near an H candidate or dev300 image leave
  the pool (11 not already caught by the hash rule); (b) 12 H/T2 candidates near a KTVIC-test or OpenViIC-test image
  leave H (10) and T2 (2): ids 484, 2304, 2349, 5870, 6018, 6028, 7503, 7510, 7528, 9564, 10600, 11034. The 10
  dropped H candidates are in neither H nor the training pool (X1). Three OpenViIC-test files are truncated and
  were decoded with PIL's truncated-image option (kept in the scan so they can still exclude).
- T1, T2 and H are disjoint (asserted). H ∩ B-R1's R3 training list = 0, so no OpenViIC caption of an H image was
  ever trained on. B-1's L5 adapters did train on H's KTVIC captions; they are never used on H.
- Images with any OpenViIC-test copy are not in H or T2 (OV test is spent). Images with an OpenViIC-train copy are
  not in H (their OV captions were read by D0/B-R1).
- **Disclosure (X1).** 687 of H's 688 OpenViIC-dev files are in Paper C's dev sets (`ov_dev_a` 352, `ov_dev_b`
  335; c_stage1 `lists.json`). C decoded those images with base LVLMs under retrieval ICL (no fine-tuned
  model in C's registered runs; CC-171) and read their OV-dev captions as development references. No B/D adapter,
  scorer run or selection step has touched H. The paper calls H "held-out images", never a test set, and states this
  overlap and the pool exclusion (CC-171 point 1). T2's OV files: 0 in C's dev sets; 29 are in C's
  `refuse.openviic_files`, in its OV-dev "B-raw" part (files protected from C's retrieval memory and not in C's final
  dev sets), not OV test (N3). N7: re-check C's use of H's OV files at the tier-3 prereg, since CC-172 may add
  fine-tuned baselines.

Levels (prefixes of `train_rl.schedule(pool, 3469, 42)` filtered to the 2,743 eligible, nested): V1 216, V2 433,
V3 867, V4 1,734 (B-1's L1–L4 N) and V5 2,743 (all eligible). x = log2 N. ids sha256: 2ce35b28…, fbcfd721…,
0e3097e8…, 46a502fc…, 9cce8523… (full values in the lists file). sft.jsonl pins (B-1's `build_gold_sft.py` call,
default `--select first`): fc8d79a7…, c83d3243…, 01875101…, 9276c5a8…, 9ea2863a… (full values in `bd_t1.py SFT_PINS`).

## 2. The three tiers (PI-1029n)

| Tier | Data | What may be chosen | Machine | GPU-h |
|---|---|---|---|---|
| 1 dev-explore (this file) | T1 (187) | the tier-1 outcome below; free iteration on dev, all logged | M2 (role m4, dev-only) | about 10.2, cap 15 |
| 2 dev-confirm rehearsal (separate prereg, written only on PROCEED_TO_TIER2; rule fixed now, §2.1) | T2 (53); O panel = OpenViIC-dev captions, the H panel source | nothing: the exact tier-3 analysis, run once | laptop CPU (the T2 preds already exist from tier 1) | 0 |
| 3 single look on held-out images (separate prereg) | H (686) | nothing | M1 (role m3, test-capable); decode the 15 tier-1 adapters on H; waits behind A's queue on M1 | about 3.9 decode + 1 Step-0, cap 8 |

- Tier 1 decodes all of dev300 (as B-1 did), so T2 predictions exist after tier 1, but no T2 score, T2 KTVIC
  reference or OpenViIC-dev caption is read before the tier-2 prereg is logged. `bd_t1.py score` reads only the 187
  (asserts T1 ∩ T2 = ∅).
- Fail at tier 2 = H is never touched; the result is reported as a dev ablation (papers-aim-for-pass).

### 2.1 Tier-2 rule (CC-171 W2, fixed now, before any tier-1 score)

On T2 (53), the 15 BD-T1 adapters' dev300 predictions (already decoded in tier 1, never scored before), O panel =
OpenViIC-dev captions of T2's copies, K panel = KTVIC references, D0 §3 k rule, one Cider per panel over T2,
bootstrap `default_rng(0)` (2000, 53). Tier 3 may be prereg'd only if ALL hold ("margin", PI-1029n, read as):
1. the exact §7 rule PASSes on T2 (g ≥ 4.934, CI_lo(g) > 0, CI_lo(g_rel) > 0, σ = ∞ CI_lo(g) > 0); and
2. the predicted joint P(PASS on H), computed as in §5 on the pooled T1 ∪ T2 images (240), is ≥ 0.98. Pooling
   rule (X3, fixed now): T1 and T2 are scored separately, each with its own O panel source and one Cider per panel
   per source (T1 = D0's object over its 187; T2 = its own over its 53); the per-image scores are then joined in
   the order T1 ids (D0 order) followed by T2 ids (numeric), and one `default_rng(0)` (2000, 240) bootstrap is drawn
   over the 240 images.
CC-171 notes a 10–20% chance of a false stop at n = 53; that cost is accepted. The OpenViIC-dev annotation file
(`data/datasets/openviic/uit-openviic-annotation-dev.json`, sha256
2a68a3eb4d41926deb524aa8f98c80f112472474906d73d9763c790fb0cac847) is opened on the laptop only, at tier-2 scoring,
and only T2's files are read from it (W3).
- H images are never on M2: the job's guard refuses while any H image sha256 exists under `$NCS_DATA/datasets`
  (operator deletes them from the staged KTVIC train folder first). `build_gold_sft.py --images-file` filters by
  id and never opens image files, so the pool builds without them.

## 3. Recipe (B-1, unchanged except the pool and levels)

B-1 PREREG ee91c152 as run on M4: `train_stage2.py --stage sft --epochs 2 --seed S --loss-mask assistant`, 4-bit,
512 vision tokens, `save_steps=200`; resume hook 05466ef5 and .venv freeze 7332d343; greedy short-prompt dev300
decode with `evaluate.py --model qwen2.5-vl-7b` (NCS_DATASET=ktvic_dev). Seeds 42/43/44. Step 0 machine parity: the
n2 p1dev_s42 adapter decoded on M2 must give ≥ 95% identical captions to the registered n2 preds (1e183383), else JOB
STOP. `b1.py check --machine --job bd_t1_job.sh` enforces B-1's job fragments and S5's forbidden flags.

## 4. Budget (B-1's measured M4 gpu_seconds.tsv)

Train, mean of seeds: 216 → 403 s, 433 → 770 s, 867 → 1,520 s, 1,734 → 2,990 s; 3,469 → 5,937 s, so V5 (2,743) ≈
4,694 s by linear scaling. Decode 330 s each, Step 0 322 s. Design: 3 × (403 + 770 + 1,520 + 2,990 + 4,694 + 5 × 330)
+ 322 ≈ 36,400 s = **10.11 GPU-h**. **Hard cap 15 GPU-h** (1.5×, B-1 accounting; timeout = final CAP STOP). Fits one
RTX 3090 24 GB (B-1 ran this recipe on a 24 GB card).

## 5. Scoring (laptop CPU, once, after the final PREREG.md sha256 is in LOG.md)

D0's scorer unchanged (`d0_reread.scored`: kit B, RDRSegmenter, lower-cased, trailing punctuation stripped, CIDEr-D
×100, one Cider per panel over its selected refs, `d0.in_order`). Panels and k rule = D0 §3 (k_i = min(5, |O|, |K|),
hash selection). Bootstrap = D0's: one `default_rng(0)` (2000, 187) index matrix, percentile 95% CIs.

- Scorer gate (a decided number, not a look): the 15 B-1 adapters rescored by this code must give D0's decided b_K,
  b_O and g within 1e-6, else abort with no output.
- Statistics on the 15 BD-T1 adapters, x = log2 N over V1–V5, seed fixed effects (`d0.fe_slope`): b_K (own panel),
  b_O (other panel), g = b_K − b_O, g_rel (ln scale, % per doubling), the same at σ = ∞ (no length penalty), per-seed
  slopes (reviewers' item 3).
- **Predicted P(PASS on H)** (CC-171 W1), averaged over the 2,000 bootstrap draws d, SE_H = SD(draws)·sqrt(187/686):
  point clause P(g ≥ 4.934) = mean Φ((d − 4.934)/SE_H); each "CI_lo > 0" clause (g, g_rel, σ = ∞ g) = mean
  Φ(d/SE_H − 1.96). Joint = 1 − Σ(1 − p_i), a Bonferroni lower bound. A planning number, not a verdict.

## 6. Tier-1 outcome (clauses in this order)

1. **NOT_REPRODUCED** if g < P1 SESOI (4.934, D0 §6, asserted against D0 decide.json) or CI_lo(g) ≤ 0; or CI_lo(g_rel)
   ≤ 0 or σ = ∞ CI_lo(g) ≤ 0. → No tier 2; the paper keeps its development-tier wording; the run is reported in the
   supplement as a dev replication with reduced pool.
2. **REPRODUCED_LOW_POWER** if the joint predicted P(PASS on H) < 0.98. → Stop. PI-1029n has no lower-P route to a
   look at H; only an explicit PI exception could reopen it (CC-171 W4).
3. **PROCEED_TO_TIER2** otherwise. → Tier-2 prereg drafted (CPU, T2).

Reading (X2, corrected): the predictor averages over the tier-1 draws, so the point clause behaves like
Φ((g − 4.934)/sqrt(SD² + SE_H²)) with SD ≈ 1.7 and SE_H ≈ 0.89. It alone falls below 0.98 at a tier-1 gap of about
8.9. D0's B-1 adapters gave g = +9.87 on T1, so tier 1 stops as low-power for any gap below about 9; even if the
effect is real, P(reaching tier 2) ≈ 0.7 and P(reaching the held-out look) ≈ 0.6 (CC-171a). Every outcome still gives
a dev replication for the supplement.

## 7. Draft tier-3 PASS rule (fixed here so tier 1 cannot tune it; copied verbatim into the tier-3 prereg)

On H, 15 BD-T1 adapters decoded on M1, O panel = OpenViIC-dev captions of H's copies (pooled, stripped, repeats
dropped, D0 §3 k rule and hash selection), K panel = KTVIC references of H, one Cider per panel over H, bootstrap
`default_rng(0)` (2000, 686), percentile 95% CIs (W3). Scored on the laptop, once, after the tier-3 prereg is in
LOG.md; the OpenViIC-dev file (sha above) is read then for H's files only. H images are staged on M1 only.
**PASS** iff g ≥ 4.934 **and** CI_lo(g) > 0 **and** CI_lo(g_rel) > 0 **and** σ = ∞ CI_lo(g) > 0.
FAIL if g ≤ 0 or CI_hi(g) < 4.934; otherwise INCONCLUSIVE. Reported in full whatever the outcome (§1 and §5.5).
Paper wording (N1): "the point estimate reached the pre-fixed SESOI of 4.93 (half the development gap, so the bar
is data-dependent)". A PASS adds one column to Table 5.2 and one abstract clause; a FAIL is reported briefly in §5.5.

## 8. Disclosures and limits

- H is KTVIC *train*: the K panel is the same annotation campaign as the training captions (that is the paper's
  point, own panel). The new adapters never saw H's images or captions.
- One backbone (Qwen2.5-VL-7B), as in B-1/D0. A second backbone is not proposed (cost, and the reviewers did not ask).
- Annotator identity is not separated (reviewers' item 10); H does not change that.
- 30 pool ids removed as near-twins of H candidates or dev300; V1–V4 keep B-1's N, but the id sets differ from
  B-1's: shared ids 171/216, 343/433, 676/867, 1,370/1,734 (X4).
- N2: dev300 includes T2, so the tier-1 decode files hold T2 predictions (unread until tier 2), and the staged
  KTVIC train_data.json on M2 holds H's KTVIC captions (text only; the guard keeps H images off M2, and the sft pins
  prove they are not trained on).
- M2 queue order (X4, CC-172): L1-b (crash triage, OPS-1030b), then A-T1, then BD-T1; the job's lock check refuses
  while another job holds M2.
- N-a: each tier-1 decode also writes evaluate.py's KTVIC CIDEr over all of dev300, which includes T2's 53 images
  (a K-panel aggregate only; no O panel, no slope; not used for any decision).
- Laptop `lists` read KTVIC image bytes and split labels only; no caption printed.

## 9. Files

- `scripts/bd_t1/bd_t1.py` (lists, ids, sft, guard, rootscan, left, score, selftest), `scripts/bd_t1/bd_t1_sscd.py`
  (W5 scan; needs torch, run once on the laptop), `scripts/bd_t1/bd_t1_job.sh`, `scripts/bd_t1/SHA256SUMS`,
  `bd_t1_sscd.json`, `bd_t1_lists.json`.
- Guard (W5, X3): the job runs `bd_t1.py rootscan` once in preflight (sha256 of every image file under /root vs H, and
  every zip/tar member name under /root vs H's file names), and
  `guard` before every GPU step (H images under `$NCS_DATA/datasets`, OpenViIC files, KTVIC test, locks).
- Reused unchanged: `scripts/b1_scaling/b1.py`, `scripts/b_d0/d0.py`, `scripts/b_r1/b_r1.py` (twin rule, role),
  `scripts/b_r1/d0_reread.py` (scorer, fit), `scripts/build_gold_sft.py`, `scripts/train_stage2.py`, `scripts/evaluate.py`.
- Selftest: `python3 scripts/bd_t1/bd_t1.py --selftest` (synthetic only; set rules, outcome order, prediction,
  slope recovery, H-file scan by sha256, cap, job fragments).
- Finalisation (F1, before any GPU step; N6: after the CC-171a re-read): rename to PREREG.md, pin its sha256 in `bd_t1.py PREREG_SHA256` and LOG.md,
  regenerate SHA256SUMS, gatekeeper commit by path.

## 10. CC-171 W-items

W1 predictor (CI clauses at 1.96·SE_H, Bonferroni joint; `predict(ci=True)`, `joint`) · W2 tier-2 rule fixed (§2.1)
· W3 H bootstrap, OV-dev file, machine and time (§2.1, §7) · W4 low-power = stop (§6) · W5 SSCD scan + rebuilt lists
and sft pins + /root scan (§1, §9) · N1 SESOI wording (§7) · N2 disclosures (§8) · N3 the 29 T2 files (§1) · N4
selftest V5 = 2,743 · N5 start after L1-b (§8) · N6 this re-read · N7 C re-check at tier 3 (§1).

CC-171a: X1 overlap 687/688 recounted, dropped ids outside H and pool · X2 low-power threshold ≈ 8.9 and P(reach)
stated · X3 rootscan checks archive members; T1 ∪ T2 pooling rule fixed (§2.1) · X4 level overlaps, M2 queue order ·
N-a dev300 aggregate · N-b SSCD-only rule, truncated files · N-c 2,743 / 10.11 · N-d OV-test keys wording.
