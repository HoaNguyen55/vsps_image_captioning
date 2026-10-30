#!/usr/bin/env python3
"""Paper A, A-T3 (TIER 1 DEV-EXPLORE; tier-2/3 analysis frozen here, not actionable before CC-183 r9): a replication
of A's gold-completeness tests on COCO with four pinned LVLMs (InternVL3, LLaVA-OV, Idefics3, Aya-Vision; three LLM
families, two of the four Qwen-family LLMs; CC-184 F3). Gold rungs per image: L = COCO-80 instance categories (annotated,
not exhaustive), R1/R2/R5 = 1/2/5 Karpathy references drawn by the frozen p50.draw() (rng 1, 20 replicates).
Joint primary (CC-183 r4): AD-1' = slope[L] - slope[R1] > 0 (a NEW variant) AND AD-2 = X5 (R1 within L below the
size-matched random-deletion null of L). L vs R5 is always reported as PREMISE_NOT_MET. X4 enters Holm by r5 only.
Prereg: manuscript/prereg/2026-10-30_a_t3/PREREG.md (CC-183).

    python3 scripts/a_t3/a_t3.py --selftest                                   CPU, synthetic only
    python3 scripts/a_t3/a_t3.py registry --out REG                           A registry from the 3 pinned sources
    python3 scripts/a_t3/a_t3.py lists --karpathy K --val2017-ids F           laptop: a_t3_lists.json (ids only)
    python3 scripts/a_t3/a_t3.py gold --karpathy K --ann Z --set S --out O    laptop/M2 dev gold (class names) + premise;
                                                                              --set pool = the W3 gate (counts only)
    python3 scripts/a_t3/a_t3.py stage --gold G --set S --root R --val2017-ids F --valsha V   fetch dev images
    python  scripts/a_t3/a_t3.py register --root R --set S --models M.. --out REG   runtime registration
    python  scripts/a_t3/a_t3.py guard --head H --val2017-ids F --valsha V    before every GPU step (W8)
    python  scripts/a_t3/a_t3.py left --ledger L --cap-h C                    seconds left under a cap
    python  scripts/a_t3/a_t3.py jobcfg --tier T --host H --reg REG           job out dir and cap (tier 2; tier 3 m3 only)
    python  scripts/a_t3/a_t3.py t3gate --test-list F [--gold G]              m3: tier-3 precheck (CC-203 W3/W6)
    python  scripts/a_t3/a_t3.py stage3 --test-list F --gold G --src D --root R --valsha V   m3: stage the test ids
    python  scripts/a_t3/a_t3.py valsha --dir D --out O                       m3 only: val2017 image sha256 (numbers)
    python  scripts/a_t3/a_t3.py neardup --cand-dir D --ref NAME=DIR.. --sscd PT --out O   m3 only (W2): drop ids
    python3 scripts/a_t3/a_t3.py testlist --karpathy K --val2017-ids F [--drop NAME=FILE..] --out O   W1 builder;
                                                                              NOT a reservation (r9)
    python3 scripts/a_t3/a_t3.py score --tier 1 --raw DIR --gold G --out O    once per tier

No caption text is printed or written: gold files hold COCO-80 class names and counts only. val2017 ids are refused
everywhere except on m3 after the test reservation (TEST_RESERVED).
"""
from __future__ import annotations

import argparse
import hashlib
import json
import math
import os
import re
import sys
import urllib.request
import zipfile
from pathlib import Path

import numpy as np

HERE = Path(__file__).resolve().parent
ROOT = HERE.parents[1]
sys.path[:0] = [str(HERE.parent / "pascal50s"), str(HERE.parent / "a_t1"), str(HERE.parent / "grl")]
import p50  # noqa: E402  draw(), BOOT constants, timed ledger, dump (puts g2b and lb on sys.path)
import p50x  # noqa: E402  salience() (X4/X5 null) and holm(), unchanged
import a_t1  # noqa: E402  order(), predict(), predict_null(), norm_cdf(), unchanged
import common  # noqa: E402  host_ok(), scan(), COCO_RE (GRL guard helpers), unchanged

PDIR = ROOT / "manuscript/prereg/2026-10-30_a_t3"
LISTS, REGISTRY, PREREG = PDIR / "a_t3_lists.json", PDIR / "a_t3_registry.json", PDIR / "PREREG.md"
PREREG_SHA256 = "a7422fbfd6e35e84c6862c9c0314648eca4e36226d4acec3849dec015b3f3c64"  # finalisation; `score` refuses while empty
TEST_RESERVED = "CC-197"  # CC-183 r9: the LOG id of the re-read ruling that reserves the W1 list; empty = no tier-3 step
PI_X4_ACCEPT = ""  # CC-184 F1: LOG id of the PI accepting an AD-1'/X5-only replication; empty = X4_NOT_EVALUABLE stops
AYA_OUT = ""  # CC-184 F9: LOG id recording Aya's §4 drop; empty = tier 1 waits for both Aya preds
CAP_GPU_H = 40.0  # THE A-T3 GPU cap (all tiers, all machines); PI-1030d (CC-184 P1). Never changed after a decode
AYA_DEADLINE = "2026-11-03T00:00:00Z"  # CC-184 F9 default (or 72 h after M2 tier-1 BLOCK DONE, if earlier)
DATE_STOP = {1: "2099-01-01T00:00:00Z", 2: "2026-11-05T00:00:00Z", 3: "2026-11-07T00:00:00Z"}  # F2: no decode starts after
SCORE_DIR = ROOT / "data/results/a_t3"  # F9: score writes only data/results/a_t3/tier{n}.json
VALSHA_SHA256 = "51baa3e4fc4c8cb373fb3e2938709aa16502526d15369ef79dad536f792b8787"  # sha256 of the m3-made val2017 image-sha file; `guard` fails closed while empty (W8)
PREREG_ID = "2026-10-30_a_t3_coco_dev"
PIN = {"karpathy": "2fd999220673258012acfb411a4e7e66af7d488050b2519b0badcc49b7600b8d",  # dataset_coco.json
       "val2017_ids": "ea37cee007069bde6d45a67186cc6c2591d0c6d7effd3c481996b6b367e060b6",  # prereg val2017_ids.txt
       # (5,000 ids, one per line; made from .session_backup/.../val2017_names.txt 612097d2..., guard input, not a reservation)
       "exclusion": "c52a96d18925b974878ae1a970c3f9133fb3482216676fd41871eeabb68cc77f",  # dev_pools exclusion.json
       "ann2017": "113a836d90195ee1f884e704da6304dfaaecff1f023f49b6ca93c4aaae470268",  # annotations_trainval2017.zip
       "sscd": "9f26bd4c848cc19b73d2ae92eea6e04886f61a7b764ceb7a13aeee62e6a6db56"}  # C's SSCD (cen_pool.SSCD_SHA256)
EXCLUSION = ROOT / "manuscript/prereg/2026-10-21_dev_pools/exclusion.json"
DEV_MEMBER, TEST_MEMBER = "annotations/instances_train2017.json", "annotations/instances_val2017.json"
SOURCES = {"a_n2": ("manuscript/prereg/2026-10-19_a_n2_lvlm_gold_ladder.json", p50.A_N2[1]),
           "l1b": ("manuscript/prereg/2026-10-29_l1b/l1b_registry.json",
                   "cd210a7ca0f85b10c6f9ee95f8b737284f5029ef5f05c84d1ee760d18e7b96e3"),
           "c_t1": ("manuscript/prereg/2026-10-30_c_t1/c_t1_registry.json",
                    "09e6f90a09735125fed09620b6a1323ef12dafc6bf0a4a4bdf1a4af1087eba3c")}
# A registry (W10): model -> (source, revision prefix, LM family, vision tower to verify at the pin, host role)
MODELS = {"internvl3_8b": ("a_n2", "259a3b64", "qwen2.5 (Qwen2.5-7B)", "InternViT-300M (verify at pin)", "m4"),
          "llava_ov_7b": ("a_n2", "0d506805", "qwen2 (Qwen2-7B)", "SigLIP-so400m (verify at pin)", "m4"),
          "idefics3_8b": ("a_n2", "fddb4ff7", "llama3.1 (Llama-3.1-8B)", "SigLIP-so400m (verify at pin)", "m4"),
          "gemma3_4b": ("l1b", "093f9f38", "gemma3", "SigLIP-400M (verify at pin)", "m4"),
          "aya_vision_8b": ("c_t1", "d7601ac8", "cohere2 (Command R7B)", "SigLIP2-so400m-patch14-384 (verify at pin)",
                            "m3")}
N_D1, N_D2, N_SMOKE = 1000, 1000, 20
N_TEST_PLAN = 3500  # fixed planning lower bound for the predictors (W1 count <= 3,685); never replaced by the W1 count
P_GO, ALPHA, KS = 0.98, 0.025, (1, 2, 5)
CAP_H = {"tier1_m4": 6.0, "tier1_m3": 2.0,  # per-machine caps inside CAP_GPU_H; tier 2 (OPS-1030at3p): measured
         "tier2_m4": 6.0, "tier2_m3": 2.0,  # tier-1 use m4 3.92 h, m3 1.42 h on the same 1,000-image size
         "tier3_m3": 19.69}  # CC-203 W5: the PREREG tier-3 projection for 3,685 images, fixed from the ledger
T3_LIST_SHA = "5aaa479fa57f9749ecd1258ae7a9f91d8b0e9b322ea1fd4418a5f91b1354db26"  # r9 list file (CC-197)
T3_IDS_SHA = "b0aefdb4a61c8099369d7f42a5625ab5aa83ec310a9f28f04bc2f00102727215"  # its 3,232 ids
TIER2_SHA = "5bc221e4041a8e3ca4a2780eefc2bb52222946b20626eeae061681dce032eaa0"  # tier2.json (TIER2.sha256, d43f787)
B_REH, R_REH = 200, 200  # tier-2 rehearsal: image-bootstrap resamples, null replicates per resample
C_NEAR_DROPS = (129062, 284623, 427649, 458410, 465179, 471991, 527616, 562059)  # C's 8 drops (CC-183 chair)
BAD_NAME = re.compile(r"val2017|val2014\.zip|train2014\.zip|annotations_trainval|captions_val|instances_val", re.I)


def sha_bytes(b: bytes) -> str:
    return hashlib.sha256(b).hexdigest()


def check_pin(p: Path, key: str) -> None:
    if p50.sha_file(p) != PIN[key]:
        raise SystemExit(f"{p}: sha256 differs from PIN[{key!r}]")


def machine_id(mid_file: Path = Path("/root/.vsps_machine_id")) -> str:
    return mid_file.read_text().strip().lower() if mid_file.is_file() else ""


def run_id(m: str, q: str, tier: int = 1) -> str:
    return f"at3t{tier}_{m}-{q}"


# ------------------------------------------------------------------------------------------------ ids (laptop)
def val2017_ids(path: Path) -> set[int]:
    check_pin(path, "val2017_ids")
    ids = {int(Path(x.strip()).stem) for x in path.read_text().splitlines() if x.strip()}
    if len(ids) != 5000:
        raise SystemExit(f"{path}: {len(ids)} val2017 ids, not 5,000")
    return ids


def excluded_coco() -> dict[str, set[int]]:
    check_pin(EXCLUSION, "exclusion")
    return {k: {int(x) for x in v} for k, v in json.loads(EXCLUSION.read_text())["ids"]["coco"].items()}


def karpathy(path: Path) -> dict[int, dict]:
    check_pin(path, "karpathy")
    return {int(r["cocoid"]): r for r in json.loads(path.read_text(encoding="utf-8"))["images"]}


def split_pool(restval: set[int], v17: set[int], excl: dict[str, set[int]]) -> tuple[list[str], dict]:
    """CC-183 r7: restval minus val2017 minus every exclusion.json coco list, ordered by sha256(str(id))."""
    pool = restval - v17 - set().union(*excl.values())
    counts = {"restval": len(restval), "restval_in_val2017": len(restval & v17),
              **{f"minus_{k}": len((restval - v17) & s) for k, s in sorted(excl.items())}, "pool": len(pool)}
    return a_t1.order([str(i) for i in pool]), counts


def cmd_lists(kar: Path, v17p: Path) -> dict:
    K, v17 = karpathy(kar), val2017_ids(v17p)
    o, counts = split_pool({i for i, r in K.items() if r["split"] == "restval"}, v17, excluded_coco())
    S = {"D1": o[:N_D1], "D2": o[N_D1:N_D1 + N_D2], "smoke": o[N_D1 + N_D2:N_D1 + N_D2 + N_SMOKE]}
    if [len(v) for v in S.values()] != [N_D1, N_D2, N_SMOKE] or any(int(i) in v17 for v in S.values() for i in v):
        raise SystemExit("set sizes or a val2017 id in a dev set")
    return {"label": "A-T3 dev lists (COCO ids only; tier 1 D1, tier 2 D2, smoke)", "prereg_id": PREREG_ID,
            "rule": "pool = Karpathy restval minus val2017 (5,000 ids) minus every exclusion.json coco list; ordered "
                    "by sha256(str(cocoid)); D1 = first 1,000, D2 = next 1,000, smoke = next 20. Dev-test "
                    "near-duplicates are dropped from the TEST side (W2), so these lists do not move.",
            "pins": {k: PIN[k] for k in ("karpathy", "val2017_ids", "exclusion")}, "counts": counts,
            "pool_ids_sha256": sha_bytes(("\n".join(o) + "\n").encode()),
            "sets": {k: {"n": len(v), "ids": v, "ids_sha256": sha_bytes(("\n".join(v) + "\n").encode())}
                     for k, v in S.items()}}


def load_set(name: str) -> list[str]:
    return json.loads(LISTS.read_text(encoding="utf-8"))["sets"][name]["ids"]


# ------------------------------------------------------------------------------------------------ gold
def instances(zp: Path, member: str, en) -> dict[int, set[str]]:
    """image id -> COCO-80 category names with any instance (crowd included), from ONE member of the pinned zip."""
    check_pin(zp, "ann2017")
    if member == TEST_MEMBER and not (machine_id() == "m3" and TEST_RESERVED):
        raise SystemExit("REFUSED: val2017 gold is read on m3 only, after the r9 reservation")
    with zipfile.ZipFile(zp) as z:
        A = json.loads(z.read(member))
    cats = {c["id"]: c["name"] for c in A["categories"]}
    if len(set(cats.values())) != 80 or any(en(n) != {n} for n in cats.values()):
        raise SystemExit("COCO category names are not the matcher's 80 classes")
    out = {int(im["id"]): set() for im in A["images"]}
    for a in A["annotations"]:
        out[int(a["image_id"])].add(cats[a["category_id"]])
    return out


def gold_sets(ids: list[str], K: dict, inst: dict, en, v17: set[int], tier3: bool = False) -> dict:
    """L_i and the matcher classes of every reference of image i (class names only; no text kept)."""
    bad = [i for i in ids if int(i) in v17]
    if bad and not tier3:
        raise SystemExit(f"REFUSED: {len(bad)} val2017 id(s) in a dev gold request")
    miss = [i for i in ids if int(i) not in inst]
    if miss:
        raise SystemExit(f"{len(miss)} id(s) not in the instance file (e.g. {miss[:3]})")
    return {"L": {i: sorted(inst[int(i)]) for i in ids},
            "refs": {i: [sorted(en(s["raw"])) for s in K[int(i)]["sentences"]] for i in ids}}


def rungs(refm: list[list[set]]) -> dict[int, list[list[set]]]:
    """k -> 20 replicate golds (one set per image): the union of the references p50.draw() picks (rng 1)."""
    sub = p50.draw([len(r) for r in refm])
    return {k: [[set().union(*(refm[n][j] for j in s[n])) for n in range(len(refm))] for s in sub[k]] for k in KS}


def premise(L: list[set], refm: list[list[set]], G: dict | None = None) -> dict:
    """Output-free gate (A-T1 §3 form with R1 = one drawn reference; CC-183 r4/W3). Sums over images; R-sums are
    means over the 20 replicates. G: the replicate golds already drawn for these images (score time)."""
    G = G or rungs(refm)
    sL = sum(map(len, L))
    s = {k: float(np.mean([sum(map(len, rep)) for rep in G[k]])) for k in KS}
    sin = {k: float(np.mean([sum(len(r & l) for r, l in zip(rep, L)) for rep in G[k]])) for k in KS}
    sall = sum(len(set().union(*r)) for r in refm)
    return {"n_images": len(L), "sum_L": sL, "sum_R": {str(k): s[k] for k in KS},
            "sum_R_in_L": {str(k): sin[k] for k in KS}, "sum_Rall": sall,
            "L_over_R1": sL / s[1], "L_over_2R1inL": sL / (2 * sin[1]), "L_over_R5": sL / s[5],
            "evaluable_2x": sL >= 2 * sin[1], "gate_R1": sL / s[1] >= 2 and sL >= 2 * sin[1],
            "gate_R5_A_T1_form": sL / s[5] >= 2 and sL >= 2 * sin[5]}


def cmd_gold(kar: Path, zp: Path, name: str, v17p: Path, test_list: Path | None = None) -> dict:
    import score_g2b as g

    en, K, v17 = g.MATCH["coco80"]["en"], karpathy(kar), val2017_ids(v17p)
    member, t3 = DEV_MEMBER, name == "test"
    if name == "pool":  # W3: the whole dev pool, counts only
        ids, _ = split_pool({i for i, r in K.items() if r["split"] == "restval"}, v17, excluded_coco())
    elif t3:  # tier 3: m3 only, after r9; the premise is logged before the first decode (W7)
        need_m3()
        if not TEST_RESERVED or test_list is None:
            raise SystemExit("REFUSED: no reserved test list (CC-183 r9)")
        ids, member = json.loads(test_list.read_text())["ids"], TEST_MEMBER
    else:
        ids = load_set(name)
    gs = gold_sets(ids, K, instances(zp, member, en), en, v17, t3)
    pr = premise([set(gs["L"][i]) for i in ids], [[set(x) for x in gs["refs"][i]] for i in ids])
    head = {"label": f"A-T3 gold for {name} (COCO-80 class names only)", "set": name, "premise": pr,
            "provenance": {"pins": PIN, "member": member, "script_sha256": p50.sha_file(Path(__file__)),
                           "ids_sha256": sha_bytes(("\n".join(ids) + "\n").encode())}}
    return head if name == "pool" else {**head, **gs}


# ------------------------------------------------------------------------------------------------ stage (dev)
def coco_url(i: str) -> str:
    return f"http://images.cocodataset.org/train2017/{int(i):012d}.jpg"  # train2017 holds no val2017 image


def cmd_stage(gold: Path, name: str, root: Path, v17p: Path, valsha: Path, fetch=None) -> dict:
    G = json.loads(gold.read_text(encoding="utf-8"))
    if G["set"] != name or not G["premise"]["gate_R1"]:
        raise SystemExit(f"PREMISE_NOT_MET on {G['set']}: {G['premise']} (no GPU step; report it)")
    ids, v17, bad_sha = load_set(name), val2017_ids(v17p), valsha_set(valsha)
    if any(int(i) in v17 for i in ids):
        raise SystemExit("REFUSED: a val2017 id in a dev set")
    fetch = fetch or (lambda u: urllib.request.urlopen(u, timeout=60).read())
    (root / "images").mkdir(parents=True, exist_ok=True)
    rows = ""
    for i in ids:
        f = root / "images" / f"{int(i):012d}.jpg"
        b = f.read_bytes() if f.exists() else fetch(coco_url(i))
        if b[:2] != b"\xff\xd8" or sha_bytes(b) in bad_sha:
            raise SystemExit(f"{i}: not a JPEG, or its sha256 is a val2017 image sha")
        f.write_bytes(b)
        rows += f"{i}\t{f.name}\t{sha_bytes(b)}\n"
    (root / "sets").mkdir(parents=True, exist_ok=True)
    (root / f"sets/a_t3_{name}.tsv").write_text(rows, encoding="utf-8")
    return {name: sha_bytes(rows.encode()), "premise": G["premise"]}


# ------------------------------------------------------------------------------------------------ registry (W10)
def source(key: str) -> dict:
    path, pin = SOURCES[key]
    b = (ROOT / path).read_bytes()
    if sha_bytes(b) != pin:
        raise SystemExit(f"REFUSED: {path} differs from its pin")
    return json.loads(b)


def complete(block: dict) -> bool:
    return all(f["hash"] for f in block["files"].values())


def build_registry() -> dict:
    out = {"schema": "vsps.a_t3_registry.v1", "prereg_id": PREREG_ID,
           "statement": "A-T3 model set. Every model block is copied byte-for-byte (as JSON) from its source "
                        "registry, checked by `registry --check`. A model whose block has a null hash at the "
                        "finalisation commit is out of A-T3 for all three tiers (no late fill; CC-168b W16).",
           "sources": {k: {"path": p, "sha256": s} for k, (p, s) in SOURCES.items()}, "order": list(MODELS),
           "models": {}, "families": {}}
    for m, (src, rev, lm, vis, host) in MODELS.items():
        b = source(src)["models"][m]
        if not b["revision"].startswith(rev):
            raise SystemExit(f"{m}: revision {b['revision'][:8]} is not the CC-183 W10 pin {rev}")
        out["models"][m] = b
        out["families"][m] = {"lm_family": lm, "vision_tower": vis, "host_role": host, "source": src,
                              "pins_complete": complete(b)}
    return out


def registry() -> dict:
    R = json.loads(REGISTRY.read_text(encoding="utf-8"))
    if json.dumps(R, sort_keys=True) != json.dumps(build_registry(), sort_keys=True):
        raise SystemExit("REFUSED: a_t3_registry.json differs from its pinned sources")
    return R


def in_models(R: dict) -> list[str]:
    return [m for m in R["order"] if R["families"][m]["pins_complete"]]


def register(root: Path, name: str, models: list[str], tier: int = 1) -> dict:
    """p50.register's pattern: A-N2 schema/decode/decoder/venv unchanged; models from the A registry."""
    date_ok(tier)
    A, R = source("a_n2"), registry()
    bad = [m for m in models if m not in in_models(R)]
    if bad:
        raise SystemExit(f"REFUSED: {bad} not in the A-T3 model set (pins incomplete or unknown)")
    reg = {k: A[k] for k in ("schema", "decode", "decoder", "venv")}
    reg.update({"prereg_id": PREREG_ID, "statement": "runtime registration built by scripts/a_t3/a_t3.py register",
                "models": {m: R["models"][m] for m in models}, "model_list": models, "datasets": {}, "runs": []})
    man = root / f"sets/a_t3_{name}.tsv"
    reg["datasets"][f"a_t3_{name}"] = {"manifest": {"path": str(man), "sha256": p50.sha_file(man)},
                                       "n_images": len(man.read_text(encoding="utf-8").splitlines()),
                                       "image_dir": f"{root.name}/images"}
    reg["runs"] = [{"run_id": run_id(m, q, tier), "model": m, "dataset": f"a_t3_{name}", "prompt_mode": q}
                   for m in models for q in p50.MODES]
    return reg


# ------------------------------------------------------------------------------------------------ guard (W8)
def valsha_set(path: Path | None) -> set[str]:
    """The m3-made val2017 image sha256 list; fail closed while it is not pinned."""
    if not VALSHA_SHA256 or path is None or not Path(path).is_file() or p50.sha_file(path) != VALSHA_SHA256:
        raise SystemExit("REFUSED: the val2017 image-sha list (made on m3 by `valsha`) is missing or not pinned")
    s = set(json.loads(Path(path).read_text())["sha256"].values())
    if len(s) != 5000:
        raise SystemExit("val2017 sha list is not 5,000 entries")
    return s


def bad_names(data: Path, v17: set[int]) -> list[str]:
    """Any val2017 annotation/zip name, or any COCO-named image whose id is a val2017 id, under data (id only)."""
    out = []
    for p in data.rglob("*"):
        m = common.COCO_RE.search(p.name)
        if BAD_NAME.search(str(p)) or (p.is_file() and m and int(m.group(1)) in v17):
            out.append(str(p))
    return out


def guard(head: str, v17p: Path, valsha: Path | None, mid_file: Path = Path("/root/.vsps_machine_id")) -> str:
    """m4 (M2): host, idle GPU, HEAD; no val2017 id or file name anywhere under $NCS_DATA/datasets, no val2017 image
    sha in the A-T3 staging dir; no test-side set staged. m3 (M1, Aya dev cells): the A-T3 staging dir only."""
    mid = machine_id(mid_file)
    if mid not in ("m3", "m4") or common.host_ok(head, mid_file) != mid:
        raise SystemExit(f"REFUSED: machine id {mid or 'missing'!r}")
    v17, bad_sha = val2017_ids(v17p), valsha_set(valsha)
    data = Path(os.environ.get("NCS_DATA", "/root/ncs-data")) / "datasets"
    stage = data / "a_t3"
    common.scan([stage], v17, bad_sha)  # id and sha (ponytail: sha only here; the rest of $NCS_DATA is id/name-only)
    if mid == "m4":
        bad = bad_names(data, v17) if data.exists() else []
        if bad or any((data / d).exists() for d in ("pascal50s", "xm3600", "nocaps")):
            raise SystemExit(f"REFUSED: a val2017 file or a test-side set is on M2: {bad[:3]}")
    print("guard ok")
    return mid


def date_ok(tier: int, now: str | None = None) -> None:
    """CC-184 F2: no tier-2 decode starts after 2026-11-05T00:00Z, no tier-3 decode after 2026-11-07T00:00Z."""
    import datetime as dt

    now = now or dt.datetime.now(dt.timezone.utc).strftime("%Y-%m-%dT%H:%M:%SZ")
    if now >= DATE_STOP[tier]:
        raise SystemExit(f"DATE STOP: tier {tier} decode may not start after {DATE_STOP[tier]} (A-T3 stops; §7 sentence)")


def reg_tier(reg: Path) -> int:
    return int(re.match(r"at3t(\d)_", json.loads(reg.read_text())["runs"][0]["run_id"]).group(1))


def job_cfg(tier: int, mid: str, reg: Path) -> tuple[str, float]:
    """a_t3_job.sh / a_t3_t3_job.sh (OPS-1030at3p, CC-203 W4): tier 2, or tier 3 on m3 only, from a registration
    whose every run is at3t{tier}_*; its own out dir (ledger, SUMS, EVENTS) and per-machine cap."""
    runs = [r["run_id"] for r in json.loads(reg.read_text())["runs"]]
    if tier not in (2, 3) or (tier == 3 and mid != "m3") or not runs or not all(r.startswith(f"at3t{tier}_") for r in runs):
        raise SystemExit(f"REFUSED: job tier {tier} on {mid}, registration runs {runs[:2]}; tier 2, or tier 3 on m3")
    return f"/root/outputs/a_t3_t{tier}", CAP_H[f"tier{tier}_{mid}"]


def left(ledger: Path, cap_h: float) -> int:
    return max(0, int(cap_h * 3600 - sum(b for _, b, _ in p50.ledger_rows(ledger))))


# ------------------------------------------------------------------------------------------------ tier 3 (CC-203)
def t3gate(lst: Path, gold: Path | None = None, mid_file: Path = Path("/root/.vsps_machine_id"),
           now: str | None = None) -> str:
    """CC-203 W3/W6, outside the frozen gold/score code (PREREG l.221): the reserved list, the committed
    REHEARSAL_PASS tier-2 result, m3, the tier-3 date stop and, with a gold file, its test-list provenance."""
    if machine_id(mid_file) != "m3":
        raise SystemExit("REFUSED t3gate: not the m3-role machine")
    date_ok(3, now)
    L = json.loads(lst.read_bytes())
    ids_sha = sha_bytes(("\n".join(L["ids"]) + "\n").encode())
    if p50.sha_file(lst) != T3_LIST_SHA or ids_sha != T3_IDS_SHA or L["ids_sha256"] != ids_sha or L["n"] != 3232:
        raise SystemExit("REFUSED t3gate: the test list is not the CC-197 r9 list")
    t2 = SCORE_DIR / "tier2.json"
    pin = (PDIR / "TIER2.sha256").read_text().split()[0]
    if not t2.is_file() or p50.sha_file(t2) != TIER2_SHA or pin != TIER2_SHA:
        raise SystemExit("REFUSED t3gate: tier2.json is not the committed TIER2.sha256 file")
    if json.loads(t2.read_text())["outcome"] != "REHEARSAL_PASS":
        raise SystemExit("REFUSED t3gate: tier 2 is not REHEARSAL_PASS")
    msg = f"t3gate ok list {T3_LIST_SHA} ids {T3_IDS_SHA} tier2 {TIER2_SHA} REHEARSAL_PASS m3"
    if gold is not None:
        G = json.loads(gold.read_text(encoding="utf-8"))
        pv = G["provenance"]
        if G["set"] != "test" or pv["ids_sha256"] != T3_IDS_SHA or pv["member"] != TEST_MEMBER or \
                pv["pins"]["ann2017"] != PIN["ann2017"]:
            raise SystemExit("REFUSED t3gate: the gold file is not the reserved-list val2017 gold")
        msg += f" goldfile {p50.sha_file(gold)} premise gate_R1 {G['premise']['gate_R1']}"
    return msg


def cmd_stage3(lst: Path, gold: Path, src: Path, root: Path, valsha: Path) -> dict:
    """Tier-3 staging (PREREG §6 F5 deviation, CC-203 W4): the 3,232 reserved ids copied from the m3 val2017 dir,
    each byte-checked against the pinned m3 sha list; refused unless the gate and the pre-decode premise hold."""
    print(t3gate(lst, gold))
    G = json.loads(gold.read_text(encoding="utf-8"))
    if not G["premise"]["gate_R1"]:
        raise SystemExit(f"PREMISE_NOT_MET on test: {G['premise']} (no decode; PREREG §3 sentence)")
    valsha_set(valsha)
    want = json.loads(Path(valsha).read_text())["sha256"]
    (root / "images").mkdir(parents=True, exist_ok=True)
    rows = ""
    for i in json.loads(lst.read_bytes())["ids"]:
        f = f"{int(i):012d}.jpg"
        b = (src / f).read_bytes()
        if sha_bytes(b) != want[str(int(i))]:
            raise SystemExit(f"{i}: sha256 differs from the m3 val2017 sha list")
        (root / "images" / f).write_bytes(b)
        rows += f"{i}\t{f}\t{sha_bytes(b)}\n"
    (root / "sets").mkdir(parents=True, exist_ok=True)
    (root / "sets/a_t3_test.tsv").write_text(rows, encoding="utf-8")
    return {"test": sha_bytes(rows.encode()), "n": len(rows.splitlines()), "premise": G["premise"]}


# ------------------------------------------------------------------------------------------------ m3-only steps
def need_m3() -> None:
    if machine_id() != "m3":
        raise SystemExit("REFUSED: runs on the m3-role machine (M1) only")


def cmd_valsha(d: Path, v17p: Path) -> dict:
    need_m3()
    shas = {str(int(p.stem)): p50.sha_file(p) for p in sorted(d.glob("*.jpg"))}
    if {int(i) for i in shas} != val2017_ids(v17p):  # CC-184 F7
        raise SystemExit(f"{len(shas)} images in {d}: ids are not the 5,000 val2017 ids")
    return {"label": "COCO val2017 image sha256 (numbers only; W8 guard input)", "sha256": shas}


def cmd_neardup(cand: Path, refs: dict[str, Path], sscd: Path) -> dict:
    """W2: C's build_memory rule unchanged (min(pHash, dHash) <= 10 AND SSCD >= 0.5, mirrored; byte-identical).
    Candidates = COCO-named images in cand; output = drop ids per reference set (numbers only)."""
    need_m3()
    check_pin(sscd, "sscd")
    sys.path.insert(0, str(ROOT / "scripts/c_stage1"))
    import build_memory as BM

    paths = sorted(p for p in cand.glob("*.jpg") if common.COCO_RE.search(p.name))
    ids = [int(common.COCO_RE.search(p.name).group(1)) for p in paths]
    fx = BM.features(paths, str(sscd))
    drops = {}
    for name, d in refs.items():
        hit = BM.near(fx, BM.features(sorted(q for q in d.rglob("*") if common.IMG_RE.search(q.name)), str(sscd)))
        drops[name] = sorted(i for i, h in zip(ids, hit) if h)
    return {"label": "W2 near-duplicate drop ids (C's build_memory.near, unchanged)",
            "rule": {"hash_max": BM.HASH_MAX, "sscd_min": BM.SSCD_MIN}, "n_candidates": len(ids),
            "unreadable": [ids[k] for k in fx["unreadable"]], "drops": drops,
            "drop_any": sorted(set().union(*map(set, drops.values()))) if drops else []}


def test_steps(restval: set[int], v17: set[int], excl: dict, drops: dict) -> tuple[list, list[str]]:
    cur = v17 & restval
    steps = [["val2017", len(v17)], ["cap_restval", len(cur)]]
    for name, s in [*sorted(excl.items()), ("c_near_dup_8", set(C_NEAR_DROPS)), *drops.items()]:
        cur = cur - s
        steps.append([f"minus_{name}", len(cur)])
    return steps, a_t1.order([str(i) for i in cur])


def cmd_testlist(kar: Path, v17p: Path, drops: dict[str, Path]) -> dict:
    """W1 by id only: val2017 cap restval, minus each exclusion.json coco list, minus C's 8, minus each --drop file.
    Every count is printed beside 5,000. NOT a reservation (CC-183 r9)."""
    K = karpathy(kar)
    steps, ids = test_steps({i for i, r in K.items() if r["split"] == "restval"}, val2017_ids(v17p), excluded_coco(),
                            {n: {int(x) for x in Path(f).read_text().split()} for n, f in drops.items()})
    return {"label": "A-T3 test candidate list (W1 rebuild)", "status": "NOT RESERVED (CC-183 r9)" if not
            TEST_RESERVED else f"reserved by {TEST_RESERVED}", "counts_beside_5000": steps, "n": len(ids),
            "ids": ids, "ids_sha256": sha_bytes(("\n".join(ids) + "\n").encode()),
            "pins": {k: PIN[k] for k in ("karpathy", "val2017_ids", "exclusion")}}


# ------------------------------------------------------------------------------------------------ analysis
def predict_null_boot(g, ment, golds, comp, idx, n_test: int, B: int = B_REH, R: int = R_REH, seed: int = 0) -> float:
    """Tier-2 rehearsal (W7): image bootstrap of the salience z, scaled to n_test; mean of Phi(z' - 1.96)."""
    rng, out = np.random.default_rng(seed), []
    for _ in range(B):
        ib = rng.choice(idx, len(idx), replace=True)
        r = p50x.salience(g, ment, golds, comp, ib, rng, R, True)
        out.append(a_t1.predict_null(r, len(idx), n_test))
    return float(np.mean(out))


def analysis(g, ids: list[str], gold: dict, caps: dict, models: list[str], tier: int = 1,
             n_boot=p50.N_BOOT, n_rep=p50x.R_NULL) -> dict:
    en = g.MATCH["coco80"]["en"]
    runs = [run_id(m, q, tier) for m in models for q in p50.MODES]
    ment = [[en(caps[r].get(i, "")) for i in ids] for r in runs]
    L = [set(gold["L"][i]) for i in ids]
    refm = [[set(x) for x in gold["refs"][i]] for i in ids]
    G, Rall = rungs(refm), [set().union(*r) for r in refm]
    clean = [n for n, i in enumerate(ids) if all(isinstance(caps[r].get(i), str) and caps[r][i].strip()
                                                 and g.is_clean(caps[r][i], "en") for r in runs)]
    if len(clean) < 2:
        return {"verdict": "NOT_EVALUABLE", "reason": "empty analysis set"}
    idx = np.array(clean)
    Wb = np.random.default_rng(p50.BOOT_SEED).multinomial(len(idx), [1 / len(idx)] * len(idx), size=n_boot).astype(float)
    one = np.ones((1, len(idx)))
    golds = {"L": [L], **{f"R{k}": G[k] for k in KS}}
    sl = {}
    for name, gd in golds.items():
        rw = [g.rows(m, gd) for m in ment]
        sl[name] = (float(g.stat_slope([g.scores(r, idx, one) for r in rw], None)[0]),
                    g.stat_slope([g.scores(r, idx, Wb) for r in rw], None))
    M = [float(g.scores(g.rows(m, [L]), idx, one)["M"][0]) for m in ment]
    ev = all(m > 0 for m in M) and len({round(m, 12) for m in M}) >= 2

    def diff(a, b, rule_label=None):
        pt, bs = sl[a][0] - sl[b][0], sl[a][1] - sl[b][1]
        iv = g.ci(bs, *p50.CI)
        v = g.verdict("sign_gt_0", pt, iv) if ev else "NOT_EVALUABLE"
        return {"point": pt, "ci95": iv, "verdict": rule_label or v, "rule_outcome": v, "_draws": bs,
                "p_one_sided": float((1 + (bs <= 0).sum()) / (len(bs) + 1))}

    pr = premise([L[n] for n in clean], [refm[n] for n in clean], {k: [[rep[n] for n in clean] for rep in G[k]]
                                                                   for k in KS})  # the slopes' own draws
    res = {"runs": runs, "n_images": len(idx), "n_dropped_unclean": len(ids) - len(idx), "M": M, "slopes": {k: v[0] for k, v in sl.items()}, "premise": pr,
           "AD1p": diff("L", "R1"), "L_vs_R5": diff("L", "R5", "PREMISE_NOT_MET"),
           "O2": {"R2-R1": diff("R2", "R1"), "R5-R2": diff("R5", "R2")}}
    res["O2"]["verdict"] = g.compound([res["O2"][k]["verdict"] for k in ("R2-R1", "R5-R2")])
    rng = np.random.default_rng(p50x.NULL_SEED)  # one stream: X5 (AD-2) first, then X4
    x5 = p50x.salience(g, ment, G[1], L, idx, rng, n_rep, ev)
    if not pr["evaluable_2x"]:
        x5["verdict"], x5["reason"] = "NOT_EVALUABLE", "sum |L| < 2 * sum |R1 & L|"
    res["X5"] = x5
    res["X4"] = p50x.salience(g, ment, G[1], Rall, idx, rng, n_rep, ev)
    res["_idx"], res["_ment"], res["_G1"], res["_L"], res["_Rall"] = idx, ment, G[1], L, Rall
    return res


def family(a: dict, x4_in: bool) -> dict:
    """Joint primary = AD-1' AND X5 (intersection-union, each at one-sided 0.025); Holm over {AD-1', X5} (+ X4 when
    promoted by r5) for any single claim."""
    fam = {"AD1p": a["AD1p"], "X5": a["X5"]} | ({"X4": a["X4"]} if x4_in else {})
    ps = {k: v["p_one_sided"] for k, v in fam.items() if v["verdict"] != "NOT_EVALUABLE"}
    keep = p50x.holm(ps, ALPHA)
    return {"joint": "PASS" if a["AD1p"]["verdict"] == "PASS" and a["X5"]["verdict"] == "PASS" else "NOT_PASS",
            "holm_p": ps, "holm_survives": keep, "x4_in_family": x4_in}


def outcome1(a: dict, p: dict) -> tuple[str, str]:
    """PREREG §6, clauses in written order."""
    if not a["premise"]["gate_R1"]:
        return "PREMISE_NOT_MET", "L/R1 < 2 or sum|L| < 2 sum|R1 & L|"
    if a["AD1p"]["verdict"] != "PASS" or a["X5"]["verdict"] != "PASS":
        return "NOT_REPRODUCED", f"AD1' {a['AD1p']['verdict']}, X5 {a['X5']['verdict']}"
    if min(p["AD1p"], p["X5"]) < P_GO:
        return "PASS_LOW_POWER", "predicted P(PASS) < 0.98 (Q8 default: stop)"
    if a["X4"]["verdict"] == "NOT_EVALUABLE":
        return "X4_NOT_EVALUABLE", "tiers 2-3 only if the PI accepts an AD-1'/X5-only replication (Q8 default: stop)"
    return "PROCEED_TO_TIER2", "all hold"


def outcome2(a: dict, p: dict) -> tuple[str, str]:
    if not a["premise"]["gate_R1"]:
        return "PREMISE_NOT_MET", "D2 premise"
    if a["AD1p"]["verdict"] != "PASS" or a["X5"]["verdict"] != "PASS" or min(p["AD1p"], p["X5"]) < P_GO:
        return "REHEARSAL_FAIL", "never touch the test (PI-1029o three-tier rule)"
    return "REHEARSAL_PASS", "test look allowed after the r9 reservation"


def tier1_binding(t1: Path | None, pi_x4: str = PI_X4_ACCEPT) -> tuple[bool, str, list[str]]:
    """Tiers 2-3 (CC-184 F1): only PROCEED_TO_TIER2 passes; X4_NOT_EVALUABLE only with PI_X4_ACCEPT set;
    PASS_LOW_POWER never. The X4 promotion and the model set are read from the tier-1 result, never set by hand."""
    if t1 is None:
        raise SystemExit("tiers 2-3 need --tier1 <tier-1 result>")
    T = json.loads(t1.read_text(encoding="utf-8"))
    ok = T["outcome"] == "PROCEED_TO_TIER2" or (T["outcome"] == "X4_NOT_EVALUABLE" and pi_x4)
    if not ok or not T["label"].startswith("A-T3 TIER 1"):
        raise SystemExit(f"tier-1 outcome {T['outcome']}: no tier 2/3")
    return bool(T["analysis"]["family"]["x4_in_family"]), p50.sha_file(t1), T["models"]


def excluded_ids(path: Path | None, tier: int) -> tuple[set[str], str | None]:
    """CC-184 F8: dev-side W2 hits (m3 `neardup`, ids only) leave the tier-1/2 analysis set; lists do not change."""
    if tier == 3:
        return set(), None
    if path is None:
        raise SystemExit("tiers 1-2 need --exclude <dev-side W2 drop ids> (CC-184 F8; may be empty)")
    D = json.loads(path.read_text(encoding="utf-8"))
    return {str(i) for i in D["drop_any"]}, p50.sha_file(path)


def score_models(R: dict, raw: Path, tier: int, t1_models: list[str] | None, aya_out: str = AYA_OUT) -> list[str]:
    """CC-184 F9 model-set lock: tier 1 waits for Aya unless AYA_OUT records its drop; tiers 2-3 = the tier-1 set."""
    have = [m for m in in_models(R) if all((raw / f"{run_id(m, q, tier)}.preds.json").exists() for q in p50.MODES)]
    if t1_models is not None:
        if have != t1_models:
            raise SystemExit(f"model set {have} is not the tier-1 set {t1_models}")
    elif "aya_vision_8b" in in_models(R) and "aya_vision_8b" not in have and not aya_out:
        raise SystemExit("tier 1 waits for both Aya preds until the §4 deadline; set AYA_OUT to record the drop")
    if len(have) < p50.MIN_MODELS:
        raise SystemExit(f"NOT_EVALUABLE: {len(have)} models decoded both prompts (< {p50.MIN_MODELS})")
    return have


def cmd_score(tier: int, raw: Path, gold_path: Path, t1: Path | None = None, excl: Path | None = None) -> None:
    import score_g2b as g

    out = SCORE_DIR / f"tier{tier}.json"
    if out.exists():
        raise SystemExit(f"{out} exists; A-T3 scores once per tier")
    if not PREREG_SHA256 or p50.sha_file(PREREG) != PREREG_SHA256:
        raise SystemExit("PREREG.md is not pinned or differs from its pin")
    if tier == 3 and not (TEST_RESERVED and machine_id() == "m3"):
        raise SystemExit("REFUSED: tier 3 scores on m3 only, after the r9 reservation")
    gold = json.loads(gold_path.read_text(encoding="utf-8"))
    name = {1: "D1", 2: "D2", 3: "test"}[tier]
    ids = load_set(name) if tier < 3 else a_t1.order(list(gold["L"]))
    if gold["set"] != name or sorted(gold["L"]) != sorted(ids):
        raise SystemExit(f"gold is for {gold['set']}, not tier {tier} ({name})")
    drop, excl_sha = excluded_ids(excl, tier)
    ids = [i for i in ids if i not in drop]
    x4_in, t1_sha, t1_models = (False, None, None) if tier == 1 else tier1_binding(t1)
    models = score_models(registry(), raw, tier, t1_models)
    caps = {}
    for m in models:
        for q in p50.MODES:
            f = raw / f"{run_id(m, q, tier)}.preds.json"
            side = f.with_suffix(".json.sha256")
            if not side.exists() or side.read_text().split()[0] != p50.sha_file(f):
                raise SystemExit(f"{f.name}: sidecar sha256 missing or different")
            caps[run_id(m, q, tier)] = {str(k): v for k, v in g.read_captions(f).items()}
    a = analysis(g, ids, gold, caps, models, tier)
    idx, ment, G1, L, Rall = (a.pop(k) for k in ("_idx", "_ment", "_G1", "_L", "_Rall"))
    p, v = {}, ("SCORED", "")
    if tier == 1:
        p = {"AD1p": a_t1.predict(a["AD1p"]["_draws"], a["n_images"], N_TEST_PLAN),
             "X5": a_t1.predict_null(a["X5"], a["n_images"], N_TEST_PLAN),
             "X4": a_t1.predict_null(a["X4"], a["n_images"], N_TEST_PLAN)}
        x4_in = a["X4"]["verdict"] == "PASS" and p["X4"] >= P_GO  # r5 promotion, binding on tiers 2-3
        v = outcome1(a, p)
    elif tier == 2:
        p = {"AD1p": a_t1.predict(a["AD1p"]["_draws"], a["n_images"], N_TEST_PLAN),
             "X5": predict_null_boot(g, ment, G1, L, idx, N_TEST_PLAN)}
        v = outcome2(a, p)
    for k in ("AD1p", "L_vs_R5"):
        a[k].pop("_draws")
    for k in ("R2-R1", "R5-R2"):
        a["O2"][k].pop("_draws")
    a["family"] = family(a, x4_in)
    out.parent.mkdir(parents=True, exist_ok=True)
    out.write_text(json.dumps({"label": f"A-T3 TIER {tier} ({'dev, not a test result' if tier < 3 else 'one look'})",
                               "prereg": {"path": os.path.relpath(PREREG, ROOT), "sha256": PREREG_SHA256},
                               "outcome": v[0], "reason": v[1], "models": models, "analysis": a,
                               "predicted_p_pass": p, "n_test_plan": N_TEST_PLAN,
                               "provenance": {"script_sha256": p50.sha_file(Path(__file__)),
                                              "gold_sha256": p50.sha_file(gold_path), "tier1_sha256": t1_sha,
                                              "exclude_sha256": excl_sha, "n_excluded_w2": len(drop)}},
                              indent=1, default=float) + "\n", encoding="utf-8")
    print(f"A-T3 tier {tier} {v[0]} ({v[1]}): AD1' {a['AD1p']['point']:+.2f} {a['AD1p']['ci95']}, "
          f"X5 p {a['X5']['p_one_sided']:.3f}, P {p}")


# ------------------------------------------------------------------------------------------------ selftest
def selftest() -> None:
    import tempfile

    import score_g2b as g

    en = g.MATCH["coco80"]["en"]
    # lists: exclusion, val2017 refusal, sha order, sizes
    rv, v17 = set(range(1, 3000)), set(range(1, 400))
    o, c = split_pool(rv, v17, {"chair500": {400, 401}, "pope500": {402}})
    assert c["pool"] == len(o) == 2600 - 3 and "400" not in o and "1" not in o and o == a_t1.order(o), c
    assert c["restval_in_val2017"] == 399 and c["minus_chair500"] == 2
    # gold: val2017 refused, class names only
    K = {7: {"sentences": [{"raw": "a dog on a couch"}, {"raw": "a cat"}]}, 3: {"sentences": [{"raw": "x"}]}}
    gs = gold_sets(["7"], K, {7: {"dog", "couch", "tv"}}, en, {3})
    assert gs["refs"]["7"] == [["couch", "dog"], ["cat"]] and gs["L"]["7"] == ["couch", "dog", "tv"]
    for bad in (lambda: gold_sets(["3"], K, {3: set()}, en, {3}), lambda: gold_sets(["9"], K, {}, en, set())):
        try:
            bad()
            raise AssertionError("val2017 or missing id accepted")
        except SystemExit:
            pass
    # premise: R1 = one drawn reference; images with < k references take all
    pr = premise([{"a", "b", "c", "d"}, {"a", "b"}], [[{"a"}, {"a"}, {"a"}, {"a"}, {"a"}], [{"z"}]])
    assert pr["sum_L"] == 6 and pr["sum_R"]["1"] == 2 and pr["L_over_R1"] == 3 and pr["gate_R1"], pr
    assert not premise([{"a"}], [[{"a"}]])["gate_R1"]
    # registry: copied blocks equal their sources; pins/families as CC-183 W10
    R = build_registry()
    assert R["order"] == list(MODELS) and all(R["models"][m]["revision"].startswith(MODELS[m][1]) for m in MODELS)
    assert R["models"]["internvl3_8b"] == source("a_n2")["models"]["internvl3_8b"]
    assert R["models"]["aya_vision_8b"] == source("c_t1")["models"]["aya_vision_8b"]
    assert R["families"]["aya_vision_8b"]["host_role"] == "m3" and R["families"]["llava_ov_7b"]["lm_family"].startswith("qwen")
    import decode_hf_vlm as dec  # register() through the decoder's own reader (p50.register_check pattern)

    with tempfile.TemporaryDirectory() as t:
        root = Path(t) / "a_t3"
        (root / "sets").mkdir(parents=True)
        (root / "sets/a_t3_D1.tsv").write_text("".join(f"{i}\t{int(i):012d}.jpg\t{'0' * 64}\n" for i in load_set("D1")))
        ms = [m for m in in_models(registry()) if MODELS[m][4] == "m4"]
        reg = register(root, "D1", ms)
        assert all(reg["models"][m] == R["models"][m] for m in ms) and len(reg["runs"]) == 2 * len(ms)
        (Path(t) / "reg.json").write_text(json.dumps(reg))
        dec.load_prereg(Path(t) / "reg.json")
        assert len(dec.manifest_items(reg, "a_t3_D1")) == N_D1 and reg["decoder"]["sha256"] == p50.DECODER_SHA
        try:
            register(root, "D1", ["gemma3_4b"] if not R["families"]["gemma3_4b"]["pins_complete"] else ["nope"])
            raise AssertionError("a model outside the A-T3 set was registered")
        except (SystemExit, KeyError):
            pass
        t1 = Path(t) / "t1.json"
        t1.write_text(json.dumps({"label": "A-T3 TIER 1 (dev)", "outcome": "PROCEED_TO_TIER2", "models": ms,
                                  "analysis": {"family": {"x4_in_family": True}}}))
        assert tier1_binding(t1)[0] is True
        def t1w(o):
            t1.write_text(json.dumps({"label": "A-T3 TIER 1 (dev)", "outcome": o, "models": ms,
                                      "analysis": {"family": {"x4_in_family": False}}}))
        t1w("X4_NOT_EVALUABLE")
        assert tier1_binding(t1, "PI-1031x")[2] == ms
        try:
            tier1_binding(t1, "")
            raise AssertionError("X4_NOT_EVALUABLE passed without the PI constant")
        except SystemExit:
            pass
        t1w("PASS_LOW_POWER")
        try:
            tier1_binding(t1, "PI-1031x")
            raise AssertionError("PASS_LOW_POWER passed")
        except SystemExit:
            pass
        t1w("NOT_REPRODUCED")
        # F9 model-set lock and F2 date stops
        raw = Path(t) / "raw"
        raw.mkdir()
        for m in ms:
            for q in p50.MODES:
                (raw / f"{run_id(m, q)}.preds.json").write_text("{}")
        for bad_m in (lambda: score_models(registry(), raw, 1, None, ""), lambda: score_models(registry(), raw, 1, ms[:2], "x")):
            try:
                bad_m()
                raise AssertionError("model-set lock bypassed")
            except SystemExit:
                pass
        assert score_models(registry(), raw, 1, None, "LOG-x") == ms and score_models(registry(), raw, 1, ms) == ms
        date_ok(2, "2026-11-04T23:59:59Z")
        for tt, now in ((2, "2026-11-05T00:00:00Z"), (3, "2026-11-08T00:00:00Z")):
            try:
                date_ok(tt, now)
                raise AssertionError("date stop not enforced")
            except SystemExit:
                pass
        assert reg_tier(Path(t) / "reg.json") == 1
        # job config (OPS-1030at3p): tier-1 registration and outputs refused; tier-2 dir, ledger and caps separate
        r2 = Path(t) / "reg_t2.json"
        r2.write_text(json.dumps({**reg, "runs": [{**r, "run_id": run_id(r["model"], r["prompt_mode"], 2)}
                                                 for r in reg["runs"]]}))
        assert reg_tier(r2) == 2 and job_cfg(2, "m4", r2) == ("/root/outputs/a_t3_t2", 6.0)
        assert job_cfg(2, "m3", r2) == ("/root/outputs/a_t3_t2", 2.0)
        mixed = Path(t) / "reg_mixed.json"
        mixed.write_text(json.dumps({**reg, "runs": json.loads(r2.read_text())["runs"][:1] + reg["runs"]}))
        for tt, rp in ((1, Path(t) / "reg.json"), (2, Path(t) / "reg.json"), (3, r2), (1, r2), (2, mixed)):
            try:
                job_cfg(tt, "m4", rp)
                raise AssertionError(f"job tier {tt} accepted {rp.name}")
            except SystemExit:
                pass
        r3 = Path(t) / "reg_t3.json"
        r3.write_text(json.dumps({**reg, "runs": [{**r, "run_id": run_id(r["model"], r["prompt_mode"], 3)}
                                                 for r in reg["runs"]]}))
        assert job_cfg(3, "m3", r3) == ("/root/outputs/a_t3_t3", 19.69)
        for tt, h, rp in ((3, "m4", r3), (2, "m3", r3), (3, "m3", mixed)):
            try:
                job_cfg(tt, h, rp)
                raise AssertionError(f"job tier {tt} on {h} accepted {rp.name}")
            except SystemExit:
                pass
        # CC-203 W5: spent 5.34 (tier 1) + 1.45 + 3.92 (tier 2 BLOCK DONE) = 10.71, plus the tier-3 cap, within 40
        assert 5.34 + 1.45 + 3.92 + CAP_H["tier3_m3"] <= CAP_GPU_H
        # t3gate (CC-203 W3/W6): the committed files pass every sha check; refused off m3, after the stop, on a copy
        tl, m3f = PDIR / "r9/a_t3_testlist_r9_drop_all.json", Path(t) / "m3"
        m3f.write_text("m3\n")
        assert t3gate(tl, None, m3f, "2026-11-06T23:59:59Z").startswith("t3gate ok")
        bad_l = Path(t) / "l.json"
        bad_l.write_text(tl.read_text() + " ")
        gf = Path(t) / "g.json"
        gf.write_text(json.dumps({"set": "test", "premise": {"gate_R1": True}, "provenance": {
            "ids_sha256": T3_IDS_SHA[::-1], "member": TEST_MEMBER, "pins": PIN}}))
        for args in ((tl, None, Path(t) / "mid_none", None), (tl, None, m3f, "2026-11-07T00:00:00Z"),
                     (bad_l, None, m3f, "2026-11-01T00:00:00Z"), (tl, gf, m3f, "2026-11-01T00:00:00Z")):
            try:
                t3gate(*args)
                raise AssertionError(f"t3gate passed {args}")
            except SystemExit:
                pass
        for bad in (lambda: tier1_binding(t1), lambda: tier1_binding(None), lambda: excluded_ids(None, 1)):
            try:
                bad()
                raise AssertionError("tier 2 without a usable tier-1 result")
            except SystemExit:
                pass
    # analysis on synthetic captions: L more complete than one reference; references = salient subset of L
    rng = np.random.default_rng(0)
    pool, n = sorted(set(en("person dog cat car bus chair couch tv bottle cup bowl pizza clock vase book bench"))), 300
    ids = [str(k) for k in range(n)]
    lab = {i: sorted(rng.choice(pool, 8, replace=False)) for i in ids}
    gold = {"L": lab, "refs": {i: [[lab[i][0]], [lab[i][0], lab[i][1]], [lab[i][1]], [lab[i][0]], [lab[i][2]]]
                               for i in ids}}
    caps, models = {}, list(MODELS)[:3]
    for mi, m in enumerate(models):
        for q, k in (("short_en", 2), ("detailed_en", 4 + 2 * mi)):
            caps[run_id(m, q)] = {i: "a photo with " + ", ".join(f"a {x}" for x in lab[i][:k] + list(rng.choice(pool, 1)))
                                  for i in ids}
    a = analysis(g, ids, gold, caps, models, n_boot=200, n_rep=100)
    assert a["AD1p"]["verdict"] == "PASS" and a["X5"]["verdict"] == "PASS", (a["AD1p"]["point"], a["X5"])
    assert a["L_vs_R5"]["verdict"] == "PREMISE_NOT_MET" and a["premise"]["gate_R1"]
    p = {"AD1p": a_t1.predict(a["AD1p"]["_draws"], n, N_TEST_PLAN), "X5": a_t1.predict_null(a["X5"], n, N_TEST_PLAN)}
    assert outcome1(a, p)[0] in ("PROCEED_TO_TIER2", "X4_NOT_EVALUABLE"), outcome1(a, p)
    assert outcome1(a, {"AD1p": 0.5, "X5": 1})[0] == "PASS_LOW_POWER"
    assert outcome2(a, {"AD1p": 0.97, "X5": 1})[0] == "REHEARSAL_FAIL"
    b = json.loads(json.dumps({k: v for k, v in a.items() if not k.startswith("_")}, default=lambda x: None))
    b["X4"]["verdict"] = "NOT_EVALUABLE"
    assert outcome1(b, {"AD1p": 1, "X5": 1})[0] == "X4_NOT_EVALUABLE"
    b["X5"]["verdict"] = "INCONCLUSIVE"
    assert outcome1(b, {"AD1p": 1, "X5": 1})[0] == "NOT_REPRODUCED"
    b["premise"]["gate_R1"] = False
    assert outcome1(b, {"AD1p": 1, "X5": 1})[0] == "PREMISE_NOT_MET"
    f = family(a, False)
    assert f["joint"] == "PASS" and set(f["holm_p"]) == {"AD1p", "X5"} and "X4" in family(a, True)["holm_p"]
    pb = predict_null_boot(g, a["_ment"], a["_G1"], a["_L"], a["_idx"], N_TEST_PLAN, B=3, R=20)
    assert 0 <= pb <= 1
    # testlist: counts beside 5,000, not reserved
    with tempfile.TemporaryDirectory() as t:
        st, tl = test_steps(set(range(1, 30)), set(range(10, 5010)), {"pope500": {11}}, {"flickr": {12, 129062}})
        assert [x[1] for x in st] == [5000, 20, 19, 19, 18] and "11" not in tl and len(tl) == 18, st
        # guard pieces: names and ids, fail-closed sha list, cap
        (Path(t) / "a_t3/images").mkdir(parents=True)
        (Path(t) / "a_t3/images/000000000009.jpg").write_bytes(b"x")
        assert bad_names(Path(t), {8}) == []
        (Path(t) / "a_t3/images/000000000008.jpg").write_bytes(b"x")
        (Path(t) / "instances_val2017.json").write_text("{}")
        assert len(bad_names(Path(t), {8})) == 2
        try:
            valsha_set(None)
            raise AssertionError("missing val2017 sha list accepted")
        except SystemExit as e:
            assert "not pinned" in str(e)
        L_ = Path(t) / "l.tsv"
        L_.write_text("a\t3600.0\t0\n")
        assert left(L_, 6.0) == 5 * 3600
        mid = Path(t) / "mid"
        mid.write_text("m9\n")
        try:
            guard("0" * 40, Path(t) / "v", None, mid)
            raise AssertionError("unknown machine accepted")
        except SystemExit as e:
            assert "machine id" in str(e)
        # stage refuses a failed premise and never fetches from val2017
        gp = Path(t) / "g.json"
        gp.write_text(json.dumps({"set": "D1", "premise": {"gate_R1": False}}))
        try:
            cmd_stage(gp, "D1", Path(t), Path(t) / "v", None)
            raise AssertionError("failed premise staged")
        except SystemExit as e:
            assert "PREMISE_NOT_MET" in str(e)
    assert "train2017" in coco_url("9") and "val" not in coco_url("9")
    try:
        instances(Path(__file__), TEST_MEMBER, en)
        raise AssertionError("val2017 member read off m3")
    except SystemExit:
        pass
    text = (HERE / "a_t3_job.sh").read_text(encoding="utf-8")
    assert "set -euo pipefail" in text and "$X guard" in text and "aya_vision_8b" in text
    assert "R=at3t${T}_$M-$Q" in text and "$X jobcfg" in text and "at3t1_" not in text
    assert "O=/root/outputs/a_t3" not in text and "/root/outputs/a_t3/" not in text and '[ "$T" = 2 ]' in text
    t3 = (HERE / "a_t3_t3_job.sh").read_text(encoding="utf-8")
    assert t3.count("$X t3gate") == 1 and t3.count("T3G") >= 5 and "--tier 3" in t3 and "at3t3_" in t3
    print("a_t3 selftest ok")


def main() -> None:
    ap = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    ap.add_argument("--selftest", action="store_true")
    sub = ap.add_subparsers(dest="cmd")
    s = sub.add_parser("registry"); s.add_argument("--out", type=Path); s.add_argument("--check", action="store_true")  # noqa: E702
    s = sub.add_parser("lists"); s.add_argument("--karpathy", type=Path, required=True); s.add_argument("--val2017-ids", type=Path, required=True)  # noqa: E702
    s = sub.add_parser("gold"); s.add_argument("--karpathy", type=Path, required=True); s.add_argument("--ann", type=Path, required=True)  # noqa: E702
    s.add_argument("--val2017-ids", type=Path, required=True); s.add_argument("--set", required=True, choices=["pool", "D1", "D2", "test"])  # noqa: E702
    s.add_argument("--out", type=Path, required=True); s.add_argument("--test-list", type=Path)  # noqa: E702
    s = sub.add_parser("stage"); s.add_argument("--gold", type=Path, required=True); s.add_argument("--set", required=True, choices=["D1", "D2"])  # noqa: E702
    s.add_argument("--root", type=Path, required=True); s.add_argument("--val2017-ids", type=Path, required=True)  # noqa: E702
    s.add_argument("--valsha", type=Path, required=True)
    s = sub.add_parser("register"); s.add_argument("--root", type=Path, required=True); s.add_argument("--set", required=True)  # noqa: E702
    s.add_argument("--models", nargs="+", required=True); s.add_argument("--tier", type=int, default=1)  # noqa: E702
    s.add_argument("--out", type=Path, required=True)
    s = sub.add_parser("guard"); s.add_argument("--head", required=True); s.add_argument("--val2017-ids", type=Path, required=True)  # noqa: E702
    s.add_argument("--valsha", type=Path, required=True)
    s = sub.add_parser("left"); s.add_argument("--ledger", type=Path, required=True); s.add_argument("--cap-h", type=float, required=True)  # noqa: E702
    s = sub.add_parser("models"); s.add_argument("--host", required=True, choices=["m3", "m4"])  # noqa: E702
    s.add_argument("--tier", type=int, default=1)
    s = sub.add_parser("t3gate"); s.add_argument("--test-list", type=Path, required=True); s.add_argument("--gold", type=Path)  # noqa: E702
    s = sub.add_parser("stage3"); s.add_argument("--test-list", type=Path, required=True); s.add_argument("--gold", type=Path, required=True)  # noqa: E702
    s.add_argument("--src", type=Path, required=True); s.add_argument("--root", type=Path, required=True)  # noqa: E702
    s.add_argument("--valsha", type=Path, required=True)
    s = sub.add_parser("jobcfg"); s.add_argument("--tier", type=int, required=True); s.add_argument("--reg", type=Path, required=True)  # noqa: E702
    s.add_argument("--host", required=True, choices=["m3", "m4"])
    s = sub.add_parser("valsha"); s.add_argument("--dir", type=Path, required=True); s.add_argument("--out", type=Path, required=True)  # noqa: E702
    s.add_argument("--val2017-ids", type=Path, required=True)
    sub.add_parser("datecheck").add_argument("--reg", type=Path, required=True)
    s = sub.add_parser("neardup"); s.add_argument("--cand-dir", type=Path, required=True); s.add_argument("--ref", nargs="+", required=True)  # noqa: E702
    s.add_argument("--sscd", type=Path, required=True); s.add_argument("--out", type=Path, required=True)  # noqa: E702
    s = sub.add_parser("testlist"); s.add_argument("--karpathy", type=Path, required=True); s.add_argument("--val2017-ids", type=Path, required=True)  # noqa: E702
    s.add_argument("--drop", nargs="*", default=[]); s.add_argument("--out", type=Path, required=True)  # noqa: E702
    s = sub.add_parser("score"); s.add_argument("--tier", type=int, required=True, choices=[1, 2, 3])  # noqa: E702
    s.add_argument("--raw", type=Path, required=True); s.add_argument("--gold", type=Path, required=True)  # noqa: E702
    s.add_argument("--tier1", type=Path); s.add_argument("--exclude", type=Path)  # noqa: E702
    a = ap.parse_args()
    pairs = lambda xs: {x.split("=", 1)[0]: Path(x.split("=", 1)[1]) for x in xs}  # noqa: E731
    if a.selftest:
        return selftest()
    if a.cmd == "registry":
        if a.check:
            registry()
            print("registry ok:", in_models(json.loads(REGISTRY.read_text())))
        else:
            p50.dump(build_registry(), a.out)
    elif a.cmd == "lists":
        if LISTS.exists():
            raise SystemExit(f"{LISTS} exists")
        LISTS.write_text(json.dumps(cmd_lists(a.karpathy, a.val2017_ids), indent=1) + "\n", encoding="utf-8")
        print(f"{p50.sha_file(LISTS)}  {LISTS.name}")
    elif a.cmd == "gold":
        p50.dump(cmd_gold(a.karpathy, a.ann, a.set, a.val2017_ids, a.test_list), a.out)
    elif a.cmd == "stage":
        print(json.dumps(cmd_stage(a.gold, a.set, a.root, a.val2017_ids, a.valsha)))
    elif a.cmd == "register":
        p50.dump(register(a.root, a.set, a.models, a.tier), a.out)
    elif a.cmd == "guard":
        guard(a.head, a.val2017_ids, a.valsha)
    elif a.cmd == "left":
        print(left(a.ledger, a.cap_h))
    elif a.cmd == "models":
        R = registry()
        print(" ".join(m for m in in_models(R) if R["families"][m]["host_role"] == a.host
                       or (a.tier == 3 and a.host == "m3")))  # CC-203 W4: the tier-3 m3 list = all in-set models
    elif a.cmd == "t3gate":
        print(t3gate(a.test_list, a.gold))
    elif a.cmd == "stage3":
        print(json.dumps(cmd_stage3(a.test_list, a.gold, a.src, a.root, a.valsha)))
    elif a.cmd == "jobcfg":
        print(*job_cfg(a.tier, a.host, a.reg))
    elif a.cmd == "valsha":
        p50.dump(cmd_valsha(a.dir, a.val2017_ids), a.out)
    elif a.cmd == "datecheck":
        date_ok(reg_tier(a.reg))
    elif a.cmd == "neardup":
        p50.dump(cmd_neardup(a.cand_dir, pairs(a.ref), a.sscd), a.out)
    elif a.cmd == "testlist":
        if not TEST_RESERVED and ROOT in a.out.resolve().parents:
            raise SystemExit("REFUSED: an unreserved test list is never written into the repo (CC-183 r9)")
        p50.dump(cmd_testlist(a.karpathy, a.val2017_ids, pairs(a.drop)), a.out)
    elif a.cmd == "score":
        cmd_score(a.tier, a.raw, a.gold, a.tier1, a.exclude)
    else:
        ap.error("a subcommand or --selftest is required")


if __name__ == "__main__":
    main()
