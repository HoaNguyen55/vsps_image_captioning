# Paper C, stage 2: pre-registration of the one-look dev-B confirmation (DRAFT)

**Label: STAGE 2 / DEV-B, ONE LOOK.** This file is the stage-2 prereg: filled from the stage-1 decide output and checked by the judge (CC-086b) before this commit.

| field | value |
|---|---|
| Paper | C: a controlled study of retrieval in-context captioning for Vietnamese, with a post-hoc object guard from a different VLM (C-f, CC-087) |
| Authority | PI decision of 2026-10-22, 00:15 VN (`manuscript/cfp/QQ34_VENUES_AND_PLAN_2026-10-21.md` §2.1, §2.4, "Quyết định của PI"); stage-1 DESIGN binding 3 and §7.4 |
| Stage-1 design | `manuscript/prereg/2026-10-22_c_stage1/DESIGN.md` sha256 `eacc9a9c737cec278c77ce5acd3b07422c9b0f7e661624ec42ba0454050ed53f` (commit 133bd16) |
| Stage-1 lists | `lists.json` sha256 `5c479f03e8be544f4cd12b5d997b5dc92b6c622df061760cd02f6ba82f6b4371`, `LISTS_ADDENDUM.md` (commit 6129e8e) |
| Paper E split | `manuscript/prereg/2026-10-22_e_stage1/e_split.json` sha256 `795652f1af45597b3a89f8a937056a1810504d54e1e41319198b3fb27fea2ef9` (commit 37e629d) |
| Rulings | CC-079 (C1–C6, Q1–Q9, style rule), CC-079b, CC-079c, CC-080, CC-081 (E2, E3, (a)), CC-081b, CC-082 (T6), CC-083, CC-084 (D1, D2, Q3), CC-085, CC-086 (kit_b, F1–F5, Q1–Q9), CC-087 (C-a…C-g, power note, salami rule), CC-088 (B-1 knock-on: PTB column), CC-093 (J1–J10, W1–W7), CC-086b |
| Stage-1 verdict | **ADVANCE** (`decide_advance.json` `verdict`; job.log `2026-10-22T11:29:36Z ADVANCE-VERDICT ADVANCE`). No judge ruling replaced it. |
| Stage-1 decide record | ledger `ledger.jsonl` sha256 `febe593ec46d7f1bdda1cf648a6248bb7c17de54e8f1d8299f8ac2f6b60f7cde` (215 rows, last row `utc` 2026-10-22T11:29:36Z, the second of the verdict; listed in the stage-1 `SHA256SUMS`, which verifies 51/51 on M3 and on the local mirror); decide output `decide_advance.json` sha256 `9940f83f7b6b5a561ca204d11601a8b792e3c1cfe38cc309ac7fed9566503eb8` (pilot `decide_pilot.json` `07291fe363c5d1e81be5580f8c0b5bb30a2ea68b93be6a8e7252c90305b242dc`, prescreen `decide_prescreen.json` `495786aac8a82cccadc1ab3df489d5af3305f320a67bbbaa24fa7f47ab981e29`) |
| Written | 2026-10-22, while C stage 1 runs on M3 (P0 GO; P1 and P2 pending). Amended the same day for CC-087 and CC-088. No OV-dev-B or XM-dev500 image has been decoded, embedded, guarded or scored by Paper C. |
| Machine | M3 only (one RTX 3090 24 GB). XM scoring runs locally on CPU (§6.3). |

## 0. Bindings

1. **Outputs are never committed.** This covers captions, example files, embeddings, guard caches and the stage-2 ledger. They live on M3 under `/root/outputs/c_stage2/` and in the 30-minute backup. Paper C commits scores only (numbers, ids, sha256), never preds, exemplar files or captions (CC-079 C3).
2. **One look at dev-B.** Each stage-2 run in §4 is decoded once and scored once with the frozen configuration of §2. No configuration, threshold, metric or set is changed after any stage-2 output exists. A re-score is allowed only to fix a scorer crash, and it must give identical numbers for the rows already written.
3. **No test look.** No OV-test or XM-test2500 image is decoded, embedded or scored, and no OV-test annotation, XM-test2500 reference or OIV7 label file is on M3, until C's test prereg is committed (QQ34 §2.4 item 4; stage-1 binding 4).
4. **No test-set tuning.** Nothing in this file was set from a test set. The SESOI (§7.1) comes from the plan, not from any C result.
5. **No "first" or "novel" claims** ("đầu tiên" included), in any paper text. The paper states differences from the closest work only (QQ34 §2.1 table). It cites Li et al. (ACL 2024, 10.18653/v1/2024.acl-long.503) and ViG (MAPR 2026, 10.1109/mapr72750.2026.11685699).
6. **"A different VLM", never "cross-family"** (CC-079 C4). The shared lineage is stated in the same or the next sentence: InternVL3-8B's LLM is Qwen2.5-7B, and Qwen3-VL is in the Qwen line.
7. **Existing data and labels only.** No new annotation. Verifier probabilities and model captions are model signals, never gold. Gold is the released references and, on XM3600, the released OIV7 human-verified labels.
8. **No dataset caption is written into any committed file.** Memory captions are read from `$NCS_DATA` at run time and never written.
9. **Order with Paper E (CC-081 E3).** See §3.3. C's stage-2 run takes no Paper E decode or cache as its own output (§3.3 rule X3).
10. **Paper E is never C's main metric** (E DESIGN binding 12). E's per-object statistic is the same statistic as C's guard; C's paper says so wherever E is cited.
11. **Framing (C-f, CC-087).** The paper is "a controlled study of retrieval in-context captioning for Vietnamese, with a post-hoc object guard". It claims no "new method" and no "first".
    - Related Work lists 2512.00887 as a high-overlap work, together with NES, 2510.24331, 1505.04467 and 2305.14800.
    - Paper C's authors read the FAIR 2025 paper (10.15625/vap.2025.0261) in full before submission.
12. **Ownership between the sister papers (salami rule, CC-087).**
    - E owns the per-object statistic as a metric and validates it (pairs, τ, later human sets).
    - C reports only the guard's effect on captions (H_G, §7.5). It cites B for the S2 verifier and E only as related work. No C claim depends on an E result.
    - C reports no pair or τ tables and does not use E as a named secondary metric. E reports no CIDEr and no ICL effect.
    - Neither paper re-reports B's 0.634 or 0.485 as its own result.
    - The cover letters name the sister papers and the boundaries. A cross 8-gram check across A/B/C/E runs before submission.

## 1. Preconditions

### 1.1 Before this prereg is committed

1. Stage 1 has ended with ADVANCE under DESIGN §7.3, or with a judge ruling that permits stage 2. Every `[FILL FROM STAGE-1: …]` is filled from the decide output and the run record, and nothing else in this file changes when filling.
2. **The `scripts/kit_b/` folder is committed through the gatekeeper** (CC-079 C5, CC-086 Part 1, blocking), in its own commit before this prereg.
   - It holds 6 files (no `__pycache__`), byte-identical to the staging tree, with Paper B's BUILD_RECORD shas: `protocol_pilot.py` 6aee4282, `punctuation_audit.py` a7e80240, `exchangeability_audit.py` f30758e3, `xm3600_period_audit.py` 145ab673, `cay_audit.py` 7334ced3 and `PROTOCOL_CARD.md` 21f0c9b9.
   - Stages 1 and 2 load two of them: `protocol_pilot.py` (sha256 `6aee428207a2d1a045cd72d054e26a2e2ac8d9c2e414cb0c161e3b95dffd92bf`) and `punctuation_audit.py` (sha256 `a7e8024030f56cbff07124278cd631964b7b1197607426d7212fd665b6c2f9b1`).
   - **Done:** commit 7fa7b83 (CC-086 Part 1). Commit 34323eb then added a seventh file, `ptb_protocol.py` (sha256 `ea5fbe6e1528e339abfcb9ba00bdd0c4d4e4bde07ae6edd30fffaa72d60754d2`, CC-088 B-1). Stage 2 also loads it, for the reported PTB column only (§6.1).
3. `frozen_config.json` next to this file holds the §2 values (k, order, template, τ per backbone), copied from the stage-1 decide output, and τ_G per backbone, derived from τ by the C-a rule of §2. It is committed with this file. The stage-2 code reads the configuration only from it, pinned by sha256, so the code can be written and selftested against a dummy config before stage 1 ends.
4. The gatekeeper's 6- and 8-gram scan of this file and `frozen_config.json` finds 0 hits apart from the known false positives (CC-079c).

The stage-2 code of §12 is **not** a precondition of this commit. It follows in a later gatekeeper commit (§1.2, Q9), so that E's stage 1 can start as soon as this file is committed (CC-081 E3).

### 1.2 Before any stage-2 decode on M3 (operator steps, recorded in the stage-2 run record)

- The stage-2 code of §12 is committed through the gatekeeper. Its selftests pass, and its sha256 are in `SHA256SUMS` next to this file. It pins this file's and `frozen_config.json`'s sha256, so this file does not list the code's hashes (as in stage 1). The gatekeeper's 6/8-gram scan of the code finds 0 hits.
- **F5 (CC-086).** The stage-2 code commit gets a judge check, as for CC-079b and CC-083, before the first stage-2 M3 step. The carve-out and refusal logic (§12 items 2, 3 and 11) is integrity-critical.
- The M3 repo is at the commit holding that code. The tracked tree is clean and `SHA256SUMS` verifies.
- **OV-dev-B block:**
  - the 925 OV-dev-B images are copied into `$NCS_DATA/datasets/openviic/images`, by an explicit list from `lists.json` `sets.ov_dev_b`, and sha-checked 925/925;
  - the OpenViIC dev annotation on M3 is replaced by a D1-style subset (CC-084 D1): the release (`2a68a3eb4d41926d…`) filtered to the keys of `sets.ov_dev_a` ∪ `sets.ov_dev_b` (1,836 keys), values unchanged. The run record holds its sha256, key count and how it was made.
- **XM-dev500 block (§3.3):**
  - **timing (F3, CC-086):** the 500 XM-dev500 images and their reference subset are copied to M3 only at §9.3 step 4, after E's stage-2 prereg is committed or E stops. Until then, no XM-dev500 image or reference is on M3 for Paper C. Separately, E DESIGN §2.6 keeps E-dev-B images off M3 until E's stage-2 prereg;
  - the 500 XM-dev500 images go into a new folder, `$NCS_DATA/datasets/c_xm_dev500/images`, that holds nothing else. They never go under `$NCS_DATA/datasets/xm3600/`, because E's `judge.py` refuses to run while `datasets/xm3600/images` exists (CC-085);
  - the Vietnamese references of these 500 images only are copied as one subset file in the same folder, values unchanged. The run record holds its sha256 and key count (500).
- The operator re-checks and records that no OV-test file or annotation, no XM600 or XM-test2500 image, no XM3600 `full_data.json`/`test_data.json` and no `oiv7_labels.json` is on M3. The CC-079 operator check (0 of 6,599 refused sha256 under `$NCS_DATA`) is repeated, with the 925 + 500 carved-out sha256 removed from the refused set.

## 2. Frozen configuration (from stage 1, DESIGN §7.2)

The pick rule, its eligibility floors and its tie-breaks are DESIGN §7.2. They were applied on dev299 only. This prereg copies the result and does not re-run `pick()`.

| item | `qwen25vl_7b` | `internvl3_8b` |
|---|---|---|
| picked run id (stage 1) | `c1_qwen25vl_7b_ktvic_dev299-ret-k8-first-T1` | `c1_internvl3_8b_ktvic_dev299-ret-k4-last-T2` |
| k | 8 | 4 |
| order | first | last |
| prompt tail | T1 | T2 |
| guard threshold τ | −∞ (ledger key `-inf`) | 0.1 (ledger key `0.10`) |
| guard-endpoint threshold τ_G (C-a, CC-087) | 0.0 (ledger key `0.00`; τ = −∞, so the 0.0 fallback) | 0.1 (ledger key `0.10`; = τ) |
| stage-1 dev299 stripped CIDEr-D of the pick (ledger value) | 58.65745289584491 (ledger row 30, τ `-inf`) | 50.99768386137087 (ledger row 122, τ `0.10`) |
| stage-1 OV-dev-A A1/A2/A3 and length-gap values | `qwen25vl_7b`: vs_rand 8.003620307354556 [6.022939909440175, 10.014891037321624]; pcm_vs_zs 4.175084175084176 [1.7471363950425358, 6.498290013679889]; verbatim_share 0.01756311745334797; length rel_gap 0.07072054898970646 (not separated from length: false). `internvl3_8b`: vs_rand 0.1526040614709113 [−1.5217013995609217, 1.8188668111964874]; pcm_vs_zs 1.179736294240111 [−0.13335120643431636, 2.5342465753424657]; verbatim_share 0.0021953896816684962; length rel_gap 0.04445267642155943 (not separated from length: false). **Pooled vs_rand (A1): 4.078112184412734 [2.6936864942371024, 5.429971067508233]** (`decide_advance.json`) | (pooled row in the left cell) |

- **T2 controls:** ran for `internvl3_8b`, whose pick is T2: `c1_internvl3_8b_ktvic_dev299-rand-k4-T2` and `c1_internvl3_8b_ktvic_dev299-fix-k4-T2` (job step `p1t2_decode_internvl` 07:57:51–08:13:50Z, items and verify 08:13:50–08:14:10Z, scored 08:14:10–08:14:19Z). The P2 controls on OV-dev-A were `c1_internvl3_8b_ov_dev_a-rand-k4-T2` and `c1_internvl3_8b_ov_dev_a-fix-k4-T2`. None was needed for `qwen25vl_7b` (T1).
- **τ_G rule (C-a, CC-087), fixed before stage-1 decide.** τ_G = τ if τ is finite. If τ is −∞ or +∞, τ_G = 0.0. τ_G is used only for the guard endpoint H_G (§7.5); it changes no arm of §4 and no §7.2 rule.
- **Timing record (J6, CC-093; from the stage-1 job log and ledger mirror, timestamps, run ids and key names only, no τ value).**
  - 04:52:33–34Z: ledger rows 1–5 (ledger sha256 `c5df04fe…`, per-row `utc`), the P0 pilot: qwen25vl_7b `ret-k4-last-T1`, `rand-k4-T1` and the reused `dp … short-T0`.
  - 06:48:13Z: CC-087 logged, fixing the τ_G rule and its 0.0 fallback.
  - 07:36:22Z: first guard verify step of stage 1 (`p1_qwen_items`/`verify`).
  - 07:56:46Z: first `p1_score` rows (row 6, ±∞; row 7, the first finite τ).
  - 07:57:51Z: `PICK` written by `p1_score`.
  - Stage-1 decide runs after that; it had not run when CC-093 was written, so τ* did not exist before CC-087.
  - The 0.0 fallback is the lowest finite value of the registered grid, a rule-based default, and applies only if τ* = ±∞.
  - **P0 note (W8, closed by CC-093):** P0 rows at 04:52Z are τ = ±∞ only (+∞ = delete-all by rule, no verifier; `guard.py:94` rejects every neighbour-only class at +∞ without reading a score); the first finite-τ row is from p1_score at 07:56Z (row 7, 07:56:46Z; row 6, also ±∞, is the first p1_score row). No verifier-scored number existed before 07:36:22Z.
- **If a picked τ is −∞** for a backbone, that backbone's frozen-τ arms carry no guard, and the paper describes its frozen configuration as "no guard" for that backbone. **If τ = +∞**, every neighbour-only class is deleted without a verifier at the frozen τ.
- **The verifier still runs in both cases** (C-a, CC-087): on the neighbour-only items of that backbone's `ret` arm, for H_G at τ_G = 0.0. Only the `rand` and `fix` verifier passes are skipped for that backbone.
- Fixed and unchanged from stage 1: the SigLIP2 embedder and revision (`google/siglip2-so400m-patch14-384` @ `e8e487298228002f3d8a82e0cd5c8ea9c567f57f`), the memory (`lists.json` `memory`, 10,501 images in 8,190 clusters), the 0.92 near cut, the prompt templates (`decode_icl.TEMPLATE_SHA256` `7478361a…`), the `zs` prompt (`evaluate.PROMPTS["short"]`, sha256 `8870589c…`), the two generators and their revisions, greedy decoding with 60 new tokens, the guard question, score s = p_with − p_without, and the deletion rule with its zero-shot fallback (DESIGN §3–§5).
- **No regeneration arm** (CC-079 Q8). No threshold is tuned on any set in stage 2.

## 3. Data

### 3.1 OV-dev-B (gating set)

- `lists.json` `sets.ov_dev_b`: **925 images** (1,006 B-raw before the protected-set cut; DESIGN §2.3). It was assigned before de-duplication and filtered against KTVIC test, OpenViIC test, all XM3600, KTVIC dev300 and the protected sets.
- References: the image's OpenViIC dev captions, as released, read through the subset file of §1.2.
- **Not yet seen:** no OV-dev-B image or caption has been on M3 (CC-084 D1). No Paper C step has decoded or scored one, and stage-1 code refuses them by file name and sha256.

### 3.2 XM-dev500 (secondary set; the only XM3600 carve-out)

- `lists.json` `sets.xm_dev500`: **500 images**, XM3600 minus XM600, ordered by sha256(`"paperC|xm|"` + image sha256), first 500 (DESIGN §2.3). It equals E-dev-A ∪ E-dev-B by sha256 (CC-085).
- References: the XM3600 Vietnamese references as released (2 per image, 3 for 15 images, §10.2).
- **Carve-out rule (CC-079 C6, amended by CC-081 (a)).**
  - XM-dev500 is the only carve-out from `exclusion.json` (sha256 `c52a96d1…`, which refuses all 3,600 XM3600 images by sha256 and the 600 XM600 ids) and from `lists.json` `refuse`.
  - An image is carved out if and only if its sha256 is in `sets.xm_dev500`. It must not be in any other refused set: XM600 ids, XM-test2500, KTVIC test, OpenViIC test, CV295, CHAIR-500 or UIT-ViIC test. The code checks this, and refuses to start on any overlap.
  - XM600 and XM-test2500 stay refused.
- **Dev–test near-duplicate check (CC-086 Q4 and F2). Done 2026-10-22, locally on CPU, before this prereg and before any E stage-1 GPU step.**
  - XM-dev500 was split by sha order, with no de-duplication against the other test sets. The OV-dev halves had one.
  - **Method.**
    - Rows come from the git-excluded stage-1 feature cache, exactly as `build_memory.features()` loads them on a cache hit. The groups are xm_all (3,600 rows), ov_test (2,001) and kt_test (558), the same groups as the lists build. Each cache file was found by its key: the group's image sha256 plus the SSCD weights sha256 `9f26bd4c…`. Nothing was recomputed.
    - Sets were matched by image sha256 through `lists.json` (`xm_dev500`, `xm_test2500`), XM600 ids, and `e_split.json` (`e_dev_a`, `e_dev_b`). The script asserted E-dev-A ∪ E-dev-B = XM-dev500.
    - The rule is `build_memory.near()`, i.e. the registered rule of DESIGN §2.4, unchanged: mirrored hashes included, and byte-identical files always match.
    - Counts only were printed. No caption was read.
  - **Counts** (images on the left-hand side with at least one near-duplicate on the right-hand side):

    | dev side | against | near-duplicates |
    |---|---|---|
    | XM-dev500 (500) | XM-test2500 (2,500) | **0** |
    | XM-dev500 (500) | XM600 (600) | **0** |
    | XM-dev500 (500) | OpenViIC test (2,001) | **0** |
    | XM-dev500 (500) | KTVIC test (558) | **0** |
    | E-dev-A (250) | E-dev-B (250) | **0** (and 0 for E-dev-B against E-dev-A) |

  - **Positive controls**, from the same run: XM-dev500 against itself matches 500/500. OpenViIC test against itself, with byte identity masked so that only the hash and SSCD rule can fire, matches 2,001/2,001. That control includes the 3 truncated images decoded under CC-082.
  - **Reproduced** 2026-10-22, before commit, together with the C-g count of §3.4: `neardup_counts.py` (sha256 `661698b10b76851d87f2548e25f3374ec43865d36db32f9fe09e07b7532cb3c7`; committed next to this file, W4 CC-093, so the 1,941 can be reproduced from the repo; it reads the git-excluded feature cache), output `neardup_counts.json` (git-excluded) sha256 `0b9b58baccb40ec542e6120612632f6aad2cb7b19b82fa5d49c609bfab30eee4`. Same cache files (cache hit only; the script stops before any SSCD pass on a miss), same rule, same counts: all six rows 0, and the two positive controls 500/500 and 2,001/2,001. The original F2 run left no artefact path in this file; this run is its record.
  - **Result:** no image is dropped. XM-dev500 stays at 500, and E's `e_split.json` and pair list are unchanged. Had there been a hit, the rule (CC-086 F2) was to drop it from the dev side only (C's XM-dev500, or E-dev-B for an A–B hit), keep the test side intact, and return to the judge before E's GPU work.

### 3.3 XM-dev500 and Paper E: the rule (CC-086 Q1–Q3)

The facts that bind the rule:
- E-dev-A and E-dev-B are both inside XM-dev500.
- E stage 1 decodes zero-shot captions of the 121 E-dev-A pair images with C's backbones and prompt, and asks C's guard question about them.
- E's stage-1 pair build has already read E-dev-A references and OIV7 labels locally, printing counts only.
- E3 (ii) covers **any** C output on XM-dev500. Restricting C to E-dev-A therefore does not avoid it.

| rule | content |
|---|---|
| **X1 (set)** | C uses **all 500** XM-dev500 images. The §3.2 check dropped none. |
| **X2 (protecting E)** | No C stage-2 decode, embedding, guard pass or score touches an XM-dev500 image until E's stage-2 prereg is committed or E has stopped. The XM-dev500 block is C's last stage-2 block, apart from the C-c image-blind step (§9.3 step 5), which runs in the same window. |
| **X3 (protecting C)** | C's configuration is frozen by this prereg, which is committed before E's stage 1 starts, so no E output can tune it. C reuses **no** E decode, cache, pair or judge output: every C stage-2 output on XM-dev500, its `zs` arm included, is decoded fresh by C's own code. Reuse would save about 0.1 GPU-h and is not worth the provenance coupling. |
| **X4 (C → E)** | C's XM-dev500 `zs` decodes and guard caches may serve as E's stage-2 data only if E's stage-2 prereg names that reuse. They are handed over as files on M3, never committed. |
| **X5 (disclosure)** | By the time C decodes XM-dev500, E stage 1 will have made zero-shot captions and guard scores on 121 E-dev-A images with the same backbones and prompt. C's paper says so. C's XM-dev500 result is fresh for C's decisions, because §2 was frozen first, but C's `zs` captions on those 121 images are not unseen outputs. |
| **X6 (OV-dev-B has no E link; CC-086 Q2)** | The OV-dev-B block touches no XM3600 image, reference or label. It **may run as soon as this prereg is committed, before or after E stage 1** on the queue; the order between those two is free. E3 (ii) does not bind it: it protects E-dev-B and E's test from C outputs on XM images, and E's stage-2 choices come from E's fixed rules on E-dev-A. **Condition:** E's stage-2 prereg states that C's OV-dev-B outputs existed when it was written, and that its frozen values come from E's own fixed rules. The XM-dev500 block stays last (X2). |

**The XM-dev500 block runs whatever the OV-dev-B outcome** (pass, fail or JUDGE), so the XM look is not chosen by the gating result (CC-086 Q3).

### 3.4 dev299 against the test sets (C-g, CC-087)

Counted 2026-10-22, locally on CPU, before this prereg is committed and before any E stage-1 GPU step, alongside the §3.2 reproduction.

- **Why.** The dev-pools record (dev-pools DESIGN §5, PD-31) has 59 KTVIC dev300 images with a copy in the OpenViIC test split (a dev-side count; CC-087 calls them "59 OV-test images", see J9), and C's §2 configuration was picked on dev299. Those test images were in effect used for tuning. Unlike CC-081 E2 (references read, no tuning), this is a tuning overlap, so the exclusion goes into the test primary (§8, §11 item 7).
- **Method.** As §3.2: the same script and output (sha256 above), the git-excluded stage-1 feature cache (`kt_dev300` group, 300 rows, subset to the 299 sha256 of `ktvic_dev299.tsv` `a4ac7fdb…`), the registered rule `build_memory.near()`, counts and ids only. `near()` uses the left side's mirrored hashes, so both directions are counted. The test side is what the exclusion removes.
- **Counts:**

  | left | right | images on the left with ≥ 1 near-duplicate on the right |
  |---|---|---|
  | OpenViIC test (2,001) | dev299 (299) | **60** |
  | dev299 (299) | OpenViIC test (2,001) | **59** (matches the dev-pools record of 59) |
  | XM-test2500 (2,500) | dev299 (299) | **0** |
  | dev299 (299) | XM-test2500 (2,500) | **0** |
  | OpenViIC test (2,001) | dev300 (300) | 60 (image `1437` adds none) |

- **Both orientations.** `near()` reads only the left side's mirrored hashes, so the script also marks every OV-test or XM-test2500 image matched with dev299 on the left. That gives 60 and 0, the same images: the union is 60 for OV-test and 0 for XM-test2500. One dev image can match more than one test copy, so 59 dev299 images give 60 test images.
- **Positive control:** dev299 against itself, byte identity masked, matches 299/299.
- **The 60 OV-test file names** are frozen now in `ov_test_dev299_neardup_files.txt`, committed next to this file (W4, CC-093; 60 lines, sorted, OpenViIC file names only, no caption text, sha256 `737e617a966478d9bcadb0c932d72a6f8de7dd5c7e83c98730e1a88720f2f41f`). None of them is one of the 3 truncated OV-test images of §11 item 1. C's test prereg pins this list by sha256 and refuses a different one.
- **Result.** C's test primary on OV-test is the 1,941 images outside the list (§8). XM-test2500 needs no exclusion.

## 4. Arms and runs

Per (set, backbone), four main runs and one image-blind run, at the frozen k, order, template and τ of §2:

| arm | run id pattern | examples shown | guard |
|---|---|---|---|
| `ret` (method) | `c2_<model>_<set>-ret-k<k>-<order>-<tpl>` | the k nearest eligible clusters (DESIGN §3.2) | frozen τ |
| `rand` (control) | `c2_<model>_<set>-rand-k<k>-<tpl>` | k random eligible clusters, seed `paperC|rand|<set>|<image id>`, prefix of 8 | same τ |
| `fix` (style control) | `c2_<model>_<set>-fix-k<k>-<tpl>` | one fixed set per dev set, seed `paperC|fix|<set>`, drawn from the clusters below the near cut for every image of that set, prefix of 8 | same τ |
| `zs` (lower bound) | `c2_<model>_<set>-zs` | none (`short` prompt) | none |
| `blind` (image-blind control, C-c, CC-087) | `c2_<model>_<set>-blind-k<k>-<order>-<tpl>` | the frozen `ret` prompt, examples and template, with **no image input** (the model's text-only path) | none |

- Sets: `ov_dev_b` (925) and `xm_dev500` (500). That gives 2 sets × 2 backbones × 4 runs = **16 main decodes**, plus 2 × 2 = **4 image-blind decodes** (C-c). The image-blind runs come after the 16 main runs and the guard (§9.3), are reported and do not gate. If the cap binds they are the first item dropped, and the drop is reported (§9.2).
- **NN copy baselines (C-b, CC-087; Devlin et al., 1505.04467).** Rows that need no decoding, built on CPU from the `ret` example lists. They are reported and do not gate:
  - `c2_nn_<set>-top1`: NN-top1, the shown caption (§5.2) of the nearest eligible cluster. It does not depend on the backbone, k or order.
  - `c2_nn_<set>-cons-k<k>`: NN-consensus, among the k shown captions of the frozen `ret` arm, the one with the highest mean CIDEr-D (stripped, kit B) against the other k − 1 (J5, CC-093). The CIDEr-D df comes from the **memory caption pool** (the shown caption of every memory cluster, the pool the k candidates are drawn from), computed once on CPU and never committed, so the choice uses no reference-side statistic of the evaluated set (as in Devlin et al.). Ties go to the nearer cluster (higher SigLIP2 cosine), then the lower cluster id. The chosen caption is then scored by the standard kit B scorer like every other row. One row per distinct frozen k.
  - Their caption files are outputs: never committed, as for memory captions (binding 1).
- The guard's zero-shot reference for each image is the same backbone's stage-2 `zs` run on that image.
- The `c2_` prefix and a separate stage-2 ledger keep stage-1 and stage-2 rows apart.

## 5. Retrieval, prompts, decoding, guard: unchanged except as below

### 5.1 Embeddings

- **Memory vectors are reused** from the stage-1 embedding file: `emb.npz` sha256 `59e65f6f6432af97504c59c72fa07b644acbff26938e1365473fad659421f7c0`; its sidecar `emb.npz.sha256` records the same value (sidecar file sha256 `9490b9b198ae9c672d9e340d35080eb63a5ffa8709777effd586fd96352e38ee`). These are the vectors under which §2 was picked. They are not an output on any stage-2 image.
- **Only the 1,425 new query images are embedded** (925 OV-dev-B, 500 XM-dev500). The embedder, revision, fp16, batch size 64 and venv are the same as stage 1. The file records the stage-1 embeddings sha256 and the stage-1 snapshot per-file sha256, and refuses on a mismatch.

### 5.2 Examples

- `ret`, `rand` and `fix` follow DESIGN §3.2–§3.3 with the new set names, so the seeds differ from stage 1's.
- The 0.92 near cut applies in every arm, and the number of cut clusters per image is recorded.
- **Shown caption for an XM query.** The memory has no XM3600 member (all 3,600 were in the protected set), so DESIGN §2.1's "own dataset" rule falls back to the cluster's **first member's** caption (`decode_icl.shown`). For an OV-dev-B query, the cluster's OpenViIC member is used if it has one, else its first member.

### 5.3 Guard

The question, verifiers and environments are DESIGN §5, unchanged:
- `qwen25vl_7b` is checked by S2's InternVL3-8B @ `853e3a79…`, in the 4.51.3 venv;
- `internvl3_8b` is checked by Qwen3-VL-8B @ `0c351dd0…`, in the B-N1 venv, with the answer-position stop rule (median yes + no mass < 0.5 over the first 20 questions → stop).

Items are the neighbour-only classes of the three ICL arms. The no-image pass is recomputed per class in stage 2, not carried over.
- **`ret` items are always verified** (C-a, CC-087): for both backbones, whatever the frozen τ, so that H_G (§7.5) can be computed at τ_G. This sits inside the budgeted guard rows (§9.1).
- `rand` and `fix` items are verified only for a backbone whose frozen τ is finite (§2).
- The image-blind arm (C-c) is not guarded.

## 6. Metrics and scorer

### 6.1 Protocol card (Paper B §4.2; DESIGN §6.1, unchanged apart from the added PTB row)

| item | stage 2 |
|---|---|
| sets | `ov_dev_b` (925, OpenViIC dev references as released); `xm_dev500` (500, XM3600 Vietnamese references as released) |
| segmenter | RDRSegmenter, VnCoreNLP 1.2, through committed `scripts/kit_b/protocol_pilot.py` `rdr`, on candidates and references, lower-cased (protocol P0). The jar must be sha256 `9e2811cdbc2ddfc71d04be5dc36e185c88dcd1ad4d5d69e4ff2e1369dccf7793`. |
| n-gram metric | CIDEr-D ×100, kit B's re-implementation, df over the scored set's references (per set) |
| punctuation | scored as written **and** with trailing punctuation tokens stripped (`punctuation_audit.strip_trailing_punct_tokens`). **Decisions use the stripped column.** |
| PTB-removed column (CC-088 B-1) | **reported, non-gating, CPU.** Protocol P0 (the segmenter row above), then every token in pycocoevalcap's PTB `PUNCTUATIONS` list removed after segmentation (`ptb_protocol.PTB_PUNCTUATIONS` and `ptb_protocol.ptb`), on candidates and references. CIDEr-D ×100 as above. Added before any stage-2 output; no §7 rule reads it. Decisions stay on the registered stripped column. |
| object matcher | v2 (tone-normalised), `rescap.chair` |
| kit | `protocol_pilot.py` `6aee4282…`, `punctuation_audit.py` `a7e80240…` and, for the PTB column only, `ptb_protocol.py` `ea5fbe6e…`, loaded from the committed `scripts/kit_b/`. `score.kit` refuses on any sha mismatch. |
| uncertainty | §6.4 |
| scorer process | separate from generation, CPU |

### 6.2 Scoring environment (CC-084 D2)

- OV-dev-B is scored on M3 in `/root/venv-c1score`: Python 3.10.12, numpy 2.2.6, scipy 1.15.3, `pip freeze` sha256 `4b81b6b6a549771115529e6900b9589835cdbfff0c6acf179aef53d283b744d5`, Java openjdk 11.0.32.1 (2026-08-18).
- The run record re-checks the freeze sha256 and the Java version before the first stage-2 score. A mismatch stops scoring and goes back to the judge.
- The registered decode venvs (`/root/venv-lb`, freeze `685ffe2a…`; `/root/vsps/.venv`, `7332d343…`) stay untouched.

### 6.3 XM-dev500 scoring (local, CPU)

- XM-dev500 references go to M3 only as the §1.2 subset, and only for the XM block.
- The OIV7 labels never go to M3.
- **Verified precision** (Paper A's `xm3600_oiv7.caption_rows` rule, with `statuses` and the 69-class map `vi_oiv7_map.json`) is computed **locally on CPU**, after the XM-dev500 preds are copied back. Its mode refuses when `VSPS_MACHINE_ID` is set and refuses any image outside XM-dev500.
- The local scorer runs CIDEr-D only if the environment record matches §6.2. Otherwise CIDEr-D and CHAIR_i are scored on M3 and only verified precision is scored locally (Q6).

### 6.4 Bootstrap

- Paired image bootstrap with **B = 2000** resamples, `numpy.random.default_rng(0)`, and percentile 95% CI (`score.boot`, `DRAWS, SEED = 2000, 0`).
- When pooling backbones, the image is the unit: per-image differences are averaged over the two backbones, then resampled.
- ΔP_cm and Δ verified precision are ratio statistics. Their numerator and denominator sums are resampled together over images (`score.pcm_ci`).
- **The same resample indices are used for every CI within a set** (CC-086). One B × n index matrix is drawn from `default_rng(0)` per set, with n the set's image count, and every difference, ratio and pooled CI on that set uses it. `score.boot` and `score.pcm_ci` already do this, because each draws `integers(0, n, (B, n))` first from a fresh `default_rng(0)`. The stage-2 code keeps this, and a selftest checks it.

### 6.5 Reported per run (all rows, both sets)

Everything in DESIGN §6.2, per run, at the frozen τ **and** at τ = −∞ (unguarded):
- CIDEr-D as written and stripped, and the PTB-removed column (CC-088 B-1, §6.1);
- CHAIR_i and mentions per image;
- ΔP_cm against `zs`;
- neighbour-only rate, rejected classes per image, and deleted and fallback rates;
- the 4-gram copy rate against the memory;
- the near-verbatim copy share;
- the hit_max rate;
- the style report (mean syllables, share ending in punctuation, top-3 opening-bigram share) for `ret`, `rand` and `fix`, plus the **source-dataset share** (C-d, CC-087): the share of shown captions taken from the query's own dataset. It is a covariate only. On XM-dev500 it is 0 by construction (§5.2);
- **neighbour-only object precision, all mentions** (C-e, CC-087; defined in §7.5), for every ICL run;
- the guard AUROC diagnostic, which never gates. It is computed and archived as registered. C's paper makes no claim about the validity of the statistic (E owns that, binding 12), and lists the row with its value in the supplementary registered-rows table, labelled "diagnostic; its interpretation is Paper E's", with no text claim (J10, CC-093).

Added rows, all reported:
- **Guard endpoint rows (C-a):** `ret` at τ_G, and `ret` at +∞ (delete-all), each with neighbour-only object precision, mentions per image and CHAIR_i, so that precision bought by deleting is visible (§7.5). For `ret`@τ_G and `ret`@−∞, also Σm and the share of images with m > 0 (J3, CC-093).
- **Image-blind arm (C-c):** the same metrics, unguarded, and Δ `ret`@−∞ − `blind` with its CI.
- **NN-top1 and NN-consensus (C-b):** CIDEr-D (as written, stripped, PTB), CHAIR_i and mentions per image, and Δ `ret` − NN with its CI, per backbone and pooled.
- **Cosine-bin dose-response (CC-087, optional, named, non-gating, CPU):** ΔCIDEr-D (stripped) of `ret` − `rand`, pooled, within tertiles of the query's SigLIP2 cosine to its nearest eligible cluster (tertile cuts per set), with CIs. The cuts are computed from that set's queries before any stage-2 caption is scored and are recorded in the run record (J8, CC-093).
- Not in this prereg (CC-087): the self-verifier, non-Qwen verifier and Vietnamese-VLM rows (optional dev-A work), and C-b on dev299 and OV-dev-A (optional, ledgered dev-A exploration that changes no pick rule).

On XM-dev500, verified precision is added.

## 7. Decision rules (fixed now; one look)

### 7.1 SESOI

**SESOI = +2.0 stripped CIDEr-D points** (ret+guard − rand+guard, pooled).
- Source: QQ34 §2.1 ("gợi ý +2"). It equals stage-1 A1's +2.0. It is fixed here, before any dev-B output, because stage-1 binding 3 requires the stage-2 prereg to fix it and the 2 × SESOI gate cannot be applied without it.
- It is **not** derived from the P0 pilot (+6.91 on dev299) or from any stage-1 number.
- **Note for the paper (CC-086).** P0's +6.91 [+0.53, +13.32] was estimated on dev299, the set used for picking, so it is expected to shrink on dev-B. The gate is meant to be demanding: S1 passed its dev look with +2.55 (lower bound +0.004) and gave −0.39 on test.
- **The test P1 keeps SESOI = +2.0** (CC-086 Q5). The plan's "chốt sau dev-B nhưng trước test" is met by fixing it here, which is earlier. Re-fixing it after seeing dev-B is the degree of freedom the gate removes.

### 7.2 Gate on OV-dev-B (per QQ34 §2.4; decides whether a test prereg is written)

With each backbone at its frozen configuration, **PASS** if all of G1–G3 hold and L does not fire:

| rule | content |
|---|---|
| **G1** | Pooled over both backbones, ΔCIDEr-D (stripped) of `ret` − `rand` (same k, template and τ) has a point estimate **≥ 2 × SESOI = +4.0** and a 95% CI lower bound **> 0**. |
| **G2** | Per backbone, the 95% CI lower bound of ΔP_cm of `ret` against `zs` is **> −1.0**. |
| **G3** | Per backbone, the near-verbatim copy share of `ret` is **≤ 0.05**. |
| **L (length, CC-079)** | If, for either backbone, \|len_ret − len_rand\| / len_rand > 0.10 (mean syllables), the G1 gain is reported as **"not separated from length"**. The verdict is **JUDGE**, whatever G1–G3 say. There is no re-look: a length-matched comparison, if the judge asks for one, is a new design and cannot reuse OV-dev-B as a fresh set. |

- Δ against `fix` and against `zs` are reported with CIs and do not gate. There is no per-backbone rescue: if G1 fails pooled, the gate fails.
- **Power note (C-M6, CC-087).** At SE ≈ 1.85 per backbone, the chance of passing G1 is about 50% if the true Δ is +4. The gate keeps 2 × SESOI; the paper states this power.
- **Outcomes:**
  - **PASS:** write C's test prereg (§8, §11).
  - **FAIL (CC-086 Q3):** OV-dev-B and XM-dev500 are then both spent and cannot confirm a stage-1b configuration, so **C stops**, with one exception. A stage-1b round (QQ34 §2.4 item 2, DESIGN §7.4) may go ahead only if its design note names a confirmation set on which no C output exists, before any stage-1b output, and the judge approves it. Its budget is only what remains under the 20 GPU-h after stage 2. Any carve-out from OV-test or XM-test2500 for that purpose is a test-set change: it needs its own ruling and must be made before any test output.
  - **JUDGE:** back to the judge, with no test prereg until the ruling.

### 7.3 Secondaries (pre-specified, do not gate): S1 and S2 on XM-dev500, S3 on both sets

- **S1:** pooled ΔCIDEr-D (stripped) of `ret` − `rand` is reported with its CI. "Confirmed" means a point estimate > 0.
- **S2:** pooled over mentions, the 95% CI lower bound of Δ verified precision (OIV7) of `ret` against `zs` is **> −1.0** points.
- The length rule L is reported for XM-dev500 too, and does not gate here.
- **S3, named secondary (C-e, CC-087), on both sets:** neighbour-only object precision with all mentions (no prefix cut; §7.5) of `ret` at the frozen τ, per backbone and pooled, with its CI. It is reported and does not gate. It is not co-primary; C's test prereg may make it so only with the multiplicity stated and before any test output.
- The paper explains why the prefix-limited ΔP_cm misses tail objects (C-e).
- S1 and S2 are reported as confirmed or not confirmed. They change neither the §7.2 verdict nor whether the XM-test2500 secondary predictions enter the test prereg (Q6).

### 7.4 Kill rules during the run

- **GPU cap** (§9.2): the queue stops at the cap. A set that is not complete is reported as incomplete and gives no verdict.
- **Verifier stop:** the Qwen3-VL answer-position rule (§5.3).
- **Retries:** a failed step is retried from its resume point, at most 3 attempts, then JOB STOP (as in stage 1).
- **Refusal:** any refused image (§3.2, §12) stops the step before the model loads.

### 7.5 Guard endpoint H_G (C-a, CC-087; does not gate §7.2)

- **Neighbour-only object precision (NP).** For a caption, the denominator is the distinct neighbour-only classes (DESIGN §5, classified before the guard) that are still in the final caption. "All mentions" means every such class counts, with no prefix cut (unlike ΔP_cm's matched prefix). The numerator is those of them found in the gold. NP = 100 · Σ tp / Σ m over the set's images.
  - Gold: on OV sets, the union of the image's references (`rescap.chair`, as CHAIR_i). On XM sets, OIV7 verified precision (Paper A's `caption_rows` rule, §6.3), scored locally: tp and m then count only the classes that rule counts as verified.
  - A fallback caption (the `zs` caption) has no neighbour-only class by definition, so it adds nothing to either sum; nor does any image with m = 0.
  - Σm and the share of images with m > 0 are reported for `ret`@τ_G and `ret`@−∞ (J3, CC-093), so a pass bought by deleting most mentions is visible next to the `ret`@+∞ row.
- **H_G** = NP(`ret`@τ_G) − NP(`ret`@−∞), pooled over both backbones (per image, tp and m summed over the backbones; numerator and denominator resampled together, §6.4). Per-backbone values are reported.
- **Pass** if both hold:
  - the 95% CI lower bound of H_G is **> 0**;
  - the CIDEr-D (stripped) cost, `ret`@τ_G − `ret`@−∞ pooled, has a point estimate **≥ −1.0**.
  - If Σ m at τ_G is 0 on the set, H_G cannot be estimated and counts as not passed.
- **Deciding set:** OV-dev-B. On XM-dev500, H_G (with OIV7 gold) is reported and does not decide.
- `ret`@+∞ (delete-all) is reported next to it, with mentions per image and CHAIR_i (its NP has an empty denominator).
- **Consequence.** H_G does not change the §7.2 verdict. It decides the guard claim:
  - if H_G fails at dev-B, the guard is reported as a registered negative, and "guard" leaves the title and the contributions;
  - it enters C's test prereg as P3 (§8) only if it passes at dev-B.
  - **Scope (J1, CC-093).** The pooled H_G decides. If one backbone's per-backbone H_G point estimate is ≤ 0, a pooled pass supports only a claim scoped to the other backbone, which is named in the title and contributions. "Guard" as a general claim needs both per-backbone point estimates > 0. No per-backbone CI is required.

## 8. Predictions to register in C's test prereg (if §7.2 PASS)

These are carried forward unchanged unless the judge rules otherwise. Their sets and thresholds are fixed here so that the test prereg cannot choose them after seeing dev-B.

| id | prediction | set |
|---|---|---|
| **P1 (primary)** | Pooled over both backbones, ΔCIDEr-D (stripped) of ret+guard − rand+guard (same k and τ, frozen §2) has a point estimate **> SESOI** and a 95% CI lower bound **> 0**. | OV-test minus the 60 dev299 near-duplicates of §3.4: **1,941 images** (C-g). The full 2,001 (with the 3 truncated images per §11) is a sensitivity analysis. |
| **P1b (secondary)** | ΔCIDEr-D against `zs` and against `fix`, reported with CIs. The expected size against `zs` (the plan says about +10) is stated in the test prereg; it does not gate. | OV-test, 1,941 (as P1) |
| **P2** | Per backbone, the 95% CI lower bound of ΔP_cm of ret+guard against `zs` is **> −1.0**. | OV-test, 1,941; full 2,001 as sensitivity (C-g) |
| **P3 (guard; only if H_G passes at dev-B, §7.5)** | H_G (pooled) has a 95% CI lower bound **> 0** and a CIDEr-D (stripped) cost with a point estimate **≥ −1.0** (C-a). A general guard claim also needs both per-backbone H_G point estimates > 0; otherwise the claim is scoped to the named backbone (J1, CC-093). Σm and the share of images with m > 0 are reported (J3). | OV-test, 1,941; XM-test2500 reported with OIV7 gold |
| **Named secondary (C-e)** | Neighbour-only object precision, all mentions, of ret+guard, reported with CIs. Co-primary only if the test prereg states the multiplicity before any test output. | OV-test, 1,941; XM-test2500 |
| **Secondary XM** | Pooled ΔCIDEr-D (stripped) of ret+guard − rand+guard has a 95% CI lower bound **> 0**, and verified precision (OIV7) of ret+guard against `zs` has a CI lower bound **> −1.0**. | XM-test2500 |
| **Length** | Rule L is reported for every test set. If it fires, the paper reports the P1 gain as "not separated from length". | all |

## 9. Budget and order (one RTX 3090)

### 9.1 Estimate

The estimate uses DESIGN §8 speeds and assumptions: Qwen 0.70 s zs, 0.91 / 1.40 s ICL; InternVL3 1.27 s zs, 1.65 / 2.54 s ICL; guard 2.5–3 items per image at 1.0–1.2 s.

| step | computation | GPU-h point | GPU-h high |
|---|---|---|---|
| SigLIP2, new queries | 1,425 images, one load | 0.05 | 0.10 |
| Qwen2.5-VL | 1,425 × (0.70 + 3 × 0.91 / 1.40) s | 1.36 | 1.94 |
| InternVL3 | 1,425 × (1.27 + 3 × 1.65 / 2.54) s | 2.46 | 3.52 |
| guard | 2 × 1,425 × 2.5–3 × 1.0–1.2 s | 1.98 | 2.85 |
| model loads (about 12 processes) | | 0.30 | 0.40 |
| **total** | | **about 6.2** | **about 8.8** |
| of which OV-dev-B block | 925 / 1,425 of the per-image rows, plus loads | about 4.0 | about 5.7 |
| of which XM-dev500 block | 500 / 1,425, plus loads | about 2.2 | about 3.1 |
| image-blind arm (C-c), 4 decodes | both sets, both backbones, after the main runs | 0.25 | 0.4 |
| **total with C-c** | | **about 6.5** | **about 9.2** |

A larger frozen k (8) sits inside the ×2.0 high assumption. A τ of −∞ or +∞ no longer removes that backbone's guard row (C-a): its `ret` items are still verified, which is inside the guard row above (that row assumed all three ICL arms). The NN baselines (C-b), the PTB column, the source-dataset share and the dose-response are CPU only.

### 9.2 Cap

- **Hard cap: min(10, 20 − stage-1 GPU-h) for stage 2**, counted as job wall time per block, with every step under `timeout` for the time left.
- QQ34 §2.4 item 3 caps C at 20 GPU-h "trên dev", and says to stop if that runs out before dev-B is passed. Dev-B counts inside the 20 h (CC-086 Q7, the plain and stricter reading). Whatever remains under the 20 h after stage 2 is the only budget for a possible stage-1b round.
- Stage 1 used **6.84 GPU-h** (job wall time; job.log `2026-10-22T11:29:36Z JOB DONE gpu_h_wall 684e-2`) of its 12-h cap. At the stage-1 point estimate (about 7.8 h) the cap is 10 h and does not bind. If the cap falls below the 8.8-h high estimate, the OV-dev-B block runs first and the XM-dev500 block runs only within what is left.
- **Priority if the cap binds (CC-087):**
  1. the OV-dev-B 16 runs and guard;
  2. the XM-dev500 16 runs and guard;
  3. the image-blind arm (C-c);
  4. the optional rows.
- Measured stage-1 speeds, s/image as per-run wall time (`finished_utc` − `started_utc`) ÷ images, over the 37 stage-1 decodes: Qwen2.5-VL `zs` 0.844, ICL k2 0.816–0.853, k4 0.853–0.893, k8 0.903–0.955; InternVL3 `zs` 1.455–1.505, ICL k2 1.492–1.692, k4 1.478–1.722, k8 1.585–1.769; s/item as verify-step wall time (load included) ÷ neighbour-only items: InternVL3-8B verifying Qwen2.5-VL 1.35 (P1, 914 s / 677) and 1.29 (P2, 1,797 s / 1,396), Qwen3-VL-8B verifying InternVL3 0.39 (P1, 281 s / 712) and 0.36 (P2, 420 s / 1,164), are disclosed next to §9.1. They do not change the cap.

### 9.3 Order on M3 (CC-086 Q2)

1. This prereg is committed. From then on, **E stage 1** (≤ 4 GPU-h, CC-081 Q2) and the **C OV-dev-B block** may each run, in either order on the queue, one at a time. The OV-dev-B block is: `embed` (OV-dev-B queries) → `exemplars` (CPU) → Qwen2.5 runs → InternVL3 runs → verifiers, each in its own process and never beside a generator → score → §7.2 verdict. The C block also needs the §1.2 conditions, the F5 judge check included.
2. Both have run. E's stage-2 prereg states that C's OV-dev-B outputs existed when it was written (X6).
3. E's stage-2 prereg is committed, or E stops.
4. **C XM-dev500 block** (same steps, then local verified precision; images and references copied to M3 only now, §1.2), and E's stage-2 run, queued one at a time on M3. The XM block runs whatever the §7.2 verdict.
5. **C image-blind arm (C-c)**, after both blocks' 16 runs and guard, within what is left of the cap: OV-dev-B, then XM-dev500. Its XM-dev500 decodes fall in the step-4 window, so X2 holds. It never runs before the XM block, so it cannot take cap owed to priority 2.

## 10. Disclosures (carried into the paper)

### 10.1 Stage 1

- **Reused `zs` file.** Stage 1 reused the dev-pool greedy file `dp_qwen25vl_7b_ktvic_dev299-short-T0.preds.json` (sha256 `5280baa49a6901fd862f7c376fc71d060477deea5235569afacca649f0378ded`) as the qwen25vl_7b `zs` arm and guard reference on dev299 (CC-079 Q3), with `guard.zs_ok` passing at run time. Stage 2 reuses no earlier output on any stage-2 image.
- **D1 (CC-084).** The OpenViIC dev annotation on M3 was a 911-key subset (`4b5347ff1a323922…` of release `2a68a3eb4d41926d…`), values unchanged. Stage 2 uses a 1,836-key subset made the same way (§1.2).
- **D2 (CC-084).** The scoring venv `/root/venv-c1score` is recorded in §6.2. No earlier kit_b CIDEr-D of 5280baa4 existed, so no reproduction check was possible.
- **Build fixes (CC-080, CC-082, implementation only).** These are the bounded batches, the dropped truncated memory image `00000007169.jpg`, the truncated decode of 3 OV-test images for de-duplication only, and the feature-cache provenance (LISTS_ADDENDUM).
- **Further stage-1 deviations:** none of the listed kinds. Every job step ran at attempt 1 (no retry), with no JOB STOP and no cap event (6.84 of 12 GPU-h). No step was rerun after a failure, all 37 decodes have `resumed: false` and `git_dirty: false` at head `6129e8e9`, and no `guard.zs_ok` failure or answer-position stop is logged. Recorded items: (i) the P0 rows at 04:52Z are τ = ±∞ only (§2 timing record; CC-093 W8, closed); (ii) `p1_internvl_items`/`p1_internvl_verify` ran a second time at 08:13:50–08:14:10Z for the T2 controls (items 712 → 716), a scheduled step of DESIGN §4.3, not a retry; (iii) CC-084 (D1, D2, Q3) was ruled at 04:41:31Z, after JOB START; `operator_step_CC079.txt` (04:38:45Z) records the repo's `data/xm3600/oiv7_labels.json` as "left in place", the run record records its removal under CC-084 Q3, and the removal time is not recorded. Stage 1 reads no XM3600 file. Items (ii) and (iii) go to the judge (CC-086b).
- All stage-1 configurations decoded are in the paper's "all configurations tried" appendix (QQ34 §2.4 item 5).

### 10.2 Paper A's 150 three-reference images (CC-079 C6 as amended by CC-081 (a))

- CC-079 C6 assumed that Paper A's 150-image XM3600 adjacency diagnostic lay inside XM600. **It does not.**
  - 27 of the 150 are in XM600.
  - 15 are in C's XM-dev500: 7 in E-dev-A and 8 in E-dev-B.
  - 108 are in C's XM-test2500.
- Paper A's N2 (2026-10-14, before C or E existed) read only the positions of shared objects across the three references of each image. It read no labels and no model output.
- **E2:** all 123 images outside XM600 stay in every C set. Every primary analysis includes them. C's test prereg adds the sensitivity analysis without the 108 (§11). No such sensitivity row is computed at dev-B.

### 10.3 Paper E overlap

- X5 (§3.3): E stage 1 makes zero-shot captions and guard scores on 121 E-dev-A images (inside XM-dev500) with C's backbones and prompt, before C's XM-dev500 block.
- E's local pair build read E-dev-A references and OIV7 labels in memory, printing counts only (E SPLIT_ADDENDUM §5).
- C reuses none of this (X3).

### 10.4 dev299 copies in OV-test (C-g, CC-087)

- 60 OV-test images are near-duplicates of dev299 images, the set on which §2 was picked (§3.4); 59 dev299 images have a copy in OV-test. They stay in OV-test under PD-31 but leave C's test primary. The full 2,001 is reported as a sensitivity analysis.
- XM-test2500 has none.

### 10.5 Licences and terms

Unchanged from stage 1 (CC-079 Q1, C2):
- KTVIC has no licence file; OpenViIC states research and non-commercial use;
- SigLIP2 is apache-2.0; SSCD is mit;
- XM3600 references and OIV7 labels are used as released (OIV7 labels are CC BY 4.0).

## 11. Obligations carried to C's test prereg

1. **CC-082 T6.** Fix, before any test decode, how the 3 truncated OV-test images (`00000000768.jpg`, 18 bytes; `00000001010.jpg`, 155 bytes; `00000005095.jpg`, 76 bytes) are decoded.
   - **Default:** the decoder wrapper retries only these files, only after the strict decode fails, with PIL `LOAD_TRUNCATED_IMAGES` set and reset around that one call. OV-test stays at 2,001.
   - Exclusion is allowed only if the test prereg fixes it before any test decode. Either choice is disclosed.
2. **CC-081 E2.** All 123 three-reference images outside XM600 stay in, and the primary includes them. A sensitivity analysis without the 108 XM-test2500 images is reported next to the XM-test2500 secondary and never replaces it.
3. **CC-081 E3 (test).**
   - E's test prereg is committed before any C test output on XM-test2500 exists.
   - E's test waits until C's test prereg is committed or C stops.
   - C's test reuses no E output unless C's test prereg names that reuse.
4. **Test gold off M3.** The OV-test annotation and the XM-test2500 references go to M3 only after the test prereg is committed, and the run record shows their sha and the time. The OIV7 labels never go to M3; verified precision is scored locally.
5. **The predictions of §8**, with the frozen §2 configuration, the SESOI (Q5), the metrics of §6 and the length rule L.
6. **One test look.** No "first" claims; the lineage wording of C4; Li et al. and ViG cited; the C-f framing and Related Work list (binding 11).
7. **C-g (CC-087).** The P1/P2 primary on OV-test **excludes** the 60 dev299 near-duplicates of §3.4 (`ov_test_dev299_neardup_files.txt`, sha256 `737e617a…`, committed next to this prereg with its producer `neardup_counts.py`; the test prereg pins it by sha256): 1,941 images. The full OV-test (2,001, with CC-082 T6) is reported as a sensitivity analysis. This is a tuning overlap, unlike CC-081 E2, so the exclusion is in the primary.
8. **C-a and C-e (CC-087).** P3 (H_G) only if H_G passed at dev-B, with the J1 scope clause; the named neighbour-only precision secondary; any co-primary status only with the multiplicity stated before any test output.
9. **J10 (CC-093).** The supplementary registered-rows table lists the guard AUROC diagnostic with its value, labelled "diagnostic; its interpretation is Paper E's", with no text claim.

## 12. Code changes stage 2 needs (listed, not written)

Recommended location: a new `scripts/c_stage2/` that imports the stage-1 modules unchanged and checks their sha256 against the stage-1 `SHA256SUMS`, so that the stage-1 files and pins stay byte-identical. The alternative, editing `scripts/c_stage1/`, changes the shas the stage-1 record cites.

1. **kit_b.** Done (7fa7b83, F1 CC-086): the `scripts/kit_b/` folder (6 files, BUILD_RECORD shas), of which stage 1 and stage 2 load `protocol_pilot` 6aee4282 and `punctuation_audit` a7e80240. Stage 2 also loads `ptb_protocol` ea5fbe6e (34323eb) for the PTB column, pinned by sha256. Point `score.KIT_B_DEFAULT` (or the stage-2 equivalent) at the committed path. Fold in the stale ":157 ponytail … add a cache" comment in `build_memory.py` only if the gatekeeper allows it under CC-080 K1, with a `SHA256SUMS` refresh.
2. **Sets.** Add `ov_dev_b` (`openviic/images`) and `xm_dev500` (`c_xm_dev500/images`) to the dataset table, with `manifest()` reading `lists.json` `sets`. Stage-1 code refuses both; stage-2 code accepts only these two sets plus nothing from dev-A.
3. **Carve-out in `refused()`.** Remove from the refused sha256 and `openviic` file-name sets exactly the 925 OV-dev-B and 500 XM-dev500 entries. Assert:
   - each carved-out sha is in no other `exclusion.json` sha list except `xm3600_all_images`;
   - no carved-out id is an XM600 id;
   - XM600 ids, XM-test2500, OV-test, KTVIC test, CV295, CHAIR-500 and UIT-ViIC test stay refused.

   Also refuse any file in the `c_xm_dev500/images` folder that is not an XM-dev500 sha.
4. **Run grid.** Replace the stage-1 grid with the 16 frozen main runs and the 4 image-blind runs of §4 (C-c). The k, order, template, τ and τ_G of §2 are read from `frozen_config.json`, pinned with this prereg by sha256. The selftest uses a dummy config, so the code does not wait for stage 1. Use the `c2_` prefix, a new output schema (`vsps.c_stage2.v1`) and a new resume key.
5. **Embed.** Embed only the stage-2 query sets. Load the memory vectors from the stage-1 embeddings file, pinned by sha256, refusing a different SigLIP2 revision or snapshot sha.
6. **Exemplars.** `ret`/`rand`/`fix` for `ov_dev_b` and `xm_dev500` (seeds per §4, near cut 0.92). Selftest that an XM query gets the first-member caption.
7. **Guard.** `items` and `score` accept the stage-2 manifests in place of the stage-1 dev manifests. Always verify the `ret` items of both backbones (C-a). Skip the `rand` and `fix` verifier passes for a backbone with τ ∈ {−∞, +∞}. Never guard the image-blind arm. `zs_ok` accepts only stage-2 `zs` files decoded by stage-2 code: no dev-pool or E reuse path.
8. **Score.**
   - `references()` for `ov_dev_b` (the 1,836-key subset) and `xm_dev500` (the subset file of §1.2).
   - A new `decide --phase confirm` that applies §7.2 and §7.3 with the frozen configuration as constants. It never calls `pick()`.
   - `SESOI = 2.0`, a gate of `2 * SESOI`, a separate stage-2 ledger, and `latest()` over that ledger only.
   - A Δ verified-precision bootstrap (ratio, as `pcm_ci`).
   - `decide --phase confirm` also reports H_G, its pass/fail and its J1 scope (general, or scoped to a named backbone; §7.5), and S3 (§7.3). τ_G is read from `frozen_config.json` and checked against the §2 rule (τ if finite, else 0.0).
   - Neighbour-only object precision, all mentions (§7.5), with the ratio bootstrap; the ret@τ_G and ret@+∞ rows.
   - The PTB-removed CIDEr-D column through `ptb_protocol.ptb` after `protocol_pilot.rdr` (CC-088 B-1). No §7 rule reads it.
   - The source-dataset share (C-d), the NN-baseline rows (C-b) and the cosine-bin dose-response (§6.5).
9. **Verified precision (local).** A `verified` mode that reads `oiv7_labels.json` locally through `xm3600_oiv7.statuses` and `caption_rows`, refuses on `VSPS_MACHINE_ID`, and refuses any image outside XM-dev500.
10. **Dev–test near-duplicate count** (§3.2, §3.4). A CPU, counts-only mode over the git-excluded feature cache, under the registered rule. The counts in this file were made by `neardup_counts.py` (§3.2), committed next to this file; this mode may reuse it unchanged.
11. **Selftests.**
    - Stage-2 modes accept OV-dev-B and XM-dev500.
    - Stage-1 modes still refuse them.
    - XM600, XM-test2500, OV-test and KTVIC test stay refused in every mode.
    - The carve-out size is exactly 925 + 500.
    - `decide --phase confirm` returns PASS, FAIL and JUDGE on synthetic ledgers, including the length rule and G1's 2 × SESOI point condition.
    - H_G: pass, fail on the CI, fail on the CIDEr-D cost, and the empty-denominator case; τ_G = 0.0 when τ = ±∞.
    - The image-blind arm passes no image to the model, and `decide --phase confirm` never reads a `blind` row into G1–G3, L, S1–S3 or H_G.
    - The `ret` verifier pass runs when τ = ±∞.
    - NN-consensus picks the caption with the highest mean CIDEr-D against the other k − 1, with df from the memory caption pool (never the scored set's references), ties to the nearer cluster, then the lower cluster id (J5, CC-093).
    - H_G per-backbone scope: a pooled pass with one per-backbone point ≤ 0 is reported as scoped to the other backbone (J1); Σm and the m > 0 share are written for `ret`@τ_G and `ret`@−∞ (J3).
12. **M3 job script and run record.** Two blocks and the image-blind step (§9.3), the 10-h cap with the §9.2 priority, retries ≤ 3, the operator checks of §1.2, and sha lists of the images copied.
13. **SHA256SUMS** next to this prereg, covering the stage-2 code.
14. **Image-blind decode (C-c).** The frozen `ret` prompt and examples through each generator's text-only path (no image tensor, no image placeholder), with its own run-id pattern (§4), greedy, 60 new tokens.
15. **NN baselines (C-b).** A CPU mode that builds NN-top1 and NN-consensus from the `ret` example lists and the run-time memory captions. NN-consensus CIDEr-D df is computed once from the memory caption pool; ties go to the nearer cluster, then the lower cluster id (J5, CC-093). Its files, the df table included, are outputs (binding 1), never committed.

## 13. Rulings and open points

### 13.1 CC-086 rulings on the draft's questions

| # | question | ruling (CC-086) |
|---|---|---|
| Q1 | XM-dev500 rule: C uses all 500, after E's stage-2 prereg or E's stop, with no reuse of E outputs in either direction unless named (X1–X5). | **YES (90%)**, with F3. X4 holds because E's stage-2 prereg is committed before any C output on XM-dev500. |
| Q2 | May C's OV-dev-B block run before E's stage-2 prereg is committed (X6)? | **YES (88%).** Once this prereg is committed, before or after E stage 1; the order between the two is free. Condition and XM-last rule as X6, X2. |
| Q3 | After an OV-dev-B FAIL, what confirms a stage-1b configuration? Does the XM-dev500 block still run? | **Partly YES (85%), F4.** The XM block runs whatever the OV outcome. After a FAIL, OV-dev-B and XM-dev500 are spent; C stops unless the stage-1b note names a confirmation set with no C output, before any stage-1b output, and the judge approves it. A carve-out from OV-test or XM-test2500 is a test-set change needing its own ruling before any test output (§7.2). |
| Q4 | The dev–test near-duplicate check of XM-dev500, and dropping hits from the dev side. | **YES (90%)**, run before commit (F2). Done: 0 hits (§3.2). |
| Q5 | Must C's test prereg keep SESOI +2.0 for P1? | **Keep +2.0 (92%).** |
| Q6 | XM-dev500 as a non-gating secondary, and local XM scoring. | **YES (90%).** S1/S2 do not gate and do not remove the XM-test2500 secondary. Verified precision is scored locally only; OIV7 labels never go to M3. |
| Q7 | Does dev-B count inside the 20 GPU-h? | **Inside (90%):** cap = min(10, 20 − stage-1 GPU-h). |
| Q8 | P2 per backbone, not pooled. | **Per backbone (92%).** |
| Q9 | May the stage-2 code follow this prereg in a later gatekeeper commit? | **YES (90%)**, with F5. |

### 13.2 CC-093 rulings on the CC-087 and CC-088 open points

| # | question | ruling (CC-093) |
|---|---|---|
| J1 | H_G (C-a): pooled or per backbone? | **Pooled decides, plus a scope clause (85%).** Image as unit, tp and m summed, per-backbone values reported. If one backbone's H_G point estimate is ≤ 0, a pooled pass supports only a claim scoped to the other backbone, named in the title and contributions; a general guard claim needs both point estimates > 0 (§7.5, §8 P3). |
| J2 | Which set decides H_G at dev-B? | **OV-dev-B decides; XM-dev500 is reported only (92%).** |
| J3 | H_G denominator. | **Accept (88%).** Distinct neighbour-only classes still in the final caption, no prefix cut; m = 0 images and fallbacks add to neither sum; Σm = 0 at τ_G is not passed. Added: Σm and the share of images with m > 0 for `ret`@τ_G and `ret`@−∞ (§6.5, §7.5). |
| J4 | Is the image-blind arm guarded? | **Unguarded, compared with `ret`@−∞ (90%).** |
| J5 | NN-consensus df and tie rule. | **Replaced (85%).** df from the memory caption pool, computed once on CPU, never committed; ties to the nearer cluster (higher SigLIP2 cosine), then the lower cluster id; the chosen caption is scored by kit B as every row (§4, §12). |
| J6 | Was the τ_G fallback fixed before τ was chosen? | **Satisfied (95%, after W8).** Times in §2: P0 rows ±∞ only; CC-087 06:48:13Z; first verify 07:36:22Z; first finite-τ row 07:56:46Z; PICK 07:57:51Z; decide later. |
| J7 | 1,941 for P1b and the named secondaries too? | **YES (90%):** P1, P1b, P2, P3 and the named OV-test secondaries; 2,001 is the sensitivity. XM-test2500 unaffected. |
| J8 | Dose-response bins. | **Accept (88%).** Per-set tertiles of the nearest-eligible-cluster cosine, computed from the set's queries before any stage-2 caption is scored; cuts in the run record; optional, named, non-gating. |
| J9 | 59 vs 60. | **Accept (95%).** 59 is the dev-side count, 60 the test-side union; the stage-2 and test preregs use 60; the dev-pools DESIGN wording is not edited. |
| J10 | Guard AUROC diagnostic under binding 12. | **Accept, with a disclosure (85%).** Computed and archived as registered; no validity claim in C's paper; listed with its value in the supplementary registered-rows table, labelled "diagnostic; its interpretation is Paper E's" (§6.5, §11 item 9). |

## 14. What this draft does not do

- It decodes, embeds and scores nothing. It reads no reference and no label.
- Its only computation is the CPU near-duplicate count of §3.2 and §3.4, over the git-excluded stage-1 feature cache. Like the lists build, it loads the KTVIC, OpenViIC test and XM3600 annotation files for their image ids and file names only; no caption or reference is printed or written.
- It changes no stage-1 file, rule or threshold.
- It holds no dataset caption and no prompt text. The prompt templates are cited by `TEMPLATE_SHA256`, and the near-duplicate rule by DESIGN §2.4.
- It is not committed and not copied to M3.
