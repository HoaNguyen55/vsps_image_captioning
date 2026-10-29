## Supplement S. Registered per-run rows

These rows are the registered aggregates the scorer wrote to each scored set's ledger:
- Qwen2.5-VL at its frozen τ = −∞;
- InternVL3 at its frozen τ = 0.10 and at τ = −∞;
- the zero-shot arms;
- the CPU copy baselines.

They are copied from the ledgers with no recomputation. "n/a" marks a field that the scorer does not define for that row. CIDEr-D columns are ×100 on that set's own document frequencies. Rates and shares are fractions; ΔP_cm is in precision points.

Rows that no rule registered (InternVL3 τ ∈ {0.00, 0.20, 0.30, +∞}, Qwen2.5-VL τ = +∞, verifier AUROC) are left out of this table and are listed in Table S12 (Section 7.3). Table S13 gives every registered and reported row of the English arm (Section 8). Table S14 gives every row of the development-set mechanism ablations (Section 6.8), which are not test results.

**Table S1. Registered per-run rows, OV-test primary (1,941).**

| run | τ | CIDEr-D stripped | CIDEr-D as written | CIDEr-D PTB | CHAIR_i | mentions/img | ΔP_cm vs zs |
| --- | --- | --- | --- | --- | --- | --- | --- |
| qwen25vl_7b-ret-k8-first-T1 | −∞ | 39.81 | 33.75 | 44.26 | 0.246 | 2.38 | 5.41 |
| qwen25vl_7b-rand-k8-T1 | −∞ | 31.48 | 27.25 | 34.95 | 0.275 | 2.32 | 2.82 |
| qwen25vl_7b-fix-k8-T1 | −∞ | 33.48 | 28.73 | 37.31 | 0.266 | 2.52 | 4.74 |
| internvl3_8b-ret-k4-last-T2 | −∞ | 39.50 | 34.32 | 42.67 | 0.237 | 2.33 | 5.80 |
| internvl3_8b-ret-k4-last-T2 | 0.10 | 33.62 | 29.71 | 35.83 | 0.254 | 1.77 | 1.57 |
| internvl3_8b-rand-k4-T2 | −∞ | 35.80 | 31.38 | 38.41 | 0.263 | 2.29 | 3.54 |
| internvl3_8b-rand-k4-T2 | 0.10 | 32.96 | 29.20 | 35.32 | 0.267 | 1.99 | 1.40 |
| internvl3_8b-fix-k4-T2 | −∞ | 38.05 | 33.72 | 41.39 | 0.247 | 2.55 | 5.79 |
| internvl3_8b-fix-k4-T2 | 0.10 | 33.01 | 29.63 | 35.42 | 0.269 | 1.97 | 1.68 |
| qwen25vl_7b-zs | −∞ | 20.05 | 18.11 | 21.14 | 0.289 | 1.81 | 0.00 |
| internvl3_8b-zs | −∞ | 24.77 | 22.30 | 26.55 | 0.274 | 1.80 | 0.00 |
| nn-top1 | −∞ | 22.73 | 22.73 | 22.73 | 0.399 | 1.99 | n/a |
| nn-cons-k4 | −∞ | 26.17 | 26.17 | 26.17 | 0.393 | 2.08 | n/a |
| nn-cons-k8 | −∞ | 28.96 | 28.96 | 28.96 | 0.384 | 2.05 | n/a |

**Table S1 (continued). Guard and copy diagnostics for the same runs.**

| run | τ | nbr-only rate | rejected/img | deleted rate | fallback rate | 4-gram copy (memory) | near-verbatim share | hit_max rate |
| --- | --- | --- | --- | --- | --- | --- | --- | --- |
| qwen25vl_7b-ret-k8-first-T1 | −∞ | 0.421 | 0.000 | 0.000 | 0.000 | 0.401 | 0.015 | 0.003 |
| qwen25vl_7b-rand-k8-T1 | −∞ | 0.226 | 0.000 | 0.000 | 0.000 | 0.269 | 0.001 | 0.003 |
| qwen25vl_7b-fix-k8-T1 | −∞ | 0.253 | 0.000 | 0.000 | 0.000 | 0.299 | 0.001 | 0.004 |
| internvl3_8b-ret-k4-last-T2 | −∞ | 0.338 | 0.000 | 0.000 | 0.000 | 0.338 | 0.003 | 0.003 |
| internvl3_8b-ret-k4-last-T2 | 0.10 | 0.338 | 0.636 | 0.122 | 0.351 | 0.269 | 0.002 | 0.003 |
| internvl3_8b-rand-k4-T2 | −∞ | 0.147 | 0.000 | 0.000 | 0.000 | 0.279 | 0.000 | 0.001 |
| internvl3_8b-rand-k4-T2 | 0.10 | 0.147 | 0.303 | 0.086 | 0.177 | 0.249 | 0.000 | 0.001 |
| internvl3_8b-fix-k4-T2 | −∞ | 0.212 | 0.000 | 0.000 | 0.000 | 0.298 | 0.000 | 0.001 |
| internvl3_8b-fix-k4-T2 | 0.10 | 0.212 | 0.489 | 0.120 | 0.286 | 0.244 | 0.000 | 0.001 |
| qwen25vl_7b-zs | −∞ | 0.000 | 0.000 | 0.000 | 0.000 | 0.147 | n/a | 0.002 |
| internvl3_8b-zs | −∞ | 0.000 | 0.000 | 0.000 | 0.000 | 0.172 | n/a | 0.001 |
| nn-top1 | −∞ | n/a | n/a | n/a | n/a | n/a | n/a | n/a |
| nn-cons-k4 | −∞ | n/a | n/a | n/a | n/a | n/a | n/a | n/a |
| nn-cons-k8 | −∞ | n/a | n/a | n/a | n/a | n/a | n/a | n/a |

**Table S2. Registered per-run rows, OV-test full (2,001).**

| run | τ | CIDEr-D stripped | CIDEr-D as written | CIDEr-D PTB | CHAIR_i | mentions/img | ΔP_cm vs zs |
| --- | --- | --- | --- | --- | --- | --- | --- |
| qwen25vl_7b-ret-k8-first-T1 | −∞ | 39.73 | 33.64 | 44.20 | 0.245 | 2.39 | 5.34 |
| qwen25vl_7b-rand-k8-T1 | −∞ | 31.44 | 27.20 | 34.91 | 0.274 | 2.33 | 2.78 |
| qwen25vl_7b-fix-k8-T1 | −∞ | 33.48 | 28.70 | 37.31 | 0.265 | 2.53 | 4.78 |
| internvl3_8b-ret-k4-last-T2 | −∞ | 39.49 | 34.28 | 42.66 | 0.237 | 2.34 | 5.49 |
| internvl3_8b-ret-k4-last-T2 | 0.10 | 33.64 | 29.70 | 35.86 | 0.253 | 1.78 | 1.35 |
| internvl3_8b-rand-k4-T2 | −∞ | 35.81 | 31.34 | 38.47 | 0.262 | 2.30 | 3.22 |
| internvl3_8b-rand-k4-T2 | 0.10 | 33.01 | 29.21 | 35.41 | 0.266 | 2.00 | 1.16 |
| internvl3_8b-fix-k4-T2 | −∞ | 37.95 | 33.61 | 41.34 | 0.247 | 2.57 | 5.44 |
| internvl3_8b-fix-k4-T2 | 0.10 | 32.98 | 29.60 | 35.42 | 0.267 | 1.99 | 1.56 |
| qwen25vl_7b-zs | −∞ | 20.09 | 18.13 | 21.16 | 0.287 | 1.83 | 0.00 |
| internvl3_8b-zs | −∞ | 24.80 | 22.31 | 26.59 | 0.271 | 1.81 | 0.00 |
| nn-top1 | −∞ | 22.74 | 22.74 | 22.74 | 0.398 | 2.00 | n/a |
| nn-cons-k4 | −∞ | 26.34 | 26.34 | 26.34 | 0.392 | 2.09 | n/a |
| nn-cons-k8 | −∞ | 28.94 | 28.94 | 28.94 | 0.382 | 2.05 | n/a |

**Table S2 (continued). Guard and copy diagnostics for the same runs.**

| run | τ | nbr-only rate | rejected/img | deleted rate | fallback rate | 4-gram copy (memory) | near-verbatim share | hit_max rate |
| --- | --- | --- | --- | --- | --- | --- | --- | --- |
| qwen25vl_7b-ret-k8-first-T1 | −∞ | 0.419 | 0.000 | 0.000 | 0.000 | 0.402 | 0.014 | 0.002 |
| qwen25vl_7b-rand-k8-T1 | −∞ | 0.226 | 0.000 | 0.000 | 0.000 | 0.269 | 0.000 | 0.003 |
| qwen25vl_7b-fix-k8-T1 | −∞ | 0.253 | 0.000 | 0.000 | 0.000 | 0.300 | 0.000 | 0.003 |
| internvl3_8b-ret-k4-last-T2 | −∞ | 0.337 | 0.000 | 0.000 | 0.000 | 0.339 | 0.002 | 0.002 |
| internvl3_8b-ret-k4-last-T2 | 0.10 | 0.337 | 0.634 | 0.121 | 0.350 | 0.270 | 0.002 | 0.002 |
| internvl3_8b-rand-k4-T2 | −∞ | 0.147 | 0.000 | 0.000 | 0.000 | 0.280 | 0.000 | 0.001 |
| internvl3_8b-rand-k4-T2 | 0.10 | 0.147 | 0.303 | 0.084 | 0.177 | 0.250 | 0.000 | 0.001 |
| internvl3_8b-fix-k4-T2 | −∞ | 0.210 | 0.000 | 0.000 | 0.000 | 0.298 | 0.000 | 0.001 |
| internvl3_8b-fix-k4-T2 | 0.10 | 0.210 | 0.487 | 0.119 | 0.286 | 0.245 | 0.000 | 0.001 |
| qwen25vl_7b-zs | −∞ | 0.000 | 0.000 | 0.000 | 0.000 | 0.148 | n/a | 0.002 |
| internvl3_8b-zs | −∞ | 0.000 | 0.000 | 0.000 | 0.000 | 0.172 | n/a | 0.000 |
| nn-top1 | −∞ | n/a | n/a | n/a | n/a | n/a | n/a | n/a |
| nn-cons-k4 | −∞ | n/a | n/a | n/a | n/a | n/a | n/a | n/a |
| nn-cons-k8 | −∞ | n/a | n/a | n/a | n/a | n/a | n/a | n/a |

**Table S3. Registered per-run rows, XM-test2500 (2,500).**

| run | τ | CIDEr-D stripped | CIDEr-D as written | CIDEr-D PTB | CHAIR_i | mentions/img | ΔP_cm vs zs |
| --- | --- | --- | --- | --- | --- | --- | --- |
| qwen25vl_7b-ret-k8-first-T1 | −∞ | 57.70 | 59.13 | 58.62 | 0.333 | 1.70 | 0.12 |
| qwen25vl_7b-rand-k8-T1 | −∞ | 54.56 | 56.53 | 55.44 | 0.335 | 1.67 | 0.73 |
| qwen25vl_7b-fix-k8-T1 | −∞ | 51.83 | 54.38 | 52.79 | 0.309 | 1.55 | 1.13 |
| internvl3_8b-ret-k4-last-T2 | −∞ | 56.35 | 56.32 | 57.41 | 0.320 | 1.75 | 1.00 |
| internvl3_8b-ret-k4-last-T2 | 0.10 | 52.85 | 53.47 | 53.68 | 0.301 | 1.42 | 0.13 |
| internvl3_8b-rand-k4-T2 | −∞ | 56.17 | 56.36 | 57.23 | 0.322 | 1.74 | 1.25 |
| internvl3_8b-rand-k4-T2 | 0.10 | 54.59 | 55.14 | 55.64 | 0.314 | 1.60 | 1.01 |
| internvl3_8b-fix-k4-T2 | −∞ | 55.14 | 56.71 | 55.98 | 0.298 | 1.53 | 1.13 |
| internvl3_8b-fix-k4-T2 | 0.10 | 53.65 | 55.33 | 54.53 | 0.298 | 1.45 | 0.74 |
| qwen25vl_7b-zs | −∞ | 43.74 | 45.51 | 44.64 | 0.335 | 1.57 | 0.00 |
| internvl3_8b-zs | −∞ | 42.84 | 44.87 | 43.46 | 0.314 | 1.47 | 0.00 |
| nn-top1 | −∞ | 13.96 | 13.96 | 14.11 | 0.622 | 1.50 | n/a |
| nn-cons-k4 | −∞ | 14.61 | 14.61 | 14.79 | 0.625 | 1.63 | n/a |
| nn-cons-k8 | −∞ | 15.39 | 15.39 | 15.58 | 0.624 | 1.67 | n/a |

**Table S3 (continued). Guard and copy diagnostics for the same runs.**

| run | τ | nbr-only rate | rejected/img | deleted rate | fallback rate | 4-gram copy (memory) | near-verbatim share | hit_max rate |
| --- | --- | --- | --- | --- | --- | --- | --- | --- |
| qwen25vl_7b-ret-k8-first-T1 | −∞ | 0.289 | 0.000 | 0.000 | 0.000 | 0.238 | 0.005 | 0.000 |
| qwen25vl_7b-rand-k8-T1 | −∞ | 0.125 | 0.000 | 0.000 | 0.000 | 0.175 | 0.000 | 0.000 |
| qwen25vl_7b-fix-k8-T1 | −∞ | 0.083 | 0.000 | 0.000 | 0.000 | 0.170 | 0.000 | 0.000 |
| internvl3_8b-ret-k4-last-T2 | −∞ | 0.242 | 0.000 | 0.000 | 0.000 | 0.196 | 0.000 | 0.000 |
| internvl3_8b-ret-k4-last-T2 | 0.10 | 0.242 | 0.365 | 0.125 | 0.183 | 0.170 | 0.000 | 0.000 |
| internvl3_8b-rand-k4-T2 | −∞ | 0.089 | 0.000 | 0.000 | 0.000 | 0.173 | 0.000 | 0.000 |
| internvl3_8b-rand-k4-T2 | 0.10 | 0.089 | 0.146 | 0.059 | 0.077 | 0.165 | 0.000 | 0.000 |
| internvl3_8b-fix-k4-T2 | −∞ | 0.072 | 0.000 | 0.000 | 0.000 | 0.159 | 0.000 | 0.000 |
| internvl3_8b-fix-k4-T2 | 0.10 | 0.072 | 0.103 | 0.027 | 0.070 | 0.153 | 0.000 | 0.000 |
| qwen25vl_7b-zs | −∞ | 0.000 | 0.000 | 0.000 | 0.000 | 0.108 | n/a | 0.001 |
| internvl3_8b-zs | −∞ | 0.000 | 0.000 | 0.000 | 0.000 | 0.123 | n/a | 0.001 |
| nn-top1 | −∞ | n/a | n/a | n/a | n/a | n/a | n/a | n/a |
| nn-cons-k4 | −∞ | n/a | n/a | n/a | n/a | n/a | n/a | n/a |
| nn-cons-k8 | −∞ | n/a | n/a | n/a | n/a | n/a | n/a | n/a |

**Table S4. Registered per-run rows, XM-test2500 without the three-reference images (2,392).**

| run | τ | CIDEr-D stripped | CIDEr-D as written | CIDEr-D PTB | CHAIR_i | mentions/img | ΔP_cm vs zs |
| --- | --- | --- | --- | --- | --- | --- | --- |
| qwen25vl_7b-ret-k8-first-T1 | −∞ | 57.64 | 59.10 | 58.55 | 0.335 | 1.70 | 0.19 |
| qwen25vl_7b-rand-k8-T1 | −∞ | 54.26 | 56.28 | 55.15 | 0.337 | 1.68 | 0.79 |
| qwen25vl_7b-fix-k8-T1 | −∞ | 51.33 | 53.91 | 52.27 | 0.313 | 1.55 | 1.11 |
| internvl3_8b-ret-k4-last-T2 | −∞ | 56.25 | 56.28 | 57.35 | 0.322 | 1.76 | 1.04 |
| internvl3_8b-ret-k4-last-T2 | 0.10 | 52.74 | 53.39 | 53.57 | 0.303 | 1.43 | 0.13 |
| internvl3_8b-rand-k4-T2 | −∞ | 56.06 | 56.30 | 57.14 | 0.325 | 1.74 | 1.17 |
| internvl3_8b-rand-k4-T2 | 0.10 | 54.48 | 55.09 | 55.55 | 0.316 | 1.60 | 0.95 |
| internvl3_8b-fix-k4-T2 | −∞ | 54.98 | 56.59 | 55.85 | 0.297 | 1.53 | 1.18 |
| internvl3_8b-fix-k4-T2 | 0.10 | 53.56 | 55.28 | 54.45 | 0.298 | 1.46 | 0.81 |
| qwen25vl_7b-zs | −∞ | 43.42 | 45.21 | 44.34 | 0.338 | 1.57 | 0.00 |
| internvl3_8b-zs | −∞ | 42.63 | 44.67 | 43.25 | 0.316 | 1.47 | 0.00 |
| nn-top1 | −∞ | 14.02 | 14.02 | 14.17 | 0.623 | 1.51 | n/a |
| nn-cons-k4 | −∞ | 14.63 | 14.63 | 14.82 | 0.626 | 1.63 | n/a |
| nn-cons-k8 | −∞ | 15.46 | 15.46 | 15.66 | 0.626 | 1.69 | n/a |

**Table S4 (continued). Guard and copy diagnostics for the same runs.**

| run | τ | nbr-only rate | rejected/img | deleted rate | fallback rate | 4-gram copy (memory) | near-verbatim share | hit_max rate |
| --- | --- | --- | --- | --- | --- | --- | --- | --- |
| qwen25vl_7b-ret-k8-first-T1 | −∞ | 0.288 | 0.000 | 0.000 | 0.000 | 0.238 | 0.004 | 0.000 |
| qwen25vl_7b-rand-k8-T1 | −∞ | 0.124 | 0.000 | 0.000 | 0.000 | 0.176 | 0.000 | 0.000 |
| qwen25vl_7b-fix-k8-T1 | −∞ | 0.083 | 0.000 | 0.000 | 0.000 | 0.169 | 0.000 | 0.000 |
| internvl3_8b-ret-k4-last-T2 | −∞ | 0.244 | 0.000 | 0.000 | 0.000 | 0.196 | 0.000 | 0.000 |
| internvl3_8b-ret-k4-last-T2 | 0.10 | 0.244 | 0.369 | 0.125 | 0.184 | 0.171 | 0.000 | 0.000 |
| internvl3_8b-rand-k4-T2 | −∞ | 0.091 | 0.000 | 0.000 | 0.000 | 0.173 | 0.000 | 0.000 |
| internvl3_8b-rand-k4-T2 | 0.10 | 0.091 | 0.149 | 0.061 | 0.079 | 0.164 | 0.000 | 0.000 |
| internvl3_8b-fix-k4-T2 | −∞ | 0.072 | 0.000 | 0.000 | 0.000 | 0.158 | 0.000 | 0.000 |
| internvl3_8b-fix-k4-T2 | 0.10 | 0.072 | 0.103 | 0.026 | 0.071 | 0.152 | 0.000 | 0.000 |
| qwen25vl_7b-zs | −∞ | 0.000 | 0.000 | 0.000 | 0.000 | 0.108 | n/a | 0.001 |
| internvl3_8b-zs | −∞ | 0.000 | 0.000 | 0.000 | 0.000 | 0.123 | n/a | 0.001 |
| nn-top1 | −∞ | n/a | n/a | n/a | n/a | n/a | n/a | n/a |
| nn-cons-k4 | −∞ | n/a | n/a | n/a | n/a | n/a | n/a | n/a |
| nn-cons-k8 | −∞ | n/a | n/a | n/a | n/a | n/a | n/a | n/a |


**Table S5. Registered control rows on all four scored sets: S-zf, copy baselines and the PTB column (each cell `ret` minus the named comparison, stripped CIDEr-D unless marked).**

| set | backbone | `ret` − `zs` | `ret` − `fix` | `ret` − NN-top1 | `ret` − NN-consensus | `ret` − `rand`, PTB column |
|---|---|---|---|---|---|---|
| OV-test primary (1,941) | pooled | +14.30 [13.38, 15.24] | +3.47 [2.54, 4.41] | +13.98 [12.63, 15.38] | +9.15 [7.84, 10.47] | +4.91 [3.93, 6.00] |
| OV-test primary (1,941) | Qwen2.5-VL | +19.76 [18.33, 21.10] | +6.33 [5.02, 7.72] | +17.08 [15.57, 18.72] | +10.85 [9.22, 12.47] | +9.31 [7.94, 10.80] |
| OV-test primary (1,941) | InternVL3 | +8.85 [7.76, 9.98] | +0.61 [−0.68, 1.87] | +10.89 [9.31, 12.51] | +7.45 [5.90, 9.05] | +0.51 [−0.81, 1.87] |
| OV-test full (2,001) | pooled | +14.24 [13.29, 15.15] | +3.46 [2.56, 4.43] | +13.95 [12.53, 15.30] | +9.05 [7.78, 10.27] | +4.87 [3.83, 5.82] |
| OV-test full (2,001) | Qwen2.5-VL | +19.64 [18.24, 21.00] | +6.25 [4.92, 7.58] | +16.99 [15.44, 18.56] | +10.79 [9.24, 12.30] | +9.29 [7.93, 10.65] |
| OV-test full (2,001) | InternVL3 | +8.84 [7.72, 9.93] | +0.66 [−0.55, 1.91] | +10.90 [9.31, 12.40] | +7.30 [5.76, 8.75] | +0.44 [−0.94, 1.73] |
| XM-test2500 (2,500) | pooled | +11.99 [10.68, 13.34] | +2.53 [1.32, 3.80] | +41.32 [39.52, 43.08] | +40.28 [38.50, 42.08] | +0.60 [−0.54, 1.85] |
| XM-test2500 (2,500) | Qwen2.5-VL | +13.96 [12.09, 15.87] | +5.87 [4.14, 7.65] | +43.75 [41.59, 46.04] | +42.32 [40.17, 44.62] | +3.17 [1.50, 4.99] |
| XM-test2500 (2,500) | InternVL3 | +10.01 [8.41, 11.62] | −0.81 [−2.41, 0.76] | +38.89 [36.95, 40.83] | +38.24 [36.25, 40.28] | −1.97 [−3.59, −0.31] |
| XM-test2500 without three-ref (2,392) | pooled | +12.16 [10.82, 13.53] | +2.75 [1.42, 4.05] | +41.17 [39.38, 42.93] | +40.15 [38.36, 41.93] | +0.71 [−0.54, 1.99] |
| XM-test2500 without three-ref (2,392) | Qwen2.5-VL | +14.22 [12.14, 16.20] | +6.32 [4.48, 8.16] | +43.63 [41.49, 45.73] | +42.19 [40.00, 44.38] | +3.40 [1.56, 5.19] |
| XM-test2500 without three-ref (2,392) | InternVL3 | +10.10 [8.47, 11.61] | −0.82 [−2.47, 0.80] | +38.72 [36.61, 40.77] | +38.11 [36.01, 40.13] | −1.98 [−3.63, −0.23] |

**Table S6. Style report, source-dataset share, length gap and near-verbatim share, all four scored sets.** For XM3600 queries the source-dataset share is the share of shown clusters with an XM3600 member; the memory holds none.

| set | backbone | arm | mean syllables | ends in punctuation | top-3 opening share | source-dataset share |
|---|---|---|---|---|---|---|
| OV-test primary (1,941) | Qwen2.5-VL | `ret` | 18.47 | 0.994 | 0.350 | 0.996 |
| OV-test primary (1,941) | Qwen2.5-VL | `rand` | 17.20 | 0.997 | 0.357 | 0.995 |
| OV-test primary (1,941) | Qwen2.5-VL | `fix` | 18.20 | 0.995 | 0.417 | 1.000 |
| OV-test primary (1,941) | Qwen2.5-VL | length gap, near-verbatim share | 0.074 |  |  | 0.015 |
| OV-test primary (1,941) | InternVL3 | `ret` | 17.02 | 0.880 | 0.154 | 0.996 |
| OV-test primary (1,941) | InternVL3 | `rand` | 17.72 | 0.869 | 0.176 | 0.994 |
| OV-test primary (1,941) | InternVL3 | `fix` | 17.94 | 0.778 | 0.205 | 1.000 |
| OV-test primary (1,941) | InternVL3 | length gap, near-verbatim share | 0.039 |  |  | 0.002 |
| OV-test full (2,001) | Qwen2.5-VL | `ret` | 18.50 | 0.995 | 0.353 | 0.996 |
| OV-test full (2,001) | Qwen2.5-VL | `rand` | 17.20 | 0.998 | 0.361 | 0.995 |
| OV-test full (2,001) | Qwen2.5-VL | `fix` | 18.20 | 0.996 | 0.421 | 1.000 |
| OV-test full (2,001) | Qwen2.5-VL | length gap, near-verbatim share | 0.076 |  |  | 0.014 |
| OV-test full (2,001) | InternVL3 | `ret` | 17.02 | 0.883 | 0.155 | 0.996 |
| OV-test full (2,001) | InternVL3 | `rand` | 17.76 | 0.871 | 0.182 | 0.994 |
| OV-test full (2,001) | InternVL3 | `fix` | 17.96 | 0.781 | 0.211 | 1.000 |
| OV-test full (2,001) | InternVL3 | length gap, near-verbatim share | 0.042 |  |  | 0.002 |
| XM-test2500 (2,500) | Qwen2.5-VL | `ret` | 14.79 | 0.998 | 0.250 | 0.000 |
| XM-test2500 (2,500) | Qwen2.5-VL | `rand` | 13.93 | 0.997 | 0.242 | 0.000 |
| XM-test2500 (2,500) | Qwen2.5-VL | `fix` | 12.82 | 0.999 | 0.277 | 0.000 |
| XM-test2500 (2,500) | Qwen2.5-VL | length gap, near-verbatim share | 0.062 |  |  | 0.005 |
| XM-test2500 (2,500) | InternVL3 | `ret` | 15.31 | 0.886 | 0.139 | 0.000 |
| XM-test2500 (2,500) | InternVL3 | `rand` | 15.75 | 0.883 | 0.186 | 0.000 |
| XM-test2500 (2,500) | InternVL3 | `fix` | 13.65 | 0.902 | 0.210 | 0.000 |
| XM-test2500 (2,500) | InternVL3 | length gap, near-verbatim share | 0.028 |  |  | 0.000 |
| XM-test2500 without three-ref (2,392) | Qwen2.5-VL | `ret` | 14.82 | 0.999 | 0.249 | 0.000 |
| XM-test2500 without three-ref (2,392) | Qwen2.5-VL | `rand` | 13.93 | 0.997 | 0.241 | 0.000 |
| XM-test2500 without three-ref (2,392) | Qwen2.5-VL | `fix` | 12.82 | 0.999 | 0.278 | 0.000 |
| XM-test2500 without three-ref (2,392) | Qwen2.5-VL | length gap, near-verbatim share | 0.064 |  |  | 0.004 |
| XM-test2500 without three-ref (2,392) | InternVL3 | `ret` | 15.35 | 0.887 | 0.139 | 0.000 |
| XM-test2500 without three-ref (2,392) | InternVL3 | `rand` | 15.77 | 0.884 | 0.185 | 0.000 |
| XM-test2500 without three-ref (2,392) | InternVL3 | `fix` | 13.67 | 0.905 | 0.209 | 0.000 |
| XM-test2500 without three-ref (2,392) | InternVL3 | length gap, near-verbatim share | 0.026 |  |  | 0.000 |

**Table S7. Dose-response on all four scored sets: pooled `ret` − `rand` within tertiles of the nearest eligible-cluster cosine, cuts per scored set.**

| set | cosine cuts | low | mid | high |
|---|---|---|---|---|
| OV-test primary (1,941) | 0.802, 0.865 | +4.40 [2.84, 6.03] (n = 647) | +2.95 [1.14, 4.79] (n = 647) | +6.13 [4.36, 7.87] (n = 647) |
| OV-test full (2,001) | 0.803, 0.865 | +4.36 [2.78, 5.92] (n = 667) | +2.75 [1.01, 4.63] (n = 667) | +6.27 [4.56, 8.03] (n = 667) |
| XM-test2500 (2,500) | 0.624, 0.680 | +1.64 [−0.31, 3.69] (n = 833) | +2.28 [0.13, 4.48] (n = 833) | −1.82 [−3.96, 0.27] (n = 834) |
| XM-test2500 without three-ref (2,392) | 0.624, 0.680 | +1.37 [−0.58, 3.45] (n = 797) | +2.44 [0.17, 4.76] (n = 797) | −1.34 [−3.46, 0.79] (n = 798) |

**Table S8. Neighbour-only object precision (a level, not a difference) of `ret` at the frozen τ.** OV-test uses reference gold; XM-test2500 uses the human-verified Open Images labels, scored offline. A CI of [100.00, 100.00] means every resampled mention was verified, and it is not informative at that count.

| set (gold) | backbone | neighbour-only precision [95% CI] | mentions | share of images with ≥ 1 |
|---|---|---|---|---|
| OV-test primary (1,941) | Qwen2.5-VL | 73.41 [71.27, 75.34] | 1,933 | 0.630 |
| OV-test primary (1,941) | InternVL3 | 77.44 [70.99, 84.02] | 164 | 0.079 |
| OV-test primary (1,941) | pooled | 73.72 [71.72, 75.64] | 2,097 | 0.648 |
| OV-test full (2,001) | Qwen2.5-VL | 73.55 [71.44, 75.55] | 1,996 | 0.631 |
| OV-test full (2,001) | InternVL3 | 77.51 [70.59, 83.71] | 169 | 0.079 |
| OV-test full (2,001) | pooled | 73.86 [71.81, 75.81] | 2,165 | 0.650 |
| XM-test2500 (2,500) | Qwen2.5-VL | 92.82 [89.03, 96.28] | 195 | 0.070 |
| XM-test2500 (2,500) | InternVL3 | 100.00 [100.00, 100.00] | 16 | 0.006 |
| XM-test2500 (2,500) | pooled | 93.36 [89.87, 96.59] | 211 | 0.073 |
| XM-test2500 without three-ref (2,392) | Qwen2.5-VL | 92.71 [88.57, 96.02] | 192 | 0.072 |
| XM-test2500 without three-ref (2,392) | InternVL3 | 100.00 [100.00, 100.00] | 16 | 0.007 |
| XM-test2500 without three-ref (2,392) | pooled | 93.27 [89.42, 96.36] | 208 | 0.075 |

**Table S9. Stage-B guard AUROC of the neighbour-only items of `ret` against reference gold, at τ = −∞.** Diagnostic only. The study meant to interpret it is stopped, and no claim is made from it.

| set | generator | items | supported | AUROC of s | AUROC of p_with | AUROC of p_without |
|---|---|---|---|---|---|---|
| OV-dev-B | Qwen2.5-VL | 900 | 658 | 0.582 | 0.703 | 0.542 |
| OV-dev-B | InternVL3 | 722 | 559 | 0.519 | 0.672 | 0.564 |
| XM-dev500 | Qwen2.5-VL | 266 | 142 | 0.551 | 0.611 | 0.512 |
| XM-dev500 | InternVL3 | 227 | 133 | 0.559 | 0.630 | 0.559 |

### All configurations tried

Every configuration decoded at stages A and B is listed, broken ones included, from the stage ledgers. For a run that a stage re-scored (with identical values), the last row is shown, as that stage's decision rule uses it.

**Table S10. Stage A (KTVIC dev299 and OV-dev-A).**

| run | τ | n | CIDEr-D stripped | ΔP_cm vs zs | near-verbatim share | hit_max rate | mean syllables |
|------------------------------------------|---------|---------|---------|---------|---------|---------|---------|
| `c1_qwen25vl_7b_ktvic_dev299-ret-k4-last-T1` | −∞ | 299 | 55.82 | 5.64 | 0.010 | 0.000 | 16.36 |
| `c1_qwen25vl_7b_ktvic_dev299-ret-k4-last-T1` | +∞ | 299 | 43.45 | 1.96 | 0.003 | 0.000 | 15.13 |
| `c1_qwen25vl_7b_ktvic_dev299-rand-k4-T1` | −∞ | 299 | 48.90 | 1.68 | 0.000 | 0.000 | 16.38 |
| `c1_qwen25vl_7b_ktvic_dev299-rand-k4-T1` | +∞ | 299 | 45.59 | 0.00 | 0.000 | 0.000 | 15.87 |
| `dp_qwen25vl_7b_ktvic_dev299-short-T0` | −∞ | 299 | 33.02 | 0.00 | n/a | 0.003 | 16.58 |
| `c1_qwen25vl_7b_ktvic_dev299-ret-k2-first-T1` | −∞ | 299 | 51.17 | 3.75 | 0.007 | 0.000 | 15.55 |
| `c1_qwen25vl_7b_ktvic_dev299-ret-k2-first-T1` | 0.00 | 299 | 50.43 | 3.39 | 0.007 | 0.000 | 15.24 |
| `c1_qwen25vl_7b_ktvic_dev299-ret-k2-first-T1` | 0.10 | 299 | 49.51 | 4.88 | 0.007 | 0.000 | 14.51 |
| `c1_qwen25vl_7b_ktvic_dev299-ret-k2-first-T1` | 0.20 | 299 | 45.76 | 2.45 | 0.007 | 0.000 | 14.48 |
| `c1_qwen25vl_7b_ktvic_dev299-ret-k2-first-T1` | 0.30 | 299 | 44.89 | 2.65 | 0.007 | 0.000 | 14.49 |
| `c1_qwen25vl_7b_ktvic_dev299-ret-k2-first-T1` | +∞ | 299 | 43.53 | 0.61 | 0.007 | 0.000 | 14.56 |
| `c1_qwen25vl_7b_ktvic_dev299-ret-k2-last-T1` | −∞ | 299 | 52.99 | 6.18 | 0.017 | 0.000 | 15.26 |
| `c1_qwen25vl_7b_ktvic_dev299-ret-k2-last-T1` | 0.00 | 299 | 52.72 | 6.21 | 0.010 | 0.000 | 15.07 |
| `c1_qwen25vl_7b_ktvic_dev299-ret-k2-last-T1` | 0.10 | 299 | 50.06 | 5.57 | 0.010 | 0.000 | 14.44 |
| `c1_qwen25vl_7b_ktvic_dev299-ret-k2-last-T1` | 0.20 | 299 | 46.31 | 2.99 | 0.007 | 0.000 | 14.49 |
| `c1_qwen25vl_7b_ktvic_dev299-ret-k2-last-T1` | 0.30 | 299 | 45.45 | 3.19 | 0.007 | 0.000 | 14.46 |
| `c1_qwen25vl_7b_ktvic_dev299-ret-k2-last-T1` | +∞ | 299 | 43.67 | 1.19 | 0.007 | 0.000 | 14.55 |
| `c1_qwen25vl_7b_ktvic_dev299-ret-k4-first-T1` | −∞ | 299 | 55.42 | 4.52 | 0.023 | 0.000 | 16.71 |
| `c1_qwen25vl_7b_ktvic_dev299-ret-k4-first-T1` | 0.00 | 299 | 53.20 | 4.76 | 0.020 | 0.000 | 16.25 |
| `c1_qwen25vl_7b_ktvic_dev299-ret-k4-first-T1` | 0.10 | 299 | 50.80 | 5.17 | 0.017 | 0.000 | 15.14 |
| `c1_qwen25vl_7b_ktvic_dev299-ret-k4-first-T1` | 0.20 | 299 | 47.69 | 2.72 | 0.013 | 0.000 | 15.06 |
| `c1_qwen25vl_7b_ktvic_dev299-ret-k4-first-T1` | 0.30 | 299 | 47.57 | 3.26 | 0.013 | 0.000 | 15.12 |
| `c1_qwen25vl_7b_ktvic_dev299-ret-k4-first-T1` | +∞ | 299 | 45.72 | 1.33 | 0.013 | 0.000 | 15.20 |
| `c1_qwen25vl_7b_ktvic_dev299-ret-k4-last-T1` | 0.00 | 299 | 53.36 | 5.48 | 0.007 | 0.000 | 16.05 |
| `c1_qwen25vl_7b_ktvic_dev299-ret-k4-last-T1` | 0.10 | 299 | 50.91 | 5.71 | 0.007 | 0.000 | 15.07 |
| `c1_qwen25vl_7b_ktvic_dev299-ret-k4-last-T1` | 0.20 | 299 | 46.38 | 3.39 | 0.003 | 0.000 | 14.98 |
| `c1_qwen25vl_7b_ktvic_dev299-ret-k4-last-T1` | 0.30 | 299 | 44.93 | 3.75 | 0.003 | 0.000 | 15.02 |
| `c1_qwen25vl_7b_ktvic_dev299-ret-k8-first-T1` | −∞ | 299 | 58.66 | 6.38 | 0.027 | 0.003 | 17.22 |
| `c1_qwen25vl_7b_ktvic_dev299-ret-k8-first-T1` | 0.00 | 299 | 56.97 | 6.25 | 0.023 | 0.003 | 16.66 |
| `c1_qwen25vl_7b_ktvic_dev299-ret-k8-first-T1` | 0.10 | 299 | 54.57 | 7.53 | 0.023 | 0.003 | 15.27 |
| `c1_qwen25vl_7b_ktvic_dev299-ret-k8-first-T1` | 0.20 | 299 | 49.93 | 3.88 | 0.023 | 0.003 | 15.15 |
| `c1_qwen25vl_7b_ktvic_dev299-ret-k8-first-T1` | 0.30 | 299 | 48.89 | 3.85 | 0.023 | 0.003 | 15.13 |
| `c1_qwen25vl_7b_ktvic_dev299-ret-k8-first-T1` | +∞ | 299 | 46.34 | 1.53 | 0.023 | 0.003 | 15.20 |
| `c1_qwen25vl_7b_ktvic_dev299-ret-k8-last-T1` | −∞ | 299 | 53.52 | 2.64 | 0.013 | 0.000 | 17.28 |
| `c1_qwen25vl_7b_ktvic_dev299-ret-k8-last-T1` | 0.00 | 299 | 49.49 | 2.10 | 0.013 | 0.000 | 16.70 |
| `c1_qwen25vl_7b_ktvic_dev299-ret-k8-last-T1` | 0.10 | 299 | 48.62 | 3.53 | 0.013 | 0.000 | 15.40 |
| `c1_qwen25vl_7b_ktvic_dev299-ret-k8-last-T1` | 0.20 | 299 | 46.67 | 1.58 | 0.013 | 0.000 | 15.00 |
| `c1_qwen25vl_7b_ktvic_dev299-ret-k8-last-T1` | 0.30 | 299 | 45.73 | 1.76 | 0.013 | 0.000 | 14.99 |
| `c1_qwen25vl_7b_ktvic_dev299-ret-k8-last-T1` | +∞ | 299 | 43.99 | 0.20 | 0.013 | 0.000 | 15.15 |
| `c1_qwen25vl_7b_ktvic_dev299-ret-k4-last-T2` | −∞ | 299 | 56.28 | 4.24 | 0.007 | 0.000 | 15.32 |
| `c1_qwen25vl_7b_ktvic_dev299-ret-k4-last-T2` | 0.00 | 299 | 54.18 | 4.46 | 0.003 | 0.000 | 15.09 |
| `c1_qwen25vl_7b_ktvic_dev299-ret-k4-last-T2` | 0.10 | 299 | 50.93 | 4.71 | 0.003 | 0.000 | 14.45 |
| `c1_qwen25vl_7b_ktvic_dev299-ret-k4-last-T2` | 0.20 | 299 | 46.66 | 3.90 | 0.003 | 0.000 | 14.57 |
| `c1_qwen25vl_7b_ktvic_dev299-ret-k4-last-T2` | 0.30 | 299 | 45.63 | 4.07 | 0.003 | 0.000 | 14.56 |
| `c1_qwen25vl_7b_ktvic_dev299-ret-k4-last-T2` | +∞ | 299 | 44.74 | 2.62 | 0.003 | 0.000 | 14.65 |
| `c1_qwen25vl_7b_ktvic_dev299-rand-k2-T1` | −∞ | 299 | 48.74 | 2.08 | 0.000 | 0.000 | 15.56 |
| `c1_qwen25vl_7b_ktvic_dev299-rand-k2-T1` | 0.00 | 299 | 47.93 | 2.08 | 0.000 | 0.000 | 15.49 |
| `c1_qwen25vl_7b_ktvic_dev299-rand-k2-T1` | 0.10 | 299 | 47.74 | 2.46 | 0.000 | 0.000 | 15.43 |
| `c1_qwen25vl_7b_ktvic_dev299-rand-k2-T1` | 0.20 | 299 | 46.66 | 1.51 | 0.000 | 0.000 | 15.46 |
| `c1_qwen25vl_7b_ktvic_dev299-rand-k2-T1` | 0.30 | 299 | 45.96 | 1.32 | 0.000 | 0.000 | 15.53 |
| `c1_qwen25vl_7b_ktvic_dev299-rand-k2-T1` | +∞ | 299 | 45.86 | 1.13 | 0.000 | 0.000 | 15.56 |
| `c1_qwen25vl_7b_ktvic_dev299-rand-k4-T1` | 0.00 | 299 | 48.84 | 2.23 | 0.000 | 0.000 | 16.21 |
| `c1_qwen25vl_7b_ktvic_dev299-rand-k4-T1` | 0.10 | 299 | 47.72 | 1.86 | 0.000 | 0.000 | 16.02 |
| `c1_qwen25vl_7b_ktvic_dev299-rand-k4-T1` | 0.20 | 299 | 46.22 | 0.56 | 0.000 | 0.000 | 15.85 |
| `c1_qwen25vl_7b_ktvic_dev299-rand-k4-T1` | 0.30 | 299 | 45.79 | 0.37 | 0.000 | 0.000 | 15.83 |
| `c1_qwen25vl_7b_ktvic_dev299-rand-k8-T1` | −∞ | 299 | 47.95 | 2.24 | 0.000 | 0.000 | 16.61 |
| `c1_qwen25vl_7b_ktvic_dev299-rand-k8-T1` | 0.00 | 299 | 47.42 | 2.79 | 0.000 | 0.000 | 16.48 |
| `c1_qwen25vl_7b_ktvic_dev299-rand-k8-T1` | 0.10 | 299 | 45.15 | 2.61 | 0.000 | 0.000 | 16.00 |
| `c1_qwen25vl_7b_ktvic_dev299-rand-k8-T1` | 0.20 | 299 | 44.10 | 1.50 | 0.000 | 0.000 | 15.62 |
| `c1_qwen25vl_7b_ktvic_dev299-rand-k8-T1` | 0.30 | 299 | 44.03 | 1.31 | 0.000 | 0.000 | 15.59 |
| `c1_qwen25vl_7b_ktvic_dev299-rand-k8-T1` | +∞ | 299 | 44.11 | 1.13 | 0.000 | 0.000 | 15.57 |
| `c1_qwen25vl_7b_ktvic_dev299-fix-k2-T1` | −∞ | 299 | 51.58 | 0.79 | 0.000 | 0.000 | 14.25 |
| `c1_qwen25vl_7b_ktvic_dev299-fix-k2-T1` | 0.00 | 299 | 51.57 | 0.79 | 0.000 | 0.000 | 14.22 |
| `c1_qwen25vl_7b_ktvic_dev299-fix-k2-T1` | 0.10 | 299 | 51.14 | 0.79 | 0.000 | 0.000 | 14.27 |
| `c1_qwen25vl_7b_ktvic_dev299-fix-k2-T1` | 0.20 | 299 | 49.50 | −0.58 | 0.000 | 0.000 | 14.08 |
| `c1_qwen25vl_7b_ktvic_dev299-fix-k2-T1` | 0.30 | 299 | 49.50 | −0.58 | 0.000 | 0.000 | 14.08 |
| `c1_qwen25vl_7b_ktvic_dev299-fix-k2-T1` | +∞ | 299 | 49.50 | −0.58 | 0.000 | 0.000 | 14.08 |
| `c1_qwen25vl_7b_ktvic_dev299-fix-k4-T1` | −∞ | 299 | 52.29 | 4.73 | 0.000 | 0.000 | 15.28 |
| `c1_qwen25vl_7b_ktvic_dev299-fix-k4-T1` | 0.00 | 299 | 51.95 | 4.56 | 0.000 | 0.000 | 15.25 |
| `c1_qwen25vl_7b_ktvic_dev299-fix-k4-T1` | 0.10 | 299 | 51.69 | 4.40 | 0.000 | 0.000 | 15.24 |
| `c1_qwen25vl_7b_ktvic_dev299-fix-k4-T1` | 0.20 | 299 | 50.58 | 2.86 | 0.000 | 0.000 | 15.13 |
| `c1_qwen25vl_7b_ktvic_dev299-fix-k4-T1` | 0.30 | 299 | 50.58 | 2.86 | 0.000 | 0.000 | 15.13 |
| `c1_qwen25vl_7b_ktvic_dev299-fix-k4-T1` | +∞ | 299 | 49.16 | 0.38 | 0.000 | 0.000 | 15.22 |
| `c1_qwen25vl_7b_ktvic_dev299-fix-k8-T1` | −∞ | 299 | 50.66 | 1.88 | 0.000 | 0.000 | 16.05 |
| `c1_qwen25vl_7b_ktvic_dev299-fix-k8-T1` | 0.00 | 299 | 50.40 | 2.25 | 0.000 | 0.000 | 15.84 |
| `c1_qwen25vl_7b_ktvic_dev299-fix-k8-T1` | 0.10 | 299 | 49.56 | 2.44 | 0.000 | 0.000 | 15.65 |
| `c1_qwen25vl_7b_ktvic_dev299-fix-k8-T1` | 0.20 | 299 | 46.99 | 0.38 | 0.000 | 0.000 | 15.31 |
| `c1_qwen25vl_7b_ktvic_dev299-fix-k8-T1` | 0.30 | 299 | 46.51 | 0.37 | 0.000 | 0.000 | 15.18 |
| `c1_qwen25vl_7b_ktvic_dev299-fix-k8-T1` | +∞ | 299 | 45.65 | −1.10 | 0.000 | 0.000 | 15.21 |
| `c1_internvl3_8b_ktvic_dev299-ret-k2-first-T1` | −∞ | 299 | 45.46 | 6.73 | 0.000 | 0.003 | 18.74 |
| `c1_internvl3_8b_ktvic_dev299-ret-k2-first-T1` | 0.00 | 299 | 45.96 | 6.94 | 0.000 | 0.003 | 18.44 |
| `c1_internvl3_8b_ktvic_dev299-ret-k2-first-T1` | 0.10 | 299 | 44.61 | 3.54 | 0.000 | 0.003 | 16.83 |
| `c1_internvl3_8b_ktvic_dev299-ret-k2-first-T1` | 0.20 | 299 | 44.20 | 3.36 | 0.000 | 0.003 | 16.64 |
| `c1_internvl3_8b_ktvic_dev299-ret-k2-first-T1` | 0.30 | 299 | 43.33 | 1.31 | 0.000 | 0.003 | 16.57 |
| `c1_internvl3_8b_ktvic_dev299-ret-k2-first-T1` | +∞ | 299 | 42.86 | 0.19 | 0.000 | 0.003 | 16.46 |
| `c1_internvl3_8b_ktvic_dev299-ret-k2-last-T1` | −∞ | 299 | 44.11 | 4.12 | 0.003 | 0.003 | 18.82 |
| `c1_internvl3_8b_ktvic_dev299-ret-k2-last-T1` | 0.00 | 299 | 44.00 | 4.13 | 0.003 | 0.003 | 18.43 |
| `c1_internvl3_8b_ktvic_dev299-ret-k2-last-T1` | 0.10 | 299 | 45.00 | 4.11 | 0.000 | 0.003 | 16.62 |
| `c1_internvl3_8b_ktvic_dev299-ret-k2-last-T1` | 0.20 | 299 | 44.23 | 3.94 | 0.000 | 0.003 | 16.52 |
| `c1_internvl3_8b_ktvic_dev299-ret-k2-last-T1` | 0.30 | 299 | 43.04 | 1.87 | 0.000 | 0.003 | 16.45 |
| `c1_internvl3_8b_ktvic_dev299-ret-k2-last-T1` | +∞ | 299 | 42.55 | 0.75 | 0.000 | 0.003 | 16.31 |
| `c1_internvl3_8b_ktvic_dev299-ret-k4-first-T1` | −∞ | 299 | 46.40 | 8.81 | 0.007 | 0.003 | 19.57 |
| `c1_internvl3_8b_ktvic_dev299-ret-k4-first-T1` | 0.00 | 299 | 45.96 | 8.05 | 0.007 | 0.003 | 19.13 |
| `c1_internvl3_8b_ktvic_dev299-ret-k4-first-T1` | 0.10 | 299 | 50.68 | 4.46 | 0.007 | 0.003 | 16.13 |
| `c1_internvl3_8b_ktvic_dev299-ret-k4-first-T1` | 0.20 | 299 | 49.76 | 4.07 | 0.007 | 0.003 | 16.05 |
| `c1_internvl3_8b_ktvic_dev299-ret-k4-first-T1` | 0.30 | 299 | 48.23 | 2.50 | 0.007 | 0.003 | 15.95 |
| `c1_internvl3_8b_ktvic_dev299-ret-k4-first-T1` | +∞ | 299 | 47.16 | 1.35 | 0.007 | 0.003 | 15.87 |
| `c1_internvl3_8b_ktvic_dev299-ret-k4-last-T1` | −∞ | 299 | 44.31 | 6.49 | 0.003 | 0.000 | 19.60 |
| `c1_internvl3_8b_ktvic_dev299-ret-k4-last-T1` | 0.00 | 299 | 44.47 | 6.51 | 0.003 | 0.000 | 19.23 |
| `c1_internvl3_8b_ktvic_dev299-ret-k4-last-T1` | 0.10 | 299 | 49.65 | 4.42 | 0.003 | 0.000 | 16.27 |
| `c1_internvl3_8b_ktvic_dev299-ret-k4-last-T1` | 0.20 | 299 | 48.60 | 4.04 | 0.003 | 0.000 | 16.20 |
| `c1_internvl3_8b_ktvic_dev299-ret-k4-last-T1` | 0.30 | 299 | 47.00 | 1.92 | 0.003 | 0.000 | 16.05 |
| `c1_internvl3_8b_ktvic_dev299-ret-k4-last-T1` | +∞ | 299 | 46.29 | 1.34 | 0.003 | 0.000 | 15.84 |
| `c1_internvl3_8b_ktvic_dev299-ret-k8-first-T1` | −∞ | 299 | 46.46 | 8.00 | 0.003 | 0.000 | 20.16 |
| `c1_internvl3_8b_ktvic_dev299-ret-k8-first-T1` | 0.00 | 299 | 46.45 | 8.03 | 0.003 | 0.000 | 19.58 |
| `c1_internvl3_8b_ktvic_dev299-ret-k8-first-T1` | 0.10 | 299 | 46.97 | 5.34 | 0.000 | 0.000 | 16.59 |
| `c1_internvl3_8b_ktvic_dev299-ret-k8-first-T1` | 0.20 | 299 | 46.40 | 4.39 | 0.000 | 0.000 | 16.46 |
| `c1_internvl3_8b_ktvic_dev299-ret-k8-first-T1` | 0.30 | 299 | 44.28 | 2.67 | 0.000 | 0.000 | 16.32 |
| `c1_internvl3_8b_ktvic_dev299-ret-k8-first-T1` | +∞ | 299 | 43.80 | 1.33 | 0.000 | 0.000 | 16.16 |
| `c1_internvl3_8b_ktvic_dev299-ret-k8-last-T1` | −∞ | 299 | 46.75 | 8.38 | 0.003 | 0.003 | 20.18 |
| `c1_internvl3_8b_ktvic_dev299-ret-k8-last-T1` | 0.00 | 299 | 46.39 | 8.03 | 0.003 | 0.003 | 19.70 |
| `c1_internvl3_8b_ktvic_dev299-ret-k8-last-T1` | 0.10 | 299 | 49.31 | 5.87 | 0.003 | 0.003 | 16.36 |
| `c1_internvl3_8b_ktvic_dev299-ret-k8-last-T1` | 0.20 | 299 | 49.02 | 5.30 | 0.003 | 0.003 | 16.17 |
| `c1_internvl3_8b_ktvic_dev299-ret-k8-last-T1` | 0.30 | 299 | 47.35 | 2.34 | 0.003 | 0.003 | 16.05 |
| `c1_internvl3_8b_ktvic_dev299-ret-k8-last-T1` | +∞ | 299 | 46.91 | 1.56 | 0.003 | 0.003 | 15.91 |
| `c1_internvl3_8b_ktvic_dev299-ret-k4-last-T2` | −∞ | 299 | 50.43 | 6.27 | 0.007 | 0.000 | 18.15 |
| `c1_internvl3_8b_ktvic_dev299-ret-k4-last-T2` | 0.00 | 299 | 49.69 | 7.48 | 0.003 | 0.000 | 17.83 |
| `c1_internvl3_8b_ktvic_dev299-ret-k4-last-T2` | 0.10 | 299 | 51.00 | 4.86 | 0.003 | 0.000 | 15.57 |
| `c1_internvl3_8b_ktvic_dev299-ret-k4-last-T2` | 0.20 | 299 | 50.45 | 4.47 | 0.003 | 0.000 | 15.43 |
| `c1_internvl3_8b_ktvic_dev299-ret-k4-last-T2` | 0.30 | 299 | 48.56 | 1.93 | 0.003 | 0.000 | 15.35 |
| `c1_internvl3_8b_ktvic_dev299-ret-k4-last-T2` | +∞ | 299 | 47.79 | 1.35 | 0.003 | 0.000 | 15.22 |
| `c1_internvl3_8b_ktvic_dev299-rand-k2-T1` | −∞ | 299 | 40.30 | 6.88 | 0.000 | 0.007 | 19.57 |
| `c1_internvl3_8b_ktvic_dev299-rand-k2-T1` | 0.00 | 299 | 41.46 | 6.68 | 0.000 | 0.007 | 19.36 |
| `c1_internvl3_8b_ktvic_dev299-rand-k2-T1` | 0.10 | 299 | 43.01 | 5.19 | 0.000 | 0.007 | 18.35 |
| `c1_internvl3_8b_ktvic_dev299-rand-k2-T1` | 0.20 | 299 | 42.79 | 5.19 | 0.000 | 0.007 | 18.30 |
| `c1_internvl3_8b_ktvic_dev299-rand-k2-T1` | 0.30 | 299 | 42.76 | 4.63 | 0.000 | 0.007 | 18.24 |
| `c1_internvl3_8b_ktvic_dev299-rand-k2-T1` | +∞ | 299 | 42.59 | 4.63 | 0.000 | 0.007 | 18.28 |
| `c1_internvl3_8b_ktvic_dev299-rand-k4-T1` | −∞ | 299 | 40.36 | 6.86 | 0.000 | 0.000 | 20.10 |
| `c1_internvl3_8b_ktvic_dev299-rand-k4-T1` | 0.00 | 299 | 41.50 | 7.04 | 0.000 | 0.000 | 19.86 |
| `c1_internvl3_8b_ktvic_dev299-rand-k4-T1` | 0.10 | 299 | 42.75 | 3.85 | 0.000 | 0.000 | 18.31 |
| `c1_internvl3_8b_ktvic_dev299-rand-k4-T1` | 0.20 | 299 | 42.52 | 3.67 | 0.000 | 0.000 | 18.24 |
| `c1_internvl3_8b_ktvic_dev299-rand-k4-T1` | 0.30 | 299 | 42.26 | 3.68 | 0.000 | 0.000 | 18.15 |
| `c1_internvl3_8b_ktvic_dev299-rand-k4-T1` | +∞ | 299 | 42.47 | 3.68 | 0.000 | 0.000 | 18.11 |
| `c1_internvl3_8b_ktvic_dev299-rand-k8-T1` | −∞ | 299 | 37.59 | 7.89 | 0.000 | 0.003 | 21.03 |
| `c1_internvl3_8b_ktvic_dev299-rand-k8-T1` | 0.00 | 299 | 38.13 | 7.92 | 0.000 | 0.003 | 20.55 |
| `c1_internvl3_8b_ktvic_dev299-rand-k8-T1` | 0.10 | 299 | 41.18 | 3.29 | 0.000 | 0.003 | 18.17 |
| `c1_internvl3_8b_ktvic_dev299-rand-k8-T1` | 0.20 | 299 | 41.02 | 3.11 | 0.000 | 0.003 | 18.07 |
| `c1_internvl3_8b_ktvic_dev299-rand-k8-T1` | 0.30 | 299 | 40.88 | 2.19 | 0.000 | 0.003 | 17.91 |
| `c1_internvl3_8b_ktvic_dev299-rand-k8-T1` | +∞ | 299 | 41.02 | 2.56 | 0.000 | 0.003 | 17.88 |
| `c1_internvl3_8b_ktvic_dev299-fix-k2-T1` | −∞ | 299 | 51.71 | 9.40 | 0.000 | 0.000 | 16.65 |
| `c1_internvl3_8b_ktvic_dev299-fix-k2-T1` | 0.00 | 299 | 51.86 | 9.60 | 0.000 | 0.000 | 16.62 |
| `c1_internvl3_8b_ktvic_dev299-fix-k2-T1` | 0.10 | 299 | 51.23 | 4.64 | 0.000 | 0.000 | 16.01 |
| `c1_internvl3_8b_ktvic_dev299-fix-k2-T1` | 0.20 | 299 | 51.23 | 4.64 | 0.000 | 0.000 | 16.01 |
| `c1_internvl3_8b_ktvic_dev299-fix-k2-T1` | 0.30 | 299 | 51.23 | 4.64 | 0.000 | 0.000 | 16.01 |
| `c1_internvl3_8b_ktvic_dev299-fix-k2-T1` | +∞ | 299 | 51.23 | 4.64 | 0.000 | 0.000 | 16.01 |
| `c1_internvl3_8b_ktvic_dev299-fix-k4-T1` | −∞ | 299 | 52.08 | 10.07 | 0.000 | 0.003 | 17.77 |
| `c1_internvl3_8b_ktvic_dev299-fix-k4-T1` | 0.00 | 299 | 51.81 | 9.91 | 0.000 | 0.003 | 17.72 |
| `c1_internvl3_8b_ktvic_dev299-fix-k4-T1` | 0.10 | 299 | 51.20 | 5.60 | 0.000 | 0.003 | 16.68 |
| `c1_internvl3_8b_ktvic_dev299-fix-k4-T1` | 0.20 | 299 | 51.20 | 5.60 | 0.000 | 0.003 | 16.68 |
| `c1_internvl3_8b_ktvic_dev299-fix-k4-T1` | 0.30 | 299 | 50.12 | 2.77 | 0.000 | 0.003 | 16.59 |
| `c1_internvl3_8b_ktvic_dev299-fix-k4-T1` | +∞ | 299 | 50.12 | 2.77 | 0.000 | 0.003 | 16.59 |
| `c1_internvl3_8b_ktvic_dev299-fix-k8-T1` | −∞ | 299 | 51.15 | 9.09 | 0.000 | 0.000 | 18.20 |
| `c1_internvl3_8b_ktvic_dev299-fix-k8-T1` | 0.00 | 299 | 50.97 | 9.29 | 0.000 | 0.000 | 18.11 |
| `c1_internvl3_8b_ktvic_dev299-fix-k8-T1` | 0.10 | 299 | 50.16 | 5.58 | 0.000 | 0.000 | 16.26 |
| `c1_internvl3_8b_ktvic_dev299-fix-k8-T1` | 0.20 | 299 | 50.16 | 5.58 | 0.000 | 0.000 | 16.26 |
| `c1_internvl3_8b_ktvic_dev299-fix-k8-T1` | 0.30 | 299 | 48.80 | 2.95 | 0.000 | 0.000 | 16.18 |
| `c1_internvl3_8b_ktvic_dev299-fix-k8-T1` | +∞ | 299 | 48.60 | 2.77 | 0.000 | 0.000 | 16.11 |
| `c1_internvl3_8b_ktvic_dev299-zs` | −∞ | 299 | 39.30 | 0.00 | n/a | 0.000 | 15.55 |
| `c1_internvl3_8b_ktvic_dev299-rand-k4-T2` | −∞ | 299 | 46.91 | 4.17 | 0.000 | 0.000 | 18.36 |
| `c1_internvl3_8b_ktvic_dev299-rand-k4-T2` | 0.00 | 299 | 47.66 | 4.54 | 0.000 | 0.000 | 18.24 |
| `c1_internvl3_8b_ktvic_dev299-rand-k4-T2` | 0.10 | 299 | 47.99 | 1.88 | 0.000 | 0.000 | 17.20 |
| `c1_internvl3_8b_ktvic_dev299-rand-k4-T2` | 0.20 | 299 | 47.14 | 1.88 | 0.000 | 0.000 | 17.15 |
| `c1_internvl3_8b_ktvic_dev299-rand-k4-T2` | 0.30 | 299 | 46.80 | 2.07 | 0.000 | 0.000 | 17.14 |
| `c1_internvl3_8b_ktvic_dev299-rand-k4-T2` | +∞ | 299 | 46.90 | 2.07 | 0.000 | 0.000 | 17.11 |
| `c1_internvl3_8b_ktvic_dev299-fix-k4-T2` | −∞ | 299 | 55.35 | 9.75 | 0.000 | 0.000 | 16.36 |
| `c1_internvl3_8b_ktvic_dev299-fix-k4-T2` | 0.00 | 299 | 54.89 | 9.77 | 0.000 | 0.000 | 16.36 |
| `c1_internvl3_8b_ktvic_dev299-fix-k4-T2` | 0.10 | 299 | 52.49 | 6.02 | 0.000 | 0.000 | 15.71 |
| `c1_internvl3_8b_ktvic_dev299-fix-k4-T2` | 0.20 | 299 | 52.49 | 6.02 | 0.000 | 0.000 | 15.71 |
| `c1_internvl3_8b_ktvic_dev299-fix-k4-T2` | 0.30 | 299 | 51.18 | 3.24 | 0.000 | 0.000 | 15.69 |
| `c1_internvl3_8b_ktvic_dev299-fix-k4-T2` | +∞ | 299 | 51.18 | 3.24 | 0.000 | 0.000 | 15.69 |
| `c1_qwen25vl_7b_ov_dev_a-ret-k8-first-T1` | −∞ | 911 | 40.45 | 4.18 | 0.018 | 0.004 | 18.50 |
| `c1_qwen25vl_7b_ov_dev_a-ret-k8-first-T1` | 0.00 | 911 | 38.05 | 3.60 | 0.010 | 0.004 | 17.86 |
| `c1_qwen25vl_7b_ov_dev_a-ret-k8-first-T1` | 0.10 | 911 | 33.36 | 2.76 | 0.008 | 0.004 | 16.43 |
| `c1_qwen25vl_7b_ov_dev_a-ret-k8-first-T1` | 0.20 | 911 | 31.33 | 1.58 | 0.005 | 0.004 | 15.90 |
| `c1_qwen25vl_7b_ov_dev_a-ret-k8-first-T1` | 0.30 | 911 | 31.05 | 1.31 | 0.005 | 0.004 | 15.91 |
| `c1_qwen25vl_7b_ov_dev_a-ret-k8-first-T1` | +∞ | 911 | 30.41 | 1.58 | 0.005 | 0.004 | 15.87 |
| `c1_qwen25vl_7b_ov_dev_a-rand-k8-T1` | −∞ | 911 | 32.44 | 3.17 | 0.001 | 0.003 | 17.28 |
| `c1_qwen25vl_7b_ov_dev_a-rand-k8-T1` | 0.00 | 911 | 31.45 | 2.71 | 0.001 | 0.003 | 16.89 |
| `c1_qwen25vl_7b_ov_dev_a-rand-k8-T1` | 0.10 | 911 | 29.62 | 1.10 | 0.001 | 0.003 | 16.05 |
| `c1_qwen25vl_7b_ov_dev_a-rand-k8-T1` | 0.20 | 911 | 28.68 | 0.14 | 0.001 | 0.003 | 15.78 |
| `c1_qwen25vl_7b_ov_dev_a-rand-k8-T1` | 0.30 | 911 | 28.51 | 0.00 | 0.001 | 0.003 | 15.70 |
| `c1_qwen25vl_7b_ov_dev_a-rand-k8-T1` | +∞ | 911 | 28.40 | 0.00 | 0.001 | 0.003 | 15.70 |
| `c1_qwen25vl_7b_ov_dev_a-fix-k8-T1` | −∞ | 911 | 31.74 | 1.58 | 0.000 | 0.001 | 17.50 |
| `c1_qwen25vl_7b_ov_dev_a-fix-k8-T1` | 0.00 | 911 | 31.41 | 1.65 | 0.000 | 0.001 | 17.33 |
| `c1_qwen25vl_7b_ov_dev_a-fix-k8-T1` | 0.10 | 911 | 29.54 | 2.12 | 0.000 | 0.001 | 16.36 |
| `c1_qwen25vl_7b_ov_dev_a-fix-k8-T1` | 0.20 | 911 | 28.61 | 1.26 | 0.000 | 0.001 | 15.94 |
| `c1_qwen25vl_7b_ov_dev_a-fix-k8-T1` | 0.30 | 911 | 28.27 | 1.06 | 0.000 | 0.001 | 15.98 |
| `c1_qwen25vl_7b_ov_dev_a-fix-k8-T1` | +∞ | 911 | 28.23 | 0.93 | 0.000 | 0.001 | 15.99 |
| `c1_internvl3_8b_ov_dev_a-ret-k4-last-T2` | −∞ | 911 | 39.38 | 2.81 | 0.002 | 0.001 | 19.49 |
| `c1_internvl3_8b_ov_dev_a-ret-k4-last-T2` | 0.00 | 911 | 38.63 | 3.64 | 0.002 | 0.001 | 18.95 |
| `c1_internvl3_8b_ov_dev_a-ret-k4-last-T2` | 0.10 | 911 | 33.43 | 1.18 | 0.002 | 0.001 | 16.99 |
| `c1_internvl3_8b_ov_dev_a-ret-k4-last-T2` | 0.20 | 911 | 33.31 | 1.04 | 0.002 | 0.001 | 16.94 |
| `c1_internvl3_8b_ov_dev_a-ret-k4-last-T2` | 0.30 | 911 | 32.38 | 0.49 | 0.002 | 0.001 | 16.76 |
| `c1_internvl3_8b_ov_dev_a-ret-k4-last-T2` | +∞ | 911 | 32.05 | 0.55 | 0.001 | 0.001 | 16.74 |
| `c1_internvl3_8b_ov_dev_a-rand-k4-T2` | −∞ | 911 | 35.95 | 3.20 | 0.000 | 0.001 | 19.19 |
| `c1_internvl3_8b_ov_dev_a-rand-k4-T2` | 0.00 | 911 | 35.47 | 3.00 | 0.000 | 0.001 | 18.95 |
| `c1_internvl3_8b_ov_dev_a-rand-k4-T2` | 0.10 | 911 | 33.27 | 1.85 | 0.000 | 0.001 | 17.78 |
| `c1_internvl3_8b_ov_dev_a-rand-k4-T2` | 0.20 | 911 | 33.03 | 2.13 | 0.000 | 0.001 | 17.71 |
| `c1_internvl3_8b_ov_dev_a-rand-k4-T2` | 0.30 | 911 | 32.83 | 2.13 | 0.000 | 0.001 | 17.62 |
| `c1_internvl3_8b_ov_dev_a-rand-k4-T2` | +∞ | 911 | 32.83 | 2.13 | 0.000 | 0.001 | 17.62 |
| `c1_internvl3_8b_ov_dev_a-fix-k4-T2` | −∞ | 911 | 31.97 | 0.26 | 0.000 | 0.002 | 22.04 |
| `c1_internvl3_8b_ov_dev_a-fix-k4-T2` | 0.00 | 911 | 31.75 | 0.07 | 0.000 | 0.002 | 21.69 |
| `c1_internvl3_8b_ov_dev_a-fix-k4-T2` | 0.10 | 911 | 29.90 | −1.13 | 0.000 | 0.002 | 19.70 |
| `c1_internvl3_8b_ov_dev_a-fix-k4-T2` | 0.20 | 911 | 29.90 | −1.13 | 0.000 | 0.002 | 19.70 |
| `c1_internvl3_8b_ov_dev_a-fix-k4-T2` | 0.30 | 911 | 29.76 | −1.00 | 0.000 | 0.002 | 19.53 |
| `c1_internvl3_8b_ov_dev_a-fix-k4-T2` | +∞ | 911 | 29.76 | −1.00 | 0.000 | 0.002 | 19.53 |
| `c1_qwen25vl_7b_ov_dev_a-zs` | −∞ | 911 | 22.65 | 0.00 | n/a | 0.002 | 16.41 |
| `c1_internvl3_8b_ov_dev_a-zs` | −∞ | 911 | 25.49 | 0.00 | n/a | 0.000 | 15.98 |

**Table S11. Stage B (OV-dev-B and XM-dev500), one look.**

| run | τ | n | CIDEr-D stripped | ΔP_cm vs zs | near-verbatim share | hit_max rate | mean syllables |
|------------------------------------------|---------|---------|---------|---------|---------|---------|---------|
| `c2_qwen25vl_7b_ov_dev_b-ret-k8-first-T1` | −∞ | 925 | 40.63 | 5.26 | 0.026 | 0.003 | 18.23 |
| `c2_qwen25vl_7b_ov_dev_b-ret-k8-first-T1` | 0.00 | 925 | 38.05 | 5.42 | 0.016 | 0.003 | 17.53 |
| `c2_qwen25vl_7b_ov_dev_b-ret-k8-first-T1` | 0.10 | 925 | 32.91 | 2.80 | 0.015 | 0.003 | 16.42 |
| `c2_qwen25vl_7b_ov_dev_b-ret-k8-first-T1` | 0.20 | 925 | 30.27 | 1.15 | 0.012 | 0.003 | 15.92 |
| `c2_qwen25vl_7b_ov_dev_b-ret-k8-first-T1` | 0.30 | 925 | 29.80 | 1.00 | 0.012 | 0.003 | 15.97 |
| `c2_qwen25vl_7b_ov_dev_b-ret-k8-first-T1` | +∞ | 925 | 28.86 | 0.78 | 0.012 | 0.003 | 15.96 |
| `c2_qwen25vl_7b_ov_dev_b-rand-k8-T1` | −∞ | 925 | 30.97 | 2.32 | 0.001 | 0.003 | 17.46 |
| `c2_qwen25vl_7b_ov_dev_b-rand-k8-T1` | +∞ | 925 | 27.36 | 0.64 | 0.000 | 0.003 | 15.83 |
| `c2_qwen25vl_7b_ov_dev_b-fix-k8-T1` | −∞ | 925 | 30.38 | 4.05 | 0.000 | 0.003 | 17.84 |
| `c2_qwen25vl_7b_ov_dev_b-fix-k8-T1` | +∞ | 925 | 26.45 | −0.21 | 0.000 | 0.003 | 15.81 |
| `c2_internvl3_8b_ov_dev_b-ret-k4-last-T2` | −∞ | 925 | 38.82 | 4.76 | 0.003 | 0.001 | 19.25 |
| `c2_internvl3_8b_ov_dev_b-ret-k4-last-T2` | 0.00 | 925 | 38.01 | 4.61 | 0.002 | 0.001 | 18.90 |
| `c2_internvl3_8b_ov_dev_b-ret-k4-last-T2` | 0.10 | 925 | 33.39 | 1.28 | 0.000 | 0.001 | 16.62 |
| `c2_internvl3_8b_ov_dev_b-ret-k4-last-T2` | 0.20 | 925 | 32.99 | 0.99 | 0.000 | 0.001 | 16.51 |
| `c2_internvl3_8b_ov_dev_b-ret-k4-last-T2` | 0.30 | 925 | 32.78 | 0.64 | 0.000 | 0.001 | 16.42 |
| `c2_internvl3_8b_ov_dev_b-ret-k4-last-T2` | +∞ | 925 | 32.32 | 0.64 | 0.000 | 0.001 | 16.40 |
| `c2_internvl3_8b_ov_dev_b-rand-k4-T2` | −∞ | 925 | 33.47 | 2.48 | 0.000 | 0.002 | 19.23 |
| `c2_internvl3_8b_ov_dev_b-rand-k4-T2` | 0.00 | 925 | 33.26 | 2.42 | 0.000 | 0.002 | 18.95 |
| `c2_internvl3_8b_ov_dev_b-rand-k4-T2` | 0.10 | 925 | 30.98 | 0.49 | 0.000 | 0.002 | 17.73 |
| `c2_internvl3_8b_ov_dev_b-rand-k4-T2` | 0.20 | 925 | 30.84 | 0.42 | 0.000 | 0.002 | 17.70 |
| `c2_internvl3_8b_ov_dev_b-rand-k4-T2` | 0.30 | 925 | 30.88 | 0.42 | 0.000 | 0.002 | 17.69 |
| `c2_internvl3_8b_ov_dev_b-rand-k4-T2` | +∞ | 925 | 30.86 | 0.42 | 0.000 | 0.002 | 17.68 |
| `c2_internvl3_8b_ov_dev_b-fix-k4-T2` | −∞ | 925 | 32.80 | 3.74 | 0.000 | 0.003 | 20.90 |
| `c2_internvl3_8b_ov_dev_b-fix-k4-T2` | 0.00 | 925 | 32.69 | 3.74 | 0.000 | 0.003 | 20.78 |
| `c2_internvl3_8b_ov_dev_b-fix-k4-T2` | 0.10 | 925 | 31.74 | 2.06 | 0.000 | 0.003 | 19.35 |
| `c2_internvl3_8b_ov_dev_b-fix-k4-T2` | 0.20 | 925 | 31.74 | 2.06 | 0.000 | 0.003 | 19.35 |
| `c2_internvl3_8b_ov_dev_b-fix-k4-T2` | 0.30 | 925 | 31.49 | 1.99 | 0.000 | 0.003 | 19.12 |
| `c2_internvl3_8b_ov_dev_b-fix-k4-T2` | +∞ | 925 | 31.49 | 1.99 | 0.000 | 0.003 | 19.12 |
| `c2_qwen25vl_7b_ov_dev_b-zs` | −∞ | 925 | 20.59 | 0.00 | n/a | 0.003 | 15.96 |
| `c2_internvl3_8b_ov_dev_b-zs` | −∞ | 925 | 23.55 | 0.00 | n/a | 0.002 | 15.70 |
| `c2_nn_ov_dev_b-top1` | −∞ | 925 | 23.28 | n/a | n/a | n/a | n/a |
| `c2_nn_ov_dev_b-cons-k4` | −∞ | 925 | 26.49 | n/a | n/a | n/a | n/a |
| `c2_nn_ov_dev_b-cons-k8` | −∞ | 925 | 29.52 | n/a | n/a | n/a | n/a |
| `c2_qwen25vl_7b_xm_dev500-ret-k8-first-T1` | −∞ | 500 | 60.01 | −0.47 | 0.002 | 0.002 | 14.84 |
| `c2_qwen25vl_7b_xm_dev500-ret-k8-first-T1` | 0.00 | 500 | 59.54 | 0.78 | 0.002 | 0.002 | 14.73 |
| `c2_qwen25vl_7b_xm_dev500-ret-k8-first-T1` | 0.10 | 500 | 57.50 | 0.79 | 0.002 | 0.002 | 14.13 |
| `c2_qwen25vl_7b_xm_dev500-ret-k8-first-T1` | 0.20 | 500 | 55.86 | 1.11 | 0.002 | 0.002 | 14.00 |
| `c2_qwen25vl_7b_xm_dev500-ret-k8-first-T1` | 0.30 | 500 | 55.39 | 1.41 | 0.002 | 0.002 | 13.88 |
| `c2_qwen25vl_7b_xm_dev500-ret-k8-first-T1` | +∞ | 500 | 54.52 | 1.09 | 0.002 | 0.002 | 13.87 |
| `c2_qwen25vl_7b_xm_dev500-rand-k8-T1` | −∞ | 500 | 55.57 | −1.56 | 0.000 | 0.000 | 13.93 |
| `c2_qwen25vl_7b_xm_dev500-rand-k8-T1` | +∞ | 500 | 53.62 | −1.57 | 0.000 | 0.000 | 13.31 |
| `c2_qwen25vl_7b_xm_dev500-fix-k8-T1` | −∞ | 500 | 56.76 | 0.16 | 0.000 | 0.000 | 13.41 |
| `c2_qwen25vl_7b_xm_dev500-fix-k8-T1` | +∞ | 500 | 55.56 | 1.11 | 0.000 | 0.000 | 13.21 |
| `c2_internvl3_8b_xm_dev500-ret-k4-last-T2` | −∞ | 500 | 61.13 | 1.43 | 0.000 | 0.000 | 16.65 |
| `c2_internvl3_8b_xm_dev500-ret-k4-last-T2` | 0.00 | 500 | 60.03 | 1.12 | 0.000 | 0.000 | 16.31 |
| `c2_internvl3_8b_xm_dev500-ret-k4-last-T2` | 0.10 | 500 | 56.05 | 0.00 | 0.000 | 0.000 | 15.13 |
| `c2_internvl3_8b_xm_dev500-ret-k4-last-T2` | 0.20 | 500 | 56.15 | 0.16 | 0.000 | 0.000 | 15.07 |
| `c2_internvl3_8b_xm_dev500-ret-k4-last-T2` | 0.30 | 500 | 56.10 | 0.16 | 0.000 | 0.000 | 15.06 |
| `c2_internvl3_8b_xm_dev500-ret-k4-last-T2` | +∞ | 500 | 55.19 | 0.33 | 0.000 | 0.000 | 14.96 |
| `c2_internvl3_8b_xm_dev500-rand-k4-T2` | −∞ | 500 | 59.59 | 1.42 | 0.000 | 0.000 | 16.27 |
| `c2_internvl3_8b_xm_dev500-rand-k4-T2` | 0.00 | 500 | 58.65 | 1.57 | 0.000 | 0.000 | 16.09 |
| `c2_internvl3_8b_xm_dev500-rand-k4-T2` | 0.10 | 500 | 57.57 | 1.11 | 0.000 | 0.000 | 15.63 |
| `c2_internvl3_8b_xm_dev500-rand-k4-T2` | 0.20 | 500 | 57.56 | 1.27 | 0.000 | 0.000 | 15.61 |
| `c2_internvl3_8b_xm_dev500-rand-k4-T2` | 0.30 | 500 | 57.56 | 1.27 | 0.000 | 0.000 | 15.61 |
| `c2_internvl3_8b_xm_dev500-rand-k4-T2` | +∞ | 500 | 57.44 | 1.27 | 0.000 | 0.000 | 15.60 |
| `c2_internvl3_8b_xm_dev500-fix-k4-T2` | −∞ | 500 | 59.63 | 1.44 | 0.000 | 0.000 | 16.45 |
| `c2_internvl3_8b_xm_dev500-fix-k4-T2` | 0.00 | 500 | 58.81 | 1.77 | 0.000 | 0.000 | 16.27 |
| `c2_internvl3_8b_xm_dev500-fix-k4-T2` | 0.10 | 500 | 58.48 | 2.44 | 0.000 | 0.000 | 15.93 |
| `c2_internvl3_8b_xm_dev500-fix-k4-T2` | 0.20 | 500 | 58.50 | 2.61 | 0.000 | 0.000 | 15.87 |
| `c2_internvl3_8b_xm_dev500-fix-k4-T2` | 0.30 | 500 | 58.50 | 2.61 | 0.000 | 0.000 | 15.87 |
| `c2_internvl3_8b_xm_dev500-fix-k4-T2` | +∞ | 500 | 58.02 | 2.45 | 0.000 | 0.000 | 15.82 |
| `c2_qwen25vl_7b_xm_dev500-zs` | −∞ | 500 | 45.42 | 0.00 | n/a | 0.000 | 14.34 |
| `c2_internvl3_8b_xm_dev500-zs` | −∞ | 500 | 46.50 | 0.00 | n/a | 0.000 | 13.47 |
| `c2_nn_xm_dev500-top1` | −∞ | 500 | 14.68 | n/a | n/a | n/a | n/a |
| `c2_nn_xm_dev500-cons-k4` | −∞ | 500 | 16.01 | n/a | n/a | n/a | n/a |
| `c2_nn_xm_dev500-cons-k8` | −∞ | 500 | 17.10 | n/a | n/a | n/a | n/a |
| `c2_qwen25vl_7b_ov_dev_b-blind-k8-first-T1` | −∞ | 925 | 24.86 | −19.78 | 0.083 | 0.000 | 16.80 |
| `c2_qwen25vl_7b_ov_dev_b-blind-k8-first-T1` | +∞ | 925 | 23.19 | −6.11 | 0.018 | 0.000 | 15.11 |
| `c2_internvl3_8b_ov_dev_b-blind-k4-last-T2` | −∞ | 925 | 22.08 | −18.38 | 0.022 | 0.000 | 17.36 |
| `c2_internvl3_8b_ov_dev_b-blind-k4-last-T2` | +∞ | 925 | 23.03 | −7.52 | 0.002 | 0.000 | 15.14 |
| `c2_qwen25vl_7b_xm_dev500-blind-k8-first-T1` | −∞ | 500 | 13.10 | −38.24 | 0.054 | 0.000 | 15.15 |
| `c2_qwen25vl_7b_xm_dev500-blind-k8-first-T1` | +∞ | 500 | 32.63 | −13.47 | 0.008 | 0.000 | 13.90 |
| `c2_internvl3_8b_xm_dev500-blind-k4-last-T2` | −∞ | 500 | 14.32 | −33.87 | 0.014 | 0.000 | 15.70 |
| `c2_internvl3_8b_xm_dev500-blind-k4-last-T2` | +∞ | 500 | 28.82 | −16.20 | 0.004 | 0.000 | 13.38 |

### Rows not registered for any claim

**Table S12. Test rows that the unchanged scorer wrote but no rule registered: InternVL3 at τ ∈ {0.00, 0.20, 0.30, +∞}, Qwen2.5-VL at τ = +∞, and InternVL3's verifier AUROC.** Not registered for any claim. No decision step reads them and the text makes no claim from them.

| scored set | run | τ | CIDEr-D stripped | ΔP_cm vs zs / note |
|---|---|---|---|---|
| 1941 | `ct_qwen25vl_7b_ov_test-ret-k8-first-T1` | +∞ | 28.15 | 0.83 |
| 1941 | `ct_qwen25vl_7b_ov_test-rand-k8-T1` | +∞ | 26.94 | 0.36 |
| 1941 | `ct_qwen25vl_7b_ov_test-fix-k8-T1` | +∞ | 26.59 | 1.05 |
| 1941 | `ct_internvl3_8b_ov_test-ret-k4-last-T2` | 0.00 | 38.61 | 5.86 |
| 1941 | `ct_internvl3_8b_ov_test-ret-k4-last-T2` | 0.20 | 33.25 | 1.60 |
| 1941 | `ct_internvl3_8b_ov_test-ret-k4-last-T2` | 0.30 | 32.76 | 1.11 |
| 1941 | `ct_internvl3_8b_ov_test-ret-k4-last-T2` | +∞ | 32.40 | 0.88 |
| 1941 | `ct_internvl3_8b_ov_test-rand-k4-T2` | 0.00 | 35.27 | 3.47 |
| 1941 | `ct_internvl3_8b_ov_test-rand-k4-T2` | 0.20 | 32.85 | 1.40 |
| 1941 | `ct_internvl3_8b_ov_test-rand-k4-T2` | 0.30 | 32.78 | 1.37 |
| 1941 | `ct_internvl3_8b_ov_test-rand-k4-T2` | +∞ | 32.79 | 1.34 |
| 1941 | `ct_internvl3_8b_ov_test-fix-k4-T2` | 0.00 | 37.36 | 5.70 |
| 1941 | `ct_internvl3_8b_ov_test-fix-k4-T2` | 0.20 | 33.02 | 1.68 |
| 1941 | `ct_internvl3_8b_ov_test-fix-k4-T2` | 0.30 | 33.01 | 1.72 |
| 1941 | `ct_internvl3_8b_ov_test-fix-k4-T2` | +∞ | 32.78 | 1.40 |
| 1941 | `ct_internvl3_8b_ov_test-ret-k4-last-T2` | −∞ (verifier AUROC of s) | 0.560 | items 1,531 |
| 1941 | `ct_internvl3_8b_ov_test-rand-k4-T2` | −∞ (verifier AUROC of s) | 0.591 | items 654 |
| 1941 | `ct_internvl3_8b_ov_test-fix-k4-T2` | −∞ (verifier AUROC of s) | 0.549 | items 1,049 |
| 2001 | `ct_qwen25vl_7b_ov_test-ret-k8-first-T1` | +∞ | 28.14 | 0.86 |
| 2001 | `ct_qwen25vl_7b_ov_test-rand-k8-T1` | +∞ | 26.97 | 0.44 |
| 2001 | `ct_qwen25vl_7b_ov_test-fix-k8-T1` | +∞ | 26.48 | 1.07 |
| 2001 | `ct_internvl3_8b_ov_test-ret-k4-last-T2` | 0.00 | 38.57 | 5.55 |
| 2001 | `ct_internvl3_8b_ov_test-ret-k4-last-T2` | 0.20 | 33.27 | 1.32 |
| 2001 | `ct_internvl3_8b_ov_test-ret-k4-last-T2` | 0.30 | 32.77 | 0.91 |
| 2001 | `ct_internvl3_8b_ov_test-ret-k4-last-T2` | +∞ | 32.42 | 0.66 |
| 2001 | `ct_internvl3_8b_ov_test-rand-k4-T2` | 0.00 | 35.28 | 3.12 |
| 2001 | `ct_internvl3_8b_ov_test-rand-k4-T2` | 0.20 | 32.90 | 1.16 |
| 2001 | `ct_internvl3_8b_ov_test-rand-k4-T2` | 0.30 | 32.80 | 1.13 |
| 2001 | `ct_internvl3_8b_ov_test-rand-k4-T2` | +∞ | 32.80 | 1.10 |
| 2001 | `ct_internvl3_8b_ov_test-fix-k4-T2` | 0.00 | 37.28 | 5.36 |
| 2001 | `ct_internvl3_8b_ov_test-fix-k4-T2` | 0.20 | 32.99 | 1.56 |
| 2001 | `ct_internvl3_8b_ov_test-fix-k4-T2` | 0.30 | 32.98 | 1.59 |
| 2001 | `ct_internvl3_8b_ov_test-fix-k4-T2` | +∞ | 32.75 | 1.32 |
| 2001 | `ct_internvl3_8b_ov_test-ret-k4-last-T2` | −∞ (verifier AUROC of s) | 0.562 | items 1,576 |
| 2001 | `ct_internvl3_8b_ov_test-rand-k4-T2` | −∞ (verifier AUROC of s) | 0.592 | items 676 |
| 2001 | `ct_internvl3_8b_ov_test-fix-k4-T2` | −∞ (verifier AUROC of s) | 0.545 | items 1,077 |
| 2500 | `ct_qwen25vl_7b_xm_test2500-ret-k8-first-T1` | +∞ | 52.27 | 0.06 |
| 2500 | `ct_qwen25vl_7b_xm_test2500-rand-k8-T1` | +∞ | 52.15 | 0.55 |
| 2500 | `ct_qwen25vl_7b_xm_test2500-fix-k8-T1` | +∞ | 50.26 | −0.22 |
| 2500 | `ct_internvl3_8b_xm_test2500-ret-k4-last-T2` | 0.00 | 55.65 | 0.88 |
| 2500 | `ct_internvl3_8b_xm_test2500-ret-k4-last-T2` | 0.20 | 52.80 | 0.22 |
| 2500 | `ct_internvl3_8b_xm_test2500-ret-k4-last-T2` | 0.30 | 52.52 | 0.54 |
| 2500 | `ct_internvl3_8b_xm_test2500-ret-k4-last-T2` | +∞ | 52.05 | 0.25 |
| 2500 | `ct_internvl3_8b_xm_test2500-rand-k4-T2` | 0.00 | 55.69 | 1.57 |
| 2500 | `ct_internvl3_8b_xm_test2500-rand-k4-T2` | 0.20 | 54.49 | 0.94 |
| 2500 | `ct_internvl3_8b_xm_test2500-rand-k4-T2` | 0.30 | 54.49 | 0.91 |
| 2500 | `ct_internvl3_8b_xm_test2500-rand-k4-T2` | +∞ | 54.50 | 0.91 |
| 2500 | `ct_internvl3_8b_xm_test2500-fix-k4-T2` | 0.00 | 54.68 | 1.30 |
| 2500 | `ct_internvl3_8b_xm_test2500-fix-k4-T2` | 0.20 | 53.65 | 0.74 |
| 2500 | `ct_internvl3_8b_xm_test2500-fix-k4-T2` | 0.30 | 53.65 | 0.74 |
| 2500 | `ct_internvl3_8b_xm_test2500-fix-k4-T2` | +∞ | 53.57 | 0.78 |
| 2500 | `ct_internvl3_8b_xm_test2500-ret-k4-last-T2` | −∞ (verifier AUROC of s) | 0.552 | items 1,063 |
| 2500 | `ct_internvl3_8b_xm_test2500-rand-k4-T2` | −∞ (verifier AUROC of s) | 0.614 | items 387 |
| 2500 | `ct_internvl3_8b_xm_test2500-fix-k4-T2` | −∞ (verifier AUROC of s) | 0.631 | items 274 |
| 2392 | `ct_qwen25vl_7b_xm_test2500-ret-k8-first-T1` | +∞ | 52.03 | 0.00 |
| 2392 | `ct_qwen25vl_7b_xm_test2500-rand-k8-T1` | +∞ | 51.83 | 0.51 |
| 2392 | `ct_qwen25vl_7b_xm_test2500-fix-k8-T1` | +∞ | 49.77 | −0.26 |
| 2392 | `ct_internvl3_8b_xm_test2500-ret-k4-last-T2` | 0.00 | 55.58 | 0.92 |
| 2392 | `ct_internvl3_8b_xm_test2500-ret-k4-last-T2` | 0.20 | 52.70 | 0.23 |
| 2392 | `ct_internvl3_8b_xm_test2500-ret-k4-last-T2` | 0.30 | 52.41 | 0.53 |
| 2392 | `ct_internvl3_8b_xm_test2500-ret-k4-last-T2` | +∞ | 51.92 | 0.23 |
| 2392 | `ct_internvl3_8b_xm_test2500-rand-k4-T2` | 0.00 | 55.57 | 1.50 |
| 2392 | `ct_internvl3_8b_xm_test2500-rand-k4-T2` | 0.20 | 54.37 | 0.89 |
| 2392 | `ct_internvl3_8b_xm_test2500-rand-k4-T2` | 0.30 | 54.37 | 0.85 |
| 2392 | `ct_internvl3_8b_xm_test2500-rand-k4-T2` | +∞ | 54.38 | 0.85 |
| 2392 | `ct_internvl3_8b_xm_test2500-fix-k4-T2` | 0.00 | 54.51 | 1.36 |
| 2392 | `ct_internvl3_8b_xm_test2500-fix-k4-T2` | 0.20 | 53.56 | 0.81 |
| 2392 | `ct_internvl3_8b_xm_test2500-fix-k4-T2` | 0.30 | 53.56 | 0.81 |
| 2392 | `ct_internvl3_8b_xm_test2500-fix-k4-T2` | +∞ | 53.47 | 0.84 |
| 2392 | `ct_internvl3_8b_xm_test2500-ret-k4-last-T2` | −∞ (verifier AUROC of s) | 0.555 | items 1,029 |
| 2392 | `ct_internvl3_8b_xm_test2500-rand-k4-T2` | −∞ (verifier AUROC of s) | 0.611 | items 379 |
| 2392 | `ct_internvl3_8b_xm_test2500-fix-k4-T2` | −∞ (verifier AUROC of s) | 0.632 | items 263 |

### English arm: every registered and reported row

**Table S13. English-arm rows on the three scored sets (PTB CIDEr-D, paired 95% bootstrap CIs, B = 2,000; InternVL3 at its frozen τ = 0.10 unless marked).** Per-backbone, `zs` and length rows are reported, non-gating. Length is the mean number of PTB tokens.

| scored set | backbone | `ret` − `rand` | `ret` − `zs` | `rand` − `zs` | length `ret` | length `rand` | length gap |
|---|---|---|---|---|---|---|---|
| COCO Karpathy test (5,000) | Qwen2.5-VL | +7.80 [6.40, 9.17] | +37.30 [35.80, 38.75] | +29.50 [28.27, 30.79] | 11.37 | 11.16 | 0.019 |
| COCO Karpathy test (5,000) | InternVL3 | −1.64 [−2.79, −0.49] | +6.49 [5.27, 7.70] | +8.13 [7.03, 9.21] | 12.47 | 12.72 | 0.019 |
| COCO Karpathy test (5,000) | pooled | +3.08 [2.08, 4.03] | +21.89 [20.90, 22.88] | | | | |
| COCO Karpathy test (5,000) | InternVL3, τ = −∞ (registered secondary) | −1.05 [−2.22, 0.08], not detected | | | | | |
| NoCaps val (4,500) | Qwen2.5-VL | +2.83 [1.69, 3.98] | +32.67 [31.37, 33.93] | +29.84 [28.56, 31.02] | 11.19 | 11.10 | 0.008 |
| NoCaps val (4,500) | InternVL3 | +0.62 [−0.37, 1.62] | +5.43 [4.37, 6.48] | +4.81 [3.86, 5.77] | 12.58 | 12.81 | 0.018 |
| NoCaps val (4,500) | pooled | +1.73 [0.94, 2.50] | +19.05 [18.18, 19.95] | | | | |
| NoCaps val (4,500) | InternVL3, τ = −∞ (registered secondary) | +1.00 [−0.01, 2.01], not detected | | | | | |
| NoCaps val without the earlier 1,000 (3,500) | Qwen2.5-VL | +2.35 [0.96, 3.73] | +32.44 [30.88, 33.95] | +30.09 [28.67, 31.47] | 11.17 | 11.09 | 0.007 |
| NoCaps val without the earlier 1,000 (3,500) | InternVL3 | +0.89 [−0.34, 2.00] | +5.64 [4.47, 6.84] | +4.74 [3.65, 5.89] | 12.55 | 12.78 | 0.018 |
| NoCaps val without the earlier 1,000 (3,500) | pooled | +1.62 [0.66, 2.52] | +19.04 [18.00, 20.05] | | | | |
| NoCaps val without the earlier 1,000 (3,500) | InternVL3, τ = −∞ (registered secondary) | +1.09 [−0.12, 2.21], not detected | | | | | |

Verdicts: P1-EN PASS (rule L does not fire); S-NC FAIL; 3,500-image sensitivity FAIL; the claim that the gain transfers to NoCaps val is not made.

**InternVL3 deletion-step counts, per run (all images of the set; identical for the 4,500 and 3,500 scored sets).** Neighbour-only and rejected are object items; deleted and fallback are captions.

| set | arm | neighbour-only | rejected | deleted | fallback |
|---|---|---|---|---|---|
| COCO Karpathy test | `ret` | 524 | 302 | 110 | 182 |
| COCO Karpathy test | `rand` | 123 | 112 | 39 | 73 |
| NoCaps val | `ret` | 304 | 234 | 72 | 154 |
| NoCaps val | `rand` | 110 | 107 | 30 | 76 |

**NoCaps val by domain (pooled `ret` − `rand`).** in-domain (n = 417) +4.64 [1.85, 7.36]; near-domain (n = 2,670) +1.96 [0.85, 2.99]; out-domain (n = 1,413) +0.43 [−0.85, 1.73].

Decision files: `decide_coco_test.json` (head ed1e6c41, 2026-10-27T10:30:58Z), `decide_nocaps_val.json` (head f8cccb68, 2026-10-27T17:33:57Z); ledger sha256 prefixes 58074daee2ff, c02f2b8f7636, fabf5a82b586.

### Mechanism on the development set (OV-dev-B), dated 2026-10-27

**Table S14. Every row of the development-ablation decision file. Label: "development set B mechanism, non-confirmatory". OV-dev-B, 925 images, stripped CIDEr-D.** Not a test result; no row enters the abstract or the contributions.

Outcomes: AB-M HOLDS (all three parts true); AB-K P-K HOLDS (all three parts true; label "shaped by stage-A dev299 selection"); AB-τ HOLDS (all three parts true); section-6 condition True.

*AB-M (memory size; shared `rand` from the full memory).*

| memory | clusters | composition (OpenViIC only / both / KTVIC only) | mean top-1 cosine | pooled | Qwen2.5-VL | Qwen2.5-VL src share | InternVL3 τ 0.10 | InternVL3 src share | InternVL3 τ −∞ |
|---|---|---|---|---|---|---|---|---|---|
| 10% | 819 | 600 / 212 / 7 | 0.772 | +3.21 [1.87, 4.54] | +5.20 [3.30, 7.03] | 0.992 | +1.21 [−0.45, 2.88] | 0.993 | +3.71 [1.94, 5.53] |
| 30% | 2,457 | 1,805 / 643 / 9 | 0.796 | +4.24 [2.90, 5.58] | +7.66 [5.76, 9.44] | 0.996 | +0.82 [−0.97, 2.62] | 0.997 | +3.61 [1.73, 5.50] |
| 100% | 8,190 | 6,017 / 2,133 / 40 | 0.821 | +6.04 [4.54, 7.58] | +9.67 [7.68, 11.72] | 0.995 | +2.41 [0.57, 4.26] | 0.995 | +5.36 [3.53, 7.12] |
| 10% − 100% | | | | −2.83 [−4.18, −1.58] | −4.47 [−6.55, −2.56] | | −1.20 [−2.94, 0.35] | | |

*AB-K (number of examples; 100% memory).*

| backbone | k | `ret` − `rand` | syllables `ret` | syllables `rand` | ends in punctuation `ret` / `rand` | top-3 opening share `ret` / `rand` | 4-gram copy share | near-verbatim share |
|---|---|---|---|---|---|---|---|---|
| Qwen2.5-VL | 2 | +6.41 [4.46, 8.49] | 16.65 | 15.98 | 0.992 / 0.994 | 0.285 / 0.306 | 0.306 | 0.009 |
| Qwen2.5-VL | 4 | +7.11 [5.23, 9.04] | 17.49 | 16.70 | 0.994 / 0.999 | 0.312 / 0.323 | 0.356 | 0.015 |
| Qwen2.5-VL | 8 | +9.67 [7.68, 11.72] | 18.23 | 17.46 | 0.994 / 0.997 | 0.337 / 0.365 | 0.402 | 0.026 |
| InternVL3 | 2 | +1.93 [0.16, 3.63] | 16.48 | 17.28 | 0.935 / 0.918 | 0.138 / 0.178 | 0.239 | 0.003 |
| InternVL3 | 4 | +2.41 [0.57, 4.26] | 16.62 | 17.73 | 0.881 / 0.864 | 0.129 / 0.178 | 0.262 | 0.000 |
| InternVL3 | 8 | +2.19 [0.73, 3.76] | 16.79 | 17.65 | 0.869 / 0.874 | 0.129 / 0.178 | 0.272 | 0.005 |

P-K difference, Qwen2.5-VL k = 8 minus k = 2: +3.26 [0.98, 5.63].

*AB-τ (InternVL3; stage-B decodes re-scored on CPU).* Cost = mean(arm at τ − arm at −∞). NO rate = neighbour-only classes / all matched classes; NP = neighbour-only precision against reference gold over Σm mentions.

| τ | `ret` − `rand` | cost `ret` | cost `rand` | arm | NO rate | rejected per image | deleted share | fallback share | NP (Σm) |
|---|---|---|---|---|---|---|---|---|---|
| −∞ | +5.36 [3.53, 7.12] |  |  | `ret` | 0.340 | 0.000 | 0.000 | 0.000 | 77.31 (714) |
|  |  |  |  | `rand` | 0.152 | 0.000 | 0.000 | 0.000 | 73.50 (317) |
| 0.00 | +4.75 [2.96, 6.62] | −0.81 [−1.39, −0.32] | −0.21 [−0.50, 0.07] | `ret` | 0.340 | 0.084 | 0.019 | 0.063 | 79.73 (602) |
|  |  |  |  | `rand` | 0.152 | 0.052 | 0.017 | 0.034 | 81.50 (254) |
| 0.10 | +2.41 [0.57, 4.26] | −5.43 [−6.76, −4.08] | −2.48 [−3.44, −1.51] | `ret` | 0.340 | 0.621 | 0.139 | 0.344 | 83.75 (80) |
|  |  |  |  | `rand` | 0.152 | 0.312 | 0.088 | 0.182 | 69.23 (13) |
| 0.20 | +2.15 [0.35, 3.97] | −5.83 [−7.19, −4.49] | −2.63 [−3.61, −1.63] | `ret` | 0.340 | 0.677 | 0.145 | 0.362 | 85.42 (48) |
|  |  |  |  | `rand` | 0.152 | 0.328 | 0.090 | 0.187 | 75.00 (4) |
| 0.30 | +1.90 [0.07, 3.74] | −6.04 [−7.44, −4.72] | −2.59 [−3.58, −1.59] | `ret` | 0.340 | 0.734 | 0.147 | 0.383 | 68.75 (16) |
|  |  |  |  | `rand` | 0.152 | 0.336 | 0.094 | 0.187 | n/a (0) |
| +∞ | +1.45 [−0.35, 3.25] |  |  | `ret` | 0.340 | 0.781 | 0.149 | 0.389 | n/a (0) |
|  |  |  |  | `rand` | 0.152 | 0.343 | 0.095 | 0.186 | n/a (0) |

*Style check (`rand` − `zs`, 100% memory; post-hoc remark only).* Qwen2.5-VL +10.38 [8.71, 12.00]; InternVL3 +7.43 [6.03, 8.93]; pooled +8.91 [7.70, 10.16].

Inputs: stage-B ledger sha256 be716482c6f9, development-ablation ledger 700f204853cb, code d66d500ed2f2. Decode parity on 52 OV-dev-B images: 52/52 identical for both backbones. GPU: 3.32 GPU-hours (cap 5, hard 6).

### Test-run operations (moved from Sections 7 and 8.5 of the main text)

These are procedural records. None changed a configuration, threshold, metric, set or rule after a test output existed, and none involved a test image unless stated.

#### Decode-parity check before the Vietnamese test, and its reruns

Before any test image reached the GPU server, the registration required a fresh decode-parity check on that machine. The frozen `ret` arm of each backbone re-decodes a fixed slice of KTVIC dev299 images through the test decode path. Each backbone passes if at least 95% of its captions are identical to the stage-A captions. The slice was 52 images, a development set; it is a parity check and is never reported as a result. The check needed three attempts.

1. **Attempt 1: stopped before any decoding.** The job's preflight self-test failed on the test machine and passed locally. A self-test wrote to a temporary path, and on the test machine the output guard correctly refused that path. No model was loaded, nothing was decoded, and the cap ledger recorded 0 GPU-seconds. The fix changed only self-test code. An independent review checked it as test-only and ruled this attempt final. The development images were removed and staged again at the new code commit.
2. **Attempt 2: PASS (Qwen2.5-VL) and PASS (InternVL3), but its record could not be closed.** Both backbones gave identical captions: Qwen2.5-VL 52/52 and InternVL3 52/52 (157 GPU-seconds). The run then stopped at the mirror checksum step. The checksum list named two partial-progress files that the mirror deliberately skips. After review, the checksum code was fixed and the reviewer authorised one rerun of the check, fixing in advance that the third run would be the check of record and that the second could not rescue it. The second run's outputs were kept under a separate name, which needed one manual rename on the test machine. The review ruled that rename a one-time deviation.
3. **Attempt 3, the check of record: PASS (Qwen2.5-VL) and PASS (InternVL3).** Qwen2.5-VL gave 52/52 (100.0%) and InternVL3 52/52 (100.0%) identical captions, with identical prompts (132 GPU-seconds). The development images were deleted, and the deletion recorded, before the OpenViIC test images were staged.

All three attempts used development data only. No test image was involved, so the one-look rule did not apply. Together they used 0.08 GPU-hours, counted against the test cap. Each code fix was a new commit with its own review, and both test blocks ran at the last of these commits.

#### The XM3600 block ran from a pinned worktree

After the OpenViIC block, the local repository's HEAD had moved, by a commit that changed no test code: the diff of the test code directory between the two commits is empty. The run script's first check refused to start because the local HEAD differed from the test commit. This happened before anything was staged or read.

The XM3600 block and the offline verified-precision step were then run from a separate worktree detached at the test commit. Its checksums verified, and a dry run of the scorer gave output byte-identical to the reviewed dry run. The GPU server stayed at the test commit throughout. Both XM3600 decision files record the same registration hash and frozen-configuration hash as the OpenViIC decision file.

#### Truncated OpenViIC test files

The three truncated OpenViIC test files took the retry path:
- in the query-embedding step (3 records);
- in each of the 8 OpenViIC decodes (24 records);
- in the verifier pass, for one file that had neighbour-only classes (1 record).

No other file failed its strict decode, and no file was excluded. All three files are in both the primary set and the full set.

#### Timing of the decision to add an English arm

The decision was taken on the Vietnamese test day, 2026-10-26. It was recorded in the project's working log at 03:11:52Z and approved by the study lead at 03:15:33Z (decision log). Neither record is a git commit, and the working log is not under version control, so these two timestamps cannot be checked independently. Both were written after the OpenViIC test block had started (2026-10-26T02:18:56Z) and before the first decision file existed (2026-10-26T06:55:27Z).

#### English arm

**One look per set, in practice.** The COCO block ran first and was decided at 2026-10-27T10:30:58Z, recorded at code commit ed1e6c41. The NoCaps block was decided at 2026-10-27T17:33:57Z. Between the two blocks the GPU server was moved from commit ed1e6c41 to f8cccb68 (2026-10-27T10:33:32Z). The diff between the two commits is empty on the English code and registration paths, and both English checksum lists verified before the NoCaps block started.

**One amendment, before any decode.** After the memory had been built, the local (CPU) step that writes the memory caption store failed on a file-permission check. Amendment 1 fixed that guard, made the caption store a separate local step with its own exclusion checks, and made test-set staging stop while a pilot job runs. The pooling, feature and build steps ran at the code before the amendment, and their outputs are unchanged. The smoke test and both test blocks ran at the amended code. No decode, score or test-set staging had run before the amendment.

**Smoke test.** Before any test image was staged, the six arms decoded 16 memory images (96 captions, 0 empty) to check the pipeline. Nothing was scored, and the outputs were deleted.

**Guard counts (COCO).** On COCO, InternVL3's `ret` captions held 524 neighbour-only object items. The verifier rejected 302 of them, 110 captions were edited by deletion and 182 fell back to the zero-shot caption. With `rand` the counts were 123, 112, 39 and 73. These counts are tallied per run over all images of the set. The NoCaps counts (Table S13) are therefore the same for the 4,500 and the 3,500 scored sets.

### Instrument definitions

These definitions make the instruments of Sections 3 and 5 usable without the companion manuscripts. All gold comes from existing released references or labels; no label was created for this study.

- **Scoring kit.** Candidates and references are lower-cased and segmented into words with RDRSegmenter (VnCoreNLP 1.2). CIDEr-D (×100) uses document frequencies over the scored set's own references. The *stripped* column removes trailing punctuation tokens from candidates and references before scoring; the *as-written* column keeps them; a PTB-tokenised column is also written. The kit is loaded by sha256, and its code is released with the study code.
- **Vietnamese object matcher.** A lexicon matcher that maps Vietnamese words to object classes after tone-mark normalisation: the two placements of the tone mark in a syllable (for example *hoà* and *hòa*) map to one form. Each caption is matched once, and its classes are the distinct classes in order of first mention. The lexicon is the companion object-precision study's and is released with its kit.
- **Count-matched precision P_cm.** For image i, with M_i(run) and M_i(zs) the distinct matched classes of the run's caption and of the same model's zero-shot caption, k_i = min(|M_i(run)|, |M_i(zs)|). tp_cm counts how many of the first k_i classes of the run's caption are supported by the gold, and tp_cm,zs does the same for the zero-shot caption. ΔP_cm = 100 · (Σ tp_cm − Σ tp_cm,zs) / Σ k_cm. On every Vietnamese set the gold for an image is the union of the classes matched in its released references. Verified precision on XM3600 (XM-b) instead uses the released Open Images V7 human-verified labels, mapped to classes by the companion study's mapping rule, and counts all mentions rather than a matched number.
- **English matcher.** The English port of the deletion step matches COCO-80 classes with the CHAIR synonym list [@Rohrbach2018CHAIR].
- **Verifier question.** For a neighbour-only class, the verifier is asked "Is there {np} in the image? Answer yes or no.", where {np} comes from the fixed 112-class English class map of the companion scoring study's verifier protocol; the score is defined in Section 3.4.
