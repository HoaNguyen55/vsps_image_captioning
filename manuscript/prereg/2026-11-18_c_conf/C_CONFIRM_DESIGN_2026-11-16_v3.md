# Paper C: design of one confirmatory test (C-CONF)

**Version 3, written from 2026-11-17T15:44:57Z (stamp from `date -u`) after ruling CC-438 (round 2, NEXT_ROUND; median 82, J1 84, J2 80, J3 82; sha256 `da467d38296c8787babd37fb3a8af0cee357d7bc8987db56fd354d9a513f586e`), for round 3, the last.** Versions 1 (`4ea07e00…`) and 2 (`79671ae00bb21ba5f899a0d93ac317d9a5fcaafc9cb4e8cc2971bd5a66924207`) are unchanged on disk; the changes of version 3 are listed with their closing text in `C_CONFIRM_CC438_RESPONSES.md` and in the diff file beside this one; the changes of version 2 are in `C_CONFIRM_CC436_RESPONSES.md`. Version 2 was written at 2026-11-15T22:31:38Z after ruling CC-436 (NEXT_ROUND; J1 70, J2 85, J3 78; sha256 `ccf67622…`). Version 1 was written between 2026-11-15T19:03Z and 2026-11-15T19:19Z, under PI-1116a item 3 and PI-1116e. This is a design for round 3, the last, of a three-judge read. Nothing here has run. For this file no test-set prediction file, no ground-truth cache, no label file and no caption was opened; the records checks of version 3 parsed the group's panel file in memory and hashed host-backup files, as the custody record of the registration draft §1.2 lists; nothing was registered, committed or written to the LOG; the Paper C repository was read only (HEAD `55315ca`). For version 2 one records check was made (LOG lines, registration text, id lists, listings and hashes only): the contact table of Section 2 and the input table of the registration draft §6.4a. CC-438 licenses no run on study data, no token, no host rental and no test look; FP-7 (recorded yes, LOG OPS-1115cm-cc438) lets the code and self-tests be drafted on synthetic fixtures. For version 3 the records checks of the registration draft v0.3 §1.2 were added (ids, LOG lines, script source, hashes; custody record there). The registration draft that goes with this file is `C_CONFIRM_PREREG_DRAFT_2026-11-16_v3.md` (draft v0.3); where the two differ, the draft governs.

Every probability, every expected rubric level and every hour figure is my opinion or my arithmetic and is marked as such. "My arithmetic" means a number computed from printed aggregate rows of the paper; no per-image file was read. "chưa kiểm" = not verified. Vietnamese scores are stripped CIDEr-D points.

Files read (first 16 hex digits of sha256): `benchmark/RUBRIC_v1.md` 3071ed8d6827c9ad; `benchmark/C_BENCHMARK_2026-11-15.md` 2d7454abda809247 (in full); `directions/C_DIRECTIONS_FROM_OBSERVATIONS_2026-11-16.md` e55f0d43cdeb31d6 and `directions/C_METHOD_M1_PRIOR_ART_2026-11-15.md` 0ecad46cef29cc80 (both in full); `directions/redesign_2026-11-11/REDESIGN_C.md` (short answer and section 1); `prereg/2026-11-11_c_attr_dev/C_ATTR_DEV_PREREG_v1_1.md` 44f81329d418efef and `C_ATTR_DEV_ADDENDUM_v1_2.md` 5858d69d7c1fa5df (both in full); `prereg/2026-10-25_c_test/PREREG.md` acecd6527217c5c5 (headings, sections 3.1 and 6); `prereg/2026-10-30_c_t2/PREREG.md` 4e831b23c8314cdb (in full; the rehearsal form of the project); `prereg/2026-10-22_c_stage1/lists.json` 5c479f03e8be544f (keys and counts only); the skill `running-vsps-research-cycle`; of the paper at `55315ca`: `06_results.md` Sections 6.1 to 6.3, 6.7 (Table 9), 6.10 and 6.11 in full, `03_method.md` Section 3.8, `09_limitations.md` Section 9.1, `07_disclosures.md` (the rows on re-used sets), `11_supplement_registered_rows.md` Tables S20 to S22; decisions LOG lines CC-099, CEN-COCO, CEN-NOCAPS, CC-196, CC-202, OPS-1112k, OPS-1114ap, PI-1029n, PI-1115v, PI-1115w, PI-1116a, PI-1116e.

Location form for numbers: `file::table or key`. `06` = `paper_v1_analysis/06_results.md`, `11` = `paper_v1_analysis/11_supplement_registered_rows.md`, both at `55315ca`.

## 1. Short answer

**Recommended: one decode session on OV-test at batch size 1 (test T3 below), which carries the confirmatory test of the attribution split as its only registered family and, from the same decodes, a batch-size-1 repeat of the registered per-backbone contrast with three random draws.** It is one look at one already used test set, under one new registration, after one development rehearsal on 2,000 OpenViIC training images that no Paper C study has decoded or scored as a query (Section 4.1 says what else they were used for). Only the attribution split is confirmatory; every other row from the same decodes is labelled "secondary, no family-wise error control".

- The two tests named by the benchmark are not alternatives: every decode that the batch-size-1 repeat needs (`ret` and `rand` at batch size 1) is already an arm of the split. Running the split alone would throw the repeat away; running the repeat alone cannot move the two criteria with the largest gain.
- My probabilities, revised after CC-436 (factor B lowered to 0.80–0.85; Section 4.3): the rehearsal reaches its bar for all three backbones, about 0.71 to 0.76 (version 1 said 0.80). The test look takes place (the primary backbone enters and the gates hold), about 0.79 to 0.84 before the investigator's decisions. All three registered claims pass at test, about 0.69 to 0.74. At least two pass, about 0.77 to 0.82.
- Compute: about 34 GPU-hours at planning rates (17 for the rehearsal, 17 for the test), about 50 under the caps. Calendar: seven days from the design read to the result read (Section 5).
- Rubric: **unconditional, the expected gain is about +2.6 to +2.7** (CC-438 ruling 6; version 2 said +2.9, and +3.7 conditional on all claims passing, both computed with P(C5 moves) 0.65, which CC-438 lowers to about 0.5). The gain of +4.4 that the benchmark prints for this item needs two criteria to move, and I give the second one (novelty) about 0.30 (Section 6).
- **Probability of reaching 80, as the panel rules it: about 0.30, less likely than not** (CC-438 ruling 6, J1, J2 and J3; CC-436 gave 0.25 to 0.40; my version-1 figure of 0.45 is withdrawn as optimistic). The gain is reliability (C7, through the rows S-rep and S-batch), not novelty. Under PI-1115t C-CONF must not displace a method or novelty route for Paper C; one must run in parallel (Section 6.1). The study is still the only registered route above the text-only ceiling of about 78.8 (Section 6.1).
- **What this test cannot do.** It does not show that retrieval helps (for two backbones the sum is known on this set, so for them the test is a split of a known contrast). It does not make the split new: the reassigned-list arm is published (`Li2024RetrievalRobustness`; `REDESIGN_C.md` short answer). It makes no row outside the one family confirmatory. Its batch row does not isolate batch size, because machine and software stack change with it. It confirms a registered prediction about where the retrieval-specific effect lies, on a test set looked at a second time, with a positive and a placebo control.

## 2. What is already known (the exploration)

All of this is tier 1 (exploration) for C-CONF. No rule of C-CONF may be tuned on it after the registration is committed, and none of its files is a rehearsal file.

| fact | number | location |
|---|---|---|
| nomination on OV-dev-A (911), batch size 1 | τ_pair +7.43 [5.54, 9.20] Qwen2.5-VL-7B; +4.96 [3.12, 6.82] InternVL3-8B (τ = −∞) | `06::Table 15` |
| the same set, τ_marg | −0.06 [−1.38, 1.30]; −1.43 [−2.78, −0.08] | `06::Table 15` |
| one look on OV-dev-B (925), batch size 1 | τ_pair +7.30 [5.58, 9.25]; +5.57 [3.94, 7.27]; +6.78 [5.33, 8.30] (Aya-Vision-8B, no claim) | `06::Table 16` |
| the same set, τ_marg | +0.96 [0.01, 1.94]; −0.35 [−1.40, 0.70]; −0.53 [−1.46, 0.41], all NEGLIGIBLE | `06::Table 16` |
| the same set, τ_sel at batch size 1 | +8.27 [6.54, 10.11]; +5.22 [3.67, 6.81]; +6.25 [4.87, 7.69] | `06::Table 16` |
| the same set, batched decodes | τ_sel +9.25, +5.19, +6.78; τ_pair +8.32, +5.62, +7.14 | `11::Table S22` |
| XM-dev500 (500), batch size 1, no rule | τ_pair +2.62 [−0.75, 6.10]; +1.11 [−1.97, 4.52]; +3.15 [0.06, 6.36] | `11::Table S21` |
| batch composition | 42/50, 37/50, 31/50 identical captions; D1 50/50 for all three | `11::Table S20` |
| placebo `rand` d1 − d2 | flagged for Aya-Vision-8B on OV-dev-B: −2.03 [−3.42, −0.74] | `06::Section 6.10.5` |
| positive control (LMCap, image-blind generator) | τ_sel +16.92 [15.00, 19.06] on OV-dev-B | `06::Table 18` |
| registered test rows on OV-test primary (1,941), batched, one draw | Qwen2.5-VL-7B `ret` − `rand` +8.33 [7.01, 9.76]; InternVL3-8B at τ = −∞ +3.71 [2.29, 5.14] | `06::Table 7`, `06::Table 9` |
| registered stage-B rows on OV-dev-B, batched, one draw | Qwen2.5-VL-7B +9.67; InternVL3-8B at τ = −∞ +5.36 | `C_ATTR_DEV_PREREG_v1_1.md::§1` (from Tables S16, S17) |
| stop rule of the development study | K1 fired for all three backbones; block 1 carries no claim; the batch-size-1 addendum was registered on string-identity counts only | `06::Section 6.10.2`; addendum v1.2 V1 |
| block 2 (backbones outside the Qwen line first decoded under that registration) | 0 of 3 ran by the cut-off 2026-11-14 18:00 (UTC+7); family S-BB is empty | `06::Section 6.10.9`; LOG OPS-1114ap |

Why assumption A1 was not met: A1 said that one image's caption does not depend on the other images of its batch. The check decoded 50 items in reversed order at batch size 1 and compared strings with the batched decode; 8, 13 and 19 captions differed. The cause given in the paper (padding and numerical shape) is a post hoc reading, not tested. At batch size 1, A1 holds by construction once the decode is deterministic, and the determinism check D1 passed 50/50 for all three. C-CONF therefore decodes everything at batch size 1 and keeps D1 as its gate; it does not reopen A1.

**Look history of the test sets** (from `C_METHOD_FAST_2026-11-15.md` section 2, the paper's `07_disclosures.md` and the LOG lines above):

| set | looks so far |
|---|---|
| OV-test (primary 1,941; full 2,001) | one registered look (2026-10-25) and ten other kinds of earlier contact: the table K1 to K11 follows below (full rows in the registration draft §1.2). Aya-Vision-8B and the LMCap re-implementation have never been decoded on it; the only earlier test-set decode of either system is the Flickr30K look of Section 8.6 of the paper (LOG OPS-1031ct3-T). No `perm` arm, no draw d1 or d2, and no batch-size-1 decode exists for it. |
| XM-test2500 | registered look of 2026-10-25; re-used in a development role (`06::Section 6.9`). Refused by C-CONF. |
| COCO Karpathy test, NoCaps val | registered looks of 2026-10-27 (LOG CEN-COCO, CEN-NOCAPS). Refused. |
| Flickr30K test | registered look under the registration of 2026-10-31 (LOG CC-202), `ret` against the baseline only. Refused. |

**Every earlier contact with OV-test (images, references or derived quantities).** Built from LOG lines, registration text, script source and ids, one status per row. K4 was settled on 2026-11-15; K3 (by kind, as CC-438 E1 asks), the full read of K10 and K11 on 2026-11-16. The rows K3-0 to K3e, with every script, line and LOG id, the ids check (`k3_ids_check.py` `29df4d0a…`, output `094f35c5…`) and the custody record (the panel file was parsed in memory five times; only ids and counts were printed) are in the registration draft §1.2; this table gives one row per kind.

| # | earlier contact | what of OV-test it touched | record | status |
|---|---|---|---|---|
| K1 | Memory build and list pinning before the first look (2026-10-22 to 2026-10-25): memory candidates compared with the OV-test images for near-duplicates; annotation keys and image bytes read to pin `ov_test_files.tsv` and the 1,941 list | image bytes, image features, annotation keys | LOG CC-082, CC-083, CC-103a; first-look registration l.84–85; paper `07_disclosures.md` §7.2 | CONTACT WITHOUT REFERENCES OR OUTPUT (no caption used, no model output) |
| K2 | **The first look**, registration of 2026-10-25: `zs`, `ret`, `rand` d0 and `fix` for Qwen2.5-VL-7B and InternVL3-8B (with its verifier passes), batched | all 2,001 images decoded; references scored once; SigLIP2 query vectors (`emb_ov_test.npz`, `644b9200…`), example file and per-image ledgers written | first-look registration; LOG CC-103b, CP-116 (decision file `9bcad498…`) | REGISTERED LOOK (the one look of the first registration) |
| K3 | The group's panel file `data/ktvic_openviic_refs.json` (`4eb02cc4…`), built on 2026-10-12 by `match_openviic.py` before Paper C existed, and the studies that read it (draft §1.2 rows K3-0 to K3e) | references of 636 OV-test files copied into the panel (576 inside the primary 1,941, 60 outside). Through the panel's `test` key the references of 75 OV-test files, all inside the primary, were used as CIDEr-D references and object-class sets (UPE-MBR, knn_prior, four audits; two reads by the scoring kit of a companion paper on 2026-10-22, after Paper C began and before the first look); through the dev300 part of the `train` key the references of the 60 files outside the primary were used in the same ways; one audit read the class sets of 567 files (507 inside the primary) through the whole `train` key; five registrations and the C-PVR copy map used `_pairs` ids only | the scripts, registrations and LOG lines of draft §1.2; ids check `k3_ids_check.py` | REFERENCES USED AS CIDEr-D REFERENCES AND AS CLASS SETS BY SEVERAL STUDIES OF THE GROUP |
| K4 | B-2, registration of 2026-10-28 (external-systems check of Paper B): system K6, a third-party BLIP checkpoint, registered on the OpenViIC test file, 2,001 images and 10,001 references (l.84, l.36) | all 2,001 images decoded once by that checkpoint; its captions scored against the OV-test references; its prediction and score files are kept in the B-2 folders and only aggregate scores were reported (l.20) | LOG OPS-1028c-op (l.566: staging, then JOB STOP at the K5 smoke step, no test image decoded), OPS-1028f-op (first attempt: JOB STOP after 32 s on a truncated file, no prediction written), CC-138c, CC-138d and OPS-1028g (l.582: Amendment 2; restage resumes at K6), **the line B2-LOOK of 2026-10-28T01:08:01Z, "systems scored: K1, K5, K6"** (LOG l.587) (scores file `e1a6e0d8…`); registration l.98 (count gate: the id set must equal the 2,001) and l.174 | DECODED AND SCORED by a third-party system, after the first look. No Paper C number used it. No separate LOG line "dec_K6 OK" was found; the status rests on the B2-LOOK line and on the count gate |
| K5 | Near-duplicate feature passes: `openviic_test.npz` (`f4c79b82…`) built in the MT4 W25-K1 pass and reused by the C-PVR W25 run documents, the Paper B amendment drafts, a VSPS-J draft (marked "hold") and the ViHal set plan | hash and copy-detection features of the 2,001 images; the C-PVR confirm-half near-copy pass (95 out, 886 kept; LOG l.1654, l.1655); 12 OV-test near-copies removed from the ViHal pool (l.2065); the BD-T1 SSCD pass over all 2,001 images (registration draft K5) | LOG CC-193, OPS-1030w25k1c, OPS-1030w25k1e, OPS-1030w25k1f, OPS-1104c; the run documents of `2026-11-02_c_pvr_tier1/` | FEATURE PASS OVER IMAGES (no reference, no caption output) |
| K6 | C-PVR, exploration half (1,020 images): embedded (`emb_openviic_explore`, `3bdb7345…`), decoded by another captioner, and scored against the exploration-half references as the CIDEr guard set | images and references of the exploration half; the parity anchor of the re-keyed exploration vectors read the first look's stored query vectors for these 1,020 images (LOG l.1760; the confirm half was never on that host, l.1733) | C-PVR registration §4.1 (annotation `66af01ba…`); LOG OPS-1107c; paper `06_results.md` §6.9 and `07_disclosures.md` l.22; CC-298 | IMAGES DECODED AND REFERENCES SCORED, exploration half only, development role |
| K7 | C-PVR CIDEr producer loaded the references of the confirm half (981 images) into memory and discarded them unscored | references of the confirm half | CC-298 J3-N6 | REFERENCES LOADED, NOT SCORED |
| K8 | Post hoc near-copy sensitivity (2026-11-10): a counting and pinning pass over the first-look example lists (12 flagged queries; list `pin_c_ov_test_ret_union.txt`, `8c75134e…`), then a post hoc re-score on the stored per-image scores (1,929 queries) | stored example lists and stored per-image scores of the first look; no new decode | LOG CC-199, OPS-1110u-pins, OPS-1111n-posthoc-c1, OPS-1111p-posthoc-result (CC-320); paper `06_results.md` §6.2 | STORED FIRST-LOOK FILES RE-READ, POST HOC |
| K9 | Knowledge of the authors: the first-look numbers and the development attribution rows were known when this registration was written; the margin 1.65 of the rehearsal rule was taken from first-look rows | results | this file | RESULTS KNOWN |
| K10 | The other LOG lines that name OV-test: the 32 lines found by a name search on 2026-11-15 (l.378–380, 386, 398, 418, 429, 547, 557, 818, 911–912, 938–939, 977, 1116, 1446–1447, 1494, 1634, 1654–1655, 1760, 1974, 2059, 2064–2065, 2078, 2105, 2119, 2125, 2629), read in full on 2026-11-16 with l.566, 928, 1294, 1466 and 1606 (CC-438 E3), and a search by file name | list pinning, staging and refusal checks, near-duplicate counts, copy-map counts by ids, text rulings and post hoc rows (draft §1.2 K10) | the LOG lines themselves; `uit-openviic-annotation-test` 0 lines, `openviic.tsv` 0 lines | FULL READ DONE: NO FURTHER DECODE OR SCORING OF OV-TEST AND NO FURTHER READ OF ITS REFERENCES; two contacts found in the read were added to K5 and K6 |
| K11 | Commit-time n-gram leak scanner of the gatekeeper: parses the OpenViIC test annotation (with the other caption corpora) at every commit; counts only, no output, no score (LOG OPS-1111j, l.2100) | the references of all 2,001 OV-test files parsed in memory to count shared 6- and 8-grams with the scanned file | scanner `ngram_scan_cen.py` `926076353d0393fc49b04f82382a6ee4ecb416b62a8436987212abb402f7adf3`, l.15 | REFERENCES PARSED FOR N-GRAM COUNTS, COUNTS ONLY |

Consequences for the design. (a) Version 1 said that OV-test "was looked at once"; with K4 (a third-party system decoded and scored on all 2,001 images) and K3 (OV-test references used as CIDEr-D references and class sets by several studies of the group) the record does not support those words. The wording is now "one registered look in this study", with the table, and the look count is scoped to Paper C. (b) The paper's `07_disclosures.md` §7.2 does not list K3, K4 and K11; the correction text is in the registration draft §7.14 and goes through the paper's text chain (FP-4, recorded yes). (c) No records condition is left for the token: the K3 development part and the full read of K10 are done. (d) The counts-only leak scan of the gatekeeper, including at this registration's own commits, is not the look (rule 8).

**The earlier ruling and ledger line that this look overrules.** CC-298 ruling 7 reads: "The G2 confirm halves (272 / 981), the NoCaps test look and the OpenViVQA-dev look stay unread and unspent." (J2-W6: the ledger keeps the confirm halves unspent.) `PORTFOLIO_3Y_2026-10-29.md` l.191 lists OV-test under "Dev-only (spent)", and l.193 makes C's development, rehearsal and datastore images yield to every other owner. This look also uses the OpenViIC test confirm half (981) that CC-298 ruling 7 kept unspent for C-PVR; that ruling is overruled for C-CONF only under PI-1116a item 3. PORTFOLIO l.191 is overruled for C-CONF only in the same way; l.193 is kept and applied to the carve (Section 4.1). The ledger line that must precede the token, fixed in the registration draft (binding 12): "OV-test (2,001 images; exploration half 1,020 and confirm half 981): moved from 'Dev-only (spent)' to 'C-CONF second look' under PI-1116a item 3 and <LOG id of the answer to FP-1>; CC-298 ruling 7 (with J2-W6) overruled for C-CONF only; no other study uses OV-test in any role until the C-CONF test decision file is logged; after that line OV-test is: looked at twice by Paper C (2026-10-25; C-CONF); also decoded and scored once by the B-2 external check of 2026-10-28 (C-CONF §1.2 K4); no further look by any study." All of this waits for the investigator's answer to FP-1 of CC-438 (Section 9). The 981 confirm-half images were not untouched when CC-298 called them unspent: B-2 had decoded and scored them on 2026-10-28 (K4; LOG l.566, l.582, l.587).

No Vietnamese test set with human references is unused (`REDESIGN_C.md` 1a). The investigator allowed, in principle, one look at an already used test set under a new registration for this one confirmatory test, labelled as such in the paper, with his explicit yes asked again after the rehearsal (PI-1116a item 3).

## 3. Candidate tests

Common to all candidates: greedy decoding, one beam, at most 60 new tokens, **batch size 1**, bfloat16, each model's own chat template; prompts, k, order, tail, memory, near cut and embedder as frozen in C-ATTR-DEV v1.1 §3.1 and §4; score = stripped CIDEr-D × 100 by the registered kit; interval = paired image bootstrap, B = 2,000, `numpy.random.default_rng(0)`, one index matrix per scored set, percentile bounds; one-sided p-like statistic (1 + #{replicate mean ≤ 0}) / (B + 1); smallest effect of interest **+2.0** points (the registered value of the paper); labels DETECTED, REVERSED, NEGLIGIBLE, UNRESOLVED as in C-ATTR-DEV v1.1 §7.4. Seeds: `rand` draw d from `paperC|rand|<set>|<image id>` with `d<d>` appended for d ≥ 1; `perm` from Sattolo's algorithm seeded by the set name and p. Draw d0 on OV-test is therefore the same list as in the first look.

### T1. Confirmatory test of the attribution split (benchmark item 4)

- **Registered hypothesis.** H_pair(m), for m in {Qwen2.5-VL-7B, InternVL3-8B at τ = −∞, Aya-Vision-8B}: on OV-test, the retrieval-specific effect needs the list retrieved for this image.
- **Estimand.** τ_pair(m) = mean over the 1,941 primary images of [s_i(`ret`) − mean over D = 2 permutations of s_i(`perm`)].
- **Contrast.** `ret` against `perm` p1, p2, same backbone, same host, same k, order and tail.
- **Pass rule.** τ_pair(m) is DETECTED: point ≥ +2.0 and p-like statistic ≤ the Holm step-down threshold at family-wise one-sided 0.025 over the claims that entered the test family.
- **Companion rows (no gate).** τ_marg(m) = mean [`perm` − `rand`], R = 3 draws, with the NEGLIGIBLE label (90% interval inside ±2.0); τ_sel and τ_any.
- **PASS lets the paper say:** the pairing component, nominated on one development set and held on a second, was confirmed on the test set under a second registration, at batch size 1, for the named backbones (for Qwen2.5-VL-7B and InternVL3-8B, a split of a retrieval contrast already known from the first look); the split moves from "development only" into the contributions, with the second-look label on every row. "Confirmed" and "confirmatory" are used for these rows only.
- **FAIL lets the paper say:** the development split did not hold at test for the named backbone; the split stays a development description; the registered FAIL is printed in the main text.

### T2. Batch-size-1 repeat of a registered contrast (benchmark item 5)

- **Registered hypothesis.** The registered `ret` − `rand` contrast of the first look is reproduced when every image is decoded alone, on another machine and software stack, with three random draws. The comparison with the first look does not isolate batch size: host, stack and session change with it.
- **Estimands.** (i) τ_sel(m) at batch size 1 with R = 3 draws on the 1,941; (ii) Δ_batch(m) = mean_i {[s_i(`ret`) − s_i(`rand` d0)] at batch size 1 − [the same difference in the stored first-look decodes]}.
- **Pass rule.** (i) DETECTED (point ≥ +2.0, p-like ≤ 0.025); (ii) NEGLIGIBLE (90% interval inside ±2.0).
- **An exact repeat exists only for Qwen2.5-VL-7B** (registered row P1b, τ = −∞) and for InternVL3-8B's registered secondary at τ = −∞ (`06::Table 9`). The pooled primary P1 used InternVL3-8B with the deletion step at τ = 0.10, which needs the verifier passes; repeating it adds a second model pass per caption and the fall-back to the zero-shot caption. I do not propose that part: the deletion step is a registered negative of the paper and is out of its claims.
- **PASS lets the paper say:** the registered per-backbone result was reproduced one image at a time with three random draws, and "decoding one image at a time on another machine and software stack changed the registered contrast by less than 2.0 points in either direction". **FAIL:** the interval of Δ_batch is printed as the measured difference between the two runs on the registered contrast; no registered number changes. The narrower reading about batch size alone would need a registered cross-host parity check on stored batched items; none is registered. S-batch reads only the first look's per-image score ledger and asserts from records that the scorer, the document-frequency set and the references equal those of C-CONF; otherwise it is NOT RUN (registration draft §6.4a, §7.7).
- Limit: T2 alone moves only the reliability criterion.

### T3. Both from one decode session (recommended)

The arms of T1 are `zs`, `ret`, `rand` d0 to d2, `perm` p1, p2. The arms of T2 are `ret`, `rand` d0 to d2. T3 decodes the T1 arms once and registers:

- **one family with a gate:** F1 = {H_pair(m)} of T1, Holm at one-sided 0.025;
- **named secondaries, each with its rule fixed and each labelled "secondary, no family-wise error control":** S-marg(m) (τ_marg label); S-rep(m) (τ_sel at batch size 1, R = 3; for Qwen2.5-VL-7B this is the repeat of registered row P1b); S-batch(m) for the two backbones of the first look (Δ_batch with its label and the reading of T2); S-bb (Aya-Vision-8B's τ_sel on OV-test: first decode of this system on the OpenViIC test set; its only earlier test-set decode is the Flickr30K look of Section 8.6). None of them is called confirmed or confirmatory. A secondary enters the abstract or the contributions only with its label, and S-bb never enters the abstract;
- **two controls of the procedure itself, also labelled "secondary, no family-wise error control":** a positive control (the LMCap re-implementation's τ_sel must be DETECTED, as on OV-dev-B; first decode of this system on the OpenViIC test set; its only earlier test-set decode is the Flickr30K look of Section 8.6) and placebo rows (`rand` d1 − d2 and `perm` p1 − p2 per backbone, flagged when |point| ≥ 2.0 and the 95% interval excludes 0). A flag changes no label, verdict or sentence; the flagged rows are printed with the flag; a judge read may add wording only. The positive control is never dropped under a compute cap, and a positive control that is not complete counts as NOT DETECTED (Section 7, rule 7).

The controls matter for the rubric as much as the family does. Criterion C5 at level 2 reads "a proposed procedure whose own test failed or was not run". For a measurement procedure the "own test" is a case with a known answer and a case with no effect, not the sign of the effect it measures. With both controls on the test set, a FAIL of an H_pair claim is a finding of the procedure, not a failure of it.

### T4. A first look at an English set never used (not recommended)

VizWiz-Captions val (about 7,750 images, chưa kiểm) with the COCO memory would be a true first look. The queries are outside the memory's source, where the paper's contrasts were small or not detected (NoCaps val S-NC FAIL, +1.73 [0.94, 2.50], LOG CEN-NOCAPS; XM-dev500 τ_pair UNRESOLVED for two of three backbones, `11::Table S21`). A split of a sum that is itself near the threshold is unlikely to reach the rehearsal bar (Section 4.2). The licence is not verified, and `Li2024RetrievalRobustness` already ran a reassigned-caption control on VizWiz with a trained captioner (`REDESIGN_C.md` short answer). My probability of a DETECTED τ_pair there for Qwen2.5-VL-7B: about 35 percent. Not proposed.

### Why not more backbones outside the Qwen line

The benchmark's item 4 mentions the block-2 backbones. Each needs a licence gate or pins, a Vietnamese check and a configuration choice on KTVIC dev299, and none has a development row. Adding one would put an untested system into a test look. Aya-Vision-8B already is a backbone outside the Qwen line with a frozen configuration and development rows; C-CONF uses it and adds no other.

## 4. Data, tiers and probabilities

### 4.1 Which data plays which role

| tier | data | status |
|---|---|---|
| 1, exploration | everything of Section 2: OV-dev-A, OV-dev-B, XM-dev500 (batched and batch-size-1 rows), KTVIC dev299 (configuration choice) | read; closed for tuning at the registration commit |
| 2, rehearsal | **OV-carve: 2,000 OpenViIC training images**, the first 2,000 of a seeded order over the pool. The pool is the 5,926 memory clusters that hold exactly one image and only an OpenViIC image (count from `lists.json::memory`, ids only; repeated by judge J3), minus: (i) every OpenViIC file with a KTVIC copy in the `_pairs` ids of `data/ktvic_openviic_refs.json` (this removes `00000001628.jpg`: 5,926 → 5,925); (ii), an assert after the draw and not a pool exclusion: no carve cluster is one of the N = 3 LMCap fixed-shot clusters of the `ov_carve` draw or a fixed-shot cluster of any arm of the study; (iii) every id match or W25 C1–C3 near-copy of another owner's set (the ViHal pool, survivors and removed list, BD-T1 with its keys H and T2, KTVIC dev300, and every list of the owners register `c_pvr_owners.json` (for the near-copy part only the KTVIC and OpenViIC-dev owners named in registration draft §5.1 (iii); no test-set image, cache or vector reaches the rehearsal host)), as PORTFOLIO l.193 requires. Paper B's H-500 is dropped as a separate owner (PI-1101p, LOG l.1083; PI-1103aa, l.1433; CC-314, l.2059): no H-500 list exists on record, and the images the name now stands for, the 739 ids of BD-T1 H and T2, stay excluded through BD-T1. Block 0 prints each count and asserts zero overlap. Each image is used as a query with its own cluster removed from every list, LMCap retrieval, shots and re-rank inputs included. References: its OpenViIC training captions as released | never decoded or scored as a query by any Paper C study. Used otherwise: the memory has shown these captions as examples to other images; OpenViIC training images are in the training pool of the MT4 K1 fine-tuning study and in the D-VI datastore of the C-PVR study (both disclosed; block 0 prints the counts for the carve) |
| 3, test | OV-test, primary 1,941 and full 2,001, the pinned lists of the first look (`ov_test_files.tsv` 99d4fc49…, `ov_test_primary1941.txt` 6458295e…) | second look; history in Section 2 |

Why a carve of training images and not fresh draws on OV-dev-A or OV-dev-B: on those two sets the `ret` side of every contrast is already known per image, so new `perm` and `rand` draws would mostly repeat a number that the exploration read. The carve is the only in-source Vietnamese data whose queries no Paper C study has decoded or scored. **Correction of version 1:** it does not follow a precedent of the project. In the registration of 2026-10-30 the Flickr30K carve of 1,000 training images was tier 1 (exploration) and Flickr30K val was the rehearsal (`c_t2` PREREG l.15, l.25); a training carve as the rehearsal set is a new choice, which the panel rules on. Its weaknesses, stated now: the references are training captions whose count per image I did not check (chưa kiểm; block 0 prints the count distribution beside OV-test's); training images may lie nearer to the memory than test images do; the memory minus one cluster is not the memory of the test; and the population differs, because the carve leaves out every OpenViIC image that has a KTVIC copy or shares a memory cluster, while OV-test has no such filter (block 0 prints the shares from ids only). For these reasons the rehearsal bar carries a fixed margin for the drop from development to test (below).

How exclusion (ii) is made well defined: the LMCap shot draw (`c_t1.py` l.300–303) takes clusters below the near cut for every query, so it needs the carve first. The carve is drawn; the shots are then drawn with no own-cluster masking, so a carve query's own cluster (cosine about 1) cannot be a shot; the code asserts it, a self-test checks that no carve query's cluster appears in LMCap retrieval, shots or re-rank inputs, and two mutants ("own cluster kept in `lmcap_ri`", "shot cluster admitted to the pool") must be killed. The seeded order of the pool is built from ids only; its sha256 is not computed yet, because it needs one ids-only run of the order builder, which FP-7 lets be drafted and no ruling lets be run (registration draft §5.1 and Q18).

The carve has 2,000 images so that the rehearsal runs at the size of the test: its bootstrap replicates of size 1,941 have the noise of the test, and the session measures the real decode time.

### 4.2 The rehearsal bar (fixed before any carve decode)

For each claim H_pair(m), on the carve:

1. **Carve PASS:** τ_pair(m) DETECTED under the registered rule, Holm over the claims whose backbone completed the rehearsal block (three if all completed).
2. **Share of replicates (the skill's definition of P(PASS)):** B = 2,000 resamples of size 1,941 drawn with replacement from the 2,000 carve images, `default_rng(1)`, one index matrix for all claims. A replicate passes for claim m when its mean is ≥ +2.0 and its mean divided by SE_m is ≥ 2.394, where SE_m = (SD of the carve's per-image differences) / √1,941 and 2.394 = Φ⁻¹(1 − 0.025/3), the strictest Holm step. P_m = the share of passing replicates; **P_m ≥ 0.98**.
3. **Margin for the drop from development to test:** the carve point of τ_pair(m) is ≥ **+3.65** = 2.0 + 1.65. The value 1.65 is the largest drop from OV-dev-B to OV-test among the paper's registered per-backbone `ret` − `rand` rows without deletion: InternVL3-8B +5.36 to +3.71; Qwen2.5-VL-7B +9.67 to +8.33, a drop of 1.34 (Section 2). Provenance, stated in the registration and in the paper: the value 1.65 was taken from first-look test rows of OV-test (06 Tables 7 and 9 against v1.1 l.35); it is fixed and disclosed, and it is not an estimate made on rehearsal data. So one constant of the rehearsal rule comes from the first look at the test set that the rehearsal guards.

A claim enters the test family only if 1, 2 and 3 hold. A backbone whose claim does not enter is not decoded on OV-test. The test look takes place only if H_pair(Qwen2.5-VL-7B) enters, the positive control is DETECTED on the carve (not complete counts as NOT DETECTED), the test-side inputs pass the check of the registration draft §6.4a, the ledger line of Section 2 is written (FP-1), and the investigator's explicit yes is in the LOG with the sha256 of the rehearsal decision file (FP-3). Nothing is retuned after the rehearsal: no arm, list, seed, k, prompt, threshold or rule.

**What the bar is, restated.** P_m is a share of bootstrap replicates of the rehearsal data that pass the test rule at the test's size. It is not the probability that the claim passes at test, and it cannot be compared with the predictive probabilities of Section 4.3. The bar 0.98 is the project's fixed three-tier rule, and holding to it is a choice of risk: a claim whose rehearsal evidence is not this stable is not allowed to spend a test look. The margin of item 3 is a second, separate allowance for the change from the rehearsal population to the test population.

### 4.3 Probabilities (my opinion; the reasoning as factors)

Planning standard errors at the size of the test, my arithmetic from the half-widths of `06::Table 16` scaled by √(925/1,941): τ_pair 0.65, 0.59, 0.52; τ_marg 0.34, 0.37, 0.33 (Qwen2.5-VL-7B, InternVL3-8B, Aya-Vision-8B).

**Power statement for the primary (fixed with the design).** With these standard errors the chance that τ_pair is DETECTED is 0.50 at a true +2.0, about 0.94 to 0.97 at +3.0, and above 0.99 at +4.0. The point condition binds; the Holm condition is weaker (2.394 × 0.65 = 1.56 < 2.0).

Factor A, the rehearsal reaches the bar, per claim. The binding condition is the margin +3.65. I take the carve's true value as the development value with an extra spread of 1.0 point for the change of population.

| claim | development values (`06::Tables 15, 16`) | my P(carve point ≥ 3.65) |
|---|---|---|
| H_pair(Qwen2.5-VL-7B) | +7.43, +7.30 | 0.99 |
| H_pair(InternVL3-8B) | +4.96, +5.57 | 0.92 |
| H_pair(Aya-Vision-8B) | +6.78 (one set; its placebo flag concerns `rand`, which τ_pair does not contain) | 0.98 |

Factor B, the gates before and during the rehearsal hold (list parity, refill share of `perm` on the carve at most 0.10, D1 on new hosts, scoring parity, the gated download of one model, inputs fetched and hashed, a pool of at least 2,000 after the exclusions, the zero-overlap and shot asserts): **0.80 to 0.85** (version 1 said 0.90; CC-436 NB-1). The refill share on the carve is unknown; on the development sets it stayed inside the gate (`11::Table S26`).

- All three claims enter: 0.99 × 0.92 × 0.98 × (0.80 to 0.85) = **0.71 to 0.76**.
- The look takes place (Qwen2.5-VL-7B enters, gates hold), before the investigator's decisions FP-1 and FP-3: 0.99 × (0.80 to 0.85) = **0.79 to 0.84**.

Factor C, a claim that entered passes at test.

| claim | reasoning | my P |
|---|---|---|
| H_pair(Qwen2.5-VL-7B) | the sum is known on the same images: +8.33 [7.01, 9.76] (`06::Table 7`); τ_marg in development was between −0.06 and +0.96; so τ_pair near +7 to +8 against a bar of +2.0 | 0.995 |
| H_pair(InternVL3-8B) | the sum is known on the same images: +3.71 [2.29, 5.14] (`06::Table 9`); τ_marg in development −1.43 and −0.35; so τ_pair near +4.5, about four standard errors above +2.0 | 0.99 |
| H_pair(Aya-Vision-8B) | nothing known on this set; development +6.78; with the drops of 1.3 to 1.7 seen for the other two, about +5; spread about 1.4 | 0.98 |

- All three pass, given all three entered: about 0.97. **All three pass, unconditional on the rehearsal: (0.71 to 0.76) × 0.97 = 0.69 to 0.74.** This is a predictive probability about the test, not a P_m share.
- At least two pass with Qwen2.5-VL-7B among them (the gate for moving the split into the contributions, Section 7): about **0.77 to 0.82** (my arithmetic: the 0.87 of version 1 scaled by the new factor B).

Secondaries (given the look):

| row | reasoning | my P |
|---|---|---|
| S-marg NEGLIGIBLE for all three | needs each point inside about ±1.4; predictive from the development values with both standard errors: 0.94, 0.87, 0.94 | 0.77 |
| the full pattern (τ_pair DETECTED and τ_marg NEGLIGIBLE) for all three | product with the line above | about 0.60 |
| S-rep(Qwen2.5-VL-7B) DETECTED | sum +8.33 on the same images | 0.995 |
| S-batch(Qwen2.5-VL-7B) NEGLIGIBLE | development: batched +9.25 against +8.27 at batch size 1 on OV-dev-B, +8.00 against +7.37 on OV-dev-A (`11::Table S22`, `06::Tables 15, 16`); a difference near −0.8; its standard error was never computed (chưa đo) | about 0.70 |
| S-bb, Aya-Vision-8B τ_sel DETECTED on OV-test | development +6.25 [4.87, 7.69], placebo flagged | 0.95 |
| positive control DETECTED | development +16.92 | 0.99 |

The weakest link is not statistical. It is whether the investigator answers FP-1 and FP-3 with yes, whether the panel accepts a carve of training images as the rehearsal set, whether a fault after step T0 spends the look without a row (Section 7, rule 8), and whether a reader accepts a confirmation whose sum was known for two of three backbones on a test set with the contact history of Section 2.

## 5. Compute, days and storage

### 5.1 GPU-hours

Rates: the planning rates of C-ATTR-DEV v1.1 §6.1 (0.80, 1.40 and 1.60 seconds per caption for Qwen2.5-VL-7B, InternVL3-8B and Aya-Vision-8B; 1.14 for LMCap). They held at batch size 1: block 1b projected 12.8 GPU-hours at these rates and used 12.27 (`06::Section 6.10.1`; addendum v1.2 V7).

| session | captions | GPU-hours at planning rates | hard cap |
|---|---|---|---|
| rehearsal on OV-carve: 3 backbones × 7 runs × 2,000, LMCap 3 × 2,000, D1 400 | 48,400 | 14.8 + 1.9 + 0.1 = **16.8** | min(30, 1.5 × the projection from the D1 rates) |
| test on OV-test: 3 backbones × 7 runs × 2,001, LMCap 3 × 2,001, D1 400 | 48,424 | 14.8 + 1.9 + 0.1 = **16.8** | the same form |
| total | 96,824 | **33.6** | about 50 |

Scoring is CPU work and runs on the rented host (the investigator's rule of 2026-11-11: tests and scoring on the rented machine).

### 5.2 Wall-clock

Set-up of a fresh host: about 4 hours (the figure used by the project's idle rule). The host is deleted between the two sessions, because the wait for the rehearsal read and the investigator's decision is longer than a set-up.

| | one 24 GB machine | two 24 GB machines |
|---|---|---|
| rehearsal session | 4 + 17 = about 21 h | 4 + 10 = about 14 h (one machine takes InternVL3-8B and LMCap, 7.3 h; the other Qwen2.5-VL-7B and Aya-Vision-8B, 9.3 h; every arm of a backbone on one machine) |
| test session | about 21 h | about 14 h |
| the two sessions | about 1.8 days of machine time | about 1.2 days |

### 5.3 What must be stored where

State of custody on 2026-11-16. The research data of the laptop's former home folders is on the investigator's cloud drive, in the folder `vsps_research_data`, as one tar archive per former home folder with a per-file sha256 list beside each (PI-1115w); the local copies of the lists are in `.session_backup/2026-11-16/drive_upload/`, and the former local folders no longer exist. **Version 1 was wrong to say that the laptop keeps no copy:** the host backups under `.session_backup/machines/` remain, and by their listing they hold every stored first-look file that C-CONF needs; the data folder of the run repository holds the OpenViIC images and annotation files. Rules: **no drive credential on a rented host**; inputs reach a host only as individually named files, each extracted on the laptop if it sits in an archive, and each checked against the `drive_upload` list and its sha256 of record; **no archive that holds any OV-test, held or label file reaches a host**; **no OV-test-derived byte reaches a host before the token**; outputs are pulled by the laptop after the job has ended and checked against the host's list. Before the token every test-side input is checked for existence and against its sha256 of record from record files and listings only (registration draft §6.4a; on 2026-11-15 all were found and equal, so no fallback row is declared NOT RUN at this draft).

| item | source | on the host |
|---|---|---|
| model snapshots (three backbones, SigLIP2, XGLM-2.9B, multilingual CLIP) | the public hub at the pinned revisions; token from standard input only | both sessions |
| OpenViIC training images of the carve (2,000) and annotation file of the training split | the drive copy or the data set's public source, sha256 against `lists.json` | rehearsal |
| memory caption store and memory vectors (`c_stage1/emb.npz` 59e65f6f…) | the drive; the store can be rebuilt on the host from the training annotation | both |
| OV-test images (2,001) | the data folder of the run repository, each file against its sha256 in `ov_test_files.tsv` (`99d4fc49…`) | test session only, after the token |
| OV-test query vectors of the first look (`emb_ov_test.npz`, `644b9200…`) and its example-id file (`ex_ov_test.json`, `4b33f1ab…`) | host backups M3 and M1 (hashes equal on 2026-11-15) | test session only; staging them under the token is the start of the look. No SigLIP2 pass over OV-test is made |
| OV-test annotation file (references; `66af01ba…`, the sha256 in the first look's host record) | the data folder of the run repository | test session only, for scoring; deleted after the verified pull |
| stored first-look per-image score ledger of OV-test for S-batch (`ledger_ov_test_1941.jsonl`, `50878193…`; the 2,001 ledger `5e04d267…`) | host backups M3 and M1 | test session only, at scoring; if missing or unequal at the registration commit, S-batch is declared NOT RUN there |
| stored batch-size-1 `ret` run of Qwen2.5-VL-7B on OV-dev-B (`f7298a01…`) with its per-image scores (scoring parity gate; D1 reference) | host backup of the attribution study | both |
| outputs (captions, ledgers) | host → laptop → drive; never committed | – |
| decision files (ids and numbers only), lists (ids only), run records | committed through the gatekeeper | – |

## 6. Rubric gain per criterion (my opinion; the benchmark agent decides)

Anchors quoted from `RUBRIC_v1.md` section 3. Present levels from `C_BENCHMARK_2026-11-15.md` section 2.

### 6.1 If the claims pass (all three, controls met, the repeat row DETECTED)

| criterion | now → then | anchor of the higher level | points | my P that the evaluator moves it | why it may not move |
|---|---|---|---|---|---|
| C5 proposed method | 3 → 4 | "a clearly specified method with a justified design, compared with suitable baselines or alternatives; its parts are tested at least in part" | +2.0 | about 0.5 (CC-438 ruling 6; version 2 said 0.65) | the anchor of level 3 includes "a modest adaptation of a known method", and the reassigned-list arm is published |
| C2 novelty | 3 → 4 | "a clear new element beyond the closest read works, differentiated from full texts; no read work already does the same" | +2.4 | 0.30 | three blind scorers gave novelty 3 of 5 to the best case of this study on 2026-11-11 (LOG OPS-1112k); a test-set confirmation changes the evidence, not the element |
| C7 reliability | 4 → 5 | "repeated runs or seeds where training or sampling is involved … robustness checks" | +2.8 | 0.60 | the repeat covers one of five test sets and one registered row exactly |
| C6 design | 4 → 5 | "hypotheses, primary outcome, sample size or power reasoning and analysis plan fixed before the data were seen" | +2.4 | 0.15 | the pooled estimand of the first look and the untested Flickr30K claims stay |
| C4 theory | 4 → 5 | "a formal result (… identification argument, or a derived property) that the experiments then test, with assumptions stated" | +1.2 | 0.15 | the split is an identity, not a theorem |

Expected gain, **unconditional: about +2.6 to +2.7** (CC-438 ruling 6: J1 N10, J2 N7, J3 N8). Version 2 gave +3.7 conditional on all claims passing (1.3 + 0.7 + 1.7, with P(C5 moves) 0.65) and +2.9 unconditional (CC-436 NB-1); the panel's figures replace both. Version-2 figures, computed with P(C5 moves) 0.65 and not revised by the panel: at least one of the three moves with probability about 0.85 to 0.90 given that the claims pass; two or more with about 0.53. The benchmark's +4.4 is the case where C5 and C2 both move; I give that about 0.25.

Arithmetic for the gate of 80. The benchmark puts the text work without a new run at 78.8. From there any one of the three rows is enough (the smallest is +2.0). If the text work delivers less than its +6.0 (the deposit with a DOI and the cut are not done yet), two rows are needed.

**The probability of reaching 80 with C-CONF and the text work, as the panel rules it: about 0.30. It is less likely than not** (CC-438 ruling 6, J1, J2 and J3; CC-436 gave 0.25 to 0.40; my version-1 figure of 0.45 was optimistic and is withdrawn). The factors:

1. the text work must be credited in full (+6.0, to 78.8), with the deposit and the cut still open;
2. the look must take place: the gates of the rehearsal, the exclusions of the pool, the input check, and the investigator's answers to FP-1 and FP-3;
3. no fault after step T0 may spend the look without rows;
4. the evaluator must move at least one criterion; **the main lever is C7 (reliability) through S-rep and S-batch**, which are secondary rows, and S-batch no longer reads as a statement about batch size alone;
5. C2 (novelty) is unlikely to move, because the reassigned-list arm is published;
6. the downside (CC-436 NB-9): a registered FAIL weakens Strength 1 of the benchmark (l.93) and the evidence for H3 (l.81), and the chance that C6 falls from 4 to 3 is about 0.1.

One decomposition of version 2, my arithmetic and not a panel figure (the panel's figure is about 0.30): 0.6 (text work credited in full) × 0.8 (the look takes place and yields rows) × 0.7 (at least one criterion moves) = about 0.34.

It remains the only registered route above the text-only ceiling of about 78.8; cost is not a factor (the investigator's rule of 2026-11-10); a clean FAIL also scores under C7. The request for the investigator's yes after the rehearsal carries a fresh benchmark re-score made after the Paper C text chain (resumed 2026-11-17; freeze line OPS-1117a written at 2026-11-17T15:31:53Z; the C2 transfer is pending its commit, LOG OPS-1117b) and this arithmetic (CC-436 NB-12, carried by CC-438 N14). Without C-CONF it is the benchmark's 78.8 at best.

**A parallel route is a condition (PI-1115t; CC-438 ruling 6, N10).** C-CONF must not displace a method or novelty route for Paper C. The coordinator recorded FP-5 as conditional on such a route running in parallel and found none (LOG OPS-1115cm-cc438: D3 about 12%, D1 about 8%, M1 published); it is brought to the investigator as the direction item. This design does not supply that route.

### 6.2 If a registered claim fails at test

| criterion | effect | anchor |
|---|---|---|
| C5 | stays 3 when both controls are met: the procedure was tested and returned a negative finding. Falls to 2 only if the positive control fails | level 2: "a proposed procedure whose own test failed or was not run" |
| C2 | stays 3 | – |
| C7 | 4 → 5 still possible through the repeat rows (my P 0.5) | "A statistically clean null or negative result is reliable evidence and is scored here by the same anchors as a positive one" |
| C8 | stays 3 | – |
| H1 honesty | stays PASS: the FAIL is printed in the main text beside its rule | – |

### 6.3 If the rehearsal does not reach its bar

No test look. The carve rows are development rows. No criterion moves; about 17 GPU-hours are spent. The paper states that the rehearsal did not reach its bar and that OV-test was not looked at a second time.

## 7. Recommendation, calendar and stop rules

**Run T3.** One family (the three H_pair claims), named secondaries, two controls, one rehearsal on OV-carve, one look at OV-test.

What each outcome lets the paper do, fixed now:

| H_pair claims that pass at test | sentence | where the split may appear |
|---|---|---|
| Qwen2.5-VL-7B and at least one more | "under a second registration and at batch size 1, the pairing component of the retrieval contrast was detected on the OpenViIC test set for <backbones> (for Qwen2.5-VL-7B and InternVL3-8B, a split of a retrieval contrast already known from the first look)" | contributions and abstract, with the words "second look" |
| Qwen2.5-VL-7B not, two others pass | "the pairing component was detected for <backbones> and not for Qwen2.5-VL-7B, the primary backbone" | Section 6.10 and the limitations only |
| exactly one | "… was detected for <backbone> and not for <backbones>" | Section 6.10 and the limitations only |
| none | "FAIL: the split nominated in development was not confirmed on the OpenViIC test set" | Section 6.10 and the limitations; the development rows keep their label |

Calendar (Vietnam time; each step waits for the one before it):

| date | step |
|---|---|
| 11-16 | round 1 ruled (CC-436, NEXT_ROUND); round 2 ruled (CC-438, NEXT_ROUND, median 82) |
| 11-17 / 11-18 | version 3 of the design and draft v0.3 of the registration, with the diffs and `C_CONFIRM_CC438_RESPONSES.md`, to round 3, the last: a full three-judge panel, the outside reader recorded NOT RUN (FP-8, recorded yes); ESCALATE_TO_PI if no GO. Code and self-tests drafted on synthetic fixtures in parallel (FP-7); after a GO, self-tests and mutants on a rented host. Every later row moves by the days this takes; the freeze of 11-27 does not move |
| 11-18 | one-judge code read; registration commit through the gatekeeper; block 0 (lists, parity gate, refill gate, carve diagnostics) |
| 11-19 | rehearsal decode on two machines; pull and hash check |
| 11-20 | rehearsal scored once; decision file hashed and logged; one-judge read; the investigator is asked for his yes with the rehearsal numbers |
| 11-21 | after his yes: test decode; pull and hash check |
| 11-22 | test scored once; result read by the panel |
| 11-23 to 11-24 | text package for the paper; re-score by the benchmark agent |

The Paper C text chain (resumed 2026-11-17; freeze line OPS-1117a at 2026-11-17T15:31:53Z; C2 transfer pending its commit) is not touched by any C-CONF step. The correction of FP-4 (disclosures and one-look sentences) goes into the next Paper C text package, built on the post-chain HEAD, whatever C-CONF does; only its second-look clause waits for the C-CONF test decision file.

Stop rules:

1. The panel does not reach GO in three rounds: to the investigator.
2. List parity fails, or the refill share on the carve is above 0.10: STOP at block 0, before any GPU step; back to the judge.
3. D1 fails for a backbone on a host: that backbone leaves the study; if it is Qwen2.5-VL-7B, the study stops.
4. The positive control is not DETECTED on the carve, or is not complete (which counts as NOT DETECTED): no test look.
5. H_pair(Qwen2.5-VL-7B) does not enter the test family: no test look; the carve rows are reported as development rows.
6. No token without all of: the explicit yes of the investigator in the LOG with the sha256 of the rehearsal decision (FP-3); the ledger line that moves OV-test to "C-CONF second look" (FP-1); every test-side input found and equal to its sha256 of record (no records condition remains open at the token). Without the token no OV-test-derived byte is staged, decoded or scored, and no feature pass runs over OV-test.
7. Compute cap. The hard cap of a session is min(30, 1.5 × the projection from the D1 rates) GPU-hours; in the test session it is computed and logged before T0 (rule 8). LMCap is never dropped; under a binding cap Aya-Vision-8B is dropped first, then InternVL3-8B; a positive control that is not complete counts as NOT DETECTED (rehearsal: no look; test: registration draft §7.12). Qwen2.5-VL-7B is never dropped either. The positive control therefore runs before the two backbones that may be dropped. No backbone is ever run in part on OV-test.
8. **When the look begins (one rule, the same words as the registration draft §6.5 and its Q5).** The second look begins at step T0, when the first OV-test-derived byte (image, vector, list, record, or the first look's example file or ledger) is staged on a host under the token; any stop, crash or partial file after that point is the look and is reported (its rows NOT RUN). There is no third look. The query vectors of OV-test come from the first look's stored file `emb_ov_test.npz` (sha256 `644b9200b5237df6bea8803a6d2b3ecbe0a15f443a647f48dad1411e262d7ebf`; LOG OPS-1107c); no SigLIP2 pass over OV-test is made before T0, and none after it. In the numbering of the registration draft: On the test host the order is: set-up; T.0 (D1 on the 50 OV-dev-B items); the cap P of §10.2 computed and logged; the scoring parity gate of §7.1 on the stored OV-dev-B run; the dry run of step 0.4; only then T0. No OV-test byte is staged until all of them pass. A stop before T0 spends no look; the host is replaced once under the same token, or the study returns to the judge. The parity gate is repeated at scoring (registration draft §6.5, §7.11). The counts-only leak scan of the gatekeeper, including at this registration's own commits, is not the look.
9. Freeze: every step not finished by 2026-11-27 18:00 (UTC+7) is NOT RUN.

## 8. Side study: the zero-GPU check of direction D3 (development only, one page)

**Question.** Direction D3 of `C_DIRECTIONS_FROM_OBSERVATIONS_2026-11-16.md` (section 6.3) says that example images help only when the neighbours are far. Its cheapest check: does the image-caption format beat the text format for Qwen2.5-VL-7B on XM-dev500 (queries outside the memory's source)?

**Data.** Two sets of per-image scores that already exist, both at batch size 1: `ret_img` of block 3 and text `ret` of block 1b, on XM-dev500 (500) and OV-dev-B (925). No decode, no GPU. The paper declined to compute this difference because it was not registered and the two runs came from different machines (`06::Section 6.10.8`).

**Estimand and rule.** Δ_fmt(set) = mean_i [s_i(`ret_img`) − s_i(`ret`)], paired bootstrap as in Section 3, labels of C-ATTR-DEV §7.4. Fixed reading: on XM-dev500, a point below +2.0 stops D3 for Vietnamese; a point of +2.0 or more keeps D3 open and proves nothing, because at 500 images the interval is near ±3 points and DETECTED needs about +6. On OV-dev-B the batched value of this difference is known (−0.53 [−2.39, 1.32], `11::Table S19` note), so that row is a batch-size-1 re-read of a known number.

**What it needs.** One registered line (an addendum to the development registration, label `DEVELOPMENT / C-ATTR-DEV, NON-CONFIRMATORY; cross-host contrast`), a one-judge read, one function with a self-test (planted difference recovered; ids of the two runs asserted equal) and one mutant (unpaired difference), a few CPU minutes on the rehearsal host in its block-0 slot, the two ledgers fetched from the drive.

**What it can and cannot do.** It can stop D3. It cannot confirm it, and it adds no rubric point by itself. My probability that the XM-dev500 point is at least +2.0: about 20 percent (the direction note's figure).

**Priority.** It rides on the rehearsal session and is dropped at the first friction (a missing ledger, a judge question). It never delays C-CONF and shares no rule, family or file with it.

## 9. Decisions only the investigator can take

As they stand after CC-438 (its questions FP-1 to FP-8) and the coordinator's record of them (LOG OPS-1115cm-cc438, 2026-11-16T00:05:46Z, applied under PI-1116g). Confidence figures are the panel's.

| question | state | default while unanswered |
|---|---|---|
| **FP-1.** May the second look use all 2,001 OV-test images, including the 981 that CC-298 called unspent (B-2 K6 had already decoded and scored them on 2026-10-28)? | recommended YES (85); **reserved to him, asked at look time** | **no token is written** |
| **FP-2.** Does the gated claim stay τ_pair alone, with the τ_marg count and the known-contrast caveat printed beside it? | **recorded yes** (78) | τ_pair alone |
| **FP-3.** After a passing rehearsal (Qwen2.5-VL-7B entered, positive control DETECTED), the one yes for the second look, with a fresh benchmark re-score and the P(80) arithmetic attached | recommended YES (80); **reserved to him** | **no look** |
| **FP-4.** Paper C's disclosures corrected in the next text package whatever C-CONF does (K3, K4, K11; "once" -> "once under its first registration", including `02_related_work` l.62 and l.66), the second-look clause only after a test decision file | **recorded yes** (90), built on the post-chain HEAD | yes, through the text chain |
| **FP-5.** Go ahead knowing P(80) is about 0.30, the gain is reliability (C7) rather than novelty, and this is the last use of OV-test? | recommended YES (72) with a method or novelty route running in parallel (PI-1115t); **conditional**: no such route exists (Section 6.1); brought to him as the direction item | code only, nothing spent |
| **FP-6.** Top-up of about 300k VND before the rehearsal rental? About 390k-520k VND is needed against a balance of about 362k (CC-438 N11). | recommended YES (85); **asked only if a rehearsal is licensed** | not asked yet |
| **FP-7.** Code and self-tests drafted now on synthetic fixtures, in parallel with the round-3 text, with the E4 step order built into the job script | **recorded yes** (82); no study data, no host run, no token, no commit before a GO | not started |
| **FP-8.** Round 3 with the outside reader recorded NOT RUN (Codex unavailable until 2026-11-27) | **recorded yes** (80); scored as not run, not as a failure | round 3 retries Codex |

New facts for his answers to FP-1, FP-3 and FP-5, from the records checks of Section 2: OV-test was also decoded and scored once by a third-party system for Paper B (row K4); the references of OV-test images were used as CIDEr-D references and class sets by several studies of the group (row K3); and the gatekeeper's leak scan parses the test annotation at every commit (row K11). None touched a Paper C number, but all must be printed in the paper.

The version-1 items, kept for the record with their state:

1. **The second look at OV-test, after the rehearsal**: now FP-3 above (and FP-1 before it).
2. **Whether the batch-size-1 repeat and the controls may ride on the same look.** Upheld by the panel (CC-436 ruling 1) on the condition that only the one family is confirmatory and every other row is labelled "secondary, no family-wise error control"; folded into FP-3.
3. **A carve of 2,000 OpenViIC training images as the rehearsal set.** A panel question (the pool with its exclusions and the shot assert, Section 4.1); it becomes his decision only if the panel escalates.
4. **Two rented machines for two sessions** (about 34 GPU-hours, about 50 under the caps). Inside the standing rental rule; reported, not asked, unless the balance needs a top-up. It does: the rental needs about 390k-520k VND against a balance of about 362k (CC-438 N11; FP-6).
5. **The wording that the paper prints** for a second look (registration draft §7.14). He rewrites the paper; the registered sentence is the floor, not the final text.

## 10. Limits of this design

- I read no per-image file, so every standard error here is scaled from printed interval widths.
- The count of references per OpenViIC training image, the refill share of `perm` on the carve, the place of each stored file on the drive and the batch-size-1 rate on a new host are not verified.
- The 1.65-point margin comes from two backbones; it is a fixed, disclosed convention, not an estimate of Aya-Vision-8B's drop.
- For Qwen2.5-VL-7B and InternVL3-8B the test confirms how a known sum splits. Only Aya-Vision-8B's rows are new information about the size of the retrieval effect on this set.
- The probabilities of Section 6 about the evaluator are guesses about a reader, not about data.
- The contact table of Section 2 was built from LOG lines, registration text, script source and ids. Row K3d (92 exploratory scripts of 2026-10-13 to 2026-10-20 that name the panel file) is bounded by ids (at most the 636 OV-test files of the panel) and not settled file by file.
- The number of pool images that exclusion (iii) removes is unknown until block 0. If fewer than 2,000 remain, the study stops at block 0, before any GPU step.
- Every sha256 input of the registration text is pinned in draft v0.3 including the carve order file of §5.1 (`8e11bad51c77adc54c05b91a86f7b6f5a1f2d0e9032f06faf80f05e438d42850`, one ids-only run licensed by CC-449). Paper B's H-500 is dropped as a separate owner (Section 4.1).
- The reading of exclusion (ii) as "carve first, shots drawn with no own-cluster masking, assert" is mine; the panel's text says "before the draw" (registration draft Q13, Q14).
- The full text of the second-look sentence departs in its first words from judge J3's text, because of rows K3 and K4 (registration draft Q15).
- The study is less likely than not to bring the paper to 80 (Section 6.1).
