# Blind pairwise caption preferences for Paper B (FE-CERT human arm): labelling plan v1.1 (2026-11-12). DRAFT, not approved

> **Changes from v1.** v1 = `B_PREF_LABELLING_PLAN_v1.md`, sha256 `22c38a7fe4e088399863c1ee7b6448df10a40c2faeda97fd83768e3786f2b063`. Ruling: CC-350 (`.session_backup/2026-10-13/decisions/CC-350.txt`, sha256 `f4e05e266059340636cdef47b49f7e0b4e7b9e4d4ce4d2a4f417995370eda493`), NEXT_ROUND. Built by `build/build_v1_1.py` from v1 with exact-once replacements. Every replacement text that CC-350 gives is copied from the CC file as written (its ASCII `<=`, `x`, `F+` and `Clopper-Pearson` kept); where it goes into a table, it is placed in the table's cells. Nothing else changed.
> - **W6** (13 of the 558 test images are `.png` or `.jpeg`): §2.1 image path; §9 pair_server item 2 (route regex, served only if listed, content type); §9 build_pairs `--selftest` addition.
> - **W7** (collision with the live Paper A labelling): the §6 label folder became `~/vsps_labels_b/b_pref/` in both places, not under `~/vsps_labels/`; the custody rules of §6 apply there; §9 pair_server item 6 (port 8791; port 8790 refused).
> - **W4** (thresholds fixed): the proposal tags are removed with the values kept (§2.2 ε = 10.0; §5.4 κ ≥ 0.40), both ruled yes (plan Q3, Q4).
> - **Rulings**: "Rule status" (ruling 9(a): the screens are inside PI-1111n/o); §2.1 (Q2: no); §3.1 (Q1: yes); §11 (the CC-350 rulings are recorded below the table).
> - **N2** (via plan Q3): quotas P 100, U 160, C 40 in §2.4 step 3, §5.2 H-P and §5.3; §7 unchanged (the U gate stays 100).
> - **Version**: title v1.1; companion file name points to `B_FECERT_PREREG_v1_1.md`.
> - Not applied in v1.1 as first built (non-blocking): N6, N8. **CC-353 round-2 fixes**, applied afterwards in place and byte-checked against CC-353: §9 pair_server item 6 (port 8792; ports 8790 and 8791 refused; one rating server at a time; start only after the XM3600-600 base labelling is finished, REDESIGN_B D1 and CC-350 ruling 13(7), with the trigger defined; CC-353 W8); §10 citation (N8); §11 note.

Drafted before the `date -u` reading 2026-11-11T23:21:54Z, revised up to 2026-11-12T02:31:06Z (2026-11-12 in Vietnam), by a writer agent, with `B_FECERT_PREREG_v1_1.md` (this folder). AI-designed; recommendations are opinions. Nothing has been built or collected. "unverified" = not checked today.

**Scope.** How the preferences are collected, kept and analysed. This file registers the human hypotheses H-P and H-U **and their analysis**, so that the analysis is fixed before any judgement exists (PI-1111n, PI-1111o). No separate analysis registration follows. Nothing may be collected before this file, the prereg and the code are judge-read and committed.

**Rule status.** This is the third human-labelled set (PI-1111n: "Quyết là có bộ nhãn người thứ ba"; PI-1111o). AI judgements are not evidence and are not used anywhere in this arm. No other human data (FAIR 2026 ratings: PD-21b) is used. CC-350 ruling 9(a): "300 distinct pairs, 30 hidden repeats and 8 practice screens are INSIDE PI-1111n/o (about 300 pairs, two raters). The repeats are within-rater reliability screens, not new items."

---

## 1. What is judged and why

- **Unit.** One KTVIC test image and two captions of it, written by two different own systems. Question (Vietnamese on the page): **"Chú thích nào mô tả bức ảnh tốt hơn?"** ("Which caption describes the image better?"). Answers: **A** (caption A is better), **B** (caption B is better), **T** Ngang nhau (tie: no meaningful difference), **X** Không đánh giá được (cannot judge: the image cannot be seen well enough, or neither caption can be understood).
- **Why.** The certificate says whether a comparison survives every admissible front end; it does not say which front end agrees with people when they disagree. Pairs whose per-image CIDEr-D order flips between two members isolate exactly that disagreement. The answer sets only the member the paper recommends for reporting (prereg §6.5). It never changes a certificate.
- **What is new.** Only the judgements. The images, references and captions were analysed before (development data, spent KTVIC test set). Every result is described as "new human judgements on previously analysed captions", registered before any judgement was made.

## 2. Items

### 2.1 Pool (fixed now)

- Images: the 558 KTVIC test images (`data/datasets/ktvic/test_data.json`; image files `data/datasets/ktvic/images/<filename>`, `filename` from `test_data.json :: images` (545 `.jpg`, 7 `.png`, 6 `.jpeg`)).
- Captions: the 33 own `-short` files of the KTVIC test (prereg §4.1; names in `SYSTEMS.tsv`). Short captions keep a judgement near 20 seconds.
- **Not shown to any rater:** the `-detailed` and `-two` files; the two KTVIC baselines, K1, K2 and every first-look file (no licence or aggregate-use-only for most of them; and the first-look files must stay unscored by people too). §11 Q2 asked whether the baselines may be added; CC-350 ruled no.
- A candidate is (image i, files a, b) with: a and b in different families (B_KAPPA §4.3 rule); both display texts (§3.1) non-empty; the display texts differ in at least 2 syllable tokens (size of the multiset symmetric difference of their lower-cased whitespace tokens ≥ 2).

### 2.2 Members used to define flips (all in F_dev; scores from prereg stage 1)

| Name | Member (U, T, P, C) |
|---|---|
| m_syl | (`syl`, tw, pa, cf) |
| m_word | (`rdr`, tw, pa, cf) |
| m_pk | (`rdr`, tw, pk, cf) = f0 |

d_m(i, a, b) = per-image CIDEr-D of a minus that of b on image i under member m (×100; document frequencies from all 558 images' references under m). Margin ε = 10.0: a difference counts only when |d_m| ≥ ε.

### 2.3 Strata (one candidate belongs to at most one)

| Stratum | Condition | What it isolates |
|---|---|---|
| **P** punctuation flip | sign d_{m_pk} ≠ sign d_{m_word}, both |d| ≥ ε; and **not** a unit flip | punctuation kept against removed, unit fixed at RDR words |
| **U** unit flip | sign d_{m_syl} ≠ sign d_{m_word}, both |d| ≥ ε; and **not** a punctuation flip | syllables against words, punctuation fixed at removed |
| **C** control | d_{m_syl}, d_{m_word}, d_{m_pk} all of one sign, all |d| ≥ ε | uncontested pairs: the base rate of human agreement with the metric |

### 2.4 Sampling (seed 20261112; counts fixed now)

1. Stage 1 writes `PAIR_CANDIDATES.json`: for every image, the candidates of each stratum, by file names and the three d values. No caption text. Its counts per stratum (number of eligible images) are logged before sampling.
2. `rng = random.Random(20261112)`. Image sets are sorted by id before every draw; candidate lists are sorted by (a, b).
3. **P**: draw min(100, |E_P|) images from E_P (images with at least one P candidate). **U**: from the images not yet drawn, draw min(160, |E_U|) from E_U. **C**: from the images not yet drawn, draw min(40, |E_C|) from E_C. One image gives one pair; images are disjoint across strata. Quotas P 100, U 160, C 40 (CC-350 N2).
4. For each drawn image, one candidate of its stratum by `rng.choice`.
5. **Shortfall.** If a stratum has fewer eligible images than its quota, all are taken and the shortfall is logged. Quotas are never moved between strata.
6. **Side.** For each pair, `rng.random() < 0.5` puts file a on the left (caption "A"); the side is stored in the key only.
7. **Order.** The ≤ 300 pairs are shuffled with `rng`.
8. **Repeats.** 30 pairs drawn with `rng.sample` from the main pairs are shown again, with sides swapped, each at a random position at least 100 screens after its first showing. Repeats are hidden (no part label). Total ≤ 330 screens.
9. **Practice.** 8 pairs from images not drawn above (any stratum), shown first, no feedback, not data.

Expected time: about 20 seconds per screen, so about 2 hours per rater including practice.

## 3. Blinding and display

### 3.1 Display normalisation (applied to both captions of every pair)

N of the prereg §2.1 (NFC, underscore to space, whitespace collapsed and trimmed); then the maximal trailing run of final punctuation and whitespace removed (κ step 5); then the first character upper-cased if it is a letter. Nothing else is changed.

**Why.** A final period and lower-case starts mark zero-shot against fine-tuned systems and are exactly what the punctuation member scores. People judge content; showing the marks would let a rater who knows the study guess the stratum or the system. Residual cues (length, vocabulary, internal commas, the KTVIC style of fine-tuned outputs) remain and are disclosed. CC-350 confirmed this choice (ruling 9(c); §11 Q1).

### 3.2 What the page shows and hides

- Shows: the image (click opens it full size), caption A and caption B (as plain text; never as HTML), the question, four buttons, overall progress "cặp i/N".
- Hides: system names, families, prompt modes, strata, members, scores, which screens are repeats, which are controls, and any per-stratum progress.

## 4. Raters and instructions

- **Raters.** Two: the PI (code `PI`) and one colleague (code `R2`), preferably not an author and not familiar with the study's files (prereg §17 PI-1). Both judge every main pair and every repeat, independently, with the same page and instructions, after the practice round. They do not discuss items until both have finished.
- **Disclosure, wherever the judgements are used:** "One rater is an author (the PI), who knows the study's hypotheses but could not see which system or front end produced a caption." If R2 is also an author: "Both raters are authors."
- **Instructions (shown on the page, Vietnamese; English gist here).**
  1. Judge which caption describes the image better, using only what you see in the image.
  2. First, correctness: a caption that names an object, person, action, number, colour or place that is not in the image is worse.
  3. Then, coverage: among correct captions, the one that states more of the image's main content is better.
  4. Ignore spelling of tone marks, capitalisation, spacing and punctuation.
  5. Choose **Ngang nhau** when the two are equally good or equally bad, or differ only in wording. Choose **Không đánh giá được** only when the image or both captions cannot be understood.
  6. Keys: 1 A, 2 B, 3 Ngang nhau, 4 Không đánh giá được; Enter next; Backspace previous.

## 5. What the judgements may estimate (fixed before any judgement exists)

### 5.1 Mapping and the decisive unit

- Each answer is mapped through the key from screen side to caption identity: prefers a, prefers b, tie, cannot.
- For a main pair, each rater's answer on its **first showing** (the main screen, not the repeat screen, which has its own qid) is used; if the rater changed that answer, the last line for that qid in the label file wins (the server's rule). Repeat screens are used only for within-rater agreement.
- **Decisive pair (consensus):** both raters prefer the same caption. Every other pair (split preference, any tie, any cannot, any missing) is not decisive and is counted by reason.

### 5.2 Hypotheses

| Id | Stratum | Statistic | Test | Labels |
|---|---|---|---|---|
| **H-P** | P | q_P = share of decisive pairs whose preferred caption is the one m_word (punctuation removed) ranks higher | exact binomial, one-sided, H1: q_P > 0.5 | Holm-rejected: **SUPPORTED** ("removing punctuation gives the order people prefer in q_P of decisive pairs"). Not rejected with n_dec ≥ 47: **NOT SUPPORTED**. Not rejected with n_dec < 47: **UNDERPOWERED** (47 = decisive pairs for 80% power at a true share of 0.70, one-sided 0.025, §5.3; reachable with the quota of 100) |
| **H-U** | U | q_U = share of decisive pairs whose preferred caption is the one m_word (words) ranks higher; 1 − q_U is the syllable share | exact binomial, two-sided, against 0.5 | Holm-rejected: **WORD AGREES MORE** or **SYLLABLE AGREES MORE**. Otherwise, if the 90% Clopper–Pearson interval lies inside [0.40, 0.60]: **EQUIVALENT within ±0.10**. Otherwise: **INCONCLUSIVE** (with n_dec) |

- **Direction of H-P, fixed now:** people judge content and the display removes final punctuation, so the member that removes punctuation is expected to agree more. H-U has no registered direction.
- **Multiplicity:** Holm over the two p-values at family-wise 0.05.
- **Estimates:** q_P and q_U with Clopper–Pearson 95% intervals, always reported, whatever the label.

### 5.3 Power (two-sided unless stated; 80% power; normal approximation to the sign test; computed 2026-11-12 by the writer)

| True share | Two-sided 0.05 | Two-sided 0.025 (Holm first step) | One-sided 0.025 |
|---|---|---|---|
| 0.60 | 194 | 236 | — |
| 0.65 | 85 | 103 | 85 |
| 0.70 | 47 | 57 | 47 |

REDESIGN_B §1(d) gave one-sided values; these replace them. If about 55% of pairs are decisive (unverified), U gives about 88 decisive pairs and P about 55 (quotas of CC-350 N2): H-P can detect a share near 0.70 (47 needed); at 88, H-U detects a share of about 0.65 only at two-sided 0.05, not at 0.025 (103). So a NOT SUPPORTED for H-P rules out a share of 0.70 or more, not a smaller effect. EQUIVALENT within ±0.10 needs about 215 decisive pairs at a true 0.50 (REDESIGN_B), so it is unlikely; INCONCLUSIVE is the probable null outcome for H-U and is reported as such.

### 5.4 Agreement and reliability

- **Inter-rater, primary:** Cohen's κ (unweighted), three categories (prefers a, prefers b, tie) on caption identity, over main pairs where neither rater chose cannot; 95% interval by a bootstrap over pairs (2,000 draws, seed 20261112).
- **Beside it:** raw agreement; Gwet's AC1; κ on two categories over pairs both raters decided; each rater's tie and cannot rates; κ per stratum.
- **Within rater:** agreement of each rater's repeat answers with their first answers (raw and κ, three categories), side swap undone.
- **Rule.**
  - κ ≥ 0.40: H-P and H-U carry the labels of §5.2.
  - 0.20 ≤ κ < 0.40: the hypotheses are reported without labels, with the words "low inter-rater agreement", and each rater's own shares are reported beside the consensus.
  - κ < 0.20: the human arm is NOT_EVALUABLE; counts only.
  - Until R2 has finished, every number carries "single rater" and no label.

### 5.5 Rows beside the hypotheses (no verdict)

- **Non-author rater alone** (or "R2 alone" if R2 is an author): the same shares and tests on R2's decided pairs (A or B), named first when the consensus and this row disagree in label.
- **Author rater alone:** the same on the PI's decided pairs.
- **Controls (stratum C):** share of decisive control pairs whose preferred caption is the one all three members rank higher, with its interval: human agreement with the metric on uncontested pairs, the yardstick for q_P and q_U.
- Agreement shares by margin bin (|d| below or above the median of the stratum).

### 5.6 Not estimated

Which system is better; system-level orders; the validity of CIDEr-D in general; anything about front-end members other than m_syl, m_word and m_pk; anything about another language.

## 6. Custody

- **Where files live.** `~/vsps_labels_b/b_pref/` on the laptop's Linux home filesystem (never under /mnt, not under `~/vsps_labels/`; CC-350 W7): `assignment.json` and `practice.json` (served; **they contain caption text**), `key.json` (private: qid → image, stratum, file left, file right, the three d values, repeat-of), `labels_PI.jsonl`, `labels_R2.jsonl`, `practice_<rater>.jsonl` (append-only, fsync per answer; a changed answer is a new line; all lines kept).
- **Never committed:** `assignment.json`, `practice.json`, `key.json`, any label file before the closing line, any file with caption text. Committed in the pin package: the code, `ITEMS_MANIFEST.tsv` (qid and image id only) and `BUILD.json` (counts and the sha256 of every input and output). `key.json` is committed only after the closing line (its sha256 is logged at build time).
- **Build.** `build_pairs.py` runs on the rented host from the stage-1 candidate table and the own `-short` files; the outputs are copied to `~/vsps_labels_b/b_pref/` with sha256 checked on both sides, and deleted from the host after the check.
- **Who sees what.** The raters see only the page. The PI, as a rater, does not open `key.json`, `assignment.json`, `PAIR_CANDIDATES.json` or `BUILD.json` counts per stratum. Agents read only `wc -l` and sha256 of label files until the closing line; nobody is shown a per-stratum, per-rater or control figure before it.
- **Session lines.** At the end of each session a LOG line records the UTC time, `wc -l` and sha256 of the rater's label file, a 444 copy `labels_<rater>.<UTC>.jsonl` with the same sha256, and the sha256 of `assignment.json`, `key.json`, `pair_server.py` and `pair.html` (unchanged).
- **Closing line.** When both raters have finished, or at 2026-11-15 18:00 VN, whichever is first, a LOG line closes the labelling with the final hashes. Only then are the 444 copies pushed to the host (sha256 checked) for stage H, which writes `HUMAN.json` (counts and statistics only, no caption text).
- The custody rules of plan §6 apply to `~/vsps_labels_b/` in the same way.

## 7. Evaluability and kill gates

| Condition | Consequence |
|---|---|
| fewer than 100 eligible images in U (stage-1 count, before sampling) | H-U NOT_EVALUABLE; the U pairs drawn are still judged and reported as counts |
| fewer than 40 eligible images in P | H-P NOT_EVALUABLE; likewise |
| R2 has not finished by the closing line | single-rater wording; no labels; the PI's answers reported as "single rater (an author)" |
| κ < 0.20 | §5.4 |
| page or server fault that loses an answer (a qid acknowledged on screen but absent from the file) | the session stops; the fault and the count are logged; affected qids are re-asked at the end of the queue |

## 8. What is reported under each outcome

| Outcome | Text |
|---|---|
| H-P SUPPORTED | "On pairs whose order changes with punctuation handling, the order with punctuation removed matched both raters' choice in q_P of n decisive pairs [interval]." The paper then recommends punctuation removal for reporting |
| H-P NOT SUPPORTED / UNDERPOWERED | the same numbers; "the judgements did not show that removing punctuation matches people better" (or "too few decisive pairs") |
| H-U directional | which unit's order matched people in q_U (or 1 − q_U) of n decisive pairs; that unit becomes the recommended default |
| H-U EQUIVALENT | "the two units agreed with people equally within ±0.10" |
| H-U INCONCLUSIVE | the share, interval and n; "the judgements do not separate syllable and word units" |
| any | κ, the control share, the non-author-only row, the repeat agreement and the not-decisive counts by reason |

## 9. Tool to-do list (not implemented; to be built after the GO)

`tools/obj_rater/server.py`, `rater.html` and `build_assignment.py` are pinned by the XM600 plan (sha256 `e3beb936…`, `84a90787…`, `497e5747…`) and logged at every XM600 session end; that labelling is still running. **They are not edited.** The pair tool is three new sibling files in the same folder, each a small derivation.

**`tools/obj_rater/pair_server.py`** (copy of `server.py`; changes):
1. `IMAGES` (hard-coded to `data/datasets/xm3600/images`) becomes a required `--images` argument, resolved and checked to be a directory; for this set, `data/datasets/ktvic/images`.
2. The image route regex becomes `([0-9]{11})\.(jpg|jpeg|png)`; the file is served only if its name equals a `filename` of `test_data.json`, with `image/png` for `.png` and `image/jpeg` otherwise.
3. `LABELS = {"Y", "N", "U", "A"}` becomes `{"A", "B", "T", "X"}`.
4. `/` and `/index.html` serve `pair.html` instead of `rater.html`.
5. Unchanged on purpose: `load_qids` (the assignment keeps `screens[].q[].qid`, one q per screen), the record fields, the append-only fsync write, the 127.0.0.1 bind, the refusal of a `--dir` under /mnt, the 4,096-byte request cap, the quiet log; `key.json` and `BUILD.json` stay unserved.
6. `--port` default 8792; the server refuses ports 8790 and 8791 (Paper A's XM600 server and its top-up session, A-E3 run document v1.1 §9.1); no test or agent calls 8790 or 8791; the `--dir` must not be under `~/vsps_labels/`. One rating server at a time on the laptop: a `pair_server.py` session starts only after the last `server.py` session has its session-end LOG line, and no `server.py` session starts while a pair session is open, that is, before the pair session's own session line (§6). Labelling for this plan starts only after the XM3600-600 base labelling is finished (REDESIGN_B D1; CC-350 ruling 13(7)): the XM600 session-end LOG line that records the PI's statement that the base assignment is finished (CC-353 W8).

**`tools/obj_rater/pair.html`** (copy of `rater.html`; changes):
1. Title, header and the script's title line (l.160 of `rater.html`): "Đánh giá cặp chú thích".
2. `render()`: one question per screen; two caption boxes labelled "A" and "B" filled with `textContent` from `q.a` and `q.b`; side by side at 900 px and wider, stacked (A above B) below; the question line above the buttons.
3. `NAMES`, `SHORT`, `KEYS` become A "Chú thích A tốt hơn", B "Chú thích B tốt hơn", T "Ngang nhau", X "Không đánh giá được", keys 1 to 4.
4. The guide block is replaced by the instructions of §4 (open by default in practice).
5. Practice feedback is removed (`revealed`, `q.answer`, the "Xem đáp án" branch of `next()`): practice pairs have no answers.
6. Progress shows "cặp i/N"; the "Phần" label is removed (repeats are hidden).
7. `finish()` text becomes "Đã trả lời hết. Mọi câu trả lời đã được lưu. Cảm ơn bạn!" (not "Cảm ơn PI!", since R2 uses the same page).

**`tools/obj_rater/build_pairs.py`** (new; reuses `sha()`, the qid pattern `sha256(f"{SEED}|{part}|{image}|{a}|{b}")[:12]` and the `BUILD.json` layout of `build_assignment.py`):
1. Inputs: `PAIR_CANDIDATES.json` (stage 1), the 33 own `-short` files, the KTVIC test file; refuses an `--out` under /mnt.
2. Does §2.4 and §3.1 exactly; stores the side in `key.json`.
3. Writes `assignment.json` (`meta`: name, seed, labels, counts; `screens`: sid, image path, `q: [{qid, a, b}]`), `practice.json`, `key.json`, `ITEMS_MANIFEST.tsv`, `BUILD.json`.
4. `--selftest` on in-memory fixtures: disjoint images across strata, quotas and shortfall rule, side balance, repeats placed at least 100 screens after the first showing with sides swapped, no file name, stratum or score in any served file, display normalisation on toy strings; every drawn image's path exists and has one of the three extensions; a fixture with a `.png` image is served by the endpoint test.

**Checks on the rented host (PI-1111j), before the pin:** endpoint test (private files not served; a bad label, a bad qid and an image outside the regex refused); headless page test on the practice round (answer, next, back, resume after reload); load test of the main page. Pin package: the three files, `assignment.json`, `practice.json` and `key.json` (sha256 only), `ITEMS_MANIFEST.tsv`, `BUILD.json`.

## 10. Licences

- **Images and references.** KTVIC states no licence; it asks for citation and research use; its authors agreed to this project's use (Paper B sec3 l.72, §3.6 Datasets; PI-1026az). The images are shown locally to two raters and are not copied elsewhere.
- **Captions.** Only the authors' own system outputs are shown. No third-party output is shown by default (§2.1).
- **Judgements.** New, owned by the project. Whether to release them (qid, image id, file names, answers; no caption text) is the PI's choice at submission; default: aggregate statistics only.

## 11. Open questions for the judge (each with a recommended answer)

| # | Question | Recommended answer | Default |
|---|---|---|---|
| Q1 | Display normalisation (§3.1): final punctuation removed and first letter upper-cased on both captions | **Yes.** It removes the two cues that reveal the stratum and the system type; residual cues disclosed | as written |
| Q2 | May the two KTVIC baselines' outputs be shown to the raters (aggregate-use permission only)? | **No**, keep own outputs only | no |
| Q3 | Quotas 80 P, 180 U, 40 C, 30 repeats; margin ε = 10 CIDEr-D points per image | Yes; P is the scarcer stratum and needs fewer pairs for its registered direction | as written |
| Q4 | Consensus as the decisive unit, Holm over H-P and H-U, κ thresholds 0.40 and 0.20 | Yes | as written |
| Q5 | Hidden repeats (XM600 showed them as part 3) | Yes; a preference repeat shown as such would invite copying the first answer | hidden |
| Q6 | Analysis registered here rather than in a later file | Yes; PI-1111o asks for the analysis to be fixed before any judgement | as written |

**CC-350 rulings on these questions** (copied from CC-350; the rows above are v1's questions as asked): Plan §11: Q1 yes; Q2 no; Q3 quotas as N2 recommends, ε = 10 yes; Q4 yes; Q5 yes; Q6 yes.
