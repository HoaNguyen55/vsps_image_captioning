#!/usr/bin/env python3
"""G-RL pilot decisions, written before any pilot output (PILOT_RULE.md §5 Gate 0, §6 Gate 1). Refuses to overwrite.

    python3 scripts/grl/decide.py --selftest
    python3 scripts/grl/decide.py gate0 --dir G0 --size 7b --out G0/gate0_decide.json
    python3 scripts/grl/decide.py gate1 --scores G1/scores.json --run G1 --out G1/gate1_decide.json
"""
from __future__ import annotations

import argparse
import json
import math
import sys
from pathlib import Path

HERE = Path(__file__).resolve().parent
sys.path.insert(0, str(HERE))
import common as K  # noqa: E402

N_REFS_UT = 12012  # id_counts.json references_per_split.ut2402
OVERHEAD_H = 0.15 * 8  # model load + guard scan per GPU stage, 8 stages


def gate0(m: dict, size: str) -> dict:
    """m: measured rates (sec per unit) and peaks. Projection of Gate 1 at the full data, then the ladder."""
    g, c = K.GATE0, K.CFG
    proj = {"base_samples": K.N_TRAIN * m["s_sample"], "rft_sft": c["sft_epochs"] * K.N_TRAIN * m["s_sft"],
            "sftref_sft": c["sft_epochs"] * N_REFS_UT * m["s_sft"], "grl": K.N_TRAIN * m["s_grl"],
            "dev_decodes": 4 * K.N_VAL * m["s_greedy"]}
    proj = {k: v / 3600 for k, v in proj.items()} | {"overhead": OVERHEAD_H}
    total = sum(proj.values())
    cap = math.ceil(g["cap_factor"] * total)
    why = []
    if not m["checks_ok"]:
        verdict = why.append("a dry-run check failed") or "STOP"
    elif m["peak_gb"] > g["peak_gb_stop"]:  # CC-118 W3; CC-124 r7: STOP -> TO-PI, no automatic 3B (PI_OK=3B only)
        verdict = why.append(f"peak {m['peak_gb']:.2f} GB > {g['peak_gb_stop']} (TO-PI; 3B only on a logged PI_OK=3B)") or "STOP"
    elif m["finished_share"] < g["finished_min"]:
        verdict = why.append(f"{m['finished_share']:.2f} of base samples finish within 160 tokens") or "TO-PI"
    elif size == "7b" and proj["grl"] > g["switch_7b_grl_gpuh"]:
        verdict = why.append(f"G-RL arm {proj['grl']:.1f} GPU-h > {g['switch_7b_grl_gpuh']} at 7B") or "SWITCH-3B"
    elif size == "3b" and proj["grl"] > g["stop_3b_grl_gpuh"]:
        verdict = why.append(f"G-RL arm {proj['grl']:.1f} GPU-h > {g['stop_3b_grl_gpuh']} at 3B") or "STOP"
    elif total > g["pi_above_gpuh"]:
        verdict = why.append(f"projected {total:.1f} GPU-h > {g['pi_above_gpuh']} (CC-118 planning figure)") or "TO-PI"
    else:
        verdict = "GO"
    return {"verdict": verdict, "why": why, "size": size, "measured": m,
            "projected_gpuh": {k: round(v, 2) for k, v in proj.items()}, "projected_total_gpuh": round(total, 2),
            "cap_gpuh": cap, "label": "Gate 0 run discarded; no adapter from it is used"}


def gate1(s: dict, window: list[float], kl_tail: float, picks: dict) -> dict:
    """GO iff every criterion holds; STOP otherwise. One look; no rerun or retune after a STOP. window: anchors.json
    (train side); kl_tail: G-RL mean KL per caption over its last steps (labels a STOP, changes no verdict)."""
    g, sy, ct = K.GATE1, s["systems"], s["contrasts"]
    main, vb = ct["grl-sftref"], ct["grl-base"]
    base, grl = sy["base"], sy["grl"]
    crit = {
        "H_raw: dF1(v2) vs SFT-ref >= SESOI and CI lo > 0":
            main["v2"]["F1"][0] >= g["sesoi_f1"] and main["v2"]["F1"][1] > 0,
        "H_matched_base: matched dF1(v2) vs base CI lo > 0": vb["matched_v2"]["F1"][1] > 0,
        "H_matched_sftref: matched dF1(v2) vs SFT-ref CI lo > -1.0":
            main["matched_v2"]["F1"][1] > g["matched_ni_sftref"],
        "NI_precision: dP(v2) vs SFT-ref CI lo > margin": main["v2"]["P"][1] > g["margin_p"],
        "G1 Vietnamese-only >= base - 0.5 pp": grl["vi_only_pct"] >= base["vi_only_pct"] - g["vi_drop_pp"],
        "G2 mean syllables inside the train-side window": window[0] <= grl["syllables_mean"] <= window[1],
        "G3 not (classes/caption > 1.5 x base and matched dF1 vs base CI lo <= 0)": not (
            grl["v2"]["classes_per_caption"] > g["class_tokens_x"] * base["v2"]["classes_per_caption"]
            and vb["matched_v2"]["F1"][1] <= 0),
        "G4 hedged/negated-mention captions <= base + 2 pp":
            grl["hedged_caption_pct"] <= base["hedged_caption_pct"] + g["hedge_rise_pp"],
        "G5 non-COCO nouns per caption >= 0.9 x base":
            grl["noncoco_nouns_per_caption"] >= (1 - g["noncoco_drop"]) * base["noncoco_nouns_per_caption"],
        "G6 list-style captions <= base + 2 pp": grl["list_style_pct"] <= base["list_style_pct"] + g["list_rise_pp"],
    }
    verdict = "GO" if all(crit.values()) else "STOP"
    logged = {k: ct[k]["v2"]["F1"] for k in ("grl-rft", "grl-base", "rft-sftref") if k in ct}
    return {"verdict": verdict, "criteria": crit, "failed": [k for k, v in crit.items() if not v],
            "under_moved": verdict == "STOP" and kl_tail < g["under_moved_kl"], "grl_kl_caption_tail": kl_tail,
            "rft_picks": picks, "logged_not_gating_dF1_v2": logged,
            "logged_matched_dF1_v2_vs_sftref": main["matched_v2"]["F1"],
            "label": "PILOT / DEV; pilot runs are not confirmatory seeds"}


def write(out: str, rec: dict) -> None:
    p = Path(out)
    if p.exists():
        raise SystemExit(f"REFUSED: {p} exists (one decision per gate)")
    p.write_text(json.dumps(rec, indent=1, default=float) + "\n")
    print(json.dumps({"verdict": rec["verdict"], **({"failed": rec["failed"]} if "failed" in rec else {}),
                      **({"cap_gpuh": rec["cap_gpuh"]} if "cap_gpuh" in rec else {})}))


def measured(d: Path) -> dict:
    """Rates from the Gate-0 stage records in d (train.py summaries and the timed evaluate.py call)."""
    j = lambda f: json.loads((d / f).read_text())  # noqa: E731
    smp, grl, sft, dec = j("samples.jsonl.summary.json"), j("grl/summary.json"), j("sft/summary.json"), j("greedy.json")
    return {"s_sample": smp["sec_per_image"], "s_grl": grl["sec_per_unit"], "s_sft": sft["sec_per_unit"],
            "s_greedy": dec["seconds"] / dec["images"], "grl_steps": grl["steps"], "sft_steps": sft["steps"],
            "finished_share": smp["finished_share"],
            "peak_gb": max(smp["peak_reserved_gb"], grl["peak_reserved_gb"], sft["peak_reserved_gb"]),
            "checks_ok": "logp" in grl["checks"] and bool(grl["checks"]["logp"]["ok"]) and grl["steps"] == K.GATE0["steps"]
            and sft["steps"] == K.GATE0["steps"]}


def selftest() -> None:
    ok = {"s_sample": 12.0, "s_grl": 30.0, "s_sft": 0.3, "s_greedy": 4.0, "peak_gb": 21.0, "checks_ok": True,
          "finished_share": 0.97}
    r = gate0(ok, "7b")
    assert r["verdict"] == "GO" and abs(r["projected_gpuh"]["grl"] - 2402 * 30 / 3600) < 0.01, r
    assert r["cap_gpuh"] == 43 and 35 < r["projected_total_gpuh"] < 36, r
    assert gate0(ok | {"s_grl": 55.0}, "7b")["verdict"] == "SWITCH-3B"  # 36.7 GPU-h > 35 (CC-124 W6)
    assert gate0(ok | {"s_grl": 40.0}, "3b")["verdict"] == "STOP"  # 26.7 > 25
    assert gate0(ok | {"peak_gb": 23.6}, "7b")["verdict"] == "STOP"
    assert gate0(ok | {"checks_ok": False}, "7b")["verdict"] == "STOP"
    assert gate0(ok | {"s_sample": 30.0}, "7b")["verdict"] == "TO-PI"
    assert gate0(ok | {"finished_share": 0.6}, "7b")["verdict"] == "TO-PI"
    sysrow = lambda f1, p, cls=2.0, vi=100.0, syl=80.0, hed=1.0, nc=5.0: {  # noqa: E731
        "v2": {"F1": f1, "P": p, "classes_per_caption": cls}, "vi_only_pct": vi, "syllables_mean": syl,
        "hedged_caption_pct": hed, "noncoco_nouns_per_caption": nc, "list_style_pct": 1.0}
    w, pk = [60.0, 100.0], {"picked": 2500}
    c = lambda d, lo: {"v2": {"F1": [d, lo, d + 2], "P": [0.0, -0.5, 0.5]}, "matched_v2": {"F1": [d, lo, d + 2]}}  # noqa: E731
    s = {"systems": {"base": sysrow(50, 60), "grl": sysrow(56, 62)},
         "contrasts": {"grl-sftref": c(3.0, 1.0), "grl-base": c(6.0, 4.0)}}
    assert gate1(s, w, 1.0, pk)["verdict"] == "GO", gate1(s, w, 1.0, pk)
    s2 = json.loads(json.dumps(s))
    s2["contrasts"]["grl-sftref"]["matched_v2"]["F1"] = [-1.5, -2.2, -0.5]
    assert gate1(s2, w, 1.0, pk)["failed"] == ["H_matched_sftref: matched dF1(v2) vs SFT-ref CI lo > -1.0"]
    s2["contrasts"]["grl-sftref"]["matched_v2"]["F1"] = [0.0, -0.5, 0.5]  # a tie at matched count passes the NI
    assert gate1(s2, w, 1.0, pk)["verdict"] == "GO" and gate1(s2, w, 0.1, pk)["under_moved"] is False
    s3 = json.loads(json.dumps(s))
    s3["systems"]["grl"]["syllables_mean"] = 120.0
    s3["contrasts"]["grl-sftref"]["v2"]["P"] = [-2.0, -1.5, -0.5]
    assert gate1(s3, w, 1.0, pk)["verdict"] == "STOP" and len(gate1(s3, w, 1.0, pk)["failed"]) == 2
    assert gate1(s3, w, 0.1, pk)["under_moved"] is True
    s4 = json.loads(json.dumps(s))
    s4["systems"]["grl"]["v2"]["classes_per_caption"] = 3.5
    s4["contrasts"]["grl-base"]["matched_v2"]["F1"] = [0.5, -0.1, 1.0]
    assert gate1(s4, w, 1.0, pk)["failed"] == ["H_matched_base: matched dF1(v2) vs base CI lo > 0",
                                              "G3 not (classes/caption > 1.5 x base and matched dF1 vs base CI lo <= 0)"]
    print("decide selftest ok")


def main() -> int:
    ap = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    ap.add_argument("gate", nargs="?", choices=("gate0", "gate1"))
    ap.add_argument("--dir")
    ap.add_argument("--size", choices=tuple(K.MODELS))
    ap.add_argument("--scores")
    ap.add_argument("--run", help="gate1: the Gate-1 output dir (anchors.json, grl/log.jsonl, picks.jsonl.summary.json)")
    ap.add_argument("--out")
    ap.add_argument("--selftest", action="store_true")
    a = ap.parse_args()
    if a.selftest:
        selftest()
        return 0
    if a.gate == "gate0":
        write(a.out, gate0(measured(Path(a.dir)), a.size))
    else:
        r = Path(a.run)
        kl = [json.loads(x)["kl_caption"] for x in (r / "grl/log.jsonl").read_text().splitlines()]
        tail = sum(kl[-K.GATE1["kl_tail_steps"]:]) / len(kl[-K.GATE1["kl_tail_steps"]:])
        write(a.out, gate1(json.loads(Path(a.scores).read_text()), json.loads((r / "anchors.json").read_text())["window"],
                           tail, json.loads((r / "picks.jsonl.summary.json").read_text())))
    return 0


if __name__ == "__main__":
    sys.exit(main())
