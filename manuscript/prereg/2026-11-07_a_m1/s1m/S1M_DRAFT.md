<!-- INTERNAL HEADER (strip before transfer to the paper repo)
Draft S1.M v1, written 2026-11-07 (date -u). Plan: manuscript/prereg/2026-11-07_a_m1/A_M1_PLAN_v3.md (12d6ad3d, 8d31ed8), §3 and §10.
Run: data/results/a_m1/a_m1_result.json (5687a66b, commit a245481), status BOUND_ONLY (CC-288 GO 88).
Status: DRAFT, not judged, not applied, not committed. Paper repo untouched. Next: S1.M read, one judge at 85, plus Codex read-only (plan J9).
Notation at transfer (plan §0): the paper writes k for the number of references per image (here k = 5) and r < k for a subset size;
frequency counts are phi_j (no clash with the paper's Q_i). Pairs, not objects: "nameable (image, class) pairs".
Items closed at the S1.M read, round 1 (CC-289; internal):
- J7 (Remark 4): CLOSED BY OMISSION (CC-289 Ruling 4). Remark 4 is not printed in SPIC; the internal block below END SUPPLEMENT TEXT
  is stripped at transfer.
- CC-285 N4 (HARD-DUE): CLOSED by CC-289 check 8. The inequality is credited to Chao (1987); the exact incidence form with (k-1)/k and
  its phi_2 = 0 branch is credited to Chao and Colwell (2017, Eq. 2b). Chao 1987 is never credited with the factor.
- CC-285 N5 (HARD-DUE): CLOSED by CC-289 check 9. No extrapolation-range guidance is attributed to any source.
- Citations not yet in paperA.bib: Chao 1987 (Biometrics, 10.2307/2531532), Chao and Colwell 2017 (SORT 41(1), 3-54,
  10.2436/20.8080.02.49), Luggen et al. 2019 (10.1007/978-3-030-30793-6_26). Records verified CC-289.
Wording checked against plan §10.2 and CC-288 MAY NOT: no banned word, no AI mention, no data-overlap wording.
-->

<!-- BEGIN SUPPLEMENT TEXT -->

## S1.M How much a five-reference gold leaves unnamed: a lower bound from the references alone

This subsection states and proves the bound reported in Section 5.4 and Supplementary S5. It uses the references only; no system output and no label enters it, except in the labelled arm and the check against labels (S5).

### S1.M.1 Setting

**Pairs and incidence.** Images are $i = 1,\dots,n$, each with the same number $k$ of references ($k = 5$ here). $V$ is the set of matched object classes (COCO-80). Reference $j$ of image $i$ names the class set $R_{ij} \subseteq V$ after matching. For a pair $(i, c)$ let $Y_{ic} = \sum_j 1[c \in R_{ij}]$, the number of references that name $c$. The pooled frequency counts are $\varphi_m = \#\{(i,c): Y_{ic} = m\}$, $m = 1,\dots,k$, and $U = \sum_{m \ge 1} \varphi_m$ is the number of pairs named at least once: the size of the $k$-reference union gold, summed over images.

**Assumptions.**
- (A1) Given image $i$, its $k$ references are independent draws from one law $P_i$ on subsets of $V$ (the exchangeability assumption of Section 4.1). Classes within one reference may depend on each other in any way. For a pair, $w_{ic} = P_i(c \in R)$ is the probability that one reference names $c$.
- (A2) Given the images, the references of different images are independent.
- (A3) Every image has the same $k \ge 2$, and at most $|V|$ classes.
- (A4) $\liminf_n \frac1n \mathbb E\,\varphi_2 > 0$.

No homogeneity of $w$ is assumed, across classes or across images.

**Estimand.** A pair is *nameable* if $w_{ic} > 0$. Let $S = \#\{(i,c): w_{ic} > 0\}$ be the number of nameable pairs, $f_0 = S - U$ the nameable pairs that no reference names, $C_k = U/S$ the coverage of the $k$-reference gold, and $m_k = 1 - C_k$ its missing share. These are quantities in matched-class space: a class the matcher extracts from a random reference with positive probability is nameable, including matcher errors; restricting the pairs to labelled classes removes those (S5, labelled arm).

**Estimator.** Pooled over all (image, class) pairs of a set,
$$\hat f_0 = \frac{k-1}{k}\,\frac{\varphi_1^2}{2\varphi_2}\ (\varphi_2 > 0), \qquad \hat f_0 = \frac{k-1}{k}\,\frac{\varphi_1(\varphi_1-1)}{2}\ (\varphi_2 = 0),$$
the incidence form of the Chao2 estimator (Chao, 1987; in this form, Chao and Colwell, 2017, Eq. 2b), and $\hat S = U + \hat f_0$, $\hat C_k = U/\hat S$, $\hat m_k = 1 - \hat C_k$. The estimator is never applied per image, and per-image values are never summed (S1.M.4).

### S1.M.2 Lemma 1 (an expectation bound)

Under (A1) and (A3), with sums over the pairs with $w > 0$,
$$\mathbb E\, f_0 = \sum (1-w)^k \;\ge\; \frac{k-1}{k}\,\frac{(\mathbb E\,\varphi_1)^2}{2\,\mathbb E\,\varphi_2}\qquad\text{whenever } \mathbb E\,\varphi_2 > 0 .$$
For $k \ge 3$, equality holds if and only if $w$ is constant over the pairs with $0 < w < 1$; pairs with $w = 1$ contribute to neither side.

*Proof.* Under (A1) the $k$ indicators $1[c \in R_{ij}]$ of a pair are independent Bernoulli($w_{ic}$), so $Y_{ic}$ is Binomial($k, w_{ic}$). Expectations are linear over pairs, so dependence between classes inside one reference does not enter:
$$\mathbb E\,\varphi_1 = k \sum w(1-w)^{k-1}, \qquad \mathbb E\,\varphi_2 = \binom{k}{2} \sum w^2 (1-w)^{k-2}, \qquad \mathbb E\, f_0 = \sum (1-w)^k .$$
Put $a = (1-w)^{k/2}$ and $b = w(1-w)^{k/2-1}$. Then $\sum ab = \mathbb E\,\varphi_1/k$, $\sum a^2 = \mathbb E\, f_0$ and $\sum b^2 = 2\,\mathbb E\,\varphi_2/(k(k-1))$. The Cauchy–Schwarz inequality $(\sum ab)^2 \le \sum a^2 \sum b^2$ rearranges to the claim. Equality holds if and only if $a \propto b$ over the pairs where either is non-zero, that is, if and only if $(1-w)/w$ is constant there. For $k \ge 3$ a pair with $w = 1$ has $a = b = 0$. $\square$

The bound is Chao's (Chao, 1987; see Chao and Colwell, 2017, Section 2.2); nothing in it is claimed as new. The only adaptation is pooling over (image, class) pairs that share one $k$.

### S1.M.3 Proposition 2 (an asymptotic lower bound)

Under (A1)–(A4), conditional on the images (so $w$ and $S$ are fixed), as $n \to \infty$,
$$\limsup_n \frac{\hat f_0 - f_0}{n} \le 0 \quad\text{almost surely.}$$
Hence $\limsup_n (\hat S - S)/n \le 0$; if $S/n$ stays bounded away from 0, $\liminf_n (\hat C_k - C_k) \ge 0$ and $\liminf_n (m_k - \hat m_k) \ge 0$.

**Reading.** $\hat S$ is an asymptotic lower bound on the number of nameable pairs, $\hat C_k$ an asymptotic upper bound on the coverage of the $k$-reference gold, and $\hat m_k$ an asymptotic lower bound on its missing share, all under (A1).

*Proof.* Write $g(x, y) = \frac{k-1}{k}\,\frac{x^2}{2y}$ and decompose into three brackets, (i) to (iii) from left to right,
$$\frac{\hat f_0 - f_0}{n} = \Big[g\big(\tfrac{\varphi_1}{n}, \tfrac{\varphi_2}{n}\big) - g\big(\tfrac{\mathbb E\varphi_1}{n}, \tfrac{\mathbb E\varphi_2}{n}\big)\Big] + \Big[g\big(\tfrac{\mathbb E\varphi_1}{n}, \tfrac{\mathbb E\varphi_2}{n}\big) - \tfrac{\mathbb E f_0}{n}\Big] + \Big[\tfrac{\mathbb E f_0}{n} - \tfrac{f_0}{n}\Big].$$
Each of $\varphi_1, \varphi_2, f_0$ is a sum over images of per-image counts bounded by $|V|$, independent across images by (A2). By Kolmogorov's strong law for independent summands with bounded variances, $(\varphi_1, \varphi_2, f_0)/n$ minus its mean tends to 0 almost surely. No limit of the means is assumed. The means lie in $[0, |V|]$, and by (A4) the mean of $\varphi_2/n$ is eventually at least some $\varepsilon > 0$. The function $g$ is uniformly continuous on $[0, |V|] \times [\varepsilon/2, |V|]$, so bracket (i) tends to 0 almost surely; the $\varphi_2 = 0$ branch is eventually not used. Bracket (ii) is at most 0 by Lemma 1. Bracket (iii) tends to 0 almost surely. The statements for $\hat S$, $\hat C_k$ and $\hat m_k$ follow because $U$ is common to both sides and $\hat S \ge U$. $\square$

### S1.M.4 Remark 3 (pairs no writer names are not identified)

Pairs with $w_{ic} = 0$ are not identified by any function of the references: the law of $(R_{i1},\dots,R_{ik})$ is the same whether such pairs are counted or not. *Proof.* $w_{ic} = 0$ means $c \notin R_{ij}$ almost surely for every $j$, so adding or removing the pair leaves the distribution of every observable unchanged. $\square$

### S1.M.5 The r-to-k check (a pre-specified development check)

For a subset $A$ of $r < k$ reference positions, $\varphi_m^A$ and $U_A$ are computed from the references in $A$ only. The incidence extrapolation (Chao et al., 2014, Table 2)
$$\hat U_A(k) = U_A + \hat f_0^A\Big[1 - \Big(1 - \frac{\varphi_1^A}{r\,\hat f_0^A + \varphi_1^A}\Big)^{k-r}\Big], \qquad \hat f_0^A = \hat f_0 \text{ computed from } A \text{ with } r \text{ in place of } k,$$
is averaged over all $\binom{k}{r}$ subsets. With $\bar U_r$ the mean of $U_A$ (the exact rarefaction mean under (A1)), the observed gain is $G = U - \bar U_r$ and the relative gain error is $\varepsilon_r = (\overline{\hat U_A(k)} - U)/G$. The check was fixed before the run with $r = 3$ and a tolerance of $\pm 0.25$ on $\varepsilon_3$. It is a pre-specified development check, not a blind test (the disclosure is in S5), and its result, with $\varepsilon_2$ and $\varepsilon_4$ beside $\varepsilon_3$, is in S5. It tests the near-range tail of the incidence model only. It is not evidence for the bound of Proposition 2: a law under which each nameable pair is named by at most one reference leaves $\varepsilon_r \approx 0$ while it inflates $\hat S$.

### S1.M.6 What these results do not guarantee

- A finite-sample bound. The plug-in ratio has a bias of order $1/n$ of either sign; at $n = 231$ the bound is approximate at this sample size.
- Any per-image version, or a sum of per-image values: with one to five pairs per image the asymptotics do not apply.
- Anything without (A1). Writers who see each other's references and avoid each other's objects (negative dependence) can void Lemma 1. So can a fixed panel of writers with unequal naming probabilities: then the $k$ indicators of a pair are independent but not identically distributed, and for one pair the Chao2 expectation ratio $\frac{k-1}{2k}\,e_1(x)^2/e_2(x)$, with $x_j = p_j/(1-p_j)$ and $e_m$ the elementary symmetric polynomials, is at least 1 by Newton's inequality, which pushes $\hat f_0$ upward for that pair; pooled over pairs, the net direction is not established. On UIT-ViIC, whose references were written by a panel of five writers, (A1) is a modelling assumption and is not checked.
- Tightness. The gap $S - \hat S$ grows with the heterogeneity of $w$ and is not estimable.
- Classes no writer would name (Remark 3).
- Interval width when the same writers serve many images: the intervals resample images and may then be too narrow.
- Anything about a benchmark other than the development sets used here, or about cause.

<!-- END SUPPLEMENT TEXT -->

<!-- FOR THE S1.M READ ONLY (plan J7): Remark 4 is NOT for print until this read verifies it.
Remark 4 (extendible exchangeability; proof sketch). If the k indicators of each pair are a mixture of i.i.d. Bernoulli(W) with a random
W (de Finetti), then E phi_m = C(k,m) E[W^m (1-W)^(k-m)], and Lemma 1 follows by Cauchy-Schwarz over the joint law of (pair, W), with
E f_0 = sum E(1-W)^k. Positive dependence of mixture type therefore keeps the bound; dependence that cannot be extended breaks it.
Finite-panel caveat (plan B1(c)): a permuted fixed panel of five writers with unequal laws is exchangeable but is not such a mixture
(Newton's inequality gives a per-pair ratio > 1, a mixture gives <= 1), so Remark 4 gives no support for UIT-ViIC. -->
