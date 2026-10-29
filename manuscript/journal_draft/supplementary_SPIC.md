# Supplementary Material

**Gold Completeness and the Verbosity Slope of Object Hallucination Metrics: A Registered Audit**

Entries reproduce, in full, material that the main text shortens or omits, with times in UTC.

## S1 Proofs and derivations

For a method $S$, a base caption $G$ (greedy) and a ranking source $V$ (the pool vote), the difference $F(S) - F(G)$ telescopes into four terms:
$$F(S) - F(G) = \underbrace{D}_{\text{base re-rank}} + \underbrace{C}_{\text{count}} + \underbrace{B}_{\text{allocation}} + \underbrace{A}_{\text{ranking}},$$
where $D = F(V \text{ at } G\text{'s } k_i) - F(G)$; $C$ moves from $G$'s per-image counts to counts with $S$'s total, keeping $G$'s allocation shape; $B$ moves to $S$'s own per-image counts $k_i$ under $V$'s ranking; and $A = F(S) - F(V\text{ at }S\text{'s }k_i)$ is exactly the per-image control of Section 3.3. Because the telescoping order matters, we also report the Shapley value of each factor (count, allocation, ranking), averaged over the orders in which the factors are switched on. Two cautions apply. First, the intermediate vertices of the Shapley cube are not exactly count-neutral, so the allocation and ranking terms can absorb small count shifts; we report the mean count at every vertex. Second, terms come with image-bootstrap intervals; a term whose interval covers 0 is not interpreted.

**Remark (re-thresholding cannot move A).** If a method only re-thresholds the comparator's own per-candidate score (it keeps candidates in the comparator's order and changes how many it keeps), then at the method's own $k_i$ it selects exactly the control's set, so $A = 0$ by construction. Only a method that brings in evidence the comparator's score does not contain (retrieval, grounding, a probe, new training signal) can make $A \neq 0$. This is the probability ranking principle applied to object mentions; we state it as a classification rule for methods, not as a new result.

**Two channels.** The increase of $\Lambda_k$ has two parts: the *b-channel* $\Delta\operatorname{logit} b_k$, which exists only because later mentions are less likely to be named (salience-dependent missingness), and the *$\bar G$-channel* $\Delta\ln\bar G(k)$, which exists under any missingness. If gold objects were missing completely at random (the SCAR assumption of positive–unlabeled learning), $b_k$ would not depend on $k$ and the b-channel would be zero: observed $M^*$ would only rescale with the label frequency. A uniform PU-style correction therefore cannot remove the part of the flip carried by the b-channel.

**Closed form.** With deterministic salience $\pi_m = \pi_1 m^{-\theta}$ and $s_m \propto m^{-D}$,
$$b_k(M) \approx 1 - D - \theta\,\varphi_k(\pi_M),\qquad \varphi_k(\pi) = \frac{k\pi(1-\pi)^{k-1}}{1-(1-\pi)^k},$$
where $\varphi_k$ is the elasticity of $c_k$ ($\varphi_1 = 1$, $\varphi_k \to 0$ as $k\to\infty$). Then $\theta = b_\infty - b_1$ is the reference-incompleteness part of the exponent deficit and $D$ the system part.

#### Proof sketch

(a) Write $1/b_k = \sum_{m\le M} \frac{s_m}{M s_M}\cdot\frac{g_k(m)}{g_k(M)}$. With $x = (1-\pi)^k$, $\frac{d}{dk}\ln c_k(\pi) = h(x)/k$ where $h(x) = -x\ln x/(1-x)$, and $h$ is increasing on $(0,1)$ because $h'(x)$ has the sign of $x - 1 - \ln x \ge 0$. Hence $c_{k'}(\pi)/c_k(\pi)$ is decreasing in $\pi$ for $k' > k$: the kernel $c_k(\pi)$ is reverse-rule of order 2 in $(k,\pi)$. Under (A2), for $m < M$ the symmetrized double integral over $x<y$ of $[c_{k'}(x)c_k(y) - c_k(x)c_{k'}(y)]\,[f_M(x)f_m(y) - f_M(y)f_m(x)]$ is nonnegative by the basic composition formula for totally positive kernels (Karlin, 1968, *Total Positivity*, Vol. I; we did not check the section number against a primary page, because the book has no DOI or Crossref record and only its author, title and year could be checked; the step itself was re-derived and checked numerically), so $g_k(m)/g_k(M)$ is nonincreasing in $k$ and $1/b_k$ falls. As $k\to\infty$, $c_k(\pi)\to 1$ for $\pi > 0$, which gives $b_\infty$.
(b) Each $c_k(\pi)$ is increasing and concave in $k$; expectations and sums preserve both.
(c) $d\ln F_1^\mu/d\ln M = b - M/(M+\bar G)$, which is positive iff $b/(1-b) > M/\bar G$; at $M^*$ the second derivative is $-b(1-b)/M^{*2} < 0$.
(d) $\operatorname{logit} b_k$ is nondecreasing in $k$ by (a), and $\ln\bar G(k)$ is increasing by (b); their sum is nondecreasing, so it crosses 0 at most once and only upward.

All steps were checked numerically on a grid ($k = 1,\dots,10$; RR2 of $c_k$, of a lag-1 dependent kernel and of the 5-reference kernel) in a numerical self-check script. Lipton et al. theorem numbering checked against arXiv 1402.1892v2 (Theorem 1, Corollary 1; numbering in the LNCS version not checked). The composition step was re-derived: with rows $(k',k)$ of the RR2 kernel $c$ and columns $(M,m)$ of the RR2 family $f$ under (A2), the basic composition formula gives $g_{k'}(M)g_k(m) - g_{k'}(m)g_k(M) \ge 0$.

**Under (A1), the subset design does not matter.** Every $k$-subset design (first-$k$, random-$k$, fixed slots) has the same expected $b(k)$, $\bar G(k)$ and slope. A difference between designs is therefore a test of (A1) (Section 5).

#### Which F1

The closed form in (c)–(d) is exact for micro-F1. The mixed F1 of Section 3.1 (micro precision, image-averaged recall) has the sign condition $P\,d > R\,(1-b)$, where $d$ is the exponent of recall in $M$ ($d < b$; e.g. 0.425 vs 0.478 on COCO with one reference). Image-averaged recall lowers the optimum $M^*$ and makes the one-reference penalty more robust. Every table and figure in Section 6 reports mixed F1, except that the label-gold F1 on XM3600 images pairs verified precision with micro recall over verified-present classes, as registered; micro-F1 otherwise appears only where a table of this supplement names it, and we never apply the micro closed form to mixed F1.

**Closed form.** Fitting $b_k = 1 - D - \theta\varphi_k(\pi_M)$ to the five random-$k$ points gives root-mean-square error 0.0017 with $D = 0.342$ on COCO-5000. Forcing $D$ to the instance-plus-references value fits worse (0.0139). Read as a model-based extrapolation, the reference limit $b_\infty$ is near 0.66, about 0.21 below the instance-plus-reference value: the share of present objects that caption writers do not name, which more references cannot recover. This extrapolation rests on two parameters fitted to four points; Supplementary S1 gives the fit, and the registered large-$k$ test on PASCAL-50S (50 references per image) is reported in Section 6.4: the slope rose at every registered level (k = 1, 2, 5, 10, 20, 50), but it is a test of the ordering, not of this extrapolation, which it neither confirms nor refutes.

**Positive dependence shrinks the gold.** For positively associated indicators, $P(o \notin G_k) \ge (1-\pi)^k$ (Esary, Proschan and Walkup, 1967, Ann. Math. Statist. 38(5):1466–1474, DOI 10.1214/aoms/1177698701) (bibliographic data verified via Crossref; we did not check where in the paper the product inequality appears, because the publisher full text is behind a bot challenge), so coverage and $\bar G(k)$ grow more slowly than under independence. For a lag-1 chain with autocorrelation $\rho$, $c_k(\pi) = 1-(1-\pi)\big(1-(1-\rho)\pi\big)^{k-1} \approx k_{\text{eff}}\,\pi$ for small $\pi$, with $k_{\text{eff}} = 1 + (k-1)(1-\rho)$: $k$ captions from one writer act like $k_{\text{eff}} < k$ independent ones. The chain kernel is still reverse-rule of order 2 (checked numerically for $\rho \in \{0.2, 0.5, 0.8\}$), so Proposition 1 holds in $k_{\text{eff}}$ and the crossing moves to larger $k$. The chain model predicts that dependence acts on the gold size to first order and on the exponent only to second order.

**Large-$k$ behaviour.** The reference limit of the exponent is a two-parameter extrapolation from five points. A test with 10 or 50 references per image, the large-reference-set test, is registered but not run: it needs GPU decodes on two large-reference datasets, which are out of scope for this paper.

### Further detail for Section 4

#### Proposition

**Proposition 1.** Under (A1)–(A3):

(a) **Monotone exponent.** $b_k(M)$ is nondecreasing in $k$. Its limits are
$$b_1(M) = \frac{M s_M\,\mathbb E_{F_M}[\pi]}{\sum_{m\le M} s_m\,\mathbb E_{F_m}[\pi]},\qquad b_\infty(M) = \frac{M s_M}{\sum_{m\le M} s_m} =: 1-D,$$
where $D$ is the part of the exponent deficit that comes from the system alone.

(b) **Concave gold growth.** $\bar G(k)$ is increasing and concave in $k$.

(c) **Sign condition** (Lipton et al., 2014, arXiv v2, Thm. 1 and Cor. 1; cited, not new). Micro-F1, $F_1^\mu = 2\,\mathrm{TP}/(M+\bar G)$, increases with $M$ if and only if $p_{\text{marg}} > F_1^\mu/2$, equivalently
$$\frac{b_k}{1-b_k} > \frac{M}{\bar G(k)}.$$
With constant $b$, $F_1^\mu$ has a unique maximum at $M^*(k) = b_k\,\bar G(k)/(1-b_k)$. For mixed F1 the condition differs (Supplementary S1), so the closed form is applied only to micro-F1.

(d) **Single crossing.** Let
$$\Lambda_k(M) = \operatorname{logit} b_k(M) + \ln \bar G(k) - \ln M .$$
$\Lambda_k(M)$ is nondecreasing in $k$. Hence, at a fixed family centre $M_0$, the sign of micro-F1's verbosity slope, $\operatorname{sign}\Lambda_k(M_0)$, changes at most once as references are added, and only from negative to positive; $M^*(k)$ is nondecreasing in $k$. Proof in Supplementary S1.

**Two channels.** $\Lambda_k$ rises through two channels: the *b-channel* $\Delta\operatorname{logit} b_k$, which exists only because later mentions are named less often, and the *$\bar G$-channel* $\Delta\ln\bar G(k)$, which exists under any missingness. Under missingness completely at random (SCAR) the b-channel is zero. Because the $k$-reference golds are nested, the $\bar G$-channel alone already orders the slopes in $k$, so the ordering is expected even if objects are missing from references at random. Confirming the ordered pattern therefore supports it empirically; it does not test the propensity model. Only the b-channel is specific to the model.

#### Post hoc descriptive checks on COCO-5000

The checks below use 9 systems on COCO-5000 (Qwen2.5-VL-7B variants; Vietnamese captions mapped to COCO-80 with a Vietnamese object lexicon and scored against the English references and instance labels; $M$ 0.84–2.18); its seed-42 half, COCO-2500, is the discovery set, on which the predictions were pre-specified and never committed, so the checks are exploratory. COCO-5000 is the full Karpathy test split (5,000 images); all nine systems were decoded on every image, four of them (the two adapters, each with both prompts) in a post hoc top-up of the 2,500 images outside the seed-42 discovery half. The parity check and top-up used 1.79 GPU-hours; the top-up was interrupted once by a machine reboot and resumed from the last written image in an unchanged software environment, and before it a 50-image re-decode of the discovery half matched the earlier captions byte for byte for all four runs. The rest of this subsection is post hoc.

**Part (a), monotone exponent.** On COCO-5000 with random-$k$ subsets, $b(k)$ rises from 0.475 at $k=1$ to 0.638 at $k=5$ and 0.850 with instance labels; the English LVLM families show the same rise (Section 6.1).

**Assumption (A2), salience ordering, tested directly.** Relative to all mentions, the share of marginal mentions (the last of each caption) falls with reference support $n$: 1.82, 1.24, 0.84, 0.48, 0.25 for $n = 1..5$, monotone in 100% of bootstrap draws, and 3.16 for present objects named by no reference.

**Part (d), single crossing.** Part (d) concerns micro-F1. On COCO-5000 the micro-F1-on-$\ln M$ slope is −2.26 [−3.16, −1.39] at $k=1$, then +5.45, +9.65, +12.36, +14.29 for $k=2..5$. The slope rises monotonically with completeness and changes sign once, from negative to positive; the mixed F1 shows the same pattern (Table 6.1), and where the change occurs is dataset-specific.

The closed form does not give the one-reference sign: at one reference $\Lambda = 0.014$ [−0.040, 0.066] sits at the boundary, and in 66% of bootstrap replicates $\Lambda_U(1) > 0$ while the slope is negative. With $M^* = 1.24$ against a median $M$ of 1.21, the systems straddle the optimum. From two references on, $\Lambda > 0$ with intervals excluding 0, rising at every step (post hoc image bootstrap, $B$ = 2,000; Supplementary S7). The negative one-reference sign is therefore an observation, not a consequence of the proposition.

**Channel split.** Between one and five references (Fig. 4), the b-channel carries 61% of the increase in $\Lambda$ on COCO-5000 (post-hoc interval [60.1, 62.3]) and 71% from one reference to instance labels ([70.3, 71.9]). These shares are post hoc and from COCO-5000 only; there, most of the rise comes from salience-dependent missingness, which a uniform (SCAR) correction cannot remove.

![Fig. 4](figs/fig4_lambda_channels.svg)

**What the decomposition does not predict.** It does not say where the sign changes, and it does not predict the sign with several references: positive all-references slopes were predicted and failed on two English LVLM families (pre-specified; Section 6.1) and on XM3600 (registered; Section 6.2). An exponent fitted on short-caption systems did not transfer to verbose ones; $M^*$ is descriptive, not an out-of-regime predictor.

## S2 Matchers, lexicons, metric conventions and control implementation

The matcher-sensitivity analysis is the second part of S2.

Precision is micro-averaged, $P = \sum_i \mathrm{TP}_i / \sum_i M_i$. Our implementation (a convention inherited from earlier work in this project) averages recall over images with non-empty gold, $R = \frac{1}{|\{i: G_i\neq\emptyset\}|}\sum_i \mathrm{TP}_i/|G_i|$, and reports $F_1 = 2PR/(P+R)$. We call this *mixed F1*. Section 4's closed form is exact for *micro-F1*, $F_1^{\mu} = 2\sum_i\mathrm{TP}_i / (\sum_i M_i + \sum_i |G_i|)$; every table that tests the theory reports both (Supplementary S1). CHAIR$_i$ is the instance-level CHAIR of Rohrbach et al. (2018): the share of object mentions that are absent from the gold, with a repeated mention of a class counted each time. It is therefore not exactly $1-P$, which counts each class once per image; it is the quantity whose published values we reproduce in Supplementary S3. Where Section 7 uses CHAIR as a caption-level score, it is the class-level complement of precision, $1 - \mathrm{TP}_i/M_i$ (0 when $M_i = 0$), computed against the gold named in each table.

Matchers. English outputs are matched to COCO-80 with the CHAIR synonym list (Rohrbach et al., 2018). Vietnamese outputs use a tone-normalized lexicon matcher; its versions and their differences are documented in the companion manuscript on KTVIC (in preparation; a copy is available to the editor). All matcher versions are pinned by file hash, and every table names the matcher. The decoding settings of the second-backbone and eight-LVLM tests (temperatures, nucleus sampling, seed, numeric precision and token caps) are those fixed in their registrations, which are released with the code.

**(a) Systems with a sample pool.** When the comparator can produce several captions per image (sampled at temperature $T$, plus the greedy caption), each candidate class $o$ in image $i$ has a sample vote share $v_{io}$ (fraction of sampled captions naming $o$) and a greedy flag $g_{io}\in\{0,1\}$.

- **(v,g) tie-averaged control.** Rank candidates by $v$, break ties by $g$, keep the top $k_i = M_i^S$. If the boundary falls inside a tied block, score the expected true positives under a uniformly random choice within the block (equivalently, average over all tie-breaks). This is the primary per-image control.
- **POOL-VOTE control.** Rank candidates by the total number of pool captions (samples plus greedy) that name them, ties broken by the greedy flag, and keep the top $k_i$. The two controls can differ in strength, which is why both are reported.

Both controls are reported side by side for every pool-based comparison. A method beats count control only if it beats both.

### Further detail for Section 3: pool controls and matcher sensitivity

**(a) Systems with a sample pool.** Each candidate class $o$ has a sample vote share $v_{io}$ and a greedy flag $g_{io}$ (Supplementary S2).

- **(v,g) tie-averaged control** (primary): rank candidates by $v$, break ties by $g$, keep the top $k_i = M_i^S$, and average over tie-breaks at the boundary.
- **POOL-VOTE control:** rank candidates by the number of pool captions that name them.

A method must beat both.

#### Matcher and label-map sensitivity

This is a post-hoc sensitivity analysis, not a registered test. We re-ran every analysis in this paper that uses an English reference gold with one English matcher throughout: the CHAIR rules that score the English captions of Supplementary S3 replace the reference-side extractor. We also re-ran the XM3600 analyses without the five doubtful Open Images mappings. The COCO rows below are the matcher sensitivity on COCO-2500, the seed-42 discovery half (Supplementary S1), not re-run on COCO-5000.

**Reproduction.** Run with the original matcher and map, the copied code reproduces the cited values exactly (34 of 34 comparisons).

**No headline change.** No verdict, ordering, endpoint or sign changes in 55 checks.

**Small shifts in the values:**
- COCO-2500 slopes: one reference −4.28 to −4.92, five references 11.08 to 10.87.
- Micro-F1 slope at one reference: −1.84 to −2.31.
- $\Lambda_U(1)$: 0.047 to 0.017, with its interval still including 0, [−0.055, 0.094].
- b-channel shares: 0.613 to 0.634 and 0.709 to 0.717.
- Adjacent-doubleton shares of Section 5: by at most 0.015.
- XM3600 OIV7 slope: 19.32 to 19.25 with the doubtful links dropped, and to 21.60 with the doubtful entries dropped.

**Two descriptive statements change:**
- the gap between the first-k and random-k one-reference slopes grows from 0.07 to 0.15;
- the share of bootstrap replicates in which $\Lambda_U(1)$ and the one-reference slope have opposite signs falls from 0.88 to 0.68 (Supplementary S1).

**Registered gold-size checks.** The registered XM3600 gold-size checks compare with values frozen under the original map, so dropping mappings moves them by construction. They were reproduced for 14 of 15 values originally, and for 10 or 9 of 15 after the drops.

## S3 Re-scoring of published comparisons: per-comparison results and control checks

### Data, fidelity and specification curve (moved from the main text in revision 1)

This section applies the controls of Section 3.3(b) to methods whose authors released their captions. The re-scoring is post hoc and exploratory (Supplementary S3). A confirmation on new method–baseline pairs was planned but not run, because too few eligible pairs were found to meet its pre-set minimum.

#### Data and fidelity

We use the released CHAIR evaluation outputs of OPERA (Huang et al., 2024) and of "Less is More" (Yue et al., 2024). Pairing each method with its authors' baseline gives 15 comparisons, 11 of decoding methods and 4 of the stopping method, on 495 to 499 COCO val2014 images each. Objects are matched to COCO-80 against the CHAIR gold: instance labels plus all reference captions (5 per image, except 3 of the 1,467 images, which have 6).

The re-implementation reproduces the four published CHAIR rows we checked to within 0.6 points on every reported column (the protocol's fidelity check).

**Registration.** The protocol was committed after a pilot had scored these 15 comparisons (Supplementary S4), so Table S3.1 is not registered; only the seed placebo was registered before its output.

#### The specification curve

"Unadjusted" means that the 95% bootstrap interval excludes 0; "Holm + SESOI" means that the Holm-corrected interval excludes 0 and the point estimate reaches +1.0 precision points (Section 3.6 of the main text).

**Table S3.1.** POST HOC specification curve (not registered; no verdict except the seed placebo row). Precision gains of 15 published methods (11 decoding comparisons, 4 of a stopping method) over their baselines, by control.

| Control | Significant gains, unadjusted | Significant after Holm + SESOI | Mean ΔP (points) |
|---|---|---|---|
| None (raw) | 12 / 15 | — | +3.41 |
| Matched prefix (protocol primary) | 3 / 15 | 2 / 15 | +0.62 |
| Sentence tie-average | 4 / 15 | 2 / 15 | +0.65 |
| Uniform random subset | 11 / 15 | 6 / 15 | +2.76 |
| Seed placebo (registered; run in the harness that failed its fidelity check, Supplementary S3) | matched prefix admissible and selected (prediction HELD) | — | — |

#### Training-based methods: a registered leaderboard (not scored)

Trained methods' outputs are not released, so the registered checkpoint leaderboard decodes public LLaVA-1.5-7B checkpoints and their base model on the 500 CHAIR images (greedy, one beam, 512 new tokens, fp16, batch 8). Its fidelity check failed: the decode harness did not reproduce the published base CHAIR_i within the registered tolerance (|ΔCHAIR_i| = 1.49 > 1.0), so the leaderboard was not scored. Base-only descriptives are in Supplementary S3. No method output was scored or read.

Its registered predictions could not be tested (Supplementary S4), including prediction (b), the second half of the two-part withdrawal rule of Section 7.3.

### Material moved from Section 6 in revision 1

**Under the order-preserving controls, most of the raw gain is a count effect (post hoc).** Twelve raw gains are significant; under the two controls that keep the order of mention, two remain. The mean gain falls from +3.41 to +0.62 points with the matched prefix and to +0.65 with the sentence tie-average, and the same two remain under both (Supplementary S3).

**One gain reverses.** OPERA on Shikra has a raw precision gain over beam search of +3.47 [+0.75, +6.03] points, and a significant loss at matched prefix, −1.23 [−2.42, −0.08]. Its captions name 16% fewer objects, consistent with the raw gain coming from naming fewer objects (post hoc).

**The random-subset control is the outlier.** Under it, 6 of 15 gains remain and the mean gain stays at +2.76 points, because it removes the count difference but not the order effect (assumption A2; Supplementary S3).

**Withdrawal rule (fixed after the pilot).** The protocol abandons the count-confound claim if more than 5 of 15 gains remain significant at matched count: not triggered under the order-preserving controls, triggered under the random subset. We report the whole curve and draw no confirmatory conclusion.

#### Placebos and positive controls (old Section 6.3)

**Registered seed placebo.** The placebo compares two sampling seeds of one model on the same images; a control that finds a "gain" there is miscalibrated. Under rules registered before any placebo output, a control is admissible if $|\Delta P| \le 0.5$ with an interval covering 0, and the first admissible control is primary (Supplementary S4). The prediction held: the matched prefix is admissible and was selected. The placebo was decoded in the leaderboard harness of Supplementary S3, which failed its fidelity check; both seeds share that harness, so the result calibrates the paired control only and is not evidence for any count-control claim.

**Positive control.** Removing the first hallucinated object from each baseline caption should raise precision at matched prefix by at least 3 points (fixed after the pilot); the control is underpowered at 500 images on 2 of 8 baselines, so the nulls of Table S3.1 are results at this sample size (Supplementary S3).

**Count versus length.** We predicted that object count explains precision gains better than word length (pre-specified, committed after its first output: exploratory); the difference, +0.186 [−0.257, +0.579] points against a required +1.0, triggered its withdrawal rule, and the claim is withdrawn.

**Most of the raw gain is a count effect.** Twelve raw gains are significant; under the two controls that keep the order of mention, two survive. The mean gain falls from +3.41 to +0.62 points with the matched prefix and to +0.65 with the sentence tie-average. The same two comparisons survive both order-preserving controls: OPERA versus greedy decoding on InstructBLIP (+3.88 [+2.49, +5.27] points at matched prefix) and the end-of-sequence method on MiniGPT-v2 (+2.81 [+0.91, +4.67]). In a descriptive decomposition with the baselines' own captions as reference points, count and per-image allocation account for 81.8% of the raw gain under the matched prefix and 80.9% under the sentence tie-average; we do not attach intervals to these shares, because several comparisons share a baseline.

**The random-subset control is the outlier, and it is the weakest control.** Under the uniform random subset, 6 of 15 gains survive and the mean gain stays at +2.76 points. This control keeps a random $k_i$ of the longer caption's mentions, so it removes the count difference but not the order effect: when later mentions are less often correct (assumption A2, which the support profile of Supplementary S1 confirms on COCO), a random subset of a long caption keeps more late, weak mentions than the shorter caption has, and the longer caption is penalized less than at matched prefix. The gap between the two controls is largest where the count ratio is smallest; for OPERA on Shikra against greedy decoding (count ratio 0.808), the matched-prefix difference is −1.23 [−2.62, +0.08] and the random-subset difference is +5.45 [+3.36, +7.40]. The random-subset control also fails its own two-seed check (two random draws of the same caption set must agree; |ΔP| within the seed placebo's bound and an interval covering 0) in 2 of 8 baselines. We report it because a reader who believes mentions are not salience-ordered would choose it.

**Substitute placebo (not the registered one).** Swapping the two captions of each image at random between method and baseline gives a null by construction. All 15 comparisons pass it. This checks the bootstrap machinery, not the calibration of a control, and we do not count it as the registered placebo.

**Positive control.** Removing the first hallucinated object from each baseline caption should raise precision at matched prefix by at least 3 points (a rule of the re-scoring protocol, fixed after the pilot). The point estimate reaches 3 points for 6 of 8 baselines, and the lower interval bound does for 3 of 8; the verdict under that rule is that the control is underpowered at 500 images on 2 of 8 baselines. The protocol's remedy, enlarging the image set to 2,000, has not been taken; the null results in Table S3.1 are therefore results at this sample size, and Supplementary S3 gives the minimum detectable effect for each comparison (80% power, standard error from the interval width, α = 0.05 and 0.05/15).

Decoding and stopping methods are one half of the literature. Most recent anti-hallucination methods are trained (preference optimization, reinforcement learning, data augmentation), and their authors do not release per-caption outputs, so they must be decoded again. The registered checkpoint leaderboard was to decode 9 public LLaVA-1.5-7B checkpoints (among them POVID (arXiv 2402.11411), RLAIF-V (arXiv 2405.17220), HALVA (arXiv 2405.18654), CHAIR-DPO (arXiv 2508.20181), SENTINEL (ICCV 2025, doi:10.1109/ICCV51701.2025.00067), HA-DPO (arXiv 2311.16839), HSA-DPO (arXiv 2404.14233) and OPA-DPO (CVPR 2025, doi:10.1109/CVPR52734.2025.00992), plus the base model), on the same 500 CHAIR images, with greedy decoding and 512 new tokens, and to score each against the base model raw, at matched prefix, with the sentence tie-average and with the CAR decomposition of Section 3.5. The leaderboard's fidelity check failed on the base run, so the leaderboard was not scored and no method output was read (Supplementary S3).

**Leaderboard base run (Supplementary S3).** Descriptive and base-only: CHAIR_i 13.91 against a published 15.4, CHAIR_s 50.3 against 50.0 (tolerance 1.5), on the 495 of 500 images with a COCO instance annotation, which the registered scorer requires; the same scorer gives CHAIR_i 15.26, CHAIR_s 50.5 and Recall 77.5 on the released Less-is-More base captions, and 3.6% of the 500 base captions match those exactly (harness variance, exploratory: below).

Harness variance (exploratory: post hoc, base-only): on the same 495 images, the base captions decoded in the checkpoint-leaderboard harness minus the released Less-is-More base captions give CHAIR_i −1.351 [−2.694, −0.052], CHAIR_s −0.202 [−4.242, +4.040] (interval includes 0) and object F1 +1.430 [+0.026, +2.816], and 10 of the 15 re-scored published comparisons (post hoc) have a smaller |ΔCHAIR_i| than the CHAIR_i point gap; this concerns reproduction variance only.

## S4 Registration ledger, full frozen-prediction texts and run histories

Quoted and frozen registration texts in this section keep their original set codes: cv295 = COCO-295, uv231 = UIT-ViIC-231 and xm600 = XM3600-600 in the main text; a "rung" of a registration is a gold level.

### Table S4.0: full registration ledger (moved from Section 1.2 in revision 1)

**Table S4.0.** Every registered prediction of this paper, with its status, its registered verdict copied from the decide file, and where it is reported, followed by the post hoc rows that carry sentences of the abstract. Registered = committed before the first output it predicts (Section 3.6); exploratory analyses and their times are in Supplementary S4.

| ID | Test (registered id) | Status | Verdict | Where |
|---|---|---|---|---|
| X-0 | XM3600 frozen inputs (FROZEN-INPUTS-SHA256) | registered | PASS | S4 |
| X-G | XM3600 gold sizes, 15 values (GBAR-*) | registered | 14 IN | 6.2, S7 |
| X-G6 | of which: one-reference gold size, non-empty images (GBAR-refs1_randk-Gbar_nonempty) | registered | OUT | 6.2 |
| A1 | One-reference slope < 0 (N1-XM-1) | registered | PASS | 6.2 |
| A2 | All-references slope > 0 (N1-XM-2) | registered | **FAIL** | 6.2 |
| A3 | Label-gold slope > 0 (N1-XM-3) | registered | PASS | 6.2 |
| A4 | Ordering 1 ref < all refs < label gold (N1-XM-4) | registered | PASS | 6.2 |
| A5 | Sign agreement with the F1 optimum (N1-XM-5) | registered | **FAIL** | 6.2 |
| X-21 | XM3600 reference adjacency, 150 images (N2-XM-FULL150) | verdict file: registered; registration quotes its own result: post hoc | PASS (verdict file); treated as post hoc | 6.2 |
| X-22 | Two-panel transfer, Vietnamese vs English references (C3-XM-PANEL-DRHO-113-TO-80) | registered | PASS, with a mixed estimator whose interval includes 1 (no primary estimator registered) | this table only |
| X-23–25 | Reference vs verified-label predictions for the adapters (C3-OIV7-1, -2, -3) | registered | PASS ×3 | this table only |
| A6 | Second backbone, four primary claims × three sets (G2B-E1, E2, O1, P1) | registered | PASS | 6.3, Table 6.2 |
| A7 | Rise at every added reference (G2B-O2) | registered | PASS | 6.3 |
| A8 | Language: same exponent (G2B-P2) | registered | INCONCLUSIVE | 6.3 |
| A9 | Sampling: same exponent (G2B-P3a) | registered | INCONCLUSIVE | 6.3 |
| A10 | Temperature (G2B-P3b) | registered | **FAIL** (UIT-ViIC-231, XM3600-600); INCONCLUSIVE (COCO-295) | 6.3 |
| A11 | Backbone (G2B-P4) | registered | INCONCLUSIVE | 6.3 |
| A12 | Condensed F1 shrinks gold dependence (A-N1) | registered | MIXED | 6.3 |
| A13 | Eight LVLMs: one-reference ranking differs (LBA-P1) | registered | PASS | 6.3 |
| A14 | Eight LVLMs: per-model ladder (LBA-P2) | registered | **FAIL** (COCO-295) | 6.3 |
| A15 | Span-label agreement rises with the gold (AN3-P1) | registered | **FAIL** | 7.2 |
| A16 | Condensed F1 agrees better with span labels (AN3-P2) | registered | INCONCLUSIVE | 7.2 |
| A17 | LongCap-Arena (i): humans penalize count | registered | PASS | 7.1 |
| A18 | LongCap-Arena (ii): count-matched precision tracks humans better | registered | **FAIL** | 7.1 |
| A19 | LongCap-Arena (iii): count-equal pairs agree more | registered | **FAIL** | 7.1 |
| A20 | VaPR mostly, not fully, count-matched | registered | PASS | 7.3 |
| A21 | RLAIF-V chosen-fewer share ≥ 0.60 | registered | **FAIL** | 7.3 |
| A22 | Seed placebo admits the matched prefix (E1 K2) | registered | HELD (calibration only) | 3.3, S3 |
| A23 | Count-matched checkpoint leaderboard, predictions (a)–(c) (N9) | registered | NOT TESTABLE: fidelity check failed | 3.3, S3 |
| A24 | PASCAL-50S: ordering 1 ref < 50 refs < VOC labels (P50-A4) | registered | **FAIL** (1 ref < 50 refs PASS, +37.16 [+35.07, +39.09]; 50 refs < VOC labels FAIL, −2.29 [−5.15, +0.61]) | 6.4 |
| A24a | PASCAL-50S: rise at every registered level, k = 1, 2, 5, 10, 20, 50 (P50-O2) | registered (secondary) | PASS | 6.4 |
| A24b | PASCAL-50S: reference-gold slope below a size-matched random-deletion null (X4) | registered (co-primary in its companion family; secondary to the confirmatory claim) | PASS (one evaluable member; no adjustment) | 6.6 |
| A24c | PASCAL-50S: the same with VOC labels as complete gold (X5) | registered (co-primary in its companion family; secondary to the confirmatory claim) | NOT EVALUABLE | 6.6 |
| A24d | PASCAL-50S: extrapolated precision from five references (X1, X2) | registered as descriptive | no verdict | S7 |
| A25 | Tone-mark normalisation sensitivity (shared instrument check) | registered | no verdict field | S2 |
| P-1 | Leave-one-system-out robustness | post hoc | no verdict | 6.5 |
| P-2 | Verified-precision bracket | post hoc (design fixed before the run) | no verdict | 6.2 |
| P-3 | Re-scoring of 15 published comparisons | post hoc | no verdict | 3.3, S3 |
| P-4 | Cap share of detailed captions | post hoc, descriptive | no verdict | 6.3 |

**What the proposition does not predict.** It does not say where the crossing lies, and the multi-reference sign is not predicted by the theory: predictions of a positive slope with all available references failed in three settings (the two English LVLM families below, where they were pre-specified, and XM3600 with 2–3 references, where they were registered; Section 6.2). On 20 public English LVLM outputs (OPERA and Less-is-More releases, 7 backbones), predictions pre-specified before scoring (file timestamp 2026-10-14 12:43Z, never committed; treated as exploratory) expected a positive slope at five references; the slope stayed negative (−29.57 [−32.69, −26.37] and −22.86 [−26.71, −18.53] in the two families) and became positive only with instance labels. The verdict under the pre-specified rule was FAILED. The pattern is still consistent with (a) and (d): within each family the slope rises monotonically from one to five references and does not cross back. The exponent fitted on short-caption systems did not transport to verbose ones, and the crossing moved to a more complete gold. $M^*$ is a descriptive decomposition with in-sample $b$, not an out-of-regime predictor; the out-of-sample test with $b$ transferred from COCO-2500 is registered for XM3600 (the XM3600 pre-registration, committed to version control at 2026-10-14 16:38Z, before the first XM3600 result at 17:00Z; the registration is valid. All six systems have been scored (Section 6.2): the one-reference and OIV7 sign predictions and the ordering held; the prediction that 2–3 references give a positive slope failed, and with it the sign-agreement check for that gold (1 of 3 out-of-sample sign predictions failed, below the registered demotion threshold of 2)).

**Registration.** The re-scoring protocol was written after a pilot had already scored these 15 comparisons, and it reports that pilot's raw and matched-prefix results. The protocol was committed to version control at 2026-10-14 07:01Z; the pilot's results file was written at 01:48Z the same day. The following were therefore fixed after the pilot results were known:
- the primary endpoint (matched prefix, Holm over the 15 comparisons, a smallest effect size of interest of +1.0);
- the fidelity check, the positive control and the protocol's withdrawal rule.

We do not count these rules, or the numbers in Table S3.1, as registered before their outputs. The sentence tie-average and the uniform random subset were added after the pilot. Only quantities added later that had no output when they were registered count as registered before their outputs, such as the seed placebo, which needed new decoding (Supplementary S3).

**Registered seed placebo: HELD.** The registered placebo compares two sampling seeds of one model on the same images; any control that finds a "gain" there is miscalibrated. The released outputs contain one seed per decoder, so the placebo needed new decoding. It was run on LLaVA-1.5-7B with two sampling seeds on the 500 CHAIR images.
Decision rules for the placebo, registered before any placebo output (in the re-scoring protocol and a later addendum): (i) withdrawal rule: a control with $|\Delta P| > 1.0$ or an interval excluding 0 on the seed placebo is miscalibrated and is dropped from the curve; (ii) selection rule: the primary control is one with $|\Delta P| \le 0.5$ and an interval covering 0 on the placebo; if more than one passes, the matched prefix stays primary. The placebo's prediction held: the matched prefix was admissible and was selected as the primary control. The placebo ran in the checkpoint-leaderboard decoding harness, whose fidelity check failed ($|\Delta\mathrm{CHAIR}_i| = 1.49 > 1.0$), so the placebo result calibrates the control only and is never evidence for any count-control claim.

Registered predictions of the checkpoint leaderboard:
- (a) the median matched-prefix precision gain over the training checkpoints exceeds the mean decoding gain of Table S3.1 (+0.62 points);
- (b) checkpoints trained on preference pairs whose chosen response names fewer objects (HA-DPO, HSA-DPO, SENTINEL; Section 7.3) reduce the mean number of classes per caption by at least 0.3 more than checkpoints trained on near-balanced pairs (POVID, mDPO);
- (c) HALVA, whose training swaps objects without changing their number, changes the mean number of classes per caption by at most 0.15.

Registered consequences: if the checkpoints' base CHAIR is more than 1.0 from the published value, the protocol is fixed before any look; if the sign of the training data's count difference does not order the change in count (difference below 0.1 class), prediction (b) is dropped; if at least half of the checkpoints keep a Holm-significant matched-prefix gain of at least +1.0, the headline becomes "training changes object choice", which still supports count-controlled reporting. If the count-matched ranking equals the raw ranking within the intervals, this paper reports the leaderboard as consistent with the raw ranking and does not rest any claim on it. The leaderboard's fidelity check failed, so the leaderboard was not scored and predictions (a)–(c) could not be tested (Supplementary S3).

**Design.** XM3600 (Thapliyal et al., EMNLP 2022) gives 2–3 Vietnamese references per image and, through Open Images V7, human-verified positive and negative image labels (OIV7). Its images are Open Images images, so pre-training exposure is possible here too. We evaluate six systems on 600 images: Qwen2.5-VL-7B zero-shot and two Vietnamese caption adapters of the same backbone, each with a short and a detailed prompt. The exponent is not refitted: we transfer $b$ from COCO-2500 (0.479 for one reference, 0.549 for the union of the 2–3 references, using the two-reference value, and 0.846 for instance-type labels) and predict the sign of each slope from $M^*_{\text{micro}} = b\,\bar G/(1-b)$ and the XM3600 gold sizes. The predictions, the evaluation code and the hashes of 11 input files were committed to version control at 2026-10-14 16:38Z, before the first XM3600 output existed (17:00Z); the registration is valid.

**Registered predictions** (the XM3600 pre-registration):
- The one-reference sign prediction: slope(one random reference) < 0 across the 6 systems ($M^*_{\text{micro}} = 1.471$ with transferred $b$, which the pre-registration expected to lie below the six systems' median $M$).
- The all-references sign prediction: slope(all references) > 0 ($M^*_{\text{micro}} = 2.859$). The pre-registration marks this as the risky test, because Section 6.1 showed that $b$ can compress on verbose outputs.
- The verified-label sign prediction: slope(OIV7 verified) > 0 ($M^*_{\text{micro}} = 11.216$).
- The ordering prediction: slope(one reference) < slope(all references) < slope(OIV7).
- The sign-agreement check: for each gold variant, sign(slope) = sign($M^*_{\text{mixed}}$ − median $M$).
- Demotion rules: if 2 or more of the three sign predictions above fail, the sign result moves from a core result to an explanatory diagnostic; if the one-reference sign prediction fails, the one-reference prediction has failed in a third setting and the sign-flip claim is dropped.

**Reading.** The sign of the verbosity reward flips between single-reference gold and the OIV7 verified labels, as predicted, and the slopes are ordered by gold completeness, as Proposition 1 requires. The registered prediction that the union of 2–3 references already gives a positive slope failed: on XM3600 the crossing lies at a gold more complete than the available references. The transferred exponent did not locate the crossing; the in-sample exponent for the all-references gold is 0.503, below the transferred 0.549, which repeats the lesson of Section 6.1. The one-reference pass also did not come about through the mechanism the pre-registration gave: the six systems' median $M$ (1.38) lies below the transferred optimum (1.471), not above it. The registered demotion rule states, in paraphrase, that if 2 or more of the 3 out-of-sample sign predictions (the one-reference, all-references and verified-label sign predictions) fail, the sign result is demoted from a core result to an explanatory lemma or diagnostic. One of the three failed, so the demotion rule was not triggered and the sign result stays a core result; the second rule (drop the sign-flip claim if the one-reference sign prediction fails) was not triggered either. What XM3600 supports is the direction and ordering of the sign change, not a prediction of where it occurs.

**Second-backbone test: registered predictions and verdict rules.** These are the predictions and rules as registered before any output of the test existed (Section 6.3). Earlier planning reports framed the test with a different primary endpoint (the paired difference in $b$) and with rules that counted backbones; the registration replaced that framing before any output, and its departures from the plans are listed below.

*Verdict rules.* A claim "> 0" passes if the 95% interval lies above 0, fails if the point estimate is at or below 0, and is inconclusive otherwise; "< 0" mirrors it. An equivalence claim $|x| \le \delta$ passes if the interval lies inside $\pm\delta$, fails if it lies wholly outside, and is inconclusive otherwise; a difference claim $|x| > \delta$ mirrors it. A compound claim fails if any part fails, is not evaluable if any part is, passes if every part passes, and is inconclusive otherwise. Withdrawal rules count failures only; an inconclusive result is never counted as support. No multiplicity correction is applied: every prediction is reported separately, per set, with its interval.

*Primary predictions* (the six-decode ladder of each set; cv295, uv231 and xm600):
- one-reference endpoint: the slope under one random reference is below 0 (the theory does not derive this sign);
- complete-gold endpoint: the slope under the label gold (Section 3.1) is above 0;
- ordering: slope(all references) − slope(one reference) > 0 and slope(label gold) − slope(all references) > 0;
- exponent ordering: $b$(all references) − $b$(one reference) > 0 and $b$(label gold) − $b$(all references) > 0.

The sign of the slope under several references is not predicted; it is reported with its interval only.

*Secondary predictions:*
- the slope rises at every added reference (cv295, uv231);
- language: $|b_{\text{EN}} - b_{\text{VI}}| \le 0.05$ under the label gold (cv295, uv231);
- sampling: the exponent of the vote family is within 0.05 of that of the greedy prompt family (uv231);
- temperature: at both sampling temperatures the exponent is within 0.05 of greedy decoding, and the intercept is lower at the higher temperature (all three sets);
- backbone: the exponent is within 0.05 of the first backbone's, while the intercepts differ by more than 2 precision points at matched $M$ (all three sets).

*Withdrawal and reporting rules.* (i) If the exponent ordering fails on 2 or more of the 3 sets, the completeness account is dropped for this backbone and only "the exponent is dataset-specific" is reported. (ii) If the language prediction fails on both cv295 and uv231, the exponent is reported per language. (iii) If the power-law RMSE exceeds 3 precision points for a gold of a set, the frontier is reported there only as a local linearization. (iv) If the one-reference endpoint fails on any set, the sign-flip claim is dropped and only the ordering can remain. (v) Verdicts use clean subsets only. (vi) A run whose model file, prompt, decoding setting or pinned instrument differs from the registration does not test it. "Replicates on a second backbone" may be written only for cv295 and xm600, and only where the one-reference endpoint, the complete-gold endpoint and the ordering all pass; uv231 failures count against the claim, but a uv231 pass is not counted as support.

*Departures from the planning reports* (registration §12):
- The KTVIC sets of the plans are left out, because KTVIC is reported in the companion manuscript on KTVIC (in preparation; a copy is available to the editor); the sampling pool is therefore decoded on uv231 only, and the plans' two-gold transfer tests are left out for the same reason.
- The English arm is this backbone's greedy short and detailed pair on cv295 and uv231; the plans had English and Vietnamese prompt families for three backbones. xm600 has no English arm, because no English-to-OIV7 class map exists.
- The plans' backbone-count rule (2 or more of 3 backbones) is evaluated in the restricted form (ii) above, because only one backbone has English outputs.
- Clean-subset scoring is applied in every case; the plans made it conditional on a failed language check.
- Every sign and ordering claim, including the plans' $b(\text{instance}) > b(5\text{ refs})$, stated there without an interval, is scored with the three-way rule above.
- The temperature prediction is added from the plans' rationale for the temperature ladder; the plans' own sampling prediction is the vote-family comparison.
- uv231: the plans' premise that its images are uncontaminated does not hold (all are COCO train2017 images), hence the uv231 rule above.

*What the author saw before registering* (registration §13): this paper's Section 6 with the first-backbone slopes on these image sets; the planning reports and earlier decisions; the XM3600 registration and two earlier registrations for this backbone; and a summary of this backbone's zero-shot language-check rates, object scores and mentions per caption on a KTVIC development split (a development file outside this paper; no number from it is used here). By that summary's thresholds the short prompt failed the language check and the detailed prompt passed; because this registration scores clean subsets in every case, no analysis choice depends on that outcome. The operational form of the predictions (families, verdict rules, the temperature and backbone statistics, clean-subset scoring and the uv231 handling) was written after reading that summary, and none of these choices uses a number from it. No caption of this backbone on cv295, uv231 or xm600 existed; while file formats were checked, the first lines of one existing first-backbone COCO caption file were displayed.

**Registration.** The sets differ in how their predictions were fixed, and every result below carries its label:
- *LongCap-Arena, registered.* The pre-registration was committed to version control (2026-10-15 02:50:04Z) and pushed (02:50:10Z) before the first output (05:59:16Z; Section 7.1).
- *THumB and Composite, pre-specified.* The predictions were written and hashed before any statistic involving a human score was computed: pre-specified (file timestamp 2026-10-14 12:52Z, never committed); treated as exploratory.
- *Polaris and DOCCI-Critique, pre-specified, committed late.* The pre-registration file was written at 2026-10-14 15:37Z, before the first results file (16:25Z), but committed at 16:47Z, 22 minutes after it. We therefore treat these two sets as exploratory, although their pre-specified rules are reported as written.

Two human-validity tests on public long-caption judgments were added, each run only after a licence check and a committed pre-registration (the LongCap-Arena pre-registration; the results file was written after the commit). The CapArena test was dropped because no licence statement for its human battles could be found.

*Footnote (run history).* The first run of the pinned analysis script crashed while writing its JSON output after test (ii), because a test result was a numpy boolean that Python's JSON encoder cannot serialize. It was re-run unchanged through a wrapper that only teaches the JSON encoder to write numpy scalars (committed to version control after the re-run); the pinned script's own hash check passed and no statistic, threshold or verdict rule was touched. The crashed run printed no statistic to the console (its log holds only the traceback). Because the script saves its results file after each test, the crashed run had already written the data summary and the test (i) result to that file before failing; the re-run, with the same seed, overwrote it. Both surviving outputs were written after the pre-registration commit was pushed (02:50:10Z): the VaPR count-control results at 02:50:28Z and the reported LongCap-Arena results at 05:59:16Z. The time of the crashed run is not preserved: the re-run overwrote its partial output, and the archived copy of its log carries the time it was archived (06:02:42Z).

**A stated prediction that failed.** Before RLHF-V and RLAIF-V were audited, the planning report, committed to version control before the audit, predicted that RLAIF-V's chosen-fewer share among unmatched pairs would be at least 0.60, and set a conditional withdrawal rule: if the share fell in [0.45, 0.55] *and* the count-matched leaderboard (Supplementary S3) showed no link between the count difference in the training data and the change in count of the trained model, the statement "length control leaves a count channel" would be withdrawn and Table S6.1 kept as description only. The share is 0.514 [0.509, 0.520], inside the withdrawal interval, so the prediction failed and the first half of the withdrawal condition is met. The second half depended on the checkpoint leaderboard (Supplementary S3). The leaderboard's fidelity check failed, so it was not scored and no method output was read; its prediction (b) and the second half of this two-part withdrawal rule therefore could not be evaluated. The statement "length control leaves a count channel" is therefore unresolved: Table S6.1 is descriptive, and its only registered support is the VaPR control.

**Scope of the confirmatory evidence.** The registered evidence on the verbosity sign is the out-of-sample test on XM3600. It confirms the ordering of the slope by gold completeness and its large-gold endpoint (positive under the OIV7 verified labels); two of its five predictions failed, as stated at the end of this paragraph. COCO-5000 shows the same ordering and endpoint (four of four predictions held on COCO-5000), but its predictions were pre-specified on its seed-42 half, COCO-2500 (file timestamp 2026-10-14 07:22Z, never committed), so it is exploratory; the registered second-backbone test is reported in Section 6.3, and the registered large-reference-set test has not been run, because it needs GPU decodes that are out of scope for this paper (Section 6.4). The negative sign at single-reference gold was observed on both datasets, but it is not a prediction of the theory (Supplementary S1). The sign with several references is not predicted by the theory: the prediction of a positive all-references slope failed on XM3600 (registered) and on two English LVLM families (pre-specified, never committed), and COCO-5000's positive five-reference slope is a dataset-specific outcome. The remaining sign evidence is exploratory or failed: the UIT-ViIC results (run before any prediction was written; with the matcher used for Vietnamese the five-reference slope stays negative, −6.28 [−8.31, −4.29]), and the English LVLM test, whose verdict under its pre-specified rule was FAILED. The "sign agreement" with $M^*$ fitted on the same outputs is close to an identity under the power-law frontier and is a goodness-of-fit check, not a prediction. The out-of-sample test with an exponent transferred from COCO is pre-registered (committed to version control at 2026-10-14 16:38Z), before the first XM3600 result (17:00Z); the registration is valid. All six systems have been scored (Section 6.2): the one-reference and OIV7 sign predictions and the ordering held; the prediction that 2–3 references give a positive slope failed, and with it the sign-agreement check for that gold (1 of 3 out-of-sample sign predictions failed, below the registered demotion threshold of 2).

### Tests without a row in another main-text table

**Table S4.1.** Tests without a row in another main-text table.

| Test | Label | Verdict | Section |
|---|---|---|---|
| XM3600 gold sizes | registered | 14 of 15 reproduced | S7 |
| XM3600 adjacency | post hoc | at or below null | 6.2 |
| Large reference sets | planned | not run | 6.4 |
| Re-scoring: fidelity check | post hoc | PASS | S3 |
| Re-scoring: withdrawal rule | post hoc | control-dependent | S3 |
| Re-scoring: positive control | post hoc | FAIL: underpowered, 2 of 8 | S3 |
| Count vs length | pre-specified | FAIL (claim withdrawn) | S3 |
| Checkpoint leaderboard | registered | not scored: fidelity failed | 3.3, S3 |
| LongCap-Arena | registered | MIXED | 7.1 |
| CapArena | not registered | dropped: no licence | 7.1 |
| Polaris-COCO | pre-specified | PASS | S8 |
| DOCCI-Critique | pre-specified | MIXED | S8 |
| VaPR count control | registered | PASS | 7.3 |

## S5 Exchangeability: all corpus and split rows

Under (A1), the pair of references that name a doubleton is a uniformly random pair, so the probability that the two are adjacent in that order is the number of adjacent pairs over the number of pairs,
$$p_{\text{adj}}^{\,0} = \frac{K-1}{\binom{K}{2}} = \frac{4}{10} = 0.40 .$$
The **adjacent-doubleton share** is the observed fraction of doubletons named by adjacent references, pooled over images, with an image-bootstrap interval. The statistic depends on the order chosen. Taking the UIT-ViIC references in the raw order of the annotation array, instead of by annotation id, also gives a value close to the null. Two companion statistics separate the mechanisms that can raise it:

**Table S5.1.** Adjacent-doubleton share (null 0.40 under exchangeability). 95% image-bootstrap intervals.

| Corpus | References | Images | Share [95% CI] | Lag-1 Jaccard excess [95% CI] |
|---|---|---|---|---|
| COCO (Karpathy test), EN | independent crowd workers | 4,867 | 0.407 [0.379, 0.433] | −0.002 [−0.007, +0.004] |
| UIT-ViIC (all splits), VI | independent annotators | 3,842 | 0.384 [0.366, 0.403] | −0.008 [−0.015, −0.002] |
| UIT-ViIC images, COCO EN references | independent crowd workers | 3,850 | 0.406 [0.380, 0.429] | +0.005 [−0.001, +0.011] |
| Flickr30k (Entities chains; Plummer et al., 2015) | independent; file order possibly sorted by length (not traced) | 31,783 | 0.483 [0.478, 0.488] | +0.055 [+0.053, +0.056] |
| UIT-OpenViIC, test-image panel (aggregates only), images with ≥5 refs, first five | not documented | 425 | 0.428 [0.385, 0.470] | +0.002 [−0.014, +0.018] |
| Flickr30k captions, COCO-80 matcher | independent | 31,783 | 0.454 [0.440, 0.466] | — |
| UIT-OpenViIC, test-image panel, images with exactly 5 refs (aggregates only) | — | 251 | 0.461 [0.401, 0.519] | +0.010 [−0.013, +0.029] |
| UIT-OpenViIC, full test split, exactly 5 refs (aggregates only) | — | 1,997 | 0.477 [0.458, 0.498] | — |

- **Flickr30k** is above the null under both object extractors (0.483 with Entities chains, 0.454 with the COCO-80 matcher) and has a positive lag-1 Jaccard excess. Flickr30k's captions come from independent crowd workers, so the excess points to a non-random file order rather than to shared writers; a length ordering of the five captions would produce it, but we did not trace mean caption length by file position, so this cause is not established. The diagnostic flags an ordering artefact, which matters for any first-$k$ analysis but not for random-$k$ analyses.
- **UIT-OpenViIC** is near the null on the panel subset also used as a second caption set in the companion manuscript on KTVIC (in preparation; a copy is available to the editor) (0.428 for the first five of ≥5 references, lag-1 excess +0.002) and moderately above it on the exactly-five subsets (0.461 on 251 panel images; 0.477 on 1,997 full-test images), without a clear lag-1 Jaccard excess where that statistic is available. We do not know OpenViIC's caption-entry protocol in enough detail to explain the difference between subsets. We report these values and draw no conclusion from them beyond this: OpenViIC references should not be assumed fully exchangeable in file order, and random-$k$ subsets should be used with them.
- **UIT-ViIC English references, test split only** (0.541 [0.436, 0.648] on 231 images) are above the null while the train and validation splits (0.415, 0.341) and the pooled value (0.406) are not. With several dozen corpus–split rows in the audit (Supplementary S5), one small-split excursion of this size is not surprising; we treat the pooled value as the estimate.

**The exchangeable baseline.** On COCO both effects are absent, as (A1) predicts. An adjacent pair of references is worth $k_{\text{eff}} = 1.99$ [1.967, 2.020] independent references on COCO-5000; adjacent and non-adjacent pairs give the same gold size ($\Delta\bar G$ +0.002 [−0.003, +0.009]) and exponent ($\Delta b$ −0.001 [−0.005, +0.002]); the five single-slot exponents lie between 0.467 and 0.482, and on COCO-5000 slot 1 differs from the mean of slots 2–5 by +0.003 [−0.007, +0.014]. First-$k$ and random-$k$ one-reference slopes are −4.30 [−5.33, −3.27] and −4.77 [−6.10, −3.54]. No single-writer corpus is tested here.

**Exchangeability of XM3600 references.** Before any GPU run, the adjacency diagnostic of Section 5 was run on the 150 XM3600 images with three Vietnamese references; the pre-registration reports its result, so this check is post hoc, not a registered test. With $K=3$ the exchangeable null is 2/3 (two of the three slot pairs are adjacent). The observed share is 0.533 [0.414, 0.647] (48 of 90 doubletons), at or below the null: no sign of single-writer entry. This row is not in Table 5.1, whose null differs. The XM3600 pre-registration also froze a test of how far count-controlled differences transfer between the Vietnamese and the English reference panels of XM3600; that two-gold analysis (C3-XM-PANEL) and the reference-versus-OIV7 predictions of the same pre-registration (C3-OIV7-1 to -3) are not analysed in this paper; their registered verdicts are listed in Table 1 (rows X-22 to X-25). The XM3600 adjacency check passed, as a post hoc check.

### Further detail for Section 5

#### Diagnostics

For an image with $K = 5$ references in a fixed order, call an object class a *doubleton* if exactly two references name it. The order is the one each release defines:
- COCO-style files (COCO, UIT-ViIC): references ordered by annotation id;
- Flickr30k: the caption-file line order;
- UIT-OpenViIC: the order of the released list.

Under (A1), the pair of references that name a doubleton is a uniformly random pair, so they are adjacent with probability
$$p_{\text{adj}}^{\,0} = \frac{K-1}{\binom{K}{2}} = \frac{4}{10} = 0.40 .$$
The **adjacent-doubleton share** is the observed fraction of doubletons named by adjacent references, pooled over images, with an image-bootstrap interval; it depends on the order chosen (Supplementary S5). Two companion statistics separate the mechanisms that can raise it:

- the **lag-1 Jaccard excess**: mean Jaccard similarity of the object sets of references at lag 1 minus the mean at lags 2–4 (0 under (A1));
- **slot profiles**: mentions per reference and the frontier exponent $b(1)$ computed from each reference slot alone (flat under (A1)).

A writer who types all references of an image in sequence raises both statistics; length-sorted references produce a position gradient; independent writers produce neither.

#### Results across corpora

**Table S5.2.** Adjacent-doubleton share (exchangeable null 0.40; 95% image-bootstrap intervals).

| Corpus | References | Images | Share | Lag-1 Jaccard excess |
|---|---|---|---|---|
| COCO (Karpathy test), EN | independent | 4,867 | 0.407 [0.379, 0.433] | −0.002 [−0.007, +0.004] |
| UIT-ViIC (all splits), VI | independent | 3,842 | 0.384 [0.366, 0.403] | −0.008 [−0.015, −0.002] |
| Flickr30k (Entities chains; Plummer et al., 2015) | independent | 31,783 | 0.483 [0.478, 0.488] | +0.055 [+0.053, +0.056] |
| UIT-OpenViIC panel, first five refs (aggregates) | not documented | 425 | 0.428 [0.385, 0.470] | +0.002 [−0.014, +0.018] |
| UIT-OpenViIC full test, exactly 5 refs (aggregates) | — | 1,997 | 0.477 [0.458, 0.498] | — |

The two independent-annotator caption sets with a documented protocol, COCO and UIT-ViIC, sit at the null in both statistics. Two corpora sit above it.

- **Flickr30k** is above the null under both extractors (0.483 with Entities chains, 0.454 with the COCO-80 matcher) and has a positive lag-1 excess. Its captions come from independent workers, so the excess points to a non-random file order, perhaps by length (we did not trace the cause); it matters for first-$k$ analyses, not random-$k$ ones.
- **UIT-OpenViIC** is near the null on the panel subset (0.428) and moderately above it on the full-test exactly-five subset (0.477; Supplementary S5). Its caption-entry protocol is not documented well enough to explain this, so random-$k$ subsets should be used.

The same check on a single-writer corpus (KTVIC) is reported in the companion manuscript on KTVIC (in preparation; a copy is available to the editor). On XM3600 the adjacency check found no excess (post hoc; Section 6.2).

#### What fails when references are not exchangeable

Dependence among an image's references violates (A1) in two ways, with different consequences.

**Positive dependence shrinks the gold.** Positively associated references cover fewer objects, so $\bar G(k)$ grows more slowly: $k$ captions from one writer act like $k_{\text{eff}} < k$ independent ones, Proposition 1 holds in $k_{\text{eff}}$, and the crossing moves to larger $k$ (Supplementary S1).

**Slot non-stationarity changes the exponent.** If a writer names different kinds of objects in early and later captions, the reference slot matters even at $k = 1$, and first-$k$ and random-$k$ designs give different exponents and slopes.

**The exchangeable baseline.** On COCO both effects are absent: an adjacent pair of references is worth $k_{\text{eff}} = 1.99$ [1.967, 2.020] independent references, and the first-$k$ and random-$k$ one-reference slopes are −4.30 [−5.33, −3.27] and −4.77 [−6.10, −3.54].

**Consequences for reporting.**
1. $k$-reference curves should use random-$k$ subsets, not file order, unless the adjacency statistic is at the null; a one-reference sign from one slot of a non-exchangeable corpus is not a property of the metric.
2. A leave-one-reference-out score on single-writer data measures within-writer consistency, not a human ceiling.
3. Completeness estimators that treat references as independent samples (Chao2, Good–Turing) give within-writer bounds at best on such data; we report none. 
4. Rater-equivalence units (Resnick et al.) are defined only where references come from distinct raters.

## S6 Numbers manifest, exploratory lexicon and data audits

The numbers manifest is provided as a separate file.

**Limits specific to this set.** The COCO-80 matcher sees few objects in long DOCCI paragraphs: a mean of 1.50 classes per paragraph (median 1), against a gold of 1.36 classes per image. Most of what these paragraphs describe is outside the pre-specified vocabulary. A larger noun vocabulary was tried after the fact; it is not in the pre-specification, is exploratory only, and supports no claim in this paper (Supplementary S6 lists it with that label).

**Positive control: length- and style-matched preference data.** VaPR (Wadhawan et al., 2025; arXiv 2510.01700; Apache-2.0) builds hard negatives matched to the chosen response in length and style. The length channel in preference data is prior work (VaPR; HDPO, Fu et al., 2025, arXiv 2411.10436); we claim only the count channel. The prediction, committed before the audit, was that VaPR's count-matched share would exceed that of HA-DPO, HSA-DPO and SENTINEL (pass rule: the lower bound of its 95% Wilson interval above each), without being fully count-matched. The verdict is **PASS**: 0.849 [0.845, 0.853] of VaPR's 25,626 pairs with objects are count-matched, against 0.473 (HA-DPO), 0.692 (HSA-DPO) and 0.349 (SENTINEL); it is not exactly count-matched. A set matched on length and style is thus mostly, but not fully, count-matched. Among VaPR's 15% count-unmatched pairs the chosen response names fewer classes in 0.373 [0.358, 0.388], so in VaPR the residual channel runs the other way (descriptive; not predicted).

**UIT-OpenViIC.** The licence terms we could find record non-commercial research use but no explicit permission for derived per-image panels. We therefore use UIT-OpenViIC only through aggregate statistics (Table 5.1 and Supplementary S5). No OpenViIC caption, n-gram or per-image derived file appears in this paper or its release; every released file is scanned for OpenViIC 8-grams before publication (0 hits required). The UIT-OpenViIC authors confirmed this use in writing.

**UIT-ViIC.** UIT-ViIC (Lam et al., 2020) is used only through aggregate statistics and pointers (image identifiers and file hashes). No UIT-ViIC caption, n-gram or per-image panel appears in this paper or its release, and we have not received written permission from the UIT-ViIC authors.

**KTVIC–OpenViIC overlap.** KTVIC and UIT-OpenViIC draw on a shared image pool and split it independently; the near-duplicate overlap between the KTVIC test images and the OpenViIC training split is documented in the companion manuscript on KTVIC (in preparation; a copy is available to the editor). No model in this paper is trained on OpenViIC, and the overlap does not affect any result here; we disclose it because the OpenViIC panel rows of Table 5.1 are computed on OpenViIC references of these KTVIC test images, and because that panel is used as an independent caption set in the companion manuscript on KTVIC (in preparation; a copy is available to the editor). Any OpenViIC-trained model must not be evaluated on KTVIC test.

**Other overlaps.** Some UIT-ViIC training images are also in the COCO Karpathy test split, including images of the COCO-5000 probe set and of POPE-500; the counts are reported in the companion manuscript on KTVIC (in preparation; a copy is available to the editor). No adapter trained on UIT-ViIC is scored on those sets in this paper.

### Further detail for Section 7.3

If the chosen response of a preference pair tends to name fewer objects, a model trained on the pairs can learn to name fewer objects. We measure this in seven public preference sets, without testing trained models.

**Method.** Both responses are matched to COCO-80 with the CHAIR matcher; $\Delta k$ is the chosen minus the rejected class count, and $\Delta$words likewise. Pairs with no COCO-80 class are dropped; a pair is *count-matched* if $\Delta k = 0$. Among unmatched pairs we report the share where the chosen response names fewer classes (0.5 = no direction), overall and within two words of length.

**Table S6.1.** Object-count imbalance in public preference data (COCO-80 matcher).

| Dataset | Pairs with objects | Count-matched share | Chosen names fewer, among unmatched [95% CI] | Mean $\Delta k$ | Same, pairs with $\lvert\Delta\text{words}\rvert \le 2$ |
|---|---|---|---|---|---|
| POVID | 16,483 | 0.521 | 0.444 [0.433, 0.455] | +0.114 | 0.243 |
| HA-DPO | 5,181 | 0.473 | 0.882 [0.870, 0.894] | −0.691 | 0.854 |
| HSA-DPO | 8,076 | 0.692 | 0.817 [0.801, 0.832] | −0.250 | 0.763 |
| mDPO (VLFeedback) | 9,281 | 0.408 | 0.498 [0.485, 0.511] | −0.103 | 0.551 |
| SENTINEL | 8,600 | 0.349 | 0.897 [0.889, 0.904] | −0.736 | 0.886 |
| RLHF-V | 5,120 | 0.632 | 0.702 [0.681, 0.722] | −0.234 | 0.791 |
| RLAIF-V | 70,029 | 0.590 | 0.514 [0.509, 0.520] | −0.017 | 0.523 |

**Four sets carry a strong count channel.** In HA-DPO, HSA-DPO, SENTINEL and RLHF-V, the chosen response names fewer classes in 70% to 90% of count-unmatched pairs, which are 31% to 65% of all pairs. Length matching does not remove the channel: on pairs within two words the share stays at 0.854, 0.763, 0.886 and 0.791, and $\Delta k$ keeps a negative logistic weight given $\Delta$words (−1.85 to −1.13 per class).

**Three sets do not.** In mDPO and RLAIF-V the share is close to 0.5, and in POVID it is 0.444. Response editing may cause the channel; we do not test this.

**A registered prediction that failed.** A planning report committed before the audit predicted that RLAIF-V's chosen-fewer share would be at least 0.60, with a two-part withdrawal rule: if the share fell in [0.45, 0.55] *and* the count-matched leaderboard (Supplementary S3) showed no link between the training data's count difference and the trained model's change in count, the statement "length control leaves a count channel" would be withdrawn and Table S6.1 kept as description only. The share is 0.514 [0.509, 0.520], inside the kill interval, so the prediction failed and the first half of the rule is met. The second half could not be evaluated, because the leaderboard was not scored (Supplementary S3); the statement is unresolved: Table S6.1 is descriptive, and its only registered support is the VaPR control below.

**Positive control: length- and style-matched preference data.** VaPR (Wadhawan et al., 2025; Apache-2.0) builds hard negatives matched to the chosen response in length and style; the length channel in preference data is prior work (VaPR; HDPO, Fu et al., 2025); we claim only counts. The registered prediction was that VaPR is more count-matched than HA-DPO, HSA-DPO and SENTINEL (lower Wilson bound above each) without being fully count-matched. The verdict is **PASS**: 0.849 [0.845, 0.853] of its 25,626 pairs with objects are count-matched, against 0.473, 0.692 and 0.349; its residual channel is in Supplementary S6.

**What the audit implies, and what it does not.** In four of seven sets, preferring the chosen response means preferring fewer objects in most count-differing pairs, even under length matching. A lower CHAIR after such training may reflect the count channel, better object choice or both; only a count-matched evaluation separates them. The audit does not show that any method's published gain is a count effect; it sees only COCO-80 objects, in released pairs whose labels we did not check.

## S7 Robustness of the verbosity-sign tests

The checks below use 9 systems on COCO-5000: Vietnamese captions of the 5,000 COCO Karpathy-test images from Qwen2.5-VL-7B variants (zero-shot, zero-shot with VCD, distilled, and two fine-tuned adapters, one of them trained with the gold-SFT recipe of Nguyen et al. (2026a); short and detailed prompts), mapped to COCO-80 with a Vietnamese lexicon and scored against the English references and COCO instance labels. Its seed-42 half, COCO-2500, is the discovery set for the sign pattern: the predictions were pre-specified on it before the run (file timestamp 2026-10-14 07:22Z, never committed), so it is treated as exploratory, and the registered tests of the pattern are those of Sections 6.2–6.4. Everything else in this subsection is a post-hoc check of the proposition, labelled as such.

**Part (a), monotone exponent.** On COCO-5000 with random-$k$ subsets, $b(k)$ = 0.475, 0.546, 0.589, 0.617, 0.638 for $k=1..5$, 0.850 with instance labels and 0.869 with instance labels plus references. On COCO images, the two English LVLM release families of Section 6.1 also show $b$ rising from one to five references, from 0.112 to 0.203 and from 0.153 to 0.282.

**Assumption (A2), salience ordering, tested directly.** For each mention we count its reference support $n$ (how many of the 5 references name it) and compare the share of *marginal* mentions (the last mention of each caption) with the share of all mentions at each $n$. Under (A2) the ratio falls with $n$. On COCO-5000 the ratio is 1.82, 1.24, 0.84, 0.48, 0.25 for $n = 1..5$ and is monotone in 100% of bootstrap draws; mentions that are present in the instance labels but named by no reference have ratio 3.16. Marginal mentions are disproportionately objects that writers do not name.

Nor does the first-order, constant-$b$ closed form resolve the one-reference sign.
- **At one reference.** With $\bar G(k) = U(k)$, the closed form evaluated at the family centre $M_0$ sits at the boundary, $\Lambda = 0.014$ [−0.040, 0.066], an interval that includes 0. The observed micro-F1 slope is negative. In 66% of bootstrap replicates $\Lambda_U(1) > 0$ while the one-reference slope is $< 0$, so the $\Lambda = 0$ boundary does not give the one-reference sign.
- **Straddling.** The micro optimum $M^* = 1.24$ lies inside the family's range (median $M$ = 1.21), so the observed one-reference sign rests on systems that straddle the optimum.
- **From two references on.** $\Lambda > 0$ with intervals that exclude 0, and it rises at every step: 0.512 [0.458, 0.562], 0.788, 0.968 and 1.104 [1.046, 1.164] for $k = 2..5$, 2.593 [2.506, 2.681] with instance labels and 2.852 [2.771, 2.941] with instance labels plus references.

The reproduction of the original run agrees to the second decimal on every slope. One sign change, from negative to positive, between one and two references, is what Proposition 1(d) allows and nothing more. The positive five-reference slope holds for this dataset and family only, as an exploratory result; it is a dataset-specific outcome, not a prediction that five references suffice in general.

- **P1 (one reference, slope < 0): held** in both families.
- **P2 (five references, slope > 0): failed** in both families (−29.57 and −22.86, intervals well below 0).
- **P3 (instance gold, slope > 0 with interval above 0): held** for the Less-is-More family (+6.91 [+2.16, +11.17]) and **failed** for the OPERA family, whose interval touches 0 (+4.24 [−0.09, +8.51]).
- **P4 (order) and P6 (rise at every step $k \to k+1$): held** in both families: −35.18, −33.87, −32.49, −30.59, −29.57 and −31.89, −29.48, −27.10, −24.63, −22.86.

UIT-ViIC test (231 COCO sports images, all from COCO train2017, so exposure is possible for any COCO-pretrained backbone; five Vietnamese references written by independent annotators; Section 5) was scored before any prediction was frozen, so every number here is exploratory. Ten Vietnamese systems were scored with two matchers. With the COCO-80 lexicon (the matcher used for English outputs), the slope rises from −13.97 with one random reference to +4.80 with five, whose interval includes 0, and to +37.52 with instance labels (Table 6.1). The paired differences are clear: five references minus the first reference +20.70 [+16.35, +25.00], instance minus five references +32.72 [+28.01, +37.27]. With the Vietnamese reference lexicon, the slope also rises (−17.25, −6.28, +7.66) but stays negative at five references.

We therefore do not claim that the sign flip between one and five references replicates on UIT-ViIC. What UIT-ViIC shows, under both matchers, is the ordering (one reference < five references < instance labels) and a negative one-reference slope; the five-reference sign depends on the matcher, because the two lexicons give different gold sizes and different mention counts (median $M$ 1.39 versus 1.99).

**Registered gold-size checks.** The pre-registration also froze the gold sizes $\bar G$ on the 600 images, because the transferred-$b$ predictions depend on them. Of the 15 registered gold-size values, 14 are reproduced exactly by the evaluation; one is out: the mean one-random-reference gold size over images with a non-empty gold is 1.8768 against a registered 1.8831. We report it as OUT. The transferred $M^*$ in the one-reference sign prediction uses the all-image gold size (1.6000, IN), which this value does not enter.

**Random-deletion null (post hoc; Section 6.3).** For each set and reference level, the observed statistic is the slope of F1 on $\ln M$ scored against the reference gold restricted to label-gold classes; the null replaces that gold by a random subset of the label-gold classes of the same size, 1,000 times, and the range is the null's 95% percentile range. The design was committed before the run, and the check carries no verdict.

**Table S7.1.** Observed slope against the random-deletion null.

| Set | Level | Observed | Null 95% range |
|---|---|---|---|
| COCO-295 (discovery images) | one reference | −14.40 | [−4.50, +4.61] |
| COCO-295 (discovery images) | all references | −6.21 | [+0.01, +9.31] |
| UIT-ViIC-231 (UIT-ViIC test) | one reference | −20.96 | [+10.35, +20.91] |
| UIT-ViIC-231 (UIT-ViIC test) | all references | +1.80 | [+18.10, +26.91] |
| XM3600-600 (second backbone) | one reference | −17.01 | [−10.99, −7.83] |
| XM3600-600 (second backbone) | all references | −16.38 | [−11.15, −8.11] |
| Section 6.2 outputs (first backbone) | one reference | −14.19 | [−9.41, −6.32] |
| Section 6.2 outputs (first backbone) | all references | −12.65 | [−8.64, −5.65] |

**Post hoc bound on the XM3600 label-gold slope (Section 6.2).** The label gold of XM3600 is human-verified labels, scored with verified precision (mentions OIV7 cannot verify are excluded). The bound re-scores the six Section 6.2 systems and the second backbone's XM3600-600 ladder twice, with the registered slope, recall and image bootstrap of each test: once counting every mapped mention that OIV7 cannot verify as an error (lower bound) and once as correct (upper bound). It also reports, per system, the share of mapped mentions OIV7 can verify and the gold size of each level. The design was fixed before the run; the bound is post hoc, carries no verdict and changes no registered verdict. Result for the label-gold slope: it is positive only when unverifiable mentions are excluded; counting them as errors removes the positive slope (post hoc).

**Table S7.2.** Post hoc bound on the label-gold slope of F1 on $\ln M$ (95% intervals; registered = verified precision, as registered).

| Set | Registered | Lower bound (unverifiable = error) | Upper bound (unverifiable = correct) | Set outcome |
|---|---|---|---|---|
| Section 6.2 systems (first backbone, 600 images) | +19.32 [+17.43, +21.13] | +5.83 [+3.82, +7.82] | +20.13 [+18.35, +21.89] | (i) |
| XM3600-600 ladder (second backbone, clean subset of 537 images) | +13.71 [+11.44, +15.79] | +1.97 [−0.44, +4.01] | +14.78 [+12.58, +16.79] | (ii) |

**Table S7.3.** Share of mapped mentions that OIV7 can verify (%, 95% interval), per system, and mean gold size per level.

| Set | System | Verifiable share |
|---|---|---|
| Section 6.2 | zero-shot, short prompt | 64.02 [60.16, 67.79] |
| Section 6.2 | zero-shot, detailed prompt | 43.37 [40.68, 45.92] |
| Section 6.2 | gold-SFT adapter, short prompt | 68.61 [64.27, 72.55] |
| Section 6.2 | gold-SFT adapter, detailed prompt | 69.71 [65.47, 73.77] |
| Section 6.2 | second adapter, short prompt | 64.66 [60.82, 68.55] |
| Section 6.2 | second adapter, detailed prompt | 59.55 [55.86, 63.15] |
| XM3600-600 | greedy, short prompt | 60.65 [56.26, 64.75] |
| XM3600-600 | greedy, detailed prompt | 43.77 [40.93, 46.73] |
| XM3600-600 | lower sampling temperature, short prompt | 61.66 [57.44, 65.55] |
| XM3600-600 | lower sampling temperature, detailed prompt | 43.94 [41.00, 46.62] |
| XM3600-600 | higher sampling temperature, short prompt | 60.85 [56.42, 65.04] |
| XM3600-600 | higher sampling temperature, detailed prompt | 44.61 [41.69, 47.49] |

| Set | One reference | All references | OIV7 verified labels |
|---|---|---|---|
| Section 6.2 | 1.61 | 2.35 | 2.04 |
| XM3600-600 | 1.59 | 2.36 | 2.03 |

Each set's outcome is the one its own lower-bound interval gives; the paper-level outcome is (i) only if both sets give (i), because they are the same images under two backbones, so it is (ii). The OIV7 gold is smaller than the union of the references on both sets, so the label gold is not a superset of the reference gold. The lower-bound point slope was approximately derivable from committed numbers before this design, and neither the design author nor the verifier computed it; the outcome-deciding CI was not derivable.

**Cap share of the second backbone's detailed captions (post hoc; Sections 6.3 and 8.5).** Every second-backbone decode file records, per image, the number of new tokens the decoder generated. A detailed caption counts as reaching the registered 160-token cap when that recorded count is at least 160. Over the nine Vietnamese detailed runs (three sets × three temperatures, every image), 3,367 of 3,378 captions (99.7%) reached the cap. As a check, the saved captions were re-tokenized with the registered tokenizer; a re-tokenized length of at least 158 agrees with the recorded reach on 3,375 of 3,378. A recorded count of 160 also arises when the end-of-sequence token is exactly the 160th token, so the share is an upper bound. The same check on other decodes of this model, which also record a cap flag: in the eight-LVLM test (English detailed prompt), 526 of 526 captions reached the cap and the re-tokenized length agrees on 526 of 526; in other Vietnamese detailed decodes of this model, 787 of 789 reached it and the re-tokenized length agrees on 788 of 789, the one disagreement being a caption with 159 recorded tokens. The design was committed before the count was computed; the count carries no verdict and no causal claim about the model's result in the eight-LVLM test.

**Table S7.4.** Second-backbone detailed captions that reached the 160-token cap, by the recorded token counts, and re-tokenization agreement (re-tokenized length ≥ 158 against the recorded reach).

| Set | Run | Captions | Reached the cap | Agreement |
|---|---|---|---|---|
| COCO-295 (discovery images) | greedy | 295 | 295 | 295 |
| COCO-295 (discovery images) | lower sampling temperature | 295 | 295 | 295 |
| COCO-295 (discovery images) | higher sampling temperature | 295 | 295 | 295 |
| COCO-295 (discovery images) | three runs pooled | 885 | 885 | 885 |
| UIT-ViIC-231 (UIT-ViIC test) | greedy | 231 | 228 | 231 |
| UIT-ViIC-231 (UIT-ViIC test) | lower sampling temperature | 231 | 228 | 229 |
| UIT-ViIC-231 (UIT-ViIC test) | higher sampling temperature | 231 | 227 | 230 |
| UIT-ViIC-231 (UIT-ViIC test) | three runs pooled | 693 | 683 | 690 |
| XM3600-600 (the same 600 XM3600 images) | greedy | 600 | 599 | 600 |
| XM3600-600 (the same 600 XM3600 images) | lower sampling temperature | 600 | 600 | 600 |
| XM3600-600 (the same 600 XM3600 images) | higher sampling temperature | 600 | 600 | 600 |
| XM3600-600 (the same 600 XM3600 images) | three runs pooled | 1,800 | 1,799 | 1,800 |
| All three sets | nine runs pooled | 3,378 | 3,367 | 3,375 |
| COCO-295, English detailed prompt (not pooled) | greedy | 295 | 295 | 295 |
| UIT-ViIC-231, English detailed prompt (not pooled) | greedy | 231 | 231 | 231 |

### PASCAL-50S: full registered output (Section 6.4, 6.6)

All values below are copied from the two decide files; the registered verdicts are in Section 6.4, Section 6.6 and Table 1. Analysis set 997 of 1,000 images (clean in every run); 7 models, 14 runs; 50 references for every image; the VOC label level was kept (no XML missing or unreadable).

**Table S7.P1.** Slope of mixed F1 on $\ln M$ by number of references $k$ (all 14 runs; registered as "no prediction", P50-NS; 95% image-bootstrap intervals).

| $k$ | COCO-80 | V20 |
|---|---|---|
| 1 | −31.38 [−32.70, −29.95] | −27.42 [−29.46, −25.30] |
| 2 | −27.87 [−29.38, −26.35] | −21.78 [−24.15, −19.42] |
| 5 | −20.99 [−22.72, −19.30] | −12.66 [−15.19, −10.15] |
| 10 | −15.07 [−16.84, −13.31] | −5.63 [−8.16, −3.18] |
| 20 | −8.75 [−10.53, −6.96] | +1.49 [−1.01, +3.96] |
| 50 | −0.83 [−2.58, +1.07] | +9.74 [+7.29, +12.12] |
| VOC labels | — | +7.45 [+4.98, +9.94] |

**Per-model slopes (descriptive, no verdict; registered as PAIR_m).** Each model's two runs (short and detailed), slope of mixed F1 on $\ln M$. Each entry is a two-run contrast, not a fit, and the COCO-80 and V20 columns use different vocabularies, so they are not comparable across columns.

| Model | 1 ref, COCO-80 | 50 refs, COCO-80 | VOC labels, V20 |
|---|---|---|---|
| InternVL3-8B | −32.04 | +1.73 | +10.26 |
| LLaVA-1.5-7B | −36.57 | −9.71 | −1.05 |
| LLaVA-OneVision-7B | −42.21 | −2.38 | −0.32 |
| Qwen2.5-VL-3B | −30.25 | +3.44 | +5.77 |
| Qwen2.5-VL-7B | −22.81 | +10.80 | +14.75 |
| Qwen3-VL-8B | −23.91 | +8.93 | +4.57 |
| SmolVLM2-2.2B | −38.10 | −1.73 | +12.38 |

**Family-wise reading (descriptive).** Holm over {P50-A4, P50-O2, X4} (X5 not evaluable; X1 and X2 never enter), next to the registered verdicts, which it does not change: P50-A4 p = 0.939, does not survive; P50-O2 p = 0.001, survives; X4 p = 0.001, survives.

**Extrapolation from five references (X1, X2; registered as descriptive, no verdict).** On the development sets the frozen first-order jackknife did not raise rank agreement, so both statistics were fixed as descriptive before this run; they do not show that the estimator is valid. For each run, precision under five references was extrapolated to the 50-reference consensus and compared with the precision actually measured against all 50 references. Mean absolute error: raw five-reference precision 9.95 points, the pooled-uniform correction 6.46, the gold-size ratio 10.51, the jackknife 4.17. The jackknife minus the better trivial correction is −2.29 [−2.51, −1.99] points (X1). Rank agreement with the 50-reference precision (Kendall τ~b~, 14 runs) is 0.868 raw and 0.956 extrapolated; the difference, +0.088 [−0.022, +0.110] (X2), has an interval that includes 0. Pool-depth extrapolation in information retrieval (Zobel, 1998) estimates how many relevant items exist, and species estimators applied to crowd answer lists (Trushkowsky et al., 2013, per the arXiv preprint 1202.2335) estimate the size of a set; X1 instead extrapolates each run's precision from the incidence of its own mentions across the references already collected, and is checked against the 50-reference consensus, not against a complete gold. No test of the estimator was registered.

**Compute and data handling.** The 8 GPU-hour cap included the 20-image smoke runs; the plan projected 26,787.3 of 28,800 GPU-seconds and left out Idefics3-8B, the first model in the registered drop order. Images, references and raw captions stayed on the scoring machine, and only the aggregate decide files were copied out. Under the registered data rule, each of the 14 caption files shared at least one 8-gram with the PASCAL-50S references, so all were deleted on the scoring machine with the images and references; no hash of them was kept. The registered verdicts can be recomputed only by re-running the registered job from the pinned model snapshots, decoder and code; per-image outputs cannot be audited.

**Table S7.P2.** Number of 8-grams each PASCAL-50S caption file shared with the 50-reference sets (counts only; no caption text was kept or read). By registration a hit is not a verdict input; overlaps can be generic phrases or memorised text.

| Model | Short prompt | Detailed prompt |
|---|---|---|
| InternVL3-8B | 184 | 83 |
| LLaVA-1.5-7B | 353 | 199 |
| LLaVA-OneVision-7B | 346 | 49 |
| Qwen2.5-VL-3B | 138 | 61 |
| Qwen2.5-VL-7B | 51 | 48 |
| Qwen3-VL-8B | 41 | 18 |
| SmolVLM2-2.2B | 419 | 120 |

**Departures from the PASCAL-50S registration.** (a) The registration said that only each hit file's SHA-256 and the aggregates would leave the scoring machine; the job copied a hash only for files without hits, and all 14 files had hits, so no hash of the caption files was kept. (b) Before the registration was committed, the PASCAL-50S reference file was fetched once on a local machine, its hash and size were checked against the pin, and its structure was checked (1,000 keys, 50 references for every image, no text printed or stored); the registration placed all PASCAL-50S data steps on the scoring machine. The rules for each possible structure were fixed before the counts were seen. Neither departure changes a verdict.

### Further detail for Section 6

#### COCO-5000: pre-specified predictions (exploratory)

Four predictions were pre-specified on COCO-2500, the seed-42 half of COCO-5000 (Supplementary S1): they were timestamped three minutes before the first output but never committed, so the test is exploratory. All four held on COCO-2500, and all four hold on COCO-5000 (the full split; post hoc extension): (P1) the slope is ordered, −4.77 < +10.57 < +22.13 (one reference, five references, instance gold); (P2) the instance-gold interval is above 0 ([+21.39, +22.89]); (P3) at one reference $M^*_{\text{micro}} = 1.38$ lies below the largest $M$ (2.18) and the slope is negative; (P4) the slope's sign equals that of $M^*_{\text{mixed}}$ minus the median $M$ for 12 of 12 gold variants, a goodness-of-fit check, since $M^*$ comes from the same outputs. The slope also rises at every step $k \to k+1$ (−4.77, +2.32, +6.26, +8.76, +10.57) and again to instance gold (+22.13). The positive five-reference slope is a dataset-specific outcome, not a prediction that five references suffice (reproduction: Supplementary S7).

#### English LVLM outputs: pre-specified predictions that failed (exploratory)

For the public CHAIR outputs of the two English release families of Supplementary S3, predictions were pre-specified but never committed (exploratory). These systems name more objects (median $M$ 3.13 and 3.03), so the five-reference prediction was the risky one. The one-reference prediction (slope < 0) and the ordering predictions (order; rise at every step) held in both. The five-reference prediction (slope > 0) **failed** in both (−29.57 and −22.86). The instance-gold prediction (slope > 0) held for Less-is-More (+6.91 [+2.16, +11.17]) and **failed** for OPERA (+4.24 [−0.09, +8.51]). The verdict under the pre-specified rule is FAILED.

What failed is the crossing's location, not its direction: the slope rises and never crosses back, but five references do not turn it positive at $M \approx 3$. The in-sample exponent shows why: 0.112 and 0.203 (OPERA) and 0.153 and 0.282 (Less-is-More) with one and five references (0.475 and 0.638 on COCO-5000); an exponent fitted on short-caption systems does not transfer to verbose ones. So under five-reference gold, raw object F1 penalizes the more verbose of two LVLMs; under instance gold it rewards it.

#### UIT-ViIC: exploratory

UIT-ViIC test (231 COCO train2017 images, so exposure is possible for any COCO-pretrained backbone) was scored before any prediction existed (exploratory). Under both matchers the slope is ordered and negative at one reference, but the five-reference sign depends on the matcher (Table 6.1; Supplementary S7), so we do not claim that the one-to-five-reference sign flip replicates here.

**Result.** All four primary claims PASS on each set. They were scored once, after all 23 registered decodes (ladders plus the secondary claims' comparison families) and the abstract's outcome sentences were committed; no withdrawal rule was triggered and no run excluded. On the clean subsets (263 of 295, 209 of 231 and 537 of 600 images, for COCO-295, UIT-ViIC-231 and XM3600-600), the slope of F1 on $\ln M$ is negative under one reference (−11.46 [−17.27, −5.19]; −20.96 [−24.31, −17.40]; −12.27 [−14.55, −10.08]) and positive under label gold, on XM3600-600 under the verified-precision rule whose bound is in Section 6.2 (+13.14 [+7.81, +18.82]; +37.36 [+35.15, +39.41]; +13.71 [+11.44, +15.79]). It rises at each level: all references minus one reference is +12.00 [+7.85, +15.73], +22.75 [+19.70, +25.95] and +5.89 [+4.76, +6.87]; label gold minus all references is +12.60 [+6.91, +18.38], +35.56 [+30.86, +40.18] and +20.10 [+17.39, +23.05]. The same registered statistics on all images (295, 231 and 600) are a registered sensitivity analysis without verdicts; their values are in Table 6.1 (one reference and label gold) and Table S7.5 (every other statistic). Only the reference levels are nested, and their ordering would also arise if objects were missing from references at random; the result supports the pattern, not a particular missingness model (Section 4.2). A post-hoc exploratory check (design committed before the run) replaces each gold by a random subset of the label-gold classes of the same size, 1,000 times. The statistic is the slope scored against the reference gold restricted to label-gold classes; it lies below the 95% range of its random-deletion slopes in all eight cells (COCO-295, UIT-ViIC-231, XM3600-600 and the Section 6.2 outputs, each at one and at all references; Supplementary S7). Which objects annotators name therefore matters beyond how many they name; the check is post hoc and carries no verdict. The secondary claims are weaker: the language and backbone comparisons are INCONCLUSIVE on every set where they are tested, the sampling comparison is INCONCLUSIVE on UIT-ViIC-231, and the temperature comparison is INCONCLUSIVE on COCO-295 and FAILS on UIT-ViIC-231 and XM3600-600.

**Condensed F1 (registered secondary).** Condensed F1 (after the condensed lists of Sakai, 2007), which drops unjudged mentions and scores verified negatives only, shrinks the gold dependence as registered on XM3600-600 (Q, the registered margin of shrinkage, 12.84 [9.86, 14.36], PASS), and on UIT-ViIC-231 (3.82 [2.58, 5.07], PASS), but not on COCO-295 (0.26 [−1.76, 2.11], INCONCLUSIVE). The registered outcome is MIXED: support required a pass on COCO-295 as well.

**Eight public LVLMs (registered secondary).** A further registered test decodes eight public LVLMs in English on COCO-295 (discovery images) and on UIT-ViIC test with English references. Its ranking prediction is PASS on both sets: one-reference F1 does not rank the eight models as complete gold does (tau_b −0.286 [−0.571, 0.000] on COCO-295 and −0.857 [−0.929, −0.500] on UIT-ViIC; PASS if the upper bound is below 0.9, a lenient rule). Its per-model ladder prediction is FAIL on COCO-295: it holds on UIT-ViIC for 8 of 8 models, but on COCO-295 five models pass, LLaVA-OneVision-7B and Idefics3-8B are INCONCLUSIVE, and Qwen3-VL-8B (detailed captions capped at 160 new tokens) fails the complete-gold part (slope −1.124 [−11.52, 6.62]), a FAIL under the registered "point ≤ 0" rule whose interval includes 0. By the registered every-model withdrawal rule, the pattern is therefore not claimed for every public LVLM; Qwen3-VL-8B is the exception on COCO-295. In this test every detailed caption of Qwen3-VL-8B and Idefics3-8B reached the registered 160-token cap on both sets (a registered descriptive; no causal claim); in the second-backbone runs, 3,367 of 3,378 Vietnamese detailed captions (99.7%) reached it (Supplementary S7). The same model's detailed decodes in this harness and in the second-backbone harness agree exactly on only 6.4% (COCO-295) and 6.5% (UIT-ViIC) of images, against 70.5% and 69.7% for short captions.

**Table S7.5.** Second backbone, the registered statistics other than the slopes of Table 6.1. For each set the first column is all images (registered sensitivity, no verdict) and the second is the clean analysis subset on which the verdicts are computed, with its size n and the verdict of that part. Point and 95% image-bootstrap interval. A part verdict is not the verdict of the prediction; the prediction verdicts are listed below the table.

| Statistic (registered id) | COCO-295, all 295 images | COCO-295, clean subset | UIT-ViIC-231, all 231 | UIT-ViIC-231, clean subset | XM3600-600, all 600 | XM3600-600, clean subset |
|---|---|---|---|---|---|---|
| Slope, all references − one reference (G2B-O1) | +12.67 [+8.68, +16.42] | n = 263: +12.00 [+7.85, +15.73], PASS | +23.21 [+20.22, +26.58] | n = 209: +22.75 [+19.70, +25.95], PASS | +5.69 [+4.62, +6.73] | n = 537: +5.89 [+4.76, +6.87], PASS |
| Slope, label gold − all references (G2B-O1) | +12.07 [+6.65, +17.74] | n = 263: +12.60 [+6.91, +18.38], PASS | +36.36 [+31.85, +40.49] | n = 209: +35.56 [+30.86, +40.18], PASS | +21.19 [+18.21, +24.02] | n = 537: +20.10 [+17.39, +23.05], PASS |
| Exponent, b(all references) − b(one reference) (G2B-P1) | +0.109 [+0.056, +0.160] | n = 263: +0.097 [+0.038, +0.151], PASS | +0.231 [+0.197, +0.271] | n = 209: +0.223 [+0.187, +0.260], PASS | +0.067 [+0.049, +0.086] | n = 537: +0.070 [+0.051, +0.087], PASS |
| Exponent, b(label gold) − b(all references) (G2B-P1) | +0.200 [+0.124, +0.275] | n = 263: +0.207 [+0.125, +0.289], PASS | +0.398 [+0.348, +0.443] | n = 209: +0.391 [+0.340, +0.440], PASS | +0.531 [+0.484, +0.583] | n = 537: +0.511 [+0.461, +0.562], PASS |
| Slope rise, one to two references (G2B-O2) | +4.42 [+2.14, +6.49] | n = 263: +3.99 [+1.70, +6.02], PASS | +10.36 [+8.70, +12.20] | n = 209: +10.07 [+8.31, +11.75], PASS | not registered | not registered |
| Slope rise, two to three references (G2B-O2) | +3.92 [+2.72, +5.11] | n = 263: +3.90 [+2.69, +5.18], PASS | +6.54 [+5.41, +7.70] | n = 209: +6.58 [+5.33, +7.86], PASS | not registered | not registered |
| Slope rise, three to four references (G2B-O2) | +2.61 [+1.67, +3.68] | n = 263: +2.51 [+1.43, +3.60], PASS | +4.02 [+3.09, +5.02] | n = 209: +3.74 [+2.75, +4.69], PASS | not registered | not registered |
| Slope rise, four to all references (G2B-O2) | +1.71 [+0.94, +2.49] | n = 263: +1.60 [+0.69, +2.47], PASS | +2.30 [+1.55, +3.06] | n = 209: +2.36 [+1.60, +3.20], PASS | not registered | not registered |
| Language, b(English) − b(Vietnamese), label gold (G2B-P2) | −0.169 [−0.316, −0.031] | n = 281: −0.163 [−0.307, −0.029], INCONCLUSIVE | +0.002 [−0.051, +0.057] | n = 215: +0.004 [−0.046, +0.059], INCONCLUSIVE | not registered | not registered |
| Sampling, b(vote) − b(greedy), label gold (G2B-P3a) | not registered | not registered | +0.043 [−0.001, +0.087] | n = 199: +0.049 [+0.001, +0.097], INCONCLUSIVE | not registered | not registered |
| Temperature, b(T = 0.5) − b(greedy), label gold (G2B-P3b) | +0.043 [−0.037, +0.126] | n = 263: +0.052 [−0.035, +0.142], INCONCLUSIVE | +0.010 [−0.017, +0.039] | n = 209: +0.014 [−0.015, +0.043], PASS | −0.003 [−0.031, +0.020] | n = 537: +0.007 [−0.019, +0.035], PASS |
| Temperature, b(T = 0.8) − b(greedy), label gold (G2B-P3b) | +0.026 [−0.075, +0.124] | n = 263: +0.011 [−0.089, +0.119], INCONCLUSIVE | +0.017 [−0.012, +0.047] | n = 209: +0.020 [−0.013, +0.053], INCONCLUSIVE | −0.028 [−0.061, +0.004] | n = 537: −0.025 [−0.059, +0.008], INCONCLUSIVE |
| Temperature, intercept shift at T = 0.8 (precision points) (G2B-P3b) | −0.05 [−1.63, +1.51] | n = 263: −0.60 [−2.45, +1.31], INCONCLUSIVE | +0.25 [−0.76, +1.13] | n = 209: +0.31 [−0.64, +1.30], FAIL | +0.65 [−0.55, +1.93] | n = 537: +0.42 [−1.03, +1.77], FAIL |
| Backbone, b(Qwen3-VL-8B) − b(Qwen2.5-VL-7B), label gold (G2B-P4) | −0.101 [−0.220, +0.005] | n = 267: −0.104 [−0.220, +0.010], INCONCLUSIVE | +0.052 [+0.014, +0.089] | n = 213: +0.034 [+0.001, +0.068], INCONCLUSIVE | −0.031 [−0.062, −0.001] | n = 530: −0.047 [−0.078, −0.014], INCONCLUSIVE |
| Backbone, intercept difference (precision points) (G2B-P4) | +0.79 [−1.71, +3.04] | n = 267: +0.59 [−1.62, +2.95], INCONCLUSIVE | +2.93 [+1.35, +4.41] | n = 213: +2.30 [+0.92, +3.75], INCONCLUSIVE | −0.85 [−2.48, +0.78] | n = 530: −0.40 [−2.14, +1.32], INCONCLUSIVE |

Prediction verdicts (clean subsets): G2B-O1 and G2B-P1 PASS on COCO-295, UIT-ViIC-231 and XM3600-600; G2B-O2 PASS on COCO-295 and UIT-ViIC-231; G2B-P2 INCONCLUSIVE on COCO-295 and UIT-ViIC-231; G2B-P3a INCONCLUSIVE on UIT-ViIC-231; G2B-P3b INCONCLUSIVE on COCO-295 and FAIL on UIT-ViIC-231 and XM3600-600; G2B-P4 INCONCLUSIVE on COCO-295, UIT-ViIC-231 and XM3600-600.

**Within one prompt and zero-shot only.** Where a subset has at least three systems, the label-gold slope is positive in every subset whose mention counts differ by more than 10%. The one-reference slope is not: among COCO-5000's four short-prompt systems it is +26.52, among its five detailed-prompt systems −12.03, and on XM3600 neither three-system prompt subset keeps its sign when one system is dropped. The second-backbone sets consist of two clusters, short and detailed captions, whose mention counts differ by less than 7% within a cluster, so their robustness to dropping a system says little about the slope within a prompt; we do not interpret their within-prompt slopes.

## S8 Human-validity analysis details

### Material moved from Section 8.3 in revision 1

THumB 1.0 and the Composite set (short COCO captions), Polaris-COCO and DOCCI-Critique (Gordon et al., 2025; 1,398 paragraphs from 14 VLMs on DOCCI images, Onoe et al., 2024) were tested with pre-specified predictions; all are exploratory (tables: Supplementary S8). The count-controlled residual agrees with the THumB and Composite human totals less often than raw −CHAIR (−0.190 [−0.277, −0.108] and −0.083 [−0.101, −0.065]; prediction failed in both), so it is not a better quality score. On short COCO captions humans are close to count-neutral (0.481 [0.429, 0.530] and 0.525 [0.506, 0.544] of count-differing pairs prefer the caption naming more classes), and completing the gold does not make F1 agree better with them (withdrawal rule triggered). On Polaris all three pre-specified predictions held (e.g. full gold minus one reference, +0.0606 [+0.0535, +0.0679]); DOCCI-Critique is MIXED (Supplementary S8).

**Declared design changes.** The release has one caption per image and no system label. The pre-registration therefore fixed three changes from the DOCCI design before any look: (i) is a pooled slope over captions rather than a within-system slope; (ii) compares scores at the caption level (Kendall $\tau_b$ with Relevance) rather than ranking systems, with the count-matched score $z_P$ = raw precision minus the mean raw precision of captions with the same $M$; (iii) compares pairs of captions across images, because no image has two captions.

**Exploratory (not registered).** Two patterns were not predicted and are reported as exploratory. First, gold completeness is the largest single driver of agreement between −CHAIR and human precision on THumB: 0.736 with one reference, 0.797 with four, 0.903 with full gold; against the human total the values are 0.627, 0.714, 0.793 on THumB and 0.743, 0.838, 0.873 on Composite. Second, −CHAIR under full gold agrees with the human total more on count-equal than on count-differing pairs: 0.846 versus 0.773 on THumB and 0.946 versus 0.838 on Composite. Polaris (Supplementary S8) tests both patterns with predictions specified before its analysis (exploratory; see Registration).

- **H-a, gold completeness.** −CHAIR agrees with the overall rating more under full gold than under one reference: +0.0606 [+0.0535, +0.0679] on all pairs and +0.090 [+0.080, +0.101] on count-differing pairs. Agreement rises from 0.920 with one reference to 0.981 with full gold.
- **H-b, count-equal pairs.** Under full gold, agreement is higher on count-equal than on count-differing pairs: +0.025 [+0.016, +0.035]. On clean matched-count CHAIR wins, humans agree in 0.996 of untied pairs; on count-confounded wins (the CHAIR winner also names fewer correct objects) in 0.667 of 108 pairs; the difference is +0.330 [+0.222, +0.437].
- **H-c, count-neutral humans.** The correlation between the number of named classes and the overall rating lies inside the pre-specified band of ±0.10: +0.067 at caption level and +0.063 within images.

**DOCCI-Critique prediction (ii), ranking the 14 VLMs: point estimate passes, interval includes 0.** The prediction was that the count-controlled (matched-prefix) object score ranks the 14 VLMs closer to human factuality than raw object precision does, by at least +0.10 in Kendall's $\tau$. The differences are +0.1538 against micro-averaged raw precision and +0.2198 against macro-averaged raw precision, both above the threshold, so prediction (ii) is labelled HELD (the pre-specified rule has no interval clause), but the image-bootstrap interval [−0.2637, +0.3077] includes 0. (The two comparisons have the same interval because, with 14 systems, every $\Delta\tau$ lies on a lattice of step 2/91 and both bootstrap distributions have their 2.5th and 97.5th percentiles on the same lattice points, although they differ in 1,671 of 2,000 resamples.) With 14 systems, a ranking test of this kind has little power.

### Further detail for Section 7

#### Short COCO captions: THumB and Composite (pre-specified; exploratory)

THumB has 500 images with 5 captions each (four systems and one human caption), 5,000 within-image pairs; the Composite set has 1,996 images and 8,348 pairs. Table S8.1 gives the pre-specified predictions and their outcomes.

**Table S8.1.** Pre-specified predictions, never committed; full gold: instances + references.

| Prediction | THumB (T) | Composite (C) | Outcome |
|---|---|---|---|
| P1a: −CHAIR beats $z$ on human precision | +0.325 [+0.247, +0.398] | +0.097 [+0.079, +0.116] | held ×2 |
| P1b: $z$ beats −CHAIR on human total | −0.190 [−0.277, −0.108] | −0.083 [−0.101, −0.065] | failed ×2 |
| P2a: humans prefer more classes (> 0.5) | 0.481 [0.429, 0.530] | 0.525 [0.506, 0.544] | failed T, held C |
| P2b: F1's longer-caption preference grows with gold (1/4/full refs), nearest humans at full | 0.41, 0.66, 0.83 | 0.54, 0.66, 0.73 | rise held; closeness failed |
| P2c: full-gold F1 beats one-reference F1 on human total | −0.018 [−0.073, +0.038] | −0.006 [−0.022, +0.010] | failed ×2; withdrawal rule triggered |
| P3: real errors cost more than "pseudo" ones: $\beta_{\text{PFP}} - \beta_{\text{FP}}$ | +1.07 [+0.82, +1.32] | +0.68 [+0.54, +0.81] | held T; failed C |
| P4: humans side with CHAIR on clean wins (≥ 0.75), not confounded ones (≤ 0.60) | 0.846; 16 confounded | 0.946; confounded 0.705 [0.645, 0.763] | underpowered T; failed C |
| P5: human captions rank lowest at one reference | — | — | failed |

**The count-controlled residual is not a better quality score.** P1b failed in both sets by a wide margin: the residual $z$ (true positives minus the frontier expectation at the caption's count) agrees with the human total less often than raw −CHAIR.

**Raw precision tracks human precision** (P1a held in both sets). On THumB, human precision falls by 1.16 points per real false positive but not for a mention only one reference omits (P3); on Composite (one crowd rater per item) such mentions cost 41.5% of a real error (P3 failed).

**Humans barely prefer naming more objects; full-gold F1 strongly does.** Humans prefer the caption that names more classes in 0.481 [0.429, 0.530] of count-differing pairs on THumB (P2a failed) and 0.525 [0.506, 0.544] on Composite (held), while F1's preference rises from 0.41 to 0.83 on THumB as the gold is completed (P2b). P2c's withdrawal rule was triggered: completing the gold does not make F1 agree better with human judgments.

**Unpredicted patterns.** Gold completeness is the largest single driver of agreement between −CHAIR and human precision on THumB (0.736 with one reference, 0.903 with full gold), and −CHAIR agrees with humans more on count-equal pairs (Supplementary S8). Polaris tests both.

#### Polaris-COCO: replication at scale (exploratory)

Polaris (Wada et al., 2024) gives overall human ratings; we use its COCO test split (2,286 images, 10,496 within-image pairs). All three pre-specified predictions held and no withdrawal rule was triggered (PASS); as the specification was committed after the first result, this is an exploratory replication.

- **H-a, gold completeness.** −CHAIR agrees with the overall rating more under full gold than under one reference: +0.0606 [+0.0535, +0.0679] on all pairs.
- **H-b, count-equal pairs.** Under full gold, agreement is higher on count-equal than on count-differing pairs: +0.025 [+0.016, +0.035].
- **H-c, count-neutral humans.** The correlation of the number of named classes with the rating lies inside the pre-specified band of ±0.10 (+0.067 at caption level; Supplementary S8).

Polaris thus replicates both patterns at scale, again on short COCO captions.

#### DOCCI-Critique: long paragraphs, mixed result (exploratory)

DOCCI-Critique (Gordon et al., 2025) gives sentence-level factuality ratings for 1,398 paragraphs from 14 VLMs on 100 images, the only long, LVLM-style outputs here. The verdict under the pre-specified rules is **MIXED** (exploratory, for the same reason as Polaris).

**Prediction (i), within-VLM count effect: primary fails.** It required mean and median within-VLM slopes below 0 and a pooled fixed-effects slope with interval below 0. Under the primary measure (sentence-level majority) the mean slope is −0.0127 [−0.0265, +0.0007] and the pooled slope −0.0157 [−0.0286, −0.0024], but the median is +0.000371 (7 of 14 VLMs negative), so the median clause fails; under the secondary measure all three clauses hold (Supplementary S8).

**Prediction (ii), ranking the 14 VLMs: HELD, interval includes 0.** The matched-prefix score ranks the VLMs closer to human factuality than raw precision by +0.1538 (micro) and +0.2198 (macro), above the pre-specified +0.10, so prediction (ii) is labelled HELD, but the interval [−0.2637, +0.3077] includes 0; with 14 systems the test has little power (Supplementary S8).

**Limits specific to this set.** The COCO-80 matcher sees few objects in these paragraphs (mean 1.50 classes, median 1, against a gold of 1.36). A larger noun vocabulary, tried post hoc, supports no claim (Supplementary S6).

## S9 Related work: details moved from Section 2

**Length controls outside captioning.** Outside captioning, Sun et al. (2019) normalize ROUGE F1 by a random system of the same average length, and Napoles et al. (2011) compare compressors at similar compression rates.

**Fazli et al. (2026).** They evaluate on three 7B LVLMs, plus MMStar (Chen et al., 2024). Their evidence is aggregate (CHAIR$_s$ and object recall correlate across model–method configurations, Pearson $r = 0.73$); on our reading, they neither match object count per image nor vary gold completeness.

**Sandhu et al. (2026).** Sandhu et al. (2026) find that a CHAIR reduction persists under fixed token budgets (64 to 128 tokens), a token-budget, not an object-count, control; under default decoding their object recall falls from 0.78 to 0.70.

### Extended related work

**Object hallucination metrics.** CHAIR (Rohrbach et al., 2018) scores the share of mentioned COCO classes absent from a gold built from instance labels and reference captions. It is precision-type: a caption that names fewer objects can lower it without choosing objects better. POPE (Li et al., 2023) replaces free-form scoring with yes/no probing and notes that CHAIR depends on the instruction and the caption length. CCEval (Zhai et al., 2023) balances mean caption length and object count across models through prompting, on means only. AMBER (Wang et al., 2023) reports a coverage score next to its hallucination rate, and THRONE (Kaul et al., 2024) uses class-wise precision, recall and an F0.5-score. ALOHa (Petryk et al., 2024) and OpenCHAIR (Ben-Kish et al., 2024) extend the vocabulary beyond COCO-80, and CAOS (Datta and Sundararaman, 2025) adds out-of-domain objects whose presence an ensemble of LVLMs verifies. Two surveys (Liu et al., 2024; Bai et al., 2024) catalogue these metrics without treating object count as a confound. All of these define what is counted; none fixes the number of mentioned objects per image when two systems are compared. HQM (Yan et al., 2024) assesses the reliability and validity of LVLM hallucination benchmarks themselves. For detailed captions, CompreCap (Lu et al., 2025) evaluates captions against directed scene graphs, DeCapBench (Ye et al., 2025) scores hallucination and comprehensiveness over primitive information units with DCScore, CapProbe (Huang et al., 2026) turns detailed-caption evaluation into dense multiple-choice questions that a language judge answers from the caption alone, and FaithScore (Jing et al., 2024) evaluates hallucinations in free-form LVLM answers at a fine-grained level; HalDec-Bench (Saito et al., 2025) and DetailVerifyBench (Wang et al., 2026) benchmark the detection and localization of hallucinated segments in captions.

**Length and count as confounds.** LeHaCE (Wei et al., 2024), the closest prior work in method, fits a model-specific curve of hallucination against description length and evaluates every model at a uniform length. Our controls instead match the number of mentioned objects per image exactly, with paired intervals and a decomposition, and are applied to other groups' released outputs. SumGD (Min et al., 2025) reports recall next to CHAIR because shorter captions lower it; "Less is More" (Yue et al., 2024) shortens outputs and accepts the recall loss; OPERA (Huang et al., 2024) fixes token budgets, not object counts. Later mentions are less reliable: hallucinated objects concentrate late in a caption (LURE; Zhou et al., 2024a), and image reliance fades during generation (M3ID; Favero et al., 2024); the matched prefix of Section 3.3 relies on this ordering. Closest in aim, Fazli et al. (2026) re-evaluate six inference-time mitigation methods with hallucination, recall and coverage metrics, and conclude that "current evaluation protocols may overestimate progress by rewarding conservative generation". On the training side, Long et al. (2026) find that RL for hallucination learns to say less and build a denser presence/absence gold, and Nguyen et al. (2026b) add an object-coverage term to the reward.

**Thresholds, F-measures and incomplete gold.** Lipton et al. (2014) prove that the F1-optimal decision rule adds an item when its probability of being correct exceeds half the attainable F1. Section 4's sign condition is their result; we cite it. Chen et al. (2015, §4.2) model human caption precision against the number of references with one naming probability per word; our propensity model lets it vary within an image. In extreme multi-label learning with missing labels, Jain et al. (2016) propose propensity-scored losses and metrics that counter the bias toward head labels; F-measures are estimable from positive–unlabeled data only under the selected-completely-at-random (SCAR) assumption (Saunders and Freitas, 2022). Our b-channel is the part of the verbosity effect that SCAR missingness cannot produce. Incidence-based species accumulation and rarefaction (Colwell et al., 2012; Chao et al., 2014) supply our expected-gold-size curve $U(k)$.

**Pool bias in information retrieval.** Gold completeness is the captioning counterpart of a known problem in information retrieval. Incomplete relevance judgments bias evaluation measures (Buckley and Voorhees, 2004), pooled judgments raise the question of how reliable large-scale results are (Zobel, 1998), and recall-oriented measures vary with pool depth (Lu et al., 2016). Pooling also disadvantages runs whose documents were left out of the judged pool (Büttcher et al., 2007). Proposed remedies estimate average precision from incomplete and imperfect judgments (Yilmaz and Aslam, 2006), correct the score of an unpooled run by the bias seen on topics where every run is fully judged (Webber and Park, 2009), or compute measures on condensed lists from which unjudged documents are removed (Sakai, 2007); compared under heavily reduced judgments, the condensed-list metrics proved more robust than bpref (Sakai and Kando, 2008). Our setting differs in three ways. (a) A retrieval run is scored to a depth the protocol fixes, whereas a captioner chooses how many objects it names ($M$), so completeness acts through verbosity. (b) What reference gold misses depends on an object's salience within the image, not only on which systems formed a pool; this is the b-channel (Section 4). (c) The gold sets the sign of F1's verbosity slope, not only the size of the bias (Section 6). Condensed F1 carries the IR correction over to captions; its registered test is mixed (Section 6.3).

**Gold quality and rater equivalence.** Making the gold more complete changes model rankings in ImageNet ReaL (Beyer et al., 2020), and RePOPE (Neuhaus and Hein, 2025) revisits POPE's labels. In detection, LVIS (Gupta et al., 2019) builds non-exhaustive labels into the protocol; COCO-ReM (Singh et al., 2024) refines COCO's instance masks and finds that models predicting sharper masks score higher, while Penquitt et al. (2026) find many missing objects but largely stable rankings. For captions, more complete gold can reverse the direction of the verbosity slope (Section 6). Rater equivalence (Resnick et al., 2021) presupposes independent raters; Section 5 shows a caption dataset whose references are not independent.

**Caption evaluation against human judgments.** THumB 1.0 (Kasai et al., 2022; expert ratings), the Composite set (Aditya et al., 2015; crowd ratings), Polaris (Wada et al., 2024; 550 evaluators) and DOCCI-Critique (Gordon et al., 2025; sentence-level factuality of long paragraphs) provide human judgments of captions. Berger et al. (2025) survey caption-evaluation metrics and their validity. We use these sets only to test what object metrics agree with, not to propose a learned metric. For long captions, CapArena (Cheng et al., 2025; over 6,000 pairwise battles) and LongCap-Arena (Matsuda et al., 2025) collect human judgments, and CAPability (Liu et al., 2025) and CapMAS (Lee et al., 2025) score precision and coverage separately; none matches the number of mentioned objects between the captions compared. In text RLHF, length is an established channel (Singhal et al., 2024; Dubois et al., 2024; Park et al., 2024). VaPR (Wadhawan et al., 2025) builds length- and style-matched hard negatives for LVLM preference data; Section 7.3 measures the object-count channel, which length matching need not remove.

**Vietnamese captioning data.** UIT-ViIC (Lam et al., 2020) provides Vietnamese captions by independent annotators for COCO sports images; KTVIC (Pham et al., 2024) has one annotator enter all five captions of an image; UIT-OpenViIC (Bui et al., 2026) is used here only through aggregate statistics (Section 9).

**Reporting standards.** sacreBLEU (Post, 2018) and SacreEOS (Hu et al., 2023) made metric conventions reportable; our two-column reporting proposal likewise changes no metric but fixes what is reported next to it.

