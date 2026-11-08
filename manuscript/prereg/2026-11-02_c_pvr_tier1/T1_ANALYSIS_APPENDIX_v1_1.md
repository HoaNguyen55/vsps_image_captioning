# T1-ANALYSIS: pre-registered analysis appendix for C-M1 and C-M2 on the C-PVR-T1 tier-1 dev outputs — DRAFT v1.1, not approved

**Status.** DRAFT v1.1 for the round-2 one-judge diff read v1 → v1.1 of CC-292 (round 1/3 = NEXT_ROUND 80; BLOCKING
W1-W3, NON-BLOCKING N1-N8), REVERSIBLE, bar 85 (DEPTH_PLAN §2.3 item 2; PI-1029o as amended by PI-1103ae). v1
(`T1_ANALYSIS_APPENDIX_v1.md`, 05005d76) is unchanged. §14 maps every v1 → v1.1 hunk to its CC-292 item.
It binds only after a GO and a gatekeeper commit that both come **before S16 reads any tier-1 output**. If it is not
committed in time, every C-M1 and C-M2 number is POST_HOC (§9.4). Nothing here was run on real data, and nothing was
committed or written to the LOG.

- **Label:** TIER 1 / DEV-EXPLORE (C-PVR-T1). Every number this file defines is "dev, in-sample (XM3600-vi)".
- **Ordered by:** PI-1107d (LOG l.1758, 2026-11-07T01:59:52Z): write and commit the T1-ANALYSIS appendix before S16.
  - C-M1 is the copy-channel decomposition of PVR − A7, with the A1 over-identification test, and NOT_IDENTIFIED if
    the OR CI contains 1.
  - C-M2 is Manski bounds under unknown labels.
  - Hard rule: it never delays S12-S15. Laptop only.
- **Blindness statement.** v1 was written 2026-11-07T23:00Z-23:20Z and v1.1 2026-11-07T23:46Z-23:48Z (`date -u`), both
  **before any tier-1 output was read**.
  - The S15 tier-1 job was launched by LOG line `OPS-1108a-hc1-t1-launch`, stamped 2026-11-07T22:45:50Z, with T_J1 =
    2026-11-07T22:45:31Z on the host clock.
  - No file under `~/c_pvr_out`, `~/s11pull_*` or `~/c_pvr_watch_*`, on any host, was read, opened, listed or
    stat-ed. No file the run writes was touched either.
  - No S11 §10.3 A1-decomposition file that reaches the laptop during S15 (`W/a1_decomp/*`, `W/PUSHED`,
    `W/watch.log`, `W/ops_side.log`) was read, opened, listed or stat-ed, and no `OPS-*-a1decomp*` LOG line was read.
    LOG reads were targeted greps for named stamps plus the range l.1755-1762, and none printed an a1decomp line
    (CC-292 N7).
  - No label file, manifest, caption or demonstration text was opened.
  - Field names come only from code equal to H = 1880951. `git diff --quiet 1880951` was clean for `c_pvr_gpu.py`,
    `c_pvr.py`, `c_pvr_manifest.py` and `xm3600_oiv7.py` (§13).
- **Binding sources (cited, not restated):**
  - prereg `PREREG_DRAFT_v1_2.md` (0a2f0773, commit 8282874), §3.1-§3.2, §5.2, §5.5, §6.3, §6.4, §12;
  - `PINS_A_DRAFT_v1_4.md` (624b0804, commit 3fb6725), §2.6-§2.7;
  - T1-REP `AMENDMENT_T1_REPORTING_DRAFT_v4.md` (0e9793f3, commit 4124ef3), §1, §2, §4, §6;
  - `S11_RUN_DOC_v1_3.md` (93ac4ee2), §10.3 and §11.
- **Plan source:** `manuscript/directions/DEPTH_PLAN_2026-11-07.md` (e8e2ab45; PI-1107b cites this sha), §2.2-§2.4.

## Tóm tắt cho PI (tiếng Việt)

- C-M1 ước lượng "tốc độ sao chép" κ⁻:
  - mỗi mệnh đề vật thể vắng bị bỏ khỏi demo thì caption bớt bao nhiêu mention vật thể vắng;
  - đo bằng tỉ số Wald gộp trên cặp khớp số lượng PVR-drop / A7.
- C-M1 có hai cổng định danh:
  - G1, cổng của PI: KTC của OR_PVR-drop/OR_A7 chứa 1 thì NOT_IDENTIFIED;
  - G2, cổng thêm: KTC của mẫu số chứa 0, hoặc hơn 1% lần lặp có mẫu số 0, thì NOT_IDENTIFIED (CC-292 W2).
- E1 nay ghi rõ cả tính đồng nhất: mọi đơn vị vắng có cùng κ⁻. Vì vậy E1 bị bác bỏ cũng có thể do bộ kiểm chứng bỏ
  đúng những đơn vị dễ bị sao chép (CC-292 W3).
- Khi G1 không đạt, câu K4 gọi phương pháp là "filtering", đúng luật T1-REP §1 (CC-292 W1).
- Phép kiểm quá định danh dùng A1, Holm trên hai hiệu, như DEPTH_PLAN. Phụ lục ghi rõ hai hiệu này thực ra là một ràng buộc, vì hiệu thứ hai = w × hiệu thứ nhất. Vì vậy phép kiểm bảo thủ (mức 0,025).
- C-M2 cho khoảng **sắc** của hiệu precision tính trên mọi mention, PVR − A8:
  - một cặp (ảnh, lớp) unknown có cùng một sự thật ở cả hai nhánh;
  - khoảng "ghép từng nhánh" trong DEPTH_PLAN đúng nhưng không sắc.
- Không đổi giả thuyết, nhãn, họ Holm, SESOI_P hay luật go/stop nào đã đăng ký. C-M1 không phải phép kiểm H-COPY.
- Mọi câu đều ghi "dev, in-sample (XM3600-vi)".

## 1. Scope: what this file adds and what it leaves alone

**Adds:**
- two non-gating, registered analyses on XM3600-vi tier-1 outputs, computed on the laptop after the registered S16
  score (`c_pvr.py score --tier 1`);
- their labels, fixed sentences, FAULT rules and placement.

**Leaves unchanged** (no registered line is edited):
- the primary contrast PVR − A8 and the prereg §5.2 Holm family;
- SESOI_P, headroom, the §6.3 variant choice and the §12 (iv) go rule;
- the T1-REP §1 "verification" / "filtering" wording rule;
- the T1-REP §4 headline sentences (HW-*);
- the T1-REP §2 identity and its checks;
- the §5.4 tier-3 rule, including condition (3) and the "rule-dependent" label;
- H-COPY's status as a hypothesis, tested only by the registered PVR − A8 and PVR − A1 contrasts (T1-REP §2, "What it
  does not claim").

**Order and isolation.**
- C-M1 and C-M2 run only after S16 has written every registered §12 decision and T1-REP report.
- Their results never feed back into those decisions.

**Not used for identification:**
- A0 (no demonstrations, so b_i changes; DEPTH_PLAN §2.3);
- PVR-keep (not count-matched with A7 at tier 1; PINS-A W5);
- every other set: only XM3600-vi has pinned existing labels at tier 1.

## 2. Inputs (exact fields)

### 2.1 Tier-1 output records (`<set>.<arm>.jsonl`, set = `xm3600_vi`)

Records are written by `c_pvr_gpu.py decode` at H, with `OUT_KEYS` at l.103-105. A field is listed only if the code
writes it for that arm.

| arm | fields used | written by (c_pvr_gpu.py at H) |
|---|---|---|
| A1 | `id`, `demo_ids`, `caption` | `demos_for` returns `st = {}` for A1, so A1 has **no** `masks` and **no** `emptied` |
| PVR-drop | `id`, `demo_ids`, `caption`, `masks`, `emptied`, `calls`, `cap_hits`, `parse_fail`, `yes`, `maybe`, `no` | `CP.pvr_masks` → `st["masks"]`; `demos_after` → `emptied` (int) |
| A7 | `id`, `demo_ids`, `caption`, `emptied` | the A7 branch sets no `st["masks"]`: **A7 masks are not stored** |
| A8 | `id`, `caption`, `emptied` (bool), `calls`, `cap_hits`, `parse_fail`, `yes`, `maybe`, `no` | `CP.a8_caption`; `demo_ids = []` |
| PVR-keep (C-M2 supplement only) | as PVR-drop | as PVR-drop |
| every other VI arm (C-M2 per-arm supplement only) | `id`, `caption` | – |

**A7 masks are recomputed on the laptop.**
- Rule: `CP.a7_masks(id, masks_PVR-drop(id))`, from `c_pvr.py` a503644a.
- Seed: 20262007, one generator per (arm seed, image id), as in PINS-A §2.7.
- These are the same call and the same saved PVR-drop masks that the host used (c_pvr_gpu l.664-666, l.581).
- **What the rebuild rests on (CC-292 N1).** `a7_masks` drops, per demonstration, as many propositions as PVR-drop
  dropped, so the recomputed A7 `emptied` equals PVR-drop's by construction. No field of the A7 records can detect a
  wrong rebuild. The rebuild rests on `c_pvr.py` a503644a plus the interpreter: `random.Random` string seeding under
  CPython 3.12 (host 3.12.3, laptop venv 3.12.3). The S16 run records `sys.version`; a different minor version is a
  FAULT (§9.1 item 10).

### 2.2 Laptop inputs (pinned; opened only at S16)

- **The sealed tier-1 manifest.**
  - It is identified by TMAN = `4849a08f…3efe` (S11 v1.3 header).
  - `manifest/xm3600_vi.json` gives `queries[*].id`, `queries[*].ranked`, and `demos[<id>]` with `text`, `sents`,
    `nouns`, `props[*].{kind, classes, start, end}`.
  - The image universe is every `queries[*].id` of that file, which is 3,600 per OPS-1107c-emb.
  - The §7.4 self-retrieval rule acts on the datastore (the kept-id files), so no query image is removed.
- **Gold:** `data/xm3600/oiv7_labels.json` (bac3953a), through `scripts/xm3600_oiv7.py` `status` / `statuses`
  (9a79403f).
- **Mapping:** `rescap/chair.py` `objects_in(…, raw_tone=False)` (e47d249a), `rescap/vi/lexicon.py` (fbc945f2), and
  the 69 keys of `data/xm3600/vi_oiv7_map.json` (27f2b1ca).
- **Shared arm code:** `scripts/c_pvr/c_pvr.py` (a503644a), functions `a7_masks`, `demos_after` and `rebuild`.
- **S16's registered outputs, used as inputs here:**
  - the T1-REP §2 counts N_A, N_P, ρ, φ for PVR-drop and A7;
  - the CI of OR_PVR-drop / OR_A7;
  - P_obj^VI and P_obj^VI,wrong per arm;
  - the §6.3 variant;
  - the A8 DEGRADED label (S11 §10.3) and the §5.7(b) guard result.
- **No other input.** There are no new labels, and no model-made label is used as evidence.

## 3. Shared definitions

- **Status.** s(i, c) ∈ {present, absent, unknown} = `status()` of (query image i, lexicon class c), exactly as prereg
  §3.1.
- **Caption counts (arm a, image i).**
  - M_a(i) = the set of the 69 map keys in `objects_in(caption_a(i), raw_tone=False)`, each class once per caption.
  - H⁺_a(i) = #{c ∈ M_a(i): s = present}.
  - H⁻_a(i) = #{c ∈ M_a(i): s = absent}.
  - U_a(i) = {(i, c): c ∈ M_a(i), s = unknown}.
  - These are the prereg §3.2 counts. P_obj^VI(a) = ΣH⁺ / Σ(H⁺ + H⁻), and P_obj^VI,wrong(a) = ΣH⁺ / Σ(H⁺ + H⁻ + |U|).
- **Demonstration units (T1-REP §1-§2 unit).**
  - A unit is (demonstration d, class c), where c is a map key carried by an object proposition of d (`props[*]` with
    `kind == "obj"`, `classes`). Each class is counted once per demonstration caption.
  - The pre-filter unit set of image i is common to A1, A7 and PVR-drop, since all three use `ranked[:K]`, K = 4.
- **Surviving units (T1-REP §2 "removed" rule, collateral removals included).**
  - For arm a ∈ {A7, PVR-drop}, rebuild each demonstration with `CP.rebuild(dc, mask)`, which is what `demos_after`
    calls.
  - An emptied demonstration (`None`) keeps no unit.
  - A unit (d, c) survives iff c ∈ `objects_in(rebuilt text of d)` ∩ keys.
  - For A1 every unit survives.
  - A class found in a rebuilt text that was not a pre-filter unit of d is a **created unit**. It is not counted in D,
    and it is reported as a count (expected 0).
- **Demonstration counts.**
  - D⁻_a(i) = number of surviving units of image i with s(i, c) = absent.
  - D⁺_a(i) = the same with s(i, c) = present.
  - Unknown-status units are not counted (T1-REP §2, assumption 1).
- **Equality checks against T1-REP §2.** All are exact integer equalities; any mismatch is a FAULT (§9.1).
  - Σ_i D⁻_A1(i) = N_A and Σ_i D⁺_A1(i) = N_P.
  - Σ_i D⁻_a(i) = N_A(1 − ρ_a) and Σ_i D⁺_a(i) = N_P(1 − φ_a), for a ∈ {PVR-drop, A7}.
- **One helper.** The S16 T1-REP §2 scorer and C-M1 call one shared survival helper (rebuilt text ∩ pre-filter units),
  so that the equality checks test code, not two readings of "removed". This is a coordination item for whoever
  writes `score --tier 1` (CC-292 Ruling 12, N5):
  - the helper also does the A7 mask rebuild, which the registered T1-REP §2 A7 counts need too;
  - its docstring cites T1-REP §2 "removed";
  - with one helper, the equality checks test the aggregation code only. So the helper's own selftest covers each
    clause of the rule: span deletion, sentence drop, emptied demonstrations, and a class kept through another
    proposition.
- **Pair difference.** Δ_{a−b} X(i) = X_a(i) − X_b(i).

## 4. C-M1: copy-channel decomposition with an over-identification test

### 4.1 Model and assumption E1 (exclusion)

For the arms with demonstrations a ∈ {A1, A7, PVR-drop}, every image i, and arm-invariant b⁻_i, b⁺_i:

E[H⁻_a(i)] = b⁻_i + κ⁻ · D⁻_a(i)        E[H⁺_a(i)] = b⁺_i + κ⁺ · D⁺_a(i)

E1 says that the arm acts on absent (present) caption mentions **only** through the count of absent (present) units
left in its demonstrations. It excludes these channels:
- demonstration length;
- emptied demonstrations;
- cross-channel effects;
- unknown-status units.

E1 also assumes **homogeneity and linearity** (CC-292 W3): every surviving absent (present) unit carries the same κ⁻
(κ⁺), whatever the arm's choice of units and whatever the count.

### 4.2 Estimands and estimators

Each estimand is a pooled Wald ratio: a ratio of sums over images, not a mean of per-image ratios.

| name | formula | role |
|---|---|---|
| κ̂⁻(A7−PVR) | Σ_i Δ_{A7−PVR}H⁻(i) / Σ_i Δ_{A7−PVR}D⁻(i) | **main estimate** (count-matched: same removal count and emptied count per demonstration) |
| κ̂⁺(A7−PVR) | Σ_i Δ_{A7−PVR}H⁺(i) / Σ_i Δ_{A7−PVR}D⁺(i) | supplement |
| κ̂⁻(A1−A7), κ̂⁻(A1−PVR) | the same with the A1 contrasts | over-identification (§4.4) |
| κ̂⁺(A1−A7), κ̂⁺(A1−PVR) | the same | supplement, descriptive |

- Under E1 every row of a sign estimates the same κ.
- By §3, Δ_{A1−a}D(i) ≥ 0 for every image.

### 4.3 Identification gates (applied before any κ is printed)

- **G1 (PI-1107d; DEPTH_PLAN §2.3).**
  - If the T1-REP §2 95% CI of OR_PVR-drop / OR_A7, as S16 prints it, contains 1, then κ⁻(A7−PVR) is
    **NOT_IDENTIFIED**.
  - The CI is not recomputed here.
- **G2 (added here, conservative; §11 item 4; CC-292 W2).** Every Wald ratio of §4.2 is **NOT_IDENTIFIED** if either:
  - the 95% percentile CI of its denominator Σ_i ΔD(i) contains 0 (same replicates as §6); or
  - more than 1% of the replicates have a zero denominator.
- **Both fail.** If G1 and G2 both fail for κ⁻(A7−PVR), the label is NOT_IDENTIFIED (G1). G1 is checked before G2.
- **Order.**
  - The gates are applied before anything else.
  - The prereg §5.5 rule (replicates with an undefined ratio are dropped and counted; more than 1% dropped = FAULT)
    applies only to ratios that pass the gates.
  - G2's second clause is exactly the §5.5 threshold, so the §5.5 FAULT cannot fire for a gated-in ratio. It is kept
    as an assert in the code. A weak denominator therefore gives NOT_IDENTIFIED (G2).
  - CC-292's case confirms this: n = 3,600, 400 images at D⁻_A1 = 2 and the rest at 0, D⁻_A7 = D⁻_A1, PVR removing
    one extra absent unit in 4 images, H the same in every arm, seed 20261102, B = 10,000. The denominator CI is [1, 8]
    and 1.82% of replicates are zero, which gives NOT_IDENTIFIED (G2) with no FAULT (§10).
- **NOT_IDENTIFIED means no number for that κ, anywhere.** The numerator and denominator sums and their CIs may appear
  in the supplement, but never their ratio.

### 4.4 Over-identification test (only κ⁻; runs only if κ̂⁻(A7−PVR) and both A1-based κ⁻ ratios are IDENTIFIED)

- δ₁ = κ̂⁻(A1−A7) − κ̂⁻(A7−PVR) and δ₂ = κ̂⁻(A1−PVR) − κ̂⁻(A7−PVR), each computed per bootstrap replicate.
- p_j = min(1, 2 · min(#{δ_j* ≤ 0}, #{δ_j* ≥ 0}) / B_eff), the prereg §5.2 form.
  - B_eff = the replicates kept after dropping the **union** of the undefined replicates of the three κ⁻ ratios.
    The same kept set serves δ₁ and δ₂, and the drop count is printed.
- **Reported p:** the Holm-adjusted p of the smaller member, min(1, 2 · min(p₁, p₂)). With p₁ = p₂ (below) this is
  min(1, 2p). This is the "Holm p" of §8.
- Holm step-down over {p₁, p₂} at family α = 0.05. This family has two members, and the §5.2 family is not changed.
- **E1_REJECTED** iff Holm rejects at least one. Otherwise **E1_NOT_REJECTED**.
- The unadjusted 95% percentile CIs of δ₁ and δ₂ are printed beside them.
- **Algebraic link, stated.** ΔH and ΔD add across arm pairs: (A1−PVR) = (A1−A7) + (A7−PVR).
  - Hence κ̂⁻(A1−PVR) = w·κ̂⁻(A1−A7) + (1 − w)·κ̂⁻(A7−PVR), with w = ΣΔ_{A1−A7}D⁻ / ΣΔ_{A1−PVR}D⁻ > 0.
  - So δ₂ = w·δ₁ in every replicate, and p₁ = p₂.
  - The two differences are **one restriction**. Holm over two equal p-values tests it at 0.025, which is conservative.
    The two-member form is kept because DEPTH_PLAN registers it.
  - |p₁ − p₂| > 1/B_eff is a scorer FAULT (§9.1). One sign flip moves p by 2/B_eff, so in effect this rule means
    p₁ ≠ p₂ (CC-292 N8). Checked on synthetic data at drafting (§10), and by CC-292 on 200 cases with 0 differences.
- **Power, stated.** The test has power against:
  - channels that differ between A1 and the filtered arms, such as length or emptied demonstrations;
  - unit heterogeneity, i.e. κ differing between the units the verifier removes and random units;
  - non-linearity in D (CC-292 W3).
  It has no power against a channel that A7 and PVR-drop share, and a rejection does not say which of these failed.
- If the test does not run: **OVERID_NOT_RUN**, with the failing gate named.

### 4.5 Strata and placebo (descriptive; never gating)

- **Strata** by the pre-filter absent count D⁻_A1(i) ∈ {0, 1, 2, ≥ 3}. This count is computed from the manifest and the
  labels only, and is arm-independent.
- In strata 1, 2 and ≥ 3: κ̂⁻(A7−PVR) per stratum, with G2 per stratum and the CI, plus κ̂⁻(≥ 3) − κ̂⁻(1) with its CI.
  This is the linearity check of DEPTH_PLAN §2.3. It carries no label.
- **Placebo (stratum 0).** There, D⁻_a(i) = 0 for every arm, so E1 implies E[Δ_{A7−PVR}H⁻(i)] = 0.
  - Report the per-image mean of Δ_{A7−PVR}H⁻ with its 95% CI.
  - **PLACEBO_CONSISTENT** if the CI contains 0, else **PLACEBO_INCONSISTENT**.
  - The placebo does not change the §4.4 verdict.

### 4.6 Accounting decomposition (the DEPTH_PLAN "Hệ quả"; supplement)

- **Formula.** For a verifier with removal rates (ρ, φ) on the same pre-filter units:

  P̂(PVR) = [ΣH⁺_A7 − κ⁺·N_P(φ_PVR − φ_A7)] / [ΣH⁺_A7 − κ⁺·N_P(φ_PVR − φ_A7) + ΣH⁻_A7 − κ⁻·N_A(ρ_PVR − ρ_A7)]

- **Tier 1: not a prediction.** κ̂ comes from the same PVR − A7 contrast, so P̂ reproduces the observed P_obj^VI(PVR-drop)
  exactly. A difference of more than 1e-9 is a FAULT.
- It is printed with the channel split:
  - ΔP⁻ = P with only H⁻ moved to PVR-drop, minus P_A7;
  - ΔP⁺ = the same with only H⁺ moved;
  - the remainder.
- Label: "accounting, in-sample, not a test".
- The predictive use (κ frozen at tier 1 and applied to tier-2 (ρ, φ)) is a tier-2 prereg item. This file does not
  register it.
- Printed only when both κ⁻ and κ⁺ (A7−PVR) are IDENTIFIED.

### 4.7 C-M1 labels (wording fixed now)

| label | condition |
|---|---|
| IDENTIFIED / NOT_IDENTIFIED (G1) / NOT_IDENTIFIED (G2) | §4.3, per ratio |
| E1_NOT_REJECTED / E1_REJECTED / OVERID_NOT_RUN | §4.4 |
| PLACEBO_CONSISTENT / PLACEBO_INCONSISTENT | §4.5 |
| POST_HOC | §9.4; replaces every label above |
| FAULT | §9.1; no number |

## 5. C-M2: sharp bounds under unknown status

### 5.1 Estimand

- The target is **all-mention object precision**: P_all(a) = (ΣH⁺_a + Σ_{u ∈ U_a} x_u) / n_a.
  - n_a = Σ_i (H⁺_a + H⁻_a + |U_a|)(i), the number of mapped mentions.
  - x_u ∈ {0, 1} is the unobserved truth of unknown pair u = (i, c).
- It is not the primary P_obj^VI, which drops unknown mentions.
- **Per arm**, with no assumption: P_all(a) ∈ [L_a, U_a], where L_a = ΣH⁺/n_a = P_obj^VI,wrong(a), the registered
  sensitivity of prereg §3.2, and U_a = (ΣH⁺ + Σ|U_a|)/n_a. Both bounds are attained, so they are sharp.
- **Contrast:** Δ_all = P_all(PVR) − P_all(A8), paired by image.
  - PVR = the variant that S16 fixes by prereg §6.3 (iii).
  - If §6.3 STOPs with no variant carried, PVR-drop. This fallback is set **by this appendix**: it is A7's tier-1
    variant, PINS-A l.158-159 (CC-292 N4).
  - Both variants go in the supplement.

### 5.2 Sharp bounds for the difference

- **Why the arms must be coupled.** One unknown pair (i, c) mentioned by both arms has **one** truth x_u. So the
  per-arm combination [L_PVR − U_A8, U_PVR − L_A8] is valid but not sharp.
- **Linear form.** Once the unknowns are resolved, the denominators n_a are fixed, so Δ_all is linear in x:
  - Δ_all = base + Σ_u c_u x_u;
  - base = ΣH⁺_PVR/n_PVR − ΣH⁺_A8/n_A8;
  - c_u = 1[u ∈ U_PVR]/n_PVR − 1[u ∈ U_A8]/n_A8.
- **Sharp bounds:** Δ_lo = base + Σ_u min(0, c_u) and Δ_hi = base + Σ_u max(0, c_u).
- **Per-image rows.** Let S_P(i), S_8(i) and S_b(i) be the counts of image i's unknown pairs mentioned by PVR only, by
  A8 only and by both. Then:
  - Δ_lo = base − ΣS_8/n_A8 + ΣS_b · min(0, 1/n_PVR − 1/n_A8);
  - Δ_hi = base + ΣS_P/n_PVR + ΣS_b · max(0, 1/n_PVR − 1/n_A8).
  - These equalled brute force over every x on 300 synthetic cases at drafting (§10).
- **Proposition.**
  - Δ_lo and Δ_hi are sharp bounds: both ends are attained with no assumption on x. The identified set is finite; it
    lies in [Δ_lo, Δ_hi] and contains both ends (CC-292 N3).
  - The sign of Δ_all is identified iff [Δ_lo, Δ_hi] excludes 0.
  - This formalises the registered "unknown = wrong" sensitivity: each arm's lower end is P_obj^VI,wrong. It does
    **not** change §5.4 (3) or the "rule-dependent" label.

### 5.3 Monotone narrowing (exact form fixed now; supplement, descriptive)

- **Assumption MA_a.** The present rate among arm a's unknown mentions is at most its rate among known mentions:
  Σ_{u ∈ U_a} x_u ≤ P_obj^VI(a) · Σ|U_a|.
- Under MA_a: P_all(a) ∈ [P_obj^VI,wrong(a), P_obj^VI(a)].
- Outer bound on the difference under MA on both arms: [P_wrong(PVR) − P_obj(A8), P_obj(PVR) − P_wrong(A8)].
- This bound is valid but not sharp. It carries no sign label, and the paper may cite it only together with "under the
  stated monotonicity assumption MA".

### 5.4 Inference and labels (wording fixed now)

- Bootstrap (§6) on the per-image rows (H⁺_P, n_P(i), H⁺_8, n_8(i), S_P, S_8, S_b). Δ_lo* and Δ_hi* are recomputed per
  replicate.
- **95% band** = [q_2.5(Δ_lo*), q_97.5(Δ_hi*)]. This is a conservative union, chosen over Imbens-Manski for
  simplicity, and stated so.
- **SIGN_IDENTIFIED_POS** iff the band's lower end > 0.
- **SIGN_IDENTIFIED_NEG** iff the band's upper end < 0.
- **SIGN_NOT_IDENTIFIED** otherwise.
- **Inherited labels.**
  - If S16 labels A8 on xm3600_vi DEGRADED (S11 v1.3 §10.3), the C-M2 label carries "DEGRADED".
  - If the §5.7(b) guard makes the primary contrast INCONCLUSIVE, the C-M2 label carries "INCONCLUSIVE".
  - In both cases the paper may not use the label as a claim.
- **Per arm** (supplement): L_a, U_a, the unknown count and the unknown share, for every VI arm on XM3600-vi.

## 6. Inference settings (shared by C-M1 and C-M2)

- **Bootstrap.** Prereg §5.5:
  - unit = image; paired: one image resample serves A1, A7, PVR-drop, PVR-keep and A8 together;
  - B = 10,000; percentile 95% CI (2.5 / 97.5).
- **Draw form.** The house form of `scripts/vsps_j_e2b/e2b.py` `boot()`:
  - `W = numpy.random.default_rng(20261102).multinomial(n, [1/n]*n, size=B)`;
  - replicate sums = `W @ rows`, with the rows in sorted image-id order;
  - one W for every statistic of this file.
- **Seed.** 20261102 is the prereg §5.5 tier-1 seed. It lies outside the PINS-A §2.7 arm seeds and the tier-2 power
  streams 20261103 and 20261104 + r.
- **numpy** is the version pinned in `scripts/c_pvr/requirements_c_pvr.lock` (2.5.4).
- **Multiplicity.**
  - The only Holm family here is the two-member §4.4 family (α = 0.05).
  - Every other interval in this file is a descriptive 95% CI with no multiplicity claim.
  - The prereg §5.2 family is unchanged, and no C-M1 or C-M2 quantity enters it.
- **Dropped replicates.** §4.3 order. Counts are printed for every ratio.

## 7. Placement in Paper C

**Main text** (analysis section, each sentence labelled "dev, in-sample (XM3600-vi)"):
- **M1:** the κ̂⁻(A7−PVR) sentence of §8, or its NOT_IDENTIFIED sentence;
- **M2:** the E1 verdict, with δ₁ [CI] and the Holm-adjusted p (only if §4.4 ran);
- **M3:** the placebo clause, only if PLACEBO_INCONSISTENT;
- **M4:** the C-M2 sentence for PVR − A8, with [Δ_lo, Δ_hi], the 95% band and the unknown shares.

**Supplement:**
- κ̂⁺ and all six Wald ratios, with numerators, denominators, CIs, G1 and G2 values, w, δ₂ and both p;
- the strata table and the placebo;
- the §4.6 decomposition and channel split;
- the created-unit count;
- C-M2 per-arm bounds for every VI arm, the per-arm (non-sharp) combination, the MA outer bound, and both PVR variants;
- replicate drops and input shas.

No sentence uses priority wording or any wording that PI-1101o bars.

## 8. What the paper may and may not claim (sentences fixed now; x [CI] filled from the output)

**C-M1, one sentence chosen mechanically:**

| case | condition | sentence |
|---|---|---|
| K1 | κ⁻(A7−PVR) IDENTIFIED, E1_NOT_REJECTED | "On the development set, in the count-matched contrast (PVR-drop vs A7), each additional absent object class carried by a demonstration (counted once per demonstration) went with x [CI] additional absent-object mentions in the captions. Under the stated exclusion assumption E1 (including a common copy rate across units), this is the rate at which absent demonstration objects are copied into captions; an over-identification test against unfiltered demonstrations did not reject E1 (δ = x [unadjusted 95% CI], Holm p = y)." |
| K2 | IDENTIFIED, E1_REJECTED | "On the development set, in the count-matched contrast (PVR-drop vs A7), each additional absent object class carried by a demonstration (counted once per demonstration) went with x [CI] additional absent-object mentions in the captions. An over-identification test rejected the exclusion assumption E1 (δ = x [unadjusted 95% CI], Holm p = y): the contrasts with unfiltered demonstrations imply a different ratio. So either the effect on captions also runs through a channel other than the count of absent demonstration objects (such as demonstration length or emptied demonstrations), or the copy rate differs between the units the verifier removes and other units, or with their number; the test does not separate these, and the ratio is not read as a copy rate." |
| K3 | IDENTIFIED, OVERID_NOT_RUN | the opening sentence of K1, then: "E1 could not be tested on this set ([gate] not met), so the ratio is reported under E1 untested." |
| K4 | NOT_IDENTIFIED (G1); also when G1 and G2 both fail | "On the development set, filtering (PVR-drop) did not remove absent-object propositions at a rate distinguishable from count-matched random removal (OR_PVR-drop / OR_A7 = x [CI]), so this design does not identify the copy channel and no rate is reported." |
| K5 | NOT_IDENTIFIED (G2) | "On the development set, the count-matched contrast did not change the number of absent demonstration objects distinguishably from zero (Σ ΔD⁻ = x [CI]), so this design does not identify the copy channel and no rate is reported." |
| no C-M1 sentence | NOT_RUN (§9.2), FAULT (§9.1) or POST_HOC (§9.4) | none in the main text; one supplement line "C-M1 not computed: <reason>" (CC-292 N2(c)) |
| placebo clause | PLACEBO_INCONSISTENT, appended to K1-K3 | "Among images whose unfiltered demonstrations held no absent-object proposition, the same contrast still changed absent-object mentions (x [CI] per image), which E1 rules out." |

**C-M2, one sentence:**

| case | sentence |
|---|---|
| SIGN_IDENTIFIED_POS | "With no assumption about mentions whose status the existing labels leave unknown, all-mention object precision was higher under PVR than under A8 on the development set (sharp bounds [lo, hi]; 95% band [a, b]; unknown share x% PVR, y% A8)." |
| SIGN_IDENTIFIED_NEG | the same with "lower" in place of "higher" |
| no C-M2 sentence | NOT_RUN, FAULT or POST_HOC | none in the main text; one supplement line "C-M2 not computed: <reason>" (CC-292 N2(c)) |
| SIGN_NOT_IDENTIFIED | "With no assumption about mentions whose status the existing labels leave unknown, the sign of the PVR − A8 difference in all-mention object precision is not identified on the development set (sharp bounds [lo, hi]; 95% band [a, b]); the primary rule excludes those mentions (unknown share x% PVR, y% A8)." |

"[unadjusted 95% CI]" is the unadjusted percentile interval of δ₁ from §4.4. It is printed with that word, so a CI
that excludes 0 next to "did not reject" (0.025 < p ≤ 0.05, §4.4) is not misread (CC-292 N2(a)). The method is named
only by the T1-REP §1 rule: "verification" iff rules (i) and (ii) hold, otherwise "filtering". K4 fires only when
rule (i) fails, so it says "filtering" (CC-292 W1).

**May, in each case, only as written above:**
- K1: a copy rate of absent demonstration objects, always "under the stated exclusion assumption E1", and "E1 was not
  rejected" (never "holds", "confirmed" or "shown").
- K2: that the effect on captions is not explained by a common per-unit rate on the absent-object count alone.
- K4 and K5: that the tier-1 design does not identify the channel.
- C-M2: what the identified set says about all-mention precision.

**May not, in any case:**
1. Call C-M1 a test, confirmation or measurement of H-COPY. H-COPY stays a hypothesis tested only by the registered
   PVR − A8 and PVR − A1 contrasts (T1-REP §2).
2. Present κ as an effect of the verifier when E1 is rejected or untested, or present κ̂⁻(A7−PVR) under K2 as a copy
   rate. The method is named only by the T1-REP §1 rule (CC-292 W1).
3. Use any C-M1 or C-M2 result to change, support or replace:
   - the "verification" / "filtering" rule (T1-REP §1);
   - the HW-* headline;
   - SESOI_P, the variant choice or the go/stop;
   - the primary contrast or the §5.2 family.
4. Present the §4.6 decomposition as a prediction or a validation at tier 1.
5. Extend C-M1 beyond object propositions mapped to the 69 classes. Excluded: attributes, relations, counts, scene
   text, unknown-status units, sets other than XM3600-vi, any test set.
6. Claim linearity beyond the observed strata.
7. Present the C-M2 band as a CI of the primary P_obj^VI, or read SIGN_IDENTIFIED as a PASS, a primary result, or a
   change to §5.4 (3).
8. Use any tier-1 sentence without "dev, in-sample (XM3600-vi)". Tier 1 has no PASS.
9. Use any priority or novelty word. The method lineage is the one in DEPTH_PLAN §2.3-§2.4 (Li et al. ACL 2024; the
   partial-identification works it names), cited after a source check.

## 9. Failure, FAULT and POST_HOC handling

### 9.1 FAULT (no C-M1 / C-M2 number; one OPS line by the coordinator; fix under a one-judge read)

1. Any input sha of §2 differs. This covers each output jsonl against its pulled sha record, the manifest against
   TMAN, and every pinned file.
2. `RESCAP_RAW_TONE` is set (prereg §3.1 N4).
3. For any image:
   - `demo_ids` differ across A1, A7 and PVR-drop, or differ from `[str(x) for x in ranked[:4]]` of the manifest. This
     is the same normalisation as `norm_ids` (c_pvr_gpu l.281-286), which does not filter (CC-292 N2(d));
   - PVR-drop `masks` do not match the manifest `props` in shape;
   - the recomputed `emptied` differs from the saved `emptied` of PVR-drop or A7. For A7 this is a consistency check
     only: it holds by construction and cannot detect a wrong rebuild (§2.1, CC-292 N1).
4. An image id is duplicated in any arm file.
5. Any §3 equality check against T1-REP §2 fails.
6. A P_obj^VI or P_obj^VI,wrong recomputed from §3 counts differs from S16's registered value (A1, A7, PVR-drop,
   PVR-keep, A8).
7. |p₁ − p₂| > 1/B_eff (§4.4), or the §4.6 reproduction is off by more than 1e-9.
8. More than 1% undefined replicates for a gated-in ratio (prereg §5.5). After G2 (§4.3) this cannot fire; it is kept
   as an assert.
9. If T1-REP §1 or §2 is itself a FAULT, C-M1 is not computed. C-M2 still runs if checks 1, 2, 4 and 6 pass for its
   arms.
10. `sys.version` of the S16 run has a different minor version from the host's CPython 3.12 (§2.1, CC-292 N1).

**A re-run after a fix:**
- It uses the same outputs and the same seed. The analysis is deterministic and dev-only, so a re-run is not a new
  look at a test set.
- Every number carries "re-run after FAULT <OPS id>, code <sha>".

### 9.2 Missing data (a run outcome, not a FAULT)

- If any of A1, A7 or PVR-drop lacks any of the 3,600 ids (a JOB STOP or a machine loss), C-M1 is **NOT_RUN**. It is
  never run on a partial set, and the missing count is printed.
- The same holds for C-M2 if PVR or A8 is incomplete.
- Phase 1 holds A1, A7 and PVR-drop, and phase 2 holds A8. A cap stop falls only on phase 3 (S11 v1.3 §10.1), so a cap
  stop does not trigger this branch.

### 9.3 DEGRADED / INCONCLUSIVE
These are inherited as in §5.4. C-M1 does not use A8, so it inherits neither.

### 9.4 POST_HOC
- If this file has no GO and gatekeeper commit before S16 reads any tier-1 output, every C-M1 and C-M2 number is
  **POST_HOC**: descriptive only, with no IDENTIFIED, E1 or SIGN label and no §8 sentence in the main text.
- The same applies to any part edited after S16 starts reading.
- The appendix never holds the machine or delays S12-S15 (PI-1107d).

## 10. Code sketch (synthetic data only; no real data)

The sketch was run at drafting with `~/.venvs/c_pvr/bin/python -I` on synthetic arrays and printed `sketch selftest
OK`. A separate synthetic check confirmed:
- the §4.4 identity (200 cases);
- that the sketch rejects E1 when A1 alone carries a length channel, and that it drops and counts undefined
  replicates without a FAULT when they are below 1%;
- that CC-292's W2 case (§4.3) gives NOT_IDENTIFIED (G2) with no FAULT (denominator CI [1, 8], 1.82% zero), and the
  same data with an OR CI containing 1 gives NOT_IDENTIFIED (G1);
- that the §5.2 bounds equal brute force over every x (300 cases);
- that the per-arm combination is never narrower.

The S16 implementation is a new function file under `scripts/c_pvr/`, with this selftest, written after the GO. It
reads §2 inputs only and builds per-image rows by §3.

```python
import numpy as np

SEED, B, ALPHA = 20261102, 10_000, 0.05          # prereg §5.5, §5.2


def boot(rows, seed=SEED, b=B):                   # e2b.py boot(): multinomial image weights, one W for everything
    rows = np.asarray(rows, float)
    n = len(rows)
    return np.random.default_rng(seed).multinomial(n, [1 / n] * n, size=b) @ rows


def pct(v):
    return [float(np.percentile(v, 2.5)), float(np.percentile(v, 97.5))]


def p2(d):                                        # prereg §5.2 two-sided bootstrap p
    return min(1.0, 2 * min((d <= 0).sum(), (d >= 0).sum()) / len(d))


def holm(ps, alpha=ALPHA):
    order, rej = sorted(range(len(ps)), key=ps.__getitem__), [False] * len(ps)
    for k, j in enumerate(order):
        if ps[j] > alpha / (len(ps) - k):
            break
        rej[j] = True
    return rej


def cm1(rows, or_ci):
    """rows[i] = (H-_A1, H-_A7, H-_PVR, D-_A1, D-_A7, D-_PVR); or_ci = T1-REP §2 CI of OR_PVR-drop / OR_A7."""
    R = np.asarray(rows, float)
    H, D = R[:, :3], R[:, 3:]
    pairs = {"A7-PVR": (1, 2), "A1-A7": (0, 1), "A1-PVR": (0, 2)}
    cols = np.column_stack([np.column_stack([H[:, a] - H[:, b], D[:, a] - D[:, b]]) for a, b in pairs.values()])
    pt, T, out = cols.sum(0), boot(cols), {}
    for k, name in enumerate(pairs):
        dci, bad = pct(T[:, 2 * k + 1]), T[:, 2 * k + 1] == 0
        gate = None
        if name == "A7-PVR" and or_ci[0] <= 1 <= or_ci[1]:     # G1 (PI-1107d), checked before G2
            gate = "G1"
        elif not (dci[0] > 0 or dci[1] < 0) or bad.mean() > 0.01:  # G2: denominator CI holds 0, or > 1 % zero
            gate = "G2"
        ok = gate is None
        with np.errstate(divide="ignore", invalid="ignore"):
            r = T[:, 2 * k] / T[:, 2 * k + 1]
        assert not (ok and bad.mean() > 0.01)                  # prereg §5.5 FAULT: unreachable after G2
        out[name] = {"label": "IDENTIFIED" if ok else "NOT_IDENTIFIED", "gate": gate, "den_ci": dci,
                     "kappa": float(pt[2 * k] / pt[2 * k + 1]) if ok else None,
                     "ci": pct(r[~bad]) if ok else None, "rep": r, "bad": bad, "dropped": int(bad.sum())}
    if any(out[k]["label"] != "IDENTIFIED" for k in out):
        return out, "OVERID_NOT_RUN"
    keep = ~(out["A7-PVR"]["bad"] | out["A1-A7"]["bad"] | out["A1-PVR"]["bad"])  # one drop set for both differences
    d1 = (out["A1-A7"]["rep"] - out["A7-PVR"]["rep"])[keep]
    d2 = (out["A1-PVR"]["rep"] - out["A7-PVR"]["rep"])[keep]
    ps = [p2(d1), p2(d2)]
    if abs(ps[0] - ps[1]) > 1 / keep.sum():                    # d2 = w d1, w > 0 (§4.4); only |d| ~ 0 may differ
        raise SystemExit("FAULT: over-identification p-values differ")
    out["overid"] = {"p": ps, "p_holm": min(1.0, 2 * min(ps)), "B_eff": int(keep.sum()), "ci": [pct(d1), pct(d2)]}
    return out, "E1_REJECTED" if any(holm(ps)) else "E1_NOT_REJECTED"


def cm2(rows):
    """rows[i] = (H+_P, n_P, H+_8, n_8, S_P, S_8, S_b) per image (§5.2)."""
    def bounds(t):
        kp, np_, k8, n8, sp, s8, sb = (t[..., j] for j in range(7))
        base, c = kp / np_ - k8 / n8, 1 / np_ - 1 / n8
        return base - s8 / n8 + sb * np.minimum(0, c), base + sp / np_ + sb * np.maximum(0, c)
    R = np.asarray(rows, float)
    lo, hi = bounds(R.sum(0))
    blo, bhi = bounds(boot(R))
    band = [float(np.percentile(blo, 2.5)), float(np.percentile(bhi, 97.5))]
    lab = "SIGN_IDENTIFIED_POS" if band[0] > 0 else "SIGN_IDENTIFIED_NEG" if band[1] < 0 else "SIGN_NOT_IDENTIFIED"
    return float(lo), float(hi), band, lab


if __name__ == "__main__":                        # synthetic only: no dataset, no output file
    g = np.random.default_rng(7)
    n = 400
    d1 = g.integers(0, 5, n)
    dpvr, d7 = d1 - np.minimum(d1, g.integers(0, 3, n)), d1 - np.minimum(d1, g.integers(0, 2, n))
    flags = [g.random(k) < 0.4 for k in d1]                    # E1 true: each kept absent unit copied w.p. 0.4
    base = g.poisson(0.3, n)                                   # arm-invariant b_i
    h = [base + np.array([f[:k].sum() for f, k in zip(flags, d)]) for d in (d1, d7, dpvr)]
    res, verdict = cm1(np.column_stack([*h, d1, d7, dpvr]), or_ci=(0.6, 0.9))
    assert res["A7-PVR"]["label"] == "IDENTIFIED" and abs(res["A7-PVR"]["kappa"] - 0.4) < 0.2
    assert cm1(np.column_stack([*h, d1, d7, dpvr]), or_ci=(0.8, 1.1))[0]["A7-PVR"]["label"] == "NOT_IDENTIFIED"
    hl = [h[0] + g.poisson(1.0, n), h[1], h[2]]                # E1 false: a length channel only A1 has
    assert cm1(np.column_stack([*hl, d1, d7, dpvr]), or_ci=(0.6, 0.9))[1] == "E1_REJECTED"
    d7s = d1.copy()                                            # A1-A7 moves D in 5 images only: replicates drop
    d7s[np.flatnonzero(d1 > 0)[:5]] -= 1
    hs = [base + np.array([f[:k].sum() for f, k in zip(flags, d)]) for d in (d1, d7s, dpvr)]
    rs, vs = cm1(np.column_stack([*hs, d1, d7s, dpvr]), or_ci=(0.6, 0.9))
    assert rs["A1-A7"]["dropped"] > 0 and vs in ("E1_NOT_REJECTED", "E1_REJECTED") and rs["overid"]["B_eff"] < B
    z = np.zeros(3600, int)                                    # CC-292 W2 case: CI [1, 8], about 1.8 % zero
    z[:400] = 2
    zp = z.copy()
    zp[:4] -= 1
    hz = np.zeros(3600, int)
    rz, vz = cm1(np.column_stack([hz, hz, hz, z, z, zp]), or_ci=(0.6, 0.9))
    assert rz["A7-PVR"]["gate"] == "G2" and vz == "OVERID_NOT_RUN", rz["A7-PVR"]["den_ci"]
    assert cm1(np.column_stack([hz, hz, hz, z, z, zp]), or_ci=(0.8, 1.1))[0]["A7-PVR"]["gate"] == "G1"
    assert holm([0.01, 0.04]) == [True, True] and holm([0.03, 0.03]) == [False, False]
    m = np.column_stack([g.integers(1, 4, n), np.full(n, 6), g.integers(1, 4, n), np.full(n, 6),
                         g.integers(0, 2, n), g.integers(0, 2, n), g.integers(0, 2, n)])
    lo, hi, band, lab = cm2(m)
    assert lo <= hi and band[0] <= lo and hi <= band[1]
    print("sketch selftest OK", verdict, vs, rs["A1-A7"]["dropped"], rz["A7-PVR"]["den_ci"],
          round(float(rz["A7-PVR"]["bad"].mean()), 4), lab)
```

## 11. Consistency with DEPTH_PLAN and T1-REP (points found and how they are resolved)

1. **A7 masks are not in the outputs** (DEPTH_PLAN §2.3: "output của mỗi nhánh lưu `demo_ids` và `masks`").
   - At H, only PVR-drop, PVR-keep and A4 records carry `masks`. A7 has `emptied` and no `masks`, and A1 has neither.
   - Resolution:
     - A7 masks are recomputed by the same `CP.a7_masks` call from PVR-drop's saved masks, as DEPTH_PLAN's own
       "A7 dựng lại từ masks đã lưu của PVR-drop" says;
     - the saved `demo_ids` are a FAULT check (§9.1 item 3). The A7 `emptied` check holds by construction and cannot
       detect a wrong rebuild, which rests on the code sha plus CPython 3.12 (§2.1; CC-292 Ruling 1, N1).
   - No GPU field is needed or added.
2. **D⁻ / D⁺ from masks vs T1-REP §2 "removed".**
   - DEPTH_PLAN defines D by status() and `objects_in`. T1-REP §2 counts collateral removals: sentence drop and
     emptied demonstrations.
   - Resolution: D comes from the rebuilt text (§3), with exact equality checks against N_A(1 − ρ) and N_P(1 − φ).
3. **The over-identification test is one restriction.**
   - DEPTH_PLAN registers Holm over two differences. They are algebraically linked (δ₂ = w·δ₁).
   - Resolution: the registered form is kept, the link is stated, and it is used as a FAULT check. The test is
     conservative (effective level 0.025).
4. **G1 alone does not make ΣΔD⁻ ≈ 0.**
   - DEPTH_PLAN reads "OR CI contains 1" as "ΣΔD⁻ ≈ 0". These are related but not equivalent: the OR ratio involves φ
     too.
   - Resolution:
     - G1 is kept verbatim (PI-1107d);
     - G2 is added on every denominator, which can only add NOT_IDENTIFIED outcomes;
     - the gates come before the §5.5 FAULT rule, and G2 also fires at > 1% zero denominators, so a weak
       denominator never reaches that FAULT (CC-292 W2).
5. **The "Hệ quả" prediction is circular at tier 1.** κ̂ is estimated from the same PVR − A7 contrast. Resolution: it
   is registered as an accounting decomposition (§4.6), and the predictive form goes to the tier-2 prereg.
6. **C-M2 sharpness.**
   - DEPTH_PLAN's per-arm combination for the paired difference is valid but not sharp, because shared unknown pairs
     have one truth.
   - Resolution: the coupled linear form of §5.2. The Manski-Pepper "example" is fixed as the exact MA_a constraint
     (§5.3) and kept descriptive.
7. **H-COPY wording.**
   - DEPTH_PLAN says C-M1 turns H-COPY into a measured parameter. T1-REP §2 says H-COPY is tested only by PVR − A8 and
     PVR − A1.
   - Resolution: C-M1 is a model-based estimate under E1, never a test of H-COPY (§8, may not, item 1). T1-REP wins.
8. **"PVR" in C-M2.** DEPTH_PLAN does not name the variant. Resolution: the prereg §6.3 (iii) variant that S16 fixes,
   with both variants in the supplement. The PVR-drop fallback on a §6.3 STOP is set by this appendix (A7's tier-1
   variant, PINS-A l.158-159; CC-292 N4).
9. **The NoCaps line of DEPTH_PLAN §2.3 item 4** is outside tier 1 and is not used here.
10. **What "khoảng cho P_obj^VI" means (CC-292 N3).** The C-M2 estimand P_all is P_obj^VI under complete labels.
    DEPTH_PLAN's "khoảng cho P_obj^VI" is read this way, since the primary P_obj^VI drops unknown mentions.
11. **Homogeneity (CC-292 W3).** DEPTH_PLAN's E1 lists only excluded channels. The model also assumes one κ per sign
    for every unit. That assumption is now part of E1 (§4.1), and the power line, K1, K2 and the K2 may-line follow
    from it.

## 12. Ruling requested (one judge, REVERSIBLE 85)

| # | question | recommended | default if no answer |
|---|---|---|---|
| J-1 | Are CC-292 W1-W3 closed as written (K4 "filtering"; G2 with the > 1% clause and the sketch; E1 homogeneity, the power line, K1 and K2)? | YES | – |
| J-2 | Are N1-N8 applied, in particular N2(a)-(d) and N7? | YES | – |
| J-3 | Is the v1 → v1.1 diff limited to the §14 hunks? | YES | – |

## 13. Drafting-touch disclosure

**Read:**
- for v1.1: CC-292 (whole);
- DEPTH_PLAN e8e2ab45 (§0, §2);
- T1-REP v4 0e9793f3 (whole);
- prereg v1.2: §2.1-§2.3, §3, §4.1, §5, §6, §7.4, §11-§13;
- PINS-A v1.4 §2.6-§2.8;
- S11 v1.3: header, §10, §11;
- LOG lines PI-1107b, PI-1107d, OPS-1108a-hc1-p1, OPS-1108a-hc1-t1-launch, the CC-253r3/r4, PI-1105g and
  OPS-1105c-rep-commit lines, and OPS-1107c-emb;
- code at H, read for field names only:
  - `c_pvr_gpu.py` l.1-140 and l.540-760 (`git show 1880951:`);
  - `c_pvr.py` l.269-372, l.449-520 and l.587-690;
  - `c_pvr_manifest.py` docstring;
  - `xm3600_oiv7.py` `status` / `statuses`;
  - `e2b.py` `boot` / `paired_ci`;
  - the numpy line of `requirements_c_pvr.lock`.

**Not opened:**
- any tier-1 output, log, marker or pull directory, on any host;
- the manifest;
- `oiv7_labels.json` and any label file;
- any caption or demonstration text;
- `~/.vsps_sealed` and any `t2pool_*` file;
- any NoCaps, TextCaps or OI test material;
- any COCO annotation file, by hand. The house NGRAM scanner (§13, last item) reads its own pinned caption corpora and
  prints counts only.

**Hashed:** DEPTH_PLAN, prereg v1.2, PINS-A v1.4, S11 v1.3, T1-REP v4, `c_pvr.py` and `c_pvr_run.py`. The sha values
were checked to match their pins.

**Synthetic checks:** run in `/tmp` only.

**NGRAM scan:** `python3 -I .session_backup/2026-10-28/snapshots/C_pass3/checks/ngram_scan_cen.py` on this file
(result in the OPS line that registers it).

## 14. Hunk map v1 (05005d76) → v1.1 (CC-292)

| # | where in v1.1 | change | CC-292 item |
|---|---|---|---|
| H1 | title, Status | v1.1; round-2 diff read; v1 unchanged; pointer to §14 | ROUND 2 |
| H2 | header, blindness statement | v1.1 writing window; the S11 §10.3 A1-decomposition files and a1decomp LOG lines are named as not opened, with how the LOG was read | N7 |
| H3 | Tóm tắt cho PI | G2 > 1% clause; E1 homogeneity; K4 "filtering" | W1, W2, W3 |
| H4 | §2.1 "What the rebuild rests on" | A7 `emptied` holds by construction; the rebuild rests on c_pvr.py a503644a + CPython 3.12; `sys.version` recorded | N1 |
| H5 | §3 "One helper" | the helper also does the A7 rebuild; docstring cites T1-REP §2; selftest clauses | Ruling 12, N5 |
| H6 | §4.1 | homogeneity and linearity added to E1 | W3(a) |
| H7 | §4.3 G2, "Both fail", Order | G2 also NOT_IDENTIFIED at > 1% zero denominators; G1 checked before G2; the false "never a FAULT" sentence replaced by a true one and CC-292's case | W2, N2(b) |
| H8 | §4.4 FAULT line, Power | 1/B_eff means p₁ ≠ p₂; power against heterogeneity and non-linearity; a rejection does not say which | N8, W3(b) |
| H9 | §5.1 | PVR-drop fallback "set by this appendix (A7's tier-1 variant, PINS-A l.158-159)" | N4 |
| H10 | §5.2 Proposition | "sharp bounds (both ends attained)"; the identified set lies in [Δ_lo, Δ_hi] | N3 |
| H11 | §8 K1, K2 | the §3 unit wording; "(including a common copy rate across units)"; K2's second clause as CC-292 wrote it; "[unadjusted 95% CI]" | W3(c), W3(d), N6, N2(a) |
| H12 | §8 K4 | "filtering (PVR-drop)"; also used when G1 and G2 both fail | W1, N2(b) |
| H13 | §8 new rows | no main-text sentence for NOT_RUN / FAULT / POST_HOC; supplement line "not computed: <reason>" | N2(c) |
| H14 | §8 note, may-list K2, may-not item 2 | naming rule stated; "a common per-unit rate"; "an effect of the verifier" + naming rule | W1, W3(d), N2(a) |
| H15 | §9.1 items 3, 8, 10 | `str(x)` normalisation; A7 `emptied` is a consistency check only; item 8 unreachable (assert); new item 10 `sys.version` | N2(d), N1, W2 |
| H16 | §10 intro and code | G2 > 1% clause and gate record (G1 before G2); §5.5 FAULT kept as an assert; the W2 case and the G1 case added to the selftest | W2, N2(b) |
| H17 | §11 items 1, 4, 8; new 10, 11 | rebuild basis; G2 clause; fallback wording; P_all reading; homogeneity | N1, W2, N4, N3, W3 |
| H18 | §12 | round-2 questions replace the v1 table | ROUND 2 |
| H19 | §13 | CC-292 added to the reads | – |
| H20 | §14 | this table | ROUND 2 |

Everything outside H1-H20 is byte-equal to v1.
