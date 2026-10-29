# Paper B: outline (journal draft; rebuilt 2026-10-20 under PD-24)

Date: 2026-10-15. Branch paper-v10. Submit by 2027-01-25.
Inputs: `manuscript/journal_draft/paperB_outline.md`, `.session_backup/2026-10-14/two_paper/PLAN_2PAPERS.md`, `.session_backup/2026-10-13/decisions/PD-6.txt`, `D18.txt`, `manuscript/cfp/TWO_PAPER_SHORTLIST.md`, the FAIR 2026 paper (`manuscript/FAIR_28.08.26_v10_EN_IEEE.pdf`), and Gemini's `paper_b_master_tables_v2.json` / `claim_ledger_v2.json` (every traced cell re-checked against its source; see "Gemini v2 audit" below).

## Abstract

Vietnamese image captioning is a low-resource setting: a few small benchmarks carry the evidence, and systems are compared mainly by CIDEr on KTVIC. We ask what a gain from more KTVIC training data measures. For a fine-tuned Qwen2.5-VL-7B model (one backbone), each doubling of KTVIC training images raises CIDEr-D (×100) by +9.61 [7.18, 12.36] on 300 development images. On the 187 development images that also have UIT-OpenViIC captions, the gain is +10.59 [7.43, 13.81] per doubling against KTVIC references but +0.72 [−0.83, 2.36] against the separately written OpenViIC panel, a gap of +9.87 [6.71, 13.35]. Gains from more KTVIC training captions register mainly on KTVIC's own references. In a two-seed reverse pilot trained on OpenViIC captions, adapters gain +2.98 [0.94, 4.88] on that panel; the reverse gap, +1.69 [−0.72, 3.91], is not distinguishable from zero, and whether these gains reach KTVIC references is not established. These are development-only score associations: writer and protocol cannot be separated, and confirmation needs a future single look on unseen data. An audit shows how KTVIC's references differ. Each image's five references come from one writer (adjacent-slot share 0.7102 against 0.40 under exchangeability). Appending a period, which no reference has, costs 35.17 points where a pipeline drops Penn Treebank punctuation removal, and nothing where it keeps it. Segmentation moves scores by 15.64 points, and 401 of the 558 test images are in UIT-OpenViIC's training split. We release a protocol card and an open evaluation kit that rerun the audit on a reader's data.<!-- BD revision 2026-10-29 (BD_META_REVIEW items 1, 2, 5, 10, 12): headline scoped to the forward direction; "reliably improves" and "thus" removed; reverse result as a two-seed pilot with g_R and "not established"; dev tier and future single look stated; B-1 (300 images) and D0 (187 images) named; +10.59 CI and gap added; period sentence tied to the pipeline condition. New sources: d0_decide.json 15dd925f primary.b_K_ci95 ; primary.g ; primary.g_ci95 ; b_r1 decide a6627047 primary.g_R ; primary.g_R_ci95. 248 words. --><!-- MERGED B+D abstract, positive-headline revision 2026-10-29 (rubric C1/C13; LRE <= 250 words; registered final-system FAIL stays in sec1 and sec5.1) (PI-1029n, 2026-10-29). Sources: number_manifest_B.tsv rows for 148.23, 0.7102, 0.40, 35.17, 15.64, 401, +9.61 (B-1 decide b44a76fe), +10.59/+0.72 (D0 15dd925f), +2.98, O5b (B-R1 a6627047), -0.39. No 'first', no transfer claim. -->
<!-- Previous abstract (249 words, PD-24 e / R2) is in .session_backup/2026-10-27/paperB_v2/before/outline_B.md. -->

**Keywords:** Vietnamese image captioning; benchmark validity; dataset audit; evaluation protocol; train–test overlap; CIDEr.<!-- CP-054 -->

### Pre-merge abstract (kept for revert)

<!-- Vietnamese image-captioning systems are compared mainly by CIDEr (consensus-based image description evaluation) on KTVIC, but a KTVIC number alone does not name its scoring protocol.<!-~ CC-147 W5: unsourced frequency claim softened to what the paper shows. ~-> We propose a protocol card naming the segmenter, CIDEr variant, scale, punctuation policy and object matcher of every score, and release an open kit that scores any system's outputs under a declared card and reruns the audit on the reader's data. With one fine-tuned Qwen2.5-VL-7B model as a fixed instrument (word-level CIDEr-D 148.23, three seeds), we measure four properties of KTVIC. Each image's five references come from one writer: objects named by exactly two references sit in adjacent slots at a share of 0.7102, against 0.40 under exchangeability. No reference ends with a period, a measured protocol hazard: where a pipeline replaces the Penn Treebank (PTB) tokenizer and loses its punctuation removal, one period per caption costs the instrument 35.17 CIDEr-D points; with PTB-style removal, nothing (post hoc). Word segmentation against syllable tokenisation moves the same outputs by 15.64 points. 401 of the 558 test images are in the UIT-OpenViIC training split, whose separately written captions disagree with KTVIC's on objects; their independence is not established. The punctuation fix did not re-rank four public vision–language models (Kendall's τ_b = 1.0; registered prediction FAIL), and the registered final-system test failed (−0.39 [−2.44, +1.67] CIDEr-D against its members' mean). Under a description-only pre-registration, we ran the kit on 3 external systems from 3 sources (descriptive scores, no ranking).<!-~ CC-145 W2 / J7 (2026-10-28, B pass 3): "so it is validated on external systems" removed (read as independent validation, which sec7 §7.1 denies); the runs are stated as the authors' runs; PREREG §7.3 permits "validated" but does not require it. J7 approved the CP-071 final-test sentence change and dropping the PD-28(2)/PD-27c kit-content sentence (kept in sec1 and §7.2). ~-><!-~ src (CC-126 W3 reframe, 2026-10-27; wording after Ken K15_REFRAME §3.1 as adopted by CC-126, with K15 mock-review W4's fallback sentence in place of the 55.12% sentence; the CP-071 final-test sentence and the PD-28 (2)/PD-27c kit-content sentence of the previous abstract are replaced/dropped, judge item J7): 148.23 = .session_backup/2026-10-15/paperA_keys/cider_3seed_mean.json :: mean ; 0.7102 / 0.40 = .session_backup/2026-10-14/r11_verify/c3_n2_exchangeability_all_datasets.json :: k5_exchangeability_audit.ktvic_test_objects_in.adjacent_share ; adjacent_share_null ; 35.17 = .session_backup/2026-10-14/r11_verify/c8_l5_d1_d3a_cpu_audit.json :: l5_d1_punct_idf_law|ktvic_test_k1_to_k5_curves|p1assist_s42-short|first_k|k=5|d_abs ; PTB 'nothing' = data/results/b_ptb/ptb_protocol.json :: ktvic_test.systems.p1assist_s42-short.PTB.first_k.k=5.d_add_minus_strip (POST_HOC) ; 15.64 = derived: .session_backup/2026-10-14/research_r10/E4/pilot_results.json :: P1_syllable CIDEr p1-gold minus P0_official_rdr CIDEr p1-gold ; 401 / 558 = .session_backup/2026-10-13/r10_cpu/r10_a1_a3_spotchecks_v2.json :: A_32_leakage_disclosure.splits.ktvic_test_558.in_openviic_train ; panel disagreement = sec5_results.md §5.3 (data/results/second_panel.json), independence not established = sec5 §5.3 / sec7 ; tau_b 1.0 = data/results/b_n1/b_n1_run.json (sha256 adad454d) :: predictions.LBB-P1.{point,verdict} (FAIL; four zero-shot VLMs, supplementary_B.md S4) ; -0.39 [-2.44, +1.67] = data/results/b_f1/b_f1_run.json (sha256 998e4f33) :: primary.D_MBR_x100_mean_lo_hi[0..2] ; primary.verdict ; external-system sentence (B v2 pass 2, 2026-10-28) = PREREG 2026-10-28_b2_external §7.3 templates; .session_backup/2026-10-28/b2_external/score/scores.json (sha256 e1a6e0d8) :: external_systems (3) ; distinct_sources (3) ; w13_validated_sentence_allowed (true); B2-LOOK LOG.md:587; the two KTVIC baselines are not counted (PREREG §1.1 K3). Removed: 55.12% and 'nearly vanishes' (CC-126 W3). ~-> -->

## Working title

Earlier merge proposal (not adopted): *What Does a Vietnamese Captioning Score Measure? Reference Panels, Training-Data Gains and a Validity Audit of KTVIC*


**What Training-Data Gains Measure on a Vietnamese Captioning Benchmark: A Development Study with Two Reference Panels, a Validity Audit of KTVIC and an Open Evaluation Kit** (BD meta-review item 4 Option A, 2026-10-29: "A Development Study with" added; PI decision (a) pending, revert by deleting those words; title page and cover letter match)

Title before the BD revision: *What Training-Data Gains Measure on a Vietnamese Captioning Benchmark: Two Reference Panels, a Validity Audit of KTVIC and an Open Evaluation Kit* (adopted 2026-10-29 for the merged B+D paper)

Pre-merge title: *What a Vietnamese Captioning Benchmark Measures: A Validity Audit of KTVIC and an Open Evaluation Kit*

Previous title: *What a Vietnamese Captioning Benchmark Measures: A Controlled Fine-Tuned VLM and a Validity Audit of KTVIC* (changed with the PD-24 audit-and-kit framing).

## Venue plan and framing

| Order | Venue | Framing | Conference-version rule |
|---|---|---|---|
| 1 | Language Resources and Evaluation (Springer; Q1 Linguistics & Language, SCIE) | lead with the dataset audit; the system is the measuring instrument | Springer general clause ("expansion of previous work"); disclose FAIR 2026, ≥ 30% new |
| 2 | IP&M special issue "Multilingual and Multimodal … Low Resource" (Q1, SCIE+SSCI; closes 2027-08-31) | low-resource VLM evaluation | call asks for "original, unpublished": disclose FAIR, ≥ 30% new, cover letter lists the new parts |
| 3 | ACM TALLIP (Q2, SCIE) | Asian-language resource and evaluation | explicit ≥ 25% new material |

**B+D merge (PI-1029n, 2026-10-29T09:08Z).** Paper D's training-set-size study (B-1 PASS, D-α INCONCLUSIVE) and its two-panel dev studies (D0 GO, B-R1 ASYMMETRIC/O5b) are part of this paper; **paper D is not submitted standalone**. Headline: what a training-set-size gain measures on KTVIC (it registers mainly on the panel whose captions were trained on; dev-only; no transfer claim; no priority claim). Submission is gated at 98 (Codex CC-166 = 94: W6 complete, H gate committed, second-reviewer FAIR/A separation check, see SEPARATION_FAIR_A.md).

D18 §5.2 applies: the kNN prior did not pass its headline test (its own rule gives SECONDARY_POSITIVE_OR_INCONCLUSIVE; LOCALLY_FROZEN, so exploratory), so the paper keeps the resource-and-audit framing (D2). PD-24 (2026-10-20) makes it an audit-and-kit resource paper for LRE: the method-side record moves to `supplementary_B.md`. M3 ran as Tier-3 S3 (a68fb66, amended 59901cc) and FAILED its dev gate; EV-RANK is POST_HOC and descriptive, not a gate.

## Section map (files in this directory)

| § | File | Content | New vs FAIR |
|---|---|---|---|
| — | `outline_B.md` (this file) | title and abstract | new |
| 1 | `sec1_intro.md` | problem, four audit findings, contributions (audit, protocol card, kit), one-line list of the moved results, relation to FAIR 2026 and the companion paper | rewritten |
| 2 | `sec2_related.md` | Vietnamese datasets and systems; reference-free scoring; VLMs; reference-based metrics and protocol signatures; reference independence | new |
| 3 | `sec3_data_and_audit.md` | KTVIC audit: single writer, punctuation (incl. XM3600 period shift), segmentation, matcher v1/v2/v3, overlaps; evaluation kit, the kit on three external systems (counts; table in S9) and data availability (§3.7) | new |
| 4 | `sec4_system.md` | the measuring instrument (zero-shot, P1, P1-R, fuse2), protocol card, reproducibility gates | mostly new (P1 recipe from FAIR) |
| 5 | `sec5_results.md` | the controlled system on KTVIC; UIT-ViIC transfer and in-domain replication; two caption panels; §5.4 training-set size (B-1, D-α) and what its gain measures (D0), §5.5 the reverse direction (B-R1) (DEV; merged B+D per PI-1029n; B-R1 ASYMMETRIC/O5b; no claim that OpenViIC-trained gains reach KTVIC references) | new |
| 6 | `sec6_discussion.md` | what KTVIC CIDEr measures; recommendations; the kit mapped to them | new |
| 7 | `sec7_limitations_ethics.md` | limitations, data and release, A↔B overlap (Table S13.1 in the supplement since CC-145 J6), AI-agent provenance | new |
| 8 | `sec8_conclusion.md` | conclusion | new |
| S | `supplementary_B.md` | S1 labels and extra systems; S2 ladder; S3 second backbone and 3B; S4 leaderboard; S5 leakage test; S6 negatives (incl. WiSE-FT); S7 dev-gated levers and the final test; S8 deviations; S9 the kit on external systems (B-2 run record and Table S9.1, ex Table 3.2); S10 references vs instance labels on UIT-ViIC (moved from §5.2); S11 matcher v3 sensitivity and role/child nouns (ex §3.5); S12 XM3600 system scores (ex §3.3); S13 companion comparison (Table S13.1, ex Table 7.1); S14 kit components, recommendation map, checks, text scan (Tables S14.1-2, ex Tables 6.1 and 3.1); S15 baseline-code provenance and software (ex §3.3, §4.3); S16 slot-rate-preserving null (ex §3.2); S17 two-panel descriptive rows and procedure (ex §5.5, BD revision 2026-10-29); section map at the top (ex sec1 PD-24 (a) list) [CC-145 W1/J6, 2026-10-28] | new |
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

Paper A owns the XM3600 system scores and the UIT-ViIC slope differences (PD-6; removed from B under PD-24 c). Paper A reports no primary KTVIC number (it uses the OpenViIC captions of KTVIC test images as one caption corpus; R2 N-M4) and cites this paper as under review. No number is primary in both papers (Table S13.1, supplement).

## Open items (not run, or for the authors)

- the MIT licence for the kit; [AUTHOR TO PROVIDE] Zenodo DOI; the KTVIC and UIT-OpenViIC authors confirmed data use in writing on 2026-10-28 (PI-1026az, LOG.md:635; e-mails on file with the PI); [AUTHOR TO PROVIDE] the same for UIT-ViIC, which PI-1026az does not cover; [AUTHOR TO CONFIRM] AI tools and AI-drafted text (sec7.4); [AUTHOR TO PROVIDE] FAIR 2026 proceedings details (paperB.bib).
- B-F1 ran once on 2026-10-21: registered verdict FAIL (−0.39 [−2.44, +1.67]; CP-071).
- Not run: POPE-500 for UIT-ViIC-trained adapters; UIT-ViIC append-period effect with the committed scorer; 8-gram scan of the kit archive; WiSE-FT addendum items; protocol-matched comparators.
- Run 2026-10-22 (post hoc, CC-088 B-2; data/results/b2_controls/): the slot-rate-preserving null (sec3.2), the published-baseline punctuation, segmentation and PTB audit with the E4 τ reproduction (sec3.3, sec3.4), the matching-threshold grid (sec3.6) and the panel n-gram overlap (sec5.3).
- Run 2026-10-28 (B-2, description-only prereg 2026-10-28_b2_external, Amendments 1-2): the kit on 3 external systems from 3 sources (K1 KTVIC, K5 UIT-ViIC, K6 UIT-OpenViIC), 0 of 10 published output files passed the gate; sec3 §3.7 (counts only), Supplement S9 Table S9.1 (moved from Table 3.2 by CC-145 W1) (scores.json e1a6e0d8, table.md f0db61f3).
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
