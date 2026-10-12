## A7 summary: naming level, classifiers and compounds

I did not write `REPORT.md`: the harness blocked it because subagents may not write report files. The full report is below this summary instead. Code, raw outputs and search logs are in `/tmp/claude-1000/-mnt-d-vsps-image-captioning/755eae04-5e4c-4ce1-ab21-d4bc106761ee/scratchpad/research_r2/A7/`.

**Idea 1 (survives): NAP, an object P/R that understands naming level, segmentation and human agreement**
- **Mechanism:**
  - Fix Vietnamese extraction: tone-mark style, compounds (cửa hàng, trái cây, cổ kính), and cây/quả used as classifiers.
  - Credit synonyms, near-synonyms and more-general names only where a statistic phi, computed from training captions alone, supports them. phi measures whether two names alternate across one image's captions but never appear in the same caption.
  - Report recall per referent, naming agreement, and the gap to a held-out human.
- **Closest prior:** ManyNames v2 (COLING 2020) grades names against verified name sets, but needs 36 elicited names per boxed object. NAP gets the name sets from the 5 existing captions and handles segmentation. CHAIR merges man/woman into one class; phi shows these are separate people.
- **Pilot:**
  - Of P1-short's reference-false mentions, 43.0% [36.5, 49.8] are naming-level and 12.7% are segmentation artefacts.
  - Precision rises 77.9 → 84.4 for P1-short and 52.3 → 66.3 for zero-shot; the zero-shot−P1 gap goes from −25.7 to −18.1.
  - The fuse2−P1 precision gap stays (−3.5 [−5.9, −1.0]), and fusion's recall gain survives per referent (+6.3 [4.3, 8.4]).
  - phi recovers CHAIR's synonym classes from COCO English captions with AUROC 0.872, and UIT-ViIC's class map with 0.817.
- **GPU-h:** 0.
- **Kill criteria:** phi AUROC ≥ 0.80 on two caption sets (passed). The protocol must move a paper-level gap by more than its CI (passed). Pending: once the UIT-ViIC P1/fuse2 predictions land, naming-level mentions must be ≥ 95% instance-present under COCO labels.
- **Confidence:** high that the measurement is right; medium that reviewers will count it as a contribution.

**Idea 2 (killed): rewrite target names to the annotators' modal name, or fuse by new referents**
- In the leakage-free offline test, p1 changes by +0.14 F1 [−0.04, 0.32], fuse2 by −0.73 [−0.94, −0.54], and referent-based fusion by −0.13.
- NAP already credits the dominant naming error (a name that is too general), so there is little left for training to fix.
- It would cost about 4.3 GPU-h; not worth running.

**Key literature finding:** in ManyNames v2, 54.5% of a strong model's mismatches with the top human name are acceptable alternative names. I found no hallucination metric that derives naming distributions from the existing references.

---

# Full report: naming level, classifiers and compounds in Vietnamese object-hallucination evaluation

All numbers were computed on CPU from existing predictions and existing human captions (KTVIC, UIT-ViIC, COCO Karpathy train). I used no new labels and no GPU. 95% CIs are percentile bootstraps over images (B = 2000 unless stated); held-out-human (1v4) rows resample images together with all 5 folds.

## 0. Verdict

- **About half of what CHAIR-vi and `object_prf` call hallucination is not a wrong object.**
  - P1-short's reference-false mentions break down as 12.7% segmentation artefacts, 43.0% [36.5, 49.8] naming-level variants of an object the references do name, and 44.3% [37.8, 51.1] "other".
  - "Other" means a wrong object, or a real object no annotator named.
  - For comparison (segmentation / naming / other): fuse2 and tags_fuse2 9–13% / 36–42% / 47–55%; zero-shot 18% / 20–31% / 51–61%; a held-out human 10% / 33% / 57%.
- **Rankings stay the same; the sizes of the numbers change.**
  - Under rule R4 (segmentation fixed; synonyms, near-synonyms and hypernyms credited), precision becomes:

    | system | precision | CHAIR_i equivalent (100 − P) |
    |---|---|---|
    | P1-short | 77.9 → 84.4 | 22.1 → 15.6 |
    | fuse2-short | 75.7 → 80.9 | 24.3 → 19.1 |
    | zero-shot-short | 52.3 → 66.3 | 47.7 → 33.7 |
    | fuse2-detailed | 68.0 → 74.0 | 32.0 → 26.0 |

  - The zero-shot−P1 gap shrinks from −25.7 to −18.1. So about 30% of SFT's apparent hallucination reduction is learning the annotators' naming conventions.
  - The fuse2−P1 precision gap does not shrink: short −2.2 → −3.5, detailed −10.4 → −9.9.
  - Fusion's recall gain holds at the referent level: short +5.7 → +6.3, detailed +18.5 → +18.0.
  - fuse2-short now recalls more of the referenced objects than a held-out human: +3.2 [0.8, 5.4] (exact rule: +1.6, not significant).
  - P1's precision gap to a held-out human shrinks from 10.0 to 5.8.
- **A label-free signal for "same object, different name" works.** phi is computed from training captions only.
  - On KTVIC: median phi is 1.00 for synonym, near-synonym and group-member pairs, 0.77 for hypernym pairs, 0.07 for unrelated pairs, and −0.14 for person siblings (man/woman).
  - It recovers CHAIR's 80-class synonym list from COCO English captions with AUROC 0.872 (pairs with phi ≥ 0.9 are 94.6% same-class), and UIT-ViIC's class map with AUROC 0.817.
  - It shows where CHAIR merges different people: female~male −3.46, girl~guy −2.15, bride~groom −1.05.
  - It finds two errors in CHAIR's list: "liner" is mapped to boat and "longboard" to surfboard, but annotators use them for planes and skateboards.
- **Models name objects more generally than annotators do.**
  - Against the other 4 captions, a held-out human uses the most common name 84.7% of the time; P1-short 79.1%; zero-shot-short 70.4%.
  - For people (most common name / more general): human 74.3 / 10.7, P1 68.3 / 17.8, zero-shot 45.1 / 44.0.
- **Training-side naming changes are dead.** Offline, consensus naming adds +0.14 F1 to P1 targets and −0.73 to fused targets; referent-based fusion gives −0.13.

## 1. Pilot design

**Data and baseline.**
- Data: KTVIC test (558 images × 5 references) and train (3,769 × 5).
- Systems: `p1-gold`, `fuse2_s42`, `tags_fuse2_s42` and `zeroshot`, each in short and detailed mode, plus `p1_s43` as a seed check.
- Baseline is `object_prf`'s exact rule. All numbers reproduce the CONTEXT table.

**Two separate layers (`naming.py`, with a `_check()` self-test).**
1. **`extract()`: segmentation fixes, on top of `objects_in`.**
   - Normalise tone marks to KTVIC's old style. Zero-shot writes "tòa" in 112 of 558 detailed captions, so "tòa nhà" was read as "nhà".
   - Add a 90-entry compound table, built from a pyvi enumeration (`enum_artefacts.py`):
     - compounds that name something else: cửa hàng = shop, cửa sổ = window, trái cây / hoa quả = fruit, cổ kính = antique, cầu thang = stairs, môi trường = environment, bàn tay = hand, người ta = pronoun;
     - coordinate compounds that `objects_in` split into two objects: quần áo, giày dép, mũ nón, ô dù, tàu thuyền, nhà cửa;
     - "xe ô tô" no longer yields an extra "xe".
   - Treat cây / quả as classifiers before a noun that is not a plant / fruit (cây cầu, quả bóng). Endocentric compounds such as áo dài keep their head, as today.
2. **`relation(m, g)`: naming relations.**
   - same / synonym (16 sets) / near-synonym (7 pairs, e.g. quầy hàng ~ sạp hàng ~ cửa hàng, tàu ~ thuyền) / hypernym / hyponym, over an explicit parent map. The parent map completes the person tree: cô gái → phụ nữ, chàng trai → đàn ông, học sinh / công nhân / cặp đôi → người, bé trai / bé gái / em bé → trẻ em.
   - member: a group noun versus one of its members.
   - person sibling: a gender or age conflict, which is not a naming variant.

**The alternation statistic phi.**
- With k_a, k_b and k_ab the number of an image's n captions naming a, b, and both: phi = 1 − Σ k_ab / Σ (k_a · k_b / n).
- Only pairs with expected co-mention ≥ 5 are kept; the table is cached in `phi_train.json`.

**Decomposition order** for each reference-false mention:
1. S_pred: my corrected extractor does not produce it (a prediction-side artefact).
2. S_gold: it matches once the references are extracted correctly.
3. N_syn / N_near / N_hyper / N_hypo / N_member / N_sib_person: its most benign relation to a referenced lemma.
4. O: none of the above.

N_phi = naming-level mentions whose pair also has phi ≥ 0.5 on train.

**Matching rules.**
- R0 = today's rule.
- R1–R3 add, in turn: the segmentation fix, synonym credit, near-synonym credit.
- R4 = R3 plus hypernym credit.
- R5 = R4 plus hyponym, member and sibling credit (an upper bound).

**Recall per referent.**
- An image's reference lemmas are grouped into clusters: names linked by a naming relation and never used together in one caption.
- R_ref = clusters named at the same or a more specific level; R_ref_vague also accepts a more general name.

**Human calibration (1v4):** each reference is scored against the other 4, and every system against the same 4-caption sets.

**Offline training test (`offline_naming.py`).** Replays `human_parity`'s "common" protocol (build from 3 captions, score against the other 2). It reproduces R4_01: p1 71.8 / 52.4 / 60.6, fuse2 63.0 / 73.6 / 67.9.

## 2. Results

### 2.1 What the reference-false mentions are (% of reference-false)

| system | S_pred | S_gold | syn | near | hyper | hypo | member | sib | **naming** | N_phi | **O** |
|---|---|---|---|---|---|---|---|---|---|---|---|
| P1-short | 11.8 [7.5,16.6] | 0.9 | 3.2 | 4.1 | 23.1 [17.4,28.8] | 10.4 | 0.9 | 1.4 | **43.0** | 38.0 | **44.3** |
| fuse2-short | 11.3 | 0.4 | 2.1 | 3.5 | 16.3 | 15.9 | 2.1 | 1.8 | **41.7 [35.7,47.7]** | 33.6 | **46.6** |
| tags_fuse2-short | 12.0 | 0.8 | 2.0 | 3.6 | 16.9 | 13.7 | 2.8 | 1.2 | **40.2** | 32.5 | **47.0** |
| zero-shot-short | 18.2 [15.2,21.3] | 0.0 | 3.6 | 0.9 | 21.0 | 5.2 | 0.2 | 0.3 | **31.2 [27.5,34.8]** | 26.3 | **50.6** |
| P1-detailed | 10.0 | 0.9 | 1.4 | 4.1 | 22.2 | 13.1 | 1.4 | 1.8 | **43.9** | 37.6 | **45.2** |
| fuse2-detailed | 8.5 | 0.4 | 2.1 | 2.3 | 15.6 | 12.9 | 1.6 | 1.8 | **36.3 [32.2,40.4]** | 30.3 | **54.8 [50.6,58.9]** |
| tags_fuse2-detailed | 9.3 | 0.4 | 2.5 | 2.1 | 16.7 | 15.0 | 2.1 | 1.6 | **39.9** | 33.3 | **50.4** |
| zero-shot-detailed | 18.0 | 0.0 | 3.0 | 0.4 | 10.6 | 5.7 | 0.2 | 0.6 | **20.5** | 12.7 | **61.4** |
| held-out human | 9.1 | 0.7 | 4.0 | 3.2 | 9.8 | 13.5 | 1.7 | 1.0 | **33.2 [29.4,37.0]** | 25.2 | **57.0** |

- **Seed check:** P1 seed 43 gives naming 46.4 / 49.2% and O 42.1 / 42.2% (short / detailed), inside the CIs.
- **Typical cases:**
  - Too general: phụ nữ where the references say cô gái (62 of zero-shot-short's 121 such mentions); người for cô gái / chàng trai.
  - Segmentation: cửa from cửa hàng, kính from cổ kính, cây from cây cầu.
  - Other: áo (48 of fuse2-detailed's 309 "other"), đường, vỉa hè, ánh sáng / bầu trời.
- **Bound without my compound table:** a pyvi-only rule flags 12–36% of reference-false mentions as artefacts and contains 80–100% of the table's artefacts.

### 2.2 Precision, CHAIR and recall under the new matching

| system | R0 | R1 | R2 | R3 | **R4** | R5 | CHAIR_s R0→R4 | R exact | **R_ref** |
|---|---|---|---|---|---|---|---|---|---|
| P1-short | 77.9 | 76.7 | 77.4 | 79.0 | **84.4 [82.1,86.6]** | 87.4 | 32.1→24.4 | 41.4 | **50.5** |
| fuse2-short | 75.7 | 74.7 | 75.3 | 76.7 | **80.9 [78.4,83.4]** | 85.9 | 39.1→30.5 | 47.1 | **56.9** |
| tags_fuse2-short | 77.9 | 77.1 | 77.7 | 78.9 | **83.0** | 87.2 | 35.8→27.8 | 46.7 | **56.7** |
| zero-shot-short | 52.3 | 52.4 | 54.6 | 55.7 | **66.3 [63.7,68.9]** | 69.3 | 65.4→51.6 | 32.5 | **41.5** |
| P1-detailed | 78.3 | 76.9 | 77.3 | 78.8 | **83.9** | 87.5 | 32.3→25.1 | 42.7 | **51.9** |
| fuse2-detailed | 68.0 | 66.6 | 67.4 | 68.6 | **74.0 [71.7,76.4]** | 79.6 | 63.3→52.9 | 61.2 | **69.9** |
| tags_fuse2-detailed | 70.7 | 69.1 | 70.1 | 71.1 | **76.4** | 82.2 | 56.5→47.0 | 59.7 | **68.5** |
| zero-shot-detailed | 31.6 | 30.9 | 33.2 | 34.6 | **42.5** | 47.8 | 98.0→95.2 | 57.1 | **69.4** |

**Gaps vs P1 (paired):**
- fuse2 short: R0 −2.2 [−4.8, 0.6] → R4 −3.5 [−5.9, −1.0]; R_ref +6.3 [4.3, 8.4].
- tags_fuse2 short: 0.0 → −1.4 [−3.6, 0.9].
- zero-shot short: −25.7 → −18.1 [−20.8, −15.1].
- fuse2 detailed: −10.4 → −9.9 [−12.3, −7.4]; R_ref +18.0 [15.9, 20.2].

**Gaps vs the held-out human (precision R0 → R4):**
- P1-short −10.0 → −5.8 [−8.2, −3.4].
- fuse2-short −12.3 → −9.4; its R_ref is +3.2 [0.8, 5.4] above the human.
- zero-shot-short −35.2 → −23.8.

**What this means:**
- Naming and segmentation inflate CHAIR_i by 5–7 points for the fine-tuned models and 11–14 for zero-shot.
- The segmentation fix on its own lowers fine-tuned precision by 0.8–1.6. SFT models copy the annotators' compounds, so the artefacts also produce false true-positives (hoa quả matched as hoa + quả; cửa hàng matched as a door).

### 2.3 The known "người" vs "cô gái" problem in CHAIR-vi

Completing only the person tree in `HYPERNYMS` gives:

| system | CHAIR_i before → after |
|---|---|
| P1-short | 19.2 → 17.0 |
| fuse2-short | 21.9 → 20.7 |
| zero-shot-short | 42.9 → 37.1 |
| fuse2-detailed | 29.0 → 27.1 |
| zero-shot-detailed | 65.1 → 61.8 |

The bare "người" accounts for only 3–24 of the removed mentions per system; most of the effect is "phụ nữ" where the references say "cô gái" (`chair_person_fix.py`).

### 2.4 Inventory of segmentation artefacts

| artefact | count | note |
|---|---|---|
| cửa (door) inside cửa hàng (shop) | 843 | 710 in predictions, 133 in test references |
| quần áo split into two garments | 148 | |
| cửa sổ (window) read as door | 124 | |
| trái cây (fruit) read as tree | 123 | |
| lề đường | 117 | |
| hoa quả read as hoa + quả | 110 | |
| cây + cầu (classifier read as tree) | 100 | |
| cổ kính read as glasses | 51 | zero-shot only |
| cầu thang (stairs) read as bridge | 28 | |
| môi trường read as school | 17 | |
| "tòa" tone-mark style | 112 captions | zero-shot detailed |

### 2.5 Validation of the naming relations with phi

| caption set | result |
|---|---|
| KTVIC train (571 pairs) | synonyms 1.00, near-synonyms 1.00, members 0.98, hypernym/hyponym 0.77 (79% ≥ 0.5), unrelated 0.07, person siblings −0.14 |
| COCO Karpathy train (113,287 images, CHAIR's 443 words) | AUROC 0.872; phi ≥ 0.9 → 94.6% same class |
| UIT-ViIC (3,846 images) | AUROC 0.817; no different-class pair above 0.33 |

- **Data support:** of the naming-level mentions, 84/95 (P1-short), 95/118 (fuse2-short) and 171/205 (fuse2-detailed) have phi ≥ 0.5 on train.
- **phi depends on the scene:** người~đàn ông is 0.80 on KTVIC but 0.28 on UIT-ViIC, where images hold players plus crowds. A fixed word hierarchy alone would over-credit in crowded scenes.

### 2.6 Expected naming level (1v4)

| | most common name | more general | more specific | other |
|---|---|---|---|---|
| human | 84.7 [82.6, 86.7] | 5.8 | 6.4 | 3.1 |
| P1-short | 79.1 [76.6, 81.8] | 10.2 | 6.1 | 4.6 |
| fuse2-short | 79.0 | 9.6 | 6.8 | 4.6 |
| zero-shot-short | 70.4 | 20.4 | 5.8 | 3.4 |
| fuse2-detailed | 79.3 | 7.1 | 9.7 | 3.9 |

- **By domain:** people is the most variable domain (top-name share 87.3%, 1.47 name types). Other domains are 92–99%.
- **Comparison with ManyNames** (75.2% overall, 59.0% for people, checked in the PDF): 5 captions give tighter name distributions, but the order across domains is the same.
- **Headroom:** perfect naming would add at most +9.5 precision to P1-short under the exact rule. Naming at human level would add about +2.5 under the exact rule and about 0 under R4.

### 2.7 Training-side pilot (3,769 images × 10 folds, B = 1000)

| target | P | R | F1 | change vs base |
|---|---|---|---|---|
| p1 | 71.8 | 52.4 | 60.6 | |
| p1 + consensus naming | 72.1 | 52.5 | 60.7 | dF1 +0.14 [−0.04, 0.32] |
| fuse2 | 63.0 | 73.6 | 67.9 | |
| fuse2 + consensus naming | 63.5 | 71.2 | 67.1 | dF1 −0.73 [−0.94, −0.54] |
| fuse2 by new referents | 62.9 | 73.4 | 67.7 | dF1 −0.13 [−0.21, −0.05] |

- Annotators' naming is largely idiosyncratic: the most common name of 3 annotators barely predicts the other 2.
- In fused targets, two names for one referent give two chances to match, so the exact rule rewards naming the same thing twice. R_ref does not.

## 3. Literature

**Naming level.**
- Ordonez et al., ICCV 2013 / IJCV 2015.
  - Entry-level names come from MTurk naming plus n-gram naturalness over WordNet hypernyms.
  - Predicted names match human names 21–37% of the time; one annotator versus two others reaches only 0.35–0.45 precision.
- Mathews et al., WACV 2015. Nearly all of the gain comes from a frequency prior; not used for caption evaluation.
- ManyNames, LREC 2020 (2020.lrec-1.710).
  - 36 names per Visual Genome (VG) object; the top name gets 75.2% of responses, 59.0% for people.
  - VG's single label equals the top name for only 72.8% of objects.
- ManyNames v2, COLING 2020 (2020.coling-main.172).
  - Bottom-Up: 73.4% top name + 14.5% adequate alternative = 87.9%; 61.2% against the single VG label.
  - 54.5% of its mismatches with the top name are adequate alternatives (people 63%, vehicles 79%; verified in the PDF).
- Graf et al., CogSci 2016: rational-speaker model of naming level, driven by informativeness versus cost.
- Gualdoni et al., CogSci 2022 and JML 2023: visual typicality and competition between names predict how much naming varies.
- Testoni et al., ACL 2024 short: compares VLM name distributions with ManyNames.
- Berger & Ponti, NAACL 2025: per-image name distributions from XM3600 captions (including Vietnamese), via machine translation into WordNet; descriptive only.
- Nebbia & Kovashka, Findings NAACL 2024: 31.7% of COCO object mentions in captions use synonyms.
- Young et al., TACL 2014 (denotation graph). Co-denotation over images cannot tell "same object" from "objects that appear together"; phi can.
- Flickr30k Entities: name sets per referent, but from manual coreference annotation.

**Hallucination metrics.**
- CHAIR, EMNLP 2018: 67 person words collapse into one class; no hypernyms.
- ALOHa, NAACL 2024: AP 48.6 vs CHAIR's 36.9 on HAT.
- OpenCHAIR, EMNLP 2024: balanced accuracy 0.93–0.95 vs CHAIR's 0.77–0.90.
- VALOR-EVAL, Findings ACL 2024: GPT-4 judge; broader names are credited for faithfulness but not for coverage.
- THRONE (CVPR 2024), AMBER and CAPTURE.
- Taxonomy-Aware Evaluation of VLMs, CVPR 2025: hierarchical precision/recall against an external taxonomy, single labels.
- Multilingual work (MHR, CLAIM, multilingual POPE) is translated yes/no only, with no Vietnamese.

**Vietnamese.**
- UIT-ViIC, KTVIC, OpenViIC and vieCap4H propose no hallucination metric.
- Tools: VnCoreNLP (segmentation F1 97.9), pyvi, underthesea.
- The Extended OMW Vietnamese wordnet covers only 70 of our 113 nouns, and I found no Vietnamese hypernymy dataset. That is why the relation layer is a small explicit list validated by phi.

## 4. Search log and limitations

**Searches.**
- WebSearch was exhausted and the arXiv / Semantic Scholar APIs returned 429 (rate limit), so I ran 22 OpenAlex queries; results are in `scoop/`.
- Partial precedents only: Taxonomy-Aware Evaluation (CVPR 2025) and Young et al. (2014).
- Novelty therefore means "not found", not "does not exist".

**Limitations.**
- The compound table and relation lists are small hand-built resources. phi, the pyvi-only bound and N_phi (30–38% for fine-tuned models) check them against human captions.
- "Other" still mixes hallucinations with objects the references simply missed. A held-out human keeps 11.9% flagged under R4.
- Crediting hypernyms can be gamed by vague captions, so P must always be read together with R_ref and naming agreement. Zero-shot's R_ref_vague − R_ref is 8.3–9.6 points.
- The generic nouns đồ / vật touch 0.2–1.2% of fine-tuned mentions and 4.0% for zero-shot detailed.

## 5. Files

All in the A7 directory above:
- `naming.py`: extraction and relation layers, with a self-check.
- `pilot_decompose.py` / `.out` / `.json`: Sections 2.1–2.2.
- `naming_level.py` / `.out` / `.json` and `phi_train.json`: Sections 2.5–2.6.
- `offline_naming.py` / `.out`: Section 2.7.
- `chair_person_fix.py`: Section 2.3.
- `phi_coco_en.py`, `phi_uitviic.py`: the phi checks on COCO English and UIT-ViIC.
- `enum_artefacts.py`, `spans.py`, `inspect_cats.py`: artefact enumeration and inspection.
- `scoop/` (search queries and results) and `lit_dl/` (downloaded papers).

To rerun: `cd /mnt/d/vsps_image_captioning && NCS_DATA=data nice -n 15 python3 <A7>/pilot_decompose.py --B 2000`.