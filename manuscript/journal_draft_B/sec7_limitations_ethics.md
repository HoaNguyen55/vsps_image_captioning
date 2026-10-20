# 7 Limitations and ethics

<!-- Draft 2026-10-15 (was sec8_limitations_ethics.md); renumbered and revised 2026-10-20 under PD-24 (a, b, c, e). -->

## 7.1 Limitations

**One model family.** Every result in the main text comes from Qwen2.5-VL-7B-Instruct with one QLoRA recipe. The registered second backbone (Qwen3-VL-8B-Instruct) stopped at its zero-shot guard, and the 3B fallback's outputs are not verified and not reported in this version (Supplementary S3). The audit findings about the references do not depend on the model, but the system scores do.

**Method-side tests.** The supervision ladder, the leaderboard, the leakage test and the training and decoding levers are reported only in the supplement. Most ladder and lever runs have one seed, so a miss of one to three precision points cannot be separated from seed noise, and the ladder's registered frontier-invariance hypothesis was not met (S2). Four registered reporting items of the weight-interpolation control were not computed (S6.6).<!-- src: .session_backup/2026-10-18/ladder_check/final/stdout.txt :: lines 1-10 (rule: a run is inside when its line has no OUT; 6 of 10) --><!-- moved from main: PD-20 verbatim sentence now in supplementary_B.md S2.2; src: manuscript/prereg/2026-10-12_frontier_invariance_V4.txt:233-236 (rule; per-run clause l.235, pooled clause l.236) ; .session_backup/2026-10-18/ladder_check/final/stdout.txt :: line 11 (95% CI) ; lines 1-10 (per-run points; |point| <= 1.0 on 8 of 10) ; line 1 (p1ep4_s42-short −1.59) ; line 3 (cons_s42-short +1.44) ; manuscript/verification/paperA/LADDER_CHECK_final.json :: rows[0].items.C2.evidence (−0.007) -->

**No human judgments.** We collected no new human annotation. The OpenViIC panel is a second set of captions, not ground truth. The within-writer leave-one-out figures are not a human ceiling. Model-generated signals (sample votes, kNN priors, model-drafted matcher rules) serve only inside methods and never as evidence.

**Earlier human ratings.** The prior FAIR-2026 ratings (2 raters, 150 captions) exceeded our pre-set agreement gate (identical scores on 71–87% of captions per scale, against a threshold of 50%), so, as fixed in advance, no criterion analysis was run. These ratings are evidence for no claim in this paper.<!-- heading was 'B-N3: NOT_RUN' ; verbatim, judge PD-21b ; src: .session_backup/2026-10-19/HL_human_labels/b_n3_quality_gate.json :: per_scale (identical_share min and max) ; n_items ; rule ; STOP ; inputs_sha256 (2 rater files) -->

**Matcher v3 is unattested.** Its rules were drafted by an AI model and have no human sign-off. No conclusion in this paper depends on it.

**Exploratory and post hoc analyses.** In the main text, the ranking concordance of Section 5.3 is post hoc and descriptive, and the v3 matcher results are sensitivity analyses. The supplement labels each of its tests by registration status (S1).

**Comparators.** No published Vietnamese system has been rescored under our protocol. HDUCap and ViG could not be obtained in full text (Section 2). We therefore make no ranking claim.

**XM3600 decomposition is partial.** On XM3600, appending a period to the fine-tuned outputs raises CIDEr-D by +2.71 (P1) and +2.75 (fusion)<!-- src: .session_backup/2026-10-18/cpu_audit_r15/xm3600_period_cider_decomposition_v1.json :: cross_system_drop_decompositions_token_level.p1_s43_short_vs_zeroshot_short.drop_decomposition.by_append_period_to_ft_pred.cider_shift_x100.est ; cross_system_drop_decompositions_token_level.fuse2_s42_short_vs_zeroshot_short.drop_decomposition.by_append_period_to_ft_pred.cider_shift_x100.est -->, but both systems still score below the zero-shot backbone (Section 3.3). We measure the period's effect in absolute points only. The rest of the drop is not decomposed, so we do not attribute it to template or content.

## 7.2 Data, licences and release

We redistribute no images, reference captions or other dataset text. The evaluation kit contains only our own code and documentation, under the MIT licence, archived on Zenodo (DOI: [AUTHOR TO PROVIDE]); readers obtain the datasets from their original sources (Section 3.7). We obtained UIT-ViIC from the UIT NLP group's dataset distribution (https://sites.google.com/uit.edu.vn/uit-nlp/datasets; accessed 2026-10-21), which offers it for research purposes and states no licence and no redistribution terms. KTVIC is publicly available from its authors' repository (https://github.com/pacman-ctm/ktvic; accessed 2026-10-21), which asks users to cite Pham et al. (2024) and states no licence or redistribution terms. UIT-OpenViIC is released by its authors (https://github.com/nghiangh/UIT-OpenViIC-dataset; accessed 2026-10-21) as "publicly available for research purposes", with a request to cite Bui et al. (2026); the repository has no licence file. The matcher lexicons, system outputs on KTVIC or UIT-ViIC images, and fine-tuned weights are not released. Qwen2.5-VL-7B-Instruct is under Apache-2.0 and Qwen2.5-VL-3B-Instruct under the non-commercial Qwen Research License Agreement (Section 3.7).

**UIT-OpenViIC** is used only through aggregate statistics. No OpenViIC caption, n-gram or per-image derived file appears in this paper or its kit.

**Leakage rules.** 401 of the 558 KTVIC test images are in OpenViIC's training split. No model here is trained on OpenViIC, and an OpenViIC-trained model must not be evaluated on KTVIC test. Any UIT-ViIC-trained adapter must be scored on POPE-500 with all 21 UIT-ViIC training images excluded, and on the COCO probe without its 59 (Section 3.6). ViCLIP-OT is trained on UIT-OpenViIC, so the same overlap applies to it, and it is never used as an evaluator on KTVIC test.

**People in images.** Captions describe everyday scenes with people. No identity recognition is performed. References and system outputs use role and gender nouns (*đàn ông* "man", for example); matcher rules for these nouns are documented so that their effect on scores can be inspected, and we report no analysis by gender.

## 7.3 Relation to the conference version and the companion paper

A conference version of part of this work appeared at FAIR 2026 (Nguyen and Tran, 2026). That paper's contribution, VSPS supervision from verified propositions, is not a contribution of this paper. What we reuse from it is the KTVIC/COCO setup, the QLoRA recipe and the P1 control. P1's seed-42 score (149.8 there, 149.79 here under the same scorer) serves only as a reference point.

A companion paper is under review. Table 7.1 states what each paper claims and which data it uses. No number is a primary result in both papers.

**Table 7.1.** What this paper and the companion paper claim, and the data each uses.

| | Companion paper (under review) | This paper |
|---|---|---|
| Question | When does an object-level hallucination score support a comparison between two systems? | What does a KTVIC CIDEr or object score measure? |
| Primary claims | one confirmatory claim: F1's slope on log object count is ordered by gold completeness and positive under complete gold (registered on XM3600; with a second backbone on the same 600 images as Paper A's Section 7.5); registered secondary: condensed F1, an eight-LVLM ranking test, human-validity and preference-data audits; exploratory: count-matched rescoring of published methods | the KTVIC audit: single-writer references, punctuation convention, segmentation sensitivity, matcher versions, image overlap, a second caption panel; the protocol card and the evaluation kit |
| KTVIC | motivating example only; no primary number | primary dataset |
| XM3600 (Vietnamese) | the registered verbosity-sign test, scored on six systems: the zero-shot backbone and this paper's KTVIC-trained P1 and fuse2, short and detailed prompts | reference end-period rate and the effect of appending a period to the same P1 and fuse2 outputs only |
| UIT-ViIC | slopes of object F1 on object count under three golds, over this paper's ten UIT-ViIC systems (exploratory); exchangeability statistic | transfer CIDEr-D; in-domain fusion effect against COCO instance labels; role/child matcher flip; reference-to-instance transfer slope; COCO/POPE overlap lists |
| UIT-OpenViIC | exchangeability statistic (aggregates only) | overlap with KTVIC; second caption panel on KTVIC test images (aggregates only) |
| English data | COCO, Flickr30k, English LVLM families, public human judgments and preference data | none |
| Count-matched controls | developed and validated there | used as a tool, supplement only |
| Systems | published systems and zero-shot LVLMs; also outputs of this paper's fine-tuned systems on XM3600 and UIT-ViIC (above) | Qwen2.5-VL-7B fine-tunes (P1, P1-R, fuse2) and the zero-shot backbone; the systems are trained and owned here |
<!-- PD-24 (c). Built from manuscript/journal_draft/sec1_introduction.md (contributions 1-5; RQ1-5), sec5_exchangeability.md Table 5.1, sec7_verbosity_sign.md §7.3 and §7.5, sec11 §11.2, and the PD-6 Q1(a) ledger. Removed from B under PD-6: XM3600 system CIDEr-D (old sec3:38) and the UIT-ViIC slopes (old sec5:72-80). -->

## 7.4 Analysis provenance and the use of AI agents

Much of the analysis code and many intermediate reports were produced by AI coding agents (two different assistants: [AUTHOR TO CONFIRM: names and versions of the AI tools]) under human direction, with one agent reviewing the other's results. AI assistants also drafted the v3 matcher rules (Section 3.5) and parts of the manuscript text; [AUTHOR TO CONFIRM: which parts of the text were AI-drafted and how the authors revised them]. Reviews found that the agents' JSON outputs reproduced from raw data, but that their prose and logs sometimes contained numbers that existed in no output file, or that disagreed with the JSON. This paper follows these rules:

1. Every number is read from a JSON key and listed with its file hash in the number manifest, which is supplementary material for reviewers.
2. A number with no computing source is not used. For example, a zero-shot CIDEr of 34.33 that came from a re-implemented scorer is replaced by the committed scorer's 28.98.
3. Every test carries one of four registration labels, computed from commit, push, file and output times (Supplementary S1). Only tests whose predictions were committed before the outputs they predict count as registered; the others are treated as exploratory.<!-- src: .session_backup/2026-10-18/paperA_tasks/A4.4/reconcile.tsv :: row 449 ; tests_status.tsv (all B tests) -->
4. Model-generated signals are never gold or human evidence. No new human annotation was collected.
5. Every cited identifier is checked on a primary page, and unread papers are cited without their numbers.

The authors take responsibility for all analyses and text.

**Funding.** This research received no external funding; all costs, including rented GPU time and AI-tool subscriptions, were borne by the authors' team.
