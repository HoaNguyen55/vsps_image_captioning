# Paper C stage 1: lists addendum (DESIGN §2.6)

Written 2026-10-22 before any Paper C decode. Rulings: CC-079 (C2, C3), CC-080, CC-082.

## lists.json
- sha256 `5c479f03e8be544f4cd12b5d997b5dc92b6c622df061760cd02f6ba82f6b4371`; `decode_icl.LISTS_SHA256` is set to this value in the same commit.
- Built locally on CPU with `scripts/c_stage1/build_memory.py lists`, sha256 `e771b92df9096e286e8d5de207d3adafe49c8e5e59eab276978b0236cc0eeab9`. The near-duplicate rule is the registered matcher `scripts/match_openviic.py`, sha256 `c0d9dd30e3222ab6542a7e1acfbb9bd3899e4b6db5c896b0adc4d805c1005a8b`.
- It embeds the DESIGN sha256 `eacc9a9c737cec278c77ce5acd3b07422c9b0f7e661624ec42ba0454050ed53f`.
- C3: `caption_8gram_hits` = 0 (the build scans its own output against the KTVIC and OpenViIC captions and refuses to write on any hit).

## Counts (`lists.json["counts"]`)
| quantity | value |
|---|---|
| OV-dev-A, before and after the protected-set cut | 1,005 → 911 |
| OV-dev-B, before and after the protected-set cut | 1,006 → 925 |
| XM-dev500 / XM-test2500 | 500 / 2,500 |
| memory candidates (KTVIC train minus dev300, plus OpenViIC train) | 12,557 |
| memory images dropped (near-duplicate of a protected image, refused sha, or unreadable) | 2,056 |
| memory images kept / clusters | 10,501 / 8,190 |
| refused OpenViIC files / refused image sha256 | 3,007 / 6,599 |
| groups hashed | kt_mem 3,469; kt_dev300 300; kt_test 558; xm_all 3,600; ov_train 9,088; ov_dev 2,011; ov_test 2,001 |

## C2 records
| | SigLIP2 | SSCD weights |
|---|---|---|
| source | `google/siglip2-so400m-patch14-384` @ `e8e487298228002f3d8a82e0cd5c8ea9c567f57f` | `https://dl.fbaipublicfiles.com/sscd-copy-detection/sscd_disc_mixup.torchscript.pt` |
| licence | apache-2.0 (model-card front matter and hub metadata agree) | mit (facebookresearch/sscd-copy-detection LICENSE; the weights are linked from its README) |
| sha256 | README `5c02af3cafc849e2acbc03630b4ef9de4cc3c29f8bbef613bf7484fe4be9a897`; config `73477b47ae9a395f008f993ebd8fb5c16ce0b5e8419ffdf2f5b2183b260f9cff`; weights LFS `9f4f4a49f908ef0c979bce8ff5a5c0e88882dc6c5dc4304387cbbd152558e2c2` | `9f26bd4c848cc19b73d2ae92eea6e04886f61a7b764ceb7a13aeee62e6a6db56` |

Both licences are in `build_memory.RESEARCH_OK`. The SSCD file used for the earlier OpenViIC match was on a former machine, and no record gives its URL or sha256. The dev-pool exclusion used that match's records, not SSCD weights.

## Disclosures (CC-080, CC-082)
- **Build fixes (implementation only).** The committed build at 5831fd4b failed twice before writing anything:
  - it ran out of memory, fixed with bounded batches of 256 (same order and computations);
  - it stopped on an unreadable image, now handled per the matcher's rule (see the next two items).
  A per-group feature cache (git-excluded, keyed by image and SSCD sha256) was added. The final build also restricts `subset()`/`concat()` to the per-image feature rows.
- **Unreadable memory image dropped.** OpenViIC train `00000007169.jpg` is truncated (1 byte not processed). It is dropped from the memory and counted in `memory_dropped` (`unreadable_memory_dropped`).
- **Truncated test images decoded.** Three OpenViIC test images are truncated: `00000000768.jpg` (18 bytes), `00000001010.jpg` (155 bytes) and `00000005095.jpg` (76 bytes). Under CC-082 (a):
  - they were decoded with PIL truncated loading, used only for protected groups, only after the normal decode failed, and set and reset around that single call;
  - their pHash, dHash and SSCD are finite;
  - they stay in the refuse list (`truncated_protected_decoded`);
  - none is excluded (`unreadable_test_excluded` = []).
- **CC-082 T4.** `dev299_near_truncated_test` = 0: no KTVIC dev300 image is a near-duplicate of the three decoded test images, so the dev-pool clearance stands.
- **Cache provenance.** Six group caches (kt_mem, kt_dev300, kt_test, xm_all, ov_train, ov_dev) were made by build_memory 246427ec. The ov_test cache was deleted and recomputed with the CC-082 retry (ebfb03fd). The last code change (e771b92d) touches only how cached rows are subset and concatenated, not how features are computed.
- **C's test prereg (CC-082 T6)** must fix how these three test images are decoded before any test decode. The default is the same truncated loading, keeping OV-test at 2,001 images.
