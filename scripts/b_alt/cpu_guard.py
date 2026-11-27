#!/usr/bin/env python3
"""CPU guard for one B-ALT stage: runs the command in its own session and kills the whole process group once the
CPU seconds of the process tree (the command, its live descendants, and every child they have reaped) reach the
limit. This closes the gap of `prlimit --cpu`, which limits each process separately (CC-506 C6: a Java child had its
own RLIMIT_CPU). Polls /proc every POLL seconds, so the overrun is at most POLL x cores seconds.
A descendant that detaches from the tree (re-parented to init) is not counted; the stage code starts none.
    python3 -I -B cpu_guard.py LIMIT_SECONDS -- CMD ...
Exit: the command's code; 7 when the guard killed the tree (the caller then writes STOP). Stdlib only."""
import os
import signal
import subprocess
import sys
import time

POLL = 2.0
CLK = os.sysconf("SC_CLK_TCK")


def tree_cpu(root: int) -> float:
    """utime + stime + cutime + cstime (seconds) of root and of every live descendant."""
    kids, tick = {}, {}
    for d in os.listdir("/proc"):
        if not d.isdigit():
            continue
        try:
            with open(f"/proc/{d}/stat") as f:
                s = f.read()
        except OSError:
            continue
        r = s[s.rindex(")") + 2:].split()
        kids.setdefault(int(r[1]), []).append(int(d))
        tick[int(d)] = sum(int(x) for x in r[11:15])
    tot, todo = 0, [root]
    while todo:
        p = todo.pop()
        tot += tick.get(p, 0)
        todo += kids.get(p, [])
    return tot / CLK


def main(argv) -> int:
    if len(argv) < 3 or argv[1] != "--":
        print("usage: cpu_guard.py LIMIT_SECONDS -- CMD ...", file=sys.stderr)
        return 2
    limit, cmd = float(argv[0]), argv[2:]
    p = subprocess.Popen(cmd, start_new_session=True)
    peak = 0.0
    while p.poll() is None:
        peak = max(peak, tree_cpu(p.pid))
        if peak >= limit:
            os.killpg(p.pid, signal.SIGKILL)
            p.wait()
            print(f"cpu_guard: KILLED at {peak:.1f} CPU-s of {limit:.1f}", file=sys.stderr)
            return 7
        time.sleep(POLL)
    print(f"cpu_guard: rc {p.returncode}, last tree reading {peak:.1f} CPU-s of {limit:.1f}", file=sys.stderr)
    return p.returncode


if __name__ == "__main__":
    sys.exit(main(sys.argv[1:]))
