# G0: PASCAL-50S output-free gold sizes on V20 (Paper A)

Pinned note per CC-181 item 1, W4 and W5. Written before any run. **POST HOC DESCRIPTIVE, NO VERDICT.**
Wording is "consistent with" only, never "explains". This is not a second look under the P50 prereg
(2026-10-28_a_p50_kladder); the registered P50-A4 FAIL (p50_decide part 2, -2.29 [-5.15, 0.61]) is unchanged
and stays in the abstract and cover letter (CC-181 r1, W6).

## Inputs (pins checked before anything is read)

| Input | Pin |
|---|---|
| `pascal50S.json` (cider repo @ f281464) | sha256 `5384abf1340f7295d535b99453bc2313e521c111ad13ec257239a4d5b477ef42`, 4,546,057 bytes (`p50.P50_JSON`) |
| VOC2008 trainval tar (`VOCtrainval_14-Jul-2008.tar`) | sha256 `7f0ca53c1b5a838fbe946965fc106c6e86832183240af5c88e3f6c306318d42e`, 577,034,240 bytes (stage.json, EVENTS 2026-10-29T00:52:26Z) |
| `scripts/pascal50s/p50.py` | sha256 `2387ca05ae8a57304a5f696c4e2f73d29297d03ccc23debb416269dc7a676d31`, committed at 353437f, unchanged |
| Image ids | `scripts/pascal50s/p50_1000_ids.txt`, sha256 `a8539efb…4cb4` via `p50.id_list()`; **all 1,000 images** |

Sources (nothing is on the laptop; the P50 run deleted its copies, EVENTS 2026-10-29T06:23:20Z):
`JSON_URL` and `TAR_URL` exactly as in `scripts/pascal50s/p50_job.sh` l.30-31.

## Frozen code used (imported, not copied or changed)

- `p50.V20`: the frozen VOC name -> COCO-80 class map (PREREG §4.2). The "aeroplane" matcher gap stays (PREREG l.267, l.391).
- `p50.voc_gold(xml_bytes)`: every `<object>` class, difficult and truncated included, mapped by V20 (PREREG §4.1).
- `p50.load_refs(path, ids)`: the W6 key normalisation and 1:1 check.
- `p50.draw(n_refs)`: the frozen reference draw (rng `default_rng(1)`, k = 1, 2, 5, 10, 20, 20 replicates).
- `score_g2b.MATCH["coco80"]["en"]` = `score_coco_probe.en_classes` with the pinned synonym table, the matcher P50 and p50x used. Mentions are intersected with `set(V20.values())`.

**Seed.** CC-181 W4 says "draw() seed 0". `draw()` is frozen at `default_rng(1)` and is used unchanged; seed 0 in
the P50 code is the bootstrap seed (`BOOT_SEED`) and the p50x null seed, and G0 has no bootstrap and no null.
The primary quantities below use no randomness. The rung rows use `draw()` as frozen. No other seed is set.
Flagged for the CC-182 read.

## Quantities (all 1,000 images; numbers only)

Per image i: `R_i = ∪ over the 50 references of (en(ref) ∩ V20)`; `L_i = voc_gold(Annotations/i.xml)`.

1. Primary: `S_ref = Σ_i |R_i|` and `S_voc = Σ_i |L_i|`; ratio `S_voc / S_ref`.
2. `Σ_i |R_i ∩ L_i|`, `Σ_i |L_i \ R_i|`, `Σ_i |R_i \ L_i|`.
3. Per class c in V20: `|{i: c ∈ L_i \ R_i}|`, `|{i: c ∈ R_i \ L_i}|`, `|{i: c ∈ R_i ∩ L_i}|`.
4. Rungs (optional row set, descriptive): for k in 1, 2, 5, 10, 20 (frozen `draw()`) the mean over the 20 replicates of
   `Σ_i |R^k_i|` and `Σ_i |R^k_i ∩ L_i|`; k = 1 with ∩ L is the per-image quantity behind X5's `sum_k_scored_mean`.

## Comparator: the 2x convention

The convention used by the P50 companion X5 gate (p50x.py l.189): a gold counts as substantially more complete
only if its size is at least twice that of the gold it is compared with. G0 applies it to the label rung versus
the 50-reference rung on V20: **outcome A if `S_voc >= 2 * S_ref`, outcome B if `S_voc < 2 * S_ref`.**

Outcome sentences, fixed now; `{S_voc}`, `{S_ref}`, `{ratio}` are filled with the numbers, nothing else changes.

- **A** (`S_voc >= 2 * S_ref`): "On all 1,000 PASCAL-50S images, the VOC labels hold {S_voc} class instances on the 20 VOC classes against {S_ref} named in the 50 references (ratio {ratio}). This post hoc descriptive count, with no verdict, is consistent with the label rung being a substantially more complete gold under the 2x convention, so the registered P50-A4 FAIL is not consistent with a label rung that is too small."
- **B** (`S_voc < 2 * S_ref`): "On all 1,000 PASCAL-50S images, the VOC labels hold {S_voc} class instances on the 20 VOC classes against {S_ref} named in the 50 references (ratio {ratio}). This post hoc descriptive count, with no verdict, is consistent with the label rung not being a substantially more complete gold than the 50 references under the 2x convention; the registered P50-A4 FAIL stands as registered."

## Disclosure

The paper's 1,782 (p50x X5 `sum_complete_scored`) is on the 997-image analysis set. That set is defined by clean
captions in every run, the outputs are deleted, and it cannot be rebuilt (CC-181 r2, p50.py l.350-351). G0 is on all
1,000 images, so the comparison with 1,782 is approximate. A sanity anchor only: `S_voc` on 1,000 must be >= 1,782.

## Execution rules (W5)

M1 (m3-role), CPU only (`nice -n 19`, `ionice -c3`), in a scratch dir outside `/root/outputs/c_t1` and every C-T1
dataset root. Pins verified before reading. Only `Annotations/<id>.xml` members are read from the streamed tar; no
JPEG is extracted or written. The output JSON holds numbers and class names only, no image ids and no reference
text; it is also run through `p50.py ngram` (exit 1 on any 8-gram hit). After the run the JSON and tar are deleted
from M1, the output JSON is mirrored, and an OPS line is logged. Glue code: `scripts/a_g0/a_g0.py` (one-judge read, CC-182).
