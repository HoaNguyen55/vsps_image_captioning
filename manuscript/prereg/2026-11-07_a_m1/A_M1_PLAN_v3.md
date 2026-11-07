# Paper A, A-M1: a reference-only bound on gold completeness (an upper bound on coverage, a lower bound on the missing share), with a k→K prediction. Plan v3 (pre-registration style)

Status: PLAN ONLY. Nothing has been run, no A-M1 code exists, and nothing is committed. The paper repo is untouched.
- v1: A_M1_PLAN_v1.md (d874fb60), written 2026-11-07T02:49Z; kept unchanged.
- v2: written 2026-11-07T03:42Z (`date -u`). It changes only the CC-285 items (round 1, NEXT_ROUND 80, with its erratum): B1–B4 BLOCKING, and N1–N12 where they are plan text. The item map is §13.
- v3: written 2026-11-07T04:04Z (`date -u`). A minimal diff from v2 (84ab7198, kept unchanged) for CC-285r2 (round 2, NEXT_ROUND 83): B5 BLOCKING, plus N-A, N-B, N-B2, N-C, N-D and N-E. The hunk map is §13.2.

Plan step: DEPTH_PLAN_2026-11-07.md (e8e2ab45, untracked) §1.2 and §5 rank 1.

Mandate: PI-1107c (LOG l.1757). A-M1 means a Chao2-type lower bound plus a falsifiable k→K extrapolation, CPU only, on COCO-5000 and UIT-ViIC 231. It goes into SPIC only if its result read is GO before 2026-11-20. Q-A2 default no: no KTVIC/OpenViIC. Q-A4 default yes: A-M2 stays in the toolkit, outside this plan.

Theory it joins:
- A_THEORY_DRAFT_2026-11-06_v2.md: 111cb591 at c914018; working tree 87cad3bc after rev 4.2b, 6e3f1f3.
- A_SUPP_S1_PROOFS_DRAFT_2026-11-06_v2.md: committed c914018; working tree 1ae396b1.
- Paper §4.1: (A1), the propensity π, and the accumulation curve Ḡ(k) (Colwell et al. 2012; Chao et al. 2014).
- Paper §5: (A1) diagnostics.

Binding records:
- CC-274 (GO 88 with addendum A1–A4): the D1–D5 labels and wording limits, and W5.
- CC-271r2 and CC-266r3: the one-attempt run pattern and custody.
- A_DCHECKS_PLAN_v3.md (03c0b975, e0b52ce) and scripts/a_dchecks/a_dchecks.py (37b2946d, 187decb): house pattern and reused helpers.

Tier: REVERSIBLE, threshold 85 (PI-1103ad/ae). Dev-only laptop CPU, spent sets, no test look, no money.

Ruling history:
- CC-285 (round 1, NEXT_ROUND 80): B1–B4 BLOCKING, N1–N12 NON-BLOCKING. v2 addresses all of them (§13).
- CC-285r2 (round 2, NEXT_ROUND 83): B1–B4 closed; B5 BLOCKING (a recorded V1 VIOLATED could still be hidden); N-A to N-E NON-BLOCKING. v3 addresses all of them (§13.2).

Next steps:
1. CC-285r3, a one-judge FULL read of this file at 85 (round 3 of 3, the last before ESCALATE_TO_PI).
2. Gatekeeper commit after a GO.
3. Write `scripts/a_m1/a_m1.py` with its selftest, synthetic calibration and mutants.
4. One-judge code read.
5. freeze, gate, run (one attempt).
6. Result read at 85.
7. S1.M draft (DEPTH_PLAN rank 4).

Hard date: the result read must be stamped before 2026-11-19T17:00:00Z (20/11 00:00 VN), otherwise A-M1 leaves SPIC (§8.4).

## 0. Binding rules

- **Data.** Spent dev sets only (PORTFOLIO_3Y_2026-10-29.md §2.3): COCO Karpathy test (COCO-5000) and UIT-ViIC test (231).
  - No XM3600 in any form. A-M1 never opens, hashes or imports-and-calls anything that reads `data/xm3600/*` or `data/datasets/xm3600/*`; `score_g2b.xm3600_context` is never called. Reasons: K = 2–3, K is not constant (§2.2 needs a constant K), and `oiv7_labels.json` is registered tier-1 gold of Paper C under its access log.
  - No KTVIC or OpenViIC (Q-A2 default), no PASCAL-50S (outputs deleted; spent test), no A-T3 COCO val2017, no NoCaps/TextCaps/OI test captions or labels, no `t2pool_*`.
  - Never `~/.vsps_sealed`: not opened, listed or stat-ed.
- **Inputs.** References and existing human labels only. No system output is read: A-M1 needs no caption from any model. `data/object_gold/annot_claude.json` is never read; AI labels are not evidence. No new gold, no annotation, no rating.
- **Status.** Every check is post hoc relative to the D-checks and is run on development data. It gives no verdict on any registered prediction. X4, X5, A27, A28 and the D1–D5 labels are unchanged whatever happens (CC-274 Ruling 1).
- **Outputs.** Pooled counts, estimates, intervals, labels and shas only. No caption text, no per-image class list, no image id outside the reused freeze lists.
- **Barred by CC-274 addendum A1.** No ŵ-based split of any gap. The depth plan's optional "size vs selection from leave-one-out ŵ" row is dropped, and so is any link to X5's "19.08 of 38.15".
- **Withdrawn values never reappear.** Chao2 "debiased ceiling" 0.9468/0.848, Chao2 0.7325, LOO 0.7072 (results_plan.md l.14–15). No earlier Chao2 script is reused except the pinned, selftested `p50x.f0_hat` (§2.4).
- **Paper wording.** "Development data". No AI mention, no data-overlap wording, no "first". Section 10 binds.
- **Notation.** As in the v2 drafts: C_i, ℓ_i, Q_i, w_ic; n images; slopes ×100.
  - The paper writes k for the number of references. This plan keeps the D-check letters: K = 5 references per image and k < K for a subset.
  - Frequency counts are φ_j, to avoid a clash with the paper's Q_i. At transfer the writer maps K → k and k → r.

## 1. What the planner saw before fixing the rules (disclosure)

This is not a blind test. Before writing §5, the planner read these committed or stored records:
1. `r4_full5000_all9.json` (332da8b6, commit 51ef280) gives the mean first-k union size on COCO-5000, arm U, key `U.refs{k}_firstk`: k = 1..5 gives 1.367, 1.693, 1.865, 1.986, 2.078. The key `U.inst` is 2.863, and `gold.*.Gbar` also exists. So the observed 3→5 gain on COCO is about 0.21 classes per image, about 10% of U_5. No φ_j, no Chao2 value and no extrapolation on this estimand was seen.
2. The in-house X1 dev check, `.session_backup/2026-10-29/a_x1_devcheck/devcheck_result.json` ("EXPLORATORY dev check on spent sets; no verdict").
   - It applied the same `p50x.f0_hat` extrapolation to a different estimand: per-run true mentions of system outputs.
   - On COCO-5000, mean absolute precision errors at T = 3 → 5 were raw 3.346 and chao 1.371. At T = 2 → 5 they were raw 7.01 and chao 5.37. uv231en and cv295 show the same pattern.
   - Read as a hint, the extrapolation recovered part of the gain at k = 3 and less at k = 2. That points to under-prediction, which a lower-bound-based tail model is expected to produce under heterogeneity.
3. `c2_n1_uitviic_mstar.json`: key names only (gold variants). No UIT-ViIC reference count was read.

Consequences:
- k is fixed by a stated principle (§5.2), not by these numbers.
- The only falsifier of the bound is V1, with labels. Its power is measured on synthetic worlds only (§5.3, §7.2).
- The planner's estimate (not a judgment) is P(V2-A PASS on COCO-5000) ≈ 0.3. The likely outcome is BOUND_ONLY (§5.5).
- V1's CONSISTENT outcome on COCO-5000 was foreseeable from the r4 aggregates already seen (N12). For V1 to fire, f̂_0^L would have to exceed L − U^L. U^L itself was not seen, but `U.inst` 2.863, `U.refs5_firstk` 2.078 and `U.inst+refs5` 3.17 put L − U^L at roughly 1.1 pairs per image (CC-285 Ruling 4). V1 therefore carries little evidence on COCO, and §10.2 says so.

## 2. Estimand, estimator and assumptions

### 2.1 Data per set

- Images i = 1..n: COCO-5000 has n = 5,000; UIT-ViIC has n = 231. Vocabulary V = coco80.
- References R_i1..R_iK ⊆ V are the matched class sets of the first K = 5 references:
  - COCO: `score_g2b.karpathy_refs`, then `sc.en_classes(s, SYN)`, English;
  - UIT-ViIC: `score_g2b.uitviic_context()["lexicons"]["coco80"]["refs"]`, the Vietnamese matcher `vi_objects`.
  These are the same calls as the COCO and UIT parts of a_dchecks.py `load_sets`, restated in A-M1 because `load_sets` also calls `xm3600_context`.
- Two arms define the class universe of a pair (i, c):
  - **Arm U**, label-free: all c ∈ V. This is the use case, a set with references and no labels.
  - **Arm L**, validation: c ∈ C_i (COCO instance labels; `data/uitviic/instance_gold.json` for UIT-ViIC), with incidence from R_ik ∩ C_i. Here L = Σ_i ℓ_i.
- Incidence count: Y_ic = Σ_k 1[c ∈ R_ik] ∈ {0..K}.
- Pooled frequency counts: φ_j = #{(i, c): Y_ic = j}, j = 1..K.
- Observed pairs: U = Σ_{j≥1} φ_j = Σ_i |∪_k R_ik| (arm-restricted).

### 2.2 Assumptions, and what each buys

| | Assumption | Buys | Evidence on dev | Not tested |
|---|---|---|---|---|
| A1 | Given image i, the K references are i.i.d. draws from one law P_i on subsets of V (paper (A1)). Classes within one reference may be dependent in any way. | For each pair, the K indicators are i.i.d. Bernoulli(w_ic) with w_ic = P_i(c ∈ R), so E φ_j = Σ C(K,j) w^j (1−w)^{K−j}. Within-reference dependence drops out, because expectations are linear over pairs. | D2 PASS (CC-274 addendum A1: test result only). D2 tests metric scores by reference position, not class-naming laws by writer (N1). §5 adjacency at the null: COCO 0.407 [0.379, 0.433] on 4,867 images, and UIT-ViIC 0.384 [0.366, 0.403] on all splits (3,842 images). These are not the 5,000 / 231 images analysed here (N2). Adjacency tests file order only. | Writer independence (paper §5: "does not test writer independence"). Identical distribution across writers (B1): a fixed panel of writers is independent but not identically distributed. |
| A2 | Given the images, reference draws are independent across images. | The law of large numbers for the pooled counts (§3.2), and the image bootstrap. | none | Cross-image dependence through shared writers is not tested: all of UIT-ViIC, and AMT workers on COCO. Image-bootstrap intervals may then be too narrow (§3.3, N9). |
| A3 | The same K for every image (K = 5). | Lemma 1 holds pooled. With mixed K the factors differ by image. | gate G2 asserts it | — |
| A4 | liminf (1/n) E φ_2 > 0. | The ratio is defined in the limit. | trivially true at these n if φ_2 > 0 | — |

No homogeneity of w is assumed, across classes or across images. That is what the Cauchy–Schwarz step buys (§3.1).

**Collection protocol per set (B1(a)), with sources.**
- **COCO captions.** Chen et al. 2015, arXiv 1504.00325, "Microsoft COCO Captions: Data Collection and Evaluation Server" [A]: "five independent human generated captions" per training and validation image. That the writers come from Amazon Mechanical Turk, a large pool, is NOT in the abstract: it is [R], from memory, and the paper body must be read before it is printed (CC-285r2 N-B). (A1) is plausible here: a random-worker mixture is i.i.d. once the workers are averaged out. Plausible, not tested.
- **UIT-ViIC.** Lam, Le, Nguyen & Nguyen 2020, ICCCI, arXiv 2002.00175. The full text was read by the planner on 2026-11-07 (§3.1–§3.2), and also in CC-285 check 6.
  - "Our human resources for dataset construction involve five writers", for all 3,850 images.
  - The tool lets users "look back their works or the others' by searching image by image ids".
  - It shows COCO category hints as icons, and the "original English captions" on request.
  - Guideline 7: "Annotators can describe the activities and objects from different perspectives."
  - The paper does not say who wrote which reference of an image. A fixed panel of five writing one reference each is the natural reading, but it is an inference.
- **Consequence for UIT-ViIC.** Three mechanisms bear on (A1):
  - (i) a fixed panel: independent, not identically distributed (§3.3);
  - (ii) seeing the others' captions, together with guideline 7: a route to avoidance (§3.3);
  - (iii) English captions shown on request: copying from outside the five, which is positive dependence.
  On UIT-ViIC, (A1) is a modelling assumption and is not checked. Every printed UIT-ViIC estimate carries the five-writer caveat (§10.2). The writer-panel worlds of §7.2 show how the estimator behaves under (i).

Not used: any model for which classes writers name (salience). Classes with w_ic = 0 are outside the estimand (§3.4).

### 2.3 Estimand

- Nameable pairs: S = #{(i, c): w_ic > 0}. In arm L, S^L ≤ L.
- Nameable but unnamed after K references: f_0 = S − U.
- Coverage of the K-reference gold: C_K = U/S (realised) and E[U]/S (expected).
- Missing share: m_K = 1 − C_K.

These are quantities in matched-class space: "nameable" means the matcher extracts c from a random reference with positive probability. In arm U, matcher false positives are nameable pairs by this definition. In arm L they are removed by the intersection.

### 2.4 Estimator (reused code: `p50x.f0_hat`, 3f562e878ed7, selftested at l.295–297)

- f̂_0 = ((K−1)/K)·φ_1²/(2φ_2) if φ_2 > 0, else ((K−1)/K)·φ_1(φ_1−1)/2. This is `f0_hat(φ1, φ2, K, inf)`, the incidence Chao2 form and its bias-corrected form at φ_2 = 0.
- Ŝ = U + f̂_0, Ĉ_K = U/Ŝ, m̂_K = 1 − Ĉ_K.
- Pooled over all (image, class) pairs of a set, never per image, and never summed over per-image ratios (§3.3).
- Per-subset form, for |A| = k positions: φ_j^A and U_A come from the references in A only. Ŝ_A(k) = U_A + f0_hat(φ_1^A, φ_2^A, k, inf).
- Extrapolation to K references from k (`f0_hat(φ1, φ2, k, K)`, Chao et al. 2014 [R], as implemented in p50x):
  Û_A(K) = U_A + Q̂_0^A·[1 − (1 − φ_1^A/(k Q̂_0^A + φ_1^A))^{K−k}], with Q̂_0^A = f0_hat(φ_1^A, φ_2^A, k, inf).
  Derivation (tail model): if the Q_0 unseen pairs and the singletons share one detection probability w*, then E φ_1/E Q_0 = k w*/(1−w*), so w* = φ_1/(kQ_0 + φ_1). K − k further references then find Q_0[1 − (1−w*)^{K−k}] of them. This is an approximation and is exact only when the tail is homogeneous. Its direction under heterogeneity is not established (§3.3).
- All C(K, k) position subsets are enumerated deterministically. Means are over subsets: Ū_k = mean_A U_A (the exact sample-based rarefaction under A1), and Ū(K←k) = mean_A Û_A(K).

## 3. What is proved and what is not

### 3.1 Lemma 1 (expectation bound; Chao 1987 [R], restated for pooled pairs)

Under A1 and A3, summing over pairs with w > 0:

E f_0 = Σ (1−w)^K ≥ ((K−1)/K)·(E φ_1)²/(2 E φ_2), whenever E φ_2 > 0.

For K ≥ 3, equality holds iff w is constant over the pairs with 0 < w < 1. Pairs with w = 1 add nothing to either side when K ≥ 3.

Proof sketch. Write E φ_1 = K Σ w(1−w)^{K−1} and E φ_2 = C(K,2) Σ w²(1−w)^{K−2}. Set a = (1−w)^{K/2} and b = w(1−w)^{K/2−1}, so Σab = E φ_1/K, Σa² = E f_0, and Σb² = 2E φ_2/(K(K−1)). Cauchy–Schwarz (Σab)² ≤ Σa²·Σb² rearranges to the claim. Equality holds iff a ∝ b, that is, iff w/(1−w) is constant.

The result is Chao's (Chao 1984 for abundance; Chao 1987 for capture–recapture with heterogeneous catchability). Neither is claimed as new. The only adaptation is the pooling over (image, class) pairs with a common K.

### 3.2 Proposition 2 (asymptotic lower bound; proved under A1–A4)

Condition on the images, so that w and S are fixed, and assume per-image counts bounded by |V| = 80. As n → ∞:

limsup (f̂_0 − f_0)/n ≤ 0 almost surely.

Hence limsup (Ŝ − S)/n ≤ 0, liminf (Ĉ_K − U/S) ≥ 0 when S/n stays bounded away from 0, and liminf (m_K − m̂_K) ≥ 0.

Proof sketch (N3; no limit of the means is assumed):
- Write g(x, y) = ((K−1)/K)·x²/(2y). Decompose
  f̂_0/n − f_0/n = [g(φ_1/n, φ_2/n) − g(Eφ_1/n, Eφ_2/n)] + [g(Eφ_1/n, Eφ_2/n) − E f_0/n] + [E f_0/n − f_0/n].
- First term → 0 a.s. (φ_1, φ_2, f_0)/n minus their means → 0 a.s. by Kolmogorov's strong law: the summands are independent across images (A2) with bounded variances. g is uniformly continuous on [0, 80] × [ε, 80], where ε > 0 comes from (A4).
- Second term ≤ 0 by Lemma 1.
- Third term → 0 a.s., by the same strong law.
- The φ_2 = 0 branch is asymptotically irrelevant under (A4).

Reading: Ŝ is asymptotically a lower bound on the number of nameable pairs, Ĉ_K an upper bound on the coverage of the K-reference gold, and m̂_K a lower bound on its missing share.

### 3.3 Not proved (and not claimed)

- A finite-n bound. The plug-in ratio has an O(1/n) bias of either sign, and UIT-ViIC has n = 231. The bootstrap interval is reported; no finite-sample guarantee is.
- Any per-image version, or a sum of per-image Chao2 values. With 1–5 pairs per image, the asymptotics do not apply.
- The accuracy or the direction of the k→K extrapolation (§2.4). It is a tail approximation, and §5.2 tests it empirically. Under-prediction under heterogeneity is expected (Lemma 1 is loose there) but not proved.
- That a k→K PASS supports the bound. It does not: it tests the near-range tail only, and it is blind to singleton-type violations, which inflate the asymptote Ŝ while leaving ε_k ≈ 0 (§5.2).
- Anything without A1. Positive dependence among writers that is not representable as a mixture of i.i.d. draws, and negative dependence of any kind, can void Lemma 1.
- **The fixed-panel case (B1(b)).** If a fixed panel writes the K references, one each, the K indicators of a pair are independent but not identically distributed (capture–recapture model M_th), with writer probabilities p_1..p_K.
  - Per pair, write x_k = p_k/(1−p_k). The Chao2 expectation ratio ((K−1)/K)(Eφ_1)²/(2Eφ_2) / E f_0 then equals ((K−1)/(2K))·e_1(x)²/e_2(x), with e_j the elementary symmetric polynomials. By Newton's inequality this is ≥ 1, with equality iff all p_k are equal. Within-pair writer heterogeneity therefore pushes Chao2 in the inflating direction.
  - Pooled over pairs, between-pair heterogeneity of w pushes the other way (Lemma 1). Which effect wins is not established.
  - CC-285 check 7 (exact enumeration, judge scratch, not a record): a common multiplicative writer effect keeps the bound, while "one-writer-dominant" pairs break it (ratios 1.55 and 5.25).
  - So on UIT-ViIC the bound is not guaranteed. §7.2 registers two writer-panel worlds, and §10.2 the caveat.
- **Avoidance through the annotation tool.** Writers who see the others' captions and are asked for "different perspectives" can avoid each other's objects. That is negative dependence, which can void Lemma 1 (§5.2: it inflates Ŝ, and V2-A cannot see it).
- **Interval width under shared writers (N9).** (A2) fails if the same writers serve many images (all of UIT-ViIC; AMT workers on COCO). Image-bootstrap intervals may then be too narrow. This note goes into S5 beside any interval.
- Tightness. The gap S − Ŝ grows with the heterogeneity of w and is not estimable.
- A sensitivity bound for X4 (the depth plan's item (c)). It needs which out-of-union mentions are nameable, which is unobservable; on PASCAL-50S it also needs references that were deleted. It is dropped (§11 J11).

### 3.4 Remark 3 (not identified; proved)

Pairs with w_ic = 0 are not identified by any function of the references. The law of (R_i1..R_iK) is unchanged by adding or removing such pairs. In arm L, L − S^L (labelled but never named) is therefore not estimable from references. Asymptotically, L − Ŝ^L is only an upper bound on it.

### 3.5 Remark 4 (extendible exchangeability; proof sketch, to be checked at the S1.M read)

If the K indicators of each pair are a mixture of i.i.d. Bernoulli(W) with random W (de Finetti), then E φ_j = C(K,j) E[W^j(1−W)^{K−j}]. Lemma 1 then follows by Cauchy–Schwarz over the joint law of (pair, W), with E f_0 = Σ E(1−W)^K. So positive dependence of mixture type keeps the bound, and only dependence that cannot be extended (for example writers avoiding each other's objects) breaks it.

This is not printed until the S1.M read verifies it (§11 J7).

**Finite-panel caveat (B1(c)).** Remark 4 does not cover a finite panel. Five fixed writers in random order give exchangeable indicators, by a draw without replacement from a finite panel. That law is not a de Finetti mixture of i.i.d. draws, and its non-identical writer laws fall under the fixed-panel item of §3.3, where Newton's inequality points the inflating way. Remark 4 therefore gives no support for UIT-ViIC.

## 4. Data and pinned inputs (precondition)

Full sha256 of every file A-M1 reads. Each was re-hashed at writing (2026-11-07). Every data file was already pinned by a_dchecks PINS or committed at 1f157d2 under CC-274; a_dchecks.py is at 187decb.

| Path | sha256 |
|---|---|
| data/datasets/karpathy/dataset_coco.json | 2fd999220673258012acfb411a4e7e66af7d488050b2519b0badcc49b7600b8d |
| data/coco_probe/manifest_full5000.json | 699769100c572675dfc4ae9f2a45f01bf387c4b1d67e9019feafc8c14fc88f7e |
| data/results/a_dchecks/freeze/instance_gold_full5000.json (tracked, 1f157d2) | bd36295146e505454f5110e817841d8300a024265c1f2cba2aade854119183f7 |
| data/results/a_dchecks/freeze/coco5000_ids.txt (tracked) | d20da3dd48646d91a7ff7837c1c1f591d52c75e72921b2fd7f6854dc1093339f |
| data/results/a_dchecks/freeze/uitviic231_ids.txt (tracked) | 96e6ffe998c0b4caf2eccb45c2b1379637bee2ddccdd18452eb8808dc63e8ecb |
| data/results/a_dchecks/freeze/freeze.json (tracked; pass = true) | 5237c7b2b90fa525dccf272367df90ee41f3c5def7933bda031f65c68fc928f7 |
| data/datasets/uitviic/test_data.json | 54abc0fb068ad1108d7d57b21328d4d68bcf8f41aa168f80ec7c275fb4ac8214 |
| data/uitviic/instance_gold.json | 278d15b97e3eeb9496a0282bb91deb365117becf24d174fbb1e0507203b12ea4 |
| data/coco_probe/coco80_vi.json | 926e08571ef6e80a7f8aae8f2b73753d6c5c54c431a750ba2b67bfaae71b540b |
| data/coco_probe/chair_synonyms.txt | b685537b36fe21b791c87151b96a991ceb582edff19f3da204dcc7a7905502f2 |
| .session_backup/2026-10-26/a_full5000/out/r4_full5000_all9.json (anchor; 51ef280; only the `U.*` keys are read, N8) | 332da8b6264c9c05232e5ef70cd864a0fe7ce58480e99aee558b1115a5c793af |
| scripts/g2b/score_g2b.py | 66c665c7a71d3b97abbf89fd5bf13871910449ad1c053ff5fb0b18663e3e7ae5 |
| scripts/score_coco_probe.py | d11db7e192f689980bb2b2bb717d852d9aa339ad857ce9411fe7bdd6fe416070 |
| scripts/pascal50s/p50x.py (f0_hat) | 3f562e878ed793f4b3cae84dd93373b10d82564d162cb399ab16e03ccf8825c2 |
| scripts/pascal50s/p50.py (imported by p50x) | 2387ca05ae8a57304a5f696c4e2f73d29297d03ccc23debb416269dc7a676d31 |
| scripts/a_dchecks/a_dchecks.py (helpers only) | 37b2946d739b476520de09d32272d452837c651369454673b38363444ffc1d36 |
| rescap/__init__.py | b712bea4d66e5e2e0f0cec1624ab244a025560ecc5d86f96cada2e0160a4890f |
| rescap/chair.py | e47d249ac7290070f2387d3fa8b22dac77728265ad276f55aa6520f5cbc591a3 |
| rescap/metrics.py | e0296ec528b87f4d1b31165cbb45deee5453783fd7dad783f248869e596bf960 |
| rescap/repro.py | 723200190818cd61a56527e6a0a1596b95f9d1ed1ebc0cabe1b29135cf03b70d |
| rescap/svp/__init__.py | 5b7f52920de75cf59bde0ae657e292a876efc63292ca6db6a4d085bb9fec1424 |
| rescap/svp/entailment.py | 4462f44df80faa0adc620d98aa5d8bbb307243d450e9aee4801bb17a3a06db23 |
| rescap/svp/matching.py | a9253060131aacfca8eaab9a4b2c473c487db96a7c1222f0b8e31f9f61b24003 |
| rescap/vi/__init__.py | f898963e95fec7d9fb236295649404815634a1d949bfd74cd7c3b90ed493bf6c |
| rescap/vi/classifier.py | 966cdab1fed8471ac57d225698e63f1e2a055435a5d669e9cca10eed703fed16 |
| rescap/vi/color.py | 242fc46f68ecb06c8eefde23350481d99e60566b3da64ab90cfa79db38fd3875 |
| rescap/vi/lexicon.py | fbc945f2247418275144ac75b893f7c51f8951b9ea42018680d433775dd79eb9 |
| rescap/vlm/__init__.py | 13de9854599acedd32ea1798ea1acc475703fcd3aa4eb4dd715dc8eadcd632cd |
| rescap/vlm/base.py | e8fee5bc5b729534af67c6e462a27f0d83ba611f18ff8e3f2717b11eb393ae93 |
| rescap/vlm/mock.py | 33793de01b4f2790964342b1af2d4c2de18d793ae4693608283992475ed62ce7 |
| rescap/vlm/registry.py | 6c261406bde3d34a73f77ce961aff7d241e2a440ba75e154fccf3ae8d4a70297 |
| rescap/vocab.py | c9143b2d973fc48a2231335844cd91ab702329c0b1aabb802884225e155967ec |
| scripts/clean_supervision.py | 01f172002a607ba9ee55bccb332439f10650832cae1f64a9b74b35c48cd9c231 |
| scripts/person_uncap.py | d16b19f6597f84597db7865dea4058f0bb1fecf914d71d34d6406d66283fa5bb |
| scripts/xm3600_oiv7.py (module code only: imported by score_g2b, never called) | 9a79403f4fc38609282d40082ab7f878133edca8aff9e0dc2462db467b7193f0 |

- The module rows above are the import closure of score_g2b and p50, the same shas as in a_dchecks PINS (the code read confirms the closure).
- No system-output file and no XM3600 data file is in the pin set. r4 is a results file that also holds per-system aggregate tables. A-M1 reads only its `U.*` keys (gate G3), and the code read checks that (N8).
- The import closure is checked fail-closed, as in `a_dchecks.load_libs`. Every imported repo module must be pinned. A-M1 needs its own loader, because `a_dchecks.load_libs` would reject `a_dchecks.py` itself, which is not in its own PINS.
- **Ids.** COCO-5000 is the 5,000 manifest ids, which must equal coco5000_ids.txt. UIT-ViIC is `uitviic_context()["ids"]`, which must equal uitviic231_ids.txt. No new id list is written.
- **Not used:** COCO images with more than 5 Karpathy sentences contribute their first 5 only, as in r4 and the D-checks. The extra sentences are not read as hold-outs. Their count is unknown and the depth plan did not fix them.

## 5. Registered checks, labels and decision rules

### 5.1 Common rules

- **Bootstrap.** Image bootstrap with B = 2,000 multinomial weight vectors per set and seed 20261107 + set offset (COCO 100, UIT 300). One weight matrix per set is shared by every statistic of that set. Every pooled count is recomputed per resample. Intervals are percentile intervals.
- **Sets are analysed separately and never pooled.** The EN (COCO) vs VI (UIT-ViIC) comparison is descriptive only, because the matchers differ.
- **Evaluability (CC-274 W5 ii).** Each check's evaluability is judged by that check's own rule (below), per set. A check counts toward the decision in §5.5 only on the sets where it is evaluable by its own rule.

### 5.2 V2: the k→K prediction (primary; arm U; label-free)

Statistic, for one set and one k:
- G = U_K − Ū_k is the observed gain from k to K = 5 references (exact rarefaction mean);
- Ĝ = Ū(K←k) − Ū_k is the predicted gain;
- ε_k = (Ĝ − G)/G = (Ū(K←k) − U_K)/G is the relative gain error. v2 wrote E_k; v3 writes ε_k so that the gain errors ε_2, ε_3, ε_4 never clash with the descriptive estimates E1–E5 of §5.4 (CC-285r2 N-D). "ε_4 beside ε_3" (B3(b)) is a gain error and may sit in the main text; E4 (the label-shortfall share) stays S5 only (J6).

NOT_EVALUABLE if the 2.5th percentile of G* ≤ 0.

**No one-sided "over-prediction" falsifier (found before the judge read).** An earlier draft had a check V2-O: FAIL on significant over-prediction of the gain, read as evidence against A1. It is dropped, because it cannot see the violation it was meant to catch.
- As Q̂_0 → ∞, w* → 0, and the formula of §2.4 tends to the linear form Q̂_0[1 − (1 − w*)^t] → t·φ_1/k, with t = K − k.
- In an "avoidance" world (each pair named by exactly one of the K references, with probability p), φ_2 = 0 and U_A = φ_1^A ≈ p(k/K)S. The true gain is pS(K−k)/K, and the predicted gain is ≈ (K−k)·p(k/K)S/k, the same number.
- So ε_k ≈ 0 there, while f̂_0 ∝ φ_1² sends Ŝ far above S.
- Copying between writers, the other plausible violation, gives under-prediction.
- A k→K check therefore tests the near-range tail only. It says nothing about whether the asymptote Ŝ is a valid lower bound (§3.3).

**V2-A, the accuracy band (two-sided; k = 3; both sets).** Three disjoint, exhaustive labels in the D3 scheme:
- FAIL if the 95% two-sided percentile interval of ε_3 lies entirely outside [−δ_A, +δ_A], with δ_A = 0.25. FAIL takes precedence.
- PASS if not FAIL and the interval lies inside [−δ_A, +δ_A]. This is equivalence by TOST at α = 0.025 per set, 0.05 over the two sets.
- UNDERPOWERED otherwise (the interval straddles ±δ_A).
- **Why k = 3, by principle (N5).** The Chao et al. 2014 abstract says its estimators "are accurate for both rarefaction and short-range extrapolation". This was verified in CC-285 check 10; the planner did not re-read it. The abstract does not define "short-range". This plan takes "short-range" to mean at most twice the sample, by convention. That convention is UNVERIFIED in the source (CC-285 N5) and is never printed as the source's guidance unless the full text is read first. Among k ∈ {2, 3, 4}, k = 3 is the smallest with K ≤ 2k, so it is the strongest test inside that range. k = 2 (K = 2.5k) is outside it, and k = 4 is a single step. The planner saw the X1 hint (§1, item 2) before choosing; the judge rules on whether the principle stands (§11 J1).
- **Why δ_A = 0.25.** By convention, the predicted gain is within a quarter of the observed gain. It is not derived from data. On COCO, §1 item 1 implies it equals about ±2.6% of U_5.
- The saturating predictor (Ĝ = 0, ε = −1) FAILs this band by construction, so a PASS is not trivial.
- The selftest reports the V2-A PASS/FAIL/UNDERPOWERED rates under the synthetic A1 worlds and the violation worlds (§7.2). Readers can then see how often the band fails when A1 holds and only the tail model is coarse, and that it can PASS when A1 fails.
- What V2-A is: the PI-mandated falsifiable k→K prediction of the incidence model's near-range extrapolation. It is not evidence for the lower bound. FAIL means only "the extrapolation is not supported".

Descriptive only, with no label: ε_2 and ε_4 in arm U, and ε_2, ε_3, ε_4 in arm L. Wherever ε_3 is printed, ε_2 and ε_4 (arm U, with intervals) are printed beside it (B3(b); §10.2). This neutralises the one choice the X1 hint could have favoured, k = 3 over k = 2.

### 5.3 V1: lower-bound consistency against labels (arm L; both sets)

- Prediction (Corollary of Proposition 2 with S^L ≤ L): Ŝ^L ≤ L asymptotically. Equivalently, the estimated coverage of the labelled nameable pairs, U^L/Ŝ^L, is at least the observed label coverage c_L = U^L/L.
- Statistic: D_L = (L − Ŝ^L)/L.
- Labels: VIOLATED if the 97.5th percentile of D_L* is < 0. That is significant overshoot of the label universe, one-sided α 0.025 per set and 0.05 over the two sets. Otherwise CONSISTENT. Never "PASS".
- V1 is the only falsifier of the bound. The bound in the label-free arm U is not checkable without labels; V1 checks it on the same references restricted to labelled classes.
- Power:
  - weak against mild violations, because labelled classes that nobody names (w = 0) push D_L positive whatever happens;
  - strong against singleton-type inflation (avoidance, forced singletons), where f̂_0 grows like φ_1².
  - The selftest measures both on graded synthetic worlds (§7.2). The expected outcome on dev is CONSISTENT. It carries limited evidence, and that is stated wherever it is printed.

### 5.4 Descriptive estimates, per set (no label; 95% percentile intervals)

- E1: Ŝ (asymptotic lower bound on nameable pairs), Ĉ_5 (asymptotic upper bound on coverage) and m̂_5 (asymptotic lower bound on the missing share), in arms U and L.
- E2: the stability curve Ŝ(k) = mean_A Ŝ_A(k) for k = 2..5. A rising curve means the bound at K is not tight.
- E3: coverage of the k-reference gold, Ĉ_k = Ū_k/Ŝ(5), for k = 1..5. The depth plan's "one-reference coverage" is Ĉ_1.
- E4: arm L, the bracket observed label coverage c_L ≤ U^L/Ŝ^L, and (Ŝ^L − U^L)/(L − U^L): an asymptotic lower bound on the nameable-but-unnamed share of the label shortfall L − U^L. Its printability is ruled in §11 J6.
- E5: pooled φ_1..φ_5, U, L and n.

### 5.5 Decision mapping (fixed now; CC-274 4b lesson)

Status of A-M1, from the labels. Precedence (B2): FALSIFIED > NOT_RUN/FAULT > METHOD/BOUND_ONLY. The first rule that applies decides.
1. **FALSIFIED:** a V1 VIOLATED label is recorded for any set (a persisted `run_record/v1_<set>.json`, §7.1), whether or not that set, the other set or the run later completed. This covers an exception or the cap inside the same set after V1, a FAULT or NOT_RUN in the other set, and a dead run. A registered falsification is never hidden by a later fault (B5).
2. **NOT_RUN / FAULT:** otherwise, if either set did not complete (any check FAULT or NOT_RUN). Nothing is printed (§10.3).
3. **METHOD:** both sets completed, V1 CONSISTENT on both, V2-A PASS on COCO-5000, and V2-A on UIT-ViIC PASS or UNDERPOWERED. UIT-ViIC NOT_EVALUABLE also counts, with the wording in §10.3.
4. **BOUND_ONLY:** both sets completed, V1 CONSISTENT on both, and rule 3 does not hold: V2-A FAIL on either set, or V2-A not PASS on COCO-5000.

"Completed" means the set's run step returned its labels without FAULT and before the cap. A persisted V1 CONSISTENT record of a set that did not complete does not make that set completed. Mutants 17, 17b and 17c (§7.3) bind the precedence.

"FAIL means":
- V2-A FAIL: the k→K extrapolation is not supported at the registered tolerance. Only the lower-bound reading (Proposition 2) may stay.
- V1 VIOLATED: the estimate exceeded the label universe. The bound is contradicted, or the matcher and labels disagree; stop.

SPIC entry under PI-1107c, if the result read is GO before the deadline:
- METHOD: main text plus S1.M plus S5.
- BOUND_ONLY: S1.M plus an S5 table, and at most one main-text sentence (default; §11 J4).
- FALSIFIED: one supplementary sentence only.

A result read can be GO with any label, as CC-274 was.

T2 credit (the A writer re-scores; planner's estimate, not a judgment):
- METHOD: +0.5. A proved proposition plus a passed k→K prediction, each counted on the sets where it is evaluable by its own rule. The proposition is supported by V1 and D2 on both sets, and by §5 adjacency for COCO. On UIT-ViIC, (A1) is a modelling assumption (§2.2).
- BOUND_ONLY: at most +0.25. A proved proposition whose only data check is V1.
- FALSIFIED: 0.
- T1, T5 and T7 move (DEPTH_PLAN §1.2) only under METHOD.

Planner's estimates (not a judgment): P(METHOD) ≈ 0.3, P(BOUND_ONLY) ≈ 0.55, P(FALSIFIED) ≈ 0.1, P(FAULT) ≈ 0.05.

## 6. S0: freeze and gate (before any φ_j)

**freeze** (S0.1):
- Asserts every pin in §4.
- Asserts that the D-check freeze.json has pass = true and the listed id and gold shas.
- Writes `data/results/a_m1/freeze/freeze.json`: script sha, plan sha, pins, B, seeds, k sets, δ_A and the selftest sha.
- Reads no reference.
- A passed freeze is final. A failed freeze is renamed `freeze.failed_<utc>.json`, and its time is added to the cap (CC-271r2 N1r2).

**gate** (S0.2) computes no φ_j and no estimate. It FAULTs on any mismatch.
- G1: loaded ids equal the frozen lists (5,000 and 231, as strings, in the frozen order).
- G2: every image of both sets has ≥ 5 references; K = 5 is used everywhere.
- G3: COCO anchors against r4. mean_i |∪_{k'≤k} R_ik'|, arm U, all 5,000 ids, rounded to 3 dp, must equal `U.refs{k}_firstk` for k = 1..5 (1.367, 1.693, 1.865, 1.986, 2.078). mean_i ℓ_i must equal `U.inst` (2.863). Definition: `check_coco_full.py` l.79–81 and l.92 (`u_all`, key `U`), mean over all images including empty sets. This validates the reference extraction against a committed record.
- G4: UIT-ViIC uses the pinned `uitviic_context` unchanged. Its pipeline was anchored by the D-check gate (`scar_observed` uv231 cells and the g2b self-check). G4 records n and Σℓ_i only, never U_k.
- G5: selftest.json exists at the current script sha with pass = true, and the synthetic calibration acceptance holds (§7.2).
- G6: re-hash every pin.
- Each gate attempt is recorded. A re-run gate keeps the earlier record as `gate.failed_<utc>.json` (fixes N1r2).

## 7. Script outline, selftest and mutants (`scripts/a_m1/a_m1.py`; not written)

### 7.1 Subcommands

- `selftest`: synthetic data only, plus the calibration in §7.2.
- `dryrun`: asserts pins and prints the planned work; writes nothing.
- `freeze`, `gate`: as §6.
- `run`: refuses unless the script and this plan equal their HEAD blobs, freeze and gate passed at this script sha, and `a_m1_result.json` is absent.
  - Exclusive `run_record/STARTED.json`, one attempt (a_dchecks `claim_start`/`run_attempt` pattern).
  - **V1 persisted at once (B5(a)).** As soon as a set's V1 is computed, and before its V2-A, the V1 label, D_L and its interval are written atomically to `run_record/v1_<set>.json` (`<set>` = coco5000 or uitviic231): write a temp file in `run_record/`, fsync it, rename it over the target, then fsync the directory. Exactly one record per set, never rewritten.
  - The status of §5.5 is derived from the persisted V1 records plus the result file. If `a_m1_result.json` is absent (dead run), the result read derives it from `run_record/v1_*.json` alone, by rule 1 or rule 2.
  - The result is written in a `finally`.
  - `run_record/` gets rc and start/end UTC (CC-274 W5 iv).

Reuse:
- imported, never copied: `p50x.f0_hat`; `score_g2b.karpathy_refs`, `uitviic_context`, `sc.en_classes`, `SYN`; a_dchecks `sha_file`, `Budget`, `run_attempt`, `claim_start`, `env_guard`, `git_blob_sha`, `coco_complete`, `Fault`;
- own code: pin assertion (its own PINS dict), loader, pooled counts, bootstrap, labels.

Records are keyed by full path and set name, never by basename (CC-274 W5 i).

**Custody guard.** `sys.addaudithook` is installed before any import of repo code.
- An exact pinned path (a §4 pin, including the pinned module `scripts/xm3600_oiv7.py` that `score_g2b` imports) is always allowed. This precedence is needed because `io.open_code` raises the `open` audit event for imported modules.
- Any other `open` under the repo that is not under `data/results/a_m1/` raises a Fault.
- So does any path, anywhere, matching these patterns: `.vsps_sealed`, `t2pool_`, `data/xm3600`, `datasets/xm3600`, `xm3600_subset`, `oiv7_labels`, `nocaps`, `textcaps`, `ktvic`, `openviic`, `annot_claude`, `/results/coco5000`, `coco_transfer`, `g2b_score/outputs`.

### 7.2 Selftest

- f0_hat parity with the closed forms (the p50x l.295 values).
- Lemma 1: exact expectations over 10,000 random heterogeneous w vectors (K = 2..5): the inequality holds in every case, with equality at constant w.
- Rarefaction identity: mean_A U_A equals Σ_pairs [1 − C(K−Y, k)/C(K, k)] exactly.
- Label rules: constructed intervals give PASS/FAIL/UNDERPOWERED as disjoint and exhaustive; V1 at its boundary and in its direction.
- **Synthetic calibration, A1 worlds.** Configurations, fixed now:
  - n ∈ {231, 5000} images;
  - nameable pairs per image 1 + Poisson(λ), λ ∈ {2, 4}, plus labelled pairs with w = 0 making up about 30% of each image's labelled pairs. Integer rule, fixed now (CC-285r2 N-C): an image with s nameable pairs gets floor(3s/7 + 1/2) labelled pairs with w = 0. The same rule is used in every A1, violation and WP world. So L > S, as on real data;
  - w i.i.d. Beta(α, β) with (α, β) ∈ {(2, 2), (1, 1), (0.5, 1), (0.3, 0.6)}, plus a homogeneous world w ≡ 0.4;
  - K = 5 i.i.d. Bernoulli references per pair; 200 worlds per configuration; seed 20261107 + 9000; B = 200 in selftest only.
  The selftest reports per configuration:
  - the V1 VIOLATED rate. Acceptance: ≤ 0.05 in every configuration, otherwise a plan defect (new plan version, no data read);
  - the V2-A label rates at k = 3 (descriptive);
  - the share of worlds with Ŝ ≤ S (Proposition 2 illustration).
- **Violation worlds (power; reported, never tuned).** n ∈ {231, 5000} (v2 ran these at n = 5,000 only; n = 231 is added so that V1's power at the UIT-ViIC size is shown, CC-285r2 N-E), λ = 2, the same unnamed-label rule, and the rest of the pairs Beta(0.5, 1):
  - graded "avoidance" mixtures: a share ν ∈ {0.1, 0.3, 0.5} of nameable pairs is named by exactly one reference at a random position with probability p = 0.6, else by none;
  - "forced singletons": with probability 0.5 per image, one extra pair is named by exactly one reference and never by two;
  - "copying": each reference after the first repeats the previous reference's class set with probability 0.5. This is positive dependence, expected to make the bound more conservative.
  The selftest reports, per world and n, the V1 VIOLATED rate, the V2-A label rates and the share with Ŝ ≤ S. That shows V1's power against singleton inflation and V2-A's blindness to it (§5.2).
- **Writer-panel worlds (B1(d); registered now, reported, never tuned).** K = 5 fixed writers, one reference each, independent given the image. n ∈ {231, 5000}, λ = 2, the same 30% of unnamed labels, base w ~ Beta(0.5, 1), 200 worlds per configuration, seed 20261107 + 9500.
  - **WP-M, "writer panel, multiplicative":** p_ick = min(1, w_ic·m_k), with m = (0.6, 0.8, 1.0, 1.2, 1.4), a spread of ±0.4.
  - **WP-D, "writer panel, one-writer-dominant":** per pair, one writer drawn uniformly at random names c with probability p_hi and the other four with p_lo. The grid is (p_hi, p_lo) ∈ {(0.5, 0.2), (0.6, 0.05), (0.8, 0.1)}; base w is not used in WP-D.
  - Reported per configuration: the V1 VIOLATED rate, the V2-A label rates, the share of worlds with Ŝ ≤ S, and the mean Ŝ/S.
  - **Flag rule, fixed now.** Each configuration gets exactly one flag:
    - BOUND_HOLDS: mean Ŝ/S ≤ 1 and the share with Ŝ ≤ S is ≥ 0.95;
    - BREAKS_DETECTED: mean Ŝ/S > 1 and the V1 VIOLATED rate is ≥ 0.8;
    - BREAKS_UNDETECTED: mean Ŝ/S > 1 and the V1 VIOLATED rate is < 0.8;
    - MARGINAL: everything else (mean Ŝ/S ≤ 1, but the share with Ŝ ≤ S is < 0.95).
  - **Consequence rule, fixed now, applied at the result read.** If any WP configuration at n = 231 is BREAKS_UNDETECTED or MARGINAL, every UIT-ViIC bound estimate (Ŝ, Ĉ_k and m̂_k for all k, in both arms, and E4) is printed in S5 only, never in the main text, whatever the status. The five-writer caveat (§10.2) is printed in every case.
  - **Expected outcome, stated now (CC-285r2 Ruling 7, N-B2).** This rule will almost surely fire. In WP-D, V1 can fire only when Ŝ/S is well above 1, because the unnamed labelled pairs make L exceed S by about 1/0.7 (§5.3, "weak against mild violations"); a dominant writer with a moderate p_hi then inflates Ŝ without V1 detecting it. So the plan expects UIT-ViIC bound numbers in S5 only, with COCO-5000 as the only main-text case. No simulated number is cited here; the selftest's own values are reported as computed.
  - The flags gate nothing in freeze, gate or run, and no parameter is changed because of them. The selftest refuses to pass if any WP configuration is missing (mutant 18, N10).
- Every number here is synthetic and is never printed in the paper.

### 7.3 Mutants (each must be killed)

1. per-image Chao2 summed instead of pooled;
2. the (K−1)/K factor dropped;
3. the classic form used at φ_2 = 0;
4. V2 on first-k positions only instead of all subsets;
5. G computed with first-k Ū_k;
6. V2-A on the point estimate;
7. V2-A at 90% instead of 95%;
8. V1 VIOLATED tested on the 2.5th instead of the 97.5th percentile of D_L*;
9. arm L incidence not intersected with C_i;
10. more than 5 references used for COCO;
11. an XM3600 or system-output path opened (the audit hook must FAULT);
12. V1 labelled PASS, or on the two-sided interval;
13. bootstrap over subsets instead of images;
14. the shared weight matrix replaced by one draw per statistic;
15. records keyed by basename;
16. gate computing φ_j;
17. status precedence broken: COCO V1 VIOLATED followed by a UIT-ViIC FAULT (or NOT_RUN at the cap) must give FALSIFIED, not NOT_RUN/FAULT (B2);
17b. COCO V1 VIOLATED, then an exception inside COCO after V1, must give FALSIFIED; and separately, the cap reached inside COCO after V1 must give FALSIFIED (B5(d));
17c. the status logic must read the persisted V1 records: a dead run after COCO V1 VIOLATED (no `a_m1_result.json`, `run_record/v1_coco5000.json` = VIOLATED) must give FALSIFIED; a non-atomic V1 write, or a V1 write after V2-A, must be caught (B5(a), (d));
18. the selftest passing with any WP-M or WP-D configuration missing (N10).

## 8. Run conditions, CPU cap and stop rules

### 8.1 Environment

- Laptop only: `OMP_NUM_THREADS=2 OPENBLAS_NUM_THREADS=2 MKL_NUM_THREADS=2 nice -n 15 ~/.venvs/vsps_h1/bin/python -I -B` (`env_guard`).
- No rented host.
- Not concurrent with any C laptop job or heavy /mnt/d I/O (EIO history). The coordinator runs the CC-271r2 idle check before freeze, gate and run, and records it in one OPS line.
- Launch detached, never under `timeout`, on mains power with sleep off.

### 8.2 Cap

- 1 CPU-h or 1 h wall in total for freeze + gate + run, whichever comes first. Budget carries the S0 time and any failed S0 time.
- Estimate: selftest about 10 min (synthetic, outside the cap); freeze under 1 min; gate about 2 min; run about 5 min.
- **Order inside run:** COCO-5000, then UIT-ViIC; within a set: E5 counts, then V1, then the atomic `run_record/v1_<set>.json` write (§7.1), then V2-A and E1–E4 from the shared bootstrap. Nothing that runs after the V1 write can change or hide it (§5.5 rule 1).

### 8.3 Stop rules

- A failed freeze, gate or selftest acceptance stops everything before any φ_j.
- At the cap, the running set and every later set are NOT_RUN. A V1 VIOLATED already persisted for the running set or an earlier set still gives FALSIFIED (§5.5 rule 1).
- Any exception inside a set: that set is FAULT and later sets are NOT_RUN. Labels of a set that completed earlier are kept and enter the §5.5 precedence. Any persisted V1 VIOLATED, including one of the faulting set itself, gives FALSIFIED (rule 1).
- One attempt. A dead run (SIGKILL, EIO, sleep) leaves STARTED.json without a result, and everything is NOT_RUN, except that §5.5 rule 1 takes precedence: if any `run_record/v1_<set>.json` holds VIOLATED, the status is FALSIFIED. A rerun needs a new plan version and a judge read. STARTED.json is never deleted.
- No parameter is changed after any φ_j is computed. No second k, δ or arm is added after the result.

### 8.4 Deadline stop

If no result-read GO is stamped by 2026-11-19T17:00:00Z, A-M1 leaves SPIC. A is submitted as now planned. A-M1 can move to A's next paper only under a new plan version. The run may still complete for the record.

### 8.5 Outputs

- `data/results/a_m1/freeze/freeze.json`
- `data/results/a_m1/gate.json`
- `data/results/a_m1/selftest.json`
- `data/results/a_m1/a_m1_result.json`
- `data/results/a_m1/run_record/` (STARTED.json, v1_coco5000.json, v1_uitviic231.json, stdout, stderr, timing, rc, start/end UTC, HEAD)

### 8.6 Schedule (UTC; planner's estimate)

| Step | Date |
|---|---|
| Plan read | 11-07/08 |
| Commit | 11-08 |
| Code, selftest and mutants | 11-08/09 |
| Code read | 11-09/10 |
| freeze, gate, run | 11-10 |
| Result read | 11-11 |
| S1.M draft and read | 11-12 to 11-15 |

The slack before 11-19T17:00Z covers one extra round per read.

## 9. Prior art, checked 2026-11-07

Verification marks:
- [A]: abstract read today.
- [R]: record only (title, year, venue, DOI) via OpenAlex or Semantic Scholar; content stated from memory and to be read before citing.
- [W3]: in-house prior-art note `.session_backup/2026-10-29/a_x1_devcheck/prior_art_W3.md`, not re-read today.

Statistical sources (cited as textbook, never claimed):

| Work | Mark | Role here |
|---|---|---|
| Chao 1984, Scand. J. Stat., "Nonparametric estimation of the number of classes in a population" (no DOI in OpenAlex, W1558982506) | [R] | Cauchy–Schwarz lower bound, abundance |
| Chao 1987, Biometrics, 10.2307/2531532, "Estimating the population size for capture-recapture data with unequal catchability" | [R] | the incidence/capture–recapture bound behind Lemma 1 |
| Chao & Lee 1992, JASA, 10.1080/01621459.1992.10475194 | [R] | coverage-based estimator (Chao92); not used |
| Colwell & Coddington 1994, Phil. Trans. R. Soc. B, 10.1098/rstb.1994.0091 | [R] | name "Chao2" for incidence data |
| Shen, Chao & Lin 2003, Ecology, 10.1890/0012-9658(2003)084[0798:PTNONS]2.0.CO;2 | [R] | predicting new species (abundance) |
| Chao et al. 2009, Ecology, 10.1890/07-2147.1, "Sufficient sampling for asymptotic minimum species richness estimators" | [R] | "minimum" (lower-bound) reading of Chao1/Chao2 |
| Colwell et al. 2012, J. Plant Ecol., 10.1093/jpe/rtr044 (already cited in paper §4.1, Crossref-verified 2026-10-18) | [R] | sample-based rarefaction and extrapolation |
| Chao et al. 2014, Ecol. Monogr., 10.1890/13-0133.1 (OpenAlex dates it 2013 online) | [R]; abstract verified in CC-285 check 10 | incidence extrapolation (the p50x formula); the abstract says "accurate for both rarefaction and short-range extrapolation". "Up to double" is NOT in the abstract and stays UNVERIFIED (N5, §5.2). The equation was not re-read. |
| Orlitsky, Suresh & Wu 2016, PNAS, 10.1073/pnas.1607774113 | [R] | unseen prediction beyond doubling (abundance) |
| Eriksson 2026, arXiv 2602.08769, "The Unseen Species Problem Revisited" | [A] | Good–Toulmin for small extrapolation, prediction intervals; i.i.d. abundance samples, not incidence |

Closest uses on annotations, data or evaluation:

| Work | Mark | What it does | A-M1 differs |
|---|---|---|---|
| Trushkowsky, Kraska, Franklin & Sarkar 2013, ICDE, 10.1109/icde.2013.6544865 (preprint 1202.2335) | [R] today; [W3] read the preprint | species estimators (Chao92, jackknife) on crowd answer lists to estimate set completeness | per-image incidence over a fixed K of references, pooled over pairs; a label-free extrapolation check and a label-based consistency check on dev; tied to the reference-gold theory of A |
| Luggen, Difallah, Sarasua & Demartini 2019, ISWC, 10.1007/978-3-030-30793-6_26 (arXiv 1909.01109) | [A] | species-estimation class-completeness estimators for Wikidata classes | knowledge-graph classes, not object classes of an image gold; no reference-gold use |
| Chung, Mortensen, Binnig & Kraska 2016, SIGMOD, 10.1145/2882903.2882909 | [A] | unknown unknowns from items shared between data sources | aggregate query results, not annotation gold |
| Chen, Fang, Lin, Vedantam et al. 2015, arXiv 1504.00325, "Microsoft COCO Captions" | [A] for "five independent human generated captions"; [R] for the Mechanical Turk pool | collection protocol (§2.2) | source for the COCO protocol, not prior art |
| Lam, Le, Nguyen & Nguyen 2020, ICCCI, arXiv 2002.00175, "UIT-ViIC" | full text read (§3.1–§3.2) | collection protocol: five writers, a tool showing the others' captions, guideline 7 (§2.2) | source for the UIT-ViIC protocol, not prior art |
| Rossetto, Sarasua & Bernstein 2024, ACM MM, 10.1145/3664647.3681594 | [A] | "visual semantic density" as a proxy for annotation completeness, from a learned estimator | no species estimation; A-M1 needs no learned model and gives a bound |
| Liu Chen 2026, Research Square, 10.21203/rs.3.rs-10639224/v1 | [A] | capture–recapture over 3 reference databases (Lincoln–Petersen, log-linear), then a PU correction of GRN benchmark AUPRC | other domain; databases as captures with explicit dependence terms; A-M1 uses K exchangeable references per image and a k→K check |
| Kansal 2026, Zenodo 10.5281/zenodo.23205993 (record type "software"; not refereed) | [A] | capture–recapture over label-error detectors on MMLU-Redux; NO-GO / PARTIAL | label errors in QA keys, detectors as captures; cite at most as "cf." |
| Ye, Santy, Hwang, Zhang et al. 2025, CVPR, 10.1109/CVPR52734.2025.02762 (arXiv 2310.14356) | [A] | multilingual caption sets name more objects than monolingual ones (XM3600, Visual Genome) | supports the EN vs VI angle; it does not estimate the unnamed |
| Tang et al. 2026, CVPR, arXiv 2602.21655 (CCCaption) | [A] | argues human references are incomplete; builds completeness rewards from model-derived queries | uses models, not an estimator; A-M1 uses references only |
| Berg et al. 2012, CVPR, 10.1109/CVPR.2012.6248100 (cited in paper §4.1) | [R] | importance as the chance an object is named | that is w; A-M1 uses the frequency profile of w to bound the unnamed |
| Zobel 1998, SIGIR, 10.1145/290941.291014 | [W3] | pool-depth extrapolation of relevant-document counts | IR pools, power-law fit |
| In-house X1/X2 (Paper A supplementary, PASCAL-50S; p50x) and the X1 dev check | committed records | Chao2/jackknife extrapolation of per-run mention precision, 5 → 50 references; registered descriptive, no verdict | A-M1's estimand is the completeness of the reference gold itself, independent of any system. It does not reuse X1 numbers; it reuses only the pinned estimator code. It changes no X1/X2 statement. |

Search log (today):
- About 20 Semantic Scholar and OpenAlex queries, including "species richness / Chao2 / capture–recapture / unseen species / Good–Turing" crossed with "caption / annotation / missing annotations / benchmark", plus an OpenAlex 2024–2026 filter.
- Citing-paper scans: Trushkowsky 2013 (123 citing papers), Berg 2012 (167), Rossetto 2024 (2).
- None applies an incidence species estimator to multi-reference caption golds.
- **arXiv API: no feed returned (0 entries, no totalResults), so the arXiv sweep is UNVERIFIED, not "no hits".**
- The citing-paper lists of Chao 1987, Chao et al. 2014 and Colwell et al. 2012 (thousands each) were not scanned.
- One off-topic capture–recapture hit on web-corpus auditing (WaC 2026) is not cited (PI-1101o).
- T5 stays about 3.5 (planner's estimate). A hard reviewer will call A-M1 "an application of Chao2"; the defence is the pooled formulation with its checks on dev, the tie to A's reference-gold theory, and the Vietnamese case.

## 10. What Paper A may print

### 10.1 Placement and companion edits (A writer at transfer; the PI rewrites wording later; the limits stay)

- Placement: a new §5.4 "How much do five references miss?" (main text ≤ 200 words), after §5.3, because it rests on (A1) and on §4.1's Ḡ(k). Lemma 1, Proposition 2, Remark 3 (and Remark 4 only after J7) and the proofs go in a new Supplementary S1.M. Estimates go in an S5 table.
- Companion edits:
  - supplementary.md l.535 and supplementary_SPIC.md l.425, item 3: "Completeness estimators … give within-writer bounds at best on such data; we report none". This stays for single-writer corpora. Append "for COCO-5000 and UIT-ViIC (development data) see Section 5.4" (METHOD or BOUND_ONLY only).
  - main-text sec5_exchangeability.md l.39, "on single-writer data, completeness estimators give within-writer quantities": the same treatment (N6).
  - sec11 limitations: one line, including the five-writer caveat for UIT-ViIC.
  - sec2: Chao 1987, Colwell et al. 2012, Chao et al. 2014, Trushkowsky et al. 2013, Luggen et al. 2019.
  - The X1 distinction sentence (§9).
  - The word cap (8,500, PI-1105k) is recounted at transfer.
  - For the A writer and the PI, outside this plan (N7): sec5_exchangeability.md l.29 calls COCO and UIT-ViIC "the two independent-annotator caption sets with a documented protocol". The UIT-ViIC protocol (five writers, a tool showing the others' captions) does not support "independent" as written. Review it at the next A diff.
  - v1 worded that append "for the two independent-writer development sets"; v2 drops "independent-writer", for the same reason.

### 10.2 Always

- "Development data". "Nameable (image, class) pairs: pairs a reference names with positive probability, in the matched COCO-80 classes."
- **Direction words (B4), each with "asymptotic, under (A1)":**
  - Ŝ: "a lower bound on the number of nameable pairs";
  - Ĉ_k: "an upper bound on the coverage of the k-reference gold" (five references "cover at most" Ĉ_5);
  - m̂_k: "a lower bound on the missing share";
  - E4: "a lower bound on the nameable share of the label shortfall".
  Never "lower bound" for Ĉ, and never "upper bound" for Ŝ or m̂.
- The bound is asymptotic. For UIT-ViIC (n = 231), "approximate at this sample size".
- **Non-blind disclosure (B3(a)), wherever V2-A is printed (main text or S5).** In substance: "k and the tolerance were fixed before any frequency count was computed, but after the authors had seen the mean union sizes on COCO-5000 and an exploratory extrapolation of a related quantity on the same sets. V2-A is a pre-specified development check, not a blind test."
- **ε_3 is never printed alone (B3(b)).** ε_2 and ε_4 (arm U, descriptive, with intervals) are printed beside it.
- **Five-writer caveat (B1(e)), with any UIT-ViIC estimate.** In substance: "The UIT-ViIC references were written by a panel of five writers, so (A1) is a modelling assumption there and is not checked; the bound may fail if writers name different objects." This uses no data-overlap wording and does not say the sets share images.
- **Shared-writer note (N9), in S5 beside any interval.** "Intervals resample images and may be too narrow when the same writers serve many images." 
- Never:
  - "the gold misses X% of the objects" as a fact; "the true number of objects"; "complete" for Ŝ; "human ceiling"; "first";
  - any statement about classes no writer names (Remark 3), or about single-writer corpora;
  - a transfer to PASCAL-50S, X4, X5, A27 or A28, or any change to a registered verdict, or a link to the X5 split (CC-274 A1);
  - a withdrawn value (§0);
  - an AI mention, data-overlap wording, or any statement that the two sets share images.
- EN vs VI: descriptive only (different matchers).
- V1 is printed as "consistent (low power)", never "passed". On COCO-5000 that outcome was foreseeable from aggregates seen before the plan (§1), and the S5 note says so.

### 10.3 Per status (§5.5)

- **METHOD.** §5.4 may say:
  - treating each reference as a sampling occasion, a pooled Chao2-type estimator gives an asymptotic lower bound on nameable pairs under (A1), and so an upper bound on the coverage of the reference gold (Chao 1987; Supplementary S1.M);
  - on development data five references cover at most Ĉ_5 [CI] of them on COCO-5000 (English). UIT-ViIC (Vietnamese) bound estimates are expected in S5 only (§7.2 consequence rule, almost sure to fire), with the five-writer caveat. Only if the rule does not fire may Ĉ_5′ [CI] appear in the main text;
  - separately, and never as support for the bound: in a pre-specified development check (not a blind test; B3(a) disclosure), the same model, fitted on three of five references, predicted the five-reference count within the registered tolerance, with ε_3 [CI] on COCO-5000, printed beside ε_2 [CI] and ε_4 [CI]. For UIT-ViIC, print its label; UNDERPOWERED is printed "not decisive at 231 images";
  - the bound's support is Proposition 2 under (A1): D2 PASS (reference position only), the §5 adjacency diagnostics (file order; COCO), and V1 "consistent (limited power)". On UIT-ViIC, (A1) is a modelling assumption.
  S5 lists V1, V2-A and E1–E4. E4 follows J6.
- **BOUND_ONLY.**
  - S1.M plus an S5 table of Ĉ_5 ("asymptotic upper bound on coverage, under (A1)") and m̂_5 ("asymptotic lower bound on the missing share, under (A1)") (B4). UIT-ViIC rows carry the five-writer caveat and sit in S5 only (§7.2 consequence rule).
  - The V2-A label and ε_3 [CI], with ε_2 [CI] and ε_4 [CI] beside it and the B3(a) disclosure, are printed with the meaning of the label actually obtained (CC-285r2 N-A): FAIL, "the extrapolation is not supported at the registered tolerance"; UNDERPOWERED, "not decisive"; NOT_EVALUABLE, "not evaluable".
  - No extrapolated count, and no Ŝ(k) curve, in the main text.
  - At most one main-text sentence (J4). It carries "asymptotic upper bound on coverage, under (A1)" and gives no extrapolated count.
- **FALSIFIED.**
  - No Ĉ or m̂ is printed as an estimate.
  - One supplementary sentence gives the registered label and its FAIL meaning (§5.5).
  - Item 3 of S5 stays as it is.
- **FAULT / NOT_RUN.** Nothing, unless rule 1 of §5.5 applies, in which case FALSIFIED is printed as above.

## 11. Open items for the judge (each with a recommendation and a default)

- **J1.** k = 3 (CC-285: YES, 86), with the N5 rewording (§5.2) and with ε_2/ε_4 printed beside ε_3 (B3(b)).
- **J2.** δ_A = 0.25: KEEP (CC-285, 86).
- **J3.** The one-sided over-prediction falsifier (V2-O) was dropped before this read (§5.2), because the reused formula tends to the linear Good–Turing form and has no power against singleton-type violations. V1 is the only falsifier of the bound, and its power is reported on graded synthetic worlds (§7.2). CONFIRMED (CC-285, 90).
- **J4.** BOUND_ONLY enters SPIC as S1.M + S5 + at most one main-text sentence: YES (CC-285, 86). The sentence follows B4.
- **J5.** METHOD with UIT-ViIC UNDERPOWERED or NOT_EVALUABLE: YES (CC-285, 85), with the five-writer caveat and the §7.2 consequence rule.
- **J6.** E4: S5 only (CC-285, 86). Never in the main text, never worded "size vs selection", never next to X5, Result 3 or any slope gap. Direction words per B4.
- **J7.** Remark 4 is not printed until the S1.M read (CC-285, 90). The finite-panel caveat is added (§3.5).
- **J8.** Deadline. Recommend 2026-11-19T17:00:00Z (20/11 00:00 VN). Default that.
- **J9.** Gate path: one judge at 85 for the plan, the code and the result, and Codex read-only at the S1.M read (CC-285, 88). Round 2 of this plan read is a FULL read. Whether PI-1107c also licenses the one-attempt dev run is the CC-285 erratum E2 PI question; default YES unless the PI says no before the run.
- **J13.** The §7.2 consequence rule for UIT-ViIC: KEEP (CC-285r2, 86). Extended to every UIT-ViIC bound estimate (Ŝ, Ĉ_k, m̂_k, E4). It is expected to fire almost surely, so UIT-ViIC bound numbers are expected in S5 only.
- **HARD-DUE before print (from CC-285):** N4, the source of the exact (K−1)/K incidence factor, checked in the full text at the S1.M read. N5, the doubling convention: full text read, or the convention is never attributed to the source.
- **J10.** The planner's prior exposure (§1): does it require a stricter rule? Recommend no: k by principle, V1 acceptance on synthetic data only, and full disclosure. Default no.
- **J11.** Depth plan item (c), an X4 sensitivity bound: dropped (§3.3). Recommend drop. Default drop.
- **J12.** Laptop only, cap 1 CPU-h / 1 h wall. Default that.

## 12. Changes against DEPTH_PLAN_2026-11-07 §1.2 (e8e2ab45)

| Item | Depth plan | This plan |
|---|---|---|
| Sets | "three dev sets" in places; COCO-5000 and UIT-ViIC 231 named | COCO-5000 and UIT-ViIC 231 (PI-1107c); XM3600 excluded with reasons (§0) |
| Estimator scale | per image, gate pooled at the set level | pooled over (image, class) pairs; per-image forms not used (§3.3) |
| Claim (a) | "E[Ŝ] ≤ S + o(1)" | Lemma 1 (expectations, exact) and Proposition 2 (asymptotic in n, a.s.); finite-n not claimed |
| Check (a) | "share of images with Ŝ ≤ number of labelled classes" | V1: pooled, one-sided, CONSISTENT/VIOLATED, low power stated |
| Prediction (b) | "95% CI of predicted − observed contains 0, plus a margin" | V2-A (two-sided equivalence band at k = 3, D3 scheme) |
| (c) X4 consequence | sensitivity bound via Result 1 | dropped (unobservable inputs; PASCAL references deleted) |
| ŵ leave-one-out split | optional row | barred (CC-274 addendum A1) |
| Disclosure | — | §1 (r4 U_k, X1 dev check) |

## 13. Item map: CC-285 items → v2 sections

| Item | Fix | Where |
|---|---|---|
| B1(a) | collection protocol per set, with sources; identical distribution across writers named as not tested | §2.2 (A1 row, "Collection protocol per set"), §9 (two source rows) |
| B1(b) | the fixed-panel case with the Newton direction; avoidance through the tool | §3.3 |
| B1(c) | finite-panel caveat: outside Remark 4 | §3.5 |
| B1(d) | two writer-panel worlds, WP-M and WP-D, registered now, with fixed flag and consequence rules | §7.2 |
| B1(e) | mandatory five-writer caveat with any UIT-ViIC estimate | §10.2, §10.3, §10.1 (sec11 line) |
| B2 | precedence FALSIFIED > NOT_RUN/FAULT > METHOD/BOUND_ONLY; mutant 17 | §5.5, §7.3, §8.3, §10.3 |
| B3(a) | "pre-specified development check, not a blind test" disclosure wherever V2-A is printed | §10.2, §10.3 |
| B3(b) | ε_3 always printed beside ε_2 and ε_4 | §5.2, §10.2, §10.3 |
| B4 | direction words: Ĉ is an upper bound on coverage; Ŝ and m̂ are the lower bounds; v1 l.504 fixed | title, §5.4, §10.2, §10.3 (BOUND_ONLY row, METHOD), §11 J4 |
| N1 | D2 cited via CC-274 addendum A1; D2 tests metric scores by position, not writer laws | §2.2 (A1 row) |
| N2 | adjacency figures: 4,867 and 3,842 images (UIT-ViIC all splits) | §2.2 (A1 row) |
| N3 | Proposition 2 proof by uniform continuity, no limit of means assumed | §3.2 |
| N4 | source of the (K−1)/K factor: HARD-DUE at the S1.M read | §11 (HARD-DUE line) |
| N5 | "up to double" → "short-range extrapolation" (verified abstract) plus an unverified convention | §5.2, §9 (Chao 2014 row), §11 |
| N6 | sec5 l.39 added to companion edits | §10.1 |
| N7 | sec5 l.29 "independent-annotator" wording: listed for the A writer and the PI, outside this plan | §10.1 |
| N8 | r4 read for `U.*` keys only | §4 (r4 row and note) |
| N9 | shared writers make image-bootstrap intervals possibly too narrow | §2.2 (A2 row), §3.3, §10.2 |
| N10 | mutant 18: selftest refuses without the WP worlds | §7.2, §7.3 |
| N11 | CC numbering (the S11 read takes the next free number) | not plan text; nothing changed |
| N12 | V1 CONSISTENT on COCO was foreseeable from r4 aggregates | §1, §10.2 |
| Erratum E1 | check_coco_full.py U key at l.79–81 and l.92 | §6 G3 |
| Erratum E2 | PI question on whether PI-1107c licenses the dev run | §11 J9 |

Unchanged from v1 apart from these items: §0, §2.1, §2.3, §2.4, §3.1, §3.4, §6 (except G3's line citation), §7.1, §8 (except §8.3), and §12.

### 13.2 v2 → v3 hunk map (CC-285r2)

| Item | Fix | Where |
|---|---|---|
| B5(a) | each set's V1 label, D_L and interval persisted atomically (temp file, fsync, rename, directory fsync) to `run_record/v1_<set>.json` as soon as V1 is computed, before V2-A | §7.1, §8.2 (order line, v2 l.434), §8.5 |
| B5(b) | rule 1 reworded: a V1 VIOLATED recorded for any set gives FALSIFIED, whether or not that set, the other set or the run later completed | §5.5 (rule 1 and the "completed" note) |
| B5(c) | §8.3 defers to rule 1: the cap line (v2 l.439), the exception line (v2 l.440) and the dead-run line (v2 l.441); a persisted CONSISTENT record of an incomplete set does not make it completed | §8.3, §5.5 |
| B5(d) | mutant 17b (exception after V1; cap after V1) and mutant 17c (dead run after a COCO VIOLATED; the status read from persisted records; non-atomic or late V1 writes caught) | §7.3 |
| N-A | each V2-A label in BOUND_ONLY prints its own meaning | §10.3 (BOUND_ONLY) |
| N-B | "Mechanical Turk" re-marked [R], not in the abstract | §2.2, §9 |
| N-B2 / J13 | the consequence rule extended to Ŝ, Ĉ_k, m̂_k and E4 for UIT-ViIC; stated as almost sure to fire, so UIT-ViIC bound numbers go to S5 only; no judge scratch number copied | §7.2, §10.3, §11 J13 |
| N-C | the integer rule for unnamed labelled pairs fixed now: floor(3s/7 + 1/2) per image, in every synthetic world | §7.2 |
| N-D | gain errors renamed E_k → ε_k; ε_4 beside ε_3 versus E4 (S5 only) resolved | §5.2 (and every ε_k occurrence: §3.3, §10.2, §10.3, §11 J1, §13) |
| N-E | avoidance, forced-singleton and copying worlds now run at n ∈ {231, 5000} | §7.2 |
| header | v3 status, ruling history, next step CC-285r3 | header |

Unchanged from v2 apart from these hunks: §0, §1, §2.1, §2.3, §2.4, §3 (apart from the ε rename), §4, §5.1, §5.3, §5.4, §6, §8.1, §8.4, §8.6, §9 (apart from the Chen et al. row), §10.1, §10.2 (apart from the ε rename), §12.
