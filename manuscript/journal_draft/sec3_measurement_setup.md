# 3 Measurement setup

## 3.1 Notation and metrics

For image $i$ in an evaluation set of $n$ images, a system $S$ produces a caption; a matcher maps it to the set $\hat O_i^S$ of mentioned object classes, with $M_i^S = |\hat O_i^S|$ and $M^S = \frac{1}{n}\sum_i M_i^S$ (mentions per image). A gold $\mathcal G$ assigns each image a set $G_i$; $\mathrm{TP}_i^S = |\hat O_i^S \cap G_i|$. We use three families of gold:

- **$k$-reference gold** $G_i^{(k)}$: the union of classes named in $k$ of the image's reference captions. Subsets are drawn at random over all $\binom{K}{k}$ choices ("random-$k$"); the file-order choice ("first-$k$") is reported only as a diagnostic, because it is not invariant when references are not exchangeable (Section 5).
- **Instance gold**: classes with at least one annotated instance (COCO instances; COCO-80 vocabulary).
- **Instance + references**: the union of both.

Precision is micro-averaged, $P = \sum_i \mathrm{TP}_i / \sum_i M_i$. Our implementation (the `object_prf` convention inherited from earlier work in this project) averages recall over images with non-empty gold, $R = \frac{1}{|\{i: G_i\neq\emptyset\}|}\sum_i \mathrm{TP}_i/|G_i|$, and reports $F_1 = 2PR/(P+R)$. We call this *mixed F1*. Section 4's closed form is exact for *micro-F1*, $F_1^{\mu} = 2\sum_i\mathrm{TP}_i / (\sum_i M_i + \sum_i |G_i|)$; every table that tests the theory reports both (H4 T2b; Appendix A). CHAIR$_i$ is $1-P$ computed against the gold named in each table.

Matchers. English outputs are matched to COCO-80 with the CHAIR synonym list (Rohrbach et al., 2018). Vietnamese outputs use a tone-normalized lexicon matcher; its versions and their differences are documented in the companion paper. All matcher versions are pinned by file hash, and every table names the matcher.

## 3.2 The frontier and why raw comparisons fail

Across a family of systems that differ mainly in how many objects they name, true positives follow a power law in the count,
$$\mathrm{TP}(M) = a\,M^{b},\qquad 0 < b < 1,$$
so precision $P(M) = a M^{b-1}$ falls with $M$. We call $b$ the frontier exponent and $\mathrm{TP}(M)$ the count frontier. The exponent is a property of the gold as much as of the systems (Section 4): on the same 9 COCO systems it is 0.479 with one reference, 0.643 with five, and 0.846 with instance labels<!-- src: .session_backup/2026-10-14/r11_verify/c1_b1_b6_reproduction.json :: B1_L1_mstar_and_stopping.check_coco_gold.refs1_randk.b, refs5_randk.b, inst.b -->. Any method that moves a system along the frontier (naming fewer or more objects with the same ranking of candidates) changes $P$, $R$, $F_1$ and CHAIR without improving object choice. A raw difference is therefore uninterpretable until the count difference is removed.

## 3.3 Per-image count-matched controls

Let method $S$ and comparator $B$ be evaluated on the same images. A count-matched control replaces one side with a selection of exactly $k_i$ classes per image, built from information the comparator already has, and compares the two at equal count. We use two settings.

**(a) Systems with a sample pool.** When the comparator can produce several captions per image (sampled at temperature $T$, plus the greedy caption), each candidate class $o$ in image $i$ has a sample vote share $v_{io}$ (fraction of sampled captions naming $o$) and a greedy flag $g_{io}\in\{0,1\}$.

- **(v,g) tie-averaged control.** Rank candidates by $v$, break ties by $g$, keep the top $k_i = M_i^S$. If the boundary falls inside a tied block, score the expected true positives under a uniformly random choice within the block (equivalently, average over all tie-breaks). This is the primary per-image control fixed in PD-2 Q1.
- **POOL-VOTE control.** Rank candidates by the total number of pool captions (samples plus greedy) that name them, ties broken by the greedy flag, and keep the top $k_i$. The two controls can differ in strength, which is why both are reported.

Both controls are reported side by side for every pool-based comparison (D17 binding condition 3). A method beats count control only if it beats both.

**(b) Published outputs without a pool.** When only one released caption per image and system is available (the decoding comparisons of Section 6), the control is a matched subset of the longer caption's mentions at $k_i = \min(M_i^S, M_i^B)$:

- **matched prefix (MCP; registered primary):** the first $k_i$ distinct classes in order of mention;
- **sentence tie-average:** whole sentences in order, with the boundary sentence's classes tie-averaged;
- **uniform random subset:** $k_i$ classes drawn uniformly from the mentions (expected value over draws).

The three differ in what they assume about the order of mention. MCP assumes salience ordering (Section 4, assumption A2), which our support-profile test checks directly; the random subset does not, and it penalizes the longer caption less. We report all three as a specification curve (Section 6), with the registered control marked, and we pre-register a seed placebo to choose the primary control: two sampling seeds of one model must show $|\Delta P| \le 0.5$ with an interval covering 0 (TODO: E1 K2 placebo not yet run; D17 §1(c)).

## 3.4 Corpus-total count matching

The per-image control holds every $k_i$ fixed, so it cannot see a method that keeps the total number of mentions but moves them to the images where they are more likely correct. The corpus-total control matches only $\sum_i M_i$: the comparator's candidates across all images are ranked by its own score and the top $\sum_i M_i^S$ are kept, so the comparator chooses its own allocation. The difference between the per-image and the corpus-total control is the allocation channel.

## 3.5 The count–allocation–ranking (CAR) decomposition

For a method $S$, a base caption $G$ (greedy) and a ranking source $V$ (the pool vote), the difference $F(S) - F(G)$ telescopes into four terms:
$$F(S) - F(G) = \underbrace{D}_{\text{base re-rank}} + \underbrace{C}_{\text{count}} + \underbrace{B}_{\text{allocation}} + \underbrace{A}_{\text{ranking}},$$
where $D = F(V \text{ at } G\text{'s } k_i) - F(G)$; $C$ moves from $G$'s per-image counts to counts with $S$'s total, keeping $G$'s allocation shape; $B$ moves to $S$'s own per-image counts $k_i$ under $V$'s ranking; and $A = F(S) - F(V\text{ at }S\text{'s }k_i)$ is exactly the per-image control of Section 3.3. Because the telescoping order matters, we also report the Shapley value of each factor (count, allocation, ranking), averaged over the orders in which the factors are switched on. Two cautions apply. First, the intermediate vertices of the Shapley cube are not exactly count-neutral, so the allocation and ranking terms can absorb small count shifts (RV1 item 2c); we report the mean count at every vertex. Second, terms come with image-bootstrap intervals; a term whose interval covers 0 is not interpreted.

**Remark (re-thresholding cannot move A).** If a method only re-thresholds the comparator's own per-candidate score (it keeps candidates in the comparator's order and changes how many it keeps), then at the method's own $k_i$ it selects exactly the control's set, so $A = 0$ by construction. Only a method that brings in evidence the comparator's score does not contain (retrieval, grounding, a probe, new training signal) can make $A \neq 0$. This is the probability ranking principle applied to object mentions; we state it as a classification rule for methods, not as a new result.

## 3.6 Statistics

Intervals are 95% percentile intervals from a paired bootstrap over images ($B = 5000$ unless stated). Multi-seed comparisons resample images and keep all seeds of an image together (image-clustered). Families of tests (P, R, F1, CHAIR$_i$ per comparison; or the 15 comparisons of Section 6) are Holm-corrected. Where a smallest effect size of interest (SESOI) is registered, a gain counts only if its Holm-corrected interval excludes 0 and its point estimate reaches the SESOI (+1.0 precision points for the decoding comparisons). For nulls we report the minimum detectable effect, and claims of equivalence use two one-sided tests at the registered tolerance.

The frontier slope used in Sections 4 and 7 is the ordinary least squares slope of $F_1$ (in points) on $\ln M$ across the systems of a family, with an image-bootstrap interval; it is conditional on the systems.

## 3.7 The two-column reporting standard

Every object-level claim reports two columns:

1. **Raw score** (P, R, F1 or CHAIR$_i$, with the gold and matcher named), with mentions per image $M$ next to it; and
2. **one pre-declared count-controlled difference**: the per-image control of Section 3.3 for selection and decoding methods, or the frontier residual at the system's own count for training-time methods (the vertical distance to the pre-registered frontier $\mathrm{TP}(M)=aM^b$ fitted on comparator systems).

The control in column 2 is fixed before the comparison is scored; other controls go to an appendix specification curve. This avoids choosing the control after seeing which one favours the method. Column 2 is an attribution tool: it says whether a difference survives when count is held fixed. It is not a better quality score. In the human judgments of Section 8, the count-controlled residual agrees with overall human preference less often than raw CHAIR (THumB −0.190 [−0.277, −0.108]; Composite −0.083 [−0.101, −0.065] in pairwise agreement)<!-- src: .session_backup/2026-10-14/r12/H1/pilot_results.json :: THumB.P1b_acc(z->T)-acc(-CHAIR->T).est, .ci; Composite.P1b_acc(z->T)-acc(-CHAIR->T).est, .ci -->.

**Why the control must be declared: an example.** On the 15 published decoding comparisons of Section 6, 12 raw precision gains are significant<!-- src: .session_backup/2026-10-13/r10_cpu/e1_x1pb_verification_v2.json :: overview_15_pairs.raw_dP_sig_pos -->. At matched count, 2 survive Holm correction and the SESOI under the registered matched-prefix control, 2 under the sentence tie-average and 6 under the uniform random subset<!-- src: same :: overview_15_pairs.mcp_prefix_survives_holm, mcp_sent_tieavg_survives_holm, mcp_rand_exact_survives_holm -->; the mean precision difference is +3.41 raw, +0.62 with the matched prefix and +2.76 with the random subset<!-- src: same :: overview_15_pairs.mean_dP_raw, mean_dP_MCP_prefix, mean_dP_MCP_rand_exact -->. The registered stopping rule (more than one third of gains surviving) is not triggered under the first two controls and is triggered under the third<!-- src: same :: overview_15_pairs.k4_en_verdict_prefix, k4_en_verdict_sent_tieavg, k4_en_verdict_random_subset -->. A reader who sees only one column cannot tell which of these was chosen, or why. The same control dependence appears in the Vietnamese case, reported in the companion paper.
