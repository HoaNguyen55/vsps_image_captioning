# A-CERT addendum VP v1.1: (V) a development re-computation of the certificate against a fuller gold on COCO-5000 and (P) its application to 15 published comparisons (Paper A)

Written 2026-11-11T07:26Z (`date -u`). vsps HEAD `0519b82`, branch `paper-v10`. Paper A at `vsps-paperA-spic` `e8aa602`.

v1.1 written 2026-11-11T08:53:29Z (`date -u`) from v1 (sha256 `60926c54…`) under CC-335 (sha256 `399096fd…`). Only the changes below were made; every other line is v1. Quoted CC-335 texts are verbatim, with its wrapped lines joined by single spaces. Line breaks kept from CC-335's layout: the break after the §V.4a heading; the B4 sentence and the four §P.4 additions are each set as their own bullet.

**Changes from v1** (CC-335 item codes; "own wording" marks text the CC does not quote)
- Title: "v1" → "v1.1" (own wording).
- B1: §V.4a inserted after §V.4 (verbatim); Q2's recommended answer replaced (verbatim).
- B2: title and §V heading replaced (verbatim); "Status" paragraph inserted as the first paragraph of §V.5 (verbatim); Q5's recommended answer replaced (verbatim); the §12 phrase replaced (verbatim).
- B3: §V.1 third bullet replaced; the second-bullet parenthesis replaced (both verbatim).
- B4: §V.8 labels K0, K-EV, K1, K2, K3 renamed KV0, KV-EV, KV1, KV2, KV3, and Q7's "(K1)" renamed "(KV1)". Every other "K…" term in this file is an A2 plan or entry-gate term and is unchanged. First bullet of §V.6 replaced (verbatim). Sentence added to "What binds this file" (verbatim). A2 plan file to be committed beside this file (the directory `manuscript/prereg/2026-11-10_a2_cpu_step/` holds this one file):
  - `manuscript/prereg/2026-11-10_a2_cpu_step/A2_CPU_STEP_PLAN_v1.md`, sha256 `cfea58d6bc810c72f04856c965bbf107ef2abaa74806c260e28f6a162cae8ae2`; not tracked by git at 2026-11-11T08:53:29Z (`git ls-files --error-unmatch` fails).
- B5: appended to §P.2 (verbatim). B6: appended to §P.3 (verbatim).
- N1: §V.2 G0 cell replaced (verbatim). N2: Q8's recommended answer replaced (verbatim). N3: sentence added to §P.1 (verbatim). N4: sentence added to the §V.6 transported-threshold row (verbatim). N5: §12 last sentence replaced (own wording, citing Ruling 9).
- Ruling 3: Disclosures label of Part V replaced by the Ruling 3 label (verbatim; Ruling 3 uses a comma where B2 uses a semicolon, and each is kept as its source has it); §V.1 "the validation is not trivial" → "the check is not trivial" (own wording).
- Ruling 4: sentence added to §11 that the gate is unchanged and that an H2d clause is the PI's decision (P-2) (own wording).
- Ruling 6: fetch only after this file is committed (own wording, §P.1); gt_cache.json default NO until a PI line answers P-1 (own wording, §P.2); the four additions to §P.4 appended as bullets (verbatim).
- Ruling 7: one line after the §13 table stating that CC-335 Rulings 2–7 answer Q1–Q10 and bind (own wording).
- Not in this file: N6 (METHOD_DELTA_A), N7 (paper package), N8 (code-read package), Ruling 8 (selftest additions; code), H2d (`A_CERT_ANALYSIS_REG_v1_2_H2D.md`).

**Status.** Draft for a one-judge FULL read (REVERSIBLE, 85). Nothing was run that produces a result, nothing was downloaded except the public arXiv page of §9, nothing was committed, no LOG line and no CC file were written. AI opinion throughout. `[read]` = read by the writer today; "chưa kiểm" = not verified by the writer.

**What binds this file.**
- The committed registration `A_CERT_ANALYSIS_REG_v1_1.md` (sha256 `e564b7b1…`) [read]. It is frozen. This addendum changes no rule, constant or verdict of it. The procedure of its §4 (orientation, `Δ_min`, caps, β, `w*`, α_S) is used unchanged; only the number of references k becomes a parameter, `c = (1 − w)/(k·w)` (A2 plan §3.4, `cfea58d6…`, untracked, never judge-read [read]).
- CC-333 [read]: the forecast (two additions), limits (i)–(ii), Q8 (the OPERA / "Less is More" row needs its own judge read, which rules on the OPERA-500 ids and `gt_cache.json`), N10 (COCO-5000 is spent Paper A data in a development role), P3 (A2-OC1 untouched). CC-334 W1–W3 [read].
- PI-1111c (method per paper; T1 on a blind card by 2026-11-18) and PI-1111g (LOG l.2170; certification folded into Paper A) [read, first 300 characters of each line].
- Data rules of `running-vsps-research-cycle` [read]: existing gold only; full splits; no caption text printed; post hoc rows labelled (PI-1110n).
- the A2 plan is committed beside this file as a pinned reference; only its §1.3-1.5 and §3.4-3.8 are incorporated, and it was never judge-read as a whole.

**Disclosures.**
- The writer did not open, list or stat `~/vsps_labels`, `~/.vsps_sealed`, `~/bpa1pull_1108`, `.session_backup/machines/HBT1/` or `.session_backup/2026-10-27/a1_precheck/raw/`, and called no port. No caption file, reference file or per-image file was opened.
- Read today, aggregates only: `r4_full5000_all9.json` (`332da8b6…`, tracked; per-system P, R, F1, M under each gold) and `e1_x1pb_verification_v2.json` (`184f9cca…`; the 15 pairs and 24 per-system rows). From the first file the writer computed the 36 precision orders at two references against the top gold (§V.1). This is a look at stored aggregates of data the paper analysed; every Part V number is therefore development, never confirmatory.
- Both parts use outputs the paper has analysed. Part V is labelled "development, outcome foreseeable from stored aggregates and an unreviewed calculation (disclosed)" (CC-335 Ruling 3); Part P is labelled POST HOC. Neither changes a registered label of Paper A.

---

## V. Development re-computation against a fuller gold on COCO-5000 (outcome largely foreseeable; disclosed)

### V.1 What is already known (POST HOC; from committed aggregates and from an unreviewed scratch)

From `r4_full5000_all9.json`, first two references (`refs2_firstk`) against `inst+refs5`, nine systems, point values [read; computed today]:
- Precision under two references lies between 59.2 and 84.9; under the top gold between 84.0 and 94.7. Between 15% and 41% of mentions are unknown under two references.
- **9 of the 36 precision orders flip** between two references and the top gold (9 with random two; 8 with the first reference and 7 with a random one; 5 at five). "Certify everything" is therefore wrong for 25% of pairs: the check is not trivial.
- All 9 flips have a two-reference margin of at most 1.64 points. The 25 pairs with a margin of at least 3.72 points all hold. Two holding pairs have margins of 0.12 and 1.18 points. A margin threshold between 1.64 and 3.72 points therefore certifies 25 of the 36 pairs with no error, and no margin threshold certifies more without error. At pair level (point aggregates), a margin ranking reaches 26 of 36 within 5% risk and no ranking can exceed 28 of 36, so K2 is near-determined not to pass. These are whole-set aggregates over the first two references, not per-draw values.

From the A2 plan §1.6 (dry calculation in an expired `/tmp`, unreviewed, not reproducible today; CHAIR_i orientation, fixed w = 0.2, per-cell budgets; chưa kiểm):
- k = 2: 222 of 720 pair-draws certified (31%), 0 of 222 wrong; 172 of 720 sign changes.
- k = 2: 263 of 1,440 cells over budget (18%); k = 5: 39 of 72 (54%). The floor (F_w) at w = 0.2 was therefore violated in many cells although no certified pair was wrong.

Consequence: validity at (k = 2, w = 0.20) is near-known and can only be re-computed, not predicted. The cells-over-budget result predicts that the floor itself is refuted on COCO. Both are registered below with their expected outcome stated, so that neither can be presented as a prediction that held.

### V.2 Data (all spent Paper A development data; no test set; no new label)

| Role | File | Pin |
|---|---|---|
| Nine systems, 5,000 captions each (`wc -l` today: 9 × 5,000) | the nine `*.shard0of1.jsonl` files of A2 plan §2.1 (`data/results/coco5000/` 4, `coco_transfer_full5000/` 4, `coco5000_vcd/` 1) | shas as A2 plan §2.1; re-hashed at freeze (chưa kiểm today) |
| Image ids | `data/results/a_dchecks/freeze/coco5000_ids.txt` | `d20da3dd…` (chưa kiểm today) |
| Instance gold, derived class sets | `data/results/a_dchecks/freeze/instance_gold_full5000.json` | `bd362951…` (chưa kiểm today) |
| Five references per image | `data/datasets/karpathy/dataset_coco.json` | `2fd99922…`; pinned dev input of A-M1 (CC-285r3). **G0:** licensed as spent development data by PI-1110g (LOG l.2039) for the A2 CPU step, which PI-1111g folded into Paper A |
| Matcher | `score_g2b.MATCH['coco80']['vi']` for outputs; English CHAIR synonyms for references, as in the paper's COCO-5000 family | `66c665c7…`, `d11db7e1…` (chưa kiểm today) |

All nine systems are one model family (first backbone, Vietnamese captions). No second-backbone output exists on COCO-5000 (its runs are on 295 and 231 images only) [read: directory listing]. Raw COCO annotation files are never opened.

### V.3 Golds and masking mechanisms (fixed now)

**Top gold** `G_top(i)` = classes named by any of the five references ∪ instance classes (the CHAIR gold; "instance-label-visible", not complete). **Truth of a pair:** `P_top(A) − P_top(B) > 0` in the certified direction; a tie is wrong. Secondary truth (no verdict): instance classes alone; it is the only one under which (A0) can fail.

**M-ref (primary; natural incompleteness, the kind XM3600-600 has).** k references drawn without replacement from the five, per image, `default_rng(20261114 + 100·k)`, images in ascending id, R = 20 draws. Known present = named by at least one drawn reference; no pair is known absent. Certificate: C-ref of v1.1 §4.2 with `c = (1 − w)/(k·w)`, V-B budget, grid w ∈ {0, 0.10, 0.20, 0.30, 0.50}, **primary k = 2 and w0 = 0.20** (the operating point of v1.1; not re-tuned). k = 1, 3, 5 and V-H are secondary rows.

**M-label (secondary; synthetic three-state gold that mimics a label gold).** Every (image, class) pair named by at least one system has its `G_top` status hidden with probability `h`, else kept (present or absent). Mean hidden share u ∈ {0.30, 0.57}, the range of mapped mentions without an Open Images status in the first family (v1.1 §9; source `xm3600_oiv7.json`, chưa kiểm today). Two laws: uniform (`h = u`); salience-dependent (`h ∝ 1/(1 + r)`, r = number of the five references naming the pair, scaled so the mean is u, capped at 1). Seed `default_rng(20261115)`, R = 20. Certificate: C-label of v1.1 §4.3 (cap X = U, no assumption). The hidden rates are fixed from XM3600 aggregates and the reference counts, not from any outcome on COCO.

### V.4 A fact about the reference-only certificate at w = 0 (AI derivation today; for the judge to check)

With a positives-only gold every unknown mention of B may be present. At the corner `x_B = U(B-only)`, `x_S = U(S)·1[n_A > n_B]`: if `n_A > n_B`, `Δ = (t_A + U(S))/n_A − 1 ≤ 0`; otherwise `Δ = t_A/n_A − 1 + U(S)/n_B ≤ U(S)(1/n_B − 1/n_A) ≤ 0`. So **C-ref at w = 0 never certifies a precision order.** All content of the reference-only certificate lies in the floor. The no-assumption certificate has content only when the gold has known-absent pairs (C-label). v1.1 §4.2 calls the w = 0 certificate "the headline"; for C-ref that headline is empty (Q2). The selftest checks the identity by enumeration; one C-ref certificate at w = 0 on real data is a code fault.

### V.4a Erratum to A_CERT_ANALYSIS_REG_v1_1.md (binding; registered before its freeze; changes no computation)

v1.1 §4.2 (l.124) and CC-333 Ruling 3 Q2 say "the w = 0 certificate is the headline". For C-ref this is withdrawn (CC-335 Ruling 2). With a positives-only gold every mention of a system is known present or unknown, so the completion that sets every unknown pair present gives precision 1 to each system. Hence C-ref at w = 0 certifies no pair (§V.4). It certifies no slope sign either, because the all-ones point lies inside the corner box of v1.1 §4.1 and has slope 0. This holds on XM3600-600 and on COCO-5000. The w = 0 rows of C-ref are computed and printed as registered. Any C-ref certificate at w = 0, pair or slope, is a code fault that `freeze` detects and handles under the v1.1 §12 fault rule. The no-assumption headline belongs to C-label (v1.1 §4.3) only. Every C-ref verdict is conditional on (F_w) and the assumptions of v1.1 §4.2. The paper says: "from references alone, no precision order and no slope sign can be certified without an assumption on how often present objects are named." The v1.1 §4.4 high end at w = 0 equals 1 for every system.

### V.5 Estimands and verdicts

**Status of every Part V verdict (binding).** Before this file was written, its writer computed from committed aggregates the precision order under G_top of all 36 pairs and their two-reference margins (§V.1). The judge of CC-335 recomputed them. An unreviewed calculation reported 0 of 222 certified pair-draws wrong and 263 of 1,440 cells over budget at w = 0.20. V1, V2, V3 and K2 are therefore labelled "development; outcome foreseeable from stored aggregates and an unreviewed calculation (disclosed)". None is called a prediction, a validation or a confirmation, in the paper, a card or a cover letter. Expected now: V1 PASS, V2 FLOOR REFUTED, V3 DISCRIMINATING, K2 not passed. The evaluability thresholds of V1 (72 of 720 certified, at least 5 pairs, at least 72 not certified) were set on 2026-11-11 after the 222 of 720 figure was known. They are not A2 plan K1(0), which is 72 of 1,440 cross-fitted half-units.

Units: 36 pairs × 20 draws = 720 pair-draws at k = 2, clustered by pair. ABSTAIN and NOT DEFINED units are excluded and counted (v1.1 B2). Cells: B-only and S of each unit, 1,440 cells.

| Id | Estimand | Rule |
|---|---|---|
| V1 validity (primary) | `e_c` = share of CERTIFIED pair-draws at (k = 2, w0) whose truth is wrong | NOT EVALUABLE if fewer than 72 pair-draws are certified, or they come from fewer than 5 pairs, or fewer than 72 are not certified. PASS: `e_c ≤ 0.05` and no pair is wrong in more than half of its certified draws. FAIL otherwise; fixed sentence: "the floor certificate at w0 made more than 5% errors on COCO-5000 against the fuller gold; it is withdrawn at that floor" |
| V2 floor (expected FLOOR REFUTED, §V.1) | share of cells with `x_top(cell) > ⌊β(cell; w0)⌋`, `x_top` = unknown pairs of the cell that are in `G_top` | FLOOR SUPPORTED if the share ≤ α_S = 0.025; FLOOR REFUTED otherwise. Fixed sentence if refuted: "on COCO-5000 the floor assumption fails at w0; the probability guarantee is not claimed there, and the error share of V1 is an empirical figure for one model family" |
| V3 discrimination | `e_n` = share wrong among non-certified pair-draws (observed direction) | DISCRIMINATING if `e_c < e_n` and the pair-cluster bootstrap 95% interval of `e_n − e_c` excludes 0 (B = 2,000, seed 20261116, certified set held fixed); else NOT DISCRIMINATING |

Reported whatever the verdicts: share certified (power) at every grid w and k; `w*` of each pair-draw beside its truth; the measured floor `ŵ = f1/(f1 + k·x_top)` per cell; the cross-fitted floor of A2 plan §3.8 (two image halves, seed 20261111) and V1–V3 at it, labelled secondary; the pair-level table (36 rows: share of draws certified, truth); the M-label power table (share of the 36 true orders certified at each u and law; **any wrong M-label certificate is a code fault: STOP**, because C-label is exact over completions); every row repeated under the instance-only truth with the count of reference-named pairs absent from the instance gold.

### V.6 Null rules and the limit on wording

Null rules at the certified count: constant, margin (largest two-reference |Δ|), length (v1.1 H2a). Expected from §V.1: the margin rule makes no error at any count up to about 25 of 36 pairs. Fixed in advance:
- **COCO K2** (the term used in the 11-16 entry gate) is A2 plan §1.4-1.5 K2: PASS iff Δ_cov >= 0.05 and the 5th percentile of its pair-cluster bootstrap is above 0; Δ_cov <= 0 is a fail. Δ_cov = Cov@5%(C) − max over B1-B3. It is computed on Part V's 720 units at k = 2 with Part V's unit truth (precision under G_top; orientation by observed two-reference precision; a tie at the top gold is wrong). C is ranked by w* ascending, NI last, ties by |Δ| descending, then pair id. B1-B3 are as in A2 plan §1.3, with precision margins. B = 2,000, with the A2 plan's seed 20261113. A2 plan K1 and K3 are not gates here. Unless COCO K2 passes, the paper never says the certificate ranks comparisons better than a margin rule, and prints "the certificate does not beat a margin ranking here".
- What may be said if V1 passes: a margin rule needs a threshold, and the threshold that worked (between 1.64 and 3.72 points) was read from the fuller gold; the certificate decides from the incomplete gold alone. Transported-threshold row (secondary): the margin threshold calibrated on one image half against `G_top`, applied to the other half and to Part P, beside the certificate. Expected to match the certificate on COCO-5000, because pair-level flips are stable across image halves.

### V.7 Evaluability, rehearsal, multiplicity

- **Evaluability cannot be shown from committed files**: the certified count needs the once-named counts `f1` per cell, which no committed file prints. The unreviewed figure is 222 of 720 (§V.1). **No-peek gate:** `a_cert_v.py freeze` reads the outputs and the per-reference class sets (over 20 draws it touches all five references of an image); a path guard refuses the instance gold, and `freeze` never forms the union of an image's five references or any `G_top` status, so no truth outcome exists before the pin. It writes all certificates, `w*`, null-rule selections and the V1 evaluability declaration to `data/results/a_cert_v/freeze/FREEZE_V.json`, which is hashed, copied 444, committed and pinned by one LOG line before `score` loads `G_top`.
- **Rehearsal that does not peek:** synthetic fixtures only (selftest: v1.1 §11 (i)–(v), the §V.4 identity, k-general toys, M-label exactness, every verdict label at its boundary; mutants: k ignored in c, truth taken from the drawn references, freeze allowed to open the instance gold, freeze forming the five-reference union, certified set recomputed in `score`, tie counted as right). No real truth is read before the freeze pin. The three-tier rule governs test looks; this is development data, so no P(PASS) rehearsal applies (as CC-333 Q9).
- **Multiplicity.** Three verdicts (V1–V3), count rules; α per cell as v1.1 §4.2. The paper prints all three with the §V.1 disclosures. One score pass; the fault rule of v1.1 §12 step 5 applies verbatim.

### V.8 Kill gates

- KV0: selftest, mutants, pins. Otherwise no run.
- KV-EV: V1 NOT EVALUABLE at the freeze → Part V reports power only; the paper says the certificate "was not validated".
- KV1: V1 FAIL → the floor w0 is withdrawn in the paper for every data set; Part P prints `w*` only, without CERTIFIED labels at w0.
- KV2: V2 FLOOR REFUTED (expected) → the guarantee sentence of v1.1 §4.2 is printed with "the floor assumption failed on COCO-5000 at w0", and the certificate is described as "empirically valid on the sets tested", if V1 passes.
- KV3: a second fault → to the PI.

## P. Application to third-party published results (POST HOC; descriptive)

### P.1 The 15 comparisons and what is public

The count and identity are from `e1_x1pb_verification_v2.json` `pairs_15` and Paper A Supplementary S3 [read]: 11 decoding comparisons (OPERA against greedy and against beam search on InstructBLIP, LLaVA-1.5, MiniGPT-4 and Shikra = 8; VCD, OPERA and OPERA-fast against LLaVA-1.5-7B in the "Less is More" release = 3) and 4 comparisons of the "Less is More" stopping method (rows r5, r8, r10, r12 against r1, r7, r9, r11). All 15 raw precision gains are positive under the CHAIR gold (per-system `P_cls`), 12 significantly.

**Per-image captions are public**: both groups released the per-image CHAIR evaluation logs, and the paper scored 24 systems from them (495 to 499 images each). Image sets (H3 `REPORT.txt` [read]): OPERA LLaVA-1.5, MiniGPT-4 and Shikra share one 500-image set (9 systems); OPERA InstructBLIP has its own 500 (3 systems); the 12 "Less is More" rows share one 500 (11 distinct systems; r5 and r6 are one blob). Same-image pairs: 3 + 36 + 55 = 94, of which 15 are the published comparisons.

**Verified today against the public source** (GitHub git-tree and licence API, metadata only, generic client, no log content fetched) [read]: both trees complete (`truncated` false); `shikiw/OPERA` at `e1bb7632508bdfaa5cdaf5b69b64419688107da8`, MIT; `yuezih/less-is-more` at `f26e187aadacc49a7cfc30443f0e9bae865b8e2e`, Apache-2.0. Totals 2,946,285 and 3,475,307 bytes, equal to METHOD_DELTA_A §4. The five OPERA blobs listed in K17 (LLaVA-1.5 three, InstructBLIP greedy and ours) equal K17 in blob sha and size.

**Pinned download list** (25 files; sha256 filled at fetch). OPERA, under `log/chair_eval_results/`:

| Path | git blob (12) | Bytes | sha256 |
|---|---|---|---|
| `instructblip/beam5.jsonl` | `ab1ec53b09e6` | 283,122 | at fetch |
| `instructblip/greedy.jsonl` | `9d71c861dd33` | 332,619 | at fetch |
| `instructblip/ours.jsonl` | `bc94b6a680d6` | 249,114 | at fetch |
| `llava-1.5/beam5.jsonl` | `497f31742ae7` | 256,392 | at fetch |
| `llava-1.5/greedy.jsonl` | `31d15f027cce` | 259,599 | at fetch |
| `llava-1.5/ours.jsonl` | `37f4f4e04986` | 249,972 | at fetch |
| `minigpt4/beam5.jsonl` | `9ac5c7bb5dbf` | 191,640 | at fetch |
| `minigpt4/greedy.jsonl` | `fb9c19134273` | 216,771 | at fetch |
| `minigpt4/ours.jsonl` | `58fe578cc7b7` | 167,490 | at fetch |
| `shikra/beam5.jsonl` | `b79c8ad8a8b2` | 257,370 | at fetch |
| `shikra/greedy.jsonl` | `316f9faedb2d` | 274,452 | at fetch |
| `shikra/ours.jsonl` | `758dc7b0630b` | 207,744 | at fetch |

"Less is More", under `CHAIR-eval/data/` (`r5` and `r6` are one blob; `r6` is fetched for the pin and not scored):

| Path | git blob (12) | Bytes | sha256 |
|---|---|---|---|
| `Table1-results/r1-llava1.5-7b.jsonl` | `d1bb620af8eb` | 351,180 | at fetch |
| `Table1-results/r2-vcd.jsonl` | `96ea6e34275f` | 344,271 | at fetch |
| `Table1-results/r3-opera.jsonl` | `f152771e272a` | 269,160 | at fetch |
| `Table1-results/r4-opera-fast.jsonl` | `a87d1c7d8578` | 261,597 | at fetch |
| `Table1-results/r5-ours-inst.jsonl` | `72e0a15f278c` | 305,870 | at fetch |
| `Table1-results/r6-ours-cap.jsonl` | `72e0a15f278c` | 305,870 | at fetch |
| `Table1-results/r7-llava1.5-13b.jsonl` | `5968104f2b8d` | 353,597 | at fetch |
| `Table1-results/r8-ours-cap.jsonl` | `2142a538648c` | 332,205 | at fetch |
| `Table1-results/r9-llava-7b.jsonl` | `4bab4a2aa9d5` | 251,491 | at fetch |
| `Table1-results/r10-ours-cap.jsonl` | `1c1477d7e6ff` | 224,043 | at fetch |
| `Table1-results/r11-minigptv2.jsonl` | `04ee46f8d9fb` | 235,084 | at fetch |
| `Table1-results/r12-ours-cap.jsonl` | `5ff35e418e46` | 180,549 | at fetch |
| `chair-500.jsonl` | `8659bef29d46` | 60,390 | at fetch |

URL form `https://raw.githubusercontent.com/<repo>/<commit>/<path>`; generic client, no e-mail address in any request. The fetch stops on any blob sha or size that differs from this list. The record schema of the logs (which fields beside the caption and image id) is known only from the paper's earlier scoring, chưa kiểm today. Each file goes to a new empty directory; scripts read it with `python3 -I`. The logs are not on disk today (A2 plan §2.2); whether copies sit inside the reserved `a1_precheck/raw/` is chưa kiểm, and that directory is not used. The fetched files are never committed; their sha256 values are pinned in the fetch LOG line; each repository is cited with its commit and licence. The fetch runs once, and only after this addendum v1.1 is committed and pinned (CC-335 Ruling 6).

### P.2 Gold and matcher (needs the Q8 ruling)

- Per-reference class sets and instance class sets for these ids exist only in `.session_backup/2026-10-14/r12/H3/out/gt_cache.json` (`f986f8ff…`, 1,478 ids), which CC-333 Q8 keeps closed until this read. Recommended (Q3): release it for Part P, read only by the pinned script, counts out only. The A2-OC1 raw logs stay closed; the OC1 units (method arms of CCA and MARINE) stay never computed; the paper states that the OC1 image set was analysed here with other systems. CC-335 sends the release to the PI (P-1, irreversible); until a PI line answers it, the default is NO, `gt_cache.json` stays closed and Part P waits.
- **Matcher-identity gate (no certificate computed before it passes):** `P_cls`, `M_cls` and `n_img` of the 24 systems, recomputed from the fetched logs and `gt_cache.json`, equal the stored `systems` rows of `e1_x1pb_verification_v2.json` to the printed precision. A mismatch drops Part P.

**No leakage into any frozen input.** Whatever the PI answers on gt_cache.json, no number computed in Part P enters a frozen input of A2-OC1 or of any registered row on XM3600-600 (w0, α, R, seeds, thresholds, code constants). Every such input is computed from COCO-5000 only and committed with a LOG pin before Part P's first result is read. The OC1 raw logs under `.session_backup/2026-10-27/a1_precheck/raw/` stay closed. `gt_cache.json` (f986f8ff) is opened only after a PI line that answers CC-335 P-1, and only by the pinned Part P script, which writes counts only. Until that line exists, CC-333 P3 (untouched) binds.

### P.3 What is computed

**P-a, reference-rung replay (primary row).** "If only k references existed, as on Vietnamese benchmarks." M-ref of §V.3 on each image set, k ∈ {1, 2, 3, 5}, R = 20 draws, seeds as §V.3, w grid and w0 as v1.1. For each of the 15 published comparisons and each k: share of draws CERTIFIED, the certified direction (the method or the baseline; orientation comes from the rung, not from the paper), the median `w*`, and whether a certified direction equals the CHAIR-gold direction. The same over the 94 same-image pairs, with V1–V3 of §V.5 computed and labelled "post hoc; truth already scored by the paper; other model families".

**P-b, the CHAIR gold itself (secondary row; no truth exists).** Known present = `G_top`; unknown = every other mention; k = 5. Budget `β(cell; w)` bounds the present pairs named by no reference; the instance-labelled ones among them, `I0(cell)`, are known, so `X = min(U, ⌊β⌋ − I0)`, and `I0 > ⌊β⌋` is printed as "floor refuted by the instance labels" for that cell (no certificate is issued at that w). Output per published comparison: CERTIFIED or NOT CERTIFIED at w0, and `w*`.

**Expectation (POST HOC, rough):** the 15 published gains are 0.5 to 7.9 precision points under the full gold, and one-third or more of mentions are unknown at two references; the writer expects few or none of the 15 certified at k = 2, and many cells with the floor refuted at k = 5. A table of "NOT CERTIFIED" is a likely outcome and is reported as such.

**Units.** The per-system rows of the matcher gate use each system's own image ids as stored. Every pair statistic, certificate and truth uses the intersection of the two systems' image ids, and its size is printed. The P-a truth is the precision direction under G_top on that intersection, recomputed by the pinned script. The stored `P_cls` rows serve only the matcher gate.

### P.4 Wording limits (binding on the paper)

- Allowed: "with k references, the direction of this published comparison is [certified / not certified] against gold incompleteness at floor w0; its break-down floor is w*". "Not certified" is always followed by "this does not say the published result is wrong".
- Never: that a published gain is wrong, overturned or unreliable; any statement about a system whose released outputs we did not score; any re-run claim; "certified" without the floor and the image set; P-a counts as evidence for the registered H2a.
- Every Part P number carries "POST HOC (released outputs the paper had already scored under the full gold)". The eight public LVLMs are named as the sources of released outputs only.
- "not certified" is never paraphrased as fragile, unreliable or unsupported;
- every Part P number carries "POST HOC; truth already scored by the paper";
- an aggregate share ("k of 15 certified") always states k, w0 and the image set;
- nothing in Part P is evidence for H2a or for any gate.

### P.5 Fallback if the fetch or the matcher gate fails

Per-image outputs are public, so no re-decode is planned. If they cannot be used: (i) published aggregate CHAIR numbers alone give nothing, because at w = 0 a positives-only gold certifies no order (§V.4) and the budget needs per-pair once-named counts; (ii) our own decodes of the released checkpoints (about 24 runs × 500 images, 10 to 20 hours on one rented RTX 3090, chưa kiểm) would support only "our decodes of these checkpoints", and the paper's earlier decode harness failed its fidelity check (|ΔCHAIR_i| = 1.49). Recommended: drop Part P rather than use (ii) before 11-18.

---

## 9. Ours against arXiv 2611.01712

Fetched today (abstract page sha256 `1532b61d…`, HTML `2859a9ce…`) [read]. Fernández-Barrios et al., "When Disagreement Labels Do Not Identify F1 Rankings" (submitted 1 Nov 2026, 6 pages): two fixed binary classifiers; all disagreement labels revealed, agreement labels unknown; exact bounds on the paired positive-class F1 difference over every completion; a choice within a tolerance ε; agreement queries; 3,200 frozen pairs; paired bounds certify 79.46% against 6.57% for separate bounds; full labels verify regret. Stated limits: fixed predictions and correct labels; "does not extend to populations, noisy labels, macro-F1, multiclass or families"; it cites Kuboyama, TDC and Polo et al. as general joint all-completion certificates (those three chưa kiểm).

| Element | 2611.01712 and the frameworks it cites | This work |
|---|---|---|
| Bounds over every completion of a fixed batch; shared completion of the pair tighter than separate bounds | **Theirs.** Our `Δ_min` at w = 0 and the shared cell are a specialisation to precision; not claimed as new (CC-333 limit (i), N8) | used |
| Check of certified choices against full labels | Theirs (retrospective; their guarantee is deterministic) | Part V does the same kind of check; not new in kind |
| Gold made of k free-text references, positives-only, multi-label mentions | outside (single correct label per item) | ours as a setting; §V.4 shows the all-completion certificate is empty there |
| A probabilistic cap on the unknown positives from once-named counts under a naming floor w | outside ("statistical alternatives can trade assumptions or error probability" is named, not done) | ours; elementary (Lemma B, Bernstein); no "first" claim |
| Break-down floor `w*` per comparison; slope-sign corners | outside | ours |
| Test of the cap's assumption against a fuller gold (V2, H2b, P-b) and a human-completed gold (v1.1) | outside | ours |
| F1 with a completion-dependent denominator; tolerance ε; query policy | Theirs | not done (precision only; F1 with recall held fixed) |

## 10. Idea provenance (own observations)

| Part | Starts from our observation | Borrowed |
|---|---|---|
| V | Paper A: the sign of a comparison depends on the gold (COCO-5000 slope −4.77, +10.57, +22.13); today's count that 9 of 36 precision orders flip at two references; the A2 dry calculation that budgets fail while certificates hold | all-completion bounds (row 1 of §9); Chao-type once-named counts |
| P | Paper A S3: 15 published gains re-scored, 12 significant raw, 2 after count control; the k-rung flips of the two English release families (H3) | the released logs; CHAIR |

## 11. Compute and calendar (CPU only; 0 GPU-hours; laptop, one I/O-heavy command at a time)

| Date (UTC) | Step |
|---|---|
| 11-12 | Judge read of this file; gatekeeper commit and LOG pin of it before any code reads data; G0 and Q8 rulings; `scripts/a_cert/a_cert_v.py` (reusing `a_cert.py` functions) with selftest and mutants; code read |
| 11-13 | `freeze` V, pin; `score` V once (under 15 CPU-minutes expected, as A2 plan §4; chưa kiểm); result read |
| 11-14 | Logged fetch for P (6.4 MB); matcher gate; P run (500 images × 3 sets; minutes) |
| 11-15 | Result read of P. **Last day for any result read.** |
| 11-16 | Entry gate, METHOD_DELTA_A §7 verbatim, unchanged by this file: "The method enters Paper A only if K0 passed, no claimed floor has more than 5% certified errors, and H2a or COCO K2 passes. Otherwise the paper keeps the intervals, H1 and H3 as an audit extension and says the certificate was not validated." |
| 11-17 to 11-18 | Paper transfer package, diff read, blind card |

**Likely outcome under the unchanged gate: "not validated"** (H2a expected NOT EVALUABLE by v1.1 §9; K2 expected not to pass by §V.6). Q10 asks whether the gate should change; the writer proposes no change by himself, because the proposal would come after today's aggregate look. CC-335 Ruling 4: the gate is unchanged. Whether a clause on H2d (`A_CERT_ANALYSIS_REG_v1_2_H2D.md`) is added to it is the PI's decision (CC-335 P-2) and is not made here.

Slip rule: Part P is dropped if its result read is not done on 11-15; Part V is never shortened to fit.

## 12. T1: what each part adds, and what stays missing (no score is promised)

The rubric caps an audit-only paper at 3 and asks, for 4, for a new tool or method born from the audit's finding, at Q1 standard with no serious criticism [read]. Paper A's own row (RUBRIC_A l.257 [read, first 700 characters]) asks for a certification rule that changes a decision, shipped in `vsps-eval`, applied to the 15 released comparisons, the eight LVLMs of the registered secondary result and the development ladders, with the share of conclusions certified or overturned.
- **Part V** answers "no validated tool" with a check against a fuller gold whose outcome was largely foreseeable (V1), where the committed registration expects NOT EVALUABLE. Weakness a scorer will see: the data were analysed before and the result was half-seen in scratch; one model family; the floor is expected to be refuted (V2), so the guarantee is not what makes the certificate valid; a margin rule ranks these 36 pairs as well (§V.6).
- **Part P** answers "changes a decision" with a per-comparison label on 15 published results and other model families. Weakness: post hoc; the likely outcome is "few certified", which shows the limit of few references more than the power of the method.
- **Still missing for 4 after both:** the rule shipped in `vsps-eval` with a test (not planned here; one day after the code read); the eight LVLMs of the paper's registered secondary result and the development ladders (not in this addendum; Part P's LVLMs are the release families); "overturned" is a word §P.4 forbids; the entry gate itself (§11); a confirmatory test on unseen outputs (A2-OC1 is the only candidate and cannot be opened by 11-18); a second family on COCO-5000; an external proof review; mixed F1; and separation from 2611.01712 beyond the floor budget, which is elementary. CC-335 Ruling 9 revises CC-333's "about 50% with both" to about 25% for this addendum as planned and about 30% with H2d; it is a judge's opinion, not an approval item, and no score is promised.

## 13. Open questions for the judge

| # | Question | Recommended answer |
|---|---|---|
| Q1 (G0) | May `dataset_coco.json` (`2fd99922…`) be read for per-reference class sets on COCO-5000? | Yes: spent development reference data, pinned by A-M1. Class sets cached in scratch only. Default: STOP |
| Q2 | §V.4: C-ref at w = 0 certifies nothing. Is the derivation right, and what replaces "the w = 0 certificate is the headline" (v1.1 §4.2)? | Answered by CC-335 Ruling 2 and §V.4a. |
| Q3 (CC-333 Q8) | May Part P read `gt_cache.json` and use the OPERA-500 ids, with the OC1 raw logs closed? | Yes, through the pinned script only; OC1 units stay never computed; disclosed. Otherwise Part P is dropped |
| Q4 | Primary operating point on COCO: w0 = 0.20 although the floor is expected to be refuted there, or the cross-fitted floor? | w0 = 0.20 (one operating point everywhere, fixed before); cross-fitted floor secondary |
| Q5 | Evaluability thresholds of V1 (72 of 720, five pairs) | Accept, labelled as in §V.5 'Status'. |
| Q6 | Is M-label worth running, given that its validity cannot fail? | Yes as a power table only; drop it if the code read is late |
| Q7 | Should V1 FAIL withdraw w0 for XM3600 too (KV1)? | Yes in the paper's wording; the registered XM3600 verdicts are still computed and printed |
| Q8 | P-b uses the instance labels to refute the floor per cell. Is that a use of gold "after the fact"? | Valid under (F_w): the I0 pairs are present and unreferenced, so the unknown present count is at most β − I0. The cap is tighter than min(U, floor(β)) and can add certificates. Both caps are printed. No truth exists for P-b; secondary only. |
| Q10 | The 11-16 entry gate asks for "H2a or COCO K2". Both are expected not to be met. Should V1 PASS (validity against the fuller gold, with V3 DISCRIMINATING) count instead of K2? | The writer leans no: A2 plan §1.6 says K1 alone can never justify GO, V1 is near-known, and the question arises after today's look. If the judge wants it, it is labelled "gate changed after the aggregate look of 2026-11-11" and needs a PI line. Default: gate unchanged; the paper then carries the method as "not validated" |

CC-335 Rulings 2–7 answer Q1–Q10. Where a recommended answer above differs from them, the rulings bind.
| Q9 | New seeds (20261114 to 20261116) or the A2 plan's seeds? | New seeds; the scratch seeds are unknown |

## 14. Not verified by the writer (chưa kiểm)

- The nine output shas, the id list, the instance-gold sha and the matcher shas (taken from the A2 plan).
- That `/tmp/prop_r2` figures (222 of 720; 263 of 1,440) are correct; the directory no longer exists.
- The content and record schema of the 25 release files (only tree metadata and licences were fetched); their sha256.
- The structure of `gt_cache.json` beyond the A2 plan's note; whether its matcher equals the one that produced the stored `systems` rows (the P.2 gate tests it).
- CPU times; the GPU-hours of the fallback; the hidden-share range 0.30 to 0.57 at its source file.
- Kuboyama, TDC and Polo et al.; the other identifiers of METHOD_DELTA_A §6.
- The §V.4 derivation and the P-b cap `⌊β⌋ − I0` are AI derivations of today, unchecked.
