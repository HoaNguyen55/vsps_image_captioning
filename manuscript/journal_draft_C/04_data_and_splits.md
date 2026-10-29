## 4. Data and splits

All data are existing public datasets with their released references and labels. No new annotation was made, and no model output is used as gold. KTVIC and UIT-OpenViIC captions are used only as research data, placed in prompts at run time and never redistributed.

**Table 3. Every set, with its full size and the reason for any exclusion.**

| set | role | images | how it was formed |
|---|---|---|---|
| memory | retrieval pool | 10,501 (8,190 clusters) | KTVIC train minus its 300-image development carve (3,469) plus OpenViIC train (9,088), less 2,056 near-duplicate, refused or unreadable images (Section 3.1) |
| KTVIC dev299 | stage A: configuration choice | 299 | the KTVIC development carve minus one image (id 1437) that is a near-duplicate of a KTVIC test image; KTVIC has no official validation split |
| OV-dev-A | stage A: advance check | 911 | OpenViIC dev (2,011 files) split by a hash order into 1,005 / 1,006 before de-duplication, then filtered |
| OV-dev-B | stage B: one-look gate | 925 | the other half, filtered against the same protected sets |
| XM-dev500 | stage B: secondary | 500 | the first images of the hash-ordered XM3600 remainder (below) |
| **OV-test primary** | **test (P1, P1b, P2)** | **1,941** | the full OpenViIC test minus 60 near-duplicates of KTVIC dev299, fixed before any test output |
| OV-test full | test sensitivity (registered) | 2,001 | all OpenViIC test files |
| **XM-test2500** | **test (XM-a, XM-b)** | **2,500** | XM3600 minus XM600 and minus XM-dev500 (below) |
| XM-test2500 without three-reference images | test sensitivity (registered) | 2,392 | minus the 108 images with three or more Vietnamese references |

**OpenViIC test.** The 2,001 test entries hold 1,997 distinct images: 4 pairs of files are byte-identical. Both entries of each pair are kept with their own references, and each entry is one bootstrap unit. No paired file is among the 60, so the primary set has 1,941 entries and 1,937 distinct images.

The 60 excluded files are near-duplicates of the KTVIC development images on which the configurations were chosen. They are a tuning overlap, so the exclusion applies to the primary, and the full 2,001-image result is reported beside it in the main table.

Three test files are truncated: `00000000768.jpg`, `00000001010.jpg` and `00000005095.jpg`. They are in both the primary and the full set. They are decoded with the strict decoder first and, only if it fails, with truncated loading enabled for that single call (retry counts in the supplement, "Test-run operations"). No file was excluded.

**XM3600.** All 3,600 XM3600 images were split before any output of this study existed:
- 600 images (XM600) belong to the test of the companion object-precision study and are excluded here;
- the other 3,000 were ordered by a hash of their image bytes; the first 500 form XM-dev500, our development set B secondary, and the remaining 2,500 form XM-test2500.

A full-XM3600 result for this study therefore cannot exist. It would score another paper's reserved test set and our own tuning set. The test uses the released Vietnamese references of the 2,500 images (5,108 references) and, offline only, the released human-verified Open Images labels.
