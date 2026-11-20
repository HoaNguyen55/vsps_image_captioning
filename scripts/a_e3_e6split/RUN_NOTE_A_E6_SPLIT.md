# Run note: `a_e6_split.py split` (REG-1119a (ii) and (iii)), laptop, once

Written 2026-11-20 by agent a-e6split-code. Outcome-free: registered rules, shas and LOG ids only. Nothing in this folder has been run yet. The laptop got `py_compile` and `bash -n` only.

## Where and when

**Laptop, once, right after the e3-score END line, in the same quiet window.** The conditions are those of CC-371 ruling 8: T12, nothing else heavy running, the rating server down, no bulk `/mnt/d` I/O.

It cannot run on a rented host. The mode reads the same four label and key files as e3-score, and CC-355 N-1 / CC-366 4(e) keep those on the laptop.

## Where it must differ from CC-371 ruling 8

1. **Licence (missing).** CC-366 4(e) names two laptop modes only, e3-freeze and e3-score, one invocation each. This mode needs its own named exception. That means a one-judge code read (REVERSIBLE, bar 85) that names it, plus the gatekeeper commit of this folder's two `.py` files. The host records come first.
2. **T8 is inverted.**
   - `data/results/a_cert_e3/score/A_CERT_E3_RESULT.json` must exist.
   - Its full sha must be on the e3-score END line. The code refuses otherwise, through `pinned(…, "A_CERT_E3_RESULT")`.
   - The split's own path, `data/results/a_cert_e3/split/A_CERT_E3_E6_SPLIT.json`, must be absent. Its run-once rule sits on this path.
3. **T2 and T11 are extended.** Two more files must equal their HEAD blobs: `a_e6_split.py`, and `overlap_images.txt` at 4f971966. The code checks both. `a_cert_e3.py` stays unchanged, so the e3-score licence (T11) is not touched.
4. **The registered result is read in memory before its result read.**
   - The code recomputes the rows on the full key and refuses unless the recomputed E6 equals the stored E6 in serial form. Only E6 is compared: it is integers and integer ratios, while E1-E5 hold bootstrap floats whose bit equality across processes is not shown anywhere.
   - It then refuses unless E1-E5 and every E6 block but `old_repeat` are unchanged by the split.
   - Nothing is displayed. Only the counts and the two agreement values are written.
   - This is a judge item (J-5 below).
5. **Run time.** The scoring core runs twice, so expect about twice the e3-score core time. This was not measured.
6. **REG-1119a is a precondition.** The code refuses unless a LOG line holds `REG-1119a-topup-e6-split` and the verbatim reason clause.

## Pre-run checks (operator; shas and modes only)

These are the CC-371 r8 block plus three changes:
- add `scripts/a_e3_e6split/a_e6_split.py` and `manuscript/prereg/2026-11-11_xm600_gold_completion/overlap_images.txt` to the `git diff --quiet HEAD` and `sha256sum` lines;
- replace the T8 line with `test -e …/A_CERT_E3_RESULT.json && echo present`, then `grep -c "<its full sha>" LOG` (expect ≥ 1) and `test -e data/results/a_cert_e3/split/A_CERT_E3_E6_SPLIT.json && echo STOP || echo absent`;
- use the same `L0 K0 L1 K1 S1` as the e3-score START line.

## The call (once)

```bash
cd /mnt/d/vsps_image_captioning
OMP_NUM_THREADS=2 nice -n 15 ~/.venvs/c_stage1_lists/bin/python -I -B scripts/a_e3_e6split/a_e6_split.py split \
  --labels "$L0" --labels-sha ba362466ebd9c50918076dcf5865fbac9c5cd6482288f4251fa1f76e0f2718b4 \
  --key "$K0" --topup-labels "$L1" --topup-labels-sha "$S1" --topup-key "$K1"
```

- **Stdout:** one JSON line `{"wrote", "sha256"}` (rc 0), or `FAULT <type>` (rc 2).
- **After rc 0:** `sha256sum`, then `chmod 444`. Do not display it, and do not commit it; keep it unstaged like the E3 result. It is read in the one-judge E3 result read, printed beside E6 (run doc §7).
- **Faults:** as CC-371 r8. STOP, one OPS line, and no rerun without a judge. A `/mnt/d` EIO is handled as in run doc §6.

## LOG templates (`date -u`; 8-hex prefixes, W4)

- `<utc> | OPS-<id>-a-e6-split-start | REG-1119a (ii)+(iii), named laptop exception <licence id>; DEVIATION (named laptop exception to PI-1111j) | python … 3.12.3 pip-freeze <8hex> | a_e6_split <8hex> (HEAD), a_cert_e3 aec32aa0, overlap 4f971966, E3 result <8hex> (END line <id>), same four inputs as <e3-score-start id>; split path absent`
- `<utc> | OPS-<id>-a-e6-split-end | exit <rc> | wrote data/results/a_cert_e3/split/A_CERT_E3_E6_SPLIT.json sha256 <full> OR FAULT <type> | nothing displayed; 444; not committed`

## Judge items (for the code read; all label-free, so they can be fixed before the one run)

- **J-1. Definition of "same-map pairs" in REG-1119a (iii).**
  - The code prints a literal count: top-up pairs of any role except `old_repeat`, on listed images, for which some base question on the same image names another class with an identical `syn` (pos and neg MIDs).
  - It also prints five variants, without choosing among them:
    - the count of (top-up pair, base pair) couples;
    - part-1 targets only;
    - all top-up images;
    - any shared pos MID;
    - exact base pairs that are not `old_repeat`.
  - The judge fixes one of these before the run. The others then stay descriptive, or the judge orders them dropped from the output.
- **J-2.** J1 B4 also asked for E6 on the listed subset. REG-1119a did not register that, so it is not computed. It can be derived from (i) minus (ii) in any case.
- **J-3. Ordering.**
  - J3 W7: "the e3-score run reads [the 8f line]; any code change for (ii) gets a code read before the score run". This code changes no line of `a_cert_e3.py`, so e3-score runs unchanged.
  - Run doc D-4 says the split does not gate e3-score.
  - Whether this code read must come before the e3-score call is the coordinator's call.
- **J-4.** Is the new laptop exception (item 1) wanted, or does the split wait for some other custody route?
- **J-5.** Is the in-memory read of `A_CERT_E3_RESULT.json` before its result read acceptable? It is compared on E6 only, and only the split values are written; a mismatch is a FAULT.
- **J-6.** Output fields: (i) and (ii) carry `n`, `n_YN_both`, `agree` and `agreement` only, not the U/A/unanswered counts of the registered E6 block. Is that enough?
- **J-7. The listed-ids guard runs after the label bytes are read.** The guard checks that every listed id is an I600 id. It needs the world's ids, so it runs inside the core, after e3_score has read the label bytes. CC-371's no-rerun reasoning assumes every label-free check comes first. The label-free overlap checks (sha and count of 150 unique ids) do run first.
- **J-8. `--overlap` is now a pinned constant path.** The plan proposed an `--overlap` argument. The code uses a constant path, pinned at sha 4f971966 and checked against its HEAD blob.
- **J-9. The real-mode branch is not exercised by the host tests.** No test reaches the `P is P_REAL` branch, which holds `real_pins` and the five SHA constants. The constants were checked by grep counts only:
  - the REASON clause appears verbatim on the REG-1119a line (1 line);
  - the freeze, part-1 and base-labels pins appear in CC-371;
  - the a_cert_e3 and overlap pins equal `sha256sum` of the files at HEAD.
- **J-10. The test is a named-check table, not bare asserts.** This is the repo's pattern (a_cert_e3 selftest and mutants), and it lets each mutant kill be attributed to a named check.
