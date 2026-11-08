# B-PA1-T1 GPU code: numbered readings and the CC-295 / CC-295r2 / CC-295r3 hunk maps

Status: **DRAFT for a round-4 full read limited to W6 and W9 (CC-295r3 ESCALATE_TO_PI; needs a PI line); not registered.**
- Each reading is a choice that the registered sources leave open, or a ruling on one. The open readings carry a
  short "why" in the section after the table (CC-295r2 Ruling 2).
- Code lines are `file:line` in `scripts/b_pa1/` at the shas of `SHA256SUMS_GPU`.
- Sources: v3.1 = `PREREG_DRAFT_v3_1.md` e9b30ca7; R5 = `AMENDMENT_R5_DRAFT_v1_2.md` 9cb21917; R6 = `AMENDMENT_R6_DRAFT_v4.md` 0b55d5f8; R6-II = `AMENDMENT_R6_PART2_CAP_DRAFT_v4.md` 0c5f919b; RD = `B_RUN_DOC_v1.md` 4067c9ef.
- This file is a document, not code. It is not in `SHA256SUMS_GPU`.

## Readings

| # | reading (default) | code | source | status |
|---|---|---|---|---|
| 1 | The host never reads `b_pa1_lists.json`. Slice A = the frame rows whose file is in the slice-A MANIFEST (sha = AMAN, on an OPS line), in frame order. The gate set = its first 231. The lists file is made by the committed `slices pick` and is read only on the laptop (`htrans`) | `b_pa1_gpu.py:370`, `b_pa1_gpu.py:712` | v3.1 l.252-254 (slice order), l.216 (gate set); RD §9.4 (AMAN from the lists) | ACCEPTED, CC-295r3 Ruling 6 |
| 2 | The GPU code lives in new sibling files with their own `SHA256SUMS_GPU`; `b_pa1.py` is not edited. The job checks both SUMS | `b_pa1_job.sh:67` | v3.1 l.12; CC-226r3 (b_pa1.py c481fcf4) | ACCEPTED, CC-295 Ruling 1 |
| 3 | Two GPU venvs: main (transformers 4.53.3) and legacy (4.45.2, for InternVL2_5-2B, Phi-3.5-vision, Molmo-7B-O). The registry gives each model its venv | `b_pa1_job.sh:150`; registry `models.*.venv`; lock headers | CPU probe 2026-11-08 (lock header); C CC-280 AM1 | ACCEPTED, Ruling 2 |
| 4 | Freeze check: the first host build writes `freeze_<venv>.sha256` and each job start compares against it. The R2 LOG pin is checked on the laptop. Only the W venv is checked against a constant (1a639a50) | `b_pa1_setup_host.sh:38`, `b_pa1_job.sh:75` | v3.1 l.653-655 (R2); RD §1.1 | ACCEPTED, CC-295r3 Ruling 6 |
| 5 | Eager download of every Rule-S-passing pin at setup (141.1 GB pinned). One combined check (ungated + gated, models not yet fetched) at the first fetch: setup refuses if bytes × 1.1 > free disk. pip runs with no wheel cache | `b_pa1_setup_host.sh:64`, `b_pa1_setup_host.sh:73`, `b_pa1_setup_host.sh:25` | RD RB6 / D-9 (lazy) struck; CC-295r2 Ruling 15 | ACCEPTED, Ruling 3 (+ N11, N-d) |
| 6 | The verifier answers all six proposition types; the laptop scorer keeps the object type for B's score | `b_pa1_gpu.py:622`; registry `verify_types` | v3.1 l.96-98, §7.1, §9.1 (p·r_v) | ACCEPTED, Ruling 4 |
| 7 | Decomposer: English instruction, Vietnamese propositions copied from the caption, JSON {type, text, object}, 512 new tokens, batch 8 left-padded greedy. Each parse is marked ok, partial or fail | `b_pa1_gpu.py:253`, `b_pa1_models.py:268`; registry `prompts.d1`, `decomposer_decode` | v3.1 §7.1, §7.2 (d1, d2) | ACCEPTED, CC-295r3 Ruling 6 |
| 8 | Smoke set: the gate captions of the 4 accepted captioners on the first 64 slice-A images, image i to captioner i mod 4. Every timing stays in memory; only `rates_smoke.json` is written | `b_pa1_gpu.py:740`, `b_pa1_gpu.py:662` | v3.1 §9.1 row S | ACCEPTED, CC-295r3 Ruling 6 |
| 9 | A4 decode rate: 16 images per A4 model, captions in memory only | `b_pa1_gpu.py:727` | v3.1 §9.1 (A4 row, trim order) | ACCEPTED, CC-295r3 Ruling 6 |
| 10 | Gate decodes are not reused. A1-decode decodes all 2,000 images, the first 231 included. Block H takes its captions from the A1-decode files of the 231 gate ids (`htrans`), never from the gate files (N-g) | `b_pa1_gpu.py:779`, `b_pa1_mid.py:395` | v3.1 §6.4 step 3 | ACCEPTED, CC-295r3 Ruling 6 |
| 11 | Pure greedy for every captioner (num_beams 1, repetition_penalty 1.0, sampling fields cleared). HOSTCHECK records the effective settings | `b_pa1_models.py:56`, `b_pa1_models.py:76`, `b_pa1_models.py:209` | v3.1 §4.4 | ACCEPTED, Ruling 5 (+ N6) |
| 12 | mBLIP has no chat template; it gets the plain instruction, as on its card | `b_pa1_models.py:147` | v3.1 §4.4 "own chat template" | ACCEPTED, CC-295r3 Ruling 6 |
| 13 | Card preprocessing values: InternVL dynamic 448 tiles max 12 + thumbnail; Phi-3.5 num_crops 16 (single frame); Molmo in bf16 (fp32 does not fit 24 GB); processors at their defaults | `b_pa1_models.py:172`, `b_pa1_models.py:224`; registry `molmo_7b_o.dtype` | model cards | ACCEPTED, CC-295r3 Ruling 6 |
| 14 | The six H2 transforms are defined in `transform` (punct toggle, NFC/NFD toggle, oa/oe/uy tone flip, R7 segmentation with `_`, case toggle, double spaces). They run on the laptop (`htrans`) and are pushed as `in/h_input.jsonl`, whose sha is EXTRA. The salt uses the registry key and the frame file name; the tier-2 prereg copies this pick form verbatim, with the registry key as the captioner id (N-h) | `b_pa1_mid.py:366`, `b_pa1_mid.py:383`, `b_pa1_gpu.py:805` | v3.1 §8.4 (l.448-461) | ACCEPTED, CC-295r3 Ruling 6 |
| 15 | Coverage: covered = exact match after NFC, lower case, `_` → space and rescap `norm_tone`, against a map term or an R7 stop word. Letterless tokens are ignored. DF counts distinct captions over the 8,000. Amended terms are appended after the map v1 terms, so existing matches never change | `b_pa1_mid.py:59`, `b_pa1_mid.py:140`, `b_pa1_mid.py:261` | v3.1 §6.1 (l.336-342) | ACCEPTED, CC-295r3 Ruling 6 |
| 16 | An (ii) entry may not reuse an existing term (a second class on a term would edit an existing entry) | `b_pa1_mid.py:229` | v3.1 §6.1 add-only | ACCEPTED, CC-295r3 Ruling 6 |
| 17 | parity2 gate: the map v1 parity1-done line; a mapfinal pin carrying the final sha, `b_pa1_map_final.json`, the crosswalk sha, the map v1 sha and the amendments-log sha; exactly one later `OPS-<id>-parity2-start:` line carrying the final, crosswalk, refs, gold and EX shas and the run dir; no parity2-done line | `b_pa1_mid.py:286` | v3.1 §6.3 run 2, §6.4 step 5 | ACCEPTED, CC-295r3 Ruling 6 |
| 18 | Instrument entries are **agent-drafted, amendment-logged**, with no model id. Each instrument entry names its drafter. The entries file names a LOG-pinned amendment, and the registry mode must match. Every entries file (dictionary or instrument) must itself be on a LOG pin line with its name and sha (W7). Registry `prompts.instrument_i` / `instrument_ii` name no drafting rule; they point by name to that amendment (W8) | `b_pa1_mid.py:198`, `b_pa1_mid.py:181`, `b_pa1_mid.py:246`; registry `instrument_llm`, `prompts.instrument_i`, `prompts.instrument_ii` | v3.1 l.328-329; PI-1108e Q2 (a) | **decided by PI-1108e**; the step-4 amendment (D8 draft, another agent) needs its own irreversible-tier read |
| 19 | Captioner prompt = `scripts/evaluate.py` `PROMPTS["short"]`, the short mode behind the 0.8409 s rate | registry `prompts.captioner` | B direction §3.7; MT4 DEV_RULE (a) | ACCEPTED, CC-295r3 Ruling 6 |
| 20 | Money stop: the coordinator writes MONEY_STOP.json (`money-stop`), then stops the job through `~/b_pa1_out/job.pid` (kp). TERM reaches the running step at once (W1); the trap waits for the step to end (N-b); a TERM with the marker present is the final money stop, with its manifest (N-a); a marker written mid-mode stops the job at the next step (N3). The run doc's money path is one TERM by job.pid, never a kill-session; a kill-session is still survived (W9). Panel reads are hourly once within 6 h × Σ r_live of the threshold (N13) | `b_pa1_gpu.py:918`, `b_pa1_gpu.py:444`, `b_pa1_job.sh:52`, `b_pa1_job.sh:41` | R6 §I.3 rule 4; RD RB9 | W1 FIXED; cadence = run doc v1.1 |
| 21 | Ledger: GPU-h = the sum of step wall seconds. The trap closes a killed step; after machine loss `resume --close-sec` closes an open step. **HB-T1′ form (N9, one form only):** setup on a fresh `~/b_pa1_out`, then `cap-init --used-sec S` (S = HB-T1's used GPU-s from the pulled ledger), then restore `out/`, `logs/`, `RUN.*` and `done.*` from the pull, and `RESUME.json` and `RESUME_USED` when present, then `resume --cause machine`. If either of those two files exists, HB-T1′ takes no resume and the PI decides (v3.1 l.519-520). S counts an open step up to the loss time, from the same pull-loop evidence as `--close-sec`. CAP.json, the ledger and the freeze files are never copied (N-i) | `b_pa1_gpu.py:428`, `b_pa1_gpu.py:900`, `b_pa1_gpu.py:871` | R6-II §2 step 5; v3.1 l.519-520 | ACCEPTED (code), CC-295r3 Ruling 6; run-doc conditions N-i |
| 22 | One resume in total: `RESUME.json` (exclusive create) plus a `RESUME_USED` marker; on HB-T1′ under reading 21's restore condition (N-i) | `b_pa1_job.sh:129` | v3.1 l.519-520 | ACCEPTED, CC-295r3 Ruling 6 |
| 23 | Trim projection formulas; the cap left is measured inside `s.trim`; TRIM.json is decided once and kept on a rerun | `b_pa1_gpu.py:473`, `b_pa1_gpu.py:756` | v3.1 l.510-511; R5 E-12; R6 §I.6; R6-II §3 | logic CORRECT, Ruling 9 |
| 24 | Core does not fit → CORE_STOP.json (written by `s.trim`, and by the job if absent). Every later step and mode refuses. a1decode needs RUN.s.done and TRIM core_fits true; a1score needs RUN.a1decode.done; rest needs RUN.a1score.done | `b_pa1_gpu.py:43`, `b_pa1_gpu.py:507`, `b_pa1_job.sh:108`, `b_pa1_job.sh:162` | v3.1 l.506 as R5 E-12 | semantics ACCEPTED (Ruling 7); W3 FIXED |
| 25 | `b_pa1_dev_contacts.json` (v3.1 §3) is not written by this code; it is an after-run laptop step | — | v3.1 l.143-147 | ACCEPTED, CC-295r3 Ruling 6 |
| 26 | Gemma-3n V = **MobileNet-V5**, under `ERRATUM_LINEAGE_GEMMA3N_v1_2.md`, a substantive pre-data amendment of N6: card, then report or paper, then the developer's official model documentation; a documented new encoder with no stated initialisation from another series is its own V line; O4's "undetermined = clash" is overridden for Gemma-3n only; V is fixed at that file's pin line. One switch: `lineage.V`; without it, `V_without_erratum` = "undetermined" | registry `models.gemma3n_e4b.lineage`; `b_pa1_gpu.py:135`, `b_pa1_gpu.py:1106` | v3.1 §4.1 N6; PI-1108e Q1 | **decided by PI-1108e**; the erratum needs its irreversible-tier read |
| 27 | First-token Y/N rule: Y holds `C` (from "Có" = C + ó) and N holds `kh` (from "không"). HOSTCHECK records each word's token count and first token | `b_pa1_gpu.py:192`, `b_pa1_models.py:428` | v3.1 §7.1 N5 | ACCEPTED, Ruling 8 (+ N6) |
| 28 | "E1 E2 NOT RUN (pre-fixed, R5 E-12)" goes into the job log at the end of S and into TRIM.json | `b_pa1_job.sh:169`, `b_pa1_gpu.py:758` | R5 E-12 | ACCEPTED, CC-295r3 Ruling 6 |
| 29 | HOSTCHECK_*.json is bound to code, freeze and the GPU uuid (HB-T1′ forces a fresh host selftest) | `b_pa1_job.sh:99` | RD §8 | ACCEPTED, CC-295r3 Ruling 6 |
| 30 | rc 137 is a final CAP STOP only if the step's elapsed time ≥ its LEFT (KILL after the timeout). An earlier 137 (OOM or an outside KILL) is a guard failure and gets the one resume. Two clocks, each compared only with itself: the job's `mono` = `/proc/uptime` (CLOCK_BOOTTIME) for EL, and the ledger's `m` = `time.monotonic()` (CLOCK_MONOTONIC) for step seconds. A wall-clock step moves neither (one was seen on the laptop during the tests). An open step from an earlier boot is never subtracted: `left` faults on an open step outside `s.trim`, `resume` needs `--close-sec`, and reading 21 never copies the ledger to HB-T1′ | `b_pa1_job.sh:159`, `b_pa1_job.sh:36`, `b_pa1_gpu.py:891`, `b_pa1_gpu.py:433` | v3.1 l.503-504, l.519-520 | ACCEPTED, CC-295r2 item 7 (N-e wording) |
| 31 | A final stop (CAP, MONEY, PA3, CORE) writes `SHA256SUMS_<run>_stop` of out/, logs/ and w25_parts; a done mode writes `SHA256SUMS_<mode>`. The EXIT trap writes either one last, after the EXIT line, so `logs/job.log` itself verifies at the pull. Teardown first ignores TERM, HUP, INT and PIPE, and `say` writes the file before the console, so a dead console cannot fail it (W9). **Tested scope** (job selftest): one TERM (B), marker then TERM (B2), marker then tmux kill-session (B4), marker, TERM and a second TERM inside a slowed teardown (B5), the in-loop marker (J), CAP (A, F, I), PA3 and CORE (G), a done mode (A). **Not covered:** a KILL of the job itself (untrappable) or a machine loss; neither leaves a manifest, and machine loss takes the reading-21 path | `b_pa1_job.sh:58`, `b_pa1_job.sh:45`, `b_pa1_job.sh:37`, `b_pa1_job.sh:48`, `b_pa1_job.sh:50` | RD §14 step 4 | W9 FIXED (CC-295r3 Ruling 5); reworded to the tested scope |
| 32 | `host_w25.sums` is required on the host (fail closed) | `b_pa1_job.sh:68` | RD §1.4 | ACCEPTED, CC-295r2 Ruling 5 |
| 33 | Before each verify or judge step, its input must be complete (4 × 2,000 for A1 and A3; the H count; 2,000 × n for A4) | `b_pa1_gpu.py:770` | v3.1 §9.1 | ACCEPTED, CC-295r2 Ruling 5 |
| 34 | Selftest and mutant scratch dirs are removed by a guarded file-by-file delete: the temp-dir parent and the prefix are checked, links are unlinked and never entered, and each emptied dir is removed with rmdir | `b_pa1_gpu.py:453` | coordinator rule (no rm -rf) | ACCEPTED, CC-295r2 Ruling 5 (N-e wording) |

## CC-295 hunk map

| item | change | where |
|---|---|---|
| W1 | Each step runs in the background (`&`, `SPID`, `wait`). The TERM / HUP / INT trap kills the step's process group, waits, then exits 143, so the EXIT trap closes the ledger step and wipes. The job writes `job.pid`. Tests: job selftest group B; mutant J17 | `b_pa1_job.sh:52`, `b_pa1_job.sh:153` |
| W2 | rc 124 → CAP STOP; rc 137 → CAP STOP only if the monotonic EL ≥ LEFT, else a guard stop. Tests: groups D, E; J18, J19 | `b_pa1_job.sh:159` |
| W3 | CORE_STOP.json is in both marker lists. `s.trim` writes it, and the job writes it if absent. Later modes need core_fits true and the previous RUN marker. Tests: python core-stop; groups G, H; G70-G72, J20-J23 | `b_pa1_gpu.py:43`, `b_pa1_gpu.py:764`, `b_pa1_job.sh:108` |
| W4 | this file | — |
| W5 | Registry `instrument_llm` = agent-drafted, amendment-logged, no id. `amend` checks the mode, the LOG-pinned amendment and a drafter per instrument entry; the log line carries `drafter=`. Tests: mid amend cases; D44-D48 | `b_pa1_mid.py:198`, `b_pa1_mid.py:179` |
| W6 | Registry Gemma-3n `lineage.V` = MobileNet-V5 with `V_without_erratum`; the erratum file is drafted (v1; now v1_2, see the CC-295r3 map). Tests: python lineage-switch | registry; `manuscript/prereg/2026-11-01_b_pa1_tier1/ERRATUM_LINEAGE_GEMMA3N_v1_2.md` |
| N1 | Kill cases: a fake-clock ledger (HM1, HM3), `--used-sec` (HM2, HM4), the money boundary (HM5), LEFT 0 (HM8, group F), the W cap (HM10, group I), rc 13 (HM9), rc 137 (HM11). Mutants G75-G79, J24, J25 | `b_pa1_gpu.py:1287` |
| N2 | Every step runs with `< /dev/null`. Test group L; J29 | `b_pa1_job.sh:149` |
| N3 | Markers are checked in the loop before `ledger start`, logging "MONEY STOP (final)" and the like. STEP is set only after `ledger start` succeeds. Group J; J26 | `b_pa1_job.sh:138` |
| N4 | A stop manifest on every final stop (now `MANIFEST=`, written by the EXIT trap; CC-295r2). J27 | `b_pa1_job.sh:58` |
| N5 | `host_w25.sums` required. J28 | `b_pa1_job.sh:68` |
| N6 | HOSTCHECK records each Y/N word's token count and first token, the digit tokens, and each captioner's decode settings | `b_pa1_models.py:76` |
| N7 | accepted (the W venv installs unhashed; the freeze compare decides) | — |
| N8 | `need()` completeness checks. G73 | `b_pa1_gpu.py:770` |
| N9 | the HB-T1′ form, reading 21 (run doc v1.1) | — |
| N10 | job selftest count reported as N checks + PASS | `b_pa1_job_selftest.sh:215` |
| N11 | disk precheck in the weights stage | `b_pa1_setup_host.sh:75` |
| N12 | process notes stay in the record | — |
| N13 | `next_read_h` and `balance-cadence`. G74 | `b_pa1_gpu.py:444` |

## Why, for the open readings (ruled at the round-3 full read, CC-295r2 Ruling 2)

Each item gives the code line, then the reason for the default. "Open" means the registered text does not fix the
choice; nothing here changes a registered rule.

**1. Slice A from the MANIFEST, not from the lists file.**
- Code: `b_pa1_gpu.py:370`, `b_pa1_gpu.py:712`.
- Why: `b_pa1_lists.json` also holds the slice-B ids, and slice B is never decoded, scored or staged in tier 1
  (v3.1 l.255). The host therefore gets no copy of it. The slice-A MANIFEST is exactly what was pushed: its sha is MAN
  (AMAN on an OPS line, RD §9.4), and the job checks the tmpfs file set against it. The frame file is in slice order
  (v3.1 §5.2), so frame order over the MANIFEST names gives slice order, and the gate set is its first 231 (v3.1 l.216).

**4. Freeze check against the first host build.**
- Code: `b_pa1_setup_host.sh:38`,
  `b_pa1_job.sh:75`.
- Why: R2 pins each venv freeze on a LOG line before the first step that reads it (v3.1 l.653-655). A GPU venv's
  freeze exists only after its first build on the host, so its R2 line can be written only after that build, from the
  pulled value. The host therefore records the first-build value and every job compares with it; the laptop compares
  the pulled value with the R2 pin line. The W
  venv is the one exception: its freeze (1a639a50) is known before any build (R5 §D.2), so the host checks the constant.

**7. Decomposer form.**
- Code: `b_pa1_gpu.py:253`, `b_pa1_models.py:268`; registry `prompts.d1`,
  `decomposer_decode`.
- Why: v3.1 §7.1-7.2 fix the model (Qwen2.5-7B-Instruct), "typed propositions" and the d1 / d2 contrast, but not the
  instruction language or the output form. Both verifier prompts take the proposition in Vietnamese (v1, v2), so the
  propositions are copied from the caption's own words. JSON with type, text and object makes the parse mechanical, and
  `object` is the field the map matches. Greedy decoding and a 512-token bound keep the step deterministic and bounded.
  Each parse is marked ok, partial or fail, so a failed parse is counted and never dropped silently.

**8. Smoke set.**
- Code: `b_pa1_gpu.py:740`,
  `b_pa1_gpu.py:662`.
- Why: row S of v3.1 §9.1 fixes 64 slice-A images and keeps smoke outputs "only as rates". The first 64 lie inside the
  231-image gate set, so their captions already exist and no extra decode is spent. Image i goes to captioner i mod 4,
  which gives each accepted captioner 16 captions. The timings stay in memory and only `rates_smoke.json` is written,
  which is stricter than writing outputs and deleting them later.

**9. A4 decode rate.**
- Code: `b_pa1_gpu.py:727`.
- Why: the trim rule (v3.1 l.510-511) needs a measured A4 rate, because A4 is the first block it drops once E2 is out,
  but §9.1 names no A4 measurement. Sixteen images per A4 model is the smoke's per-captioner count. It bounds the cost
  to about 3 × 16 × 0.84 s of decode plus the model loads [est.]. A4 captions are no S output, so they stay in memory.

**10. Gate decodes are not reused in A1-decode.**
- Code: `b_pa1_gpu.py:779`.
- Why: §6.4 step 3 defines A1-decode as the slice-A captions of the 4 accepted captioners, as one step. A full re-decode
  makes each captioner's file one run: one code path and one manifest. A file joined from block S and
  block A1 would mix two runs. The cost is 4 × 231 × 0.8409 s, about 13 min [est.]. Block H is consistent with it: `htrans`
  takes the A1-decode captions of the 231 gate ids, not the gate files (N-g).

**12. mBLIP prompt.**
- Code: `b_pa1_models.py:147`.
- Why: v3.1 l.220 asks for "each model's own chat template". mBLIP (a BLIP-2 model) ships no chat template, and its
  model card prompts with the plain instruction. That plain form is therefore its own template.

**13. Card preprocessing values.**
- Code: `b_pa1_models.py:172`, `b_pa1_models.py:224`; registry `molmo_7b_o.dtype`.
- Why: v3.1 fixes the prompt and decoding (l.220) but not the image preprocessing. The card values are each model's
  intended use, and taking them involves no tuning on B data. Molmo-7B-O runs in bf16 because its fp32 weights
  (30.67 GB in the registry) do not fit in 24 GB.

**14. H2 transforms on the laptop.**
- Code: `b_pa1_mid.py:366`, `b_pa1_mid.py:383`,
  `b_pa1_gpu.py:805`.
- Why: the segmentation transform uses the R7 segmenter (v3.1 §8.4), which is pinned on the laptop. Running all six
  transforms there keeps R7 off the host. The host gets one input file, and the job checks its sha (EXTRA). The pick is
  §8.4's argmin of sha256("b-pa1-h2|" + file_name + "|" + captioner id), with the registry key as the captioner id. It
  is fixed before any caption exists. The tier-2 prereg, which runs the same rule on slice B, copies this form verbatim
  (N-h).

**15. Coverage normalisation and counting.**
- Code: `b_pa1_mid.py:59`, `b_pa1_mid.py:140`, `b_pa1_mid.py:261`.
- Why: "covered" should mean what the scorer would match, so tokens and terms go through the same NFC, lower-case,
  `_`-to-space and rescap `norm_tone` steps. A token with no letter cannot be a map entry. §6.1 (i) counts captions
  ("occurring in ≥ 10 slice-A captions"), so the count is over distinct captions of the 8,000, not over occurrences.
  New terms are appended after the map v1 terms, so add-only also holds for the order the matcher reads.

**16. An (ii) entry may not reuse an existing term.**
- Code: `b_pa1_mid.py:229`.
- Why: §6.1 says amendments are add-only and that no existing entry is edited. Giving an existing term a second class
  changes what that existing entry matches, which is an edit. So only a term that is new to both the map and the log
  is accepted.

**17. The parity2 gate.**
- Code: `b_pa1_mid.py:286`.
- Why: §6.3 registers run 2 "on the final map sha" with the same statistic and stop, but not the LOG line form. Three
  checks make run 2 provably that run: the parity1-done line of the map v1 it extends, a freeze pin line carrying every
  input sha, and exactly one start line with no done line. Without the last check, a second run could be chosen after
  seeing the first.

**19. Captioner prompt.**
- Code: registry `prompts.captioner` (= `scripts/evaluate.py` `PROMPTS["short"]`).
- Why: the decode cost in §9.1 and R6-II §2 step 6 rests on the 3090 short-mode rate of 0.8409 s per caption, which was
  measured with this prompt (B direction §3.7). Any other prompt would leave the cap arithmetic without its measured
  base. v3.1 l.220 also asks for the tier-3 prompt, and that is the short mode.

**21. Ledger and the HB-T1′ form.**
- Code: `b_pa1_gpu.py:428`, `b_pa1_gpu.py:900`, `b_pa1_gpu.py:871`.
- Why: the cap is GPU-h of steps; setup and pushes are costed apart (§9.1 "plus 4 h setup"). The step seconds come from
  the monotonic clock (reading 30). R6-II §2 step 5 makes the cap one total over HB-T1 and HB-T1′, so `cap-init
  --used-sec` carries the used seconds to the new host. The ledger is not copied, because its `m` values belong to the
  lost machine's boot clock. CAP.json is not copied either, since `cap-init` writes it fresh, and the freeze files are
  re-recorded from the new build and checked against R2 on the laptop. `RESUME.json` and `RESUME_USED` travel when
  present (N-i): `resume` does not check `RESUME_USED`, and the job's `set -C` guard sees only the new `~/b_pa1_out`, so
  without them a resume used on HB-T1 would not count. If either exists, HB-T1′ takes no resume and the PI decides.

**22. One resume in total.**
- Code: `b_pa1_job.sh:129`.
- Why: v3.1 l.519-520 allows one resume, for machine loss or a guard failure only. `RESUME.json` records the cause.
  `RESUME_USED` is made with noclobber (`set -C`), so it is created at most once; a second attempt, even after a crash
  in between, finds it and stops.

**25. `b_pa1_dev_contacts.json`.**
- Code: none in this set (no GPU file names it; the committed `b_pa1.py` lists it as "not-yet-written").
- Why: v3.1 l.143-147 makes it the list of every image id that B decodes or scores. Those ids are in the pulled
  outputs, which the laptop holds after the final pull, while the host is deleted. Writing the list once on the laptop,
  from the pulled and sha-checked files, gives one source and one sha.

**28. "E1 E2 NOT RUN".**
- Code: `b_pa1_job.sh:169`,
  `b_pa1_gpu.py:758`.
- Why: R5 E-12 fixes E1 and E2 as NOT RUN and asks for the record in the run log before the end of A2. The end of block
  S is the first point after the trim decision. TRIM.json carries the same words, so the record is in the pulled
  output as well as in the log.

**29. HOSTCHECK binding.**
- Code: `b_pa1_job.sh:99`.
- Why: a HOSTCHECK file proves the token sets, digit tokens and decode settings for one code sha, one freeze and one
  GPU. HB-T1′ restores `~/b_pa1_out` from the pull, which would bring the lost host's HOSTCHECK files with it. The
  uuid binding makes the job refuse them, so the new machine must pass its own `selftest` mode first (RD §8).

## CC-295r2 hunk map (round 3)

| item | change | where |
|---|---|---|
| W7 | `amend` refuses an entries file whose own sha is not on a LOG pin line naming it (every entries file, dictionary or instrument; the D-8 §7 pin form). Tests: mid "amend-entries-pin" (an unpinned file with a pinned amendment is refused; look-alike non-pin lines do not count). Mutant D49 | `b_pa1_mid.py:246` |
| W8 | Registry `prompts.instrument_i` (sha 4ac3f695) and `instrument_ii` (sha 79950e29) name no drafting rule. They point by name, not by sha, to "the step-4 amendment named in each entries file's provenance and pinned on a LOG line (b_pa1_mid.amendment_ok)" | registry `prompts`; `instrument_llm.prompts` |
| W6 | The registry source string and the selftest assert name `ERRATUM_LINEAGE_GEMMA3N_v1_1.md`, with v1_1's resolver order | gpu selftest assert (renamed to v1_2 in round 4); registry `models.gemma3n_e4b.lineage.source` |
| N-a | Teardown: rc 143 with MONEY_STOP.json present logs "MONEY STOP (final) on signal" and writes `SHA256SUMS_<run>_stop`. Every manifest (stop or done) is now written by the EXIT trap after the EXIT line, so `logs/job.log` verifies. Tests: group B2; "mode manifest written last"; each stop manifest is verified with `sha256sum -c`. Mutants J32, J33, J34 (J26, J27 re-cut) | `b_pa1_job.sh:48`, `b_pa1_job.sh:50`, `b_pa1_job.sh:168` |
| N-b | Kill case for the trap's `wait`: a stub step traps TERM and exits 2 s later, recording its exit on CLOCK_MONOTONIC. The test asserts that the ledger end's `sec` exceeds (stub exit − start `m`), so the end was written after the step ended. Mutant J31 | `b_pa1_job_selftest.sh:46`, `b_pa1_job_selftest.sh:74` |
| N-c | `x/coverage.json` removed by name and `x/` by rmdir. `outside_tree` takes the tree root; the refusal case targets `x/` inside the selftest's own fixture repo and asserts nothing was made, so D14 dies on its assertion and a mutant can write only in the scratch tree. Mutant D50 | `b_pa1_mid.py:64`, `b_pa1_mid.py:518` |
| N-d | One combined disk check at the first fetch; `PIP_NO_CACHE_DIR=1` | `b_pa1_setup_host.sh:73`, `b_pa1_setup_host.sh:25` |
| N-e | Readings 30 (the two clocks) and 34 (the guarded delete) reworded | this file |
| readings | The open readings carry a "why" with code lines (section above) | this file |
| erratum | `ERRATUM_LINEAGE_GEMMA3N_v1_1.md` (E1-E8); v1 kept unchanged and never committed | `manuscript/prereg/2026-11-01_b_pa1_tier1/` |

## CC-295r3 hunk map (round 4 draft; `b_pa1_mid.py` unchanged at b8afa120, CC-296 Ruling 10)

| item | change | where |
|---|---|---|
| W6 | The registry source string and the gpu selftest assert name `ERRATUM_LINEAGE_GEMMA3N_v1_2.md`. Only that file name changes in the registry; model pins and prompt shas are unchanged | `b_pa1_gpu.py:1106`; registry `models.gemma3n_e4b.lineage.source` |
| W9 (a) | Teardown's first line keeps `rc`, then ignores TERM, HUP, INT and PIPE, so a second signal cannot cut it short. Test: group B5 (marker, TERM, a second TERM while the slowed wipe runs; rc 143, EXIT line, manifest verifies). Mutant J35 | `b_pa1_job.sh:45` |
| W9 (b) | `say` writes job.log first, then the console with `|| true`, so a dead pty cannot end teardown under errexit. Test: group B4 (marker, then `tmux kill-session` on the job's own tmux socket; EXIT line, money line, manifest verifies, set wiped). Mutant J36 | `b_pa1_job.sh:37` |
| W9 (c) | The kills and the `wait` in `on_signal` end with `|| true` | `b_pa1_job.sh:52` |
| reading 31 | Reworded to the tested scope | this file |
| N-f HM28 | Group B: a TERM without the marker writes no money line and no stop manifest. Mutant J37 | `b_pa1_job_selftest.sh:133` |
| N-f HM32 | A rc-3 step (`s.smoke`) gives PA3 STOP with a verified `SHA256SUMS_s_stop`. Mutant J38 | `b_pa1_job_selftest.sh:192` |
| N-f HM36 | **Not done.** The case ("the right sha under another name is refused") belongs in the `b_pa1_mid` selftest, and `b_pa1_mid.py` must stay b8afa120. By reading, `amend` passes `a.entries.name` to `pin_line`, which needs the name as a delimited token on the same PIN_RE line | `b_pa1_mid.py` `cmd_amend` (unchanged) |
| N-g | Reading 10 states that H uses the A1-decode captions. The optional `htrans` assert is not added, for the same reason (mid frozen) | this file |
| N-h | Reading 14: the tier-2 prereg copies the pick form verbatim | this file |
| N-i | Reading 21: the HB-T1′ restore list adds `RESUME.json` and `RESUME_USED`; if either exists, no resume and the PI decides; S counts an open step up to the loss. It binds the run doc v1.1; no code change (with `RESUME_USED` restored, the job's `set -C` guard refuses; with `RESUME.json` restored, `resume` refuses on its exclusive create) | this file |
| J17, J31 | Patterns re-cut to the `|| true` form | `b_pa1_gpu_mutants.py` |
| erratum | `ERRATUM_LINEAGE_GEMMA3N_v1_2.md` (E9: l.155-156 twice, l.158, the l.160-162 quote verbatim in full); v1 and v1_1 kept unchanged and never committed | `manuscript/prereg/2026-11-01_b_pa1_tier1/` |
