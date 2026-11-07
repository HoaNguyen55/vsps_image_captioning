<!-- INTERNAL HEADER (strip before transfer)
S5 table under status BOUND_ONLY (CC-288 GO 88; plan §10.3 BOUND_ONLY, CC-288 N1/N2 defaults: arm U primary, the narrow list plus E5
pooled counts; arm L Ĉ_5 only, labelled "restricted to labelled classes"). E2 (the Ŝ(r) curve), E3 (Ĉ_r for r < 5) and E4 are NOT
included: they enter only if the S1.M read allows it (N2), E4 then under J6.
Every number: data/results/a_m1/a_m1_result.json (sha256 5687a66b20785c626646d1b54934c590274c4a5244c4cb27150ab6292f00dcb4,
commit a245481), key paths below, rounded to 3 decimals (counts exact). R = data/results/a_m1/a_m1_result.json.
J13 fired (CC-288 Ruling 4): every UIT-ViIC bound number is in S5 only, never in the main text.
-->

<!-- BEGIN SUPPLEMENT TEXT -->

**Table S5.M.** Reference-only bound on the coverage of the five-reference gold, and two pre-specified development checks (development data; pairs pooled over images; 95% image-bootstrap intervals, 2,000 resamples; every bound asymptotic, under (A1); Supplementary S1.M).

| Row | COCO-5000 (EN, 5,000 images) | UIT-ViIC (VI, 231 images)† |
|---|---|---|
| Pairs named by 1, 2, 3, 4, 5 references (φ₁..φ₅) | 2,356; 1,376; 1,287; 1,740; 3,629<!-- src: R :: sets.coco5000.E5.U.{phi_1..phi_5} --> | 61; 67; 45; 48; 208<!-- src: R :: sets.uitviic231.E5.U.{phi_1..phi_5} --> |
| Pairs in the five-reference union gold (U) | 10,388<!-- src: R :: sets.coco5000.E5.U.U --> | 429<!-- src: R :: sets.uitviic231.E5.U.U --> |
| Ĉ₅: upper bound on the coverage of the five-reference gold | 0.866 [0.854, 0.876]<!-- src: R :: sets.coco5000.descriptive.U.E1.C_hat_5.{point,ci95} --> | 0.951 [0.920, 0.972]<!-- src: R :: sets.uitviic231.descriptive.U.E1.C_hat_5.{point,ci95} --> |
| m̂₅: lower bound on the missing share | 0.134 [0.124, 0.146]<!-- src: R :: sets.coco5000.descriptive.U.E1.m_hat_5.{point,ci95} --> | 0.049 [0.028, 0.080]<!-- src: R :: sets.uitviic231.descriptive.U.E1.m_hat_5.{point,ci95} --> |
| Ĉ₅ restricted to labelled classes (upper bound on coverage) | 0.927 [0.918, 0.934]<!-- src: R :: sets.coco5000.descriptive.L.E1.C_hat_5.{point,ci95} --> | 0.952 [0.923, 0.972]<!-- src: R :: sets.uitviic231.descriptive.L.E1.C_hat_5.{point,ci95} --> |
| Check against labels, D_L = (L − Ŝ^L)/L | 0.332 [0.321, 0.343]: consistent (low power)<!-- src: R :: sets.coco5000.V1.{label,D_L.point,D_L.ci95} --> | 0.463 [0.427, 0.494]: consistent (low power)<!-- src: R :: sets.uitviic231.V1.{label,D_L.point,D_L.ci95} --> |
| Three-to-five-reference check, ε₃ (tolerance ±0.25) | −0.325 [−0.339, −0.312]: FAIL<!-- src: R :: sets.coco5000.V2A.{label,eps_3.point,eps_3.ci95} --> | −0.186 [−0.266, −0.080]: UNDERPOWERED<!-- src: R :: sets.uitviic231.V2A.{label,eps_3.point,eps_3.ci95} --> |
| ε₂ (descriptive) | −0.746 [−0.754, −0.737]<!-- src: R :: sets.coco5000.descriptive.U.eps.eps_2.{point,ci95} --> | −0.805 [−0.832, −0.771]<!-- src: R :: sets.uitviic231.descriptive.U.eps.eps_2.{point,ci95} --> |
| ε₄ (descriptive) | −0.101 [−0.111, −0.091]<!-- src: R :: sets.coco5000.descriptive.U.eps.eps_4.{point,ci95} --> | −0.026 [−0.098, 0.067]<!-- src: R :: sets.uitviic231.descriptive.U.eps.eps_4.{point,ci95} --> |

*Notes.*
- Pairs are (image, class) pairs in the matched COCO-80 classes; a pair is nameable if a reference names it with positive probability. Ĉ₅ is an asymptotic upper bound on coverage, and m̂₅ an asymptotic lower bound on the missing share, both under (A1).
- † UIT-ViIC: the references were written by a panel of five writers, so (A1) is a modelling assumption there and is not checked; the bound may fail if writers name different objects. Its values are approximate at this sample size (231 images).
- The check against labels can only detect a gross excess of the estimate over the labelled classes. It is reported as consistent (low power) only. On COCO-5000 this outcome was foreseeable from aggregate counts seen before the check was fixed.
- The three-to-five-reference check and the check against labels are pre-specified development checks. The number of references (three) and the tolerance were fixed before any frequency count was computed, but after the authors had seen the mean union sizes on COCO-5000 and an exploratory extrapolation of a related quantity on the same sets. They are not a blind test.
- FAIL (COCO-5000) means that the extrapolation from three to five references is not supported at the registered tolerance; only the lower-bound reading of Proposition 2 stays. UNDERPOWERED (UIT-ViIC) means that the check is not decisive at 231 images. ε₂ and ε₄ are descriptive and carry no label. The check is not evidence for the bound (S1.M.5).
- Intervals resample images and may be too narrow when the same writers serve many images.

<!-- END SUPPLEMENT TEXT -->
