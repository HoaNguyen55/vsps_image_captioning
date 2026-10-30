#!/bin/bash
# MT4 Branch K1+K6 dev rule (manuscript/prereg/2026-10-30_mt4_k1k6/PREREG_DRAFT.md). One job, three tiers, m3 role (M1)
# only. The K2 Gate 1 job's patterns: HEAD + clean tree, tmux, one lock, venv freeze + pip check, snapshot pins, guard
# before every GPU step, ledger start line (fsynced, full-timeout charge if left open), fresh partials, .done shas.
#   TIER=1 EXPECT_HEAD=<commit> GPU=m3 bash scripts/mt4_k1k6/k1k6_job.sh    tier 1: val 924, fixes (a)-(d)
#   TIER=2 EXPECT_HEAD=<commit> GPU=m3 bash scripts/mt4_k1k6/k1k6_job.sh    tier 2: confirmatory seeds + T2 rehearsal
#   TIER=3 EXPECT_HEAD=<commit> GPU=m3 bash scripts/mt4_k1k6/k1k6_job.sh    tier 3: the KV decodes (after a T2_PASS)
#   TIER=3 SCORE=1 EXPECT_HEAD=<commit> GPU=m3 bash scripts/mt4_k1k6/k1k6_job.sh   the one look, after the freeze instant
#   bash scripts/mt4_k1k6/k1k6_job.sh --selftest                                    CPU, repo root
set -euo pipefail
H_Q3=2bb7397e7db350a2c225df590cdd9531df6a3247f7a3f217e1b64ed2d9f1be80   # venv_q3_freeze.txt (W22 PREREG §8)
D=scripts/mt4_k1k6; P=manuscript/prereg/2026-10-30_mt4_k1k6
PY=/root/vsps/.venv/bin/python; [ -x $PY ] || PY=python3
if [ "${1:-}" = "--selftest" ]; then
  bash -n "$0"
  $PY $D/k1k6.py --selftest
  sha256sum --quiet -c $D/SHA256SUMS
  ! grep -qE '[|] *t[e]e' "$0" || { echo "a tee pipe masks exit codes (the N9 bug)"; exit 1; }
  [ "$(grep -cE '^ *step [^#]*partial[.]jsonl" --' "$0")" = 1 ] && [ "$(grep -c '[$]X decode' "$0")" = 1 ] \
    || { echo "a decode runs outside dec(), the one step with a fresh partial"; exit 1; }
  r=0; out=$(GPU=m4 TIER=1 EXPECT_HEAD=x bash "$0" 2>&1) || r=$?
  [ "$r" = 1 ] && [[ $out == *"m3 role"* ]] || { echo "GPU=m4 was not refused"; exit 1; }
  echo "k1k6_job selftest ok"
  exit 0
fi
[ "${GPU:-}" = m3 ] || { echo "REFUSED: K1/K6 runs on the m3 role (M1) only; GPU=${GPU:-unset}"; exit 1; }
TIER=${TIER:?set TIER=1, 2 or 3}
cd /root/vsps
export NCS_DATA=/root/ncs-data HF_HUB_OFFLINE=1 TRANSFORMERS_OFFLINE=1 PYTORCH_CUDA_ALLOC_CONF=expandable_segments:True
HEAD=${EXPECT_HEAD:?set EXPECT_HEAD to the commit holding the dev rule and its gate ids}
VQ=/root/venv-q3/bin/python; X=$D/k1k6.py
S8=/root/ncs-data/models/Qwen3-VL-8B-Instruct-0c351dd; S4=/root/ncs-data/models/Qwen3-VL-4B-Instruct-ebb281e
DATA=$NCS_DATA/datasets/k1k6_pool; UV=$NCS_DATA/datasets/uitviic; VAL=manuscript/prereg/2026-10-21_dev_pools/uitviic_val.tsv
ANN=$NCS_DATA/datasets/coco_probe/annotations   # instances_val2014.json (pin e1b4d1bc), O-5
O=/root/outputs/mt4_k1k6; LOCK=$O/RUNNING; L=$O/gpu_seconds.tsv
[ "$(tr -d '[:space:]' < /root/.vsps_machine_id)" = m3 ] || { echo "REFUSED: this host is not the m3 role"; exit 1; }
[ "$(git rev-parse HEAD)" = "$HEAD" ] || { echo "REFUSED: HEAD is not $HEAD"; exit 1; }
git diff --quiet HEAD -- || { echo "REFUSED: tracked files differ from HEAD"; exit 1; }
[ -n "${TMUX:-}" ] || { echo 'REFUSED: run inside a tmux session'; exit 1; }
[ "$(tmux ls 2>/dev/null | wc -l)" = 1 ] || { echo "REFUSED: another tmux session exists"; exit 1; }
OTHER=$(ls /root/outputs/*/RUNNING 2>/dev/null || true)
[ -z "$OTHER" ] || { echo "REFUSED: a lock exists: $OTHER"; exit 1; }
mkdir -p "$O"; touch "$L"
( set -o noclobber; echo "$0 tier $TIER $(date -u +%FT%TZ)" > "$LOCK" ) || { echo "REFUSED: $LOCK exists"; exit 1; }
trap 'rm -f "$LOCK"' EXIT
echo "$(date -u +%FT%TZ) start tier $TIER head $HEAD" >> "$O/runs.log"
fault() { echo "$(date -u +%FT%TZ) FAULT tier $TIER: $1" > "$O/K1K6_FAULT_$(date -u +%Y%m%dT%H%M%SZ).txt"; echo "FAULT: $1" >> "$O/runs.log"; echo "K1/K6 NOT RUN (fault) -> TO-PI: $1"; exit 0; }
cost() { echo "$(date -u +%FT%TZ) NOT-RUN (cost) tier $TIER: $1" > "$O/K1K6_COST.txt"; cat "$O/K1K6_COST.txt" >> "$O/runs.log"; exit 0; }
[ ! -e "$O/K1K6_COST.txt" ] || { echo "STOP: a cost stop closed this branch (TO-PI)"; exit 1; }
# CPU checks: selftest, venv freeze, snapshots, gate ids committed at HEAD
bash $0 --selftest >> "$O/runs.log" 2>&1 || fault "selftest"
[ -x $VQ ] || fault "$VQ missing (built by setup_gpu.sh, never here)"
[ "$($VQ -m pip freeze | sha256sum | cut -c1-64)" = "$H_Q3" ] || fault "venv-q3 freeze differs from ${H_Q3:0:8}"
$VQ -m pip check >> "$O/runs.log" 2>&1 || fault "venv-q3 pip check"
$PY scripts/w22_sft/w22_sft.py snapcheck --snapshot $S8 >> "$O/runs.log" 2>&1 || fault "8B snapshot pins"
for f in model-00001-of-00002.safetensors model-00002-of-00002.safetensors; do   # 4B LFS pins (k1k6.SNAP_4B_LFS)
  $PY -c "import sys,hashlib; sys.path.insert(0,'$D'); import k1k6; h=hashlib.sha256(open('$S4/$f','rb').read()).hexdigest(); sys.exit(h!=k1k6.SNAP_4B_LFS['$f'])" \
    || fault "4B snapshot $f differs from its pin (K6 is dropped only by a ruling, PREREG §5 l.92)"
done
case $TIER in 1) need="W25K1 COST";; 2) need="W25K1 COST T1 AMEND2";; 3) need="W25K1 COST T1 AMEND2 T2";; *) fault "TIER $TIER";; esac
for k in $need; do
  $PY -c "import sys; sys.path.insert(0,'$D'); import k1k6; sys.exit(bool(k1k6.gates_missing(('$k',))))" \
    || fault "HELD: gate $k has no LOG id in $P/GATES.json at HEAD (pattern (OPS|CC|PI)-dddd...; AMEND2 missing = HELD -> TO-PI)"
done
# W7: the dev rule and its lists are pinned and committed (prereg-folder SHA256SUMS, written by the gatekeeper)
git cat-file -e "HEAD:$P/DEV_RULE.md" 2>/dev/null && grep -q ' DEV_RULE.md$' "$P/SHA256SUMS" || fault "HELD: DEV_RULE.md not committed and pinned"
(cd "$P" && sha256sum --quiet -c SHA256SUMS) || fault "a pinned prereg file differs from $P/SHA256SUMS"
git cat-file -e "HEAD:$P/w25k1_excluded_keys.txt" 2>/dev/null || fault "HELD: W25-K1 exclusions not committed"
[ -s "$O/pool.tsv" ] || $PY $X pool --data "$DATA" --out "$O/pool.tsv" >> "$O/runs.log" 2>&1 || fault "pool manifest"
G() { $PY $X guard "$HEAD" --tier "$TIER" --pool "$O/pool.tsv" >> "$O/runs.log" 2>&1; }
G || fault "guard refused"
# W8: the W25-K1 pass (laptop CPU) is charged to the test line once, at its 5.4 h cap
grep -q '^w25k1 ' "$L" || $PY scripts/k2_gate1/k2_gate1.py ledger --ledger "$L" --line "w25k1 19440" || fault "ledger w25k1"
export VSPS_MACHINE_ID=m3 VSPS_JOB_SHA256="$(sha256sum "$0" | cut -c1-64)" VSPS_VENV_FREEZE_SHA256=$H_Q3
step() {  # step NAME PARTIAL -- command...   (skipped when NAME.done matches; returns 1 when the stage is cut)
  # DESC=1: the descriptive K1 detailed KV row; a short remainder or exit 124 skips it, never a cost stop (CC-175 W2)
  local name=$1 part=$2 t rc=0 t0; shift 3
  if [ -s "$O/$name.done" ] && (cd "$O" && sha256sum -c --status "$name.done" 2>/dev/null); then
    echo "$(date -u +%FT%TZ) $name reused (sha matches)" >> "$O/runs.log"; return 0
  fi
  t=$($PY $X left --ledger "$L" --stage "$name" --caps "$CAPS") || rc=$?
  [ "$rc" = 4 ] && fault "HELD: $name would end after D_K"
  [ "$rc" = 6 ] && fault "ledger: an open start before $name (charged in full; rerunnable)"
  if [ "$rc" = 5 ]; then echo "$(date -u +%FT%TZ) $name cut by caps.json (ladder or remainder)" >> "$O/runs.log"; return 1; fi
  [ "$rc" = 0 ] || fault "left exit $rc before $name"
  if [ "${DESC:-0}" = 1 ] && [ "$t" -lt "$(cap_s "$name")" ]; then
    echo "$(date -u +%FT%TZ) $name (descriptive) not run: $t s left < its cap" >> "$O/runs.log"; return 1
  fi
  [ "$t" -gt 0 ] || cost "test line spent before $name"
  G || fault "guard refused before $name"
  [ -z "$part" ] || rm -f "$part"   # every attempt starts from zero (CC-162a F1)
  t0=$(date +%s)
  $PY scripts/k2_gate1/k2_gate1.py ledger --ledger "$L" --line "$name start $t0 $t" || fault "ledger start $name"
  timeout "$t" "$@" >> "$O/$name.log" 2>&1 || rc=$?
  $PY scripts/k2_gate1/k2_gate1.py ledger --ledger "$L" --line "$name $(( $(date +%s) - t0 ))" || fault "ledger end $name"
  if [ "$rc" = 124 ] && [ "${DESC:-0}" = 1 ]; then echo "$(date -u +%FT%TZ) $name (descriptive) hit its cap" >> "$O/runs.log"; return 1; fi
  [ "$rc" = 124 ] && cost "exit 124 in $name ($t s)"
  [ "$rc" = 0 ] || fault "$name exit $rc"
}
cap_s() { $PY -c "import json; print(round(json.load(open('$CAPS'))['cap_h']['$1'] * 3600))"; }
done_sha() { (cd "$O" && sha256sum "${@:2}" > "$1.done"); }
dec() {  # dec STAGE MODEL MODE NNEW MANIFEST IMAGES OUT [ADAPTER]
  local AD=(); [ -z "${8:-}" ] || AD=(--adapter "$8")
  step "$1" "$O/$7.partial.jsonl" -- $VQ $X decode --model $2 --mode $3 --n-new $4 "${AD[@]}" --manifest $5 --images $6 --out "$O/$7" \
    || return 1
  done_sha "$1" "$7"
}
if [ "$TIER" = 1 ]; then
  CAPS=$O/caps_plan.json; [ -s "$CAPS" ] || $PY $X plan --out "$CAPS" >> "$O/runs.log" 2>&1 || cost "planning caps exceed the test line"
  [ -s "$O/probe.tsv" ] || $PY scripts/k2_gate1/k2_gate1.py manifest --set probe --out "$O/probe.tsv" || fault "probe manifest"
  dec t1_timing 8b detailed 512 "$O/probe.tsv" "$UV/images" k1k6_t1_timing-detailed.preds.json
  step t1_train "" -- $VQ $X train --model 8b --seed 0 --epochs 3 --save-epochs --pool "$O/pool.tsv" --data "$DATA" --out-dir "$O/t1" \
    || fault "t1_train cut"
  done_sha t1_train t1/train.json t1/epoch1/adapter_model.safetensors t1/epoch2/adapter_model.safetensors t1/epoch3/adapter_model.safetensors
  dec t1_dec_base8_s 8b short 160 $VAL "$UV/images" k1k6_t1_base8_s-short.preds.json
  for e in 1 2 3; do dec t1_dec_e$e 8b short 160 $VAL "$UV/images" k1k6_t1_e$e-short.preds.json "$O/t1/epoch$e"; done
  [ -s "$O/t1_select.json" ] || $PY $X t1select --dir "$O" >> "$O/runs.log" 2>&1 || fault "t1select"
  $PY - "$O" > "$O/rates.json" <<'EOF' || fault "rates"
import json, sys; from pathlib import Path
o = Path(sys.argv[1]); r = lambda f: json.loads((o / f).read_text())
print(json.dumps({"train_8b": r("t1/train.json")["s_per_example"],
                  "short": max(r(f"k1k6_t1_{s}-short.preds.json")["s_per_image_decode"] for s in ("base8_s", "e1", "e2", "e3")),
                  "detailed": r("k1k6_t1_timing-detailed.preds.json")["s_per_image_decode"]}))
EOF
  rc=0; $PY $X plan --rates "$O/rates.json" --t1 "$O/t1_select.json" --out "$O/caps.json" >> "$O/runs.log" 2>&1 || rc=$?
  [ "$rc" = 2 ] && cost "measured caps exceed the test line after the ladder"
  echo "$(date -u +%FT%TZ) tier 1 done: t1_select.json + caps.json for the gatekeeper" >> "$O/runs.log"
fi
if [ "$TIER" = 2 ]; then
  for f in t1_select.json caps.json; do   # W4: both committed with the T1 gate and equal to the M1 copies
    git cat-file -e "HEAD:$P/$f" 2>/dev/null || fault "HELD: $f not committed"
    [ "$(git show HEAD:$P/$f | sha256sum | cut -c1-64)" = "$(sha256sum < "$O/$f" | cut -c1-64)" ] || fault "$f differs from HEAD"
  done
  CAPS=$P/caps.json
  read -r E NS V < <($PY -c "import json; r=json.load(open('$O/t1_select.json')); print(r.get('epochs',0), r['n_short'], r['verdict'])")
  [ "$V" = T1_OK ] || fault "tier 1 verdict $V: no tier 2 (TO-PI)"
  for s in 1 2; do
    step train_k1_s$s "" -- $VQ $X train --model 8b --seed $s --epochs $E --pool "$O/pool.tsv" --data "$DATA" --out-dir "$O/k1_s$s" \
      && done_sha train_k1_s$s k1_s$s/train.json k1_s$s/adapter_model.safetensors
  done
  step train_k6_s1 "" -- $VQ $X train --model 4b --seed 1 --epochs $E --pool "$O/pool.tsv" --data "$DATA" --out-dir "$O/k6_s1" \
    && done_sha train_k6_s1 k6_s1/train.json k6_s1/adapter_model.safetensors
  [ -s "$O/t2.tsv" ] || { $PY $X stage --set t2 --ann "$ANN" --out "$O/t2.tsv" >> "$O/runs.log" 2>&1 || fault "T2 staging"; G || fault "guard after T2 staging"; }
  T2I=$NCS_DATA/datasets/k1k6_t2/images
  dec t2_short_base8_s 8b short $NS "$O/t2.tsv" $T2I k1k6_t2_base8_s-short.preds.json
  dec t2_short_k1_s1 8b short $NS "$O/t2.tsv" $T2I k1k6_t2_k1_s1-short.preds.json "$O/k1_s1"
  dec t2_short_k1_s2 8b short $NS "$O/t2.tsv" $T2I k1k6_t2_k1_s2-short.preds.json "$O/k1_s2" || true   # cut by the ladder
  dec t2_short_k6_s1 4b short $NS "$O/t2.tsv" $T2I k1k6_t2_k6_s1-short.preds.json "$O/k6_s1" || true   # cut by the ladder
  dec t2_detailed_base8_s 8b detailed 512 "$O/t2.tsv" $T2I k1k6_t2_base8_s-detailed.preds.json
  dec t2_detailed_k6_s1 4b detailed 512 "$O/t2.tsv" $T2I k1k6_t2_k6_s1-detailed.preds.json "$O/k6_s1" || true   # cut by the ladder
  git cat-file -e "HEAD:$P/t2_gold.json" 2>/dev/null || fault "HELD: t2_gold.json not committed (k1k6.py gold --set t2)"
  [ -s "$O/t2_decide.json" ] || $PY $X t2decide --dir "$O" >> "$O/runs.log" 2>&1 || fault "t2decide"
  echo "$(date -u +%FT%TZ) tier 2 decided: t2_decide.json for the gatekeeper's anchor" >> "$O/runs.log"
fi
if [ "$TIER" = 3 ]; then
  CAPS=$P/caps.json
  [ "$(git show HEAD:$P/caps.json | sha256sum | cut -c1-64)" = "$(sha256sum < "$CAPS" | cut -c1-64)" ] || fault "caps.json differs from HEAD"
  $PY $X kvready --dir "$O" > "$O/kv_kept.json" 2>> "$O/runs.log" || fault "kvready refused (no anchored T2_PASS, or not M1)"
  if [ "${SCORE:-0}" = 1 ]; then
    $PY $X kvscore --dir "$O" >> "$O/runs.log" 2>&1 || fault "kvscore (HELD before the freeze instant, or a FAULT)"
    exit 0
  fi
  [ -s "$O/kv.tsv" ] || { $PY $X stage --set kv --ann "$ANN" --out "$O/kv.tsv" >> "$O/runs.log" 2>&1 || fault "KV staging"; G || fault "guard after KV staging"; }
  KVI=$NCS_DATA/datasets/k1k6_kv/images; NS=$($PY -c "import json; print(json.load(open('$O/t1_select.json'))['n_short'])")
  while read -r M S; do
    case $S in k6_*) MOD=4b;; *) MOD=8b;; esac
    AD=""; [ "$S" = base8_s ] || AD="$O/$S"
    NN=$NS; [ "$M" = detailed ] && NN=512
    F=k1k6_kv_$S-$M.preds.json
    dec kv_${M}_$S $MOD $M $NN "$O/kv.tsv" $KVI $F $AD || fault "kv_${M}_$S cut although kept (caps.json and kv_kept disagree)"
    grep -q "  $F  " "$P/KV_PRED_SUMS" 2>/dev/null || $PY $X kvsums --pred "$O/$F" --system "$M:$S" || fault "kvsums $F"
  done < <($PY -c "import json; k=json.load(open('$O/kv_kept.json')); [print(m, s) for m in k for s in k[m]]")
  F=k1k6_kv_k1_s1-detailed.preds.json   # the descriptive row: last, from what is left, outside the kept set (W1, W2)
  if DESC=1 dec kv_detailed_k1_s1 8b detailed 512 "$O/kv.tsv" $KVI $F "$O/k1_s1"; then
    grep -q "  $F  " "$P/KV_PRED_SUMS" 2>/dev/null || $PY $X kvsums --pred "$O/$F" --system "detailed:k1_s1" || fault "kvsums $F"
  fi
  rm -rf "$NCS_DATA/datasets/k1k6_kv"; echo "$(date -u +%FT%TZ) deleted $NCS_DATA/datasets/k1k6_kv after the KV decodes" >> "$O/deletions.log"
  G || fault "guard after KV cleanup"
fi
