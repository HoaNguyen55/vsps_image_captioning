#!/usr/bin/env python3
"""A-N1 REV (CC-032 correction): ADDENDUM_v2.{json,md} are the reviewed drafts plus ONLY the additions of main's REV brief.

  (i)   the PD-16 final (b) scope paragraph, with the stage-1 conflict counts read from stage1_results.json;
  (ii)  the "descriptive: bpref_set Q" entry (already computed by score_an1.py, whose sha is unchanged);
  (iii) and (iv) the measures and score_an1 code paths become scripts/g2b/an1/ (shas unchanged);
  (v)   one note in the deviation record.

Every new number is read from its file, and the md's number-sources table gets one row per new number. The reviewed
drafts must match their MANIFEST.json shas. Existing outputs are never overwritten.

  python3 build_addendum_v2.py
"""
from __future__ import annotations

import json
import re

import build_addendum as b

g, HERE = b.g, b.HERE
DRAFT_JSON, DRAFT_MD = HERE / "ADDENDUM_DRAFT.json", HERE / "ADDENDUM_DRAFT.md"
OUT_JSON, OUT_MD = HERE / "ADDENDUM_v2.json", HERE / "ADDENDUM_v2.md"
DESC_KEYS = ["sets.<set>.primary_analysis.descriptive_Q_at_theta.bpref",
             "sets.<set>.sensitivity_full_set.descriptive_Q_at_theta.bpref"]
SCOPE_TEXT = ("The claim holds given verified negatives. On CV295 and UV231 the negatives are U80 minus the image's "
              "instance classes, the exhaustive complement of the complete gold, so cF1 carries complete-gold negatives "
              "at every ladder level and part of the shrinkage on those sets is by construction. XM600's OIV7 absent "
              "labels are not exhaustive, so XM600 is the informative set.")
MD_SCOPE = """- **Given verified negatives (PD-16 final (b)).** The claim holds given verified negatives.
  - On CV295 and UV231 the negatives are U80 \\ inst_i, the exhaustive complement of the complete gold. cF1 therefore
    carries the complete gold's negatives at every ladder level, and part of the shrinkage on these sets is by
    construction.
  - XM600's OIV7 `absent` labels are not exhaustive: {{s1:sets.XM3600.diagnostics.images_without_negatives}} of the
    {{s1:sets.XM3600.n_images}} stage-1 XM3600 images carry none (D2). XM600 is therefore the informative set.
  - Conflict rates at all_refs, stage 1: reference positives that the complete gold marks absent, where the positive
    wins (D6). COCO-2500 {{s1:sets.COCO-2500.diagnostics.conflict_pairs_all_refs}} of
    {{s1:sets.COCO-2500.diagnostics.positive_pairs_all_refs}}; UIT-ViIC test
    {{s1:sets.UIT-ViIC test.diagnostics.conflict_pairs_all_refs}} of
    {{s1:sets.UIT-ViIC test.diagnostics.positive_pairs_all_refs}}; XM3600
    {{s1:sets.XM3600.diagnostics.conflict_pairs_all_refs}} of {{s1:sets.XM3600.diagnostics.positive_pairs_all_refs}}
    (keys `sets.<set>.diagnostics.conflict_pairs_all_refs` and `positive_pairs_all_refs`). The scorer reports the same
    counts for each registered set under `sets.<set>.primary_analysis.diagnostics_all_images`.
"""
MD_DESC = """- **Descriptive: bpref_set Q (PD-16 final (a)).** Q_bpref = θ · Range_F1 − Range_bpref_set per set, with the
  primary's θ, bootstrap draws, clean LADDER subset, levels and lexicon. Output keys
  `sets.<set>.primary_analysis.descriptive_Q_at_theta.bpref` and `sets.<set>.sensitivity_full_set.descriptive_Q_at_theta.bpref`.
  It has no verdict and enters no verdict, outcome or kill rule.
"""
MD_DEV = ("\n  PD-16 final (a): bpref_set's Q is now reported per set, descriptively and without a verdict (§3, \"Descriptive: "
          "bpref_set Q\").\n")


def resolve(text: str, data: dict, sources: dict) -> tuple[str, list[str]]:
    rows = []

    def sub(m: re.Match) -> str:
        v = data[m.group(1)]
        for k in m.group(2).split("."):
            v = v[int(k)] if isinstance(v, list) else v[k]
        p = sources[m.group(1)]
        rows.append(f"| {v} | `{b.rel(p)}` | {g.sha256_file(p)[:16]} | `{m.group(2)}` |")
        return str(v)

    return re.sub(r"\{\{(\w+):([^|}]+)\}\}", sub, text), rows


def once(text: str, old: str, new: str) -> str:
    assert text.count(old) == 1, old[:60]
    return text.replace(old, new)


def main() -> None:
    for p in (OUT_JSON, OUT_MD):
        if p.exists():
            raise SystemExit(f"{p} exists; never overwritten")
    man = g.jload(HERE / "MANIFEST.json")["files"]
    for p in (DRAFT_JSON, DRAFT_MD):
        assert g.sha256_file(p) == man[p.name]["sha256"], f"{p.name} differs from the reviewed draft"
    s1, add = g.jload(b.S1), g.jload(DRAFT_JSON)
    cite = {"source": b.rel(b.S1), "sha256": g.sha256_file(b.S1)}
    cp = add["proposed_commit_paths"]
    add["code"]["measures"]["path"], add["code"]["score_an1"]["path"] = cp["measures"], cp["score_an1"]
    scope = {"text": SCOPE_TEXT, "authority": "PD-16 final (b)",
             "stage1_conflicts_all_refs": {**{n: {k: s["diagnostics"][k] for k in ("conflict_pairs_all_refs",
                                                                                    "positive_pairs_all_refs")}
                                              for n, s in s1["sets"].items()}, **cite,
                                           "keys": "sets.<set>.diagnostics.{conflict_pairs_all_refs, "
                                                   "positive_pairs_all_refs}"},
             "stage1_xm3600_images_without_negatives": {
                 "value": s1["sets"]["XM3600"]["diagnostics"]["images_without_negatives"],
                 "of": s1["sets"]["XM3600"]["n_images"], **cite,
                 "keys": "sets.XM3600.diagnostics.images_without_negatives, sets.XM3600.n_images"},
             "registered_sets": "score_an1.py reports the same counts per set: "
                                "sets.<set>.primary_analysis.diagnostics_all_images"}
    desc = {"statistic": "theta * Range_F1 - Range_bpref_set, per set", "output_keys": DESC_KEYS,
            "same_as_primary": "theta, bootstrap draws, clean LADDER subset, gold levels and lexicon",
            "verdict": "none; bpref_set enters no verdict(), outcome() or kill rule",
            "code": "score_an1.py analyse_set (descriptive_Q_at_theta); sha unchanged, see code.score_an1",
            "authority": "PD-16 final (a)"}
    out = {}
    for k, v in add.items():
        out[k] = v
        if k == "scope":
            out["scope_given_verified_negatives"] = scope
        if k == "descriptive":
            out["descriptive_bpref_set_Q"] = desc
    out["deviation_from_stage1_plan"]["note_pd16_final"] = (
        "bpref_set's Q is now reported per set as a descriptive output without a verdict (descriptive_bpref_set_Q)")
    OUT_JSON.write_text(json.dumps(out, indent=1, ensure_ascii=False) + "\n", encoding="utf-8")

    md = DRAFT_MD.read_text(encoding="utf-8")
    scope_md, rows = resolve(MD_SCOPE, {"s1": s1}, {"s1": b.S1})
    md = once(md, "  `alternative_if_rule_kept` of the JSON. No code changes, because the scripts read the measure and θ "
                  "from the JSON.\n", "  `alternative_if_rule_kept` of the JSON. No code changes, because the scripts "
                  "read the measure and θ from the JSON.\n" + MD_DEV)
    md = once(md, "  - the unjudged shares, D2 counts and D6 counts.\n",
              "  - the unjudged shares, D2 counts and D6 counts.\n" + MD_DESC)
    md = once(md, "  - a PASS there is never counted as support.\n", "  - a PASS there is never counted as support.\n"
              + scope_md)
    md = once(md, "`python3 score_an1.py score --addendum", f"`python3 {cp['score_an1']} score --addendum")
    OUT_MD.write_text(md.rstrip("\n") + "\n" + "\n".join(rows) + "\n", encoding="utf-8")
    print(json.dumps({"json_sha256": g.sha256_file(OUT_JSON), "md_sha256": g.sha256_file(OUT_MD)}))


if __name__ == "__main__":
    main()
