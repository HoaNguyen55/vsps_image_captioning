# Pre-Registration: R12 H1 Proposals G2 (Polaris-COCO) and G3 (DOCCI-Critique) Human-Judgment Replications

**Frozen At:** 2026-10-14 (strictly BEFORE downloading or inspecting any `yuwd/Polaris` or `google/DOCCI-Critique` data files).  
**Mandate:** `PD-4 Q5(b)` and `manuscript/research_r12/H1/REPORT.txt` §2 Proposals G2 & G3.  
**Execution Environment:** CPU-only (`nice -n 19`, `OMP_NUM_THREADS=1`, `python3 -I` on untrusted downloads in `/tmp/claude-1000/-mnt-d-vsps-image-captioning/755eae04-5e4c-4ce1-ab21-d4bc106761ee/scratchpad/r12/H1/dl/`).

---

## 1. Proposal G2: `Polaris-COCO` Confirmatory Replication (`yuwd/Polaris`, BSD License)

### 1.1 Data & Object Pipeline
- **Dataset:** `yuwd/Polaris` (`Polaris` CVPR 2024; candidate captions rated for overall human quality on a 1–5 scale, `human_score`).
- **Primary Confirmatory Split:** `test` split mapped to COCO `val2014` `cocoid` via normalized Karpathy reference matching (`karpathy_refs` in `h1_pilot.py`). Secondary splits (`val`, `train` overlapping COCO `val2014`) are reported for completeness but do not govern the confirmatory verdict.
- **Object Extractor:** E1's CHAIR re-implementation (`data/coco_probe/chair_synonyms.txt`, 80 COCO classes, distinct class set per caption, identical to `h1_pilot.py`).
- **Gold Levels ($g$):**
  - `refs1`: 1 random reference drawn from `refs4` (`NDRAW = 20`, `seed = 0`, averaged across draws as in `h1_pilot.py`).
  - `refs2`: 2 random references drawn from `refs4` (`NDRAW = 20`, `seed = 0`).
  - `refs4`: up to 4 COCO reference captions for image $i$ (excluding any reference identical to a candidate caption on image $i$).
  - `inst`: COCO `instances_val2014.json` classes for image $i$.
  - `full`: `inst | refs4`.
- **Metrics:**
  - `M`: number of distinct COCO-80 classes named in candidate caption (`|cl|`).
  - `negCHAIR` ($1 - \text{CHAIR}_i - 1 = -\text{FP}_g / \max(M, 1)$).
  - `F1` ($2\text{TP}_g / (M + G_g)$).
  - `z`: count-conditioned TP residual $\text{TP}_g - \bar{\text{TP}}_g(m)$ with $m = \min(M, 6)$, identical to `h1_pilot.py`.
- **Unit & Bootstrap:** Within-image candidate caption pairs $(a, b)$; pairwise concordance `acc(X -> overall) = concordant / (concordant + discordant)` over untied pairs (`dX != 0` and `dH != 0`), with `NBOOT = 2,000` image-clustered bootstrap resamples (`seed = 0`, 95% percentile CI).

### 1.2 Frozen Hypotheses & Kill Rule (G2)
- **`H-a` (Gold completeness drives human validity of object precision):**
  $$\text{acc}(-\text{CHAIR}_{\text{full}} \to \text{overall}) - \text{acc}(-\text{CHAIR}_{\text{refs1}} \to \text{overall}) > 0$$
  with 95% image-bootstrap CI lower bound $> 0$ on the `test` split (evaluated both on all pairs `all` and on count-differing pairs `cdiff`).
- **`H-b` (Count-equal pairs agree with humans more than count-differing pairs):**
  Under `full` gold on the `test` split,
  $$\text{acc}_{\text{ceq}}(-\text{CHAIR}_{\text{full}} \to \text{overall}) - \text{acc}_{\text{cdiff}}(-\text{CHAIR}_{\text{full}} \to \text{overall}) > 0$$
  with 95% image-bootstrap CI lower bound $> 0$.
- **`H-c` (Approximate human count-neutrality in the short-caption COCO regime):**
  Caption-level and within-image demeaned Pearson correlation $\text{corr}(M, \text{overall}) \in [-0.10, +0.10]$ on the `test` split.
- **Secondary Diagnostics (G2):** Replicate `P1b` (`acc(z_full -> overall) - acc(-CHAIR_full -> overall)` on `cdiff`) and `P2b/P2c` (`F1` preference for larger $M$ across `refs1 -> refs4 -> full` vs human preference for larger $M$).
- **Kill Rule (G2):** If `H-a` 95% CI lower bound $\le 0$ on the `test` split, `G2` is **KILLED**.

---

## 2. Proposal G3: `DOCCI-Critique` Long-Caption LVLM Test (`google/DOCCI-Critique`, CC BY 4.0)

### 2.1 Data & Object Pipeline
- **Dataset:** `google/DOCCI-Critique` (`metadata.csv`, CC BY 4.0; 100 DOCCI images $\times$ 14 VLMs = 1,400 multi-sentence paragraphs, ~10,216 sentence rows).
- **Paragraph Reconstruction & Human Factuality (`P_human`):**
  - Group sentence rows by `(image_id / file_name, Captioner_VLM)` in sentence order to reconstruct each of the 1,400 paragraphs $(i, s)$ ($i \in \{1..100\}$, $s \in \{1..14\}$).
  - Primary human factuality score `P_human_sent_maj(i, s)`: share of sentences in paragraph $(i, s)$ rated factual/accurate by a majority of raters (Per `H1/REPORT.txt` §2 G3: *"Per paragraph: human precision = share of sentences rated Accurate"*).
  - Secondary human factuality score `P_human_rater_mean(i, s)`: mean fraction of `Accurate` ratings across all sentence $\times$ rater annotations in paragraph $(i, s)$.
- **Object Mentions & Reference Gold:**
  - Extract ordered distinct COCO-80 classes $u_{i,s} = (c_1, \dots, c_{M_{i,s}})$ from the full paragraph text of $(i, s)$ using E1's CHAIR matcher (`M_{i,s} = |u_{i,s}|`).
  - Gold $G_i$: distinct COCO-80 classes extracted from the ground-truth DOCCI human reference description for image $i$ (`1` dense reference description; gold sparsity on COCO-80 is explicitly noted as a caveat).
  - Raw object precision of paragraph $(i, s)$: $P_{\text{obj,raw}}(i, s) = 1 - \text{CHAIR}(i, s) = |u_{i,s} \cap G_i| / \max(M_{i,s}, 1)$ (for $M_{i,s} > 0$).
- **Matched-Count Object Precision across the 14 VLMs:**
  - **Primary (`MCP` pairwise prefix matching, as in `H1` §2 G3 *"pair VLMs on the same image, first-k classes"* and `E1`/`H3` `h3_c3.py`):** For each image $i$ and each ordered VLM pair $(s, t)$, let $k^*_{i,s,t} = \min(M_{i,s}, M_{i,t})$. Over images with $k^*_{i,s,t} \ge 1$, compute the matched-prefix precision difference:
    $$\Delta P_{\text{MCP}}(s, t) = \frac{\sum_i \left(|u_{i,s}[:k^*_{i,s,t}] \cap G_i| - |u_{i,t}[:k^*_{i,s,t}] \cap G_i|\right)}{\sum_i k^*_{i,s,t}}$$
    and define each VLM's matched-count score $S_{\text{MCP}}(s) = \frac{1}{13}\sum_{t \neq s} \Delta P_{\text{MCP}}(s, t)$ (the Borda/net-advantage score across all 13 opponents at per-image matched prefix count $k^*$).
  - **Secondary count-matched estimators (reported alongside `MCP` in a specification table):**
    1. Fixed prefix budget $P_{\text{obj}@k}(s)$ at $k = \text{median}(M)$ across paragraphs;
    2. Count-residualized precision $z_P(i, s) = P_{\text{obj,raw}}(i, s) - \bar{P}_{\text{obj,raw}}(M_{i,s})$ averaged per VLM $s$.

### 2.2 Frozen Hypotheses & Kill Rule (G3)
- **`G3-(i)` (Per-VLM human factuality falls with object count $M$):**
  - Across paragraphs within each VLM $s$, human factuality `P_human` decreases with $M$: the mean (and median) across the 14 VLMs of the within-VLM OLS slope of `P_human` on $M$ is $< 0$, and the pooled within-VLM (VLM-fixed-effect) OLS slope of `P_human` on $M$ is $< 0$ with 95% image-clustered bootstrap CI upper bound $< 0$.
- **`G3-(ii)` (Matched-count object precision improves 14-VLM ranking agreement with human factuality):**
  - Across the $N_{\text{sys}} = 14$ VLMs, let $\bar{P}_{\text{human}}(s) = \frac{1}{100}\sum_i P_{\text{human}}(i, s)$ and $\bar{P}_{\text{obj,raw}}(s)$ be the VLM-level raw object precision (micro $\sum_i \text{TP}_{i,s} / \sum_i M_{i,s}$ and macro mean of $P_{\text{obj,raw}}(i, s)$).
  - The Kendall rank correlation $\tau$ between the 14-VLM matched-count object-precision ranking $S_{\text{MCP}}(s)$ and $\bar{P}_{\text{human}}(s)$ exceeds the raw object-precision Kendall $\tau(\bar{P}_{\text{obj,raw}}, \bar{P}_{\text{human}})$ by at least $+0.10$:
    $$\Delta\tau = \tau(S_{\text{MCP}}, \bar{P}_{\text{human}}) - \tau(\bar{P}_{\text{obj,raw}}, \bar{P}_{\text{human}}) \ge +0.10$$
    (Also report pairwise VLM-pair direction accuracy across all $\binom{14}{2} = 91$ VLM pairs and within-image pairwise concordance across all $100 \times 91 = 9,100$ `(image, VLM_A, VLM_B)` pairs.)
- **Kill Rule (G3):** If $\Delta\tau \le 0$ on `G3-(ii)`, **KILL** the claim that matched-count object precision improves VLM ranking agreement with human factuality on `DOCCI-Critique`.
