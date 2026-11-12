# A-CERT VP host checks (addendum VP v1.1: Part V and Part P; written 2026-11-11)

PI rule 2026-11-11: no test runs on the laptop. Run these on the rented host (alias `hc2`) in the tree
`/root/a_cert_tree` (a tar-pushed copy, not a git checkout), python `/root/vsps/.venv/bin/python -I -B`, CPU only under
`nice -n 19`. Runs so far: `host_checks_vp/` (first run, `a_cert.py` working copy `92b11910…`) and `host_checks_vp2/`
(2026-11-11 22:58–23:05 UTC, against the committed `a_cert.py` `2e872588…` and `a_cert_mutants.py` `9d4d5916…`; runner
`run_vp2.sh` `c7952d3c…`). Only `host_checks_vp2/` counts for KV0.

Synthetic fixtures only (CC-335 item (2)). The self-test does not read COCO outputs, `dataset_coco.json`, the
instance gold, `gt_cache.json`, release logs or any label file. It writes its fixtures to a fresh system temp
directory and deletes it afterwards.

## 1. Files the self-test and mutants need on the host tree

Every path below must exist. The self-test's first check, `deps_present`, lists any that are missing.

New, untracked (copy them; `sha256sum -c SHA256SUMS_VP` in `scripts/a_cert/`):
- `scripts/a_cert/a_cert_vp.py`
- `scripts/a_cert/a_cert_vp_mutants.py`

Imported code:
- `scripts/a_cert/a_cert.py`, committed in 44a2696 as `2e872588baf6109fad20111aecd25e2504fd0096f9033a95649027a2eed46cf4`. Binding is by record, not by a constant in the code: the self-test record stores the `a_cert.py` sha it ran with, and `v-freeze`, `v-score` and `p-score` refuse to run unless that sha equals the file at run time (KV0) and the file equals its HEAD blob (`committed`). Its changes since 11febfc (`A_CERT_SCORE_S1_S4.diff`) add score-side code only; no name that `a_cert_vp.py` imports changed.
- `scripts/a_cert/a_cert_mutants.py`, committed in 44a2696 as `9d4d5916ecd884522d0b4e39c87665f93203584c86ed5368f2354bd9bb656227`. The VP harness runs its `main()` with `SRC` and `M` replaced. Since 11febfc only its docstring and its own mutant list `M` changed; `run` and `main` are unchanged.
- `scripts/g2b/score_g2b.py`, `scripts/score_coco_probe.py`, `scripts/xm3600_oiv7.py` (imported by score_g2b; it reads no data at import), `scripts/clean_supervision.py`, `scripts/person_uncap.py`
- the whole tracked `rescap/` tree (25 files):
  - `rescap/__init__.py`, `chair.py`, `metrics.py`, `metrics_svp.py`, `repro.py`, `viz.py`, `vocab.py`
  - `rescap/pipeline/{generate,realize,select,verify}.py`
  - `rescap/svp/{__init__,entailment,matching}.py`
  - `rescap/vi/{__init__,classifier,color,lexicon}.py`
  - `rescap/vlm/{__init__,base,mock,qwen_vl,registry,replay,vintern}.py`
- `.session_backup/2026-10-14/research_r10/E1/e1_chair_count.py` (tracked, `1e59ff12…`; E1's CHAIR matcher for Part P)

Small non-label data:
- `data/coco_probe/chair_synonyms.txt` (`b685537b…`): E1 opens it at import; score_coco_probe also reads it
- `data/coco_probe/coco80_vi.json` (`926e0857…`): score_g2b loads it at import
- `manuscript/prereg/2026-11-11_a_cert/A_CERT_ADDENDUM_VP_v1_1.md` (`0e586fa9…`): the wording labels are checked verbatim against it

Third-party: numpy only. The pycocoevalcap, py_vncorenlp, torch and transformers imports inside `rescap` are lazy.

Not needed, unlike the `a_cert.py` self-test: `evaluate_xm3600_predictions_v3.py`, `scripts/n_f1/bracket.py`,
`scripts/a_m1/a_m1.py` and `scripts/pascal50s/p50x.py`. `a_cert_vp.py` never calls `a_cert.test_mods`, `fixture`
or `_load_world`.

## 2. Self-test and mutants (host)

What was run for `host_checks_vp2/` is `run_vp2.sh` (in the tree; logs to `/root/outputs/a_cert_checks_vp2/`, mutant
scratch in `/root/outputs/a_cert_checks_vp2/mut/`). The block below is the generic form.

```sh
set -o pipefail
for f in scripts/a_cert/a_cert_vp.py scripts/a_cert/a_cert_vp_mutants.py scripts/a_cert/a_cert.py \
  scripts/a_cert/a_cert_mutants.py scripts/g2b/score_g2b.py scripts/score_coco_probe.py scripts/xm3600_oiv7.py \
  scripts/clean_supervision.py scripts/person_uncap.py .session_backup/2026-10-14/research_r10/E1/e1_chair_count.py \
  data/coco_probe/chair_synonyms.txt data/coco_probe/coco80_vi.json \
  manuscript/prereg/2026-11-11_a_cert/A_CERT_ADDENDUM_VP_v1_1.md; do test -f "$f" || echo "MISSING $f"; done
test "$(find rescap -name '*.py' | wc -l)" -ge 25 || echo "MISSING rescap files"   # the tree is not a git checkout
sha256sum scripts/a_cert/a_cert_vp.py scripts/a_cert/a_cert_vp_mutants.py   # compare with the first two lines of SHA256SUMS_VP
PY=/root/vsps/.venv/bin/python O=/root/outputs/a_cert_checks_vp2
# self-test: expect "selftest ok", 89 checks, exit 0
OMP_NUM_THREADS=2 nice -n 19 $PY -I -B scripts/a_cert/a_cert_vp.py selftest --out $O/selftest_vp.json > $O/selftest_vp.log 2>&1
# mutants: scratch dir outside the tree; expect "39/39 killed", exit 0 (each mutant reruns the self-test)
OMP_NUM_THREADS=2 nice -n 19 $PY -I -B scripts/a_cert/a_cert_vp_mutants.py $O/mut > $O/mutants_vp.log 2>&1
cp $O/mut/mutants_result.json $O/mutants_result_vp.json
```

The mutant run repeats the self-test 40 times; run it detached (`setsid nohup`), not in a foreground ssh. Pull the
logs, the two JSON records and `status.log` (not the mutated copies) to `scripts/a_cert/host_checks_vp2/` with a sums
file, and list them in `SHA256SUMS_VP`.

The self-test must not list, open or stat anything under `~/vsps_labels`, `~/.vsps_sealed`, `~/bpa1pull_1108`,
`.session_backup/machines/HBT1/` or `.session_backup/2026-10-27/a1_precheck/raw/`. The audit hook refuses all of
these, and the self-test only probes such paths inside its own temp directory.

## 3. Later real-data modes (NOT licensed yet)

The real-data modes may run only after the addendum commit, a one-judge code read (CC-335 Ruling 8) and the pins
of §V.7 / §P.1. Their arguments are the self-test and mutant records of `host_checks_vp2/`. They call `committed()`
(`git show HEAD:<file>`), so they must run in a git checkout that holds the committed VP code, not in the tar-pushed
`/root/a_cert_tree`; the exact steps are in `VP_READ_PACKAGE.md` §6.

```sh
PY=/root/vsps/.venv/bin/python; R="--selftest scripts/a_cert/host_checks_vp2/selftest_vp.json --mutants scripts/a_cert/host_checks_vp2/mutants_result_vp.json"
OMP_NUM_THREADS=2 nice -n 19 $PY -I -B scripts/a_cert/a_cert_vp.py v-freeze $R   # then hash, 444, commit, LOG pin "FREEZE_V <sha256>"
OMP_NUM_THREADS=2 nice -n 19 $PY -I -B scripts/a_cert/a_cert_vp.py v-score $R    # once; writes data/results/a_cert_v/score/
$PY -I -B scripts/a_cert/a_cert_vp.py p-fetch-check --logs <new empty dir with OPERA/... and less-is-more/...>
OMP_NUM_THREADS=2 nice -n 19 $PY -I -B scripts/a_cert/a_cert_vp.py p-score --logs <dir> \
  --gt-cache .session_backup/2026-10-14/r12/H3/out/gt_cache.json --allow-gt-cache \
  --v-result data/results/a_cert_v/score/A_CERT_V_RESULT.json $R
```

Inputs:
- `v-freeze` reads the nine shards of A2 plan §2.1, `data/results/a_dchecks/freeze/coco5000_ids.txt` and `data/datasets/karpathy/dataset_coco.json`, plus the code above. It never reads the instance gold.
- `v-score` additionally reads `data/results/a_dchecks/freeze/instance_gold_full5000.json` (`bd362951…`).
- `p-score` needs `.session_backup/2026-10-13/r10_cpu/e1_x1pb_verification_v2.json`. It is untracked (`184f9cca…`), so copy it to the host.
- The release logs go under `--logs` as `OPERA/<model>/<decoder>.jsonl` and `less-is-more/Table1-results/<run>.jsonl`, plus `less-is-more/chair-500.jsonl`. `p-fetch-check` prints their sha256 for the fetch LOG line. `p-score` refuses to run unless every one of those sha256, the Part V result sha and a `PI-1111i` line are in the LOG.
