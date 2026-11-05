# T1-REP: amendment to C-PVR-T1 (tier-1 reporting, arm protection, cap rule) — DRAFT v3, not approved

Status: DRAFT v3 for round 3/3 of CC-253 (the last round; CC-253r2 NEXT_ROUND 80) (full 3-judge panel plus a read-only Codex read). Tier: **IRREVERSIBLE, bar
85** (CC-253 TIER and N-11; PI-1103ad, LOG l.1439). It amends committed, test-spending prereg text and the registered
cap rule. v1's "REVERSIBLE, one judge" header is withdrawn.

It binds only after a GO and a gatekeeper commit, **before the first tier-1 output**. Speed-test outputs are never
read (NB-SPEED), but S14 follows the speed test with no gap, so the commit must come before the speed test.

Earlier versions are left untouched:
- v1 = `AMENDMENT_T1_REPORTING_DRAFT.md` (af3e847d): CC-253 NEXT_ROUND 74.
- v2 = `AMENDMENT_T1_REPORTING_DRAFT_v2.md` (9aae4184): CC-253r2 NEXT_ROUND 80.

§14 lists the changes v1 → v2 and §15 the changes v2 → v3, each with its source.

Written 2026-11-05 (UTC). Planning text only: nothing was run, rented, decoded or committed. AI opinion throughout.

Amends:
- `PREREG_DRAFT_v1_2.md` (0a2f0773…df2b, committed 8282874);
- `PINS_A_DRAFT_v1_4.md` (624b0804932731e3881cf058f6e680f96db476a0e1b852e615d920e417b8c99f, committed 3fb6725), §8 only.

Line numbers come from `git show <commit>:<path>`, which is byte-equal to the working copies.

Sources:
- `manuscript/directions/C_NEXT_STEPS_2026-11-04.md` (S3, §2, §5, §6);
- `C_TALLIP_2026-11-03_META_REVIEW.md` items 1, 2a, 2c, 3, 6, 7, 8, 9, 11, 15;
- CC-252;
- CC-253 (9c6f55cb);
- CC-254 Item 2, CC-254r2 (cc0c5292) and CC-254r3 (N116, N120);
- CC-253r2 (e4e350da): RB1-RB4, CX3, N1-N14;
- PI-1102a (l.1140), PI-1103g (l.1315), PI-1104af (l.1530), PI-1104ag (l.1534), PI-1104ah (l.1536), PI-1105a
  (l.1543), PI-1105c (l.1550).

The per-host money ledger has **one home**: the host amendment's §3. That home holds r_host, S, the block ledger and
T_down. The host file is `AMENDMENT_HOST_3090_DRAFT_v3.md` (e9c04955, commit 5d6f5ca), committed before this file (CC-254r2 Ruling 6). This file cites host §3 for S and T_down and does not restate or redefine them. It
replaces only the cap formula and the cut order.

## Tóm tắt cho PI (tiếng Việt)

- PI đã trả lời Q3, Q5, Q8 = CÓ (PI-1104ah). Vì vậy A4/A9 không bị cắt nữa (thứ tự cắt mới A10 → A5 → A3 → A2 → A11),
  và việc này ràng buộc không cần điều kiện.
- Luật trần trong §10.1 được thay nguyên khối:
  - bỏ min(⌈1,25·P1⌉, 37) và mặc định 20 GPU-giờ;
  - tiền tính theo từng máy của C (sổ ở amendment máy v3, commit 5d6f5ca);
  - giữ 1 giờ tiền máy cho bước kéo kết quả và xoá máy.
- Ví dụ ở P1 = 30: còn 31 giờ dưới 350 nghìn, nên **cắt khoảng 3–4 arm**. Trần 30 giờ, cả khối ≤ 338.793 đ. Các ngưỡng
  chỉ là minh hoạ, vì các arm có verifier tốn hơn.
- Hệ quả (a) về A7 trong v1 là sai, và đã được viết lại theo tỉ số odds (1−ρ)/(1−φ). Ở tầng 1, A7 chỉ đi theo
  PVR-drop. Vì vậy luật dùng chữ "verification" chỉ dùng cặp PVR-drop/A7 (ở tầng 2–3 là biến thể mà §6.3 chọn), và
  cần PVR > A7 có ý nghĩa trong họ Holm.
- Bản v3 còn sửa ba điểm khác:
  - dòng Q-cost của §14 được ghi là đã bị thay thế;
  - thêm dòng thay host l.95-97;
  - §5 của kế hoạch C_NEXT_STEPS được sửa theo dạng odds (CX3).
- Câu headline viết sẵn được sửa: nêu rõ P_obj^VI, có điều kiện theo luật go/primary, có câu cho trường hợp primary
  không đạt, và dùng "chưa được chứng minh là nâng".

## 1. Verifier-validity table (meta item 1; registered, non-gating, in-sample)

- **Where.** XM3600-vi, every arm that calls the verifier on demonstration propositions (PVR-drop, PVR-keep; A8's
  output-side labels are tabulated separately).
- **Unit.** One object proposition from a retrieved demonstration that maps, through `objects_in(…, raw_tone=False)`,
  to one of the 69 classes of `vi_oiv7_map.json` (27f2b1ca). Each class is counted once per demonstration caption, as
  in §3.1.
- **Gold.** The status of (query image, class) by the registered `status()` rule, against the existing OI human labels
  already pinned for XM3600: `oiv7_labels.json` bac3953a (prereg §2.1 l.202, §2.3). No new labels, no AI labels.
- **Table.** A 3 × 3 count table: verifier label {SUPPORTED, UNCERTAIN, REJECTED} × status {present, absent, unknown},
  plus parse failures (counted as UNCERTAIN, §6.3).
- **Reported:**
  - precision and recall of REJECTED for absent;
  - the SUPPORTED share on present;
  - Cohen's κ on the 2 × 2 of {REJECTED, SUPPORTED} × {absent, present} (UNCERTAIN and unknown excluded, with their
    counts beside it);
  - the yes-share, the UNCERTAIN share and the parse-failure share;
  - all of these with image-bootstrap CIs (§5.5 settings).
- **Limitation, stated.** Attribute, relation, count and scene-text propositions cannot be validated with existing
  gold.
- **PAPER wording rule (revised, CC-253 MB4; CC-253r2 RB1, N1).**
  - **Variant V.** V = PVR-drop at tier 1, because A7 follows PVR-drop there (PINS-A v1.4 l.158-159). At tiers 2-3, V
    is the variant §6.3 selects, fixed at the end of tier 1 before any tier-2 data, which A7 follows there.
  - The method is called "verification" only if both of these hold for V on the set being reported:
    - (i) **demonstration side:** the 95% CI of OR_V / OR_A7 (§2) lies wholly below 1, so V lowers the absent odds
      more than A7's count-matched random removal does;
    - (ii) **caption level:** V > A7 on P_obj^VI, Holm-significant.
  - Any OR_PVR-keep / OR_A7 at tier 1 is labelled **"not count-matched"** (PINS-A W5, l.160). It is descriptive only,
    is not a selectivity measure, and never enters rule (i).
  - A rule (i) claim on a set other than XM3600-vi needs that set's OR computation registered first, in the tier-2 or
    tier-3 prereg.

  Otherwise the method is called "filtering". Condition (ii) alone is not enough, because the caption-level contrast
  also runs through ICL copying (H-COPY) and through emptied demonstrations.
- This table also supplies the inputs ρ, φ and c of §2.

## 2. T2 result: an odds accounting identity for verifier error propagation (plan §5)

**What this is.** It is an exact accounting identity on counts, stated in odds form. It is not a statistical
guarantee and not a theorem about caption quality (CC-253 N-6). Its use is to make the verifier's effect on the
demonstrations measurable, and to tie that measurement to existing labels.

**Plain statement.** Filtering multiplies the odds that a demonstration object is wrong by (1 − ρ)/(1 − φ). It lowers
the share of wrong objects exactly when the verifier removes wrong objects at a higher rate than right ones.

**Setting.** Fix one arm and one query set (XM3600-vi). Pool over query images.
- Let N_A and N_P be the counts of retrieved-demonstration object propositions whose (query image, class) status is
  absent and present, before filtering. They are taken over all four demonstrations of every query image.
- Let c = N_A / (N_A + N_P), the absent share.
- A proposition counts as *removed* iff its mapped mention is no longer in the demonstration after span deletion,
  sentence drop and the dropping of emptied demonstrations (§6.4). So collateral removals are included.
  - Under PVR-drop, the verifier's removal set is REJECTED ∪ UNCERTAIN.
  - Under PVR-keep, it is REJECTED only.
- Let ρ = (removed absent) / N_A and φ = (removed present) / N_P, the empirical removal rates.

**Identity.** Assume 0 < c < 1, ρ < 1 and φ < 1. Then

odds(c′) = odds(c) · OR, where OR = (1 − ρ)/(1 − φ) and odds(x) = x / (1 − x).

Equivalently, c′ = c(1 − ρ) / (c(1 − ρ) + (1 − c)(1 − φ)). Hence c′ < c iff OR < 1 iff ρ > φ.

**Proof sketch.** After filtering, N_A(1 − ρ) absent and N_P(1 − φ) present propositions remain, by definition. Their
ratio is odds(c′) = [N_A / N_P] · [(1 − ρ)/(1 − φ)] = odds(c) · OR. Since odds is strictly increasing on (0, 1), c′ < c
iff OR < 1, and OR < 1 iff ρ > φ. No sampling model is used.

**The A7 reference (replaces v1 corollary (a), CC-253 MB4).**
- A7 removes, **within each demonstration**, a uniformly random subset of propositions, of the same size as the
  matched variant's removal in that demonstration. It also matches that variant's emptied-demonstration count (PINS-A
  v1.4 l.150, l.156).
- **The matched variant.** At tier 1, A7 follows **PVR-drop only** (PINS-A l.158-159). At tiers 2-3 it follows the
  variant §6.3 selects. So the count-matched pair is (PVR-drop, A7) at tier 1.
- **Within one demonstration** the A7 draw is status-blind, so its expected removal rates on absent and present
  propositions there are equal.
- **Pooled, they need not be.** A7 removes more where PVR removes more. If PVR's removal count tracks a demonstration's
  absent share, pooled ρ_A7 > φ_A7 is possible.
- So OR_A7 is not 1 by design. Pooled ρ_A7, φ_A7, OR_A7 and c′_A7 are reported **as measured**: a status-blind
  reference with PVR's per-demonstration removal counts, not a null.
- **Selectivity beyond count-matched random removal** is the demonstration-side ratio
  odds(c′_V) / odds(c′_A7) = OR_V / OR_A7, for the matched variant V only. It is exact, because both arms start from the
  same c, and it is reported with an image-bootstrap CI.
- OR_PVR-keep / OR_A7 at tier 1 is **"not count-matched"** (PINS-A W5, l.160). It is reported as a descriptive only and
  is not a selectivity measure.
- **Analytic pool-level null.** A random drop of the same total count, uniform over the pooled propositions, has
  E[ρ] = E[φ] and so E[OR] ≈ 1. It is computed on counts (no decode) and printed beside the measured A7 values.
- The **caption-level** PVR − A7 contrast is not a test of selectivity. It also passes through H-COPY and through
  emptied demonstrations.

**Recall side.** The share of present propositions kept is 1 − φ. The demonstrations then offer at most N_P(1 − φ)
correct object propositions to copy. This bounds the demonstration-side support for R_obj^VI.

**Assumptions, named.**
1. **Unknown-status pairs are excluded.** c, ρ and φ use known-status propositions only. The identity holds on the
   known part and says nothing about the unknown part. The unknown share is reported beside it.
2. **The mapping is taken as given.** A mismapped mention (for example the 'cây' case of §5) enters at its mapped class.
   The §5 sensitivity rule reports c, ρ, φ and OR under both scorers.
3. **Pooling.** The identity holds for pooled counts. The per-image distribution of ρ and φ is descriptive.

**What it does not claim.** It does not say that a lower c′ gives more precise captions. That link runs through ICL
copying and is a **hypothesis** (H-COPY). H-COPY is tested only by the registered PVR − A8 and PVR − A1 contrasts and
reported as such.

**Checks on existing labels only (registered, in-sample, non-gating).** On XM3600-vi, for PVR-drop, PVR-keep and A7,
report:
- c, ρ, φ, OR and c′, each with an image-bootstrap CI;
- OR_PVR-drop / OR_A7 with its CI (the selectivity measure), and OR_PVR-keep / OR_A7 with its CI labelled "not
  count-matched";
- the analytic pool-level null;
- the unknown share.

c′ computed from (c, ρ, φ) must equal the c′ counted directly; a mismatch is a scorer FAULT, not a finding. The inputs
are the §1 table and the OI labels already pinned. No new labels, no AI labels as evidence, no extra GPU.

**Plan revised (CC-253r2 CX3; CC-253 MB4).** `manuscript/directions/C_NEXT_STEPS_2026-11-04.md` §5 has been revised to
this odds-form account by a dated note (OPS-1105c-amend-v3 LOG line; old sha 2e2384a9, pre-edit copy in
`.session_backup/2026-11-04/c_amend/`). The plan no longer says "A count-matched random drop (A7) has ρ = φ, so its
c′ = c" or "The PVR − A7 contrast isolates the ρ − φ term". It is a plan file and registers nothing.

## 3. A4 and A9 protected (meta item 2a; PI-1104ah Q8 = YES, binding)

- Move A4 (NES-style CLIP filter) and A9 (ITM/ARA re-ranking) to the never-cut list.
- New cut order: A10 → A5 → A3 → A2 → A11.
- Name PVR − A4 and PVR − A9 on P_obj^VI as key secondaries, reported beside the primary contrast. The Holm family is
  unchanged.
- The PI line exists: PI-1104ah, LOG l.1536, Q8 = YES. That meets PINS-A (3fb6725) l.686-687, which sends changes
  outside the §5.1 cost rule to the PI. R-1 and R-2 therefore bind unconditionally on registration.
- **Consequence.** The PINS-A cut-first addendum (plan S9) must pin A4 and A9 before the speed test.
- **PINS-A l.685-686 (CC-253r2 N5).** These lines still list "The cut-first arm helpers (A4 CLIP filter, A5 LMCap, A9
  ITM, A10 prompt)". After R-1, A4 and A9 are never-cut arms. Row R-9 amends the text; the addendum route (one-judge
  read before the speed test) is unchanged.

## 4. A0, the mechanism check and pre-written headlines (meta item 3; CC-253 MB5)

**Tier 1, registered, in-sample.**
- A1 − A0 on XM3600-vi (P_obj^VI, R_obj^VI and CIDEr-VI) is the ICL-mechanism check. It is reported next to the
  headroom check (A12 − A1).
- Also reported:
  - PVR − A0;
  - the distribution of SigLIP retrieval similarity per set;
  - the share of rejected demonstration propositions by type;
  - the share of emptied demonstrations.
- None gates.

**The A8 key ("the rule"), per tier (CC-253r2 N2).**
- Tier 1: the §12 (iv) go rule, point ΔP_obj^VI(PVR − A8) ≥ SESOI_P on XM3600-vi. Tier 1 has no PASS, and every
  tier-1 sentence is labelled "dev, in-sample (XM3600-vi)".
- Tiers 2-3: condition 1 of §5.3 / §5.4, i.e. the CI lower bound of ΔP_obj^VI(PVR − A8) > 0 and the point estimate
  ≥ SESOI_P. The full PASS headline is separate: §5.3 / §5.4.

**Three PVR − A0 cases on P_obj^VI:**
- **L**, lowered: the CI upper bound < 0;
- **N**, not shown: the CI covers 0;
- **R**, raised: the CI lower bound > 0.

**Headline wording, written now.**
- The tier-1 dev report uses it, labelled dev.
- It binds the paper only through the tier-3 prereg, which takes it over at the IRREVERSIBLE tier.
- Each sentence is chosen mechanically from the conditions below. x and [CI] are filled from the registered output.

| case | condition | sentence |
|---|---|---|
| HW-2 "retrieval hurts" | A1 − A0 on P_obj^VI has CI upper bound < 0 | "With this datastore (KTVIC and OpenViIC training captions), unverified retrieved demonstrations lowered object precision (P_obj^VI) below zero-shot captioning (A1 − A0 = x [CI])." Stated in the main results and the abstract-level summary, never omitted |
| HW-1a | case N **and** the rule holds | "Verifying retrieved demonstrations before use raised object precision (P_obj^VI) above post-hoc correction with the same verifier (PVR − A8 = x [CI]), but was not shown to raise P_obj^VI above zero-shot captioning (PVR − A0 = x [CI])." |
| HW-1b | case N **and** the rule fails | "Verifying retrieved demonstrations before use was not shown to raise object precision (P_obj^VI) above post-hoc correction with the same verifier (PVR − A8 = x [CI]) or above zero-shot captioning (PVR − A0 = x [CI])." |
| HW-La | case L **and** the rule holds | "Verifying retrieved demonstrations before use raised object precision (P_obj^VI) above post-hoc correction with the same verifier (PVR − A8 = x [CI]), but lowered it below zero-shot captioning (PVR − A0 = x [CI])." |
| HW-Lb | case L **and** the rule fails | "Verifying retrieved demonstrations before use was not shown to raise object precision (P_obj^VI) above post-hoc correction with the same verifier (PVR − A8 = x [CI]), and lowered it below zero-shot captioning (PVR − A0 = x [CI])." |
| HW-1 harm clause | appended to HW-1a, HW-1b, HW-La or HW-Lb **only if HW-2 holds** | "With this datastore, unverified retrieval lowered P_obj^VI below zero-shot captioning, and verification [reduced / was not shown to reduce] that loss (PVR − A1 = x [CI])." "reduced" iff the CI lower bound of PVR − A1 on P_obj^VI is > 0 |
| HW-3 | case R **and** the rule holds | "Verifying retrieved demonstrations before use raised object precision (P_obj^VI) above both post-hoc correction with the same verifier (PVR − A8 = x [CI]) and zero-shot captioning (PVR − A0 = x [CI])", with the datastore named in the claim sentence. At tier 1 it is labelled "dev go (§12 iv)", never "PASS" |
| HW-0 | case R **and** the rule fails | "Verifying retrieved demonstrations before use raised object precision (P_obj^VI) above zero-shot captioning (PVR − A0 = x [CI]) but was not shown to raise it above post-hoc correction with the same verifier (PVR − A8 = x [CI])." |

- Exactly one of HW-0, HW-1a, HW-1b, HW-La, HW-Lb and HW-3 applies. HW-2 is added whenever its condition holds.
- No sentence uses overlap or duplication wording (PI-1101o).

## 5. 'cây' sensitivity rule (meta item 6; PI-1104ah Q5 = YES, sensitivity only)

- **Scorer of record.** It stays `rescap/chair.py` (e47d249a…), unedited.
- **Classifier set.** K = the nouns n with `NOUN_CLASSIFIER[n] == "cây"` and n ≠ "cây" in `rescap/vi/lexicon.py`
  (fbc945f2…). At that sha K = {dù, bút, chổi, cầu} (4 nouns). K is recomputed from the pinned file by code, never
  typed.
- **Rule (deterministic; hardened per CC-253 N-7).**
  1. Work on the caption's raw NFC, lower-cased string.
  2. At each occurrence of the word "cây", check that it is followed by exactly one space and then a word, with no
     punctuation between. For example, "cây, dù …" is not adjacent.
  3. Find the longest match of that word sequence over **all** NOUN_CLASSIFIER keys, ending at a word boundary.
  4. The occurrence is ignored only if that longest match is in K. Example: if a longer key such as a two-word
     compound starting with "cầu" exists and matches, the match is not in K and nothing is ignored.
  5. The 'cây' mention is kept if any other occurrence remains. The class is counted at most once per caption.
- **Disclosed limits.**
  - K covers only nouns listed in NOUN_CLASSIFIER with classifier "cây". Classifier uses with unlisted nouns are not
    caught.
  - A compound that starts with a K noun but is not a NOUN_CLASSIFIER key at fbc945f2 is matched as the K noun alone.
    "cầu thủ" is one such compound (it has 0 keys in the file). So a 'cây' directly before it is ignored wrongly. The
    rule does not match over a wider lexicon; this limit is disclosed beside the sensitivity result (CC-253r2 N6).
- **Report.**
  - ΔP_obj^VI(PVR − A8) under both scorers, at every tier.
  - At tier 1: the c, ρ, φ and OR of §2 under both scorers.
  - "Mentions ignored by the sensitivity rule", per arm. This is a scorer-side count, **not a data removal**. It stays
    in the supplement and out of the paper body (CC-253 CX2; PI-1101o read as covering data removals).
- **Code.** A new scorer file under `scripts/c_pvr/` (plan S10), with a selftest on synthetic short phrases, including a
  non-adjacent case and a longer-key case. `rescap/chair.py` is not edited.
- **Paper A.** A notice to A's owner that A uses the same matcher (CC-253 N-10) is a coordinator step. It is recorded
  by its own LOG line before this file's commit, and has not been recorded yet (CC-253r2 N14). Any rescoring of A is
  labelled post hoc.

## 6. Tier-1 descriptives (meta items 7, 8, 9, 15; every one non-gating)

**Item 7.**
- Per arm and set: mapped mentions split into present, absent and unknown.
- The verifiable-mention share, with an image-bootstrap CI. The §5.7(a) 5-point flag stays.
- Mapped mentions per caption.

**Item 8.**
- ΔR_obj^VI(PVR − A8) with a CI.
- A8's recall loss against A1, and A8's empty-caption share.
- ΔCHAIR_s^VI.
- Per image and arm: mean verifier calls, cap hits and wall-clock.
- PVR-keep − A8 on P_obj^VI as a registered sensitivity analysis.
- The base P_obj^VI and R_obj^VI of A0 and A1, next to δ_R and SESOI_P.
- **Mention-count strata**: images split by the number of mapped mentions in A1's caption, {0, 1, 2, ≥ 3}, with
  ΔP_obj^VI(PVR − A8) per stratum.
- **Per-arm speed projection:** the P1 LOG line lists the projected hours of every arm, before any cut (R2 m7).

**Item 9 (per arm and set).** All deterministic and non-AI:
- the Vietnamese-letter token share: tokens after NFC, lower-casing and punctuation strip, made only of letters of the
  Vietnamese alphabet with its diacritics, excluding f, j, w and z; the regex is pinned in the S10 scorer;
- the empty share;
- the share of captions with a repeated 3-gram;
- mean length in syllables;
- distinct-1 and distinct-2;
- the truncation share;
- the segmenter failure rate.

The §5.7(b) VI-script guard is unchanged. A syllable-share PASS condition is a tier-3 prereg item.

**Item 15 (XM3600-vi; dev).**
- REJECTED and UNCERTAIN rates, and ΔP_obj^VI, by proposition type.
- The same by Vietnamese feature:
  - classifier + noun phrases (con, cái, chiếc, cây);
  - compounds the rule-based segmenter splits;
  - nouns written with variant tone-mark placement. `norm_tone` (chair.py l.64-76) normalises placement only and merges
    no tones; v1's "tone-ambiguous nouns merged" is withdrawn (CC-253 N-7).
- A short error analysis of demonstrations rewritten after span deletion. Examples in repo files are id-only or
  synthetic, never dataset caption text.

## 7. Coverage and base rates (meta item 11, tier-1 part)

- **Base rates.**
  - The tier-1 report gives the XM3600 base rate from the committed manifest: present share among verified pairs =
    4,453 / (4,453 + 8,276) = 35.0% (prereg §3.3 l.311).
  - The tier-2 report adds the NoCaps-val figure.
  - The NoCaps-test figure (39,975 / 74,502 = 53.7%) is cited from the committed G-B aggregates only, with no new read.
- **In-sample label.** SESOI_P stays labelled in-sample (NB-INSAMPLE, §12).
- **Out-of-sample check.** The tier-2 NoCaps-val rehearsal is the only out-of-sample check before the test. NoCaps val
  was already looked at in the CC-212 study, with other models and another method.
- **Stale forecast.** The 58.9% XM3600 coverage forecast (C_DIRECTION_v4_1 l.163) is never given as the protocol's
  reason. No study-brief or paper text quotes v4.1 l.163, l.256 or l.459.

## 8. Prior art: MeaCap (meta item 2c; CC-253 N-8)

Add to prereg §1.3:

"MeaCap (Zeng et al., CVPR 2024; arXiv 2403.03715) retrieves memory captions, extracts key concepts from them and filters
those concepts against the image before generation, for zero-shot captioning. It filters memory **concepts**, not
in-context **demonstrations**. Of the pre-generation filters it is the closest to C's position. A6 and A4 bracket it in
the arm plan."

CC-253 N-8 ordered the source check. The CC-253r2 round-2 judges verified arXiv 2403.03715 against the source
(CC-253r2 N10).

The full re-sweep (CLAIM, TOMM 2026, NAICL, Re3Cap, the SSRN preprint, HSTFG, the Adjudicated Captioning DOI) stays a
tier-2 and tier-3 prereg item. Each entry is verified against its source before citing. No "first" claim.

## 9. Cap rule, replaced as one block (CC-253 MB1, MB2, MB3)

**Symbols.**
- r_host: VND per GPU-h, recorded in the rental LOG line (`AMENDMENT_HOST_3090_DRAFT_v3.md` (e9c04955, commit 5d6f5ca) §2).
- S: C's per-host spend for the block up to the P1 line, including setup, selftest, speed test and idle time.
  - Defined only in **host amendment §3**: the per-instance "spent" of each HC-n instance, as in the LOG l.1164
    precedent.
  - Never a balance difference (CC-253 MB2; PI-1104ag).
- T_down: the teardown reserve, defined and pinned only in **`AMENDMENT_HOST_3090_DRAFT_v3.md` (e9c04955, commit 5d6f5ca) §3**. It pays for the final output pull,
  the last backup, the logged deletion and the machine delete. This file cites the value and does not set it.
- P1: the projected tier-1 decode GPU-h from the speed test, as the sum of the per-arm hours.
- **H_M = ⌊(M − S − T_down) / r_host⌋** for a money ceiling M.

**Rule (mechanical, applied at the P1 line; no judge round).**
1. If ⌈1.25 × P1⌉ ≤ H_350k: cap = ⌈1.25 × P1⌉ GPU-h. No cut.
2. Otherwise, cut arms one at a time in the §5.1 order (A10 → A5 → A3 → A2 → A11) until ⌈1.25 × P1′⌉ ≤ H_350k. Then
   cap = ⌈1.25 × P1′⌉.
3. If every cuttable arm is cut and it still does not fit, apply PQ-C2 = YES (PI-1104af). M = 465,000 VND, subject to
   the `AMENDMENT_HOST_3090_DRAFT_v3.md` (e9c04955, commit 5d6f5ca) §3 solvency rule (CC-253r2 N4). If ⌈1.25 × P1′⌉ ≤ H_465k, then cap = ⌈1.25 × P1′⌉, and the
   cuts of step 2 are kept.
4. If it still does not fit, the PI decides before any decode. No set is shrunk. The machine is deleted if the wait
   exceeds setup time.

**Money stop.**
- Decoding stops when the block's per-host spend reaches M − T_down. T_down is used only for teardown.
- The money ledger binds over every hour figure.
- Projection before every block; a cap stop is final; one resume only for machine loss.

**Worked example [illustrative].**
- Assumptions: r_host = 9,282 VND/h (LOG l.923); S = 5.5 h × r = 51,051 VND (setup and selftest about 4 h, speed test
  ≤ 1.5 h); T_down = 9,282 VND.
- This gives H_350k = ⌊(350,000 − 51,051 − 9,282) / 9,282⌋ = ⌊31.2⌋ = **31** and H_465k = ⌊43.6⌋ = **43**.
- At P1 = 30 GPU-h (plan estimate, 20 × 1.5): ⌈1.25 × 30⌉ = 38 > 31, so cuts are certain.
  - With v = 0.8 and equal per-arm cost, each VI arm is 30 × 0.8 / 15 = 1.6 h. Four arms are cut (A10, A5, A3, A2):
    P1′ = 23.6, cap = ⌈29.5⌉ = 30.
  - With v = 1.0, each arm is 2.0 h. Three are cut: P1′ = 24.0, cap = 30.
  - Block money ≤ S + cap × r + T_down = 51,051 + 30 × 9,282 + 9,282 = **338,793 VND** ≤ 350,000. v1's 348,075 omitted
    the teardown reserve and is withdrawn.
- At a 3090/4090 factor of 1.2: P1 ≈ 24, ⌈30⌉ = 30 ≤ 31, so no cut.

**Thresholds [illustrative only, CC-253 N-4].**
- These assume equal per-arm cost. The verifier arms (PVR-drop, PVR-keep, A8, A10) cost more, so the real thresholds
  differ.
- The binding rule above sums the measured per-arm hours.
- v = the VI share of P1. All five cuts remove v/3 of P1.

| event | condition | v = 0.7 | v = 0.8 | v = 0.9 | v = 1.0 |
|---|---|---|---|---|---|
| cuts start | P1 > 31 / 1.25 | 24.8 | 24.8 | 24.8 | 24.8 |
| PQ-C2 branch (all 5 cut, still > H_350k) | P1 > 24.8 / (1 − v/3) | 32.3 | 33.8 | 35.4 | 37.2 |
| PI decides (all 5 cut, still > H_465k) | P1 > 34.4 / (1 − v/3) | 44.9 | 46.9 | 49.1 | 51.6 |

**Overrules, stated (CC-253 Ruling 10).**
- **CC-220r2 N-B2, its closure in CC-220r3, and the prereg §14 Q-cost row l.809** (R-8) (l.47: "Cap = min(ceil(1.25 x P1), 37) GPU-h iff Q-cost YES, else 20
  GPU-h hard"). Superseded on three counts:
  - PI-1102a (l.1140) answered Q-cost = YES, so the 20 GPU-h default branch is spent;
  - PI-1103g (l.1315) made the cap money, ≤ 350k VND, not hours;
  - PI-1104af (l.1530) added PQ-C2, ≤ 465k VND after every cut.
- **CC-236 Ruling 5, row A13 only, and W7** (`cap_GPUh = min(⌈1.25 × P1⌉, ⌊350,000 / r_host⌋)`, PINS-A §8 l.540-543),
  and W7's "read from balance lines". Superseded by the per-host ledger (`AMENDMENT_HOST_3090_DRAFT_v3.md` (e9c04955, commit 5d6f5ca) §3; CC-254 N91) and by T_down. The rest of
  CC-236 Ruling 5, the two-stage pin rule, stays in force (CC-253r2 N3).
- PI-1103g's money cap itself is kept and applied.

**Errata to the plan** (`C_NEXT_STEPS_2026-11-04.md`, untracked; 2e2384a9 → 639192a4, §5 revised by the dated note of §2):
- **E1.** §1 "Budget risk" omits the 1.25 factor and the teardown reserve. Cuts are certain at P1 = 30. The PQ-C2
  branch opens near P1 ≈ 32–37 [illustrative], not about 40.
- **E2.** S6 lists O_B "allowed by NB-OVQALOST". O_B is **not licensed until the tier-2 prereg** (prereg §4.3
  l.363-367; CC-254 Ruling 1.4). Nothing in this file depends on O_B.
- **E3.** §5 rested on the withdrawn A7 corollary; it is now revised to the odds-form account (§2; plan sha 639192a4).

## 10. Registered lines changed (old → new)

| # | where | old (quoted) | new |
|---|---|---|---|
| R-1 | prereg §5.1 l.386-387 (8282874) | "Cut order if the projection exceeds the cap: A10 -> A5 -> A9 -> A3 -> A2 -> A4 -> A11; never cut PVR-drop, PVR-keep, A8, A1, A0, A6, A7, A12 (v4.1 l.458)." | "Cut order if the projection exceeds the cap: A10 -> A5 -> A3 -> A2 -> A11; never cut PVR-drop, PVR-keep, A8, A1, A0, A4, A6, A7, A9, A12 (v4.1 l.458; T1-REP §3; PI-1104ah Q8 = YES)." |
| R-2 | prereg §5.2 l.390 | "**One primary contrast:** PVR − A8 on P_obj^VI (primary unknown rule), paired by image." | unchanged; add after it: "Key secondaries, reported beside the primary: PVR − A4 and PVR − A9 on P_obj^VI (Holm family unchanged; PI-1104ah Q8)." |
| R-3 | prereg §10.1 l.722-729, **one block** | "- **Cap (CC-220r2 N-B2; the rule is pinned in PINS-A before the speed test and any output).** P1 = projected tier-1 GPU-h on M1 from the speed-test throughput only (never from any output). / - **If the PI answers Q-cost = YES:** cap = min(⌈1.25 × P1⌉, 37) GPU-h (one re-base for M1, NB-CAP; 37 = the money ceiling <= 350k VND at 9,282 VND/h, LOG l.1109; MT4 AMENDMENT_COST precedent as cited in CC-220 l.58). / - **Otherwise (the default):** cap = **20 GPU-h hard** (v4.1 l.457; about 186k VND on M1). / - In both cases, if ⌈1.25 × P1⌉ exceeds the cap, arms are cut in the order of §5.1 until it fits; if it still does not fit, the PI decides before any decode (no set is shrunk). Projection before every block; a cap stop is final; one resume only for machine loss." | "- **Cap (money; PI-1103g, PQ-C2 PI-1104af; T1-REP §9; supersedes CC-220r2/r3 N-B2 and CC-236 Ruling 5).** P1 = projected tier-1 GPU-h on the named host (host amendment) from the speed-test throughput only (never from any output), as the sum of per-arm hours. / - S = C's per-host spend up to the P1 line and T_down, both as defined in the host amendment (AMENDMENT_HOST_3090_DRAFT_v3.md, commit 5d6f5ca) §3; H_M = ⌊(M − S − T_down) / r_host⌋; M = 350,000 VND. / - If ⌈1.25 × P1⌉ ≤ H_M, cap = ⌈1.25 × P1⌉ GPU-h; otherwise arms are cut in the order of §5.1 until ⌈1.25 × P1′⌉ ≤ H_M and cap = ⌈1.25 × P1′⌉; if every cuttable arm is cut and it still does not fit, M = 465,000 VND (PQ-C2), cuts kept, subject to the host amendment's §3 solvency rule; if it still does not fit, the PI decides before any decode (no set is shrunk). / - Decoding stops when the per-host spend reaches M − T_down; the money ledger binds over every hour figure. Projection before every block; a cap stop is final; one resume only for machine loss." |
| R-3b | prereg §10.2 l.735-736 | "- **Tier 1 on M1** (9,282 VND/h, LOG l.1109): default 20 GPU-h hard ≈ 186k VND; only with Q-cost = YES, the re-based ceiling <= 37 GPU-h ≈ <= 350k VND (§10.1) [est.; arithmetic 20 × 9,282 = 185,640; 350,000 / 9,282 = 37.7]." | "- **Tier 1 on the named host** (r_host at rental; 9,282 VND/h [est.], LOG l.923): money ≤ 350,000 VND per host ledger, setup, speed test, idle time and the 1 h teardown reserve included; ≤ 465,000 VND only under PQ-C2 after every §5.1 cut (§10.1) [illustrative: P1 = 30 → cap 30 GPU-h, block ≤ 338,793 VND]." |
| R-4 | PINS-A §8 l.540-543 (3fb6725) | "`cap_GPUh = min(⌈1.25 × P1⌉, ⌊350,000 / r_host⌋)`, … If the projection does not fit, arms are cut in the §5.1 order (A10 → A5 → A9 → A3 → A2 → A4 → A11); if it still does not fit, the PI decides." | "The cap rule is prereg §10.1 as amended by T1-REP R-3 (one text; not restated here); S and T_down per host amendment §3." Lines l.544-546, which say what counts and how it is read, are amended by the host amendment (its row H-21), which registers first; this file does not touch them. |
| R-5 | prereg §1.3, after l.184 | – | the MeaCap paragraph of §8 |
| R-6 | prereg §3.2 l.302-303 | "Always reported per set and arm: verified present / absent pair counts …; verifiable-mention share … beside P_obj^VI." | unchanged; add: "plus the unknown count, mentions per caption and the verifiable-mention share with an image-bootstrap CI (T1-REP §6)." |
| R-7 | prereg §12 l.765-768 | "**Decides (in order):** (i) SESOI_P … (iv) go to tier 2 iff …" | unchanged; add a new bullet: "**Reports (registered, non-gating, in-sample):** the T1-REP §1 verifier table, the §2 identity checks, the §4 A0 contrasts and headline case, the §5 'cây' sensitivity, the §6 descriptives and the §7 base rates." |
| R-8 | prereg §14 | – | two answered rows: "PQ-C2 — YES (PI-1104af, LOG l.1530)" and "meta Q3, Q5, Q8 — YES (PI-1104ah, LOG l.1536)". |
| R-8b | prereg §14 Q-cost row l.809 | "| Q-cost | Accept a C tier-1 cap re-based on M1 to min(⌈1.25 × P1⌉, 37) GPU-h (<= 350k VND) and a C total ≈155-195 4090-GPU-h (≈2.7-3.4M VND) [est.] after A and B? This answer sets the registered cap directly (§10.1, CC-220r2 N-B2) \| YES \| 20 GPU-h hard cap (≈186k VND), arms cut in the §5.1 order; if it still does not fit, you decide before any decode; no C spend before Q11 |" | "| Q-cost | answered YES (PI-1102a, LOG l.1140); its cap form min(⌈1.25 × P1⌉, 37) and the 20 GPU-h default are superseded by PI-1103g, PI-1104af and T1-REP R-3 / R-3b; the registered cap is prereg §10.1 as amended by R-3 \| – \| – |" (CC-253r2 RB3) |
| R-9 | PINS-A l.685-686 (3fb6725) | "The cut-first arm helpers (A4 CLIP filter, A5 LMCap, A9 ITM, A10 prompt) are arm pins: a PINS-A addendum (one-judge read) before the speed test" | "The arm helpers A4 CLIP filter and A9 ITM (never-cut, T1-REP R-1) and the cut-first helpers A5 LMCap and A10 prompt are arm pins: a PINS-A addendum (one-judge read) before the speed test" (CC-253r2 N5) |
| R-10 | host amendment AMENDMENT_HOST_3090_DRAFT_v3.md (e9c04955, commit 5d6f5ca) §2 l.95-97 | "- **Once T1-REP is registered** (`AMENDMENT_T1_REPORTING_DRAFT.md`, af3e847d, under the CC-253 panel read; PI-1104ah Q8 = YES), its §9 / R-3 / R-4 form replaces the formula and cut order above. That form uses the money left, ⌊(M − S) / r_host⌋, and the cut order A10 → A5 → A3 → A2 → A11." | "- **Once T1-REP is registered**: T1-REP (registered at <commit>) §9: H_M = ⌊(M − S − T_down)/r_host⌋, cut order A10 → A5 → A3 → A2 → A11." The token <commit> is resolved by T1-REP's gatekeeper LOG line, because a byte-equal registered file cannot hold its own commit id (CC-253r2 RB2; CC-254r3 N116, N120) |

**Overlap with the host amendment, stated.** The host file registers first (CC-254r2 Ruling 6).
- Its H-10 rewrites prereg l.722-723 ("on M1" → "on HC-n"). Its H-12 rewrites l.735-736.
- Its H-18 rewrites PINS-A §8 l.541-542 (where r_host is named). R-4 replaces l.540-543 as a pointer to R-3. The
  pointer keeps r_host as defined by H-18 and host §2, so H-18's text is not contradicted (CC-253r2 RB4; CC-254r3
  N120).
- R-10 supersedes host l.95-97, which still names T1-REP v1 and ⌊(M − S)/r_host⌋.
- On this file's registration, R-3 replaces l.722-729 as one block, R-3b replaces l.735-736, and R-4 replaces PINS-A
  l.540-543. They supersede the host's interim text for those lines.
- Both keep "on the named host (host amendment)" and the host amendment's §3 definitions, so nothing in the host file
  is contradicted.

## 11. Change table (against the registered prereg and PINS-A)

| id | item | type | binds when |
|---|---|---|---|
| §1 | meta 1 | new registered report; revised wording rule | GO + commit, before the first tier-1 output |
| §2 | plan §5 (T2) | registered odds identity + checks | same |
| §3, R-1, R-2 | meta 2a | registered §5.1/§5.2 lines | same (PI-1104ah Q8 = YES) |
| §4 | meta 3 | new report + headline forms | tier 1 now; tier-3 binding via the tier-3 prereg |
| §5 | meta 6 | new sensitivity rule | same as §1; scorer code is plan S10 |
| §6, R-6, R-7 | meta 7, 8, 9, 15 | new descriptives | same as §1 |
| §7 | meta 11 (tier-1 part) | report rule | same as §1 |
| §8, R-5 | meta 2c | prior art | same as §1 |
| §9, R-3, R-3b, R-4, R-8, R-8b, R-10 | cap rule, PQ-C2, Q-cost | registered cap block (prereg §10.1, §10.2, §14; PINS-A §8; host l.95-97) | same as §1 |
| R-9 | A4/A9 helper text | PINS-A l.685-686 | same as §1 |

## 12. Rulings needed

| # | from | question | recommended | default if no answer |
|---|---|---|---|---|
| J-1 | panel + Codex | Are CC-253r2 RB1–RB4 and CX3, and N1–N12 and N14, closed (and CC-253 MB1–MB5, CX2)? | YES | – |
| J-2 | panel | Is the §2 identity and the A7 reference stated correctly (odds form; A7 matched per demonstration to PVR-drop at tier 1; OR_PVR-drop / OR_A7 as the only selectivity measure; PVR-keep labelled "not count-matched")? | YES | – |
| J-3 | panel | Accept the R-3 / R-3b / R-4 block (money cap, per-host ledger cited, T_down = 1.0 h × r_host, PQ-C2 after the cuts, overrules stated)? | YES | registered §10.1 / PINS-A §8 text (conflicting cap texts stay) |
| J-4 | panel | Is citing host §3 for S and T_down (1.0 h × r_host, pinned there) consistent with CC-253 MB2/MB3 and CC-254r2 N98/N103? | YES | – |
| PI 2 (CC-253) | PI | Shared ckey balance with B's PI-1104ag blocks | **answered:** PI-1105a (LOG l.1543): rent sequentially, C first, then B, one 3090 at a time, no top-up. PI-1105c (l.1550): if C's spend leaves too little for B's 28 h cap, B runs at its registered 22 h cap. Path record: under PQ-C2 (≤ 465k) about 333k remains, which covers B's 22 h block; C's L-before re-reads the balance (CC-253r2 N9, N12) | – |
| PI 1 (CC-253r2) | PI | Split commit: may T1-GUARD commit alone on its own round-3 GO? | YES (CC-253r2 Ruling 9) | one joint commit after round 3 |
| PI 3 (CC-253r2) | PI | Q-cost superseded (RB3, FYI) | confirm superseded | superseded, as R-8b states |

## 13. Drafting-touch disclosure

Read:
- the committed prereg and PINS-A text;
- `rescap/vi/lexicon.py`, the `NOUN_CLASSIFIER` entries equal to "cây" (grep);
- the `rescap/chair.py` function names (grep);
- LOG lines PI-1102a, PI-1103ad/ae, PI-1103g, PI-1104ae/af/ag/ah, l.923, l.1164, l.1375;
- CC-220.txt l.59, CC-220r2, CC-220r3, CC-236 l.134-222, CC-253, CC-254, and the CC-253 workflow journal;
- `c_pvr_lists.json` counts.

Not opened: any label file (`oiv7_labels.json` was not opened or hashed; its sha is cited from the prereg), any caption
text, any NoCaps, TextCaps or OI test file, `~/.vsps_sealed`.

## 14. Change table against v1 (af3e847d)

| # | v1 place | v2 change | source |
|---|---|---|---|
| V-1 | §9 rule; R-3 (l.727-729 only); R-4 | §10.1 l.722-729 quoted and replaced as one block. min(⌈1.25P1⌉, 37) and the 20 GPU-h default are removed; "Projection before every block; a cap stop is final; one resume only for machine loss" is kept verbatim. New R-3b replaces §10.2 l.735-736. R-4 points to R-3 and drops the balance-line reading. CC-220r2/r3 N-B2 and CC-236 Ruling 5 / W7 are overruled with PI-1102a, PI-1103g and PI-1104af | CC-253 MB1, Ruling 10 |
| V-2 | §9 "S = balance before − balance at P1" | S is the per-host spend. Its single home is host §3 (v3), cited and not restated. Balance lines are solvency checks only | CC-253 MB2; CC-254 N91; CC-254r2 N98(b), N103 |
| V-3 | §9 H_M = ⌊(M − S)/r⌋; example 32 / 44 h and 348,075 VND | H_M = ⌊(M − S − T_down)/r_host⌋, with T_down = 1.0 h × r_host cited from host §3; money stop at M − T_down. Recomputed: H 31 / 43; at P1 = 30, 3–4 arms cut, cap 30, block ≤ 338,793 VND | CC-253 MB3; CC-254r2 N103 |
| V-3b | R-4 | R-4 limited to PINS-A l.540-543. l.544-546 is left to host H-21, because the host registers first | CC-254r2 N99, Ruling 6 |
| V-4 | §2 corollary (a) "E[ρ_A7] = E[φ_A7] … isolates the ρ − φ term" | deleted. Restated: A7 is matched per demonstration (PINS-A l.150, l.156); pooled ρ_A7 and φ_A7 are reported as measured; selectivity = OR_PVR / OR_A7 in odds form; analytic pool-level null added; the caption-level contrast passes through H-COPY and emptied demonstrations | CC-253 MB4; J2 W2 |
| V-5 | §1 wording rule | "verification" needs (i) OR_PVR / OR_A7 CI below 1 and (ii) PVR − A7 Holm-significant | CC-253 MB4 |
| V-6 | — | C_NEXT_STEPS §5 flagged as resting on the withdrawn corollary (E3); not edited | CC-253 MB4 |
| V-7 | §4 headline table | rebuilt. "The rule" is defined per tier (tier 1 = §12 iv go). HW-1a/HW-1b name P_obj^VI and are conditional on the rule, with a pre-written failed-rule sentence. The harm clause appears only if HW-2 holds. "was not shown to raise" is used. HW-3 names the tier-1 rule and never says PASS at tier 1. HW-0 closes the remaining case | CC-253 MB5 |
| V-8 | §5 "count of 'cây' mentions removed per arm" | renamed "mentions ignored by the sensitivity rule", a scorer-side count, not a data removal, supplement only | CC-253 CX2 |
| V-9 | §5 rule | hardened: raw-string adjacency, longest match over all NOUN_CLASSIFIER keys, drop only if the match is in K; K's coverage limit disclosed; A's owner told, rescoring labelled post hoc | CC-253 N-7, N-10 |
| V-10 | §6 item 15 "tone-ambiguous nouns merged by raw_tone=False" | corrected: norm_tone moves tone placement only | CC-253 N-7, Ruling 8 |
| V-11 | §3, R-1, R-2, §12 PI Q8/Q5 rows, VN summary | PI-1104ah cited; R-1/R-2 bind unconditionally; default rows removed | CC-253 N-1 |
| V-12 | §9 thresholds, E1, VN summary "33–37" | labelled illustrative (verifier arms cost more); aligned to the recomputed table (32.3–37.2) | CC-253 N-4 |
| V-13 | §2 title and framing | called an exact odds accounting identity, without a rigour oversell | CC-253 N-6 |
| V-14 | §8 MeaCap | Zeng et al., CVPR 2024, arXiv 2403.03715; described as retrieve-then-filter of memory concepts for zero-shot captioning, not ICL demonstrations; "[verify before cite]" dropped per the panel's source check | CC-253 N-8 |
| V-15 | header l.3 | tier IRREVERSIBLE, full panel + Codex at 85 | CC-253 N-11, TIER |
| V-16 | new §10 note | the overlap with host H-10 / H-12 is stated (host v2 8127874d then; now v3 e9c04955, commit 5d6f5ca); R-3 / R-3b are the final text | CC-254 Item 2; MB2 single home |
| V-17 | §12 | PI rows replaced by CC-253 PI questions 2 and 3 | CC-253 "For the PI" |
| V-18 | §7 | NoCaps-test base rate cited with its committed aggregates (39,975 / 74,502) | – (clarity) |

## 15. Change table against v2 (9aae4184)

| # | v2 place | v3 change | source |
|---|---|---|---|
| W-1 | §1 rules (i)/(ii); §2 A7 reference and checks | A7 follows PVR-drop only at tier 1 (PINS-A l.158-159). Rule (i) uses OR_V / OR_A7 with V = PVR-drop (tier 1) or the §6.3-selected variant fixed before tier-2 data (tiers 2-3). OR_PVR-keep / OR_A7 is labelled "not count-matched" (W5 l.160) and is not a selectivity measure. Rule (ii) is directional: "V > A7, Holm-significant". A rule (i) claim on another set needs its OR registered first | CC-253r2 RB1, N1; PINS-A l.157-160 |
| W-2 | §10 | new row R-10 supersedes committed host l.95-97 with the T1-REP §9 form, including T_down. Every "host amendment v2" reference is now the v3 file name with e9c04955 / 5d6f5ca (header, VN summary, §9, overrules, V-16) | CC-253r2 RB2; CC-254r3 N116, N120 |
| W-3 | §10 | new row R-8b marks prereg §14 Q-cost l.809 as answered YES (PI-1102a), with its cap form and the 20 h default superseded by PI-1103g, PI-1104af and R-3 / R-3b; overrules list extended | CC-253r2 RB3 |
| W-4 | §10 overlap note | H-18 (PINS-A l.541-542) named beside H-10 and H-12 | CC-253r2 RB4 |
| W-5 | §2 flag | C_NEXT_STEPS §5 revised by a dated note to the odds-form account (pre-edit copy kept); the two withdrawn sentences are struck | CC-253r2 CX3; CC-253 MB4 |
| W-6 | §4 | "the rule" keys the A8 clause: tier 1 §12 (iv), tiers 2-3 condition 1 of §5.3 / §5.4. Lowered case L added (HW-La, HW-Lb). HW-3 has x [CI] placeholders. Tier-1 sentences labelled in-sample | CC-253r2 N2 |
| W-7 | §9 overrules | CC-236 overrule limited to Ruling 5 row A13 and W7; the two-stage pin stays | CC-253r2 N3 |
| W-8 | §9 step 3; R-3 | "M = 465,000 VND, subject to solvency" | CC-253r2 N4 |
| W-9 | §3; new R-9 | PINS-A l.685-686 A4/A9 helper text amended to never-cut | CC-253r2 N5 |
| W-10 | §5 limits | the "cầu thủ" limit is disclosed | CC-253r2 N6 |
| W-11 | §12 | PI rows updated for PI-1105a / PI-1105c and the path record; CC-253r2 PI Q1 (split) and Q3 (Q-cost) added | CC-253r2 N9, N12, N14 |
| W-12 | §8 | MeaCap attribution corrected (CC-253 N-8 ordered the check; the CC-253r2 judges verified it) | CC-253r2 N10 |
| W-13 | §9 T_down; R-3 | the T_down value is no longer restated; it is cited from host §3 | CC-253r2 N11 |
| W-14 | §5 Paper A | the notice to A's owner is a coordinator LOG step, not yet recorded | CC-253r2 N14 |
| W-15 | header, sources | v3 status (round 3/3); CC-253r2, CC-254r3 and PI-1105c added | CC-253r2 NEXT STEP |
| V4-1 | l.20; l.79, l.127, l.495; l.392, l.397 | v4 changes only these lines. (1) l.20 now gives the full PINS-A v1.4 sha 624b0804…e417b8c99f; v3 spliced the tail "b16b148" from another file's sha, an anchor miss not caught in CC-253, CC-253r2 or CC-254r3. Erratum, not edited here: the committed host v3 (5d6f5ca, e9c04955) l.21 carries the same spliced tail; the correct PINS-A sha is 624b0804932731e3881cf058f6e680f96db476a0e1b852e615d920e417b8c99f. (2) l.392 and l.397 now agree with §2 l.170-173: the plan file was revised to 639192a4 (N-a). (3) the A7-variant cite is PINS-A l.158-159, not l.157-158 (N-b). Status: T1-GUARD v3 is committed alone at f5c6741 (PI-1105f) | CC-253r3; PI-1105f (PQ-REP YES, N-a, N-b) |
