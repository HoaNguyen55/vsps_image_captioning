#!/usr/bin/env python
"""D2: relation -> entity backoff, recovering object existence from SAVED evidence.

    python scripts/relation_backoff.py --in <stage1_dir> --out <dir> --level strict|lenient
    python scripts/relation_backoff.py --self-check

Finding (KE_HOACH_Q2 Ket luan 3): objects reachable only through an UNCERTAIN
relation/spatial_relation with grounding >= 0.9 match the references about as
well as SUPPORTED ones. Most of those relations are UNCERTAIN because of a
ceiling (missing box, unconfirmed argument existence), not because the probe
answers disagree. The relation itself stays UNCERTAIN. The backoff drops it and
keeps only what the evidence covers: that its argument entities exist.

Why the relation's evidence speaks to existence: the direct probe "does X <rel> Z?"
answered yes in EVERY sample presupposes that X and Z are in the image, and the
negated probe "is it true X does NOT <rel> Z?" answered no in EVERY sample means
the yes was not acquiescence bias. A high grounding_score on its own is not
enough: it is a score built from those same answers, so the probe unanimity is
required at both levels. The relation still never settles existence by itself.
The entity's own existence proposition has to agree too, and the level says how
strongly.

BACKOFF CRITERIA (pre-registered, machine-readable, no explanation-text parsing,
no re-querying of any model). For each relation/spatial_relation R and each
argument entity A (subject, object):
 R1. R.verification.status == UNCERTAIN and R.external_knowledge.inference_type
     in {none, None};
 R2. R's evidence is unanimous: direct probe all-yes, negated probe all-no,
     R.grounding_score >= tau;
 E1. A has an existence proposition P_A whose status is UNCERTAIN (never
     SUPPORTED, which is already counted, and never REJECTED) and whose
     inference_type is in {none, None};
 E2 strict:  P_A's own evidence is unanimous (both probes, P_A.grounding >= tau),
             so two independent probe families agree on existence;
 E2 lenient: P_A's own evidence is not against it: a strict majority of the
             direct samples say yes AND a strict majority of the negated
             samples say no (this excludes acquiescence and disagreement).
 T.  The derived text is the bare noun phrase of P_A: leading quantifier
     dropped (no count), cut at the first relational / attribute word (no
     attribute or second object), gendered nouns neutralised (person_uncap).
All met: a NEW entity proposition `<P_A.id>~rb` with status SUPPORTED, trace
`backoff{kind:"relation_to_entity", level, tau, entity_proposition_id,
source_relation_ids, original_text_vi, relation_grounding, entity_grounding}`.
One per entity, however many relations reach it. R and P_A are left untouched
and selected_ids is not changed. The input directory is immutable.
"""

from __future__ import annotations

import argparse
import copy
import json
import re
import sys
from collections import Counter
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))
from person_uncap import _GENDER_RE, _NO, _YES, neutralise  # noqa: E402

RELATION_TYPES = ("relation", "spatial_relation")

_QUANT_RE = re.compile(
    r"^(?:(?:một số|một nhóm|một vài|một|hai|ba|bốn|năm|sáu|bảy|tám|chín|mười"
    r"|nhiều|vài|các|những|mấy|\d+)\s+)+"
)
_CUT_WORDS = (
    "trên", "dưới", "trong", "ngoài", "bên", "cạnh", "với", "của", "đang", "có",
    "màu", "ở", "phía", "gần", "sau", "trước", "giữa", "và", "đầy", "được",
    "làm", "khác", "đỏ", "vàng", "trắng", "đen", "hồng", "tím", "cam", "nâu",
    "xám", "xanh lá", "xanh dương", "xanh lam", "lớn", "nhỏ", "to", "cao", "thấp",
    "dài", "ngắn", "cũ", "mới", "mặc", "đeo", "cầm", "đội", "xách", "mang",
)
_CUT_RE = re.compile(r"(?:\s+(?:" + "|".join(_CUT_WORDS) + r")\b|\s*[\"'“(,:;.]).*$")


def bare_noun_phrase(text: str) -> str:
    out = _QUANT_RE.sub("", text.strip().lower())
    out = _CUT_RE.sub("", out)
    return neutralise(out).strip(" ,.")


def _share(probe: dict, heads: tuple[str, ...]) -> float:
    samples = probe.get("samples") or [probe.get("answer")]
    hits = sum(
        any(str(s or "").strip().lower().startswith(h) for h in heads) for s in samples
    )
    return hits / len(samples) if samples else 0.0


def _probe_shares(p: dict) -> tuple[float, float] | None:
    """(yes share of the direct probe, no share of the negated probe).

    Probes are told apart by the question, not by `polarity`, which is the
    parsed ANSWER: a direct all-no plus negated all-yes would otherwise pass.
    """
    probes = (p.get("evidence") or {}).get("probes") or []
    direct = next((q for q in probes if "KHÔNG" not in str(q.get("question_vi"))), None)
    negated = next((q for q in probes if "KHÔNG" in str(q.get("question_vi"))), None)
    if direct is None or negated is None:
        return None
    return _share(direct, _YES), _share(negated, _NO)


def _grounding(p: dict) -> float:
    g = ((p.get("evidence") or {}).get("visual_grounding") or {}).get("grounding_score")
    return float(g) if g is not None else 0.0


def unanimous(p: dict, tau: float) -> bool:
    return _probe_shares(p) == (1.0, 1.0) and _grounding(p) >= tau


def not_against(p: dict) -> bool:
    shares = _probe_shares(p)
    return shares is not None and shares[0] > 0.5 and shares[1] > 0.5


def _no_inference(p: dict) -> bool:
    ek = (p.get("evidence") or {}).get("external_knowledge") or {}
    return ek.get("inference_type") in (None, "none")


def _status(p: dict) -> str | None:
    return (p.get("verification") or {}).get("status")


def backoff_record(rec: dict, level: str, tau: float) -> list[dict]:
    """Append derived existence propositions to `rec` in place; return them."""
    props = rec.get("propositions") or []
    existence: dict[str, dict] = {}
    for p in props:
        eid = (p.get("subject") or {}).get("entity_id")
        if p.get("type") == "entity" and eid and eid not in existence:
            existence[str(eid)] = p
    sources: dict[str, list[dict]] = {}
    for r in props:
        if r.get("type") not in RELATION_TYPES or _status(r) != "UNCERTAIN":
            continue
        if not (_no_inference(r) and unanimous(r, tau)):
            continue
        for role in ("subject", "object"):
            eid = (r.get(role) or {}).get("entity_id")
            if eid:
                sources.setdefault(str(eid), []).append(r)

    entity_ok = (lambda e: unanimous(e, tau)) if level == "strict" else not_against
    derived: list[dict] = []
    for eid, rels in sources.items():
        ent = existence.get(eid)
        if ent is None or _status(ent) != "UNCERTAIN" or not _no_inference(ent):
            continue
        if not entity_ok(ent):
            continue
        text = bare_noun_phrase(str(ent.get("text_vi") or ""))
        if not text:
            continue
        head = neutralise(str((ent.get("subject") or {}).get("head_noun_vi") or ""))
        rel_ids = sorted({str(r.get("id")) for r in rels})
        derived.append({
            "id": f"{ent.get('id')}~rb",
            "type": "entity",
            "subject": {"entity_id": eid, "text_vi": text, "head_noun_vi": head},
            "predicate": {"lemma_vi": "có"},
            "object": None,
            "attributes": [],
            "spatial_relation": None,
            "text_vi": text,
            "epistemic": "OBSERVATION",
            "evidence": copy.deepcopy(ent.get("evidence")),
            "verification": {
                "status": "SUPPORTED",
                "explanation_vi": (
                    f"Lùi quan hệ về thực thể (D2, {level}): quan hệ {', '.join(rel_ids)} "
                    "có bằng chứng nhất trí cả hai chiều nên các đối tượng tham gia tồn tại; "
                    "bản thân quan hệ vẫn UNCERTAIN và bị bỏ."
                ),
                "explanation_en": (
                    f"Relation-to-entity backoff (D2, {level}): relation(s) {', '.join(rel_ids)} "
                    "have unanimous two-way evidence, so their arguments exist; the relation "
                    "itself stays UNCERTAIN and is dropped."
                ),
                "verifier": "offline backoff over saved stage-1 evidence",
                "decision_rule_version": f"relation_backoff-v1+level={level}+tau={tau}",
            },
            "backoff": {
                "kind": "relation_to_entity",
                "level": level,
                "tau": tau,
                "entity_proposition_id": ent.get("id"),
                "source_relation_ids": rel_ids,
                "original_text_vi": ent.get("text_vi"),
                "relation_grounding": max(_grounding(r) for r in rels),
                "entity_grounding": _grounding(ent),
            },
        })
    props.extend(derived)
    return derived


def _probe(question: str, samples: list[str]) -> dict:
    return {"question_vi": question, "samples": samples, "answer": samples[0]}


def _prop(pid, ptype, status, text, evidence, ids=(None, None)) -> dict:
    direct, negated, g = evidence
    subj, obj = ids
    return {
        "id": pid, "type": ptype, "text_vi": text,
        "subject": {"entity_id": subj, "text_vi": text, "head_noun_vi": text},
        "object": {"entity_id": obj} if obj else None,
        "evidence": {
            "external_knowledge": {"inference_type": "none"},
            "probes": [_probe("Trong ảnh có X không", direct),
                       _probe("Có đúng là KHÔNG có X không", negated)],
            "visual_grounding": {"grounding_score": g},
        },
        "verification": {"status": status},
    }


def self_check() -> None:
    y, n = ["Có."] * 5, ["Không."] * 5
    mixed = ["Có.", "Có.", "Có.", "Không.", "Có."]
    rec = {"propositions": [
        _prop("P1", "entity", "UNCERTAIN", "Một người đàn ông", (y, n, 0.95), ("a", None)),
        _prop("P2", "entity", "UNCERTAIN", "hai chiếc thuyền trên sông", (mixed, n, 0.6), ("b", None)),
        _prop("P3", "entity", "SUPPORTED", "một cái bàn", (y, n, 0.95), ("c", None)),
        _prop("P4", "entity", "UNCERTAIN", "một con chó", (n, y, 0.0), ("d", None)),
        _prop("R1", "relation", "UNCERTAIN", "người đẩy thuyền", (y, n, 0.92), ("a", "b")),
        _prop("R2", "spatial_relation", "UNCERTAIN", "bàn cạnh chó", (y, n, 0.95), ("c", "d")),
        _prop("R3", "relation", "UNCERTAIN", "người cầm bàn", (y, n, 0.5), ("a", "c")),
    ]}
    before = json.dumps(rec, sort_keys=True)
    strict = backoff_record(copy.deepcopy(rec), "strict", 0.9)
    lenient = backoff_record(copy.deepcopy(rec), "lenient", 0.9)
    assert json.dumps(rec, sort_keys=True) == before, "input mutated"
    assert [d["subject"]["entity_id"] for d in strict] == ["a"], strict
    assert sorted(d["subject"]["entity_id"] for d in lenient) == ["a", "b"], lenient
    texts = {d["subject"]["entity_id"]: d["text_vi"] for d in lenient}
    assert texts == {"a": "người", "b": "chiếc thuyền"}, texts
    assert all(d["verification"]["status"] == "SUPPORTED"
               and d["backoff"]["kind"] == "relation_to_entity" for d in lenient)
    assert lenient[0]["backoff"]["source_relation_ids"] == ["R1"]
    assert bare_noun_phrase("Một bức tranh trên tường") == "bức tranh"
    assert bare_noun_phrase("một số người khác") == "người"
    assert bare_noun_phrase("Hai chiếc xe máy màu đỏ") == "chiếc xe máy"
    assert bare_noun_phrase("nhiều cây xanh") == "cây xanh"
    assert bare_noun_phrase("Một người phụ nữ mặc áo hồng") == "người"
    assert bare_noun_phrase('một bức tranh chữ "Hoi An"') == "bức tranh chữ"
    assert bare_noun_phrase("ánh sáng xanh lá cây") == "ánh sáng"
    assert bare_noun_phrase("một tòa nhà cao tầng trong ảnh, một biển") == "tòa nhà"
    # direct all-no + negated all-yes must not pass, whatever `polarity` says
    assert not unanimous(_prop("X", "relation", "UNCERTAIN", "x", (n, y, 0.99)), 0.9)
    print("self-check OK")


def main() -> int:
    ap = argparse.ArgumentParser(description=__doc__,
                                 formatter_class=argparse.RawDescriptionHelpFormatter)
    ap.add_argument("--in", dest="src")
    ap.add_argument("--out", dest="dst")
    ap.add_argument("--level", choices=("strict", "lenient"), default="strict")
    ap.add_argument("--tau", type=float, default=0.9)
    ap.add_argument("--self-check", action="store_true")
    args = ap.parse_args()
    if args.self_check:
        self_check()
        return 0
    if not (args.src and args.dst):
        ap.error("--in and --out are required")

    src = Path(args.src).expanduser().resolve()
    dst = Path(args.dst).expanduser().resolve()
    if src == dst:
        ap.error("--out must differ from --in (the input directory is immutable)")
    dst.mkdir(parents=True, exist_ok=True)

    stats: Counter[str] = Counter()
    for f in sorted(src.glob("*.json")):
        rec = json.loads(f.read_text(encoding="utf-8"))
        stats["records"] += 1
        derived = backoff_record(rec, args.level, args.tau)
        for d in derived:
            assert not _GENDER_RE.search(d["text_vi"]), d["text_vi"]
        if derived:
            stats["records_changed"] += 1
            stats["recovered"] += len(derived)
            stats["source_relations"] += len(
                {r for d in derived for r in d["backoff"]["source_relation_ids"]})
        (dst / f.name).write_text(json.dumps(rec, ensure_ascii=False), encoding="utf-8")

    print(json.dumps({"level": args.level, "tau": args.tau, **stats}, ensure_ascii=False, indent=1))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
