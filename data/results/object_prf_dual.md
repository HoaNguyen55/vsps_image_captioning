# E1: object P/R/F1 under both matching rules, KTVIC test (558 images), 95% bootstrap CI (1,000 image resamples)

    NCS_DATA=... python scripts/object_prf.py --results <dir with *-detailed.preds.json> --ci

Exact = Table IV rule. Hypernym = the rule CHAIR-vi already uses: a mention is correct if it is a gold class or an ancestor of one (P_h); R_spec counts the most specific gold classes named exactly, R_vague also credits an ancestor. Report all three; the hypernym rule is not a replacement.

| system | P | R | F1 [CI] | P_h | R_spec | F1_spec [CI] | R_vague | F1_vague [CI] |
|---|---|---|---|---|---|---|---|---|
| **P1 gold-caption SFT** | **78.3** | 42.7 | **55.3 [53.0, 57.5]** | **80.3** | 41.8 | **55.0 [52.6, 57.3]** | 46.1 | **58.6 [56.5, 60.8]** |
| zero-shot Qwen2.5-VL-7B | 31.6 | **57.1** | 40.7 [39.2, 42.3] | 33.4 | **55.5** | 41.7 [40.1, 43.3] | **60.8** | 43.1 [41.5, 44.7] |
| VCD | 31.9 | 55.9 | 40.6 [38.9, 42.3] | 34.0 | 54.6 | 41.9 [40.2, 43.5] | 60.1 | 43.4 [41.8, 45.0] |
| VSPS main_s42 | 41.5 | 36.7 | 39.0 [37.1, 41.0] | 48.2 | 34.2 | 40.0 [38.0, 42.0] | 46.4 | 47.3 [45.4, 49.2] |
| VSPS main_s43 | 42.4 | 37.3 | 39.7 [37.7, 41.7] | 49.5 | 34.6 | 40.7 [38.7, 42.8] | 46.6 | 48.0 [46.1, 49.9] |
| VSPS main_s44 | 41.7 | 37.2 | 39.3 [37.4, 41.2] | 48.4 | 34.5 | 40.3 [38.3, 42.2] | 46.8 | 47.6 [45.7, 49.6] |
| p2-noverif4090 | 39.0 | 42.0 | 40.4 [38.6, 42.2] | 44.8 | 39.3 | 41.9 [40.1, 43.7] | 51.4 | 47.9 [46.1, 49.6] |
| vsps_neutral | 39.9 | 37.7 | 38.8 [37.0, 40.6] | 46.3 | 35.1 | 39.9 [38.0, 41.8] | 47.0 | 46.6 [44.8, 48.5] |

Readings:
- P1 is above every other system under all three rules, with CIs disjoint from all of them. The paper's baseline is P1.
- The exact rule ranks zero-shot ≈ VSPS (CIs overlap). The hypernym rule with R_vague ranks VSPS above zero-shot (47.3 vs 43.1, CIs disjoint), entirely through `người` (R2_05). R_spec gives the old ordering back, so this is a statement about naming level, not about content.
- Zero-shot R_spec/R_vague here are 55.5/60.8 against 55.8/61.1 in R2_05 (agent's ad-hoc script); this file is the reference implementation.
- v2raw and v3 preds are not in this directory yet; v3 eval is queued after the stage-1 pilot.
