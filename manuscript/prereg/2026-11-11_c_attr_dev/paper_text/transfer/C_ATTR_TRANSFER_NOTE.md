# C-ATTR-DEV → Paper C transfer note (for a one-judge diff read)

Label: DEVELOPMENT / C-ATTR-DEV, NON-CONFIRMATORY. No test set was touched.

**What this is.** This is an UNCOMMITTED working-tree change to `vsps-paperC-tallip` at HEAD `f6aa449`. Nothing was `git add`-ed or committed, and `docs/CC309_PARAGRAPH_DRAFT.md` was not touched.
- The text was built by `c_attr_transfer.py`, run as `python3 -I c_attr_transfer.py <scratch>`. The script starts from `git show HEAD:` of each paper file, so re-running it is idempotent.
- Phases A and B of CC-358 Ruling 5 are transferred together in one diff. Each block below is tagged with its phase, so the reader can apply the right gate.

**Sources:**
- package `C_ATTR_PAPER_TEXT_v1.md`: e1be6f93…, asserted by the script;
- CC-358: ded17561;
- CC-363: 904ecf43…, asserted (used only for the Ruling 3 sentence);
- numbers: `data/results/c_attr_1112_score/res/`. The script asserts the sha of every res/ file against `SHA256SUMS` cb0af612… (PIN-1112-c-attr-score-records).
- Phase-A tokens, under the coordinator rule of 2026-11-12, are filled from:
  - (a) committed files pinned by a ruling or LOG line: `K0_REPORT.json` 15108f2b, with the HEAD blob checked equal;
  - (b) count/record files of the read-only ATTR_H1 pulls, each checked against its pull `SHA256SUMS`. Block 1 is a2b63fef and block 1b is 0754128c; both SUMS shas are asserted. `CAP_1B.json` 6d42608e and `STEPS_1B.tsv` bd9139b0 are checked against the OPS-1112af pins.
  - `logs/job.log` is outside the sums by design. Only the `JOB DONE gpu_h` line and the OK lines were used, and the script asserts that each value is stated by its OPS line (OPS-1112c-c-attr-block1-done for block 1, OPS-1112af-c-attr-1b-done-pull for block 1b).
  - Every file opened is listed with its sha under "Phase-A sources opened".
  - GS1 and GS1B take the job's own JOB DONE value: the package's rule is "sum of non-start rows / 3600, the job's JOB DONE gpu_h rule". `gpu_seconds.tsv` itself is NOT in either pull's SUMS, so it was not used.
  - `SUM::n_b1_runs` = the number of `STEPS_1B.tsv` steps with an "OK <step>" line in job.log (50). The script also asserts 55 OK lines in all, as OPS-1112af states, and no CAP STOP or JOB STOP.

**Not opened:** any ledger, `.preds.json`, `.partial.jsonl`, caption file, label path or test set. Under `.session_backup/machines/ATTR_H1/` only the files listed under "Phase-A sources opened" and the two `SHA256SUMS` files were read; the two pull folders and their `parity/` folders were listed.

**Build:** `paper_v1_analysis/tex/` is the pandoc output of `tex/build.sh`. It was NOT run on the laptop and was not hand-patched. `tex/` still holds 10 uncorrected "52/52" lines, `tex/build.sh` and these ten "52/52" tex lines wait for a build on a rented host. `tex/paperC.bib` is the build's copy of `paperC.bib`.

## Counts

- **Fills:** 1,564 values filled by script (`fills.json`): 1,236 numbers or counts, and 328 labels, flags or status strings. This includes all 74 Phase-A tokens; 0 tokens are left. Every fill has one row in `number_manifest_C.tsv`.
- **Manifest:** 1,565 rows appended. The extra row is the W1 label source.

## TG1–TG11

| item | status | how / where |
|---|---|---|
| TG1 byte match | met, with listed edits | Each block is the package text with the `> ` quote prefix stripped. Whole-line bold headings (`**3.8 …**`) became markdown headings (`###`/`####`).<br>Outcome sentences and table captions are taken by line number from the package (`segs()`/`pl()`).<br>Deliberate departures:<br>(a) the two P-3 sentences of l.122 are held;<br>(b) TG8 cuts of dangling references (listed under "TG8 cuts", coordinator decision (2));<br>(c) 7.5 "Blocks 2–4 {{…}}." is held (W3);<br>(d) the 6.10.3–6.10.7 headings are taken from the package's §4 titles;<br>(e) the copy-bound sentence adds "<backbone>," after "<set>," (the template names no backbone);<br>(f) the swap sentence lists both backbones in one δ clause;<br>(g) W2 replaces "{{review id and its consequence}}." including the template's final period (Ruling 3's sentence ends in its own period). The result reads "…are used; A recorded review…": the capital after the semicolon is cosmetic, kept verbatim, and is the reader's call.<br>(h) The Section 3 opening drops one "and" to take the clause: 03_method.md:3. |
| TG2 values from pinned files | met | Every fill comes from res/ (sha-asserted), with one manifest row each (`number_manifest_C.tsv`, status "keyed (DEVELOPMENT / C-ATTR-DEV, NON-CONFIRMATORY; CC-363)").<br>The 74 Phase-A tokens are filled by script from the sources listed above: 6.10.1 (06:128), 6.10.2 (06:134, 06:136, 06:142), 9.1 bullet 2 (09:11), 6.11 (06:227), Table S20 (11:983-989) and Table S26 (11:1089-1102).<br>Script cross-checks:<br>- `len(failing_ids) = n − identical`;<br>- the STEP10/STEP1B0 verdicts equal `NOM::parity`;<br>- every K0 gate is "pass" with refill share ≤ 0.10, so the S26 sentence matches its keys.<br>The values equal the LOG values of record (42/37/31; 50/50; D1 50/50 ×3; 6.41; 12.27; 17.95), but none was typed.<br>Numbers printed as package literal text (e.g. 911, 925, 6,017, 111,927, 22 of 22, 33 of 33, 73 of 73, about 1.03, ±3.4, 0.92) have NO manifest row. Package §6.2 asks for rows only for counts, GPU-hours and scores; the reader decides whether literal rows are owed.<br>S20 verdict cells now come from the package's own STEP10/STEP1B0 keys. The earlier nomination-file substitution is removed. |
| TG3 outcome sentence by stored label | met | Case N+ only: `NOM::closed` is absent and nominated = [H_pair(qwen25vl_7b), H_pair(internvl3_8b)]. The opening sentence is at 06:157.<br>Two PASS sentences, Qwen first (06:176). Each is asserted in the script: label DETECTED, d ≥ 2, p̃ ≤ α_j.<br>α_j by hand: tied p̃ = 1/2,001, ties by claim name, so InternVL3 j = 1 → 0.0125 and Qwen j = 2 → 0.025 (asserted).<br>No FAIL, Z, N0, Holm-stop, withdrawal, monotonicity, ω ≤ 0.25, "placebo not flagged" or "partly bounded" sentence is present.<br>Non-nominated rows get one sentence each by label (06:178 Qwen and InternVL3; 06:180 Aya, after the Aya first-look sentence).<br>The script asserts that only the "L_cp ≤ 0" copy sentence applies (12 cells, 06:213-215) and that only the flagged-placebo sentence applies (06:190). |
| TG4 strings verbatim | met | The four fixed labels, the V1 K1 sentence (06:134), the §7.12 FAIL wording (registration text in 5.7 only, 05:157), the V6 PASS wording, the §8/§7.9 readings and both E6 third-party strings (03:122) are all asserted by the script.<br>"values are for m = 1" appears 3× (one per NEGLIGIBLE row). |
| TG5 no "test" for the analysis; no RAGCap-style; no published system tested; no p other than p̃ | met | A regex self-check blocks "attribution test" and "test of the method/attribution". Remaining "test" words refer to test sets, TOST, self-tests or "not tested". |
| TG6 bib | met | See "Bib check". Entries are appended to `paperC.bib`; the audit has 4 rows in `paperC_bib_audit.tsv`. Holm1979 was verified on OpenAlex and its citation is restored (05:140). |
| TG7 title, abstract, contributions | met | 00_abstract, 01_introduction and 10_conclusion are byte-unchanged (asserted). P-1 default (NO) is kept, and the 6.10 box says the study enters neither the abstract nor the contributions (06:126). |
| TG8 cross-references | met in the md; tex waits for build | Met: 6.10 Compute → 6.11 (06:225), the §5.5 pointer → 6.11 (05:117), and new numbering 3.8, 5.7, 6.10.x, 7.5 and Tables 15–17 / S20–S26 (after Table 14 / S19).<br>Dangling references were cut, with no claim added; see "TG8 cuts" below (03:122, 05:155, 06:190 ×6). The script asserts that no "6.10.8" remains.<br>`tex/` waits for a build on a rented host: ten "52/52" tex lines remain until then.<br>For the reader: the opening of Section 6 (06:3, "Sections 6.8 and 6.9 are the exceptions") does not name 6.10. That is not package text and was left for the reader. |
| TG9 no caption, host, IP or internal code | met | Self-check: no `OPS-`, `CC-3`, host name or IP pattern in new text. K1/D1/A1/C-ATTR-DEV are defined in Box 1 (05:21-27). No AI text, and no "independent" review claim was added. |
| TG10 past-tense procedure | met | "Block 1b re-decoded … no cap stop and no job stop": OPS-1112af.<br>"its verification stage passed …": VERIFY.json and CC-363 R1d.<br>"nomination file was hashed and its sha256 logged before any new OV-dev-B output was scored": CC-363 R1c (11:09:27Z before ovb rows at 11:11:25Z).<br>"each stage ran once": CC-363 R1b.<br>"D1 passed for all three (50/50 ×3)": the D1 and STEP1B0 records.<br>Confirmation was through CC-363 Ruling 1 and the OPS lines read through `cut` (OPS-1112c, j, af, ba–be), not a fresh full read of each OPS line.<br>For the reader: the 5.7 Budget paragraph (package l.162, transferred because CC-358 did not hold it) says the 2026-11-16 12:00 freeze "ended every unfinished step". Today is 2026-11-12, so that clause stays future-dated until K7. |
| TG11 parity_slice0 contact | met | Coordinator LOG line OPS-1112bs-c-tg11 (2026-11-12T14:08:18Z): no earlier contact on record, so no disclosure is needed. |

## CC-363 W1–W7 and Ruling A

| item | status | where |
|---|---|---|
| W1 Aya XM-dev500 copy-bound label | met | Table 17 flags column (06:210-211), the Table 17 caption (06:196) and the Table S24 tier cells. The source is the scoring run doc v1.1 §1 step 5, recorded in a manifest row (status "label source (CC-363 W1; not in COPYBOUND_xm_dev500_aya_vision_8b.json)"). |
| W2 Ruling 3 sentence, Aya flags, no P2 numbers | met | The sentence is verbatim at 06:190.<br>Aya OV-dev-B rows that contain `rand` carry "placebo flagged (Section 6.10.5)": Table 16 τ_marg, τ_sel and τ_any; the matching sentences at 06:180; Table 17 and S24 (L_cp/K_nc); S23a (flag column).<br>Aya τ_pair (no `rand` arm) is used as labelled. The P2 numbers do not appear anywhere. The flag wording is writer-composed. |
| W3 scope + B2–B4 not transferred | met | 6.10.8 is absent; the 7.5 "Blocks 2–4" sentence is held; no scope sentence. |
| W4 Ruling A, label on every `fix` row, words only | met | 128 cells marked † in table rows or headers whose arm is `fix`, found by grep of HEAD `06_results.md` and `11_supplement_registered_rows.md`. That covers Table 6 header; S1–S4 and their continuations; S5 header `ret` − `fix`; S6 `fix` rows; S10/S11 `-fix-` runs; S12 `-fix-` runs. 14 note lines (1 under Table 6, 13 in the supplement; per-table counts in the Ruling A section below) read "† Conditional on the realised fixed set (development estimate, batched decodes, Section 6.10.5)." The script fails closed if any other table line with `fix` or `-fix-` in the 0*/10/11 files is unmarked.<br>Excluded as definitions, not rows: the Section 3.2 arm table (03:19) and Box 1.<br>Not marked (prose, not a table row): 6.4 "Fixed examples." (06:73). Reader's call.<br>No ω number is in any test table; ω̂ and ω^U appear only in 06:192 and S23(b). |
| W5 no batched vs batch-1 comparison; no XM conclusion; no no/zero wording; no "test" | met | The only XM-dev500 sentence is the fixed no-rule sentence (06:186). N1 wording is at 06:178. |
| W6 ledgers never committed | not applicable here | Nothing is committed; no ledger was read. |
| W7 scoring-time deviations in 7.5 | met (writer-composed) | 07:59 "Deviations at scoring time": CPU scoring beside another study's GPU decode; reference files re-staged from the copies of record; segmenter files restored and recorded afterwards; scoring mutant record without network isolation (cross-referenced to the existing bullet). It makes no claim of no effect. |
| N1 | met in part | Interval clause filled from VER (06:178), printed in the paper's unsigned-bound format "[0.01, 1.94]". The ruling writes "[+0.01, +1.94]": same values, and the reader may prefer the ruling's signs. The "realised SE below planned" note is not added, because no stored key holds it. |
| N2 | not applicable | The importlib package-list sha is not printed in the paper. |
| N3 | met | 11:1087 (writer-composed). |
| N4 | met | 11:981, OV-dev-A m = 1 labels from NOM (writer-composed). |
| N7 | not used | Optional. |

## Deliberately NOT transferred, and why

- **Scope sentence (§4.9) and the B2/B3/B4 NOT RUN sentences, which form all of 6.10.8, and the 7.5 "Blocks 2–4 …" sentence.** CC-363 W3 holds them until the 2026-11-14 18:00 VN cut-off line, the K7 line, or their own packages.
- **The two draw-variance sentences of the 5.7 "Interval and p-like statistic" paragraph.** CC-358 R5 Phase A (ii) holds them until the P-3 reconciliation read, and no LOG line shows that read.
- **Abstract, introduction, contributions and conclusion.** P-1 default is NO (TG7).
- **Shells that do not apply:** V, S, T, Z, N0, FAIL, Tier B/C NOT RUN, withdrawal and monotonicity.
- **The "Values of record" notes and the transfer notes of the package.** They are not paper text.
- **f30k_val rows of K0 in S26.** Block 4 was not run, so S26 lists the three Vietnamese sets only.
- **CC-358 P-2.** The supplement's "an independent review" was not changed, as it is outside this package.

## Formatting rules applied

- **Intervals** follow Table 13: point signed, bounds unsigned unless negative, U+2212 minus, two decimals, never "−0.00".
- **p̃** uses three significant digits. At the floor it prints "at its floor (1/2,001)" in tables and "1/2,001, its floor" in sentences.
- **Shares** (draw part, total, share) use three decimals. All other values use two.
- **The [[…|90]] macro** renders as "d [lo, hi] (90% interval [lo90, hi90])".
- **Phase-A values:** cap_h uses two decimals. K0 refill shares use six decimals, overlaps four, cosines three, all rounded half-up on the stored decimal. Counts are integers. A1 "FAIL" prints "FAIL (K1 fired)" in the S20 K1 column. gpu_h is printed as the job wrote it.
- **Rounding check.** Three L_cp points print as −8.91, −8.78 and −4.82 (Qwen OV-dev-B (i), Qwen XM-dev500 (ii), InternVL3 XM-dev500 (i)); the CC-363 read wrote −8.92, −8.79 and −4.83. The stored values −8.9149, −8.7848 and −4.8250 round as printed (see the fills table). The paper text is unchanged.

## Bib check (TG6), 2026-11-12, no personal data in any request

| key | result | URL |
|---|---|---|
| Sattolo1986 | VERIFIED: Sandra Sattolo, "An algorithm to generate a random cyclic permutation", Information Processing Letters 22(6) 315–317, 1986, doi 10.1016/0020-0190(86)90073-6. Added to the bib. | https://api.crossref.org/works/10.1016/0020-0190(86)90073-6 |
| Schuirmann1987 | VERIFIED: Donald J. Schuirmann, "A comparison of the Two One-Sided Tests Procedure and the Power Approach for assessing the equivalence of average bioavailability", J Pharmacokinet Biopharm 15(6) 657–680, 1987, doi 10.1007/BF01068419. Added to the bib. | https://api.crossref.org/works/10.1007/BF01068419 |
| Li2025UnveilingICL | VERIFIED: TPAMI 48(11) 14759–14776, 2026, doi 10.1109/TPAMI.2026.3719106, six authors matching the bib. The "short-cut" finding is in the text (arXiv 2507.08021): Finding 5, "Similarity-Based Retrieval Induces Shortcut-Driven CIDEr Inflation", "short-cut phenomenon where captions from ICE are copied". Already in the bib. | https://api.crossref.org/works/10.1109/TPAMI.2026.3719106 ; https://arxiv.org/html/2507.08021 |
| Holm1979 | VERIFIED on OpenAlex (W2121044470): Sture Holm, "A Simple Sequentially Rejective Multiple Test Procedure", Scandinavian Journal of Statistics vol. 6, pp. 65–70, 1979, doi 10.2307/4615733. The record holds no issue number, so the bib has no `number` field. Added to the bib; the citation is restored in 5.7 (05:140). Also tried: the JSTOR stable page (did not load, twice) and the Crossref DOI record (404); Crossref title search (no hit). No API key was used. | https://api.openalex.org/works?filter=title.search:simple%20sequentially%20rejective%20multiple%20test%20procedure |
| Ramos2023LMCap, Bazi2025RAGCap | present in the bib (asserted) | – |


## Block map (package lines -> paper file:lines)

| block | phase | package lines | paper file:lines |
|---|---|---|---|
| P1-open | A | 46 | paper_v1_analysis/03_method.md:3-3 |
| P1 | A | 64-90 | paper_v1_analysis/03_method.md:96-122 |
| P2 | A | 96-102 | paper_v1_analysis/05_preregistration_and_analysis.md:21-27 |
| TG8-5.5 | A | - | paper_v1_analysis/05_preregistration_and_analysis.md:117-117 |
| P3-5.6 | A | 108 | paper_v1_analysis/05_preregistration_and_analysis.md:125-125 |
| P3-5.7 | A+B (Order of looks = B) | 112-162 minus P-3 sentences of l.122 | paper_v1_analysis/05_preregistration_and_analysis.md:127-177 |
| P4+P5+6.11 | A+B | 170-182, 199-203, 209-374 | paper_v1_analysis/06_results.md:124-227 |
| P9-Box2 | A | 452 | paper_v1_analysis/07_disclosures.md:9-9 |
| P7-Box2rows | A | 419-422 | paper_v1_analysis/07_disclosures.md:22-25 |
| P7-7.5 | A+B (scoring sentence = B; W7 bullet = B) | 402-413 minus the blocks 2-4 sentence; + W7 | paper_v1_analysis/07_disclosures.md:49-61 |
| P9-9.1 | A | 451 | paper_v1_analysis/09_limitations.md:9-9 |
| P8-9.1 | A | 428-429 | paper_v1_analysis/09_limitations.md:10-11 |
| P8-9.2int | A | 433 | paper_v1_analysis/09_limitations.md:18-18 |
| P8-9.2con | A | 437 | paper_v1_analysis/09_limitations.md:20-20 |
| P8-9.3 | A | 441 | paper_v1_analysis/09_limitations.md:28-28 |
| P9-supp-closing | A | 453 | paper_v1_analysis/11_supplement_registered_rows.md:751-751 |
| P9-supp-l711 | A | 454 | paper_v1_analysis/11_supplement_registered_rows.md:737-737 |
| P6 | A (S20, S26) + B (S21-S25) | 257-260, 269-283, 303, 318-321, 328-345, 378-394, 445 | paper_v1_analysis/11_supplement_registered_rows.md:977-1102 |

## Finer block map (phase gate per subsection / table)

| block | phase | package lines | paper file:lines |
|---|---|---|---|
| 6.10 box + 6.10.1 (first part) | A | 199-203 | paper_v1_analysis/06_results.md:124-126 |
| 6.10.1 incl. last sentence (Scoring followed ... parity gate passed) | A; last sentence B | 203 | paper_v1_analysis/06_results.md:128-128 |
| 6.10.2 | A | 170-182 | paper_v1_analysis/06_results.md:130-142 |
| 6.10.3 Table 15, N+ opening, Table 16, PASS, row sentences, DF | B | 209-253, 336 | paper_v1_analysis/06_results.md:144-182 |
| 6.10.4 | B | 265 | paper_v1_analysis/06_results.md:184-186 |
| 6.10.5 (+ CC-363 Ruling 3, Ruling A sentence) | B | 286-290 | paper_v1_analysis/06_results.md:188-192 |
| 6.10.6 Table 17, copy sentences, swap | B | 295-314, 349-350 | paper_v1_analysis/06_results.md:194-219 |
| 6.10.7 | B | 324 | paper_v1_analysis/06_results.md:221-223 |
| 6.11 Compute (+ sentence) | A | 374 | paper_v1_analysis/06_results.md:225-227 |
| 5.7 Order of looks paragraph | B | 160 | paper_v1_analysis/05_preregistration_and_analysis.md:175-175 |
| Supplement header + N4 labels | A (N4 = B) | 445 | paper_v1_analysis/11_supplement_registered_rows.md:977-981 |
| Table S20 | A (verdict cells from NOM) | 378-384 | paper_v1_analysis/11_supplement_registered_rows.md:983-989 |
| Table S21 | B | 257-261 | paper_v1_analysis/11_supplement_registered_rows.md:991-997 |
| Table S22 | B | 318-322 | paper_v1_analysis/11_supplement_registered_rows.md:999-1010 |
| Table S23 (a, b) | B | 269-283 | paper_v1_analysis/11_supplement_registered_rows.md:1012-1030 |
| Table S24 | B | 303 | paper_v1_analysis/11_supplement_registered_rows.md:1032-1071 |
| Table S25 (a, b) + N3 note | B | 328-345 | paper_v1_analysis/11_supplement_registered_rows.md:1073-1087 |
| Table S26 + sentence | A | 388-394 | paper_v1_analysis/11_supplement_registered_rows.md:1089-1102 |

## Ruling A: 128 table rows or headers marked †; 14 note lines

| file | table | marked rows |
|---|---|---|
| 06_results.md | Table 6 | 1 |
| 11_supplement_registered_rows.md | Table S1 | 3 |
| 11_supplement_registered_rows.md | Table S1 (continued) | 3 |
| 11_supplement_registered_rows.md | Table S2 | 3 |
| 11_supplement_registered_rows.md | Table S2 (continued) | 3 |
| 11_supplement_registered_rows.md | Table S3 | 3 |
| 11_supplement_registered_rows.md | Table S3 (continued) | 3 |
| 11_supplement_registered_rows.md | Table S4 | 3 |
| 11_supplement_registered_rows.md | Table S4 (continued) | 3 |
| 11_supplement_registered_rows.md | Table S5 | 1 |
| 11_supplement_registered_rows.md | Table S6 | 8 |
| 11_supplement_registered_rows.md | Table S10 | 54 |
| 11_supplement_registered_rows.md | Table S11 | 16 |
| 11_supplement_registered_rows.md | Table S12 | 24 |

Excluded as definitions (not result rows): 03_method.md arm table row `fix`; Box 1 row `ret`, `rand`, `fix`, `zs`. The script asserts that no other table line with `fix` / `-fix-` in 0*/10/11 files is unmarked.

## Phase-A sources opened (each verified before use)

| file | sha256 | verified by |
|---|---|---|
| `.session_backup/machines/ATTR_H1/root/outputs/c_attr/parity/S10a_qwen25vl_7b_ov_dev_b.json` | e2fc6937712f0c7e9d90a3d459570eb88c171f5d8a19a67d22acfd6862468c5a | pull SHA256SUMS of c_attr (a2b63fef) |
| `.session_backup/machines/ATTR_H1/root/outputs/c_attr/parity/S10a_qwen25vl_7b_ov_dev_a.json` | 5c07af41d50737f3599493a9a9abe7ace0a39c89f59353a0ca6ac93ba8be6c81 | pull SHA256SUMS of c_attr (a2b63fef) |
| `.session_backup/machines/ATTR_H1/root/outputs/c_attr/parity/S10b_qwen25vl_7b.json` | 75987300072e27212d88c1bf05f5f4e0396582648816500367192ac2e938ad11 | pull SHA256SUMS of c_attr (a2b63fef) |
| `.session_backup/machines/ATTR_H1/root/outputs/c_attr/parity/STEP10_qwen25vl_7b.json` | abc4a87611bc68f0fdebd6ca18d36ef1d5d086462fde5031c7251aa5f866d0bc | pull SHA256SUMS of c_attr (a2b63fef) |
| `.session_backup/machines/ATTR_H1/root/outputs/c_attr_b1/parity/D1_qwen25vl_7b.json` | 699d7a92c60085f4d470c32167ca220d711b553ad8e97b1d6bab09317749c719 | pull SHA256SUMS of c_attr_b1 (0754128c) |
| `.session_backup/machines/ATTR_H1/root/outputs/c_attr_b1/parity/STEP1B0_qwen25vl_7b.json` | cc2ef7e499796c56ac370f9d12507b5d33fbca18473c0798025129b7c495659d | pull SHA256SUMS of c_attr_b1 (0754128c) |
| `.session_backup/machines/ATTR_H1/root/outputs/c_attr/parity/S10a_internvl3_8b_ov_dev_b.json` | 5ba968270f755d50d360bd9dfba66fd2bb0ad1233ec768ff2d99ecb2e4a3397d | pull SHA256SUMS of c_attr (a2b63fef) |
| `.session_backup/machines/ATTR_H1/root/outputs/c_attr/parity/S10a_internvl3_8b_ov_dev_a.json` | 7e38688d26a64a5bf2be2c71ddb4df770d5e63bdff242d1eeecfb3ac17307c07 | pull SHA256SUMS of c_attr (a2b63fef) |
| `.session_backup/machines/ATTR_H1/root/outputs/c_attr/parity/S10b_internvl3_8b.json` | aa4e8b5c7874ada7ec4d6445da7a6f17a70ca6aa34d3cd3ccee38f44f1eea74f | pull SHA256SUMS of c_attr (a2b63fef) |
| `.session_backup/machines/ATTR_H1/root/outputs/c_attr/parity/STEP10_internvl3_8b.json` | 866970f99ab709f3ece748b6954d345702582e4dbbe384b1269516fb0940f415 | pull SHA256SUMS of c_attr (a2b63fef) |
| `.session_backup/machines/ATTR_H1/root/outputs/c_attr_b1/parity/D1_internvl3_8b.json` | b819ad40f82d44f0d42f3bd6055e7699dd581a8cad39638590ab0304cc60ecd2 | pull SHA256SUMS of c_attr_b1 (0754128c) |
| `.session_backup/machines/ATTR_H1/root/outputs/c_attr_b1/parity/STEP1B0_internvl3_8b.json` | 3e858c5be63b3a175d753ef03f70be0088c741fa3db9523d17b51038713594bc | pull SHA256SUMS of c_attr_b1 (0754128c) |
| `.session_backup/machines/ATTR_H1/root/outputs/c_attr/parity/S10a_aya_vision_8b_ov_dev_b.json` | e87a37c1f54771ad6023968a3c13d158d04a5693d2e4826620c98b0af6280ca5 | pull SHA256SUMS of c_attr (a2b63fef) |
| `.session_backup/machines/ATTR_H1/root/outputs/c_attr/parity/S10b_aya_vision_8b.json` | 1d00be3abadf320551ea9b54c34fa8b0c72cac3c14d52c7b167ff7cd3f0d0c93 | pull SHA256SUMS of c_attr (a2b63fef) |
| `.session_backup/machines/ATTR_H1/root/outputs/c_attr/parity/STEP10_aya_vision_8b.json` | 0337b1e821d17f90853403fa56456528441fe0d678bc7d0ebc823a770d1b1107 | pull SHA256SUMS of c_attr (a2b63fef) |
| `.session_backup/machines/ATTR_H1/root/outputs/c_attr_b1/parity/D1_aya_vision_8b.json` | a7f4df473dad67db54dc485e5cc9a706d8b883b87c82bdb4bc76b136c1cd9996 | pull SHA256SUMS of c_attr_b1 (0754128c) |
| `.session_backup/machines/ATTR_H1/root/outputs/c_attr_b1/parity/STEP1B0_aya_vision_8b.json` | 1b43c2552aac3ae559d0f7407478a06f26921ccbc64a0a591eaffe45215b88c1 | pull SHA256SUMS of c_attr_b1 (0754128c) |
| `.session_backup/machines/ATTR_H1/root/outputs/c_attr_b1/CAP_1B.json` | 6d42608e205a495215b2d1df30b70ea18d4fa65cc6c5edee437d1fe449a5c3a7 | LOG/ruling pin |
| `scripts/c_attr/block0/K0_REPORT.json` | 15108f2b1260770e4aa92fb44ae6301df45106b52a334d4b33068a4cf1028019 | LOG/ruling pin; HEAD blob equal |
| `.session_backup/machines/ATTR_H1/root/outputs/c_attr_b1/STEPS_1B.tsv` | bd9139b03dd1d5734ea189fff7c532de18387abc4208a07f8b9a7c2d6d711ea4 | LOG/ruling pin |
| `.session_backup/machines/ATTR_H1/root/outputs/c_attr/logs/job.log` | 3917e6d28fa1129e9f4fafdf7e794b9639125db8a85305ec6dfceec77b3718b7 | outside the pull sums by design; only the JOB DONE line (and, for block 1b, the OK lines) used, each stated by OPS-1112c-c-attr-block1-done |
| `.session_backup/machines/ATTR_H1/root/outputs/c_attr_b1/logs/job.log` | 3bf50f52837e9fd04cda6f142db8a80f70e0677c0c253f7e91bf0d06d108848b | outside the pull sums by design; only the JOB DONE line (and, for block 1b, the OK lines) used, each stated by OPS-1112af-c-attr-1b-done-pull |

## TG8 cuts (deviations from TG1 for the judge; no claim added)

- 03_method.md §3.8 "Not used." (package l.90): cut " Section 6.10.8 states which of them ran."
- 05 §5.7 "Multiplicity." (package l.140): "(S-BB; Section 6.10.8)" -> "(S-BB)"
- 06 §6.10.5 draw-share sentences x6 (package l.288): cut "; the intervals of Tables 16 and S21 include this part (Section 5.7)" (its support, the 5.7 draw-variance sentences, is held for the P-3 read)

## Tokens left unfilled: 0



## Filled placeholders (1564 rows; value as stored → value as printed)

| # | source file | key | stored | printed | kind | used in |
|---|---|---|---|---|---|---|
| 1 | data/results/c_attr_1112_score/res/VERIFY.json | `prompts.b1_runs` | 50 | 50 | number | 06_results.md §6.10 |
| 2 | data/results/c_attr_1112_score/res/VERIFY.json | `prompts.pairs` | 50 | 50 | number | 06_results.md §6.10 |
| 3 | data/results/c_attr_1112_score/res/VERIFY.json | `prompts.unequal` | [] | 0 | count | 06_results.md §6.10 |
| 4 | data/results/c_attr_1112_score/res/VERIFY.json | `parity_7_1.result` | "ok" | ok | text | 06_results.md §6.10 |
| 5 | data/results/c_attr_1112_score/res/c_attr_nomination.json | `nominated` | ["H_pair(qwen25vl_7b)", "H_pair(internvl3_8b)"] | H_pair(qwen25vl_7b), H_pair(internvl3_8b) | text | 06_results.md §6.10.3 Table 15 |
| 6 | data/results/c_attr_1112_score/res/c_attr_nomination.json | `rows.qwen25vl_7b~tau_pair.d` | 7.425546158068052 | +7.43 | number | 06_results.md §6.10.3 Table 15 |
| 7 | data/results/c_attr_1112_score/res/c_attr_nomination.json | `rows.qwen25vl_7b~tau_pair.lo` | 5.543342892425909 | 5.54 | number | 06_results.md §6.10.3 Table 15 |
| 8 | data/results/c_attr_1112_score/res/c_attr_nomination.json | `rows.qwen25vl_7b~tau_pair.hi` | 9.196925874039524 | 9.20 | number | 06_results.md §6.10.3 Table 15 |
| 9 | data/results/c_attr_1112_score/res/c_attr_nomination.json | `rows.qwen25vl_7b~tau_marg.d` | -0.055514434687154335 | −0.06 | number | 06_results.md §6.10.3 Table 15 |
| 10 | data/results/c_attr_1112_score/res/c_attr_nomination.json | `rows.qwen25vl_7b~tau_marg.lo` | -1.3847427895170135 | −1.38 | number | 06_results.md §6.10.3 Table 15 |
| 11 | data/results/c_attr_1112_score/res/c_attr_nomination.json | `rows.qwen25vl_7b~tau_marg.hi` | 1.3036076536772785 | 1.30 | number | 06_results.md §6.10.3 Table 15 |
| 12 | data/results/c_attr_1112_score/res/c_attr_nomination.json | `rows.qwen25vl_7b~tau_sel.d` | 7.370031723380897 | +7.37 | number | 06_results.md §6.10.3 Table 15 |
| 13 | data/results/c_attr_1112_score/res/c_attr_nomination.json | `rows.qwen25vl_7b~tau_sel.lo` | 5.480500740944016 | 5.48 | number | 06_results.md §6.10.3 Table 15 |
| 14 | data/results/c_attr_1112_score/res/c_attr_nomination.json | `rows.qwen25vl_7b~tau_sel.hi` | 9.327822952799119 | 9.33 | number | 06_results.md §6.10.3 Table 15 |
| 15 | data/results/c_attr_1112_score/res/c_attr_nomination.json | `rows.internvl3_8b~tau_pair.d` | 4.955545773874867 | +4.96 | number | 06_results.md §6.10.3 Table 15 |
| 16 | data/results/c_attr_1112_score/res/c_attr_nomination.json | `rows.internvl3_8b~tau_pair.lo` | 3.1184246062019736 | 3.12 | number | 06_results.md §6.10.3 Table 15 |
| 17 | data/results/c_attr_1112_score/res/c_attr_nomination.json | `rows.internvl3_8b~tau_pair.hi` | 6.819400552963782 | 6.82 | number | 06_results.md §6.10.3 Table 15 |
| 18 | data/results/c_attr_1112_score/res/c_attr_nomination.json | `rows.internvl3_8b~tau_marg.d` | -1.4286902305159188 | −1.43 | number | 06_results.md §6.10.3 Table 15 |
| 19 | data/results/c_attr_1112_score/res/c_attr_nomination.json | `rows.internvl3_8b~tau_marg.lo` | -2.782270439077938 | −2.78 | number | 06_results.md §6.10.3 Table 15 |
| 20 | data/results/c_attr_1112_score/res/c_attr_nomination.json | `rows.internvl3_8b~tau_marg.hi` | -0.07796801317234082 | −0.08 | number | 06_results.md §6.10.3 Table 15 |
| 21 | data/results/c_attr_1112_score/res/c_attr_nomination.json | `rows.internvl3_8b~tau_sel.d` | 3.5268555433589484 | +3.53 | number | 06_results.md §6.10.3 Table 15 |
| 22 | data/results/c_attr_1112_score/res/c_attr_nomination.json | `rows.internvl3_8b~tau_sel.lo` | 1.6370859083424707 | 1.64 | number | 06_results.md §6.10.3 Table 15 |
| 23 | data/results/c_attr_1112_score/res/c_attr_nomination.json | `rows.internvl3_8b~tau_sel.hi` | 5.3902792782656395 | 5.39 | number | 06_results.md §6.10.3 Table 15 |
| 24 | data/results/c_attr_1112_score/res/VERDICT.json | `sets.ov_dev_b.rows.qwen25vl_7b~tau_pair.d` | 7.304952972972977 | +7.30 | number | 06_results.md §6.10.3 Table 16 |
| 25 | data/results/c_attr_1112_score/res/VERDICT.json | `sets.ov_dev_b.rows.qwen25vl_7b~tau_pair.lo` | 5.57678686756757 | 5.58 | number | 06_results.md §6.10.3 Table 16 |
| 26 | data/results/c_attr_1112_score/res/VERDICT.json | `sets.ov_dev_b.rows.qwen25vl_7b~tau_pair.hi` | 9.246359268918917 | 9.25 | number | 06_results.md §6.10.3 Table 16 |
| 27 | data/results/c_attr_1112_score/res/VERDICT.json | `sets.ov_dev_b.rows.qwen25vl_7b~tau_pair.p` | 0.0004997501249375312 | at its floor (1/2,001) | number | 06_results.md §6.10.3 Table 16 |
| 28 | data/results/c_attr_1112_score/res/VERDICT.json | `sets.ov_dev_b.rows.qwen25vl_7b~tau_pair.m` | 2 | 2 | number | 06_results.md §6.10.3 Table 16 |
| 29 | data/results/c_attr_1112_score/res/VERDICT.json | `sets.ov_dev_b.rows.qwen25vl_7b~tau_pair.label` | "DETECTED" | DETECTED | label | 06_results.md §6.10.3 Table 16 |
| 30 | data/results/c_attr_1112_score/res/VERDICT.json | `sets.ov_dev_b.rows.qwen25vl_7b~tau_marg.d` | 0.9615085405405353 | +0.96 | number | 06_results.md §6.10.3 Table 16 |
| 31 | data/results/c_attr_1112_score/res/VERDICT.json | `sets.ov_dev_b.rows.qwen25vl_7b~tau_marg.lo` | 0.013999703603605433 | 0.01 | number | 06_results.md §6.10.3 Table 16 |
| 32 | data/results/c_attr_1112_score/res/VERDICT.json | `sets.ov_dev_b.rows.qwen25vl_7b~tau_marg.hi` | 1.9406458378378355 | 1.94 | number | 06_results.md §6.10.3 Table 16 |
| 33 | data/results/c_attr_1112_score/res/VERDICT.json | `sets.ov_dev_b.rows.qwen25vl_7b~tau_marg.p` | 0.02348825587206397 | 0.0235 | number | 06_results.md §6.10.3 Table 16 |
| 34 | data/results/c_attr_1112_score/res/VERDICT.json | `sets.ov_dev_b.rows.qwen25vl_7b~tau_marg.m` | 1 | 1 | number | 06_results.md §6.10.3 Table 16 |
| 35 | data/results/c_attr_1112_score/res/VERDICT.json | `sets.ov_dev_b.rows.qwen25vl_7b~tau_marg.label` | "NEGLIGIBLE" | NEGLIGIBLE | label | 06_results.md §6.10.3 Table 16 |
| 36 | data/results/c_attr_1112_score/res/VERDICT.json | `sets.ov_dev_b.rows.qwen25vl_7b~tau_sel.d` | 8.266461513513512 | +8.27 | number | 06_results.md §6.10.3 Table 16 |
| 37 | data/results/c_attr_1112_score/res/VERDICT.json | `sets.ov_dev_b.rows.qwen25vl_7b~tau_sel.lo` | 6.5360347648648585 | 6.54 | number | 06_results.md §6.10.3 Table 16 |
| 38 | data/results/c_attr_1112_score/res/VERDICT.json | `sets.ov_dev_b.rows.qwen25vl_7b~tau_sel.hi` | 10.108259738738747 | 10.11 | number | 06_results.md §6.10.3 Table 16 |
| 39 | data/results/c_attr_1112_score/res/VERDICT.json | `sets.ov_dev_b.rows.qwen25vl_7b~tau_sel.p` | 0.0004997501249375312 | at its floor (1/2,001) | number | 06_results.md §6.10.3 Table 16 |
| 40 | data/results/c_attr_1112_score/res/VERDICT.json | `sets.ov_dev_b.rows.qwen25vl_7b~tau_sel.m` | 1 | 1 | number | 06_results.md §6.10.3 Table 16 |
| 41 | data/results/c_attr_1112_score/res/VERDICT.json | `sets.ov_dev_b.rows.qwen25vl_7b~tau_sel.label` | "DETECTED" | DETECTED | label | 06_results.md §6.10.3 Table 16 |
| 42 | data/results/c_attr_1112_score/res/VERDICT.json | `sets.ov_dev_b.rows.internvl3_8b~tau_pair.d` | 5.571313999999994 | +5.57 | number | 06_results.md §6.10.3 Table 16 |
| 43 | data/results/c_attr_1112_score/res/VERDICT.json | `sets.ov_dev_b.rows.internvl3_8b~tau_pair.lo` | 3.9416437662162176 | 3.94 | number | 06_results.md §6.10.3 Table 16 |
| 44 | data/results/c_attr_1112_score/res/VERDICT.json | `sets.ov_dev_b.rows.internvl3_8b~tau_pair.hi` | 7.271802772972968 | 7.27 | number | 06_results.md §6.10.3 Table 16 |
| 45 | data/results/c_attr_1112_score/res/VERDICT.json | `sets.ov_dev_b.rows.internvl3_8b~tau_pair.p` | 0.0004997501249375312 | at its floor (1/2,001) | number | 06_results.md §6.10.3 Table 16 |
| 46 | data/results/c_attr_1112_score/res/VERDICT.json | `sets.ov_dev_b.rows.internvl3_8b~tau_pair.m` | 2 | 2 | number | 06_results.md §6.10.3 Table 16 |
| 47 | data/results/c_attr_1112_score/res/VERDICT.json | `sets.ov_dev_b.rows.internvl3_8b~tau_pair.label` | "DETECTED" | DETECTED | label | 06_results.md §6.10.3 Table 16 |
| 48 | data/results/c_attr_1112_score/res/VERDICT.json | `sets.ov_dev_b.rows.internvl3_8b~tau_marg.d` | -0.35087590990990947 | −0.35 | number | 06_results.md §6.10.3 Table 16 |
| 49 | data/results/c_attr_1112_score/res/VERDICT.json | `sets.ov_dev_b.rows.internvl3_8b~tau_marg.lo` | -1.4001851819819833 | −1.40 | number | 06_results.md §6.10.3 Table 16 |
| 50 | data/results/c_attr_1112_score/res/VERDICT.json | `sets.ov_dev_b.rows.internvl3_8b~tau_marg.hi` | 0.6966404364864898 | 0.70 | number | 06_results.md §6.10.3 Table 16 |
| 51 | data/results/c_attr_1112_score/res/VERDICT.json | `sets.ov_dev_b.rows.internvl3_8b~tau_marg.p` | 0.7486256871564217 | 0.749 | number | 06_results.md §6.10.3 Table 16 |
| 52 | data/results/c_attr_1112_score/res/VERDICT.json | `sets.ov_dev_b.rows.internvl3_8b~tau_marg.m` | 1 | 1 | number | 06_results.md §6.10.3 Table 16 |
| 53 | data/results/c_attr_1112_score/res/VERDICT.json | `sets.ov_dev_b.rows.internvl3_8b~tau_marg.label` | "NEGLIGIBLE" | NEGLIGIBLE | label | 06_results.md §6.10.3 Table 16 |
| 54 | data/results/c_attr_1112_score/res/VERDICT.json | `sets.ov_dev_b.rows.internvl3_8b~tau_sel.d` | 5.220438090090084 | +5.22 | number | 06_results.md §6.10.3 Table 16 |
| 55 | data/results/c_attr_1112_score/res/VERDICT.json | `sets.ov_dev_b.rows.internvl3_8b~tau_sel.lo` | 3.674398657657658 | 3.67 | number | 06_results.md §6.10.3 Table 16 |
| 56 | data/results/c_attr_1112_score/res/VERDICT.json | `sets.ov_dev_b.rows.internvl3_8b~tau_sel.hi` | 6.807832445045041 | 6.81 | number | 06_results.md §6.10.3 Table 16 |
| 57 | data/results/c_attr_1112_score/res/VERDICT.json | `sets.ov_dev_b.rows.internvl3_8b~tau_sel.p` | 0.0004997501249375312 | at its floor (1/2,001) | number | 06_results.md §6.10.3 Table 16 |
| 58 | data/results/c_attr_1112_score/res/VERDICT.json | `sets.ov_dev_b.rows.internvl3_8b~tau_sel.m` | 1 | 1 | number | 06_results.md §6.10.3 Table 16 |
| 59 | data/results/c_attr_1112_score/res/VERDICT.json | `sets.ov_dev_b.rows.internvl3_8b~tau_sel.label` | "DETECTED" | DETECTED | label | 06_results.md §6.10.3 Table 16 |
| 60 | data/results/c_attr_1112_score/res/VERDICT.json | `sets.ov_dev_b.rows.aya_vision_8b~tau_pair.d` | 6.77628524324324 | +6.78 | number | 06_results.md §6.10.3 Table 16 |
| 61 | data/results/c_attr_1112_score/res/VERDICT.json | `sets.ov_dev_b.rows.aya_vision_8b~tau_pair.lo` | 5.3348291067567635 | 5.33 | number | 06_results.md §6.10.3 Table 16 |
| 62 | data/results/c_attr_1112_score/res/VERDICT.json | `sets.ov_dev_b.rows.aya_vision_8b~tau_pair.hi` | 8.29571288243243 | 8.30 | number | 06_results.md §6.10.3 Table 16 |
| 63 | data/results/c_attr_1112_score/res/VERDICT.json | `sets.ov_dev_b.rows.aya_vision_8b~tau_pair.p` | 0.0004997501249375312 | at its floor (1/2,001) | number | 06_results.md §6.10.3 Table 16 |
| 64 | data/results/c_attr_1112_score/res/VERDICT.json | `sets.ov_dev_b.rows.aya_vision_8b~tau_pair.m` | 1 | 1 | number | 06_results.md §6.10.3 Table 16 |
| 65 | data/results/c_attr_1112_score/res/VERDICT.json | `sets.ov_dev_b.rows.aya_vision_8b~tau_pair.label` | "DETECTED" | DETECTED | label | 06_results.md §6.10.3 Table 16 |
| 66 | data/results/c_attr_1112_score/res/VERDICT.json | `sets.ov_dev_b.rows.aya_vision_8b~tau_marg.d` | -0.5282516576576555 | −0.53 | number | 06_results.md §6.10.3 Table 16 |
| 67 | data/results/c_attr_1112_score/res/VERDICT.json | `sets.ov_dev_b.rows.aya_vision_8b~tau_marg.lo` | -1.4580608400900907 | −1.46 | number | 06_results.md §6.10.3 Table 16 |
| 68 | data/results/c_attr_1112_score/res/VERDICT.json | `sets.ov_dev_b.rows.aya_vision_8b~tau_marg.hi` | 0.4084987022522563 | 0.41 | number | 06_results.md §6.10.3 Table 16 |
| 69 | data/results/c_attr_1112_score/res/VERDICT.json | `sets.ov_dev_b.rows.aya_vision_8b~tau_marg.p` | 0.8740629685157422 | 0.874 | number | 06_results.md §6.10.3 Table 16 |
| 70 | data/results/c_attr_1112_score/res/VERDICT.json | `sets.ov_dev_b.rows.aya_vision_8b~tau_marg.m` | 1 | 1 | number | 06_results.md §6.10.3 Table 16 |
| 71 | data/results/c_attr_1112_score/res/VERDICT.json | `sets.ov_dev_b.rows.aya_vision_8b~tau_marg.label` | "NEGLIGIBLE" | NEGLIGIBLE | label | 06_results.md §6.10.3 Table 16 |
| 72 | data/results/c_attr_1112_score/res/VERDICT.json | `sets.ov_dev_b.rows.aya_vision_8b~tau_sel.d` | 6.248033585585585 | +6.25 | number | 06_results.md §6.10.3 Table 16 |
| 73 | data/results/c_attr_1112_score/res/VERDICT.json | `sets.ov_dev_b.rows.aya_vision_8b~tau_sel.lo` | 4.871869390090089 | 4.87 | number | 06_results.md §6.10.3 Table 16 |
| 74 | data/results/c_attr_1112_score/res/VERDICT.json | `sets.ov_dev_b.rows.aya_vision_8b~tau_sel.hi` | 7.68671373873874 | 7.69 | number | 06_results.md §6.10.3 Table 16 |
| 75 | data/results/c_attr_1112_score/res/VERDICT.json | `sets.ov_dev_b.rows.aya_vision_8b~tau_sel.p` | 0.0004997501249375312 | at its floor (1/2,001) | number | 06_results.md §6.10.3 Table 16 |
| 76 | data/results/c_attr_1112_score/res/VERDICT.json | `sets.ov_dev_b.rows.aya_vision_8b~tau_sel.m` | 1 | 1 | number | 06_results.md §6.10.3 Table 16 |
| 77 | data/results/c_attr_1112_score/res/VERDICT.json | `sets.ov_dev_b.rows.aya_vision_8b~tau_sel.label` | "DETECTED" | DETECTED | label | 06_results.md §6.10.3 Table 16 |
| 78 | data/results/c_attr_1112_score/res/VERDICT.json | `sets.ov_dev_b.rows.qwen25vl_7b~tau_any.d` | 11.098666810810812 | +11.10 | number | 06_results.md §6.10.3 Table 16 |
| 79 | data/results/c_attr_1112_score/res/VERDICT.json | `sets.ov_dev_b.rows.qwen25vl_7b~tau_any.lo` | 9.73213418918919 | 9.73 | number | 06_results.md §6.10.3 Table 16 |
| 80 | data/results/c_attr_1112_score/res/VERDICT.json | `sets.ov_dev_b.rows.qwen25vl_7b~tau_any.hi` | 12.442437478378375 | 12.44 | number | 06_results.md §6.10.3 Table 16 |
| 81 | data/results/c_attr_1112_score/res/VERDICT.json | `sets.ov_dev_b.rows.qwen25vl_7b~tau_any.p` | 0.0004997501249375312 | at its floor (1/2,001) | number | 06_results.md §6.10.3 Table 16 |
| 82 | data/results/c_attr_1112_score/res/VERDICT.json | `sets.ov_dev_b.rows.qwen25vl_7b~tau_any.m` | 1 | 1 | number | 06_results.md §6.10.3 Table 16 |
| 83 | data/results/c_attr_1112_score/res/VERDICT.json | `sets.ov_dev_b.rows.qwen25vl_7b~tau_any.label` | "DETECTED" | DETECTED | label | 06_results.md §6.10.3 Table 16 |
| 84 | data/results/c_attr_1112_score/res/VERDICT.json | `sets.ov_dev_b.rows.internvl3_8b~tau_any.d` | 10.465775423423423 | +10.47 | number | 06_results.md §6.10.3 Table 16 |
| 85 | data/results/c_attr_1112_score/res/VERDICT.json | `sets.ov_dev_b.rows.internvl3_8b~tau_any.lo` | 9.056194427027025 | 9.06 | number | 06_results.md §6.10.3 Table 16 |
| 86 | data/results/c_attr_1112_score/res/VERDICT.json | `sets.ov_dev_b.rows.internvl3_8b~tau_any.hi` | 11.816608999999996 | 11.82 | number | 06_results.md §6.10.3 Table 16 |
| 87 | data/results/c_attr_1112_score/res/VERDICT.json | `sets.ov_dev_b.rows.internvl3_8b~tau_any.p` | 0.0004997501249375312 | at its floor (1/2,001) | number | 06_results.md §6.10.3 Table 16 |
| 88 | data/results/c_attr_1112_score/res/VERDICT.json | `sets.ov_dev_b.rows.internvl3_8b~tau_any.m` | 1 | 1 | number | 06_results.md §6.10.3 Table 16 |
| 89 | data/results/c_attr_1112_score/res/VERDICT.json | `sets.ov_dev_b.rows.internvl3_8b~tau_any.label` | "DETECTED" | DETECTED | label | 06_results.md §6.10.3 Table 16 |
| 90 | data/results/c_attr_1112_score/res/VERDICT.json | `sets.ov_dev_b.rows.aya_vision_8b~tau_any.d` | 13.853420684684686 | +13.85 | number | 06_results.md §6.10.3 Table 16 |
| 91 | data/results/c_attr_1112_score/res/VERDICT.json | `sets.ov_dev_b.rows.aya_vision_8b~tau_any.lo` | 12.71046142162162 | 12.71 | number | 06_results.md §6.10.3 Table 16 |
| 92 | data/results/c_attr_1112_score/res/VERDICT.json | `sets.ov_dev_b.rows.aya_vision_8b~tau_any.hi` | 15.106386545045043 | 15.11 | number | 06_results.md §6.10.3 Table 16 |
| 93 | data/results/c_attr_1112_score/res/VERDICT.json | `sets.ov_dev_b.rows.aya_vision_8b~tau_any.p` | 0.0004997501249375312 | at its floor (1/2,001) | number | 06_results.md §6.10.3 Table 16 |
| 94 | data/results/c_attr_1112_score/res/VERDICT.json | `sets.ov_dev_b.rows.aya_vision_8b~tau_any.m` | 1 | 1 | number | 06_results.md §6.10.3 Table 16 |
| 95 | data/results/c_attr_1112_score/res/VERDICT.json | `sets.ov_dev_b.rows.aya_vision_8b~tau_any.label` | "DETECTED" | DETECTED | label | 06_results.md §6.10.3 Table 16 |
| 96 | data/results/c_attr_1112_score/res/VERDICT.json | `sets.ov_dev_b.rows.qwen25vl_7b~tau_pair.d` | 7.304952972972977 | +7.30 | number | 06_results.md §6.10.3 Table 16 |
| 97 | data/results/c_attr_1112_score/res/VERDICT.json | `sets.ov_dev_b.rows.qwen25vl_7b~tau_pair.lo` | 5.57678686756757 | 5.58 | number | 06_results.md §6.10.3 Table 16 |
| 98 | data/results/c_attr_1112_score/res/VERDICT.json | `sets.ov_dev_b.rows.qwen25vl_7b~tau_pair.hi` | 9.246359268918917 | 9.25 | number | 06_results.md §6.10.3 Table 16 |
| 99 | data/results/c_attr_1112_score/res/VERDICT.json | `sets.ov_dev_b.rows.qwen25vl_7b~tau_pair.p` | 0.0004997501249375312 | 1/2,001, its floor | number | 06_results.md §6.10.3 Table 16 |
| 100 | data/results/c_attr_1112_score/res/VERDICT.json | `sets.ov_dev_b.rows.qwen25vl_7b~tau_pair.label` | "DETECTED" | PASS (label DETECTED) | label | 06_results.md §6.10.3 Table 16 |
| 101 | data/results/c_attr_1112_score/res/VERDICT.json | `sets.ov_dev_b.rows.internvl3_8b~tau_pair.d` | 5.571313999999994 | +5.57 | number | 06_results.md §6.10.3 Table 16 |
| 102 | data/results/c_attr_1112_score/res/VERDICT.json | `sets.ov_dev_b.rows.internvl3_8b~tau_pair.lo` | 3.9416437662162176 | 3.94 | number | 06_results.md §6.10.3 Table 16 |
| 103 | data/results/c_attr_1112_score/res/VERDICT.json | `sets.ov_dev_b.rows.internvl3_8b~tau_pair.hi` | 7.271802772972968 | 7.27 | number | 06_results.md §6.10.3 Table 16 |
| 104 | data/results/c_attr_1112_score/res/VERDICT.json | `sets.ov_dev_b.rows.internvl3_8b~tau_pair.p` | 0.0004997501249375312 | 1/2,001, its floor | number | 06_results.md §6.10.3 Table 16 |
| 105 | data/results/c_attr_1112_score/res/VERDICT.json | `sets.ov_dev_b.rows.internvl3_8b~tau_pair.label` | "DETECTED" | PASS (label DETECTED) | label | 06_results.md §6.10.3 Table 16 |
| 106 | data/results/c_attr_1112_score/res/VERDICT.json | `sets.ov_dev_b.rows.qwen25vl_7b~tau_marg.d` | 0.9615085405405353 | +0.96 | number | 06_results.md §6.10.3 Table 16 |
| 107 | data/results/c_attr_1112_score/res/VERDICT.json | `sets.ov_dev_b.rows.qwen25vl_7b~tau_marg.lo` | 0.013999703603605433 | 0.01 | number | 06_results.md §6.10.3 Table 16 |
| 108 | data/results/c_attr_1112_score/res/VERDICT.json | `sets.ov_dev_b.rows.qwen25vl_7b~tau_marg.hi` | 1.9406458378378355 | 1.94 | number | 06_results.md §6.10.3 Table 16 |
| 109 | data/results/c_attr_1112_score/res/VERDICT.json | `sets.ov_dev_b.rows.qwen25vl_7b~tau_marg.lo90` | 0.17295133693693768 | 0.17 | number | 06_results.md §6.10.3 Table 16 |
| 110 | data/results/c_attr_1112_score/res/VERDICT.json | `sets.ov_dev_b.rows.qwen25vl_7b~tau_marg.hi90` | 1.7444878081081001 | 1.74 | number | 06_results.md §6.10.3 Table 16 |
| 111 | data/results/c_attr_1112_score/res/VERDICT.json | `sets.ov_dev_b.rows.qwen25vl_7b~tau_marg.label` | "NEGLIGIBLE" | NEGLIGIBLE | label | 06_results.md §6.10.3 Table 16 |
| 112 | data/results/c_attr_1112_score/res/VERDICT.json | `sets.ov_dev_b.rows.qwen25vl_7b~tau_sel.d` | 8.266461513513512 | +8.27 | number | 06_results.md §6.10.3 Table 16 |
| 113 | data/results/c_attr_1112_score/res/VERDICT.json | `sets.ov_dev_b.rows.qwen25vl_7b~tau_sel.lo` | 6.5360347648648585 | 6.54 | number | 06_results.md §6.10.3 Table 16 |
| 114 | data/results/c_attr_1112_score/res/VERDICT.json | `sets.ov_dev_b.rows.qwen25vl_7b~tau_sel.hi` | 10.108259738738747 | 10.11 | number | 06_results.md §6.10.3 Table 16 |
| 115 | data/results/c_attr_1112_score/res/VERDICT.json | `sets.ov_dev_b.rows.qwen25vl_7b~tau_sel.p` | 0.0004997501249375312 | 1/2,001, its floor | number | 06_results.md §6.10.3 Table 16 |
| 116 | data/results/c_attr_1112_score/res/VERDICT.json | `sets.ov_dev_b.rows.qwen25vl_7b~tau_sel.label` | "DETECTED" | DETECTED | label | 06_results.md §6.10.3 Table 16 |
| 117 | data/results/c_attr_1112_score/res/VERDICT.json | `sets.ov_dev_b.rows.qwen25vl_7b~tau_any.d` | 11.098666810810812 | +11.10 | number | 06_results.md §6.10.3 Table 16 |
| 118 | data/results/c_attr_1112_score/res/VERDICT.json | `sets.ov_dev_b.rows.qwen25vl_7b~tau_any.lo` | 9.73213418918919 | 9.73 | number | 06_results.md §6.10.3 Table 16 |
| 119 | data/results/c_attr_1112_score/res/VERDICT.json | `sets.ov_dev_b.rows.qwen25vl_7b~tau_any.hi` | 12.442437478378375 | 12.44 | number | 06_results.md §6.10.3 Table 16 |
| 120 | data/results/c_attr_1112_score/res/VERDICT.json | `sets.ov_dev_b.rows.qwen25vl_7b~tau_any.p` | 0.0004997501249375312 | 1/2,001, its floor | number | 06_results.md §6.10.3 Table 16 |
| 121 | data/results/c_attr_1112_score/res/VERDICT.json | `sets.ov_dev_b.rows.qwen25vl_7b~tau_any.label` | "DETECTED" | DETECTED | label | 06_results.md §6.10.3 Table 16 |
| 122 | data/results/c_attr_1112_score/res/VERDICT.json | `sets.ov_dev_b.rows.internvl3_8b~tau_marg.d` | -0.35087590990990947 | −0.35 | number | 06_results.md §6.10.3 Table 16 |
| 123 | data/results/c_attr_1112_score/res/VERDICT.json | `sets.ov_dev_b.rows.internvl3_8b~tau_marg.lo` | -1.4001851819819833 | −1.40 | number | 06_results.md §6.10.3 Table 16 |
| 124 | data/results/c_attr_1112_score/res/VERDICT.json | `sets.ov_dev_b.rows.internvl3_8b~tau_marg.hi` | 0.6966404364864898 | 0.70 | number | 06_results.md §6.10.3 Table 16 |
| 125 | data/results/c_attr_1112_score/res/VERDICT.json | `sets.ov_dev_b.rows.internvl3_8b~tau_marg.lo90` | -1.17659941891893 | −1.18 | number | 06_results.md §6.10.3 Table 16 |
| 126 | data/results/c_attr_1112_score/res/VERDICT.json | `sets.ov_dev_b.rows.internvl3_8b~tau_marg.hi90` | 0.5301149378378358 | 0.53 | number | 06_results.md §6.10.3 Table 16 |
| 127 | data/results/c_attr_1112_score/res/VERDICT.json | `sets.ov_dev_b.rows.internvl3_8b~tau_marg.label` | "NEGLIGIBLE" | NEGLIGIBLE | label | 06_results.md §6.10.3 Table 16 |
| 128 | data/results/c_attr_1112_score/res/VERDICT.json | `sets.ov_dev_b.rows.internvl3_8b~tau_sel.d` | 5.220438090090084 | +5.22 | number | 06_results.md §6.10.3 Table 16 |
| 129 | data/results/c_attr_1112_score/res/VERDICT.json | `sets.ov_dev_b.rows.internvl3_8b~tau_sel.lo` | 3.674398657657658 | 3.67 | number | 06_results.md §6.10.3 Table 16 |
| 130 | data/results/c_attr_1112_score/res/VERDICT.json | `sets.ov_dev_b.rows.internvl3_8b~tau_sel.hi` | 6.807832445045041 | 6.81 | number | 06_results.md §6.10.3 Table 16 |
| 131 | data/results/c_attr_1112_score/res/VERDICT.json | `sets.ov_dev_b.rows.internvl3_8b~tau_sel.p` | 0.0004997501249375312 | 1/2,001, its floor | number | 06_results.md §6.10.3 Table 16 |
| 132 | data/results/c_attr_1112_score/res/VERDICT.json | `sets.ov_dev_b.rows.internvl3_8b~tau_sel.label` | "DETECTED" | DETECTED | label | 06_results.md §6.10.3 Table 16 |
| 133 | data/results/c_attr_1112_score/res/VERDICT.json | `sets.ov_dev_b.rows.internvl3_8b~tau_any.d` | 10.465775423423423 | +10.47 | number | 06_results.md §6.10.3 Table 16 |
| 134 | data/results/c_attr_1112_score/res/VERDICT.json | `sets.ov_dev_b.rows.internvl3_8b~tau_any.lo` | 9.056194427027025 | 9.06 | number | 06_results.md §6.10.3 Table 16 |
| 135 | data/results/c_attr_1112_score/res/VERDICT.json | `sets.ov_dev_b.rows.internvl3_8b~tau_any.hi` | 11.816608999999996 | 11.82 | number | 06_results.md §6.10.3 Table 16 |
| 136 | data/results/c_attr_1112_score/res/VERDICT.json | `sets.ov_dev_b.rows.internvl3_8b~tau_any.p` | 0.0004997501249375312 | 1/2,001, its floor | number | 06_results.md §6.10.3 Table 16 |
| 137 | data/results/c_attr_1112_score/res/VERDICT.json | `sets.ov_dev_b.rows.internvl3_8b~tau_any.label` | "DETECTED" | DETECTED | label | 06_results.md §6.10.3 Table 16 |
| 138 | data/results/c_attr_1112_score/res/VERDICT.json | `sets.ov_dev_b.rows.aya_vision_8b~tau_pair.d` | 6.77628524324324 | +6.78 | number | 06_results.md §6.10.3 Table 16 |
| 139 | data/results/c_attr_1112_score/res/VERDICT.json | `sets.ov_dev_b.rows.aya_vision_8b~tau_pair.lo` | 5.3348291067567635 | 5.33 | number | 06_results.md §6.10.3 Table 16 |
| 140 | data/results/c_attr_1112_score/res/VERDICT.json | `sets.ov_dev_b.rows.aya_vision_8b~tau_pair.hi` | 8.29571288243243 | 8.30 | number | 06_results.md §6.10.3 Table 16 |
| 141 | data/results/c_attr_1112_score/res/VERDICT.json | `sets.ov_dev_b.rows.aya_vision_8b~tau_pair.p` | 0.0004997501249375312 | 1/2,001, its floor | number | 06_results.md §6.10.3 Table 16 |
| 142 | data/results/c_attr_1112_score/res/VERDICT.json | `sets.ov_dev_b.rows.aya_vision_8b~tau_pair.label` | "DETECTED" | DETECTED | label | 06_results.md §6.10.3 Table 16 |
| 143 | data/results/c_attr_1112_score/res/VERDICT.json | `sets.ov_dev_b.rows.aya_vision_8b~tau_marg.d` | -0.5282516576576555 | −0.53 | number | 06_results.md §6.10.3 Table 16 |
| 144 | data/results/c_attr_1112_score/res/VERDICT.json | `sets.ov_dev_b.rows.aya_vision_8b~tau_marg.lo` | -1.4580608400900907 | −1.46 | number | 06_results.md §6.10.3 Table 16 |
| 145 | data/results/c_attr_1112_score/res/VERDICT.json | `sets.ov_dev_b.rows.aya_vision_8b~tau_marg.hi` | 0.4084987022522563 | 0.41 | number | 06_results.md §6.10.3 Table 16 |
| 146 | data/results/c_attr_1112_score/res/VERDICT.json | `sets.ov_dev_b.rows.aya_vision_8b~tau_marg.lo90` | -1.3139612216216234 | −1.31 | number | 06_results.md §6.10.3 Table 16 |
| 147 | data/results/c_attr_1112_score/res/VERDICT.json | `sets.ov_dev_b.rows.aya_vision_8b~tau_marg.hi90` | 0.27426181711711584 | 0.27 | number | 06_results.md §6.10.3 Table 16 |
| 148 | data/results/c_attr_1112_score/res/VERDICT.json | `sets.ov_dev_b.rows.aya_vision_8b~tau_marg.label` | "NEGLIGIBLE" | NEGLIGIBLE | label | 06_results.md §6.10.3 Table 16 |
| 149 | data/results/c_attr_1112_score/res/VERDICT.json | `sets.ov_dev_b.rows.aya_vision_8b~tau_sel.d` | 6.248033585585585 | +6.25 | number | 06_results.md §6.10.3 Table 16 |
| 150 | data/results/c_attr_1112_score/res/VERDICT.json | `sets.ov_dev_b.rows.aya_vision_8b~tau_sel.lo` | 4.871869390090089 | 4.87 | number | 06_results.md §6.10.3 Table 16 |
| 151 | data/results/c_attr_1112_score/res/VERDICT.json | `sets.ov_dev_b.rows.aya_vision_8b~tau_sel.hi` | 7.68671373873874 | 7.69 | number | 06_results.md §6.10.3 Table 16 |
| 152 | data/results/c_attr_1112_score/res/VERDICT.json | `sets.ov_dev_b.rows.aya_vision_8b~tau_sel.p` | 0.0004997501249375312 | 1/2,001, its floor | number | 06_results.md §6.10.3 Table 16 |
| 153 | data/results/c_attr_1112_score/res/VERDICT.json | `sets.ov_dev_b.rows.aya_vision_8b~tau_sel.label` | "DETECTED" | DETECTED | label | 06_results.md §6.10.3 Table 16 |
| 154 | data/results/c_attr_1112_score/res/VERDICT.json | `sets.ov_dev_b.rows.aya_vision_8b~tau_any.d` | 13.853420684684686 | +13.85 | number | 06_results.md §6.10.3 Table 16 |
| 155 | data/results/c_attr_1112_score/res/VERDICT.json | `sets.ov_dev_b.rows.aya_vision_8b~tau_any.lo` | 12.71046142162162 | 12.71 | number | 06_results.md §6.10.3 Table 16 |
| 156 | data/results/c_attr_1112_score/res/VERDICT.json | `sets.ov_dev_b.rows.aya_vision_8b~tau_any.hi` | 15.106386545045043 | 15.11 | number | 06_results.md §6.10.3 Table 16 |
| 157 | data/results/c_attr_1112_score/res/VERDICT.json | `sets.ov_dev_b.rows.aya_vision_8b~tau_any.p` | 0.0004997501249375312 | 1/2,001, its floor | number | 06_results.md §6.10.3 Table 16 |
| 158 | data/results/c_attr_1112_score/res/VERDICT.json | `sets.ov_dev_b.rows.aya_vision_8b~tau_any.label` | "DETECTED" | DETECTED | label | 06_results.md §6.10.3 Table 16 |
| 159 | data/results/c_attr_1112_score/res/DFSENS.json | `status` | "computed" | computed | text | 06_results.md §6.10.3 (last paragraph); Table S25a |
| 160 | data/results/c_attr_1112_score/res/VERDICT.json | `sets.ov_dev_b.rows.aya_vision_8b~placebo_d1_d2.d` | -2.031620864864866 | −2.03 | number | 06_results.md §6.10.5 |
| 161 | data/results/c_attr_1112_score/res/VERDICT.json | `sets.ov_dev_b.rows.aya_vision_8b~placebo_d1_d2.lo` | -3.4191781540540562 | −3.42 | number | 06_results.md §6.10.5 |
| 162 | data/results/c_attr_1112_score/res/VERDICT.json | `sets.ov_dev_b.rows.aya_vision_8b~placebo_d1_d2.hi` | -0.7409918891891858 | −0.74 | number | 06_results.md §6.10.5 |
| 163 | data/results/c_attr_1112_score/res/VERDICT.json | `sets.ov_dev_b.rows.aya_vision_8b~placebo_d1_d2.flag` | true | flagged | label | 06_results.md §6.10.5 |
| 164 | data/results/c_attr_1112_score/res/SUMMARY.json | `sets.ov_dev_b.variance.qwen25vl_7b.share` | 0.0886998970528775 | 0.089 | number | 06_results.md §6.10.5 |
| 165 | data/results/c_attr_1112_score/res/SUMMARY.json | `sets.ov_dev_b.variance.internvl3_8b.share` | 0.1631763367076525 | 0.163 | number | 06_results.md §6.10.5 |
| 166 | data/results/c_attr_1112_score/res/SUMMARY.json | `sets.ov_dev_b.variance.aya_vision_8b.share` | 0.1494676979695886 | 0.149 | number | 06_results.md §6.10.5 |
| 167 | data/results/c_attr_1112_score/res/SUMMARY.json | `sets.xm_dev500.variance.qwen25vl_7b.share` | 0.16013079972847782 | 0.160 | number | 06_results.md §6.10.5 |
| 168 | data/results/c_attr_1112_score/res/SUMMARY.json | `sets.xm_dev500.variance.internvl3_8b.share` | 0.1915660835218231 | 0.192 | number | 06_results.md §6.10.5 |
| 169 | data/results/c_attr_1112_score/res/SUMMARY.json | `sets.xm_dev500.variance.aya_vision_8b.share` | 0.20328366065844103 | 0.203 | number | 06_results.md §6.10.5 |
| 170 | data/results/c_attr_1112_score/res/SUMMARY.json | `batched.ov_dev_b.fixed_set.qwen25vl_7b.label` | "conditional on the realised fixed set" | conditional on the realised fixed set | label | 06_results.md §6.10.5 |
| 171 | data/results/c_attr_1112_score/res/SUMMARY.json | `batched.ov_dev_b.fixed_set.qwen25vl_7b.omega` | 2.5126771001134514 | 2.51 | number | 06_results.md §6.10.5 |
| 172 | data/results/c_attr_1112_score/res/SUMMARY.json | `batched.ov_dev_b.fixed_set.qwen25vl_7b.omega_upper` | 15.197522895461283 | 15.20 | number | 06_results.md §6.10.5 |
| 173 | data/results/c_attr_1112_score/res/SUMMARY.json | `batched.xm_dev500.fixed_set.qwen25vl_7b.label` | "conditional on the realised fixed set" | conditional on the realised fixed set | label | 06_results.md §6.10.5 |
| 174 | data/results/c_attr_1112_score/res/SUMMARY.json | `batched.xm_dev500.fixed_set.qwen25vl_7b.omega` | 0.44315803460085584 | 0.44 | number | 06_results.md §6.10.5 |
| 175 | data/results/c_attr_1112_score/res/SUMMARY.json | `batched.xm_dev500.fixed_set.qwen25vl_7b.omega_upper` | 4.2071179831759995 | 4.21 | number | 06_results.md §6.10.5 |
| 176 | data/results/c_attr_1112_score/res/COPYBOUND_ov_dev_b_qwen25vl_7b.json | `bound.i_syllables.n3.withdrawn` | false | in force | label | 06_results.md §6.10.6 Table 17 |
| 177 | data/results/c_attr_1112_score/res/COPYBOUND_ov_dev_b_qwen25vl_7b.json | `bound.i_syllables.monotonicity check failed` | false | – | label | 06_results.md §6.10.6 Table 17 |
| 178 | data/results/c_attr_1112_score/res/COPYBOUND_ov_dev_b_qwen25vl_7b.json | `bound.i_syllables.n3.K_ret.d` | 18.58449544906159 | +18.58 | number | 06_results.md §6.10.6 Table 17 |
| 179 | data/results/c_attr_1112_score/res/COPYBOUND_ov_dev_b_qwen25vl_7b.json | `bound.i_syllables.n3.K_ret.lo` | 16.563576582062172 | 16.56 | number | 06_results.md §6.10.6 Table 17 |
| 180 | data/results/c_attr_1112_score/res/COPYBOUND_ov_dev_b_qwen25vl_7b.json | `bound.i_syllables.n3.K_ret.hi` | 20.728290133833966 | 20.73 | number | 06_results.md §6.10.6 Table 17 |
| 181 | data/results/c_attr_1112_score/res/COPYBOUND_ov_dev_b_qwen25vl_7b.json | `bound.i_syllables.n3.K_ret.label` | "DETECTED" | DETECTED | label | 06_results.md §6.10.6 Table 17 |
| 182 | data/results/c_attr_1112_score/res/COPYBOUND_ov_dev_b_qwen25vl_7b.json | `bound.i_syllables.n3.L_cp.d` | -8.914878699583078 | −8.91 | number | 06_results.md §6.10.6 Table 17 |
| 183 | data/results/c_attr_1112_score/res/COPYBOUND_ov_dev_b_qwen25vl_7b.json | `bound.i_syllables.n3.L_cp.lo` | -10.707668881201924 | −10.71 | number | 06_results.md §6.10.6 Table 17 |
| 184 | data/results/c_attr_1112_score/res/COPYBOUND_ov_dev_b_qwen25vl_7b.json | `bound.i_syllables.n3.L_cp.hi` | -7.06586722529071 | −7.07 | number | 06_results.md §6.10.6 Table 17 |
| 185 | data/results/c_attr_1112_score/res/COPYBOUND_ov_dev_b_qwen25vl_7b.json | `bound.i_syllables.n3.L_cp.label` | "REVERSED" | REVERSED | label | 06_results.md §6.10.6 Table 17 |
| 186 | data/results/c_attr_1112_score/res/COPYBOUND_ov_dev_b_qwen25vl_7b.json | `bound.i_syllables.n3.K_nc.d` | 5.587956366154785 | +5.59 | number | 06_results.md §6.10.6 Table 17 |
| 187 | data/results/c_attr_1112_score/res/COPYBOUND_ov_dev_b_qwen25vl_7b.json | `bound.i_syllables.n3.K_nc.lo` | 4.411402401183649 | 4.41 | number | 06_results.md §6.10.6 Table 17 |
| 188 | data/results/c_attr_1112_score/res/COPYBOUND_ov_dev_b_qwen25vl_7b.json | `bound.i_syllables.n3.K_nc.hi` | 6.748425069214175 | 6.75 | number | 06_results.md §6.10.6 Table 17 |
| 189 | data/results/c_attr_1112_score/res/COPYBOUND_ov_dev_b_qwen25vl_7b.json | `bound.i_syllables.n3.K_nc.label` | "DETECTED" | DETECTED | label | 06_results.md §6.10.6 Table 17 |
| 190 | data/results/c_attr_1112_score/res/COPYBOUND_ov_dev_b_qwen25vl_7b.json | `bound.ii_words.n3.withdrawn` | false | in force | label | 06_results.md §6.10.6 Table 17 |
| 191 | data/results/c_attr_1112_score/res/COPYBOUND_ov_dev_b_qwen25vl_7b.json | `bound.ii_words.monotonicity check failed` | false | – | label | 06_results.md §6.10.6 Table 17 |
| 192 | data/results/c_attr_1112_score/res/COPYBOUND_ov_dev_b_qwen25vl_7b.json | `bound.ii_words.n3.K_ret.d` | 18.744748958014974 | +18.74 | number | 06_results.md §6.10.6 Table 17 |
| 193 | data/results/c_attr_1112_score/res/COPYBOUND_ov_dev_b_qwen25vl_7b.json | `bound.ii_words.n3.K_ret.lo` | 16.709541442190336 | 16.71 | number | 06_results.md §6.10.6 Table 17 |
| 194 | data/results/c_attr_1112_score/res/COPYBOUND_ov_dev_b_qwen25vl_7b.json | `bound.ii_words.n3.K_ret.hi` | 20.841703464971697 | 20.84 | number | 06_results.md §6.10.6 Table 17 |
| 195 | data/results/c_attr_1112_score/res/COPYBOUND_ov_dev_b_qwen25vl_7b.json | `bound.ii_words.n3.K_ret.label` | "DETECTED" | DETECTED | label | 06_results.md §6.10.6 Table 17 |
| 196 | data/results/c_attr_1112_score/res/COPYBOUND_ov_dev_b_qwen25vl_7b.json | `bound.ii_words.n3.L_cp.d` | -9.075132208536466 | −9.08 | number | 06_results.md §6.10.6 Table 17 |
| 197 | data/results/c_attr_1112_score/res/COPYBOUND_ov_dev_b_qwen25vl_7b.json | `bound.ii_words.n3.L_cp.lo` | -10.981918956274114 | −10.98 | number | 06_results.md §6.10.6 Table 17 |
| 198 | data/results/c_attr_1112_score/res/COPYBOUND_ov_dev_b_qwen25vl_7b.json | `bound.ii_words.n3.L_cp.hi` | -7.218559968005788 | −7.22 | number | 06_results.md §6.10.6 Table 17 |
| 199 | data/results/c_attr_1112_score/res/COPYBOUND_ov_dev_b_qwen25vl_7b.json | `bound.ii_words.n3.L_cp.label` | "REVERSED" | REVERSED | label | 06_results.md §6.10.6 Table 17 |
| 200 | data/results/c_attr_1112_score/res/COPYBOUND_ov_dev_b_qwen25vl_7b.json | `bound.ii_words.n3.K_nc.d` | 5.763409396791424 | +5.76 | number | 06_results.md §6.10.6 Table 17 |
| 201 | data/results/c_attr_1112_score/res/COPYBOUND_ov_dev_b_qwen25vl_7b.json | `bound.ii_words.n3.K_nc.lo` | 4.710411667316011 | 4.71 | number | 06_results.md §6.10.6 Table 17 |
| 202 | data/results/c_attr_1112_score/res/COPYBOUND_ov_dev_b_qwen25vl_7b.json | `bound.ii_words.n3.K_nc.hi` | 6.946254936929598 | 6.95 | number | 06_results.md §6.10.6 Table 17 |
| 203 | data/results/c_attr_1112_score/res/COPYBOUND_ov_dev_b_qwen25vl_7b.json | `bound.ii_words.n3.K_nc.label` | "DETECTED" | DETECTED | label | 06_results.md §6.10.6 Table 17 |
| 204 | data/results/c_attr_1112_score/res/COPYBOUND_ov_dev_b_internvl3_8b.json | `bound.i_syllables.n3.withdrawn` | false | in force | label | 06_results.md §6.10.6 Table 17 |
| 205 | data/results/c_attr_1112_score/res/COPYBOUND_ov_dev_b_internvl3_8b.json | `bound.i_syllables.monotonicity check failed` | false | – | label | 06_results.md §6.10.6 Table 17 |
| 206 | data/results/c_attr_1112_score/res/COPYBOUND_ov_dev_b_internvl3_8b.json | `bound.i_syllables.n3.K_ret.d` | 9.930191644911444 | +9.93 | number | 06_results.md §6.10.6 Table 17 |
| 207 | data/results/c_attr_1112_score/res/COPYBOUND_ov_dev_b_internvl3_8b.json | `bound.i_syllables.n3.K_ret.lo` | 8.3114443484374 | 8.31 | number | 06_results.md §6.10.6 Table 17 |
| 208 | data/results/c_attr_1112_score/res/COPYBOUND_ov_dev_b_internvl3_8b.json | `bound.i_syllables.n3.K_ret.hi` | 11.599691381171834 | 11.60 | number | 06_results.md §6.10.6 Table 17 |
| 209 | data/results/c_attr_1112_score/res/COPYBOUND_ov_dev_b_internvl3_8b.json | `bound.i_syllables.n3.K_ret.label` | "DETECTED" | DETECTED | label | 06_results.md §6.10.6 Table 17 |
| 210 | data/results/c_attr_1112_score/res/COPYBOUND_ov_dev_b_internvl3_8b.json | `bound.i_syllables.n3.L_cp.d` | -4.573759735321315 | −4.57 | number | 06_results.md §6.10.6 Table 17 |
| 211 | data/results/c_attr_1112_score/res/COPYBOUND_ov_dev_b_internvl3_8b.json | `bound.i_syllables.n3.L_cp.lo` | -6.4621888546336175 | −6.46 | number | 06_results.md §6.10.6 Table 17 |
| 212 | data/results/c_attr_1112_score/res/COPYBOUND_ov_dev_b_internvl3_8b.json | `bound.i_syllables.n3.L_cp.hi` | -2.611113435330269 | −2.61 | number | 06_results.md §6.10.6 Table 17 |
| 213 | data/results/c_attr_1112_score/res/COPYBOUND_ov_dev_b_internvl3_8b.json | `bound.i_syllables.n3.L_cp.label` | "REVERSED" | REVERSED | label | 06_results.md §6.10.6 Table 17 |
| 214 | data/results/c_attr_1112_score/res/COPYBOUND_ov_dev_b_internvl3_8b.json | `bound.i_syllables.n3.K_nc.d` | 2.6512390611780208 | +2.65 | number | 06_results.md §6.10.6 Table 17 |
| 215 | data/results/c_attr_1112_score/res/COPYBOUND_ov_dev_b_internvl3_8b.json | `bound.i_syllables.n3.K_nc.lo` | 1.6056779017737755 | 1.61 | number | 06_results.md §6.10.6 Table 17 |
| 216 | data/results/c_attr_1112_score/res/COPYBOUND_ov_dev_b_internvl3_8b.json | `bound.i_syllables.n3.K_nc.hi` | 3.7564925870071915 | 3.76 | number | 06_results.md §6.10.6 Table 17 |
| 217 | data/results/c_attr_1112_score/res/COPYBOUND_ov_dev_b_internvl3_8b.json | `bound.i_syllables.n3.K_nc.label` | "DETECTED" | DETECTED | label | 06_results.md §6.10.6 Table 17 |
| 218 | data/results/c_attr_1112_score/res/COPYBOUND_ov_dev_b_internvl3_8b.json | `bound.ii_words.n3.withdrawn` | false | in force | label | 06_results.md §6.10.6 Table 17 |
| 219 | data/results/c_attr_1112_score/res/COPYBOUND_ov_dev_b_internvl3_8b.json | `bound.ii_words.monotonicity check failed` | false | – | label | 06_results.md §6.10.6 Table 17 |
| 220 | data/results/c_attr_1112_score/res/COPYBOUND_ov_dev_b_internvl3_8b.json | `bound.ii_words.n3.K_ret.d` | 8.99277629645961 | +8.99 | number | 06_results.md §6.10.6 Table 17 |
| 221 | data/results/c_attr_1112_score/res/COPYBOUND_ov_dev_b_internvl3_8b.json | `bound.ii_words.n3.K_ret.lo` | 7.483059970757614 | 7.48 | number | 06_results.md §6.10.6 Table 17 |
| 222 | data/results/c_attr_1112_score/res/COPYBOUND_ov_dev_b_internvl3_8b.json | `bound.ii_words.n3.K_ret.hi` | 10.574427316745426 | 10.57 | number | 06_results.md §6.10.6 Table 17 |
| 223 | data/results/c_attr_1112_score/res/COPYBOUND_ov_dev_b_internvl3_8b.json | `bound.ii_words.n3.K_ret.label` | "DETECTED" | DETECTED | label | 06_results.md §6.10.6 Table 17 |
| 224 | data/results/c_attr_1112_score/res/COPYBOUND_ov_dev_b_internvl3_8b.json | `bound.ii_words.n3.L_cp.d` | -3.6363443868694802 | −3.64 | number | 06_results.md §6.10.6 Table 17 |
| 225 | data/results/c_attr_1112_score/res/COPYBOUND_ov_dev_b_internvl3_8b.json | `bound.ii_words.n3.L_cp.lo` | -5.550854071186638 | −5.55 | number | 06_results.md §6.10.6 Table 17 |
| 226 | data/results/c_attr_1112_score/res/COPYBOUND_ov_dev_b_internvl3_8b.json | `bound.ii_words.n3.L_cp.hi` | -1.6886715001354877 | −1.69 | number | 06_results.md §6.10.6 Table 17 |
| 227 | data/results/c_attr_1112_score/res/COPYBOUND_ov_dev_b_internvl3_8b.json | `bound.ii_words.n3.L_cp.label` | "REVERSED" | REVERSED | label | 06_results.md §6.10.6 Table 17 |
| 228 | data/results/c_attr_1112_score/res/COPYBOUND_ov_dev_b_internvl3_8b.json | `bound.ii_words.n3.K_nc.d` | 2.9136053661161374 | +2.91 | number | 06_results.md §6.10.6 Table 17 |
| 229 | data/results/c_attr_1112_score/res/COPYBOUND_ov_dev_b_internvl3_8b.json | `bound.ii_words.n3.K_nc.lo` | 1.879252971984675 | 1.88 | number | 06_results.md §6.10.6 Table 17 |
| 230 | data/results/c_attr_1112_score/res/COPYBOUND_ov_dev_b_internvl3_8b.json | `bound.ii_words.n3.K_nc.hi` | 3.9356815288159694 | 3.94 | number | 06_results.md §6.10.6 Table 17 |
| 231 | data/results/c_attr_1112_score/res/COPYBOUND_ov_dev_b_internvl3_8b.json | `bound.ii_words.n3.K_nc.label` | "DETECTED" | DETECTED | label | 06_results.md §6.10.6 Table 17 |
| 232 | data/results/c_attr_1112_score/res/COPYBOUND_ov_dev_b_aya_vision_8b.json | `bound.i_syllables.n3.withdrawn` | false | in force | label | 06_results.md §6.10.6 Table 17 |
| 233 | data/results/c_attr_1112_score/res/COPYBOUND_ov_dev_b_aya_vision_8b.json | `bound.i_syllables.monotonicity check failed` | false | – | label | 06_results.md §6.10.6 Table 17 |
| 234 | data/results/c_attr_1112_score/res/COPYBOUND_ov_dev_b_aya_vision_8b.json | `bound.i_syllables.n3.K_ret.d` | 9.015603056161774 | +9.02 | number | 06_results.md §6.10.6 Table 17 |
| 235 | data/results/c_attr_1112_score/res/COPYBOUND_ov_dev_b_aya_vision_8b.json | `bound.i_syllables.n3.K_ret.lo` | 7.829099297057835 | 7.83 | number | 06_results.md §6.10.6 Table 17 |
| 236 | data/results/c_attr_1112_score/res/COPYBOUND_ov_dev_b_aya_vision_8b.json | `bound.i_syllables.n3.K_ret.hi` | 10.266404539773546 | 10.27 | number | 06_results.md §6.10.6 Table 17 |
| 237 | data/results/c_attr_1112_score/res/COPYBOUND_ov_dev_b_aya_vision_8b.json | `bound.i_syllables.n3.K_ret.label` | "DETECTED" | DETECTED | label | 06_results.md §6.10.6 Table 17 |
| 238 | data/results/c_attr_1112_score/res/COPYBOUND_ov_dev_b_aya_vision_8b.json | `bound.i_syllables.n3.L_cp.d` | -1.7019866073755456 | −1.70 | number | 06_results.md §6.10.6 Table 17 |
| 239 | data/results/c_attr_1112_score/res/COPYBOUND_ov_dev_b_aya_vision_8b.json | `bound.i_syllables.n3.L_cp.lo` | -3.2767966252914245 | −3.28 | number | 06_results.md §6.10.6 Table 17 |
| 240 | data/results/c_attr_1112_score/res/COPYBOUND_ov_dev_b_aya_vision_8b.json | `bound.i_syllables.n3.L_cp.hi` | -0.13369643074849094 | −0.13 | number | 06_results.md §6.10.6 Table 17 |
| 241 | data/results/c_attr_1112_score/res/COPYBOUND_ov_dev_b_aya_vision_8b.json | `bound.i_syllables.n3.L_cp.label` | "REVERSED" | REVERSED | label | 06_results.md §6.10.6 Table 17 |
| 242 | data/results/c_attr_1112_score/res/COPYBOUND_ov_dev_b_aya_vision_8b.json | `bound.i_syllables.n3.K_nc.d` | 3.5049051729064655 | +3.50 | number | 06_results.md §6.10.6 Table 17 |
| 243 | data/results/c_attr_1112_score/res/COPYBOUND_ov_dev_b_aya_vision_8b.json | `bound.i_syllables.n3.K_nc.lo` | 2.7354240083286645 | 2.74 | number | 06_results.md §6.10.6 Table 17 |
| 244 | data/results/c_attr_1112_score/res/COPYBOUND_ov_dev_b_aya_vision_8b.json | `bound.i_syllables.n3.K_nc.hi` | 4.297150391640748 | 4.30 | number | 06_results.md §6.10.6 Table 17 |
| 245 | data/results/c_attr_1112_score/res/COPYBOUND_ov_dev_b_aya_vision_8b.json | `bound.i_syllables.n3.K_nc.label` | "DETECTED" | DETECTED | label | 06_results.md §6.10.6 Table 17 |
| 246 | data/results/c_attr_1112_score/res/COPYBOUND_ov_dev_b_aya_vision_8b.json | `bound.ii_words.n3.withdrawn` | false | in force | label | 06_results.md §6.10.6 Table 17 |
| 247 | data/results/c_attr_1112_score/res/COPYBOUND_ov_dev_b_aya_vision_8b.json | `bound.ii_words.monotonicity check failed` | false | – | label | 06_results.md §6.10.6 Table 17 |
| 248 | data/results/c_attr_1112_score/res/COPYBOUND_ov_dev_b_aya_vision_8b.json | `bound.ii_words.n3.K_ret.d` | 7.879667897111323 | +7.88 | number | 06_results.md §6.10.6 Table 17 |
| 249 | data/results/c_attr_1112_score/res/COPYBOUND_ov_dev_b_aya_vision_8b.json | `bound.ii_words.n3.K_ret.lo` | 6.733035151792877 | 6.73 | number | 06_results.md §6.10.6 Table 17 |
| 250 | data/results/c_attr_1112_score/res/COPYBOUND_ov_dev_b_aya_vision_8b.json | `bound.ii_words.n3.K_ret.hi` | 9.105078916395515 | 9.11 | number | 06_results.md §6.10.6 Table 17 |
| 251 | data/results/c_attr_1112_score/res/COPYBOUND_ov_dev_b_aya_vision_8b.json | `bound.ii_words.n3.K_ret.label` | "DETECTED" | DETECTED | label | 06_results.md §6.10.6 Table 17 |
| 252 | data/results/c_attr_1112_score/res/COPYBOUND_ov_dev_b_aya_vision_8b.json | `bound.ii_words.n3.L_cp.d` | -0.5660514483250949 | −0.57 | number | 06_results.md §6.10.6 Table 17 |
| 253 | data/results/c_attr_1112_score/res/COPYBOUND_ov_dev_b_aya_vision_8b.json | `bound.ii_words.n3.L_cp.lo` | -2.163585953345003 | −2.16 | number | 06_results.md §6.10.6 Table 17 |
| 254 | data/results/c_attr_1112_score/res/COPYBOUND_ov_dev_b_aya_vision_8b.json | `bound.ii_words.n3.L_cp.hi` | 0.9943073192522447 | 0.99 | number | 06_results.md §6.10.6 Table 17 |
| 255 | data/results/c_attr_1112_score/res/COPYBOUND_ov_dev_b_aya_vision_8b.json | `bound.ii_words.n3.L_cp.label` | "NEGLIGIBLE" | NEGLIGIBLE | label | 06_results.md §6.10.6 Table 17 |
| 256 | data/results/c_attr_1112_score/res/COPYBOUND_ov_dev_b_aya_vision_8b.json | `bound.ii_words.n3.K_nc.d` | 2.548901300617866 | +2.55 | number | 06_results.md §6.10.6 Table 17 |
| 257 | data/results/c_attr_1112_score/res/COPYBOUND_ov_dev_b_aya_vision_8b.json | `bound.ii_words.n3.K_nc.lo` | 1.9003322796710789 | 1.90 | number | 06_results.md §6.10.6 Table 17 |
| 258 | data/results/c_attr_1112_score/res/COPYBOUND_ov_dev_b_aya_vision_8b.json | `bound.ii_words.n3.K_nc.hi` | 3.249917224902498 | 3.25 | number | 06_results.md §6.10.6 Table 17 |
| 259 | data/results/c_attr_1112_score/res/COPYBOUND_ov_dev_b_aya_vision_8b.json | `bound.ii_words.n3.K_nc.label` | "DETECTED" | DETECTED | label | 06_results.md §6.10.6 Table 17 |
| 260 | data/results/c_attr_1112_score/res/COPYBOUND_xm_dev500_qwen25vl_7b.json | `bound.i_syllables.n3.withdrawn` | false | in force | label | 06_results.md §6.10.6 Table 17 |
| 261 | data/results/c_attr_1112_score/res/COPYBOUND_xm_dev500_qwen25vl_7b.json | `bound.i_syllables.monotonicity check failed` | false | – | label | 06_results.md §6.10.6 Table 17 |
| 262 | data/results/c_attr_1112_score/res/COPYBOUND_xm_dev500_qwen25vl_7b.json | `bound.i_syllables.n3.K_ret.d` | 14.250830606039694 | +14.25 | number | 06_results.md §6.10.6 Table 17 |
| 263 | data/results/c_attr_1112_score/res/COPYBOUND_xm_dev500_qwen25vl_7b.json | `bound.i_syllables.n3.K_ret.lo` | 11.591669018621667 | 11.59 | number | 06_results.md §6.10.6 Table 17 |
| 264 | data/results/c_attr_1112_score/res/COPYBOUND_xm_dev500_qwen25vl_7b.json | `bound.i_syllables.n3.K_ret.hi` | 17.040899963011668 | 17.04 | number | 06_results.md §6.10.6 Table 17 |
| 265 | data/results/c_attr_1112_score/res/COPYBOUND_xm_dev500_qwen25vl_7b.json | `bound.i_syllables.n3.K_ret.label` | "DETECTED" | DETECTED | label | 06_results.md §6.10.6 Table 17 |
| 266 | data/results/c_attr_1112_score/res/COPYBOUND_xm_dev500_qwen25vl_7b.json | `bound.i_syllables.n3.L_cp.d` | -9.810331287465733 | −9.81 | number | 06_results.md §6.10.6 Table 17 |
| 267 | data/results/c_attr_1112_score/res/COPYBOUND_xm_dev500_qwen25vl_7b.json | `bound.i_syllables.n3.L_cp.lo` | -13.665674727804914 | −13.67 | number | 06_results.md §6.10.6 Table 17 |
| 268 | data/results/c_attr_1112_score/res/COPYBOUND_xm_dev500_qwen25vl_7b.json | `bound.i_syllables.n3.L_cp.hi` | -5.626911363695306 | −5.63 | number | 06_results.md §6.10.6 Table 17 |
| 269 | data/results/c_attr_1112_score/res/COPYBOUND_xm_dev500_qwen25vl_7b.json | `bound.i_syllables.n3.L_cp.label` | "REVERSED" | REVERSED | label | 06_results.md §6.10.6 Table 17 |
| 270 | data/results/c_attr_1112_score/res/COPYBOUND_xm_dev500_qwen25vl_7b.json | `bound.i_syllables.n3.K_nc.d` | 7.591905836734717 | +7.59 | number | 06_results.md §6.10.6 Table 17 |
| 271 | data/results/c_attr_1112_score/res/COPYBOUND_xm_dev500_qwen25vl_7b.json | `bound.i_syllables.n3.K_nc.lo` | 5.35626324314929 | 5.36 | number | 06_results.md §6.10.6 Table 17 |
| 272 | data/results/c_attr_1112_score/res/COPYBOUND_xm_dev500_qwen25vl_7b.json | `bound.i_syllables.n3.K_nc.hi` | 10.004235425661449 | 10.00 | number | 06_results.md §6.10.6 Table 17 |
| 273 | data/results/c_attr_1112_score/res/COPYBOUND_xm_dev500_qwen25vl_7b.json | `bound.i_syllables.n3.K_nc.label` | "DETECTED" | DETECTED | label | 06_results.md §6.10.6 Table 17 |
| 274 | data/results/c_attr_1112_score/res/COPYBOUND_xm_dev500_qwen25vl_7b.json | `bound.ii_words.n3.withdrawn` | false | in force | label | 06_results.md §6.10.6 Table 17 |
| 275 | data/results/c_attr_1112_score/res/COPYBOUND_xm_dev500_qwen25vl_7b.json | `bound.ii_words.monotonicity check failed` | false | – | label | 06_results.md §6.10.6 Table 17 |
| 276 | data/results/c_attr_1112_score/res/COPYBOUND_xm_dev500_qwen25vl_7b.json | `bound.ii_words.n3.K_ret.d` | 13.225311524965774 | +13.23 | number | 06_results.md §6.10.6 Table 17 |
| 277 | data/results/c_attr_1112_score/res/COPYBOUND_xm_dev500_qwen25vl_7b.json | `bound.ii_words.n3.K_ret.lo` | 10.702924207714606 | 10.70 | number | 06_results.md §6.10.6 Table 17 |
| 278 | data/results/c_attr_1112_score/res/COPYBOUND_xm_dev500_qwen25vl_7b.json | `bound.ii_words.n3.K_ret.hi` | 15.955657728088893 | 15.96 | number | 06_results.md §6.10.6 Table 17 |
| 279 | data/results/c_attr_1112_score/res/COPYBOUND_xm_dev500_qwen25vl_7b.json | `bound.ii_words.n3.K_ret.label` | "DETECTED" | DETECTED | label | 06_results.md §6.10.6 Table 17 |
| 280 | data/results/c_attr_1112_score/res/COPYBOUND_xm_dev500_qwen25vl_7b.json | `bound.ii_words.n3.L_cp.d` | -8.784812206391813 | −8.78 | number | 06_results.md §6.10.6 Table 17 |
| 281 | data/results/c_attr_1112_score/res/COPYBOUND_xm_dev500_qwen25vl_7b.json | `bound.ii_words.n3.L_cp.lo` | -12.874638721484633 | −12.87 | number | 06_results.md §6.10.6 Table 17 |
| 282 | data/results/c_attr_1112_score/res/COPYBOUND_xm_dev500_qwen25vl_7b.json | `bound.ii_words.n3.L_cp.hi` | -4.726277337968858 | −4.73 | number | 06_results.md §6.10.6 Table 17 |
| 283 | data/results/c_attr_1112_score/res/COPYBOUND_xm_dev500_qwen25vl_7b.json | `bound.ii_words.n3.L_cp.label` | "REVERSED" | REVERSED | label | 06_results.md §6.10.6 Table 17 |
| 284 | data/results/c_attr_1112_score/res/COPYBOUND_xm_dev500_qwen25vl_7b.json | `bound.ii_words.n3.K_nc.d` | 7.065209177258651 | +7.07 | number | 06_results.md §6.10.6 Table 17 |
| 285 | data/results/c_attr_1112_score/res/COPYBOUND_xm_dev500_qwen25vl_7b.json | `bound.ii_words.n3.K_nc.lo` | 5.121710989146588 | 5.12 | number | 06_results.md §6.10.6 Table 17 |
| 286 | data/results/c_attr_1112_score/res/COPYBOUND_xm_dev500_qwen25vl_7b.json | `bound.ii_words.n3.K_nc.hi` | 9.120985958646356 | 9.12 | number | 06_results.md §6.10.6 Table 17 |
| 287 | data/results/c_attr_1112_score/res/COPYBOUND_xm_dev500_qwen25vl_7b.json | `bound.ii_words.n3.K_nc.label` | "DETECTED" | DETECTED | label | 06_results.md §6.10.6 Table 17 |
| 288 | data/results/c_attr_1112_score/res/COPYBOUND_xm_dev500_internvl3_8b.json | `bound.i_syllables.n3.withdrawn` | false | in force | label | 06_results.md §6.10.6 Table 17 |
| 289 | data/results/c_attr_1112_score/res/COPYBOUND_xm_dev500_internvl3_8b.json | `bound.i_syllables.monotonicity check failed` | false | – | label | 06_results.md §6.10.6 Table 17 |
| 290 | data/results/c_attr_1112_score/res/COPYBOUND_xm_dev500_internvl3_8b.json | `bound.i_syllables.n3.K_ret.d` | 6.365504336354737 | +6.37 | number | 06_results.md §6.10.6 Table 17 |
| 291 | data/results/c_attr_1112_score/res/COPYBOUND_xm_dev500_internvl3_8b.json | `bound.i_syllables.n3.K_ret.lo` | 4.3486890920937915 | 4.35 | number | 06_results.md §6.10.6 Table 17 |
| 292 | data/results/c_attr_1112_score/res/COPYBOUND_xm_dev500_internvl3_8b.json | `bound.i_syllables.n3.K_ret.hi` | 8.588429420226277 | 8.59 | number | 06_results.md §6.10.6 Table 17 |
| 293 | data/results/c_attr_1112_score/res/COPYBOUND_xm_dev500_internvl3_8b.json | `bound.i_syllables.n3.K_ret.label` | "DETECTED" | DETECTED | label | 06_results.md §6.10.6 Table 17 |
| 294 | data/results/c_attr_1112_score/res/COPYBOUND_xm_dev500_internvl3_8b.json | `bound.i_syllables.n3.L_cp.d` | -4.824963268680341 | −4.82 | number | 06_results.md §6.10.6 Table 17 |
| 295 | data/results/c_attr_1112_score/res/COPYBOUND_xm_dev500_internvl3_8b.json | `bound.i_syllables.n3.L_cp.lo` | -8.721365769963858 | −8.72 | number | 06_results.md §6.10.6 Table 17 |
| 296 | data/results/c_attr_1112_score/res/COPYBOUND_xm_dev500_internvl3_8b.json | `bound.i_syllables.n3.L_cp.hi` | -1.0966026692992596 | −1.10 | number | 06_results.md §6.10.6 Table 17 |
| 297 | data/results/c_attr_1112_score/res/COPYBOUND_xm_dev500_internvl3_8b.json | `bound.i_syllables.n3.L_cp.label` | "REVERSED" | REVERSED | label | 06_results.md §6.10.6 Table 17 |
| 298 | data/results/c_attr_1112_score/res/COPYBOUND_xm_dev500_internvl3_8b.json | `bound.i_syllables.n3.K_nc.d` | 4.273893751222864 | +4.27 | number | 06_results.md §6.10.6 Table 17 |
| 299 | data/results/c_attr_1112_score/res/COPYBOUND_xm_dev500_internvl3_8b.json | `bound.i_syllables.n3.K_nc.lo` | 2.248201760049327 | 2.25 | number | 06_results.md §6.10.6 Table 17 |
| 300 | data/results/c_attr_1112_score/res/COPYBOUND_xm_dev500_internvl3_8b.json | `bound.i_syllables.n3.K_nc.hi` | 6.485958306410675 | 6.49 | number | 06_results.md §6.10.6 Table 17 |
| 301 | data/results/c_attr_1112_score/res/COPYBOUND_xm_dev500_internvl3_8b.json | `bound.i_syllables.n3.K_nc.label` | "DETECTED" | DETECTED | label | 06_results.md §6.10.6 Table 17 |
| 302 | data/results/c_attr_1112_score/res/COPYBOUND_xm_dev500_internvl3_8b.json | `bound.ii_words.n3.withdrawn` | false | in force | label | 06_results.md §6.10.6 Table 17 |
| 303 | data/results/c_attr_1112_score/res/COPYBOUND_xm_dev500_internvl3_8b.json | `bound.ii_words.monotonicity check failed` | false | – | label | 06_results.md §6.10.6 Table 17 |
| 304 | data/results/c_attr_1112_score/res/COPYBOUND_xm_dev500_internvl3_8b.json | `bound.ii_words.n3.K_ret.d` | 4.919111123751006 | +4.92 | number | 06_results.md §6.10.6 Table 17 |
| 305 | data/results/c_attr_1112_score/res/COPYBOUND_xm_dev500_internvl3_8b.json | `bound.ii_words.n3.K_ret.lo` | 3.3659999362587487 | 3.37 | number | 06_results.md §6.10.6 Table 17 |
| 306 | data/results/c_attr_1112_score/res/COPYBOUND_xm_dev500_internvl3_8b.json | `bound.ii_words.n3.K_ret.hi` | 6.648879470932601 | 6.65 | number | 06_results.md §6.10.6 Table 17 |
| 307 | data/results/c_attr_1112_score/res/COPYBOUND_xm_dev500_internvl3_8b.json | `bound.ii_words.n3.K_ret.label` | "DETECTED" | DETECTED | label | 06_results.md §6.10.6 Table 17 |
| 308 | data/results/c_attr_1112_score/res/COPYBOUND_xm_dev500_internvl3_8b.json | `bound.ii_words.n3.L_cp.d` | -3.3785700560766108 | −3.38 | number | 06_results.md §6.10.6 Table 17 |
| 309 | data/results/c_attr_1112_score/res/COPYBOUND_xm_dev500_internvl3_8b.json | `bound.ii_words.n3.L_cp.lo` | -7.17070945510841 | −7.17 | number | 06_results.md §6.10.6 Table 17 |
| 310 | data/results/c_attr_1112_score/res/COPYBOUND_xm_dev500_internvl3_8b.json | `bound.ii_words.n3.L_cp.hi` | 0.2811291763762643 | 0.28 | number | 06_results.md §6.10.6 Table 17 |
| 311 | data/results/c_attr_1112_score/res/COPYBOUND_xm_dev500_internvl3_8b.json | `bound.ii_words.n3.L_cp.label` | "UNRESOLVED" | UNRESOLVED | label | 06_results.md §6.10.6 Table 17 |
| 312 | data/results/c_attr_1112_score/res/COPYBOUND_xm_dev500_internvl3_8b.json | `bound.ii_words.n3.K_nc.d` | 3.328526357577078 | +3.33 | number | 06_results.md §6.10.6 Table 17 |
| 313 | data/results/c_attr_1112_score/res/COPYBOUND_xm_dev500_internvl3_8b.json | `bound.ii_words.n3.K_nc.lo` | 1.8097687375483216 | 1.81 | number | 06_results.md §6.10.6 Table 17 |
| 314 | data/results/c_attr_1112_score/res/COPYBOUND_xm_dev500_internvl3_8b.json | `bound.ii_words.n3.K_nc.hi` | 5.068607219547311 | 5.07 | number | 06_results.md §6.10.6 Table 17 |
| 315 | data/results/c_attr_1112_score/res/COPYBOUND_xm_dev500_internvl3_8b.json | `bound.ii_words.n3.K_nc.label` | "DETECTED" | DETECTED | label | 06_results.md §6.10.6 Table 17 |
| 316 | data/results/c_attr_1112_score/res/COPYBOUND_xm_dev500_aya_vision_8b.json | `bound.i_syllables.n3.withdrawn` | false | in force | label | 06_results.md §6.10.6 Table 17 |
| 317 | data/results/c_attr_1112_score/res/COPYBOUND_xm_dev500_aya_vision_8b.json | `bound.i_syllables.monotonicity check failed` | false | – | label | 06_results.md §6.10.6 Table 17 |
| 318 | data/results/c_attr_1112_score/res/COPYBOUND_xm_dev500_aya_vision_8b.json | `bound.i_syllables.n3.K_ret.d` | 7.18214796770334 | +7.18 | number | 06_results.md §6.10.6 Table 17 |
| 319 | data/results/c_attr_1112_score/res/COPYBOUND_xm_dev500_aya_vision_8b.json | `bound.i_syllables.n3.K_ret.lo` | 5.347825637875918 | 5.35 | number | 06_results.md §6.10.6 Table 17 |
| 320 | data/results/c_attr_1112_score/res/COPYBOUND_xm_dev500_aya_vision_8b.json | `bound.i_syllables.n3.K_ret.hi` | 8.979910563316842 | 8.98 | number | 06_results.md §6.10.6 Table 17 |
| 321 | data/results/c_attr_1112_score/res/COPYBOUND_xm_dev500_aya_vision_8b.json | `bound.i_syllables.n3.K_ret.label` | "DETECTED" | DETECTED | label | 06_results.md §6.10.6 Table 17 |
| 322 | data/results/c_attr_1112_score/res/COPYBOUND_xm_dev500_aya_vision_8b.json | `bound.i_syllables.n3.L_cp.d` | -6.363300549838219 | −6.36 | number | 06_results.md §6.10.6 Table 17 |
| 323 | data/results/c_attr_1112_score/res/COPYBOUND_xm_dev500_aya_vision_8b.json | `bound.i_syllables.n3.L_cp.lo` | -10.106843487585213 | −10.11 | number | 06_results.md §6.10.6 Table 17 |
| 324 | data/results/c_attr_1112_score/res/COPYBOUND_xm_dev500_aya_vision_8b.json | `bound.i_syllables.n3.L_cp.hi` | -3.015405324741291 | −3.02 | number | 06_results.md §6.10.6 Table 17 |
| 325 | data/results/c_attr_1112_score/res/COPYBOUND_xm_dev500_aya_vision_8b.json | `bound.i_syllables.n3.L_cp.label` | "REVERSED" | REVERSED | label | 06_results.md §6.10.6 Table 17 |
| 326 | data/results/c_attr_1112_score/res/COPYBOUND_xm_dev500_aya_vision_8b.json | `bound.i_syllables.n3.K_nc.d` | 4.997852712409303 | +5.00 | number | 06_results.md §6.10.6 Table 17 |
| 327 | data/results/c_attr_1112_score/res/COPYBOUND_xm_dev500_aya_vision_8b.json | `bound.i_syllables.n3.K_nc.lo` | 3.473389177704702 | 3.47 | number | 06_results.md §6.10.6 Table 17 |
| 328 | data/results/c_attr_1112_score/res/COPYBOUND_xm_dev500_aya_vision_8b.json | `bound.i_syllables.n3.K_nc.hi` | 6.725281087653715 | 6.73 | number | 06_results.md §6.10.6 Table 17 |
| 329 | data/results/c_attr_1112_score/res/COPYBOUND_xm_dev500_aya_vision_8b.json | `bound.i_syllables.n3.K_nc.label` | "DETECTED" | DETECTED | label | 06_results.md §6.10.6 Table 17 |
| 330 | data/results/c_attr_1112_score/res/COPYBOUND_xm_dev500_aya_vision_8b.json | `bound.ii_words.n3.withdrawn` | false | in force | label | 06_results.md §6.10.6 Table 17 |
| 331 | data/results/c_attr_1112_score/res/COPYBOUND_xm_dev500_aya_vision_8b.json | `bound.ii_words.monotonicity check failed` | false | – | label | 06_results.md §6.10.6 Table 17 |
| 332 | data/results/c_attr_1112_score/res/COPYBOUND_xm_dev500_aya_vision_8b.json | `bound.ii_words.n3.K_ret.d` | 5.69235564018542 | +5.69 | number | 06_results.md §6.10.6 Table 17 |
| 333 | data/results/c_attr_1112_score/res/COPYBOUND_xm_dev500_aya_vision_8b.json | `bound.ii_words.n3.K_ret.lo` | 4.033461631205525 | 4.03 | number | 06_results.md §6.10.6 Table 17 |
| 334 | data/results/c_attr_1112_score/res/COPYBOUND_xm_dev500_aya_vision_8b.json | `bound.ii_words.n3.K_ret.hi` | 7.449728473624756 | 7.45 | number | 06_results.md §6.10.6 Table 17 |
| 335 | data/results/c_attr_1112_score/res/COPYBOUND_xm_dev500_aya_vision_8b.json | `bound.ii_words.n3.K_ret.label` | "DETECTED" | DETECTED | label | 06_results.md §6.10.6 Table 17 |
| 336 | data/results/c_attr_1112_score/res/COPYBOUND_xm_dev500_aya_vision_8b.json | `bound.ii_words.n3.L_cp.d` | -4.8735082223203 | −4.87 | number | 06_results.md §6.10.6 Table 17 |
| 337 | data/results/c_attr_1112_score/res/COPYBOUND_xm_dev500_aya_vision_8b.json | `bound.ii_words.n3.L_cp.lo` | -8.612374737950532 | −8.61 | number | 06_results.md §6.10.6 Table 17 |
| 338 | data/results/c_attr_1112_score/res/COPYBOUND_xm_dev500_aya_vision_8b.json | `bound.ii_words.n3.L_cp.hi` | -1.5062229898819266 | −1.51 | number | 06_results.md §6.10.6 Table 17 |
| 339 | data/results/c_attr_1112_score/res/COPYBOUND_xm_dev500_aya_vision_8b.json | `bound.ii_words.n3.L_cp.label` | "REVERSED" | REVERSED | label | 06_results.md §6.10.6 Table 17 |
| 340 | data/results/c_attr_1112_score/res/COPYBOUND_xm_dev500_aya_vision_8b.json | `bound.ii_words.n3.K_nc.d` | 4.091567756359667 | +4.09 | number | 06_results.md §6.10.6 Table 17 |
| 341 | data/results/c_attr_1112_score/res/COPYBOUND_xm_dev500_aya_vision_8b.json | `bound.ii_words.n3.K_nc.lo` | 2.663845967648181 | 2.66 | number | 06_results.md §6.10.6 Table 17 |
| 342 | data/results/c_attr_1112_score/res/COPYBOUND_xm_dev500_aya_vision_8b.json | `bound.ii_words.n3.K_nc.hi` | 5.725164499160832 | 5.73 | number | 06_results.md §6.10.6 Table 17 |
| 343 | data/results/c_attr_1112_score/res/COPYBOUND_xm_dev500_aya_vision_8b.json | `bound.ii_words.n3.K_nc.label` | "DETECTED" | DETECTED | label | 06_results.md §6.10.6 Table 17 |
| 344 | data/results/c_attr_1112_score/res/COPYBOUND_ov_dev_b_qwen25vl_7b.json | `bound.i_syllables.n3.L_cp.d` | -8.914878699583078 | −8.91 | number | 06_results.md §6.10.6 |
| 345 | data/results/c_attr_1112_score/res/COPYBOUND_ov_dev_b_qwen25vl_7b.json | `bound.i_syllables.n3.L_cp.lo` | -10.707668881201924 | −10.71 | number | 06_results.md §6.10.6 |
| 346 | data/results/c_attr_1112_score/res/COPYBOUND_ov_dev_b_qwen25vl_7b.json | `bound.i_syllables.n3.L_cp.hi` | -7.06586722529071 | −7.07 | number | 06_results.md §6.10.6 |
| 347 | data/results/c_attr_1112_score/res/COPYBOUND_ov_dev_b_qwen25vl_7b.json | `bound.ii_words.n3.L_cp.d` | -9.075132208536466 | −9.08 | number | 06_results.md §6.10.6 |
| 348 | data/results/c_attr_1112_score/res/COPYBOUND_ov_dev_b_qwen25vl_7b.json | `bound.ii_words.n3.L_cp.lo` | -10.981918956274114 | −10.98 | number | 06_results.md §6.10.6 |
| 349 | data/results/c_attr_1112_score/res/COPYBOUND_ov_dev_b_qwen25vl_7b.json | `bound.ii_words.n3.L_cp.hi` | -7.218559968005788 | −7.22 | number | 06_results.md §6.10.6 |
| 350 | data/results/c_attr_1112_score/res/COPYBOUND_ov_dev_b_internvl3_8b.json | `bound.i_syllables.n3.L_cp.d` | -4.573759735321315 | −4.57 | number | 06_results.md §6.10.6 |
| 351 | data/results/c_attr_1112_score/res/COPYBOUND_ov_dev_b_internvl3_8b.json | `bound.i_syllables.n3.L_cp.lo` | -6.4621888546336175 | −6.46 | number | 06_results.md §6.10.6 |
| 352 | data/results/c_attr_1112_score/res/COPYBOUND_ov_dev_b_internvl3_8b.json | `bound.i_syllables.n3.L_cp.hi` | -2.611113435330269 | −2.61 | number | 06_results.md §6.10.6 |
| 353 | data/results/c_attr_1112_score/res/COPYBOUND_ov_dev_b_internvl3_8b.json | `bound.ii_words.n3.L_cp.d` | -3.6363443868694802 | −3.64 | number | 06_results.md §6.10.6 |
| 354 | data/results/c_attr_1112_score/res/COPYBOUND_ov_dev_b_internvl3_8b.json | `bound.ii_words.n3.L_cp.lo` | -5.550854071186638 | −5.55 | number | 06_results.md §6.10.6 |
| 355 | data/results/c_attr_1112_score/res/COPYBOUND_ov_dev_b_internvl3_8b.json | `bound.ii_words.n3.L_cp.hi` | -1.6886715001354877 | −1.69 | number | 06_results.md §6.10.6 |
| 356 | data/results/c_attr_1112_score/res/COPYBOUND_ov_dev_b_aya_vision_8b.json | `bound.i_syllables.n3.L_cp.d` | -1.7019866073755456 | −1.70 | number | 06_results.md §6.10.6 |
| 357 | data/results/c_attr_1112_score/res/COPYBOUND_ov_dev_b_aya_vision_8b.json | `bound.i_syllables.n3.L_cp.lo` | -3.2767966252914245 | −3.28 | number | 06_results.md §6.10.6 |
| 358 | data/results/c_attr_1112_score/res/COPYBOUND_ov_dev_b_aya_vision_8b.json | `bound.i_syllables.n3.L_cp.hi` | -0.13369643074849094 | −0.13 | number | 06_results.md §6.10.6 |
| 359 | data/results/c_attr_1112_score/res/COPYBOUND_ov_dev_b_aya_vision_8b.json | `bound.ii_words.n3.L_cp.d` | -0.5660514483250949 | −0.57 | number | 06_results.md §6.10.6 |
| 360 | data/results/c_attr_1112_score/res/COPYBOUND_ov_dev_b_aya_vision_8b.json | `bound.ii_words.n3.L_cp.lo` | -2.163585953345003 | −2.16 | number | 06_results.md §6.10.6 |
| 361 | data/results/c_attr_1112_score/res/COPYBOUND_ov_dev_b_aya_vision_8b.json | `bound.ii_words.n3.L_cp.hi` | 0.9943073192522447 | 0.99 | number | 06_results.md §6.10.6 |
| 362 | data/results/c_attr_1112_score/res/COPYBOUND_xm_dev500_qwen25vl_7b.json | `bound.i_syllables.n3.L_cp.d` | -9.810331287465733 | −9.81 | number | 06_results.md §6.10.6 |
| 363 | data/results/c_attr_1112_score/res/COPYBOUND_xm_dev500_qwen25vl_7b.json | `bound.i_syllables.n3.L_cp.lo` | -13.665674727804914 | −13.67 | number | 06_results.md §6.10.6 |
| 364 | data/results/c_attr_1112_score/res/COPYBOUND_xm_dev500_qwen25vl_7b.json | `bound.i_syllables.n3.L_cp.hi` | -5.626911363695306 | −5.63 | number | 06_results.md §6.10.6 |
| 365 | data/results/c_attr_1112_score/res/COPYBOUND_xm_dev500_qwen25vl_7b.json | `bound.ii_words.n3.L_cp.d` | -8.784812206391813 | −8.78 | number | 06_results.md §6.10.6 |
| 366 | data/results/c_attr_1112_score/res/COPYBOUND_xm_dev500_qwen25vl_7b.json | `bound.ii_words.n3.L_cp.lo` | -12.874638721484633 | −12.87 | number | 06_results.md §6.10.6 |
| 367 | data/results/c_attr_1112_score/res/COPYBOUND_xm_dev500_qwen25vl_7b.json | `bound.ii_words.n3.L_cp.hi` | -4.726277337968858 | −4.73 | number | 06_results.md §6.10.6 |
| 368 | data/results/c_attr_1112_score/res/COPYBOUND_xm_dev500_internvl3_8b.json | `bound.i_syllables.n3.L_cp.d` | -4.824963268680341 | −4.82 | number | 06_results.md §6.10.6 |
| 369 | data/results/c_attr_1112_score/res/COPYBOUND_xm_dev500_internvl3_8b.json | `bound.i_syllables.n3.L_cp.lo` | -8.721365769963858 | −8.72 | number | 06_results.md §6.10.6 |
| 370 | data/results/c_attr_1112_score/res/COPYBOUND_xm_dev500_internvl3_8b.json | `bound.i_syllables.n3.L_cp.hi` | -1.0966026692992596 | −1.10 | number | 06_results.md §6.10.6 |
| 371 | data/results/c_attr_1112_score/res/COPYBOUND_xm_dev500_internvl3_8b.json | `bound.ii_words.n3.L_cp.d` | -3.3785700560766108 | −3.38 | number | 06_results.md §6.10.6 |
| 372 | data/results/c_attr_1112_score/res/COPYBOUND_xm_dev500_internvl3_8b.json | `bound.ii_words.n3.L_cp.lo` | -7.17070945510841 | −7.17 | number | 06_results.md §6.10.6 |
| 373 | data/results/c_attr_1112_score/res/COPYBOUND_xm_dev500_internvl3_8b.json | `bound.ii_words.n3.L_cp.hi` | 0.2811291763762643 | 0.28 | number | 06_results.md §6.10.6 |
| 374 | data/results/c_attr_1112_score/res/COPYBOUND_xm_dev500_aya_vision_8b.json | `bound.i_syllables.n3.L_cp.d` | -6.363300549838219 | −6.36 | number | 06_results.md §6.10.6 |
| 375 | data/results/c_attr_1112_score/res/COPYBOUND_xm_dev500_aya_vision_8b.json | `bound.i_syllables.n3.L_cp.lo` | -10.106843487585213 | −10.11 | number | 06_results.md §6.10.6 |
| 376 | data/results/c_attr_1112_score/res/COPYBOUND_xm_dev500_aya_vision_8b.json | `bound.i_syllables.n3.L_cp.hi` | -3.015405324741291 | −3.02 | number | 06_results.md §6.10.6 |
| 377 | data/results/c_attr_1112_score/res/COPYBOUND_xm_dev500_aya_vision_8b.json | `bound.ii_words.n3.L_cp.d` | -4.8735082223203 | −4.87 | number | 06_results.md §6.10.6 |
| 378 | data/results/c_attr_1112_score/res/COPYBOUND_xm_dev500_aya_vision_8b.json | `bound.ii_words.n3.L_cp.lo` | -8.612374737950532 | −8.61 | number | 06_results.md §6.10.6 |
| 379 | data/results/c_attr_1112_score/res/COPYBOUND_xm_dev500_aya_vision_8b.json | `bound.ii_words.n3.L_cp.hi` | -1.5062229898819266 | −1.51 | number | 06_results.md §6.10.6 |
| 380 | data/results/c_attr_1112_score/res/POSTHOC.json | `swap.length` | {} | NOT RUN (rule L) | text | 06_results.md §6.10.6 (last paragraph); Table S25b |
| 381 | data/results/c_attr_1112_score/res/POSTHOC.json | `swap.rows.qwen25vl_7b.delta.d` | -5.436874500000001 | −5.44 | number | 06_results.md §6.10.6 (last paragraph); Table S25b |
| 382 | data/results/c_attr_1112_score/res/POSTHOC.json | `swap.rows.qwen25vl_7b.delta.lo` | -9.0747935025 | −9.07 | number | 06_results.md §6.10.6 (last paragraph); Table S25b |
| 383 | data/results/c_attr_1112_score/res/POSTHOC.json | `swap.rows.qwen25vl_7b.delta.hi` | -2.0357453625000015 | −2.04 | number | 06_results.md §6.10.6 (last paragraph); Table S25b |
| 384 | data/results/c_attr_1112_score/res/POSTHOC.json | `swap.rows.qwen25vl_7b.delta.label` | "REVERSED" | REVERSED | label | 06_results.md §6.10.6 (last paragraph); Table S25b |
| 385 | data/results/c_attr_1112_score/res/POSTHOC.json | `swap.rows.aya_vision_8b.delta.d` | -0.009911199999999454 | −0.01 | number | 06_results.md §6.10.6 (last paragraph); Table S25b |
| 386 | data/results/c_attr_1112_score/res/POSTHOC.json | `swap.rows.aya_vision_8b.delta.lo` | -3.4165317724999995 | −3.42 | number | 06_results.md §6.10.6 (last paragraph); Table S25b |
| 387 | data/results/c_attr_1112_score/res/POSTHOC.json | `swap.rows.aya_vision_8b.delta.hi` | 3.3571946975000024 | 3.36 | number | 06_results.md §6.10.6 (last paragraph); Table S25b |
| 388 | data/results/c_attr_1112_score/res/POSTHOC.json | `swap.rows.aya_vision_8b.delta.label` | "UNRESOLVED" | UNRESOLVED | label | 06_results.md §6.10.6 (last paragraph); Table S25b |
| 389 | data/results/c_attr_1112_score/res/c_attr_nomination.json | `rows.qwen25vl_7b~tau_pair.label` | "DETECTED" | DETECTED | label | 11_supplement_registered_rows.md (nomination-file labels) |
| 390 | data/results/c_attr_1112_score/res/c_attr_nomination.json | `rows.qwen25vl_7b~tau_marg.label` | "NEGLIGIBLE" | NEGLIGIBLE | label | 11_supplement_registered_rows.md (nomination-file labels) |
| 391 | data/results/c_attr_1112_score/res/c_attr_nomination.json | `rows.qwen25vl_7b~tau_sel.label` | "DETECTED" | DETECTED | label | 11_supplement_registered_rows.md (nomination-file labels) |
| 392 | data/results/c_attr_1112_score/res/c_attr_nomination.json | `rows.internvl3_8b~tau_pair.label` | "DETECTED" | DETECTED | label | 11_supplement_registered_rows.md (nomination-file labels) |
| 393 | data/results/c_attr_1112_score/res/c_attr_nomination.json | `rows.internvl3_8b~tau_marg.label` | "REVERSED" | REVERSED | label | 11_supplement_registered_rows.md (nomination-file labels) |
| 394 | data/results/c_attr_1112_score/res/c_attr_nomination.json | `rows.internvl3_8b~tau_sel.label` | "DETECTED" | DETECTED | label | 11_supplement_registered_rows.md (nomination-file labels) |
| 395 | data/results/c_attr_1112_score/res/SUMMARY.json | `sets.xm_dev500.rows.qwen25vl_7b~tau_any.d` | 12.139300933333331 | +12.14 | number | 11_supplement_registered_rows.md Table S21 |
| 396 | data/results/c_attr_1112_score/res/SUMMARY.json | `sets.xm_dev500.rows.qwen25vl_7b~tau_any.lo` | 8.857540251666665 | 8.86 | number | 11_supplement_registered_rows.md Table S21 |
| 397 | data/results/c_attr_1112_score/res/SUMMARY.json | `sets.xm_dev500.rows.qwen25vl_7b~tau_any.hi` | 15.403969710000002 | 15.40 | number | 11_supplement_registered_rows.md Table S21 |
| 398 | data/results/c_attr_1112_score/res/SUMMARY.json | `sets.xm_dev500.rows.qwen25vl_7b~tau_any.label` | "DETECTED" | DETECTED | label | 11_supplement_registered_rows.md Table S21 |
| 399 | data/results/c_attr_1112_score/res/SUMMARY.json | `sets.xm_dev500.rows.qwen25vl_7b~tau_sel.d` | 1.7910556666666722 | +1.79 | number | 11_supplement_registered_rows.md Table S21 |
| 400 | data/results/c_attr_1112_score/res/SUMMARY.json | `sets.xm_dev500.rows.qwen25vl_7b~tau_sel.lo` | -1.2996083983333373 | −1.30 | number | 11_supplement_registered_rows.md Table S21 |
| 401 | data/results/c_attr_1112_score/res/SUMMARY.json | `sets.xm_dev500.rows.qwen25vl_7b~tau_sel.hi` | 4.948772919999983 | 4.95 | number | 11_supplement_registered_rows.md Table S21 |
| 402 | data/results/c_attr_1112_score/res/SUMMARY.json | `sets.xm_dev500.rows.qwen25vl_7b~tau_sel.label` | "UNRESOLVED" | UNRESOLVED | label | 11_supplement_registered_rows.md Table S21 |
| 403 | data/results/c_attr_1112_score/res/SUMMARY.json | `sets.xm_dev500.rows.qwen25vl_7b~tau_marg.d` | -0.8247758333333266 | −0.82 | number | 11_supplement_registered_rows.md Table S21 |
| 404 | data/results/c_attr_1112_score/res/SUMMARY.json | `sets.xm_dev500.rows.qwen25vl_7b~tau_marg.lo` | -2.9193811841666633 | −2.92 | number | 11_supplement_registered_rows.md Table S21 |
| 405 | data/results/c_attr_1112_score/res/SUMMARY.json | `sets.xm_dev500.rows.qwen25vl_7b~tau_marg.hi` | 1.2096976416666505 | 1.21 | number | 11_supplement_registered_rows.md Table S21 |
| 406 | data/results/c_attr_1112_score/res/SUMMARY.json | `sets.xm_dev500.rows.qwen25vl_7b~tau_marg.label` | "UNRESOLVED" | UNRESOLVED | label | 11_supplement_registered_rows.md Table S21 |
| 407 | data/results/c_attr_1112_score/res/SUMMARY.json | `sets.xm_dev500.rows.qwen25vl_7b~tau_pair.d` | 2.6158314999999988 | +2.62 | number | 11_supplement_registered_rows.md Table S21 |
| 408 | data/results/c_attr_1112_score/res/SUMMARY.json | `sets.xm_dev500.rows.qwen25vl_7b~tau_pair.lo` | -0.7475234925000039 | −0.75 | number | 11_supplement_registered_rows.md Table S21 |
| 409 | data/results/c_attr_1112_score/res/SUMMARY.json | `sets.xm_dev500.rows.qwen25vl_7b~tau_pair.hi` | 6.103402162500004 | 6.10 | number | 11_supplement_registered_rows.md Table S21 |
| 410 | data/results/c_attr_1112_score/res/SUMMARY.json | `sets.xm_dev500.rows.qwen25vl_7b~tau_pair.label` | "UNRESOLVED" | UNRESOLVED | label | 11_supplement_registered_rows.md Table S21 |
| 411 | data/results/c_attr_1112_score/res/SUMMARY.json | `sets.xm_dev500.rows.qwen25vl_7b~placebo_d1_d2.flag` | false | not flagged | label | 11_supplement_registered_rows.md Table S21 |
| 412 | data/results/c_attr_1112_score/res/SUMMARY.json | `sets.xm_dev500.rows.qwen25vl_7b~placebo_d1_d2.d` | 3.210298999999999 | +3.21 | number | 11_supplement_registered_rows.md Table S21 |
| 413 | data/results/c_attr_1112_score/res/SUMMARY.json | `sets.xm_dev500.rows.qwen25vl_7b~placebo_d1_d2.lo` | -0.11569781999999974 | −0.12 | number | 11_supplement_registered_rows.md Table S21 |
| 414 | data/results/c_attr_1112_score/res/SUMMARY.json | `sets.xm_dev500.rows.qwen25vl_7b~placebo_d1_d2.hi` | 6.179432014999989 | 6.18 | number | 11_supplement_registered_rows.md Table S21 |
| 415 | data/results/c_attr_1112_score/res/SUMMARY.json | `sets.xm_dev500.rows.internvl3_8b~tau_any.d` | 13.772210400000006 | +13.77 | number | 11_supplement_registered_rows.md Table S21 |
| 416 | data/results/c_attr_1112_score/res/SUMMARY.json | `sets.xm_dev500.rows.internvl3_8b~tau_any.lo` | 10.333671345000003 | 10.33 | number | 11_supplement_registered_rows.md Table S21 |
| 417 | data/results/c_attr_1112_score/res/SUMMARY.json | `sets.xm_dev500.rows.internvl3_8b~tau_any.hi` | 17.316508696666663 | 17.32 | number | 11_supplement_registered_rows.md Table S21 |
| 418 | data/results/c_attr_1112_score/res/SUMMARY.json | `sets.xm_dev500.rows.internvl3_8b~tau_any.label` | "DETECTED" | DETECTED | label | 11_supplement_registered_rows.md Table S21 |
| 419 | data/results/c_attr_1112_score/res/SUMMARY.json | `sets.xm_dev500.rows.internvl3_8b~tau_sel.d` | 0.11156179999999694 | +0.11 | number | 11_supplement_registered_rows.md Table S21 |
| 420 | data/results/c_attr_1112_score/res/SUMMARY.json | `sets.xm_dev500.rows.internvl3_8b~tau_sel.lo` | -2.819838843333326 | −2.82 | number | 11_supplement_registered_rows.md Table S21 |
| 421 | data/results/c_attr_1112_score/res/SUMMARY.json | `sets.xm_dev500.rows.internvl3_8b~tau_sel.hi` | 3.30798066166666 | 3.31 | number | 11_supplement_registered_rows.md Table S21 |
| 422 | data/results/c_attr_1112_score/res/SUMMARY.json | `sets.xm_dev500.rows.internvl3_8b~tau_sel.label` | "UNRESOLVED" | UNRESOLVED | label | 11_supplement_registered_rows.md Table S21 |
| 423 | data/results/c_attr_1112_score/res/SUMMARY.json | `sets.xm_dev500.rows.internvl3_8b~tau_marg.d` | -1.0033102000000014 | −1.00 | number | 11_supplement_registered_rows.md Table S21 |
| 424 | data/results/c_attr_1112_score/res/SUMMARY.json | `sets.xm_dev500.rows.internvl3_8b~tau_marg.lo` | -3.165334103333323 | −3.17 | number | 11_supplement_registered_rows.md Table S21 |
| 425 | data/results/c_attr_1112_score/res/SUMMARY.json | `sets.xm_dev500.rows.internvl3_8b~tau_marg.hi` | 1.1809946883333402 | 1.18 | number | 11_supplement_registered_rows.md Table S21 |
| 426 | data/results/c_attr_1112_score/res/SUMMARY.json | `sets.xm_dev500.rows.internvl3_8b~tau_marg.label` | "UNRESOLVED" | UNRESOLVED | label | 11_supplement_registered_rows.md Table S21 |
| 427 | data/results/c_attr_1112_score/res/SUMMARY.json | `sets.xm_dev500.rows.internvl3_8b~tau_pair.d` | 1.1148719999999983 | +1.11 | number | 11_supplement_registered_rows.md Table S21 |
| 428 | data/results/c_attr_1112_score/res/SUMMARY.json | `sets.xm_dev500.rows.internvl3_8b~tau_pair.lo` | -1.966703380000008 | −1.97 | number | 11_supplement_registered_rows.md Table S21 |
| 429 | data/results/c_attr_1112_score/res/SUMMARY.json | `sets.xm_dev500.rows.internvl3_8b~tau_pair.hi` | 4.5199426225000074 | 4.52 | number | 11_supplement_registered_rows.md Table S21 |
| 430 | data/results/c_attr_1112_score/res/SUMMARY.json | `sets.xm_dev500.rows.internvl3_8b~tau_pair.label` | "UNRESOLVED" | UNRESOLVED | label | 11_supplement_registered_rows.md Table S21 |
| 431 | data/results/c_attr_1112_score/res/SUMMARY.json | `sets.xm_dev500.rows.internvl3_8b~placebo_d1_d2.flag` | false | not flagged | label | 11_supplement_registered_rows.md Table S21 |
| 432 | data/results/c_attr_1112_score/res/SUMMARY.json | `sets.xm_dev500.rows.internvl3_8b~placebo_d1_d2.d` | -1.489409000000009 | −1.49 | number | 11_supplement_registered_rows.md Table S21 |
| 433 | data/results/c_attr_1112_score/res/SUMMARY.json | `sets.xm_dev500.rows.internvl3_8b~placebo_d1_d2.lo` | -4.82888304000001 | −4.83 | number | 11_supplement_registered_rows.md Table S21 |
| 434 | data/results/c_attr_1112_score/res/SUMMARY.json | `sets.xm_dev500.rows.internvl3_8b~placebo_d1_d2.hi` | 1.7229946949999875 | 1.72 | number | 11_supplement_registered_rows.md Table S21 |
| 435 | data/results/c_attr_1112_score/res/SUMMARY.json | `sets.xm_dev500.rows.aya_vision_8b~tau_any.d` | 23.976445666666663 | +23.98 | number | 11_supplement_registered_rows.md Table S21 |
| 436 | data/results/c_attr_1112_score/res/SUMMARY.json | `sets.xm_dev500.rows.aya_vision_8b~tau_any.lo` | 20.42876399999999 | 20.43 | number | 11_supplement_registered_rows.md Table S21 |
| 437 | data/results/c_attr_1112_score/res/SUMMARY.json | `sets.xm_dev500.rows.aya_vision_8b~tau_any.hi` | 27.925260033333327 | 27.93 | number | 11_supplement_registered_rows.md Table S21 |
| 438 | data/results/c_attr_1112_score/res/SUMMARY.json | `sets.xm_dev500.rows.aya_vision_8b~tau_any.label` | "DETECTED" | DETECTED | label | 11_supplement_registered_rows.md Table S21 |
| 439 | data/results/c_attr_1112_score/res/SUMMARY.json | `sets.xm_dev500.rows.aya_vision_8b~tau_sel.d` | 1.736536733333331 | +1.74 | number | 11_supplement_registered_rows.md Table S21 |
| 440 | data/results/c_attr_1112_score/res/SUMMARY.json | `sets.xm_dev500.rows.aya_vision_8b~tau_sel.lo` | -1.0942328250000084 | −1.09 | number | 11_supplement_registered_rows.md Table S21 |
| 441 | data/results/c_attr_1112_score/res/SUMMARY.json | `sets.xm_dev500.rows.aya_vision_8b~tau_sel.hi` | 4.534435456666663 | 4.53 | number | 11_supplement_registered_rows.md Table S21 |
| 442 | data/results/c_attr_1112_score/res/SUMMARY.json | `sets.xm_dev500.rows.aya_vision_8b~tau_sel.label` | "UNRESOLVED" | UNRESOLVED | label | 11_supplement_registered_rows.md Table S21 |
| 443 | data/results/c_attr_1112_score/res/SUMMARY.json | `sets.xm_dev500.rows.aya_vision_8b~tau_marg.d` | -1.4180492666666638 | −1.42 | number | 11_supplement_registered_rows.md Table S21 |
| 444 | data/results/c_attr_1112_score/res/SUMMARY.json | `sets.xm_dev500.rows.aya_vision_8b~tau_marg.lo` | -3.5013785224999934 | −3.50 | number | 11_supplement_registered_rows.md Table S21 |
| 445 | data/results/c_attr_1112_score/res/SUMMARY.json | `sets.xm_dev500.rows.aya_vision_8b~tau_marg.hi` | 0.6225693866666722 | 0.62 | number | 11_supplement_registered_rows.md Table S21 |
| 446 | data/results/c_attr_1112_score/res/SUMMARY.json | `sets.xm_dev500.rows.aya_vision_8b~tau_marg.label` | "UNRESOLVED" | UNRESOLVED | label | 11_supplement_registered_rows.md Table S21 |
| 447 | data/results/c_attr_1112_score/res/SUMMARY.json | `sets.xm_dev500.rows.aya_vision_8b~tau_pair.d` | 3.154585999999995 | +3.15 | number | 11_supplement_registered_rows.md Table S21 |
| 448 | data/results/c_attr_1112_score/res/SUMMARY.json | `sets.xm_dev500.rows.aya_vision_8b~tau_pair.lo` | 0.05717991500000186 | 0.06 | number | 11_supplement_registered_rows.md Table S21 |
| 449 | data/results/c_attr_1112_score/res/SUMMARY.json | `sets.xm_dev500.rows.aya_vision_8b~tau_pair.hi` | 6.3649232 | 6.36 | number | 11_supplement_registered_rows.md Table S21 |
| 450 | data/results/c_attr_1112_score/res/SUMMARY.json | `sets.xm_dev500.rows.aya_vision_8b~tau_pair.label` | "DETECTED" | DETECTED | label | 11_supplement_registered_rows.md Table S21 |
| 451 | data/results/c_attr_1112_score/res/SUMMARY.json | `sets.xm_dev500.rows.aya_vision_8b~placebo_d1_d2.flag` | false | not flagged | label | 11_supplement_registered_rows.md Table S21 |
| 452 | data/results/c_attr_1112_score/res/SUMMARY.json | `sets.xm_dev500.rows.aya_vision_8b~placebo_d1_d2.d` | 0.8272496000000089 | +0.83 | number | 11_supplement_registered_rows.md Table S21 |
| 453 | data/results/c_attr_1112_score/res/SUMMARY.json | `sets.xm_dev500.rows.aya_vision_8b~placebo_d1_d2.lo` | -2.1603134249999965 | −2.16 | number | 11_supplement_registered_rows.md Table S21 |
| 454 | data/results/c_attr_1112_score/res/SUMMARY.json | `sets.xm_dev500.rows.aya_vision_8b~placebo_d1_d2.hi` | 3.848266890000001 | 3.85 | number | 11_supplement_registered_rows.md Table S21 |
| 455 | data/results/c_attr_1112_score/res/SUMMARY.json | `batched.ov_dev_a.rows.qwen25vl_7b~tau_sel.d` | 8.00362030735456 | +8.00 | number | 11_supplement_registered_rows.md Table S22 |
| 456 | data/results/c_attr_1112_score/res/SUMMARY.json | `batched.ov_dev_a.rows.qwen25vl_7b~tau_sel.lo` | 6.022939909440169 | 6.02 | number | 11_supplement_registered_rows.md Table S22 |
| 457 | data/results/c_attr_1112_score/res/SUMMARY.json | `batched.ov_dev_a.rows.qwen25vl_7b~tau_sel.hi` | 10.014891037321629 | 10.01 | number | 11_supplement_registered_rows.md Table S22 |
| 458 | data/results/c_attr_1112_score/res/SUMMARY.json | `batched.ov_dev_a.rows.qwen25vl_7b~tau_sel.label` | "DETECTED" | DETECTED | label | 11_supplement_registered_rows.md Table S22 |
| 459 | data/results/c_attr_1112_score/res/SUMMARY.json | `batched.ov_dev_a.rows.qwen25vl_7b~tau_marg.d` | 0.4180577387486295 | +0.42 | number | 11_supplement_registered_rows.md Table S22 |
| 460 | data/results/c_attr_1112_score/res/SUMMARY.json | `batched.ov_dev_a.rows.qwen25vl_7b~tau_marg.lo` | -0.7544120787596014 | −0.75 | number | 11_supplement_registered_rows.md Table S22 |
| 461 | data/results/c_attr_1112_score/res/SUMMARY.json | `batched.ov_dev_a.rows.qwen25vl_7b~tau_marg.hi` | 1.5785980557080161 | 1.58 | number | 11_supplement_registered_rows.md Table S22 |
| 462 | data/results/c_attr_1112_score/res/SUMMARY.json | `batched.ov_dev_a.rows.qwen25vl_7b~tau_marg.label` | "NEGLIGIBLE" | NEGLIGIBLE | label | 11_supplement_registered_rows.md Table S22 |
| 463 | data/results/c_attr_1112_score/res/SUMMARY.json | `batched.ov_dev_a.rows.qwen25vl_7b~tau_pair.d` | 7.58556256860593 | +7.59 | number | 11_supplement_registered_rows.md Table S22 |
| 464 | data/results/c_attr_1112_score/res/SUMMARY.json | `batched.ov_dev_a.rows.qwen25vl_7b~tau_pair.lo` | 5.791544732436897 | 5.79 | number | 11_supplement_registered_rows.md Table S22 |
| 465 | data/results/c_attr_1112_score/res/SUMMARY.json | `batched.ov_dev_a.rows.qwen25vl_7b~tau_pair.hi` | 9.357942457464324 | 9.36 | number | 11_supplement_registered_rows.md Table S22 |
| 466 | data/results/c_attr_1112_score/res/SUMMARY.json | `batched.ov_dev_a.rows.qwen25vl_7b~tau_pair.label` | "DETECTED" | DETECTED | label | 11_supplement_registered_rows.md Table S22 |
| 467 | data/results/c_attr_1112_score/res/SUMMARY.json | `batched.ov_dev_a.rows.qwen25vl_7b~tau_any.d` | 9.79646926454446 | +9.80 | number | 11_supplement_registered_rows.md Table S22 |
| 468 | data/results/c_attr_1112_score/res/SUMMARY.json | `batched.ov_dev_a.rows.qwen25vl_7b~tau_any.lo` | 8.157465 | 8.16 | number | 11_supplement_registered_rows.md Table S22 |
| 469 | data/results/c_attr_1112_score/res/SUMMARY.json | `batched.ov_dev_a.rows.qwen25vl_7b~tau_any.hi` | 11.352243191547744 | 11.35 | number | 11_supplement_registered_rows.md Table S22 |
| 470 | data/results/c_attr_1112_score/res/SUMMARY.json | `batched.ov_dev_a.rows.qwen25vl_7b~tau_any.label` | "DETECTED" | DETECTED | label | 11_supplement_registered_rows.md Table S22 |
| 471 | data/results/c_attr_1112_score/res/SUMMARY.json | `batched.ov_dev_a.rows.qwen25vl_7b~tau_sel.R` | 1 | 1 | number | 11_supplement_registered_rows.md Table S22 |
| 472 | data/results/c_attr_1112_score/res/SUMMARY.json | `batched.ov_dev_a.rows.qwen25vl_7b~tau_pair.D` | 2 | 2 | number | 11_supplement_registered_rows.md Table S22 |
| 473 | data/results/c_attr_1112_score/res/SUMMARY.json | `batched.ov_dev_a.rows.internvl3_8b~tau_sel.d` | 3.430180900109768 | +3.43 | number | 11_supplement_registered_rows.md Table S22 |
| 474 | data/results/c_attr_1112_score/res/SUMMARY.json | `batched.ov_dev_a.rows.internvl3_8b~tau_sel.lo` | 1.5946740806805726 | 1.59 | number | 11_supplement_registered_rows.md Table S22 |
| 475 | data/results/c_attr_1112_score/res/SUMMARY.json | `batched.ov_dev_a.rows.internvl3_8b~tau_sel.hi` | 5.2158990998902235 | 5.22 | number | 11_supplement_registered_rows.md Table S22 |
| 476 | data/results/c_attr_1112_score/res/SUMMARY.json | `batched.ov_dev_a.rows.internvl3_8b~tau_sel.label` | "DETECTED" | DETECTED | label | 11_supplement_registered_rows.md Table S22 |
| 477 | data/results/c_attr_1112_score/res/SUMMARY.json | `batched.ov_dev_a.rows.internvl3_8b~tau_marg.d` | -1.1529428649835296 | −1.15 | number | 11_supplement_registered_rows.md Table S22 |
| 478 | data/results/c_attr_1112_score/res/SUMMARY.json | `batched.ov_dev_a.rows.internvl3_8b~tau_marg.lo` | -2.497521070252473 | −2.50 | number | 11_supplement_registered_rows.md Table S22 |
| 479 | data/results/c_attr_1112_score/res/SUMMARY.json | `batched.ov_dev_a.rows.internvl3_8b~tau_marg.hi` | 0.2186403841931969 | 0.22 | number | 11_supplement_registered_rows.md Table S22 |
| 480 | data/results/c_attr_1112_score/res/SUMMARY.json | `batched.ov_dev_a.rows.internvl3_8b~tau_marg.label` | "UNRESOLVED" | UNRESOLVED | label | 11_supplement_registered_rows.md Table S22 |
| 481 | data/results/c_attr_1112_score/res/SUMMARY.json | `batched.ov_dev_a.rows.internvl3_8b~tau_pair.d` | 4.583123765093298 | +4.58 | number | 11_supplement_registered_rows.md Table S22 |
| 482 | data/results/c_attr_1112_score/res/SUMMARY.json | `batched.ov_dev_a.rows.internvl3_8b~tau_pair.lo` | 2.807797209110865 | 2.81 | number | 11_supplement_registered_rows.md Table S22 |
| 483 | data/results/c_attr_1112_score/res/SUMMARY.json | `batched.ov_dev_a.rows.internvl3_8b~tau_pair.hi` | 6.457820038419317 | 6.46 | number | 11_supplement_registered_rows.md Table S22 |
| 484 | data/results/c_attr_1112_score/res/SUMMARY.json | `batched.ov_dev_a.rows.internvl3_8b~tau_pair.label` | "DETECTED" | DETECTED | label | 11_supplement_registered_rows.md Table S22 |
| 485 | data/results/c_attr_1112_score/res/SUMMARY.json | `batched.ov_dev_a.rows.internvl3_8b~tau_any.d` | 10.464134138309547 | +10.46 | number | 11_supplement_registered_rows.md Table S22 |
| 486 | data/results/c_attr_1112_score/res/SUMMARY.json | `batched.ov_dev_a.rows.internvl3_8b~tau_any.lo` | 8.662399333150384 | 8.66 | number | 11_supplement_registered_rows.md Table S22 |
| 487 | data/results/c_attr_1112_score/res/SUMMARY.json | `batched.ov_dev_a.rows.internvl3_8b~tau_any.hi` | 12.156285979692646 | 12.16 | number | 11_supplement_registered_rows.md Table S22 |
| 488 | data/results/c_attr_1112_score/res/SUMMARY.json | `batched.ov_dev_a.rows.internvl3_8b~tau_any.label` | "DETECTED" | DETECTED | label | 11_supplement_registered_rows.md Table S22 |
| 489 | data/results/c_attr_1112_score/res/SUMMARY.json | `batched.ov_dev_a.rows.internvl3_8b~tau_sel.R` | 1 | 1 | number | 11_supplement_registered_rows.md Table S22 |
| 490 | data/results/c_attr_1112_score/res/SUMMARY.json | `batched.ov_dev_a.rows.internvl3_8b~tau_pair.D` | 2 | 2 | number | 11_supplement_registered_rows.md Table S22 |
| 491 | data/results/c_attr_1112_score/res/SUMMARY.json | `batched.ov_dev_b.rows.qwen25vl_7b~tau_sel.d` | 9.254956180180173 | +9.25 | number | 11_supplement_registered_rows.md Table S22 |
| 492 | data/results/c_attr_1112_score/res/SUMMARY.json | `batched.ov_dev_b.rows.qwen25vl_7b~tau_sel.lo` | 7.593054208108109 | 7.59 | number | 11_supplement_registered_rows.md Table S22 |
| 493 | data/results/c_attr_1112_score/res/SUMMARY.json | `batched.ov_dev_b.rows.qwen25vl_7b~tau_sel.hi` | 11.137056849549548 | 11.14 | number | 11_supplement_registered_rows.md Table S22 |
| 494 | data/results/c_attr_1112_score/res/SUMMARY.json | `batched.ov_dev_b.rows.qwen25vl_7b~tau_sel.label` | "DETECTED" | DETECTED | label | 11_supplement_registered_rows.md Table S22 |
| 495 | data/results/c_attr_1112_score/res/SUMMARY.json | `batched.ov_dev_b.rows.qwen25vl_7b~tau_marg.d` | 0.9321815855855888 | +0.93 | number | 11_supplement_registered_rows.md Table S22 |
| 496 | data/results/c_attr_1112_score/res/SUMMARY.json | `batched.ov_dev_b.rows.qwen25vl_7b~tau_marg.lo` | -0.035677390540543995 | −0.04 | number | 11_supplement_registered_rows.md Table S22 |
| 497 | data/results/c_attr_1112_score/res/SUMMARY.json | `batched.ov_dev_b.rows.qwen25vl_7b~tau_marg.hi` | 1.8640367981982022 | 1.86 | number | 11_supplement_registered_rows.md Table S22 |
| 498 | data/results/c_attr_1112_score/res/SUMMARY.json | `batched.ov_dev_b.rows.qwen25vl_7b~tau_marg.label` | "NEGLIGIBLE" | NEGLIGIBLE | label | 11_supplement_registered_rows.md Table S22 |
| 499 | data/results/c_attr_1112_score/res/SUMMARY.json | `batched.ov_dev_b.rows.qwen25vl_7b~tau_pair.d` | 8.322774594594584 | +8.32 | number | 11_supplement_registered_rows.md Table S22 |
| 500 | data/results/c_attr_1112_score/res/SUMMARY.json | `batched.ov_dev_b.rows.qwen25vl_7b~tau_pair.lo` | 6.53457363783784 | 6.53 | number | 11_supplement_registered_rows.md Table S22 |
| 501 | data/results/c_attr_1112_score/res/SUMMARY.json | `batched.ov_dev_b.rows.qwen25vl_7b~tau_pair.hi` | 10.193557644594595 | 10.19 | number | 11_supplement_registered_rows.md Table S22 |
| 502 | data/results/c_attr_1112_score/res/SUMMARY.json | `batched.ov_dev_b.rows.qwen25vl_7b~tau_pair.label` | "DETECTED" | DETECTED | label | 11_supplement_registered_rows.md Table S22 |
| 503 | data/results/c_attr_1112_score/res/SUMMARY.json | `batched.ov_dev_b.rows.qwen25vl_7b~tau_any.d` | 10.793769441441437 | +10.79 | number | 11_supplement_registered_rows.md Table S22 |
| 504 | data/results/c_attr_1112_score/res/SUMMARY.json | `batched.ov_dev_b.rows.qwen25vl_7b~tau_any.lo` | 9.35810744954955 | 9.36 | number | 11_supplement_registered_rows.md Table S22 |
| 505 | data/results/c_attr_1112_score/res/SUMMARY.json | `batched.ov_dev_b.rows.qwen25vl_7b~tau_any.hi` | 12.219814712612607 | 12.22 | number | 11_supplement_registered_rows.md Table S22 |
| 506 | data/results/c_attr_1112_score/res/SUMMARY.json | `batched.ov_dev_b.rows.qwen25vl_7b~tau_any.label` | "DETECTED" | DETECTED | label | 11_supplement_registered_rows.md Table S22 |
| 507 | data/results/c_attr_1112_score/res/SUMMARY.json | `batched.ov_dev_b.rows.qwen25vl_7b~tau_sel.R` | 3 | 3 | number | 11_supplement_registered_rows.md Table S22 |
| 508 | data/results/c_attr_1112_score/res/SUMMARY.json | `batched.ov_dev_b.rows.qwen25vl_7b~tau_pair.D` | 2 | 2 | number | 11_supplement_registered_rows.md Table S22 |
| 509 | data/results/c_attr_1112_score/res/SUMMARY.json | `batched.ov_dev_b.rows.internvl3_8b~tau_sel.d` | 5.190223135135128 | +5.19 | number | 11_supplement_registered_rows.md Table S22 |
| 510 | data/results/c_attr_1112_score/res/SUMMARY.json | `batched.ov_dev_b.rows.internvl3_8b~tau_sel.lo` | 3.6271519288288268 | 3.63 | number | 11_supplement_registered_rows.md Table S22 |
| 511 | data/results/c_attr_1112_score/res/SUMMARY.json | `batched.ov_dev_b.rows.internvl3_8b~tau_sel.hi` | 6.785967852252246 | 6.79 | number | 11_supplement_registered_rows.md Table S22 |
| 512 | data/results/c_attr_1112_score/res/SUMMARY.json | `batched.ov_dev_b.rows.internvl3_8b~tau_sel.label` | "DETECTED" | DETECTED | label | 11_supplement_registered_rows.md Table S22 |
| 513 | data/results/c_attr_1112_score/res/SUMMARY.json | `batched.ov_dev_b.rows.internvl3_8b~tau_marg.d` | -0.42506713513513716 | −0.43 | number | 11_supplement_registered_rows.md Table S22 |
| 514 | data/results/c_attr_1112_score/res/SUMMARY.json | `batched.ov_dev_b.rows.internvl3_8b~tau_marg.lo` | -1.4265870527027062 | −1.43 | number | 11_supplement_registered_rows.md Table S22 |
| 515 | data/results/c_attr_1112_score/res/SUMMARY.json | `batched.ov_dev_b.rows.internvl3_8b~tau_marg.hi` | 0.5934090450450458 | 0.59 | number | 11_supplement_registered_rows.md Table S22 |
| 516 | data/results/c_attr_1112_score/res/SUMMARY.json | `batched.ov_dev_b.rows.internvl3_8b~tau_marg.label` | "NEGLIGIBLE" | NEGLIGIBLE | label | 11_supplement_registered_rows.md Table S22 |
| 517 | data/results/c_attr_1112_score/res/SUMMARY.json | `batched.ov_dev_b.rows.internvl3_8b~tau_pair.d` | 5.615290270270265 | +5.62 | number | 11_supplement_registered_rows.md Table S22 |
| 518 | data/results/c_attr_1112_score/res/SUMMARY.json | `batched.ov_dev_b.rows.internvl3_8b~tau_pair.lo` | 4.047379408108112 | 4.05 | number | 11_supplement_registered_rows.md Table S22 |
| 519 | data/results/c_attr_1112_score/res/SUMMARY.json | `batched.ov_dev_b.rows.internvl3_8b~tau_pair.hi` | 7.2871582540540505 | 7.29 | number | 11_supplement_registered_rows.md Table S22 |
| 520 | data/results/c_attr_1112_score/res/SUMMARY.json | `batched.ov_dev_b.rows.internvl3_8b~tau_pair.label` | "DETECTED" | DETECTED | label | 11_supplement_registered_rows.md Table S22 |
| 521 | data/results/c_attr_1112_score/res/SUMMARY.json | `batched.ov_dev_b.rows.internvl3_8b~tau_any.d` | 10.079809189189191 | +10.08 | number | 11_supplement_registered_rows.md Table S22 |
| 522 | data/results/c_attr_1112_score/res/SUMMARY.json | `batched.ov_dev_b.rows.internvl3_8b~tau_any.lo` | 8.7278956972973 | 8.73 | number | 11_supplement_registered_rows.md Table S22 |
| 523 | data/results/c_attr_1112_score/res/SUMMARY.json | `batched.ov_dev_b.rows.internvl3_8b~tau_any.hi` | 11.395515301801801 | 11.40 | number | 11_supplement_registered_rows.md Table S22 |
| 524 | data/results/c_attr_1112_score/res/SUMMARY.json | `batched.ov_dev_b.rows.internvl3_8b~tau_any.label` | "DETECTED" | DETECTED | label | 11_supplement_registered_rows.md Table S22 |
| 525 | data/results/c_attr_1112_score/res/SUMMARY.json | `batched.ov_dev_b.rows.internvl3_8b~tau_sel.R` | 3 | 3 | number | 11_supplement_registered_rows.md Table S22 |
| 526 | data/results/c_attr_1112_score/res/SUMMARY.json | `batched.ov_dev_b.rows.internvl3_8b~tau_pair.D` | 2 | 2 | number | 11_supplement_registered_rows.md Table S22 |
| 527 | data/results/c_attr_1112_score/res/SUMMARY.json | `batched.ov_dev_b.rows.aya_vision_8b~tau_sel.d` | 6.780426018018019 | +6.78 | number | 11_supplement_registered_rows.md Table S22 |
| 528 | data/results/c_attr_1112_score/res/SUMMARY.json | `batched.ov_dev_b.rows.aya_vision_8b~tau_sel.lo` | 5.3320985180180145 | 5.33 | number | 11_supplement_registered_rows.md Table S22 |
| 529 | data/results/c_attr_1112_score/res/SUMMARY.json | `batched.ov_dev_b.rows.aya_vision_8b~tau_sel.hi` | 8.332504719819816 | 8.33 | number | 11_supplement_registered_rows.md Table S22 |
| 530 | data/results/c_attr_1112_score/res/SUMMARY.json | `batched.ov_dev_b.rows.aya_vision_8b~tau_sel.label` | "DETECTED" | DETECTED | label | 11_supplement_registered_rows.md Table S22 |
| 531 | data/results/c_attr_1112_score/res/SUMMARY.json | `batched.ov_dev_b.rows.aya_vision_8b~tau_marg.d` | -0.36108106306306453 | −0.36 | number | 11_supplement_registered_rows.md Table S22 |
| 532 | data/results/c_attr_1112_score/res/SUMMARY.json | `batched.ov_dev_b.rows.aya_vision_8b~tau_marg.lo` | -1.2550820527027042 | −1.26 | number | 11_supplement_registered_rows.md Table S22 |
| 533 | data/results/c_attr_1112_score/res/SUMMARY.json | `batched.ov_dev_b.rows.aya_vision_8b~tau_marg.hi` | 0.5968106216216174 | 0.60 | number | 11_supplement_registered_rows.md Table S22 |
| 534 | data/results/c_attr_1112_score/res/SUMMARY.json | `batched.ov_dev_b.rows.aya_vision_8b~tau_marg.label` | "NEGLIGIBLE" | NEGLIGIBLE | label | 11_supplement_registered_rows.md Table S22 |
| 535 | data/results/c_attr_1112_score/res/SUMMARY.json | `batched.ov_dev_b.rows.aya_vision_8b~tau_pair.d` | 7.141507081081084 | +7.14 | number | 11_supplement_registered_rows.md Table S22 |
| 536 | data/results/c_attr_1112_score/res/SUMMARY.json | `batched.ov_dev_b.rows.aya_vision_8b~tau_pair.lo` | 5.69306925405405 | 5.69 | number | 11_supplement_registered_rows.md Table S22 |
| 537 | data/results/c_attr_1112_score/res/SUMMARY.json | `batched.ov_dev_b.rows.aya_vision_8b~tau_pair.hi` | 8.686738902702704 | 8.69 | number | 11_supplement_registered_rows.md Table S22 |
| 538 | data/results/c_attr_1112_score/res/SUMMARY.json | `batched.ov_dev_b.rows.aya_vision_8b~tau_pair.label` | "DETECTED" | DETECTED | label | 11_supplement_registered_rows.md Table S22 |
| 539 | data/results/c_attr_1112_score/res/SUMMARY.json | `batched.ov_dev_b.rows.aya_vision_8b~tau_any.d` | 13.553595603603602 | +13.55 | number | 11_supplement_registered_rows.md Table S22 |
| 540 | data/results/c_attr_1112_score/res/SUMMARY.json | `batched.ov_dev_b.rows.aya_vision_8b~tau_any.lo` | 12.404495802702705 | 12.40 | number | 11_supplement_registered_rows.md Table S22 |
| 541 | data/results/c_attr_1112_score/res/SUMMARY.json | `batched.ov_dev_b.rows.aya_vision_8b~tau_any.hi` | 14.841590929729731 | 14.84 | number | 11_supplement_registered_rows.md Table S22 |
| 542 | data/results/c_attr_1112_score/res/SUMMARY.json | `batched.ov_dev_b.rows.aya_vision_8b~tau_any.label` | "DETECTED" | DETECTED | label | 11_supplement_registered_rows.md Table S22 |
| 543 | data/results/c_attr_1112_score/res/SUMMARY.json | `batched.ov_dev_b.rows.aya_vision_8b~tau_sel.R` | 3 | 3 | number | 11_supplement_registered_rows.md Table S22 |
| 544 | data/results/c_attr_1112_score/res/SUMMARY.json | `batched.ov_dev_b.rows.aya_vision_8b~tau_pair.D` | 2 | 2 | number | 11_supplement_registered_rows.md Table S22 |
| 545 | data/results/c_attr_1112_score/res/SUMMARY.json | `batched.xm_dev500.rows.qwen25vl_7b~tau_sel.d` | 2.681282599999996 | +2.68 | number | 11_supplement_registered_rows.md Table S22 |
| 546 | data/results/c_attr_1112_score/res/SUMMARY.json | `batched.xm_dev500.rows.qwen25vl_7b~tau_sel.lo` | -0.31365458333333773 | −0.31 | number | 11_supplement_registered_rows.md Table S22 |
| 547 | data/results/c_attr_1112_score/res/SUMMARY.json | `batched.xm_dev500.rows.qwen25vl_7b~tau_sel.hi` | 5.660119968333333 | 5.66 | number | 11_supplement_registered_rows.md Table S22 |
| 548 | data/results/c_attr_1112_score/res/SUMMARY.json | `batched.xm_dev500.rows.qwen25vl_7b~tau_sel.label` | "UNRESOLVED" | UNRESOLVED | label | 11_supplement_registered_rows.md Table S22 |
| 549 | data/results/c_attr_1112_score/res/SUMMARY.json | `batched.xm_dev500.rows.qwen25vl_7b~tau_marg.d` | -0.7514217999999957 | −0.75 | number | 11_supplement_registered_rows.md Table S22 |
| 550 | data/results/c_attr_1112_score/res/SUMMARY.json | `batched.xm_dev500.rows.qwen25vl_7b~tau_marg.lo` | -2.870455000833327 | −2.87 | number | 11_supplement_registered_rows.md Table S22 |
| 551 | data/results/c_attr_1112_score/res/SUMMARY.json | `batched.xm_dev500.rows.qwen25vl_7b~tau_marg.hi` | 1.3301116166666678 | 1.33 | number | 11_supplement_registered_rows.md Table S22 |
| 552 | data/results/c_attr_1112_score/res/SUMMARY.json | `batched.xm_dev500.rows.qwen25vl_7b~tau_marg.label` | "UNRESOLVED" | UNRESOLVED | label | 11_supplement_registered_rows.md Table S22 |
| 553 | data/results/c_attr_1112_score/res/SUMMARY.json | `batched.xm_dev500.rows.qwen25vl_7b~tau_pair.d` | 3.4327043999999916 | +3.43 | number | 11_supplement_registered_rows.md Table S22 |
| 554 | data/results/c_attr_1112_score/res/SUMMARY.json | `batched.xm_dev500.rows.qwen25vl_7b~tau_pair.lo` | 0.09094603000000083 | 0.09 | number | 11_supplement_registered_rows.md Table S22 |
| 555 | data/results/c_attr_1112_score/res/SUMMARY.json | `batched.xm_dev500.rows.qwen25vl_7b~tau_pair.hi` | 6.778745342499995 | 6.78 | number | 11_supplement_registered_rows.md Table S22 |
| 556 | data/results/c_attr_1112_score/res/SUMMARY.json | `batched.xm_dev500.rows.qwen25vl_7b~tau_pair.label` | "DETECTED" | DETECTED | label | 11_supplement_registered_rows.md Table S22 |
| 557 | data/results/c_attr_1112_score/res/SUMMARY.json | `batched.xm_dev500.rows.qwen25vl_7b~tau_any.d` | 11.907461999999995 | +11.91 | number | 11_supplement_registered_rows.md Table S22 |
| 558 | data/results/c_attr_1112_score/res/SUMMARY.json | `batched.xm_dev500.rows.qwen25vl_7b~tau_any.lo` | 8.675557383333343 | 8.68 | number | 11_supplement_registered_rows.md Table S22 |
| 559 | data/results/c_attr_1112_score/res/SUMMARY.json | `batched.xm_dev500.rows.qwen25vl_7b~tau_any.hi` | 15.085479578333333 | 15.09 | number | 11_supplement_registered_rows.md Table S22 |
| 560 | data/results/c_attr_1112_score/res/SUMMARY.json | `batched.xm_dev500.rows.qwen25vl_7b~tau_any.label` | "DETECTED" | DETECTED | label | 11_supplement_registered_rows.md Table S22 |
| 561 | data/results/c_attr_1112_score/res/SUMMARY.json | `batched.xm_dev500.rows.qwen25vl_7b~tau_sel.R` | 3 | 3 | number | 11_supplement_registered_rows.md Table S22 |
| 562 | data/results/c_attr_1112_score/res/SUMMARY.json | `batched.xm_dev500.rows.qwen25vl_7b~tau_pair.D` | 2 | 2 | number | 11_supplement_registered_rows.md Table S22 |
| 563 | data/results/c_attr_1112_score/res/SUMMARY.json | `batched.xm_dev500.rows.internvl3_8b~tau_sel.d` | 0.5937809333333419 | +0.59 | number | 11_supplement_registered_rows.md Table S22 |
| 564 | data/results/c_attr_1112_score/res/SUMMARY.json | `batched.xm_dev500.rows.internvl3_8b~tau_sel.lo` | -2.4653779983333313 | −2.47 | number | 11_supplement_registered_rows.md Table S22 |
| 565 | data/results/c_attr_1112_score/res/SUMMARY.json | `batched.xm_dev500.rows.internvl3_8b~tau_sel.hi` | 3.6651635483333425 | 3.67 | number | 11_supplement_registered_rows.md Table S22 |
| 566 | data/results/c_attr_1112_score/res/SUMMARY.json | `batched.xm_dev500.rows.internvl3_8b~tau_sel.label` | "UNRESOLVED" | UNRESOLVED | label | 11_supplement_registered_rows.md Table S22 |
| 567 | data/results/c_attr_1112_score/res/SUMMARY.json | `batched.xm_dev500.rows.internvl3_8b~tau_marg.d` | -1.289019566666667 | −1.29 | number | 11_supplement_registered_rows.md Table S22 |
| 568 | data/results/c_attr_1112_score/res/SUMMARY.json | `batched.xm_dev500.rows.internvl3_8b~tau_marg.lo` | -3.582754132500011 | −3.58 | number | 11_supplement_registered_rows.md Table S22 |
| 569 | data/results/c_attr_1112_score/res/SUMMARY.json | `batched.xm_dev500.rows.internvl3_8b~tau_marg.hi` | 0.9337319041666635 | 0.93 | number | 11_supplement_registered_rows.md Table S22 |
| 570 | data/results/c_attr_1112_score/res/SUMMARY.json | `batched.xm_dev500.rows.internvl3_8b~tau_marg.label` | "UNRESOLVED" | UNRESOLVED | label | 11_supplement_registered_rows.md Table S22 |
| 571 | data/results/c_attr_1112_score/res/SUMMARY.json | `batched.xm_dev500.rows.internvl3_8b~tau_pair.d` | 1.882800500000009 | +1.88 | number | 11_supplement_registered_rows.md Table S22 |
| 572 | data/results/c_attr_1112_score/res/SUMMARY.json | `batched.xm_dev500.rows.internvl3_8b~tau_pair.lo` | -1.1951066274999955 | −1.20 | number | 11_supplement_registered_rows.md Table S22 |
| 573 | data/results/c_attr_1112_score/res/SUMMARY.json | `batched.xm_dev500.rows.internvl3_8b~tau_pair.hi` | 5.210863469999987 | 5.21 | number | 11_supplement_registered_rows.md Table S22 |
| 574 | data/results/c_attr_1112_score/res/SUMMARY.json | `batched.xm_dev500.rows.internvl3_8b~tau_pair.label` | "UNRESOLVED" | UNRESOLVED | label | 11_supplement_registered_rows.md Table S22 |
| 575 | data/results/c_attr_1112_score/res/SUMMARY.json | `batched.xm_dev500.rows.internvl3_8b~tau_any.d` | 14.03839026666666 | +14.04 | number | 11_supplement_registered_rows.md Table S22 |
| 576 | data/results/c_attr_1112_score/res/SUMMARY.json | `batched.xm_dev500.rows.internvl3_8b~tau_any.lo` | 10.644265375000007 | 10.64 | number | 11_supplement_registered_rows.md Table S22 |
| 577 | data/results/c_attr_1112_score/res/SUMMARY.json | `batched.xm_dev500.rows.internvl3_8b~tau_any.hi` | 17.814303286666668 | 17.81 | number | 11_supplement_registered_rows.md Table S22 |
| 578 | data/results/c_attr_1112_score/res/SUMMARY.json | `batched.xm_dev500.rows.internvl3_8b~tau_any.label` | "DETECTED" | DETECTED | label | 11_supplement_registered_rows.md Table S22 |
| 579 | data/results/c_attr_1112_score/res/SUMMARY.json | `batched.xm_dev500.rows.internvl3_8b~tau_sel.R` | 3 | 3 | number | 11_supplement_registered_rows.md Table S22 |
| 580 | data/results/c_attr_1112_score/res/SUMMARY.json | `batched.xm_dev500.rows.internvl3_8b~tau_pair.D` | 2 | 2 | number | 11_supplement_registered_rows.md Table S22 |
| 581 | data/results/c_attr_1112_score/res/SUMMARY.json | `batched.xm_dev500.rows.aya_vision_8b~tau_sel.d` | 1.6795706666666703 | +1.68 | number | 11_supplement_registered_rows.md Table S22 |
| 582 | data/results/c_attr_1112_score/res/SUMMARY.json | `batched.xm_dev500.rows.aya_vision_8b~tau_sel.lo` | -1.3062768333333348 | −1.31 | number | 11_supplement_registered_rows.md Table S22 |
| 583 | data/results/c_attr_1112_score/res/SUMMARY.json | `batched.xm_dev500.rows.aya_vision_8b~tau_sel.hi` | 4.5576839850000015 | 4.56 | number | 11_supplement_registered_rows.md Table S22 |
| 584 | data/results/c_attr_1112_score/res/SUMMARY.json | `batched.xm_dev500.rows.aya_vision_8b~tau_sel.label` | "UNRESOLVED" | UNRESOLVED | label | 11_supplement_registered_rows.md Table S22 |
| 585 | data/results/c_attr_1112_score/res/SUMMARY.json | `batched.xm_dev500.rows.aya_vision_8b~tau_marg.d` | -1.345614133333335 | −1.35 | number | 11_supplement_registered_rows.md Table S22 |
| 586 | data/results/c_attr_1112_score/res/SUMMARY.json | `batched.xm_dev500.rows.aya_vision_8b~tau_marg.lo` | -3.4910895875 | −3.49 | number | 11_supplement_registered_rows.md Table S22 |
| 587 | data/results/c_attr_1112_score/res/SUMMARY.json | `batched.xm_dev500.rows.aya_vision_8b~tau_marg.hi` | 0.6575888516666764 | 0.66 | number | 11_supplement_registered_rows.md Table S22 |
| 588 | data/results/c_attr_1112_score/res/SUMMARY.json | `batched.xm_dev500.rows.aya_vision_8b~tau_marg.label` | "UNRESOLVED" | UNRESOLVED | label | 11_supplement_registered_rows.md Table S22 |
| 589 | data/results/c_attr_1112_score/res/SUMMARY.json | `batched.xm_dev500.rows.aya_vision_8b~tau_pair.d` | 3.0251848000000052 | +3.03 | number | 11_supplement_registered_rows.md Table S22 |
| 590 | data/results/c_attr_1112_score/res/SUMMARY.json | `batched.xm_dev500.rows.aya_vision_8b~tau_pair.lo` | -0.21953460999999716 | −0.22 | number | 11_supplement_registered_rows.md Table S22 |
| 591 | data/results/c_attr_1112_score/res/SUMMARY.json | `batched.xm_dev500.rows.aya_vision_8b~tau_pair.hi` | 6.3596293575000065 | 6.36 | number | 11_supplement_registered_rows.md Table S22 |
| 592 | data/results/c_attr_1112_score/res/SUMMARY.json | `batched.xm_dev500.rows.aya_vision_8b~tau_pair.label` | "UNRESOLVED" | UNRESOLVED | label | 11_supplement_registered_rows.md Table S22 |
| 593 | data/results/c_attr_1112_score/res/SUMMARY.json | `batched.xm_dev500.rows.aya_vision_8b~tau_any.d` | 24.41290693333334 | +24.41 | number | 11_supplement_registered_rows.md Table S22 |
| 594 | data/results/c_attr_1112_score/res/SUMMARY.json | `batched.xm_dev500.rows.aya_vision_8b~tau_any.lo` | 20.749546470000002 | 20.75 | number | 11_supplement_registered_rows.md Table S22 |
| 595 | data/results/c_attr_1112_score/res/SUMMARY.json | `batched.xm_dev500.rows.aya_vision_8b~tau_any.hi` | 28.363572681666668 | 28.36 | number | 11_supplement_registered_rows.md Table S22 |
| 596 | data/results/c_attr_1112_score/res/SUMMARY.json | `batched.xm_dev500.rows.aya_vision_8b~tau_any.label` | "DETECTED" | DETECTED | label | 11_supplement_registered_rows.md Table S22 |
| 597 | data/results/c_attr_1112_score/res/SUMMARY.json | `batched.xm_dev500.rows.aya_vision_8b~tau_sel.R` | 3 | 3 | number | 11_supplement_registered_rows.md Table S22 |
| 598 | data/results/c_attr_1112_score/res/SUMMARY.json | `batched.xm_dev500.rows.aya_vision_8b~tau_pair.D` | 2 | 2 | number | 11_supplement_registered_rows.md Table S22 |
| 599 | data/results/c_attr_1112_score/res/SUMMARY.json | `sets.ov_dev_b.rows.qwen25vl_7b~placebo_d1_d2.flag` | false | not flagged | label | 11_supplement_registered_rows.md Table S23 |
| 600 | data/results/c_attr_1112_score/res/SUMMARY.json | `sets.ov_dev_b.variance.qwen25vl_7b.sigma2_w` | 212.52124580327208 | 212.52 | number | 11_supplement_registered_rows.md Table S23 |
| 601 | data/results/c_attr_1112_score/res/SUMMARY.json | `sets.ov_dev_b.variance.qwen25vl_7b.draw_part` | 0.07658423272189985 | 0.077 | number | 11_supplement_registered_rows.md Table S23 |
| 602 | data/results/c_attr_1112_score/res/SUMMARY.json | `sets.ov_dev_b.variance.qwen25vl_7b.total` | 0.8634083608489982 | 0.863 | number | 11_supplement_registered_rows.md Table S23 |
| 603 | data/results/c_attr_1112_score/res/SUMMARY.json | `sets.ov_dev_b.variance.qwen25vl_7b.share` | 0.0886998970528775 | 0.089 | number | 11_supplement_registered_rows.md Table S23 |
| 604 | data/results/c_attr_1112_score/res/SUMMARY.json | `sets.ov_dev_b.rows.qwen25vl_7b~placebo_d1_d2.d` | -0.33175967567567355 | −0.33 | number | 11_supplement_registered_rows.md Table S23 |
| 605 | data/results/c_attr_1112_score/res/SUMMARY.json | `sets.ov_dev_b.rows.qwen25vl_7b~placebo_d1_d2.lo` | -1.6359834702702702 | −1.64 | number | 11_supplement_registered_rows.md Table S23 |
| 606 | data/results/c_attr_1112_score/res/SUMMARY.json | `sets.ov_dev_b.rows.qwen25vl_7b~placebo_d1_d2.hi` | 0.992492956756755 | 0.99 | number | 11_supplement_registered_rows.md Table S23 |
| 607 | data/results/c_attr_1112_score/res/SUMMARY.json | `sets.ov_dev_b.rows.internvl3_8b~placebo_d1_d2.flag` | false | not flagged | label | 11_supplement_registered_rows.md Table S23 |
| 608 | data/results/c_attr_1112_score/res/SUMMARY.json | `sets.ov_dev_b.variance.internvl3_8b.sigma2_w` | 290.4653692379207 | 290.47 | number | 11_supplement_registered_rows.md Table S23 |
| 609 | data/results/c_attr_1112_score/res/SUMMARY.json | `sets.ov_dev_b.variance.internvl3_8b.draw_part` | 0.10467220513078224 | 0.105 | number | 11_supplement_registered_rows.md Table S23 |
| 610 | data/results/c_attr_1112_score/res/SUMMARY.json | `sets.ov_dev_b.variance.internvl3_8b.total` | 0.6414668158552514 | 0.641 | number | 11_supplement_registered_rows.md Table S23 |
| 611 | data/results/c_attr_1112_score/res/SUMMARY.json | `sets.ov_dev_b.variance.internvl3_8b.share` | 0.1631763367076525 | 0.163 | number | 11_supplement_registered_rows.md Table S23 |
| 612 | data/results/c_attr_1112_score/res/SUMMARY.json | `sets.ov_dev_b.rows.internvl3_8b~placebo_d1_d2.d` | -0.5550476756756737 | −0.56 | number | 11_supplement_registered_rows.md Table S23 |
| 613 | data/results/c_attr_1112_score/res/SUMMARY.json | `sets.ov_dev_b.rows.internvl3_8b~placebo_d1_d2.lo` | -2.1812182756756764 | −2.18 | number | 11_supplement_registered_rows.md Table S23 |
| 614 | data/results/c_attr_1112_score/res/SUMMARY.json | `sets.ov_dev_b.rows.internvl3_8b~placebo_d1_d2.hi` | 1.0469011783783815 | 1.05 | number | 11_supplement_registered_rows.md Table S23 |
| 615 | data/results/c_attr_1112_score/res/SUMMARY.json | `sets.ov_dev_b.rows.aya_vision_8b~placebo_d1_d2.flag` | true | flagged | label | 11_supplement_registered_rows.md Table S23 |
| 616 | data/results/c_attr_1112_score/res/SUMMARY.json | `sets.ov_dev_b.variance.aya_vision_8b.sigma2_w` | 216.95696173621624 | 216.96 | number | 11_supplement_registered_rows.md Table S23 |
| 617 | data/results/c_attr_1112_score/res/SUMMARY.json | `sets.ov_dev_b.variance.aya_vision_8b.draw_part` | 0.0781826889139518 | 0.078 | number | 11_supplement_registered_rows.md Table S23 |
| 618 | data/results/c_attr_1112_score/res/SUMMARY.json | `sets.ov_dev_b.variance.aya_vision_8b.total` | 0.5230741489700285 | 0.523 | number | 11_supplement_registered_rows.md Table S23 |
| 619 | data/results/c_attr_1112_score/res/SUMMARY.json | `sets.ov_dev_b.variance.aya_vision_8b.share` | 0.1494676979695886 | 0.149 | number | 11_supplement_registered_rows.md Table S23 |
| 620 | data/results/c_attr_1112_score/res/SUMMARY.json | `sets.ov_dev_b.rows.aya_vision_8b~placebo_d1_d2.d` | -2.031620864864866 | −2.03 | number | 11_supplement_registered_rows.md Table S23 |
| 621 | data/results/c_attr_1112_score/res/SUMMARY.json | `sets.ov_dev_b.rows.aya_vision_8b~placebo_d1_d2.lo` | -3.4191781540540562 | −3.42 | number | 11_supplement_registered_rows.md Table S23 |
| 622 | data/results/c_attr_1112_score/res/SUMMARY.json | `sets.ov_dev_b.rows.aya_vision_8b~placebo_d1_d2.hi` | -0.7409918891891858 | −0.74 | number | 11_supplement_registered_rows.md Table S23 |
| 623 | data/results/c_attr_1112_score/res/SUMMARY.json | `sets.xm_dev500.rows.qwen25vl_7b~placebo_d1_d2.flag` | false | not flagged | label | 11_supplement_registered_rows.md Table S23 |
| 624 | data/results/c_attr_1112_score/res/SUMMARY.json | `sets.xm_dev500.variance.qwen25vl_7b.sigma2_w` | 640.5166543682467 | 640.52 | number | 11_supplement_registered_rows.md Table S23 |
| 625 | data/results/c_attr_1112_score/res/SUMMARY.json | `sets.xm_dev500.variance.qwen25vl_7b.draw_part` | 0.4270111029121645 | 0.427 | number | 11_supplement_registered_rows.md Table S23 |
| 626 | data/results/c_attr_1112_score/res/SUMMARY.json | `sets.xm_dev500.variance.qwen25vl_7b.total` | 2.666639420000501 | 2.667 | number | 11_supplement_registered_rows.md Table S23 |
| 627 | data/results/c_attr_1112_score/res/SUMMARY.json | `sets.xm_dev500.variance.qwen25vl_7b.share` | 0.16013079972847782 | 0.160 | number | 11_supplement_registered_rows.md Table S23 |
| 628 | data/results/c_attr_1112_score/res/SUMMARY.json | `sets.xm_dev500.rows.qwen25vl_7b~placebo_d1_d2.d` | 3.210298999999999 | +3.21 | number | 11_supplement_registered_rows.md Table S23 |
| 629 | data/results/c_attr_1112_score/res/SUMMARY.json | `sets.xm_dev500.rows.qwen25vl_7b~placebo_d1_d2.lo` | -0.11569781999999974 | −0.12 | number | 11_supplement_registered_rows.md Table S23 |
| 630 | data/results/c_attr_1112_score/res/SUMMARY.json | `sets.xm_dev500.rows.qwen25vl_7b~placebo_d1_d2.hi` | 6.179432014999989 | 6.18 | number | 11_supplement_registered_rows.md Table S23 |
| 631 | data/results/c_attr_1112_score/res/SUMMARY.json | `sets.xm_dev500.rows.internvl3_8b~placebo_d1_d2.flag` | false | not flagged | label | 11_supplement_registered_rows.md Table S23 |
| 632 | data/results/c_attr_1112_score/res/SUMMARY.json | `sets.xm_dev500.variance.internvl3_8b.sigma2_w` | 740.4924560408066 | 740.49 | number | 11_supplement_registered_rows.md Table S23 |
| 633 | data/results/c_attr_1112_score/res/SUMMARY.json | `sets.xm_dev500.variance.internvl3_8b.draw_part` | 0.4936616373605377 | 0.494 | number | 11_supplement_registered_rows.md Table S23 |
| 634 | data/results/c_attr_1112_score/res/SUMMARY.json | `sets.xm_dev500.variance.internvl3_8b.total` | 2.5769782849076206 | 2.577 | number | 11_supplement_registered_rows.md Table S23 |
| 635 | data/results/c_attr_1112_score/res/SUMMARY.json | `sets.xm_dev500.variance.internvl3_8b.share` | 0.1915660835218231 | 0.192 | number | 11_supplement_registered_rows.md Table S23 |
| 636 | data/results/c_attr_1112_score/res/SUMMARY.json | `sets.xm_dev500.rows.internvl3_8b~placebo_d1_d2.d` | -1.489409000000009 | −1.49 | number | 11_supplement_registered_rows.md Table S23 |
| 637 | data/results/c_attr_1112_score/res/SUMMARY.json | `sets.xm_dev500.rows.internvl3_8b~placebo_d1_d2.lo` | -4.82888304000001 | −4.83 | number | 11_supplement_registered_rows.md Table S23 |
| 638 | data/results/c_attr_1112_score/res/SUMMARY.json | `sets.xm_dev500.rows.internvl3_8b~placebo_d1_d2.hi` | 1.7229946949999875 | 1.72 | number | 11_supplement_registered_rows.md Table S23 |
| 639 | data/results/c_attr_1112_score/res/SUMMARY.json | `sets.xm_dev500.rows.aya_vision_8b~placebo_d1_d2.flag` | false | not flagged | label | 11_supplement_registered_rows.md Table S23 |
| 640 | data/results/c_attr_1112_score/res/SUMMARY.json | `sets.xm_dev500.variance.aya_vision_8b.sigma2_w` | 638.6024994746933 | 638.60 | number | 11_supplement_registered_rows.md Table S23 |
| 641 | data/results/c_attr_1112_score/res/SUMMARY.json | `sets.xm_dev500.variance.aya_vision_8b.draw_part` | 0.42573499964979555 | 0.426 | number | 11_supplement_registered_rows.md Table S23 |
| 642 | data/results/c_attr_1112_score/res/SUMMARY.json | `sets.xm_dev500.variance.aya_vision_8b.total` | 2.0942903048421546 | 2.094 | number | 11_supplement_registered_rows.md Table S23 |
| 643 | data/results/c_attr_1112_score/res/SUMMARY.json | `sets.xm_dev500.variance.aya_vision_8b.share` | 0.20328366065844103 | 0.203 | number | 11_supplement_registered_rows.md Table S23 |
| 644 | data/results/c_attr_1112_score/res/SUMMARY.json | `sets.xm_dev500.rows.aya_vision_8b~placebo_d1_d2.d` | 0.8272496000000089 | +0.83 | number | 11_supplement_registered_rows.md Table S23 |
| 645 | data/results/c_attr_1112_score/res/SUMMARY.json | `sets.xm_dev500.rows.aya_vision_8b~placebo_d1_d2.lo` | -2.1603134249999965 | −2.16 | number | 11_supplement_registered_rows.md Table S23 |
| 646 | data/results/c_attr_1112_score/res/SUMMARY.json | `sets.xm_dev500.rows.aya_vision_8b~placebo_d1_d2.hi` | 3.848266890000001 | 3.85 | number | 11_supplement_registered_rows.md Table S23 |
| 647 | data/results/c_attr_1112_score/res/SUMMARY.json | `batched.ov_dev_b.fixed_set.qwen25vl_7b.MS_F` | 2737.576495794759 | 2737.58 | number | 11_supplement_registered_rows.md Table S23 |
| 648 | data/results/c_attr_1112_score/res/SUMMARY.json | `batched.ov_dev_b.fixed_set.qwen25vl_7b.MS_I` | 4085.619340810017 | 4085.62 | number | 11_supplement_registered_rows.md Table S23 |
| 649 | data/results/c_attr_1112_score/res/SUMMARY.json | `batched.ov_dev_b.fixed_set.qwen25vl_7b.MS_E` | 227.367392317339 | 227.37 | number | 11_supplement_registered_rows.md Table S23 |
| 650 | data/results/c_attr_1112_score/res/SUMMARY.json | `batched.ov_dev_b.fixed_set.qwen25vl_7b.V_b` | 2.7137395713269403 | 2.71 | number | 11_supplement_registered_rows.md Table S23 |
| 651 | data/results/c_attr_1112_score/res/SUMMARY.json | `batched.ov_dev_b.fixed_set.qwen25vl_7b.V_img` | 1.0800192238009454 | 1.08 | number | 11_supplement_registered_rows.md Table S23 |
| 652 | data/results/c_attr_1112_score/res/SUMMARY.json | `batched.ov_dev_b.fixed_set.qwen25vl_7b.omega` | 2.5126771001134514 | 2.51 | number | 11_supplement_registered_rows.md Table S23 |
| 653 | data/results/c_attr_1112_score/res/SUMMARY.json | `batched.ov_dev_b.fixed_set.qwen25vl_7b.omega_upper` | 15.197522895461283 | 15.20 | number | 11_supplement_registered_rows.md Table S23 |
| 654 | data/results/c_attr_1112_score/res/SUMMARY.json | `batched.ov_dev_b.fixed_set.qwen25vl_7b.dev_row.d` | 8.164714335135136 | +8.16 | number | 11_supplement_registered_rows.md Table S23 |
| 655 | data/results/c_attr_1112_score/res/SUMMARY.json | `batched.ov_dev_b.fixed_set.qwen25vl_7b.dev_row.lo` | 4.849070304615683 | 4.85 | number | 11_supplement_registered_rows.md Table S23 |
| 656 | data/results/c_attr_1112_score/res/SUMMARY.json | `batched.ov_dev_b.fixed_set.qwen25vl_7b.dev_row.hi` | 11.480358365654588 | 11.48 | number | 11_supplement_registered_rows.md Table S23 |
| 657 | data/results/c_attr_1112_score/res/SUMMARY.json | `batched.xm_dev500.fixed_set.qwen25vl_7b.MS_F` | 1395.7182583556998 | 1395.72 | number | 11_supplement_registered_rows.md Table S23 |
| 658 | data/results/c_attr_1112_score/res/SUMMARY.json | `batched.xm_dev500.fixed_set.qwen25vl_7b.MS_I` | 6044.477957711326 | 6044.48 | number | 11_supplement_registered_rows.md Table S23 |
| 659 | data/results/c_attr_1112_score/res/SUMMARY.json | `batched.xm_dev500.fixed_set.qwen25vl_7b.MS_E` | 634.8982540286939 | 634.90 | number | 11_supplement_registered_rows.md Table S23 |
| 660 | data/results/c_attr_1112_score/res/SUMMARY.json | `batched.xm_dev500.fixed_set.qwen25vl_7b.V_b` | 1.5216400086540118 | 1.52 | number | 11_supplement_registered_rows.md Table S23 |
| 661 | data/results/c_attr_1112_score/res/SUMMARY.json | `batched.xm_dev500.fixed_set.qwen25vl_7b.V_img` | 3.4336283895304405 | 3.43 | number | 11_supplement_registered_rows.md Table S23 |
| 662 | data/results/c_attr_1112_score/res/SUMMARY.json | `batched.xm_dev500.fixed_set.qwen25vl_7b.omega` | 0.44315803460085584 | 0.44 | number | 11_supplement_registered_rows.md Table S23 |
| 663 | data/results/c_attr_1112_score/res/SUMMARY.json | `batched.xm_dev500.fixed_set.qwen25vl_7b.omega_upper` | 4.2071179831759995 | 4.21 | number | 11_supplement_registered_rows.md Table S23 |
| 664 | data/results/c_attr_1112_score/res/SUMMARY.json | `batched.xm_dev500.fixed_set.qwen25vl_7b.dev_row.d` | 2.5764050000000003 | +2.58 | number | 11_supplement_registered_rows.md Table S23 |
| 665 | data/results/c_attr_1112_score/res/SUMMARY.json | `batched.xm_dev500.fixed_set.qwen25vl_7b.dev_row.lo` | -2.004409014657732 | −2.00 | number | 11_supplement_registered_rows.md Table S23 |
| 666 | data/results/c_attr_1112_score/res/SUMMARY.json | `batched.xm_dev500.fixed_set.qwen25vl_7b.dev_row.hi` | 7.157219014657732 | 7.16 | number | 11_supplement_registered_rows.md Table S23 |
| 667 | data/results/c_attr_1112_score/res/COPYBOUND_ov_dev_b_qwen25vl_7b.json | `bound.i_syllables.n2.K_ret.d` | 20.173259607874694 | +20.17 | number | 11_supplement_registered_rows.md Table S24 |
| 668 | data/results/c_attr_1112_score/res/COPYBOUND_ov_dev_b_qwen25vl_7b.json | `bound.i_syllables.n2.K_ret.lo` | 18.165258683901303 | 18.17 | number | 11_supplement_registered_rows.md Table S24 |
| 669 | data/results/c_attr_1112_score/res/COPYBOUND_ov_dev_b_qwen25vl_7b.json | `bound.i_syllables.n2.K_ret.hi` | 22.21177198842961 | 22.21 | number | 11_supplement_registered_rows.md Table S24 |
| 670 | data/results/c_attr_1112_score/res/COPYBOUND_ov_dev_b_qwen25vl_7b.json | `bound.i_syllables.n2.K_ret.label` | "DETECTED" | DETECTED | label | 11_supplement_registered_rows.md Table S24 |
| 671 | data/results/c_attr_1112_score/res/COPYBOUND_ov_dev_b_qwen25vl_7b.json | `bound.i_syllables.n2.L_cp.d` | -10.503642858396184 | −10.50 | number | 11_supplement_registered_rows.md Table S24 |
| 672 | data/results/c_attr_1112_score/res/COPYBOUND_ov_dev_b_qwen25vl_7b.json | `bound.i_syllables.n2.L_cp.lo` | -12.212096373847976 | −12.21 | number | 11_supplement_registered_rows.md Table S24 |
| 673 | data/results/c_attr_1112_score/res/COPYBOUND_ov_dev_b_qwen25vl_7b.json | `bound.i_syllables.n2.L_cp.hi` | -8.749487533101663 | −8.75 | number | 11_supplement_registered_rows.md Table S24 |
| 674 | data/results/c_attr_1112_score/res/COPYBOUND_ov_dev_b_qwen25vl_7b.json | `bound.i_syllables.n2.L_cp.label` | "REVERSED" | REVERSED | label | 11_supplement_registered_rows.md Table S24 |
| 675 | data/results/c_attr_1112_score/res/COPYBOUND_ov_dev_b_qwen25vl_7b.json | `bound.i_syllables.n2.K_nc.d` | 7.340368174435672 | +7.34 | number | 11_supplement_registered_rows.md Table S24 |
| 676 | data/results/c_attr_1112_score/res/COPYBOUND_ov_dev_b_qwen25vl_7b.json | `bound.i_syllables.n2.K_nc.lo` | 5.881051422410266 | 5.88 | number | 11_supplement_registered_rows.md Table S24 |
| 677 | data/results/c_attr_1112_score/res/COPYBOUND_ov_dev_b_qwen25vl_7b.json | `bound.i_syllables.n2.K_nc.hi` | 8.74308837362394 | 8.74 | number | 11_supplement_registered_rows.md Table S24 |
| 678 | data/results/c_attr_1112_score/res/COPYBOUND_ov_dev_b_qwen25vl_7b.json | `bound.i_syllables.n2.K_nc.label` | "DETECTED" | DETECTED | label | 11_supplement_registered_rows.md Table S24 |
| 679 | data/results/c_attr_1112_score/res/COPYBOUND_ov_dev_b_qwen25vl_7b.json | `bound.i_syllables.n2.K_rand.d` | 3.876477314428872 | +3.88 | number | 11_supplement_registered_rows.md Table S24 |
| 680 | data/results/c_attr_1112_score/res/COPYBOUND_ov_dev_b_qwen25vl_7b.json | `bound.i_syllables.n2.K_rand.lo` | 3.006042178026314 | 3.01 | number | 11_supplement_registered_rows.md Table S24 |
| 681 | data/results/c_attr_1112_score/res/COPYBOUND_ov_dev_b_qwen25vl_7b.json | `bound.i_syllables.n2.K_rand.hi` | 4.784432195523283 | 4.78 | number | 11_supplement_registered_rows.md Table S24 |
| 682 | data/results/c_attr_1112_score/res/COPYBOUND_ov_dev_b_qwen25vl_7b.json | `bound.i_syllables.n2.K_ret_minus_K_nc.d` | 12.832891433439022 | +12.83 | number | 11_supplement_registered_rows.md Table S24 |
| 683 | data/results/c_attr_1112_score/res/COPYBOUND_ov_dev_b_qwen25vl_7b.json | `bound.i_syllables.n2.K_ret_minus_K_nc.lo` | 10.992827521559997 | 10.99 | number | 11_supplement_registered_rows.md Table S24 |
| 684 | data/results/c_attr_1112_score/res/COPYBOUND_ov_dev_b_qwen25vl_7b.json | `bound.i_syllables.n2.K_ret_minus_K_nc.hi` | 14.86462361656612 | 14.86 | number | 11_supplement_registered_rows.md Table S24 |
| 685 | data/results/c_attr_1112_score/res/COPYBOUND_ov_dev_b_qwen25vl_7b.json | `bound.i_syllables.n2.blind_loss.d` | 22.667381861047055 | +22.67 | number | 11_supplement_registered_rows.md Table S24 |
| 686 | data/results/c_attr_1112_score/res/COPYBOUND_ov_dev_b_qwen25vl_7b.json | `bound.i_syllables.n2.blind_loss.lo` | 20.67743279906598 | 20.68 | number | 11_supplement_registered_rows.md Table S24 |
| 687 | data/results/c_attr_1112_score/res/COPYBOUND_ov_dev_b_qwen25vl_7b.json | `bound.i_syllables.n2.blind_loss.hi` | 24.691665772672362 | 24.69 | number | 11_supplement_registered_rows.md Table S24 |
| 688 | data/results/c_attr_1112_score/res/COPYBOUND_ov_dev_b_qwen25vl_7b.json | `bound.i_syllables.n2.K_ret.tier` | "POST HOC" | POST HOC | label | 11_supplement_registered_rows.md Table S24 |
| 689 | data/results/c_attr_1112_score/res/COPYBOUND_ov_dev_b_qwen25vl_7b.json | `bound.i_syllables.n3.K_ret.d` | 18.58449544906159 | +18.58 | number | 11_supplement_registered_rows.md Table S24 |
| 690 | data/results/c_attr_1112_score/res/COPYBOUND_ov_dev_b_qwen25vl_7b.json | `bound.i_syllables.n3.K_ret.lo` | 16.563576582062172 | 16.56 | number | 11_supplement_registered_rows.md Table S24 |
| 691 | data/results/c_attr_1112_score/res/COPYBOUND_ov_dev_b_qwen25vl_7b.json | `bound.i_syllables.n3.K_ret.hi` | 20.728290133833966 | 20.73 | number | 11_supplement_registered_rows.md Table S24 |
| 692 | data/results/c_attr_1112_score/res/COPYBOUND_ov_dev_b_qwen25vl_7b.json | `bound.i_syllables.n3.K_ret.label` | "DETECTED" | DETECTED | label | 11_supplement_registered_rows.md Table S24 |
| 693 | data/results/c_attr_1112_score/res/COPYBOUND_ov_dev_b_qwen25vl_7b.json | `bound.i_syllables.n3.L_cp.d` | -8.914878699583078 | −8.91 | number | 11_supplement_registered_rows.md Table S24 |
| 694 | data/results/c_attr_1112_score/res/COPYBOUND_ov_dev_b_qwen25vl_7b.json | `bound.i_syllables.n3.L_cp.lo` | -10.707668881201924 | −10.71 | number | 11_supplement_registered_rows.md Table S24 |
| 695 | data/results/c_attr_1112_score/res/COPYBOUND_ov_dev_b_qwen25vl_7b.json | `bound.i_syllables.n3.L_cp.hi` | -7.06586722529071 | −7.07 | number | 11_supplement_registered_rows.md Table S24 |
| 696 | data/results/c_attr_1112_score/res/COPYBOUND_ov_dev_b_qwen25vl_7b.json | `bound.i_syllables.n3.L_cp.label` | "REVERSED" | REVERSED | label | 11_supplement_registered_rows.md Table S24 |
| 697 | data/results/c_attr_1112_score/res/COPYBOUND_ov_dev_b_qwen25vl_7b.json | `bound.i_syllables.n3.K_nc.d` | 5.587956366154785 | +5.59 | number | 11_supplement_registered_rows.md Table S24 |
| 698 | data/results/c_attr_1112_score/res/COPYBOUND_ov_dev_b_qwen25vl_7b.json | `bound.i_syllables.n3.K_nc.lo` | 4.411402401183649 | 4.41 | number | 11_supplement_registered_rows.md Table S24 |
| 699 | data/results/c_attr_1112_score/res/COPYBOUND_ov_dev_b_qwen25vl_7b.json | `bound.i_syllables.n3.K_nc.hi` | 6.748425069214175 | 6.75 | number | 11_supplement_registered_rows.md Table S24 |
| 700 | data/results/c_attr_1112_score/res/COPYBOUND_ov_dev_b_qwen25vl_7b.json | `bound.i_syllables.n3.K_nc.label` | "DETECTED" | DETECTED | label | 11_supplement_registered_rows.md Table S24 |
| 701 | data/results/c_attr_1112_score/res/COPYBOUND_ov_dev_b_qwen25vl_7b.json | `bound.i_syllables.n3.K_rand.d` | 1.9117414874932566 | +1.91 | number | 11_supplement_registered_rows.md Table S24 |
| 702 | data/results/c_attr_1112_score/res/COPYBOUND_ov_dev_b_qwen25vl_7b.json | `bound.i_syllables.n3.K_rand.lo` | 1.3740210974691518 | 1.37 | number | 11_supplement_registered_rows.md Table S24 |
| 703 | data/results/c_attr_1112_score/res/COPYBOUND_ov_dev_b_qwen25vl_7b.json | `bound.i_syllables.n3.K_rand.hi` | 2.4937739230519593 | 2.49 | number | 11_supplement_registered_rows.md Table S24 |
| 704 | data/results/c_attr_1112_score/res/COPYBOUND_ov_dev_b_qwen25vl_7b.json | `bound.i_syllables.n3.K_ret_minus_K_nc.d` | 12.996539082906802 | +13.00 | number | 11_supplement_registered_rows.md Table S24 |
| 705 | data/results/c_attr_1112_score/res/COPYBOUND_ov_dev_b_qwen25vl_7b.json | `bound.i_syllables.n3.K_ret_minus_K_nc.lo` | 11.151866686415204 | 11.15 | number | 11_supplement_registered_rows.md Table S24 |
| 706 | data/results/c_attr_1112_score/res/COPYBOUND_ov_dev_b_qwen25vl_7b.json | `bound.i_syllables.n3.K_ret_minus_K_nc.hi` | 14.98035675424074 | 14.98 | number | 11_supplement_registered_rows.md Table S24 |
| 707 | data/results/c_attr_1112_score/res/COPYBOUND_ov_dev_b_qwen25vl_7b.json | `bound.i_syllables.n3.blind_loss.d` | 19.887256582488497 | +19.89 | number | 11_supplement_registered_rows.md Table S24 |
| 708 | data/results/c_attr_1112_score/res/COPYBOUND_ov_dev_b_qwen25vl_7b.json | `bound.i_syllables.n3.blind_loss.lo` | 17.951735125239544 | 17.95 | number | 11_supplement_registered_rows.md Table S24 |
| 709 | data/results/c_attr_1112_score/res/COPYBOUND_ov_dev_b_qwen25vl_7b.json | `bound.i_syllables.n3.blind_loss.hi` | 21.858453485831465 | 21.86 | number | 11_supplement_registered_rows.md Table S24 |
| 710 | data/results/c_attr_1112_score/res/COPYBOUND_ov_dev_b_qwen25vl_7b.json | `bound.i_syllables.n3.K_ret.tier` | "POST HOC" | POST HOC | label | 11_supplement_registered_rows.md Table S24 |
| 711 | data/results/c_attr_1112_score/res/COPYBOUND_ov_dev_b_qwen25vl_7b.json | `bound.i_syllables.n4.K_ret.d` | 14.264802781738277 | +14.26 | number | 11_supplement_registered_rows.md Table S24 |
| 712 | data/results/c_attr_1112_score/res/COPYBOUND_ov_dev_b_qwen25vl_7b.json | `bound.i_syllables.n4.K_ret.lo` | 12.371446445555144 | 12.37 | number | 11_supplement_registered_rows.md Table S24 |
| 713 | data/results/c_attr_1112_score/res/COPYBOUND_ov_dev_b_qwen25vl_7b.json | `bound.i_syllables.n4.K_ret.hi` | 16.189306081390207 | 16.19 | number | 11_supplement_registered_rows.md Table S24 |
| 714 | data/results/c_attr_1112_score/res/COPYBOUND_ov_dev_b_qwen25vl_7b.json | `bound.i_syllables.n4.K_ret.label` | "DETECTED" | DETECTED | label | 11_supplement_registered_rows.md Table S24 |
| 715 | data/results/c_attr_1112_score/res/COPYBOUND_ov_dev_b_qwen25vl_7b.json | `bound.i_syllables.n4.L_cp.d` | -4.5951860322597655 | −4.60 | number | 11_supplement_registered_rows.md Table S24 |
| 716 | data/results/c_attr_1112_score/res/COPYBOUND_ov_dev_b_qwen25vl_7b.json | `bound.i_syllables.n4.L_cp.lo` | -6.475802004574802 | −6.48 | number | 11_supplement_registered_rows.md Table S24 |
| 717 | data/results/c_attr_1112_score/res/COPYBOUND_ov_dev_b_qwen25vl_7b.json | `bound.i_syllables.n4.L_cp.hi` | -2.667201825702172 | −2.67 | number | 11_supplement_registered_rows.md Table S24 |
| 718 | data/results/c_attr_1112_score/res/COPYBOUND_ov_dev_b_qwen25vl_7b.json | `bound.i_syllables.n4.L_cp.label` | "REVERSED" | REVERSED | label | 11_supplement_registered_rows.md Table S24 |
| 719 | data/results/c_attr_1112_score/res/COPYBOUND_ov_dev_b_qwen25vl_7b.json | `bound.i_syllables.n4.K_nc.d` | 3.3865031556716163 | +3.39 | number | 11_supplement_registered_rows.md Table S24 |
| 720 | data/results/c_attr_1112_score/res/COPYBOUND_ov_dev_b_qwen25vl_7b.json | `bound.i_syllables.n4.K_nc.lo` | 2.557330300792549 | 2.56 | number | 11_supplement_registered_rows.md Table S24 |
| 721 | data/results/c_attr_1112_score/res/COPYBOUND_ov_dev_b_qwen25vl_7b.json | `bound.i_syllables.n4.K_nc.hi` | 4.309342019885388 | 4.31 | number | 11_supplement_registered_rows.md Table S24 |
| 722 | data/results/c_attr_1112_score/res/COPYBOUND_ov_dev_b_qwen25vl_7b.json | `bound.i_syllables.n4.K_nc.label` | "DETECTED" | DETECTED | label | 11_supplement_registered_rows.md Table S24 |
| 723 | data/results/c_attr_1112_score/res/COPYBOUND_ov_dev_b_qwen25vl_7b.json | `bound.i_syllables.n4.K_rand.d` | 1.173521915072893 | +1.17 | number | 11_supplement_registered_rows.md Table S24 |
| 724 | data/results/c_attr_1112_score/res/COPYBOUND_ov_dev_b_qwen25vl_7b.json | `bound.i_syllables.n4.K_rand.lo` | 0.7818249911783214 | 0.78 | number | 11_supplement_registered_rows.md Table S24 |
| 725 | data/results/c_attr_1112_score/res/COPYBOUND_ov_dev_b_qwen25vl_7b.json | `bound.i_syllables.n4.K_rand.hi` | 1.5890729785919984 | 1.59 | number | 11_supplement_registered_rows.md Table S24 |
| 726 | data/results/c_attr_1112_score/res/COPYBOUND_ov_dev_b_qwen25vl_7b.json | `bound.i_syllables.n4.K_ret_minus_K_nc.d` | 10.878299626066662 | +10.88 | number | 11_supplement_registered_rows.md Table S24 |
| 727 | data/results/c_attr_1112_score/res/COPYBOUND_ov_dev_b_qwen25vl_7b.json | `bound.i_syllables.n4.K_ret_minus_K_nc.lo` | 9.18090345950955 | 9.18 | number | 11_supplement_registered_rows.md Table S24 |
| 728 | data/results/c_attr_1112_score/res/COPYBOUND_ov_dev_b_qwen25vl_7b.json | `bound.i_syllables.n4.K_ret_minus_K_nc.hi` | 12.6232092598162 | 12.62 | number | 11_supplement_registered_rows.md Table S24 |
| 729 | data/results/c_attr_1112_score/res/COPYBOUND_ov_dev_b_qwen25vl_7b.json | `bound.i_syllables.n4.blind_loss.d` | 15.920389591980394 | +15.92 | number | 11_supplement_registered_rows.md Table S24 |
| 730 | data/results/c_attr_1112_score/res/COPYBOUND_ov_dev_b_qwen25vl_7b.json | `bound.i_syllables.n4.blind_loss.lo` | 14.183920361737215 | 14.18 | number | 11_supplement_registered_rows.md Table S24 |
| 731 | data/results/c_attr_1112_score/res/COPYBOUND_ov_dev_b_qwen25vl_7b.json | `bound.i_syllables.n4.blind_loss.hi` | 17.74358904541176 | 17.74 | number | 11_supplement_registered_rows.md Table S24 |
| 732 | data/results/c_attr_1112_score/res/COPYBOUND_ov_dev_b_qwen25vl_7b.json | `bound.i_syllables.n4.K_ret.tier` | "POST HOC" | POST HOC | label | 11_supplement_registered_rows.md Table S24 |
| 733 | data/results/c_attr_1112_score/res/COPYBOUND_ov_dev_b_qwen25vl_7b.json | `bound.ii_words.n2.K_ret.d` | 21.37487895310364 | +21.37 | number | 11_supplement_registered_rows.md Table S24 |
| 734 | data/results/c_attr_1112_score/res/COPYBOUND_ov_dev_b_qwen25vl_7b.json | `bound.ii_words.n2.K_ret.lo` | 19.36191229750859 | 19.36 | number | 11_supplement_registered_rows.md Table S24 |
| 735 | data/results/c_attr_1112_score/res/COPYBOUND_ov_dev_b_qwen25vl_7b.json | `bound.ii_words.n2.K_ret.hi` | 23.499706323302597 | 23.50 | number | 11_supplement_registered_rows.md Table S24 |
| 736 | data/results/c_attr_1112_score/res/COPYBOUND_ov_dev_b_qwen25vl_7b.json | `bound.ii_words.n2.K_ret.label` | "DETECTED" | DETECTED | label | 11_supplement_registered_rows.md Table S24 |
| 737 | data/results/c_attr_1112_score/res/COPYBOUND_ov_dev_b_qwen25vl_7b.json | `bound.ii_words.n2.L_cp.d` | -11.70526220362513 | −11.71 | number | 11_supplement_registered_rows.md Table S24 |
| 738 | data/results/c_attr_1112_score/res/COPYBOUND_ov_dev_b_qwen25vl_7b.json | `bound.ii_words.n2.L_cp.lo` | -13.471743326166632 | −13.47 | number | 11_supplement_registered_rows.md Table S24 |
| 739 | data/results/c_attr_1112_score/res/COPYBOUND_ov_dev_b_qwen25vl_7b.json | `bound.ii_words.n2.L_cp.hi` | -9.89134397934223 | −9.89 | number | 11_supplement_registered_rows.md Table S24 |
| 740 | data/results/c_attr_1112_score/res/COPYBOUND_ov_dev_b_qwen25vl_7b.json | `bound.ii_words.n2.L_cp.label` | "REVERSED" | REVERSED | label | 11_supplement_registered_rows.md Table S24 |
| 741 | data/results/c_attr_1112_score/res/COPYBOUND_ov_dev_b_qwen25vl_7b.json | `bound.ii_words.n2.K_nc.d` | 7.522856633306463 | +7.52 | number | 11_supplement_registered_rows.md Table S24 |
| 742 | data/results/c_attr_1112_score/res/COPYBOUND_ov_dev_b_qwen25vl_7b.json | `bound.ii_words.n2.K_nc.lo` | 6.143296812381639 | 6.14 | number | 11_supplement_registered_rows.md Table S24 |
| 743 | data/results/c_attr_1112_score/res/COPYBOUND_ov_dev_b_qwen25vl_7b.json | `bound.ii_words.n2.K_nc.hi` | 8.891809200142339 | 8.89 | number | 11_supplement_registered_rows.md Table S24 |
| 744 | data/results/c_attr_1112_score/res/COPYBOUND_ov_dev_b_qwen25vl_7b.json | `bound.ii_words.n2.K_nc.label` | "DETECTED" | DETECTED | label | 11_supplement_registered_rows.md Table S24 |
| 745 | data/results/c_attr_1112_score/res/COPYBOUND_ov_dev_b_qwen25vl_7b.json | `bound.ii_words.n2.K_rand.d` | 3.898530725116333 | +3.90 | number | 11_supplement_registered_rows.md Table S24 |
| 746 | data/results/c_attr_1112_score/res/COPYBOUND_ov_dev_b_qwen25vl_7b.json | `bound.ii_words.n2.K_rand.lo` | 3.0407432882075414 | 3.04 | number | 11_supplement_registered_rows.md Table S24 |
| 747 | data/results/c_attr_1112_score/res/COPYBOUND_ov_dev_b_qwen25vl_7b.json | `bound.ii_words.n2.K_rand.hi` | 4.763224830126949 | 4.76 | number | 11_supplement_registered_rows.md Table S24 |
| 748 | data/results/c_attr_1112_score/res/COPYBOUND_ov_dev_b_qwen25vl_7b.json | `bound.ii_words.n2.K_ret_minus_K_nc.d` | 13.85202231979718 | +13.85 | number | 11_supplement_registered_rows.md Table S24 |
| 749 | data/results/c_attr_1112_score/res/COPYBOUND_ov_dev_b_qwen25vl_7b.json | `bound.ii_words.n2.K_ret_minus_K_nc.lo` | 11.927023933921594 | 11.93 | number | 11_supplement_registered_rows.md Table S24 |
| 750 | data/results/c_attr_1112_score/res/COPYBOUND_ov_dev_b_qwen25vl_7b.json | `bound.ii_words.n2.K_ret_minus_K_nc.hi` | 15.92434542298745 | 15.92 | number | 11_supplement_registered_rows.md Table S24 |
| 751 | data/results/c_attr_1112_score/res/COPYBOUND_ov_dev_b_qwen25vl_7b.json | `bound.ii_words.n2.blind_loss.d` | 22.94478926566286 | +22.94 | number | 11_supplement_registered_rows.md Table S24 |
| 752 | data/results/c_attr_1112_score/res/COPYBOUND_ov_dev_b_qwen25vl_7b.json | `bound.ii_words.n2.blind_loss.lo` | 20.93646550397877 | 20.94 | number | 11_supplement_registered_rows.md Table S24 |
| 753 | data/results/c_attr_1112_score/res/COPYBOUND_ov_dev_b_qwen25vl_7b.json | `bound.ii_words.n2.blind_loss.hi` | 24.97104532769559 | 24.97 | number | 11_supplement_registered_rows.md Table S24 |
| 754 | data/results/c_attr_1112_score/res/COPYBOUND_ov_dev_b_qwen25vl_7b.json | `bound.ii_words.n2.K_ret.tier` | "POST HOC" | POST HOC | label | 11_supplement_registered_rows.md Table S24 |
| 755 | data/results/c_attr_1112_score/res/COPYBOUND_ov_dev_b_qwen25vl_7b.json | `bound.ii_words.n3.K_ret.d` | 18.744748958014974 | +18.74 | number | 11_supplement_registered_rows.md Table S24 |
| 756 | data/results/c_attr_1112_score/res/COPYBOUND_ov_dev_b_qwen25vl_7b.json | `bound.ii_words.n3.K_ret.lo` | 16.709541442190336 | 16.71 | number | 11_supplement_registered_rows.md Table S24 |
| 757 | data/results/c_attr_1112_score/res/COPYBOUND_ov_dev_b_qwen25vl_7b.json | `bound.ii_words.n3.K_ret.hi` | 20.841703464971697 | 20.84 | number | 11_supplement_registered_rows.md Table S24 |
| 758 | data/results/c_attr_1112_score/res/COPYBOUND_ov_dev_b_qwen25vl_7b.json | `bound.ii_words.n3.K_ret.label` | "DETECTED" | DETECTED | label | 11_supplement_registered_rows.md Table S24 |
| 759 | data/results/c_attr_1112_score/res/COPYBOUND_ov_dev_b_qwen25vl_7b.json | `bound.ii_words.n3.L_cp.d` | -9.075132208536466 | −9.08 | number | 11_supplement_registered_rows.md Table S24 |
| 760 | data/results/c_attr_1112_score/res/COPYBOUND_ov_dev_b_qwen25vl_7b.json | `bound.ii_words.n3.L_cp.lo` | -10.981918956274114 | −10.98 | number | 11_supplement_registered_rows.md Table S24 |
| 761 | data/results/c_attr_1112_score/res/COPYBOUND_ov_dev_b_qwen25vl_7b.json | `bound.ii_words.n3.L_cp.hi` | -7.218559968005788 | −7.22 | number | 11_supplement_registered_rows.md Table S24 |
| 762 | data/results/c_attr_1112_score/res/COPYBOUND_ov_dev_b_qwen25vl_7b.json | `bound.ii_words.n3.L_cp.label` | "REVERSED" | REVERSED | label | 11_supplement_registered_rows.md Table S24 |
| 763 | data/results/c_attr_1112_score/res/COPYBOUND_ov_dev_b_qwen25vl_7b.json | `bound.ii_words.n3.K_nc.d` | 5.763409396791424 | +5.76 | number | 11_supplement_registered_rows.md Table S24 |
| 764 | data/results/c_attr_1112_score/res/COPYBOUND_ov_dev_b_qwen25vl_7b.json | `bound.ii_words.n3.K_nc.lo` | 4.710411667316011 | 4.71 | number | 11_supplement_registered_rows.md Table S24 |
| 765 | data/results/c_attr_1112_score/res/COPYBOUND_ov_dev_b_qwen25vl_7b.json | `bound.ii_words.n3.K_nc.hi` | 6.946254936929598 | 6.95 | number | 11_supplement_registered_rows.md Table S24 |
| 766 | data/results/c_attr_1112_score/res/COPYBOUND_ov_dev_b_qwen25vl_7b.json | `bound.ii_words.n3.K_nc.label` | "DETECTED" | DETECTED | label | 11_supplement_registered_rows.md Table S24 |
| 767 | data/results/c_attr_1112_score/res/COPYBOUND_ov_dev_b_qwen25vl_7b.json | `bound.ii_words.n3.K_rand.d` | 1.8917202126540622 | +1.89 | number | 11_supplement_registered_rows.md Table S24 |
| 768 | data/results/c_attr_1112_score/res/COPYBOUND_ov_dev_b_qwen25vl_7b.json | `bound.ii_words.n3.K_rand.lo` | 1.380838114926982 | 1.38 | number | 11_supplement_registered_rows.md Table S24 |
| 769 | data/results/c_attr_1112_score/res/COPYBOUND_ov_dev_b_qwen25vl_7b.json | `bound.ii_words.n3.K_rand.hi` | 2.4847033571258357 | 2.48 | number | 11_supplement_registered_rows.md Table S24 |
| 770 | data/results/c_attr_1112_score/res/COPYBOUND_ov_dev_b_qwen25vl_7b.json | `bound.ii_words.n3.K_ret_minus_K_nc.d` | 12.981339561223553 | +12.98 | number | 11_supplement_registered_rows.md Table S24 |
| 771 | data/results/c_attr_1112_score/res/COPYBOUND_ov_dev_b_qwen25vl_7b.json | `bound.ii_words.n3.K_ret_minus_K_nc.lo` | 11.130462616183326 | 11.13 | number | 11_supplement_registered_rows.md Table S24 |
| 772 | data/results/c_attr_1112_score/res/COPYBOUND_ov_dev_b_qwen25vl_7b.json | `bound.ii_words.n3.K_ret_minus_K_nc.hi` | 14.920479719729046 | 14.92 | number | 11_supplement_registered_rows.md Table S24 |
| 773 | data/results/c_attr_1112_score/res/COPYBOUND_ov_dev_b_qwen25vl_7b.json | `bound.ii_words.n3.blind_loss.d` | 19.265091052424175 | +19.27 | number | 11_supplement_registered_rows.md Table S24 |
| 774 | data/results/c_attr_1112_score/res/COPYBOUND_ov_dev_b_qwen25vl_7b.json | `bound.ii_words.n3.blind_loss.lo` | 17.40347635580285 | 17.40 | number | 11_supplement_registered_rows.md Table S24 |
| 775 | data/results/c_attr_1112_score/res/COPYBOUND_ov_dev_b_qwen25vl_7b.json | `bound.ii_words.n3.blind_loss.hi` | 21.17617211985015 | 21.18 | number | 11_supplement_registered_rows.md Table S24 |
| 776 | data/results/c_attr_1112_score/res/COPYBOUND_ov_dev_b_qwen25vl_7b.json | `bound.ii_words.n3.K_ret.tier` | "POST HOC" | POST HOC | label | 11_supplement_registered_rows.md Table S24 |
| 777 | data/results/c_attr_1112_score/res/COPYBOUND_ov_dev_b_qwen25vl_7b.json | `bound.ii_words.n4.K_ret.d` | 13.16330707873851 | +13.16 | number | 11_supplement_registered_rows.md Table S24 |
| 778 | data/results/c_attr_1112_score/res/COPYBOUND_ov_dev_b_qwen25vl_7b.json | `bound.ii_words.n4.K_ret.lo` | 11.396077559615048 | 11.40 | number | 11_supplement_registered_rows.md Table S24 |
| 779 | data/results/c_attr_1112_score/res/COPYBOUND_ov_dev_b_qwen25vl_7b.json | `bound.ii_words.n4.K_ret.hi` | 15.067252156886674 | 15.07 | number | 11_supplement_registered_rows.md Table S24 |
| 780 | data/results/c_attr_1112_score/res/COPYBOUND_ov_dev_b_qwen25vl_7b.json | `bound.ii_words.n4.K_ret.label` | "DETECTED" | DETECTED | label | 11_supplement_registered_rows.md Table S24 |
| 781 | data/results/c_attr_1112_score/res/COPYBOUND_ov_dev_b_qwen25vl_7b.json | `bound.ii_words.n4.L_cp.d` | -3.493690329259999 | −3.49 | number | 11_supplement_registered_rows.md Table S24 |
| 782 | data/results/c_attr_1112_score/res/COPYBOUND_ov_dev_b_qwen25vl_7b.json | `bound.ii_words.n4.L_cp.lo` | -5.348075181464655 | −5.35 | number | 11_supplement_registered_rows.md Table S24 |
| 783 | data/results/c_attr_1112_score/res/COPYBOUND_ov_dev_b_qwen25vl_7b.json | `bound.ii_words.n4.L_cp.hi` | -1.540600180488842 | −1.54 | number | 11_supplement_registered_rows.md Table S24 |
| 784 | data/results/c_attr_1112_score/res/COPYBOUND_ov_dev_b_qwen25vl_7b.json | `bound.ii_words.n4.L_cp.label` | "REVERSED" | REVERSED | label | 11_supplement_registered_rows.md Table S24 |
| 785 | data/results/c_attr_1112_score/res/COPYBOUND_ov_dev_b_qwen25vl_7b.json | `bound.ii_words.n4.K_nc.d` | 2.8914854829479113 | +2.89 | number | 11_supplement_registered_rows.md Table S24 |
| 786 | data/results/c_attr_1112_score/res/COPYBOUND_ov_dev_b_qwen25vl_7b.json | `bound.ii_words.n4.K_nc.lo` | 2.074174669136092 | 2.07 | number | 11_supplement_registered_rows.md Table S24 |
| 787 | data/results/c_attr_1112_score/res/COPYBOUND_ov_dev_b_qwen25vl_7b.json | `bound.ii_words.n4.K_nc.hi` | 3.7928414285533223 | 3.79 | number | 11_supplement_registered_rows.md Table S24 |
| 788 | data/results/c_attr_1112_score/res/COPYBOUND_ov_dev_b_qwen25vl_7b.json | `bound.ii_words.n4.K_nc.label` | "DETECTED" | DETECTED | label | 11_supplement_registered_rows.md Table S24 |
| 789 | data/results/c_attr_1112_score/res/COPYBOUND_ov_dev_b_qwen25vl_7b.json | `bound.ii_words.n4.K_rand.d` | 0.8449095105615779 | +0.84 | number | 11_supplement_registered_rows.md Table S24 |
| 790 | data/results/c_attr_1112_score/res/COPYBOUND_ov_dev_b_qwen25vl_7b.json | `bound.ii_words.n4.K_rand.lo` | 0.5037958205746846 | 0.50 | number | 11_supplement_registered_rows.md Table S24 |
| 791 | data/results/c_attr_1112_score/res/COPYBOUND_ov_dev_b_qwen25vl_7b.json | `bound.ii_words.n4.K_rand.hi` | 1.224517892204566 | 1.22 | number | 11_supplement_registered_rows.md Table S24 |
| 792 | data/results/c_attr_1112_score/res/COPYBOUND_ov_dev_b_qwen25vl_7b.json | `bound.ii_words.n4.K_ret_minus_K_nc.d` | 10.2718215957906 | +10.27 | number | 11_supplement_registered_rows.md Table S24 |
| 793 | data/results/c_attr_1112_score/res/COPYBOUND_ov_dev_b_qwen25vl_7b.json | `bound.ii_words.n4.K_ret_minus_K_nc.lo` | 8.618829353134016 | 8.62 | number | 11_supplement_registered_rows.md Table S24 |
| 794 | data/results/c_attr_1112_score/res/COPYBOUND_ov_dev_b_qwen25vl_7b.json | `bound.ii_words.n4.K_ret_minus_K_nc.hi` | 12.023002336395509 | 12.02 | number | 11_supplement_registered_rows.md Table S24 |
| 795 | data/results/c_attr_1112_score/res/COPYBOUND_ov_dev_b_qwen25vl_7b.json | `bound.ii_words.n4.blind_loss.d` | 14.872392279489782 | +14.87 | number | 11_supplement_registered_rows.md Table S24 |
| 796 | data/results/c_attr_1112_score/res/COPYBOUND_ov_dev_b_qwen25vl_7b.json | `bound.ii_words.n4.blind_loss.lo` | 13.167581593540032 | 13.17 | number | 11_supplement_registered_rows.md Table S24 |
| 797 | data/results/c_attr_1112_score/res/COPYBOUND_ov_dev_b_qwen25vl_7b.json | `bound.ii_words.n4.blind_loss.hi` | 16.699250970933996 | 16.70 | number | 11_supplement_registered_rows.md Table S24 |
| 798 | data/results/c_attr_1112_score/res/COPYBOUND_ov_dev_b_qwen25vl_7b.json | `bound.ii_words.n4.K_ret.tier` | "POST HOC" | POST HOC | label | 11_supplement_registered_rows.md Table S24 |
| 799 | data/results/c_attr_1112_score/res/COPYBOUND_ov_dev_b_internvl3_8b.json | `bound.i_syllables.n2.K_ret.d` | 12.492112008597351 | +12.49 | number | 11_supplement_registered_rows.md Table S24 |
| 800 | data/results/c_attr_1112_score/res/COPYBOUND_ov_dev_b_internvl3_8b.json | `bound.i_syllables.n2.K_ret.lo` | 10.852945451324088 | 10.85 | number | 11_supplement_registered_rows.md Table S24 |
| 801 | data/results/c_attr_1112_score/res/COPYBOUND_ov_dev_b_internvl3_8b.json | `bound.i_syllables.n2.K_ret.hi` | 14.221371622445831 | 14.22 | number | 11_supplement_registered_rows.md Table S24 |
| 802 | data/results/c_attr_1112_score/res/COPYBOUND_ov_dev_b_internvl3_8b.json | `bound.i_syllables.n2.K_ret.label` | "DETECTED" | DETECTED | label | 11_supplement_registered_rows.md Table S24 |
| 803 | data/results/c_attr_1112_score/res/COPYBOUND_ov_dev_b_internvl3_8b.json | `bound.i_syllables.n2.L_cp.d` | -7.135680099007221 | −7.14 | number | 11_supplement_registered_rows.md Table S24 |
| 804 | data/results/c_attr_1112_score/res/COPYBOUND_ov_dev_b_internvl3_8b.json | `bound.i_syllables.n2.L_cp.lo` | -8.818606133625323 | −8.82 | number | 11_supplement_registered_rows.md Table S24 |
| 805 | data/results/c_attr_1112_score/res/COPYBOUND_ov_dev_b_internvl3_8b.json | `bound.i_syllables.n2.L_cp.hi` | -5.474965641653122 | −5.47 | number | 11_supplement_registered_rows.md Table S24 |
| 806 | data/results/c_attr_1112_score/res/COPYBOUND_ov_dev_b_internvl3_8b.json | `bound.i_syllables.n2.L_cp.label` | "REVERSED" | REVERSED | label | 11_supplement_registered_rows.md Table S24 |
| 807 | data/results/c_attr_1112_score/res/COPYBOUND_ov_dev_b_internvl3_8b.json | `bound.i_syllables.n2.K_nc.d` | 4.099370436023604 | +4.10 | number | 11_supplement_registered_rows.md Table S24 |
| 808 | data/results/c_attr_1112_score/res/COPYBOUND_ov_dev_b_internvl3_8b.json | `bound.i_syllables.n2.K_nc.lo` | 2.8680724001646647 | 2.87 | number | 11_supplement_registered_rows.md Table S24 |
| 809 | data/results/c_attr_1112_score/res/COPYBOUND_ov_dev_b_internvl3_8b.json | `bound.i_syllables.n2.K_nc.hi` | 5.405270199506312 | 5.41 | number | 11_supplement_registered_rows.md Table S24 |
| 810 | data/results/c_attr_1112_score/res/COPYBOUND_ov_dev_b_internvl3_8b.json | `bound.i_syllables.n2.K_nc.label` | "DETECTED" | DETECTED | label | 11_supplement_registered_rows.md Table S24 |
| 811 | data/results/c_attr_1112_score/res/COPYBOUND_ov_dev_b_internvl3_8b.json | `bound.i_syllables.n2.K_rand.d` | 1.3707563806556058 | +1.37 | number | 11_supplement_registered_rows.md Table S24 |
| 812 | data/results/c_attr_1112_score/res/COPYBOUND_ov_dev_b_internvl3_8b.json | `bound.i_syllables.n2.K_rand.lo` | 0.7472468326532646 | 0.75 | number | 11_supplement_registered_rows.md Table S24 |
| 813 | data/results/c_attr_1112_score/res/COPYBOUND_ov_dev_b_internvl3_8b.json | `bound.i_syllables.n2.K_rand.hi` | 1.966253769283786 | 1.97 | number | 11_supplement_registered_rows.md Table S24 |
| 814 | data/results/c_attr_1112_score/res/COPYBOUND_ov_dev_b_internvl3_8b.json | `bound.i_syllables.n2.K_ret_minus_K_nc.d` | 8.392741572573746 | +8.39 | number | 11_supplement_registered_rows.md Table S24 |
| 815 | data/results/c_attr_1112_score/res/COPYBOUND_ov_dev_b_internvl3_8b.json | `bound.i_syllables.n2.K_ret_minus_K_nc.lo` | 6.718817051459844 | 6.72 | number | 11_supplement_registered_rows.md Table S24 |
| 816 | data/results/c_attr_1112_score/res/COPYBOUND_ov_dev_b_internvl3_8b.json | `bound.i_syllables.n2.K_ret_minus_K_nc.hi` | 9.998858236289385 | 10.00 | number | 11_supplement_registered_rows.md Table S24 |
| 817 | data/results/c_attr_1112_score/res/COPYBOUND_ov_dev_b_internvl3_8b.json | `bound.i_syllables.n2.blind_loss.d` | 18.56306179279743 | +18.56 | number | 11_supplement_registered_rows.md Table S24 |
| 818 | data/results/c_attr_1112_score/res/COPYBOUND_ov_dev_b_internvl3_8b.json | `bound.i_syllables.n2.blind_loss.lo` | 16.939673304237562 | 16.94 | number | 11_supplement_registered_rows.md Table S24 |
| 819 | data/results/c_attr_1112_score/res/COPYBOUND_ov_dev_b_internvl3_8b.json | `bound.i_syllables.n2.blind_loss.hi` | 20.209941970011933 | 20.21 | number | 11_supplement_registered_rows.md Table S24 |
| 820 | data/results/c_attr_1112_score/res/COPYBOUND_ov_dev_b_internvl3_8b.json | `bound.i_syllables.n2.K_ret.tier` | "POST HOC" | POST HOC | label | 11_supplement_registered_rows.md Table S24 |
| 821 | data/results/c_attr_1112_score/res/COPYBOUND_ov_dev_b_internvl3_8b.json | `bound.i_syllables.n3.K_ret.d` | 9.930191644911444 | +9.93 | number | 11_supplement_registered_rows.md Table S24 |
| 822 | data/results/c_attr_1112_score/res/COPYBOUND_ov_dev_b_internvl3_8b.json | `bound.i_syllables.n3.K_ret.lo` | 8.3114443484374 | 8.31 | number | 11_supplement_registered_rows.md Table S24 |
| 823 | data/results/c_attr_1112_score/res/COPYBOUND_ov_dev_b_internvl3_8b.json | `bound.i_syllables.n3.K_ret.hi` | 11.599691381171834 | 11.60 | number | 11_supplement_registered_rows.md Table S24 |
| 824 | data/results/c_attr_1112_score/res/COPYBOUND_ov_dev_b_internvl3_8b.json | `bound.i_syllables.n3.K_ret.label` | "DETECTED" | DETECTED | label | 11_supplement_registered_rows.md Table S24 |
| 825 | data/results/c_attr_1112_score/res/COPYBOUND_ov_dev_b_internvl3_8b.json | `bound.i_syllables.n3.L_cp.d` | -4.573759735321315 | −4.57 | number | 11_supplement_registered_rows.md Table S24 |
| 826 | data/results/c_attr_1112_score/res/COPYBOUND_ov_dev_b_internvl3_8b.json | `bound.i_syllables.n3.L_cp.lo` | -6.4621888546336175 | −6.46 | number | 11_supplement_registered_rows.md Table S24 |
| 827 | data/results/c_attr_1112_score/res/COPYBOUND_ov_dev_b_internvl3_8b.json | `bound.i_syllables.n3.L_cp.hi` | -2.611113435330269 | −2.61 | number | 11_supplement_registered_rows.md Table S24 |
| 828 | data/results/c_attr_1112_score/res/COPYBOUND_ov_dev_b_internvl3_8b.json | `bound.i_syllables.n3.L_cp.label` | "REVERSED" | REVERSED | label | 11_supplement_registered_rows.md Table S24 |
| 829 | data/results/c_attr_1112_score/res/COPYBOUND_ov_dev_b_internvl3_8b.json | `bound.i_syllables.n3.K_nc.d` | 2.6512390611780208 | +2.65 | number | 11_supplement_registered_rows.md Table S24 |
| 830 | data/results/c_attr_1112_score/res/COPYBOUND_ov_dev_b_internvl3_8b.json | `bound.i_syllables.n3.K_nc.lo` | 1.6056779017737755 | 1.61 | number | 11_supplement_registered_rows.md Table S24 |
| 831 | data/results/c_attr_1112_score/res/COPYBOUND_ov_dev_b_internvl3_8b.json | `bound.i_syllables.n3.K_nc.hi` | 3.7564925870071915 | 3.76 | number | 11_supplement_registered_rows.md Table S24 |
| 832 | data/results/c_attr_1112_score/res/COPYBOUND_ov_dev_b_internvl3_8b.json | `bound.i_syllables.n3.K_nc.label` | "DETECTED" | DETECTED | label | 11_supplement_registered_rows.md Table S24 |
| 833 | data/results/c_attr_1112_score/res/COPYBOUND_ov_dev_b_internvl3_8b.json | `bound.i_syllables.n3.K_rand.d` | 0.24914618065103103 | +0.25 | number | 11_supplement_registered_rows.md Table S24 |
| 834 | data/results/c_attr_1112_score/res/COPYBOUND_ov_dev_b_internvl3_8b.json | `bound.i_syllables.n3.K_rand.lo` | -0.07484912791725326 | −0.07 | number | 11_supplement_registered_rows.md Table S24 |
| 835 | data/results/c_attr_1112_score/res/COPYBOUND_ov_dev_b_internvl3_8b.json | `bound.i_syllables.n3.K_rand.hi` | 0.5913116569012556 | 0.59 | number | 11_supplement_registered_rows.md Table S24 |
| 836 | data/results/c_attr_1112_score/res/COPYBOUND_ov_dev_b_internvl3_8b.json | `bound.i_syllables.n3.K_ret_minus_K_nc.d` | 7.278952583733424 | +7.28 | number | 11_supplement_registered_rows.md Table S24 |
| 837 | data/results/c_attr_1112_score/res/COPYBOUND_ov_dev_b_internvl3_8b.json | `bound.i_syllables.n3.K_ret_minus_K_nc.lo` | 5.772035737548404 | 5.77 | number | 11_supplement_registered_rows.md Table S24 |
| 838 | data/results/c_attr_1112_score/res/COPYBOUND_ov_dev_b_internvl3_8b.json | `bound.i_syllables.n3.K_ret_minus_K_nc.hi` | 8.831172406629902 | 8.83 | number | 11_supplement_registered_rows.md Table S24 |
| 839 | data/results/c_attr_1112_score/res/COPYBOUND_ov_dev_b_internvl3_8b.json | `bound.i_syllables.n3.blind_loss.d` | 14.207319095145248 | +14.21 | number | 11_supplement_registered_rows.md Table S24 |
| 840 | data/results/c_attr_1112_score/res/COPYBOUND_ov_dev_b_internvl3_8b.json | `bound.i_syllables.n3.blind_loss.lo` | 12.588047287861984 | 12.59 | number | 11_supplement_registered_rows.md Table S24 |
| 841 | data/results/c_attr_1112_score/res/COPYBOUND_ov_dev_b_internvl3_8b.json | `bound.i_syllables.n3.blind_loss.hi` | 15.827926196889749 | 15.83 | number | 11_supplement_registered_rows.md Table S24 |
| 842 | data/results/c_attr_1112_score/res/COPYBOUND_ov_dev_b_internvl3_8b.json | `bound.i_syllables.n3.K_ret.tier` | "POST HOC" | POST HOC | label | 11_supplement_registered_rows.md Table S24 |
| 843 | data/results/c_attr_1112_score/res/COPYBOUND_ov_dev_b_internvl3_8b.json | `bound.i_syllables.n4.K_ret.d` | 7.371576064146204 | +7.37 | number | 11_supplement_registered_rows.md Table S24 |
| 844 | data/results/c_attr_1112_score/res/COPYBOUND_ov_dev_b_internvl3_8b.json | `bound.i_syllables.n4.K_ret.lo` | 5.96432495603297 | 5.96 | number | 11_supplement_registered_rows.md Table S24 |
| 845 | data/results/c_attr_1112_score/res/COPYBOUND_ov_dev_b_internvl3_8b.json | `bound.i_syllables.n4.K_ret.hi` | 8.813577007438145 | 8.81 | number | 11_supplement_registered_rows.md Table S24 |
| 846 | data/results/c_attr_1112_score/res/COPYBOUND_ov_dev_b_internvl3_8b.json | `bound.i_syllables.n4.K_ret.label` | "DETECTED" | DETECTED | label | 11_supplement_registered_rows.md Table S24 |
| 847 | data/results/c_attr_1112_score/res/COPYBOUND_ov_dev_b_internvl3_8b.json | `bound.i_syllables.n4.L_cp.d` | -2.015144154556074 | −2.02 | number | 11_supplement_registered_rows.md Table S24 |
| 848 | data/results/c_attr_1112_score/res/COPYBOUND_ov_dev_b_internvl3_8b.json | `bound.i_syllables.n4.L_cp.lo` | -3.8965222524608736 | −3.90 | number | 11_supplement_registered_rows.md Table S24 |
| 849 | data/results/c_attr_1112_score/res/COPYBOUND_ov_dev_b_internvl3_8b.json | `bound.i_syllables.n4.L_cp.hi` | -0.0846585809846125 | −0.08 | number | 11_supplement_registered_rows.md Table S24 |
| 850 | data/results/c_attr_1112_score/res/COPYBOUND_ov_dev_b_internvl3_8b.json | `bound.i_syllables.n4.L_cp.label` | "REVERSED" | REVERSED | label | 11_supplement_registered_rows.md Table S24 |
| 851 | data/results/c_attr_1112_score/res/COPYBOUND_ov_dev_b_internvl3_8b.json | `bound.i_syllables.n4.K_nc.d` | 2.297472731880234 | +2.30 | number | 11_supplement_registered_rows.md Table S24 |
| 852 | data/results/c_attr_1112_score/res/COPYBOUND_ov_dev_b_internvl3_8b.json | `bound.i_syllables.n4.K_nc.lo` | 1.5502985088026762 | 1.55 | number | 11_supplement_registered_rows.md Table S24 |
| 853 | data/results/c_attr_1112_score/res/COPYBOUND_ov_dev_b_internvl3_8b.json | `bound.i_syllables.n4.K_nc.hi` | 3.102588220018188 | 3.10 | number | 11_supplement_registered_rows.md Table S24 |
| 854 | data/results/c_attr_1112_score/res/COPYBOUND_ov_dev_b_internvl3_8b.json | `bound.i_syllables.n4.K_nc.label` | "DETECTED" | DETECTED | label | 11_supplement_registered_rows.md Table S24 |
| 855 | data/results/c_attr_1112_score/res/COPYBOUND_ov_dev_b_internvl3_8b.json | `bound.i_syllables.n4.K_rand.d` | 0.31922282375053646 | +0.32 | number | 11_supplement_registered_rows.md Table S24 |
| 856 | data/results/c_attr_1112_score/res/COPYBOUND_ov_dev_b_internvl3_8b.json | `bound.i_syllables.n4.K_rand.lo` | 0.06967716617289306 | 0.07 | number | 11_supplement_registered_rows.md Table S24 |
| 857 | data/results/c_attr_1112_score/res/COPYBOUND_ov_dev_b_internvl3_8b.json | `bound.i_syllables.n4.K_rand.hi` | 0.5882569049158415 | 0.59 | number | 11_supplement_registered_rows.md Table S24 |
| 858 | data/results/c_attr_1112_score/res/COPYBOUND_ov_dev_b_internvl3_8b.json | `bound.i_syllables.n4.K_ret_minus_K_nc.d` | 5.074103332265969 | +5.07 | number | 11_supplement_registered_rows.md Table S24 |
| 859 | data/results/c_attr_1112_score/res/COPYBOUND_ov_dev_b_internvl3_8b.json | `bound.i_syllables.n4.K_ret_minus_K_nc.lo` | 3.802993691754735 | 3.80 | number | 11_supplement_registered_rows.md Table S24 |
| 860 | data/results/c_attr_1112_score/res/COPYBOUND_ov_dev_b_internvl3_8b.json | `bound.i_syllables.n4.K_ret_minus_K_nc.hi` | 6.367258262349236 | 6.37 | number | 11_supplement_registered_rows.md Table S24 |
| 861 | data/results/c_attr_1112_score/res/COPYBOUND_ov_dev_b_internvl3_8b.json | `bound.i_syllables.n4.blind_loss.d` | 9.821579830668577 | +9.82 | number | 11_supplement_registered_rows.md Table S24 |
| 862 | data/results/c_attr_1112_score/res/COPYBOUND_ov_dev_b_internvl3_8b.json | `bound.i_syllables.n4.blind_loss.lo` | 8.37823016796241 | 8.38 | number | 11_supplement_registered_rows.md Table S24 |
| 863 | data/results/c_attr_1112_score/res/COPYBOUND_ov_dev_b_internvl3_8b.json | `bound.i_syllables.n4.blind_loss.hi` | 11.275741843844658 | 11.28 | number | 11_supplement_registered_rows.md Table S24 |
| 864 | data/results/c_attr_1112_score/res/COPYBOUND_ov_dev_b_internvl3_8b.json | `bound.i_syllables.n4.K_ret.tier` | "POST HOC" | POST HOC | label | 11_supplement_registered_rows.md Table S24 |
| 865 | data/results/c_attr_1112_score/res/COPYBOUND_ov_dev_b_internvl3_8b.json | `bound.ii_words.n2.K_ret.d` | 12.281085768681049 | +12.28 | number | 11_supplement_registered_rows.md Table S24 |
| 866 | data/results/c_attr_1112_score/res/COPYBOUND_ov_dev_b_internvl3_8b.json | `bound.ii_words.n2.K_ret.lo` | 10.597351213149935 | 10.60 | number | 11_supplement_registered_rows.md Table S24 |
| 867 | data/results/c_attr_1112_score/res/COPYBOUND_ov_dev_b_internvl3_8b.json | `bound.ii_words.n2.K_ret.hi` | 14.025548730031627 | 14.03 | number | 11_supplement_registered_rows.md Table S24 |
| 868 | data/results/c_attr_1112_score/res/COPYBOUND_ov_dev_b_internvl3_8b.json | `bound.ii_words.n2.K_ret.label` | "DETECTED" | DETECTED | label | 11_supplement_registered_rows.md Table S24 |
| 869 | data/results/c_attr_1112_score/res/COPYBOUND_ov_dev_b_internvl3_8b.json | `bound.ii_words.n2.L_cp.d` | -6.9246538590909195 | −6.92 | number | 11_supplement_registered_rows.md Table S24 |
| 870 | data/results/c_attr_1112_score/res/COPYBOUND_ov_dev_b_internvl3_8b.json | `bound.ii_words.n2.L_cp.lo` | -8.650936643080854 | −8.65 | number | 11_supplement_registered_rows.md Table S24 |
| 871 | data/results/c_attr_1112_score/res/COPYBOUND_ov_dev_b_internvl3_8b.json | `bound.ii_words.n2.L_cp.hi` | -5.2385625987777455 | −5.24 | number | 11_supplement_registered_rows.md Table S24 |
| 872 | data/results/c_attr_1112_score/res/COPYBOUND_ov_dev_b_internvl3_8b.json | `bound.ii_words.n2.L_cp.label` | "REVERSED" | REVERSED | label | 11_supplement_registered_rows.md Table S24 |
| 873 | data/results/c_attr_1112_score/res/COPYBOUND_ov_dev_b_internvl3_8b.json | `bound.ii_words.n2.K_nc.d` | 3.319493805015673 | +3.32 | number | 11_supplement_registered_rows.md Table S24 |
| 874 | data/results/c_attr_1112_score/res/COPYBOUND_ov_dev_b_internvl3_8b.json | `bound.ii_words.n2.K_nc.lo` | 2.1436422559517307 | 2.14 | number | 11_supplement_registered_rows.md Table S24 |
| 875 | data/results/c_attr_1112_score/res/COPYBOUND_ov_dev_b_internvl3_8b.json | `bound.ii_words.n2.K_nc.hi` | 4.595887565147858 | 4.60 | number | 11_supplement_registered_rows.md Table S24 |
| 876 | data/results/c_attr_1112_score/res/COPYBOUND_ov_dev_b_internvl3_8b.json | `bound.ii_words.n2.K_nc.label` | "DETECTED" | DETECTED | label | 11_supplement_registered_rows.md Table S24 |
| 877 | data/results/c_attr_1112_score/res/COPYBOUND_ov_dev_b_internvl3_8b.json | `bound.ii_words.n2.K_rand.d` | 0.9549248402126665 | +0.95 | number | 11_supplement_registered_rows.md Table S24 |
| 878 | data/results/c_attr_1112_score/res/COPYBOUND_ov_dev_b_internvl3_8b.json | `bound.ii_words.n2.K_rand.lo` | 0.42137334644482644 | 0.42 | number | 11_supplement_registered_rows.md Table S24 |
| 879 | data/results/c_attr_1112_score/res/COPYBOUND_ov_dev_b_internvl3_8b.json | `bound.ii_words.n2.K_rand.hi` | 1.4984555559619859 | 1.50 | number | 11_supplement_registered_rows.md Table S24 |
| 880 | data/results/c_attr_1112_score/res/COPYBOUND_ov_dev_b_internvl3_8b.json | `bound.ii_words.n2.K_ret_minus_K_nc.d` | 8.961591963665377 | +8.96 | number | 11_supplement_registered_rows.md Table S24 |
| 881 | data/results/c_attr_1112_score/res/COPYBOUND_ov_dev_b_internvl3_8b.json | `bound.ii_words.n2.K_ret_minus_K_nc.lo` | 7.334724497232327 | 7.33 | number | 11_supplement_registered_rows.md Table S24 |
| 882 | data/results/c_attr_1112_score/res/COPYBOUND_ov_dev_b_internvl3_8b.json | `bound.ii_words.n2.K_ret_minus_K_nc.hi` | 10.560399337873816 | 10.56 | number | 11_supplement_registered_rows.md Table S24 |
| 883 | data/results/c_attr_1112_score/res/COPYBOUND_ov_dev_b_internvl3_8b.json | `bound.ii_words.n2.blind_loss.d` | 17.722288929049714 | +17.72 | number | 11_supplement_registered_rows.md Table S24 |
| 884 | data/results/c_attr_1112_score/res/COPYBOUND_ov_dev_b_internvl3_8b.json | `bound.ii_words.n2.blind_loss.lo` | 16.128920477674296 | 16.13 | number | 11_supplement_registered_rows.md Table S24 |
| 885 | data/results/c_attr_1112_score/res/COPYBOUND_ov_dev_b_internvl3_8b.json | `bound.ii_words.n2.blind_loss.hi` | 19.328471847724355 | 19.33 | number | 11_supplement_registered_rows.md Table S24 |
| 886 | data/results/c_attr_1112_score/res/COPYBOUND_ov_dev_b_internvl3_8b.json | `bound.ii_words.n2.K_ret.tier` | "POST HOC" | POST HOC | label | 11_supplement_registered_rows.md Table S24 |
| 887 | data/results/c_attr_1112_score/res/COPYBOUND_ov_dev_b_internvl3_8b.json | `bound.ii_words.n3.K_ret.d` | 8.99277629645961 | +8.99 | number | 11_supplement_registered_rows.md Table S24 |
| 888 | data/results/c_attr_1112_score/res/COPYBOUND_ov_dev_b_internvl3_8b.json | `bound.ii_words.n3.K_ret.lo` | 7.483059970757614 | 7.48 | number | 11_supplement_registered_rows.md Table S24 |
| 889 | data/results/c_attr_1112_score/res/COPYBOUND_ov_dev_b_internvl3_8b.json | `bound.ii_words.n3.K_ret.hi` | 10.574427316745426 | 10.57 | number | 11_supplement_registered_rows.md Table S24 |
| 890 | data/results/c_attr_1112_score/res/COPYBOUND_ov_dev_b_internvl3_8b.json | `bound.ii_words.n3.K_ret.label` | "DETECTED" | DETECTED | label | 11_supplement_registered_rows.md Table S24 |
| 891 | data/results/c_attr_1112_score/res/COPYBOUND_ov_dev_b_internvl3_8b.json | `bound.ii_words.n3.L_cp.d` | -3.6363443868694802 | −3.64 | number | 11_supplement_registered_rows.md Table S24 |
| 892 | data/results/c_attr_1112_score/res/COPYBOUND_ov_dev_b_internvl3_8b.json | `bound.ii_words.n3.L_cp.lo` | -5.550854071186638 | −5.55 | number | 11_supplement_registered_rows.md Table S24 |
| 893 | data/results/c_attr_1112_score/res/COPYBOUND_ov_dev_b_internvl3_8b.json | `bound.ii_words.n3.L_cp.hi` | -1.6886715001354877 | −1.69 | number | 11_supplement_registered_rows.md Table S24 |
| 894 | data/results/c_attr_1112_score/res/COPYBOUND_ov_dev_b_internvl3_8b.json | `bound.ii_words.n3.L_cp.label` | "REVERSED" | REVERSED | label | 11_supplement_registered_rows.md Table S24 |
| 895 | data/results/c_attr_1112_score/res/COPYBOUND_ov_dev_b_internvl3_8b.json | `bound.ii_words.n3.K_nc.d` | 2.9136053661161374 | +2.91 | number | 11_supplement_registered_rows.md Table S24 |
| 896 | data/results/c_attr_1112_score/res/COPYBOUND_ov_dev_b_internvl3_8b.json | `bound.ii_words.n3.K_nc.lo` | 1.879252971984675 | 1.88 | number | 11_supplement_registered_rows.md Table S24 |
| 897 | data/results/c_attr_1112_score/res/COPYBOUND_ov_dev_b_internvl3_8b.json | `bound.ii_words.n3.K_nc.hi` | 3.9356815288159694 | 3.94 | number | 11_supplement_registered_rows.md Table S24 |
| 898 | data/results/c_attr_1112_score/res/COPYBOUND_ov_dev_b_internvl3_8b.json | `bound.ii_words.n3.K_nc.label` | "DETECTED" | DETECTED | label | 11_supplement_registered_rows.md Table S24 |
| 899 | data/results/c_attr_1112_score/res/COPYBOUND_ov_dev_b_internvl3_8b.json | `bound.ii_words.n3.K_rand.d` | 0.33399443766987663 | +0.33 | number | 11_supplement_registered_rows.md Table S24 |
| 900 | data/results/c_attr_1112_score/res/COPYBOUND_ov_dev_b_internvl3_8b.json | `bound.ii_words.n3.K_rand.lo` | 0.04408247390290005 | 0.04 | number | 11_supplement_registered_rows.md Table S24 |
| 901 | data/results/c_attr_1112_score/res/COPYBOUND_ov_dev_b_internvl3_8b.json | `bound.ii_words.n3.K_rand.hi` | 0.6367806739471628 | 0.64 | number | 11_supplement_registered_rows.md Table S24 |
| 902 | data/results/c_attr_1112_score/res/COPYBOUND_ov_dev_b_internvl3_8b.json | `bound.ii_words.n3.K_ret_minus_K_nc.d` | 6.079170930343474 | +6.08 | number | 11_supplement_registered_rows.md Table S24 |
| 903 | data/results/c_attr_1112_score/res/COPYBOUND_ov_dev_b_internvl3_8b.json | `bound.ii_words.n3.K_ret_minus_K_nc.lo` | 4.715992644856046 | 4.72 | number | 11_supplement_registered_rows.md Table S24 |
| 904 | data/results/c_attr_1112_score/res/COPYBOUND_ov_dev_b_internvl3_8b.json | `bound.ii_words.n3.K_ret_minus_K_nc.hi` | 7.479701039824079 | 7.48 | number | 11_supplement_registered_rows.md Table S24 |
| 905 | data/results/c_attr_1112_score/res/COPYBOUND_ov_dev_b_internvl3_8b.json | `bound.ii_words.n3.blind_loss.d` | 13.192999025695292 | +13.19 | number | 11_supplement_registered_rows.md Table S24 |
| 906 | data/results/c_attr_1112_score/res/COPYBOUND_ov_dev_b_internvl3_8b.json | `bound.ii_words.n3.blind_loss.lo` | 11.643429165871389 | 11.64 | number | 11_supplement_registered_rows.md Table S24 |
| 907 | data/results/c_attr_1112_score/res/COPYBOUND_ov_dev_b_internvl3_8b.json | `bound.ii_words.n3.blind_loss.hi` | 14.758452756355844 | 14.76 | number | 11_supplement_registered_rows.md Table S24 |
| 908 | data/results/c_attr_1112_score/res/COPYBOUND_ov_dev_b_internvl3_8b.json | `bound.ii_words.n3.K_ret.tier` | "POST HOC" | POST HOC | label | 11_supplement_registered_rows.md Table S24 |
| 909 | data/results/c_attr_1112_score/res/COPYBOUND_ov_dev_b_internvl3_8b.json | `bound.ii_words.n4.K_ret.d` | 5.8786087911917315 | +5.88 | number | 11_supplement_registered_rows.md Table S24 |
| 910 | data/results/c_attr_1112_score/res/COPYBOUND_ov_dev_b_internvl3_8b.json | `bound.ii_words.n4.K_ret.lo` | 4.572379690974512 | 4.57 | number | 11_supplement_registered_rows.md Table S24 |
| 911 | data/results/c_attr_1112_score/res/COPYBOUND_ov_dev_b_internvl3_8b.json | `bound.ii_words.n4.K_ret.hi` | 7.258841259835504 | 7.26 | number | 11_supplement_registered_rows.md Table S24 |
| 912 | data/results/c_attr_1112_score/res/COPYBOUND_ov_dev_b_internvl3_8b.json | `bound.ii_words.n4.K_ret.label` | "DETECTED" | DETECTED | label | 11_supplement_registered_rows.md Table S24 |
| 913 | data/results/c_attr_1112_score/res/COPYBOUND_ov_dev_b_internvl3_8b.json | `bound.ii_words.n4.L_cp.d` | -0.5221768816016019 | −0.52 | number | 11_supplement_registered_rows.md Table S24 |
| 914 | data/results/c_attr_1112_score/res/COPYBOUND_ov_dev_b_internvl3_8b.json | `bound.ii_words.n4.L_cp.lo` | -2.3850148637471476 | −2.39 | number | 11_supplement_registered_rows.md Table S24 |
| 915 | data/results/c_attr_1112_score/res/COPYBOUND_ov_dev_b_internvl3_8b.json | `bound.ii_words.n4.L_cp.hi` | 1.423858185592611 | 1.42 | number | 11_supplement_registered_rows.md Table S24 |
| 916 | data/results/c_attr_1112_score/res/COPYBOUND_ov_dev_b_internvl3_8b.json | `bound.ii_words.n4.L_cp.label` | "UNRESOLVED" | UNRESOLVED | label | 11_supplement_registered_rows.md Table S24 |
| 917 | data/results/c_attr_1112_score/res/COPYBOUND_ov_dev_b_internvl3_8b.json | `bound.ii_words.n4.K_nc.d` | 1.7074507828045244 | +1.71 | number | 11_supplement_registered_rows.md Table S24 |
| 918 | data/results/c_attr_1112_score/res/COPYBOUND_ov_dev_b_internvl3_8b.json | `bound.ii_words.n4.K_nc.lo` | 1.0000767770651973 | 1.00 | number | 11_supplement_registered_rows.md Table S24 |
| 919 | data/results/c_attr_1112_score/res/COPYBOUND_ov_dev_b_internvl3_8b.json | `bound.ii_words.n4.K_nc.hi` | 2.4879367572358873 | 2.49 | number | 11_supplement_registered_rows.md Table S24 |
| 920 | data/results/c_attr_1112_score/res/COPYBOUND_ov_dev_b_internvl3_8b.json | `bound.ii_words.n4.K_nc.label` | "UNRESOLVED" | UNRESOLVED | label | 11_supplement_registered_rows.md Table S24 |
| 921 | data/results/c_attr_1112_score/res/COPYBOUND_ov_dev_b_internvl3_8b.json | `bound.ii_words.n4.K_rand.d` | 0.19959447807947026 | +0.20 | number | 11_supplement_registered_rows.md Table S24 |
| 922 | data/results/c_attr_1112_score/res/COPYBOUND_ov_dev_b_internvl3_8b.json | `bound.ii_words.n4.K_rand.lo` | 0.057381033933476565 | 0.06 | number | 11_supplement_registered_rows.md Table S24 |
| 923 | data/results/c_attr_1112_score/res/COPYBOUND_ov_dev_b_internvl3_8b.json | `bound.ii_words.n4.K_rand.hi` | 0.35426708514900473 | 0.35 | number | 11_supplement_registered_rows.md Table S24 |
| 924 | data/results/c_attr_1112_score/res/COPYBOUND_ov_dev_b_internvl3_8b.json | `bound.ii_words.n4.K_ret_minus_K_nc.d` | 4.1711580083872075 | +4.17 | number | 11_supplement_registered_rows.md Table S24 |
| 925 | data/results/c_attr_1112_score/res/COPYBOUND_ov_dev_b_internvl3_8b.json | `bound.ii_words.n4.K_ret_minus_K_nc.lo` | 3.0608864701016314 | 3.06 | number | 11_supplement_registered_rows.md Table S24 |
| 926 | data/results/c_attr_1112_score/res/COPYBOUND_ov_dev_b_internvl3_8b.json | `bound.ii_words.n4.K_ret_minus_K_nc.hi` | 5.338132867151114 | 5.34 | number | 11_supplement_registered_rows.md Table S24 |
| 927 | data/results/c_attr_1112_score/res/COPYBOUND_ov_dev_b_internvl3_8b.json | `bound.ii_words.n4.blind_loss.d` | 8.53173904054515 | +8.53 | number | 11_supplement_registered_rows.md Table S24 |
| 928 | data/results/c_attr_1112_score/res/COPYBOUND_ov_dev_b_internvl3_8b.json | `bound.ii_words.n4.blind_loss.lo` | 7.124882144727961 | 7.12 | number | 11_supplement_registered_rows.md Table S24 |
| 929 | data/results/c_attr_1112_score/res/COPYBOUND_ov_dev_b_internvl3_8b.json | `bound.ii_words.n4.blind_loss.hi` | 9.918670056594754 | 9.92 | number | 11_supplement_registered_rows.md Table S24 |
| 930 | data/results/c_attr_1112_score/res/COPYBOUND_ov_dev_b_internvl3_8b.json | `bound.ii_words.n4.K_ret.tier` | "POST HOC" | POST HOC | label | 11_supplement_registered_rows.md Table S24 |
| 931 | data/results/c_attr_1112_score/res/COPYBOUND_ov_dev_b_aya_vision_8b.json | `bound.i_syllables.n2.K_ret.d` | 14.202718384824406 | +14.20 | number | 11_supplement_registered_rows.md Table S24 |
| 932 | data/results/c_attr_1112_score/res/COPYBOUND_ov_dev_b_aya_vision_8b.json | `bound.i_syllables.n2.K_ret.lo` | 12.67237047724983 | 12.67 | number | 11_supplement_registered_rows.md Table S24 |
| 933 | data/results/c_attr_1112_score/res/COPYBOUND_ov_dev_b_aya_vision_8b.json | `bound.i_syllables.n2.K_ret.hi` | 15.745665767400412 | 15.75 | number | 11_supplement_registered_rows.md Table S24 |
| 934 | data/results/c_attr_1112_score/res/COPYBOUND_ov_dev_b_aya_vision_8b.json | `bound.i_syllables.n2.K_ret.label` | "DETECTED" | DETECTED | label | 11_supplement_registered_rows.md Table S24 |
| 935 | data/results/c_attr_1112_score/res/COPYBOUND_ov_dev_b_aya_vision_8b.json | `bound.i_syllables.n2.L_cp.d` | -6.889101936038179 | −6.89 | number | 11_supplement_registered_rows.md Table S24 |
| 936 | data/results/c_attr_1112_score/res/COPYBOUND_ov_dev_b_aya_vision_8b.json | `bound.i_syllables.n2.L_cp.lo` | -8.475996900508747 | −8.48 | number | 11_supplement_registered_rows.md Table S24 |
| 937 | data/results/c_attr_1112_score/res/COPYBOUND_ov_dev_b_aya_vision_8b.json | `bound.i_syllables.n2.L_cp.hi` | -5.369320517725971 | −5.37 | number | 11_supplement_registered_rows.md Table S24 |
| 938 | data/results/c_attr_1112_score/res/COPYBOUND_ov_dev_b_aya_vision_8b.json | `bound.i_syllables.n2.L_cp.label` | "REVERSED" | REVERSED | label | 11_supplement_registered_rows.md Table S24 |
| 939 | data/results/c_attr_1112_score/res/COPYBOUND_ov_dev_b_aya_vision_8b.json | `bound.i_syllables.n2.K_nc.d` | 6.651247845787729 | +6.65 | number | 11_supplement_registered_rows.md Table S24 |
| 940 | data/results/c_attr_1112_score/res/COPYBOUND_ov_dev_b_aya_vision_8b.json | `bound.i_syllables.n2.K_nc.lo` | 5.6924728463728425 | 5.69 | number | 11_supplement_registered_rows.md Table S24 |
| 941 | data/results/c_attr_1112_score/res/COPYBOUND_ov_dev_b_aya_vision_8b.json | `bound.i_syllables.n2.K_nc.hi` | 7.690517796580252 | 7.69 | number | 11_supplement_registered_rows.md Table S24 |
| 942 | data/results/c_attr_1112_score/res/COPYBOUND_ov_dev_b_aya_vision_8b.json | `bound.i_syllables.n2.K_nc.label` | "DETECTED" | DETECTED | label | 11_supplement_registered_rows.md Table S24 |
| 943 | data/results/c_attr_1112_score/res/COPYBOUND_ov_dev_b_aya_vision_8b.json | `bound.i_syllables.n2.K_rand.d` | 1.540717670577349 | +1.54 | number | 11_supplement_registered_rows.md Table S24 |
| 944 | data/results/c_attr_1112_score/res/COPYBOUND_ov_dev_b_aya_vision_8b.json | `bound.i_syllables.n2.K_rand.lo` | 1.0547903580165532 | 1.05 | number | 11_supplement_registered_rows.md Table S24 |
| 945 | data/results/c_attr_1112_score/res/COPYBOUND_ov_dev_b_aya_vision_8b.json | `bound.i_syllables.n2.K_rand.hi` | 2.0815871955480776 | 2.08 | number | 11_supplement_registered_rows.md Table S24 |
| 946 | data/results/c_attr_1112_score/res/COPYBOUND_ov_dev_b_aya_vision_8b.json | `bound.i_syllables.n2.K_ret_minus_K_nc.d` | 7.5514705390366785 | +7.55 | number | 11_supplement_registered_rows.md Table S24 |
| 947 | data/results/c_attr_1112_score/res/COPYBOUND_ov_dev_b_aya_vision_8b.json | `bound.i_syllables.n2.K_ret_minus_K_nc.lo` | 6.073883562195619 | 6.07 | number | 11_supplement_registered_rows.md Table S24 |
| 948 | data/results/c_attr_1112_score/res/COPYBOUND_ov_dev_b_aya_vision_8b.json | `bound.i_syllables.n2.K_ret_minus_K_nc.hi` | 9.070062233810189 | 9.07 | number | 11_supplement_registered_rows.md Table S24 |
| 949 | data/results/c_attr_1112_score/res/COPYBOUND_ov_dev_b_aya_vision_8b.json | `blind` | "NOT RUN: no admitted blind run staged" | NOT RUN: no admitted blind run staged | text | 11_supplement_registered_rows.md Table S24 |
| 950 | data/results/c_attr_1112_score/res/COPYBOUND_ov_dev_b_aya_vision_8b.json | `bound.i_syllables.n2.K_ret.tier` | "POST HOC" | POST HOC | label | 11_supplement_registered_rows.md Table S24 |
| 951 | data/results/c_attr_1112_score/res/COPYBOUND_ov_dev_b_aya_vision_8b.json | `bound.i_syllables.n3.K_ret.d` | 9.015603056161774 | +9.02 | number | 11_supplement_registered_rows.md Table S24 |
| 952 | data/results/c_attr_1112_score/res/COPYBOUND_ov_dev_b_aya_vision_8b.json | `bound.i_syllables.n3.K_ret.lo` | 7.829099297057835 | 7.83 | number | 11_supplement_registered_rows.md Table S24 |
| 953 | data/results/c_attr_1112_score/res/COPYBOUND_ov_dev_b_aya_vision_8b.json | `bound.i_syllables.n3.K_ret.hi` | 10.266404539773546 | 10.27 | number | 11_supplement_registered_rows.md Table S24 |
| 954 | data/results/c_attr_1112_score/res/COPYBOUND_ov_dev_b_aya_vision_8b.json | `bound.i_syllables.n3.K_ret.label` | "DETECTED" | DETECTED | label | 11_supplement_registered_rows.md Table S24 |
| 955 | data/results/c_attr_1112_score/res/COPYBOUND_ov_dev_b_aya_vision_8b.json | `bound.i_syllables.n3.L_cp.d` | -1.7019866073755456 | −1.70 | number | 11_supplement_registered_rows.md Table S24 |
| 956 | data/results/c_attr_1112_score/res/COPYBOUND_ov_dev_b_aya_vision_8b.json | `bound.i_syllables.n3.L_cp.lo` | -3.2767966252914245 | −3.28 | number | 11_supplement_registered_rows.md Table S24 |
| 957 | data/results/c_attr_1112_score/res/COPYBOUND_ov_dev_b_aya_vision_8b.json | `bound.i_syllables.n3.L_cp.hi` | -0.13369643074849094 | −0.13 | number | 11_supplement_registered_rows.md Table S24 |
| 958 | data/results/c_attr_1112_score/res/COPYBOUND_ov_dev_b_aya_vision_8b.json | `bound.i_syllables.n3.L_cp.label` | "REVERSED" | REVERSED | label | 11_supplement_registered_rows.md Table S24 |
| 959 | data/results/c_attr_1112_score/res/COPYBOUND_ov_dev_b_aya_vision_8b.json | `bound.i_syllables.n3.K_nc.d` | 3.5049051729064655 | +3.50 | number | 11_supplement_registered_rows.md Table S24 |
| 960 | data/results/c_attr_1112_score/res/COPYBOUND_ov_dev_b_aya_vision_8b.json | `bound.i_syllables.n3.K_nc.lo` | 2.7354240083286645 | 2.74 | number | 11_supplement_registered_rows.md Table S24 |
| 961 | data/results/c_attr_1112_score/res/COPYBOUND_ov_dev_b_aya_vision_8b.json | `bound.i_syllables.n3.K_nc.hi` | 4.297150391640748 | 4.30 | number | 11_supplement_registered_rows.md Table S24 |
| 962 | data/results/c_attr_1112_score/res/COPYBOUND_ov_dev_b_aya_vision_8b.json | `bound.i_syllables.n3.K_nc.label` | "DETECTED" | DETECTED | label | 11_supplement_registered_rows.md Table S24 |
| 963 | data/results/c_attr_1112_score/res/COPYBOUND_ov_dev_b_aya_vision_8b.json | `bound.i_syllables.n3.K_rand.d` | 0.7040663831816164 | +0.70 | number | 11_supplement_registered_rows.md Table S24 |
| 964 | data/results/c_attr_1112_score/res/COPYBOUND_ov_dev_b_aya_vision_8b.json | `bound.i_syllables.n3.K_rand.lo` | 0.3401763772541416 | 0.34 | number | 11_supplement_registered_rows.md Table S24 |
| 965 | data/results/c_attr_1112_score/res/COPYBOUND_ov_dev_b_aya_vision_8b.json | `bound.i_syllables.n3.K_rand.hi` | 1.0850263870992176 | 1.09 | number | 11_supplement_registered_rows.md Table S24 |
| 966 | data/results/c_attr_1112_score/res/COPYBOUND_ov_dev_b_aya_vision_8b.json | `bound.i_syllables.n3.K_ret_minus_K_nc.d` | 5.51069788325531 | +5.51 | number | 11_supplement_registered_rows.md Table S24 |
| 967 | data/results/c_attr_1112_score/res/COPYBOUND_ov_dev_b_aya_vision_8b.json | `bound.i_syllables.n3.K_ret_minus_K_nc.lo` | 4.316250917818969 | 4.32 | number | 11_supplement_registered_rows.md Table S24 |
| 968 | data/results/c_attr_1112_score/res/COPYBOUND_ov_dev_b_aya_vision_8b.json | `bound.i_syllables.n3.K_ret_minus_K_nc.hi` | 6.755543029124099 | 6.76 | number | 11_supplement_registered_rows.md Table S24 |
| 969 | data/results/c_attr_1112_score/res/COPYBOUND_ov_dev_b_aya_vision_8b.json | `blind` | "NOT RUN: no admitted blind run staged" | NOT RUN: no admitted blind run staged | text | 11_supplement_registered_rows.md Table S24 |
| 970 | data/results/c_attr_1112_score/res/COPYBOUND_ov_dev_b_aya_vision_8b.json | `bound.i_syllables.n3.K_ret.tier` | "POST HOC" | POST HOC | label | 11_supplement_registered_rows.md Table S24 |
| 971 | data/results/c_attr_1112_score/res/COPYBOUND_ov_dev_b_aya_vision_8b.json | `bound.i_syllables.n4.K_ret.d` | 5.686352912357513 | +5.69 | number | 11_supplement_registered_rows.md Table S24 |
| 972 | data/results/c_attr_1112_score/res/COPYBOUND_ov_dev_b_aya_vision_8b.json | `bound.i_syllables.n4.K_ret.lo` | 4.657937089697401 | 4.66 | number | 11_supplement_registered_rows.md Table S24 |
| 973 | data/results/c_attr_1112_score/res/COPYBOUND_ov_dev_b_aya_vision_8b.json | `bound.i_syllables.n4.K_ret.hi` | 6.738778456216686 | 6.74 | number | 11_supplement_registered_rows.md Table S24 |
| 974 | data/results/c_attr_1112_score/res/COPYBOUND_ov_dev_b_aya_vision_8b.json | `bound.i_syllables.n4.K_ret.label` | "DETECTED" | DETECTED | label | 11_supplement_registered_rows.md Table S24 |
| 975 | data/results/c_attr_1112_score/res/COPYBOUND_ov_dev_b_aya_vision_8b.json | `bound.i_syllables.n4.L_cp.d` | 1.627263536428716 | +1.63 | number | 11_supplement_registered_rows.md Table S24 |
| 976 | data/results/c_attr_1112_score/res/COPYBOUND_ov_dev_b_aya_vision_8b.json | `bound.i_syllables.n4.L_cp.lo` | -0.006391026133506171 | −0.01 | number | 11_supplement_registered_rows.md Table S24 |
| 977 | data/results/c_attr_1112_score/res/COPYBOUND_ov_dev_b_aya_vision_8b.json | `bound.i_syllables.n4.L_cp.hi` | 3.2912934529959466 | 3.29 | number | 11_supplement_registered_rows.md Table S24 |
| 978 | data/results/c_attr_1112_score/res/COPYBOUND_ov_dev_b_aya_vision_8b.json | `bound.i_syllables.n4.L_cp.label` | "UNRESOLVED" | UNRESOLVED | label | 11_supplement_registered_rows.md Table S24 |
| 979 | data/results/c_attr_1112_score/res/COPYBOUND_ov_dev_b_aya_vision_8b.json | `bound.i_syllables.n4.K_nc.d` | 1.612966697178939 | +1.61 | number | 11_supplement_registered_rows.md Table S24 |
| 980 | data/results/c_attr_1112_score/res/COPYBOUND_ov_dev_b_aya_vision_8b.json | `bound.i_syllables.n4.K_nc.lo` | 1.1138676181689844 | 1.11 | number | 11_supplement_registered_rows.md Table S24 |
| 981 | data/results/c_attr_1112_score/res/COPYBOUND_ov_dev_b_aya_vision_8b.json | `bound.i_syllables.n4.K_nc.hi` | 2.165355971095514 | 2.17 | number | 11_supplement_registered_rows.md Table S24 |
| 982 | data/results/c_attr_1112_score/res/COPYBOUND_ov_dev_b_aya_vision_8b.json | `bound.i_syllables.n4.K_nc.label` | "UNRESOLVED" | UNRESOLVED | label | 11_supplement_registered_rows.md Table S24 |
| 983 | data/results/c_attr_1112_score/res/COPYBOUND_ov_dev_b_aya_vision_8b.json | `bound.i_syllables.n4.K_rand.d` | 0.3643108324635052 | +0.36 | number | 11_supplement_registered_rows.md Table S24 |
| 984 | data/results/c_attr_1112_score/res/COPYBOUND_ov_dev_b_aya_vision_8b.json | `bound.i_syllables.n4.K_rand.lo` | 0.06491819752498312 | 0.06 | number | 11_supplement_registered_rows.md Table S24 |
| 985 | data/results/c_attr_1112_score/res/COPYBOUND_ov_dev_b_aya_vision_8b.json | `bound.i_syllables.n4.K_rand.hi` | 0.6970950723599142 | 0.70 | number | 11_supplement_registered_rows.md Table S24 |
| 986 | data/results/c_attr_1112_score/res/COPYBOUND_ov_dev_b_aya_vision_8b.json | `bound.i_syllables.n4.K_ret_minus_K_nc.d` | 4.073386215178573 | +4.07 | number | 11_supplement_registered_rows.md Table S24 |
| 987 | data/results/c_attr_1112_score/res/COPYBOUND_ov_dev_b_aya_vision_8b.json | `bound.i_syllables.n4.K_ret_minus_K_nc.lo` | 3.078376318584529 | 3.08 | number | 11_supplement_registered_rows.md Table S24 |
| 988 | data/results/c_attr_1112_score/res/COPYBOUND_ov_dev_b_aya_vision_8b.json | `bound.i_syllables.n4.K_ret_minus_K_nc.hi` | 5.088573424711384 | 5.09 | number | 11_supplement_registered_rows.md Table S24 |
| 989 | data/results/c_attr_1112_score/res/COPYBOUND_ov_dev_b_aya_vision_8b.json | `blind` | "NOT RUN: no admitted blind run staged" | NOT RUN: no admitted blind run staged | text | 11_supplement_registered_rows.md Table S24 |
| 990 | data/results/c_attr_1112_score/res/COPYBOUND_ov_dev_b_aya_vision_8b.json | `bound.i_syllables.n4.K_ret.tier` | "POST HOC" | POST HOC | label | 11_supplement_registered_rows.md Table S24 |
| 991 | data/results/c_attr_1112_score/res/COPYBOUND_ov_dev_b_aya_vision_8b.json | `bound.ii_words.n2.K_ret.d` | 13.288599007948886 | +13.29 | number | 11_supplement_registered_rows.md Table S24 |
| 992 | data/results/c_attr_1112_score/res/COPYBOUND_ov_dev_b_aya_vision_8b.json | `bound.ii_words.n2.K_ret.lo` | 11.812324665764024 | 11.81 | number | 11_supplement_registered_rows.md Table S24 |
| 993 | data/results/c_attr_1112_score/res/COPYBOUND_ov_dev_b_aya_vision_8b.json | `bound.ii_words.n2.K_ret.hi` | 14.803384465566065 | 14.80 | number | 11_supplement_registered_rows.md Table S24 |
| 994 | data/results/c_attr_1112_score/res/COPYBOUND_ov_dev_b_aya_vision_8b.json | `bound.ii_words.n2.K_ret.label` | "DETECTED" | DETECTED | label | 11_supplement_registered_rows.md Table S24 |
| 995 | data/results/c_attr_1112_score/res/COPYBOUND_ov_dev_b_aya_vision_8b.json | `bound.ii_words.n2.L_cp.d` | -5.974982559162655 | −5.97 | number | 11_supplement_registered_rows.md Table S24 |
| 996 | data/results/c_attr_1112_score/res/COPYBOUND_ov_dev_b_aya_vision_8b.json | `bound.ii_words.n2.L_cp.lo` | -7.628161012126013 | −7.63 | number | 11_supplement_registered_rows.md Table S24 |
| 997 | data/results/c_attr_1112_score/res/COPYBOUND_ov_dev_b_aya_vision_8b.json | `bound.ii_words.n2.L_cp.hi` | -4.384695747077884 | −4.38 | number | 11_supplement_registered_rows.md Table S24 |
| 998 | data/results/c_attr_1112_score/res/COPYBOUND_ov_dev_b_aya_vision_8b.json | `bound.ii_words.n2.L_cp.label` | "REVERSED" | REVERSED | label | 11_supplement_registered_rows.md Table S24 |
| 999 | data/results/c_attr_1112_score/res/COPYBOUND_ov_dev_b_aya_vision_8b.json | `bound.ii_words.n2.K_nc.d` | 6.090918357701016 | +6.09 | number | 11_supplement_registered_rows.md Table S24 |
| 1000 | data/results/c_attr_1112_score/res/COPYBOUND_ov_dev_b_aya_vision_8b.json | `bound.ii_words.n2.K_nc.lo` | 5.146639758172222 | 5.15 | number | 11_supplement_registered_rows.md Table S24 |
| 1001 | data/results/c_attr_1112_score/res/COPYBOUND_ov_dev_b_aya_vision_8b.json | `bound.ii_words.n2.K_nc.hi` | 7.107954783747053 | 7.11 | number | 11_supplement_registered_rows.md Table S24 |
| 1002 | data/results/c_attr_1112_score/res/COPYBOUND_ov_dev_b_aya_vision_8b.json | `bound.ii_words.n2.K_nc.label` | "DETECTED" | DETECTED | label | 11_supplement_registered_rows.md Table S24 |
| 1003 | data/results/c_attr_1112_score/res/COPYBOUND_ov_dev_b_aya_vision_8b.json | `bound.ii_words.n2.K_rand.d` | 1.501963438859951 | +1.50 | number | 11_supplement_registered_rows.md Table S24 |
| 1004 | data/results/c_attr_1112_score/res/COPYBOUND_ov_dev_b_aya_vision_8b.json | `bound.ii_words.n2.K_rand.lo` | 1.033781820278085 | 1.03 | number | 11_supplement_registered_rows.md Table S24 |
| 1005 | data/results/c_attr_1112_score/res/COPYBOUND_ov_dev_b_aya_vision_8b.json | `bound.ii_words.n2.K_rand.hi` | 2.0271649759123895 | 2.03 | number | 11_supplement_registered_rows.md Table S24 |
| 1006 | data/results/c_attr_1112_score/res/COPYBOUND_ov_dev_b_aya_vision_8b.json | `bound.ii_words.n2.K_ret_minus_K_nc.d` | 7.197680650247869 | +7.20 | number | 11_supplement_registered_rows.md Table S24 |
| 1007 | data/results/c_attr_1112_score/res/COPYBOUND_ov_dev_b_aya_vision_8b.json | `bound.ii_words.n2.K_ret_minus_K_nc.lo` | 5.826413596372083 | 5.83 | number | 11_supplement_registered_rows.md Table S24 |
| 1008 | data/results/c_attr_1112_score/res/COPYBOUND_ov_dev_b_aya_vision_8b.json | `bound.ii_words.n2.K_ret_minus_K_nc.hi` | 8.673567559148822 | 8.67 | number | 11_supplement_registered_rows.md Table S24 |
| 1009 | data/results/c_attr_1112_score/res/COPYBOUND_ov_dev_b_aya_vision_8b.json | `blind` | "NOT RUN: no admitted blind run staged" | NOT RUN: no admitted blind run staged | text | 11_supplement_registered_rows.md Table S24 |
| 1010 | data/results/c_attr_1112_score/res/COPYBOUND_ov_dev_b_aya_vision_8b.json | `bound.ii_words.n2.K_ret.tier` | "POST HOC" | POST HOC | label | 11_supplement_registered_rows.md Table S24 |
| 1011 | data/results/c_attr_1112_score/res/COPYBOUND_ov_dev_b_aya_vision_8b.json | `bound.ii_words.n3.K_ret.d` | 7.879667897111323 | +7.88 | number | 11_supplement_registered_rows.md Table S24 |
| 1012 | data/results/c_attr_1112_score/res/COPYBOUND_ov_dev_b_aya_vision_8b.json | `bound.ii_words.n3.K_ret.lo` | 6.733035151792877 | 6.73 | number | 11_supplement_registered_rows.md Table S24 |
| 1013 | data/results/c_attr_1112_score/res/COPYBOUND_ov_dev_b_aya_vision_8b.json | `bound.ii_words.n3.K_ret.hi` | 9.105078916395515 | 9.11 | number | 11_supplement_registered_rows.md Table S24 |
| 1014 | data/results/c_attr_1112_score/res/COPYBOUND_ov_dev_b_aya_vision_8b.json | `bound.ii_words.n3.K_ret.label` | "DETECTED" | DETECTED | label | 11_supplement_registered_rows.md Table S24 |
| 1015 | data/results/c_attr_1112_score/res/COPYBOUND_ov_dev_b_aya_vision_8b.json | `bound.ii_words.n3.L_cp.d` | -0.5660514483250949 | −0.57 | number | 11_supplement_registered_rows.md Table S24 |
| 1016 | data/results/c_attr_1112_score/res/COPYBOUND_ov_dev_b_aya_vision_8b.json | `bound.ii_words.n3.L_cp.lo` | -2.163585953345003 | −2.16 | number | 11_supplement_registered_rows.md Table S24 |
| 1017 | data/results/c_attr_1112_score/res/COPYBOUND_ov_dev_b_aya_vision_8b.json | `bound.ii_words.n3.L_cp.hi` | 0.9943073192522447 | 0.99 | number | 11_supplement_registered_rows.md Table S24 |
| 1018 | data/results/c_attr_1112_score/res/COPYBOUND_ov_dev_b_aya_vision_8b.json | `bound.ii_words.n3.L_cp.label` | "NEGLIGIBLE" | NEGLIGIBLE | label | 11_supplement_registered_rows.md Table S24 |
| 1019 | data/results/c_attr_1112_score/res/COPYBOUND_ov_dev_b_aya_vision_8b.json | `bound.ii_words.n3.K_nc.d` | 2.548901300617866 | +2.55 | number | 11_supplement_registered_rows.md Table S24 |
| 1020 | data/results/c_attr_1112_score/res/COPYBOUND_ov_dev_b_aya_vision_8b.json | `bound.ii_words.n3.K_nc.lo` | 1.9003322796710789 | 1.90 | number | 11_supplement_registered_rows.md Table S24 |
| 1021 | data/results/c_attr_1112_score/res/COPYBOUND_ov_dev_b_aya_vision_8b.json | `bound.ii_words.n3.K_nc.hi` | 3.249917224902498 | 3.25 | number | 11_supplement_registered_rows.md Table S24 |
| 1022 | data/results/c_attr_1112_score/res/COPYBOUND_ov_dev_b_aya_vision_8b.json | `bound.ii_words.n3.K_nc.label` | "DETECTED" | DETECTED | label | 11_supplement_registered_rows.md Table S24 |
| 1023 | data/results/c_attr_1112_score/res/COPYBOUND_ov_dev_b_aya_vision_8b.json | `bound.ii_words.n3.K_rand.d` | 0.6155802825394757 | +0.62 | number | 11_supplement_registered_rows.md Table S24 |
| 1024 | data/results/c_attr_1112_score/res/COPYBOUND_ov_dev_b_aya_vision_8b.json | `bound.ii_words.n3.K_rand.lo` | 0.28623339215920157 | 0.29 | number | 11_supplement_registered_rows.md Table S24 |
| 1025 | data/results/c_attr_1112_score/res/COPYBOUND_ov_dev_b_aya_vision_8b.json | `bound.ii_words.n3.K_rand.hi` | 0.962383611826503 | 0.96 | number | 11_supplement_registered_rows.md Table S24 |
| 1026 | data/results/c_attr_1112_score/res/COPYBOUND_ov_dev_b_aya_vision_8b.json | `bound.ii_words.n3.K_ret_minus_K_nc.d` | 5.330766596493459 | +5.33 | number | 11_supplement_registered_rows.md Table S24 |
| 1027 | data/results/c_attr_1112_score/res/COPYBOUND_ov_dev_b_aya_vision_8b.json | `bound.ii_words.n3.K_ret_minus_K_nc.lo` | 4.125198649067705 | 4.13 | number | 11_supplement_registered_rows.md Table S24 |
| 1028 | data/results/c_attr_1112_score/res/COPYBOUND_ov_dev_b_aya_vision_8b.json | `bound.ii_words.n3.K_ret_minus_K_nc.hi` | 6.513137013195792 | 6.51 | number | 11_supplement_registered_rows.md Table S24 |
| 1029 | data/results/c_attr_1112_score/res/COPYBOUND_ov_dev_b_aya_vision_8b.json | `blind` | "NOT RUN: no admitted blind run staged" | NOT RUN: no admitted blind run staged | text | 11_supplement_registered_rows.md Table S24 |
| 1030 | data/results/c_attr_1112_score/res/COPYBOUND_ov_dev_b_aya_vision_8b.json | `bound.ii_words.n3.K_ret.tier` | "POST HOC" | POST HOC | label | 11_supplement_registered_rows.md Table S24 |
| 1031 | data/results/c_attr_1112_score/res/COPYBOUND_ov_dev_b_aya_vision_8b.json | `bound.ii_words.n4.K_ret.d` | 4.350286607845466 | +4.35 | number | 11_supplement_registered_rows.md Table S24 |
| 1032 | data/results/c_attr_1112_score/res/COPYBOUND_ov_dev_b_aya_vision_8b.json | `bound.ii_words.n4.K_ret.lo` | 3.37449307975052 | 3.37 | number | 11_supplement_registered_rows.md Table S24 |
| 1033 | data/results/c_attr_1112_score/res/COPYBOUND_ov_dev_b_aya_vision_8b.json | `bound.ii_words.n4.K_ret.hi` | 5.366923004381609 | 5.37 | number | 11_supplement_registered_rows.md Table S24 |
| 1034 | data/results/c_attr_1112_score/res/COPYBOUND_ov_dev_b_aya_vision_8b.json | `bound.ii_words.n4.K_ret.label` | "DETECTED" | DETECTED | label | 11_supplement_registered_rows.md Table S24 |
| 1035 | data/results/c_attr_1112_score/res/COPYBOUND_ov_dev_b_aya_vision_8b.json | `bound.ii_words.n4.L_cp.d` | 2.9633298409407636 | +2.96 | number | 11_supplement_registered_rows.md Table S24 |
| 1036 | data/results/c_attr_1112_score/res/COPYBOUND_ov_dev_b_aya_vision_8b.json | `bound.ii_words.n4.L_cp.lo` | 1.3421881678945802 | 1.34 | number | 11_supplement_registered_rows.md Table S24 |
| 1037 | data/results/c_attr_1112_score/res/COPYBOUND_ov_dev_b_aya_vision_8b.json | `bound.ii_words.n4.L_cp.hi` | 4.621830708063117 | 4.62 | number | 11_supplement_registered_rows.md Table S24 |
| 1038 | data/results/c_attr_1112_score/res/COPYBOUND_ov_dev_b_aya_vision_8b.json | `bound.ii_words.n4.L_cp.label` | "DETECTED" | DETECTED | label | 11_supplement_registered_rows.md Table S24 |
| 1039 | data/results/c_attr_1112_score/res/COPYBOUND_ov_dev_b_aya_vision_8b.json | `bound.ii_words.n4.K_nc.d` | 1.162858737390289 | +1.16 | number | 11_supplement_registered_rows.md Table S24 |
| 1040 | data/results/c_attr_1112_score/res/COPYBOUND_ov_dev_b_aya_vision_8b.json | `bound.ii_words.n4.K_nc.lo` | 0.7242204867411417 | 0.72 | number | 11_supplement_registered_rows.md Table S24 |
| 1041 | data/results/c_attr_1112_score/res/COPYBOUND_ov_dev_b_aya_vision_8b.json | `bound.ii_words.n4.K_nc.hi` | 1.6504297130971881 | 1.65 | number | 11_supplement_registered_rows.md Table S24 |
| 1042 | data/results/c_attr_1112_score/res/COPYBOUND_ov_dev_b_aya_vision_8b.json | `bound.ii_words.n4.K_nc.label` | "NEGLIGIBLE" | NEGLIGIBLE | label | 11_supplement_registered_rows.md Table S24 |
| 1043 | data/results/c_attr_1112_score/res/COPYBOUND_ov_dev_b_aya_vision_8b.json | `bound.ii_words.n4.K_rand.d` | 0.13377648421719263 | +0.13 | number | 11_supplement_registered_rows.md Table S24 |
| 1044 | data/results/c_attr_1112_score/res/COPYBOUND_ov_dev_b_aya_vision_8b.json | `bound.ii_words.n4.K_rand.lo` | -0.08422898384064853 | −0.08 | number | 11_supplement_registered_rows.md Table S24 |
| 1045 | data/results/c_attr_1112_score/res/COPYBOUND_ov_dev_b_aya_vision_8b.json | `bound.ii_words.n4.K_rand.hi` | 0.40595571670763986 | 0.41 | number | 11_supplement_registered_rows.md Table S24 |
| 1046 | data/results/c_attr_1112_score/res/COPYBOUND_ov_dev_b_aya_vision_8b.json | `bound.ii_words.n4.K_ret_minus_K_nc.d` | 3.187427870455176 | +3.19 | number | 11_supplement_registered_rows.md Table S24 |
| 1047 | data/results/c_attr_1112_score/res/COPYBOUND_ov_dev_b_aya_vision_8b.json | `bound.ii_words.n4.K_ret_minus_K_nc.lo` | 2.2208616360665845 | 2.22 | number | 11_supplement_registered_rows.md Table S24 |
| 1048 | data/results/c_attr_1112_score/res/COPYBOUND_ov_dev_b_aya_vision_8b.json | `bound.ii_words.n4.K_ret_minus_K_nc.hi` | 4.1503120025624725 | 4.15 | number | 11_supplement_registered_rows.md Table S24 |
| 1049 | data/results/c_attr_1112_score/res/COPYBOUND_ov_dev_b_aya_vision_8b.json | `blind` | "NOT RUN: no admitted blind run staged" | NOT RUN: no admitted blind run staged | text | 11_supplement_registered_rows.md Table S24 |
| 1050 | data/results/c_attr_1112_score/res/COPYBOUND_ov_dev_b_aya_vision_8b.json | `bound.ii_words.n4.K_ret.tier` | "POST HOC" | POST HOC | label | 11_supplement_registered_rows.md Table S24 |
| 1051 | data/results/c_attr_1112_score/res/COPYBOUND_xm_dev500_qwen25vl_7b.json | `bound.i_syllables.n2.K_ret.d` | 17.056682226919445 | +17.06 | number | 11_supplement_registered_rows.md Table S24 |
| 1052 | data/results/c_attr_1112_score/res/COPYBOUND_xm_dev500_qwen25vl_7b.json | `bound.i_syllables.n2.K_ret.lo` | 13.796868718233663 | 13.80 | number | 11_supplement_registered_rows.md Table S24 |
| 1053 | data/results/c_attr_1112_score/res/COPYBOUND_xm_dev500_qwen25vl_7b.json | `bound.i_syllables.n2.K_ret.hi` | 20.15056436077975 | 20.15 | number | 11_supplement_registered_rows.md Table S24 |
| 1054 | data/results/c_attr_1112_score/res/COPYBOUND_xm_dev500_qwen25vl_7b.json | `bound.i_syllables.n2.K_ret.label` | "DETECTED" | DETECTED | label | 11_supplement_registered_rows.md Table S24 |
| 1055 | data/results/c_attr_1112_score/res/COPYBOUND_xm_dev500_qwen25vl_7b.json | `bound.i_syllables.n2.L_cp.d` | -12.616182908345483 | −12.62 | number | 11_supplement_registered_rows.md Table S24 |
| 1056 | data/results/c_attr_1112_score/res/COPYBOUND_xm_dev500_qwen25vl_7b.json | `bound.i_syllables.n2.L_cp.lo` | -16.39933863415256 | −16.40 | number | 11_supplement_registered_rows.md Table S24 |
| 1057 | data/results/c_attr_1112_score/res/COPYBOUND_xm_dev500_qwen25vl_7b.json | `bound.i_syllables.n2.L_cp.hi` | -8.750901909595164 | −8.75 | number | 11_supplement_registered_rows.md Table S24 |
| 1058 | data/results/c_attr_1112_score/res/COPYBOUND_xm_dev500_qwen25vl_7b.json | `bound.i_syllables.n2.L_cp.label` | "REVERSED" | REVERSED | label | 11_supplement_registered_rows.md Table S24 |
| 1059 | data/results/c_attr_1112_score/res/COPYBOUND_xm_dev500_qwen25vl_7b.json | `bound.i_syllables.n2.K_nc.d` | 10.52508522866084 | +10.53 | number | 11_supplement_registered_rows.md Table S24 |
| 1060 | data/results/c_attr_1112_score/res/COPYBOUND_xm_dev500_qwen25vl_7b.json | `bound.i_syllables.n2.K_nc.lo` | 7.626710311226753 | 7.63 | number | 11_supplement_registered_rows.md Table S24 |
| 1061 | data/results/c_attr_1112_score/res/COPYBOUND_xm_dev500_qwen25vl_7b.json | `bound.i_syllables.n2.K_nc.hi` | 13.652061999003305 | 13.65 | number | 11_supplement_registered_rows.md Table S24 |
| 1062 | data/results/c_attr_1112_score/res/COPYBOUND_xm_dev500_qwen25vl_7b.json | `bound.i_syllables.n2.K_nc.label` | "DETECTED" | DETECTED | label | 11_supplement_registered_rows.md Table S24 |
| 1063 | data/results/c_attr_1112_score/res/COPYBOUND_xm_dev500_qwen25vl_7b.json | `bound.i_syllables.n2.K_rand.d` | 6.868462539747274 | +6.87 | number | 11_supplement_registered_rows.md Table S24 |
| 1064 | data/results/c_attr_1112_score/res/COPYBOUND_xm_dev500_qwen25vl_7b.json | `bound.i_syllables.n2.K_rand.lo` | 4.961116754063524 | 4.96 | number | 11_supplement_registered_rows.md Table S24 |
| 1065 | data/results/c_attr_1112_score/res/COPYBOUND_xm_dev500_qwen25vl_7b.json | `bound.i_syllables.n2.K_rand.hi` | 8.991870267764929 | 8.99 | number | 11_supplement_registered_rows.md Table S24 |
| 1066 | data/results/c_attr_1112_score/res/COPYBOUND_xm_dev500_qwen25vl_7b.json | `bound.i_syllables.n2.K_ret_minus_K_nc.d` | 6.531596998258605 | +6.53 | number | 11_supplement_registered_rows.md Table S24 |
| 1067 | data/results/c_attr_1112_score/res/COPYBOUND_xm_dev500_qwen25vl_7b.json | `bound.i_syllables.n2.K_ret_minus_K_nc.lo` | 3.798109744642752 | 3.80 | number | 11_supplement_registered_rows.md Table S24 |
| 1068 | data/results/c_attr_1112_score/res/COPYBOUND_xm_dev500_qwen25vl_7b.json | `bound.i_syllables.n2.K_ret_minus_K_nc.hi` | 9.203688641626567 | 9.20 | number | 11_supplement_registered_rows.md Table S24 |
| 1069 | data/results/c_attr_1112_score/res/COPYBOUND_xm_dev500_qwen25vl_7b.json | `bound.i_syllables.n2.blind_loss.d` | 10.28016183499102 | +10.28 | number | 11_supplement_registered_rows.md Table S24 |
| 1070 | data/results/c_attr_1112_score/res/COPYBOUND_xm_dev500_qwen25vl_7b.json | `bound.i_syllables.n2.blind_loss.lo` | 8.626494074663542 | 8.63 | number | 11_supplement_registered_rows.md Table S24 |
| 1071 | data/results/c_attr_1112_score/res/COPYBOUND_xm_dev500_qwen25vl_7b.json | `bound.i_syllables.n2.blind_loss.hi` | 12.050374614452592 | 12.05 | number | 11_supplement_registered_rows.md Table S24 |
| 1072 | data/results/c_attr_1112_score/res/COPYBOUND_xm_dev500_qwen25vl_7b.json | `bound.i_syllables.n2.K_ret.tier` | "first look" | first look | label | 11_supplement_registered_rows.md Table S24 |
| 1073 | data/results/c_attr_1112_score/res/COPYBOUND_xm_dev500_qwen25vl_7b.json | `bound.i_syllables.n3.K_ret.d` | 14.250830606039694 | +14.25 | number | 11_supplement_registered_rows.md Table S24 |
| 1074 | data/results/c_attr_1112_score/res/COPYBOUND_xm_dev500_qwen25vl_7b.json | `bound.i_syllables.n3.K_ret.lo` | 11.591669018621667 | 11.59 | number | 11_supplement_registered_rows.md Table S24 |
| 1075 | data/results/c_attr_1112_score/res/COPYBOUND_xm_dev500_qwen25vl_7b.json | `bound.i_syllables.n3.K_ret.hi` | 17.040899963011668 | 17.04 | number | 11_supplement_registered_rows.md Table S24 |
| 1076 | data/results/c_attr_1112_score/res/COPYBOUND_xm_dev500_qwen25vl_7b.json | `bound.i_syllables.n3.K_ret.label` | "DETECTED" | DETECTED | label | 11_supplement_registered_rows.md Table S24 |
| 1077 | data/results/c_attr_1112_score/res/COPYBOUND_xm_dev500_qwen25vl_7b.json | `bound.i_syllables.n3.L_cp.d` | -9.810331287465733 | −9.81 | number | 11_supplement_registered_rows.md Table S24 |
| 1078 | data/results/c_attr_1112_score/res/COPYBOUND_xm_dev500_qwen25vl_7b.json | `bound.i_syllables.n3.L_cp.lo` | -13.665674727804914 | −13.67 | number | 11_supplement_registered_rows.md Table S24 |
| 1079 | data/results/c_attr_1112_score/res/COPYBOUND_xm_dev500_qwen25vl_7b.json | `bound.i_syllables.n3.L_cp.hi` | -5.626911363695306 | −5.63 | number | 11_supplement_registered_rows.md Table S24 |
| 1080 | data/results/c_attr_1112_score/res/COPYBOUND_xm_dev500_qwen25vl_7b.json | `bound.i_syllables.n3.L_cp.label` | "REVERSED" | REVERSED | label | 11_supplement_registered_rows.md Table S24 |
| 1081 | data/results/c_attr_1112_score/res/COPYBOUND_xm_dev500_qwen25vl_7b.json | `bound.i_syllables.n3.K_nc.d` | 7.591905836734717 | +7.59 | number | 11_supplement_registered_rows.md Table S24 |
| 1082 | data/results/c_attr_1112_score/res/COPYBOUND_xm_dev500_qwen25vl_7b.json | `bound.i_syllables.n3.K_nc.lo` | 5.35626324314929 | 5.36 | number | 11_supplement_registered_rows.md Table S24 |
| 1083 | data/results/c_attr_1112_score/res/COPYBOUND_xm_dev500_qwen25vl_7b.json | `bound.i_syllables.n3.K_nc.hi` | 10.004235425661449 | 10.00 | number | 11_supplement_registered_rows.md Table S24 |
| 1084 | data/results/c_attr_1112_score/res/COPYBOUND_xm_dev500_qwen25vl_7b.json | `bound.i_syllables.n3.K_nc.label` | "DETECTED" | DETECTED | label | 11_supplement_registered_rows.md Table S24 |
| 1085 | data/results/c_attr_1112_score/res/COPYBOUND_xm_dev500_qwen25vl_7b.json | `bound.i_syllables.n3.K_rand.d` | 3.5094694485633235 | +3.51 | number | 11_supplement_registered_rows.md Table S24 |
| 1086 | data/results/c_attr_1112_score/res/COPYBOUND_xm_dev500_qwen25vl_7b.json | `bound.i_syllables.n3.K_rand.lo` | 1.9628360018907471 | 1.96 | number | 11_supplement_registered_rows.md Table S24 |
| 1087 | data/results/c_attr_1112_score/res/COPYBOUND_xm_dev500_qwen25vl_7b.json | `bound.i_syllables.n3.K_rand.hi` | 5.2323383699628865 | 5.23 | number | 11_supplement_registered_rows.md Table S24 |
| 1088 | data/results/c_attr_1112_score/res/COPYBOUND_xm_dev500_qwen25vl_7b.json | `bound.i_syllables.n3.K_ret_minus_K_nc.d` | 6.658924769304976 | +6.66 | number | 11_supplement_registered_rows.md Table S24 |
| 1089 | data/results/c_attr_1112_score/res/COPYBOUND_xm_dev500_qwen25vl_7b.json | `bound.i_syllables.n3.K_ret_minus_K_nc.lo` | 4.541798001627329 | 4.54 | number | 11_supplement_registered_rows.md Table S24 |
| 1090 | data/results/c_attr_1112_score/res/COPYBOUND_xm_dev500_qwen25vl_7b.json | `bound.i_syllables.n3.K_ret_minus_K_nc.hi` | 8.836101391162206 | 8.84 | number | 11_supplement_registered_rows.md Table S24 |
| 1091 | data/results/c_attr_1112_score/res/COPYBOUND_xm_dev500_qwen25vl_7b.json | `bound.i_syllables.n3.blind_loss.d` | 8.14903601478122 | +8.15 | number | 11_supplement_registered_rows.md Table S24 |
| 1092 | data/results/c_attr_1112_score/res/COPYBOUND_xm_dev500_qwen25vl_7b.json | `bound.i_syllables.n3.blind_loss.lo` | 6.556764675497696 | 6.56 | number | 11_supplement_registered_rows.md Table S24 |
| 1093 | data/results/c_attr_1112_score/res/COPYBOUND_xm_dev500_qwen25vl_7b.json | `bound.i_syllables.n3.blind_loss.hi` | 9.898365474877528 | 9.90 | number | 11_supplement_registered_rows.md Table S24 |
| 1094 | data/results/c_attr_1112_score/res/COPYBOUND_xm_dev500_qwen25vl_7b.json | `bound.i_syllables.n3.K_ret.tier` | "first look" | first look | label | 11_supplement_registered_rows.md Table S24 |
| 1095 | data/results/c_attr_1112_score/res/COPYBOUND_xm_dev500_qwen25vl_7b.json | `bound.i_syllables.n4.K_ret.d` | 6.812342883964858 | +6.81 | number | 11_supplement_registered_rows.md Table S24 |
| 1096 | data/results/c_attr_1112_score/res/COPYBOUND_xm_dev500_qwen25vl_7b.json | `bound.i_syllables.n4.K_ret.lo` | 4.746648080221209 | 4.75 | number | 11_supplement_registered_rows.md Table S24 |
| 1097 | data/results/c_attr_1112_score/res/COPYBOUND_xm_dev500_qwen25vl_7b.json | `bound.i_syllables.n4.K_ret.hi` | 8.903367327886812 | 8.90 | number | 11_supplement_registered_rows.md Table S24 |
| 1098 | data/results/c_attr_1112_score/res/COPYBOUND_xm_dev500_qwen25vl_7b.json | `bound.i_syllables.n4.K_ret.label` | "DETECTED" | DETECTED | label | 11_supplement_registered_rows.md Table S24 |
| 1099 | data/results/c_attr_1112_score/res/COPYBOUND_xm_dev500_qwen25vl_7b.json | `bound.i_syllables.n4.L_cp.d` | -2.3718435653908982 | −2.37 | number | 11_supplement_registered_rows.md Table S24 |
| 1100 | data/results/c_attr_1112_score/res/COPYBOUND_xm_dev500_qwen25vl_7b.json | `bound.i_syllables.n4.L_cp.lo` | -6.229241622567628 | −6.23 | number | 11_supplement_registered_rows.md Table S24 |
| 1101 | data/results/c_attr_1112_score/res/COPYBOUND_xm_dev500_qwen25vl_7b.json | `bound.i_syllables.n4.L_cp.hi` | 1.4309883419154201 | 1.43 | number | 11_supplement_registered_rows.md Table S24 |
| 1102 | data/results/c_attr_1112_score/res/COPYBOUND_xm_dev500_qwen25vl_7b.json | `bound.i_syllables.n4.L_cp.label` | "UNRESOLVED" | UNRESOLVED | label | 11_supplement_registered_rows.md Table S24 |
| 1103 | data/results/c_attr_1112_score/res/COPYBOUND_xm_dev500_qwen25vl_7b.json | `bound.i_syllables.n4.K_nc.d` | 2.5680950776003484 | +2.57 | number | 11_supplement_registered_rows.md Table S24 |
| 1104 | data/results/c_attr_1112_score/res/COPYBOUND_xm_dev500_qwen25vl_7b.json | `bound.i_syllables.n4.K_nc.lo` | 1.3468507548326003 | 1.35 | number | 11_supplement_registered_rows.md Table S24 |
| 1105 | data/results/c_attr_1112_score/res/COPYBOUND_xm_dev500_qwen25vl_7b.json | `bound.i_syllables.n4.K_nc.hi` | 3.8685392423789984 | 3.87 | number | 11_supplement_registered_rows.md Table S24 |
| 1106 | data/results/c_attr_1112_score/res/COPYBOUND_xm_dev500_qwen25vl_7b.json | `bound.i_syllables.n4.K_nc.label` | "DETECTED" | DETECTED | label | 11_supplement_registered_rows.md Table S24 |
| 1107 | data/results/c_attr_1112_score/res/COPYBOUND_xm_dev500_qwen25vl_7b.json | `bound.i_syllables.n4.K_rand.d` | 0.8327444782208586 | +0.83 | number | 11_supplement_registered_rows.md Table S24 |
| 1108 | data/results/c_attr_1112_score/res/COPYBOUND_xm_dev500_qwen25vl_7b.json | `bound.i_syllables.n4.K_rand.lo` | -0.15867395656740155 | −0.16 | number | 11_supplement_registered_rows.md Table S24 |
| 1109 | data/results/c_attr_1112_score/res/COPYBOUND_xm_dev500_qwen25vl_7b.json | `bound.i_syllables.n4.K_rand.hi` | 1.8227400329334695 | 1.82 | number | 11_supplement_registered_rows.md Table S24 |
| 1110 | data/results/c_attr_1112_score/res/COPYBOUND_xm_dev500_qwen25vl_7b.json | `bound.i_syllables.n4.K_ret_minus_K_nc.d` | 4.24424780636451 | +4.24 | number | 11_supplement_registered_rows.md Table S24 |
| 1111 | data/results/c_attr_1112_score/res/COPYBOUND_xm_dev500_qwen25vl_7b.json | `bound.i_syllables.n4.K_ret_minus_K_nc.lo` | 2.4246997486084645 | 2.42 | number | 11_supplement_registered_rows.md Table S24 |
| 1112 | data/results/c_attr_1112_score/res/COPYBOUND_xm_dev500_qwen25vl_7b.json | `bound.i_syllables.n4.K_ret_minus_K_nc.hi` | 6.205356119327505 | 6.21 | number | 11_supplement_registered_rows.md Table S24 |
| 1113 | data/results/c_attr_1112_score/res/COPYBOUND_xm_dev500_qwen25vl_7b.json | `bound.i_syllables.n4.blind_loss.d` | 6.046703186339529 | +6.05 | number | 11_supplement_registered_rows.md Table S24 |
| 1114 | data/results/c_attr_1112_score/res/COPYBOUND_xm_dev500_qwen25vl_7b.json | `bound.i_syllables.n4.blind_loss.lo` | 4.586646490047476 | 4.59 | number | 11_supplement_registered_rows.md Table S24 |
| 1115 | data/results/c_attr_1112_score/res/COPYBOUND_xm_dev500_qwen25vl_7b.json | `bound.i_syllables.n4.blind_loss.hi` | 7.698114555228794 | 7.70 | number | 11_supplement_registered_rows.md Table S24 |
| 1116 | data/results/c_attr_1112_score/res/COPYBOUND_xm_dev500_qwen25vl_7b.json | `bound.i_syllables.n4.K_ret.tier` | "first look" | first look | label | 11_supplement_registered_rows.md Table S24 |
| 1117 | data/results/c_attr_1112_score/res/COPYBOUND_xm_dev500_qwen25vl_7b.json | `bound.ii_words.n2.K_ret.d` | 18.040330379803553 | +18.04 | number | 11_supplement_registered_rows.md Table S24 |
| 1118 | data/results/c_attr_1112_score/res/COPYBOUND_xm_dev500_qwen25vl_7b.json | `bound.ii_words.n2.K_ret.lo` | 14.787952826094045 | 14.79 | number | 11_supplement_registered_rows.md Table S24 |
| 1119 | data/results/c_attr_1112_score/res/COPYBOUND_xm_dev500_qwen25vl_7b.json | `bound.ii_words.n2.K_ret.hi` | 21.03076400086946 | 21.03 | number | 11_supplement_registered_rows.md Table S24 |
| 1120 | data/results/c_attr_1112_score/res/COPYBOUND_xm_dev500_qwen25vl_7b.json | `bound.ii_words.n2.K_ret.label` | "DETECTED" | DETECTED | label | 11_supplement_registered_rows.md Table S24 |
| 1121 | data/results/c_attr_1112_score/res/COPYBOUND_xm_dev500_qwen25vl_7b.json | `bound.ii_words.n2.L_cp.d` | -13.59983106122959 | −13.60 | number | 11_supplement_registered_rows.md Table S24 |
| 1122 | data/results/c_attr_1112_score/res/COPYBOUND_xm_dev500_qwen25vl_7b.json | `bound.ii_words.n2.L_cp.lo` | -17.703332916051192 | −17.70 | number | 11_supplement_registered_rows.md Table S24 |
| 1123 | data/results/c_attr_1112_score/res/COPYBOUND_xm_dev500_qwen25vl_7b.json | `bound.ii_words.n2.L_cp.hi` | -9.346609302000388 | −9.35 | number | 11_supplement_registered_rows.md Table S24 |
| 1124 | data/results/c_attr_1112_score/res/COPYBOUND_xm_dev500_qwen25vl_7b.json | `bound.ii_words.n2.L_cp.label` | "REVERSED" | REVERSED | label | 11_supplement_registered_rows.md Table S24 |
| 1125 | data/results/c_attr_1112_score/res/COPYBOUND_xm_dev500_qwen25vl_7b.json | `bound.ii_words.n2.K_nc.d` | 9.743159630658534 | +9.74 | number | 11_supplement_registered_rows.md Table S24 |
| 1126 | data/results/c_attr_1112_score/res/COPYBOUND_xm_dev500_qwen25vl_7b.json | `bound.ii_words.n2.K_nc.lo` | 6.849585158083206 | 6.85 | number | 11_supplement_registered_rows.md Table S24 |
| 1127 | data/results/c_attr_1112_score/res/COPYBOUND_xm_dev500_qwen25vl_7b.json | `bound.ii_words.n2.K_nc.hi` | 12.665665975045336 | 12.67 | number | 11_supplement_registered_rows.md Table S24 |
| 1128 | data/results/c_attr_1112_score/res/COPYBOUND_xm_dev500_qwen25vl_7b.json | `bound.ii_words.n2.K_nc.label` | "DETECTED" | DETECTED | label | 11_supplement_registered_rows.md Table S24 |
| 1129 | data/results/c_attr_1112_score/res/COPYBOUND_xm_dev500_qwen25vl_7b.json | `bound.ii_words.n2.K_rand.d` | 6.792719337114791 | +6.79 | number | 11_supplement_registered_rows.md Table S24 |
| 1130 | data/results/c_attr_1112_score/res/COPYBOUND_xm_dev500_qwen25vl_7b.json | `bound.ii_words.n2.K_rand.lo` | 4.897928085846684 | 4.90 | number | 11_supplement_registered_rows.md Table S24 |
| 1131 | data/results/c_attr_1112_score/res/COPYBOUND_xm_dev500_qwen25vl_7b.json | `bound.ii_words.n2.K_rand.hi` | 8.879522743766422 | 8.88 | number | 11_supplement_registered_rows.md Table S24 |
| 1132 | data/results/c_attr_1112_score/res/COPYBOUND_xm_dev500_qwen25vl_7b.json | `bound.ii_words.n2.K_ret_minus_K_nc.d` | 8.297170749145014 | +8.30 | number | 11_supplement_registered_rows.md Table S24 |
| 1133 | data/results/c_attr_1112_score/res/COPYBOUND_xm_dev500_qwen25vl_7b.json | `bound.ii_words.n2.K_ret_minus_K_nc.lo` | 5.5141019177449975 | 5.51 | number | 11_supplement_registered_rows.md Table S24 |
| 1134 | data/results/c_attr_1112_score/res/COPYBOUND_xm_dev500_qwen25vl_7b.json | `bound.ii_words.n2.K_ret_minus_K_nc.hi` | 10.923125049340204 | 10.92 | number | 11_supplement_registered_rows.md Table S24 |
| 1135 | data/results/c_attr_1112_score/res/COPYBOUND_xm_dev500_qwen25vl_7b.json | `bound.ii_words.n2.blind_loss.d` | 10.24040841037189 | +10.24 | number | 11_supplement_registered_rows.md Table S24 |
| 1136 | data/results/c_attr_1112_score/res/COPYBOUND_xm_dev500_qwen25vl_7b.json | `bound.ii_words.n2.blind_loss.lo` | 8.583204396111979 | 8.58 | number | 11_supplement_registered_rows.md Table S24 |
| 1137 | data/results/c_attr_1112_score/res/COPYBOUND_xm_dev500_qwen25vl_7b.json | `bound.ii_words.n2.blind_loss.hi` | 12.056707472912914 | 12.06 | number | 11_supplement_registered_rows.md Table S24 |
| 1138 | data/results/c_attr_1112_score/res/COPYBOUND_xm_dev500_qwen25vl_7b.json | `bound.ii_words.n2.K_ret.tier` | "first look" | first look | label | 11_supplement_registered_rows.md Table S24 |
| 1139 | data/results/c_attr_1112_score/res/COPYBOUND_xm_dev500_qwen25vl_7b.json | `bound.ii_words.n3.K_ret.d` | 13.225311524965774 | +13.23 | number | 11_supplement_registered_rows.md Table S24 |
| 1140 | data/results/c_attr_1112_score/res/COPYBOUND_xm_dev500_qwen25vl_7b.json | `bound.ii_words.n3.K_ret.lo` | 10.702924207714606 | 10.70 | number | 11_supplement_registered_rows.md Table S24 |
| 1141 | data/results/c_attr_1112_score/res/COPYBOUND_xm_dev500_qwen25vl_7b.json | `bound.ii_words.n3.K_ret.hi` | 15.955657728088893 | 15.96 | number | 11_supplement_registered_rows.md Table S24 |
| 1142 | data/results/c_attr_1112_score/res/COPYBOUND_xm_dev500_qwen25vl_7b.json | `bound.ii_words.n3.K_ret.label` | "DETECTED" | DETECTED | label | 11_supplement_registered_rows.md Table S24 |
| 1143 | data/results/c_attr_1112_score/res/COPYBOUND_xm_dev500_qwen25vl_7b.json | `bound.ii_words.n3.L_cp.d` | -8.784812206391813 | −8.78 | number | 11_supplement_registered_rows.md Table S24 |
| 1144 | data/results/c_attr_1112_score/res/COPYBOUND_xm_dev500_qwen25vl_7b.json | `bound.ii_words.n3.L_cp.lo` | -12.874638721484633 | −12.87 | number | 11_supplement_registered_rows.md Table S24 |
| 1145 | data/results/c_attr_1112_score/res/COPYBOUND_xm_dev500_qwen25vl_7b.json | `bound.ii_words.n3.L_cp.hi` | -4.726277337968858 | −4.73 | number | 11_supplement_registered_rows.md Table S24 |
| 1146 | data/results/c_attr_1112_score/res/COPYBOUND_xm_dev500_qwen25vl_7b.json | `bound.ii_words.n3.L_cp.label` | "REVERSED" | REVERSED | label | 11_supplement_registered_rows.md Table S24 |
| 1147 | data/results/c_attr_1112_score/res/COPYBOUND_xm_dev500_qwen25vl_7b.json | `bound.ii_words.n3.K_nc.d` | 7.065209177258651 | +7.07 | number | 11_supplement_registered_rows.md Table S24 |
| 1148 | data/results/c_attr_1112_score/res/COPYBOUND_xm_dev500_qwen25vl_7b.json | `bound.ii_words.n3.K_nc.lo` | 5.121710989146588 | 5.12 | number | 11_supplement_registered_rows.md Table S24 |
| 1149 | data/results/c_attr_1112_score/res/COPYBOUND_xm_dev500_qwen25vl_7b.json | `bound.ii_words.n3.K_nc.hi` | 9.120985958646356 | 9.12 | number | 11_supplement_registered_rows.md Table S24 |
| 1150 | data/results/c_attr_1112_score/res/COPYBOUND_xm_dev500_qwen25vl_7b.json | `bound.ii_words.n3.K_nc.label` | "DETECTED" | DETECTED | label | 11_supplement_registered_rows.md Table S24 |
| 1151 | data/results/c_attr_1112_score/res/COPYBOUND_xm_dev500_qwen25vl_7b.json | `bound.ii_words.n3.K_rand.d` | 3.0080819946689163 | +3.01 | number | 11_supplement_registered_rows.md Table S24 |
| 1152 | data/results/c_attr_1112_score/res/COPYBOUND_xm_dev500_qwen25vl_7b.json | `bound.ii_words.n3.K_rand.lo` | 1.6862137705212634 | 1.69 | number | 11_supplement_registered_rows.md Table S24 |
| 1153 | data/results/c_attr_1112_score/res/COPYBOUND_xm_dev500_qwen25vl_7b.json | `bound.ii_words.n3.K_rand.hi` | 4.457885021251432 | 4.46 | number | 11_supplement_registered_rows.md Table S24 |
| 1154 | data/results/c_attr_1112_score/res/COPYBOUND_xm_dev500_qwen25vl_7b.json | `bound.ii_words.n3.K_ret_minus_K_nc.d` | 6.160102347707123 | +6.16 | number | 11_supplement_registered_rows.md Table S24 |
| 1155 | data/results/c_attr_1112_score/res/COPYBOUND_xm_dev500_qwen25vl_7b.json | `bound.ii_words.n3.K_ret_minus_K_nc.lo` | 4.106126890953454 | 4.11 | number | 11_supplement_registered_rows.md Table S24 |
| 1156 | data/results/c_attr_1112_score/res/COPYBOUND_xm_dev500_qwen25vl_7b.json | `bound.ii_words.n3.K_ret_minus_K_nc.hi` | 8.184550955232574 | 8.18 | number | 11_supplement_registered_rows.md Table S24 |
| 1157 | data/results/c_attr_1112_score/res/COPYBOUND_xm_dev500_qwen25vl_7b.json | `bound.ii_words.n3.blind_loss.d` | 7.986262671528752 | +7.99 | number | 11_supplement_registered_rows.md Table S24 |
| 1158 | data/results/c_attr_1112_score/res/COPYBOUND_xm_dev500_qwen25vl_7b.json | `bound.ii_words.n3.blind_loss.lo` | 6.453188762338751 | 6.45 | number | 11_supplement_registered_rows.md Table S24 |
| 1159 | data/results/c_attr_1112_score/res/COPYBOUND_xm_dev500_qwen25vl_7b.json | `bound.ii_words.n3.blind_loss.hi` | 9.764466483115319 | 9.76 | number | 11_supplement_registered_rows.md Table S24 |
| 1160 | data/results/c_attr_1112_score/res/COPYBOUND_xm_dev500_qwen25vl_7b.json | `bound.ii_words.n3.K_ret.tier` | "first look" | first look | label | 11_supplement_registered_rows.md Table S24 |
| 1161 | data/results/c_attr_1112_score/res/COPYBOUND_xm_dev500_qwen25vl_7b.json | `bound.ii_words.n4.K_ret.d` | 6.5839599732011065 | +6.58 | number | 11_supplement_registered_rows.md Table S24 |
| 1162 | data/results/c_attr_1112_score/res/COPYBOUND_xm_dev500_qwen25vl_7b.json | `bound.ii_words.n4.K_ret.lo` | 4.490347830589646 | 4.49 | number | 11_supplement_registered_rows.md Table S24 |
| 1163 | data/results/c_attr_1112_score/res/COPYBOUND_xm_dev500_qwen25vl_7b.json | `bound.ii_words.n4.K_ret.hi` | 8.844474645790115 | 8.84 | number | 11_supplement_registered_rows.md Table S24 |
| 1164 | data/results/c_attr_1112_score/res/COPYBOUND_xm_dev500_qwen25vl_7b.json | `bound.ii_words.n4.K_ret.label` | "DETECTED" | DETECTED | label | 11_supplement_registered_rows.md Table S24 |
| 1165 | data/results/c_attr_1112_score/res/COPYBOUND_xm_dev500_qwen25vl_7b.json | `bound.ii_words.n4.L_cp.d` | -2.143460654627147 | −2.14 | number | 11_supplement_registered_rows.md Table S24 |
| 1166 | data/results/c_attr_1112_score/res/COPYBOUND_xm_dev500_qwen25vl_7b.json | `bound.ii_words.n4.L_cp.lo` | -5.963066258740224 | −5.96 | number | 11_supplement_registered_rows.md Table S24 |
| 1167 | data/results/c_attr_1112_score/res/COPYBOUND_xm_dev500_qwen25vl_7b.json | `bound.ii_words.n4.L_cp.hi` | 1.7243202160026967 | 1.72 | number | 11_supplement_registered_rows.md Table S24 |
| 1168 | data/results/c_attr_1112_score/res/COPYBOUND_xm_dev500_qwen25vl_7b.json | `bound.ii_words.n4.L_cp.label` | "UNRESOLVED" | UNRESOLVED | label | 11_supplement_registered_rows.md Table S24 |
| 1169 | data/results/c_attr_1112_score/res/COPYBOUND_xm_dev500_qwen25vl_7b.json | `bound.ii_words.n4.K_nc.d` | 2.0292913663538004 | +2.03 | number | 11_supplement_registered_rows.md Table S24 |
| 1170 | data/results/c_attr_1112_score/res/COPYBOUND_xm_dev500_qwen25vl_7b.json | `bound.ii_words.n4.K_nc.lo` | 1.0324330158905317 | 1.03 | number | 11_supplement_registered_rows.md Table S24 |
| 1171 | data/results/c_attr_1112_score/res/COPYBOUND_xm_dev500_qwen25vl_7b.json | `bound.ii_words.n4.K_nc.hi` | 3.2887410414339837 | 3.29 | number | 11_supplement_registered_rows.md Table S24 |
| 1172 | data/results/c_attr_1112_score/res/COPYBOUND_xm_dev500_qwen25vl_7b.json | `bound.ii_words.n4.K_nc.label` | "DETECTED" | DETECTED | label | 11_supplement_registered_rows.md Table S24 |
| 1173 | data/results/c_attr_1112_score/res/COPYBOUND_xm_dev500_qwen25vl_7b.json | `bound.ii_words.n4.K_rand.d` | 0.7118787930901778 | +0.71 | number | 11_supplement_registered_rows.md Table S24 |
| 1174 | data/results/c_attr_1112_score/res/COPYBOUND_xm_dev500_qwen25vl_7b.json | `bound.ii_words.n4.K_rand.lo` | 0.057521708113070925 | 0.06 | number | 11_supplement_registered_rows.md Table S24 |
| 1175 | data/results/c_attr_1112_score/res/COPYBOUND_xm_dev500_qwen25vl_7b.json | `bound.ii_words.n4.K_rand.hi` | 1.5169774824300648 | 1.52 | number | 11_supplement_registered_rows.md Table S24 |
| 1176 | data/results/c_attr_1112_score/res/COPYBOUND_xm_dev500_qwen25vl_7b.json | `bound.ii_words.n4.K_ret_minus_K_nc.d` | 4.554668606847307 | +4.55 | number | 11_supplement_registered_rows.md Table S24 |
| 1177 | data/results/c_attr_1112_score/res/COPYBOUND_xm_dev500_qwen25vl_7b.json | `bound.ii_words.n4.K_ret_minus_K_nc.lo` | 2.6402259422176355 | 2.64 | number | 11_supplement_registered_rows.md Table S24 |
| 1178 | data/results/c_attr_1112_score/res/COPYBOUND_xm_dev500_qwen25vl_7b.json | `bound.ii_words.n4.K_ret_minus_K_nc.hi` | 6.514043045131512 | 6.51 | number | 11_supplement_registered_rows.md Table S24 |
| 1179 | data/results/c_attr_1112_score/res/COPYBOUND_xm_dev500_qwen25vl_7b.json | `bound.ii_words.n4.blind_loss.d` | 5.656644737789973 | +5.66 | number | 11_supplement_registered_rows.md Table S24 |
| 1180 | data/results/c_attr_1112_score/res/COPYBOUND_xm_dev500_qwen25vl_7b.json | `bound.ii_words.n4.blind_loss.lo` | 4.186508717042565 | 4.19 | number | 11_supplement_registered_rows.md Table S24 |
| 1181 | data/results/c_attr_1112_score/res/COPYBOUND_xm_dev500_qwen25vl_7b.json | `bound.ii_words.n4.blind_loss.hi` | 7.327935997857519 | 7.33 | number | 11_supplement_registered_rows.md Table S24 |
| 1182 | data/results/c_attr_1112_score/res/COPYBOUND_xm_dev500_qwen25vl_7b.json | `bound.ii_words.n4.K_ret.tier` | "first look" | first look | label | 11_supplement_registered_rows.md Table S24 |
| 1183 | data/results/c_attr_1112_score/res/COPYBOUND_xm_dev500_internvl3_8b.json | `bound.i_syllables.n2.K_ret.d` | 10.497799655550761 | +10.50 | number | 11_supplement_registered_rows.md Table S24 |
| 1184 | data/results/c_attr_1112_score/res/COPYBOUND_xm_dev500_internvl3_8b.json | `bound.i_syllables.n2.K_ret.lo` | 7.685198276598269 | 7.69 | number | 11_supplement_registered_rows.md Table S24 |
| 1185 | data/results/c_attr_1112_score/res/COPYBOUND_xm_dev500_internvl3_8b.json | `bound.i_syllables.n2.K_ret.hi` | 13.273165755958528 | 13.27 | number | 11_supplement_registered_rows.md Table S24 |
| 1186 | data/results/c_attr_1112_score/res/COPYBOUND_xm_dev500_internvl3_8b.json | `bound.i_syllables.n2.K_ret.label` | "DETECTED" | DETECTED | label | 11_supplement_registered_rows.md Table S24 |
| 1187 | data/results/c_attr_1112_score/res/COPYBOUND_xm_dev500_internvl3_8b.json | `bound.i_syllables.n2.L_cp.d` | -8.957258587876368 | −8.96 | number | 11_supplement_registered_rows.md Table S24 |
| 1188 | data/results/c_attr_1112_score/res/COPYBOUND_xm_dev500_internvl3_8b.json | `bound.i_syllables.n2.L_cp.lo` | -12.793472269768179 | −12.79 | number | 11_supplement_registered_rows.md Table S24 |
| 1189 | data/results/c_attr_1112_score/res/COPYBOUND_xm_dev500_internvl3_8b.json | `bound.i_syllables.n2.L_cp.hi` | -5.294377690294856 | −5.29 | number | 11_supplement_registered_rows.md Table S24 |
| 1190 | data/results/c_attr_1112_score/res/COPYBOUND_xm_dev500_internvl3_8b.json | `bound.i_syllables.n2.L_cp.label` | "REVERSED" | REVERSED | label | 11_supplement_registered_rows.md Table S24 |
| 1191 | data/results/c_attr_1112_score/res/COPYBOUND_xm_dev500_internvl3_8b.json | `bound.i_syllables.n2.K_nc.d` | 6.017881529277993 | +6.02 | number | 11_supplement_registered_rows.md Table S24 |
| 1192 | data/results/c_attr_1112_score/res/COPYBOUND_xm_dev500_internvl3_8b.json | `bound.i_syllables.n2.K_nc.lo` | 3.644665438330657 | 3.64 | number | 11_supplement_registered_rows.md Table S24 |
| 1193 | data/results/c_attr_1112_score/res/COPYBOUND_xm_dev500_internvl3_8b.json | `bound.i_syllables.n2.K_nc.hi` | 8.57362328596225 | 8.57 | number | 11_supplement_registered_rows.md Table S24 |
| 1194 | data/results/c_attr_1112_score/res/COPYBOUND_xm_dev500_internvl3_8b.json | `bound.i_syllables.n2.K_nc.label` | "DETECTED" | DETECTED | label | 11_supplement_registered_rows.md Table S24 |
| 1195 | data/results/c_attr_1112_score/res/COPYBOUND_xm_dev500_internvl3_8b.json | `bound.i_syllables.n2.K_rand.d` | 2.515777191731018 | +2.52 | number | 11_supplement_registered_rows.md Table S24 |
| 1196 | data/results/c_attr_1112_score/res/COPYBOUND_xm_dev500_internvl3_8b.json | `bound.i_syllables.n2.K_rand.lo` | 0.9428376165166164 | 0.94 | number | 11_supplement_registered_rows.md Table S24 |
| 1197 | data/results/c_attr_1112_score/res/COPYBOUND_xm_dev500_internvl3_8b.json | `bound.i_syllables.n2.K_rand.hi` | 4.147355708045055 | 4.15 | number | 11_supplement_registered_rows.md Table S24 |
| 1198 | data/results/c_attr_1112_score/res/COPYBOUND_xm_dev500_internvl3_8b.json | `bound.i_syllables.n2.K_ret_minus_K_nc.d` | 4.47991812627277 | +4.48 | number | 11_supplement_registered_rows.md Table S24 |
| 1199 | data/results/c_attr_1112_score/res/COPYBOUND_xm_dev500_internvl3_8b.json | `bound.i_syllables.n2.K_ret_minus_K_nc.lo` | 1.6631997095619984 | 1.66 | number | 11_supplement_registered_rows.md Table S24 |
| 1200 | data/results/c_attr_1112_score/res/COPYBOUND_xm_dev500_internvl3_8b.json | `bound.i_syllables.n2.K_ret_minus_K_nc.hi` | 7.226140538086413 | 7.23 | number | 11_supplement_registered_rows.md Table S24 |
| 1201 | data/results/c_attr_1112_score/res/COPYBOUND_xm_dev500_internvl3_8b.json | `bound.i_syllables.n2.blind_loss.d` | 9.654728776662026 | +9.65 | number | 11_supplement_registered_rows.md Table S24 |
| 1202 | data/results/c_attr_1112_score/res/COPYBOUND_xm_dev500_internvl3_8b.json | `bound.i_syllables.n2.blind_loss.lo` | 7.814256342043131 | 7.81 | number | 11_supplement_registered_rows.md Table S24 |
| 1203 | data/results/c_attr_1112_score/res/COPYBOUND_xm_dev500_internvl3_8b.json | `bound.i_syllables.n2.blind_loss.hi` | 11.506929391356957 | 11.51 | number | 11_supplement_registered_rows.md Table S24 |
| 1204 | data/results/c_attr_1112_score/res/COPYBOUND_xm_dev500_internvl3_8b.json | `bound.i_syllables.n2.K_ret.tier` | "first look" | first look | label | 11_supplement_registered_rows.md Table S24 |
| 1205 | data/results/c_attr_1112_score/res/COPYBOUND_xm_dev500_internvl3_8b.json | `bound.i_syllables.n3.K_ret.d` | 6.365504336354737 | +6.37 | number | 11_supplement_registered_rows.md Table S24 |
| 1206 | data/results/c_attr_1112_score/res/COPYBOUND_xm_dev500_internvl3_8b.json | `bound.i_syllables.n3.K_ret.lo` | 4.3486890920937915 | 4.35 | number | 11_supplement_registered_rows.md Table S24 |
| 1207 | data/results/c_attr_1112_score/res/COPYBOUND_xm_dev500_internvl3_8b.json | `bound.i_syllables.n3.K_ret.hi` | 8.588429420226277 | 8.59 | number | 11_supplement_registered_rows.md Table S24 |
| 1208 | data/results/c_attr_1112_score/res/COPYBOUND_xm_dev500_internvl3_8b.json | `bound.i_syllables.n3.K_ret.label` | "DETECTED" | DETECTED | label | 11_supplement_registered_rows.md Table S24 |
| 1209 | data/results/c_attr_1112_score/res/COPYBOUND_xm_dev500_internvl3_8b.json | `bound.i_syllables.n3.L_cp.d` | -4.824963268680341 | −4.82 | number | 11_supplement_registered_rows.md Table S24 |
| 1210 | data/results/c_attr_1112_score/res/COPYBOUND_xm_dev500_internvl3_8b.json | `bound.i_syllables.n3.L_cp.lo` | -8.721365769963858 | −8.72 | number | 11_supplement_registered_rows.md Table S24 |
| 1211 | data/results/c_attr_1112_score/res/COPYBOUND_xm_dev500_internvl3_8b.json | `bound.i_syllables.n3.L_cp.hi` | -1.0966026692992596 | −1.10 | number | 11_supplement_registered_rows.md Table S24 |
| 1212 | data/results/c_attr_1112_score/res/COPYBOUND_xm_dev500_internvl3_8b.json | `bound.i_syllables.n3.L_cp.label` | "REVERSED" | REVERSED | label | 11_supplement_registered_rows.md Table S24 |
| 1213 | data/results/c_attr_1112_score/res/COPYBOUND_xm_dev500_internvl3_8b.json | `bound.i_syllables.n3.K_nc.d` | 4.273893751222864 | +4.27 | number | 11_supplement_registered_rows.md Table S24 |
| 1214 | data/results/c_attr_1112_score/res/COPYBOUND_xm_dev500_internvl3_8b.json | `bound.i_syllables.n3.K_nc.lo` | 2.248201760049327 | 2.25 | number | 11_supplement_registered_rows.md Table S24 |
| 1215 | data/results/c_attr_1112_score/res/COPYBOUND_xm_dev500_internvl3_8b.json | `bound.i_syllables.n3.K_nc.hi` | 6.485958306410675 | 6.49 | number | 11_supplement_registered_rows.md Table S24 |
| 1216 | data/results/c_attr_1112_score/res/COPYBOUND_xm_dev500_internvl3_8b.json | `bound.i_syllables.n3.K_nc.label` | "DETECTED" | DETECTED | label | 11_supplement_registered_rows.md Table S24 |
| 1217 | data/results/c_attr_1112_score/res/COPYBOUND_xm_dev500_internvl3_8b.json | `bound.i_syllables.n3.K_rand.d` | 1.601906398010205 | +1.60 | number | 11_supplement_registered_rows.md Table S24 |
| 1218 | data/results/c_attr_1112_score/res/COPYBOUND_xm_dev500_internvl3_8b.json | `bound.i_syllables.n3.K_rand.lo` | 0.6246273718601166 | 0.62 | number | 11_supplement_registered_rows.md Table S24 |
| 1219 | data/results/c_attr_1112_score/res/COPYBOUND_xm_dev500_internvl3_8b.json | `bound.i_syllables.n3.K_rand.hi` | 2.710405874444003 | 2.71 | number | 11_supplement_registered_rows.md Table S24 |
| 1220 | data/results/c_attr_1112_score/res/COPYBOUND_xm_dev500_internvl3_8b.json | `bound.i_syllables.n3.K_ret_minus_K_nc.d` | 2.0916105851318725 | +2.09 | number | 11_supplement_registered_rows.md Table S24 |
| 1221 | data/results/c_attr_1112_score/res/COPYBOUND_xm_dev500_internvl3_8b.json | `bound.i_syllables.n3.K_ret_minus_K_nc.lo` | -0.14011459093563142 | −0.14 | number | 11_supplement_registered_rows.md Table S24 |
| 1222 | data/results/c_attr_1112_score/res/COPYBOUND_xm_dev500_internvl3_8b.json | `bound.i_syllables.n3.K_ret_minus_K_nc.hi` | 4.380066545732982 | 4.38 | number | 11_supplement_registered_rows.md Table S24 |
| 1223 | data/results/c_attr_1112_score/res/COPYBOUND_xm_dev500_internvl3_8b.json | `bound.i_syllables.n3.blind_loss.d` | 6.3884810454380485 | +6.39 | number | 11_supplement_registered_rows.md Table S24 |
| 1224 | data/results/c_attr_1112_score/res/COPYBOUND_xm_dev500_internvl3_8b.json | `bound.i_syllables.n3.blind_loss.lo` | 4.781393989937838 | 4.78 | number | 11_supplement_registered_rows.md Table S24 |
| 1225 | data/results/c_attr_1112_score/res/COPYBOUND_xm_dev500_internvl3_8b.json | `bound.i_syllables.n3.blind_loss.hi` | 8.11085308861961 | 8.11 | number | 11_supplement_registered_rows.md Table S24 |
| 1226 | data/results/c_attr_1112_score/res/COPYBOUND_xm_dev500_internvl3_8b.json | `bound.i_syllables.n3.K_ret.tier` | "first look" | first look | label | 11_supplement_registered_rows.md Table S24 |
| 1227 | data/results/c_attr_1112_score/res/COPYBOUND_xm_dev500_internvl3_8b.json | `bound.i_syllables.n4.K_ret.d` | 2.4898886151646096 | +2.49 | number | 11_supplement_registered_rows.md Table S24 |
| 1228 | data/results/c_attr_1112_score/res/COPYBOUND_xm_dev500_internvl3_8b.json | `bound.i_syllables.n4.K_ret.lo` | 1.3553100672224807 | 1.36 | number | 11_supplement_registered_rows.md Table S24 |
| 1229 | data/results/c_attr_1112_score/res/COPYBOUND_xm_dev500_internvl3_8b.json | `bound.i_syllables.n4.K_ret.hi` | 3.7571346120366194 | 3.76 | number | 11_supplement_registered_rows.md Table S24 |
| 1230 | data/results/c_attr_1112_score/res/COPYBOUND_xm_dev500_internvl3_8b.json | `bound.i_syllables.n4.K_ret.label` | "DETECTED" | DETECTED | label | 11_supplement_registered_rows.md Table S24 |
| 1231 | data/results/c_attr_1112_score/res/COPYBOUND_xm_dev500_internvl3_8b.json | `bound.i_syllables.n4.L_cp.d` | -0.949347547490215 | −0.95 | number | 11_supplement_registered_rows.md Table S24 |
| 1232 | data/results/c_attr_1112_score/res/COPYBOUND_xm_dev500_internvl3_8b.json | `bound.i_syllables.n4.L_cp.lo` | -4.803875557409168 | −4.80 | number | 11_supplement_registered_rows.md Table S24 |
| 1233 | data/results/c_attr_1112_score/res/COPYBOUND_xm_dev500_internvl3_8b.json | `bound.i_syllables.n4.L_cp.hi` | 2.8122066459059374 | 2.81 | number | 11_supplement_registered_rows.md Table S24 |
| 1234 | data/results/c_attr_1112_score/res/COPYBOUND_xm_dev500_internvl3_8b.json | `bound.i_syllables.n4.L_cp.label` | "UNRESOLVED" | UNRESOLVED | label | 11_supplement_registered_rows.md Table S24 |
| 1235 | data/results/c_attr_1112_score/res/COPYBOUND_xm_dev500_internvl3_8b.json | `bound.i_syllables.n4.K_nc.d` | 0.9762939792383616 | +0.98 | number | 11_supplement_registered_rows.md Table S24 |
| 1236 | data/results/c_attr_1112_score/res/COPYBOUND_xm_dev500_internvl3_8b.json | `bound.i_syllables.n4.K_nc.lo` | 0.028118495236403016 | 0.03 | number | 11_supplement_registered_rows.md Table S24 |
| 1237 | data/results/c_attr_1112_score/res/COPYBOUND_xm_dev500_internvl3_8b.json | `bound.i_syllables.n4.K_nc.hi` | 2.1261346294953007 | 2.13 | number | 11_supplement_registered_rows.md Table S24 |
| 1238 | data/results/c_attr_1112_score/res/COPYBOUND_xm_dev500_internvl3_8b.json | `bound.i_syllables.n4.K_nc.label` | "NEGLIGIBLE" | NEGLIGIBLE | label | 11_supplement_registered_rows.md Table S24 |
| 1239 | data/results/c_attr_1112_score/res/COPYBOUND_xm_dev500_internvl3_8b.json | `bound.i_syllables.n4.K_rand.d` | 0.7802803364298639 | +0.78 | number | 11_supplement_registered_rows.md Table S24 |
| 1240 | data/results/c_attr_1112_score/res/COPYBOUND_xm_dev500_internvl3_8b.json | `bound.i_syllables.n4.K_rand.lo` | -0.006869341383682733 | −0.01 | number | 11_supplement_registered_rows.md Table S24 |
| 1241 | data/results/c_attr_1112_score/res/COPYBOUND_xm_dev500_internvl3_8b.json | `bound.i_syllables.n4.K_rand.hi` | 1.732607418665606 | 1.73 | number | 11_supplement_registered_rows.md Table S24 |
| 1242 | data/results/c_attr_1112_score/res/COPYBOUND_xm_dev500_internvl3_8b.json | `bound.i_syllables.n4.K_ret_minus_K_nc.d` | 1.513594635926248 | +1.51 | number | 11_supplement_registered_rows.md Table S24 |
| 1243 | data/results/c_attr_1112_score/res/COPYBOUND_xm_dev500_internvl3_8b.json | `bound.i_syllables.n4.K_ret_minus_K_nc.lo` | 0.029366449276357 | 0.03 | number | 11_supplement_registered_rows.md Table S24 |
| 1244 | data/results/c_attr_1112_score/res/COPYBOUND_xm_dev500_internvl3_8b.json | `bound.i_syllables.n4.K_ret_minus_K_nc.hi` | 2.93328004764275 | 2.93 | number | 11_supplement_registered_rows.md Table S24 |
| 1245 | data/results/c_attr_1112_score/res/COPYBOUND_xm_dev500_internvl3_8b.json | `bound.i_syllables.n4.blind_loss.d` | 3.8837383216918457 | +3.88 | number | 11_supplement_registered_rows.md Table S24 |
| 1246 | data/results/c_attr_1112_score/res/COPYBOUND_xm_dev500_internvl3_8b.json | `bound.i_syllables.n4.blind_loss.lo` | 2.635316105340601 | 2.64 | number | 11_supplement_registered_rows.md Table S24 |
| 1247 | data/results/c_attr_1112_score/res/COPYBOUND_xm_dev500_internvl3_8b.json | `bound.i_syllables.n4.blind_loss.hi` | 5.253262762011963 | 5.25 | number | 11_supplement_registered_rows.md Table S24 |
| 1248 | data/results/c_attr_1112_score/res/COPYBOUND_xm_dev500_internvl3_8b.json | `bound.i_syllables.n4.K_ret.tier` | "first look" | first look | label | 11_supplement_registered_rows.md Table S24 |
| 1249 | data/results/c_attr_1112_score/res/COPYBOUND_xm_dev500_internvl3_8b.json | `bound.ii_words.n2.K_ret.d` | 10.101977267050136 | +10.10 | number | 11_supplement_registered_rows.md Table S24 |
| 1250 | data/results/c_attr_1112_score/res/COPYBOUND_xm_dev500_internvl3_8b.json | `bound.ii_words.n2.K_ret.lo` | 7.494411801288491 | 7.49 | number | 11_supplement_registered_rows.md Table S24 |
| 1251 | data/results/c_attr_1112_score/res/COPYBOUND_xm_dev500_internvl3_8b.json | `bound.ii_words.n2.K_ret.hi` | 12.730101211241104 | 12.73 | number | 11_supplement_registered_rows.md Table S24 |
| 1252 | data/results/c_attr_1112_score/res/COPYBOUND_xm_dev500_internvl3_8b.json | `bound.ii_words.n2.K_ret.label` | "DETECTED" | DETECTED | label | 11_supplement_registered_rows.md Table S24 |
| 1253 | data/results/c_attr_1112_score/res/COPYBOUND_xm_dev500_internvl3_8b.json | `bound.ii_words.n2.L_cp.d` | -8.561436199375745 | −8.56 | number | 11_supplement_registered_rows.md Table S24 |
| 1254 | data/results/c_attr_1112_score/res/COPYBOUND_xm_dev500_internvl3_8b.json | `bound.ii_words.n2.L_cp.lo` | -12.307742480030846 | −12.31 | number | 11_supplement_registered_rows.md Table S24 |
| 1255 | data/results/c_attr_1112_score/res/COPYBOUND_xm_dev500_internvl3_8b.json | `bound.ii_words.n2.L_cp.hi` | -4.930924591228911 | −4.93 | number | 11_supplement_registered_rows.md Table S24 |
| 1256 | data/results/c_attr_1112_score/res/COPYBOUND_xm_dev500_internvl3_8b.json | `bound.ii_words.n2.L_cp.label` | "REVERSED" | REVERSED | label | 11_supplement_registered_rows.md Table S24 |
| 1257 | data/results/c_attr_1112_score/res/COPYBOUND_xm_dev500_internvl3_8b.json | `bound.ii_words.n2.K_nc.d` | 5.401779073865651 | +5.40 | number | 11_supplement_registered_rows.md Table S24 |
| 1258 | data/results/c_attr_1112_score/res/COPYBOUND_xm_dev500_internvl3_8b.json | `bound.ii_words.n2.K_nc.lo` | 3.1986874552327533 | 3.20 | number | 11_supplement_registered_rows.md Table S24 |
| 1259 | data/results/c_attr_1112_score/res/COPYBOUND_xm_dev500_internvl3_8b.json | `bound.ii_words.n2.K_nc.hi` | 7.742354915348059 | 7.74 | number | 11_supplement_registered_rows.md Table S24 |
| 1260 | data/results/c_attr_1112_score/res/COPYBOUND_xm_dev500_internvl3_8b.json | `bound.ii_words.n2.K_nc.label` | "DETECTED" | DETECTED | label | 11_supplement_registered_rows.md Table S24 |
| 1261 | data/results/c_attr_1112_score/res/COPYBOUND_xm_dev500_internvl3_8b.json | `bound.ii_words.n2.K_rand.d` | 2.696866056952048 | +2.70 | number | 11_supplement_registered_rows.md Table S24 |
| 1262 | data/results/c_attr_1112_score/res/COPYBOUND_xm_dev500_internvl3_8b.json | `bound.ii_words.n2.K_rand.lo` | 1.1145627390246713 | 1.11 | number | 11_supplement_registered_rows.md Table S24 |
| 1263 | data/results/c_attr_1112_score/res/COPYBOUND_xm_dev500_internvl3_8b.json | `bound.ii_words.n2.K_rand.hi` | 4.360325913515137 | 4.36 | number | 11_supplement_registered_rows.md Table S24 |
| 1264 | data/results/c_attr_1112_score/res/COPYBOUND_xm_dev500_internvl3_8b.json | `bound.ii_words.n2.K_ret_minus_K_nc.d` | 4.700198193184487 | +4.70 | number | 11_supplement_registered_rows.md Table S24 |
| 1265 | data/results/c_attr_1112_score/res/COPYBOUND_xm_dev500_internvl3_8b.json | `bound.ii_words.n2.K_ret_minus_K_nc.lo` | 1.8662229389508513 | 1.87 | number | 11_supplement_registered_rows.md Table S24 |
| 1266 | data/results/c_attr_1112_score/res/COPYBOUND_xm_dev500_internvl3_8b.json | `bound.ii_words.n2.K_ret_minus_K_nc.hi` | 7.460483132242821 | 7.46 | number | 11_supplement_registered_rows.md Table S24 |
| 1267 | data/results/c_attr_1112_score/res/COPYBOUND_xm_dev500_internvl3_8b.json | `bound.ii_words.n2.blind_loss.d` | 9.223744659951587 | +9.22 | number | 11_supplement_registered_rows.md Table S24 |
| 1268 | data/results/c_attr_1112_score/res/COPYBOUND_xm_dev500_internvl3_8b.json | `bound.ii_words.n2.blind_loss.lo` | 7.3446607954649625 | 7.34 | number | 11_supplement_registered_rows.md Table S24 |
| 1269 | data/results/c_attr_1112_score/res/COPYBOUND_xm_dev500_internvl3_8b.json | `bound.ii_words.n2.blind_loss.hi` | 11.057319250657459 | 11.06 | number | 11_supplement_registered_rows.md Table S24 |
| 1270 | data/results/c_attr_1112_score/res/COPYBOUND_xm_dev500_internvl3_8b.json | `bound.ii_words.n2.K_ret.tier` | "first look" | first look | label | 11_supplement_registered_rows.md Table S24 |
| 1271 | data/results/c_attr_1112_score/res/COPYBOUND_xm_dev500_internvl3_8b.json | `bound.ii_words.n3.K_ret.d` | 4.919111123751006 | +4.92 | number | 11_supplement_registered_rows.md Table S24 |
| 1272 | data/results/c_attr_1112_score/res/COPYBOUND_xm_dev500_internvl3_8b.json | `bound.ii_words.n3.K_ret.lo` | 3.3659999362587487 | 3.37 | number | 11_supplement_registered_rows.md Table S24 |
| 1273 | data/results/c_attr_1112_score/res/COPYBOUND_xm_dev500_internvl3_8b.json | `bound.ii_words.n3.K_ret.hi` | 6.648879470932601 | 6.65 | number | 11_supplement_registered_rows.md Table S24 |
| 1274 | data/results/c_attr_1112_score/res/COPYBOUND_xm_dev500_internvl3_8b.json | `bound.ii_words.n3.K_ret.label` | "DETECTED" | DETECTED | label | 11_supplement_registered_rows.md Table S24 |
| 1275 | data/results/c_attr_1112_score/res/COPYBOUND_xm_dev500_internvl3_8b.json | `bound.ii_words.n3.L_cp.d` | -3.3785700560766108 | −3.38 | number | 11_supplement_registered_rows.md Table S24 |
| 1276 | data/results/c_attr_1112_score/res/COPYBOUND_xm_dev500_internvl3_8b.json | `bound.ii_words.n3.L_cp.lo` | -7.17070945510841 | −7.17 | number | 11_supplement_registered_rows.md Table S24 |
| 1277 | data/results/c_attr_1112_score/res/COPYBOUND_xm_dev500_internvl3_8b.json | `bound.ii_words.n3.L_cp.hi` | 0.2811291763762643 | 0.28 | number | 11_supplement_registered_rows.md Table S24 |
| 1278 | data/results/c_attr_1112_score/res/COPYBOUND_xm_dev500_internvl3_8b.json | `bound.ii_words.n3.L_cp.label` | "UNRESOLVED" | UNRESOLVED | label | 11_supplement_registered_rows.md Table S24 |
| 1279 | data/results/c_attr_1112_score/res/COPYBOUND_xm_dev500_internvl3_8b.json | `bound.ii_words.n3.K_nc.d` | 3.328526357577078 | +3.33 | number | 11_supplement_registered_rows.md Table S24 |
| 1280 | data/results/c_attr_1112_score/res/COPYBOUND_xm_dev500_internvl3_8b.json | `bound.ii_words.n3.K_nc.lo` | 1.8097687375483216 | 1.81 | number | 11_supplement_registered_rows.md Table S24 |
| 1281 | data/results/c_attr_1112_score/res/COPYBOUND_xm_dev500_internvl3_8b.json | `bound.ii_words.n3.K_nc.hi` | 5.068607219547311 | 5.07 | number | 11_supplement_registered_rows.md Table S24 |
| 1282 | data/results/c_attr_1112_score/res/COPYBOUND_xm_dev500_internvl3_8b.json | `bound.ii_words.n3.K_nc.label` | "DETECTED" | DETECTED | label | 11_supplement_registered_rows.md Table S24 |
| 1283 | data/results/c_attr_1112_score/res/COPYBOUND_xm_dev500_internvl3_8b.json | `bound.ii_words.n3.K_rand.d` | 1.140793076903156 | +1.14 | number | 11_supplement_registered_rows.md Table S24 |
| 1284 | data/results/c_attr_1112_score/res/COPYBOUND_xm_dev500_internvl3_8b.json | `bound.ii_words.n3.K_rand.lo` | 0.04368009568452092 | 0.04 | number | 11_supplement_registered_rows.md Table S24 |
| 1285 | data/results/c_attr_1112_score/res/COPYBOUND_xm_dev500_internvl3_8b.json | `bound.ii_words.n3.K_rand.hi` | 2.3916448615781563 | 2.39 | number | 11_supplement_registered_rows.md Table S24 |
| 1286 | data/results/c_attr_1112_score/res/COPYBOUND_xm_dev500_internvl3_8b.json | `bound.ii_words.n3.K_ret_minus_K_nc.d` | 1.5905847661739274 | +1.59 | number | 11_supplement_registered_rows.md Table S24 |
| 1287 | data/results/c_attr_1112_score/res/COPYBOUND_xm_dev500_internvl3_8b.json | `bound.ii_words.n3.K_ret_minus_K_nc.lo` | -0.3498766572777403 | −0.35 | number | 11_supplement_registered_rows.md Table S24 |
| 1288 | data/results/c_attr_1112_score/res/COPYBOUND_xm_dev500_internvl3_8b.json | `bound.ii_words.n3.K_ret_minus_K_nc.hi` | 3.445697994340238 | 3.45 | number | 11_supplement_registered_rows.md Table S24 |
| 1289 | data/results/c_attr_1112_score/res/COPYBOUND_xm_dev500_internvl3_8b.json | `bound.ii_words.n3.blind_loss.d` | 5.896662964943922 | +5.90 | number | 11_supplement_registered_rows.md Table S24 |
| 1290 | data/results/c_attr_1112_score/res/COPYBOUND_xm_dev500_internvl3_8b.json | `bound.ii_words.n3.blind_loss.lo` | 4.3456868614577635 | 4.35 | number | 11_supplement_registered_rows.md Table S24 |
| 1291 | data/results/c_attr_1112_score/res/COPYBOUND_xm_dev500_internvl3_8b.json | `bound.ii_words.n3.blind_loss.hi` | 7.568581634661702 | 7.57 | number | 11_supplement_registered_rows.md Table S24 |
| 1292 | data/results/c_attr_1112_score/res/COPYBOUND_xm_dev500_internvl3_8b.json | `bound.ii_words.n3.K_ret.tier` | "first look" | first look | label | 11_supplement_registered_rows.md Table S24 |
| 1293 | data/results/c_attr_1112_score/res/COPYBOUND_xm_dev500_internvl3_8b.json | `bound.ii_words.n4.K_ret.d` | 1.4798499753863665 | +1.48 | number | 11_supplement_registered_rows.md Table S24 |
| 1294 | data/results/c_attr_1112_score/res/COPYBOUND_xm_dev500_internvl3_8b.json | `bound.ii_words.n4.K_ret.lo` | 0.555353945537404 | 0.56 | number | 11_supplement_registered_rows.md Table S24 |
| 1295 | data/results/c_attr_1112_score/res/COPYBOUND_xm_dev500_internvl3_8b.json | `bound.ii_words.n4.K_ret.hi` | 2.567792557980423 | 2.57 | number | 11_supplement_registered_rows.md Table S24 |
| 1296 | data/results/c_attr_1112_score/res/COPYBOUND_xm_dev500_internvl3_8b.json | `bound.ii_words.n4.K_ret.label` | "UNRESOLVED" | UNRESOLVED | label | 11_supplement_registered_rows.md Table S24 |
| 1297 | data/results/c_attr_1112_score/res/COPYBOUND_xm_dev500_internvl3_8b.json | `bound.ii_words.n4.L_cp.d` | 0.0606910922880279 | +0.06 | number | 11_supplement_registered_rows.md Table S24 |
| 1298 | data/results/c_attr_1112_score/res/COPYBOUND_xm_dev500_internvl3_8b.json | `bound.ii_words.n4.L_cp.lo` | -3.82484721595028 | −3.82 | number | 11_supplement_registered_rows.md Table S24 |
| 1299 | data/results/c_attr_1112_score/res/COPYBOUND_xm_dev500_internvl3_8b.json | `bound.ii_words.n4.L_cp.hi` | 4.03519682968598 | 4.04 | number | 11_supplement_registered_rows.md Table S24 |
| 1300 | data/results/c_attr_1112_score/res/COPYBOUND_xm_dev500_internvl3_8b.json | `bound.ii_words.n4.L_cp.label` | "UNRESOLVED" | UNRESOLVED | label | 11_supplement_registered_rows.md Table S24 |
| 1301 | data/results/c_attr_1112_score/res/COPYBOUND_xm_dev500_internvl3_8b.json | `bound.ii_words.n4.K_nc.d` | 0.588802672912291 | +0.59 | number | 11_supplement_registered_rows.md Table S24 |
| 1302 | data/results/c_attr_1112_score/res/COPYBOUND_xm_dev500_internvl3_8b.json | `bound.ii_words.n4.K_nc.lo` | -0.07991579133411324 | −0.08 | number | 11_supplement_registered_rows.md Table S24 |
| 1303 | data/results/c_attr_1112_score/res/COPYBOUND_xm_dev500_internvl3_8b.json | `bound.ii_words.n4.K_nc.hi` | 1.4712506423511345 | 1.47 | number | 11_supplement_registered_rows.md Table S24 |
| 1304 | data/results/c_attr_1112_score/res/COPYBOUND_xm_dev500_internvl3_8b.json | `bound.ii_words.n4.K_nc.label` | "NEGLIGIBLE" | NEGLIGIBLE | label | 11_supplement_registered_rows.md Table S24 |
| 1305 | data/results/c_attr_1112_score/res/COPYBOUND_xm_dev500_internvl3_8b.json | `bound.ii_words.n4.K_rand.d` | 0.5861186225056713 | +0.59 | number | 11_supplement_registered_rows.md Table S24 |
| 1306 | data/results/c_attr_1112_score/res/COPYBOUND_xm_dev500_internvl3_8b.json | `bound.ii_words.n4.K_rand.lo` | 0.17897099990025891 | 0.18 | number | 11_supplement_registered_rows.md Table S24 |
| 1307 | data/results/c_attr_1112_score/res/COPYBOUND_xm_dev500_internvl3_8b.json | `bound.ii_words.n4.K_rand.hi` | 1.1310673611286532 | 1.13 | number | 11_supplement_registered_rows.md Table S24 |
| 1308 | data/results/c_attr_1112_score/res/COPYBOUND_xm_dev500_internvl3_8b.json | `bound.ii_words.n4.K_ret_minus_K_nc.d` | 0.8910473024740752 | +0.89 | number | 11_supplement_registered_rows.md Table S24 |
| 1309 | data/results/c_attr_1112_score/res/COPYBOUND_xm_dev500_internvl3_8b.json | `bound.ii_words.n4.K_ret_minus_K_nc.lo` | -0.43842615783898387 | −0.44 | number | 11_supplement_registered_rows.md Table S24 |
| 1310 | data/results/c_attr_1112_score/res/COPYBOUND_xm_dev500_internvl3_8b.json | `bound.ii_words.n4.K_ret_minus_K_nc.hi` | 2.1023807916482853 | 2.10 | number | 11_supplement_registered_rows.md Table S24 |
| 1311 | data/results/c_attr_1112_score/res/COPYBOUND_xm_dev500_internvl3_8b.json | `bound.ii_words.n4.blind_loss.d` | 3.1930530952300398 | +3.19 | number | 11_supplement_registered_rows.md Table S24 |
| 1312 | data/results/c_attr_1112_score/res/COPYBOUND_xm_dev500_internvl3_8b.json | `bound.ii_words.n4.blind_loss.lo` | 1.9956526384709623 | 2.00 | number | 11_supplement_registered_rows.md Table S24 |
| 1313 | data/results/c_attr_1112_score/res/COPYBOUND_xm_dev500_internvl3_8b.json | `bound.ii_words.n4.blind_loss.hi` | 4.508422480636732 | 4.51 | number | 11_supplement_registered_rows.md Table S24 |
| 1314 | data/results/c_attr_1112_score/res/COPYBOUND_xm_dev500_internvl3_8b.json | `bound.ii_words.n4.K_ret.tier` | "first look" | first look | label | 11_supplement_registered_rows.md Table S24 |
| 1315 | data/results/c_attr_1112_score/res/COPYBOUND_xm_dev500_aya_vision_8b.json | `bound.i_syllables.n2.K_ret.d` | 15.189464157347144 | +15.19 | number | 11_supplement_registered_rows.md Table S24 |
| 1316 | data/results/c_attr_1112_score/res/COPYBOUND_xm_dev500_aya_vision_8b.json | `bound.i_syllables.n2.K_ret.lo` | 12.50325853320605 | 12.50 | number | 11_supplement_registered_rows.md Table S24 |
| 1317 | data/results/c_attr_1112_score/res/COPYBOUND_xm_dev500_aya_vision_8b.json | `bound.i_syllables.n2.K_ret.hi` | 17.860138705000626 | 17.86 | number | 11_supplement_registered_rows.md Table S24 |
| 1318 | data/results/c_attr_1112_score/res/COPYBOUND_xm_dev500_aya_vision_8b.json | `bound.i_syllables.n2.K_ret.label` | "DETECTED" | DETECTED | label | 11_supplement_registered_rows.md Table S24 |
| 1319 | data/results/c_attr_1112_score/res/COPYBOUND_xm_dev500_aya_vision_8b.json | `bound.i_syllables.n2.L_cp.d` | -14.370616739482019 | −14.37 | number | 11_supplement_registered_rows.md Table S24 |
| 1320 | data/results/c_attr_1112_score/res/COPYBOUND_xm_dev500_aya_vision_8b.json | `bound.i_syllables.n2.L_cp.lo` | -18.389470168634638 | −18.39 | number | 11_supplement_registered_rows.md Table S24 |
| 1321 | data/results/c_attr_1112_score/res/COPYBOUND_xm_dev500_aya_vision_8b.json | `bound.i_syllables.n2.L_cp.hi` | -10.820726918860816 | −10.82 | number | 11_supplement_registered_rows.md Table S24 |
| 1322 | data/results/c_attr_1112_score/res/COPYBOUND_xm_dev500_aya_vision_8b.json | `bound.i_syllables.n2.L_cp.label` | "REVERSED" | REVERSED | label | 11_supplement_registered_rows.md Table S24 |
| 1323 | data/results/c_attr_1112_score/res/COPYBOUND_xm_dev500_aya_vision_8b.json | `bound.i_syllables.n2.K_nc.d` | 11.808371272999358 | +11.81 | number | 11_supplement_registered_rows.md Table S24 |
| 1324 | data/results/c_attr_1112_score/res/COPYBOUND_xm_dev500_aya_vision_8b.json | `bound.i_syllables.n2.K_nc.lo` | 9.397319631634618 | 9.40 | number | 11_supplement_registered_rows.md Table S24 |
| 1325 | data/results/c_attr_1112_score/res/COPYBOUND_xm_dev500_aya_vision_8b.json | `bound.i_syllables.n2.K_nc.hi` | 14.499587915420136 | 14.50 | number | 11_supplement_registered_rows.md Table S24 |
| 1326 | data/results/c_attr_1112_score/res/COPYBOUND_xm_dev500_aya_vision_8b.json | `bound.i_syllables.n2.K_nc.label` | "DETECTED" | DETECTED | label | 11_supplement_registered_rows.md Table S24 |
| 1327 | data/results/c_attr_1112_score/res/COPYBOUND_xm_dev500_aya_vision_8b.json | `bound.i_syllables.n2.K_rand.d` | 4.364486515285325 | +4.36 | number | 11_supplement_registered_rows.md Table S24 |
| 1328 | data/results/c_attr_1112_score/res/COPYBOUND_xm_dev500_aya_vision_8b.json | `bound.i_syllables.n2.K_rand.lo` | 3.0926878403400027 | 3.09 | number | 11_supplement_registered_rows.md Table S24 |
| 1329 | data/results/c_attr_1112_score/res/COPYBOUND_xm_dev500_aya_vision_8b.json | `bound.i_syllables.n2.K_rand.hi` | 5.812549306167869 | 5.81 | number | 11_supplement_registered_rows.md Table S24 |
| 1330 | data/results/c_attr_1112_score/res/COPYBOUND_xm_dev500_aya_vision_8b.json | `bound.i_syllables.n2.K_ret_minus_K_nc.d` | 3.3810928843477845 | +3.38 | number | 11_supplement_registered_rows.md Table S24 |
| 1331 | data/results/c_attr_1112_score/res/COPYBOUND_xm_dev500_aya_vision_8b.json | `bound.i_syllables.n2.K_ret_minus_K_nc.lo` | 1.0739332909256318 | 1.07 | number | 11_supplement_registered_rows.md Table S24 |
| 1332 | data/results/c_attr_1112_score/res/COPYBOUND_xm_dev500_aya_vision_8b.json | `bound.i_syllables.n2.K_ret_minus_K_nc.hi` | 5.913793926176988 | 5.91 | number | 11_supplement_registered_rows.md Table S24 |
| 1333 | data/results/c_attr_1112_score/res/COPYBOUND_xm_dev500_aya_vision_8b.json | `blind` | "NOT RUN: no admitted blind run staged" | NOT RUN: no admitted blind run staged | text | 11_supplement_registered_rows.md Table S24 |
| 1334 | data/results/c_attr_1112_score/res/COPYBOUND_xm_dev500_aya_vision_8b.json | `bound.i_syllables.n2.K_ret.tier` | "first look" | first look | label | 11_supplement_registered_rows.md Table S24 |
| 1335 | data/results/c_attr_1112_score/res/COPYBOUND_xm_dev500_aya_vision_8b.json | `bound.i_syllables.n3.K_ret.d` | 7.18214796770334 | +7.18 | number | 11_supplement_registered_rows.md Table S24 |
| 1336 | data/results/c_attr_1112_score/res/COPYBOUND_xm_dev500_aya_vision_8b.json | `bound.i_syllables.n3.K_ret.lo` | 5.347825637875918 | 5.35 | number | 11_supplement_registered_rows.md Table S24 |
| 1337 | data/results/c_attr_1112_score/res/COPYBOUND_xm_dev500_aya_vision_8b.json | `bound.i_syllables.n3.K_ret.hi` | 8.979910563316842 | 8.98 | number | 11_supplement_registered_rows.md Table S24 |
| 1338 | data/results/c_attr_1112_score/res/COPYBOUND_xm_dev500_aya_vision_8b.json | `bound.i_syllables.n3.K_ret.label` | "DETECTED" | DETECTED | label | 11_supplement_registered_rows.md Table S24 |
| 1339 | data/results/c_attr_1112_score/res/COPYBOUND_xm_dev500_aya_vision_8b.json | `bound.i_syllables.n3.L_cp.d` | -6.363300549838219 | −6.36 | number | 11_supplement_registered_rows.md Table S24 |
| 1340 | data/results/c_attr_1112_score/res/COPYBOUND_xm_dev500_aya_vision_8b.json | `bound.i_syllables.n3.L_cp.lo` | -10.106843487585213 | −10.11 | number | 11_supplement_registered_rows.md Table S24 |
| 1341 | data/results/c_attr_1112_score/res/COPYBOUND_xm_dev500_aya_vision_8b.json | `bound.i_syllables.n3.L_cp.hi` | -3.015405324741291 | −3.02 | number | 11_supplement_registered_rows.md Table S24 |
| 1342 | data/results/c_attr_1112_score/res/COPYBOUND_xm_dev500_aya_vision_8b.json | `bound.i_syllables.n3.L_cp.label` | "REVERSED" | REVERSED | label | 11_supplement_registered_rows.md Table S24 |
| 1343 | data/results/c_attr_1112_score/res/COPYBOUND_xm_dev500_aya_vision_8b.json | `bound.i_syllables.n3.K_nc.d` | 4.997852712409303 | +5.00 | number | 11_supplement_registered_rows.md Table S24 |
| 1344 | data/results/c_attr_1112_score/res/COPYBOUND_xm_dev500_aya_vision_8b.json | `bound.i_syllables.n3.K_nc.lo` | 3.473389177704702 | 3.47 | number | 11_supplement_registered_rows.md Table S24 |
| 1345 | data/results/c_attr_1112_score/res/COPYBOUND_xm_dev500_aya_vision_8b.json | `bound.i_syllables.n3.K_nc.hi` | 6.725281087653715 | 6.73 | number | 11_supplement_registered_rows.md Table S24 |
| 1346 | data/results/c_attr_1112_score/res/COPYBOUND_xm_dev500_aya_vision_8b.json | `bound.i_syllables.n3.K_nc.label` | "DETECTED" | DETECTED | label | 11_supplement_registered_rows.md Table S24 |
| 1347 | data/results/c_attr_1112_score/res/COPYBOUND_xm_dev500_aya_vision_8b.json | `bound.i_syllables.n3.K_rand.d` | 1.4245706321010105 | +1.42 | number | 11_supplement_registered_rows.md Table S24 |
| 1348 | data/results/c_attr_1112_score/res/COPYBOUND_xm_dev500_aya_vision_8b.json | `bound.i_syllables.n3.K_rand.lo` | 0.7042107390183563 | 0.70 | number | 11_supplement_registered_rows.md Table S24 |
| 1349 | data/results/c_attr_1112_score/res/COPYBOUND_xm_dev500_aya_vision_8b.json | `bound.i_syllables.n3.K_rand.hi` | 2.267213650220064 | 2.27 | number | 11_supplement_registered_rows.md Table S24 |
| 1350 | data/results/c_attr_1112_score/res/COPYBOUND_xm_dev500_aya_vision_8b.json | `bound.i_syllables.n3.K_ret_minus_K_nc.d` | 2.184295255294037 | +2.18 | number | 11_supplement_registered_rows.md Table S24 |
| 1351 | data/results/c_attr_1112_score/res/COPYBOUND_xm_dev500_aya_vision_8b.json | `bound.i_syllables.n3.K_ret_minus_K_nc.lo` | 0.456304673762884 | 0.46 | number | 11_supplement_registered_rows.md Table S24 |
| 1352 | data/results/c_attr_1112_score/res/COPYBOUND_xm_dev500_aya_vision_8b.json | `bound.i_syllables.n3.K_ret_minus_K_nc.hi` | 4.03498262943476 | 4.03 | number | 11_supplement_registered_rows.md Table S24 |
| 1353 | data/results/c_attr_1112_score/res/COPYBOUND_xm_dev500_aya_vision_8b.json | `blind` | "NOT RUN: no admitted blind run staged" | NOT RUN: no admitted blind run staged | text | 11_supplement_registered_rows.md Table S24 |
| 1354 | data/results/c_attr_1112_score/res/COPYBOUND_xm_dev500_aya_vision_8b.json | `bound.i_syllables.n3.K_ret.tier` | "first look" | first look | label | 11_supplement_registered_rows.md Table S24 |
| 1355 | data/results/c_attr_1112_score/res/COPYBOUND_xm_dev500_aya_vision_8b.json | `bound.i_syllables.n4.K_ret.d` | 2.7545909939711617 | +2.75 | number | 11_supplement_registered_rows.md Table S24 |
| 1356 | data/results/c_attr_1112_score/res/COPYBOUND_xm_dev500_aya_vision_8b.json | `bound.i_syllables.n4.K_ret.lo` | 1.5524855294138633 | 1.55 | number | 11_supplement_registered_rows.md Table S24 |
| 1357 | data/results/c_attr_1112_score/res/COPYBOUND_xm_dev500_aya_vision_8b.json | `bound.i_syllables.n4.K_ret.hi` | 4.138600280888201 | 4.14 | number | 11_supplement_registered_rows.md Table S24 |
| 1358 | data/results/c_attr_1112_score/res/COPYBOUND_xm_dev500_aya_vision_8b.json | `bound.i_syllables.n4.K_ret.label` | "DETECTED" | DETECTED | label | 11_supplement_registered_rows.md Table S24 |
| 1359 | data/results/c_attr_1112_score/res/COPYBOUND_xm_dev500_aya_vision_8b.json | `bound.i_syllables.n4.L_cp.d` | -1.9357435761060409 | −1.94 | number | 11_supplement_registered_rows.md Table S24 |
| 1360 | data/results/c_attr_1112_score/res/COPYBOUND_xm_dev500_aya_vision_8b.json | `bound.i_syllables.n4.L_cp.lo` | -5.527799856989129 | −5.53 | number | 11_supplement_registered_rows.md Table S24 |
| 1361 | data/results/c_attr_1112_score/res/COPYBOUND_xm_dev500_aya_vision_8b.json | `bound.i_syllables.n4.L_cp.hi` | 1.2290136805265768 | 1.23 | number | 11_supplement_registered_rows.md Table S24 |
| 1362 | data/results/c_attr_1112_score/res/COPYBOUND_xm_dev500_aya_vision_8b.json | `bound.i_syllables.n4.L_cp.label` | "UNRESOLVED" | UNRESOLVED | label | 11_supplement_registered_rows.md Table S24 |
| 1363 | data/results/c_attr_1112_score/res/COPYBOUND_xm_dev500_aya_vision_8b.json | `bound.i_syllables.n4.K_nc.d` | 2.0606360290606007 | +2.06 | number | 11_supplement_registered_rows.md Table S24 |
| 1364 | data/results/c_attr_1112_score/res/COPYBOUND_xm_dev500_aya_vision_8b.json | `bound.i_syllables.n4.K_nc.lo` | 1.0414171034155268 | 1.04 | number | 11_supplement_registered_rows.md Table S24 |
| 1365 | data/results/c_attr_1112_score/res/COPYBOUND_xm_dev500_aya_vision_8b.json | `bound.i_syllables.n4.K_nc.hi` | 3.2139121870483445 | 3.21 | number | 11_supplement_registered_rows.md Table S24 |
| 1366 | data/results/c_attr_1112_score/res/COPYBOUND_xm_dev500_aya_vision_8b.json | `bound.i_syllables.n4.K_nc.label` | "DETECTED" | DETECTED | label | 11_supplement_registered_rows.md Table S24 |
| 1367 | data/results/c_attr_1112_score/res/COPYBOUND_xm_dev500_aya_vision_8b.json | `bound.i_syllables.n4.K_rand.d` | 0.5289777931869218 | +0.53 | number | 11_supplement_registered_rows.md Table S24 |
| 1368 | data/results/c_attr_1112_score/res/COPYBOUND_xm_dev500_aya_vision_8b.json | `bound.i_syllables.n4.K_rand.lo` | 0.122038896806509 | 0.12 | number | 11_supplement_registered_rows.md Table S24 |
| 1369 | data/results/c_attr_1112_score/res/COPYBOUND_xm_dev500_aya_vision_8b.json | `bound.i_syllables.n4.K_rand.hi` | 0.9705697369269303 | 0.97 | number | 11_supplement_registered_rows.md Table S24 |
| 1370 | data/results/c_attr_1112_score/res/COPYBOUND_xm_dev500_aya_vision_8b.json | `bound.i_syllables.n4.K_ret_minus_K_nc.d` | 0.6939549649105607 | +0.69 | number | 11_supplement_registered_rows.md Table S24 |
| 1371 | data/results/c_attr_1112_score/res/COPYBOUND_xm_dev500_aya_vision_8b.json | `bound.i_syllables.n4.K_ret_minus_K_nc.lo` | -0.6969085532507457 | −0.70 | number | 11_supplement_registered_rows.md Table S24 |
| 1372 | data/results/c_attr_1112_score/res/COPYBOUND_xm_dev500_aya_vision_8b.json | `bound.i_syllables.n4.K_ret_minus_K_nc.hi` | 2.202660419969026 | 2.20 | number | 11_supplement_registered_rows.md Table S24 |
| 1373 | data/results/c_attr_1112_score/res/COPYBOUND_xm_dev500_aya_vision_8b.json | `blind` | "NOT RUN: no admitted blind run staged" | NOT RUN: no admitted blind run staged | text | 11_supplement_registered_rows.md Table S24 |
| 1374 | data/results/c_attr_1112_score/res/COPYBOUND_xm_dev500_aya_vision_8b.json | `bound.i_syllables.n4.K_ret.tier` | "first look" | first look | label | 11_supplement_registered_rows.md Table S24 |
| 1375 | data/results/c_attr_1112_score/res/COPYBOUND_xm_dev500_aya_vision_8b.json | `bound.ii_words.n2.K_ret.d` | 13.706763903137139 | +13.71 | number | 11_supplement_registered_rows.md Table S24 |
| 1376 | data/results/c_attr_1112_score/res/COPYBOUND_xm_dev500_aya_vision_8b.json | `bound.ii_words.n2.K_ret.lo` | 11.044719804172543 | 11.04 | number | 11_supplement_registered_rows.md Table S24 |
| 1377 | data/results/c_attr_1112_score/res/COPYBOUND_xm_dev500_aya_vision_8b.json | `bound.ii_words.n2.K_ret.hi` | 16.34214961144768 | 16.34 | number | 11_supplement_registered_rows.md Table S24 |
| 1378 | data/results/c_attr_1112_score/res/COPYBOUND_xm_dev500_aya_vision_8b.json | `bound.ii_words.n2.K_ret.label` | "DETECTED" | DETECTED | label | 11_supplement_registered_rows.md Table S24 |
| 1379 | data/results/c_attr_1112_score/res/COPYBOUND_xm_dev500_aya_vision_8b.json | `bound.ii_words.n2.L_cp.d` | -12.887916485272017 | −12.89 | number | 11_supplement_registered_rows.md Table S24 |
| 1380 | data/results/c_attr_1112_score/res/COPYBOUND_xm_dev500_aya_vision_8b.json | `bound.ii_words.n2.L_cp.lo` | -16.76367512354203 | −16.76 | number | 11_supplement_registered_rows.md Table S24 |
| 1381 | data/results/c_attr_1112_score/res/COPYBOUND_xm_dev500_aya_vision_8b.json | `bound.ii_words.n2.L_cp.hi` | -9.440807342903225 | −9.44 | number | 11_supplement_registered_rows.md Table S24 |
| 1382 | data/results/c_attr_1112_score/res/COPYBOUND_xm_dev500_aya_vision_8b.json | `bound.ii_words.n2.L_cp.label` | "REVERSED" | REVERSED | label | 11_supplement_registered_rows.md Table S24 |
| 1383 | data/results/c_attr_1112_score/res/COPYBOUND_xm_dev500_aya_vision_8b.json | `bound.ii_words.n2.K_nc.d` | 10.249308028136948 | +10.25 | number | 11_supplement_registered_rows.md Table S24 |
| 1384 | data/results/c_attr_1112_score/res/COPYBOUND_xm_dev500_aya_vision_8b.json | `bound.ii_words.n2.K_nc.lo` | 8.023209207353093 | 8.02 | number | 11_supplement_registered_rows.md Table S24 |
| 1385 | data/results/c_attr_1112_score/res/COPYBOUND_xm_dev500_aya_vision_8b.json | `bound.ii_words.n2.K_nc.hi` | 12.794999286642843 | 12.79 | number | 11_supplement_registered_rows.md Table S24 |
| 1386 | data/results/c_attr_1112_score/res/COPYBOUND_xm_dev500_aya_vision_8b.json | `bound.ii_words.n2.K_nc.label` | "DETECTED" | DETECTED | label | 11_supplement_registered_rows.md Table S24 |
| 1387 | data/results/c_attr_1112_score/res/COPYBOUND_xm_dev500_aya_vision_8b.json | `bound.ii_words.n2.K_rand.d` | 4.220567372366594 | +4.22 | number | 11_supplement_registered_rows.md Table S24 |
| 1388 | data/results/c_attr_1112_score/res/COPYBOUND_xm_dev500_aya_vision_8b.json | `bound.ii_words.n2.K_rand.lo` | 2.9662244079266546 | 2.97 | number | 11_supplement_registered_rows.md Table S24 |
| 1389 | data/results/c_attr_1112_score/res/COPYBOUND_xm_dev500_aya_vision_8b.json | `bound.ii_words.n2.K_rand.hi` | 5.640717929800841 | 5.64 | number | 11_supplement_registered_rows.md Table S24 |
| 1390 | data/results/c_attr_1112_score/res/COPYBOUND_xm_dev500_aya_vision_8b.json | `bound.ii_words.n2.K_ret_minus_K_nc.d` | 3.457455875000193 | +3.46 | number | 11_supplement_registered_rows.md Table S24 |
| 1391 | data/results/c_attr_1112_score/res/COPYBOUND_xm_dev500_aya_vision_8b.json | `bound.ii_words.n2.K_ret_minus_K_nc.lo` | 1.1330389547450255 | 1.13 | number | 11_supplement_registered_rows.md Table S24 |
| 1392 | data/results/c_attr_1112_score/res/COPYBOUND_xm_dev500_aya_vision_8b.json | `bound.ii_words.n2.K_ret_minus_K_nc.hi` | 6.055777805721517 | 6.06 | number | 11_supplement_registered_rows.md Table S24 |
| 1393 | data/results/c_attr_1112_score/res/COPYBOUND_xm_dev500_aya_vision_8b.json | `blind` | "NOT RUN: no admitted blind run staged" | NOT RUN: no admitted blind run staged | text | 11_supplement_registered_rows.md Table S24 |
| 1394 | data/results/c_attr_1112_score/res/COPYBOUND_xm_dev500_aya_vision_8b.json | `bound.ii_words.n2.K_ret.tier` | "first look" | first look | label | 11_supplement_registered_rows.md Table S24 |
| 1395 | data/results/c_attr_1112_score/res/COPYBOUND_xm_dev500_aya_vision_8b.json | `bound.ii_words.n3.K_ret.d` | 5.69235564018542 | +5.69 | number | 11_supplement_registered_rows.md Table S24 |
| 1396 | data/results/c_attr_1112_score/res/COPYBOUND_xm_dev500_aya_vision_8b.json | `bound.ii_words.n3.K_ret.lo` | 4.033461631205525 | 4.03 | number | 11_supplement_registered_rows.md Table S24 |
| 1397 | data/results/c_attr_1112_score/res/COPYBOUND_xm_dev500_aya_vision_8b.json | `bound.ii_words.n3.K_ret.hi` | 7.449728473624756 | 7.45 | number | 11_supplement_registered_rows.md Table S24 |
| 1398 | data/results/c_attr_1112_score/res/COPYBOUND_xm_dev500_aya_vision_8b.json | `bound.ii_words.n3.K_ret.label` | "DETECTED" | DETECTED | label | 11_supplement_registered_rows.md Table S24 |
| 1399 | data/results/c_attr_1112_score/res/COPYBOUND_xm_dev500_aya_vision_8b.json | `bound.ii_words.n3.L_cp.d` | -4.8735082223203 | −4.87 | number | 11_supplement_registered_rows.md Table S24 |
| 1400 | data/results/c_attr_1112_score/res/COPYBOUND_xm_dev500_aya_vision_8b.json | `bound.ii_words.n3.L_cp.lo` | -8.612374737950532 | −8.61 | number | 11_supplement_registered_rows.md Table S24 |
| 1401 | data/results/c_attr_1112_score/res/COPYBOUND_xm_dev500_aya_vision_8b.json | `bound.ii_words.n3.L_cp.hi` | -1.5062229898819266 | −1.51 | number | 11_supplement_registered_rows.md Table S24 |
| 1402 | data/results/c_attr_1112_score/res/COPYBOUND_xm_dev500_aya_vision_8b.json | `bound.ii_words.n3.L_cp.label` | "REVERSED" | REVERSED | label | 11_supplement_registered_rows.md Table S24 |
| 1403 | data/results/c_attr_1112_score/res/COPYBOUND_xm_dev500_aya_vision_8b.json | `bound.ii_words.n3.K_nc.d` | 4.091567756359667 | +4.09 | number | 11_supplement_registered_rows.md Table S24 |
| 1404 | data/results/c_attr_1112_score/res/COPYBOUND_xm_dev500_aya_vision_8b.json | `bound.ii_words.n3.K_nc.lo` | 2.663845967648181 | 2.66 | number | 11_supplement_registered_rows.md Table S24 |
| 1405 | data/results/c_attr_1112_score/res/COPYBOUND_xm_dev500_aya_vision_8b.json | `bound.ii_words.n3.K_nc.hi` | 5.725164499160832 | 5.73 | number | 11_supplement_registered_rows.md Table S24 |
| 1406 | data/results/c_attr_1112_score/res/COPYBOUND_xm_dev500_aya_vision_8b.json | `bound.ii_words.n3.K_nc.label` | "DETECTED" | DETECTED | label | 11_supplement_registered_rows.md Table S24 |
| 1407 | data/results/c_attr_1112_score/res/COPYBOUND_xm_dev500_aya_vision_8b.json | `bound.ii_words.n3.K_rand.d` | 1.1345598415779459 | +1.13 | number | 11_supplement_registered_rows.md Table S24 |
| 1408 | data/results/c_attr_1112_score/res/COPYBOUND_xm_dev500_aya_vision_8b.json | `bound.ii_words.n3.K_rand.lo` | 0.5236813292476826 | 0.52 | number | 11_supplement_registered_rows.md Table S24 |
| 1409 | data/results/c_attr_1112_score/res/COPYBOUND_xm_dev500_aya_vision_8b.json | `bound.ii_words.n3.K_rand.hi` | 1.8787741271164746 | 1.88 | number | 11_supplement_registered_rows.md Table S24 |
| 1410 | data/results/c_attr_1112_score/res/COPYBOUND_xm_dev500_aya_vision_8b.json | `bound.ii_words.n3.K_ret_minus_K_nc.d` | 1.6007878838257543 | +1.60 | number | 11_supplement_registered_rows.md Table S24 |
| 1411 | data/results/c_attr_1112_score/res/COPYBOUND_xm_dev500_aya_vision_8b.json | `bound.ii_words.n3.K_ret_minus_K_nc.lo` | -0.06982485168273747 | −0.07 | number | 11_supplement_registered_rows.md Table S24 |
| 1412 | data/results/c_attr_1112_score/res/COPYBOUND_xm_dev500_aya_vision_8b.json | `bound.ii_words.n3.K_ret_minus_K_nc.hi` | 3.4859052595618576 | 3.49 | number | 11_supplement_registered_rows.md Table S24 |
| 1413 | data/results/c_attr_1112_score/res/COPYBOUND_xm_dev500_aya_vision_8b.json | `blind` | "NOT RUN: no admitted blind run staged" | NOT RUN: no admitted blind run staged | text | 11_supplement_registered_rows.md Table S24 |
| 1414 | data/results/c_attr_1112_score/res/COPYBOUND_xm_dev500_aya_vision_8b.json | `bound.ii_words.n3.K_ret.tier` | "first look" | first look | label | 11_supplement_registered_rows.md Table S24 |
| 1415 | data/results/c_attr_1112_score/res/COPYBOUND_xm_dev500_aya_vision_8b.json | `bound.ii_words.n4.K_ret.d` | 2.594823573247706 | +2.59 | number | 11_supplement_registered_rows.md Table S24 |
| 1416 | data/results/c_attr_1112_score/res/COPYBOUND_xm_dev500_aya_vision_8b.json | `bound.ii_words.n4.K_ret.lo` | 1.5064393287976694 | 1.51 | number | 11_supplement_registered_rows.md Table S24 |
| 1417 | data/results/c_attr_1112_score/res/COPYBOUND_xm_dev500_aya_vision_8b.json | `bound.ii_words.n4.K_ret.hi` | 3.874122745257287 | 3.87 | number | 11_supplement_registered_rows.md Table S24 |
| 1418 | data/results/c_attr_1112_score/res/COPYBOUND_xm_dev500_aya_vision_8b.json | `bound.ii_words.n4.K_ret.label` | "DETECTED" | DETECTED | label | 11_supplement_registered_rows.md Table S24 |
| 1419 | data/results/c_attr_1112_score/res/COPYBOUND_xm_dev500_aya_vision_8b.json | `bound.ii_words.n4.L_cp.d` | -1.7759761553825848 | −1.78 | number | 11_supplement_registered_rows.md Table S24 |
| 1420 | data/results/c_attr_1112_score/res/COPYBOUND_xm_dev500_aya_vision_8b.json | `bound.ii_words.n4.L_cp.lo` | -5.335497244452532 | −5.34 | number | 11_supplement_registered_rows.md Table S24 |
| 1421 | data/results/c_attr_1112_score/res/COPYBOUND_xm_dev500_aya_vision_8b.json | `bound.ii_words.n4.L_cp.hi` | 1.3745760473560429 | 1.37 | number | 11_supplement_registered_rows.md Table S24 |
| 1422 | data/results/c_attr_1112_score/res/COPYBOUND_xm_dev500_aya_vision_8b.json | `bound.ii_words.n4.L_cp.label` | "UNRESOLVED" | UNRESOLVED | label | 11_supplement_registered_rows.md Table S24 |
| 1423 | data/results/c_attr_1112_score/res/COPYBOUND_xm_dev500_aya_vision_8b.json | `bound.ii_words.n4.K_nc.d` | 0.7036376092330172 | +0.70 | number | 11_supplement_registered_rows.md Table S24 |
| 1424 | data/results/c_attr_1112_score/res/COPYBOUND_xm_dev500_aya_vision_8b.json | `bound.ii_words.n4.K_nc.lo` | 0.017812163589399466 | 0.02 | number | 11_supplement_registered_rows.md Table S24 |
| 1425 | data/results/c_attr_1112_score/res/COPYBOUND_xm_dev500_aya_vision_8b.json | `bound.ii_words.n4.K_nc.hi` | 1.4904111494618377 | 1.49 | number | 11_supplement_registered_rows.md Table S24 |
| 1426 | data/results/c_attr_1112_score/res/COPYBOUND_xm_dev500_aya_vision_8b.json | `bound.ii_words.n4.K_nc.label` | "NEGLIGIBLE" | NEGLIGIBLE | label | 11_supplement_registered_rows.md Table S24 |
| 1427 | data/results/c_attr_1112_score/res/COPYBOUND_xm_dev500_aya_vision_8b.json | `bound.ii_words.n4.K_rand.d` | 0.2580662980526264 | +0.26 | number | 11_supplement_registered_rows.md Table S24 |
| 1428 | data/results/c_attr_1112_score/res/COPYBOUND_xm_dev500_aya_vision_8b.json | `bound.ii_words.n4.K_rand.lo` | 0.03690578638560481 | 0.04 | number | 11_supplement_registered_rows.md Table S24 |
| 1429 | data/results/c_attr_1112_score/res/COPYBOUND_xm_dev500_aya_vision_8b.json | `bound.ii_words.n4.K_rand.hi` | 0.5293928140432492 | 0.53 | number | 11_supplement_registered_rows.md Table S24 |
| 1430 | data/results/c_attr_1112_score/res/COPYBOUND_xm_dev500_aya_vision_8b.json | `bound.ii_words.n4.K_ret_minus_K_nc.d` | 1.8911859640146889 | +1.89 | number | 11_supplement_registered_rows.md Table S24 |
| 1431 | data/results/c_attr_1112_score/res/COPYBOUND_xm_dev500_aya_vision_8b.json | `bound.ii_words.n4.K_ret_minus_K_nc.lo` | 0.7202063532372673 | 0.72 | number | 11_supplement_registered_rows.md Table S24 |
| 1432 | data/results/c_attr_1112_score/res/COPYBOUND_xm_dev500_aya_vision_8b.json | `bound.ii_words.n4.K_ret_minus_K_nc.hi` | 3.3043660863962354 | 3.30 | number | 11_supplement_registered_rows.md Table S24 |
| 1433 | data/results/c_attr_1112_score/res/COPYBOUND_xm_dev500_aya_vision_8b.json | `blind` | "NOT RUN: no admitted blind run staged" | NOT RUN: no admitted blind run staged | text | 11_supplement_registered_rows.md Table S24 |
| 1434 | data/results/c_attr_1112_score/res/COPYBOUND_xm_dev500_aya_vision_8b.json | `bound.ii_words.n4.K_ret.tier` | "first look" | first look | label | 11_supplement_registered_rows.md Table S24 |
| 1435 | data/results/c_attr_1112_score/res/DFSENS.json | `rows.tau_pair.nominated` | true | yes | label | 11_supplement_registered_rows.md Table S25 |
| 1436 | data/results/c_attr_1112_score/res/DFSENS.json | `rows.tau_pair.d` | 7.304953006288278 | +7.30 | number | 11_supplement_registered_rows.md Table S25 |
| 1437 | data/results/c_attr_1112_score/res/DFSENS.json | `rows.tau_pair.lo_df_resampled` | 5.686531327633289 | 5.69 | number | 11_supplement_registered_rows.md Table S25 |
| 1438 | data/results/c_attr_1112_score/res/DFSENS.json | `rows.tau_pair.hi_df_resampled` | 9.12866141965415 | 9.13 | number | 11_supplement_registered_rows.md Table S25 |
| 1439 | data/results/c_attr_1112_score/res/DFSENS.json | `rows.tau_pair.lo_df_fixed` | 5.646121362136599 | 5.65 | number | 11_supplement_registered_rows.md Table S25 |
| 1440 | data/results/c_attr_1112_score/res/DFSENS.json | `rows.tau_pair.hi_df_fixed` | 9.136034079107976 | 9.14 | number | 11_supplement_registered_rows.md Table S25 |
| 1441 | data/results/c_attr_1112_score/res/DFSENS.json | `rows.tau_marg.nominated` | false | no | label | 11_supplement_registered_rows.md Table S25 |
| 1442 | data/results/c_attr_1112_score/res/DFSENS.json | `rows.tau_marg.d` | 0.9615087710524601 | +0.96 | number | 11_supplement_registered_rows.md Table S25 |
| 1443 | data/results/c_attr_1112_score/res/DFSENS.json | `rows.tau_marg.lo_df_resampled` | 0.1654131866872407 | 0.17 | number | 11_supplement_registered_rows.md Table S25 |
| 1444 | data/results/c_attr_1112_score/res/DFSENS.json | `rows.tau_marg.hi_df_resampled` | 1.8932401102759575 | 1.89 | number | 11_supplement_registered_rows.md Table S25 |
| 1445 | data/results/c_attr_1112_score/res/DFSENS.json | `rows.tau_marg.lo_df_fixed` | 0.07815268475336169 | 0.08 | number | 11_supplement_registered_rows.md Table S25 |
| 1446 | data/results/c_attr_1112_score/res/DFSENS.json | `rows.tau_marg.hi_df_fixed` | 1.9372417578188075 | 1.94 | number | 11_supplement_registered_rows.md Table S25 |
| 1447 | data/results/c_attr_1112_score/res/POSTHOC.json | `swap.rows.qwen25vl_7b.tau_sel_f30k.d` | -0.39711900000000017 | −0.40 | number | 11_supplement_registered_rows.md Table S25 |
| 1448 | data/results/c_attr_1112_score/res/POSTHOC.json | `swap.rows.qwen25vl_7b.tau_sel_f30k.lo` | -2.8089804849999993 | −2.81 | number | 11_supplement_registered_rows.md Table S25 |
| 1449 | data/results/c_attr_1112_score/res/POSTHOC.json | `swap.rows.qwen25vl_7b.tau_sel_f30k.hi` | 2.055883577499998 | 2.06 | number | 11_supplement_registered_rows.md Table S25 |
| 1450 | data/results/c_attr_1112_score/res/POSTHOC.json | `swap.rows.qwen25vl_7b.tau_sel_coco.d` | 5.039755500000001 | +5.04 | number | 11_supplement_registered_rows.md Table S25 |
| 1451 | data/results/c_attr_1112_score/res/POSTHOC.json | `swap.rows.qwen25vl_7b.tau_sel_coco.lo` | 2.3857199450000004 | 2.39 | number | 11_supplement_registered_rows.md Table S25 |
| 1452 | data/results/c_attr_1112_score/res/POSTHOC.json | `swap.rows.qwen25vl_7b.tau_sel_coco.hi` | 7.670817754999995 | 7.67 | number | 11_supplement_registered_rows.md Table S25 |
| 1453 | data/results/c_attr_1112_score/res/POSTHOC.json | `swap.rows.qwen25vl_7b.delta.d` | -5.436874500000001 | −5.44 | number | 11_supplement_registered_rows.md Table S25 |
| 1454 | data/results/c_attr_1112_score/res/POSTHOC.json | `swap.rows.qwen25vl_7b.delta.lo` | -9.0747935025 | −9.07 | number | 11_supplement_registered_rows.md Table S25 |
| 1455 | data/results/c_attr_1112_score/res/POSTHOC.json | `swap.rows.qwen25vl_7b.delta.hi` | -2.0357453625000015 | −2.04 | number | 11_supplement_registered_rows.md Table S25 |
| 1456 | data/results/c_attr_1112_score/res/POSTHOC.json | `swap.rows.qwen25vl_7b.delta.label` | "REVERSED" | REVERSED | label | 11_supplement_registered_rows.md Table S25 |
| 1457 | data/results/c_attr_1112_score/res/POSTHOC.json | `swap.rows.aya_vision_8b.tau_sel_f30k.d` | 6.114182500000001 | +6.11 | number | 11_supplement_registered_rows.md Table S25 |
| 1458 | data/results/c_attr_1112_score/res/POSTHOC.json | `swap.rows.aya_vision_8b.tau_sel_f30k.lo` | 3.7111273699999994 | 3.71 | number | 11_supplement_registered_rows.md Table S25 |
| 1459 | data/results/c_attr_1112_score/res/POSTHOC.json | `swap.rows.aya_vision_8b.tau_sel_f30k.hi` | 8.51815423 | 8.52 | number | 11_supplement_registered_rows.md Table S25 |
| 1460 | data/results/c_attr_1112_score/res/POSTHOC.json | `swap.rows.aya_vision_8b.tau_sel_coco.d` | 6.1240937 | +6.12 | number | 11_supplement_registered_rows.md Table S25 |
| 1461 | data/results/c_attr_1112_score/res/POSTHOC.json | `swap.rows.aya_vision_8b.tau_sel_coco.lo` | 3.4746893999999995 | 3.47 | number | 11_supplement_registered_rows.md Table S25 |
| 1462 | data/results/c_attr_1112_score/res/POSTHOC.json | `swap.rows.aya_vision_8b.tau_sel_coco.hi` | 8.778537847499996 | 8.78 | number | 11_supplement_registered_rows.md Table S25 |
| 1463 | data/results/c_attr_1112_score/res/POSTHOC.json | `swap.rows.aya_vision_8b.delta.d` | -0.009911199999999454 | −0.01 | number | 11_supplement_registered_rows.md Table S25 |
| 1464 | data/results/c_attr_1112_score/res/POSTHOC.json | `swap.rows.aya_vision_8b.delta.lo` | -3.4165317724999995 | −3.42 | number | 11_supplement_registered_rows.md Table S25 |
| 1465 | data/results/c_attr_1112_score/res/POSTHOC.json | `swap.rows.aya_vision_8b.delta.hi` | 3.3571946975000024 | 3.36 | number | 11_supplement_registered_rows.md Table S25 |
| 1466 | data/results/c_attr_1112_score/res/POSTHOC.json | `swap.rows.aya_vision_8b.delta.label` | "UNRESOLVED" | UNRESOLVED | label | 11_supplement_registered_rows.md Table S25 |
| 1467 | .session_backup/machines/ATTR_H1/root/outputs/c_attr/logs/job.log | `gpu_h` | "6.41" | 6.41 | label | 06_results.md |
| 1468 | .session_backup/machines/ATTR_H1/root/outputs/c_attr_b1/CAP_1B.json | `cap_h` | 17.949664828683932 | 17.95 | number | 06_results.md |
| 1469 | .session_backup/machines/ATTR_H1/root/outputs/c_attr_b1/logs/job.log | `gpu_h` | "12.27" | 12.27 | label | 06_results.md |
| 1470 | .session_backup/machines/ATTR_H1/root/outputs/c_attr_b1/STEPS_1B.tsv | `n_b1_runs` | 50 | 50 | number | 06_results.md |
| 1471 | .session_backup/machines/ATTR_H1/root/outputs/c_attr/parity/S10b_qwen25vl_7b.json | `identical` | 42 | 42 | number | 06_results.md |
| 1472 | .session_backup/machines/ATTR_H1/root/outputs/c_attr/parity/S10b_qwen25vl_7b.json | `n` | 50 | 50 | number | 06_results.md |
| 1473 | .session_backup/machines/ATTR_H1/root/outputs/c_attr/parity/S10b_internvl3_8b.json | `identical` | 37 | 37 | number | 06_results.md |
| 1474 | .session_backup/machines/ATTR_H1/root/outputs/c_attr/parity/S10b_internvl3_8b.json | `n` | 50 | 50 | number | 06_results.md |
| 1475 | .session_backup/machines/ATTR_H1/root/outputs/c_attr/parity/S10b_aya_vision_8b.json | `identical` | 31 | 31 | number | 06_results.md |
| 1476 | .session_backup/machines/ATTR_H1/root/outputs/c_attr/parity/S10b_aya_vision_8b.json | `n` | 50 | 50 | number | 06_results.md |
| 1477 | .session_backup/machines/ATTR_H1/root/outputs/c_attr/parity/S10b_qwen25vl_7b.json | `failing_ids` | 8 | 8 | count | 06_results.md |
| 1478 | .session_backup/machines/ATTR_H1/root/outputs/c_attr/parity/S10b_internvl3_8b.json | `failing_ids` | 13 | 13 | count | 06_results.md |
| 1479 | .session_backup/machines/ATTR_H1/root/outputs/c_attr/parity/S10b_aya_vision_8b.json | `failing_ids` | 19 | 19 | count | 06_results.md |
| 1480 | .session_backup/machines/ATTR_H1/root/outputs/c_attr_b1/parity/D1_qwen25vl_7b.json | `identical` | 50 | 50 | number | 06_results.md |
| 1481 | .session_backup/machines/ATTR_H1/root/outputs/c_attr_b1/parity/D1_qwen25vl_7b.json | `n` | 50 | 50 | number | 06_results.md |
| 1482 | .session_backup/machines/ATTR_H1/root/outputs/c_attr_b1/parity/D1_internvl3_8b.json | `identical` | 50 | 50 | number | 06_results.md |
| 1483 | .session_backup/machines/ATTR_H1/root/outputs/c_attr_b1/parity/D1_internvl3_8b.json | `n` | 50 | 50 | number | 06_results.md |
| 1484 | .session_backup/machines/ATTR_H1/root/outputs/c_attr_b1/parity/D1_aya_vision_8b.json | `identical` | 50 | 50 | number | 06_results.md |
| 1485 | .session_backup/machines/ATTR_H1/root/outputs/c_attr_b1/parity/D1_aya_vision_8b.json | `n` | 50 | 50 | number | 06_results.md |
| 1486 | .session_backup/machines/ATTR_H1/root/outputs/c_attr/logs/job.log | `gpu_h` | "6.41" | 6.41 | label | 06_results.md |
| 1487 | .session_backup/machines/ATTR_H1/root/outputs/c_attr_b1/logs/job.log | `gpu_h` | "12.27" | 12.27 | label | 06_results.md |
| 1488 | .session_backup/machines/ATTR_H1/root/outputs/c_attr_b1/CAP_1B.json | `cap_h` | 17.949664828683932 | 17.95 | number | 06_results.md |
| 1489 | .session_backup/machines/ATTR_H1/root/outputs/c_attr/parity/S10b_qwen25vl_7b.json | `failing_ids` | 8 | 8 | count | 09_limitations.md |
| 1490 | .session_backup/machines/ATTR_H1/root/outputs/c_attr/parity/S10b_internvl3_8b.json | `failing_ids` | 13 | 13 | count | 09_limitations.md |
| 1491 | .session_backup/machines/ATTR_H1/root/outputs/c_attr/parity/S10b_aya_vision_8b.json | `failing_ids` | 19 | 19 | count | 09_limitations.md |
| 1492 | .session_backup/machines/ATTR_H1/root/outputs/c_attr/parity/S10a_qwen25vl_7b_ov_dev_b.json | `identical` | 50 | 50 | number | 11_supplement_registered_rows.md |
| 1493 | .session_backup/machines/ATTR_H1/root/outputs/c_attr/parity/S10a_qwen25vl_7b_ov_dev_b.json | `n` | 50 | 50 | number | 11_supplement_registered_rows.md |
| 1494 | .session_backup/machines/ATTR_H1/root/outputs/c_attr/parity/S10a_qwen25vl_7b_ov_dev_a.json | `identical` | 50 | 50 | number | 11_supplement_registered_rows.md |
| 1495 | .session_backup/machines/ATTR_H1/root/outputs/c_attr/parity/S10a_qwen25vl_7b_ov_dev_a.json | `n` | 50 | 50 | number | 11_supplement_registered_rows.md |
| 1496 | .session_backup/machines/ATTR_H1/root/outputs/c_attr/parity/S10b_qwen25vl_7b.json | `identical` | 42 | 42 | number | 11_supplement_registered_rows.md |
| 1497 | .session_backup/machines/ATTR_H1/root/outputs/c_attr/parity/S10b_qwen25vl_7b.json | `n` | 50 | 50 | number | 11_supplement_registered_rows.md |
| 1498 | .session_backup/machines/ATTR_H1/root/outputs/c_attr/parity/STEP10_qwen25vl_7b.json | `A1` | "FAIL" | FAIL (K1 fired) | label | 11_supplement_registered_rows.md |
| 1499 | .session_backup/machines/ATTR_H1/root/outputs/c_attr_b1/parity/D1_qwen25vl_7b.json | `identical` | 50 | 50 | number | 11_supplement_registered_rows.md |
| 1500 | .session_backup/machines/ATTR_H1/root/outputs/c_attr_b1/parity/D1_qwen25vl_7b.json | `n` | 50 | 50 | number | 11_supplement_registered_rows.md |
| 1501 | .session_backup/machines/ATTR_H1/root/outputs/c_attr_b1/parity/STEP1B0_qwen25vl_7b.json | `D1` | "PASS" | PASS | label | 11_supplement_registered_rows.md |
| 1502 | .session_backup/machines/ATTR_H1/root/outputs/c_attr/parity/S10a_internvl3_8b_ov_dev_b.json | `identical` | 50 | 50 | number | 11_supplement_registered_rows.md |
| 1503 | .session_backup/machines/ATTR_H1/root/outputs/c_attr/parity/S10a_internvl3_8b_ov_dev_b.json | `n` | 50 | 50 | number | 11_supplement_registered_rows.md |
| 1504 | .session_backup/machines/ATTR_H1/root/outputs/c_attr/parity/S10a_internvl3_8b_ov_dev_a.json | `identical` | 50 | 50 | number | 11_supplement_registered_rows.md |
| 1505 | .session_backup/machines/ATTR_H1/root/outputs/c_attr/parity/S10a_internvl3_8b_ov_dev_a.json | `n` | 50 | 50 | number | 11_supplement_registered_rows.md |
| 1506 | .session_backup/machines/ATTR_H1/root/outputs/c_attr/parity/S10b_internvl3_8b.json | `identical` | 37 | 37 | number | 11_supplement_registered_rows.md |
| 1507 | .session_backup/machines/ATTR_H1/root/outputs/c_attr/parity/S10b_internvl3_8b.json | `n` | 50 | 50 | number | 11_supplement_registered_rows.md |
| 1508 | .session_backup/machines/ATTR_H1/root/outputs/c_attr/parity/STEP10_internvl3_8b.json | `A1` | "FAIL" | FAIL (K1 fired) | label | 11_supplement_registered_rows.md |
| 1509 | .session_backup/machines/ATTR_H1/root/outputs/c_attr_b1/parity/D1_internvl3_8b.json | `identical` | 50 | 50 | number | 11_supplement_registered_rows.md |
| 1510 | .session_backup/machines/ATTR_H1/root/outputs/c_attr_b1/parity/D1_internvl3_8b.json | `n` | 50 | 50 | number | 11_supplement_registered_rows.md |
| 1511 | .session_backup/machines/ATTR_H1/root/outputs/c_attr_b1/parity/STEP1B0_internvl3_8b.json | `D1` | "PASS" | PASS | label | 11_supplement_registered_rows.md |
| 1512 | .session_backup/machines/ATTR_H1/root/outputs/c_attr/parity/S10a_aya_vision_8b_ov_dev_b.json | `identical` | 50 | 50 | number | 11_supplement_registered_rows.md |
| 1513 | .session_backup/machines/ATTR_H1/root/outputs/c_attr/parity/S10a_aya_vision_8b_ov_dev_b.json | `n` | 50 | 50 | number | 11_supplement_registered_rows.md |
| 1514 | .session_backup/machines/ATTR_H1/root/outputs/c_attr/parity/S10b_aya_vision_8b.json | `identical` | 31 | 31 | number | 11_supplement_registered_rows.md |
| 1515 | .session_backup/machines/ATTR_H1/root/outputs/c_attr/parity/S10b_aya_vision_8b.json | `n` | 50 | 50 | number | 11_supplement_registered_rows.md |
| 1516 | .session_backup/machines/ATTR_H1/root/outputs/c_attr/parity/STEP10_aya_vision_8b.json | `A1` | "FAIL" | FAIL (K1 fired) | label | 11_supplement_registered_rows.md |
| 1517 | .session_backup/machines/ATTR_H1/root/outputs/c_attr_b1/parity/D1_aya_vision_8b.json | `identical` | 50 | 50 | number | 11_supplement_registered_rows.md |
| 1518 | .session_backup/machines/ATTR_H1/root/outputs/c_attr_b1/parity/D1_aya_vision_8b.json | `n` | 50 | 50 | number | 11_supplement_registered_rows.md |
| 1519 | .session_backup/machines/ATTR_H1/root/outputs/c_attr_b1/parity/STEP1B0_aya_vision_8b.json | `D1` | "PASS" | PASS | label | 11_supplement_registered_rows.md |
| 1520 | scripts/c_attr/block0/K0_REPORT.json | `diagnostics.ov_dev_a.p1.refill_share_8` | 0.0 | 0.000000 | number | 11_supplement_registered_rows.md |
| 1521 | scripts/c_attr/block0/K0_REPORT.json | `diagnostics.ov_dev_a.p1.refill_gate` | "pass" | pass | label | 11_supplement_registered_rows.md |
| 1522 | scripts/c_attr/block0/K0_REPORT.json | `diagnostics.ov_dev_a.p1.overlap_with_ret_4` | 0.000549 | 0.0005 | number | 11_supplement_registered_rows.md |
| 1523 | scripts/c_attr/block0/K0_REPORT.json | `diagnostics.ov_dev_a.p1.overlap_with_ret_8` | 0.001921 | 0.0019 | number | 11_supplement_registered_rows.md |
| 1524 | scripts/c_attr/block0/K0_REPORT.json | `diagnostics.ov_dev_a.p1.mean_cos_ret_8` | 0.786842 | 0.787 | number | 11_supplement_registered_rows.md |
| 1525 | scripts/c_attr/block0/K0_REPORT.json | `diagnostics.ov_dev_a.p1.mean_cos_perm_8` | 0.539218 | 0.539 | number | 11_supplement_registered_rows.md |
| 1526 | scripts/c_attr/block0/K0_REPORT.json | `diagnostics.ov_dev_a.p1.mean_cos_rand_d0_8` | 0.511611 | 0.512 | number | 11_supplement_registered_rows.md |
| 1527 | scripts/c_attr/block0/K0_REPORT.json | `diagnostics.ov_dev_a.p2.refill_share_8` | 0.000137 | 0.000137 | number | 11_supplement_registered_rows.md |
| 1528 | scripts/c_attr/block0/K0_REPORT.json | `diagnostics.ov_dev_a.p2.refill_gate` | "pass" | pass | label | 11_supplement_registered_rows.md |
| 1529 | scripts/c_attr/block0/K0_REPORT.json | `diagnostics.ov_dev_a.p2.overlap_with_ret_4` | 0.000823 | 0.0008 | number | 11_supplement_registered_rows.md |
| 1530 | scripts/c_attr/block0/K0_REPORT.json | `diagnostics.ov_dev_a.p2.overlap_with_ret_8` | 0.003293 | 0.0033 | number | 11_supplement_registered_rows.md |
| 1531 | scripts/c_attr/block0/K0_REPORT.json | `diagnostics.ov_dev_a.p2.mean_cos_ret_8` | 0.786842 | 0.787 | number | 11_supplement_registered_rows.md |
| 1532 | scripts/c_attr/block0/K0_REPORT.json | `diagnostics.ov_dev_a.p2.mean_cos_perm_8` | 0.539081 | 0.539 | number | 11_supplement_registered_rows.md |
| 1533 | scripts/c_attr/block0/K0_REPORT.json | `diagnostics.ov_dev_a.p2.mean_cos_rand_d0_8` | 0.511611 | 0.512 | number | 11_supplement_registered_rows.md |
| 1534 | scripts/c_attr/block0/K0_REPORT.json | `diagnostics.ov_dev_b.p1.refill_share_8` | 0.0 | 0.000000 | number | 11_supplement_registered_rows.md |
| 1535 | scripts/c_attr/block0/K0_REPORT.json | `diagnostics.ov_dev_b.p1.refill_gate` | "pass" | pass | label | 11_supplement_registered_rows.md |
| 1536 | scripts/c_attr/block0/K0_REPORT.json | `diagnostics.ov_dev_b.p1.overlap_with_ret_4` | 0.00027 | 0.0003 | number | 11_supplement_registered_rows.md |
| 1537 | scripts/c_attr/block0/K0_REPORT.json | `diagnostics.ov_dev_b.p1.overlap_with_ret_8` | 0.001216 | 0.0012 | number | 11_supplement_registered_rows.md |
| 1538 | scripts/c_attr/block0/K0_REPORT.json | `diagnostics.ov_dev_b.p1.mean_cos_ret_8` | 0.785404 | 0.785 | number | 11_supplement_registered_rows.md |
| 1539 | scripts/c_attr/block0/K0_REPORT.json | `diagnostics.ov_dev_b.p1.mean_cos_perm_8` | 0.540412 | 0.540 | number | 11_supplement_registered_rows.md |
| 1540 | scripts/c_attr/block0/K0_REPORT.json | `diagnostics.ov_dev_b.p1.mean_cos_rand_d0_8` | 0.510352 | 0.510 | number | 11_supplement_registered_rows.md |
| 1541 | scripts/c_attr/block0/K0_REPORT.json | `diagnostics.ov_dev_b.p2.refill_share_8` | 0.0 | 0.000000 | number | 11_supplement_registered_rows.md |
| 1542 | scripts/c_attr/block0/K0_REPORT.json | `diagnostics.ov_dev_b.p2.refill_gate` | "pass" | pass | label | 11_supplement_registered_rows.md |
| 1543 | scripts/c_attr/block0/K0_REPORT.json | `diagnostics.ov_dev_b.p2.overlap_with_ret_4` | 0.001622 | 0.0016 | number | 11_supplement_registered_rows.md |
| 1544 | scripts/c_attr/block0/K0_REPORT.json | `diagnostics.ov_dev_b.p2.overlap_with_ret_8` | 0.002973 | 0.0030 | number | 11_supplement_registered_rows.md |
| 1545 | scripts/c_attr/block0/K0_REPORT.json | `diagnostics.ov_dev_b.p2.mean_cos_ret_8` | 0.785404 | 0.785 | number | 11_supplement_registered_rows.md |
| 1546 | scripts/c_attr/block0/K0_REPORT.json | `diagnostics.ov_dev_b.p2.mean_cos_perm_8` | 0.539737 | 0.540 | number | 11_supplement_registered_rows.md |
| 1547 | scripts/c_attr/block0/K0_REPORT.json | `diagnostics.ov_dev_b.p2.mean_cos_rand_d0_8` | 0.510352 | 0.510 | number | 11_supplement_registered_rows.md |
| 1548 | scripts/c_attr/block0/K0_REPORT.json | `diagnostics.xm_dev500.p1.refill_share_8` | 0.0 | 0.000000 | number | 11_supplement_registered_rows.md |
| 1549 | scripts/c_attr/block0/K0_REPORT.json | `diagnostics.xm_dev500.p1.refill_gate` | "pass" | pass | label | 11_supplement_registered_rows.md |
| 1550 | scripts/c_attr/block0/K0_REPORT.json | `diagnostics.xm_dev500.p1.overlap_with_ret_4` | 0.008 | 0.0080 | number | 11_supplement_registered_rows.md |
| 1551 | scripts/c_attr/block0/K0_REPORT.json | `diagnostics.xm_dev500.p1.overlap_with_ret_8` | 0.0135 | 0.0135 | number | 11_supplement_registered_rows.md |
| 1552 | scripts/c_attr/block0/K0_REPORT.json | `diagnostics.xm_dev500.p1.mean_cos_ret_8` | 0.62178 | 0.622 | number | 11_supplement_registered_rows.md |
| 1553 | scripts/c_attr/block0/K0_REPORT.json | `diagnostics.xm_dev500.p1.mean_cos_perm_8` | 0.469958 | 0.470 | number | 11_supplement_registered_rows.md |
| 1554 | scripts/c_attr/block0/K0_REPORT.json | `diagnostics.xm_dev500.p1.mean_cos_rand_d0_8` | 0.403164 | 0.403 | number | 11_supplement_registered_rows.md |
| 1555 | scripts/c_attr/block0/K0_REPORT.json | `diagnostics.xm_dev500.p2.refill_share_8` | 0.0 | 0.000000 | number | 11_supplement_registered_rows.md |
| 1556 | scripts/c_attr/block0/K0_REPORT.json | `diagnostics.xm_dev500.p2.refill_gate` | "pass" | pass | label | 11_supplement_registered_rows.md |
| 1557 | scripts/c_attr/block0/K0_REPORT.json | `diagnostics.xm_dev500.p2.overlap_with_ret_4` | 0.0065 | 0.0065 | number | 11_supplement_registered_rows.md |
| 1558 | scripts/c_attr/block0/K0_REPORT.json | `diagnostics.xm_dev500.p2.overlap_with_ret_8` | 0.00925 | 0.0093 | number | 11_supplement_registered_rows.md |
| 1559 | scripts/c_attr/block0/K0_REPORT.json | `diagnostics.xm_dev500.p2.mean_cos_ret_8` | 0.62178 | 0.622 | number | 11_supplement_registered_rows.md |
| 1560 | scripts/c_attr/block0/K0_REPORT.json | `diagnostics.xm_dev500.p2.mean_cos_perm_8` | 0.467674 | 0.468 | number | 11_supplement_registered_rows.md |
| 1561 | scripts/c_attr/block0/K0_REPORT.json | `diagnostics.xm_dev500.p2.mean_cos_rand_d0_8` | 0.403164 | 0.403 | number | 11_supplement_registered_rows.md |
| 1562 | scripts/c_attr/block0/K0_REPORT.json | `diagnostics.ov_dev_a.same_donor_p1_p2` | 4 | 4 | number | 11_supplement_registered_rows.md |
| 1563 | scripts/c_attr/block0/K0_REPORT.json | `diagnostics.ov_dev_b.same_donor_p1_p2` | 2 | 2 | number | 11_supplement_registered_rows.md |
| 1564 | scripts/c_attr/block0/K0_REPORT.json | `diagnostics.xm_dev500.same_donor_p1_p2` | 0 | 0 | number | 11_supplement_registered_rows.md |

(Row keys write `|` as `~`, as the package does.)
