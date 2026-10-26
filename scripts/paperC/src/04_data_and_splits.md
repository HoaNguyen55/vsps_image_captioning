## 4. Data and splits

All data are existing public datasets with their released references and labels. No new annotation was made, and no model output is used as gold. KTVIC and UIT-OpenViIC captions are used only as research data, placed in prompts at run time and never redistributed.

**Table 2. Every set, with its full size and the reason for any exclusion.**

| set | role | images | how it was formed |
|---|---|---|---|
| memory | retrieval pool | {{LISTS:counts.memory_images|i}} ({{LISTS:counts.memory_clusters|i}} clusters) | KTVIC train minus its {{LISTS:counts.groups.kt_dev300|i}}-image development carve ({{LISTS:counts.groups.kt_mem|i}}) plus OpenViIC train ({{LISTS:counts.groups.ov_train|i}}), less {{LISTS:counts.memory_dropped|i}} near-duplicate, refused or unreadable images (Section 3.1) |
| KTVIC dev299 | stage A: configuration choice | {{CHAIN:dev299_staged|i}} | the KTVIC development carve minus one image (id {{C:dev299_dropped_id|raw}}) that is a near-duplicate of a KTVIC test image; KTVIC has no official validation split |
| OV-dev-A | stage A: advance check | {{LISTS:counts.ov_dev_a|i}} | OpenViIC dev ({{LISTS:counts.groups.ov_dev|i}} files) split by a hash order into {{LISTS:counts.ov_dev_a_raw|i}} / {{LISTS:counts.ov_dev_b_raw|i}} before de-duplication, then filtered |
| OV-dev-B | stage B: one-look gate | {{LISTS:counts.ov_dev_b|i}} | the other half, filtered against the same protected sets |
| XM-dev500 | stage B: secondary | {{LISTS:sets.xm_dev500.#len|i}} | the first images of the hash-ordered XM3600 remainder (below) |
| **OV-test primary** | **test (P1, P1b, P2)** | **{{PL:ov_test_primary1941.txt|i}}** | the full OpenViIC test minus {{PL:neardup60|i}} near-duplicates of KTVIC dev299, fixed before any test output |
| OV-test full | test sensitivity (registered) | {{PL:ov_test_files.tsv|i}} | all OpenViIC test files |
| **XM-test2500** | **test (XM-a, XM-b)** | **{{CHAIN:xm_staged|i}}** | XM3600 minus XM600 and minus XM-dev500 (below) |
| XM-test2500 without three-reference images | test sensitivity (registered) | {{L2392:ct_qwen25vl_7b_xm_test2500-ret-k8-first-T1@-inf:n|i}} | minus the {{PL:xm_test2500_threeref108.txt|i}} images with three or more Vietnamese references |

**OpenViIC test.** The {{PL:ov_test_files.tsv|i}} test entries hold {{CHAIN:ov_distinct|i}} distinct images: {{C:dup_pairs|i}} pairs of files are byte-identical. Both entries of each pair are kept with their own references, and each entry is one bootstrap unit. No paired file is among the {{PL:neardup60|i}}, so the primary set has {{PL:ov_test_primary1941.txt|i}} entries and {{C:primary_distinct|i}} distinct images.

The {{PL:neardup60|i}} excluded files are near-duplicates of the KTVIC development images on which the configurations were chosen. They are a tuning overlap, so the exclusion applies to the primary, and the full {{PL:ov_test_files.tsv|i}}-image result is reported beside it in the main table.

Three test files are truncated: `00000000768.jpg`, `00000001010.jpg` and `00000005095.jpg`. They are in both the primary and the full set. They are decoded with the strict decoder first and, only after it fails, with truncated loading set and reset around that single call. This happened in every step that opens an image (Section 7.3). No file was excluded.

**XM3600.** All {{LISTS:counts.groups.xm_all|i}} XM3600 images were split before any output of this study existed:
- {{C:xm600|i}} images (XM600) belong to the test of companion submission A and are refused here;
- the other {{C:xm_nonxm600|i}} were ordered by a hash of their image bytes; the first {{LISTS:sets.xm_dev500.#len|i}} form XM-dev500, our development set B secondary, and the remaining {{LISTS:sets.xm_test2500.#len|i}} form XM-test2500.

A full-XM3600 result for this study therefore cannot exist. It would score another paper's refused test set and our own tuning set. The test uses the released Vietnamese references of the {{CHAIN:xm_staged|i}} images ({{CHAIN:xm_ref_annotations|i}} references) and, offline only, the released human-verified Open Images labels.
