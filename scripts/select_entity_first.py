"""D1: entity-first selection over existing Stage-1 verdicts (offline, no GPU).

Phase 1 covers every distinct entity mentioned by a SUPPORTED proposition once;
phase 2 fills the remaining budget with the existing M5 objective. Scoring,
admissibility, tie-breaking and the invariant checks are `rescap.pipeline.select`'s.
The pool is SUPPORTED only (neutralized propositions carry status SUPPORTED):
UNCERTAIN and REJECTED never enter.

    python3 scripts/select_entity_first.py IN_DIR OUT_DIR --budget 9 [--cap 15]
    python3 scripts/select_entity_first.py IN_DIR OUT_DIR --budget 9 --method greedy
    python3 scripts/select_entity_first.py --selftest

`--cap N` makes the budget adaptive: B = min(N, max(budget, #distinct SUPPORTED
entities)). `--method greedy` is the control: the existing `select()` on
SUPPORTED + UNCERTAIN, exactly as scripts/build_dpo_data.py rung A calls it.
OUT_DIR receives copies of the records with `selected_ids` rewritten, plus
`short_ids` (the first two selected SUPPORTED ids in record order, which is what
build_dpo_data derives the short-mode target from).
"""

from __future__ import annotations

import argparse
import json
import statistics
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parents[1]))

from rescap.pipeline.select import (  # noqa: E402
    _EPS,
    _TIE_PRECISION,
    SelectionConfig,
    _mentioned_entities,
    _Selector,
    _verdict_of,
    select,
)


class EntityFirstSelector(_Selector):
    """`_Selector` whose greedy is preceded by a forced entity-coverage phase."""

    def _best(self, pool, selected, require_gain):
        """Highest marginal F gain in `pool`, using select.py's own tie-break."""
        base = self.objective(selected).total
        scored = []
        for c in pool:  # candidates are id-sorted, so max() keeps the lowest id on ties
            gain = self.objective(selected + [c.pid]).total - base
            if require_gain and gain <= _EPS:
                continue
            scored.append(((round(gain, _TIE_PRECISION),
                            round(c.factuality or 0.0, _TIE_PRECISION),
                            round(c.informativeness, _TIE_PRECISION)), c))
        return max(scored, key=lambda kc: kc[0])[1] if scored else None

    def run(self):
        selected: list[str] = []
        covered: set[str] = set()
        for phase_needs_new_entity in (True, False):
            while len(selected) < self.config.budget:
                pool = [c for c in self.candidates
                        if c.pid not in selected
                        and (not phase_needs_new_entity or c.entity_ids - covered)
                        and self._admissible(c, selected, 0)]
                # Phase 1 takes the best coverer even at non-positive gain: coverage is the guarantee.
                best = self._best(pool, selected, require_gain=not phase_needs_new_entity)
                if best is None:
                    break
                selected.append(best.pid)
                covered |= best.entity_ids
        return self.finalise(selected)


def supported_entities(props) -> set[str]:
    return set().union(set(), *(_mentioned_entities(p) for p in props if _verdict_of(p) == "SUPPORTED"))


def select_record(d: dict, budget: int, cap: int | None, method: str) -> tuple[list[str], int]:
    props, entities = d["propositions"], d.get("entities") or []
    if method == "greedy":
        pool = [p for p in props if _verdict_of(p) in ("SUPPORTED", "UNCERTAIN")]
        if not pool:
            return [], budget
        return select(pool, entities, config=SelectionConfig(budget=budget)).selected_ids, budget
    supported = [p for p in props if _verdict_of(p) == "SUPPORTED"]
    b = budget if cap is None else min(cap, max(budget, len(supported_entities(supported))))
    if not supported:
        return [], b
    sel = EntityFirstSelector(supported, entities, SelectionConfig(budget=b), None, None)
    return sel.run().selected_ids, b


def short_ids(d: dict, selected: list[str]) -> list[str]:
    """build_dpo_data: `[p for p in chosen_a if SUPPORTED][:2]`, chosen_a in record order."""
    keep = set(selected)
    return [p["id"] for p in d["propositions"]
            if _verdict_of(p) == "SUPPORTED" and p["id"] in keep][:2]


def main(argv=None) -> None:
    ap = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    ap.add_argument("src", type=Path)
    ap.add_argument("dst", type=Path)
    ap.add_argument("--budget", type=int, default=9)
    ap.add_argument("--cap", type=int, default=None)
    ap.add_argument("--method", choices=("entity_first", "greedy"), default="entity_first")
    a = ap.parse_args(argv)
    a.dst.mkdir(parents=True, exist_ok=True)
    n_sel, budgets, full_cover = [], [], []
    for f in sorted(a.src.glob("*.json")):
        d = json.loads(f.read_text(encoding="utf-8"))
        selected, b = select_record(d, a.budget, a.cap, a.method)
        sup = {p["id"]: p for p in d["propositions"] if _verdict_of(p) == "SUPPORTED"}
        chosen_sup = [sup[i] for i in selected if i in sup]
        ents = supported_entities(sup.values())
        if ents:
            full_cover.append(ents <= supported_entities(chosen_sup))
        n_sel.append(len(chosen_sup))
        budgets.append(b)
        d["selected_ids"], d["hedged_ids"] = selected, [i for i in selected if i not in sup]
        d["short_ids"], d["selection_budget"] = short_ids(d, selected), b
        (a.dst / f.name).write_text(json.dumps(d, ensure_ascii=False), encoding="utf-8")
    print(f"{a.method} budget={a.budget} cap={a.cap}: images={len(n_sel)} "
          f"mean_supported_selected={statistics.mean(n_sel):.2f} mean_B={statistics.mean(budgets):.2f} "
          f"all_supported_entities_covered={100 * statistics.mean(full_cover):.1f}%")


def _selftest() -> None:
    def prop(pid, ent, status, score, ptype="attribute"):
        return {"id": pid, "type": ptype, "subject": {"entity_id": ent}, "object": None,
                "text_vi": f"{ent} {pid}",
                "verification": {"status": status, "support_score": score, "contradiction_score": 0.0}}

    props = [prop(f"P{i}", "a", "SUPPORTED", 0.99) for i in range(1, 6)]
    props += [prop("P6", "b", "SUPPORTED", 0.3, "entity"), prop("P7", "c", "SUPPORTED", 0.3, "entity"),
              prop("P8", "d", "UNCERTAIN", 0.99, "entity"), prop("P9", "e", "REJECTED", 0.99, "entity")]
    d = {"propositions": props, "entities": [{"id": e} for e in "abcde"]}
    sel, b = select_record(d, budget=3, cap=None, method="entity_first")
    assert b == 3 and len(sel) == 3, (b, sel)
    assert {"P6", "P7"} <= set(sel), sel                     # b and c covered before a's 2nd attribute
    assert not {"P8", "P9"} & set(sel), sel                  # never UNCERTAIN / REJECTED
    assert supported_entities(props) == {"a", "b", "c"}
    _, b = select_record(d, budget=2, cap=15, method="entity_first")
    assert b == 3                                             # max(2, 3 entities)
    _, b = select_record(d, budget=1, cap=2, method="entity_first")
    assert b == 2                                             # capped
    sel, _ = select_record(d, budget=9, cap=None, method="entity_first")
    assert len(sel) == 7 and short_ids(d, sel) == ["P1", "P2"], sel
    print("selftest ok")


if __name__ == "__main__":
    if sys.argv[1:] == ["--selftest"]:
        _selftest()
    else:
        main()
