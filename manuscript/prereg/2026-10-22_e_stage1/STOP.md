# Paper E, stage 1: STOP (registered negative)

- **Verdict:** FAIL, from `score.py decide` on the stage-1 dev-A data. The judge ruled E stops at stage 1, and no stage-1b round runs (CC-097, 92%).
- **Pick:** `E:vi:sub:0.0`. Calibration was not kept. The best global scorer is `whole_raw`, both on bc and on τ.
- **A1 (bc margin):** −0.013, 95% CI [−0.107, 0.081], 77 pairs on 43 images. The registered requirement is ≥ +0.10 with the CI lower bound above 0, so A1 is **not met**.
- **A2 (τ):** +0.079 [−0.016, 0.176]. Met.
- **A3 (floor):** met.
- **Answer-token mass (CC-095 D1 and D3):**
  - yes_no_mass_median for qwen25vl_7b: en 0.9997, vi 0.9661. The vi value is an upper bound, because the `C` and `kh` pieces are counted.
  - For qwen3vl_8b: en 1.0000, vi 1.0000.
  - Vi minus en: −0.026 raw, 0 subtracted. D4 is not triggered.
- **Records:**
  - decide output `decide_stage1.json`, sha256 767ee7a6efb56d69…;
  - ledger `ledger.jsonl`, sha256 2ad94febb42bf0cb….
  - Both are kept with the run record, outside the repo.
- **Compute:** 1.57 GPU-h of the 4.0-h cap, on one RTX 3090. The job ran 11:45:30–13:21:16Z on 2026-10-22, at HEAD 4ee4e4e, with no failed or skipped step.
- **Data hygiene:** G9 deleted the 121 E-dev-A pair images from the GPU host at 13:21:54Z. No E stage-2 prereg will be written.
