# Paper E' H2 precheck: registered outcome GO-own; H2 closed (CC-102)

**EXPLORATORY / DEV-PRECHECK (CC-098, CC-101, CC-102). Not confirmatory.** Times are UTC.

## Registered outcome (PRECHECK_NOTE.md, `flipbudget.decide`): GO-own
- **Run.** Code at 69ccf0e; M3 at d65d38b7; the job ran 2026-10-25 04:44:37–05:03:14Z.
- **Inputs.** Step 0 (CPU) pooled deletion ceiling 3.961 [3.463, 4.511], at least 2.0, so the job PROCEEDED (`ceiling.json`).
- **Bounds.** Pooled over 4 cells, F1 points × 100, paired image bootstrap, 2,000 draws, seed 0.
  - Cascade bound: 3.853 [3.374, 4.390].
  - Own bound: 2.536 [2.189, 2.949]. By model: Qwen2.5-VL-7B 2.850, InternVL3-8B 2.223.
- **Checks.** The verdict is the same with unlocated mentions counted as changeable or not (0 unlocated). No cell lacks changeable steps, and no model is report-only.
- **Parity.** Captions match the E' pilot's arm D at 100.0% in all 4 cells, so the rebuilt M3 is faithful (CC-101 ruling 5).
- GO-own authorises an H2 pilot note. It does not require one.

## POST HOC reading (not part of the registered rule; CC-102)
- **The headroom is all KTVIC.** The deletion ceiling per cell is 7.51 for Qwen on KTVIC and 7.10 for InternVL3 on KTVIC, against 0.64 and 0.60 on XM. So 92% of the pooled ceiling comes from KTVIC dev299.
  - There, a "wrong" mention is one no reference names: 279 of 610 mentions for Qwen and 265 of 587 for InternVL3.
  - That gold cannot tell a hallucination from an object the references missed. Paper A's registered result orders F1's verbosity slope by gold completeness, so a claim built on this headroom would contradict A.
- **Under verified gold the ceiling is below the SESOI.** On XM-dev300, with OIV7 human labels on 172 of 300 images, only 7 mentions per model are absent. Deleting all of them gains 0.64 and 0.60 points, under the SESOI of 2.0.
  - No other existing verified Vietnamese gold is free for this purpose: the complete-gold sets are A's test sets, and they are refused.
- **"Selective" selects almost nothing at β = 0.1.** |V_head| ≥ 2 holds at 46–57% of steps, and the median first changeable step is the first token. Between 49% and 69% of the right mentions are changeable too. This is the deletion-for-precision route that failed as C's guard (CC-099).
- **Alternatives rejected.** Requiring "XM gain > 0" would be too weak to mean anything. Requiring ≥ 2.0 on XM cannot be met. Lowering the SESOI after seeing these numbers would pick the effect size from the data.

## Decision (CC-102): H2 is closed. No H2 pilot note is written.
- **Next step.** E' goes to the PI. The options are: stop E' (the judge's recommendation), a new PI-chosen direction under CC-102's preconditions, or a negative-results note after A and B are submitted.
- **E' GPU spent.** H1 pilot 1.22 GPU-h (CC-100). H2 precheck 0.31 GPU-h (1,121 GPU-s). E's stage 1, 1.57 GPU-h, is recorded in its own STOP.md.
- **Restore check scope.** The O1 restore check covered the 271 mirrored files of c_stage1, c_stage2 and eprime_pilot. Two files existed only on M3 and could not be covered: `claude_ops/h2_precheck_operator.log` and `claude_ops/r_d65d38b.bundle`. Both were created on 2026-10-25 by this run's operator steps.
- **Other papers.** Nothing from this precheck goes into Paper A without its own ruling.
- **Records.** Captions and per-step records stay in output files on M3 and in local scratch; they are never committed. The local record is `.session_backup/2026-10-25/h2_precheck/` (RUN_RECORD.md, precheck_result.json dd64c205, ceiling.json, CHAIN.log).
