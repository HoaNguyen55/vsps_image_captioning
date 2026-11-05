<!-- INTERNAL HEADER (strip before transfer to the paper repo)
Draft v2, 2026-11-06 (v1 2026-11-05). Step 4 of manuscript/directions/A_UPGRADE_PLAN_2026-11-04.md (theory Results 1-3, target rubric T2 = 3).
Status: DRAFT, not judged, not applied, not committed. Paper repo untouched.
Placement: new §4.3 in paper/sec4_theory.md, after the paragraph "Two channels, and what this does not predict".
Proofs: manuscript/reviews/A_SUPP_S1_PROOFS_DRAFT_2026-11-06_v2.md (Supplementary S1, new subsection S1.N).
Word count of the paper text below (between the BEGIN/END markers, comments excluded): see the proofs file, record R0.
Notation vs plan §2.1: the plan's n_i, k_i, R_i, N become l_i, q_i, Q_i, n here, because the paper already uses
n = images, k = number of references, R = recall (sec3 §3.1). G-tilde (null gold) avoids the paper's generic G_i.
Departures from the plan §2.2, all found while checking the algebra (details in the proofs file, internal notes):
 (1) CHAIR is not 1 - P (supplementary_SPIC.md:86); both CHAIR forms are written as affine in the indicators.
 (2) Mixed-F1 plug-in error: exact identity, never below the null mean, O(1/n); the plan's "variances only" missed Cov(P,R).
 (3) The registered X4/X5 statistic averages J = 20 reference draws, and its null uses nested prefixes of one
     permutation (scripts/pascal50s/p50x.py null_slopes); the textbook exactness holds for J = 1 or under a nested null
     law. Under reference-level SCAR the registered null is over-dispersed (conservative), not exact.
 (4) The nested-frontier condition differs by metric (precision / micro-F1 / recall); stated per metric in S1.
Assumptions are "to be checked (D1-D5)"; none is verified yet.

v2 (2026-11-06), from v1 A_THEORY_DRAFT_2026-11-05.md (3b5d7263, unchanged) after CC-263 (NEXT_ROUND 78):
| Item | v1 | v2 |
|---|---|---|
| B1 | "lies below the null when ...; on a nested frontier, exactly when" | "In expectation, ... at or below the null whenever ...; on a nested frontier, the excess does not rise exactly when" |
| B2 | "the plug-in value is never below the null mean" | per system score; slope plug-in error "can take either sign" |
| B3 | "not exact; for mixed F1 expected, not proved, conservative" | "valid only under a nested hypothesis that real references do not satisfy"; variance ordering for P and R, conservative under approximate normality; mixed F1 "a conjecture" |
| B5 | "label gold" for C_i | "complete gold" (label gold where labels exist; X4: union of all references); "label-gold recall/TP" -> "complete-gold" |
| N3 | "the selection form of the b-channel" | "a selection analogue ... (heuristic link, Supplementary S1)" |
| N5 | Chen author form open | cite comment: Crossref family name Chen (fields still to add to paperA.bib) |
| N2 (at transfer) | - | companion edits, not made here: sec4 "Two channels" and §6.6 "are that SCAR case"/"can reject uniform deletion" must say the registered null is the nested SCAR null and point to §4.3 and Supplementary Proposition N.4 |
-->

<!-- BEGIN PAPER TEXT -->

## 4.3 What the size-matched deletion null identifies

Let $C_i$ be the complete gold of image $i$ ($\ell_i$ classes; the label gold where labels exist, and for X4 the union of all references) and $Q_i \subseteq C_i$ a reference gold restricted to $C_i$ ($q_i$ classes; keep-rate $\rho_i = q_i/\ell_i$). The null of Section 6.6 replaces $Q_i$ by a uniformly random $q_i$-subset of $C_i$. With captions fixed, precision, recall, micro-F1 and both CHAIR forms are affine in the indicators $1[c \in Q_i]$, since size matching fixes every denominator; we call them *linear*. Mixed F1 is not. Proofs: Supplementary S1.

**Result 1 (null mean).** For a linear metric, the null mean of each score and of the verbosity slope is the value with every indicator replaced by $\rho_i$; no simulation is needed. Under the null, recall equals complete-gold recall (over images with a non-empty reference gold) in expectation, while precision weights each image's complete-gold true positives by its keep-rate; a constant keep-rate only rescales (cf. Shulman, 2026; Chen, 2026)<!-- cite: to verify; Shulman SSRN 10.2139/ssrn.7291675 (abstract read only, keep "cf."); Research Square 10.21203/rs.3.rs-10639224/v1, Crossref family name Chen -->. For mixed F1 this holds to first order only: each system's plug-in score is never below its null mean, and under mild conditions the gap shrinks as $1/n$; for the slope, the plug-in error can take either sign.

**Result 2 (validity).** If, given $C_i$ and $q_i$, the reference gold is a uniformly random subset, independent across images and of the captions, the observed slope is one more draw from the null and the Monte Carlo p-value is valid for any statistic. This is the standard randomisation-test argument (Besag and Clifford, 1989)<!-- cite: to verify; not in paperA.bib -->, not a contribution. The registered statistic averages 20 reference draws while its null draws nested subsets<!-- src: scripts/pascal50s/p50.py (sha256 2387ca05ae8a) :: N_REP = 20; scripts/pascal50s/p50x.py (sha256 3f562e878ed7) :: null_slopes, salience -->; the p-value is therefore valid only under a nested hypothesis that real references do not satisfy. When references omit objects at random, that null has at least the true variance for precision and recall, so the test is conservative under approximate normality; for mixed F1 this is a conjecture.

**Result 3 (what the gap measures).** Let $w_{ic}$ be the probability that real references keep class $c$ of $C_i$, and $\delta_{ic} = w_{ic} - \rho_i$ its excess over random. For a linear metric, the expected gap between the reference-gold slope and the null mean is the verbosity slope of the systems' excess; for precision, the mention-weighted mean excess $\sum_i\sum_c h^S_{ic}\delta_{ic}/\sum_i M^S_i$, with $h^S_{ic} = 1$ if system $S$ mentions $c$. In expectation, the precision slope lies at or below the null whenever this excess does not rise with verbosity; on a nested frontier, the excess does not rise exactly when the classes a more verbose system adds carry, per mention, no more excess than those it already mentions. This is a selection analogue of the b-channel (Section 4.2; a heuristic link, Supplementary S1).

**Assumptions and limits.** All results condition on the captions, the complete gold and the sizes $q_i$; Results 1 and 3 use only marginal keep probabilities, Result 2 the joint law. That the excess falls with verbosity is an assumption, to be checked on development data. The results do not guarantee that $C_i$ itself lists every present object (reference classes outside it are dropped), the exact mixed-F1 null mean or the sign of its gap, the direction when the excess is negative and verbose systems add mostly unmatched mentions (the test then loses power but stays valid), transfer to another benchmark, or anything about cause.

<!-- END PAPER TEXT -->
