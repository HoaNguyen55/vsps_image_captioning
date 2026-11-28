"""A-8 store (ERRATUM_O31_5 E-B6; CODE_NEEDS C13): FAIR's recorded verdicts with the scaled budget B_i of §4.4.

Order of ERRATUM_O31_1 E4: recorded statuses (no O31 verdict is applied) -> person_uncap -> store.rebuild(scaled=True),
written as the E5 store with its sha256, and the K0 funnel numbers. This is run_k0's S1 arm with the budget as the
only difference; run_k0 itself is not changed. A separate CPU call after P1, on the same raw records P1 reads.
"""
from __future__ import annotations

from pathlib import Path

from . import gate, store


def arm_store(records: list[dict], scaled: bool, name: str, store_dir: Path | None, build=None) -> dict:
    """run_k0's arm() on recorded statuses: person_uncap -> rebuild -> funnel; the store sha is that of the written
    sft.jsonl when store_dir is given (E5)."""
    unc, ust = store.uncap(records)
    rows, rep = store.rebuild(unc, scaled=scaled, build=build)
    sha = store.write_store(rows, Path(store_dir) / name) if store_dir else store.store_sha(rows)
    return {**gate.store_funnel(records, store.detailed_captions(rows)), "rows": len(rows), "store": name,
            "sft_sha256": sha, "uncap": ust,
            "mean_budget": sum(rep["budgets"].values()) / max(len(rep["budgets"]), 1)}


def a8_store(records: list[dict], store_dir: Path | None, build=None) -> dict:
    """E-B6 A-8: recorded statuses, scaled budget."""
    return arm_store(records, True, "A8", store_dir, build)
