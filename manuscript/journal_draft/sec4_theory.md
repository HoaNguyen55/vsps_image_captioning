# 4 Theory: the gold-indexed frontier and the sign of the verbosity reward

This section explains why the same metric can reward and penalize verbosity depending on the gold, and states the conditions under which the change of sign happens at most once. The sign condition itself is due to Lipton et al. (2014); the propensity model extends Chen et al. (2015, §4.2). We state the new parts as a proposition with a proof sketch (full proof in Appendix A) and test each part on fixed system outputs. The proposition is a sufficient-condition result under assumptions (A1)–(A3); (A2) is tested directly, and (A1) is shown to fail on one dataset (Section 5).

## 4.1 A propensity model of reference gold

Let object $o$ present in image $i$ have a *naming propensity* $\pi_o \in [0,1]$: the probability that one reference writer names it. Unlike Chen et al. (2015, §4.2), who use one naming probability per word and ignore image-level salience, $\pi$ varies within an image (salient objects are named by almost every writer, background objects rarely).

**(A1) Exchangeable references.** The $K$ references of an image are exchangeable and conditionally independent given the image.

Under (A1), an object enters the $k$-reference gold with probability
$$c_k(\pi) = 1-(1-\pi)^k,$$
and the expected gold size $\bar G(k) = U(k) = \sum_o \mathbb E\,c_k(\pi_o)$ is the incidence-based species-accumulation curve (Colwell et al., 2012; Chao et al., 2014). Instance gold corresponds to $c_\infty = 1$ for every present object, including objects that no writer would name.

Consider a family of systems that differ in how many objects they mention, $M$. The $m$-th mention is a nameable present object with probability $s_m$ (otherwise it is hallucinated, or present but outside what any writer would name), and its propensity has law $F_m$. Then
$$\mathrm{TP}_k(M) = \sum_{m\le M} s_m\, g_k(m),\qquad g_k(m) = \mathbb E_{F_m}\big[c_k(\pi)\big].$$

**(A2) Salience ordering.** $F_m$ decreases in $m$ in the likelihood-ratio order: later mentions have stochastically lower propensity.

**(A3) Shared frontier.** The systems of a family share $s_m$ and $F_m$. They need not produce nested captions; they need only sit on one frontier.

Define the local frontier exponent $b_k(M) = d\ln \mathrm{TP}_k / d\ln M$. It equals the ratio of the marginal precision of the $M$-th mention to the average precision, $b_k = p_{\text{marg}}/P$.

## 4.2 Proposition

**Proposition 1.** Under (A1)–(A3):

(a) **Monotone exponent.** $b_k(M)$ is nondecreasing in $k$. Its limits are
$$b_1(M) = \frac{M s_M\,\mathbb E_{F_M}[\pi]}{\sum_{m\le M} s_m\,\mathbb E_{F_m}[\pi]},\qquad b_\infty(M) = \frac{M s_M}{\sum_{m\le M} s_m} =: 1-D,$$
where $D$ is the part of the exponent deficit that comes from the system alone.

(b) **Concave gold growth.** $\bar G(k)$ is increasing and concave in $k$.

(c) **Sign condition** (Lipton et al., 2014, arXiv v2, Thm. 1 and Cor. 1; cited, not new). Micro-F1, $F_1^\mu = 2\,\mathrm{TP}/(M+\bar G)$, increases with $M$ if and only if $p_{\text{marg}} > F_1^\mu/2$, equivalently
$$\frac{b_k}{1-b_k} > \frac{M}{\bar G(k)}.$$
With constant $b$, $F_1^\mu$ has a unique maximum at $M^*(k) = b_k\,\bar G(k)/(1-b_k)$.

(d) **Single crossing.** Let
$$\Lambda_k(M) = \operatorname{logit} b_k(M) + \ln \bar G(k) - \ln M .$$
$\Lambda_k(M)$ is nondecreasing in $k$. Hence, at a fixed family centre $M_0$, the sign of micro-F1's verbosity reward, $\operatorname{sign}\Lambda_k(M_0)$, changes at most once as references are added, and only from negative to positive; $M^*(k)$ is nondecreasing in $k$.

**Two channels.** The increase of $\Lambda_k$ has two parts: the *b-channel* $\Delta\operatorname{logit} b_k$, which exists only because later mentions are less likely to be named (salience-dependent missingness), and the *$\bar G$-channel* $\Delta\ln\bar G(k)$, which exists under any missingness. If gold objects were missing completely at random (the SCAR assumption of positive–unlabeled learning), $b_k$ would not depend on $k$ and the b-channel would be zero: observed $M^*$ would only rescale with the label frequency. A uniform PU-style correction therefore cannot remove the part of the flip carried by the b-channel.

**Closed form.** With deterministic salience $\pi_m = \pi_1 m^{-\theta}$ and $s_m \propto m^{-D}$,
$$b_k(M) \approx 1 - D - \theta\,\varphi_k(\pi_M),\qquad \varphi_k(\pi) = \frac{k\pi(1-\pi)^{k-1}}{1-(1-\pi)^k},$$
where $\varphi_k$ is the elasticity of $c_k$ ($\varphi_1 = 1$, $\varphi_k \to 0$ as $k\to\infty$). Then $\theta = b_\infty - b_1$ is the reference-incompleteness part of the exponent deficit and $D$ the system part.

## 4.3 Proof sketch

(a) Write $1/b_k = \sum_{m\le M} \frac{s_m}{M s_M}\cdot\frac{g_k(m)}{g_k(M)}$. With $x = (1-\pi)^k$, $\frac{d}{dk}\ln c_k(\pi) = h(x)/k$ where $h(x) = -x\ln x/(1-x)$, and $h$ is increasing on $(0,1)$ because $h'(x)$ has the sign of $x - 1 - \ln x \ge 0$. Hence $c_{k'}(\pi)/c_k(\pi)$ is decreasing in $\pi$ for $k' > k$: the kernel $c_k(\pi)$ is reverse-rule of order 2 in $(k,\pi)$. Under (A2), for $m < M$ the symmetrized double integral over $x<y$ of $[c_{k'}(x)c_k(y) - c_k(x)c_{k'}(y)]\,[f_M(x)f_m(y) - f_M(y)f_m(x)]$ is nonnegative by the basic composition formula for totally positive kernels (Karlin, 1968, *Total Positivity*, Vol. I) [UNVERIFIED: bibliographic entry and section number not checked against a primary page (book has no DOI/Crossref record); the step itself was re-derived and checked numerically, `.session_backup/2026-10-15/paperA_keys/karlin_check.py`], so $g_k(m)/g_k(M)$ is nonincreasing in $k$ and $1/b_k$ falls. As $k\to\infty$, $c_k(\pi)\to 1$ for $\pi > 0$, which gives $b_\infty$.
(b) Each $c_k(\pi)$ is increasing and concave in $k$; expectations and sums preserve both.
(c) $d\ln F_1^\mu/d\ln M = b - M/(M+\bar G)$, which is positive iff $b/(1-b) > M/\bar G$; at $M^*$ the second derivative is $-b(1-b)/M^{*2} < 0$.
(d) $\operatorname{logit} b_k$ is nondecreasing in $k$ by (a), and $\ln\bar G(k)$ is increasing by (b); their sum is nondecreasing, so it crosses 0 at most once and only upward.

All steps were checked numerically on a grid ($k = 1,\dots,10$; RR2 of $c_k$, of a lag-1 dependent kernel and of the 5-reference kernel) in `h4_check.py`<!-- src: .session_backup/2026-10-14/r12/H4/scripts/h4_check.py (self-check T1); output .session_backup/2026-10-14/r12/H4/out/h4_check.json -->. Lipton et al. theorem numbering checked against arXiv 1402.1892v2 (Theorem 1, Corollary 1; numbering in the LNCS version not checked). The composition step was re-derived: with rows $(k',k)$ of the RR2 kernel $c$ and columns $(M,m)$ of the RR2 family $f$ under (A2), the basic composition formula gives $g_{k'}(M)g_k(m) - g_{k'}(m)g_k(M) \ge 0$.

**Under (A1), the subset design does not matter.** Every $k$-subset design (first-$k$, random-$k$, fixed slots) has the same expected $b(k)$, $\bar G(k)$ and slope. A difference between designs is therefore a test of (A1) (Section 5).

## 4.4 Which F1

The closed form in (c)–(d) is exact for micro-F1. The mixed F1 of Section 3.1 (micro precision, image-averaged recall) has the sign condition $P\,d > R\,(1-b)$, where $d$ is the exponent of recall in $M$ ($d < b$; e.g. 0.425 vs 0.478 on COCO with one reference)<!-- src: .session_backup/2026-10-14/r11_verify/c1_b1_b6_reproduction.json :: B1_L1_mstar_and_stopping.check_coco_gold.refs1_firstk.d_recall, .b -->. Image-averaged recall lowers the optimum $M^*$ and makes the one-reference penalty more robust. Every table in Section 7 reports both F1 variants, and we never apply the micro closed form to mixed F1.

## 4.5 Checks on fixed outputs

The checks below use 9 systems on COCO-2500: Vietnamese captions of 2,500 COCO images from Qwen2.5-VL-7B variants (zero-shot, zero-shot with VCD, distilled, and two fine-tuned adapters; short and detailed prompts), mapped to COCO-80 with a Vietnamese lexicon and scored against the English references and COCO instance labels<!-- src: .session_backup/2026-10-14/r12/H4/out/h4_check.json :: coco2500.systems, coco2500.n_img; TODO: confirm the lexicon name (score_coco_probe.vi_objects) and the mention range M 0.84-2.14 (c1 JSON check_coco_gold.*.M_range) --> COCO-2500 is the confirmatory set for the sign pattern: its predictions were frozen before the run (`check_coco_PREDICTIONS.txt`)<!-- src: .session_backup/2026-10-14/r11_litmaps/L1/check_coco_PREDICTIONS.txt -->. Everything else in this subsection is a post-hoc check of the proposition, labelled as such.

**Part (a), monotone exponent.** On COCO-2500 with random-$k$ subsets, $b(k)$ = 0.479, 0.549, 0.592, 0.620, 0.643 for $k=1..5$, 0.846 with instance labels and 0.867 with instance labels plus references<!-- src: .session_backup/2026-10-14/r11_verify/c1_b1_b6_reproduction.json :: B1_L1_mstar_and_stopping.check_coco_gold.{refs1..refs5}_randk.b, inst.b, inst+refs5.b -->. The same monotone pattern holds on the Vietnamese motivating case (companion paper). On UIT-ViIC test (231 images, 6 transfer systems), with the Vietnamese reference lexicon and first-$k$ subsets, $b(k)$ = 0.445, 0.498, 0.522, 0.538, 0.535 for $k=1..5$: one dip of −0.003 between four and five references, inside the five-reference interval [0.491, 0.587]; with random-$k$ subsets the same lexicon gives no dip (0.436 … 0.535), and with the COCO-80 lexicon $b$ rises without a dip from 0.354 to 0.551 and reaches 0.943 with instance labels<!-- src: .session_backup/2026-10-14/r11_verify/c2_n1_uitviic_mstar_v2.json :: uitviic_test.lexicons.{vi_objects_in,coco80}.gold_variants.{refs1..refs5}_{firstk,randk}.groups.transfer_6.b, coco80.gold_variants.inst_only.groups.transfer_6.b; CI: .session_backup/2026-10-13/r10_cpu/g2_g3_mt9_verification_v3.json :: g2c_loo_and_jackknife.UIT-ViIC/refs-lex.b_ols_ci_image_boot -->. The instance-gold value uses the COCO-80 lexicon and is not on the same scale as the reference-lexicon values.

**Assumption (A2), salience ordering, tested directly.** For each mention we count its reference support $n$ (how many of the 5 references name it) and compare the share of *marginal* mentions (the last mention of each caption) with the share of all mentions at each $n$. Under (A2) the ratio falls with $n$. On COCO-2500 the ratio is 1.86, 1.25, 0.80, 0.48, 0.26 for $n = 1..5$ and is monotone in 100% of bootstrap draws; mentions that are present in the instance labels but named by no reference have ratio 3.20<!-- src: .session_backup/2026-10-14/r12/H4/out/h4_check.json :: coco2500.T2_profile.n1..n5.ratio_r, n0_inst.ratio_r, coco2500.T2_share_draws_r_monotone_n1to5 -->. Marginal mentions are disproportionately objects that writers do not name.

**Part (d), single crossing.** On COCO-2500 the F1-on-$\ln M$ slope (mixed F1) is −4.28, +2.82, +6.69, +9.16, +11.08 for $k = 1..5$, +22.41 with instance labels and +24.16 with instance labels plus references<!-- src: .session_backup/2026-10-14/r11_verify/c1_b1_b6_reproduction.json :: check_coco_gold.{refs1..refs5}_randk.slope, inst.slope, inst+refs5.slope -->: one sign change, from negative to positive, and the slope rises monotonically with completeness. With micro-F1 the pattern is the same (−1.84 [−3.14, −0.55] at $k=1$, then +5.78, +9.96, +12.71, +14.69)<!-- src: .session_backup/2026-10-14/r12/H4/out/h4_check.json :: coco2500.T2_microF1_randk.{1..5}.slope, .1.slope_ci -->, but at $k=1$ the micro optimum $M^* = 1.26$ lies inside the family's range (median $M$ = 1.19)<!-- src: same :: coco2500.T2_microF1_randk.1.Mstar_micro, coco2500.median_M -->, so the one-reference sign rests on systems that straddle the optimum.

**Channel split.** Between one and five references, the b-channel carries 68% of the increase in $\Lambda$ on COCO-2500 and 74% from one reference to instance labels<!-- src: .session_backup/2026-10-14/r12/H4/out/h4_check.json :: T4.coco_randk.b_channel_share, T4.coco_refs1_to_inst.b_channel_share -->. Most of the flip therefore comes from salience-dependent missingness, which a uniform (SCAR) correction for missing gold cannot remove.

**Closed form.** Fitting $b_k = 1 - D - \theta\varphi_k(\pi_M)$ to the five random-$k$ points gives root-mean-square error 0.0019 with $D = 0.333$ on COCO-2500<!-- src: same :: T5_closed_form.coco_free_D.rmse, .D -->. Forcing $D$ to the instance-plus-references value fits worse (0.0127)<!-- src: same :: T5_closed_form.coco_D_from_inst+refs.rmse -->. Read as a [MODEL] extrapolation, the reference limit $b_\infty$ is near 0.67, about 0.20 below the instance-plus-reference value: the share of present objects that caption writers do not name, which more references cannot recover. This extrapolation rests on two parameters fitted to four points; Appendix A gives the fit, and a large-$k$ test (nocaps, PASCAL-50S) is planned (TODO: B3 on the second machine, after a licence check).

**What the proposition does not predict.** It does not say where the crossing lies. On 20 public English LVLM outputs (OPERA and Less-is-More releases, 7 backbones), predictions frozen before scoring expected a positive slope at five references; the slope stayed negative (−29.57 [−32.69, −26.37] and −22.86 [−26.71, −18.53] in the two families) and became positive only with instance labels<!-- src: .session_backup/2026-10-14/r12/H3/out/n1_results.json :: families.F-B.gold.refs5_randk.slope/_ci, families.F-C.gold.refs5_randk.slope/_ci; frozen file .session_backup/2026-10-14/r12/H3/N1_PREDICTIONS.txt -->. The registered verdict was FAILED. The pattern is still consistent with (a) and (d): within each family the slope rises monotonically from one to five references and does not cross back<!-- src: same :: families.F-B.gold.refs{1..5}_randk.slope -->. The exponent fitted on short-caption systems did not transport to verbose ones, and the crossing moved to a more complete gold. $M^*$ is a descriptive decomposition with in-sample $b$, not an out-of-regime predictor; the out-of-sample test with $b$ transferred from COCO-2500 is frozen for XM3600 (`manuscript/prereg/2026-10-14_xm3600_predictions.json`, pre-registered in commit 4ccbee3 (2026-10-14 23:38 +07), before the first XM3600 result (00:29 +07); the registration is valid. Results not yet reviewed or used; TODO).
