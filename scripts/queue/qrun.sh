#!/bin/bash
# Committed GPU queue runner with mandatory Gate G-1 PASS code enforcement.
while true; do
  j=$(ls /root/queue/*.sh 2>/dev/null | sort | head -1)
  if [ -z "$j" ]; then sleep 120; continue; fi
  n=$(basename "$j" .sh)
  if ! /root/vsps/.venv/bin/python /root/vsps/scripts/queue/check_g1_pass.py >> /root/queue/queue.log 2>&1; then
    echo "$(date -u +%FT%T) BLOCKED_BY_G1_GATE $n" >> /root/queue/queue.log
    sleep 120
    continue
  fi
  echo "$(date -u +%FT%T) START $n" >> /root/queue/queue.log
  if bash "$j" > "/root/queue/$n.log" 2>&1; then
    s=OK
    /root/vsps/.venv/bin/python /root/vsps/scripts/checkpoint_resume_hook.py --stamp-results /root/ncs-data/results /root/ncs-data/runs >> "/root/queue/$n.log" 2>&1 || true
    /root/vsps/.venv/bin/python /root/vsps/scripts/queue/stamp_pre_g1.py >> "/root/queue/$n.log" 2>&1 || true
    rsync -a /root/ncs-data/results/ /root/outputs/results/ || true
    find /root/ncs-data/results /root/outputs/runs -type f -mmin -240 -exec sha256sum {} + 2>/dev/null | sort -k2 > "/root/outputs/sha256/$n.sha256" || true
    cp -f "/root/outputs/sha256/$n.sha256" "/root/queue/done/$n.sha256" 2>/dev/null || true
    mv "$j" /root/queue/done/
  else
    s=FAIL
    mv "$j" /root/queue/failed/
  fi
  echo "$(date -u +%FT%T) $s $n" >> /root/queue/queue.log
done
