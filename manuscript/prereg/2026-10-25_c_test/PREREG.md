# Paper C, test: pre-registration of the one-look test on OV-test and XM-test2500

**Label: TEST, ONE LOOK PER SET.** Committed after CC-103 (W1–W16) and CC-103a. No test image or test gold may reach M3 before E1–E7 (§1.2) hold.

| field | value |
|---|---|
| Paper | C: a controlled study of retrieval in-context captioning for Vietnamese (C-f, CC-087; CC-099 §2 "Framing"). The object guard appears only as a registered negative (CC-099 §1). |
| Authority | CC-099 §2 ("The C test prereg … must contain"); stage-2 PREREG §8 and §11; QQ34 §2.4 item 4 |
| Stage-1 design and lists | `manuscript/prereg/2026-10-22_c_stage1/DESIGN.md` sha256 `eacc9a9c737cec278c77ce5acd3b07422c9b0f7e661624ec42ba0454050ed53f`; `lists.json` sha256 `5c479f03e8be544f4cd12b5d997b5dc92b6c622df061760cd02f6ba82f6b4371` (stage-1 `SHA256SUMS`) |
| Stage-2 prereg (binding) | `manuscript/prereg/2026-10-22_c_stage2/PREREG.md` sha256 `6d039398c88ab00c5c303b671552b3f7c550d4d1a0c55e388ce7c03b249570b6`; `frozen_config.json` sha256 `2f0c32be7720b672f6e4aae229aba69da8742e0f9e32d34c5137e985ea36aa16` (pinned in `scripts/c_stage2/stage2.py:56–58`; committed 4ee4e4e, CC-086b) |
| Near-duplicate exclusion | `ov_test_dev299_neardup_files.txt` sha256 `737e617a966478d9bcadb0c932d72a6f8de7dd5c7e83c98730e1a88720f2f41f` (60 lines) (pinned in `scripts/c_stage2/stage2.py:56–58`; committed 4ee4e4e, CC-086b); producer `neardup_counts.py` sha256 `661698b10b76851d87f2548e25f3374ec43865d36db32f9fe09e07b7532cb3c7` (CC-086b; commit 4ee4e4e) |
| Stage-2 result read | `decide_final.json` sha256 `92a1f0e992cb974f0d2dfc59a765d1adbfa89338a6d7eed267edd583e2cd162b` (local only, `.session_backup/2026-10-22/c_stage2/final/`); ledger sha256 `be716482c6f934e975bdbc58927cfc42a4c0ff589c9c5f95affd67c03eac0938` (84 rows); verified sha256 `d69bddadfc686d47f4c89bd68ae8306679442288c4a6c0a8dcb7f62d0d7208b1` (30 rows) (C_STAGE2_RUN_RECORD, "sha256") |
| Rulings | CC-079 … CC-088, CC-093, CC-086b, CC-096, CC-097, CC-098, CC-099, CC-103, CC-103a |
| Written | 2026-10-25, CPU only; fixed for CC-103 on 2026-10-26. No OV-test or XM-test2500 image has been decoded, embedded, guarded or scored by Paper C, and no OIV7 label has been read. For the pinned lists (§3.1, §3.2) the producers read only the OpenViIC test annotation's keys, the OV-test image bytes (sha256), and the XM3600 annotation rows' `image_id` (counted per image); caption fields were parsed by the JSON loader but never used, printed or written; only keys, image bytes and per-image annotation counts were used (CC-103 W2, W14). |
| Pinned lists (CC-103 W2, W14) | `ov_test_files.tsv` sha256 `99d4fc49cc8283d1555d37b975cca5a32598ea0ec571d8bef8cf811df2c33695` (2,001 rows); `ov_test_primary1941.txt` sha256 `6458295ed1df42b854fed3807be3541cc452d6eeb79ee565780b72a777c807e2` (1,941 lines); `xm_test2500_threeref108.txt` sha256 `2d42a80972c6d0531bcc9d3d2aff43ced617b3bc808d1359b3577a564739fefb` (108 lines); producers `scripts/c_test/make_ov_test_manifest.py`, `scripts/c_test/make_xm_threeref108.py`; all in this folder's `SHA256SUMS` |
| Machine | M3 only: the test machine, which runs C's test steps only (CC-103a). Verified precision is scored locally on CPU. M4, the dev machine, never holds a test image or a C test output. |

Short paths: `PR2` = the stage-2 PREREG.md; `DF` = `decide_final.json`; `L2` = `.session_backup/machines/M3/root/outputs/c_stage2/ledger.jsonl` (row = line number); `CC-xxx` = `.session_backup/2026-10-13/decisions/CC-xxx.txt`.

## 0. Bindings

1. **All stage-1 and stage-2 bindings carry over** (PR2 §0, items 1–12), applied to the test sets. Outputs (captions, example files, embeddings, guard caches, ledgers) are never committed; Paper C commits scores, ids and sha256 only.
2. **One look per set.** Each test run is decoded once and scored once with the frozen configuration of §2. Each set's decide runs once. No configuration, threshold, metric, set or rule is changed after any test output exists. A re-score is allowed only to fix a scorer crash, and it must give identical numbers for rows already written (as PR2 binding 2).
3. **No test image or test gold on M3 before this prereg and the test code are committed** and the test code has its F5-style judge check, CC-103b (§1.2, §11.1).
4. **Nothing in this file is set from a test set.** The SESOI and every threshold come from PR2 or from the plan.
5. **The frozen configuration does not change** (CC-099 §1, "The frozen configuration (InternVL3 at τ = 0.1) is not changed"). The τ = −∞ numbers motivated by dev-B appear only as a labelled registered secondary (§8.4; CC-103 OQ-J, W12), never as InternVL3's result.
6. **No guard claim.** H_G failed at dev-B (DF `ov_dev_b.H_G.passed` = false; `xm_dev500.H_G.passed` = false). It is a registered negative, and there is no P3 (CC-099 §1, §2).
7. **Ownership (salami rule, CC-087; PR2 binding 12).** C owns retrieval in-context captioning only. C takes neither A's count control nor B's protocol as its own; it cites them. B's kit is used as the registered scorer (PR2 §6.1), and E's per-object statistic is not a C metric.
8. **No dataset caption** in any committed file, this one included.
9. **One look in practice (CC-103 W10).** No person or agent reads any test caption, ledger row, score or partial decide output before that block's decide has run. Monitoring uses progress logs only: counts, times, GPU-s and return codes. The OV decide, the XM decide on M3 and the local XM-b step each run once, and each JSON records the sha256 of every ledger it read (CC-086b O4).
10. **Framing (CC-103 W15).** PR2 binding 11's title wording ("with a post-hoc object guard") is amended by CC-099: the guard is a registered negative only (binding 6). PR2 bindings 5 and 6 carry over by name: no "first"; "a different VLM" with the lineage sentence; and the citations of Li et al. and ViG (PR2 §11 item 6).

## 1. Preconditions

### 1.1 Before this prereg is committed

1. The judge has ruled on this draft, including the open questions of §15 (CC-103), and the fixed draft has passed the fill and sha check CC-103a (CC-103 E1).
2. The OV-test manifest and the 108 list are pinned (§3.1 "Manifest", §3.2): `ov_test_files.tsv` (`99d4fc49…`), `ov_test_primary1941.txt` (`6458295e…`) and `xm_test2500_threeref108.txt` (`2d42a809…`), produced locally on CPU by `scripts/c_test/make_ov_test_manifest.py` and `scripts/c_test/make_xm_threeref108.py`, and listed with them in this folder's `SHA256SUMS` (CC-103 W2, W14, E1).
3. The gatekeeper's 6- and 8-gram scan of this file and of every file committed with it finds 0 hits apart from the known false positives (CC-079c), and the identity and path grep finds 0.

### 1.2 Before any test step on M3

CC-103 preconditions E1–E7 all hold, in order (CC-103 "Early run"):
1. **E1.** §1.1 holds and the gatekeeper has committed this prereg with the three pinned lists.
2. **E2.** The test code (§13) is committed through the gatekeeper with its `SHA256SUMS`, its selftests pass, and it has passed the separate judge round **CC-103b** (F5-style, as CC-096; the gatekeeper does not certify it), including the CPU decide replay and the CPU scorer replay of §13 item 10.
3. **E3.** A new M3 rental (the PI's decision): m3_rekey.sh; the rebuild by `.session_backup/machines/setup_gpu.sh m3`, recorded in `M3/m3_rebuild_2026-10-26.log` with its §9 result line; the three venv freezes equal to `685ffe2a`, `4b81b6b6` and `7332d343` and the five model pins pass; the repo at the E2 commit, tracked tree clean, `SHA256SUMS` verifying. Host and port go only into `~/.ssh/config` and `gpu_backup.sh`, never into a repo file.
4. **E4.** A fresh decode-parity check on the new rental, on M3 only; the 299 KTVIC dev299 images are copied to M3 by list into their own folder, sha-checked, with no KTVIC test file, and deleted after the E4 result is in the run record and before the OV staging (CC-103a): the frozen `ret` arm of each backbone re-decodes a fixed slice of ≥ 50 dev299 images through the test decode path, compared with the stage-1 preds of the frozen runs; ≥ 95% identical captions per backbone passes (CC-101 rule), otherwise stop and return to the judge. The result is in the run record before any test image moves.
5. **E5.** The gpu_backup loops (full and critical) run on the new rental, and `~/.config/vsps/usage_check.sh` leaves headroom to supervise a whole block with its mirror and deletion; a block is not started if the usage guard is likely to stop the session inside it.
6. **E6.** Staging exactly as §11.
7. **E7.** The test GPU cap of §12.
8. The host check of §11.2 passes for the block about to run.

## 2. Frozen configuration (carried over unchanged)

Read only from `frozen_config.json` (sha256 `2f0c32be…`), as stage 2 did. Nothing below is new.

| item | `qwen25vl_7b` | `internvl3_8b` | source |
|---|---|---|---|
| stage-1 picked run | `c1_qwen25vl_7b_ktvic_dev299-ret-k8-first-T1` | `c1_internvl3_8b_ktvic_dev299-ret-k4-last-T2` | `frozen_config.json` `models.*.stage1_run_id` |
| k | 8 | 4 | `models.*.k` |
| order | first | last | `models.*.order` |
| prompt tail | T1 | T2 | `models.*.tpl` |
| guard threshold τ | −∞ (`-inf`, no guard) | 0.10 (`0.10`) | `models.*.tau` |
| τ_G | 0.00 | 0.10 | `models.*.tau_G` (used by no test prediction; there is no P3) |

- Also unchanged (PR2 §2, l.96): the SigLIP2 embedder and revision, the memory (`lists.json` `memory`, 8,190 clusters, `lists.json` `counts.memory_clusters`), the stage-1 memory vectors (`emb.npz` sha256 `59e65f6f6432af97504c59c72fa07b644acbff26938e1365473fad659421f7c0`, PR2 §5.1), the 0.92 near cut, the prompt templates (`decode_icl.TEMPLATE_SHA256`), the `zs` prompt, the two generators and their revisions, greedy decoding with 60 new tokens, the guard question and verifiers, score s = p_with − p_without, and the deletion rule with its zero-shot fallback.
- No regeneration arm, no threshold tuning, no `pick()` call.

## 3. Sets

### 3.1 OV-test (primary set)

- **Definition.** All 2,001 OpenViIC test files (DESIGN §2.3, l.91; LISTS_ADDENDUM l.21, group `ov_test` 2,001), pinned as `ov_test_files.tsv` (below).
- **Entries and distinct images (CC-103 W2).** OV-test has 2,001 entries but **1,997 distinct images** (sha256): 4 byte-identical pairs, `00000005497.jpg`/`00000009980.jpg`, `00000006957.jpg`/`00000009950.jpg`, `00000009345.jpg`/`00000009997.jpg` and `00000009606.jpg`/`00000009892.jpg` (CC-103 l.53; producer output). None of the 8 is in the 60, so the primary has **1,941 entries / 1,937 distinct images**. Both entries of a pair are kept, each with its own references, and each entry is one bootstrap unit (CC-096 point 3).
- **Primary, 1,941 images:** OV-test minus the 60 file names of `ov_test_dev299_neardup_files.txt` (sha256 `737e617a…`; PR2 §3.4, l.165 and l.173; C-g, CC-087; CC-093 J7). The test code refuses a list with a different sha256.
- **Sensitivity set, 2,001 images:** the full OV-test (CC-099 §2, P1 bullet).
- **The 3 truncated files** (`00000000768.jpg`, `00000001010.jpg`, `00000005095.jpg`; `lists.json` `truncated_protected_decoded.ov_test`) are **not** among the 60 (PR2 §3.4, l.173), so they are inside **both** the 1,941 and the 2,001. Their decode rule (CC-082 T6; PR2 §11 item 1) is fixed here for every OV-test analysis:
  - **in every step that opens an OV-test image** (CC-103 W3): the SigLIP2 query embed, both generators and the verifier passes (§13 item 4; which verifier passes run is fixed by §4), the strict decode is tried first, and only these 3 files are retried after it fails, with PIL `LOAD_TRUNCATED_IMAGES` set and reset around that one call;
  - the run record lists, per step, which files took the retry path;
  - any other file that fails its strict decode is a **JOB STOP**, back to the judge;
  - if one of the 3 still fails after the retry, CC-082 T5 applies, fixed now: that file leaves both the 1,941 and the 2,001, is recorded as `unreadable_test_excluded`, and is disclosed;
  - this is disclosed in the paper.
- **Manifest (could not be taken from `lists.json`).** `lists.json` `sets` holds `ov_dev_a`, `ov_dev_b`, `xm_dev500` and `xm_test2500` only; `refuse.openviic_files` (3,007 names) mixes OV-test with OV-dev B-raw (`build_memory.py:285–286`). So this prereg pins, next to this file:
  - `ov_test_files.tsv` (sha256 `99d4fc49cc8283d1555d37b975cca5a32598ea0ec571d8bef8cf811df2c33695`): 2,001 rows (file name, image sha256), sorted by file name, from the OpenViIC test annotation's keys and the image bytes (caption fields parsed by the JSON loader but never used, printed or written; X2);
  - `ov_test_primary1941.txt` (sha256 `6458295ed1df42b854fed3807be3541cc452d6eeb79ee565780b72a777c807e2`): the 1,941 names, in the TSV order filtered;
  - producer `scripts/c_test/make_ov_test_manifest.py` (sha in `SHA256SUMS`), run locally on CPU on 2026-10-26.
  - Checks, all asserted by the producer before it writes anything, and all passed (CC-103 W2): pinned inputs (`lists.json` `5c479f03…`, the 60-list `737e617a…`, `exclusion.json` `c52a96d1…` = `scripts/c_stage1/decode_icl.py:40`); 2,001 names; 1,997 distinct sha256, the duplicate pairs equal to the 4 above; the 60-list lies inside the 2,001; none of the 8 paired files is in the 60; 1,941 entries / 1,937 distinct images; the 3 truncated files are in the 1,941; every name in `refuse.openviic_files`, every sha in `refuse.image_sha256`; 0 overlap by sha and by name with `ov_dev_a`, `ov_dev_b`, `xm_dev500`, `xm_test2500`, and 0 by sha with every `exclusion.json` `image_sha256` list; every output line is a file name (and sha256) only.
- References: the OpenViIC test captions as released, read from the test annotation file, which goes to M3 only for the OV block (§11).

### 3.2 XM-test2500 (secondary set)

- `lists.json` `sets.xm_test2500`: **2,500 images** (`lists.json` sets count; DESIGN §2.3, l.89).
- Near-duplicates against dev299 and XM-dev500: 0 (PR2 §3.4 table, l.167–168; §3.2 table, l.126). No exclusion.
- References: the XM3600 Vietnamese references of these 2,500 images, as released, copied as one subset file for the XM block only.
- **Three-reference sensitivity (CC-081 E2; PR2 §11 item 2):** the analysis without Paper A's 108 three-reference images in XM-test2500 (count: `manuscript/prereg/2026-10-22_e_stage1/SPLIT_ADDENDUM.md` §1 table; rule `scripts/e_stage1/e_lists.py:102`, images with ≥ 3 Vietnamese references). It is reported next to the XM prediction and never replaces it. **The 108 are pinned now (CC-103 W14)** as `xm_test2500_threeref108.txt` (sha256 `2d42a80972c6d0531bcc9d3d2aff43ced617b3bc808d1359b3577a564739fefb`; image ids only, sorted), made locally by `scripts/c_test/make_xm_threeref108.py` with e_lists.py:102's rule, counting annotation rows per image only; caption fields were parsed by the JSON loader but never used, printed or written; only keys, image bytes and per-image annotation counts were used; it asserts 150 three-reference images in XM3600 and 108 in XM-test2500 (`e_split.json` sha256 `795652f1…`, E stage-1 `SHA256SUMS` l.4; keys `counts.paperA_n2_three_ref_images`, `counts.paperA_n2_three_ref_in.xm_test2500`) and that the 108 are a subset of `lists.json` `sets.xm_test2500`. The test code asserts the list's sha256, a count of 108 and the subset relation; this replaces the run-time recount.
- OIV7 labels never go to M3; verified precision is scored locally only (CC-086 Q6; CC-099 §2).

### 3.3 Paper E

E stopped at stage 1 (CC-097: "no E stage-2 or test prereg will be written; E-dev-B and XM-test2500 were never touched by E"). The E3 test-order conditions of PR2 §11 item 3 therefore have no remaining object. C's test reuses no E output. E′ uses no C test set (CC-098, l.26 and l.47).

## 4. Arms and runs

Per (set, backbone), at the frozen k, order, template and τ of §2, the four main arms of PR2 §4: `ret`, `rand`, `fix`, `zs`. Run ids use a new `ct_` prefix (accepted, CC-103 OQ-7; verified in code at CC-103b) in place of `c2_`.

- Sets: `ov_test` (2,001 decoded once; the 1,941 is a subset of the same decodes) and `xm_test2500` (2,500). That gives 2 sets × 2 backbones × 4 arms = **16 main decodes**.
- `rand` seed `paperC|rand|<set>|<image id>`, `fix` seed `paperC|fix|<set>`, prefix of 8, as PR2 §4 with the new set names.
- **No image-blind arm at test** (CC-099 §2, "No image-blind arm at test; C-c stays a dev-B result").
- **NN-top1 and NN-consensus rows** (C-b; PR2 §4, l.189–192), CPU only, one NN-consensus row per distinct frozen k (k4, k8), df from the memory caption pool (J5, CC-093).
- **Verifier passes.** InternVL3's frozen τ = 0.10 is finite, so its `ret`, `rand` and `fix` items are verified (PR2 §5.3). Qwen's frozen τ is −∞, so no Qwen arm needs a verifier for any registered prediction. **PR2 §5.3's "ret items are always verified" (C-a) lapses with P3** (CC-103 OQ-2, W11): Qwen gets no verifier pass at test, and no H_G, τ_G or Qwen AUROC row is produced.

## 5. Retrieval, prompts, decoding, guard

PR2 §5 unchanged, with the test sets in place of the dev-B sets:
- memory vectors reused from `emb.npz` `59e65f6f…`; only the 4,501 test queries (2,001 + 2,500) are embedded;
- shown caption: for an OV-test query, the cluster's OpenViIC member if it has one, else its first member; for an XM query, the first member (PR2 §5.2);
- guard questions, verifiers and venvs as PR2 §5.3, except that C-a's "ret items are always verified" lapses (§4; CC-103 W11).

## 6. Metrics, scorer and bootstrap

### 6.1 Scorer

PR2 §6.1 unchanged: RDRSegmenter through committed `scripts/kit_b/protocol_pilot.py` (`6aee4282…`), CIDEr-D ×100 by kit B, trailing punctuation stripped by `punctuation_audit.py` (`a7e80240…`), PTB column by `ptb_protocol.py` (`ea5fbe6e…`), object matcher v2. **The decision column is `cider_s`, the stripped CIDEr-D** (PR2 §6.1 "Decisions use the stripped column"). Scoring environment as PR2 §6.2 (`/root/venv-c1score`, freeze sha256 `4b81b6b6…`), re-checked before the first test score.

### 6.2 CIDEr-D df for the 1,941 and the 2,001

PR2 §6.1 fixes "df over the scored set's references (per set)". Fixed (CC-103 OQ-3): the 1,941 and the 2,001 are **two scored sets**, each with its own df over its own references, from the same single decode; likewise the 2,500 and the 2,392 (XM-test2500 without the 108, §3.2). All scorings are fixed here, before any output, so none is a second look. The NN-consensus df stays on the memory pool (J5).

### 6.3 Bootstrap

- Paired image bootstrap, **B = 2000**, percentile 95% CI, `numpy.random.default_rng(0)`, indices `integers(0, n, (B, n))` drawn first from a fresh generator (`scripts/c_stage1/score.py:41`, `:248`, `:256`; `scripts/c_stage2/decide2.py:32–34`).
- **One index matrix per scored set**, with n = 1,941, 2,001 and 2,500 (and n = 2,392 for the XM sensitivity without the 108), used by every CI on that set (PR2 §6.4; CC-086). Each scored set's matrix is drawn fresh with its own n; the 1,941 matrix is not a subset of the 2,001 one (CC-103 W6).
- **Image order, pinned now (CC-103 W6).** OV-test: the sorted file-name order of `ov_test_files.tsv`; the 1,941 is that order filtered (`ov_test_primary1941.txt`). XM-test2500: the order of `lists.json` `sets.xm_test2500` as stored (not re-sorted); the 2,392 is that order filtered by `xm_test2500_threeref108.txt`. Decide re-indexes every run to the pinned order and asserts identical ids across the runs and both backbones.
- Pooling over backbones: per-image differences averaged over the two backbones, then resampled (`decide2.gate`, `np.mean(diffs, axis=0)`).
- Ratio statistics (ΔP_cm, Δ verified precision, neighbour-only precision): numerator and denominator resampled together over images (`score.pcm_ci`, `decide2.ratio`).

### 6.4 Reported per run

PR2 §6.5 rows, per run, at the frozen τ **and** at τ = −∞: CIDEr-D as written, stripped and PTB; CHAIR_i and mentions per image; ΔP_cm against `zs`; neighbour-only, rejected, deleted and fallback rates; the 4-gram copy rate; the near-verbatim copy share; the hit_max rate; the style report and source-dataset share (C-d); neighbour-only object precision, all mentions (C-e). No H_G row, no `ret`@τ_G row and no Qwen guard AUROC row is produced at test (no P3; CC-103 OQ-2, W11).
- **Rows nobody registered (CC-103 W11).** The InternVL3 τ-grid rows that the unchanged scorer writes (0.00, 0.20, 0.30, +∞) and InternVL3's guard AUROC are archived. They appear only in the supplementary all-rows table, labelled "not registered for any claim", with no text claim. Decide reads only the frozen-τ rows and the −∞ rows.

## 7. Predictions and decision rules (fixed now; one look per set)

Notation: for backbone m and image i, Δ_m,i = `cider_s`(ret_m at τ_m, i) − `cider_s`(rand_m at τ_m, i), with τ_m the frozen τ of §2 (same k, order, template). Pooled Δ_i = ½(Δ_qwen,i + Δ_internvl,i).

### 7.1 SESOI

**SESOI = +2.0 stripped CIDEr-D points** (PR2 §7.1, l.283 and l.287; CC-086 Q5; DF `SESOI` = 2.0). Unchanged.

### 7.2 P1 (primary; gates the paper's main claim)

| item | content |
|---|---|
| estimand | mean over images of pooled Δ_i (ret − rand, each backbone at its frozen configuration) |
| set | OV-test primary, **1,941** images (§3.1) |
| column | `cider_s` |
| CI | §6.3, n = 1,941 |
| pass | point estimate **> +2.0** (SESOI) **and** 95% CI lower bound **> 0** (PR2 §8 P1, l.347; CC-099 §2) |
| fail | either condition not met |
| sensitivity | the same estimand on the full **2,001** (§3.1), reported next to P1 and never replacing it |
| length rule L | computed per backbone at the frozen τ (mean syllables of the final captions, `ret` against `rand`) on the **1,941**, and reported on the 2,001 and on XM-test2500 (CC-103 W5). L fires if, for either backbone, \|len_ret − len_rand\| / len_rand > 0.10 on the 1,941 (PR2 §7.2 L; §8 "Length", l.353). If P1 passes and L fires, P1 is recorded as **"PASS, not separated from length"** |

Dev-B reference, for the reader only: pooled 6.04 [4.54, 7.58] (DF `ov_dev_b.gate.pooled_vs_rand`). It sets nothing here.

### 7.3 P1b (new; named; per backbone; non-gating; CC-099 §2)

| item | content |
|---|---|
| estimand | per backbone, mean over images of Δ_m,i |
| set | OV-test primary 1,941; 2,001 as sensitivity |
| column / CI | `cider_s`; §6.3 |
| prediction | **Qwen2.5-VL: point estimate > +2.0** (stated "confirmed" / "not confirmed"). **InternVL3: reported only**, point and CI, with no prediction |
| use | it decides the scope sentence of the paper (§9.2), and nothing else |

Dev-B reference: Qwen 9.67 [7.68, 11.72]; InternVL3 2.41 [0.57, 4.26] (DF `ov_dev_b.gate.per_model.*.vs_rand`).

### 7.4 P2 (per backbone; gates the object-precision claim)

| item | content |
|---|---|
| estimand | per backbone, ΔP_cm of `ret` at the frozen τ against `zs`: 100 · (Σ tp_cm − Σ tp_cm_zs) / Σ k_cm over images (`score.pcm_ci`) |
| set | OV-test primary 1,941; 2,001 as sensitivity (PR2 §8 P2, l.349) |
| CI | §6.3, ratio bootstrap |
| pass | for **each** backbone, the 95% CI lower bound **> −1.0** (PR2 §8 P2; CC-086 Q8) |
| fail | for a backbone whose lower bound is ≤ −1.0, no claim that retrieval keeps object precision is made for that backbone |

### 7.5 XM-test2500 prediction (secondary; does not gate P1)

| item | content |
|---|---|
| XM-a estimand | pooled mean over images of Δ_i on XM-test2500 (2,500), `cider_s`, §6.3 with n = 2,500 |
| XM-a pass | 95% CI lower bound **> 0** (PR2 §8 "Secondary XM", l.352) |
| point > 0 | printed as a descriptive number only, with no "confirmed" label (CC-103 OQ-1) |
| XM-b estimand | pooled over mentions and backbones, Δ verified precision (OIV7, Paper A's `caption_rows` rule) of `ret` at the frozen τ against `zs` (`decide2.s2`) |
| XM-b pass | 95% CI lower bound **> −1.0** (PR2 §8 l.352; CC-086 Q6) |
| scoring | CIDEr-D and CHAIR_i on M3; verified precision **locally only**; OIV7 labels never on M3 |
| sensitivity | XM-a and XM-b without the 108 three-reference images (§3.2), reported next to them |
| per backbone | Δ_m reported for both backbones, with CIs |
| **XM prediction** | **"confirmed" iff XM-a and XM-b both pass**, the registered conjunction of PR2 §8 (CC-103 OQ-1, W1); otherwise "not confirmed" |

CC-099 §2's "point > 0" for XM is withdrawn by CC-103 (it restated the dev-B S1 rule); PR2 §8 binds.

Dev-B reference: S1 1.46 [−1.07, 4.17]; S2 0.61 [−1.09, 2.40] (DF `xm_dev500.S1`, `xm_dev500.S2`); per backbone Qwen 4.44 [0.98, 7.85], InternVL3 −1.52 [−5.41, 2.51] (DF `xm_dev500.detail.per_model.*.vs_rand`).

### 7.6 Kill rules during the run

As PR2 §7.4: GPU cap (§12), verifier answer-position stop, at most 3 attempts per step then JOB STOP, refusal of any refused image before the model loads. A set that is not complete gives no verdict and is reported as incomplete.
- **Crash (CC-103 W8).** A crash may be resumed with the same code, with rows already written unchanged.
- **Cap stop (CC-103 W8, E7).** A cap stop is final for that set: no verdict, reported as incomplete, unless the judge extends the cap before any partial output of that set is read or scored.
- **Verifier stop (CC-103 W16).** If the Qwen3-VL answer-position stop fires for InternVL3's verifier on a set, that set's InternVL3 frozen arms are incomplete. P1/P2 (or, on XM-test2500, the XM prediction) are then not evaluated and are reported as incomplete. There is no fallback to τ = −∞.

## 8. Secondaries (named, all non-gating)

None of these can turn a failed P1, P2 or XM prediction into a pass, and none appears in the title, abstract or contributions as a result.

### 8.1 Listed by CC-099 §2 ("Named secondaries")

1. **Neighbour-only object precision, all mentions** (C-e; PR2 §7.5 definition, l.325–327), of `ret` at the frozen τ, per backbone and pooled, with CIs; Σm and the share of images with m > 0. OV-test 1,941 (gold: reference union) and XM-test2500 (OIV7, local). **Not co-primary** (C-e allows co-primary status only with multiplicity stated; this draft does not take it).
2. **NN-top1 and NN-consensus baselines** (C-b): Δ `ret` − NN with CIs, per backbone and pooled, on both sets.
3. **PTB-removed column** (CC-088 B-1) for P1, P1b and XM-a.
4. **Style report and source-dataset share** for `ret`, `rand`, `fix` (C-d).
5. **Per-backbone rows everywhere**: every pooled number is printed next to its two per-backbone values (CC-086b note; CC-099 §1).
6. **X5 disclosure** (PR2 §3.3): carried into the paper as written.

### 8.2 Renamed from PR2 §8 "P1b" (kept so that no registered row disappears; CC-103 OQ-4)

**S-zf:** ΔCIDEr-D (`cider_s`) of `ret` against `zs` and against `fix`, per backbone and pooled, with CIs, on OV-test 1,941 (2,001 as sensitivity) and XM-test2500. The expected size against `zs`, stated now as the plan requires (QQ34:165, "Mức kỳ vọng so với zero-shot (cỡ +10) cũng chốt sau dev-B"), is **about +10, pooled** (CC-103 OQ-4: QQ34:165 sits in the pooled-P1 context); the per-backbone values are printed beside it. It has no pass label; the paper states the observed value next to it.

### 8.3 Dose-response: reported, non-gating, always computed (CC-103 OQ-6, W7)

**Cosine-bin dose-response** of pooled ret − rand within per-set tertiles of the query's nearest-eligible-cluster SigLIP2 cosine, CPU. The cuts are per scored set, from that set's queries, and are recorded in the run record before any test caption is scored (PR2 §6.5; J8, CC-093). It is always computed and reported, and it does not gate.

### 8.4 Registered secondary (CC-103 OQ-J): per-backbone ret − rand at τ = −∞

**Adopted by CC-103 (OQ-J, W12) as written below; it is a registered secondary, motivated by dev-B (post hoc at dev-B, pre-specified at test).**

- **What it is.** A **non-gating secondary disclosed as motivated by dev-B**: the per-backbone ret − rand at τ = −∞ on OV-test (1,941; 2,001 as sensitivity) and XM-test2500 (2,392 as sensitivity) (CC-103 W12).
- **What does not change.** P1, P1b, P2 and the XM prediction stay at the frozen configuration, InternVL3 at τ = 0.10 (CC-099 §1; binding 5).
- **Motivation (post hoc, dev-B).** At τ = −∞ InternVL3's ret − rand was +5.36 [3.53, 7.12] on OV-dev-B and +1.54 [−2.12, 5.25] on XM-dev500, against the registered +2.41 and −1.52 at τ = 0.10 (`manuscript/ken/CRITIQUE_CE_BATCH5_2026-10-24.md` §1 table, from L2 rows 11/17 and 44/50; recomputed by the judge with the registered bootstrap as 5.356 [3.527, 7.119] and 1.541 [−2.120, 5.250], CC-103 l.34). Those contrasts are post hoc; only the per-run −∞ rows were registered as reported rows (PR2 §6.5, l.258).
- **Cost: 0 extra GPU-h (verified).**
  - The guard is a post-decode deletion. `scripts/c_stage1/score.py:116–136` (`variants`) builds every τ variant from the same decoded captions, and emits `-inf` for every non-`zs` run even before the guard cache is complete (`:122`).
  - At τ = −∞ nothing is rejected: `scripts/c_stage1/guard.py:94` rejects a class only if τ = +∞ or (τ > −∞ and s < τ), and `score.py:129` reads no verifier score at ±∞.
  - The stage-2 ledger has a `-inf` row for every ICL run: L2 rows 1, 7, 9, 11, 17, 23 (OV-dev-B) and 34, 40, 42, 44, 50, 56 (XM-dev500).
  - So the −∞ rows exist at test anyway (§6.4); the contrast is a CPU step in decide.
- **Scope of the row.**
  - Per backbone only; **no pooled −∞ row**, so it cannot compete with P1.
  - Qwen's frozen τ is already −∞, so its row is identical to P1b-Qwen and is not reported twice. **Only the InternVL3 row is new.**
  - Estimand: mean over images of `cider_s`(ret_internvl at −∞) − `cider_s`(rand_internvl at −∞), §6.3 CIs, same index matrix as the set's other CIs.
  - Label: "detected" if the 95% CI lower bound > 0, otherwise "not detected", on each set (XM-dev500 showed nothing either way, so "replicated" would not fit).
- **Decide key (CC-103 W12).** Decide writes it under a separate key, `secondary_devb_motivated.internvl3_neg_inf`, and a selftest shows that no gate, scope rule or claim reads it.
- **Reporting rule.** Wherever it appears, the paper prints InternVL3's registered τ = 0.10 result first. Shown only in a table labelled "secondary, motivated by dev-B (post hoc at dev-B, pre-specified at test)". It never enters the title, abstract or contributions as InternVL3's result, and it changes no scope sentence of §9.2. The paper also shows the dev-B decomposition table, labelled post hoc (critique "Keep #1").

## 9. Multiplicity and what gates which claim

### 9.1 Multiplicity

- **One primary (P1)**, one test, α = 0.05 two-sided percentile CI; no adjustment.
- **P2** is a conjunction over the two backbones (intersection–union); requiring both lower bounds needs no adjustment. A one-backbone failure only scopes the claim (§7.4).
- **P1b, XM-a/b, §8:** non-gating, reported with unadjusted 95% CIs, and described as secondary. No family-wise claim is made from them.
- **No rescue:** a failed P1 is not rescued by the 2,001 sensitivity, P1b, the PTB column, the XM set, the τ = −∞ row or any subgroup.

### 9.2 Claims and their gates

| claim in the paper | needs |
|---|---|
| "retrieved examples beat random examples on OpenViIC test" (headline) | P1 pass **and** rule L does not fire on the 1,941 (CC-103 W5) |
| "retrieved examples beat random examples on OpenViIC test, but the gain is not separated from caption length" (replaces the headline) | P1 pass and L fires on the 1,941 (CC-103 W5) |
| scope sentence | only if P1 passes: the fixed mapping from P1b below (CC-103 OQ-5, W4); InternVL3 is described by its point and CI only. If P1 fails, no scope sentence is used and the P1b rows are printed as numbers only |
| "no object-precision cost" for backbone m | P2 pass for m |
| "the gain transfers to XM3600 Vietnamese" | XM-a pass, with XM-b printed next to it (CC-103 W1) |
| "the registered XM prediction is confirmed" | XM-a **and** XM-b pass (CC-103 W1) |
| any guard statement | none: registered negative from dev-B only |

**Scope sentence, fixed now (applied mechanically to the OV-test 1,941 P1b rows, only if P1 passes; CC-103 OQ-5, W4). The rows are exhaustive:**

| P1b outcome | sentence beside every pooled number |
|---|---|
| Qwen point > +2.0 and InternVL3 95% CI lower bound ≤ 0 | "carried mainly by Qwen2.5-VL; not detected for InternVL3" (CC-099 §1 wording) |
| Qwen point > +2.0, InternVL3 lower bound > 0, InternVL3 point < Qwen point | "carried mainly by Qwen2.5-VL; smaller for InternVL3", with InternVL3's point and CI |
| Qwen point > +2.0, InternVL3 lower bound > 0, InternVL3 point ≥ Qwen point | "present for both backbones", with both points and CIs |
| Qwen point ≤ +2.0, InternVL3 point > +2.0 and InternVL3 lower bound > 0 | "carried mainly by InternVL3; not at the SESOI for Qwen2.5-VL", with both points and CIs (CC-103 W4) |
| Qwen point ≤ +2.0, every other InternVL3 outcome | "not carried by either backbone at the SESOI", with both points and CIs |

## 10. Reporting rules for null or negative results

- Every registered row is reported with its value and CI, whatever its outcome, in the main text or the supplementary registered-rows table.
- **P1 fails:** the paper reports "the dev-B gain did not replicate on OV-test", with the number. The framing stays "a controlled study"; no claim of a retrieval gain is made, and no post-hoc analysis is offered in its place.
- **P1 passes on 1,941 and fails on 2,001 (or the reverse):** both are reported; the 1,941 decides.
- **Rule L fires (P1 passing):** P1 is recorded as "PASS, not separated from length", and the headline is replaced as in §9.2 (CC-103 W5).
- **P1b-Qwen fails:** reported as not confirmed; if P1 passes, the scope sentence is the matching Qwen ≤ +2.0 row of the §9.2 mapping; if P1 fails, no scope sentence (CC-103 W4).
- **P2 fails for a backbone:** that backbone's ΔP_cm is reported as a cost.
- **XM-a fails:** "the gain was not detected out of domain (XM3600)", with the CI. If the point is > 0 but the CI includes 0, the paper says so in those words, as a descriptive number with no "confirmed" label (CC-103 OQ-1).
- **XM-a passes, XM-b fails (CC-103 W1, CC-103a):** the paper states 'the gain transfers to XM3600 Vietnamese' with the XM-b estimate and its CI in the same sentence, and reports the registered XM prediction as 'not confirmed: its verified-precision part (XM-b) failed'. No sentence says retrieval keeps object precision on XM3600.
- **Guard:** reported only as the dev-B registered negative (DF `ov_dev_b.H_G`: +2.91 [0.46, 5.31] precision, cost −4.01), with Σm 714 → 80 for InternVL3 (DF `ov_dev_b.H_G.per_model.internvl3_8b.at_-inf.sum_m` and `at_tau_G.sum_m`). No test guard claim.
- J10 (CC-093): the dev-B guard AUROC row stays in the supplementary table, labelled "diagnostic; its interpretation is Paper E's".
- Every configuration tried in stages 1 and 2 stays in the "all configurations tried" appendix (QQ34 §2.4 item 5).

## 11. Test-copy rules (CC-099 §2; PR2 §11 item 4)

### 11.1 When test data may reach M3

Only after **all** of E1–E5 (§1.2): this prereg committed; the test code committed with its `SHA256SUMS`; CC-103b passed; the new rental rebuilt and parity-checked. Then one set at a time, in this order: **OV-test block, then XM-test2500 block** (CC-099 §2, "Order: OV-test, then XM-test2500. One block at a time, never alongside another paper's job"). **The XM-test2500 block runs whatever the OV-test verdict** (pre-committed, as PR2 §3.3 and CC-086 Q3; CC-103 W9); only the cap can prevent it.

Staging order (CC-103 E6): (1) OV block: images by the explicit manifest into `c_ov_test/images` and the annotation into `c_ov_test/`; sha-check 2,001 names and 1,997 shas; host check; run; decide once. (2) Mirror and sha-confirm; then delete the 2,001 images and the annotation from M3, recording times and shas. (3) XM block: images into `c_xm_test2500/images` and the reference subset; 2,500/2,500; host check; run; M3 decide once (XM-a). (4) Mirror, sha-confirm, then delete. (5) Local CPU: verified precision (XM-b), once. Never alongside another paper's job; OIV7 labels never go on M3; no dev-B or XM-dev500 image is re-staged (the CC-103b replays are CPU only). The C run ends and is cleaned up before any A-4 or B job is staged on M3, and nothing of A's or B's goes to M3 while a C test block is staged (CC-103 "Relative to A and B").

### 11.2 Per block

**OV-test block**
- The 2,001 images are copied by the explicit list `ov_test_files.tsv` into a new folder used for nothing else (`$NCS_DATA/datasets/c_ov_test/images`, accepted, CC-103 OQ-7), and sha-checked: 2,001 names, 1,997 distinct sha256 (§3.1).
- The OpenViIC test annotation is copied into the same folder, as released; the run record holds its sha256, key count (2,001) and copy time.
- Host check before the first step must pass (CC-103 W13):
  - the stage-2 absences hold: no XM-test2500 image (no XM-test2500 sha anywhere), no XM3600 reference file, no `xm3600/`, `xm3600_en/`, `c_xm_dev500/` or `e_dev_a_pairs/` folder, and no `oiv7_labels.json` anywhere under the repo or `$NCS_DATA` (as CC-096 point 2 and X1);
  - no OV-dev-B image, no OV-dev-B annotation subset;
  - the refused set is `lists.json` `refuse.image_sha256` minus the **1,997** OV-test sha256 (2,001 entries, 1,997 distinct images; §3.1);
  - present OV-test images are counted **by name** (2,001), and only inside `c_ov_test/images`, with none under `openviic/images`;
  - `c_ov_test/` may hold exactly one non-image file, the released test annotation under its file name fixed in code, whose key set must equal the 2,001 manifest names; its sha256 and key count go into the run record before the host check; any other file in `c_ov_test/` that is not in the manifest is refused (CC-103a point 3);
  - other papers' test images (`exclusion.json` lists) are counted only, as at stage 2.

**XM-test2500 block**
- Starts only after the OV-test block's deletion is recorded (§11.3).
- The 2,500 images go into a new folder used for nothing else (`$NCS_DATA/datasets/c_xm_test2500/images`, accepted, CC-103 OQ-7), never under `datasets/xm3600/` (CC-085), sha-checked 2,500/2,500; their Vietnamese references as one subset file in the same folder, values unchanged, with sha256 and key count (2,500) recorded.
- Host check (CC-103 W13): the same stage-2 absences as the OV block (with the XM-test2500 images now present only in `c_xm_test2500/`), plus no `c_ov_test/` folder, no OV-test annotation anywhere and no OV-test sha; the refused set is `refuse.image_sha256` minus the 2,500 XM-test2500 sha256 (2,500 distinct); XM600 and XM-dev500 images are refused; `c_xm_test2500/` may hold exactly one non-image file, the reference subset under its file name fixed in code, whose image-id set must equal the 2,500 ids of `sets.xm_test2500`, with Vietnamese references only; its sha256 and key count go into the run record before the host check; any other file in `c_xm_test2500/` that is not in the set is refused (CC-103a point 3).

### 11.3 Deletion after use

After each block: the outputs are mirrored and the mirror is sha-confirmed; then the block's images and gold are deleted from M3; the run record states the shas, counts and UTC times (as the CC-099 §3 clean-up). Verified-precision outputs, and anything derived from OIV7, are never copied to M3.

### 11.4 One look

Each block's decide runs once, and no one reads test outputs before it (binding 9; CC-103 W10). Its JSON records the sha256 of every ledger it read (CC-086b O4). No block is re-run after a decide. A crash may be resumed with the same code, with rows already written unchanged. A cap stop is final for that set: no verdict, reported as incomplete, unless the judge extends the cap before any partial output of that set is read or scored (§7.6; CC-103 W8).

## 12. Budget and blocks

| block | computation (CC-099 §2, from stage-2 rates) | GPU-h |
|---|---|---|
| OV-test, 2,001 images | 3.09 × 2,001 / 925 (ov block 3.09 GPU-h, C_STAGE2_RUN_RECORD "ov block") | about 6.7 |
| XM-test2500 | 1.41 × 2,500 / 500 (xm block 1.41 GPU-h, C_STAGE2_RUN_RECORD "xm block") | about 7.1 |
| **total** | 6.68 + 7.05 (CC-103 l.47; CC-099's 13.8 is the sum of rounded parts) | **about 13.7 (upper bound)** |
| **hard cap** | job wall time, every step under `timeout` for the time left; separate from C's dev cap of 20 GPU-h, of which 6.84 + 4.91 = 11.75 were used (CC-103 l.48, E7 l.151) | **20** |

- The stage-2 rates include the Qwen `ret` verifier pass, which CC-103 OQ-2 drops, so 13.7 h is an upper bound.
- Timing: **early run authorised by CC-103 after E1–E7** (§1.2), in an M3 window not shared with another paper's job; it fits before B's W-B window (11-10 to 11-20; CC-103 "Relative to A and B").
- A cap stop is final for that set (§7.6; CC-103 W8).
- **Priority if the cap binds:** (1) the OV-test 8 main decodes, InternVL3 verifier, score and decide; (2) the XM-test2500 block. The CPU rows (NN, PTB, style, dose-response, verified precision) cost no GPU.

## 13. Test code needed (items 1–10 listed, not written; CC-103b check before use)

The stage-2 code accepts only the two dev sets (`scripts/c_stage2/stage2.py:61–62` `SETS`; `manifest2`) and its host check fails on the OpenViIC test annotation and on any `xm3600*` folder (`stage2.py:239–241`). The test needs new code in `scripts/c_test/` (CC-103 OQ-7), importing the stage-1 and stage-2 modules unchanged and checking their shas:

1. Sets `ov_test` (`c_ov_test/images`, manifest `ov_test_files.tsv`) and `xm_test2500` (`c_xm_test2500/images`, `lists.json` `sets.xm_test2500`); the 1,941 list pinned by sha256 and asserted equal to the manifest minus `737e617a…`.
2. Carve-out from the stage-1 refusal: exactly the active block's set (OV: 2,001 names, 1,997 sha256; XM: 2,500 sha256; §11.2, CC-103 W13); every other test set stays refused; selftests as PR2 §12 item 11 with the test sets, including refusal of every non-active test set and the 1,997/2,001 carve-out (CC-103 E2(c)).
3. Run grid: the 16 main runs of §4, `ct_` prefix, new schema, new ledger, read from `frozen_config.json` `2f0c32be…`. No blind arm.
4. Truncated-file retry (§3.1), only for the 3 named files and in every image-opening step (SigLIP2 query embed, both generators, the verifier passes), with a selftest; any other strict-decode failure is a JOB STOP (CC-103 W3).
5. Scoring of the 1,941, the 2,001, the 2,500 and the 2,392 as four scored sets (§6.2); one bootstrap matrix per scored set, in the pinned order of §6.3, with the id-identity assert (CC-103 W6).
6. `decide --phase test` with P1, P1b, P2, XM-a, XM-b, the sensitivities and §8 rows; constants SESOI = 2.0, PCM floor −1.0, VP floor −1.0; no `pick()`. The XM prediction is the conjunction XM-a ∧ XM-b (§7.5). The InternVL3 −∞ row is written under `secondary_devb_motivated.internvl3_neg_inf`, which no gate, scope rule or claim reads, with a selftest (CC-103 W12). Decide reads only the frozen-τ and −∞ rows (CC-103 W11).
7. Local `verified` mode accepting `xm_test2500` only, refusing when `VSPS_MACHINE_ID` is set, refusing any outside image; the 108 list read from `xm_test2500_threeref108.txt` with its sha256, count 108 and subset of `sets.xm_test2500` asserted, or refuse (CC-103 W14).
8. Host check per §11.2; deletion steps per §11.3, writing shas and times to the run record.
9. M3 job script: two blocks in order, the XM block whatever P1 showed, cap 20 h, retries ≤ 3; no Qwen verifier pass (CC-103 OQ-2); a selftest that a cap stop is final (CC-103 E2(c)).
10. **Replay modes for CC-103b (CC-103 E2(a), (b)).** (a) CPU decide replay: `decide --phase test` on the mirrored stage-2 ledger `be716482…` plus verified `d69bddad…`, with `ov_dev_b` in the OV slot and `xm_dev500` in the XM slot, must reproduce DF `92a1f0e9…` exactly (G1 → P1, per_model → P1b, pcm → P2, S1 → XM-a point and CI, S2 → XM-b). (b) CPU scorer replay: the test scorer on the mirrored stage-2 preds of at least one OV-dev-B run pair (`ret` and `rand`, both backbones) must reproduce the L2 `cider_s` and `per_image` values exactly.
11. **Pinned-list producers (committed now).** `scripts/c_test/make_ov_test_manifest.py` (CC-103 W2) and `scripts/c_test/make_xm_threeref108.py` (CC-103 W14), CPU, local; shas in this folder's `SHA256SUMS`.

## 14. Disclosures carried into the paper

- C-g: 60 OV-test near-duplicates of dev299 leave the primary (PR2 §10.4).
- OV-test: 2,001 entries / 1,997 distinct images; primary 1,941 / 1,937. The 4 byte-identical pairs are kept, each entry with its own references and as one bootstrap unit (CC-103 W2; CC-096 point 3).
- CC-082 T6: the 3 truncated OV-test files were decoded with truncated loading, in every step that opens an OV-test image, strict decode first (CC-103 W3); any of them excluded under CC-082 T5 is disclosed.
- CC-081 E2: the 108 three-reference images stay in XM-test2500; the sensitivity without them is reported.
- X5 (PR2 §3.3), and E's stop (CC-097).
- The guard is a dev-B registered negative; InternVL3's frozen τ = 0.10 was chosen on KTVIC dev299 and kept.
- The two byte-identical OV-dev-B files (CC-096 point 3) concern dev-B only.
- Three OV-test images (00000000104.jpg, 00000001494.jpeg, 00000010529.png) are byte-identical to three OpenViIC dev files that the stage-1 protected-set filter (DESIGN l.86–87) removed from OV-dev-B; no dev set or memory entry shares their bytes.

## 15. Open questions (all ruled by CC-103)

| # | question | ruling (CC-103) | applied in |
|---|---|---|---|
| **OQ-J** | The τ = −∞ secondary of §8.4. | YES, as written, with W12 (83%) | §8.4, §13 item 6 |
| OQ-1 | XM pass rule. | PR2 §8 stands: XM-a (CI LB > 0) ∧ XM-b (VP LB > −1.0); CC-099 §2's "point > 0" withdrawn; point > 0 printed as a number only (93%) | §7.5, §9.2, §10 |
| OQ-2 | Qwen `ret` verifier pass at test. | Skip it; 13.7 h becomes an upper bound (88%) | §4, §6.4, §12 |
| OQ-3 | CIDEr-D df for the subsets. | Own df per scored set (1,941; 2,001; 2,500; 2,392); NN-consensus df stays on the memory pool (85%) | §6.2 |
| OQ-4 | The name P1b. | P1b = CC-099's per-backbone ret − rand; PR2's row = S-zf, pooled, about +10 vs `zs`; S-zf on XM accepted as a reported row (80%) | §8.2 |
| OQ-5 | Scope mapping. | Accepted after W4, only if P1 passes (85%) | §9.2 |
| OQ-6 | Dose-response. | Always computed and reported, non-gating, cuts per scored set before scoring (88%) | §8.3 |
| OQ-7 | `c_ov_test/`, `c_xm_test2500/`, `ct_`. | Accepted; verified in code at CC-103b (92%) | §4, §11.2, §13 |

## 16. What this draft does not do

- It decodes, embeds and scores nothing, and reads no label. For the OV-test manifest and the 108 list (§3.1, §3.2), caption fields were parsed by the JSON loader but never used, printed or written; only keys, image bytes and per-image annotation counts were used.
- It changes no stage-1 or stage-2 file, rule, threshold or frozen value.
- It holds no dataset caption, no prompt text and no host address.
- It holds no test data. It reaches M3 only as part of the repository.
