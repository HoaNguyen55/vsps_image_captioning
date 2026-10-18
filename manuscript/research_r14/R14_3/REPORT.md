# R14-3: test-time methods that add evidence (KTVIC CIDEr, object F1, CHAIR_i)

Date: 2026-10-15. CPU only (nice 19, 1 thread). No git commit. No "first" claims. All numbers below are dev300 unless marked.
Instrument: `manuscript/research_r14/R14_3/oracle_headroom.py` → `oracle_headroom.json` (inputs: sha256 prefixes in its `inputs` key).

## 1. Oracle headroom on dev300 (ceiling for any reranker of the existing pools)

Pool per image = P1_dev greedy (`data/results/rl/p1dev_s42-dev300-short.preds.json`) + 6 samples at T0.5 + 6 at T0.8
(`data/results/upe/p1dev_s42-dev300-short-T{0.5,0.8}.jsonl`). N7 = greedy + one temperature; N13 = both.
CIDEr-D ×100, word level (VnCoreNLP RDRSegmenter, DF from dev300 refs). Objects: `rescap.chair.objects_in`, exact match
(object_prf rows). "ktvic5" gold = union of the 5 KTVIC refs; "panel" = OpenViIC panel (296 of 300 images). CHAIR_i ×100.
All keys are `oracle_headroom.json :: pools.<pool>.<row>.<metric>`.

| row (pool N13) | CIDEr | F1 ktvic5 | F1 panel | CHAIR_i | classes/cap |
|---|---|---|---|---|---|
| greedy | 144.33 | 54.57 | 40.65 | 23.25 | 1.76 |
| random sample (mean of 50 draws) | 122.04 | 52.40 | 40.02 | 25.60 | 1.76 |
| oracle by CIDEr (same 5 refs) | 206.31 | 62.86 | 41.56 | 12.78 | 1.77 |
| oracle by per-image F1 (ktvic5) | 154.19 | 71.48 | 45.45 | 7.55 | 2.03 |
| oracle by F1 on refs 0-2 only | 159.07 | 68.12 | 44.09 | 9.34 | 1.93 |
| count-locked oracle (max TP, \|M\| = greedy's), ktvic5 | 150.37 | 61.21 | 41.24 | 14.93 | 1.76 |
| count-locked oracle selected on refs 0-2 | 151.13 | 60.03 | 41.28 | 16.82 | 1.76 |

Held-out-reference ceilings (select with some refs, score on the others; `pools.<pool>.split_*`, `oracle_f1_selectA012_evalB34`):

| pool | CIDEr: pick on refs 0-2, score refs 3-4 (greedy → oracle) | pick on 2-4, score 0-1 | F1 on refs 3-4: pick by F1 on 0-2 / count-locked |
|---|---|---|---|
| N7_T0.5 | 114.54 → 130.77 (+16.2) | 181.62 → 188.14 (+6.5) | 50.73 → 58.26 / 53.16 |
| N7_T0.8 | 114.54 → 130.81 (+16.3) | 181.62 → 192.03 (+10.4) | 50.73 → 58.37 / 54.34 |
| N13 | 114.54 → 135.71 (+21.2) | 181.62 → 187.53 (+5.9) | 50.73 → 60.22 / 54.90 |

What the ceilings say:
- **CIDEr.** The same-reference oracle (+62 on N13; +42.9 on N7_T0.5 in `data/results/upe/upe_choose_t.json :: T0.5.r0_vs_greedy.cider`)
  mostly measures fitting the 5 refs. A perfect selector that never sees the scoring refs gains only +5.9 to +21.2.
  At T=1.0 with k=8 the same split gives +3.3 [−7.0, +14.2] and −20.9 [−37.1, −4.6]
  (`data/results/rl/g0_report.json :: dev.best_of_k_A012_B34_minus_greedy`, `..._A234_B01_...`).
  A random sample loses 13–29 CIDEr to greedy, so every non-greedy pick must be justified by evidence. The only way to win is to keep greedy by default.
- **Object F1 at fixed count** (the term L1 says can win): +6.6 against ktvic5 (it chooses on its own gold, so this is optimistic),
  +4.2 against held-out refs 3-4, and only **+0.6 against the independent panel** (40.65 → 41.24). A reranker over these
  pools cannot move panel F1 by much without changing count. Panel gates must therefore be non-inferiority, not superiority.
- **Coverage.** Most of the F1 ceiling (R 43 → 55-59) comes with +0.17 to +0.27 classes per caption. On the panel, UPE shows
  that ≈ +0.14 classes buys ≈ +2.2 F1 for free (count effect, §2). The panel F1 headroom beyond count is therefore on the order of +1.
- **CHAIR_i.** The count-locked oracle cuts CHAIR_i from 23.3 to 14.9–16.8, which is large. It is the most reachable target.
- Increasing N from 7 to 13 adds +0.6 to +1.7 F1 (count-locked, held-out) and +5 CIDEr (split 0-2→3-4). Gains from scaling N are real but small.

## 2. Why the earlier methods failed (failure modes to design against)

- **UPE-MBR** (`manuscript/prereg/2026-10-13_upe_mbr.md`; `data/results/upe/test/upe_mbr_ktvic_test.json`).
  Against greedy it gives panel F1 +1.53 [0.89, 2.19] (s42 `vs_greedy.panel_obj.F1`). Against COUNT it gives
  +0.07 / +0.03 / +0.17, with every CI containing 0 (kill 2, 3/3 seeds). The failure has three parts.
  - (F-a) The evidence q_o comes from the policy's own samples, which share its errors. Within a (votes, generations) cell, votes carry no extra
    information, so EF1 acts as a count knob.
  - (F-b) The utility rewards adding classes, so the raw gain is a count shift: classes per caption rise 1.76 → 1.91 (`T0.5.classes_per_caption`).
  - (F-c) The base utility (self-MBR plus retrieval CIDEr) is also self-evidence. Its CIDEr change is +0.30 [−5.05, +5.47] on dev.
- **Self-fuse k=2** (`journal_draft_B/sec6_negatives.md` §6.6). The frontier residual is −4.21 [−6.11, −2.27] on fuse2 and −3.84 on P1 s43.
  - (F-d) It appends unverified objects: the precision of the added objects is below the frontier.
  - (F-e) It makes the caption longer, often two sentences, which moves it off the KTVIC reference style (CIDEr and relations suffer).
- **Text-kNN prior.** Within-cell AUROC is 0.614 on dev and 0.581 on test (§6.1). (F-f) Text priors from similar images are evidence about the
  dataset, not about this image.
- **Detector tags** (Grounding-DINO, test only). Votes give AUROC 0.762; votes + tag give 0.765
  (`.session_backup/2026-10-13/research_r9/C5_decision_f1/out/p20_detector.log`). The strict veto gives dF1 −0.3 [−0.6, −0.1]
  (`.../C3_halluc_decode/out/p1b_gdino_strict.log`). (F-g) The detector vocabulary is COCO-like, while KTVIC errors are on quả/hoa/cây/xe, so the tags add almost no information beyond the votes.
- **Contrastive decoding.**
  - On KTVIC zero-shot short, VCD gives CIDEr 28.98 → 26.10 and CHAIR_i 0.429 → 0.449, i.e. worse on both
    (`data/results/vcd-short.json` vs `zeroshot-short.json :: results[0].scores_scaled_x100.CIDEr`, `chair.CHAIR_i`).
  - Under fixed token budgets, SPIN and VCD do not reduce hallucination consistently (2608.24966).
  - ICD, M3ID and OPERA reweight the policy's own logits, so by L1 they add no evidence. AGLA's image–prompt matching (external evidence) is applied at token level; on a captioner with 1.8 mentions per caption there is little to gain.
  - None of these papers reports CIDEr in its abstract (checked for AGLA and 2412.06775). The ±CIDEr effect is unmeasured on our setting except for VCD (negative).
  - **Not proposed.**
- **Reference-free metrics.** Polos (2402.18091) and VELA (2509.25818) are trained or judged on English. Using them in Vietnamese requires
  translation, which adds noise, so they are not used as selectors. Multilingual CLIPScore (2502.06600) is an option for Vietnamese.
  ViCLIP-OT (2602.22678) is trained on UIT-OpenViIC, and 401 of the 558 test images near-duplicate OpenViIC train images, so it is ruled out as a selector (it may serve only for sensitivity).

Design rules for any new method:
- the evidence source must be a different model that looks at the image;
- it is compared against COUNT-matched controls;
- greedy is the default, and switching away from it requires a margin;
- it emits single-sentence captions only (no fusion).

## 3. Proposals

### P1 — XV-EF1: cross-model verified expected-F1 MBR (fixes F-a, F-b, F-d, F-e)

Rule: the UPE rule unchanged, except the evidence term. The vote-based q_o is replaced by q_o = p_V(o | image), the P(yes) of an
**independent VLM verifier** asked "Is there a/an <English class name> in the image?" (113-entry lexicon mapped to English once,
frozen). Verifier: InternVL3-8B (2504.10479); fallback MiniCPM-V 2.6 (2408.01800). It is used as a scorer only, never as a writer.
The rule picks only among existing pool captions, so it never fuses or rewrites. The greedy-default margin is kept.
Existing pools are reused:
- dev N13;
- test greedy + 6 T0.5 samples for p1assist s42/s43/s44 (`data/results/upe/test/*.jsonl`, hashes in `upe_mbr_ktvic_test.json :: inputs`).

So no new captions are generated.

- **GPU-h.** About 1.3k (image, class) queries on dev and about 1.7k per test seed (measured: 4.35 and 3.04 unique pool classes per image).
  Each query is run with the image and once more without it (prior-leakage control, as in `scripts/probe_existence.py`), ≈ 13k forwards in total.
  Estimate ≈ 1 GPU-h, plus 0.5 GPU-h for download and a dry run. **≈ 1.5 GPU-h.**
- **Gate G0** (CPU, dev, before any test look). Within-(votes, generations)-cell AUROC of p_V vs ktvic5 gold ≥ 0.58 (the EV-RANK
  threshold already used for M3), and the no-image AUROC must be ≤ 0.60. If G0 fails, the method is KILLED and test is never touched.
  Reference point: Qwen's own P(có) with the image has AUROC 0.709 against 0.453 without it (`data/results/e2_probe.log`). That is not within-cell and comes from the policy itself.
- **Prereg sketch.**
  - Freeze before G0: verifier checkpoint hash, prompt, English class map, LAM/MARGIN (UPE's frozen values; no retuning), p_V cache sha256.
  - Freeze before test: the test pick file (sha256 committed) and the COUNT control lam matched on mean classes per caption.
  - Primary endpoint, KTVIC test pooled over 3 seeds, image-clustered bootstrap B = 5000: ΔF1(XV-EF1 − COUNT) ≥ +0.5 with CI lower bound > 0.
  - Co-primary: ΔCHAIR_i(XV-EF1 − COUNT) ≤ −1.0 with CI upper bound < 0.
  - Guards: CIDEr Δ vs greedy ≥ −2.0; panel ΔF1 vs COUNT ≥ −0.5 (non-inferiority; the panel ceiling is +0.6, §1).
  - Kill rules:
    - G0 fails;
    - the primary CI includes 0 on ≥ 2/3 seeds;
    - any guard fails;
    - the no-image verifier gives ≥ 70% of the with-image gain (prior leak).
- **Expected effects.** At fixed count the held-out ceiling is +4.2 F1 (N13) or +2.4 (N7_T0.5, the test pool shape), and CHAIR_i
  23.3 → 16.8. With an in-cell AUROC of about 0.65–0.75, expect roughly 20–40% of that: **ΔF1 vs COUNT +0.5 to +1.0, CHAIR_i −1.5 to −3,
  CIDEr −1 to +2, panel ≈ 0.**
  - Support: SelfVal (2601.22451) uses language-prior-free object verification over sampled captions to select among them and reports a 65.6% relative CHAIR_i reduction on LLaVA-1.5-7B; its abstract gives no recall or CIDEr figures. RLAIF-V (2405.17220) reports self-feedback at inference time.
  - Risk: the tested pool is N7 at T0.5, where the ceiling is smallest.

### P2 — LS-BoN: a dev-trained selector on external features, with held-out-reference targets (fixes F-c)

- Features per candidate:
  - p_V terms from P1 (min, mean, and the sum of log p over the mentioned classes);
  - multilingual SigLIP 2 (2502.14786) image–caption score;
  - self-consensus CIDEr, retrieval CIDEr, length, count, and the is-greedy flag.
- Model: pairwise logistic (candidate vs greedy), 5-fold cross-fit on dev300 grouped by image.
- Target: CIDEr on refs 3-4 plus 10·F1 on refs 3-4, with features and selection never seeing refs 3-4. This avoids learning the same-ref +62.
- **GPU-h:** SigLIP 2 over 300×13 + 558×7×3 captions ≈ 0.3 GPU-h; training on CPU. **≈ 0.3 GPU-h** (it needs P1's p_V cache).
- **Prereg sketch.**
  - Freeze the feature list, model class, regularization grid (chosen by inner CV), and the switch threshold (the margin that keeps greedy on ≥ 70% of dev images).
  - Freeze the test picks.
  - Primary: CIDEr Δ vs greedy ≥ +2.0 with CI > 0 on pooled test.
  - Co-primary: ΔF1 vs COUNT ≥ 0 (non-inferiority, −0.5).
  - Kill rules:
    - the dev cross-fit gain on refs 3-4 is < +2 CIDEr;
    - the selector's gain is ≥ 70% reproduced by a self-features-only ablation (that would mean no new evidence).
- **Expected effects.** The held-out CIDEr ceiling is +6 to +16 (N7_T0.5). Self-features alone gave +0.3. Expect **+1 to +3 CIDEr** and **F1 ≈ 0 to +0.5**.
  CLIP-style rewards are known to trade reference metrics for distinctiveness (2205.13115; CLIPScore 2104.08718), so SigLIP must
  enter as a feature, not as the objective. The risk of overfitting on 300 images is real, which is why the cross-fit kill rule exists.

### P3 — N-scaling of P1 (run only if P1 passes)

- Sample 32 captions per image at T0.5 for dev300 and test (3 seeds), then rerun P1/P2 frozen.
- **≈ 4 GPU-h** for sampling plus 1.5 for verifier queries on new classes.
- Expected: N7 → N13 added +1.7 to +2.5 F1 (count-locked, held-out) and +5 CIDEr to the ceiling. Realized gains are probably about +0.3 F1 and +1 CIDEr over P1.
- Prereg: same endpoints as P1. The kill rule is Δ(P3 − P1) < +0.3 F1.

## 4. Ranking

| rank | proposal | GPU-h | evidence source | expected (vs COUNT / greedy) | main risk |
|---|---|---|---|---|---|
| 1 | P1 XV-EF1 | ≈ 1.5 | independent VLM (image) | F1 +0.5..1.0, CHAIR_i −1.5..−3, CIDEr ±2 | verifier in-cell AUROC < 0.58 |
| 2 | P2 LS-BoN | ≈ 0.3 (+P1) | VLM + SigLIP 2 + learned on dev | CIDEr +1..3, F1 ≈ 0..0.5 | overfit on 300 images |
| 3 | P3 N=32 | ≈ 5.5 | as P1, bigger pool | +0.3 F1, +1 CIDEr over P1 | small ceiling growth |
| — | VCD/ICD/M3ID/OPERA/AGLA, Polos/VELA, GDINO veto | — | self-logits or English-only or weak detector | ≤ 0 measured locally | not proposed |

Honest bound: even a perfect reranker over these pools is capped at about +0.6 panel F1 at fixed count and about +4 KTVIC F1
(held-out refs). The realistic value of P1/P2 is a CHAIR_i reduction plus a small, count-controlled F1 gain, not a frontier jump.

## 5. Verified paper IDs (arXiv abstract pages fetched 2026-10-15; titles matched)

2311.16922 VCD · 2403.18715 ICD · 2403.14003 M3ID · 2406.12718 AGLA (CVPR 2025 per abstract page) · 2311.17911 OPERA ·
2412.06775 Delve into VCD · 2608.24966 attention heads behind object hallucination in LLaVA (fixed-budget SPIN/VCD) ·
2403.00425 HALC · 2310.16045 Woodpecker · 2405.17220 RLAIF-V · 2601.22451 Self-Validation framework (SelfVal) ·
2402.18091 Polos · 2509.25818 VELA · 2502.06600 multilingual CLIP captioning evaluation · 2602.22678 ViCLIP-OT ·
2504.10479 InternVL3 · 2408.01800 MiniCPM-V · 2502.14786 SigLIP 2 · 2104.08718 CLIPScore · 2205.13115 CLIP reward captioning.
