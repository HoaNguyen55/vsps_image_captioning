## 8. English arm (C-EN) — PLACEHOLDER

> **PLACEHOLDER. Nothing in this section is a result.** This section is filled only from the decision files of the separate English registration, after its own one-look test. Until then it holds the commitments below and no numbers from any English run.
>
> Editorial note (remove before submission): if the English arm is not complete in time, the paper is submitted without this section, and the arm is reported under its own registration at revision.

**Status.** The commitment to run the arm was recorded in the project's working log and approved in the decision log (PI-1026b) after the OpenViIC test block had started and before the first decision file existed. Neither record is a git commit (Section 7.7). The English registration is not yet written, and it will be committed before any English decode. If the arm's verdict is not available in time, this paper may be submitted without it (decision log PI-1026l).

**Planned design (planned, not binding; the English registration fixes it).**
- **Test sets.** The full COCO Karpathy test (5,000 images) is primary. The full NoCaps validation set (4,500 images) is secondary.
- **Memory.** COCO Karpathy train and restval: 112,322 images after excluding 965 refused ids, reported beside the full 113,287.
- **Arms.** `ret`, `rand` and `zs`, with k, order, τ and backbones carried over from Table 1 and the two prompt tails translated directly. There is no English tuning and no English development evaluation.
- **Scoring and decisions.** PTB-tokenised CIDEr-D, with SESOI +2.0 and one look per set.

**Disclosures that this section must carry.**
- Earlier decodes of the Karpathy test images by other systems in the same group, which are not reused here.
- A companion submission's use of the references of 2,441 of the Karpathy test images.
- Earlier Qwen-model decodes on a stratified 1,000-image subset of NoCaps validation. The NoCaps result is also reported without that subset.
- The 163-image reference exposure of Section 7.5. 133 of these images are in the Karpathy test, 59 in a COCO subset used by a companion submission, 14 in a CHAIR evaluation subset and 21 in a POPE subset. The lists overlap, so these parts sum to 227, not 163. Only gold references were read, in aggregate; no model output was involved, and no image is dropped.
- That the English registration was written after the Vietnamese test had started and its verdicts were known.

**[RESULTS TABLE — to be filled from the English decision files.]**

**[RESULTS TEXT — the verdict of each registered English prediction, reported as computed, beside the Vietnamese results and never compared with them as a cross-language difference.]**
