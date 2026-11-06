<!-- INTERNAL HEADER (strip before transfer to the paper repo)
Draft v2, 2026-11-06 (v1 2026-11-05, unchanged). Step 4 of manuscript/directions/A_UPGRADE_PLAN_2026-11-04.md. Proofs for the new §4.3
(manuscript/reviews/A_THEORY_DRAFT_2026-11-06_v2.md). Target: a new subsection of Supplementary S1.
Status: DRAFT, not judged, not applied, not committed. Paper repo untouched. Assumption checks D1-D5 run once on development data (CC-274 GO 88; data/results/a_dchecks/dchecks_result.json 63cabfa3, commit 1f157d2): D1 PASS, D2 PASS, D3 PASS (COCO-5000 and XM3600 only; UIT-ViIC not testable; no T2 credit, plan l.109), D4a FAIL, D4b FAIL (D4: simulated references, not gold), D5 DESCRIPTIVE (reading (c) for the 14 ALLOWED pairs only).
R0, word count of the §4.3 paper text (BEGIN/END markers, HTML comments removed, `wc -w`, LaTeX tokens included): 633 (rev 4.2, after the D3/D5 sentences and the N.4(c) wording; v2: 560; v1: 508).
Main-text cap 8,500 words (PI-1105k). The sec4 text it joins is 694 words today (paper repo, wc -w).
Sources read: plan §2 (all), paper sec3_measurement_setup.md §3.1, sec4_theory.md, sec7_verbosity_sign.md §6.6,
supplementary_SPIC.md:86 (CHAIR is not 1 - P), PHD_PAPER_RUBRIC_2026-11-04.md T2, and the code that computes X4/X5:
scripts/pascal50s/p50x.py (sha256 3f562e878ed7) null_slopes/salience, scripts/pascal50s/p50.py (2387ca05ae8a) draw/N_REP,
scripts/g2b/score_g2b.py (66c665c7a71d) rows/scores/stat_slope, scripts/a_t3/a_t3.py (57507e0917a7) l.544-549.
Notation map to plan §2.1: plan n_i -> l_i, k_i -> q_i, R_i -> Q_i, N -> n, G (null) -> G-tilde.

v2 change table (from v1 A_SUPP_S1_PROOFS_DRAFT_2026-11-05.md, 1e572150, unchanged), after CC-263 (NEXT_ROUND 78):
| Item | Where | v2 change |
|---|---|---|
| B3 | S1.N.4 Prop. N.4(c), "What this means", S1.N.7 | "exact under H0^nest" -> "valid only under H0^nest, which real references do not satisfy"; editorial "should not be printed" note removed; "proved for the linear class" -> "variance ordering proved for the class of (b); conservatism follows under approximate normality"; J = 1 "exact" -> "valid under H0" |
| B4(i) | Thm N.5(c) instance CHAIR | conditions added: nested multisets a^S <= a^{S+1} and t_S > 0; with t_S < 0 the equivalence can flip (check_v2 E1) |
| B4(ii) | Thm N.5(c) caption CHAIR | sufficient condition corrected: per-image condition on covered images AND newly covered images (M_i^S = 0) with new-mention excess <= 0; CC-263 counterexample stated (check_v2 E2) |
| B5 | S1.N.1, Cor. N.1, Thm N.3, S1.N.6 row 2, S1.N.7 | "label gold" -> "complete gold" (label gold where labels exist; X4 union of all references) |
| B1, B2 | main text only | see A_THEORY_DRAFT_2026-11-06_v2.md |
| N1 | throughout | results numbered S1.N-locally (Lemma N.1 ... Remark N.2; paper's Proposition 1 untouched); totals T_S -> tau_S; Sum q_i K -> q_+; recall coefficients beta_ic -> eta_ic; linear constant kappa^S -> f^S_0 (kappa kept for draw weights) |
| N3 | Prop. N.4(c), Remark N.2 | "heuristic expectation"/"heuristic" -> "conjecture" |
| N4 | Prop. N.4(b) | caption-level CHAIR added to the covered class |
| N8 | Remark N.1 | one-clause disclosure: registered rule's size exceeds 0.025 by at most 0.001; rules agree at the §6.6 p-value floor |
| N5, N6, N7 | - | not in this draft: bib fields and HLP §2.17 check before transfer (N5); D1-D5 rules frozen at step 5 (N6); strip/scan/word cap at transfer (N7) |
| N2 | paper sec4, §6.6 | companion edit at transfer, listed in the main-text v2 header |
-->

<!-- BEGIN SUPPLEMENT TEXT -->

## S1.N The size-matched deletion null: statements and proofs

This subsection proves the three results of Section 4.3. Everything is conditional on the systems scored, their captions and the matcher, as are all slopes in this paper.

### S1.N.1 Setting

**Images and golds.** Images are $i = 1,\dots,n$. The complete gold $C_i$ (the label gold where labels exist; for X4 the union of all references) has $\ell_i$ classes. The gold under test is the reference gold restricted to $C_i$, $Q_i = G_i \cap C_i$, with $q_i = |Q_i|$ classes and keep-rate $\rho_i = q_i/\ell_i$ ($\rho_i = 0$ when $\ell_i = 0$). On COCO val2017 (X5) $C_i$ is the instance labels; on PASCAL-50S (X4) it is the union of all references; on XM3600 the OIV7 labels are not a superset of the references, so $Q_i$ is always the intersection. Let $n_+ = |\{i : q_i > 0\}|$. Write $Z_{ic} = 1[c \in Q_i]$ for $c \in C_i$.

**Systems.** Systems $S \in \mathcal S$ ($|\mathcal S| \ge 2$, at least two distinct $x^S$). For $c \in C_i$, $h^S_{ic} = 1[c \in \hat O^S_i]$, and $a^S_{ic}$ is the number of times $S$ mentions $c$ (instance count). $M^S_i = |\hat O^S_i|$ counts every mentioned class, including those outside $C_i$; $A^S_i$ counts every mention with repeats. All of these are fixed: they depend on the captions and on $C_i$, never on $Q_i$. Throughout, $n_+ > 0$ and $\sum_i M^S_i > 0$ for every system (otherwise recall or precision is undefined). **Scope.** The theory covers metrics scored against a reference gold $Q_i$. The XM3600 verified precision of Section 6.2 involves no reference gold; its denominator counts only the mapped mentions that OIV7 marks present or absent, so it is outside this subsection's scope. On XM3600 the results apply to reference-gold scoring with $Q_i$ = references ∩ labels and the precision defined below.

**Metrics as functions of $Z$.**

| Metric | Value at indicators $Z$ |
|---|---|
| precision | $P^S(Z) = \sum_i\sum_c h^S_{ic} Z_{ic} \,/\, \sum_i M^S_i$ |
| recall | $R^S(Z) = \frac{1}{n_+}\sum_{i:\,q_i>0} \sum_c h^S_{ic} Z_{ic} / q_i$ |
| micro-F1 | $F^{\mu,S}(Z) = 2\sum_i\sum_c h^S_{ic} Z_{ic} \,/\, (\sum_i M^S_i + \sum_i q_i)$ |
| CHAIR$_i$ (instance) | $1 - \sum_i\sum_c a^S_{ic} Z_{ic} \,/\, \sum_i A^S_i$ |
| CHAIR (caption level, Section 7) | $\frac1n \sum_{i:\,M^S_i>0} \big(1 - \sum_c h^S_{ic} Z_{ic}/M^S_i\big)$ |
| mixed F1 | $F^S(Z) = g\big(P^S(Z), R^S(Z)\big)$, $g(p,r) = 2pr/(p+r)$, $g(0,0) = 0$ |

A metric is **linear** if $f^S(Z) = f^S_0 + \sum_i\sum_c y^S_{ic} Z_{ic}$ with $f^S_0, y^S$ fixed. The first five rows are linear: the sizes $q_i$ enter the recall and micro-F1 denominators, and a size-matched gold keeps them fixed. Mixed F1 is not linear.

**Slope.** $x^S = \ln M^S$ and $\beta(f) = \sum_S \lambda_S f^S$ with $\lambda_S = (x^S - \bar x)/\sum_{S'}(x^{S'} - \bar x)^2$, the OLS slope over systems (printed ×100). Any slope whose weights depend on $x$ only is covered in the same way.

**The null $\mathcal N$.** $\tilde G_i$ is a uniformly random $q_i$-subset of $C_i$, independent across images and of the captions; $\tilde Z_{ic} = 1[c \in \tilde G_i]$.

**The registered statistic.** X4 and X5 average the mixed-F1 score over $J = 20$ random reference draws $Q^{(1)},\dots,Q^{(J)}$, each with its own sizes $q^{(j)}_i$. A null replicate draws one uniform permutation of $C_i$ per image and lets draw $j$ keep its first $q^{(j)}_i$ classes. The statistic is $T = \sum_S \lambda_S \frac1J\sum_j F^S(Q^{(j)})$. The p-value is $(1 + \#\{b: T_b \le T_0\})/(B+1)$ with $B = 1{,}000$, and PASS is $T_0$ below the linearly interpolated 2.5th percentile of the $T_b$.<!-- src: scripts/pascal50s/p50x.py (sha256 3f562e878ed7) :: null_slopes, salience (p_one_sided, PASS rule); scripts/pascal50s/p50.py (sha256 2387ca05ae8a) :: N_REP = 20, draw(); scripts/g2b/score_g2b.py (sha256 66c665c7a71d) :: scores (mixed F1, mean over subsets), stat_slope; scripts/a_t3/a_t3.py (sha256 57507e0917a7) :: l.544-549 (same salience() for X5 and X4 on COCO val2017) -->

### S1.N.2 A lemma on random subsets

**Lemma N.1.** (If $\ell = 1$, every covariance below is zero.) Let $A, B$ be random subsets of a set $C$ of size $\ell \ge 2$ with fixed sizes $k_1, k_2$. Suppose the joint law of $(A, B)$ is invariant under permutations of $C$, and let $m = |A \cap B|$. Then $P(c \in A) = k_1/\ell$, and for any $u, v \in \mathbb R^C$
$$\operatorname{Cov}\Big(\sum_c u_c 1[c\in A],\ \sum_c v_c 1[c \in B]\Big) = \frac{\ell\,\mathbb E m - k_1 k_2}{\ell(\ell-1)} \sum_c (u_c - \bar u)(v_c - \bar v).$$
With $A = B$ uniform of size $k$ this is the sampling-without-replacement variance $\frac{k(\ell-k)}{\ell(\ell-1)}\sum_c (u_c - \bar u)^2$.

*Proof.* Invariance gives $P(c \in A) = k_1/\ell$ and $P(c \in A, c \in B) = \mathbb E m/\ell$. Since $\sum_{c, c'} 1[c\in A]1[c' \in B] = k_1 k_2$ and the diagonal contributes $m$, invariance also gives $P(c \in A, c' \in B) = (k_1k_2 - \mathbb E m)/(\ell(\ell-1))$ for $c \ne c'$. With $\Sigma_{uv} = \sum_c u_c v_c$ and totals $u_+ = \sum_c u_c$, $v_+ = \sum_c v_c$,
$\operatorname{Cov} = \Sigma_{uv}\big(\tfrac{\mathbb E m}{\ell} - \tfrac{k_1k_2}{\ell^2}\big) + (u_+v_+ - \Sigma_{uv})\big(\tfrac{k_1k_2 - \mathbb E m}{\ell(\ell-1)} - \tfrac{k_1k_2}{\ell^2}\big) = \tfrac{\ell \mathbb E m - k_1k_2}{\ell^2(\ell-1)}\,(\ell\,\Sigma_{uv} - u_+v_+)$, and $\ell\Sigma_{uv} - u_+v_+ = \ell\sum_c (u_c - \bar u)(v_c - \bar v)$. $\square$

### S1.N.3 Result 1: the null mean

**Theorem N.1.** For every linear metric $f$ and system $S$, $\mathbb E_{\mathcal N}[f^S(\tilde Z)] = f^S(\rho)$, where $\rho$ puts $\rho_i$ in every entry of image $i$, and $\mathbb E_{\mathcal N}[\beta(f)] = \beta\big(f(\rho)\big)$. Only the marginal probabilities $P(c \in \tilde G_i) = \rho_i$ are used.

*Proof.* $f^S$ and $\beta$ are affine in $\tilde Z$ with fixed coefficients; take expectations and use Lemma N.1. $\square$

**Corollary N.1.** Under $\mathcal N$:
- $\mathbb E R^S = \frac1{n_+}\sum_{i:\,q_i>0} |\hat O^S_i \cap C_i|/\ell_i$: recall is unbiased for complete-gold recall over the images with a non-empty reference gold;
- $\mathbb E P^S = \sum_i \rho_i\,\mathrm{TP}^S_i(C) / \sum_i M^S_i$: complete-gold precision with image $i$ weighted by its keep-rate, so the null can reorder systems only through these weights;
- if $\rho_i \equiv \rho$, then $\mathbb E P^S = \rho\,P^S(C)$ and $\mathbb E\beta(P) = \rho\,\beta(P(C))$ (pure rescaling), while recall is unchanged. Micro-F1 is not a rescaling even then: its denominator holds $\sum_i q_i$ rather than $\sum_i \ell_i$. The constant-rate case is close to results stated for sparse annotation in two 2026 preprints (cf. Shulman, 2026; Chen, 2026)<!-- cite: to verify; Shulman abstract read only -->, and is not claimed as new.

**Proposition N.2 (mixed F1: first order only).** Fix $S$ and one draw, and let $p = \mathbb E_{\mathcal N}P^S$, $r = \mathbb E_{\mathcal N}R^S$ (closed form by Theorem N.1), with $p + r > 0$. Let $U = rP^S - pR^S$ and $V = P^S + R^S - p - r$, so $\mathbb E U = \mathbb E V = 0$. Then:

(a) exactly, $\gamma^S := g(p, r) - \mathbb E_{\mathcal N} F^S = \dfrac{2}{(p+r)^2}\,\mathbb E\Big[\dfrac{U^2}{P^S + R^S}\Big] \ge 0$ (with $0/0 = 0$), so the plug-in value is never below the null mean;

(b) $\gamma^S \le \dfrac{4\operatorname{Var} U}{(p+r)^3} + \dfrac{4\max(p,r)\,\operatorname{sd}(U)\operatorname{sd}(V)}{(p+r)^3}$ and $\gamma^S \le \dfrac{2\max(p,r)\operatorname{sd}(U)}{(p+r)^2}$. $\operatorname{Var}U$ and $\operatorname{Var}V$ are closed-form sums over images by Lemma N.1, with per-class coefficients $r\,\alpha_{ic} - p\,\eta_{ic}$ and $\alpha_{ic} + \eta_{ic}$, where $\alpha, \eta$ are the precision and recall coefficients. The covariance of $P$ and $R$ therefore enters through $U$, not only their two variances;

(c) if $\ell_i \le \bar\ell$, $\sum_i M^S_i \ge c_1 n$, $n_+ \ge c_2 n$ and $p + r \ge c_0 > 0$ (constants free of $n$; the bounds in (b) divide by powers of $p+r$), every coefficient is $O(1/n)$, so $\operatorname{Var}U, \operatorname{Var}V = O(1/n)$ and $\gamma^S = O(1/n)$. The second-order (delta-method) term is $2\operatorname{Var}U/(p+r)^3$;

(d) for the slope, $\mathbb E_{\mathcal N}\beta(F) = \beta\big(g(p,r)\big) - \beta(\gamma)$, and $|\beta(\gamma)| \le \tfrac12(\max_S\gamma^S - \min_S\gamma^S)\sum_S|\lambda_S|$. Here $\sum_S |\lambda_S| = \sum_S|x^S - \bar x| / \sum_S (x^S - \bar x)^2$ is large when the systems' $\ln M$ spread is narrow. With $J$ draws, average over draws.

*Proof.* (a) $g$ is positively homogeneous of degree 1, so $\nabla g(p,r)\cdot(p,r) = g(p,r)$ (Euler), with $\nabla g(p,r) = \big(2r^2, 2p^2\big)/(p+r)^2$. Direct algebra gives
$\nabla g(p,r)\cdot(P,R) - g(P,R) = \dfrac{2\big[(r^2P + p^2R)(P+R) - PR(p+r)^2\big]}{(p+r)^2(P+R)} = \dfrac{2(rP - pR)^2}{(p+r)^2(P+R)}$.
Take expectations and use $\mathbb E[\nabla g(p,r)\cdot(P,R)] = \nabla g(p,r)\cdot(p,r) = g(p,r)$. Nonnegativity also follows from Jensen's inequality, since $g$ is concave: its Hessian is $-\frac{4}{(p+r)^3}(r,-p)^{\top}(r,-p)$.
(b) $|U| \le \max(p,r)(P+R)$ because $-pR \le U \le rP$. Hence $U^2/(P+R) \le \max(p,r)|U|$, which with Cauchy–Schwarz gives the second bound. For the first, split on $E = \{P + R \ge (p+r)/2\}$. On $E$, $U^2/(P+R) \le 2U^2/(p+r)$. On $E^c$, use $\max(p,r)|U|$ together with $\mathbb E[|U|1_{E^c}] \le \operatorname{sd}(U)\,P(E^c)^{1/2}$ and Chebyshev's $P(E^c) \le 4\operatorname{Var}V/(p+r)^2$.
(c) Under the null the images are independent, so the variances are sums of the per-image terms of Lemma N.1, each $O(\bar\ell/n^2)$.
(d) $\beta(\gamma) = \sum_S \lambda_S(\gamma^S - m)$ for any constant $m$, because $\sum_S\lambda_S = 0$; take $m$ at the midrange. $\square$

Proposition N.2 concerns the null mean only. The printed X4/X5 null means are Monte Carlo means of mixed F1 and do not depend on it. It says how well the closed form of Theorem N.1 approximates them; check D1 measures that on development data. D1 passed there: for the four linear metrics the closed-form null mean matched the Monte Carlo mean (largest $|z|$ 1.96 over 280 tests, against the Bonferroni bound 3.75), and the mixed-F1 plug-in stayed within its one-sided bound, with a largest slope error of 0.045 points; instance CHAIR omitted (class-set matchers). First order remains a usable approximation, and the printed X4/X5 values remain Monte Carlo means.

### S1.N.4 Result 2: validity of the randomisation test

**Theorem N.3 (standard; Besag and Clifford, 1989; Phipson and Smyth, 2010)**<!-- cite: to verify; neither is in paperA.bib -->. Let $\mathcal F$ be the complete golds, the sizes $q_i$ and the captions. Suppose
$H_0$: given $\mathcal F$, the $Q_i$ are independent across images and each is uniform over the $q_i$-subsets of $C_i$.
Let $T$ be any statistic, $T_0 = T(Q)$, and $T_1,\dots,T_B$ independent null replicates given $\mathcal F$. Then $(T_0,\dots,T_B)$ is exchangeable given $\mathcal F$, and $p = (1 + \#\{b: T_b \le T_0\})/(B+1)$ satisfies $P(p \le \alpha \mid \mathcal F) \le \alpha$ for every $\alpha \in [0,1]$.

*Proof.* Under $H_0$, $Q$ and $\tilde G_b$ have the same conditional law, so the $T$'s are i.i.d. given $\mathcal F$. Let $m = \lfloor \alpha(B+1)\rfloor$. Then $p \le \alpha$ iff at most $m - 1$ of the other $B$ values are $\le T_0$. At most $m$ indices $j \in \{0,\dots,B\}$ can have this property, ties included, and by exchangeability each index has it with the same probability. So $P(p \le \alpha) \le m/(B+1) \le \alpha$. Ties count against rejection, which makes the test conservative. $\square$

This holds for mixed F1 and for any other statistic. It is the textbook Monte Carlo test, and we do not claim it as new.

**Remark N.1 (the registered percentile rule).** PASS requires $T_0$ below the 2.5th percentile of $B = 1{,}000$ values, linearly interpolated at position 24.975, which lies between the 25th and 26th smallest. A PASS therefore implies that at most 25 null values are $\le T_0$. Its size under $H_0$ is then at most $26/1001 = 0.02597$, and close to $(25 + 0.975)/1001 = 0.02595$ for a continuous statistic. The rule $p \le 0.025$ has size at most $25/1001 = 0.02498$. The two rules can disagree only when $T_0$ falls between the 25th and 26th smallest null values, so the registered rule's size can exceed 0.025 by at most 0.001; at the p-value floor of Section 6.6 the two rules agree.

**Proposition N.4 (the registered $J$-draw statistic).** Theorem N.3 assumes that the null and the observed golds have the same joint law. With $J > 1$ draws, the registered null makes the $J$ golds of an image nested, because they are prefixes of one permutation. Two hypotheses follow.
- $H_0^{\text{nest}}$: given $\mathcal F$ (now including all $q^{(j)}_i$), images are independent, and $(Q^{(1)}_i,\dots,Q^{(J)}_i)$ has the law of the prefixes of one uniform permutation of $C_i$. Under $H_0^{\text{nest}}$, Theorem N.3's argument applies to $T$ verbatim. But $H_0^{\text{nest}}$ forces the golds drawn from different references to be nested, which real references generally are not.
- $H_0^{\text{perm}}$ (reference-level SCAR): given $\mathcal F$, images are independent, and the joint law of $(Q^{(1)}_i,\dots,Q^{(J)}_i)$ is invariant under permutations of $C_i$. This holds, for example, when the objects of an image are exchangeable in how references name them, such as equal naming propensity with independent naming. It does not need nesting.

Each draw has the same marginal law under both hypotheses: uniform of size $q^{(j)}_i$. So:

(a) for a linear statistic the means agree (Theorem N.1);

(b) let $T$ be linear with per-draw coefficient vectors $y^{(j)}_{i\cdot} = \kappa_{ij}\,u_{i\cdot}$ with $\kappa_{ij} \ge 0$. This covers precision ($\kappa = 1/J$), recall ($\kappa_{ij} = 1/(J\,n^{(j)}_+ q^{(j)}_i)$, and $0$ when $q^{(j)}_i = 0$), instance CHAIR, caption-level CHAIR (draw-invariant coefficients) and their OLS slopes, each taken alone, and combinations of draw-invariant statistics only (precision with instance CHAIR). It does not cover a mix of precision and recall: with $y^{(j)} = u + \kappa_j v$ the cross term can be negative (one image, $\ell = 2$, two size-1 draws, $u = (1,0)$, $v = (0,1)$, $\kappa = 0$ and $2$: nested covariance $-0.25$, independent $0$). For such $T$, $\operatorname{Var}_{\text{nest}}(T) \ge \operatorname{Var}_{\text{perm}}(T)$;

(c) for a statistic in the class of (b), only the variance ordering is proved. Conservatism then follows under approximate normality under both hypotheses: the test is conservative under $H_0^{\text{perm}}$ to that approximation, and not exact. Its true size is below the nominal level, so it errs toward FAIL. Normality is plausible here because $T$ is a sum of independent bounded image terms. Micro-F1 and mixed F1 fall outside (b): for micro-F1 the denominator $\sum_i M^S_i + \sum_i q^{(j)}_i$ mixes $S$ and $j$, and for mixed F1 the delta-method weights $\partial_P g, \partial_R g$ change with the draw. For these two, and so for the registered mixed-F1 statistic, conservatism is a **conjecture**, not a proved property: it holds to the extent that those weights vary little across draws, which is an assumption. Check D4a (development data; simulated references (not gold); the registered statistic) returned FAIL, so this conjecture is unsupported (S1.N.6).

*Proof of (b).* Images are independent under both hypotheses, so it suffices to treat one image. The diagonal terms $\operatorname{Var}(\sum_c y^{(j)}_c Z^{(j)}_c)$ depend only on the marginals, so they agree. For $j \ne j'$, Lemma N.1 gives the covariance as $\frac{\ell \mathbb E m_{jj'} - q^{(j)}q^{(j')}}{\ell(\ell-1)}\kappa_j\kappa_{j'}\sum_c(u_c - \bar u)^2$. This is nondecreasing in $\mathbb E m_{jj'}$, and the nested coupling attains the largest possible intersection, $m_{jj'} = \min(q^{(j)}, q^{(j')})$. $\square$

What this means for the printed results: the X4/X5 p-values are valid only under the nested hypothesis $H_0^{\text{nest}}$, which real references do not satisfy. Under reference-level SCAR, the variance ordering is proved for the class of (b) and conservatism then follows under approximate normality; for the registered mixed-F1 statistic, conservatism is an unsupported conjecture (check D4a on development data, simulated references (not gold): FAIL; S1.N.6). The printed p ≤ 0.001 of X4 and X5 therefore describes $H_0^{\text{nest}}$ only: it is not evidence against reference-level random omission, and not a size guarantee under SCAR. A single-draw ($J = 1$) statistic would be valid under $H_0$ (Theorem N.3).

### S1.N.5 Result 3: what the gap identifies

Let the real reference process have marginal keep probabilities $w_{ic} = P(c \in Q_i \mid \mathcal F)$ (with $J$ draws, $w^{(j)}_{ic}$, averaged as the statistic is). Define the excess $\delta_{ic} = w_{ic} - \rho_i$. Since $Q_i \subseteq C_i$ and $|Q_i| = q_i$, $\sum_c w_{ic} = q_i$, so $\sum_{c \in C_i}\delta_{ic} = 0$ for every image.

**Theorem N.5.**

(a) *Identity.* For every linear metric $f$, $\mathbb E[f^S(Q)] - \mathbb E_{\mathcal N}[f^S] = e^S_f := \sum_i\sum_c y^S_{ic}\,\delta_{ic}$, and $\mathbb E[\beta(f(Q))] - \mathbb E_{\mathcal N}[\beta(f)] = \beta(e_f)$. Explicitly:
- $e_P^S = \sum_i\sum_c h^S_{ic}\delta_{ic}/\sum_i M^S_i$;
- $e_R^S = \frac1{n_+}\sum_{i:\,q_i>0}\sum_c h^S_{ic}\delta_{ic}/q_i$;
- $e_{\mu}^S = 2\sum_i\sum_c h^S_{ic}\delta_{ic}/(\sum_i M^S_i + \sum_i q_i)$;
- $e_{\text{CHAIR}_i}^S = -\sum_i\sum_c a^S_{ic}\delta_{ic}/\sum_i A^S_i$;
- $e_{\text{CHAIR}}^S = -\frac1n\sum_{i:\,M^S_i>0}\sum_c h^S_{ic}\delta_{ic}/M^S_i$.

The identity uses only the marginals $w$; it needs no independence across images. Under the reference model, the observed gap $\beta(f(Q)) - \mathbb E_{\mathcal N}\beta(f)$ is therefore an unbiased estimate of $\beta(e_f)$, the verbosity slope of the selection excess.

(b) *Sign.* If $e^S$ is nonincreasing in $x^S$ ($x^S < x^{S'} \Rightarrow e^S \ge e^{S'}$), then $\beta(e) \le 0$. Equality holds iff $e$ is constant across systems with distinct $x^S$. For the two CHAIR forms $e$ carries a minus sign, so the CHAIR slope lies *above* its null when the corresponding precision-type excess is nonincreasing. If the keep probabilities are those of random deletion ($w_{ic} = \rho_i$), then $\delta \equiv 0$ and the gap is zero for every linear metric.

(c) *Nested frontier.* Order the systems so that $x^1 < x^2 < \dots$, and suppose $\hat O^S_i \subseteq \hat O^{S+1}_i$ for all $i$. This is a strong form of (A3), checked by D5 on development data. Reading (c) is allowed only where the lower 95% bootstrap bound of both matched shares is at least 0.80. This holds for 14 recorded short–detailed pairs: on COCO-5000 the distilled, zero-shot, fuse2_s42 and p1_s43 systems; on XM3600 fuse2_s42, p1_s43 and zero-shot; on UIT-ViIC p1_s43, zero-shot, and fuse2_s42 and p1_s42 from a second set of UIT-ViIC runs; and the second backbone on UIT-ViIC at T0, T05 and T08. For the second backbone on XM3600 (T0, T05, T08) the lower all-mention bound is 0.729–0.748, so there reading (c) is tied to the prefix arm of D3(b). One further UIT-ViIC fuse2_s42 pair is not in the record and gets no reading.<!-- src: data/results/a_dchecks/dchecks_result.json (63cabfa3, commit 1f157d2) :: checks.D5.pairs.*.{lower_gold, lower_all, label}: ALLOWED = coco/F1|{distill,zeroshot,fuse2_s42,p1_s43}, xm/F1|xm3600_{fuse2_s42,p1_s43,zeroshot}, uit/F1|uitviic_{p1_s43,zeroshot} (data/results/uitviic/), uit/F1|uitviic_{fuse2_s42,p1_s42} (data/results/uitviic_ind_test/; CC-274 Ruling 4c), uit/F2|g2b_q3_uv231-T{0,05,08}; PREFIX_ONLY = xm/F2|g2b_q3_xm600-T{0,05,08}, lower_all 0.7457/0.7481/0.7285; unrecorded = data/results/uitviic/uitviic_fuse2_s42 (basename collision, CC-274 W3) --> Let $\tau_S = \sum_i M^S_i$ and $D_S = \sum_i\sum_c h^S_{ic}\delta_{ic}$. Step $S \to S+1$ adds $t_S = \tau_{S+1} - \tau_S > 0$ (strictly increasing $x^S$ with nested classes gives $t_S > 0$) classes, of total excess $d_S = D_{S+1} - D_S$; an added class outside $C_i$ adds 1 to $t_S$ and 0 to $d_S$. Then:
- precision: $e_P^{S+1} \le e_P^S \iff d_S/t_S \le D_S/\tau_S = e_P^S$. This is the condition that the marginal excess per added mention is at most the average excess;
- micro-F1 ($q_+ = \sum_i q_i$): $e_\mu^{S+1} \le e_\mu^S \iff d_S/t_S \le D_S/(\tau_S + q_+) = e_\mu^S/2$;
- recall: $e_R^{S+1} - e_R^S = \frac1{n_+}\sum_{i:\,q_i>0}\big(\sum_{c\ \text{added}}\delta_{ic}\big)/q_i$. It is nonincreasing iff the added classes have a nonpositive $1/q_i$-weighted excess. Added classes outside $C_i$ leave it unchanged;
- instance CHAIR: as precision, with repeat counts ($\tau_S = \sum_i A^S_i$, $D_S = \sum_{i,c} a^S_{ic}\delta_{ic}$), and with the sign reversed as in (b). This needs nested mention multisets ($a^S_{ic} \le a^{S+1}_{ic}$) and $t_S = \tau_{S+1} - \tau_S > 0$: nested classes along increasing $\ln M$ do not force $\sum_i A^S_i$ to rise, and with $t_S < 0$ the equivalence can flip;
- caption-level CHAIR: write $\varepsilon^S = \frac1n\sum_{i:\,M^S_i>0} D^S_i/M^S_i$, so $e^S_{\text{CHAIR}} = -\varepsilon^S$. A sufficient condition for $\varepsilon^{S+1} \le \varepsilon^S$ is: the precision condition within every image already covered at $S$, and, for every image first covered at $S+1$ ($M^S_i = 0 < M^{S+1}_i$), a total excess $D^{S+1}_i \le 0$ of its new mentions. Without the second part it fails: with two images, $S$ mentioning one class of excess 0 on image 1 only, and $S+1$ adding a class of excess $+0.5$ on image 2, $\varepsilon$ rises from 0 to 0.25 although no covered image breaks the per-image condition.

(d) *Where the sign condition fails.* For precision, if $e_P^S < 0$ and the added mentions all lie outside $C_i$ ($d_S = 0$), then $e_P^{S+1} = \tau_S e_P^S/(\tau_S + t_S) > e_P^S$. More generally, the condition fails whenever $d_S/t_S > e_P^S$. This can happen even when every added label class has $\delta_{ic} \le 0$, because unmatched mentions dilute a negative average. In this regime $\beta(e_P)$ need not be negative, even if references favour salient objects. The test of Theorem N.3 keeps its validity and loses power. Recall has no such regime (see (c)).

(e) *Mixed F1* (assume $p^S_\rho + r^S_\rho > 0$ and $p^S_w + r^S_w > 0$). $\mathbb E F^S(Q) - \mathbb E_{\mathcal N}F^S = \big[g(p^S_w, r^S_w) - g(p^S_\rho, r^S_\rho)\big] - \gamma^S_Q + \gamma^S_{\mathcal N}$. Here $p_w = \mathbb E P(Q)$ and $r_w = \mathbb E R(Q)$ (Theorem N.5(a)), the subscript $\rho$ marks the null values, and $\gamma$ are the plug-in gaps of Proposition N.2. $\gamma_{\mathcal N}$ is $O(1/n)$. $\gamma_Q$ is $O(1/n)$ if the real reference process is independent across images, and otherwise unknown. By the mean-value theorem the bracket equals $\partial_P g(\xi^S)\,e_P^S + \partial_R g(\xi^S)\,e_R^S$, with $\xi^S$ on the segment and both partial derivatives in $[0, 2]$. So the mixed-F1 gap is, up to $O(1/n)$, a nonnegative combination of the precision and recall excesses whose weights vary by system. Its sign is therefore not implied by the precision condition of (c). The mixed-F1 version of Result 3 is first order only. We do not linearise in $\delta$: on X4 the excess is larger in size than the null mean, so $\delta$ is not small.

*Proofs.* (a) Theorem N.1's argument with $w$ in place of $\rho$, then subtract. (b) Chebyshev's sum inequality (Hardy, Littlewood and Pólya, 1952, §2.17)<!-- cite: to verify -->: $\sum_S(x^S - \bar x)(e^S - \bar e) = \frac{1}{2|\mathcal S|}\sum_{S,S'}(x^S - x^{S'})(e^S - e^{S'})$, and every term is $\le 0$ when $e$ is nonincreasing in $x$; all terms vanish iff $e$ is constant across distinct $x$. The OLS slope has the sign of this sum. (c) $e_P^{S+1} = \frac{\tau_S}{\tau_S + t_S}e_P^S + \frac{t_S}{\tau_S+t_S}\frac{d_S}{t_S}$ is a weighted mean of $e_P^S$ and $d_S/t_S$. For micro-F1, $(D_S + d_S)(\tau_S + q_+) \le D_S(\tau_S + t_S + q_+) \iff d_S(\tau_S + q_+) \le D_S t_S$. Recall is a sum with fixed denominators. (d) is direct substitution. (e) Proposition N.2(a) applied to both processes, and the mean-value theorem for $g$ on the segment from $(p_\rho, r_\rho)$ to $(p_w, r_w)$. $\square$

**Remark N.2 (link to Proposition 1; a conjecture, not proved).** Under (A1)–(A3), a $k$-reference gold keeps an object of propensity $\pi$ with probability $c_k(\pi) = 1 - (1-\pi)^k$, which increases in $\pi$. (A2) orders $F_m$ by likelihood ratio, which implies the usual stochastic order. Hence $\mathbb E_{F_m}[c_k(\pi)]$ is nonincreasing in the mention rank $m$; this step is proved. If one reads $w_{ic} \approx c_k(\pi_c)$, centred by the image mean, as the excess, the expected per-mention excess at rank $m$ is $s_m\bar\delta_m$ with $\bar\delta_m$ nonincreasing. The condition of (c) holds along the frontier whenever $s_m\bar\delta_m$ is nonincreasing, since the average of a nonincreasing sequence is at least its next term. That follows from (A2) when $\bar\delta_m \ge 0$ and $s_m$ is nonincreasing, but not when $\bar\delta_m < 0$ and $s_m$ falls, which is case (d). The reading is heuristic because $w_{ic}$ conditions on $(C_i, q_i)$, $c_k$ does not, and the centring constants differ. It motivates the condition; it does not derive it from Proposition 1.

### S1.N.6 Assumptions and their checks

All checks were run once, on spent development sets only, on CPU, as post hoc descriptive checks with no verdict on any registered prediction. Labels: D1 PASS, D2 PASS, D3 PASS (COCO-5000 and XM3600 only), D4a FAIL, D4b FAIL (both on simulated references, not gold), D5 descriptive.<!-- src: data/results/a_dchecks/dchecks_result.json (63cabfa3, commit 1f157d2) :: checks.*.label; status; CC-274 Ruling 1 -->

| # | Assumption | Used by | Check on development data, label |
|---|---|---|---|
| 1 | Size matching per image: $q_i$ is the observed reference-gold size and $Q_i \subseteq C_i$ (intersection where labels are not a superset) | all | by construction (code: `salience`, intersection step) |
| 2 | Captions, complete gold and sizes are conditioned on | all | by construction |
| 3 | Linear metric for the exact parts | Theorems N.1, N.5(a)–(d) | mixed F1 first order only: D1 measures the plug-in error: **PASS** (four linear metrics and the mixed-F1 plug-in; instance CHAIR omitted (class-set matchers)) |
| 4 | Excess nonincreasing in $x^S$ (marginal ≤ average excess along the frontier) | Theorem N.5(b)–(c) | D3 (per-mention excess curve; within-caption prefix truncation); share of unmatched added mentions (regime (d)): **PASS** on COCO-5000 and XM3600 only (prefix arm: every one-sided upper bound below 0, largest −0.015, SESOI 0.01); UIT-ViIC not testable, as outputs rarely reach five classes; Kendall τ descriptive only |
| 5 | $w$ estimated leave-one-out from the other $K-1$ references (exchangeable references, (A1), Section 5). This estimate is unconditional on $q_i$, which is disclosed | Theorem N.5(a) on data | D2: **PASS**, per-reference exchangeability not rejected (Holm over 38 tests, minimum p 0.080, every half-width within $0.5\,\lvert g_{\text{obs}}\rvert$); R descriptive only |
| 6 | $H_0$ (single draw) or $H_0^{\text{perm}}$ (registered $J$-draw statistic) | Theorem N.3, Proposition N.4 | D4a (simulated references (not gold) under reference-level SCAR: p-value uniformity of the registered statistic): **FAIL**. D4b (salience-correlated thinning, simulated references (not gold)): **FAIL**, $\bar G = -11.61$ against $\beta_\delta = -11.57$, tolerance 0.035 |
| 7 | Nested outputs (strong (A3)) | Theorem N.5(c) | D5: descriptive; reading (c) for 14 recorded pairs only |

*D4a, FAIL.* With simulated references (not gold), the check used the 20-draw statistic on development data (simulated references at the real K and sizes, level 1; 50 simulated references, levels 1 and 5). PASCAL-50S outputs cannot be re-checked per image; this is an analogue on development data. Sections 4.3 and 6.6 therefore do not read p ≤ 0.001 beyond $H_0^{\text{nest}}$, and the conjecture of Proposition N.4(c) is unsupported. Post hoc observation: the observed rejection rate at the 2.5% level was 0.000–0.020 in all 48 cell-by-statistic tests, below the registered bound 0.059; the failure comes from the one-sided Kolmogorov–Smirnov criterion, which rejected in 34 of 48 tests (14 of 16 cells).

*D4b, FAIL.* On development data, with simulated references (not gold), the identity check failed. Under the registered rule, FAIL means an implementation fault, or the identity is not reached; the record does not tell these two apart. Result 3 is therefore not illustrated by the simulation, and no power statement is made.<!-- src: data/results/a_dchecks/dchecks_result.json (63cabfa3, commit 1f157d2) :: checks.D4a.{label, wording, disclosure, m = 48}, checks.D4a.cells.*.{F,P,R}.{rejection_rate (min 0.0, max 0.02), bound (0.05898), ks_one_sided_p (< 0.05/48 in 34 tests, 14 cells)}; checks.D4b.{G_bar, beta_delta, se_sim, se_w, label}, tolerance = 2*sqrt(se_sim^2 + se_w^2) = 0.0346 (DERIVED); plan A_DCHECKS_PLAN_v3.md l.214, l.223; CC-274 Ruling 2(d)-(e), Ruling 3, addendum A2 -->

### S1.N.7 What these results do not guarantee

- That $C_i$ itself lists every present object. Everything is relative to $C_i$, and reference classes outside $C_i$ are removed by construction, so reference-gold precision on those classes is not assessed.
- The exact mixed-F1 null mean, and the sign of the mixed-F1 gap. Both are first order only (Proposition N.2, Theorem N.5(e)).
- The direction of the gap when the excess is negative and verbose systems add mostly unmatched mentions (Theorem N.5(d)).
- Validity of the registered 20-draw test beyond the nested hypothesis. Under reference-level SCAR only a variance ordering is proved (class of Proposition N.4(b)); conservatism follows under approximate normality, and for mixed F1 it is an unsupported conjecture (Proposition N.4(c); check D4a on development data, simulated references (not gold): FAIL).
- Anything about cause.
- Transfer of the excess curve from a development set to another benchmark.
- Monotonicity of $e^S$ across 4–6 systems, which is barely testable. This is why check D3 adds within-caption prefix truncation.

<!-- END SUPPLEMENT TEXT -->

## Verification record (internal; numbers here are synthetic, not paper numbers)

- Script: `~/a_theory_check_1105/check.py`, sha256 `5af48362a7844645fe0efe5f41ae8c54475a0d0438c76740ddce881c42a97807`.
- Run: `~/.venvs/vsps_h1/bin/python -I check.py > out.txt` (numpy 2.5.4, scipy 1.18.1; laptop CPU, about 50 s; no repo data read).
- Scope of the checks: these are **illustrative synthetic math checks**, not a proof and not a test of the production code (`p50x.py` is not imported). They do not exercise Theorem N.5(e), the recall frontier condition or the caption-level CHAIR condition; Proposition N.4 is illustrated on one simulated world type ($J = 5$); the $J = 1$ size checks use a 3-SE tolerance, so they can detect gross errors only.
- Output `out.txt` sha256: `faccc7dd464a275827365a257dc428ac1ff69018e5b233fceaa2129c7ca76a1f`. Result: 49/49 checks passed.
- The script has four parts:
  - Part A is exact rational enumeration (`fractions.Fraction`) over every joint gold of a 4-image, 4-system instance. That instance has repeated mentions, hallucinated mentions and one image with $q_i = 0$. Part A also uses a non-uniform process whose images are dependent: a mixture of two conditional-Bernoulli products.
  - Part B is Monte Carlo (4,000 null draws per $n$) of the mixed-F1 gap.
  - Part C is Monte Carlo for Theorem N.3, Remark N.1 and Proposition N.4.
  - Part D covers the sign algebra.
- Two Part B columns need reading notes:
  - "direct−identity" is the plain Monte Carlo difference, dominated by its MC SE (shown).
  - The exact-identity estimator has far lower variance; $n\cdot$gap stays near 0.011 as $n$ grows 64-fold, which is the $1/n$ rate.

Verbatim output:

```
== Part A: exact enumeration ==
[PASS] R1 exact: E_null[P] per system == plug-in at keep-rate
[PASS] R1 exact: E_null[slope P] == slope at keep-rate
[PASS] R1 exact: E_null[R] per system == plug-in at keep-rate
[PASS] R1 exact: E_null[slope R] == slope at keep-rate
[PASS] R1 exact: E_null[F1mu] per system == plug-in at keep-rate
[PASS] R1 exact: E_null[slope F1mu] == slope at keep-rate
[PASS] R1 exact: E_null[CHAIRi] per system == plug-in at keep-rate
[PASS] R1 exact: E_null[slope CHAIRi] == slope at keep-rate
[PASS] R1 exact: E_null[CHAIRc] per system == plug-in at keep-rate
[PASS] R1 exact: E_null[slope CHAIRc] == slope at keep-rate
[PASS] R1 corollary: E_null[R] == complete-gold recall over images with r_i > 0
[PASS] R1 mixed F1: exact identity for the plug-in gap
[PASS] R1 mixed F1: gap <= 4VarU/(p+r)^3 + 4max(p,r)sd(U)sd(P+R)/(p+r)^3 for every system
[PASS] R1 mixed F1: plug-in >= null mean for every system (concavity)
   plug-in gap per system  : ['0.00555', '0.00331', '0.00206', '0.00104']
   leading term per system : ['0.00583', '0.00348', '0.00165', '0.00090']
   slope of exact E F1mix vs plug-in slope: 0.06546 0.06163
[PASS] R3: sum_c delta_ic == 0 per image
[PASS] R3(a) exact (dependent images): E[metric] == plug-in at w
[PASS] R3(a) exact identity: E[slope P](R) - E_null[slope P] == slope of excess
[PASS] R3(a) exact identity: E[slope R](R) - E_null[slope R] == slope of excess
[PASS] R3(a) exact identity: E[slope F1mu](R) - E_null[slope F1mu] == slope of excess
[PASS] R3(a) exact identity: E[slope CHAIRi](R) - E_null[slope CHAIRi] == slope of excess
   gaps P, R, F1mu, CHAIRi: ['0.00778', '0.01622', '0.00633', '-0.00080']
[PASS] cov lemma formula exact [nested; y,y]
[PASS] cov lemma formula exact [nested; y,3y]
[PASS] cov lemma formula exact [nested; y,yb]
[PASS] cov lemma formula exact [independent; y,y]
[PASS] cov lemma formula exact [independent; y,3y]
[PASS] cov lemma formula exact [independent; y,yb]
[PASS] cov lemma formula exact [overlap=0; y,y]
[PASS] cov lemma formula exact [overlap=0; y,3y]
[PASS] cov lemma formula exact [overlap=0; y,yb]
[PASS] cov lemma formula exact [overlap=1; y,y]
[PASS] cov lemma formula exact [overlap=1; y,3y]
[PASS] cov lemma formula exact [overlap=1; y,yb]
[PASS] cov lemma formula exact [overlap=2; y,y]
[PASS] cov lemma formula exact [overlap=2; y,3y]
[PASS] cov lemma formula exact [overlap=2; y,yb]
[PASS] cov lemma: nested coupling has the largest covariance for proportional coefficients
   cov (y,yb) by coupling: {'nested': '-98/25', 'independent': '0', 'overlap=0': '147/25', 'overlap=1': '49/50', 'overlap=2': '-98/25'} -> sign can reverse when coefficients are not proportional
== Part B: mixed-F1 plug-in error vs n (Monte Carlo) ==
   n=  100  gap(identity MC) mean=9.54e-05  n*gap=0.010  sum lead/sum identity=0.978  direct-identity max|.|=3.9e-04 (direct MC SE 4.1e-04)  slope err (x100)=-0.0173  bound (x100)=0.0203
   n=  400  gap(identity MC) mean=3.05e-05  n*gap=0.012  sum lead/sum identity=0.980  direct-identity max|.|=3.1e-04 (direct MC SE 2.1e-04)  slope err (x100)=-0.0053  bound (x100)=0.0061
   n= 1600  gap(identity MC) mean=7.02e-06  n*gap=0.011  sum lead/sum identity=1.016  direct-identity max|.|=1.4e-04 (direct MC SE 1.0e-04)  slope err (x100)=-0.0012  bound (x100)=0.0014
   n= 6400  gap(identity MC) mean=1.84e-06  n*gap=0.012  sum lead/sum identity=0.996  direct-identity max|.|=9.7e-05 (direct MC SE 5.1e-05)  slope err (x100)=-0.0003  bound (x100)=0.0004
[PASS] R1 mixed F1: leading term within 5% of the exact gap at n=6400
[PASS] R1 mixed F1: slope error within the range bound
== Part C: Result 2 ==
   share of null draws tied with the observed value: 0.0000 (ties count against rejection)
[PASS] R2 (J=1, H0 exact): P(p<=0.01) = 0.0073 vs exact 0.0100 (3 SE = 0.0054)
[PASS] R2 (J=1, H0 exact): P(p<=0.025) = 0.0193 vs exact 0.0200 (3 SE = 0.0077)
[PASS] R2 (J=1, H0 exact): P(p<=0.05) = 0.0443 vs exact 0.0500 (3 SE = 0.0119)
[PASS] R2 (J=1, H0 exact): P(p<=0.1) = 0.0927 vs exact 0.1000 (3 SE = 0.0164)
   KS of randomised p-values vs U(0,1): D=0.0208, p=0.148
[PASS] R2 (J=1): randomised p-values not rejected as uniform (KS p > 0.01)
   percentile rule (obs < 2.5th percentile of 1,000): rate=0.02599; theory 0.02595; p<=0.025 rule size 0.02498
[PASS] R2: percentile-rule size matches (25+0.975)/1001 within 3 SE
   reference-level SCAR, J=1: P(p<=0.025)=0.0320 (exact 0.0250), var(z)=1.007
[PASS] R2 (J=1, reference SCAR): size within 3 SE of 0.025
   reference-level SCAR, J=5: P(p<=0.025)=0.0000 (exact 0.0250), var(z)=0.392
[PASS] R2 (J=5, nested null under reference SCAR): conservative (var(z) < 1, size <= 0.025 + 2 SE)
== Part D: Result 3(b)-(d) ==
[PASS] R3(b): nonincreasing excess => OLS slope <= 0 (20,000 random cases)
[PASS] R3(c): e_{s+1} <= e_s  <=>  d/t <= D/(T+K)  (K=0 precision; K=sum r micro-F1)
[PASS] R3(d): e_s < 0 and only unmatched additions => e_{s+1} > e_s

49/49 checks passed
```

Reading notes:
- **Small-instance leading term.** In the 4-image instance the leading term is off by up to 20%, as expected at $n = 4$. At $n = 6{,}400$ it is within 0.4%.
- **Reference-level SCAR world (Part C).** It has 10 references per image and $J$ single-reference draws. The world for $J = 5$ shows the conservatism of Proposition N.4 ($\operatorname{var} z = 0.39$, no rejection in 400 worlds); the case $J = 1$ shows exactness.
- **Percentile-rule size.** A separate 1,000,000-draw run (uniform, seed 99) gave 0.026056 against the theoretical 0.025949 (0.67 SE). That run is not part of `check.py`.

## Verification record v2 (internal; 2026-11-06)

- `check.py` (5af48362) re-run unchanged: output byte-identical to `out.txt` (faccc7dd), 49/49 PASS.
- `~/a_theory_check_1105/check_v2.py` sha256 `8606cb8d97c361721e45e620ebbd103e0316f46e2d9d7e46c5a268e1cb3ba95a` = check.py plus Part E (CC-263 B4 edge cases). Run `~/.venvs/vsps_h1/bin/python -I check_v2.py > out_v2.txt`; `out_v2.txt` sha256 `578a3be249bce9aabc9f7a9571a046d4c8180978c45b5baf609a3c8910096bdf`; 53/53 PASS. Parts A-D output identical to out.txt (diff differs by one blank line only). Part E output:

```
== Part E: Theorem N.5(c) edge cases (CC-263 B4) ==
[PASS] E1: t_S < 0 counterexample: d/t <= D/tau yet (D+d)/(tau+t) > D/tau
[PASS] E1: with t_S > 0 the instance-CHAIR (precision-type) equivalence holds (20,000 cases)
[PASS] E2: newly covered image with positive excess: e_CHAIRc falls (0 -> -0.25) with no per-image violation
[PASS] E2: per-image condition + newly covered images with excess <= 0 => caption-CHAIR excess sign holds

53/53 checks passed
```
(Part E labels in the script refer to Theorem N.5, the v2 numbering. A third Part E check on the recall increment was dropped as tautological.)

## Codex read-only math check (internal; strip before transfer)

Run 2026-11-05/06 via the codex plugin `codex-companion.mjs task` without `--write` (sandbox "read-only"); thread 01a1aca8-2bf7-7873-a98f-9dcf232a39c1. Prompt: seven targeted questions (Lemma N.1; Prop. 2; Thm 3 and Remark N.1; Prop. 4 against the code; Thm 5; exactness/assumptions; check.py coverage). Raw output kept at /tmp/codex_a_theory_out.txt (not archived).

| # | Codex verdict and finding | Class | Response |
|---|---|---|---|
| Q1 | Lemma N.1 correct for l ≥ 2 incl. sizes 0 or l; l = 1 case missing | NB | Fixed: l = 1 covariance is zero, stated |
| Q2 | Identity (a), bounds (b), slope bound (d) correct; O(1/n) in (c) needs p + r ≥ c0 > 0 | **B** | Fixed: c0 added to (c); main text now "under mild conditions" |
| Q3 | Rank argument with ties correct; 24.975 position, 26/1001 bound, 25.975/1001 continuous size, 25/1001 for p ≤ .025 all correct | — | No change |
| Q4 | Code confirmed: 20 independent observed draws vs nested prefixes of one permutation per null replicate; variance ordering correct for the proportional class; "approximately conservative" for the registered mixed-F1 statistic overstated | **B** | Fixed: conservatism proved only for the linear class of 4(b); for mixed F1 called a heuristic expectation, to be checked by D4 with the registered statistic; main text and "does not guarantee" list changed to match |
| Q5 | (a) marginals only, (b) incl. ties, (c) per-metric conditions, (d), (e) algebra correct; (e) needs p+r > 0 at both endpoints; n+ > 0 | NB | Fixed: endpoint conditions in (e); n+ > 0 and ΣM > 0 stated in the setting |
| Q6 | XM3600 OIV7 verified precision (denominator = mapped mentions with known status) is not the theory's metric | **B** | Fixed: scope paragraph in S1.N.1; verified precision is out of scope; XM3600 checks use references ∩ labels with standard precision |
| Q7 | check.py useful but illustrative: no production-code parity; Prop. 4 one world; J = 1 check 3-SE tolerance weak; 5(e), recall frontier, caption-CHAIR condition untested | NB | Accepted: scope sentence added to the verification record; no new checks added (D1-D5 on dev data are the real tests; production parity belongs to step 8's deletion_null selftest) |

All three BLOCKING items were addressed by narrowing claims, not by adding new results. No algebraic error was found. A second Codex read was not run; the one-judge full read at step 4's gate should confirm the three fixes.
