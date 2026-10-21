# 3 Measurement setup

## 3.1 Notation and metrics

For image $i$ in an evaluation set of $n$ images, a system $S$ produces a caption; a matcher maps it to the set $\hat O_i^S$ of mentioned object classes, with $M_i^S = |\hat O_i^S|$ and $M^S = \frac{1}{n}\sum_i M_i^S$ (mentions per image). A gold $\mathcal G$ assigns each image a set $G_i$; $\mathrm{TP}_i^S = |\hat O_i^S \cap G_i|$. We use three families of gold:

- **$k$-reference gold** $G_i^{(k)}$: the classes named in $k$ of the image's references. Analyses that vary $k$ use at most the first five references (COCO-2500, the English LVLM families of Section 7.2, and the COCO English rows of Section 5); the CHAIR gold of Section 6 reads all of them.<!-- src: .session_backup/2026-10-18/gemini_handoff/G-A8.6/coco_ref_counts.json (sha256 ad76f8c1ae90) :: /caps_summary.caps_at_mode (English LVLM families F-B and F-C; COCO-2500 slopes, exponents and support profile; exchangeability COCO English-reference rows) and /caps_summary.reads_all (E1 re-scoring of released outputs, 15 pairs); VERIFIED in manuscript/verification/paperA/G-A8.6.json --> Subsets are drawn at random over all $\binom{K}{k}$ choices ("random-$k$"); first-$k$ (file order) is only a diagnostic (Section 5).
- **Instance gold**: classes with at least one annotated instance (COCO instances, Lin et al., 2014; COCO-80 vocabulary)<!-- cite: lin2014microsoft (A5.2 v3); arXiv 1405.0312, 'Microsoft COCO: Common Objects in Context', verified 2026-10-18 via export.arxiv.org -->.
- **Instance + references**: the union of both (the CHAIR gold of Section 6 and the *full gold* of Section 8.2).

**Gold per set.** The third rung, *label gold* (the registrations' *complete gold*), is instance gold on COCO-2500, the English LVLM families, UIT-ViIC test (*uv231*) and the 295 COCO-2500 val2017 images of Section 7.6 (*cv295*). On the 600 XM3600 evaluation images (*xm600*; Section 7.5) it is human-verified labels, scored with verified precision (mentions OIV7 cannot verify are excluded).<!-- PD-28 (1); CONFIRMATION_MAP Amendment 4; G2-B prereg md:130 (oiv7 rung: verified precision over verified mapped mentions = F1_pos of evaluate_xm3600_predictions_v3.py); xm600 = data/xm3600_subset.txt (f5ab86c7) = the Section 7.5 images; cv295 ids all in data/coco_probe/manifest.json --> Only the reference rungs are nested: label gold need not contain the reference gold, and on XM3600 its rung also changes the precision rule.

Precision is micro-averaged, $P = \sum_i \mathrm{TP}_i / \sum_i M_i$. Recall is averaged over images with non-empty gold, $R = \frac{1}{|\{i: G_i\neq\emptyset\}|}\sum_i \mathrm{TP}_i/|G_i|$, and $F_1 = 2PR/(P+R)$; we call this *mixed F1*. Section 4's closed form is exact for *micro-F1*, $F_1^{\mu} = 2\sum_i\mathrm{TP}_i / (\sum_i M_i + \sum_i |G_i|)$; Section 4 and Supplementary S1 report both. CHAIR$_i$ is Rohrbach et al.'s (2018) instance-level CHAIR, which counts repeated mentions (so it is not exactly $1-P$). Where Section 8 uses CHAIR as a caption-level score, it is the class-level $1 - \mathrm{TP}_i/M_i$ (0 when $M_i = 0$).<!-- Code: .session_backup/2026-10-14/research_r10/E1/e1_chair_count.py per_image()/agg(): CHAIR_i = 100*h/n over all mentions (repeats counted), P_cls over distinct classes; .session_backup/2026-10-14/r12/H1/scripts/h1_pilot.py classes() returns a set and chair = FP/M per caption. A8.2 finding F3. Implementation conventions: Supplementary S2. -->

Matchers. English outputs are matched to COCO-80 with the CHAIR synonym list; Vietnamese outputs use a tone-normalized lexicon (Supplementary S2). Every table names its matcher.

## 3.2 The frontier and why raw comparisons fail

Across a family of systems that differ mainly in how many objects they name, true positives follow a power law in the count,
$$\mathrm{TP}(M) = a\,M^{b},\qquad 0 < b < 1,$$
so precision $P(M) = a M^{b-1}$ falls with $M$. We call $b$ the frontier exponent and $\mathrm{TP}(M)$ the count frontier. The exponent is a property of the gold as much as of the systems (Section 4): on the same 9 COCO systems it is 0.479 with one reference, 0.643 with five, and 0.846 with instance labels<!-- src: .session_backup/2026-10-14/r11_verify/c1_b1_b6_reproduction.json :: B1_L1_mstar_and_stopping.check_coco_gold.refs1_randk.b, refs5_randk.b, inst.b -->. A method that moves a system along the frontier (naming fewer or more objects with the same ranking of candidates) changes $P$, $R$, $F_1$ and CHAIR without improving object choice, so a raw difference is uninterpretable until the count difference is removed.<!-- src (A6.3 merge, VERIFIED): '9' (COCO-2500 systems) = .session_backup/2026-10-14/r11_litmaps/L1/check_coco.json :: len(systems) -->

## 3.3 Per-image count-matched controls

For method $S$ and comparator $B$ on the same images, a count-matched control replaces one side with a selection of exactly $k_i$ classes per image, built from information the comparator already has, and compares the two at equal count.

**(a) Systems with a sample pool.** Each candidate class $o$ has a sample vote share $v_{io}$ and a greedy flag $g_{io}$ (Supplementary S2).

- **(v,g) tie-averaged control** (primary)<!-- PD-2 Q1 -->: rank candidates by $v$, break ties by $g$, keep the top $k_i = M_i^S$, and average over tie-breaks at the boundary.
- **POOL-VOTE control:** rank candidates by the number of pool captions that name them.

A method must beat both.<!-- D17 condition 3 -->

**(b) Published outputs without a pool.** With one released caption per image and system (Section 6), the control is a matched subset of the longer caption's mentions at $k_i = \min(M_i^S, M_i^B)$:

- **matched prefix (primary in the re-scoring protocol, which was written after a pilot, so post hoc; Section 6.1):** the first $k_i$ distinct classes in order of mention;
- **sentence tie-average:** whole sentences in order, with the boundary sentence's classes tie-averaged;
- **uniform random subset:** $k_i$ classes drawn uniformly from the mentions (expected value over draws).

The matched prefix assumes salience ordering (assumption A2; Section 4.1); the random subset does not, and it penalizes the longer caption less. We report all three as a specification curve (Section 6). A registered seed placebo admitted the matched prefix as primary, but it ran in a harness that failed its fidelity check, so it calibrates the control and supports no count-control claim (Section 6.3).

## 3.4 Corpus-total count matching

The corpus-total control matches only $\sum_i M_i$ and lets the comparator choose its own allocation across images; its difference from the per-image control is the allocation channel.

## 3.5 The count–allocation–ranking (CAR) decomposition

For a method $S$, a base caption $G$ and a ranking source $V$, the difference telescopes into four terms,
$$F(S) - F(G) = \underbrace{D}_{\text{base re-rank}} + \underbrace{C}_{\text{count}} + \underbrace{B}_{\text{allocation}} + \underbrace{A}_{\text{ranking}},$$
where $A$ is the per-image control of Section 3.3. We report Shapley values with intervals (definitions: Supplementary S1).

## 3.6 Statistics

Intervals are 95% percentile intervals from a paired bootstrap over images ($B = 5000$, or the draw count a registration fixes); multi-seed comparisons keep all seeds of an image together. Holm correction is used where a protocol fixes it (Section 6); the registered tests of Sections 7–9 report each prediction with an uncorrected interval, as registered.<!-- N-M5: G2-B prereg §8 and A-N2 prereg 'multiplicity: No correction; every prediction is reported separately, per dataset, with its CI'; the XM3600, LongCap-Arena, VaPR, A-N1 and A-N3 registrations fix no correction; Holm: E1 protocol (15 comparisons, post hoc) and N9 §5 (six comparisons; not scored). Draw counts: XM3600 B=500 (prereg md:53), G2-B/A-N1/A-N2/A-N3 1000, LongCap-Arena and K2 2000 (minor 9; values not printed, no manifest row added) --> Where a protocol fixes a smallest effect size of interest (SESOI), a gain counts only if its Holm-corrected interval excludes 0 and its point estimate reaches the SESOI (+1.0 precision points for the 15 published comparisons of Section 6). For nulls we report the minimum detectable effect, and claims of equivalence use two one-sided tests at the registered tolerance.<!-- src (A6.3 merge, VERIFIED): '15' (E1 comparisons) = .session_backup/2026-10-13/r10_cpu/e1_x1pb_verification_v2.json :: overview_15_pairs.n_pairs; '+1.0' (E1 SESOI) = manuscript/research_r10/E1/REPORT.txt :: line 182 -->

**Analysis code and provenance.** Analysis code was written with AI assistance under the authors' direction. Four rules apply.<!-- PD-25 Q3 (a): fixed methods sentence; the sentence on numbers found in no output file was removed (PD-25, 80%). --> (i) Every reported result in the paper is produced by a script from a JSON key and listed, with the file's SHA-256, in a numbers manifest released with the code; a number with no computing script is not used.<!-- manuscript/journal_draft/number_manifest.tsv (H6 P1) --> (ii) A prediction counts as registered only if it was committed to version control before the first output it predicts; predictions written and timestamped before the first output but never committed, or committed only after it, are labelled *pre-specified* and treated as exploratory, and analyses written after a first output are labelled post hoc (Supplementary S4 gives every time)<!-- src: .session_backup/2026-10-18/paperA_tasks/A4.4/tests_status.tsv :: L1_COCO, H3_N1, H1_TC, G2_POLARIS, G3_DOCCI, X1_PB = LOCALLY_FROZEN; E1_A, XM_N2 = POST_HOC; manuscript/prereg/2026-10-18_never_committed_frozen_files.json -->. (iii) Model-produced signals are never treated as gold or as human evidence, and no new human annotation was collected. (iv) Every cited identifier was checked on a primary record (see also the AI declaration).<!-- Merged here from old §11.3 (A7.3 units s11.16–s11.19). Dropped as repeats: the withdrawn-values examples of old rule 2 (a "debiased" Chao2 human ceiling and UIT-ViIC slopes found in a log but in no output file), the old rule-3 lists of which tests carry which label (now in Tab. 7 and Supplementary S4), and the responsibility sentence (in declarations.md). -->

The frontier slope used in Sections 4 and 7 is the ordinary least squares slope of $F_1$ (in points) on $\ln M$ across the systems of a family, with an image-bootstrap interval; it is conditional on the systems.

## 3.7 The two-column reporting standard

Every object-level claim reports two columns:

1. **Raw score** (P, R, F1 or CHAIR$_i$, with the gold and matcher named), with mentions per image $M$ next to it; and
2. **one pre-declared count-controlled difference**: the per-image control of Section 3.3 for selection and decoding methods, or the frontier residual at the system's own count for training-time methods (the vertical distance to the pre-registered frontier $\mathrm{TP}(M)=aM^b$ fitted on comparator systems).

The control in column 2 is fixed before the comparison is scored, so it cannot be chosen after seeing which one favours the method; other controls go to a specification curve. Column 2 is a control for a confound, justified by construct validity, not by agreement with human judges. Raw precision responds to count mechanically (Section 3.2), and on long captions human judges also penalize naming more objects (Section 8.1); a comparison that leaves count free therefore cannot attribute a difference to object choice.
It is not a better quality score: it does not agree with human judgments better than raw precision (Section 8).
<!-- Example paragraph removed in the PD-23 length pass (its numbers are in Sections 1 and 6): 12 of 15 raw gains; 2, 2 or 6 survive under the three controls. [ src: .session_backup/2026-10-13/r10_cpu/e1_x1pb_verification_v2.json :: overview_15_pairs.n_pairs, overview_15_pairs.raw_dP_sig_pos ][ src: same :: overview_15_pairs.mcp_prefix_survives_holm, mcp_sent_tieavg_survives_holm, mcp_rand_exact_survives_holm ] -->
