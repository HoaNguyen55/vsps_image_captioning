## 10. Conclusion

We asked whether retrieved example captions help two open MLLMs caption images more than random captions from the same memory. We asked it first in Vietnamese and then, with the same frozen configurations and no re-tuning, in English. Each question was answered by a preregistered study with one look per test set.

**In domain, in both languages.** On the OpenViIC test, retrieval beat random examples by +4.49 [3.52, 5.57] stripped CIDEr-D points pooled, P1 PASS. On the COCO Karpathy test it did so by +3.08 [2.08, 4.03] PTB CIDEr-D points, P1-EN PASS. In both languages the gain is carried mainly by Qwen2.5-VL; InternVL3's row is not detected on OpenViIC test and, as a reported row, below zero on COCO. On OpenViIC test, neither model lost count-matched object precision against its own zero-shot captions; this compares the full in-context prompt with zero-shot, not retrieved with random examples.

**Outside the memory's source.** On XM3600 Vietnamese the gain was not detected (+0.70 [−0.45, 1.97]), and the registered XM3600 prediction is not confirmed. On NoCaps val the pooled gain was +1.73 [0.94, 2.50]: its CI lies above zero, but the point is below the SESOI under the stricter English rule (S-NC FAIL), so the transfer claim is not made. Its reported per-domain rows fall from the images with only COCO classes to those with none.

**Controls.** In domain, the registered S-zf row puts `ret` − `zs` at +14.30 [13.38, 15.24], against P1's `ret` − `rand` of +4.49 [3.52, 5.57]; descriptively, random in-domain examples already score well above zero-shot (Table 6).

**What a practitioner can take from this.** Three things are needed before a gain over zero-shot is attributed to retrieval:
1. a random-example control at equal k, drawn from the same memory;
2. the result for each backbone, not only the pooled one;
3. to consider whether the memory's captions come from the target set's source. In this study the registered predictions passed only there, but memory source and test set changed together, and Qwen2.5-VL's out-of-source rows stayed above zero, so this is an observation and not a tested cause.

A post-decode deletion step needs the same care: on the development set it removed more from retrieved-example captions than from random ones (Section 6.8).

**Data and code availability.** We release:
- the registrations, with their pinned lists;
- the test code and the decision files;
- scores, image ids and sha256 hashes.

No caption from any dataset, no model caption and no per-image ledger is released. The authors of UIT-OpenViIC and KTVIC confirmed in writing (2026-10-28) the use of their datasets in this study; the confirmations are on file with the corresponding author. UIT-ViIC is not used as data; it appears only as aggregate counts and image-id pointers (Section 7.2), no UIT-ViIC caption or per-image panel is shown or released, and no permission from its authors is claimed.<!-- PI-1026az (2026-10-28); CC-126 W17 --> [Repository link and archive DOI withheld for anonymous review; an anonymised copy of the registrations, code and decision files can be provided to the editor.]

**Use of generative AI.** During this work the authors used AI-assisted tools (a large language model coding and writing assistant) to help write analysis scripts, check consistency between the text and the recorded results, verify bibliographic identifiers, and draft and edit text. The authors reviewed and edited all content and take full responsibility for it.
