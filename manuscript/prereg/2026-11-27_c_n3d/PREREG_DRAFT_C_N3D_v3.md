# PREREG DRAFT C-N3D v2: rule-based failure categories of the retrieval contrast on stored development decodes (Paper C, RQ3)

Drafted 2026-11-27T12:14Z (v1). Revised 2026-11-27 (v2) under ruling CC-509 (NEXT_ROUND 72). Each change is tagged [W1]…[W7] or [N1]…[N3]; the hunk-to-item map is in `V1_TO_V2.diff`.

DRAFT. It licenses nothing until a round-2 judge ruling (GO) and a commit through the gatekeeper. **No study number has been computed.** No stored per-image file was opened to write v1 or v2. Every input file named in section 4 was listed and hashed only. Each hash matched its `.sha256` sidecar, `scripts/c_attr/STORED_SHA256`, or a pin in code or a registration (see COMPUTE_C_N3D_v2.md).

**Text of record.** Paper C: `~/vsps_ro3/c_now/paper_v1_analysis/` 00–11 at HEAD 9bf8f89.

**Origin.** Benchmark `BENCH_C_2026-11-27.md` §5, NEW CONTRIBUTION rank 1, "N3(d) failure categories". The benchmark puts it at C9 4 → 5, +1.6 points, with P about 0.4 for this item alone (BENCH l.120). The route K1 + K2 + N3(d) = 81.4 has P(all three) about 0.3–0.35 (BENCH l.105). [N2]

**Lineage. [OQ-1 ruled, CC-509 ruling 3]**
- **N3D supersedes C-RAA step T8.** T8 is defined at `NOVELTY90_C_PILOT_PLAN_v2_2026-11-26.md:160`, `:177`. T8 is withdrawn from the C-RAA run order, and only one of the two runs. C-RAA's steps T1–T7 are unchanged.
- **Margin.** N3D reuses T8's margin, which NOTE1 W7-b fixed before any output (`NOTE1:122`): 10.0 points of per-image stripped CIDEr-D × 100. It does not reuse T8's other rules (length shift above 10%, seed 1126001, B 10,000).
- **C-RAA tier 2.** If tier 2 later inherits N3D's rules, it needs its own code, or code adapted from `raa_failcat.py` (tested tree c2add164, which implements T8's rules and not N3D's), and its own code read.

## 1. Question

When the retrieved examples (`ret`) give a caption a lower score than random examples from the same memory (`rand`), what goes wrong? Is the failure tied to what retrieval puts in the prompt (objects borrowed from the shown captions, near-verbatim copying), or to something generic (zero-shot content dropped, a length change, nothing the rules can see)?

Paper C now measures the retrieval contrast and splits it (τ_sel = τ_marg + τ_pair, Section 3.8). It has no categorised failure analysis (BENCH C9; `06:116`; `09:6`). This study adds that analysis with existing instruments only.

## 2. What this study is not

- **No new labels.** It makes no new gold labels and uses no human rating. No model output serves as gold, and no AI-silver label counts as evidence. The VLM verifier of Section 3.4 (its yes/no scores) is **not** used in any category or row.
- **No test set, and no contact with these files.** The following are never opened, pushed or staged:
  - OV-test (both files);
  - KTVIC test;
  - XM-test2500;
  - COCO Karpathy test;
  - NoCaps val;
  - Flickr30K test: its decodes, scores and outputs (`c_t3/**`);
  - **Flickr30K val: its decodes, scores and outputs (`c_t2/**`, the rehearsal used once)** [W1];
  - every C-CONF output (`.session_backup/machines/CONF_H1/**`, and the OV carve and confirm halves of registration 2);
  - every C-RAA tier-1 or tier-2 output;
  - **the per-image ledgers of the C-ATTR scoring (`.session_backup/machines/ATTR_H1/root/c_attr_score/led/*`), which are hash-only** [N1].
- **Id lists only.** `ov_test_files.tsv` and `c_conf_carve_order.json` are used only as id and sha256 lists in the custody check of section 10, step 2a. No OV-test or carve image byte, caption or output is read. [W3]
- **Whole public files with protected rows.** The Flickr30K CSV (`395990db…`) holds all Flickr30K splits, and `oiv7_labels.json` (`bac3953a…`) covers all XM3600 images. Both are pushed whole so that their pins hold. `c_n3d.py` keeps only the carve ids of `c_t1_f30k_lists.json` and the XM-dev500 ids of `lists.json`. It asserts that no id of `c_t1_f30k_lists.json` `refuse.val` or `refuse.test`, and no id of `lists.json` `sets.xm_test2500`, enters any row. No other row is parsed into a row, printed or scored. This is the contact already made by the Flickr30K carve exploration and by the C-ATTR verified precision. [CC-509 r2 R1]
- **No GPU.** It decodes nothing. All work is CPU work on stored decodes, done on a rented host that has never held, and will never hold, an OV-test byte (the committed name-and-sha256 list `ov_test_files.tsv` is not an OV-test byte; CC-483r2 ruling 5), the C-CONF token or a C-CONF output. [W2]
- **No change to Paper C's registered results.** It changes no registered result, verdict or scope sentence of Paper C. Every row is labelled **"DEVELOPMENT / C-N3D, NON-CONFIRMATORY; rule-based categories, no human labels"**.

## 3. Sets, backbones, decodes

| role | set | n | decodes (primary) |
|---|---|---|---|
| primary, carries the rule | OV-dev-B | 925 | batch size 1 (block 1b): `zs`, `ret`, `rand` d0, d1, d2 |
| secondary, rows with labels, no rule | XM-dev500 | 500 | the same |
| English comparison, descriptive | Flickr30K carve (Karpathy train, 1,000) | 1,000 | Flickr30K registration exploration: `zs`, `ret`, `rand` d0 (COCO memory) |

- **Overlap with Paper B's set H. [W7]** OV-dev-B's 925 images include 335 OpenViIC-dev copies of Paper B's BD-T1 held-out set H. None of them is a memory member (CC-493e1). They stay in the set, and the count is printed in every OV-dev-B table note.
- **Backbones.**
  - Qwen2.5-VL-7B: k 8, first, T1.
  - InternVL3-8B: k 4, last, T2, τ = −∞, with no deletion step, as in the attribution study.
  - Aya-Vision-8B: k 4, last, T1.
- **Aya-Vision-8B on OV-dev-B** carries the placebo flag of Section 6.10.5 (`rand` d1 − d2 = −2.03 [−3.42, −0.74]) on every row. Its placebo-differenced rows (section 6) use that same flagged contrast. It is outside the family.
- **Why batch size 1 is primary.** K1 fired (Section 6.10.2), so batched per-image differences can contain a batch-mate term. The block-1b set is complete for all three backbones on both sets. The stored batched stage-2 decodes are sensitivity row SR3 only, labelled "A1 not met; batched decode; descriptive".
- **The `rand` arms.**
  - `rand` d0 is the comparison arm for the retrieval split.
  - `rand` d1 and d2 form the placebo split (section 5).
  - The mean over R = 3 draws is sensitivity row SR1.
- **Not used.**
  - OV-dev-A, which has no batch-1 `zs` (OQ-2).
  - `perm` (hash-only, never pushed; OQ-5) [W1].
  - `fix`, which was batched only.
  - Flickr30K val (hash-only, never pushed) [W1].

## 4. Inputs (sha256; listed and hashed 2026-11-27, contents not opened)

Full paths and full hashes are in `COMPUTE_C_N3D_v2.md` §2. That section is split into a **PUSH LIST** and a **HASH-ONLY LIST** [W1].

**PUSH LIST**
- 30 batch-1 decode files (`zs`, `ret`, `rand` d0–d2 × 3 backbones × 2 sets) under `.session_backup/machines/ATTR_H1/root/outputs/c_attr_b1/out/`. Each matches its sidecar.
- Shown lists:
  - `scripts/c_attr/c_attr_lists.json` 8a2b977f…, which holds the per-draw `rand` lists;
  - `c_stage2/ex_ov_dev_b.json` 072b17d1…;
  - `c_stage2/ex_xm_dev500.json` 9a79b97d…;
  - `manuscript/prereg/2026-10-30_c_t1/c_t1_f30k_lists.json` eebcd95b…, the carve's shown lists and ids.
- SR3: 12 stored stage-2 batched decodes.
- English: 9 Flickr30K-carve decodes.
- Code: `c_attr_score.py` cca5e327…, `c_attr.py` a3bd7b93…, `match_openviic.py` c0d9dd30…, `score_coco_probe.py` d11db7e1….
- Gold, label and loader pins, all fixed now [W6c]:

| item | file | sha256 | loader (file:function) |
|---|---|---|---|
| OpenViIC dev references | `.session_backup/2026-10-22/c_stage2/subsets/uit-openviic-annotation-dev.json` (the stage-2 subset of record, 1,085,184 B; CC-362, OPS-1112bc), pushed unchanged to `ncs-data/datasets/openviic/` on the host | `550cfe06b06084976e81286531f7f4e52bea717e29004c699ccaf1e48919bdff` | `c_attr_score.py`, the reference loader of `score_call` (l.647), with the pin `B3_REFS` at l.84–85 |
| XM3600 Vietnamese references (XM-dev500) | `datasets/c_xm_dev500/xm_dev500_data.json` (host data folder) | `0da82355b65ab284fe55fc0d3c4101090301767347a02721890556618ca4905f` | `c_attr_score.py`, the same loader, with the pin `B3_REFS` at l.86 |
| Flickr30K train references (carve) | Flickr30K CSV, `nlphuji/flickr30k` @2b239bef | `395990db603ab8bafd5c7ab2746b22058bb1e75b78b3eb56ad755931364ac137` | `c_attr.py`: `f30k_rows` / `f30k_split` (l.149), sha check `F30K_CSV_SHA256` (l.81, l.181) |
| Open Images human-verified labels for XM3600 | `data/xm3600/oiv7_labels.json` | `bac3953a511a9793c22e928a29b68ae05dbf9654502abcbe7b64fd9f6d74c8b2` | `scripts/xm3600_oiv7.py` 9a79403f… (`resolve_map`, `statuses`, `caption_rows`), as called by `scripts/c_stage2/score2.py` 0f99e36e… `cmd_verified` (l.192–226) |
| OIV7 class descriptions | `data/datasets/xm3600/oiv7/oidv7-class-descriptions.csv` | `84a4373a0efb7fd6d93fe19b0e7ceb6c1b855c233d13b9b78a9a33655c9fdce3` | `xm3600_oiv7.resolve_map` |
| Vietnamese-to-OIV7 class map | `data/xm3600/vi_oiv7_map.json` | `27f2b1ca3f2bf47d43c8f00e8409472c8d571eb720d47b8107a1c77bd208d16a` | the same, via `score2.cmd_verified` |
| label provenance record | `data/xm3600/manifest.json` | `263015f9dc46ebe2cea80055e04ed39baf80a356f4e027cd3756464279135bef` | read at the code read only |
| VnCoreNLP 1.2 jar (RDRSegmenter) | `VnCoreNLP-1.2.jar` | `9e2811cdbc2ddfc71d04be5dc36e185c88dcd1ad4d5d69e4ff2e1369dccf7793` | `score2.py` l.153, check against `S.JAR_SHA256` |

- **The verified labels.** They are the public Open Images V7 human-verified image labels for XM3600 images, as used offline for Paper C's verified precision (Section 3.6). They are **not** Paper A's XM600 gold. XM-dev500 is disjoint from XM600 (`04_data_and_splits.md` l.13, l.16, l.32). The code read confirms this provenance from `manifest.json`. [W6c]
- **The release file is not the pin.** The laptop file `data/datasets/openviic/uit-openviic-annotation-dev.json` (1,192,514 B, mtime 2024-05-27, sha256 `2a68a3eb…`) is the original release. The pin `550cfe06…` is the stage-2 subset of record (CC-362), and three copies of it agree under `.session_backup/` (2026-10-22, 2026-10-30, 2026-11-18). The release file is never pushed or used. The host STOPs if its copy does not hash to `550cfe06…`. (OQ-11, established by listing and sha256 in CC-509 r2.)
- **Custody-check lists (ids and sha256 only, read in section 10 step 2a)** [W3]:
  - `manuscript/prereg/2026-10-22_c_stage1/lists.json` `5c479f03e8be544f4cd12b5d997b5dc92b6c622df061760cd02f6ba82f6b4371` (keys `ov_dev_b`, `xm_dev500`, `xm_test2500`, `image_sha256`);
  - `manuscript/prereg/2026-10-25_c_test/ov_test_files.tsv` `99d4fc49cc8283d1555d37b975cca5a32598ea0ec571d8bef8cf811df2c33695`;
  - `manuscript/prereg/2026-11-18_c_conf/c_conf_carve_order.json` `8e11bad51c77adc54c05b91a86f7b6f5a1f2d0e9032f06faf80f05e438d42850`;
  - the carve ids of `c_t1_f30k_lists.json` (above).

**HASH-ONLY LIST (never pushed, never opened)** [W1, N1]
- 12 `perm` p1/p2 batch-1 decode files.
- 8 `t2_*_f30k_val` decode files.
- 5 C-ATTR per-image ledgers under `ATTR_H1/root/c_attr_score/led/`: `ovb.jsonl` f79ea6a9…, `xm_b1.jsonl` f8e375a3…, `ova.jsonl` 324550c3…, `bat_ov_dev_b.jsonl` ca675471…, `bat_xm_dev500.jsonl` 00310e59….

## 5. Definitions (fixed before any output)

All of these are per backbone b, set S and image i.

**Per-image score.** s_i(a) is stripped CIDEr-D × 100 of arm a, computed as in Section 3.6. Document frequencies come from S's own references and are computed once per set. English uses the PTB-tokenised CIDEr-D of Section 8.1.

**Differences.**
- The retrieval split uses d_i = s_i(`ret`) − s_i(`rand` d0).
- The placebo split uses e_i = s_i(`rand` d1) − s_i(`rand` d2). [W4]

**Groups.** The margin is M = 10.0 (T8, NOTE1 W7-b).
- Losers: L = {i : d_i < −M}.
- Winners: W = {i : d_i > +M}.
- Placebo losers: P− = {i : e_i < −M}.
- Placebo winners: P+ = {i : e_i > +M}. [W4]

**Object sets.**
- Classes are found with the matcher of Section 3.6 (English: the COCO-80 matcher).
- G_i is the gold class set, the union of image i's references.
- On XM-dev500, the verified labels decide the classes they cover, through the `statuses` rule of `xm3600_oiv7.py` unchanged. A class they do not cover is decided by the reference union. The share decided each way is printed.
- A class is **unsupported** when it is absent from G_i (OV, English) or verified absent (XM).

**Flags.** Each flag is computed on the caption y_a of arm a ∈ {`ret`, `rand` d0, `rand` d1, `rand` d2}, each against that arm's own shown list S_a,i. The flags are multi-label.

| flag | rule | instrument (existing) |
|---|---|---|
| **BO** (borrowed unsupported object) | at least one neighbour-only class of y_a (Section 3.4: in y_a, absent from the same backbone's batch-1 `zs` caption, present in a caption of S_a,i) that is unsupported | matcher, Section 3.4 rule, references / verified labels |
| **CP** (near-verbatim copy) | m(y_a, S_a,i) ≥ 0.90, with m the near-verbatim copy statistic of supplement l.791 | copy statistic |
| **ZL** (zero-shot content lost) | at least one class in the `zs` caption that is supported (in G_i, or verified present) and absent from y_a | matcher, references / verified labels |
| **LN** (length off) | \|len(y_a) − med_i\| ≥ 0.25 · med_i, with len in syllables and med_i the median syllable length of image i's references | lengths |

**Exclusive category of an image** in a group: it is read from the caption on the "treatment" side of that split (`ret` for L and W; `rand` d1 for P− and P+). It is assigned by fixed precedence **CP > BO > ZL > LN > OTHER**. Precedence follows how directly a category can be attributed to the prompt.

**Sensitivity rows** (descriptive, no label):
- SR1: `rand` = mean over d0–d2, in the retrieval split only.
- SR2: M ∈ {5.0, 15.0}.
- SR3: stored batched stage-2 decodes. These have no d1 or d2 for Qwen and InternVL3 on XM, so the rows are not placebo-differenced.
- SR4: LN at 0.10 and 0.40.
- SR5: T8's own length rule (ret-versus-rand length shift above 10%).
- SR6: exclusive categories under the reversed precedence LN > ZL > BO > CP > OTHER.
- SR7: the relative-risk form of the H1 and H2 estimands, log[Pr(f | L)/Pr(f | W)] − log[Pr(f | P−)/Pr(f | P+)], for the base-rate confound of section 6. [W4]

## 6. Estimands, hypotheses and thresholds

**Bootstrap. [W6b]**
- The index matrix is `numpy.random.default_rng(1127001).integers(0, n, (2000, n))`. One generator is created once and called once per set, in the order OV-dev-B (n = 925), XM-dev500 (n = 500), Flickr30K carve (n = 1,000). All backbones and rows of a set share that set's matrix.
- L, W, P− and P+ are recomputed inside each replicate. Numerator and denominator are resampled together.
- p̃ = (1 + #{b : statistic_b ≤ threshold}) / (2000 + 1), one-sided.

**Why the verdict uses a placebo-differenced contrast. [W4]** The difference d_i is stripped CIDEr-D against the references. BO needs a class absent from the references, and ZL needs a dropped class that is present in them. Either one can lower the flagged caption's own score mechanically. So "Pr(flag | L) > Pr(flag | W)" follows in part from how d_i and the flags are defined, whether or not retrieval matters.

The placebo split d1 − d2 has the same coupling. Its "treatment" caption (d1) is flagged against its own shown list in the same way. But its two arms differ only by a random draw, and no retrieval is involved. Subtracting the placebo enrichment removes the part that the score definition alone produces.

**Residual confound, stated.** Neighbour-only classes are more frequent with retrieved examples than with random ones. On OV-dev-B, InternVL3 batched, the share of classes was 0.340 against 0.152 (Section 6.8). The mechanical coupling grows with the base rate of the flag, so a positive difference can still arise from the higher base rate under `ret` without any retrieval-specific harm. SR7 (relative-risk form) and the printed base rates Pr(f | all) per arm are there to read this. A PASS is worded as an association beyond the placebo, never as a cause (section 8).

**G0, the noise floor (descriptive only; it no longer gates wording). [W4]** It prints |L|, |W|, |P−| and |P+|, with E = (|L| − |P−|)/n and its CI.
- v1 made G0 gate the wording. That was ill-posed. d has a positive mean (τ_sel > 0), while e is centred near 0. So |L| < |P−| is expected even when retrieval has a real failure mode, and E ≤ 0 says nothing about whether losers are noise.
- G0 is therefore printed with this sentence and no reading rule.

**Decidability.** A row is decided only if each of L, W, P− and P+ holds at least 30 images on the full sample. Otherwise it is **NOT DECIDABLE (counts)**. **A NOT DECIDABLE row enters Holm with p̃ = 1; m stays 6.** [W6a]

**Primary family** (Holm, one-sided family-wise α = 0.025, m = 6): H1–H3 × {Qwen2.5-VL-7B, InternVL3-8B} on OV-dev-B.

For flag f, let D_f^ret = Pr(f(`ret`) | L) − Pr(f(`ret`) | W) and D_f^plac = Pr(f(`rand` d1) | P−) − Pr(f(`rand` d1) | P+).

| id | estimand | PASS if | reading if PASS |
|---|---|---|---|
| **H1** borrowed-object enrichment beyond the placebo [W4] | Δ_BO = D_BO^ret − D_BO^plac | point ≥ +0.10 **and** Holm-adjusted p̃ (Δ_BO ≤ 0) < α | the images that retrieved examples cost more than 10 points carry an unsupported borrowed object more often than the images they helped, by more than two random draws produce between their own losers and winners |
| **H2** zero-shot-content-lost enrichment beyond the placebo [W4] | Δ_ZL = D_ZL^ret − D_ZL^plac | point ≥ +0.10 **and** Holm-adjusted p̃ (Δ_ZL ≤ 0) < α | the same for dropped supported zero-shot content |
| **H3** coverage compared with winners [W5] | C_L = 1 − Pr(OTHER \| L); C_W, C_P−, C_P+ likewise | C_L point ≥ 0.60 **and** Holm-adjusted p̃ (C_L ≤ 0.50) < α **and** point of C_L − C_W ≥ +0.10 **and** point of (C_L − C_W) − (C_P− − C_P+) ≥ 0 | "the rules flagged more of the images retrieval hurt than of those it helped" (no wider reading) |

- C_W, C_all, C_P− and C_P+ are printed with CIs on every H3 row. [W5]
- The last point condition of H3 (≥ 0 beyond the placebo) is added in v2 for the same coupling reason as W4. It makes H3 stricter than the form CC-509 suggested.
- Anything other than PASS is FAIL. There is no third verdict apart from NOT DECIDABLE.

**Power, corrected. [W4]** The printed CIs imply the following. These are planning values, derived from the CIs and not from data.
- **Qwen2.5-VL on OV-dev-B, retrieval split.** τ_sel = +8.27 [6.54, 10.11] at n = 925 gives an SE of about 0.91, so the per-image SD of d is about 28. Under a normal approximation, that implies about 0.26 · 925 ≈ 240 losers and about 0.48 · 925 ≈ 440 winners.
- **Placebo split.** e has mean near 0 and a similar SD, which implies about 300–330 images in each of P− and P+.
- **InternVL3.** τ_sel = +5.22 implies about 270 losers and about 400 winners.
- **Standard errors.** At a flag rate near 0.3, the SE of each D is about 0.04, so the SE of Δ is about 0.05–0.06 (the two splits share images, and the correlation is ignored). A true Δ of +0.10 then has power of about 0.4–0.5 at the Holm level.
- **Caveat.** Per-image CIDEr-D is skewed, so the realised counts may differ. The +0.10 threshold is kept and not tuned.

**Thresholds, with reasons.**
- +0.10 is the smallest difference in share that a reader would call a different failure profile.
- 0.60 and 0.50 make "most" strict.

**Secondary rows** (labels printed, no family, no conclusion beyond the row):
- **S1:** within L, Pr(BO(`ret`)) − Pr(BO(`rand` d0)), paired. Labels are DETECTED, REVERSED or UNRESOLVED. **The coupling is stated:** L is selected on `ret` < `rand`, and BO lowers the flagged caption's score, so S1 is biased towards DETECTED by construction. Its placebo twin, within P−, Pr(BO(d1)) − Pr(BO(d2)), is printed beside it. [W4]
- **S2:** the same for CP, with its twin.
- **S3:** shares of every exclusive category in L, W, P− and P+, with 95% CIs, per backbone and set.
- **S4:** H1–H3 estimands for Aya-Vision-8B on OV-dev-B, with the placebo flag.
- **S5:** every H and S row on XM-dev500 (all three backbones; BO on verified labels).
- **S6:** G0 on each set.

**English comparison** (descriptive, no label):
- Only `rand` d0 exists on the carve, so there is no placebo split. The English rows print D_f^ret and S3, labelled "**not placebo-differenced; coupled by construction (section 6)**".
- They use the COCO-80 matcher, with Flickr30K references as gold.
- The decode policy is the Flickr30K registration's, as stored (OQ-4).
- Each English row sits beside the matching OV-dev-B D_f^ret row. No Vietnamese-minus-English difference is computed.

## 7. Numbers already seen (all from the text of record; none is a category share)

**What is known about per-image values.**
- No per-image count of `ret` < `rand` − 10, and no category share, has been printed or logged for any set. The CC-509 judge grep of LOG.md, the paper text and `manuscript/reviews` found none.
- **Ledgers [N1].** The C-ATTR block-1b scoring computed per-image differences internally and wrote per-image ledgers. They are at `.session_backup/machines/ATTR_H1/root/c_attr_score/led/` (`ovb.jsonl`, `xm_b1.jsonl`, `ova.jsonl`, `bat_ov_dev_b.jsonl`, `bat_xm_dev500.jsonl`, `parity_c2.jsonl`). As far as the drafter knows, none of them has been opened by a person or an agent since it was written. They are on the HASH-ONLY LIST.
- **SD of d [W4].** When v1 set M = 10.0 (reused from T8) and the "≥ 30" rule, the per-image SD of d (about 28 on OV-dev-B) could be derived from the printed CIs of Tables 11 and S21. v1's power line ignored it. v2 corrects that line in section 6. M is unchanged, because NOTE1 W7-b fixed it before any output.

**Numbers already seen.**
- **Groups depend on these.** Table 11 and Table S21 give batch-1 τ_sel, τ_any, τ_pair and τ_marg on OV-dev-B and XM-dev500 for all three backbones.
  - OV-dev-B τ_sel: Qwen +8.27 [6.54, 10.11]; InternVL3 +5.22 [3.67, 6.81]; Aya +6.25 [4.87, 7.69].
  - XM-dev500 τ_sel: +1.79 / +0.11 / +1.74.
  - Also seen: Table 10 (OV-dev-A); Table S22 (batched, including Qwen OV-dev-B +9.25); Tables S16 and S17 (stage B, d0 batched: Qwen +9.67; InternVL3 τ = −∞ +5.36 on OV-dev-B and +1.54 on XM).
- **The placebo split depends on these.** The `rand` d1 − d2 placebo of Section 6.10.5 and Table S23a: Aya OV-dev-B −2.03 [−3.42, −0.74], flagged; Qwen XM +3.21; InternVL3 XM −1.49. Section 6.10.5 also gives the variance shares of the random draw: 0.089 / 0.163 / 0.149 on OV-dev-B and 0.160 / 0.192 / 0.203 on XM-dev500.
- **BO depends on these.**
  - Section 6.8 (batched, OV-dev-B, InternVL3): neighbour-only share of classes 0.340 (`ret`) against 0.152 (`rand`), and a reference-gold precision of 77.31 (714 mentions) (supplement l.722–723).
  - Section 6.6 (test, not used): 73.41 / 77.44 / 92.82.
  - BO is labelled "shaped by aggregates already seen".
- **CP depends on these.** Table S11, stage-B near-verbatim share on OV-dev-B, τ = −∞: Qwen `ret` 0.026 and `rand` 0.001; InternVL3 0.003 and 0.000. The XM-dev500 rows were also seen. The test figures were 0.015 / 0.002. CP is expected to be rare, and no hypothesis rests on it.
- **LN depends on these.** Table S11 mean syllables (Qwen `ret` 18.23 and `rand` 17.46; InternVL3 19.25 and 19.23) and Table S6 (test). Reference median lengths have not been seen. LN is labelled "shaped by length aggregates already seen".
- **Copy bound.** Table 12, all rows, and Table S19 English carve rows: `ret` − `rand` +6.12 / −1.00 / +5.04; masked rows −3.58 / −10.37 / −14.33.
- **Margin.** M = 10.0 was fixed by C-RAA NOTE1 W7-b before any output.
- **Set H [W7].** 335 of OV-dev-B's images are copies of Paper B's BD-T1 set H (CC-493e1, LOG l.3156). That is a count only. No Paper B label enters this study.

## 8. Falsifiers and what the paper may say

Every sentence carries "development data, re-used sets, non-confirmatory; rule-based categories from existing instruments, no human labels". [W4: the sentences below follow the placebo-differenced estimands.]

| outcome | the paper may say | the paper may not say |
|---|---|---|
| H1 PASS for both backbones | "On OV-dev-B, the images where retrieved examples lowered the score by more than 10 points carried an unsupported object found only in the shown captions more often than the images where they raised it, and this difference exceeded the one between the losers and winners of two random draws (Qwen Δ +x [CI], InternVL3 +y [CI]). Part of it may reflect the higher rate of borrowed objects under retrieved examples (SR7)." | that borrowed objects *cause* the loss; that the score definition plays no part; anything about test sets |
| H1 PASS for one backbone | the same sentence for that backbone, with the other row printed as FAIL | a general statement across backbones |
| H1 FAIL (both) | "Beyond what two random draws show, unsupported borrowed objects were not more frequent among the images retrieval hurt than among those it helped (rows)." | that borrowing is harmless (BO is one rule) |
| H2 PASS / FAIL | the same pattern for dropped zero-shot content | – |
| H3 PASS | "The rules flagged more of the images retrieval hurt than of those it helped (C_L x, C_W y)." | that the rules explain *why*; "most failures are explained" |
| H3 FAIL | "The four rule-based categories did not separate the images retrieval hurt from those it helped (C_L, C_W rows)." | – |
| **NULL** (H1, H2, H3 all FAIL, or NOT DECIDABLE) | the category table (S3) with intervals, the G0 row and the placebo rows, and one sentence: "Beyond the placebo, the rule-based categories do not separate the images retrieval hurt from those it helped." This is still printed in Section 6.10 and the supplement. | any mechanism claim; no C9 credit argued in the cover letter |
| D_f^ret > 0 but Δ_f ≤ 0 | "The enrichment seen between losers and winners is matched by two random draws, consistent with the score definition alone." | any retrieval-specific reading of D_f^ret |
| S1 DETECTED | the row with its stated coupling and its placebo twin beside it, and no sentence beyond the row | that the difference is retrieval-specific |
| XM-dev500 / English rows | label printed, no conclusion (n = 500; English has no placebo split) | a transfer or language claim |

**Falsifiers** (each named before any output):
1. Δ_BO ≤ 0, with its CI including 0 or below it: refutes "failures are marked by borrowed objects beyond what the score definition produces".
2. The same for Δ_ZL.
3. C_L − C_W < +0.10, or below its placebo twin: refutes "the rules pick out failures".
4. SR6 (the reversed precedence) changes which category is the largest in L: the exclusive shares are precedence-driven. The text then reports the multi-label flags and not the exclusive ranking.
5. SR7 has the opposite sign to Δ for a PASS row: the PASS is attributed to the base-rate confound, and section 8 row 1 is replaced by the D_f^ret > 0, Δ ≤ 0 sentence.

## 9. Where the rows go in the paper

- A new subsection, 6.10.10 "Failure categories on development data", with one table (OV-dev-B primary; XM-dev500 and the Flickr30K carve beside it). The table note carries the W7 count.
- Supplement tables for SR1–SR7 and the placebo rows.
- One limitation bullet in Section 9: rule-based categories, matcher recall, incomplete reference-union gold, the coupling of flags with the score, and re-used development sets.

Nothing is added to the abstract, the contributions list or the conclusion unless the PI decides otherwise after the PI rewrite.

## 10. Order of work (after a round-2 GO and the commit)

1. **Code.** Write `c_n3d.py`, which imports `c_attr_score` unchanged for scoring and the copy statistic, and `xm3600_oiv7` unchanged for verified statuses. Add a self-test with planted cells: a hand-built toy set where each flag, the precedence, the placebo difference and Holm with a NOT DECIDABLE row are known. Then a judge's code read. **No input is opened before that read.**
2. **Host.** Use a rented host that has never held an OV-test byte (the committed name-and-sha256 list `ov_test_files.tsv` is not an OV-test byte; CC-483r2 ruling 5), the C-CONF token or a C-CONF output [W2]. Push the PUSH LIST only, then run a per-file sha256 STOP check against section 4.
   - **2a. Custody check [W3].** Before any decode file is opened:
     - intersect the image ids and the image sha256 values of OV-dev-B (925) and XM-dev500 (500), the sha256 being the third field of each entry of `lists.json` `sets.ov_dev_b` and `sets.xm_dev500`, with the names and sha256 values of `ov_test_files.tsv` (`99d4fc49cc8283d1555d37b975cca5a32598ea0ec571d8bef8cf811df2c33695`) and with the ids of `c_conf_carve_order.json` (`8e11bad51c77adc54c05b91a86f7b6f5a1f2d0e9032f06faf80f05e438d42850`);
     - intersect the XM-dev500 ids with the XM-test2500 ids of `lists.json` (`5c479f03…`);
     - intersect the 1,000 carve ids of `c_t1_f30k_lists.json` (`eebcd95b…`) with its `refuse.val` (1,014) and `refuse.test` (1,000) ids;
     - no image file is pushed or read for this check.
     - Only counts are printed. **Any count above 0 is a STOP.**
   - **2b.** Self-tests and mutants.
3. **Run once,** in order: G0 → S3 → H1–H3 → S1, S2, S4, S5 → SR1–SR7 → English. Every output is an aggregate (counts, shares, CIs). The output never holds captions or per-image rows.
4. **Decision file.** Hash it, then log it. Scoring and the decision run once.
