# Paper C review: Reviewer R3 (evaluation metrics and benchmark validity)

AI-generated reviewer opinion. Panel output of 2026-10-29.

**Scores (1-5):** novelty 2, correctness 4, contribution 3, clarity 3. **Recommendation:** major revision (TALLIP). **Confidence:** 4/5. **Q1 (Neurocomputing):** not ready.

## Summary

Every headline number checked matches the decision files and preregistrations: P1 +4.49 [3.52, 5.57] PASS, P1b, P2, XM-a +0.70 [-0.45, 1.97] FAIL, XM-b, P1-EN +3.08 [2.08, 4.03] PASS, S-NC +1.73 [0.94, 2.50] FAIL, InternVL3 rows. Rules match PREREG.md. Failed tests are reported adequately. Weak points:

1. Closest MLLM prior art missing: Flamingo/OpenFlamingo RICES vs random on COCO.
2. Table 21 called "a position, not a ranking", then ranked.
3. Benchmark contamination of the backbones not discussed; "training-free" label misleading.
4. SESOI unjustified; +2.0 carried from stripped Vietnamese to PTB English CIDEr-D.
5. Registered commitment to state stage-B power not met.
6. Text contradicts itself on whether the dev ablation is a contribution.

Mostly text and framing changes; no new test look needed.

## Verification performed

- decide_ov.json, decide_xm_m3.json, decide_xmb.json, decide_coco_test.json, decide_nocaps_val.json: P1, P1b, P2, length gaps, scope row, XM-a, per-backbone XM, XM-b, S-zf, P1-EN, InternVL3 τ = -∞ secondary, S-NC, guard counts all match after rounding.
- Rules match c_test PREREG §7.1-7.5 and c_en PREREG §7, including that the English rule was fixed after XM-a.
- Table 21 values keyed in number_manifest_C.tsv; published rows not re-opened.
- Build: 37 pp. + 20 pp., no undefined references.
- Searches: arXiv API ran; Semantic Scholar HTTP 429; OpenAlex budget exhausted; no API key registered, no e-mail sent. OpenFlamingo (arXiv:2308.01390) Appendix Table 9 read directly.

## Major issues

**M1. Closest MLLM prior art missing.** 02:27-42 (Table 1) and 02:44-47 omit Flamingo (Alayrac et al. 2022, arXiv:2204.14198) and OpenFlamingo (Awadalla et al. 2023, arXiv:2308.01390); neither among the 39 bib keys. OpenFlamingo Appendix Table 9, OF-9B: RICES vs random at equal shots on COCO +4.1 CIDEr at 4 shots (89.0 to 93.1), +9.5 at 32; on Flickr-30K -20.3 at 4 shots, -13.6 at 32. Change: (a) add both to §2 and Table 1; (b) state the equal-k COCO gain for a frozen VLM is known, so the English arm is a replication under text-only examples with a one-look test; (c) use the Flickr-30K reversal when discussing InternVL3's COCO sign and the out-of-source failures. Novelty rests on Vietnamese setting, text-only examples, same-memory equal-k control, registered tests.

**M2. Table 21 ranked in prose.** 08:122 vs 08:147. Non-comparable rows: NoCaps re-fetched from Open Images (08:108); local pycocoevalcap with df over 4,500 images, not the official evaluator; MeaCap memory differs by row (COCO vs CC3M); Vietnamese published rows use full 3,600/2,001 images and other segmentation vs this study's as-written column on XM-test2500. Change: delete every ordinal sentence at :147; keep setting differences and the "far from fine-tuned on OpenViIC" remark; add scorer/tokenisation, #images, #references columns; show `ret`/`rand`/`zs` consistently or `ret` only; consider moving to supplement.

**M3. Benchmark contamination and "training-free".** No discussion of whether backbone pretraining/instruction tuning include COCO, NoCaps, Open Images or Vietnamese captioning data (grep finds nothing in §0-10). Table 21 (08:124-145) labels both MLLMs "training-free" beside MeaCap. Authors should check Qwen2.5-VL and InternVL3 technical reports/model cards. Affects reading of COCO results and zero-shot baselines (InternVL3 zs 78.85 vs Qwen zs 59.06 on COCO). Change: Table 21 setting "no task training in this study; backbone training data undisclosed / may include COCO"; paragraph in 09_limitations.md:21-29; note that equal-k `rand` removes contamination effects shared by both arms but not those interacting with retrieval.

**M4. SESOI unjustified, reused across scales.** 05:19 no rationale; stage-2 PREREG:284 traces it to a planning suggestion. 08:18, :24 apply +2.0 to PTB CIDEr-D (COCO means ~85-96 vs OV ~30-40), roughly a third as large relatively. Figure 1 (08:82) draws one SESOI line across both scales. Change: short rationale; state English SESOI carried over without recalibration; relative size per set; mark Figure 1 line "registered threshold, different scales". No verdict changes.

**M5. Registered reporting commitment unmet.** Stage-2 PREREG:301 promises the paper states G1 power; "power" appears nowhere in 0*.md. Change: one sentence at 05:8 (stage B) or §6.7; ideally approximate power/MDE of P1, XM-a, P1-EN, S-NC at actual n.

**M6. Dev ablation status contradictory; "explain" overstates.** 02:47 lists "the backbone-dependence explanation" as item 3 of what the study adds; 06:172 says ablations "enter neither the abstract nor the contributions"; 06:220 says they "explain why". Account fails on XM-test2500, COCO, NoCaps (InternVL3 τ = -∞ not detected, 06:222). Change: remove item 3 from 02:44-47 or reword as dev-only description; at 06:220 replace "explain" with "are consistent with a deletion-step account on OV-dev-B".

## Minor issues

- m1. Failure framing: (a) NoCaps CI [0.94, 2.50] excludes zero and contains the SESOI: inconclusive w.r.t. SESOI, not a null; add "CI above zero, point below the registered +2.0" in abstract. (b) 10:14 turns the post-hoc, confounded domain-coverage reading (08:88) into a practitioner rule; move to a post-hoc discussion sentence or soften to "consider".
- m2. P2 compares `ret` with `zs`, not `rand`. Table S1 gives `rand` ΔP_cm vs zs (2.82 Qwen; 1.40 InternVL3 at τ = 0.10); state descriptive `ret` - `rand` precision difference, labelled post hoc. Say 35% of InternVL3 `ret` captions are zero-shot fallbacks with ΔP_cm = 0 by construction (06:136).
- m3. Table S1: InternVL3 `ret` at τ = 0.10 vs τ = -∞ has higher CHAIR_i (0.254 vs 0.237), lower ΔP_cm vs zs (1.57 vs 5.80), lower stripped CIDEr-D (33.62 vs 39.50). The frozen deletion step worsened every reported quality measure on OV-test; say so in §6.6 or §9.2.
- m4. Construct validity: retrieved captions share annotator-group phrasing that `rand` does not control; Qwen 4-gram copy share rises with k (0.306 to 0.402, 06:216). Suggest a dev-only (OV-dev-B) masked-n-gram analysis, labelled, or a stated limitation. Do not re-score test sets.
- m5. XM-a pooled upper bound 1.97 just below SESOI: descriptive remark that the pooled XM3600 gain is unlikely to reach the SESOI, labelled.
- m6. Add vieCap4H (VLSP 2021) at 01:5 / 02:19, or narrow to "general-domain".
- m7. Internal process detail (07:74, 08:100 "laptop-side step", 07:53 and 08:113 "sister study", parity narrative 07:9-11) to supplement.
- m8. Abstract leads with COCO; lead with OpenViIC P1 (primary; TALLIP).
- m9. Consider opening abstract with the per-backbone picture (cf. own advice 10:13).
- m10. Table 21 Vietnamese rows: as-written column on 2,001 images vs stripped on 1,941 in main analysis; say why in caption.
- m11. Own arXiv search (Vietnamese AND captioning) found no in-context Vietnamese captioning study; "no priority claim" appropriate. S2 429 / OpenAlex exhausted.
- m12. Figure 1: separate x-axes per language panel.

## Specific checks

- Failed tests adequate: yes (abstract, contributions, own subsections with registered wording, Limitations, Conclusion; stricter NoCaps rule disclosed). Refinements in m1.
- Comparison table as ranking: yes in practice (M2, M3).

## Q1 readiness

Not ready: no method (01:34); gain on one of two backbones; both out-of-source predictions failed; OpenFlamingo already shows the COCO gain. Would need a method or broader evidence (more families/sizes, principled account of when retrieval helps), under new three-tier registrations on fresh, never-looked test sets; no re-scoring of existing test sets. Ops-log style needs heavy trimming.

## Recommendation

Major revision. Core registered results sound and honestly reported; novelty positioning, Table 21 framing, contamination caveat, SESOI rationale and registered power statement must be fixed.
