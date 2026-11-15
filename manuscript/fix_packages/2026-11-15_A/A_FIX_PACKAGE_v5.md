# Paper A fix package v5

Written 2026-11-15T06:55Z (2026-11-15, 13:55 Vietnam time). Target journal of the paper: Signal Processing: Image Communication.

**What this file is.** Two proposed changes that a judge can rule on, and skip, separately: (1) the agreement clause of the KTVIC authors beside the KTVIC training sentence, in three places of the paper, and (2) a correction record to the PASCAL-50S registration (CC-407 W6). Each text change is an exact OLD/NEW pair with its evidence. Nothing has been applied, staged or committed. The package is outcome-free with respect to Section 6.7 and Supplementary S11: it quotes nothing from them, from the abstract body or from the highlights, so no `*_HELD.md` file was needed.

**Inputs.**
- Paper: `/mnt/d/vsps_papers/vsps-paperA-spic/paper/`, HEAD `59648b7` (group U of package v4 applied under CC-412). The working tree of `paper/` is clean.
- Plan `manuscript/KE_HOACH_GOAL_2026-11-15.md`, task 6, third step.
- Ruling `CC-407`, revised text, read in full (Ruling 1, Ruling 2, W6, N9). Ruling `CC-412`, read up to the line before its last section (Ruling 3, the carried W6, N1, N4); its last section was not read.
- Decisions LOG `.session_backup/2026-10-13/decisions/LOG.md` (2,668 lines), searched for the investigator's lines on dataset agreements: PI-1026az (l.635), PI-1110o (l.2072), PI-1115i (l.2662); also OPS-1115g and OPS-1115h (l.2642, l.2645). `manuscript/directions/integrity_2026-11-10/FIX_RESOLUTIONS_2026-11-10.md` l.33 (F-19).
- Registration `manuscript/prereg/2026-10-28_pascal50s/PREREG.md` (sha256 1448ab13fcb5..., commit `353437f`), l.105-113 and l.375-381 only. Its copy in the paper repository, `prereg/2026-10-28_pascal50s/PREREG.md`, has the same sha256.
- Not opened: any label folder, key file, label file, `gt_cache.json`, `b_text_held`, `b_result_snapshot`, CC-394.txt, CC-396.txt. Of `sec7_verbosity_sign.md`, both supplement files and `abstract_A.md`, only the parts before `## 6.7`, before `## S11` and before `## Abstract` were displayed; `highlights_A.md` was not displayed. The script reads those files whole, to compare bytes and to count words, and prints none of their text.

**The two groups.**
- **Group K (KTVIC agreement clause; PI-1115i item 8).** 3 items, 4 blocks. The clause "one of us contacted the KTVIC authors, who agreed to this use" is put directly after the KTVIC training sentence in `declarations.md`, `anon/declarations_anon.md` and Section 9.2 (`sec11_limitations_ethics.md`). It is the form the paper prints for UIT-OpenViIC, with the dataset name changed. No "in writing", no date, no "on file", no licence or terms wording. No existing agreement clause is touched.
- **Group R (CC-407 W6; correction record).** 1 item, no block. A new file, `CORRECTION_PASCAL50S_2026-11-15.md` in this folder, to be placed beside the registration (Section 4). The registration file is not edited.

Section 6.7, Supplementary S11, the abstract body and the highlights stay byte-unchanged; the script asserts it. Neither supplement file, `sec7_verbosity_sign.md`, `highlights_A.md`, the cover letter nor the title page is written.

## 1. Counts

- 4 blocks, all in group K: `declarations.md` 2 (`a` printed text, `b` an unprinted comment that would otherwise become untrue), `anon/declarations_anon.md` 1, `sec11_limitations_ethics.md` 1.
- 1 step that is not a block: S3, the length comment of `abstract_A.md` (before `## Abstract`; the abstract body is not touched).
- 1 new file (group R), placed at two paths in write mode (Section 4).
- Deferred: 6 items (Section 6.1). For the judge: 6 points (Section 6.2). For the investigator: nothing.
- Main text: 19,241 words at HEAD; +24 (12 in `declarations.md`, 12 in Section 9.2); 19,265 after the package.

## 2. Table of blocks

| Id | Group | Source | File | Line at HEAD | What changes |
|---|---|---|---|---|---|
| A5-K01a | K | PI-1115i (8) | `declarations.md` | 19 | Data availability: agreement clause added after the KTVIC training sentence |
| A5-K01b | K | PI-1115i (8); CC-412 N4 | `declarations.md` | 19 | Unprinted comment: "no agreement clause is printed" for KTVIC replaced by the history of the clause |
| A5-K02 | K | PI-1115i (8) | `anon/declarations_anon.md` | 10 | Anonymised copy: same clause, with an unprinted comment |
| A5-K03 | K | PI-1115i (8) | `sec11_limitations_ethics.md` | 48 | Section 9.2, paragraph KTVIC: same clause as its own sentence, with an unprinted comment |

## 3. Blocks

Each OLD string is given exactly as it stands in the file at HEAD, and each NEW string exactly as it should stand. A marker line is not part of a string; the string is the text between two marker lines, without the line break before the next marker. Every string is a single line. A5-K01a and A5-K01b go together or not at all.

### Group K: the agreement clause of the KTVIC authors

<<<A5-K01a declarations.md OLD>>>
Two adapters of the first backbone (Section 6.2) were trained on the KTVIC training split (its 3,769 images, with captions of that split as training targets); no KTVIC image or caption and no trained adapter weight is part of the release.
<<<A5-K01a declarations.md NEW>>>
Two adapters of the first backbone (Section 6.2) were trained on the KTVIC training split (its 3,769 images, with captions of that split as training targets); one of us contacted the KTVIC authors, who agreed to this use; no KTVIC image or caption and no trained adapter weight is part of the release.
<<<A5-K01a EVIDENCE>>>
Decision: LOG l.2662, PI-1115i (2026-11-15T03:43:33Z), the investigator's typed words for item 8: "Số 8 tôi đồng ý."; read in the same line as "(8) the acceptance he received from the KTVIC authors covers the training (coordinator reading of "đồng ý" to the question as asked; restoring an agreement clause beside the KTVIC training sentence goes through a judge read)". Form: LOG l.2072, PI-1110o (2026-11-10T13:48:07Z): "the PI states that the dataset authors' acceptance HAS been confirmed, and that this is all the coordinator needs to know (no document will be filed in the repo). [...] the papers state the agreement as a fact ('One of us contacted the ... authors, who agreed to this use'); the words 'in writing', the date 2026-10-28 and 'on file with the corresponding author' are NOT written by the coordinator, because their form and date are known only to the PI; the PI may restore them in the rewrite if they are accurate. Item closed; no further question to the PI on it." First record: LOG l.635, PI-1026az (2026-10-28), "PI verbatim: "Cứ làm đi, tôi liên hệ riêng và họ accpeted rồi"): the PI contacted privately and received acceptance from (1) PASCAL-50S authors [...] (2) UIT-OpenViIC and (3) KTVIC authors -> data use / pointer release confirmed for B and C" (two names left out at the first mark). Model of the clause, same paragraph of this file at HEAD: "UIT-OpenViIC is used only through aggregates and pointers; one of us contacted the UIT-OpenViIC authors, who agreed to this use." The new clause is that clause with the dataset name changed, and nothing else. Place: directly after the training sentence, so that "this use" is the training on the training split (two adapters, 3,769 images, captions of that split as targets), which is what PI-1115i (8) covers; the clause on what is not released follows it unchanged. History: until commit `dafba17` this paragraph printed "one of us contacted the UIT-OpenViIC and KTVIC authors, who agreed to this use" for use through aggregates and pointers; CC-407 (revised) Ruling 1 took the KTVIC half out when the stated use came to include training, because no record then showed that the training had been put to the KTVIC authors, and said a scoped clause can come back when the record shows what was agreed. The record now is the investigator's decision PI-1115i (8). Not written: "in writing", a date, "on file", any licence or terms wording (asserted by the script: the printed text of the file after the block equals the printed text before it plus exactly this clause). Existing clauses: the UIT-OpenViIC clause and the PASCAL-50S clause of this file are outside the OLD string and are counted before and after by the script.

<<<A5-K01b declarations.md OLD>>>
for KTVIC no agreement clause is printed since CC-407, where the stated use includes training (CC-407 N9);
<<<A5-K01b declarations.md NEW>>>
for KTVIC the agreement clause left under CC-407 Ruling 1, when the stated use came to include training, and returned beside the training sentence on PI-1115i item 8 (LOG.md, 2026-11-15: the PI states that the acceptance he received from the KTVIC authors covers the training);
<<<A5-K01b EVIDENCE>>>
Unprinted comment (inside `<!-- -->`; the script asserts that the printed text of the file is the same before and after this block). After A5-K01a the old comment would say that no KTVIC agreement clause is printed, which would be untrue. The new text gives the history: out under CC-407 (revised) Ruling 1, back under PI-1115i item 8 (LOG l.2662, quoted in A5-K01a). It also closes CC-412 N4, which asked that this comment cite Ruling 1 and not N9 at the next touch of the file. The rest of the comment (PI-1026az, PI-1110o, "no document is filed in the repo, so the text states the agreement as a fact without "in writing", a date or "on file"") is unchanged.

<<<A5-K02 anon/declarations_anon.md OLD>>>
Two adapters of the first backbone (Section 6.2) were trained on the KTVIC training split (its 3,769 images, with captions of that split as training targets); no KTVIC image or caption and no trained adapter weight is part of the archive.
<<<A5-K02 anon/declarations_anon.md NEW>>>
Two adapters of the first backbone (Section 6.2) were trained on the KTVIC training split (its 3,769 images, with captions of that split as training targets); one of us contacted the KTVIC authors, who agreed to this use; no KTVIC image or caption and no trained adapter weight is part of the archive.<!-- PI-1115i item 8 (LOG.md, 2026-11-15): the PI states that the acceptance he received from the KTVIC authors covers the training; stated as a fact, no document is filed in the repo (PI-1110o) -->
<<<A5-K02 EVIDENCE>>>
Decision and form: PI-1115i (8), PI-1110o and PI-1026az, as quoted in A5-K01a (LOG l.2662, l.2072, l.635). The anonymised copy repeats the data statement of `declarations.md` in shorter form and differs from it here only in "archive" for "release". Anonymised form: "one of us" names no person, role, institution or date, so the clause is the same as in `declarations.md`. The anonymised copy prints no agreement clause for another dataset (it sends the reader to Section 9.2 for UIT-OpenViIC), so no existing clause is touched. The comment is unprinted; the head comment of the file says that all comments are stripped when the upload file is built. For the judge: point J-3 (this block can be skipped alone).

<<<A5-K03 sec11_limitations_ethics.md OLD>>>
**KTVIC.** Two adapters of the first backbone (Section 6.2) were trained on the KTVIC training split (Pham et al., 2024): its 3,769 images, with captions of that split as training targets. No KTVIC image or caption and no trained adapter weight is part of this paper's release.
<<<A5-K03 sec11_limitations_ethics.md NEW>>>
**KTVIC.** Two adapters of the first backbone (Section 6.2) were trained on the KTVIC training split (Pham et al., 2024): its 3,769 images, with captions of that split as training targets. One of us contacted the KTVIC authors, who agreed to this use. No KTVIC image or caption and no trained adapter weight is part of this paper's release.<!-- PI-1115i item 8 (LOG.md, 2026-11-15): the PI states that the acceptance he received from the KTVIC authors covers the training; stated as a fact, no document is filed in the repo (PI-1110o) -->
<<<A5-K03 EVIDENCE>>>
Decision and form: PI-1115i (8), PI-1110o and PI-1026az, as quoted in A5-K01a (LOG l.2662, l.2072, l.635). Model of the clause, Section 9.2 of this file at HEAD (l.44): "One of us contacted the UIT-OpenViIC authors, who agreed to this use; we have not received written permission from the UIT-ViIC authors (Lam et al., 2020)." The new sentence is its first clause with the dataset name changed, set as its own sentence directly after the training sentence, so that "this use" is the training. The UIT-OpenViIC clause of l.44 is in another paragraph and is not touched (counted before and after by the script). The comment is unprinted and follows the form of the comment at the end of l.44.

## 4. Group R: correction record to the PASCAL-50S registration (CC-407 W6)

**The file.** `manuscript/fix_packages/2026-11-15_A/CORRECTION_PASCAL50S_2026-11-15.md`, sha256 in Section 7.2. It states (1) what the registration says: section 1.4 l.109, "Written confirmation from the dataset authors was obtained (2026-10-28; on file with the corresponding author)", and the same clause in the disclosure sentence of l.113; (2) what the record is: PI-1026az and PI-1110o, and that the search of CC-407 found no saved reply; (3) what the paper prints: "the dataset authors were contacted by one of us and agreed to this use", without "in writing", a date or "on file"; (4) what does not change; (5) what would restore the registered wording (CC-407 Ruling 2 (b)). It names no person, address or host and quotes no result.

**Evidence.** CC-407 (revised) Ruling 2, item W6: "Before submission, either (b) is done for PASCAL-50S, or a disclosed correction record states that the confirmation was the PI's statement (PI-1026az, PI-1110o)." CC-412, carried items: "Under the CC-407 lesson, no new question goes to the PI on this. CC-407 Ruling 2 allows a route that needs no question [...] Prepare that record before submission". LOG l.635 (PI-1026az) and l.2072 (PI-1110o), as quoted in A5-K01a; in l.635 the words "disclosure becomes 'written confirmation obtained'" stand outside the investigator's quoted words. Registration lines read: l.105-113.

**Path (the rulings leave it open).** Proposed, both written by the script in write mode, byte-equal to the file above, and only if the path is free:
1. run repository: `manuscript/prereg/2026-10-28_pascal50s/CORRECTION_2026-11-15.md`;
2. paper repository: `prereg/2026-10-28_pascal50s/CORRECTION_2026-11-15.md`, beside the copy of the registration that goes into the release archive. This is what makes the record "disclosed".

The registration file is not edited at either path; the script asserts its sha256 at both.

## 5. OLD occurs once

Counted by the script in `git show HEAD:paper/<file>` (HEAD `59648b7`).

| Id | File | OLD at HEAD | NEW at HEAD | NEW after the package |
|---|---|---|---|---|
| A5-K01a | `declarations.md` | 1 | 0 | 1 |
| A5-K01b | `declarations.md` | 1 | 0 | 1 |
| A5-K02 | `anon/declarations_anon.md` | 1 | 0 | 1 |
| A5-K03 | `sec11_limitations_ethics.md` | 1 | 0 | 1 |

Agreement clauses, counted as the string "agreed to this use" in the printed text (comments stripped): `declarations.md` 2 at HEAD (UIT-OpenViIC, PASCAL-50S), 3 after; `anon/declarations_anon.md` 0, 1 after; `sec11_limitations_ethics.md` 1 (UIT-OpenViIC), 2 after. Every clause printed at HEAD is printed after the package.

## 6. Not in this package

### 6.1 Deferred

1. **CC-412 N1 (deferred to the rewrite; no block).** The registered branch text for the outcome reported in Section 6.4 has three sentences: `manuscript/prereg/2026-10-28_pascal50s/PREREG.md`, section 9.2, l.379. Its third sentence, which begins "The images and captions have been public since 2008–2015", is not printed in Section 6.4 (`sec7_verbosity_sign.md` l.86, before `## 6.7`), and the paragraph does not say so. CC-412 N1: at the rewrite either restore the sentence or record the deviation, at least in the source comment of the paragraph and in the S4 deviation notes; the same check is due for the branch text of the COCO val2017 test. Both places lie in files this package does not write.
2. **CC-407 W5** (internal terms and leak hits of S11): with the S11 update, after the release of the held study.
3. **Section 6.7 and S11 text, abstract, highlights, cover letter**: later steps of task 6.
4. **A line in Supplementary S7** ("Departures from the PASCAL-50S registration") that points to the correction record: optional; it would change both supplement files and the provenance table, so it belongs to the S11 package, which writes them anyway (J-5).
5. **`PROVENANCE.md` row** of the paper repository for the new file under `prereg/`: it needs the commit id of the run repository, so it is written by the gatekeeper after that commit.
6. **CC-407 N8** (keep or retire the anonymised copy): carried unchanged.

### 6.2 For the judge

- **J-1 (the decision against CC-407 Ruling 2 (c)).** Ruling 2 (c) said the KTVIC clause returns beside the training sentence with a saved reply whose accepted use covers the training. No reply is saved. What exists is the investigator's decision PI-1115i (8), newer than the ruling, that the acceptance he received covers the training. The package follows the rule of the revised CC-407 itself: the newest decision of the investigator on the point stands, and PI-1110o fixed that no document is filed and that the agreement is stated as a fact. The judge rules whether PI-1115i (8) takes the place of the saved reply for the fact form. For "in writing", a date or "on file", Ruling 2 (b) stays as it is; none of them is written here.
- **J-2 (what the investigator was asked).** The LOG line gives his answer ("Số 8 tôi đồng ý.") and the coordinator's reading of the question. The text of the twelve points as put to him was not found in the LOG. If the judge needs the question itself, the coordinator supplies it.
- **J-3 (anonymised copy).** `anon/declarations_anon.md` prints no agreement clause for another dataset, so A5-K02 has no model inside that file. It is written so that the two data statements agree. To skip it: `SKIP = ("A5-K02",)`; the target of that file then falls away and the others hold.
- **J-4 (the referent of "this use").** In all three places the clause follows the training sentence directly. In `declarations.md` and the anonymised copy the parenthesis and a semicolon stand between "trained on the KTVIC training split" and the clause; the judge may prefer a full stop, as in Section 9.2.
- **J-5 (the correction record).** Path, the two copies, and whether the record needs a pointer in Supplementary S7 before submission or whether its place beside the registration in the archive is disclosure enough.
- **J-6 (length).** +24 words of main text; the text is 10,765 words over the limit of 8,500 used in the length comment. Left to the cut plan.

## 7. Script, pins and targets

### 7.1 Script

`manuscript/fix_packages/2026-11-15_A/apply_a_v5.py`.
- Check mode (default; nothing written): `python3 -I -B apply_a_v5.py`
- Write mode: `python3 -I -B apply_a_v5.py --write --ruling <id of the GO ruling>`: writes four files to the working tree of the paper repository and the correction record to its two paths. It never runs `git add` or `git commit`.
- With a block skipped by the ruling, set `SKIP` and replace `TARGETS` by the values the ruling fixes.

Assertions: pins of this file and of the record; `59648b7` is HEAD or an ancestor; clean `paper/` tree; base sha256 of the eight files read; each OLD once; printed text after each block equals printed text before it plus exactly the clause (group K `a`, 02, 03) or equals it (K01b); no agreement clause printed at HEAD is lost; `abstract_A.md` unchanged from `## Abstract`; `sec7_verbosity_sign.md`, `highlights_A.md`, both supplement files, the cover letter and the title page not written; no run of eight words from Section 6.7, S11, the abstract body or the highlights occurs in this package, in the record or in the script; registration sha256 at both paths.

### 7.2 Pins

| Object | sha256 |
|---|---|
| `CORRECTION_PASCAL50S_2026-11-15.md` | `465ad1b6828d7eb3117ced13717e4a216474e51308581b0c3fc2b616f324b038` |
| `PREREG.md` of PASCAL-50S (both repositories; not edited) | `1448ab13fcb509b4f6dff1e15344809f529478f6606df8880498427153c2db3b` |

The sha256 of this package file is pinned in the script and reported with the script's own sha256 in the hand-over message.

### 7.3 Targets (files after the package; SKIP empty)

| File under `paper/` | sha256 at HEAD `59648b7` | sha256 after the package |
|---|---|---|
| `abstract_A.md` | `38300b3f79fa5a3119dc9ec12f16e39005aa0eeefabe8d4ce02434f3489c41fd` | `b566eb8e8f4ca29d9ccc5383c987aca53bd54678cddd414e68836d81c7c29752` |
| `anon/declarations_anon.md` | `ec71a9b953ab3609a31f457b8368814c35a82443035885cfa64d9d8df84a96cb` | `e407d32ddd13b2903482472e35cf011e71177ea23f271425e9e38f60ee5172ca` |
| `declarations.md` | `5920d0fa7461f0a75cd6aae6d58df7e7588111ba9ad39ff76e1aa3af4c4702ba` | `3b2381ca23d22682dd431dfed5c7a738c2ae41bf55356fa5291b23c6a598b5d2` |
| `sec11_limitations_ethics.md` | `a7258f2eddb6e137d6abe6990063ce2cc8a4e8e57c9e6bddcef6161e54d2a1e4` | `dff441d598ae945c459dfbc348d2dd51e2a8c2a2621a62a781c0d6836d74a34f` |

Read and not written (sha256 at HEAD, asserted): `sec7_verbosity_sign.md` `b6f46b8aaf33ef133b54e5e4d91f2c1f037e061d48f495e1b23eed5b0aaf4817`; `highlights_A.md` `64c671615bd5106cba42cf168ff7ff85460bd9bd72b3c52a2d9903861c281aa5`; `supplementary.md` `dd7277069ced9d4d66c2b57e933d06a9b05cc41aae546b5cefa0c10ddcccc2ee`; `supplementary_SPIC.md` `0c746c2127cac8bcb25340172e3859cc3c023d4739e7e8d812967287e554f280`.

**S3. Length comment of `abstract_A.md`** (an HTML comment before `## Abstract`). Four replacements, each on a string that occurs once: "recounted after fix package v4 of 2026-11-15)." gains "; recounted after fix package v5 of 2026-11-15" before the bracket; "Main text now: 19,241 words" becomes "Main text now: 19,265 words"; "Over the limit by 10,741 words." becomes "Over the limit by 10,765 words."; the line "Longest files:" is rebuilt from the counts (`sec11_limitations_ethics.md` 2,128 becomes 2,140 if it stays among the three longest). The counts are computed by the script with the method named in that comment.
