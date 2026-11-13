# C-ATTR-DEV block 3: transfer record (Paper C, ACM TALLIP)

Written 2026-11-13T03:49:24Z (`date -u`) by the transfer operator, for the one-judge diff read of CC-380 ruling 15 (4). Label: `DEVELOPMENT / C-ATTR-DEV, NON-CONFIRMATORY`. Development sets OV-dev-B and XM-dev500 only; no test set was touched, staged or named. Nothing was staged, committed, stashed, checked out or pushed in either repo; no LOG or CC file was written.

## 1. Bases

| item | value |
|---|---|
| run repo HEAD | `a4db071e6a270eefa77aefb2efcb2d055f67fc52` |
| paper repo HEAD | `44bbdd9979ea03d0d9c30c435a0246984022c561` (= package and CC-380; G2 met without moved lines) |
| package `C_ATTR_B3_PAPER_TEXT_v1.md` | `e3820d3bf93f4246913c6eb651373965303d4afb31fc51fc3db48687ab2904f6` = CC-380 ruling 14 TARGET (asserted by the script) |
| ruling CC-380 | `60b7e074445a7ac0c6dfbef2f37a5bbd90a82972c0fe6043450d245aea9f7634` (asserted) |
| W1 (G0) | closed: LOG `OPS-1113bb-c-b3-w1-end` (2026-11-13T02:40:55Z): self-test ok; 8 PASS lines, `ALL PASS (8 rows)`, each max\|diff\| 0.000e+00 against B3_SUMMARY.json `61bf697b…`; inputs k5.jsonl `87c2ef2c…`, b3_ov_dev_b.jsonl `7602d4e2…`, b3_xm_dev500.jsonl `0285083c…`; numpy 2.5.4; Python 3.12.3; inputs_digest `01588f1d…` = OPS-1113ao. Read here from `w1/selftest.out`, `w1/recompute.out`, `w1/inputs_digest.txt`, `w1/python_version.txt` (all equal the LOG line). |
| script | `transfer/c_attr_b3_transfer.py` `2817b88a6ebba907ca70e3713439d34704f74d75c7705ff55ce007a980e2df93`, run as `python3 -I` from the run-repo root; run twice, same after-shas (idempotent: every paper file starts from `git show HEAD:`) |

Untracked file in the paper repo: `docs/CC309_PARAGRAPH_DRAFT.md` existed before the transfer, was not opened or changed, and is not part of this transfer. Paper-repo `git status --porcelain` after the transfer: the 7 ` M` files below plus that one `??`; nothing staged (`git diff --cached` empty); `git diff --summary` empty (no mode change).

## 2. Rows applied

Each OLD was asserted to occur exactly once in the working text at its point of the sequence, and each filled NEW exactly once afterwards (script, plain `str.replace`, package order).

| row | file (`paper_v1_analysis/`) | applied |
|---|---|---|
| E1 | 03_method.md | yes |
| E2 | 05_preregistration_and_analysis.md | yes |
| E3 | 05_preregistration_and_analysis.md | yes |
| E4 | 05_preregistration_and_analysis.md | yes |
| E5 | 05_preregistration_and_analysis.md | yes |
| E6 | 06_results.md | yes |
| E7 | 06_results.md | yes |
| E8 | 06_results.md | yes |
| E9 | 07_disclosures.md | yes |
| E10 | 07_disclosures.md | yes |
| E11 | 07_disclosures.md | yes |
| E12 | 09_limitations.md | yes |
| E13 | 11_supplement_registered_rows.md | yes |
| E14 | 11_supplement_registered_rows.md | yes |
| E15 | 11_supplement_registered_rows.md | yes |
| E16 | 05_preregistration_and_analysis.md | yes |
| E17 | 05_preregistration_and_analysis.md | yes |
| E18 | 05_preregistration_and_analysis.md | yes |
| E19 | 05_preregistration_and_analysis.md | yes |
| M (127 rows) | number_manifest_C.tsv | yes (appended) |

## 3. Changed paper files (sha256)

| file | before (HEAD blob) | after (working tree) |
|---|---|---|
| 03_method.md | `50b0529c8c4341d3438e0438bcbf301d94067def6c9df2f08c2c52decac31615` | `7e23b048208b11508a937970194d4600f19c0f93532d67f024e63695ce41e2f2` |
| 05_preregistration_and_analysis.md | `489c4b79dd70d85ec449ad5dcbf3f8f8db55381c2035eed5503bc35dc6a813be` | `218b7d3ec603d80d037d6268452c7135bc822da4783452b3c806e522c6f4f440` |
| 06_results.md | `61be0e29a9bb5984c2404c023daefb99fe0ff1d6cc4dbc773d7a0b4efcf58ecc` | `943d0e19806ec5b0ee7cfc869236f7098f5355b81c4aa995a1a39cc276fc47d8` |
| 07_disclosures.md | `8e58dc6d739cb67ddd194d5d774c516c1a8be042701e5f8405a7f0e30b8571d2` | `9654358c8a92e917da407d74a4d679bd1b8b97f83bb3af3bc17050351cd1577d` |
| 09_limitations.md | `349703a1600a8c8e5bb70cfc96f1c360bf4ec8191dbed43166677a32c6805160` | `76fb358f22ac5ad64b87afdd7d49765fe8f91b97182e158fa572ea86415de4e3` |
| 11_supplement_registered_rows.md | `1223064fb563ba612fb04648984a8f21ba2b063615899796a4196d8c7db70e08` | `c4be508db3eed048990132a5eb17721730f6a94ebbc77a79168d65b98fb74b63` |
| number_manifest_C.tsv | `3eeb2dab9fd0e5ee369ec7f5b6dd4f0123240baf41fb4e02a4bac8b748e87d68` | `83a9ebc3930c3472576759cb68346ee52812974f4105609c5759bb1a98422835` |

Diff: `transfer/C_B3_TRANSFER.diff` (= `git -C /mnt/d/vsps_papers/vsps-paperC-tallip diff`, 332 lines, 7 files, 203 insertions, 11 deletions), sha256 `bdbcc3c9abf8a66db23ddf924cfca2d811e7cf72e6cc7fd2bc6bb52e48b184ff`.

Not changed (`git diff --quiet HEAD`): `00_abstract.md`, `01_introduction.md` (with its contributions list), `10_conclusion.md`, `paperC.bib`, `tex/`.

## 4. Placeholders and manifest

- Fill map (package §5.1): 128 entries parsed from the package = 123 tokens + 5 non-token entries (the four "(evidence for …)" rows and "ten (05 E5, S27)").
- Filled in E1–E19: **154 occurrences of 116 distinct tokens** (after expanding `[[Rk]]`, `[[BOV]]`, `[[BXM]]` to `{{Rk.d}} [{{Rk.lo}}, {{Rk.hi}}]` and `[[R3|90]]` to the same plus ` (90% interval [{{R3.lo90}}, {{R3.hi90}}])`, the house format of the 1b transfer `iv()`); every token resolved; no `{{`, `}}`, `[[` or `]]` left.
- Map tokens not used by E1–E19 (7): `R1.m`, `R3.m`, `R5.m`, `R6.m`, `R7.m`, `R8.m` (the E-rows print `m` only for R2 and R4), and `VER1B::…aya_vision_8b~tau_sel.label` (shell C1 only).
- Manifest: **127 rows appended** in the house columns (`number | file::key | raw_value | sha256_prefix | status | used_in`; header equal to the house header at HEAD). Status clause "W1 recompute pending" replaced by "W1 recompute PASS" in 58 rows (57 B3_SUMMARY rows + the K5 verdict row); 0 "pending" left.
- Verification of every manifest row, in the script, before any write (fail-closed): the source file's sha256 starts with the row's 12-hex prefix; the value re-read at its key equals `raw_value` exactly (`repr`); the display recomputed by the house rules (signed two-decimal point, unsigned two-decimal bounds, U+2212, never "−0.00", p̃ floor forms or three significant digits, thousands commas, sha 8 hex + "…") equals the `number` column. JSON rows by key path; `gpu_seconds*.tsv` by line and non-start sums; `job.log` by status lines only; `mutants.log` last two lines (`107/107 killed; survived: none`, `rc 0`); registered literals by substring in the registered text (v1.1 §6.5 "hard cap 5 GPU-h", addendum "min(12, 1.5 P3)", §7.13 "about 0.49", "about 1.03", "NEGLIGIBLE needs |θ̂| below about 0.3", run doc "first 50 OV-dev-B items", v1.1 "K = 4", "N = 3 shot", erratum model.safetensors sha `9e292657…`). Result: **127/127 rows pass**. The map's display column also equals the manifest's `number` column row by row (127/127, the extra "ten (05 E5, S27)" entry dropped), so every filled display is tied to a verified row.
- G1 in the script: `data/results/c_attr_1113_b3score/SHA256SUMS` = `d2500b48…`, all 28 lines re-hashed equal; 1b beside files VERDICT `a69a0ec2b758`, SUMMARY `1d78cd205ff8` by their manifest prefixes.

## 5. Conditional shells C1 and C2: not applied

`grep -c 'c-b2-cutoff' .session_backup/2026-10-13/decisions/LOG.md` = 0: no cut-off line exists, and C1 needs one stamped at or after 2026-11-14T11:00:00Z. C2 needs C1 plus a K7 line stamped at or after 2026-11-16T05:00:00Z; today is 2026-11-13. Nothing of C1 or C2 entered: the changed files contain 0 × "6.10.9", "What did not run", "(S-BB; Section", "ended every step", "Block 4 was not run". Each shell needs its own diff read or a ruled addendum (CC-380 ruling 12).

## 6. N-gram scan (`python3 -I .session_backup/2026-10-28/snapshots/C_pass3/checks/ngram_scan_cen.py <file>`, scanner sha `92607635…`, one file at a time, run-repo root)

| file | result |
|---|---|
| 03_method.md | NGRAM SCAN PASS |
| 05_preregistration_and_analysis.md | NGRAM SCAN PASS |
| 06_results.md | NGRAM SCAN PASS |
| 07_disclosures.md | NGRAM SCAN PASS |
| 09_limitations.md | NGRAM SCAN PASS |
| 11_supplement_registered_rows.md | NGRAM SCAN PASS |
| number_manifest_C.tsv | NGRAM SCAN PASS |

All hits 0 (uitviic 6-gram; coco_karpathy 8- and 6-gram); the scanner's own positive control printed hits as usual. Evidence is the scanner's "NGRAM SCAN PASS" line for every file; the exit code was captured for the last three files only (0 each), the first four were piped through `tail`.

## 7. Text guards (76 added paper-text lines of the diff; hits on modified lines classified NEW text vs. text already at HEAD)

| guard | count on added lines | reading |
|---|---|---|
| "test" (word part) | 9: 4 at HEAD (06 l.254 "The test used 9.59 GPU-hours", "pre-test"; 09 l.10 "not a test result"), 5 new: 06 l.244 "any test set"; 07 l.26 "no other effect was tested"; 07 l.61 "self-tests", "self-test", "self-tests", "was not tested" | no new text calls the attribution analysis a test; all new hits are ruled wording (CC-380 W1c, W5; V4; ruling 5 limits) |
| CC / OPS / PI ids, "C-T1", "kit B", J-B3 / W-fix codes | 0 | – |
| K-codes | "K1" 5: 4 at HEAD; 1 new, 06 l.227 (Table 18 caption quotes the 1b label "batch size 1; registered in v1.2 after K1 fired, …", CC-380 W3b) | "kill gate K1" is a paper term (6.10.2) |
| host name / IP / port / machine label (H1, ATTR_H1, M1–M5, m5, ckey, ssh) | 0 | the word "host" occurs 6× in new text, all ruled generic wording (V1, V2, V3, V5) |
| AI mention (AI, Claude, GPT, Gemini, Codex, agent, LLM) | 0 | – |
| "no overlap" | 0 | "overlap" 1× new: 07 l.61 "it may have overlapped the D1 step" (W1c, ruled) |
| "confirm…", "validat…" | 5: "NON-CONFIRMATORY" 3× (labels); "does not re-validate" 2× (06 l.244, 09 l.10; ruling 5 limits, negative sense) | none positive |
| "no effect", "not significant", "exceeds the SESOI" | 1 new: 06 l.244 "how often DETECTED is returned when no effect is present" (ruling 5 limit (ii), ruled E7 text) | not a claim of no effect; for the judge's G5 read |
| "RAGCap-style", "low power by design", "narrower than planned" | 0 | – |
| "split of a known" | 4: 3 at HEAD/E17-scoped rows (05 l.24 E17, 05 l.138 E18 line, 09 l.10), 1 new: 05 l.164 E3 "they do not carry 'split of a known τ_sel'" | not on a block-3 row |
| "larger" / "smaller" | 3 new: 06 l.246 ×2 "smaller than 2.0 points in either direction" (V8, W1b); 06 l.248 "neither is called larger" | no comparison of image-format with text-example rows |
| pooled / τ_any / masked / copy bound | 7: 3 at HEAD; 4 new, all in E3 "No pooled row, no τ_any, no masked contrast and no copy bound is computed for block 3." | negative statement, ruled |
| ASCII "-" before a digit; "−0.00"; Java; Vietnamese caption text | 0 | – |
| development label on new captions | Table 18 caption and Table S27 caption each carry "DEVELOPMENT / C-ATTR-DEV, NON-CONFIRMATORY" (1/1 each) | met |
| abstract, introduction (contributions), conclusion, bib, tex/ | byte-unchanged | met |
| manifest added rows | CC ids in the status column 127/127 (house practice of the manifest, not paper text) | – |

Whole-file counts on the six changed paper-text files (working tree; HEAD in brackets), `grep -cE`: `\bCC-[0-9]` 0 (0); `\bOPS-` 0 (0); `\bPI-[0-9]` 0 (0); `C-T1` 0 (0); `kit B` 0 (0); IPv4 pattern 0 (0); `\bssh\b`, `ckey`, `\bH1\b`, `ATTR_H1` 0 (0); `\bAI\b` 0 (0); `Claude|ChatGPT|Gemini|Codex` 0 (0); `no overlap` 0 (0); `\bport\b` 1 (1), the pre-existing 11 l.789 "The English port of the deletion step" (not a network port).

Format notes: the house helper for points has no "−0.00" guard of its own (only the bound helper has); no point value rounds to zero, and the "−0.00" count on added lines is 0.

## 8. Gate checklist

| gate | check | result |
|---|---|---|
| G0 (W1) | OPS-1113bb ALL PASS (8 rows), self-test ok | MET |
| G1 (records) | SHA256SUMS `d2500b48…`, 28/28 re-hashed equal; each source prefix in the manifest equal; `git ls-files data/results/c_attr_1113_b3score` = 29 files, last commit 7640a19; `git diff --quiet HEAD` clean and tracked for that folder, `data/results/c_attr_1112_score/res`, v1.1, addendum v1.2, block-3 run doc v1.1, its erratum 1 and the package (so the script's working-tree reads equal the committed bytes) | MET |
| G2 (base) | paper HEAD `44bbdd9…`, 11 HEAD blob shas = package list; package sha = CC-380 TARGET | MET |
| G3 (numbers) | 154 fills from the map; map = manifest `number` column 127/127; 127/127 rows re-read from source; house format, U+2212, no "−0.00", p̃ forms | MET |
| G4 (strings verbatim) | E6 strings: 03 1+1 (with citations), Table 18 caption 1+1; "batch size 1 (addendum v1.2 V8)" 2 (Table 18 caption, 11 header); "all arms decoded on one host in block 3; stored decodes not used" 1; W2 wording 6 (rows R2, R3, R6, R7 + the two 6.10.8 sentences; not on R1/R5); XM no-rule wording 4 (R5–R8); R8 UNRESOLVED sentence 1; "The positive control was met." 1; V4 (107 of 107) 1; V5 parity sentence 1 | MET (mechanical counts) |
| G4 + ruling 15 | W1b sentence 1; W1c sentence 1; E16, E17, E18, E19 strings 1 each | MET |
| G5 (forbidden) | see §7; "low power by design" / "narrower than planned" 0; no C-T1 / earlier-stage `lmcap_ri` or `ret_img` number beside a block-3 contrast (no such number in the E-rows) | MET mechanically; judge reads the "no effect is present" phrase |
| G6 (untouched) | 00, 01, 10 byte-unchanged; tex/ untouched | MET; the commit message must say tex/ and PDFs are stale (step 5) |
| G7 (shells) | 0 shell sentences | MET |
| G8 (hygiene) | no caption text, host/IP/port, machine label, CC/OPS/PI/C-T1 id, "kit B", Java string | MET |
| G9 (past tense) | job.log: 10 " OK B3_" lines, `JOB DONE gpu_h 3.70` (2026-11-12T23:27:30Z), 0 CAP STOP / JOB STOP; `STAGE_b3k5.prev_sha256` = sha(VERIFY.json) and `STAGE_b3rest.prev_sha256` = sha(K5.json), `B3_SUMMARY.k5_sha256` = sha(K5.json), `B3_SUMMARY.not_run` = []; K5 LOG line OPS-1113ai 00:24:14Z before b3rest OPS-1113an 00:25:30Z; mutants.log `107/107 killed; survived: none`, `rc 0`; gpu_seconds_try1.tsv 3 attempts (25+24+24 s), first start 2026-11-12T19:13:59Z; ca24e13 committed 2026-11-13T00:03:08Z (after JOB DONE); 60358b2 committed 2026-11-12T18:28:19Z (before the first launch); PREFLIGHT OK 19:44:24Z at 60358b2 | MET for these; the reference-file removal line, CC-370's 19:37:46Z and the ruling-6 facts against OPS-1113o rev, u, x, ac are left to the judge (ruling 15 (4)) |
| G10 (bib) | cite keys on added lines: `Ramos2023LMCap`, `Bazi2025RAGCap`, each once in paperC.bib; no new key; bib unchanged | MET |

## 9. Departures and points for the judge

1. **Folder.** CC-380 ruling 15 (3) names `paper_text/transfer_b3/`; the operator brief named `paper_text/transfer/`. The records are in `transfer/`, beside the untracked 1b transfer files, whose names they do not share; no 1b file was changed. The judge may rule the folder; a move changes no byte.
2. **W1 status wording.** Ruling 15 (3) fixes it: "W1 recompute pending" → "W1 recompute PASS" (no LOG id appended). Package §5 says the clause is dropped after W1; the ruling's wording was used.
3. **Aya-Vision-8B row.** The manifest row `VERDICT.json::…aya_vision_8b|tau_sel.label` (status "label (CC-363; shell C1 only)") is one of the 127 ruled rows and was appended; its placeholder is in no applied row. The judge may decide whether it waits for C1.
4. **Unused `.m` entries.** The map has `m` entries for R1, R3, R5–R8 that no E-row prints (Table 18's caption states "m = 1 on every row"); their manifest rows stay as backing for that caption.
5. **06 l.244 "when no effect is present".** Ruled E7 text (ruling 5 limit on the absent negative control); listed because G5 names "no effect".
6. **Guard scope.** The pattern guards of §7 ran on the diff's added lines (hits classified new vs. HEAD); the hygiene guards were also counted on the whole changed files (§7, last paragraph).
7. **G9 items not checked here** (ruling 15 (4) gives them to the judge): the reference-file removal line; CC-370's LOG time 19:37:46Z; the ruling-6 / W1c facts against OPS-1113o rev, u, x, ac.

## 10. Stale build

`tex/` and the PDF of the paper repo are stale after this transfer: no build was made on the laptop (CC-365 ruling 8; CC-380 carried item c4). The paper-repo commit message after the read's GO must say so.

## 11. Files of this record

`SHA256SUMS_B3_TRANSFER` (same folder) lists the record files, the script, the 7 changed paper files (absolute paths, working tree) and the 8 files of `paper_text/w1/`.
