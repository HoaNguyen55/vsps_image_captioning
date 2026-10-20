# Pre-registration: B-F1, Paper B's single final KTVIC test look (P1 + S1 seed-consensus MBR-3)

**Frozen:** 2026-10-20T15:43:08Z, before any B-F1 output exists (section 1). Repo HEAD at freeze: `ff17599d14fd83620188e9628e8abbb2c014eebd` (branch `paper-v10`).
**Machine-readable:** `manuscript/prereg/2026-10-20_b_f1_final_stack.json`; every number here is copied from it, and its `sources` block (with `frozen_files` and the quoted lines) gives each number's file and key or line.
**Authority:** PD-22 option (A), bindings 1-8 (`.session_backup/2026-10-13/decisions/PD-22.txt`, sha256 `d0b68ded647eb6a941b14ebfa327be2571b03f7c19729722565e6a5602030d64`); PD-9 Q4 (Paper B owns the stacked system) and Q5 (the seed-MBR proxy, L4, is a test look).
**Status:** frozen before any B-F1 output exists; REGISTERED only if this file is committed before any B-F1 decode output (D-W13-6; CHECKLIST C3: commit time < output mtime).

## 1. Registered before any output exists

- At 2026-10-20T15:43:08Z no B-F1 output exists: file names containing `b_f1`, `p1dev_s42-test`, `p1dev_s43-test`, `p1dev_s44-test`, `p1dev_mbr3-test` under `data/results`, `.session_backup/machines/O-2308423/root/outputs`, `.session_backup/machines/O-2308423/root/queue`, `.session_backup/machines/O-2308428/root/outputs`, `.session_backup/machines/O-2308428/root/queue`: 0 hits.
- No p1dev test decode exists: 296 paths contain `p1dev` (under `data`, `.session_backup/machines`, `manuscript`, `scripts`); 0 contain `test`; the evaluate.py results among them have split `dev_data.json` (15), `rl1000_data.json` (1), none `test_data.json`. Judge check (PD-22 line 12): "- Judge check: no p1dev test decode exists anywhere (106 p1dev files, all dev300)."

## 2. Members and decode (binding 1)

| member | adapter_model.safetensors sha256 | adapter_config.json sha256 |
|---|---|---|
| `p1dev_s42` | `227a3312a18cf69b355c20311ff1228167b2af1436e0cb443055dfdfcd40c5c3` | `93f042284aea64fcdf831590c592a7459849632dcb3ee4448b379177b7a298c5` |
| `p1dev_s43` | `d74d3dd4b4c620fdd18e0ab0f6fe4b0ed751dc0e008b5a49b79ea85612e613a7` | `93f042284aea64fcdf831590c592a7459849632dcb3ee4448b379177b7a298c5` |
| `p1dev_s44` | `b04354c86eede3bb6ba21842fdef876f6ae73d6d18b225b8f75b2a4b706b51d7` | `93f042284aea64fcdf831590c592a7459849632dcb3ee4448b379177b7a298c5` |

- Sources: p1dev_s42 from the S1 registration (`models.member_s42`), p1dev_s43 and p1dev_s44 from S1's `SHA256SUMS` (the S1 record). The mirrored copies match: True.
- Not members: the p1assist seeds, whose test captions were already seen (the L4 proxy, UPE, B-N2).
- Decoded fresh on KTVIC test (558 images) under the machine rule (one host decodes all three members in one job; the host has exactly one GPU with >= 24 GB; check records its machine_id and card, and all three provenances must carry that same machine_id and card; every other pin stays exact; CC-042), venv torch 2.5.1+cu121, transformers 4.51.3, peft 0.21.2; base `Qwen/Qwen2.5-VL-7B-Instruct` at `cc594898137f460bfe9f0759e9844b3ce807cfb5` (HF_HUB_OFFLINE=1; refs/main and the 5 shard sha256 checked).
- Settings: S1's greedy short-prompt decode (S1 procedure.decode): scripts/evaluate.py --model qwen2.5-vl-7b --adapter <member> --prompt short, bf16 (no --four-bit), greedy (do_sample=False), its defaults; evaluate.py defaults max-new-tokens 160, max-vision-tokens 512.
- Split: the 558 KTVIC test images (data/datasets/ktvic/test_data.json): evaluate.py gets --split <a copy of test_data.json holding its images list only>, so it writes predictions and scores nothing (its caption-free split path); NCS_DATASET unset, so images load from the KTVIC images folder. Every image is checked against `data/lb/sets/ktvic_test.tsv` (id, file name, sha256) before any decode.
- Outputs on the decode host: `/root/outputs/b_f1_ktvic_test`; names `p1dev_s42-test-short`, `p1dev_s43-test-short`, `p1dev_s44-test-short`; per decode `<name>.preds.json`, `<name>.preds.json.sha256`, `<name>.provenance.json`, `<name>.log (stdout and stderr of evaluate.py)`. Once only: a decode whose predictions exist is skipped; nothing is overwritten; nobody reads a prediction before score_b_f1.py run.

## 3. Variant and code (binding 2)

- MBR-3 (S1's carried variant): carried by the S1 dev300 gate (`gate.json` verdict PASS, carried mbr).
- Rule, unchanged: per image, the medoid of the three members' greedy captions: argmax over a of the sum over b != a of rl_reward.CiderD(c_a, [c_b]), document frequencies from the references of the 3469 train-minus-dev300 images and rl_reward.Segmenter word segmentation (UPE-MBR's selection side, so the selection reads no dev reference); ties go to the lower seed.
- Code: `scripts/seed_consensus.py` (sha256 `2b72dc417d60c5ec6a0be9cfd3b69692a783e2ba9bd1fc7dcb14c5195296c486`): `seed_consensus.medoid` with the selection lines of `seed_consensus.mbr`; no new MBR implementation; no change of utility, document frequencies (3469 train-minus-dev300 images), prompt or decode settings; short prompt only. No test reference enters the selection.

## 4. Self-check before any test statistic (binding 2)

- Reproduce the S1 gate from the S1 dev outputs (`.session_backup/machines/O-2308423/root/outputs/t3_2_s1_seed_consensus`, each file sha256-pinned): D_MBR 2.5498 [0.0035, 5.2374] and dCHAIR_i -0.193 (rounded to 4 and 3 decimals), and exactly the stored values (`gate.json` D_cider_x100_mean_lo_hi.mbr, dCHAIR_i_points.mbr), with S1's bootstrap (B = 2000, numpy default_rng(0)).
- Checks: per-image CIDEr-D of the S1 systems (members, soup, MBR) recomputed by rl_report.dev_scores (1e-6 assert) equal gate.json per_image_cider_x100 exactly; D_MBR and dCHAIR_i recomputed by seed_consensus.variant_deltas equal gate.json exactly and the quoted values at their decimals; the MBR selection run by the B-F1 code on the S1 dev decodes equals S1's picked_member list and the sha256 of S1's MBR prediction file; S1 is not void (s1_void_check.json void false) and T-3V marks S1 VERIFIED.
- On failure: stop: no test statistic is computed (K-SC).

## 5. Primary endpoint and verdict (binding 3)

- D_MBR = mean over the 558 test images of [CIDEr_i(MBR) - (1/3) * sum over the three members of CIDEr_i(member)], word-level CIDEr-D x100.
- Scoring: scripts/evaluate.py --predictions <file> --split test_data.json --prompt short (the protocol card: RDRSegmenter word level, CIDEr-D x100, rescap.metrics.CaptionMetrics), run once per system in a fresh process by score_b_f1.py run; per-image CIDEr-D from rl_report.dev_scores with the test references, which asserts that their mean equals evaluate.py's corpus value.
- F0: for each member and the MBR, the word-level row's segmenter is rdrsegmenter, the ids are exactly the 558 test ids, and |mean of per-image CIDEr-D - corpus CIDEr-D| < tolerance; any failure stops the work before D_MBR (K-F0) (tolerance 1e-6).
- CI: paired percentile bootstrap over test images, B = 5000, numpy default_rng(0), sorted-id order (ids sorted as strings), 95% (rl_reward.boot's two-sided 95% percentiles); rl_reward.boot(d, seed, B): default_rng(seed).integers(0, n, (B, n)); every CI of this registration uses these same draws (paired).
- Verdict `sign_gt_0` (B-N1 section 6, `verdict_rules.sign_gt_0`): PASS if ci95_lo > 0; FAIL if point <= 0; else INCONCLUSIVE.
- Prediction check, not the verdict: the S1 / R14-4 table (dCIDEr 1.0 to 3.0, dBLEU-4 0.5 to 1.0, dF1 -1.0 to 1.5, dCHAIR_i -1.0 to 0.5 points, |dmentions| <= 0.1) is reported as inside or outside for each point estimate.
- Absolute numbers: each system's absolute test CIDEr-D is reported descriptively, with the PD-22 risk note on the members' smaller training set; the claim is the paired delta.

## 6. Secondary endpoints (binding 4)

- K2: CHAIR_i is more than 1.0 pp above the member mean. (R14-4 line 127; PD-22: "K2: CHAIR_i more than 1.0 pp above the member mean is reported as harm.") Estimate: point estimate: CHAIR_i(MBR) - mean of the members' CHAIR_i, CHAIR-vi against the test references, x100.
- K3: a test F1 drop whose CI excludes 0 is reported as a negative. (R14-4 line 128) Estimate: dF1 = F1_ktvic5(MBR) - mean of the members' F1_ktvic5 (object_prf.scores, exact classes, gold from the test references), CI from the primary's draws; a drop is ci_hi < 0.
- Objects: no PD-2 count-matched object primary and no panel side are registered for KTVIC test (the OpenViIC panel is not read); object metrics are descriptive and enter no abstract sentence.
- Descriptive: BLEU-4 and mentions per caption against the predictions; object P / R / F1 (ktvic5) and CHAIR_i of every system and as deltas; absolute CIDEr-D of every system; the members' spread of test CIDEr-D; the share of images on which all three members agree; the MBR pick counts.
- The optional p1assist row: not run (optional in binding 1; it would recompute a look already made).

## 7. Test set (binding 5)

- Primary: all 558 images (`data/lb/sets/ktvic_test.tsv`).
- Clean 157 (`data/lb/splits/ktvic_test_openviic_train_clean.txt`): descriptive sensitivity only, no verdict (binding 5); D_MBR and its CI on these ids, same per-image values (document frequencies of all 558).
- The PD-19 leakage finding does not apply: every B-F1 member is trained on KTVIC train minus dev300 only (S1 prereg data.split), so no member saw OpenViIC train.

## 8. Test-look ledger and Stage-2 status (binding 6)

| id | earlier KTVIC-test computation on P1-family outputs | systems | files | used a p1dev member | informed the variant |
|---|---|---|---|---|---|
| L1 | P1-family KTVIC test scores (evaluate.py results on test_data.json) | p1-gold, p1_s43, p1_s43mbr, p1_s43selffuse, p1_s44, p1assist_s42, p1assist_s43, p1assist_s44, p1ep4_s42, p1mask_s42, tags_p1_s43 | 23 file(s) | no | no |
| L2 | UPE-MBR on KTVIC test (sample pools of p1assist_s42/s43/s44 and its statistics) | p1assist_s42, p1assist_s43, p1assist_s44 | 5 file(s) | no | no |
| L3 | PLAN-F1: its registered test step never ran (dev pilot parked on CPU, D12) | none | 1 file(s) | no | no |
| L4 | MBR over the three p1assist seeds' test captions minus their mean, syllable-level CIDEr-D; an exploratory test look (PD-9 Q5), never used to choose the variant | p1assist_s42, p1assist_s43, p1assist_s44 | 1 file(s) | no | no |
| L5 | B-N2 leaked/clean subset statistics on KTVIC test (run once from the committed scorer) | fuse2_s42, fuse2_s43, fuse2_s44, mr5assist_s42, p1-gold, p1_s43, p1_s44, p1assist_s42, p1assist_s43, p1assist_s44 | 1 file(s) | no | no |

- L4 value: +3.05 [+1.03, +5.11] (R14-4's proxy MBR used syllable-level CIDEr with test-reference document frequencies; the registered MBR uses word-level CIDEr-D with train-minus-dev300 document frequencies.).
- None used a p1dev member: True. None informed the choice of variant: True (the variant was chosen on dev300).
- Stage 2: S6 eligible, not run (PD-22, decided before any B-F1 output); S8 eligible, not run (PD-22, decided before any B-F1 output); if run, it is a separate UIT-ViIC item under PD-22 C1-C4 and never enters this stack; S4 not eligible (S3 outcome FAIL); S7 closed (D14; PD-9 Q3); XV-EF1 not carried. PD-22 (lines 44-49): "- Record the Stage-2 status: - S6 and S8 were eligible but not run, decided in PD-22 before any B-F1 output (reasons: cost, and R14-4's expected KTVIC effect of +/-1); - S4 is not eligible (S3 FAIL); - S7 is closed (D14); - XV-EF1 was not carried."

## 9. Procedure (binding 7) and closure (binding 8)

- 1. Commit this prereg pair through the gatekeeper.
- 2. Commit the instrument addendum (scorer and job sha256), the scorer, the job file and the gate and dry-run records; all before any test decode.
- 3. Queue the job once on one host under decode.machine.rule; it decodes the three members and writes sidecars and provenance; nobody reads a prediction before scoring.
- 4. Score once from the committed copy: score_b_f1.py run --gate <committed gate record> --outputs <mirror of the decode folder>.
- 5. An independent verifier re-runs it (CC-038b canonical form); commit through the gatekeeper.
- 6. No re-decode or re-score after any output has been read; a failure stops the work and comes back to the judge.
- Kill rules: K-SC: the self-check fails: stop before any test statistic; K-PROV: a decode fails admission (sha256 sidecar, SHA256SUMS, provenance: machine, job, evaluate.py, adapter, base revision, test data, commit carrying this registration, decoded after its commit): stop; K-COV: a member lacks a prediction for a test id: stop; K-F0: F0 fails for any system: stop; D_MBR is not computed; after_stop: the record states which rule fired; the work comes back to the judge.
- Closure: After B-F1, Paper B makes no further KTVIC-test look for any method; any later KTVIC-side item is dev300-only and exploratory.

## 10. Disclosures

- The +3.05 [+1.03, +5.11] proxy (L4) was seen before this registration; it is a test look (PD-9 Q5) and played no part in choosing the variant, which the S1 dev300 gate chose.
- PD-22 risks, quoted: - The one look is spent on a single-component stack. A stronger later lever cannot be confirmed on KTVIC. - The p1dev members are trained on 300 fewer images, so the absolute test CIDEr will sit a little below full-train P1. The claim is the paired delta; report the absolute number descriptively and with that note. - The dev lower bound is 0.0035, so the test verdict may be INCONCLUSIVE. Report it as it comes. 
- Decode-only: evaluate.py receives the images list of test_data.json without captions, so no test score exists before score_b_f1.py run; generation arguments are S1's.
- The MBR selection reads no test reference; its document frequencies come from the train-minus-dev300 references.
- No model-generated signal is used as gold; the scored references are KTVIC's human captions.
- S1's dev decodes ran on an RTX 3090; the B-F1 decode runs on a new rental under decode.machine.rule (CC-042). All three members are decoded on one host, so the paired delta is within one host; a card difference touches only the absolute numbers.

## 11. Deviations

- Any change after this freeze goes into a new dated file, committed through the gatekeeper before the affected output exists, and is reported next to every number it touches.

## 12. Frozen files

| path | sha256 | git | role |
|---|---|---|---|
| `.session_backup/2026-10-13/decisions/CC-042.txt` | `4401a68a90608ad885479d48875f280be7b2dde927e358319d8a92adc139524f` | not in git (git-excluded or untracked) | CC-042: the machine rule that replaces the fixed M1 pin |
| `.session_backup/2026-10-13/decisions/PD-22.txt` | `d0b68ded647eb6a941b14ebfa327be2571b03f7c19729722565e6a5602030d64` | not in git (git-excluded or untracked) | the ruling (bindings 1-8) |
| `.session_backup/2026-10-13/decisions/PD-9.txt` | `9d14a9573849a36bd98445c18e93e05f16e5c5ff43c27c4fd1470a5eaaf844f0` | not in git (git-excluded or untracked) | PD-9 Q4/Q5 (stacked system owned by Paper B; the seed-MBR proxy is a test look) |
| `.session_backup/machines/O-2308423/root/outputs/t3_2_s1_seed_consensus/SHA256SUMS` | `32195a8963da2a412b067f9313096a18941fd074971f698268679c2d0bf15527` | not in git (git-excluded or untracked) | S1 output checksums (the S1 record) |
| `.session_backup/machines/O-2308423/root/outputs/t3_2_s1_seed_consensus/gate.json` | `8998aff2003101bf668c5bfc2c2ea09c86afcf27b040cf6d1596c36e2bf6796c` | not in git (git-excluded or untracked) | S1 dev output read by the self-check |
| `.session_backup/machines/O-2308423/root/outputs/t3_2_s1_seed_consensus/p1dev_mbr3-dev300-short.json` | `0341fd5783174e06f4279c817982ca10ca6e935f0a89cc97f4a1ff8cee350c07` | not in git (git-excluded or untracked) | S1 dev output read by the self-check |
| `.session_backup/machines/O-2308423/root/outputs/t3_2_s1_seed_consensus/p1dev_mbr3-dev300-short.preds.json` | `474085418eed0ec83feaca963d26937995b09dc20f40e459a4fb276c0c6124d5` | not in git (git-excluded or untracked) | S1 dev output read by the self-check |
| `.session_backup/machines/O-2308423/root/outputs/t3_2_s1_seed_consensus/p1dev_mbr3_selection.json` | `fd02b1460b2b092bd2d6b39e45274857bdc6c016603ba5699e9d401055143168` | not in git (git-excluded or untracked) | S1 dev output read by the self-check |
| `.session_backup/machines/O-2308423/root/outputs/t3_2_s1_seed_consensus/p1dev_s42_redecode-dev300-short.json` | `18ba9da8b50794997d46852c7002034da26540e66310ae2c5ed53d0ae64ece76` | not in git (git-excluded or untracked) | S1 dev output read by the self-check |
| `.session_backup/machines/O-2308423/root/outputs/t3_2_s1_seed_consensus/p1dev_s43-dev300-short.json` | `9d9b2cb260ce8f8d1831ba4c9c27ce243a3f2c36246cfa71225422f3271e7fb3` | not in git (git-excluded or untracked) | S1 dev output read by the self-check |
| `.session_backup/machines/O-2308423/root/outputs/t3_2_s1_seed_consensus/p1dev_s44-dev300-short.json` | `5734b0f73064059acd52049da70e9d76be6470ee4f2b883c56be081808389681` | not in git (git-excluded or untracked) | S1 dev output read by the self-check |
| `.session_backup/machines/O-2308423/root/outputs/t3_2_s1_seed_consensus/p1dev_soup3_s42s43s44-dev300-short.json` | `a43ed5cb8fb89aeff834c68da786c5f0883d68267b8539525c950a5ada8c516a` | not in git (git-excluded or untracked) | S1 dev output read by the self-check |
| `.session_backup/machines/O-2308423/root/outputs/t3_2_s1_seed_consensus/s1_void_check.json` | `ae06e7ee2ceb6c68e757748cffd7d2b29da62c64b8d5933386fb8d7ef8541b72` | not in git (git-excluded or untracked) | S1 dev output read by the self-check |
| `.session_backup/machines/O-2308423/root/outputs/t3_3_s3_cm_dpo_rft/s3_verdict.json` | `0445997fccc76aed08e426bd2bf599feb6481fe6386a637d94214addb537b3e4` | not in git (git-excluded or untracked) | S3 outcome (S4 eligibility) |
| `data/datasets/ktvic/test_data.json` | `cc22ec6a8883773cb23c87ad5b64925f5a53c21982117274b53621f454e7ebbf` | not in git (git-excluded or untracked) | KTVIC references (git-excluded): test for scoring, train for the selection's document frequencies |
| `data/datasets/ktvic/train_data.json` | `72ee9b57c350fb5f215e1f04701c515a51e5e415240e51a77c8ce00ce6316a0f` | not in git (git-excluded or untracked) | KTVIC references (git-excluded): test for scoring, train for the selection's document frequencies |
| `data/lb/sets/ktvic_test.tsv` | `456243c0cfc82b0c3cc4ad52c694e11b4d9702f3ca14cd8103c3a82cd74a90eb` | 327191c | KTVIC test image manifest: id, file name, image sha256 (558 rows) |
| `data/lb/splits/ktvic_test_openviic_train_clean.txt` | `4832c16b4499a70b5b6d5c3967a22f551283b45b3a885ba011301b6a4e90015e` | 327191c | KTVIC test ids without an OpenViIC train copy (descriptive sensitivity) |
| `data/lb/splits/ktvic_test_openviic_train_leaked.txt` | `56e57ea468e48b692ed704ab4655f53cb878309bc3953cfb8dfd57b56590380f` | 327191c | KTVIC test ids with an OpenViIC train copy (complement of the clean list) |
| `data/results/b_n2/b_n2_run.json` | `59463c4c73e66349f047c5661823a6c49e1d37ac30b7d2728f42579ce68174ab` | 6f12bad | ledger source |
| `data/results/p1-gold-detailed.json` | `1055c4e05d5791ad1cde9ae07d43e228abbc3956eb99f22f0025b78f9c189c46` | 1f30d09 | earlier P1-family KTVIC test score (ledger) |
| `data/results/p1-gold-short.json` | `d333cdb0a7ef4109aaceecae0653cc90785ff00509b069ca388d042c9a5fe968` | 1f30d09 | earlier P1-family KTVIC test score (ledger) |
| `data/results/p1_s43-detailed.json` | `0d0034f3a95c998b85a11233706e57d16f295d9764b7680bbd236c12b2aa52b6` | 81c97c4 | earlier P1-family KTVIC test score (ledger) |
| `data/results/p1_s43-short.json` | `451fa02d522979c3ccbb75b1c183b876a796797b55db9c21729abf966ed7af21` | 81c97c4 | earlier P1-family KTVIC test score (ledger) |
| `data/results/p1_s43-two.json` | `52b07e685e27bc7d8164bf628f8b63dfd0674d93b36159f0c7dd2d51f5e9bb21` | e564ed6 | earlier P1-family KTVIC test score (ledger) |
| `data/results/p1_s43mbr-short.json` | `5eb84e2631510a76f2da268244d98f2a814c38399cc51564a59666eecd6215f2` | 63761c0 | earlier P1-family KTVIC test score (ledger) |
| `data/results/p1_s43selffuse-two.json` | `1e0453983fb3be027ad14dd45aada16b11c8d96bb2e21d5836353507f1d0274e` | 63761c0 | earlier P1-family KTVIC test score (ledger) |
| `data/results/p1_s44-detailed.json` | `0beaf55193e293bb50666542c149166017b36da478853e9a8e1dc76cacf75e80` | e564ed6 | earlier P1-family KTVIC test score (ledger) |
| `data/results/p1_s44-short.json` | `71a8c25c9d7cb1a10b835c1c2be1ea9e4f3e1e84d6900e009065cae21604346e` | e564ed6 | earlier P1-family KTVIC test score (ledger) |
| `data/results/p1assist_s42-detailed.json` | `87dd4fa70dda94ae8abe37280f1d638eb1c7a31fb8ed1e99c730f3982514763b` | 423ea81 | earlier P1-family KTVIC test score (ledger) |
| `data/results/p1assist_s42-short.json` | `ea38b60e7dc5c243356b98b8ac19b91165cb93ecb6f8a6f2badcbeb7053dbfa9` | 423ea81 | earlier P1-family KTVIC test score (ledger) |
| `data/results/p1assist_s43-detailed.json` | `06e314bfe0ebe23a5e115c866c38db532a047ef7eafb4aed60429c9687a77153` | eafe7ba | earlier P1-family KTVIC test score (ledger) |
| `data/results/p1assist_s43-short.json` | `ce8576a440d55888c2954070cef7c916f8030de94f5e171d9e6a02aef79137eb` | eafe7ba | earlier P1-family KTVIC test score (ledger) |
| `data/results/p1assist_s44-detailed.json` | `550d2613591286e5bf4608177de77e326ad92581fa10e8cbdbda5aa3bf1d82e6` | 9d81fe5 | earlier P1-family KTVIC test score (ledger) |
| `data/results/p1assist_s44-short.json` | `723d97653f895e98306a4dbbbf85a1dcd1d6df9012422711bfd85f98b2cca2ad` | 9d81fe5 | earlier P1-family KTVIC test score (ledger) |
| `data/results/p1ep4_s42-detailed.json` | `5f896014a3f7e344522550fb1f4a6005b07965e9d5256029e9bf7f5703acb470` | fece3c7 | earlier P1-family KTVIC test score (ledger) |
| `data/results/p1ep4_s42-short.json` | `de233a37ed8fd841d1a1ab65a5a5a3ebbbce08bdee743f2932dd1fa8eee3b75a` | fece3c7 | earlier P1-family KTVIC test score (ledger) |
| `data/results/p1ep4_s42-two.json` | `2ed5bad78fc8eae9a5c965004a74c4f35d0bea6b4ea9cac64d2d7093b3dc54c2` | fece3c7 | earlier P1-family KTVIC test score (ledger) |
| `data/results/p1mask_s42-detailed.json` | `bd63b9af1bc34b13453998d9f0d41bed3c9e9ec8bbeb75ed61a68ab9b55e6b41` | d576a2a | earlier P1-family KTVIC test score (ledger) |
| `data/results/p1mask_s42-short.json` | `00c9655f4aaa5b09cb0cafb4fcd051c16c6223d5bba5655233bea104afc04851` | d576a2a | earlier P1-family KTVIC test score (ledger) |
| `data/results/p1mask_s42-two.json` | `2e9fd7991e29165366e01ffe1bd3beec2289a3b84251f4026eb3088224527ec9` | d576a2a | earlier P1-family KTVIC test score (ledger) |
| `data/results/tags_p1_s43-detailed.json` | `67ed5270722e148436b968b5933302caa9f52a4ce8b7744873fef1aa37db36f7` | e564ed6 | earlier P1-family KTVIC test score (ledger) |
| `data/results/tags_p1_s43-short.json` | `081ac7544ef13ee39ec7c105e1cea557a79d51934714872c378c745c18c2adca` | e564ed6 | earlier P1-family KTVIC test score (ledger) |
| `data/results/upe/test/p1assist_s42-test-short-T0.5.jsonl` | `87341261a3d541506ff3758373cf983475b26fe711f62b0c807261b4d82a2021` | ba351f8 | UPE-MBR KTVIC test pool and statistics (ledger) |
| `data/results/upe/test/p1assist_s43-test-short-T0.5.jsonl` | `9c2b917b4d771d1d25a2ef5b436363cc36908f269248c80226dcefbe557f2708` | ba351f8 | UPE-MBR KTVIC test pool and statistics (ledger) |
| `data/results/upe/test/p1assist_s44-test-short-T0.5.jsonl` | `14dee7feca45f8e2e38041a83e69f4128e5b1281ce82874f6f931c47079c0bdd` | ba351f8 | UPE-MBR KTVIC test pool and statistics (ledger) |
| `data/results/upe/test/upe_mbr_ktvic_test.json` | `b75a1304a13406f1db6b7f5cd2bc5c80d6743f8ebbead4fda7b673e2b75fb99a` | ba351f8 | UPE-MBR KTVIC test pool and statistics (ledger) |
| `data/results/upe/test/upe_mbr_ktvic_test.log` | `b8863b7c1df10fdf51caaf7c2d4d29d517a7e3da4d2bef02b8d3e34db6dffdeb` | ba351f8 | UPE-MBR KTVIC test pool and statistics (ledger) |
| `data/splits/ktvic_dev300.txt` | `cee024f8bb76846b1623e36d1861caccc4d13874db87544213a1f18f3de6898c` | b44db13 | S1 split list |
| `data/splits/ktvic_train_minus_dev300.txt` | `006080b455a553ca9cc5d3f514ad76bfbe67f444c9c145a5696de681a4be1a58` | b44db13 | S1 split list |
| `manuscript/prereg/2026-10-13_plan_f1.md` | `e5550673f17c9962d4f7f99d9f6c980ddf647f11c786c107a883a0103cc7a722` | ee583c7 | ledger source |
| `manuscript/prereg/2026-10-13_upe_mbr.md` | `f4d2a5424a25c478d7d3c13817efe5193c93a9be849cd78602effbf83b041688` | 257bc8c | ledger source |
| `manuscript/prereg/2026-10-18_tier3_S1.json` | `e485da949cce2ee97fbc569c0b977549e0f55c56a91ca43d8356b87f15686bd2` | a68fb66 | S1 registration (members, base, venv, MBR rule, analysis, predictions, ledger) |
| `manuscript/prereg/2026-10-18_tier3_S1.md` | `4b1e7c6dd17f2d7e6b4f2bb389ddd7df9edd66609fc7243f4c8f0c376ec3c0a4` | a68fb66 | S1 registration (text) |
| `manuscript/prereg/2026-10-18_tier3_S1_instrument.json` | `904f2eb14249de28e7fdc5edf911347db4fe1169f5e860f40f7ee900cd873b87` | 7382600 | S1 instrument addendum (pins scripts/seed_consensus.py) |
| `manuscript/prereg/2026-10-18_tier3_S1_operations.md` | `c77e05a57c70c8442665b3b5214411c3dcaaa22d69be7468ba433c6bf6f79bcf` | f6b1656 | S1 operating notes (void rule) |
| `manuscript/prereg/2026-10-19_b_n1_vi_leaderboard.json` | `9ff02dc259258de1add426abd02131f2122e3476a81f9a076066ed6d74906134` | 327191c | B-N1 registration: verdict rule sign_gt_0 (section 6) |
| `manuscript/prereg/2026-10-19_b_n2_leakage_did_prereg_v2.json` | `675d37a9da2b26a0472ff0fd58a370dd55705602c78006bc1a52d96245d15972` | 9f7e6bf | B-N2 registration: systems of the subset statistics (ledger) |
| `manuscript/research_r14/R14_4/REPORT.md` | `acfe227a74e530788142e3da98043a99579067d257f1c2045e9a17bc22659504` | 5a6e8ac | R14-4 report: K2/K3 and the test predictions (section 3 A) |
| `manuscript/research_r14/R14_4/soup_proxy.out` | `0a2aef243cf2d2d7ee532b30e4b7916811c47a0a947388813be3594249ab8345` | 5a6e8ac | ledger source |
| `manuscript/verification/paperA/T3V_S1_S3_S5.json` | `112fd94227b4714ba0a979a628ba7b8ee3bb0db39c38e2009f072a8dbeb49bd3` | not in git (git-excluded or untracked) | T-3V verification of S1 |
| `rescap/chair.py` | `e47d249ac7290070f2387d3fa8b22dac77728265ad276f55aa6520f5cbc591a3` | a0accb5 | code read by the B-F1 scorer or job |
| `rescap/metrics.py` | `e0296ec528b87f4d1b31165cbb45deee5453783fd7dad783f248869e596bf960` | 4e646da | code read by the B-F1 scorer or job |
| `rescap/svp/matching.py` | `a9253060131aacfca8eaab9a4b2c473c487db96a7c1222f0b8e31f9f61b24003` | 1f30d09 | code read by the B-F1 scorer or job |
| `rescap/vi/lexicon.py` | `fbc945f2247418275144ac75b893f7c51f8951b9ea42018680d433775dd79eb9` | 996c32f | code read by the B-F1 scorer or job |
| `scripts/checkpoint_resume_hook.py` | `05466ef5ed3bef2b732ccd01f530a8c977c4c822ef8619b0238f562fb11e5895` | d89094e | code read by the B-F1 scorer or job |
| `scripts/evaluate.py` | `a68d56826d90d8a409493cd6f49007e906c6cb4f5668314edb9b8e7a632e8236` | d4de7b0 | code read by the B-F1 scorer or job |
| `scripts/object_prf.py` | `6b711280d70b780d596414896d832738da58f1b079015dee888605d1ba350adc` | 20ea9d4 | code read by the B-F1 scorer or job |
| `scripts/queue/adapters_canonical.sha256` | `031b7cc782c546f9746394370bb77a649de72aaaf9cc6b906bfc2ca6cd8c726d` | cb03bba | canonical adapter checksums (p1dev_s42) |
| `scripts/queue/check_g1_pass.py` | `39fe181f38bd57a7de32111745bc91de6d684f89c1a931b805da80fe85e104bc` | d89094e | code read by the B-F1 scorer or job |
| `scripts/queue/jobs/t3_2_s1_seed_consensus.sh` | `3acd86835c728bf432f622c7bafc03a177e54047b3206570b23514c7a2080ffb` | 7382600 | S1 job file (model for the B-F1 job) |
| `scripts/rl_report.py` | `f92faa61965348fc5296f7e97399a82086a125c1b936b9dfb4494cda266997c5` | 3ec03bf | code read by the B-F1 scorer or job |
| `scripts/rl_reward.py` | `3b18b7a3620c2511d4d13caea62f204534783e3024cac188da78d957e6a0a74b` | 3ec03bf | code read by the B-F1 scorer or job |
| `scripts/seed_consensus.py` | `2b72dc417d60c5ec6a0be9cfd3b69692a783e2ba9bd1fc7dcb14c5195296c486` | 7382600 | code read by the B-F1 scorer or job |
