# B-PA1 tier 1: scorer code-read package v2 (2026-11-11T01:53:57Z)

Record only, for CC-316 round 2 (amendment read, code v2 diff read). Synthetic fixtures only; no pulled output, gold
or sealed path touched; no commit, no real run. v1 files are unchanged (`c712899d`, `8ad6b555`).

## 1. Files

| file | sha256 |
|---|---|
| `AMENDMENT_T1_SCORING_RULES_v1.md` (this folder) | `316862730591de00f9a519d52bf6dc3daef2c0edf15214b8dc26aec087e7a93a` |
| `scripts/b_pa1/b_pa1_score_v2.py` | `4ab648e433918be89d416a0c8be60117675e4cf8b643e4269bc1c5c0a1e063cc` |
| `scripts/b_pa1/b_pa1_score_v2_mutants.py` | `fe939e7188d1c041403d295902120bd88dfcabdcb9f01786f548f1bded78272f` |
| `scripts/b_pa1/SHA256SUMS_SCORE_v2` | `227c724f7837a5b5e23fe2d0176405407126b80b4a8665d332129117507e32dc` |

Venvs (R2, `-I`): PN = `~/.venvs/c_stage1_lists`, freeze `1a639a50`, frozen again 2026-11-10: `numpy==2.5.4`,
`scipy==1.18.1`. The v1 line "No scipy" was wrong (W8). PJ = `~/.venvs/b_pa1_ijson`, freeze `dffafd50`.

## 2. CC-316 item → where closed (`b_pa1_score_v2.py` lines)

| item | closed in |
|---|---|
| W1 Q1 (a)-(e), W10 | amendment §1; `terms_of` :103, `cmd_join` :214, `gold_of` :258 |
| W1 Q2 | amendment §2; `Mapper` :278 |
| W2 Q3 | amendment §3; `baselines` :399, `cmd_thresholds` :421-426, `deltas` :360, `bound` :367, `cmd_tau` :466 and :494, `strict` :94 |
| W2 Q4 | amendment §4 and its §10 deviation line; `P_PASS` :76 |
| W3 V1 | `gold_of`, `Mapper`: both OPEN refusals removed |
| W3 V2 | `tau_c` :339 (scipy, variants c and b), `boot` :345 (expanded resample); the numpy `tau` :537 serves the selftest only; both outputs record `scipy.__version__` |
| W3 V3 | as W2 |
| W3 V5, V7 | §3 below |
| W4 | §5 below; **not written** |
| W5, V4 | amendment §7; `CONV` :78 in both outputs; p form governs, `holm` :384 |
| W6 | amendment §5; open (O6) |
| W7, V6 | `terms_of` :106; `IMPORTS` :74 and `load_join` :253; `pin_lines` :173 and `cmd_tau` :443; dictionary-only bounds :502; `cmd_contacts` :192 |
| W8 | §1 above |
| W9 | wording only: the scorer takes the ACCEPT keys from `ACCEPT.json` |
| W11 | `mention_counts` :266 and `per_captioner` in `T1_RESULT.json`, for the result read |
| W12 | LOG OPS-1111d-cc316 (ACCESS_LOG row 60) |

## 3. Results (code `4ab648e4`)

- **Selftest** (`PN -I -B scripts/b_pa1/b_pa1_score_v2.py selftest`): `b_pa1_score_v2 ok`, 53 checks, about 1 min.
- Fixture modes: FAIL, EDGE, CONST (undefined τ of B), FLAT (undefined lever τ) and PASS. PASS runs the command
  line's default, the registered 10,000 resamples (mutants S9, S10). The other four pass 1,000 through the test-only
  `nb` argument, because the scipy call is slow.
- Cases for the new rules: a two-row term with one boxed class; two terms of one class; a term with rows of both
  tags under both tag sets; a word written twice; a classifier head noun; an empty head noun; at step 7 a null
  baseline, an undefined τ and an undefined SE_A replicate; undefined replicates in Holm and in the bounds. scipy
  equals the pair definition on every point; the scipy bootstrap equals v1's numpy bootstrap through SE_A, the
  bounds and the p values.
- **Mutants** (`PN -I -B scripts/b_pa1/b_pa1_score_v2_mutants.py`): control passes; **68/68 killed**, 3 min 57 s.
  CC-316 V7's four are G3 (any-of → all-of), G4 (term → class unit), M1 (matcher → lookup), T1 and T2 (scipy
  variant c ↔ b).

## 4. Laptop commands after a GO (steps 6-8)

`. ~/bpa1_env_4.sh; cd "$R"; unset RESCAP_RAW_TONE; PN=~/.venvs/c_stage1_lists/bin/python;
PJ=~/.venvs/b_pa1_ijson/bin/python; S=scripts/b_pa1/b_pa1_score_v2.py; P=$PULL/final/b_pa1_out`; `D` = a new
directory outside the tree.

1. Gatekeeper: commit the files of §1 and this package; write the two lines of amendment §10, then the §5 line.
2. `$PN -I -B $S selftest`
3. `$PN -I -B $S contacts --pulled $P --lists $PRE/b_pa1_lists.json --out-dir $D/contacts`
4. Step 6, alone on /mnt/d: `$PJ -I -B $S join --pulled $P --lists $PRE/b_pa1_lists.json --map $S4/final/b_pa1_map_final.json --ann data/datasets/objects365_v2/zhiyuan_objv2_train.json --out-dir $D`
5. Step 7: `$PN -I -B $S thresholds --pulled $P --join $D`
6. Gatekeeper, once: `<date -u +%FT%TZ> OPS-<MMDD>b-t1thr-pin: PIN T1_THRESHOLDS.json <sha256 of $D/T1_THRESHOLDS.json>`
7. Step 8: `$PN -I -B $S tau --pulled $P --join $D --map $S4/final/b_pa1_map_final.json`; then the one-judge result
   read.

## 5. W4: the `SHA256SUMS_rest` pin line (CC-316 Ruling 3, verbatim)

To be written by the gatekeeper **only after** the amendment and code v2 have a GO and are committed. The sha comes
from `sha256sum` of the file only (no content read) and must start `f6fcbcd0`.

`<date -u +%FT%TZ> OPS-<MMDD>b-t1sums-pin: PIN SHA256SUMS_rest <64-hex sha256 of $PULL/final/b_pa1_out/SHA256SUMS_rest> (B PA1 tier-1 final pull, 84 lines, FULL OK at OPS-1110b-hbt1-pulled and T1_HANDOFF_STATUS s2; scorer input lock per CC-316)`

## 6. Open points

- Amendment §11, O1-O8: O1-O4 extend CC-316's Q3 sentences; O5 leaves N_val, n and the ε seed to the tier-2 prereg;
  O6 the Q5 rows; O7 the distinct-class row is not registered; O8 the `rescap/` files are not re-hashed.
- Four of five selftest modes run 1,000 resamples (§3).
- Two v1 mutants (T1, T2 on the numpy formula) have no v2 counterpart: that formula is now a selftest check.
