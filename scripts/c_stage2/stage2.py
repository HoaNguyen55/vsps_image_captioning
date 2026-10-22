#!/usr/bin/env python3
"""Paper C stage 2 (STAGE 2 / DEV-B, ONE LOOK): pins, the two dev-B sets, the carve-out refusal, the frozen run
grid and the operator checks. Prereg manuscript/prereg/2026-10-22_c_stage2/PREREG.md §1.2, §2-§4, §12 items 2-4.

The stage-1 modules are imported unchanged; their sha256 must match the stage-1 SHA256SUMS before any import.

  python scripts/c_stage2/stage2.py --selftest                                   CPU, no data
  python scripts/c_stage2/stage2.py runs --set S [--model M] [--arm A ...]       run ids of the frozen grid
  python scripts/c_stage2/stage2.py verify-arms --model M                        arms whose items are verified
  python scripts/c_stage2/stage2.py check-host --block ov|xm --lists L            CPU, on M3 (§1.2)
  python scripts/c_stage2/stage2.py subsets --lists L --openviic-dev F --xm-full F --out-dir D   CPU, local
"""
from __future__ import annotations

import argparse
import hashlib
import json
import os
import sys
import tempfile
from pathlib import Path

HERE = Path(__file__).resolve().parent
ROOT = HERE.parents[1]
S1_SUMS = ROOT / "manuscript/prereg/2026-10-22_c_stage1/SHA256SUMS"


def sha_file(p: Path) -> str:
    h = hashlib.sha256()
    with open(p, "rb") as f:
        for b in iter(lambda: f.read(1 << 20), b""):
            h.update(b)
    return h.hexdigest()


def check_stage1() -> None:
    """Stage 2 imports scripts/c_stage1 unchanged: every stage-1 file must match the stage-1 SHA256SUMS."""
    for line in S1_SUMS.read_text(encoding="utf-8").splitlines():
        h, rel = line.split(maxsplit=1)
        if rel.startswith("scripts/c_stage1/") and sha_file(ROOT / rel) != h:
            raise SystemExit(f"{rel}: differs from the stage-1 SHA256SUMS")


check_stage1()
sys.path.insert(0, str(ROOT / "scripts/c_stage1"))
import decode_icl as C  # noqa: E402
import guard as G  # noqa: E402

lb = C.lb
LABEL = "STAGE 2 / DEV-B, ONE LOOK"
SCHEMA = "vsps.c_stage2.v1"
PREREG = "manuscript/prereg/2026-10-22_c_stage2/PREREG.md"
FROZEN = "manuscript/prereg/2026-10-22_c_stage2/frozen_config.json"
OVT60 = "manuscript/prereg/2026-10-22_c_stage2/ov_test_dev299_neardup_files.txt"
PTB = "scripts/kit_b/ptb_protocol.py"
PINS = {PREREG: "6d039398c88ab00c5c303b671552b3f7c550d4d1a0c55e388ce7c03b249570b6",
        FROZEN: "2f0c32be7720b672f6e4aae229aba69da8742e0f9e32d34c5137e985ea36aa16",
        OVT60: "737e617a966478d9bcadb0c932d72a6f8de7dd5c7e83c98730e1a88720f2f41f",
        PTB: "ea5fbe6e1528e339abfcb9ba00bdd0c4d4e4bde07ae6edd30fffaa72d60754d2"}
EMB1_SHA256 = "59e65f6f6432af97504c59c72fa07b644acbff26938e1365473fad659421f7c0"  # stage-1 emb.npz (§5.1)
SETS = {"ov_dev_b": {"src": "openviic", "image_dir": "openviic/images", "n": 925},
        "xm_dev500": {"src": "xm3600", "image_dir": "c_xm_dev500/images", "n": 500}}
C.DATASETS.update({k: {"src": v["src"], "image_dir": v["image_dir"]} for k, v in SETS.items()})  # for C.shown etc.
OV_DEV_ANN = "datasets/openviic/uit-openviic-annotation-dev.json"  # the 1,836-key subset (§1.2)
XM_REFS = "datasets/c_xm_dev500/xm_dev500_data.json"  # the 500-image reference subset (§1.2)
TAUS = tuple({float("inf"): "inf", -float("inf"): "-inf"}.get(t, f"{t:.2f}") for t in G.TAUS)
INFINITE = ("-inf", "inf")
ARMS = ("ret", "rand", "fix", "zs", "blind")
MAIN = ("ret", "rand", "fix", "zs")


def pinned(rel: str) -> Path:
    p = ROOT / rel
    if sha_file(p) != PINS[rel]:
        raise SystemExit(f"{rel}: sha256 differs from the stage-2 pin")
    return p


# ------------------------------------------------------------------------------------------------ frozen grid
def tau_g(tau: str) -> str:
    """C-a (CC-087, CC-093): tau_G = tau if finite, else 0.0."""
    return "0.00" if tau in INFINITE else tau


def frozen(path: Path | None = None) -> dict:
    """frozen_config.json, pinned by sha256 (a selftest passes a dummy path, unpinned)."""
    cfg = json.loads((path or pinned(FROZEN)).read_text(encoding="utf-8"))
    if set(cfg["models"]) != set(C.MODELS):
        raise SystemExit("frozen config: not the two backbones")
    for m, c in cfg["models"].items():
        ok = (c["k"] in C.KS and c["order"] in ("first", "last") and c["tpl"] in C.TAILS and c["tau"] in TAUS
              and c["tau_G"] == tau_g(c["tau"]))
        if not ok:
            raise SystemExit(f"frozen config: {m} is not a registered configuration with the tau_G rule")
    return cfg


def spec(cfg: dict, ds: str, model: str, arm: str) -> dict:
    c = cfg["models"][model]
    k, o, t = c["k"], c["order"], c["tpl"]
    tag = {"ret": f"ret-k{k}-{o}-{t}", "rand": f"rand-k{k}-{t}", "fix": f"fix-k{k}-{t}", "zs": "zs",
           "blind": f"blind-k{k}-{o}-{t}"}[arm]
    return {"run_id": f"c2_{model}_{ds}-{tag}", "dataset": ds, "model": model, "arm": arm,
            "k": 0 if arm == "zs" else k, "order": o if arm in ("ret", "blind") else None,
            "tpl": None if arm == "zs" else t}


def grid(cfg: dict) -> dict[str, dict]:
    """The 16 main runs and the 4 image-blind runs of §4, by run id."""
    out = {}
    for ds in SETS:
        for m in C.MODELS:
            for arm in ARMS:
                s = spec(cfg, ds, m, arm)
                out[s["run_id"]] = s
    return out


def verify_arms(cfg: dict, model: str) -> list[str]:
    """§5.3 (C-a): ret items are always verified; rand and fix only when the frozen tau is finite."""
    return ["ret"] if cfg["models"][model]["tau"] in INFINITE else ["ret", "rand", "fix"]


# ------------------------------------------------------------------------------------------------ carve-out
def carve(lists: dict) -> tuple[set[str], set[str]]:
    """(image sha256s, OpenViIC file names) carved out of the stage-1 refusal: exactly the 925 OV-dev-B and 500
    XM-dev500 entries. Two OV-dev-B files of the release are byte-identical, so the 925 files hold 924 shas."""
    b, x = lists["sets"]["ov_dev_b"], lists["sets"]["xm_dev500"]
    sb, sx, files = {r[2] for r in b}, {r[2] for r in x}, {r[1] for r in b}
    if (len(b), len(x), len(files), len(sx)) != (925, 500, 925, 500) or sb & sx:
        raise SystemExit("carve-out: not exactly 925 OV-dev-B + 500 XM-dev500 images")
    return sb | sx, files


def refused2(lists: dict) -> tuple[dict[str, set[str]], set[str]]:
    """§12 item 3: the stage-1 refusal minus exactly the carve-out, with the asserts that keep the test sets refused."""
    ids, hashes = C.refused(lists)
    ex = json.loads(C.pinned(C.EXCL).read_text(encoding="utf-8"))
    shas, files = carve(lists)
    xm_dev = {r[2] for r in lists["sets"]["xm_dev500"]}
    if not (shas <= hashes and files <= ids["openviic"]):
        raise SystemExit("carve-out: a carved-out image was not refused in stage 1")
    for name, v in ex["image_sha256"].items():
        if (shas if name != "xm3600_all_images" else shas - xm_dev) & set(v):
            raise SystemExit(f"carve-out: a carved-out image is in exclusion.json {name}")
    if {r[0] for r in lists["sets"]["xm_dev500"]} & ids["xm3600"]:
        raise SystemExit("carve-out: an XM600 id is in XM-dev500")
    ids2, hashes2 = {**ids, "openviic": ids["openviic"] - files}, hashes - shas
    stay = [set(v) for n, v in ex["image_sha256"].items() if n != "xm3600_all_images"]
    stay += [set(ex["image_sha256"]["xm3600_all_images"]) - xm_dev, {r[2] for r in lists["sets"]["xm_test2500"]},
             set(lists["refuse"]["image_sha256"]) - shas]
    if not all(s <= hashes2 for s in stay) or ids2["xm3600"] != ids["xm3600"] or ids2["ktvic"] != ids["ktvic"]:
        raise SystemExit("carve-out: a test set would no longer be refused")
    return ids2, hashes2


def manifest2(ds: str, lists: dict) -> list[tuple[str, str, str]]:
    """[(id, file, sha256)] of a stage-2 set; refused unless every row is in that set's carve-out."""
    if ds not in SETS:
        raise SystemExit(f"REFUSED: stage 2 decodes only {sorted(SETS)}, not {ds}")
    rows = [tuple(r) for r in lists["sets"][ds]]
    if len({r[0] for r in rows}) != len(rows) or any(len(r) != 3 for r in rows) or len(rows) != SETS[ds]["n"]:
        raise SystemExit(f"{ds}: not {SETS[ds]['n']} distinct (id, file, sha256) rows")
    C.refuse_rows(rows, SETS[ds]["src"], *refused2(lists))
    test60 = set(pinned(OVT60).read_text(encoding="utf-8").split())
    if {f for _i, f, _h in rows} & test60:  # the 1,941 exclusion is an OV-test rule; dev-B never holds one
        raise SystemExit("REFUSED: an OV-test near-duplicate of dev299 is in a dev-B set")
    return rows


def check_folder(ds: str, lists: dict, data: Path | None = None) -> None:
    """§12 item 3: refuse a file in the XM-dev500 folder that is not an XM-dev500 image."""
    if ds != "xm_dev500":
        return
    folder = (data or lb.DATA) / "datasets" / SETS[ds]["image_dir"]
    ok = {r[2] for r in lists["sets"][ds]}
    bad = [p.name for p in sorted(folder.iterdir()) if p.is_file() and sha_file(p) not in ok]
    if bad:
        raise SystemExit(f"REFUSED: {len(bad)} file(s) in {folder} are not XM-dev500 images, e.g. {bad[:3]}")


# ------------------------------------------------------------------------------------------------ references
def references2(ds: str, lists: dict, data: Path | None = None) -> dict[str, list[str]]:
    """{image id: references} of a stage-2 set, from the §1.2 subset files, read at run time from $NCS_DATA."""
    data = data or lb.DATA
    ids = {i for i, _f, _h in manifest2(ds, lists)}
    if ds == "ov_dev_b":
        ann = json.loads((data / OV_DEV_ANN).read_text(encoding="utf-8"))
        if set(ann) != {r[0] for r in lists["sets"]["ov_dev_a"]} | ids:
            raise SystemExit(f"{OV_DEV_ANN}: not the 1,836-key subset of OV-dev-A and OV-dev-B")
        return {f: [c.strip() for c in ann[f]["captions"]] for f in ids}
    d = json.loads((data / XM_REFS).read_text(encoding="utf-8"))
    if {str(i["id"]) for i in d["images"]} != ids:
        raise SystemExit(f"{XM_REFS}: not the 500 XM-dev500 images")
    out: dict[str, list[str]] = {}
    for a in d["annotations"]:
        out.setdefault(str(a["image_id"]), []).append(a["caption"])
    if set(out) != ids:
        raise SystemExit(f"{XM_REFS}: an XM-dev500 image has no reference")
    return out


def cmd_subsets(a) -> None:
    """The two §1.2 subset files, values unchanged (json.dump, ensure_ascii=False, as CC-084 D1). Local, CPU."""
    if os.environ.get("VSPS_MACHINE_ID"):
        raise SystemExit("subsets runs locally, where the releases are; not on a GPU host")
    lists = C.load_lists(a.lists)
    keep = {r[0] for r in lists["sets"]["ov_dev_a"]} | {r[0] for r in lists["sets"]["ov_dev_b"]}
    ann = json.loads(Path(a.openviic_dev).read_text(encoding="utf-8"))
    sub = {k: v for k, v in ann.items() if k in keep}
    xm_ids = {r[0] for r in lists["sets"]["xm_dev500"]}
    full = json.loads(Path(a.xm_full).read_text(encoding="utf-8"))
    xm = {"images": [i for i in full["images"] if str(i["id"]) in xm_ids],
          "annotations": [x for x in full["annotations"] if str(x["image_id"]) in xm_ids]}
    if len(sub) != 1836 or len(xm["images"]) != 500:
        raise SystemExit(f"subsets: {len(sub)} OpenViIC keys, {len(xm['images'])} XM images")
    out = Path(a.out_dir)
    for name, obj in (("uit-openviic-annotation-dev.json", sub), ("xm_dev500_data.json", xm)):
        with open(out / name, "w", encoding="utf-8") as f:
            json.dump(obj, f, ensure_ascii=False)
        print(json.dumps({"file": name, "sha256": sha_file(out / name), "keys": len(obj) if name[0] == "u"
                          else len(obj["images"]), "release_sha256": sha_file(Path(
                              a.openviic_dev if name[0] == "u" else a.xm_full))}))


# ------------------------------------------------------------------------------------------------ host check
def check_host(block: str, lists: dict, data: Path | None = None, repo: Path = ROOT) -> dict:
    """§1.2 operator re-check before a block. Fails on: the CC-079 refused set (lists.json `refuse`: OV-test, the
    B-raw cut, XM3600) minus the carve-out, an OpenViIC test name, absent-file violations, the OV-dev annotation
    subset, and (X2, F3) any XM-dev500 image before the XM block. Other papers' test images (exclusion.json lists:
    KTVIC test, UIT-ViIC test, CV295, CHAIR-500) are on M3 by design and are counted only; stage-2 code refuses
    them by sha anyway. Records the sha256 of every carved-out image present (§12 item 12)."""
    data = data or lb.DATA
    ds_dir = data / "datasets"
    ids2, _hashes2 = refused2(lists)
    shas_c, _files = carve(lists)
    fail = set(lists["refuse"]["image_sha256"]) - shas_c
    present = sorted(p.name for p in ds_dir.iterdir())
    bad = [n for n in ("xm3600", "xm3600_en", "e_dev_a_pairs") if n in present]
    bad += [str(p) for root in (repo, data) for p in root.rglob("oiv7_labels.json")]
    bad += [n for n in ("uit-openviic-annotation-test.json",) if (ds_dir / "openviic" / n).exists()]
    if block == "ov" and "c_xm_dev500" in present:
        bad.append("c_xm_dev500 present before the XM block (F3)")
    files = [p for p in ds_dir.rglob("*") if p.is_file() and p.suffix.lower() in (".jpg", ".jpeg", ".png")]
    shas = {p: sha_file(p) for p in files}
    ov_names = ids2["openviic"]
    hit = [str(p) for p, h in shas.items() if h in fail or (p.parent == ds_dir / "openviic/images" and p.name in
                                                            ov_names)]
    xm_dev = {r[2] for r in lists["sets"]["xm_dev500"]}
    if block == "ov":
        hit += [str(p) for p, h in shas.items() if h in xm_dev]
    else:
        check_folder("xm_dev500", lists, data)
    ex = json.loads(C.pinned(C.EXCL).read_text(encoding="utf-8"))["image_sha256"]
    have = set(shas.values())
    copied = {s_: {p.name: h for p, h in sorted(shas.items()) if p.parent == ds_dir / SETS[s_]["image_dir"]
                   and h in {r[2] for r in lists["sets"][s_]}} for s_ in (["ov_dev_b"] if block == "ov" else SETS)}
    for s_, got in copied.items():
        if len(got) != SETS[s_]["n"]:
            bad.append(f"{len(got)}/{SETS[s_]['n']} {s_} images present")
    references2("ov_dev_b", lists, data)  # the 1,836-key subset
    rec = {"block": block, "utc": lb.utc(), "datasets": present, "image_files": len(files),
           "refused_present": len(hit), "problems": bad, "ov_dev_ann_sha256": sha_file(data / OV_DEV_ANN),
           "other_papers_test_images_present": {n: len(have & set(v)) for n, v in ex.items()},
           "copied_sha256": copied}
    if block == "xm":
        rec["xm_refs_sha256"] = sha_file(data / XM_REFS)
    if hit or bad:
        print(json.dumps({k: v for k, v in rec.items() if k != "copied_sha256"} | {"examples": hit[:3]}))
        raise SystemExit("host check failed: back to the operator")
    return rec


def fake_host(tmp: Path, lists: dict) -> Path:
    """A synthetic $NCS_DATA for the host check: file contents are the made-up names fake_lists hashes."""
    data = tmp / "ncs"
    img = data / "datasets/openviic/images"
    img.mkdir(parents=True)
    for _i, f, _h in lists["sets"]["ov_dev_b"]:
        (img / f).write_text(f.removesuffix(".jpg"))
    keys = [r[0] for r in lists["sets"]["ov_dev_a"] + lists["sets"]["ov_dev_b"]]
    (data / OV_DEV_ANN).write_text(json.dumps({k: {"captions": ["w1"]} for k in keys}), encoding="utf-8")
    (data / "datasets/ktvic/images").mkdir(parents=True)
    (data / "datasets/ktvic/images/k1.jpg").write_text("k1")
    return data


# ------------------------------------------------------------------------------------------------ zero-shot inputs
def zs_ok2(prov: dict, model: str, ds: str) -> None:
    """§12 item 7: a zero-shot input is a stage-2 zs file decoded by stage-2 code; no dev-pool or E reuse path."""
    reg = C.registration()
    m = reg["models"][model]
    same = tuple(prov.get(k) for k in ("hub_id", "revision", "prompt_text_sha256", "max_new_tokens",
                                        "generate_kwargs", "dataset", "packages")) == (
        m["hub_id"], m["revision"], C.ZS_PROMPT_SHA256, 60, {"max_new_tokens": 60, "do_sample": False, "num_beams": 1},
        ds, reg["venv"]["packages"])
    spec_ = prov.get("spec")
    own = (prov.get("c_schema") == SCHEMA and isinstance(spec_, dict) and spec_.get("arm") == "zs"
           and prov.get("run_id", "").startswith("c2_") and prov.get("wrapper_sha256") == sha_file(HERE / "decode2.py"))
    if not (same and own):
        raise SystemExit(f"{prov.get('run_id')}: not a stage-2 zero-shot run of {model} on {ds}")


# ------------------------------------------------------------------------------------------------ self-test (CPU)
def fake_lists(tmp: Path) -> tuple[Path, dict]:
    """Synthetic lists with made-up ids: carve-out sets of the registered sizes, test and memory rows."""
    h = lambda s: hashlib.sha256(s.encode()).hexdigest()  # noqa: E731
    b = [[f"b{n}.jpg", f"b{n}.jpg", h(f"b{n}")] for n in range(925)]
    x = [[f"x{n}", f"x{n}.jpg", h(f"x{n}")] for n in range(500)]
    t = [[f"t{n}", f"t{n}.jpg", h(f"t{n}")] for n in range(3)]
    lists = {"design_sha256": C.PINS[C.DESIGN], "sets": {"ov_dev_a": [["a1.jpg", "a1.jpg", h("a1")]],
                                                         "ov_dev_b": b, "xm_dev500": x, "xm_test2500": t},
             "refuse": {"openviic_files": ["ot1.jpg"] + [r[1] for r in b],
                        "image_sha256": [h("ot1")] + [r[2] for r in b + x + t]},
             "memory": [{"cid": f"m{n}", "members": [["openviic", f"y{n}.jpg", f"y{n}.jpg", h(f"y{n}")]]}
                        for n in range(9)]}
    lp = tmp / "lists.json"
    lp.write_text(json.dumps(lists), encoding="utf-8")
    return lp, lists


def selftest() -> None:
    cfg = frozen()
    g = grid(cfg)
    assert len(g) == 20 and sum(s["arm"] == "blind" for s in g.values()) == 4, "16 main + 4 image-blind runs"
    assert all(r.startswith("c2_") for r in g) and not any("-ret-" in r for r, s in g.items() if s["arm"] != "ret")
    assert {m: (c["tau"], c["tau_G"]) for m, c in cfg["models"].items()} == {
        "qwen25vl_7b": ("-inf", "0.00"), "internvl3_8b": ("0.10", "0.10")}
    assert tau_g("-inf") == tau_g("inf") == "0.00" and tau_g("0.20") == "0.20", "tau_G rule"
    assert verify_arms(cfg, "qwen25vl_7b") == ["ret"] and verify_arms(cfg, "internvl3_8b") == ["ret", "rand", "fix"]
    with tempfile.TemporaryDirectory() as tmp:
        bad = Path(tmp) / "cfg.json"
        bad.write_text(json.dumps({"models": {m: {**c, "tau": "inf", "tau_G": "inf"} for m, c in
                                              cfg["models"].items()}}), encoding="utf-8")
        assert C.refuses(lambda: frozen(bad)), "a tau_G that breaks the rule is refused"
        dummy = Path(tmp) / "dummy.json"
        dummy.write_text(json.dumps({"models": {m: {"k": 2, "order": "last", "tpl": "T1", "tau": "inf",
                                                    "tau_G": "0.00"} for m in C.MODELS}}), encoding="utf-8")
        assert verify_arms(frozen(dummy), "internvl3_8b") == ["ret"], "the ret verifier still runs at tau = +inf"
        lp, lists = fake_lists(Path(tmp))
        ids2, hashes2 = refused2(lists)
        assert len(manifest2("ov_dev_b", lists)) == 925 and len(manifest2("xm_dev500", lists)) == 500
        assert C.refuses(lambda: C.manifest("ov_dev_a", {**lists, "sets": {**lists["sets"], "ov_dev_a": lists[
            "sets"]["ov_dev_b"][:1]}})), "stage-1 modes still refuse OV-dev-B"
        assert C.refuses(lambda: manifest2("ov_dev_a", lists)), "stage-2 modes accept nothing from dev-A"
        for rows, ns in (([("t0", "t0.jpg", lists["sets"]["xm_test2500"][0][2])], "xm3600"),  # XM-test2500
                         ([("ot1.jpg", "ot1.jpg", "1" * 64)], "openviic"),                     # OV-test file
                         ([("1", "00000000001.jpg", "2" * 64)], "ktvic")):                     # KTVIC test id
            assert C.refuses(lambda: C.refuse_rows(rows, ns, ids2, hashes2)), "a test image stays refused"
        xm600 = next(iter(C.refused(lists)[0]["xm3600"]))
        assert C.refuses(lambda: C.refuse_rows([(xm600, "f.jpg", "3" * 64)], "xm3600", ids2, hashes2)), "XM600"
        short = {**lists, "sets": {**lists["sets"], "xm_dev500": lists["sets"]["xm_dev500"][:499]}}
        assert C.refuses(lambda: carve(short)), "the carve-out is exactly 925 + 500"
        leak = {**lists, "sets": {**lists["sets"], "xm_dev500": lists["sets"]["xm_dev500"][:499] + [xm600_row(
            lists, xm600)]}}
        assert C.refuses(lambda: refused2(leak)), "an XM600 id cannot be carved out"
        folder = Path(tmp) / "datasets/c_xm_dev500/images"
        folder.mkdir(parents=True)
        (folder / "other.jpg").write_bytes(b"not an XM-dev500 image")
        assert C.refuses(lambda: check_folder("xm_dev500", lists, Path(tmp))), "stray file in the XM folder"
        host_selftest(Path(tmp), lists)
    real = C.load_lists(ROOT / "manuscript/prereg/2026-10-22_c_stage1/lists.json")
    shas, files = carve(real)
    ids2, hashes2 = refused2(real)
    ids1, hashes1 = C.refused(real)
    assert len(real["sets"]["ov_dev_b"]) + len(real["sets"]["xm_dev500"]) == 1425, "real carve-out: 925 + 500 entries"
    assert len(hashes1 - hashes2) == len(shas) == 1424 and len(ids1["openviic"] - ids2["openviic"]) == 925
    assert len(manifest2("ov_dev_b", real)) == 925 and len(manifest2("xm_dev500", real)) == 500
    print(f"selftest ok: frozen grid ({len(g)} runs), tau_G rule, verify arms, carve-out 925 + 500 and refusals, "
          "stage-1 refusal kept, XM folder check, host check (passes; refuses test, XM-dev500, folders, labels, subset)")


def host_selftest(tmp: Path, lists: dict) -> None:
    import shutil

    data = fake_host(tmp, lists)
    rec = check_host("ov", lists, data, repo=tmp)
    assert rec["refused_present"] == 0 and len(rec["copied_sha256"]["ov_dev_b"]) == 925, "a clean host passes"
    for name, make in (("OV-test file", lambda: (data / "datasets/openviic/images/ot1.jpg").write_text("ot1")),
                       ("XM-test image", lambda: (data / "datasets/ktvic/images/t0.jpg").write_text("t0")),
                       ("XM-dev500 image before the XM block", lambda: (data / "datasets/ktvic/images/x0.jpg")
                        .write_text("x0")),
                       ("c_xm_dev500 folder", lambda: (data / "datasets/c_xm_dev500").mkdir()),
                       ("e_dev_a_pairs folder", lambda: (data / "datasets/e_dev_a_pairs").mkdir()),
                       ("xm3600_en folder", lambda: (data / "datasets/xm3600_en").mkdir()),
                       ("oiv7 labels", lambda: (tmp / "oiv7_labels.json").write_text("{}"))):
        make()
        assert C.refuses(lambda: check_host("ov", lists, data, repo=tmp)), name
        shutil.rmtree(tmp / "ncs")
        for p in (tmp / "oiv7_labels.json",):
            p.unlink(missing_ok=True)
        data = fake_host(tmp, lists)
    (data / OV_DEV_ANN).write_text(json.dumps({"a1.jpg": {"captions": ["w1"]}}), encoding="utf-8")
    assert C.refuses(lambda: check_host("ov", lists, data, repo=tmp)), "a wrong annotation subset"
    shutil.rmtree(tmp / "ncs")


def xm600_row(lists: dict, xm600_id: str) -> list:
    return [xm600_id, f"{xm600_id}.jpg", lists["sets"]["xm_dev500"][-1][2]]


def main() -> None:
    ap = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    ap.add_argument("--selftest", action="store_true")
    sub = ap.add_subparsers(dest="cmd")
    p = sub.add_parser("runs")
    p.add_argument("--set", choices=sorted(SETS), required=True)
    p.add_argument("--model", choices=C.MODELS)
    p.add_argument("--arm", nargs="+", choices=ARMS, default=list(MAIN))
    p = sub.add_parser("verify-arms")
    p.add_argument("--model", choices=C.MODELS, required=True)
    p = sub.add_parser("check-host")
    p.add_argument("--block", choices=("ov", "xm"), required=True)
    p.add_argument("--lists", type=Path, required=True)
    p = sub.add_parser("subsets")
    p.add_argument("--lists", type=Path, required=True)
    p.add_argument("--openviic-dev", type=Path, required=True, help="the released OpenViIC dev annotation")
    p.add_argument("--xm-full", type=Path, required=True, help="the released XM3600 full_data.json")
    p.add_argument("--out-dir", type=Path, required=True)
    a = ap.parse_args()
    if a.selftest:
        return selftest()
    handlers = {
        "runs": lambda: print(" ".join(spec(frozen(), a.set, m, arm)["run_id"]
                                       for m in ([a.model] if a.model else C.MODELS) for arm in a.arm)),
        "verify-arms": lambda: print(" ".join(verify_arms(frozen(), a.model))),
        "check-host": lambda: print(json.dumps(check_host(a.block, C.load_lists(a.lists)))),
        "subsets": lambda: cmd_subsets(a),
    }
    handlers.get(a.cmd, lambda: ap.error("mode?"))()


if __name__ == "__main__":
    main()
