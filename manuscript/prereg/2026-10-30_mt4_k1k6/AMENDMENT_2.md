# MT4 confirmatory PREREG, AMENDMENT 2 (DRAFT): the three-tier gate of Branch K1+K6

**Label: PREREG AMENDMENT.** It amends `manuscript/prereg/2026-10-28_mt4_kv/PREREG.md` (PREREG below) for Branch K1+K6 only.
It is not the §8 cost-only amendment. That one is DEV_RULE §8 (685e4dd6), the first and only one.
This file adds nothing to it and changes nothing in it.

**Status: DRAFT v3, 2026-10-31, written blind.** v2 applied CC-205 (panel 3/3, GO-with-fixes, 92) W3–W9 and W12; v3
applies the Codex read (`manuscript/reviews/MT4_AMEND2_codex_read.md`, 55) items 1–3.
- No K1, K6 or base8_s adapter or decode exists. Tier 1 has not been launched; `outputs/mt4_k1k6` is absent from the
  M1 mirror at 00:50Z.
- No T2-2000 image has been staged for or decoded by any K1, K6 or base8_s system.
  - All 2,000 T2 ids are in C-EN's retrieval memory (DEV_RULE §1 disclosure), and M1 holds `datasets/cen_memory`
    (111,927 COCO train/restval images; launch request B2). So T2 bytes may sit on M1, but only inside that C-EN
    folder.
  - The laptop mirror excludes `ncs-data/`, so this can be neither confirmed nor ruled out from the laptop.
  - Tier 1's guard refuses the T2 ids, so that folder must be parked before tier 1.
  - The W25-K1 exclusion features were the only other T2 fetch: laptop tmpfs, deleted and logged
    (AMENDMENT_W25K1 §3).
- No `kv4224.txt`, `t2_gold.json` or `kv_gold.json` exists, and no KV image or prediction exists.
- No rule below depends on a tier-1 number. Each tier-1 outcome is a branch in Part B, written now.

**Tier: IRREVERSIBLE** (PI-1029o: actionable at ≥ 92, band 92–98, ranked options). It binds only after all of these:
1. the PI's explicit YES to the re-asked CC-175 Q1 (CC-205 ruling 7, W1): **met, PI-1031e** (LOG l.986,
   2026-10-31T02:35Z, "Đồng ý cả 5"). It approves AMENDMENT_2 with D_K 2027-02-28T12:00Z, after W1–W12, the Codex
   read and the diff read. PI-1031e also answers CC-205 Q2–Q5: top-up, the freeze-wait exception, a one-seed H-B1
   descriptive only, and the spend;
2. the 3-judge panel: done, CC-205, GO-with-fixes 3/3 at 92. It reads all of `k1k6.py` (CC-189 W7);
3. a Codex read (CC-205 W2);
4. a one-judge read of this revised text and the full diff (CC-205 W2);
5. the gatekeeper's commit, before tier 1 ends, of:
   - this file, renamed `AMENDMENT_2.md`;
   - `AMENDMENT_2_k1k6.diff` applied to `scripts/mt4_k1k6/k1k6.py`;
   - a one-line pointer **`2026-10-28_mt4_kv/AMENDMENT_2_K1K6.md`**, a new file. `AMENDMENT_COST_K1K6.md` stays
     byte-unchanged (CC-205 W3);
   - **all three `SHA256SUMS` files** (CC-205 W4): `2026-10-30_mt4_k1k6/SHA256SUMS` (this file);
     `2026-10-28_mt4_kv/SHA256SUMS` (the pointer); `scripts/mt4_k1k6/SHA256SUMS` (`k1k6.py` → the A3 pin). Without
     the scripts line, every tier FAULTs at the job selftest.

   GATES `AMEND2` then gets that commit's **OPS** LOG id; a CC id does not match `GATE_RE`. The commit message and this
   file cite CC-205 ruling 6, which explicitly overrules the CC-188 l.83 / W4 timing ("AMEND2 panel after A is
   submitted"), citing PI-1031b (keep M1 busy) and do-work-early. The commit is approved by PI-1031e. A preempts at step boundaries only.

All of it must happen **before the first tier-2 step** (DEV_RULE l.15). It may also happen before tier 1 ends; that is
the preferred order, because the text is then committed before any K1 output exists. **Fallback (DEV_RULE l.18):** if
this file is not committed before the first tier-2 step, Branch K1+K6 is HELD → TO-PI, and there is no KV look.

**Sources:**
- PREREG §1, §2 l.39–43, §3, §5 l.88–106, §8 l.144–145, §10;
- AMENDMENT_1 A0, A3, A5 (l.119: Branch K1+K6 keeps its own freeze rule);
- DEV_RULE §1, §6, §7, §10, §14 (sha 685e4dd6);
- AMENDMENT_W25K1 l.78 and §7 (77359031);
- CC-175 r3, W3, W7, W9, N3, R2-1, R2-2 and Q1;
- CC-188 W4 (timing overruled by CC-205 r6); CC-189 W7; CC-190 W3; CC-205 rulings 1–9, W1–W12;
- PI-1029m, PI-1029n, PI-1029o, PI-1031b, PI-1031e.

**Scope (DEV_RULE l.16–17, CC-175 W9).** This amendment holds only:
- the T2 gate and its outcomes (A1);
- the K1+K6 freeze mechanics (A2);
- the KV gold and scorer pins (A3).

It also holds three items that other rulings routed to it:
- the byte pins of the staged sets (A4, from AMENDMENT_W25K1 l.78);
- matcher v1 beside v2 (A5, from CC-175 N3 and R2-2);
- the HOLDs before tiers 2 and 3 (A6).

Caps, rates, the ladder and D_K belong to the cost-only amendment. They are restated in Part C only, as planning.

---

# Part A: binding text (replaces or adds PREREG text for Branch K1+K6)

## A1. PREREG §5: the T2 gate (new text after l.103)

PREREG has no T2 gate. §5 l.95 says "This PREREG fixes the test side only". New text:

> **Three-tier gate (Branch K1+K6; PI-1029n).**
>
> **The KV look and its licence.** The one KV look (§2) is licensed only by an anchored **T2_PASS**. T2_PASS is the
> verdict of a rehearsal on T2-2000 (`t2_ids.txt`, sha 298ae5e1; DEV_RULE §1), a set never used for selection.
>
> **The rehearsal.** It runs the registered analysis of §3 and §5 exactly:
> - the same `hyp()` that scores KV;
> - B = 2,000, `default_rng(0)`, one shared draw, K1 seeds pooled;
> - the H-B1 and H-B2 forms of l.102–103.
>
> It also computes the predicted P(PASS on KV-4,224) with the two-level bootstrap of DEV_RULE §6 (`p_pass`,
> R = 2,000).
>
> **The rule.** The rule is `k1k6.t2_rule` at the scorer sha of A3. `t2_decide.json` is written once (O_EXCL).
> - **T2_PASS** iff all of: H-B1 holds on T2; every K1 seed's short-caption language-fail share is ≤ 2%;
>   P(H-B1 on KV) ≥ 0.98.
> - **K6 is kept for KV** iff T2_PASS and also: H-B2 holds on T2; K6's language-fail share is ≤ 2%;
>   P(H-B1 ∧ H-B2) ≥ 0.98.
>   - Otherwise K6 is not decoded on KV, and H-B2 reads "not tested (K6 failed the tier-2 rehearsal)".
>   - A K6 cut by the committed `caps.json` reads "not tested (cost)".
> - **T2_FAIL** otherwise: no KV look for this branch, ever. The T2 numbers are reported briefly as a development
>   result (PI-1029m) and go TO-PI under the pivot rule.
>
> **The anchor.**
> - The gatekeeper anchors the file's sha in `t2_decide.sha256` and fills GATES `T2` with that commit's LOG id.
> - The gatekeeper refuses to anchor a `t2_decide.json` in any of these cases:
>   - its `scorer_sha256` is not the A3 pin;
>   - its `scorer_closure` differs from the committed shas of the A3 closure files;
>   - its `inputs_sha256` do not equal the pulled prediction files.
> - Tier 3 reads the kept set only from the anchored file (`kv_ready`), never from a caller.
>
>
> **K1 seed count (CC-205 ruling 3, W5b; PREREG l.42, l.142, l.145).** If the committed `caps.json` applies the
> ladder step "cut K1 seed 2", H-B1 is **not confirmatory**. This is enforced in code (Codex 1). `k1k6.py left` prints
> 0 for every stage of such a `caps.json`, so the frozen job's `cost` path writes `K1K6_COST.txt` before the first
> tier-2 stage. No K1 seed 1 or K6 training runs, and l.49 closes the branch for every later tier. It is reported as descriptive only, and the branch gets
> no confirmatory KV look on H-B1. H-B2 needs H-B1 first in the fixed sequence, so no H remains. The branch is then
> NOT-RUN (cost) → TO-PI, settled before any confirmatory training. KV-4,224 stays unspent. The PI accepted this in
> PI-1031e (CC-205 Q4). (J3 dissents: it would accept a disclosed one-seed test. That form needs a new irreversible
> ruling.)
>
> **Before T2, tier 1** (val 924, DEV_RULE §5) may end in T1_FAIL. That covers no qualifying checkpoint and the
> futility stop (best ΔF1 < +2.0). It may also end in NOT-RUN (cost): the re-priced caps exceed the test line after
> the ladder. Each of these ends the branch before any confirmatory training: no tier 2, no KV look, TO-PI.

**Report sentences, added to §10 (Branch K1+K6):**
- **T1_FAIL:** "On the development set, fine-tuning on all available Vietnamese gold captions did not reach the
  pre-registered selection rule (best ΔF1 X on val 924, SESOI +2.0); per the rule, no confirmatory system was trained
  and the test set was not used. It is reported as a development result."
- **T2_FAIL:** "In the pre-registered dress rehearsal on 2,000 held-out development images, fine-tuning did not meet
  the licence for the test look (ΔF1 X [CI]; predicted P(PASS) Y < 0.98); per the rule, the test set was not used. It
  is reported as a development result."
- **K6 not kept:** "H-B2 was not tested: K6 did not pass its pre-registered rehearsal."

## A2. PREREG §2 l.39–40 for Branch K1+K6: the freeze

Old (l.39–40): "**Freeze, about 11-18 (VN).** … The gatekeeper's commit of `KV_PRED_SUMS` with the shas of the KV gold,
`kv4224.txt` and the scoring code is the freeze." and "**A system not in `KV_PRED_SUMS` at the freeze loses
confirmatory status** …".

New, for Branch K1+K6. AMENDMENT_1 A3's mechanics apply, with D_K in place of D:

> **Freeze (Branch K1+K6).**
> - **Writing the lines.** When a KV decoder finishes, `k1k6.py kvsums` appends its line `SHA  FILE  SYSTEM  UTC` to
>   the one constant path `manuscript/prereg/2026-10-30_mt4_k1k6/KV_PRED_SUMS` on M1, fsynced. UTC comes from the
>   code, never from a hand.
>   - No one opens a KV prediction (unchanged).
>   - Laptop backup copies of the prediction files are compared by sha only and are never opened.
> - **The kept set** = `kv_kept` of the anchored `t2_decide.json` (A1). The descriptive K1 seed 1 detailed row is
>   outside it.
> - **Which lines count.** The first line per system counts.
>   - Another sha for a kept system halts the freeze (FAULT → PI), also after D_K. A same-sha repeat is descriptive.
>   - Lines out of order, or earlier than the `utc` of the anchored `t2_decide.json`, halt it.
>   - Lines outside the kept set, or after D_K, are descriptive.
> - **The freeze instant** = min(UTC of the line that completes the kept set + 24 h, **D_K = 2027-02-28T12:00:00Z**).
>   `kvscore` refuses before it.
> - **The log decides.** The freeze is fixed by the log, the kept set and D_K, which are all fixed now. The
>   gatekeeper's later commit of `KV_PRED_SUMS` (with `mt4_k1k6_decide.json`) records the frozen set; its timing
>   changes nothing. The committed file must equal the M1 file byte for byte.
> - **Missing rows** (DEV_RULE §7, W1). A kept system missing at the instant loses confirmatory status.
>   - A missing base8_s or K1 seed row makes H-B1 NOT-RUN and stops the sequence.
>   - A missing K6 short, K6 detailed or base8_s detailed row makes only H-B2 NOT-RUN.
>   - The descriptive row never affects either.
> - **Scoring** is one run of `k1k6.py kvscore` on M1 (the m3 role), after the instant. It writes
>   `mt4_k1k6_decide.json` once (O_EXCL). That write is the look.
> - **One attempt (Codex 2).** The order inside `kvscore` is fixed:
>   1. `kv_ready`, then the closure check (A3);
>   2. `freeze_set` reads `KV_PRED_SUMS`, which holds shas and times only. Before the instant it exits HELD and writes
>      nothing, so an early call costs nothing;
>   3. `kvscore` creates `kvscore_attempt.json` O_EXCL and fsynced, holding the time, the closure sha and the frozen
>      set;
>   4. only then is any KV gold or prediction read.
>
>   `kv_ready` refuses whenever the marker exists, for scoring and for KV decoding. Any failure after the marker (a
>   crash, a FAULT, a host loss) is therefore **terminal**: NOT-RUN (fault) → TO-PI, with no rerun without a new
>   irreversible ruling. There is no rescoring, and no matcher or gold change
>   (§2 l.41–42 unchanged). M1 must therefore stay rented until the scoring run ends.
> - **Threat model:** AMENDMENT_1 A0, out-of-scope list unchanged. Host clock skew in the UTC column is checked only
>   for order and against the T2 anchor time.

## A3. PREREG §1: gold and scorer pins

- **Gold definition.** `t2_gold.json` and `kv_gold.json` are written by `k1k6.py gold --set t2|kv`, from
  `instances_val2014.json` (pin e1b4d1bc). They use the definition of `gold_instances.json`: COCO-2014 instance
  classes, 80 categories, crowd included. The output is deterministic, given the pinned inputs and `t2_ids.txt` /
  `kv4224.txt`.
- **`t2_gold.json`.** Built on the laptop, with counts only on stdout. It is committed, with a line in this folder's
  `SHA256SUMS`, **before the tier-2 launch HEAD**. The job's `sha256sum -c` (k1k6_job.sh l.67) then enforces it at
  every tier-2/3 start, and `t2decide` reads it only if it equals HEAD.
- **`kv_gold.json`.** Built on the laptop after `kv4224.txt` (pin 86d93863) is committed by its own, separately
  judged `id_counts.py` writer (O-1). Counts only are printed, and nobody opens the file.
  - It is committed with a `SHA256SUMS` line **before the tier-3 launch HEAD**, so l.67 refuses KV staging without it.
  - This is stricter than §1's "before the freeze".
  - `kvscore` reads it only if it equals HEAD, and checks `kv4224.txt` against 86d93863.
- **Scorer pin.** `scripts/mt4_k1k6/k1k6.py` at the sha committed with this amendment. With the v2 diff it is
  `7dbca3c4d4bbe39f0e07bbb9b7f0d7de738f4d4d6875bb6dc0933e17e8569534` (v1: ec959982…, v2: 5c5766ca…); the gatekeeper writes the
  final sha here at the commit. `t2_decide.json` and `mt4_k1k6_decide.json` record `scorer_sha256`.
- **Scorer closure (CC-205 W5).** The closure is every repo file the scorer loads, `k1k6.SCORER_CLOSURE`:
  - `scripts/mt4_k1k6/k1k6.py`;
  - `scripts/grl/{common,k2_gate0,reward}.py`;
  - `scripts/{score_coco_probe,clean_supervision,rl_reward,person_uncap}.py`;
  - `rescap/{__init__,chair,metrics,repro,vocab}.py`, `rescap/svp/{__init__,entailment,matching}.py`,
    `rescap/vi/{__init__,classifier,color,lexicon}.py`;
  - `data/coco_probe/coco80_vi.json`.

  How the closure is enforced:
  - A closure file that is missing is a SystemExit FAULT, not a FileNotFoundError (Codex 3).
  - `t2decide` writes `scorer_closure` (file → sha256) into `t2_decide.json`, which is then anchored.
  - `kvscore` compares the current closure with the anchored one right after `kv_ready`. On any difference it
    FAULTs, **before it reads `KV_PRED_SUMS`, any prediction or any gold** (NOT-RUN (fault) → TO-PI; KV not read).
  - The selftest asserts that a fresh process that imports `k1k6.py` and scores v1 and v2 loads no repo file outside
    the list, and that a changed, missing or absent entry FAULTs.
  - Any edit of **any closure file** between the A3 commit and the look needs a new irreversible ruling. This covers
    the shared `grl`/`rescap` modules too, so other studies must not edit them while this branch is open. Python and
    numpy are not in the closure: M1's `/root/vsps/.venv` stays as it is between `t2decide` and `kvscore`, logged by
    `pip freeze` sha at both steps.

## A4. Byte pins of the staged sets (code; AMENDMENT_W25K1 l.78)

- **T2 (tier 2).** Every staged T2 body must equal its row of C-EN `fetch/memory.sha256.tsv` (pin 553fb604; 2,000 of
  2,000 T2 ids present), else FAULT and the body is not written. The refused-sha check stays as well.
- **KV (tier 3): a defect in the committed code, fixed here.**
  - `common.refused_sets()` includes the C-EN Karpathy-val record (`coco_kval.sha256.tsv`; 5,000 of 5,000 KV ids).
    So at k1k6.py f2273b90, `stage --set kv` refuses every KV body ("refused image by sha256"), and the tier-3 guard
    would refuse every staged KV file. Tier 3 cannot run as committed.
  - **New rule:** in tier 3 only, a KV-4,224 file may exist only under `datasets/k1k6_kv/`, and only if its sha256
    equals **its own** row of `coco_kval.sha256.tsv`. That record is pinned now at
    `8c93f306f24588fb6e66eed0a8ba2ba97e61adf901ddf5ab614b37d5b677ee1c` (laptop mirror of M1). The gatekeeper checks
    the M1 copy before tier 3.
  - Every other refused id and sha is still refused. This makes DEV_RULE §7 l.214–216 exact, and it is no new
    licence: the same ids and the same folder, now with a byte pin.
  - **Form (CC-205 ruling 1, Q7 = (a)):** the own-row exemption. Reading ids and shas only from that record is not
    test data (CC-205 r1).
  - **Check at the `kv4224.txt` commit (W8):** 0 own-row shas of the 4,224 ids lie in exclusion.json
    `image_sha256`, `coco_test` or `nocaps_val`; else FAULT → judge. CC-205 found the 61 `coco_kval` shas in
    exclusion.json all belong to the 130 removed ids.
  - **Missing ids (W8):** a `kv4224.txt` id with no record row is a SystemExit FAULT in `cmd_guard`, never a KeyError.
- **Code.** `cen_record` (pinned record loader) and `stage_check` (refused-sha rule plus own-row pin), called before
  any byte is written. `scan_k1` and `cmd_guard` take `kv_ok` as {id: sha} instead of a set of ids.

## A5. Matcher v1 beside v2 (code; CC-175 N3, R2-2; PREREG §1 l.31)

- **Definition.** `row_v1` = `k2_gate0.row` with the v1 class lexicon in place of v2. Everything else is the same:
  - the same negation and hedge split (an unasserted class is a mention and never a TP);
  - the same `untruncate`, P/R/F1 and CHAIR_i;
  - the same bootstrap draw.
- **Where it is written.** `v1_desc` writes the v1 block inside the same one-shot records: `tier2_matcher_v1` in
  `t2_decide.json` and `kv_matcher_v1` in `mt4_k1k6_decide.json`. It has to be inside them, because nothing is
  rescored after a look.
- **No gating role.** The block has no `holds` or `tested` fields, and `t2_rule` and `kvscore` never read it.
- **Label (CC-205 W9):** "v1 class lexicon with the section-1 negation/hedge rule". This differs from `score_dev.py`'s
  negation-blind v1. The definition was fixed **after** the val-924 planning numbers were seen: 786 of 1,848 rows
  differ, ΔF1 +13.4 under v1 vs +5.7 under v2. It is descriptive only and never gates.
- **Failure:** a v1 exception never blocks the v2 write (`v1_safe`). The block then holds only the exception type.

## A6. HOLDs (preconditions; no rule change)

| Tier | Holds until |
|---|---|
| 2 | Gates and code: GATES `T1` and `AMEND2` (OPS ids); `t1_select.json` and `caps.json` committed and equal to the M1 copies (W4); `t2_gold.json` committed with a SUMS line; `k1k6.py` = the A3 pin |
| 2 | M1 files: 4B snapshot pins (O-2); `instances_val2014.json` on M1 (O-5); C-EN `memory.sha256.tsv` at 553fb604 |
| 2, 3 | **Money and rental (CC-205 ruling 8, W7).** Before the tier-2 launch, and again before KV staging, the gatekeeper logs the M1 ckey balance end and the rental end. Each must fall at or after the projected tier-3 end at caps, plus the 24 h freeze, plus `kvscore`, plus one fault rerun, plus 12 h. Otherwise NOT-RUN (cost), KV unspent |
| 2 | **Custody (CC-205 ruling 9, W11):** no AMEND2 bundle or fast-forward reaches M1 before `runs.log` shows "tier 1 done" and `t1_select.json` and `caps.json` exist on M1 |
| 3 | The above, plus: GATES `T2` (anchored T2_PASS); `kv4224.txt` (O-1, separately judged) at 86d93863; `kv_gold.json` committed with a SUMS line; C-EN `coco_kval.sha256.tsv` on M1 at 8c93f306; no `KV_PRED_SUMS` and no `mt4_k1k6_decide.json` on M1 |

**Exception to PI-1031c (CC-205 W7; PI Q3).** M1 is not deleted between the first KV decode and the `kvscore` write.
Deleting it would destroy the authoritative `KV_PRED_SUMS`. Other approved jobs may use the freeze wait only after
`k1k6_kv/` is deleted and the guard passes. The PI granted it in PI-1031e (CC-205 Q3).

## A7. What this amendment does not change

- Every H, threshold, SESOI, matcher used for an H, gold definition and test set; the fixed sequence; seed pooling;
  the bootstrap.
- The one look; the branch rule (§0, AMENDMENT_1 A2).
- The cost-only amendment (DEV_RULE §8): rates, caps formula, ladder, D_K, the test line of 100 GPU-h.
- The English arm (§6); Branch K2 text (AMENDMENT_1 A3/A4).
- `t2_ids.txt`, `w25k1_excluded_keys.txt`; the training, decode, `plan`, `t1_rule`, `hyp`, `p_pass`, `t2_rule` and
  `freeze_set` functions (byte-identical; Part D).

**Disclosures (CC-205 W12).**
- The `decoder_sha256` in the tier-1 prediction records (k1k6.py f2273b90) differs from the one in tier-2/3 records
  (the A3 pin). The decode path itself is byte-identical (Part D).
- `k1k6_lists.json` keeps `script_sha256` 5b73fb81 as written (CC-189 W3).

---

# Part B: branches keyed to the registered tier-1 outcomes (all written now)

| Tier-1 record (`t1_select.json`, `plan` exit) | What follows | AMENDMENT_2 |
|---|---|---|
| **T1_OK, E\* ∈ {1, 2, 3}**, `caps.json` fits with no ladder | Tier 2: K1 s1, K1 s2 and K6 s1 at E\*; T2 stage; 4 short and 2 detailed T2 decodes; `t2decide` → A1 outcomes | binds |
| T1_OK, `n_short` = 256 (> 1% cap hits) | as above, with short decodes at 256 tokens in tiers 2–3; caps as committed (Q4) | binds |
| T1_OK, ladder "cut K6" | K6 not trained or decoded; H-B2 "not tested (cost)"; T2_PASS on H-B1 alone | binds |
| T1_OK, ladder "cut K6" + "cut K1 seed 2" | H-B1 descriptive only, not confirmatory (CC-205 r3). The first tier-2 `left` prints 0, so `K1K6_COST.txt` is written before any training (Codex 1). NOT-RUN (cost) → TO-PI | moot; KV unspent |
| `plan` exit 2 (H systems do not fit 100 after the ladder) | NOT-RUN (cost) → TO-PI; `K1K6_COST.txt` closes the branch | moot; KV unspent |
| **T1_FAIL** (no checkpoint with lang ≤ 2% and ΔP ≥ −1.0) | `t1_select.json` has no "epochs", so `plan --t1` exits 1 and no `caps.json` is written. The frozen job still logs "tier 1 done"; the operator's OPS line records "tier 1 done (T1_FAIL, no caps)" (CC-205 W6 i). No tier 2, no KV look; dev result; A1 sentence; TO-PI (pivot rule) | moot; KV unspent |
| **T1_FAIL, futility** (best ΔF1 < +2.0) | same | moot; KV unspent |
| tier-1 exit 124 or cost stop (`K1K6_COST.txt`) | NOT-RUN (cost) → TO-PI (W6 ii) | moot; KV unspent |
| FAULT in tier 1 | rerun from the failed step (ledger charges per DEV_RULE §8) | unchanged |

| Tier-2 record (`t2_decide.json`) | What follows |
|---|---|
| **T2_PASS, K6 kept** | Tier 3, kept set: short base8_s, K1 s1, K1 s2, K6 s1; detailed base8_s, K6 s1; then the descriptive K1 s1 detailed row, from what is left |
| **T2_PASS, K6 not kept** | Tier 3 without the K6 rows; H-B2 "not tested (K6 failed the tier-2 rehearsal)" |
| **T2_FAIL** | No KV look, ever; dev result (A1 sentence); TO-PI. KV-4,224 stays unspent and reserved by the PREREG |
| exit 124 or cost stop in tier 2 | NOT-RUN (cost) → TO-PI, never a negative result; KV unspent |
| FAULT in tier 2 (W6 iii) | rerun from the failed step (`.done` reuse, ledger charges); `t2decide` is one-shot, so a FAULT after its write goes to the judge; KV unspent |
| a kept T2 system's file missing because its stage hit the remainder (W6 iv) | `t2decide` FAULTs (file missing); labelled NOT-RUN (cost) → TO-PI, KV unspent |

| Tier-3 event (W6 v) | What follows |
|---|---|
| FAULT, exit 124, cost stop, or M1 lost **before** the first `kvsums` line | NOT-RUN (fault/cost) → TO-PI. No KV prediction exists, so KV-4,224 is unspent, but a re-stage needs a one-judge ruling |
| the same **after** the first `kvsums` line | NOT-RUN (fault/cost) → TO-PI. **KV-4,224 counts as spent** for this branch. No re-decode on any host without a new irreversible ruling |
| `kvscore` closure FAULT (A3) | NOT-RUN (fault) → TO-PI; nothing read; KV spent (predictions exist) |
| any failure after `kvscore_attempt.json` exists (Codex 2) | terminal: NOT-RUN (fault) → TO-PI; `kv_ready` refuses every rerun; KV spent |

"KV unspent" means KV-4,224 stays reserved by the committed PREREG. It is not reassigned without a ruling.

---

# Part C: planning annex (NOT binding; estimates are AI opinion)

**GPU-h after tier 1, caps at planning rates (`plan()`; illustrative).** The binding numbers are the committed
`caps.json`.

| E\* | Training (3 runs) | Tier 2 decodes | KV H rows + staging | KV descriptive | Total cap | Projection (pool 14,104) |
|---|---|---|---|---|---|---|
| 1 | 9.3 | 12.6 | 27.8 | 9.3 | **59.0** | ≈ 48 |
| 2 | 17.7 | 12.6 | 27.8 | 9.3 | **67.4** | ≈ 55 |
| 3 | 26.4 | 12.6 | 27.8 | 9.3 | **76.1** | ≈ 61 |

`plan()` prices training at the screening n 15,249, not the training pool 14,104 (AMENDMENT_W25K1 §7). That
overstates the training caps by about 8%. It is conservative and is left as committed.

**M1 calendar (VN = UTC+7; E\* = 3; worst case at projection):**

| When (VN) | M1 | Gate / laptop work |
|---|---|---|
| 10-31 07:30 → ~10:00 | C-T3 (running, cap 2.5) | AMEND2 panel + Codex in parallel (this request) |
| ~10-31 → ~11-01 morning | A-T3 tier 3 (~17–20 GPU-h; every cell starts before 11-07 07:00) | O-1 `kv4224.txt` writer read (separate, one judge); `t2_gold.json` built |
| ~11-01 → ~11-01 20:00–23:00 | MT4 tier 1 (cap 11.1, ~13 h wall) | AMEND2 diff read + commit, ideally **before** tier 1 ends |
| ~11-01 23:00 | — (≤ 2 h gap) | T1 commit (`t1_select`, `caps.json`, GATES T1); M1 fast-forward; tier-2 launch |
| ~11-02 → ~11-03 06:00 | Tier 2 (≈ 31 h at E\* = 3; 24 h at E\* = 2; 18 h at E\* = 1) | — |
| ~11-03 morning | — (≤ 3 h gap) | `t2_decide` pull, anchor and GATES T2; `kv_gold` built and committed; tier-3 HEAD |
| ~11-03 → ~11-04 16:00 | Tier 3: KV H rows ≈ 23 h, then the descriptive row ≈ 8 h, then delete | — |
| ~11-05 ≈ 09:00 | `kvscore` on M1 (freeze instant = H set complete + 24 h) | anchor + commit `KV_PRED_SUMS`, decision |

**Money.**
- The M1 balance runs out at about **23:00 VN 11-04** (audit; 1,051,025 VND at 05:45 VN 10-31, 9,282 VND/h).
- The chain above needs M1 alive until about **11-05 noon VN**, plus room for one host-loss rerun.
- A top-up of **≥ 0.5 M VND (≈ 54 h)**, about **1.0 M** with one fault, is due before **11-02 12:00 VN**, with the rental
  running past ~11-06 noon VN. The PI approved both in PI-1031e (CC-205 Q2). The A6 gate still checks the logged
  balance end and rental end before each launch.
- If the balance reaches 0 in tier 3, the KV images die with the host (custody: COCO public images). An open start is
  charged in full, and `kvscore` cannot run off M1. Warn the PI ≥ 12 h ahead.

**Preemption.** "A preempts" (CC-189) is done by the operator, at a **step boundary only**: wait for the step's end
ledger line, then end the tmux session; the rerun reuses `.done` steps. Ending a session inside a step leaves an open
start, which is charged its full timeout (8.8 h for a training step at E\* = 3). One such loss uses about the
descriptive row's 9.3 h; two put the H rows at risk.

**Custody checklist (operator and gatekeeper; the gates above enforce most of it).**
0. **No M1 fast-forward while tier 1 runs (binding: A6, CC-205 ruling 9).** The AMEND2 commit may land on the laptop at any time. M1 moves to it
   only after tier 1 has written `t1_select.json` and `caps.json`. The job runs `k1k6.py` from the working tree at
   every step and the guard checks HEAD = EXPECT_HEAD, so a mid-run move would FAULT tier 1, or run its later steps
   on the new code.
1. **Tier-2 HEAD.** It holds this amendment, `k1k6.py` = the A3 pin, all three SUMS, `t1_select`/`caps.json`, `t2_gold`,
   GATES T1/AMEND2. M1 is fast-forwarded by git bundle; both `sha256sum -c` OK; porcelain clean.
2. **Tier-2 job.** It stages T2 with the A4 pin and runs the guard, then trains, decodes and runs `t2decide`.
3. **T2 pull and anchor.** Pull `t2_decide.json` and the T2 predictions pull-only. Check `scorer_sha256` = A3 pin,
   `scorer_closure` = the committed closure shas, and `inputs_sha256` = the pulled files. Anchor `t2_decide.sha256`, fill GATES T2 (OPS id) and push. Branch protection
   on q2 main is ON (PI-1029n).
4. **Before tier 3.** `kv4224.txt` (O-1) committed; `kv_gold.json` built (counts only) and committed with SUMS. The
   M1 `coco_kval.sha256.tsv` = 8c93f306. Verify that the laptop backup loop still excludes `ncs-data/` (KV images are
   never mirrored). `KV_PRED_SUMS` and `mt4_k1k6_decide.json` are absent on M1.
5. **Tier-3 job.** It runs `kvready`, then KV staging into `k1k6_kv` only (own-row pin), then the guard, the kept-set
   decodes and `kvsums`, then the descriptive row last. It then runs `rm -rf k1k6_kv`, logs it in `deletions.log` and
   runs the guard again.
6. **Scoring.** After the instant, `TIER=3 SCORE=1` on M1. Pull, anchor the decision sha, and commit it with
   `KV_PRED_SUMS` (record only). There is no rerun: a FAULT goes TO-PI.

---

# Part D: code (`AMENDMENT_2_k1k6.diff`, not applied; tracked `k1k6.py` stays f2273b90 for tier 1)

- **Size.** `git apply --check` is clean against HEAD. The new sha is `7dbca3c4…8569534` (A3); 245 changed lines,
  including the selftest. In a scratch copy with `scripts/mt4_k1k6/SHA256SUMS` updated to the new sha, `bash
  k1k6_job.sh --selftest` passes; the job itself is unchanged (27d2b431).
- **Changed functions:** `cmd_stage`, `scan_k1`, `cmd_guard`, `short_counts`, `detailed_counts` (a `ver="v2"`
  default), `load_set`, `cmd_t2decide`, `cmd_kvscore`, `cmd_left` (the Codex 1 branch stop), `kv_ready` (the Codex 2
  marker refusal), `selftest`.
- **Added functions:** `cen_record`, `stage_check`, `row_v1`, `v1_desc`, `v1_safe`, `closure`, `closure_check`,
  `kv_attempt`; added constants `SCORER_CLOSURE`, `V1_LABEL` and `KV_ATTEMPT`.
- **Byte-identical function bodies** (AST compare): `cmd_train`, `cmd_decode`, `load`, `plan`, `t1_rule`,
  `pool_rows`, `drop_trunc`, `example_plan`, `cmd_gold`, `prf`, `chair`, `pool_seeds`, `hyp`, `p_pass`, `t2_rule`,
  `freeze_set`, `cmd_kvsums`. `k1k6_job.sh` is unchanged.
- **No other caller.** A grep of `scripts/` finds no caller of the changed signatures outside `k1k6.py`: `scan_k1`
  (`kv_ok` is now a dict), `cmd_stage` (now `rec`), `short_counts` and `detailed_counts` (now `ver`). `w25k1_prep.py`
  does not call them.
- **Selftest** (`python3 k1k6.py --selftest`, scratch copy): ok. New cases:
  - the v1 block equals the v2 numbers on identical rows and carries no `holds`/`tested`;
  - `row_v1` calls the lexicon with "v1" only;
  - `stage_check` passes a matching T2 row and a KV own row, and FAULTs on: another sha, a missing row, a refused T2
    sha, a KV sha that is not its own row;
  - an unpinned C-EN record is refused;
  - closure: equal passes; a changed sha, a missing entry, an empty or absent anchor FAULT. A fresh-process probe finds
    no repo module outside `SCORER_CLOSURE`; a mutation test that drops `scripts/person_uncap.py` from the list fails
    the selftest;
  - `v1_safe` records an exception type instead of raising;
  - Codex 1: a `caps.json` with "cut K1 seed 2" makes `left` print 0, and with "cut K6" alone it does not;
  - Codex 2: after the attempt marker and a simulated crash, both `kv_ready` and a second marker are refused;
  - Codex 3: a missing closure file is a FAULT;
  - mutation tests: removing the marker refusal, or the seed-2 stop, fails the selftest;
  - `scan_k1` passes a KV file under the KV root only with its own row, and refuses another sha, no row, or the
    wrong root.
- **Real-file checks (laptop, CPU, ids, shas and dev counts only):**
  - the C-EN mirror records hold 2,000 of 2,000 T2 rows (553fb604) and 5,000 of 5,000 Karpathy-val rows (8c93f306);
  - on the two val-924 planning prediction files (47f3e0ba, 6120c566), the old and new v2 `short_counts`,
    `detailed_counts` and `hyp()` outputs are identical;
  - the v1 rows differ from v2 on 786 of 1,848 image rows (Q6).
