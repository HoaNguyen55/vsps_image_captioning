# A-CERT paper text v1: certifying a comparison under incomplete gold (Paper A, SPIC): transfer package

Written 2026-11-12T06:46:49Z (`date -u`). Writer agent. Run repo `/mnt/d/vsps_image_captioning`, branch `paper-v10`. Paper repo `/mnt/d/vsps_papers/vsps-paperA-spic` at `e8aa602` (read only; nothing edited there).

**Status.** Text package for a judge read. No result of the certification study exists in this file and none was looked for. Every result number is a named placeholder `{{file::key}}`. Nothing was run, committed or logged. AI opinion throughout. This file is not a registration: where it differs from a registered text, the registered text binds.

**Custody.** The writer did not open, list or stat `data/results/a_cert/` (gate, FREEZE or score), `data/results/a_cert_v/`, `data/results/a_cert_p/`, any label file, `~/vsps_labels/`, `key.json`, `assignment.json`, `~/.vsps_sealed`, `~/bpa1pull_1108`, `.session_backup/machines/`, `.session_backup/2026-10-27/a1_precheck/raw/`, `gt_cache.json` or any pulled model output. Read: the registrations and rulings below, the labelling plan v1.1, the two scripts (for output key names and fixed strings only), the paper text at `e8aa602` (sections 1-5, 6.1-6.3, 8, 9, the outline, Supplementary S1.M and Table S7.2), the study brief, the integrity files FIX_A2 and FIX_RESOLUTIONS_2026-11-10, and the first 30 lines of the untracked draft `A_CERT_ADDENDUM_E3_v1.md` (to learn its status only). LOG lines were read through `cut -c1-300` only. No caption text appears in this file.

**Forecast rule.** Registered texts and rulings contain forecasts of outcomes (A-CERT v1.1 §9; addendum VP §V.1, §V.5 "Expected now", §P.3 "Expectation", §11, §12; CC-333 Ruling 2 and P2; CC-335 Rulings 3, 5, 9 and P-2/P-3). None of them is carried into this file. The only forecast-flavoured strings kept are binding verbatim labels (the Part V label, the H2d label and the CC-343 disclosure sentence), because the registrations require them to be printed.

## 0. Sources and aliases

Registered texts (sha256 recomputed by the writer at the time above; first 16 hex digits):

| Alias | File | sha256 |
|---|---|---|
| R11 | `manuscript/prereg/2026-11-11_a_cert/A_CERT_ANALYSIS_REG_v1_1.md` (committed `0519b82`) | `e564b7b10cf500db` |
| VP | `manuscript/prereg/2026-11-11_a_cert/A_CERT_ADDENDUM_VP_v1_1.md` (committed `bd7ef1c`) | `0e586fa95814ef9e` |
| H2D | `manuscript/prereg/2026-11-11_a_cert/A_CERT_ANALYSIS_REG_v1_3_H2D.md` (committed `659f6c7`, LOG pin OPS-1111at) | `d0afcaf0390031f1` |
| PLAN | `manuscript/prereg/2026-11-11_xm600_gold_completion/XM600_GOLD_COMPLETION_PLAN_v1_1.md` | `8ad28f67fe4fbc3e` |
| E3RD | `manuscript/prereg/2026-11-12_a_e3_arm/A_E3_ARM_RUN_DOC_v1_1.md` | `1df371cc5e3b0f84` |
| CC-333, CC-335, CC-343, CC-347, CC-352 | `.session_backup/2026-10-13/decisions/CC-3xx.txt` | `466a4b580e3e463d`, `399096fd435cb5c9`, `d1647083ae428b2e`, `8ff9e21a6e383ba6`, `f49429297f522cff` |
| FIXA2 | `manuscript/directions/integrity_2026-11-10/FIX_A2_UITVIIC_WRITERS.md` | `890e2322d1d97758` |
| AC | `scripts/a_cert/a_cert.py` (the CC-343/CC-344 version) | `2e872588baf6109f` |
| ACVP | `scripts/a_cert/a_cert_vp.py` (CC-352 GO) | `17507200acd540fb` |

Added as a source by CC-357: `A_CERT_ADDENDUM_E3_v1.md`, committed in `2a39f87` at sha256 `64fad5185f019b50` (CC-355); it governs the other-family rows (J-27).

Output files named by the placeholders (paths from AC `P_REAL` and ACVP `V_REAL`, `P_REAL`; none was opened):

| Placeholder file | Path | Written by | Label the registrations attach |
|---|---|---|---|
| `FREEZE.json` | `data/results/a_cert/freeze/FREEZE.json` | `a_cert.py freeze` (label-free) | "development (no labels)" (R11 §8 l.226) |
| `A_CERT_RESULT.json` | `data/results/a_cert/score/A_CERT_RESULT.json` | `a_cert.py score` (one pass) | "single annotator; new labels on previously analysed captions" (AC `score_core`, key `label`) |
| `FREEZE_V.json` | `data/results/a_cert_v/freeze/FREEZE_V.json` | `a_cert_vp.py v-freeze` | Part V label (below) |
| `A_CERT_V_RESULT.json` | `data/results/a_cert_v/score/A_CERT_V_RESULT.json` | `a_cert_vp.py v-score` | "development; outcome foreseeable from stored aggregates and an unreviewed calculation (disclosed)" |
| `A_CERT_P_RESULT.json` | `data/results/a_cert_p/score/A_CERT_P_RESULT.json` | `a_cert_vp.py p-score` | "POST HOC; truth already scored by the paper" |
| `LOG.md` | `.session_backup/2026-10-13/decisions/LOG.md` | pin lines | times and shas only |

Placeholder forms: `{{FILE::key.path}}` = one stored value; `{{DERIVED: rule}}` = a stated derivation from stored values (manifest status DERIVED); `{{NO KEY YET: what}}` = a registered quantity whose output key does not exist yet. `<w>` in a key is the grid value as the code prints it (`"0.0"`, `"0.1"`, `"0.2"`, `"0.3"`, `"0.5"`); `<s>` is a system name; `<fam>` is `Q25` or `Q3`.

## 0.1 Notation: registered name → paper name

The paper's notation (Section 3.1, Section 4.1, Supplementary S1.M) already uses some of the letters the registrations use for other things. The text below uses the right-hand column. Every row is open point J-1.

| Registered (R11, VP, code) | Paper text here | Why renamed |
|---|---|---|
| systems `A`, `B`; `A` = higher observed precision | $A$, $B$ (same) | Section 3.3's method–comparator pair is $S$, $B$; here the pair is oriented by observation, so $A$, $B$ are kept |
| cells `B-only`, `A-only`, `S` (code keys `"B"`, `"A"`, `"S"`) | $\mathcal C_{B\setminus A}$, $\mathcal C_{A\setminus B}$, $\mathcal C_{A\cap B}$ | `S` is the paper's system symbol and S1.M's number of nameable pairs |
| `N_s` (all unknown mentions of system s) | $\mathcal N_S$ | – |
| `n_s`, `t_s` | $n_S$, $t_S$ | – |
| `U(cell)`, `X(cell)`, `x(cell)` | $u(\mathcal C)$, $X(\mathcal C)$, $x(\mathcal C)$ | S1.M's $U$ is the size of the union gold |
| `f1(cell)` (named by exactly one of the two references) | $\varphi_1(\mathcal C)$ | `f1` reads as $F_1$; S1.M already writes $\varphi_1$ for "named by exactly one reference" |
| floor `w`; `(F_w)` | $w$; (F$_w$): $w_{ic} \ge w$ for every present pair of the cell | S1.M writes $w_{ic} = P_i(c \in R)$ for the naming probability of a pair; the floor is a lower bound on it |
| `c = (1 − w)/(k·w)` | $c_w = (1-w)/(kw)$ | – |
| `β(cell; w)`, `α_S`, `α` | $\beta(\mathcal C; w)$, $\alpha_S$, $\alpha$ | – |
| (A0), (A1), (A1+) | (A0), (A1), (A1+) | (A1) is the paper's (A1) (Section 4.1, S1.M.1); (A0) and (A1+) do not collide with (A2)–(A4) of Section 4.1 or S1.M |
| `V_m` | $V_m$ (mapped classes, 69) | – |
| `I600`, `I537` | XM3600-600; its registered clean subset of 537 images (Section 6.3) | paper's names |
| `Q25`, `Q3` | first-backbone family (the six systems of Section 6.2); second-backbone family (the six XM3600-600 runs of Section 6.3) | paper's names |
| `P_c`, `_lo`, `_hi` | $P^{\mathrm c}$, $P^{\mathrm c}_{\mathrm{lo}}$, $P^{\mathrm c}_{\mathrm{hi}}$ | – |
| `b_F`, `b_P` | $b_F$, $b_P$ | – |
| `N_u`, `φ1`, `φ2`, `f̂0` | $\mathcal N_u$, $\varphi_1$, $\varphi_2$, $\hat f_0$ | S1.M's names |
| `G_top` | $G^{\mathrm{top}}$ | – |
| F-A, F-B, F-C (Part P image sets) | OPERA InstructBLIP set; OPERA set of LLaVA-1.5, MiniGPT-4 and Shikra; "Less is More" set | Table 6.1 calls F-B "English LVLMs, OPERA release" and F-C "Less-is-More release" |

---

## 1. Where each piece goes

### 1.1 Two homes, decided by the registered entry gate

The entry gate is fixed and unchanged (CC-335 Ruling 4): "The method enters Paper A only if K0 passed, no claimed floor has more than 5% certified errors, and H2a or COCO K2 passes. Otherwise the paper keeps the intervals, H1 and H3 as an audit extension and says the certificate was not validated." (VP §11 l.224, quoting METHOD_DELTA_A §7.) Whether a clause on H2d is added to it is the PI's decision (CC-335 P-2; VP §11 l.227; H2D Status l.20); no LOG line read by the writer records an answer (open point J-2).

The method text of §2 below is the same in both homes. Only its location and the abstract, introduction and contribution sentences differ. All seven registered verdicts on the labels, the Part V verdicts and the Part P rows are printed in both homes (Table 1 and the supplement); a verdict is never dropped because the gate is not met.

| Piece (this file) | Gate met (Home M) | Gate not met (Home S) | What it replaces or follows in the paper at `e8aa602` |
|---|---|---|---|
| §2.1 Problem; §2.2 definitions and worst case; §2.3 the two caps, the floor, $w^*$, slopes; §2.4 what "certified" means | new **Section 3.8** "Certifying a comparison when the gold marks only some present objects" | new **Supplementary S11.1–S11.3**, introduced as "a proposed rule that was not validated" (CC-335 Ruling 4 (i)); one pointer sentence in Section 8.1 | follows Section 3.7 ("A reporting proposal (untested)") |
| §2.5 Per-system precision interval (§4.4 of R11) | Section 3.8, last paragraph | **Section 6.7** (main text: "the paper keeps the intervals") | new |
| §2.6–§2.7 Human labelling protocol and completed quantities | **Section 6.7.1** | **Section 6.7.1** | new; Section 3.6 rule (iii) must change (§1.3 item E1) |
| §2.8 H1 (completed label-gold slope) | **Section 6.7.2**, with one sentence added to the "Reading." paragraph of Section 6.2 and one to the "Primary result." paragraph of Section 6.3 | same | follows the post hoc bound sentence of Section 6.2 ("counting unverifiable mentions as errors leaves +5.83 …"); on an H1b/H1c FAIL that sentence is replaced (§3.2) |
| §2.9 H2a, H2b (validity of the reference-only certificate) | **Section 6.7.3** | **Supplementary S11.4**; their verdicts in Table 1 and in one sentence of Section 6.7 that names each verdict (CC-357 J-39) | new |
| §2.10 H2d (break-down floor as a ranking) | **Section 6.7.4** | **Supplementary S11.4** | new |
| §2.11 H3 (coverage bound against the completed gold) | **Section 6.7.5**, plus one sentence at the end of Section 5.4 | same | follows the Section 5.4 sentence on the COCO-5000 coverage bound; Supplementary S1.M.6 gets one sentence |
| §2.13 Part V (COCO-5000, DEVELOPMENT) | **Section 6.8** (short) + **Supplementary S11.5** (full) | **Supplementary S11.5** only | new |
| §2.14 Part P (15 published comparisons, POST HOC) | **Section 6.8** (short) + **Supplementary S11.6**, and one sentence in Section 3.3 after "No count-control result in this paper is therefore confirmatory." | **Supplementary S11.6**; the Section 3.3 sentence kept | new |
| §2.12 Freeze, one pass, multiplicity | Section 6.7, first paragraph | Section 6.7, first paragraph | new |
| §4 Limitations and disclosures | **Section 9.1**: new paragraphs after "Construct validity: reference-only bound."; **Section 9.2**: one new paragraph | same | follows Section 9.1's paragraph on the reference-only bound |
| §5 Claim → evidence | `number_manifest.tsv` rows and the claim map of the writing plan | same | – |
| Abstract, highlights, contribution, RQ | §3.8 shells | §3.8 shells | Section 1.1 gets RQ4; Section 1 contribution list gets item 6 (Home M) or a narrower item (Home S) |
| Related work | **Section 2**, paragraph "F-measures, thresholds and incomplete gold.": one sentence; **Table 2.1**: the "This paper" row changes (§1.3 E2) | same | follows the sentence on species-accumulation curves |
| Registration ledger | **Table 1** (Section 1.2) new rows; **Supplementary Table S4.0** new rows | same | §3.9 below |

### 1.2 Supplementary section S11 (new, both homes)

"S11 Certification of a comparison under incomplete gold: derivations, the human-completed gold, a development check on COCO-5000 and a post hoc application to published comparisons". Subsections: S11.1 definitions and the closed form (Home S only; in Home M, Section 3.8 holds them); S11.2 the budget and its derivation; S11.3 why references alone certify nothing without a floor (the VP §V.4a identity); S11.4 every registered and secondary row on XM3600-600; S11.5 Part V; S11.6 Part P; S11.7 the labelling protocol in full (items, wording, answers, practice, custody); S11.8 code, pins and run records. The commit messages of `d13ae5c` and `2593f1d` call Part V and Part P "the certification appendix"; S11 is that appendix.

### 1.3 Existing sentences that become untrue or must change

| Id | Place at `e8aa602` | Current text (visible) | Why it must change | Replacement |
|---|---|---|---|---|
| E1 | Section 3.6, "Analysis code and provenance.", rule (iii) | "model-produced signals are never treated as gold or human evidence, and no new human annotation was collected" | the XM3600-600 completion collects new human labels | "(iii) model-produced signals are never treated as gold or human evidence; one set of new human labels was collected, for the object gold of XM3600-600, under a labelling plan and an analysis registration fixed before anyone but the annotator opened a label value (Section 6.7)" (open point J-3) |
| E2 | Table 2.1, row "This paper", column "Needs new labels?" | "No" | as E1 | "Yes, for one set: a human completion of the XM3600-600 object gold (Section 6.7); no new labels elsewhere" (J-3) |
| E3 | Table 2.1, row "This paper", column "Statistical guarantee" | "Image-bootstrap intervals, registered predictions, a size-matched random-deletion null" | the certificate adds a stated guarantee | Home M: append "; a certificate whose error probability is at most α under a stated naming floor (Section 3.8)". Home S: unchanged (J-3) |
| E4 | Section 6.2, "Reading." | "counting unverifiable mentions as errors leaves +5.83 [+3.82, +7.82] here, still above both reference slopes at point level" | R11 §6 l.170 | replaced only on H1b/H1c FAIL below the lower end (§3.2, sentence H1-F-low) |
| E5 | Section 6.3, "Primary result." | (no sentence on the bound) | R11 §6 l.169: on H1a FAIL Section 6.3's support "is contradicted" and the paper says so | one sentence appended on H1a FAIL (§3.2) |
| E6 | Section 9.1, "Construct validity: precision rule." | "The positive label-gold slope on XM3600 depends on the verified-precision rule: counting unverifiable mentions as errors leaves its interval including 0 …" | H1 measures what the bound only bracketed | one sentence appended (§3.2, sentence H1-9.1) |
| E7 | Section 9.1, "Construct validity: reference-only bound." | "The reference-only bound of Section 5.4 assumes exchangeable, independent writers (A1)." | the same (A1) now also carries the certificate and H3; FIXA2 rule: no corpus is described as having independent writers beyond its source | Ruled (CC-357 J-4): the sentence stays (FIXA2 §2.3 lists it as careful wording already in place); after the UIT-ViIC sentence that follows it, add: "The certificate of Section 3.8 and the test of Section 6.7.5 rest on the same (A1), which the diagnostic of Section 5 checks for reference order only." |
| E8 | Section 1, "Contributions" and Section 1.1 | five contributions, three RQs | new method and new labels | §3.8 shells |
| E9 | Section 8.5, "Conclusion." | counts of registered FAILs ("Nine registered predictions failed (Table 1)") | the seven label verdicts are registered predictions (the Part V verdicts are development rows and are not counted) | the existing count stays true for the earlier ledger, and Section 8.5 adds the §3.6 count line for the seven (E11; CC-357 J-5); no number is written now (J-5) |
| E10 | `declarations.md` and `anon/declarations_anon.md`, "Ethics" | "No new human annotation was collected and no human subjects were involved; all human judgments are public datasets used under their licences (Section 9.2). No ethics approval was required." | already untrue: the XM3600-600 labels are being collected | "One set of new human labels was collected: answers on whether object classes are present in public XM3600 images, given by one author and, on 150 of the images, by a second annotator (Section 6.7.1); no personal data were collected. All other human judgments are public datasets used under their licences (Section 9.2)." The sentence "No ethics approval was required." is kept only after the PI confirms it (CC-357); the tense of the second-annotator clause follows J-13. Phase A. |
| E11 | Abstract ("Nine registered predictions failed (two of five on Crossmodal-3600)."), Table 1 row head "FAIL (9)", Section 1 "The confirmatory claim." ("Our one confirmatory claim") | (as quoted) | the seven predictions on the new labels are registered predictions | Table 1 gets one new row group, "Registered on new labels of previously analysed images (development role; single annotator)", holding all seven verdicts by name; the existing groups, the count 9 and "one confirmatory claim" then stay true. After the results, Section 8.5 adds the §3.6 count line for the seven and the abstract adds one clause with the number of FAILs among them (none omitted). No number is written now. Phase B. |
| E12 | Supplementary S10 in both supplement files: the pre-revision copies of "Analysis code and provenance." (rule (iii)) and of the conclusion ("Nine registered predictions failed") | (as E1 and E11) | S10's own rule: "sentences later corrected to match their sources or the registered record follow the corrected wording" | the E1 replacement (Phase A) and the E11 clause (Phase B) are applied to the S10 copies in the same diff. |
| E13 | "the positive label-gold sign depends on excluding unverifiable mentions" and its variants: abstract, Section 1 "The confirmatory claim.", Section 6.2 "Reading." ("so the positive label-gold slope depends on excluding unverifiable mentions", beside E4), Section 8.5, highlight 4, cover letter, and the S10 copies of the Section 1 and Section 8.5 paragraphs in both supplement files | it stays true of the post hoc bracket, but H1 measures what the bracket only bounds | after the result read each place gets the H1 clause of §3.2 for its backbone (verdict word and "single annotator"); on an H1a FAIL, E5 also applies. No clause is written now. Phase B. |

### 1.4 Ride-along: FIX_A2 (UIT-ViIC "independent writers"), carried into this transfer

FIXA2 is not applied at `e8aa602`: `grep -c -F` on the paper repo at the time above gives `UIT-ViIC (all splits), VI | independent` 1/2/2 (sec5 / SPIC / supp), `independent-annotator` 1/1/1, `written by independent annotators` 0/1/1, `No single-writer corpus is tested here.` 0/1/1. No LOG line read by the writer (through `cut -c1-300`) records a ruling on FIXA2's Q1–Q11 (J-6).

Rules this file follows, from FIXA2:
- No sentence of this package says that any corpus's writers are independent. (A1) is called "a modelling assumption" on every set the certificate uses (XM3600-600, COCO-5000 and the released image sets of Part P) (FIXA2 §1.2, §2.3; S1.M.6).
- Where UIT-ViIC is named, it is described as "written by a panel of five writers (Lam et al., 2020, do not state whether one image's five captions come from different writers)" (FIXA2 W-04 default text). This package names UIT-ViIC only in the ride-along list below; no certification row uses UIT-ViIC.
- The transfer is applied after FIXA2 or together with it, so that the paper never holds both the new (A1) wording of E7 and the old "independent-annotator" sentences.

FIXA2 items to apply in the same paper diff, with their statuses as FIXA2 gives them: W-01 (sec5 Table 5.1 cell, NEEDS-JUDGE Q1), W-02 (Table S5.1 cell, NEEDS-JUDGE Q1), W-03 (Table S5.2 cell, NEEDS-JUDGE Q1), W-04 (sec5 grouping sentence, NEEDS-JUDGE Q2), W-05 (S5 sentence, NEEDS-JUDGE Q2, Q3), W-06 (S7 paragraph, READY), W-07 ("No single-writer corpus", NEEDS-JUDGE Q4), W-08 (no change proposed, NEEDS-JUDGE Q5). Each is located by its "old" string, not by line number (FIXA2 "Apply order").

---

## 2. The method section in full (paper text)

How to read this part. Each subsection gives paper text, ready to paste into the home named in §1.1, followed by an HTML comment naming the registered line(s) every sentence rests on. "Writer note" lines are not paper text. Numbers in the method text are registered design constants (not results); each also has a FREEZE key, given in the comment, so that the manifest can key it.

### 2.1 The problem (Section 3.8 opening; Home S: S11.1)

A comparison between two systems is usually read from the difference of an object score under one gold. When the gold marks only some of the objects present in an image, part of each system's mentions is neither confirmed nor rejected, and a conclusion such as "system $A$ names objects more precisely than system $B$" can depend on how those mentions would be settled. Section 6 shows that the sign of the verbosity slope changes with the gold, and Table S7.2 shows that on XM3600 the label-gold slope depends on how the mentions the labels cannot verify are counted. This section turns that finding into a decision for one comparison at a time: is its direction fixed by the incomplete gold alone, and if not, under what assumption on the missing part is it fixed?
<!-- src: R11 §4.1 l.97-98 ("An incomplete gold gives each mention one of three states"); CC-333 Ruling 2 l.95-98 (method "born from the paper's own finding (the sign of the slope depends on the gold, and the label gold is incomplete: Table S7.2)", output "a decision per comparison (CERTIFIED / NOT CERTIFIED, and the break-down floor w*)"); paper sec7 §6.2 "Reading." and supplementary_SPIC Table S7.2 l.600-605 (e8aa602). -->

**Three states.** An incomplete gold gives each mentioned (image, class) pair one of three states: known present, known absent or unknown. Two incomplete golds are used here. The XM3600 label gold (human-verified Open Images labels, Section 3.1) has all three: verified present, verified absent, and no status. A gold built from two references has only two: a class named by at least one of the two references is known present, and every other mentioned class is unknown; no pair is known absent. Counts are taken over the distinct mapped classes of each caption ($V_m$, the 69 lexicon classes that have an Open Images mapping), summed over images.
<!-- src: R11 §4.1 l.98; §4.2 l.114 ("Known present = named by at least one of the two. No pair is known absent. Unknown = named by neither."); §4.3 l.129 ("known present = verified present, known absent = verified absent, unknown = no status"); §1 l.55 (V_m, 69 classes, vi_oiv7_map.json 27f2b1ca); §2 l.71 and PLAN §5 l.48 ("distinct mapped classes per caption, summed over images"). -->

### 2.2 Definitions and the worst case (Section 3.8; Home S: S11.1)

For two systems $A$ and $B$ scored on the same images, let $n_S$ be the number of mentions of system $S$ and $t_S$ the number of its known-present mentions. The unknown pairs fall into three cells: $\mathcal C_{B\setminus A}$ (named by $B$ and not by $A$), $\mathcal C_{A\setminus B}$ (named by $A$ and not by $B$) and $\mathcal C_{A\cap B}$ (named by both); $u(\mathcal C)$ is the number of unknown pairs in cell $\mathcal C$. A *completion* declares $x(\mathcal C)$ of them present, with $0 \le x(\mathcal C) \le X(\mathcal C)$, where the cap $X(\mathcal C)$ is fixed below. Under a completion the precisions are
$$P(A) = \frac{t_A + x(\mathcal C_{A\setminus B}) + x(\mathcal C_{A\cap B})}{n_A}, \qquad P(B) = \frac{t_B + x(\mathcal C_{B\setminus A}) + x(\mathcal C_{A\cap B})}{n_B}.$$
<!-- src: R11 §4.1 l.99-102. Notation map §0.1 of this file (registered B-only, A-only, S, U, X, x). -->

**Orientation.** $A$ is the system with the higher observed precision $t/n$. An exact tie gives the verdict ABSTAIN. A system with $n_S = 0$ makes the pair NOT DEFINED; such pairs are counted and excluded.
<!-- src: R11 §4.1 l.104; AC certify() (verdict strings "ABSTAIN", "NOT DEFINED"). -->

**Worst case.** The difference $P(A) - P(B)$ is linear in the three $x$'s, so over all admissible completions it is smallest when no unknown pair of $A$ alone is present, every admissible pair of $B$ alone is present, and the shared cell is set to whichever end lowers the difference:
$$\Delta_{\min} = \frac{t_A}{n_A} - \frac{t_B + X(\mathcal C_{B\setminus A})}{n_B} + \min\!\Big(0,\ \frac{1}{n_A} - \frac{1}{n_B}\Big)\,X(\mathcal C_{A\cap B}).$$
The comparison is **CERTIFIED** if and only if $\Delta_{\min} > 0$, and **NOT CERTIFIED** otherwise; ABSTAIN counts as NOT CERTIFIED. The bound over every completion, and the use of one shared completion for both systems rather than two separate bounds, are not ours: Fernández-Barrios et al. (2026) give exact bounds of this kind over every completion for F1 rankings and report that shared completions tighten them. The form above is their idea specialised to precision with cells defined by which system names a pair.
<!-- src: R11 §4.1 l.106-109; CC-333 WHAT I CHECKED (1) l.57-59 (minimum at x_A = 0, x_B = X(B-only), x_S = X(S)·1[n_A > n_B]); CC-333 Ruling 2 (i) l.100-103 ("the w = 0 and C-label parts, including the shared-cell coupling, are already in 2611.01712"); CC-333 N8 l.228-229; VP §9 table row 1 l.201 ("Theirs ... not claimed as new"). Citation: arXiv 2611.01712, Fernández-Barrios, Pastor-López, González-Santocildes, García Bringas, "When Disagreement Labels Do Not Identify F1 Rankings" (CC-333 l.75-77, fetched by the judge; VP §9 l.197). The three frameworks that paper cites (Kuboyama, TDC, Polo et al.) are "chưa kiểm" (VP §14 l.262) and are not cited here. -->

### 2.3 The two caps: the label-side certificate and the reference-only certificate (Section 3.8; Home S: S11.1–S11.2)

**Label-side certificate (C-label).** With the Open Images statuses as the gold, the cap is $X(\mathcal C) = u(\mathcal C)$: every unknown pair may be present or absent. No assumption is made; the verdict holds for every completion of the label gold. Because a human answer never overrides an Open Images label (Section 6.7.1), the human-completed gold is one of these completions, so a C-label verdict can be contradicted by it only through the pairs the annotator left unsettled. C-label carries no hypothesis: it states which conclusions the Open Images labels already fix, whatever the human answers.
<!-- src: R11 §4.3 l.128-129; VP §V.4a l.79 ("The no-assumption headline belongs to C-label (v1.1 §4.3) only"); PLAN §5 l.41 ("An Open Images label is never overridden by a human answer"). FREEZE key per pair: FREEZE.json::pairs[*].clabel.verdict. -->

**Reference-only certificate (C-ref).** On XM3600-600 the reference gold is two Vietnamese references per image. For the 27 images with three references, two are drawn once (`default_rng(20261111)`, images in ascending identifier, `choice(3, 2, replace=False)`); taking the first two in file order is a sensitivity row without a verdict. With no known-absent pair, a cap that sets every unknown pair present ($X = u$) makes the precision of every system equal to 1, so **from references alone, no precision order and no slope sign can be certified without an assumption on how often present objects are named.** The reference-only certificate therefore rests on a *naming floor*. For a floor $w > 0$ the cap is $X(\mathcal C) = \min\big(u(\mathcal C), \lfloor \beta(\mathcal C; w)\rfloor\big)$, with
$$c_w = \frac{1-w}{k\,w},\qquad L = \ln\frac{2}{\alpha_S},\qquad \varphi_1^{+} = \varphi_1 + L + \sqrt{L^2 + 2L\varphi_1},$$
$$\beta(\mathcal C; w) = c_w\,\varphi_1 + \frac{(1+c_w)L}{3} + \sqrt{\Big(\frac{(1+c_w)L}{3}\Big)^2 + 2c_w(1+c_w)\,\varphi_1^{+} L},$$
where $\varphi_1 = \varphi_1(\mathcal C)$ is the number of pairs of the cell's system(s) named by exactly one of the $k$ references ($k = 2$ on XM3600-600). At $w = 0$ the cap is $X = u$, and the reference-only certificate certifies nothing; its rows at $w = 0$ are printed as computed.
<!-- src: R11 §4.2 l.114-118 (gold, seeded draw, first-two sensitivity row (CC-333 Q5, N2), f1(cell), caps, β = V-B); VP "What binds" l.25 (k a parameter, c = (1 − w)/(k·w), A2 plan §3.4) and CC-335 WHAT I CHECKED Math (1) l.59-61; VP §V.4a l.79 (erratum; the bold sentence is the sentence "The paper says:" verbatim; "The w = 0 rows of C-ref are computed and printed as registered"); CC-335 Ruling 2 l.101-104. Draw constants: FREEZE.json::refs_draw; seed FREEZE.json::constants.seed. Writer note: the sentence "makes the precision of every system equal to 1" restates VP §V.4a l.79 ("the completion that sets every unknown pair present gives precision 1 to each system"). -->

**What the floor means, and what is proved under it.** Write $w_{ic}$ for the probability that one reference of image $i$ names class $c$ (Supplementary S1.M.1). The floor assumption (F$_w$) is that $w_{ic} \ge w$ for every present pair of the cell. Suppose also (A0) that every pair a reference names is present, (A1) that the references of an image are independent draws from one law (Section 4.1), and (A1+) that the naming events of different pairs are independent given the image. Then $P\big(x(\mathcal C) > \beta(\mathcal C; w)\big) \le \alpha_S$ for the number $x(\mathcal C)$ of present pairs in the cell, so a CERTIFIED verdict is wrong with probability at most $\alpha$ for fixed outputs on these images. The argument: for a present pair named by $N$ of $k$ references, $P(N=0)/P(N=1) = (1-w_{ic})/(k\,w_{ic}) \le c_w$; summing over the pairs of the cell and applying Bernstein's inequality twice (once to bound the expected number of once-named pairs by $\varphi_1^{+}$, once to the sum) gives the budget, each step at level $\alpha_S/2$ (Supplementary S11.2). A second budget that drops (A1+), the image-level Hoeffding budget $\beta_H(\mathcal C; w) = c_w\,\varphi_1 + (1+c_w)\sqrt{\tfrac12\sum_i |O_i^{\mathcal C}|^2 \ln(1/\alpha_S)}$, with $|O_i^{\mathcal C}|$ the number of the cell's pairs on image $i$ (known and unknown), is reported beside it as a secondary row.
<!-- src: R11 §4.2 l.124 ("What is proved, and under what"; the proof sketch; "for fixed outputs on these images"); l.119 (V-H, CC-333 N2, Q2); CC-333 WHAT I CHECKED Math (2)-(4) l.60-65 (Lemma B; f1+; β with E1∩E2 each α_S/2); CC-335 Math (1) l.59-61 (k-general ratio (1−p)/(kp)). Writer note: R11 l.124 says "The paper labels V-B 'derived by the authors'"; the same line says "This derivation is an AI derivation" and that one judge checked it by hand (CC-333 Q2). How the paper words authorship of the derivation is open point J-7; this text says neither. -->

**Constants, fixed before anyone but the annotator opened a label value.** $\alpha = 0.05$ per verdict; $\alpha_S = 0.025$ for each pair cell, each per-system interval (end of this section) and each H2b budget; $\alpha_S = \alpha/m$ for the corners of a slope over $m = 6$ systems. Grid $w \in \{0, 0.10, 0.20, 0.30, 0.50\}$. The primary floor is $w_0 = 0.20$; the *weakest evaluable floor* $w_{\mathrm{ev}}$, the smallest grid value at which at least 10 of the 30 within-family pairs are CERTIFIED ("none" if no grid value reaches 10), is secondary. Both were fixed before the freeze, and the primary floor is not switched after it. $w_0 = 0.20$ came from an earlier, unreviewed calculation on COCO-5000 and has no further justification.
<!-- src: R11 §4.2 l.120 (constants; CC-333 N3, Q3, Q6), l.122 (w_ev); CC-333 Ruling 3 Q3 l.119; CC-333 WHAT I CHECKED l.70-72 ("w0 = 0.20: its only origin is the A2 plan l.118 COCO dry calculation (unreviewed scratch ...); the registration says it has no principled basis"); R11 §13 Q3 l.277. FREEZE keys: FREEZE.json::constants.{alpha, alpha_S, alpha_slope, grid, w0}, FREEZE.json::w_ev. Writer note: the last sentence discloses the origin of w0 (J-8). -->

**The break-down floor.** For each comparison, $w^*$ is the smallest floor at which it is CERTIFIED, found by 30 bisection steps on $[0.001, 1]$; it is reported as NI if the comparison is not CERTIFIED even at $w = 1$. ($w^* = 0$, certification without a floor, cannot occur for the reference-only certificate.) The smaller $w^*$, the weaker the assumption on the missing part that the comparison needs. The certified set grows with $w$, so $w^*$ orders comparisons by the strength of the floor assumption each one needs; whether that order tracks which comparisons hold under a fuller gold is what H2d tests (Section 6.7.4).
<!-- src: R11 §4.2 l.121; VP §V.4a l.79 and H2D §2 l.33 ("w* = 0 cannot occur, addendum VP v1.1 §V.4a; it would be a code fault"); CC-347 Ruling 3 #6 l.136-137 ("Refutation and certification are both up-sets in w"); CC-335 Ruling 9 l.200-201 ("the break-down floor w* is a per-comparison robustness score that reads the incompleteness of the gold"). FREEZE key: FREEZE.json::pairs[*].w_star. -->

**A slope.** For a family of systems, each system gets the precision interval $[\,t_S/n_S,\ (t_S + X(\mathcal N_S))/n_S\,]$, where $\mathcal N_S$ is the cell of all its unknown mentions. The slope interval is the minimum and the maximum of the ordinary least squares slope (Section 3.6) over the corners of these intervals: a system above the mean $\ln M$ takes its low end for the minimum and its high end for the maximum, and the reverse below the mean. The sign of the slope is CERTIFIED if and only if the interval excludes 0. The interval ignores that two systems can share an unknown pair, so it is an outer interval and can only fail to certify. The reference-only certificate certifies the precision slope only, because a completion would also change the recall measured against the reference gold. The label-side certificate gives the precision slope and the F1 slope with the registered recall held fixed. For a slope over $m$ systems each cell is taken at level $\alpha/m$.
<!-- src: R11 §4.1 l.111; CC-333 WHAT I CHECKED (5) l.66 ("the exact extreme of a linear function over a box; F with R fixed is monotone in P"); VP §V.4a l.79 (no C-ref slope sign at w = 0). FREEZE keys: FREEZE.json::slopes.<fam>.cref_P.<w>.{range, certified_sign}; FREEZE.json::slopes.<fam>.clabel.{F,P}.{range, certified_sign}. -->

### 2.4 What "certified" means and does not mean (Section 3.8; Home S: S11.1)

**Means.** A CERTIFIED comparison has the same direction under every completion of the gold that the cap allows. For the label-side certificate the cap allows every completion, and the statement needs no assumption. For the reference-only certificate the statement holds with probability at least $1 - \alpha$ under (A0), (A1), (A1+) and (F$_{w}$) at the stated floor, for the fixed captions on these images.
<!-- src: R11 §4.1 l.106-109; §4.2 l.124; §4.3 l.129; VP §V.4a l.79 ("Every C-ref verdict is conditional on (F_w) and the assumptions of v1.1 §4.2"). -->

**Does not mean.** A certificate says nothing when the floor fails, and the pairs it fails for are exactly the present objects that writers rarely name, which make up the unknown part. It says nothing about a re-run of a system, another image set, recall, mixed F1 or CHAIR$_s$. Proposition 2 (Section 5.4) cannot certify: it bounds the missing share from below, and a certificate needs a bound from above. The certificate uses the cap and the floor; Proposition 2 keeps the per-system intervals below and the test of Section 6.7.5. NOT CERTIFIED does not say that a comparison's direction is reversed; it says that the incomplete gold does not fix it at the stated floor.
<!-- src: R11 §4.2 l.126 ("What it does not guarantee"; "The paper uses these words (CC-333 Q1)"); CC-333 Ruling 3 Q1 l.114-115 ("Proposition 2 cannot certify. The certificate uses the cap and the floor; Proposition 2 keeps §4.4 and H3. Use these words in the paper."); VP §P.4 l.181 ("'Not certified' is always followed by 'this does not say the published result is wrong'"). Writer note: the last sentence generalises the §P.4 tail from published comparisons to every comparison; whether the paper may do so is open point J-9. -->

**Relation to prior work (one sentence for Section 2, paragraph "F-measures, thresholds and incomplete gold.", after the sentence on species-accumulation curves).** Bounds on a ranking over every completion of the missing labels are given by Fernández-Barrios et al. (2026) for F1 with single-label items; Section 3.8 uses them for precision on multi-label caption mentions, where a positives-only reference gold makes them empty, and adds a probabilistic cap on the unknown present objects from once-named counts under a naming floor.
<!-- src: VP §9 table l.199-207 (rows: "Theirs" all-completion bounds and shared completion; "outside (single correct label per item)"; "§V.4 shows the all-completion certificate is empty there"; "A probabilistic cap ... ours; elementary (Lemma B, Bernstein); no 'first' claim"); CC-333 Ruling 2 (i) l.100-103. Writer note: Table 2.1 may get a row for arXiv 2611.01712; its cells must come from that paper's text as VP §9 l.197 reads it (J-10). -->

### 2.5 Per-system precision interval (Section 3.8 last paragraph in Home M; Section 6.7 in Home S)

For each of the twelve systems on XM3600-600 the precision interval under the two-reference gold has the low end $(t_S + \hat L_S)/n_S$ and, for each grid floor $w$, the high end $(t_S + X(\mathcal N_S; w))/n_S$. Here $\hat L_S = \varphi_1^2/(4\varphi_2)$ (or $\varphi_1(\varphi_1-1)/4$ if $\varphi_2 = 0$), with $\varphi_1$, $\varphi_2$ the pairs of $\mathcal N_S$ together with the known-present mentions of $S$ named by exactly one and by both references: Proposition 2 with $k = 2$, applied to the pairs the system names. The low end is asymptotic, holds under (A0) and (A1), and is never used to certify. At $w = 0$ the high end is 1 for every system.
<!-- src: R11 §4.4 l.131-132; VP §V.4a l.79 ("The v1.1 §4.4 high end at w = 0 equals 1 for every system"); CC-333 Ruling 3 Q1 (Proposition 2 "keeps §4.4"). FREEZE keys: FREEZE.json::intervals_44.<s>.{n, t, U, f1, phi1, phi2, L_hat, low, high.<w>}; label "development (no labels)" (R11 §8 l.226). -->

### 2.6 The human-completed gold of XM3600-600 (Section 6.7.1; protocol in full in S11.7)

**Why labels were collected.** The Open Images V7 labels settle only part of the classes that captions name on XM3600-600, so Section 6.2 reports the label-gold slope under verified precision and brackets the unsettled mentions post hoc (Table S7.2). A human answer for each unsettled pair replaces that bracket by a measurement and gives a gold against which the certificate can be tested. The 600 images were analysed in this paper before (Section 6.2); the registered look at them is spent, and they are used here in a development role. No test set is touched and no model is decoded. Only the labels are new: every result that uses them is reported as "new labels on previously analysed captions".
<!-- src: PLAN §1 l.8-10, §7 l.56; R11 Disclosures l.42-43 (CC-333 N9 sentence: "XM3600-600 is Paper A's test set whose registered look is spent; it is used here in a development role (PI-1105k, PI-1107c). No test set is touched and no model is decoded."); CC-333 Ruling 4 l.136-138. -->

**Items.** One question is one (image, lexicon class) pair: "is an object of this class in the image?" The pairs are those named by any of the twelve stored caption sets of Sections 6.2 and 6.3 or by the Vietnamese references, as the paper's matcher extracts them (Section 3.1); 4,910 pairs are named. Part 1 holds the 1,790 named pairs whose class has an Open Images mapping and whose Open Images status is unknown, mixed on each image with 443 hidden control questions: 143 named pairs that Open Images verifies absent, 200 named pairs it verifies present (drawn at random) and 100 unnamed pairs it verifies absent (drawn at random), 2,233 questions in all. Part 2 holds the 2,100 named pairs whose class has no Open Images mapping; part 3 asks 150 random part-1 targets again. The 4,483 questions sit on 1,288 screens, one image per screen. Image order within a part and question order within a screen are random with a fixed seed.
<!-- src: PLAN §1 l.9, l.11; §2 l.14-21 (table and counts; seed 20261111); R11 §11 l.257 (gate reproduces "4,910 named pairs; 1,790 part-1 targets"); CC-333 Ruling 5 (2) l.148-149 (|part 1| − 1,790 = 443); AC constants N_TARGETS1 = 1790, N_NAMED = 4910, N_CTRL = 443, P_REAL part1_n = 2233. Manifest: these are design counts of manuscript/prereg/2026-11-11_xm600_gold_completion/BUILD.json (pinned in FREEZE.json::pins); keys open point J-11. -->

**What the annotator saw.** A mapped class is shown with the Open Images classes it maps to, and the annotator is told to read the class by them, so that targets and controls measure the construct of the Open Images labels. The answers are "yes", "no", "cannot be settled from the image" (U) and "the word does not name an object category" (A). Depictions (drawings, statues, printed pictures) and partly hidden or small objects count as present. A practice round on 15 XM3600 images outside the 600, with Open Images answers and feedback, precedes the task; practice answers are not data.
<!-- src: PLAN §2 l.23-25. -->

**Blinding.** The labelling page shows the image, the class and its hint. It shows no caption, no system name and no mark of which question is a target or a control. The annotator cannot see which system or reference named a class. Repeats are not hidden: they form part 3 and are asked after parts 1 and 2, so they measure agreement after a delay. Every answer is appended to a file; a changed answer is a new line, and the last line of a question is its answer. Until the analysis registration was committed, nobody but the annotator was shown a per-role, per-class or per-system figure.
<!-- src: PLAN §3 l.28-31; R11 §3 l.83 ("the last line of a qid is its answer"). Writer note: file paths, the server and the key file are not named in the paper (custody); S11.7 may name the tool by repository path (J-12). -->

**Who labelled.** One annotator, who is an author and knows the study, gives every answer used in the registered analysis. A second annotator, a colleague, answers every question of 150 of the images (25% of the images with a target, drawn with a fixed seed) with the same page and instructions, without seeing the first answers.
<!-- src: PLAN §3 l.29, §4 l.37, §7 l.56; R11 Disclosures l.39. Writer note: the PLAN says the second annotator "labels" (future); at the time of writing no second-annotator line was seen by the writer. Tense follows the state at transfer (J-13). -->

**Completed status.** A named pair is *present* if Open Images verifies it present or the human answer is yes, and *absent* if Open Images verifies it absent or the answer is no. U, A and unanswered pairs stay unsettled and form the *remainder*; they are counted. An Open Images label is never overridden by a human answer; the control questions measure the disagreement. Each pair keeps its own answer: a yes on one class settles no other class, including a hypernym, a hyponym or a synonym with the same mapping; disagreements between same-map synonyms on one image are counted and reported as a consistency figure. The part-1 answer is the label; the part-3 answer is used only for agreement within the annotator. Control questions never enter a status.
<!-- src: PLAN §5 l.41, l.44-47; R11 §2 l.64-70, §3 l.83-85 ("Part-3 lines and control roles never enter a status"); AC answers(), human(), counts() (as described in CC-343 Ruling 1 l.68-70). -->

**Quality measures, reported whatever their value; none gates anything.** Against Open Images: the share of the 443 control questions on which the yes or no answer equals the Open Images label, with U and A apart, reported separately for named-present controls, named-absent controls and unnamed-absent foils, and, for the absent questions, split by whether the Open Images rule that marked the pair absent covers every class shown in the hint or only part of them. Whether depictions count as present in the Open Images image-level labels is not verified. Within the annotator: agreement of the 150 repeats with the first answer. Between annotators: Cohen's kappa on yes against no over the part-1 target questions of the 150 overlap images that both answered yes or no, with raw agreement and PABAK beside it, and each annotator's U and A rates.
<!-- src: PLAN §4 l.35-37; R11 §6 l.153 ("Control agreement (443 questions) and repeat agreement (150) are reported whatever their value; they gate nothing"); CC-343 Ruling 5 l.264-265 and S1 l.294-299 (per role; split by hint coverage). Output keys: A_CERT_RESULT.json::quality.control_by_role.{ctrl_present,ctrl_absent,foil_absent}, ::quality.control_absent_by_hint_coverage.{full,partial}. Kappa: no output key yet (J-14). -->

**The kappa rule.** Until the second annotator has labelled the overlap images, every verdict that uses the labels carries the words "single annotator". Then a part-1 target kappa at or above 0.60 keeps each verdict, with kappa reported; a kappa below 0.60 turns every verdict into "sensitivity analysis only", printed with the table of disagreements. Nothing is recomputed and no threshold moves.
<!-- src: PLAN §4 l.38; R11 §6 l.153. -->

### 2.7 Quantities computed from the completed gold (Section 6.7.1)

For each system on its image set, over the distinct mapped classes of each caption summed over images: $p_m$ and $a_m$ count the mentions that Open Images verifies present and absent, $h_y$ and $h_n$ the mentions settled yes and no by the annotator, and $r$ the remainder. *Completed precision* is $P^{\mathrm c} = (p_m + h_y)/(p_m + a_m + h_y + h_n)$, the registered verified-precision formula with fewer unsettled mentions. Its two remainder ends set the remainder all absent or all present, $P^{\mathrm c}_{\mathrm{lo}} = (p_m + h_y)/(p_m + a_m + h_y + h_n + r)$ and $P^{\mathrm c}_{\mathrm{hi}} = (p_m + h_y + r)/(p_m + a_m + h_y + h_n + r)$, every system's remainder set the same way, as Table S7.2 is computed. F1 is computed under the recall gold of Section 6.2 (Open Images verified-present classes, unchanged) as $F^{\mathrm c} = 2P^{\mathrm c}R/(P^{\mathrm c}+R)$, with its two ends likewise. $b_F$ is the ordinary least squares slope of $100\,F^{\mathrm c}$ on $\ln M$ across a family, and $b_P$ the same for $100\,P^{\mathrm c}$; the slope, F1, recall and bootstrap functions are the registered ones, unchanged. Recall, F1, verified-negative hallucination and the share of captions naming an absent class are also reported under a second gold, Open Images plus human yes, labelled "pooled gold; favours systems that name more"; no verdict attaches to it, and the two golds are never mixed in one row.
<!-- src: R11 §3 l.85-93; PLAN §5 l.42-43, l.47-48; R11 §2 l.66; CC-343 S2 l.300-310 (gold (ii) definitions); AC GOLD_II_LABEL = "pooled gold; favours systems that name more"; AC pc_ends(), fam_slopes(). -->

**Image sets and bootstrap.** Statistics of the first-backbone family use the 600 images; those of the second-backbone family use its registered clean subset of 537 images; statistics over all twelve systems use the 600 images. Intervals are 95% percentile intervals from the registered image bootstraps: for the first-backbone family the first 500 rows of `default_rng(0).integers(0, 600, (2000, 600))`, for the second-backbone family `default_rng(0).multinomial(n, 1/n, size=1000)` over the clean subset; for H2a, H2d and H3, 2,000 multiplicity vectors from `a_m1.boot_weights(600, default_rng(20261111), 2000)` (the second-backbone pairs use its entries on the 537 images).
<!-- src: R11 §1 l.59; §2 l.77; §6 H2a l.186 (B = 2,000, seed 20261111), H3 l.199; H2D §3 l.40 and CC-336 Q3 (as recorded in H2D §6 l.67); CC-343 Ruling 3 (g) l.186 ("H2a bootstrap for I537 pairs reuses the I600 draws restricted to I537"). -->

### 2.8 Hypotheses H1 (completed label-gold slope), as registered (Section 6.7.2)

**H1.** The statistic is $b_F$, the F1 slope that Table S7.2 brackets; $b_P$ is reported beside it with its interval and carries no verdict. Every rule of H1 is evaluated at the registered value (remainder excluded) and at the two remainder ends, every system's remainder set the same way. For H1a the 95% interval is computed at the registered value only; at the two ends only the point is checked. PASS or FAIL is given only if its rule holds at all three; if the PASS rule or the FAIL rule holds at the registered value but not at both ends, the verdict is INCONCLUSIVE (remainder).

| Id | Family and images | Prediction | PASS | FAIL | Otherwise |
|---|---|---|---|---|---|
| H1a | second backbone, 537 images | $b_F > 0$ | point > 0 and the 95% interval excludes 0 | point ≤ 0 | INCONCLUSIVE, or INCONCLUSIVE (remainder) |
| H1b | first backbone, 600 images | $b_F$ inside [+5.83, +20.13] (Table S7.2) | point inside | point outside | INCONCLUSIVE (remainder) |
| H1c | second backbone, 537 images | $b_F$ inside [+1.97, +14.78] (Table S7.2) | point inside | point outside | INCONCLUSIVE (remainder) |

Reported with H1b and H1c: the paired-bootstrap interval of $b_F$ minus each end of Table S7.2. Reported with H1a: the Bonferroni interval (99.17%) beside the 95% interval.
<!-- src: R11 §6 "Remainder rule." l.155 (CC-333 B1 verbatim), H1 l.157-166; §7 l.216 (Bonferroni 99.17% beside H1a and H3); CC-343 Ruling 3 (g) l.183-184 ("The printed v1.1 bounds [5.83, 20.13] and [1.97, 14.78] bind. Report the stored ends 5.826/20.134/1.968/14.777 beside them"). The Table S7.2 ends are existing paper numbers with manifest rows 657-660. Output keys: A_CERT_RESULT.json::H1.{H1a,H1b,H1c}, ::H1.<fam>.{b_F, b_P, b_F_ci95, b_P_ci95, b_F_bonf, b_F_minus_S72_lower_ci95, b_F_minus_S72_upper_ci95, S72_ends_unrounded_from_FREEZE, direction}. -->

**Facts fixed before unsealing (post hoc; not predictions).** Before anyone but the annotator opened a label value, the range of the label-gold F1 slope over every completion of the unverifiable mentions (the label-side slope interval of Section 3.8) was computed from the stored outputs with the registered code and bootstrap and pinned: {{FREEZE.json::slopes.Q25.clabel.F.range}} for the first-backbone family and {{FREEZE.json::slopes.Q3.clabel.F.range}} for the second-backbone family; the precision-slope ranges are {{FREEZE.json::slopes.Q25.clabel.P.range}} and {{FREEZE.json::slopes.Q3.clabel.P.range}} (post hoc (stored outputs, no labels); recomputed at the freeze: development (no labels)). Table S7.2 sets every system's unverifiable mentions the same way, so it is not a bound on the slope: the completed slope can fall outside it. A computed $b_F$ outside the pinned range (and, for the second-backbone family, $b_P$ outside its range) would have been a code fault and stopped the analysis.
<!-- src: R11 §5 l.134-149 (B3 label "post hoc (stored outputs, no labels)"; "Table S7.2 ... is not a bound on the slope ... The completed slope can fall outside it"; "a computed b_F outside ... is a code fault: STOP"; N5 Q3 guard; "The freeze (§8) recomputes these with the registered code and bootstrap, and pins them"); R11 §8 l.226 ("development (no labels)"); AC score_core §5 STOP guard (F for both families, P for Q3). Writer note: the literal §5 values of R11 are not printed here; the paper prints the FREEZE values (J-15 on which of the two labels these numbers carry). -->

### 2.9 Hypotheses H2a and H2b (validity of the reference-only certificate), as registered (Section 6.7.3; Home S: S11.4)

**Units.** The 30 within-family pairs: 15 among the six first-backbone systems on the 600 images, 15 among the six second-backbone runs on the 537 images. The 36 pairs across families (on the 537 images) form a secondary row. The second-backbone runs are two prompts at three temperatures, so about 9 of its 15 pairs are short-against-detailed and 6 are near-copies; the effective number of independent comparisons is far below 30.
<!-- src: R11 §6 H2 l.175; §7 l.214. -->

**Truth.** A pair is *confirmed* if $P^{\mathrm c}(A) - P^{\mathrm c}(B) > 0$ in the certified direction (for a pair that is not certified, in the observed reference-gold direction) at the registered value and at both remainder ends. A tie is not confirmed. Only precision is used, so no verdict rests on the pooled gold. A pair that is ABSTAIN or NOT DEFINED is excluded from every count, null rule and evaluability count, and their number is printed.
<!-- src: R11 §6 "Truth." l.177; "Ties and undefined pairs." l.179 (CC-333 B2); AC confirmed(), h2a_rule(). -->

**H2a (primary, at $w_0 = 0.20$).** $V_c$ is the share of CERTIFIED pairs that are confirmed and $V_n$ the share of the other pairs that are confirmed.
- NOT EVALUABLE if fewer than 10 pairs are CERTIFIED or fewer than 10 are not; this is known at the freeze and was declared there, before unsealing.
- PASS: at most $\lfloor 0.05\, n_{\mathrm{cert}}\rfloor$ certified pairs are not confirmed (so $V_c \ge 0.95$), and $V_c > V_n$.
- VALID, NOT DISCRIMINATING: the first condition holds and $V_c \le V_n$.
- FAIL: more than $\lfloor 0.05\, n_{\mathrm{cert}}\rfloor$ certified pairs are not confirmed.

Reported whatever the verdict: $V_c$, $V_n$, the image-bootstrap 95% interval of $V_c - V_n$ with the certified set held fixed, the exact one-sided 95% lower limit $0.05^{1/n_{\mathrm{cert}}}$ when no certified pair fails (descriptive, because pairs share images and systems), and three null rules at the same count: certify every pair (constant), certify the $n_{\mathrm{cert}}$ pairs with the largest observed two-reference margin (margin; ties broken by pair index), and certify a pair if and only if the observed-better system names more (length; equal counts not certified). If the margin rule makes fewer errors than the certificate at the same count, the paper does not say the certificate beats a margin threshold.
<!-- src: R11 §6 H2a l.181-186; CC-333 Ruling 3 Q4 l.120; AC h2a_rule(), null_select(); output keys A_CERT_RESULT.json::H2a.{label, n_cert, n_other, n_excluded, n_cert_unconfirmed, limit, V_c, V_n, Vc_minus_Vn_ci95, exact_lower_limit, nulls.{constant,margin,length}.{n,errors}, margin_beats_certificate}; declared at the freeze: FREEZE.json::h2a_declared.<w>.{n_cert, n_other, n_excluded, evaluable}, FREEZE.json::h2a_evaluable_w0. -->

**H2a secondary rows (no verdict for the method).** H2a's counts at every grid floor and at $w_{\mathrm{ev}}$, each labelled VALID AT $w$ or REFUTED AT $w$ by H2a's error rule; the break-down floor $w^*$ of every pair beside its confirmed status; the cross-family pairs; the count of certified pairs that are unconfirmed only through the remainder; and the adversarial remainder corner (the pairwise worst case over the remainder).
<!-- src: R11 §6 l.193 (registered secondary row); §10 row CC-333 N6 l.246; AC score_core keys A_CERT_RESULT.json::H2a.{secondary_by_w.<w>.{n_cert, n_other, n_cert_unconfirmed, V_c, V_n, label}, cross_family_secondary, n_cert_unconfirmed_only_through_remainder, n_cert_confirmed_adversarial, pairs[*].{w_star, confirmed}}. -->

**H2b (budget coverage; always evaluable).** For each of the twelve systems on the 600 images, $x_S$ is the number of completed-present pairs in $\mathcal N_S$ and $x_S^{\mathrm{hi}}$ adds the remainder in $\mathcal N_S$. The system is *covered* if $x_S^{\mathrm{hi}} \le \lfloor \beta(\mathcal N_S; w_0)\rfloor$.
- PASS: at least 11 of 12 systems covered. FAIL: 10 or fewer. If the Open Images statuses alone already put two systems above the budget, FAIL is determined at the freeze and was declared there.
- If $\lfloor\beta\rfloor \ge u(\mathcal N_S)$ for all twelve systems, the budget never binds and the verdict is "PASS (vacuous)", which supports nothing. The number of systems whose budget binds was printed at the freeze.
- Reported per system and for every grid floor: $x_S$, $u(\mathcal N_S)$, $\beta$, and the measured effective floor $\hat w_S = \varphi_1/(\varphi_1 + 2x_S)$.
<!-- src: R11 §6 H2b l.188-191; AC h2b_rule(); keys A_CERT_RESULT.json::H2b.{label, n_covered, n_binding, systems.<s>.{x, x_hi, U, f1, beta.<w>, covered, w_hat}}; FREEZE.json::h2b_declared.{n_binding, n_oi_above_budget, determined}. -->

### 2.10 Hypothesis H2d (the break-down floor as a ranking), as registered (Section 6.7.4; Home S: S11.4)

**Label printed with every H2d number:** "registered on 2026-11-11 after the aggregate look on COCO-5000, before anyone but the annotator opened a human label value; the human answers are unseen by the analysts, the Open Images statuses that enter the outcome are partly seen (v1.1 §9)".

H2d asks whether $w^*$ orders the 30 within-family comparisons by robustness better than two rules that need no floor. Units are the 30 within-family pairs of H2a, pooled into one ranking, after the ABSTAIN and NOT DEFINED exclusions (fixed at the freeze); the outcome is 1 if the pair is confirmed (as in H2a) and 0 otherwise; $n_1$ and $n_0$ count the two classes. Three rankings, all read from the freeze: $w^*$ ascending (NI pairs lowest and tied with each other); the observed two-reference margin $|t_A/n_A - t_B/n_B|$ (larger ranked higher); and the length rule as a binary score (1 if the observed-better system names more, 0 otherwise, including equal counts). Equal scores are ties with half credit; no tie-break is used. For each ranking the AUC is the share of (confirmed, unconfirmed) pairs ordered correctly, ties counting one half, and $D = \mathrm{AUC}(w^*) - \max\big(\mathrm{AUC}(\text{margin}), \mathrm{AUC}(\text{length})\big)$.
- NOT EVALUABLE if $n_1 < 5$ or $n_0 < 5$ (known only after the labels, unlike H2a).
- PASS if $D \ge 0.10$ (the smallest effect of interest) and the 2.5th percentile of the bootstrap distribution of $D$ is above 0.
- FAIL otherwise.

The bootstrap uses 2,000 image-multiplicity vectors (`a_m1.boot_weights(600, default_rng(20261111), 2000)`, rows 1 to 2,000; the second-backbone pairs use the entries of the 537 images); the scores and exclusions are held fixed and the confirmed status is recomputed in each replicate; a replicate in which one class is empty gets $D^* = -1$ and their number is printed. Printed whatever the verdict: $n_1$, $n_0$, the excluded count, the NI count, the three AUCs, $D$ with its 95% interval, the same per family (descriptive), and the 0.36th percentile of $D^*$ (100α/14 = 0.357; Bonferroni over seven predictions; no verdict).
<!-- src: H2D Label l.18 (verbatim; AC H2D_LABEL), §1 l.28-30, §2 l.33-36, §3 l.39-44, §4 l.51-55 (SESOI 0.10, the writer's choice, accepted by CC-336 Q1 per H2D §6 l.65, l.73); CC-343 Ruling 1 H2d l.114-123 and (e) l.176-178 ("Print it as '0.36th percentile (100 alpha/14 = 0.357)'"; AC BONF7_TXT). Output keys: A_CERT_RESULT.json::H2d.{label, printed_label, reading, fail_adds, n1, n0, n_excluded, n_NI, AUC_w_star_margin_length, D, D_ci95, D_star_p036_bonferroni7, D_star_p036_label, n_replicates, n_replicates_empty_class, per_family_descriptive.<fam>}. Writer note: the SESOI rationale (H2D §4) goes to S11.4 in full (J-16). -->

### 2.11 Hypothesis H3 (the coverage bound of Section 5.4 against the completed gold), as registered (Section 6.7.5; one sentence at the end of Section 5.4)

**Universe.** $\mathcal N_u$ is the set of pairs (image, class) on the 600 images, with the class in $V_m$, that at least one of the twelve caption sets names and that have no Open Images status. It is fixed by the images and the stored outputs, independently of the labels. Inside it the completed gold is a full inventory up to the remainder.

**Statistic.** With the two references of Section 3.8, $\varphi_1$ and $\varphi_2$ count the pairs of $\mathcal N_u$ named by exactly one and by both references, and $\hat f_0 = \varphi_1^2/(4\varphi_2)$ is the estimator of Section 5.4 with two references. $X$ counts the pairs of $\mathcal N_u$ that neither reference names and that the annotator marked present; $X_{\mathrm{hi}}$ adds the remainder among them. $D = X - \hat f_0$ and $D_{\mathrm{hi}} = X_{\mathrm{hi}} - \hat f_0$, with the image bootstrap of Section 6.7.1 (2,000 replicates).

| Label | Rule |
|---|---|
| RESPECTED (PASS) | the 2.5th percentile of $D^*$ is above 0 |
| VIOLATED (FAIL) | the 97.5th percentile of $D^*_{\mathrm{hi}}$ is below 0 |
| INCONCLUSIVE | neither |
| NOT EVALUABLE | $\varphi_2 = 0$ or $\varphi_1 + \varphi_2 < 50$ |

VIOLATED means that the estimator predicts more unnamed pairs than exist among the pairs the systems name: either (A1) fails on these references or the references name classes that are absent. The number of reference-named pairs of $V_m$ whose completed status is absent is reported beside it. The Bonferroni interval (99.17%) is printed beside the 95% interval.
<!-- src: R11 §6 H3 l.195-208; §7 l.216; CC-333 WHAT I CHECKED (7) l.67-69 ("RESPECTED uses the low X and VIOLATED the high X. Conservative both ways"); FREEZE.json::h3.{N_u, phi1, phi2, f0_hat, evaluable} (declared at the freeze); A_CERT_RESULT.json::H3.{label, phi1, phi2, f0_hat, X, X_hi, D, D_hi, D_ci95, D_hi_ci95, D_bonf, ratio_X_f0, n_ref_named_completed_absent}. -->

**H3 secondary rows (no verdict).** The same on all system-named pairs of $V_m$ on the 600 images; the ratio $X/\hat f_0$; the low ends of the per-system intervals (Section 3.8) beside $P^{\mathrm c}$ for the twelve systems; and the form $D_L$ of Section 5.4's development check over all completed-present pairs, of which only "consistent" can be read, because the labels are not a complete inventory of the image.
<!-- src: R11 §6 l.210; CC-343 S3 l.311-315; AC h3_row(), dl_row(), dl_rule(); keys A_CERT_RESULT.json::secondary.H3_all_system_named.*, ::secondary.D_L.{D_L, D_L_ci95, label}, ::H2b.systems.<s>.{low_44, P_c}. Writer note: R11 l.210 carries a further clause on this row that this file does not reproduce (J-17). -->

### 2.12 Order, multiplicity and the single pass (Section 6.7, first paragraph)

**Freeze.** Before any label value was opened by anyone but the annotator, a label-free run computed every certificate, $w^*$, null-rule selection, per-system interval, label-side verdict and slope range, $\varphi_1$, $\varphi_2$ and $\hat f_0$ of H3, and the evaluability of H2a and H3, wrote them to a file, and fixed the file by its hash in the project log; the analysis registration was fixed with it. Every number from that file is labelled "development (no labels)", carries no verdict and changes no registered result of this paper.
<!-- src: R11 §8 l.224-228 (CC-333 B3, Q7, N7); CC-343 Ruling 4 l.221-225 (order: gate, freeze, FREEZE pinned); LOG pin OPS-1112h (2026-11-11T18:29:02Z; FREEZE c51ea7dc; also CC-347 l.126; the writer did not open the file). Placeholders: {{LOG.md::OPS-1112h.utc}}, {{LOG.md::OPS-1112h.sha256}}. -->

**One pass.** The scoring run reads the label file once, computes every statistic in memory, and writes its result only after every check passes; on any fault it writes and prints no statistic. A second fault would have stopped the analysis. The order is: the quality figures; H3; H2b; H2a with its secondary rows and H2d; H1; the secondary rows.
<!-- src: R11 §7 "Order." l.218; §12 step 5 "Fault rule." l.267 (CC-333 B4); H2D §5 l.58 (H2d right after H2a, same pass); AC score() and score_core(). Placeholder for the run: {{LOG.md::<score run line>.utc}} (no line exists yet; J-18). -->

**Multiplicity.** Seven predictions are registered on the labels: H1a, H1b, H1c, H2a, H2b, H2d and H3. Their rules are point or count rules, except the intervals of H1a, H2d and H3, which are 95% and uncorrected, as in the paper's other registrations (Section 3.6); a Bonferroni interval (99.17%) is printed beside those of H1a and H3, and the 0.36th percentile of the bootstrap distribution of $D$ (Bonferroni over seven) beside that of H2d. The paper prints how many were registered, passed, failed, were inconclusive and were not evaluable, and writes "all pass" only if all seven pass.
<!-- src: R11 §7 "Multiplicity." l.216; H2D §5 l.59 ("H2d is a seventh registered prediction: the v1.1 §7 count prints seven ... 'all pass' needs all seven"); CC-343 Ruling 3 (d) l.171-173 (H2d committed and pinned before any freeze, so not void). -->

### 2.13 Part V: a development check on COCO-5000 against a fuller gold (Section 6.8 short and S11.5 in Home M; S11.5 in Home S). Label: DEVELOPMENT

**Label printed with every Part V number:** "development; outcome foreseeable from stored aggregates and an unreviewed calculation (disclosed)". No Part V result is called a prediction, a validation or a confirmation.
<!-- src: VP §V.5 "Status" l.83 (CC-335 B2 verbatim: "None is called a prediction, a validation or a confirmation, in the paper, a card or a cover letter"); ACVP V_LABEL; CC-335 Ruling 3 l.106-115. -->

**Why it can be done.** On COCO-5000 (the 5,000 COCO Karpathy-test images of Section 6.1, spent development data of this paper) the nine first-backbone systems of Table 6.1 have five references per image and COCO instance labels. A gold built from $k$ of the five references is incomplete in the way the XM3600 reference gold is, while the union of all five references and the instance classes, $G^{\mathrm{top}}$ (the CHAIR gold of Section 3.3), is fuller. Because the reference-only certificate decides from the $k$ drawn references alone, its verdicts can be checked against the direction under $G^{\mathrm{top}}$. $G^{\mathrm{top}}$ is not complete; it is "instance-label-visible". All nine systems are one model family (first backbone, Vietnamese captions).
<!-- src: VP §V.2 l.53-63 (data; G0 licensed by PI-1110g; "All nine systems are one model family"), §V.3 l.67 (G_top definition; "instance-label-visible, not complete"); CC-333 N10 l.232 ("COCO-5000 is spent Paper A data in a development role"). -->

**Masking (M-ref, primary).** For each $k$, $k$ references are drawn without replacement from the five, per image (`default_rng(20261114 + 100k)`, images in ascending identifier), $R = 20$ times. Known present = named by at least one drawn reference; no pair is known absent. The certificate is the reference-only certificate with $c_w = (1-w)/(kw)$, the V-B budget and the grid of Section 3.8; the primary operating point is $k = 2$ and $w_0 = 0.20$, the operating point of XM3600-600, not re-tuned. $k = 1, 3, 5$ and the V-H budget are secondary rows.
<!-- src: VP §V.3 l.69; ACVP draws(), units_at(); CC-347 Ruling 1 l.73-75 (draw-major order accepted, Ruling 3 l.148). -->

**Masking (M-label, secondary).** Every (image, class) pair named by at least one system has its $G^{\mathrm{top}}$ status hidden with probability $h$, else kept (present or absent), with mean hidden share $u \in \{0.30, 0.57\}$ under two laws: uniform ($h = u$) and salience-dependent ($h \propto 1/(1+r)$, $r$ the number of the five references naming the pair, scaled to mean $u$ and capped at 1); `default_rng(20261115)`, $R = 20$. The certificate is the label-side certificate (no assumption). The hidden rates come from Open Images aggregates of the XM3600 first-backbone family and the reference counts, not from any outcome on COCO. A wrong label-side certificate here would be a code fault, so this row measures how often the no-assumption certificate decides, not whether it is right.
<!-- src: VP §V.3 l.71; §V.5 l.93 ("any wrong M-label certificate is a code fault: STOP, because C-label is exact over completions"); CC-335 Ruling 7 Q6 l.166 ("YES, as a power table only"). Keys: A_CERT_V_RESULT.json::primary_truth_G_top.M_label."u=<u> <law>".{n_units, n_certified, share_certified}. -->

**Verdicts.** Units are the 36 system pairs × 20 draws = 720 pair-draws at $k = 2$, clustered by pair; ABSTAIN and NOT DEFINED units are excluded and counted. A pair-draw's truth is the precision direction under $G^{\mathrm{top}}$, the certified direction for a certified unit and the observed direction otherwise; a tie under $G^{\mathrm{top}}$ counts as wrong. Cells are the worse-only and shared cells of each unit, 1,440 in all.

| Id | Estimand | Rule |
|---|---|---|
| V1 (primary) | $e_c$, the share of CERTIFIED pair-draws at ($k = 2$, $w_0$) whose truth is wrong | NOT EVALUABLE if fewer than 72 pair-draws are certified, or they come from fewer than 5 pairs, or fewer than 72 are not certified (declared at the freeze). PASS: $e_c \le 0.05$ and no pair is wrong in more than half of its certified draws. FAIL otherwise |
| V2 (floor) | share of cells with $x^{\mathrm{top}}(\mathcal C) > \lfloor\beta(\mathcal C; w_0)\rfloor$, $x^{\mathrm{top}}$ the unknown pairs of the cell that are in $G^{\mathrm{top}}$ | FLOOR SUPPORTED if the share ≤ $\alpha_S = 0.025$; FLOOR REFUTED otherwise |
| V3 (discrimination) | $e_n$, the share wrong among non-certified pair-draws | DISCRIMINATING if $e_c < e_n$ and the pair-cluster bootstrap 95% interval of $e_n - e_c$ excludes 0 (B = 2,000, `seed 20261116`, certified set held fixed); else NOT DISCRIMINATING |

The evaluability thresholds of V1 (72 of 720 certified, at least 5 pairs, at least 72 not certified) were set on 2026-11-11, after an earlier unreviewed calculation on the same data was known (Section 9.1).
<!-- src: VP §V.5 l.83 (thresholds set after the 222/720 figure; label), l.85-91 (units, table, fixed sentences), §V.3 l.67 (truth; tie wrong); ACVP v1_declare(), v_rules(), v2_rule(). Keys: FREEZE_V.json::v1_declared.{n_cert, n_pairs_cert, n_other, n_excluded, evaluable}; A_CERT_V_RESULT.json::registered.{V1,V2,V3}; ::primary_truth_G_top.V1_V3.{e_c, e_n, n_cert, n_pairs_cert, n_other, n_excluded, n_cert_direction_fails, pairs_failing_in_most_certified_draws, e_n_minus_e_c_ci95, n_replicates_empty_class}; ::primary_truth_G_top.V2.{label, n_cells, n_over_budget, share}. Writer note: the last sentence states the timing fact without the calculation's figures (J-19). -->

**Ranking check against a margin rule (COCO K2).** PASS if $\Delta_{\mathrm{cov}} \ge 0.05$ and the 5th percentile of its pair-cluster bootstrap is above 0; $\Delta_{\mathrm{cov}} \le 0$ is a fail. $\Delta_{\mathrm{cov}} = \mathrm{Cov@5\%}(C) - \max(B1, B2, B3)$ on the 720 units at $k = 2$ with the Part V truth, where Cov@5% is the largest share of units a ranking can take from the top while holding at most 5% wrong units. $C$ ranks by $w^*$ ascending (NI last; ties by $|\Delta|$ descending, then pair). $B1$ certifies all units or none, $B2$ ranks by the two-reference margin $|\Delta|$, $B3$ by the log ratio of mention counts. B = 2,000, `seed 20261113`. Unless COCO K2 passes, the paper never says that the certificate ranks comparisons better than a margin rule.
<!-- src: VP §V.6 first bullet l.98 (CC-335 B4 verbatim definition); ACVP k2_rule(), rankings(), cov5(), k2_label() ("PASS" / "NOT PASSED"); CC-347 Ruling 1 l.87-89 (B1 constant rule, B3 ties by |Δ|). Keys: A_CERT_V_RESULT.json::registered."COCO K2"; ::primary_truth_G_top."COCO K2".{label, Cov5, delta_cov, LB_p5}. -->

**Reported whatever the verdicts.** The share certified at every grid floor and $k$ (power); $w^*$ of each pair-draw beside its truth; the measured floor $\hat w = \varphi_1/(\varphi_1 + k\,x^{\mathrm{top}})$ per cell; a cross-fitted floor (calibrated on one image half, applied to the other, `seed 20261111`) with V1–V3 at it, labelled secondary; the 36-row pair table; the M-label power table; and every row again under the instance classes alone as the truth, with the number of reference-named pairs absent from the instance gold (the only truth under which (A0) can fail). A transported-threshold row (the margin threshold read from one half against $G^{\mathrm{top}}$, applied to the other half and to Part P) is secondary.
<!-- src: VP §V.5 l.93; §V.6 second bullet l.99; CC-347 W1 and CC-352 Ruling 2 W1 (V2 at the cross-fitted floor). Keys: A_CERT_V_RESULT.json::power.by_k.<k>.{V-B,V-H}.<w>; ::primary_truth_G_top.{pair_table, w_star_beside_truth, V2.cells[*].w_hat, cross_fit.{V-B,V-H}.{w0_by_half, V1, V3, V2, n_half_units_excluded_floor_0}, cross_fit.transported_margin}; ::secondary_instance_only_truth.{..., n_ref_named_pairs_not_in_instance_gold}; ::transported_threshold. -->

**Kill gates.** KV0: self-test, mutation test and input pins, otherwise no run. KV-EV: V1 NOT EVALUABLE at the freeze → Part V reports power only, and the paper says the certificate "was not validated". KV1: V1 FAIL → the floor $w_0$ is withdrawn in the paper for every data set, and Part P prints $w^*$ only, without CERTIFIED labels at $w_0$; the registered XM3600-600 verdicts are still computed and printed. KV2: V2 FLOOR REFUTED → the guarantee sentence of Section 3.8 is printed with "the floor assumption failed on COCO-5000 at w0", and, if V1 passes, the certificate is described as "empirically valid on the sets tested". KV3: a second fault goes to the PI.
<!-- src: VP §V.8 l.109-113; CC-335 Ruling 7 Q7 l.167-168; ACVP kv_block() (strings KV2_FLOOR, KV2_EMP, NOT_VALIDATED). Keys: A_CERT_V_RESULT.json::KV.{KV0, KV-EV, KV1, KV2, KV3}; ::sentences. -->

**Implementation note (S11.8, CC-352 N1).** The addendum names the Part V script `a_cert_v.py`; it is implemented as `scripts/a_cert/a_cert_vp.py`, modes `v-freeze` and `v-score`. This changes no computation.
<!-- src: CC-347 N1 l.264; CC-352 N1 l.204 (carried); CC-347 Ruling 3 l.147. -->

### 2.14 Part P: the certificate applied to 15 published comparisons (Section 6.8 short and S11.6 in Home M; S11.6 in Home S). Label: POST HOC

**Label printed with every Part P number:** "POST HOC; truth already scored by the paper". The methods sentence: "POST HOC (released outputs the paper had already scored under the full gold)".
<!-- src: VP §P.4 l.183, l.185 (CC-335 Ruling 6 additions); ACVP P_LABEL, METHODS_P (CC-347 l.40-41: "P_LABEL ... is on every Part P number, and METHODS_P is printed once"). -->

**Data.** The 15 published comparisons of Section 3.3 and Supplementary S3: 11 decoding comparisons (OPERA against greedy and against beam search on InstructBLIP, LLaVA-1.5, MiniGPT-4 and Shikra; VCD, OPERA and OPERA-fast against LLaVA-1.5-7B in the "Less is More" release) and 4 comparisons of the "Less is More" stopping method against its base models. Both groups released per-image CHAIR evaluation logs; the paper had already scored 24 systems from them (Section 3.3). The image sets are as released: one 500-image set shared by OPERA's LLaVA-1.5, MiniGPT-4 and Shikra runs, one for OPERA's InstructBLIP runs, and one for the "Less is More" rows; every same-image pair of systems (94, of which 15 are the published comparisons) is scored on the images both systems have. The logs were fetched once from `shikiw/OPERA` at commit `e1bb7632508bdfaa5cdaf5b69b64419688107da8` (MIT licence) and `yuezih/less-is-more` at commit `f26e187aadacc49a7cfc30443f0e9bae865b8e2e` (Apache-2.0); they are not redistributed. The public LVLMs behind these logs are named only as the sources of the released outputs.
<!-- src: VP §P.1 l.119-123, l.160 (N3 of CC-335: "each repository is cited with its commit and licence"); §P.4 l.183 ("The eight public LVLMs are named as the sources of released outputs only"); §P.3 "Units." l.177 (CC-335 B6); CC-347 Ruling 2 (iii) and W4 (images as stored = images with an instance entry, E1's rule). Placeholders for fetch facts: {{LOG.md::<fetch line>.sha256[25]}} (no line seen by the writer; J-18). -->

**Gold and matcher check.** $G^{\mathrm{top}}$ is the first five references of each image together with its instance classes, as in Part V; the check that the matcher reproduces the paper's earlier scoring uses every reference, as that scoring did. Before any certificate is computed, precision, mentions per caption and the image count of all 24 systems, recomputed from the fetched logs, must equal the stored rows of Supplementary S3 to the printed precision; a mismatch drops Part P.
<!-- src: CC-352 N4 l.208-209 (carried from CC-347 N4 l.271: "G_top = first five references ∪ instances (§V.3); the matcher gate uses every reference, as E1 did"); VP §P.2 l.165 (matcher-identity gate). Keys: A_CERT_P_RESULT.json::matcher_gate.{passed, systems.<s>.{recomputed, stored, equal}}, ::dropped. -->

**Reserved gold.** The gold class sets of these image identifiers had been reserved for a later test of other methods; they were opened for this row only, by the pinned scoring script, which writes counts only. The image set of that reserved test is analysed here with other systems (the released outputs above). That later test is not part of this paper, and no number computed here enters any of its frozen inputs.
<!-- src: VP §P.2 l.164 ("the paper states that the OC1 image set was analysed here with other systems"), l.167 (CC-335 B5 "No leakage into any frozen input"); PI-1111i (LOG l.2176, read through cut -c1-300: P-1 answered YES); CC-352 Ruling 5 step 9 l.165-166. Writer note: wording of the registered duty "the OC1 image set was analysed here with other systems" is J-20. -->

**P-a, reference-rung replay (primary row).** "If only $k$ references existed, as on Vietnamese benchmarks": the masking of Part V on each image set, $k \in \{1, 2, 3, 5\}$, $R = 20$ draws, the grid and $w_0$ of Section 3.8. For each published comparison and each $k$: the share of draws CERTIFIED in the method's direction, the share certified in the baseline's direction (a separate field, never added to the first), the median $w^*$, and whether a certified direction equals the direction under $G^{\mathrm{top}}$. The orientation comes from the reference draw, not from the published paper. Over the 94 same-image pairs, V1–V3 and V2 of Part V are computed and labelled "post hoc; truth already scored by the paper; other model families".
<!-- src: VP §P.3 l.171; CC-347 W2 l.242-251 and CC-352 Ruling 2 W2 l.73-80 (direction field; share_certified_w0 = method direction only); CC-347 W3 / CC-352 W3 (V2 over the 94 pairs); ACVP P_FAMILY_LABEL. Keys: A_CERT_P_RESULT.json::P_a.published[*].{comparison, k, image_set, n_images, median_w_star, share_certified_w0, share_certified_w0_baseline_direction, n_certified_method_direction, n_certified_baseline_direction, n_certified_equal_to_chair_gold_direction, sentence}; ::P_a.same_image_pairs.{n_pairs, V1_V3, V2}. -->

**P-b, the CHAIR gold itself (secondary row; no truth exists).** Known present = $G^{\mathrm{top}}$; unknown = every other mention; $k = 5$. The budget $\beta(\mathcal C; w)$ bounds the present pairs that no reference names; those of them that the instance labels mark, $I_0(\mathcal C)$, are known, so the cap is $X = \min(u, \lfloor\beta\rfloor - I_0)$, and a cell with $I_0 > \lfloor\beta\rfloor$ is printed as "floor refuted by the instance labels" (no certificate is issued at that floor). Both caps are printed. Output per published comparison: CERTIFIED or NOT CERTIFIED at $w_0$, and $w^*$.
<!-- src: VP §P.3 l.173; §13 Q8 recommended answer l.249 (CC-335 N2: "The cap is tighter than min(U, floor(β)) and can add certificates. Both caps are printed. No truth exists for P-b; secondary only."); ACVP p_b_row(), REFUTED_I0. Keys: A_CERT_P_RESULT.json::P_b[*].{comparison, image_set, n_images, I0_by_cell, w_star_cap_I0, w_star_cap_min_U_floor_beta, verdict_w0_cap_I0, verdict_w0_cap_min_U_floor_beta, certified_direction, cells_with_floor_refuted_at_w0, sentence}. -->

**Nothing in Part P is evidence for H2a or for any gate.** Every Part P row is a description of released outputs that the paper had already scored under the full gold.
<!-- src: VP §P.4 l.182 ("P-a counts as evidence for the registered H2a" is in "Never"), l.187 ("nothing in Part P is evidence for H2a or for any gate"). -->

---

## 3. Result tables and sentences as shells

Rules for this part.
- Every number is a placeholder. A sentence is chosen by the verdict string stored in the result file, never by reading the numbers.
- Source order for each sentence: **[code]** = a string the scoring code itself writes (printed verbatim); **[reg]** = a fixed sentence of a registered text or ruling (verbatim); **[CC]** = a paper claim a ruling states for that outcome; **[own]** = the writer's plain sentence for an outcome no registered text words (each listed in §6).
- Every sentence on the labels carries "(single annotator)" until the kappa line of §3.6 exists; then it carries the kappa clause or the "sensitivity analysis only" form (§3.6).
- Every Part V number carries the Part V label; every Part P number carries the Part P label; every H2d number carries the H2d label (§2.10); every FREEZE number carries "development (no labels)".

### 3.1 The freeze figures (Section 6.7, first paragraph; S11.4)

Sentence [own, from R11 §8 l.226 and CC-333 B3]: "Before anyone but the annotator opened a label value, the freeze fixed (development (no labels)): at $w_0 = 0.20$, {{FREEZE.json::h2a_declared."0.2".n_cert}} of the 30 within-family pairs were CERTIFIED by the reference-only certificate, {{FREEZE.json::h2a_declared."0.2".n_other}} were not and {{FREEZE.json::h2a_declared."0.2".n_excluded}} were excluded as ties or undefined; H2a was declared {{FREEZE.json::h2a_evaluable_w0 → "evaluable" / "not evaluable"}}; the H2b budget binds for {{FREEZE.json::h2b_declared.n_binding}} of the twelve systems{{FREEZE.json::h2b_declared.determined = "FAIL" → ", and the Open Images statuses alone put {{FREEZE.json::h2b_declared.n_oi_above_budget}} systems above it, so H2b FAIL was declared at the freeze"}}; H3 was declared {{FREEZE.json::h3.evaluable → "evaluable" / "not evaluable"}} ($\varphi_1$ = {{FREEZE.json::h3.phi1}}, $\varphi_2$ = {{FREEZE.json::h3.phi2}})."

Sentence [own] for the label-side certificate (C-label): "With the Open Images statuses alone, {{DERIVED: count of FREEZE.json::pairs[*] with scope ≠ "cross" and clabel.verdict = "CERTIFIED"}} of the 30 within-family comparisons were already fixed by the Open Images labels alone (development (no labels)); the sign of the label-gold F1 slope was fixed for {{DERIVED: list of <fam> with FREEZE.json::slopes.<fam>.clabel.F.certified_sign = true, or "neither family"}}."

**Table 6.7a (freeze, development (no labels)).** One row per within-family pair; secondary rows for the 36 cross-family pairs in S11.4.

| Pair (A vs B) | Family | Images | $n_A$, $n_B$ | $t_A$, $t_B$ | Reference-only certificate at $w$ = 0 / 0.10 / 0.20 / 0.30 / 0.50 | $w^*$ | V-H at $w_0$ | First-two references at $w_0$ | Label-side certificate |
|---|---|---|---|---|---|---|---|---|---|
| {{FREEZE.json::pairs[j].A}} vs {{…B}} | {{…scope}} | {{…n_images}} | {{…cells.nA}}, {{…cells.nB}} | {{…cells.tA}}, {{…cells.tB}} | {{…cref."0.0".label}} / {{…cref."0.1".label}} / {{…cref."0.2".label}} / {{…cref."0.3".label}} / {{…cref."0.5".label}} | {{…w_star}} | {{…vh."0.2"}} | {{…first_two."0.2"}} | {{…clabel.label}} |

Note to the table [reg, R11 §4.2 l.124 as corrected by VP §V.4a l.79]: "The $w = 0$ column of the reference-only certificate is computed and printed; it certifies no pair, as Section 3.8 shows." A pair printed "NOT CERTIFIED (ABSTAIN; …)" [code: AC `PRINT_LABEL`] is printed in the paper as "ABSTAIN (exact tie; excluded)" (J-21).

**Table 6.7a′ (freeze, development (no labels)).** Per-system precision interval under the two-reference gold, 600 images (Section 3.8, last paragraph; in Home S this table is in Section 6.7). In Home M this table follows Section 3.8; in Home S it is one of the three main-text items that remain.

| System | $n_S$ | $t_S$ | $u(\mathcal N_S)$ | $\varphi_1$, $\varphi_2$ | Low end (asymptotic; never used to certify) | High end at $w$ = 0 / 0.10 / 0.20 / 0.30 / 0.50 | Budget binds at $w_0$ |
|---|---|---|---|---|---|---|---|
| {{<s>}} | {{FREEZE.json::intervals_44.<s>.n}} | {{….t}} | {{….U}} | {{….phi1}}, {{….phi2}} | {{….low}} | {{….high."0.0"}} / {{….high."0.1"}} / {{….high."0.2"}} / {{….high."0.3"}} / {{….high."0.5"}} | {{….binds}} |

Note [reg, VP §V.4a l.79]: the $w = 0$ column is computed and printed as registered; every entry in it is 1 ("The v1.1 §4.4 high end at w = 0 equals 1 for every system") (J-42).

**Table 6.7a″ (freeze, development (no labels); the label-side ranges are also post hoc (stored outputs, no labels), Section 6.7.2).** Slope certificates. Reference-only: the precision slope (cells at level $\alpha/m$, $m = 6$). Label-side: the precision slope and the F1 slope with the registered recall held fixed (the ranges of Section 6.7.2).

| Family | Certificate | Slope | Floor | Range | Sign certified |
|---|---|---|---|---|---|
| {{<fam>}} | reference-only | precision | $w$ = 0, 0.10, 0.20, 0.30, 0.50 | {{FREEZE.json::slopes.<fam>.cref_P.<w>.range}} | {{FREEZE.json::slopes.<fam>.cref_P.<w>.certified_sign}} |
| {{<fam>}} | label-side | precision | – | {{FREEZE.json::slopes.<fam>.clabel.P.range}} | {{FREEZE.json::slopes.<fam>.clabel.P.certified_sign}} |
| {{<fam>}} | label-side | F1 (recall fixed) | – | {{FREEZE.json::slopes.<fam>.clabel.F.range}} | {{FREEZE.json::slopes.<fam>.clabel.F.certified_sign}} |

Sentence [own]: "Under the two-reference gold the sign of the precision slope is {{certified at the smallest floor {{DERIVED: smallest <w> with cref_P.<w>.certified_sign = true}} | not certified at any grid floor}} for the {{first | second}}-backbone family (development (no labels))." The $w = 0$ row is computed and certifies nothing (Section 3.8).

### 3.2 H1: completed label-gold slope (Section 6.7.2)

**Table 6.7b.** Completed label-gold slopes (single annotator; new labels on previously analysed captions). Slopes of F1 (and precision) on $\ln M$, in points, 95% image-bootstrap intervals; "lo"/"hi" = every system's remainder counted absent/present.

| Family (images) | $b_F$ [95%] | $b_F$ at lo, hi | $b_P$ [95%] | Table S7.2 bracket (stored ends) | $b_F$ − lower end [95%] | $b_F$ − upper end [95%] | Verdict |
|---|---|---|---|---|---|---|---|
| First backbone (600) | {{A_CERT_RESULT.json::H1.Q25.b_F.reg}} {{…H1.Q25.b_F_ci95}} | {{…H1.Q25.b_F.lo}}, {{…H1.Q25.b_F.hi}} | {{…H1.Q25.b_P.reg}} {{…H1.Q25.b_P_ci95}} | [+5.83, +20.13] ({{…H1.Q25.S72_ends_unrounded_from_FREEZE.lower}}, {{….upper}}) | {{…H1.Q25.b_F_minus_S72_lower_ci95}} | {{…H1.Q25.b_F_minus_S72_upper_ci95}} | H1b {{A_CERT_RESULT.json::registered.H1b}} |
| Second backbone (537) | {{…H1.Q3.b_F.reg}} {{…H1.Q3.b_F_ci95}} (99.17%: {{…H1.Q3.b_F_bonf}}) | {{…H1.Q3.b_F.lo}}, {{…H1.Q3.b_F.hi}} | {{…H1.Q3.b_P.reg}} {{…H1.Q3.b_P_ci95}} | [+1.97, +14.78] ({{…H1.Q3.S72_ends_unrounded_from_FREEZE.lower}}, {{….upper}}) | {{…H1.Q3.b_F_minus_S72_lower_ci95}} | {{…H1.Q3.b_F_minus_S72_upper_ci95}} | H1a {{…registered.H1a}}; H1c {{…registered.H1c}} |

Secondary row (no verdict; R11 §10, CC-333 N6): the slope corner over the remainder, {{A_CERT_RESULT.json::H1.<fam>.remainder_corner_F_secondary}}.

Sentences, chosen by `A_CERT_RESULT.json::registered.H1a`:
- **PASS** [own]: "On the second backbone's XM3600-600 outputs (537 images), with the mentions Open Images cannot verify settled by a human, the label-gold F1 slope is positive, $b_F$ = {{H1.Q3.b_F.reg}} {{H1.Q3.b_F_ci95}}, and it stays positive with the unsettled pairs counted absent or present ({{H1.Q3.b_F.lo}}, {{H1.Q3.b_F.hi}}): H1a PASS (single annotator)."
- **FAIL** [reg, R11 §6 l.169, with CC-333 N4]: "With the unverifiable mentions settled by a human, the label-gold slope of the second backbone is not positive; the registered PASS depended on excluding them." Followed by [own]: "($b_F$ = {{H1.Q3.b_F.reg}} {{H1.Q3.b_F_ci95}}; at the two ends of the unsettled pairs {{H1.Q3.b_F.lo}}, {{H1.Q3.b_F.hi}}; H1a FAIL, single annotator)" and by [reg]: "This contradicts Section 6.3's support for a positive label-gold slope on a second backbone. The registered verdict of Section 6.3 is unchanged; Section 6.2 already states that the second-backbone positive slope depends on excluding unverifiable mentions." Added to Section 6.3 "Primary result." (E5) [own]: "A later measurement with human labels did not support a positive label-gold slope for this backbone on these 537 images (Section 6.7.2, H1a FAIL, single annotator; new labels on previously analysed captions)."
- **INCONCLUSIVE (remainder)** [own]: "The PASS or the FAIL rule of H1a held at the registered value ($b_F$ = {{H1.Q3.b_F.reg}} {{H1.Q3.b_F_ci95}}) but not at both ends of the unsettled pairs ({{H1.Q3.b_F.lo}}, {{H1.Q3.b_F.hi}}), so H1a is INCONCLUSIVE (remainder): the pairs the annotator could not settle decide the outcome (single annotator)."
- **INCONCLUSIVE** [own]: "The completed slope of the second backbone is {{H1.Q3.b_F.reg}}, but its 95% interval {{H1.Q3.b_F_ci95}} includes 0: H1a is INCONCLUSIVE (single annotator)."

Sentences, chosen by `registered.H1b` (first backbone) and `registered.H1c` (second backbone); `H1.<fam>.direction` gives the side for a FAIL:
- **PASS** [own]: "On the {{first-backbone family (600 images) | second-backbone family (537 images)}}, the completed slope $b_F$ = {{H1.<fam>.b_F.reg}} lies inside the post hoc bracket of Table S7.2 ({{bracket}}) at the registered value and at both ends of the unsettled pairs: {{H1b | H1c}} PASS (single annotator)."
- **FAIL, below the lower end** [reg, R11 §6 l.170]: "Counting unverifiable mentions as errors did not bound the slope from below." For H1b this triggers E4: the Section 6.2 sentence "counting unverifiable mentions as errors leaves +5.83 [+3.82, +7.82] here, still above both reference slopes at point level" is replaced [own; the registered duty is "replaced by the certified range of §5"] by: "counting unverifiable mentions as errors gives +5.83 [+3.82, +7.82] here, but a human completion of those mentions gives {{H1.Q25.b_F.reg}} (Section 6.7.2; single annotator), below that value; over every completion of the unverifiable mentions the slope lies in {{FREEZE.json::slopes.Q25.clabel.F.range}} (post hoc (stored outputs, no labels))". For H1c the second-backbone clause of the same Section 6.2 sentence ("but +1.97 [−0.44, +4.01] on the second backbone's XM3600-600 outputs") gets the same addition with the Q3 keys.
- **FAIL, above the upper end** [reg, R11 §6 l.171 "the same for the upper end"; wording own]: "Counting unverifiable mentions as correct did not bound the slope from above." With the same replacement duty for the upper end.
- If `direction` holds both "below" and "above" (the three points on different sides), both sentences are printed.
- **INCONCLUSIVE (remainder)** [own]: "The completed slope $b_F$ = {{H1.<fam>.b_F.reg}} lies {{inside | outside}} the Table S7.2 bracket at the registered value but not at both ends of the unsettled pairs ({{lo}}, {{hi}}): {{H1b | H1c}} is INCONCLUSIVE (remainder) (single annotator)."

Sentence when H1a, H1b and H1c are all PASS [reg, R11 §6 l.172, CC-333 N4]: "the paper's reading stands, and the post hoc bound is supplemented by a measurement on new labels (single annotator)".

Sentence appended to Section 9.1 "Construct validity: precision rule." (E6) [own]: "With those mentions settled by a human annotator, the completed label-gold slope is {{H1.Q25.b_F.reg}} {{H1.Q25.b_F_ci95}} on the first backbone and {{H1.Q3.b_F.reg}} {{H1.Q3.b_F_ci95}} on the second (H1a {{registered.H1a}}, H1b {{registered.H1b}}, H1c {{registered.H1c}}; single annotator; Section 6.7.2)."

### 3.3 H2a and H2b: validity of the reference-only certificate (Section 6.7.3; Home S: S11.4)

**Table 6.7c.** H2a at $w_0 = 0.20$ and at every grid floor (single annotator; certified set and orientation from the freeze).

| Floor | Certified | Not certified | Excluded | Certified, not confirmed | $V_c$ | $V_n$ | Reading |
|---|---|---|---|---|---|---|---|
| $w_0$ = 0.20 (primary) | {{A_CERT_RESULT.json::H2a.n_cert}} | {{…H2a.n_other}} | {{…H2a.n_excluded}} | {{…H2a.n_cert_unconfirmed}} (limit {{…H2a.limit}}) | {{…H2a.V_c}} | {{…H2a.V_n}} | H2a {{…registered.H2a}}; $V_c - V_n$ {{…H2a.Vc_minus_Vn_ci95}} |
| $w$ = 0, 0.10, 0.30, 0.50, $w_{\mathrm{ev}}$ = {{FREEZE.json::w_ev}} (secondary) | {{…H2a.secondary_by_w.<w>.n_cert}} | {{….n_other}} | – | {{….n_cert_unconfirmed}} | {{….V_c}} | {{….V_n}} | {{….label}} |
| Null: constant | {{…H2a.nulls.constant.n}} | – | – | {{…H2a.nulls.constant.errors}} | – | – | no verdict |
| Null: margin | {{…H2a.nulls.margin.n}} | – | – | {{…H2a.nulls.margin.errors}} | – | – | no verdict |
| Null: length | {{…H2a.nulls.length.n}} | – | – | {{…H2a.nulls.length.errors}} | – | – | no verdict |
| Cross-family pairs (secondary) | {{…H2a.cross_family_secondary.n_cert}} | {{….n_other}} | {{….n_excluded}} | {{….n_cert_unconfirmed}} | {{….V_c}} | {{….V_n}} | {{….label}}, no verdict |

Note to the table [reg CC-343 N9 l.331-332]: a secondary row printed "VALID AT $w$" with no certified pair (always the case at $w = 0$) is printed "vacuous (no pair certified)".

Sentences, chosen by `registered.H2a`:
- **NOT EVALUABLE** [own, from R11 l.182]: "H2a could not be evaluated: at $w_0 = 0.20$ the reference-only certificate certified {{FREEZE.json::h2a_declared."0.2".n_cert}} of the within-family pairs and left {{FREEZE.json::h2a_declared."0.2".n_other}} uncertified, and at least 10 of each were needed; this was declared at the freeze, before unsealing."
- **PASS** [CC, CC-335 Ruling 4 (ii): "validated on a human-completed gold (single annotator, N certified pairs)"; surrounding words own]: "At $w_0 = 0.20$, {{DERIVED: H2a.n_cert − H2a.n_cert_unconfirmed}} of the {{H2a.n_cert}} certified comparisons held under the human-completed gold ($V_c$ = {{H2a.V_c}}), against $V_n$ = {{H2a.V_n}} for the uncertified ones ($V_c - V_n$ {{H2a.Vc_minus_Vn_ci95}}): H2a PASS. The reference-only certificate at $w_0$ is validated on a human-completed gold (single annotator, {{H2a.n_cert}} certified pairs)."
- **VALID, NOT DISCRIMINATING** [reg, R11 l.184]: "the certificate made no error, and the uncertified reference-gold orderings held as often" when `H2a.n_cert_unconfirmed` = 0, followed by [own] "($V_c$ = {{H2a.V_c}}, $V_n$ = {{H2a.V_n}}; single annotator)". When `H2a.n_cert_unconfirmed` > 0 (possible only with 20 certified pairs, allowance 1) [reg, corrected by CC-357 J-22]: "the certificate made {{H2a.n_cert_unconfirmed}} error, within the registered allowance of {{H2a.limit}}, and the uncertified reference-gold orderings held at least as often ($V_c$ = {{H2a.V_c}}, $V_n$ = {{H2a.V_n}}; single annotator; the registered sentence says "made no error", which would be untrue here)".
- **FAIL** [reg, R11 l.185]: "the floor w0 is refuted on a two-reference Vietnamese gold; only the no-assumption certificate may be used there". Followed by [CC-357 J-23]: "From references alone that certificate certifies nothing (Section 3.8); the label-side certificate is unaffected ({{H2a.n_cert_unconfirmed}} of {{H2a.n_cert}} certified comparisons unconfirmed, allowance {{H2a.limit}}; single annotator)."
- Added whatever the verdict when `H2a.exact_lower_limit` exists [own]: "No certified comparison was unconfirmed; with {{H2a.n_cert}} dependent pairs the exact one-sided 95% lower limit of the share that holds is {{H2a.exact_lower_limit}} (descriptive)."
- Added when `H2a.margin_beats_certificate` = true [own, from R11 l.186]: "At the same count the margin rule made {{H2a.nulls.margin.errors}} errors against the certificate's {{H2a.n_cert_unconfirmed}}, so we do not say that the certificate beats a margin threshold."
- Added whatever the verdict [own, CC-333 N6]: "{{H2a.n_cert_unconfirmed_only_through_remainder}} certified pairs are unconfirmed only through the unsettled pairs."

**Table 6.7d.** H2b, budget coverage at $w_0$ (single annotator; 600 images).

| System | $u(\mathcal N_S)$ | $\lfloor\beta(\mathcal N_S; w_0)\rfloor$ | $x_S$ | $x_S^{\mathrm{hi}}$ | Covered | $\hat w_S$ | $P^{\mathrm c}$ | Interval low end (Section 3.8) |
|---|---|---|---|---|---|---|---|---|
| {{<s>}} | {{A_CERT_RESULT.json::H2b.systems.<s>.U}} | {{DERIVED: floor(H2b.systems.<s>.beta."0.2")}} | {{….x}} | {{….x_hi}} | {{….covered}} | {{….w_hat}} | {{….P_c}} | {{….low_44}} |

Sentences, chosen by `registered.H2b`:
- **PASS** [own]: "The budget at $w_0 = 0.20$ covered the human-completed present pairs among the unknown mentions of {{H2b.n_covered}} of the twelve systems (at least 11 needed): H2b PASS (single annotator)."
- **FAIL** [own]: "The budget at $w_0 = 0.20$ covered the human-completed present pairs of only {{H2b.n_covered}} of the twelve systems (11 needed): H2b FAIL (single annotator); for the other systems more unknown mentions were present than the budget at $w_0$ allows."
- **FAIL declared at the freeze** (when `FREEZE.json::h2b_declared.determined` = "FAIL") [own]: "H2b FAIL was already determined at the freeze: the Open Images statuses alone put {{FREEZE.json::h2b_declared.n_oi_above_budget}} systems above the budget."
- **PASS (vacuous)** [reg-derived, R11 l.190 "it supports nothing"]: "No system's budget binds at $w_0$, so H2b is PASS (vacuous); it supports nothing."

**Table 6.7d′ (secondary; no verdict).** Recall, F1, verified-negative hallucination and the share of captions naming an absent class per system on the 600 images, under the two golds, never mixed in one row (single annotator).

| System | Gold (i) recall | $P^{\mathrm c}$ (reg / lo / hi) | F1 under gold (i) (reg / lo / hi) | Hallucination, gold (i) | Captions naming an absent class, gold (i) | Gold (ii) recall | F1 under gold (ii) | Hallucination, gold (ii) | Captions naming an absent class, gold (ii) |
|---|---|---|---|---|---|---|---|---|---|
| {{<s>}} | {{A_CERT_RESULT.json::secondary.golds_I600.gold_i.systems.<s>.recall}} | {{….gold_i.systems.<s>.P_c.reg}} / {{….lo}} / {{….hi}} | {{….gold_i.systems.<s>.F1.reg}} / {{….lo}} / {{….hi}} | {{….gold_i.systems.<s>.hallucination}} | {{….gold_i.systems.<s>.share_naming_absent}} | {{….gold_ii.systems.<s>.recall}} | {{….gold_ii.systems.<s>.F1}} | {{….gold_ii.systems.<s>.hallucination}} | {{….gold_ii.systems.<s>.share_naming_absent}} |

Column heads for gold (ii) carry [code, AC `GOLD_II_LABEL`] "pooled gold; favours systems that name more"; gold (i) is "Open Images verified classes, as registered" [code]. No sentence draws a conclusion from gold (ii) (PLAN §5 l.43: "No verdict attaches to (ii)").

### 3.4 H2d: the break-down floor as a ranking (Section 6.7.4; Home S: S11.4)

Every H2d number carries the label of §2.10 ({{A_CERT_RESULT.json::H2d.printed_label}}, printed verbatim).

**Table 6.7e.** H2d (single annotator; scores from the freeze).

| Pooled within-family pairs | $n_1$ | $n_0$ | Excluded | NI | AUC($w^*$) | AUC(margin) | AUC(length) | $D$ [95%] | 0.36th percentile of $D^*$ | Verdict |
|---|---|---|---|---|---|---|---|---|---|---|
| both families | {{A_CERT_RESULT.json::H2d.n1}} | {{…H2d.n0}} | {{…H2d.n_excluded}} | {{…H2d.n_NI}} | {{…H2d.AUC_w_star_margin_length[0]}} | {{…[1]}} | {{…[2]}} | {{…H2d.D}} {{…H2d.D_ci95}} | {{…H2d.D_star_p036_bonferroni7}} ({{…H2d.D_star_p036_label}}) | {{…registered.H2d}} |
| first backbone only (descriptive) | {{…H2d.per_family_descriptive.Q25.n1}} | {{….n0}} | {{….n_excluded}} | {{….n_NI}} | {{….AUC_w_star_margin_length}} | | | {{….D}} {{….D_ci95}} | – | no verdict |
| second backbone only (descriptive) | {{…H2d.per_family_descriptive.Q3.n1}} | … | | | | | | | – | no verdict |

Replicates with an empty class: {{…H2d.n_replicates_empty_class}} of {{…H2d.n_replicates}}.

Sentences: the code writes the registered reading itself; print `A_CERT_RESULT.json::H2d.reading` verbatim [code = reg, H2D §3 l.47-49]. Its three forms:
- PASS: "the break-down floor w* ranked the robustness of comparisons better than the observed margin and the length rule on a new benchmark's human-completed gold (single annotator, {n1+n0} dependent pairs)". H2D l.47 adds, and the paper prints: "It is not a validation of the floor guarantee (that is H2a and H2b) and changes no H2a verdict."
- FAIL: "On the human-completed gold of XM3600-600 (single annotator, {n1+n0} dependent pairs), the break-down floor w* did not rank the comparisons better than the observed two-reference margin and the length rule by the registered amount (D = {D}, 95% interval {lo} to {hi}; SESOI 0.10). With {n1+n0} dependent pairs the test has low power; this result alone does not show that w* ranks worse." Followed, only when `H2d.fail_adds` is not null, by: "the rule with the larger AUC (margin or length) ranked them better than w* here".
- NOT EVALUABLE: "H2d could not be evaluated: {n1} confirmed and {n0} unconfirmed pairs, at least 5 of each needed." The AUCs are then printed as descriptive figures with no reading.

### 3.5 H3: the coverage bound against the completed gold (Section 6.7.5; one sentence in Section 5.4)

**Table 6.7f.** H3 (single annotator; 600 images).

| Universe | $\varphi_1$ | $\varphi_2$ | $\hat f_0$ | $X$ | $X_{\mathrm{hi}}$ | $D$ [95%] (99.17%) | $D_{\mathrm{hi}}$ [95%] | $X/\hat f_0$ | Reference-named pairs completed absent | Verdict |
|---|---|---|---|---|---|---|---|---|---|---|
| $\mathcal N_u$ (registered) | {{A_CERT_RESULT.json::H3.phi1}} | {{…H3.phi2}} | {{…H3.f0_hat}} | {{…H3.X}} | {{…H3.X_hi}} | {{…H3.D}} {{…H3.D_ci95}} ({{…H3.D_bonf}}) | {{…H3.D_hi}} {{…H3.D_hi_ci95}} | {{…H3.ratio_X_f0}} | {{…H3.n_ref_named_completed_absent}} | {{…registered.H3}} |
| All system-named pairs of $V_m$ (secondary; {{J-17: the parenthetical of R11 l.210, verbatim, inserted only in Phase B}}) | {{…secondary.H3_all_system_named.phi1}} | {{….phi2}} | {{….f0_hat}} | {{….X}} | {{….X_hi}} | {{….D}} {{….D_ci95}} | {{….D_hi}} {{….D_hi_ci95}} | – | – | {{….reading_no_verdict}}, no verdict |
| $D_L$ over all completed-present pairs (secondary) | {{…secondary.D_L.phi1}} | {{….phi2}} | – | – | – | $D_L$ {{….D_L}} {{….D_L_ci95}} | – | – | – | {{….label}}, no verdict |

Sentences, chosen by `registered.H3`:
- **RESPECTED** [own]: "Among the system-named pairs that Open Images does not settle, the pairs that neither reference names and the annotator marked present outnumber the estimate of Section 5.4 ($X$ = {{H3.X}} against $\hat f_0$ = {{H3.f0_hat}}; $D$ {{H3.D_ci95}}), as Proposition 2's lower bound requires: H3 RESPECTED (single annotator)."
- **VIOLATED** [reg-derived, R11 l.208]: "The estimate of Section 5.4 predicts more unnamed pairs than exist among the pairs the systems name ($X_{\mathrm{hi}}$ = {{H3.X_hi}} against $\hat f_0$ = {{H3.f0_hat}}; $D_{\mathrm{hi}}$ {{H3.D_hi_ci95}}): H3 VIOLATED (single annotator). Either (A1) fails on these references or the references name classes that are absent; {{H3.n_ref_named_completed_absent}} reference-named pairs were completed as absent."
- **INCONCLUSIVE** [own]: "The completed gold neither respects nor violates the bound at the registered level ($D$ {{H3.D_ci95}}, $D_{\mathrm{hi}}$ {{H3.D_hi_ci95}}): H3 INCONCLUSIVE (single annotator)."
- **NOT EVALUABLE** [own, from R11 l.206]: "H3 could not be evaluated: the two references name {{H3.phi1}} pairs of the universe once and {{H3.phi2}} twice, fewer than the registered minimum (both counts positive and at least 50 together); this was known at the freeze."
- Sentence for the end of Section 5.4 [own]: "On XM3600-600, with two references and a human completion of the object gold, the test of the bound gave {{RESPECTED | VIOLATED | INCONCLUSIVE | NOT EVALUABLE}} (Section 6.7.5; single annotator)."
- Sentence for Supplementary S1.M.6 [own]: "A test of the bound against a human-completed gold on XM3600-600 is in Section 6.7.5."

### 3.6 Annotator agreement, the kappa rule and the count line (Section 6.7.1, 6.7)

**Table 6.7g.** Label quality (descriptive; gates nothing).

| Measure | n | Agreement (all) | Agreement among yes/no | U | A |
|---|---|---|---|---|---|
| All controls | {{A_CERT_RESULT.json::quality.n_control}} | {{…quality.control_agreement_of_all}} | {{…quality.control_agreement_among_YN}} | {{…quality.control_U}} | {{…quality.control_A}} |
| Named present | {{…quality.control_by_role.ctrl_present.n}} | {{….agreement_of_all}} | {{….agreement_among_YN}} | {{….U}} | {{….A}} |
| Named absent | {{…quality.control_by_role.ctrl_absent.n}} | … | … | … | … |
| Unnamed absent (foils) | {{…quality.control_by_role.foil_absent.n}} | … | … | … | … |
| Absent, full hint coverage | {{…quality.control_absent_by_hint_coverage.full.n}} | … | … | … | … |
| Absent, partial hint coverage | {{…quality.control_absent_by_hint_coverage.partial.n}} | … | … | … | … |
| Repeats (part 3) | {{…quality.n_repeat}} ({{…quality.repeat_answered}}) | {{…quality.repeat_agreement}} | – | – | – |
| Same-map synonym disagreements | {{…quality.synonym_disagreements}} | – | – | – | – |
| Second annotator, part-1 targets of 150 images | {{NO KEY YET: kappa run}} | raw {{NO KEY YET}}; κ {{NO KEY YET}}; PABAK {{NO KEY YET}} | – | {{NO KEY YET}} | {{NO KEY YET}} |

Notes: U and A rates by class go to S11.7 ({{A_CERT_RESULT.json::quality.UA_rate_by_class}}). The repeat row prints "partial (k of 150 answered at the part-1 unsealing)" when `quality.repeat_answered` says so [reg, CC-343 Ruling 4 l.234-237; AC `repeat_label`]. Beside the control rows [reg, PLAN §4 l.35]: "Whether depictions count as present in the Open Images image-level labels is not verified."

Kappa sentences [own, from PLAN §4 l.38 and R11 §6 l.153]:
- Before the second annotator: every label verdict sentence carries "(single annotator)".
- κ ≥ 0.60: "A second annotator labelled the 150 overlap images; on the part-1 targets both answered yes or no, Cohen's kappa is {{NO KEY YET}} (raw agreement {{NO KEY YET}}, PABAK {{NO KEY YET}}), at or above the registered 0.60, so the first annotator's labels are the completed gold." The words "(single annotator)" are then replaced by "(two annotators on 150 images, κ = {{NO KEY YET}})".
- κ < 0.60: "On the 150 overlap images Cohen's kappa is {{NO KEY YET}}, below the registered 0.60; every result that uses the labels is therefore a sensitivity analysis only, and the table of disagreements is in Supplementary S11.7." Every verdict word in §3.2–§3.5 is then followed by "(sensitivity analysis only)". Nothing is recomputed and no threshold moves.

Count line [own, from R11 §7 l.216 and H2D §5 l.59]: "Seven predictions were registered on the labels: {{DERIVED: count of verdicts in A_CERT_RESULT.json::registered equal to "PASS" or "RESPECTED"}} passed, {{DERIVED: count of "FAIL" and "VIOLATED"}} failed, {{DERIVED: count of verdicts beginning "INCONCLUSIVE"}} were inconclusive and {{DERIVED: count of "NOT EVALUABLE"}} were not evaluable{{DERIVED: if a verdict is "VALID, NOT DISCRIMINATING" or "PASS (vacuous)" → "; {{count}} ended with a verdict that is neither a pass nor a failure ({{each such verdict by name, e.g. H2a VALID, NOT DISCRIMINATING}})"}} (Table 1)." The sentence "all pass" is written only if each of the seven verdicts is "PASS" or, for H3, "RESPECTED" (CC-357 J-24: "VALID, NOT DISCRIMINATING" and "PASS (vacuous)" are named, never counted as passed).

### 3.7 Part V shells (Section 6.8 and S11.5)

Every sentence and table of this subsection begins with, or carries in its caption, the Part V label: "development; outcome foreseeable from stored aggregates and an unreviewed calculation (disclosed)".

**Table S11.5a.** Part V verdicts, $k = 2$, $w_0 = 0.20$, truth $G^{\mathrm{top}}$ (and the instance-only truth as a secondary row).

| Truth | Certified pair-draws (pairs) | Not certified | Excluded | Certified, wrong | $e_c$ | $e_n$ | $e_n - e_c$ [95%] | V1 | V2: cells over budget / cells (share) | V2 | V3 | COCO K2: $\Delta_{\mathrm{cov}}$ (5th pct.) |
|---|---|---|---|---|---|---|---|---|---|---|---|---|
| $G^{\mathrm{top}}$ | {{A_CERT_V_RESULT.json::primary_truth_G_top.V1_V3.n_cert}} ({{….n_pairs_cert}}) | {{….n_other}} | {{….n_excluded}} | {{….n_cert_direction_fails}} | {{….e_c}} | {{….e_n}} | {{….e_n_minus_e_c_ci95}} | {{A_CERT_V_RESULT.json::registered.V1}} | {{…primary_truth_G_top.V2.n_over_budget}} / {{….n_cells}} ({{….share}}) | {{…registered.V2}} | {{…registered.V3}} | {{…primary_truth_G_top."COCO K2".delta_cov}} ({{….LB_p5}}): {{…registered."COCO K2"}} |
| Instance classes only (secondary) | {{…secondary_instance_only_truth.V1_V3.n_cert}} | … | … | … | … | … | … | no verdict | {{…secondary_instance_only_truth.V2.n_over_budget}} / … | no verdict | no verdict | no verdict |
| Cross-fitted floor, V-B (secondary; floor by half {{…primary_truth_G_top.cross_fit."V-B".w0_by_half}}) | {{…cross_fit."V-B".n_cert}} | … | … | … | {{….e_c}} | {{….e_n}} | … | {{…cross_fit."V-B".V1}}, no verdict | {{…cross_fit."V-B".V2.n_over_budget}} / {{….n_cells}} | {{…cross_fit."V-B".V2.label}}, no verdict | {{…cross_fit."V-B".V3}}, no verdict | – |
| Cross-fitted floor, V-H (secondary) | as the V-B row with "V-H" | | | | | | | | | | | |

Power (share certified) by $k$ and $w$, both budgets: {{A_CERT_V_RESULT.json::power.by_k.<k>."V-B".<w>}}, {{….power.by_k.<k>."V-H".<w>}}; the null rules at the certified count: {{…primary_truth_G_top.nulls_w0.<rule>.{n, n_direction_fails}}}; M-label power: {{…primary_truth_G_top.M_label."u=0.3 uniform".share_certified}} etc.; reference-named pairs absent from the instance gold: {{…secondary_instance_only_truth.n_ref_named_pairs_not_in_instance_gold}}; the transported margin threshold by half: {{…transported_threshold.by_half[h].{tau_points, n_certified, n_direction_fails}}}.

Sentences. The code writes the registered sentences that apply into `A_CERT_V_RESULT.json::sentences`; the paper prints each of them verbatim [code = reg, VP §V.5, §V.6, §V.4a]:
- if V1 FAIL: "the floor certificate at w0 made more than 5% errors on COCO-5000 against the fuller gold; it is withdrawn at that floor", followed by [own] "({{V1_V3.n_cert_direction_fails}} of {{V1_V3.n_cert}} certified pair-draws wrong, $e_c$ = {{V1_V3.e_c}}; pairs wrong in more than half of their certified draws: {{V1_V3.pairs_failing_in_most_certified_draws}})"
- if V2 FLOOR REFUTED: "on COCO-5000 the floor assumption fails at w0; the probability guarantee is not claimed there, and the error share of V1 is an empirical figure for one model family"
- if COCO K2 is "NOT PASSED": "the certificate does not beat a margin ranking here", followed by [own] "($\Delta_{\mathrm{cov}}$ = {{"COCO K2".delta_cov}}, 5th percentile {{"COCO K2".LB_p5}})"
- always: "from references alone, no precision order and no slope sign can be certified without an assumption on how often present objects are named."

By verdict, where no code string exists:
- **V1 NOT EVALUABLE** (KV-EV) [code, `KV.KV-EV`]: "V1 NOT EVALUABLE at the freeze: Part V reports power only; the certificate was not validated". Paper sentence [own around it]: "On COCO-5000 the registered check could not be evaluated at $w_0 = 0.20$ ({{FREEZE_V.json::v1_declared.n_cert}} certified from {{FREEZE_V.json::v1_declared.n_pairs_cert}} pairs, {{FREEZE_V.json::v1_declared.n_other}} not certified; at least 72 certified pair-draws, 5 pairs and 72 not certified were needed; declared at the freeze); Part V reports power only, and the certificate was not validated."
- **V1 PASS** [own]: "At $w_0 = 0.20$ with two references, {{V1_V3.n_cert_direction_fails}} of {{V1_V3.n_cert}} certified pair-draws on COCO-5000 had the wrong direction under the fuller gold ($e_c$ = {{V1_V3.e_c}}; at most 5% allowed, and no pair wrong in more than half of its certified draws): V1 PASS."
- **V2 FLOOR SUPPORTED** [own]: "In {{V2.n_over_budget}} of {{V2.n_cells}} cells ({{V2.share}}) more unknown pairs were present under the fuller gold than the budget at $w_0$ allows, within the registered $\alpha_S = 0.025$: FLOOR SUPPORTED."
- **V2 FLOOR REFUTED** adds, besides the code sentence [own]: "In {{V2.n_over_budget}} of {{V2.n_cells}} cells ({{V2.share}}) more unknown pairs were present than the budget at $w_0$ allows, above the registered $\alpha_S = 0.025$." And KV2 [code, `KV.KV2`]: the guarantee sentence of Section 3.8 is printed with "the floor assumption failed on COCO-5000 at w0"; if V1 is PASS the certificate is described as "empirically valid on the sets tested".
- **V3 DISCRIMINATING** [own]: "Uncertified pair-draws had the wrong direction more often than certified ones ($e_n$ = {{V1_V3.e_n}} against $e_c$ = {{V1_V3.e_c}}; $e_n - e_c$ {{V1_V3.e_n_minus_e_c_ci95}}): V3 DISCRIMINATING."
- **V3 NOT DISCRIMINATING** [own]: "Uncertified pair-draws were not shown to have the wrong direction more often than certified ones ($e_n - e_c$ {{V1_V3.e_n_minus_e_c_ci95}}): V3 NOT DISCRIMINATING."
- **COCO K2 PASS** [CC, CC-335 Ruling 4 (iii)]: "ranks comparisons better than trivial rules on COCO-5000 (development data, spent)"; full sentence [own]: "Ranked by $w^*$, the certificate covers {{"COCO K2".delta_cov}} more of the pair-draws within 5% risk than the best of the three simple rankings (5th percentile {{"COCO K2".LB_p5}}): COCO K2 PASS; it ranks comparisons better than trivial rules on COCO-5000 (development data, spent)."
- **KV1** [code, `KV.KV1`]: "V1 FAIL: the floor w0 is withdrawn in the paper for every data set; Part P prints w* only". Paper [own around it]: "Because V1 failed, the floor $w_0 = 0.20$ is withdrawn for every data set in this paper: the XM3600-600 verdicts of Section 6.7 are still printed as registered, and Part P prints break-down floors only."
- Cross-fitted floor, CC-352 N9 [reg]: the count of excluded half units includes the half units without a direction; when a cross-fitted V2 row has `n_cells` = 0, it is printed "no finite budget at the cross-fitted floor", not as a measured refutation.

### 3.8 Part P shells (Section 6.8 and S11.6)

Every Part P number carries "POST HOC; truth already scored by the paper"; the methods paragraph carries {{A_CERT_P_RESULT.json::methods_sentence}}.

If `A_CERT_P_RESULT.json::dropped` exists, the paper prints only [code]: "Part P dropped: the matcher-identity gate failed (§P.2)", reworded for the paper [own] as "The re-scoring of the released logs did not reproduce the stored rows of Supplementary S3 to the printed precision, so the certificate was not applied to the published comparisons (post hoc row dropped)." If Part P is not run by its slip date [own, VP §11 l.229]: "The application to published comparisons was not run (post hoc row dropped)."

**Table S11.6a.** P-a, each published comparison at each $k$ (POST HOC; truth already scored by the paper).

| Comparison (method vs baseline) | Image set (images) | $k$ | Share of 20 draws certified, method direction | Share certified, baseline direction | Median $w^*$ | Certified draws agreeing with the CHAIR-gold direction | Transported margin row ($k = 2$; secondary) |
|---|---|---|---|---|---|---|---|
| {{A_CERT_P_RESULT.json::P_a.published[j].comparison}} | {{….image_set}} ({{….n_images}}) | {{….k}} | {{….share_certified_w0}} | {{….share_certified_w0_baseline_direction}} | {{….median_w_star}} | {{….n_certified_equal_to_chair_gold_direction}} | {{….transported_margin_secondary}} |

Per-comparison sentence [code = reg template of VP §P.4 l.181]: print `P_a.published[j].sentence` verbatim. Its forms (from ACVP `p_row`): "with {k} references, the direction of this published comparison is {certified in all {n} reference draws | not certified in any of the {n} reference draws | certified in {c} and not certified in {n−c} of the {n} reference draws} against gold incompleteness at floor w0 = 0.2 on image set {set} ({images} images); its median break-down floor is w* = {w*}", followed, whenever not all draws are certified in the method's direction, by "; this does not say the published result is wrong". Under KV1 the sentence is instead [code]: "with {k} references, the median break-down floor of this published comparison on image set {set} ({images} images) is w* = {w*}".

Aggregate sentence [code, `P_a.aggregate[k].text`, with the CC-352 N10 reading]: the code prints "image sets F-A, F-B and F-C as released"; the paper prints [own, per N10] "mean share of the 20 reference draws certified over the 15 published comparisons: {{P_a.aggregate[k].text → value}} (k = {{k}}, w0 = 0.20, the three released image sets as released, images with instance labels, as in Supplementary S3, {{min}} to {{max}} images per comparison)", and never without $k$, $w_0$ and the image sets (VP §P.4 l.186). (J-25: "E1's rule" names an internal label; the paper text may say "images with instance labels, as in Supplementary S3".)

**Table S11.6b.** Same-image pairs (94; post hoc; truth already scored by the paper; other model families): per pair the median $w^*$ at each $k$ ({{P_a.same_image_pairs.pairs[*].median_w_star_k<k>}}) and the share of draws certified in either direction ({{….share_certified_w0_k<k>}}); V1–V3 and V2 over the 94 pairs at $k = 2$: {{P_a.same_image_pairs.V1_V3.{V1, V3, e_c, e_n, n_cert}}}, {{P_a.same_image_pairs.V2.V2.{label, n_over_budget, n_cells, share}}}. CC-352 N10 [reg]: the column `share_certified_w0_k<k>` counts certificates in either direction and is never printed as "certified" for a published comparison. The V1–V3 and V2 labels of this table are printed with "post hoc; truth already scored by the paper; other model families" and are not verdicts (J-26).

**Table S11.6c.** P-b, the CHAIR gold itself ($k = 5$; secondary; no truth exists): per published comparison {{P_b[j].comparison}}, {{….image_set}} ({{….n_images}}), $I_0$ by cell {{….I0_by_cell}}, $w^*$ with the instance-label cap {{….w_star_cap_I0}} and with the plain cap {{….w_star_cap_min_U_floor_beta}}, cells with the floor refuted at $w_0$ {{….cells_with_floor_refuted_at_w0}}. Sentence [code]: print `P_b[j].sentence` verbatim ("with 5 references and the instance labels, the direction of this published comparison is {certified | not certified} against gold incompleteness at floor w0 = 0.2 on image set {set} ({n} images); its break-down floor is w* = {w*}", with "; floor refuted by the instance labels in cell(s) … at w0" when a cell is refuted, and "; this does not say the published result is wrong" whenever not certified). CC-352 N10 [reg]: `verdict_w0_cap_min_U_floor_beta` is never printed as "certified" for a published comparison; a baseline-direction certificate appears only as the field {{P_b[j].certified_direction}}, never in a sentence.

### 3.9 Ledger rows (Table 1 in Section 1.2; Supplementary Table S4.0)

New Table 1 entries (identifiers A-C1 to A-C7 are placeholders; J-28). All seven go to one new Table 1 row group, "Registered on new labels of previously analysed images (development role; single annotator)", each with its verdict by name (CC-357 E11); nothing is placed before the result exists.

| Id | Prediction (short) | Section | Verdict cell |
|---|---|---|---|
| A-C1 | H1a: completed label-gold slope of the second backbone > 0 | 6.7.2 | {{A_CERT_RESULT.json::registered.H1a}} |
| A-C2 | H1b: first-backbone completed slope inside the Table S7.2 bracket | 6.7.2 | {{…registered.H1b}} |
| A-C3 | H1c: second-backbone completed slope inside the Table S7.2 bracket | 6.7.2 | {{…registered.H1c}} |
| A-C4 | H2a: the reference-only certificate at $w_0$ holds on the completed gold and beats uncertified pairs | 6.7.3 | {{…registered.H2a}} |
| A-C5 | H2b: the budget at $w_0$ covers at least 11 of 12 systems | 6.7.3 | {{…registered.H2b}} |
| A-C6 | H2d: $w^*$ ranks comparisons better than margin and length by AUC ≥ 0.10 | 6.7.4 | {{…registered.H2d}} (label of §2.10) |
| A-C7 | H3: the coverage bound against the completed gold | 6.7.5 | {{…registered.H3}} |

New Table 1 row "Development, no verdict on the paper's claims": V1 {{A_CERT_V_RESULT.json::registered.V1}}, V2 {{…registered.V2}}, V3 {{…registered.V3}}, COCO K2 {{…registered."COCO K2"}} (Section 6.8; label of §2.13). New entry in the row "Post hoc, no verdict": "certificate applied to 15 published comparisons (Section 6.8)". Supplementary Table S4.0 gets the registration times: {{LOG.md::OPS-1111an.utc}} (R11 commit), {{LOG.md::OPS-1111as.utc}} (VP commit), {{LOG.md::OPS-1111at.utc}} (H2D commit and pin), {{LOG.md::OPS-1112h.utc}} (FREEZE pin), {{LOG.md::<FREEZE_V pin>.utc}}, {{LOG.md::<score run>.utc}}, {{LOG.md::<v-score run>.utc}}, {{LOG.md::<p-score run>.utc}}, and the first-label time {{LOG.md::OPS-1111al.utc}}.

### 3.10 Abstract, highlight, research question and contribution shells

Which shell is used depends only on the stored verdicts. The entry gate is met iff KV0 passed, no claimed floor has more than 5% certified errors (V1 is not FAIL and H2a is not FAIL), and H2a PASS or COCO K2 PASS (VP §11 l.224). (Whether H2d PASS also meets the gate is the PI's decision, J-2.)

Research question (both homes) [own]: "**RQ4 (certification; registered on new labels of previously analysed XM3600-600 captions, development role).** Can the direction of a comparison between two systems be fixed from an incomplete gold, and under what assumption on its missing part? (Sections 3.8 and 6.7–6.8)"

Home M, gate met through H2a PASS [CC-335 Ruling 4 (ii) + own]:
- Abstract [own]: "We propose a certificate that states whether the direction of a comparison is fixed by an incomplete gold, and the weakest naming floor under which it is. On a human completion of the XM3600-600 object gold (single annotator), the reference-only certificate was validated at the registered floor ({{H2a.n_cert}} certified pairs; H2a PASS)."
- Contribution 6 [own]: "A certificate for the direction of a comparison under an incomplete gold, with a break-down floor per comparison, validated on a human-completed gold (single annotator, {{H2a.n_cert}} certified pairs; registered on new labels of previously analysed captions), checked on COCO-5000 against a fuller gold (development) and applied to 15 published comparisons (post hoc) (Sections 3.8, 6.7, 6.8)."

Home M, gate met through COCO K2 PASS [CC-335 Ruling 4 (iii) + own]:
- Abstract [own]: "… The break-down floor ranks comparisons better than trivial rules on COCO-5000 (development data, spent; COCO K2 PASS), and the registered test on the human-completed XM3600-600 gold gave H2a {{registered.H2a}}."
- Contribution 6 [own]: as above, with "ranks comparisons better than trivial rules on COCO-5000 (development data, spent)" in place of "validated …".

Home M through H2d PASS, only if the PI adds the clause before `score` [CC-335 Ruling 4 (iv)]: "the break-down floor w* ranked the robustness of comparisons better than the observed margin and the length rule on a new benchmark's human-completed gold (single annotator, 30 dependent pairs)", with the H2d label. (CC-335 writes "30 dependent pairs"; the code prints $n_1 + n_0$; the paper uses {{H2d.n1}} + {{H2d.n0}}, J-29.)

Home S, gate not met [CC-335 Ruling 4 (i), generalised from its stated case; own where marked]:
- Abstract [own]: "A human completion of the XM3600-600 object gold (single annotator) measures the label-gold slope that the verified-precision rule only bracketed: {{H1a/H1b/H1c sentence short form}}; it {{respects | violates | does not settle | could not test}} the reference-only coverage bound (H3 {{registered.H3}}). A proposed certificate for the direction of a comparison under incomplete gold was not validated (Supplementary S11)."
- Section 8.1 pointer sentence [CC-335 Ruling 4 (i), with its figures as placeholders]: "We propose a certificate; on a development set with a fuller gold (development; outcome foreseeable from stored aggregates and an unreviewed calculation (disclosed)) {{registered.V1 = "PASS" or "FAIL" → "it made {{V1_V3.n_cert_direction_fails}} certified errors in {{V1_V3.n_cert}} certified pair-draws at w0 = 0.20"}}{{registered.V1 = "FAIL" → ", so the floor w0 is withdrawn"}}{{registered.V1 = "NOT EVALUABLE" → "the registered check could not be evaluated at w0 = 0.20 and only power is reported"}}{{registered.V2 = "FLOOR REFUTED" → ", although its floor assumption failed in {{V2.share}} of cells"}}; {{registered."COCO K2" = "NOT PASSED" → "it did not rank comparisons better than a margin rule; "}}it was not validated." (CC-357 J-30: each clause follows the stored verdict string; under KV-EV the V2 and COCO K2 values are "not computed (KV-EV)" and their clauses are omitted.)
- Contribution [own]: "A human completion of the XM3600-600 object gold (single annotator; new labels on previously analysed captions, registered before anyone but the annotator opened a label value) that measures the label-gold slope bracketed in Section 6.2 (H1) and tests the coverage bound of Section 5.4 (H3)."

Highlight (≤ 85 characters) [own], one of:
- Home M: "A per-comparison certificate tells when an incomplete gold fixes a comparison" (77)
- Home S: "Human labels complete the XM3600 object gold and measure the label-gold slope" (77)

---

## 4. Limitations and disclosure paragraphs (paper text)

Home: Section 9.1, as new paragraphs after "Construct validity: reference-only bound." (whose first sentence changes as E7 of §1.3), in both homes; the Part V and Part P paragraphs also open S11.5 and S11.6. Section 9.2 gets the last paragraph.

**Construct and internal validity: the human-completed gold.** The completion of the XM3600-600 object gold was labelled by one annotator, who is an author and knows the study; every result that uses it carries the words "single annotator" until a second annotator's answers on 150 of the images have been compared under the registered kappa rule (Section 6.7.1). The annotator could not tell which system or reference named a class; he saw every answer he gave while labelling, and an author can still know how answers enter the statistics. The single annotator is an author. After the main analysis registration was committed and before he gave any answer in the main labelling task, he was told that an internal forecast of the method's success was low and that a rehearsed assessment of the method depended on the checks against his labels; he was not told which answers would favour which outcome, and the labelling page showed no caption, no system name and no mark of target or control questions. One registered test (H2d) was added after the first of these messages and before any main label existed. The registered instruments for a general lean are the 443 control questions with Open Images answers, the 150 repeats and the second annotator; none of them gates a verdict.
<!-- src: PLAN §3 l.28-29, §4 l.37-38, §7 l.56; R11 Disclosures l.39 ("He saw every value while labelling. He could not see which caption set or reference named a pair."); CC-343 Ruling 5 l.242-253 (the disclosure sentence, verbatim, "for Paper A's limitations, in the section that reports the human-completed gold", and the H2d addition "If the paper describes H2d, it adds: ..." verbatim), l.256-263 (why no rule changes; the instruments). Writer note: the CC-343 sentence appears twice in effect (its last clause repeats the page facts of the sentence before it); the verbatim sentence is kept whole, and the writer's own page sentence before it may be cut (J-38). -->

**Construct validity: what the labels are.** The labels are class-level answers for (image, class) pairs, not judgements of a caption's wording: the matcher's lexical ambiguity remains (the A answer measures part of it), and the labels are not a complete inventory of the image. An Open Images label is never overridden, so where the annotator and Open Images would disagree the Open Images label stands, and the controls measure the disagreement. Whether depictions count as present in the Open Images image-level labels is not verified.
<!-- src: PLAN §5 l.41, l.49; §4 l.35; §7 l.56. -->

**Internal validity: data the paper had already analysed.** The 600 images and the twelve caption sets were analysed in this paper before the labels were collected; the registered look at these images is spent and they are used in a development role (Section 6.2). Only the labels are new, and every label-based result is "new labels on previously analysed captions". The analysis was registered and committed, and its label-free part computed and fixed by hash, before anyone but the annotator opened a label value; the scoring ran once. Before the labels existed, the analysts had computed figures from the stored Open Images statuses that bear on some outcomes, and kept them with the registration; the human answers were unseen by the analysts until the scoring run. For H2d this is stated in its label. These figures, and the expectations stated with the registration, are printed in Supplementary S11.4 {{J-19: R11 §9 bullets, verbatim, inserted only in Phase B}}.
<!-- src: R11 Disclosures l.42-43 (CC-333 N9), §8 l.224-228, §12 l.261-268; R11 §7 l.220 ("the disclosed §9 rehearsal on stored Open Images statuses"); H2D Disclosures l.24 ("The Open Images statuses are partly seen ... The human answers are unseen by the analysts"); CC-333 Ruling 4 l.136-138. Writer note: the figures of R11 §9 and H2D l.24 are not printed here (J-19). -->

**Construct validity: the assumptions of the reference-only certificate.** From references alone no precision order and no slope sign can be certified without an assumption on how often present objects are named (Section 3.8), so every reference-only verdict is conditional on the floor (F$_w$) and on (A0), (A1) and (A1+). The floor cannot be checked from the references: the present objects that writers rarely name are exactly the part the references leave unknown, and the primary floor $w_0 = 0.20$ was fixed from an earlier calculation, not derived. (A1) is a modelling assumption on XM3600-600, on COCO-5000 and on the released image sets of Part P and is not checked (the diagnostic of Section 5 checks reference order only). (A0) fails wherever a reference names a class that is not in the image (Section 4.2); the instance-only rows of Part V and the count printed beside H3 show how often this happens on the sets where it can be counted. (A1+) is dropped by the secondary Hoeffding budget. The derivation of the budget (Supplementary S11.2) has had no external proof review.
<!-- src: VP §V.4a l.79; R11 §4.2 l.124, l.126; CC-333 l.70-72 (origin of w0); FIXA2 §1.2, §2.3 and S1.M.6 (no independence claim; (A1) "a modelling assumption ... not checked"); VP §V.3 l.67 ("Secondary truth (no verdict): instance classes alone; it is the only one under which (A0) can fail"); R11 §6 H3 l.208; CC-333 Q2 l.116-117 ("This is not an external proof review"). Writer note: "derivation not reviewed outside the authors' group" is the writer's rendering of CC-333 Q2; authorship of the derivation is J-7. -->

**Statistical conclusion validity: few, dependent comparisons.** Twelve caption sets give 66 pairs, of which the 30 within-family pairs carry H2a and H2d; the second-backbone runs are two prompts at three temperatures, so about 9 of its 15 pairs are short-against-detailed and 6 are near-copies, and the effective number of independent comparisons is far below 30. Pairs share images and systems, so the exact lower limit printed with H2a is descriptive, and H2d has low power. A certificate holds for the fixed captions on these images; it says nothing about a re-run of a system or another image set.
<!-- src: R11 §7 l.214; §6 H2a l.186 ("pairs share images and systems, so it is descriptive"); H2D §3 l.48 ("With n1 + n0 dependent pairs the test has low power"); R11 §4.2 l.124, l.126. -->

**Development and post hoc rows.** The check on COCO-5000 (Section 6.8, Supplementary S11.5) uses spent development data of this paper and one model family, and every one of its numbers carries the label "development; outcome foreseeable from stored aggregates and an unreviewed calculation (disclosed)": before its registration was written, the precision order of all 36 system pairs under the fuller gold and their two-reference margins had been computed from committed aggregates, and an earlier unreviewed calculation had reported figures for the error share and the cells over budget at $w = 0.20$; the evaluability thresholds of its check were set after that calculation was known. These figures, and the outcomes the registration stated in advance, are printed in Supplementary S11.5 {{J-19: VP §V.1 bullets and the first paragraph of VP §V.5, verbatim, inserted only in Phase B}}. None of its results is a prediction, a validation or a confirmation. The application to 15 published comparisons (Section 6.8, Supplementary S11.6) is post hoc: the paper had already scored these released outputs under the full gold, and every one of its numbers carries "POST HOC; truth already scored by the paper". Neither part changes a registered result of this paper, and neither is evidence for the registered test H2a. "Not certified" for a published comparison does not say the published result is wrong.
<!-- src: VP Disclosures l.33-34; §V.5 "Status" l.83 (CC-335 B2); §V.2 l.63 (one model family); §P.4 l.181-187; CC-335 Ruling 3 l.106-115; R11 §8 l.226 ("never changes a registered label of Paper A"). Writer note: the calculation's figures are not printed (J-19). -->

**Prior work.** The bound over every completion of the missing labels and the use of a shared completion for the two systems compared are taken from Fernández-Barrios et al. (2026) and specialised to precision; they are not claimed as ours. What this paper adds is the setting of multi-reference caption golds, where those bounds are empty from references alone, a probabilistic cap from once-named counts under a naming floor, the break-down floor per comparison, the slope corners, and the tests of the cap against a fuller gold and a human-completed gold.
<!-- src: VP §9 table l.199-207; CC-333 Ruling 2 (i) l.100-103 ("What is ours is the floor budget (the upper twin of Chao), the multi-reference caption setting, w*, the slope corners and the test against human completion"); CC-333 N8 l.228-229. -->

**Other-family arm (printed only if its rows are printed; see J-27).** {{NO KEY YET: number of models in passed_7a.txt}} further models were decoded on the same 600 images in a development arm, and the pairs that only they name were labelled in a separate session with the same page, wording and rules. The annotator knew that this session asked about pairs named by new models, so that group was not blind, although which new model named a pair stayed hidden; 50 earlier questions asked again and the controls were mixed in, and give a cross-session agreement figure. The annotator had already seen these images in the main session.{{E3 §8, CC-355 W3: if the part-1 result was shown to the PI before the top-up session-end LOG line → " He had also seen the result of the main analysis before the top-up session ended."}} Every row of the arm carries the label "development; new decodes on previously analysed images; new labels; single annotator until the second annotator's top-up overlap is labelled" and no verdict.
<!-- src: E3RD §9.2 l.281-284 ("Disclosed leak: ... The PI has already seen these images in part 1. Disclose this beside the top-up results."); PLAN §6 l.52. Writer note: the model count comes from the arm's pass list, a pulled output the writer did not open. -->

Model-naming sentence for that arm, chosen by the number of models that pass (E3RD §2.3 l.106-110, verbatim; CC-184 F3 and CC-349 Q14: no sentence about language-model lineage relative to the paper's own systems):
- Four pass: "Four further models, Aya-Vision-8B, Gemma-3-4B-it, Idefics3-8B and LLaVA-1.5-7B, span three language-model families (Command R7B; Gemma 3; Llama, in Llama 3.1 and Llama 2 form) and three vision-encoder lines (SigLIP2, SigLIP, CLIP). Idefics3-8B and LLaVA-1.5-7B also appear in the eight-LVLM ladder (A-N2 registry), and Aya-Vision-8B and Idefics3-8B in the COCO arm (A-T3)." (J-27: "A-N2 registry" and "A-T3" are internal names; the paper names the sections.)
- Three pass: name the three and count again; if Gemma and Aya are two of them, say "two language-model families besides Llama".
- Two pass (Aya, Gemma): "Two further models, Aya-Vision-8B and Gemma-3-4B-it (language models Command R7B and Gemma 3) …", and say that the other candidates did not write Vietnamese often enough to be scored ({{NO KEY YET: G4 counts}}).

**Wording duties carried from the code reads (CC-352 N1, N4, N9, N10; CC-343 N9).** These bind the paper text wherever the rows are printed; §2.13, §2.14, §3.3, §3.7 and §3.8 already apply them.
- N1 (CC-347 N1, carried by CC-352): S11.8 states that the addendum names the Part V script `a_cert_v.py` and that it is implemented as `scripts/a_cert/a_cert_vp.py`, modes `v-freeze` and `v-score`.
- N4: the Part P text states that $G^{\mathrm{top}}$ is the first five references of an image together with its instance classes, and that the matcher check uses every reference, as the paper's earlier scoring did (§2.14).
- N9: in the Part V cross-fitted rows, the count of excluded half units includes the half units without a direction, and a row with no cells is printed "no finite budget at the cross-fitted floor", not as a measured refutation (§3.7).
- N10: the plain-cap verdict of P-b and the either-direction share of the 94 same-image pairs are never printed as "certified" for a published comparison; the aggregate's "as released" is printed as "as released, images with instance labels" (§3.8).
- CC-343 N9: an H2a secondary row printed "VALID AT $w$" with no certified pair is printed "vacuous (no pair certified)" (§3.3).
<!-- src: CC-352 l.204, l.208-209, l.214-217; CC-347 N1 l.264, N4 l.271; CC-343 N9 l.331-332. -->

**Section 9.2, new paragraph (data and licences).** The released per-image CHAIR evaluation logs of OPERA (`shikiw/OPERA`, commit `e1bb7632508bdfaa5cdaf5b69b64419688107da8`, MIT licence) and of "Less is More" (`yuezih/less-is-more`, commit `f26e187aadacc49a7cfc30443f0e9bae865b8e2e`, Apache-2.0) were used for evaluation only and are not redistributed; their SHA-256 values are recorded. The new human labels for XM3600-600 are {{J-31: release decision}}.
<!-- src: VP §P.1 l.123, l.160 (N3: "The fetched files are never committed; their sha256 values are pinned in the fetch LOG line; each repository is cited with its commit and licence"); CC-352 Ruling 5 step 8 l.163-164. -->

---

## 5. Claim → evidence table

Status column: METHOD (definition or derivation, no data), REGISTERED (verdict on the labels), DEVELOPMENT, POST HOC, DESCRIPTIVE, DISCLOSURE. "Label" is the exact label the registrations require beside the number.

| # | Claim (as the paper may state it) | Registered source | Output key that carries it | Status | Label printed |
|---|---|---|---|---|---|
| 1 | CERTIFIED iff $\Delta_{\min} > 0$ over the capped completions; ABSTAIN and NOT DEFINED excluded | R11 §4.1 l.104-109 | AC `certify`, `delta_min` | METHOD | – |
| 2 | From references alone, no precision order and no slope sign can be certified without a naming assumption | VP §V.4a l.79; CC-335 Ruling 2 | FREEZE.json::pairs[*].cref."0.0".verdict and ::slopes.<fam>.cref_P."0.0".certified_sign (a certificate there is a code fault) | METHOD (proved; checked by a judge by hand) | – |
| 3 | Under (A0), (A1), (A1+), (F$_w$) a CERTIFIED verdict is wrong with probability ≤ α for fixed outputs on these images | R11 §4.2 l.124; CC-333 Math (2)-(4) | – | METHOD (derivation; J-7) | – |
| 4 | Proposition 2 cannot certify; it keeps the intervals and H3 | R11 §4.2 l.126; CC-333 Q1 | – | METHOD | – |
| 5 | The all-completion bound and the shared completion are prior work | CC-333 Ruling 2 (i); VP §9 | citation arXiv 2611.01712 | – | – |
| 6 | Label-side certificates fixed by the Open Images labels alone: k of 30 comparisons; slope signs | R11 §4.3 | FREEZE.json::pairs[*].clabel.verdict (DERIVED count); ::slopes.<fam>.clabel.{F,P}.certified_sign | DEVELOPMENT (no labels) | "development (no labels)" |
| 7 | Range of the label-gold slope over all completions | R11 §5 | FREEZE.json::slopes.<fam>.clabel.{F,P}.range | POST HOC | "post hoc (stored outputs, no labels)" (J-15) |
| 8 | Per-system precision intervals | R11 §4.4 | FREEZE.json::intervals_44.<s>.{low, high.<w>} | DEVELOPMENT (no labels) | "development (no labels)" |
| 9 | H2a evaluability, H2b and H3 declarations made before unsealing | R11 l.182, l.189, §8 l.226 | FREEZE.json::{h2a_declared, h2a_evaluable_w0, h2b_declared, h3.evaluable} | DEVELOPMENT (no labels), declared before unsealing | "development (no labels)" |
| 10 | H1a verdict on the second-backbone completed slope | R11 §6 l.162 | A_CERT_RESULT.json::registered.H1a; ::H1.Q3.{b_F, b_F_ci95, b_F_bonf} | REGISTERED | "single annotator; new labels on previously analysed captions" |
| 11 | H1b verdict | R11 §6 l.163 | ::registered.H1b; ::H1.Q25.{b_F, direction, b_F_minus_S72_*_ci95} | REGISTERED | as 10 |
| 12 | H1c verdict | R11 §6 l.164 | ::registered.H1c; ::H1.Q3.{b_F, direction, b_F_minus_S72_*_ci95} | REGISTERED | as 10 |
| 13 | $b_P$ beside $b_F$ | R11 §6 l.158 | ::H1.<fam>.{b_P, b_P_ci95} | DESCRIPTIVE (no verdict) | as 10 |
| 14 | H2a verdict, $V_c$, $V_n$, nulls | R11 §6 l.181-186 | ::registered.H2a; ::H2a.* | REGISTERED | as 10 |
| 15 | "The certificate beats a margin threshold" may be said only if the margin rule does not make fewer errors | R11 l.186 | ::H2a.margin_beats_certificate | REGISTERED (wording rule) | as 10 |
| 16 | H2a secondary rows by floor, cross-family, remainder, adversarial | R11 l.193, §10 (N6) | ::H2a.{secondary_by_w, cross_family_secondary, n_cert_unconfirmed_only_through_remainder, n_cert_confirmed_adversarial} | DESCRIPTIVE (no verdict) | as 10; "vacuous (no pair certified)" where n_cert = 0 |
| 17 | H2b verdict and per-system coverage | R11 §6 l.188-191 | ::registered.H2b; ::H2b.* | REGISTERED | as 10 |
| 18 | H2d verdict and reading | H2D §3 | ::registered.H2d; ::H2d.{reading, fail_adds, D, D_ci95, AUC_w_star_margin_length, ...} | REGISTERED | H2d label (§2.10) + "single annotator" |
| 19 | H3 verdict | R11 §6 l.195-208 | ::registered.H3; ::H3.* | REGISTERED | as 10 |
| 20 | H3 and $D_L$ secondary rows | R11 l.210; CC-343 S3 | ::secondary.{H3_all_system_named, D_L} | DESCRIPTIVE (no verdict) | as 10 |
| 21 | Control, repeat and synonym agreement | PLAN §4; CC-343 S1 | ::quality.* | DESCRIPTIVE (gates nothing) | as 10; "partial (k of 150 …)" where it applies |
| 22 | Recall, F1, hallucination under gold (i) and gold (ii) | PLAN §5; CC-343 S2 | ::secondary.golds_I600.{gold_i, gold_ii} | DESCRIPTIVE (no verdict) | "pooled gold; favours systems that name more" on gold (ii) |
| 23 | Kappa and the verdict wording it implies | PLAN §4 l.38 | {{NO KEY YET}} | DESCRIPTIVE (decides wording) | – |
| 24 | Seven predictions registered; counts by outcome | R11 §7; H2D §5 | ::registered (DERIVED counts) | REGISTERED (summary) | – |
| 25 | V1, V2, V3 verdicts on COCO-5000 | VP §V.5 | A_CERT_V_RESULT.json::registered.{V1,V2,V3}; ::primary_truth_G_top.{V1_V3, V2} | DEVELOPMENT | Part V label |
| 26 | COCO K2; "the certificate does not beat a margin ranking here" unless it passes | VP §V.6 | ::registered."COCO K2"; ::sentences | DEVELOPMENT | Part V label |
| 27 | Kill-gate consequences (not validated; floor withdrawn; guarantee qualified) | VP §V.8 | ::KV.*; FREEZE_V.json::KV-EV | DEVELOPMENT | Part V label |
| 28 | Power by $k$ and $w$; M-label power; cross-fitted floor; transported threshold; instance-only truth | VP §V.5 l.93, §V.6 | ::power; ::primary_truth_G_top.{M_label, cross_fit}; ::transported_threshold; ::secondary_instance_only_truth | DEVELOPMENT (secondary) | Part V label |
| 29 | Per published comparison: certified / not certified at $w_0$ with $k$ references, median $w^*$ | VP §P.3-§P.4 | A_CERT_P_RESULT.json::P_a.published[*].{sentence, share_certified_w0, median_w_star} | POST HOC | "POST HOC; truth already scored by the paper" |
| 30 | Mean share certified over the 15 comparisons, per $k$ | VP §P.4 l.186 | ::P_a.aggregate[*].text | POST HOC | as 29, with $k$, $w_0$, image sets (N10 reading) |
| 31 | V1–V3, V2 over the 94 same-image pairs | VP §P.3 | ::P_a.same_image_pairs.{V1_V3, V2} | POST HOC | "post hoc; truth already scored by the paper; other model families" |
| 32 | P-b per comparison | VP §P.3 | ::P_b[*].{sentence, w_star_cap_I0, cells_with_floor_refuted_at_w0} | POST HOC (secondary; no truth) | as 29 |
| 33 | Matcher-identity gate | VP §P.2 | ::matcher_gate.passed; ::dropped | POST HOC | as 29 |
| 34 | Entry-gate statement: "validated" / "ranks better than trivial rules" / "was not validated" | VP §11; CC-335 Ruling 4 | DERIVED from A_CERT_RESULT.json::registered.H2a, A_CERT_V_RESULT.json::registered.{V1, "COCO K2"}, ::KV.KV0 | per outcome | per outcome |
| 35 | Disclosure on the annotator (CC-343 sentence) | CC-343 Ruling 5 | – | DISCLOSURE | – |
| 36 | Top-up leak and prior viewing of images (other-family arm) | E3RD §9.2 | E3 addendum §2 (committed `2a39f87`, sha256 `64fad518`); top-up result keys not yet written | DISCLOSURE | "development; new decodes on previously analysed images; new labels; single annotator until the second annotator's top-up overlap is labelled" (E3 §0, verbatim) |

---

## 6. Open for the judge

Every place where the registered texts do not fix the paper wording, or where this file had to choose.

1. **J-1 Notation.** §0.1 renames registered symbols to fit the paper (cells $\mathcal C_{\cdot}$, $u(\cdot)$ for `U`, $\varphi_1$ for `f1`, (F$_w$) as $w_{ic} \ge w$). "Exactly as registered" and "in the paper's notation" conflict here; rule on the mapping.
2. **J-2 Entry gate.** No LOG line read by the writer answers CC-335 P-2 (H2d as a gate clause). The writer reads "no claimed floor has more than 5% certified errors" as "V1 not FAIL and H2a not FAIL"; the gate text does not define "claimed floor". Rule on both before the result read.
3. **J-3 Sentences made untrue.** E1 (Section 3.6 rule (iii)), E2 and E3 (Table 2.1 "This paper" row): replacement texts are the writer's.
4. **J-4 (A1) sentence in Section 9.1 (E7).** FIXA2 §2.3 lists sec11:15 as "careful wording already in place"; the transfer rewrites its first sentence because it says "independent writers". Accept, or keep the sentence and add a new one.
5. **J-5 Conclusion counts.** Section 8.5 counts registered FAILs; the recount after the results is not written now.
6. **J-6 FIXA2.** Its Q1–Q11 have no ruling in the LOG lines read; W-01 to W-08 ride along with their NEEDS-JUDGE statuses.
7. **J-7 Authorship of the budget derivation.** R11 l.124 says the paper labels V-B "derived by the authors" and, in the same line, "This derivation is an AI derivation", checked by hand by one judge (CC-333 Q2). The venue card (SPIC, AI policy check of 2026-11-10) says AI used in the research process is described in Methods; the project rule leaves the final sentence to the PI and bars a false "no AI". This file writes neither label; the PI decides.
8. **J-8 Origin of $w_0$.** §2.3 and §4 disclose that $w_0 = 0.20$ came from an earlier unreviewed calculation on COCO-5000 (CC-333 l.70-72). The registrations do not require this sentence; it bears on Part V, which uses the same floor on the same data.
9. **J-9 "Not certified" tail beyond Part P.** VP §P.4 fixes the tail for published comparisons; §2.4 generalises it to every comparison.
10. **J-10 Table 2.1 row** for arXiv 2611.01712, cells from that paper's own text.
11. **J-11 Design counts** (4,910; 1,790; 443; 2,233; 2,100; 150; 4,483; 1,288; 15 practice images) need manifest rows keyed to `BUILD.json`; the writer did not open `BUILD.json` for its key names.
12. **J-12 Naming the labelling tool and files** in S11.7 (repository paths) or not.
13. **J-13 Tense** of the second-annotator sentences at transfer time.
14. **J-14 Kappa** has no output key: the second-annotator analysis is a later, separate unsealing (R11 §12 step 7) with no code read yet.
15. **J-15 Label of the FREEZE-recomputed slope ranges**: R11 §5 says "post hoc (stored outputs, no labels)", R11 §8 says every FREEZE number is "development (no labels)". This file prints the first for the ranges and the second for everything else in FREEZE.
16. **J-16 H2d SESOI rationale** (H2D §4): in S11.4 in full, or one clause in Section 6.7.4.
17. **J-17 R11 l.210 clause** on the all-system-named H3 row: R11 l.210 adds a clause about that row's outcome that this file does not reproduce, because it reads as a forecast. Rule whether the paper prints it beside the row.
18. **J-18 Missing LOG lines**: the score run, the FREEZE_V pin, the fetch line with 25 sha256 values, the v-score and p-score runs. Placeholders `{{LOG.md::<…>}}` stand for them.
19. **J-19 Printing the earlier figures.** The Part V label ends "(disclosed)", VP §V.7 says "The paper prints all three with the §V.1 disclosures", and R11 §7 calls the §9 rehearsal "disclosed". The figures themselves (the 36-pair flip count and margins, the unreviewed calculation's error and over-budget counts, R11 §9's counts, H2D l.24's sign-agreement count) are forecasts in effect and have no manifest keys. This file states that they exist and when they were known, without the figures. Rule whether the paper prints the figures, where (S11.5 only?), and with which source keys.
20. **J-20 Reserved gold sentence.** VP §P.2 requires "the paper states that the OC1 image set was analysed here with other systems". §2.14 words it without the internal name; rule on the wording.
21. **J-21 ABSTAIN label.** The code prints "NOT CERTIFIED (ABSTAIN; §4.1, excluded from V_c, V_n and counts by B2)"; the paper needs a reader-facing form.
22. **J-22 H2a VALID, NOT DISCRIMINATING sentence** (R11 l.184) says "made no error", but the rule allows up to ⌊0.05 n_cert⌋ unconfirmed certified pairs. Keep verbatim, or print "made {{H2a.n_cert_unconfirmed}} errors" when the count is positive.
23. **J-23 H2a FAIL sentence** (R11 l.185) ends "only the no-assumption certificate may be used there"; after VP §V.4a the no-assumption certificate certifies nothing from references, so the sentence may need "(the label-side certificate)".
24. **J-24 Count line.** How "VALID, NOT DISCRIMINATING", "PASS (vacuous)", "RESPECTED", "VIOLATED" and "INCONCLUSIVE (remainder)" are counted in "passed / failed / otherwise / not evaluable".
25. **J-25 "E1's rule"** in the CC-352 N10 reading is an internal name; the paper may say "images with instance labels, as in Supplementary S3".
26. **J-26 Same-image V1–V3 labels** under Part P: the code prints the verdict words (PASS, DISCRIMINATING …) for post hoc rows; the paper should print them as descriptions, not verdicts.
27. **J-27 Other-family arm.** The E3 addendum is an untracked draft (not judge-read, not committed); its rows have no output keys, and the arm's pass list is a pulled output the writer did not open. The §2.3 sentences of E3RD name internal registries ("A-N2 registry", "A-T3"). Rule on whether the top-up rows enter Paper A at all and how the arm is referred to.
28. **J-28 Ledger identifiers** A-C1 to A-C7 are placeholders; Table S4.0 numbering is the paper's.
29. **J-29 "30 dependent pairs"** in CC-335 Ruling 4 (iv) against the code's $n_1 + n_0$ (after exclusions).
30. **J-30 CC-335 Ruling 4 (i).** §3.10 makes each clause of the ruling's sentence conditional on the stored verdicts and replaces its figures by placeholders; confirm this reading.
31. **J-31 Release of the new labels**: no registered text decides whether the XM3600-600 labels are released, under which licence, or as aggregates only.
32. **J-32 Writer's own sentences.** Every sentence marked [own] in §3: H1a PASS and both INCONCLUSIVE forms; H1b/H1c PASS, FAIL above (adapted), INCONCLUSIVE (remainder); the Section 6.2, 6.3 and 9.1 insertions; H2a NOT EVALUABLE, PASS frame, exact-limit, margin and remainder sentences; H2b PASS, FAIL, freeze-FAIL; H3 RESPECTED, INCONCLUSIVE, NOT EVALUABLE and the Section 5.4 and S1.M.6 sentences; the freeze sentences; the kappa sentences; the count line; V1 PASS and NOT EVALUABLE frames, V2 SUPPORTED and REFUTED counts, V3 both ways, COCO K2 PASS frame, KV1 frame; the Part P drop and slip sentences; the RQ, abstract, contribution and highlight shells; and the limitation paragraphs of §4 except the CC-343 sentences.
33. **J-33 Homes and numbering.** New Sections 3.8, 6.7 (with 6.7.1–6.7.5) and 6.8 and Supplementary S11; whether Section 6.8 (Part V and Part P) is in the main text in Home M.
34. **J-34 Abstract length.** The SPIC abstract is at about 250 words; the shells of §3.10 need cuts elsewhere, which this file does not choose.
35. **J-35 The H2a PASS claim word "validated".** CC-335 Ruling 4 (ii) uses it; VP §V.5 bars "validation" for Part V only. Confirm that "validated on a human-completed gold" may be printed for H2a PASS.
36. **J-36 The "eight public LVLMs" phrase** of VP §P.4 l.183: the two releases cover InstructBLIP, LLaVA-1.5, MiniGPT-4, Shikra, LLaVA-1.5-13B, LLaVA-7B and MiniGPT-v2 (seven distinct names if OPERA's LLaVA-1.5 is the 7B model; not checked); §2.14 avoids the count.
37. **J-37 H1a FAIL text.** R11 l.169 includes "This contradicts Section 6.3's support for a positive label-gold slope on a second backbone"; rule whether that registered description is printed as a paper sentence (this file prints it).
38. **J-38 Repetition in the annotator paragraph.** The CC-343 sentence restates the page facts; the writer's own preceding sentence may be cut to avoid saying it twice.
39. **J-39 Gate-not-met home of H2a, H2b and H2d.** CC-335 Ruling 4 (i) says the method "sits in Discussion or the Supplement"; this file moves the three verdicts to S11.4 and keeps them in Table 1. Confirm that this is not "hiding" a registered verdict.
40. **J-40 Analysis stopped by a second fault.** No registered sentence exists for the case in which a second fault stops the label analysis or Part V and the case goes to the PI (R11 §12 step 5; VP §V.8 KV3). The paper would then report that the registered analysis was not completed; the wording is open.
41. **J-41 KV-EV against H2a PASS.** If V1 is NOT EVALUABLE on COCO-5000 (KV-EV: the paper says the certificate "was not validated") while H2a passes on XM3600-600 ("validated on a human-completed gold"), the two registered phrases collide. Rule which sentence the paper prints, or how both are scoped (by data set).
42. **J-42 The $w = 0$ columns.** Section 3.8 states that the reference-only rows at $w = 0$ certify nothing and that the interval high end there is 1; whether the tables print those columns (registered: "computed and printed as registered", VP §V.4a) or a note only.



