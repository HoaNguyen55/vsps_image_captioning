## 9. Limitations and threats to validity

### 9.1 Limitations

- **Two backbones, and the effect is carried by one.** In both languages the in-domain gain is carried mainly by Qwen2.5-VL. For InternVL3 the gain was not detected on OpenViIC test, and on COCO its row is below zero (−1.64 [−2.79, −0.49]). On the development set, the ablations of Section 6.8 trace part of this dependence to the frozen deletion step; whether InternVL3 also takes up less of the examples is not settled, because its k rows are scored after deletion. That account is dev-only and non-confirmatory. Outside in-domain Vietnamese it does not hold: InternVL3's τ = −∞ row is not detected on XM-test2500, COCO or NoCaps. With two backbones, the study cannot say which property of a model predicts the gain. The pooled estimand averages two backbone-plus-configuration pairs that differ in k, order, tail and τ, so it is not an effect for a typical MLLM.
- **Out of the memory's source, the registered predictions did not pass.** On XM3600 Vietnamese the gain was not detected (XM-a FAIL). On NoCaps val the CI lies above zero but the point stayed below the SESOI (S-NC FAIL), under a rule that was fixed after XM-a was known and is stricter than XM-a's. Neither memory holds captions of the target set. Memory source and test set change together across these rows, and no test varied the memory on fixed test images, so the source match is confounded with the test set. The "domain coverage" reading of Section 8.4 is post hoc and untested, and its per-domain rows have overlapping CIs.
- **The metric is reference-based.** CIDEr-D rewards matching the references' wording. In Vietnamese, the stripped column removes the trailing-period effect, and the PTB column agrees with it. Still, part of any `ret` − `rand` gain may be closer wording of image-specific content rather than better content. The study has no human judgments; by design, it uses existing data and labels only.
- **Object measures depend on the matcher and the gold.** On OpenViIC, gold objects come from the union of the references, so a correct object that no reference names counts as an error. On XM3600, the verified labels cover only the mapped classes. The English arm registered no object-precision prediction.
- **The memory and test sets come from related sources.** KTVIC and OpenViIC share images. We removed byte-identical and near-duplicate images between the memory and every protected set, and excluded the near-duplicates of the tuning set from the primary set. Overlaps below the pixel rule's thresholds would not be caught. The same rule protected the English sets.
- **One test look, one machine, one run, one random draw.** Each test set was decoded once with greedy decoding. The CIs capture image sampling conditional on one seeded `rand` assignment per image and on full-set document frequencies; they do not include the variation from drawing other random examples, or run-to-run variation. Decode-parity checks on the same machine and software stack found no run-to-run variation on development data (52/52 identical captions per backbone; supplement, "Test-run operations", and Table S14).
- **The backbones' training data are not fully disclosed.** The Qwen2.5-VL report [@Bai2025Qwen25VL] describes its training data by category (image captions, interleaved image-text, OCR data that include Vietnamese); in our reading it does not name COCO, NoCaps or a Vietnamese caption set. The InternVL3 report [@Zhu2025InternVL3] builds on the corpora of InternVL2.5, whose report lists COCO captions, Open Images captions and TextCaps among its training data [@Chen2024InternVL25]. COCO images and captions, and Open Images images like those of NoCaps, may therefore have been seen in training, at least by InternVL3. The equal-k `rand` control removes contamination that `ret` and `rand` share, but not contamination that interacts with retrieval, for example if retrieved captions cue memorised references. "Training-free" in this paper means no task training in this study. This is a desk check of public reports, not an audit.
- **No priority claim.** Retrieval in-context captioning has been studied before (Section 2). This paper's contribution is the controlled, preregistered comparison, not the method.

### 9.2 Threats to validity

**Internal validity (is the contrast caused by retrieval?).**
- `ret`, `rand` and `fix` share one prompt template, one k and one decoder, and differ only in which captions are shown. `rand` is seeded per image.
- Rule L checks that the gain is not a length effect: it did not fire on OpenViIC test (0.074, 0.039) or COCO (0.019, 0.019).
- The source-dataset share of shown examples is near one for every arm (Table 11). `rand` therefore shows in-domain captions too, and the contrast is not between in-domain and out-of-domain style.
- One threat remains, and it is a design limitation of the registered estimand: InternVL3's deletion step acts after decoding and treats `ret` and `rand` captions differently, because they introduce different numbers of neighbour-only objects (Section 6.8). τ = 0.10 was chosen at stage A under the ΔP_cm constraint of the selection rule and was kept after the guard hypothesis failed at stage B. On OV-test the step lowered CIDEr-D and did not improve CHAIR_i or ΔP_cm (Section 6.6). The registered τ = −∞ secondary is printed beside every τ = 0.10 row for this reason.

**Construct validity (does the score measure caption quality?).**
- CIDEr-D measures agreement with the references, in Vietnamese on word-segmented text (RDRSegmenter) and in English on PTB tokens; Vietnamese caption length is counted in syllables. The two scales are not comparable, and no cross-language difference is computed.
- Count-matched object precision guards against a gain bought by copying wrong objects. On OpenViIC test it held for both backbones. It was not registered in English.

**External validity (where does the result apply?).**
- In-domain, on two benchmarks in two languages, with two 7–8B open MLLMs and a memory of one or two benchmarks' training captions.
- Not out of the memory's source (XM3600, NoCaps).
- Not, so far, for other model families or sizes, for sampled decoding, or for prompts with example images.
- The English arm reused Vietnamese-chosen configurations without re-tuning. This makes it a conservative transfer test, not an estimate of the best English setting.

**Statistical conclusion validity.**
- Every decision uses a registered rule on a paired image bootstrap (B = 2,000, percentile 95% CI) with a fixed SESOI. The SESOI was a planning value, not calibrated, and was carried to English without recalibration (Sections 5.2 and 5.4).
- P1 and P1-EN are single primaries. P2 is an intersection–union test. S-NC was gated in a fixed order after P1-EN.
- Per-backbone, per-domain and development rows are reported with unadjusted CIs and carry no claim.
- No p-values are reported. Any added later would be post hoc and would change no verdict.

**Researcher degrees of freedom.**
- Configurations were frozen on development data before any test output existed.
- Each test set was looked at once, and the English registration fixed its design before any English decode.
- The English registration was written after the Vietnamese verdicts were known, and the mechanism ablations were registered after the test. Both facts are disclosed (Sections 7.4, 8.5 and 6.8).
- The choice to judge NoCaps by the P1 rule, stricter than XM-a's, was made after the XM-a result was known.
- Two of the six τ points of the mechanism ablation were known before it was registered.

### 9.3 Reproducibility

- **Pinned components.** Every model snapshot, processor setting, environment, prompt template, list and code file is pinned by sha256 (Section 3.3).
- **Decision files.** Each decision file records the sha256 of the ledgers it read, the registration hash and the code commit.
- **What is released.** Scores, image ids and sha256 hashes are released; under the registrations, captions, example files, embeddings and per-image ledgers are not. A third party can re-run the study from the public datasets with the released code, lists and seeds, and check each run against the released hashes.
- **Re-run cost.** A full re-run needs the public datasets and one 24 GB GPU: 9.59 GPU-hours for the Vietnamese test and 13.22 for the English one. At the Vietnamese test, Qwen2.5-VL with eight examples took about 0.69 s per image and arm, and InternVL3 about 1.24 s.
