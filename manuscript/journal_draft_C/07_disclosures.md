## 7. Disclosures

This section lists every deviation and exposure that touched the registered test, and every split decision a reader needs to judge it. None of them changed a configuration, threshold, metric, set or rule after a test output existed. Operational detail (the decode-parity reruns, the pinned worktree, the truncated-file retry counts and the timestamps of the English decision) is in the supplement, section "Test-run operations"; the full split list and the full record of earlier contact are in the supplement, section "Disclosure detail".

**Box 2. Disclosure summary.**

| item | effect on data | exposure of test data | verdict changed? |
|---|---|---|---|
| decode-parity check before the test needed three attempts | development images only (52/52 identical captions per backbone at the check of record) | none | no |
| XM3600 block run from a worktree pinned at the test commit | none; the test-code diff between the two commits is empty | none | no |
| three truncated OpenViIC test files decoded by a fixed retry rule | none excluded | none | no |
| 60 near-duplicates of the tuning images excluded from the primary set | the full 2,001 is reported beside it | none | no |
| test-image hashes, ids and reference counts read on CPU to pin lists | no model output | ids, bytes, counts; no caption used | no |
| earlier zero-shot decodes of 121 XM-dev500 images by another study | stage B only | none on any test set | no |
| UIT-ViIC reference pre-check by an unrelated project | 133 images are in the COCO Karpathy test | English references, in aggregate | no |
| per-backbone rows quoted in the abstract and contributions | none | none | no (see the deviation summary below) |
| English arm registered after the Vietnamese verdicts; NoCaps rule fixed after XM-a | none | none | no (Sections 8.1 and 8.5) |
| scorer rows that no rule registered | Table S12 only | none | no |

**Deviation summary.** The Vietnamese test registration bars its secondaries from the title, the abstract and the contributions as results (Section 5.3). The Vietnamese per-backbone information in the abstract and contributions is the registered scope sentence (Table 5), so it complies. The English registration has no such rule; the abstract and the contributions quote InternVL3's COCO per-backbone row as descriptive context, labelled as a reported row, because the pooled number alone would overstate the effect. No verdict depends on it. No registered rule, set, threshold or metric was changed.

### 7.1 Splits and exclusions

Section 4 and Table 3 give every split with its full size and the reason for each exclusion. The primary OpenViIC set excludes 60 near-duplicates of the tuning images, and the full 2,001 is in the main table (Table 7). XM-test2500 was fixed by a hash order before any output of this study, so a full-XM3600 result cannot exist without scoring another paper's reserved test set and our own stage-B set. KTVIC dev299 is not a fresh set: its parent carve set decoding options for a companion submission. The byte-identical pairs, the unreadable memory image and the dev299 zero-shot reuse are listed in the supplement.

### 7.2 Earlier contact with the test data, and work by other studies of the group

To pin lists, local CPU scripts read the OpenViIC test annotation keys, the test image bytes (for hashes) and the per-image reference counts of XM3600; no caption was used, printed or written, and no model output was computed. Another study of the group made zero-shot captions of 121 XM-dev500 images before our stage-B block; it never touched XM-test2500, and none of its outputs is reused.

A pre-check for another project read UIT-ViIC Vietnamese references and their COCO-English counterparts, in aggregate, for the UIT-ViIC training and validation images. No OpenViIC, KTVIC or XM3600 reference was read, so the exposure is not relevant to the Vietnamese results. 133 of these images are in the COCO Karpathy test, which is disclosed for the English arm (Section 8.5); the counts were made from image ids only. UIT-ViIC is not a data set of this study: it enters the paper only through these aggregate counts and id pointers, no UIT-ViIC caption or per-image panel appears in the paper or its release, and no permission from the UIT-ViIC authors is claimed.

### 7.3 Rows that no rule registered

The unchanged scorer also writes rows that no rule registered: InternVL3 at τ ∈ {0.00, 0.20, 0.30, +∞}, Qwen2.5-VL at τ = +∞, and InternVL3's verifier AUROC. They appear only in Table S12, labelled "not registered for any claim", and no decision step or claim reads them. Every configuration tried at stages A and B is in Tables S10–S11.

### 7.4 The English arm is a separate preregistered study

An English comparison was decided on the Vietnamese test day, after the OpenViIC test block had started and before the first Vietnamese decision file existed; the record states that the arm would be preregistered and run whatever the Vietnamese outcome (timestamps in the supplement). The English registration has its own directory, does not amend this paper's registration, and was committed before any English decode. It was written after the Vietnamese verdicts were known, and this is disclosed. English results change no Vietnamese claim; they and their own disclosures are in Section 8 only.
