# VSPS-J E2b tier-1 AMENDMENT 1 (post-rate): rate results, the 1b-i cell set, block caps, W25 for ledger line 2, CC-218 closure

Status: DRAFT v1.2 for CC-223 round 3/3 (last round; full panel at 90). Tier REVERSIBLE (dev-explore), bar >= 90.
v1 = 668626ad (written 2026-11-02T00:42:05Z, revised 00:55:57Z); v1.1 = 030dcfb3 (finished 2026-11-02T03:58:33Z);
v1.2 written 2026-11-02T04:23:57Z (all stamps from `date -u`).
v1.1 = v1 plus CC-223 BLOCKING B1-B4, the folded NON-BLOCKING N1-N15 wording, the coordinator-verified K8 fact (and the
same treatment for the other pinned laptop caches K6, K7, K9), and the corrections listed in section I.
v1.2 = v1.1 plus CC-223r2 W1 (B3(a) scope), NB-1 to NB-6, the PI answers of PI-1102e, and the KV-row narrowing that
follows from the ids-only KV-5,000 measurement (section J).
Nothing is committed, launched or logged by this file.
Label: `TIER 1 / DEV-EXPLORE (VSPS-J E2b)`. Every estimate is AI opinion.
**Licence scope.** If approved, this amendment licenses tier-1b-i (M-HalDetect val, vi frames, then the EN frame for
the winner) only after these launch gates hold (CC-223 Ruling 7):
1. this amendment's judge read and gatekeeper commit;
2. a diff read of the code changes in section F (D1-D11, T) and of `e2b_w25.py`;
3. the W25 pass of section D, under its pre-fixed outcome rule (D.3);
4. the NB-C8 gate (section B.3): **waived for tier 1b-i only** by PI-1102e (LOG l.1173; QG1 YES), so it is met for 1b-i;
5. gate G-L8 (M8 funding, section F): the top-up is logged (LOG l.1163-1164); a per-launch balance line is still required.
It licenses no tier 2 and no tier 1b-ii, e-SNLI-VE, VALSE or AMBER step.
Effort: about 1-1.5 agent-days for D1-D11, `e2b_w25.py`, tests and reads (CC-223 N15). This never takes an agent or
an M8 slot from A, B or C; VSPS-J has no STATE target.

Sources. `P` = `PREREG_DRAFT.md` (sha 6bf702a9, commit 26ae375). `RJ` = `.session_backup/2026-11-02/e2b_rate/rate.json`.
`RL` = `.../e2b_rate/rate.jsonl`. `LOG` = `.session_backup/2026-10-13/decisions/LOG.md`. `E` = `scripts/vsps_j_e2b/e2b.py`
(3df7ce62). `J` = `scripts/vsps_j_e2b/e2b_job.sh` (0478fee9). CC files are in `.session_backup/2026-10-13/decisions/`.
Unsourced numbers are marked [proposal]. Values derived by arithmetic from sourced numbers are marked [derived].
**No M-HalDetect text appears in this file** (CC-218r3 N3). The only data reads behind it are RJ and RL, which hold
timing fields only (`E` l.61 `RATE_KEYS`), plus shas.

## A. Rate run: registered facts

**Run record.**
- Launch: OPS-1102e2b-launch (LOG l.1144), under PI-1102a (LOG l.1140), which approved CC-218r3 option 1.
- Done: OPS-1102e2b-done (LOG l.1146). JOBEXIT 0 at 00:27:36Z. One start, no resume (launch.json `starts` 1).
- Machine: M8, RTX 4090.
- Environment: venv-lb on python 3.12.3, torch 2.5.1+cu121, transformers 4.57.6, freeze 685ffe2a. Import gate PASS
  (LOG l.1144, transcript `.session_backup/2026-11-02/e2b_gate/gate_20261102T001432Z.txt` sha 6447d8a1).

**Output shas** (re-hashed on the laptop at 00:29Z; OUT_MANIFEST re-checked OK):

| file | sha256 | note |
|---|---|---|
| rate.json | a57179187068127522d09d1e98cd7b651220fe5417e69c87d1d58495b844ae91 | authoritative record |
| rate.jsonl | 49db03fb701f74777224f601f26257eb13646debaee353d7a2dfd098a26f87c4 | 880 rows; keys = RATE_KEYS only |
| OUT_MANIFEST.sha256 | 267cdcff6463ffbf2c842ab06e1155dd5d67561d1beefda83a1d14f7fe5aa8c4 | |
| launch.json | d0664c9414870e5e2d626e8eb9dcc031a6d2bc503cc4d1b845303934ecfd47c6 | |
| pip_freeze_rate.txt | 685ffe2a0100ce2489cccd77313d366fb1dce4455871a9d82f65aa139fa85784 | = LB_FREEZE (`E` l.51) |
| e2b_gate/e2b_job.log | 094a688a36348d909b09eec6ae5667bd9f03865c6b7780e93716b20802e9aa37 | no exception (LOG l.1146) |
| e2b_gate/smi.log | 4bc78ffbd550ceef01481b7fa7daee424d461955112dc59a30b698f8ff175e56 | 25 samples; peak 20,500 MiB; compute apps <= 1 (LOG l.1146) |

**Per candidate and form.** Keep rule: mean s/probe <= 0.50 on the 4090 (`P` l.299-303; `E` l.59; CC-218 Ruling 5).
The rate means are over 200 timed probes. RL row ranges are file lines. Every median in this file (RJ `median_s`,
RJ `n_tok_median`, and the RL recomputations) uses the code's upper-median convention `sorted(x)[len(x) // 2]`
(`E` l.335, l.357).

| candidate | load_s | form | status | mean s | median s | n_tok med | keep | sources |
|---|---|---|---|---|---|---|---|---|
| qwen25vl_7b | 46.93 | FA | DONE | 0.1151 | 0.1148 | 414 | **yes** | RJ l.10, 13-18; RL l.1-210 |
| | | FB | SMOKE_FAULT, smoke_ok 8/10 | - | - | - | no | RJ l.21-22; RL l.211-220 |
| internvl3_8b | 149.32 | FA | DONE | 0.3376 | 0.2628 | 1845 | **yes** | RJ l.32, 35-40; RL l.221-430 |
| | | FB | SMOKE_FAULT, smoke_ok 8/10 | - | - | - | no | RJ l.43-44; RL l.431-440 |
| aya_vision_8b | 188.98 | FA | SMOKE_FAULT, smoke_ok 0/10 | - | - | - | no | RJ l.54, 57-58; RL l.441-450 |
| | | FB | SMOKE_FAULT, smoke_ok 0/10 | - | - | - | no | RJ l.61-62; RL l.451-460 |
| qwen3vl_8b | 167.05 | FA | DONE | 0.0811 | 0.0791 | 318 | **yes** | RJ l.72, 75-80; RL l.461-670 |
| | | FB | DONE | 0.0798 | 0.0792 | 329 | **yes** | RJ l.83-88; RL l.671-880 |

**Other recorded facts.**
- Peak VRAM, GB: qwen25vl 15.66, internvl 16.01, aya 17.84, qwen3vl 16.55 (RJ l.25, 47, 65, 91).
- Elapsed 0.193 GPU-h of the 3.0 cap (RJ l.95, l.4). Check by arithmetic: the four load_s sum to 552.3 s and the 880
  RL probe seconds to 141.4 s; together 0.1927 h [derived]. Loads were about 80 % of the run.
- Qwen3-VL ran because the job passes `--with-qwen3` (`J` l.40). Its smoke passed long before the 2.0 GPU-h mark
  (`E` l.355; elapsed 0.193).

**Registered outcomes, recorded as they are; nothing is re-tuned.**
1. Smoke faults on Qwen2.5-VL F-B and InternVL3 F-B (8/10 each). The registered smoke needs finite masses and label
   mass >= 0.5 on all 10 items (`P` l.294-295; `E` l.349, 353-354). Both cells are dropped under `P` l.216-217
   (smoke FAULT).
2. Aya-Vision-8B smoke 0/10 in F-A and in F-B. This is a SMOKE_FAULT, not an ERROR:
   - the candidate's status is DONE (RJ l.53);
   - no exception was raised (LOG l.1146);
   - no TOKEN_FAULT was recorded, so the token-set gate passed (`E` l.369-372).

   It is therefore **not** an operator FAULT:
   - CC-218 Ruling 4 covers hub authentication errors only;
   - CC-218r2 W3 covers import, environment and compile errors only;
   - CC-218r3 N4 asks for an ERROR-type read, and RJ has no ERROR entry.

   Both Aya cells are dropped as registered.
3. Disclosure: RJ `n_tok_median` is taken over smoke + rate rows (`E` l.357), as an upper median
   (`sorted[len // 2]`). Rate-only upper medians differ by at most 1 token (Qwen3-VL F-A 319, F-B 330; recomputed from
   RL).
4. Disclosure (CC-218r2 N2): the 1a run used python 3.12.3. The registered venv-lb was built under 3.10 and setuptools
   is absent on 3.12 (LOG l.1119, l.1144). The freeze sha is unchanged (685ffe2a). **Pin for 1b-i:** the same
   `/root/venv-lb` on M8 (python 3.12.3, freeze 685ffe2a, torch 2.5.1+cu121), so the measured s/probe carries over.

**Open question QA (Aya 0/10: a code defect or the model's behaviour?).** The evidence below comes from code reading
and RL fields only. Nothing was re-run.
- The probe reads the label masses at the **last input position only**, right after
  `apply_chat_template(..., add_generation_prompt=True)` (`E` l.284-290). `first_ids` drops blank tokens on the
  label-word side (`E` l.113-120), but nothing skips a non-label first token on the model side.
- Both Aya forms fail on all 10 items, with two disjoint label-word sets. The same code passes 10/10 on F-A for three
  other models. A label-word clash would have raised TOKEN_FAULT before the smoke (`E` l.370-372).
- The image was in the input. Aya n_tok upper medians (`sorted[len // 2]` over the 10 smoke rows) are 1,806 (F-A)
  and 1,818 (F-B), close to InternVL's 1,851 (RL l.441-460 vs l.221-230). So "image dropped" is unlikely.
- **Hypothesis (unconfirmed).** Aya's first generated token is not a label word, for example a response-start control
  token or a formatting token from its chat template. Then the label mass at that position is near 0 by construction.
- Earlier Aya runs in other blocks used `make_generate`, which decodes with `skip_special_tokens=True`
  (`scripts/lb/decode_hf_vlm.py` l.215). A leading control token would have been invisible there, so those runs are
  no evidence either way.
- The hypothesis cannot be checked by code reading. The Aya snapshot's chat template is not on the laptop, and the
  laptop's transformers is 4.51.3, not 4.57.6.
- **Ruled (CC-223 Ruling 1; effective with a GO):**
  - Aya stays out of E2b tier 1 as a registered smoke drop.
  - A changed probe for Aya would be a new measurement chosen after seeing its outcome (cf. `P` l.101-102, "no fix-up
    after seeing the clash"). Any Aya diagnostic is a separate later item with its own registration.
  - This tier does no Aya re-run.
- **Paper wording (CC-223 Ruling 1, N9):** Aya-Vision-8B is reported as "not assessed: probe-format smoke failure
  0/10 (registered)". No Aya result re-enters E2b tier 1.

## B. Cells carried into tier 1b-i (by the prereg's own rules)

**B.1 Cell set.** Rule: `P` l.216-217. The 8 single-model configs minus every cell dropped by the rate run (keep rule,
token FAULT, smoke FAULT, error after one retry). Result: **4 cells.**

| cell | in 1b-i | rule |
|---|---|---|
| qwen25vl_7b × F-A (vi) | yes | kept (A); N9 applies (`P` l.77-80) |
| internvl3_8b × F-A (vi) | yes | kept (A) |
| qwen3vl_8b × F-A (vi) | yes | kept (A) |
| qwen3vl_8b × F-B (vi) | yes | kept (A); the only F-B cell |
| qwen25vl_7b × F-B, internvl3_8b × F-B | no | smoke FAULT |
| aya_vision_8b × F-A, × F-B | no | smoke FAULT |
| PA2 (Vintern + Aya F-A / F-B) | **void** | no Aya cell exists (`P` l.218-219). `cmd_score` builds PA2 only from Aya runs (`E` l.696-697) |

**B.2 Consequences, registered now.**
- No other-family candidate remains. `P` l.75-76 named Aya as the only other-family model, so tier 1 makes **no
  cross-family claim**. `P` l.351, "any cross-family claim except for Aya", narrows to none.
- The tie-break clause "then Aya" (`P` l.227) is vacuous. The clause "prefer F-B" may also be vacuous: the only F-B
  cell (qwen3vl) can be infeasible under R-a (D4), and then no F-B config competes (CC-223 N5).
- If no single-model config is feasible, the outcome goes straight to PA1 or PA4 (`P` l.228). There is no PA2 step.
- N9 is live because Qwen2.5-VL is in the set (`pick()`, `E` l.568).
- The EN frame runs for the winner only (`P` l.220, l.325), after the vi score names it (section F, D2).
- `cmd_probe` refuses any cell without keep=true in the pulled RJ (`E` l.437-438), so the four dropped cells cannot
  run.

**B.3 NB-C8 gate (`P` l.271-272): not met on its own terms; WAIVED for tier 1b-i only (PI-1102e, LOG l.1173).**
- The gate needs one of two things: a VALSE ledger decision, or an answer to CC-207 Q2.
- CC-207 Q2 was recommended "NOT YET" (CC-207.txt l.69). PI-1102a said YES to the *recommended* answers (LOG l.1140),
  so Q2 stays NOT YET.
- No VALSE ledger line exists (LOG grep "VALSE": no hit after l.461). The VALSE id fetch needs its own irreversible
  >= 92 ruling (CC-218 l.53, l.99).
- NB-C8 was sized for a 7-35 GPU-h tier-1b spend (CC-215r2 l.62). The measured 1b-i spend is about 4.4 GPU-h
  (estimate), at most 6.5 h at the caps of section C (CC-223 N14).
- **The PI waived NB-C8 for tier 1b-i only and kept it for tier 2 and beyond (PI-1102e, LOG l.1173; QG1 YES).** It is no
  longer a 1b-i launch gate.

## C. Per-block GPU-h caps, from the measured rates

**Inputs.**
- 16,027 probes per cell (`P` l.126, l.324).
- Mean s/probe and load_s per cell (section A).
- One `probe` process per cell, with its own `launch.json` t0 and its own `--cap-h` (`E` l.442, l.747).
- The cap clock is wall time since t0, including load and any gap before the one allowed resume (`E` l.237-238,
  l.229-233).
- load_s from the rate run includes the snapshot download and sha check (`E` l.263-274). Under `P` Q8 (keep
  snapshots), 1b-i re-checks rather than re-downloads, so load_s is an upper value.

**Why the rate means are conservative for 1b-i.**
- The image open is inside the timed region in both paths (`E` l.347 and l.468).
- The rate run reopened an image on most probes: 200 spans on 171 images (`P` l.145).
- 1b-i groups about 20.8 segments per image: 16,027 / 769 [derived], with a one-image cache (`E` l.299).

**Cap rule (CC-223 Ruling 2 / W4; fixed before any scored data).**
cap = ceil0.1(max(1.25 × est, (16,027 × max_rate_s + load_s) / 3600)), where est = (16,027 × mean_s + load_s) / 3600
and max_rate_s = the cell's largest rate-phase s/probe in RL. The 1.25 factor follows the PI's tier-1 cap form for C,
`min(ceil(1.25 × P1), 37)` (PI-1102a, LOG l.1140), applied as a precedent. The second term is the all-max tail: the
cap is never below the time the cell would take if every probe ran at the slowest rate-phase probe.

| block | estimate h [derived] | upper-95 mean h [derived] | 1.25 × est [derived] | max_rate_s (RL) | all-max tail h [derived] | cap h | stops if running mean > [derived] |
|---|---|---|---|---|---|---|---|
| 1b-i qwen25vl_7b F-A vi | 0.525 (0.512 probes + 0.013 load) | 0.531 | 0.657 | 0.149 (RL l.11-210) | 0.676 | **0.7** | 0.154 s (+34 %) |
| 1b-i internvl3_8b F-A vi | 1.544 (1.503 + 0.041) | 1.624 | 1.931 | 0.486 (RL l.231-430) | 2.205 | **2.3** | 0.507 s (+50 %) |
| 1b-i qwen3vl_8b F-A vi | 0.408 (0.361 + 0.046) | 0.411 | 0.509 | 0.108 (RL l.471-670) | 0.525 | **0.6** | 0.124 s (+53 %) |
| 1b-i qwen3vl_8b F-B vi | 0.402 (0.355 + 0.046) | 0.404 | 0.502 | 0.099 (RL l.681-880) | 0.488 | **0.6** | 0.124 s (+56 %) |
| **vi block total** | **2.879** | | | | | **4.2** (sum of the cell caps) | |
| 1b-i EN frame, winner only | <= 1.544 (the winner's vi figure) | | | | | **= the winner's vi cell cap** (0.6-2.3) | |
| **1b-i total** | **<= 4.42** | | | | | **<= 6.5** | |

**Notes on the table.**
- **Upper-95 mean column:** mean + 1.96 × SD / √200, from RL. The SDs are 0.0085 / 0.1281 / 0.0053 / 0.0043 s, in
  table order [derived].
- **InternVL tail:** its per-probe time varies widely. Rate-phase max 0.486 s; n_tok 291-3,390 (RL l.231-430;
  dynamic tiling). The all-max tail is 2.205 h [derived], so the cap rule sets 2.3 h. Because a registered STOP is a
  registered drop of the cell (QJ4, D1), the cap must not sit below that tail (CC-223 W4).
- **EN arm:** its rate was never measured. The rate run used `prompt(form, "vi", ...)` only (`E` l.347). Using the vi
  figure assumes image tokens dominate the input (the n_tok medians in section A versus a one-sentence frame)
  [proposal]. At load, the EN run first passes the token-set gate (`E` l.452) and then a registered 10-item EN smoke
  (D5b; CC-223 N4). A token clash or a smoke fail means the EN arm is not run, and that is recorded. EN stays
  descriptive.
- **Cost, for reference only.** M8 bills 17,499 VND/h (LOG l.1109) whether idle or running (LOG l.1140), so 1b-i adds
  **no marginal cost while M8 stays funded** (CC-223 N1). The top-up is logged (CC-223r2 NB-3): PI-1102b (LOG l.1163,
  03:56:44Z) and OPS-1102topup (LOG l.1164): +1,000,000 VND at 10:26 VN on 02/11; balance 1,194,532 VND; M1 + M8 at
  26,781 VND/h gives about 44.6 h, so the balance reaches zero around 07:40 VN on 04/11. Gate G-L8 still requires a
  per-launch balance line. The vi estimate equals about
  50,400 VND, and all caps together about 113,700 VND (6.5 h) [derived].
- **M8 yields between cells (CC-223 N3).** Each cell is its own run, and M8 is free between cells for any B or C GPU
  step with a GO. Before any C custody step on M8, the 769 images and the e2b snapshots are removed from M8 (C
  `PREREG_DRAFT_v1_2.md` l.115, "never M8 while E2b or B jobs run"; PI-1102a Q-custody, LOG l.1140).
- **Restatement of `P` l.334-335.** The keep-bound estimate there was "17.8 GPU-h at most, plus 2.2 h". The measured
  figure is 2.88 h for vi plus at most 1.54 h for EN.

**C.1 The projection rule needs a code change, or the caps fail at the first image.**
- `cmd_probe` switches from the rate mean to the run's own running mean as soon as one probe exists
  (`E` l.449, l.463). The projection is checked before every image, so before image 2 it uses image 1's probes only.
- Each cell is a fresh process, and its first forward pass pays a warm-up cost. The first row of the process (RL l.1)
  took 1.276 s against a cell mean of 0.115 s (about 11 ×). The first rows of later candidates in the same process show
  no such jump: RL l.221 0.501 s against InternVL's 0.338 s mean (+48 %; a smoke row,
  above the rate-phase max of 0.486 s, with n_tok 3,361; CC-223r2 NB-1. No rule depends on it: the first probe of
  each start is excluded under the rule below), l.461 0.109 s against 0.081 s, l.671 0.080 s against 0.080 s.
- **Worked example, qwen3vl F-A:** one cold probe plus 20 probes at 0.081 s gives a projection of 0.66 h [derived].
  That exceeds the 0.6 h cap, and `PROJECTION_STOP` is final (`m0.refuse_if_stopped`).
- **Amended rule, replacing `P` l.332-333 (CC-223 W1 / B1, binding on D5):**
  - The projection uses the rate `mean_s` until the cell's **TOTAL completed probes, across all starts**, reach
    N_RATE = **200** (`E` l.59).
  - After that, it uses the mean of **all completed probes, excluding the first probe of each start** (the
    original start and the one allowed resume).
  - If that set is empty, it uses the rate `mean_s`.
  - Everything else is unchanged: projection = GPU-h used since the first t0 (resume included) + remaining × that mean;
    projection > cap means `PROJECTION_STOP`.
- Code change: section F, D5. The D5 diff read checks the code against this spec, and the D5 test includes a resume
  case.

## D. W25 decision for ledger line 2 (Q5, deferred by CC-218 Ruling 2)

**Ledger line 2, as registered** (`P` l.146-147): "M-HalDetect val, full 769 (tier 1b-i): includes the 91
Karpathy-test images (dev only, spent; PORTFOLIO l.188), held out of every choice." That PORTFOLIO cite is stale: the
91-image line is now PORTFOLIO_3Y l.192, and l.188 is the image-level rule (HEAD).

**Why line 1's ground does not carry over.** CC-218 Ruling 2 granted line 1 partly because its output was
"timing-only (RATE_KEYS)" (CC-218 l.44). Line 2 writes label masses that are scored and drive the selection
(`E` l.472, l.682-725). PORTFOLIO l.188 says: "Before any decode, run the W25 near-duplicate filter across all ledger
owners". Two things still hold, but they are id-level facts only:
- no new image is decoded beyond M0's (PORTFOLIO l.189);
- id intersections were removed (`P` l.152-153).

No SSCD pass has ever been run on these 769 (`P` l.154-155).

**Options.**

| # | option | for | against |
|---|---|---|---|
| D-1 | W25 exception for line 2, no pass (`P` Q5 original recommendation) | zero cost; precedents CC-208 r8, CC-209 r6 | line 1's "timing only" ground is gone; PORTFOLIO l.188 says "before any decode"; J1 withdrew "needs no W25" for line 1 (CC-218 l.13) |
| **D-2** | **W25 rules C1/C2/C3 on the 769 before any 1b-i probe: features on M8, decide on the laptop, against every owner with an SSCD cache (D.1), plus a named partial exception for the owners without one (D.2)** | a measured pass where caches exist, and a named exception, not an implicit one, where they do not; about 2 min CPU; owner caches never move | needs a small new wrapper and its own read; the exception (D.2) needs the panel's grant |
| D-3 | Same pass, but owner caches copied to M8 and decided there | one machine | moves sealed-owner derivatives (KV-5,000 features) onto a shared rented host; needs a ledger ruling (cf. the CC-217r2 custody item on M8) |
| D-4 | Run the whole pass on M1 (m3), where venv-cenfeat, SSCD and the owner caches already live (OPS-1028z-op, LOG l.657) | no new environment | the 769 bytes would have to go to M1; M1 order rules (`P` l.164-165) slip VSPS-J, never A or B |
| D-5 | Defer 1b-i to a portfolio-wide W25 that includes all 3,454 M0 ids (PORTFOLIO l.189) | one pass for everything | no such pass is scheduled; open-ended wait |

**Recommended: D-2** (the panel's choice, CC-223 Ruling 4). D-1 and D-3 are rejected by CC-223 Ruling 4; D-4 stays a
fallback for the feature step only, if M8 is lost. Default if not decided: 1b-i waits (`P` Q5 default).

**D-2 as specified.**

*Code.* `scripts/w25/w25.py` cannot run as committed on these images:
- `w25_job.sh` refuses unless `GPU=m3` (l.23) and the host id is m3 (l.31);
- `cmd_feats_ut` reads the `ut2402` list (w25.py l.141);
- `decide` compares UT against KV and OIV7 (w25.py l.231-248).

New file `scripts/vsps_j_e2b/e2b_w25.py`, about 80 lines [proposal]. It reuses the following unchanged and pinned:
`build_memory.features` and `build_memory.near` (`scripts/c_stage1/build_memory.py`), and `w25.rule` and `w25.sscd_any`
(w25.py l.214-229; C1 sha-equal ∨ C2 min(pHash, dHash) <= 10 with SSCD >= 0.5 ∨ C3 SSCD > 0.75,
`manuscript/prereg/2026-10-28_w25_neardup/RULE.md` l.38-42; below, "RULE.md" means this path).
It has two subcommands:
- `feats`: M8, CPU. The 769 staged images checked against the plan's `probe_images` shas (`E` l.440). Writes
  `feats_mh769.npz` (ids, hashes, SSCD descriptors, file sha256; no text) to `/root/e2b_w25/` by tmp + rename.
- `decide`: laptop, one look. It reads the owner caches as **image features only** (ids, pHash/dHash, mirrored hashes,
  SSCD descriptors, file sha256; RULE.md l.28); it opens no image, caption, label or score. For each owner cache in
  D.1 it prints:
  - the **id-level intersection count** between the 769 and the owner's ids (every owner, KV-5,000 included; CC-223
    W2);
  - counts per criterion (C1, C2, C3) and per image group (the 106 held; the 663 outside them);
  - the E2b image ids to drop or hold, from the 663 only. For the KV row, a drop needs a match with a KV-4,224 image;
    `decide` builds that list with `m0.kv4224()` (ids and keys only, pin 86d93863).

  It never prints owner-side ids (PI-1101o: counts only). It writes `e2b_w25_decide.json` (counts, input shas) and
  `e2b_w25_lists.json` (the sorted drop and hold id lists, possibly empty) by tmp + rename, then their sha256.

It also needs a CPU selftest on synthetic images, and a diff read together with section F.

**D.1 Owner caches compared.** All are already on the laptop as files; each was re-hashed on the laptop and equals
its pin (K1-K5 at 2026-11-02T00:55:57Z; K8 UIT-ViIC test at 2026-11-02T03:33:04Z; K6, K7, K9 at 2026-11-02T03:57:44Z;
path and sha only, opened by nobody). The `~/vsps_w25k1/` caches were built by the W25-K1 laptop run with the same
feature code: venv c_stage1_lists freeze 1a639a50, SSCD 9f26bd4c, parity n = 50 with hashes equal and SSCD cosine min
0.99999988 (LOG l.938).

| owner | cache (laptop path) | sha256 (pin) | on a match outside the 106 held | reason |
|---|---|---|---|---|
| KV-4,224 (MT4 sealed), compared through the KV-5,000 cache | `.session_backup/machines/M1/root/outputs/c_en/feats_coco_kval.npz` | 9783f7a6 (SHA256SUMS_feats l.1; RULE.md l.18) | **drop** on a C1/C2/C3 match with a **KV-4,224** image; a match with the KV-5,000 minus KV-4,224 part is **reported as a count only** (v1.2 narrowing, H10, QJ6) | sealed earlier owner; overlaps are dropped from the later-registered set (PORTFOLIO l.188). The other 776 KV-5,000 images (130 exclusion.json refusals, 130 UT-2,532 ids, 516 A-touched; MT4 PREREG l.29) are not an owner. `decide` takes the KV-4,224 list from `m0.kv4224()` (pin 86d93863, m0.py l.169-191) |
| UT-2,402 (K2 pool) | `.../outputs/w25/feats_ut.npz` | 17d3ebf0 (w25/SHA256SUMS l.3) | **drop** | earlier owner (PORTFOLIO l.188) |
| NoCaps val (4,457 rows after the XM3600 drop, RULE.md l.19) | `.../c_en/feats_nocaps_val.npz` | b69dac29 (SHA256SUMS_feats l.4; RULE.md l.19) | **drop** | assigned to C under PI-1102a Q11 (LOG l.1140); earlier owner (PORTFOLIO l.188) |
| UIT-ViIC test 231 (E1a records; spent dev) | `~/vsps_w25k1/uitviic_test.npz` | 4f478490 (committed: `manuscript/prereg/2026-10-30_mt4_k1k6/w25k1_decide.json` l.76; 231 at l.66) | **drop** | E1a custody: UIT-ViIC test pixels never leave M1 or the laptop (`P` l.164), so a near-copy is not probed on M8. It holds 0 M-HalDetect images by id (CC-208 l.33). Feature parity: LOG l.938 |
| OIV7 val − 456 XM ids, 41,164 (L2-P1) | `~/vsps_w25k1/oiv7_val.npz` | 2ca7e2f5 (committed: `w25k1_decide.json` l.74; 41,164 at l.64) | **drop** | earlier owner (PORTFOLIO l.188); NoCaps val is a subset, so its row above is kept as C's |
| KTVIC test 558 (spent dev) | `~/vsps_w25k1/ktvic_test.npz` | cd985050 (committed: `w25k1_decide.json` l.75; 558 at l.65) | **hold** | spent dev (PORTFOLIO l.191), same reason as Karpathy test |
| OpenViIC test 2,001 (spent dev, OV-test) | `~/vsps_w25k1/openviic_test.npz` | f4c79b82 (committed: `w25k1_decide.json` l.77; 2,001 at l.67) | **hold** | spent dev (PORTFOLIO l.191), same reason as Karpathy test |
| COCO Karpathy test 5,000 (spent dev; contains C's KT-C dev) | `.../c_en/feats_coco_test.npz` | 2bc3b83e (LOG-pinned: OPS-1102b-k2-pin, LOG l.1171; = SHA256SUMS_feats l.2) | **hold** | spent dev, already decoded by M0, as with the 91 (PORTFOLIO l.191-192); the positive control (D.3) also checks this cache |
| C-EN memory: Karpathy train + restval minus 965 refused ids (B4's restval; the UIT-ViIC train pool) | `.../c_en/feats_memory.npz` | caf4a621 (SHA256SUMS_feats l.3) | report count only, handed to B4's ledger as a count-only line | B4's restval is the later-registered set and drops the M0 ids itself (PORTFOLIO l.189); the UIT-ViIC train pool is not yet an owner (PORTFOLIO §2.3, "needs ruling") |

K6-K9 have no positive control of their own: their feature parity rests on LOG l.938, and the M8 features of the 769
are validated by the 91/91 control against K2 (D.3) (CC-223r2 NB-4).

**D.2 Named W25 partial exception for ledger line 2 (CC-223 W3 / B3; proposed text in the CC-218 Ruling 2 style; it
takes effect only with a GO on this amendment).**
"W25 partial exception granted for ledger line 2 only (tier 1b-i, the 769 images of `e2b_plan.json` `probe_images`),
for EVERY PORTFOLIO §2.3 owner (l.161-187), and every owner named in CC-223 W3(a), that has no SSCD feature cache
(CC-223r2 W1):
- A-T3 3,232 (COCO): id-level only; the id intersection is 0 (`P` l.152).
- XM3600 (not from COCO): C1 through M0's `sha_refused`. `cmd_plan` refuses any probe image whose bytes equal an
  `exclusion.json` `image_sha256.xm3600_all_images` entry outside the held set (`E` l.185-186; 3,600 shas). The plan is
  written only after those refusals (`E` l.209), and `e2b_plan.json` exists (6b1b9dd5), so the check passed.
- B's Flickr8K-Expert and Objects365 v2 val: not from COCO; no image-level check.
- C's current PVR sets (C prereg 8282874, blob 0a2f0773): NoCaps test (Open Images, not COCO); OpenViVQA dev (no
  cache; source per dataset description, not re-checked; its source is not stated in C's prereg); XM3600-vi (the
  XM3600 images, so C1 through `sha_refused` as above).
- Each of the following: no cache; source per dataset description, not re-checked.
  - PASCAL-50S (A);
  - ViTextCaps test (C);
  - VieCap4H private test (C);
  - Flickr30K Karpathy test (C);
  - H = 500 KTVIC-train ∩ OV-train-only (B);
  - ADE20K SceneParsing val + LN-ADE val (A);
  - AMBER generative 1,004 (L2-P2; never fetched, `P` §3.5);
  - ViTextVQA test (L1-P1);
  - MTVQA test vi/fr/de/it (L1-P1);
  - TextVQA val / TextCaps val (L1-P1 / L1-P2);
  - VinText test (L1-P2);
  - ViOCRVQA test (L1-P1);
  - ViSignVQA test (reserve);
  - VinDr-CXR test 3,000 (L4 reserve);
  - VizWiz val 7,750 (unassigned).
- The spent dev-only sets of PORTFOLIO l.191 without a cache of their own (spent sets, not owners; the §2.3 heading
  l.161 gives owners to unspent sets only):
  - UIT-ViIC val 924 (COCO; spent K2 dev): its images lie in the COCO 2014 Karpathy split covered by K1, K2 and K3, but
    no per-set tag is used;
  - LongCap, Polaris, DOCCI, THumB, Composite, VaPR: no cache; source per dataset description, not re-checked."

Every other §2.3 row is compared or held:
- KV-4,224 and OIV7 val are compared in D.1.
- B4's restval and the UIT-ViIC train pool are inside the C-EN memory cache (D.1, count only).
- The exclusion.json sets are held by id inside the 106 (`P` l.153-154).

Grounds:
- for A-T3 3,232, KV-4,224 and UT-2,532 only, the id intersections are measured (0 after M0's drop; `P` l.152-153; the
  KV-4,224 figure was re-measured for v1.2, H10). No id intersection is measured for Flickr8K-Expert, Objects365 v2
  val, OpenViVQA or the other rows above;
- E2b is zero-shot probing only, with no training or tuning on any image;
- M0 already decoded all 769 (PORTFOLIO l.189), so no new image is decoded."

This replaces v1's "C's Flickr30K Karpathy test", which is pre-PVR. UIT-ViIC test is not in the exception: it has a
cache and is compared in D.1. v1 wrongly called it "held"; it holds 0 M-HalDetect images (CC-208 l.33).

*Custody.*
- The 769 images are staged on M8 under `/root/.cache/` (inside the backup pull's exclude; `J` l.31-33). 1b-i needs
  them there anyway. They are VSPS-J M0 dev images (PORTFOLIO l.189), fetched like M0 (LOG l.1144, "m0_job.sh
  pattern") and sha-checked against `e2b_plan.json` `probe_images`.
- Only `feats_mh769.npz` leaves M8: a hand pull with its sha, logged in an OPS line.
- Owner caches never leave the laptop and never reach M8.
- No image pair is ever shown to anyone (as in the w25.py header, l.6).

*Environment (CC-223 N10).*
- **M8 side, venv-cenfeat:** built on M8 as `/root/venv-cenfeat` from the committed freeze file
  `manuscript/prereg/2026-10-27_c_en/cenfeat_venv_freeze.txt` (sha 1a639a50; torch 2.5.1+cpu, ImageHash 4.3.2),
  installed `--no-deps`. Gate: `pip freeze | sha256sum` = 1a639a50 (`w25_job.sh` H_FT; RULE.md l.30), logged.
- **M8 side, SSCD weights:** copied from the laptop file `.session_backup/2026-10-22/c_stage1/sscd_disc_mixup.torchscript.pt`
  (re-hashed on the laptop: 9f26bd4c = w25.py `SSCD_SHA`) to `/root/.cache/e2b_w25/`, by `scp` from the laptop. The sha
  is checked on M8 before `feats` runs, and `feats` refuses another sha.
- **Risk:** M8 has only python 3.12.3 (LOG l.1119), while venv-cenfeat was built on M3. If that freeze does not install
  on 3.12, it is an operator FAULT (CC-218r2 W3), not a W25 outcome. The fallback is D-4 for the feature step only.
- **Laptop side:** `decide` needs numpy and build_memory's `near` (build_memory imports numpy at module level, l.24).
  The laptop venv is to be named at the diff read; `~/.venvs/c_stage1_lists` has imagehash.

*Cost.*
- No GPU-h.
- Feature step about 94 s CPU [derived]: 769 × (1.25 h / 36,707 images). The rate is W25's own OIV7 pass on M3,
  fetch included (LOG l.673). M8's CPU is a Ryzen 5 5600, 6/12 vCPU (LOG l.1109).
- Wall cap 0.5 h [proposal], one look, no rerun after `decide` (except the operator-FAULT re-run below).
- `decide` takes seconds on the laptop [proposal].
- The feature step runs only after gate G-L8 (section F).

**D.3 Pre-fixed outcome rule (CC-223 W2 / B2; written before the pass; any later reading is post hoc).**
- **Scope.** Drops and holds are counted only among images **outside the 106 already held** (the 663 of the
  selection set). The 106 stay held whatever they match.
- **Positive control.** `decide` first prints how many of the 91 have a row in `feats_coco_test.npz`. If fewer than 91,
  that is an operator FAULT that goes straight to a judge, because a re-run cannot change the cache.
  The 91 Karpathy-test images in the 769 (PORTFOLIO l.192; CC-208 l.33) must each be flagged by
  at least one of C1/C2/C3 against `feats_coco_test.npz` (2bc3b83e): 91/91. If fewer, the pass is an **operator
  FAULT with no outcome**: nothing is dropped or held, and the pass is re-run under a diff-read note (protocol in
  section F, N7). "At least one of C1/C2/C3" is used because byte equality between the val2014 fetch and the cache's
  source is unverified (CC-223 W2, dissent 4); a later round may tighten it with evidence.
- **Id-level counts.** `decide` prints the id-level intersection count for every owner in D.1, KV-5,000 included.
  These are reported, not used as a pass condition. The only id-based pass condition is the positive control above.
  - Measured before: Karpathy test 91 (CC-208 l.33), UIT-ViIC test 0 (CC-208 l.33), KV-4,224 0 and UT-2,532 0 after
    M0's drop (`P` l.152-153).
  - Measured for v1.2 (ids only, H10): 95 of the 769 ids are KV-5,000 ids, 0 of them KV-4,224; 3 lie in the held 106
    and 92 in the 663. A match with those 95, or with any KV-5,000 image outside KV-4,224, is reported as a count only
    (D.1 KV row). RULE.md l.21 used the superset to exclude extra *training* images; here it would cut 92 dev images
    and protect no owner (QJ6).
  - NoCaps val, OIV7 val, KTVIC test and OpenViIC test ids are not COCO ids, so an id match is not meaningful there;
    only C1/C2/C3 count.
- **A NEW Karpathy-test match beyond the 91** (an image of the 663 flagged against `feats_coco_test.npz`) is **held**,
  not dropped. PORTFOLIO l.188 drops overlaps from the later-registered set, but Karpathy test is spent dev
  (PORTFOLIO l.191), and l.192 holds the 91 for the same reason. Such an image is already decoded by M0, so holding it
  out of every choice is the l.192 precedent applied to a near copy (CC-223 W3(d), chair's answer). It is also excluded
  from any tier-2 Karpathy-test read (carried to the tier-2 amendment, irreversible 92; CC-223 N12).
- **0 drops and 0 holds outside the 106, with the positive control passing:** 1b-i runs on the 769
  exactly as planned. `e2b_w25_lists.json` is empty and is pinned by sha in the OPS line.
- **Any drop or hold outside the 106:** the lists go into `e2b_w25_lists.json`, pinned by sha in an OPS line and
  committed by the gatekeeper before any probe. The code that applies them is written now (D11) and diff-read with
  D1-D10, so no new code is needed after the pass.
- The other owner's ledger gets a count-only line, because M0 already decoded the image (PORTFOLIO l.189).
- **UIT-ViIC test near-copy (CC-223r2 NB-6):** its bytes were already staged on M8 as one of the 769. The drop stops
  any further probing; the OPS line records it count-only as a custody note.

**Ledger line 2 under D-2 (proposed text):** M-HalDetect val, full 769 (tier 1b-i): includes the 91 Karpathy-test
images (dev only, spent; PORTFOLIO l.192), held out of every choice; W25 C1/C2/C3 on the 769 before any probe
(AMENDMENT_1 §D, features M8, decide laptop), per the D.1 table plus the gap exception (§D.2, every owner without an SSCD
cache); outside the 106 held, a match with a sealed or earlier owner is dropped and a match with spent dev (Karpathy
test, KTVIC test, OpenViIC test) is held.

## E. CC-218 N-items: closure table

"Closed" means closed in this text or by a cited record. "D#" items close at the diff read of section F.

| item | status | where |
|---|---|---|
| N1 selection rule, keep-set check, single score, shared-type macro, STOP folders | specified; closes at the diff read | F: D1-D4, D11 |
| N2 tie-break "within 0.5" vs strict `<` | **closed in text**: the registered reading is strict, "less than 0.5 points", matching `E` l.563. No byte change; no scored data exists | this row |
| N3 select-half CI is selection-biased; Vintern's select half is not fresh | **closed in text**: the winner's select-half CI is descriptive and selection-biased, and tier 2 confirms. M0 scored all 663 for Vintern (`P` l.26, l.127). The output carries the note | F: D9 |
| N4 "PASS = all three" (`P` l.250) | carried to the tier-2 amendment (irreversible 92; CC-223 N12) | - |
| N5 reason (b) for -2.0 | **closed in text**: UNSURE spans are not scored, so 435 / 16,885 = 2.6 % (`P` l.259) is an ambiguity proxy, not a noise floor on scored items | this row |
| N6 P(PASS) MC SE about 0.006 at B_out 500 | carried to the tier-2 amendment (irreversible 92; CC-223 N12). Recommendation: decide on the point estimate and report the MC SE. The Karpathy-test hold of D.3 also binds any tier-2 Karpathy-test read | - |
| N7 §6 wording on 0.59 | **closed in text**: 0.59 s on the 4090 would give about 21.0 + 2.6 GPU-h (CC-218 l.72), inside the table. What it breaks is the 0.85 s bound in 3090 terms. Moot now: measured means are 0.08-0.34 s (A) | this row |
| N8 cap checked only between probes | rate: disclosed at launch (LOG l.1144), no overrun (0.193 of 3.0 h). 1b-i: pre-load check | F: D6 |
| N9 memory.used logging | **closed for the rate run** (smi.log 4bc78ffb, 25 samples, apps <= 1; LOG l.1146). 1b-i: the same 30 s sidecar logger is a launch gate; no code | gate G-L5 |
| N10 error message + traceback | rate: no ERROR occurred (RJ l.9, 31, 53, 71 all DONE). 1b-i code | F: D7 |
| N11 exact image set | rate: exactly 171 staged (LOG l.1144). 1b-i: `check_images` today accepts extra files (`E` l.306-309); code | F: D8 |
| N12 HF token custody | **closed for the rate run** (stdin env; token scans 0; LOG l.1144-1145). 1b-i: every kept cell is ungated (B-N1 registry l.103, 192, 279 `"gated": false`), so **no token is passed** | F: D10 |
| N13 DRAFT status line | **closed**: the 26ae375 message governs (CC-209c), ratified prospectively by PI-1102a (LOG l.1140). The same rule applies to this file | - |
| N14 laptop selftest needs no `-I` | carried (disclosure); the host `-I` run is unaffected (LOG l.1144 selftest in the job) | - |
| N15 B's reciprocal NB-C10 sentence | **carried, narrower** (CC-223 Ruling 6, N11): B `PREREG_DRAFT_v3_1.md` (5ff00c9) l.104-106 already bars VSPS / VSPS-J weights, prompts and thresholds; only the literal reciprocal sentence is missing. Carried to B's R5 amendment, before any B 4090 step (B and E2b share the Qwen2.5-VL-7B pin cc594898). B's item, not closable here | to B (R5) |
| N16 STATE file stale | **coordinator item before the gatekeeper commit** (CC-223 N13): refresh the compute row of `.claude/agents/STATE_2026-11-01.md` l.6 ("Rented: M1, one RTX 3090 only"); M8 (RTX 4090) is rented per LOG l.1109 | coordinator |
| N17 n-gram scan | **closed** by CC-218r3 Ruling 1 (OPS-1101e2b-dev26ae375) | - |
| N18 §3.2 header (`P` l.143) | **closed in text**: the ledger text is at `P` l.145-147, not in the request | this row |
| N19 e2b.py size | carried. D1-D11 add about 130 lines [proposal]; QJ5 "leave" upheld (CC-223 Ruling 5) | G |

**Carries from CC-218r2 and CC-218r3.**

| item | status |
|---|---|
| r2 N1 / r3 N9: versions in launch.json; ImportError -> Fault in code | F: D7 |
| r2 N2: 3.10 -> 3.12 disclosure, interpreter pin | **closed in text** (A, disclosure 4) |
| r2 N3 / r3 N8: `P` §3.5 says an AMBER copy exists | **closed in text**: the copy is gone, OPS-1101amber-del (LOG l.1118); `P` l.185-189 is superseded |
| r2 N4: AMBER literal deviation, /mnt/c unchecked | carried (disclosure) |
| r2 N5 / r3 N5: token scans | closed for the rate run (LOG l.1144-1145); 1b-i passes no token |
| r2 W3: environment error = operator FAULT | **binding in 1b-i**: a STOP with rc 5 `ENV_FAULT` (D7), rc 6 `PIN_FAULT` or a vi rc 7 `TOKEN_FAULT` (D1), and a lost M8 (G-L8), is never a registered drop; it is re-run under the operator-FAULT protocol (section F) |
| r2 N7 / r3 N1: gatekeeper-GO rule; stamps from `date -u` | binding; this file is stamped from `date -u`; WORKFLOW_LOG lesson carried (operator) |
| r3 N3: "no M-HalDetect text" statement | **closed** (header). Probe outputs hold masses, not text; add M-HalDetect to the n-gram corpus before any commit that holds text |
| r3 N4: ERROR types in rate.json | **closed**: no ERROR entry (RJ l.9, 31, 53, 71) |

## F. Code changes: diff plan only (e2b.py, e2b_job.sh and test_e2b.py are not edited here)

| # | file / place | change | closes |
|---|---|---|---|
| D1 | `cmd_score` (`E` l.682-690), `load_runs` (`E` l.653-664); `cmd_probe` load path (`E` l.450-454) | New `--rate R` argument and pin `RATE_SHA = "a57179187068127522d09d1e98cd7b651220fe5417e69c87d1d58495b844ae91"`. `kept = {(c, f) : RJ cands.c.forms.f.keep}`. Every `*_F?_vi` folder must be a kept cell, and every kept cell must have a folder, else REFUSED. The load path gets its own codes (CC-223 N6): a snapshot pin mismatch from `load_cand` -> rc 6 `PIN_FAULT`; a token-set clash from `make_probe` -> rc 7 `TOKEN_FAULT`; rc 2 is then only `FAULT non-finite mass` (`E` l.471). A folder is either complete (sha + cover of the remaining keys: 16,027 when there is no drop; D11) or holds a STOP marker, classified by its JSON `rc`. (1) rc 3 `PROJECTION_STOP`, rc 4 `CAP_STOP` (including D6's pre-load stop) and rc 2 non-finite mass -> `DROPPED_STOP`: recorded and left out of `pick()`, the same class as a rate-run drop (`P` l.216-217). This amends `P` l.343 for these codes only. **Score never opens `probes.jsonl` in a DROPPED_STOP folder; partial probes feed no output, descriptive ones included.** (2) rc 6 `PIN_FAULT`, rc 5 `ENV_FAULT` (D7), or rc 7 `TOKEN_FAULT` on a **vi** cell -> operator FAULT: REFUSED, re-run under the operator-FAULT protocol below (CC-218r2 W3). **This amends `P` l.101-102 and §8 for 1b-i vi cells** (CC-223r2 NB-2). Reason: the rate run passed the vi token-set gate for all four kept cells, the tokenizer files are sha-checked by `check_snapshot` (a mismatch is rc 6), and the freeze is gated (G-L4), so a vi clash with equal pins and freeze is drift. The rate run recorded no token ids (`E` l.369 discards `_sets`; RJ holds none), so there is no rate-run `token_sets.json` to compare with. Each 1b-i cell's `token_sets.json` sha goes into its OPS line, so later cells are compared observed to observed. **A second vi clash on the re-run takes the registered drop path (DROPPED_STOP).** rc 7 on an **EN** cell means "EN arm not run" (D2). (3) No folder, or an incomplete folder with no STOP marker (a crashed, resumable run) -> REFUSED. `load_runs` stops calling `refuse_if_stopped` and reads the STOP JSON (`m0.halt`, m0.py l.428-429) | N1 (keep set, STOP / never-reached); CC-223 N6 |
| D2 | `cmd_score`; new `score-en` | Single-score guard: refuse if `runs/SCORED.json` exists. After `res` is written, write `SCORED.json` with {res sha256, RATE_SHA, cells, utc}. The SCORED.json sha goes into an OPS line as soon as it is written (CC-223 N7). Move the EN block (`E` l.719-722) into a new subcommand `score-en`. It refuses unless `SCORED.json` exists, its res sha matches, and the only `*_en` folder is `<winner cand>_<winner form>_en`; an EN folder with rc 7 `TOKEN_FAULT` or rc 8 `EN_SMOKE_FAULT` is recorded as "EN arm not run" and its probes are never opened. It writes `res_en.json` once (`SCORED_EN.json` guard), reports the EN malformed-mass share (share of EN probes with label mass < 0.5), and never re-runs `pick()`. This resolves "EN for the winner only" (`P` l.220) vs "scored once" (`P` §4 header): today `score` sees EN only if it already exists | N1 (single score); EN conflict |
| D3 | `macro` (`E` l.538-541), row build (`E` l.703-706) | `macro_pair(E, V, k)` averages only over primary types where **both** systems have `k` defined. Apply it to dprec, dret and drecall; record `types_used` per config. U stays `macro(E, "U")`. This **clarifies `P` l.229** ("a type with an undefined metric is left out"), fixed before any scored output (CC-223 N5) | N1 (shared types) |
| D4 | `pick()` (`E` l.549-569), rows (`E` l.703) | Recall-comparable feasibility (QJ1, option R-a): a config is feasible only if its **tune strict recall >= R_DESIGN 0.83 on each primary type**, in addition to U <= 12 and Δret >= -2.0. This reuses the registered 0.83 (`P` l.202). F-A configs meet it by construction unless they fell back to 0.5; F-B must reach the same recall to compete. **If a primary type's tune recall is undefined (no gold-false tune probe), the config is infeasible.** This **amends `P` l.226**, fixed before any scored output (CC-223 N5). Disclosed: the only F-B cell (qwen3vl) may be infeasible, and then the "prefer F-B" tie-break is vacuous (B.2). Pass `tune_recall` into `rows` | N1 (selection) |
| D5 | `cmd_probe` (`E` l.449, l.463, l.475) | Spec of C.1 (CC-223 W1 / B1), verbatim: the projection uses rate `mean_s` until the cell's TOTAL completed probes, across all starts, reach N_RATE = 200; after that, the mean of all completed probes excluding the first probe of each start; if that set is empty, rate `mean_s`. Implementation: each `probes.jsonl` row gains `start` (= `launch.json` `starts` at write time); the mean drops the first row of each `start` value. The loaded rows of a resume count toward both the threshold and the mean | C.1 (B1) |
| D5b | `cmd_probe`, `--lang en` only, after `make_probe` | Registered 10-item EN smoke at load (CC-223 N4): the first 10 segments in M0's image order; finite masses and label mass >= 0.5 on all 10 (the rate-run smoke rule, `P` l.294-295). On a fail: `m0.halt(out, 8, "EN_SMOKE_FAULT ...")`; the EN arm is not run, and `score-en` records that. Smoke results are booleans only, as in the rate run | CC-223 N4 |
| D6 | `cmd_probe` before `load_cand` (`E` l.451) | `if elapsed_h(out) >= a.cap_h: return m0.halt(out, 4, "CAP_STOP before load")`. With Q8 (snapshots kept) the fetch is a re-check; this is the pre-fetch check. Such a stop is a registered drop (D1) | N8 |
| D7 | `prep_out` (`E` l.222-234); `cmd_rate` except (`E` l.417-420); `cmd_probe` | First start: `launch.json` gains `python` (sys.version), `torch`, `cuda` (torch.version.cuda) and `transformers`. ImportError, ModuleNotFoundError and torch/CUDA compile errors -> `m0.halt(out, 5, "ENV_FAULT ...")`. Other exceptions: write `error.json` with `type`, `msg` and `traceback`, each passed through `redact()` (replaces the `HF_TOKEN` env value and `hf_[A-Za-z0-9]{30,}` with `<redacted>`, cut to 4 kB), then re-raise (a crash keeps its one resume). rate.json stays authoritative over duplicate rate.jsonl rows after a retry | N10; r2 N1; r2 W3 |
| D8 | `check_images` (`E` l.306-309) | Also FAULT if the folder holds any file not in `want` (exact set) | N11 |
| D9 | `cmd_score` (`E` l.713) | `res["winner_ci_select_note"] = "selection-biased, descriptive; tier 2 confirms; Vintern select half not fresh (M0 scored all 663)"` | N3 |
| D10 | `e2b_job.sh` (`J` l.14-17, l.30, l.40) | New `probe` sub-job: `CELL=<cand>_<form>_<lang>`. Fixed table `CAPS` = qwen25vl_7b_FA 0.7, internvl3_8b_FA 2.3, qwen3vl_8b_FA 0.6, qwen3vl_8b_FB 0.6 (vi; section C rule, CC-223 W4). EN: the winner's vi cap, accepted only with `RES=<res.json>`, whose winner must match. `--cap-h` is taken from the table and never typed. OUT `/root/e2b_probe`. RATE = the pulled rate.json, checked against a5717918 before the run. IMAGES must be exactly the 769 minus any D.3 drops (D11) under `/root/.cache/`. **No HF_TOKEN required** for probe. Same SUMS, LB and freeze checks; RTX 4090 check; per-cell OUT_MANIFEST. GPU sharing stays "alone not required" (`P` l.324), but the smi logger runs | caps pinned; N12 |
| D11 | `sets_and_segments` (`E` l.155-163), `cmd_plan` (`E` l.173-176), `cmd_score` (`E` l.688), `load_runs` (`E` l.661), `cmd_probe` | Drop/hold mechanics, written now (CC-223 N10). New pin `W25_LISTS_SHA` = the sha of `e2b_w25_lists.json` ({"drop": [...], "hold": [...]}, sorted COCO ids), filled from the OPS line after the pass. `sets_and_segments` removes the drop ids from probe, selection and held, and moves the hold ids into held. The count asserts become: probe = 769 − n_drop images, selection = 663 − n_drop − n_hold, with segment counts recomputed and printed. Score's cover checks use the remaining keys: M0 arm-A rows must cover them (a superset is allowed), and each run folder must cover them exactly. `cmd_probe` refuses if the staged images differ from the remaining set. With empty lists every count equals today's | CC-223 N10; D.3 |
| T | `test_e2b.py` | One assert group per change: R-a feasibility, including the undefined-recall case; `macro_pair` on a NaN type; D5 projection, a cold first probe does not trip the cap, **and a resume case** (two starts, each with a slow first probe; both excluded; threshold counted across starts); D5b EN smoke fail -> rc 8; exact-set refusal; second `score` refused; `score-en` refuses a non-winner folder and never opens rc 7 / rc 8 probes; DROPPED_STOP folders never opened; rc 5 / rc 6 / first vi rc 7 refused, second vi rc 7 -> DROPPED_STOP; `redact()` removes a fake `hf_` token; D11 with empty and non-empty lists | - |

Not changed: the rate path (done), `band` / `hi_rule` / `match_lo`, `paired_ci`, prompts, token sets, keep rule.
`e2b_w25.py` (section D) joins the same diff read. No code is written against this amendment until it has a GO
(CC-223 Ruling 8).

**Operator-FAULT re-run protocol (CC-223 N7).** It applies to rc 5 `ENV_FAULT`, rc 6 `PIN_FAULT`, a vi rc 7 `TOKEN_FAULT`,
a lost M8, and a W25 pass with a failed positive control.
- Archive the faulted folder outside the runs folder, unchanged.
- Re-run with a fresh OUT and a fresh t0.
- At most one re-run per cell (and one per W25 pass).
- Log an OPS line each time.
- A second operator FAULT on the same cell or pass holds the score and goes to a judge. It is never a registered drop,
  except a second vi rc 7, which takes the registered drop path (D1; CC-223r2 NB-2).

**Launch gates for any 1b-i cell** (one OPS line, every stamp from `date -u`):
- G-L1: this amendment committed after a GO, plus the diff-read GO on D1-D11, T and `e2b_w25.py`; M8 HEAD = that
  commit; porcelain 0.
- G-L2: NB-C8 waived for tier 1b-i only (PI-1102e, LOG l.1173; QG1 YES). Met.
- G-L3: the W25 pass done under D.3, with the positive control passed and `e2b_w25_lists.json` pinned (D-1 is rejected).
- G-L4: import gate re-run under `/root/venv-lb/bin/python -I`, freeze 685ffe2a, with its transcript sha.
- G-L5: exactly the 769 images minus any D.3 drops (D11) under `/root/.cache/`, sha-checked; the 30 s smi logger
  running.
- G-L6: `--exclude='/e2b_probe/'` added to the M8 full pull (as OPS-1101bak-e2b did for `/e2b_rate/`), with a hand pull
  plus manifest per cell.
- G-L7: snapshots still in `/root/.cache/e2b_hub`, else the download counts inside the cell cap (it is in load_s
  anyway).
- G-L8 (CC-223 N2; also before the D-2 feature step): a logged executed top-up (met: PI-1102b and
  OPS-1102topup, LOG l.1163-1164) AND, for each launch, a logged M8 balance and remaining rental time that cover the
  cell cap plus the pull; and no B or C GPU step with a GO waiting for M8. If M8 is lost,
  that is an operator FAULT, not a registered drop. The re-run goes on a 4090 with the venv-lb freeze 685ffe2a, and
  either the rate is re-measured or the carry-over is disclosed.

## G. Questions (each with a recommendation and a default)

**For the PI.**

| # | question | recommendation | default |
|---|---|---|---|
| QG1 | Waive NB-C8 for tier 1b-i only, keeping it for tier 2 and beyond? | **ANSWERED YES** (PI-1102e, LOG l.1173) | - |
| QG2 | W25 for ledger line 2 | **ANSWERED: D-2** (PI-1102e, LOG l.1173), with the named partial exception (D.2) | - |
| QG3 | Aya-Vision-8B 0/10 smoke as a registered drop (no re-run; PA2 void; no cross-family claim in tier 1) | **ANSWERED YES** (PI-1102e, LOG l.1173) | - |
| QG4 | EN arm as a once-only `score-en` for the winner only, with a registered 10-item EN smoke at load (D2, D5b) | **ANSWERED YES** (PI-1102e, LOG l.1173) | - |
| QG5 | M8 top-up | **ANSWERED: topped up** (PI-1102b, LOG l.1163; OPS-1102topup, LOG l.1164: +1,000,000 VND, balance 1,194,532 VND, zero around 07:40 VN on 04/11) | - |
| QG6 (CC-223r2 Q2) | Accept that the cacheless §2.3 owners (the D.2 list, AMBER included) are covered by a named exception marked "source per dataset description, not re-checked", instead of verifying each source now? | **YES** | **registered as written in D.2** (not yet answered by the PI) |

**For the judges.**

| # | question | recommendation | default |
|---|---|---|---|
| QJ1 | N1 recall comparability: R-a (feasible only if tune strict recall >= 0.83 per primary type; undefined = infeasible; no new number), R-b (Δrecall on the select half >= -2.0, mirroring H4) [proposal], or R-c (no rule; disclose the recall gaps) | **R-a** (upheld, CC-223 Ruling 5); R-b quantities stay reported (`P` l.210-211) | R-a |
| QJ2 | Superseded by CC-223 Ruling 2: cap = ceil0.1(max(1.25 × est, all-max tail)), caps 0.7 / 2.3 / 0.6 / 0.6 h; EN = the winner's vi cap | - | - |
| QJ3 | Projection change C.1 / D5 (the B1 spec: rate mean until 200 total probes across starts; then all probes minus the first of each start) | **Yes** (upheld, CC-223 Ruling 5); without it every cell risks a final PROJECTION_STOP at image 2 | 1b-i waits for D5 |
| QJ4 | A registered STOP in a 1b-i cell (rc 3 PROJECTION_STOP, rc 4 CAP_STOP, rc 2 non-finite mass, and a second vi rc 7) = a registered drop of that cell from the selection (D1), not a refusal of the whole score. rc 5 ENV_FAULT, rc 6 PIN_FAULT and a first vi rc 7 TOKEN_FAULT stay operator FAULTs that are re-run (the vi rc 7 rule amends `P` l.101-102 and §8 for 1b-i vi cells) | **Yes**; upheld only together with B1 (C.1) and B4 (caps), so that a timing artifact cannot become a registered drop (CC-223 Ruling 5) | whole score refused (`P` l.343) |
| QJ5 | Split e2b.py (N19) at this revision? | **No** (upheld, CC-223 Ruling 5; Q9 LEAVE stands) | leave |
| QJ6 | KV row (v1.2 narrowing, made on ids only, before any W25 pass, label, score or model output): drop only on a match with a KV-4,224 image, and report a match with the rest of KV-5,000 as a count, or keep v1.1's "drop on any KV-5,000 match"? The latter would drop the 92 A-touched ids in the 663 by C1 alone: selection 663 -> 571, with the tune / select splits and segment counts shifting, while protecting no owner | **Narrow to KV-4,224** (the row's stated reason is the sealed owner; 0 of the 95 are in it) | the narrowed rule, as written in D.1 |

## H. Conflicts found while drafting

1. **NB-C8 was a 1b-i blocker; it is now waived for tier 1b-i only** (PI-1102e, LOG l.1173; QG1). It still binds
   tier 2 and beyond.
2. **Score-once vs EN for the winner only.** `cmd_score` includes EN only if an EN folder already exists (`E` l.719),
   and the winner is unknown until `score` runs. A single-score guard would make the registered EN arm impossible
   (D2).
3. **Running-mean projection vs per-process warm-up** (C.1). With registered code, a cap near the estimate stops at
   image 2.
4. **W25 tooling is M3- and UT-bound** (`w25_job.sh` m3-only; `cmd_feats_ut` reads `ut2402`). "Run w25.py on M8" needs
   the wrapper in section D. The owners without an SSCD cache are named in the D.2 partial exception.
5. **N15 narrower than in v1.** B v3.1 l.104-106 already bars VSPS / VSPS-J weights, prompts and thresholds; only the
   literal reciprocal sentence is missing (carried to B's R5 amendment).
6. **Stale cite.** `P` l.146 cites PORTFOLIO l.188 for the 91 Karpathy-test images; that line is now l.192 (HEAD).
7. **`P` §3.5 (l.183-189)** still says an AMBER query copy exists; it was deleted (LOG l.1118). Superseded here.
8. **v1 was wrong on UIT-ViIC test.** v1 said it was "held" and had no SSCD cache. It holds 0 M-HalDetect images
   (CC-208 l.33), and a committed-pin cache exists on the laptop (`~/vsps_w25k1/uitviic_test.npz` 4f478490;
   `w25k1_decide.json` l.76; found by the B R5 drafter, K8). v1.1 compares against it (D.1). This moves UIT-ViIC test
   out of the literal CC-223 W3(a) gap list, a named deviation from the ruling text, made on a fact verified by path
   and sha. For consistency, the other pinned laptop caches from the same run are also compared: K6 OIV7 val, K7 KTVIC
   test and K9 OpenViIC test.
9. **`feats_coco_test.npz` (2bc3b83e) is now LOG-pinned** (OPS-1102b-k2-pin, LOG l.1171; it was a mirror pin only in
   v1.1). The D.3 positive control (91/91) also checks that cache.
10. **KV-5,000 id intersection with the 769, measured for v1.2 (ids only; CC-223r2 NB-5):**
    - Counts: 95 of the 769 ids are KV-5,000 ids. 0 of them are in KV-4,224, so all 95 are in KV-5,000 minus KV-4,224.
      3 are in the held 106 (all exclusion.json refusals). 92 are in the 663. Those 92 are neither refused nor UT-2,532
      ids, so by the `counts()` set definitions (`scripts/grl/id_counts.py` l.63-72) they are A-touched ids.
    - A-touched is not a ledger owner: PORTFOLIO has no "A-touched" row, and M0's owner list is A-T3, KV-4,224 and
      UT-2,532 (m0.py l.143).
    - Method: the 769 ids are parsed from the keys of `e2b_plan.json` `probe_images` (6b1b9dd5). KV-5,000 is
      `manuscript/prereg/2026-10-27_grl_pilot/kv5000.txt` (b7a7a89d). KV-4,224 is rebuilt by `m0.kv4224()` (m0.py
      l.169-191; venv vsps_j_m0, python -I), which checks the result against pin 86d93863. That function loads the
      UIT-ViIC JSONs, `dataset_coco.json`, `gt_cache.json` and `a_n3_instance_gold.json` and uses ids and keys only;
      it is M0's judged route.
    - Also read: exclusion.json `ids.coco` (c52a96d1), `selection_excluded_ids.txt` (57195c49), `ut2532.txt`
      (288340b8). Only counts were printed.
    - Consequence: v1.1's "drop any KV-5,000 match" would have dropped those 92 by id alone. v1.2 narrows the KV row
      to KV-4,224 (D.1, D.3, QJ6).
11. **M8 funding: resolved.** PI-1102b (LOG l.1163) and OPS-1102topup (LOG l.1164) log the top-up (+1,000,000 VND at
    10:26 VN on 02/11; balance 1,194,532 VND; about 44.6 h for M1 + M8; zero around 07:40 VN on 04/11). G-L8 still
    needs a per-launch balance line.

## I. v1.1 changes (CC-223 closure; v1 = 668626ad stays byte-equal)

| CC-223 item | v1.1 change | where |
|---|---|---|
| W1 = B1 projection under resume | single spec: rate mean until TOTAL probes across starts reach 200; then all probes minus the first of each start; empty set -> rate mean. D5 restates it verbatim; T has a resume case | C.1, D5, T |
| W2 = B2 W25 outcome rule | counted outside the 106 only; 91 Karpathy-test images = positive control, 91/91 by >= 1 of C1/C2/C3, else operator FAULT with no outcome; id-level counts per owner incl. KV-5,000; a new Karpathy-test match is HELD (PORTFOLIO l.188 vs l.191-192) and kept out of any tier-2 Karpathy-test read | D.3; `decide` spec in D |
| W3 = B3 named partial exception | CC-218 Ruling 2-style text naming A-T3 3,232; XM3600; B's Flickr8K-Expert and Objects365 v2 val; C's PVR sets (NoCaps test, OpenViVQA, XM3600-vi; 8282874 / 0a2f0773), with status and grounds; D-2 row and ledger-line-2 text reworded ("per the §D table plus the gap exception"); Flickr30K removed | D options table, D.2, ledger line 2 |
| W3(c) UIT-ViIC test | corrected: 0 M-HalDetect images (CC-208 l.33), not "held". Coordinator fact verified by path + sha: cache `~/vsps_w25k1/uitviic_test.npz` 4f478490 = committed pin `w25k1_decide.json` l.76; feature parity LOG l.938. **Deviation from W3(a)'s literal list:** UIT-ViIC test moves from the gap list into the compared owners (drop on a match, E1a custody). The same run's pinned caches K6 OIV7 val (drop), K7 KTVIC test and K9 OpenViIC test (hold) are added the same way. D.2 is scoped to the W3(a) owners, and every other §2.3 row is accounted for | D.1, D.2, H8 |
| W4 = B4 caps | cap = ceil0.1(max(1.25 × est, (16,027 × max_rate_s + load_s)/3600)) -> 0.7 / 2.3 / 0.6 / 0.6 h; vi 4.2 h, total <= 6.5 h; D10 CAPS 2.3; QJ2 superseded | C table, D10, G |
| N1 cost wording | "no marginal cost while M8 stays funded" | C notes, QG1 |
| N2 G-L8 | hard launch gate, also before the D-2 feature step; lost M8 = operator FAULT | F gates, QG5 |
| N3 M8 yields | between cells; the 769 images and e2b snapshots removed before any C custody step | C notes |
| N4 EN smoke | registered 10-item EN smoke at load (rc 8); EN malformed-mass share in res_en.json | C notes, D2, D5b |
| N5 D3 / D4 | D4 amends `P` l.226, D3 clarifies `P` l.229; undefined tune recall = infeasible; F-B tie-break may be vacuous | B.2, D3, D4, QJ1 |
| N6 D1 | DROPPED_STOP probes never opened; load-path rc 2 split into rc 6 PIN_FAULT and rc 7 TOKEN_FAULT; a vi rc 7 is an operator FAULT, an EN rc 7 means the EN arm is not run | D1, QJ4 |
| N7 re-run protocol | archive, fresh OUT and t0, one re-run, OPS line; SCORED.json sha logged at once | F protocol, D2 |
| N8 n_tok, l.190-191 | upper-median convention stated; InternVL first row 0.501 s vs 0.338 s (+48 %) | A, C.1 |
| N9 Aya wording | "not assessed: probe-format smoke failure 0/10 (registered)" | A (QA) |
| N10 decide / environment / reasons | features only; venv-cenfeat from the committed freeze 1a639a50 and SSCD 9f26bd4c from the laptop copy, both sha-checked on M8; full RULE.md path; a reason per owner row; drop/hold mechanics written now (D11) | D, D.1, D11 |
| N11 B / cites | N15 narrower, carried to B R5; stale `P` l.146 cite and §3.5 AMBER sentence fixed as drafted | E, H |
| N12 tier-2 carry | N4, N6 and the Karpathy-test hold go to the tier-2 amendment (irreversible 92) | E, D.3 |
| N13 STATE | coordinator item before the gatekeeper commit (`.claude/agents/STATE_2026-11-01.md` l.6) | E (N16 row) |
| N14 NB-C8 sizing | 7-35 GPU-h sized vs about 4.4 h measured (6.5 h at caps) | B.3, QG1 |
| N15 effort | about 1-1.5 agent-days; never takes an A, B or C slot | header |
| Rulings 1, 4, 5, 7 | Aya drop upheld; D-1 and D-3 rejected, D-4 fallback; QJ1 / QJ3 / QJ4 / QJ5 upheld; launch gates (i)-(iv) in the header | A, D, G, header |
| own corrections | RULE.md cites checked (KV-5,000 superset l.21, feature content l.28); `feats_coco_test.npz` was a mirror pin only (H9; LOG-pinned since v1.2); KV-5,000 id intersection unmeasured (H10) | D.3, H |

## J. v1.2 changes (CC-223r2 closure; v1 and v1.1 stay byte-equal)

| CC-223r2 item | v1.2 change | where |
|---|---|---|
| W1 B3(a) scope (BLOCKING) | the D.2 grant covers every cacheless §2.3 row and W3(a) owner: A-T3, XM3600, Flickr8K-Expert, Objects365 v2 val, NoCaps test, OpenViVQA, XM3600-vi, and 15 rows marked "no cache; source per dataset description, not re-checked", AMBER 1,004 included; "the panel may require" deleted; the id-intersection ground limited to A-T3, KV-4,224 and UT-2,532 | D.2 |
| NB-1 | the RL l.221 0.501 s row is called a smoke row above the 0.486 s rate-phase max; no rule depends on it | C.1 |
| NB-2 | vi rc 7 labelled "amends `P` l.101-102 and §8 for 1b-i vi cells"; the rate run recorded no token ids, so drift is argued from the pins and freeze, and each 1b-i cell's `token_sets.json` sha is logged; a second vi clash takes the registered drop path | D1, F protocol, T, QJ4 |
| NB-3 | funding text set to PI-1102b and OPS-1102topup; QG5 answered; G-L8 = logged top-up AND a per-launch balance line | header, C notes, G-L8, QG5, H11 |
| NB-4 | ledger line 2 says "per the D.1 table"; K6-K9 note (no own positive control; parity LOG l.938; M8 features validated by 91/91) | D.1, ledger line 2 |
| NB-5 | K2 cache LOG-pinned (OPS-1102b-k2-pin, LOG l.1171); KV-5,000 id intersection measured, ids only: 95 / 0 in KV-4,224 / 3 held / 92 in the 663 | D.1, D.3, H9, H10 |
| NB-5 follow-on (new) | the KV row is narrowed to KV-4,224 (drop); the rest of KV-5,000 is count only. Made on ids only, before any W25 pass, label, score or output; named for the panel | D.1, D.3, `decide` spec, QJ6 |
| NB-6 | a UIT-ViIC test near-copy is recorded count-only as a custody note; the drop stops further probing | D.3 |
| PI-1102e | QG1 YES (NB-C8 waived for 1b-i only), QG2 D-2, QG3 Aya registered drop, QG4 score-en once: marked answered | header, B.3, G-L2, G, H1 |
| CC-223r2 Q2 | registered as QG6 with the recommended default (named exception, "not re-checked") | G |
| carried | N13 STATE refresh (coordinator, before any commit); venv-cenfeat on python 3.12 (FAULT, fallback M1); code diff read of D1-D11, T and `e2b_w25.py` after adoption | E, D, F |
