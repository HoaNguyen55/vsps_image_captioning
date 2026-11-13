# B-FECERT code package: notes for the code read (IRREVERSIBLE tier, CC-350 ruling 11)

Registration `manuscript/prereg/2026-11-12_b_fecert/B_FECERT_PREREG_v1_1.md` (736b7e6a…); rulings CC-350 and CC-353. Files: `family.py` (§2, §5.1 family), `b_fecert.py` (stages F, C, G, 1, pin, 2a, 2b, 3, H, plus `selftest`), `mutants.py` (60 mutants), `SHA256SUMS`. Written under CC-353 4(d). Nothing was run: only `python3 -m py_compile`. The tool `pair_server.py`, `pair.html` and `build_pairs.py` are not in this package.

## Run order (host only; CC-353 4(e))
`selftest`, then `mutants.py`, then the stages in order: F, C, G, 1, pin, 2a, 2b, 3, H. Every stage after F needs two things, or it refuses:
- `--prev`: the sha256 of the previous stage's file;
- a LOG pin line for that file in `--log`, in the `b_pa1.pin_line` form `<UTC> OPS-<id>-pin: <name> <sha> …`.

The previous-stage file named by `--prev`:

| Stage | `--prev` names |
|---|---|
| C | FAMILY.json |
| G | CENSUS.json |
| 1 | GATE2.json |
| pin | DEV.json, plus `--nc` NC.json |
| 2a | DEV.json, whose line must also carry NC.json; GATE2.json must have its own line; no RESULT*.json may exist |
| 2b | V.json |
| 3 | RESULT.json; PRINTED.json must be logged, or `--k-print` is given after 2026-11-15 05:00Z |
| H | FEID.json; one closing line must carry key.json and each labels_*.jsonl |

Every stage refuses to start after K-time (2026-11-16 05:00Z), and a stage that finishes after it is a FAULT. Outputs are written once. The code prints shas and never writes the LOG.

## Reused, not rewritten
- `kit_b/protocol_pilot.py`: `rdr`, `Cider`, `bleu4`, `rouge_l`, `ngrams`.
- `kit_b/ptb_protocol.py`: `load_refs`, `load_preds`.
- `b2_external/b2.py`: `parse`, `norm_id`, `sha_file`, `git_blob`.
- `kit_b/b2_controls.py`: the `THESIS` blob pins.
- `b_pa1/b_pa1.py`: `pin_line`.
- `rescap.metrics.CaptionMetrics` for r*.
- New code: `bleu_img` / `bleu_corpus` (per-image BLEU counts; the self-test checks the sum against `bleu4`) and the strict g2 domain (deliberately not `norm_tone`, which also rewrites the qúy type).

## Self-test checks (39; synthetic temp-dir fixtures, stub word units, stub r*)
family_enumeration, tone_domain, toy_tokens, f1_rule, matched_scoring, bootstrap_ref, same_draws, merge_by_tokens, bleu_counts, certificate_cases, near_margin, cp_points (0.0495076 and 0.0503393 at n = 59 and 58; √0.95; 0.05^(1/10)), p1_labels, p2_labels, nc_check, f_held_empty, census_uts, gate_rules, fe_id_tolerance, identify_labels, p4_fault, p3_labels, pair_strata, kappa_hand, h_labels, g_repro, env_pins, pipeline (F→H end to end), stage_order, gate_2a_pin, gate_2a_gate2, gate_2a_result, gate_2b_V, k_time, k_print, h_closing, dev_no_heldout, image_route (.png/.jpeg fixture), no_text.
Exit codes: 1 if any check FAILs, 2 if any CRASHes. A mutant counts as killed only on `SELFTEST FAIL <its named check>`.

## Assumed file schemas (please check each against SCHEMA_PRINT.txt or the source)
1. FL output files, parsed by `b2.parse`:
   - X4 and G2 `.txt`: `id<TAB>caption` (schema print: 2 tab fields).
   - X3 and Flickr `*_pred.json`: list of {image_id, caption} (schema print).
   - X1 and X2: no id key, so they fail §4.3 rule 1.
   - K2 `results.xlsx`: a metric table with no caption column, so it fails rule 1 (whether `openpyxl` is installed or not).
2. FL reference files:
   - `captions.txt`: `id<TAB>caption`, ids repeated per caption; a `#n` suffix is cut if present.
   - `*_gt.json`: COCO-like {images, annotations[image_id, caption]}.
   - Ids are normalised with `b2.norm_id`: extension stripped, digits made int.
3. Host layout of `--fl`:
   - `fetched/<X..>/…`, the b2_external `fetched/` tree;
   - `loc110504/VietnameseSportImageCaptioning/…`;
   - `vanngthi/ViECAP-Image-Captioning-Vietnamese/annotations/…`;
   - paths as in the schema print.
   - Which loc110504 file is which X4a–e system is not needed (pairs only).
4. KTVIC baselines: `--baselines` holds `result_resnetlstm.json` and `result_vittrans.json`, each a list of {image_id, caption} (the b2_controls l.350 loader). The registration's path `…/thesis_code_1a8d105/simple_evaluate/` does not exist locally: the files sit one level up, and `simple_evaluate/` is their path inside the thesis-code repository. Git blobs are checked against `b2_controls.THESIS`.
5. `$NCS_DATA` (protocol_pilot layout):
   - `datasets/ktvic/test_data.json`: images[id, filename], annotations[image_id, caption];
   - `datasets/uitviic/test_data.json` (G5);
   - `results/<name>.preds.json`;
   - `results/<name>.json` with `results[0].scores_scaled_x100.CIDEr` and `results[*].segmenter` (evaluate.py l.398-443);
   - `results/tone_norm/ktvic_side_by_side.json :: systems`;
   - `vncorenlp/VnCoreNLP-1.2.jar`.
6. b2_external score files (`--b2-score`, `scores.json`): there is no `segmenter` field. The census reads every `segmenter` value and every numeric-field name (for example `CIDEr_PYVI`). A hit is "underthesea" or a `_UTS` suffix; a `char`/`_CHR` hit is logged only.
7. `PRINTED.json` (written by another agent): `{"entries": [{"source", "system", "file": <name used here: ktvic_resnetlstm, ktvic_vittrans, X4a, G2_cnn_t5, X3_original, K2 …> or null, "metrics": {"CIDEr-D": "21.8", "BLEU-1": …}}]}`.
   - Values are strings, so the decimals are kept.
   - Metric keys: BLEU-1…4, METEOR, ROUGE-L, CIDEr-D; others are listed as not used.
   - The first entry per file is used.
8. Human arm:
   - `key.json`: {qid: {image, stratum P/U/C, left, right, a, b, d: {m_syl, m_word, m_pk}, repeat_of: qid|null}}, with d = a minus b.
   - Labels: server.py jsonl {qid, label A/B/T/X}; the last line wins.
   - `build_pairs.py` is not written yet and must emit this key.

## Ambiguities and the reading coded
- **Bootstrap.** `numpy.random.default_rng(20261112).integers(0, n, (10000, n))`, one matrix per image-list length. Percentiles use numpy's default (linear). sd_boot uses ddof = 1. z = ∞ when sd = 0 and D ≠ 0.
- **BLEU-4 certificate.** The kit's `bleu4` is corpus-level, so the per-image counts are resampled. ROUGE-L uses the per-image `rouge_l`.
- **G-repro.** Any mismatch among the 67 is a FAULT. All 73 are seen under P0; B_KAPPA's "exclude a U file" clause is not used.
- **Family rule.** `_?(mbr|selffuse)$`, then `_s4[234]$`, then p1-gold→p1 and seed4x→seed. Stage C FAULTs unless the result is 26 families.
- **tm/tf before case.** The domain is matched on lower-cased letters and the written case is kept.
- **F1.** A "failed string" is an empty output from a non-empty input, or a crash or misalignment of the unit. "Whitespace fallback" means no reference token contains "_".
- **Wheels.** `--pyvi-wheel` and `--uts-wheel` are recorded by name and sha. A FAULT is raised if the name lacks `-<installed version>-` or pyvi ≠ 0.1.1.
- **Point-sign flip in P1 reversal.** D under a held-out class has the opposite sign to the certified direction.
- **FE-PRED AUC.** Computed over comparisons significant under f0, as P(z0 of CHANGED < z0 of not CHANGED).
- **FE-ID.**
  - Only CIDEr-D, BLEU-4 and ROUGE-L identify, because non-r* members compute only these.
  - r* is its own class.
  - Margin = the smallest max-metric distance to another class.
  - r* enters F⁺, including the plant draw (`random.Random(20261113).choice` over the sorted F⁺ names, in S order), only if K-coco keeps every identification metric.
  - Units dropped by K-unit are left out of F⁺.
- **P3.**
  - M_new is taken over the in-scope metrics printed for either baseline, after K-coco drops.
  - K-coco runs r* on a toy English fixture before any baseline is scored.
- **Groups.**
  - Per-repository counts use the owner.
  - G6: K2 as one file, compared with the two baselines; the baseline pair stays in D.
- **Human arm.**
  - The κ CI uses `default_rng(20261112)`.
  - Margin bins use |d_m_word| for every stratum.
  - "R2 finished" means R2 answered every main qid; otherwise the single-rater wording applies.
- **English control.** NOT RUN, because no files were named at this code read (Q13).

## CC-353 items carried to this read
- N6b ("about 2 hours" on the page) belongs to `pair.html`, which is outside this package.
- N9: no key or label here calls the E4 mismatched row "P4". "P4" is only the method check.

## Disclosure
To make one text replacement in my own draft of `b_fecert.py`, I ran a `python3` heredoc (string replace, file write). It imported nothing from the project and read no data, but it was not `py_compile`.

I read `~/b_fecert_fetch/SCHEMA_PRINT.txt` (key names, types and counts only). I opened no fetched file, label folder or KTVIC reference or prediction file.

---

# Round 2 (CC-361, NEXT_ROUND on the round-1 bytes)

Diff base: the read-only snapshot `.session_backup/2026-11-12/b_fecert/code_r1/` (unchanged). Unified diffs: `scripts/b_fecert/B_FECERT_R1_R2.diff` (family.py, b_fecert.py, mutants.py) and `tools/obj_rater/PAIR_R1_R2.diff` (pair_server.py, pair.html, build_pairs.py). The pair tool's own round-2 table is in `tools/obj_rater/PAIR_READ_PACKAGE.md`. New plan text: `manuscript/prereg/2026-11-12_b_fecert/B_PREF_PLAN_ADDENDUM_SALT_v1.md` (D15, and the D16 slot).

**Nothing in round 2 has run.** The rented host hc2 was deleted at 2026-11-12T15:47Z, before the round-2 bytes were ready. Every round-2 self-test and mutant is therefore **written, not run**. On the laptop only `python3 -m py_compile` (cache under `~/b_fecert_stage/pycache`), `diff`, `sha256sum`, `grep` and `sed` were used. The D18 host records are **OWED** (recipe below).

## Per D item

Line numbers refer to the round-2 bytes. "check" is the `b_fecert.py selftest` check name, or "bp: …" for a `build_pairs.py --selftest` line. "mutant" is the id in `mutants.py`.

| D | What changed | Where (round 2) | Check | Mutant |
|---|---|---|---|---|
| D1 | Stage 3 reads the pinned PRINTED.json layout `values.{KTVIC,K2}[] {system, metric_as_printed, value_as_printed}` through `printed_entries`. The sha256 must equal `2a962a2b…`, or FAULT. In-code maps: rows 1) and 2) map to the two baselines; GRIT and the three K2 rows map to null; CIDEr maps to CIDEr-D; ROUGE and ROUGE-L map to ROUGE-L; BLEU-1, BLEU-4 and METEOR keep their names (registration §5.1, §6.3). Decimals come from `value_as_printed`. An unmapped system or metric, a metric printed twice for one system, or a value that is not a string is a FAULT. The self-test fixture (`_printed_fixture`) uses the real layout and the registered strings with synthetic numbers, and the chain's stage 3 reads it. | b_fecert.py l.96-104 (pins, maps), l.1327 `printed_entries`, l.1250 ff. `st_3`, `_printed_fixture` | printed_adapter; pipeline (stage 3 through the adapter) | R1 (ROUGE unmapped), R2 (unmapped system), R3 (sha not asserted) |
| D2 | No code. The coordinator appends the `OPS-<id>-pin: PRINTED.json 2a962a2b…` line in the b_pa1 form before stage 3. | — | — | — |
| D3 | Stage 1 writes `{epsilon: 10.0, eligible_images: {P,U,C}, images: {id: [{a, b, stratum, d_syl, d_word, d_pk}]}}` (plus the usual provenance fields of `rec`) once, by `write_once`. The `filename` key is no longer in the candidates: both tools read image names only from `test_data.json :: images[].filename`, and `image_files()` no longer accepts `file_name`. `build_pairs.load_inputs` STOPs unless the top level and every candidate are exactly in this contract. Stage H checks `eligible_images` keys. | b_fecert.py l.695 `CAND_FIELDS`, l.698 `candidates`; build_pairs.py l.85-97 | pairs_integration; bp: "stops on a candidate field outside …" | R4 (stage 1 writes `dword`), R5 (build_pairs contract check off) |
| D4 | Stage H reads `key.json` as build_pairs writes it: `{"salt", "items": {qid: {image, part, stratum, a, b, file_left, file_right, d_syl, d_word, d_pk, repeat_of}}}`. `key_items` FAULTs on any other field set. `ident` maps A to `file_left` and B to `file_right`. main = `part == "main"`, repeats = `part == "repeat"`, and practice is never used. `hi` and the margin bins use `d_word`. | b_fecert.py l.753-775, l.777 `human`, agreement `reps`, l.1379 `st_H` | key_contract (400-image build_pairs fixture: 30 repeats, 8 practice); h_labels; pairs_integration | R6 (practice as main), R7 (wrong field name in the contract), R8 (sides swapped) |
| D5 | Cross-package integration. In the chain, stage 1's `PAIR_CANDIDATES.json` goes to `build_pairs.build` (fixed salt), then to synthetic labels for PI and R2, then to the closing pin line and stage H. A second leg, `key_contract`, uses build_pairs' 400-image fixture, so repeats, practice and both salt paths are exercised. Stage 3 reads the real-layout PRINTED fixture. `mutants.py` now copies `tools/obj_rater/` as real files into the scratch tree (no mutant writes through a symlink) and can kill on a `build_pairs.py --selftest` line ("bp:" checks). There are 34 new mutants, R1-R34. | b_fecert.py `_chain`, `key_contract`; mutants.py `tree`, `one`, MUT R1-R34 | pairs_integration, key_contract | R1-R34 |
| D6 | underthesea must be 9.5.0 (`UTS_VERSION`) with wheel sha256 `81400f41…` (`UTS_WHEEL_SHA`, the wheel installed on hc2 for round 2), and `inspect.signature(word_tokenize)` must be recorded. Otherwise FAULT. Every wheel record is now required, not only when the package is present. In `family.f1` the blanket `except` is gone: a unit that raises is not a string failure. In `st_F`, F3 (toy strings) runs before F1, and any exception from a unit in F3 or F1 is a FAULT, never a K-unit drop. String-level failures (an empty output from a non-empty input, lost alignment) still follow F1. | b_fecert.py l.84 ff., l.881 `env_record`, l.927 `env_check`, l.976 `st_F`; family.py l.226 `f1` | env_pins (absent, 9.4.0, wrong wheel sha, no signature); f1_rule (a raising unit) | R9, R10, R11, R12 |
| D7 | `env_record` adds the pycocoevalcap version, a `rescap.metrics`/`pycocoevalcap` import flag, the `rescap/metrics.py` sha256 and `java -version`. `rstar_check` FAULTs unless pycocoevalcap is 1.2, the rescap sha is `e0296ec5…` and Java is `21.0.13.0.3`. It runs in stage F (through `env_check`; recorded in FAMILY.json) and again at the start of stage 3 (recorded as `env_rstar` in FEID.json). In `k_coco` an `ImportError` is a FAULT. Only other, scorer-level exceptions on the toy fixture follow K-coco. | b_fecert.py l.86-88, l.908-925, l.638 `k_coco`, `st_3` | env_pins; k_coco_import | R13, R14, R15 |
| D8 | `inputs()` checks, in every stage after F, that each other work file the stage reads has a LOG pin line with its current sha256 (`INPUTS`, l.1397; the `--prev` file keeps its `prev_ok` check). It also checks that `test_data.json` still has the sha256 recorded in FAMILY.json. Shas go to `rec["inputs_sha256"]`. SYSTEMS.tsv is bound by `systems_tsv_sha256` in CENSUS.json (see "not literal"). The pin stage now prints PAIR_CANDIDATES.json on the DEV/NC pin line, and stage H requires it to be logged. | b_fecert.py l.196 `inputs`, l.225 `systems`, l.1397 `INPUTS`, `run` | inputs_logged (DEV.json altered after its pin, refused in 2b; FAMILY refs sha; SYSTEMS.tsv); gate_2a_gate2; gate_2a_pin | R16, R17, R18, M41 (now on `INPUTS["2a"]`) |
| D9 | `provenance()`: each FL output equals its fetch record (git blob from `b2.A_SYSTEMS` for `fetched/`, MANIFEST.tsv sha256 for the loc110504 G2 outputs and the vanngthi G4 outputs), or FAULT. `group_refs`: G1-G4 references must equal CC-354 3(d) (609af61a, ac9cab7d, 2acef66e, f02cf2b9), or FAULT. GATE2.json records `refs_sha256`. `gate_files` re-checks the reference and output shas in 2a, 2b and 3. | b_fecert.py l.131-146, l.261, l.268, l.327, l.1146 | fl_provenance | R19, R20, R21 |
| D10 | `--b2-score` must be a directory holding at least one `*.json`; a file, an empty folder or no argument is a FAULT. CENSUS.json records `b2_score_sha256` for each file. | b_fecert.py l.1007 `census` | census_b2dir; census_uts | R22 |
| D11 | `rated_both`: one definition for the kappa gate and for the agreement rows. It keeps pairs both raters answered, with neither answering cannot. `kappa` sorts categories with `key=str`, so a None can no longer crash it. | b_fecert.py l.771, l.722 | kappa_gate (PI missed 2 screens: n = 8, κ = 1) | R23 |
| D12 | FE-ID metric set: `ID_METRICS = (BLEU-1, BLEU-4, ROUGE-L, CIDEr-D)` for non-r* members. BLEU-1 comes from the per-image counts (`bleu_corpus(S, 1)`). METEOR is excluded for non-r* members as a forced reading and disclosed in FEID.json (`METEOR_excluded_for_members`, `printed_used`). r* is held to every in-scope printed metric. The plant stays on CIDEr-D, BLEU-4 and ROUGE-L (`PLANT_METRICS`). | b_fecert.py l.89-95, l.404, l.571 `identify`, l.617 `fe_table`, `st_3` | identify_labels (BLEU-1 separates two classes; r* held to METEOR); bleu_counts (BLEU-1 by hand) | R24, R25 |
| D13 | **OPEN.** No PI answer to Q2 was in the LOG when this round was written, so the coded reading (a) stays as the default of CC-361: any mismatch among the scored files is a FAULT. The docstring states this. Reading (b) is not coded. FAMILY.json now lists the files without a committed score (`no_committed_score`). | b_fecert.py l.965 `grepro`, `st_F` | g_repro (mismatch on a non-S and on an S file) | R26 (a mismatch outside S not a FAULT) |
| D14 | (pair tool) build_pairs no longer checks that image files exist. pair_server checks, before it serves, that every assignment and practice image is listed in test_data.json and exists under `--images`. | build_pairs.py l.108-109; pair_server.py l.99-103 | bp: "built with no images folder …", "pair_server refuses to start when a served image is missing" | R29 |
| D15 | (pair tool) Salted qid: `qid = sha256(SALT|SEED|part|image|a|b)[:12]`, with `SALT = secrets.token_hex(16)` per build. The salt is kept only in key.json. The self-tests inject `"5a17" * 8`. The plan addendum is written. | build_pairs.py l.80, l.123 ff.; addendum | key_contract; bp: qid formula, salt-only-in-key, fresh salt per build, two-run fixture shas | R27, R28 |
| D16 | (pair tool) pair.html carries the registered Vietnamese block (CC-364, block sha256 `45d59b54…`) between `<!--BEGIN-VI-INSTRUCTIONS-->` and `<!--END-VI-INSTRUCTIONS-->`. pair_server recomputes the block from the six `<li>` and the one `<p>` and refuses to start on a mismatch. It serves the bytes it checked. On the laptop the block was recomputed with sed/awk and equals `45d59b54…`. | pair.html l.47-57; pair_server.py l.36-40, l.62, l.76 | bp: "pair_server starts on the built fixture with the real pair.html", "… differs by one character" (×2) | R30 (one character of pair.html altered), R31 |
| D17 | No code. The LOG access line is for the coordinator. | — | — | — |
| D18 | **OWED** (host deleted). Recipe below. | — | — | — |

NB items done in the round-2 bytes:
- NB2: `FE_PRED_AUC` is the literal §6.6 row over D ∪ FL, and `FE_PRED_AUC_f0_significant_EXTRA` is the labelled extra row.
- NB3: in `fl_inputs`, outputs are parsed before references are loaded; G5's UIT references are opened only if an output parses. The 10-row id rule is in the `group_refs` docstring.
- NB4: `main()` prints `ERROR: <type>`, exit 4.
- NB5: see the pair package.
- NB6: stage 1 uses `build_pairs.tok_diff`, and `syl_diff` is deleted.
- NB7: F3 rows carry `addition`.
- NB9: `--candidates-sha`, and the pin line carries PAIR_CANDIDATES.json.
- NB13: METEOR disclosure field.

Not done: NB8 (runtime timing, a host measurement), NB10 (disclose only) and NB11 (STATE/RESUME files, the coordinator's).

### Not literal, or for the round-2 panel
1. **D8, SYSTEMS.tsv.** It is not on the ruling's list. It is bound through the sha256 recorded in the logged CENSUS.json, not through a LOG line of its own.
2. **D6, "F1's except branch covers string-level failures only".** Coded as no `except` around the batch call. A unit that raises is a FAULT in stage F. String-level failures are the empty outputs and the alignment loss, as before.
3. **D6/D7 pins.** `UTS_VERSION`/`UTS_WHEEL_SHA` and `JAVA_VERSION` were taken from hc2 (round-2 setup, 11:44-11:51Z). If the next host's `java -version` is not `21.0.13.0.3`, or pip resolves another underthesea wheel, stage F and the selftest's real env check will FAULT. The pin must then be changed (one line, a diff read) before records. Recommended: install the same wheels (list below) and the same Ubuntu 24.04 `openjdk-21-jre-headless` build.
4. **D13** is open (see the table).
5. **Coded readings carried for an explicit ruling (NB19):** bootstrap, family rule, tm/tf before case, F1, wheels, point-sign flip, groups, English control NOT RUN, FE-ID as above, and the pair ambiguities 4-7 and 10 (pair package). Unchanged from round 1.
6. **The self-tests and mutants of round 2 have never run.** Some checks rely on the synthetic chain giving at least one stage-1 candidate. For example, `pairs_integration` asserts `main` is non-empty. By construction it should: `p1_s42-short` equals reference 0, so every image gives a C candidate against `fuse2_s42-short`. This is not verified. If the first host run fails an unmutated check, CC-361 ruling 3(a) stops the run, and a fix goes back to a diff read.

### Disclosure (round 2)
- The family.py edits were applied once with a `python3` heredoc (exact string replace, asserted once each, file write). It imported nothing from the project and read no data, but it was not `py_compile`. One `python3 -c ""` (empty) was also run by mistake. Every other edit used the editor tool.
- On hc2 (h1), round 2, all under `nice -n 19 ionice -c3`, `CUDA_VISIBLE_DEVICES=` and `OMP_NUM_THREADS=2`, CPU only, outside the A-E3 directories and tmux sessions. None of these are D18 records:
  - 11:44:03-11:45:13Z, own tmux `bfe_venv`: built `/root/venv-bfe` (script `bfe_venv_setup.sh`; log, freeze and wheel shas now in `.session_backup/machines/ATTR_H1_misc/outputs_bfe_checks/`).
  - 11:50:05Z: pushed the round-1 bytes plus the import closure to `/root/b_fecert_smoke_r1/`. The round-1 smoke selftest ran 11:50:09-11:50:14Z: 39 ok, 0 FAIL, 0 CRASH, wall 4.9 s (ruling 3(a): a smoke run, not a record).
  - 11:50:30-11:50:35Z: probe of pyvi, underthesea and r* on toy strings (both units load; r* returns BLEU-1..4, METEOR, ROUGE-L, CIDEr).
  - About 11:51Z: a second toy probe (both units join compounds such as Hà_Nội).
  - `java -version` rc 0, written to `java_version.txt`.
  - No KTVIC, FL, label or data file was on the host tree. NCS_DATA pointed at the empty `/root/bfe_empty_ncs`.

## D18 record runs on h2 (2026-11-13)
- **r2 (record, kept unedited):** OPS-1113be, 03:09:28Z-03:10:25Z, bytes as reported in round 2. Records are in `host_checks_r2/`. Selftest 47/47; build_pairs 39/39 twice, with equal fixture shas; mutants **killed 92 of 94**. SURVIVED R5 (the bad candidate crashed with a KeyError instead of a named FAIL) and R8 (`key_contract` gave the same count for swapped sides).
- **r2b (test side only):**
  - R5: `build_pairs.selftest.stops()` now returns False on any exception other than SystemExit, so the check FAILs by name.
  - R8: in `key_contract` both raters pick the side that shows caption a, so a swapped mapping changes the word-agreement count (all pairs against none). The within-rater raw agreement is now 1.0.
  - No scoring or analysis code changed.
  - **Expected counts are unchanged:** selftest 47/47; build_pairs PASS 39/39 twice; mutants **killed 94 of 94**.
  - Records go to `host_checks_r2b/`, including recipe run 5.

## D18 host records: recipe (an RTX 3090 rental; CPU only for these runs)

Terms (CC-361 ruling 3(a)):
- CPU only: `nice -n 19 ionice -c3`, `CUDA_VISIBLE_DEVICES=` on every python call, `OMP_NUM_THREADS=2`.
- A new minimal tree with no data, no `.session_backup/`, no FL, KTVIC reference, prediction or label file. `NCS_DATA` points at an empty directory.
- Wall cap 3 h.
- Stop at the first failed unmutated self-test or the first surviving mutant. One re-run for an infrastructure error only.
- Never beside a RUNNING Paper C CPU stage (`pgrep -af c_attr` first).
- Times from `date -u`. Every ssh output is piped through `grep -v -E '([0-9]{1,3}\.){3}[0-9]{1,3}'`, so versions are recorded in files and pulled.

```bash
# 0. laptop: the tree (code only; round-2 shas = scripts/b_fecert/SHA256SUMS and tools/obj_rater/PAIR_SHA256SUMS)
cd /mnt/d/vsps_image_captioning
tar -cf /tmp/bfe_tree.tar scripts/b_fecert/{family,b_fecert,mutants}.py scripts/kit_b/{protocol_pilot,ptb_protocol,b2_controls,exchangeability_audit}.py \
  scripts/b2_external/b2.py scripts/b_pa1/b_pa1.py scripts/grl/{common,id_counts}.py \
  rescap/{__init__,metrics,repro,vocab,chair}.py rescap/svp/{__init__,entailment,matching}.py \
  rescap/vi/{__init__,classifier,color,lexicon}.py tools/obj_rater/{pair_server.py,build_pairs.py,pair.html}
# 1. host: venv from pinned wheels (python3 = 3.12.3 on Ubuntu 24.04; Java: openjdk 21.0.13.0.3)
H=<alias>; ssh -o BatchMode=yes $H 'mkdir -p /root/b_fecert_tree /root/bfe_empty_ncs /root/outputs_bfe_checks && tar -xf - -C /root/b_fecert_tree' < /tmp/bfe_tree.tar
ssh -o BatchMode=yes $H 'set -e; export CUDA_VISIBLE_DEVICES= OMP_NUM_THREADS=2; N="nice -n 19 ionice -c3"; O=/root/outputs_bfe_checks
  $N /usr/bin/python3 -m venv /root/venv-bfe; P=/root/venv-bfe/bin/python; $N $P -m pip install -q pip==24.3.1
  mkdir -p /root/venv-bfe-wheels; $N $P -m pip download -q --dest /root/venv-bfe-wheels pyvi==0.1.1 underthesea==9.5.0 \
    pycocoevalcap==1.2 numpy==2.5.4 scipy==1.18.1 scikit-learn==1.9.1 python-crfsuite==0.9.12 sklearn-crfsuite==0.5.0 underthesea_core==3.3.2
  $N $P -m pip install -q --no-index --find-links /root/venv-bfe-wheels pyvi==0.1.1 underthesea==9.5.0 pycocoevalcap==1.2 numpy==2.5.4 scipy==1.18.1
  $P -m pip freeze > $O/pip_freeze.txt; (cd /root/venv-bfe-wheels && sha256sum *) > $O/wheels_sha256.txt; java -version > $O/java_version.txt 2>&1
  (cd /root/b_fecert_tree && find . -type f | sort | xargs sha256sum) > $O/TREE_SHA256.txt
  mkdir -p /root/b_fecert_tree/toy_vnc && cp -r /root/ncs-data/vncorenlp/VnCoreNLP-1.2.jar /root/ncs-data/vncorenlp/models /root/b_fecert_tree/toy_vnc/
  sha256sum /root/b_fecert_tree/toy_vnc/VnCoreNLP-1.2.jar > $O/jar_sha256.txt'
```
The wheel sha256 must equal the round-2 list (`.session_backup/machines/ATTR_H1_misc/outputs_bfe_checks/wheels_sha256.txt`):
- underthesea `81400f41…`;
- pyvi `e5e9e0e4…`;
- pycocoevalcap `083ed791…`;
- numpy `fbde6962…`;
- scipy `f55fa87b…`.

The jar sha256 must begin `9e2811cd`. The jar and `models/` come from the host setup's `/root/ncs-data/vncorenlp/`, used read-only.

Then each run below, with `date -u +%FT%TZ` before and after, in `/root/b_fecert_tree`, with `E=env CUDA_VISIBLE_DEVICES= OMP_NUM_THREADS=2 NCS_DATA=/root/bfe_empty_ncs nice -n 19 ionice -c3 /root/venv-bfe/bin/python -X utf8 -I -B`:

| # | Command | Output file | Expected |
|---|---|---|---|
| 1 | `$E scripts/b_fecert/b_fecert.py selftest` | `selftest_r2.log` | rc 0; `selftest: 47 ok, 0 FAIL, 0 CRASH of 47 checks` |
| 2 | `$E tools/obj_rater/build_pairs.py --selftest` | `bp_selftest_run1.log` | rc 0; `SELFTEST PASS 39/39`; two `fixture sha256` lines |
| 3 | same as 2 | `bp_selftest_run2.log` | rc 0; the two `fixture sha256` lines byte-equal to run 1 |
| 4 | `$E scripts/b_fecert/mutants.py --jobs 4` | `mutants_r2.log` | rc 0; `killed 94 of 94` (60 round-1 + 34 round-2); about 94 × 2 × 5 s / 4 jobs, a few minutes |
| 5 | toy env record, the snippet below | `env_toy_r2.json` | `env_check` passes; F3 for rdr, pyvi and uts without exception; `k_coco()` keeps CIDEr-D and BLEU-4 |

Toy env snippet (run 5; toy strings only; production functions, no stub):
```bash
$E -c 'import sys, json, argparse; from pathlib import Path; sys.path.insert(0, "scripts/b_fecert")
import b_fecert as BF, family as FM, protocol_pilot as E4
E4.VNC = Path("toy_vnc").resolve()
a = argparse.Namespace(pyvi_wheel="/root/venv-bfe-wheels/pyvi-0.1.1-py2.py3-none-any.whl",
                       uts_wheel="/root/venv-bfe-wheels/underthesea-9.5.0-py3-none-any.whl")
rec = BF.env_record(a); BF.env_check(rec)
f3 = {u: FM.f3(u) for u in ("rdr", "pyvi", "uts")}; ok, dropped, got = BF.k_coco()
print(json.dumps({"env": rec, "F3_equal": {u: [x["equal"] for x in v] for u, v in f3.items()}, "k_coco_ok": ok, "k_coco_dropped": dropped}))' > /root/outputs_bfe_checks/env_toy_r2.json
```
Pull `/root/outputs_bfe_checks/` to `scripts/b_fecert/host_checks_r2/`, check the shas on both sides, and `chmod 444` the copy. The record set:
- the tree sha listing;
- the pip freeze;
- the wheel shas;
- the java and jar records;
- the five logs with start and end UTC.

A different count, a CRASH, a SURVIVED line or any rc ≠ 0 stops the run under ruling 3(a).
