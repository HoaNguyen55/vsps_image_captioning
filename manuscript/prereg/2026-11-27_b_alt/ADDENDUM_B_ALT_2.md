# ADDENDUM B-ALT-2 to PREREG_DRAFT_B_ALT_v2.md (ed05acdb) and ERRATUM_B_ALT_1.md (8367face): D1 results added to the §2 seen list

Written by ruling CC-510e3 (2026-11-27) under CC-514 W9, before FE-LOCUS S2. No FE-LOCUS quantity of §3.4 or §4 has been computed.

It changes no hypothesis, threshold, floor, seed, split, estimand, data set, host rule or stage order. It only adds lines to §2, "Numbers already printed or seen". §2 promised to list D1's outputs "at the commit"; the registration commit, 74e5034, came before D1's result, so they are listed here instead.

## Added to §2 (POST HOC for this study; no rule of FE-LOCUS is decided by them)

The D1+A3 registered result, `RESULT_D1.json` c2fa610c, as read in ruling CC-514. Labels are worded as the D1 registration words them: DEVELOPMENT, REGISTERED PREDICTION, every p and bound nominal.
- **H1** (FE-CERT vs reference-member margin, equal size): **SUPPORTED**.
  - b_FE 3 vs b_MG 34, n 37; one-sided exact p 6.17e-8, Holm reject.
  - Per fold: syl 1 vs 12, pyvi 1 vs 12, uts 1 vs 10 (K 918 / 910 / 909).
- **H2** (FE-CERT vs Lu et al. AER ensemble, equal size): **NOT SUPPORTED**.
  - b_FE 3 vs b_AER 11, n 14; raw one-sided p 0.0287, against a Holm step of 0.0167, so not rejected. AER-fewer p 0.9935.
  - Per fold: 1 vs 5, 1 vs 4, 1 vs 2.
- **H3** (tone placement beyond a scorer-and-tokenizer grid): **NULL**.
  - k_T 0 of n 782; one-sided 95% CP [0, 0.0038]; split by unit 0/0/0.
  - DESCRIPTIVE: syl-only grid 796, k_U 14, k_TU 14.
- **A3** (per-member level on exchangeable sign-flip nulls): **AT OR BELOW NOMINAL**.
  - r_f0+ 22/1000 (97.5% CP 0.0138–0.0331); r_f0− 24/1000 (0.0154–0.0355).
  - r_A3 over F_dev 15 / 14, over F 15 / 13 (DESCRIPTIVE).
  - Maximum per-member rate over F_dev: + 0.025, − 0.030 (DESCRIPTIVE).
- **M1 = M1′ method check:** equal on 1101 of 1101 comparisons; 0 mixed-direction all-significant.
- **H2 DESCRIPTIVE (native size):**
  - claims FE 918/910/909, AER 931/933/931, f0 936;
  - held-out flip coverage FE 0.64/0.94/0.94, AER 0.44/0.61/0.75;
  - false-tie analogue FE 0.002/0.010/0.013, AER 0/0/0;
  - FRAGILE over G_u 44/52/59 of 1101.
- **POST HOC T-split count** (CC-514, from the class statistics stored in `DEV.json`): the tone levels tm/tf form a class different from tw in all 1101 comparisons, with syl 13,206, pyvi 13,206 and rdr 594 member-cells.

## Not seen, still

- Any per-type disagreement count.
- Any rdr→pyvi shift δ on a comparison. CC-514 states none.
- Any pinned score.
- Any quantity of §3.4 or §4.
- `PER_IMAGE_D1.npz`, which this study never opens.

## Why nothing here can move FE-LOCUS

- Every FE-LOCUS rule was fixed before these numbers existed, at 74e5034, 2d3c39f and 7f7cf4f.
- FE-LOCUS's labels are relative: κ_head against the per-draw c band, ρ_head against 0.50, and the floors (i)–(v). None of the numbers above enters them.
- The T-split count concerns the part of the shift that κ_head already removes from the primary label (§3.4).
- §7 still forbids using any FE-LOCUS row to qualify D1's H3.
