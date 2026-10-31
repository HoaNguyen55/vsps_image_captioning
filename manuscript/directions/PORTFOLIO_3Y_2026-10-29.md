# Three-year publication portfolio, 11/2026 – 10/2029 (PI-1029f synthesis, 2026-10-29)

> **AI opinion, not expert-validated, not a ruling.** This file synthesises the four scout files, the A/B/C pivot files, CC-158 and the proposal v5. Nothing was run, edited or committed, and no GPU was used. Every GPU item below still needs its own gate rule, a ruling at ≥ 90% (PI-1029e) and a gatekeeper commit before it runs. Quartiles are SJR 2025 values copied from `manuscript/cfp/05_two_paper_targets.json`, `04_rolling_journals.json` and `venue_fit_2026-10-28.json`, and are marked **verify** because they must be rechecked on scimagojr.com in the year of acceptance. Confidence figures labelled "scout" are the scout's own; the others are this synthesis's.

Inputs read in full: `SCOUT_BRIEF.md`; `2026-10-29_scout{1_lit_gaps,2_vietnamese,3_applications,4_assets}.md`; `manuscript/pivots/2026-10-29_{A,B,C}_pivots.md`; `CC-158.txt`; `CC-158_codex_review.md`; `DeCuong_NCS_LHU_2026-10_v5.md`; `REGULATIONS_PUBLICATION_REQUIREMENTS.md`. Spot checks: LOG l.690–698 (PI-1029c/e/f); `prereg/2026-10-18_tier3_S5.md` (it mentions only OpenViVQA/EVJVQA, as excluded training images, so MTVQA, ViTextVQA, VinText and ViOCRVQA are unused by this team); `cfp/*.json` quartiles.

## 0. Three facts that shape the whole plan

1. **"Counts" means published before the thesis evaluation.** TT 18 Art. 14.1.c counts work «được công bố», and LHU's 3×Q1 exemption counts published work too. A Q1 review with one revision takes 6–12 months, or longer. **A first Q1 submission after about 03/2028 adds almost nothing to the count.** Proposal v5 puts all three Q1 papers late: B6 05/2028, B4 11/2028 and B5 05/2029. **B5 cannot count, and B4 is unlikely to.** The Q1 attempts must move into 2027.
2. **The regulatory floor is separate from the Q1 goal.** It is ≥ 2.0 points, as first or corresponding author, from WoS/Scopus outlets. **FAIR 2026 probably does not count**, because its proceedings are national and not shown to be Scopus-indexed (REGULATIONS §3). The cheapest path is A or C at a SCIE/Scopus Q2 journal (1.75) plus one Scopus-indexed conference paper in 2027 (1.0), which gives 2.75. This floor must not depend on the Q1 bets.
3. **A, B and C are Q2 recovery bets, not Q1 routes** (CC-158; Codex: P(Q2) A 25%, B 15%, C 25%). Every Q1 paper must therefore come from a new line.

## 1. Research lines

The scout directions were merged into three new lines plus the current A/B/C/D stream (L0). Two scout directions were dropped or set aside:
- Scout 3 D3 (VizWiz) is folded into L1 as an application section.
- Scout 3 D2 (VinDr-CXR) is held as reserve direction L4 (not counted as a line). It is gated by credentials and its fit is about 7.

### L1. Vietnamese tone-mark fidelity in text-in-image descriptions: diagnose, explain, fix

Merges scout 1 D1, scout 2 D2, scout 3 D1 and scout 2 D1. Three scouts reached this line independently, which is weak but real evidence that the gap exists.

- **Gap.** Text-centric LVLM benchmarks that include Vietnamese (MTVQA 2405.11985, SEA-Vision 2603.15409, VMMU 2508.13680) report only aggregate accuracy or CER. Nobody separates *diacritic- or tone-only* errors on a correctly read base letter from reading errors, explains where they come from (resolution, language prior or tokenizer), or fixes them in general LVLMs. In Vietnamese such an error changes the word; the scout 2 CPU pre-pilot found 74% of syllable types ambiguous once stripped.
- **Nearest threats, and how this line differs from each.**
  - **semCER 2610.20461** (2026-10-14) already *measures* diacritic damage in OCR, using an LLM-judge severity score. A "first diacritic error measure" claim is therefore gone. L1 instead offers a deterministic NFD decomposition against human gold, applied to LVLM answers and captions, plus causal manipulations and a fix.
  - **ViTextCaps/PhonoSTFG 2604.27712** trains a phonological fusion captioner; it does not diagnose general LVLMs. Its data is reserved for C and is **not used here**.
  - **VinText dictionary-guided recognition** (CVPR 2021) fixes specialist recognisers, not LVLMs. "A dictionary for LVLMs" alone would be a +0.5, so the claim must rest on the decomposition, the explanation and stability across backbones.
- **Novelty claim (Q1 form).** Observe → explain → fix (p300 Pattern 2).
  - Observe: a new error class (diacritic-only), its share of errors, and how much it moves published backbone rankings.
  - Explain: three manipulations on fixed items: crop/resolution, the no-image language prior, and tokenizer fertility. The explanation is backed by a cross-language dose-response (vi against fr/de/it in MTVQA).
  - Fix: training-free, glyph-verified tone re-ranking over the closed orthographic candidate set.
  - Known-order corruptions of gold (Pattern 8) validate the measure. They are corruptions of existing gold, not new labels.
- **Why it can reach Q1.** The language is a *necessary* test case: Vietnamese is the densest-diacritic Latin-script language in these benchmarks. The line has a mechanism and a fix, not just a number. ESWA has a direct Vietnamese scene-text precedent (ViTextVQA, doi 10.1016/j.eswa.2025.130839), and the application value is concrete (signs, menus, medicine labels, screen readers).
- **Data (public; no new gold; AI output is never evidence).**
  - ViTextVQA: 16,762 images and 50,342 QA pairs with human-transcribed answers. The HF mirror is tagged CC BY-NC 3.0; the official licence and "on request" status are **to check**.
  - MTVQA: CC BY-NC 4.0, native annotators. The Vietnamese test count is **to check**.
  - VinText: 2,000 images and about 56k human transcriptions. The data terms are **unverified**; AGPL-3.0 is the code's licence.
  - ViOCRVQA: the gold comes from bookstore metadata, so it is a secondary source only, on a pre-registered subset, or it is dropped.
  - ViSignVQA (2512.22218): licence **to check**.
  - English nulls (no tone layer): TextVQA val and TextCaps val.
  - The OCR lattice from an off-the-shelf spotter may be used only as a method input or training signal, never as gold.
- **Unused test sets it needs (status: all unspent; owners in §2.3).** ViTextVQA test and MTVQA test (vi, fr, de, it) → L1-P1. VinText test → L1-P2. A pre-fixed held-out pool for L1-P3 needs a ruling (scout 2 Q-S2-1).
- **Dev pilot and kill criterion (≤ 12 GPU-h, train/dev splits only, 3 backbones).** Kill or demote to a conference paper if either holds:
  - diacritic-only errors are < 10% of wrong transcription-type answers (scout 1's denominator rule) for every backbone;
  - re-ranking gains < +1.0 EM with bootstrap CI_lo ≤ 0 on ≥ 2 of 3 backbones.

  The "raise" threshold is a diacritic-only share ≥ 20% that changes the backbone ranking, plus a re-rank gain ≥ +2 on 3 backbones. The L1-P2 span pilot (≤ 8 GPU-h, VinText train slice) has its own kill: a diacritic-corrupted span rate < 5% for both 7–8B models, or repair not beating "OCR tokens in prompt" by 2×MDE (scout 3 K1/K2).
- **Papers.** L1-P1 (Q1), L1-P2 (Q1 attempt), L1-P3 (PRL Q1 attempt, short), CF1 (kit, Scopus conference).
- **Shared failure mode.** If diacritic errors turn out to be rare in strong LVLMs, L1-P1, L1-P2 and CF1 all weaken together. The L1-a pilot is therefore the first gate for the whole line.

### L2. Cross-lingual hallucination: measurement artefact first, then alignment transfer

Merges scout 1 D2, scout 4 D3, scout 1 D3 and **A pivot Option 3**. A Option 3 and scout 1 D3 become **one** paper (L2-P2), not two.

- **Gap.** Every published non-English LVLM hallucination number rests on GPT- or Google-translated test items: MHR 2408.00550 (ACM TOMM 2026, 13 languages, no Vietnamese) and CLAIM 2506.11073 (7 languages, no captioning). The two give conflicting causes. Neither controls translation artefacts or caption length and object count, which the survey 2404.18930 §4 names as a CHAIR confound. English-only multimodal DPO transfer has been tested only for text LLMs (2406.16235, 2404.12318).
- **Novelty claim.** L2-P1 decomposes the vi−en hallucination gap into three parts, using language-invariant instance gold and deterministic templated probes (from A's COCO-80 lexicon, no MT):
  - (i) the MT pipeline;
  - (ii) verbosity and object count, using A's count control;
  - (iii) residual grounding loss.

  It also runs a registered test of which published explanation survives. L2-P2 is a controlled test of whether English-only multimodal DPO transfers to Vietnamese, and at what cost: language drift and the object-count channel. Its label-free fix is language-consistency pairs built from language ID.
- **Why it can reach Q1.** The topic is already Q1 in CS (MHR in TOMM), and a measurement critique of a Q1 literature is a classic Q1 form. Either outcome is publishable, but the kill rule below demotes the mundane outcome.
- **Data.** Gold is instance annotations; templated Vietnamese probes are deterministic.
  - RLAIF-V (83,132 pairs, cc-by-nc-4.0 per its HF tag) and HA-DPO pairs serve only as a training signal.
  - Pilots use only spent sets in a dev role: UIT-ViIC test (231 images, COCO gold) and XM3600 (OIV7 labels).
- **Unused test sets.**
  - L2-P1 → **OIV7 val minus the 456 XM3600 ids (41,164 images)**: human-verified labels, images CC BY 2.0, annotations CC BY 4.0. Its features exist from W25, which was a dedup pass, not a look.
  - **Cost.** Scout 1's "about 30 GPU-h" assumed 5k images, which the full-splits rule does not allow. The full split costs 41,164 × 3 backbones × 2 languages × 1.5 s ≈ **105 GPU-h** for short captions, and about 225 GPU-h for detailed captions (3.25 s per image). This is PI Q5.
  - L2-P2 → **AMBER generative (1,004 images)**. AMBER is fallback-only under CC-147 r4, so it needs a new PI line.
- **Dev pilots and kill criteria.**
  - **L2-a (≤ 15 GPU-h, UIT-ViIC test + XM3600, 3 backbones).** First a 0-GPU matcher-parity check: run the VI matcher on the human VI captions and the CHAIR matcher on the human EN captions of the same images. If they differ by > 2 points, stop until the matcher is fixed. Then **demote L2-P1 to TALLIP** if native and translate-then-score CHAIR_i agree within ±1 **and** count-matching moves the vi−en gap by < 20%, whatever the residual gap.
  - **L2-b (≤ 20 GPU-h, 2B backbone, spent dev set).** Kill if English DPO transfers ≥ 80% with < 5% drift (there is then nothing to fix), or if it has no effect in either language.
- **Papers.** L2-P1 (Q1), L2-P2 (Q1 attempt), CF2 (Vietnamese templated-POPE and native-CHAIR kit, conference).
- **Overlap to rule.** L2-P1's "English-anchored verification" fix is close to C's §3.4 verifier. Recommended: **L2-P1 stays diagnosis plus a registered which-explanation test, with no verifier fix**. The verifier belongs to C and B5, which avoids slicing.

### L3. Verified training and repair at matched coverage (the proposal's MT4 spine, un-parked)

Scout 4 D2 plus proposal B6, B4 and B5.

- **Gap.** Hallucination-reduction fine-tuning is reported as lower CHAIR without controlling how many objects the caption names. No method has shown a reduction that survives a matched-coverage comparison against a truncation frontier and an unedited self-training control, on an unseen gold-backed set, in a low-resource language. Prior work: STIC 2405.19716, ReCaption 2312.01701, SENTINEL 2507.12455 and HallE-Control 2310.01779, which claims coverage is maintained but runs no matched-coverage analysis.
- **Novelty claim.** Combined claim: "verified training beats truncation at equal coverage, Vietnamese primary with an English arm." It uses:
  - A's count control as the instrument;
  - the FAIR verifier as a gold-free arm (needs a PREREG amendment beyond §8);
  - KV-4,224 instance gold, which needs no Vietnamese references.

  Alone this is setting novelty (about 3/5, as the committed PREREG itself narrows it). The registered matched-coverage frontier is what lifts it.
- **Why it can reach Q1.** It is the only line that already holds a **committed, unspent, gold-backed one-look test** (KV-4,224, commit 70c898a). About 17 GPU-h of Gate 1 work has already been spent, and the `adapters/gold` and `adapters/unedited` arms survive.
- **Data.**
  - Training: UT-2,402 minus the 10 W25 exclusions.
  - Dev: val 924.
  - Test: KV-4,224.
  - COCO annotations are CC BY 4.0. UIT-ViIC is research use (PI-1026bc).
- **Unused test sets.**
  - L3-P1 → KV-4,224, committed.
  - B4 → **COCO Karpathy restval (about 30.5k images)**, with Visual Genome relationships on the overlapping images as relation gold. The VG overlap count and licence are **to verify**.
  - B5 → **Objects365 v2 val**. Its size and licence are **to verify**.
- **Dev pilot and kill criterion.**
  - L3-a: resume K2 Gate 1 from the surviving adapters (skip train_det, a dev-only arm) and decode val 924 with base, gold and unedited. Cost about 3–6 GPU-h.
  - **Kill** (MT4 PREREG K1+K6) if gold − unedited at matched R(K) has a CHAIR_i CI that contains 0, or if gold does not beat the truncation frontier (G4). L3-P1 then drops to Q2.
  - Needs, in this order: the PI un-parks MT4 (it was parked by PI-1029c's reading), a judge rules the resume, and Gate 1 `NOT_AFTER` (2026-11-06T12:00Z) is amended.
- **Papers.** L3-P1 = B6 (Q1). B4 (Q1 attempt, moved earlier). B5 (Q1 attempt). B5 owns "repair-not-delete" for objects and relations. **Text-span repair belongs to L1-P2**, which cites B5's framing; B5 does not cover text spans.

### L0. Current stream (A, B, C, D), as decided in CC-158

| Paper | Direction (CC-158) | Status |
|---|---|---|
| A | Options 1+2: few-reference estimator plus salience excess test, as a companion prereg on the P50 decodes | 0 extra GPU-h; P50 cap 8 GPU-h on M1; P50 held until the companion commit or 11-08 12:00Z |
| B | Option 1: same-image panel swap | Gated on D0 (CPU), the PI's B+D line and the PI's H carve-out; about 40–65 GPU-h on M2 |
| C | Option B: SCD with the 2×2 embedded, only if ViTextCaps arrives | Otherwise Option E on 11-12 (Q3); about 60 GPU-h dev on M2 and 37 GPU-h test on M1 |
| D | VJCS (Q3), the default if B+D is refused | If B+D is approved, D is absorbed into B and leaves the count |

Scout 4 D1, an A+B estimator-and-panel synthesis at IP&M, is **not** a separate paper now (CC-158 r5: no A+B merge). It is listed in §2.4 as a 2028 conditional Q1 lever, allowed only if A and B both PASS and only as new work on new data.

### Reserve direction (not a line): L4, Vietnamese chest X-ray findings verified against radiologist boxes

Scout 3 D2. VinDr-CXR test (3,000 images, 5-radiologist consensus) would be fresh. The line is gated by PhysioNet credentials and the DUA, which must allow rented GPUs and open-weight models only. Venue fit is about 7. Scout confidence is 30% if access is granted and 10% unconditionally. It is kept as a possible extra Q1 attempt for 2028 (PI Q9), not planned.

## 2. Paper table

### 2.1 Papers

Rules for the table:
- **Q-tier** is the SJR quartile in a Computer Science category (verify).
- **P(Q1)** is this synthesis's probability that the paper is *published* in a CS-Q1 journal before about 07/2029, including its Q1→Q1 cascade. It is unconditional on pilots: AI opinion, discounted from the scouts' own figures.
- **GPU-h** is RTX 3090 hours for the full paper, not the pilot.
- **Fit provenance.** The fit ≥ 8 bar is *not evidenced* where the tag is not [s]. Score every [b] and [e] fit with the `venue_fit` rubric before submission.
  - [s] scored for this direction by a scout or venue_fit;
  - [b] borrowed from a venue_fit entry scored for another paper;
  - [e] this synthesis's estimate, unscored.

| # | Paper (line) | Distinct contribution (no slicing) | Venue: primary → cascade (fit /10) | CS quartile (verify) | Target | Submit | GPU-h | P(Q1) | Depends on |
|---|---|---|---|---|---|---|---|---|---|
| B0 | FAIR 2026 (published) | Verified-proposition supervision (VSPS) | FAIR 2026, IEEE | not WoS/Scopus (probably 0 toward the 2.0) | – | done | – | – | – |
| 1 | **A** (L0) | Few-reference to complete-gold estimator plus reporting-bias excess, on PASCAL-50S | SPIC (8 [s]) → VJCS | Q2 CV&PR | Q2 | 12/2026 (date of record 12-21) | ≤ 8 | 0 | Companion prereg W1–W3; P50 key match |
| 2 | **B** (L0) | Panel dependence of score and scaling slope on the same images (KTVIC vs OpenViIC) | LRE (8 [s]) → TALLIP | Q2 in CS Applications (Q1 only in Linguistics and LIS) | Q2 | 12/2026–01/2027 | 40–65 | 0 (see PI Q6) | D0, PI B+D, PI H |
| 3 | **C** (L0) | SCD: style examples plus verified content hints, with an equal-k random control and LOSO | TALLIP (8–9 [s]) → VJCS | Q2 CS (misc.) | Q2 (Q3 if Option E) | 01/2027 | about 97 | 0 | ViTextCaps by 11-12; Flickr30K line (CC-158 r4) |
| 4 | **D / B3b** (L0) | Multi-seed Vietnamese data curve (B-1), with D-α reported as INCONCLUSIVE | VJCS (8 [s]) → FAIR 2027 | Q3 | Q3 | 03/2027 | 0–5 | 0 | Absorbed into B if B+D is approved |
| 5 | **L3-P1 = B6** | Verified self-distillation beats truncation at matched coverage; VI primary, EN arm | IP&M SI MMLowRes (about 8 [s] scout 4; deadline 2027-08-31, verify) → IEEE TMM (8 [b]) → TALLIP | Q1 CS Applications | **Q1** | 04–05/2027 | ≤ 170 cap (about 17 spent) | 0.30 | PI un-park; Gate 1 resume ruling; KV freeze |
| 6 | **L1-P1** | Diacritic-only error class in LVLM text-VQA, its cause (3 manipulations plus language dose), training-free tone re-ranking | ESWA (about 8 [s] scout 3; ViTextVQA precedent) → Pattern Recognition (7 [s], fit < 8) → SPIC | Q1 AI / CS Applications | **Q1** | 06/2027 | about 50 | 0.30 | L1-a pilot; ViTextVQA access; MTVQA-vi count |
| 7 | **L2-P1** | Multilingual hallucination gap decomposed into MT artefact, count and residual, on language-invariant gold; which published cause survives | ACM TOMM (9 [s] scout 1; MHR precedent) → IJMIR (8 [s] scout 1) → TALLIP | Q1 in Computer Networks and Communications / Hardware and Architecture (both SJR CS categories; verify) | **Q1** | 08/2027 | 105–225 (full OIV7 val) | 0.30 | L2-a pilot; OIV7 assignment; full-split decision (Q5) |
| 8 | **L1-P3** | Image as disambiguator: diacritic-free VI text → image retrieval and image-conditioned restoration | Pattern Recognition Letters (8 [e], short; cfp gave 3/5 for A/B/C) → TALLIP | Q1 in CV&PR, Q2 in AI (cfp/04, verify) | Q1 attempt | 10/2027 | 40–60 | 0.12 | Eval-pool ruling (Q-S2-1); scout 2 kill (ΔR@1 < 2 **and** < 25% residual fixed) |
| 9 | **L1-P2** | Span-level fabricated and diacritic-corrupted text in free VI descriptions; repair to the OCR lattice instead of deletion (equal text coverage) | IJMIR (8 [b], scored by scout 1 for L1-P1) → IEEE TMM (8 [b]) → Multimedia Systems (Q2 in CS) | Q1 all categories (IJMIR) | Q1 attempt | 12/2027 | about 60 | 0.15 | L1-b pilot; VinText terms; L1-P1 instrument |
| 10 | **L2-P2** (A Opt 3 + scout 1 D3) | Does English-only multimodal DPO transfer to VI, does it "say less" (object-count channel), and a fix with language-consistency pairs | IEEE TMM (8 [b]; scout 1's TOMM 8 is taken by L2-P1, and two TOMM papers in one year is avoided) → Neurocomputing (fit < 8) → TALLIP | Q1 CS Applications | Q1 attempt | 02/2028 | about 150 (one 7–8B plus the 2B pilot; scout 1's 250–400 was for 2 backbones) | 0.12 | L2-b pilot; scoop check; AMBER PI line |
| 11 | **B4** (L3) | Region-grounded relation propositions that can verify spatial relations (0/26,795 SUPPORTED in FAIR) | CVIU (8 [b]) → Pattern Recognition (7 [e]) | Q1 CV&PR | Q1 attempt | 06/2028 | about 120 (estimate) | 0.08 | COCO restval + VG relations (verify); MT1.2 pilot |
| 12 | **B5** (L3) | Agentic repair or neutralise instead of delete, for objects and relations, at matched coverage | Image and Vision Computing (8 [b]) → KBS (7 [s] scout 3) | Q1 CV&PR | Q1 attempt (too late to count) | 11/2028 | about 100 (estimate) | 0.03 | B4; Objects365 v2 val (verify) |
| 13 | **CF1** (L1) | Diacritic-aware text-VQA scoring kit plus known-order corruption validation (resource only; no LVLM ranking claim) | KSE / SoICT / RIVF / MAPR 2027 (Scopus proceedings: **verify per edition**) | conference | Scopus conf. (1.0 pt) | 06–09/2027 | ≤ 5 | – | Must precede L1-P1 or be cited as its instrument |
| 14 | **CF2** (L2) | Vietnamese templated-POPE and native-CHAIR kit with matcher-parity validation (resource) | LREC 2028 (deadline about 10/2027, weak basis) or SoICT 2027 | conference | Scopus conf. | 10/2027 | ≤ 5 | – | L2-a matcher parity |

That is 14 rows plus the thesis. Over three years this gives four Q2–Q3 journals (A, B, C, D), four front-loaded Q1 attempts (5, 6, 7, 8) submitted by 10/2027, four later Q1 attempts (9–12) and two Scopus conference papers.

### 2.2 Anti-slicing boundaries (one estimand, one test set and one method per paper)

- **L1-P1 vs L1-P2.** L1-P1 covers VQA *answers*: the error decomposition, its causes and token-level re-ranking, scored on ViTextVQA and MTVQA tests. L1-P2 covers *free descriptions*: span-level fabrication and corruption, and lattice repair at equal coverage, scored on the VinText test.
- **L1-P3** is the reverse direction: the query text is degraded and the image is the context. It has no LVLM reading claim.
- **CF1** is the instrument only. It makes no model claim, and the L1 papers cite it.
- **L2-P1 vs L2-P2.** L2-P1 is diagnosis only, at inference. L2-P2 is training (DPO transfer). They have different test sets (OIV7 val and AMBER).
- **L3-P1 vs B5 vs C.** L3-P1 is training. B5 is inference-time agentic repair. C is prompting. The FAIR verifier is reused and cited, not re-claimed.
- **A vs L2.** A owns the gold-incompleteness estimator and the count control. L2 uses the count control as a cited instrument.
- **Judge check needed.** Whether CF1/CF2 count as separate contributions or as salami (PI Q12).

### 2.3 Test-set ledger (each unspent set has exactly one owner)

| Set | Gold | Status | Owner |
|---|---|---|---|
| PASCAL-50S | 50 refs + V20 labels | unspent, PREREG uncommitted | A |
| KV-4,224 (COCO Karpathy val) | COCO instances | committed unspent | L3-P1 |
| ViTextCaps test | human captions | release unverified | C only (scout 3 Q3) |
| Flickr30K Karpathy test | human captions | unscored; A read its references (disclose) | C (CC-158 r4, needs PI line) |
| H = 500 KTVIC-train ∩ OV-train-only | two human panels | carve-out | B (needs PI line, W5) |
| ADE20K SceneParsing val (2,000) + LN-ADE val | pixel labels + narratives | unused (A-T1 tier 3, CC-170) | A |
| AMBER generative (1,004) | object annotations | fallback-only (CC-147 r4) | L2-P2 (needs new PI line) |
| OIV7 val − 456 XM ids (41,164) | human-verified labels | features only (W25 dedup) | L2-P1 |
| COCO Karpathy restval (about 30.5k) + VG relations | instances + relations | feature cache only | B4 (VG overlap: verify) |
| Objects365 v2 val | instances | size and licence to verify | B5 |
| ViTextVQA test (about 10k QA) | human transcriptions | unused | L1-P1 |
| MTVQA test vi/fr/de/it | native annotators | unused (tier3_S5 checked) | L1-P1 |
| TextVQA val / TextCaps val | human | unused | L1-P1 / L1-P2 English null |
| VinText test | human transcriptions | unused | L1-P2 |
| ViOCRVQA test | metadata gold | flagged | L1-P1 secondary pre-fixed subset, or dropped (judge) |
| ViSignVQA test | human QA | licence to check | reserve (L1 replication) |
| VinDr-CXR test (3,000) | 5-radiologist consensus | access-gated | L4 reserve |
| VizWiz val (7,750) | 5-vote quality flags | no VI gold | unassigned (L1-P2 application section only, descriptive) |
| UIT-ViIC train pool | VI + EN human captions | used only for training adapters | L1-P3 evaluation pool, **needs ruling** |

**Image-level rule.** KV-4,224, COCO restval, the UIT-ViIC train pool and UT-2,402 all come from COCO. Before any decode, run the W25 near-duplicate filter across **all** ledger owners, so that each image has exactly one owner. Overlaps are dropped from the later-registered set, under a rule fixed in advance.
VSPS-J M0 dev-touched: every M-HalDetect image, 786 val + 2,695 train = 3,454 COCO ids (27 in both; 73 never decoded), `manuscript/prereg/2026-10-31_vsps_j_m0/dev_touched_ids.txt` sha 91db7e2f. B4 drops them from restval (599 val + 2,027 train in restval). W25 not run for M0 (CC-208 r8); later W25 passes include these 3,454 ids.

**Dev-only (spent):** XM3600 (all), UIT-ViIC test and val, KTVIC test, OV-test, COCO Karpathy test, nocaps val, LongCap/Polaris/DOCCI/THumB/Composite/VaPR. UIT-ViIC val 924 is K2 dev, and sharing it needs a PI and judge line.
VSPS-J M0 probes 91 Karpathy-test images (M-HalDetect val ∩ Karpathy test) at dev only; held out of every operating-point choice; `karpathy_test_val_ids.txt` sha 88e40e3c.
VSPS-J E1+E2 (dev-explore): E1a decodes all 231 UIT-ViIC test images (already spent; dev only; ids sha 96e6ffe9 in manuscript/prereg/2026-10-31_vsps_j_e1e2/e1e2_plan.json); E1b re-probes the 3,700 KTVIC train stage-1 images (in-sample). No new owner displaced; T-COCO from E1a is never a tier-3 claim. W25 not run for E1a (CC-209 r6, read-only); the 231 stay in exclusion.json for every later W25 pass.

### 2.4 Expected Q1 count, and what would raise it

- **Expected count (sum of P(Q1), rows 5–12):** 0.30 + 0.30 + 0.30 + 0.12 + 0.15 + 0.12 + 0.08 + 0.03 ≈ **1.4** (plausible range 1.0–2.0).
- **P(≥ 3 Q1 published by thesis):** about **10%**. The papers are positively correlated: L1-P1, L1-P2 and CF1 share the diacritic-share risk, and L2 and L3 share the count-control instrument.
- **This is below 3.** The scouts' own figures are higher (scout 1: 40/45/30; scout 4: 30/20/20; scout 3: 30). Those are single-agent opinions conditional on their pilots, so they are discounted here.

What would raise the count. These are concrete levers, not re-tuned numbers.

1. **Kill-and-replace, decided early.** The unconditional 0.30 figures already average over pilot outcomes, so running a pilot only reveals information; it does not raise the expectation. For example, if L1-a, L2-a and L3-a all clear their raise thresholds, rows 5–7 rise to about 0.45 each and the total reaches about **1.85**. The lever is speed: the three pilots cost about 35 GPU-h and give an answer by about 12/2026. Any line that is killed must have its slot filled at once by the next early attempt (L4 or the scout 4 D1 conditional below), so the number of live, independent Q1 attempts in 2027 does not fall below four.
2. **More independent early attempts.**
   - L4 (VinDr), if credentials arrive by 02/2027: +0.10–0.15, an independent failure mode.
   - Scout 4 D1 (an A+B estimator-and-panel synthesis at IP&M, 2028), only if A and B both PASS, and only on new data: +0.10.
3. **Front-loading.** Every Q1 first submission should be in by 03/2028, so that a rejection can still cascade to a second Q1 venue in time. Rows 11–12 are late and nearly worthless for the count unless moved up.
4. **Category ruling at LHU (PI Q6).** If LHU's exemption counts any SCImago Q1, then B at LRE (Q1 in Linguistics) becomes a Q1 attempt (about +0.15), under the looser reading.
5. **Evidence boosts that Q1 reviewers reward.** An outside replication or co-author, and a released kit with a DOI (artifacts ≥ 3).

**Plain statement for the PI.** No combination of the levers above brings the expected count to 3. With every lever applied, the expected count is about 2.0–2.3 and P(≥ 3) about 20–30%. **Three Q1 papers in three years is a stretch goal on this evidence.** The regulatory floor (§0.2) does not depend on it.

## 3. Mapping onto MT1–MT4 / B0–B6, and changes to proposal v5

| Proposal item | Paper(s) here | Change from v5 |
|---|---|---|
| B0 (MT1, MT3, MT4) | B0 | Note that it likely does not count toward the 2.0 points |
| B1 = A (MT2.2, MT3.2) | A | None (SPIC Q2, 11–12/2026) |
| B2 = B (MT3.3, MT2.2) | B | Submission moves from 05/2027 to 12/2026–01/2027 (PI-1026v). LRE is Q2 *in CS*. Panel-swap content |
| B3 = C (MT2.1) | C | Submission moves from 11/2027 to 01/2027. SCD method. Q3 if Option E |
| B3b = D (MT4.1) | D | Q3 VJCS, or absorbed by B |
| B6 (MT4.1–4.3, 4.5) | L3-P1 | **Moves from 05/2028 to 04–05/2027** (IP&M SI) |
| B4 (MT1.2, MT2.2) | B4 | Moves from 11/2028 to 06/2028. Relation gold from VG on COCO restval |
| B5 (MT3.1–3.3) | B5 | Moves from 05/2029 to 11/2028. Still too late to count; kept for the thesis chapter |
| — (new) MT3.2 / MT3.3 / MT4.5 | L1-P1, L1-P2, CF1 | New text-in-image fidelity chapter: measurement (MT3.2), Vietnamese (MT3.3), inference-time fix (MT4.5), span repair (MT3.1, CH3) |
| — (new) MT3.2 / MT4.2 | L2-P1, L2-P2, CF2 | New cross-lingual measurement and alignment chapter; MT4.2 preference optimisation gets a concrete transfer study |
| — (new) MT2.1 | L1-P3 | Retrieval as a semantic source, diacritic-free queries |

**What would change in proposal v5** (not edited here; this is a list for the PI's rewrite):
- §2.4: add a fifth gap, KT5 (Vietnamese diacritic fidelity in text-in-image descriptions), and widen KT3 to "hallucination measured on translated items".
- §4.2: add ViTextVQA, MTVQA, VinText, OIV7, AMBER and (for C) ViTextCaps to the data scope.
- §5: add CH5/GT5 (diacritic-only errors are a distinct, explainable and fixable class).
- §9.1, Table 1 and Table 2: grow from 7 to about 12 publications. Move the Q1 attempts into 2027, and replace the "B4, B5, B6" Q1 target sentence with "B6, L1-P1, L2-P1 primary; B4, L1-P2, L1-P3, L2-P2 backup".
- State the publish-before-evaluation constraint.
- Keep the thesis title. Present L1 as "text-in-image descriptions" (PI Q3).

## 4. First four weeks of GPU work (10-30 → 11-26)

This plan builds on CC-158 r7 and does not replace it.
- **Weeks:** W1 = 10-30..11-05, W2 = 11-06..11-12, W3 = 11-13..11-19, W4 = 11-20..11-26.
- **Roles:** M1 is test-capable (m3 role). M2 is dev-only (m4 role): no one-look test images may ever be on M2.

**Prerequisites common to every item:**
1. a gate rule with its kill criterion, committed before any output exists;
2. a ruling at ≥ 90% (PI-1029e);
3. data in hand with a licence check;
4. a backbone pin and an import check in the target venv on the target machine;
5. ≤ 3 background agents, with the usage guard run at each step.

Idle is preferred over filler. **W1 for the new lines is CPU and data access only**: ViTextVQA is gated or on request, VinText's terms are unverified, and the MTVQA-vi count is unknown.

### M2 (dev-only), in order

| # | Pilot (≤ 20 GPU-h each) | GPU-h | Earliest | Prerequisites beyond the common five |
|---|---|---|---|---|
| 1 | Backbone pins and import checks: Qwen2.5-VL-7B, InternVL3-8B, Qwen3-VL-8B, plus the new L1 backbones (CC-158) | ≤ 1 each | W1 | Setup finished (CC-157) |
| 2 | C SCD dev gate (CC-158 majority 2/1) | ≤ 15 | W1–W2 | W7 gate rule committed; dropped if C falls to Option E on 11-12 |
| 3 | **L1-a**: diacritic decomposition + tone re-rank, 3 backbones, MTVQA train (vi/fr/de/it) and ViTextVQA dev | ≤ 12 | W2 | Denominator rule pinned; only train/dev files copied to M2; ViTextVQA access (otherwise MTVQA train only) |
| 4 | **L2-a**: native vs translate-then-score vs count-matched gap, 3 backbones, UIT-ViIC test + XM3600 (spent, dev role) | ≤ 15 | W2–W3 | 0-GPU matcher-parity check passed; a judge confirms that spent sets may sit on M2 |
| 5 | B exact-recipe timing pilot | ≤ 1 | W3 | D0 GO, PI B+D and H lines, committed prereg (CC-158 W4/W5) |
| 6 | **L1-b**: span-level corruption pilot, 2 MLLMs, held-out VinText-train slice (about 300 images) | ≤ 8 | W3 | VinText data terms confirmed; slice ids committed |
| 7 | **L2-b**: English-only DPO transfer + count-channel pilot, 2B backbone | ≤ 20 | W4 | Scoop check (OpenAlex/S2 after the rate limit resets; contact vsps-research@example.org or none); PI Q8 |

### M1 (test-capable), in order

| # | Item | GPU-h | Earliest | Prerequisites |
|---|---|---|---|---|
| 1 | Finish setup (CC-157); nothing else | 0 | W1 | – |
| 2 | **L3-a**: K2 Gate 1 resume from the surviving gold/unedited adapters, val 924 dev decodes | 3–6 | W1–W2 | In order: PI un-park (Q2), a judge resume ruling, and Gate 1 `NOT_AFTER` amended **before 2026-11-06T12:00Z** |
| 3 | A P50 (CC-158; registered one look, cap 8) | ≤ 8 | W2 (11-07..11-10) | Companion prereg committed or 11-08 12:00Z; cutoff 11-16 12:00Z |

### Slot planning: confirmatory jobs, not pilots (these exceed 20 GPU-h by design)

| Machine | Job | GPU-h | Earliest | Prerequisites |
|---|---|---|---|---|
| M2 | B T (backbone 1), then T2 (backbone 2) | about 20 + 22 | W3–W4 | Timing pilot; D0 GO; PI B+D and H; committed prereg |
| M1 | C test (one look) | about 37 | W3–W4 | ViTextCaps in hand + C PREREG committed (W7) |
| M1 | L3-P1 KV test (one look) | ≤ 100 (MT4 cap) | W4 or later | L3-a GO; KV freeze; any PREREG amendment (VI−EN contrast, verifier arm) ruled first |

**New-line pilot GPU over the four weeks:** about 55 GPU-h on M2 (L1-a, L2-a, L1-b, L2-b) and 3–6 GPU-h on M1. CC-158's own items add about 25 GPU-h, or about 65 if B Option 1 is approved. This is far below capacity. **The binding limits are rulings and data access, not GPU.**

## 5. Open questions for the PI (each with a recommendation and a default)

| # | Question | Recommendation | Default if no answer |
|---|---|---|---|
| Q1 | Adopt L1 (tone-mark fidelity), L2 (cross-lingual measurement → alignment) and L3 (MT4 un-parked) as the Q1 programme, with A/B/C/D as the Q2–Q3 stream? | YES, then run a 3-judge panel plus Codex on this file before acting (PI-1029e ≥ 90%) | Scout files stay notes; v5 is unchanged |
| Q2 | Un-park MT4/K2 (parked under the PI-1029c reading) on idle M1 slots, resuming Gate 1 from the surviving adapters? | YES. It is the only line with a committed unspent test, and the `NOT_AFTER` amendment must land before 11-06 12:00Z | Stays parked; Gate 1 is HELD after 11-06 |
| Q3 | Accept text-in-image work (scene-text VQA and descriptions) as thesis chapters under MT3.2/MT3.3/MT4.5? | YES, framed as "fidelity of text in image descriptions" | L1 keeps only L1-P2 (captions); L1-P1 becomes a conference paper |
| Q4 | Approve the test-set ledger (§2.3), including the new AMBER → L2-P2 line (lifts CC-147 r4) | YES, as one ruling | Nothing new assigned; new lines stay dev-only (Q3 ceiling) |
| Q5 | OIV7 val for L2-P1: full split (41,164 images; about 105 GPU-h short / 225 detailed, 3 backbones × 2 languages) or a pre-fixed draw? | Full split, short-caption prompt, 3 backbones (full-datasets rule) | Full split, 3 backbones |
| Q6 | Ask the LHU graduate office in writing: (a) does the 3×Q1 exemption need a CS category (LRE is SJR Q1 only in Linguistics and LIS)? (b) is FAIR 2026 counted? (c) which regime (TT 18 or TT 53) covers the 12/2026 intake? | YES. You or the student send it; agents never use a personal address | Plan on the strict reading: CS-category Q1, FAIR not counted |
| Q7 | Move the Q1 dates in v5 earlier (B6 → 04–05/2027; B4 → 06/2028; B5 → 11/2028) and list about 12 publications? | YES, because only published work counts | v5 dates unchanged (then B4/B5 cannot count) |
| Q8 | Merge A Option 3 (DPO count channel) with scout 1 D3 (cross-lingual DPO) into one paper, L2-P2? | YES, after the scoop check | Neither is run |
| Q9 | Start PhysioNet credentialing (CITI course + DUA) for reserve direction L4 (VinDr-CXR)? | YES. It is a student action and cheap; decide on L4 at 02/2027 | L4 is not pursued |
| Q10 | ViTextVQA (and VinText terms) access: the official release is "on request"; the HF mirror is gated | You or the student submit the HF gated form or the author request yourselves, or approve a draft first, as in CC-158 Q4. vsps-research@example.org cannot receive replies, and agents never use a personal address; agents only watch for public releases | L1-a runs on openly downloadable MTVQA train only |
| Q11 | ViTextCaps stays C-only, even if it arrives | YES | YES |
| Q12 | Two Scopus conference resource papers (CF1, CF2), plus one Scopus conference in 2027 to secure the 2.0 floor early | YES, with a judge anti-slicing check; verify each edition's Scopus indexing | Kits ship as artifacts inside the journal papers; the floor rests on A/C |
| Q13 | L2-P1's verifier fix overlaps C's §3.4 verifier | L2-P1 is diagnosis plus a registered which-explanation test, with no fix | Same |

## 6. Checks still open (no GPU needed)

- OpenAlex/S2 rerun of the L1 and L2 "no prior work" claims after the rate limit resets. Look especially for semCER follow-ups and any LVLM diacritic diagnosis.
- MTVQA-vi test size.
- Official licences of ViTextVQA, ViOCRVQA, VinText, ViSignVQA, Objects365 v2 and Visual Genome.
- VG overlap with COCO restval.
- Quartile and category re-check of every venue in §2.1, including the TOMM and PRL categories and IJMIR "all categories".
- Scopus indexing of the specific KSE/SoICT/RIVF/MAPR editions.
- IP&M SI MMLowRes deadline.
- Judge: whether the deterministic lexicon/template probes (L2) and the orthographic candidate sets (L1) count as "new gold". Recommendation: they do not, because they are deterministic resources fixed before any output exists.
