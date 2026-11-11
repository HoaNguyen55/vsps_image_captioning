# A2 CPU step plan v1: certify or abstain for paired ΔCHAIR_i / micro-F1 under incomplete reference gold

- **Written:** 2026-11-10T00:50:34Z (`date -u`), which is 07:50 on 2026-11-10 Vietnam time. vsps HEAD `9472f91`, branch `paper-v10`.
- **Authority:**
  - PI-1110e (LOG.md l.2030): one bounded CPU-only dev step for the certify-or-abstain direction, as a **separate paper A2**. Limits: ≤ 4 days, 0 GPU-h. Paper A (SPIC) stays unchanged.
  - PI-1110b (LOG.md l.2027): each paper may **propose** one owned confirmatory set. Nothing in it is opened until an irreversible judge read (≥ 85) and a PI line approve it.
  - ITERATE_A Q-1 (default "run the step; nothing confirmatory").
- **Cycle gate:** gate 2 (plan). This file needs a **one-judge FULL read, REVERSIBLE ≥ 85**, before any code is written.
- **What was done for this file:** nothing was run and nothing was committed. Only this file was written. Inputs were checked only in three ways:
  - by `sha256sum`, `ls` and key-and-type reads of result JSON files;
  - by the reads listed in §9;
  - by the mandated NGRAM scan of this file. The scanner itself reads `dataset_coco.json`, every `uitviic/*.json` (including `test_data.json`) and the ktvic and openviic files, and prints counts only.
- **Status of the content:** AI opinion. Every derivation in §3 is an AI derivation, not yet checked by a judge or Codex. Only the toy numbers in §3.10 were checked, by exact rational arithmetic on the toy values alone.

## Tóm tắt cho PI (tiếng Việt)

- **Câu hỏi của bước này (một câu, có thể sai):** trên tập dev COCO-5000 đã dùng (9 hệ, 36 cặp), với 2 tham chiếu mỗi ảnh, chứng nhận theo cặp có xếp các so sánh theo độ bền tốt hơn luật tầm thường mạnh nhất không?
  - Ba luật tầm thường: hằng số, ngưỡng chênh lệch, độ dài.
  - "Tốt hơn" nghĩa là quyết định an toàn thêm ít nhất 5 điểm phần trăm số so sánh, với sai ≤ 5% so với bậc gold đầy đủ nhất (5 tham chiếu ∪ nhãn instance).
- **Luật dừng (KILL):** dừng hướng A2 nếu xảy ra một trong các điều sau:
  - (K1) điểm vận hành đã cố định sai > 5%;
  - (K2) phần hơn < 0,05, hoặc cận dưới bootstrap theo cặp ≤ 0; hòa cũng tính là KILL;
  - (K3) có < 30 đơn vị bất đồng, hoặc chúng nằm trong < 3 cặp. Khi đó kết quả là UNDERPOWERED và hướng A2 cũng đóng.
- **Dữ liệu:** chỉ COCO-5000 (dev đã tiêu), gồm 9 file output, gold instance đã dẫn xuất và tham chiếu Karpathy.
  - **Mục dừng G0:** file tham chiếu `dataset_coco.json` là file chú thích (caption) COCO. A-M1 đã ghim nó làm dev (2fd99922).
  - Người viết **chưa mở** file này. Coordinator phải quyết trước khi chạy:
    - khuyến nghị: cho phép, vì đây là dev đã tiêu;
    - mặc định nếu chưa có quyết định: **DỪNG**.
  - Không dùng UIT-ViIC, XM3600 hay log OPERA/LiM: log OPERA/LiM không còn trên đĩa.
- **Đề xuất tập xác nhận riêng (A2-OC1, chưa mở):** nhánh method chưa từng tính của 3 log LLaVA-1.5-7B đã công bố: MARINE (A1-01), CCA dài và CCA ngắn (A1-19, A1-20).
  - Đại lượng xác nhận là phán quyết của chứng nhận đã cố định ở bậc 1–2 tham chiếu, và việc phán quyết đó có khớp với gold CHAIR hay không. Không bao giờ là chiều của mức cải thiện, vì Bảng 2 của CCA đã in sẵn mức này.
  - Loại A1-25, A1-26 và A1-21.
  - Cỡ mẫu chỉ có 3 so sánh, nên lực thống kê thấp; điều này được ghi rõ.
- **Chi phí:** 0 GPU-giờ; dưới 1 CPU-giờ trên laptop; khoảng 3–4 ngày công, gồm cả các vòng đọc của judge.

## 0. Scope

- **This step is** tier 1 (dev-explore) of the three-tier rule, on spent COCO-5000 dev data only. Its single purpose is to decide whether A2 is real: GO to a dev-confirm prereg, or close the line (§7).
- **This step is not:**
  - a preregistration of any A2 confirmatory claim;
  - a test look or an owned-set opening;
  - paper text.
- **Excluded from this step:**
  - no Paper A file is touched;
  - no GPU;
  - no UIT-ViIC, XM3600, PASCAL-50S, OPERA or LiM input;
  - no mixed-F1 claim (the coupled sum-of-ratios problem stays open; DR_GAPS_A G1);
  - no moment-LP, minimax or slope certificate (§8).
- **Estimands:**
  - **ΔCHAIR_i** is primary and the only target that enters the kill rule.
  - **Pooled micro-F1** is secondary and reported only.

## 1. Dev question, baselines and kill rule (fixed before any computation)

### 1.1 The one falsifiable dev question

> On the 9 spent COCO-5000 dev systems (36 pairs), at the two-reference rung (k = 2), does the paired coupled-strata floor certificate (§3) rank the 720 pair-draws by robustness better than the best of three trivial baselines? Concretely:
> - does it decide safely (top-rung error ≤ 5%) a share of pair-draws at least 0.05 larger than the constant, margin or length rule, with a pair-cluster bootstrap lower bound above 0;
> - and does its cross-fitted operating point keep its own top-rung error ≤ 5%?

### 1.2 Units and targets

- **Rungs**, per image i:
  - references R_i1..R_i5 are the first 5 Karpathy sentences, as in `score_g2b.coco_context` and A-M1;
  - the k-rung for draw r is G_i^(k,r), the union of the English class sets (CHAIR synonyms) of k references drawn uniformly without replacement;
  - the top rung is G_i^top, the union of all 5 references' class sets and the instance classes.
  - Following DR_GAPS_A §3.3, the top rung is "instance-label-visible", not complete.
- **Mentions:** M_i^s are the COCO-80 classes in system s's caption, from the Vietnamese lexicon matcher (`score_g2b.MATCH['coco80']['vi']`), exactly as in A's COCO-5000 family.
- **Unit:** u = (system pair, draw r) at rung k.
  - **Primary:** k = 2, the full 5,000 images, R = 20 draws, so 36 × 20 = **720 units**, clustered by the 36 pairs.
  - **Orientation:** A is the system with the lower CHAIR_i at rung (k, r) and B the other.
  - **Ties at the rung:** the unit is ABSTAIN for every rule and is placed last in every ranking.
- **Outcome:** a unit is **wrong** if CHAIR_i^top(A) ≥ CHAIR_i^top(B). Ties at the top rung count as wrong.

### 1.3 Baselines (named by the critics; ITERATE_A §3.1 item 2, §4.2 item 1)

| Id | Rule | Pairwise form used in the kill rule | Ranking score |
|---|---|---|---|
| B1 | constant | "The observed k-rung ordering always holds": certify every unit. Its slope form, "label-rung slope > 0", is §1.7 | none: random order, so Cov@5% = 1 if the top-rung flip share ≤ 0.05, else 0 |
| B2 | margin | Certify iff \|ΔCHAIR_i^(k)\| is large | \|ΔCHAIR_i^(k)\|, descending |
| B3 | length | Certify iff the observed-better system is the more verbose one | ℓ = ln(n_A / n_B), descending; ties broken by \|Δ\| |
| C | certificate | §3: certify iff w* ≤ w_0 | break-down floor w*, ascending; NI last; ties broken by \|Δ\| descending, then pair id |

n_X is the total number of mentions of X on the image set.

### 1.4 Statistics

- **Cov@5%(score).** Sort the units by the score. Cov@5% is max{m/N : the top m units contain ≤ 0.05·m wrong units}. This reads each rule's whole ranking at a matched risk of 5%, without tuning a threshold.
- **Primary contrast:** Δ_cov = Cov@5%(C) − max{Cov@5%(B1), Cov@5%(B2), Cov@5%(B3)}. It is computed on the 720 units at k = 2.
- **Bootstrap:**
  - resample the 36 pairs with replacement (B = 2,000, seed 20261113), keeping all 20 draws of each resampled pair;
  - recompute every Cov@5% in each replicate;
  - LB = the 5th percentile of Δ_cov.
- **Operating-point validity (cross-fit):**
  - split the 5,000 ids into two halves (seeded shuffle, seed 20261111);
  - on each half h, calibrate w_0 on the other half (§3.8);
  - certify the units of half h, where 36 × 20 = 720 per half, so 1,440 half-units;
  - pool the results: N_c = the number certified, W_C = the number certified and wrong.
- **Matched-coverage readout** (reported; it enters only K1b): at each half's N_c, take the top N_c units of B2 and B3. W_B2 and W_B3 are their wrong counts, and W_B1 = N_c × the half's flip share.
- **Discordance:** the number of units inside exactly one of the two 5%-risk prefixes, C's or that of the best baseline, together with the number of distinct pairs they come from.

### 1.5 Kill rule (KILL closes the A2 line; §7)

- **K0, code gate (not science):** selftest, toy (§3.10), brute force and mutants all PASS, and every pin matches. Otherwise there is no run, and the code goes back to the code read.
- **K1, validity:**
  - (0) N_c(V-B) < 0.05 × 1,440 = 72 certified half-units → **KILL**: the certificate is not usable at its own operating point. If N_c(V-H) = 0, K1 for V-H is a vacuous PASS, because V-H is sensitivity only;
  - (a) W_C / N_c > 0.05 for the primary V-B budgets, or for the V-H sensitivity budgets when N_c(V-H) > 0 → **KILL**;
  - (b) at matched coverage the best baseline makes fewer wrong certifications than C (min W_B < W_C) → **KILL**.
- **K2, beats the trivial baselines:**
  - Δ_cov < 0.05 → **KILL**;
  - LB ≤ 0 → **KILL**;
  - ties (Δ_cov ≤ 0) → **KILL**.
- **K3, power:** fewer than 30 discordant units, or discordant units from fewer than 3 distinct pairs → **UNDERPOWERED**. The line closes; this is not a pass.
- **No target moving.** k = 2 is the only kill rung. A pass at k = 1, 3 or 5, on 500-image blocks or on micro-F1 never replaces a k = 2 failure.

### 1.6 Numbers already seen on these data (disclosed; why K2 is not pre-answered)

**From the impact-r2-1 dry calc** (`/tmp/prop_r2/dry*.py`; AI scratch, unreviewed, not writer-checked; global or stratum budgets at fixed w = 0.2, never cross-fitted):
- certified shares:
  - 10/36 at k = 5 and 0/720 at k = 2 with the global floor;
  - 69% / 55% / 31% at k = 5 / 3 / 2 with stratum budgets;
- sign changes and certified errors:
  - k = 2: 172/720 sign changes, 0/222 certified wrong;
  - k = 5: 5/36 changes, 0/25 certified wrong;
- strata over budget: 39/72 at k = 5 and 263/1,440 at k = 2;
- in the 500-image regime: 61% certified at k = 5, 56/322 among small-gap pairs, and 0/335 small-gap pairs certified at k = 2.

**From the writer checks** (ITERATE_A §3.2, on `coco2500_per_system.json`, mixed F1, 5 refs → instances):
- 15/36 and 6/36 flips;
- margin AUC 0.933;
- the length rule flags 6/6 flips with 1 false flag.

**From `a1_system_robustness.json`:** the label-rung slope is > 0 in 9/9 families.

**Reading:**
- K1(a) may be near-known from the 0/222 count. **K1 alone can therefore never justify GO.**
- K2 is the decisive test. It has never been computed: no one has compared risk-matched coverage of the C, B2 and B3 rankings for ΔCHAIR_i at k = 2 against the top rung. The 0.933 AUC was for mixed-F1 flips at a different rung. So K2 can fail (B2 or B3 may rank as well as C) and can pass (C uses the stratum singleton counts, which B2 and B3 do not see).

### 1.7 Slope target (descriptive only, outside the kill rule)

- The constant "label-rung slope > 0" is right in 9/9 families, so no certificate can beat it on sign accuracy.
- The step reports only the observed sign of the across-system OLS slope of CHAIR_i on ln n, at each rung and each draw, beside the constant's prediction. The verdict "slope certification not shown" is fixed in advance.
- A's registered mixed-F1 slope is not addressed.

## 2. Data

### 2.1 Inputs (all spent COCO-5000 dev; sha256 checked on disk by this writer before 2026-11-10T00:50:34Z unless marked)

The code pins the **full import closure**, as A-M1 PINS do: `rescap/*`, `scripts/xm3600_oiv7.py`, `scripts/pascal50s/p50*.py`, plus the files below. Pinned shas are read from disk at freeze.

| Role | Path | sha256 |
|---|---|---|
| system distill-detailed | `data/results/coco5000/distill-detailed.shard0of1.jsonl` | `6453bfd5a2f7667d0cc879d3e4ca359553b9bda994760d227785da141ec001fd` |
| system distill-short | `data/results/coco5000/distill-short.shard0of1.jsonl` | `12ab5a6e2b707068a48f2247832bcd125559a291ea8f265946e9031d3ccef1b0` |
| system zeroshot-detailed | `data/results/coco5000/zeroshot-detailed.shard0of1.jsonl` | `96e15f40cead64a993ff01ba2392857b1dae16155661ffddd7f2bac3af54365a` |
| system zeroshot-short | `data/results/coco5000/zeroshot-short.shard0of1.jsonl` | `15ca56156796605c02397d13c60047bc6260d34ac65b8cc54f7651d71717feba` |
| system fuse2_s42-detailed | `data/results/coco_transfer_full5000/fuse2_s42-detailed.shard0of1.jsonl` | `f205805a7ab12cbd93c9ef6e240772fff7ac237e559cae57916b6191c85ce257` |
| system fuse2_s42-short | `data/results/coco_transfer_full5000/fuse2_s42-short.shard0of1.jsonl` | `cd947944d3cf578bbffdc40ca9ae920f9595511e9ee395f06585bcd1db6fbd2f` |
| system p1_s43-detailed | `data/results/coco_transfer_full5000/p1_s43-detailed.shard0of1.jsonl` | `b12fbeb91e9023c2872db3b03724e7b9ecdfe264b1bb0a3928fb5e4028d1befd` |
| system p1_s43-short | `data/results/coco_transfer_full5000/p1_s43-short.shard0of1.jsonl` | `b0dbbdc50af75a77fa3da2808018faf0b7c26b52db3a86fbdf333da601cfbb24` |
| system zeroshot-detailed+vcd | `data/results/coco5000_vcd/zeroshot-detailed.shard0of1.jsonl` | `d6173e34823383202298ea7dc00afdd92604277a70bff5a9f1d93e1173396bbd` |
| image ids (5,000) | `data/results/a_dchecks/freeze/coco5000_ids.txt` | `d20da3dd48646d91a7ff7837c1c1f591d52c75e72921b2fd7f6854dc1093339f` |
| manifest (Karpathy test, 5,000) | `data/coco_probe/manifest_full5000.json` | `699769100c572675dfc4ae9f2a45f01bf387c4b1d67e9019feafc8c14fc88f7e` |
| instance gold (derived class sets) | `data/results/a_dchecks/freeze/instance_gold_full5000.json` (the same bytes as `.session_backup/2026-10-26/a_full5000/instance_gold_full5000.json`) | `bd36295146e505454f5110e817841d8300a024265c1f2cba2aade854119183f7` |
| EN synonyms | `data/coco_probe/chair_synonyms.txt` | `b685537b36fe21b791c87151b96a991ceb582edff19f3da204dcc7a7905502f2` |
| VI lexicon | `data/coco_probe/coco80_vi.json` | `926e08571ef6e80a7f8aae8f2b73753d6c5c54c431a750ba2b67bfaae71b540b` |
| matcher code | `scripts/g2b/score_g2b.py`; `scripts/score_coco_probe.py` | `66c665c7a71d3b97abbf89fd5bf13871910449ad1c053ff5fb0b18663e3e7ae5`; `d11db7e192f689980bb2b2bb717d852d9aa339ad857ce9411fe7bdd6fe416070` |
| **references (G0, §2.3)** | `data/datasets/karpathy/dataset_coco.json` (137.5 MB) | **not hashed by this writer; read only by the mandated NGRAM scanner (counts only)**; pin `2fd999220673258012acfb411a4e7e66af7d488050b2519b0badcc49b7600b8d`, from `scripts/a_m1/a_m1.py` PINS (fa8c9bf2) and `data/results/a_m1/freeze/freeze.json` (7ea4bfa0) |

**Registration of the output shas:**
- The five coco5000 / vcd shas equal the `input` rows of `.session_backup/2026-10-26/a_full5000/SHA256SUMS` (71003c83).
- The four full5000 transfer shas appear in `.session_backup/2026-10-13/decisions/CP-117a.txt` (d2ddc22e).

**Read-only background, not step inputs:**

| File | sha256 |
|---|---|
| `data/results/a1_robustness/a1_system_robustness.json` | `af77ffa0f82b79560de6fa2118b186758b9a7bca8c098525ffab635aabe081f7` |
| `data/results/a1_robustness/coco2500_per_system.json` | `735ad31d5a0463e0b6d41febc6eeeac3b63f151edb0710351aaf1ca6bd0f7869` |
| `.session_backup/2026-10-26/a_full5000/out/r4_full5000_all9.json` | `332da8b6264c9c05232e5ef70cd864a0fe7ce58480e99aee558b1115a5c793af` |
| `.session_backup/2026-10-14/r12/H3/out/n1_results.json` | `b82053f9aad5773dc581439551acf8f16134ed82dc67b98b36bfa946d81a4ce1` |
| `.session_backup/2026-10-27/a1_precheck/precheck.json` | `fa459a4259a5fe27f3eff023e9c9b8dc65a5c2294c09238406dda273a55c81c6` |

### 2.2 Files this step never opens

| File or class | Why |
|---|---|
| `data/datasets/coco_probe/annotations/instances_val2014.json` (SUMS row e1b4d1bc), `annotations_trainval2014.zip`, any `annotations/captions_*` or `instances_*` | Raw COCO annotations, barred. The instance rung comes only from the derived `instance_gold_full5000.json`, which `.session_backup/2026-10-26/a_full5000/eval/build_instance_gold_full5000.py` (dc0d1f52) built earlier. The build is not re-run |
| `data/datasets/uitviic/test_data.json` | Test-set annotation file by name, barred. UIT-ViIC stays out of this step, although A-M1 pinned it |
| `data/xm3600*`, `datasets/xm3600*`, `oiv7_labels`, XM3600 full_data | Barred |
| `~/.vsps_sealed`, `t2pool_*` | Barred. Not listed, not stat'ed |
| `.session_backup/2026-10-27/a1_precheck/raw/**` (all released CHAIR logs on disk) | **Reserved** for A2-OC1 (§5). Method arms are never computed; no log file is read in this step |
| `.session_backup/2026-10-14/r12/H3/out/gt_cache.json` (f986f8ff; derived reference and instance class sets for 1,478 val2014 ids) | Reserved as possible OC1 gold. This writer read its key structure (two keys; per-id lists of class-name lists) and, through an over-long structure dump, printed its image ids. No class content was printed |
| OPERA (shikiw/OPERA@e1bb763) and LiM (yuezih/less-is-more@f26e187) family logs | **Not on disk.** The H3/E1 download scratch was in an expired `/tmp`. No sha exists to verify a re-fetch against, so they are left out (default). A pinned re-fetch would be its own logged step and would be descriptive only |
| `/tmp/prop_r2/dry*.py` | Unreviewed AI scratch, and its F1 allocation is greedy, not exact. Not reused (§3.11) |

### 2.3 G0, the stop item: is `dataset_coco.json` a barred "COCO annotation"?

- **Facts.**
  - The COCO-5000 k-rungs need per-reference class sets. The only on-disk source is `data/datasets/karpathy/dataset_coco.json`, the Karpathy split. It contains COCO caption references.
  - No derived per-reference cache for these 5,000 ids exists. A search of `data/` and `.session_backup/` for reference-set or ladder caches found none.
  - The file was a pinned dev input of registered steps:
    - A-M1 (A_M1_PLAN_v3 12d6ad3d, CC-285r3 GO 87; CC-287r3 code read);
    - Paper C P4 (OPS-1106c-p4-draft, DEMO_PIN 2fd99922).
  - The gatekeeper NGRAM scanner reads it on every check (counts only).
- **The brief's rule** says: never open COCO annotations; if a needed file is one, stop and say so.
- **Stop condition (binding).** If the coordinator classes this file as barred, **this step STOPS before any code runs.** There is no substitute source and no partial run. The line stays paused, A is unchanged, and an OPS line records the stop.
- **Recommendation:** classify it as spent dev reference data, not as a barred raw annotation file. Reasons:
  - COCO-5000 is the Karpathy test split already spent as Paper A dev;
  - A-M1 registered and pinned this exact sha.
  - The file is read once, and only class sets are cached in scratch (§4). No caption text is written anywhere.
- **Default if no answer:** STOP. The file is not opened.

### 2.4 Why A2 may read paths that A-M1's DENY list refused

- A-M1 DENY refused `/results/coco5000` and `coco_transfer` because A-M1's estimand used only references and gold.
- These 9 output files are spent COCO-5000 dev outputs of Paper A's own family:
  - their shas are registered in the a_full5000 SHA256SUMS and CP-117a;
  - Paper A's dev runs read them (`r4_full5000_all9.json`);
  - so did the impact-r2-1 dry calc.
- Reading them opens no new set.

## 3. Certificate math

### 3.1 Setting

- **Objects:** images i = 1..N; vocabulary V (COCO-80); true object sets T_i (unknown); observed gold G_i at rung k.
- **Fixed outputs:** two systems, A (observed-better at rung k) and B, with mention sets M_i^A and M_i^B.
- **Output-fixed cells** per image:
  - A-only: O_i^A = M_i^A \ M_i^B;
  - B-only: O_i^B = M_i^B \ M_i^A;
  - both: O_i^S = M_i^A ∩ M_i^B;
  - neither: O_i^Z = V \ (M_i^A ∪ M_i^B).
- **Per-cell totals** (S ∈ {A, B, S, Z}, pooled over images):
  - U(S) = Σ_i |O_i^S \ G_i|, the ungolded pairs;
  - f1(S) = the number of pairs in O^S named by **exactly one** of the k drawn references;
  - x(S) = the number of ungolded pairs in S that are true. This is the unknown completion.
- **Pooled counts:**
  - n_X = Σ_i |M_i^X|;
  - Ĥ_X = Σ_i |M_i^X \ G_i|;
  - t_X = n_X − Ĥ_X;
  - g = Σ_i |G_i|.
- **CHAIR_i:** CHAIR_i(X) = (Ĥ_X − completion of X's ungolded mentions) / n_X.

### 3.2 Assumptions (stated; each is a reviewer target)

- **A0, one-sided gold:** G_i ⊆ T_i. Every reference-named class, after the synonym matcher, is a true object.
  - Matcher ghosts and non-assertive mentions (2610.23610) violate A0. Not modelled.
- **A1, exchangeable references:**
  - given the image, each of the k references names each true pair (i, c) independently, with probability p_ic;
  - the system outputs are fixed functions of the image.
- **A1+, pair independence** (used only by the V-B budget): naming events of distinct pairs are independent given the image. V-H drops it.
- **A2, floor:** p_ic ≥ w for every true pair in the cells the adversary uses. This is a floor on **mentioned** true objects only, inside output-fixed strata. It is not a floor on all true objects.
- **A3:** images are independent.

### 3.3 Bound direction (DR_GAPS_A §3.0)

- Paper A's Prop. 2 (Chao2) is an upper bound on coverage, which makes it a **lower** bound on missing pairs. It can never certify.
- An upper bound on x(S) needs one of two things:
  - **(i) no assumption:** the cap U(S). For Z this is the vocabulary cap, 80·N − g − (mentioned ungolded pairs);
  - **(ii) the explicit floor A2.**
- Without (ii), the identified upper end is the cap (Link 2003; Mao and Lindsay 2007; Anthony and Nobari 2607.21480, Prop. 3).

### 3.4 Floor budget (Lemma B; AI derivation)

- **Setup:** for a true pair with naming probability p and k references, the count of references naming it is N ~ Bin(k, p). Then:
  - P(N = 0) = (1−p)^k;
  - P(N = 1) = kp(1−p)^(k−1);
  - their ratio is (1−p)/(kp).
- **Lemma B.** For p ≥ w the ratio is ≤ c(w, k) = (1−w)/(kw), so summing termwise over the true pairs of a fixed cell S gives

  E[x(S)] = E[f0(S)] ≤ c(w, k) · E[f1(S)].

- **Sharpness:** equality holds iff every p = w (a point mass at the floor). This is the upper-bound dual of Chao's lower bound.
- **Coverage:** the result covers floor gold only. Sub-floor true mass is unbounded.

### 3.5 Finite-sample budgets

**Per-pair variable.** For each true pair j in S, let Y_j = 1{N_j = 0} − c·1{N_j = 1}. Then:
- Y_j ∈ [−c, 1];
- E Y_j ≤ 0 under A2;
- Var Y_j ≤ c(1+c)·P(N_j = 1);
- Σ_j Y_j = x(S) − c·f1(S).

**V-B (primary; A0–A3 with A1+; Bernstein).** Let L = ln(2/α_S), and let f1⁺ = f1 + L + √(L² + 2L·f1) be an upper (1 − α_S/2) bound on E f1. Then

β_B(S; w) = c·f1 + (1+c)L/3 + √( ((1+c)L/3)² + 2·c(1+c)·f1⁺·L ),

and P(x(S) > β_B) ≤ α_S.

**V-H (sensitivity; A0–A3 without A1+; image-level Hoeffding).** Image sums lie in [−c·|O_i^S|, |O_i^S|], so

β_H(S; w) = c·f1 + (1+c)·√( ½ · Σ_i |O_i^S|² · ln(1/α_S) ).

**Caps and per-verdict error:**
- the cap used is X(S) = min(U(S), ⌊β(S; w)⌋);
- the per-verdict error is α = 0.05, split over the cells the adversary uses:
  - CHAIR_i uses B and S, so α_S = 0.025;
  - micro-F1 uses B, S and Z, so α_S = 0.05/3.

### 3.6 Paired certificate for ΔCHAIR_i (closed form; exact relative to the box)

**Worst case.** Δ(x) = CHAIR_A − CHAIR_B = (Ĥ_A − x_A − x_S)/n_A − (Ĥ_B − x_B − x_S)/n_B, over the box R_w = {0 ≤ x(S) ≤ X(S)}. The maximum is at x_A = 0, x_B = X(B), x_S = X(S)·1[n_A > n_B]:

Δ_max(w) = Ĥ_A/n_A − (Ĥ_B − X(B))/n_B + max(0, 1/n_B − 1/n_A) · X(S).

**Verdict.** CERTIFIED(w) iff Δ_max(w) < 0.

**Sharpness (Prop. S, AI).** Δ_max is attained by a feasible vertex, so the verdict is exact (sharp) for R_w. R_w is a confidence box built from the per-cell singleton counts only. The profile LP over mixing measures, which also uses f2..fk, could shrink it; that LP is out of this step (§8).

**Coupling gain.** Separate per-system intervals certify iff Ĥ_A/n_A < (Ĥ_B − X(B) − X(S))/n_B. The paired certificate is never weaker than that, and its worst case is smaller by exactly

X(S) / max(n_A, n_B),

the shared true objects that separate intervals count for B only.

**No-assumption case** (DR_GAPS_A G1(iii)). With X = U (w → 0) and n_A ≤ n_B, certified iff U(B) < b* = Ĥ_B − n_B·Ĥ_A/n_A.

### 3.7 Paired certificate for pooled micro-F1 (exact; secondary)

**Sign.** sign(F1_A − F1_B) = sign N, with

N(a, b, s, z) = (t_A + a + s)(n_B + g + a + b + s + z) − (t_B + b + s)(n_A + g + a + b + s + z).

Its non-linear part is +a² − b² + as + az − bs − bz (writer-checked in DR_GAPS_A §1).

**Exact minimum** over the box:
- ∂N/∂a = (n_B + g + t_A − t_B) + 2a + s + z > 0, so a = 0;
- for fixed (a, b), N is linear in (s, z), so s and z sit at endpoints;
- for fixed (a, s, z), N is concave in b, so b sits at an endpoint.
- The minimum is therefore over the 8 vertices b ∈ {0, X(B)}, s ∈ {0, X(S)}, z ∈ {0, X(Z)} with a = 0.

**Verdict.** CERTIFIED iff min N > 0.

### 3.8 Break-down floor w* and operating floor w_0

**w\*.** β is decreasing in w, so Δ_max(w) (and min N) is monotone, and the certified set is an up-set in w:
- w* = inf{w : CERTIFIED(w)}, found by bisection on [10⁻³, 1] in 30 steps;
- w* = 0 if the unit is certified at the caps U (no assumption);
- w* = NI if it is not certified at w = 1.
- C's ranking score is w*.

**w_0, cross-fitted, frozen per half before evaluation.** On the calibration half, at k = 2, take each stratum (unit × cell ∈ {B, S}). Let x_top(S) = Σ_i |(O_i^S \ G_i^(k)) ∩ G_i^top|. Then:
- exceed(w) = the share of strata with x_top(S) > ⌊β(S; w)⌋;
- w_0 = max{w ∈ {0.01, 0.02, …, 0.99} : exceed(w) ≤ α_S}. This is monotone in w;
- if no w qualifies, w_0 = 0, and only no-assumption certificates count;
- w_0 is calibrated **separately** for V-B and V-H, each with its own β in exceed(w). It is never carried over from one variant to the other.

**Transport check (reported):** exceed(w_0) at k = 1 and k = 3, with w_0 calibrated at k = 2.

### 3.9 What the certificate does not guarantee

- It covers only true mass above the floor in the cells used. The dev calibration tests adequacy only for the top-rung step, x_top ≤ true x, so w_0 is optimistic relative to truth.
- It covers fixed outputs. It says nothing about a method's re-run.
- It covers CHAIR_i and pooled micro-F1. Mixed F1, CHAIR_s and slopes are not covered.
- Ghost mentions (A0 violations) are not covered.
- Qwen-on-COCO dev calibration does not transport to other systems or images without a check (§5, risk 5).

### 3.10 Toy self-check (exact; expected outputs are hard-coded in the selftest)

Budgets here use slack 0 (expectation level) with k = 2, so every number can be checked by hand.

**T1 (the DR_GAPS_A §3.0 example):**
- A: n_A = 4, t_A = 3, one A-only ungolded mention (U(A) = 1).
- B: n_B = 12, t_B = 5, seven B-only ungolded mentions (U(B) = 7).
- |G| = 5: 3 pairs are named by both systems and 2 by B only. U(S) = 0, f1(B) = 2, f1(Z) = 0.

| Check | Expected |
|---|---|
| CHAIR_i at the rung | A 1/4 = 0.2500; B 7/12 = 0.5833 |
| b* | 7 − 12·(1/4) = **4** (tie at x_B = 4) |
| No-assumption CHAIR_i verdict | NOT IDENTIFIED (U(B) = 7 ≥ 4) |
| CHAIR_i w* (cap ⌊2c⌋ must be ≤ 3, so c < 2) | **0.2**: certified for every w > 0.2; at w = 0.2 the cap is 4, a tie |
| micro-F1 at the rung | A 6/9 = 0.6667; B 10/17 = 0.5882; Δ = +4/51 = +0.0784 |
| Neither-stratum flip, no floor | z* = **3**: N = 6 − 2z; 6/(9+z) = 10/(17+z) at z = 3 |
| One B-only addition | flips: N(0,1,0,0) = −6; F1 A 0.600 vs B 0.667 |
| One A-only addition | N(1,0,0,0) = 22 (helps A, so the adversary sets a = 0) |
| micro-F1 w* (needs ⌊2c⌋ = 0, so c < 1/2) | **0.5** |

**T2 (coupling):**
- A: n_A = 10, Ĥ_A = 3 (U(A) = 2, plus 1 shared).
- B: n_B = 20, Ĥ_B = 7 (U(B) = 6, plus the same shared pair, so U(S) = 1).
- f1(B) = 2, f1(S) = 3, k = 2, w = 0.6, so c = 1/3, X(B) = ⌊2/3⌋ = 0 and X(S) = ⌊1⌋ = 1.

| Check | Expected |
|---|---|
| Paired Δ_max | 3/10 − 7/20 + max(0, 1/20 − 1/10)·1 = **−0.05**, so CERTIFIED |
| Separate intervals | max CHAIR_A 0.30 vs min CHAIR_B (7 − 0 − 1)/20 = 0.30, so NOT certified |
| Coupling gain | X(S)/max(n) = 1/20 = 0.05 |
| Brute force over x_A ∈ {0,1,2}, x_S ∈ {0,1} | max Δ = −0.05 at (0, 0) |
| No assumption (X(B) = 6) | Δ_max = +0.25, so NOT IDENTIFIED |
| w* paired vs separate | 0.5 vs 0.6 |
| Margin and length rules | \|Δ\| = 0.05; length rule ABSTAINS, because A is the terser system. This is a C-vs-B3 disagreement case |

### 3.11 Code checks (gate 3; K0)

- **New code only:** `scripts/a2/a2_cpu.py`, `scripts/a2/a2_cpu_mutants.py` and `scripts/a2/SHA256SUMS`. Matchers are imported unchanged from `score_g2b` and `score_coco_probe` (pinned shas). Nothing from `/tmp/prop_r2` is reused.
- **Selftest:**
  - (i) T1 and T2 exact, using `fractions.Fraction`;
  - (ii) closed forms equal exhaustive enumeration of all integer completions in the box on ≥ 300 random small instances, for CHAIR_i and micro-F1 separately;
  - (iii) monotonicity of Δ_max in w on the same instances;
  - (iv) a size simulation (2,000 replicates, point mass p = w and two Beta mixtures on [w, 1]): P(x(S) > β_B) ≤ α_S + 2 MC SE.
- Check (iv) is a code check, not evidence for A2 (the critics called it circular).
- **Mutants**, each of which must be caught:
  - drop the coupling (use separate intervals);
  - flip the shared-cell sign condition;
  - use c = (1−w)/w (k ignored);
  - use a greedy F1 allocation;
  - count top-rung ties as right;
  - leak the evaluation half into w_0;
  - rank B2 ascending.
- **Custody guard,** in the style of A-M1 `_allowed`:
  - exact pins only;
  - DENY = A-M1's list minus `/results/coco5000` and `coco_transfer`, plus `uitviic`, `annotations/instances_`, `annotations/captions_`, `annotations_trainval`, `val2017`, `a1_precheck/raw`, `r12/H3/out/gt_cache`.

## 4. Procedure and CPU budget (4-vCPU / 20 GB laptop)

1. **G0 ruling and plan read.** The one-judge FULL read must be GO before any code.
2. **Code** (`scripts/a2/`), then selftest and mutants, then a one-judge code read, then the gatekeeper commit of the code.
3. **Freeze:** `data/results/a2_cpu_step/freeze/freeze.json` holds the pins, seeds, grids, α, B and R. It is committed before the run.
4. **Run:** `nice -n 19 env OMP_NUM_THREADS=1 python3 -I -B scripts/a2/a2_cpu.py run`.
   - **One read pass** from /mnt/d: about 11 MB of outputs, 0.36 MB of gold and the 137.5 MB reference file (only if G0 allows).
   - The run writes class sets only to `/home/hoanguyen/.claude/jobs/638bac1e/tmp/a2/cache/`, with no caption text, and computes everything from there.
   - No other heavy /mnt/d job runs at the same time (the EIO rule).
5. **Caps:** CPU ≤ 3,600 s and wall ≤ 3,600 s (as A-M1), RAM ≤ 4 GB. The expected run is under 15 CPU-min:
   - mention extraction 9 × 5,000;
   - 720 units × 4 rungs;
   - bisection;
   - 2,000 pair-cluster replicates.
6. **Seeds:**
   - base 20261110;
   - halves 20261111;
   - blocks 20261112;
   - bootstrap 20261113;
   - reference draws 20261110 + 100·k.
7. **Secondary readouts** (fixed now; no verdict):
   - k = 1, 3, 5;
   - 10 disjoint 500-image blocks, which mirror OC1's size, reported beside the full-5,000 result;
   - micro-F1, with the same statistics;
   - V-H;
   - no-assumption share;
   - coupling gain (units certified paired but not separately);
   - w_0 transport;
   - the slope table (§1.7);
   - a margin-within-length baseline: rank by length class (n_A ≥ n_B first), then by |Δ|. It is reported as a Cov@5% row beside K2 and never replaces K2. If it reaches or beats C, this is printed as "C does not beat the known verbosity direction".
8. **Result read:** labels are recomputed read-only from the result JSON, then a one-judge read, then the result commit. The scratch cache is deleted after the result read.

**Time:** about 3–4 days in all.
- day 1: plan read and G0;
- days 1–2: code and code read;
- day 3: freeze, run and result read;
- day 4: buffer for one NEXT_ROUND and the closing lines.

GPU: 0 h.

## 5. Owned confirmatory set proposal (PI-1110b): A2-OC1 (proposed only, NOT opened)

**Name.** A2-OC1, "never-computed method arms of three released LLaVA-1.5-7B CHAIR logs".

**Units.** All three are pinned in `precheck.json` (fa459a42) and kept at `.session_backup/2026-10-27/a1_precheck/raw/`; none was opened or hashed by this writer.

| Id | Method arm (sha256) | Baseline arm (sha256) | Licence (K17 §0.1, gh API) | Shared ids |
|---|---|---|---|---|
| A1-01 MARINE | γ = 0.7: `093f25a1fc8bbf289a461098f2d06ebdbc545af6cf8805b3af7c3c3e07b33bd7` | γ = 0.0: `83ee234cdb92c9945145e8848ec4412a26a4e5ea17a9ce2ec696a36b4944b8e1` | **none recorded, so UNVERIFIED for reuse.** Derived counts only, no redistribution; PI to decide | 500 |
| A1-19 CCA long | `20da252fccd5d77bf8ea075f490a7dd0ee3d7a2c50ed9c6127ec8f90c544b534` | `48373a1421637e532cb266ccfdb3a2c88af1cc06cb639d74df560e523b009def` | Apache-2.0 | 499 with instance gold |
| A1-20 CCA short | `13c4f7b5c61f7b9603f2a197fe950f406608f0963e63058b5adf8aa352e5fe58` | `02dfb28f07364732227b805484392db283be6efde5725c11c984dac4ab32973a` | Apache-2.0 | 499 with instance gold |

**Why it is owned and never computed:**
- No method-arm CHAIR, mention set or certificate has ever been computed by any VSPS step.
- precheck read only ids, record counts and schema of the method arms, and recomputed **baseline** CHAIR only.

**Confirmatory quantity.**
- **Inputs, all frozen on COCO-5000 dev before opening:** code, w_0, α, R and the seeds.
- **For each comparison and k ∈ {1, 2}:** the certificate's reference-rung verdict over R = 20 seeded draws (CERTIFIED / ABSTAIN / NI), plus w*.
- **Registered pass rule:**
  - no CERTIFIED verdict disagrees with the CHAIR-gold verdict;
  - the share certified is reported.
- **Never the gain direction.** CCA's Table 2 prints both arms' CHAIR (long 46.2/12.9 → 43.0/11.5; short 21.0/6.2 → 18.2/5.4, per ITERATE critic 1; not writer-checked). The MARINE table prints its gain too.
- **Power, stated honestly:** n = 3 comparisons, two from one paper. A PASS is weak evidence; one certified disagreement is a clean falsification.

**Custody risks found by the critics, and how they are avoided:**

| # | Risk | Avoidance |
|---|---|---|
| 1 | CCA Table 2 is public, so the gains are known | The target is the frozen k-rung verdict and its agreement, with no free parameter left after the dev freeze. The gain is never a claim. Disclosed in the prereg |
| 2 | A1-25 (SHIELD-LLaVA vs OPERA-ours): E6 unseeded sampling, E7 cross-repo, shares an E1 file | Excluded |
| 3 | A1-26: 6-image overlap, and its ids were already read (the "never touched" claim was wrong) | Excluded; the custody note is corrected here |
| 4 | A1-21 (Devils): E2 fidelity Δ 1.72 > 1.0; A1-16..18: E1 fail | Excluded |
| 5 | LLaVA-1.5 trained on COCO train2017, which holds most val2014 images, so A1 may fail | Budget adequacy (exceed(w_0) against the CHAIR-gold rung) is registered as an OC1 secondary readout. "Assumption not supported" is printed if it is > α_S |
| 6 | The images are spent: CCA uses the OPERA-500 ids, the F-B image set of A's H3 dev | Only method-arm outputs are new. Image-disjointness rule: OC1 is scored on ids not in `coco5000_ids.txt`, computed ids-only at opening, with ≥ 400 required (K0-OC1). w_0 is never refitted on OC1 |
| 7 | Gold source and matcher | OC1 gold comes from derived class sets (gt_cache f986f8ff covers the OPERA-500 ids). Two parts are unresolved: (a) whether gt_cache's matcher (E1 `nodes`) equals the dev matcher (`en_classes`), to be checked on dev before any prereg; (b) whether MARINE's ids are covered. If not, MARINE needs a G0-type ruling or is dropped |

**Gate.**
1. This step reads GO.
2. Dev-confirm rehearsal: P(PASS) ≥ 98% on dev for the OC1 rule.
3. OC1 prereg.
4. **Irreversible three-judge panel ≥ 85 plus read-only Codex**, and a **PI line**.
5. Only then the opening, in this order: ids-only K0-OC1, then the frozen run, then one look.

Until that point, no file under `a1_precheck/raw/` is read.

## 6. Outputs and LOG lines

**Outputs** (counts and labels only; no caption text and no per-image class lists in the repo):
- `data/results/a2_cpu_step/freeze/freeze.json`;
- `.../run_record/{STARTED.json, timing.json, run.stdout, run.stderr}`;
- `.../a2_cpu_result.json`, holding per rung: N, flips, N_c, W_C, the W_B values, w_0 per half, the Cov@5% values, Δ_cov, LB, discordance, the K labels, the verdict and the secondary readouts;
- `.../selftest.json`;
- `.../mutants_result.json`;
- code: `scripts/a2/*` with SHA256SUMS.

**LOG lines to write** (drafts; stamps from `date -u` at the time; not appended by this writer):
- `<utc> OPS-1110<x>-a2-plan: A2 CPU step plan v1 manuscript/prereg/2026-11-10_a2_cpu_step/A2_CPU_STEP_PLAN_v1.md <sha8> (PI-1110e); NGRAM PASS; nothing run, nothing committed; G0 ruling on dataset_coco.json (2fd99922) requested (rec: spent dev, allow; default: STOP). Next: one-judge FULL read, REVERSIBLE 85.`
- `<utc> | CC-<n> | A2 CPU step plan v1 <sha8> one-judge FULL read (round r/3), REVERSIBLE 85 | GO / NEXT_ROUND | <score>% | CC-<n>.txt`
- `<utc> OPS-<MMDD><x>-a2-g0: coordinator ruling (PI-1109d): dataset_coco.json <allowed as spent dev | barred -> step STOPPED>.`
- `<utc> OPS-<MMDD><x>-a2-code / -a2-freeze / -a2-run: shas, selftest/mutant counts, CPU s, PASS/FAIL.`
- `<utc> OPS-<MMDD><x>-a2-result: k=2 N 720; K1 W_C/N_c <w>/<n> (V-B), <..> (V-H), min W_B <..>; K2 Delta_cov <..> LB <..>; K3 discordant <..> over <..> pairs -> <GO | KILL | UNDERPOWERED>; result <sha8>.`
- On KILL, UNDERPOWERED or STOP: `<utc> OPS-<MMDD><x>-a2-close: A2 certify-or-abstain line CLOSED per A2_CPU_STEP_PLAN_v1 §7 (<reason>); Paper A (SPIC) unchanged; A2-OC1 never opened.`

## 7. GO to dev-confirm vs close the line

**GO** requires all of the following:
- K0 PASS;
- K1 PASS for both V-B and V-H;
- K2 PASS;
- not K3.

The next files after GO, each with its own gate:
1. **A2 dev-confirm prereg.** It registers the OC1 rule and a rehearsal on COCO-5000 with fresh reference draws (new seed), B and seed fixed. P(PASS) = the share of pair-cluster bootstrap replicates passing the rule, and it must be ≥ 98%. If the rehearsal fails, OC1 is never opened.
2. **The matcher-identity check** (§5, risk 7).
3. **The prior-art full-text reads** before any A2 text:
   - ITERATE_A §4.2 item 7;
   - 2212.09844 and 2204.00180 (T2 machinery);
   - 2209.08858;
   - Fröbe et al. 2023 (denominator coupling).
4. **The OC1 package** to the irreversible panel, Codex and the PI.

**CLOSE** follows on any of:
- KILL (K1 or K2);
- UNDERPOWERED (K3);
- G0 = barred (STOP);
- K0 still failing after 3 code rounds.

On CLOSE:
- write one OPS close line;
- report the FAIL briefly in a short A2 direction note, never hidden;
- leave Paper A unchanged;
- never open OC1;
- start no theorem work on this line.

**Not a GO:** a pass only at k ≠ 2, only on blocks, only on micro-F1, or only with V-B.

## 8. Out of scope and open risks (AI opinion)

- **T2 items for later, only after GO:**
  - the profile-sharp moment LP over mixing measures on [w, 1] using f2..fk (Mao 2006–2008; Wu–Yang 2019);
  - a minimax lower bound for the paired verdict;
  - the mixed-F1 extension.
- **Narrow dev evidence.** There is one model family (Qwen2.5-VL-7B variants writing Vietnamese), and the 720 units resample 36 pairs. The pair-cluster bootstrap accounts for the resampling; the single family is not fixed.
- **Scoop velocity is high** (ITERATE_A §3.3). A 2027 IP&M route stays conditional (ITERATE_A §6).
- **Vietnamese necessity is weak.** k = 2 mirrors Vietnamese benchmarks with 2–5 references, but the method is language-agnostic.

## 9. Read for this plan (sha256)

| File | sha256 (8) | Parts read |
|---|---|---|
| `manuscript/directions/ITERATE_A_2026-11-09T1717Z.md` | 9695f255 | full |
| `manuscript/directions/DR_GAPS_A_2026-11-10.md` | 170186a3 | full |
| `manuscript/directions/notebooklm/NOTEBOOKLM_COMPARE_A_2026-11-10.md` | 955bca2a | full |
| `manuscript/directions/rubric_2026-11-09/RUBRIC_A_2026-11-09.md` | d2cdd1bd | full |
| `.claude/skills/running-vsps-research-cycle/SKILL.md` | 1d9d69fe | full |
| `.session_backup/2026-10-13/decisions/LOG.md` | — | ll. 2000–2030 (PI-1110a..e) and the A-M1 rulings (ll. 1780–1793) |
| `scripts/a_m1/a_m1.py` | fa8c9bf2 | PINS and DENY (ll. 95–160) |
| `scripts/g2b/score_g2b.py` | 66c665c7 | loaders (ll. 55–140) |
| `manuscript/ken/K17_A1_INVENTORY_2026-10-27.md` | 4656ddde | licence and pairing rows (grep) |
| `precheck.json` | fa459a42 | E criteria, arm paths and shas, baseline recompute; no log file opened |
| `gt_cache.json` | f986f8ff | key structure, types and image ids (§2.2); no class content |
| H3 `REPORT.txt` and the `h3_n1.py` header | — | download provenance |
