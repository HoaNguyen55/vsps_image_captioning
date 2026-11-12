#!/bin/bash
# VP self-test + mutants against committed a_cert.py 2e872588 / a_cert_mutants.py 9d4d5916; CPU only, nice 19.
cd /root/a_cert_tree || exit 1
PY=/root/vsps/.venv/bin/python; O=/root/outputs/a_cert_checks_vp2; M=$O/mut
mkdir -p $O
{ echo "start $(date -u +%FT%TZ)"; sha256sum scripts/a_cert/a_cert.py scripts/a_cert/a_cert_mutants.py \
    scripts/a_cert/a_cert_vp.py scripts/a_cert/a_cert_vp_mutants.py; } >> $O/status.log
OMP_NUM_THREADS=2 nice -n 19 $PY -I -B scripts/a_cert/a_cert_vp.py selftest --out $O/selftest_vp.json > $O/selftest_vp.log 2>&1
echo "selftest_vp rc $? $(date -u +%FT%TZ)" >> $O/status.log
OMP_NUM_THREADS=2 nice -n 19 $PY -I -B scripts/a_cert/a_cert_vp_mutants.py $M > $O/mutants_vp.log 2>&1
echo "mutants_vp rc $? $(date -u +%FT%TZ)" >> $O/status.log
cp $M/mutants_result.json $O/mutants_result_vp.json
echo "DONE $(date -u +%FT%TZ)" >> $O/status.log
