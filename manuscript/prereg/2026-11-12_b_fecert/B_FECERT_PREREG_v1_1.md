# B-FECERT: registration of the front-end certificate for comparisons of Vietnamese caption scores, with a held-out front-end check, a first scoring of other groups' released outputs, a front-end identification of the published KTVIC baseline scores, and a human preference arm (Paper B, LRE). DRAFT v1.1, not approved

> **Changes from v1.** v1 = `B_FECERT_PREREG_v1.md`, sha256 `4943b3c13cc5d619f24b604c348098de921c1f078298d4c3fd0a6a09ff721cd0`. Ruling: CC-350 (`.session_backup/2026-10-13/decisions/CC-350.txt`, sha256 `f4e05e266059340636cdef47b49f7e0b4e7b9e4d4ce4d2a4f417995370eda493`), NEXT_ROUND. Built by `build/build_v1_1.py` from v1 with exact-once replacements. Every replacement text that CC-350 gives is copied from the CC file as written (its ASCII `<=`, `x`, `F+` and `Clopper-Pearson` kept); where it goes into a table, it is placed in the table's cells. Nothing else changed.
> - **W1** (P1 control and order): §6.1 NC bullet replaced; §6.1 "Sets" (V written to `V.json` by stage 2a, its sha256 logged before stage 2b); §6.1 "Rule" bound wording; §9 stage 2 split into 2a and 2b, and 2b refuses to start without the `V.json` LOG line; §12 new mutant and stage list; §13 row 11-14.
> - **W2** (P4 is a method check): §6.4 replaced; every row that named P4 as a prediction changed: §0 label table, §5.3 heading and last bullet, §6.5, §7, §9 stage 3, §10 K-plant, §11 P4 row, §12 self-test.
> - **W3** (P3 labels): §6.3 "Labels" bullet replaced; §6.3 heading and P3a bullet aligned with it; §11 P3 SUPPORTED row restricted to M_new, with CIDEr-D and BLEU-4 POST HOC.
> - **W4** (order; thresholds): every value v1 tagged as a proposal is fixed and untagged (§2.6 F1; §4.3 items 2, 5, 6; §6.1 z_min and N; §6.2 n_FL; §6.4's value went with W2), and the header sentence says so; §9 stage 0 split into 0a documents and 0b code; "stage-0" became "stage-0b" in §12 and §13; §13 row 11-12 replaced.
> - **W5** (character unit, CC-350 ruling 2): §2.2 `chr` row; §2.3 `chr` bullet; §2.4 (F_held = `uts`, 18 members; F = 72); §5.1 (F⁺ still 271, `chr` included); §6.1 per-unit row and expectation line; §6.6 "with `chr`" row; §10 K-unit; §11 P1 FAIL row (`uts`; four units); §16 Q3 ruling recorded. Consequential: §3.2 example, §15 row.
> - **Rulings**: §0 Authority (Q1: D4 retired, D2 as in ruling 8(d); ruling 9(a) scope); §0 "supersedes" and "imported" paragraphs (Q11 status line; full B_KAPPA sha, N5; the inline-instead option dropped); §1.1 (ruling 10 conditions); §4.2 fetch bullet (ruling 8(d)); §12 code read (rulings 11 and 12); §16 (the CC-350 rulings are recorded below the table).
> - **N2** (via plan Q3): the quotas in §8. **N3** (via Q4 and Q9): §1.2 O8; §2.4 (pyvi in B-2; the 82.6% base); §4.3 (thresholds set after the gate.json values were seen).
> - **Version**: title v1.1; companion file names point to `B_PREF_LABELLING_PLAN_v1_1.md`.
> - Not applied in v1.1 as first built (non-blocking): N1, N4, N6, N8. **CC-353 round-2 fixes**, applied afterwards in place and byte-checked against CC-353: §2.3 admissibility rule (a) (CC-353 W5r); §4.2 G6 cell (N1); §9 stage C segmenter census (N4); §17 PI-3 permission date and scope (CC-353 W9, was N8). In the labelling plan: §9 pair_server item 6 (CC-353 W8), §10 citation (N8), §11 note.

Drafted between the `date -u` readings 2026-11-11T23:05:59Z and 23:21:54Z, revised up to 2026-11-12T02:31:06Z (2026-11-12 in Vietnam), by a writer agent. vsps HEAD `3d7a119`, branch `paper-v10`. Paper B text at `vsps-paperB-lre` `edf7fee`. AI-designed; every recommendation is an opinion. Nothing here has run. No code exists. "unverified" marks a statement the writer did not check today. The thresholds that v1 tagged as proposals are fixed in v1.1 and carry no tag (CC-350 W4).

Companion file: `B_PREF_LABELLING_PLAN_v1_1.md` (this folder). That file registers the human arm (items, blinding, agreement rule and its analysis). This file refers to it and does not repeat it.

---

## 0. Status, labels, authority

**Evidence labels used in this file and in any text built on it.**

| Label | Meaning | Where it applies |
|---|---|---|
| `DEVELOPMENT` | computed on files that this project scored before, on spent references | every number on the 73 own KTVIC files and the two KTVIC baselines (§4.1) |
| `POST HOC` | a number that existed in a stored file before this registration, or a row added after a look | the October numbers listed in §1.2; anything added after a look |
| `FIRST SCORING OF RELEASED OUTPUTS` | the first n-gram score ever computed by this project on another group's released output file. The references used may be spent (KTVIC test, UIT-ViIC test) | the first-look comparisons of §4.2. Never called "held-out test", "test-set result" or "confirmatory" |
| `HELD-OUT FRONT END` | a front-end member never run on any system output by this project before this registration's commit | the held-out members of §2.4 |
| `REGISTERED PREDICTION` | a rule fixed in this file, before the quantity it governs exists in any file | P1 to P3 (§6) and the human hypotheses of the labelling plan; P4 (§6.4) is a method check, not a prediction (CC-350 W2) |
| `DESCRIPTIVE` | reported with no verdict | everything else |
| `CONTROL` | English analogue, no verdict | §6.6 |

**Authority.**
- PI-1111l (LOG, 2026-11-11T16:01:21Z): Paper B's route is front-end validity at LRE, and its method part is redesigned "theo khuyến nghị". The writer read that LOG line only to 300 characters (custody rule for LOG reads). CC-350 Q1: "PI-1111l (16:01:21Z) predates REDESIGN_B (16:02-16:50Z), so it cannot cover D2 or D4. PI-1111n/o do not visibly cover them within 300 characters. D4 (retire the swap test of an unjudged, uncommitted draft) is a reversible technical call and is decided here: retired. D2: the fetch is licensed as in ruling 8(d)." Ruling 8(d) is carried into §4.2.
- PI-1111n and PI-1111o (2026-11-11T16:58:44Z and 16:59:44Z): a third human-labelled set, blind pairwise preferences, about 300 caption pairs, two raters. Items, blinding, agreement rule and analysis are registered and judged before any judgement is collected. Read to 300 characters. CC-350 ruling 9(a): "300 distinct pairs, 30 hidden repeats and 8 practice screens are INSIDE PI-1111n/o (about 300 pairs, two raters). The repeats are within-rater reliability screens, not new items."
- Design source: `manuscript/directions/redesign_2026-11-11/REDESIGN_B.md` (sha256 `2242fcc2a6cdbd4e…`), candidate C1 FE-CERT with C3 as its human arm and the FE-PRED row, plus the FE-ID finding of C2 as its application. The coordinator chose this combination after the blind scores in `REDESIGN_SCORES_2026-11-12.md` (sha256 `0adecfa15475c411…`).
- What the design must answer, from those scores (K41, K45): a recombination of known arguments; most comparisons certify, so few conclusions change; the held-out outcome is foreseeable; an author as rater; few systems with a paper; a small user community. §15 says which of these a design can answer and which it cannot.

**What this file supersedes.** `manuscript/prereg/2026-11-11_b_kappa/B_KAPPA_PREREG_v1.md` (sha256 `b56d8ccded3c10b26c318262699e26014c5eb07f8f3da70afba5949ff1eeb35d`, unjudged, uncommitted; CC-350 N5). Its κ specification (§2.1 to §2.4 there: the seven steps, the strict g2 domain, main-vowel direction) is reused here as the tone-placement level tm (§2.2). Its rank-swap test (§4 to §8 there) is retired and not run (REDESIGN_B D4; decided by CC-350 Q1). Its finding that the pinned segmenter rewrites tone placement itself (§2.4 and §5.3 there) is carried as a fact to be re-checked by code (§2.6, check F3). Consequence for that file: FE-CERT scores its 49 "U" files under other written forms, so the κ test could not later claim those files as unseen. CC-350 Q11 records it: Log one status line: "superseded, never registered; swap test retired, not run; only the sections imported by B_FECERT v1.1 bind". The same line records that B_KAPPA's 49 U files lose "unseen under other forms" when stage 1 runs.

**Definitions imported from B_KAPPA v1 by reference** (that file is committed unchanged with this one as a pinned reference; CC-350 Q11): §2.2 (Unicode version, the 25 White_Space code points, case fold, the final-punctuation set, letter runs, tone marks and vowel modifiers, the onset list); §2.3 (the g2-variable run, strict domain); §2.4 (main-vowel direction); §2.5 (moves g1 to g6); §3.1 (toy strings, used by check F3); §4.2 (the 24-file E4 seen set S, used by the planted check); §4.3 (the family rule from file names); §5.1 (scorer and the G-repro rule).

**Rules that bind.** No AI label is evidence. No caption text is printed, logged or committed (`evaluating-image-captions`). CPU steps, self-tests and mutants run on a rented host, not on the laptop (PI-1111j). One I/O-heavy command at a time on /mnt/d. A FAIL is reported where a PASS would have been. The human-label custody of the labelling plan §6 binds every agent.

---

## 1. What existed before, and what the writer of this file saw

### 1.1 What the writer opened for this draft

- In full: REDESIGN_B.md; REDESIGN_SCORES_2026-11-12.md; B_KAPPA_PREREG_v1.md; `XM600_GOLD_COMPLETION_PLAN_v1_1.md`; `tools/obj_rater/server.py`, `rater.html`, `build_assignment.py` (sha256 `e3beb936…`, `84a90787…`, `497e5747…`, equal to the XM600 pins); Paper B `paper/sec3_data_and_audit.md` at `edf7fee`; the skills `running-vsps-research-cycle`, `evaluating-image-captions` and `venue-lre`; `.claude/agents/STATE_2026-11-10.md`; three memory notes.
- In part: `A_CERT_ANALYSIS_REG_v1_1.md` (headings and first 40 lines, as a format model); `scripts/kit_b/protocol_pilot.py` (function list, l.40 to 68 and l.225 to 256: the tokenisers and the protocol table, code only); `scripts/identify_segmenter.py` docstring; `scripts/evaluate.py` l.20 to 32; Paper B `sec5_results.md` l.27 and l.7 (two grep hits, 260 characters each); LOG lines 2205 to 2240 and the grep hits for PI-1111*, each cut at 300 characters.
- Structure only: `.session_backup/2026-10-28/b2_external/gate.json` (per file: sha256, rows, unknown ids, covered ids, duplicates, empty, reference-copy share, reason; no caption, no score) and `fetched/fetch.json` (URLs, commits, git blob ids, sha256, bytes); the file names and sizes under `b2_external/fetched/` (no file opened).
- Metadata: `pip show pyvi` on the laptop (version 0.1.1); the file list of `data/datasets/ktvic/` (4,327 image files named by 11-digit ids); `import underthesea` on the laptop (not installed).
- **Not opened:** any `*.preds.json`; `E4/pilot_results.json`; any score or result file; any file under `~/.vsps_sealed`, `~/bpa1pull_1108` or `.session_backup/machines/HBT1/`.
- **Touch to disclose:** one command `ls ~/vsps_labels >/dev/null` at about 2026-11-11T23:03Z. The listing went to /dev/null; no file name or content was seen. No file under that directory was opened. Reported to the coordinator for the access record. CC-350 ruling 10: The disclosure in §1.1 l.46 SUFFICES, on these conditions:
  - the output went to /dev/null and no name or content was seen, as the writer states;
  - the writer agent takes no role as a rater or analyst of the XM600 labels (condition; the coordinator confirms this in the access record).

### 1.2 Numbers that already exist (all POST HOC for this registration)

Every number below was computed from stored files before this registration, and most were seen by the project in October. None may be cited as a result of this registration. Each is quoted from REDESIGN_B or Paper B with its source key; the writer did not re-open the source files.

| # | Number | Source key (as quoted) | Role here |
|---|---|---|---|
| O1 | 105 pairs of 15 own fine-tuned systems on KTVIC test; point order flips: syllable 2, pyvi 1, stripped punctuation 1; 26 pairs significant under the committed scorer, 0 reversed by any front end | `.session_backup/2026-10-14/research_r10/E4/pilot_results.json` (sha256 `17c67171…`) `:: ranking` | development; the reason the expected case is "most own comparisons certify" |
| O2 | zero-shot files move more: 27.91 against 26.10 under RDRSegmenter becomes 32.10 against 32.58 under syllables | same file | development; the reason first-look systems with low scores may be fragile |
| O3 | KTVIC baselines, mismatched row P4 (RDR-segmented outputs against unsegmented references): CIDEr-D 21.79 and 36.77, BLEU-4 15.47 and 19.34; printed values 21.8, 36.8, 15.5, 19.3 | `pilot_results.json :: protocols` rows `P4_T3bug_rdr_hyp_vs_raw_refs`; KTVIC paper (arXiv 2401.08100, HTML read 2026-11-11 by REDESIGN's writer) | **POST HOC.** The FE-ID finding on KTVIC is development evidence, seen in October |
| O4 | matched RDR 48.85 and 72.87 (BLEU-4 22.74, 27.63); matched syllables 52.85 and 79.10; pyvi 48.87 and 72.63 | same | POST HOC |
| O5 | ROUGE-L of the two baselines under all 13 E4 protocols, row `P4_T3bug…` included | same file (it computes CIDEr-D, BLEU-4, ROUGE-L) | **stored but never compared with the printed ROUGE-L** (REDESIGN_B §0 Fact 2: "ROUGE-L and the other printed metrics were not compared today"). It exists, so it is not "unseen"; §5.4 says how P3 treats it |
| O6 | 15.64-point CIDEr-D shift from unit alone (p1-gold: 149.79 RDR, 165.43 syllables); τ = 0.969 over 26 systems; pyvi 149.12, τ = 0.994 | Paper B sec3 §3.4 with its src keys | POST HOC |
| O7 | one appended period: −35.17 CIDEr-D under P0; 0.00 with PTB-style removal | Paper B sec3 §3.3 | POST HOC |
| O8 | RDRSegmenter reproduces KTVIC's `segment_caption` on 2,790 of 2,790 test references; underthesea on 82.6% | Paper B sec3 §3.4 src; `scripts/evaluate.py` l.27 | POST HOC; underthesea has been run on references (not on system outputs); CC-350 N3: the 82.6% is on 2,000 KTVIC captions, and identify_segmenter.py prefers train_data.json. |
| O9 | the pinned segmenter writes main-vowel tone placement whatever the input ("hòa bình" and "hoà bình" both give `hoà_bình`), toy strings only | B_KAPPA_PREREG_v1 §2.4 | re-checked by code (§2.6 F3) |
| O10 | the ten fetched other-group files: rows, id coverage and gate reasons (all ten failed the 2026-10-27 gate; "0 metric lines") | `gate.json` (sha256 `5519b26d…` per Paper B src), CHAIN.log per REDESIGN_B §1 | structure only; no metric has ever been computed on them |
| O11 | REDESIGN_B's power table (37, 67, 153, 215 decisive judgements) | arithmetic, not data | replaced by the two-sided values of the labelling plan §5 |

**What follows for the labels.** Every certificate on the 73 own files and the two baselines is `DEVELOPMENT`. The held-out members are new for all files. The first-look comparisons are new for all members. The FE-ID statement "the printed KTVIC baseline scores are reproduced by a mismatched pipeline" is `POST HOC` for CIDEr-D and BLEU-4; only the metrics never compared with print can carry a registered prediction (§5.4).

---

## 2. The admissible front-end family

### 2.1 Pipeline order (fixed; every member applies all steps in this order, to outputs and references alike)

For a text t:

1. **N (always).** NFC over the whole string; each U+005F (underscore) becomes U+0020; every maximal whitespace run (the 25 White_Space code points of B_KAPPA §2.2) becomes one space; leading and trailing whitespace removed. N is not an axis. It makes the released underscore-segmented outputs of the KTVIC baselines comparable (Paper B sec3 §3.4 does the same).
2. **T, tone placement** (on the output of 1).
3. **P-pre, punctuation before the unit** (on the output of 2).
4. **U, unit tokenisation** (on the output of 3, with case as written).
5. **C, case** (on the tokens of 4).
6. **P-post, punctuation token removal** (on the tokens of 5; only for level pa).
7. NFC on each token.

Case is applied after the unit so that the segmenters see case as written. This is the committed scorer's order (`lower(rdr(t)).split()`, B_KAPPA §5.1), so member f0 (§2.5) is the committed protocol P0.

### 2.2 Axis levels

| Axis | Level | Exact definition |
|---|---|---|
| T | tw as written | no change |
| | tm main-vowel | κ step 6 of B_KAPPA §2.3 to §2.4: in a g2-variable letter run (onset + one of the pairs oa, oe, uy without vowel modifier, one tone mark, end of run, not after q) the tone mark is moved to the second letter |
| | tf first-vowel | the same domain; the mark is moved to the first letter |
| P | pk as written | P-pre and P-post do nothing; punctuation is whatever the unit tokeniser makes of it |
| | pf final run stripped | P-pre removes the maximal trailing run of characters from {U+002E, U+0021, U+003F, U+2026, U+003B, U+003A, U+002C} and whitespace (κ step 5) |
| | pa all punctuation removed | P-pre inserts one space before and after every character whose Unicode general category starts with P; P-post drops every token made only of such characters. This covers every token of pycocoevalcap 1.2's PTB punctuation list except the bracket names `-LRB-` and similar, which only PTB's own tokeniser creates |
| C | cf folded | `str.casefold()` on each token |
| | ck kept | no change |
| U | `syl` syllable | `str.split()` on the single-space text |
| | `rdr` word, RDRSegmenter | VnCoreNLP 1.2 jar, sha256 `9e2811cd…`, through `scripts/kit_b/protocol_pilot.py::rdr` (sha256 `6aee4282…`); tokens are the segmenter's words, syllables joined by "_" |
| | `pyvi` word | pyvi 0.1.1 (laptop `pip show`, 2026-11-12; the host version must equal it, else FAULT), `ViTokenizer.tokenize(t).split()` |
| | `uts` word, underthesea | `underthesea.word_tokenize(t, format="text").split()` (call signature unverified today; the code read checks it against the installed release); version: the release installed on the host before the code read, recorded with the wheel sha256 in `FAMILY.json` before any score. Version unverified today |
| | `chr` character | every non-whitespace code point of the text, in order (spaces are not tokens). not in F (CC-350 ruling 2); in F+ only |

### 2.3 Members and admissibility

A member is f = (U, T, P, C), always "matched": the same f is applied to outputs and references. There are 3 × 3 × 2 = 18 members per unit.

**Admissibility rule.** A member is admissible when (a) its unit is used by a public Vietnamese captioning scorer or paper, or is a released Vietnamese word segmenter with a pinned version, and (b) each of its T, P and C levels is either used by such a scorer or differs from a used level only by moves g2, g5 or g6 of the κ transform set (tone placement, case, final punctuation; B_KAPPA §2.5). `chr` meets (a) as written but is excluded by name (CC-350 ruling 2: its only user reports it as distorting the scores; CC-353 W5r). Under this rule and that exclusion:
- `syl`, `rdr`, `pyvi`, `uts`: admissible (ViTextCaps Appendix C.2 uses space split, PyVi and underthesea, per REDESIGN_B §1(b); RDRSegmenter is KTVIC's own).
- `chr`: not admissible (CC-350 ruling 2).
- ck (case kept), pk, pf, pa, tw to tf: admissible under (b).
- **Mismatched pipelines are never admissible**: any treatment that differs between outputs and references. They appear only in the identification family F⁺ of §5.

### 2.4 Development and held-out members (fixed now)

| Set | Units | Members | Why |
|---|---|---|---|
| F_dev (development) | `syl`, `rdr`, `pyvi` | 54 | `syl` and `rdr` are the two units of the paper's audit; `pyvi` was run on 24 own files and both baselines in the E4 pilot (October), so it cannot be held out. CC-350 N3: pyvi also ran on K1, K5 and K6 in B-2 (b2.py l.711-752). |
| F_held (held-out) | `uts` | 18 | never run on a system output by this project. `uts` was run on KTVIC references in `identify_segmenter.py` (82.6% agreement, O8; CC-350 N3: the 82.6% is on 2,000 KTVIC captions, and identify_segmenter.py prefers train_data.json); disclosed. `chr` is not in F (CC-350 ruling 2) |
| F = F_dev ∪ F_held | | 72 | `chr` is not admissible (CC-350 ruling 2); F_held = `uts` (18 members) |

### 2.5 Reference member and merging

- **f0** = (`rdr`, tw, pk, cf) = the committed protocol P0 of Paper B. It is the member under which an author would report, and it fixes the "nominal direction" of a comparison (§3.2). Gate G-repro (§9) checks that f0 reproduces the committed scores.
- **Merging.** For one comparison, two members are one **class** when they produce identical token sequences for every output of both files and every reference of the image list. Merging is by token identity only, never by score. The number of classes per comparison is reported. Example expected from O9: tw, tm and tf should merge under `rdr` when the segmenter rewrites placement itself; whether they do is measured, not assumed.

### 2.6 Preconditions (run on the host before any system output is scored)

- **F1, real decomposer.** Each word unit is run on the KTVIC test references. Every string must come back non-empty and aligned; a whitespace fallback or more than 0.5% failed strings drops that unit from F (recorded in `FAMILY.json` before any score). A failure of `rdr` is a FAULT: nothing proceeds.
- **F2, versions.** The jar sha256, the pyvi and underthesea versions and wheel sha256, the Python and `unicodedata.unidata_version` are written into `FAMILY.json`.
- **F3, tone placement under each unit.** On the toy strings of B_KAPPA §3.1 (no dataset text), each word unit's output for the tm and tf spellings is recorded. This replaces the assumption of O9 by a code record.

---

## 3. The certificate

### 3.1 Comparison and statistic

A **comparison** c = (a, b, I, R): two output files a and b on the same image list I, with reference sets R from one reference file. Metric: CIDEr-D (n = 1 to 4, σ = 6, document frequencies from the references of I under the member; `Cider` of `protocol_pilot.py`, ×100). BLEU-4 and ROUGE-L are computed and reported with no verdict.

Under member f: per-image scores s_f(a, i), s_f(b, i); difference D_f(c) = mean over i in I of s_f(a, i) − s_f(b, i).

**Interval.** Paired bootstrap over images: B = 10,000 draws, seed 20261112. Each draw resamples the indices of I once; the same draws are used for every member and for every comparison on the same image list. Document frequencies stay at their full-list values. [L_f, U_f] = the 2.5th and 97.5th percentiles of the bootstrap D_f: a two-sided 95% percentile interval, because the direction of a comparison is read from the data.

### 3.2 Decision rule (for a family G: F_dev, F_held or F)

- sig+(f): L_f > 0. sig−(f): U_f < 0.
- **CERTIFIED (a > b over G)**: sig+(f) for every class f of G. **CERTIFIED (b > a)**: sig−(f) for every class. The output names the direction.
- **REVERSED**: sig+ under some member and sig− under another.
- **FRAGILE**: not certified, and significant under at least one member (REVERSED is a subset).
- **NULL-STABLE**: significant under no member.
- **Nominal direction**: the significant direction under f0; if f0 is not significant, the direction significant under more classes; if neither, none.
- **Breaking set** of a FRAGILE comparison: the classes under which the nominal direction is not significant, reported with counts per axis level (for example "breaks under every `uts` member and under ck with pk").
- **CHANGED (the conclusion changes)**: the comparison is significant under f0 and not CERTIFIED over G. Its denominator is the number of comparisons significant under f0. NULL-STABLE comparisons and those significant only under members other than f0 are reported in separate rows and never enter the CHANGED share.
- **Point-sign flip** (reported, no verdict): the signs of D_f differ between two classes, both |D_f| > 1e-9.

### 3.3 What the certificate guarantees, and whose argument it is

- **Statement.** Take the null hypothesis "for some member f in G, the population mean difference Δ_f ≤ 0" (population = images exchangeable with I, references and outputs fixed). A test that declares CERTIFIED (a > b) only when every member's test rejects Δ_f ≤ 0 at level α has level α for that union null. No multiplicity correction over members is needed. This is the intersection–union principle (Berger, 1982; Berger and Hsu, 1996; both unverified today, to be read before any text cites them).
- **Nominal, not exact.** Each per-member test here is a percentile bootstrap at one-sided 2.5% per direction, so the guarantee is nominal. It holds conditional on the reference sets and on the document frequencies of the full list.
- **Not guaranteed:** front ends outside G; learned metrics; human agreement; anything about another language; the absence of training exposure of the systems (irrelevant to the certificate, which concerns the metric's verdict on given outputs, not system quality).
- **Conservative by design.** Requiring every member to pass lowers the share of certified comparisons. The NULL-STABLE and FRAGILE rows show that cost.
- **Idea provenance (for every text built on this file).** Core idea, checking one conclusion under every defensible specification: specification-curve and multiverse analysis (Simonsohn, Simmons and Nelson, 2020; Steegen et al., 2016, unverified today). Score signatures and the warning that tokenisers make scores incomparable: sacreBLEU (Post, 2018). Guarantee: intersection–union tests (Berger). Nearest Vietnamese work: ViTextCaps Appendix C.2 (five tokenisations, one order swap at character level, no per-comparison verdict, no held-out front end, no human judgement). Ours: the enumerated Vietnamese family, the held-out front-end check with its sensitivity control, the CHANGED count on other groups' released outputs, the human-preference arm, and the KTVIC application. **Type: combination.** No "first" claim.

---

## 4. The comparisons

### 4.1 Development comparisons D (seen files; label `DEVELOPMENT`)

- Files: the 73 own KTVIC test files `data/results/<name>.preds.json` (names = keys of `data/results/tone_norm/ktvic_side_by_side.json :: systems`, B_KAPPA §4.1); references `data/datasets/ktvic/test_data.json` field `caption` (558 images, 2,790 references).
- Strata: prompt mode (`-short`, `-detailed`, `-two`). Families: the file-name rule of B_KAPPA §4.3 (26 families).
- **D** = all unordered pairs of own files in the same stratum and in different families, plus the one pair of the two KTVIC baselines (ResNet101-LSTM against ViT-Transformer; `.session_backup/2026-10-22/b2/thesis_code_1a8d105/simple_evaluate/`, aggregate use only). Its size is printed by stage C; no number is promised here.
- Not in D by default: own files against the baselines (the paper states it ranks no Vietnamese system; §16 Q8), K1 (the B-2 registration says that run "ranks no system", §16 Q8), same-family pairs.
- Expected case, stated now from O1 (not a prediction): few CHANGED comparisons in D among fine-tuned files; more among zero-shot files.

### 4.2 First-look comparisons FL (label `FIRST SCORING OF RELEASED OUTPUTS`)

**Groups and the maximum count by enumeration.** A comparison is formed only inside one group (same image list, same reference file). "Max" assumes every file passes the gate of §4.3; all ten fetched files failed the older gate of 2026-10-27, mostly on ids, so the realised count may be much lower.

| Group | Files (state) | Image list and reference file that scores it | Licence | Max comparisons |
|---|---|---|---|---|
| G1 | X4a to X4e, `uit_generated_captions.txt` of 5 systems (fetched; sha256 in gate.json; never scored) | the repository's own 578-row UIT-ViIC list; references from `data/uit_test/` of `loc110504/VietnameseSportImageCaptioning` @6d8132e (**to fetch**; content unverified) | MIT | 10 |
| G2 | the same 5 systems, `us_generated_captions.txt` (**never fetched**) | the repository's sport set; references from `data/capydata_ic/test/` (**to fetch**; size unverified) | MIT | 10 |
| G3 | X3 `uit_viic_original_pred.json`, `uit_viic_detect_pred.json` (fetched; never scored) | 924 rows (the size of the official UIT-ViIC validation split; ids unverified); the reference file beside them in `annotations/` of `vanngthi/ViECAP-Image-Captioning-Vietnamese` @fd71ca5 (**to fetch**; which file unverified) | none: aggregate only | 1 |
| G4 | X3 Flickr sport `flickr_*_pred.json`, 2 variants (**never fetched**) | 100 images; references beside them (**to fetch**) | none: aggregate only | 1 |
| G5 | X1 `trannam710/NIC-with-Soft-Attention` @0660118 and X2 `trannam710/Meshed-Memory-Transformer` @6109801, `caption_results.json` (fetched; never scored) | UIT-ViIC; split unverified. Scored against this project's UIT-ViIC copy only if the ids equal one official split; else not admitted | MIT; BSD-style | 1 |
| G6 | K2 `SuperCoolGuy855/CLIP_mT5_Image_captioning` @d786f6d `results.xlsx` (fetched; never scored; number of systems unverified; the README prints three CIDEr values) | KTVIC test, `data/datasets/ktvic/test_data.json` (spent references) | none: aggregate only | 3 within K2, plus 3 x 2 = 6 against the two KTVIC baselines: up to 9 |
| | | | **Total (maximum)** | **32** |

- Concentration: G1 and G2 come from one repository and give up to 20 of the 32. Every FL count is reported per repository and with each repository left out in turn (§6.2).
- The fetch of G2, G4 and the reference files of G1, G3, G4 needs D2 of REDESIGN_B. Fetching follows the B-2 pattern: a generic client, a pinned commit, sha256 and git blob id logged, no content printed. CC-350 ruling 8(d): Licensed by this ruling only AFTER the v1.1 commit (W4), as follows:
  - sha only, a generic client, a pinned commit, and no content printed;
  - the schema print shows key names, types, lengths and row counts only;
  - files from MIT repositories (loc110504, trannam710) may then be fetched at once;
  - files from repositories without a licence (the vanngthi Flickr outputs and the reference files beside them) are fetched under the CC-092 aggregate-only rule, and the coordinator reports this to the PI first (PI-1110i: "licences ... are reported first");
  - if the PI objects, FL = the MIT files plus the already-fetched X3 and K2 files, aggregate only.
- Nothing in FL is scored under any member before this registration and its code are committed (§9).
- Not in FL: the eight public checkpoints of REDESIGN_B D3 (a GPU decode on an unseen set). Not registered in v1 (§16 Q12).

### 4.3 Structure gate v2 (admission without any score; mechanical)

The parser for each source is written from a schema print (key names, value types, lengths, row counts; no caption text) and is part of the code read. A file is **admitted** when all of these hold:

1. it parses to {image id: one caption string} (a list value: its first element, as `load_preds` of the kit does);
2. coverage: at least 95% of the image ids of its reference file have a caption, and at most 5% of its rows have ids absent from that reference file (those rows are dropped);
3. duplicate ids at most 1% of rows (first occurrence kept);
4. empty captions at most 1% of rows;
5. reference-copy share at most 5%: captions equal, after N and casefold, to one of the image's own references;
6. at least 50% of captions contain a letter with a Vietnamese diacritic (detects stripped diacritics or another language).

A comparison of two admitted files is **formed** when their covered id sets overlap in at least 95% of the reference file's ids and the comparison is scored on that intersection. Training exposure of a system's images (REDESIGN_B notes that X3's outputs may be on training images) does not affect admission, for the reason stated in §3.3. The gate writes `GATE2.json` (per file: the six values, admitted or not; per comparison: formed or not, intersection size). The coordinator logs its sha256 before any FL score exists. CC-350 N3: The gate v2 thresholds were set after the writer saw the gate.json values (no score; refcopy 0.0; unknown-id counts).

---

## 5. Front-end identification (FE-ID), the application

### 5.1 Family F⁺ and rule

- F⁺ = every member f of F (§2.4) and the 18 `chr` members, 90 members in all (`chr` is not in F, CC-350 ruling 2, but identification needs no admissibility), applied three ways: **matched** (both sides), **outputs only** (references get N only, then whitespace split), **references only** (outputs get N only); plus **r\***, the released-script member: pycocoevalcap 1.2 `COCOEvalCap` (PTB tokeniser, both sides as released, underscores kept). |F+| = 90 x 3 + 1 = 271, `chr` included.
- Input: output file, reference file, the printed values p_m of each printed metric m with d_m printed decimals.
- A member **reproduces** when |score_m − p_m| ≤ 0.5 × 10^(−d_m) + 1e-9 for every printed metric m.
- Members are merged into classes by token identity on the given files (as §2.5).
- **IDENTIFIED**: the reproducing members form exactly one class. **AMBIGUOUS**: two or more classes. **OUTSIDE**: none. Reported beside it: the smallest distance, on the printed scale, between the reproducing class and the nearest other class (the identifiability margin).
- What it cannot show: that the true pipeline is in F⁺, or that the released outputs are the ones that were scored. Every FE-ID sentence carries both caveats.

### 5.2 Printed values

A separate agent (not the coder) copies every printed metric value of the KTVIC baselines (KTVIC paper table; arXiv 2401.08100, version and table number recorded), the K2 README, and any README or paper of the FL groups that prints a score, into `PRINTED.json` with URL, version, access date and table or line. Which metrics the KTVIC table prints beyond CIDEr and BLEU-4 is unverified today. `PRINTED.json` is judge-checked against the sources and its sha256 logged before FE-ID runs.

### 5.3 Planted check (method validation; METHOD CHECK, not a registered prediction)

- 24 cases: each of the 24 own files of the E4 seen set (B_KAPPA §4.2) is scored under one member of F⁺ drawn with `random.Random(20261113)` by a `plant` step that writes the truth to `PLANT_KEY.json` and only the rounded CIDEr-D, BLEU-4 and ROUGE-L (one decimal, as KTVIC prints) to `PLANT_PRINTED.json`. The identification step reads only `PLANT_PRINTED.json`; the key is compared after all 24 identifications are written.
- **Wrong recovery**: IDENTIFIED with a class that does not contain the true member.
- **P4 (§6.4)** is the method check on these cases: a wrong recovery is a FAULT, not a FAIL (CC-350 W2).

### 5.4 KTVIC baselines (label `POST HOC` for O3; `REGISTERED PREDICTION, DEVELOPMENT DATA` for the parts never compared with print)

What is already known (O3, O4): a mismatched row reproduces the printed CIDEr-D and BLEU-4 of both baselines; the matched rows do not. What has not been done: run r\* (the released script) at all; compare any printed metric other than CIDEr-D and BLEU-4 with any computed value. The ROUGE-L values of O5 exist in a stored file but were never compared with print; the writer has not seen them.

P3 (§6.3) registers what can still fail. Reporting wording is neutral (§14): "the printed scores are reproduced by pipeline X; under matched scoring the values are Y".

### 5.5 Printed comparisons (label `DESCRIPTIVE`, a count with its denominator)

- Census: every pair of systems that one source prints side by side (KTVIC table: 3 systems, 3 pairs; K2 README: up to 3 pairs; FL repositories: whatever `PRINTED.json` holds).
- For each printed pair: whether both sides' outputs are released and admitted (**re-scorable**), one side only (**one-sided**), or neither.
- Re-scorable pairs: printed order, order under f0, the certificate over F, the printed gap and the gap under f0. One-sided pairs (for example GRIT 136.0 against the baselines): the gap with the released side re-scored under f0, labelled "one side re-scored; the other side's pipeline unknown".
- Reported as "k of n printed comparisons change order under matched scoring; m of n are not certified over F", with n stated. No word such as "wrong", "error" or "invalid" is attached to a published score.

---

## 6. Estimands and predictions (thresholds fixed now)

### 6.1 P1, held-out front-end check (`REGISTERED PREDICTION`; the check that can fail)

- **Sets.** Cert_dev = every comparison in D ∪ FL that is CERTIFIED over F_dev. Margin of a certified comparison: z_min = the smallest, over the classes of F_dev, of |D_f| / sd_boot(D_f). **Verdict set** V = the certified comparisons with z_min ≤ 4 (near-margin). If |V| < 59, V = Cert_dev; which set was used follows mechanically from F_dev scores alone and is written, with the ids of V, into `V.json` by stage 2a (D and FL under F_dev only); the coordinator logs the sha256 of `V.json` before stage 2b runs any held-out member.
- **Why near-margin.** D holds several hundred own pairs (count printed by stage C), FL at most 32; most own certificates have margins of tens of CIDEr-D points (fine-tuned against zero-shot), which no admissible front end can break. A verdict on all of Cert_dev would be decided by easy own pairs, and FL could break entirely while P1 passed. Restricting to near-margin certificates keeps the verdict on comparisons a front end could plausibly break. Expected split: V is still mostly D; FL carries its own row below.
- **Break.** The certified direction is not significant under at least one class of F_held. **Reversal** (reported inside the break count): significant in the opposite direction, or a point-sign flip, under a held-out class.
- **Estimand.** r = breaks / N, N = |V|.
- **Rule.** N < 59 (59 is the smallest N for which zero breaks give a one-sided 95% Clopper–Pearson upper bound below 0.05): NOT_EVALUABLE. If the one-sided 95% Clopper-Pearson upper bound <= 0.05: **PASS** ("certificates on the development family held under the held-out front ends in this pool"). Lower one-sided 95% bound > 0.05: **FAIL** ("the development family does not cover the front-end variation that matters"). Otherwise: **INCONCLUSIVE**.
- **FL row (reported with its own Clopper–Pearson interval, no verdict).** r over the FL comparisons in Cert_dev. If its lower one-sided 95% bound exceeds 0.05, the paper states this beside the P1 label whatever the label is.
- **Reported beside it (no verdict):** r over all of Cert_dev; r for D and for FL separately; r for `uts`, and DESCRIPTIVE 'with chr' rows (chr members added to F_held), no verdict; the reversal count.
- **Disclosed weakness.** Comparisons share files, so they are not independent; the Clopper–Pearson bound is a nominal summary.
- **Sensitivity control NC (computed and pinned at stage 1, before any held-out member runs).** On D only, with the verdict-set rule of P1: Cert_NC = the D comparisons CERTIFIED over the 18 `syl` members; z_min^NC = the smallest, over the `syl` classes, of |D_f| / sd_boot(D_f); V_NC = the comparisons of Cert_NC with z_min^NC <= 4; if |V_NC| < 59, V_NC = Cert_NC. A break is: the certified direction is not significant under at least one `rdr` or `pyvi` class. r_NC = breaks / |V_NC|. NC.json records which set was used and |V_NC|. If |V_NC| < 59 after the fallback, NC is NOT_EVALUABLE and P1 carries the words 'sensitivity not measured'. If r_NC <= 0.05, P1 is labelled LOW-SENSITIVITY whatever its outcome: 'a one-unit family was broken by the other development units in at most 5% of its near-margin certificates, so the held-out check had little room to fail'.
- **Expectation stated now (not a prediction).** With `uts` alone: PASS is likely (O1: pyvi reversed 0 of 26 significant own pairs).

### 6.2 P2, how many conclusions change on other groups' outputs (`REGISTERED PREDICTION`)

- **Estimand.** Over FL: n_FL = comparisons significant under f0; k_FL = those CHANGED over F (§3.2).
- **Rule.** n_FL < 10: NOT_EVALUABLE (counts reported, no label). k_FL ≥ 3 and k_FL / n_FL ≥ 0.10: **SUPPORTED** ("the front end changes the conclusion of k of n significant comparisons among other groups' released outputs"). Otherwise: **NOT SUPPORTED**, reported as "the certificate changed few conclusions in this pool (k of n)".
- **Always reported:** the counts of CERTIFIED, FRAGILE, REVERSED and NULL-STABLE over F and over F_dev; k_FL per repository and with each repository left out; the breaking axis levels; the same counts for D, labelled DEVELOPMENT.
- **Why this threshold.** The scorers' objection was that "few conclusions change". The design cannot make conclusions change; it can pre-state the count that would make the method matter and publish the count either way.

### 6.3 P3, FE-ID on the KTVIC baselines (`REGISTERED PREDICTION, DEVELOPMENT DATA` on M_new only; the rest `POST HOC`)

- **Metrics in scope.** BLEU-1 to BLEU-4, METEOR, ROUGE-L and CIDEr-D as computed by pycocoevalcap 1.2 (`COCOEvalCap`; METEOR and the PTB tokeniser need Java on the host). Printed metrics outside this list (for example SPICE) are listed and not used. A metric in scope whose scorer fails its host precondition (pycocoevalcap import, Java, METEOR jar) is dropped from P3a before any baseline is scored, recorded in `FEID.json`. If CIDEr-D or BLEU-4 cannot be computed by r\*, P3 is NOT RUN.
- **P3a.** r\* (the released script, never run) reproduces every in-scope printed metric of both baselines in `PRINTED.json` within half a unit of the last printed digit. Informed by O3 (a seen proxy, E4 row `P4_T3bug…`), so it is POST HOC-informed for CIDEr-D and BLEU-4 and a registered prediction only for the other printed metrics ("Labels", below).
- **P3b.** No matched member of F reproduces the printed CIDEr-D of either baseline.
- **Labels.** P3b is POST HOC for `syl`, `rdr` and `pyvi` (O4) and is reported as a POST HOC check for every matched member. P3a is POST HOC-informed for CIDEr-D and BLEU-4 (O3: a seen proxy). The REGISTERED PREDICTION is P3a restricted to the in-scope printed metrics other than CIDEr-D and BLEU-4 (set M_new, from PRINTED.json): SUPPORTED if r* reproduces every metric of M_new for both baselines; otherwise NOT SUPPORTED, with the failing metric and the distance. If M_new is empty, P3 carries no registered label: the reproduction of CIDEr-D and BLEU-4 by r* is reported as POST HOC. The identification label and the margin are reported for each baseline.
- O5 (stored ROUGE-L under the E4 row `P4_T3bug…`) is not used for P3; it is reported, after P3, as POST HOC beside r\*.

### 6.4 P4, FE-ID planted check (METHOD CHECK, not a registered prediction)
- Because each planted member reproduces its own rounded scores under the same code, an IDENTIFIED class always contains the true member unless the code is wrong. A wrong recovery is therefore a FAULT (stage 3 stops; a re-run needs a judge line), not a FAIL.
- Reported: the IDENTIFIED, AMBIGUOUS and OUTSIDE counts among the 24 and the identifiability margins (the identifiability rate at one printed decimal).
- Fewer than 12 of the 24 IDENTIFIED: P3's identification label is NOT_EVALUABLE and FE-ID is reported as a reproduction table.

### 6.5 Human arm (registered in `B_PREF_LABELLING_PLAN_v1_1.md` §5)

- H-P (punctuation stratum, one-sided): the punctuation-removed order agrees with the raters' consensus in more than half of the decisive pairs.
- H-U (unit stratum, two-sided): which unit's per-image order agrees with the raters.
- **Use in the certificate.** The human result never changes F, a certificate, a P1 to P3 label or the P4 method check. It decides only which member the paper recommends as the default for reporting: if H-U is decisive, the unit that agrees more; if H-P is SUPPORTED, punctuation level pa; otherwise f0 stays the default and the paper says the human data did not separate the options.

### 6.6 Secondary and control rows (each labelled where printed; no verdict)

- **FE-PRED row.** Over D ∪ FL: the area under the ROC curve of |D_f0| / sd_boot(D_f0) for predicting CHANGED. Expected high (O1); reported to show that the margin under one member already predicts fragility.
- BLEU-4 and ROUGE-L certificates with the same rule.
- Certificates over F without ck, with `chr`, and without pk (sensitivity to the admissibility calls).
- **English control (CONTROL).** If at least three English output files of different systems exist on disk for one English test set (coordinator names them at the code read; unverified today), the English analogue family (units: PTB tokens, whitespace; case; pk to pa) is run on them and the CERTIFIED share is reported. Otherwise NOT RUN. No claim beyond Vietnamese is made from it (§14).

---

## 7. Multiplicity

- **Within a comparison**: none needed (§3.3).
- **Across comparisons**: no family-wise claim. The counts are counts of per-comparison 2.5%-per-direction decisions; the paper states that about 2.5% of comparisons with a true null under some member may be certified in error.
- **P1 to P3**: three separate threshold rules on three different questions, each reported with its own label; P4 is a method check (§6.4). No overall "success" statement combines them; none is dropped from the report.
- **Human arm**: Holm over H-P and H-U at family-wise 0.05 (labelling plan §5).
- **Secondary rows**: none carries a verdict.

---

## 8. Human arm

Registered in full in `B_PREF_LABELLING_PLAN_v1_1.md`: about 300 pairs (160 unit-flip, 100 punctuation-flip, 40 non-flip controls; CC-350 N2) plus 30 hidden repeats, two raters on all pairs, Cohen's κ on caption identity with thresholds 0.40 and 0.20, consensus as the decisive unit, Holm over two strata, a non-author-rater-only row, custody by line counts and hashes. The pairs come from the own `-short` files of D only; no FL file is shown to any rater.

---

## 9. Stages, order and custody

Each stage is a subcommand of `scripts/b_fecert/b_fecert.py`, refuses to start without the sha256 of its inputs and the LOG line of the previous stage, and writes its output sha256 with a `date -u` stamp. All stages run on the rented host (PI-1111j); the laptop writes files and serves the rating page only.

| Stage | Opens | Computes | Writes | May look |
|---|---|---|---|---|
| 0a documents (before any fetch or schema print) | — | the gatekeeper commit of this file v1.1, the labelling plan v1.1 and B_KAPPA v1 unchanged (CC-350 Q11) | commit id in LOG | — |
| 0b code (after the code read) | — | the gatekeeper commit of the code | commit id in LOG | — |
| F family | references, toy strings | F1 to F3 (§2.6); G-repro: f0 reproduces the committed CIDEr-D of the 67 own files that have a score file within 0.01 (B_KAPPA §5.1 rule: a mismatch on a seen file is a FAULT) | `FAMILY.json` | coordinator, judge |
| C census | file names, git index, gate print; the `segmenter` field of every stored result file named in `SYSTEMS.tsv` and of the b2_external score files (no score read) | `SYSTEMS.tsv` (name, stratum, family, sha256, role); D listed; segmenter census (CC-350 N4): any `underthesea` score on a system output moves `uts` to F_dev before stage 1 and is logged (F_held may then be empty, and P1 is then NOT_EVALUABLE); a character-unit score is logged only | `SYSTEMS.tsv`, `CENSUS.json` | coordinator, judge |
| G gate | FL files, schema print only | §4.3 | `GATE2.json`, logged | coordinator, judge |
| 1 dev | D files under F_dev | certificates over F_dev; NC (§6.1); human candidate table (labelling plan §2) | `DEV.json`, `NC.json`, `PAIR_CANDIDATES.json` (no text) | coordinator, judge |
| pin | — | — | LOG line with the sha256 of `DEV.json` and `NC.json`; read-only (444) copies under `.session_backup/2026-11-12/b_fecert/pins/` | coordinator |
| 2a first look, development family | FL files under F_dev; `DEV.json` | certificates of FL over F_dev; with D: Cert_dev, z_min, V (§6.1) | `V.json` (with the ids of V); the coordinator logs its sha256 | after the pin only |
| 2b first look, held-out members | D and FL files under F_held | held-out members on D and FL; all certificates over F; P1, P2; secondary rows | `RESULT.json` | after the `V.json` LOG line only |
| 3 FE-ID | KTVIC baselines, K2 and FL files with a printed value; `PRINTED.json`; planted files | plant, identify, compare; P3; P4 method check; §5.5 | `FEID.json`, `PLANT_KEY.json` | after `PRINTED.json` is logged |
| H human | label files after the closing LOG line | labelling plan §5 | `HUMAN.json` | after the labelling plan's closing line |

**Before the pin nobody may** run a held-out member on any system output, score any FL file, or change a threshold, the family or the gate. Stage 2a checks that no `RESULT*.json` exists and that the pin line precedes its start line. Stage 2b refuses to start without the V.json LOG line.

**After stage 2**, any further analysis on FL files is POST HOC. A FAULT stops the chain; a re-run after a fix needs a judge line and is disclosed.

---

## 10. Kill gates and evaluability

| Gate | Condition | Consequence |
|---|---|---|
| K-rdr | F1 fails for `rdr`, or G-repro fails on a seen file | FAULT; nothing proceeds |
| K-unit | F1 fails for `pyvi` or `uts` | that unit is dropped before any score, recorded in `FAMILY.json`; if F_held becomes empty, P1 is NOT_EVALUABLE |
| K-FL | fewer than 10 FL comparisons significant under f0 | P2 NOT_EVALUABLE; counts reported |
| K-FL20 | fewer than 20 formed FL comparisons | the application claim in the paper is descriptive ("k of n in a small pool"), as REDESIGN_B set it |
| K-N | N < 59 in the verdict set V after the fallback of §6.1 | P1 NOT_EVALUABLE |
| K-NC | r_NC ≤ 0.05 | P1 carries LOW-SENSITIVITY |
| K-print | `PRINTED.json` not logged by 2026-11-15 12:00 VN | P3 NOT RUN; O3 stays POST HOC in the text |
| K-coco | pycocoevalcap 1.2 or Java fails its host precondition for CIDEr-D or BLEU-4 | P3 NOT RUN; other in-scope metrics dropped one by one as §6.3 says |
| K-plant | fewer than 12 of 24 planted cases IDENTIFIED | P3's identification label NOT_EVALUABLE; FE-ID reported as a reproduction table (P4 method check, §6.4) |
| K-human | labelling plan §7 | as registered there |
| K-time | a stage not finished by 2026-11-16 12:00 VN | that stage NOT RUN, reported as such |

---

## 11. What is reported under each outcome

| Outcome | Paper text (neutral wording; no "first", no "wrong") |
|---|---|
| P1 PASS | Certificates on three units held under the held-out front ends (N, breaks, bound). If LOW-SENSITIVITY: the same sentence plus the NC figure and "the check had little room to fail" |
| P1 FAIL | The held-out units broke r of N certificates (bound). The paper recommends certifying over all four units of F and names the breaking unit (`uts`). The development-family certificate is not offered as sufficient |
| P1 INCONCLUSIVE / NOT_EVALUABLE | counts and bound only |
| P2 SUPPORTED | k of n significant comparisons among other groups' outputs change their conclusion with the front end, per repository and leave-one-out |
| P2 NOT SUPPORTED | "the certificate changed few conclusions in this pool (k of n)"; the method is then presented as a cheap check whose usual answer is CERTIFIED, with the counts |
| P3 SUPPORTED | Reported on the metrics never compared before (M_new): "The printed scores of the two KTVIC baselines are reproduced by pipeline r\* (every metric of M_new within half a unit); under matched scoring (f0) the values are Y". CIDEr-D and BLEU-4 stay POST HOC |
| P3 NOT SUPPORTED | the metrics that r\* does and does not reproduce, with distances; O3 stated as POST HOC |
| P4 wrong recovery: FAULT; fewer than 12 IDENTIFIED: reproduction table | a wrong recovery stops stage 3 (§6.4); with fewer than 12 IDENTIFIED, FE-ID is reported as a reproduction table without identification labels |
| Human | as the labelling plan §8 |

Every FAIL appears where a PASS would have appeared, at the same length.

---

## 12. Code and compute

**New folder `scripts/b_fecert/`; no existing file is edited.**

| File | Content | Self-test and mutants |
|---|---|---|
| `family.py` | §2: the steps, the axis levels, member enumeration, class merging, F1 to F3 | toy strings with known tokens per member; mutants: wrong step order (case before unit), pa keeps tokens of only punctuation, tm outside the g2 domain, mismatched application allowed into F, merging by score |
| `b_fecert.py` | stages F, C, G, 1, pin, 2a, 2b, 3, H; certificate, NC, P1 to P3, the P4 method check, FE-ID, planted check | synthetic fixtures in memory with known CERTIFIED, FRAGILE, REVERSED, NULL-STABLE and CHANGED cases, a known P1 PASS and FAIL, a planted identification, a wrong recovery raises FAULT; mutants: one-sided interval, resampling files instead of images, separate draws per member, CHANGED denominator over all comparisons, held-out member allowed before the pin, FL scored before `GATE2.json` is logged, reproduction tolerance of a full unit, held-out member scored before the V.json LOG line |
| `mutants.py`, `SHA256SUMS` | as in `scripts/b_kappa` plan | "killed n of n", exit 0 only if all |

Reused unchanged: `scripts/kit_b/protocol_pilot.py` (`rdr`, `Cider`, `bleu4`, `rouge_l`), `scripts/kit_b/ptb_protocol.py` (`load_refs`, `load_preds`, `sha`), the pin-line pattern of `scripts/b_pa1/b_pa1.py`.

**Compute (CPU, rented host).** Segmenting: about 76 KTVIC files × 558 outputs plus 2,790 references, and the FL files, under 18 (T, P) pre-unit variants per word unit; unique strings are cached. Bootstrap: one index matrix per image list (10,000 × |I|) multiplied by the per-image difference matrix of all comparisons and classes; about 10^11 multiply-adds for D, minutes on a 16-core host. FE-ID: 271 members on five files. Estimate: under one host day in total, unverified. No GPU.

**Code read**: one judge, FULL read, with self-tests and mutants re-run on the host, before the stage-0b commit. CC-350 ruling 11: the code read is ruled at the IRREVERSIBLE tier (bar 85), and its request says so. CC-350 ruling 12: it names the host for the self-tests, mutants and stages F to 3 under CC-346 R5, CC-349 3(c) and PI-1112b.

---

## 13. Calendar (Vietnam dates; results needed by 2026-11-16 12:00 VN)

| Date | Step | Gate |
|---|---|---|
| 11-12 | round-2 diff read; gatekeeper commit of this file v1.1, the labelling plan v1.1 and B_KAPPA v1 (reference); only then: fetch of the D2 files (separate agent, sha only), schema print, PRINTED.json by a separate agent; PI names the second rater | no judgement, no score |
| 11-13 | code, self-tests and mutants on the host; code read; stage-0b commit; stages F, C, G, 1; pin; assignment built and pinned (labelling plan §2.4 and §9); rating page tested on the host | nothing scored on FL before the pin |
| 11-13 evening to 11-15 18:00 | labelling by both raters | closing LOG line |
| 11-14 | stages 2a, 2b and 3 | result read (one judge) |
| 11-15 | stage H after the closing line; human result read | — |
| 11-16 12:00 | freeze | stages not finished are NOT RUN |

---

## 14. Paper-text clauses (binding on any writer)

- The certificate is called a combination of known ideas, credited as in §3.3. No "first" claim.
- Own-file results are DEVELOPMENT. FL results are "a first scoring of other groups' released outputs"; where the references are KTVIC or UIT-ViIC test references, the text says that those references were used before. Never "held-out test".
- The KTVIC finding is worded as reproduction facts: "the printed scores are reproduced by pipeline X; under matched scoring the values are Y". No sentence says that the published scores are wrong or erroneous. Its CIDEr-D and BLEU-4 part is POST HOC (seen October 2026).
- Paper B currently says "We rank no Vietnamese system" (sec5 l.27) and that no published system is rescored under the paper's protocol (sec3 l.36 source comment). Re-scoring the KTVIC baselines under f0 changes the second statement (§17 PI-3). Reporting CERTIFIED or FRAGILE verdicts on named other-group systems (the FL comparisons, K2 against the baselines) is a comparison of named Vietnamese systems and touches the first statement (§17 PI-6). Neither statement is changed without the PI's answer.
- No claim beyond Vietnamese. The English control is a control.
- The human arm says that one rater is an author if that is the case, and reports the non-author rater alone beside the consensus result.
- The 73 own files are described as variants of the authors' own systems; 12 of the 14 other-group systems have no paper; up to 20 of 32 FL comparisons come from one repository.

---

## 15. Limits (and which scorer objections the design answers)

| Objection (K41, K45) | Answered by the design? | How, or why not |
|---|---|---|
| Recombination of known arguments | No | It is a combination; §3.3 says so and credits each part. The design cannot change that |
| Most comparisons certify; few conclusions change | Partly | P2 pre-states the count that would matter and publishes it either way; the CHANGED denominator is fixed now |
| Held-out outcome foreseeable | Partly | pyvi moved to development; `uts` never run on outputs (`chr` not admissible, CC-350 ruling 2); NC measures, before the look, whether the check can fail; the rule has a FAIL branch |
| An author as rater | Partly | a non-author second rater (PI decision); the non-author-only row; blinding by display normalisation |
| Few systems with a paper | No | The pool is what exists (REDESIGN_B §1: "none found" beyond the KTVIC baselines). Reported plainly |
| Small user community | No | Vietnamese only, by rule |

Further limits: the own files are one backbone family; CIDEr-D is the only metric with a verdict; per-image human preferences say nothing direct about system-level orders; the family is enumerated, so nothing is guaranteed outside it; the bootstrap guarantee is nominal; KTVIC images and references were used before.

---

## 16. Open questions for the judge (each with a recommended answer)

| # | Question | Recommended answer | Default if no ruling |
|---|---|---|---|
| Q1 | Does PI-1111l ("Chốt hướng đi bài B theo khuyến nghị") cover REDESIGN_B D2 (fetch and first scoring of other groups' files) and D4 (retire the κ swap test)? The writer read the line to 300 characters | Coordinator quotes the full line in the ruling; if it does not cover D2, FL is limited to the already-fetched files | FL = fetched files only (G1 without references is then not formed) |
| Q2 | Tier and form | IRREVERSIBLE (it spends the first scoring of other groups' files and starts a human-labelled set): three-judge panel at 85. Codex is unavailable until 2026-11-27; the panel proceeds without it, recorded | panel, no Codex |
| Q3 | Is the character unit `chr` admissible (ViTextCaps C.2 uses it; it is the held-out member most able to break a certificate)? | **Yes**, with the "without `chr`" sensitivity row | No: F_held = `uts` only, and P1 will likely carry LOW-SENSITIVITY. **Ruled: not admissible (CC-350 ruling 2); F = 72, F_held = `uts`** |
| Q4 | pyvi in development, not held out (seen in E4) | Yes | as written |
| Q5 | P1 rule: verdict set = near-margin certificates (z_min ≤ 4) with fallback to all of Cert_dev below 59; Clopper–Pearson bounds at 0.05; INCONCLUSIVE between; FL as a separate row. Alternative: FL carries its own verdict (likely NOT_EVALUABLE, since FL gives at most 32 comparisons) | Yes, as written | as written |
| Q6 | P2 thresholds: n_FL ≥ 10; k_FL ≥ 3 and ≥ 10% | Yes | as written |
| Q7 | f0 = the committed P0 (punctuation kept), not the kit's PTB-style row | Yes: it is what the paper's numbers use, so CHANGED measures what would change for this paper's own reporting | as written |
| Q8 | Own files against the KTVIC baselines, and K1, stay out of D | Yes: the paper ranks no Vietnamese system and B-2 ranks none; the certificate on own pairs needs neither | out |
| Q9 | Gate v2 thresholds (95% coverage, 5% unknown ids, 1% duplicates and empties, 5% reference copies, 50% diacritic letters) | Yes | as written |
| Q10 | Case-kept (ck) members are admissible although no Vietnamese captioning scorer is known to keep case | Yes, with the "without ck" row; the breaking set shows when case alone breaks a certificate | as written |
| Q11 | Record that FE-CERT spends the "unseen under other forms" status of B_KAPPA's 49 U files; commit B_KAPPA v1 unchanged beside this file as a pinned reference (status "superseded; swap test retired, not run"), because §0 imports its definitions | Yes | as recommended |
| Q15 | P3 metric scope (BLEU-1 to 4, METEOR, ROUGE-L, CIDEr-D via pycocoevalcap 1.2) and the K-coco and K-plant gates (12 of 24 IDENTIFIED) | Yes | as written |
| Q12 | The eight-checkpoint GPU arm (REDESIGN_B D3; the writer could not confirm from the LOG whether the PI approved it) | Not in v1. If the PI's line covers it and the calendar allows, a separate run document and addendum | not run |
| Q13 | English control conditional on three English output files on one set | Yes | NOT RUN |
| Q14 | Stage order: dev and NC pinned before any held-out member or FL file is scored | Yes | as written |

**CC-350 rulings on these questions** (copied from CC-350; the rows above are v1's questions as asked):

- Q1  PI-1111l (16:01:21Z) predates REDESIGN_B (16:02-16:50Z), so it cannot cover D2 or D4. PI-1111n/o do not visibly cover them within 300 characters. D4 (retire the swap test of an unjudged, uncommitted draft) is a reversible technical call and is decided here: retired. D2: the fetch is licensed as in ruling 8(d).
- Q2  The commit is REVERSIBLE, with one judge (ruling 11). The code read that licenses the runs is IRREVERSIBLE tier. The absence of Codex is recorded.
- Q3  No (ruling 2): F = 72, F_held = uts. chr stays in F+ (271) and in the DESCRIPTIVE "with chr" rows.
- Q4  Yes. Also disclose the pyvi runs of b2.py (N3).
- Q5  Yes, with W1 (NC mirrors V; V is logged before any held-out run).
- Q6  Yes (n_FL >= 10; k_FL >= 3 and >= 10%).
- Q7  Yes. G-repro checks that f0 (with step N) reproduces P0.
- Q8  Yes, out of D.
- Q9  Yes, with the disclosure of N3. The thresholds lose the [proposal] tag in v1.1 (W4).
- Q10 Yes, with the "without ck" row.
- Q11 Yes. Commit B_KAPPA v1 unchanged beside v1.1 and cite its full sha in §0 (N5). Log one status line: "superseded, never registered; swap test retired, not run; only the sections imported by B_FECERT v1.1 bind". The same line records that B_KAPPA's 49 U files lose "unseen under other forms" when stage 1 runs.
- Q12 Not in v1 (agree).
- Q13 Yes. The coordinator names the files at the code read; otherwise NOT RUN.
- Q14 Yes, with stage 2 split into 2a and 2b (W1).
- Q15 Scope and K-coco: yes. K-plant (12 of 24): yes, within W2.

---

## 17. What only the PI can decide (each with a recommendation)

| # | Decision | Recommendation | Default |
|---|---|---|---|
| PI-1 | Who is the second rater | A native Vietnamese speaker who is not an author and has not seen the study's files; told only the instructions | the labelling plan's single-rater wording applies until a second rater has finished |
| PI-2 | How the KTVIC finding is worded toward the KTVIC authors, and whether the PI writes to them before submission | Neutral wording only: "the printed scores are reproduced by pipeline X; under matched scoring the values are Y". The PI writes to the authors before submission, sharing the reproduction table | kept out of paper text until the PI answers |
| PI-3 | May the paper print matched (f0) scores of the two KTVIC baselines? This changes "no published system is rescored" and uses the thesis-code author's verbal, unarchived permission reported in CC-092b (2026-10-22) to use the baseline outputs; CC-092 limits that use to aggregate statistics (a score is one), and the permission is cited as a personal communication only after its text is archived (CC-092b R6) | Yes, as aggregate scores with the permission cited, no ranking language | values computed, not printed |
| PI-4 | Whether the human arm needs an ethics or consent record (LRE asks for ethics and consent statements) | A one-paragraph written consent from each rater; no personal data stored beyond the rater code; the paper's ethics statement says so | written consent collected before labelling |
| PI-5 | How the second rater reaches the page | In person, on the PI's laptop (the server binds 127.0.0.1 only) | in person |
| PI-6 | May the paper report certificate verdicts (CERTIFIED, FRAGILE) on named other-group systems, given "We rank no Vietnamese system" (sec5 l.27)? A verdict says whether a comparison survives the front end, not which system is better, but it names both systems | Yes, with the systems named by repository and commit, the direction stated only as "the comparison of X and Y is (not) certified", and no league table | verdicts reported as counts by repository, systems not named |
