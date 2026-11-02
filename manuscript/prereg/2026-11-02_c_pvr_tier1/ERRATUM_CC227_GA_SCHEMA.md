# CC-227 erratum to the CC-222 amendment (C-PVR-T1): G-A input schema FAULT on the NoCaps-test image info (v3)

Base: `AMENDMENT_CC222_DRAFT_v1_3.md` (c565e67a, commit db97b93), `scripts/c_pvr/gates.py` 130ddd61 (same commit).
Tier: irreversible (≥ 92), per amendment §4.2 (N10): a FAULT at the G-A input check goes to a ruling at this tier.
v2 answers CC-227 round 1 (NEXT_ROUND, median 90): B1/W1 (full pins and supersessions), E3 lower bound, l.115,
wording, custody, disclosure, staging, STATE. v1 (16a04777) is kept at `.session_backup/2026-11-02/snap/C_ERRATUM_CC227_v1_16a04777.md`.
v3 answers CC-227r2 (NEXT_ROUND, median 89): B-r2-1 (l.797, l.803, l.125, §0 heading) plus NB items (historical anchors,
ACCESS_LOG format, exact commands, full --info-sha, E3 strictness). Text only; gates.py, SUMS and the harness are byte-equal
to v2. v2 (73e1b53a) is kept at `.session_backup/2026-11-02/snap/C_ERRATUM_CC227_v2_73e1b53a.md`.

## 0. Pins (full; these supersede every 130ddd61 and b3352fe6 reference, §3 E6)
| Object | Path | sha256 |
|---|---|---|
| gates.py (new) | `scripts/c_pvr/gates.py` (1,188 l.) | `bf4d5f64485efbce07f254a6a7e5c79f4e8384c4448e9662ec9fe987fbca3468` |
| SHA256SUMS (new) | `scripts/c_pvr/SHA256SUMS` | `bc7e53b4d123363a045d3632271f7b9535a7d2fed643dc62ee40825833b89757` |
| mutant harness | `scripts/c_pvr/gates_mutants.py` (repo destination; copy of `.session_backup/2026-11-02/c_ga_fault/C_gates_mutants_cc227.py`) | `f9c1ff3c68b3ccd6cae080c3d172cc3fc2f37a87a216381bb338801d4be07c44` |
| harness output (not committed) | `.session_backup/2026-11-02/c_ga_fault/mutants_cc227_out.txt` | `35ac52a8402dd0ac55abc65e335967c0eb1c3c8db4bf3d3b5bd518bce7c621be` |
| diff 130ddd61 → bf4d5f64 (not committed) | `.session_backup/2026-11-02/c_ga_fault/gates_130ddd61_to_bf4d5f64.diff` | `1de5afd5a1d325a812af7b83cbe42d28958552f3362eafe1708f5e1abe9fd460` |
| g_c2_provenance.json (unchanged) | `manuscript/prereg/2026-11-02_c_pvr_tier1/g_c2_provenance.json` | `e242623fdcd984a5ddcb21732f2ff5adeb65cc23c50e64af9ae1b28cd4c7819b` |

`SHA256SUMS` now lists gates.py, g_c2_provenance.json and gates_mutants.py; `sha256sum -c scripts/c_pvr/SHA256SUMS`,
run from the repo root (the paths are repo-relative), passes 3/3. Harness command:
`python3 -I scripts/c_pvr/gates_mutants.py scripts/c_pvr/gates.py <scratch dir outside the repo>`.
New selftest line (replaces amendment l.141):
```
selftest ok  TIER 1 / DEV-EXPLORE (C-PVR-T1)  gates.py bf4d5f64485efbce07f254a6a7e5c79f4e8384c4448e9662ec9fe987fbca3468
```
Mutants on bf4d5f64: 68 run, 68 killed; the 2 registered equivalents (`eq_val_term`, `eq_no_36707_assert`) survive as before.
Round-1 pins 4ed409a4 (gates.py), be2d3ffd (SUMS), 93e0b27d (diff), 16fe81e6/d76276d8 (harness) are superseded by this
table: bf4d5f64 adds only CC-227 NB6 (hash the bytes read once in `info_schema`; a 64-character `type` pass case).

## 1. What happened (LOG OPS-1102c-ga-step0, -ga-pin, -ga-fault)
- §2.3 steps 2 and 3 passed: `gate-a step0` reported l2p1 41,164, l2p1_q11 36,707, oiv7 41,620, val 4,500, xm 3,600, with no FAULT.
- §2.3 step 4 passed. Both files are pinned at download, before any parse, mode 400 in a 700 directory:
  - `nocaps_test_image_info.json`: 3,069,304 B, first byte `{`, sha256 `f22809de674afa26bd81ece416266d4eab63b6d9d6f618ae92ea3ca1bd3da7a8`;
  - `test-images-with-rotation.csv`: 45,227,339 B, md5 d832feb775b3cb78077bf8ae350adce5 (= bucket md5), sha256 `de55c6b8cbda32a79f4a20f28572d54e9c49d527a4006725675764074a51a36d`.
- §2.3 step 5 (`gate-a join`, 08:43Z) FAULTed (rc 1) in `info_ids` at its first schema check:
  > top-level keys [images, info, licenses, type] outside [images, info, licenses]
- **No file was written** (no `xm3600_all_ids.txt`, `ga_counts.json` or `ga_remaining_ids.txt`). Only key **names** were seen; no value was read, printed or logged. The image-record key check and the id/count checks have **not** run on the real file.

## 2. Evidence about `type` (documentation only; copies in `.session_backup/2026-11-02/c_ga_fault/`, stamped in `ACCESS.txt`)
- nocaps.org/download (copy sha 2e69a9a1): the format block lists `licenses`, `info`, `images` and `annotations` ("absent in test set"); it does not mention `type`. `type` is **undocumented by NoCaps**.
- COCO caption toolkit, `tylin/coco-caption` `pycocotools/coco.py` (copy sha e6f62fea): `loadRes` runs `res.dataset['type'] = copy.deepcopy(self.dataset['type'])` (l.270); `createIndex`/`showAnns` branch on `dataset['type'] == 'instances'` / `'captions'` (l.93, 139, 232, 257). A NoCaps file read by that toolkit must carry a top-level `type`.
- The value stays unread. With `type` capped as a str of ≤ 64 characters and the join reading only `open_images_id`, allowing it cannot change the result.

## 3. Changes (E1–E9)
- **E1 (§3.1 "Schema enforced", first bullet).** "top-level keys ⊆ {images, licenses, info}" becomes: top-level keys ⊆ {images, licenses, info} ∪ {type}; `type`, if present, must be a `str` of at most 64 characters; its value is never printed, logged or compared. `annotations`, every other extra key, and a `type` that is not a short string still FAULT.
- **E2 (§2.3, new step 4b): `gate-a schema --info-sha <step-4 sha>`.** Runs after this erratum's commit and before step 5. It refuses bytes other than the step-4 sha (hashing the bytes it reads). It prints **key names, type names and lengths only**: each top-level key with its value's type name and, for str/list/dict, its length (the length of the `type` string is therefore printed and disclosed); the union of image-record key names; and the record count. It prints no value and writes no file. The coordinator copies the output into LOG (`OPS-1102c-ga-schema`).
- **E2a (§3.1 l.253 amended).** "Only `id`, `open_images_id` and `file_name` are read" becomes: "The join reads only `id`, `open_images_id` and `file_name`. Step 4b reads every top-level value and every image record only to report its type name, length and key names; it prints no value."
- **E3 (decision rule, fixed in advance by this ruling).** Step 5 (`gate-a join` on the step-4 shas) runs **only if** the step-4b output is exactly:
  - top-level keys = {images, licenses, info, type} or {images, licenses, info};
  - `images` is a list of length 10,600; `licenses` is a list; `info` is a dict; `type`, if present, is a str of length ≤ 64;
  - `image_keys` ⊇ {id, open_images_id, file_name} **and** ⊆ the 8 documented keys (id, open_images_id, height, width, coco_url, file_name, license, date_captured); an absent optional key is not a STOP;
  - `n_images` = 10,600.

  Any other output is a **STOP**: LOGged, G-A goes to the PI and a new ruling, and no further code change is made under this erratum.
  These conditions are stricter than the code in places (`licenses` list, `info` dict, `n_images`); they bind exactly as written and are never relaxed after the step-4b output is seen.
  **Still unverified until step 5** (each FAULTs before any write and follows §4.2, a ruling at ≥ 92): per-record key presence; 16-hex `open_images_id`; uniqueness of `id` and `open_images_id`; `file_name` = oid + `.jpg`; the OI CSV header and rows; T ⊂ OI test; OI test ∩ OIV7 val = ∅.
- **E4 (look accounting).** A FAULT before any write is not a G-A look. The step-5 join under bf4d5f64, on the same pinned shas f22809de/de55c6b8, is the first complete G-A. The inputs are not downloaded again; a second download needs a new erratum. `verify` (the rerun rule) applies from that first complete G-A onward.
- **E5 (code; the only code change, diff 1de5afd5).** In `gates.py`: `INFO_TOP_STR = {"type"}` with the str/≤ 64 check in `info_ids`; the new `info_schema` and the `gate-a schema` subcommand. Selftest cases: a str `type` passes; a 64-character `type` passes (boundary); `type` as dict, list, int or a 65-character string FAULTs; an extra key `foo` FAULTs; `annotations` still FAULTs; the schema output holds no value; a wrong sha FAULTs. Harness: the CC-222 harness plus 7 CC-227 mutants (`cc227_any_type_value`, `cc227_no_len_cap`, `cc227_no_str_check`, `cc227_type_in_top`, `cc227_schema_no_sha`, `cc227_schema_values`, `cc227_len_ge_64`), with `no_annotations_guard` re-targeted. Nothing else in `gates.py` changes.
- **E6 (supersessions in the amendment).**
  - l.5: "`gates.py` 130ddd61 … `SHA256SUMS` b3352fe6" now reads gates.py bf4d5f64 and SHA256SUMS bc7e53b4 (§0).
  - l.141: the selftest line is replaced by the §0 line.
  - l.795 (§12): the gates.py row becomes `bf4d5f64485efbce07f254a6a7e5c79f4e8384c4448e9662ec9fe987fbca3468  scripts/c_pvr/gates.py (1,188 l.; stdlib only; selftest ok)`, plus a row for `scripts/c_pvr/gates_mutants.py` f9c1ff3c.
  - l.115: "`gates.py` changes only through this amendment and PINS-B" is overridden **once**, by this erratum; after it the clause binds again (changes only through PINS-B or a new ruling).
  - §2.3, §5.6, l.600 and l.608: "the one GO-pinned `gates.py`" is **bf4d5f64**. No G-C2 scan has run, so no G-C2 record goes stale.
  - **(v3, CC-227r2 B-r2-1)** l.797: the SHA256SUMS row becomes
    `bc7e53b4d123363a045d3632271f7b9535a7d2fed643dc62ee40825833b89757  scripts/c_pvr/SHA256SUMS    (3 l.: gates.py, g_c2_provenance.json, gates_mutants.py; sha256sum -c OK from the repo root)`.
  - **(v3)** l.803: "v1.3 verifies at the end that the first three lines above are byte-unchanged" is superseded for the gates.py and SHA256SUMS rows (now §0); the g_c2_provenance.json row e242623f stays byte-unchanged.
  - **(v3)** l.125: "(which lists both)" becomes "(which lists the three files of erratum §0)".
  - **(v3, historical anchors)** l.798-799 (harness d6eb10cb, run a09d4ad4, 61/61) are CC-222 historical anchors, superseded as anchors by §0 f9c1ff3c / 35ac52a8. l.129 (freeze order), l.208 (aislop, 1,148 lines), l.711 (Q-ROUTE) and l.753 ("The code is unchanged (130ddd61)") are historical records of v1.3, not pins; their behaviour statements stay valid under bf4d5f64.
  - The behaviour descriptions at l.516 and l.753 stay valid under bf4d5f64.
  - **(v3, record)** Round 2 changed code although CC-227 Ruling 8 planned text only: the delta 4ed409a4 → bf4d5f64 is CC-227 NB6 only (diff 93e0b27d vs 1de5afd5), the selftest passes and the mutant run re-ran (68/68, 35ac52a8). CC-227r2 accepted this as a disclosed, verified scope change.
- **E7 (custody).** `access_log` runs only on the success path (gates.py, `gate_a_join`). The coordinator appends by hand, to `~/.vsps_sealed/c_pvr/ACCESS_LOG.tsv` and mirrored in LOG, one line for the FAULTed 08:43Z join and one for the step-4b schema run, before step 5. No code change.
  **Format (v3):** exactly 5 tab-separated fields `utc<TAB>coordinator<TAB>action<TAB>path<TAB>sha256`, one LF; the action is `gate-a join FAULT (hand)` or `gate-a schema (hand)` and never starts with `gate-c2` (`_logged_faults` parses by tab position and that prefix).
- **E8 (disclosure).** C's tier-1 report and the paper carry a labelled deviation for CC-227: the schema guard was relaxed after the key names of the test info file were seen, before any count or id was computed; outcome-invariant.
- **E9 (staging and STATE).** The gatekeeper stages exactly: this erratum, `scripts/c_pvr/gates.py`, `scripts/c_pvr/SHA256SUMS`, `scripts/c_pvr/gates_mutants.py`. Never `__pycache__`, `idcheck.py` or `idcheck_out*.txt` (CC-214r3 W8). After GO, the coordinator refreshes the C row of STATE_2026-11-01 (CC-222 in db97b93; G-A FAULTed; CC-227 status).

## 4. What does not change
- G-C2 stays held behind a complete G-A (N9, CC-222r3 Ruling 9). No `gate-c2` scan has run.
- PI-1102h/i, the 0.90 floor, the STOP routes, the TALLIP pivot checkpoint and every other CC-222 ruling stand.

## 5. Order after GO
1. Gatekeeper commit of the four E9 files, byte-equal to §0.
2. LOG line: gates.py sha, `sha256sum -c scripts/c_pvr/SHA256SUMS` (from the repo root) 3/3, the `selftest ok … bf4d5f64` line, and the exact harness command of §0.
3. ACCESS_LOG + LOG line for the 08:43Z FAULTed join (E7 format).
4. Step 4b (`gate-a schema --info-sha f22809de674afa26bd81ece416266d4eab63b6d9d6f618ae92ea3ca1bd3da7a8`); the `OPS-1102c-ga-schema` LOG line carries that full argument, states it equals the OPS-1102c-ga-pin sha, and copies the output; ACCESS_LOG line (E7 format); then the E3 decision (LOG).
5. Step 5 (`gate-a join`), LOG line with the output shas, gatekeeper commit of `xm3600_all_ids.txt`, `ga_counts.json`, `ga_remaining_ids.txt` (§4.3).
