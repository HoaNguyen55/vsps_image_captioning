#!/usr/bin/env python
"""Draw the C2 three-state audit sample from TRAINING Stage-1 records.

    python scripts/audit_three_state_sample.py --records ~/ncs-data/stage1_neutral \
        --out data/annotations/audit_three_state_sample.json
    python scripts/audit_props.py --annotator <name> --sample data/annotations/audit_three_state_sample.json

Round 1 (tn.json) audited only machine-SUPPORTED propositions, and from TEST
images. This sample covers all three machine states on the records that become
D_VSPS, so it measures precision of SUPPORTED, what UNCERTAIN withholds and what
REJECTED throws away, per proposition type.

Strata = machine state x type. UNCERTAIN is split in two bands so that relaxed
rules (e.g. accept 4/5 affirm when the negated probe is unanimous) get a direct
human estimate instead of an extrapolation:
  near = direct probe >= 4/5 affirm AND negated probe 5/5 deny; rest = everything else.
Allocation: equal per state, equal per type within a state (largest remainder),
types with an empty pool are skipped (spatial_relation has no SUPPORTED).
At most --per-image propositions per image. Items are shuffled so the annotator
is blind to the stratum; audit_props.py shows only the image and text_vi.
Each item keeps its stored evidence, and `strata` keeps the population size of
every cell so estimates can be reweighted to the population.
"""

from __future__ import annotations

import argparse
import json
import random
import sys
from collections import Counter, defaultdict
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parents[1]))
from rescap.vlm.base import parse_yes_no  # noqa: E402

STATES = ("SUPPORTED", "UNCERTAIN", "REJECTED")
ITEM_KEYS = ("image_id", "file_name", "prop_id", "type", "text_vi", "machine_verdict")


def polarity_counts(probe: dict | None) -> tuple[int, int]:
    """(affirm, refute) sample counts of one probe; (0, 0) when absent."""
    if not probe:
        return 0, 0
    pols = [parse_yes_no(s).value for s in probe.get("samples") or []]
    return pols.count("affirms"), pols.count("refutes")


def evidence(p: dict) -> dict:
    ev, ver = p.get("evidence") or {}, p.get("verification") or {}
    probes = ev.get("probes") or []
    direct = [q for q in probes if "KHÔNG" not in q["question_vi"]]
    negated = [q for q in probes if "KHÔNG" in q["question_vi"]]
    aff_yes, _ = polarity_counts(direct[0] if direct else None)
    _, neg_no = polarity_counts(negated[0] if negated else None)
    out = {"aff_yes": aff_yes, "neg_no": neg_no,
           "grounding_score": (ev.get("visual_grounding") or {}).get("grounding_score"),
           "answer_prob": direct[0].get("answer_prob") if direct else None,
           "epistemic": p.get("epistemic"),
           "support_score": ver.get("support_score"),
           "evidence_sufficiency": ver.get("evidence_sufficiency"),
           "explanation_en": ver.get("explanation_en", "")}
    if len(direct) > 1:  # colour cross-check by the second verifier
        out["xcheck_aff_yes"] = polarity_counts(direct[1])[0]
        out["xcheck_neg_no"] = polarity_counts(negated[1] if len(negated) > 1 else None)[1]
    return out


def stratum(state: str, ptype: str, ev: dict) -> str:
    if state == "UNCERTAIN":
        band = "near" if ev["aff_yes"] >= 4 and ev["neg_no"] == 5 else "rest"
        return f"UNCERTAIN-{band}|{ptype}"
    return f"{state}|{ptype}"


def load_pool(records: Path) -> dict[str, list[dict]]:
    pool: dict[str, list[dict]] = defaultdict(list)
    files = sorted(records.glob("*.json"))
    if not files:
        raise SystemExit(f"no *.json records in {records}")
    for f in files:
        rec = json.loads(f.read_text(encoding="utf-8"))
        for p in rec["propositions"]:
            state = (p.get("verification") or {}).get("status")
            if state not in STATES:
                continue
            ev = evidence(p)
            pool[stratum(state, p["type"], ev)].append({
                "image_id": str(rec["image_id"]), "file_name": rec["file_name"],
                "prop_id": p["id"], "type": p["type"], "text_vi": p["text_vi"],
                "machine_verdict": state, "evidence": ev})
    return pool


def largest_remainder(total: int, keys: list[str]) -> dict[str, int]:
    base, extra = divmod(total, len(keys))
    return {k: base + (i < extra) for i, k in enumerate(sorted(keys))}


def allocate(n: int, pool: dict[str, list[dict]]) -> dict[str, int]:
    """Equal per state; within UNCERTAIN equal per band; then equal per type."""
    groups: dict[str, list[str]] = defaultdict(list)
    for cell, rows in pool.items():
        if rows:
            groups[cell.split("|")[0]].append(cell)
    per_state = largest_remainder(n, list(STATES))
    quota: dict[str, int] = {}
    for state, k in per_state.items():
        if state == "UNCERTAIN":
            bands = largest_remainder(k, ["UNCERTAIN-near", "UNCERTAIN-rest"])
            for band, kb in bands.items():
                quota.update(largest_remainder(kb, groups[band]))
        else:
            quota.update(largest_remainder(k, groups[state]))
    for cell, k in quota.items():
        if k > len(pool[cell]):
            raise SystemExit(f"stratum {cell}: quota {k} > pool {len(pool[cell])}")
    return quota


def draw(pool: dict[str, list[dict]], quota: dict[str, int], seed: int, per_image: int) -> list[dict]:
    rng = random.Random(seed)
    queues = {}
    for cell in sorted(quota):
        rows = list(pool[cell])
        rng.shuffle(rows)
        queues[cell] = rows
    taken: dict[str, list[dict]] = defaultdict(list)
    per_img: Counter = Counter()
    # Round-robin, smallest pool first, so a scarce cell is not starved by the per-image cap.
    order = sorted(quota, key=lambda c: (len(pool[c]), c))
    while any(len(taken[c]) < quota[c] for c in order):
        progressed = False
        for cell in order:
            if len(taken[cell]) >= quota[cell]:
                continue
            q = queues[cell]
            while q and per_img[q[-1]["image_id"]] >= per_image:
                q.pop()
            if not q:
                raise SystemExit(f"stratum {cell} exhausted under the per-image cap")
            row = q.pop()
            per_img[row["image_id"]] += 1
            taken[cell].append(dict(row, stratum=cell))
            progressed = True
        if not progressed:
            break
    items = [r for c in order for r in taken[c]]
    rng.shuffle(items)
    return items


def check(sample: dict, quota: dict[str, int], per_image: int) -> None:
    items = sample["items"]
    assert len(items) == sample["n"] == sum(quota.values())
    keys = [f"{i['image_id']}:{i['prop_id']}" for i in items]
    assert len(set(keys)) == len(keys), "duplicate proposition"
    assert max(Counter(i["image_id"] for i in items).values()) <= per_image
    assert Counter(i["stratum"] for i in items) == Counter(quota)
    assert all(all(i.get(k) not in (None, "") for k in ITEM_KEYS) for i in items)
    assert all(i["stratum"].split("|")[1] == i["type"] for i in items)
    assert all(i["stratum"].startswith(i["machine_verdict"]) for i in items)
    for i in items:
        near = i["evidence"]["aff_yes"] >= 4 and i["evidence"]["neg_no"] == 5
        if i["machine_verdict"] == "UNCERTAIN":
            assert i["stratum"].startswith("UNCERTAIN-near") == near


def _selftest() -> None:
    assert largest_remainder(200, list("abcdef")) == {"a": 34, "b": 34, "c": 33, "d": 33, "e": 33, "f": 33}
    fake = {f"{s}|t{j}": [{"image_id": str(i % 50), "file_name": f"{i}.jpg", "prop_id": f"P{s}{j}{i}",
                           "type": f"t{j}", "text_vi": "x", "machine_verdict": s.split("-")[0],
                           "evidence": {"aff_yes": 5 if s.endswith("near") else 0, "neg_no": 5}}
                          for i in range(40)]
            for s in ("SUPPORTED", "UNCERTAIN-near", "UNCERTAIN-rest", "REJECTED") for j in range(2)}
    quota = allocate(60, fake)
    assert sum(quota.values()) == 60 and quota["SUPPORTED|t0"] == 10
    items = draw(fake, quota, 1, 3)
    check({"n": 60, "items": items}, quota, 3)
    assert items == draw(fake, quota, 1, 3), "not deterministic for a fixed seed"


def main() -> None:
    ap = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    ap.add_argument("--records", required=True, type=Path, help="TRAINING Stage-1 records (stage1_neutral)")
    ap.add_argument("--out", type=Path, default=Path("data/annotations/audit_three_state_sample.json"))
    ap.add_argument("--n", type=int, default=600)
    ap.add_argument("--seed", type=int, default=42)
    ap.add_argument("--per-image", type=int, default=3)
    args = ap.parse_args()

    _selftest()
    pool = load_pool(args.records)
    quota = allocate(args.n, pool)
    items = draw(pool, quota, args.seed, args.per_image)
    sample = {
        "note": "C2 three-state audit: machine SUPPORTED / UNCERTAIN (near: affirm>=4/5 and "
                "negation 5/5; rest) / REJECTED x type, from TRAINING records, blind "
                "(shuffled; audit_props.py does not show machine_verdict).",
        "records": str(args.records), "seed": args.seed, "per_image": args.per_image,
        "n": len(items),
        "strata": {c: {"n": quota[c], "population": len(pool[c])} for c in sorted(quota)},
        "items": items,
    }
    check(sample, quota, args.per_image)
    args.out.parent.mkdir(parents=True, exist_ok=True)
    args.out.write_text(json.dumps(sample, ensure_ascii=False, indent=1), encoding="utf-8")
    print(f"{'stratum':34} {'n':>4} {'population':>11}")
    for c, v in sample["strata"].items():
        print(f"{c:34} {v['n']:>4} {v['population']:>11}")
    print(f"total {len(items)} propositions from {len({i['image_id'] for i in items})} images -> {args.out}")


if __name__ == "__main__":
    main()
