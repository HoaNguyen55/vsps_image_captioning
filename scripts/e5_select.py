#!/usr/bin/env python
"""E5, step 2 (CPU): rank sampled captions by utility U, write SFT and DPO data.

    python scripts/e5_select.py --samples e5_samples.jsonl --gold-sft $NCS_DATA/gold_fuse2 \\
        --out $NCS_DATA/e5_round1
    python scripts/e5_select.py --selftest

U(caption) = object F1 against the union of the image's reference objects
             - lam * #{mentioned objects no reference names, with p_exist < tau}.
An unreferenced object without a probe score counts as low (penalised).

Writes OUT/sft.jsonl (best sample per image with U >= --min-u, detailed prompt, plus
every row of GOLD_SFT/sft.jsonl, shuffled) and OUT/dpo.jsonl (best vs worst when
U_best - U_worst >= --margin), in the formats train_stage2.py --stage sft/dpo reads.
"""
from __future__ import annotations

import argparse
import json
import random
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT))
sys.path.insert(0, str(ROOT / "scripts"))


def utility(mentioned: set[str], gold: set[str], p_exist: dict[str, float], lam: float, tau: float) -> float:
    tp = len(mentioned & gold)
    f1 = 2 * tp / (len(mentioned) + len(gold)) if tp else 0.0
    low = sum(p_exist.get(o, 0.0) < tau for o in mentioned - gold)
    return f1 - lam * low


def selftest() -> None:
    g = {"người", "chó"}
    assert utility({"người", "chó"}, g, {}, 0.1, 0.5) == 1.0
    assert utility(set(), g, {}, 0.1, 0.5) == 0.0
    # one unreferenced object: F1 = 2*2/(3+2) = 0.8; penalised unless the probe vouches for it
    assert abs(utility({"người", "chó", "xe"}, g, {}, 0.1, 0.5) - 0.7) < 1e-9
    assert abs(utility({"người", "chó", "xe"}, g, {"xe": 0.3}, 0.1, 0.5) - 0.7) < 1e-9
    assert abs(utility({"người", "chó", "xe"}, g, {"xe": 0.9}, 0.1, 0.5) - 0.8) < 1e-9
    assert utility({"mèo"}, g, {}, 0.1, 0.5) == -0.1
    print("selftest ok")


def main() -> int:
    ap = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    ap.add_argument("--selftest", action="store_true")
    ap.add_argument("--samples")
    ap.add_argument("--gold-sft", help="directory with the sft.jsonl to mix in (gold_fuse2)")
    ap.add_argument("--out")
    ap.add_argument("--lam", type=float, default=0.1)
    ap.add_argument("--tau", type=float, default=0.2,
                    help="probe scores of unreferenced objects run low (label = any annotator named it)")
    ap.add_argument("--min-u", type=float, default=0.0, help="keep the best sample only if U exceeds this")
    ap.add_argument("--margin", type=float, default=0.2, help="DPO pair only if U_best - U_worst >= this")
    ap.add_argument("--seed", type=int, default=42)
    args = ap.parse_args()
    if args.selftest:
        selftest()
        return 0
    if not (args.samples and args.gold_sft and args.out):
        ap.error("--samples, --gold-sft and --out are required")

    from build_dpo_data import PROMPT
    from evaluate import references
    from rescap.chair import objects_in

    gold = {i: set().union(*[set(objects_in(c)) for c in cs]) for i, cs in references("train_data.json").items()}
    sft, dpo, us = [], [], []
    for line in Path(args.samples).read_text(encoding="utf-8").splitlines():
        r = json.loads(line)
        scored = sorted((utility(set(objects_in(s)), gold[r["image_id"]], r.get("p_exist", {}),
                                 args.lam, args.tau), s) for s in set(r["samples"]) if s)
        if not scored:
            continue
        (u_worst, worst), (u_best, best) = scored[0], scored[-1]
        us.append(u_best)
        base = {"image_id": r["image_id"], "file_name": r["file_name"], "prompt": PROMPT}
        if u_best > args.min_u:
            sft.append({**base, "response": best, "variant": "e5_best"})
        if u_best - u_worst >= args.margin:
            dpo.append({**base, "chosen": best, "rejected": worst, "pair_type": "e5_U_best>worst"})

    gold_rows = [json.loads(x) for x in (Path(args.gold_sft) / "sft.jsonl").read_text(encoding="utf-8").splitlines()]
    rows = sft + gold_rows
    random.Random(args.seed).shuffle(rows)
    dst = Path(args.out)
    dst.mkdir(parents=True, exist_ok=True)
    for name, data in (("sft.jsonl", rows), ("dpo.jsonl", dpo)):
        (dst / name).write_text("".join(json.dumps(x, ensure_ascii=False) + "\n" for x in data), encoding="utf-8")
    report = {"samples": args.samples, "images": len(us), "lam": args.lam, "tau": args.tau,
              "min_u": args.min_u, "margin": args.margin, "mean_best_u": sum(us) / max(len(us), 1),
              "sft_e5_rows": len(sft), "sft_gold_rows": len(gold_rows), "dpo_pairs": len(dpo)}
    (dst / "_build_report.json").write_text(json.dumps(report, indent=2), encoding="utf-8")
    print(json.dumps(report, indent=2))
    return 0


if __name__ == "__main__":
    sys.exit(main())
