# Pre-registration: XM3600 Out-of-Sample Sign Predictions (`N1`), Reference Adjacency (`N2`), and Two-Gold Transfer (`C3`) (`PD-4 Q5(c)`)

Status: frozen `2026-10-14`, before `58_z_xm3600_eval.sh` (`39_xm3600_eval.sh`, sha256 `8ab1afccc06b1b6edd6c5b339ed9483c91dd1adff339b88a36b0ae471616596e`) is executed on GPU and before any file exists in `data/results/xm3600/`.
Companion machine-readable file: `manuscript/prereg/2026-10-14_xm3600_predictions.json`.

Authority: judge decision `PD-4 Q5(c)`, `H6/REPORT.txt` §2 Proposal P2 & §4 Claims 8 & 11, and `H3/REPORT.txt` §2 Proposal P2.

---

## 1. Frozen Inputs, Queue Verification (`H6` Claim 8), and Gold Densities ($\bar{G}$)

### 1.1 Queue Mechanics and Job Hash (`H6` Claim 8)
- Job file `.session_backup/machines/n2/queue/paused/39_xm3600_eval.sh` has SHA-256 `8ab1afccc06b1b6edd6c5b339ed9483c91dd1adff339b88a36b0ae471616596e`.
- Renaming the job file to `58_z_xm3600_eval.sh` (or `54_z_xm3600_eval.sh` to run immediately after `54_p1_4ep_s42.sh`) preserves its byte content and SHA-256 (`8ab1afcc...`) identically.
- `.session_backup/machines/n2/qrun.sh` selects the next job via `j=$(ls /root/queue/*.sh 2>/dev/null | head -1)`, which orders jobs strictly by ASCII/lexical filename order.
- The job decodes 6 system outputs (`{zeroshot, p1_s43, fuse2_s42} x {short, detailed}`) on the 600-image XM3600 evaluation subset (`data/datasets/xm3600/test_data.json`) into `$NCS_DATA/results/xm3600/xm3600_{zeroshot,p1_s43,fuse2_s42}-{short,detailed}.preds.json` and runs `scripts/xm3600_oiv7.py score --results $O --vs xm3600_p1_s43 --out $O/xm3600_oiv7.json`.

### 1.2 Frozen Input Hashes

| File | SHA-256 | Role |
|---|---|---|
| `data/datasets/xm3600/test_data.json` | `0a613214f95605ff137879f70cb84f8160172c28a650317766ac4a1d9c3b72e8` | 600-image Vietnamese evaluation split (573 with 2 refs, 27 with 3 refs) |
| `data/datasets/xm3600/full_data.json` | `101d24ad98e9dec43625ee425fa1b49aa1bde98f9609945bf5dd4424fef1dacc` | Full 3,600-image Vietnamese XM3600 captions (3,450 with 2 refs, 150 with 3 refs) |
| `data/datasets/xm3600_en/test_data.json` | `3a1bf2ef38a7ba5e23edc2abdb98a4bdd34ad9221e3e5e89aaabcab9204711b6` | Paired 600-image English XM3600 captions (independent English annotator panel) |
| `data/datasets/xm3600_en/full_data.json` | `fd9cda7223dc5029d76a14cc42d594097c3bde2f7ade9005161962d6a2af13b3` | Full 3,600-image English XM3600 captions |
| `data/xm3600/oiv7_labels.json` | `bac3953a511a9793c22e928a29b68ae05dbf9654502abcbe7b64fd9f6d74c8b2` | Open Images V7 human-verified positive and negative image labels |
| `data/xm3600/vi_oiv7_map.json` | `27f2b1ca3f2bf47d43c8f00e8409472c8d571eb720d47b8107a1c77bd208d16a` | Mapping of 82 Vietnamese lexicon classes to OIV7 `pos`/`neg` MIDs |
| `data/xm3600/manifest.json` | `263015f9dc46ebe2cea80055e04ed39baf80a356f4e027cd3756464279135bef` | Build manifest and coverage statistics |
| `data/xm3600_subset.txt` | `f5ab86c7f3126ab6683e97b769e462aa149ca22b081a889d0a0027904d503952` | 600 seeded evaluation image IDs (`seed = 0`) |
| `scripts/xm3600_oiv7.py` | `9a79403f4fc38609282d40082ab7f878133edca8aff9e0dc2462db467b7193f0` | Builder and scorer for XM3600 Vietnamese captions + OIV7 labels |
| `.session_backup/machines/n2/queue/paused/39_xm3600_eval.sh` | `8ab1afccc06b1b6edd6c5b339ed9483c91dd1adff339b88a36b0ae471616596e` | Queued GPU evaluation script (`58_z_xm3600_eval.sh`) |
| `.session_backup/2026-10-14/r11_litmaps/L1/check_coco.json` | `cb21dd257f93a794fa7933c39a994a15825e95f705bdf3dd3e5cc1ad273593aa` | Source of out-of-sample transferred $b$ priors from COCO-2500 |

### 1.3 Pre-Computed Gold Densities ($\bar{G}$) on the 600-Image Evaluation Subset

Using `rescap.chair.objects_in` (113-entry Vietnamese lexicon) for reference captions and `xm3600_oiv7.statuses` (82 mapped classes) for Open Images V7 human-verified labels:

| Gold Variant $g$ | $\bar{G}_{\text{all}}$ ($n=600$) | $\bar{G}_{\text{nonempty}}$ | Non-Empty Images | Empty Share | Prior $b_{\text{COCO-2500}}$ (No Refit) | $M^*_{\text{micro,prior-}b}$ ($\bar{G}_{\text{all}}$ / $\bar{G}_{\text{nonempty}}$) |
|---|---:|---:|---:|---:|---:|---:|
| `refs1_firstk` (slot 0) | `1.4950` | `1.7657` | `508 / 600` | `0.1533` | `0.478` | `1.369 / 1.617` |
| `refs1_randk` (mean 1-ref) | `1.6000` | `1.8831` | `509.8 / 600` | `0.1503` | `0.479` | `1.471 / 1.731` |
| `refs_all` ($2\text{--}3$ refs union) | `2.3483` | `2.5387` | `555 / 600` | `0.0750` | `0.549` (`refs2`) | `2.859 / 3.090` |
| `oiv7_verified` (82 mapped classes) | `2.0417` | `2.5206` | `486 / 600` | `0.1900` | `0.846` (`inst`) | `11.216 / 13.847` |

*(In addition, each evaluation image has a mean of `4.0067` verified-absent mapped classes under OIV7.)*

---

## 2. Frozen Predictions

### 2.1 `(a)` Out-of-Sample and Relative-Form `N1` Sign Predictions (`H6` P2a & `H3` P2)

Across the 6 queued systems (`{zeroshot, p1_s43, fuse2_s42} x {short, detailed}`), let $\text{slope}(g)$ be the OLS slope of $F_1(g)$ (in percentage points) on $\log M$ across the 6 systems (computed via `check_mstar.py` with $B=500$ image-bootstrap draws; for `oiv7_verified`, $P = \text{verified\_precision}$ over verified mapped mentions, $R = \text{pos\_recall}$ over verified positives, and $F_1 = 2PR/(P+R)$):

1. **Out-of-sample transferred-$b$ sign predictions (`H6` P2a)**:
   - Using $b$ transferred without refitting from COCO-2500 (`check_coco.json`: $b_{\text{refs1}} = 0.479$, $b_{\text{refs2}} = 0.549$, $b_{\text{inst}} = 0.846$) and XM3600 $\bar{G}$:
     - **`N1-XM-1 (`refs1`)`**: $\text{slope}(\text{refs1\_randk}) < 0$ (since $M^*_{\text{micro,prior-}b} = 1.471\text{--}1.731$ sits below the 6-system short+detailed median $M \approx 1.8\text{--}2.1$).
     - **`N1-XM-2 (`refs_all`)`**: $\text{slope}(\text{refs\_all}) > 0$ under transferred $b = 0.549$ ($M^*_{\text{micro,prior-}b} = 2.859\text{--}3.090$). *Risk disclosure (`H3` §1a)*: on verbose outputs where reference recall saturates, in-sample $b$ can compress below $0.549$; this is therefore a genuine risky out-of-sample test.
     - **`N1-XM-3 (`OIV7`)`**: $\text{slope}(\text{oiv7\_verified}) > 0$ (since $M^*_{\text{micro,prior-}b} = 11.22\text{--}13.85$ sits far above all 6 systems' $M$).
2. **Relative-form predictions (`H3` P2 / `PD-4 Q5(c)`)**:
   - **`N1-XM-4 (Ordering)`**: $\text{slope}(\text{refs1\_randk}) < \text{slope}(\text{refs\_all}) < \text{slope}(\text{oiv7\_verified})$.
   - **`N1-XM-5 (Relative $M^*$ sign)`**: For each gold variant $g \in \{\text{refs1\_firstk}, \text{refs1\_randk}, \text{refs\_all}, \text{oiv7\_verified}\}$, $\text{sign}(\text{slope}_g) = \text{sign}(M^*_{\text{mixed}}(g) - \text{median } M)$.
3. **Kill Rules (`H6` P2 & `H3` P2)**:
   - If $\ge 2$ of the 3 out-of-sample sign predictions (`N1-XM-1`, `N1-XM-2`, `N1-XM-3`) fail, `N1` is demoted from a core result to an explanatory lemma / diagnostic.
   - If $\text{slope}(\text{refs1\_randk}) \ge 0$ (`N1-XM-1` fails), `N1`'s 1-reference prediction fails in a third setting and the sign-flip claim is dropped per the R11 stop rule.

---

### 2.2 `(b)` `N2` Reference Adjacency Audit on 3-Reference XM3600-vi Images (`H6` P2b & Claim 11 — Completed Pre-GPU)

Before treating XM3600-vi references as independent annotator trials, we run the `N2` adjacent-doubleton test (`c3_n2` protocol) on all XM3600-vi images that have $K = 3$ human captions in `data/datasets/xm3600/raw/captions.zip`:
- **Sample size**: Across all $3,600$ images in `captions.zip`, $3,450$ images have $K=2$ Vietnamese captions and **$150$ images have $K=3$ Vietnamese captions** ($27$ of which fall in the $n=600$ evaluation subset).
- **Exchangeable permutation null ($K=3$)**: Among the $\binom{3}{2} = 3$ caption-slot pairs $\{(0,1), (1,2), (0,2)\}$, exactly $2$ pairs $\{(0,1), (1,2)\}$ are adjacent in file order. Under exchangeable annotator order, the expected adjacent-doubleton share is exactly:
  $$p_{\text{null}}(K=3) = \frac{2}{3} \approx 0.6667 \quad (66.67\%).$$
- **Observed XM3600-vi result**:
  - Across the $150$ 3-reference images in `full_data.json`, there are $90$ doubleton object occurrences ($k_o = 2$ of $3$ captions naming class $o$), of which **$48 / 90 = 0.5333$ (`53.33%`, 95% image-bootstrap CI `[0.4141, 0.6471]`, $B=5000$)** occur in adjacent slots `(0,1)` or `(1,2)`.
  - On the $27$ 3-reference images in the $n=600$ evaluation subset (`test_data.json`), $9 / 17 = 0.5294$ (`52.94%`, 95% CI `[0.2500, 0.8000]`) are adjacent.
- **Verdict (`H6` Claim 11)**: There is **zero positive adjacency excess** on XM3600-vi ($\hat{p}_{\text{adj}} = 0.5333 \le 0.6667$, difference $-13.33\text{ pp}$), in sharp contrast to KTVIC test ($0.710$ vs $0.400$ null, $+31.0\text{ pp}$ / $+77.5\%$ excess from single-writer sequential entry). XM3600-vi passes the `N2` reference-independence check.

---

### 2.3 `(c)` `C3` Two-Caption-Panel Transfer (`XM3600-vi` vs `XM3600-en`) and `refs` vs `OIV7` (`H6` P2c & `H3` P2)

1. **Two-caption-panel transfer (`XM3600-vi` refs vs `XM3600-en` refs, `H3` P2)**:
   - Gold `A`: XM3600-vi human references (`data/datasets/xm3600/test_data.json`, 113-entry Vietnamese lexicon).
   - Gold `I_panel`: XM3600-en human references on the exact same 600 images (`data/datasets/xm3600_en/test_data.json`, independent English annotator panel and guideline, aligned to the shared 82-class / COCO-80 concept vocabulary).
   - **Prediction (`C3-XM-Panel`)**: Across count-matched contrasts (MCP / frontier residual $\Delta \rho$) among `zeroshot`, `p1_s43`, and `fuse2_s42`, the OLS-through-origin transfer slope $\kappa(A \to I_{\text{panel}})$ satisfies $\kappa < 1$ with 95% image-bootstrap CI upper bound $< 1$.
   - **Kill rule**: If the 95% CI of $\kappa(A \to I_{\text{panel}})$ includes $1$, partial transfer between caption panels is reported as KTVIC-specific (`H3` §2 P1/P2).
2. **Reference gold vs OIV7 verified truth labels (`xm3600_oiv7.py score --vs xm3600_p1_s43`, `H6` P2c)**:
   - **`C3-OIV7-1`**: KTVIC SFT adapters (`p1_s43-short`, `fuse2_s42-short`) raise reference precision $P_{\text{refs}}$ over `zeroshot-short` on XM3600-vi captions, but their OIV7 `verified_precision` gain over `zeroshot-short` is strictly smaller than their reference precision gain ($\Delta \text{vP}_{\text{OIV7}} < \Delta P_{\text{refs}}$).
   - **`C3-OIV7-2`**: Detailed decoding (`zeroshot-detailed`, `fuse2_s42-detailed`) increases OIV7 `pos_recall` over short decoding ($\Delta \text{pos\_recall} > 0$, 95% CI $> 0$) while decreasing reference precision $P_{\text{refs}}$ ($\Delta P_{\text{refs}} < 0$).
   - **`C3-OIV7-3`**: Among reference-false mapped mentions (`ref_false_mapped`, mentioned by the model on a mapped class but absent from the image's XM3600-vi references), the OIV7 verified-present share `oi_present / (oi_present + oi_absent)` is higher for SFT short models (`p1_s43-short`, `fuse2_s42-short`) than for `zeroshot-detailed`.
