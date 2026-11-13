# C-ATTR-DEV block 3: paper text package v1 (Paper C, ACM TALLIP)

Written 2026-11-13 (UTC, `date -u`) for a one-judge read (CC-358/CC-365 pattern) before any block-3 number enters the paper repo. Label of every row and sentence: `DEVELOPMENT / C-ATTR-DEV, NON-CONFIRMATORY`. Development sets OV-dev-B and XM-dev500 only; no test set was touched, staged or named. AI opinion, not expert-validated.

**Licence and gates.** CC-378 (sha256 `b78f184b…`, GO 88) licenses writing this package with the claim wording of its rulings 4–5 and the disclosure sentences of its ruling 3. It does not license any block-3 number in the paper repo before (1) W1, the ledger-level recompute (`c_attr_b3_ledger_recompute.py`, beside this file), returns ALL PASS or a judge rules a waiver, and (2) the transfer diff gets its own one-judge read (§6). Every number below is therefore a placeholder; the manifest of §5 gives the value each placeholder takes, read by me from the files, for the judge's check only.

**Three licence tiers.** Every piece carries one:
- **T-B3** (block-3 text). Unconditional in content; enters the paper only after W1 and the transfer read. §1–§3, §5.
- **T-CUT** (scope, block 2, the restored pointers). Only if the cut-off LOG line of CC-378 ruling 7 exists, stamped at or after 2026-11-14T11:00:00Z, with the content of its template. §4, shell C1.
- **T-K7** (block 4 and the freeze tense). Only after the K7 LOG line, stamped at or after 2026-11-16T05:00:00Z. §4, shell C2.

Nowhere does this package state, as a fact, that block 2 or block 4 did not run.

**Sources (sha256 prefix, re-hashed 2026-11-13).**
- Rulings: CC-378 `b78f184b`; CC-376 `80da2766`; CC-365 `f3624e74`; CC-363 `904ecf43`; CC-358 `ded17561`; LOG PI-1112e (item 3).
- Registered texts: v1.1 `44f81329`; erratum 1 `f9f0842e`; addendum v1.2 `5858d69d`; block-3 run document v1.1 `e8ae45a5` and its erratum 1 `e3a55b72`; block-3 scoring run document v1 `619a7f04`.
- The 1b package `C_ATTR_PAPER_TEXT_v1.md` `e1be6f93` (pattern, and the B2/B4/scope texts).
- Result files (`data/results/c_attr_1113_b3score/`, `sha256sum -c SHA256SUMS` 28/28 OK on 2026-11-13, SHA256SUMS `d2500b48`; untracked at writing, gatekeeper commit in progress):
  - `res/B3_SUMMARY.json` `61bf697b`; `res/K5.json` `bd9b0158`; `res/VERIFY.json` `28ab8f59`;
  - `decode/CAP_3.json` `542bb950`; `decode/gpu_seconds.tsv` `400be946`; `decode/gpu_seconds_try1.tsv` `6275b87c`; `decode/job.log` `e6081c58`; `decode/STEPS_3.tsv` `e77caf71`; `decode/D1_lmcap.json` `dd9bb57d`; `decode/D1_qwen25vl_7b.json` `799b0aed`;
  - `s0_hs/mutants.log` `9203e196`.
- Beside rows: `data/results/c_attr_1112_score/res/VERDICT.json` `a69a0ec2` and `SUMMARY.json` `1d78cd20` (committed at 42276d5).
- Code read for definitions only (not run): `scripts/c_attr/c_attr_score.py` `cca5e327` and `c_attr.py` `a3bd7b93` at ca24e13.
- Paper repo `vsps-paperC-tallip` at HEAD **`44bbdd9979ea03d0d9c30c435a0246984022c561`**; working tree clean apart from the untracked `docs/CC309_PARAGRAPH_DRAFT.md`. Files at HEAD (sha256 prefix): `03_method.md` `50b0529c`, `05_preregistration_and_analysis.md` `489c4b79`, `06_results.md` `61be0e29`, `07_disclosures.md` `8e58dc6d`, `09_limitations.md` `349703a1`, `11_supplement_registered_rows.md` `1223064f`, `number_manifest_C.tsv` `3eeb2dab`, `paperC.bib` `a415c4da`; `00_abstract.md` `4c023726`, `01_introduction.md` `b731e637`, `10_conclusion.md` `83d466df` (these three are not touched).

**Placeholders.**
- `{{A::key}}` is the value at `key` in the file with alias `A`; `~` stands for `|` inside row names, so that Markdown tables stay intact.
- `[[A::path]]` renders `{{A::path.d}} [{{A::path.lo}}, {{A::path.hi}}]`, in the house format of Tables 13 and 16: signed point, unsigned bounds unless negative, U+2212 minus, two decimals (CC-365 ruling 2).
- `[[A::path|90]]` adds `(90% interval [{{A::path.lo90}}, {{A::path.hi90}}])`.
- p̃ prints `at its floor (1/2,001)` in a table cell (`{{Rk.p}}`) and `1/2,001, its floor` in a sentence (`{{Rk.p|s}}`) when it equals 1/2,001; otherwise three significant digits.
- `[[Rk]]` with `Rk` a row name below renders `{{Rk.d}} [{{Rk.lo}}, {{Rk.hi}}]` from that row; `{{Rk.x}}` is key `x` of that row. Every placeholder of the E-rows maps to exactly one manifest row of §5; the map (placeholder → display) is §5.1.

| alias | file (run repo) |
|---|---|
| `B3S` | `data/results/c_attr_1113_b3score/res/B3_SUMMARY.json` |
| `K5` | `data/results/c_attr_1113_b3score/res/K5.json` |
| `VFY3` | `data/results/c_attr_1113_b3score/res/VERIFY.json` |
| `CAP3` | `data/results/c_attr_1113_b3score/decode/CAP_3.json` |
| `GS3`, `GS3T1` | `…/decode/gpu_seconds.tsv`, `…/decode/gpu_seconds_try1.tsv`; `Σ` = sum of the rows that are not `start` rows; `Σ/3600` in GPU-hours |
| `GS3+T1` | `GS3::Σ` + `GS3T1::Σ` (the total of record, CC-378 ruling 3(c)) |
| `JOB3` | `…/decode/job.log` (status lines only) |
| `D1L`, `D1Q` | `…/decode/D1_lmcap.json`, `…/decode/D1_qwen25vl_7b.json` |
| `MUT3` | `…/s0_hs/mutants.log` (last two lines) |
| `VER1B`, `SUM1B` | `data/results/c_attr_1112_score/res/VERDICT.json`, `…/SUMMARY.json` |
| `ERR3` | `manuscript/prereg/2026-11-11_c_attr_dev/C_ATTR_BLOCK3_RUN_DOC_ERRATUM_1.md` |
| `REG`, `ADD`, `RUN3` | registration v1.1, addendum v1.2, block-3 run document v1.1 (registered literals) |

Row paths used below: `R1` = `B3S::sets.ov_dev_b.rows.lmcap~tau_sel`, `R2` = `…ov_dev_b.rows.lmcap~tau_pair`, `R3` = `…ov_dev_b.rows.lmcap~tau_marg`, `R4` = `…ov_dev_b.rows.qwen25vl_7b~tau_sel_img`, `R5`–`R8` the same four under `sets.xm_dev500`; `BOV` = `VER1B::sets.ov_dev_b.rows.qwen25vl_7b~tau_sel`, `BXM` = `SUM1B::sets.xm_dev500.rows.qwen25vl_7b~tau_sel`.

---

## 1. Placement (a)

Numbering: the paper repo's at `44bbdd9`. Block 3 becomes **6.10.8**; the not-run subsection that the 1b package called 6.10.8 becomes **6.10.9** and is written only under shell C1 (§4). The two ruled pointers that named 6.10.8 for the not-run text (CC-365 N12: " Section 6.10.8 states which of them ran."; "(S-BB; Section 6.10.8)") are restored under C1 with 6.10.9 (open point J-B3-1). New tables continue the series: **Table 18** (main) and **Table S27** (supplement).

| # | piece | place in the paper | tier | E-row |
|---|---|---|---|---|
| P1 | block-3 arms, positive control, how block 3 was decoded (ruling 3(a), 3(b) sentences) | 03 §3.8, replaces the last paragraph "**Other registered arms.**" with four new paragraphs and a shortened "Other registered arms" | T-B3 | E1 |
| P2 | glossary rows | 05 Box 1, after the row "C-ATTR-DEV" | T-B3 | E2 |
| P3 | registered rule for block 3 (positive control, m = 1, first-look tiers) | 05 §5.7, new paragraph after "**XM-dev500.**" | T-B3 | E3 |
| P4 | block-3 scoring order | 05 §5.7 "Order of looks", appended | T-B3 | E4 |
| P5 | block-3 cap | 05 §5.7 "Budget", inserted before the freeze sentence | T-B3 | E5 |
| P6 | what ran in block 3 | 06 §6.10.1, appended | T-B3 | E6 |
| P7 | 6.10.8 with Table 18 (R1–R8 and two beside rows) | 06, new subsection after 6.10.7 | T-B3 | E7 |
| P8 | GPU-hours of block 3 | 06 §6.11 Compute | T-B3 | E8 |
| P9 | Box 2 row | 07 Box 2, after the row "other CPU checks beside running decodes …" | T-B3 | E9 |
| P10 | block order | 07 §7.5 "Block order", appended | T-B3 | E10 |
| P11 | block-3 disclosure bullet (ruling 3(d), CC-376 N4 facts, N1 sentence; optional 3(g) sentence) | 07 §7.5, new bullet before "What was post hoc" | T-B3 | E11 |
| P12 | limitation: what the positive control does not show | 09 §9.1, bullet "The attribution study is development-only …", appended | T-B3 | E12 |
| P13 | supplement header: Table 18/S27 pointers, block-3 batch label, release scope (PI-1112e item 3) | 11, header of "Attribution study (C-ATTR-DEV): every row" | T-B3 | E13, E14 |
| P14 | Table S27, block-3 decode record | 11, after the Table S26 closing sentence (end of file) | T-B3 | E15 |
| P14b | the one late commit (block-3 run-doc erratum) | 05 §5.7 "Files and order", one clause; the fact itself in E11 | T-B3 | E16 |
| P15 | manifest rows (§5) | `number_manifest_C.tsv`, appended | T-B3 | M |
| P16 | 6.10.9 and the restored pointers | 06, 03, 05, 07 | T-CUT / T-K7 | shells C1, C2 (§4) |
| – | abstract, introduction, contributions, conclusion, title | not touched (§7) | – | – |

---

## 2. New text for block 3 (b)

The paper-ready text is inside the E-rows of §3 (each NEW is what the paper gets). This section keeps the ruled sentences verbatim beside their paper-ready forms, so the judge can see each change.

### 2.1 Verbatim ruled sentences and their paper-ready forms

Changes are of three kinds only: internal codes removed (TG9: CC ids and the stage code "C-T1" are not defined in the paper and the rulings are not released, PI-1112e item 3); numbers as placeholders; and the house number format. Open point J-B3-2 asks the judge to accept these.

| id | ruling text (verbatim) | paper-ready form (in the E-row) | E-row |
|---|---|---|---|
| V1 | 3(a): "On the block-3 host the first launch stopped while loading the XGLM-2.9B weights, before any caption was generated, because the installed library versions refuse the pinned pytorch_model.bin; as in C-T1, the bit-identical safetensors copy of the same weights (sha256 9e292657…) was placed beside the pinned files and block 3 was restarted from its host checks (73 GPU-seconds charged, no output; CC-370)." | "… as in the exploration runs of the Flickr30K registration, the bit-identical safetensors copy … (sha256 {{ERR3::sha}}) … ({{GS3T1::Σ}} GPU-seconds charged, no output)." | E1 |
| V2 | 3(b): "lmcap_ri and ret_img on OV-dev-B were decoded again on the block-3 host so that every block-3 contrast pairs decodes of one host and one code path (disclosed deviation from registration v1.1 §6.5, fixed before any block-3 output; CC-368)." | "`lmcap_ri` and `ret_img` on OV-dev-B were decoded again on the block-3 host … (disclosed deviation from registration v1.1 §6.5, fixed before any block-3 output)." | E1 |
| V3 | 3(b) row note O1: "all arms decoded on one host in block 3; stored decodes not used" | verbatim, in the caption of Table 18 ("Every row: …") | E7 |
| V4 | 3(d): "The self-tests and the mutant run of the scoring code were first made in a scratch copy of the code beside the decode. Their binding to the committed bytes could not be shown as required, so they were set aside and the full self-test and mutant run (107 of 107 mutants killed) was repeated in the committed tree before any score was computed." | verbatim, with "107 of 107" filled from `MUT3` | E11 |
| V5 | CC-376 N1 (ruling 4): "the parity gate covers the segmenter, the references and kit B; the LMCap scoring path itself has no re-score against a ledger of record on this host." | "The scoring parity gate (Section 5.7) covers the segmenter, the references and the scoring kit; the LMCap scoring path itself has no re-score against a ledger of record on the block-3 host." ("kit B" is not a paper term.) | E11 |
| V6 | R1: "Positive control (registered): LMCap's text generator never sees the image, so the image reaches it only through the retrieved captions and the re-ranking of its beams. Replacing the retrieved captions with random ones should therefore lower its score. It did: +16.92 [+15.00, +19.06], DETECTED. The positive control was met. This is the first look at this contrast; the lmcap_ri level had been seen in an earlier stage (C-T1)." | "… It did: [[R1]] (p̃ = {{R1.p|s}}), {{R1.label}}. The positive control was met. This is the first look at this contrast; the `lmcap_ri` level on this set had been seen in the exploration runs of the Flickr30K registration (no number of those runs is used here)." | E7 |
| V7 | R2/R3, R6/R7 (W2): "computed after tau_sel, in the registered order; not the split of a tau_sel known when the rule was registered" | verbatim with τ_sel; it is fixed text, not the JSON `tier` string "first look (not a split of a known τ_sel: the sum was not known)" (CC-378 W2) | E3, E7 |
| V8 | R3: "smaller than 2.0 points in either direction (the 90% interval lies inside ±2.0); NEGLIGIBLE does not mean zero" | verbatim; plus the J9 power clause (open point J-B3-4) | E7 |
| V9 | R4: "first look; its ret_img side was seen in C-T1." | "first look; its `ret_img` side had been seen in the exploration runs of the Flickr30K registration." | E7 |
| V10 | XM-dev500: "no registered rule (v1.1 §7.8); label printed, no conclusion drawn" | "no registered rule (registration §7.8); label printed, no conclusion drawn" | E7 |
| V11 | R8: "UNRESOLVED: the data neither establish an effect of at least +2.0 nor bound it inside ±2.0." | verbatim | E7 |
| V12 | optional descriptive (ruling 4): "LMCap's retrieval-specific effect on OV-dev-B lies in the pairing of captions to the query (tau_pair DETECTED) and not in the set of captions shown (tau_marg NEGLIGIBLE), the same label pattern as the nominated claims of Section <6.x>; this is a description, not a check of those claims." | verbatim with "Section 6.10.3" and τ symbols; marked OPTIONAL in E7 (open point J-B3-5) | E7 |
| V13 | 3(g), optional: "Another study's agent copied code files to the block-3 host while its CPU window was closed, at or after 19:37:33Z; its end time is not recorded; no process ran from them until the window reopened after the cap line (OPS-1113o rev)." (run-record sentence) | not in the paper as worded (agent, window, OPS id); an OPTIONAL paper sentence of the same facts, matching the 1b "Other work on the same machine" bullet, is in E11 (open point J-B3-6) | E11 |
| V14 | ruling 5 (what K5 licenses; limits (i)–(vi)) | composed in E7 ("What the positive control shows") and E12, each limit kept; no "confirmed", "validated" or "test" | E7, E12 |

### 2.2 Claim → evidence (block 3)

| # | claim | section | status | evidence (`file::key`) |
|---|---|---|---|---|
| B1 | positive control met (LMCap τ_sel on OV-dev-B DETECTED; K5 not fired) | 6.10.8 | REGISTERED rule (v1.1 §7.10, §10.1), m = 1 | `R1.{d,lo,hi,p,m,label}`; `K5::verdict`, `K5::consequence` |
| B2 | LMCap τ_pair DETECTED, τ_marg NEGLIGIBLE on OV-dev-B | 6.10.8 | DESCRIPTIVE, first look, labelled | `R2.*`, `R3.*` incl. `lo90`, `hi90` |
| B3 | Qwen2.5-VL-7B image-format τ_sel DETECTED on OV-dev-B, beside the text-example row | 6.10.8 | DESCRIPTIVE, first look; no difference | `R4.*`; `BOV.{d,lo,hi,label}` |
| B4 | XM-dev500 rows: labels printed, no rule | 6.10.8 | DESCRIPTIVE, no rule (v1.1 §7.8) | `R5`–`R8`; `BXM.{d,lo,hi,label}` |
| B5 | the effect is about 8.5 × the SESOI; planned power at +2.0 unchanged | 6.10.8 | derived / registered planning value | `R1.d` / 2.0; REG §7.13 |
| B6 | ten steps, no cap stop, no job stop, none NOT RUN; 3.72 of 5.51 GPU-h | 6.10.1, 6.11, S27 | FACT | `CAP3::steps`, `::not_run`, `::cap_h`; `JOB3` status lines; `GS3+T1::Σ/3600` |
| B7 | D1 50/50 for both runners | 3.8, S27 | FACT | `D1L`, `D1Q::identical, n`; `VFY3::d1.*.D1` |
| B8 | first launch stopped at the model load, 73 s, no output | 3.8, 6.11, S27 | FACT | `GS3T1::Σ`; erratum `ERR3` |
| B9 | re-decodes of `lmcap_ri` and `ret_img` on OV-dev-B | 3.8 | FACT (disclosed deviation) | run doc v1.1 §2 steps 1 and 7; `CAP3::steps[0]`, `[6]` |
| B10 | scoring order: verification, positive control alone, then the rest; each stage once on the logged sha of the previous | 5.7 | FACT | `res/STAGE_b3k5.json::prev_sha256` = sha(VERIFY.json); `res/STAGE_b3rest.json::prev_sha256` = sha(K5.json); `B3S::k5_sha256` |
| B11 | 107 of 107 mutants killed in the committed tree | 7.5 | FACT | `MUT3` last two lines |
| B12 | scope sentence, block 2, block 4 | 6.10.9 | T-CUT / T-K7 shells | the LOG lines of §4; `VER1B::…aya_vision_8b~tau_sel.label` |

---

## 3. Edit rows E1–E19 (c)

Each OLD below occurs exactly once in its file at paper-repo HEAD `44bbdd9` (counted with `python3 -I` on 2026-11-13). The rows were applied in this order to scratch copies by plain string replacement; after the application each NEW occurs once, both erratum-E6 strings are unbroken, and no OLD of a later row is consumed by an earlier one. Format as in CC-365's ANNEX: the string is the text between the marker line and `<<<END>>>`, without the newline right after the opening marker and without the newline right before `<<<END>>>`. Minus signs inside placeholders are filled at transfer. Apostrophes are ASCII.

<<<E1 03_method.md OLD>>>
**Other registered arms.** The registration also names a memory swap on fixed English images, re-implemented third-party arms with random and permuted examples (a re-implementation of the LMCap recipe by this study; not the authors' code (no licence); not a statement about the published numbers [@Ramos2023LMCap]; and an image-caption-pair prompt format, as used by RAGCap; not RAGCap [@Bazi2025RAGCap]) and further backbones outside the Qwen language-model line.
<<<END>>>
<<<E1 03_method.md NEW>>>
**Third-party arms (block 3).** The registration applies the split to two further systems, on OV-dev-B and XM-dev500 only, with the estimands defined per image as above.

*LMCap:* a re-implementation of the LMCap recipe by this study; not the authors' code (no licence); not a statement about the published numbers [@Ramos2023LMCap]. It is the re-implementation of Section 3.7, with its four disclosed deviations, here writing Vietnamese captions from the registered Vietnamese memory. Its text generator never sees the image: the image reaches it only through the retrieved captions and through the multilingual CLIP re-rank of its three beams, which always uses the query image. Three arms differ only in the query's K = {{REG::§2 K}} captions. In `lmcap_ri` they are LMCap's own retrieval. In `lmcap_rand` they are the first {{REG::§2 K}} clusters of the query's `rand` d0 list that are not one of the N = {{REG::§2 N}} fixed demonstrations. In `lmcap_perm` they are the first {{REG::§2 K}} of the LMCap retrieval list of the donor π_1(q) that pass the query's near cut and are not a demonstration cluster (one permutation, p = 1). Demonstrations, template, beam and re-rank are unchanged. Then τ_sel = `lmcap_ri` − `lmcap_rand`, τ_pair = `lmcap_ri` − `lmcap_perm` and τ_marg = `lmcap_perm` − `lmcap_rand`.

*Image format:* an image-caption-pair prompt format, as used by RAGCap; not RAGCap [@Bazi2025RAGCap], for Qwen2.5-VL-7B. Each shown example is given as its image followed by its caption line (the interleaved image-caption arm named in Section 6.10.2), at the configuration of Table 2, with the same examples, order and tail as the text-example arm. `ret_img` shows the `ret` clusters in this format and `rand_img` the `rand` d0 clusters, and τ_sel = `ret_img` − `rand_img`. This row is printed beside the text-example τ_sel of the same backbone (Section 6.10.3); no difference between the two is computed, because it would be an unregistered contrast between prompt formats.

**The positive control.** LMCap's generator never sees the image, so retrieval must carry image information to it, and replacing its retrieved captions with random ones should lower its score. Its τ_sel on OV-dev-B is therefore the registered positive control of the attribution analysis: a case in which the answer is known in advance (Section 5.7).

**How block 3 was decoded.** Every block-3 arm was decoded at batch size 1 (LMCap decodes one query per call in any case) on one rented machine with no other GPU job. Before the first registered step, the determinism check D1 was made per runner on the arm that runner decodes in block 3 (`lmcap_ri` and `ret_img`, the first {{RUN3::§2 D1 50}} OV-dev-B items decoded in reversed and in stored order), in place of the `ret` items named in the addendum; both passed ({{D1L::identical}}/{{D1L::n}} and {{D1Q::identical}}/{{D1Q::n}} identical strings). `lmcap_ri` and `ret_img` on OV-dev-B were decoded again on the block-3 host so that every block-3 contrast pairs decodes of one host and one code path (disclosed deviation from registration v1.1 §6.5, fixed before any block-3 output). No decode stored by an earlier stage enters a block-3 contrast. On the block-3 host the first launch stopped while loading the XGLM-2.9B weights, before any caption was generated, because the installed library versions refuse the pinned pytorch_model.bin; as in the exploration runs of the Flickr30K registration, the bit-identical safetensors copy of the same weights (sha256 {{ERR3::sha}}) was placed beside the pinned files and block 3 was restarted from its host checks ({{GS3T1::Σ}} GPU-seconds charged, no output).

**Other registered arms.** The registration also names a memory swap on fixed English images and further backbones outside the Qwen language-model line.
<<<END>>>
<<<E2 05_preregistration_and_analysis.md OLD>>>
| C-ATTR-DEV | the attribution study's registration; every row carries "development, non-confirmatory" |
<<<END>>>
<<<E2 05_preregistration_and_analysis.md NEW>>>
| C-ATTR-DEV | the attribution study's registration; every row carries "development, non-confirmatory" |
| `lmcap_ri`, `lmcap_rand`, `lmcap_perm` | the LMCap re-implementation shown its own retrieved captions, random captions, or the retrieved captions of another image (Section 3.8) |
| `ret_img`, `rand_img` | retrieved or random examples shown to Qwen2.5-VL-7B as image-caption pairs (Section 3.8) |
| positive control | LMCap's τ_sel on OV-dev-B, which the registration required to be DETECTED (Sections 3.8 and 5.7) |
<<<END>>>
<<<E3 05_preregistration_and_analysis.md OLD>>>
so neither DETECTED at +2.0 nor NEGLIGIBLE can be decided reliably.
<<<END>>>
<<<E3 05_preregistration_and_analysis.md NEW>>>
so neither DETECTED at +2.0 nor NEGLIGIBLE can be decided reliably.

**Third-party arms and the positive control.** Block 3 adds, on OV-dev-B and XM-dev500, LMCap's τ_sel, τ_pair and τ_marg and the image-format τ_sel of Qwen2.5-VL-7B (Section 3.8). Each is a row of its own, outside every family (m = 1), with the labels above. The registration fixed one rule for them: LMCap's τ_sel on OV-dev-B must be DETECTED. Had it not been, the positive control would have failed and the third-party rows would have been printed without interpretation. On OV-dev-B every block-3 contrast is a first look, although the `lmcap_ri` and `ret_img` levels on this set had been seen in the exploration runs of the Flickr30K registration. LMCap's τ_pair and τ_marg are computed after τ_sel, in the registered order; they are not the split of a τ_sel known when the rule was registered, and they do not carry "split of a known τ_sel". The XM-dev500 rows carry no rule, as above. No pooled row, no τ_any, no masked contrast and no copy bound is computed for block 3.
<<<END>>>
<<<E4 05_preregistration_and_analysis.md OLD>>>
The scorer refused every OV-dev-B run before the nomination file existed and every batched run before the OV-dev-B verdict.
<<<END>>>
<<<E4 05_preregistration_and_analysis.md NEW>>>
The scorer refused every OV-dev-B run before the nomination file existed and every batched run before the OV-dev-B verdict. Block 3 was scored later, on the block-3 machine, CPU only, in three stages of its own run document: a verification stage; the positive control alone, whose result file was written and its sha256 logged before any other block-3 row was computed; and then the other block-3 rows. Each stage required the logged sha256 of the previous stage's file and ran once.
<<<END>>>
<<<E5 05_preregistration_and_analysis.md OLD>>>
Tier A was never to run in part.
<<<END>>>
<<<E5 05_preregistration_and_analysis.md NEW>>>
Tier A was never to run in part. Block 3 had a hard cap of {{REG::§6.5 5}} GPU-hours in version 1.1; the addendum replaced it by {{ADD::V8}} GPU-hours, with P3 projected from the batch-size-1 rates measured in block 3's own D1 check and logged before its first registered step. P3 was computed over all ten steps of block 3, the two re-decodes included (Section 3.8).
<<<END>>>
<<<E6 06_results.md OLD>>>
and the scoring parity gate passed (ok).
<<<END>>>
<<<E6 06_results.md NEW>>>
and the scoring parity gate passed (ok). Block 3 (Section 6.10.8) decoded its arms at batch size 1 on another rented machine, under the hard cap of {{CAP3::cap_h}} GPU-hours fixed after its D1 check, and used {{GS3+T1::Σ/3600}} GPU-hours, the D1 check and a first launch that stopped at the model load included. All {{CAP3::steps|count}} steps of its run document finished, with no cap stop, no job stop and no step NOT RUN. Its scoring passed its verification stage, with the scoring parity gate passed ({{VFY3::parity_7_1.result}}).
<<<END>>>
<<<E7 06_results.md OLD>>>
Host parity held for every backbone, so no base arm was re-decoded.

### 6.11 Compute
<<<END>>>
<<<E7 06_results.md NEW>>>
Host parity held for every backbone, so no base arm was re-decoded.

#### 6.10.8 The positive control and the third-party arms (block 3)

**Table 18. Third-party arms at batch size 1 (block 3). DEVELOPMENT / C-ATTR-DEV, NON-CONFIRMATORY. OV-dev-B ({{B3S::sets.ov_dev_b.n}} images) and XM-dev500 ({{B3S::sets.xm_dev500.n}} images); stripped CIDEr-D points, paired 95% bootstrap CIs, B = 2,000, one index matrix per set; one `rand` draw (d0) and one permutation (p = 1). p̃: one-sided p-like statistic; "at its floor (1/2,001)" means the floor of the bootstrap statistic, 1/2,001, not an exact p-value. m = 1 on every row (no family). Every block-3 row: "batch size 1 (addendum v1.2 V8)"; "all arms decoded on one host in block 3; stored decodes not used". LMCap rows: "re-implementation of the LMCap recipe by this study; not the authors' code (no licence); not a statement about the published numbers". Image-format rows: "image-caption-pair prompt format, as used by RAGCap; not RAGCap". Rows marked "beside" repeat the text-example τ_sel of Tables 16 and S21 for reading only: they were decoded in block 1b on another machine and average R = 3 `rand` draws per image; they carry their block-1b label "batch size 1; registered in v1.2 after K1 fired, on string-identity counts only"; their p̃ is in Table 16, and Table S21 prints none ("–"); no difference is computed.**

| set | system | estimand | difference [95% CI] | p̃ | label | note |
|---|---|---|---|---|---|---|
| OV-dev-B | LMCap | τ_sel | [[R1]] | {{R1.p}} | {{R1.label}} | registered positive control; first look at this contrast |
| OV-dev-B | LMCap | τ_pair | [[R2]] | {{R2.p}} | {{R2.label}} | first look; computed after τ_sel, in the registered order; not the split of a τ_sel known when the rule was registered |
| OV-dev-B | LMCap | τ_marg | [[R3]]; 90% [{{R3.lo90}}, {{R3.hi90}}] | {{R3.p}} | {{R3.label}} | first look; computed after τ_sel, in the registered order; not the split of a τ_sel known when the rule was registered |
| OV-dev-B | Qwen2.5-VL-7B, image format | τ_sel | [[R4]] | {{R4.p}} | {{R4.label}} | first look; its `ret_img` side had been seen in the exploration runs of the Flickr30K registration |
| OV-dev-B | Qwen2.5-VL-7B, text examples (beside) | τ_sel | [[BOV]] | see Table 16 | {{BOV.label}} | block 1b; batch-1 re-decode of a known τ_sel |
| XM-dev500 | LMCap | τ_sel | [[R5]] | {{R5.p}} | {{R5.label}} | no registered rule (registration §7.8); label printed, no conclusion drawn |
| XM-dev500 | LMCap | τ_pair | [[R6]] | {{R6.p}} | {{R6.label}} | no registered rule (registration §7.8); label printed, no conclusion drawn; computed after τ_sel, in the registered order; not the split of a τ_sel known when the rule was registered |
| XM-dev500 | LMCap | τ_marg | [[R7]]; 90% [{{R7.lo90}}, {{R7.hi90}}] | {{R7.p}} | {{R7.label}} | no registered rule (registration §7.8); label printed, no conclusion drawn; computed after τ_sel, in the registered order; not the split of a τ_sel known when the rule was registered |
| XM-dev500 | Qwen2.5-VL-7B, image format | τ_sel | [[R8]] | {{R8.p}} | {{R8.label}} | no registered rule (registration §7.8); label printed, no conclusion drawn |
| XM-dev500 | Qwen2.5-VL-7B, text examples (beside) | τ_sel | [[BXM]] | – | {{BXM.label}} | block 1b; no rule |

**The positive control (registered).** LMCap's text generator never sees the image, so the image reaches it only through the retrieved captions and the re-ranking of its beams. Replacing the retrieved captions with random ones should therefore lower its score. It did: [[R1]] (p̃ = {{R1.p|s}}), {{R1.label}}. The positive control was met. This is the first look at this contrast; the `lmcap_ri` level on this set had been seen in the exploration runs of the Flickr30K registration (no number of those runs is used here).

**What the positive control shows, and what it does not.** The registered contrast and label rule returned DETECTED in a case where the answer was known in advance: retrieval must carry image information to an image-blind generator. This is evidence that the arms, the scoring path for these rows and the bootstrap and label rules can detect a retrieval-specific effect when one is present. The effect is about {{R1.d/2.0}} times the SESOI of +2.0, so the control says nothing about sensitivity near +2.0: the planned chance of DETECTED at a true +2.0 on OV-dev-B stays {{REG::§7.13 about 0.49}} at the planned standard error of Qwen2.5-VL-7B (registration §7.13; values are for m = 1). It has no negative control, so it says nothing about how often DETECTED is returned when no effect is present; the `rand` d1 − d2 placebo rows of Section 6.10.5 are the study's only such check, and one of them, Aya-Vision-8B's on OV-dev-B, was flagged. It does not re-validate or strengthen the rows of Section 6.10.3, neither the two nominated τ_pair claims nor the τ_marg rows: those rest on their own registration, scoring path and labels, while LMCap ran on another model, pipeline and scoring path, on another machine. It says nothing about the `perm` arm's validity for those rows or about how their τ_sel splits, nothing about LMCap's published numbers or the authors' system, and nothing about any test set or about XM-dev500.

**LMCap's split on OV-dev-B.** LMCap's τ_pair was [[R2]] (p̃ = {{R2.p|s}}, m = {{R2.m}}): {{R2.label}}; first look; computed after τ_sel, in the registered order; not the split of a τ_sel known when the rule was registered. LMCap's τ_marg was [[R3|90]]: {{R3.label}}, smaller than 2.0 points in either direction (the 90% interval lies inside ±2.0); NEGLIGIBLE does not mean zero. First look; computed after τ_sel, in the registered order; not the split of a τ_sel known when the rule was registered. The registration's planning values for this label belong to Qwen2.5-VL-7B (standard error {{REG::§7.13 about 1.03}} on OV-dev-B, where NEGLIGIBLE needs a point within {{REG::§7.13 about ±0.3}} of zero; registration §7.13; values are for m = 1); no planning value was registered for LMCap. LMCap's retrieval-specific effect on OV-dev-B lies in the pairing of captions to the query (τ_pair DETECTED), while the part given by the set of captions shown is smaller than 2.0 points in either direction (τ_marg NEGLIGIBLE): the same label pattern as the τ_pair and τ_marg rows of Qwen2.5-VL-7B and InternVL3-8B on this set (Section 6.10.3). This is a description, not a check of those rows.

**The image format on OV-dev-B.** Qwen2.5-VL-7B's image-format τ_sel was [[R4]] (p̃ = {{R4.p|s}}, m = {{R4.m}}): {{R4.label}}; first look; its `ret_img` side had been seen in the exploration runs of the Flickr30K registration. Beside it, the text-example τ_sel of the same backbone on this set was [[BOV]], {{BOV.label}}, with its own labels (Table 16). The two rows were decoded on different machines, in different blocks. No difference or ratio between them is computed, and neither is called larger: that would be an unregistered contrast between prompt formats.

**XM-dev500.** Every XM-dev500 row of Table 18 has no registered rule (registration §7.8): its label is printed and no conclusion is drawn, for the DETECTED rows as well. Qwen2.5-VL-7B's image-format row there is UNRESOLVED: the data neither establish an effect of at least +2.0 nor bound it inside ±2.0. Beside it, the text-example row of Table S21 is printed with its own label; no difference is computed.

### 6.11 Compute
<<<END>>>
<<<E8 06_results.md OLD>>>
6.41 GPU-hours in block 1 (cap 12) and 12.27 in block 1b (cap 17.95), on one 24 GB GPU; its scoring ran on CPU.
<<<END>>>
<<<E8 06_results.md NEW>>>
6.41 GPU-hours in block 1 (cap 12), 12.27 in block 1b (cap 17.95) and {{GS3+T1::Σ/3600}} in block 3 (cap {{CAP3::cap_h}}; {{GS3T1::Σ/3600}} of them in a first launch that stopped at the model load, Section 3.8), on one 24 GB GPU; its scoring ran on CPU.
<<<END>>>
<<<E9 07_disclosures.md OLD>>>
| other CPU checks beside running decodes; pulled-tree checksum list omits the job's final log lines (Section 7.5) | none | none | no |
<<<END>>>
<<<E9 07_disclosures.md NEW>>>
| other CPU checks beside running decodes; pulled-tree checksum list omits the job's final log lines (Section 7.5) | none | none | no |
| block 3: a first launch stopped at the model load, with no output; two OV-dev-B arms decoded again on the block-3 machine; scoring-code checks first made in a scratch copy and repeated in the committed tree; other work on the machine during the decode; one run-document erratum committed after the decode (Sections 3.8, 5.7 and 7.5) | block-3 contrasts use block-3 decodes only; no other effect was tested | none | no |
<<<END>>>
<<<E10 07_disclosures.md OLD>>>
Block 1b re-decoded every contrast arm at batch size 1. Scoring followed in the registered order (Section 5.7).
<<<END>>>
<<<E10 07_disclosures.md NEW>>>
Block 1b re-decoded every contrast arm at batch size 1. Scoring followed in the registered order (Section 5.7). After block 1b had been scored, block 3 decoded the third-party arms at batch size 1 on another rented machine and was scored in its own registered order, the positive control first (Sections 3.8 and 5.7).
<<<END>>>
<<<E11 07_disclosures.md OLD>>>
- **What was post hoc.**
<<<END>>>
<<<E11 07_disclosures.md NEW>>>
- **Block 3.** The first launch, the re-decodes of two OV-dev-B arms and the replaced D1 items are stated in Section 3.8. The self-tests and the mutant run of the scoring code were first made in a scratch copy of the code beside the decode. Their binding to the committed bytes could not be shown as required, so they were set aside and the full self-test and mutant run ({{MUT3::107 of 107}} mutants killed) was repeated in the committed tree before any score was computed. That mutant run, like the earlier ones, ran without network isolation. The two reference files were staged again from the copies of record at their pinned hashes and removed from the machine after the scoring outputs had been pulled. The scoring environment is recorded by the sha256 of its installed-package listing ({{VFY3::env.packages_sha256|8}}). The stored zero-shot decodes of Qwen2.5-VL-7B entered the scoring call only because the scorer needs one zero-shot run per backbone; they enter no block-3 contrast. An identity check of the block-3 `lmcap_ri` and `ret_img` decodes against the decodes of the earlier stage was optional and was not run. The erratum to the block-3 run document that adds the staging step for the XGLM-2.9B weights file (Section 3.8) was reviewed before block 3 was relaunched, but was committed only after block 3 had been decoded, together with the scoring code; the other block-3 run documents and code were committed before the steps they govern. The scoring parity gate (Section 5.7) covers the segmenter, the references and the scoring kit; the LMCap scoring path itself has no re-score against a ledger of record on the block-3 host. Other work also ran on the block-3 machine: CPU-only code self-tests and mutant runs of another study of the group, during the machine's set-up and, after the D1 step, while block 3 decoded, each with the copying of its code files and the set-up of its Python environment; and, after the D1 step, the scratch checks of the scoring code named above. None used the GPU. One copy of that study's code files (file writes only; nothing was run from them before the block-3 cap had been logged) started after a check made shortly before block 3 was relaunched, and its end is not recorded, so it may have overlapped the D1 step. As in blocks 1 and 1b, these are disclosed as deviations from the registration's rule that no job runs beside another. Whether this work changed a greedy string or a timing was not tested.
- **What was post hoc.**
<<<END>>>
<<<E12 09_limitations.md OLD>>>
The copy bound rests on assumption A_cp, which can only overstate copying, and it bounds the stored batched contrast, not the batch-size-1 one.
<<<END>>>
<<<E12 09_limitations.md NEW>>>
The copy bound rests on assumption A_cp, which can only overstate copying, and it bounds the stored batched contrast, not the batch-size-1 one. The registered positive control (Section 6.10.8) shows that the analysis returns DETECTED when a large retrieval-specific effect is present by construction, for an image-blind generator; it does not show sensitivity near +2.0, it has no negative control, and it does not re-validate the rows of the three backbones.
<<<END>>>
<<<E13 11_supplement_registered_rows.md OLD>>>
Tables S20–S26 give the rows of the study's scoring files, with the label, family, tier and batch label the scorer wrote; the placebo and draw-variance entries of the batched runs are not printed. Batch-size-1 rows carry
<<<END>>>
<<<E13 11_supplement_registered_rows.md NEW>>>
Tables S20–S26 give the rows of the study's scoring files, with the label, family, tier and batch label the scorer wrote; the placebo and draw-variance entries of the batched runs are not printed. Table 18 gives the block-3 rows, with the scorer's labels and with tier notes worded as in Section 6.10.8, and Table S27 the block-3 decode record. Block-3 rows carry "batch size 1 (addendum v1.2 V8)". Other batch-size-1 rows carry
<<<END>>>
<<<E14 11_supplement_registered_rows.md OLD>>>
The registration, its erratum and addendum, the run documents and the rulings that read them will be released with the code on publication.
<<<END>>>
<<<E14 11_supplement_registered_rows.md NEW>>>
The registration, its erratum and addendum, and the run documents will be released with the code on publication.
<<<END>>>
<<<E15 11_supplement_registered_rows.md OLD>>>
On every set the refill share stayed within the registered gate, so `perm` carries its rules on every set (Table S26).
<<<END>>>
<<<E15 11_supplement_registered_rows.md NEW>>>
On every set the refill share stayed within the registered gate, so `perm` carries its rules on every set (Table S26).

**Table S27. Block-3 decode record (counts and GPU-seconds; no score). DEVELOPMENT / C-ATTR-DEV, NON-CONFIRMATORY. Every decode at batch size 1, on one rented machine.**

| step | system | arm | set | images | GPU-seconds |
|---|---|---|---|---|---|
| first launch (three attempts of the first D1 decode, each stopped at the model load; no output) | LMCap | `lmcap_ri` | OV-dev-B | – | {{GS3T1::Σ}} |
| D1 | LMCap | `lmcap_ri`, reversed, then stored order | OV-dev-B | {{RUN3::§2 D1 50}} + {{RUN3::§2 D1 50}} | {{GS3::line 2}} + {{GS3::line 4}} |
| D1 | Qwen2.5-VL-7B | `ret_img`, reversed, then stored order | OV-dev-B | {{RUN3::§2 D1 50}} + {{RUN3::§2 D1 50}} | {{GS3::line 6}} + {{GS3::line 8}} |
| 1 | LMCap | `lmcap_ri` (decoded again on this machine) | OV-dev-B | {{CAP3::steps[0].n}} | {{GS3::line 10}} |
| 2 | LMCap | `lmcap_rand` | OV-dev-B | {{CAP3::steps[1].n}} | {{GS3::line 12}} |
| 3 | LMCap | `lmcap_perm` | OV-dev-B | {{CAP3::steps[2].n}} | {{GS3::line 14}} |
| 4 | LMCap | `lmcap_ri` | XM-dev500 | {{CAP3::steps[3].n}} | {{GS3::line 16}} |
| 5 | LMCap | `lmcap_rand` | XM-dev500 | {{CAP3::steps[4].n}} | {{GS3::line 18}} |
| 6 | LMCap | `lmcap_perm` | XM-dev500 | {{CAP3::steps[5].n}} | {{GS3::line 20}} |
| 7 | Qwen2.5-VL-7B | `ret_img` (decoded again on this machine) | OV-dev-B | {{CAP3::steps[6].n}} | {{GS3::line 22}} |
| 8 | Qwen2.5-VL-7B | `rand_img` | OV-dev-B | {{CAP3::steps[7].n}} | {{GS3::line 24}} |
| 9 | Qwen2.5-VL-7B | `ret_img` | XM-dev500 | {{CAP3::steps[8].n}} | {{GS3::line 26}} |
| 10 | Qwen2.5-VL-7B | `rand_img` | XM-dev500 | {{CAP3::steps[9].n}} | {{GS3::line 28}} |
| total | | | | | {{GS3+T1::Σ}} ({{GS3+T1::Σ/3600}} GPU-hours) |

D1 identical strings: LMCap {{D1L::identical}}/{{D1L::n}} ({{VFY3::d1.lmcap.D1}}), Qwen2.5-VL-7B {{D1Q::identical}}/{{D1Q::n}} ({{VFY3::d1.qwen25vl_7b.D1}}). Decode rates measured in D1: LMCap {{CAP3::rates_L_r.lmcap[1]}} s per caption (load {{CAP3::rates_L_r.lmcap[0]}} s), Qwen2.5-VL-7B {{CAP3::rates_L_r.qwen25vl_7b[1]}} s (load {{CAP3::rates_L_r.qwen25vl_7b[0]}} s). Projection P3 = {{CAP3::P_h}} GPU-hours over the ten steps; hard cap min(12, 1.5 P3) = {{CAP3::cap_h}} GPU-hours ({{CAP3::cap_s}} s), logged before step 1. The decode job's own total is {{GS3::Σ}} s ({{JOB3::JOB DONE gpu_h}} GPU-hours); the first launch adds {{GS3T1::Σ}} s. No step was dropped and none ran in part.
<<<END>>>

<<<E16 05_preregistration_and_analysis.md OLD>>>
Each file, each code version and each run document was reviewed and committed before the step it governs.
<<<END>>>
<<<E16 05_preregistration_and_analysis.md NEW>>>
Each file, each code version and each run document was reviewed and committed before the step it governs, with one exception in block 3 (Section 7.5).
<<<END>>>
<<<E17 05_preregistration_and_analysis.md OLD>>>
| split of a known τ_sel | wording attached to every τ_pair and τ_marg row on OV-dev-A and OV-dev-B, where τ_sel was already known (Section 5.7) |
<<<END>>>
<<<E17 05_preregistration_and_analysis.md NEW>>>
| split of a known τ_sel | wording attached to every τ_pair and τ_marg row of the three backbones of Section 3.8 on OV-dev-A and OV-dev-B, where τ_sel was already known (Section 5.7); the block-3 rows do not carry it |
<<<END>>>
<<<E18 05_preregistration_and_analysis.md OLD>>>
Every row and sentence about τ_pair or τ_marg on OV-dev-A or OV-dev-B therefore carries the words
<<<END>>>
<<<E18 05_preregistration_and_analysis.md NEW>>>
Every row and sentence about the three backbones' τ_pair or τ_marg on OV-dev-A or OV-dev-B therefore carries the words
<<<END>>>
<<<E19 05_preregistration_and_analysis.md OLD>>>
At batch size 1, τ_sel on OV-dev-A and OV-dev-B carries
<<<END>>>
<<<E19 05_preregistration_and_analysis.md NEW>>>
At batch size 1, the three backbones' text-example τ_sel on OV-dev-A and OV-dev-B carries
<<<END>>>

Notes for the transfer (not paper text):
- E1 keeps both erratum-E6 strings whole, each followed (not interrupted) by its citation, as CC-358 W3 requires; the short "Other registered arms" no longer lists the third-party arms, because they now have their own paragraph. It makes no status claim about blocks 2 and 4 (CC-365 B2).
- E1 places the ruling-3(a) and 3(b) sentences in the method section (Section 3.8), once, as ruling 3(a) and CC-370 W2 ask; Box 2 (E9) and 7.5 (E11) point to it without repeating it.
- E6: "no cap stop and no job stop" rests on `JOB3` (10 `OK B3_` lines, 0 `CAP STOP`/`JOB STOP` lines, `JOB DONE gpu_h 3.70`); "none NOT RUN" on `CAP3::not_run` = [] and `B3S::not_run` = [].
- E7: Table 18 prints the 90% interval only on the two NEGLIGIBLE rows (as the 1b sentences do); the other 90% bounds stay in the file.
- E8 prints 0.02 for the first launch: 73 s / 3600 = 0.0203. The total 3.72 = (13,318 + 73) s / 3600 (CC-378 ruling 3(c)); the job's own JOB DONE line says 3.70 and is printed in Table S27 only.
- E11 `{{VFY3::env.packages_sha256|8}}` prints the first eight hex digits and an ellipsis.

---

## 4. Conditional shells (d)

Nothing in this section enters the paper unless its condition holds. Each shell has exact text and an exact condition. A LOG line that exists but differs in content from the condition gives no sentence: the matter goes to a judge.

### Shell C1 (T-CUT): the block-2 cut-off

**Condition, all of:**
1. a decisions-LOG line whose id ends `-c-b2-cutoff`, stamped (`date -u`) at or after `2026-11-14T11:00:00Z`;
2. its text equals, as a string, the EXACT CUT-OFF LINE template of CC-378 ruling 7 with only `<utc>` and `<id>` filled (the template's line breaks and indentation in the CC file joined to single spaces); any other difference gives no sentence and goes to a judge;
3. `VER1B::sets.ov_dev_b.rows.aya_vision_8b|tau_sel.label` = DETECTED (manifest row);
4. no block-2 host, package, read or decode on the LOG (the line itself confirms it).

**If C1 holds, five pieces enter (the transfer for C1 is a new diff with its own read, or a ruled addendum to the block-3 transfer read):**

C1-a, 06, new subsection after 6.10.8 (OLD = `### 6.11 Compute`, inserted before it):

> #### 6.10.9 What did not run
>
> Block 2, which would have added backbones outside the Qwen language-model line, was not run by its registered cut-off (2026-11-14 18:00, UTC+7); the secondary family S-BB is empty.
>
> Scope (registration §7.6), counting the non-Qwen backbones whose τ_sel on OV-dev-B is DETECTED: the retrieval-specific effect was seen for one backbone outside the Qwen line. This count rests on one backbone, Aya-Vision-8B, whose row is post hoc (its τ_sel on this set was known before the registration) and a batch-1 re-decode of a known τ_sel; no backbone first decoded under this registration was run. Aya-Vision-8B's row ({{VER1B::sets.ov_dev_b.rows.aya_vision_8b~tau_sel.label}}, Table 16) also carries the placebo flag of Section 6.10.5. InternVL3-8B runs on a Qwen2.5 language model and is not counted.
>
> Block 3 ran (Section 6.10.8).

Variant before the K7 line: the B2 sentence above (the 1b package l.363 text without its words "or before the freeze", which would state a future event in the past tense; CC-365 B1 precedent). After the K7 line (shell C2) the sentence takes its full 1b form: "… was not run by its registered cut-off (2026-11-14 18:00, UTC+7) or before the freeze; the secondary family S-BB is empty."

C1-b, 03 (E1's NEW, last paragraph): `**Other registered arms.** The registration also names a memory swap on fixed English images and further backbones outside the Qwen language-model line.` → append ` Section 6.10.9 states whether they ran.` (CC-365 N12, renumbered; "which of them ran" → "whether they ran" ruled in CC-380). C1-b enters only when C2 also holds: the memory swap's status is stated only by C2-a.

C1-c, 05 §5.7 Multiplicity: `(S-BB)` → `(S-BB; Section 6.10.9)` (CC-365 N12, renumbered; OLD occurs once at HEAD).

C1-d, 07 §7.5 Block order (after E10): append ` Block 2 was not run by its registered cut-off (Section 6.10.9).`

C1-e, manifest: the Aya label row of §5 (status already set) and one row for the LOG line, status `FACT_RECORDED (LOG line id, stamp)`; the count "one" is derived from the label and the line, not from the LOG alone.

No third scope sentence (K4 does not fire: CC-378 ruling 7). The 6.10.4 sentence "no XM-dev500 row enters a family or a scope sentence" stays.

### Shell C2 (T-K7): the freeze

**Condition, all of:** C1 has entered; a decisions-LOG K7 line stamped at or after `2026-11-16T05:00:00Z` lists block-4 steps 4.1–4.5 (with the memory swap of §7.9) as NOT RUN; no block-4 package, read or host exists on the LOG. If a block-4 package or run exists, no sentence of C2 applies (CC-378 ruling 7; CC-363 W3).

**If C2 holds:**

C2-a, 06 §6.10.9, appended (1b package l.370, verbatim):

> Block 4 was not run before the freeze: the English `perm` and extra `rand` arms and the size-matched memory swap on fixed Flickr30K val images have no rows. The memory-source question on Vietnamese data could not be posed in any case: the registered Vietnamese memory holds 40 KTVIC-only clusters out of 8,190, so no out-of-source Vietnamese memory exists in it.

and the B2 sentence of C1-a takes its full form (above).

C2-b, 05 Budget: `A freeze at 2026-11-16 12:00 (UTC+7) ends every step not finished by then.` → `A freeze at 2026-11-16 12:00 (UTC+7) ended every step not finished by then.` (CC-365 N13).

C2-c, 07 §7.5 Block order: append ` Block 4 was not run before the freeze (Section 6.10.9).`

C2-d, the K6 consequence ("swap NOT RUN") needs no further sentence: C2-a says the swap has no rows.

Open point J-B3-8: block 4 includes step 4.4 (LMCap `lmcap_rand` and `lmcap_perm` on the COCO memory); the 1b B4 text names "the English `perm` and extra `rand` arms" without naming LMCap.

---

## 5. Manifest rows (e)

127 rows to append to `number_manifest_C.tsv`, in its columns (`number | file::key | raw_value | sha256_prefix | status | used_in`). Every value was read by me with one `python3 -I` script over the JSON/TSV files (scratchpad; it reads no ledger and runs no repo code) and is printed here as the paper prints it. Rows keyed to `B3S` carry `W1 recompute pending` in their status: at transfer the status loses that clause only after W1 passes. Row names use `|` as in the house manifest. Derived rows state their rule in the key. Registered literals point to the registered text. The beside rows key to the committed 1b files (re-hashed: `a69a0ec2`, `1d78cd20`).

```tsv
number	file::key	raw_value	sha256_prefix	status	used_in
925	data/results/c_attr_1113_b3score/res/B3_SUMMARY.json::sets.ov_dev_b.n	925	61bf697b9015	keyed (DEVELOPMENT / C-ATTR-DEV, NON-CONFIRMATORY; CC-378; W1 recompute pending)	06_results.md
+16.92	data/results/c_attr_1113_b3score/res/B3_SUMMARY.json::sets.ov_dev_b.rows.lmcap|tau_sel.d	16.92275945945946	61bf697b9015	keyed (DEVELOPMENT / C-ATTR-DEV, NON-CONFIRMATORY; CC-378; W1 recompute pending)	06_results.md
15.00	data/results/c_attr_1113_b3score/res/B3_SUMMARY.json::sets.ov_dev_b.rows.lmcap|tau_sel.lo	15.002931970270268	61bf697b9015	keyed (DEVELOPMENT / C-ATTR-DEV, NON-CONFIRMATORY; CC-378; W1 recompute pending)	06_results.md
19.06	data/results/c_attr_1113_b3score/res/B3_SUMMARY.json::sets.ov_dev_b.rows.lmcap|tau_sel.hi	19.055565594594594	61bf697b9015	keyed (DEVELOPMENT / C-ATTR-DEV, NON-CONFIRMATORY; CC-378; W1 recompute pending)	06_results.md
at its floor (1/2,001)	data/results/c_attr_1113_b3score/res/B3_SUMMARY.json::sets.ov_dev_b.rows.lmcap|tau_sel.p	0.0004997501249375312	61bf697b9015	keyed (DEVELOPMENT / C-ATTR-DEV, NON-CONFIRMATORY; CC-378; W1 recompute pending)	06_results.md
1/2,001, its floor	data/results/c_attr_1113_b3score/res/B3_SUMMARY.json::sets.ov_dev_b.rows.lmcap|tau_sel.p	0.0004997501249375312	61bf697b9015	keyed (DEVELOPMENT / C-ATTR-DEV, NON-CONFIRMATORY; CC-378; W1 recompute pending)	06_results.md
1	data/results/c_attr_1113_b3score/res/B3_SUMMARY.json::sets.ov_dev_b.rows.lmcap|tau_sel.m	1	61bf697b9015	keyed (DEVELOPMENT / C-ATTR-DEV, NON-CONFIRMATORY; CC-378; W1 recompute pending)	06_results.md
DETECTED	data/results/c_attr_1113_b3score/res/B3_SUMMARY.json::sets.ov_dev_b.rows.lmcap|tau_sel.label	'DETECTED'	61bf697b9015	label (DEVELOPMENT / C-ATTR-DEV; CC-378; W1 recompute pending)	06_results.md
+17.40	data/results/c_attr_1113_b3score/res/B3_SUMMARY.json::sets.ov_dev_b.rows.lmcap|tau_pair.d	17.402667459459458	61bf697b9015	keyed (DEVELOPMENT / C-ATTR-DEV, NON-CONFIRMATORY; CC-378; W1 recompute pending)	06_results.md
15.48	data/results/c_attr_1113_b3score/res/B3_SUMMARY.json::sets.ov_dev_b.rows.lmcap|tau_pair.lo	15.480765094594592	61bf697b9015	keyed (DEVELOPMENT / C-ATTR-DEV, NON-CONFIRMATORY; CC-378; W1 recompute pending)	06_results.md
19.41	data/results/c_attr_1113_b3score/res/B3_SUMMARY.json::sets.ov_dev_b.rows.lmcap|tau_pair.hi	19.40936236486486	61bf697b9015	keyed (DEVELOPMENT / C-ATTR-DEV, NON-CONFIRMATORY; CC-378; W1 recompute pending)	06_results.md
at its floor (1/2,001)	data/results/c_attr_1113_b3score/res/B3_SUMMARY.json::sets.ov_dev_b.rows.lmcap|tau_pair.p	0.0004997501249375312	61bf697b9015	keyed (DEVELOPMENT / C-ATTR-DEV, NON-CONFIRMATORY; CC-378; W1 recompute pending)	06_results.md
1/2,001, its floor	data/results/c_attr_1113_b3score/res/B3_SUMMARY.json::sets.ov_dev_b.rows.lmcap|tau_pair.p	0.0004997501249375312	61bf697b9015	keyed (DEVELOPMENT / C-ATTR-DEV, NON-CONFIRMATORY; CC-378; W1 recompute pending)	06_results.md
1	data/results/c_attr_1113_b3score/res/B3_SUMMARY.json::sets.ov_dev_b.rows.lmcap|tau_pair.m	1	61bf697b9015	keyed (DEVELOPMENT / C-ATTR-DEV, NON-CONFIRMATORY; CC-378; W1 recompute pending)	06_results.md
DETECTED	data/results/c_attr_1113_b3score/res/B3_SUMMARY.json::sets.ov_dev_b.rows.lmcap|tau_pair.label	'DETECTED'	61bf697b9015	label (DEVELOPMENT / C-ATTR-DEV; CC-378; W1 recompute pending)	06_results.md
−0.48	data/results/c_attr_1113_b3score/res/B3_SUMMARY.json::sets.ov_dev_b.rows.lmcap|tau_marg.d	-0.479908	61bf697b9015	keyed (DEVELOPMENT / C-ATTR-DEV, NON-CONFIRMATORY; CC-378; W1 recompute pending)	06_results.md
−1.27	data/results/c_attr_1113_b3score/res/B3_SUMMARY.json::sets.ov_dev_b.rows.lmcap|tau_marg.lo	-1.2730384864864874	61bf697b9015	keyed (DEVELOPMENT / C-ATTR-DEV, NON-CONFIRMATORY; CC-378; W1 recompute pending)	06_results.md
0.28	data/results/c_attr_1113_b3score/res/B3_SUMMARY.json::sets.ov_dev_b.rows.lmcap|tau_marg.hi	0.2763620189189175	61bf697b9015	keyed (DEVELOPMENT / C-ATTR-DEV, NON-CONFIRMATORY; CC-378; W1 recompute pending)	06_results.md
−1.14	data/results/c_attr_1113_b3score/res/B3_SUMMARY.json::sets.ov_dev_b.rows.lmcap|tau_marg.lo90	-1.1402483567567567	61bf697b9015	keyed (DEVELOPMENT / C-ATTR-DEV, NON-CONFIRMATORY; CC-378; W1 recompute pending)	06_results.md
0.17	data/results/c_attr_1113_b3score/res/B3_SUMMARY.json::sets.ov_dev_b.rows.lmcap|tau_marg.hi90	0.1690337999999997	61bf697b9015	keyed (DEVELOPMENT / C-ATTR-DEV, NON-CONFIRMATORY; CC-378; W1 recompute pending)	06_results.md
0.891	data/results/c_attr_1113_b3score/res/B3_SUMMARY.json::sets.ov_dev_b.rows.lmcap|tau_marg.p	0.8910544727636182	61bf697b9015	keyed (DEVELOPMENT / C-ATTR-DEV, NON-CONFIRMATORY; CC-378; W1 recompute pending)	06_results.md
1	data/results/c_attr_1113_b3score/res/B3_SUMMARY.json::sets.ov_dev_b.rows.lmcap|tau_marg.m	1	61bf697b9015	keyed (DEVELOPMENT / C-ATTR-DEV, NON-CONFIRMATORY; CC-378; W1 recompute pending)	06_results.md
NEGLIGIBLE	data/results/c_attr_1113_b3score/res/B3_SUMMARY.json::sets.ov_dev_b.rows.lmcap|tau_marg.label	'NEGLIGIBLE'	61bf697b9015	label (DEVELOPMENT / C-ATTR-DEV; CC-378; W1 recompute pending)	06_results.md
+6.36	data/results/c_attr_1113_b3score/res/B3_SUMMARY.json::sets.ov_dev_b.rows.qwen25vl_7b|tau_sel_img.d	6.356164864864873	61bf697b9015	keyed (DEVELOPMENT / C-ATTR-DEV, NON-CONFIRMATORY; CC-378; W1 recompute pending)	06_results.md
4.30	data/results/c_attr_1113_b3score/res/B3_SUMMARY.json::sets.ov_dev_b.rows.qwen25vl_7b|tau_sel_img.lo	4.298073548648655	61bf697b9015	keyed (DEVELOPMENT / C-ATTR-DEV, NON-CONFIRMATORY; CC-378; W1 recompute pending)	06_results.md
8.46	data/results/c_attr_1113_b3score/res/B3_SUMMARY.json::sets.ov_dev_b.rows.qwen25vl_7b|tau_sel_img.hi	8.455595308108105	61bf697b9015	keyed (DEVELOPMENT / C-ATTR-DEV, NON-CONFIRMATORY; CC-378; W1 recompute pending)	06_results.md
at its floor (1/2,001)	data/results/c_attr_1113_b3score/res/B3_SUMMARY.json::sets.ov_dev_b.rows.qwen25vl_7b|tau_sel_img.p	0.0004997501249375312	61bf697b9015	keyed (DEVELOPMENT / C-ATTR-DEV, NON-CONFIRMATORY; CC-378; W1 recompute pending)	06_results.md
1/2,001, its floor	data/results/c_attr_1113_b3score/res/B3_SUMMARY.json::sets.ov_dev_b.rows.qwen25vl_7b|tau_sel_img.p	0.0004997501249375312	61bf697b9015	keyed (DEVELOPMENT / C-ATTR-DEV, NON-CONFIRMATORY; CC-378; W1 recompute pending)	06_results.md
1	data/results/c_attr_1113_b3score/res/B3_SUMMARY.json::sets.ov_dev_b.rows.qwen25vl_7b|tau_sel_img.m	1	61bf697b9015	keyed (DEVELOPMENT / C-ATTR-DEV, NON-CONFIRMATORY; CC-378; W1 recompute pending)	06_results.md
DETECTED	data/results/c_attr_1113_b3score/res/B3_SUMMARY.json::sets.ov_dev_b.rows.qwen25vl_7b|tau_sel_img.label	'DETECTED'	61bf697b9015	label (DEVELOPMENT / C-ATTR-DEV; CC-378; W1 recompute pending)	06_results.md
500	data/results/c_attr_1113_b3score/res/B3_SUMMARY.json::sets.xm_dev500.n	500	61bf697b9015	keyed (DEVELOPMENT / C-ATTR-DEV, NON-CONFIRMATORY; CC-378; W1 recompute pending)	06_results.md
+16.58	data/results/c_attr_1113_b3score/res/B3_SUMMARY.json::sets.xm_dev500.rows.lmcap|tau_sel.d	16.577268000000004	61bf697b9015	keyed (DEVELOPMENT / C-ATTR-DEV, NON-CONFIRMATORY; CC-378; W1 recompute pending)	06_results.md
13.91	data/results/c_attr_1113_b3score/res/B3_SUMMARY.json::sets.xm_dev500.rows.lmcap|tau_sel.lo	13.90551453	61bf697b9015	keyed (DEVELOPMENT / C-ATTR-DEV, NON-CONFIRMATORY; CC-378; W1 recompute pending)	06_results.md
19.19	data/results/c_attr_1113_b3score/res/B3_SUMMARY.json::sets.xm_dev500.rows.lmcap|tau_sel.hi	19.185015064999998	61bf697b9015	keyed (DEVELOPMENT / C-ATTR-DEV, NON-CONFIRMATORY; CC-378; W1 recompute pending)	06_results.md
at its floor (1/2,001)	data/results/c_attr_1113_b3score/res/B3_SUMMARY.json::sets.xm_dev500.rows.lmcap|tau_sel.p	0.0004997501249375312	61bf697b9015	keyed (DEVELOPMENT / C-ATTR-DEV, NON-CONFIRMATORY; CC-378; W1 recompute pending)	06_results.md
1	data/results/c_attr_1113_b3score/res/B3_SUMMARY.json::sets.xm_dev500.rows.lmcap|tau_sel.m	1	61bf697b9015	keyed (DEVELOPMENT / C-ATTR-DEV, NON-CONFIRMATORY; CC-378; W1 recompute pending)	06_results.md
DETECTED	data/results/c_attr_1113_b3score/res/B3_SUMMARY.json::sets.xm_dev500.rows.lmcap|tau_sel.label	'DETECTED'	61bf697b9015	label (DEVELOPMENT / C-ATTR-DEV; CC-378; W1 recompute pending)	06_results.md
+17.02	data/results/c_attr_1113_b3score/res/B3_SUMMARY.json::sets.xm_dev500.rows.lmcap|tau_pair.d	17.0192282	61bf697b9015	keyed (DEVELOPMENT / C-ATTR-DEV, NON-CONFIRMATORY; CC-378; W1 recompute pending)	06_results.md
14.43	data/results/c_attr_1113_b3score/res/B3_SUMMARY.json::sets.xm_dev500.rows.lmcap|tau_pair.lo	14.425659025	61bf697b9015	keyed (DEVELOPMENT / C-ATTR-DEV, NON-CONFIRMATORY; CC-378; W1 recompute pending)	06_results.md
19.42	data/results/c_attr_1113_b3score/res/B3_SUMMARY.json::sets.xm_dev500.rows.lmcap|tau_pair.hi	19.41988629	61bf697b9015	keyed (DEVELOPMENT / C-ATTR-DEV, NON-CONFIRMATORY; CC-378; W1 recompute pending)	06_results.md
at its floor (1/2,001)	data/results/c_attr_1113_b3score/res/B3_SUMMARY.json::sets.xm_dev500.rows.lmcap|tau_pair.p	0.0004997501249375312	61bf697b9015	keyed (DEVELOPMENT / C-ATTR-DEV, NON-CONFIRMATORY; CC-378; W1 recompute pending)	06_results.md
1	data/results/c_attr_1113_b3score/res/B3_SUMMARY.json::sets.xm_dev500.rows.lmcap|tau_pair.m	1	61bf697b9015	keyed (DEVELOPMENT / C-ATTR-DEV, NON-CONFIRMATORY; CC-378; W1 recompute pending)	06_results.md
DETECTED	data/results/c_attr_1113_b3score/res/B3_SUMMARY.json::sets.xm_dev500.rows.lmcap|tau_pair.label	'DETECTED'	61bf697b9015	label (DEVELOPMENT / C-ATTR-DEV; CC-378; W1 recompute pending)	06_results.md
−0.44	data/results/c_attr_1113_b3score/res/B3_SUMMARY.json::sets.xm_dev500.rows.lmcap|tau_marg.d	-0.4419601999999996	61bf697b9015	keyed (DEVELOPMENT / C-ATTR-DEV, NON-CONFIRMATORY; CC-378; W1 recompute pending)	06_results.md
−1.50	data/results/c_attr_1113_b3score/res/B3_SUMMARY.json::sets.xm_dev500.rows.lmcap|tau_marg.lo	-1.4987333349999996	61bf697b9015	keyed (DEVELOPMENT / C-ATTR-DEV, NON-CONFIRMATORY; CC-378; W1 recompute pending)	06_results.md
0.49	data/results/c_attr_1113_b3score/res/B3_SUMMARY.json::sets.xm_dev500.rows.lmcap|tau_marg.hi	0.48560778500000074	61bf697b9015	keyed (DEVELOPMENT / C-ATTR-DEV, NON-CONFIRMATORY; CC-378; W1 recompute pending)	06_results.md
−1.31	data/results/c_attr_1113_b3score/res/B3_SUMMARY.json::sets.xm_dev500.rows.lmcap|tau_marg.lo90	-1.3108209	61bf697b9015	keyed (DEVELOPMENT / C-ATTR-DEV, NON-CONFIRMATORY; CC-378; W1 recompute pending)	06_results.md
0.38	data/results/c_attr_1113_b3score/res/B3_SUMMARY.json::sets.xm_dev500.rows.lmcap|tau_marg.hi90	0.37888855999999904	61bf697b9015	keyed (DEVELOPMENT / C-ATTR-DEV, NON-CONFIRMATORY; CC-378; W1 recompute pending)	06_results.md
0.810	data/results/c_attr_1113_b3score/res/B3_SUMMARY.json::sets.xm_dev500.rows.lmcap|tau_marg.p	0.8095952023988006	61bf697b9015	keyed (DEVELOPMENT / C-ATTR-DEV, NON-CONFIRMATORY; CC-378; W1 recompute pending)	06_results.md
1	data/results/c_attr_1113_b3score/res/B3_SUMMARY.json::sets.xm_dev500.rows.lmcap|tau_marg.m	1	61bf697b9015	keyed (DEVELOPMENT / C-ATTR-DEV, NON-CONFIRMATORY; CC-378; W1 recompute pending)	06_results.md
NEGLIGIBLE	data/results/c_attr_1113_b3score/res/B3_SUMMARY.json::sets.xm_dev500.rows.lmcap|tau_marg.label	'NEGLIGIBLE'	61bf697b9015	label (DEVELOPMENT / C-ATTR-DEV; CC-378; W1 recompute pending)	06_results.md
+2.27	data/results/c_attr_1113_b3score/res/B3_SUMMARY.json::sets.xm_dev500.rows.qwen25vl_7b|tau_sel_img.d	2.2654017999999994	61bf697b9015	keyed (DEVELOPMENT / C-ATTR-DEV, NON-CONFIRMATORY; CC-378; W1 recompute pending)	06_results.md
−1.19	data/results/c_attr_1113_b3score/res/B3_SUMMARY.json::sets.xm_dev500.rows.qwen25vl_7b|tau_sel_img.lo	-1.191809400000005	61bf697b9015	keyed (DEVELOPMENT / C-ATTR-DEV, NON-CONFIRMATORY; CC-378; W1 recompute pending)	06_results.md
5.92	data/results/c_attr_1113_b3score/res/B3_SUMMARY.json::sets.xm_dev500.rows.qwen25vl_7b|tau_sel_img.hi	5.916796775000008	61bf697b9015	keyed (DEVELOPMENT / C-ATTR-DEV, NON-CONFIRMATORY; CC-378; W1 recompute pending)	06_results.md
0.101	data/results/c_attr_1113_b3score/res/B3_SUMMARY.json::sets.xm_dev500.rows.qwen25vl_7b|tau_sel_img.p	0.10094952523738131	61bf697b9015	keyed (DEVELOPMENT / C-ATTR-DEV, NON-CONFIRMATORY; CC-378; W1 recompute pending)	06_results.md
1	data/results/c_attr_1113_b3score/res/B3_SUMMARY.json::sets.xm_dev500.rows.qwen25vl_7b|tau_sel_img.m	1	61bf697b9015	keyed (DEVELOPMENT / C-ATTR-DEV, NON-CONFIRMATORY; CC-378; W1 recompute pending)	06_results.md
UNRESOLVED	data/results/c_attr_1113_b3score/res/B3_SUMMARY.json::sets.xm_dev500.rows.qwen25vl_7b|tau_sel_img.label	'UNRESOLVED'	61bf697b9015	label (DEVELOPMENT / C-ATTR-DEV; CC-378; W1 recompute pending)	06_results.md
DETECTED	data/results/c_attr_1113_b3score/res/K5.json::verdict	'DETECTED'	bd9b0158e9d2	label (DEVELOPMENT / C-ATTR-DEV; CC-378; W1 recompute pending)	06_results.md
8.5	data/results/c_attr_1113_b3score/res/B3_SUMMARY.json::sets.ov_dev_b.rows.lmcap|tau_sel.d / sesoi (2.0)	8.46137972972973	61bf697b9015	derived (d / SESOI; CC-378 ruling 5(i))	06_results.md
+8.27	data/results/c_attr_1112_score/res/VERDICT.json::sets.ov_dev_b.rows.qwen25vl_7b|tau_sel.d	8.266461513513512	a69a0ec2b758	keyed (DEVELOPMENT / C-ATTR-DEV, NON-CONFIRMATORY; CC-363; beside row, CC-378 R4/R8)	06_results.md
6.54	data/results/c_attr_1112_score/res/VERDICT.json::sets.ov_dev_b.rows.qwen25vl_7b|tau_sel.lo	6.5360347648648585	a69a0ec2b758	keyed (DEVELOPMENT / C-ATTR-DEV, NON-CONFIRMATORY; CC-363; beside row, CC-378 R4/R8)	06_results.md
10.11	data/results/c_attr_1112_score/res/VERDICT.json::sets.ov_dev_b.rows.qwen25vl_7b|tau_sel.hi	10.108259738738747	a69a0ec2b758	keyed (DEVELOPMENT / C-ATTR-DEV, NON-CONFIRMATORY; CC-363; beside row, CC-378 R4/R8)	06_results.md
DETECTED	data/results/c_attr_1112_score/res/VERDICT.json::sets.ov_dev_b.rows.qwen25vl_7b|tau_sel.label	'DETECTED'	a69a0ec2b758	keyed (DEVELOPMENT / C-ATTR-DEV, NON-CONFIRMATORY; CC-363; beside row, CC-378 R4/R8)	06_results.md
+1.79	data/results/c_attr_1112_score/res/SUMMARY.json::sets.xm_dev500.rows.qwen25vl_7b|tau_sel.d	1.7910556666666722	1d78cd205ff8	keyed (DEVELOPMENT / C-ATTR-DEV, NON-CONFIRMATORY; CC-363; beside row, CC-378 R4/R8)	06_results.md
−1.30	data/results/c_attr_1112_score/res/SUMMARY.json::sets.xm_dev500.rows.qwen25vl_7b|tau_sel.lo	-1.2996083983333373	1d78cd205ff8	keyed (DEVELOPMENT / C-ATTR-DEV, NON-CONFIRMATORY; CC-363; beside row, CC-378 R4/R8)	06_results.md
4.95	data/results/c_attr_1112_score/res/SUMMARY.json::sets.xm_dev500.rows.qwen25vl_7b|tau_sel.hi	4.948772919999983	1d78cd205ff8	keyed (DEVELOPMENT / C-ATTR-DEV, NON-CONFIRMATORY; CC-363; beside row, CC-378 R4/R8)	06_results.md
UNRESOLVED	data/results/c_attr_1112_score/res/SUMMARY.json::sets.xm_dev500.rows.qwen25vl_7b|tau_sel.label	'UNRESOLVED'	1d78cd205ff8	keyed (DEVELOPMENT / C-ATTR-DEV, NON-CONFIRMATORY; CC-363; beside row, CC-378 R4/R8)	06_results.md
DETECTED	data/results/c_attr_1112_score/res/VERDICT.json::sets.ov_dev_b.rows.aya_vision_8b|tau_sel.label	'DETECTED'	a69a0ec2b758	label (CC-363; shell C1 only)	06_results.md
5.51	data/results/c_attr_1113_b3score/decode/CAP_3.json::cap_h	5.513546938747167	542bb950bda2	fact (DEVELOPMENT / C-ATTR-DEV; CC-378)	06_results.md,11_supplement_registered_rows.md
19,848	data/results/c_attr_1113_b3score/decode/CAP_3.json::cap_s	19848	542bb950bda2	fact (DEVELOPMENT / C-ATTR-DEV; CC-378)	11_supplement_registered_rows.md
3.68	data/results/c_attr_1113_b3score/decode/CAP_3.json::P_h	3.6756979591647783	542bb950bda2	fact (DEVELOPMENT / C-ATTR-DEV; CC-378)	11_supplement_registered_rows.md
ten	data/results/c_attr_1113_b3score/decode/CAP_3.json::steps (length)	10	542bb950bda2	fact (DEVELOPMENT / C-ATTR-DEV; CC-378)	05_preregistration_and_analysis.md,06_results.md,11_supplement_registered_rows.md
no step NOT RUN	data/results/c_attr_1113_b3score/decode/CAP_3.json::not_run	[]	542bb950bda2	fact (DEVELOPMENT / C-ATTR-DEV; CC-378)	06_results.md
925	data/results/c_attr_1113_b3score/decode/CAP_3.json::steps[0].n (B3_lmcap_ov_dev_b_ri)	925	542bb950bda2	fact (DEVELOPMENT / C-ATTR-DEV; CC-378)	11_supplement_registered_rows.md
925	data/results/c_attr_1113_b3score/decode/CAP_3.json::steps[1].n (B3_lmcap_ov_dev_b_rand)	925	542bb950bda2	fact (DEVELOPMENT / C-ATTR-DEV; CC-378)	11_supplement_registered_rows.md
925	data/results/c_attr_1113_b3score/decode/CAP_3.json::steps[2].n (B3_lmcap_ov_dev_b_perm)	925	542bb950bda2	fact (DEVELOPMENT / C-ATTR-DEV; CC-378)	11_supplement_registered_rows.md
500	data/results/c_attr_1113_b3score/decode/CAP_3.json::steps[3].n (B3_lmcap_xm_dev500_ri)	500	542bb950bda2	fact (DEVELOPMENT / C-ATTR-DEV; CC-378)	11_supplement_registered_rows.md
500	data/results/c_attr_1113_b3score/decode/CAP_3.json::steps[4].n (B3_lmcap_xm_dev500_rand)	500	542bb950bda2	fact (DEVELOPMENT / C-ATTR-DEV; CC-378)	11_supplement_registered_rows.md
500	data/results/c_attr_1113_b3score/decode/CAP_3.json::steps[5].n (B3_lmcap_xm_dev500_perm)	500	542bb950bda2	fact (DEVELOPMENT / C-ATTR-DEV; CC-378)	11_supplement_registered_rows.md
925	data/results/c_attr_1113_b3score/decode/CAP_3.json::steps[6].n (B3_qwen25vl_7b_ov_dev_b_ret_img)	925	542bb950bda2	fact (DEVELOPMENT / C-ATTR-DEV; CC-378)	11_supplement_registered_rows.md
925	data/results/c_attr_1113_b3score/decode/CAP_3.json::steps[7].n (B3_qwen25vl_7b_ov_dev_b_rand_img)	925	542bb950bda2	fact (DEVELOPMENT / C-ATTR-DEV; CC-378)	11_supplement_registered_rows.md
500	data/results/c_attr_1113_b3score/decode/CAP_3.json::steps[8].n (B3_qwen25vl_7b_xm_dev500_ret_img)	500	542bb950bda2	fact (DEVELOPMENT / C-ATTR-DEV; CC-378)	11_supplement_registered_rows.md
500	data/results/c_attr_1113_b3score/decode/CAP_3.json::steps[9].n (B3_qwen25vl_7b_xm_dev500_rand_img)	500	542bb950bda2	fact (DEVELOPMENT / C-ATTR-DEV; CC-378)	11_supplement_registered_rows.md
0.94	data/results/c_attr_1113_b3score/decode/CAP_3.json::rates_L_r.lmcap[1] (decode s per caption)	0.9397109079360962	542bb950bda2	fact (DEVELOPMENT / C-ATTR-DEV; CC-378)	11_supplement_registered_rows.md
24.5	data/results/c_attr_1113_b3score/decode/CAP_3.json::rates_L_r.lmcap[0] (load s)	24.54790949821472	542bb950bda2	fact (DEVELOPMENT / C-ATTR-DEV; CC-378)	11_supplement_registered_rows.md
3.18	data/results/c_attr_1113_b3score/decode/CAP_3.json::rates_L_r.qwen25vl_7b[1] (decode s per caption)	3.175675797462463	542bb950bda2	fact (DEVELOPMENT / C-ATTR-DEV; CC-378)	11_supplement_registered_rows.md
4.3	data/results/c_attr_1113_b3score/decode/CAP_3.json::rates_L_r.qwen25vl_7b[0] (load s)	4.321260452270508	542bb950bda2	fact (DEVELOPMENT / C-ATTR-DEV; CC-378)	11_supplement_registered_rows.md
73	data/results/c_attr_1113_b3score/decode/gpu_seconds.tsv::line 2 (D1r_lmcap)	73	400be9464fc3	fact (DEVELOPMENT / C-ATTR-DEV; CC-378)	11_supplement_registered_rows.md
73	data/results/c_attr_1113_b3score/decode/gpu_seconds.tsv::line 4 (D1_lmcap)	73	400be9464fc3	fact (DEVELOPMENT / C-ATTR-DEV; CC-378)	11_supplement_registered_rows.md
174	data/results/c_attr_1113_b3score/decode/gpu_seconds.tsv::line 6 (D1r_qwen25vl_7b)	174	400be9464fc3	fact (DEVELOPMENT / C-ATTR-DEV; CC-378)	11_supplement_registered_rows.md
172	data/results/c_attr_1113_b3score/decode/gpu_seconds.tsv::line 8 (D1_qwen25vl_7b)	172	400be9464fc3	fact (DEVELOPMENT / C-ATTR-DEV; CC-378)	11_supplement_registered_rows.md
896	data/results/c_attr_1113_b3score/decode/gpu_seconds.tsv::line 10 (B3_lmcap_ov_dev_b_ri)	896	400be9464fc3	fact (DEVELOPMENT / C-ATTR-DEV; CC-378)	11_supplement_registered_rows.md
894	data/results/c_attr_1113_b3score/decode/gpu_seconds.tsv::line 12 (B3_lmcap_ov_dev_b_rand)	894	400be9464fc3	fact (DEVELOPMENT / C-ATTR-DEV; CC-378)	11_supplement_registered_rows.md
913	data/results/c_attr_1113_b3score/decode/gpu_seconds.tsv::line 14 (B3_lmcap_ov_dev_b_perm)	913	400be9464fc3	fact (DEVELOPMENT / C-ATTR-DEV; CC-378)	11_supplement_registered_rows.md
410	data/results/c_attr_1113_b3score/decode/gpu_seconds.tsv::line 16 (B3_lmcap_xm_dev500_ri)	410	400be9464fc3	fact (DEVELOPMENT / C-ATTR-DEV; CC-378)	11_supplement_registered_rows.md
431	data/results/c_attr_1113_b3score/decode/gpu_seconds.tsv::line 18 (B3_lmcap_xm_dev500_rand)	431	400be9464fc3	fact (DEVELOPMENT / C-ATTR-DEV; CC-378)	11_supplement_registered_rows.md
416	data/results/c_attr_1113_b3score/decode/gpu_seconds.tsv::line 20 (B3_lmcap_xm_dev500_perm)	416	400be9464fc3	fact (DEVELOPMENT / C-ATTR-DEV; CC-378)	11_supplement_registered_rows.md
2,976	data/results/c_attr_1113_b3score/decode/gpu_seconds.tsv::line 22 (B3_qwen25vl_7b_ov_dev_b_ret_img)	2976	400be9464fc3	fact (DEVELOPMENT / C-ATTR-DEV; CC-378)	11_supplement_registered_rows.md
2,842	data/results/c_attr_1113_b3score/decode/gpu_seconds.tsv::line 24 (B3_qwen25vl_7b_ov_dev_b_rand_img)	2842	400be9464fc3	fact (DEVELOPMENT / C-ATTR-DEV; CC-378)	11_supplement_registered_rows.md
1,601	data/results/c_attr_1113_b3score/decode/gpu_seconds.tsv::line 26 (B3_qwen25vl_7b_xm_dev500_ret_img)	1601	400be9464fc3	fact (DEVELOPMENT / C-ATTR-DEV; CC-378)	11_supplement_registered_rows.md
1,447	data/results/c_attr_1113_b3score/decode/gpu_seconds.tsv::line 28 (B3_qwen25vl_7b_xm_dev500_rand_img)	1447	400be9464fc3	fact (DEVELOPMENT / C-ATTR-DEV; CC-378)	11_supplement_registered_rows.md
13,318	data/results/c_attr_1113_b3score/decode/gpu_seconds.tsv::sum of non-start rows	13318	400be9464fc3	fact (DEVELOPMENT / C-ATTR-DEV; CC-378)	11_supplement_registered_rows.md
73	data/results/c_attr_1113_b3score/decode/gpu_seconds_try1.tsv::sum of non-start rows	73	6275b87c8155	fact (DEVELOPMENT / C-ATTR-DEV; CC-378)	03_method.md,11_supplement_registered_rows.md
0.02	data/results/c_attr_1113_b3score/decode/gpu_seconds_try1.tsv::sum of non-start rows / 3600	0.020277777777777777	6275b87c8155	fact (DEVELOPMENT / C-ATTR-DEV; CC-378)	06_results.md
13,391	data/results/c_attr_1113_b3score/decode/gpu_seconds.tsv::sum of non-start rows + gpu_seconds_try1.tsv sum	13391	400be9464fc3	fact (DEVELOPMENT / C-ATTR-DEV; CC-378)	11_supplement_registered_rows.md
3.72	data/results/c_attr_1113_b3score/decode/gpu_seconds.tsv::(sum of non-start rows + gpu_seconds_try1.tsv sum) / 3600	3.7197222222222224	400be9464fc3	fact (DEVELOPMENT / C-ATTR-DEV; CC-378)	06_results.md,11_supplement_registered_rows.md
3.70	data/results/c_attr_1113_b3score/decode/job.log::line "JOB DONE gpu_h"	'3.70'	e6081c58cf3e	fact (DEVELOPMENT / C-ATTR-DEV; CC-378)	11_supplement_registered_rows.md
10	data/results/c_attr_1113_b3score/decode/job.log::lines " OK B3_" (count)	10	e6081c58cf3e	fact (DEVELOPMENT / C-ATTR-DEV; CC-378)	06_results.md
no cap stop, no job stop	data/results/c_attr_1113_b3score/decode/job.log::lines "CAP STOP" or "JOB STOP" (count)	0	e6081c58cf3e	fact (DEVELOPMENT / C-ATTR-DEV; CC-378)	06_results.md
50	data/results/c_attr_1113_b3score/decode/D1_lmcap.json::identical	50	dd9bb57d1f75	fact (DEVELOPMENT / C-ATTR-DEV; CC-378)	03_method.md,11_supplement_registered_rows.md
50	data/results/c_attr_1113_b3score/decode/D1_lmcap.json::n	50	dd9bb57d1f75	fact (DEVELOPMENT / C-ATTR-DEV; CC-378)	03_method.md,11_supplement_registered_rows.md
50	data/results/c_attr_1113_b3score/decode/D1_qwen25vl_7b.json::identical	50	799b0aed5004	fact (DEVELOPMENT / C-ATTR-DEV; CC-378)	03_method.md,11_supplement_registered_rows.md
50	data/results/c_attr_1113_b3score/decode/D1_qwen25vl_7b.json::n	50	799b0aed5004	fact (DEVELOPMENT / C-ATTR-DEV; CC-378)	03_method.md,11_supplement_registered_rows.md
PASS	data/results/c_attr_1113_b3score/res/VERIFY.json::d1.lmcap.D1	'PASS'	28ab8f59780e	fact (DEVELOPMENT / C-ATTR-DEV; CC-378)	11_supplement_registered_rows.md
PASS	data/results/c_attr_1113_b3score/res/VERIFY.json::d1.qwen25vl_7b.D1	'PASS'	28ab8f59780e	fact (DEVELOPMENT / C-ATTR-DEV; CC-378)	11_supplement_registered_rows.md
ok	data/results/c_attr_1113_b3score/res/VERIFY.json::parity_7_1.result	'ok'	28ab8f59780e	fact (DEVELOPMENT / C-ATTR-DEV; CC-378)	06_results.md
e95831b6…	data/results/c_attr_1113_b3score/res/VERIFY.json::env.packages_sha256	'e95831b6f8c56dfe7f66d652420bd5cfc708c0cd2412f84bd4a632863703ee2d'	28ab8f59780e	fact (DEVELOPMENT / C-ATTR-DEV; CC-378)	07_disclosures.md
107 of 107	data/results/c_attr_1113_b3score/s0_hs/mutants.log::line "107/107 killed; survived: none"	'107/107 killed; survived: none'	9203e19671c3	fact (DEVELOPMENT / C-ATTR-DEV; CC-378)	07_disclosures.md
9e292657…	manuscript/prereg/2026-11-11_c_attr_dev/C_ATTR_BLOCK3_RUN_DOC_ERRATUM_1.md::§9 item 4 model.safetensors sha256	'9e2926577049a20960ead82d1ebe5ce04d498f450ca53e5c1fb0993c4fc7d8de'	e3a55b72f687	fact (DEVELOPMENT / C-ATTR-DEV; CC-378)	03_method.md
5	manuscript/prereg/2026-11-11_c_attr_dev/C_ATTR_DEV_PREREG_v1_1.md::§6.5 heading (hard cap 5 GPU-h)	'5'	44f81329d418	registered text (v1.1)	05_preregistration_and_analysis.md
min(12, 1.5 P3)	manuscript/prereg/2026-11-11_c_attr_dev/C_ATTR_DEV_ADDENDUM_v1_2.md::V8 (block 3 cap)	'min(12, 1.5 P3)'	5858d69d7c1f	registered text (addendum v1.2)	05_preregistration_and_analysis.md,11_supplement_registered_rows.md
about 0.49	manuscript/prereg/2026-11-11_c_attr_dev/C_ATTR_DEV_PREREG_v1_1.md::§7.13 OV-dev-B Qwen2.5-VL chance of DETECTED at a true +2.0	'about 0.49'	44f81329d418	registered text (v1.1)	06_results.md
about 1.03	manuscript/prereg/2026-11-11_c_attr_dev/C_ATTR_DEV_PREREG_v1_1.md::§7.13 OV-dev-B Qwen2.5-VL standard error	'about 1.03'	44f81329d418	registered text (v1.1)	06_results.md
about ±0.3	manuscript/prereg/2026-11-11_c_attr_dev/C_ATTR_DEV_PREREG_v1_1.md::§7.13 NEGLIGIBLE needs |θ̂| below about 0.3	'about 0.3'	44f81329d418	registered text (v1.1)	06_results.md
50	manuscript/prereg/2026-11-11_c_attr_dev/C_ATTR_BLOCK3_RUN_DOC_v1_1.md::§2 D1 (first 50 OV-dev-B items per runner)	50	e8ae45a59b08	registered text (run doc v1.1)	03_method.md,11_supplement_registered_rows.md
4	manuscript/prereg/2026-11-11_c_attr_dev/C_ATTR_DEV_PREREG_v1_1.md::§2 lmcap_rand / lmcap_perm (K = 4)	4	44f81329d418	registered text (v1.1)	03_method.md
3	manuscript/prereg/2026-11-11_c_attr_dev/C_ATTR_DEV_PREREG_v1_1.md::§2 lmcap_rand (N = 3 shots)	3	44f81329d418	registered text (v1.1)	03_method.md
```

### 5.1 Placeholder → display (the fill map)

Each placeholder of §3 and §4 takes exactly this display; the manifest row is the one of §5 with the same key. `(table)` and `(sentence)` are the two p̃ forms. Rows marked "(evidence …)" back words, not numbers.

| placeholder | display |
|---|---|
| `{{B3S::sets.ov_dev_b.n}}` | 925 |
| `R1.d` | +16.92 |
| `R1.lo` | 15.00 |
| `R1.hi` | 19.06 |
| `{{R1.p}} (table)` | at its floor (1/2,001) |
| `{{R1.p}} (sentence)` | 1/2,001, its floor |
| `{{R1.m}}` | 1 |
| `{{R1.label}}` | DETECTED |
| `R2.d` | +17.40 |
| `R2.lo` | 15.48 |
| `R2.hi` | 19.41 |
| `{{R2.p}} (table)` | at its floor (1/2,001) |
| `{{R2.p}} (sentence)` | 1/2,001, its floor |
| `{{R2.m}}` | 1 |
| `{{R2.label}}` | DETECTED |
| `R3.d` | −0.48 |
| `R3.lo` | −1.27 |
| `R3.hi` | 0.28 |
| `{{R3.lo90}}` | −1.14 |
| `{{R3.hi90}}` | 0.17 |
| `{{R3.p}} (table)` | 0.891 |
| `{{R3.m}}` | 1 |
| `{{R3.label}}` | NEGLIGIBLE |
| `R4.d` | +6.36 |
| `R4.lo` | 4.30 |
| `R4.hi` | 8.46 |
| `{{R4.p}} (table)` | at its floor (1/2,001) |
| `{{R4.p}} (sentence)` | 1/2,001, its floor |
| `{{R4.m}}` | 1 |
| `{{R4.label}}` | DETECTED |
| `{{B3S::sets.xm_dev500.n}}` | 500 |
| `R5.d` | +16.58 |
| `R5.lo` | 13.91 |
| `R5.hi` | 19.19 |
| `{{R5.p}} (table)` | at its floor (1/2,001) |
| `{{R5.m}}` | 1 |
| `{{R5.label}}` | DETECTED |
| `R6.d` | +17.02 |
| `R6.lo` | 14.43 |
| `R6.hi` | 19.42 |
| `{{R6.p}} (table)` | at its floor (1/2,001) |
| `{{R6.m}}` | 1 |
| `{{R6.label}}` | DETECTED |
| `R7.d` | −0.44 |
| `R7.lo` | −1.50 |
| `R7.hi` | 0.49 |
| `{{R7.lo90}}` | −1.31 |
| `{{R7.hi90}}` | 0.38 |
| `{{R7.p}} (table)` | 0.810 |
| `{{R7.m}}` | 1 |
| `{{R7.label}}` | NEGLIGIBLE |
| `R8.d` | +2.27 |
| `R8.lo` | −1.19 |
| `R8.hi` | 5.92 |
| `{{R8.p}} (table)` | 0.101 |
| `{{R8.m}}` | 1 |
| `{{R8.label}}` | UNRESOLVED |
| `(evidence for 'The positive control was met.')` | DETECTED |
| `{{R1.d/2.0}}` | 8.5 |
| `BOV.d` | +8.27 |
| `BOV.lo` | 6.54 |
| `BOV.hi` | 10.11 |
| `{{BOV.label}}` | DETECTED |
| `BXM.d` | +1.79 |
| `BXM.lo` | −1.30 |
| `BXM.hi` | 4.95 |
| `{{BXM.label}}` | UNRESOLVED |
| `{{VER1B::sets.ov_dev_b.rows.aya_vision_8b~tau_sel.label}}` | DETECTED |
| `{{CAP3::cap_h}}` | 5.51 |
| `{{CAP3::cap_s}}` | 19,848 |
| `{{CAP3::P_h}}` | 3.68 |
| `{{CAP3::steps|count}}` | ten |
| `ten (05 E5, S27)` | ten |
| `(evidence for 'no step NOT RUN')` | no step NOT RUN |
| `{{CAP3::steps[0].n}}` | 925 |
| `{{CAP3::steps[1].n}}` | 925 |
| `{{CAP3::steps[2].n}}` | 925 |
| `{{CAP3::steps[3].n}}` | 500 |
| `{{CAP3::steps[4].n}}` | 500 |
| `{{CAP3::steps[5].n}}` | 500 |
| `{{CAP3::steps[6].n}}` | 925 |
| `{{CAP3::steps[7].n}}` | 925 |
| `{{CAP3::steps[8].n}}` | 500 |
| `{{CAP3::steps[9].n}}` | 500 |
| `{{CAP3::rates_L_r.lmcap[1]}}` | 0.94 |
| `{{CAP3::rates_L_r.lmcap[0]}}` | 24.5 |
| `{{CAP3::rates_L_r.qwen25vl_7b[1]}}` | 3.18 |
| `{{CAP3::rates_L_r.qwen25vl_7b[0]}}` | 4.3 |
| `{{GS3::line 2}}` | 73 |
| `{{GS3::line 4}}` | 73 |
| `{{GS3::line 6}}` | 174 |
| `{{GS3::line 8}}` | 172 |
| `{{GS3::line 10}}` | 896 |
| `{{GS3::line 12}}` | 894 |
| `{{GS3::line 14}}` | 913 |
| `{{GS3::line 16}}` | 410 |
| `{{GS3::line 18}}` | 431 |
| `{{GS3::line 20}}` | 416 |
| `{{GS3::line 22}}` | 2,976 |
| `{{GS3::line 24}}` | 2,842 |
| `{{GS3::line 26}}` | 1,601 |
| `{{GS3::line 28}}` | 1,447 |
| `{{GS3::Σ}}` | 13,318 |
| `{{GS3T1::Σ}}` | 73 |
| `{{GS3T1::Σ/3600}}` | 0.02 |
| `{{GS3+T1::Σ}}` | 13,391 |
| `{{GS3+T1::Σ/3600}}` | 3.72 |
| `{{JOB3::JOB DONE gpu_h}}` | 3.70 |
| `(evidence for 'all ten steps … finished')` | 10 |
| `(evidence for 'no cap stop, no job stop')` | no cap stop, no job stop |
| `{{D1L::identical}}` | 50 |
| `{{D1L::n}}` | 50 |
| `{{D1Q::identical}}` | 50 |
| `{{D1Q::n}}` | 50 |
| `{{VFY3::d1.lmcap.D1}}` | PASS |
| `{{VFY3::d1.qwen25vl_7b.D1}}` | PASS |
| `{{VFY3::parity_7_1.result}}` | ok |
| `{{VFY3::env.packages_sha256|8}}` | e95831b6… |
| `{{MUT3::107 of 107}}` | 107 of 107 |
| `{{ERR3::sha}}` | 9e292657… |
| `{{REG::§6.5 5}}` | 5 |
| `{{ADD::V8}}` | min(12, 1.5 P3) |
| `{{REG::§7.13 about 0.49}}` | about 0.49 |
| `{{REG::§7.13 about 1.03}}` | about 1.03 |
| `{{REG::§7.13 about ±0.3}}` | about ±0.3 |
| `{{RUN3::§2 D1 50}}` | 50 |
| `{{REG::§2 K}}` | 4 |
| `{{REG::§2 N}}` | 3 |

Not given a row (already in the paper with rows, or registered constants of 5.7): B = 2,000; 1/2,001; +2.0; 0.025; 0.92.

---

## 6. Transfer gates (f)

The transfer of block 3 is a script-filled diff of E1–E19 plus the manifest rows, read by one judge before any commit (CC-365 pattern). The diff read must check:

- **G0 (W1, BLOCKING precondition).** A LOG line records the reader's run of `c_attr_b3_ledger_recompute.py` over `led/k5.jsonl`, `led/b3_ov_dev_b.jsonl`, `led/b3_xm_dev500.jsonl` and `res/B3_SUMMARY.json` (pull copy under `.session_backup/machines/H1/root/c_attr_score_b3/`), with the three input sha256 lines, eight PASS lines and `ALL PASS (8 rows)`; or a judge line that waives W1 with its reason. On any FAIL: STOP, no transfer, the matter goes to a judge. The script's `--selftest` output is in the same record.
- **G1 (records).** The run-repo gatekeeper commit of CC-378 ruling 8 exists; `data/results/c_attr_1113_b3score/SHA256SUMS` is `d2500b48…` and `sha256sum -c` is 28/28; B3_SUMMARY `61bf697b`, K5 `bd9b0158`, VERIFY `28ab8f59`, CAP_3 `542bb950`, gpu_seconds `400be946`, gpu_seconds_try1 `6275b87c`, job.log `e6081c58`, D1 files `dd9bb57d`/`799b0aed`, mutants.log `9203e196`.
- **G2 (base).** Paper repo at `44bbdd9` (or, if it moved, every OLD still occurs exactly once and the moved lines are listed). Package sha = the TARGET of its read.
- **G3 (numbers).** Every placeholder filled by script from its key in a file whose sha is G1's; every printed number has a manifest row; rounding to half a unit of the last digit; U+2212; house format; "−0.00" never printed; p̃ formatted as in the Placeholders paragraph.
- **G4 (strings verbatim).** Both E6 strings wherever the arms are named (03 E1, Table 18 caption), unbroken; "batch size 1 (addendum v1.2 V8)"; "all arms decoded on one host in block 3; stored decodes not used"; the W2 wording on R2, R3, R6, R7; "no registered rule (registration §7.8); label printed, no conclusion drawn" on R5–R8; the R8 UNRESOLVED sentence; "The positive control was met."; the ruling-3 sentences in the forms of §2.1.
- **G5 (forbidden).** "test" naming the attribution analysis (TG5 of CC-358 stays); "confirmed", "validated" or "re-validated" in a positive sense about any row; "no effect", "not significant", "exceeds the SESOI"; any difference, ratio, "larger" or "smaller" between an image-format row and a text-example row; any C-T1 number beside a block-3 contrast (CC-368 N4(d), CC-378 ruling 6); "split of a known τ_sel" on a block-3 row; "RAGCap-style"; a pooled, τ_any, masked or copy-bound row for block 3; any sentence that a published system was tested; "no overlap"; any AI statement.
- **G6 (untouched).** `00_abstract.md`, `01_introduction.md`, `10_conclusion.md` byte-unchanged; the contributions do not name the attribution analysis (CC-378 Q1 default; PI-1112e item 3); `tex/` untouched, with the commit message saying the build is stale (CC-365 ruling 8).
- **G7 (shells).** No sentence of shell C1 or C2 in the diff unless its LOG line exists with the stated content; if present, the text is exactly §4's.
- **G8 (hygiene).** No caption text; no host name, IP or port; no machine label of a rented host (the labels the LOG uses) in paper text; no CC, OPS, PI or "C-T1" id; no "kit B"; no Java version string.
- **G9 (past tense).** Each procedure sentence matches its record: 10 `OK B3_` lines and `JOB DONE gpu_h 3.70` with no `CAP STOP`/`JOB STOP` (job.log); `STAGE_b3k5.prev_sha256` = sha(VERIFY.json) and `STAGE_b3rest.prev_sha256` = sha(K5.json); the K5 LOG line stamped before the b3rest start; the reference-file removal line; `107/107 killed; survived: none` and `rc 0` (mutants.log); 3 attempts in gpu_seconds_try1.tsv; the run-doc erratum commit ca24e13 (2026-11-13T00:03:08Z) after `JOB DONE` (2026-11-12T23:27:30Z) and its review CC-370 (2026-11-12T19:37:46Z, LOG) before the relaunch `PREFLIGHT OK` (19:44:24Z); run doc v1.1 and the decode code at 60358b2 (2026-11-12T18:28:19Z) before the first launch (19:13:59Z, gpu_seconds_try1.tsv).
- **G10 (bib).** No new key; `Ramos2023LMCap` and `Bazi2025RAGCap` are present (counted at HEAD).

---

## 7. What is NOT changed (g)

- Title, abstract (`00`), introduction and its contributions list (`01`), conclusion (`10`): byte-unchanged. The contributions do not name the attribution analysis (CC-378 Q1 default "no"; PI-1112e item 3, the CC-363 P-1 default). Ruling 9 of CC-378: block 3 does not by itself change the method novelty; a blind rubric re-score and a verified prior-art check of the random/permuted-example decomposition come first.
- The 6.10 box sentence ("enters neither the abstract nor the contributions") stays.
- No block-1b number, label, sentence or table (Tables 15–17, S20–S26) changes. No sentence says that block 3 confirms, validates or strengthens a block-1b row (CC-378 ruling 5(iii)).
- Table S19 and its "Interleaved examples" note (the earlier-stage interleaved row on OV-dev-B) stay as they are; no block-3 sentence points to that row or its number (CC-378 ruling 6 by analogy for `ret_img`; open point J-B3-3).
- Section 3.7 (LMCap's four deviations) is not edited; E1 points to it.
- Sections 9.2 and 9.3 are not edited. 9.2's "untested for … prompts with example images" refers to the registered test results and stays true.
- No scope sentence, no block-2 or block-4 status, no freeze tense change, until shells C1/C2.
- No AI-use sentence, and no "no AI was used" sentence (PI-1110n: the PI decides at submission).
- The group's FAIR 2026 conference paper is not cited by this package: no sentence needs it.

---

## 8. Open points for the judge (h), each with my recommended reading

- **J-B3-1 (numbering).** Block 3 = 6.10.8; the not-run subsection = 6.10.9 (shell C1), and the two pointers CC-365 N12 ruled with "6.10.8" are restored with "6.10.9". *Recommended:* accept; the alternative (block 3 as 6.10.9 after the not-run text) would put a result after the text that says what did not run, and would leave 6.10.8 empty until 11-14.
- **J-B3-2 (ruled sentences, paper-ready forms).** The ruling-3 and R1/R4 sentences carry CC ids and "C-T1". *Recommended:* the forms of §2.1 (ids removed, "C-T1" → "the exploration runs of the Flickr30K registration", "kit B" → "the scoring kit", house number format). Each removes a code or format only; no claim moves.
- **J-B3-3 (earlier-stage `ret_img` row).** Table S19's note already prints the earlier-stage interleaved-minus-text `ret` row on OV-dev-B (−0.53 [−2.39, 1.32]). A reader can combine it with Table 18 and Table 16. *Recommended:* no pointer from block-3 text to it, no edit to it now; ruling 6 names only `lmcap_ri`, so the judge may extend it to `ret_img` and decide whether S19's note needs a "different decoding host and stage" clause.
- **J-B3-4 (power clause on NEGLIGIBLE).** CC-331 Q5 / CC-358 J9 ask for the power statement wherever NEGLIGIBLE is used; CC-378 R3 gives none, and no planning value exists for LMCap. *Recommended:* the bracketed sentence in E7 (the registered Qwen2.5-VL-7B values, "values are for m = 1", and "no planning value was registered for LMCap"). XM-dev500's NEGLIGIBLE row needs none: it has no rule.
- **J-B3-5 (optional descriptive sentence, ruling 4).** *Recommended:* include. It is labelled a description and "not a check of those claims"; ruling 5(iii) is respected.
- **J-B3-6 (other work on the block-3 machine).** Ruling 3(g) requires no paper sentence. The 1b bullet "Other work on the same machine" disclosed the same kind of deviation for blocks 1 and 1b (v1.1 §6.7: no job beside another). *Recommended:* include the optional sentence of E11, for consistency with the 1b disclosure; it states facts and claims no effect either way.
- **J-B3-7 (run-document departures (ii) and (iii)).** CC-368's departures (ii), D1 per runner on its own block-3 arm, and (iii), P3 and the cap over all ten steps, are not in ruling 3. *Recommended:* state both, as E1 ("in place of the `ret` items named in the addendum") and E5 ("P3 was computed over all ten steps") do; both are registered-text facts, not new claims.
- **J-B3-8 (block-4 text and LMCap).** The 1b B4 sentence does not name LMCap's English arms (step 4.4). *Recommended:* keep the ruled 1b text under C2; adding "and LMCap's" is a judge's choice.
- **J-B3-9 (release scope, E14).** PI-1112e item 3: "registrations and code only, not the rulings". The supplement still promises "the rulings that read them". *Recommended:* E14 drops the rulings and keeps the run documents (CC-365 P-5's reading: run documents are registered texts). If the PI reads "registrations" strictly, cut "and the run documents" too.
- **J-B3-10 (where W1 runs).** See the build note: the PI's rule puts scoring-type computation on a rented host (PI-1111j, and the PI's 2026-11-11 rule that self-tests, mutants and CPU scoring run on the rented machine), and no host exists now; the recompute is a 2,000 × n integer bootstrap on two sets, seconds of CPU. *Recommended:* a named one-off on the laptop under a judge line (the ledgers already sit there as 0444 pull copies; nothing new is copied), because the transfer waits on it and the next host has no date. Default if the judge prefers the rule as written: the first step on the next rented host.
- **J-B3-11 (recompute script output).** The script prints, besides the eight "row, max|diff|, PASS/FAIL" lines and the final line, the sha256 of each input and the numpy version. These carry no ledger value. *Recommended:* keep them; they bind the PASS to the bytes and expose a numpy-stream mismatch. Strike them if the brief's "only" is read strictly (two `print` lines).
- **J-B3-12 (supplement header).** E13 makes the header name Table 18 as the block-3 rows and Table S27 as the decode record, and states the block-3 batch label, which differs from the 1b label. *Recommended:* accept.

## Conflicts between CC-378 and the standing 1b guards (for the record)

1. Internal codes in verbatim ruling-3, R1 and R4 sentences (CC ids, "C-T1", "kit B") against CC-358 TG9 and PI-1112e item 3 (rulings not released) — J-B3-2.
2. CC-378's number format "[+15.00, +19.06]" against the house format ruled correct in CC-365 ruling 2 — house format used.
3. W2 fixed wording against the JSON `tier` string ("the sum was not known") — W2 wording used as fixed text, never filled from `tier` (CC-378 W2 itself).
4. R3/R7 carry no power statement against CC-358 J9 — J-B3-4.
5. The 1b B2 sentence "or before the freeze" is premature before the K7 line (CC-365 B1, N13) — split into pre-K7 and post-K7 forms in shell C1.
6. Ruling 3(g) "no paper sentence required" against the 1b 7.5 practice of disclosing other work on the same machine — J-B3-6.
7. The supplement header still promises release of "the rulings that read them", against PI-1112e item 3 — E14 (a standing defect of the paper, not of CC-378).
8. CC-365 N12 ruled the restored pointer as "Section 6.10.8"; block 3 now takes 6.10.8 — J-B3-1.
