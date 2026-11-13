# Paper A certification: PHASE B paper-text transfer record (for a one-judge diff read)

Written 2026-11-12T23:20Z, revised 2026-11-12T23:33:03Z (`date -u`) by the transfer operator (revision: TG4 labels added to the count line, the H2b W2 sentences, the H3 and H1 secondary sentences, the H2a remainder and H2d replicate lines and the Part V null/M-label paragraph; Part P log time corrected to 10:45; UTC dates in two comments; record overclaims corrected). Home S (CC-369 Ruling 6: entry gate not met).

**CUSTODY (CC-369 H-5).** This record, `A_PHASE_B.diff` and the paper files it names carry part-1 figures derived from the PI's answers (H-1) and Part V/P figures. They may sit in the paper repo; the coordinator must not show or quote them to the PI before the H-1 release event, and nothing here goes to the second annotator (H-4). The paper text must not be pushed while the second annotator can read the repo (CC-373 W3).

**What this is.** An UNCOMMITTED working-tree change to `/mnt/d/vsps_papers/vsps-paperA-spic` (branch `main`, HEAD `c58a0be22cbbf8325d5ea39d4bcc1785d7b33d01`, `git status --short` empty before the run). Nothing staged, committed, stashed or pushed in either repo. No LOG or CC file written. No build, no pandoc/LaTeX, no scoring code run.

- Built by `a_phase_b_transfer.py` (this folder): `python3 -I a_phase_b_transfer.py`. It starts from `git show HEAD:` of every target file, so a re-run is idempotent (it was re-run several times while fixing wording; the last run's `after` shas are those below). It writes `a_phase_b_report.json` (rows, departures, NEW TEXT list, file shas, word counts, TG9 counts).
- The script asserts: the sha256 of the package, the four result files (each also = run-repo HEAD blob) and the four registrations; paper HEAD; every package line used starts with its expected lead-in; every OLD occurs exactly once; the CC-375 C5 base shas of sec5 and both supplements; the stored verdict strings (`registered.*` of the label result and of Part V) from which every outcome sentence is selected; the filled sentences equal the rulings' filled texts (CC-369 Ruling 5: H1a PASS, H2a NOT EVALUABLE, H3 RESPECTED figures; CC-360 Ruling 3 (a), (d), (h)); CC-369 W3 coverage counts (4 and 1 of 12 at 0.30; 12 of 12 at 0.50) recomputed from the stored H2b rows; the S11 block is byte-identical in the two supplement files; the closing checks below.
- Every result, freeze or Part V/P value the script places goes through one getter that reads `file::key` and appends its `number_manifest.tsv` row in the same call, so the manifest value is the stored value as formatted. Not through the getter: (i) literal design constants inside copied package method text and own captions (for example 27 images with three references, 30 bisection steps, [0.001, 1], 36 pairs, 20 draws, 720 pair-draws, 94 pairs, 72/5/72, the 10 and 11 thresholds, 0.067 in the quoted SESOI rationale); 50 registered constants are keyed to their registration lines, the rest are 'literal, no new row', as in Phase A; (ii) numbers already in the paper at HEAD on lines that were re-written (the abstract and Section 1 paragraph); (iii) section, table, model and seed tokens. A sweep of the 9,224 numeric tokens on added lines found no result value outside the manifest other than these categories (operator check, not scripted).

## Sources

| Source | sha256 |
|---|---|
| Package `paper_text/A_CERT_PAPER_TEXT_v1.md` | `d2548abc…` (= CC-357 TARGET, committed 867fb07) (TG1) |
| `data/results/a_cert/score/A_CERT_RESULT.json` | `7492a16c…` (PIN-1112-a-cert-RESULT; committed 03ba1a2) |
| `data/results/a_cert/freeze/FREEZE.json` | `c51ea7dc…` (OPS-1112h) |
| `data/results/a_cert_v/score/A_CERT_V_RESULT.json` | `2675cdce…` (PIN-1112-a-vp-RESULT) |
| `data/results/a_cert_p/score/A_CERT_P_RESULT.json` | `a05edf41…` (PIN-1112-a-p-RESULT) |
| R11 v1.1 / VP v1.1 / H2D v1.3 / PLAN v1.1 | `e564b7b1…` / `0e586fa9…` / `d0afcaf0…` / `8ad28f67…` |
| Rulings read in full | CC-357, CC-360, CC-369, CC-373, CC-375; FIX_A2 §3, §6, §7 |
| arXiv 2611.01712 abstract page | fetched once on 2026-11-12 (UTC) during this task, for the bib fields only (four authors' full names, title, 1 Nov 2026, cs.LG) |

Not opened: `~/vsps_labels/`, any `key.json`, `data/results/a_cert_e3/`, `data/results/a_e3/`, `~/.vsps_sealed`, any `gt_cache.json`, `~/bpa1pull_1108`, `.session_backup/machines/`, `a1_precheck/raw/`, `FREEZE_V.json` (not needed: V1 evaluable). `gate.json` hashed only (f04d2142…). LOG read through `cut -c1-300` (tail l.2363–2403 at 230 characters; pin lines located by id). The scoring code `a_cert.py` was read at l.805–836 only, to state the definition of the per-class U/A rate (S11.7a).

**Preconditions (CC-357 Ruling 5 Phase B; CC-373 "Phase B must, first").** A_CERT result read: CC-369. Part V/P reads: CC-360. FIX_A2 own read: CC-375 (closed only at this diff read by byte match, W1). Gate CC line: CC-369 Ruling 6 (Home S). No PI line before the `score` start (TG7; OPS-1113p W8 record), so no H2d clause. LOG re-checked at 23:16Z: 2,403 lines; no second-annotator start line, no top-up session line, no PI answer to P-2/P-3/Q-A/Q-B.

## Rows

### Applied (63 replacements + appended blocks; every OLD exactly once)

| Row (ruling) | File | Note |
|---|---|---|
| FIX_A2 W-01, W-04 (CC-375 Ruling 4 string for W-04) | sec5 | |
| FIX_A2 W-02, W-03, W-05, W-06 (CC-375 strings for W-05/W-06), W-07, Q6 | both supplements | identical in both |
| CC-375 W2: citation-map and in-text-trace rows for `lam2020uit` in sec5 | citation_map_A_v2.tsv, intext_trace_A.tsv | plus two rows each for the new arXiv 2611.01712 citation (sec2, sec11) |
| E6 (9.1 precision rule, sentence H1-9.1 filled) | sec11 | |
| E7/N1 (CC-357 J-4) | sec11 | Home S pointers (departure list) |
| E11: Table 1 new row group (seven verdicts by name + count line + W2), Development row, Post hoc row entry | sec1 | |
| E11 count line in 8.5 (+ W2 sentence for H2b) | sec10 | |
| E12 count part: count line in the S10 copy of 8.5 | both supplements | |
| E13 clause (CC-369 Ruling 5 / W7, verbatim) | sec7 6.2 Reading; sec1 confirmatory claim; sec10 8.5; cover letter; abstract; S10 copies of Section 1 and 8.5 in both supplements | highlight: see conflicts K3 |
| J-39 paragraph "Outcome for the certificate" (H2a NOT EVALUABLE sentence, H2b PASS + W2, H2d reading with label, count line) | sec7 6.7 | NEW TEXT lead (gate statement) |
| N2 / C6 run fact "The scoring ran once, on 2026-11-12, with no fault." | sec7 6.7 One pass | OPS-1112ch; commit 03ba1a2 message |
| C4(b) l.170 → "Supplementary S11.1"; l.181 → "(Section 6.7.3)" | sec7 | |
| C5 pointers: "the certificate of Supplementary S11" (Freeze, Why labels), H2a/H2b/H2d → S11.4 (Multiplicity; 9.1 statistical conclusion), $V_m$ one-line definition in 6.7.4 Universe | sec7, sec11 | |
| C1 renumbering: 6.7.1, 6.7.2 kept; 6.7.3 = §2.5 per-system intervals (Home S main text); 6.7.5 → 6.7.4 (H3); every "Section 6.7.5" pointer updated | sec7, sec5, sec11, S11, S1.M.6 | no gap |
| C7/N4 captions with "new labels on previously analysed captions" on every 6.7 table (6.7a–6.7f) | sec7 | Table 6.7d (freeze) caption: see conflicts K6 |
| §2.8 "Facts fixed before unsealing" with FREEZE ranges, both J-15 labels | sec7 6.7.2 | |
| §3.2 Table 6.7b → Table 6.7c (H1 results), secondary corner row, H1a/H1b/H1c PASS sentences, all-three [reg] sentence | sec7 6.7.2 | |
| §2.5 + Table 6.7a′ → 6.7.3 + Table 6.7d, J-42 note | sec7 | |
| §3.5 Table 6.7f (with J-17 parenthetical, W16), H3 RESPECTED sentence, W5 ratio and 108 count | sec7 6.7.4 | |
| §3.6 Table 6.7g → Table 6.7a (quality; W5 rows) | sec7 6.7.1 | kappa row not printed (deferred) |
| §4 paragraphs: internal validity (J-19 → pointer to S11.4), assumptions, development and post hoc rows (J-19 → pointer to S11.5), prior work, other-family arm (J-27 one sentence), 9.2 released logs (+ P-3 default clause) | sec11 | |
| §3.5 Section 5.4 sentence; S1.M.6 sentence | sec5; both supplements | |
| §2.4 prior-work sentence after the species-accumulation sentence; bib entry `fernandezbarrios2026disagreement` | sec2; paperA.bib | Home S pointer |
| RQ4 (W10), Contribution 6 (Home S shell, W11b) | sec1 | |
| 8.1 pointer sentence (CC-360 Ruling 3(h), filled; asserted equal) | sec10 | |
| Abstract: E13 clause, seven-count clause (W6), "a proposed certificate was not validated"; cuts to 250 words (J-34) | abstract_A.md | NEW TEXT |
| Highlight (Home S, 77 characters) replacing highlight 3 | highlights_A.md | conflict K3 |
| S4.0 rows A31–A37 (the seven), D-1–D-4 (Part V, development), P-5 (Part P, post hoc); times paragraph (J-28: next free ids checked: A30 last, P-4 last, no D- ids) | both supplements | |
| S11 (S11.1–S11.8), identical in both supplement files | both supplements | |
| number_manifest rows | number_manifest.tsv | 2,495 rows, lines 1448–3942 |

### Not applied: condition not met (outcome-selected)

E3 (Home M only); E4 (only on H1b/H1c FAIL); E5 (only on H1a FAIL); H1 FAIL / INCONCLUSIVE sentences; H2a PASS / VALID, NOT DISCRIMINATING / FAIL sentences; H2a exact-limit sentence (`exact_lower_limit` absent) and margin sentence (`margin_beats_certificate` false); H2b FAIL / freeze-FAIL / PASS (vacuous); H2d PASS / NOT EVALUABLE forms and `fail_adds` (null); H3 VIOLATED / INCONCLUSIVE / NOT EVALUABLE; V1 FAIL / NOT EVALUABLE; V2 SUPPORTED; V3 NOT DISCRIMINATING; COCO K2 PASS; KV1 sentence; Part P dropped / not-run sentences; all Home M shells (Sections 3.8 and 6.8, Home M abstract/contribution/highlight); the H2d gate clause (no PI line, TG7); J-40 text (no second fault). Section 3.3 sentence: Home S keeps the existing 3.3 sentence unchanged (placement table "Supplementary S11.6; the Section 3.3 sentence kept"); nothing added.

### Deferred (listed, not written)

| Item | Why |
|---|---|
| Kappa sentences, Table 6.7a kappa row, "(single annotator)" → kappa form | second annotator has not labelled; kappa unscored (J-13, J-14; CC-369 Ruling 5). Every label-based number keeps "single annotator". |
| Part-2 secondary rows; part-3 repeat-agreement figure | later unsealing (CC-369 H-3). Only "partial (0 of 150 answered at the part-1 unsealing)" is printed. |
| CC-369 disclosure sentence (l.287–298, date 2026-11-12 from OPS-1113q) and C8 post-relay count | it stands beside the part-2 rows, the repeat figure and the top-up rows, none of which exists; its clause "withheld from him until he had finished all his labelling" is not yet a fact; the count needs a later split-code read of a closed file. No ruling grants a pending key in paper text (Phase A rule: no `{{` in paper text). See conflict K9. |
| Top-up / E-rows / S11.9 and the E3 §8 disclosure | top-up session not held, E3 result not read (J-27; CC-369 H-2). Only the one J-27 sentence is in 9.1. |
| Table 2.1 row for arXiv 2611.01712 (J-10) | cells must come from that paper's text; only the abstract was fetched (bib fields). |
| Part V per-unit listings: 36-row pair table, 720 $w^*$-beside-truth rows, 1,440 per-cell $\hat w$ | registered "reported whatever the verdicts" (package §2.13) but not in CC-360 Ruling 7's eligible list; too long for print; kept in the result file of the review record. Judge to rule. |
| CC-375 W4 stale internal files (provenance_internal rows 276–278, 321; intext_trace l.61 claim text; outline l.64) | non-blocking, not paper text |
| Smoke build (CC-373 Phase B item 5; CC-375 W3 "recount at the smoke build") | no builds allowed on the laptop in this task |

## Departures from a byte copy (TG1), each for the judge

All are in `a_phase_b_report.json` "departures" with OLD and NEW. Summary:
1. Home S cross-references (TG1 allows): "Section 3.8" → Supplementary S11.1 (definitions, grid, guarantee sentence, prior-work sentence, H3 statistic), S11.3 (the references-alone identity: 9.1 assumptions paragraph; Table S11.4a note) or Section 6.7.3 (per-system intervals: sec7 l.181, S11.4d header, S11.1 "Does not mean"); "Section 6.8" → S11.5 / S11.6; "Section 6.7.3/6.7.4" (H2a/H2b/H2d) → S11.4; "Section 6.7.5" → 6.7.4; RQ4 "(Sections 3.8 and 6.7–6.8)" → "(Section 6.7 and Supplementary S11)".
2. KV2 / TG11 / CC-360 W2: one sentence after the guarantee in S11.1 ("On COCO-5000 the floor assumption failed at w0 (V2 FLOOR REFUTED, Supplementary S11.5), so this guarantee is not claimed there; with V1 PASS the certificate is described as "empirically valid on the sets tested" (COCO-5000, one model family, development).") and a parenthesis in S11.1 "Means".
3. TG9 on the Kill-gates paragraph (§2.13): KV0–KV3 → (a)–(e); "KV3: a second fault goes to the PI." → "(e) A second fault stops the analysis." (meaning changed from "goes to the PI" to "stops"; judge to confirm).
4. J-19 marker texts removed from the two §4 paragraphs; the quoted registered texts are printed in S11.4 (R11 §9 bullets) and S11.5 (VP §V.1 lead-ins and bullets, VP §V.5 Status paragraph), verbatim.
5. Count line: package §3.6 shell filled in the W6 form with names; "none was inconclusive" for the zero count.
6. Table changes: Table 6.7a (pkg 6.7g) gains Yes/No columns (W5 "32 Y of 143"); all-controls Yes/No DERIVED; S11.4a uses C / NC / ABSTAIN abbreviations with a key and puts the 36 cross-family rows in the same table; S11.4c prints "vacuous (no pair certified)" at w = 0 and 0.10 and "secondary; no verdict" plus grid coverage at 0.30 and 0.50 in place of the code labels "VALID AT 0.3/0.5" (W3); W4 cells "not defined (no certified pair)"; S11.4f per-family AUCs filled; S11.5a instance-only row filled with "no verdict" labels; S11.6a k = 1 "1 references" → "1 reference" (CC-360 W6); S11.6c cell letters in the §0.1 notation (W7).
7. System names: from Table S7.3 ("zero-shot, short (1)", "greedy, detailed (2)", "lower/higher temperature" for T0.5/T0.8, key in each caption); Part P names from the released file ids ("OPERA [Shikra]", "Less is More (r8) [LiM]"; J-36: each model named as a source of released outputs).
8. n-gram scan: in the §4 assumptions paragraph (9.1) "names a class that is not in the image" → "names a class absent from the image" (the first scan of sec11 failed on one 6-gram shared with the COCO Karpathy captions; wording only).
10. TG4 label insertions: "(single annotator)" added to the count line ("registered on the labels (single annotator)"), to every W2 sentence ("For H2b (single annotator), …"), the H1 secondary-corner sentence, the H3 "Beside it" sentence, the H2a remainder sentence, the H2d replicate line and the synonym count; the abstract says "these single-annotator labels"; the Part V null/transported/M-label sentences are one paragraph opened by the Part V label.
9. Sentence glue: lead-in "With H1a, H1b and H1c all PASS, " before the [reg] all-three fragment; "**Certificate (Supplementary S11):**" before the 8.1 sentence; capitalisation/full stops where a [code] string starts or ends a sentence; W2 capitalised as its own sentence after H2b PASS; "**Released evaluation logs.**" as the 9.2 lead-in; §2.5 gets one pointer sentence to S11.1; Contribution 6 "(H3)." → "(H3; Section 6.7)."; §2.4 relation sentence gets "**Relation to prior work.**" in S11.1.

## NEW TEXT (needs the judge's read)

Line numbers in the files after the run.

| Item | File : lines |
|---|---|
| "Outcome for the certificate." lead (gate statement before the registered sentences) | sec7 : 132 |
| Run fact (N2) | sec7 : 128 (last sentence but one) |
| Captions of Tables 6.7a, 6.7b, 6.7c (pkg caption), 6.7d, 6.7e, 6.7f; Table 6.7a note sentences | sec7 : 156 and 167 (6.7a), 173, 185, 200, 225, 238 |
| §2.5 pointer sentence | sec7 : 198 (end of paragraph) |
| Other-family arm sentence (J-27) | sec11 : 31 |
| 9.2 label-release clause (P-3 default) | sec11 : 51 (last sentence) |
| Table 1 row group and Development row wording | sec1 : 49–50 |
| Abstract (whole paragraph re-cut; additions: E13 clause verbatim, seven-count clause, "a proposed certificate was not validated") | abstract_A.md : 9 |
| S11 opening; S11.2 (registered sketch restated); S11.3 (VP §V.4/§V.4a identity in paper notation); SESOI lead-in; R11 §9 lead-in; KV2 sentence; matcher-check sentence; all S11 table captions; S11.7 protocol paragraph + Table S11.7a caption; S11.8 list (code, pins, run records, J-1 notation map) | supplementary_SPIC.md : 1174–1734; supplementary.md : 1367–1927 (S11.1 1178, S11.2 1214, S11.3 1218, S11.4 1222, S11.5 1425, S11.6 1490, S11.7 1696, S11.8 1728 in SPIC; +193 in supp) |
| Table S4.0 rows A31–A37, D-1–D-4, P-5 and the times paragraph | SPIC : 313–323, 328, 330; supp : 374–384, 389, 391 |

## Files: sha256 before (= HEAD blob) and after

| File | Before | After |
|---|---|---|
| paper/sec7_verbosity_sign.md | 15f0c20bfcf3b63980a88467d5ffaaa10d85c4ac34c6e3e299946b53e4a2c4a2 | 718fa68a586e7caab6026d9a9b6728fc116968f050ba8688c1d832f69a335f44 |
| paper/sec11_limitations_ethics.md | ef133a636e2fd5a81de3bc6b6f050100f7bda3b041dd54337ac7d73d775fdab4 | a1d01319b7fd4211b68355a0c60c38df35fe7cc0164a9001fe342fbf7eba6f16 |
| paper/sec5_exchangeability.md | d55ea4287b44ecfe3a13cda769be70ba78f2d69b06fc19e9486c842f03f9578d | a05270dd0ca4a71cd427fef36c7ce2188d1cbd81934fb58b98b69e82e4d76d8f |
| paper/sec2_related_work.md | d22d33b39852f647363703091981e0ecbc77d66644172a9661aae47d2a7ca4f2 | de85f341f07c90b09d90164abcaec474f0f78c80ea1353cf7f2c3455a9d5b080 |
| paper/sec1_introduction.md | f6596e0c92434b415cb6363ca4ba33c85c0fc3c5d8f69f17e26a1052d12bb4e4 | 042ff754edb3e419bd791ba63bd1a31c9adbcb4bad7938475e51f98715d5eb97 |
| paper/sec10_discussion.md | c5168c0ef712ebf569aec041f1dfa188d10dd52a1b53deb55302c65653c485c6 | f2eea5dc85db421acec1c678f3c1aa3975856f7e1a77507e00a7d0d6a53a7d40 |
| paper/cover_letter_A.md | abfedcbab6c120a26b50b798277eaccacdf5ee357baacc05e846e88b8826620a | 7c14bb274f6e50c47abdbaceeebacad22da86d52043ac731dbac6835b8737957 |
| paper/highlights_A.md | f02bb46700939c866d972ac2c437aa7c567cfc672cea561989ba562bc9f84f66 | 64c671615bd5106cba42cf168ff7ff85460bd9bd72b3c52a2d9903861c281aa5 |
| paper/abstract_A.md | 5d45fe18302f8b2161de800894d287b81e71f2346e533782c8bdb1cb27307edf | 6cf53ad8408b63e758883daa2c05a924a8870f36d4c63f106f8d02053e958d02 |
| paper/supplementary_SPIC.md | bf0d2127f413fcdd84edf6e0d127b1906a0d670da5d7f014dd6dbbd56d59dfed | 8260c34d7375f12cd352d60cd882c695b0dc6e11b1914a991f0a9a4ce8344983 |
| paper/supplementary.md | 1cd45dcdef2748c2524daafe404332ed88f051bf220339c9ca92546b2a46aed6 | 7f26b0d379e2144845dfdf6e814ecebce80f124441d127c773c5d4b60da96fd4 |
| paper/number_manifest.tsv | 1e9b92dc41a1eaa44540309094b601c2c784fe3d299abe7519cab37c1ecbf8d2 | 7e88baffb0a965d91de2b7e0f30efb6e6e0ac5394c0c06acade2e61054a77071 |
| paper/paperA.bib | 9958a0de392fa6670289565f649856664912cc5cbadd4d10b470db6d2febcf44 | 5a215e170422ce8fa49173c44775086228647ce32b19753b522892804f09bcdc |
| paper/citation_map_A_v2.tsv | 164f22e39e737a5e1f3940bf1d4f9fd3681146305102c9c2c4fd09444a166f4f | d4d987e80314136879565ee71ab0cc169d72efe78b7c8e824b47ed2aed3ee8b5 |
| paper/intext_trace_A.tsv | 3e1c337e085b7c6c8981c2d144303d25f489219db2ccd13774faa2c5c5ea4f0a | c3c84266ae99ceee9fc18b5c61ff2ad34386b0864ec1d1189940b009a952fbf3 |

Unchanged: `paper/declarations.md`, `paper/anon/declarations_anon.md` (J-13 strings still true; no second-annotator line). `git diff --stat`: 15 files, 3,794 insertions, 39 deletions.

## Word counts

Method of V2_PROGRESS.md "Word counts": comments stripped, `wc -w`-style split, tables included, sec1–sec11 plus declarations.md.
- Main text: HEAD 15,196 → after 18,483. The 8,500-word cap (PI-1105k, CC-375 W3) was already exceeded at HEAD; Phase B adds 3,287 (mostly Section 6.7 tables and the §4 paragraphs placed in 9.1 by the placement table). Not cut (conflict K1).
- Abstract (paragraph, comments stripped): HEAD 240 → 250 (TG10 ≤ 250). Highlights: 5, each ≤ 85 characters.

## Manifest rows added (number_manifest.tsv lines 1448–3942; 2,495 rows)

Each row: `<number as printed> (<places>)`, `A`, file, key, sha prefix, status. Values are read from the file at the key by the script and formatted in the same call (verified by construction; the shas of the files are asserted at the top of the script).

| Source | keyed | DERIVED |
|---|---|---|
| A_CERT_RESULT.json (7492a16c) | 455 | 25 |
| FREEZE.json (c51ea7dc) | 549 | 4 |
| A_CERT_V_RESULT.json (2675cdce) | 118 | 0 |
| A_CERT_P_RESULT.json (a05edf41) | 1,279 | 4 |
| Registered constants (CC-373 N3): R11 25, VP 19, H2D 2, PLAN 4 (each keyed to file, line and the literal, asserted present on that line; the VP §V.1 and R11 §9 quoted figures are keyed to their lines with the status "REGISTERED CONSTANT … quoted"; they were not recomputed from `r4_full5000_all9.json` / `xm3600_oiv7.json`, see K5) | 50 | – |
| LOG line times (11) | 11 | – |

## Closing checks (run by the script)

- CC-375 W1: in sec5 and both supplements, each Ruling 4 NEW occurs once and each OLD 0 times; FIX_A2 §7 greps (`independent-annotator`, `written by independent annotators`, `UIT-ViIC (all splits), VI | independent`) are 0.
- TG5: "No new human annotation" 0 times in paper/*.md and paper/anon/*.md; "No ethics approval" 0 times in both declarations files; no new "independent" writer claim.
- TG9 on the added visible text: no `{{`, KV-EV, KV1, OC1, A-N2, A-T3, "E1's rule", PI-/OPS- codes, "R11"/"VP" names or line numbers outside quotes. Remaining internal tokens occur only inside verbatim registered quotes or code strings (K4).
- S11 identical in both supplements; no "Section 3.8", "Section 6.8" or "Section 6.7.5" left in any sec*.md or in S11.

## n-gram scanner

`python3 -I .session_backup/2026-10-28/snapshots/C_pass3/checks/ngram_scan_cen.py <file>` from the run-repo root, one file at a time, on the after shas above. Each run printed the positive-control hits (ktvic 8:5 6:7; openviic 8:16 6:18; uitviic 8:2 6:4; coco_karpathy 8:7 6:9).

| File (after sha prefix) | Result |
|---|---|
| abstract_A.md (6cf53ad8; earlier 751bdd26 also PASS) | NGRAM SCAN PASS (rc 0) |
| highlights_A.md (64c67161) | PASS |
| cover_letter_A.md (7c14bb27) | PASS |
| sec1_introduction.md (042ff754; earlier 62801ae2 also PASS) | PASS |
| sec2_related_work.md (de85f341) | PASS |
| sec5_exchangeability.md (a05270dd) | PASS |
| sec7_verbosity_sign.md (718fa68a; earlier 4267df6d also PASS) | PASS |
| sec10_discussion.md (f2eea5dc; earlier 2202d3a8 also PASS) | PASS |
| sec11_limitations_ethics.md | first scan (b65aca67): FAIL, coco_karpathy 6-gram, line 25, 1 hit (the generic phrase in departure 8); after the rewording (a1d01319): PASS (rc 0) |
| paperA.bib (5a215e17; earlier ac7c5cc8 also PASS) | PASS |
| citation_map_A_v2.tsv (d4d987e8) | PASS |
| intext_trace_A.tsv (c3c84266) | PASS |
| number_manifest.tsv (7e88baff; earlier aba2b218 also PASS) | PASS |
| supplementary_SPIC.md (8260c34d; earlier 082aeaae also PASS) | PASS |
| supplementary.md (7f26b0d3; earlier 21a6a2ab also PASS) | PASS |

After the 23:33Z revision the eight changed files were scanned again on their final shas (all PASS); the other seven are byte-identical to the shas first scanned. Every final sha in the files table has a PASS.

## Conflicts between the rulings and the paper files (for the judge)

- **K1 Word cap.** Main text 18,483 against the 8,500 cap (15,196 at HEAD). The placement table puts §2.5, every main 6.7 table and five §4 paragraphs in the main text in Home S. Moving Tables 6.7a/6.7d and the §4 certificate paragraphs to S11 would cut most of the addition; not done (needs a ruling).
- **K2 Abstract.** CC-369 W2 says "wherever H2b PASS is named" add the coverage clause; the W6 count line in the abstract names H2b. Adding W2 (~30 words) breaks the 250 cap. Not added in the abstract (added in 6.7, Table 1, 8.5, S11.4, S4.0). The H2d FAIL is named without its estimate, interval and threshold in the abstract, in Table 1 and in the 8.5 count line (they are in 6.7 and S11.4 with the H2d label), as the paper does for the other nine FAILs there. The abstract also departs from the Home S shell (package §3.10; CC-369 Ruling 5): it names H3 inside the count clause instead of "it respects … the reference-only coverage bound (H3 RESPECTED)", and it drops "(Supplementary S11)" after "was not validated"; both are cuts forced by the 250-word cap. The abstract now carries "Section 6.7.2" inside the verbatim E13 clause. Cuts listed in the abstract's comment; no registered FAIL removed.
- **K3 Highlights.** Five highlights exist (TG10: 3–5); E13 names "highlight 4", which is the third bullet ("A positive label-gold slope needs unverifiable mentions excluded from precision"); the E13 clause cannot fit 85 characters. I replaced that bullet by the Home S highlight (77 characters). Judge to confirm or choose.
- **K4 Verbatim quotes vs TG9.** J-19 (R11 §9 bullets; VP §V.1 lead-ins and bullets; VP §V.5 Status paragraph), J-16 (H2D §4 bullets) and the H2d printed label (CC-369 Ruling 5: verbatim) contain internal names: "Q25", "`xm3600_oiv7.json`", "A2 plan", "`refs2_firstk`", "`/tmp`", "chưa kiểm", "K2", "CC-335", "The judge of CC-335", "§V.1", "(v1.1 §9)". Printed verbatim; judge to rule (verbatim vs TG9).
- **K5 J-19 manifest.** J-19 asks the aggregate figures to be keyed to `r4_full5000_all9.json` (332da8b6) and `xm3600_oiv7.json`; I keyed them to the registration lines (quoted) and did not recompute them from those files.
- **K6 TG4 on the freeze table.** Table 6.7d (per-system intervals) uses no label; its caption carries "development (no labels)" and says it belongs to the analysis registered on new labels, rather than claiming new labels.
- **K7 S11.2.** No registered text holds a derivation beyond the R11 l.124 sketch; S11.2 restates the sketch. CC-357 P-4 / W12 refer to "the one-page derivation (Supplementary S11.2)", which does not exist.
- **K8 W3 labels.** The stored secondary labels "VALID AT 0.3/0.5" are not printed; W3's "secondary; no verdict" is. Judge to confirm.
- **K9 C11.** CC-373 Phase B item 5 orders "the C11 sentence with the C8 count"; I deferred it (reasons in the Deferred table).
- **K10 Kill gates.** TG9 forces removal of KV0–KV3 from the §2.13 paragraph; "goes to the PI" was rendered "stops the analysis".
- **K11 Times.** The package calls OPS-1111al "the first-label time"; that line pins the labelling plan, and OPS-1111be (13:53Z) shows no main label file then. Table S4.0 prints it as "Labelling plan pinned".
- **K12 E3 source sha.** CC-357 W14a names the E3 addendum at 64fad518 (2a39f87); the file is now c0eee4fb (later commit 7568e46). Only the J-27 sentence uses the arm, so no E3 string was transferred.
- **K13 Part V per-unit listings** (deferred table) and the Table 2.1 row for arXiv 2611.01712 (J-10) are not printed.
- **K14 RQ4 in Home S.** The package gives RQ4 for both homes; under Home S it asks a question whose answer is "not validated" (supplement). Kept as ordered.

## What the judge must decide

K1–K14 above; every NEW TEXT item; departures 3, 6, 7 and 8; whether the §4 certificate paragraphs stay in 9.1 under Home S.
