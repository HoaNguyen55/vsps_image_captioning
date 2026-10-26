# Post-hoc registration: Paper B, (a) a full-train MBR-3 row over P1-R's existing KTVIC-test captions; (b) the p1-gold s42 retrain (not triggered)

**Written:** 2026-10-26T04:15Z. No computation of (a) or (b) has been run. The only operations on the member files listed in §A.2 were sha256 hashes. No member caption was read, and no test statistic of the MBR-3 selection exists.
**Status:** DRAFT, amended 2026-10-26 under CP-112 W1-W4 and CP-112a W1-W5 (the earlier sha256 values 9443aa16… and cfe044dd… are void). It becomes the registration of (a) only if it is committed through the gatekeeper before any output of (a) exists (commit time < output mtime, CHECKLIST C3). Even then, (a) carries the label **POST_HOC** (Supplement S1 labels): §A.1 lists the earlier looks at the same members.
**Authority:** PI-1026e (`.session_backup/2026-10-13/decisions/LOG.md` l.456, 2026-10-26T03:57:14Z, chat ~11:00 VN).
- It answers CC-109 Q2 and Q3 (`.session_backup/2026-10-13/decisions/CC-109.txt`).
- Q2 lifts the B-F1 §9 closure for ONE post hoc full-train MBR-3 row over P1-R's existing KTVIC-test captions, with three conditions: a prereg first, a post hoc label, and the B-F1 verdict staying FAIL.
- Q3 orders a retrain of p1-gold s42 on all 3,769 images *if* it proves to be 3,700-trained.
- CC-109's panel recommended NO on Q2 (J1 80, J2 85, J3 85). The PI overruled that on 2026-10-26, and this file records the overrule as the PI's decision.

## A. The MBR-3 row over P1-R (post hoc, no verdict)

### A.1 What was already seen (why the label is POST_HOC)

| ledger | look at the same members | value | source |
|---|---|---|---|
| L1 | P1-R per-seed KTVIC test CIDEr-D (s42, s43, s44) | 148.66, 148.06, 147.96 | `data/results/p1assist_s4{2,3,4}-short.json` |
| L2 | UPE-MBR on P1-R's test sample pools | KILL (S6.2) | `data/results/upe/test/upe_mbr_ktvic_test.json` |
| L4 | MBR over the three P1-R seeds' test captions minus their mean (syllable-level CIDEr, test-reference document frequencies; exploratory test look, PD-9 Q5) | +3.05 [+1.03, +5.11] | B-F1 prereg §8 l.71, l.74; `manuscript/research_r14/R14_4/soup_proxy.out` |
| L5 | B-N2 leaked/clean subset statistics | descriptive | `data/results/b_n2/b_n2_run.json` |
| B-F1 | registered MBR-3 over p1dev s42-44 (3,469-trained) | D_MBR −0.391 [−2.437, +1.666], FAIL | `data/results/b_f1/b_f1_run.json` (sha256 998e4f33…) |

- B-F1 §6 (`manuscript/prereg/2026-10-20_b_f1_final_stack.md` l.56) declined this exact row: "The optional p1assist row: not run (optional in binding 1; it would recompute a look already made)."
- This file is written after L4 and after B-F1's result were seen. The row therefore tests nothing and is descriptive. It is added to the B-F1 ledger as **L6**.

### A.2 Members (fixed files; no decode)

| member | test-caption file | sha256 | committed in | decoded on | adapter_model.safetensors sha256 |
|---|---|---|---|---|---|
| P1-R s42 (`p1assist_s42`) | `data/results/p1assist_s42-short.preds.json` | `ca5ce25366b04def1ca1099344a0e4a610bf767e357140525e4290913ffe2fef` | 423ea81 | n2 (job 34) | `4efbb4e4bc6bf255369e3166f255cd8fe70ffe754eeefa8ff9e34a162d475a36` |
| P1-R s43 (`p1assist_s43`) | `data/results/p1assist_s43-short.preds.json` | `13343482926cade1e3640185e3c5bd7cd504df5f2a2099ffb614d7a9bcb51861` | eafe7ba | n3 | `cbad831b31c0a18920e9eb4d903054acfdcb97bd00c6ca25742246bf34c75634` |
| P1-R s44 (`p1assist_s44`) | `data/results/p1assist_s44-short.preds.json` | `9344cb3504f3b925156ee59952735e946a97de29b682583d217de4198060f248` | 9d81fe5 | n3 | `d8cd93348de3640326a3ed9f276775cb6cc140a7cda6e59a33fec830a5107903` |

- The adapter shas come from `scripts/queue/adapters_canonical.sha256` l.15-17 (cb03bba) and equal the mirrored copies.
- All three members trained on all 3,769 KTVIC train images (dev300 included). The evidence is the training log for s42 (`.session_backup/machines/n2/queue/34_p1_assist_s42.log` l.10: "training set: 3769 examples, loss mask: assistant") and 942 optimizer steps for each seed (metrics.jsonl), i.e. 2 epochs × ⌊3,769 / 8⌋.
- Decode settings, per member:
  - s42: `.session_backup/machines/n2/queue/done/34_p1_assist_s42.sh` l.7 calls `scripts/evaluate.py --model qwen2.5-vl-7b --adapter … --split test_data.json --prompt short` with no other generation flag (the job line also sets --name and loops over short/detailed under timeout), so evaluate.py's defaults apply (bf16, greedy, max-new-tokens 160, 512 vision tokens).
  - s43, s44: the same short prompt (result metadata, `data/results/p1assist_s4{3,4}-short.json` :: prompt_style, prompt). No n3 job file or decode log survives locally, so the other generation arguments are not recorded.
- **Disclosed differences from B-F1's decode.** s42 was decoded on n2 and s43/s44 on n3, before CC-042's single-host rule existed and with the evaluate.py commit of 2026-10-12/13. B-F1 decoded all members on one host.
  - The paired delta of this row therefore mixes two hosts.
  - The members are fixed files, so nothing is re-decoded.
- Nothing is decoded and no GPU is used.

### A.3 Selection (unchanged from B-F1 §3)

- Rule: per image, the medoid of the three members' greedy captions, i.e. the argmax over a of the sum over b ≠ a of `rl_reward.CiderD(c_a, [c_b])`. Ties go to the lower seed.
- Code: `scripts/seed_consensus.py` (sha256 `2b72dc417d60c5ec6a0be9cfd3b69692a783e2ba9bd1fc7dcb14c5195296c486`), `seed_consensus.medoid` with the selection lines of `seed_consensus.mbr`. The code is called through `scripts/b_f1/score_b_f1.py`'s `selector` (sha256 `9c57cc9771d6da84f56534004ebd60c72acd1103ca7c63a741c2f482881304aa`).
- Document frequencies are **unchanged** from B-F1: the references of the 3,469 train-minus-dev300 images (`data/splits/ktvic_train_minus_dev300.txt`, sha256 `006080b455a553ca9cc5d3f514ad76bfbe67f444c9c145a5696de681a4be1a58`; `data/datasets/ktvic/train_data.json`, sha256 `72ee9b57c350fb5f215e1f04701c515a51e5e415240e51a77c8ce00ce6316a0f`). Segmentation is `rl_reward.Segmenter`.
  - The members are the only thing that differs from B-F1.
  - Switching the document frequencies to all 3,769 images would be a deviation and is not done.
- No test reference enters the selection.

### A.4 Scoring (B's frozen protocol, as B-F1 §5-7)

- Systems: the MBR-3 selection and each of the three members.
  - Each is scored once by `scripts/evaluate.py --predictions <file> --split test_data.json --prompt short` in a fresh process (sha256 `a68d56826d90d8a409493cd6f49007e906c6cb4f5668314edb9b8e7a632e8236`).
  - The protocol card is P0: RDRSegmenter VnCoreNLP 1.2, word level, CIDEr-D ×100, `rescap.metrics.CaptionMetrics`.
  - The references are `data/datasets/ktvic/test_data.json` (sha256 `cc22ec6a8883773cb23c87ad5b64925f5a53c21982117274b53621f454e7ebbf`), all 558 images.
- Per-image CIDEr-D comes from `rl_report.dev_scores` (sha256 `f92faa61965348fc5296f7e97399a82086a125c1b936b9dfb4494cda266997c5`). It asserts that the per-image mean equals evaluate.py's corpus value.
- F0: B-F1's check. For every system the segmenter must be rdrsegmenter, the ids exactly the 558 test ids, and |per-image mean − corpus| < 1e-6.
- Endpoint: D_MBR = mean over the 558 images of [CIDEr_i(MBR) − (1/3) Σ_members CIDEr_i(member)].
- CI: paired percentile bootstrap over images, B = 5,000, `numpy default_rng(0)`, ids sorted as strings, 95% (`rl_reward.boot`, sha256 `3b18b7a3620c2511d4d13caea62f204534783e3024cac188da78d957e6a0a74b`).
- Descriptive only:
  - absolute CIDEr-D of the MBR-3 selection and of the member mean;
  - ΔCHAIR_i and ΔF1 (ktvic5), computed as in B-F1's K2/K3 but with no kill;
  - ΔBLEU-4;
  - pick counts;
  - D_MBR on the clean 157 ids (`data/lb/splits/ktvic_test_openviic_train_clean.txt`).
- **No verdict.** `sign_gt_0` is not applied, and no PASS, FAIL or INCONCLUSIVE label is attached to this row. The B-F1 verdict stays **FAIL**.
- **Instrument.** A thin runner calls `score_b_f1.py`'s `look` (which runs `selector`, `evaluate_py`, `f0` and `statistics`), with the code of those functions unchanged. B-F1's `run` mode refuses any decode it did not admit, so it cannot be reused directly. Because `look` alone skips the checks that `run` makes, the runner adds the gates G1-G8 below. They are part of this registration, not of the addendum.
  - The runner passes the three files of §A.2 as the members under the keys `s42`, `s43` and `s44`.
  - `P` is B-F1's registered prereg JSON, unchanged. `cfg` keeps B-F1's values (B, seed, level, tol, k2); only the output names and paths are new.
  - `statistics` also writes `primary.verdict`, `K2.fires`, `K2.reported_as`, `K3.fires`, `K3.reported_as`, `prediction_check`, `objects.claims_allowed` and `objects.status` (`score_b_f1.py` l.431, l.433, l.435 for the `reported_as` and `status` labels). The runner drops these fields from the record, and they are never reported (no verdict, no kill, no claim label, no prediction check).
  - The runner is written after this file is committed.
  - It is dry-run on synthetic references, then committed through the gatekeeper with its sha256 in an addendum to this directory, all before it reads a member file.
  - The addendum supplies only the member mapping, the output names and the paths, and it may not change anything else in §A.2-A.5.
- **Runner gates (G1-G8).** Each failure stops the work before any test statistic, with no re-run, and the work goes back to the judge.
  - G1, gate and self-check equality: the runner calls B-F1's `pin_all`, then `gate_body` (which runs `self_check`). It requires `all_pass` and requires `pins`, `instrument` and `self_check` to equal those of the committed B-F1 gate record `manuscript/prereg/2026-10-20_b_f1_record/b_f1_gate.json` (sha256 `cf64ee1c4caa2f483141e9d8b202d25af23e93c523e490a74a63d082a79b8dc2`, 877f7db), exactly as `run` does (`score_b_f1.py` l.484-486). This reads only S1 dev outputs, so no B-F1 test output is re-scored.
  - G2, pinned split: `rest` from `sc.split_ids(sc.load_prereg())` must equal, as a set and in count (3,469), the ids of the pinned `data/splits/ktvic_train_minus_dev300.txt` (sha256 `006080b4…`).
  - G3, K-COV before selection: each member file's keys must equal the 558 test ids exactly, and this is checked before `selector` runs.
  - G4, K-L1: each member's re-scored corpus CIDEr-D (word level, ×100, the evaluate.py result inside `look`) must equal the committed L1 values within 1e-6: s42 148.66403869141925, s43 148.06296896003204, s44 147.96149059506558 (`data/results/p1assist_s4{2,3,4}-short.json` :: results[0].scores_scaled_x100.CIDEr; sha256 `ea38b60e…`, `ce8576a4…`, `723d9765…`). evaluate.py has been unchanged since d4de7b0. The check sits inside `look`'s member loop, as a guard around the module-level `evaluate_py`/`f0` with their function bodies unchanged. It runs after the three members are scored and before the MBR file is scored and `statistics()` runs. Each member is scored once. On a mismatch the runner stops before D_MBR, nothing is written or printed, and nothing is re-run.
  - G5, no verdict fields: the runner never calls `score_b_f1.py`'s `main()`. It deletes `primary.verdict`, `K2.fires`, `K2.reported_as`, `K3.fires`, `K3.reported_as`, `prediction_check`, `objects.claims_allowed` and `objects.status` before anything is written or printed. The three labels `K2.reported_as`, `K3.reported_as` and `objects.status` (`score_b_f1.py` l.431, l.433, l.435) are added to CP-112 W3(e)'s list by an explicit amendment (CP-112a ruling 1).
  - G6, no caption text: the runner prints no caption. The MBR prediction file stays in a temporary directory outside the repository, and only its sha256 is recorded.
  - G7, once only: the runner refuses to start if its output record already exists.
  - G8, text pre-commitment: whatever the value, no abstract or conclusion sentence of Paper B changes, and sec5.1 gets at most one claim-free post hoc sentence (§A.6).
- No positive control (a re-computation of B-F1's published result from the p1dev decodes) is run. B-F1 §9 step 6 (l.85) bars re-scoring after an output has been read, and the PI's lift covers only this row (CP-112 ruling 6).
- Machine: local CPU. No GPU, no M3 and no M4. No test image is loaded.

### A.5 Kill rules, once-only, closure

- K-PIN: any member file, scorer file or reference file whose sha256 differs from §A.2-A.4 stops the work before selection.
- K-COV (G3): a member whose keys are not exactly the 558 test ids stops the work before selection.
- K-L1 (G4): a member whose re-scored CIDEr-D differs from its committed L1 value by 1e-6 or more stops the work inside `look`'s member loop, before the MBR file is scored and before D_MBR. Nothing is written, printed or re-run.
- K-SC (G1, G2): gate, self-check or split inequality stops the work before any test file is read.
- K-F0: F0 fails for any system, so D_MBR is not computed.
- After any kill the record states which rule fired, and the work goes back to the judge.
- The row runs once. Nothing is re-selected or re-scored after any output has been read.
- An independent verifier re-runs it (CC-038b canonical form).
- After this row, the B-F1 §9 closure is back in force: Paper B makes no further KTVIC-test look for any method.

### A.6 Reporting

- Supplement S7 gets one row beside B-F1 and L4: "post hoc, PI decision 2026-10-26 lifting the §9 closure for this row only; written after L4 and B-F1 were seen; members trained on all 3,769 images; decoded on two hosts".
  - It gives D_MBR [95% CI] and the absolute CIDEr-D of the MBR selection and of the member mean.
  - B-F1's registered FAIL (−0.39 [−2.44, +1.67]) and L4 (+3.05 [+1.03, +5.11], a different utility and scorer) sit next to it.
- sec5.1 gets at most one sentence, labelled post hoc, with no claim. The main-text system stays P1-R.
- Every number gets a number_manifest_B row with its source key.

## B. p1-gold s42 retrain on 3,769: NOT TRIGGERED

- **Trigger (PI-1026e Q3):** "if FAIR's P1 s42 (149.79) proves 3,700-trained". The evidence (CPU check, `.session_backup/2026-10-26/b_cp109/CHANGES.md` §W5) does not establish 3,700:
  - No run record of p1-gold survives: no training log, no build report, no metrics.jsonl and no adapter.
  - Its scores were committed on 2026-08-30 in 1f30d09. The `gold_p1` build reports showing 3,769 on n2 and n3 date from 2026-10-11 and belong to the later runs (p1_s43/s44, p1mask, P1-R), not to p1-gold.
  - The only P1 build path at 1f30d09 (`scripts/build_gold_sft.py`) writes one row for every captioned image of the annotations file it is given and has no image filter. `--images-file` arrived later, in 56e50a1 (2026-10-12). The only cut, `--limit`, is documented as "for quick trials only", and `--limit 3700` would not give FAIR's 3,700-image set (checked against `data/stage1_records` and `data/screening/val_manifest.json`).
  - `train_stage2.py` at 1f30d09 has no image filter either.
  - FAIR v10 §IV-A states that 3,700 training images were used "for supervision construction and SFT" and that the 69 held-out images had "no SFT". §IV-D says that P1 "applies the same SFT recipe to KTVIC gold captions". Read together, these point to 3,700.
  - The builder in the code committed with its scores (1f30d09, 2026-08-30) has no image filter and points to 3,769. The run predates that commit, and no run record decides between the two. The count is not established either way.
- **Status:** not triggered. No retrain prereg is registered here.
- **The retrain is redundant.** The run Q3 describes already exists. p1mask_s42 is seed 42, legacy mask, all 3,769 training images (`.session_backup/machines/n2/queue/33_p1_maskfix_s42.log` l.10), with set_seed before LoRA init (commit d576a2a). It scores 147.67 CIDEr-D on KTVIC test (`data/results/p1mask_s42-short.json` :: results[0].scores_scaled_x100.CIDEr = 147.67041072387474, sha256 `00c9655f…`; B-F1 ledger L1). It is quoted beside 149.79 as an existing result, neither re-scored nor a new look. 149.79 predates the set_seed fix, so a retrain could not reproduce it, and a retrain would also need a second KTVIC-test decode outside the one-row lift (CP-112 ruling 3).
- If later evidence shows 3,700 (for example a recovered step count of 924 = 2 × ⌊3,700 / 8⌋ against 942 for 3,769), a separate prereg is written and committed before any computation.
  - Recipe: 1f30d09's `build_gold_sft.py` and `train_stage2.py --stage sft --epochs 2 --seed 42`, legacy mask, hyperparameters frozen as in sec4.1, all 3,769 train images.
  - Machines: training on M4 (≈1.9 GPU-h); the KTVIC-test decode on M3 only (≈0.3 GPU-h), after C's blocks and A's W4.
  - Caps, gates (adapter sha256 recorded, a parity slice) and post hoc reporting beside 149.79.

## C. Frozen-file checks

`SHA256SUMS` in this directory lists this file. The input shas are quoted inline above and are re-checked by K-PIN.
