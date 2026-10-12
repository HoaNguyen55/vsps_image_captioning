#!/usr/bin/env python
"""Agreement, merged labels, verified precision, human-gold P/R/F1, CHAIR and POPE-vi from the human object kit.

    NCS_DATA=$PWD/data python3 scripts/score_human_gold.py --key OUT/key.json \
        --a1 vsps-objgold-v1_nguoi1.json [vsps-objgold-v1-batch2_nguoi1.json] --a2 vsps-objgold-v1_nguoi2.json \
        [--adj vsps-objgold-v1-adj_nguoi3.json] --out data/results/human_gold.json --pope-out data/object_gold/pope_vi_ktvic.json
    ... --partial                  # calibration / progress: only what both annotators have finished
    ... --write-adjudication DIR   # kit asking every disagreement as a yes/no question, for a third annotator
    python3 scripts/score_human_gold.py --self-check

Inputs are the exports of annotation/gan_nhan.html for the kit and key.json of
scripts/build_annotation_kit.py. Files marked AI-produced are refused unless --allow-ai, and
the report then says AI-silver. Classes are the 101 checkboxes with the guideline's synonyms
folded (build_annotation_kit.FOLD), and every gold is closed upward under its hierarchy
(build_annotation_kit.ancestors): a tick on `cô gái` puts `phụ nữ` and `người` in the gold.

Task A (Part 2, verify). Cohen's kappa (agreement.cohens_kappa) over yes/no/unsure and over yes vs
the rest, per item kind and per class (>= 10 items); per annotator the share of controls answered
yes and of catch trials answered no. Merge: agreeing labels stand; a disagreement takes the
adjudicator's label when it matches one side (majority of three), `unsure` when all three differ,
and stays `disputed` without --adj.

Task B (Part 1, exhaustive). object_gold_score.agreement on the closed tick sets (unsure counts as
not ticked). Golds: `agreed` (both), `union` (either), and `adjudicated` (agreed plus the disputed
classes the adjudicator answers yes) once every disputed class has an answer. The main gold is
`adjudicated`, else `agreed`.

Per system and mode, mentions folded the same way (unique classes per caption):
  ref        reference gold: classes the 5 references name, closed upward (CHAIR-vi rule)
  verified   a mention is correct when the references imply it or Task A says yes; P_hi also counts
             unsure and disputed answers; P is None unless every reference-false mention was asked
  human      object_prf.scores on the main Task B gold: P, R_spec, R_vague, F1, CHAIR_i = 100 - P,
             CHAIR_s = % captions with a mention outside the gold
  ref|human  the same on reference gold union human gold
  ref_false  mentions outside the reference gold, split by Task A (present but unmentioned /
             hallucinated / unsure / disputed / not asked) and by the human gold (present / absent)
Paired bootstrap (object_prf.paired, same resampled images) of every system minus --vs, per mode.
These numbers fold synonyms and use the guideline hierarchy, so they differ slightly from
object_prf.py (Table IV), which uses the raw lexicon.

POPE-vi (--pope-out), per image with >= 3 askable gold classes: 3 positives (most specific gold
classes first) and 3 negatives drawn only from human-verified absent classes, i.e. not related
(equal, ancestor or descendant) to anything an annotator ticked, marked unsure, or answered yes or
unsure in Task A, or that a reference names. Negatives per setting: random; popular (most frequent
gold class); adversarial (most co-occurring with the image's gold). 6 questions per image.
"""

from __future__ import annotations

import argparse
import json
import random
import shutil
import statistics
import sys
from collections import Counter, defaultdict
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT))
sys.path.insert(0, str(ROOT / "scripts"))

from agreement import cohens_kappa  # noqa: E402
from build_annotation_kit import (KIT_ID, KNOWN, TITLE, ancestors, close, fold, payload, related,  # noqa: E402
                                  said, write_tasks, zip_dir)
from object_gold_score import agreement, ai_produced, load_preds  # noqa: E402
from object_prf import image_counts, paired, scores  # noqa: E402

ANSWERS = ("yes", "no", "unsure")
SYSTEMS = ["p1-gold", "fuse2_s42", "tags_fuse2_s42", "e5_s42", "e5dpo_s42", "zeroshot", "tags_zeroshot"]
VERIFY = ("A", "A2")
#: classes POPE-vi never asks: generic (`đồ`, `vật`, `ánh sáng`) or decided by age or role, not by sight
POPE_SKIP = {"đồ", "vật", "ánh sáng", "thanh niên", "cô gái", "chàng trai", "cặp đôi", "học sinh", "công nhân"}
NAN = float("nan")


def load_annotator(paths: list[str], allow_ai: bool = False) -> dict:
    """One annotator's exports (main kit, batch 2, adjudication kit) merged into {name, sections, ai}."""
    names, sections, ai = set(), {}, False
    for p in map(Path, paths):
        if ai_produced(p):
            if not allow_ai:
                raise SystemExit(f"{p.name} is AI-produced, not human gold; pass --allow-ai to score it as AI-silver")
            ai = True
        data = json.loads(p.read_text(encoding="utf-8"))
        if not str(data.get("kit", "")).startswith(KIT_ID) or not isinstance(data.get("sections"), dict):
            raise SystemExit(f"{p.name} is not an export of the {KIT_ID} kit")
        names.add(data["annotator"])
        for key, labels in data["sections"].items():
            sections.setdefault(key, {}).update(labels)
    if len(names) != 1:
        raise SystemExit(f"{paths}: exports of different annotators {sorted(names)}")
    return {"name": names.pop(), "sections": sections, "ai": ai}


def answers(person: dict, section: str) -> dict[str, str]:
    return {k: v["answer"] for k, v in person["sections"].get(section, {}).items() if v.get("answer") in ANSWERS}


def merge(a: str, b: str, c: str | None) -> str:
    """Two labels, and the adjudicator's when they differ: majority of three, `unsure` if all differ."""
    if a == b:
        return a
    if c is None:
        return "disputed"
    return c if c in (a, b) else "unsure"


def specific(gold: set[str]) -> list[str]:
    """Gold classes no other gold class is a kind of: `phụ nữ` stays, `người` goes."""
    return sorted(c for c in gold if not any(c != o and c in ancestors(o) for o in gold))


def agree_verify(items: dict, x: dict, y: dict) -> dict:
    """Cohen's kappa on the items both answered: 3-way, yes vs rest, per kind and per class (>= 10 items)."""
    def kappa(sub, binary=True):
        k, raw = cohens_kappa([(x[i] == "yes", y[i] == "yes") if binary else (x[i], y[i]) for i in sub])
        return {"n": len(sub), "kappa": k, "raw": raw}

    by_class = defaultdict(list)
    for i in items:
        by_class[items[i]["class"]].append(i)
    return {"three_way": kappa(items, False), "binary": kappa(items),
            **{kind: kappa([i for i in items if items[i]["kind"] == kind]) for kind in ("test", "control", "catch")},
            "per_class": {c: kappa(v) for c, v in sorted(by_class.items()) if len(v) >= 10}}


def quality(items: dict, x: dict) -> dict:
    """Share of controls answered yes and of catch trials answered no."""
    ctl = [x[i] == "yes" for i in items if items[i]["kind"] == "control" and i in x]
    cat = [x[i] == "no" for i in items if items[i]["kind"] == "catch" and i in x]
    return {"control_yes": statistics.mean(ctl) if ctl else None, "catch_no": statistics.mean(cat) if cat else None}


def verify_block(key: dict, people: list[dict], partial: bool) -> tuple[dict, dict]:
    """Report of the verify sections both annotators started, and (image, class) -> merged label."""
    x, y = people[:2]
    third = answers(people[2], "J") if len(people) > 2 else {}
    report, final = {}, {}
    for sec in VERIFY:
        items = key["sections"].get(sec, {})
        ax, ay = answers(x, sec), answers(y, sec)
        if not (ax or ay):
            continue
        todo = {p["name"]: sum(i not in a for i in items) for p, a in ((x, ax), (y, ay))}
        if any(todo.values()) and not partial:
            raise SystemExit(f"section {sec}: unanswered items {todo}; finish them or pass --partial")
        both = {i: v for i, v in items.items() if i in ax and i in ay}
        merged = {i: merge(ax[i], ay[i], third.get(i)) for i in both}
        final.update({(v["image"], v["class"]): merged[i] for i, v in both.items()})
        report[sec] = {"n_items": len(items), "n_both": len(both), "unanswered": todo,
                       "kinds": dict(Counter(v["kind"] for v in items.values())),
                       "agreement": agree_verify(both, ax, ay), "merged": dict(Counter(merged.values())),
                       "quality": {p["name"]: quality(items, a) for p, a in ((x, ax), (y, ay))}}
    return report, final


def ticks(person: dict, ids: list[str]) -> dict[str, tuple[set[str], set[str]]]:
    """image -> (ticked classes, lexicon words typed in 'other' included; unsure classes) for done images."""
    out, wanted = {}, set(ids)
    for i, v in person["sections"].get("B", {}).items():
        if i in wanted and v.get("done"):
            present = {fold(c) for c in v.get("classes", [])} | said(v.get("other", ""))
            if present - KNOWN:
                raise SystemExit(f"{person['name']}: image {i} has unknown classes {sorted(present - KNOWN)}")
            out[i] = (present, {fold(c) for c in v.get("unsure", [])} - present)
    return out


def exhaustive_block(key: dict, people: list[dict], partial: bool) -> tuple[dict, dict, list[dict]]:
    """Report of Part 1, the golds {variant: {image: closed classes}}, and both annotators' ticks."""
    ids_all = key["sections"]["B"]
    tx, ty = ticks(people[0], ids_all), ticks(people[1], ids_all)
    ids = [i for i in ids_all if i in tx and i in ty]
    if len(ids) < len(ids_all) and not partial:
        raise SystemExit(f"Part 1: images not done {people[0]['name']} {len(ids_all) - len(tx)}, "
                         f"{people[1]['name']} {len(ids_all) - len(ty)}; finish them or pass --partial")
    cx, cy = ({i: close(t[i][0]) for i in ids} for t in (tx, ty))
    golds = {"agreed": {i: cx[i] & cy[i] for i in ids}, "union": {i: cx[i] | cy[i] for i in ids}}
    disputed = [(i, c) for i in ids for c in sorted(cx[i] ^ cy[i])]
    third = answers(people[2], "J") if len(people) > 2 else {}
    if len(people) > 2 and all(f"B-{i}-{c}" in third for i, c in disputed):
        golds["adjudicated"] = {i: close(golds["agreed"][i] | {c for c in cx[i] ^ cy[i] if third[f"B-{i}-{c}"] == "yes"})
                                for i in ids}
    report = {"n_images": len(ids), "agreement": agreement(cx, cy), "n_disputed": len(disputed),
              "adjudicated": "adjudicated" in golds,
              "unsure_per_image": {p["name"]: statistics.mean(len(t[i][1]) for i in ids) if ids else None
                                   for p, t in zip(people, (tx, ty))},
              "specific_gold_per_image": {k: statistics.mean(len(specific(g[i])) for i in ids) if ids else None
                                          for k, g in golds.items()}}
    return report, golds, [tx, ty]


def system_rows(caps: dict[str, str], ref: dict[str, set[str]], final: dict, gold: dict) -> tuple[dict, Counter]:
    """object_prf rows per gold for one system-mode, and how its reference-false mentions split."""
    rows, split = defaultdict(list), Counter()
    for i in ref:
        m = said(caps.get(i, ""))
        ok = hi = len(m & ref[i])
        rows["ref"].append(image_counts(m, ref[i], ancestors))
        for c in sorted(m - ref[i]):
            label = final.get((i, c), "not_asked")
            split[label] += 1
            ok += label == "yes"
            hi += label in ("yes", "unsure", "disputed")
            if i in gold:
                split["human_present" if c in gold[i] else "human_absent"] += 1
        rows["ver"].append((ok, len(m), ok, NAN, NAN, NAN))
        rows["ver_hi"].append((hi, len(m), hi, NAN, NAN, NAN))
        if i in gold:
            rows["human"].append(image_counts(m, gold[i], ancestors))
            rows["union"].append(image_counts(m, ref[i] | gold[i], ancestors))
    return rows, split


def gold_scores(rows: list[tuple]) -> dict:
    s = scores(rows)
    return {"P": s["P"], "R_spec": s["R_spec"], "F1_spec": s["F1_spec"], "R_vague": s["R_vague"],
            "F1_vague": s["F1_vague"], "CHAIR_i": 100 - s["P"],
            "CHAIR_s": 100 * statistics.mean(r[0] < r[1] for r in rows)}


def summarize(rows: dict, split: Counter) -> dict:
    n = sum(r[1] for r in rows["ref"])
    ref_false = n - sum(r[0] for r in rows["ref"])
    covered = not split["not_asked"]
    out = {"mentions_per_image": n / len(rows["ref"]), "ref": gold_scores(rows["ref"]),
           "verified": {"P": scores(rows["ver"])["P"] if covered else None,
                        "P_hi": scores(rows["ver_hi"])["P"] if covered else None,
                        "coverage": 100 * (1 - split["not_asked"] / ref_false) if ref_false else 100.0},
           "ref_false": {"n": ref_false, "present_unmentioned": split["yes"], "hallucinated": split["no"],
                         "unsure": split["unsure"], "disputed": split["disputed"], "not_asked": split["not_asked"],
                         "human_present": split["human_present"], "human_absent": split["human_absent"]}}
    if rows["human"]:
        out["human"], out["ref_or_human"] = gold_scores(rows["human"]), gold_scores(rows["union"])
    return out


def compare(rows: dict, covered: dict[str, bool], vs: str, n_boot: int) -> dict:
    """Every system minus `vs` in the same mode, paired bootstrap on the same resampled images."""
    out = {}
    for name, r in rows.items():
        system, mode = name.rsplit("-", 1)
        base = rows.get(f"{vs}-{mode}")
        if base is None or system == vs:
            continue
        d = {"P_ref": paired(base["ref"], r["ref"], ("P",), n_boot)["P"]}
        if covered[name] and covered[f"{vs}-{mode}"]:
            d["P_ver"] = paired(base["ver"], r["ver"], ("P",), n_boot)["P"]
        if r["human"]:
            d.update({f"{k}_human": v for k, v in paired(base["human"], r["human"], ("P", "R_spec", "F1_spec"),
                                                         n_boot).items()})
            d["P_ref_or_human"] = paired(base["union"], r["union"], ("P",), n_boot)["P"]
        out[name] = d
    return out


def pope(gold: dict[str, set[str]], blocked: dict[str, set[str]], files: dict[str, str], seed: int) -> dict:
    """POPE-vi: per image 3 gold positives and 3 verified-absent negatives in each of the three settings."""
    rng = random.Random(seed)
    ask = sorted(KNOWN - POPE_SKIP)
    freq = Counter(c for g in gold.values() for c in g)
    co = Counter((a, b) for g in gold.values() for a in g for b in g if a != b)
    out, skipped = {"random": [], "popular": [], "adversarial": []}, []
    for i, g in gold.items():
        spec = [c for c in specific(g) if c in ask]
        pos = rng.sample(spec, min(3, len(spec)))
        rest = [c for c in sorted(g) if c in ask and c not in pos]
        pos += rng.sample(rest, min(3 - len(pos), len(rest)))
        free = [c for c in ask if not related(c, blocked[i])]
        if len(pos) < 3 or len(free) < 3:
            skipped.append(i)
            continue
        negatives = {"random": rng.sample(free, 3),
                     "popular": sorted(free, key=lambda c: (-freq[c], c))[:3],
                     "adversarial": sorted(free, key=lambda c: (-sum(co[a, c] for a in g), -freq[c], c))[:3]}
        for setting, neg in negatives.items():
            qs = [(c, "yes") for c in pos] + [(c, "no") for c in neg]
            rng.shuffle(qs)
            out[setting] += [{"question_id": len(out[setting]) + n + 1, "image_id": i, "image": files[i], "class": c,
                              "text": f"Trong ảnh có {c} không?", "label": label} for n, (c, label) in enumerate(qs)]
    return {**out, "n_images": len(gold) - len(skipped), "skipped": skipped, "classes": ask}


def pope_blocked(people: list[dict], ticked: list[dict], refs: dict, ids: list[str]) -> dict[str, set[str]]:
    """Per image every class a person ticked, doubted or answered yes/unsure, or a reference names."""
    blocked = {i: set().union(*map(said, refs[i])) for i in ids}
    for t in ticked:
        for i in ids:
            blocked[i] |= t[i][0] | t[i][1]
    for p in people:
        for sec in (*VERIFY, "J"):
            for v in p["sections"].get(sec, {}).values():
                if v.get("answer") in ("yes", "unsure") and v.get("image") in blocked:
                    blocked[v["image"]].add(fold(v["class"]))
    return blocked


def run(key: dict, people: list[dict], refs: dict, preds: dict, partial: bool = False) -> tuple[dict, dict, dict]:
    """(report, per-image rows per system-mode for compare(), POPE-vi questions)."""
    report = {"annotators": [p["name"] for p in people],
              "gold_kind": "AI-silver" if any(p["ai"] for p in people) else "human"}
    report["verify"], final = verify_block(key, people, partial)
    report["exhaustive"], golds, ticked = exhaustive_block(key, people, partial)
    main_gold = "adjudicated" if "adjudicated" in golds else "agreed"
    gold = golds[main_gold]
    report["exhaustive"]["main_gold"] = main_gold
    ref = {i: close(set().union(*map(said, refs[i]))) for i in key["sections"]["B"]}
    rows, report["systems"] = {}, {}
    for name, caps in preds.items():
        rows[name], split = system_rows(caps, ref, final, gold)
        report["systems"][name] = summarize(rows[name], split)
    questions = pope(gold, pope_blocked(people, ticked, refs, list(gold)), key["files"], key["seed"])
    report["pope"] = {"n_images": questions["n_images"], "n_skipped": len(questions["skipped"]),
                      "per_setting": {s: len(questions[s]) for s in ("random", "popular", "adversarial")}}
    return report, rows, questions


def adjudication_items(key: dict, people: list[dict], seed: int = 0) -> list[dict]:
    """Every Task A disagreement (same id) and every disputed Task B class (id B-<image>-<class>), shuffled."""
    x, y = people[:2]
    items = []
    for sec in VERIFY:
        ax, ay = answers(x, sec), answers(y, sec)
        items += [{"id": i, "image": v["image"], "class": v["class"]} for i, v in key["sections"].get(sec, {}).items()
                  if i in ax and i in ay and ax[i] != ay[i]]
    tx, ty = (ticks(p, key["sections"]["B"]) for p in (x, y))
    for i in key["sections"]["B"]:
        if i in tx and i in ty:
            items += [{"id": f"B-{i}-{c}", "image": i, "class": c} for c in sorted(close(tx[i][0]) ^ close(ty[i][0]))]
    random.Random(seed).shuffle(items)
    return items


def write_adjudication(out: Path, key_path: Path, key: dict, items: list[dict]) -> Path:
    """Copy of the main kit (it must sit next to key.json) whose one section asks `items`; returns the zip."""
    src, kit_id = key_path.parent / key.get("kit", KIT_ID), KIT_ID + "-adj"
    if not (src / "gan_nhan.html").exists():
        raise SystemExit(f"{src} not found: the main kit folder must sit next to {key_path.name}")
    d = out / kit_id
    shutil.rmtree(d, ignore_errors=True)
    shutil.copytree(src, d, ignore=shutil.ignore_patterns("tasks.js"))
    section = {"key": "J", "kind": "verify", "title": "Phân xử · Có/không", "items": items}
    write_tasks(d / "tasks.js", payload(kit_id, TITLE + " (phân xử)", [section], key["files"]))
    zip_dir(d, out / f"{kit_id}.zip")
    return out / f"{kit_id}.zip"


def print_report(r: dict) -> None:
    def k(x):
        return "n/a" if x is None else f"{x:.2f}"

    def f(x):
        return "  n/a" if x is None else f"{x:5.1f}"

    print(f"annotators {r['annotators']}, {r['gold_kind']} labels")
    for sec, v in r["verify"].items():
        ag = v["agreement"]
        print(f"Task A [{sec}]: {v['n_both']}/{v['n_items']} items answered by both {v['kinds']}; kappa 3-way "
              f"{k(ag['three_way']['kappa'])}, yes-vs-rest {k(ag['binary']['kappa'])} (test {k(ag['test']['kappa'])}, "
              f"control {k(ag['control']['kappa'])}); merged {v['merged']}")
        for name, q in v["quality"].items():
            print(f"   {name}: controls answered yes {k(q['control_yes'])}, catch trials answered no {k(q['catch_no'])}")
    e, ag = r["exhaustive"], r["exhaustive"]["agreement"]
    print(f"Task B: {e['n_images']} images; pooled kappa {k(ag['pooled_kappa'])}, macro {k(ag['macro_kappa'])}, "
          f"Jaccard {k(ag['mean_jaccard'])}; disputed classes {e['n_disputed']}; main gold {e['main_gold']}; "
          f"specific gold classes/image {e['specific_gold_per_image']}")
    low = sorted((v["kappa"], c) for c, v in ag["per_class"].items()
                 if v["kappa"] is not None and v["n_a"] + v["n_b"] >= 10)[:8]
    print("   lowest-kappa classes (>= 10 ticks): " + ", ".join(f"{c} {x:.2f}" for x, c in low))
    print(f"{'system-mode':25s} M/img P_ref P_ver  P_hi  cov | P_hum R_spc R_vag CH_i  CH_s | P_r|h "
          f"| ref-false: n present halluc unsure+disp not-asked")
    for name, s in r["systems"].items():
        v, h, u, rf = s["verified"], s.get("human", {}), s.get("ref_or_human", {}), s["ref_false"]
        print(f"{name:25s} {s['mentions_per_image']:5.2f} {f(s['ref']['P'])} {f(v['P'])} {f(v['P_hi'])} "
              f"{v['coverage']:4.0f} | {f(h.get('P'))} {f(h.get('R_spec'))} {f(h.get('R_vague'))} "
              f"{f(h.get('CHAIR_i'))} {f(h.get('CHAIR_s'))} | {f(u.get('P'))} | {rf['n']:4d} "
              f"{rf['present_unmentioned']:4d} {rf['hallucinated']:4d} {rf['unsure'] + rf['disputed']:4d} "
              f"{rf['not_asked']:4d}")
    for name, d in r.get("paired", {}).items():
        print(f"  {name} - vs: " + "  ".join(f"d{m}={pt:+.1f} [{lo:+.1f},{hi:+.1f}] p={p:.4f}"
                                            for m, (pt, lo, hi, p) in d.items()))
    p = r["pope"]
    print(f"POPE-vi: {p['n_images']} images x 6 questions per setting {p['per_setting']}, {p['n_skipped']} skipped")


def _refused(fn, *args, **kwargs) -> bool:
    """True when fn stops the run with SystemExit (a refusal), False when it returns."""
    try:
        fn(*args, **kwargs)
    except SystemExit:
        return True
    return False


def _fixture() -> tuple:
    """30 fake images with 4 true classes each; references name 2, P1 says 1 named + 1 unnamed true + 1 false."""
    from build_annotation_kit import FORMS, numbered, verify_items

    rng = random.Random(0)
    pool = ["bàn", "ghế", "cốc", "sách", "hoa", "quả", "cầu", "núi", "sông", "bát", "đĩa", "dao", "bút", "chổi"]
    ids = [str(i) for i in range(1, 31)]
    truth = {i: rng.sample(pool, 4) for i in ids}
    fake = {i: rng.choice([c for c in pool if c not in truth[i]]) for i in ids}

    def say(cs):
        return "trong ảnh có " + " và ".join(FORMS[c][0] for c in cs)

    refs = {i: [say(truth[i][:2])] * 5 for i in ids}
    preds = {"p1-gold-short": {i: say([truth[i][0], truth[i][2], fake[i]]) for i in ids},
             "fuse2_s42-short": {i: say(truth[i][:2]) for i in ids}}
    assert all(said(preds["p1-gold-short"][i]) == {truth[i][0], truth[i][2], fake[i]} for i in ids)
    named = {i: said(refs[i][0]) for i in ids}
    said_by = defaultdict(list)
    for name, caps in preds.items():
        for i in ids:
            for c in said(caps[i]):
                said_by[i, c].append(name)
    blocked = {i: named[i] | {c for j, c in said_by if j == i} for i in ids}
    items = numbered(verify_items(said_by, named, 10, 0.05, random.Random(1), blocked), "A")
    key = {"kit": KIT_ID, "seed": 42, "split": "-", "modes": ["short"], "files": {i: f"{i}.jpg" for i in ids},
           "sections": {"B": ids, "A": items}}
    tests = [i for i, v in items.items() if v["kind"] == "test"]
    assert len(tests) == 60 and sum(v["kind"] == "catch" for v in items.values()) == 4

    def truly(v):
        return "yes" if v["class"] in truth[v["image"]] else "no"

    flip = set(tests[:5])
    a_y = {i: {**v, "answer": ("no" if truly(v) == "yes" else "yes") if i in flip else truly(v)} for i, v in items.items()}
    x = {"name": "x", "ai": False, "sections": {
        "A": {i: {**v, "answer": truly(v)} for i, v in items.items()},
        "B": {i: {"classes": truth[i] + (["cô gái"] if i == "1" else []), "unsure": [], "other": "", "done": True}
              for i in ids}}}
    y = {"name": "y", "ai": False, "sections": {
        "A": a_y,
        "B": {i: {"classes": truth[i] + (["phụ nữ"] if i == "1" else []), "unsure": ["voi"] if i == "2" else [],
                  "other": "", "done": True} for i in ids}}}
    return key, refs, preds, truth, x, y, flip


def _check() -> None:
    """Synthetic annotators on fake images; every number below is known in advance."""
    key, refs, preds, truth, x, y, flip = _fixture()
    ids, items = key["sections"]["B"], key["sections"]["A"]
    disputes = adjudication_items(key, [x, y])
    assert {d["id"] for d in disputes} == flip | {"B-1-cô gái"}, disputes
    judge = {"name": "z", "ai": False, "sections": {"J": {
        d["id"]: {**d, "answer": "yes" if d["class"] in truth[d["image"]] or d["id"] == "B-1-cô gái" else "no"}
        for d in disputes}}}

    r, rows, q = run(key, [x, y, judge], refs, preds)
    assert r["verify"]["A"]["merged"] == dict(Counter(v["answer"] for v in x["sections"]["A"].values()))
    assert 0 < r["verify"]["A"]["agreement"]["binary"]["kappa"] < 1
    assert r["verify"]["A"]["quality"]["x"] == {"control_yes": 1.0, "catch_no": 1.0}
    p1, f2 = r["systems"]["p1-gold-short"], r["systems"]["fuse2_s42-short"]
    assert abs(p1["ref"]["P"] - 100 / 3) < 1e-9 and abs(p1["verified"]["P"] - 200 / 3) < 1e-9
    assert p1["ref_false"]["present_unmentioned"] == 30 and p1["ref_false"]["hallucinated"] == 30
    assert p1["ref_false"]["human_present"] == 30 and p1["verified"]["coverage"] == 100
    assert f2["ref"]["P"] == 100 and f2["verified"]["P"] == 100
    assert r["exhaustive"]["main_gold"] == "adjudicated" and r["exhaustive"]["n_disputed"] == 1
    assert 0 < r["exhaustive"]["agreement"]["pooled_kappa"] < 1
    assert abs(p1["human"]["P"] - 200 / 3) < 1e-9 and abs(p1["human"]["R_spec"] - 100 * (29 * 0.5 + 0.4) / 30) < 1e-9
    assert abs(p1["human"]["CHAIR_i"] - 100 / 3) < 1e-9 and p1["human"]["CHAIR_s"] == 100
    d = compare(rows, {n: s["verified"]["P"] is not None for n, s in r["systems"].items()}, "p1-gold", 200)
    pt, lo, _, pval = d["fuse2_s42-short"]["P_ver"]
    assert abs(pt - 100 / 3) < 1e-9 and lo > 0 and pval <= 0.01
    said_yes = {(v["image"], v["class"]) for p in (x, y) for v in p["sections"]["A"].values() if v["answer"] == "yes"}
    for setting in ("random", "popular", "adversarial"):
        assert len(q[setting]) == 6 * len(ids)
        for i in ids:
            mine = [z for z in q[setting] if z["image_id"] == i]
            seen = set(truth[i]) | {"1": {"cô gái", "phụ nữ"}, "2": {"voi"}}.get(i, set())
            assert sum(z["label"] == "yes" for z in mine) == 3 and len({z["class"] for z in mine}) == 6
            assert all(z["class"] in close(truth[i]) for z in mine if z["label"] == "yes")
            assert not any(related(z["class"], seen) or (i, z["class"]) in said_yes for z in mine if z["label"] == "no")

    r2 = run(key, [x, y], refs, preds)[0]
    v2 = r2["systems"]["p1-gold-short"]["verified"]
    assert r2["exhaustive"]["main_gold"] == "agreed" and v2["P"] <= 200 / 3 <= v2["P_hi"] and v2["P"] < v2["P_hi"]
    first = next(i for i, v in items.items() if v["kind"] == "test")
    y_short = {**y, "sections": {**y["sections"], "A": {i: v for i, v in y["sections"]["A"].items() if i != first}}}
    assert _refused(run, key, [x, y_short], refs, preds) and not _refused(run, key, [x, y_short], refs, preds, True)
    _check_files(key, refs, preds, x, disputes)
    print("self-check OK")


def _check_files(key: dict, refs: dict, preds: dict, x: dict, disputes: list[dict]) -> None:
    """Adjudication kit on disk, and which export files load_annotator accepts."""
    import tempfile

    with tempfile.TemporaryDirectory() as tmp:
        tmp = Path(tmp)
        (tmp / KIT_ID / "images").mkdir(parents=True)
        (tmp / KIT_ID / "gan_nhan.html").write_text("<html></html>")
        (tmp / "key.json").write_text(json.dumps(key, ensure_ascii=False))
        z = write_adjudication(tmp / "adj", tmp / "key.json", key, disputes)
        kit = json.loads((tmp / "adj" / f"{KIT_ID}-adj" / "tasks.js").read_text(encoding="utf-8")[13:-2])
        assert z.exists() and [s["key"] for s in kit["sections"]] == ["J"] and len(kit["sections"][0]["items"]) == 6
        dump = {"kit": KIT_ID, "annotator": "x", "sections": x["sections"]}
        (tmp / "x.json").write_text(json.dumps(dump, ensure_ascii=False))
        (tmp / "bot.json").write_text(json.dumps({**dump, "ai_produced": True}, ensure_ascii=False))
        (tmp / "old.json").write_text(json.dumps({"annotator": "x", "labels": {}}))
        assert load_annotator([str(tmp / "x.json")])["sections"] == x["sections"]
        assert _refused(load_annotator, [str(tmp / "bot.json")]), "AI labels must be refused without --allow-ai"
        assert _refused(load_annotator, [str(tmp / "old.json")]), "exports of other tools must be refused"
        bot = load_annotator([str(tmp / "bot.json")], allow_ai=True)
        assert bot["ai"] and run(key, [x, bot], refs, preds)[0]["gold_kind"] == "AI-silver"


def main() -> int:
    ap = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    ap.add_argument("--key", help="key.json written by build_annotation_kit.py")
    ap.add_argument("--a1", nargs="+", help="export(s) of the first annotator: main kit [, batch 2]")
    ap.add_argument("--a2", nargs="+", help="export(s) of the second annotator")
    ap.add_argument("--adj", nargs="+", default=None, help="export of the adjudication kit (third annotator)")
    ap.add_argument("--results", default=str(ROOT / "data" / "results"))
    ap.add_argument("--systems", nargs="+", default=SYSTEMS)
    ap.add_argument("--vs", default="p1-gold", help="baseline of the paired bootstrap")
    ap.add_argument("--bootstrap", type=int, default=5000)
    ap.add_argument("--partial", action="store_true", help="score only what both annotators finished")
    ap.add_argument("--allow-ai", action="store_true", help="accept AI-produced files; the report says AI-silver")
    ap.add_argument("--out", default=None, help="report JSON")
    ap.add_argument("--pope-out", default=None, help="POPE-vi questions JSON")
    ap.add_argument("--write-adjudication", default=None, metavar="DIR")
    ap.add_argument("--self-check", action="store_true")
    args = ap.parse_args()
    if args.self_check:
        _check()
        return 0
    if not (args.key and args.a1 and args.a2):
        ap.error("--key, --a1 and --a2 are required")
    key = json.loads(Path(args.key).read_text(encoding="utf-8"))
    people = [load_annotator(p, args.allow_ai) for p in (args.a1, args.a2, args.adj) if p]
    if args.write_adjudication:
        items = adjudication_items(key, people)
        print(f"{len(items)} disagreements -> {write_adjudication(Path(args.write_adjudication), Path(args.key), key, items)}")
        return 0

    from evaluate import references

    results = Path(args.results)
    preds = {f"{s}-{m}": load_preds(results / f"{s}-{m}.preds.json") for s in args.systems for m in key["modes"]
             if (results / f"{s}-{m}.preds.json").exists()}
    report, rows, questions = run(key, people, references(key["split"]), preds, args.partial)
    covered = {name: s["verified"]["P"] is not None for name, s in report["systems"].items()}
    report["paired"] = compare(rows, covered, args.vs, args.bootstrap)
    print_report(report)
    if args.out:
        Path(args.out).write_text(json.dumps(report, ensure_ascii=False, indent=1), encoding="utf-8")
    if args.pope_out:
        Path(args.pope_out).write_text(json.dumps(questions, ensure_ascii=False, indent=1), encoding="utf-8")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
