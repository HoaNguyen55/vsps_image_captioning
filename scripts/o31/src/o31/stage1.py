"""G1 stage-1 for the KTVIC-train images that have no stage-1 record (prereg v3 §3.1; ERRATUM_O31_3 F1-F3).

The pool is all KTVIC train images (train_data.json, sha 72ee9b57: 3,769) minus the 2 byte twins of KTVIC test.
3,698 of them have records in the stage-1 tarball (b312de68: 3,700 records, twins included). The other 69, matched
by file stem (F3: 115 train names end in .png/.jpeg/.JPG; records are named by stem) and equal to the names of
data/screening/val_manifest.json (79f3628c), get a new stage-1 run with the FIRST-RELEASE code (F1): rescap/ and
scripts/generate_stage1.py of commit 1f30d09, delivered as `git archive 1f30d09 rescap scripts/generate_stage1.py`,
every file checked against RELEASE below, loaded only after the HEAD-snapshot checks (use_release). main() runs
unchanged with its own defaults = configs/main.env: generator qwen2.5-vl-7b, verifier vintern-1b with K = 5 sampled
dual queries, max-entities 8, max-pairs 8, verifier tiles 4, colour cross-check on. F1's fixed run details:
transformers 4.51.3; Qwen2.5-VL-7B-Instruct @ cc594898 and Vintern-1B-v3_5 @ b98f263e loaded by hub id, offline,
from $HF_HOME (the checked folder must be the cache snapshot that loads); QWEN_MAX_PIXELS unset; the loaded
generator's attention implementation is recorded. F2: random, NumPy and torch seeded with 42 once before main().
Records land in OUT/records in the stage-1 format, with the train_data.json reference captions (load_manifest).

Cap: G1's 3.5 GPU-h (COMPUTE_PLAN G1, stage-1 plus the Vintern probes of these 69) from OUT/launch.json t0, wall
time (ERRATUM_O31_2 E7). The Vintern probe job runs with --out OUT and so keeps the same t0. At the cap the run
stops after the image in flight (generate_stage1's own stop flag) and writes STOP.json. Logs print counts only.
"""
from __future__ import annotations

import hashlib
import json
import os
import tarfile
import threading
import time
from pathlib import Path

from . import repo
from .probe import STOP, halt, refused_shas, sha_lines

KTVIC_TRAIN_SHA = "72ee9b57c350fb5f215e1f04701c515a51e5e415240e51a77c8ce00ce6316a0f"
RECORDS_TAR_SHA = "b312de68180a2f9bf31602bae917ed170b2630174c30c11e9ea59c64aff840b0"
N_TRAIN, N_RECORDS, N_NEW = 3769, 3700, 69
TWINS = ("00000003589.jpg", "00000007511.jpg")  # train 3589 = test 1335, train 7511 = test 507 (prereg §3.1)
MANIFEST = "o31_g1_manifest.json"  # generate_stage1.load_manifest reads a *_manifest.json as {"images": [...]}
FAIR_ARGS = ("--generator", "qwen2.5-vl-7b", "--verifier", "vintern-1b", "--max-entities", "8", "--max-pairs", "8",
             "--verifier-tiles", "4")
QWEN = {"repo": "Qwen/Qwen2.5-VL-7B-Instruct", "revision": "cc594898137f460bfe9f0759e9844b3ce807cfb5",
        "registry_key": "qwen25vl_7b"}
VINTERN = {"repo": "5CD-AI/Vintern-1B-v3_5", "revision": "b98f263eab246eb5269ade64edbdca8a887dc44d"}
TRANSFORMERS = "4.51.3"
CAP_H = 3.5
SEED = 42  # ERRATUM_O31_3 F2 (configs/main.env SEED)
SCREEN = ("data/screening/val_manifest.json", "79f3628c156c955698afb66393f4a3e2496c82c78427d603d19887fde6e18790")
RELEASE_COMMIT = "1f30d09"
RELEASE = {  # every file of `git archive 1f30d09 rescap scripts/generate_stage1.py` (ERRATUM_O31_3 F1)
    "rescap/__init__.py": "b712bea4d66e5e2e0f0cec1624ab244a025560ecc5d86f96cada2e0160a4890f",
    "rescap/chair.py": "16ef38bf025db67ccc5e4a159af3e8367bcf6cab4f6ca637263c24bd64ea34d6",
    "rescap/metrics.py": "46d60e97c634a9fb1343f93a6ccdcf29e575628e67f85ab6b66ee0e5cdf360ed",
    "rescap/metrics_svp.py": "f9b85faf4726eae2f2b5b442b3921f1f756ce67d3a775a8d54b1e56d2d00e3ad",
    "rescap/pipeline/generate.py": "72f8bc7cb215ed9d908d3004fd1743031d12e48f2b6a52d8ffc6591c2acdc58d",
    "rescap/pipeline/realize.py": "607278e01fb79c747add2502c9905c9fd9717c190d13a09c3bc7cf2ac857a972",
    "rescap/pipeline/select.py": "38ccd5b51ad37beefc2ba4b2b3ceb7e0c6b6f6d4887ca8e0812434dc74b13874",
    "rescap/pipeline/verify.py": "9802412537f391373e82a9a621f5b9e7b693d32972019ed5b107881c6c60e7a2",
    "rescap/repro.py": "c3f05b15d85c1bb3cb52b6252109caba1b6c3bc0f2010f620c88fc725dd3a21d",
    "rescap/svp/__init__.py": "5b7f52920de75cf59bde0ae657e292a876efc63292ca6db6a4d085bb9fec1424",
    "rescap/svp/entailment.py": "4462f44df80faa0adc620d98aa5d8bbb307243d450e9aee4801bb17a3a06db23",
    "rescap/svp/matching.py": "a9253060131aacfca8eaab9a4b2c473c487db96a7c1222f0b8e31f9f61b24003",
    "rescap/vi/__init__.py": "f898963e95fec7d9fb236295649404815634a1d949bfd74cd7c3b90ed493bf6c",
    "rescap/vi/classifier.py": "966cdab1fed8471ac57d225698e63f1e2a055435a5d669e9cca10eed703fed16",
    "rescap/vi/color.py": "242fc46f68ecb06c8eefde23350481d99e60566b3da64ab90cfa79db38fd3875",
    "rescap/vi/lexicon.py": "a1f431324f1a5b7ad50126b43a15297a1fff245ce2b710595b453ef642ea2c7e",
    "rescap/viz.py": "b0d122cc4f6118bc5d6d0554713d7ba0d7187994690e500a45acf30144420f02",
    "rescap/vlm/__init__.py": "13de9854599acedd32ea1798ea1acc475703fcd3aa4eb4dd715dc8eadcd632cd",
    "rescap/vlm/base.py": "e8fee5bc5b729534af67c6e462a27f0d83ba611f18ff8e3f2717b11eb393ae93",
    "rescap/vlm/mock.py": "33793de01b4f2790964342b1af2d4c2de18d793ae4693608283992475ed62ce7",
    "rescap/vlm/qwen_vl.py": "0990c54a930337a6f4e7ac38a9cc2d32259f60caf868417776b18ad3ed3930a7",
    "rescap/vlm/registry.py": "6c261406bde3d34a73f77ce961aff7d241e2a440ba75e154fccf3ae8d4a70297",
    "rescap/vlm/replay.py": "7554850252693081032596c59479128bf4d59b7e7b354356abb549baeb6d4f4d",
    "rescap/vlm/vintern.py": "05c52858e8ad288c48aa3575d832701c10bf8e4b55fb1297409f84d922a83493",
    "rescap/vocab.py": "c9143b2d973fc48a2231335844cd91ab702329c0b1aabb802884225e155967ec",
    "scripts/generate_stage1.py": "e9d911a1c32d4e3aa258cc26c33a4023e3ffb93207cbc41ecf65d23a1654cf57",
}
RELEASE_MODULES = ("rescap.pipeline.generate", "rescap.pipeline.verify", "rescap.pipeline.select",
                   "rescap.pipeline.realize", "rescap.vlm.registry", "rescap.vlm.qwen_vl", "rescap.vlm.vintern")


def _sha(p: Path) -> str:
    return hashlib.sha256(Path(p).read_bytes()).hexdigest()


def record_names(tar: Path) -> set:
    """File stems of the 3,700 tarball records, from member names only (no record is opened; F3)."""
    if _sha(tar) != RECORDS_TAR_SHA:
        raise SystemExit("FAULT stage-1 records tarball is not b312de68")
    with tarfile.open(tar, "r:gz") as tf:
        names = {Path(m.name).stem for m in tf if m.isfile() and m.name.endswith(".json")
                 and not Path(m.name).name.startswith("_")}
    if len(names) != N_RECORDS:
        raise SystemExit(f"FAULT tarball holds {len(names)} records, not {N_RECORDS}")
    return names


def new_items(items: list[dict], stems: set) -> list[dict]:
    """The pool images without a record: load_manifest items of train_data.json whose file stem is not a record stem
    (F3), in file order. Record stems are named back to their train file names; an unknown stem stays unmatched."""
    names = [i["file_name"] for i in items]
    if len(names) != N_TRAIN or len(set(names)) != N_TRAIN:
        raise SystemExit(f"FAULT train_data.json lists {len(set(names))} distinct images, not {N_TRAIN}")
    by_stem = {Path(n).stem: n for n in names}
    if len(by_stem) != N_TRAIN:
        raise SystemExit("FAULT two KTVIC-train files share a stem")
    have = {by_stem.get(s, s) for s in stems}
    if not set(TWINS) <= have or not have <= set(names):
        raise SystemExit("FAULT the records are not a subset of KTVIC train holding both byte twins")
    new = [i for i in items if i["file_name"] not in have]
    if len(new) != N_NEW or set(TWINS) & {i["file_name"] for i in new}:
        raise SystemExit(f"FAULT {len(new)} images without records, expected {N_NEW} (twins excluded)")
    return new


def check_env() -> None:
    import transformers

    if os.environ.get("QWEN_MAX_PIXELS"):
        raise SystemExit("FAULT QWEN_MAX_PIXELS must be unset (adapter default 1280*28*28, as stage 1)")
    if os.environ.get("HF_HUB_OFFLINE") != "1":
        raise SystemExit("FAULT need HF_HUB_OFFLINE=1")
    if transformers.__version__ != TRANSFORMERS:
        raise SystemExit(f"FAULT stage-1 needs transformers {TRANSFORMERS}, found {transformers.__version__}")


def check_cache(snap: Path, model: dict) -> None:
    """W7 (CC-521): the checked folder must be the $HF_HOME snapshot that rescap loads by hub id."""
    home = os.environ.get("HF_HOME")
    want = Path(home or "/nonexistent") / "hub" / ("models--" + model["repo"].replace("/", "--")) / "snapshots" / \
        model["revision"]
    if not home or Path(snap).resolve() != want.resolve():
        raise SystemExit(f"FAULT {model['repo']}: the checked snapshot is not the HF_HOME cache snapshot that loads")


def check_vintern(snap: Path) -> None:
    """Vintern binding for stage-1 (W7); its file pins are m0.check_model's (g12 stage1 calls both)."""
    check_cache(snap, VINTERN)


def check_qwen(snap: Path) -> None:
    """rescap loads Qwen by hub id from the HF cache: the snapshot dir is the pinned revision under $HF_HOME, refs/main
    points at it, and every B-N1 file pin holds (decode_hf_vlm.check_snapshot, unchanged)."""
    check_cache(snap, QWEN)
    repo()
    import decode_hf_vlm as LB

    from .probe import registry_entry

    m = registry_entry(QWEN["registry_key"])
    ref = snap.parent.parent / "refs" / "main"
    if m["revision"] != QWEN["revision"] or snap.name != QWEN["revision"] or not ref.is_file() \
            or ref.read_text().strip() != QWEN["revision"]:
        raise SystemExit("FAULT Qwen snapshot is not the B-N1 pinned revision in the HF cache")
    LB.check_snapshot(m, snap)


def use_release(tree: Path, pins: dict | None = None):
    """F1: the 1f30d09 tree, every file equal to its pin and no other file; then rescap and generate_stage1 load from
    it. Call after the HEAD-snapshot checks (check_qwen, m0.check_model); probes, K0 and the rest keep HEAD."""
    import importlib
    import sys

    pins = RELEASE if pins is None else pins
    tree = Path(tree).resolve()
    files = {str(p.relative_to(tree)) for p in tree.rglob("*") if p.is_file() and "__pycache__" not in p.parts}
    bad = [f for f in pins if not (tree / f).is_file() or _sha(tree / f) != pins[f]]
    if bad or files != set(pins):
        raise SystemExit(f"FAULT release tree differs from the {RELEASE_COMMIT} pins: {len(bad)} changed, "
                         f"{len(files ^ set(pins))} extra or missing")
    for k in [k for k in sys.modules if k == "generate_stage1" or k == "rescap" or k.startswith("rescap.")]:
        del sys.modules[k]
    sys.path[:0] = [str(tree), str(tree / "scripts")]
    g = importlib.import_module("generate_stage1")
    for m in (g, *map(importlib.import_module, RELEASE_MODULES)):
        if not Path(m.__file__).resolve().is_relative_to(tree):
            raise SystemExit(f"FAULT {m.__name__} loads from outside the release tree")
    return g


def screen_names() -> list[str]:
    root = repo()
    rel, want = SCREEN
    if _sha(root / rel) != want:
        raise SystemExit(f"FAULT {rel} differs from its pin")
    return [i["file_name"] for i in json.loads((root / rel).read_text(encoding="utf-8"))["images"]]


def prepare(stage: Path, train_json: Path, records_tar: Path, g, refused: set | None = None,
            screen: list | None = None) -> list[dict]:
    """Write stage/datasets/ktvic/o31_g1_manifest.json for the 69 images (g = the release generate_stage1); every
    image present, none refused, and the 69 names equal the screening manifest's (F3)."""
    if _sha(train_json) != KTVIC_TRAIN_SHA:
        raise SystemExit("FAULT train_data.json is not the pinned KTVIC train file (72ee9b57)")
    kt = stage / "datasets" / "ktvic"
    if (kt / train_json.name).resolve() != train_json.resolve():
        raise SystemExit("FAULT train_data.json must be the staged copy in NCS_DATA/datasets/ktvic")
    g.KTVIC = kt  # generate_stage1 reads KTVIC at import time from NCS_DATA; pinned to the staged folder
    new = new_items(g.load_manifest(train_json.name), record_names(records_tar))
    screen = screen_names() if screen is None else screen
    if sorted(i["file_name"] for i in new) != sorted(screen):
        raise SystemExit("FAULT the 69 images differ from data/screening/val_manifest.json (79f3628c)")
    refused = refused_shas() if refused is None else refused
    bad = [i["file_name"] for i in new if not (kt / "images" / i["file_name"]).is_file()
           or _sha(kt / "images" / i["file_name"]) in refused]
    if bad:
        raise SystemExit(f"FAULT {len(bad)} of the {N_NEW} images are missing or refused")
    (kt / MANIFEST).write_text(json.dumps({"images": new}, ensure_ascii=False), encoding="utf-8")
    return new


def seed_all(seed: int = SEED) -> None:
    """F2: Python random, NumPy and torch (CPU and CUDA) seeded once; no deterministic-algorithm switch."""
    import random

    import numpy as np
    import torch

    random.seed(seed)
    np.random.seed(seed)
    torch.manual_seed(seed)
    if torch.cuda.is_available():
        torch.cuda.manual_seed_all(seed)


def attn_recorder(rec: dict):
    """F1: record the loaded generator's attention implementation (QwenVLAdapter.load of the loaded rescap)."""
    from rescap.vlm.qwen_vl import QwenVLAdapter

    orig = QwenVLAdapter.load

    def load(self):
        res = orig(self)
        rec.setdefault("attn_implementation", getattr(self, "attn_implementation", None))
        return res
    QwenVLAdapter.load = load
    return lambda: setattr(QwenVLAdapter, "load", orig)


def run(out: Path, stage: Path, new: list[dict], g, cap_h: float = CAP_H, main=None) -> int:
    """g.main() (the release generate_stage1) unchanged, with its FAIR flags, on the 69 images; the cap stops it after
    the image in flight. Returns 0 iff OUT/records holds exactly the 69 records (matched by stem)."""
    import sys

    out.mkdir(parents=True, exist_ok=True)
    if (out / STOP).exists():
        raise SystemExit(f"REFUSED: {out / STOP} exists; no resume without a ruling")
    lf = out / "launch.json"
    if not lf.exists():
        lf.write_text(json.dumps({"t0": time.time(), "job": "g1_stage1", "images": len(new)}) + "\n")
    t0 = json.loads(lf.read_text())["t0"]
    left = cap_h * 3600 - (time.time() - t0)
    if left <= 0:
        return halt(out, 4, "CAP_STOP before stage-1")
    g.KTVIC = stage / "datasets" / "ktvic"
    g._stop = False
    timer = threading.Timer(left, lambda: setattr(g, "_stop", True))
    timer.daemon = True
    rec_dir = out / "records"
    sys.argv = ["generate_stage1.py", "--source", MANIFEST, "--out", str(rec_dir), *FAIR_ARGS]
    seen: dict = {}
    restore = attn_recorder(seen)
    seed_all()
    timer.start()
    try:
        rc = (main or g.main)()
    finally:
        timer.cancel()
        restore()
    got = sorted(p.stem for p in rec_dir.glob("*.json") if not p.name.startswith("_"))
    want = sorted(Path(i["file_name"]).stem for i in new)
    rec = {"rc": rc, "records": len(got), "expected": len(want), "names_sha256": sha_lines(got),
           "elapsed_h": (time.time() - t0) / 3600, "seed": SEED, "release_commit": RELEASE_COMMIT,
           "generate_stage1_sha256": _sha(g.__file__), "attn_implementation": seen.get("attn_implementation")}
    (out / "g1_stage1.json").write_text(json.dumps(rec) + "\n")
    if g._stop:
        return halt(out, 4, f"CAP_STOP in stage-1 after {len(got)} records")
    print(json.dumps({k: rec[k] for k in ("rc", "records", "expected", "elapsed_h")}))
    return 0 if rc == 0 and got == want else 5  # 5: failed images; the same command may resume (no marker)
