# A-CERT addendum E3 v1: the top-up labels of the other-family arm (Paper A, XM3600-600)

Written 2026-11-12T04:13Z (`date -u`). vsps HEAD `26574ef`, branch `paper-v10`. Writer agent. Written as a draft for a one-judge read; the text fixes W1-W5 of CC-355 were applied in place before the commit. Nothing was run on labels and no LOG line was written. No label file, `key.json`, `assignment.json`, caption file or A-E3 output was opened. `~/vsps_labels/` and the A-E3 pull dir were not opened, listed or stat-ed. Read: the run document, CC-327/349/351, A-CERT v1.1, plan v1.1, the base `BUILD.json` (counts and sha256), and code. AI opinion throughout. "chưa kiểm" = not checked.

**Source of every rule below.** Run document v1.1 Annex A (the draft of this addendum) and §9.2, §9.4; A-CERT v1.1 §10 (other-family row) and §12 step 7; CC-349 rulings 5, Q6, Q7, N9; CC-351 "LATER, WITH THEIR OWN READS". Where these leave a choice open, the choice is listed in §9; CC-355 adopted every recommended value there (W4).

**What binds this file (sha256).**
- A-CERT analysis registration v1.1, `manuscript/prereg/2026-11-11_a_cert/A_CERT_ANALYSIS_REG_v1_1.md`, `e564b7b1…`. This file adds rows to its §10 other-family row. It changes no line of v1.1.
- Labelling plan v1.1, `manuscript/prereg/2026-11-11_xm600_gold_completion/XM600_GOLD_COMPLETION_PLAN_v1_1.md`, `8ad28f67…`, §3–§6. This file may not change them (CC-327 L6).
- A-E3 run document v1.1, `manuscript/prereg/2026-11-12_a_e3_arm/A_E3_ARM_RUN_DOC_v1_1.md`, `1df371cc…`, §9 and Annex A.
- Rulings CC-327 (`0f8e8b84…`) L2; CC-349 (`bb7b93da…`); CC-351 (`149a8708…`).
- The 12-system FREEZE, `data/results/a_cert/freeze/FREEZE.json`, `c51ea7dc…` (OPS-1112h). Unchanged by this file.

**Gate.** This file is judge-read and committed **before any top-up label value is opened** by anyone other than the annotator (CC-349 ruling 5; CC-351). Until then, top-up labels enter no analysis (run document §9.4).

---

## 0. Scope, label and status

- **Systems S_E.** The 600-image Vietnamese caption sets of the A-E3 models that passed G4 and G5 (two per model: `ae3_<key>_xm600-short`, `ae3_<key>_xm600-detailed`), on I600. Only models listed in the pulled `passed_7a.txt` (pull copy `.session_backup/machines/ATTR_H1/root/a_e3/out/`) or in the pulled `passed_7c.txt` (pull copy `.session_backup/machines/ATTR_H1_7c/root/a_e3/out/`; A-E3 addendum v1 `A_E3_ADDENDUM_MODELS_v1.md`, CC-359); a `passed_7c.txt` model's rows carry the addendum's disclosure. HELD outputs (G5 failure) and models that failed G4 are not in S_E.
- **Home.** A-CERT v1.1 §10, row "Other-family arm (PI-1105k, PI-1107c): a third family on I600 — development; C-ref and C-label at once; completed-gold rows only after a top-up labelling session and a separate unsealing; CC-327 L2 applies", and §12 step 7.
- **Label of every row:** "development; new decodes on previously analysed images; new labels; single annotator until the second annotator's top-up overlap is labelled".
- **No verdict** attaches to any row of this file. No row is a hypothesis.
- **Why the top-up labels need this file.** By construction, no top-up target pair is named by any of the twelve stored caption sets or by a reference. They therefore lie outside every registered H1–H3 universe of A-CERT v1.1 (run document §9.4).

## 1. Items and the deviation from plan §6

- **Deviation (CC-349 N9).** Plan §6 says the top-up items are "built by the same script from the new caption files". They are built instead by a **new wrapper**, `tools/obj_rater/build_topup.py`, which imports `tools/obj_rater/build_assignment.py` (497e5747) unchanged. Reason: `build_assignment.py` is pinned in plan §8, `a_cert.py` imports its `load_systems`, and `a_cert gate` reproduces its counts (run document §9.1). The wrapper rebuilds the base and stops unless the four pinned base outputs are reproduced. The wrapper has its own one-judge code read before any build.
- **Items** (run document §9.1 step 4): part 1 = new `unknown` pairs (target), new named `absent` pairs (`ctrl_absent`), `ctrl_present` sampled from new named-present pairs, unnamed-absent foils, and 50 base part-1 targets asked again (`old_repeat`), all mixed within screens; part 2 = new `unmapped` pairs (target); part 3 = repeats of new part-1 targets. Counts are printed by the wrapper before the session (`BUILD_TOPUP1.json`).
- **CC-327 L2 (Q6).** Pairs of `tranh`, `bức tranh` and `mỏm đá` that Open Images marks absent are not asked, and never become controls or foils. Their registered Open Images status stays. The excluded counts are printed in `BUILD_TOPUP1.json`.
- **Page, wording and answers** are those of plan §2–§3. Labels go to `~/vsps_labels/xm600_gold_topup1/labels_PI.jsonl`, separate from part 1.

## 2. Disclosures (printed beside every top-up row)

- **Annotator.** The PI, an author who knows the study. He saw every value while labelling. He cannot see which caption set or reference named a pair.
- **The PI has seen these images in part 1.** Disclosed beside the top-up results (run document §9.2).
- **Disclosed leak.** The annotator knows that a top-up session asks about pairs named by new models, so that group is not blind. Which of the new models named a pair is still hidden. The 50 old repeats and the controls dilute the group, and they give a cross-session test-retest figure (run document §9.2).
- **Images and captions.** The 600 images were analysed before. The S_E captions are new decodes on these images; the labels are new.

## 3. Freeze E3 (before the top-up labels are opened)

- The `a_cert.py freeze` logic is run on the 12 + |S_E| caption sets. FREEZE_E3.json is hashed, copied read-only (444), committed through the gatekeeper and pinned by one LOG line.
- It holds: the C-ref certificates of every pair of systems with at least one member in S_E; the C-label verdicts (A-CERT §4.3) of the same pairs, because A-CERT v1.1 §10 says "C-ref and C-label at once" (CC-355 W1); the budgets β(N_s; w) and the §4.4 low ends for every system in S_E.
- The 12-system FREEZE (`c51ea7dc…`) is unchanged and keeps binding every part-1 row.
- **Code needed (not written by this file).** In `scripts/a_cert/a_cert.py` only: an optional list of extra caption files, added after its unchanged call of `build_assignment.load_systems()`, never used by default. It gets a one-judge code read, and the 12-system `gate` must still reproduce its registered numbers (A-CERT §11) before FREEZE_E3 is made.

## 4. Completed status for S_E (plan §5 rule, extended)

- Base pairs: the base labels (part 1, last line wins).
- Top-up pairs: the top-up labels (part 1 of the top-up, last line wins).
- An Open Images label is never overridden.
- U and A go to the remainder; unanswered pairs too.
- No propagation between classes.
- **Agreement-only answers (CC-349 Q7).** `old_repeat` answers, control answers and part-3 answers are used only for agreement. They are never labels and never enter a status. An `old_repeat` answer never changes the base label of its pair.

## 5. Rows (descriptive; no verdict)

| Id | Row | Note |
|---|---|---|
| E1 | Completed precision `P_c` on mapped classes for each system in S_E, with the image bootstrap as registered | A-CERT §3 formula |
| E2 | The H2a counts `V_c`, `V_n` and their interval, for the pairs with at least one member in S_E | the family of an S_E system is its A-E3 model: the two prompts of one model form the within-family pair; every other pair is cross-family and printed apart (CC-355 W5) |
| E3 | H2b budget coverage for each system in S_E (covered or not), and the count | from FREEZE_E3 budgets |
| E4 | H3 on the universe `N_u'` = pairs named by any of the 12 + S_E sets, with no Open Images status | A-CERT §6 H3 definitions |
| E5 | For each A-E3 model, the completed label-gold slope over its two prompts (two points), printed as a difference, not as a slope claim | point values only; no interval (CC-355 W5) |
| E6 | Cross-session agreement on the `old_repeat` items; the top-up control agreement; the agreement of the top-up part-3 repeats with their top-up part-1 answers; beside it, the number of `old_repeat` items that are also base part-3 repeats | reported whatever its value; no gate (CC-355 W5) |

Top-up labels never enter gold (ii) for the twelve systems' rows: the registered rows use the base session's labels only (run document §9.4).

## 6. Order

Preconditions, before any top-up label value is opened: this file committed; the wrapper code-read and committed before any build; FREEZE_E3 pinned (§3). The top-up session itself starts only after the session-end LOG line that records the PI's statement that part 1 of the base assignment is finished (all 2,233 part-1 questions), so that no `old_repeat` item is asked before its part-1 answer and no top-up session can act on a part-1 label (§7) (CC-355 W2).

1. The part-1 scoring run of A-CERT v1.1 (§12 step 5) comes before the top-up scoring run of step 3. The top-up session may start once part 1 is finished (preconditions above) and may end before or after the part-1 unsealing (CC-355 W2).
2. The top-up session ends, with its LOG line: `wc -l`, sha256 and a read-only (444) copy of `labels_PI.jsonl` (plan §3).
3. A single scoring run on that copy, with the fault rule of A-CERT §12 step 5. The E-row scoring code (E1-E6, reusing the registered functions by import) is written, self-tested and mutant-tested on a rented host, gets its own one-judge code read and is committed before this run; the run refuses without the FREEZE_E3 pin line and the top-up session-end line (CC-355 W2).
4. A one-judge result read.
5. Part-2 top-up targets follow the part-2 kappa rule. Part-1 top-up targets follow the part-1 kappa rule (plan §4: 0.60), using the second annotator's labels on `overlap_images_topup1.txt`. Until then every top-up number carries "single annotator".

## 7. Never

- A top-up label changes a registered H1–H3 verdict of A-CERT v1.1, or gold (ii) of the twelve systems.
- A top-up row or a top-up kappa changes a part-1 verdict. Only the base part-1 target kappa on the base overlap can reword a part-1 verdict (A-CERT §6, §12 step 7); the top-up kappa gates top-up rows only.
- A top-up row changes a registered label of Paper A (PI-1110n).

## 8. Custody

- The writer, the judge and the coordinator open no top-up label value before this file is committed. Agents read `wc -l` and sha256 only (plan §3).
- `key.json` of the top-up stays in `~/vsps_labels/xm600_gold_topup1/`, is not served, and is read only by code. The PI does not open it.
- Until this file is committed, no one is shown a per-role, per-class or per-system figure of the top-up session (plan §3, applied to the top-up).
- Until the top-up session-end LOG line, the PI (the annotator) is shown no FREEZE_E3 figure and no Annex B row (B2-B4) of the A-E3 runs; the item counts of `BUILD_TOPUP1.json` may be shown. If the PI has seen the part-1 result (A-CERT §12 step 6) before the top-up session ends, this is disclosed beside every top-up row (CC-355 W3).

## 9. Choices Annex A left open: each recommended value below is adopted and binds (CC-355 ruling 2, W4)

| # | Open choice | Recommended |
|---|---|---|
| O1 | Bootstrap of E1 ("as registered") for S_E on I600 | The Q25 bootstrap of A-CERT §2 (first 500 rows of `default_rng(0).integers(0, 600, (2000, 600))`), because S_E lives on I600 as Q25 does |
| O2 | E2/E3 floor and level | w0 = 0.20 primary, the §4.2 grid secondary, α_S = 0.025 for pair cells and budgets (A-CERT §4.2); no other w |
| O3 | Image set for E2 pairs with a Q3 member | I537, as A-CERT runs Q3 and cross-family rows on I537; pairs of S_E with Q25 or S_E on I600 |
| O4 | E5 statistic: `F_c` or `P_c` | `100·F_c` difference (detailed − short) with gold (i) recall, as `b_F` in A-CERT §3; `P_c` difference and the ln M difference beside it |
| O5 | E6 agreement definition | Share of `old_repeat` items whose top-up Y/N equals the base last-line Y/N, over items with Y/N in both; U and A rates reported apart; control agreement as plan §4 (Y/N vs Open Images, split by hint coverage) |
| O6 | E4 bootstrap and evaluability | H3's rules unchanged: B = 2,000, seed 20261111, NOT EVALUABLE if φ2 = 0 or φ1 + φ2 < 50; printed without a RESPECTED/VIOLATED verdict word, as the row is descriptive |
| O7 | Kappa threshold for top-up targets | Plan §4 unchanged: 0.60, part-1 and part-2 target kappa computed on the top-up overlap questions only |
| O8 | Gold (ii) rows (recall, hallucination) for S_E | Not registered by this file (Annex A has none); any such row needs its own read |
| O9 | Base part-3 repeats among the 50 `old_repeat` draws | The wrapper draws from all base part-1 targets, as §9.1 writes; keep |
| O10 | Tier and bar of the read of this file | One judge, REVERSIBLE, bar 85, as for the run document (plan §5 step 7 gate) |
| O11 | E1: also print the remainder ends `P_c_lo`, `P_c_hi` (A-CERT §3) | Yes, beside the point, as A-CERT does for the twelve systems |
| O12 | E5 under run document S6 (fewer than two passing models) | E5 is per model, so it is still printed; no cross-model comparison is drawn from it |
