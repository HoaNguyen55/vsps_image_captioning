#!/usr/bin/env python
"""VSPS-J E1 + E2 (manuscript/prereg/2026-10-31_vsps_j_e1e2/PREREG.md).

    python3 -I scripts/vsps_j_e1e2/e1e2.py plan                       laptop: pins, custody, counts
    python3 -I scripts/vsps_j_e1e2/e1e2.py fetchlist > <file>         host: E1a fetch list, checked against the plan
    PY -I e1e2.py e1b --images <KTVIC images> --model <Vintern snap> --out <OUT>              GPU, sub-job 1
    NCS_DATA=<stage> PY -I e1e2.py e1a --model <Vintern snap> --qwen <Qwen snap> --out <OUT>  GPU, sub-job 2
    PY_H1 -I e1e2.py detect --records <OUT>/e1a/records --images <UIT images> --out <OUT>    laptop CPU, H1 env
    PY -I e1e2.py score --out <OUT> --res <OUT>/e1e2_result.json                            laptop, once
    python3 -I e1e2.py selftest

E1b re-asks every unique Vintern question of the 3,700 KTVIC-train stage-1 records once as a yes/no logit probe
(M0's pinned probe, zero-shot single probe). E1a runs stage-1 v1 unchanged (scripts/generate_stage1.py main(),
K=5) on UIT-ViIC test (231 COCO images) and logs the same logit probe beside every Vintern K=5 probe. E2 replays
verify() on CPU with the logits and picks one per-type S_hi vector on KTVIC train (in-sample dev), then reads
T-COCO on E1a at that vector only. Guards are M0's (scripts/vsps_j_m0/m0.py, imported unchanged): one OUT
folder, a STOP marker per sub-job folder, the cap checked before each image, refusal to resume or score a stop.
"""
from __future__ import annotations

import argparse
import copy
import hashlib
import json
import math
import os
import random
import statistics
import sys
import tarfile
import time
from pathlib import Path

HERE = Path(__file__).resolve().parent
ROOT = HERE.parents[1]
sys.path[:0] = [str(ROOT), str(ROOT / "scripts"), str(ROOT / "scripts/vsps_j_m0"), str(HERE)]  # -I drops these
import m0  # noqa: E402  M0 guards and pinned probe, reused byte-identical (dba7685)

PDIR = ROOT / "manuscript/prereg/2026-10-31_vsps_j_e1e2"
PLAN = PDIR / "e1e2_plan.json"
VIN = m0.MODEL["repo"]
PATHS = {"records_tar": "data/stage1_records/stage1_records.tar.gz",
         "uit_test": "data/datasets/uitviic/test_data.json",
         "instances": "data/datasets/coco_probe/annotations/instances_train2014.json",
         "coco80_vi": "data/coco_probe/coco80_vi.json",
         "ktvic_train": "data/datasets/ktvic/train_data.json",
         "ktvic_test": "data/datasets/ktvic/test_data.json",
         "bn1_registry": "manuscript/prereg/2026-10-19_b_n1_vi_leaderboard.json",
         "karpathy": "data/datasets/karpathy/dataset_coco.json",
         "mhal_touched": "manuscript/prereg/2026-10-31_vsps_j_m0/dev_touched_ids.txt"}
PIN = {"records_tar": "b312de68180a2f9bf31602bae917ed170b2630174c30c11e9ea59c64aff840b0",
       "uit_test": "54abc0fb068ad1108d7d57b21328d4d68bcf8f41aa168f80ec7c275fb4ac8214",
       "instances": "777ef504abfeba349930485bb32ecd5b6529129a3e010f7852e1437cb049b732",
       "coco80_vi": "926e08571ef6e80a7f8aae8f2b73753d6c5c54c431a750ba2b67bfaae71b540b",
       "ktvic_train": "72ee9b57c350fb5f215e1f04701c515a51e5e415240e51a77c8ce00ce6316a0f",
       "ktvic_test": "cc22ec6a8883773cb23c87ad5b64925f5a53c21982117274b53621f454e7ebbf",
       "bn1_registry": "9ff02dc259258de1add426abd02131f2122e3476a81f9a076066ed6d74906134",
       "karpathy": m0.PIN["karpathy"],
       "mhal_touched": "91db7e2fbb3d479f79ed19fca4aa100399730910cd7511f832576350f26f9b63"}
QWEN = {"repo": "Qwen/Qwen2.5-VL-7B-Instruct", "key": "qwen25vl_7b", "revision": "cc594898137f460bfe9f0759e9844b3ce807cfb5"}
SEED = m0.SEED
CAP_H = {"e1b": 5.0, "e1a": 7.5}
N_PROJ = {"e1b": 200, "e1a": 20}
SMOKE_IMG, SMOKE_Q = 20, 5
N_E1B, N_E1A = 3700, 231
TYPES = ("entity", "counting", "attribute", "action", "relation", "spatial_relation")
GRID = tuple(round(0.50 + 0.05 * i, 2) for i in range(10))
PASSES = 2
S_HI_V1 = 0.70
P_FLOOR, RET_STOP, DR_MARGIN, N_ABSENT_MIN, KAPPA_MIN, B_BOOT = 39.2, 65.0, 5.0, 200, 0.70, 2000
MAX_E1A_MISSING = 11  # 5 % of 231: images still failing after the one allowed resume are listed, 0 T-COCO units


class Halt(BaseException):
    """Escapes generate_stage1.main()'s `except Exception` so a stopped image is never written."""

    def __init__(self, rc: int, reason: str):
        super().__init__(reason)
        self.rc, self.reason = rc, reason


# ------------------------------------------------------------------------------------------------ shared helpers
def pinned(name: str) -> Path:
    p = ROOT / PATHS[name]
    if m0.sha_file(p) != PIN[name]:
        raise SystemExit(f"FAULT {PATHS[name]}: sha256 differs from the pin")
    return p


def qkey(q: str) -> str:
    """rescap.vlm.replay.ReplayVLM._key: the join key between records and logit rows."""
    return " ".join(q.strip().rstrip("?.").split()).lower()


def vintern_questions(rec: dict, model: str = VIN) -> dict:
    """Unique Vintern questions of one record, first occurrence kept: {key: recorded probe}."""
    out: dict = {}
    for p in rec["propositions"]:
        for q in (p.get("evidence") or {}).get("probes") or []:
            if str(q.get("model", "")) == model and q.get("question_vi"):
                out.setdefault(qkey(q["question_vi"]), q)
    return out


def tar_records(path: Path | None = None) -> list:
    """The 3,700 pinned stage-1 records, read from the tarball in name order (no extraction)."""
    path = path or pinned("records_tar")
    if path != ROOT / PATHS["records_tar"] and m0.sha_file(path) != PIN["records_tar"]:
        raise SystemExit("FAULT records tarball pin")
    with tarfile.open(path, "r:gz") as tf:
        mem = sorted((m for m in tf.getmembers() if m.isfile() and m.name.endswith(".json")), key=lambda m: m.name)
        return [json.loads(tf.extractfile(m).read().decode("utf-8")) for m in mem]


def record_files(d: Path) -> list:
    """Stage-1 record files; generate_stage1 also writes _report_shard*.json there."""
    return sorted(p for p in d.glob("*.json") if not p.name.startswith("_"))


def shuffled(items, seed: int) -> list:
    out = sorted(items)
    random.Random(seed).shuffle(out)
    return out


def sha_lines(items) -> str:
    return m0.sha_text("".join(f"{x}\n" for x in items))


def prep_out(out: Path) -> Path:
    if out.resolve().is_relative_to(ROOT):
        raise SystemExit("REFUSED --out inside the repo")
    out.mkdir(parents=True, exist_ok=True)
    m0.refuse_if_stopped(out)
    launch = out / "launch.json"
    if not launch.exists():
        launch.write_text(json.dumps({"t0": time.time()}))
    return out


def elapsed_h(out: Path) -> float:
    return (time.time() - json.loads((out / "launch.json").read_text())["t0"]) / 3600


def kappa(a: list, b: list) -> float:
    """gate_t05.kappa (Cohen), restated to avoid importing that script's data-path globals."""
    n = len(a)
    po = sum(x == y for x, y in zip(a, b)) / n
    pa, pb = sum(a) / n, sum(b) / n
    pe = pa * pb + (1 - pa) * (1 - pb)
    return 1.0 if pe == 1 else (po - pe) / (1 - pe)


def is_yes(text: str) -> bool:
    return str(text or "").strip().lower().startswith(("có", "đúng", "phải", "yes"))


# ------------------------------------------------------------------------------------------------ plan (laptop)
def cmd_plan(_a) -> int:
    recs = tar_records()
    kt = {s: {i["filename"] for i in json.loads(pinned(f"ktvic_{s}").read_text())["images"]} for s in ("train", "test")}
    names = [r["file_name"] for r in recs]
    bad = [n for n in names if n not in kt["train"] or n in kt["test"]]
    if len(names) != N_E1B or bad:
        raise SystemExit(f"FAULT E1b custody: {len(names)} records, {len(bad)} not train-only KTVIC")
    nq = [len(vintern_questions(r)) for r in recs]
    uit = json.loads(pinned("uit_test").read_text(encoding="utf-8"))["images"]
    ids = {int(i["id"]) for i in uit}
    ks = {int(i["cocoid"]): i["split"] for i in json.loads(pinned("karpathy").read_text())["images"]}
    inst = json.loads(pinned("instances").read_text())
    touched = {int(x) for x in pinned("mhal_touched").read_text().split()}
    overlap = {"a_t3_3232": len(ids & m0.at3_ids()), "kv_4224": len(ids & m0.kv4224()),
               "ut_2532": len(ids & m0.ut2532()), "karpathy_test": sum(ks.get(i) == "test" for i in ids),
               "mhaldetect_dev_touched": len(ids & touched),
               "in_instances_train2014": len(ids & {int(i["id"]) for i in inst["images"]})}
    refused = m0.refused_sets()[0]
    if len(refused["uitviic_test"] & ids) != N_E1A or overlap["in_instances_train2014"] != N_E1A or any(
            overlap[k] for k in ("a_t3_3232", "kv_4224", "ut_2532", "karpathy_test", "mhaldetect_dev_touched")):
        raise SystemExit(f"FAULT E1a custody: {overlap}")
    plan = {
        "pins": {k: PIN[k] for k in PATHS}, "qwen": QWEN, "vintern": m0.MODEL["revision"],
        "e1b": {"records": len(recs), "propositions": sum(len(r["propositions"]) for r in recs),
                "vintern_unique_questions": sum(nq), "median_q_per_image": statistics.median(nq),
                "names_sha256": sha_lines(names), "order_sha256": sha_lines(shuffled(names, SEED + 6)),
                "ktvic_train_images": len(kt["train"]), "unrecorded_train_images": len(kt["train"] - kt["test"] - set(names))},
        "e1a": {"images": len(uit), "ids_sha256": sha_lines(sorted(ids)),
                "order_sha256": sha_lines([i["file_name"] for i in uit]), "overlap": overlap,
                "fetch_sha256": m0.sha_text(fetch_text(uit)), "exclusion_uitviic_test_shas": len(json.loads(m0.EXCLUSION.read_text())["image_sha256"]["uitviic_test"])},
    }
    PLAN.write_text(json.dumps(plan, indent=1) + "\n", encoding="utf-8")
    print(json.dumps(plan, indent=1))
    return 0


def fetch_text(uit: list) -> str:
    """E1a fetch list, "file_name coco_url" per image in test_data.json order. Built on the host from the pinned file,
    never committed (the n-gram scan counts UIT-ViIC JSON fields)."""
    return "".join(f"{i['file_name']} {i['coco_url']}\n" for i in uit)


def cmd_fetchlist(_a) -> int:
    text = fetch_text(json.loads(pinned("uit_test").read_text(encoding="utf-8"))["images"])
    if m0.sha_text(text) != json.loads(PLAN.read_text(encoding="utf-8"))["e1a"]["fetch_sha256"]:
        raise SystemExit("FAULT fetch list differs from the plan")
    sys.stdout.write(text)
    return 0


# ------------------------------------------------------------------------------------------------ E1b (GPU)
def load_vintern(model: Path, device: str):
    from rescap.vlm.registry import get_vlm

    m0.check_model(model)
    ad = get_vlm(m0.MODEL["name"], model_id=VIN, device=device,
                 dtype="bfloat16" if device == "cuda" else "float32").load()
    if ad.max_tiles != m0.MODEL["max_tiles"]:
        raise SystemExit("FAULT max_tiles is not the registry value 4")
    return ad


def run_smoke(ad, work: list, img) -> dict:
    """M0 section 7.1 rules, arm A only: tokens, finite, mass, text, yes_no_logit equivalence on the first 5."""
    tok = m0.token_check(ad)
    rows, equiv = [], []
    for name, qs in work[:SMOKE_IMG]:
        im = img(name)
        pv = ad._pixel_values(im)
        for _k, q in qs[:SMOKE_Q]:
            t = time.perf_counter()
            text, p, m = m0.probe(ad, pv, q)
            rows.append({"arm": "A", "p_yes": p, "mass": m, "text": text, "sec": time.perf_counter() - t})
            if len(equiv) < 5:
                equiv.append(abs(ad.yes_no_logit(im, q)[1] - p))
    v = m0.smoke_verdict(rows, equiv)
    v.pop("B", None)
    v.update(token=tok, fault=not (v["A"]["ok"] and tok["ok"]), sec_median=statistics.median(r["sec"] for r in rows))
    return v


def run_pass(probe, out: Path, work: list, img, cap_h: float, n_proj: int, smoke_s: float) -> int:
    """E1b loop. probe(pv_source, q) -> (text, p, mass); work = [(image name, [(key, question), ...]), ...]."""
    pf, pre_f, proj_f = out / "probes.jsonl", out / "projection_pre_val.json", out / "projection.json"
    done = {(r["image"], r["q"]) for r in map(json.loads, pf.read_text(encoding="utf-8").splitlines())} if pf.exists() else set()
    total = sum(len(qs) for _n, qs in work)
    if not pre_f.exists() and not done:
        pj = elapsed_h(out) + total * smoke_s / 3600
        pre_f.write_text(json.dumps({"elapsed_h": elapsed_h(out), "projected_h": pj, "cap_h": cap_h, "stop": pj > cap_h}))
        if pj > cap_h:
            return m0.halt(out, 3, f"PROJECTION_STOP before the pass: projected {pj:.2f} GPU-h > cap {cap_h}", 0)
    with open(pf, "a", encoding="utf-8") as fh:
        for n, (name, qs) in enumerate(work, 1):
            if elapsed_h(out) > cap_h:
                return m0.halt(out, 4, f"CAP_STOP before image {n}: {elapsed_h(out):.2f} GPU-h", n)
            todo = [(k, q) for k, q in qs if (name, k) not in done]
            if todo:
                src = img(name)
                for k, q in todo:
                    t = time.perf_counter()
                    text, p, m = probe(src, q)
                    row = {"image": name, "q": k, "n_img": n, "p_yes": p, "mass": m, "text": text,
                           "sec": time.perf_counter() - t}
                    m0.append(fh, row)
                    if not math.isfinite(p):
                        fh.flush()
                        return m0.halt(out, 2, f"FAULT non-finite P(yes) at {name}", n)
                    done.add((name, k))
                fh.flush()
                os.fsync(fh.fileno())
            if n == n_proj and not proj_f.exists():
                rows = [json.loads(x) for x in pf.read_text(encoding="utf-8").splitlines()]
                med = statistics.median(r["sec"] for r in rows if 2 <= r["n_img"] <= n_proj)
                pj = elapsed_h(out) + (total - len(done)) * med / 3600
                proj_f.write_text(json.dumps({"elapsed_h": elapsed_h(out), "median_s": med, "remaining": total - len(done),
                                              "projected_h": pj, "cap_h": cap_h, "stop": pj > cap_h}))
                if pj > cap_h:
                    return m0.halt(out, 3, f"PROJECTION_STOP projected {pj:.2f} GPU-h > cap {cap_h}", n)
    print(json.dumps({"status": "DONE", "elapsed_h": elapsed_h(out), "probes": len(done)}))
    return 0


def check_images(names, folder: Path, refused_sha: set, must_be_in: set | None = None) -> None:
    """Every image present; none whose bytes exclusion.json lists (E1b), or every one listed there (E1a pin)."""
    shas = {n: m0.sha_file(folder / n) for n in names}
    hits = [n for n, h in shas.items() if h in refused_sha]
    if must_be_in is None and hits:
        raise SystemExit(f"FAULT {len(hits)} images match exclusion.json image_sha256: {hits[:3]}")
    if must_be_in is not None and any(h not in must_be_in for h in shas.values()):
        raise SystemExit("FAULT an E1a image is not byte-equal to exclusion.json uitviic_test")


def cmd_e1b(a) -> int:
    from PIL import Image

    out = prep_out(a.out / "e1b")
    plan = json.loads(PLAN.read_text(encoding="utf-8"))
    recs = {r["file_name"]: r for r in tar_records(a.records_tar)}
    order = shuffled(recs, SEED + 6)
    if sha_lines(order) != plan["e1b"]["order_sha256"]:
        raise SystemExit("FAULT E1b order differs from the plan")
    ex = json.loads(m0.EXCLUSION.read_text(encoding="utf-8"))
    check_images(order, a.images, set(ex["image_sha256"]["ktvic_test"]))
    work = [(n, [(k, q["question_vi"]) for k, q in vintern_questions(recs[n]).items()]) for n in order]
    ad = load_vintern(a.model, a.device)
    img = lambda n: Image.open(a.images / n).convert("RGB")  # noqa: E731
    smoke_f = out / "smoke.json"
    if not smoke_f.exists():
        smoke_f.write_text(json.dumps(run_smoke(ad, work, img), indent=1, ensure_ascii=False))
    v = json.loads(smoke_f.read_text())
    if v["fault"]:
        return m0.halt(out, 2, "FAULT smoke (tokens / mass / text / equivalence); see smoke.json")
    cache: dict = {}

    def pv_of(name):
        if cache.get("n") != name:
            cache.update(n=name, pv=ad._pixel_values(img(name)))
        return cache["pv"]

    return run_pass(lambda name, q: m0.probe(ad, pv_of(name), q), out, work, lambda n: n,
                    CAP_H["e1b"], N_PROJ["e1b"], v["sec_median"])


# ------------------------------------------------------------------------------------------------ E1a (GPU)
def check_qwen(snap: Path) -> None:
    """Qwen2.5-VL-7B at the B-N1 registry pin: LFS files by sha256, the rest by git blob sha1."""
    reg = json.loads(pinned("bn1_registry").read_text(encoding="utf-8"))
    entry = next(v for v in _walk(reg) if isinstance(v, dict) and v.get("hub_id") == QWEN["repo"])
    if entry["revision"] != QWEN["revision"] or snap.name != QWEN["revision"]:
        raise SystemExit("FAULT Qwen snapshot is not the B-N1 pinned revision")
    ref = snap.parent.parent / "refs" / "main"
    if os.environ.get("HF_HUB_OFFLINE") != "1" or not ref.is_file() or ref.read_text().strip() != QWEN["revision"]:
        raise SystemExit("FAULT need HF_HUB_OFFLINE=1 and Qwen refs/main = the pinned revision")
    for f, h in entry["files"].items():
        if h["hash"] is None:
            continue
        data = (snap / f).read_bytes()
        got = (hashlib.sha256(data).hexdigest() if h["kind"] == "sha256"
               else hashlib.sha1(b"blob %d\0" % len(data) + data).hexdigest())
        if got != h["hash"]:
            raise SystemExit(f"FAULT Qwen {f}: hash differs from the B-N1 pin")


def _walk(x):
    yield x
    for v in (x.values() if isinstance(x, dict) else x if isinstance(x, list) else ()):
        yield from _walk(v)


def install_sidelog(cls, state: dict, fh, probe, order: set, cap_h: float, out: Path, n_proj: int):
    """Wrap cls.probe_yes_no (v1 K=5 answer returned unchanged) to log one logit probe per call, and PIL.Image.open
    to track the current image, check the cap before each image and apply the 20-image projection.
    Returns an uninstall function."""
    import PIL.Image

    orig_pyn, orig_open = cls.probe_yes_no, PIL.Image.open

    def pyn(self, image, question, *, k=1, temperature=0.0):
        ans = orig_pyn(self, image, question, k=k, temperature=temperature)
        t = time.perf_counter()
        text, p, m = probe(self, image, question)
        m0.append(fh, {"image": state["file"], "q": qkey(question), "n_img": state["n"], "p_yes": p, "mass": m,
                       "text": text, "sec": time.perf_counter() - t})
        fh.flush()
        if not math.isfinite(p):
            raise Halt(2, f"FAULT non-finite P(yes) at {state['file']}")
        return ans

    def hooked_open(fp, *args, **kw):
        name = Path(str(fp)).name
        if name in order and name != state["file"]:
            now = time.time()
            if state["t_last"] is not None:
                state["sec"].append(now - state["t_last"])
                if state["n"] == 1 and not (state["rec_dir"] / f"{Path(state['file']).stem}.json").exists():
                    raise Halt(2, f"FAULT first image {state['file']} produced no record (load or pipeline error)")
            if elapsed_h(out) > cap_h:
                raise Halt(4, f"CAP_STOP before image {state['n'] + 1}: {elapsed_h(out):.2f} GPU-h")
            proj_f = out / "projection.json"
            if len(state["sec"]) == n_proj and not proj_f.exists():
                med = statistics.median(state["sec"][1:])
                pj = elapsed_h(out) + (len(order) - n_proj - state["skipped"]) * med / 3600
                proj_f.write_text(json.dumps({"elapsed_h": elapsed_h(out), "median_s_per_image": med,
                                              "projected_h": pj, "cap_h": cap_h, "stop": pj > cap_h}))
                if pj > cap_h:
                    raise Halt(3, f"PROJECTION_STOP projected {pj:.2f} GPU-h > cap {cap_h}")
            state.update(file=name, n=state["n"] + 1, t_last=now)
        return orig_open(fp, *args, **kw)

    cls.probe_yes_no, PIL.Image.open = pyn, hooked_open

    def uninstall():
        cls.probe_yes_no, PIL.Image.open = orig_pyn, orig_open
    return uninstall


def cached_probe():
    """M0's probe on the image's pixel values, tiled once per (image object) like the K=5 path."""
    cache: dict = {}

    def probe(ad, image, question):
        if cache.get("id") is not image:
            cache.update(id=image, pv=ad._pixel_values(image))
        return m0.probe(ad, cache["pv"], question)
    return probe


def run_stage1(out: Path, src_name: str, cls, probe, order: list, cap_h: float, n_proj: int, gen: str, ver: str) -> int:
    """generate_stage1.main() unchanged, under the side-log; a Halt writes the STOP marker, nothing else."""
    import generate_stage1 as g

    rec_dir = out / "records"
    done = {p.stem for p in rec_dir.glob("*.json")} if rec_dir.exists() else set()
    state = {"file": None, "n": 0, "t_last": None, "sec": [], "rec_dir": rec_dir,
             "skipped": sum(Path(n).stem in done for n in order)}
    sys.argv = ["generate_stage1.py", "--source", src_name, "--out", str(rec_dir), "--generator", gen, "--verifier", ver]
    with open(out / "probes.jsonl", "a", encoding="utf-8") as fh:
        uninstall = install_sidelog(cls, state, fh, probe, set(order), cap_h, out, n_proj)
        try:
            rc = g.main()
        except Halt as h:
            return m0.halt(out, h.rc, h.reason, state["n"])
        finally:
            uninstall()
    n_rec = len(record_files(rec_dir))
    status = "DONE" if rc == 0 and n_rec == len(order) else "FAILURES"
    print(json.dumps({"status": status, "records": n_rec, "elapsed_h": elapsed_h(out)}))
    return 0 if status == "DONE" else 5  # 5: some images failed; no marker, the same command may resume once


def cmd_e1a(a) -> int:
    from rescap.vlm.vintern import VinternAdapter

    out = prep_out(a.out / "e1a")
    smoke = a.out / "e1b" / "smoke.json"
    if not smoke.is_file() or json.loads(smoke.read_text())["fault"]:
        raise SystemExit("REFUSED E1a needs the E1b smoke with fault false (same Vintern, same block)")
    if os.environ.get("QWEN_MAX_PIXELS"):
        raise SystemExit("FAULT QWEN_MAX_PIXELS must be unset (adapter default 1280*28*28, as stage 1)")
    plan = json.loads(PLAN.read_text(encoding="utf-8"))
    stage = Path(os.environ.get("NCS_DATA", "")) / "datasets" / "ktvic"
    src = stage / "uitviic_test.json"
    if m0.sha_file(src) != PIN["uit_test"]:
        raise SystemExit("FAULT staged uitviic_test.json is not the pinned UIT-ViIC test file")
    order = [i["file_name"] for i in json.loads(src.read_text(encoding="utf-8"))["images"]]
    if sha_lines(order) != plan["e1a"]["order_sha256"]:
        raise SystemExit("FAULT E1a order differs from the plan")
    ex = json.loads(m0.EXCLUSION.read_text(encoding="utf-8"))
    check_images(order, stage / "images", set(), must_be_in=set(ex["image_sha256"]["uitviic_test"]))
    m0.check_model(a.model)
    check_qwen(a.qwen)
    return run_stage1(out, src.name, VinternAdapter, cached_probe(), order, CAP_H["e1a"], N_PROJ["e1a"],
                      "qwen2.5-vl-7b", "vintern-1b")


# ------------------------------------------------------------------------------------------------ detectors (laptop CPU)
def cmd_detect(a) -> int:
    """H1 detectors (scripts/vsps_h1 config/map pins, Detectors class unchanged) on the 231 E1a images, CPU."""
    from PIL import Image

    sys.path.insert(0, str(ROOT / "scripts/vsps_h1"))
    import detect_boxes as db

    plan = json.loads(PLAN.read_text(encoding="utf-8"))
    out = prep_out(a.out / "e1a_det")
    recs = record_files(a.records)
    if len(recs) != plan["e1a"]["images"]:
        raise SystemExit("REFUSED detect needs all 231 E1a records")
    vi_en = json.loads((db.HERE / "vi_en_map.json").read_text(encoding="utf-8"))["map"]
    csha, msha = db.file_sha(db.HERE / "config.json"), db.file_sha(db.HERE / "vi_en_map.json")
    done = db.read_lines(out / "boxes.jsonl", csha, msha, "cpu")
    det = db.Detectors("cpu")
    pins = {k: {"repo": v["repo"], "revision": v["revision"]} for k, v in db.CONFIG["detectors"].items()}
    with open(out / "boxes.jsonl", "a", encoding="utf-8") as fh:
        for f in recs:
            rec = json.loads(f.read_text(encoding="utf-8"))
            if rec["image_id"] in done:
                continue
            ents = {e["id"]: vi_en.get(str(e.get("category_vi") or "")) for e in rec["entities"]}
            prompts = sorted({p for p in ents.values() if p})
            image = Image.open(a.images / rec["file_name"]).convert("RGB")
            g = det.gdino(image, prompts) if prompts else {}
            o = det.owlv2(image, prompts) if prompts else {}
            m0.append(fh, {"image_id": rec["image_id"], "file_name": rec["file_name"], "device": "cpu", "pins": pins,
                           "config_sha256": csha, "map_sha256": msha, "entities": ents,
                           "prompts": {p: {"gdino": g[p], "owlv2": o[p]} for p in prompts}})
            fh.flush()
    return 0


# ------------------------------------------------------------------------------------------------ E2 replay (laptop CPU)
def logit_vlm_class():
    from rescap.vlm.base import Answer, ConfidenceMethod, Polarity, YesNo
    from rescap.vlm.replay import ReplayVLM

    class LogitVLM(ReplayVLM):
        """Vintern answers from the logit table: AFFIRMS iff P(yes) >= 0.5, confidence max(p, 1-p) (raw, not
        vintern.calibrated()), one sample. A question missing from the table answers INCONCLUSIVE and counts as a miss."""

        def __init__(self, propositions, table: dict, model_name: str = VIN):
            super().__init__(propositions, model_name=model_name)
            self.table = table

        def probe_yes_no(self, image, question, *, k=1, temperature=0.0):
            p = self.table.get(self._key(question))
            if p is None:
                self.misses += 1
                return YesNo(polarity=Polarity.INCONCLUSIVE, confidence=0.0,
                             answer=Answer(text="", confidence=0.0, method=ConfidenceMethod.NONE,
                                           model=self.name, prompt=question))
            self.hits += 1
            yes = p >= 0.5
            conf, text = max(p, 1 - p), ("Có." if yes else "Không.")
            return YesNo(polarity=Polarity.AFFIRMS if yes else Polarity.REFUTES, confidence=conf,
                         answer=Answer(text=text, confidence=conf, method=ConfidenceMethod.TOKEN_PROB, samples=[text],
                                       model=self.model_name, prompt=question))
    return LogitVLM


def replay(rec: dict, table: dict | None, s_hi: dict, votes: dict | None = None, model: str = VIN):
    """verify() replayed on one record: table None = recorded K=5 answers (v1 replay), else logit answers.
    The second model (the Qwen colour cross-check) always replays its recorded answers. Returns (statuses, misses)."""
    from rescap.pipeline.verify import Thresholds, VerificationConfig, verify
    from rescap.vlm.replay import ReplayVLM

    r = copy.deepcopy(rec)
    for p in r["propositions"]:
        p["verification"] = {"status": None}
    models = {str(q.get("model", "")) for p in rec["propositions"] for q in (p.get("evidence") or {}).get("probes") or []}
    if not models:
        return [None] * len(r["propositions"]), 0
    second = sorted(models - {model})
    ver = ReplayVLM(rec["propositions"], model_name=model) if table is None else logit_vlm_class()(rec["propositions"], table, model)
    cfg = VerificationConfig(per_type_thresholds={t: Thresholds(S_hi=v) for t, v in s_hi.items() if v != S_HI_V1})
    verify(ver, None, r["entities"], r["propositions"], config=cfg,
           colour_verifier=ReplayVLM(rec["propositions"], model_name=second[0]) if second else None, entity_votes=votes)
    return [p["verification"]["status"] for p in r["propositions"]], ver.misses


def kt_prepare(recs: list) -> list:
    """Per record: gold lexicon objects (refs) and the lexicon objects each proposition names."""
    from rescap.chair import objects_in

    return [(set().union(*[set(objects_in(c)) for c in r["reference_captions"]]),
             [set(objects_in(p["text_vi"])) for p in r["propositions"]]) for r in recs]


def kt_metrics(prep: list, statuses: list) -> dict:
    """T-KT (in-sample dev, CC-207 W6): supported-stage P and R (recall_funnel), retention and mirror (ret.py)."""
    tp = named = kp = ap = dn = an = 0
    recalls = []
    for (gold, objs), st in zip(prep, statuses):
        if not gold:
            continue
        kept = set().union(*[o for o, s in zip(objs, st) if s == "SUPPORTED"])
        pairs = set().union(*objs)
        tp, named = tp + len(kept & gold), named + len(kept)
        recalls.append(len(kept & gold) / len(gold))
        kp, ap = kp + len(kept & gold), ap + len(pairs & gold)
        dn, an = dn + len((pairs - gold) - kept), an + len(pairs - gold)
    return {"P": 100 * tp / max(named, 1), "R": 100 * sum(recalls) / max(len(recalls), 1),
            "retention": 100 * kp / max(ap, 1), "mirror": 100 * dn / max(an, 1)}


def select_s_hi(evaluate) -> tuple[dict, list]:
    """Pre-fixed coordinate rule, PASSES passes over TYPES in order: each type's S_hi on GRID with the other types at
    their current values (start: v1 0.70); keep max retention with P >= P_FLOOR; ties -> the larger S_hi; no feasible
    value -> the type keeps its current value."""
    s_hi = dict.fromkeys(TYPES, S_HI_V1)
    trace = []
    for k in range(PASSES):
        for t in TYPES:
            best = None
            for v in GRID:
                m = evaluate({**s_hi, t: v})
                trace.append({"pass": k + 1, "type": t, "S_hi": v, **m})
                if m["P"] >= P_FLOOR and (best is None or m["retention"] >= best[1] - 1e-9):
                    best = (v, m["retention"])
            s_hi[t] = best[0] if best else s_hi[t]
    return s_hi, trace


# ------------------------------------------------------------------------------------------------ T-COCO (E1a)
def tcoco_units(recs: list, statuses: list, inst: dict) -> list:
    """Entity propositions naming exactly one COCO-80 class (FAIR matcher v2): (image, absent, status)."""
    from score_coco_probe import load_vi_terms, vi_objects

    terms = load_vi_terms()
    units = []
    for r, st in zip(recs, statuses):
        gold = inst.get(int(r["image_id"]), set())
        for p, s in zip(r["propositions"], st):
            if p["type"] == "entity":
                cls = vi_objects(p["text_vi"], terms)
                if len(cls) == 1:
                    units.append((int(r["image_id"]), next(iter(cls)) not in gold, s))
    return units


def tcoco_rates(units: list) -> dict:
    ab = [s for _i, a, s in units if a]
    pr = [s for _i, a, s in units if not a]
    return {"n_absent": len(ab), "n_present": len(pr),
            "DR": 100 * sum(s != "SUPPORTED" for s in ab) / max(len(ab), 1),
            "DR_strict": 100 * sum(s == "REJECTED" for s in ab) / max(len(ab), 1),
            "RT": 100 * sum(s == "SUPPORTED" for s in pr) / max(len(pr), 1)}


def cluster_ci(conds: dict, base: str) -> dict:
    """Image-clustered percentile bootstrap (B_BOOT, SEED): 95% CI of each condition's DR / RT and of its DR / RT
    difference from `base` (paired: the same resampled images)."""
    imgs = sorted({u[0] for u in next(iter(conds.values()))})
    by = {c: {} for c in conds}
    for c, units in conds.items():
        for u in units:
            by[c].setdefault(u[0], []).append(u)
    rng = random.Random(SEED)
    draws = {(c, k): [] for c in conds for k in ("DR", "RT", "dDR", "dRT")}
    for _b in range(B_BOOT):
        pick = [imgs[rng.randrange(len(imgs))] for _ in imgs]
        rates = {c: tcoco_rates([u for i in pick for u in by[c].get(i, [])]) for c in conds}
        for c in conds:
            draws[(c, "DR")].append(rates[c]["DR"])
            draws[(c, "RT")].append(rates[c]["RT"])
            draws[(c, "dDR")].append(rates[c]["DR"] - rates[base]["DR"])
            draws[(c, "dRT")].append(rates[c]["RT"] - rates[base]["RT"])
    q = lambda xs: [sorted(xs)[int(0.025 * B_BOOT)], sorted(xs)[int(0.975 * B_BOOT) - 1]]  # noqa: E731
    return {f"{c}.{k}": q(v) for (c, k), v in draws.items()}


# ------------------------------------------------------------------------------------------------ score (laptop, once)
def logit_tables(rows: list) -> dict:
    t: dict = {}
    for r in rows:
        t.setdefault(r["image"], {}).setdefault(r["q"], r["p_yes"])
    return t


def fidelity(recs: list, tables: dict, model: str = VIN) -> dict:
    """Coverage (every unique recorded Vintern question has a logit row; else REFUSED) and the gate T0.5 G2 check:
    kappa(P(yes) >= 0.5, recorded K=5 majority) >= KAPPA_MIN; agreement by K=5 vote margin is descriptive."""
    a, b, margin = [], [], {}
    for r in recs:
        t = tables.get(r["file_name"], {})
        for k, q in vintern_questions(r, model).items():
            if k not in t:
                raise SystemExit(f"INCOMPLETE: no logit row for a recorded question of {r['file_name']}")
            s = q.get("samples") or [q.get("answer", "")]
            ys = sum(map(is_yes, s))
            a.append(t[k] >= 0.5)
            b.append(ys * 2 > len(s))
            key = f"{max(ys, len(s) - ys)}/{len(s)}"
            margin.setdefault(key, []).append(a[-1] == b[-1])
    kap = kappa(a, b)
    return {"n": len(a), "kappa": kap, "agreement": sum(x == y for x, y in zip(a, b)) / len(a),
            "by_margin": {k: [len(v), sum(v) / len(v)] for k, v in sorted(margin.items())}, "pass": kap >= KAPPA_MIN}


def score_e1b(out: Path) -> dict:
    tables = logit_tables(m0.check_scorable(out / "e1b"))
    recs = tar_records()
    fid = fidelity(recs, tables)
    res: dict = {"fidelity": fid}
    prep = kt_prepare(recs)
    rec_st = [[p["verification"]["status"] for p in r["propositions"]] for r in recs]
    res["recorded_v1"] = kt_metrics(prep, rec_st)
    res["replay_v1_k5"] = kt_metrics(prep, [replay(r, None, {})[0] for r in recs])

    def evaluate(s_hi):
        st, miss = zip(*(replay(r, tables[r["file_name"]], s_hi) for r in recs))
        if sum(miss):
            raise SystemExit(f"FAULT {sum(miss)} logit-table misses in replay")
        return kt_metrics(prep, list(st))

    res["logit_base"] = evaluate(dict.fromkeys(TYPES, S_HI_V1))
    if not fid["pass"]:
        res["e2_kt"] = "STOP (fidelity kappa < 0.70)"
        return res
    s_hi, trace = select_s_hi(evaluate)
    res.update(s_hi=s_hi, sweep=trace, chosen=evaluate(s_hi))
    res["e2_kt"] = "CONTINUE" if res["chosen"]["retention"] >= RET_STOP and res["chosen"]["P"] >= P_FLOOR else "STOP"
    return res


def score_e1a(out: Path, s_hi: dict | None) -> dict:
    recs = [json.loads(f.read_text(encoding="utf-8")) for f in record_files(out / "e1a" / "records")]
    if len(recs) < N_E1A - MAX_E1A_MISSING:
        raise SystemExit(f"INCOMPLETE: {len(recs)} E1a records (at most {MAX_E1A_MISSING} may fail after one resume)")
    tables = logit_tables(m0.check_scorable(out / "e1a"))
    have = {r["file_name"] for r in recs}
    order = [i["file_name"] for i in json.loads(pinned("uit_test").read_text(encoding="utf-8"))["images"]]
    res: dict = {"records": len(recs), "failed_images": [n for n in order if n not in have],
                 "fidelity": fidelity(recs, tables)}
    inst_j = json.loads(pinned("instances").read_text())
    names = {c["id"]: c["name"] for c in inst_j["categories"]}
    inst: dict = {}
    for an in inst_j["annotations"]:
        inst.setdefault(an["image_id"], set()).add(names[an["category_id"]])
    conds = {"recorded_v1": [[p["verification"]["status"] for p in r["propositions"]] for r in recs],
             "replay_v1_k5": [replay(r, None, {})[0] for r in recs],
             "logit_base": [replay(r, tables[r["file_name"]], {})[0] for r in recs]}
    if s_hi is not None:
        conds["e2_chosen"] = [replay(r, tables[r["file_name"]], s_hi)[0] for r in recs]
        boxes = out / "e1a_det" / "boxes.jsonl"
        if boxes.is_file():
            sys.path.insert(0, str(ROOT / "scripts/vsps_h1"))
            from vote import votes_and_boxes

            det = {d["file_name"]: d for d in map(json.loads, boxes.read_text(encoding="utf-8").splitlines())}
            ents = [v for d in det.values() for v in d["entities"].values()]
            res["det_mapped_entity_share"] = sum(v is not None for v in ents) / max(len(ents), 1)
            conds["e2_chosen_det"] = [replay(r, tables[r["file_name"]], s_hi, votes_and_boxes(det[r["file_name"]])[0])[0]
                                      for r in recs]
    units = {c: tcoco_units(recs, st, inst) for c, st in conds.items()}
    res["tcoco"] = {c: tcoco_rates(u) for c, u in units.items()}
    res["tcoco_ci95"] = cluster_ci(units, "replay_v1_k5")
    if "e2_chosen" in res["tcoco"]:
        drop = res["tcoco"]["replay_v1_k5"]["DR"] - res["tcoco"]["e2_chosen"]["DR"]
        decisive = res["tcoco"]["e2_chosen"]["n_absent"] >= N_ABSENT_MIN
        res["e2_tcoco"] = ("STOP" if drop > DR_MARGIN else "CONTINUE") + ("" if decisive else " (descriptive, n_absent < 200)")
    return res


def isolated(fn, *args) -> dict:
    """A stopped or incomplete sub-job is recorded and never blocks the other one (PREREG section 6)."""
    try:
        return fn(*args)
    except SystemExit as e:
        return {"not_scored": str(e)}


def cmd_score(a) -> int:
    res = {"tier": "TIER 1 / DEV-EXPLORE (VSPS-J E1+E2)", "e1b_e2_kt": isolated(score_e1b, a.out)}
    kt = res["e1b_e2_kt"]
    res["e1a_tcoco"] = isolated(score_e1a, a.out, kt.get("s_hi") if kt.get("e2_kt") == "CONTINUE" else None)
    res["note"] = ("T-KT is in-sample dev on caption-derived KTVIC train gold (CC-207 W6): never registered, never a "
                   "headline. T-COCO is COCO-80 entity existence on 231 sports images (UIT-ViIC test, spent, dev role).")
    a.res.write_text(json.dumps(res, indent=1, ensure_ascii=False) + "\n", encoding="utf-8")
    print(json.dumps({k: res[k] for k in ("tier",)} | {"e2_kt": kt.get("e2_kt"), "s_hi": kt.get("s_hi"),
                                                       "e2_tcoco": res["e1a_tcoco"].get("e2_tcoco")}, indent=1))
    return 0


def main() -> int:
    ap = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    sp = ap.add_subparsers(dest="cmd", required=True)
    sp.add_parser("selftest")
    sp.add_parser("plan")
    sp.add_parser("fetchlist")
    b = sp.add_parser("e1b")
    b.add_argument("--records-tar", type=Path, default=ROOT / PATHS["records_tar"])
    b.add_argument("--images", type=Path, required=True, help="KTVIC images (the 3,700 train records' files)")
    b.add_argument("--model", type=Path, required=True, help="Vintern snapshot dir named by the pinned revision")
    b.add_argument("--out", type=Path, required=True, help="the ONE OUT folder of this block")
    b.add_argument("--device", default="cuda")
    e = sp.add_parser("e1a")
    e.add_argument("--model", type=Path, required=True)
    e.add_argument("--qwen", type=Path, required=True, help="Qwen snapshot dir named by the pinned revision")
    e.add_argument("--out", type=Path, required=True)
    d = sp.add_parser("detect")
    d.add_argument("--records", type=Path, required=True)
    d.add_argument("--images", type=Path, required=True)
    d.add_argument("--out", type=Path, required=True)
    s = sp.add_parser("score")
    s.add_argument("--out", type=Path, required=True)
    s.add_argument("--res", type=Path, required=True)
    a = ap.parse_args()
    if a.cmd == "selftest":
        import test_e1e2

        test_e1e2.main()
        return 0
    return {"plan": cmd_plan, "fetchlist": cmd_fetchlist, "e1b": cmd_e1b, "e1a": cmd_e1a, "detect": cmd_detect, "score": cmd_score}[a.cmd](a)


if __name__ == "__main__":
    sys.exit(main())
