"""Single-probe scores and the three-state combiner (prereg §4.1-§4.3).

Per family f: s_f = p(yes) / (p(yes) + p(no)) at the answer position (M0 token sets: yes c/có, no kh/không).
Per family state: YES if s_f >= tau_acc, NO if s_f <= tau_rej, else UNSURE; a missing or NaN score is UNSURE.
Combined: SUPPORTED if any family says YES; REJECTED only if every declared family says NO; else UNCERTAIN.
With all scores present this equals §4.2 (max_f s_f >= tau_acc / max_f s_f <= tau_rej). Spatial relations are
always UNCERTAIN. Torch is imported only inside probe_model().
"""
from __future__ import annotations

import copy
import math
import statistics

SUPPORTED, UNCERTAIN, REJECTED = "SUPPORTED", "UNCERTAIN", "REJECTED"
TAU_ACC = (0.50, 0.60, 0.70, 0.80, 0.90)
TAU_REJ = (0.10, 0.20, 0.30)
FAMILY_SETS = (("vintern",), ("vintern", "internvl3"))
FAIR_MODEL = "5CD-AI/Vintern-1B-v3_5"  # erratum E3: the string in evidence.probes = m0.MODEL["repo"] = E1b VIN (test-pinned)
ALWAYS_UNCERTAIN = ("spatial_relation",)
MASS_FLOOR, SMOKE_N = 0.5, 20


def grid() -> list[tuple[float, float, tuple[str, ...]]]:
    """The 30 candidate operating points of §4.3, in a fixed order (families, tau_acc, tau_rej)."""
    return [(a, r, f) for f in FAMILY_SETS for a in TAU_ACC for r in TAU_REJ]


def score(p_yes: float, p_no: float) -> float:
    """s = p(yes) / (p(yes) + p(no)); NaN when the yes+no mass is 0 (as m0.probe)."""
    mass = p_yes + p_no
    return p_yes / mass if mass > 0 else float("nan")


def smoke_ok(masses: list[float]) -> bool:
    """Smoke rule: median yes+no mass over the first 20 probes >= 0.5."""
    first = masses[:SMOKE_N]
    return len(first) == SMOKE_N and statistics.median(first) >= MASS_FLOOR


def family_state(s: float | None, tau_acc: float, tau_rej: float) -> str:
    if s is None or (isinstance(s, float) and math.isnan(s)):
        return "UNSURE"
    return "YES" if s >= tau_acc else "NO" if s <= tau_rej else "UNSURE"


def combine(scores: dict[str, float | None], families: tuple[str, ...], tau_acc: float, tau_rej: float,
            ptype: str = "entity") -> str:
    """Three-state verdict of one proposition from its per-family scores (families not in `scores` are missing)."""
    if not tau_rej < tau_acc:
        raise ValueError(f"tau_rej {tau_rej} must be < tau_acc {tau_acc}")
    if ptype in ALWAYS_UNCERTAIN:
        return UNCERTAIN
    states = [family_state(scores.get(f), tau_acc, tau_rej) for f in families]
    if "YES" in states:
        return SUPPORTED
    if states and all(s == "NO" for s in states):
        return REJECTED
    return UNCERTAIN


def qkey(q: str) -> str:
    """rescap.vlm.replay.ReplayVLM._key (= e1e2.qkey): the join key between records and probe rows."""
    return " ".join(q.strip().rstrip("?.").split()).lower()


def affirmative_key(prop: dict, model: str = FAIR_MODEL) -> str | None:
    """Q+ of a proposition: the first recorded probe of the FAIR verifier (verify._probe_record writes the direct
    question before the negated one). None when the proposition carries no such probe."""
    for q in (prop.get("evidence") or {}).get("probes") or []:
        if str(q.get("model", "")) == model and q.get("question_vi"):
            return qkey(q["question_vi"])
    return None


def apply_states(rec: dict, tables: dict[str, dict[str, float]], families: tuple[str, ...], tau_acc: float,
                 tau_rej: float) -> tuple[dict, dict]:
    """Deep copy of a stage-1 record with every proposition's verification.status set by combine().
    tables: {family: {qkey: s}} for this image. Erratum E3: a proposition with no Q+ keeps its recorded status.
    Returns (record, counts): states after the step, no_q, no_q_not_rejected (the K0 driver refuses these) and
    miss = Q+ keys absent from a used family's table (the K0 driver refuses them, E2)."""
    out = copy.deepcopy(rec)
    n = {SUPPORTED: 0, UNCERTAIN: 0, REJECTED: 0, "no_q": 0, "no_q_not_rejected": 0, "miss": 0}
    for p in out["propositions"]:
        k = affirmative_key(p)
        if k is None:
            st = (p.get("verification") or {}).get("status")
            n["no_q"] += 1
            n["no_q_not_rejected"] += st != REJECTED
            n[st] = n.get(st, 0) + 1
            continue
        sc = {f: tables.get(f, {}).get(k) for f in families}
        n["miss"] += sum(v is None for v in sc.values())
        st = combine({f: v for f, v in sc.items() if v is not None}, families, tau_acc, tau_rej, p.get("type", ""))
        p.setdefault("verification", {})["status"] = st
        n[st] += 1
    return out, n


def probe_model(*_a, **_k):  # pragma: no cover - GPU host only, after the prereg commit
    """InternVL3-8B / Vintern single-probe runner. Not run before the commit (CC-501 ruling 6)."""
    import torch  # noqa: F401
    raise NotImplementedError("probe runner: written and run on the host after the prereg commit")
