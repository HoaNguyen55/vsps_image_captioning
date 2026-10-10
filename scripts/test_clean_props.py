"""Assert-based checks for build_dpo_data.clean_props. Run: python3 scripts/test_clean_props.py"""
import sys
from collections import Counter
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))
sys.path.insert(0, str(Path(__file__).resolve().parents[1]))
from build_dpo_data import clean_props  # noqa: E402


def ent_prop(pid, eid, text, status="SUPPORTED"):
    return {"id": pid, "type": "entity", "subject": {"entity_id": eid, "text_vi": text},
            "predicate": {"lemma_vi": "có"}, "text_vi": text, "verification": {"status": status}}


def entity(eid, cat, n, classifier="chiếc"):
    return {"id": eid, "category_vi": cat, "classifier": classifier, "number": {"value": n}}


SWALLOW = {"id": "P9", "type": "action",
           "subject": {"entity_id": "ao_2", "text_vi": "nhiều chiếc áo"},
           "predicate": {"lemma_vi": "một người phụ nữ đang cầm một chiếc áo"},
           "text_vi": "nhiều chiếc áo một người phụ nữ đang cầm một chiếc áo",
           "verification": {"status": "SUPPORTED"}}


def run(woman_n=1, woman_status="SUPPORTED", extra=(), entities=True):
    props = [ent_prop("P1", "phu_nu_1", "một người", woman_status),
             ent_prop("P2", "ao_2", "nhiều chiếc áo"), *extra, SWALLOW]
    ents = [entity("phu_nu_1", "phụ nữ", woman_n, "người"), entity("ao_2", "áo", None)]
    ents += [entity(p["subject"]["entity_id"], "phụ nữ", 1, "người") for p in extra]
    out = clean_props(props, Counter(), ents if entities else None)
    return [p for p in out if p["id"] == "P9"]


# rehome: clause re-attached to its own SUPPORTED subject; the neutralised surface is used, gender not restored
(fixed,) = run()
assert fixed["subject"]["entity_id"] == "phu_nu_1"
assert fixed["predicate"]["lemma_vi"] == "đang cầm một chiếc áo"
assert fixed["text_vi"] == "một người đang cầm một chiếc áo"
assert SWALLOW["subject"]["entity_id"] == "ao_2"  # input not mutated
# refusals keep the old drop: count disagrees, existence not SUPPORTED, ambiguous NP, no entities passed
assert run(woman_n=4) == []
assert run(woman_status="REJECTED") == []
assert run(extra=[ent_prop("P3", "phu_nu_3", "một người")]) == []
assert run(entities=False) == []

# unchanged rules
base = {"type": "attribute", "subject": {"entity_id": "x"}, "verification": {"status": "SUPPORTED"}}
assert clean_props([{**base, "id": "a", "text_vi": "một người mặc áo đỏ đỏ", "predicate": {"lemma_vi": "mặc"}}], Counter(), []) == []
assert clean_props([{**base, "id": "b", "text_vi": "x", "predicate": {"lemma_vi": " ".join(["w"] * 13)}}], Counter(), []) == []
dup = {**base, "id": "c", "text_vi": "Một chiếc xe", "predicate": {"lemma_vi": "có"}}
assert len(clean_props([dup, {**dup, "id": "d", "text_vi": "một chiếc xe"}], Counter(), [])) == 1
print("ok")
