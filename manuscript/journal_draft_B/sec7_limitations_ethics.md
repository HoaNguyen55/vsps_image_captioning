# 7 Limitations and ethics

<!-- Draft 2026-10-15 (was sec8_limitations_ethics.md); renumbered and revised 2026-10-20 under PD-24 (a, b, c, e). -->

## 7.1 Limitations

**One model family.** Every result in the main text comes from Qwen2.5-VL-7B-Instruct with one QLoRA recipe. The registered second backbone (Qwen3-VL-8B-Instruct) stopped at its zero-shot guard, and the 3B fallback's outputs are not verified and not reported in this version (Supplementary S3). The audit findings about the references do not depend on the model, but the system scores do.

**Method-side tests.** The supervision ladder, the leaderboard, the leakage test and the training and decoding levers are reported only in the supplement. Most ladder and lever runs have one seed, so a miss of one to three precision points cannot be separated from seed noise, and the ladder's registered frontier-invariance hypothesis was not met (S2). Four registered reporting items of the weight-interpolation control were not computed (S6.6). The single pre-registered test of the final system returned FAIL: −0.39 [−2.44, +1.67] CIDEr-D against its members' mean (Section 5.1, S7).<!-- src: data/results/b_f1/b_f1_run.json (sha256 998e4f33) :: primary.D_MBR_x100_mean_lo_hi[0..2] ; primary.verdict --><!-- src: .session_backup/2026-10-18/ladder_check/final/stdout.txt :: lines 1-10 (rule: a run is inside when its line has no OUT; 6 of 10) --><!-- moved from main: PD-20 verbatim sentence now in supplementary_B.md S2.2; src: manuscript/prereg/2026-10-12_frontier_invariance_V4.txt:233-236 (rule; per-run clause l.235, pooled clause l.236) ; .session_backup/2026-10-18/ladder_check/final/stdout.txt :: line 11 (95% CI) ; lines 1-10 (per-run points; |point| <= 1.0 on 8 of 10) ; line 1 (p1ep4_s42-short −1.59) ; line 3 (cons_s42-short +1.44) ; manuscript/verification/paperA/LADDER_CHECK_final.json :: rows[0].items.C2.evidence (−0.007) -->

**No human judgments.** We collected no new human annotation. The OpenViIC panel is a second set of captions, not ground truth. The within-writer leave-one-out figures are not a human ceiling. Model-generated signals (sample votes, kNN priors, model-drafted matcher rules) serve only inside methods and never as evidence.

**Earlier human ratings.** The prior FAIR-2026 ratings (2 raters, 150 captions) exceeded our pre-set agreement gate (identical scores on 71–87% of captions per scale, against a threshold of 50%), so, as fixed in advance, no criterion analysis was run. The gate is a stop rule fixed before any statistic was computed; it is not a verdict on the ratings. These ratings are evidence for no claim in this paper.<!-- R2 N-m5: stop-rule clarification added; the PD-21b verbatim sentence is kept. -->
<!-- heading was 'B-N3: NOT_RUN' ; verbatim, judge PD-21b ; src: .session_backup/2026-10-19/HL_human_labels/b_n3_quality_gate.json :: per_scale (identical_share min and max) ; n_items ; rule ; STOP ; inputs_sha256 (2 rater files) -->

**Matcher v3 is unattested.** Its rules were drafted with AI assistance and not reviewed by a person. No conclusion in this paper depends on it, and its rules are not in the kit.

**Exploratory and post hoc analyses.** In the main text, the PTB-style punctuation-removal row of Section 3.3 was added after an internal review and is post hoc, the ranking concordance of Section 5.3 is post hoc and descriptive, and the v3 matcher results are sensitivity analyses. The supplement labels each of its tests by registration status (S1).

**Comparators.** We report no published Vietnamese system's score under our protocol as a comparison; two KTVIC baselines' outputs enter only the rank correlation (Section 3.4) and the punctuation audit (Section 3.3). HDUCap and ViG could not be obtained in full text (Section 2). We therefore make no ranking claim.

**XM3600 decomposition is partial.** On XM3600, appending a period to the fine-tuned outputs raises CIDEr-D by +2.71 (P1) and +2.75 (fusion)<!-- src: .session_backup/2026-10-18/cpu_audit_r15/xm3600_period_cider_decomposition_v1.json :: cross_system_drop_decompositions_token_level.p1_s43_short_vs_zeroshot_short.drop_decomposition.by_append_period_to_ft_pred.cider_shift_x100.est ; cross_system_drop_decompositions_token_level.fuse2_s42_short_vs_zeroshot_short.drop_decomposition.by_append_period_to_ft_pred.cider_shift_x100.est -->. The fine-tuned systems score lower than the zero-shot backbone (Section 3.3); we measure the period's effect in absolute points only.<!-- R2 N-M4 / sec3:38: "still score below the zero-shot backbone" removed (PD-24 c). --> The rest of the drop is not decomposed, so we do not attribute it to template or content.

## 7.2 Data, licences and release

We redistribute no images and no reference captions. The evaluation kit holds our own code and documentation, the pre-registration files, score-only copies of the cited result files and the numbers manifest; the code is under the MIT licence. It is archived on Zenodo (DOI: [AUTHOR TO PROVIDE])<!-- CC-088 (A-2): "in one deposit shared with the companion paper" removed -->; readers obtain the datasets from their original sources (Section 3.7). We obtained UIT-ViIC from the UIT NLP group's dataset distribution (https://sites.google.com/uit.edu.vn/uit-nlp/datasets; accessed 2026-10-21), which offers it for research purposes and states no licence and no redistribution terms. KTVIC is publicly available from its authors' repository (https://github.com/pacman-ctm/ktvic; accessed 2026-10-21), which asks users to cite Pham et al. (2024) and states no licence or redistribution terms. UIT-OpenViIC is released by its authors (https://github.com/nghiangh/UIT-OpenViIC-dataset; accessed 2026-10-21) as "publicly available for research purposes", with a request to cite Bui et al. (2026); the repository has no licence file. System outputs and fine-tuned weights are not released. The kit contains our matcher word lists (author-built, v1 and v2) but no counts derived from KTVIC and no dataset captions; the model-drafted v3 rules are not included. A scan of the archive finds no dataset caption, only 11 documented short matches in pinned code (Section 3.7). Qwen2.5-VL-7B-Instruct is under Apache-2.0 and Qwen2.5-VL-3B-Instruct under the non-commercial Qwen Research License Agreement (Section 3.7).

**UIT-OpenViIC** is used only through aggregate statistics. No OpenViIC caption, n-gram or per-image derived file appears in this paper or its kit (the scan of Section 3.7 covers OpenViIC).

**Leakage rules.** 401 of the 558 KTVIC test images are in OpenViIC's training split. No model here is trained on OpenViIC, and an OpenViIC-trained model must not be evaluated on KTVIC test. Any UIT-ViIC-trained adapter must be scored on POPE-500 with all 21 UIT-ViIC training images excluded, and on the COCO probe without its 59 (Section 3.6). ViCLIP-OT is trained on UIT-OpenViIC, so the same overlap applies to it, and it is never used as an evaluator on KTVIC test.

**People in images.** Captions describe everyday scenes with people. No identity recognition is performed. References and system outputs use role and gender nouns (*đàn ông* "man", for example); matcher rules for these nouns are documented so that their effect on scores can be inspected, and we report no analysis by gender.

## 7.3 Relation to the conference version and the companion paper

A conference version of part of this work appeared at FAIR 2026 (Nguyen et al., 2026b). That paper's contribution, VSPS supervision from verified propositions, is not a contribution of this paper. What we reuse from it is the KTVIC/COCO setup, the QLoRA recipe and the P1 control. P1's seed-42 score (149.8 there, 149.79 here under the same scorer) serves only as a reference point.

Table 7.1 compares this paper with a companion manuscript under review (title withheld for double-anonymized review).<!-- CC-088 (A-2): A's title and "by the same authors" removed (CC-074 (c)); A's title is only in cover_letter_B.md and is restored after the IP&M decision --> The table states what each paper claims and which data it uses. No number is a primary result in both papers. Each paper has its own archive; this paper's holds only the components of Table 3.1.<!-- CC-088 (A-2): any deposit made public before A's decision holds B's components only --> The overlap also runs through the exchangeability statistic: it is defined in the companion, which reports it on other corpora and leaves KTVIC to this paper, so each paper relies on the other for half of the contrast (Section 3.2).<!-- R2 N-M3, N-M4 -->

**Table 7.1.** What this paper and the companion paper claim, and the data each uses.

| | Companion paper (under review) | This paper |
|---|---|---|
| Question | When does an object-level hallucination score support a comparison between two systems? | What does a KTVIC CIDEr or object score measure? |
| Primary claims | one confirmatory claim: F1's slope on log object count is ordered by gold completeness and positive under complete gold (registered on XM3600; with a second backbone on the same 600 images, as the companion's Section 7.5 reports; stated for these Qwen-VL systems); registered secondary: condensed F1, an eight-LVLM ranking test, human-validity and preference-data audits; exploratory: count-matched rescoring of published methods | the KTVIC audit: single-writer references, punctuation convention, segmentation sensitivity, matcher versions, image overlap, a second caption panel; the protocol card and the evaluation kit |
| KTVIC | no primary number; the OpenViIC captions of KTVIC test images are one of its caption corpora (exchangeability statistic, aggregates only) | primary dataset |
| XM3600 (Vietnamese) | the registered verbosity-sign test, scored on six systems: the zero-shot backbone and this paper's KTVIC-trained P1 and fuse2, short and detailed prompts | reference end-period rate; CIDEr-D of the zero-shot backbone and the same P1 and fuse2 outputs (short prompt), under P0 and with PTB-style punctuation removal; the effect of appending a period to the P1 and fuse2 outputs |<!-- CC-088 B-3: Table 7.1 matches sec3.3 -->
| UIT-ViIC | slopes of object F1 on object count under three golds, over this paper's ten UIT-ViIC systems (exploratory); exchangeability statistic | transfer CIDEr-D; in-domain fusion effect against COCO instance labels; role/child matcher flip; reference-to-instance transfer slope; COCO/POPE overlap lists |
| UIT-OpenViIC | exchangeability statistic on the full test split and on the panel of KTVIC test images (aggregates only) | overlap with KTVIC; second caption panel on KTVIC test images (aggregates only) |
| English data | COCO, Flickr30k, English LVLM families, public human judgments and preference data | none |
| Count-matched controls | developed and validated there | used as a tool, supplement only |
| Exchangeability statistic | defined there; reported on COCO, UIT-ViIC, Flickr30k and UIT-OpenViIC | reported on KTVIC only |
| Archive | its own archive | its own Zenodo deposit, holding the components of Table 3.1 only |<!-- CC-088 A-2 -->
| Systems | published systems and zero-shot LVLMs; also outputs of this paper's fine-tuned systems on XM3600 and UIT-ViIC (above) | Qwen2.5-VL-7B fine-tunes (P1, P1-R, fuse2) and the zero-shot backbone; the systems are trained and owned here |
<!-- PD-24 (c). Built from manuscript/journal_draft/sec1_introduction.md (contributions 1-5; RQ1-5), sec5_exchangeability.md Table 5.1, sec7_verbosity_sign.md §7.3 and §7.5, sec11 §11.2, and the PD-6 Q1(a) ledger. Removed from B under PD-6: XM3600 system CIDEr-D (old sec3:38) and the UIT-ViIC slopes (old sec5:72-80). -->

## 7.4 Analysis provenance

Analysis code was written with AI assistance under the authors' direction; the v3 matcher rules (Section 3.5) were drafted with AI assistance and not reviewed by a person. Every reported number is traced to an output file, a stated derivation or a cited source, and listed in a numbers manifest. This paper follows these rules:<!-- PD-25 Q3 (a), chosen by the author 2026-10-21. -->

1. Every number is read from an output file (a JSON key, a TSV cell or a line of logged output) or from a stated derivation of such values, or is cited from the literature, and is listed in the numbers manifest with its file hash where it has one.<!-- R2 N-m6 --> The manifest is archived with score-only copies of its source files (caption fields removed for licensing; original SHA-256 given); 42 of its 604 rows cite sources that could not be released and are marked.<!-- src: .session_backup/2026-10-22/b_deposit_v4/ktvic_eval_kit_v4.tar.gz :: manifests/number_manifest_B.tsv rows whose archive_path contains "withheld:" (42 of 604; B deposit v4, 2026-10-22) -->
2. A number with no computing source is not used. For example, a zero-shot CIDEr of 34.33 that came from a re-implemented scorer is replaced by the committed scorer's 28.98.
3. Every test carries one of four registration labels, computed from commit, push, file and output times (Supplementary S1). Only tests whose predictions were committed before the outputs they predict count as registered; the others are treated as exploratory. The archive ships the pre-registration files but not the version-control history, so the commit times behind these labels are self-attested: a reader can check that the shipped files match the SHA-256 values we cite, but not when they were committed.<!-- R2 N-M11: option (c), self-attested; no public repository URL exists. --><!-- src: .session_backup/2026-10-18/paperA_tasks/A4.4/reconcile.tsv :: row 449 ; tests_status.tsv (all B tests) -->
4. Model-generated signals are never gold or human evidence. No new human annotation was collected.
5. Every cited identifier is checked on a primary page, and unread papers are cited without their numbers.

The authors take responsibility for all analyses and text.

## 7.5 Declarations

**Use of generative AI.** During this work the authors used Claude (Anthropic) and Gemini (Google) to write and run analysis code, to draft and edit the manuscript text and to check references. The authors designed the study, directed and checked all analyses, reviewed and edited all text, and take full responsibility for the content.

**Funding.** This research received no external funding; all costs, including rented GPU time and AI-tool subscriptions, were borne by the authors' team.

**Competing interests.** The authors declare no competing interests.

**Ethics approval.** Not applicable: no new data from human participants were collected.

**Data and code availability.** See Section 3.7. The kit is released under the MIT licence; the datasets are available from their original sources.

**Authors' contributions (CRediT).** **Nguyễn Lê Minh Hòa:** Conceptualization, Methodology, Software, Validation, Formal analysis, Investigation, Data curation, Writing – original draft, Writing – review & editing, Visualization, Project administration. **Nguyễn Văn Thịnh:** Conceptualization, Methodology, Supervision, Writing – review & editing. **Trần Văn Lăng:** Conceptualization, Methodology, Supervision, Writing – review & editing.<!-- PD-25, PD-25b; corresponding author Trần Văn Lăng (title page). -->
