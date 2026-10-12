# Pre-registered Vietnamese diagnostics for CN-RLOO vs P1_dev

Status: frozen 2026-10-12 16:50 UTC, before any CN-RLOO output exists (the first 35_c outputs are expected
around 21:00 UTC). Author: R6 agent N1 (research_r6/N1_vietnamese/REPORT.txt). The R6 judge accepted D3 (no GPU for
Vietnamese-specific components). These rates are interpretive diagnostics of what RL changes in Vietnamese. They
do not replace the CIDEr gate, and they gate nothing by themselves.

## Instrument (frozen)

| file | sha256 |
|---|---|
| scripts/vi_diagnostics.py | 1e4fc8b6653141204cd66f30581b276147b6600bee3db7a96ebe281e7f27f094 |
| person_terms.tsv | 361cca3cf459d7d2741c250a6c26b2e348942a926d98a018407e59b507d29fd9 |
| quantifiers.tsv | 83d2a94c7c37e209f5621e55cf15678b9859522ee56eff3ec857d2dca93a2172 |
| frames.tsv | 77f4208419bcdd2b8134490b7991e0c816e5204b3258d05df07c918fe77aba87 |
| culture_terms.tsv | 7c8bcf3cc14d80ad1bde2f27e09861cc82de593d62b134579ed4687b816adc8c |

The script prints both hashes (`script_sha256`, `lists_sha256`) in every report. A report whose hashes differ
from this table is not a test of these predictions. Any later change goes in a new dated prereg directory and is
reported as a deviation.

    NCS_DATA=data python scripts/vi_diagnostics.py --split dev --preds P1DEV_DEV_PREDS CNRLOO_DEV_PREDS --out OUT.json

`--preds` takes a preds.json (`{id: caption or [caption]}`) or an evaluate.py `--out` report. The first file is
the base. `compare` gives CN-RLOO minus P1_dev for every rate, with a 95% percentile CI over a paired bootstrap
of the 300 dev images (B = 2000, numpy seed 0).

## Data roles

- Dev: data/splits/ktvic_dev300.txt (300 KTVIC train images, string-id rule, judge D1/C1), scored against their
  KTVIC train references. Any go/no-go use of these rates must use dev.
- Test: reporting only.
- Lists: analysis lists, never labels. They only select which surface strings are counted.
  - The candidate inventories in the script are a priori (general Vietnamese lexicology).
  - `--build-lists` kept the candidates attested in the KTVIC train references of the 3,469 images outside
    dev300 (17,345 captions) and recorded their train counts.
  - Culture bands come from those counts: head >= 50 captions, mid 10-49, tail 1-9; unattested candidates were
    dropped.
  - No dev or test reference was used to build or band any list. No UIT-OpenViIC text is used anywhere.
- Text handling: lowercase, NFC, KTVIC old-style tone placement (hóa -> hoá), syllables; terms matched as
  syllable sequences, longest first. "xuất hiện" is counted only outside "sự xuất hiện".

## Rates

| rate | definition |
|---|---|
| person_bare / person_gendered / person_age | among captions naming a person: bare "người" only / a gendered term / an age-graded term |
| q_những, q_nhiều, q_một vài, q_các, q_một số, q_vài | occurrences per caption |
| f_của, f_sự xuất hiện, f_đang, f_xuất hiện | occurrences per caption |
| init_có, init_ở, init_một, init_đây | share of captions starting with the word |
| cons_spec_recall | images where >= 3 of 5 refs name the person with a gendered or age-graded term: share of captions that do |
| cons_bare_recall | images where >= 3 of 5 refs are bare-"người" only: share of captions that are |
| cons_nhung_recall | images where >= 2 of 5 refs use "những": share of captions that use it |
| cult_recall_head / mid / tail / all | (image, culture term) pairs named by >= 2 of 5 refs: share the caption names |
| cult_precision | share of the caption's culture-term mentions named by at least one reference |

## Frozen context (computed with the frozen instrument)

Reference profiles:

| rate | dev refs (300 img) | train refs, all positions | train refs, position 0 (P1's SFT target) |
|---|---|---|---|
| q_những | 0.107 | 0.145 | 0.122 |
| q_một vài | 0.061 | 0.059 | 0.062 |
| f_của | 0.247 | 0.232 | 0.091 |
| f_sự xuất hiện | 0.097 | 0.094 | 0.001 |
| f_đang | 0.514 | 0.518 | 0.653 |
| init_có | 0.573 | - | - |
| init_ở | 0.129 | - | - |
| person_bare / gendered / age | 0.429 / 0.351 / 0.242 | - | - |

P1 on TEST, reporting context only. P1_dev does not exist yet; it is a P1-style first-caption SFT, so a similar
profile is expected. Seeds 42 / 43 / 44:

| rate | P1 s42 / s43 / s44 |
|---|---|
| q_những | 0.034 / 0.043 / 0.036 |
| q_một vài | 0.111 / 0.102 / 0.111 |
| init_có | 0.959 / 0.955 / 0.966 |
| f_đang | 0.763 / 0.740 / 0.751 |
| f_của | 0.057 / 0.047 / 0.041 |
| f_sự xuất hiện | 0 / 0 / 0 |
| init_ở | 0 / 0 / 0 |
| cons_nhung_recall | 0.096 / 0.103 / 0.088 (136 images) |
| cons_spec_recall | 0.737 / 0.694 / 0.718 (209 images) |
| cult_recall_all | 0.413 / 0.396 / 0.393 |
| cult_recall_mid | 0.289 / 0.211 / 0.158 (38 targets) |
| cult_recall_tail | 0 / 0 / 0 (6 targets) |

## Evidence for the directions

Analysis on test samples, not a go/no-go use. The setup is the offline proxy for one RL step:
- Candidates per test image: 6 T = 0.8 samples + greedy (B1's copies for p1_s43 and fuse2_s42).
- Pick: by word-level CIDEr-D on refs A, over 4 non-interleaved splits.
- Comparison: rates of the picks minus greedy, 95% paired-bootstrap CI over 558 images.
- Population rates need no references. Consensus and culture rates were judged on the held-out refs B only:
  person "all of B"; những/culture ">= 2 of B, or both when |B| = 2". These are not the frozen definitions.

| rate | p1_s43 pick - greedy | fuse2_s42 pick - greedy |
|---|---|---|
| q_những | +0.042 [+0.022, +0.061] | +0.033 [+0.013, +0.053] |
| cons_nhung_recall (on B) | +0.112 [+0.028, +0.195] | +0.078 [+0.010, +0.154] |
| q_một vài | -0.028 [-0.050, -0.007] | -0.046 [-0.068, -0.024] |
| init_có | -0.097 [-0.121, -0.075] | -0.105 [-0.130, -0.079] |
| person_bare | -0.051 [-0.086, -0.018] | -0.028 [-0.057, +0.002] |
| culture recall (on B) | +0.059 [+0.012, +0.106] | +0.005 [-0.040, +0.051] |
| f_đang | -0.009 [-0.031, +0.015] | -0.033 [-0.057, -0.010] |
| f_của | +0.015 [-0.003, +0.032] | -0.009 [-0.028, +0.010] |
| q_nhiều | -0.031 [-0.056, -0.007] | +0.001 [-0.018, +0.021] |
| cons_spec_recall (on B) | +0.037 [-0.005, +0.079] | -0.007 [-0.049, +0.037] |
| f_sự xuất hiện, init_ở | 0.000 (never sampled) | +0.001 |

## Predictions: CN-RLOO minus P1_dev on dev (same 300 images, greedy, short prompt)

Primary (both policies agree in the evidence):

| id | rate | predicted | expected size |
|---|---|---|---|
| H1 | q_những | up | +0.02 to +0.06 per caption |
| H2 | cons_nhung_recall | up | +0.05 to +0.15 |
| H3 | q_một vài | down | -0.02 to -0.05 |
| H4 | init_có | down | -0.05 to -0.12 |

Secondary (one policy supports it; the other has the same sign, n.s.):

| id | rate | predicted |
|---|---|---|
| H5 | person_bare | down |
| H6 | cult_recall_all | up |
| H7 | f_đang | down |

Support-limited nulls. These apply when CN-RLOO is initialised from P1_dev (first-caption SFT). They are void if
the RL start point is an all-references (MR5) SFT, because position 0 almost never uses these constructions and
P1-style samples never produced them:

| id | rate | predicted |
|---|---|---|
| N1 | f_sự xuất hiện | stays <= 0.01 per caption (dev refs 0.097) |
| N2 | init_ở | stays <= 0.01 (dev refs 0.129) |

No directional prediction (reported only): f_của, f_xuất hiện, q_nhiều, q_các, q_một số, q_vài, person_gendered,
person_age, person_mention_share, cons_spec_recall, cons_bare_recall, cult_recall_head, cult_recall_mid,
cult_recall_tail, cult_precision, init_một, init_đây.

Expected tail-band targets on dev are too few for a test, and RL cannot create vocabulary that the SFT policy never
samples; cult_recall_tail is report-only.

## Decision rules (fixed now)

- A directional prediction is **confirmed** if the 95% CI of CN-RLOO minus P1_dev excludes 0 in the predicted
  direction. It is **refuted** if the CI excludes 0 in the opposite direction. Otherwise it is **inconclusive**.
  Expected sizes are descriptive and are not part of the rule.
- N1 and N2 are confirmed if CN-RLOO's dev rate is <= 0.01, and refuted otherwise.
- With several CN-RLOO seeds or checkpoints, the pre-registered comparison is the run and checkpoint that the CIDEr
  gate selects on dev. Others are reported as secondary.
- Reading: none of these outcomes changes a CIDEr decision.
  - CIDEr gain with H1-H4 confirmed: part of the RL gain runs through Vietnamese plural marking and frame choice.
  - CIDEr gain without H1-H4: the gain is content outside these lists.
  - H1-H4 confirmed without a CIDEr gain: RL moved form choices that do not transfer to unseen references. That is
    consistent with N1's finding that Vietnamese form variation is reference noise.
- Test-set values may be reported next to dev, never used to choose a run, checkpoint or threshold.
