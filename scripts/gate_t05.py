#!/usr/bin/env python
"""Gate T0.5: can one logit pass replace the K=5 self-consistency verifier?

    python scripts/gate_t05.py --in <stage1_dir> --n 600 --out data/results/gate_t05.json
    python scripts/gate_t05.py --self-check

For a random sample of stored probes, re-asks the same question once with
`VinternAdapter.yes_no_logit` and compares against what Stage 1 saved:
 G1  greedy answer agreement (logit-pass yes/no vs stored greedy answer) >= 98%;
 G2  Cohen's kappa between P(yes) >= 0.5 and the K=5 majority >= 0.7;
 plus seconds per probe for the logit pass. Pass = G1 and G2.
"""
from __future__ import annotations

import argparse
import json
import os
import random
import time
from pathlib import Path

IMAGES = Path(os.environ.get("NCS_DATA", "~/ncs-data")).expanduser() / "datasets" / "ktvic" / "images"


def is_yes(text: str) -> bool:
    return str(text or "").strip().lower().startswith(("có", "đúng", "phải", "yes"))


def kappa(a: list[bool], b: list[bool]) -> float:
    n = len(a)
    po = sum(x == y for x, y in zip(a, b)) / n
    pa, pb = sum(a) / n, sum(b) / n
    pe = pa * pb + (1 - pa) * (1 - pb)
    return 1.0 if pe == 1 else (po - pe) / (1 - pe)


def sample_probes(src: Path, n: int, seed: int) -> list[dict]:
    probes = []
    for f in sorted(src.glob("*.json")):
        rec = json.loads(f.read_text(encoding="utf-8"))
        for p in rec["propositions"]:
            for q in (p.get("evidence") or {}).get("probes") or []:
                if q.get("samples"):
                    probes.append({"file_name": rec["file_name"], "question": q["question_vi"],
                                   "greedy": q["answer"], "samples": q["samples"]})
    random.Random(seed).shuffle(probes)
    return probes[:n]


def score(rows: list[dict]) -> dict:
    greedy = [is_yes(r["greedy"]) for r in rows]
    logit_ans = [is_yes(r["logit_text"]) for r in rows]
    logit_p = [r["p_yes"] >= 0.5 for r in rows]
    majority = [sum(map(is_yes, r["samples"])) * 2 > len(r["samples"]) for r in rows]
    g1 = sum(x == y for x, y in zip(logit_ans, greedy)) / len(rows)
    g2 = kappa(logit_p, majority)
    return {"n": len(rows), "G1_greedy_agreement": round(g1, 4), "G2_kappa_vs_k5": round(g2, 4),
            "sec_per_probe": round(sum(r["sec"] for r in rows) / len(rows), 3),
            "pass": g1 >= 0.98 and g2 >= 0.7}


def self_check() -> None:
    assert kappa([True, False, True, False], [True, False, True, False]) == 1.0
    assert abs(kappa([True, True, False, False], [True, False, True, False])) < 1e-9
    rows = [{"greedy": "Có.", "logit_text": "Có", "p_yes": 0.9, "samples": ["Có"] * 4 + ["Không"], "sec": 0.1},
            {"greedy": "Không.", "logit_text": "Không", "p_yes": 0.2, "samples": ["Không"] * 5, "sec": 0.1}]
    s = score(rows)
    assert s["G1_greedy_agreement"] == 1.0 and s["G2_kappa_vs_k5"] == 1.0 and s["pass"], s
    print("self-check OK")


def main() -> int:
    ap = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    ap.add_argument("--in", dest="src", type=Path, required=True)
    ap.add_argument("--n", type=int, default=600)
    ap.add_argument("--seed", type=int, default=42)
    ap.add_argument("--out", type=Path, required=True)
    ap.add_argument("--raw-prompt", action="store_true", help="ask the probe verbatim, without the yes/no instruction")
    args = ap.parse_args()

    import sys
    sys.path.insert(0, str(Path(__file__).resolve().parents[1]))
    from PIL import Image
    from rescap.vlm.vintern import VinternAdapter

    model = VinternAdapter().load()
    rows = []
    for probe in sample_probes(args.src, args.n, args.seed):
        image = Image.open(IMAGES / probe["file_name"]).convert("RGB")
        t = time.perf_counter()
        text, p_yes = model.yes_no_logit(image, probe["question"], instruct=not args.raw_prompt)
        rows.append({**probe, "logit_text": text, "p_yes": p_yes, "sec": time.perf_counter() - t})
    report = score(rows)
    args.out.parent.mkdir(parents=True, exist_ok=True)
    args.out.write_text(json.dumps({**report, "rows": rows}, ensure_ascii=False, indent=1), encoding="utf-8")
    print(json.dumps(report))
    return 0 if report["pass"] else 1


if __name__ == "__main__":
    import sys
    sys.exit(self_check() if "--self-check" in sys.argv else main())
