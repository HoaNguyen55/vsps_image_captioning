## 8. English arm (C-EN) — PLACEHOLDER

> **PLACEHOLDER. Nothing in this section is a result.** This section is filled only from the decision files of the separate English registration, after its own one-look test. Until then it holds the commitments below and no numbers from any English run.
>
> Editorial note (remove before submission): if the English arm is not complete in time, the paper is submitted without this section, and the arm is reported under its own registration at revision.

**Status.** The commitment to run the arm was recorded in the project's working log and approved in the decision log (PI-1026b) after the OpenViIC test block had started and before the first decision file existed. Neither record is a git commit (Section 7.7). The English registration is not yet written, and it will be committed before any English decode. If the arm's verdict is not available in time, this paper may be submitted without it (decision log PI-1026l).

**Planned design (planned, not binding; the English registration fixes it).**
- **Test sets.** The full COCO Karpathy test ({{C:cen_karpathy|i}} images) is primary. The full NoCaps validation set ({{C:cen_nocaps|i}} images) is secondary.
- **Memory.** COCO Karpathy train and restval: {{C:cen_memory|i}} images after excluding {{C:cen_memory_excl|i}} refused ids, reported beside the full {{C:cen_memory_full|i}}.
- **Arms.** `ret`, `rand` and `zs`, with k, order, τ and backbones carried over from Table 1 and the two prompt tails translated directly. There is no English tuning and no English development evaluation.
- **Scoring and decisions.** PTB-tokenised CIDEr-D, with SESOI +{{OV:SESOI|f1}} and one look per set.

**Disclosures that this section must carry.**
- Earlier decodes of the Karpathy test images by other systems in the same group, which are not reused here.
- A companion submission's use of the references of {{C:cen_a_refs|i}} of the Karpathy test images.
- Earlier Qwen-model decodes on a stratified {{C:cen_nocaps_seen|i}}-image subset of NoCaps validation. The NoCaps result is also reported without that subset.
- The {{C:refused163|i}}-image reference exposure of Section 7.5. {{C:refused163_karpathy|i}} of these images are in the Karpathy test, {{C:refused163_coco2500|i}} in a COCO subset used by a companion submission, {{C:refused163_chair|i}} in a CHAIR evaluation subset and {{C:refused163_pope|i}} in a POPE subset. The lists overlap, so these parts sum to {{C:refused163_sum|i}}, not {{C:refused163|i}}. Only gold references were read, in aggregate; no model output was involved, and no image is dropped.
- That the English registration was written after the Vietnamese test had started and its verdicts were known.

**[RESULTS TABLE — to be filled from the English decision files.]**

**[RESULTS TEXT — the verdict of each registered English prediction, reported as computed, beside the Vietnamese results and never compared with them as a cross-language difference.]**
