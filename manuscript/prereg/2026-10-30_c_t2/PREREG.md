# C-T2: tier-2 DEV-CONFIRM rehearsal prereg for Paper C (Flickr30K val, the five C-T1 NOMINATE claims)

Status: DRAFT v1, written 2026-10-30 under ruling CC-191 (GO-with-fixes, 91%; W1-W5 applied here, W6 optional and
not part of this prereg). Nothing here has run. Not committed. This is AI opinion, not expert-validated.
Label on every output: `TIER 2 / DEV-CONFIRM (C-T2)`. Launch read: irreversible tier (the run uses Flickr30K val's
single look), bar ≥ 92 (band 92-98, PI-1029o); the judge reads this file and `diff scripts/c_t1/c_t1.py
scripts/c_t2/c_t2.py` (JUDGE_READ_REQUEST.md).
Code: `scripts/c_t2/c_t2.py` (a copy of `scripts/c_t1/c_t1.py` sha256 `022af90e` with the minimal W1 change; CPU
selftest `python3 scripts/c_t2/c_t2.py --selftest`), `scripts/c_t2/c_t2_job.sh`. Tier-1 files are not edited.
Tier-1 anchor: commit `0bf52da`; `T1_SUMMARY.json` sha256 `7d5b2918…dfda6`; carve ledger `carve_coco.jsonl` sha256
`4ced15b4…5615` (pinned in `c_t2.py` for pooling).

## 1. What tier 2 is, and what it is not

The three-tier method (PI-1029n): tier 1 explored on dev (the C-T1 carve), tier 2 rehearses the candidate
claims once on a split never used for selection (Flickr30K Karpathy val, 1,014 images), and only claims that pass the
rehearsal with margin may go to the one test look (Flickr30K Karpathy test, 1,000 images, tier 3, its own prereg). A
claim that fails tier 2 never touches test. Tier 2 makes no paper claim by itself: its rows enter C as labelled dev
rows, beside C's registered Vietnamese P1 and C-EN P1-EN verdicts, which are unchanged.

| set | tier-2 use |
|---|---|
| Flickr30K Karpathy val (1,014) | **the tier-2 set, all 1,014 images, one look** (never used in tier 1; C-T1 PREREG §1) |
| Flickr30K Karpathy test (1,000) | **refused** (C's one-look set, tier 3). Never extracted from the zip, never staged; every data command refuses its 1,000 file names |
| Flickr30K carve (1,000 train) | not decoded again; its tier-1 per-image differences (ledger `4ced15b4`) are pooled with val for the predicted P (§8 rule) |
| every spent or other-owner set (C-T1 PREREG §1 table) | never |

## 2. Claims (exactly the five C-T1 NOMINATE claims; CC-191 r4)

From `T1_SUMMARY.json` (carve, n = 1,000, PTB CIDEr-D, SESOI +2.0):

| id | claim | carve d [95% CI] | tier-1 planning P (m = 1 / m = 5) |
|---|---|---|---|
| E1 | Aya-Vision-8B `ret` − `rand` d0 | +6.12 [+3.47, +8.78] | .997 / .987 |
| E2 | Qwen2.5-VL-7B `ret` − `rand` d0 | +5.04 [+2.39, +7.67] | .969 / .906 |
| E3a | Aya-Vision-8B `ret` − `lmcap_ri` | +28.14 [+24.84, +31.44] | 1.000 / 1.000 |
| E3b | InternVL3-8B `ret` − `lmcap_ri` | +41.08 [+37.55, +44.74] | 1.000 / 1.000 |
| E3c | Qwen2.5-VL-7B `ret` − `lmcap_ri` | +40.79 [+37.36, +44.53] | 1.000 / 1.000 |

No claim is added or removed. Qwen E2's tier-1 P of .906 at m = 5 is a planning number; removing E2 now would be a
selection that C-T1 §8 does not allow (CC-191 r4). InternVL3 `ret` − `rand` (−1.00 on the carve) was never a §8
candidate (§8 lists E1 for the third backbone, E2 for Qwen, E3 for every backbone). The tier-1 summary code labelled
it "DROP" because it labels every backbone's `ret` − `rand`; that label is a code-versus-prereg naming mismatch (W4).
It is recorded here, it is not "a dropped claim", and InternVL3 `rand` is not decoded at tier 2. The tier-2 code
names the five claims explicitly (`T2_CLAIMS`), so no other contrast can carry a claim label (asserted by the
selftest).

## 3. Tier-2 and tier-3 rules (C-T1 PREREG §8, copied verbatim)

Source: C-T1 `PREREG.md` lines 239-250 (sha256 `f1d06278`), unchanged:

- **Tier-2 and tier-3 rules, fixed now (W7; copied verbatim into the tier-2 prereg, never redefined after data):**
  - val PASS per claim = point ≥ +2.0 PTB CIDEr-D AND 95% CI lower bound > 0 (C's A1 form), percentile bootstrap,
    B = 2,000, seed 0, on Flickr30K val (all 1,014 images, never used in tier 1);
  - predicted P(PASS on test, n = 1,000) from the pooled carve ∪ val per-image differences, joint = Φ(z1) + Φ(z2) − 1
    (Fréchet lower bound), z2 = d/SE − Φ⁻¹(1 − 0.05/m) with m = the size of the tier-3 family (CC-172a W12),
    labelled as such;
  - "PASS with margin" (PI-1029n, CC-171 W2 form) = val point ≥ +2.0 AND that pooled predicted P ≥ 0.98;
  - claim family = every claim NOMINATEd here AND passing with margin at tier 2. Tier-3 multiplicity: **Holm over the
    family at α = 0.05** (one-sided bootstrap p for Δ ≤ 0, Holm-adjusted); a claim PASSes at test iff point ≥ +2.0
    AND its Holm-adjusted p < 0.05. Holm is chosen now; no primary claim is named;
  - tier 3 (one look at Flickr30K test; irreversible tier, 92-98 band, PI-1029o) only if both margin conditions
    hold; no low-power route (CC-171 W4).

### 3.1 Clarifications, fixed before any val decode (not redefinitions)

- **C1, the family size m in the predicted P (CC-191 r5).** §8 sets m = the size of the tier-3 family, and the
  family depends on which claims reach P ≥ 0.98, so the rule is circular as written. Resolution, conservative,
  single pass: m = the number of the five claims that **pass val** (A1 form: point ≥ +2.0 AND 95% CI lower bound
  > 0). Each claim's pooled P is computed once at that m. There is no iteration. This mirrors tier 1, which used
  m = the number of entrants. The Holm family size at test (`m_holm`) is the number of claims that enter tier 3 (C2),
  and m_holm ≤ m. The permissive reading (the largest s such that the s-th highest P at m = s is ≥ 0.98) is noted for
  the launch judge only. It was conceived after Qwen's .906 was seen, so it is not the default.
- **C2, entry to tier 3 needs val PASS.** The §8 bullets name val PASS and "PASS with margin" (val point ≥ +2.0 AND
  pooled P ≥ 0.98) separately. Under the three-tier rule (PI-1029n: a claim that fails the rehearsal never touches
  test), a claim enters the tier-3 family iff it is **val PASS AND pooled P ≥ 0.98**. The point ≥ +2.0 part of the
  margin is inside val PASS, so this adds exactly one condition, "95% CI lower bound > 0 on val". This is a judge
  question (JUDGE_READ_REQUEST Q-a); default = this reading.
- **C3, pooled P computation.** The pooled sample is the concatenation of the carve per-image differences (1,000,
  from ledger `4ced15b4`) and the val per-image differences (1,014): n = 2,014. d = pooled mean; SE = pooled SD / √1000
  (the test n); P = `p_pass(d, SE, m)` of C-T1 (Fréchet lower bound, z2 with Φ⁻¹(1 − 0.05/m)). Code: `c_t2.py
  t2_decide`, `cmd_t2`.
- **C4, no kill gate at tier 2.** §8's kill gate was a tier-1 rule; it did not fire (Qwen carve `ret` − `rand` +5.04).
- **C5, missing arms.** A claim whose `ret` or comparator arm was not decoded (cap stop, failure) is NOT RUN, never
  enters the family, and is reported so. No rerun beyond a partial-file resume.
- **C6, InternVL3 τ = 0.10 (PREREG §5 B4, PI Q1 of CC-191).** Declined at tier 2 (default; PI may overrule before
  the launch read). InternVL3 advances only through E3, whose margin does not depend on τ, and the cap goes to the
  W2 zs arms. InternVL3 stays τ = −∞, as at tier 1.

## 4. Frozen configuration (tier-1 values, no tuning; CC-191 W1)

| item | value (source) |
|---|---|
| Aya-Vision-8B | rev `d7601ac8`; `ret` k = 4, order last, template T1, τ = −∞ (C-T1 B1 selection, `t_config.json` sha `948165b8`) |
| Qwen2.5-VL-7B | `ret` k = 8, order first, T1, τ = −∞ (C-EN's registered config, as tier 1 B4) |
| InternVL3-8B | `ret` k = 4, order last, T2, **τ = −∞ only** (C6) |
| `rand` | draw 0 = C's rule `random.Random(seed("rand", "f30k_val", id))`, same k and template as `ret` |
| `zs` | C-EN's English zero-shot prompt, all three backbones (W2, descriptive) |
| LMCap `ri` | C-T1 §4 re-implementation unchanged: M-CLIP xlm-roberta-large-ViT-H-14 image→caption retrieval, K = 4, N = 3 fixed shots drawn by the per-set rule `seed("lmcap_shots", "f30k_val")` among clusters below the near cut for every val query, XGLM-2.9B fp16 (safetensors `9e292657`, bit-identical to the pin, C-T1 AMENDMENT_2), beam 3, 3 returned, M-CLIP re-rank, 40 new tokens |
| memory | C-EN's COCO memory, 111,927 clusters (`cen_memory.json` `b77e4bde`, `cen_memory_emb.npz` `add1d92a`); shown caption = members[0]'s first sentence |
| near cut | SigLIP2 cosine ≥ 0.92 never shown (C's rule), every arm and LMCap's retrieval |
| prompts | C-EN English template sha `b329e57a`, greedy, 60 new tokens, each model's own chat template |
| scorer | C-EN's PTB CIDEr-D (pycocoevalcap 1.2), df over val's own 5 references per image; paired per-image differences, percentile bootstrap B = 2,000, seed 0 |
| lists | `c_t1_f30k_lists.json` `eebcd95b` (val = its `refuse.val` list, 1,014 names; test = `refuse.test`, 1,000 names, refused) |

## 5. Arms, order, GPU budget, machine

Rates are C-T1's measured seconds per 1,000 carve images (M1 mirror `gpu_seconds.tsv`) × 1.014:

| block | arms (run order) | est. s |
|---|---|---|
| V0 | SigLIP2 vectors of val; example lists vs the COCO memory (CPU) | 37 |
| V1 (claims) | LMCap `ri` 727; Aya `ret` 1,359 + `rand` 1,388; Qwen `ret` 374 + `rand` 369; InternVL3 `ret` 1,241 | 5,458 |
| V2 (W2, descriptive) | `zs`: Qwen 350, InternVL3 1,194, Aya 1,463 | 3,007 |
| **total** | | **≈ 8,500 s = 2.4 GPU-h** |

**Hard cap 3.0 GPU-h** (`b1.left` accounting, every step under `timeout` for the time left; a timeout is a CAP STOP,
final). The job runs V1 before V2, so the cap cuts the zs arms first, last-to-first (Aya zs, then InternVL3 zs, then
Qwen zs). One look: no rerun after a failure other than a resume of its own partial file.

**Machine: M1 (machine id m3) only.** Only M1 may open the Flickr30K zip (C-T1 PREREG §2 custody); C-T1 ran there
(CC-176). Queue: A-T3's Aya block (running on M1) → **C-T2** → MT4 K1+K6. C-T2 never runs ahead of an A or B job; if one becomes ready mid-run, C-T2 stops between steps and later
resumes from its `.done`/partial files (the same single look, never a re-decode). If this
prereg is not judged and committed when M1 frees, MT4 starts rather than leave M1 idle (keep-queue-full), and C-T2
takes the next free M1 slot. M2 stays with A-T3 tier 2 until its rental ends (2026-11-02 04:46 VN). M1 rental: kept at
most until 2027-03-04 (PI answer to CC-191 Q2, as given in the coordinator's brief; no LOG id seen by the drafter). If
M1 ends before C-T2 runs, C-T2 waits for the next M1-role rental (the zip stays on the test-role host). Never
concurrent with another GPU job (the job refuses a busy GPU).

## 6. Scoring and decision (laptop, after the pull; one call each, run once)

`$R` = the pulled `/root/outputs/c_t2/out`, `$ST` = the caption stores outside the repo, `$CSV` = the pinned
Flickr30K annotation file (sha256 `395990db…ac137`), `$LED` = a ledger dir outside the repo:

```
mkdir -p $LED $ST .session_backup/2026-10-30/c_t2
python3 scripts/c_t2/c_t2.py store --csv $CSV --what val_refs --out $ST/val_refs.json
python3 scripts/c_t2/c_t2.py score --set f30k_val --memory coco --runs $R/t2_*_f30k_val-zs.preds.json \
    $R/t2_*_f30k_val-*-mcoco*.preds.json $R/t2_lmcap-ri_f30k_val-mcoco.preds.json \
    --refs $ST/val_refs.json --captions $ST/coco_captions.json --ledger $LED/val_coco.jsonl
python3 scripts/c_t2/c_t2.py t2 --ledger $LED/val_coco.jsonl --carve-ledger .session_backup/2026-10-30/c_t1/ledgers/carve_coco.jsonl \
    --exclude $R/../dupcheck.json --out .session_backup/2026-10-30/c_t2/T2_DECISION.json
```
`store` keeps only val rows (test rows are dropped as the csv is read); the val references never go to M1. `t2`
refuses a carve ledger other than `4ced15b4` and a val ledger that is not all 1,014 images. Its output holds ids and
numbers only: per claim the val contrast, val PASS, the pooled d/SD/SE, P at `m_plan`, the status (TIER-3 FAMILY /
VAL PASS, NO MARGIN / VAL FAIL / NOT RUN), the family, `m_holm`, and the descriptive W2 rows (`zs` − `lmcap_ri` and
`ret` − `zs` per backbone). `masked3` rows are scored as at tier 1 and stay descriptive. No agent opens a preds file.

**Dedup (PI-1030f; dev = exact sha/id only).** Val ids are disjoint from the carve and the X5 memory by the Karpathy
split (`load_lists` asserts it). `dupcheck` (CPU, in the job) lists val images whose sha256 equals a COCO memory
example image (members[0]), a carve image, or an earlier val image. The decision column is **all 1,014 images** (§8
wording). If the list is not empty, the same decision computed without those images is printed beside it
(`dedup_beside`), labelled, never replacing the full-set result. An exact memory duplicate cannot be shown as an
example anyway (cosine 1 ≥ 0.92). Full near-duplicate search against test is a tier-3 item.

## 7. Staging checklist (operator, M1, before the job; one LOG line, no host string)

1. M1 is free: A-T3's Aya block done and its GPU idle; no `RUNNING` of another job.
2. The Flickr30K zip is at `$NCS_DATA/f30k_raw/flickr30k-images.zip` with sha256 `2ce2420c…7391`. If it is absent, fetch it
   from the pinned revision on M1 only, never on the laptop.
3. `c_t2.py extract --zip <zip> --out /root/c_t2_stage/c_t2_f30k_val.tar` (refuses off m3; reads the 1,014 val members
   only; writes `manifest_val.json`). Untar by list into `$NCS_DATA/datasets` (`c_t2_f30k_val/images/`), copy the
   manifest to `c_t2_f30k_val/manifest.json`, record both shas, delete the `.tar` and the stage dir.
4. `$NCS_DATA/datasets` holds only allowed dirs (`ktvic openviic c_t1_f30k_carve c_t1_f30k_memory cen_memory c_t1_mem
   c_t2_f30k_val`). A-T3's `a_t3/` is moved outside `$NCS_DATA` before the job (logged) and back after it, or A-T3
   has released it.
5. Still staged from C-T1 and checked by the job: `cen_memory/images` (memcheck), `c_t1_mem/memfiles_coco.json`,
   `c_t1_mem/coco_captions.json`, `c_t1_f30k_carve/manifest.json` (dupcheck), `/root/outputs/c_en/cen_memory*.{json,npz}`
   (sha-checked against C-T1 `RESTORED_SHA256`), model snapshots (`qwen25vl_7b`, `internvl3_8b`, `c_t1_aya_vision_8b`,
   `c_t1_xglm_2_9b` with the AMENDMENT_2 safetensors, `c_t1_mclip_h14`, `siglip2`), venv-lb, venv-t1 (`T1_FREEZE` =
   `1766dc23a71509ba4fb6b8adb34b1999a3a2bf78ebe1e227730fd6647bea3599`, C-T1 AMENDMENT_1 l.99; re-check on the current M1), venv-c1score.
6. `/root/vsps` fast-forwarded to the commit that holds this prereg (git bundle, `--ff-only`); launch
   `bash scripts/c_t2/c_t2_job.sh <HEAD>` in tmux.

## 8. Tier 3, decided now

- Only claims in the tier-2 family go to Flickr30K test, one look, under their own tier-3 prereg (irreversible, band
  92-98). Holm over the family at α = 0.05, as in §3. If the family is empty, there is no tier 3 and C reports the
  tier-2 rows as dev rows (PI-1029m form: brief, not hidden).
- **W2 at tier 3:** `zs` of all three backbones is decoded on test as well (descriptive), so E3 is always printed
  beside `zs` − `lmcap_ri` on the same set. Fallback if the cap or a later judge refuses the cost: the decomposition
  is shown on the carve and val only, labelled so.
- Tier 3 needs, in its own prereg: the pixel-level near-duplicate rule against test (PI-1030f, test = full near-dup),
  the test extract on M1, and the same frozen configurations.

## 9. Wording commitments for Paper C (W2-W5; checked when C is revised)

- **E3 (W2, CC-191 r1/r2):** E3 is written as the reviewers' requested same-data head-to-head with a published
  training-free baseline (meta-review item 3), never as evidence for the retrieval prompt. `zs` − `lmcap_ri` is
  printed beside every E3 row (carve: Aya −13.8, Qwen +18.2, InternVL3 +37.9). The LMCap row is labelled
  "re-implemented, this study, dev" with the deviations listed: one shown caption per memory cluster (not all
  captions), C's SigLIP2 near cut also removes LMCap's closest neighbours, 40 new tokens, fp16. The robustness bound
  is stated: at LMCap's published XM3600-en level (45.2) E3 would still be about +17.6 / +30.5 / +30.2.
- **Aya RICES (W3, CC-191 r3), sentence used as is:** "Aya-Vision's interleaved multi-image prompt was run once and
  not validated; its row is shown and not interpreted." No claim about image versus text demonstrations rests on Aya.
- **InternVL3 `ret` − `rand` (W4):** "descriptive, not a §8 candidate" (consistent with OpenFlamingo's Flickr-30K
  reversal), never "a dropped claim".
- **X2 (W5):** `ret` − `rand` turns negative for every backbone after masking 3-grams shared with the shown examples,
  so the CIDEr gain travels through borrowed reference-like wording (lexical/style transfer). Masking is biased
  against `ret` (it also removes correct borrowed words), so X2 does not show the gain is spurious. C claims nothing
  beyond lexical/style transfer from CIDEr gains; P2 object-precision claims stand as registered.
- **X5 (W5):** the memory swap is a style- and size-confounded descriptive row (rand drops as much as ret, captions get
  longer, the shown caption is Flickr's first reference, 28k vs 112k clusters), never "in-domain memory hurts".
- X3 (P_cm, Vietnamese) stays descriptive C support, not a hallucination-metric finding.
- Qwen RICES beats text-only `ret` on the English carve (+8.5; −0.5, n.s., on OV-dev-B); C's text-only design is
  justified by cost (about 5× GPU time) and the Vietnamese parity, not by accuracy.

## 10. Binding-rule compliance

- Three-tier method: tier 2 on val only; no test look; test refused by name in every data command and the guard,
  never extracted, never staged (selftest: `f30k_names`, `extract_want`, `items_of`, the guard and the live open()
  hook each refuse a real test name and admit a real val name).
- No new human labels; no AI label used as evidence. Full official split: all 1,014 val images; the dedup row is
  only printed beside the full result.
- Captions: no OpenViIC/KTVIC/UIT-ViIC or Flickr30K caption text in any repo file; preds and stores live under
  `/root/outputs/c_t2` and outside the repo; the ledger and decision hold ids and numbers only; no agent opens a
  preds file. No host, IP or port in repo files. No personal e-mail in any request.
- Cost: ≤ 3.0 GPU-h on M1. The drafting agent made no commit, no GPU use and no machine access; commit via the
  gatekeeper after the launch judge.

## 11. Open items (before launch)

- O1: launch judge read (≥ 92) of this file and the code diff; Q-a (C2), Q-b (C1 default vs the permissive
  reading), Q-c (τ = 0.10 declined).
- O2: gatekeeper writes `manuscript/prereg/2026-10-30_c_t2/SHA256SUMS` and `scripts/c_t2/SHA256SUMS` at commit (draft
  sums are present now and must be regenerated if any file changes).
- O3: staging items 2, 4 and 5 of §7 checked on the current M1 (zip present, `a_t3/` out of datasets, carve manifest
  and COCO memory still staged).
- O4: C §6 sentence check for W5 (paper side, when C is revised; not part of the run).
