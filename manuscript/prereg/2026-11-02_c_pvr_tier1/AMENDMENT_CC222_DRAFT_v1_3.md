# CC-222 amendment to C-PVR-T1: G-A and G-C2 entry point, inputs, custody and the G-C2 rule (v1.3)

Status: **v1.3 DRAFT, TEXT-ONLY, prepared for the PI after CC-222r3 (ESCALATE_TO_PI, median 88; option 1: a text-only
v1.3, then one diff read under the PI's authority, then the gatekeeper commit). Not registered, not committed.**
`gates.py` 130ddd61, `g_c2_provenance.json` e242623f and `SHA256SUMS` b3352fe6 are **byte-unchanged** from v1.2, so the
v1.2 selftest and mutant anchors carry over. v1 (c26796e3), v1.1 (009b6fe9) and v1.2 (`AMENDMENT_CC222_DRAFT_v1_2.md`,
ad329dc4) are kept byte-equal as records only (snapshots in `.session_backup/2026-11-02/snap/`).
Written 2026-11-02T04:47:04Z (`date -u`, at the last edit; v1.3 drafting began 2026-11-02T04:46Z); HEAD at drafting
`1f23d30`. Amends the registered prereg `PREREG_DRAFT_v1_2.md` (commit 8282874, blob 0a2f0773). Code and data:
`scripts/c_pvr/gates.py`, `manuscript/prereg/2026-11-02_c_pvr_tier1/g_c2_provenance.json`, `scripts/c_pvr/SHA256SUMS`
(shas in §12). Label on every output: `TIER 1 / DEV-EXPLORE (C-PVR-T1)`.
**Licence.** Drafting only. CC-222 (NEXT_ROUND, median 87) and CC-222r2 (NEXT_ROUND, diff read): nothing is
licensed; no agent runs G-A, G-C2 or any gate-c2 scan; no NoCaps-test or OI download; the gatekeeper commits nothing
for CC-222 (CC-221r3 W5 stands); CC-222r3 licenses nothing either. v1.2 and v1.3 used no network at all.
Nothing here ran beyond the CPU selftest on synthetic fixtures (§2.2), HEAD requests, range reads of at most 4 KB on
public SFT lists, and documentation pages (§7). v1.1 read no byte of any test-set file; the v1 200 B read is a recorded
deviation of form (§7). No NoCaps file, OI file, label CSV, SFT
list or image was downloaded. No token. The only address ever sent was the placeholder `vsps-research@example.org`, in
the User-Agent of the requests of 01:13-01:20Z; every later request and every registered curl line sends
`vsps-research` only.
Values this amendment proposes, with no earlier source, are marked [proposal]. Estimates are marked [est.].

## v1.3 changes (text only; CC-222r3)

| item (CC-222r3) | change | where |
|---|---|---|
| B1 (W1) floor wording | the 0.90 floor is stated as the code applies it (`gates.py` l.420): `mblip_capfilt_raw` closes **permanently** once **more than 10 %** of static-Flickr-host hits are unparsed; no data-based estimate of the CapFilt parse rate exists (SH1 holds no host forms); 0.90 was set after about 546 sampled CapFilt `url` keys had been seen (hosts not saved) | §5.2, §5.3 STOP routes, §9 Q-FLOOR, §10 |
| B2 (W2) STOP routes | every route to UNCHECKABLE, HIT or STOP for mBLIP is listed: (i) content FAULT with its full condition list, (ii) unplaceable image form incl. an empty or extension-only value, (iii) unpinned image-like key, (iv) 16-hex HIT, (v) OpenViVQA name hit / reverse check | §5.3, §9 Q-STOP |
| B3 (W3) key-name cap | the 256-unit key-name cap of `KEY_RX` (a unit is one raw byte, or a backslash plus the byte after it) (`gates.py` l.326) is a registered limit | §5.2 (v), §10 |
| B4 (W4) mode wording | "no write bit (written 0444)" wherever the mode check is described | §0.0, §5.6, §6 |
| Q-EMPTY | code unchanged; an empty or extension-only image value (`''`, `'.jpg'` → `~\|other`) is named under Q-STOP | §5.3, §9 |
| N1 | SH1 is 76 lines; mBLIP offsets 20 + 240 = 260 | §0.0, §10 |
| N2 | the 546 sampled `url` keys disclosed before the floor | §10 |
| N4 | `valid_scan` checks consistency, not authorship; the coordinator LOGs each `scan.json` sha256 at write time and the G-C2 one-judge read checks the records against those lines (INC-1027a precedent) | §5.6 |
| N5 | until `MAP_BARRED` is hardened at a future re-pin, the one-judge map read refuses any Flickr- or XM3600-derived nested prefix | §5.3 (b) |
| N6 | size of the committed scan-record copies estimated; a sha-pinned compressed copy above 5 MB | §6, §11.1 |
| N7 | a status changed through a post-census map is labelled post hoc | §5.3 (b), §5.6 |
| N8 | the stored mutant output a09d4ad4 has a hand-added 2-line header; the `gates.py` docstring still says v1.1 and is not changed (no re-pin) | §2.2, §10 |
| N9 | G-A runs to completion before any G-C2 scan; the first scan runs only after a LOG line records the PI's answers to Q-PANGEA, Q-FLOOR, Q-STOP and Q-EMPTY | §2.3, §5.2, §11 |
| N10 | STATE row refresh after the commit | §11.1 |
| PI answers | Q-PANGEA stands as answered in PI-1102e (register now); Q-ROUTE, Q-FLOOR, Q-STOP and Q-EMPTY answered in PI-1102h (LOG 2026-11-02T08:16:25Z) on v1.3 sha 3320a7eb, risk table completed in PI-1102i (08:20:39Z); the CC-222pi text edits (key-name cap in units, static-host positive control, these answers, the three PI risk controls) add no route and change no code | §9 |

## 0. Closure tables

### 0.0 CC-222r2 (round 2) items

| item (CC-222r2) | asked | where closed in v1.2 |
|---|---|---|
| W1 BLOCKING (NB-R2-1) | a benign Flickr host form must not close a file; option (i) or (ii); fixtures (buddyicon, combo.staticflickr.com/pw, percent-encoded, server-less); correct §5.3 STOP text and Q-STOP | option (ii) **plus** wider parsing: §5.2. The parser now also takes `%2F` and the server-less form; host forms it cannot parse are counted as `n_flickr_host_unparsed` ("unknown, disclosed") and never FAULT by themselves. The only Flickr FAULTs are the ≥ 1 positive control and a parse-rate floor of **0.90**, registered now, both only on a file with a positive control (`mblip_capfilt_raw`); the floor closes that file permanently once more than 10 % of its static-Flickr-host hits are unparsed (v1.3 wording, CC-222r3 B1) (`content_faults` l.410, `FLICKR_FLOOR` l.325). All four fixtures leave the file open. §5.3 STOP text and Q-STOP corrected. |
| W2 BLOCKING (Codex 1) | the join validates every `<key>.scan.json` | `valid_scan` l.489: label, file, sha256, size, url = `SFT[key]`; `gates_sha256` = the running `gates.py`; no write bit (written 0444). Any mismatch is a FAULT and never counts toward CLEAN (§5.6). Selftest: wrong sha256, file, gates_sha256, label, url, size and a writable record are each refused. |
| W3 BLOCKING (Codex 2) | the image-like key rule matches names with punctuation or escapes | `KEY_RX` l.326 reads every JSON key name of up to 256 units (a unit is one raw byte, or a backslash plus the byte after it; any characters, JSON escapes decoded; the cap is a registered limit since v1.3, §5.2 (v)); `IMGLIKE` l.327 tests "contains image/img/photo/file/url/jpg", any case. An undecodable key name is counted as `<undecodable key>` (unpinned, so UNCHECKABLE). Fixtures: `image-path`, `Image URL`, `img.url`, `Image_File`, an escaped `ph\u006fto id`, an undecodable name. |
| W4 (T1, M7) | kill the `~` guard mutant or prove it | the guard is **removed**: after W8, no directory census key can start with `~` (such a directory is keyed `./~…`), and a bare-name key never contains `/`, so the guard could never fire; the mutant no longer exists. Harness and list saved (§2.2). |
| W5 (T2) | `load_prov` refuses map entries for `flickr/`, `xm3600/` and bare-hex keys | `MAP_BARRED` l.504, checked in `load_prov` l.507; fixtures for `flickr`, `flickr/x`, `xm3600/images`, `./xm3600`, a 16-char bare-hex key |
| W6 (T3) | save the 4 KB shape sample with its sha; cite it in §5.3 | `.session_backup/2026-11-02/cc222_net/40256607b3a3758a78dcceb11bf8bc5eb57e59a9b9c2722b2e03d1833aae7d19.txt` (76 l.); cited as source **SH1** in §5.3 |
| W7 (T4) | mirror each FAULT attempt into ACCESS_LOG | `_log_fault` l.444 appends `gate-c2 FAULT <kind>` lines; `fault_state` l.433 FAULTs if `<key>.fault.json` holds fewer attempts than ACCESS_LOG (a silent reset); the coordinator mirrors each line in the LOG |
| W8 (T5) | the `~` key collision | `census_key` l.398: a directory whose masked path starts with `~` is keyed `./~…`, so it never equals a bare-name key; fixture |
| W9 (T6) | STATE row refresh | §11.1 (coordinator, after GO) |
| new anchors | new gates sha + SUMS -c; provenance e242623f unchanged; mutant list/harness sha; selftest with the W1-W3 fixtures | §12; §2.2 |

### 0.1 CC-222 BLOCKING (W1-W10, CC-222 l.66-75)

| item | asked | where closed in v1.1 |
|---|---|---|
| W1 (B-GA) | refuse if `ga_remaining_ids.txt` OR `ga_counts.json` exists; counts first (with `ga_remaining_sha256`), ids last as the commit marker; selftests for a stale counts file and a partial write | §4.3; `gate_a_join` l.259, `gate_a_verify` l.286; selftest: stale counts, simulated crash between the two writes, partial-state `verify` FAULT |
| W2 (B-C2a) | mBLIP under the census rule, table from S15 Table 6 (COCO, VQAv2, A-OKVQA, LLaVA(COCO), ImageNet non-OI; CapFilt web); any other prefix incl. `flickr/`, `xm3600/` UNCHECKABLE | §5.3; `MODELS` l.93 (all four census True); `g_c2_provenance.json` files `mblip_*` |
| W3 (B-C2b) | `g_c2_provenance.json` for every census model, before any scan record, docs only (URL, `date -u`, sha); OI-containing = OI or undetermined; web only with a cited crawl; post-census map onto registered components only; origins frozen | §5.3; the table is written and pinned now (§12; `PINS["prov"]` l.55); `load_prov` l.507 enforces the schema and the map rule |
| W4 (B-C2c) | full directory path, digit segments → '#', longest prefix, nested fixture | **closed and extended** (§5.2): every digit is masked character by character (length kept), and a bare file name is keyed `~` + its masked stem; `census_key` l.398; nested and xm3600-style fixtures |
| W5 (B-C2d) | count image-like key names; unpinned non-zero name → UNCHECKABLE; `n_key == 0` FAULT; report `n_key` + `n_null` against the record count; Pangea vs 6,450,624 | §5.2, §5.3 (e); `KEY_RX` + `IMGLIKE` l.326-327, `content_faults` l.410; the Pangea comparison is coded (`SFT["pangeains"]["n_records"]`) and runs only on the Pangea trace branch (§5.3 (c), Q-PANGEA) |
| W6 (B-C2e) | Flickr parser accepts `\/`; positive control (host count = parsed count; CapFilt yields > 0) — the host = parse equality is **replaced in v1.2** by the ≥ 1 control plus the 0.90 floor (§0.0 W1) | §5.5; `SEP`, `FHOST_RX`, `FLICKR_RX`, `FLICKR_FLOOR` l.321-325; `content_faults`; selftest with escaped and two-segment forms |
| W7 (HEX_RX) | case-insensitive, then lower-cased | `HEX_RX` l.319; selftest with upper-case ids |
| W8 (B-C2f) | a scan FAULT after a stated retry count → that model UNCHECKABLE on nocaps_test; the join continues | §5.2; transport FAULT retried up to 3 attempts, content FAULT final at once (`fault_state` l.433, `gate_c2_scan` l.455); the join continues with a FAULT note; a never-attempted scan refuses the join |
| W9 (Codex) | the join enforces `gate-a verify`; §11 puts verify first | `gate_c2_join` l.589 calls `gate_a_verify` first; §11 |
| W10 | W1-W9 land before any scan; re-pin `gates.py` (§12, SUMS); selftest ok logged with the new sha | §2.2, §12; order in §2.3 |

### 0.2 CC-222 NON-BLOCKING (N1-N16, CC-222 l.78-93)

| item | where |
|---|---|
| N1 four surviving mutants | §2.2: TAIL=4096 and the OI-test ∩ OIV7 FAULT are now killed by fixtures; the `val` term in `removed` and the 36,707 assert are **equivalent mutants** (proof in §2.2) |
| N2 §8 rows | §8: `other` → FAULT, OI-test ∩ OIV7 FAULT, widened §9.1 step-4 scope, census rule, provenance pin, doc-decided rule |
| N3 size | 15,269,972,625 B = 15.27 GB = 14.22 GiB for all five lists; with Pangea decided by documentation the scans stream 3,247,151,058 B (3.02 GiB); no resume (§5.1, §6, Q-NET) |
| N4 real-file step 0 before any download | `gate-a step0` (§2.3 step 3) |
| N5 step-3 check; custody recovery | `gate-a pin` (size 3,069,304 B, first byte `{`, OI md5/size/header) before the shas are logged; recovery rule §6 |
| N6 Flickr id → set of OI ids | `landing_ids` l.553; fixture with two OI ids sharing one photo |
| N7 PINS-A by the fixed candidate order; n_e_power drop printed | §5.5 |
| N8 URL-form-only disclosure; Q-FLICKR asymmetry | §5.5, §9 |
| N9 HIT final; UNCHECKABLE upgraded only on new documentation before PINS-A, labelled | §5.3 (f) |
| N10 G-A FAULT path | §4.2 |
| N11 gate-b calls `gate_a_verify` in code | §2.3 (PINS-B code obligation) |
| N12 reverse check; conditional VI sets; token variants | §5.4; `VI_RX` l.320, `VI_DEFERRED` l.100 |
| N13 Pangea table time-box; untraced → UNCHECKABLE | §5.3 (c); Q-PANGEA |
| N14 §4.1 order; CC-221a cite | §4.1 (asserts, then copy); CC-221a Ruling 8 is l.126-132 |
| N15 200 B range read | §7: deviation of form (CC-222 Ruling 6); HEAD-only forward rule |
| N16 stage-only list; STATE; 0 GPU-h | §11.1 |

### 0.3 Carried closures (CC-222 Ruling 1; unchanged from v1)

| item (source line) | where |
|---|---|
| CC-221 B1 (i)-(v) (l.94-98), B2 (l.100), B3 (l.101), B4 (l.102) | §1, §2, §3, §6 |
| CC-221 W7 (l.127), W10 (l.130) | §4.1, §4.3, §2.2 |
| CC-221a W6 (l.182-186), W7 (l.187), Ruling 8 = A6 (l.126-132) | §5.3-§5.5 (code now fail-closed, W2-W8) |
| CC-221a W4, Ruling 10 (l.139-145, l.173) | §5.6: separate `G_C2_record.json` |
| CC-220 B2 (l.52), carried | §3.2, §6; `BARRED` l.71 |
| PI-1102a Q-GA-src YES (LOG l.1140) | §3.3 |

## 1. Entry point: `scripts/c_pvr/gates.py` (CC-221 B1 (i), B4)

`gates.py` holds `gate-a`, `gate-c2` and `selftest` now. G-B is added to it only by PINS-B. `c_pvr.py` keeps every
other subcommand of §11 (lists, owners, ovqa-pin, parity, w25, score).
Reasons:
1. The registered text already makes `gates.py` the sha-pinned gate file: l.22 ("G-A, G-B, G-C2; pinned by sha before
   it runs"), l.636 (PINS-B pins the `gates.py` sha), l.655 (`gates.py` sha equals PINS-B before G-B).
2. `c_pvr.py` will gain about eight subcommands (l.747-758). With G-A inside it, every later diff would touch the G-A
   file. `gates.py` changes only through this amendment and PINS-B.
3. `gates.py` is stdlib-only with no repo import and no network code, so its sha is its whole code closure. All
   downloads are the curl lines of §3 and §5. `gate-a` reads only local files; `gate-c2 scan` reads stdin.

Overrides (stated, not silent): l.749-750 become the `gates.py` commands of §11; l.746 `test_c_pvr.py` is not needed for
G-A/G-C2 (their selftest is `gates.py selftest`; `test_c_pvr.py` stays for the `c_pvr.py` subcommands).

## 2. Code pin, selftest and the rerun rule (CC-221 B1 (ii), B1 (v), B4, W10; CC-222 W10)

### 2.1 Pins
- `scripts/c_pvr/gates.py`, `g_c2_provenance.json` and `scripts/c_pvr/SHA256SUMS` (which lists both): shas in §12.
  The panel reads these bytes; the gatekeeper commits them byte-equal.
- The provenance table's sha is also a constant inside `gates.py` (`PINS["prov"]`, l.55), so editing any origin breaks
  the pin and every gate-c2 command FAULTs (W3: origins frozen). Freeze order used: provenance JSON → `gates.py` →
  `SHA256SUMS` → this amendment. **v1.2 and v1.3 leave the provenance table byte-unchanged at e242623f (CC-222r2 Ruling 5; CC-222r3).**
- **`OI_TEST_URL` is pinned by value:** `https://open-images-dataset.s3.amazonaws.com/test/{file}` (prereg l.533),
  a constant at `gates.py` l.65, so the `gates.py` sha pins it before step 3. Evidence: HEAD on that template with the
  first ImageID of the official list (§3.2) returned 200, `image/jpeg`, 429,350 B (transcript, §7). G-A does not use the
  URL. `c_pvr.py w25` must carry the identical string, and PINS-A asserts the equality (no second value can exist).

### 2.2 CPU selftest (run on the laptop, `python3 -I`, stdlib only)
Run 2026-11-02 at the final bytes of §12 (stdout, then the one stderr note the W8 fixture prints by design); re-run
unchanged at the v1.3 stamp, because v1.3 changes no code:
```
real pins (sha only): xm_src=OK xm_attr=OK oiv7_val=OK xm456=OK noc_val=OK gc1=OK prov=OK
registered provenance: schema ok; 24 undetermined image-bearing Pangea components -> pangeains decided by documentation, not scanned
selftest ok  TIER 1 / DEV-EXPLORE (C-PVR-T1)  gates.py 130ddd61ccde5443590d8eda05031c44211a7cfecf2fe2a02813e006e1f19dce
[stderr] FAULT f: scan FAULT after 3 attempt(s): 55 B sha 9d373235, pinned 55 B 00000000; no record written -> its models UNCHECKABLE on nocaps_test; join continues
```
- `socket.socket` and `socket.create_connection` raise for the whole run; an `urlopen` probe is asserted to fail.
- Synthetic fixtures at the registered sizes: 3,600 XM3600 ids with OI splits 1,399 / 456 / 1,745, 41,620 OIV7 val ids,
  4,500 NoCaps val rows (43 XM), 10,600 NoCaps test ids, and an OI test list.
- **W10 reading (stated; unchanged).** Step-0 asserts (a)-(d) of prereg §2.2 l.220-225, the NoCaps val schema check,
  the ⊂-OIV7 and 43-overlap checks and both L2-P1 bases run on the fixtures; each guard is broken once and must fire.
  The **real** pinned files are checked **by sha only** in the selftest (1bd00f46, 288de413, 4b7a1813, 54966ca7,
  6add90eb, 1f65b2ae, e242623f). Their parse is `gate-a step0`, after the CC-222 GO and before any download (N4).
  The selftest also loads the **real registered provenance table** through `load_prov` (schema, pin, every SFT file
  covered) and checks that only `pangeains` is decided by documentation.
- From v1.1 (kept):
  - G-A write order (W1): a stale `ga_counts.json` refuses the join; a crash simulated between the two writes leaves
    counts without ids, which `verify` reports as partial and `join` refuses;
  - `gate-a pin` (N5): an interstitial body (first byte not `{`) and a wrong size are refused;
  - an OIV7 val id inside the OI test list FAULTs (N1);
  - scanner: upper-case 16-hex ids found and lower-cased (W7); escaped `\/` and two-segment Flickr URLs parsed
    (W6); a stream with a 190 KB match scanned at the registered 1 MB TAIL equals the one-shot scan (N1); `n_key == 0`,
    key/value mismatch and a zero positive control are content FAULTs (v1.1's host = parse FAULT is replaced in v1.2);
  - census keys: nested `general/cambrian/images/textvqa` beats `general/cambrian/images` (longest prefix, W4);
    `xm3600/images/<hex>.jpg` and a bare hex stem land as "no provenance prefix" (UNCHECKABLE), never as joinable;
    8- and 10-digit bare names stay apart; ImageNet synset directories collapse to `n########`;
  - provenance: bad origin, a cite to an unregistered source, `web` without a crawl, a prefix onto an unregistered
    component, a source without sha, a pin drift, a post-census map onto an unregistered component, and a re-mapped
    prefix all FAULT;
  - scans: one scan per file; three transport FAULTs close a file; a content FAULT closes it at once; a
    documentation-decided file is refused;
  - join: a tampered `ga_remaining_ids.txt` FAULTs through `verify` (W9); a HIT stays HIT despite other reasons (N9);
    an unpinned image-like key and a record-count mismatch give UNCHECKABLE (W5); a closed file gives UNCHECKABLE and
    the join continues (W8); a file with no provenance entry refuses; a VI-set name gives UNCHECKABLE; conditional VI
    sets are DEFERRED; two OI ids sharing one Flickr photo are both excluded (N6).
- New in v1.2 (CC-222r2):
  - W1: a CapFilt-like file with 20 photo URLs plus a buddyicon URL, a `combo.staticflickr.com/pw` URL, a
    percent-encoded URL and a server-less `static.flickr.com/<id>_x.jpg` URL stays open; the last two are parsed, the
    first two are counted as unparsed (disclosed). A file with 2 parsed of 10 hosts fails the 0.90 floor; a file with 0
    parsed ids fails the positive control; a file without a positive control never FAULTs on Flickr forms;
  - W2: a scan record with a wrong sha256, file, gates_sha256, label, url or size, or a writable record, is refused by
    the join; records used by the join are built with the fields the scanner writes;
  - W3: key names `image-path`, `Image URL`, `img.url`, `Image_File`, an escaped `ph\u006fto id` and an undecodable
    name are all counted as image-like;
  - W5: post-census map entries `flickr`, `flickr/x`, `xm3600/images`, `./xm3600` and a 16-char bare-hex key are
    refused;
  - W7: three transport FAULTs leave three ACCESS_LOG lines; deleting `<key>.fault.json` after one FAULT makes the next
    scan FAULT as a reset;
  - W8: `census_key("~12345678/a.jpg")` is `./~########|other`, distinct from the bare key `~########`; a `./~…` key is
    unmapped even when `~########` is registered.
- **Mutation check** (scratch copies, not in the repo), run on the final bytes of §12 with the saved harness
  `.session_backup/2026-11-02/snap/C_gates_mutants_d6eb10cb.py` (sha256 d6eb10cb1af2ae32859154fe9edb4a966b62c0f69c5030bef58fc22c428ddc7c;
  the mutant list is inside it), output `C_gates_mutants_d6eb10cb_run_a09d4ad4.txt` (its first 2 lines, a `date -u`
  stamp and the gates/harness sha line, were added by hand before the harness output; the rest is the harness output):
  **61 mutants, 61 killed, 0 survived; the 2 registered equivalent mutants were run and survive, as proven below.**
  A mutant counts as killed only if the selftest fails before its final real-pin check (scratch copies always fail that
  check). The list covers every guard of v1.1 plus: the server-required and one-segment Flickr forms, `%2F`, the
  host = parse rule restored, the floor, the positive control, the `./~` key, each of the six `valid_scan` fields and
  its mode check, `valid_scan` bypassed, narrow key names, undecoded key names, the map bar, the ACCESS_LOG mirror and
  the reset check.
- **M7 (CC-222r2 W4).** The `not p.startswith("~")` guard in `eval_census` is removed rather than kept as a third
  survivor. Proof that it was dead: `census_key` gives a bare file name a key `~…` with no `/` (no directory), and gives
  a directory whose masked path starts with `~` the key `./~…` (W8); so no census key both equals a `~` prefix plus `/`
  and something more, and `d.startswith(p + "/")` with `p` starting with `~` can never hold.
- **Equivalent mutants (N1; no fixture can kill them, stated with the proof):**
  - removing the `t & s["val"]` term from `removed`: `step0` asserts NoCaps val ⊂ OIV7 val, so `t ∩ val ⊆ t ∩ oiv7`,
    which is already in `removed`;
  - removing the 36,707 assert: `step0` asserts |OIV7 val| = 41,620, the 456 = XM ∩ OIV7 (so ⊂ OIV7), |NoCaps val| =
    4,500 ⊂ OIV7 val and |val ∩ 456| = 43, hence |l2p1| = 41,620 − 456 = 41,164 and |l2p1_q11| = 41,164 − (4,500 − 43)
    = 36,707 identically. Both mutants were run and survive, as expected.
- **aislop** (scan of a scratch copy): 0 errors, score 80. Three warnings are left: file length (1,148 lines; one file
  keeps the pinned closure to one sha) and two handler ladders in `scan_stream` and its dispatch.

### 2.3 Order before G-A, and the rerun rule
1. Route (CC-222r3 option 1, if the PI approves Q-ROUTE): the PI's authority, then one diff read of this text-only
   v1.3 (checks: text only; `gates.py`, the table and SUMS byte-equal), then the gatekeeper commits this amendment,
   `gates.py`, `g_c2_provenance.json` and `SHA256SUMS` byte-equal to the read shas (§11.1).
2. `sha256sum -c scripts/c_pvr/SHA256SUMS` OK, and `python3 -I scripts/c_pvr/gates.py selftest` prints `selftest ok`.
   The coordinator writes a LOG line with the `gates.py` sha and the selftest output (B4, CC-222 W10).
3. `gates.py gate-a step0` on the real pinned id files (N4): prints the step-0 counts; any FAULT stops here, before
   any download.
4. Downloads of §3.1 and §3.2, then `gates.py gate-a pin` (N5): size 3,069,304 B and first byte `{` for the test info;
   bucket md5, size and header for the OI list. A failed file is discarded and downloaded again. Then a LOG line with
   the printed sha256/md5: this is the sha **pinned at download**, written before any parse.
5. `gate-a join --info-sha <step-4 sha> --oi-sha <step-4 sha>`. It refuses any other bytes.
- **Rerun rule (B1 (v)).** Any later `gates.py` (PINS-B adds G-B; any fix) runs `gates.py gate-a verify` before its
  first use. `verify` recomputes the join offline from the kept inputs (§6) and must reproduce `ga_remaining_ids.txt`
  byte for byte, and its sha in `ga_counts.json`. Otherwise: FAULT, G-B does not run, and the case goes to a ruling.
- **G-C2 is not covered by this rerun rule:** its scans and join run under the one GO-pinned `gates.py`, before PINS-B;
  a later `gates.py` makes its records stale (§5.6).
- **G-C2 order (CC-222r3 Ruling 9, N9):** step 5 (G-A) runs to completion first. The first `gate-c2 scan` runs only
  after a LOG line records the PI's answers to Q-PANGEA, Q-FLOOR, Q-STOP and Q-EMPTY on this text.
- **In code:** `gate-c2 join` calls `gate_a_verify` before anything else (W9). **N11, a PINS-B code obligation:** the
  future `gate-b` calls `gate_a_verify` in code before any label stream opens, and its selftest proves it.

## 3. G-A inputs

### 3.1 NoCaps test image info (CC-221 B1 (iii), B3)
- **Official host.** `https://nocaps.org/download` (read 2026-11-02T01:13:45Z, page sha256 2e69a9a1): "Test Set ...
  Sourced from Open Images test set (v4). 10600 images" and the button "Download Test Set Image Info" ->
  `https://drive.google.com/file/d/1y8rBQZp5jsKS-eO2xmFPeJr8Rz-ShQst/view`. **Drive id `1y8rBQZp5jsKS-eO2xmFPeJr8Rz-ShQst`.**
- **The registered S3 URLs are dead.** HEAD gives 403 for `s3.amazonaws.com/nocaps/nocaps_test_image_info.json` and
  `s3.amazonaws.com/nocaps/nocaps_val_image_info.json` (two of the three URLs J3 reported, CC-221 l.63, re-confirmed).
  The test variant `nocaps.s3.amazonaws.com/nocaps_test_image_info.json` is also 403; J3's third URL (the `_val_`
  variant on that host) was not re-tested.
- **Download URL and HEAD.** `https://drive.usercontent.google.com/download?id=1y8rBQZp5jsKS-eO2xmFPeJr8Rz-ShQst&export=download`
  returns `200`, `content-disposition: attachment; filename="nocaps_test_public.json"`, `content-length: 3069304`,
  `last-modified: Thu, 08 May 2025 15:57:12 GMT`, and no hash header. (The v1 200-byte range read on this file is a
  recorded deviation of form, §7; no further body read of any test-set file is made.)
- **Pin.** Before download: the Drive id, the URL and the byte size 3,069,304 (asserted by `gates.py`, `INFO` l.60).
  At download: `gate-a pin` checks size and first byte, then the sha256 is logged before any parse (§2.3 step 4).
- **Schema enforced** (`info_ids`, `gates.py`):
  - top-level keys ⊆ {images, licenses, info}. The format block on nocaps.org says `"annotations": [  // This field is absent in test set.`, and a present `annotations` key is a FAULT;
  - every image record's keys ⊆ the 8 documented keys (id, open_images_id, height, width, coco_url, file_name, license, date_captured);
  - 10,600 unique 16-hex `open_images_id`, each with `file_name` = id + `.jpg`.
- Only `id`, `open_images_id` and `file_name` are read. The whole-file `json.loads` that reads no caption key is not a
  label read (CC-221r3 Ruling 4, l.57).
- **Download command** (laptop, after §2.3 step 3):
  ```
  umask 077; mkdir -p ~/.vsps_sealed/c_pvr/ga && chmod 700 ~/.vsps_sealed/c_pvr/ga
  curl -sS --fail -A vsps-research -o ~/.vsps_sealed/c_pvr/ga/nocaps_test_image_info.json \
    'https://drive.usercontent.google.com/download?id=1y8rBQZp5jsKS-eO2xmFPeJr8Rz-ShQst&export=download'
  ```
  There is no `-L`. A redirect or an interstitial page fails `gate-a pin` (size, first byte).

### 3.2 Official OI test image-id list (CC-221 B1 (iii), B3; CC-220 B2 carried)
- **File.** `https://storage.googleapis.com/openimages/2018_04/test/test-images-with-rotation.csv`.
  - The Open Images V7 download page (`https://storage.googleapis.com/openimages/web/download_v7.html`, read
    01:14:17Z, sha256 6d71544e) links it as the "Test" image-ID file.
  - It is the same 2018_04 folder as the validation list that produced 4b7a1813 (RULE l.23). That file's md5
    `ZDpU5DsLq4rM6IF7SlaXgA==`, 15,245,485 B, was re-confirmed today by HEAD.
- **HEAD:** `200`, `text/csv`, `content-length: 45227339`, `x-goog-hash: md5=2DL+t3Wzy3gHe/iuNQrc5Q==` (hex
  `d832feb775b3cb78077bf8ae350adce5`), `last-modified: Thu, 17 May 2018 14:33:36 GMT`.
- **Header schema** (v1 range 0-299 → 206):
  `ImageID,Subset,OriginalURL,OriginalLandingURL,License,AuthorProfileURL,Author,Title,OriginalSize,OriginalMD5,Thumbnail300KURL,Rotation`.
  - It has no `LabelName` and no `Confidence` column. It is an image-metadata file, not an annotations or labels CSV.
  - Every label CSV on that page is named `*-annotations-*` or `*-imagelabels*`. `gates.py` refuses such paths (l.71).
- **Pin before download:** bucket md5 and size, asserted by `gates.py` (`OIL`, l.61-62) before parsing (`gate-a pin`
  and `oi_rows`). Its sha256 is logged at download (§2.3 step 4).
- **Parse.** Exact 12-column header; every row has 12 fields, `Subset` = `test` and a 16-hex `ImageID`. The ids are used
  for G-A. The two Flickr URL columns are used only by the G-C2 Flickr join (§5.5).
- **Count.** The 125,436 of prereg l.649 has no repo source, so it is **counted at G-A**, printed, and not asserted. The
  chance overlap with XM3600 is recomputed as 1,399 × 10,600 / count (`xm_expected_by_chance`).
- **Download command:**
  ```
  curl -sS --fail -A vsps-research -o ~/.vsps_sealed/c_pvr/ga/test-images-with-rotation.csv \
    https://storage.googleapis.com/openimages/2018_04/test/test-images-with-rotation.csv
  python3 -I scripts/c_pvr/gates.py gate-a pin     # then chmod 400 ~/.vsps_sealed/c_pvr/ga/* and the LOG line
  ```

### 3.3 Ids-only NoCaps val source (CC-221 B1 (iv), B2; PI-1102a Q-GA-src YES)
- **Source.** `manuscript/prereg/2026-10-27_c_en/cen_nocaps_val.tsv`, sha256 `6add90eb`.
  - Committed in 780ac71 and listed in C-EN SHA256SUMS l.5.
  - C-EN PREREG l.11, l.28 and l.62 describe it as the 4,500 `images` of the official NoCaps v0.1 val file (Drive
    `1zrsLhT94nazJ5h-LleHsU4AojHBqpcA0`, sha256 2e8071fc), made by `cen_fetch.py nocaps-list`.
  - Columns: `#id  file  url  domain`, where `file` = `<open_images_id>.jpg`.
  - It is already the NoCaps-val OI-id source of W25 (`w25.py` l.91, l.104, l.386: `r[1][:-4]`).
- **Schema-only check, done at drafting** (only counts were printed):
  - the header equals `#id\tfile\turl\tdomain`;
  - all 4,500 rows match `^[0-9]+\t[0-9a-f]{16}\.jpg\thttps?://[a-zA-Z0-9./_-]+\.jpg\t[a-z0-9-]+$`;
  - no row has more than 4 fields.
  - No field can hold a caption. `gates.py` repeats this check before use (`noc_val_ids`).
- **Why no official ids-only val file exists.**
  - nocaps.org/download offers for val only "Download Validation Set Captions" (Drive `1zrsLhT9…`). HEAD: 200,
    `nocap_val_4500_captions.json`, 6,159,547 B.
  - That is byte-for-byte the size of the barred file `data/datasets/nocaps/nocaps_val_4500_captions.json` (`stat`
    only; not opened).
  - The `nocaps_val_image_info.json` S3 URL is 403.
- **The barred file stays unopened.** `gates.py` refuses any `*captions*` path.
- FYI (not chased): nocaps.org states val domains 648 / 2,938 / 914. `cen_fetch.py` l.48 holds 417 / 2,670 / 1,413 ("the
  artifact's labels"). G-A never reads the domain column.

## 4. G-A procedure and outputs

### 4.1 Step 0 (prereg §2.2; W10; N4, N14)
- `gate-a step0` runs these asserts on the real files before any download (§2.3 step 3); `gate-a join` runs them again.
- Asserts (prereg §2.2 l.221-225):
  - (a) 3,600 unique 16-hex ids;
  - (b) Subset counts test 1,399 / validation 456 / train 1,745 from `image_attributions.csv` 288de413 (ImageID and
    Subset only);
  - (c) 54966ca7 ⊂ the list;
  - (d) the 456 = list ∩ 4b7a1813.
- It also asserts: NoCaps val (§3.3) ⊂ 4b7a1813, and |NoCaps val ∩ the 456| = 43 (RULE l.19).
- **L2-P1 bases:** 41,164 = 4b7a1813 − 54966ca7 (RULE l.19); 36,707 = 41,164 − (NoCaps val − its 43 XM ids) =
  41,164 − 4,457 (RULE l.19; prereg §14 Q11 l.805). Both counts are asserted.
- **Order (N14, aligned with the code):** the asserts and the join run first; only then does `gate-a join` copy
  `data/datasets/xm3600/oiv7/xm3600_ids.txt` to `xm3600_all_ids.txt` in this folder and assert the copy's sha 1bd00f46.

### 4.2 Join (ids only, laptop CPU) and the FAULT path (N10)
- T = the 10,600 NoCaps-test OI ids.
- FAULT if any id of T is not in the OI test list [Q-OTHER]. nocaps.org says the test split is sourced from OI test v4,
  and an id outside the list could never pass the W25 fetch assert (l.537).
- FAULT if the OI test list shares an id with 4b7a1813 (split disjointness, checked by id).
- removed = T ∩ (3,600 XM3600 ∪ 41,620 OIV7 val ∪ 4,500 NoCaps val); remaining = T − removed.
- Once T ⊂ OI test, overlaps with OIV7 val, L2-P1 and NoCaps val are 0 by split. They are still computed and printed.
- **FAULT path (N10):** any FAULT in step 0, the input checks or the join stops before any file is written. The
  inputs stay in custody (§6). The case goes to a ruling at the irreversible tier (≥ 92), because any rerun fixes the
  one-look set. A partial write (counts without ids, §4.3) follows the same path.

### 4.3 Printed and written (W1)
- **Counts in `ga_counts.json`:**
  - `nocaps_test`, `in_oi_test`, `in_oiv7_val`, `other` and `oi_test_list_n`;
  - **`x_l2p1_41164` and `x_l2p1_36707` (W7, both bases)**;
  - `x_xm3600_3600` and `x_xm3600_by_split`;
  - `xm_expected_by_chance`;
  - `x_nocaps_val`, `removed` and `remaining`.
- **Provenance:** every input sha, the `gates.py` sha, `ga_remaining_sha256` and a `date -u` stamp.
- **Write order (W1).** `gate-a join` refuses if `ga_remaining_ids.txt` **or** `ga_counts.json` exists. It writes
  `xm3600_all_ids.txt`, then `ga_counts.json` (carrying `ga_remaining_sha256`), then `ga_remaining_ids.txt` **last**,
  as the commit marker: its presence means a complete G-A. Each file is written once (tmp + `os.replace`, mode 0444).
  `verify` FAULTs on counts without ids (partial); a partial state goes to a ruling (§4.2).
- `ga_remaining_ids.txt` is independent of Q11: Q11 changes only which L2-P1 base is printed, and both are printed.
- **`ga_remaining_ids.txt` format:** Open Images ImageIDs (16 hex), not NoCaps integer ids; sorted, LF line ends, one
  trailing newline. It is the key the G-B stream filter matches on (`$1` = ImageID, l.698) and the key of the W25
  assert (l.537).
- The gatekeeper commits `ga_remaining_ids.txt`, `ga_counts.json` and `xm3600_all_ids.txt` after a LOG line with
  their shas.

### 4.4 Owners in the OI id space

| owner | OI split | joined at G-A? |
|---|---|---|
| XM3600, all 3,600 (A; prereg §2.2) | test 1,399 / val 456 / train 1,745 | yes, by id |
| OIV7 val 41,620 ⊇ L2-P1 41,164 ⊇ 36,707 (RULE l.19-23) | validation | yes; 0 by split, printed |
| NoCaps val 4,500 (C-EN; spent) | validation | yes; 0 by split, printed |
| TextVQA val / TextCaps val (L1-P1/L1-P2 English nulls, PORTFOLIO l.180) | OI train (TextVQA paper, S26 l.633-634) | no id list is pinned; disjoint from OI test by split; the W25 pass of prereg §5.6 stays the image-level guard [proposal] |
| every other owner (COCO, UIT-ViIC, KTVIC, OpenViIC, ViTextVQA, OpenViVQA, ...) | not OI | not in this id space |

An owner found later only shrinks the scored set, count only (prereg §7.2 rule 3). It never adds an image.

### 4.5 Host and tenancy
Laptop CPU. G-A reads ids only (no pixel, no label). The §8.2 tenancy windows (W25, G-B) do not apply.

## 5. G-C2 design (prereg §9.1 step 4, widened; CC-221a W6, W7, Ruling 8; CC-222 W2-W9)

### 5.1 Lists fetched (ids only; streamed, never stored)
Scope: the four NoCaps-test CLEAN-candidates of the committed G-C1 record (1f65b2ae, `stop_check`, `llava_handling`).
Sizes and sha256 are the HF LFS oids at the pinned revision (tree API and `x-linked-etag` on HEAD, 2026-11-02, §7).
Image keys and record keys come from range reads (§7).

| model(s) | file (repo @ revision) | size | sha256 | image key / record key |
|---|---|---|---|---|
| mblip-bloomz-7b, mblip-mt0-xl | `Gregor/mblip-train` @123e944e `task_mix_mt.json` | 747,734,272 | 72c60ff9… | `image_id` / `context` |
| same | same, `task_mix_v2_mt.json` | 962,641,896 | 4dfe4ab0… | `image_id` / `context` |
| same | same, `blip_captions/ccs_synthetic_filtered_large_2273005_raw.json` (S14 l.47: "we provide the URLs and filenames") | 506,886,927 | 23229e1e… | `jpg` (+ allowed `url`) / `caption` |
| LLaVA-1.5-7B (EN) | `liuhaotian/LLaVA-Instruct-150K` @9d451dc7 `llava_v1_5_mix665k.json` (S24) | 1,029,887,963 | ce959ce6… | `image` / `id` |
| Pangea-7B | `neulab/PangeaInstruct` @d0819917 `PangeaIns.json` (S18 l.72: "# samples: 6450624") | 12,022,821,567 | 40481cd8… | `image` / `id`; documented 6,450,624 records |

- **Sizes (N3):** all five lists 15,269,972,625 B = 15.27 GB = 14.22 GiB. Under the registered table (§5.3 (c)),
  `PangeaIns.json` is decided by documentation and not scanned, so the scans stream **3,247,151,058 B (3.25 GB =
  3.02 GiB)**. There is no resume: a dropped stream is a transport FAULT and a full retry (§5.2).
- **mBLIP uses both mixes [Q-MIX].** This read does not establish which mix trained which checkpoint, so their union is
  joined. This is fail-closed: a hit in either mix counts against both models.
- **Not fetched:** weights, images, tars, the pretraining-stage web lists (LLaVA-Pretrain 558K, BLIP-2 129M). Those are
  web-scale "unknown, disclosed" (Q5, CC-219 R6).
- **Fetch** (laptop idle windows, never beside B's T1a; CC-222 Ruling 8):
  ```
  curl -sS --fail -L -A vsps-research '<url>' | python3 -I scripts/c_pvr/gates.py gate-c2 scan --file <key>
  ```
  `-L` follows the HF CDN redirect. Integrity rests on the pinned sha256 and size over the bytes `gates.py` reads.

### 5.2 Scan (`gate-c2 scan`, no join; W4, W5, W6, W7, W8)
One streamed pass (`scan_stream`, `gates.py` l.338) keeps only:
- (i) **image references** under the pinned key, as a census. **Census key (W4, closed and extended):** the full
  directory path with every digit masked to `#` character by character (so `coco/train2017` → `coco/train####` and
  `n01440764` → `n########`); a bare file name (no directory) is keyed `~` + its digit-masked stem (so CapFilt's
  8-digit names are `~########` and stay apart from a 10-digit `~##########`). Class: 16-hex stem (any case) / digits /
  other. **Why the extension:** sampling (§7) shows mBLIP's `image_id` values are bare names (CapFilt
  `########.jpg`, COCO `COCO_train####_############.jpg`) and ImageNet uses synset directories; W4's literal rule
  (directory only, all-digit segments masked) would merge CapFilt and COCO under one empty key and create about 1,000
  ImageNet keys. **Collision rule (CC-222r2 W8):** a directory whose masked path starts with `~` is keyed `./~…`, so it
  never equals a bare-name key. The frozen table's `census_key_rule` string (e242623f) states the v1.1 rule without
  this clause; the clause changes no registered key, because no registered prefix starts with `./` or `~` followed by a
  directory, so the code and the frozen table place every registered key identically. A value may be a string (≤ 2 KB), an integer, a list of ≤ 128 strings, or `null`
  (counted, not censused);
- (ii) every **16-hex token** anywhere in the bytes, any case, lower-cased (W7); 15- and 17-hex runs never match;
- (iii) **Flickr photo ids**, from `static.flickr.com` / `*.staticflickr.com` image URLs with zero, one or two numeric
  segments before `<id>_` or `<id>.`, and from `flickr.com/photos/<user>/<id>`, with `/`, the JSON-escaped `\/` (W6)
  or the percent-encoded `%2F` (CC-222r2 W1). Every static-host occurrence is also counted; a host occurrence that the
  parser cannot read (e.g. a buddyicon or `combo.staticflickr.com/pw/...` URL) is counted as
  `n_flickr_host_unparsed`, reported, and treated as **"unknown, disclosed"** (on `mblip_capfilt_raw` only while at
  most 10 % of its static-host hits are unparsed; above that the floor closes the file, §5.2 FAULTs);
- (iv) counts of the **VI-set names**, with variants (N12): `open[_-]?vivqa`, `vi[_-]?textcaps`, `vie[t]?cap`, any case;
- (v) **W5 counts:** records (pinned record key), image keys, parsed values, nulls, image references, and every key
  whose name contains `image`, `img`, `photo`, `file`, `url` or `jpg`, literally and in any case: every JSON key name
  is read whatever its characters (`-`, `.`, spaces, `_`, escapes), its JSON escapes are decoded, and the test is
  "contains" (CC-222r2 W3). A key name that cannot be decoded is counted as `<undecodable key>`. **Registered limit
  (CC-222r3 B3):** a key name is read only if it is at most **256 units** long as written in the file, where a unit is one raw byte, or a backslash plus the byte after it (256 characters for plain ASCII; a Vietnamese letter in UTF-8 is 2-3 units; a `\uXXXX` escape is 5 units;
  `KEY_RX`, `gates.py` l.326). A longer key name is not read at all: it is neither counted as image-like nor as
  `<undecodable key>`. No such key is expected in a JSON training list; the limit is disclosed, not hidden.

No conversation, caption, question or answer text is printed or stored. Records go to
`~/.vsps_sealed/c_pvr/gc2/<key>.scan.json` (one write). A scan does not read `ga_remaining_ids.txt`, but **the order is
binding (CC-222r3 Ruling 9, N9): G-A runs to completion before any G-C2 scan, and the first scan runs only after a LOG
line records the PI's answers to Q-PANGEA, Q-FLOOR, Q-STOP and Q-EMPTY** (and after this amendment's GO and commit;
CC-222 Ruling 7).

**FAULTs (W8, registered in advance):**
- **Transport FAULT:** the bytes read are not the pinned size and sha256, or a read error occurs. No record is written,
  and the attempt is logged in `<key>.fault.json` **and mirrored as a line in `ACCESS_LOG.tsv`** (CC-222r2 W7; the
  coordinator mirrors it in the LOG). Up to **3 attempts**; the third transport FAULT closes the file. If
  `<key>.fault.json` ever holds fewer attempts than ACCESS_LOG, every later scan of that file FAULTs as a reset and the
  case goes to a ruling.
- **Content FAULT:** the bytes equal the pin, but `n_key == 0`; or keys ≠ parsed values (a value that is a JSON
  object, a string over 2 KB, a list of more than 128 items, or anything else the value pattern does not take leaves a
  key without a parsed value); or — **only on a file with a positive control** (`mblip_capfilt_raw`) — fewer than 1
  Flickr photo id parsed from a static-host URL (an id parsed only from a `flickr.com/photos/` page URL does not
  count, `gates.py` l.386), or a parse rate (static-host ids parsed / static-host occurrences) below **0.90**, i.e. **the file
  closes once more than 10 % of its static-Flickr-host hits are unparsed** (`gates.py` l.420) [proposal, registered
  before any scan; CC-222r2 W1 option (ii); Q-FLOOR]. Unparsed host forms are disclosed and do not FAULT as long as at
  least 90 % of the hits parse. The bytes cannot change, so a content FAULT closes the file at once and permanently.
- A closed file makes every model that uses it **UNCHECKABLE on nocaps_test**. `gate-c2 join` prints a FAULT note and
  continues for the other models (no traceback). A file with neither a record nor a closed FAULT refuses the join
  (the procedure is not finished).

### 5.3 NoCaps-test status per model (`gate-c2 join`)
- (a) **HIT** if any 16-hex token of the model's lists is in `ga_remaining_ids.txt` (CC-219 R6: "published SFT data
  joinable by OI id is checkable").
- (b) **W7, adopted verbatim (CC-221a l.187): "an OI-sourced subset with no recoverable OI id = UNCHECKABLE for NoCaps
  test."** All four models are under this census rule (W2). It is mechanised by the **registered provenance table**
  `g_c2_provenance.json` (W3), written **now, before any scan record exists**, from documentation only. Each source
  carries URL, `date -u` and page sha256; each component carries its origin ∈ {OI, non-OI, web, undetermined} and at
  least one cite; every `web` component names its crawl. `gates.py` pins the table's sha and checks this schema.
  - **Post-census map:** a one-judge read may add prefixes onto components already registered
    (`g_c2_prefix_map.json`). It can never add a component, change an origin or re-map a registered prefix, and it
    can never map a `flickr/` or `xm3600/` key or a bare-hex key (CC-222r2 W5; all enforced by `load_prov` l.507 with
    `MAP_BARRED` l.504). `MAP_BARRED` is anchored at the start of the key, so a nested key such as `x/xm3600/...` or
    `flickr30k...` is not barred in code; **until `MAP_BARRED` is hardened to a segment match at a future re-pin, the
    one-judge map read refuses any Flickr- or XM3600-derived nested prefix** (CC-222r3 N5). An unmapped census key is
    UNCHECKABLE. A map acts only on scan records that exist: it can never reopen a file closed by a FAULT (§5.2).
    **Any status changed through a post-census map is labelled post hoc** in the one-judge ruling, the commit message
    and the G-C2 report (the record itself shows the map by its sha in `inputs.prefix_map`) (N7).
  - **Rules** (`eval_census`, l.564; longest registered prefix wins; a `~` key is never a directory, §5.2):
    - a component with some but not all refs having a 16-hex stem → UNCHECKABLE (mixed);
    - no 16-hex stem and origin OI → UNCHECKABLE (W7);
    - origin undetermined → UNCHECKABLE [Q-UNDET];
    - a census key with no registered prefix → UNCHECKABLE (this catches `flickr/`, `xm3600/` and any bare hex stem);
    - origin web → unknown, disclosed;
    - all refs 16-hex → joinable, and (a) decides.
- **Registered table (summary; full text and cites in `g_c2_provenance.json`, e242623f):**

  | file | census key | component | origin | cites |
  |---|---|---|---|---|
  | mblip mixes | `~########` | Web CapFilt | web (crawl CC3M + CC12M + SBU) | S15 l.1958, l.2034-2035; S14 l.47 |
  | mblip mixes | `~COCO_train####_############`, `~COCO_val####_############` | MSCOCO images (MSCOCO, VQAv2, A-OKVQA, LLaVA rows) | non-OI | S15 l.1972, 1980, 1988, 1997, 2005; l.2050-2051; l.2066-2069 |
  | mblip mixes | `n########` | ImageNet | non-OI | S15 l.2013, l.2077-2082 |
  | mblip_capfilt_raw | `~########` | Web CapFilt | web | as above |
  | llava_mix665k | `coco/train####` | COCO train2017 | non-OI | S24 l.338, l.347-348 |
  | llava_mix665k | `gqa/images` | GQA (VG images from COCO and Flickr) | non-OI | S24 l.339; D1 (GQA paper) l.208-209 |
  | llava_mix665k | `ocr_vqa/images` | OCR-VQA (book covers) | non-OI | S24 l.340; D3 (OCR-VQA paper) l.186-188 |
  | llava_mix665k | `textvqa/train_images` | TextVQA train/val | **OI** | S24 l.341; S26 l.633-634 |
  | llava_mix665k | `vg/VG_###K`, `vg/VG_###K_#` | Visual Genome (YFCC100M ∩ MS-COCO) | non-OI | S24 l.342; D2 (VG paper) l.131-134 |
  | pangeains | (no prefix registered) | 31 S18 rows: 3 LAION-Multi rows **web** (S19 l.115, l.263); Cambrian737k **OI** (T1 lists `general/cambrian/images/textvqa.tar.gz`; S26); 3 text-only rows non-OI, not image-bearing; **24 image-bearing rows undetermined** (not traced; N13 default) | | S18 l.76-106 |

  Notes: the S15 Table 6 dagger footnote is not in the extracted text, so the mBLIP COCO reading rests on the
  `COCO_<split>2014_<12 digits>` file-name convention and the per-row details (A-OKVQA l.2066-2069; Karpathy split
  l.2050-2051). The `flickr/` and `xm3600/` folders of `mblip-train` (tree 3f25b918) are evaluation files; any of their
  references inside a mix is unmapped → UNCHECKABLE (W2).
  **Where the census keys came from (CC-222r2 Ruling 6 / W6).** The mBLIP and LLaVA key strings were taken from 410
  range reads of 4 KB on the public SFT lists (20 at 02:42:48Z, 390 from 02:51:17Z; no test-set file), not only from
  the documents; the documents decide the origins. The digit-masked shape sample is saved as source **SH1**:
  `.session_backup/2026-11-02/cc222_net/40256607b3a3758a78dcceb11bf8bc5eb57e59a9b9c2722b2e03d1833aae7d19.txt` (76 l.;
  shapes and key names only, no caption text). SH1 is evidence for this amendment; it is not a source inside the
  frozen table e242623f.
- (c) **Decided by documentation (registered rule) [Q-PANGEA].** A file whose registered components include an
  image-bearing component of undetermined origin cannot become CLEAN: its models are UNCHECKABLE on nocaps_test, and
  the file is not scanned (`doc_decided`, l.545; `gate-c2 scan` refuses it). Today this applies to `pangeains` only
  (24 components), so **Pangea-7B is UNCHECKABLE on NoCaps test**. This is the N13 default ("untraced components
  default to UNCHECKABLE"). The registered table stays e242623f in this round (CC-222r2 Ruling 5); a Pangea trace
  would change it and therefore needs its own amendment and read before any scan (Q-PANGEA). On that branch only, the
  Pangea scan runs and its record count is compared with 6,450,624 (W5).
- (d) Otherwise **CLEAN**, with web-scale pretraining "unknown (disclosed)".
- (e) **W5 in the join:** for a census model, any image-like key name with a non-zero count other than the pinned key
  (and `url` in `mblip_capfilt_raw`) → UNCHECKABLE; a pinned documented record count that differs → UNCHECKABLE. Every
  scan record reports `n_records`, `n_key`, `n_null`, `n_values` and `n_img_refs`.
- (f) **N9:** a HIT is final. An UNCHECKABLE row may be upgraded only on new documentation, before PINS-A, through an
  amendment that changes the registered table (new pin, its own read at this tier) and is labelled "upgraded on new
  documentation". Origins are never changed after a census by any other route.
- **Every route to UNCHECKABLE, HIT or STOP for mBLIP (for the PI; CC-222r3 B2, as `gates.py` 130ddd61 does it).**
  With Pangea decided by documentation (PI-1102e), C's VI side rests on the two mBLIP models, which share the same
  three lists (`mblip_mix_v1`, `mblip_mix_v2`, `mblip_capfilt_raw`). Each route below hits both models at once. If no
  VI captioner or verifier is CLEAN on NoCaps test, C STOPs (prereg l.466, l.626, l.630).
  - **(i) A content FAULT on any of the three files** (§5.2): `n_key == 0`; keys ≠ parsed values (any value that is a
    JSON object, a string over 2 KB, a list of more than 128 items, or another unparsed form); and, on
    `mblip_capfilt_raw` only, fewer than 1 Flickr id parsed from a static-host URL or **more than 10 % of static-Flickr-host hits unparsed**
    (the 0.90 floor). A closed file is final and permanent: no post-census map, no later read and no rerun can reopen
    it (the join never reads the census of a closed file). Three transport FAULTs close a file the same way. **No
    remedy.**
  - **(ii) An image-reference form the census cannot place:** any form beyond the four registered mBLIP keys, a
    registered component whose references mix 16-hex and other stems, and **an empty or extension-only value**
    (`''` or `'.jpg'` is keyed `~|other`, unmapped; Q-EMPTY). This is the **only route a post-census map can remedy**
    (onto an already registered component, on documentation, one-judge read, labelled post hoc; never `flickr/`,
    `xm3600/`, bare hex or any Flickr- or XM3600-derived nested prefix).
  - **(iii) An unpinned image-like key name:** any key whose name contains image/img/photo/file/url/jpg (W3 substring
    rule, any punctuation or case, up to the 256-unit cap of §5.2 (v)) other than `image_id` (mixes) or `jpg`/`url`
    (CapFilt), with a non-zero count (join, `gates.py` l.636-638). **No remedy.**
  - **(iv) A 16-hex HIT:** any 16-hex token in any of the three lists that is a `ga_remaining` id. **Final** (N9).
  - **(v) The Vietnamese verifier route (§5.4):** an OpenViVQA name (with variants) anywhere in the three lists makes
    `openvivqa_dev` UNCHECKABLE, and the pre-PINS-A reverse check makes it HIT if OpenViVQA's image source is a
    registered mBLIP component. Either removes mBLIP from the v4.1 l.276 "every registered test set" verifier rule,
    which only mBLIP can meet. **No remedy.**
  - A Flickr-photo match (§5.5) is **not** a route: it drops the image, count only.

### 5.4 Vietnamese sets: docs-only CLEAN rule (CC-221a W6, Ruling 8 option (i), A6; N12)
- **Ruling 4b reading, stated:**
  - Web-crawl parts in an SFT stage (mBLIP's Web CapFilt: CC3M + CC12M + SBU; CC-221a l.90) are "unknown, disclosed",
    exactly like web-scale pretraining under Q5.
  - An English-alt-text crawl with Vietnamese only as machine-translated text (S14: "The original English examples
    were machine translated to the following 95 languages") is **not** a Vietnamese image component.
- **Registered rule.** A VI-role model is CLEAN on **openvivqa_dev** iff all three hold:
  - its committed G-C1 entry for that set is CLEAN-candidate;
  - the set's name (with variants, §5.2 (iv)) occurs 0 times in the model's pinned SFT lists;
  - **reverse check (N12):** before PINS-A, a one-judge documentation read records the set's own image source and
    confirms it is not one of the model's registered SFT components (§5.3 table). If it is, the row is HIT. If the
    source is a web crawl, the row stays CLEAN with "web-crawl overlap unknown, disclosed" (Ruling 4b).

  Any name occurrence → UNCHECKABLE. A G-C1 UNCHECKABLE row stays UNCHECKABLE. LLaVA's VI rows stay N/A, never CLEAN
  (CC-221a l.123).
- **Conditional sets (N12):** `vitextcaps_test` and `viecap4h_private_test` are DEFERRED in `G_C2_record.json`
  (`VI_DEFERRED`, l.100). Each gets its own amendment if its test data is released (prereg l.374-376).
- **Why not option (ii).** A native-id join is impossible: these sets' native image ids and mBLIP's COCO/CapFilt file
  names are different id spaces. A URL join would need source URLs for the Vietnamese sets' images, and none is pinned
  in this prereg or its inputs.
- **Disclosure for the paper:** "CLEAN on the Vietnamese sets rests on the published training-data documentation and a
  name check of the released training lists; web-crawled components are unknown."
- This rule is fixed before PINS-A picks a verifier (W6). It decides whether mBLIP can meet the v4.1 l.276
  "every registered test set" verifier rule.

### 5.5 Flickr join (CC-221a W6 hardening; N6, N7, N8)
- The CapFilt raw file has keys `caption`, `jpg` and `url`; the sampled URLs include `static.flickr.com` (§7).
- The OI test list carries `OriginalURL` and `OriginalLandingURL` (Flickr).
- `gate-c2 join` maps each Flickr photo id to the **set** of `ga_remaining` ids with that photo (N6), and intersects
  it with the Flickr photo ids found in each model's lists.
- **Rule `CAPFILT_RULE = "image"` [registered default; Q-FLICKR]:**
  - A matched NoCaps-test image leaves P_obj^VI, R_obj^VI and the proxy at every tier, count only (as prereg §7.2
    rule 3).
  - It is a **new count-only exclusion class (d)**, printed as its own count (`flickr_image_exclusions`), never folded
    unseen into another count. n_e_power subtracts it beside the W25-flagged count (prereg §5.6); **the drop in
    n_e_power from (d) is printed (N7).**
  - `G_C2_record.json` lists the matches per model. The record's union covers every model still CLEAN on NoCaps test
    (an upper bound). The exclusion applied is the union over the models PINS-A pins (captioner, verifier, EN arm).
  - **PINS-A picks models by the fixed candidate order (prereg l.457, the G-C1 record's order), never by Flickr
    counts (N7).**
  - The model status does not change (Q5: web = unknown).
- **Asymmetry, disclosed (N8):** an OI-id hit (a), from curated SFT data, removes the model; a Flickr-photo hit, from a
  web crawl (unknown under Q5), removes only the image. The alternative `"model"` (a Flickr hit = model HIT) could
  remove mBLIP and reach the l.626 STOP; it is the PI's choice.
- **Coverage, disclosed (N8; CC-222r2 W1):** the Flickr join catches only URL forms it can parse (`static.flickr.com`,
  `*.staticflickr.com`, with zero to two numeric segments, `/`, `\/` or `%2F`; and `flickr.com/photos/...`). Host forms
  it cannot parse (buddyicons, `combo.staticflickr.com/pw/...`, others) are counted per file as
  `n_flickr_host_unparsed` and reported in the scan record as "unknown, disclosed". A Flickr photo held under another
  host, a re-encoded copy, or a COCO/VG/GQA image that is the same Flickr photo under its own id space is not caught.
  Those stay "unknown, disclosed".

### 5.6 Output, tier and commit path
- `gate-c2 join` first runs `gate_a_verify` (W9), then loads and checks the pinned provenance table, then **validates
  every scan record it uses** (CC-222r2 W2, `valid_scan` l.489): `label` = the tier label, `file` = the key, `sha256`,
  `size` and `url` = the pinned `SFT[key]`, `gates_sha256` = the sha of the running `gates.py`, and **no write bit
  (written 0444; a stricter 0400 is accepted)**. Any mismatch is a FAULT: the join stops and nothing counts toward
  CLEAN. **`valid_scan` checks consistency, not authorship** (a successful scan writes no ACCESS_LOG line): the
  coordinator LOGs each `<key>.scan.json` sha256 at write time, and the G-C2 one-judge read checks every record used
  against those LOG lines before the commit (INC-1027a precedent; CC-222r3 N4). A record written by another
  `gates.py` is therefore refused; the scans and the join run under the one GO-pinned `gates.py`. Then it writes
  `G_C2_record.json` in this folder, once. It holds per model: the status per set, the 16-hex hit ids, the Flickr-matched
  ids, the UNCHECKABLE reasons, the web-scale components and the name-token counts; plus `flickr_image_exclusions`,
  the FAULT notes and every input sha.
- **Override of l.650 ("appended to `G_C1_record.json`")**: a separate file. The committed G-C1 blob 1f65b2ae must stay
  byte-equal (CC-221a Ruling 10, W4).
- `gates.py` verifies 1f65b2ae and reads only `entries[].model/set/status`. It FAULTs if a scoped model is not
  CLEAN-candidate on nocaps_test.
- **Stale records (registered).** Every G-C2 scan and the join run under the one GO-pinned `gates.py`, and the join runs
  before PINS-B (prereg §9.1: step 4 before step 5). Because records are write-once and the join demands
  `gates_sha256` = the running `gates.py`, any change to `gates.py` after the first scan record makes every record
  stale: the join refuses, and recovery (rescans under a new pin) needs a ruling at 92. The G-A `verify` rerun rule
  (§2.3) does not cover G-C2; G-C2 has no silent rerun path.
- **G-C2 tier:** the scan records are write-once (CC-222 TIER), so the scans run only under the CC-222 GO (irreversible,
  92). The post-census prefix map and `G_C2_record.json` each get a one-judge read before the gatekeeper commit
  [proposal]. Any HIT or UNCHECKABLE removes that model for NoCaps test (l.628-630). If no VI captioner or verifier is
  CLEAN → STOP (l.630, l.466).

## 6. Custody of every file

| file | from | stored at | mode | lifetime |
|---|---|---|---|---|
| `nocaps_test_image_info.json` | Drive `1y8rBQZp…` (§3.1) | `~/.vsps_sealed/c_pvr/ga/` (WSL ext4 home) | file 0400, dir 0700 | kept until the tier-3 freeze (rerun rule §2.3); deletion barred before then |
| `test-images-with-rotation.csv` (image metadata, no label column) | GCS 2018_04 (§3.2) | same | same | same; needed by `verify` and the §5.5 join |
| 4 SFT lists scanned (3.25 GB; `PangeaIns.json` not fetched under the registered table) | HF (§5.1) | **never on disk**: curl stdout → `gates.py` stdin | – | only the scan records survive |
| `<key>.scan.json`, `<key>.fault.json` | `gate-c2 scan` | `~/.vsps_sealed/c_pvr/gc2/` | scan written 0444; the join requires no write bit (§5.6) / fault file replaced per attempt, each attempt also a line in ACCESS_LOG | kept; **a byte copy of each is committed beside `G_C2_record.json`** (public, SFT-derived counts, tokens and Flickr ids only), so the disclosed counts (`n_flickr_host_unparsed`, `n_records`, `n_key`, `n_null`, …) are visible |
| `xm3600_all_ids.txt`, `ga_counts.json`, `ga_remaining_ids.txt`, `g_c2_provenance.json`, `g_c2_prefix_map.json`, `G_C2_record.json` | `gates.py` / desk | `manuscript/prereg/2026-11-02_c_pvr_tier1/` | 0444 | gatekeeper commit |
| `ACCESS_LOG.tsv` | coordinator (each curl) and `gates.py` (`gate-a join`, every `gate-c2` FAULT attempt) | `~/.vsps_sealed/c_pvr/` | append | kept; mirrored in the LOG |

- The custody inputs never go under `/mnt/d`, `data/`, the repo or a backup path, and never to a rented host.
- `gates.py` refuses to run when `~/.vsps_sealed` resolves under `/mnt/`.
- No `oidv7-*-annotations*` or label CSV is downloaded or read by G-A or G-C2. `gates.py` refuses such paths (l.71), and
  the label CSVs first appear at G-B under prereg §9.6, unchanged (CC-220 B2).
- **Custody recovery (N5; WSL EIO precedent of 2026-10-22):** if a kept G-A input is lost or unreadable, it is
  downloaded again with the same §3 command and must match the sha256 of the step-4 LOG line. A match restores custody
  (logged). A mismatch is a FAULT and goes to a ruling; G-B does not run meanwhile.

## 7. Network evidence and touch disclosure

| `date -u` | method | URL | status, key headers |
|---|---|---|---|
| 01:13:45Z | GET (docs page) | nocaps.org/download | 200, 7,012 B, sha256 2e69a9a1 |
| 01:13:58Z, 01:43:42Z | HEAD | drive.usercontent … id=1y8rBQZp… | 200, `nocaps_test_public.json`, 3,069,304 B, lm 2025-05-08 |
| 01:13:58Z, 01:43:44Z | HEAD | drive.usercontent … id=1zrsLhT9… | 200, `nocap_val_4500_captions.json`, 6,159,547 B |
| 01:13:58Z, 01:43:45-47Z | HEAD | 3 S3 image-info URLs (§3.1) | 403 each |
| 01:14:17Z | GET (docs page) | OI download_v7.html | 200, 76,552 B, sha256 6d71544e |
| 01:14:24Z, 01:43:48Z | HEAD + range 0-299 | OI 2018_04 test list | 200 / 206; 45,227,339 B; md5 2DL+t3Wz…; 12-column header (§3.2) |
| 01:14:24Z, 01:43:48Z | HEAD + range 0-299 | OI 2018_04 validation list | 200 / 206; md5 ZDpU5DsL… = RULE l.23 |
| 01:14:35Z | range 0-199 | Drive test info | 206; first byte `{`, `"images"` at byte 1 — **deviation of form** (below) |
| 01:16:29Z, 01:20:10Z | GET (HF API) | trees of mblip-train, PangeaInstruct, LLaVA-Instruct-150K | 200; file names, sizes, LFS oids |
| 01:20:10Z, 01:43:49-51Z | HEAD + range 0-1499 | the 4 mix files of §5.1 | 302 to HF CDN; `x-linked-size` / `x-linked-etag` = §5.1 |
| 01:26:46Z | range 0-1199 | CapFilt raw json | 206; keys `caption`, `jpg`, `url` |
| 01:23:07Z, 01:43:48Z | HEAD | `OI_TEST_URL` with id `848d938b566f5e9c` | 200, `image/jpeg`, 429,350 B (no body) |
| 02:42:48Z | 20 range reads of 4 KB | both mBLIP mixes, 10 offsets each | digit-masked `image_id` shapes only |
| 02:47:28-31Z | GET (docs pages) | GQA about page, OCR-VQA page, VG index, arXiv 1602.07332 abstract | 200; sha fe68a2d4, bf6603f0, 64164dcb, 73a25199 |
| 02:47:47Z, 02:47:54Z, 02:54:08Z | GET (papers) | VG paper (arXiv 1602.07332v1), OCR-VQA paper, GQA paper (arXiv 1902.09506) | 200; sha e5a0c3cb, b630d44a, 327aae42 (D2, D3, D1) |
| 02:51:17Z (ended about 02:56Z) | range reads of 4 KB | mBLIP mixes 120 offsets each, CapFilt raw 30, LLaVA mix 120 | digit-masked shapes and image-like key names only |
| v1.2 (no time) | none | — | v1.2 used no network; SH1 was written from the logged outputs of the two sampling runs |

**Sampling result (shapes only, used for the registered table):**
- mBLIP mixes: `########.jpg` (bare, CapFilt), `COCO_train####_############.jpg` (bare, COCO), `n########/n########_#…#.JPEG`
  (ImageNet); image-like keys: `image_id` only.
- CapFilt raw: `########.jpg`; keys `jpg`, `url`.
- LLaVA mix: `coco/train####`, `gqa/images`, `ocr_vqa/images`, `textvqa/train_images` (16-hex stems), `vg/VG_###K`,
  `vg/VG_###K_#`; key `image` only.
- Not seen in the sample: any bare 12-digit name (LLaVA-Instruct's COCO train2017 naming) inside the mBLIP mixes; if it
  occurs, it is unmapped until a post-census one-judge read maps it onto "MSCOCO images" on documentation (§5.3 (b)).

**Evidence copies** (named by sha256) are in `.session_backup/2026-11-02/cc222_net/`:
- `2e69a9a1….html` (nocaps.org); `6d71544e….html` (OI V7 page);
- `3f25b918….json` (mblip-train tree); `5eea0e60….json` (PangeaInstruct tree, T1); `073e5e68….json` (LLaVA tree);
  `69a6e373….json` (LLaVA dataset info); `c945b6c4….txt` (HEAD transcript);
- `fe68a2d4….html`, `bf6603f0….html`, `64164dcb….html`, `73a25199….html` (docs pages);
- `e5a0c3cb….pdf` (D2), `b630d44a….pdf` (D3), `327aae42….pdf` (D1);
- `40256607….txt` (SH1, the 4 KB shape sample, CC-222r2 W6).

**Touches (disclosed).**
- The first data row of the OI test list (ImageID `848d938b566f5e9c`, its Flickr URL and a licence-URL prefix) and of
  the OI val list.
- **The v1 200-byte range read of the NoCaps test info (01:14:35Z) is recorded as a deviation of form** against
  CC-220r3 l.19 and CC-221r3 W5 (CC-222 Ruling 6). It is not a test look: image info only, no gold, unused, saved to
  the scratchpad and deleted, only `{` printed. **Forward rule, binding now:** HEAD requests only on any test-set file
  until that file is licensed. v1.1 and v1.2 made no read of any test-set file.
- The nocaps.org format block, which shows one example caption on the public page (not C data).
- SFT range reads: key names, shapes with digits masked, 4 mBLIP `image_id` values and 4 image paths in v1, and URL
  hosts. No conversation or caption text was kept.
- `cen_nocaps_val.tsv`: header line printed, plus a full-line regex pass that printed counts only (§3.3).
- `nocaps_val_4500_captions.json`: `stat` size only.

## 8. Overrides of the registered prereg (stated)

| prereg line | registered | amended to |
|---|---|---|
| l.22 | `gates.py` (G-A, G-B, G-C2) | unchanged in content; G-A and G-C2 now, G-B by PINS-B; rerun rule §2.3 |
| l.628-630 (§9.1 step 4) | G-C2 = OI-id join of the public SFT image lists | **widened**: OI-id join + W7 census rule under a registered provenance table + documentation-decided rule + VI-name check + Flickr join + scan-record validation; FAULTs as in §5.2 (positive control and 0.90 parse-rate floor on `mblip_capfilt_raw` only) (§5) |
| l.633-634 (PINS-A) | `OI_TEST_URL` and the `c_pvr.py` sha pinned at step 5 | `OI_TEST_URL` pinned by value now in `gates.py` (§2.1); PINS-A asserts that `c_pvr.py` carries the same string |
| l.649 | `nocaps_val_image_info.json` | `cen_nocaps_val.tsv` 6add90eb (§3.3) |
| l.649 | "official OI test image-id list" (unnamed); 125,436 | `2018_04/test/test-images-with-rotation.csv` (§3.2); count printed, not assumed |
| l.649 | public `nocaps_test_image_info.json` (S3) | Drive `1y8rBQZp…` (§3.1) |
| l.649 | "NoCaps test in OI test / OI val / other" (counts) | `other` > 0 is a **FAULT** [Q-OTHER]; an OI-test-list id inside OIV7 val is a **FAULT** (§4.2) |
| l.650 | G-C2 appended to `G_C1_record.json` | separate `G_C2_record.json` (§5.6) |
| l.497-498 (§7.2 rule 3) | NoCaps-test images leave the local metrics if they overlap an earlier owner (G-A id join or W25) or are lost | also if their Flickr photo id is matched in a pinned SFT list of a PINS-A model (§5.5) [Q-FLICKR] |
| l.504-505 (§7.3) | counts (a) G-A, (b) W25-flagged + lost, (c) self-retrieval, each printed | adds (d) Flickr-matched, printed separately |
| l.421-426 (§5.6) | n_e_power = n_e(G-B) − W25-flagged (+ lost) | also − Flickr-matched (d), printed beside the others, with the drop it causes |
| l.374-376 (conditional VI sets) | ViTextCaps test / VieCap4H private test if released | G-C2 marks them DEFERRED; each gets its own amendment on release (§5.4) |
| l.746, l.749-750 | `test_c_pvr.py`; `c_pvr.py gate-a … --val-info …`; `c_pvr.py gate-c2` | `gates.py selftest`, `gates.py gate-a step0/pin/join/verify`, `gates.py gate-c2 scan/join` (§11) |

## 9. Questions for the PI (each with a recommendation and a default)

| # | question | recommended | default |
|---|---|---|---|
| Q-ROUTE | Approve this text-only v1.3 (gates.py, the provenance table and SUMS byte-unchanged), then one diff read under your authority, then the gatekeeper commit? | YES (0 GPU-h, about 1-2 agent-hours, no risk to A or B) | YES; **answered YES in PI-1102h** (LOG 2026-11-02T08:16:25Z) |
| Q-PANGEA | Register Pangea's 24 untraced image-bearing components as undetermined (Pangea UNCHECKABLE on NoCaps test, its 12 GB list not fetched; the table stays e242623f), or buy a time-boxed documentation trace (changes the table: new pin and its own read before any scan)? | register now | **answered: register now (PI-1102e); stands** (CC-222r3 Ruling 6) |
| Q-FLICKR | A Flickr-photo match with a NoCaps-test image: drop that image (count only), or count it as a model HIT? Asymmetry with an OI-id hit disclosed (§5.5) | image-level | image-level, frozen at the first join |
| Q-MIX | mBLIP: join both instruction mixes (union)? | YES (fail-closed) | union |
| Q-UNDET | Undetermined origin = UNCHECKABLE? | YES | YES |
| Q-OTHER | A NoCaps-test id outside the OI test list FAULTs (G-A writes nothing)? | YES | FAULT |
| Q-STOP | Accept that C's VI side rests on mBLIP alone, with these routes to UNCHECKABLE, HIT or STOP (§5.3), each hitting both mBLIP models: (i) a content FAULT on any mBLIP list — no image key at all; a key whose value is not parsed (a JSON object, a string over 2 KB, a list of more than 128 items); on CapFilt, no Flickr id parsed from a static-host URL or more than 10 % of static-Flickr-host hits unparsed — final and permanent, no remedy; (ii) an image form the census cannot place, including an empty or extension-only value ('' or '.jpg') — the only route a post-census map (documentation, one-judge read, labelled post hoc) can remedy; (iii) an unpinned image-like key name (contains image/img/photo/file/url/jpg) — no remedy; (iv) a 16-hex OI-id HIT — final; (v) an OpenViVQA name in the lists, or OpenViVQA's image source being an mBLIP component — removes mBLIP as the all-sets verifier, no remedy? | accept; the 80 % pivot rule then applies to C | accept; **answered: accept, with the five routes and the PI-1102c pivot checkpoint (PI-1102h, given on v1.3 sha 3320a7eb)** (CC-222r3 Ruling 6) |
| Q11 ledger | Keep the Q11 ledger ruling (≥ 92; gates G-B and C GPU only) separate from CC-222? | separate | separate |
| Q-NET | Stream 3.25 GB (15.27 GB if Q-PANGEA = trace) through the laptop in logged idle windows, never beside B's T1a? | YES | laptop, idle windows |
| Q-FLOOR | Keep the CapFilt Flickr parse-rate floor at 0.90, registered before any scan? As coded (`gates.py` l.420), it closes `mblip_capfilt_raw` — and with it both mBLIP models and C's VI side — **permanently once more than 10 % of the static-Flickr-host hits in the file are unparsed**. No data-based estimate of the CapFilt parse rate exists (the saved shape sample SH1 holds no host forms), and 0.90 was set after the drafter had seen about 546 sampled CapFilt `url` keys (key names counted only; values and hosts neither printed nor saved). The alternative, e.g. 0.50, set before any scan, costs a `gates.py` re-pin, a selftest and mutant re-run and its own read at 92 | keep 0.90: every known CC3M / CC12M / SBU Flickr form in the fixtures parses | 0.90; **answered: keep 0.90, never changed after any scan (PI-1102h, given on v1.3 sha 3320a7eb)** (CC-222r3 Ruling 6) |
| Q-EMPTY | Count an empty or extension-only image value ('' or '.jpg') as null (disclosed) instead of an unplaceable form? | no: leave the code (keeps v1.3 text-only) and name the value under Q-STOP route (ii) | leave and disclose; **answered: leave the code; the value is named under Q-STOP route (ii) (PI-1102h, given on v1.3 sha 3320a7eb)** (CC-222r3 Ruling 6) |
| Q-200B | Accept the v1 200 B range read as a deviation of form, record kept, HEAD-only from now on? | YES | YES |

**PI risk controls (PI-1102h, PI-1102i; binding on C's tier-1 report and the paper).** (1) If too few CapFilt
Flickr links can be read (the 0.90 floor, §5.2), the file closes fail-closed, and no record, report or paper calls any
model using it clean on NoCaps test; within the floor, every CLEAN status carries its `n_flickr_host_unparsed`
count in `G_C2_record.json` and the tier-1 report. (2) If mBLIP is CLEAN but weak in Vietnamese, the TALLIP pivot checkpoint of PI-1102c
applies right after G-C2; it is judged on dev data and documentation only, never on a test-set look, and it changes no
registered gate, threshold or status. (3) The other six models (Vintern-1B-v3_5, Vintern-1B-v2, Qwen2.5-VL-7B,
InternVL3-8B, Aya-Vision-8B, Pangea-7B) cannot be verified: C's conclusions are limited in scope to the models that
can, and the paper states the limit as a model-selection criterion (the VI captioner and verifier are selected only
among models whose published training-data lists can be checked, the registered first-passing-model rule of prereg
§6.2; the conclusions do not generalise to the other models), with no data-overlap wording (PI-1101o). None of
the three controls changes `gates.py`, the provenance table or a registered rule.

## 10. Not closed, or closed with a known limit
- **Test-info hash.** The sha256 of the NoCaps test info cannot be known before download, because Drive publishes no
  hash. It is pinned at download by the step-4 LOG line, after `gate-a pin` and before any parse; `join` and `verify`
  refuse any other bytes. Recovery: §6.
- **Real-file step 0 (W10 reading).** Not run now (deny by default); its first run is `gate-a step0` (§2.3 step 3).
- **mBLIP mix mapping.** The mix-to-checkpoint mapping is not established (Q-MIX; union joined).
- **Renamed OI files in mBLIP.** An undocumented OI-sourced mBLIP component whose file names match a registered form
  (e.g. 8 digits) would be read as that component. This reliance on documentation is CC-221a Ruling 4b, registered.
- **Unsampled forms.** Sampling covered 260 offsets of the mBLIP mixes (20 + 240; SH1); a rare form can still appear.
  It fails closed (UNCHECKABLE; only a post-census map onto a registered component can place it, Q-STOP route (ii)).
- **Flickr floor.** 0.90 is a registered proposal (Q-FLOOR), not derived from data: no data-based estimate of the
  CapFilt parse rate exists, because SH1 holds no host forms. **Disclosure (CC-222r3 N2):** the value was set after the
  drafter had seen about 546 sampled CapFilt `url` keys in the second sampling run (§7). That run counted key names
  only; the URL values and their hosts were neither printed nor saved. The only CapFilt hosts ever printed are the four
  of the v1 1.2 KB read (§7), one of them `static.flickr.com`. The floor closes the file once more than 10 % of static-host hits are unparsed
  (§5.2); unparsed forms within that margin are disclosed per file, never silently dropped.
- **Key-name cap (registered limit, CC-222r3 B3).** `KEY_RX` reads key names of at most 256 units (a unit is one raw byte, or a backslash plus the byte after it; §5.2 (v)); a
  longer key name is not counted. The code is unchanged (130ddd61); the limit is disclosed.
- **Docstring.** The `gates.py` docstring still names "AMENDMENT_CC222 v1.1"; it is not changed, because any byte
  change would need a re-pin. It is corrected at the next re-pin (CC-222r3 N8).
- **Accidental 16-hex hits.** A 16-hex token in free text could hit a `ga_remaining` id by accident [est.: tokens ×
  10,600 / 2^64, negligible]; each hit id is recorded for a read, and a HIT is final (N9).
- **Drive behaviour.** The Drive endpoint's no-redirect behaviour was observed by HEAD only; a change fails `gate-a
  pin` (FAULT), not silently.
- **Equivalent mutants.** Two N1 mutants cannot be killed by any fixture; proofs in §2.2. The v1.1 M7 survivor is
  removed with its dead guard (§2.2).

## 11. Run commands (after the CC-222 GO and the gatekeeper commit)
```
sha256sum -c scripts/c_pvr/SHA256SUMS && python3 -I scripts/c_pvr/gates.py selftest       # LOG: sha + output
python3 -I scripts/c_pvr/gates.py gate-a step0                                            # real id files, no download
# §3.1 and §3.2 curl lines -> ~/.vsps_sealed/c_pvr/ga/
python3 -I scripts/c_pvr/gates.py gate-a pin                                              # LOG: sha256 + md5 (pinned at download)
python3 -I scripts/c_pvr/gates.py gate-a join --info-sha <sha> --oi-sha <sha>             # irreversible: counts, then ids
python3 -I scripts/c_pvr/gates.py gate-a verify                                           # every later gates.py, before use
# G-A complete; LOG line with the PI's answers to Q-PANGEA, Q-FLOOR, Q-STOP, Q-EMPTY (N9) -- only then the scans
curl -sS --fail -L -A vsps-research '<§5.1 url>' | python3 -I scripts/c_pvr/gates.py gate-c2 scan --file <key>   # 4 files; LOG each scan.json sha256 (N4)
# census -> optional g_c2_prefix_map.json (registered components only) -> one-judge read
python3 -I scripts/c_pvr/gates.py gate-c2 join [--prefix-map manuscript/prereg/2026-11-02_c_pvr_tier1/g_c2_prefix_map.json]
#   (join calls gate-a verify itself, W9)
```

### 11.1 Gatekeeper and coordinator (N16)
- At the commit the gatekeeper stages **only** `AMENDMENT_CC222_DRAFT_v1_3.md`, `scripts/c_pvr/gates.py`,
  `manuscript/prereg/2026-11-02_c_pvr_tier1/g_c2_provenance.json` and `scripts/c_pvr/SHA256SUMS`, byte-equal to the
  judge-read shas. `idcheck.py`, `idcheck_out.txt` and `idcheck_out_rerun.txt` stay out (CC-214r3 W8). v1, v1.1 and
  v1.2 are records and are not committed. The commit line governs the DRAFT status line (CC-209c).
- After `gate-c2 join` and its one-judge read, the gatekeeper commits `G_C2_record.json` with byte copies of every
  `<key>.scan.json` and `<key>.fault.json` used (§6), under `manuscript/prereg/2026-11-02_c_pvr_tier1/g_c2_scans/`,
  each byte-equal to the sealed file (sha checked). **Size (N6) [est.]:** the CapFilt record holds the Flickr photo
  ids found (up to about one per SBU/CC URL, i.e. up to roughly 1-2.3 M ids of about 12 bytes each in indented JSON,
  some tens of MB); the other records are small. If the copies total more than 5 MB, the gatekeeper commits instead
  one compressed archive (`g_c2_scans.tar.gz`, made with `tar --sort=name --mtime=@0 --owner=0 --group=0` and
  `gzip -n`) whose sha256 is in the commit message and the LOG, with the per-file sha256 list beside it.
- The coordinator refreshes the stale `STATE_2026-11-01` C row (M8; G-C1 commit 1f23d30) after the commit; the files
  win. The LOG line notes 0 GPU-h. Stamp erratum OPS-1102stamp-erratum2 is carried (CC-222r3 N10).

## 12. Shas (at the read)
```
130ddd61ccde5443590d8eda05031c44211a7cfecf2fe2a02813e006e1f19dce  scripts/c_pvr/gates.py      (1,148 l.; stdlib only; selftest ok)
e242623fdcd984a5ddcb21732f2ff5adeb65cc23c50e64af9ae1b28cd4c7819b  manuscript/prereg/2026-11-02_c_pvr_tier1/g_c2_provenance.json  (502 l.; registered 2026-11-02T02:58:42Z; unchanged since v1.1)
b3352fe67229d9a172a5a097689bfa45ad239ad4dec437e35fe735a586d3d8d7  scripts/c_pvr/SHA256SUMS    (2 l.: the two files above; `sha256sum -c` OK)
d6eb10cb1af2ae32859154fe9edb4a966b62c0f69c5030bef58fc22c428ddc7c  .session_backup/2026-11-02/snap/C_gates_mutants_d6eb10cb.py   (mutant list + harness)
a09d4ad4d277ec6c800683facce3ed638ce117dbf5bd3618759eb87dc2de73e4  .session_backup/2026-11-02/snap/C_gates_mutants_d6eb10cb_run_a09d4ad4.txt   (61/61 killed; 2 equivalent survive)
40256607b3a3758a78dcceb11bf8bc5eb57e59a9b9c2722b2e03d1833aae7d19  .session_backup/2026-11-02/cc222_net/40256607….txt   (SH1 shape sample)
```
Records: v1 amendment c26796e3 and `gates.py` 5e425fa7; v1.1 amendment 009b6fe9 and `gates.py` 3cf296b6 (snapshots in
`.session_backup/2026-11-02/snap/`); **v1.3 verifies at the end that the first three lines above are byte-unchanged.** v1.2 amendment ad329dc4 (this text's base; code unchanged). This file's own sha256 is given in the diff-read brief
(a file cannot carry its own hash).
