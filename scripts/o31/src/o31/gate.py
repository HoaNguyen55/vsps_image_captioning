"""Gate K0 (prereg §4.5): supervision object recall and precision of a store at recall_funnel's `sft_caption` stage.

recall_funnel.py (sha 6313f1b2) definitions, kept exactly: gold = 113-lexicon objects (rescap.chair.objects_in) of
the record's references; images with empty gold are skipped; P = 100 * sum|M&G| / max(sum|M|, 1) (micro);
R = 100 * mean_i |M_i&G_i| / |G_i| (macro); an image with no detailed row has M = {} (recall 0).
OP* = max R_sup subject to P_sup >= P_floor = P_sup(S1) - 2.0; ties -> higher P_sup, then grid order.
No feasible point -> FAIL. K0 PASS iff R_sup(OP*) >= 47.1.
"""
from __future__ import annotations

from . import repo

R_GOAL, FLOOR_DROP = 47.1, 2.0


def funnel(pairs: list[tuple[set, set]]) -> dict:
    """pairs = [(gold, mentioned)] per record; returns {P, R, n} as recall_funnel's sft_caption line."""
    tp = named = 0
    recalls = []
    for gold, m in pairs:
        if not gold:
            continue
        tp += len(m & gold)
        named += len(m)
        recalls.append(len(m & gold) / len(gold))
    if not recalls:
        raise ValueError("no record with gold objects")
    return {"P": 100 * tp / max(named, 1), "R": 100 * sum(recalls) / len(recalls), "n": len(recalls)}


def store_funnel(records: list[dict], captions: dict) -> dict:
    repo()
    from rescap.chair import objects_in

    pairs = [(set().union(*[set(objects_in(c)) for c in r["reference_captions"]]),
              set(objects_in(captions.get(r["image_id"], "")))) for r in records]
    return funnel(pairs)


def choose(points: list[dict], s1: dict) -> dict:
    """points: [{op, P, R}] in grid order; s1: {P, R} of the S1 store. Returns the K0 decision record."""
    floor = s1["P"] - FLOOR_DROP
    feas = [(i, p) for i, p in enumerate(points) if p["P"] >= floor]
    if not feas:
        return {"P_floor": floor, "op_star": None, "op_mid": None, "pass": False, "reason": "no feasible point"}
    i_star, star = max(feas, key=lambda ip: (ip[1]["R"], ip[1]["P"], -ip[0]))
    mid_r = (s1["R"] + star["R"]) / 2
    _, mid = min(enumerate(points), key=lambda ip: (abs(ip[1]["R"] - mid_r), -ip[1]["P"], ip[0]))
    return {"P_floor": floor, "op_star": star, "op_mid": mid, "mid_target_R": mid_r,
            "pass": star["R"] >= R_GOAL, "reason": "R_sup(OP*) >= 47.1" if star["R"] >= R_GOAL else "R_sup(OP*) < 47.1"}


# ------------------------------------------------------------------ K0 replay driver (P0r: Vintern-only; P1: full grid)
def load_table(path) -> dict:
    """probes.jsonl -> {image file name: {qkey: p_yes}}, first occurrence kept (e1e2.logit_tables)."""
    import json
    from pathlib import Path

    t: dict = {}
    for line in Path(path).read_text(encoding="utf-8").splitlines():
        if line.strip():
            r = json.loads(line)
            t.setdefault(r["image"], {}).setdefault(r["q"], r["p_yes"])
    return t


def run_k0(records: list[dict], tables: dict[str, dict], build=None, store_dir=None) -> dict:
    """records: RAW (pre-neutralization) stage-1 records with file_name and reference_captions; tables:
    {family: load_table}. Erratum E4 order for every arm: statuses -> person_uncap -> build.
    S1 = recorded statuses at B = 9; each grid point whose families all have a table = apply_states (O31 combiner)
    at the scaled budget. FAULTs: a Q+ absent from a used table (E2), a proposition without Q+ whose recorded status
    is not REJECTED (E3), a record already carrying gender_uncap (E4). Only a complete 30-point run carries the K0
    verdict; a partial run (P0r) carries a preview choice, labelled so (E7). Numbers and shas only, no caption text.
    store_dir: each arm's sft.jsonl is written to store_dir/<arm>/ and its sha is the one reported (E5); the stores
    are training-pool supervision and stay on the host."""
    import sys
    import time
    from pathlib import Path

    from . import store, verify

    def arm(unc: list[dict], ust: dict, scaled: bool, name: str) -> dict:
        """unc = records after person_uncap (ust = its stats) -> build -> K0 numbers."""
        rows, rep = store.rebuild(unc, scaled=scaled, build=build)
        sha = store.write_store(rows, Path(store_dir) / name) if store_dir else store.store_sha(rows)
        return {**store_funnel(records, store.detailed_captions(rows)), "rows": len(rows), "store": name,
                "sft_sha256": sha, "uncap": ust,
                "mean_budget": sum(rep["budgets"].values()) / max(len(rep["budgets"]), 1)}

    t0 = time.time()
    s1 = arm(*store.uncap(records), scaled=False, name="S1")  # recorded statuses -> person_uncap -> build (E4)
    s1["elapsed_s"] = time.time() - t0
    points, skipped = [], []
    todo = sum(set(f) <= set(tables) for *_, f in verify.grid())
    for i, (a, r, fams) in enumerate(verify.grid()):
        if not set(fams) <= set(tables):
            skipped.append([a, r, list(fams)])
            continue
        recs, n = [], {}
        for rec in records:
            out, c = verify.apply_states(rec, {f: tables[f].get(rec["file_name"], {}) for f in fams}, fams, a, r)
            recs.append(out)
            for k, v in c.items():
                n[k] = n.get(k, 0) + v
        if n["miss"]:
            raise SystemExit(f"FAULT {n['miss']} Q+ keys missing from the {fams} tables at ({a}, {r})")
        if n["no_q_not_rejected"]:
            raise SystemExit(f"FAULT {n['no_q_not_rejected']} propositions without Q+ are not recorded REJECTED")
        t1 = time.time()
        name = f"p{i:02d}_{'+'.join(fams)}_{a:.2f}_{r:.2f}"
        points.append({"op": [a, r, list(fams)], "states": n, **arm(*store.uncap(recs), scaled=True, name=name)})  # E4
        points[-1]["elapsed_s"] = time.time() - t1
        print(f"K0 point {len(points)}/{todo}: {points[-1]['elapsed_s']:.0f} s; projected total "
              f"{(time.time() - t0) / len(points) * todo / 3600:.2f} h", file=sys.stderr)
    complete = not skipped
    choice = choose(points, s1) if points else None
    return {"s1": s1, "points": points, "skipped": skipped, "complete": complete,
            "decision": choice if complete else None,
            "preview_no_verdict": None if complete else choice}


def main(argv=None) -> int:
    """Entry point of k0.py (top level): python -I -B k0.py --records DIR --table vintern=probes.jsonl
    [--table internvl3=...] [--exclude ids.txt] --store-dir DIR --out k0.json"""
    import argparse
    import json
    from pathlib import Path

    from . import sha_file

    ap = argparse.ArgumentParser()
    ap.add_argument("--records", required=True, type=Path)
    ap.add_argument("--table", action="append", default=[], help="family=path")
    ap.add_argument("--exclude", type=Path, help="file names removed by the §3.5 (a) overlap pass, one per line")
    ap.add_argument("--out", required=True, type=Path)
    ap.add_argument("--store-dir", required=True, type=Path, help="host folder for each arm's sft.jsonl (E5)")
    a = ap.parse_args(argv)
    files = sorted(p for p in a.records.glob("*.json") if not p.name.startswith("_"))
    drop = set(a.exclude.read_text(encoding="utf-8").split()) if a.exclude else set()
    recs = [json.loads(p.read_text(encoding="utf-8")) for p in files]
    recs = [r for r in recs if r["file_name"] not in drop]
    spec = dict(t.split("=", 1) for t in a.table)
    res = run_k0(recs, {f: load_table(p) for f, p in spec.items()}, store_dir=a.store_dir)
    res["inputs"] = {"n_records": len(recs), "n_excluded": len(files) - len(recs),
                     "exclude_sha256": sha_file(a.exclude) if a.exclude else None,
                     "tables": {f: sha_file(Path(p)) for f, p in spec.items()}}
    a.out.write_text(json.dumps(res, indent=1) + "\n", encoding="utf-8")
    d = res["decision"] or res["preview_no_verdict"] or {}
    print(json.dumps({"complete": res["complete"], "pass": d.get("pass"), "P_floor": d.get("P_floor")}))
    return 0

