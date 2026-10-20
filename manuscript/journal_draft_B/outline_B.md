# Paper B: outline (journal draft, first full version)

Date: 2026-10-15. Branch paper-v10. Submit by 2027-01-25.
Inputs: `manuscript/journal_draft/paperB_outline.md`, `.session_backup/2026-10-14/two_paper/PLAN_2PAPERS.md`, `.session_backup/2026-10-13/decisions/PD-6.txt`, `D18.txt`, `manuscript/cfp/TWO_PAPER_SHORTLIST.md`, the FAIR 2026 paper (`manuscript/FAIR_28.08.26_v10_EN_IEEE.pdf`), and Gemini's `paper_b_master_tables_v2.json` / `claim_ledger_v2.json` (every traced cell re-checked against its source; see "Gemini v2 audit" below).

## Working title

**What a Vietnamese Captioning Benchmark Measures: A Controlled Fine-Tuned VLM and a Validity Audit of KTVIC**

Alternative: *A Controlled Baseline and a Validity Audit for Vietnamese Image Captioning.*

## Venue plan and framing

| Order | Venue | Framing | Conference-version rule |
|---|---|---|---|
| 1 | Language Resources and Evaluation (Springer; Q1 Linguistics & Language, SCIE) | lead with the dataset audit; the system is the measuring instrument | Springer general clause ("expansion of previous work"); disclose FAIR 2026, ≥ 30% new |
| 2 | IP&M special issue "Multilingual and Multimodal … Low Resource" (Q1, SCIE+SSCI; closes 2027-08-31) | low-resource VLM evaluation | call asks for "original, unpublished": disclose FAIR, ≥ 30% new, cover letter lists the new parts |
| 3 | ACM TALLIP (Q2, SCIE) | Asian-language resource and evaluation | explicit ≥ 25% new material |

D18 §5.2 applies: the kNN prior did not pass its headline test (its own rule gives SECONDARY_POSITIVE_OR_INCONCLUSIVE; LOCALLY_FROZEN, so exploratory), so the paper keeps the resource-and-audit framing (D2). M3 is registered separately (Tier-3 S3, a68fb66) and has not run; EV-RANK is POST_HOC and descriptive, not a gate.

## Section map (files in this directory)

| § | File | Content | New vs FAIR |
|---|---|---|---|
| 1 | `sec1_intro.md` | problem, contributions, relation to FAIR 2026 and the companion paper | rewritten |
| 2 | `sec2_related.md` | Vietnamese datasets and systems; reference-based metrics and protocol signatures; reference independence | new |
| 3 | `sec3_data_and_audit.md` | KTVIC audit: single writer, punctuation, segmentation, matcher v1/v2/v3, overlaps; release kit (§3.7) | new |
| 4 | `sec4_system.md` | controlled system (P1, response-only P1, fusion), protocol card, registered ladder design, B1 design, reproducibility gates | mostly new (P1 recipe from FAIR) |
| 5 | `sec5_results.md` | 3-seed system; ladder; UIT-ViIC transfer; two caption panels (C3) | new |
| 6 | `sec6_negatives.md` | pre-registered and controlled negatives | new (FAIR's DPO negative is cited, not reused) |
| 7 | `sec7_discussion.md` | what KTVIC CIDEr measures; recommendations; the release kit mapped to them (§7.4) | new |
| 8 | `sec8_limitations_ethics.md` | limitations, data and release statement, AI-agent provenance | new |
| — | `number_manifest_B.tsv` | every number, its JSON key and file hash | — |
| — | `new_vs_FAIR.md` | overlap table and percentage | — |

## Claims Paper B owns (PD-6 ledger)

1. KTVIC system: response-only P1 on Qwen2.5-VL-7B, word-level CIDEr-D 148.23 (SD 0.38) over 3 seeds.
2. Registered supervision ladder (REGISTERED, 1b5d16b): 6/10 landed runs inside all intervals (55 cons P OUT; fuse2_s43-detailed M OUT above; 58 unf2-short and 57 rnd2-short M OUT below); joint 10-run 95% CI [−0.90, +0.92] (registered check stdout:11), registered H0 (conjunction, V4.txt:233-235) NOT MET: pooled part met (point −0.007 computed from printed per-run points), per-run part not (8/10 within ±1.0; p1ep4 −1.59, cons +1.44) (PD-20); mean of printed per-run points −0.007 (computed, verifier record). The ±0.8 TOST (addendum) is POST_HOC and FAILS on the six earlier runs; pooled ±1.0/±2.0 are EXPLORATORY.
3. B1 (Qwen3-VL-8B-Instruct) aborted at its registered Step 1 guard (PD-8): reported as a boundary result. Wording: "two model scales of one family (7B, 3B)"; 3B runs PENDING; Qwen3-VL post-guard run optional/PENDING.
4. UIT-ViIC transfer and in-domain replication (the slope-ordering differences belong to Paper A).
5. KTVIC audit: single writer; no punctuation in references and −35.17 CIDEr-D for one "."; segmentation sensitivity; XM3600: 17.69% of references end with a period, and appending a period recovers +2.71 / +2.75 CIDEr-D (absolute shift only; the rest of the drop is not decomposed); UIT-ViIC period effect PENDING (c8 values withdrawn, B2); matcher v1/v2/v3 with no human sign-off for v3.
6. Two caption panels (C3): KTVIC references vs an independent OpenViIC panel on the same images, aggregates only.
7. Pre-registered and controlled negatives (kNN prior, UPE-MBR kill 2, 35_e RL, P-M6b, PLAN-F1, self-fuse, E5 RFT/DPO, MR5, loss mask, tags).

Paper A uses KTVIC only as a motivating example and cites this paper as under review. No number is primary in both papers.

## PENDING (marked in text and manifest)

- Ladder reruns 56/57/58: scored once by the registered check (stdout 0477f26f; VERIFIED LADDER_CHECK_final.json be043f40). H0 as registered: NOT MET (PD-20).
- 3B fallback runs 61_p1_3b_s42 and 62_fuse2_3b_s42 on M2 (PD-8; PD-8's "57/58" predates GPU_JOB_PLAN_v1's IDs); optional Qwen3-VL post-guard run under a new prereg.
- POPE-500 for any UIT-ViIC-trained adapter, with all 21 UIT-ViIC training images excluded (CC-005).
- B-N3: NOT_RUN (agreement gate STOP; PD-21b). The FAIR-2026 human ratings are evidence for no claim in Paper B.
- M3 = Tier-3 S3 count-matched DPO (registered a68fb66; not run).
- WiSE-FT (59): gate DONE and VERIFIED (wise_ft_gate.json 93eb8e67; §6.6); the addendum's reporting items are [PENDING-WISE-ADDENDUM].
- B-N1 protocol-card leaderboard (prereg 327191c; decodes not run); B-N2 leakage DiD not evaluable (no OpenViIC-trained run), placebo and descriptive gaps pending the judge.
- Protocol-matched comparators (GRIT, ViG, HDUCap). Matcher v3 ships labelled unattested; no sign-off is planned (no new annotation).

## Gemini v2 audit (2026-10-15)

All 2,349 traced cells in `paper_b_master_tables_v2.json` (2,209) and `claim_ledger_v2.json` (140) resolve to their source key and match at the displayed precision; all stated file hashes match. Mismatches are in the ledger's prose, not in traced cells:

- **B-T2 title** says "5/6 fall inside all three (M, P, R) intervals". Source: 4/6. Besides 55 cons (P OUT), `fuse2_s43-detailed` has M = 3.2545 > 3.254 (`c9_55_ladder_cons_s42_evaluation.json :: prereg_ladder_check.all_6_landed_ladder_runs.fuse2_s43-detailed.in_prereg_interval.M = false`).
- **B-T2 title** says the pooled result "confirms L over T"; the per-run verdicts support L, but T was already refuted on count (H6 §1d), and four of the six pooled runs are fuse2 seed replicates, not ladder steps.
- **B-T3 title** says role/child canonicalisation "resolves CHAIR_i inflation"; that matcher has no human sign-off.
- **B-T5 title** uses "typicality vs visual truth", which the required wording forbids ("two caption panels disagree").
- **Ownership resolved (main, 2026-10-15):** +20.70 / +32.72 are gold-completeness slope differences (N1 replication on UIT-ViIC), which PD-6 gives to Paper A. Removed from B.
- **Outside v2 (Paper B outline only):** the zero-shot CIDEr "34.33 → 38.02 (+10.74%)" from `c1_b1_b6_reproduction.json` uses a re-implemented scorer (`E4.Cider`) that does not reproduce the committed score (28.98, `data/results/zeroshot-short.json`). This draft uses the c8 values (28.98 → 33.30), which use the committed scorer.
- **Gemini prose:** `xm3600_short_interim_verdict.md` line 49 says 99.83% end-period rate for zero-shot; the JSON and line 50 say 99.5. The draft uses the JSON.
