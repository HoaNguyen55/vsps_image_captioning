# Pre-registration Addendum: KTVIC Training-Target Ladder Interpretation and TOST Equivalence (`H6` Proposal P4)

Status: frozen `2026-10-14`, as an interpretive addendum to `manuscript/prereg/2026-10-12_ladder_predictions.json` (SHA-256 `65dae1bc1598c6b7fc4743fd5ba9e3e25245a3a90b2e6d8ec614eeea5702ece3`, commit `1b5d16b`).

Authority: judge decision `PD-4` (Q1, Q4, Q6) and `H6/REPORT.txt` §2 Proposal P4 (`l.110-117`) & §5h (`l.246-254`).

---

## 1. Zero Changes to Frozen Predictions or Decision Rules

This addendum makes **no change** to any frozen numerical prediction, interval, anchor constant, or decision rule in `manuscript/prereg/2026-10-12_ladder_predictions.json` or `scripts/prereg_ladder_check.py` (SHA-256 `279942468d879c93ca4c5c8767b829397b58cebedd73d845496f6ead22616d19`). Every landed ladder run (`p1ep4_s42`, `multiref_s42`, `cons_s42`, `unf2_s42`, `rnd2_s42`, `fuse2_s43`, `fuse2_s44`) continues to be scored mechanically by `scripts/prereg_ladder_check.py` against the exact pre-registered intervals in `2026-10-12_ladder_predictions.json`.

---

## 2. Four Binding Interpretation Points (`H6` Proposal P4)

Because post-registration corpus audits established that KTVIC's 5 captions per image were entered sequentially by a single writer per image (`Pham et al., 2024`, arXiv `2401.08100`, §3.2, Fig. 5: three annotators in total, each entering five captions per image into five blank boxes; `N2` adjacent-doubleton share `0.710 [0.670, 0.752]` on KTVIC test vs `0.400` exchangeable null), the following four rules govern how ladder outcomes are interpreted in the manuscript:

1. **Interpretation of the `T` Model (`A1` Implicit Threshold / Ideal Learner)**:
   - `T`'s predicted count ratios (`models.T` in `2026-10-12_ladder_predictions.json`) assume independent binomial reference sampling $k_c \sim \text{Bin}(5, \pi_c)$ (`V4` A1), which KTVIC's single-writer sequential captions violate (`V4` prereg §1d), and `T` already misses `P1`'s observed count by $+44\%$ (`V4` §2).
   - Therefore, every arm's placement relative to `L` and `T` is reported in full as pre-registered, but any outcome landing near `T` is **not** read as confirmatory support for `A1` Proposition 1. The ladder tests **frontier invariance across SFT target-curation recipes** (`L`: count driven by target length plus a single learner precision-count frontier).

2. **Interpretation of `multiref_s42-short` (`H1_variance_channel`)**:
   - In `2026-10-12_ladder_predictions.json`, `multiref_s42-short` (`5.0` rows/image, training on all 5 KTVIC captions per image) registered `H1_variance_channel` (`frontier residual P >= +1.0` with 95% CI excluding `0`) as a test of between-annotator variance reduction.
   - Because all 5 captions of a KTVIC image come from a single writer's 5-box entry sequence rather than 5 independent annotators, `multiref_s42-short` cannot test between-annotator variance reduction on KTVIC; it tests **within-writer multi-caption paraphrase diversity** against single-caption training.

3. **Interpretation of `P1`-Family Slot-0 Training Targets**:
   - The `P1`-family arms (`p1-gold`, `p1_s43`, `p1_s44`, `p1assist_s42..44`, `p1ep4_s42`) train on reference slot `0` (`scripts/build_gold_sft.py`, first caption in file order).
   - On KTVIC, slot `0` is the first caption typed in a single-writer 5-caption sequence, which has systematically lower object density (`U(1) = 1.6229` on test, `1.5646` on train) than later slots (`mean M_ref = 1.7427` on test, `1.6939` on train; `G3` slot-order audit). This slot-0 target property is disclosed whenever `P1`-family counts and residuals are compared against multi-slot or fused targets (`cons`, `unf2`, `rnd2`, `fuse2`).

4. **Secondary Descriptive Equivalence Analysis (TOST at $\pm 1.0\text{ pp}$ Precision Tolerance + MDE)**:
   - Because $n = 558$ KTVIC test images yield per-run paired 95% CIs of half-width $\approx \pm 1.5\text{ to }\pm 2.0\text{ pp}$ on precision `P` and `F1`, a non-significant frontier residual ($0 \in \text{CI}_{95\%}$) must not be overstated as exact point invariance without reporting its precision bound (`H6` Risk R5).
   - Accordingly, alongside the primary pre-registered interval check in `scripts/prereg_ladder_check.py`, each landed ladder run $r$ and the pooled mean frontier residual across all landed runs will report:
     - **Two One-Sided Tests (TOST) equivalence** at the registered model-`L` precision tolerance $\Delta_{\text{TOST}} = \pm 1.0\text{ pp}$ on `frontier_residual_P` (and $\pm 0.8\text{ pp}$ on the pooled mean residual across landed runs, matching `structural.joint_frontier_invariance` in `2026-10-12_ladder_predictions.json`), where equivalence holds at $\alpha = 0.05$ iff the 90% image-bootstrap CI ($\text{CI}_{90\%} = [q_{5\%}, q_{95\%}]$ over $B = 5000$ paired resamples) lies entirely within $[-\Delta_{\text{TOST}}, +\Delta_{\text{TOST}}]$.
     - **Minimum Detectable Effect (MDE)** at 80% power (two-sided $\alpha = 0.05$): $\text{MDE}_{80\%} = (z_{0.975} + z_{0.80}) \cdot \text{SE}_{\text{boot}} \approx 2.8016 \cdot \text{SE}_{\text{boot}}$ for each individual arm and for the joint pooled residual.
   - *Current landed check (`54_p1_4ep_s42` / `p1ep4_s42-short`)*: As noted in `PD-4` Reasons (Q3/Q6), `54_p1_4ep_s42` landed inside all three pre-registered intervals (`M`, `P`, `R`), and the joint residual over the 5 landed runs is `-0.54 [-1.55, +0.54]`.
