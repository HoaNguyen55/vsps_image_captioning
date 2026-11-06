# Paper A dev assumption checks D1–D5: plan v3 (pre-registration style)

Status: PLAN ONLY. Nothing run, no check code written, not committed. Paper repo untouched. v1 (f027b70d) and v2 (c07f5a9b) are unchanged. v3 changes only the CC-266r2 items (§9).
Plan step: A_UPGRADE_PLAN_2026-11-04.md §5 step 5 (EXP-CPU, dev). Theory under test: A_THEORY_DRAFT_2026-11-06_v2.md (111cb591) and A_SUPP_S1_PROOFS_DRAFT_2026-11-06_v2.md (10a0f5bf), committed c914018 under CC-263r2 GO 89 (carried item C4/N6).
Ruling history:
- CC-266 (round 1, NEXT_ROUND 74): B1–B5 BLOCKING, N1–N6. v2 closes all of them (§8).
- D4(b) thinning ALLOWED at 88 (CC-266 ruling 8).
Next steps:
1. CC-266r3, a one-judge diff read v2 → v3 (round 3/3).
2. Gatekeeper commit of v3 after a GO.
3. One-judge CODE read of `a_dchecks.py` (selftest, kernel gate, mutants).
4. S0.
5. Run.
6. Result read at 85.

## 0. Binding rules

- Data: spent dev sets only (PORTFOLIO_3Y_2026-10-29.md §2.3 "Dev-only (spent)": COCO Karpathy test, XM3600, UIT-ViIC test). No decode, no GPU, no new test look. Stored outputs and existing human gold only.
- No new gold. AI labels are not evidence: `data/object_gold/annot_claude.json` is never read, and no model judges anything.
- Every check is post hoc and descriptive, with no verdict on any registered prediction. X4/X5 verdicts are unchanged whatever happens here.
- Outputs hold counts, rates, slopes and shas only, never caption text.
- Paper wording:
  - "development data";
  - "simulated references (not gold)" for D4;
  - no AI mention, no data-overlap wording.
- Notation as in the v2 drafts: C_i complete gold (ℓ_i classes), Q_i = reference ∩ C_i (q_i classes), ρ_i = q_i/ℓ_i, x^S = ln M^S, slopes ×100.

## 1. Precondition: stored per-image inputs (listing and sha256 only)

All 37 output pins and all 61 input pins of `data/results/scar/scar_null_result.json` (242fc04e) re-hash unchanged (here and in CC-266). The 12 g2b outputs match their `.sha256` sidecars. No caption text was opened.

| Set (dev) | Family | Per-image outputs (sha256, first 12 hex) | Images |
|---|---|---|---|
| COCO-5000 (Karpathy test) | F1, 9 Qwen cells | `data/results/coco5000/`: distill-detailed 6453bfd5a2f7, distill-short 12ab5a6e2b70, zeroshot-detailed 96e15f40cead, zeroshot-short 15ca56156796; `coco_transfer_full5000/`: fuse2_s42-detailed f205805a7ab1, fuse2_s42-short cd947944d3cf, p1_s43-detailed b12fbeb91e90, p1_s43-short b0dbbdc50af7; `coco5000_vcd/zeroshot-detailed` d6173e348233 | 5,000 lines each |
| XM3600-600 | F1, 6 Qwen cells | `data/results/xm3600/xm3600_*.preds.json`: fuse2_s42-detailed b941181c7b11, fuse2_s42-short 426c2d8140a9, p1_s43-detailed 296a26bfe176, p1_s43-short 1150a046e634, zeroshot-detailed 47db3b9d2795, zeroshot-short 1f3573324772 | 600 |
| XM3600-600 | F2, Qwen3-VL, 6 cells | `.session_backup/2026-10-20/g2b_score/outputs/g2b_q3_xm600-`: detailed-T0 a66647d12140, -T05 3e6189d627af, -T08 944668eb32fb; short-T0 82b6ef5fdb9b, -T05 522819dfe54d, -T08 71b168e79099 | 600 (537 scored) |
| UIT-ViIC test 231 | F1, 10 Qwen cells | `data/results/uitviic/`: fuse2_s42-detailed 82f34b94cf50, fuse2_s42-short 42122e7ada5a, p1_s43-detailed 46cb0033cb22, p1_s43-short 42ad49eebac9, zeroshot-detailed 0589973c264b, zeroshot-short 76361ccde3db; `data/results/uitviic_ind_test/`: fuse2_s42-detailed c7757cc73413, fuse2_s42-short ebf68bca65b4, p1_s42-detailed 56aac8a6e873, p1_s42-short 94b87b4933d8 | 231 |
| UIT-ViIC test 231 | F2, Qwen3-VL, 6 cells | `g2b_q3_uv231-`: short-T0 7553ab1b58e4, -T05 fcde78a819df, -T08 4839f485665c; detailed-T0 2a92344baddc, -T05 3bef57a29456, -T08 d994c6961bf1 | 231 (209 scored) |

References per image: COCO K = 5 (the first 5 Karpathy sentences); UIT-ViIC K = 5 (all 231 images); XM3600 K = 2 (573 images) or 3 (27). These are counts only.

Gold and references (existing human annotations):
- **COCO, full 5,000 (B1).** Already pinned:
  - deterministic builder `scripts/paperA/a_w4/eval/build_instance_gold_full5000.py` dc0d1f52bffd (tracked, commit 78d0e22), which asserts that its 2,500-probe slice equals `data/coco_probe/instance_gold.json` 963af2c6cc71;
  - its output `.session_backup/2026-10-26/a_full5000/instance_gold_full5000.json` bd36295146e5 (untracked; sha recorded in that folder's SHA256SUMS l.9);
  - manifest `data/coco_probe/manifest_full5000.json` 699769100c57;
  - committed 9 × 5,000 cells `.session_backup/2026-10-26/a_full5000/out/r4_full5000_all9.json` 332da8b6264c (commit 51ef280), produced by `scripts/paperA/a_w4/eval/check_coco_full.py` adb3b936b962. inst slope +22.13; median M 1.21.

  Other COCO inputs: references `data/datasets/karpathy/dataset_coco.json` 2fd999220673; boxes for D4(b) `data/datasets/coco_probe/annotations/instances_val2014.json` e1b4d1bc5490; `data/coco_probe/coco80_vi.json` 926e08571ef6; `data/coco_probe/chair_synonyms.txt` b685537b36fe.
- XM3600:
  - `data/xm3600_subset.txt` f5ab86c7f312 (600 ids);
  - `data/datasets/xm3600/test_data.json` 0a613214f956;
  - `data/xm3600/oiv7_labels.json` bac3953a511a;
  - `data/xm3600/vi_oiv7_map.json` 27f2b1ca3f2b;
  - `data/datasets/xm3600/oiv7/oidv7-class-descriptions.csv` 84a4373a0efb.
- UIT-ViIC: `data/datasets/uitviic/test_data.json` 54abc0fb068a, `data/uitviic/instance_gold.json` 278d15b97e3e.

Code reused (pinned):
- `scripts/g2b/score_g2b.py` 66c665c7a71d (`karpathy_refs`, `uitviic_context`, `xm3600_context`, `mentions`, `rows`, `scores`, `ols`);
- `rescap/chair.py` e47d249ac729;
- `scripts/xm3600_oiv7.py` 9a79403f4fc3;
- `scripts/scar/scar_null.py` b0e3825eaa48;
- `scripts/pascal50s/p50x.py` 3f562e878ed7 (`salience`, `null_slopes`, X4 levels and the compound rule, l.172-181);
- `scripts/pascal50s/p50.py` (`draw`: default_rng(1), J = 20).

Other committed anchors for S0:
- `.session_backup/2026-10-14/r11_litmaps/L1/check_coco.json` cb21dd257f93;
- `.session_backup/2026-10-14/r11_verify/c2_n1_uitviic_mstar.json` bed1dc259aef;
- `.session_backup/2026-10-14/r12_verify/xm3600_full_verdict.json` 0b2b3aa5e1a3;
- `data/results/g2b/g2b_score.json` 68be2b7a0904.

**How COCO gold reaches the scorer (B1 iv).** `score_g2b.coco_context` hardcodes the 2,500-image gold and uses `inst.get(i, {})`, so the other 2,500 images would score as empty. The checks therefore never call `coco_context`. `a_dchecks.py` builds the COCO context itself:
- references come from `score_g2b.karpathy_refs` and `sc.en_classes` (unchanged);
- C_i is `inst[i]["coco"]` from `instance_gold_full5000.json`, indexed directly;
- a missing id raises and stops the run (fail-closed).

`score_g2b.py` is not edited. A mutant with the `.get(i, {})` fallback must be caught.

Missing or not usable:
- **PASCAL-50S: all 14 caption files are gone.** They were deleted on the scoring machine after scoring under the registered data-handling rule. `data/results/p50/` holds only decide files, EVENTS and about 110-byte n-gram stubs. X4 cannot be re-checked per image; the U arm below is an analogue (§2).
- **A-T3 COCO val2017 per-image outputs are not stored.** That set is a spent test and is not re-read. The 593 Karpathy-test ids from val2017 are read only through the stored outputs of the systems in the table (CC-266 ruling 2).

Excluded, each by a fixed rule:
- `uitviic_ind_val`: K2 dev.
- g2b `*_en` runs: English prompts against Vietnamese references.
- `uv231-short-T05x6.samples.jsonl`: a sample pool, not a system.
- `coco_transfer/` 2,500-line files: the same systems as `coco_transfer_full5000`.
- g2b `cv295`: not in the dev list; val2017 images.
- `annot_claude.json`: AI labels.

Single family: all usable outputs are Qwen (F1 fine-tunes and zero-shot; F2 Qwen3-VL). This is disclosed until step 7.

## 2. Common definitions (fixed now)

- **Arms.**
  - **L** (label gold, the X5 analogue): C_i = COCO instance classes (coco80), OIV7 present mapped labels (XM3600) or UIT-ViIC instance classes. Level 1 only, with X5's evaluability rule (Σ ℓ_i ≥ 2·Σ q_i, else NOT_EVALUABLE).
  - **U** (all-reference gold, the X4 analogue): C_i = union of all K matched references. COCO and UIT-ViIC only. **At the real K = 5 only level 1 is used. Level 5 equals C_i, so its null is degenerate (p50x returns NOT_EVALUABLE).** XM3600 has no U arm (K = 2–3).
- **The 20-draw statistic T (B2).** T = Σ_S λ_S (1/20) Σ_j F^S(G^{(j)}), where G^{(j)} = (union of k drawn references) ∩ C_i at level k.
  - The draws follow `p50.draw` unchanged: default_rng(1); for r = 1..20 and each image in id order, choice(K, k, replace=False).
  - At K = 5, level 1 repeats references across the 20 draws, unlike K = 50. This is stated. XM3600 draws from its own K (2 or 3).
  - The null is the nested null of `p50x.salience`: one permutation per (replicate, image), and draw j keeps its first q_i^{(j)}. The p-value is (1 + #{T_b ≤ T_0})/(B + 1). The decision is PASS below the interpolated 2.5th percentile. U-arm levels {1, 5} combine with `g.compound`, p = max over levels.
  - Single-draw statistics use reference 1.
- **Images.** Within one set × family × arm, the images are the same across systems. They enter under the pinned `score_g2b` clean rule; counts go to S0.
- **Seeds.** p50 draw seed 1. Base seed 20261106 for everything else; each check × set × arm offset is fixed in the script header before S0.
- **Linear metrics** (S1.N.1 table): P, R, micro-F1, caption CHAIR, and instance CHAIR (only where the matcher emits repeat counts; otherwise omitted, and this is stated). Mixed F1 is not linear.
- **Null kernel.** `p50x.null_slopes` loops in Python over replicates and images, which is about 50 min per COCO D4 simulation at the anchor rate.
  - The checks use one vectorized kernel: integer class slots; h^S as a 0/1 matrix; Z^{(j)} = 1[rank < q_i^{(j)}] from one random key per slot and replicate; segment sums. Weighted draws use keys −ln(u)/a_c.
  - Gate: under identical permutations, the kernel equals `p50x.null_slopes` and `scar_null.null_slopes` to 1e-12, on synthetic data and on 5 replicates of each real cell.
- **Evaluability.** A cell with no evaluable images or systems is NOT_EVALUABLE, never PASS. A check counts toward T2 only if every set it names has at least one evaluable cell.

## 3. S0 freeze and gate (before any D statistic)

1. Write the id lists (ids only, with shas): COCO-5000 (= `manifest_full5000.json`), XM3600-600 (= `xm3600_subset.txt`), UIT-ViIC 231. There is no KT-C side list (N6).
2. Run `build_instance_gold_full5000.py` unchanged into the freeze directory. FAIL unless the output sha is bd36295146e5. No new derivation code.
3. Reproduce the anchors:
   - the r4 cells `inst`, `refs1_firstk`, `refs1_randk` and `refs5_firstk` via `check_coco_full.py` with argv `data/coco_probe/manifest_full5000.json instance_gold_full5000.json all9full <out>` (W4_TOPUP_NOTE l.126). Plain `all9` reads the 2,500-line files. The imported `.session_backup/2026-10-14/r11_litmaps/L1/scripts/check_mstar.py` is pinned at 6e2c0042ac44;
   - the same cells through the `a_dchecks` COCO context;
   - the `check_coco.json` cells (2,500; `data/coco_probe/manifest.json` pinned at 931e572ec8ea);
   - the `c2_n1_uitviic_mstar.json` all_10 cells;
   - the `xm3600_full_verdict.json` v2 cells;
   - the `scar_null_result.json` observed cells for xm600, uv231 and s75.

   Any mismatch beyond the stored rounding stops the run.
4. Record:
   - per system and arm, the count of images whose output reaches 5 classes (N5), so D3(b) NOT_EVALUABLE is known before any D statistic;
   - the kernel speed;
   - the evaluability of every cell.
5. Re-hash every input in §1. Any change stops the run.

## 4. The checks

### D1: Result 1 exactness and the mixed-F1 plug-in error (Thm N.1, Prop. N.2)

- Assumption: a linear metric's null mean is the closed form (indicator → ρ_i). Mixed F1 holds only to first order.
- Data: all sets × families; arms L and U, level 1.
- Per-image inputs: h^S_i, C_i, q_i^{(1)} and q_i^{(j)}.
- Statistic: B = 10,000 uniform q_i-subsets per cell. For each system score and slope of the five linear metrics, z = (closed form − MC mean)/MC SE.
- Family sizes (as in v1): the rule is a maximum over every z, so the Bonferroni count is the number of z statistics, not the number of cells. Counting cells (8) with about 350 z's would give about 2 exceedances under an exact closed form, and the run would stop itself.
  - m_lin = number of linear z's = Σ over cells (set × family × arm) of (number of linear metrics) × (systems + 1 slope).
  - m_mix = number of per-system mixed-F1 tests = Σ over cells of the number of systems.
  - Both counts are written to S0 before any D statistic.
- Pass:
  - linear: max |z| ≤ Φ⁻¹(1 − 0.025/m_lin);
  - mixed F1: every per-system plug-in − MC mean ≥ −Φ⁻¹(1 − 0.05/m_mix)·SE (Prop. N.2(a));
  - every slope |plug-in − MC mean| ≤ 0.5 slope points.

  T is reported beside the single-draw statistic.
- CPU: 15 min.
- FAIL means:
  - linear: an implementation fault; stop and fix;
  - mixed F1: §4.3 drops "first order" as a usable approximation and prints the largest dev error. Printed X4/X5 values stay Monte Carlo means.

### D2: per-reference exchangeability behind the Result 3(a) identity (assumption 5, Thm N.5(a)) (B3)

- Assumption: with exchangeable references (A1), ŵ_ic^{(−k)} (the share of the other K − 1 references naming c) estimates w_ic for reference k. Unconditional on q_i; disclosed.
- Why per k: for linear P, Σ_k (g_obs^{(k)} − g_pred^{(k)}) = 0 identically (CC-266 ruling 3), so the mean over k cannot fail. The test is per k: D^{(k)} has mean 0 under A1 but is not forced to 0, so it tests whether reference k is exchangeable with the other K − 1. The identity mean_k D = 0 is a selftest guard, never the test.
- Data: arm L. COCO-5000 (k = 1..5), UIT-ViIC (k = 1..5), XM3600 (k = 1, 2; images with K = 3 use the other two for ŵ; low precision disclosed). Arm U is excluded, because a class named only by reference k has ŵ^{(−k)} = 0 by construction.
- Statistic: D^{(k)} = g_obs^{(k)} − g_pred^{(k)}, where g_obs^{(k)} = β(Q^{(k)}) − β(ρ^{(k)}) and g_pred^{(k)} = β_δ̂ with δ̂ = ŵ^{(−k)} − ρ^{(k)}. Computed for P and micro-F1. Image bootstrap with 2,000 resamples gives a two-sided p and CI per k.
- Pass:
  - no D^{(k)} rejected after Holm at α = 0.05 over k × set × family × metric;
  - and every per-k 95% CI half-width ≤ 0.5·|g_obs^{(k)}|.
- Labels: a wider CI is UNDERPOWERED (reported, not PASS). A Holm rejection is FAIL. R is descriptive only: its 1/q_i^{(k)} weights make D biased even under A1.
- CPU: 10 min.
- FAIL means: some reference is not exchangeable with the others on dev, so ŵ does not measure w. Result 3 stays an identity in expectation, with no numeric split of the gap via ŵ, and "−19.07" stays observed minus null mean.

### D3: excess nonincreasing in verbosity (assumption 4, Thm N.5(b)–(d)) (B4 i)

- Assumption: e^S = Σ_i Σ_c h^S_ic δ̂_ic / Σ_i M^S_i does not rise with x^S, where δ̂_ic = ŵ_ic − mean_k ρ_i^{(k)} and ŵ is the share of all K references naming c.
- Data: arms L and U, all sets × families. Per-image inputs: as D2, plus word-boundary prefixes of each stored output (read inside the script only, never printed).
- (a) Between systems: Kendall τ of e^S on x^S per cell, reported only.
- (b) Prefix arm, nested by construction:
  - Budgets b ∈ {2, 3, 5}, fixed. Each prefix is the shortest word-boundary prefix whose re-matched class set reaches b.
  - Images per system: those whose full output reaches 5, held constant across levels. Systems with < 100 such images are dropped; a cell with none left is NOT_EVALUABLE.
  - Nesting violations are counted and kept; a sensitivity run without them is reported beside.
- Statistic: Δe_{2→3} and Δe_{3→5}, mention-weighted over systems, per set × family × arm. Image bootstrap with 2,000 resamples.
- SESOI, fixed now: 0.01 excess units per step (δ is a keep-rate difference in [−1, 1]). For each increment:
  - m = the number of evaluable increments over set × family × arm × step, fixed in S0.
  - **FAIL** if Holm (one-sided, α = 0.05, over the m increments) rejects H0: Δe ≤ 0. FAIL takes precedence.
  - **PASS** if not FAIL and the one-sided upper bound at level 1 − 0.05/m is ≤ 0.01.
  - **UNDERPOWERED** if neither (not FAIL, and the upper bound is > 0.01).

  The three labels are disjoint and exhaustive.

  D3 counts toward T2 only if every evaluable increment PASSES.
- Regime (d) is reported at every step: the share of added classes outside C_i, and steps with e < 0.
- CPU: 30 min.
- FAIL means:
  - §4.3 says the excess did not fall monotonically on development data;
  - Result 3(b) stays conditional, with no salience link to the gap's sign;
  - a high regime-(d) share is cited for the "loses power" clause.

  UNDERPOWERED means: "not testable at this precision on development data".

### D4: Result 2 under reference-level SCAR, and Result 3 power (Thm N.3, Prop. N.4)

(a) **SCAR size of the 20-draw statistic (B2).**
- Assumption: under H0^perm, T with the nested null is conservative (proved for P and R under approximate normality; a conjecture for mixed F1). The single-draw test is exact.
- Every simulated reference is an **independent** uniform subset of C_i. Prefixes of one permutation would test H0^nest, which is already proved.
- Two simulated worlds:
  - **W-real** (sets COCO L/U, UIT-ViIC L/U, XM3600 L; F1, F2). Real K. Reference k has size |ref_k ∩ C_i|. In arm U, C_i is the real union, held fixed. Level 1. W-real arm U is a fixed-gold SCAR world: its simulated references need not union to C_i. Only W-50 arm U mirrors X4's union structure.
  - **W-50** (sets COCO, UIT-ViIC, XM3600 arm L; COCO and UIT-ViIC arm U). 50 references per image. Sizes are drawn once per image, with replacement, from the image's real sizes (seed fixed), and then held fixed. Arm L uses level 1 only (as in §2). Arm U uses levels {1, 5} with `g.compound`, mirroring X4. The simulated references are drawn from the arm's real C_i (in arm U, the real 5-reference union). In arm U the null's complete gold is then the union of the 50 simulated references; H0^perm still holds given the union.
- Null sharing (N2): the nested and single-draw nulls depend only on C_i, the q^{(j)} and the outputs. 
  - In W-real and in W-50 arm L (level 1 only), q_i^{(j)} is the fixed size of the drawn reference. So one null (B = 1,000) per cell is shared across simulations, and p-values are i.i.d. given the null. Its quantile error (about ±0.005 on the size at B = 1,000) lies inside the tolerance.
  - In W-50 arm U, C_i and the level-5 sizes change per simulation, so the null is redrawn per simulation, at both levels.
- Statistics: T (mixed F1, P, R) and the single-draw mixed F1.
- Pass:
  - T, one-sided: rejection rate ≤ 0.025 + Φ⁻¹(1 − 0.05/m)·√(0.025·0.975/S), and a one-sided KS test (p smaller than U(0,1)) not rejected at 0.05/m. W-50 arm U uses the compound level rule.
  - Single-draw: a two-sided KS not rejected at 0.05/m (implementation check).
  - m = the number of cells (world × set × family × arm, with W-50 arm U counted once under the compound rule) × 3 T statistics (mixed F1, P, R). It is fixed in S0. The single-draw tests are counted separately (cells × 1).
  - Detectable size (N4): with m about 48, the bound is about 0.059 at S = 200 and 0.072 at S = 100. Only over-rejection above about 6–7% is detected, and the PASS wording says so.
- S = 200. Calibration, fixed now: time the first 5 simulations per cell. No p-value from them is computed or read; they are discarded. If the projected D4(a) wall time exceeds the §6 remainder, S = 100 for every cell. S is never changed after any p-value is seen.
- CPU: about 1 h. W-real costs observed statistics only. W-50 arm U costs 2–5 s per COCO simulation.
- PASS/FAIL wording is always "the 20-draw statistic on development data (simulated references at the real K and sizes, level 1; 50 simulated references, levels 1 and 5)", never "the X4 p-value". Disclosure sentence: "PASCAL-50S outputs cannot be re-checked per image; this is an analogue on development data."
- FAIL means: the 20-draw statistic over-rejects under reference-level random omission on development data. §4.3/§6.6 then do not read "p ≤ 0.001" beyond H0^nest, and Prop. N.4(c)'s conjecture is printed as unsupported. A single-draw FAIL is an implementation fault; stop.

(b) **Salience-correlated thinning** (ALLOWED, CC-266 ruling 8, 88).
- "Simulated references (not gold)". No sentence about real-reference salience is drawn from it.
- Data: COCO-5000, arm L, family F1 only.
- Reference k is size-matched to |ref_k ∩ C_i| and drawn without replacement with weight a_c (the largest box area of class c over the image area). w_ic comes from 10,000 weighted draws per image. S = 100.
- Statistic: Ḡ = mean_s[β_P(sim) − β_P(ρ)] against β_δ, with δ = w − ρ. Power = the rejection rate of T.
- Pass (N3): |Ḡ − β_δ| ≤ 2·√(SE_sim² + SE_w²), where SE_w is from 10 batches of the 10,000 draws. Power and the sign of Ḡ are reported beside D3(a).
- CPU: 30 min.
- FAIL means: an implementation fault, or the identity is not reached. Result 3 is then not illustrated, and no power statement is printed.

### D5: nesting of outputs (strong A3, Thm N.5(c)) (B4 ii)

- Data: same-model short/detailed pairs. F1: zeroshot, distill (COCO), fuse2, p1. F2: T0, T05, T08. vcd has no short pair.
- Statistic: matched share Σ_i |S_i ∩ D_i ∩ C_i| / Σ_i |S_i ∩ C_i|, and the same over all mentioned classes. Image bootstrap, 2,000 resamples.
- Rule: applies to the **lower 95% bootstrap bound (the 2.5th percentile of the two-sided 95% percentile CI)**, not the point estimate (reported beside). If the lower bound is ≥ 0.80 for both shares, reading (c) is allowed for that pair. Otherwise reading (c) is printed only for the D3(b) prefix arm.
- CPU: 5 min.
- FAIL means: §4.3's "nested frontier" sentence is tied to the prefix arm.

## 5. Script outline (not written; the step 8 kit shares it)

`scripts/a_dchecks/a_dchecks.py` has four subcommands:
- `selftest`: Thm N.1 closed form; N.5(c) step identity; check_v2 E1/E2; mean_k D = 0 for P; kernel = p50x under shared permutations.
- `freeze`: S0.1–2.
- `gate`: S0.3–5, computing no D statistic.
- `run`: refuses unless the script and this plan equal their HEAD blobs.

It imports `score_g2b`, `scar_null`, `p50` and `p50x`, with no copies; COCO context as in §1.

Mutants, each to be caught:
- D2 averaged over k;
- the `.get(i, {})` 2,500-gold fallback;
- kernel ≠ p50x;
- S changed after a p-value;
- D5 rule on the point estimate;
- D3 PASS without the SESOI;
- level 5 used at K = 5;
- D3: an increment with 0 < lower bound and upper bound ≤ 0.01 must be FAIL, not PASS;
- D1 with m = cells instead of z statistics;
- a shared null at W-50 level 5.

## 6. Run conditions and stop rule (B5)

- **Laptop only.** `~/.venvs/vsps_h1/bin/python -I`, `OMP_NUM_THREADS=2 OPENBLAS_NUM_THREADS=2 MKL_NUM_THREADS=2 nice -n 15`.
- **Rented hosts.** The v1 rented-host fallbacks are struck; any such move needs its own ruling (CC-266 PQ3, default laptop only).
- **Concurrency.** Not concurrent with C's laptop runs or any other heavy /mnt/d job (EIO history). The coordinator confirms an idle laptop before `run`.
- **Order.** Cheap first: D1, D5, D2, D3, D4(b), D4(a).
- **Cap.** 6 CPU-h or 4 h wall in total, whichever comes first.
- **Stop condition.**
  - When the cap is reached, the running check stops, and it and every later check are written as NOT_RUN.
  - A failed S0 step or kernel gate stops everything before any D statistic.
  - Unfinished checks are never resumed with changed parameters. A resume needs a new plan version and a judge read.
- **Outputs.**
  - `data/results/a_dchecks/freeze/` (id lists, gold copy, shas);
  - `data/results/a_dchecks/gate.json`;
  - `data/results/a_dchecks/selftest.json`;
  - `data/results/a_dchecks/dchecks_result.json`;
  - `data/results/a_dchecks/run_record/` (stdout, stderr, timing, HEAD).
- **Estimate:** S0 20 min + D1 15 + D2 10 + D3 30 + D4(b) 30 + D4(a) 60 + D5 5 ≈ **3 CPU-h, about 2 h wall.** The anchor is `scar_null`: 1,000 replicates over 4 sets in 63 s with the Python set loop. Kernel speed is measured in S0.

## 7. Open items (defaults)

- Q1: D4(b): ALLOWED (CC-266 ruling 8).
- Q2: no KT-C side report (N6, ruling 9). The full split is primary.
- Q3: all 9 COCO systems (yes; matches r4).
- Q4: thresholds as written: 0.5 pt (D1), 0.5·|g_obs^{(k)}| (D2), SESOI 0.01 (D3), lower bound ≥ 0.80 (D5).

## 8. Changes against v1 (f027b70d)

| Item | v1 | v2 |
|---|---|---|
| B1 | §1: "no committed score file covers all 5,000; only 2,500 anchored"; S0 derived the gold anew; score_g2b imported as is | pinned builder dc0d1f52, output bd362951, r4 332da8b6 (51ef280); S0.2 runs the builder unchanged; S0.3 reproduces r4 cells; COCO context built in `a_dchecks` with fail-closed indexing, never `coco_context` |
| B2 | "T exactly as in p50x", levels unstated; FAIL spoke of "the X4 p-value" | T defined (p50.draw, J = 20, levels); arm U at K = 5 is level 1 only, with level 5 degenerate; W-50 world mirrors levels {1, 5}; wording "the 20-draw statistic on development data"; PASCAL disclosure |
| B3 | D2 mean over k (≡ 0 for P) | per-k D^{(k)}, Holm over k × set × family × metric; per-k precision rule; mean-over-k only as a selftest guard |
| B4 | D3 non-rejection = PASS; D5 "share ≥ 0.80" | D3 SESOI 0.01 with PASS/FAIL/UNDERPOWERED; D5 on the lower 95% bound |
| B5 | no cap; rented-host fallbacks | §6: env, threads, nice, 6 CPU-h / 4 h cap, NOT_RUN stop rule, no resume with changed parameters, outputs, no concurrency; rented host needs its own ruling |
| N1 | csv without directory; ind_test p1 seed unstated | full csv path; p1_s42 |
| N2 | null sharing unstated | shared per cell except W-50 arm U |
| N3 | D4(b) tolerance 2·SE_sim | includes SE_w |
| N4 | no detectable size | stated (about 0.057 / 0.070) |
| N5 | — | S0.4 records per-system reach-5 counts |
| N6 | Q2 default yes (KT-C) | no KT-C report |
| other | CPU 3–3.5 h | about 3 h; S0 record list; new mutants |

## 9. Changes against v2 (c07f5a9b), per CC-266r2

| Item | v2 | v3 |
|---|---|---|
| N-B1 | D1 "m = number of cells" with max over all z | m_lin = number of linear z statistics (as in v1), m_mix = number of per-system mixed-F1 tests, both fixed in S0; reason stated |
| N-B2 | W-50 "levels {1, 5}" for all arms; arm L null shared | W-50 arm L level 1 only (shared null valid); arm U levels {1, 5} with `g.compound`, null redrawn per simulation at both levels |
| N-B3 | D3 FAIL "Δe > 0 is rejected"; overlaps PASS; m undefined | FAIL = Holm rejects H0: Δe ≤ 0, and takes precedence; PASS needs not-FAIL plus upper bound ≤ 0.01; labels disjoint and exhaustive; m = evaluable increments |
| N1' | S0.3 argv unstated; check_mstar and manifest.json unpinned | argv `all9full`; check_mstar.py 6e2c0042ac44; manifest.json 931e572ec8ea |
| N2' | "(real K = 2–5, level 1; ...)" | "simulated references at the real K and sizes" |
| N3' | D5 "lower 95% bootstrap bound" | 2.5th percentile of the two-sided 95% percentile CI |
| N4' | D4(a) "m about 24"; timing simulations unstated; W-real U unstated | m count rule (about 48, bound 0.059/0.072); timing simulations compute no p-value; W-real U is a fixed-gold world; shared-null quantile error sentence |
| §5 | 7 mutants | plus the D3 overlap case, D1 m = cells, and a shared null at W-50 level 5 |
| header | v2, CC-266r2 next | v3, CC-266r3 next |
