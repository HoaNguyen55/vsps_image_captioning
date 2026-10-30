# VSPS H1 pilot: tier-1 DEV-EXPLORE prereg (hybrid detector verifier on KTVIC TRAIN stage-1 records)

Status: DRAFT v2, 2026-10-31. v2 applies the fixes W1–W7 required by CC-198 (GO-with-fixes, 90%). The PI approved the H1
pilot proposal (PI-1030i, "Đồng ý đề xuất", LOG 2026-10-30 ~23:30 VN); this prereg itself is not yet approved.
Not committed. Phase A starts only after a scoped one-judge diff read of W1–W7 and a gatekeeper commit (W8).
Nothing in Phase A has run.
Label on every output: `TIER 1 / DEV-EXPLORE (VSPS-H1)`. Every estimate here is AI opinion, not evidence.
Phase A is **directional only**. The references are incomplete: KTVIC gold is caption-derived, so an object nobody mentioned
counts as wrong (rescap/chair.py docstring), which biases measured precision against H1. Detector labels are AI labels and
are not evidence about any image. No Phase A number is reported as VSPS absolute recall or precision; at most it appears as a
labelled replay ablation.

## 1. Question

H1 (manuscript/directions/VSPS_UPGRADE_DEEP_RESEARCH_2026-10-30.md): does a hybrid verifier recover the supervision recall
that the VSPS verifier drops without losing precision? The hybrid verifier has two parts:
- a two-detector existence vote (GroundingDINO + OWLv2);
- the existing model-free geometric channel (rescap/pipeline/verify.py `geometric_check`, flag A7). That channel has been
  idle because the stage-1 records carry no boxes.

Detector-verified existence is not new by itself (Woodpecker-style verification, RelCheck-style geometry). If the pilot has
any novelty, it lies in the Vietnamese prompt-mapped three-state vote inside VSPS.

## 2. Inputs (fixed)

| item | value |
|---|---|
| records | `data/stage1_records/stage1_records.tar.gz` sha256 `b312de68180a2f9bf31602bae917ed170b2630174c30c11e9ea59c64aff840b0`; 3,700 KTVIC **train** images, 192,216 propositions |
| images | `data/datasets/ktvic/images/<file_name>` for those 3,700 ids only. `detect_boxes.py` stops if an id is missing from `train_data.json` or present in `test_data.json` |
| prompt map | `scripts/vsps_h1/vi_en_map.json`, built by `build_map.py` (sha256 values in `scripts/vsps_h1/SHA256SUMS`) |
| detector config | `scripts/vsps_h1/config.json` |
| GroundingDINO | `IDEA-Research/grounding-dino-base` @ `12bdfa3120f3e7ec7b434d90674b3396eccf88eb`; box 0.35, text 0.25 |
| OWLv2 | `google/owlv2-base-patch16-ensemble` @ `cfd3195ba4ea9592eec887ded089f4c08eff231d`; box 0.10; query `a photo of a <prompt>` |
| other fixed values | top 5 boxes per prompt per detector; 8 prompts per GroundingDINO call |
| environment | python 3.12, torch 2.15.0, transformers 5.22.1, pillow 13.0.0 |
| verifier | **replayed** on CPU from the probe answers recorded in stage 1 (`rescap/vlm/replay.py`, as in `scripts/validate_replay.py`). No VLM is rerun, so the verifier costs 0 GPU-h |

**Line pins (W1).** Every detector line carries:
- `config_sha256` (config.json);
- `map_sha256` (vi_en_map.json);
- `device`.

On resume, `detect_boxes.py` skips an image only if its line matches all three for the current run. Any other line stops the
run. `vote.py` refuses any line whose sha differs from the files pinned in SHA256SUMS, and any boxes file that mixes devices.
Phase A writes a **fresh** boxes file; no smoke line is reused.

**Threshold change after the smoke.** One threshold changed after the 5-image plumbing smoke on train images: OWLv2 0.20 →
0.10. The 0.10 value is taken from the transformers OWLv2 example, an external anchor, not a search. At 0.20, OWLv2 found no
`man` in any of the 3 images where GroundingDINO found men. No other value was looked at. All values are now fixed.

**Consequence, disclosed.** At 0.10, OWLv2 is permissive. In the smoke run:
- OWLv2 found at least one box for 23 of 24 prompts and hit the 5-box cap for 15;
- GroundingDINO found a box for 19 of 24;
- over mapped entities, the positive rate was 0.97 for OWLv2 and 0.84 for GroundingDINO.

R2 is therefore registered openly as a **"GroundingDINO-led vote"**: SUPPORTED mostly means "GroundingDINO found it", and
REFUTED almost never fires. The precision guard is the funnel P (§5), not the two-detector design. M5 reports the positive
rate of each detector.

Detector lines store every OWLv2 box at or above 0.10 with its score, so the results at other thresholds can be recomputed.
Any such number is **post hoc**, is labelled as such, and cannot change GO/STOP. The OWLv2 query template is kept as it was
smoked, including for plural prompts (`trees`, `flags`).

**Smoke images.** Ids 2, 3, 4, 5 and 6 (5 of the 3,700) were used in the smoke run. They are inside the decision set, are
disclosed here, and are not excluded.

**Map (W5).** The map covers 1,217 head-noun types (28,912 entity mentions). 801 types are unmapped, which is **9.8 % of
mentions**; unmapped nouns get the detector vote UNCERTAIN. The table is a prompt dictionary, a method component, and labels
no image. It was drafted by an AI agent from the vocabulary, frequency first.

Coverage of the 113 CHAIR-vi lexicon nouns (`vi_en_map.json` → `lexicon_coverage`):

| measure | result |
|---|---|
| resolvable by the rules | 111 / 113 (not `vật`, `đồ`) |
| present as head-noun types in the 3,700 records, after `key_of` | 92 mapped, 2 unmapped (`vật` 34 mentions, `đồ` 231), 19 absent |

Cross-check against `data/coco_probe/coco80_vi.json` (`coco80_crosscheck`), both ways:
- of the 221 coco80_vi terms, 64 agree with the table, 19 differ, and 138 are resolved only by the coco80 rule;
- 30 lexicon nouns are coco80_vi terms, and 10 of them differ.

Every difference is the same deliberate choice. The open-vocabulary prompt names the noun itself:
- `man`, `woman`, `child`, `girl`, `baby` and `young man` replace COCO `person`; the gender ceiling still caps them;
- plain English replaces COCO class labels: table, phone, television, ball, water bottle, ship and computer.

The cross-check found one rule bug, now fixed in v2: a noun that begins with a number word (`ba lô`) was being read as a
quantifier. The unstripped form is now tried first. No record noun changes mapping because of this fix.

Ambiguous entries are kept as written and disclosed:

| entry | readings |
|---|---|
| `bóng` | ball / shadow / bulb |
| `quả` | fruit / any round thing |
| `xe` | any vehicle |
| `biển` | sea / sign; KTVIC often means a sign |
| `cam` | orange fruit / orange colour |

Human review of the map is **optional and non-blocking** (CC-198 ruling 4). If the PI edits the map before launch, the edit
is a pre-launch amendment. After launch the map is frozen.

## 3. Method (code: `scripts/vsps_h1/`)

1. `detect_boxes.py` runs both detectors once per image, with the image's mapped prompts, and writes one pinned jsonl line
   per image. `--out` must be outside the repo. Boxes are converted to `[x, y, w, h]` in absolute pixels in one place
   (`xyxy_to_xywh`).
2. `vote.py` gives each entity a vote:
   - both detectors find the prompt → SUPPORTED;
   - neither finds it → REFUTED;
   - only one finds it, or the noun is unmapped → UNCERTAIN.

   Only SUPPORTED entities get a box: the GroundingDINO box, distinct instances in score order. Entities that share a prompt
   take the next box; one left without a box keeps none.
3. Existence rule (`verify.detector_vote`, used only when `entity_votes` is passed):
   - a detector SUPPORTED lifts a verifier UNCERTAIN to SUPPORTED;
   - a detector SUPPORTED meeting a verifier REJECTED gives UNCERTAIN;
   - a detector REFUTED meeting a verifier SUPPORTED gives UNCERTAIN;
   - every other case keeps the verifier verdict.

   **Detectors alone never REJECT.** A REJECTED existence would cascade onto every dependent claim. Ceilings (gender,
   inference, depth) apply after the rule.
4. Absent box (`VerificationConfig.absent_bbox_is_evidence = False` in R1, R2 and R3): an entity without a consensus box gets
   the bbox signal ⊥, not 0.0.
5. Four replayed conditions run on the same 3,700 records:
   - **R0**: v1 rule, no boxes, no votes;
   - **R1**: boxes plus the geometric channel;
   - **R2**: R1 plus the vote. This is the H1 arm, the "GroundingDINO-led vote";
   - **R3** (falsifier, CC-198 ruling 6): R1 plus a SUPPORTED vote for every entity that R1 left UNCERTAIN, with no detector
     involved. Ceilings are the same.

   `scripts/recall_funnel.py` runs unchanged on each condition's records. The records go to the persistent out-of-repo
   folder `~/vsps_h1_runs/` and never to the repo.

**verify.py change.** 51 lines added, all default-off. With `entity_votes=None` and the default config, verdicts are
byte-identical to HEAD (checked on 300 records).

Selftest: `python3 scripts/vsps_h1/test_h1.py`. It covers:
- the map;
- box conversion;
- the vote;
- the line pins (W1);
- the R3 falsifier (W4);
- the verify hooks.

## 4. Outcome metrics (all against KTVIC **train** references, read in memory only)

- **M1, supervision recall.** `recall_funnel` R at the `supported` stage.
- **M2, reference precision of supported propositions.** `recall_funnel` P at the `supported` stage.
- **M3, entity reference precision.** Of the lexicon objects named by SUPPORTED `entity` propositions, the share the
  references name.
- **M4, spatial.** Over spatial propositions:
  - the share that leaves UNCERTAIN;
  - the share the bbox geometry decides.
- **M5, detectors.** Over mapped entities:
  - agreement: (both present + both absent) / mapped;
  - the positive rate of each detector.
- **M6, exact-replay robustness (W3).** R2 − R0 supported recall, restricted to the images whose R0 entity verdicts all
  equal the recorded ones. On the records there are 3,551 such images out of 3,700. The recall is computed in process and
  checked against `recall_funnel` on the full set first.

The `supported_selected` and `sft_caption` stages are **stale**, because selection and rendering are not rerun. They are not
outcomes.

**Baseline**, computed from the records only:
- R0 `supported` P 41.2, R 36.9;
- R0 `not_rejected` R 62.2.

The replayed verifier therefore loses 25.3 points. The "−18" in KE_HOACH_Q2 §0 came from the 10-09 `stage1_final` set.

**Replay fidelity** is 188,992 / 192,216 = 98.32 %, with 100 % probe hits. This is **below the harness's own 99 % bar**.
Drift by type:

| type | drift |
|---|---|
| entity | 1.40 % |
| spatial | 1.28 % |
| counting | 3.27 % |
| others | 1.1–1.7 % |

Entity propositions only (W3), recorded → replay (28,912 propositions):

| shift | count | effect on the pool the vote can lift |
|---|---|---|
| UNCERTAIN→SUPPORTED | 191 | shrinks it (bias against GO) |
| UNCERTAIN→REJECTED | 129 | shrinks it (bias against GO) |
| REJECTED→UNCERTAIN | 47 | enlarges it (bias for GO) |
| SUPPORTED→UNCERTAIN | 39 | enlarges it (bias for GO) |

The drift is **not arm-neutral**. The vote acts only on entities that the replay calls UNCERTAIN, so the drift changes the
pool the vote can lift. On entities the pool is a net 234 smaller than under the recorded verdicts, so the drift most likely
works against GO. M6 checks this rather than assuming it. The pilot does not track the drift down.

## 5. Decision rule (fixed now)

**GO** if both conditions hold on the full set:
- R2 − R0 supported-stage recall ≥ **+5.0 points**. This is PI-1030i's "recover ≥ 5 of the 18 points", taken as absolute
  points.
- R0 − R2 supported-stage precision ≤ **2.0 points**.

With the baseline above, that means R ≥ 41.9 and P ≥ 39.2. Otherwise the outcome is **STOP**: report it briefly as an
ablation (an R0–R3 table) and do not retune thresholds or the map on these records.

The decision is taken only when all 3,700 record ids have a valid, pinned line. Otherwise `vote.py` prints INCOMPLETE and no
verdict.

A GO goes to a **judge read before any Phase B prereg** if either condition below holds. Both are written into
`summary.json` → `decision.judge_read_required`.
- R2 − R3 supported precision < +2.0. The detectors would then add little beyond relaxing the gate.
- The M6 recall gain is < +5.0.

R1, R3 and M3 to M5 are descriptive. **A GO licenses only a Phase B prereg**, and Phase B must confirm on stage-1 records
**outside these 3,700**. These 3,700 are dev-explore records, and the threshold was set on 5 of them.

## 6. Exclusions and custody

- No KTVIC test image is opened.
- The 244-proposition human audit is not used, because those are test images.
- No OpenViIC or UIT-ViIC data is used.
- No new gold labels are made.
- Re-verified records, detector lines and summary.json stay in `~/vsps_h1_runs/`, outside the repo. The repo gets only the
  sha256 of summary.json, through a gatekeeper commit. The file itself is committed only if a caption-text scan finds 0.

## 7. Known limits, stated now

- **Depth relations.** They stay UNCERTAIN by design: `phía sau` and `phía trước` are 5,165 of the 26,795 spatial
  propositions. `geometric_check` has a box test for these relations:
  - `bên trái` / `bên phải`;
  - `trên` / `dưới` / `trên đầu`;
  - `trong` / `ngoài`;
  - `gần` / `xa` / `bên cạnh`;
  - `ở giữa`.

  A difference inside the margin still gives UNCERTAIN.
- **Same-noun pairs** get distinct boxes only if the detector returns several instances.
- **Gendered person prompts** (`man` / `woman`) are kept. The gender ceiling still caps them.
- **Prior on detector misses.** GroundingDINO misses objects often. K2 P2 measured recall 51.36 against gold 65.28 on COCO.
  Misses mostly cost lift, not precision.
- **Boxes can lower E.** Once an entity has a box, `region_area` and occlusion (1 − max IoU with any other box) enter E, and
  R0 computes neither. Co-referent entities (`người` with `phụ nữ`) and nested ones (shirt on a woman) overlap by design.
  In the smoke run, 30 verdicts changed between R0 and R1:
  - 24 carry the "too small" cause;
  - 1 carries the "occluded" cause;
  - 5 carry another cause.

  A STOP whose R1 already lost recall is attributed to this, and the attribution is reported.

## 8. Machine, cost, phases (CC-198 ruling 7)

- **Phase A** runs on the **laptop CPU**: nice 19, threads capped, one device for all 3,700. That is 0 GPU-h and about 45 h
  of wall time (44.2 s per image measured in the smoke run). A-T3 or C-T2 scoring on the laptop preempts it: pause with
  SIGSTOP, or kill it, since resume is built in.
- **Not started** until the W8 diff read and the gatekeeper commit. The PI may override with M1. In that case:
  - the cap is 4 GPU-h, and the 50-image projection rule applies;
  - only {image_id, file_name, entity id → category_vi} and the 3,700 train JPEGs are uploaded, to a folder outside C's
    dataset tree;
  - the run never overlaps C-T2 or A-T3;
  - the replay and the funnel stay on the laptop;
  - a run is all-CPU or all-GPU, never mixed.
- **Run command** (laptop, after W8):
  ```
  cd /mnt/d/vsps_image_captioning
  nice -n 19 env OMP_NUM_THREADS=3 HF_HUB_DISABLE_TELEMETRY=1 ~/.venvs/vsps_h1/bin/python scripts/vsps_h1/detect_boxes.py \
      --records ~/vsps_h1_runs/stage1 --images data/datasets/ktvic/images \
      --out ~/vsps_h1_runs/phaseA/boxes.jsonl --device cpu > ~/vsps_h1_runs/phaseA/detect.log 2>&1
  python3 scripts/vsps_h1/vote.py --records ~/vsps_h1_runs/stage1 --boxes ~/vsps_h1_runs/phaseA/boxes.jsonl \
      --out ~/vsps_h1_runs/phaseA/replay
  ```
  `~/vsps_h1_runs/stage1` is the record archive above, extracted as is. `phaseA/boxes.jsonl` must not exist before the
  first start.
- **Phase B** (rent a 4090) happens only on GO, after any judge read that §5 requires. It needs its own prereg on records
  outside these 3,700.
