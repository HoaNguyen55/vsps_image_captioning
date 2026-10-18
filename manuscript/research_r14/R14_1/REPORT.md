# R14-1: Evidence from external visual grounding (detectors) for the Qwen2.5-VL-7B Vietnamese captioner

CPU only: nice 19, 1 thread, ulimit 1.5 GB, `python3 -I`. No GPU, no commits.

**Frozen inputs (sha256 prefix):**
- `p1assist_s42-short.preds.json` ca5ce253
- `rl/p1dev_s42-dev300-short.preds.json` 1e183383 (adapter trained without dev300)
- `tags_gdino.json` a17220f8 (Grounding DINO base, COCO-80 classes, KTVIC test only)
- `ktvic_openviic_refs.json` 4eb02cc4
- `vi_oiv7_map.json` 27f2b1ca
- `uitviic_p1_s43-short.preds.json` 42ad49ee

**Matchers reused unchanged:** `rescap.chair` (`objects_in`, `_gold_objects`, `canonical`, `_ancestors`), `object_prf.image_counts` and `scores`, `coco80_vi.json`, `vi_oiv7_map.json`.

## 0. Verdict

1. **Much of KTVIC's "hallucination" is real objects the annotators didn't name.**
   - Detectors could see about half of it: 54% of hallucinated mentions on test and 59% on dev300 are in OIV7-mapped classes.
   - But a second, independent human panel (the UIT-OpenViIC captions of the same images) names 54% (test) and 58% (dev300) of the "hallucinated" mentions. The R9 C3 figure was 56.5%.
   - A perfect detector would confirm those objects, not refute them.
2. **Upper bound for removing every refuted mention** (test, p1assist_s42 short), with a perfect presence verifier and no recall loss:
   - OIV7 classes: precision 78.1 → 80.4, CHAIR_i 18.3 → 15.9, F1 +0.6.
   - All classes (open vocabulary): precision 85.3, CHAIR_i 10.7, F1 +1.7.
   - Only an oracle that reads the reference captions (gaming the metric) reaches precision 86.6 over OIV7 classes.
3. **The real detector loses F1.** The rule "drop a COCO-class mention that Grounding DINO did not tag" gives:
   - CHAIR_i −0.7 points, 95% CI [−1.7, +0.2]
   - precision +0.25, recall −4.3, F1 −3.7
   - It removes 86 correct mentions for 27 hallucinated ones, so a refutation is only 24% precise.
4. **Break-even for F1 (derived here).** Deleting a mention raises F1 only if it is hallucinated with probability q > 1 − F1/2, about 0.73 on KTVIC.
   - CHAIR_i improves whenever q is above CHAIR_i (0.18).
   - So detector removal moves the CHAIR/precision operating point; at best it leaves F1 unchanged.
   - It cannot raise CIDEr, only avoid losing it.
5. **UIT-ViIC: about zero headroom.**
   - CHAIR_i against the references is 30.0 (P1 s43).
   - Of 130 hallucinated mentions, 52 are strict COCO classes, and 41 of those are *cô gái* (a gender/age word detectors cannot check).
   - A detector can refute about 1–2 mentions (`uit.out`).
6. **Proposals:** P-A (verify, then re-decode) and P-B (detector-checked, count-matched DPO).
   - Expected: CHAIR_i −1 to −3.5 points, precision +1 to +3.5, F1 −0.5 to +1.5, CIDEr −2 to +1.
   - Tag-conditioned SFT (b) and a detector-reward GRPO (c) are rejected (section 4).

## 1. CPU feasibility (`feas.json`, `uit.out`)

**Lexicon coverage:**
- 47 of the 113 KTVIC classes are reached by any `coco80_vi` synonym, 34 by first entries only, and 30 are strict whole-name COCO classes.
- `vi_oiv7_map.json` maps **69** classes, not 82. Its `_skipped` list excludes stalls, carts, *cửa*, *cầu*, *quả* and others whose absence can't be verified soundly. Every number here uses 69.

| | dev300 p1dev_s42 | test p1assist_s42 | test fuse2_s42 |
|---|---|---|---|
| Unique mentions / hallucinated / CHAIR_i | 529 / 123 / 23.3 | 1017 / 186 / 18.3 | 1167 / 256 / 21.9 |
| Hallucinated share in COCO-any / COCO-first / OIV7 classes | 51 / 34 / 59% | 47 / 28 / 54% | 49 / 28 / 62% |
| Hallucinated share in person subtypes | 11% | 15% | 13% |
| Hallucinated mentions the panel confirms as present | 57.7% | 53.8% | 54.3% |
| Same, within OIV7 classes | 63.9% (n=72) | 63.0% (n=100) | – |

**Top hallucinated classes on test** (count, then how many the panel confirms):
- *đường* 24 (13), *quầy hàng* 21 (4), *phụ nữ* 16 (13), *đàn ông* 12 (7), *cửa* 8 (6), *thuyền* 8 (7), *vỉa hè* 5 (0), *cặp đôi* 5 (1).
- The classes the panel rarely confirms (stalls, sidewalks, couples) are outside OIV7. Catching them needs targeted text prompts to the detector, not a fixed tag list.

**Upper bounds** (recall unchanged; exact object P/R/F1 as in Table IV):

| Rule | dev300 P / CHAIR_i / F1 | test P / CHAIR_i / F1 |
|---|---|---|
| Base | 73.4 / 23.3 / 53.8 | 78.1 / 18.3 / 54.9 |
| Perfect presence verifier, OIV7 minus person subtypes | 76.4 / 20.1 / 54.6 | 80.4 / 15.9 / 55.5 |
| Perfect presence verifier, all classes | 81.3 / 14.9 / 55.8 | 85.3 / 10.7 / 56.6 |
| Oracle that reads the references, OIV7 classes (not achievable) | 84.9 / 11.2 / 56.6 | 86.6 / 9.4 / 56.9 |
| Real Grounding DINO tags: drop untagged COCO-first mentions | no dev300 tags exist | 78.3 / 17.6 / 51.2 (recall −4.3) |

**Caveats:**
- A mention the panel doesn't name is not proof the object is absent, so the perfect-presence rows are upper bounds.
- The Grounding DINO row is descriptive and has no parameters; nothing was selected on test.
- CIDEr after removal is not measured.

## 2. Literature

All IDs were checked on their arxiv.org/abs pages on 2026-10-15.

**Detectors (prefer open weights; sending KTVIC images to an API raises a licence question):**
- Grounding DINO 2303.05499 (ECCV 2024). The Hugging Face base checkpoint was trained with COCO.
- Grounding DINO 1.5 2405.10300 and DINO-X 2411.14347 (arXiv). The Pro versions are API-only; recheck before relying on this.
- OWLv2 2306.09683 (NeurIPS 2023), YOLO-World 2401.17270 (CVPR 2024), Florence-2 2311.06242 (CVPR 2024).

**Methods:**

| Method | ID / venue | What it does | Reported result | Quality cost |
|---|---|---|---|---|
| Woodpecker | 2310.16045 (Sci. China Inf. Sci.) | Grounding DINO verification + LLM rewrite | POPE accuracy (MiniGPT-4) 54.7 → 85.3 | POPE recall 84.0 → 78.7; recall 41.1 → 38.4 in MARINE's rerun |
| LURE | 2310.00754 (ICLR 2024) | Trained revisor | CHAIR_s 54.0 → 27.1 | CHAIR_s rose 8.8 → 38.9 in MARINE's rerun |
| HALC | 2403.00425 (ICML 2024) | Grounding DINO / OWLv2 contrastive decoding | LLaVA-1.5 CHAIR_s/CHAIR_i 20.8/6.77 → 13.8/5.50 | Recall not reported |
| MARINE | 2402.08680 | Detector-guided decoding | CHAIR_i 4.6 → 3.0, recall 41.1 → 44.3 | – |
| SENTINEL | 2507.12455 (arXiv) | Grounding DINO + YOLO-World cross-check, then sentence-level on-policy DPO | Object HalBench response/mention 52.7/28.0 → 4.3/2.6; AMBER CHAIR 8.4 → 2.9 | VQAv2 78.5 → 78.4; no CIDEr reported |
| MOCHa | 2312.03631 (EMNLP 2024) | RL on a fidelity + adequacy reward, no detector | BLIP-L CHAIR_i 2.3 → 2.1 | CIDEr 138.4 → 139.6; BLIP-2 144.3 → 144.3 |

- In SENTINEL's ablation, Grounding DINO alone scores 14.3/7.7 and YOLO-World alone 12.3/6.9, against 6.6/3.8 for both together, so requiring two detectors to agree matters.
- **Related work:**
  - ViGoR 2402.06118 (ECCV 2024): detector-verified reward.
  - HSA-DPO 2404.14233.
  - OPA-DPO 2501.09695 (CVPR 2025).
  - HalluciDoctor 2311.13614 (CVPR 2024).
  - OCS-RL 2610.14976 (IEEE Access 2026; already cited in Paper A).
  - ClaimDiff-RL 2605.20278.
  - Ground-What-You-See 2601.06224 (AAAI 2026).
- **Tags in the prompt** (from R9 C2): TUNA 2406.10839 gains +0.0 with inference-only tags; ViECap 2307.16525 shows the model copies tags unless they are masked in training.
- **Pattern:** detector methods buy precision and lower CHAIR; post-hoc deletion costs recall. No paper reviewed reports a CIDEr gain from detector grounding on an in-domain fine-tuned captioner.

## 3. Proposals

### P-A. Two-detector targeted verification, then banned-word re-decode ("VRD")

**Mechanism:**
1. For each mentioned class, query Grounding DINO-T and OWLv2 with its English gloss. The glosses are in R9 `C2_detect_tags/ram_cover.py:GLOSS`.
2. Never refute a person subtype (gender or age); only the parent *người* can be refuted.
3. A class counts as refuted only when both detectors' best box score is below τ.
4. Re-decode affected images greedily, with the refuted words banned (`bad_words_ids`).
5. All other captions stay byte-identical.

**GPU cost:** about 1–1.5 GPU-h in total (detection on about 3.6k images plus re-decoding about 15% of them, 3 seeds).

**dev300 selection:**
- Grid: τ ∈ {0.15, 0.20, 0.25, 0.30, 0.35} × {both detectors agree, either detector}.
- Pick the cell with the lowest CHAIR_i, subject to:
  - refutation precision q ≥ 0.40
  - recall change ≥ −0.5
  - CIDEr change ≥ −1.0

**Prereg sketch:**
- **Frozen:** the p1assist s42/43/44 test predictions (by sha), τ and the detector rule, and the detector checkpoint revisions.
- **Primary endpoint:** test CHAIR_i, paired bootstrap B = 5000.
- **Secondary endpoints:** precision, F1, CIDEr, BLEU-4, and XM3600 OIV7-verified precision (human labels).
- **Kill rules (any one):**
  - dev300 CHAIR_i drop smaller than 1.0 point
  - q < 0.40
  - CIDEr change < −1.5
  - more than 25% of re-decodes introduce a new hallucinated class

**Expected effect (test):** CHAIR_i −1 to −3, precision +1 to +3, recall 0 to −0.8, F1 −0.5 to +0.8, CIDEr −1.5 to +0.5. UIT-ViIC: about zero.

**Novelty:** low; it is close to Woodpecker, HALC and SENTINEL, so scoop risk is high. What is defensible:
- the split into panel-confirmed versus refutable hallucination;
- the q > 1 − F1/2 break-even;
- the Vietnamese gloss-based verification.

Present it as an analysis row, not as the contribution.

### P-B. Detector-checked, count-matched on-policy DPO ("DX-DPO"; a variant of the approved M3)

**Mechanism:**
1. Use 6 samples at T = 0.8 per train-minus-dev300 image, reusing M3's pool if it exists.
2. Label each mentioned class present, absent or uncertain with P-A's two-detector rule.
3. Build pairs with equal mention counts:
   - chosen: a sample with no absent class;
   - rejected: a sample that differs only by at least one absent class.
4. Also require the chosen caption's reference CIDEr to be at least 90% of the greedy caption's.
5. Train DPO with M3's hyper-parameters.
6. Disclose that the detector labels are AI training signal, never evaluation evidence.

It targets only the 42–46% of hallucinated mentions the panel does not confirm.

**GPU cost:** about 9 GPU-h to the seed-42 gate and about 19 for 3 seeds:
- sampling about 3 (zero if M3's pool exists)
- detection about 1
- DPO 4.2 per seed
- evaluation about 0.5 per seed

The preferred option fixes β and epochs at M3's values, so selection costs nothing extra.

**Gate (dev300, seed 42, vs p1dev_s42):**
- CHAIR_i drop of at least 1.5 points
- recall change ≥ −1.0
- CIDEr change ≥ −2.0

**Kill rules (any one):**
- any gate miss
- fewer than 1,500 valid pairs
- mentions per caption falling by more than 0.15 (a count shortcut)

Report the result on the count-matched frontier plot.

**Expected effect (test):** CHAIR_i −1.5 to −3.5, precision +1.5 to +3.5, recall −1 to +1, F1 0 to +1.5, CIDEr −2 to +1.
- SENTINEL is the upper reference, but only about 45% of our hallucination mass is addressable.
- MOCHa shows CIDEr can stay within ±1.
- It uses refutation only: R9 C4 killed a detector recall reward (F1 −2.7, CIDEr −13).

**Novelty:** low to moderate; SENTINEL, ViGoR and HSA-DPO are close prior work. What is new:
- the count matching;
- the salience-aware evaluation against a second human panel;
- the Vietnamese setting.

Scoop risk is high for the generic method.

## 4. Not proposed

- **(b) Tag-conditioned SFT:**
  - The trained models ignore the tag channel (uptake 24.1% → 24.4%).
  - Judge D10 already rejected the CG-TagSFT variant (NO, 85%).
  - The oracle tag headroom is mostly *người* and rewording (R9 C2 §2b).
- **(c) Detector-reward GRPO:**
  - CIDEr-RL (N11) failed and R9 C4 killed the detector reward.
  - P-B gets the same evidence at a third to a fifth of the GPU cost.
- **HALC:** per-step detector calls are slow, and its gain on short captions is capped by section 1.
- **LURE:** its revisor raised CHAIR_s in MARINE's rerun.

## 5. Ranking

| Rank | Proposal | GPU-h | Expected effect (test) | Why |
|---|---|---|---|---|
| 1 | P-B DX-DPO | about 9 to gate, about 19 for 3 seeds | CHAIR_i −1.5 to −3.5, precision +1.5 to +3.5, F1 0 to +1.5, CIDEr −2 to +1 | Changes the model, shares M3's pool, count-matched |
| 2 | P-A VRD | about 1–1.5 | CHAIR_i −1 to −3, precision +1 to +3, F1 −0.5 to +0.8, CIDEr −1.5 to +0.5 | Nearly free and gives the dev300 refutation precision q, so **run it first as a probe** |

**Order:**
1. Run P-A's detection pass on dev300.
2. If q ≥ 0.40 and the CHAIR_i drop is at least 1.0, preregister P-A for test and build the P-B pairs.
3. Otherwise stop the detector line and report the negative: presence detectors cannot fix KTVIC's salience-driven hallucination.

The F1 ceiling for detector evidence is +0.6 (OIV7) to +1.7 (open vocabulary) on KTVIC test, and about zero on UIT-ViIC.

---

Sources:
- [MOCHa (EMNLP 2024)](https://aclanthology.org/2024.emnlp-main.1263/)
- [SENTINEL 2507.12455](https://arxiv.org/html/2507.12455)
- [ViGoR 2402.06118](https://arxiv.org/html/2402.06118)
- [OCS-RL 2610.14976](https://arxiv.org/html/2610.14976)
- [Ground What You See 2601.06224](https://arxiv.org/html/2601.06224v2)
- [ClaimDiff-RL 2605.20278](https://arxiv.org/html/2605.20278)
- [ALOHa 2404.02904](https://arxiv.org/html/2404.02904v1)
- [Survey 2507.19024](https://arxiv.org/pdf/2507.19024)
