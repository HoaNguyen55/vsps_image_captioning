# Paper E, stage 1: split addendum

**Label: EXPLORATORY / DEV.** This addendum is not a registration. It carries out DESIGN §2.4 under CC-081 (E4, E5) and CC-081b.

| field | value |
|---|---|
| Design | `DESIGN.md` sha256 `c793cbe6f9b57aca71a70e5cdcc954d914624e89b93661015a430802a9ae98bd`, unchanged since commit b46ebe6 |
| Paper C lists | `manuscript/prereg/2026-10-22_c_stage1/lists.json` sha256 `5c479f03e8be544f4cd12b5d997b5dc92b6c622df061760cd02f6ba82f6b4371` (commit 6129e8e) |
| Written | 2026-10-22, locally on CPU. Nothing ran on M3, and no model, judge or embedding ran anywhere. |

## 1. The split

`e_lists.py split --c-lists manuscript/prereg/2026-10-22_c_stage1/lists.json` wrote `e_split.json`:
- sha256 `795652f1af45597b3a89f8a937056a1810504d54e1e41319198b3fb27fea2ef9`;
- XM-dev500 equals Paper C's `xm_dev500` (checked by image sha256), and `e_split.json` records C's lists sha256;
- its 6-gram and 8-gram scans against KTVIC, OpenViIC and XM3600 vi+en captions found 0 hits.

| set | images | Paper A's three-reference images |
|---|---|---|
| XM600 | 600 | 27 |
| E-dev-A | 250 | 7 |
| E-dev-B | 250 | 8 |
| XM-test2500 | 2,500 | 108 |

- The counts reproduce CC-081 E4's 600 / 250 / 250 / 2,500 and 27 / 7 / 8 / 108; `split` refuses on any mismatch.
- `refuse_image_sha256` holds 3,350 sha256: XM600, E-dev-B and XM-test2500.

## 2. Code change in this addendum

`scripts/e_stage1/e_lists.py`:
- `SPLIT_SHA256` is set to the sha256 above, so the GPU modes and `pairs.py` can now load the split.
- `M3_ABSENT_DATA` also lists `$NCS_DATA/datasets/xm3600/images` (CC-081b).
  - Every `judge.py` mode now refuses while that folder exists on the host.
  - E's pair-image folder therefore lives elsewhere on M3, at a path passed with `--images`. This supersedes the phrase "only the copied pair-image folder if it is placed there" in DESIGN §2.6: the pair images are never placed under `datasets/xm3600/`.

`scripts/e_stage1/judge.py`, self-test only: the check "no GPU step while the split is unpinned" now passes the pin as `None` explicitly. It also checks that a split file other than the pinned one is refused.

Neither change alters a rule of the design, so `DESIGN.md` and its sha256 stay as they are. All four `--selftest`s pass, and `aislop scan` gives 100 with no findings.

## 3. Images that go to M3 (CC-081 E5)

- **121 E-dev-A images.** These are the labelled E-dev-A images (128) that have at least one base reference naming a class.
  - The list is `e_dev_a_pair_images.tsv` next to this note: image id, file name and image sha256, one per line. Its sha256 is `246756171101213ca25a2d762c63b31ef43691c6b62dbbe3f17c5a0d2c4511f1`, and its 6-gram and 8-gram scans found 0 hits.
- **Why 121 and not 115.** 115 of these images carry at least one pair. The other 6 have a base caption but no constructible pair. They are still decoded and judged, because their model captions enter τ (DESIGN §3.6).
- **Where they go.** The images are copied into one folder on M3 that holds nothing else, outside `$NCS_DATA/datasets/xm3600/`. The run record keeps the count and sha256 list, and must match the TSV.
- **When.** Under CC-081 E3 (DESIGN binding 5), not before Paper C's stage-2 prereg is committed or C has stopped. Before that, the operator also removes `data/xm3600/oiv7_labels.json` from M3 and records its absence (DESIGN §2.6, CC-081 E1).

## 4. Local pair build (DESIGN §3; outputs git-excluded)

`pairs.py build` and `pairs.py items` ran locally and wrote to `.session_backup/2026-10-22/e_stage1/`, which `.git/info/exclude` covers. Those files are never committed.

| file | sha256 |
|---|---|
| `pairs.jsonl` (ids, types, classes; no text) | `6bad4850534d18269764af223bf96c4c113020ec85f1a9fea58708441f5a2e7f` |
| `captions.jsonl` (E-dev-A base and perturbed texts) | `16ab2b42f92cbeb037c5ad32f8f4d5573712fbdd6c9324ccaa4c39514fa5205b` |
| `items.jsonl` (image, class) | `882fdecf333fffe29f010c13fdd8515cecec5033dfde0be19832d7baa7c1fb40` |
| `pairs.counts.json` | `8b35026a03850942f46708c9773215491cc8608c2d5f01f87d7ff903cc0d3ab0` |

**Counts**

| type | vi | en |
|---|---|---|
| swap | 28 | 31 |
| add_absent | 113 | 72 |
| add_present | 158 | 121 |
| delete | 47 | — |
| ool_absent | 40 | — |
| pad | 74 | 48 |
| pad_control | 86 | 63 |
| **bc pairs (images)** | **77 (43)** | 49 (30) |

- **Bases.** 385 base references name a class. 34 Vietnamese and 93 English references name none.
- **Captions and items.** There are 1,266 captions (bases plus perturbed) and 669 (image, class) items over 121 images.
- **JUDGE rule.** DESIGN §7.3 returns JUDGE when fewer than 40 images contribute Vietnamese bc pairs. There are 43, so the rule is not triggered. The margin is thin, as CC-081 noted under Risks.
- **Same as the dry run.** Every count equals the counts-only dry run disclosed in DESIGN §10.

## 5. Disclosures

- **`items` has to run again.** It was run before any model caption existed, so `items.jsonl` and `captions_all.jsonl` cover base and perturbed captions only.
  - Under DESIGN §8 step 2, the decodes are copied back after step 1 and `items` runs again locally with `--preds`.
  - The 669 items are a lower bound; the design expects about 900 once model captions are added.
- **What this build read.** It read E-dev-A references and the OIV7 labels of E-dev-A images in memory, locally (CC-081 (b) allows this). It printed counts only. No caption was printed or inspected.
- **Three-reference images.** 2 of the 121 pair images are among Paper A's three-reference images; 7 are in all of E-dev-A. They stay in, under CC-081 E2.
- **M3 was not touched.** Nothing ran or was copied there.
