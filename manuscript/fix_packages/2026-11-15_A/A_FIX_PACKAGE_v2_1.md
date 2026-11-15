# Paper A fix package v2.1

Written 2026-11-15T00:29Z (2026-11-15, 07:29 Vietnam time). Target journal of the paper: Signal Processing: Image Communication.

**Supersedes** `A_FIX_PACKAGE_v2.md` (sha256 b9cf7066e03f...). The only changes are in group A (blocks A2-F01 to A2-F03), after the corresponding author's answer to follow-up F2; all other blocks and steps are the same text as in v2. Use `apply_a_v2_1.py`, not `apply_a_v2.py`.

**What this file is.** Proposed text changes to Paper A after ruling CC-403, each as an exact OLD/NEW pair with its evidence, for a judge to read before anything is applied. Nothing has been applied, staged or committed. The package is outcome-free with respect to Section 6.7 and Supplementary S11: it quotes no figure and no verdict of that study, so no `*_HELD.md` file was needed.

**Inputs.**
- Paper: `/mnt/d/vsps_papers/vsps-paperA-spic/paper/` at HEAD `dafba17` (package v1 applied under CC-403); working tree of `paper/` clean.
- Ruling `CC-403` (open items W4, W5, N1 to N5; Annex B texts N-12r and N-15r).
- The corresponding author's answers A1, A2, A3 and A6 in `manuscript/RESPONSE_FROM_CORESSPONDING_AUTHOR.answers_7e8f958d.md`, and the answer to follow-up F2 in `...answers_4b4ec736.md` (only these five answers were read; no name, identifier or address from those files is copied here).
- LOG lines `OPS-1115d-author-followup` and `OPS-1115e-ktvic-readme` (the coordinator's public reads of the dataset repository on 2026-11-15).

**Numbering.** In CC-403 itself the KTVIC declaration is W5 (item N-09 of package v1) and the internal terms of Supplementary S11 are W4 (item N-03). The task brief names them the other way round. This package uses the numbering of the ruling.

**What the package does.**
- Group A (CC-403 W5, answers A1 and F2): `declarations.md`, its anonymised copy and Section 9.2 get one KTVIC sentence in the structure of the PASCAL-50S sentence, with three facts: the public repository carries no data licence file (as read on a stated date); the training split was used to train the two adapters of Section 6.2; nothing of KTVIC and no adapter is redistributed. The training fact is verified from the run records, the repository fact from the two LOG lines, the third from the record of the staged archive. No licence or terms wording, and no sentence that the authors agreed. What could not be verified is a `[TO CONFIRM]` note in Section 5, not paper text.
- Group B (answer A1, decision (2)): the four other places that say dataset authors agreed lose that clause. Group B is a separate group so that the judge can rule on it apart from group A.
- Group N (CC-403 N1 to N5): five carried items, all outside the custody zones.
- Section 6.7, Supplementary S11, the abstract and the highlights stay byte-unchanged (hold H-1); the apply script asserts it.

## 1. Counts

- 14 items, written as 18 blocks (four items touch both supplement files: `a` = `supplementary.md`, `b` = `supplementary_SPIC.md`).
- 3 steps that are not blocks (two manifest rows, the regenerated provenance table, the length block).
- Deferred: 6 items (Section 6.1). For the investigator: 7 items (Section 6.2).
- Main text: 18,780 words at HEAD, 18,931 after the package (+151).

## 2. Table of blocks

| Id | Source | File | Line at HEAD | What changes |
|---|---|---|---|---|
| A2-F01 | W5 / A1 | `declarations.md` | 19 | Data availability: KTVIC sentence in the structure of the PASCAL-50S sentence (repository carries no data licence file, as read on a stated date; training split used to train the two adapters of Section 6.2; nothing redistributed); the clause that the dataset authors agreed is gone |
| A2-F02 | W5 / A1 | `anon/declarations_anon.md` | 10 | anonymised declarations: the same KTVIC sentence added |
| A2-F03 | W5 / A1 | `sec11_limitations_ethics.md` | 48 | Section 9.2: a KTVIC paragraph added with the same three facts |
| A2-F04 | A1 (2) | `sec11_limitations_ethics.md` | 44 | Section 9.2: the clause that the UIT-OpenViIC authors agreed removed |
| A2-F05 | A1 (2) | `declarations.md` | 19 | Data availability: the clause that the PASCAL-50S authors agreed removed |
| A2-F06a | A1 (2) | `supplementary.md` | 658 | Supplementary S6: the sentence that the UIT-OpenViIC authors agreed removed |
| A2-F06b | A1 (2) | `supplementary_SPIC.md` | 540 | Supplementary S6: the sentence that the UIT-OpenViIC authors agreed removed |
| A2-F07a | A1 (2) | `supplementary.md` | 1350 | Supplementary S10: the clause that the UIT-OpenViIC authors agreed removed |
| A2-F07b | A1 (2) | `supplementary_SPIC.md` | 1156 | Supplementary S10: the clause that the UIT-OpenViIC authors agreed removed |
| A2-F08a | N1 | `supplementary.md` | 497 | Supplementary S4, "Scope of the confirmatory evidence": "endpoint" replaced by what it meant, a positive label-gold slope |
| A2-F08b | N1 | `supplementary_SPIC.md` | 405 | Supplementary S4, "Scope of the confirmatory evidence": "endpoint" replaced by what it meant, a positive label-gold slope |
| A2-F09a | N2 | `supplementary.md` | 278 | Supplementary S3, "One gain reverses": "a significant loss" replaced by "a loss ... whose unadjusted interval excludes 0" |
| A2-F09b | N2 | `supplementary_SPIC.md` | 234 | Supplementary S3, "One gain reverses": "a significant loss" replaced by "a loss ... whose unadjusted interval excludes 0" |
| A2-F10 | N3 | `sec3_measurement_setup.md` | 52 | Section 3.6: the draw count of Table 5.1 (1,000) stated |
| A2-F11 | N4 (N-12r) | `sec10_discussion.md` | 18 | Section 8.3, checklist item 2: advice changed from "locate systems relative to the F1 optimum" to "report under more than one gold" |
| A2-F12 | N4 (N-12r) | `sec10_discussion.md` | 19 | Section 8.3, checklist item 3: "calibrate" lowered to "check", with the limit of the placebo named |
| A2-F13 | N4 (N-15r) | `sec4_theory.md` | 23 | Section 4.2: one sentence that Proposition 1 does not cover the label step on XM3600 |
| A2-F14 | N5 | `V2_PROGRESS.md` | 63 | V2_PROGRESS.md (internal): the claim that the scrub re-runs clean replaced by the true state |

## 3. Blocks

Each OLD string is given exactly as it stands in the file at HEAD, and each NEW string exactly as it should stand. A marker line is not part of a string; the string is the text between two marker lines, without the line break before the next marker. An empty NEW means that the OLD string is deleted. The NEW string of A2-F03 holds one empty line (a paragraph break).

<<<A2-F01 declarations.md OLD>>>
UIT-OpenViIC and KTVIC are used only through aggregates and pointers; one of us contacted the UIT-OpenViIC and KTVIC authors, who agreed to this use.
<<<A2-F01 declarations.md NEW>>>
UIT-OpenViIC is used only through aggregates and pointers. The public repository of KTVIC (Pham et al., 2024) carries no data licence file (as read on 15 November 2026); the KTVIC training split (3,769 images, with captions of that split as training targets) was used to train the two adapters of the first backbone (Section 6.2); no KTVIC image or caption is redistributed, and the trained adapters are not part of the release.
<<<A2-F01 EVIDENCE>>>
Repository clause: decision of the corresponding author in answer F2 (no licence or terms wording; state the checked facts in the structure of the PASCAL-50S sentence) and the coordinator's public reads of 2026-11-15, LOG lines OPS-1115d-author-followup and OPS-1115e-ktvic-readme (`decisions/LOG.md` l.2634 and l.2635): the repository has no licence file, a null licence field and no terms sentence in its README (git blob sha1 79df85a4...). The text says only that the repository carries no data licence file, with the date of the read; it does not say that the data are free of terms. Training clause: Run records (run repo): `.session_backup/machines/n2/ncs-data/gold_p1/_build_report.json` (sha256 prefix c2d032a08577): source = `.../datasets/ktvic/train_data.json`, images_with_caption = 3769, captions_total = 18845, captions_used = 3769, policy "short row: first caption"; `.../gold_fuse2/_build_report.json` (136c2228ea70): same source, images_with_caption = 3769, captions_used = 7538 (one consensus-caption row and one row of up to two joined captions per image). The two training files hold 3,769 and 7,538 rows over 3,769 distinct images each. Run folders `.../runs/p1_s43` and `.../runs/fuse2_s42`: `adapter_config.json` base model Qwen/Qwen2.5-VL-7B-Instruct, LoRA; `metrics.jsonl` ends at step 942 and step 1,884, epoch 2.0 (3,769 x 2 / 8 and 7,538 x 2 / 8). The source file equals `data/datasets/ktvic/train_data.json` (72ee9b57c350; 3,769 images, 18,845 captions); the KTVIC test file (558 images) is not a source of either build. Manifest rows l.1405 and l.1406 key the 3,769 to the two build reports. Paper text: Section 6.2 (`sec7_verbosity_sign.md` l.45) "two Vietnamese adapters, both trained on the 3,769 images of the KTVIC training split". Nothing-redistributed clause: record of the staged archive `.session_backup/2026-10-21/zenodo_build`: its `README.md` (sha256 prefix b4897be2c239) l.24 "No caption text", l.30 "The archive contains no images, no reference captions and no model weights", l.75 lists "System outputs, adapters and checkpoints" as not included; `FINAL_SCAN.json` (43800f2e7856) has no caption-text hit over 407 files; the folder holds no image file and no weight file. The existing sentence of `declarations.md` l.19 already says that the reference captions of KTVIC are not redistributed. The deposit itself does not exist yet (note TC-3). No sentence says that the dataset authors agreed: answer A1 of the corresponding author, decision (2), prints that clause only once the written reply is on file, and the task brief orders it out. Clauses that could not be verified are not in the text; they are the [TO CONFIRM] notes of Section 5. Structure: the PASCAL-50S sentence of the same paragraph (repository and its licence state; what the data were used for; what is not redistributed). The old sentence was untrue for KTVIC in two ways: the training use was left out, and "only through aggregates and pointers" excluded it. The new text makes no "only" statement about KTVIC.

<<<A2-F02 anon/declarations_anon.md OLD>>>
UIT-OpenViIC, KTVIC references and human-judgment ratings are not redistributed (Section 9.2).
<<<A2-F02 anon/declarations_anon.md NEW>>>
UIT-OpenViIC, KTVIC references and human-judgment ratings are not redistributed (Section 9.2). The public repository of KTVIC (Pham et al., 2024) carries no data licence file (as read on 15 November 2026); the KTVIC training split (3,769 images, with captions of that split as training targets) was used to train the two adapters of the first backbone (Section 6.2); the trained adapters are not part of the archive.
<<<A2-F02 EVIDENCE>>>
Repository clause: decision of the corresponding author in answer F2 (no licence or terms wording; state the checked facts in the structure of the PASCAL-50S sentence) and the coordinator's public reads of 2026-11-15, LOG lines OPS-1115d-author-followup and OPS-1115e-ktvic-readme (`decisions/LOG.md` l.2634 and l.2635): the repository has no licence file, a null licence field and no terms sentence in its README (git blob sha1 79df85a4...). The text says only that the repository carries no data licence file, with the date of the read; it does not say that the data are free of terms. Training clause: Run records (run repo): `.session_backup/machines/n2/ncs-data/gold_p1/_build_report.json` (sha256 prefix c2d032a08577): source = `.../datasets/ktvic/train_data.json`, images_with_caption = 3769, captions_total = 18845, captions_used = 3769, policy "short row: first caption"; `.../gold_fuse2/_build_report.json` (136c2228ea70): same source, images_with_caption = 3769, captions_used = 7538 (one consensus-caption row and one row of up to two joined captions per image). The two training files hold 3,769 and 7,538 rows over 3,769 distinct images each. Run folders `.../runs/p1_s43` and `.../runs/fuse2_s42`: `adapter_config.json` base model Qwen/Qwen2.5-VL-7B-Instruct, LoRA; `metrics.jsonl` ends at step 942 and step 1,884, epoch 2.0 (3,769 x 2 / 8 and 7,538 x 2 / 8). The source file equals `data/datasets/ktvic/train_data.json` (72ee9b57c350; 3,769 images, 18,845 captions); the KTVIC test file (558 images) is not a source of either build. Manifest rows l.1405 and l.1406 key the 3,769 to the two build reports. Paper text: Section 6.2 (`sec7_verbosity_sign.md` l.45) "two Vietnamese adapters, both trained on the 3,769 images of the KTVIC training split". Nothing-redistributed clause: record of the staged archive `.session_backup/2026-10-21/zenodo_build`: its `README.md` (sha256 prefix b4897be2c239) l.24 "No caption text", l.30 "The archive contains no images, no reference captions and no model weights", l.75 lists "System outputs, adapters and checkpoints" as not included; `FINAL_SCAN.json` (43800f2e7856) has no caption-text hit over 407 files; the folder holds no image file and no weight file. The existing sentence of `declarations.md` l.19 already says that the reference captions of KTVIC are not redistributed. The deposit itself does not exist yet (note TC-3). Clauses that could not be verified are not in the text; they are the [TO CONFIRM] notes of Section 5. The anonymised copy (built for an earlier double-anonymised target) never said that the authors agreed and already says that KTVIC references are not redistributed; it gets the same sentence, with "archive" for "release" as in its own wording. The sentence names no author of this paper.

<<<A2-F03 sec11_limitations_ethics.md OLD>>>
**Licences of human-judgment data.**
<<<A2-F03 sec11_limitations_ethics.md NEW>>>
**KTVIC.** The public repository of KTVIC (Pham et al., 2024) carries no data licence file (as read on 15 November 2026). The KTVIC training split (3,769 images, with captions of that split as training targets) was used to train the two adapters of the first backbone (Section 6.2). No KTVIC image or caption is redistributed, and the trained adapters are not part of this paper's release.

**Licences of human-judgment data.**
<<<A2-F03 EVIDENCE>>>
Repository clause: decision of the corresponding author in answer F2 (no licence or terms wording; state the checked facts in the structure of the PASCAL-50S sentence) and the coordinator's public reads of 2026-11-15, LOG lines OPS-1115d-author-followup and OPS-1115e-ktvic-readme (`decisions/LOG.md` l.2634 and l.2635): the repository has no licence file, a null licence field and no terms sentence in its README (git blob sha1 79df85a4...). The text says only that the repository carries no data licence file, with the date of the read; it does not say that the data are free of terms. Training clause: Run records (run repo): `.session_backup/machines/n2/ncs-data/gold_p1/_build_report.json` (sha256 prefix c2d032a08577): source = `.../datasets/ktvic/train_data.json`, images_with_caption = 3769, captions_total = 18845, captions_used = 3769, policy "short row: first caption"; `.../gold_fuse2/_build_report.json` (136c2228ea70): same source, images_with_caption = 3769, captions_used = 7538 (one consensus-caption row and one row of up to two joined captions per image). The two training files hold 3,769 and 7,538 rows over 3,769 distinct images each. Run folders `.../runs/p1_s43` and `.../runs/fuse2_s42`: `adapter_config.json` base model Qwen/Qwen2.5-VL-7B-Instruct, LoRA; `metrics.jsonl` ends at step 942 and step 1,884, epoch 2.0 (3,769 x 2 / 8 and 7,538 x 2 / 8). The source file equals `data/datasets/ktvic/train_data.json` (72ee9b57c350; 3,769 images, 18,845 captions); the KTVIC test file (558 images) is not a source of either build. Manifest rows l.1405 and l.1406 key the 3,769 to the two build reports. Paper text: Section 6.2 (`sec7_verbosity_sign.md` l.45) "two Vietnamese adapters, both trained on the 3,769 images of the KTVIC training split". Nothing-redistributed clause: record of the staged archive `.session_backup/2026-10-21/zenodo_build`: its `README.md` (sha256 prefix b4897be2c239) l.24 "No caption text", l.30 "The archive contains no images, no reference captions and no model weights", l.75 lists "System outputs, adapters and checkpoints" as not included; `FINAL_SCAN.json` (43800f2e7856) has no caption-text hit over 407 files; the folder holds no image file and no weight file. The existing sentence of `declarations.md` l.19 already says that the reference captions of KTVIC are not redistributed. The deposit itself does not exist yet (note TC-3). Clauses that could not be verified are not in the text; they are the [TO CONFIRM] notes of Section 5. Section 9.2 named UIT-OpenViIC and UIT-ViIC only; the citation is the one Section 1 already uses for KTVIC.

<<<A2-F04 sec11_limitations_ethics.md OLD>>>
One of us contacted the UIT-OpenViIC authors, who agreed to this use; we have not received written permission from the UIT-ViIC authors (Lam et al., 2020).
<<<A2-F04 sec11_limitations_ethics.md NEW>>>
We have not received written permission from the UIT-ViIC authors (Lam et al., 2020).
<<<A2-F04 EVIDENCE>>>
Answer A1, decision (2): the clause that dataset authors agreed is printed only when the written reply is on file; the task brief orders that no sentence says so. Whether a reply is on file was not checked here (the records of that question are outside what this task may read), so the clause is removed and the fact is left for the investigator to restore. Removing it states nothing new. Section 9.2, paragraph "UIT-OpenViIC and UIT-ViIC". The UIT-ViIC half is unchanged.

<<<A2-F05 declarations.md OLD>>>
the dataset authors were contacted by one of us and agreed to this use; 
<<<A2-F05 declarations.md NEW>>>

<<<A2-F05 EVIDENCE>>>
Answer A1, decision (2): the clause that dataset authors agreed is printed only when the written reply is on file; the task brief orders that no sentence says so. Whether a reply is on file was not checked here (the records of that question are outside what this task may read), so the clause is removed and the fact is left for the investigator to restore. Removing it states nothing new. Data availability, PASCAL-50S sentence; its source comment says the written document still has to be confirmed as on file. The rest of the sentence (public repository, licence notice of the repository, evaluation only, nothing redistributed) stays.

<<<A2-F06a supplementary.md OLD>>>
 One of us contacted the UIT-OpenViIC authors, who agreed to this use.
<<<A2-F06a supplementary.md NEW>>>

<<<A2-F06a EVIDENCE>>>
Answer A1, decision (2): the clause that dataset authors agreed is printed only when the written reply is on file; the task brief orders that no sentence says so. Whether a reply is on file was not checked here (the records of that question are outside what this task may read), so the clause is removed and the fact is left for the investigator to restore. Removing it states nothing new. Supplementary S6, paragraph "UIT-OpenViIC" (`supplementary_SPIC.md` l.540). The OLD string starts with one space.

<<<A2-F06b supplementary_SPIC.md OLD>>>
 One of us contacted the UIT-OpenViIC authors, who agreed to this use.
<<<A2-F06b supplementary_SPIC.md NEW>>>

<<<A2-F06b EVIDENCE>>>
Answer A1, decision (2): the clause that dataset authors agreed is printed only when the written reply is on file; the task brief orders that no sentence says so. Whether a reply is on file was not checked here (the records of that question are outside what this task may read), so the clause is removed and the fact is left for the investigator to restore. Removing it states nothing new. Supplementary S6, paragraph "UIT-OpenViIC" (`supplementary_SPIC.md` l.540). The OLD string starts with one space.

<<<A2-F07a supplementary.md OLD>>>
contain only aggregate statistics of it (Table 5.1 and Supplementary S5); one of us contacted its authors, who agreed to this use.
<<<A2-F07a supplementary.md NEW>>>
contain only aggregate statistics of it (Table 5.1 and Supplementary S5).
<<<A2-F07a EVIDENCE>>>
Answer A1, decision (2): the clause that dataset authors agreed is printed only when the written reply is on file; the task brief orders that no sentence says so. Whether a reply is on file was not checked here (the records of that question are outside what this task may read), so the clause is removed and the fact is left for the investigator to restore. Removing it states nothing new. Supplementary S10, "From Section 9" (`supplementary_SPIC.md` l.1156). S10 is verbatim earlier text, but its header rule lets sentences later corrected follow the corrected wording.

<<<A2-F07b supplementary_SPIC.md OLD>>>
contain only aggregate statistics of it (Table 5.1 and Supplementary S5); one of us contacted its authors, who agreed to this use.
<<<A2-F07b supplementary_SPIC.md NEW>>>
contain only aggregate statistics of it (Table 5.1 and Supplementary S5).
<<<A2-F07b EVIDENCE>>>
Answer A1, decision (2): the clause that dataset authors agreed is printed only when the written reply is on file; the task brief orders that no sentence says so. Whether a reply is on file was not checked here (the records of that question are outside what this task may read), so the clause is removed and the fact is left for the investigator to restore. Removing it states nothing new. Supplementary S10, "From Section 9" (`supplementary_SPIC.md` l.1156). S10 is verbatim earlier text, but its header rule lets sentences later corrected follow the corrected wording.

<<<A2-F08a supplementary.md OLD>>>
COCO-5000 shows the same ordering and endpoint (four of four predictions held on COCO-5000)
<<<A2-F08a supplementary.md NEW>>>
COCO-5000 shows the same ordering and a positive label-gold slope (four of four predictions held on COCO-5000)
<<<A2-F08a EVIDENCE>>>
CC-403 N1: after block A-F02 of package v1 the word "endpoint" has no antecedent. Table 6.1, COCO-5000 row, label gold +22.13 [+21.39, +22.89] (`sec7_verbosity_sign.md` l.11); Section 6.1 "the slope is ordered, −4.77 < +10.57 < +22.13".

<<<A2-F08b supplementary_SPIC.md OLD>>>
COCO-5000 shows the same ordering and endpoint (four of four predictions held on COCO-5000)
<<<A2-F08b supplementary_SPIC.md NEW>>>
COCO-5000 shows the same ordering and a positive label-gold slope (four of four predictions held on COCO-5000)
<<<A2-F08b EVIDENCE>>>
CC-403 N1: after block A-F02 of package v1 the word "endpoint" has no antecedent. Table 6.1, COCO-5000 row, label gold +22.13 [+21.39, +22.89] (`sec7_verbosity_sign.md` l.11); Section 6.1 "the slope is ordered, −4.77 < +10.57 < +22.13".

<<<A2-F09a supplementary.md OLD>>>
and a significant loss at matched prefix, −1.23 [−2.42, −0.08]
<<<A2-F09a supplementary.md NEW>>>
and a loss at matched prefix whose unadjusted interval excludes 0, −1.23 [−2.42, −0.08]
<<<A2-F09a EVIDENCE>>>
CC-403 N2 (text ruled there). Result file `.session_backup/2026-10-13/r10_cpu/e1_x1pb_verification_v2.json` (sha256 prefix 184f9ccac1b9), `pairs_15."opera/shikra__ours vs opera/shikra__beam5".dP_MCP_prefix`: est −1.231, ci95 [−2.419, −0.082], p_boot 0.04898, p_holm15 0.58776, survives_holm_and_sesoi1 false. Section 3.6 applies Holm to these 15 comparisons, so "significant" without a qualifier is wrong.

<<<A2-F09b supplementary_SPIC.md OLD>>>
and a significant loss at matched prefix, −1.23 [−2.42, −0.08]
<<<A2-F09b supplementary_SPIC.md NEW>>>
and a loss at matched prefix whose unadjusted interval excludes 0, −1.23 [−2.42, −0.08]
<<<A2-F09b EVIDENCE>>>
CC-403 N2 (text ruled there). Result file `.session_backup/2026-10-13/r10_cpu/e1_x1pb_verification_v2.json` (sha256 prefix 184f9ccac1b9), `pairs_15."opera/shikra__ours vs opera/shikra__beam5".dP_MCP_prefix`: est −1.231, ci95 [−2.419, −0.082], p_boot 0.04898, p_holm15 0.58776, survives_holm_and_sesoi1 false. Section 3.6 applies Holm to these 15 comparisons, so "significant" without a qualifier is wrong.

<<<A2-F10 sec3_measurement_setup.md OLD>>>
whose draws also resample the 20 reference subsets).
<<<A2-F10 sec3_measurement_setup.md NEW>>>
whose draws also resample the 20 reference subsets). The adjacent-doubleton shares of Table 5.1 use $B$ = 1,000.
<<<A2-F10 EVIDENCE>>>
CC-403 N3, now confirmed for all five rows of Table 5.1. COCO row: `.session_backup/2026-10-26/a_full5000/eval/exch_full.py` l.35 calls `adj.summarize(...)` without B, and `.session_backup/2026-10-14/r11_litmaps/L2/scripts/adjacency_check.py` l.43 has `def summarize(name, per_image, B=1000, seed=0)` (sha256 prefix 71efcd76be23). UIT-ViIC, Flickr30k and UIT-OpenViIC panel rows (manifest l.107, l.111, l.113 -> `c1_b1_b6_reproduction.json`): `c1_b1_b6_reproduction.py` l.247 calls the same `summarize` without B. UIT-OpenViIC full-test row (manifest l.118 -> `c3_n2_exchangeability_all_datasets.json`): `c3_n2_exchangeability_all_datasets.py` l.37 `B_BOOT = 1000`, used at l.228 inside `audit_k5` (sha256 prefix e2bb5de6ac95). All are percentile intervals over image resamples. Two manifest rows are added by step S1.

<<<A2-F11 sec10_discussion.md OLD>>>
2. **Do not compare F1 across verbosity regimes under incomplete gold** without locating the systems relative to the F1 optimum (Section 6).
<<<A2-F11 sec10_discussion.md NEW>>>
2. **Do not compare F1 across verbosity regimes under one incomplete gold;** report it under more than one gold (Section 6).
<<<A2-F11 EVIDENCE>>>
Text of CC-403 Annex B (N-12r), copied; it asks for a read by someone other than its author. This reader's check: the registered sign-agreement prediction with the F1 optimum failed on XM3600 (Table 1, row A5), and Supplementary S1 says "$M^*$ is descriptive, not an out-of-regime predictor" (`supplementary_SPIC.md` l.80), so the old advice rests on a tool the paper found unreliable; the new advice is what Table 6.1 itself does. It changes what the paper recommends.

<<<A2-F12 sec10_discussion.md OLD>>>
calibrate it with a seed placebo,
<<<A2-F12 sec10_discussion.md NEW>>>
check it with a seed placebo (a check of the paired control only; Section 3.3),
<<<A2-F12 EVIDENCE>>>
Text of CC-403 Annex B (N-12r), copied. This reader's check: Section 3.3 says the registered seed placebo "calibrates the paired control only" (`sec3_measurement_setup.md`, "Applied to published methods"). Remark: the item then ends with a second "(Section 3.3)"; the judge may drop the first pointer.

<<<A2-F13 sec4_theory.md OLD>>>
it motivates, but does not derive, the ordering of the mixed-F1 slopes tested in Section 6.
<<<A2-F13 sec4_theory.md NEW>>>
it motivates, but does not derive, the ordering of the mixed-F1 slopes tested in Section 6. On XM3600 the label gold is not the instance-gold limit of this model ($c_\infty = 1$): it is smaller than the union of all references (Table 6.2) and is scored with verified precision (Section 3.1), so Proposition 1 does not cover the label step there.
<<<A2-F13 EVIDENCE>>>
Text of CC-403 Annex B (N-15r), copied. This reader's check: Section 4.1 (`sec4_theory.md` l.11) "Instance gold corresponds to $c_\infty = 1$ for every present object"; under the model that gold contains every reference gold, while Table 6.2 gives the XM3600 label gold as 0.87 times the union of all references; Section 3.1 gives the verified-precision rule. The sentence is interpretive and adds no number.

<<<A2-F14 V2_PROGRESS.md OLD>>>
`supplementary_SPIC.md` is currently in sync with `supplementary.md`: a re-run of `scrub_supp.py` into scratch is byte-identical (442 comments, 0 leaks). On 11-05:
<<<A2-F14 V2_PROGRESS.md NEW>>>
`supplementary_SPIC.md` equals `scrub()` of `supplementary.md` byte for byte (checked by importing `scrub()` from `scrub_supp.py`, not by running the script). A run of `scrub_supp.py` itself would stop on its leak check, because visible text of Supplementary S11.5 and S11.8 matches the leak pattern (one decision id and three `scripts/` paths); the script must not be run, and the checklist below cannot be executed, until the S11 update removes those hits (CC-403 W4). The checklist as prepared for 11-05:
<<<A2-F14 EVIDENCE>>>
CC-403 N5: the old sentence is false on both counts. At HEAD dafba17 `scrub(supplementary.md)` equals `supplementary_SPIC.md` byte for byte (653 comments removed) and stays equal after this package; the leak pattern matches at `supplementary_SPIC.md` l.1486 (a decision id) and l.1728 (three hits on two script paths), all inside S11. `V2_PROGRESS.md` is an internal file.


## 4. Steps that are not blocks

**S1. Two rows appended to `number_manifest.tsv`** (for A2-F10; tab-separated, in the format of the file; shown here with the tabs as they are):

```
1,000 (Table 5.1 bootstrap draws: COCO, UIT-ViIC, Flickr30k and UIT-OpenViIC panel rows)	A	.session_backup/2026-10-14/r11_litmaps/L2/scripts/adjacency_check.py	l.43 "def summarize(name, per_image, B=1000, seed=0)"; called without B by exch_full.py l.35 and c1_b1_b6_reproduction.py l.247	71efcd76be23	keyed_text (CC-403 N3; code default; sec3 §3.6)
1,000 (Table 5.1 bootstrap draws: UIT-OpenViIC full-test row)	A	.session_backup/2026-10-14/r11_verify/c3_n2_exchangeability_all_datasets.py	l.37 "B_BOOT = 1000", used at l.228 in audit_k5	e2bb5de6ac95	keyed_text (CC-403 N3; code constant; sec3 §3.6)
```

**S2. `supplementary_provenance_internal.tsv` regenerated** from the rows that `scrub()` returns for the changed `supplementary.md`, written in the format of `scrub_supp.py`'s `main()` (header line, tab-joined rows). `scrub_supp.py` itself is not run (CC-403 W2 and W4).

**S3. Length block at the top of `abstract_A.md`** (an HTML comment, not paper text; the abstract paragraph, its 250 words and the keywords line are unchanged):

- `recounted 2026-11-14 UTC after the CC-403 text fixes).` -> `recounted 2026-11-14 UTC after the CC-403 text fixes; recounted after fix package v2 of 2026-11-15).`
- `Main text now: 18,780 words` -> `Main text now: 18,931 words`
- `Over the limit by 10,280 words.` -> `Over the limit by 10,431 words.`
- `Longest files: sec7_verbosity_sign.md 7,523; sec2_related_work.md 2,184; sec11_limitations_ethics.md 2,007.` -> `Longest files: sec7_verbosity_sign.md 7,523; sec2_related_work.md 2,184; sec11_limitations_ethics.md 2,061.`

## 5. Notes on the KTVIC statement

1. **What the run records show.** Two LoRA adapters of Qwen2.5-VL-7B (run records `p1_s43` and `fuse2_s42`) were trained on files built from the KTVIC training split only: 3,769 images in both builds; one caption per image in the first build, and two rows per image in the second (a consensus caption for the short prompt, up to two joined captions for the detailed prompt). The KTVIC test split is not a source of either build. These are the "two Vietnamese adapters" of Section 6.2; the same two adapters are among the systems of the exploratory COCO-5000 rows of Section 6.1 (Supplementary S7, l.574 of the journal file).
2. **The repository clause.** Answer F2 decides: no licence or terms wording; state the checked facts in the structure of the PASCAL-50S sentence. The checked facts are those of the two LOG lines: no licence file, a null licence field, no terms sentence in the README. The text therefore says that the public repository "carries no data licence file (as read on 15 November 2026)". It does not say that the data are free of terms, and it prints no licence name. My own search of the run repository agrees with this as far as it goes: the local dataset folder holds `images/`, `train_data.json` and `test_data.json` only, and the two annotation files have no licence or info field.
3. **Structure.** The PASCAL-50S sentence has four parts: where the data were obtained (with a commit), the licence state of that place, what the data were used for, what is not redistributed. The KTVIC sentence has the last three. The first part is left out because it could not be verified (TC-2).
4. **Other uses of KTVIC that the paper already states.** Supplementary S4 (journal file l.392) says that a summary on a KTVIC development split informed the second-backbone registration and that no number from it is used. Section 1 cites the size of KTVIC from its paper. The new sentences do not say "only", so they do not contradict either.
5. **The anonymised copy.** `anon/declarations_anon.md` was built for an earlier, double-anonymised target and says so in its first comment. It is updated because the brief names it; whether the file is still needed for this journal (single-anonymised review) is for the investigator.
6. **Internal comments.** The source comments beside the removed clauses still record that the investigator obtained written acceptance from three dataset groups. They are internal, are not printed, and are left as the record of why the clause was there.

**`[TO CONFIRM]` notes (not paper text).**

- **TC-1 `[TO CONFIRM]` Which repository.** The LOG lines confirm the state of the repository named in answer F2. That this repository is the one the dataset paper names for the data (a footnote of that paper) was read by the corresponding author; the paper's own reference for KTVIC (`paperA.bib`, key `pham2024ktvic`) gives the preprint, not the repository. One reading of the dataset paper closes this. The text prints no address.
- **TC-2 `[TO CONFIRM]` Where the local copy came from.** No download record and no commit of the dataset repository was found in the run repository for the local KTVIC files. The local `train_data.json` (sha256 prefix 72ee9b57c350; 3,769 images) and `test_data.json` (558 images) agree with the totals that Section 1 cites from the dataset paper, but equality with the files in the public repository was not checked (no hash of them is on record). The text therefore says "the KTVIC training split", not "the released training split", and does not say where the copy was obtained. A hash comparison with the repository files closes this; the clause "obtained from the authors' public repository (commit ...)" can then be added as for PASCAL-50S.
- **TC-3 `[TO CONFIRM]` The release.** "No KTVIC image or caption is redistributed, and the trained adapters are not part of the release" is verified against the staged archive of 2026-10-21 only. The deposit itself does not exist yet (item N-06 of package v1). When it is made, its content has to be checked against this sentence; if the investigator decides to release the adapters, the last clause changes.
- **TC-4 `[TO CONFIRM]` What the deposit holds for KTVIC.** Answer F2 also proposes to say that the deposit holds only aggregate statistics, score-only files and pointers. The first sentences of the Data availability paragraph already say this for the whole deposit, so it is not repeated for KTVIC. Whether the deposit holds any KTVIC pointer file was not checked.
- **TC-5 `[TO CONFIRM]` The date.** "As read on 15 November 2026" is the date of the LOG reads (2026-11-15T00:22Z and 00:23Z). The repository should be read again shortly before submission and the date updated.
- **TC-6 `[TO CONFIRM]` Agreement.** The clause that the dataset authors agreed stays out until a written reply is on file (item I-1).

## 6. Deferred items and items for the investigator

### 6.1 Deferred (not in this package)

- **D-1. CC-403 W4 (item N-03): internal terms in the quoted registered text of Section 6.7 and Supplementary S11, and the leak hits of the scrub.** Waits for the H-1 release and the S11 update; the approach is ruled in CC-403 Ruling 2. Until then `scrub_supp.py` must not be run.
- **D-2. Abstract, highlights and cover letter** (items N-02, N-08, N-11 and A-F21 of package v1; L-01 to L-05): one sync after the release.
- **D-3. Answer A6, the title.** The corresponding author keeps the working title until the investigator's last rewrite and then prefers a neutral wording in place of "Gold Completeness" (first candidate: "Gold-Set Specification and the Verbosity Slope of Object Hallucination Metrics: A Registered Audit"), with one sentence in the abstract and Section 1 that separates the reference steps from the label step. Section 1 already has that distinction (`sec1_introduction.md` l.11, the two sentences on the reference steps and the label step). The abstract and the title page are not touched now.
- **D-4. Carried by CC-403 and not asked here:** the second half of CC-262 N2 (S10 confirmatory-claim paragraph) and CC-262r2 N4 to N6.
- **D-5. Item N-13 of package v1** (Table 2.1: two papers to read in full, one more row, the status of a concurrent manuscript, two year mismatches): needs the network.
- **D-6. Length** (item N-01): no text is cut; see `A_CUT_PLAN_v1.md` in this folder. Its note on the effect of this package gives the figure of v2 (+109 words); with v2.1 the rise is +151 words (Section 7.2 gives it by file).

### 6.2 For the investigator

- **I-1. Written confirmation from the KTVIC authors** (answer A1, decision (2)): one letter that also covers the training of the two adapters. The clause that the authors agreed can return to the three KTVIC texts only when the reply is on file.
- **I-2. Group B.** Are written replies from the UIT-OpenViIC and PASCAL-50S authors on file? If yes, the removed clauses (A2-F04 to A2-F07) can be restored in the form "written confirmation is on file"; if no, they stay out.
- **I-3. Answer A3, the declaration on AI tools.** The corresponding author chose a full, truthful statement, the same in all papers, placed for this journal in the Methods (use in the research process) and in a separate section before the references with the publisher's heading. The investigator writes the text from the actual use; no block is proposed, and no sentence denying use may ever be written. The journal's current policy page still has to be re-read in a normal browser.
- **I-4. The `[TO CONFIRM]` notes TC-1, TC-2 and TC-5** (Section 5): one reading of the dataset paper, one hash comparison, and a second read of the repository before submission.
- **I-5. Adapter weights** (TC-3). The new sentences say that the trained adapters are not part of the release. Confirm, or say that the adapters will be released.
- **I-6. Still open from CC-403:** item N-04 (the undefined word "hits" in Supplementary S7), N-05 (addresses and reviewer link), N-06 (the restricted deposit).
- **I-7. The anonymised copy** (note 5): keep or retire.

## 7. Checks run

### 7.1 OLD occurs exactly once (every block)

| Id | File | Count of OLD at HEAD | Count when the blocks of the file are applied in id order | Exactly once |
|---|---|---|---|---|
| A2-F01 | `declarations.md` | 1 | 1 | yes |
| A2-F02 | `anon/declarations_anon.md` | 1 | 1 | yes |
| A2-F03 | `sec11_limitations_ethics.md` | 1 | 1 | yes |
| A2-F04 | `sec11_limitations_ethics.md` | 1 | 1 | yes |
| A2-F05 | `declarations.md` | 1 | 1 | yes |
| A2-F06a | `supplementary.md` | 1 | 1 | yes |
| A2-F06b | `supplementary_SPIC.md` | 1 | 1 | yes |
| A2-F07a | `supplementary.md` | 1 | 1 | yes |
| A2-F07b | `supplementary_SPIC.md` | 1 | 1 | yes |
| A2-F08a | `supplementary.md` | 1 | 1 | yes |
| A2-F08b | `supplementary_SPIC.md` | 1 | 1 | yes |
| A2-F09a | `supplementary.md` | 1 | 1 | yes |
| A2-F09b | `supplementary_SPIC.md` | 1 | 1 | yes |
| A2-F10 | `sec3_measurement_setup.md` | 1 | 1 | yes |
| A2-F11 | `sec10_discussion.md` | 1 | 1 | yes |
| A2-F12 | `sec10_discussion.md` | 1 | 1 | yes |
| A2-F13 | `sec4_theory.md` | 1 | 1 | yes |
| A2-F14 | `V2_PROGRESS.md` | 1 | 1 | yes |

### 7.2 Other checks (all in memory; no paper file was written)

- Paper HEAD `dafba17e543c94f600d16fe0c74b0cb8f7d178b4`; `git status --porcelain -- paper` empty. OLD strings were checked against `git show HEAD:paper/<file>`.
- Every NEW string occurs exactly once in its file after application.
- Supplement sync after all blocks: `scrub(supplementary.md)` equals `supplementary_SPIC.md` byte for byte: **yes** (`scrub()` imported from `paper/build/scrub_supp.py`; the script was not run).
- Leak pattern of the scrub on the journal supplement after the blocks: `CC-335`, `scripts/a_cert/a_cert.py`, `scripts/a_cert/a_cert_vp.py` at line(s) 1486, 1728, 1728, 1728; all inside S11 (deferred item D-1); no new hit.
- Custody zones byte-unchanged (asserted): everything from `## S11 ` to the end of both supplement files; `sec7_verbosity_sign.md` is not written at all (so Section 6.7 is unchanged); `abstract_A.md` from `## Abstract` to the end; `highlights_A.md` is not written.
- Main-text words by the method of the length block: 18,780 at HEAD, 18,931 after the package (+151). By file: `sec3_measurement_setup.md` +10; `sec4_theory.md` +45; `sec10_discussion.md` +8; `sec11_limitations_ethics.md` +54; `declarations.md` +34.
- Files that change (12) and their sha256, HEAD -> after all blocks and steps (the writer's own computation; the ruling fixes the targets):

| File | sha256 at HEAD | sha256 after |
|---|---|---|
| `paper/V2_PROGRESS.md` | 873525d043c8565d | 42872dc943dab4e230ecaeb556302e93db6fb1d75102f8de64f9463354a6c77e |
| `paper/abstract_A.md` | 61fa852921d406e9 | cac8336212ace33d580bf36f94c4e9a23136531a9140e5baeaa13c8ca4ddb8bc |
| `paper/anon/declarations_anon.md` | 27b31182cab4c67a | b60846cf6607b63c4a5b867ca45463607dd2103165d9aef29d98bea0e024adcf |
| `paper/declarations.md` | a96c5d31ada50ccd | 63a224d405a28738215e2b9c1aca642d0f564d0ffcc2a31dd0461edc9f760e00 |
| `paper/number_manifest.tsv` | 14f12d297b63ab23 | d3ca0672f389ebd1621a49de625aa3d926e3603f0f78d7e1ae6881b1b2b41c8b |
| `paper/sec10_discussion.md` | 0b7137efc9a323f3 | 77ceb4083d5c1e39206f8badfabaa8651f6a6a4fb4af7627579035fa04e76a54 |
| `paper/sec11_limitations_ethics.md` | 912620f1a520b4fe | a28d835e62028e12549fb0224a47afabf2d8bda8f98f44035b4a5524f544b65e |
| `paper/sec3_measurement_setup.md` | e24a48620d6ea264 | bfc5c286c533b52d881899486ef1eef534dd43940d4028898adc98da9ae8bd8d |
| `paper/sec4_theory.md` | 9daa48f5f465fc60 | 50024781b9b1b658f1671db39c846a72863b5dcb2ce2506041d6943a612c1d01 |
| `paper/supplementary.md` | 497bf520564c025e | 5b77cd93390e12d9532187cae4fdb44dff6f406fbf673b07c36976656c6b13ec |
| `paper/supplementary_SPIC.md` | 711a98e45815c858 | f26f9209b02fa9071d47eb4dabf3270df690bb7cd85c9ce320e6d43865bdb47f |
| `paper/supplementary_provenance_internal.tsv` | b50eee90834a95e3 | 2add9e43ea3d0164462f6bad34dfc7b7028f4016014b01f392d5646e4d4e34fd |

### 7.3 The apply script

`apply_a_v2_1.py` in this folder reads the blocks from this file (pinned by sha256), rebuilds every changed file in memory from `git show HEAD:paper/<file>`, runs the steps S1 to S3 and the custody assertions, and prints the resulting sha256 values. In its default mode it writes nothing. It writes the files only with `--write --ruling <id>` and only if every result equals the target table inside the script, which holds the values of Section 7.2; if the judge drops or changes a block, the targets must be replaced by those of the ruling. It never stages or commits. It was run in the default (check) mode only, to test it; the write mode was not run.

### 7.4 What was opened for this package

- The five answers named above; ruling CC-403; the two LOG lines named above (found by their ids in `decisions/LOG.md`, l.2634 and l.2635).
- Run records: the two build reports, the two run folders (`adapter_config.json`, the first and last line of `metrics.jsonl`, the model card), the two training files (row counts, field names and image identifiers only; no caption was printed or copied), `data/datasets/ktvic/train_data.json` and `test_data.json` (keys and counts only).
- For CC-403 N2 and N3: `e1_x1pb_verification_v2.json`, `c1_b1_b6_reproduction.json` and `.py`, `c3_n2_exchangeability_all_datasets.json` and `.py`, `exch_full.json` and `exch_full.py`, `adjacency_check.py`.
- For the terms question: file names matching licence, terms or dataset card across the run repository (the two held Paper B folders were excluded from the search); `b3_licence_verification.json` and `licence_check_2026-10-15.json` (neither covers KTVIC); the lines on licence or terms of three of the group's own letter drafts (addresses not printed).
- The staged archive of 2026-10-21: file types, `README.md`, `FINAL_SCAN.json`, the key names of `BUILD_RECORD.json`, and the names of files with "ktvic" in them.
- `paperA.bib`: the KTVIC entry.
- Not opened: any label folder, `key.json`, `assignment.json`, label `.jsonl` files, the held Paper B folders, answers other than A1, A2, A3, A6 and F2. No network read was made for this package.
