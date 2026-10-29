"""Render supplement Tables S13 (C-EN) and S14 (C-2) from the decide files; prints markdown. No preds read."""
import json
from pathlib import Path
R = Path("/mnt/d/vsps_image_captioning")
CO = json.loads((R / ".session_backup/machines/M3/root/outputs/c_en/decide_coco_test.json").read_text())
NC = json.loads((R / ".session_backup/machines/M3/root/outputs/c_en/decide_nocaps_val.json").read_text())
C2 = json.loads((R / ".session_backup/machines/M4/root/outputs/c2_ablation/decide.json").read_text())
M = "−"
n = lambda x, d=2: f"{x:,.{d}f}".replace("-", M)
s = lambda x: ("+" if x > 0 else "") + n(x)
t = lambda o: f"{s(o['d'])} [{n(o['lo'])}, {n(o['hi'])}]"
NM = {"qwen25vl_7b": "Qwen2.5-VL", "internvl3_8b": "InternVL3"}
out = []
P = out.append
P("### English arm (C-EN): every registered and reported row\n")
P("**Table S13. C-EN rows on the three scored sets (PTB CIDEr-D, paired 95% bootstrap CIs, B = 2,000; InternVL3 at its frozen τ = 0.10 unless marked).** Per-backbone, `zs` and length rows are reported, non-gating. Length is the mean number of PTB tokens.\n")
P("| scored set | backbone | `ret` − `rand` | `ret` − `zs` | `rand` − `zs` | length `ret` | length `rand` | length gap |")
P("|---|---|---|---|---|---|---|---|")
sets = [("COCO Karpathy test (5,000)", CO["scored"]["coco_test_5000"]), ("NoCaps val (4,500)", NC["scored"]["nocaps_val_4500"]),
        ("NoCaps val without the earlier 1,000 (3,500)", NC["scored"]["nocaps_val_3500"])]
for name, sc in sets:
    for m, r in sc["per_model"].items():
        P(f"| {name} | {NM[m]} | {t(r['ret_minus_rand'])} | {t(r['ret_minus_zs'])} | {t(r['rand_minus_zs'])} | "
          f"{n(r['len_ret'])} | {n(r['len_rand'])} | {n(r['length_gap'], 3)} |")
    P(f"| {name} | pooled | {t(sc['pooled'])} | {t(sc['pooled_ret_minus_zs'])} | | | | |")
    P(f"| {name} | InternVL3, τ = −∞ (registered secondary) | {t(sc['secondary_neg_inf_internvl3'])}, {sc['secondary_neg_inf_internvl3']['label']} | | | | | |")
P("\nVerdicts: P1-EN " + CO["P1_EN"]["verdict"] + " (rule L does not fire); S-NC " + NC["S_NC"]["verdict"] +
  "; 3,500-image sensitivity " + NC["S_NC_sensitivity_3500"]["verdict"] + "; the claim that the gain transfers to NoCaps val is not made.\n")
P("**InternVL3 deletion-step counts, per run (all images of the set; identical for the 4,500 and 3,500 scored sets).** Neighbour-only and rejected are object items; deleted and fallback are captions.\n")
P("| set | arm | neighbour-only | rejected | deleted | fallback |")
P("|---|---|---|---|---|---|")
for name, sc in sets[:2]:
    g = sc["per_model"]["internvl3_8b"]
    for a, k in (("`ret`", "guard"), ("`rand`", "guard_rand")):
        P(f"| {name.split(' (')[0]} | {a} | {g[k]['neighbour_only']} | {g[k]['rejected']} | {g[k]['deleted']} | {g[k]['fallback']} |")
P("\n**NoCaps val by domain (pooled `ret` − `rand`).** " + "; ".join(
    f"{d} (n = {v['n']:,}) {t(v)}" for d, v in NC["per_domain"].items()) + ".\n")
P("Decision files: `decide_coco_test.json` (head " + CO["head"][:8] + ", " + CO["utc"] + "), `decide_nocaps_val.json` (head " +
  NC["head"][:8] + ", " + NC["utc"] + "); ledger sha256 prefixes " + ", ".join(v[:12] for v in {**CO["ledger_sha256"], **NC["ledger_sha256"]}.values()) + ".\n")

P("### Mechanism on the development set (OV-dev-B), dated 2026-10-27\n")
P(f"**Table S14. Every row of the C-2 decision file. Label: \"{C2['label']}\". OV-dev-B, {C2['n_images']} images, stripped CIDEr-D.** Not a test result; no row enters the abstract or the contributions.\n")
P("Outcomes: AB-M " + C2["AB-M"]["outcome"] + f" (M1 {C2['AB-M']['M1_ci_hi_lt_0']}, M2 {C2['AB-M']['M2_did_le_minus_sesoi']}, M3 {C2['AB-M']['M3_monotone_points']}); "
  "AB-K P-K " + C2["AB-K"]["P-K"]["outcome"] + f" (K1 {C2['AB-K']['P-K']['K1_monotone_points']}, K2 {C2['AB-K']['P-K']['K2_did_ge_sesoi']}, K3 {C2['AB-K']['P-K']['K3_ci_lo_gt_0']}; label \"{C2['AB-K']['P-K']['label']}\"); "
  "AB-τ " + C2["AB-tau"]["outcome"] + f" (i {C2['AB-tau']['i_monotone']}, ii {C2['AB-tau']['ii_cost_ret_lt_rand']}, iii {C2['AB-tau']['iii_inf_ci_lo_le_0']}); "
  f"section-6 condition {C2['section6_explains_backbone_dependence']}.\n")
P("*AB-M (memory size; shared `rand` from the full memory).*\n")
P("| memory | clusters | composition (OpenViIC only / both / KTVIC only) | mean top-1 cosine | pooled | Qwen2.5-VL | Qwen2.5-VL src share | InternVL3 τ 0.10 | InternVL3 src share | InternVL3 τ −∞ |")
P("|---|---|---|---|---|---|---|---|---|---|")
A = C2["AB-M"]
for p in ("10", "30", "100"):
    cl = C2["subsets"][p]["n"] if p in C2["subsets"] else sum(C2["composition"][p].values())
    c = C2["composition"][p]
    P(f"| {p}% | {cl:,} | {c['openviic']:,} / {c['ktvic+openviic']:,} / {c['ktvic']:,} | {n(C2['mean_top1_cos'][p], 3)} | {t(A['pooled'][p])} | "
      f"{t(A['per_model']['qwen25vl_7b']['delta'][p])} | {n(A['per_model']['qwen25vl_7b']['src_share'][p], 3)} | "
      f"{t(A['per_model']['internvl3_8b']['delta'][p])} | {n(A['per_model']['internvl3_8b']['src_share'][p], 3)} | "
      f"{t(A['per_model']['internvl3_8b']['delta_tau_-inf'][p])} |")
P(f"| 10% − 100% | | | | {t(A['did_pooled'])} | {t(A['per_model']['qwen25vl_7b']['did'])} | | {t(A['per_model']['internvl3_8b']['did'])} | | |")
P("\n*AB-K (number of examples; 100% memory).*\n")
P("| backbone | k | `ret` − `rand` | syllables `ret` | syllables `rand` | ends in punctuation `ret` / `rand` | top-3 opening share `ret` / `rand` | 4-gram copy share | near-verbatim share |")
P("|---|---|---|---|---|---|---|---|---|")
for m in ("qwen25vl_7b", "internvl3_8b"):
    K = C2["AB-K"][m]
    for k in ("2", "4", "8"):
        st = K["style"][k]
        P(f"| {NM[m]} | {k} | {t(K['delta'][k])} | {n(st['ret']['mean_syllables'])} | {n(st['rand']['mean_syllables'])} | "
          f"{n(st['ret']['ends_punct'], 3)} / {n(st['rand']['ends_punct'], 3)} | {n(st['ret']['top3_open_share'], 3)} / {n(st['rand']['top3_open_share'], 3)} | "
          f"{n(K['copy4_memory'][k], 3)} | {n(K['verbatim_share'][k], 3)} |")
P(f"\nP-K difference, Qwen2.5-VL k = 8 minus k = 2: {t(C2['AB-K']['P-K']['did_8_minus_2'])}.\n")
P("*AB-τ (InternVL3; stage-B decodes re-scored on CPU).* Cost = mean(arm at τ − arm at −∞). NO rate = neighbour-only classes / all matched classes; NP = neighbour-only precision against reference gold over Σm mentions.\n")
P("| τ | `ret` − `rand` | cost `ret` | cost `rand` | arm | NO rate | rejected per image | deleted share | fallback share | NP (Σm) |")
P("|---|---|---|---|---|---|---|---|---|---|")
T = C2["AB-tau"]
for tau in ("-inf", "0.00", "0.10", "0.20", "0.30", "inf"):
    lab = {"-inf": "−∞", "inf": "+∞"}.get(tau, tau)
    for a in ("ret", "rand"):
        g = T["guard_rates"][tau][a]
        np_ = "n/a (0)" if g["np"] is None else f"{n(g['np'])} ({g['np_sum_m']})"
        c = T["cost"].get(tau, {}).get(a)
        first = a == "ret"
        P(f"| {lab if first else ''} | {t(T['delta'][tau]) if first else ''} | {t(T['cost'][tau]['ret']) if first and tau in T['cost'] else ''} | "
          f"{t(T['cost'][tau]['rand']) if first and tau in T['cost'] else ''} | `{a}` | {n(g['neighbour_only_rate'], 3)} | {n(g['rejected_per_image'], 3)} | "
          f"{n(g['deleted_rate'], 3)} | {n(g['fallback_rate'], 3)} | {np_} |")
r = C2["rand_minus_zs_100"]
P(f"\n*Style check (`rand` − `zs`, 100% memory; post-hoc remark only).* Qwen2.5-VL {t(r['qwen25vl_7b'])}; InternVL3 {t(r['internvl3_8b'])}; pooled {t(r['pooled'])}.\n")
P("Inputs: stage-B ledger sha256 " + C2["inputs"]["l2_sha256"][:12] + ", C-2 ledger " + C2["inputs"]["ledger_sha256"][:12] +
  ", code " + C2["inputs"]["code_sha256"][:12] + ". Decode parity on 52 OV-dev-B images: 52/52 identical for both backbones. GPU: 3.32 GPU-hours (cap 5, hard 6).")
print("\n".join(out))
