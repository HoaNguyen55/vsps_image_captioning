# Per-annotator H1–H3 on the overlap: read package, round 2 (Paper A)

This package is for the round-2 one-judge code read after CC-391 (NEXT_ROUND, round 1 of 3; CC-391.txt sha256 `da1f1105…`). It covers the registered row of `A_CERT_ANALYSIS_REG_v1_1.md` §10, l.243: "H1 to H3 on the 150 overlap images with each annotator's labels | descriptive; after the second annotator | plan §4" (owed by CC-372 N3 and CC-374 ruling 6).

**Expected counts, stated BEFORE any host run (CC-391 N4):**
- self-test: **N = 59** checks, ending `59 checks; selftest ok`;
- mutant harness: **M = 61**, ending `61/61 killed`, with no BAD_TARGET, SURVIVED or CRASH.

Nothing has run anywhere. On the laptop the writer ran only `python3 -I -m py_compile` on the two code files, `sha256sum`, `diff -u` (to write the round diff) and read-only `grep`/`sed`/`wc`/`ls`/`awk`. The host run is made once, on these round-2 bytes, never on the round-1 bytes (CC-391 B4).

## 0. Round 2: how each CC-391 item is closed

Line numbers are those of `a_cert_perann.py` and `a_cert_perann_mutants.py` at their round-2 shas (§1). The round diff is `PERANN_R1_R2.diff`.

| Item | Closed by |
|---|---|
| **B1** H2b on the overlap | `h2b_budgets` (l.182–190): label-free, before the key read, from `a_cert.sys_cell` and `a_cert.beta_B` on the 150 overlap positions, NOT intersected with I537. `h2b_rows` (l.193–212): after labels, x_s and x_s_hi (the `score_core` l.866–874 loop with i600 → overlap), covered, w_hat, n_covered, n_binding; the `a_cert.h2b_rule` word only as `reading_no_verdict`. Not printed: low_44, P_c, any PASS/FAIL. Every H2b row (block and per system) carries the stamp. `REASONS["H2b"]` is deleted. Checks `H2b_all_images_equals_score_core` (every Q2 field, floor at w0, counts and word = `score_core`'s H2b block, image set = all images) and `H2b_counts_binding_and_word_by_hand`; the invariance check `answers_outside_overlap_change_nothing` now covers the H2b rows (it compares whole annotator blocks); `overlap_rows_differ_from_all_image_rows` now includes an H2b U. Mutants H01–H06 (H2b x on all images; budgets on all images; x_s_hi without the remainder; covered at another grid w; index within I537; binding count from x_s). |
| **B2** gate-line content | The two need tuples are named lines (`end_need` l.282, `up_need` l.286). Six refusal checks, each with the line id PRESENT and one item missing or wrong: `refuses_end_line_without_phrase`, `refuses_end_line_with_other_R2_sha`, `refuses_unsealing_line_without_token`, `…_without_PI_sha`, `…_without_R2_sha`, `…_without_script_sha`. The fixture U-P id (`OPS-fx-up`) no longer contains the token, so the token is tested as content. Mutants G01 (content test dropped from `log_hit`), G02–G03 (each `end_need` item), G04–G07 (each `up_need` item). |
| **B3** label-free work before the key | `prepare` (l.215–230) builds `sub_world`, the STOP ranges `clabel_slope`, the unlabelled `fam_slopes` points, the golds, the H2b budgets, N_u and the H3 stream; a non-finite range, point slope or budget is a Fault (l.226). `score` calls it at l.358, before `read_key`. `compute` (l.232–243) only takes these as arguments. Check `nonfinite_overlap_faults_label_free_before_key` (made-up world whose overlap M is 0 for one system; key and label paths absent; the Fault word and the printed `FAULT Fault label-free`). Mutants P01 (construction moved after the labels) and P02 (finiteness check removed). |
| **B4** host tree and recipe | §7 rewritten: explicit allow-list (the E3 code-only list minus the E3 files, plus the kappa and perann files), forbidden list, import-failure rule, `test -e` refusals, venv and mutant scratch outside the tree, `mkdir -p` records, status.log with UTC, Python version, the tree digest and both return codes from `PIPESTATUS`, records named as listed, IP/host filter. |
| **B5** U-P template | §5: the U-P line cites L-e, L-f (main), the LAST L-g and the kappa unsealing id or "not yet", and states the display hold of CC-391 item 4. §8: the run line confirms that no L-g follows the cited one and that no rating server listens. |
| N1 | §5 holds one copy of each table. |
| N2 | D_bonf omitted, stated in D14 (`a_cert.h3_row` does not return the replicate vector of D; computing it would restate the estimator). |
| N3 | `REASONS["H1_interval"]` (l.67–71) states the fixed-matrix (H1) versus registered-function-call (H3) distinction. |
| N4 | Counts restated above; §6 lists updated. |
| N5 | The five checks named by no mutant are listed in §6; accepted by CC-391. |
| N6 | §8: before the real run the operator logs `git show HEAD:<path> \| sha256sum` for the four files and the registration sha. |
| N7 | §9 records the round-1 departure. |

## 1. Files (sha256)

| File | sha256 |
|---|---|
| `scripts/a_cert/a_cert_perann.py` (724 lines; numpy + the a_cert code) | see `SHA256SUMS_PERANN` (round-2 bytes) |
| `scripts/a_cert/a_cert_perann_mutants.py` (204 lines) | see `SHA256SUMS_PERANN` |
| `scripts/a_cert/PERANN_R1_R2.diff` (unified diff of the two code files, round 1 → round 2) | see `SHA256SUMS_PERANN` |
| `scripts/a_cert/PERANN_READ_PACKAGE.md` (this file) | see `SHA256SUMS_PERANN` |
| `scripts/a_cert/perann_r1_asread/` (444): the four round-1 files as read by CC-391 | `a_cert_perann.py` 5fc83845…, `a_cert_perann_mutants.py` 29b7da07…, `PERANN_READ_PACKAGE.md` fc36b393…, `SHA256SUMS_PERANN` 4210e635… |

**Imported, unchanged, pinned in code (`CODE_PINS`, l.38–51; checked before either module is imported; a mismatch raises `SystemExit`):** `a_cert.py` `2e872588baf6109fad20111aecd25e2504fd0096f9033a95649027a2eed46cf4`, `a_cert_kappa.py` `1a0be69411da6ca39a939526236ab9f1f108ee1681a380c3541fa958f29c753c`. Neither file, nor anything under `tools/obj_rater/`, was edited.

**Registered inputs (sha256 on disk):** reg v1.1 `e564b7b1…` (= `a_cert.SHA_REG`); reg v1.3 H2d `d0afcaf0…`; plan v1.1 `8ad28f67…`; `overlap_images.txt` `4f971966…`; base `assignment.json` `55e07337…`; `overlap_r2/assignment.json` `fc8aafe9…`; CC-367 `f37090f5…`, CC-372 `d8eb3d84…`, CC-374 `7599bb60…`, CC-391 `da1f1105…`.

## 2. What the code does

### Flow of `score` (l.341–370)

Every step before `read_labels` is label-free; a fault there prints `label-free`.

1. **`check_args`** (l.246–259): `--out` absent (one pass only); both label sha arguments 64 hex and distinct; `--labels-pi-sha` = PI1_SHA `ba362466…`; real mode only: this script, `a_cert.py`, `a_cert_kappa.py` and reg v1.1 equal their HEAD blobs, and reg v1.1 = `SHA_REG`.
2. **`public_inputs`** (l.262–271): the base assignment, the R2 assignment and `overlap_images.txt` match their pins; the overlap list holds 150 ids and equals the set of R2 screen images.
3. **`gate_lines`** (l.278–289): (i) a LOG line with the `--r2-end-line` id holding every item of `end_need` ("R2 finished all screens yes", the R2 copy's sha); (ii) after it, a line with the `--unseal-line` id holding every item of `up_need` (the token `a-perann-unseal`, the R2 sha, the PI sha, this script's sha256).
4. **FREEZE** via `a_cert.pinned_freeze`; its sha must equal `c51ea7dc…` (OPS-1112h, LOG l.2220). Used only for the pins-equality check.
5. **World**: `a_cert._score_world()` (600 images, unchanged); pins = FREEZE pins; 600 ids in real mode; `positions`; `check_restriction` (all-image restricted context reproduces the registered F and P points within 1e-9).
6. **`prepare`** (l.215–230), every label-free overlap quantity, with the finiteness Fault (B3).
7. **Key**: `read_key` (l.292–302; path allowed only inside its try, discarded in `finally`; key sha = KEY_SHA `a2cef894…`; the same bytes hashed and parsed), `key_targets` (l.305–313; 557 R2 part-1 questions, key part 1 on an overlap image; **457** overlap targets).
8. **Labels**: `read_labels` (l.316–327; the stage turns after-labels just before the first byte; `_OK` cleared in `finally`; bytes = arguments; rows parsed by `a_cert_kappa.answers`: last line wins, annotator "PI" in L1 and "R2" in L3, labels in Y/N/U/A), `label_checks` (l.330–338; qids within their assignments; both annotators answered all 457).
9. **`compute`** (l.232–243): per annotator, its answers restricted to the 457 targets go through `a_cert.human` → `a_cert.counts`; then H1 (`h1_rows`), H2b (`h2b_rows`), H3 (`h3_rows`); H2a and H2d are not-computable rows.
10. One atomic write (`a_cert.write_atomic`); stdout `{"wrote", "sha256"}`; on any fault only `FAULT <type> <label-free|after-labels>` and no file (`run_score`, l.373–384).

### Result content per annotator (`annotators.PI`, `annotators.R2`)

Every row carries `label` = "descriptive; no verdict; 150 overlap images; annotator PI|R2".

- **`H1.Q25`, `H1.Q3`:** `n_images` (150; |overlap ∩ I537|); `b_F`, `b_P` at `reg`, `lo`, `hi`.
- **`H1.interval`, `H1.rule_words`, `H2a`, `H2d`:** "not computable on the overlap subset", with the reason (`REASONS`, l.66–79).
- **`H2b`:** `n_images` (150); `systems` keyed by the public BUILD system names, each with its own label and `x`, `x_hi`, `U`, `f1`, `beta` (every grid w; None at 0), `floor_beta_w0`, `covered`, `w_hat`; `n_covered`, `n_binding`, `reading_no_verdict`.
- **`H3`:** `n_images`; `phi1`, `phi2`, `f0_hat`, `X`, `X_hi`, `D`, `D_hi`, `D_ci95`, `D_hi_ci95`, `reading_no_verdict` (all `a_cert.h3_row`); `n_ref_named_completed_absent`; `stream` (call and sha256 of rows 1..2000).

Top level: `n_images`, `provenance` (label copy shas, key, FREEZE, code, code pins, the two LOG line ids). The result holds no qid, image id, class, caption text, per-question row or label text (CC-391 item 4); `result_and_stdout_hold_no_qid_image_or_class` checks the whole body, now including the H2b rows.

## 3. Design choices, each with the line it rests on

| # | Choice | Rests on |
|---|---|---|
| D1 | Reuse, not copy: `_score_world`, `draw_two`, `gold_ref`, `human`, `counts`, `fam_slopes`, `clabel_slope`, `sys_cell`, `beta_B`, `h2b_rule`, `h3_row`, `pinned_freeze`, `write_atomic`, `committed` are called unchanged. Restated from `score_core` (Q10 pattern, each checked equal to `score_core` with the image set = all images): the H1 completed columns (l.947–948 → l.154–155), N_u (l.840–841 → l.165–170), the completed-absent count (l.860–861 → l.175), and the H2b block (l.866–881 → l.182–212). `score_core` itself is not called on a subset: its STOP guard uses the 600-image FREEZE ranges and its H2a/H2d take the certified set and scores from the 600-image FREEZE. | CC-374 ruling 6; CC-391 Q10 |
| D2 | The world stays the full 600 images; only an image index changes. Golds are drawn on all 600 ids. | reg §4.2 |
| D3 | Q25 and the twelve-system H2b on the 150 overlap images; Q3 on overlap ∩ I537 (size printed). | reg §1 l.59; CC-391 Q2 |
| D4 | H1 via `fam_slopes` on a restricted context (`sub_world`, l.118–129): s75 `full` = overlap positions, `M_pt` = mean \|objects_in\| over them (bracket's M); xm600 `idx` = overlap ∩ I537 with a one-row unit weight. Placeholder bootstrap rows are never reported. | reg §2 l.74, §3; CC-391 ruling 1 |
| D5 | `check_restriction` before labels. | code-fault guard |
| D6 | STOP guard on the overlap's own C-label corner ranges, now built in `prepare` before the key read. | reg §5; CC-391 Q9, B3 |
| D7 | H1 interval: not computed (fixed matrices on fixed sets). | reg §2 l.77; CC-391 Q3 |
| D8 | H1a/H1b/H1c words: not computed. | reg §10 l.243; §2 l.78; CC-391 Q4 |
| D9 | H2a, its secondary row, H2d: not computable. | reg §6 H2a, §8, §11; v1.3 §2–§3; CC-391 Q1 |
| D10 | **H2b computed on the overlap** (round 1 said not computable; overruled by CC-391 Q2). Budgets label-free in `prepare`; truth after labels; word only as `reading_no_verdict`; low_44 and P_c not printed. | CC-391 Q2, B1 |
| D11 | H3 on N_u within the overlap; stream `a_m1.boot_weights(150, default_rng(20261111), 2000)`, built once in `prepare`, paired across annotators. | reg l.196–208; CC-391 Q5, Q6 |
| D12 | PI labels from L1 (`ba362466…`), R2 from the last L-g copy; only the 457 overlap part-1 targets enter. | reg §3 l.83; CC-372 2(a), 2(e); CC-391 Q8 |
| D13 | Completeness: a Fault if either annotator lacks one of the 457. | CC-372 ruling 4 |
| D14 | Not computed: S2 golds, S3 rows, adversarial corner, X/f̂0 ratio, D_L; and **D_bonf (N2)**: `a_cert.h3_row` returns only the 95% percentiles, so a Bonferroni interval would need D's replicate vector, i.e. restating h3_row's estimator. The Bonferroni interval serves verdict multiplicity (reg §7 l.216); this row has no verdict. | reg §10 l.243; CC-391 N2 |
| D15 | Custody: one audit hook (`a_cert_kappa.refused` plus `data/results/a_cert/score/`); the key allowed only in `read_key`, the two copies only in `read_labels`. | CC-372 ruling 1 |
| D16 | Order: every label-free overlap quantity before the key read; a non-finite value is a label-free Fault. | CC-391 B3; CC-343 N12 |

## 4. Design questions: CC-391 rulings and points still open

**Ruled by CC-391 (bind round 2):** Q1 H2a/H2d not computable (upheld); Q2 H2b computed (overruled, now coded); Q3 H1 point only (upheld); Q4 no H1b/H1c comparator (upheld); Q5 H3 stream at n = 150 (upheld); Q6 `reading_no_verdict` for H3 and H2b (upheld); Q7 no kappa precondition in code (upheld); Q8 PI from L1 (upheld); Q9 STOP guard kept, ranges before the key (upheld, B3); Q10 restated expressions accepted, now including H2b; Q11 label text (upheld); Q12 ruling-8 items mapped as in §5.

**New, for the round-2 judge (recommended reading = coded):**

| # | Question | Recommended reading (coded) |
|---|---|---|
| Q13 | Each H2b per-system row carries the stamp as well as the H2b block ("every H2b row carries the stamp"). | Yes. |
| Q14 | `floor_beta_w0` is printed per system (CC-391 Q2 lists it among the label-free quantities). | Print it; it is a budget value, not a figure about labels. |
| Q15 | `check_restriction` compares with `abs(a − b) > 1e-9`, which a NaN on both sides would pass. The all-image registered slopes are finite by the a_cert gate, and every overlap value is finiteness-checked in `prepare`. | No change (the byte change would add an untested branch). |

## 5. Gate conditions (one copy; CC-391 N1)

**Checked in code** (the real run refuses unless all hold):
- **Arguments.** `--out` absent; two label shas 64 hex and distinct; PI sha = `ba362466…`.
- **Code and registration.** This script, `a_cert.py`, `a_cert_kappa.py` and reg v1.1 equal their HEAD blobs; reg v1.1 = `e564b7b1…`; `a_cert.py` and `a_cert_kappa.py` equal `CODE_PINS` at import.
- **Public inputs.** Assignments and overlap list match their pins; overlap = R2 screen images.
- **LOG lines.** End line: id + "R2 finished all screens yes" + the L3 sha. U-P line after it: id + token + R2 sha + PI sha + script sha. Each item is tested (B2).
- **FREEZE and world.** FREEZE pinned in the LOG at `c51ea7dc…`; world pins = FREEZE pins; restriction reproduces the registered slopes; every overlap quantity finite (before the key).
- **Key.** key.json = `a2cef894…`; 557 R2 part-1 questions; 457 targets (before any label byte).
- **Labels.** Bytes = arguments; annotator fields right; qids within their assignments; both annotators complete on the 457.

**CC-374 ruling 8 (a)–(h), mapped to this row (CC-391 Q12):**

| Item | Kappa meaning | Here |
|---|---|---|
| (a) | part-1 score pinned | Met (PIN-1112-a-cert-RESULT); not read by this code (the hook refuses it). |
| (b) | code committed after GO, with the CC sha | **Code:** HEAD blobs. **Operator:** GO CC sha in the commit message; OPS commit line. |
| (c) | L-e line (PI parts 1–3 finished) | **Operator:** cited by id in the U-P line. |
| (d) | L-f main line | **Operator:** cited by id in the U-P line. |
| (e) | last L-g, "R2 finished all screens yes", 444 copy | **Code:** end line; **operator:** no later L-g exists. |
| (f) | PI Q1 relay | Not applicable (no kappa gate here). |
| (g) | separate unsealing line | **Code:** the U-P line. |
| (h) | PI said nothing to R2 | **Operator:** the PI's statement in the U-P line. |

**U-P LOG line template (CC-391 B5).** The code requires, in this one line, the id token, `a-perann-unseal` and the three full shas.

```
U-P <UTC> | OPS-<id>-a-perann-unseal | reg v1.1 §10 l.243 and §12.7; CC-374 ruling 6; code read CC-391 and GO CC-<n>: per-annotator H1, H2b and H3 on the 150 base overlap images (descriptive; no verdict; H1 intervals and rule words, H2a and H2d not computable). Triggers: L-e <id>; L-f (main) <id>; LAST L-g <id> (no later L-g exists); kappa unsealing <id or "not yet">. Label copies: PI ba362466ebd9c50918076dcf5865fbac9c5cd6482288f4251fa1f76e0f2718b4; R2 <sha64>. Code a_cert_perann.py <sha64>, commit <hash>. PI statement: nothing said to R2 about any answer. Display hold (CC-391 item 4): the result is written 444 and not displayed; its one-judge result read carries a CUSTODY header and holds every figure from the PI and from the coordinator's reports until the later of L-e, R2's last L-g and the PI's top-up session-end line; nothing from it ever reaches the second annotator (CC-367 ruling 4 extends to any later session of theirs); no dashboard entry carries any figure or word from it.
```

**Untested by design** (accepted by CC-391 2(iv), with the operator evidence of N6 in §8): the three real-mode lines (`P["real"]`): the HEAD-blob check, the reg v1.1 sha check, the 600-image check. The import-time `CODE_PINS` check is covered (`code_pins_hold_and_other_sha_refused`, W21).

## 6. Self-test (N = 59) and mutants (M = 61)

### Fixture
`a_cert.fixture(br)`: 40 made-up images, the 12 BUILD system names, 8 mapped classes plus one unmapped, Q3 = images with k % 8 ≠ 0. Key and PI answers from `a_cert.fixture_labels(w)` (synthetic), with `annotator: "PI"` added. R2 answers drawn here (`default_rng(13)`, Y/N/U/A at .4/.4/.1/.1 on every part-1 qid of the overlap). Overlap = images with k % 4 ∈ {0, 1} (20 images, 5 outside the fixture's I537). Files in a temp dir under names the hook lets through. No real label, key entry, freeze value or result figure is used.

### Hand worlds
- **H3** (`H3_overlap_wiring_by_hand`): images i, j, k; overlap {i, k}; systems s {a,b},{a},{c,d} and t {b,e},{b},{d}; Open Images a present on i, d absent on k; golds i kp {b,x} once {x} twice {b}, j kp {a} once {a}, k kp {d} once {d}; answers (i,e) Y, (i,x) N, (j,b) Y, (k,c) unanswered. N_u: i {b,e}, j {a,b}, k {c}. On {i,k}: φ1 0, φ2 1, X 1, X_hi 2, f̂0 0, D 1, D_hi 2, completed-absent 2, NOT EVALUABLE, n_images 2.
- **H2b** (`H2b_counts_binding_and_word_by_hand`), same world, made-up budgets s (U 5, f1 1, floor 3) and t (U 2, f1 0, floor 4): s x 1 (a, OI present) and x_hi 2 (+ c, remainder); t x 1 and x_hi 1 (e, Y); covered both; w_hat 1/3 and 0; n_covered 2; n_binding 1 (s only; from x it would be 0); `h2b_rule([True, True], 1)` = "FAIL" (word only).

### Checks (6 + 13 + 7 + 31 + 2 = 59)
- **Unit (6):** `code_pins_hold_and_other_sha_refused`, `stamp_text`, `positions_by_hand_and_missing_id_fault`, `stop_guard_by_hand`, `H3_overlap_wiring_by_hand`, `H2b_counts_binding_and_word_by_hand`.
- **Fixture (13):** `restricted_M_on_all_images_equals_context_M`, `Q3_is_overlap_within_I537`, `restriction_on_all_images_reproduces_fam_slopes`, `H2b_all_images_equals_score_core`, `H1_all_images_equals_score_core_reg_lo_hi`, `H3_all_images_equals_score_core`, `overlap_rows_differ_from_all_image_rows`, `answers_outside_overlap_change_nothing`, `R2_rows_from_R2_answers_and_differ_from_PI`, `H1_n_images_Q25_overlap_Q3_within_I537`, `H3_stream_boot_weights_20_seed_20261111_rows_1_2000`, `not_computable_rows_with_their_reasons` (H1 interval, H1 rule words, H2a, H2d), `every_row_carries_the_label` (now with the H2b block and every H2b system row).
- **End to end (7):** `ok_list_cleared_after_score`, `score_writes_once_rows_equal_direct_compute`, `stdout_is_wrote_and_sha_only`, `result_and_stdout_hold_no_qid_image_or_class`, `second_run_refused_FAULT_type_label_free`, `after_labels_fault_prints_stage_and_writes_nothing`, `main_maps_score_argv_to_a_label_free_fault`.
- **Refusals and order (31):** the 23 refusals of round 1 (arguments ×4; public pins ×3 and overlap ≠ screens; LOG: no end line, no U-P line, U-P before end; FREEZE sha; world pins; restriction; key sha; R2 part-1 count and target count before labels; label sha; PI row in R2 file; R2 qid outside; PI qid outside; PI incomplete; R2 incomplete), `ok_list_empty_after_key_fault` (round 1), the six B2 content checks and `nonfinite_overlap_faults_label_free_before_key`. Label-free refusals run with absent label and key paths (absent label paths only for the key-derived ones), so a guard moved after a read fails its check.
- **Custody (2):** `custody_refuses_key_labels_and_part1_result`, `custody_hook_blocks_open_of_key_json`.

(Grouping as counted by grep on the source: 59 distinct `ck[...]` names.)

### Mutants (61)
Each replaces one target that occurs exactly once (checked by `grep -cF`, P01's four lines included); G02/G03, G04–G07 and H02/H05 share a target. Every named check exists among the 59.

| Group | Mutants |
|---|---|
| Wiring and values (21) | W01–W14, W16–W21 as round 1; W15 now "H2d reason of H2a" (the H2b reason no longer exists) |
| H2b (6) | H01 x on all images; H02 budgets on all images; H03 x_hi without remainder; H04 covered at grid w = 0.3; H05 budgets within I537; H06 binding count from x |
| Gate-line content (7) | G01 content test dropped; G02 end phrase dropped; G03 end R2 sha dropped; G04–G07 U-P token / R2 sha / PI sha / script sha dropped |
| Order (2) | P01 construction after the labels; P02 finiteness check removed |
| Refusals and fault rule (21) | S01–S21 as round 1 |
| Custody (4) | C01–C04 as round 1 |

Indirect kills (CC-371 harness rule; accepted by CC-391 2): W03, W04, W07, H01 through the invariance check; H02 through the overlap/all-images difference; W20; S13–S18; G02–G07 and P01–P02 die because, with the guard weakened, score proceeds to the absent key path and raises FileNotFoundError, not the Fault the check requires.

Checks named by no mutant (CC-391 N5, accepted): `R2_rows_from_R2_answers_and_differ_from_PI`, `every_row_carries_the_label`, `refuses_row_of_other_annotator`, `result_and_stdout_hold_no_qid_image_or_class`, `stdout_is_wrote_and_sha_only`.

## 7. Host recipe (CC-391 B4; rented host, CPU only, synthetic fixtures)

**Tree = an explicit code-only allow-list** (precedent: the E3 code-only tree, `host_checks_e3code/status.log` sha256 `1a0635c3…`). Each file is pushed at its laptop sha, which the operator re-hashes before the push:
- `rescap/`: `__init__.py`, `chair.py`, `metrics.py`, `metrics_svp.py`, `pipeline/{generate,realize,select,verify}.py`, `repro.py`, `svp/{__init__,entailment,matching}.py`, `vi/{__init__,classifier,color,lexicon}.py`, `viz.py`, `vlm/{__init__,base,mock,qwen_vl,registry,replay,vintern}.py`, `vocab.py`;
- `scripts/a_m1/a_m1.py`, `scripts/clean_supervision.py`, `scripts/g2b/score_g2b.py`, `scripts/n_f1/bracket.py`, `scripts/object_prf.py`, `scripts/pascal50s/p50.py`, `scripts/pascal50s/p50x.py`, `scripts/person_uncap.py`, `scripts/score_coco_probe.py`, `scripts/xm3600_oiv7.py`;
- `.session_backup/2026-10-14/r12_verify/evaluate_xm3600_predictions_v3.py`;
- `data/coco_probe/coco80_vi.json`, `data/coco_probe/chair_synonyms.txt` (lexicon files read at import);
- `scripts/a_cert/a_cert.py` (2e872588), `scripts/a_cert/a_cert_kappa.py` (1a0be694, stdlib imports only), `scripts/a_cert/a_cert_perann.py`, `scripts/a_cert/a_cert_perann_mutants.py`, `scripts/a_cert/SHA256SUMS_PERANN` (round-2 shas).
- NOT pushed (in the E3 list, not needed here): `a_cert_e3.py`, `a_cert_e3_mutants.py`, `CC-359.txt`, `A_CERT_ADDENDUM_E3_v1.md`.

**Forbidden on the host:** anything under `data/results/`, `data/datasets/`, `data/xm3600/`; any assignment, overlap list, `BUILD*.json`, `FREEZE*`, `LOG.md` or CC text; `~/vsps_labels*`, any `key.json` or label copy; any token.

**Import failure:** stop. Push only the named CODE file, with a logged line (E3 precedent), never a data, label, key or result file.

**Step 0 (host environment; one OPS line before the push).** A fresh Ubuntu 24.04 host lacks `python3.12-venv` (STATE 2026-11-13, infra lessons): `apt-get install -y --no-install-recommends python3.12-venv`, nothing else installed or upgraded; the line records the package version.

**Step 1 (laptop; one guarded push).** Re-hash every allow-list file against its laptop sha (a mismatch stops the work), then push the list in one stream into a path that must not exist:

```bash
tar cf - $FILES | ssh -o BatchMode=yes <host alias> 'test -e /root/a_perann && exit 1; test -e /root/a_perann_mut && exit 1; test -e /root/a_perann_records && exit 1; mkdir -p /root/a_perann && tar xf - -C /root/a_perann' 2>&1 | grep -v -E '([0-9]{1,3}\.){3}[0-9]{1,3}'
```

`$FILES` is the allow-list above, repo-root relative. A non-zero exit stops the work; nothing is pushed twice without a LOG line.

**Step 2 (host; runner, kept as `run_perann.sh` in the records, CC-374 W3):**

```bash
#!/bin/bash
set -u
TREE=/root/a_perann; VENV=/root/a_perann_venv; MUT=/root/a_perann_mut; REC=/root/a_perann_records
cd "$TREE" || exit 1               # the runner never starts outside the pushed tree
test -e "$MUT" && exit 1
mkdir -p "$REC" || exit 1
python3 -m venv "$VENV" && "$VENV/bin/pip" install numpy==2.5.4 || exit 1   # numpy of the a_cert host records
J="env CUDA_VISIBLE_DEVICES= OMP_NUM_THREADS=2 nice -n 19 ionice -c3 $VENV/bin/python -I -B"
{ echo "start $(date -u +%FT%TZ) tree $TREE (code only)"; "$VENV/bin/python" --version
  find . -type f -not -path '*/__pycache__/*' | sort | xargs sha256sum; } > "$REC/status.log" 2>&1
$J scripts/a_cert/a_cert_perann.py selftest --out "$REC/selftest_perann.json" 2>&1 | tee "$REC/selftest_perann.log"
echo "selftest rc ${PIPESTATUS[0]} $(date -u +%FT%TZ)" >> "$REC/status.log"
$J scripts/a_cert/a_cert_perann_mutants.py "$MUT" 2>&1 | tee "$REC/mutants_perann.log"
echo "mutants rc ${PIPESTATUS[0]} $(date -u +%FT%TZ)" >> "$REC/status.log"
cp "$MUT/mutants_result.json" "$REC/mutants_result_perann.json"
"$VENV/bin/pip" freeze > "$REC/venv_freeze.txt"
cp "$0" "$REC/run_perann.sh"
echo "DONE $(date -u +%FT%TZ)" >> "$REC/status.log"
(cd "$REC" && find . -maxdepth 1 -type f ! -name SHA256SUMS | sort | xargs sha256sum > SHA256SUMS)
```

The runner is started once, from a path outside the tree (for example `bash /root/run_perann.sh`), after step 1 exited 0; the tree, the scratch and the records paths did not exist before step 1, and the runner refuses to start outside the tree, so `status.log` hashes the pushed tree only. CPU only; no GPU job path is touched.

**Records** (pulled to `scripts/a_cert/host_checks_perann/`): `status.log`, `selftest_perann.log`, `selftest_perann.json`, `mutants_perann.log`, `mutants_result_perann.json`, `venv_freeze.txt`, `run_perann.sh`, `SHA256SUMS`. Before and after the pull, grep every file for dotted IPv4 addresses and host names; none may remain.

**Acceptance:** `59 checks; selftest ok`; `61/61 killed`, each KILLED with a non-empty `named_failed` and no `no_exception` entry; `selftest rc 0` and `mutants rc 0` in status.log; the status.log digest lines of the four a_cert files equal §1 and `SHA256SUMS_PERANN`; `script_sha256` / `source_sha256` equal the round-2 sha. No rerun after a failed acceptance without a judge line.

## 8. Real `score` (later; laptop only; after a round-2 GO, host records, the commit and the LOG lines of §5)

**Operator pre-run evidence, logged in the run line:**
- `git show HEAD:<path> | sha256sum` for `scripts/a_cert/a_cert_perann.py`, `scripts/a_cert/a_cert.py`, `scripts/a_cert/a_cert_kappa.py` and reg v1.1, each equal to its disk sha; reg v1.1 = `e564b7b1…` (CC-391 N6);
- no L-g line follows the one cited in the U-P line (B5);
- `ss -ltn | grep -E ':879[0-3]\b'` empty: no rating server listening (B5);
- `--out` does not exist and lies outside `~/vsps_labels*`.

```bash
OMP_NUM_THREADS=2 nice -n 15 ~/.venvs/c_stage1_lists/bin/python -I -B scripts/a_cert/a_cert_perann.py score \
  --labels-pi "$HOME/vsps_labels/xm600_gold/labels_PI.20261112T181546Z.jsonl" \
  --labels-pi-sha ba362466ebd9c50918076dcf5865fbac9c5cd6482288f4251fa1f76e0f2718b4 \
  --labels-r2 "<444 copy named in the LAST L-g>" --labels-r2-sha <sha64 from that L-g> \
  --key "$HOME/vsps_labels/xm600_gold/key.json" \
  --r2-end-line <last L-g id> --unseal-line <OPS-id-a-perann-unseal> \
  --out data/results/a_cert_perann/score/A_CERT_PERANN_RESULT.json
```

**After the run:** chmod 444; not displayed; a run line with UTC, command, rc and every input and result sha; a one-judge result read under the display hold of CC-391 item 4 (stated in the U-P line). Fault rule of CC-372 ruling 8 / CC-374: `FAULT <type> <stage>` logged verbatim; no rerun without a one-judge read; a label-free fault is a setup fault; a second after-labels fault goes to the PI.

## 9. What the writer read and did not read

**Round 1** (unchanged): reg v1.1 in full; reg v1.3 H2d (lines cut at 600); the VP v1.1 and E3 v1 addenda by grep only; plan v1.1; BUILD.json; BUILD_OVERLAP.json; the head and line count of `overlap_images.txt`; `a_cert.py`, `a_cert_kappa.py`, `KAPPA_READ_PACKAGE.md`, `a_cert_kappa_mutants.py` in full; `HOST_CHECKS.md` (cut 400); `bracket.py` l.80–239; the v3 evaluator l.120–260; `score_g2b.py` l.185–250; `object_prf.image_counts`; `a_m1.boot_weights`; `p50x.f0_hat`; `build_assignment.py` l.95–126 (key schema); CC-372, CC-374 in full; CC-367 (cut 300); LOG by grep cut at 300 (which showed the index lines of CC-369, CC-379 and CC-381, titles only; the ruling files were not opened).

**Round-1 departure (CC-391 N7), recorded:** once, `python3 -c` parsed the public committed `overlap_r2/assignment.json` and printed its top-level keys and first screen. Not repeated in round 2.

**Round 2:** CC-391 in full (sha256 checked = `da1f1105…`); `scripts/a_cert/host_checks_e3code/status.log` (the code-only list) and a listing of that folder; the round-1 files. No LOG.md read in round 2. Ran only `python3 -I -m py_compile`, `sha256sum`, `diff -u`, and read-only `grep`/`sed`/`wc`/`ls`/`awk`/`cat` on code and package files.

**Never opened, listed or stat-ed:** `~/vsps_labels*`, any label file, any `key.json`; FREEZE content (no hash taken; its sha is from LOG l.2220); `data/results/a_cert/score/`; `~/.vsps_sealed`; `data/results/a_e3/`, `data/results/a_cert_e3/`, any FREEZE_E3; the `a_new_method_2026-11-13*` and `calibration_2026-11-13_A_phaseB` folders; `paper_text/`; the rulings CC-369, CC-377, CC-379, CC-381, CC-386, CC-387.

Nothing was committed, staged or pushed; nothing was written to LOG.md. `py_compile` writes `scripts/a_cert/__pycache__/` (git-ignored, never staged).
