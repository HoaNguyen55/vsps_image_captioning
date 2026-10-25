# Paper E' H2 precheck note: the deletion ceiling of contrastive decoding under greedy search

**EXPLORATORY / DEV-PRECHECK (CC-098, CC-101; H2 is the backup after the H1 pilot's NO-GO). Not confirmatory.** It makes no claim.
- **STOP** closes H2 before any pilot.
- **GO** means "not ruled out". It is not evidence for H2, and it only authorises writing an H2 pilot note (≤ 2 GPU-h, in CC-098's rule shape).

Committed before any computation, including step 0. Times are UTC.

## Question
H2 is selective VCD: contrastive decoding applied at some steps only. It must beat greedy decoding (CC-098).

Under greedy search, VCD's adaptive plausibility constraint keeps only the head set V_head = {v : p(v) ≥ β · max p}, and takes the argmax of the contrasted logits inside it. So with β ≥ 0.1, a token can differ from greedy only at a step where |V_head| ≥ 2 at β = 0.1. After the first such step, every later token may differ.

The precheck measures the **deletion ceiling**: the object-F1 gain from removing every changeable wrong mention, with recall held fixed. **This is not an upper bound on CD's F1 gain.** A rewrite after a change can also add or drop right objects.

H2 is proposed as hallucination reduction. If deleting every hallucination reachable at β = 0.1 cannot reach the SESOI of +2.0 object F1 points, then H2's proposed mechanism cannot reach it either. Reviving H2 on recall grounds after a STOP would be a new direction, and it would go to the PI.

The H2 pilot must use β ≥ 0.1, or this bound does not bind it.

## Step 0 (CPU, no GPU; CC-101 W1)
`flipbudget.py ceiling` uses the E' pilot's mirrored arm-D outputs (`ep_*-d.preds.json`).
- Every wrong mention is removed, and object F1 minus greedy is computed with the pilot's rows, F1, pooling and bootstrap.
- **If the pooled ceiling is < 2.0: STOP, with no GPU spent.** Otherwise the GPU step below runs.

## Decode (GPU; ≤ 1 GPU-h, a named CC-101 deviation from CC-098's 0-GPU precheck shape)
- **Arm and code path.** The arm is the E' pilot's arm D, unchanged: the B-N1 short Vietnamese prompt (sha256 8870589c), greedy, 60 new tokens. The batch slices and code path are the same (`decode_pilot.run_arm`, `lb.load`). The outputs inherit run_arm's provenance strings; the note and decoder shas in each file identify this precheck.
- **What is added.** `generate` gets `output_scores=True` and `output_logits=True`. Per step, the job keeps:
  - |V_head| at β = 0.1, on the processed scores that the greedy argmax uses, and on the raw logits, where VCD's reference code applies the cutoff;
  - the top-2 log-probability gap;
  - the token's end offset in the caption;
  - each record also carries the sha256 of its caption.
- **Models.** Qwen2.5-VL-7B and InternVL3-8B, at the B-N1 snapshots.
- **Sets.** The E' pilot's sets: KTVIC dev299 (sha256 a4ac7fdb) and XM-dev300 (sha256 b6331534).
  - The pilot already spent both, so no fresh set is spent here.
  - The disjointness refusals are the pilot's: 0 images in OV-test, XM-test2500, A's XM600, or any A, B or C test set.
  - These sets cannot be E' confirmation sets (CC-098 §3).
- **Parity.** The share of captions identical to the pilot's arm D is reported per cell. It is not a gate.
  - A cell below 95% is recorded as "rebuild not faithful". The rebuilt M3 (2026-10-25) must then be diagnosed before C's test prereg fixes M3's environment.

## Metric (local, CPU; Paper A's matcher v2 `rescap.chair.objects_in`; gold as in the pilot)
- **Wrong mention.** Its class is not in the KTVIC gold (the union of the image's references), or it is OIV7-`absent` on XM (`xm3600_oiv7`).
- **Location.** Each distinct mention is located at the first whole-word occurrence of its tone-normalised form whose blanking removes the mention from `objects_in`. The test window is the occurrence plus up to 2 words on each side.
  - So `xe` inside `xe máy`, `cây` inside `xanh lá cây` and `người` inside `người đàn ông` are passed over.
  - The located span is then mapped to tokens by their end offsets.
  - A zero-width token right after a mention token belongs to the mention (it completes a byte). EOS never belongs to a mention.
- **Changeable step.** |V_head| ≥ 2 on the processed scores or on the raw logits.
  - **own:** a token of the mention is changeable.
  - **cascade:** some token up to the mention's last token is changeable.
- **Bounds.** Remove every changeable wrong mention, change nothing else, and compute object F1 exactly as in the pilot (`score_pilot.rows_of`, `f1`). Each bound is that F1 minus greedy, in points × 100.
  - Pooled = the mean over the 4 cells (2 models × 2 sets), and by model = the mean over that model's 2 sets.
  - Paired image bootstrap: 2,000 draws, seed 0, 95% percentile CI.
  - Unlocated mentions count as changeable for the verdict. Both bounds are also reported with them counted as not changeable.
- **Reported, no rule (CC-101 W6):**
  - the ceiling and the per-model bounds;
  - the n of the labelled XM images;
  - the shares of wrong and right mentions that are changeable, the wrong ones split by single-syllable and multi-syllable mentions (CC-098's compound premise);
  - the share of steps with |V_head| ≥ 2, on processed scores and on raw logits;
  - the median first changeable step;
  - per-cell greedy F1 beside the pilot's arm-D F1;
  - the parity.

## Decision rule (`flipbudget.decide`, CC-101)
- **STOP** if the pooled cascade bound is < 2.0. Deleting every hallucination reachable at β = 0.1 cannot reach the SESOI. H2 closes, and E' goes back to the judge and the PI.
- **GO-own** if the cascade bound is ≥ 2.0 and the own bound is ≥ 2.0.
- **GO-cascade-only** if the cascade bound is ≥ 2.0 and the own bound is < 2.0.
  - The H2 pilot note must then say that any gain has to come from rewrites after a change, not from a corrected object token.
- In every GO, a model whose cascade bound is < 2.0 is report-only in the H2 pilot. The pooled rule is unchanged.
- **TO-JUDGE** if either of these happens:
  - the verdict with unlocated mentions counted as not changeable differs from the deciding verdict;
  - a cell has 0% steps with |V_head| ≥ 2 on the processed scores (the signature of a sampling warper leaking into the scores).
- **Next step (CC-101 O4).** The H2 pilot's step-selection rule must be fixed from the literature, or written down before this precheck's scores are read. Otherwise the pilot is read on disjoint images that the judge names.

## Budget and data handling
- **GPU:** ≤ 1 GPU-h wall for the whole job (hard `timeout`), one RTX 3090 (M3), never in C's January test window. The estimate is ~0.45 h: arm D took 22 min of decode for the four cells in the E' pilot, plus the model loads.
- **Preflight (CC-101 O1).** The job refuses to start unless all of these hold:
  - the venv-lb freeze sha256 is 685ffe2a…;
  - there is no `decide_final*`, `verified*.jsonl` or `oiv7*` file on M3;
  - there is no `oiv7_labels.json` in the checkout;
  - there are no earlier `h2_*` outputs.
- **Host state.** C's stage-2 XM dev state is re-staged exactly as for the E' pilot (CC-100b, the same files and shas). Then come the host check, the run, a mirror with sha check, and the CC-099 clean-up.
  - The clean-up runs on every exit after staging (CC-101 O2).
  - Nothing from XM-test2500 or OV-test goes to M3, and no OIV7 labels.
- **Outputs.** Captions and per-step records stay in output files on M3 and in local scratch. They are never committed or printed. The committed record holds numbers, ids and sha256 only.
- **Gold.** Existing gold only, with no new annotation. AI-silver is not evidence.
- **Ownership.** A owns the count-confound result, B the protocol, C retrieval ICL. This precheck uses no exemplars and makes no claim about any of them.
- **Files.** `scripts/h2_precheck/{flipbudget.py,job.sh}`, pinned in `SHA256SUMS` together with the pilot's `decode_pilot.py` and `score_pilot.py`.
