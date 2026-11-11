#!/usr/bin/env python
"""Build the labelling assignment for the human completion of the XM3600-600 object gold (Paper A).

Unit: one (image, lexicon class) pair; question: "is this object in the image?".
Targets: every pair that a scored system or a Vietnamese reference names and that the Open Images V7
human-verified labels cannot settle (mapped class with unknown status, or class without a mapping).
Hidden controls: pairs that OIV7 does settle (named present, named absent, unnamed absent) and repeats.

Outputs (in --out, never under /mnt/d): assignment.json (served), practice.json (served, with answers),
key.json (private: what each question is), overlap_images.txt (the 25% of images for the second annotator),
BUILD.json (counts and input hashes). No caption text is written anywhere.

    NCS_DATA=data ~/.venvs/c_stage1_lists/bin/python -B tools/obj_rater/build_assignment.py --out ~/vsps_labels/xm600_gold
"""
from __future__ import annotations

import argparse
import hashlib
import json
import random
import sys
from collections import defaultdict
from pathlib import Path

ROOT = Path(__file__).resolve().parents[2]
sys.path.insert(0, str(ROOT))
sys.path.insert(0, str(ROOT / "scripts"))

SEED = 20261111
N_CTRL_PRESENT, N_FOIL, N_REPEAT, OVERLAP_SHARE, N_PRACTICE = 200, 100, 150, 0.25, 15
A_DIR = ROOT / "data" / "results" / "xm3600"
G2B_DIR = ROOT / ".session_backup" / "machines" / "O-2308428" / "root" / "outputs" / "g2b_qwen3vl"
DS = ROOT / "data" / "datasets" / "xm3600"
IMG_DIR = DS / "images"


def sha(path: Path) -> str:
    return hashlib.sha256(path.read_bytes()).hexdigest()


def load_systems() -> tuple[dict[str, dict[str, str]], dict[str, str]]:
    systems, shas = {}, {}
    for f in sorted(A_DIR.glob("*.preds.json")):
        p = json.loads(f.read_text(encoding="utf-8"))
        systems[f.name.removesuffix(".preds.json")] = {str(k): (v[0] if isinstance(v, list) else v) or "" for k, v in p.items()}
        shas[str(f.relative_to(ROOT))] = sha(f)
    for f in sorted(G2B_DIR.glob("g2b_q3_xm600-*.preds.json")):
        p = json.loads(f.read_text(encoding="utf-8"))["predictions"]
        systems[f.name.removesuffix(".preds.json")] = {str(k): v or "" for k, v in p.items()}
        shas[str(f.relative_to(ROOT))] = sha(f)
    return systems, shas


def build(out: Path) -> dict:
    import xm3600_oiv7 as X
    from rescap.chair import objects_in

    data = json.loads((DS / "test_data.json").read_text(encoding="utf-8"))
    refs = defaultdict(list)
    for a in data["annotations"]:
        refs[str(a["image_id"])].append(a["caption"])
    ids = sorted(refs)
    labels = {k: v for k, v in json.loads(X.LABELS.read_text(encoding="utf-8")).items() if not k.startswith("_")}
    vmap = X.resolve_map(DS / "oiv7" / "oidv7-class-descriptions.csv")
    raw_map = {k: v for k, v in json.loads(X.MAP.read_text(encoding="utf-8")).items() if not k.startswith("_")}
    st = X.statuses(vmap, labels)
    systems, in_shas = load_systems()
    for name, p in systems.items():
        assert not set(ids) - p.keys(), f"{name}: captions missing for {len(set(ids) - p.keys())} images"

    named: dict[tuple[str, str], set[str]] = defaultdict(set)  # (image, class) -> who names it
    for name, p in systems.items():
        for i in ids:
            for c in set(objects_in(p[i])):
                named[(i, c)].add(name)
    for i in ids:
        for cap in refs[i]:
            for c in set(objects_in(cap)):
                named[(i, c)].add("reference")

    def bucket(i: str, c: str) -> str:
        return "unmapped" if c not in vmap else st.get(i, {}).get(c, "unknown")

    rng = random.Random(SEED)
    targets1 = sorted(p for p in named if bucket(*p) == "unknown")   # part 1: the bucket the paper's bound covers
    targets2 = sorted(p for p in named if bucket(*p) == "unmapped")  # part 2: classes without an OIV7 mapping
    named_abs = sorted(p for p in named if bucket(*p) == "absent")
    named_pre = sorted(p for p in named if bucket(*p) == "present")
    ctrl_pre = sorted(rng.sample(named_pre, min(N_CTRL_PRESENT, len(named_pre))))
    foil_pool = sorted((i, c) for i in ids for c, s in st.get(i, {}).items() if s == "absent" and (i, c) not in named)
    foils = sorted(rng.sample(foil_pool, min(N_FOIL, len(foil_pool))))
    repeats = sorted(rng.sample(targets1, min(N_REPEAT, len(targets1))))

    def hint(c: str) -> str:
        pos = raw_map.get(c, {}).get("pos") or []
        return ("Open Images: " + ", ".join(pos)) if pos else ""

    key, screens = {}, []

    def qid(part: int, i: str, c: str) -> str:
        return hashlib.sha256(f"{SEED}|{part}|{i}|{c}".encode()).hexdigest()[:12]

    def add_part(part: int, rows: list[tuple[str, str, str]]) -> None:
        by_img = defaultdict(list)
        for i, c, role in rows:
            by_img[i].append((c, role))
        order = sorted(by_img)
        rng.shuffle(order)
        for i in order:
            qs = by_img[i]
            rng.shuffle(qs)
            q_out = []
            for c, role in qs:
                q = qid(part, i, c)
                assert q not in key
                key[q] = {"image": i, "class": c, "part": part, "role": role, "bucket": bucket(i, c),
                          "named_by": sorted(named.get((i, c), []))}
                q_out.append({"qid": q, "label": c, "hint": hint(c)})
            screens.append({"sid": f"p{part}-{i}", "part": part, "image": f"images/{i}.jpg", "q": q_out})

    add_part(1, [(i, c, "target") for i, c in targets1] + [(i, c, "ctrl_absent") for i, c in named_abs]
             + [(i, c, "ctrl_present") for i, c in ctrl_pre] + [(i, c, "foil_absent") for i, c in foils])
    add_part(2, [(i, c, "target") for i, c in targets2])
    add_part(3, [(i, c, "repeat") for i, c in repeats])

    need_imgs = {i for i, _ in targets1 + targets2}
    # practice: XM3600 images outside the 600, questions with an OIV7-verified answer (feedback is shown)
    prng = random.Random(SEED + 1)
    outside = sorted(i for i in st if i not in set(ids) and (IMG_DIR / f"{i}.jpg").is_file()
                     and sum(s == "present" for s in st[i].values()) >= 2 and sum(s == "absent" for s in st[i].values()) >= 2)
    practice = []
    for i in prng.sample(outside, min(N_PRACTICE, len(outside))):
        pre = sorted(c for c, s in st[i].items() if s == "present")
        ab = sorted(c for c, s in st[i].items() if s == "absent")
        cs = prng.sample(pre, min(3, len(pre))) + prng.sample(ab, min(2, len(ab)))
        prng.shuffle(cs)
        qs = [{"qid": f"practice-{i}-{n}", "label": c, "hint": hint(c), "answer": "Y" if st[i][c] == "present" else "N"}
              for n, c in enumerate(cs)]
        practice.append({"sid": f"practice-{i}", "part": 0, "image": f"images/{i}.jpg", "q": qs})

    overlap = sorted(rng.sample(sorted(need_imgs), round(OVERLAP_SHARE * len(need_imgs))))
    n_q = sum(len(s["q"]) for s in screens)
    meta = {"name": "xm600_gold_completion", "seed": SEED, "labels": {"Y": "Có", "N": "Không", "U": "Không xác định được",
            "A": "Tên lớp mơ hồ"}, "n_screens": len(screens), "n_questions": n_q}
    out.mkdir(parents=True, exist_ok=True)
    files = {"assignment.json": {"meta": meta, "screens": screens}, "practice.json": {"meta": {**meta, "name": "practice"},
             "screens": practice}, "key.json": key}
    for name, obj in files.items():
        (out / name).write_text(json.dumps(obj, ensure_ascii=False, sort_keys=True, indent=1), encoding="utf-8")
    (out / "overlap_images.txt").write_text("\n".join(overlap) + "\n", encoding="utf-8")
    counts = {"images": len(ids), "systems": sorted(systems), "named_pairs": len(named), "part1_targets_mapped_unknown": len(targets1),
              "part2_targets_unmapped": len(targets2), "ctrl_absent_named": len(named_abs), "ctrl_present_named": len(ctrl_pre),
              "foil_absent_unnamed": len(foils), "repeats": len(repeats), "screens": len(screens), "questions": n_q,
              "images_with_targets": len(need_imgs), "practice_screens": len(practice), "overlap_images": len(overlap)}
    build_rec = {"counts": counts, "inputs_sha256": {**in_shas, "data/datasets/xm3600/test_data.json": sha(DS / "test_data.json"),
                 "data/xm3600/oiv7_labels.json": sha(X.LABELS), "data/xm3600/vi_oiv7_map.json": sha(X.MAP),
                 "tools/obj_rater/build_assignment.py": sha(Path(__file__))},
                 "outputs_sha256": {n: sha(out / n) for n in (*files, "overlap_images.txt")}}
    (out / "BUILD.json").write_text(json.dumps(build_rec, ensure_ascii=False, indent=1), encoding="utf-8")
    return build_rec


def main() -> int:
    ap = argparse.ArgumentParser()
    ap.add_argument("--out", required=True)
    args = ap.parse_args()
    out = Path(args.out).expanduser().resolve()
    assert not str(out).startswith("/mnt/"), "write the assignment and labels on the Linux home filesystem, not /mnt"
    rec = build(out)
    print(json.dumps(rec["counts"], ensure_ascii=False, indent=1))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
