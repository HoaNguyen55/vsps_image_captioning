# Paper B: outline (journal draft; rebuilt 2026-10-20 under PD-24)

Date: 2026-10-15. Branch paper-v10. Submit by 2027-01-25.
Inputs: `manuscript/journal_draft/paperB_outline.md`, `.session_backup/2026-10-14/two_paper/PLAN_2PAPERS.md`, `.session_backup/2026-10-13/decisions/PD-6.txt`, `D18.txt`, `manuscript/cfp/TWO_PAPER_SHORTLIST.md`, the FAIR 2026 paper (`manuscript/FAIR_28.08.26_v10_EN_IEEE.pdf`), and Gemini's `paper_b_master_tables_v2.json` / `claim_ledger_v2.json` (every traced cell re-checked against its source; see "Gemini v2 audit" below).

## Abstract

Vietnamese captioning systems are compared mainly by CIDEr on KTVIC, but what KTVIC scores measure is unexamined. We audit the dataset with a controlled fine-tuned vision–language model as instrument. Four properties change what KTVIC scores mean. First, each image's five references come from one writer: objects named by two references sit in adjacent slots at a share of 0.7102, against 0.40 under exchangeability. Second, no reference ends with a period: stripping final periods raises the zero-shot backbone's CIDEr-D from 28.98 to 33.30, and appending one to every output of a fine-tuned system that never punctuates costs 35.17 points; KTVIC-trained systems keep the unpunctuated style on XM3600. Third, CIDEr-D moves by 15.64 points between word segmentation and syllable tokenisation, and object scores depend on unpublished matcher rules. Fourth, 401 of the 558 test images also appear in the UIT-OpenViIC training split, and 555 somewhere in it; against their separately written OpenViIC captions, KTVIC's precision cost for a fusion system nearly vanishes (one contrast, one seed). We propose a protocol card stating segmenter, CIDEr variant, punctuation policy and matcher, and release an evaluation kit: scorer, matcher code and audit scripts. The kit contains our matcher word lists (author-built, v1 and v2) but no counts derived from KTVIC and no dataset captions; the model-drafted v3 rules are not included. Pre-registered method tests are in a supplement; the single pre-registered test of the final system did not raise CIDEr-D over its members' mean (−0.39 [−2.44, +1.67]; registered verdict FAIL; the interval includes 0).<!-- src: data/results/b_f1/b_f1_run.json (sha256 998e4f33) :: primary.D_MBR_x100_mean_lo_hi[0..2] ; primary.verdict (judge's fixed sentence, CP-071) -->
<!-- PD-24 (e). Numbers: 0.7102 / 0.40 (sec1 item 1 src), 35.17 (sec3.3 src), 15.64 (sec3.4 derived src), 401 / 558 (sec3.6 src). 28.98 / 33.30 (sec3.3 src). Kit sentence = PD-28 (2) / PD-27c fix 2. R2 2026-10-21: N-M7 (lead with strip/append; XM3600 only; "nearly vanishes" = sec5:43 P cost −2.21 → −0.25, one contrast), N-M8 (segmentation vs syllables), N-M10 ("separately written"), N-m7 (250 words); the "final test not run" clause moved out (N-M12; still in sec1 and S7). -->

**Keywords:** Vietnamese image captioning; benchmark validity; dataset audit; evaluation protocol; train–test overlap; CIDEr.<!-- CP-054 -->

## Working title

**What a Vietnamese Captioning Benchmark Measures: A Validity Audit of KTVIC and an Open Evaluation Kit**

Previous title: *What a Vietnamese Captioning Benchmark Measures: A Controlled Fine-Tuned VLM and a Validity Audit of KTVIC* (changed with the PD-24 audit-and-kit framing).

## Venue plan and framing

| Order | Venue | Framing | Conference-version rule |
|---|---|---|---|
| 1 | Language Resources and Evaluation (Springer; Q1 Linguistics & Language, SCIE) | lead with the dataset audit; the system is the measuring instrument | Springer general clause ("expansion of previous work"); disclose FAIR 2026, ≥ 30% new |
| 2 | IP&M special issue "Multilingual and Multimodal … Low Resource" (Q1, SCIE+SSCI; closes 2027-08-31) | low-resource VLM evaluation | call asks for "original, unpublished": disclose FAIR, ≥ 30% new, cover letter lists the new parts |
| 3 | ACM TALLIP (Q2, SCIE) | Asian-language resource and evaluation | explicit ≥ 25% new material |

D18 §5.2 applies: the kNN prior did not pass its headline test (its own rule gives SECONDARY_POSITIVE_OR_INCONCLUSIVE; LOCALLY_FROZEN, so exploratory), so the paper keeps the resource-and-audit framing (D2). PD-24 (2026-10-20) makes it an audit-and-kit resource paper for LRE: the method-side record moves to `supplementary_B.md`. M3 ran as Tier-3 S3 (a68fb66, amended 59901cc) and FAILED its dev gate; EV-RANK is POST_HOC and descriptive, not a gate.

## Section map (files in this directory)

| § | File | Content | New vs FAIR |
|---|---|---|---|
| — | `outline_B.md` (this file) | title and abstract | new |
| 1 | `sec1_intro.md` | problem, four audit findings, contributions (audit, protocol card, kit), one-line list of the moved results, relation to FAIR 2026 and the companion paper | rewritten |
| 2 | `sec2_related.md` | Vietnamese datasets and systems; reference-free scoring; VLMs; reference-based metrics and protocol signatures; reference independence | new |
| 3 | `sec3_data_and_audit.md` | KTVIC audit: single writer, punctuation (incl. XM3600 period shift), segmentation, matcher v1/v2/v3, overlaps; evaluation kit and data availability (§3.7) | new |
| 4 | `sec4_system.md` | the measuring instrument (zero-shot, P1, P1-R, fuse2), protocol card, reproducibility gates | mostly new (P1 recipe from FAIR) |
| 5 | `sec5_results.md` | the controlled system on KTVIC; UIT-ViIC transfer and in-domain replication; two caption panels | new |
| 6 | `sec6_discussion.md` | what KTVIC CIDEr measures; recommendations; the kit mapped to them | new |
| 7 | `sec7_limitations_ethics.md` | limitations, data and release, Table 7.1 (A↔B overlap), AI-agent provenance | new |
| 8 | `sec8_conclusion.md` | conclusion | new |
| S | `supplementary_B.md` | S1 labels and extra systems; S2 ladder; S3 second backbone and 3B; S4 leaderboard; S5 leakage test; S6 negatives (incl. WiSE-FT); S7 dev-gated levers and the final test; S8 deviations | new |
| — | `number_manifest_B.tsv` | every number, its JSON key and file hash | — |
| — | `new_vs_FAIR.md` | overlap table and percentage | — |

## Claims Paper B owns (PD-6 ledger, PD-24 placement)

Main text:
1. KTVIC audit: single writer (adjacency 0.7102 vs 0.40); no punctuation in references and −35.17 CIDEr-D for one "."; XM3600 reference end-period rate (17.69%) and the period-append shift (+2.71 / +2.75; absolute only); segmentation sensitivity (15.64); matcher v1/v2/v3 with no human sign-off for v3; image overlap (KTVIC–OpenViIC 401/558 train split, 555/558 any split; UIT-ViIC–COCO/POPE).
2. The measuring instrument: response-only P1 on Qwen2.5-VL-7B-Instruct, word-level CIDEr-D 148.23 (SD 0.38) over 3 seeds; protocol card; scoring reproducibility gates.
3. UIT-ViIC transfer and in-domain fusion replication against COCO instance labels; reference-to-instance transfer slope κ.
4. Two caption panels (KTVIC references vs a separately written OpenViIC panel on the same images, aggregates only); EV-RANK concordance (POST_HOC, descriptive).
5. The evaluation kit (own code only; licence and DOI from the authors).

Supplement (verdicts unchanged): ladder (H0 NOT MET, PD-20); B1 aborted at Step 1 guard, 3B outputs unverified and not reported; B-N1 (LBB-P1 FAIL, LBB-P2 INCONCLUSIVE, LBB-P3 FAIL; KB1); B-N2 (placebo INCONCLUSIVE, headline NOT_EVALUABLE); negatives (kNN, UPE-MBR, RL, P-M6b, PLAN-F1, WiSE-FT, levers); Tier-3 (S1 PASS dev only, S2 not carried, S3 FAIL, S5 FUND_EXTERNAL_IMAGE_DATA); B-F1 registered (d6cb2c7), not run.

Paper A owns the XM3600 system scores and the UIT-ViIC slope differences (PD-6; removed from B under PD-24 c). Paper A reports no primary KTVIC number (it uses the OpenViIC captions of KTVIC test images as one caption corpus; R2 N-M4) and cites this paper as under review. No number is primary in both papers (Table 7.1).

## Open items (not run, or for the authors)

- the MIT licence for the kit; [AUTHOR TO PROVIDE] Zenodo DOI; [AUTHOR TO PROVIDE] the terms under which KTVIC, UIT-ViIC and UIT-OpenViIC were obtained (PD-24 b question to the user); [AUTHOR TO CONFIRM] AI tools and AI-drafted text (sec7.4); [AUTHOR TO PROVIDE] FAIR 2026 proceedings details (paperB.bib).
- B-F1 ran once on 2026-10-21: registered verdict FAIL (−0.39 [−2.44, +1.67]; CP-071).
- Not run: POPE-500 for UIT-ViIC-trained adapters; UIT-ViIC append-period effect with the committed scorer; slot-rate-preserving permutation null for the single-writer test; 8-gram scan of the kit archive; WiSE-FT addendum items; protocol-matched comparators.
- Exists but unverified, not reported: 3B fallback outputs (61/62); UIT-ViIC role/child flip paired CI.

## Gemini v2 audit (2026-10-15)

All 2,349 traced cells in `paper_b_master_tables_v2.json` (2,209) and `claim_ledger_v2.json` (140) resolve to their source key and match at the displayed precision; all stated file hashes match. Mismatches are in the ledger's prose, not in traced cells:

- **B-T2 title** says "5/6 fall inside all three (M, P, R) intervals". Source: 4/6. Besides 55 cons (P OUT), `fuse2_s43-detailed` has M = 3.2545 > 3.254 (`c9_55_ladder_cons_s42_evaluation.json :: prereg_ladder_check.all_6_landed_ladder_runs.fuse2_s43-detailed.in_prereg_interval.M = false`).
- **B-T2 title** says the pooled result "confirms L over T"; the per-run verdicts support L, but T was already refuted on count (H6 §1d), and four of the six pooled runs are fuse2 seed replicates, not ladder steps.
- **B-T3 title** says role/child canonicalisation "resolves CHAIR_i inflation"; that matcher has no human sign-off.
- **B-T5 title** uses "typicality vs visual truth", which the required wording forbids ("two caption panels disagree").
- **Ownership resolved (main, 2026-10-15):** +20.70 / +32.72 are gold-completeness slope differences (N1 replication on UIT-ViIC), which PD-6 gives to Paper A. Removed from B.
- **Outside v2 (Paper B outline only):** the zero-shot CIDEr "34.33 → 38.02 (+10.74%)" from `c1_b1_b6_reproduction.json` uses a re-implemented scorer (`E4.Cider`) that does not reproduce the committed score (28.98, `data/results/zeroshot-short.json`). This draft uses the c8 values (28.98 → 33.30), which use the committed scorer.
- **Gemini prose:** `xm3600_short_interim_verdict.md` line 49 says 99.83% end-period rate for zero-shot; the JSON and line 50 say 99.5. The draft uses the JSON.
