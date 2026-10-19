#!/bin/bash
# G2-B registered scoring (prereg 2026-10-18_g2b_qwen3vl_ladder; job set f942714; judge bindings CC-027): run the
# committed scripts/g2b/score_g2b.py ONCE on the 23 G2-B decodes, after the CC-027 pre-score checks. A second run is refused.
set -euo pipefail
REPO=/mnt/d/vsps_image_captioning
RUN=$REPO/.session_backup/2026-10-20/g2b_score
SRC=$REPO/.session_backup/machines/O-2308428/root/outputs/g2b_qwen3vl
OUT=data/results/g2b/g2b_score.json
LOG=$RUN/precheck.log
cd "$REPO"
[ -e "$RUN/RAN_ONCE" ] && { echo "REFUSED: the scorer already ran once" >&2; exit 3; }
[ -e "$OUT" ] && { echo "REFUSED: $OUT exists" >&2; exit 3; }
[ -e "$RUN/outputs" ] && { echo "REFUSED: $RUN/outputs exists; inspect it first" >&2; exit 3; }
: > "$LOG"
die() { echo "ABORT: $*" | tee -a "$LOG" >&2; exit 2; }
PY=(env -i HOME="$HOME" PATH=/usr/bin:/bin LANG=C.UTF-8 PYTHONDONTWRITEBYTECODE=1 OMP_NUM_THREADS=2
    OPENBLAS_NUM_THREADS=2 MKL_NUM_THREADS=2 NUMEXPR_NUM_THREADS=2 nice -n 15 python3)

# 1. Code, prereg and the PD-10 confirmation map are committed and unchanged at HEAD.
for f in scripts/g2b/score_g2b.py manuscript/prereg/2026-10-18_g2b_qwen3vl_ladder.json \
         manuscript/paperA_plan/CONFIRMATION_MAP.json manuscript/paperA_plan/CONFIRMATION_MAP.md; do
  git ls-files --error-unmatch "$f" > /dev/null 2>&1 || die "not tracked: $f"
  git diff --quiet HEAD -- "$f" || die "differs from HEAD: $f"
done

# 2. CC-027 pre-score checks on every registered run, then a sha-checked frozen copy in $RUN/outputs.
mkdir "$RUN/outputs"
python3 - "$SRC" "$RUN" <<'PY' >> "$LOG" || die "pre-score checks failed; see precheck.log"
import hashlib, json, shutil, subprocess, sys
from pathlib import Path
src, run = Path(sys.argv[1]), Path(sys.argv[2])
sha = lambda b: hashlib.sha256(b).hexdigest()
head = lambda p: subprocess.run(["git", "show", f"HEAD:{p}"], capture_output=True, check=True).stdout
reg = json.loads(head("manuscript/prereg/2026-10-18_g2b_qwen3vl_ladder.json"))
want = {"decoder_sha256": sha(head("scripts/g2b/decode_qwen3vl.py")),
        "job_sha256": sha(head("scripts/queue/jobs/m2_07_g2b_qwen3vl_ladder.sh"))}
rows, bad = {}, []
for r in reg["runs"]:
    rid = r["run_id"]
    f = src / f"{rid}.{'samples.jsonl' if r['sequences_per_image'] > 1 else 'preds.json'}"
    side = Path(f"{f}.sha256")
    if not (f.exists() and side.exists()):
        bad.append(f"{rid}: output or sidecar missing"); continue
    data = f.read_bytes()
    if side.read_text(encoding="utf-8").split()[0] != sha(data):
        bad.append(f"{rid}: sha differs from sidecar"); continue
    prov = json.loads(data.decode("utf-8").splitlines()[0]) if r["sequences_per_image"] > 1 else json.loads(data)
    probs = [f"{k} {prov.get(k)} != {v}" for k, v in want.items() if prov.get(k) != v]
    if prov.get("git_dirty") is not False:
        probs.append(f"git_dirty {prov.get('git_dirty')}")
    gh = str(prov.get("git_head"))
    if subprocess.run(["git", "merge-base", "--is-ancestor", "f942714", gh], capture_output=True).returncode != 0:
        probs.append(f"git_head {gh} does not contain f942714 (or is unknown here)")
    if probs:
        bad.append(f"{rid}: " + "; ".join(probs)); continue
    for p in (f, side):
        shutil.copy2(p, run / "outputs" / p.name)
    if sha((run / "outputs" / f.name).read_bytes()) != sha(data):
        bad.append(f"{rid}: copy differs"); continue
    rows[rid] = {"file": f.name, "sha256": sha(data), "git_head": gh, "generate_kwargs": prov.get("generate_kwargs"),
                 "n_images": prov.get("n_images"), "started_utc": prov.get("started_utc"),
                 "finished_utc": prov.get("finished_utc")}
    print(f"OK {rid} {sha(data)}")
summary = {"registered_runs": len(reg["runs"]), "checked_ok": len(rows), "problems": bad, "expected": want,
           "operator_list_note": "outputs/sha256/07_g2b_qwen3vl_ladder.sha256 lists only the 2 N9 provenance files the job "
                                 "stamped; decode integrity rests on each output's sidecar and its recorded provenance",
           "runs": rows}
(run / "precheck.json").write_text(json.dumps(summary, indent=1, sort_keys=True) + "\n", encoding="utf-8")
print(f"CHECKED {len(rows)}/{len(reg['runs'])} problems={len(bad)}")
sys.exit(1 if bad or len(rows) != len(reg["runs"]) else 0)
PY

# 3. Import preflight in a separate process: every repo file the scorer loads is tracked and equals HEAD.
"${PY[@]}" - > "$RUN/imports.txt" <<'PY'
import importlib.util, sys
from pathlib import Path
spec = importlib.util.spec_from_file_location("score_g2b", "scripts/g2b/score_g2b.py")
spec.loader.exec_module(importlib.util.module_from_spec(spec))
root = Path.cwd().resolve()
for m in sorted({Path(f).resolve() for v in list(sys.modules.values()) if (f := getattr(v, "__file__", None)) and Path(f).is_file()}):
    if root in m.parents:
        print(m.relative_to(root))
PY
echo scripts/g2b/score_g2b.py >> "$RUN/imports.txt"
while read -r f; do
  git ls-files --error-unmatch "$f" > /dev/null 2>&1 || die "imported file not tracked: $f"
  git diff --quiet HEAD -- "$f" || die "imported file differs from HEAD: $f"
done < "$RUN/imports.txt"
echo "IMPORTS $(wc -l < "$RUN/imports.txt") repo files, all tracked and equal to HEAD" >> "$LOG"

# 4. Run the registered scorer once.
PYV=$("${PY[@]}" -c 'import sys; print(sys.version.split()[0])')
NPV=$("${PY[@]}" -c 'import numpy; print(numpy.__version__)')
HEAD_SHA=$(git rev-parse HEAD)
touch "$RUN/RAN_ONCE"
T0=$(date -u +%FT%T.%3NZ)
set +e
"${PY[@]}" scripts/g2b/score_g2b.py score --outputs-dir "$RUN/outputs" --out "$OUT" > "$RUN/run.stdout" 2> "$RUN/run.stderr"
RC=$?
set -e
T1=$(date -u +%FT%T.%3NZ)
echo "RUN rc=$RC start=$T0 end=$T1 head=$HEAD_SHA python=$PYV numpy=$NPV" >> "$LOG"
[ $RC -eq 0 ] || die "scorer exited rc=$RC; see run.stderr. Report to the judge before any retry"
echo "DONE $(sha256sum "$OUT" | cut -c1-64)  $OUT" | tee -a "$LOG"
