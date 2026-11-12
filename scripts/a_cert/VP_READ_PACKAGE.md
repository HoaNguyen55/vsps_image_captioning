# A-CERT VP read package (Part V and Part P; for the one-judge code read, CC-335 Ruling 8)

Spec: `manuscript/prereg/2026-11-11_a_cert/A_CERT_ADDENDUM_VP_v1_1.md` (`0e586fa9…`, commit bd7ef1c). Synthetic
fixtures only so far (CC-335 item (2)). Nothing here is committed.

## 1. Files (sha256)

| File | sha256 | Status |
|---|---|---|
| `scripts/a_cert/a_cert_vp.py` | `867a5974be2dad823db8cc018658b2151a42494bdc6b877f1a8429044c28f5d5` | new, to read |
| `scripts/a_cert/a_cert_vp_mutants.py` | `a29ff113a85e009a9ba03f68936b43990ad3f08f4dfdda9ea4f341bb4ec832d0` | new, to read |
| `scripts/a_cert/HOST_CHECKS_VP.md` | `dd3403f9ffa07f5c8ea5feef05ff4d027772dc557ea060b8c97808b0e485b58d` | host instructions |
| `scripts/a_cert/host_checks_vp2/*` | see `host_checks_vp2/SHA256SUMS_VP2CHK` | host records (KV0) |
| `scripts/a_cert/SHA256SUMS_VP_INPUTS` | listed in `SHA256SUMS_VP` | laptop sums of the 15 Part V inputs |
| `scripts/a_cert/a_cert.py` | `2e872588baf6109fad20111aecd25e2504fd0096f9033a95649027a2eed46cf4` | committed 44a2696, imported, not changed |
| `scripts/a_cert/a_cert_mutants.py` | `9d4d5916ecd884522d0b4e39c87665f93203584c86ed5368f2354bd9bb656227` | committed 44a2696, `main()` reused, not changed |

The binding to `a_cert.py` is by record, not by a constant. The self-test record stores the sha of `a_cert.py` it ran with.
Real modes refuse unless that sha equals the file at run time (KV0), and unless `a_cert_vp.py`, `a_cert.py` and the
addendum equal their HEAD blobs. `A_CERT_SCORE_S1_S4.diff` (11febfc→44a2696) adds score-side code only. No name that
`a_cert_vp.py` uses changed. These are: `Fault, certify, committed, corner, delta_min, ols, pair_cells, sha, w_star,
write_atomic, ALPHA_S, GRID, W0, P_REAL["log"], ROOT, SELF, beta_B, beta_H, null_select, pinned_freeze, refused`. Its
removed lines touch only `h2d_rule`'s result dict, `score_core`, `score` and `fixture`, and none of these is called. In
`a_cert_mutants.py` only the docstring and its own list `M` changed.

Host check (hc2, `/root/a_cert_tree`, CPU, `nice -n 19`, 2026-11-11 22:58–23:05 UTC):

| Check | Result | Record |
|---|---|---|
| Self-test | 89/89, `selftest ok` | `selftest_vp.json` `cb04a394…`, with `a_cert_sha256` = 2e872588… |
| Mutants | 39/39 killed | `mutants_result_vp.json` `e96e9fb4…`, with `source_sha256` = 867a5974… |

## 2. Modes

- `selftest --out F`: synthetic fixtures only.
- `v-freeze`: label-free. It writes `data/results/a_cert_v/freeze/FREEZE_V.json`.
- `v-score`: runs once after the LOG line `FREEZE_V <sha>`. It writes `data/results/a_cert_v/score/A_CERT_V_RESULT.json`.
- `p-fetch-check --logs DIR`: checks the 25 release files (size and git blob) and prints their sha256.
- `p-score`: POST HOC. It writes under `data/results/a_cert_p/` only.

Each real mode takes `--selftest S --mutants M` (KV0). Fault rule (v1.1 §12 step 5):
- Any exception writes `<out>/faults/FAULT_n.json` (type only) and exits with 2.
- A rerun with the same script sha is refused.
- A second fault refuses the run and sends the analysis to the PI (KV3).

## 3. Twelve places where the code takes the stricter reading

The earlier list was not saved to a file. These twelve are recovered from the code and checked against the addendum
text. Compare them with the list in the earlier report.

1. **§V.4a (w = 0 fault).** It covers more than the V-B grid verdict. A fault is also raised by:
   - a V-H verdict at w = 0, `w* = 0`, or the fine-grid minimum at 0 (`v4a`);
   - in Part P, `p_unit` (`w* = 0`) and `p_b_row` (a positives-only certificate at 0).
2. **§V.7 five-reference union.** `rung` raises a fault if the freeze draws k ≥ the image's reference count. Power at k = 5 is computed in `v-score`, before the instance gold is opened (`v_score_core`).
3. **§V.7 no-peek guard.** It is an audit hook on `open`, `listdir`, `scandir`, `rename` and `mkdir`. It refuses any path containing `instance_gold` in `v-freeze`, not only the pinned file.
4. **COCO K2.** ABSTAIN and NOT DEFINED units sit last in every ranking and count as failing the truth. The addendum states "excluded and counted" only for V1–V3.
5. **Cross-fitted floor (secondary).** If no w in 0.01–0.99 meets α_S on a half, w0 = 0 and nothing is certified there (`calibrate`, `at_floor`).
6. **P-b.** `I0 > ⌊β⌋` in any one cell of a pair leaves the whole pair NOT CERTIFIED at that w. If that holds at `w*`, `w*` is printed as `NI (floor refuted by the instance labels)` (`pb_verdict`, `pb_wstar`).
7. **§P.2 matcher gate.** "To the printed precision" is read as exact equality with the stored values.
8. **§P.1 fetch.** Any file under `--logs` that is not in the list fails `p-fetch-check`. `p-score` also requires each release sha256 to appear in the LOG.
9. **`p-score` LOG check.** It refuses unless the LOG holds a `PI-1111i` line and the Part V result sha. The `gt_cache.json` prefix `f986f8ff` and the stored E1 rows (`184f9cca…`) must also match.
10. **Custody.** Paths are refused as follows:
    - `gt_cache.json`: in every mode except `p-score` with `--allow-gt-cache`;
    - the OC1 raw logs, label directories and sealed paths: always;
    - XM3600 and OC1 frozen inputs (`P_DENY`): in Part P.

    Part P may write only under its own output directory.
11. **Fault rule.** The fault record holds the exception type only, and nothing is printed beyond `FAULT <type>`. A rerun with the same script sha is refused. A second fault stops the analysis (KV3).
12. **KV0.** It needs a passing self-test record that binds both `a_cert_vp.py` and `a_cert.py`, and a mutant record with every mutant killed. It also needs HEAD-blob equality for the script, `a_cert.py` and the addendum. `v-score` further requires the input pins and the code pins to equal those in FREEZE_V. Under KV1, Part P drops every CERTIFIED share, the aggregate, the 94-pair V1–V3 and the transported threshold, and prints `w*` only.

## 4. Host dependencies

- Python is `/root/vsps/.venv/bin/python -I -B`. The only third-party package is numpy. The `pycocoevalcap`, `py_vncorenlp`, `torch` and `transformers` imports inside `rescap` are lazy.
- Code:
  - `scripts/a_cert/{a_cert,a_cert_mutants,a_cert_vp,a_cert_vp_mutants}.py`
  - `scripts/g2b/score_g2b.py`, `scripts/score_coco_probe.py`, `scripts/xm3600_oiv7.py`, `scripts/clean_supervision.py`, `scripts/person_uncap.py`
  - the 25 tracked `rescap/` files
  - `.session_backup/2026-10-14/research_r10/E1/e1_chair_count.py`
- Small non-label files: `data/coco_probe/chair_synonyms.txt`, `data/coco_probe/coco80_vi.json` and the addendum.

## 5. Never run

The following have never run on any machine:
- real `v-freeze` and `v-score`;
- `p-fetch-check` on real files (the 25 public files have not been fetched);
- `p-score`.

Two more steps are also untried:
- the `committed()` gate has never returned True on the host;
- the checkout recipe of §6 has never been tried.

Only `selftest` and the mutant harness have run, on the host, against synthetic fixtures.

## 6. Real Part V run on the host (not licensed until the code read GO and commit; recipe untested)

The real modes call `committed()` (`git show HEAD:<file>` must equal the working file), so they cannot run in
`/root/a_cert_tree`, which is not a git checkout. Any failed check inside a run writes FAULT_1, and a rerun of the same
script is then refused. Every pre-check below must therefore pass before the first run.

The tree needs a git checkout whose HEAD holds `a_cert_vp.py`, `a_cert.py` and the addendum. There are two options;
**the coordinator decides which one:**
- **(a) Full checkout.**
  - Steps: `git bundle create vp.bundle <branch>` on the laptop, push the bundle, then `git clone -b <branch> vp.bundle /root/a_cert_vp_real`. Whether a bundle of `HEAD` alone checks out is unknown, so name the branch.
  - Consequence: `instance_gold_full5000.json` is tracked, so it reaches the host **before** the freeze, together with every other tracked file and the full history. The freeze's audit hook still refuses to open it.
- **(b) Minimal repo on the host.**
  - Steps: tar only the code of §4 and the freeze inputs, then `git init && git add -A && git commit` on the host.
  - Consequence: the instance gold stays off the host until after the pin. `committed()` then only proves that nothing was edited after that host commit. The binding to the laptop repo comes from the KV0 records and the `sha256sum -c` checks below.

| Repo path | sha256 (pin in code) | Kind | Mode | Git; pin checked 2026-11-12 on the laptop |
|---|---|---|---|---|
| `data/results/coco5000/distill-detailed.shard0of1.jsonl` | `6453bfd5…` | stored model outputs | freeze, score | tracked; match |
| `data/results/coco5000/distill-short.shard0of1.jsonl` | `12ab5a6e…` | stored model outputs | freeze, score | tracked; match |
| `data/results/coco5000/zeroshot-detailed.shard0of1.jsonl` | `96e15f40…` | stored model outputs | freeze, score | tracked; match |
| `data/results/coco5000/zeroshot-short.shard0of1.jsonl` | `15ca5615…` | stored model outputs | freeze, score | tracked; match |
| `data/results/coco_transfer_full5000/fuse2_s42-detailed.shard0of1.jsonl` | `f205805a…` | stored model outputs | freeze, score | tracked; match |
| `data/results/coco_transfer_full5000/fuse2_s42-short.shard0of1.jsonl` | `cd947944…` | stored model outputs | freeze, score | tracked; match |
| `data/results/coco_transfer_full5000/p1_s43-detailed.shard0of1.jsonl` | `b12fbeb9…` | stored model outputs | freeze, score | tracked; match |
| `data/results/coco_transfer_full5000/p1_s43-short.shard0of1.jsonl` | `b0dbbdc5…` | stored model outputs | freeze, score | tracked; match |
| `data/results/coco5000_vcd/zeroshot-detailed.shard0of1.jsonl` | `d6173e34…` | stored model outputs | freeze, score | tracked; match |
| `data/results/a_dchecks/freeze/coco5000_ids.txt` | `d20da3dd…` | image id list (no labels) | freeze, score | tracked; match |
| `data/datasets/karpathy/dataset_coco.json` | `2fd99922…` | public human reference captions (the incomplete gold that is certified against; 144 MB) | freeze, score | untracked, push; match |
| `data/results/a_dchecks/freeze/instance_gold_full5000.json` | `bd362951…` | **gold** (COCO instance classes, truth side) | **score only** | tracked; pin in code, **not checked** (push after the FREEZE_V pin under (b)) |
| `.session_backup/2026-10-13/decisions/LOG.md` | not pinned | decisions LOG; `pinned_freeze` needs its `FREEZE_V <sha>` line | score | untracked; push after the pin line |
| `data/results/a_cert_v/freeze/FREEZE_V.json` | its LOG pin | our freeze output | score | committed after the freeze |

The other four pinned files come with the code: `chair_synonyms.txt`, `coco80_vi.json`, `score_g2b.py` and
`score_coco_probe.py`. Their pins also match. All 15 laptop sums are in `SHA256SUMS_VP_INPUTS`, with paths relative to
the repo root.

Pre-check, then the commands, run from the checkout root:

```sh
cd /root/a_cert_vp_real && PY=/root/vsps/.venv/bin/python
sha256sum scripts/a_cert/a_cert.py scripts/a_cert/a_cert_vp.py      # expect 2e872588… and 867a5974…
sha256sum -c scripts/a_cert/SHA256SUMS_VP_INPUTS                     # 15 x OK
(cd scripts/a_cert/host_checks_vp2 && sha256sum -c SHA256SUMS_VP2CHK)
for f in scripts/a_cert/a_cert.py scripts/a_cert/a_cert_vp.py manuscript/prereg/2026-11-11_a_cert/A_CERT_ADDENDUM_VP_v1_1.md; do
  test "$(git show HEAD:$f | sha256sum | cut -c1-64)" = "$(sha256sum < $f | cut -c1-64)" || echo "NOT COMMITTED $f"; done
test -e data/results/a_cert_v || echo "no prior output or fault: ok"
R="--selftest scripts/a_cert/host_checks_vp2/selftest_vp.json --mutants scripts/a_cert/host_checks_vp2/mutants_result_vp.json"
OMP_NUM_THREADS=2 nice -n 19 $PY -I -B scripts/a_cert/a_cert_vp.py v-freeze $R
```

After `v-freeze`, the steps are:
1. Pull `FREEZE_V.json`, then hash it, set it to 444, commit it and write the LOG line `FREEZE_V <sha256>`.
2. Push the LOG (and, under (b), `instance_gold_full5000.json`). Check the gold against `bd362951…` on the host.
3. Run:

```sh
OMP_NUM_THREADS=2 nice -n 19 $PY -I -B scripts/a_cert/a_cert_vp.py v-score $R   # once
```

Part P needs extra inputs and a PI line, none of which exist yet:
- the 25 fetched files, under `--logs`;
- `.session_backup/2026-10-14/r12/H3/out/gt_cache.json` (**gold**, `f986f8ff…`), with `--allow-gt-cache` and a PI-1111i line;
- `.session_backup/2026-10-13/r10_cpu/e1_x1pb_verification_v2.json` (stored aggregate rows from the paper's earlier scoring, `184f9cca…`, untracked);
- the Part V result and its LOG pin.

## 7. Round 2 (CC-347 W1–W4; for the round-2 diff read)

Base: commit d13ae5c (`a_cert_vp.py` 867a5974…, `a_cert_vp_mutants.py` a29ff113…). The whole change is
`A_CERT_VP_W1_W4.diff` (`git diff d13ae5c -- scripts/a_cert/a_cert_vp.py scripts/a_cert/a_cert_vp_mutants.py`). Only
W1–W4 are in it. N2–N5 are NOT in it: the coder brief said "change nothing else", while CC-347 says the N items are
"carried into the round-2 diff where they touch code". The judge decides. Adding N2/N3/N5 later changes the script sha
again and needs new host records.

What changed:
- **W1 (Part V, before `v-freeze`).** New `xfit_v2(hu, info, w0h, beta)`. For each budget (V-B with `beta_Bk`,
  V-H with `beta_Hk`), every half unit with `better` not None and `w0h[half] > 0` adds the cells
  `(x_w, floor(beta(cells[worse], w0h[half], α_S, 2)))` and `(x_s, floor(beta(cells["S"], w0h[half], α_S, 2)))`;
  `xfit` adds `"V2": v2_rule(cells)` and `"n_half_units_excluded_floor_0"` to `cross_fit["V-B"]` and
  `cross_fit["V-H"]`. Reading: "excluded" counts every half unit of a half whose floor is 0 (including units without
  a direction). If both floors are 0, `v2_rule([])` gives `FLOOR REFUTED` with 0 cells, as the existing rule is worded.
- **W2 (Part P).** `p_row`: `c = cm` (method direction only), so `share_certified_w0 = cm/n`, the state sentence uses
  `cm`, the tail is added whenever `cm < n`, and the aggregate averages `cm/n`. New field
  `share_certified_w0_baseline_direction = cb/n`. `p_b_row`: `cert` needs `CERTIFIED` and `better == "A"` (the
  method); `certified_direction` keys on the verdict alone, so it keeps the baseline name. No new prose.
- **W3 (Part P).** `p_unit` takes the family's G_top `T`. For each k = 2 unit with a direction it stores the worse-only
  and S cells `(x_top under T on the pair's intersection, floor(beta_Bk(cell, W0, α_S, 2)))`. `p_score_core` adds
  `same_image_pairs["V2"] = {"label": P_FAMILY_LABEL, "k": 2, "w0": 0.2, "V2": v2_rule(...)}`; under KV1 it carries the
  same "not computed: KV1 …" text as `V1_V3`.
- **W4 (Part P).** `p_family`: `ids` = the union of the family's ids ∩ the images with an entry in gt_cache `inst`
  (E1's kept ids). `inter_idx` keeps only ids in that set (`if i in pos`), so the draws and every intersection use it.
  The matcher gate is unchanged. Fixture: image 105 (F-B) has no instance entry; the stored rows follow E1's rule.
- **Mutants.** M05's target line follows the new `inter_idx` line (same mutation: union for intersection). Five new
  mutants: `W1_V2_at_cross_fitted_floor_dropped`, `W2a_baseline_direction_counted_certified` (restores `c = cm + cb`),
  `W2b_Pb_baseline_direction_called_certified`, `W3_same_image_V2_x_top_under_drawn_gold`,
  `W4_units_include_images_without_instance_entry`.

New self-test checks (5): `V2_at_cross_fitted_floor_by_hand_and_on_fixture` (W1: by hand at w = 0.5, floor(β) = 10
at f1 = 0 and 13 at f1 = 3; on the fixture, both budgets have a non-zero floor, and `n_cells` and the excluded count
follow the half units), `P_baseline_direction_not_counted_as_certified` (W2: a `p_row` with 15 baseline and 5 method
certificates; a `p_b_row` whose certificate comes out of `certify` in the baseline direction),
`P_same_image_V2_worse_only_and_S_under_G_top` (W3, by hand: cells `[(1, 26), (0, 26)]`),
`P_KV1_suppresses_same_image_V2` (W3), `P_units_only_images_with_instance_entry` (W4: F-B pairs and gate `n_img` = 19).

Round-2 files (sha256):

| File | sha256 |
|---|---|
| `scripts/a_cert/a_cert_vp.py` | `17507200acd540fb967c1e11883800b29e138c6509bf04417df5e9c462229ff1` |
| `scripts/a_cert/a_cert_vp_mutants.py` | `815da83a1d5c4da0d733e3e25b08fdf3d82fd2a73d8e820c07cbbcd3e71f957c` |
| `scripts/a_cert/A_CERT_VP_W1_W4.diff` | listed in `SHA256SUMS_VP` |
| `scripts/a_cert/host_checks_vp3/*` | see `host_checks_vp3/SHA256SUMS_VP3CHK` |

Host check, round 2. Host: hc2, because the separate test host was deleted before it started. Tree:
`/root/a_cert_tree` with the two changed files pushed in, and the committed `a_cert.py` 2e872588… and
`a_cert_mutants.py` 9d4d5916…. Run: `/root/vsps/.venv/bin/python -I -B` (Python 3.12.3, numpy 2.5.4), CPU only,
`nice -n 19`, while `/root/outputs/c_attr_b1/RUNNING` existed, as CC-346 Ruling 6 allows. Runner: `run_vp3.sh`.
Times: 2026-11-12 03:50:56Z to 03:58:57Z. One earlier self-test of a draft ran at 03:49:18–03:49:29Z and failed one
check, because the W3 block label was overwritten; a second ran at 03:50:16–03:50:27Z and passed. Neither is a record.

| Check | Result | Record |
|---|---|---|
| VP self-test | 94/94 (89 + 5 new), `selftest ok` | `selftest_vp.json`, `script_sha256` 17507200…, `a_cert_sha256` 2e872588… |
| VP mutants | 44/44 killed (39 + 5 new). Each new mutant is killed by its named check, not by a crash. Only M07a is still a crash kill (CC-347 N5, not in this diff) | `mutants_result_vp.json`, `source_sha256` 17507200… |
| Main-study self-test (`a_cert.py selftest`, environment check of the host) | 92/92, `selftest ok` | `selftest_main_env.json` |

These records are made in the venv that holds the earlier records, `/root/vsps/.venv`. CC-347 Ruling 4(a) asks for the
round-2 records to come "on the host that will run Part V, in the venv that runs it". If Part V runs on a different
host or venv, the records have to be made again there.

### Host recipe for the real Part V run (CC-347 Ruling 4(b); W6)

1. **Push 1.** On the laptop: `git archive <commit of the W1–W4 code>` holding exactly:
   - the code paths of §4;
   - `scripts/a_cert/{SHA256SUMS_VP, SHA256SUMS_VP_INPUTS}` and `scripts/a_cert/host_checks_vp3/` (or the records made on the Part V host);
   - the addendum;
   - the 9 shards, `coco5000_ids.txt`, `chair_synonyms.txt` and `coco80_vi.json`.

   Send `data/datasets/karpathy/dataset_coco.json` (untracked) separately. **The instance gold is not in push 1.**
   Make a sha256 manifest of the archive on the laptop.
2. **On the host:**
   - extract into a NEW directory, then `git init; git add -A; git commit`;
   - `sha256sum -c` the laptop manifest: every line OK;
   - `sha256sum -c scripts/a_cert/SHA256SUMS_VP_INPUTS`: 15 OK;
   - addendum = 0e586fa9…, `a_cert.py` = 2e872588…, `a_cert_mutants.py` = 9d4d5916…;
   - run the HEAD-blob test of §6;
   - `test ! -e data/results/a_dchecks/freeze/instance_gold_full5000.json` and `test ! -e data/results/a_cert_v`.

   OPS line with the archive sha and the manifest sha.
3. **`v-freeze`**, under `timeout 3600 /usr/bin/time -v`, `OMP_NUM_THREADS=2`, `nice -n 19`, one process at a time,
   with OPS start and end lines. Stop at RSS > 8 GB or wall time > 60 min. On HC2 this may run only after
   `/root/outputs/c_attr_b1/RUNNING` is gone; until then, on a separate rented host.
4. **Pull `FREEZE_V.json`.** Laptop checks, all before the pin:
   - its sha equals the printed sha;
   - `FREEZE_V["code"]` equals the laptop HEAD sha of every listed file;
   - `FREEZE_V["pins"]` equals `SHA256SUMS_VP_INPUTS`;
   - `FREEZE_V["kv0"]` equals the record shas.

   Then hash it, `chmod 444`, gatekeeper commit, and a LOG line holding `FREEZE_V <full 64-hex sha256>`, the commit id
   and the KV-EV declaration.
5. **Push 2, only after the pin line:**
   - the instance gold, from `git show <commit>:data/results/a_dchecks/freeze/instance_gold_full5000.json`, checked on the host against `bd362951…`;
   - a LOG EXTRACT at the LOG path holding only the byte-copied pin line(s), never the whole LOG. Record its sha256 in the OPS line.

   Pre-flight:
   - the pin line is in the extract;
   - the gold is `bd362951…`;
   - FREEZE_V on the host has the pinned sha;
   - neither `data/results/a_cert_v/score` nor `data/results/a_cert_v/faults` exists.
6. **`v-score`**, once, under the same limits. A killed run is fault 1: an OPS line, then a judge line, before any rerun.
7. **After `v-score`.** Delete the gold and the LOG extract from the host. Pull the result, hash it, `chmod 444`,
   commit, and write a LOG line with `A_CERT_V_RESULT <full sha>`.

**Part P runs on the laptop, not on a rented host** (CC-347 Ruling 4(c)). `gt_cache.json` never leaves the laptop.
- The 25 files are fetched into a new empty directory outside the repo.
- Run `p-fetch-check`, then `p-score`, with `-I -B`, under `timeout 1200 /usr/bin/time -v`, `OMP_NUM_THREADS=2`, `nice -n 15`.
- Stop at 4 GB, and run only while the labelling server is idle.

**Supersedes (round 2).** The real modes take only the round-2 records: `host_checks_vp3/` or the records re-made on
the Part V host. The expected sha of `a_cert_vp.py` is now `17507200…`, not `867a5974…`. The `host_checks_vp2` paths
and the 867a5974 sha in §6 above and in `HOST_CHECKS_VP.md` §3 are superseded. With the vp2 records, `kv0` faults
inside `v-freeze` and writes `FAULT_1`.
