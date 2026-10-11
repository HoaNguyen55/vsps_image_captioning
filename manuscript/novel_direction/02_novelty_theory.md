# 02 — Novelty check: operating-point theory (section 1 + contribution 2)

*11/10/2026. Scope: 00_DE_XUAT.md §1 and contribution 2. Venues checked on publisher/anthology pages; (preprint) = not peer-reviewed.*

## Verdicts

| Item | Verdict | One-line reason |
|---|---|---|
| (a) Trade-off = moving along a fixed ROC; only better evidence gives a Pareto gain (NP) | **Partial** | The trade-off is widely reported and BCEA (2026) already answers abstention cost with "acquire more evidence". No paper found states the ROC/NP lens explicitly for captioning, but the math is textbook. |
| (b) F1-optimal thresholding (F*/2, GFM, Jansche) applied to object mention in captioning | **None** (application), **trivial** (theory) | No captioning/VLM use found; the results are textbook. |
| (c) AUROC/calibration of object mentions, conformal mention selection, perception vs language-prior decomposition | **Partial, heavy** | Every component exists: AUROC detectors, a Bayesian prior+internal-signal combiner (HaloProbe, close to XWit's f), conformal claim filtering for LVLMs, language-prior attribution. Cross-lingual decorrelation as the decomposition tool was not found. |

## (a) The ROC / Neyman–Pearson framing

**What exists**
- The trade-off is documented: mitigation "raises precision at the expense of recall" (SPARC, [arXiv 2502.01419](https://arxiv.org/abs/2502.01419)); precision alone rewards short captions (THRONE, CVPR 2024, [arXiv 2405.05256](https://arxiv.org/abs/2405.05256)).
- Summary-Guided Decoding (Min et al.) says existing methods trade off precision and recall while its own method is "Pareto optimal". It appeared at the NeurIPS 2024 Safe GenAI workshop and later as SumGD in Findings of NAACL 2025 ([arXiv 2410.13321](https://arxiv.org/abs/2410.13321), [ACL](https://aclanthology.org/2025.findings-naacl.235/)). So "Pareto improvement" claims in this space are already made, empirically.
- **BCEA**, *Look Again Before You Abstain* (Xu et al., [arXiv 2606.16667](https://arxiv.org/abs/2606.16667), preprint 06/2026). It finds that keeping hallucination below 5% with a conformal filter means abstaining on more than 80% of claims, and it adds an "acquire more visual evidence" action. This is the operational form of "only new evidence moves the frontier", stated without ROC or NP language. **This is the closest overlap.**
- Adjacent theory, not ROC-based and not about VLMs: validity/breadth trade-offs in generation (Kalavasis et al., ALT 2026, [PMLR v313](https://proceedings.mlr.press/v313/kalavasis26a.html)) and hallucination as a thresholded binary decision (Kalai et al., OpenAI 09/2025, [blog](https://openai.com/index/why-language-models-hallucinate/)).

**What is new:** naming the implicit per-object "mention decision" and arguing that deletion, conservative decoding and precision-only DPO move along one ROC. Not found stated for captioning.

**What is wrong or overstated in §1**
1. "Most methods only move along a fixed ROC" is an empirical claim, not a theorem, and it is false in general. DPO, VCD and SumGD change the generator, so both the scores and the candidate pool change. SumGD and SPARC report Pareto gains without a new evidence source. The paper may claim this only for **post-hoc filters on a fixed candidate pool**, which is where it is true by construction. For VSPS v1/v2 it must be shown on data: plot the old operating points on the dev ROC.
2. "Errors **uncorrelated** with the old evidence" is the wrong condition. It is neither necessary nor sufficient. Pure noise is uncorrelated and adds nothing. The right condition is **conditional informativeness**: Y is not independent of W given S (see P2).
3. Recall is not a function of the ROC alone. It equals TPR times pool coverage. A filter cannot recover objects that no generator proposed. Most of XWit's recall gain must come from enlarging the pool (English witnesses), not from a better ROC. The theory has to separate these two effects (see P1′).

## (b) F1-optimal thresholding

**Verified sources**
- Lipton, Elkan, Naryanaswamy, *Optimal Thresholding of Classifiers to Maximize F1 Measure*, ECML PKDD 2014, LNCS 8725:225–239 ([DOI 10.1007/978-3-662-44851-9_15](https://doi.org/10.1007/978-3-662-44851-9_15), [arXiv 1402.1892](https://arxiv.org/abs/1402.1892)). For calibrated scores the optimal threshold is F*/2. An uninformative classifier should predict all positive. Arxiv spells the third author "Narayanaswamy", Springer "Naryanaswamy".
- Dembczyński, Waegeman, Cheng, Hüllermeier, *An Exact Algorithm for F-Measure Maximization*, NIPS 2011, pp. 1404–1412 ([proceedings](https://papers.nips.cc/paper/4389-an-exact-algorithm-for-f-measure-maximization)). GFM needs O(m²) parameters and no independence assumption. Extended in Waegeman et al., JMLR 2014 ([arXiv 1310.4849](https://arxiv.org/abs/1310.4849)).
- Jansche, *A Maximum Expected Utility Framework for Binary Sequence Labeling*, ACL 2007, pp. 736–743 ([P07-1093](https://aclanthology.org/P07-1093/)). Gives maximum-expected-F decoding.

**Application to captioning/VLM:** none found. Per-class F1 thresholding exists for multi-label image tagging, but it is not about hallucination or generation. **Verdict: no overlap, but low novelty.** Present it as a corollary that explains the empirical results, not as a contribution. Two caveats:
- F*/2 is for **corpus-level (micro) F1** with calibrated, separable decisions. VSPS reports per-image F1 averaged (check which one). For that metric the optimal set is not a threshold in general, and GFM/Jansche is the correct reference.
- It needs a **calibrated** posterior. The Vintern logit verifier is calibrated to K=5 agreement levels, not to gold existence. So calibration against gold must be measured (ECE on the 300-image gold set) before the rule is applied.

## (c) Mention confidence, conformal selection, hallucination sources

**Object-mention detection with AUROC and calibration**
- MetaToken (Fieback et al.), VISAPP 2025 ([arXiv 2405.19186](https://arxiv.org/abs/2405.19186)): a token-level object-hallucination classifier with AUROC up to 92.1% and ECE 0.8–2.0%.
- **HaloProbe** (Zohrabi, …, A. & M. Rohrbach), ICML 2026 ([arXiv 2604.06165](https://arxiv.org/abs/2604.06165)). A Bayesian combination of an external prior (object occurrence, position, repetition) with internal decoding evidence into a token-level hallucination posterior, used to re-score decoding. **This is structurally the same as XWit contribution 3**: f(witnesses, verifier logit, co-occurrence prior). The difference is that XWit's main evidence is cross-lingual witnesses. Cite it and compare against it.
- EAZY, *Hallucinatory Image Tokens* (Che et al.), ICCV 2025 ([supp.](https://openaccess.thecvf.com/content/ICCV2025/supplemental/Che_Hallucinatory_Image_Tokens_ICCV_2025_supplemental.pdf)): reports ROC-AUC and PR-AUC for object hallucination detection.
- LURE (Zhou et al.), ICLR 2024 ([arXiv 2310.00754](https://arxiv.org/abs/2310.00754)): attributes hallucination to co-occurrence, uncertainty and position.

**Conformal and selective generation**
- Mohri & Hashimoto, *Language Models with Conformal Factuality Guarantees*, ICML 2024, PMLR 235:36029–36047 ([link](https://proceedings.mlr.press/v235/mohri24a.html)).
- Lee, Kim, Kim, Park, *Selective Generation for Controllable Language Models*, NeurIPS 2024 spotlight ([link](https://proceedings.neurips.cc/paper_files/paper/2024/hash/5a6815122f533193a022cbc41786c1cc-Abstract.html)): FDR control with respect to entailment.
- **ConfLVLM** (Li et al.), *Towards Statistical Factuality Guarantee for LVLMs*, EMNLP 2025 ([2025.emnlp-main.576](https://aclanthology.org/2025.emnlp-main.576)): conformal claim filtering for LVLM descriptions. On LLaVA-1.5 scene descriptions, claim error drops from 87.8% to 10.0%.
- BCEA (above). It also cites CAP and CEBC; these were not verified individually.
- *Implication:* guaranteed "precision ≥ p₀" mention selection is already done. Do not claim it; use split-conformal calibration as a tool or leave guarantees out.

**Language prior vs perception**
- VCD (Leng et al.), CVPR 2024 ([CVF](https://openaccess.thecvf.com/content/CVPR2024/html/Leng_Mitigating_Object_Hallucinations_in_Large_Vision-Language_Models_through_Visual_Contrastive_CVPR_2024_paper.html)): blames statistical bias and unimodal language priors.
- OPERA (Huang et al.), CVPR 2024 Highlight ([CVF](https://openaccess.thecvf.com/content/CVPR2024/html/Huang_OPERA_Alleviating_Hallucination_in_Multi-Modal_Large_Language_Models_via_Over-Trust_CVPR_2024_paper.html)): over-trust in summary tokens.
- Visual attention sink (Kang et al.), ICLR 2025 ([arXiv 2503.03321](https://arxiv.org/abs/2503.03321)).
- SumGD (above): reliance on the language prior grows with sequence length.
- NOPE (Lovenia et al.), ALVR workshop 2024 ([2024.alvr-1.4](https://aclanthology.org/2024.alvr-1.4)): a negative-presence VQA benchmark. It measures hallucination but does not decompose it.
- Bai et al., MLLM hallucination survey ([arXiv 2404.18930](https://arxiv.org/abs/2404.18930), preprint): a taxonomy of causes (data/model/training/inference). Its perception-vs-prior split was not checked.

**Cross-lingual work**
- CLAIM, reported as ACL 2025 (anthology page not individually confirmed): non-English queries hallucinate more; fixed by cross-lingual attention intervention.
- MHR ([arXiv 2408.00550](https://arxiv.org/abs/2408.00550), preprint): multilingual hallucination removal via multi-response preference data.

Neither uses cross-lingual **agreement** as evidence or measures cross-lingual error correlation: the only unscooped part of (c) found.

## The strongest defensible formal statement

**Setup.**
- For image x, let C(x) be the **union candidate pool** of object classes proposed by any source (VSPS, each language witness), and G(x) the gold set.
- Each candidate c has label Y = 1[c ∈ G(x)] and evidence (S, W): S is the old VSPS score, W is the new witness or verifier features.
- A candidate never proposed by a source gets that source's minimum score. So a source's pool ceiling shows up as an ROC truncated at (f_max, T_max).
- Let π = P(Y=1 | candidate) and κ = |C ∩ G| / |G| (pool coverage, fixed once the pool is fixed).
- A rule "mention iff score ≥ t" gives (FPR f, TPR T). Corpus micro precision is P = πT / (πT + (1−π)f), and recall is R = κT.

**P1 (local NP dominance).** Fix p₀ ∈ (π, 1) and let k = (1−π)p₀ / (π(1−p₀)). Then "P ≥ p₀" is equivalent to "T ≥ k·f", a ray through the origin in ROC space. Let (f₀, T₀) be the old operating point with P ≥ p₀. If the new score's ROC (randomised thresholds allowed) passes weakly above (f₀, T₀), meaning some new point has f ≤ f₀ and T ≥ T₀, then there is a new threshold with P ≥ p₀ and R ≥ R₀. If it passes strictly above, then R > R₀.
*Proof:* about two lines. A point with f ≤ f₀ and T ≥ T₀ satisfies T ≥ T₀ ≥ k·f₀ ≥ k·f.
*Honest assessment:* **trivial.** It is the NP lemma plus the geometry of a precision iso-line. Its value is that it turns H3 into a precise, testable condition: local dominance at VSPS's own operating point, with a bootstrap band. Global dominance is not needed. State it as a lemma in the method section, not as a contribution.

**P1′ (where recall gain comes from).** On the union pool, R_new − R_old = κ(T_new − T_old). Witnesses in other languages that propose objects VSPS never proposed show up as extra TPR above VSPS's truncation level T_max^old. In this form the "borrow recall from English" claim is just P1 on the union pool. Not stating it this way is the main way the paper could be **wrong**: comparing ROCs computed on different pools (different π) is invalid.

**P2 (when new evidence helps; the non-trivial part).** Let Λ(s, w) be the likelihood ratio p(s, w | Y=1) / p(s, w | Y=0), or equivalently the posterior q(s, w) = P(Y=1 | s, w).
- (i) The ROC of Λ dominates the ROC of S everywhere. Proof: any test on S is a test on (S, W), and by NP the LR test is most powerful at every size.
- (ii) Dominance is strict at size α if and only if W is informative about Y given S on the relevant region, i.e. Y is not independent of W given S. When W is independent of Y given S, the ROCs coincide.
This replaces the proposal's "uncorrelated errors" with the correct condition. It also makes H1 (low ρ) a *heuristic* for H3, not a sufficient condition. A logistic f estimates q only if it is well specified, so in practice (i) holds approximately. Report the dev ROC, not the theorem, as the evidence.

**P3 (F1 corollary, explains "strict verifiers lose F1").** Assume micro-F1 over the corpus, a calibrated posterior q, and many candidates. Then the F1-optimal set is {q ≥ F*/2} (Lipton et al. 2014). Since F* ≤ 1, the optimal cut is at most 0.5. Any filter that deletes candidates with q in [F*/2, t) lowers expected F1 compared with the optimal cut, and the loss grows with the posterior mass in that band. Deleting nothing (the zero-shot point, f = T = 1 on its own pool) beats a strict verifier whenever the strict verifier's deletions are concentrated above F*/2.
*Where this would be wrong:*
- if F1 is averaged per image: then use GFM/Jansche, and the optimum need not be a threshold;
- if q is the K=5 agreement probability rather than P(gold): measure calibration on gold first;
- if "zero-shot" means a different generator: then it is not a point on the same ROC, and P3 says nothing about it.

**Do not claim:**
- a theorem that existing methods only slide along the ROC (that is empirical, and false for decoding/DPO in general);
- "Pareto improvement is *only* possible via new evidence" (false: a better generator also changes the pool and the curve);
- that low ρ implies better ROC (wrong; P2(ii) is the condition).

## Recommendation

- Shrink contribution 2 to a half-page analysis lens (P1/P1′ lemma, P2 proposition, P3 corollary); do not sell it as theory, since P1 and P3 are textbook.
- Position explicitly against BCEA and HaloProbe. For a guarantee, use split-conformal thresholding (Mohri & Hashimoto, ConfLVLM).
- The genuinely open piece is contribution 1 (cross-lingual error correlation).
