#!/usr/bin/env python
"""D3 — offline backoff beyond gender, on SAVED stage-1 evidence (no re-query).

    python scripts/extra_backoff.py --in <stage1_neutral> --out <dir> \
        [--ops colour,count,infer_artifact,prereq] [--link-unchanged]
    python scripts/extra_backoff.py --selfcheck

Same contract as scripts/person_uncap.py: pre-registered criteria, the input
directory is immutable, every flip carries `backoff{kind, ops, original_text_vi,
cleared}`. A proposition flips UNCERTAIN -> SUPPORTED only when EVERY doubt the
verifier recorded for it is cleared by an enabled operator, and the stored
probes give unanimous support (every sample, tau = 0.9 over 5 samples) for the
claim that remains after coarsening.

Doubts are read from the verifier's templated `explanation_en` (verify.py emits
one fixed string per ceiling, so this is a categorical field, not free text).
Any doubt not in the table below blocks the flip.

OPERATORS (each separately switchable)
  colour  — doubt "colour verifiers disagree" or "bare 'xanh' unresolved".
            Specific xanh hue -> "xanh". Specific => coarse (blue ⊂ xanh), so a
            unanimous yes to "X xanh dương" supports "X xanh". For a
            disagreement the remaining claim is supported by the AFFIRMING
            verifier's unanimous yes; the refuting verifier denied the specific
            hue, which does not deny xanh (doc: Vintern's colour errors all
            fall on the blue/green pair). Not applied when the value holds no
            specific hue (the dispute is then about xanh itself = the coarse
            part) or names any non-xanh colour (dispute may be about that one).
            For bare-xanh both verifiers must be unanimous: the probes asked
            the claim as written, which already is (or implies) the coarse one.
  count   — doubt "exact count above 5". Leading numeral -> "nhiều". "exactly
            N, N > 5" => "many". Only the cap case: when resamples disagree the
            doubt is the count itself and nothing stored probes "nhiều".
  infer_artifact — doubt "inference beyond what is visible" whose INFERENCE tag
            comes from generate.classify_epistemic's SUBSTRING match of a
            gendered noun inside a non-gendered word (bàn ⊃ bà, tranh/xanh ⊃
            anh, sông/thông/công ⊃ ông). Cleared iff no gendered noun occurs as
            a whole word and inference_type is "none". Text unchanged.
  prereq  — doubt "existence of E is itself unconfirmed" where E's existence
            proposition is now SUPPORTED (gender_uncap upstream, or
            infer_artifact here). Mirrors verify.py's cascade exactly. If E was
            gender-neutralised the dependent text is neutralised too.

Hypernym backoff (breed/species -> parent) is NOT implemented: in the 3,700
records every UNCERTAIN species claim with unanimous evidence is capped by the
infer_artifact bug (cây thông ⊃ ông), and the rest are resample disagreement
on the specific noun, where no stored probe asks about the parent.
"""

from __future__ import annotations

import argparse
import json
import os
import re
import sys
from collections import Counter
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent.parent))
sys.path.insert(0, str(Path(__file__).resolve().parent))
from person_uncap import _NO, _YES, neutralise  # noqa: E402
from rescap.vi.lexicon import (  # noqa: E402
    COLORS, EXACT_COUNT_LIMIT, GENDERED_NOUNS, NON_VISUAL_MARKERS, NUMERALS,
    XANH_BLUE, XANH_GREEN,
)

TAU = 0.9
OPS = ("colour", "count", "infer_artifact", "prereq")
PRECAP = "Supported by visual evidence."
XANH_UNRESOLVED = "Not enough evidence to decide (bare 'xanh' could not be resolved to blue or green)."

_HUES = sorted(XANH_BLUE | XANH_GREEN, key=len, reverse=True)
_HUE_RE = re.compile(r"\b(" + "|".join(_HUES) + r")\b")
_OTHER_COLOUR_RE = re.compile(
    r"\b(" + "|".join(sorted(COLORS - XANH_BLUE - XANH_GREEN, key=len, reverse=True)) + r")\b")
_GENDER_WORD_RE = re.compile(
    r"\b(" + "|".join(sorted(GENDERED_NOUNS, key=len, reverse=True)) + r")\b")
_NUM_RE = re.compile(
    r"^\s*((?:" + "|".join(NUMERALS) + r"|mươi|\d+)(?:\s+(?:" + "|".join(NUMERALS) + r"|mươi))*)\b",
    re.IGNORECASE)


def doubts(v: dict) -> tuple[list, bool]:
    """(doubt keys, pre-cap verdict was SUPPORTED). Unknown doubt -> 'other'."""
    e = str(v.get("explanation_en") or "")
    if e == XANH_UNRESOLVED:
        return ["xanh_unresolved"], True
    if not e.startswith(PRECAP + " Capped at UNCERTAIN because "):
        return ["other"], False
    out = []
    for r in e.split("because ", 1)[1].rstrip(".").split("; "):
        m = re.fullmatch(r"the existence of (\S+) is itself unconfirmed", r)
        if m:
            out.append(("exists", m.group(1)))
        elif r.startswith("colour verifiers disagree"):
            out.append("colour_disagree")
        elif r.startswith("an exact count above"):
            out.append("count_gt5")
        elif r == "the claim rests on inference beyond what is visible":
            out.append("inference")
        else:
            out.append("other")
    return out, True


def _frac(samples: list, heads: tuple) -> float:
    ts = [str(s or "").strip().lower() for s in samples]
    return sum(any(t.startswith(h) for h in heads) for t in ts) / len(ts) if ts else 0.0


def model_support(p: dict) -> dict:
    """model -> min(frac 'yes' to the claim, frac 'no' to its negation)."""
    by: dict = {}
    for q in (p.get("evidence") or {}).get("probes") or []:
        samples = q.get("samples") or [q.get("answer")]
        neg = "KHÔNG" in str(q.get("question_vi"))
        by.setdefault(q.get("model"), {})["neg" if neg else "dir"] = _frac(samples, _NO if neg else _YES)
    return {m: min(d.get("dir", 0.0), d.get("neg", 0.0)) for m, d in by.items()}


def colour_value(p: dict) -> str:
    return " ".join(str(a.get("value_vi") or "") for a in p.get("attributes") or []
                    if a.get("kind") == "màu_sắc").lower()


def coarsen_hue(text: str) -> str:
    return _HUE_RE.sub("xanh", text)


def coarsen_count(text: str) -> str:
    return _NUM_RE.sub("nhiều", text, count=1)


def is_infer_artifact(p: dict) -> bool:
    low = str(p.get("text_vi") or "").lower()
    ek = (p.get("evidence") or {}).get("external_knowledge") or {}
    return (ek.get("inference_type") in (None, "none")
            and not _GENDER_WORD_RE.search(low)
            and not any(m in low for m in NON_VISUAL_MARKERS))


def try_flip(p: dict, ops: set, entity_ok: dict, neutral_ents: set) -> tuple[str, list] | None:
    """New text + operators used, or None. Pure: does not mutate p."""
    v = p.get("verification") or {}
    if v.get("status") != "UNCERTAIN":
        return None
    ds, precap = doubts(v)
    if not precap:
        return None
    sup = model_support(p)
    g = ((p.get("evidence") or {}).get("visual_grounding") or {}).get("grounding_score")
    text, used, colour_disputed = str(p.get("text_vi") or ""), [], False
    for d in ds:
        if d in ("colour_disagree", "xanh_unresolved") and "colour" in ops:
            val = colour_value(p)
            if d == "colour_disagree" and (not _HUE_RE.search(val) or _OTHER_COLOUR_RE.search(val)):
                return None
            colour_disputed |= d == "colour_disagree"
            text, used = coarsen_hue(text), used + ["colour"]
        elif d == "count_gt5" and "count" in ops:
            n = (p.get("count") or {}).get("value")
            new = coarsen_count(text)
            if not (isinstance(n, int) and n > EXACT_COUNT_LIMIT) or new == text:
                return None
            text, used = new, used + ["count"]
        elif d == "inference" and "infer_artifact" in ops and is_infer_artifact(p):
            used.append("infer_artifact")
        elif isinstance(d, tuple) and "prereq" in ops and entity_ok.get(d[1]):
            if d[1] in neutral_ents:
                text = neutralise(text)
            used.append("prereq")
        else:
            return None
    # Bare-xanh doubts are not ceilings: verify.py never states the hidden ones,
    # so re-derive the prerequisite structurally.
    if "xanh_unresolved" in ds:
        eid = (p.get("subject") or {}).get("entity_id")
        if p.get("type") != "entity" and eid and eid in entity_ok and not entity_ok[eid]:
            return None
        if ((p.get("evidence") or {}).get("external_knowledge") or {}).get("requires_inference"):
            return None
    if not sup:
        return None
    if colour_disputed:  # remaining claim rests on the affirming verifier
        if max(sup.values()) < TAU:
            return None
    else:
        if min(sup.values()) < TAU or g is None or float(g) < TAU:
            return None
    return text, sorted(set(used))


def process(rec: dict, ops: set, types: set, stats: Counter) -> bool:
    props = rec.get("propositions") or []
    exist = {}
    for p in props:
        if p.get("type") == "entity":
            exist.setdefault((p.get("subject") or {}).get("entity_id"), p)
    neutral_ents = {eid for eid, p in exist.items()
                    if (p.get("backoff") or {}).get("kind") == "gender_uncap"}
    changed = False
    entity_ok: dict = {}
    # Entities first: their verdicts feed the prerequisite cascade.
    for phase in ("entity", "rest"):
        if phase == "rest":
            entity_ok = {eid: (p.get("verification") or {}).get("status") == "SUPPORTED"
                         for eid, p in exist.items()}
        for p in props:
            if (p.get("type") == "entity") != (phase == "entity") or p.get("type") not in types:
                continue
            r = try_flip(p, ops, entity_ok, neutral_ents)
            if r is None:
                continue
            text, used = r
            v = p["verification"]
            p["backoff"] = {"kind": "+".join(used), "ops": used,
                            "original_text_vi": p.get("text_vi"),
                            "cleared": v.get("explanation_en")}
            p["text_vi"] = text
            if "count" in used:
                p["count"] = {**(p.get("count") or {}), "exact": False, "marker": "nhiều"}
            v["status"] = "SUPPORTED"
            v["explanation_vi"] = f"Lùi mức (D3: {', '.join(used)}): bằng chứng gốc nhất trí cho mệnh đề còn lại."
            v["explanation_en"] = f"Backoff (D3: {', '.join(used)}): stored evidence is unanimous for the remaining claim."
            changed = True
            stats["flipped"] += 1
            stats[f"flipped:{p.get('type')}"] += 1
            for u in used:
                stats[f"op:{u}"] += 1
    return changed


def main() -> int:
    ap = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    ap.add_argument("--in", dest="src")
    ap.add_argument("--out", dest="dst")
    ap.add_argument("--ops", default=",".join(OPS))
    ap.add_argument("--types", default="entity,attribute,action,counting",
                    help="relation/spatial_relation excluded by default, as in person_uncap.py")
    ap.add_argument("--link-unchanged", action="store_true",
                    help="symlink unchanged records instead of copying (saves disk for ablations)")
    ap.add_argument("--selfcheck", action="store_true")
    a = ap.parse_args()
    if a.selfcheck:
        _selfcheck()
        return 0
    ops = {o.strip() for o in a.ops.split(",") if o.strip()}
    assert ops <= set(OPS), f"unknown ops: {ops - set(OPS)}"
    types = {t.strip() for t in a.types.split(",") if t.strip()}
    src, dst = Path(a.src).expanduser().resolve(), Path(a.dst).expanduser()
    dst.mkdir(parents=True, exist_ok=True)
    stats: Counter = Counter()
    for f in sorted(src.glob("*.json")):
        rec = json.loads(f.read_text(encoding="utf-8"))
        stats["records"] += 1
        out = dst / f.name
        if out.is_symlink() or out.exists():
            out.unlink()
        if process(rec, ops, types, stats):
            stats["records_changed"] += 1
            out.write_text(json.dumps(rec, ensure_ascii=False), encoding="utf-8")
        elif a.link_unchanged:
            os.symlink(f, out)
        else:
            out.write_text(json.dumps(rec, ensure_ascii=False), encoding="utf-8")
    print(json.dumps({"ops": sorted(ops), **stats}, ensure_ascii=False, indent=1))
    return 0


def _selfcheck() -> None:
    def probes(model, yes, no):
        return [{"model": model, "question_vi": "Trong ảnh có X không", "samples": ["Có."] * yes + ["Không."] * (5 - yes)},
                {"model": model, "question_vi": "Có đúng là KHÔNG có X không", "samples": ["Không."] * no + ["Có."] * (5 - no)}]

    def prop(pid, typ, text, expl, pr, eid="x_1", **kw):
        return {"id": pid, "type": typ, "text_vi": text, "subject": {"entity_id": eid},
                "evidence": {"probes": pr, "visual_grounding": {"grounding_score": 1.0},
                             "external_knowledge": {"requires_inference": "inference" in expl,
                                                    "inference_type": "none"}},
                "verification": {"status": "UNCERTAIN", "explanation_en": expl}, **kw}

    cap = PRECAP + " Capped at UNCERTAIN because "
    assert coarsen_hue("cái áo màu xanh dương") == "cái áo màu xanh"
    assert coarsen_hue("lá xanh lá cây") == "lá xanh"
    assert coarsen_count("Mười hai chiếc xe máy") == "nhiều chiếc xe máy"
    assert coarsen_count("sáu ô dù") == "nhiều ô dù"
    bàn = prop("P1", "entity", "một chiếc bàn", cap + "the claim rests on inference beyond what is visible.",
               probes("V", 5, 5), eid="ban_1")
    man = prop("P2", "entity", "một người đàn ông", cap + "the claim rests on inference beyond what is visible.",
               probes("V", 5, 5), eid="dan_ong_1")
    assert is_infer_artifact(bàn) and not is_infer_artifact(man)
    dis = cap + "colour verifiers disagree (V: affirms, Q: refutes)."
    col = prop("P3", "attribute", "bàn màu xanh dương", dis, probes("V", 5, 5) + probes("Q", 1, 2), eid="ban_1",
               attributes=[{"kind": "màu_sắc", "value_vi": "xanh dương"}])
    bare = prop("P4", "attribute", "bàn màu xanh", dis, probes("V", 5, 5) + probes("Q", 0, 0), eid="ban_1",
                attributes=[{"kind": "màu_sắc", "value_vi": "xanh"}])
    mixed = prop("P5", "attribute", "bàn màu xanh dương và đỏ", dis, probes("V", 5, 5) + probes("Q", 0, 0),
                 eid="ban_1", attributes=[{"kind": "màu_sắc", "value_vi": "xanh dương và đỏ"}])
    cnt = prop("P6", "counting", "sáu ô dù", cap + "an exact count above 5 cannot be verified reliably.",
               probes("V", 5, 5), eid="o_1", count={"value": 6, "exact": True})
    shaky = prop("P7", "counting", "sáu ô dù", cap + "an exact count above 5 cannot be verified reliably.",
                 probes("V", 4, 5), eid="o_1", count={"value": 6, "exact": True})
    dep = prop("P8", "attribute", "bàn bằng gỗ", cap + "the existence of ban_1 is itself unconfirmed.",
               probes("V", 5, 5), eid="ban_1")
    rec = {"propositions": [bàn, man, col, bare, mixed, cnt, shaky, dep]}
    st: Counter = Counter()
    assert process(rec, {"colour", "count"}, {"entity", "attribute", "counting"}, st)
    assert dep["verification"]["status"] == "UNCERTAIN", "prereq disabled -> no cascade"
    assert bàn["verification"]["status"] == "UNCERTAIN", "infer_artifact disabled"
    assert col["text_vi"] == "bàn màu xanh" and col["backoff"]["kind"] == "colour"
    assert bare["verification"]["status"] == "UNCERTAIN", "dispute on xanh itself is not recoverable"
    assert mixed["verification"]["status"] == "UNCERTAIN", "dispute may be about đỏ"
    assert cnt["text_vi"] == "nhiều ô dù" and cnt["count"]["exact"] is False
    assert shaky["verification"]["status"] == "UNCERTAIN", "4/5 < tau"
    process(rec, set(OPS), {"entity", "attribute", "counting"}, st)
    assert bàn["verification"]["status"] == "SUPPORTED" and bàn["text_vi"] == "một chiếc bàn"
    assert man["verification"]["status"] == "UNCERTAIN", "real gendered noun keeps the cap"
    assert dep["verification"]["status"] == "SUPPORTED" and dep["backoff"]["kind"] == "prereq"
    d, pre = doubts({"explanation_en": cap + "the existence of a_1 is itself unconfirmed; geometry is inconclusive: missing bounding box."})
    assert pre and d == [("exists", "a_1"), "other"]
    print("selfcheck OK")


if __name__ == "__main__":
    raise SystemExit(main())
