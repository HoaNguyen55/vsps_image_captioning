"""Supervision store rebuild (prereg §4.4): FAIR's builder unchanged, detailed budget scaled per image.

B_i = clip(ceil(1.5 * n_SUPP_entities(i)), 5, 15); S1 (OP_strict) keeps B = 9. n_SUPP_entities(i) = number of
distinct subject entity ids among the image's SUPPORTED propositions of type `entity` (a proposition without an
entity id counts by its own id). The builder is scripts/build_dpo_data.py build_for_image, called unchanged with the
FAIR flags (--style-variation --clean-props, detailed variant B); the variant-B pick replicates its main()
(l.660-679, sha 9ef1e8fc). Erratum E4 order, every arm: statuses (recorded for S1, O31 combiner otherwise) ->
person_uncap (scripts/person_uncap.py main(), unchanged, default types, on temp dirs) -> build. n_SUPP_entities is
counted after the uncap (E5).
"""
from __future__ import annotations

import copy
import math
from collections import Counter

from . import repo

K_SCALE, B_MIN, B_MAX, B_FAIR = 1.5, 5, 15, 9
DETAILED_MARK = "Mô tả chi tiết"  # recall_funnel.py reads detailed rows by this prompt prefix


def n_supp_entities(rec: dict) -> int:
    ids = {str((p.get("subject") or {}).get("entity_id") or f"p:{p.get('id')}")
           for p in rec.get("propositions") or []
           if p.get("type") == "entity" and (p.get("verification") or {}).get("status") == "SUPPORTED"}
    return len(ids)


def budget(n: int) -> int:
    return min(B_MAX, max(B_MIN, math.ceil(K_SCALE * n)))


def variant_b(sft: dict | None, pairs: list[dict], stats: Counter) -> dict | None:
    """build_dpo_data.main() --detailed-variant B, verbatim logic."""
    if not sft:
        return None
    b_text = next((p["rejected"] for p in pairs if p["pair_type"].startswith("A>B")), None) or \
        next((p["chosen"] for p in pairs if p["pair_type"].startswith("B>C")), None)
    if b_text:
        stats["sft_detailed_B"] += 1
        return dict(sft, response=b_text, variant_detailed="B")
    if sft.get("n_uncertain", 0) == 0:
        stats["sft_detailed_B_equals_A"] += 1
        return dict(sft, variant_detailed="B_equals_A")
    stats["skipped_no_rung_B"] += 1
    return None


def fair_builder():
    """build_dpo_data.build_for_image with the FAIR flags set; returns f(record, budget) -> (sft, short, pairs)."""
    repo()
    import build_dpo_data as bd

    bd.STYLE_VARIATION[0] = True
    bd.CLEAN_PROPS[0] = True
    stats: Counter = Counter()

    def build(rec: dict, b: int):
        bd.SELECT_BUDGET[0] = b
        return bd.build_for_image(rec, stats)
    build.stats = stats
    return build


def rebuild(records: list[dict], scaled: bool, build=None, min_supported: int = 1) -> tuple[list[dict], dict]:
    """Store rows (detailed variant B + short) of every record, and a report with per-image budgets and counts.
    scaled=False is S1's fixed B = 9. `build` defaults to fair_builder()."""
    build = build or fair_builder()
    stats: Counter = Counter()
    rows, budgets = [], {}
    for rec in records:
        n_sup = sum((p.get("verification") or {}).get("status") == "SUPPORTED" for p in rec.get("propositions") or [])
        if n_sup < min_supported:
            stats["skipped_too_few_supported"] += 1
            continue
        b = budget(n_supp_entities(rec)) if scaled else B_FAIR
        budgets[str(rec.get("image_id"))] = b
        sft, short, pairs = build(copy.deepcopy(rec), b)  # the builder edits some proposition dicts in place
        sft = variant_b(sft, pairs, stats)
        rows += [r for r in (sft, short) if r]
    stats["rows"] = len(rows)
    stats["detailed_rows"] = sum(DETAILED_MARK in r["prompt"] for r in rows)
    return rows, {"counts": dict(stats), "budgets": budgets}


def uncap(records: list[dict]) -> tuple[list[dict], dict]:
    """FAIR person_uncap.main() unchanged (default --types) on a temp copy of `records`; returns (records, its stats).
    A record that already carries a gender_uncap backoff is a FAULT (E4: the input must be pre-neutralization)."""
    import contextlib
    import io
    import json
    import sys
    import tempfile
    from pathlib import Path

    for r in records:
        if any((p.get("backoff") or {}).get("kind") == "gender_uncap" for p in r.get("propositions") or []):
            raise SystemExit(f"FAULT record {r.get('image_id')} already carries a gender_uncap backoff")
    repo()
    import person_uncap

    with tempfile.TemporaryDirectory(prefix="o31_uncap_") as d:
        src, dst = Path(d) / "in", Path(d) / "out"
        src.mkdir()
        for i, r in enumerate(records):
            (src / f"{i:07d}.json").write_text(json.dumps(r, ensure_ascii=False), encoding="utf-8")
        argv, sys.argv = sys.argv, ["person_uncap.py", "--in", str(src), "--out", str(dst)]
        buf = io.StringIO()
        try:
            with contextlib.redirect_stdout(buf):
                rc = person_uncap.main()
        finally:
            sys.argv = argv
        if rc != 0:
            raise SystemExit(f"FAULT person_uncap exit {rc}")
        out = [json.loads((dst / f"{i:07d}.json").read_text(encoding="utf-8")) for i in range(len(records))]
    text = buf.getvalue()
    stats = json.loads(text[:text.index("=== UNCAP")])
    return out, stats


def store_bytes(rows: list[dict], seed: int = 42) -> bytes:
    """sft.jsonl as build_dpo_data.main() writes it (random.Random(42) shuffle)."""
    import json
    import random

    rows = list(rows)
    random.Random(seed).shuffle(rows)
    return "".join(json.dumps(r, ensure_ascii=False) + "\n" for r in rows).encode("utf-8")


def store_sha(rows: list[dict]) -> str:
    import hashlib

    return hashlib.sha256(store_bytes(rows)).hexdigest()


def write_store(rows: list[dict], out_dir) -> str:
    """Write sft.jsonl; returns its sha256 (E5: the arm trains on these exact bytes)."""
    from pathlib import Path

    Path(out_dir).mkdir(parents=True, exist_ok=True)
    b = store_bytes(rows)
    (Path(out_dir) / "sft.jsonl").write_bytes(b)
    import hashlib

    return hashlib.sha256(b).hexdigest()


def detailed_captions(rows: list[dict]) -> dict:
    """{image_id: detailed response}, as recall_funnel.py reads the store."""
    return {r["image_id"]: r["response"] for r in rows if DETAILED_MARK in r["prompt"]}
