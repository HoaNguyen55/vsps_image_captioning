# C-ATTR-DEV: scoring run document v1 (block 1b, batched block-1 rows, block-0 post hoc rows), on the rented host

Version v1, written 2026-11-12T00:03Z (07:03 VN). Not committed. It binds only after the one-judge read of the scoring package, which is a new topic (CC-346 ruling 5). Label: `DEVELOPMENT / C-ATTR-DEV, NON-CONFIRMATORY`. Rules: registration v1.1 §7–§9, erratum 1, addendum v1.2 V4 (scoring order) and V6 (labels); CC-338 S1–S5; CC-346 SC1–SC5; PI-1111j (CPU scoring runs on the rented host; the laptop keeps the 444 copy and the hashes only). Nothing on this page names a host address.

Code: the pre-score commit, `scripts/c_attr/SHA256SUMS` (its eight files). The entry is `scripts/c_attr/c_attr_score_job.sh`. The order is enforced in `c_attr_score.py` (`stage`), and `c_attr.py score` itself runs the V4 gates (SC1). Every stage prints only file names, counts, labels and sha256. No stage prints a caption.

## 0. Preconditions (each a STOP gate)

| item | check | otherwise |
|---|---|---|
| decode job ended | `/root/outputs/c_attr_b1/RUNNING` and `/root/outputs/c_attr/RUNNING` absent; `JOB DONE` in `c_attr_b1/logs/job.log` and every Tier-A step `OK` (CC-346 N2) | a CAP STOP, a JOB STOP or K7 before the last Tier-A step: no score until a judge line (CC-346 R5) |
| block-1b pull | laptop pull per block-1b run document v1.1 §5 (R7): whole-tree digest equal, `sha256sum -c` all OK except `logs/job.log`, 444. The OPS line gives the sha256 of `c_attr_b1/SHA256SUMS` (= B1SUMS) | STOP |
| block-1 pull | the sha256 of `c_attr/SHA256SUMS` from the OPS-1112c pull (= BSUMS) | STOP |
| scoring code on the host | `/root/vsps` checked out at the pre-score commit, only after the decode job ended | STOP |
| stage-2 ledger | copied from the laptop to `/root/c_attr_score/in/stage2_ledger.jsonl`; the code checks it against `be716482…` | STOP at verify |
| segmenter | `$NCS_DATA/vncorenlp/VnCoreNLP-1.2.jar`, sha256 `9e2811cdbc2ddfc71d04be5dc36e185c88dcd1ad4d5d69e4ff2e1369dccf7793` (`score.JAR_SHA256`), with its `models/wordsegmenter/` files, and a Java runtime. If the files are missing, copy them from the laptop's `ncs-data/vncorenlp/`. Nothing is downloaded or built on the host. The model files have no committed pin. Their sha256 go into `VERIFY.json`, and the §7.1 parity gate is the binding check | STOP at verify |
| references | `$NCS_DATA/datasets/openviic/uit-openviic-annotation-dev.json` (OV-dev-A and OV-dev-B) and `$NCS_DATA/datasets/c_xm_dev500/xm_dev500_data.json` (XM-dev500), checked by the readers' own id rules. These files, the segmenter folder and the memory annotations were **not verified on the host** by the coder, who was barred from `/root/ncs-data`. On 2026-11-12, Java answered rc 0 on the host | STOP at verify or at the first score |
| Python | `/root/vsps/.venv/bin/python` (the host has no `venv-c1score`). The sha256 of its package list goes into `VERIFY.json`; every later stage requires the same environment. A failed import is a STOP: nothing is installed without a judge line | STOP |
| stored runs | every `.preds.json` of `STORED_SHA256` present under `/root/outputs/c_stage1`, `c_stage2`, `c_t1` and equal to its pin. A missing file is restored from the laptop backup and checked against its pin | STOP at verify |
| optional, for `posthoc` only | `in/blind/`: the stage-2 image-blind runs, admitted only when their sha256 equals the `run_sha256` of the pinned stage-2 ledger. `in/carve/carve_coco.jsonl`: `4ced15b4…`, checked. `in/carve/carve_f30k.jsonl` has no committed pin, so its sha256 is logged before `posthoc`. `in/carve/runs/`: the four carve `ret` / `rand` d0 runs of each backbone, used for rule L | rows NOT RUN, reported |

## 1. Sequence (one call per stage; `H` = the pre-score commit; every call runs under `nice -n 19`, CPU only)

| step | command | writes | gate before the next step |
|---|---|---|---|
| 0 | `bash scripts/c_attr/c_attr_score_job.sh H selftest`; `/root/venv-lb/bin/python -I -B scripts/c_attr/c_attr.py --selftest`; `/root/vsps/.venv/bin/python -I -B scripts/c_attr/c_attr_mutants.py --no-netns --jobs 4` | `logs/selftest.log`, mutant log | `SELFTEST OK`; four "selftest ok" lines; "73/73 killed; survived: none". The mutant record is not network-isolated (CC-346 flag a) |
| 1 | `bash scripts/c_attr/c_attr_score_job.sh H verify --b1-sums B1SUMS --b-sums BSUMS` | read-only copies `in/b1`, `in/b`; `res/VERIFY.json` | the copies equal the logged sums (only `logs/job.log` exempt, no unlisted file); stored pins; jar; environment record; SC5 (every `-b1` run's per-image prompt sha256 equals that of the batched or stored run of the same backbone, set, arm and draw; counts only); §7.1 parity (C's six stage-2 OV-dev-B runs re-scored equal the stage-2 ledger within 1e-4). **The operator logs the sha256 of `VERIFY.json` (OPS line). STOP** |
| 2 | `… ova --prev <VERIFY sha>` (V4 step 1) | `led/ova.jsonl`, `res/c_attr_nomination.json`, `res/STAGE_ova.json` | batch-1 OV-dev-A rows of the D1-PASS nominators only. SC4: the four columns (ret, rand d0, perm p1, p2) of every D1-PASS nominator are present. **The operator logs the nomination sha256 before any other step. STOP** |
| 2′ | instead of 2, under the release clause: `… close --prev <VERIFY sha> --reason "<reason>"` | the empty v1.2 nomination file | **OPS line "1b closed: <reason>" with its sha256. STOP.** Then go to step 4 with this sha |
| 3 | `… ovb --prev <nomination sha>` (V4 step 2; one look) | `led/ovb.jsonl`, `res/VERDICT.json` (summary of both batch-1 sets), `res/DFSENS.json` | §9 row: Qwen2.5-VL τ_pair and τ_marg, document frequencies recomputed in the first 200 rows of OV-dev-B's shared index matrix, the fixed-df interval beside it. Its full-df scores must equal the ledger's. **The operator logs the sha256 of VERDICT and DFSENS. STOP** |
| 4 | `… rest --prev <VERDICT sha>` (V4 step 3; under the release, the empty nomination sha) | `led/xm_b1.jsonl`, `led/bat_<set>.jsonl`, `res/SUMMARY.json` | XM-dev500 at batch 1. Every batched block-1 output with the stored runs of its set; batched rows carry "A1 not met; batched decode; descriptive", no family. **The operator logs the SUMMARY sha256. STOP** |
| 5 | `… posthoc --prev <SUMMARY sha>` | `res/COPYBOUND_<set>_<model>.json`, `res/POSTHOC.json` | the copy bound (§8, units i and ii, n = 2/3/4, the companions K_rand, K_ret − K_nc and the blind loss, descriptive), POST HOC except κ on XM-dev500 (first look). The swap δ (§7.9) on the stored carve cells is POST HOC and size-confounded, with rule L. **The operator logs the POSTHOC sha256** |

Labels as registered: batch-1 rows carry "batch size 1; registered in v1.2 after K1 fired, on string-identity counts only". τ_pair and τ_marg on OV-dev-A/B carry "split of a known τ_sel". τ_sel at batch 1 on OV-dev-A/B carries "batch-1 re-decode of a known τ_sel" and stays outside every family.

## 2. STOP rules

- A `SCORE STOP`, a `REFUSED`, a parity failure (§7.1 at verify, §9 at ovb) or a non-zero return code stops scoring. Nothing is re-run with changed inputs, and the matter goes to the judge. A failed `verify` leaves a partial `in/`, which is removed only after a judge line.
- The `--prev` value is copied from the LOG line, never from the terminal. A stage whose `--prev` does not match the file stops (V4 order). Every stage runs once.
- No byte under `scripts/c_attr/` changes between step 0 and step 5. The wrapper checks HEAD, the tracked tree and `SHA256SUMS` at every call.
- A D1 FAIL in any `STEP1B0` file removes that backbone, whatever the order of the files (SC3).
- No stage runs while `RUNNING` exists under `/root/outputs/c_attr` or `/root/outputs/c_attr_b1` (§6.7).
- Never on the laptop: the laptop runs no stage and opens no ledger before the pull.

## 3. Pull

After step 5, or after any STOP, pull `/root/c_attr_score/res/`, `led/` and `logs/`; they hold ids, numbers and labels only. Check each logged sha256 and the whole-folder digest, then store a 444 copy under `.session_backup/machines/<host>/root/c_attr_score/`. The `in/` copies hold captions and are not pulled again, because the laptop already holds their 444 originals. The host is then handled under PI-1109g (keep the queue full, or back it up and delete it).

## 4. Not covered here

Blocks 2–4. The English copy bound (Flickr30K carve and val, unit i, PTB CIDEr-D) is not coded. A second-host tree (h2) needs an addendum to this document.
