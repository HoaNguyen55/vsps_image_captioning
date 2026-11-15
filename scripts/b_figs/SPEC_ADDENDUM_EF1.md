# SPEC_ADDENDUM_EF1: open points of Fig. EF1 (Paper B), settled from registered sources

Addendum to `.session_backup/2026-11-14/b_text_held/draft_v3/FIGURE_TABLE_SPEC.md` (sha256 `7e2d11bd…`, read-only), row "Fig. EF1" of section A3. It answers the three gaps the coder left open: the field names of the per-comparison rows, the definition of the standardised margin, and the inputs the figure needs besides RESULT.json. Each item gives its file::key (or file:line) evidence. Items that no registered source settles are listed under OPEN with their options; the script `figEF1.py` carries a provisional choice for each, marked as such.

## Sources read

| Source | sha256 |
|---|---|
| `manuscript/prereg/2026-11-12_b_fecert/B_FECERT_PREREG_v1_1.md` (the registration; "prereg" below) | `736b7e6a8ea2007270a3329db7ad6a09197c4804c9bc3821ea6bd4ceb5a61aa0` |
| `scripts/b_fecert/b_fecert.py` (stage code) | `67e43dea1b37c3bbfaa3fe5081d6f3d36848397451ad0a24d67fa67389b06b59` |
| `scripts/b_fecert/family.py` | `7cb2c69b8b7840388568fd5f9b248e2cf25df28185386be875a65d921a9e4178` |
| `manuscript/prereg/2026-11-12_b_fecert/results/B_FECERT_RESULT_NOTE_v1.md` (independent recompute; "result note") | `94730df22e910e7ee75cf07ead554c1d06400235bf8f50d77ffb43d0794817fe` |
| `.session_backup/2026-11-14/b_text_held/draft_v3/number_manifest_B_v2.tsv` | `d129e42e515d1ba46f55b40d92db87da0326c00acd9c9fbd971c56ee4df08979` |
| `.session_backup/2026-11-14/b_text_held/draft_v3/online_resource.md` (block EF1, l.150-151) | `19616bac34837a47eee6456a83a82dc924416f866361c9182914b7fe7a2938f2` |
| `.session_backup/2026-11-14/b_text_held/draft_v3/paper.md` (l.289, Table 7 paragraph) | `cb462dfc4797f3b7030fbe58a7b873aabef8a204cba62b55392cde92c1ed6a0e` |
| Key names and structure (no value) of RESULT.json, DEV.json, V.json under `.session_backup/2026-11-13/b_stages/host_pull/20261113T174234Z/b_work/` | listed in S6 |

Code identity: `RESULT.json::code_sha256`, `V.json::code_sha256` and `DEV.json::code_sha256` each name `scripts/b_fecert/b_fecert.py` = `67e43dea…` and `scripts/b_fecert/family.py` = `7cb2c69b…`, equal to the files on disk. The line numbers below are therefore those of the code that produced the three files.

## Settled

**S1. Per-comparison rows.** `RESULT.json::comparisons[i]`, a list of 1123 [n090] objects with keys `id` (str), `a`, `b`, `set`, `repo`, `D_f0` (float), `F` (str), `F_dev` (str), `changed_F` (bool). Written at `b_fecert.py:1242-1244` (stage 2b). Ids start with `D:` (the development pairs D) or `FL:` (the first-look pool).

**S2. The CHANGED flag.** `RESULT.json::comparisons[i].changed_F`; defined at `b_fecert.py:479` as `bool(f0) and s0 != 0 and not cert` over the full family F (`vF`, `b_fecert.py:1215`). It is used as stored and is not recomputed: the statistics of the held-out members are not stored in any released file (result note l.148), so CHANGED over F cannot be rebuilt from DEV.json and V.json. Counts: 30 CHANGED [n337], 1093 not [n338].

**S3. The standardised margin under f0.** prereg l.308 (§6.6 FE-PRED row): "the area under the ROC curve of |D_f0| / sd_boot(D_f0) for predicting CHANGED". In the code: `z0 = zval(f0 class cider)` (`b_fecert.py:1226`), `zval(s) = |s[0]| / s[3]` (`b_fecert.py:456`), with `s = [D_f, 2.5th percentile, 97.5th percentile, sd_boot]` (`stats()`, `b_fecert.py:383-387`, prereg §3.1). f0 is the member `rdr.tw.pk.cf` (`family.py:31`, `F0 = ("rdr", "tw", "pk", "cf")`; name form `family.py:46-50`). The margin is not a field of RESULT.json: `RESULT.json::comparisons[i]` holds `D_f0` but not `sd_boot`. It is read from the one class whose `members` list contains `rdr.tw.pk.cf`:
- for a `D:` id: `DEV.json::comparisons[j].classes[k].cider[3]`;
- for an `FL:` id: `V.json::fl[j].classes[k].cider[3]`;
joined on `id`. The result note recomputes the same way ("z under f0 is recomputed from the stored f0 class", I-36 (c), l.780). No class has sd_boot = 0 (result note l.168 and l.1199, its tag n009; not a row of the draft manifest), so no margin is infinite; the script still stops if one is.

**S4. Significance under f0.** Not a field of any released file. Derived as in the code: `sig(s) = +1 if s[1] > 0, -1 if s[2] < 0, else 0` (`b_fecert.py:452-453`) on the same f0 class; significant when `sig != 0` (`sig0`, `b_fecert.py:1227`; `sig_f0`, `b_fecert.py:479`). Count: 946 [n340] (manifest source "RESULT.json + DEV.json + V.json::derived", which names the same three files). Every CHANGED comparison is significant under f0 by definition (`b_fecert.py:479`); the script checks this.

**S5. Direction and ties of the area under the curve.** `auc()` at `b_fecert.py:553-557`: the probability that a CHANGED comparison has the smaller margin than one not CHANGED, ties counted one half. The registration does not state the direction (result note I-36 (e), l.783); the coded one is used, and paper.md l.289 already says so. Values: `RESULT.json::secondary.FE_PRED_AUC` = 0.801158889905459 [n336], printed 0.8012; `RESULT.json::secondary.FE_PRED_AUC_f0_significant_EXTRA` = 0.9545851528384279 [n339], printed 0.9546 (extra row, not registered; result note I-37).

**S6. Inputs.** All three under `.session_backup/2026-11-13/b_stages/host_pull/20261113T174234Z/b_work/`:

| File | sha256 | Manifest prefix | Keys used |
|---|---|---|---|
| RESULT.json | `25614b469cf59dc61f15e839b89a8e78ca0b316905afc4bd2ae52eaa0d32b43a` | `25614b46` (n336 to n340) | `comparisons[i].{id, D_f0, changed_F}`; `secondary.FE_PRED_AUC`; `secondary.FE_PRED_AUC_f0_significant_EXTRA` |
| DEV.json | `88ff39aa9552b671a0e439aec961d0fefe02df1f52a2a5df9765a9d8226f7e8d` | `88ff39aa` (n340) | `comparisons[j].{id, classes[k].members, classes[k].cider}` (1101 comparisons) |
| V.json | `1f011538bf06a601c2104116ccef31f470eed473b2a96c9e6f8a5408f126f6b9` | `1f011538` (n340) | `fl[j].{id, classes[k].members, classes[k].cider}` (22 comparisons) |

The ids of RESULT.json equal those of DEV.json plus V.json, with no repeat, and each comparison has exactly one class holding `rdr.tw.pk.cf` (structure check of key names and membership only; no value was read). Byte-equal copies of DEV.json (same sha256) also sit under `20261113T154430Z/b_work/` and `20261113T174234Z/b_pins/`; the script reads the `174234Z/b_work/` copy, beside RESULT.json.

**S7. What the figure shows.** Two distributions, CHANGED over F and not CHANGED over F, over all 1123 comparisons with D and FL pooled: online_resource.md l.151 ("of the comparisons that are CHANGED over F and of those that are not") and paper.md l.289 ("computed over both pools together (1123 comparisons)"). The 946-comparison subset enters only the second area-under-the-curve check, not as a third curve. The labels stay in the caption, not inside the figure: DESCRIPTIVE; D is DEVELOPMENT; the first-look pool is FIRST SCORING OF RELEASED OUTPUTS (online_resource.md l.151).

**Checks in `figEF1.py` before any file is written:** sha256 of each input; ids equal and unique; exactly one f0 class per comparison; `RESULT.json` `D_f0` equals `cider[0]` of that class (within 1e-12; this proves the join); every margin finite; `changed_F` boolean, and CHANGED implies significant under f0; counts 1123, 30, 1093, 946; both recomputed areas equal the `secondary` values within 1e-12 and round to 0.8012 and 0.9546.

## OPEN (not settled by a registered source; for the coordinator)

| Id | Point | Options | Provisional choice in `figEF1.py` |
|---|---|---|---|
| O1 | Form of the "two distributions" | (a) empirical cumulative distribution, two step lines; (b) histograms on shared bins; (c) jittered strip or box plot | (a): it needs no bin width or jitter and shows the ordering the area under the curve measures |
| O2 | Horizontal scale of the margin | (a) linear from 0; (b) logarithmic (fails for a margin of exactly 0, which `zval` returns when D_f0 = 0); (c) symmetric-log | (a). The choice must not be made by looking at the real margins on this laptop; if it changes, decide it at the host run from the rule, not from the picture |
| O3 | Area-under-the-curve values inside the figure | (a) caption only; (b) also as text in the panel | (a): the caption already carries them (spec rule 3) |
| O4 | Output folder | (a) `scripts/b_figs/out` (default of the existing scripts, `--out` overrides); (b) the held `figures/` folder of spec rule 7 | (a), with `--out` available for (b) |
| O5 | Counts in the legend | (a) "(n = 30)" and "(n = 1093)", both in Table 7 [n337, n338]; (b) no counts | (a) |

Nothing else is open. The script was run only with `--selftest` on synthetic data; it has not read the real inputs.
