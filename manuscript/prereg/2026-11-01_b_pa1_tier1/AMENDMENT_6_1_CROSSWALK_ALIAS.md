# Amendment to B-PA1-T1 prereg v3.1 §6.1: crosswalk aliases, strikes and the mandatory crosswalk read

Status: **DRAFT for the CC-230 round-2 read; not pinned, not committed.** Written 2026-11-02T23:10Z (`date -u`).
Label: `TIER 1 / DEV-EXPLORE (B-PA1-T1)`. Amends `PREREG_DRAFT_v3_1.md` (`e9b30ca7…`, commit 5ff00c9) §6.1 and
§6.4 step 1. v3.1 is not edited. This amendment takes effect when its sha is on the alias pin line, which must come
before the map v1 build start line. Basis: CC-230 W2, W3, W4 and Rulings 3-6. Objects365 class names appear only in
the pinned alias file (git-excluded), never in this file (CC-228 6(b)).

## 1. Added source (CC-230 W3)

In §6.1, after "Paper A's tone-normalised COCO-80 lexicon (matcher v2, cited as A)", add:

> **Crosswalk alias file.** An agent-drafted, judge-read, LOG-pinned file `b_pa1_crosswalk_alias.json`. Its `aliases`
> add Objects365 → COCO-80 links tagged `instrument`. Its `strikes` remove dictionary links. Its `none` records the
> COCO-80 classes with no Objects365 counterpart.
> - Provenance is recorded in the file (`provenance.drafter` = model id, `provenance.utc`). The file's sha256 is on
>   its pin line and is copied into map v1 and the crosswalk (`alias_sha256`).
> - `instrument` links never enter the §6.2 dictionary-only rows.
> - No open-LLM instrument is used in map v1.

## 2. Link rule, fixed before the build (CC-230 W2(b)-(e))

An Objects365 class C links to COCO-80 class k iff one '/'-separated alternative of C's name satisfies one of the
following. This is judged on **name semantics only**.

| rule | condition | effect |
|---|---|---|
| R1 identity | equals k's name or a spelling variant of it | link |
| R2 kind-of | its ordinary primary sense is k or a kind of k | link; a name whose common sense is neither k nor a kind of k is **not** linked |
| R3 broader (hypernym handling) | the name is broader than k, so k is one of several kinds it covers | **not** linked; if nothing else links to k, k is recorded under `none` with a reason (PI Q-CC230-hypernym default NO) |
| R4 game name | names only a ball game | read, in this list of physical-object classes, as that game's ball, unless the game's table is a plausible referent |

The rule is applied to **every** Objects365 class, not only to the COCO classes left empty:
- it adds missing links (completeness);
- it strikes dictionary links that fail R1/R2 (correctness).

**Never used:** mention frequency, any UIT-ViIC content, Paper A's prior scores or outputs, or the expected Δ.

## 3. Mandatory completeness (CC-230 W2(a), W4), enforced by `map_v1.py build`

- Every COCO-80 class has at least one link after the strikes and aliases, or a `none` record with a reason. The build
  **refuses** otherwise; a strike can never leave a class silently unlinked.
- A `none` record for a linked or repeated class is refused.
- Every entry needs a COCO-80 class and a non-empty reason. Every named Objects365 class must be in the pinned list.
- A strike must name an existing dictionary link (class and COCO target). An alias may not change an existing or
  struck link (add-only).
- The build prints `strikes` and `links_instrument` counts and `coco80_without_o365` (= the `none` classes).
- An alias file needs `provenance.drafter` and `provenance.utc`.
- The freeze pin line must carry the alias sha.

## 4. The drafted alias file (for the round-2 read)

`.session_backup/2026-11-02/b_pa1/b_pa1_crosswalk_alias.json`, sha256
`3a1e3d1c49a063d13d46b34ac866ec4e99ce145d3da19302bd7de58f9ba94397`. Provenance: drafter `claude-opus-5-5`,
UTC 2026-11-02T23:05:35Z.

- **Effect on the pinned class list** (crosswalk function only; no map built, read-only): the dictionary rule gives
  94 links, 0 ambiguous. After **10 strikes** and **19 aliases** there are 84 dictionary links and 19 instrument links.
- **`none`:** teddy bear (only a broader class exists, R3) and suitcase (its only dictionary link is broader and
  struck, R3).
- **The 4 classes the dictionary rule left empty** (hair drier, skis, sports ball, teddy bear):
  - hair drier, skis and sports ball are linked by aliases;
  - teddy bear is `none`.
- The file also lists, without effect on the build:
  - the reviewed dictionary links kept, with their reasons;
  - the classes considered but not linked, with their reasons;
  - the check of J1's synonym words, none of which creates a link.

## 5. Mandatory crosswalk read before the freeze (CC-230 W4, Ruling 6)

- **Who and when.** One judge reads the build output after the build and before the freeze pin.
- **What the reader may use.** The crosswalk, the map, the alias file and the pinned class list, by class names only.
  No UIT-ViIC file and no gold.
- **Scope.** Completeness and semantic correctness of **every** link (dictionary and instrument) and of every `none`
  record, against §2. The reader has no discretion over whether aliases are used (W2(f)).
- **If the reader asks for a correction:**
  - the drafter writes a revised alias file (new sha), tied to the cited §2 rule only;
  - the gatekeeper pins it;
  - the build runs again into a new directory with its own start line;
  - the earlier directory is kept and never freeze-pinned.
- **No edit after the freeze, ever.**

## 6. Pin line (gatekeeper; after the r3b line, before the build start line)

`<date -u> OPS-1102b-alias-pin: PIN b_pa1_crosswalk_alias.json 3a1e3d1c49a063d13d46b34ac866ec4e99ce145d3da19302bd7de58f9ba94397 PIN manuscript/prereg/2026-11-01_b_pa1_tier1/AMENDMENT_6_1_CROSSWALK_ALIAS.md <full sha of this file> (§6.1 amendment per CC-230 W2-W4: agent-drafted instrument aliases, strikes, none; drafter claude-opus-5-5 2026-11-02T23:05:35Z; 84 dictionary + 19 instrument links, 10 strikes, none = teddy bear, suitcase)`
