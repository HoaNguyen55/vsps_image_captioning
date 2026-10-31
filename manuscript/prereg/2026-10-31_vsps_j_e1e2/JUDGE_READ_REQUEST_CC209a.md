# JUDGE_READ_REQUEST CC-209a: one-judge diff read of AMENDMENT_1 + CC209a_W1.diff (REVERSIBLE, bar >= 90)

Requested 2026-10-31 by the drafting agent. Parent: CC-209 (GO-with-fixes 90), path (ii), W1 a-e and W2; the W5
commit is 43423d9 (pushed to q2 main). Funding line: PI-1031k. W4 was closed by the coordinator (OPS-1031e1aimg).
A GO licenses:
- the gatekeeper commit of the files below;
- then one rented RTX 4090 for **E1b only**, under PI-1031k with the PI told at rent time;
- E1a on M1 when its queue slot comes (CC-207 r8), or earlier in an idle window if the PI allows it (CC-209 Q3).

## Files (old sha at 43423d9 -> new sha)
- `scripts/vsps_j_e1e2/e1e2.py` 8694206e -> c659691a9b790d2de5989dc0f87e1649f19040bbf4046b96f58e437f361b4ce4
- `scripts/vsps_j_e1e2/e1e2_job.sh` aedaf47f -> d7cc6a2b81c3f3f41e077e4098e9e8d3153d3aadb6f88a58ef31b2143ac36522
- `scripts/vsps_j_e1e2/test_e1e2.py` 63fc3abf -> 43f6c36fc0c2b6c1c6fa880ea8e2b05ca1ebbb83d1704a2b500f48d5ff1487d7
- `scripts/vsps_j_e1e2/SHA256SUMS` fab66fb4 -> 75c0cb9206e2f1216ae900209f1cc5e90b2bd99acc997a0cd261a3ebea2cf519
- `scripts/vsps_j_e1e2/ret.py` bf0c1696 (unchanged)
- `manuscript/prereg/2026-10-31_vsps_j_e1e2/PREREG.md` 555a832f -> 0fdc1c7bcc76b6fd7769ee6043bab3ba218e1c647267eea37409d7ac7ed81985
- `manuscript/prereg/2026-10-31_vsps_j_e1e2/SHA256SUMS` 9965d745 -> facce311f8d0a708dc14c912c93b70a2b5a7e33b251bf9c711b580117ab2451f
- `manuscript/prereg/2026-10-31_vsps_j_e1e2/e1e2_plan.json` 0aafd392 (unchanged; `plan` re-run, byte-identical)
- `manuscript/prereg/2026-10-31_vsps_j_e1e2/AMENDMENT_1.md` (new) 5f67e70997802201ad8f5228111370e52092ce9fea3afa6ed125d4c6e19f0615
- `manuscript/prereg/2026-10-31_vsps_j_e1e2/CC209a_W1.diff` (new, outside the SUMS) 890897639e1b0e54cf0575f0f47aead81e23065f4f0e223bd89c37b389cc13de
- `manuscript/prereg/2026-10-31_vsps_j_e1e2/JUDGE_READ_REQUEST.md` 6f2188cb (unchanged)
- this file is outside the SUMS.

## Checks already run (re-runnable)
1. **The diff applies to 43423d9.** `git archive 43423d9` into a fresh scratch tree, `git apply` the diff, then `cmp`:
   all 7 changed or new files are equal to the working tree.
2. **AST compare of e1e2.py against 43423d9.**
   - Changed: `cmd_e1a`, `cmd_score`, `main`. New: `e1a_smoke`, `cmd_smokelist`. Removed: none.
   - Module-level constants: none changed, none added.
   - `run_pass`, `run_smoke`, `replay`, `kt_metrics`, `select_s_hi`, `tcoco_*`, `cluster_ci`, `fidelity`, `score_e1b`,
     `score_e1a`, `install_sidelog`, `run_stage1` and `cmd_e1b` are AST-identical.
3. **Selftests:**
   - `~/.venvs/vsps_j_m0/bin/python -I scripts/vsps_j_e1e2/e1e2.py selftest` gives `selftest ok`;
   - `PY=<that venv> bash scripts/vsps_j_e1e2/e1e2_job.sh --selftest` gives `selftest ok`. It now runs on the laptop: the
     accelerate / qwen-vl-utils pins are asserted only in the `e1a` branch.
   - New cases: a repeated score is refused; `--stage e1a` with a wrong frozen sha is refused; the staged e1b -> e1a
     path works; `broken()` fails by RuntimeError (W1e).
4. **Plan:** `python3 -I scripts/vsps_j_e1e2/e1e2.py plan` leaves `e1e2_plan.json` byte-identical (0aafd392).
   `smokelist` gives the 20 names, after the order sha check against the plan.
5. **E1b branch isolation:** in `e1e2_job.sh`, every UIT-ViIC and Qwen step (fetch list, curl, sha list, staging, Qwen
   snapshot) is inside the `e1a` branch. The `e1b` branch fetches Vintern only and runs `e1e2.py e1b`.
6. **Leak and ident scans:** 8-gram scan 0 on every new or changed file (KTVIC, UIT-ViIC, OpenViIC, COCO). Host / IP /
   port / e-mail grep 0.

## W1 / W2 map
| CC-209 item | Where |
|---|---|
| W1a E1b never fetches or stages UIT-ViIC | `e1e2_job.sh` selector; AMENDMENT_1 A1 |
| W1b E1a's own smoke on M1, section 6 rules unchanged, refuses unless it passes | `e1a_smoke()`; A2 |
| W1c one OUT folder per host; laptop score root assembled from two sha-checked pulls | A3 |
| W1d exact pins accelerate 1.15.0, qwen-vl-utils 0.0.14 | `e1e2_job.sh` e1a branch; A4 |
| W1e `broken()` | `test_e1e2.py` |
| W2 staged scoring, S_hi frozen and logged before E1a, no repeat | `cmd_score --stage/--frozen/--frozen-sha`, no-overwrite refusal; A5 |
| W6 operator rules (single resume, folder recreation, M1 isolation, detect re-fetch and deletion) | A1, A6 |
| W7 program pointers | `VSPS_J_PROGRAM_2026-10-31.md` (untracked, edited: 82d770e4 -> fa4c6040) |

## Questions (recommendation and default)
1. **E1a runs with its own `HF_HOME` on M1.** The job refuses without it, because `refs/main` is rewritten to the pins
   and must never move other owners' Qwen loads. It also needs a fresh Qwen download (about 16.6 GB) on M1. Accept?
   Recommended: YES. Default: YES.
2. **Staged scoring is primary** when E1b is pulled before E1a launches, and `--stage all` is the fallback. Accept?
   Recommended: YES. It freezes S_hi before any E1a datum exists. Default: YES.
3. **The 20 KTVIC-train smoke images are staged on M1.** They are train images, not test images, and are checked
   against the `ktvic_test` bytes. Accept? Recommended: YES. Default: YES.

## Default if no ruling
No amendment commit and no rental. The W5 commit (43423d9) stands.
