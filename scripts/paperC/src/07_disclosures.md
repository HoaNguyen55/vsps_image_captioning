## 7. Disclosures

This section lists every deviation, rerun and exposure that touched the registered test, together with every split decision a reader needs to judge it. None of them changed a configuration, threshold, metric, set or rule after a test output existed.

### 7.1 Decode-parity check before the test, and its reruns

Before any test image reached the decoding machine, the registration required a fresh decode-parity check on that machine. The frozen `ret` arm of each backbone re-decodes a fixed slice of KTVIC dev299 images through the test decode path. Each backbone passes if at least {{C:e4_pass_pct|i}}% of its captions are identical to the stage-A captions. The slice was {{E4Q:n|i}} images, a development set; it is a parity check and is never reported as a result. The check needed three attempts.

1. **Attempt 1: stopped before any decoding.** The job's preflight self-test failed on the test machine and passed locally. A self-test wrote to a temporary path, and on the test machine the output guard correctly refused that path. No model was loaded, nothing was decoded, and the cap ledger recorded {{GS:0|i}} GPU-seconds. The fix changed only self-test code. An independent review checked it as test-only and ruled this attempt final. The development images were removed and staged again at the new code commit.
2. **Attempt 2: {{E4R2Q:passed|v:pass}} (Qwen2.5-VL) and {{E4R2I:passed|v:pass}} (InternVL3), but its record could not be closed.** Both backbones gave identical captions: Qwen2.5-VL {{E4R2Q:identical|i}}/{{E4R2Q:n|i}} and InternVL3 {{E4R2I:identical|i}}/{{E4R2I:n|i}} ({{GS:1|i}} GPU-seconds). The run then stopped at the mirror checksum step. The checksum list named two partial-progress files that the mirror deliberately skips. After review, the checksum code was fixed and the reviewer authorised one rerun of the check, fixing in advance that the third run would be the check of record and that the second could not rescue it. The second run's outputs were kept under a separate name, which needed one manual rename on the test machine. The review ruled that rename a one-time deviation.
3. **Attempt 3, the check of record: {{E4Q:passed|v:pass}} (Qwen2.5-VL) and {{E4I:passed|v:pass}} (InternVL3).** Qwen2.5-VL gave {{E4Q:identical|i}}/{{E4Q:n|i}} ({{E4Q:pct|f1}}%) and InternVL3 {{E4I:identical|i}}/{{E4I:n|i}} ({{E4I:pct|f1}}%) identical captions, with identical prompts ({{GS:2|i}} GPU-seconds). The development images were deleted, and the deletion recorded, before the OpenViIC test images were staged.

All three attempts used development data only. No test image was involved, so the one-look rule did not apply. Together they used {{CHAIN:e4r3_total|p}} GPU-hours, counted against the test cap. Each code fix was a new commit with its own review, and both test blocks ran at the last of these commits.

### 7.2 The XM3600 block ran from a pinned worktree

After the OpenViIC block, the local repository's HEAD had moved, by a commit that changed no test code: the diff of the test code directory between the two commits is empty. The run script's first check refused to start because the local HEAD differed from the test commit. This happened before anything was staged or read.

The XM3600 block and the offline verified-precision step were then run from a separate worktree detached at the test commit. Its checksums verified, and a dry run of the scorer gave output byte-identical to the reviewed dry run. The decoding machine stayed at the test commit throughout. Both XM3600 decision files record the same registration hash and frozen-configuration hash as the OpenViIC decision file.

### 7.3 Truncated OpenViIC test files

The three truncated OpenViIC test files took the retry path:
- in the query-embedding step ({{T6:embed.records|i}} records);
- in each of the {{T6:decode.steps|i}} OpenViIC decodes ({{T6:decode.records|i}} records);
- in the verifier pass, for one file that had neighbour-only classes ({{T6:verify.records|i}} record).

No other file failed its strict decode, and no file was excluded. All three files are in both the primary set and the full set.

### 7.4 Splits and exclusions

Section 4 gives every split with its full size. In summary:
1. The primary OpenViIC set excludes {{PL:neardup60|i}} near-duplicates of the tuning images, and the full {{PL:ov_test_files.tsv|i}} is in the main table (Table 6).
2. The OpenViIC test entries hold {{CHAIN:ov_distinct|i}} distinct images ({{C:dup_pairs|i}} byte-identical pairs).
3. Three truncated files are decoded with the rule above.
4. XM-test2500 is XM3600 minus XM600 (the refused test set of a companion submission) and minus XM-dev500 (our stage-B set). The split was fixed by a hash order before any output of this study. A full-XM3600 result cannot exist without scoring those sets.
5. The three-reference sensitivity ({{L2392:ct_qwen25vl_7b_xm_test2500-ret-k8-first-T1@-inf:n|i}} images) is reported beside each XM3600 prediction.
6. OV-dev-A and OV-dev-B together are the whole OpenViIC dev set ({{LISTS:counts.groups.ov_dev|i}} files), {{LISTS:counts.ov_dev_a|i}} and {{LISTS:counts.ov_dev_b|i}} after de-duplication.
7. KTVIC dev299 is the {{LISTS:counts.groups.kt_dev300|i}}-image KTVIC development carve minus one image that is a near-duplicate of a KTVIC test image. KTVIC has no official validation split.
8. The memory is KTVIC train minus the development carve, plus OpenViIC train, de-duplicated to {{LISTS:counts.memory_images|i}} images. One unreadable OpenViIC training image (`{{LISTS:unreadable_memory_dropped.ov_train.0|raw}}`) was dropped from the memory.

Three further facts concern overlap between splits:
- {{C:ov_devdup3|i}} OpenViIC test files are byte-identical to three OpenViIC dev files. The protected-set filter removed those dev files from OV-dev-B, and no development set or memory entry shares their bytes.
- {{C:devb_dup2|i}} byte-identical OV-dev-B files affect stage B only.
- KTVIC dev299 is not a fresh set. Its parent carve set decoding options for a companion submission, and zero-shot captions of it existed before this study. The Qwen2.5-VL zero-shot arm on dev299 reused one such earlier decode, after a check that its model revision, prompt, token cap, decoding and environment matched this study's.

### 7.5 Earlier contact with the test data, and work by sister studies

**Pinned lists.** To pin the OpenViIC manifest and the three-reference list, local CPU scripts read the OpenViIC test annotation's keys, the test image bytes (for hashes) and the per-image reference counts of XM3600. The JSON loader parsed the caption fields, but no caption was used, printed or written.

**De-duplication.** Before stage A, perceptual hashes and copy-detection descriptors of the test images were computed on CPU for de-duplication. No model output was computed.

**Earlier decodes on the XM3600 development images.** A sister study, now stopped, made zero-shot captions and guard scores on {{C:e_dev_a|i}} of the XM-dev500 images, with the same backbones and prompt, before our stage-B XM block. Our stage-B result is fresh for our decisions, because the configuration was frozen first. Our zero-shot captions of those images are, however, not unseen outputs. That study never touched XM-test2500, and this study reuses none of its outputs.

**Images read by an unrelated pre-check.** A pre-check for another project read reference captions, in aggregate, for the {{C:uitviic_train|i}} UIT-ViIC training images. {{C:refused163|i}} of these are refused for development use. We recounted the {{C:refused163|i}} as the intersection of the refused COCO id lists with the UIT-ViIC training ids, using ids only. The lists overlap: the parts are {{C:refused163_karpathy|i}}, {{C:refused163_coco2500|i}}, {{C:refused163_chair|i}} and {{C:refused163_pope|i}}, which sum to {{C:refused163_sum|i}} because an image can sit in more than one list. The {{C:uitviic_val|i}} UIT-ViIC validation images whose references the pre-check also read include 0 refused ids.

We checked whether this touches this paper's sets:
- what was read were UIT-ViIC Vietnamese references and their COCO-English counterparts;
- no OpenViIC, KTVIC or XM3600 reference was read, so no reference that this paper scores against was exposed, whatever pixel overlap may exist between the source image pools.

The exposure is therefore not relevant to the Vietnamese results. It is relevant to the English arm ({{C:refused163_karpathy|i}} of the images are in the COCO Karpathy test) and is disclosed there (Section 8).

### 7.6 Rows that no rule registered

The unchanged scorer also writes some rows that no rule registered:
- InternVL3 at τ ∈ {0.00, 0.20, 0.30, +∞};
- Qwen2.5-VL at τ = +∞;
- InternVL3's verifier AUROC.

These are archived and will appear only in a supplementary all-rows table labelled "not registered for any claim". No decision step reads them and the text makes no claim from them. Every configuration tried at stages A and B goes into an "all configurations tried" appendix.

### 7.7 The English arm is a separate preregistered study

An English comparison (the COCO Karpathy test as primary) was decided on the test day, 2026-10-26. The commitment was recorded in the project's working log at {{C:cen_logged|raw}} and approved by the principal investigator at {{C:cen_approved|raw}} (decision log PI-1026b). Neither record is a git commit, and the working log is not under version control. Both were written after the OpenViIC test block had started ({{CHAIN:ov_job_start|raw}}) and before the first decision file existed (decide_ov.json::utc, {{OV:utc|raw}}). The record states that the arm will be preregistered and run whatever the Vietnamese outcome. By a later decision (decision log PI-1026l), this paper may be submitted without the English arm if the arm's verdict is not available in time; the arm then enters at revision under its own registration.

The English registration has its own directory and does not amend this paper's registration. It carries over the frozen k, order, τ and backbones with no English tuning, and it will be committed before any English decode. It will be written after the Vietnamese verdicts were known, and this is disclosed. English results will not change any Vietnamese claim, and no English analysis is offered in place of a Vietnamese one. Its results enter Section 8 only.
