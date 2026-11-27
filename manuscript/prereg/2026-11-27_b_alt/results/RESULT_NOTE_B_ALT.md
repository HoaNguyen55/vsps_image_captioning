# Result note: Paper B, study FE-LOCUS (third registered study; DEVELOPMENT)

- **Written by:** an agent that is none of the study's coder, its operator or the paper's text writer (CC-516 W1).
- **Written from:** RESULT_ALT.json `18654e20`, G0_ALT.json `e18992c9`, S1B.json `46099ea3`, the five `.time` records, and checked against the judge's recomputation recompute_out.json `8d6e8846`.
- **Numbers:** every number has an `alt_*` row in NUMBER_MANIFEST_ALT.tsv (`file::key` or a stated derivation, the recompute value where one exists, check OK on all 77 rows).
- **Labels:** DEVELOPMENT; REGISTERED PREDICTION for H-L1 and H-L2; every interval nominal (units share files and images).

## Design in three sentences
1. The 558 KTVIC test images are split by seed 20261127 into halves A and B of 279. A census of word-boundary disagreement types between `rdr.tw.pk.cf` and `pyvi.tw.pk.cf` on half A's references gives Π_head (shortest prefix covering ≥ 0.80 of occurrences) and Π_all.
2. On half B, over 1,101 development comparisons × 18 matched `rdr`/`pyvi` level pairs (19,818 units), the shift δ of each comparison difference is compared with the shift left after pinning the boundaries of the listed types (ρ_head, ρ_all, κ_head = ρ_head/ρ_all). The intervals come from W_B (seed 20261128, B 10,000).
3. Floors (i)–(v) are checked in order before any label. H-L1 tests κ_head against the per-draw band [c_ref^B, c_out^B]; H-L2 tests ρ_head against 0.50.

## Floors in registered order, and the labels
| floor | value | rule | outcome |
|---|---|---|---|
| (i) G0 | 1,101 comparisons, key/member/sig mismatch 0, max \|diff\| 2.8e-14 | ≤ 1e-6 | PASS |
| (ii) unaligned, half-A refs | 2 of 1,395 (0.14%), recomputed from stored image counts; census `floor` null | ≤ 0.5% | PASS |
| (iii) types | 45 (≥ 30); \|Π_head\| 15; coverage 148/185 = 0.80 (recomputed) | ≥ 30 | PASS |
| **(iv) shift size, half B** | Σ\|δ\| = 7,806.7 against 0.01 · Σ\|D_r\| = 13,413.0 (Σ\|D_r\| = 1,341,296.2); ratio 0.0058 | ≥ 0.01 | **FIRED** |
| (v) | not reached (checked after (iv)) | | — |

**H-L1 (primary): NOT_EVALUABLE (iv). H-L2 (secondary): NOT_EVALUABLE (iv).** Final (CC-516 ruling 2): no re-run, subset, alternative floor or half swap.

DESCRIPTIVE rows (registered, no label, not interpretable under the floor): κ_head 0.480 [−0.743, 0.891]; ρ_head 0.313 [−0.946, 2.109]; ρ_all 0.651 [−1.906, 3.885]; c_ref^B 0.786 [0.687, 0.875]; c_out^B 0.772 [0.693, 0.836]; ρ_all `tw` 0.626 [−1.842, 3.919], `tm`/`tf` 0.665 [−1.917, 3.912]; half-B outputs 1,380 Π_all / 8,704 other / 417 unaligned; half-B references 140 / 24 (recomputed) / 0 unaligned; pin moves the reference member 3.6e-5 (head), 8.5e-5 (all); FRAGILE over G_w 47 (CHANGED 28) raw, 43 (24) Π_head-pinned; σ-zero units 0; zero-denominator draws 0.
Not a label, not for the paper: `d_lo_95` [−1.502, 0.118], `d_hi_95` [−1.532, 0.056] (RESULT_ALT.json::H-L1); the judge's POST HOC would-be labels and `floor_v_posthoc` in recompute_out.json.

## What the paper may and may not say
- **May (prereg §7 NOT_EVALUABLE row; CC-516 ruling 3):** the question, the registration commits, the split design, floor (iv) with its count (7,806.7 against 1,341,296.2; ratio 0.0058 against 0.01; 19,818 units on 279 images), and both labels NOT_EVALUABLE, worded no more strongly than "the registered floor on the size of the shift was not met". DESCRIPTIVE rows only in Online Resource 1, Table E9, each marked "not interpreted".
- **May not:** any other H-L1/H-L2 label or the words of the other outcomes; κ_head against the 0.77–0.79 band as a trend; ρ as "the list removes x% of the shift"; FRAGILE 47 → 43 or CHANGED 28 → 24 as a benefit of pinning; that the segmenter does not matter or that the two segmenters are interchangeable; the 8,704 vs 1,380 row as a finding; any use to qualify D1's H3; any C8 release sentence (dropped, prereg §8); any claim for other segmenters, metrics or data.
- English control: NOT RUN (prereg §4b). No type string printed (OQ4 not answered yes).

## Deviations and disclosures (all without effect on the data; all carried into E.9)
1. Host (b), a computer owned by one of the authors, under ERRATUM_B_ALT_1 (written before use); H1–H7 by record.
2. CPU (user + sys from the `.time` records): s0 199.1, s1a 1.9, s1b 1,206.9, g0 31.9, s2 38.9 = 1,478.7 s (0.41 CPU-h) of 28,800 s; no STOP.
3. Set-up tar `prep_pc.tar` 6ac7dd51 (code and environment, no data) untarred before its sha comparison (disclosed by the operator; sha matched).
4. Two self-matching pgrep patterns, re-run (reported by the lead; **not yet in SESSION_RECORD.md**, CC-516 W5 open).
5. `prlimit --cpu` in place of `ulimit -t` (same RLIMIT_CPU; judge's finding).
6. H7 wipe before the s2 LOG pin (host shas equalled the laptop copies at H6; judge's finding).
7. H7 listing shows `~` for the expanded home path (redaction).
8. Coded reading 5 (pin on a malformed token leaves the string unchanged; 0 such strings for Π_head and Π_all) and coded reading 6 (c_ref/c_out counts tallied in s1b, recomputed per draw in s2), both disclosed in RUN_NOTE and ruled in CC-512. Unregistered zero-denominator rule: did not fire.
9. Independent recompute (recompute.py 927d4492): every point and bound equal to max |diff| 2.7e-15; counts, FRAGILE rows and the label equal. The FRAGILE rows reuse b_fecert.certify (registered rule).

## Files and shas (inputs)
RESULT_ALT.json `18654e20` · G0_ALT.json `e18992c9` · S1B.json `46099ea3` · PER_IMAGE_ALT.npz `32da6dd0` (never committed) · CENSUS_ALT.json `2b84084a` (deleted with the host folder; never committed) · recompute_out.json `8d6e8846` · PREREG v2 `ed05acdb` (registered at 74e5034 as `eddade6d`; redaction 2d3c39f) · ERRATUM 1 `8367face` (7f7cf4f) · ADDENDUM 2 `16816c93` (c55a83d) · code scripts/b_alt at 820ec42 (b_alt.py `7dc734c8`, SHA256SUMS `486e9f6c`) · `.time`: s0 `4e1fcb3f`, s1a `94ece0d5`, s1b `03d74feb`, g0 `1ba1936a`, s2 `e5ef3e22`. Commit set as for D1: aggregates only.
