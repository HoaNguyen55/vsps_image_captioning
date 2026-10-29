## 7. Disclosures

This section lists every deviation and exposure that touched the registered test, and every split decision a reader needs to judge it. None of them changed a configuration, threshold, metric, set or rule after a test output existed. Operational detail (the decode-parity reruns, the pinned worktree, the truncated-file retry counts and the timestamps of the English decision) is in the supplement, section "Test-run operations".

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

**Deviation summary.** The Vietnamese test registration bars its secondaries from the title, the abstract and the contributions as results (Section 5.3). The Vietnamese per-backbone information in the abstract and contributions is the registered scope sentence (Table 5), so it complies. The English registration has no such rule; the abstract and the contributions quote InternVL3's COCO per-backbone row as descriptive context, labelled as a reported row, because the pooled number alone would overstate the effect. No verdict depends on it, and it is recorded here so that readers can weigh it. No registered rule, set, threshold or metric was changed. The other entries of Box 2 are procedural and are described below or in the supplement.

### 7.1 Splits and exclusions

Section 4 gives every split with its full size. In summary:
1. The primary OpenViIC set excludes 60 near-duplicates of the tuning images, and the full 2,001 is in the main table (Table 7).
2. The OpenViIC test entries hold 1,997 distinct images (4 byte-identical pairs).
3. Three truncated files are decoded with the rule above.
4. XM-test2500 is XM3600 minus XM600 (the refused test set of a companion submission) and minus XM-dev500 (our stage-B set). The split was fixed by a hash order before any output of this study. A full-XM3600 result cannot exist without scoring those sets.
5. The three-reference sensitivity (2,392 images) is reported beside each XM3600 prediction.
6. OV-dev-A and OV-dev-B together are the whole OpenViIC dev set (2,011 files), 911 and 925 after de-duplication.
7. KTVIC dev299 is the 300-image KTVIC development carve minus one image that is a near-duplicate of a KTVIC test image. KTVIC has no official validation split.
8. The memory is KTVIC train minus the development carve, plus OpenViIC train, de-duplicated to 10,501 images. One unreadable OpenViIC training image (`00000007169.jpg`) was dropped from the memory.

Three further facts concern overlap between splits:
- 3 OpenViIC test files are byte-identical to three OpenViIC dev files. The protected-set filter removed those dev files from OV-dev-B, and no development set or memory entry shares their bytes.
- 2 byte-identical OV-dev-B files affect stage B only.
- KTVIC dev299 is not a fresh set. Its parent carve set decoding options for a companion submission, and zero-shot captions of it existed before this study. The Qwen2.5-VL zero-shot arm on dev299 reused one such earlier decode, after a check that its model revision, prompt, token cap, decoding and environment matched this study's.

### 7.2 Earlier contact with the test data, and work by other studies of the group

**Pinned lists.** To pin the OpenViIC manifest and the three-reference list, local CPU scripts read the OpenViIC test annotation's keys, the test image bytes (for hashes) and the per-image reference counts of XM3600. The JSON loader parsed the caption fields, but no caption was used, printed or written.

**De-duplication.** Before stage A, perceptual hashes and copy-detection descriptors of the test images were computed on CPU for de-duplication. No model output was computed.

**Earlier decodes on the XM3600 development images.** Another study of the group, now stopped, made zero-shot captions and guard scores on 121 of the XM-dev500 images, with the same backbones and prompt, before our stage-B XM block. Our stage-B result is fresh for our decisions, because the configuration was frozen first. Our zero-shot captions of those images are, however, not unseen outputs. That study never touched XM-test2500, and this study reuses none of its outputs.

**Images read by an unrelated pre-check.** A pre-check for another project read reference captions, in aggregate, for the 2,695 UIT-ViIC training images. 163 of these are refused for development use. We recounted the 163 as the intersection of the refused COCO id lists with the UIT-ViIC training ids, using ids only. The lists overlap: the parts are 133, 59, 14 and 21, which sum to 227 because an image can sit in more than one list. The 924 UIT-ViIC validation images whose references the pre-check also read include 0 refused ids.

We checked whether this touches this paper's sets:
- what was read were UIT-ViIC Vietnamese references and their COCO-English counterparts;
- no OpenViIC, KTVIC or XM3600 reference was read, so no reference that this paper scores against was exposed, whatever pixel overlap may exist between the source image pools.

The exposure is therefore not relevant to the Vietnamese results. It is relevant to the English arm (133 of the images are in the COCO Karpathy test) and is disclosed there (Section 8).

### 7.3 Rows that no rule registered

The unchanged scorer also writes some rows that no rule registered:
- InternVL3 at τ ∈ {0.00, 0.20, 0.30, +∞};
- Qwen2.5-VL at τ = +∞;
- InternVL3's verifier AUROC.

They appear only in Table S12, labelled "not registered for any claim". The development-set counterparts of the InternVL3 τ rows (stage B, OV-dev-B) were registered later by the mechanism ablation of Section 6.8, before anyone read them; that registration covers the development rows only and makes no claim about the test rows. No decision step reads them and the text makes no claim from them. Every configuration tried at stages A and B is in the supplement (Tables S10–S11).

### 7.4 The English arm is a separate preregistered study

An English comparison (the COCO Karpathy test as primary) was decided on the Vietnamese test day, after the OpenViIC test block had started and before the first Vietnamese decision file existed. The decision was recorded in the project's working and decision logs, which are not under version control; their timestamps are in the supplement. The record states that the arm would be preregistered and run whatever the Vietnamese outcome. Both English verdicts became available, so the arm is reported in full in Section 8.

The English registration has its own directory and does not amend this paper's registration. It carries over the frozen k, order, τ and backbones with no English tuning, and it was committed before any English decode. It was written after the Vietnamese verdicts were known, and this is disclosed. English results change no Vietnamese claim, and no English analysis is offered in place of a Vietnamese one. Its results and its own disclosures are in Section 8 only.
