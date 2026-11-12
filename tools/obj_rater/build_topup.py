#!/usr/bin/env python
"""Top-up labelling items for new caption sets on XM3600-600 (Paper A, A-E3 arm; run document v1.1 §9.1).

Wraps build_assignment.py (pinned 497e5747, imported unchanged). Rebuilds the base in <out>/_base and requires its four
pinned output sha256; reads the base roles from _base/key.json in memory only; deletes _base; then builds the items for
the (image, class) pairs that only the --extra caption sets name. No caption text is written or printed.

    NCS_DATA=data ~/.venvs/c_stage1_lists/bin/python -B tools/obj_rater/build_topup.py --out ~/vsps_labels/xm600_gold_topup1 \
        --name topup1 --extra <pulled ae3_<key>_xm600-{short,detailed}.preds.json of the models in passed_7a.txt>
    python3 -I -B tools/obj_rater/build_topup.py --selftest      # synthetic fixtures in a temp dir only
"""
from __future__ import annotations

import argparse
import contextlib
import hashlib
import io
import json
import random
import re
import shutil
import sys
import tempfile
import types
from collections import Counter, defaultdict
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))
import build_assignment as B  # noqa: E402

BASE_PINS = {"assignment.json": "55e07337218acc820aafc27659e499ade4ae622cc6eaf41be2f7bb3df510cb2d",
             "practice.json": "e0ed805b31fc623df52f40d7e517cd22f8474fb043d00cb0a167d07ac4fcbbf7",
             "key.json": "a2cef89475675b66867577d399d7050ccf2925abc7a0b04f9572718a85a1c73a",
             "overlap_images.txt": "4f9719667c8a9294dc8cadc9565a048b9b7008ee0c1ecb924317550ba5278273"}
BASE_T1, N_OLD_REPEAT = 1790, 50
L2 = {"tranh", "bức tranh", "mỏm đá"}  # CC-327 L2: Open Images neg narrower than pos; their absent pairs are never asked
EXTRA_RE = re.compile(r"ae3_[a-z0-9_]+_xm600-(short|detailed)")
PUBLIC = B.ROOT / "manuscript" / "prereg" / "2026-11-12_a_e3_arm"


def build_topup(out: Path, name: str, extras: list[Path], public: Path, pins: dict = BASE_PINS) -> dict:
    out = out.expanduser().resolve()
    if str(out).startswith("/mnt/"):
        raise SystemExit("STOP: --out must be on the Linux home filesystem, not /mnt")
    if not re.fullmatch(r"topup[0-9]+", name):
        raise SystemExit("STOP: --name must be topup<N>")
    if out.exists() or public.exists():
        raise SystemExit("STOP: refusing to overwrite an existing output or public dir")
    out.mkdir(parents=True)
    try:
        return _build(out, name, extras, public, pins)
    except BaseException:
        shutil.rmtree(out / "_base", ignore_errors=True)
        if not any(out.iterdir()):
            out.rmdir()
        raise


def _build(out: Path, name: str, extras: list[Path], public: Path, pins: dict) -> dict:
    import xm3600_oiv7 as X
    from rescap.chair import objects_in

    # 1. rebuild the base and prove it; base roles in memory only; delete _base
    base = out / "_base"
    base_rec = B.build(base)
    if base_rec["outputs_sha256"] != pins:
        raise SystemExit("STOP: the rebuilt base differs from the four pinned output sha256")
    key0 = json.loads((base / "key.json").read_text(encoding="utf-8"))
    label_words = json.loads((base / "assignment.json").read_text(encoding="utf-8"))["meta"]["labels"]
    practice = (base / "practice.json").read_bytes()
    overlap0 = (base / "overlap_images.txt").read_text(encoding="utf-8").split()
    n_base_files = len(list(base.iterdir()))
    shutil.rmtree(base)
    print(f"deleted {base.name} ({n_base_files} files)")
    base_t1 = sorted((v["image"], v["class"]) for v in key0.values() if v["part"] == 1 and v["role"] == "target")
    base_foils = {(v["image"], v["class"]) for v in key0.values() if v["role"] == "foil_absent"}

    # 2. base named set, exactly as build() l.58-79
    data = json.loads((B.DS / "test_data.json").read_text(encoding="utf-8"))
    refs = defaultdict(list)
    for a in data["annotations"]:
        refs[str(a["image_id"])].append(a["caption"])
    ids = sorted(refs)
    labels = {k: v for k, v in json.loads(X.LABELS.read_text(encoding="utf-8")).items() if not k.startswith("_")}
    vmap = X.resolve_map(B.DS / "oiv7" / "oidv7-class-descriptions.csv")
    raw_map = {k: v for k, v in json.loads(X.MAP.read_text(encoding="utf-8")).items() if not k.startswith("_")}
    st = X.statuses(vmap, labels)
    systems, _ = B.load_systems()
    named: dict[tuple[str, str], set[str]] = defaultdict(set)
    for sname, p in systems.items():
        for i in ids:
            for c in set(objects_in(p[i])):
                named[(i, c)].add(sname)
    for i in ids:
        for cap in refs[i]:
            for c in set(objects_in(cap)):
                named[(i, c)].add("reference")
    base_named = set(named)
    asked = {(v["image"], v["class"]) for v in key0.values() if v["role"] != "foil_absent"}
    if asked - base_named or base_foils & base_named:
        raise SystemExit("STOP: the recomputed base named set does not match the base key")

    # 3. new systems: LB schema, key `predictions`, exactly the base images
    new_names, ex_sha = [], {}
    for f in extras:
        sname = f.name.removesuffix(".preds.json")
        if not EXTRA_RE.fullmatch(sname) or sname in systems or sname in new_names:
            raise SystemExit(f"STOP: --extra {f.name} is not a new ae3_<key>_xm600-(short|detailed) run")
        d = json.loads(f.read_text(encoding="utf-8"))
        p = d.get("predictions")
        if (d.get("schema") != "vsps.lb_decode.v1" or not isinstance(p, dict) or set(p) != set(ids)
                or not all(isinstance(v, str) for v in p.values())):
            raise SystemExit(f"STOP: --extra {f.name}: not the LB schema with exactly the {len(ids)} images")
        for i in ids:
            for c in set(objects_in(p[i])):
                named[(i, c)].add(sname)
        new_names.append(sname)
        ex_sha[str(f)] = B.sha(f)
    named_new = sorted(set(named) - base_named)

    # 4. items, same buckets and wording as the base
    def bucket(i: str, c: str) -> str:
        return "unmapped" if c not in vmap else st.get(i, {}).get(c, "unknown")

    rng = random.Random(f"{B.SEED}|{name}")
    targets1 = [p for p in named_new if bucket(*p) == "unknown"]
    targets2 = [p for p in named_new if bucket(*p) == "unmapped"]
    absent = [p for p in named_new if bucket(*p) == "absent"]
    named_abs = [p for p in absent if p[1] not in L2]
    named_pre = [p for p in named_new if bucket(*p) == "present"]
    t1 = len(targets1)
    n_pre, n_foil, n_rep = (round(k * t1 / BASE_T1) for k in (B.N_CTRL_PRESENT, B.N_FOIL, B.N_REPEAT))
    ctrl_pre = sorted(rng.sample(named_pre, min(n_pre, len(named_pre))))
    foil_all = sorted((i, c) for i in ids for c, s in st.get(i, {}).items()
                      if s == "absent" and (i, c) not in named and (i, c) not in base_foils)
    foil_pool = [p for p in foil_all if p[1] not in L2]
    foils = sorted(rng.sample(foil_pool, min(n_foil, len(foil_pool))))
    old_rep = sorted(rng.sample(base_t1, min(N_OLD_REPEAT, len(base_t1))))
    repeats = sorted(rng.sample(targets1, min(n_rep, len(targets1))))

    key, screens = {}, []

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
                q = hashlib.sha256(f"{B.SEED}|{name}|{part}|{i}|{c}".encode()).hexdigest()[:12]
                if q in key or q in key0:
                    raise SystemExit("STOP: qid collision with the base or within the top-up")
                key[q] = {"image": i, "class": c, "part": part, "role": role, "bucket": bucket(i, c),
                          "named_by": sorted(named.get((i, c), []))}
                pos = raw_map.get(c, {}).get("pos") or []
                q_out.append({"qid": q, "label": c, "hint": ("Open Images: " + ", ".join(pos)) if pos else ""})
            screens.append({"sid": f"{name}-p{part}-{i}", "part": part, "image": f"images/{i}.jpg", "q": q_out})

    add_part(1, [(i, c, "target") for i, c in targets1] + [(i, c, "ctrl_absent") for i, c in named_abs]
             + [(i, c, "ctrl_present") for i, c in ctrl_pre] + [(i, c, "foil_absent") for i, c in foils]
             + [(i, c, "old_repeat") for i, c in old_rep])
    add_part(2, [(i, c, "target") for i, c in targets2])
    add_part(3, [(i, c, "repeat") for i, c in repeats])

    # 5-6. overlap, outputs, public copy without key.json
    need = {i for i, _ in targets1 + targets2}
    overlap = sorted(set(overlap0) & need)
    n_q = sum(len(s["q"]) for s in screens)
    meta = {"name": f"xm600_gold_completion_{name}", "seed": f"{B.SEED}|{name}", "labels": label_words,
            "n_screens": len(screens), "n_questions": n_q}
    ovl, rec_name = f"overlap_images_{name}.txt", f"BUILD_{name.upper()}.json"
    for fname, obj in {"assignment.json": {"meta": meta, "screens": screens}, "key.json": key}.items():
        (out / fname).write_text(json.dumps(obj, ensure_ascii=False, sort_keys=True, indent=1), encoding="utf-8")
    (out / "practice.json").write_bytes(practice)
    (out / ovl).write_text("\n".join(overlap) + "\n", encoding="utf-8")
    by_part: dict[str, dict[str, int]] = defaultdict(dict)
    for (part, role), n in sorted(Counter((v["part"], v["role"]) for v in key.values()).items()):
        by_part[f"part{part}"][role] = n
    counts = {"images": len(ids), "base_systems": sorted(systems), "new_systems": sorted(new_names),
              "base_named_pairs": len(base_named), "new_named_pairs": len(named_new), "t1_new_part1_targets": t1,
              "formula_n": {"ctrl_present": n_pre, "foil_absent": n_foil, "repeat": n_rep, "old_repeat": N_OLD_REPEAT},
              "by_part_role": by_part, "l2_named_absent_not_asked": len(absent) - len(named_abs),
              "l2_absent_left_out_of_foil_pool": len(foil_all) - len(foil_pool), "screens": len(screens),
              "questions": n_q, "images_with_targets": len(need), "overlap_images": len(overlap)}
    rec = {"counts": counts,
           "inputs_sha256": {**ex_sha, "data/datasets/xm3600/test_data.json": B.sha(B.DS / "test_data.json"),
                             "tools/obj_rater/build_assignment.py": B.sha(Path(B.__file__)),
                             "tools/obj_rater/build_topup.py": B.sha(Path(__file__))},
           "base_check": {"pinned_outputs_sha256": pins, "rebuilt_equal": True, "base_dir_deleted": True,
                          "base_inputs_sha256": base_rec["inputs_sha256"]},
           "outputs_sha256": {n: B.sha(out / n) for n in ("assignment.json", "practice.json", "key.json", ovl)}}
    (out / rec_name).write_text(json.dumps(rec, ensure_ascii=False, indent=1), encoding="utf-8")
    public.mkdir(parents=True)
    for fname in ("assignment.json", "practice.json", ovl, rec_name):
        shutil.copyfile(out / fname, public / fname)
    return rec


# ------------------------------------------------------------------------------------------- selftest (synthetic)

def _fixture(fx: Path) -> dict:
    r = random.Random(7)
    mapped = [f"m{k:02d}" for k in range(40)] + sorted(L2)
    vocab = sorted(mapped + [f"u{k:02d}" for k in range(15)])
    ids = [f"{k:016x}" for k in range(1, 81)]
    outside = [f"{k:016x}" for k in range(1001, 1021)]

    def cap(k: int) -> str:
        return ";".join(r.sample(vocab, k) + ["SENTINELCAP"])

    labels = {i: {c: s for c in mapped if (s := r.choices(["present", "absent", None],
                                                           [.1, .7, .2] if c in L2 else [.3, .3, .4])[0])}
              for i in ids + outside}
    base = {"a/xm3600_s1-short.preds.json": {i: cap(4) for i in ids},
            "a/xm3600_s1-detailed.preds.json": {i: [cap(6)] for i in ids},
            "g2b/g2b_q3_xm600-short-T0.preds.json": {"predictions": {i: cap(4) for i in ids}}}
    refs = [{"image_id": i, "caption": cap(3)} for i in ids for _ in range(2)]
    new = {f"pull/ae3_{k}_xm600-{m}.preds.json": {"schema": "vsps.lb_decode.v1", "predictions": {i: cap(8) for i in ids}}
           for k, m in (("aa", "short"), ("bb", "detailed"))}
    files = {**base, **new, "labels.json": labels, "map.json": {c: {"pos": [f"OI {c}"]} for c in mapped},
             "ds/test_data.json": {"annotations": refs}}
    for rel, obj in files.items():
        (fx / rel).parent.mkdir(parents=True, exist_ok=True)
        (fx / rel).write_text(json.dumps(obj, ensure_ascii=False), encoding="utf-8")
    (fx / "ds" / "images").mkdir()
    for i in outside:
        (fx / "ds" / "images" / f"{i}.jpg").write_bytes(b"")
    caps = [p.get("predictions", p) for p in base.values()] + [{d["image_id"]: d["caption"] for d in refs[::2]},
                                                                {d["image_id"]: d["caption"] for d in refs[1::2]}]
    return {"ids": ids, "vocab": set(vocab), "labels": labels, "mapped": set(mapped), "base_caps": caps,
            "new_caps": [d["predictions"] for d in new.values()], "extras": [fx / k for k in new]}


def selftest() -> int:
    n_ok = 0

    def check(cond: bool, what: str) -> None:
        nonlocal n_ok
        if not cond:
            raise SystemExit(f"SELFTEST FAIL: {what}")
        n_ok += 1
        print(f"ok {n_ok:2d} {what}")

    def stops(fn) -> bool:
        try:
            with contextlib.redirect_stdout(io.StringIO()):
                fn()
        except SystemExit as e:
            return str(e).startswith("STOP")
        return False

    with tempfile.TemporaryDirectory() as td:
        fx = Path(td)
        F = _fixture(fx)
        B.ROOT, B.A_DIR, B.G2B_DIR, B.DS, B.IMG_DIR = fx, fx / "a", fx / "g2b", fx / "ds", fx / "ds" / "images"
        X = types.ModuleType("xm3600_oiv7")
        X.LABELS, X.MAP = fx / "labels.json", fx / "map.json"
        X.resolve_map = lambda _csv: json.loads(X.MAP.read_text(encoding="utf-8"))
        X.statuses = lambda vmap, labels: {i: {c: s for c, s in d.items() if c in vmap} for i, d in labels.items()}
        chair = types.ModuleType("rescap.chair")
        chair.objects_in = lambda t: [w for w in t.split(";") if w in F["vocab"]]
        sys.modules.update({"xm3600_oiv7": X, "rescap": types.ModuleType("rescap"), "rescap.chair": chair})

        with contextlib.redirect_stdout(io.StringIO()):
            pins = B.build(fx / "probe")["outputs_sha256"]
        key0 = json.loads((fx / "probe" / "key.json").read_text(encoding="utf-8"))
        ex = F["extras"]
        args = ("topup1", ex)

        check(stops(lambda: build_topup(Path("/mnt/never_topup_selftest"), *args, fx / "p0")), "refuses an --out under /mnt")
        bad = {**pins, "key.json": "0" * 64}
        check(stops(lambda: build_topup(fx / "o_bad", *args, fx / "p_bad", bad))
              and not (fx / "o_bad").exists() and not (fx / "p_bad").exists(), "base-pin mismatch stops, nothing left")
        short = fx / "pull" / "ae3_cc_xm600-short.preds.json"
        short.write_text(json.dumps({"schema": "vsps.lb_decode.v1", "predictions": dict(
            list(F["new_caps"][0].items())[:-1])}), encoding="utf-8")
        check(stops(lambda: build_topup(fx / "o_short", "topup1", [short], fx / "p_short", pins))
              and not (fx / "o_short").exists(), "an --extra file missing an image stops, _base and out removed")

        buf = io.StringIO()
        with contextlib.redirect_stdout(buf):
            rec = build_topup(fx / "o1", *args, fx / "p1", pins)
        o1, p1 = fx / "o1", fx / "p1"
        check(not (o1 / "_base").exists() and "deleted _base" in buf.getvalue(), "_base deleted and the deletion logged")
        check(stops(lambda: build_topup(o1, *args, fx / "p9", pins)), "refuses to overwrite an existing --out")
        key = json.loads((o1 / "key.json").read_text(encoding="utf-8"))
        check(not set(key) & set(key0), "top-up qids disjoint from every base qid")
        check(all(q == hashlib.sha256(f"{B.SEED}|topup1|{v['part']}|{v['image']}|{v['class']}".encode()).hexdigest()[:12]
                  for q, v in key.items()), "qid = sha256(SEED|topup1|part|image|class)[:12]")

        base_named = {(i, c) for d in F["base_caps"] for i, t in d.items()
                      for c in (t[0] if isinstance(t, list) else t).split(";") if c in F["vocab"]}
        new_named = {(i, c) for d in F["new_caps"] for i, t in d.items() for c in t.split(";") if c in F["vocab"]} - base_named
        new_names = {"ae3_aa_xm600-short", "ae3_bb_xm600-detailed"}
        tgt = [v for v in key.values() if v["role"] in ("target", "repeat")]
        check(bool(tgt) and all((v["image"], v["class"]) not in base_named and v["named_by"]
                                and set(v["named_by"]) <= new_names for v in tgt),
              "no top-up target or repeat is in the base named set; each is named by a new system only")

        def st(i: str, c: str) -> str:
            return "unmapped" if c not in F["mapped"] else F["labels"][i].get(c, "unknown")

        roles = Counter((v["part"], v["role"]) for v in key.values())
        t1 = sum(st(*p) == "unknown" for p in new_named)
        pool_pre = sum(st(*p) == "present" for p in new_named)
        n_pre, n_foil, n_rep = (round(k * t1 / 1790) for k in (200, 100, 150))
        check(0 < n_pre <= pool_pre and 0 < n_foil and 0 < n_rep <= t1 and roles[(1, "target")] == t1
              and roles[(1, "ctrl_present")] == n_pre and roles[(1, "foil_absent")] == n_foil
              and roles[(3, "repeat")] == n_rep
              and roles[(2, "target")] == sum(st(*p) == "unmapped" for p in new_named)
              and roles[(1, "ctrl_absent")] == sum(st(*p) == "absent" and p[1] not in L2 for p in new_named),
              f"counts follow the formulas (t1 {t1}: ctrl_present {n_pre}, foils {n_foil}, repeats {n_rep})")
        check(rec["counts"]["by_part_role"]["part1"] == {r: n for (p, r), n in roles.items() if p == 1},
              "BUILD_TOPUP1 counts by part and role equal key.json")
        base_t1 = {(v["image"], v["class"]) for v in key0.values() if v["part"] == 1 and v["role"] == "target"}
        old = [(v["image"], v["class"]) for v in key.values() if v["role"] == "old_repeat"]
        check(len(base_t1) > 50 and len(old) == 50 and set(old) <= base_t1 and all(
            v["part"] == 1 for v in key.values() if v["role"] == "old_repeat"), "old_repeat = 50 base part-1 targets, in part 1")
        base_foils = {(v["image"], v["class"]) for v in key0.values() if v["role"] == "foil_absent"}
        foils = [(v["image"], v["class"]) for v in key.values() if v["role"] == "foil_absent"]
        check(all(st(*p) == "absent" and p not in base_named and p not in new_named and p not in base_foils for p in foils),
              "foils: verified absent, unnamed by anyone, not a base foil")
        c = rec["counts"]
        check(c["l2_named_absent_not_asked"] > 0 and c["l2_absent_left_out_of_foil_pool"] > 0 and not any(
            v["class"] in L2 and v["bucket"] == "absent" for v in key.values()),
              "CC-327 L2 absent pairs never become controls or foils (excluded counts > 0 printed)")
        asg = json.loads((o1 / "assignment.json").read_text(encoding="utf-8"))
        check(all(s["sid"].startswith("topup1-p") and set(s) == {"sid", "part", "image", "q"}
                  and all(set(q) == {"qid", "label", "hint"} for q in s["q"]) for s in asg["screens"]),
              "screen ids prefixed topup1-; served items carry no role or system")
        check((o1 / "practice.json").read_bytes() == (fx / "probe" / "practice.json").read_bytes(),
              "practice.json byte-equal to the base")
        need = {v["image"] for v in key.values() if v["role"] == "target"}
        base_ovl = set((fx / "probe" / "overlap_images.txt").read_text(encoding="utf-8").split())
        check((o1 / "overlap_images_topup1.txt").read_text(encoding="utf-8").split() == sorted(base_ovl & need),
              "overlap = base overlap images with a top-up target")
        check(sorted(x.name for x in p1.iterdir()) == ["BUILD_TOPUP1.json", "assignment.json", "overlap_images_topup1.txt",
                                                      "practice.json"]
              and all((p1 / x.name).read_bytes() == (o1 / x.name).read_bytes() for x in p1.iterdir()),
              "public copy = all outputs except key.json, byte-equal")
        check(rec["inputs_sha256"][str(ex[0])] == B.sha(ex[0]) and rec["inputs_sha256"][str(ex[1])] == B.sha(ex[1])
              and rec["base_check"]["pinned_outputs_sha256"] == pins, "BUILD_TOPUP1 holds every --extra sha and the base check")
        blob = buf.getvalue() + json.dumps(rec) + "".join(x.read_text(encoding="utf-8") for x in o1.iterdir())
        check("SENTINELCAP" not in blob, "no caption text in any output or in stdout")

        with contextlib.redirect_stdout(io.StringIO()):
            build_topup(fx / "o2", *args, fx / "p2", pins)
        check(all((o1 / x.name).read_bytes() == (fx / "o2" / x.name).read_bytes() for x in o1.iterdir())
              and sorted(x.name for x in o1.iterdir()) == sorted(x.name for x in (fx / "o2").iterdir()),
              "determinism: two builds byte-equal")
        for fname in ("assignment.json", "key.json", "overlap_images_topup1.txt"):  # compare across two processes
            print(f"fixture sha256 {fname} {B.sha(o1 / fname)}")
    print(f"SELFTEST PASS {n_ok}/{n_ok}")
    return 0


def main() -> int:
    ap = argparse.ArgumentParser()
    ap.add_argument("--selftest", action="store_true")
    ap.add_argument("--out")
    ap.add_argument("--name", default="topup1")
    ap.add_argument("--extra", nargs="+")
    ap.add_argument("--public", help="public copy dir (default manuscript/prereg/2026-11-12_a_e3_arm/<name>)")
    a = ap.parse_args()
    if a.selftest:
        return selftest()
    if not (a.out and a.extra):
        ap.error("--out and --extra are required")
    rec = build_topup(Path(a.out), a.name, [Path(f) for f in a.extra], Path(a.public) if a.public else PUBLIC / a.name)
    print(json.dumps(rec["counts"], ensure_ascii=False, indent=1))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
