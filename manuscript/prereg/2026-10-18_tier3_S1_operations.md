# Tier-3 S1 (T3.2): operating notes for the frozen job

These notes change nothing registered and no instrument file.

- **Registration:** `2026-10-18_tier3_S1.{md,json}`.
- **Instrument:** pinned by `2026-10-18_tier3_S1_instrument.json` (commit `738260059d284a7f23a026e8c7805ecc8e1a3ab9`).
  - `scripts/seed_consensus.py`: `2b72dc417d60c5ec6a0be9cfd3b69692a783e2ba9bd1fc7dcb14c5195296c486`
  - `scripts/queue/jobs/t3_2_s1_seed_consensus.sh`: `3acd86835c728bf432f622c7bafc03a177e54047b3206570b23514c7a2080ffb`

## Before queueing (M1, after S5)

- **HEAD:** M1's HEAD is 7382600, or a later commit that leaves `scripts/queue/qrun.sh` at `2eaca17c...` (D-W14-1). The job's `check` refuses any other qrun.sh, because qrun.sh is in the registered code_at_head.
- **G-1:** G-1 v5 has passed for that HEAD (D-W13-3).
- **Panel file:** `data/ktvic_openviic_refs.json` is at `/root/vsps/data/` with sha256 `4eb02cc43841bae4f844ee74d4c01b58e677dc8d6abafdd998c9f5b5706f725d`. It never enters git, and it is deleted at rental end.
- **Queue file:** a byte-identical copy of the committed job file, under any queue name. The job checks its own sha256 against the addendum.

## Restart after an interruption

The job skips every step whose output exists and never overwrites an output. Before re-queueing:

- Move aside whatever the interrupted step left. Rename it with an `.aborted_<UTC>` suffix; never delete it.
- Report every move to main.

Paths:

- `O` is `/root/outputs/t3_2_s1_seed_consensus`.
- The hook's mirror for a run is `/root/outputs/runs/<run>`.

| interrupted during | move aside | why |
|---|---|---|
| training `p1dev_s43` or `p1dev_s44` (CC-019) | `$NCS_DATA/runs/<run>`, `/root/outputs/runs/<run>`, `O/train_<run>.log` | The member is retrained from step 0. If only the run directory is moved, `checkpoint_resume_hook` copies the mirror's `checkpoint-*` back and auto-resumes. The training log is appended (`tee -a`). |
| the soup step, `soup_selfcheck.json` absent | `$NCS_DATA/runs/p1dev_soup3_s42s43s44`, if it exists | The soup step refuses an existing soup. The rebuild from the same members is byte-identical. |
| MBR, `p1dev_mbr3_selection.json` absent | `O/p1dev_mbr3-dev300-short.preds.json`, plus `O/p1dev_mbr3-dev300-short.json` and its `.provenance.json` if they exist | The gate reads the selection with the captions. The selection is deterministic and is redone, then scored again. |
| a decode or its scoring | nothing | Captions already on disk are scored; they are not decoded again. |

If `O/soup_selfcheck.json` records `"self_check_pass": false`, stop and report. The soup was not saved, and S1 does not go on without a ruling.

The move-aside rule applies whenever an operator re-queues the job. There is one other path: if qrun reruns the same queue file by itself after a machine restart, the hook resumes a member from its last checkpoint. Rule V4 below covers that case.

## Step count of the new members (judge CC-019b, option (a))

**Expected count.** Each of `p1dev_s43` and `p1dev_s44` takes 866 optimizer steps, i.e. 2 × floor(3469 / 8). This is the same as p1dev_s42's n2 run (final step 866, epoch 1.996).

**Void rule.** S1 is VOID if any of V1 to V4 holds for either member. VOID is a disclosed deviation: neither PASS nor KILL, and nothing is carried.

- **V1:** the last record of `runs/<R>/metrics.jsonl` does not have integer `step == 866`.
- **V2:** `runs/<R>/metrics.jsonl` or `O/train_<R>.log` was last modified after `O/soup_selfcheck.json`.
- **V3:** `O/train_<R>.log` records an exception or traceback, or lacks `loss mask: assistant`.
- **V4:** `resume_manifest.json` shows a resume and the run did not reach step 866.

A resumed run that does reach 866 is valid. It is still disclosed, with the resume step and the fact that the RNG state was not restored.

**Who and when.** The M1 operator, or a CPU verifier, checks V1 to V4 from the machine snapshot before anyone reads `gate.json`. The values for each member are then recorded:

- in a new file next to the results, `O/s1_void_check.json`, holding the snippet's output and written once (never overwrite; use `_v2`);
- in `M1_EVENTS.log`.

**Where the evidence is.** `metrics.jsonl` sits in `$NCS_DATA/runs/<R>/` on the machine. If the job ended OK, qrun also copies it, with its mtime, to `/root/outputs/runs/<R>/`. The training logs and `soup_selfcheck.json` are in `O`.

```bash
python3 - /root/outputs/t3_2_s1_seed_consensus /root/ncs-data/runs <<'PY'
import json, re, sys
from pathlib import Path
O, RUNS = Path(sys.argv[1]), Path(sys.argv[2])  # or the snapshot copies of the same two directories
soup_t, rows = (O / "soup_selfcheck.json").stat().st_mtime, {}
for run in ("p1dev_s43", "p1dev_s44"):
    m, log, man = RUNS / run / "metrics.jsonl", O / f"train_{run}.log", RUNS / run / "resume_manifest.json"
    step = json.loads(m.read_text(encoding="utf-8").splitlines()[-1]).get("step")
    text = log.read_text(encoding="utf-8", errors="replace")
    resumed = json.loads(man.read_text(encoding="utf-8")).get("resumed_from_step", []) if man.is_file() else []
    raised = "Traceback (most recent call last)" in text or bool(re.search(r"^\w*(Error|Exception): ", text, re.M))
    rows[run] = {"last_step": step, "resumed_from_step": resumed, "metrics_mtime": m.stat().st_mtime,
                 "log_mtime": log.stat().st_mtime, "soup_selfcheck_mtime": soup_t,
                 "V1": not (type(step) is int and step == 866),
                 "V2": max(m.stat().st_mtime, log.stat().st_mtime) > soup_t,
                 "V3": raised or "loss mask: assistant" not in text,
                 "V4": bool(resumed) and step != 866}
void = any(r[v] for r in rows.values() for v in ("V1", "V2", "V3", "V4"))
print(json.dumps({"rule": "CC-019b void rule", "members": rows, "void": void}, indent=1))
PY
```
