# Pre-registration: R13-Q2, object metrics vs LongCap-Arena human Relevance

**Frozen:** 2026-10-15, before any statistic involving a LongCap-Arena human score was computed. Mandate: PD-7 Q2.
**Frozen predictions (machine-readable):** `2026-10-15_q2_longcap_arena.json`.
**Script:** `scripts/r13/r13_q2_longcap_arena.py`, sha256 `c0d8533fe3db9b3d0f090e7ef866956813a68b7d7e05b825fc74538781a658ec`. The script refuses to run if its own sha or any input sha differs from the JSON.

## Data and licence

- LongCap-Arena (Matsuda et al., VELA, EMNLP 2025). Annotation CSVs from `github.com/Ka2ukiMatsuda/VELA` `data/` at HEAD `666e33c7`. The GitHub repo has a BSD-3-Clause LICENSE; the HF card (`Ka2ukiMatsuda/LongCap-Arena`) states BSD-3-Clause-Clear. Both permit research use and derived scoring.
- Stored as untrusted data in `.session_backup/2026-10-15/r13_data/longcap_arena_vela_repo/`. The script is run from outside that folder with `python3 -E -P`. That is `-I` without `-s`, because numpy is installed in user site-packages; the data folder is never on `sys.path`.
- Input sha256s for all 15 CSVs, the synonym list and the E1 matcher are listed in the JSON.
- What parsing showed before freezing: 5,109 Relevance rows, one candidate per image, one reference per image, and no system label. The paper says candidates come from ten models, but the model of each row is not released.

## Design (adapted from the registered DOCCI G3, 2026-10-14_h1_polaris_docci.md §2)

- **Matcher:** the E1 COCO-80 CHAIR matcher (primary and only). Gold = COCO-80 classes in the image's human reference. M = distinct classes named; P_raw = TP/M; −CHAIR = −FP/max(M,1).
- **Human measure:** Relevance (it penalises wrong objects, attributes and relations), all splits pooled.
- **Deviations from G3:** these are forced by the release format and fixed here before any look.
  - (i) is a pooled slope, because system IDs are not released, so a within-system slope cannot be computed.
  - (ii) uses the caption-level Kendall τ_b, because the 14-VLM-style system ranking cannot be built. The matched-prefix MCP needs same-image pairs, so the count-matched score is z_P = P_raw − mean P_raw at the same M (G3's registered secondary estimator).
  - (iii) uses pairs across images, because each image has only one candidate.
- **Bootstrap:** 2,000 image-clustered multinomial resamples, seed 0. Each image has one caption, so image = caption.

## Frozen predictions

| Test | Prediction | Pass rule |
|---|---|---|
| (i) | Human Relevance falls with object count M | OLS slope β_M < 0 and 95% CI upper bound < 0 |
| (ii) | Count-matched precision tracks Relevance better than raw precision | Δτ_b = τ_b(z_P, Rel) − τ_b(P_raw, Rel) ≥ +0.10 and CI lower bound > 0 (captions with M ≥ 1) |
| (iii) | −CHAIR agrees with Relevance more on count-equal than on count-differing pairs | acc_ceq − acc_cdiff > 0 and CI lower bound > 0 |

**Overall verdict:** PASS if all three tests pass, FAIL if none passes, otherwise MIXED.

**Kill rules:**
- (ii): if Δτ ≤ 0, the claim that count-matched precision tracks LongCap-Arena Relevance better is withdrawn.
- (iii): if the difference is ≤ 0, the claim that agreement is higher on count-equal pairs on LongCap-Arena is withdrawn.

**Reporting:** the result is reported whichever way it falls. The OLS of Relevance on M + words + G is descriptive only. Descriptiveness and Fluency are not tested.
