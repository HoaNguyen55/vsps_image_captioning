# 4 A descriptive decomposition of the verbosity slope

<!-- v2 (SPIC, 2026-10-27): cut per plan §2 "§4" and Ken W5 (accepted): keeps §4.1 and the statement of Proposition 1 with one "describes, does not predict" paragraph. The limits of parts (a) and (c), the closed form M*, the old §4.3 post hoc checks on COCO-5000 (all numbers with their src comments), Fig. 4 and the channel split moved verbatim to Supplementary S1 ("Material moved from Section 4 in v2"); the proof was already in S1. -->

This section decomposes F1's verbosity slope under a gold; it is a description, not the claim the registered tests confirm (proofs and post hoc checks: Supplementary S1).<!-- rev2 (CC-181 W8): condensed; original paragraph moved verbatim to Supplementary S10 -->

## 4.1 A propensity model of reference gold

Let object $o$ present in image $i$ have a *naming propensity* $\pi_o \in [0,1]$: the probability that one reference writer names it. Unlike in Chen et al. (2015, §4.2), $\pi$ varies within an image: salient objects are named by almost every writer, background objects rarely. The propensity is close in spirit to measures of object importance built from which objects people name (Spain and Perona, 2011; Berg et al., 2012).

**(A1) Exchangeable references.** The $K$ references of an image are exchangeable and conditionally independent given the image (tested in Section 5). Under (A1) an object enters the $k$-reference gold with probability $c_k(\pi) = 1-(1-\pi)^k$, and the expected gold size $\bar G(k) = \sum_o \mathbb E\,c_k(\pi_o)$ is the incidence-based species-accumulation curve (Colwell et al., 2012<!-- cite: Colwell, Chao, Gotelli, Lin, Mao, Chazdon and Longino, J. Plant Ecology 5(1):3-21, DOI 10.1093/jpe/rtr044 (individual- and sample-based rarefaction and extrapolation), verified 2026-10-18 via Crossref -->; Chao et al., 2014). Instance gold corresponds to $c_\infty = 1$ for every present object.

For a family of systems that differ in how many objects they mention, let the $m$-th mention be a nameable present object with probability $s_m$, with propensity law $F_m$. Then $\mathrm{TP}_k(M) = \sum_{m\le M} s_m\, \mathbb E_{F_m}[c_k(\pi)]$.

**(A2) Salience ordering.** Later mentions have stochastically lower propensity ($F_m$ decreases in $m$ in the likelihood-ratio order).

**(A3) Shared frontier.** The systems of a family share $s_m$ and $F_m$; they need only sit on one frontier.

## 4.2 Proposition

Define the local frontier exponent $b_k(M) = d\ln \mathrm{TP}_k / d\ln M$, the ratio of marginal to average precision.

**Proposition 1.** Under (A1)–(A3): (a) $b_k(M)$ is nondecreasing in $k$; (b) $\bar G(k)$ is increasing and concave in $k$; (c) micro-F1 increases with $M$ if and only if $b_k/(1-b_k) > M/\bar G(k)$ (Lipton et al., 2014, Thm. 1; cited, not new); and (d) the index $\Lambda_k(M) = \operatorname{logit} b_k(M) + \ln \bar G(k) - \ln M$ is nondecreasing in $k$, so at a fixed family centre the sign of micro-F1's verbosity slope changes at most once as references are added, and only from negative to positive. For mixed F1 the condition differs, so the closed form is applied only to micro-F1 (Supplementary S1). Proposition 1 is therefore a micro-F1 result: it motivates, but does not derive, the ordering of the mixed-F1 slopes tested in Section 6.

**Two channels, and what this does not predict.** $\Lambda_k$ rises through a *b-channel*, which exists only because later mentions are named less often, and a *$\bar G$-channel*, which exists under any missingness. Because the $k$-reference golds are nested, the $\bar G$-channel alone already orders the slopes in $k$, so the ordering is expected even if objects are missing from references completely at random (SCAR), and confirming it supports the pattern, not the propensity model. The decomposition does not predict where the sign changes, the negative one-reference sign, or the sign with several references, which was predicted positive and failed on two English LVLM families and on XM3600; on PASCAL-50S neither sign-change location was predicted either (Section 6).<!-- rev1 (item 14): data/results/p50/p50_decide.json (0da4cab90fe9) :: analysis_set.P50-NS.{refs50|coco80, refs10_randk|V20, refs20_randk|V20, refs50|V20} (manifest keyed) --><!-- rev2 (CC-181 W8): condensed; original paragraph moved verbatim to Supplementary S10 -->
