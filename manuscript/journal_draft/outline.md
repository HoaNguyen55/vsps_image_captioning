# Paper A: outline

Status: first draft, 2026-10-14; §6–§10 drafted 2026-10-15 (pending-run placeholders marked `[PENDING: run, prereg]`). Scope: Paper A of the two-paper plan (`.session_backup/2026-10-14/two_paper/PLAN_2PAPERS.md`).
Framing (PD-4 Q2, D17 §3a): measurement validity of object-level caption metrics under three threats: object count, gold completeness and reference exchangeability. Vietnamese captioning on KTVIC is the motivating case only. The Vietnamese system, the KTVIC dataset audit and the two-gold analysis belong to the companion paper (Paper B, `paperB_outline.md`).

Venue order: TACL (about 10 pages plus appendix), then ACL ARR (2027-01-04 cycle), then IP&M; TMLR last. Submission due 2026-12-20. The registered DOCCI-Critique verdict is MIXED (G3-(i) primary fails; G3-(ii) point estimate passes, CI includes 0), so the TACL framing rests on the metric-property results plus bounded human evidence (PD-6 follow-up ruling recorded in `h1_g3_registered_supplement_v2.json :: registered_G3.verdict_detail.pd6_tacl_implication`).

Source convention: every number carries an HTML comment `<!-- src: path :: key -->`. Paths are relative to the repo root. Numbers marked TODO are not yet traced or not yet computed.

## Title options

1. Counting Before Comparing: Count, Gold Completeness and Reference Exchangeability in Object-Level Caption Evaluation
2. When Does an Object Metric Reward Verbosity? Measurement Validity of Object Hallucination Scores
3. What Object Hallucination Metrics Measure: Count Control, Gold Completeness and Exchangeable References
4. Object Metrics Under Incomplete Gold: A Measurement-Validity Analysis of Caption Hallucination Scores

Working choice: option 1 (short, names the three threats). Avoid "first", "novel" and "law".

## Abstract (≤ 200 words)

Object-level scores such as CHAIR, object precision and F1 are the standard evidence that a vision-language model hallucinates less. We argue that three properties of the measurement, not of the model, can decide such claims. First, the number of objects a caption names moves precision mechanically, a concern raised before; in a pre-registered per-image count-matched re-scoring of published decoding methods, significant precision gains fall from 12 of 15 to between 2 and 6 of 15, depending on the control. Second, gold completeness orders the verbosity reward. We give a proposition under which the frontier exponent rises with the number of references and the sign of F1's verbosity reward changes at most once, from negative to positive. With frozen predictions, the slope is ordered by completeness, negative with one reference and positive with instance labels; the sign with several references is not predicted by the theory and differs between datasets. Third, the proposition assumes exchangeable references; an adjacency statistic detects datasets where one writer produced all references. Human judgments support count matching and complete gold as conditions for valid comparison, not the count-controlled score as a quality measure. We release the controls as a two-column reporting standard.

<!-- word count ≤ 200 (CC-007 rewrite; PD-7 trim). Numbers: 12/15 raw, 2/15 and 6/15: .session_backup/2026-10-13/r10_cpu/e1_x1pb_verification_v2.json :: overview_15_pairs.raw_dP_sig_pos, mcp_prefix_survives_holm, mcp_rand_exact_survives_holm. -->
<!-- TODO: "We release" requires the toolkit (H2 P4) and a licence check; keep or drop at submission. -->

## Contributions

1. **A pre-registered, per-image count-matched measurement of a concern others have raised.** Fazli et al. (2026; arXiv 2609.01888) report that lower hallucination scores of inference-time methods go with lower object recall and coverage ("risk suppression"), and Sandhu et al. (2026; arXiv 2608.24966) show a CHAIR gain that comes with shorter, lower-recall captions; we measure that concern per image at matched object count. Two per-image controls (vote/greedy tie-averaged and POOL-VOTE), a corpus-total count match, and a Shapley decomposition of a score difference into count, allocation and ranking (CAR). Applied to 15 published decoding comparisons on public outputs, the number of surviving gains is reported as a specification curve over controls (2/15 to 6/15). We do not claim that count is a better unit than word length on English outputs (that registered test failed).
2. **A gold-indexed account of the verbosity reward.** Under exchangeable references and salience-ordered mentions, the frontier exponent $b(k)$ is nondecreasing in the number of references $k$, and the sign of micro-F1's verbosity reward changes at most once (from negative to positive) as $k$ grows. The F1 half-threshold rule is Lipton et al. (2014); the propensity view of human precision versus $k$ is Chen et al. (2015, §4.2). Our part is the monotonicity, the single crossing, the two-channel split, and the tests on fixed outputs. The proposition orders the slopes and fixes the two endpoints; it does not predict the number of references at which the sign changes.
3. **The ordering and the endpoints of the verbosity sign, tested out of sample.** Confirmed: the slope is ordered by gold completeness, negative at one reference and positive at instance-level gold (COCO-2500 frozen, 4 of 4; XM3600 frozen, both endpoints and the ordering held). Not predicted by the theory: the multi-reference sign. Frozen predictions of a positive all-references slope failed in three settings (two English LVLM families, XM3600); COCO-2500's positive five-reference slope is a dataset-specific outcome. On UIT-ViIC (exploratory) the five-reference sign depends on the matcher.
4. **A reference-exchangeability check.** An adjacent-doubleton statistic and two companion statistics separate independent annotators (COCO, UIT-ViIC) from corpora with a non-random reference order (Flickr30k; partly OpenViIC), and show what breaks in reference-count curves when exchangeability fails.
5. **Human validity, stated narrowly.** On THumB 1.0 and the Composite set, object precision agrees with expert precision more under complete gold, and object metrics agree with humans most on count-matched pairs; the count-controlled residual is not a better overall quality score than raw CHAIR. Polaris-COCO (registered, PASS) replicates the gold-completeness and matched-count patterns; DOCCI-Critique (long paragraphs) is MIXED. Both preregistrations were committed after the results JSON existed; disclosed.
6. **Preference data audit.** In public hallucination-preference sets, a large share of chosen/rejected pairs differ in object count, and in several sets the chosen response names fewer objects in most count-unmatched pairs; length matching does not remove this.

## Section plan (TACL, ~10 pages + appendix)

| § | Section | File | Status | Pages |
|---|---|---|---|---|
| 1 | Introduction | `sec1_introduction.md` | drafted | 1.2 |
| 2 | Related work | `sec2_related_work.md` | drafted | 1.0 |
| 3 | Measurement setup: count-matched controls, CAR, two-column reporting | `sec3_measurement_setup.md` | drafted | 1.5 |
| 4 | Theory: gold-indexed frontier and the single crossing | `sec4_theory.md` | drafted | 1.5 |
| 5 | Reference exchangeability | `sec5_exchangeability.md` | drafted | 0.8 |
| 6 | Experiments I: re-scoring published methods (E1 spec curve; N9 leaderboard) | `sec6_rescoring_published_methods.md` | drafted; [PENDING] N9, E1 K2 placebo | 1.3 |
| 7 | Experiments II: the verbosity sign across golds (COCO-2500 confirmatory; LVLM failed frozen test; UIT-ViIC exploratory; XM3600 frozen out-of-sample, 1/3 sign predictions failed; G2-B, B3 frozen) | `sec7_verbosity_sign.md` | drafted; XM3600 filled from full verdict; [PENDING] G2-B, B3 | 1.2 |
| 8 | Experiments III: human validity (THumB/Composite; Polaris; DOCCI-Critique; LongCap-Arena, CapArena) | `sec8_human_validity.md` | drafted; [PENDING] PD-7 Q2/Q3 | 1.0 |
| 9 | Preference data audit | `sec9_preference_audit.md` | drafted; conditional kill waits on N9; [PENDING] VaPR control (PD-7 Q4) | 0.4 |
| 10 | Discussion and recommendations (two-column standard, checklist) | `sec10_discussion.md` | drafted | 0.5 |
| 11 | Limitations and ethics | `sec11_limitations_ethics.md` | drafted | 0.5 |
| App. | A proofs; B matcher and lexicons; C spec curve per pair; D prereg ledger; E per-dataset adjacency tables; F numbers manifest | — | A partly in §4 | — |

Companion-paper pointers (one line each in Paper A, citing Paper B as under review): the KTVIC baseline and ladder; the 11 families of pre-registered negatives; the single-writer, punctuation and matcher audit of KTVIC (including its adjacency value, which Paper A does not quote); the UPE control-dependence example; the two-gold analysis ("two caption panels disagree").

## Figure and table plan

| ID | Content | Data status (details in `results_plan.md`) |
|---|---|---|
| Fig. 1 | Motivating schematic: one image, 1 vs 5 references vs instance labels, a terse and a verbose caption; F1 ranks them in opposite orders | illustrative; no numbers |
| Fig. 2 | Slope of F1 on $\log M$ versus gold completeness ($k=1..5$, instance, instance+refs) for COCO-2500 and the two English LVLM families and XM3600 (refs1, 2–3 refs, OIV7) | available |
| Fig. 3 | Specification curve: 15 decoding pairs × controls (raw, prefix MCP, sentence tie-avg, random subset; unadjusted and Holm+SESOI) | available; add K2 placebo when run |
| Fig. 4 | Single crossing: $\Lambda_k(M_0)$ and its b-channel / $\bar G$-channel split | available |
| Fig. 5 | Adjacency statistic by dataset with CIs and the 0.40 null (COCO, UIT-ViIC, Flickr30k, OpenViIC aggregates; no KTVIC row); XM3600 3-ref row with its own 2/3 null | available (XM3600 row keyed, §7.5) |
| Tab. 1 | Notation and the three controls | text |
| Tab. 2 | E1 spec-curve counts | available |
| Tab. 3 | N9 count-matched leaderboard (9 LLaVA-1.5-7B checkpoints) | pending (N9) |
| Tab. 4 | Verbosity slope by gold: COCO-2500 (confirmatory), English LVLM families, UIT-ViIC (exploratory), XM3600 (frozen; N1-XM-2 failed) | available |
| Tab. 5 | Human validity: THumB, Composite (Tab. 8.1), Polaris G2, DOCCI-Critique G3 | available |
| Tab. 6 | Preference data audit (7 datasets) | available |
| Tab. 7 | Prereg ledger: claim, registration time, first-look time, status | to compile |
