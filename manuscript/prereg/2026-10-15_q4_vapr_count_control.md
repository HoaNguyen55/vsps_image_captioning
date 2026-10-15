# Pre-registration: R13-Q4, VaPR as a positive control for the preference count audit (sec. 9)

**Frozen:** 2026-10-15, before the VaPR count audit was computed. Mandate: PD-7 Q4.
**Frozen predictions (machine-readable):** `2026-10-15_q4_vapr_count_control.json`.
**Script:** `scripts/r13/r13_q4_vapr_count_audit.py`, sha256 `0e834cf703bed475cd11c356b8267f6549a635e6c4a2b2579a465f46233e8c75`. The script refuses to run if its own sha or any input sha differs from the JSON.

## Data and licence

- VaPR (Wadhawan et al., COLM 2025), `huggingface.co/datasets/VaPR-UCLA/vapr-30k` at commit `261940f2`, Apache-2.0. The release has 29,938 pairs; chosen responses come from LLaVA-665K and rejected responses are LLM-edited hard negatives matched for length and style.
- Stored as untrusted data in `.session_backup/2026-10-15/r13_data/vapr_30k/`. Parsing is limited to `json.loads`; the script is run with `python3 -E -P` from outside the folder.
- Input sha256s (VaPR json, the sec. 9 audit JSON, synonyms, E1 matcher) are listed in the JSON.

## Design

- **Procedure:** the same as Table 9.1. The E1 COCO-80 matcher is applied to the concatenated gpt turns of the chosen and rejected conversations. dk = classes(chosen) − classes(rejected). Pairs in which neither response names a class are dropped. Count-matched share = share with dk = 0.
- **Comparators:** the count-matched shares of HA-DPO, HSA-DPO and SENTINEL are read in code from `.session_backup/2026-10-14/r11_verify/c6_n3_rlaifv_rlhfv_audit.json` (`summary_table_7_datasets`).

## Frozen prediction

- **Prediction:** VaPR is length- and style-matched, so its count-matched share is **higher** than that of HA-DPO, HSA-DPO and SENTINEL. It is not predicted to be fully count-matched (share 1.0).
- **Pass rule:** the Wilson 95% lower bound of VaPR's count-matched share exceeds each comparator's share.
- **Verdict rule:** PASS if the pass rule holds. PARTIAL_POINT_ONLY if only the point estimate exceeds all three. FAIL otherwise.
- **Kill rule:** on FAIL, sec. 9 does not present VaPR as a positive control; the number is still reported.

## Scope

Only the **count** channel is claimed. The length channel is prior work (VaPR, HDPO). The share of chosen-fewer among unmatched pairs and the |Δwords| ≤ 2 subset are descriptive only.
