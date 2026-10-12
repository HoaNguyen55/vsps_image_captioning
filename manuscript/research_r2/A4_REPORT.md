# A4: Object precision / CHAIR under incomplete multi-reference gold — a selection-aware capture–recapture correction, validated with existing instance labels

Research agent A4 (round 2), 2026-10-12. Everything below was produced on CPU from existing data. No new labels were made, and no AI-made label is used as evidence.

Code and outputs are in `research_r2/A4/` (§9). Tables quoted below are copied from `A4/out/*.txt`.

---------------------------------------------------------------------------------------------------
## 0. Bottom line

1. **One idea survives, in narrowed form: IFCR (imitator-family capture–recapture precision).**
   - Reference precision, and CHAIR_i = 100 − P, can be corrected for reference incompleteness **without any instance label**, provided the system picks objects like an annotator. "Like an annotator" means its selection is a mixture of three annotator-imitator selections: consensus-of-2, single, or union-of-2.
   - With A = 5 annotators per image and K = 3 scoring references, this family is exactly what is identifiable (Prop. 1).
   - A label-free parametric-bootstrap fit test flags systems outside the family. For those, only a bracket is identified: [IFCR, instance-calibrated inverse propensity]. The upper end is a bound under monotone selection (Prop. 2) and needs instance labels.

2. **Validation against COCO-2014 instance gold.** Truth is instance ∪ scoring references, the frozen protocol of `score_coco_probe.py`.
   - Annotator-imitating systems (annotators and fused annotator pairs) are corrected to within ±0.6 on COCO (Ucal). On UIT-ViIC the errors are −0.2…−3.9 (Ucal) and −0.3…−3.0 (label-free). Raw reference precision is off by −5 to −18.5.
   - VLM short captions and caption prefixes (Vietnamese Qwen2.5-VL outputs on COCO; GPT-4V first 1–4 sentences) are corrected to within about 1–3 points.
   - Zero-shot, VCD and GPT-4V full detailed captions fail the fit test at p < 0.001 and are bracketed; the bracket contains the truth.
   - The old-VSPS detailed captions are flagged only weakly (p = .04) and keep a −4 (label-free) to −6 (Ucal) under-correction.
   - On COCO-5000 (24 systems), mean absolute error falls from 11.6 [11.3, 12.0] (raw) to 1.9 [1.7, 2.4] with the instance-calibrated tilt.

3. **The trap ("a caption system is not an annotator") is real and sits in a specific place.**
   - VLMs depart from annotators on low-propensity clutter classes: chair, cup, bowl, bottle, spoon, handbag.
   - References carry no information exactly there (Link 2003 non-identifiability).
   - So any reference-only correction is a *lower* bracket for detailed VLM captions.
   - Plain class-level inverse-propensity weighting (Jain et al. KDD 2016, PSP@k) is the *upper* bracket. It over-corrects annotator-like systems by +3 to +11.

4. **Calibrated propensities do not transfer across languages.** Calibrating on English COCO references gives −6 to −9 points of error on Vietnamese UIT-ViIC pairs, and the fit test notices. Use label-free components from the target dataset's own references.

5. **KTVIC** (no instance labels). Naming variants are merged first, with A7's lexical layer; IFCR then runs label-free.
   - fuse2-short − P1-short: −2.7 [−4.9, −0.6] → **−1.6 [−3.7, +1.0]**, no longer significant.
   - fuse2-detailed − P1-short: −12.7 → −10.0 [−12.1, −7.0]. Only ≈2.7 points of the gap are identifiable annotator-like reference incompleteness.
   - fuse2-detailed fails the fit test (pooled p = 0.005), so 80.0 is a lower bracket on its precision.
   - The deciding experiment is the queued UIT-ViIC in-domain P1/fuse2 run scored with COCO instance gold. It is also IFCR's kill test (§6).

---------------------------------------------------------------------------------------------------
## 1. Question and setting

Reference-derived object precision, and CHAIR when only references exist (as on KTVIC), counts every unmentioned-but-present object as a hallucination. This penalises high-coverage captions.

The A4 question has three parts:
- (1) Estimate mention propensities from data that has both captions and instances: UIT-ViIC Vietnamese captions, COCO Karpathy English captions, COCO instances.
- (2) Correct reference precision with them: inverse propensity, or capture–recapture / occupancy / Good–Turing ideas.
- (3) Validate the correction against instance-gold precision across systems, then transfer it to KTVIC.

**Truth** is the frozen protocol gold: COCO instance classes ∪ the classes the K scoring references name. With this truth, references never name an absent class, so every hallucination lands in the "named by 0 references" cell. That turns the problem into capture–recapture with a contaminated zero cell.

**Matchers** are the repo's, including the longest-span-first fix:
- Vietnamese: `score_coco_probe.vi_classes` over `coco80_vi.json`.
- English: `en_classes` with Rohrbach's synonyms.

---------------------------------------------------------------------------------------------------
## 2. Literature: closest work, mechanisms, numbers

Starred (*) entries were read in full text, by me or by two literature sub-agents. Raw texts are in `A4/lit_raw*`.

| Work | Mechanism | Incompleteness handling / numbers | Relation to A4 |
|---|---|---|---|
| *Rohrbach et al. EMNLP 2018 (1809.02156), CHAIR | Gold = COCO segmentation ∪ objects in the 5 references (80 classes + synonyms) | Says humans "will not mention all objects … using only … reference captions leads to higher hallucination (and practically incorrect) rates". No numbers, no correction | Known qualitatively. Nothing exists for reference-only settings (KTVIC, Vietnamese) |
| *Misra, Zitnick, Mitchell, Girshick CVPR 2016 (1512.06974) | h(y\|I) = Σ_j r(y\|z=j,I)·v(z=j\|I) (relevance × visual presence) | Classifier training only. 73 COCO classes: mAP 63.7→66.8 (vs 76.3 with true labels). The most under-reported object is mentioned "roughly half as much as it appears". The 5 references are collapsed to their union | Closest model of reporting bias. It never corrects a metric and ignores per-annotator counts |
| Berg et al. CVPR 2012; Spain & Perona IJCV 2011 | P(mentioned\|present) per category (horse .99 … chair/bottle .26); importance = P(named first) from an urn model over 25 lists | Category predicts mention better than size | Empirical basis for "salience" |
| *Jain, Prabhu & Varma KDD 2016 | **PSP@k = (1/k)Σ y_l/p_l**, unbiased for P@k when propensity is constant per label. p_l = 1/(1+C e^{−A log(N_l+B)}) | An existing propensity-corrected *evaluation* metric, in extreme classification | Our `ipw0` is this estimator with instance-calibrated class propensities. It over-corrects annotator-like systems by +3…+11 (§5) |
| *Schultheis et al. KDD 2022 (2207.13186) | Critique of PSP | Instance-dependent propensities break unbiasedness | Our pilot shows this failure concretely for captions |
| *Elkan & Noto KDD 2008; *Bekker & Davis (1809.03207, 1811.04820) | SCAR c = P(s=1\|y=1); SAR propensity e(x) | Weights must condition on the selection attributes | Here the selection attribute is the system's own salience preference, identified from its referenced profile |
| *Chao 1987 (Biometrics 43:783); *Link 2003 (Biometrics 59:1123); Darroch et al. 1993; Dorazio & Royle 2003 | Capture–recapture with heterogeneous catchability: lower bound ((K−1)/K)f1²/(2f2); Rasch multiple-systems estimation | Population size is non-identifiable under heterogeneity; different mixtures fit equally well | We apply capture–recapture to the **evaluated system as one more occasion** with a contaminated zero cell, and restrict its selection to an identifiable family. Chao's bound is far too loose (§5) |
| *MacKenzie et al. 2002; Royle & Nichols 2003; Royle & Link 2006; Miller et al. 2011; Chambert et al. 2015/2018 | Occupancy with imperfect detection; p = 1−(1−r)^N; false positives; classifier detections plus known-truth anchors | Known-truth units restore identifiability | Our instance-calibrated salience-blind component plays the "known truth" role. It is the only part that needs labels |
| Buckley & Voorhees SIGIR 2004; Yilmaz & Aslam CIKM 2006; *Büttcher et al. SIGIR 2007 (10.1145/1277741.1277755); *Webber & Park SIGIR 2009 (10.1145/1571941.1572018); Lipani et al. ECIR 2016 | IR evaluation with incomplete or pooled judgments; pool-bias score adjustment | One binary judgment per document; correction by regression or leave-one-run-out | Closest cross-field analogue of correcting a new system's precision. They have no replicate (K-annotator) structure, which is what our identification uses |
| *RePOPE (2504.15707) | Two annotators re-label POPE | "No" questions 1.7% wrong + 4.3% ambiguous; "yes" questions 9.3% wrong + 13.8% ambiguous; rankings change | Instance gold is imperfect too. Fixed by relabelling, no estimator |
| *THRONE CVPR 2024 (2405.05256) | 9 FLAN-T5 judges, COCO/Objects365 instance gold | Assumes COCO image-level exhaustiveness (~99%). Oracle: THRONE 96% vs CHAIR 91% | No correction |
| *ALOHa NAACL 2024 (2404.02904) | LLM-extracted objects + references + DETR; Hungarian S-BERT matching | HAT localisation accuracy 20.3 vs CHAIR_s 6.7 | Fixes incompleteness with a detector and an LLM |
| *AMBER (2311.07397); CAPTURE (2405.19092); DCScore (2503.07906); HallE-Control (2310.01779); OpenCHAIR (2312.03631) | Dense annotation, scene-graph matching, GPT-4o unit checks, LLM judges | DCScore adds verified-correct non-reference units to the denominator (Pearson .6151→.6605) | All relabel or use LLM/VLM checks; none estimates incompleteness |
| *Do More Details … (2406.12663) | Manual check of CHAIR-flagged LLaVA-1.5 captions; CLIP-P/R on Visual Genome regions | ">55% of these identified hallucinations are unjustified" | Matches our measurement (§4) |
| *Penquitt et al. (2609.21822, Sep 2026) | COCO val re-annotation | +40% instances; missed-object rate 13.1%→6.1% | Instance gold is incomplete at instance level; class-level presence much less so |
| *Ye et al. CVPR 2025 (2310.14356) | Multilingual caption sets | Multilingual human sets name 46.0% more objects | Mention propensity depends on language, consistent with our cross-language transfer failure |
| *ECCV Caption (2204.03359) | Verified false negatives in COCO retrieval | Original pairs cover 21.1% / 13.8% of verified positives | Same phenomenon, retrieval side |
| Liu Chen, Research Square rs-10639224 (Aug 2026) | Title only: capture–recapture on reference networks "rescales, but rarely reorders" gene-regulatory-network benchmarks | Abstract not retrievable (UNVERIFIED) | Cross-field precedent. Our COCO result also shows large rescaling and modest re-ranking |

### Scooping searches

The session's WebSearch budget was exhausted, so searches went through public scholarly APIs. Queries and hits are in `A4/scoop/`.

- **arXiv API, 14 boolean queries:**
  - capture(-)recapture × {caption, hallucination, annotation, annotators, missing labels};
  - reporting bias × {hallucination, CHAIR, caption evaluation};
  - propensity × hallucination × {caption, object};
  - CHAIR × {incomplete, missing objects, unannotated};
  - unseen species × {image, annotation, labels};
  - occupancy model × {annotation, labels, classifier};
  - positive-unlabeled × evaluation × {caption, hallucination, VLM};
  - object hallucination × {annotation errors, label errors, incomplete annotations};
  - mention × propensity × caption;
  - propensity-scored × precision;
  - Good-Turing × {hallucination, caption, missing mass};
  - multiple references × hallucination × precision;
  - inverse propensity × missing labels × evaluation.
- **OpenAlex, 14 queries**, same themes plus pool-bias, Lincoln–Petersen and species-richness.
- **Semantic Scholar, 12 queries.** Rate-limited; 2 returned.
- **Sub-agent scans** of ACL Anthology 2023–26 and CVF titles.

**Result: no work applies propensity weighting, capture–recapture, occupancy or unseen-species estimation to correct caption object precision or CHAIR.** The nearest work is:
- relabelling, LLM and detector fixes (RePOPE, THRONE, ALOHa, DCScore);
- manual inspection (2406.12663);
- propensity-scored precision in extreme classification (Jain 2016);
- IR pool-bias correction;
- a 2026 gene-network preprint (title only).

The defensible novelty claim is therefore "first statistical, validated correction of reference-based object precision in captioning, with an identification result and a fit test". It is **not** "first capture–recapture correction of a benchmark".

---------------------------------------------------------------------------------------------------
## 3. Theory: the evaluated system as an extra capture occasion

### Setup

- Units are (image, class) pairs.
- A present pair has latent salience p ~ G_c. Each annotator names it independently with probability p (exchangeable annotators, local independence).
- References never name absent pairs (protocol gold).
- The system names a present pair with probability w(p), its *selection function*. It may also name absent pairs (hallucinations) at any rate.
- Given p, the system's mention is independent of the references.
- For a system mention, s ∈ {0..K} is the number of the K scoring references that name it; f_s counts mentions at each s.

Then:

    E f_s = T·π_w(s)  for s >= 1,   with  π_w(s) = E_G[w(p) Bin(s;K,p)] / E_G[w(p)];
    hallucinations only add to f_0;
    true precision = (Σ_{s>=1} f_s + T·π_w(0)) / N.

### Proposition 1 (identification)

Let w = Σ_j λ_j b_j, where each b_j is a polynomial of degree ≤ A − K. Then:
- π_{b_j}(s) is a ratio of moments of G of order ≤ A, all identified by the distribution of t, the number of the A annotators who name a pair.
- For b_j(p) = p^j (consensus of j held-out annotators) and b_j(p) = 1 − (1−p)^j (union of j), π_{b_j} is a U-statistic over annotator subsets: the multivariate-hypergeometric split of t over j held-out, K scoring and A − j − K unused references (`tilt.components`, `tilt.union_components`).
- Since b_j(0) = 0, it never uses the number of present pairs that **no** annotator names. **It is label-free.**
- λ is identified from the referenced profile f_1..f_K when the number of free weights is ≤ K − 1 and the truncated components are linearly independent.
- With A = 5 and K = 3 the basis is {consensus-2 (p²), single (p), union-2 (1−(1−p)²)}. These match the selection of a consensus caption (fuse2-short), P1 and a fusion of 2 captions (fuse2-detailed).
- Only components with b(0) > 0, such as salience-blind w ≡ 1, need the count of never-named present pairs, i.e., instance labels.

`python tilt.py` checks this:
- `_check_identification`: union and consensus components equal the exact tilted binomial mixtures to within 0.004, and are invariant to the zero count.
- `_check`: a simulated system with λ = 0.6 is recovered as 0.60, with P̂ 75.2 vs true 75.0 (raw 63.7).

### Proposition 2 (non-identification; upper bracket)

- Without restricting w, the referenced profile is compatible with any amount of true mass on pairs with p → 0, because those pairs only add to f_0 (Link 2003).
- If w is non-decreasing in p, write w = ∫1{p ≥ u}dμ(u). The zero-cell odds of the step at u, E[(1−p)^K; p ≥ u] / E[1−(1−p)^K; p ≥ u], are non-increasing in u. The mixture's odds are a weighted average of these, so they are at most the u = 0 odds, which are the salience-blind odds.
- Hence **class-level IPW with instance-calibrated propensities (`ipw0`, the PSP form) is an upper bound under monotone selection.**
- Empirically it holds to within 1–2 points of calibration noise. The exception is the UIT-ViIC synthetic detector, where IPW is unstable for near-zero propensities (§5).

### Estimators

- `raw`: precision against K references.
- `ipw0`: salience-blind (Jain-style class IPW; instance-calibrated).
- `U1`: single-annotator imitator, label-free.
- `Ufit`: imitator family, label-free. Components come from the *evaluation* images' own 5 references.
- `Ucal`: imitator family with instance-calibrated components (calibration sets: COCO Karpathy train+restval; UIT-ViIC train). Reference-only pairs (named, no instance) count only when a scoring reference names them, as in the truth.
- `tilt`: `Ucal` plus the instance-calibrated salience-blind component. `LR` = 2(ll_tilt − ll_Ucal).
- `chao1`: Chao's lower bound on the system's pooled profile.

All K-reference quantities are averaged over the 5 cyclic reference subsets. Classes are shrunk towards the pooled profile with 20 pseudo-pairs; varying this from 2 to 100 changes COCO MAE by ≤ 0.3. The fit uses a coarse-to-fine search over the simplex, within 0.16 points of an exhaustive grid.

### Fit test (label-free, `gof.py`)

1. Fit `Ufit`.
2. Simulate f_c(1..K) ~ Multinomial(F_c, fitted shape_c), refit, and recompute G per class and G pooled over bins.
3. The p-value is the share of 100–200 simulations at least as extreme as the observed G.

---------------------------------------------------------------------------------------------------
## 4. Pilot data and systems (existing data only)

### COCO Karpathy test, 5,000 images, 5 English references

- **Vietnamese captions** from `data/results/coco5000` and `coco5000_vcd`: zero-shot short/detailed, old VSPS ("distill") short/detailed, VCD detailed.
- **Prefix systems:** their first 1 and first 2 sentences.
- **Humans:** English annotator j against the other annotators; the union of annotators (a, a+1) against the other 3.
- **Synthetic detectors:** all instance classes; instance classes with largest box > 2%; all classes plus one random absent class in 50% of images.

### UIT-ViIC val+test, 1,155 images

Each image has 5 Vietnamese references, 5 English Karpathy references (every UIT-ViIC image is a COCO-2014 image) and COCO instances.
- Vietnamese annotator j, and Vietnamese pairs.
- English annotator j scored against the Vietnamese references: a cross-lingual "foreign" system.
- The union of the 5 English captions.
- A synthetic detector.

### ShareGPT4V

`Lin-Chen/ShareGPT4V`, `sharegpt4v_instruct_gpt4-vision_cap100k.json`, 128 MB, downloaded to `A4/dl_sharegpt4v/`. It has 50,012 COCO train2017 images with GPT-4V detailed captions of about 157 words.
- Prefix systems: 1, 2, 3, 4 sentences and the full caption.
- 2 cross-fitted folds of 8,000 images each, calibrated on the other image-id parity.

### KTVIC test, 558 images

The paper's systems (`data/results/*.preds.json`), plus annotators and annotator pairs, at three levels:
- `exact`: the paper's rule, `rescap.chair.objects_in`.
- `seg`: A7's segmentation-fixed `naming.extract`.
- `coarse`: `seg` plus naming variants merged into one referent class: person nouns → người, A7's synonym canon (`canon`) and near-synonym groups (`NEAR`), toà/dãy nhà → nhà, nón lá → mũ. These lexical pairs are those A7 validated with cross-annotator alternation φ ≥ 0.5. They are lexical resources, not image labels.

Components are label-free, from the KTVIC test references.

### Raw facts

- **COCO train, present pairs, K = 5 English references:** S | present = {0: 39.0%, 1: 9.5%, 2: 7.5%, 3: 7.9%, 4: 11.1%, 5: 25.0%}. The distribution is U-shaped: 39% of present (image, class) pairs are named by none of 5 annotators.
- **Per-class q5 = P(≥1 of 5 names | present):** handbag .037, potted plant .051, backpack .092, cup .150 … giraffe .995.
- **Reference-only pairs** are 9.6% of protocol-present pairs.
- **Reference-false mentions that are instance-present**, as a share of each system's reference-false mentions:
  - zero-shot detailed 47%, VCD detailed 51%, GPT-4V full 42%;
  - English annotators against the other 4: 57–61%;
  - Vietnamese annotators on UIT-ViIC: 97–100%;
  - English annotators against Vietnamese references: 97–98%.

---------------------------------------------------------------------------------------------------
## 5. Results

### 5.1 COCO-5000, K = 3 English references, 24 systems, B = 200 image bootstrap (`out/coco_k3_b200.txt`)

Cells are error vs instance-gold precision, with the [95% CI] of the error.

```
system                 m/img truth |  raw           ipw0          Ufit (label-free)  Ucal          tilt          fit-test p (class/pool)
distill-detailed        1.40  88.3 | -11.9[-13,-11]  +9.0[+8,+9]   -4.0[-5,-4]   -6.0[-7,-5]   -3.5[-6,-1]   .040/.090
distill-short           0.84  93.6 |  -6.2[-7,-6]    +4.5[+4,+5]   -1.4[-2,-1]   -2.5[-3,-2]   -2.5[-3,-1]   .100/.410
zeroshot-detailed       2.22  81.6 | -19.7[-20,-19] +11.6[+10,+12]-11.1[-12,-10]-13.9[-15,-13]  +9.2[+4,+11]  .000/.000  FLAG
zeroshot-short          1.19  93.5 |  -7.1[-8,-7]    +5.6[+5,+6]   +0.9[-0,+1]   -1.5[-2,-1]   +2.4[-1,+4]   .090/.580
vcd-detailed            2.06  83.5 | -20.5[-21,-20] +11.2[+10,+11]-11.7[-13,-11]-14.6[-15,-14]  +9.0[+4,+10]  .000/.000  FLAG
zeroshot-det[:1s]       0.92  94.4 |  -4.4[-5,-4]    +4.5[+4,+5]   -0.5[-1,-0]   -1.8[-2,-1]   +0.4[-2,+1]   .080/.080
zeroshot-det[:2s]       1.26  90.6 |  -7.6[-8,-7]    +6.5[+6,+7]   -0.5[-1,-0]   -2.7[-3,-2]   +0.2[-3,+3]   .400/.430
vcd-det[:1s]            0.86  95.2 |  -3.9[-4,-4]    +4.0[+3,+4]   +0.5[-0,+1]   -1.0[-2,-1]   +0.3[-1,+1]   .040/.660
vcd-det[:2s]            1.17  91.1 |  -7.0[-8,-7]    +6.6[+6,+7]   +0.4[-1,+1]   -2.1[-3,-2]   +0.2[-2,+2]   .070/.650
distill-det[:1s]        1.24  89.8 |  -9.2[-10,-9]   +7.6[+7,+8]   -2.2[-3,-2]   -3.8[-5,-3]   -2.1[-4,-0]   .030/.350
distill-det[:2s]        1.39  88.3 | -11.7[-12,-11]  +9.0[+8,+10]  -3.9[-5,-3]   -5.8[-7,-5]   -3.3[-6,-1]   .020/.090
SYN det-all             2.86 100.0 | -42.8[-44,-42]  -1.9[-5,-2] -34.5[-35,-33]-36.5[-37,-36]  -1.9[-5,-2]   .000/.000  FLAG
SYN det-big(>2%)        1.60 100.0 | -22.6[-23,-22]  -0.1[-1,-0] -12.9[-14,-12]-15.7[-17,-15]  -4.4[-8,-3]
SYN det-all+noise       3.35  85.4 | -36.5[-37,-36]  +1.5[-1,+2] -29.3[-30,-28]-31.2[-32,-30]  +1.5[-2,+2]
HUM EN 0..4 (5 systems) ~1.37 96.5-97.0 | -5.4..-6.0 (CI +-0.5) +2.9..+3.3  +1.8..+2.2   -0.1..-0.6    -0.1..-0.6    p .25-.98
HUM EN pairs (5 systems) ~1.69 94.9-95.3| -7.4..-8.2 (CI +-0.6) +4.5..+4.8  +3.0..+3.6   -0.6..+0.1    -0.6..+1.4    p .02-.72
across 24 systems:  MAE raw 11.63 [11.29,11.97] | ipw0 5.10 [4.76,5.21] | Ufit 5.83 [5.38,5.86] | Ucal 5.94 [5.83,6.49]
                    | tilt 1.89 [1.68,2.41] | chao1 9.05 [8.76,9.42]
                    Kendall tau: raw 0.570 [0.490,0.599], tilt 0.672 [0.541,0.759], ipw0 0.744 [0.577,0.759]
```

Group means of the error (`out/coco5000_k3_b0.json`):

| Group | raw | Ucal | tilt | Ufit | ipw0 |
|---|---|---|---|---|---|
| Humans | −5.7 | −0.4 | −0.3 | +2.0 | +3.1 |
| Fused human pairs | −7.9 | −0.3 | 0.0 | +3.3 | +4.6 |
| VLM short | −6.6 | −2.0 | | −0.3 | +5.1 |
| VLM prefixes | −7.3 | −2.9 | −0.7 | −1.0 | +6.4 |
| VLM detailed | −17.3 | −11.5 | +4.8 | −9.0 | +10.6 |

The label-free Ufit sits about +2 to +3 above Ucal on humans and pairs. The reason is that label-free components must treat reference-only names (no instance) as true; that is the label-free notion of truth.

**K-invariance.** From K = 2 to K = 3, corrected errors move less than 1 point; raw errors drift 3–4 points (`out/coco5000_k2_b0.json`):
- humans: Ucal −0.5 → −0.4;
- pairs: −0.8 → −0.6;
- zero-shot short: −1.9 → −1.5;
- old-VSPS detailed: −6.4 → −6.0.

### 5.2 UIT-ViIC val+test, K = 3 Vietnamese references, 17 systems, B = 200 (`out/uit_k3_b200.txt`)

- **Vietnamese annotators:** raw −12.7…−15.8 → Ufit **−0.5…−3.0** (CIs within [−6, 0]). Ucal −0.5…−3.9.
- **Vietnamese pairs (fusion of 2):** raw −15.9…−18.5 → Ufit **−0.3…−2.0**. Ucal −0.2…−3.2.
- **English annotators scored against Vietnamese references:**
  - flagged (LR 11–14, devLF 16–22);
  - raw −28.6…−29.2;
  - imitator estimates −15 (wrong);
  - **ipw0 −0.5…−1.0 (right)**, because English annotators select salience-blindly relative to Vietnamese ones;
  - tilt −3…−5.
- **Synthetic detector:** ipw0 −14.8. This is IPW instability for near-zero propensities on a 2,695-image calibration set.
- **MAE (17 systems):** raw 23.1 [21.9, 24.3]; ipw0 1.2 [1.1, 1.8]; tilt 3.8 [3.0, 6.0]. Truths cluster at 98–100, so rank correlations are uninformative here.
- **Transfer test (calibration on COCO English references, `out/uit_k3_calEN_b0.txt`):** Ucal on Vietnamese pairs is −6.2…−9.1 instead of −0.2…−3.2, and ipw0 on English annotators is −9.6 instead of −1.0. **Calibrated components do not cross languages.** Label-free components are unaffected.

### 5.3 ShareGPT4V GPT-4V captions, K = 3 English references, 2 × 8,000 images, B = 100 (`out/s4v_k3_b100.txt`)

| Prefix | raw (fold 0 / fold 1) | Ufit | Ucal |
|---|---|---|---|
| 1 sentence | −2.8 / −3.2 | +0.5 / −0.4 | −0.8 / −1.3 |
| 2 sentences | −5.0 / −5.4 | +1.8 / +1.7 | −1.1 / −1.1 |
| 3 sentences | −7.7 / −8.1 | +1.3 / +1.3 | −2.2 / −2.2 |
| 4 sentences | −10.0 / −10.3 | +0.5 / +0.5 | −3.5 / −3.5 |
| Full caption (2.45 objects/img) | −16.6 / −16.5 | | |

The full caption is flagged (LR 70–80). Its bracket is [Ucal −10.4, ipw0 +12.1] and contains the truth; tilt is +5.1 / +6.5.

### 5.4 The trap, located (`out` per-class breakdown, K = 3, Ucal)

- **Old-VSPS detailed:** −417 hidden mentions (−6.0 points), almost all in clutter classes: chair (true hidden 151, estimated 41), cup (99 vs 18), bowl (58 vs 12), bottle (43 vs 10), spoon, tie, handbag.
- **Zero-shot detailed:** −13.9 points, from person (239 vs 87), cup (170 vs 24), chair, bottle, car, book, dining table.

The systems name clutter objects in a near salience-blind way *within* these classes, where references are least informative. This is Prop. 2's non-identified region.

### 5.5 Fit-test operating characteristic (COCO, `out/gof_coco_k3.txt`; KTVIC, `out/gof_ktvic_coarse.txt`)

**COCO.**
- p < 0.001 on both statistics: only zero-shot detailed, VCD detailed and the all-instances detector, exactly the off-family systems.
- Humans: p = .25–.98. Pairs: p = .02–.72 (pooled), .17–.72 (per class).
- VLM systems with residual clutter error of 2–6 points: per-class p .02–.10. This is weak power, as non-identifiability predicts.
- **With the rule "flag if either p < .05"**, unflagged systems have |Ucal| ≤ 2.7 and |Ufit| ≤ 3.6.

**KTVIC (naming-merged, label-free).**
- P1 (gold, s43, both modes): pooled p .19–.52, unflagged.
- Humans and pairs: pooled p .045–.60.
- **Flagged:** fuse2-short .005, fuse2-detailed .005, tags-fuse2-detailed < .005, e5-detailed .015, tags-fuse2-short .02, zero-shot detailed < .001.

So the fused systems' extra mentions sit at lower reference counts than any annotator-union imitator produces.

### 5.6 KTVIC transfer: naming-merged, label-free, K = 3, B = 500 (`out/ktvic_coarse_k3_test_b500.txt`; exact level in `out/ktvic_exact_k3_test_b500.txt`)

Precision in % at K = 3; corrected values carry [95% CI].

| system | exact raw | naming-merged raw | IFCR corrected [95% CI] | fit p (pool) |
|---|---|---|---|---|
| P1-short (p1-gold) | 69.7 | 80.2 | **90.0 [86.9, 91.2]** | .32 |
| P1 seed 43, short | 70.6 | 81.2 | 90.7 [87.9, 92.0] | .23 |
| fuse2-short | 67.0 | 77.5 | 88.4 [85.3, 90.1] | .005 |
| tags-fuse2-short | 69.0 | 78.7 | 89.8 [86.6, 91.0] | .02 |
| fuse2-detailed | 58.6 | 67.5 | **80.0 [77.1, 82.2]** (lower bracket) | .005 |
| tags-fuse2-detailed | 61.1 | 70.3 | 83.1 [80.2, 84.8] | <.005 |
| e5-detailed | 57.8 | 66.6 | 79.1 [76.3, 81.2] | .015 |
| zero-shot short | 46.6 | 62.6 | 72.7 [69.6, 74.9] | .37 |
| zero-shot detailed | 28.4 | 36.4 | 43.8 [42.2, 45.4] (lower bracket) | <.001 |
| humans (mean of 5) | 79.5 | 85.4 | 95.5 (91.1–97.9) | .045–.60 |
| human pairs (mean of 5) | 72.8 | 79.2 | 92.7 (84.4–97.4) | .045–.57 |

Paired differences (same bootstrap images; naming-merged):

| Comparison | raw ΔP [95% CI] | corrected ΔP [95% CI] |
|---|---|---|
| fuse2-short − P1-short | −2.7 [−4.9, −0.6] | **−1.6 [−3.7, +1.0]** |
| tags-fuse2-short − P1-short | −1.5 [−3.7, +0.6] | −0.2 [−2.7, +1.9] |
| fuse2-detailed − P1-short | −12.7 [−15.0, −10.7] | **−10.0 [−12.1, −7.0]** |
| fuse2-detailed − P1-detailed | −12.2 [−14.5, −10.0] | −9.5 [−11.9, −6.7] |
| human pair (0+1) − human 0 | −5.8 [−7.5, −4.1] | −2.1 [−4.2, −0.6] |

On COCO, instance-gold truth for unions of two humans is also about 1.8 below single humans, so the −2.1 is plausible rather than a bias. At the exact level: fuse2-detailed − P1-short −11.2 → −9.7 [−12.1, −6.4]; fuse2-short − P1-short −2.7 → −2.0 [−4.5, +1.1].

**Decomposition of each system's reference-false share at K = 3** (exact → naming-merged → corrected):

| System | Naming / segmentation | Identifiable annotator-like incompleteness | Residual (hallucination or non-identified clutter) |
|---|---|---|---|
| P1-short (30.3 points reference-false) | 10.5 | 9.8 | 10.0 |
| fuse2-detailed (41.4) | 8.9 | 12.5 | 20.0 (an upper bound, since flagged) |
| Single human | 5.9 | 10.1 | 4.5 |
| Human pair | 6.4 | 13.5 | 7.3 |

So at matched selection, the residual exceeds the human one by 5.5 points for P1-short and by ≤ 12.7 points for fuse2-detailed.

**KTVIC-specific caveats.**
- Components built from KTVIC *train* references fit worse, even for humans: devLF up to 15.7. Use test-reference self-calibration.
- KTVIC's 5 captions are not exchangeable. The caption at index 4 is confirmed by the other four only 76.8% of the time, vs 85–90% for the others; KTVIC used 3 annotators plus 2 reviewers.
- Exact-match counting without A7's naming merge mixes naming variation into the zero cell.

---------------------------------------------------------------------------------------------------
## 6. The surviving idea

### IFCR: imitator-family capture–recapture precision

**What it is.** A label-free, identification-guaranteed correction of reference-based object precision and CHAIR_i for multi-reference caption datasets, with a fit test that reports when references cannot decide.

**Mechanism.**
1. The K references are capture occasions. The system is one more occasion whose zero cell holds all hallucinations.
2. The system's referenced profile (how many references confirm each mention) is fitted by a mixture of annotator-imitator selections: consensus-2, single and union-2. Their components are U-statistics over held-out annotators, so they are label-free and identified (Prop. 1).
3. The zero cell is extrapolated to give corrected precision with an image-bootstrap CI.
4. A parametric-bootstrap fit test flags systems whose mentions sit where annotators almost never name objects. For those only the bracket [IFCR, instance-calibrated class IPW] is identified (Prop. 2).
5. On KTVIC it runs after A7's naming merge.

**Closest prior and delta.**
- **Jain, Prabhu & Varma KDD 2016 (PSP@k)** is the only existing propensity-corrected evaluation metric. It uses class-level IPW in extreme classification and over-corrects annotator-like captioners by +3 to +11 on COCO, the SAR failure Schultheis et al. KDD 2022 predicted. The delta has four parts:
  - the system's own selection is identified from the replicate-reference profile;
  - Props 1–2 (what is and is not identifiable for given A and K, and which components need labels);
  - a fit test;
  - validation against instance gold in two languages, including the cross-language transfer failure.
- **Capture–recapture and occupancy** (Chao 1987; Link 2003; Chambert 2015) are applied to *the evaluated system's precision*, with a contaminated zero cell and a restricted, identified selection family, not to population size.
- **In captioning** there are only relabelling, LLM or detector fixes (RePOPE, THRONE, ALOHa, DCScore), manual audits (2406.12663), and Rohrbach's instance ∪ reference gold.

**Pilot evidence** (§5). Human and fused-human systems are corrected to within ±0.6 on COCO (Ucal; +1.8…+3.6 label-free) and to −0.2…−3.9 on UIT-ViIC (Ucal; −0.3…−3.0 label-free); raw errors are −5…−18.5. VLM short captions and prefixes are within about 1–3. Zero-shot, VCD and GPT-4V full detailed captions are flagged at p < .001 and bracketed, and the brackets contain the truth. Old-VSPS detailed is only weakly flagged (p = .04) with a −4…−6 residual. COCO MAE over 24 systems is 11.6 → 1.9 (tilt).

**Use in the paper.**
- One methods paragraph plus an appendix (Props 1–2, fit test).
- A KTVIC table: raw (K = 5), naming-merged, IFCR with CI and fit p.
- A validation table on UIT-ViIC / COCO with instance gold.
- An honest statement: references can identify only about 2.7 of the 12.7-point precision gap of fuse2-detailed; the rest must be settled with instance gold, on UIT-ViIC and COCO.

**GPU-h.** None for the method. The kill test needs P1 and fuse2 captions on UIT-ViIC val+test (jobs 59a/59b are already queued), plus optionally COCO-5000 (COCO transfer queued). If they must be regenerated: ≤ 1.5 GPU-h for UIT-ViIC and ≤ 4 GPU-h for COCO.

**Kill criterion (pre-registered).** Run on UIT-ViIC val+test, scored with COCO instance ∪ reference gold, for P1-short, P1-detailed, fuse2-short and fuse2-detailed.
- (a) Every system that passes the fit test (both p ≥ .05) must have |IFCR (label-free, components from UIT-ViIC references) − truth| ≤ 2.5, with the bootstrap CI overlapping that band.
- (b) The corrected ΔP(fuse2 − P1) must lie inside the instance-gold ΔP's 95% CI.
- (c) For flagged systems, [IFCR, ipw0 calibrated on UIT-ViIC train] must contain the truth.

Kill IFCR as a precision estimator if (a) fails for 2 or more systems, or (b) fails. In that case keep only the naming merge plus the bracket as a reporting device.

**Confidence.**
- About 0.6 that it passes for the short-mode systems.
- About 0.35 that fuse2-detailed passes the fit test. It is likely flagged, giving a bracket only, as on KTVIC.
- About 0.5 that reviewers see it as a contribution rather than a sanity appendix. It is strongest as "a principled, validated way to state how much of a precision drop references can and cannot explain".

---------------------------------------------------------------------------------------------------
## 7. What did not survive (well-founded negatives)

1. **Class-level IPW / PSP as a general correction.** It over-corrects every annotator-like system (+3…+11 on COCO) and is unstable for near-zero propensities (UIT-ViIC detector −14.8). It is valid only as an upper bracket, and only for salience-blind systems.
2. **Reference-only Chao / Lincoln–Petersen.** Chao1 on the system profile recovers under 40% of the gap: COCO MAE 9.05 vs raw 11.63, and −3.3 on humans. This repeats round-1 ET3's finding for population coverage (Chao2 2.18 vs 3.19 true classes per image).
3. **Correcting detailed VLM captions from references alone.** This is not identified: brackets are about 22 points wide for zero-shot, VCD and GPT-4V full captions. That is Link (2003) in practice.
4. **Transferring instance-calibrated propensities across languages or annotator pools** (COCO English → UIT-ViIC Vietnamese) gives −6…−9 points. So "fit on COCO, apply to KTVIC for shared classes" is not supported; only label-free, in-dataset components transfer.
5. **Re-ranking.** Kendall τ across 24 COCO systems improves only from 0.57 to 0.67 (tilt) / 0.74 (ipw0). The correction mostly rescales.
6. **On KTVIC, no reference-only method can say whether fuse2-detailed's low-propensity extra mentions are real.** The fit test says they are outside the annotator family. Instance gold (UIT-ViIC in-domain; COCO) has to decide.

---------------------------------------------------------------------------------------------------
## 8. Relation to other agents and round 1

- **A7 (naming level).** 36–44% of the paper systems' reference-false mentions on KTVIC are naming-level, and about 10–12% are segmentation artefacts. All KTVIC IFCR numbers above are computed after A7's segmentation fix and naming merge (`--level coarse`); the `exact` level is reported for comparison. COCO and UIT-ViIC work at a naming-absorbed level by construction, because the 80-class matchers map woman/man → person.
- **Round-1 ET2 / ET3** (internal, unpublished):
  - ET2's propensity-amplification lemma for a truthful k-fusion imitator is the special case λ = (union-k) of Prop. 1.
  - ET3's reference-only capture–recapture failure is Prop. 2.
  - IFCR differs from both: it fits each system's selection from its referenced profile, tests the fit, and is validated against instance gold.

---------------------------------------------------------------------------------------------------
## 9. Files (`research_r2/A4/`)

| File | Contents |
|---|---|
| `prep.py`, `prep2.py` | Caches (`cache/*.pkl`): COCO-2014 per-image instance facts; English Karpathy and Vietnamese UIT-ViIC reference class sets; Vietnamese COCO-5000 system mentions, per sentence; ShareGPT4V per-sentence classes |
| `a4lib.py` | Loaders |
| `explore.py` | Raw reference P vs instance P vs protocol P for all caption sets |
| `tilt.py` | Components (power and union bases), coarse-to-fine fit, Chao1. Self-checks: `python tilt.py` |
| `pilot.py` | COCO / UIT-ViIC / ShareGPT4V validation: all estimators, image bootstrap, MAE / Kendall / Spearman |
| `gof.py` | Label-free parametric-bootstrap fit test |
| `ktvic.py` | KTVIC transfer at exact / seg / coarse levels, with paired bootstrap differences. Uses `../A7/naming.py` for seg / coarse |
| `out/` | All tables and JSON. Main files: `coco_k3_b200.txt`, `uit_k3_b200.txt`, `uit_k3_calEN_b0.txt`, `s4v_k3_b100.txt`, `gof_coco_k3.txt`, `gof_ktvic_coarse.txt`, `ktvic_coarse_k3_test_b500.txt`, `ktvic_exact_k3_test_b500.txt` |
| `scoop/` | Scooping queries and hits (`arxiv_hits.txt`, `oa_hits.txt`, `s2_hits.txt`) |
| `lit_raw/`, `lit_raw2/` | Full texts read |
| `dl_sharegpt4v/` | Downloaded ShareGPT4V caption file |

How to rerun:

```
python tilt.py
nice -n 15 python pilot.py --set coco5000 --k 3 --boot 200
nice -n 15 python pilot.py --set uitviic --k 3 --boot 200
nice -n 15 python pilot.py --set uitviic --k 3 --cal-from-en
nice -n 15 python pilot.py --set sharegpt4v --k 3 --boot 100 --max-img 8000
nice -n 15 python gof.py --set coco5000
cd /mnt/d/vsps_image_captioning && NCS_DATA=data nice -n 15 python <A4>/ktvic.py --k 3 --boot 500 --cal test --level coarse
cd /mnt/d/vsps_image_captioning && NCS_DATA=data nice -n 15 python <A4>/gof.py --set ktvic --level coarse
```
