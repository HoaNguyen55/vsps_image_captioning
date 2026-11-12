# Paper A certification: PHASE A paper-text transfer record (for a one-judge diff read)

Written 2026-11-12T19:20:00Z, revised 2026-11-12T20:15:02Z (`date -u`; the anon Ethics row moved from partly applied to SKIPPED, the CC-369 disclosure sentence added as deferred, the custody lines completed) by the transfer operator. Label of the transferred text: the package's own labels; no figure from FREEZE or any result file is in it.

**What this is.** An UNCOMMITTED working-tree change to `/mnt/d/vsps_papers/vsps-paperA-spic` (branch `main`, HEAD `e8aa602516a83a12a2ca6bf883748d53a81e0dfe`, tree clean before the run). Nothing was staged, committed or pushed in either repo. No LOG or CC file was written. No build was run.

- Built by `a_phase_a_transfer.py` (this folder), run as `python3 -I a_phase_a_transfer.py`. It starts from `git show HEAD:` of every target file, so a re-run is idempotent (checked: re-runs give the same eight `after` shas). An earlier run had also changed the first Ethics sentence of `paper/anon/declarations_anon.md`. The current script keeps that file in its loop with zero edits, so it was rewritten from its HEAD blob; it no longer appears in `git status`.
- The script asserts: package sha256; paper HEAD; each package line used starts with its expected lead-in; every OLD occurs exactly once in its file; every inserted paragraph except the one J-13 paragraph is a byte substring of the package; BUILD.json sha on disk and in run-repo HEAD; each manifest value equals its BUILD.json key.

## Sources

| Source | sha256 | Note |
|---|---|---|
| Package `manuscript/prereg/2026-11-11_a_cert/paper_text/A_CERT_PAPER_TEXT_v1.md` | `d2548abc379de4d9c6b0132865cdfe6fb39639f777c4503a15cb5e8aa7ed0b73` | = CC-357 TARGET; committed `867fb07` (TG1) |
| CC-357 `.session_backup/2026-10-13/decisions/CC-357.txt` | `9c6d588d4467cb9ef8639f703226150c705598ef92e7f2d0d933709556a6e0d1` | Ruling 5 Phase A list, TG1–TG12, J-rulings |
| CC-369 `.session_backup/2026-10-13/decisions/CC-369.txt` | `d92c89d96b78ba0f265ef9230e7c325e46791e326f7c7cb0f46a0473cb5e28da` | read: l.147–192 (Ruling 5: claim wording, with its filled Phase B sentences, and the Phase A/Phase B paragraph l.173–191), l.286–299 (the disclosure sentence), l.313–374 (Ruling 10, tier, REQUIRED FIXES W1–W11, the carried line). Located by two greps (section heads and `Paper text\|Phase A\|Phase B\|W[0-9]\|disclosure\|commit`; then case-insensitive `disclos\|the paper (states\|says\|prints)`). None of its result figures or verdict words is used in the paper text or in this record |
| `manuscript/prereg/2026-11-11_xm600_gold_completion/BUILD.json` | `d424fdcaa6a99b84c329a9a65edacff5f3654284fecfe5b716debfa6b5295d87` | committed `971962f`; pinned in LOG OPS-1111al-xm600-label-start (l.2165) and OPS-1112h FREEZE pin line (l.2220); disk = HEAD blob |

**Trigger (CC-357 Ruling 5 preconditions, TG12).** Package committed at TARGET (`867fb07`). Part-1 session-end line: LOG l.2357, `OPS-1112cf-xm600-session-end-part1`, `2026-11-12T18:15:46Z`. This transfer was made after it; the Phase A commit must also be after it.

**Custody.** Not opened: `data/results/a_cert/score/A_CERT_RESULT.json`, `data/results/a_cert/freeze/FREEZE.json`, `data/results/a_cert_e3/`, `data/results/a_e3/`, `data/results/a_cert_v/`, `data/results/a_cert_p/`, `~/vsps_labels/`, any `key.json`, `assignment.json`, `~/.vsps_sealed`. LOG (`.session_backup/2026-10-13/decisions/LOG.md`) searches, every printed line cut to 300 characters or fewer:
- `d424fdca` (BUILD pin) and `OPS-1112cf` (trigger);
- `grep -o 'BUILD(\.json)?…<hex>'` (BUILD pin strings only, no `cut`; the match is at most about 110 characters);
- `ethic|P-2.*CC-357|CC-357.*P-2|CC-357 P-|PI-1112|PI-1113` (case-insensitive): no PI line answers CC-357 P-2;
- `second annotator|second-annotator|R2 session|xm600-r2|overlap_r2` and, later, `r2|second annot` (case-insensitive) on the last lines: the second-annotator lines are build and commit lines only (OPS-1112cd, PIN-1112-a-xm600-r2, OPS-1112ce); no labelling-start line; the later `r2` hits are an unrelated E3 round-2 host;
- `tail -4` of the LOG (cut to 260 characters).

Disclosure: the CC-369 header grep, made to locate the permitted parts, printed some lines of its other rulings to the operator's screen. Nothing from them is used in the paper text or in this record.

**Placeholders.** The Phase A visible text holds no `{{…}}` placeholder. The two LOG placeholders of package §2.12 (`{{LOG.md::OPS-1112h.utc}}`, `{{LOG.md::OPS-1112h.sha256}}`; the line exists: LOG l.2220, `OPS-1112h-a-cert-FREEZE-pin`, `2026-11-11T18:29:02Z`) and the score-run placeholder sit only in the package's `<!-- src -->` comments. Package comments are not transferred (as in the Paper C transfer, CC-365), so none of them is placed. This is how "§2.12 without run facts" was read.

## Rows

| Row (CC-357) | File | Status | How |
|---|---|---|---|
| §2.12 Freeze, One pass, Multiplicity → 6.7 first paragraphs | `paper/sec7_verbosity_sign.md` | applied | byte copies of package l.304, 307, 310 |
| §2.6 → 6.7.1 | `paper/sec7_verbosity_sign.md` | applied | byte copies of l.197, 200, 203, 206, 212, 215, 218; l.209 with the J-13 change below |
| §2.7 → 6.7.1 | `paper/sec7_verbosity_sign.md` | applied | byte copies of l.223, 226 |
| §2.8 H1 definitions and table, without "Facts fixed" → 6.7.2 | `paper/sec7_verbosity_sign.md` | applied | byte copies of l.231, 233–237, 239; l.242 ("Facts fixed before unsealing") left out |
| §2.11 H3 → 6.7.5 | `paper/sec7_verbosity_sign.md` | applied | byte copies of l.285, 287, 289–294, 296, 299 |
| §4 annotator paragraph (CC-343; N6 already in TARGET) → 9.1 | `paper/sec11_limitations_ethics.md` | applied | byte copy of l.648, inserted after "Construct validity: reference-only bound." |
| §4 "what the labels are" → 9.1 | `paper/sec11_limitations_ethics.md` | applied | byte copy of l.651 |
| §4 statistical conclusion validity → 9.1 | `paper/sec11_limitations_ethics.md` | applied | byte copy of l.660 |
| E1 (Section 3.6 rule (iii)) | `paper/sec3_measurement_setup.md` | applied | OLD = `(iii) model-produced signals … and no new human annotation was collected` (once) → package E1 NEW verbatim |
| E2 (Table 2.1, "This paper", "Needs new labels?") | `paper/sec2_related_work.md` | applied | OLD = `\| Nested reference golds and instance or verified labels \| No \| Image-bootstrap intervals` (once; the bare `\| No \|` is not unique) → cell = package E2 NEW verbatim |
| E10 (Ethics) | `paper/declarations.md` | applied, with J-13 and the P-2 default | OLD = the package's two-sentence quote (once) → E10 NEW with the J-13 change; "No ethics approval was required." dropped (no PI line answers CC-357 P-2; default "removed until you confirm") |
| E10 (Ethics) | `paper/anon/declarations_anon.md` | SKIPPED (mismatch) | E10's quoted OLD does not occur (asserted: 0 times): the file's second sentence is "No ethics approval was required: no new data from human participants were collected.", not "No ethics approval was required.". File unchanged (= HEAD blob). See C2 |
| E12, E1 part (S10 copies) | `paper/supplementary.md`, `paper/supplementary_SPIC.md` | applied by suffix (see C10) | the S10 copies read "(iii) Model-produced signals are never treated as gold or as human evidence, and no new …". OLD = the shared suffix `, and no new human annotation was collected` (once per file) → the E1 NEW suffix `; one set of new human labels … (Section 6.7)`. The differing prefix ("Model-produced … or as human evidence") is unchanged |
| J-11 manifest rows | `paper/number_manifest.tsv` | applied | 16 rows appended (lines 1432–1447), see below |
| S11.7 (protocol) | – | SKIPPED | the package has no paste-ready S11.7 text (only its description in §1.2 and pointers). Composing it would go beyond the registered strings |
| S11.8 (code and pins) | – | SKIPPED | as S11.7. The package's only S11.8 sentence is the §2.13 "Implementation note" (Part V, Phase B), and the J-1 one-line notation map has no package text |

## Departures from a byte match (TG1), each for the judge

1. **J-13, §2.6 "Who labelled." (sec7 l.142).** No second-annotator labelling line exists in the LOG (the last such lines are OPS-1112cd/ce/PIN-1112-a-xm600-r2, 17:30–17:32Z: build and commit only; f267815 "no second-annotator session has started").
   - before: "A second annotator, a colleague, answers every question of 150 of the images (25% of the images with a target, drawn with a fixed seed) with the same page and instructions, without seeing the first answers."
   - after: "A second annotator, a colleague, will answer every question of 150 of the images (25% of the images with a target, drawn with a fixed seed) with the same page and instructions, without seeing the first answers, and has not yet labelled."
2. **J-13, E10** (`declarations.md`).
   - package: "given by one author and, on 150 of the images, by a second annotator (Section 6.7.1)"
   - transferred: "given by one author; a second annotator, who will answer the same questions on 150 of the images, has not yet labelled (Section 6.7.1)"
   - Both J-13 changes must be re-checked at commit time: if the second annotator starts before the Phase A commit, the tense is stale.
3. **E10 ethics sentence** dropped in `declarations.md` (CC-357 P-2 default). The anon file is not edited (row above).
4. **Headings** (no registered title exists for 6.7; the others are the package subsection titles without their location notes):
   - `## 6.7 A human completion of the XM3600-600 object gold (registered on new labels of previously analysed captions; development role)` (words from the Home-independent RQ4/contribution label of CC-357 W10/W11 and the package's "A human completion of the XM3600-600 object gold");
   - `### 6.7.1 The human-completed gold of XM3600-600` (§2.6);
   - `### 6.7.2 Hypotheses H1 (completed label-gold slope), as registered` (§2.8);
   - `### 6.7.5 Hypothesis H3 (the coverage bound of Section 5.4 against the completed gold), as registered` (§2.11).
   - §2.7 has no lead-in in the package; its two paragraphs follow §2.6 inside 6.7.1 unchanged.
5. **Package `<!-- src -->` comments and "Writer note" text** are not transferred (precedent: the Paper C transfer added no package comments).

## Conflicts between CC-357's Phase A list and the paper files (flagged, not edited)

- **C1. S11.7 / S11.8** are listed as Phase A, but the package holds no text for them. Skipped (rows above).
- **C2. Anon Ethics paragraph** (row above). E10 is not applied there, because its quote does not occur. The file still says "No new human annotation was collected …" and "No ethics approval was required: no new data from human participants were collected.", so TG5 is not met for this file until the judge gives an OLD/NEW for it. A partial edit was tried and withdrawn: replacing only the first sentence would have left the ethics clause that the P-2 default removes, right after a sentence stating that new labels were collected.
- **C3. Table 2.1, RePOPE row, column "What remains for this paper"** ends "…; no new labels". It describes this paper and is not covered by E1–E13. Left unchanged.
- **C4. Home-dependent cross-references kept byte-exact** (choosing a home would encode the entry-gate outcome; TG1 allows the swap at Phase B):
  - 6.7.5 "**Statistic.** With the two references of Section 3.8, …" (sec7 l.170);
  - 6.7.5 "**H3 secondary rows** … the low ends of the per-system intervals (Section 3.8) …" (sec7 l.181).
- **C5. Forward references to Phase B material** (expected in a two-phase transfer):
  - Section 3.8 and $V_m$ (defined in package §2.1) do not exist in the paper yet;
  - "the certificate" (6.7.1 "Why labels were collected.");
  - H2a, H2b, H2d (6.7 "Multiplicity.", 6.7.1 "Image sets and bootstrap.", 9.1 statistical-conclusion paragraph);
  - 6.7.3 and 6.7.4 are absent, so the numbering jumps from 6.7.2 to 6.7.5.
- **C6. "One pass."** ends "A second fault would have stopped the analysis." It is transferred verbatim. Whether it counts as a run fact is for the judge.
- **C7. TG4 caption string.** The H1 and H3 rule tables of 6.7.2/6.7.5 have no caption in the package, so "new labels on previously analysed captions" is not in a caption. The 6.7 heading carries it. No caption was composed.
- **C8. CC-369 W1** says the paper prints the post-relay label-line count beside the disclosure sentence. That count comes from a later code read and is not in the package. Not in Phase A.
- **C9. FIX_A2 (J-6)** is not applied; 9.1 still holds the E7 sentence unchanged (E7/N1 is Phase B).
- **C10. E12 by suffix.** E1's quote does not occur in the S10 copies, so the E1 part of E12 was applied by its suffix (rows above). The span replaced is exactly the span that E1's NEW replaces in Section 3.6. The judge may void it.
- **C11. CC-369 disclosure sentence** (l.287–298, "The annotator was told the registered verdicts of the part-1 analysis on <date of the W1 relay line> …"). CC-369 places it beside the part-2 rows, the repeat-agreement figure and every top-up row, and it has a variant that depends on a PI answer. It is deferred; Phase A has none of those rows. The W1 count (C8) goes beside it.

## Manifest rows (J-11), `paper/number_manifest.tsv` lines 1432–1447

All keyed to `manuscript/prereg/2026-11-11_xm600_gold_completion/BUILD.json`, sha prefix `d424fdcaa6a9`. The value of each was asserted against BUILD.json by the script.

| Line | Number in text | Key | Status |
|---|---|---|---|
| 1432 | 600 | `counts.images` | keyed |
| 1433 | twelve | `len(counts.systems)` | keyed |
| 1434 | 4,910 | `counts.named_pairs` | keyed |
| 1435 | 1,790 | `counts.part1_targets_mapped_unknown` | keyed |
| 1436 | 143 | `counts.ctrl_absent_named` | keyed |
| 1437 | 200 | `counts.ctrl_present_named` | keyed |
| 1438 | 100 | `counts.foil_absent_unnamed` | keyed |
| 1439 | 443 | 143 + 200 + 100 | DERIVED |
| 1440 | 2,233 | 1,790 + 443 | DERIVED |
| 1441 | 2,100 | `counts.part2_targets_unmapped` | keyed |
| 1442 | 150 (repeats) | `counts.repeats` | keyed |
| 1443 | 4,483 | `counts.questions` (= 1,790 + 443 + 2,100 + 150, asserted) | keyed |
| 1444 | 1,288 | `counts.screens` | keyed |
| 1445 | 15 (practice) | `counts.practice_screens` (one image per screen) | keyed |
| 1446 | 150 (overlap images) | `counts.overlap_images` | keyed |
| 1447 | 25% | 100 × 150 / `counts.images_with_targets` (598) = 25.08 | DERIVED |

Literal numbers in the Phase A text with NO new manifest row (registered design constants from R11/H2D/PLAN, not BUILD.json; the reader decides whether rows are owed):
- 537 (clean subset, an existing paper number);
- [+5.83, +20.13] and [+1.97, +14.78] (existing manifest rows 657–660);
- bootstrap sizes 500 of 2,000 × 600, 1,000, 2,000 and seed `20261111`;
- 99.17%, 0.60, 50, 95%;
- 66, 30, 15, 9, 6, seven, 0.36th percentile.

## Files: sha256 before (HEAD blob = disk before the run) and after

| File | Before | After |
|---|---|---|
| `paper/sec3_measurement_setup.md` | `bab8b5c66e39b96b8214a2440299621e3a530946dbb250f48c78675b499e9815` | `07d1f5fee0c1652167b0341a0d4842773d26e6347ca4002795e3ebb55bced79d` |
| `paper/sec2_related_work.md` | `2272d9c60811fee827a14de052e29aeaf57c546affc2cd8e101387d2dd686af0` | `548f9c4960c6074bc873abd0552a43e48ec142aed121e3918fdd7b86a02e1b1d` |
| `paper/declarations.md` | `8529413e25608b2de45261e5a185dc0dcda7e86f956a82b08506ec3a59ea2631` | `a96c5d31ada50ccd7d5b9528e47dcbadcd8cc8066a9a83c5bb3b6bc8fbbad9c5` |
| `paper/supplementary.md` | `1c8a68cd268bb99cbcfaebc26b7b9eac145097d9b893b7cbe31c71d14db09c2a` | `1cd45dcdef2748c2524daafe404332ed88f051bf220339c9ca92546b2a46aed6` |
| `paper/supplementary_SPIC.md` | `9be31e5895e0715c4f6da70e0768d6b6e417a0f57dfc9eeaad81007ccae75929` | `bf0d2127f413fcdd84edf6e0d127b1906a0d670da5d7f014dd6dbbd56d59dfed` |
| `paper/sec7_verbosity_sign.md` | `f5be769c615ced3c07a93766f72a5c16b29ebb39cfd549a5cab087ebf711ec0e` | `15f0c20bfcf3b63980a88467d5ffaaa10d85c4ac34c6e3e299946b53e4a2c4a2` |
| `paper/sec11_limitations_ethics.md` | `a4f26a094b593e9b4439b089daf5f99ebefc48a6cdbf05361cc7e0daeaabde10` | `ef133a636e2fd5a81de3bc6b6f050100f7bda3b041dd54337ac7d73d775fdab4` |
| `paper/number_manifest.tsv` | `de317ad3a5d7176a46ea5a840403da4a58d4ec67a6b201b0a1a6cc3f3ad78ef2` | `1e9b92dc41a1eaa44540309094b601c2c784fe3d299abe7519cab37c1ecbf8d2` |

`paper/anon/declarations_anon.md` is unchanged: `34ac759724dbcdb1f8d10282b50cc6c7ed66aa6513dd18fd0522b61eecce24f6` (= HEAD blob).

`A_PHASE_A.diff` = `git -C /mnt/d/vsps_papers/vsps-paperA-spic diff` after the run (8 files, 86 insertions, 5 deletions; sha256 in SHA256SUMS_PHASE_A).

## Block map (package line → paper file:line, after)

| Package | Paper |
|---|---|
| headings 6.7 / 6.7.1 / 6.7.2 / 6.7.5 | sec7:124 / 132 / 154 / 166 |
| l.304, 307, 310 (§2.12) | sec7:126, 128, 130 |
| l.197, 200, 203, 206 (§2.6) | sec7:134, 136, 138, 140 |
| l.209 (§2.6, J-13) | sec7:142 |
| l.212, 215, 218 (§2.6) | sec7:144, 146, 148 |
| l.223, 226 (§2.7) | sec7:150, 152 |
| l.231, 233–237, 239 (§2.8) | sec7:156, 158–162, 164 |
| l.285, 287, 289–294, 296, 299 (§2.11) | sec7:168, 170, 172–177, 179, 181 |
| l.648, 651, 660 (§4) | sec11:17, 19, 21 |
| E1 | sec3:54 |
| E2 | sec2:34 |
| E10 | declarations:27 (anon: skipped) |
| E12 (E1 part) | supplementary:1234; supplementary_SPIC:1041 |

## Checks run

- TG5: "no new human annotation" (case-insensitive) is gone from sec*, `declarations.md`, both supplements, abstract, cover letter, title page and highlights. It remains in `anon/declarations_anon.md` (C2). "independent writers": no new occurrence (the existing 9.1 E7 sentence is Phase B).
- Visible-text search (HTML comments stripped) of sec*, abstract, highlights, cover letter, title page and both declarations files for `new labels?|new annotation|new human`. Apart from the transferred text, the hits are the Table 2.1 header and caption, the RePOPE cell (C3) and the anon Ethics sentence (C2).
- TG8/TG9 on the added lines (manifest excluded): no AI text, no `{{`, no J-, R11, VP, KV-, OC1, A-N2, A-T3, "E1's rule", line numbers, CC-/PI-/OPS- codes. The only hits are pre-existing HTML comments on the two changed rule-(iii) lines (sec3:54, supplementary:1234).
- No caption text, host, IP or port in the added text.

## n-gram scanner

`python3 -I .session_backup/2026-10-28/snapshots/C_pass3/checks/ngram_scan_cen.py <file>`, run from the run-repo root, one file at a time:

| File (after sha above) | Result |
|---|---|
| `paper/sec3_measurement_setup.md` | NGRAM SCAN PASS (rc 0) |
| `paper/sec2_related_work.md` | NGRAM SCAN PASS (rc 0) |
| `paper/declarations.md` | NGRAM SCAN PASS (rc 0) |
| `paper/anon/declarations_anon.md` | not changed now (restored to HEAD); the PASS above was on the withdrawn partial version |
| `paper/sec11_limitations_ethics.md` | NGRAM SCAN PASS (rc 0) |
| `paper/sec7_verbosity_sign.md` | NGRAM SCAN PASS (rc 0) |
| `paper/number_manifest.tsv` | NGRAM SCAN PASS (rc 0) |
| `paper/supplementary_SPIC.md` | NGRAM SCAN PASS (rc 0) |
| `paper/supplementary.md` | NGRAM SCAN PASS (rc 0) |

Each run reported positive-control hits (8-gram 7, 6-gram 9) and 0 hit lines for the file. The scan ran before the anon file was restored. The script re-run gave the same `after` sha for the other eight files, so their PASS applies to the files as they are now.

## Left for Phase B (CC-357 Ruling 5), with the reason

- §2.1–§2.5, §2.9, §2.10, §2.13, §2.14 (the method, H2a/H2b, H2d, Part V, Part P): their home depends on the entry gate, which needs a CC line recording the gate under J-2.
- §2.8 "Facts fixed before unsealing": needs FREEZE values.
- §3 (all result tables and sentences, the freeze figures, the kappa and count lines, Table 6.7a–g, S11.5/S11.6 shells): need FREEZE or result values.
- §4 paragraphs "Internal validity: data the paper had already analysed" and "Development and post hoc rows" (J-19 insertions), "Construct validity: the assumptions of the reference-only certificate", "Prior work", the other-family arm (J-27; E3 result read), the wording duties, and the Section 9.2 data paragraph (J-31 release decision): listed in Phase B by Ruling 5.
- E3 (home-dependent), E4–E9 and E13 (need results), E11 and the E12 count part (need the count), E7/N1 (J-4).
- Abstract, RQ4, contributions, highlights; Table 1 and S4.0 rows (J-28); the Section 2 prior-work sentence and any Table 2.1 row for arXiv 2611.01712 (J-10).
- The Section 5.4 and S1.M.6 H3 sentences: need the H3 result.
- S11.1–S11.6 and, if the judge so rules, S11.7/S11.8 (C1).
- FIX_A2 (J-6): its own one-judge read must close first.
- The kappa sentences (J-14) and the post-relay label-line count (C8): wait for later code reads.
- The CC-369 disclosure sentence (C11): it goes beside the part-2, repeat and top-up rows.
- E10 for `anon/declarations_anon.md` (C2): needs an OLD/NEW that matches the file.
