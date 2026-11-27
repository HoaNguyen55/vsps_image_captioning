#!/usr/bin/env bash
# C-N3D host steps (rented host only; never a host that holds an OV-test byte, the C-CONF token or a C-CONF output).
#   host_selftest.sh selftest              synthetic self-tests + all mutants, byte-compile; opens no input
#   host_selftest.sh closure ROOT DATA     imports every instrument module from ROOT (PUSH LIST only) with python -I,
#                                          calls each instrument on synthetic strings, checks every loaded module pin
#   host_selftest.sh s0 ROOT DATA          the S0 record (W8 (i)): versions, pins, selftest, closure, listings
#   host_selftest.sh custody ROOT DATA     step 2 (PUSH LIST + every $NCS_DATA pin) + 2a (R2 counts; STOP if any > 0)
#   host_selftest.sh run ROOT DATA OUT     step 4 under a hard 4 h kill (CC-511 W4)
set -euo pipefail
HERE="$(cd "$(dirname "$0")" && pwd)"
PY="${PY:-python3}"
cd "$HERE"
sha256sum -c --quiet CODE.sha256          # the code read's hashes; any change is a STOP
need_host() { : "${VSPS_MACHINE_ID:?set VSPS_MACHINE_ID on the rented host}"; }
case "${1:-}" in
  selftest)
    "$PY" -I -B test_c_n3d.py
    "$PY" -I -B -c "import ast, sys; [ast.parse(open(f).read()) for f in sys.argv[1:]]" \
      c_n3d.py c_n3d_host.py test_c_n3d.py closure.py probe.py
    echo "selftest: ok" ;;
  closure)
    "$PY" -I -B probe.py "$2" "$3" --pins "$HERE/PUSH_LIST.sha256"
    echo "closure: ok" ;;
  s0)
    need_host
    {
      echo "S0 RECORD C-N3D  utc $(date -u +%Y-%m-%dT%H:%M:%SZ)  machine ${VSPS_MACHINE_ID}"
      echo "python: $("$PY" -c 'import sys; print(sys.version.split()[0])')  numpy: $("$PY" -c 'import numpy; print(numpy.__version__)')"
      echo "java: $(java -version 2>&1 | head -1)"
      echo "pip-freeze sha256: $("$PY" -m pip freeze 2>/dev/null | sha256sum | cut -c1-64)"
      echo "jar and segmenter models:"; sha256sum "$3"/vncorenlp/VnCoreNLP-1.2.jar "$3"/vncorenlp/models/wordsegmenter/*
      echo "CODE.sha256: ok ($(sha256sum CODE.sha256 | cut -c1-64))"
      "$PY" -I -B test_c_n3d.py
      "$PY" -I -B probe.py "$2" "$3" --pins "$HERE/PUSH_LIST.sha256" && echo "closure: ok"
      echo "files under ROOT not on the PUSH LIST (must be none):"
      comm -23 <(cd "$2" && find . -type f | sed 's#^\./##' | sort) <(grep -v '^#' PUSH_LIST.sha256 | awk '{print $2}' | sort)
      echo "forbidden names under ROOT and DATA (must be none):"
      { find "$2" "$3" -type f; } | grep -Ei 'c_t2/|c_t3/|CONF_H1|c_conf_r|/c_en/(runs|out)/|ledger|ov_test|xm_test|_test[_.]|nocaps|karpathy_test|f30k_val|f30k_test|/led/' \
        | grep -vxF "$2/manuscript/prereg/2026-10-25_c_test/ov_test_files.tsv" \
        | grep -vxF "$2/manuscript/prereg/2026-10-22_c_stage2/ov_test_dev299_neardup_files.txt" || true
      echo "statement: this host has never held an OV-test byte, the C-CONF token or a C-CONF output (operator to sign)"
    } 2>&1 | tee "S0_RECORD_${VSPS_MACHINE_ID}.txt"
    sha256sum "S0_RECORD_${VSPS_MACHINE_ID}.txt" ;;
  custody)
    need_host
    "$PY" -I -B "$HERE/c_n3d.py" custody --root "$2" --data "$3" 2>&1 | tee "CUSTODY_RECORD_${VSPS_MACHINE_ID}.txt"
    sha256sum "CUSTODY_RECORD_${VSPS_MACHINE_ID}.txt" ;;
  run)
    need_host
    timeout --signal=KILL 4h "$PY" -I -B "$HERE/c_n3d.py" run --root "$2" --data "$3" --out "$4" ;;
  *) echo "usage: $0 selftest | closure ROOT DATA | s0 ROOT DATA | custody ROOT DATA | run ROOT DATA OUT" >&2; exit 2 ;;
esac
