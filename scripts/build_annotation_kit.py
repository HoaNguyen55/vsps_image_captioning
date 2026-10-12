#!/usr/bin/env python
"""Build the blind human object-gold kit for the 300 sampled KTVIC test images.

    NCS_DATA=$PWD/data python3 scripts/build_annotation_kit.py --out-dir /tmp/objgold_kit
    NCS_DATA=$PWD/data python3 scripts/build_annotation_kit.py --out-dir OUT --images-dir /root/ncs-data/datasets/ktvic/images
    python3 scripts/build_annotation_kit.py --self-check

Each annotator does two parts on the images of data/object_gold/sample.json (seed 42), in this order.

Part 1 = Task B, exhaustive gold: tick every class visible in the image (yes / unsure / blank) over
the 101 checkboxes of object_gold_sample.py. Nothing is pre-filled.

Part 2 = Task A, federated verification (LVIS-style): one image and "Trong ảnh có <class> không?",
answered Có / Không / Không chắc, for
  test     every (image, class) that a --systems caption names in either mode and no reference names
           (classes folded by FOLD; a class a reference only implies, e.g. `xe` for `xe máy`, is asked too),
  control  --controls pairs those captions name and a reference names as well,
  catch    --catch-rate of all items: a CATCH class that no reference and no caption of any system
           relates to (hierarchy below).
Items are shuffled. Item kind and the systems that name a pair are written only to key.json.
The pairs of --batch2-systems that Part 2 does not ask form an optional second kit (section A2) with
its own controls and catch trials. AI-silver labels (annot_claude.json) are never read.

Writes into --out-dir:
  vsps-objgold-v1/, vsps-objgold-v1-batch2/   gan_nhan.html, tasks.js, huong_dan.md, README.md, images/
                                               (original files; JPEG at --max-side when larger)
  vsps-objgold-v1.zip, vsps-objgold-v1-batch2.zip   what is sent to the annotators
  key.json                                     item -> image, class, kind, systems; never sent

The synonym folding (FOLD) and the hierarchy that the guideline (annotation/huong_dan.md §2, §4)
promises annotators are defined here; scripts/score_human_gold.py imports them.
"""

from __future__ import annotations

import argparse
import json
import random
import re
import shutil
import sys
import tempfile
import zipfile
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT))
sys.path.insert(0, str(ROOT / "scripts"))

from object_gold_sample import GROUPS  # noqa: E402
from object_gold_score import ANCESTORS, CLASSES, FORMS, load_preds, mentions  # noqa: E402

SRC = ROOT / "annotation"
KIT_ID = "vsps-objgold-v1"
TITLE = "Gán nhãn vật thể"
SYSTEMS = ["p1-gold", "fuse2_s42", "tags_fuse2_s42", "e5_s42"]
BATCH2 = ["zeroshot", "tags_zeroshot"]
#: every system whose captions keep a class out of an image's catch trials
ALL_SYSTEMS = [*SYSTEMS, *BATCH2, "e5dpo_s42"]
MODES = ("short", "detailed")
#: large, distinctive classes for catch trials; used only where nothing relates to them
CATCH = ["voi", "khỉ", "rắn", "ngựa", "xe tăng", "máy bay"]
SEC_PER_IMAGE = (60, 90)

#: Synonyms the guideline lets annotators tick either way (huong_dan.md §4).
FOLD = {"đứa trẻ": "trẻ em", "cô gái trẻ": "cô gái", "nam thanh niên": "chàng trai", "bạn trẻ": "thanh niên",
        "bạn": "người"}
VEHICLES = ["xe máy", "xe đạp", "ô tô", "xe buýt", "xe tải", "xe tăng", "xe ba gác", "xe đẩy", "xích lô"]
#: Parents the guideline adds to the lexicon hypernyms (rescap/vi/lexicon.py), which give `cô gái`,
#: `chàng trai` and `em bé` none and send vehicles and animals to nouns that are not checkboxes.
EXTRA_PARENTS = {"cô gái": {"phụ nữ"}, "chàng trai": {"đàn ông"}, "bé gái": {"trẻ em"}, "bé trai": {"trẻ em"},
                 "em bé": {"trẻ em"}, "học sinh": {"người"}, "công nhân": {"người"}, "nón lá": {"mũ"},
                 "dãy nhà": {"nhà"}, "khu rừng": {"cây"},
                 **{v: {"xe"} for v in VEHICLES},
                 **{a: {"vật"} for a in GROUPS["Động vật"] if a != "vật"}}
KNOWN = frozenset(FOLD.get(c, c) for c in CLASSES)


def fold(c: str) -> str:
    return FOLD.get(c, c)


def said(text: str) -> set[str]:
    """Folded classes a caption, a reference or an 'other objects' field names."""
    return {fold(c) for c in mentions(text or "")}


def ancestors(c: str) -> set[str]:
    """c and every class it is a kind of: lexicon hypernyms plus EXTRA_PARENTS."""
    out, todo = set(), [fold(c)]
    while todo:
        x = todo.pop()
        if x not in out:
            out.add(x)
            todo += [fold(p) for p in ANCESTORS.get(x, set()) | EXTRA_PARENTS.get(x, set())]
    return out


def close(classes) -> set[str]:
    """Upward closure over the checkbox classes: `cô gái` brings `phụ nữ` and `người`."""
    return set().union(*map(ancestors, classes)) & KNOWN


def related(c: str, named: set[str]) -> bool:
    """c equals, is implied by, or is a kind of something in `named`; then c is not a safe 'absent'."""
    return c in close(named) or bool(ancestors(c) & named)


def glosses(guide: str) -> dict[str, str]:
    """class -> definition, from the '| `class` | definition |' rows of the guideline's §6 table."""
    table = guide.split("\n## 6.", 1)[1].split("\n## ", 1)[0]
    rows = dict(re.findall(r"^\| `([^`]+)` \| (.+?) \|$", table, flags=re.M))
    unknown = set(rows) - set(CLASSES)
    assert not unknown, f"the guideline defines classes that are not checkboxes: {sorted(unknown)}"
    return rows


def mentioned(results: Path, systems: list[str], ids: list[str]) -> dict[tuple[str, str], list[str]]:
    """(image, class) -> the '<system>-<mode>' runs whose caption names it."""
    out: dict[tuple[str, str], list[str]] = {}
    for system in systems:
        for mode in MODES:
            caps = load_preds(results / f"{system}-{mode}.preds.json")
            for i in ids:
                for c in sorted(said(caps.get(i, ""))):
                    out.setdefault((i, c), []).append(f"{system}-{mode}")
    return out


def verify_items(said_by: dict, named: dict[str, set[str]], n_controls: int, catch_rate: float,
                 rng: random.Random, blocked: dict[str, set[str]]) -> list[dict]:
    """Test pairs (named by a caption, by no reference), controls, catch trials; shuffled.

    A catch class must be unrelated to everything in blocked[image].
    """
    test = [(p, "test") for p in sorted(said_by) if p[1] not in named[p[0]]]
    pool = sorted(p for p in said_by if p[1] in named[p[0]])
    picked = [(p, "control") for p in rng.sample(pool, min(n_controls, len(pool)))]
    n_catch = round(catch_rate * (len(test) + len(picked)) / (1 - catch_rate))
    for i in rng.sample(sorted(named), len(named)):
        free = [c for c in CATCH if not related(c, blocked[i])]
        if free and n_catch:
            picked.append(((i, rng.choice(free)), "catch"))
            n_catch -= 1
    items = test + picked
    rng.shuffle(items)
    return [{"image": i, "class": c, "kind": kind, "systems": said_by.get((i, c), [])} for (i, c), kind in items]


def numbered(items: list[dict], section: str) -> dict[str, dict]:
    return {f"{section}-{n:04d}": item for n, item in enumerate(items, 1)}


def public(items: dict[str, dict]) -> list[dict]:
    """What the annotator may see of an item: no kind, no systems."""
    return [{"id": k, "image": v["image"], "class": v["class"]} for k, v in items.items()]


def payload(kit_id: str, title: str, sections: list[dict], files: dict[str, str]) -> dict:
    guide = (SRC / "huong_dan.md").read_text(encoding="utf-8")
    return {"id": kit_id, "title": title, "classes": CLASSES, "groups": GROUPS, "forms": FORMS,
            "gloss": glosses(guide), "images": files, "guide": guide, "sections": sections}


def write_tasks(path: Path, kit: dict) -> None:
    path.write_text("window.KIT = " + json.dumps(kit, ensure_ascii=False) + ";\n", encoding="utf-8")


def prepare_images(files: dict[str, str], src: Path, dst: Path, max_side: int) -> None:
    from PIL import Image

    missing = [f for f in files.values() if not (src / f).exists()]
    if missing:
        raise SystemExit(f"{len(missing)} images are not under {src}, e.g. {missing[:3]}; pass --images-dir")
    dst.mkdir(parents=True, exist_ok=True)
    for f in files.values():
        with Image.open(src / f) as im:
            if max(im.size) > max_side:
                small = im.convert("RGB")
                small.thumbnail((max_side, max_side))
                small.save(dst / f, quality=90)
                continue
        shutil.copyfile(src / f, dst / f)


def zip_dir(folder: Path, dest: Path) -> None:
    """Zip `folder` so that it unpacks to a folder of the same name."""
    with zipfile.ZipFile(dest, "w") as z:
        for p in sorted(folder.rglob("*")):
            if p.is_file():
                kind = zipfile.ZIP_STORED if p.suffix.lower() in (".jpg", ".jpeg", ".png") else zipfile.ZIP_DEFLATED
                z.write(p, Path(folder.name) / p.relative_to(folder), compress_type=kind)


def write_kit(out: Path, kit_id: str, sections: list[dict], files: dict[str, str], images: Path) -> Path:
    """out/<kit_id>/ with html, guideline, README, tasks.js and a copy of `images`; returns the zip."""
    d = out / kit_id
    if d.exists():
        shutil.rmtree(d)
    shutil.copytree(images, d / "images")
    for name in ("gan_nhan.html", "huong_dan.md", "README.md"):
        shutil.copyfile(SRC / name, d / name)
    write_tasks(d / "tasks.js", payload(kit_id, TITLE, sections, files))
    zip_dir(d, out / f"{kit_id}.zip")
    return out / f"{kit_id}.zip"


def kinds(items: dict[str, dict]) -> str:
    n = {k: sum(v["kind"] == k for v in items.values()) for k in ("test", "control", "catch")}
    return f"{len(items)} items = {n['test']} test + {n['control']} control + {n['catch']} catch"


def main() -> int:
    ap = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    ap.add_argument("--out-dir", help="where the kits, zips and key.json go (keep images out of the repo)")
    ap.add_argument("--images-dir", default=None, help="KTVIC images (default $NCS_DATA/datasets/ktvic/images)")
    ap.add_argument("--sample", default=str(ROOT / "data" / "object_gold" / "sample.json"))
    ap.add_argument("--results", default=str(ROOT / "data" / "results"))
    ap.add_argument("--split", default="test_data.json")
    ap.add_argument("--systems", nargs="+", default=SYSTEMS)
    ap.add_argument("--batch2-systems", nargs="+", default=BATCH2)
    ap.add_argument("--controls", type=int, default=200)
    ap.add_argument("--controls2", type=int, default=100, help="controls of the optional second batch")
    ap.add_argument("--catch-rate", type=float, default=0.05)
    ap.add_argument("--seed", type=int, default=42)
    ap.add_argument("--max-side", type=int, default=1280)
    ap.add_argument("--sec-per-item", type=float, default=4.0, help="Part 2 time estimate")
    ap.add_argument("--self-check", action="store_true")
    args = ap.parse_args()
    if args.self_check:
        _check()
        return 0
    if not args.out_dir:
        ap.error("--out-dir is required")

    from evaluate import KTVIC, references

    sample = json.loads(Path(args.sample).read_text(encoding="utf-8"))
    ids = [im["id"] for im in sample["images"]]
    files = {im["id"]: im["file"] for im in sample["images"]}
    refs = references(args.split)
    named = {i: set().union(*map(said, refs[i])) for i in ids}
    results = Path(args.results)
    every = mentioned(results, sorted({*ALL_SYSTEMS, *args.systems, *args.batch2_systems}), ids)
    blocked = {i: set(named[i]) for i in ids}
    for i, c in every:
        blocked[i].add(c)

    rng = random.Random(args.seed)
    part2 = numbered(verify_items(mentioned(results, args.systems, ids), named, args.controls,
                                  args.catch_rate, rng, blocked), "A")
    taken = {(v["image"], v["class"]) for v in part2.values()}
    for i, c in taken:
        blocked[i].add(c)
    rest = {p: runs for p, runs in mentioned(results, args.batch2_systems, ids).items() if p not in taken}
    batch2 = numbered(verify_items(rest, named, args.controls2, args.catch_rate, rng, blocked), "A2")

    out = Path(args.out_dir)
    out.mkdir(parents=True, exist_ok=True)
    with tempfile.TemporaryDirectory(dir=out) as tmp:
        prepare_images(files, Path(args.images_dir) if args.images_dir else KTVIC / "images", Path(tmp),
                       args.max_side)
        zips = [write_kit(out, KIT_ID, [
                    {"key": "B", "kind": "exhaustive", "title": "Phần 1 · Gán đầy đủ", "images": ids},
                    {"key": "A", "kind": "verify", "title": "Phần 2 · Có/không", "items": public(part2)}],
                    files, Path(tmp)),
                write_kit(out, KIT_ID + "-batch2", [
                    {"key": "A2", "kind": "verify", "title": "Phần 3 · Có/không (đợt 2)", "items": public(batch2)}],
                    files, Path(tmp))]
    key = {"kit": KIT_ID, "seed": args.seed, "split": args.split, "systems": args.systems,
           "batch2_systems": args.batch2_systems, "modes": list(MODES), "files": files,
           "sections": {"B": ids, "A": part2, "A2": batch2}}
    (out / "key.json").write_text(json.dumps(key, ensure_ascii=False, indent=1), encoding="utf-8")

    lo, hi = (len(ids) * s / 60 for s in SEC_PER_IMAGE)
    print(f"Part 1 (Task B): {len(ids)} images, ~{lo:.0f}-{hi:.0f} min per annotator at "
          f"{SEC_PER_IMAGE[0]}-{SEC_PER_IMAGE[1]} s/image")
    for name, items, systems in (("Part 2 (Task A)", part2, args.systems),
                                 ("Batch 2 (optional)", batch2, args.batch2_systems)):
        print(f"{name}: {kinds(items)}, ~{len(items) * args.sec_per_item / 60:.0f} min per annotator at "
              f"{args.sec_per_item:g} s/item; systems {', '.join(systems)}")
    asked = {(v["image"], v["class"]) for v in [*part2.values(), *batch2.values()]}
    for system in sorted(set(ALL_SYSTEMS) - {*args.systems, *args.batch2_systems}):
        extra = {p for p in mentioned(results, [system], ids) if p[1] not in named[p[0]]} - asked
        print(f"  not asked: {len(extra)} reference-false pairs only {system} names "
              f"(add it to --systems to verify them)")
    for z in zips:
        print(f"  {z} ({z.stat().st_size / 2**20:.1f} MB)")
    print(f"  {out / 'key.json'} (keep; never send)")
    return 0


def _check() -> None:
    assert len(KNOWN) == len(CLASSES) - len(FOLD) and set(FOLD.values()) <= KNOWN
    assert close({"cô gái"}) == {"cô gái", "phụ nữ", "người"}
    assert close({"đứa trẻ"}) == {"trẻ em", "người"} and close({"bé gái"}) >= {"trẻ em", "phụ nữ", "người"}
    assert close({"xe máy"}) == {"xe máy", "xe"} and close({"nón lá"}) == {"nón lá", "mũ"}
    assert related("người", {"cô gái"}) and related("cô gái", {"người"}) and related("voi", {"vật"})
    assert not related("đàn ông", {"cô gái"}) and not related("ô tô", {"xe máy"})
    assert said("một cô gái trẻ và một đứa trẻ bên chiếc xe máy") == {"cô gái", "trẻ em", "xe máy"}
    gloss = glosses((SRC / "huong_dan.md").read_text(encoding="utf-8"))
    assert {"cửa", "người", "xe", "đồ"} <= gloss.keys(), sorted(gloss)

    named = {"1": {"chó"}, "2": set(), "3": {"bàn"}, "4": set()}
    said_by = {("1", "chó"): ["s-short"], ("1", "mèo"): ["s-short"], ("2", "ghế"): ["s-detailed"],
               ("3", "bàn"): ["s-short", "s-detailed"], ("4", "vật"): ["s-short"]}
    blocked = {i: named[i] | {c for j, c in said_by if j == i} for i in named}
    items = verify_items(said_by, named, 1, 0.25, random.Random(0), blocked)
    by_kind = {k: {(x["image"], x["class"]) for x in items if x["kind"] == k} for k in ("test", "control", "catch")}
    assert by_kind["test"] == {("1", "mèo"), ("2", "ghế"), ("4", "vật")}
    assert len(by_kind["control"]) == 1 and by_kind["control"] <= {("1", "chó"), ("3", "bàn")}
    assert len(by_kind["catch"]) == 1, by_kind
    assert all(not related(c, blocked[i]) for i, c in by_kind["catch"])
    assert not any(i == "4" and c in ("voi", "khỉ", "rắn", "ngựa") for i, c in by_kind["catch"]), "vật blocks animals"
    assert verify_items(said_by, named, 1, 0.25, random.Random(0), blocked) == items, "deterministic for a seed"
    everything = {i: blocked[i] | set(CATCH) for i in named}
    assert not [x for x in verify_items(said_by, named, 0, 0.5, random.Random(1), everything) if x["kind"] == "catch"]
    assert all(set(x) == {"id", "image", "class"} for x in public(numbered(items, "A")))
    with tempfile.TemporaryDirectory() as d:
        write_tasks(Path(d) / "tasks.js", payload("t", "t", [], {"1": "1.jpg"}))
        text = (Path(d) / "tasks.js").read_text(encoding="utf-8")
        kit = json.loads(text.removeprefix("window.KIT = ").removesuffix(";\n"))
        assert kit["gloss"] == gloss and len(kit["classes"]) == 101 and "1." in kit["guide"]
    print("self-check OK")


if __name__ == "__main__":
    raise SystemExit(main())
