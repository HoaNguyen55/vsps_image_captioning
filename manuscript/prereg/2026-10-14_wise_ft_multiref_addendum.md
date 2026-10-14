# Pre-Registration Addendum: Two-Gold Count-Controlled Endpoints for `56_multiref_s42` (`40_multiref_s42`) and `59_wise_ft_s42` (`PD-4 Q6` / `PD-2` / `D17`)

- **Registration Date**: `2026-10-14` (locked before `56_multiref_s42` and `59_wise_ft_s42` outputs exist)
- **Generator Script**: `.session_backup/2026-10-14/r12_verify/build_pd4_q6_preregs.py` (zero hand-typed floats)
- **Companion JSON**: `.session_backup/2026-10-14/r12_verify/wise_ft_multiref_addendum.json`

---

## 1. Frozen Parent Pre-Registrations & Checksums

| File | Bytes | SHA-256 | MD5 |
|---|---:|---|---|
| `manuscript/prereg/2026-10-13_vgr_wise_ft.md` | 7819 | `8d7e5ece468e98d58dfb42c13e760382abd5a6e473d9d4ab5ae1df837d7db429` | `c438e4325ec6fa4c6d9e97fc9a089ac0` |
| `manuscript/prereg/2026-10-13_vgr_wise_ft_jobs/59_wise_ft_s42.sh` | 7316 | `bb4b1d6d064384c23a2ad25819e50352608de4fceb8573327de7777af6c0a32e` | `de216d599e558d5f1d0085ac26e3700e` |
| `manuscript/prereg/2026-10-12_ladder_predictions.json` | 7066 | `65dae1bc1598c6b7fc4743fd5ba9e3e25245a3a90b2e6d8ec614eeea5702ece3` | `e48078359b4fd633c9091d45b1e61096` |
| `manuscript/prereg/2026-10-14_ladder_interpretation_addendum.md` | 5413 | `23ef221062fe7b1c3e7a81f08c6f77739e38e42b42da5d5ef88cc80cb10027c1` | `195eea02c1799ce2f20c7e763cb54294` |

---

## 2. Primary Count-Controlled Endpoint (`PD-2` Option A) & Two-Gold Protocol

Per `PD-2` Q1 (`Option A`), `PD-4` Q6, and `D17` §3(c), every training-time or weight-interpolation run is evaluated at its own observed mention count $M(\alpha)$ against the frozen KTVIC learner frontier with **zero refitted parameters**:

$$\widehat{\text{TP}}_0(M) = 1.3996 \cdot \left(\frac{M}{1.7826}\right)^{0.7468}, \qquad \hat{P}_0(M) = \frac{100\,\widehat{\text{TP}}_0(M)}{M}, \qquad \hat{R}_0(M) = 5.4859 + 25.9815\,\widehat{\text{TP}}_0(M),$$

$$\Delta P_{\text{front}}(\alpha) = P(\alpha) - \hat{P}_0(M(\alpha)).$$

Alongside $\Delta P_{\text{front}}(\alpha)$ (reported both on the fixed curve above and with $B=5000$ image-bootstrap 95% CIs refitting the 4 anchor runs `p1-gold-short`, `p1_s43-short`, `p1_s44-short`, `fuse2_s42-detailed` on each bootstrap draw), every system is scored on:
1. **N-gram & Surface Metrics**: `CIDEr-D`, `BLEU-1..4`, `ROUGE-L`, `METEOR`, `CHAIR_s`, `CHAIR_i`, words/caption, sentences/caption, and CJK rate.
2. **Two-Gold Object `P / R / F1` (`v1` raw-tone `RESCAP_RAW_TONE=1` and `v2` tone-normalised `RESCAP_RAW_TONE=0` side by side)**:
   - **Gold 1 (Reference Union)**: KTVIC 5-ref union (`n = 558` test images).
   - **Gold 2 (Independent Human Panel / Instance Truth)**: OpenViIC 5-annotator human panel (`n = 555` matched KTVIC test images, strictly aggregate scores only) with linear contrast $L(\kappa_0=0.35) = \Delta\rho_I - 0.35\,\Delta\rho_A$; plus `UIT-ViIC val` (`n = 924`) COCO-80 human instance gold for `59_wise_ft_s42`.
3. **Two-Sided Matched-Count Vocabulary Controls (`(v, g)` Tie-Avg and `POOL-VOTE`)**:
   - At each image's observed mention count $k_i = |M_i(\alpha)|$, we evaluate both analytical `(v, g)` tie-averaging expectation and `POOL-VOTE` (`6v + g` with corpus prior `lp` tie-breaking) on the `p1assist_s42` 7-caption pool (`1` greedy + `6` $T=0.5$ samples) to separate count shifts from within-count object ranking.

---

## 3. Pre-Registered Specification for `56_multiref_s42` (`40_multiref_s42`, Ladder Step 1)

- **Training recipe**: All 5 human references per image (`18845` rows, `5.0` rows/image, `942` optimizer steps, seed 42), evaluated in `short`, `detailed`, and `two` modes.
- **Pre-registered `multiref_s42-short` intervals (`2026-10-12_ladder_predictions.json`)**:
  - `M`: point `1.741`, interval **`[1.645, 1.836]`** (`M / M_P1` in `[0.923, 1.030]`; `T` model predicts ideal test count `1.28`)
  - `P`: point `79.0`, interval **`[76.9, 81.1]`** (`dP_vs_P1 = +0.5`)
  - `R`: point `41.2`, interval **`[38.7, 43.7]`** (`dR_vs_P1 = -0.6`; `F1` point `54.2`)
  - **Frontier residual `H0`**: `point in [-1.0, +1.0]; H0 rejected only if the 95% CI (~+-2 P) excludes 0`
  - **Variance channel `H1`**: `frontier residual P >= +1.0 with a CI excluding 0 (A1 proxy: +3.0 mP net)`
  - **Single-writer interpretation rule (`H6 P4`)**: Per 2026-10-14_ladder_interpretation_addendum.md (H6 P4), KTVIC's 5 references per image are written sequentially by a single annotator (N2 lag-1 adjacency 0.7102 on test, 0.6673 on train vs 0.4000 null). Therefore multiref_s42 tests within-annotator 5-slot mention variance rather than between-annotator consensus variance, while p1_s42 trains on slot 0 (first-sentence salience bias).
  - **Structural check (`multiref_s42-detailed`)**: `p1ep4/cons/unf2/multiref with the detailed prompt write one sentence (mean sentences <= 1.03) and M within +-0.08 of their short mode`

---

## 4. Pre-Registered Specification for `59_wise_ft_s42` (`WiSE-FT` Weight-Space Interpolation)

| $\alpha$ | LoRA $r$ | `lora_alpha` | Effective Scale $\alpha \cdot (\text{lora\_alpha}_0 / r)$ | Adapter Tag | Status |
|---:|---:|---:|---:|---|---|
| `0.00` | `16` | `0` | `0.0000` | `zeroshot` | `LANDED_ANCHOR` |
| `0.25` | `16` | `8` | `0.5000` | `fuse2_s42_wise025` | `OPTIONAL_GRID_POINT` |
| `0.50` | `16` | `16` | `1.0000` | `fuse2_s42_wise05` | `STEP0_PRIMARY_CANDIDATE` |
| `0.75` | `16` | `24` | `1.5000` | `fuse2_s42_wise075` | `STEP0_PRIMARY_CANDIDATE` |
| `1.00` | `16` | `32` | `2.0000` | `fuse2_s42` | `LANDED_ANCHOR` |

- **KTVIC `short` CIDEr-D guard**: $\ge 140.7$
- **VGR SFT futility threshold on `UIT-ViIC val`**: $\Delta F_1(\text{instance}) \ge +3.5$
- **Primary KTVIC count-controlled endpoint**: At each evaluated alpha in {0.0, 0.25, 0.50, 0.75, 1.0} and mode in {short, detailed}, report Delta_P_front(alpha) = P(alpha) - P_hat_0(M(alpha)) (both fixed-curve and refitted-anchor B=5000 CI) and paired Delta(Delta_P_front)(alpha vs 1.0) against fuse2_s42 (alpha=1.0), under both v1 and v2.
- **Matched-count `(v, g)` controls**: At each alpha's per-image mention count k_i = |M_i(alpha)|, report paired dP, dR, dF1 against both (v,g) tie-avg and POOL-VOTE controls on KTVIC 5-ref gold (n=558) and OpenViIC panel gold (n=555).
- **OpenViIC panel contrast $L(0.35)$**: Linear contrast L(0.35) = Delta_rho_I(alpha vs 1.0) - 0.35 * Delta_rho_A(alpha vs 1.0) on the 555 OpenViIC-matched KTVIC test images.
- **`UIT-ViIC val` truth endpoint**: On UIT-ViIC val (n=924 COCO-2014 images), report COCO-80 human instance-gold (P, R, F1), instance+5ref union (P, R, F1), 73-rare-class recall (<200 KTVIC train mentions), and count-matched (v,g) tie-avg control at k_i = |M_i(alpha)|.
- **Decision & kill rule (`H6 P7` / `N12-D2`)**: Per H6 P7 & D17 §3(c): WiSE-FT claims a count-controlled truth-side positive only if at the dev-chosen alpha* in {0.50, 0.75} (satisfying KTVIC short CIDEr-D >= 140.7), (i) UIT-ViIC val instance-gold F1 gain over fuse2_s42 has 95% CI > 0, (ii) KTVIC test frontier residual change Delta(Delta_P_front)(alpha* vs 1.0) is non-negative or its 95% CI covers 0 (no precision collapse below the learner frontier), and (iii) if the count-controlled residual CI on UIT-ViIC val covers 0 at alpha*, record WiSE-FT as a count-shift negative and skip VGR SFT.

---

## 5. Committed Baseline Anchors on `KTVIC test` (`n = 558`, `v2` Tone-Normalised & `v1` Raw-Tone)

| Anchor Run | CIDEr-D | BLEU-4 | `M` (`v2`/`v1`) | KTVIC `P / R / F1` (`v2`) | KTVIC `P / R / F1` (`v1`) | Panel `P / R / F1` (`v2`, `n=555`) | Fixed $\Delta P_{\text{front}}$ (`v2`) | Refit $\Delta P_{\text{front}}$ 95% CI (`v2`) | `(v,g)` Tie-Avg `P / F1` at $k_i=M_i$ (`v2`) | `POOL-VOTE` `P / F1` at $k_i=M_i$ (`v2`) |
|---|---:|---:|---|---|---|---|---:|---|---|---|
| `zeroshot-short` | 28.98 | 5.48 | 2.167 / 2.167 | 52.52 / 32.65 / 40.27 | 52.27 / 32.48 / 40.07 | 70.65 / 26.90 / 38.96 | `-22.21` | `-22.21 [-25.01, -19.58]` | 72.20 / 51.41 | 75.57 / 53.88 |
| `zeroshot-detailed` | 0.01 | 2.87 | 6.564 / 6.541 | 31.78 / 57.61 / 40.96 | 31.59 / 57.12 / 40.68 | 47.81 / 53.75 / 50.61 | `-24.66` | `-24.67 [-28.37, -21.20]` | 67.79 / 62.13 | 68.02 / 62.29 |
| `fuse2_s42-short` | 143.90 | 42.29 | 2.091 / 2.091 | 75.75 / 47.13 / 58.11 | 75.75 / 47.13 / 58.11 | 78.68 / 29.38 / 42.78 | `+0.35` | `+0.34 [-1.51, +2.25]` | 74.20 / 55.85 | 78.52 / 58.92 |
| `fuse2_s42-detailed` | 23.86 | 27.24 | 3.154 / 3.154 | 67.95 / 61.17 / 64.39 | 67.95 / 61.17 / 64.39 | 74.74 / 40.89 / 52.86 | `+0.00` | `+0.00 [+0.00, +0.00]` | 69.91 / 60.07 | 71.93 / 61.82 |
| `p1-gold-short` | 149.79 | 45.55 | 1.796 / 1.796 | 77.94 / 41.42 / 54.09 | 77.94 / 41.42 / 54.09 | 78.98 / 25.25 / 38.27 | `-0.42` | `-0.43 [-1.47, +0.56]` | 75.03 / 52.05 | 80.74 / 55.89 |
| `p1-gold-detailed` | 146.19 | 44.39 | 1.828 / 1.828 | 78.33 / 42.70 / 55.27 | 78.33 / 42.70 / 55.27 | 79.55 / 26.16 / 39.37 | `+0.32` | `+0.31 [-1.18, +1.79]` | 75.23 / 52.61 | 80.30 / 56.10 |
| `p1_s43-short` | 143.92 | 45.15 | 1.763 / 1.763 | 78.76 / 41.69 / 54.52 | 78.76 / 41.69 / 54.52 | 79.00 / 25.45 / 38.50 | `+0.03` | `+0.03 [-1.05, +1.05]` | 75.51 / 52.40 | 80.98 / 55.88 |
| `p1_s43-detailed` | 140.45 | 43.72 | 1.771 / 1.771 | 79.86 / 42.33 / 55.33 | 79.86 / 42.33 / 55.33 | 80.20 / 25.64 / 38.86 | `+1.21` | `+1.21 [-0.39, +2.83]` | 76.04 / 52.62 | 81.36 / 56.14 |
| `p1_s44-short` | 143.70 | 44.79 | 1.788 / 1.788 | 78.86 / 42.45 / 55.19 | 78.86 / 42.45 / 55.19 | 79.70 / 25.49 / 38.63 | `+0.41` | `+0.41 [-0.56, +1.40]` | 75.26 / 52.49 | 80.80 / 56.21 |
| `p1_s44-detailed` | 142.14 | 44.62 | 1.808 / 1.808 | 78.49 / 43.18 / 55.72 | 78.49 / 43.18 / 55.72 | 80.32 / 26.18 / 39.48 | `+0.26` | `+0.26 [-1.33, +1.81]` | 74.67 / 52.38 | 79.98 / 56.04 |
| `p1assist_s42-short` | 148.66 | 45.88 | 1.823 / 1.823 | 78.76 / 42.86 / 55.51 | 78.76 / 42.86 / 55.51 | 79.76 / 26.43 / 39.71 | `+0.69` | `+0.68 [-0.83, +2.19]` | 74.76 / 52.87 | 80.33 / 56.72 |
| `p1assist_s43-short` | 148.06 | 45.63 | 1.774 / 1.774 | 79.09 / 42.30 / 55.12 | 79.09 / 42.30 / 55.12 | 79.74 / 26.02 / 39.24 | `+0.48` | `+0.48 [-1.04, +1.96]` | 75.79 / 52.75 | 81.36 / 56.49 |
| `p1assist_s44-short` | 147.96 | 45.72 | 1.760 / 1.760 | 80.04 / 42.68 / 55.68 | 80.04 / 42.68 / 55.68 | 80.18 / 25.50 / 38.69 | `+1.27` | `+1.27 [-0.18, +2.68]` | 75.81 / 52.65 | 81.60 / 56.57 |
| `p1ep4_s42-short` | 143.10 | 44.49 | 1.726 / 1.726 | 77.57 / 39.77 / 52.58 | 77.57 / 39.77 / 52.58 | 80.08 / 24.86 / 37.94 | `-1.59` | `-1.59 [-3.47, +0.23]` | 75.59 / 50.92 | 81.18 / 54.71 |
| `cons_s42-short` | 147.09 | 44.97 | 2.074 / 2.074 | 77.01 / 47.53 / 58.78 | 77.01 / 47.53 / 58.78 | 78.14 / 29.07 / 42.38 | `+1.44` | `+1.44 [-0.10, +2.97]` | 73.99 / 55.59 | 78.34 / 58.85 |
