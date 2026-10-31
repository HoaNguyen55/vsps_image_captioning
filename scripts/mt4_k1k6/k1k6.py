#!/usr/bin/env python3
"""MT4 Branch K1+K6 dev rule (manuscript/prereg/2026-10-30_mt4_k1k6/PREREG_DRAFT.md; CC-174 W3, PI-1029n).
Tier 1 (dev-explore, UIT-ViIC val 924) fixes PREREG §5 (a)-(d); tier 2 (dev-confirm, T2-2000, never used for
selection) rehearses H-B1/H-B2 with the registered analysis and a simulated P(PASS on KV-4,224) >= 0.98; tier 3 is the
one KV look, on the m3 role (M1) only, only after an anchored tier-2 PASS.

    python3 k1k6.py --selftest                                      CPU, synthetic rows (laptop or M1)
    python3 k1k6.py lists                                           laptop CPU, ids only: T2-2000 list + counts
    python3 k1k6.py power --base P --sys S [--n2 N ...]             laptop CPU: planning P(PASS) on existing dev preds
    python3 k1k6.py nogo                                            CPU: the RULE l.296 sentence from the anchored file
    python3 k1k6.py gold --ann DIR --set t2|kv                      CPU: {t2,kv}_gold.json from instances_val2014 (pinned)
    python3 k1k6.py stage --set t2|kv --ann DIR --out TSV           M1: COCO val2014 bytes of T2 (tier 2) / KV (tier 3)
    python3 k1k6.py pool --data DIR --out TSV                       CPU: K1 pool manifest (ids, files, shas, ref counts)
    python3 k1k6.py w25k1 feats|decide ...                          laptop CPU: W25 pass of the K1 pools (§4)
    python3 k1k6.py guard HEAD --tier 1|2|3                         M1: host, C-EN isolation, allow-listed image scan
    python3 k1k6.py plan [--rates R.json] --out CAPS.json           CPU: projections, caps, ladder, test line 100
    python3 k1k6.py left --ledger L --stage S --caps CAPS.json      CPU: timeout s = min(stage cap, line left)
    $VQ     k1k6.py train --model 8b|4b --seed S --epochs E --pool TSV --out-dir O [--save-epochs]   GPU
    $VQ     k1k6.py decode --model 8b|4b --mode short|detailed [--adapter D] --manifest TSV --images DIR --out F  GPU
    python3 k1k6.py t1select --dir O                                CPU: tier-1 rules (a), (c), (d) -> t1_select.json
    python3 k1k6.py t2decide --dir O                                CPU, one look: tier-2 verdict -> t2_decide.json
    python3 k1k6.py kvready --dir O                                 CPU: exit 0 only if the KV look is licensed
    python3 k1k6.py kvsums --pred F --system NAME                   CPU: one fsynced KV_PRED_SUMS line
    python3 k1k6.py kvscore --dir O                                 CPU, one look: mt4_k1k6_decide.json

Caption text (references, predictions) is read only by code; every printed line and record is numbers and shas.
"""
from __future__ import annotations

import argparse
import hashlib
import json
import math
import os
import re
import sys
import time
from pathlib import Path

import numpy as np

HERE = Path(__file__).resolve().parent
sys.path[:0] = [str(HERE.parent / "grl"), str(HERE.parent / "w22_sft"), str(HERE.parent / "lb"),
                str(HERE.parent / "k2_gate1"), str(HERE.parent / "w25"), str(HERE.parent)]
import common as K  # noqa: E402
import k2_gate0 as KG  # noqa: E402

ROOT = K.ROOT
PDIR = ROOT / "manuscript/prereg/2026-10-30_mt4_k1k6"
T2_IDS = PDIR / "t2_ids.txt"
GATES = PDIR / "GATES.json"
T2_ANCHOR = PDIR / "t2_decide.sha256"
KV_SUMS = PDIR / "KV_PRED_SUMS"
GATE1_DECIDE_ANCHOR = "manuscript/prereg/2026-10-28_k2_gate1/gate1_decide.sha256"
KV4224 = "manuscript/prereg/2026-10-28_mt4_kv/kv4224.txt"
KV4224_SHA = "86d9386324e8cb34c4c7216e494b21da0cbcfe458702952b9ce261a9f608f8f9"  # MT4 PREREG §1 (CC-153 W10)
#: the l1b.py guard pattern (CC-169 W3 lesson): a gate field holds a LOG line id, never a ruling id like CC-175
GATE_RE = re.compile(r"(OPS|CC|PI)-\d{4}[A-Za-z0-9-]*")
GATE_KEYS = ("W25K1", "COST", "T1", "AMEND2", "T2")  # AMEND2: MT4 PREREG AMENDMENT_2 (three-tier gate), tiers 2-3
T2_IDS_SHA = "298ae5e1aa327e99f09ca09e2f0694ebef03f73c082cf447e501cb8dc3c69ac1"  # re-carved CC-188 W1 (was 9f0e0c0b)

# ------------------------------------------------------------------------------------------------ fixed now (§2)
MODELS = {  # key -> (hub id, revision, snapshot dir on M1, LoRA trainable params at r16 on 7 projections x 36 layers)
    "8b": ("Qwen/Qwen3-VL-8B-Instruct", "0c351dd01ed87e9c1b53cbc748cba10e6187ff3b",
           "/root/ncs-data/models/Qwen3-VL-8B-Instruct-0c351dd", 36 * 1_212_416),
    "4b": ("Qwen/Qwen3-VL-4B-Instruct", "ebb281ec70b05090aa6165b016eac8ec08e71b17",
           "/root/ncs-data/models/Qwen3-VL-4B-Instruct-ebb281e", 36 * 917_504),  # 2560 hidden, 9728 MLP, 8 KV heads
}
SNAP_4B_LFS = {"model-00001-of-00002.safetensors": "30a01a0556622645a3cce87b655bbbbbc1f170c196099f1b666c93202c3339a9",
               "model-00002-of-00002.safetensors": "046296a2a387efb43b0c997d5833c789604d168834f6e0d3064bf7bb13d002a6"}
N_SHORT, N_SHORT_FALLBACK, N_DET, BATCH = 160, 256, 512, 4  # (a): evaluate.py default; one pre-written fallback
CAPHIT_MAX = 0.01  # (a): any tier-1 short decode with > 1% cap hits moves N_SHORT to 256 for tiers 2 and 3
LANG_MAX = 0.02  # (d): share of short captions failing k2_gate0.language_ok, per trained system
EPOCH_GRID, EPOCH_TIE = (1, 2, 3), 0.5  # (c): one 3-epoch seed-0 run, checkpoints at 1, 2, 3; ties -> fewer epochs
T1_SEED, K1_SEEDS, K6_SEEDS = 0, (1, 2), (1,)  # tier-1 adapters are never test systems (PILOT_RULE §6)
T2_N, T2_SALT = 2000, "mt4_k1k6_t2_2026-10-30"
N_KV = 4224
SESOI_F1, MARGIN_P, P_MIN = 2.0, -1.0, 0.98  # MT4 PREREG §5 H-B1; PI-1029n
B_BOOT, R_SIM, Z = 2000, 2000, 1.959963984540054
# planning rates (no K2 Gate 1 number; W2): W22-SFT C1 64-token rate, CANDIDATES §3 short rate, Gate 0 bf16 detailed
S_TR, CPU_ALLOW, S_SHORT, S_DET_BF16, NF4_PLAN, LOAD_H, CAP_FACTOR = 0.454, 1.25, 0.55, 3.25, 2.0, 0.1, 1.2
POOL_PLAN, VAL_N, PROBE_N, W25K1_H, KV_STAGE_H = 15249, 924, 40, 4.5, 2.0
TEST_LINE_H = 100.0  # MT4 PREREG §8 test line, unspent on this branch (§5 l.96)
D_K = 1803816000  # 2027-02-28T12:00:00Z: Branch K1+K6 freeze date (cost-only amendment, §5 l.96; CC-189 r4); KV lines after it are descriptive
SYSTEMS_T2 = {"short": ("base8_s", "k1_s1", "k1_s2", "k6_s1"), "detailed": ("base8_s", "k6_s1")}
SYSTEMS_KV = {"short": ("base8_s", "k1_s1", "k1_s2", "k6_s1"), "detailed": ("base8_s", "k6_s1")}  # H systems only
KV_DESC = "kv_detailed_k1_s1"  # descriptive K1 detailed row: no H, scheduled last from what is left (CC-175 W2)
HB1_NEEDS = ("short:base8_s",)  # plus every kept short:k1_s* (W1); H-B2 needs the three below
HB2_NEEDS = ("short:k6_s1", "detailed:k6_s1", "detailed:base8_s")
#: CC-205 W5: the scorer closure = every repo file the scorer loads (this file, the matcher modules, the lexicon data).
#: t2decide records it; kvscore FAULTs before reading any prediction or gold unless it equals the anchored record.
SCORER_CLOSURE = ("scripts/mt4_k1k6/k1k6.py", "scripts/grl/common.py", "scripts/grl/k2_gate0.py", "scripts/grl/reward.py",
                  "scripts/score_coco_probe.py", "scripts/clean_supervision.py", "scripts/rl_reward.py",
                  "scripts/person_uncap.py", "rescap/__init__.py", "rescap/chair.py", "rescap/metrics.py",
                  "rescap/repro.py", "rescap/svp/__init__.py", "rescap/svp/entailment.py", "rescap/svp/matching.py",
                  "rescap/vi/__init__.py", "rescap/vi/classifier.py", "rescap/vi/color.py", "rescap/vi/lexicon.py",
                  "rescap/vocab.py", "data/coco_probe/coco80_vi.json")


def sha(p: Path) -> str:
    return hashlib.sha256(Path(p).read_bytes()).hexdigest()


def utc(t: float | None = None) -> str:
    return time.strftime("%Y-%m-%dT%H:%M:%SZ", time.gmtime(time.time() if t is None else t))


def excl_write(path: Path, text: str) -> None:
    """One writer, one look: O_EXCL create, fsync. A second call fails before writing anything."""
    fd = os.open(path, os.O_WRONLY | os.O_CREAT | os.O_EXCL, 0o644)
    with os.fdopen(fd, "w") as f:
        f.write(text)
        f.flush()
        os.fsync(f.fileno())


# ------------------------------------------------------------------------------------------------ gates
def committed(rel: str) -> str | None:
    """The file's text at HEAD (git show), or None: gate files count only when committed (CC-175 W3); an untracked or
    modified copy on disk is refused by the callers that compare it."""
    import subprocess

    r = subprocess.run(["git", "-C", str(ROOT), "show", f"HEAD:{rel}"], capture_output=True, text=True)
    return r.stdout if r.returncode == 0 else None


def committed_file(p: Path) -> Path:
    """p, only if its bytes equal the HEAD copy (gold files, caps.json): else REFUSED."""
    t = committed(p.relative_to(ROOT).as_posix())
    if t is None or not p.is_file() or t.encode() != p.read_bytes():
        raise SystemExit(f"REFUSED: {p.name} is not committed at HEAD (or differs from it)")
    return p


def gates_missing(keys=GATE_KEYS, text: str | None = "HEAD") -> list[str]:
    if text == "HEAD":
        text = committed(GATES.relative_to(ROOT).as_posix())
    g = json.loads(text) if text else {}
    return [k for k in keys if not GATE_RE.fullmatch(str(g.get(k) or ""))]


# ------------------------------------------------------------------------------------------------ T2 split (tier 2)
#: training-side resource lists, not scored or selection sets: C-EN's English retrieval memory (COCO train + restval
#: minus refused; C retrieves their English captions as in-context examples, nothing is ever scored on them)
MEMORY_SIDE = ("manuscript/prereg/2026-10-27_c_en/cen_memory_allowed.tsv",)


def json_int_lists(o, out: set[int]) -> set[int]:
    """Every member of every JSON list whose items are all ints or digit strings (A-T3 D1/D2/smoke, W2 drops; CC-188 W1)."""
    if isinstance(o, dict):
        for v in o.values():
            json_int_lists(v, out)
    elif isinstance(o, list):
        if o and all((type(x) is int and x >= 0) or (isinstance(x, str) and x.isdigit()) for x in o):
            out.update(int(x) for x in o)
        else:
            for v in o:
                json_int_lists(v, out)
    return out


def prereg_int_ids(root: Path = ROOT / "manuscript/prereg") -> set[int]:
    """Every integer in the first column of every id list (.txt/.tsv), and every integer id list inside every .json,
    under manuscript/prereg, except this folder and MEMORY_SIDE: a conservative 'ever listed for a study' set (a
    non-COCO integer can only remove more candidates)."""
    out: set[int] = set()
    for p in sorted(root.rglob("*")):
        if p.suffix not in (".txt", ".tsv", ".json") or PDIR in p.parents or not p.is_file() or \
                p.as_posix().endswith(MEMORY_SIDE):
            continue
        if p.suffix == ".json":
            json_int_lists(json.loads(p.read_text(encoding="utf-8")), out)
            continue
        for line in p.read_text(encoding="utf-8", errors="ignore").splitlines():
            tok = line.split("\t")[0].strip()
            if tok.isdigit():
                out.add(int(tok))
    return out


def t2_sample(cands: set[int], n: int = T2_N, salt: str = T2_SALT) -> list[int]:
    """The n candidates with the smallest sha256(salt:id): seeded, order-free, reproducible from the id set alone."""
    if len(cands) < n:
        raise SystemExit(f"FAULT: {len(cands)} T2 candidates < {n}")
    key = lambda i: hashlib.sha256(f"{salt}:{i}".encode()).hexdigest()  # noqa: E731
    return sorted(sorted(cands, key=key)[:n])


def cmd_lists(_a) -> None:
    """Laptop, ids only (id_counts.py's inputs and pins): T2 = Karpathy restval minus exclusion.json, minus every
    UIT-ViIC id (train, val, test), minus A-touched ids, minus C-EN's kval/test lists, minus every id in a committed
    prereg list; then the T2_N smallest salted hashes. Restval is COCO val2014, the source of KV, and has no
    Vietnamese reference, so no group model was ever selected on it."""
    import id_counts as IC

    for rel, want in IC.INPUTS.items():
        if IC.sha_file(ROOT / rel) != want:
            raise SystemExit(f"{rel}: sha256 differs from its id_counts pin")
    load = lambda rel: json.loads((ROOT / rel).read_text(encoding="utf-8"))  # noqa: E731
    ex = load("manuscript/prereg/2026-10-21_dev_pools/exclusion.json")["ids"]["coco"]
    refused = set().union(*map(set, ex.values()))
    uv = set()
    for s in ("train", "val", "test"):
        uv |= {int(i["id"]) for i in load(f"data/datasets/uitviic/{s}_data.json")["images"]}
    rv = {int(i["cocoid"]) for i in load("data/datasets/karpathy/dataset_coco.json")["images"] if i["split"] == "restval"}
    gt = load(".session_backup/2026-10-14/r12_verify/gt_cache.json")
    touched = {int(k) for k in (*gt["refs"], *gt["inst"],
                                *load(".session_backup/2026-10-19/HL_human_labels/a_n3_instance_gold.json"))}
    listed = prereg_int_ids()
    cands = rv - refused - uv - touched - listed
    ids = t2_sample(cands)
    PDIR.mkdir(parents=True, exist_ok=True)
    T2_IDS.write_text("".join(f"{i}\n" for i in ids), encoding="utf-8")
    rec = {"schema": "vsps.mt4_k1k6.lists.v1", "script_sha256": sha(Path(__file__)),
           "counts": {"restval": len(rv), "minus_refused": len(rv - refused), "minus_uitviic_all": len(rv - refused - uv),
                      "minus_a_touched": len(rv - refused - uv - touched), "candidates": len(cands), "t2": len(ids)},
           "salt": T2_SALT, "t2_ids_sha256": sha(T2_IDS), "listed_ids_removed": len((rv - refused - uv - touched) & listed),
           "t2_in_cen_memory": len(set(ids) & {int(x.split("\t")[0]) for x in (ROOT / MEMORY_SIDE[0]).read_text()
                                                .splitlines() if x.split("\t")[0].isdigit()}),
           "note": "ids only; caption fields were parsed by the JSON loader and never used, printed or written"}
    (PDIR / "k1k6_lists.json").write_text(json.dumps(rec, indent=1) + "\n", encoding="utf-8")
    print(json.dumps(rec["counts"] | {"sha": rec["t2_ids_sha256"][:8]}))


def t2_ids() -> list[int]:
    if sha(T2_IDS) != T2_IDS_SHA:
        raise SystemExit("REFUSED: t2_ids.txt differs from its pin 298ae5e1")
    return [int(x) for x in T2_IDS.read_text().split()]


def set_ids(name: str) -> list[int]:
    """t2: T2-2000 (this folder); kv: KV-4,224 (MT4 PREREG §1 pin, checked)."""
    if name == "t2":
        return t2_ids()
    f = ROOT / KV4224
    if not f.is_file() or sha(f) != KV4224_SHA:
        raise SystemExit("REFUSED: kv4224.txt missing or not the PREREG §1 pin")
    return [int(x) for x in f.read_text().split()]


def cmd_gold(a) -> None:
    """{t2,kv}_gold.json with gold_instances.json's definition (reward.build_gold): COCO-2014 categories with >= 1
    instance, crowd included, from the pinned instances_val2014.json (T2 = restval and KV = Karpathy val: val2014).
    Counts only on stdout; the KV file is read by the scorer only (PREREG §1)."""
    pin = VAL2014_PIN
    f = Path(a.ann) / "instances_val2014.json"
    if sha(f) != pin:
        raise SystemExit("REFUSED: instances_val2014.json differs from its pin")
    want = set(set_ids(a.set))
    inst = json.loads(f.read_text())
    cat = {c["id"]: c["name"] for c in inst["categories"]}
    if {r["id"] for r in inst["images"]} & want != want:
        raise SystemExit("FAULT: an id is not in instances_val2014")
    gold: dict[int, set] = {i: set() for i in want}
    for x in inst["annotations"]:
        if x["image_id"] in want:
            gold[x["image_id"]].add(cat[x["category_id"]])
    out = PDIR / f"{a.set}_gold.json"
    out.write_text(json.dumps({"schema": "vsps.grl.gold.v1", "definition": "as gold_instances.json", "inputs_sha256":
                               {"instances_val2014.json": pin}, "n": len(gold),
                               "gold": {str(i): sorted(gold[i]) for i in sorted(gold)}}, ensure_ascii=False) + "\n")
    print(json.dumps({"n": len(gold), "sha256": sha(out)}))


VAL2014_PIN = "e1b4d1bc54906827b1a029981b1c77f2088bd4462569b7615db7929070c3ab47"
#: AMENDMENT_2 B4: positive pins of the staged bytes = C-EN's fetch records on M1 (AMENDMENT_W25K1 l.78, CC-190 W3):
#: T2 = memory (restval), KV = coco_kval (Karpathy val). Every KV body is a refused sha by design (common.refused_sets
#: holds coco_kval), so in tier 3 it passes only as its own record row, and the guard only under k1k6_kv.
CEN_RECORDS = {"t2": ("memory", "553fb604c21b54e37cd980297d78fe388d5751561b495d61f13f1fc52eb1e852"),
               "kv": ("coco_kval", "8c93f306f24588fb6e66eed0a8ba2ba97e61adf901ddf5ab614b37d5b677ee1c")}


def cen_record(name: str, rec: Path = K.CEN_REC) -> dict[int, str]:
    """{coco id: sha256} of a C-EN fetch record (id, file, sha256, bytes) at its pin, else REFUSED."""
    stem, pin = CEN_RECORDS[name]
    p = rec / f"{stem}.sha256.tsv"
    if not p.is_file() or sha(p) != pin:
        raise SystemExit(f"REFUSED: {p} missing or not its pin {pin[:8]}")
    return {int(r[0]): r[2] for r in (x.split("\t") for x in p.read_text().splitlines())}


def stage_check(name: str, i: int, h: str, bad_sha: set[str], rec: dict[int, str]) -> None:
    """A refused sha is a FAULT, except a KV body equal to its own Karpathy-val record row; then every body must equal
    its own record row (a missing row is a FAULT too). Called before any byte is written."""
    if h in bad_sha and not (name == "kv" and rec.get(i) == h):
        raise SystemExit(f"FAULT: {i} is a refused image by sha256; not written")
    if rec.get(i) != h:
        raise SystemExit(f"FAULT: {i} differs from its C-EN record row (AMENDMENT_2 B4); not written")


def cmd_stage(a, get=None, rec=None) -> None:
    """Stage T2 (tier 2) or KV-4,224 (tier 3, after kvready) from each image's own `coco_url` in the pinned
    instances_val2014.json (as common.stage does; no host is written in this code) into their own folder (k1k6_t2 /
    k1k6_kv), every body hashed in memory and checked by stage_check (refused shas; its own C-EN record row),
    written by tmp + rename; then the manifest TSV (id, file, sha256). Idempotent."""
    import concurrent.futures as cf

    get = get or K.fetch
    ids = set_ids(a.set)
    rec = rec or cen_record(a.set)
    f = Path(a.ann) / "instances_val2014.json"
    if sha(f) != VAL2014_PIN:
        raise SystemExit("REFUSED: instances_val2014.json differs from its pin")
    url = {r["id"]: r["coco_url"] for r in json.loads(f.read_text())["images"] if r["id"] in set(ids)}
    folder = K.NCS_DATA / "datasets" / f"k1k6_{a.set}" / "images"
    folder.mkdir(parents=True, exist_ok=True)
    _, bad_sha = K.refused_sets()

    def one(i):
        f = folder / f"COCO_val2014_{i:012d}.jpg"
        if f.exists():
            stage_check(a.set, i, h := K.sha_file(f), bad_sha, rec)
            return i, f.name, h
        b = get(url[i])
        h = hashlib.sha256(b).hexdigest()
        stage_check(a.set, i, h, bad_sha, rec)
        tmp = f.with_name("." + f.name)
        tmp.write_bytes(b)
        os.replace(tmp, f)
        return i, f.name, h
    with cf.ThreadPoolExecutor(16) as ex:
        rows = sorted(ex.map(one, ids))
    Path(a.out).write_text("".join(f"{i}\t{f}\t{h}\n" for i, f, h in rows))
    print(json.dumps({"set": a.set, "n": len(rows), "manifest_sha256": sha(Path(a.out))}))


# ------------------------------------------------------------------------------------------------ K1 pool (c)
#: CC-199 r1 (ii): the one truncated OpenViIC training file (1 byte, AMENDMENT_W25K1 §6-§7) is dropped from training.
#: Key-only (CC-200): the file sha is provenance and is never read from disk (M1 does not hold the file).
K1_TRUNC_DROP = {"openviic:00000007169": "4859dd1fc17d928fed15035b69c9964401cf327b33d4ca04b161b3d252fb9d20"}


def drop_trunc(rows: list[tuple[str, str, int]]) -> list[tuple[str, str, int]]:
    """CC-199/CC-200: FAULT unless every K1_TRUNC_DROP key is a pool row; return the rows without them."""
    keys = {r[0] for r in rows}
    for k in K1_TRUNC_DROP:
        if k not in keys:
            raise SystemExit(f"FAULT: {k} is not a pool row (CC-199)")
    return [r for r in rows if r[0] not in K1_TRUNC_DROP]


def pool_rows(data: Path, w25_ut: set[int], w25_k1: set[str]) -> list[tuple[str, str, int]]:
    """(key, image path relative to data, n refs). KTVIC train + UT-2,402 minus the K2 W25 ids + OpenViIC train, minus
    the W25-K1 exclusions (keys), minus K1_TRUNC_DROP (CC-199). One example per image per epoch; the reference cycles
    with the epoch (§2 (c))."""
    rows = []
    kt = json.loads((data / "ktvic/train_data.json").read_text(encoding="utf-8"))
    n = {}
    for x in kt["annotations"]:
        n[x["image_id"]] = n.get(x["image_id"], 0) + bool(x.get("caption"))
    rows += [(f"ktvic:{i['id']}", f"ktvic/images/{i['filename']}", n.get(i["id"], 0)) for i in kt["images"]]
    ut = set(K.ids("ut2402")) - w25_ut
    uv = json.loads((data / "uitviic/train_data.json").read_text(encoding="utf-8"))
    n = {}
    for x in uv["annotations"]:
        n[int(x["image_id"])] = n.get(int(x["image_id"]), 0) + bool(x.get("caption"))
    rows += [(f"uitviic:{i}", f"uitviic/images/{i:012d}.jpg", n.get(i, 0)) for i in sorted(ut)]
    ov = json.loads((data / "openviic/uit-openviic-annotation-train.json").read_text(encoding="utf-8"))
    rows += [(f"openviic:{Path(f).stem}", f"openviic/images/{f}", len(v["captions"])) for f, v in sorted(ov.items())]
    rows = [r for r in drop_trunc(rows) if r[0] not in w25_k1]
    if any(r[2] == 0 for r in rows):
        raise SystemExit("FAULT: a pool image has no reference")
    return rows


def refs_of(data: Path) -> dict[str, list[str]]:
    """{pool key: references in file order}. Read by the trainer only; never printed."""
    out: dict[str, list[str]] = {}
    kt = json.loads((data / "ktvic/train_data.json").read_text(encoding="utf-8"))
    for x in kt["annotations"]:
        if x.get("caption"):
            out.setdefault(f"ktvic:{x['image_id']}", []).append(x["caption"])
    uv = json.loads((data / "uitviic/train_data.json").read_text(encoding="utf-8"))
    for x in uv["annotations"]:
        if x.get("caption"):
            out.setdefault(f"uitviic:{int(x['image_id'])}", []).append(x["caption"])
    ov = json.loads((data / "openviic/uit-openviic-annotation-train.json").read_text(encoding="utf-8"))
    for f, v in ov.items():
        out[f"openviic:{Path(f).stem}"] = list(v["captions"])
    return out


def cmd_pool(a) -> None:
    data = Path(a.data)
    w25_ut = {int(x) for x in (ROOT / "manuscript/prereg/2026-10-28_k2_gate1/w25_excluded_ids.txt").read_text().split()}
    w25_k1 = set((PDIR / "w25k1_excluded_keys.txt").read_text().split())  # committed with the W25K1 gate
    rows = pool_rows(data, w25_ut, w25_k1)
    lines = [f"{k}\t{p}\t{sha(data / p)}\t{n}" for k, p, n in rows]
    Path(a.out).write_text("\n".join(lines) + "\n")
    by = {}
    for k, _, n in rows:
        by[k.split(":")[0]] = by.get(k.split(":")[0], 0) + 1
    print(json.dumps({"n": len(rows), "by_dataset": by, "dropped_truncated": len(K1_TRUNC_DROP),
                      "sha256": sha(Path(a.out))}))


def pool_manifest(p: Path) -> list[tuple[str, str, str, int]]:
    return [(k, f, h, int(n)) for k, f, h, n in (x.split("\t") for x in p.read_text().splitlines() if x)]


def example_plan(pool: list[tuple[str, str, str, int]], epochs: int, seed: int) -> list[tuple[str, int]]:
    """(key, reference index): one example per image per epoch in train.schedule order (seeded); the e-th time an
    image comes up it gets reference (e + seed) mod n_refs, so every reference is used across epochs."""
    from train import schedule

    nref = {k: n for k, _, _, n in pool}
    seen: dict[str, int] = {}
    out = []
    for k in schedule(sorted(nref), epochs * len(nref), seed):
        e = seen.get(k, 0)
        seen[k] = e + 1
        out.append((k, (e + seed) % nref[k]))
    return out


# ------------------------------------------------------------------------------------------------ W25-K1 (§4)
def w25k1_decide(pool: dict, sets: dict[str, dict], near, sha_lists: dict[str, set] | None = None
                 ) -> tuple[list[str], dict]:
    """W25 RULE §3 unchanged (C1 byte-identical OR C2 hashes<=10 AND SSCD>=0.5, OR C3 SSCD>0.75) of every K1 pool
    image against every featured set, plus C1 by sha against every exclusion.json image_sha256 list (XM3600 among
    them: byte identity only, CC-153 r4; J-3); union over sets."""
    import w25

    per = {s: w25.rule(pool, y, near) for s, y in sets.items()}
    for name, shas in (sha_lists or {}).items():  # C1 by sha only (XM3600: CC-153 r4, no XM byte is read)
        hit = np.array([h in shas for h in pool["sha"]], bool)
        per[f"sha:{name}"] = {"C1_sha_list": hit, "excluded": hit}
    ex = np.zeros(len(pool["ids"]), bool)
    for r in per.values():
        ex |= r["excluded"]
    keys = sorted(k for k, e in zip(pool["ids"], ex) if e)
    return keys, {"n_pool": len(pool["ids"]), "n_excluded": len(keys),
                  "counts": {s: {k: int(v.sum()) for k, v in r.items()} for s, r in per.items()},
                  "n_compared": {s: len(y["ids"]) for s, y in sets.items()}}


def cmd_w25k1(a) -> None:
    import w25

    if a.op == "feats":  # one set: ids = pool keys or image stems; images read where they already are (laptop)
        rows = [x.split("\t") for x in Path(a.list).read_text().splitlines() if x]
        paths = [Path(a.images) / r[1] for r in rows]
        f = w25.bm().features(paths, w25.ok_sscd(Path(a.sscd)), workers=a.workers)
        if f["unreadable"]:
            raise SystemExit(f"FAULT: {len(f['unreadable'])} image(s) cannot be hashed")
        w25.save(Path(a.out), [r[0] for r in rows], f, set=a.name, utc=utc())
        print(json.dumps({"set": a.name, "n": len(rows)}))
        return
    out = PDIR / "w25k1_decide.json"
    if out.exists():
        raise SystemExit("REFUSED: w25k1_decide.json exists (one look)")
    pool = w25.load(Path(a.pool))
    sets = {Path(p).stem: w25.load(Path(p)) for p in a.sets}
    ex = json.loads(K.pinned("manuscript/prereg/2026-10-21_dev_pools/exclusion.json").read_text())["image_sha256"]
    keys, rec = w25k1_decide(pool, sets, w25.bm().near, {k: set(v) for k, v in ex.items()})
    rec |= {"schema": "vsps.mt4_k1k6.w25k1.v1", "inputs_sha256": {Path(p).name: sha(Path(p)) for p in [a.pool, *a.sets]},
            "utc": utc(), "label": "W25-K1 leakage exclusion: training side only, keys and counts"}
    (PDIR / "w25k1_excluded_keys.txt").write_text("".join(f"{k}\n" for k in keys))
    excl_write(out, json.dumps(rec, indent=1) + "\n")
    print(json.dumps({k: rec[k] for k in ("n_pool", "n_excluded")}))


# ------------------------------------------------------------------------------------------------ guard (M1)
def scan_k1(roots, bad_ids: set[int], bad_sha: set[str], allow_sha: set[str], allow_root: Path,
            kv_ok: dict[int, str] | None = None, kv_root: Path | None = None, skip=("/root/vsps/.venv",)) -> int:
    """common.scan with two amendments (§6): a non-COCO file name (KTVIC, OpenViIC) passes only under allow_root and
    only if its sha256 is in the pool manifest; in tier 3 a KV-4,224 file passes only under kv_root and only if its
    sha256 is its own C-EN Karpathy-val record row (kv_ok, AMENDMENT_2 B4), although that sha is a refused one. Everything else is
    common.scan unchanged (refused COCO ids, exclusion.json and C-EN test-side shas)."""
    seen = 0
    for root in roots:
        for dirpath, dirs, files in os.walk(root):
            dirs[:] = [d for d in dirs if not os.path.join(dirpath, d).startswith(skip)]
            for f in files:
                if not K.IMG_RE.search(f):
                    continue
                p, m = Path(dirpath) / f, K.COCO_RE.search(f)
                h = K.sha_file(p)
                kv_here = bool(kv_root and kv_ok) and kv_root in p.parents and m is not None and kv_ok.get(int(m.group(1))) == h
                if h in bad_sha and not kv_here:
                    raise SystemExit(f"REFUSED: test image {p} (refused sha256)")
                if m is None:
                    if allow_root not in p.parents or h not in allow_sha:
                        raise SystemExit(f"REFUSED: unidentifiable image {p} (not a COCO name, not a pool image)")
                elif int(m.group(1)) in bad_ids and not kv_here:
                    raise SystemExit(f"REFUSED: test image {p} (refused COCO id)")
                seen += 1
    return seen


def cmd_guard(a) -> None:
    mid = K.host_ok(a.head)
    if mid != "m3":
        raise SystemExit("REFUSED: K1/K6 GPU steps run on the m3 role (M1) only (MT4 AMENDMENT_1 A5)")
    iso = K.m3_clear()
    if any(K.UV.rglob("test*")):
        raise SystemExit(f"REFUSED: a UIT-ViIC test file exists under {K.UV}")
    bad_ids, bad_sha = K.refused_sets()
    if a.tier == 1:
        bad_ids = bad_ids | set(t2_ids())  # T2 bytes may not exist while anything is selected (tier 1)
    allow = {r[2] for r in pool_manifest(Path(a.pool))}
    kv_ok = {}
    if a.tier == 3:
        f = K.ROOT / KV4224
        if not f.is_file() or sha(f) != KV4224_SHA:
            raise SystemExit("REFUSED: kv4224.txt missing or not the PREREG §1 pin")
        kv = cen_record("kv")  # a KV-4,224 file passes only under k1k6_kv and only as its own record row (B4)
        kv_ids = [int(x) for x in f.read_text().split()]
        if miss := [i for i in kv_ids if i not in kv]:  # CC-205 W8: a FAULT, never a KeyError
            raise SystemExit(f"FAULT: {len(miss)} kv4224 id(s) have no row in the C-EN Karpathy-val record")
        kv_ok = {i: kv[i] for i in kv_ids}
    n = scan_k1(K.SCAN_ROOTS, bad_ids, bad_sha, allow, K.NCS_DATA / "datasets/k1k6_pool", kv_ok,
                K.NCS_DATA / "datasets/k1k6_kv" if a.tier == 3 else None)
    print(json.dumps({"machine_id": mid, "tier": a.tier, "images_scanned": n, **iso}))


# ------------------------------------------------------------------------------------------------ cost (§8 amendment)
def cap(h: float) -> float:
    return math.ceil(round(10 * CAP_FACTOR * h, 6)) / 10


def plan(r: dict | None = None, epochs: int = max(EPOCH_GRID), n_pool: int = POOL_PLAN) -> dict:
    """Stage projections (GPU-h) and caps = ceil(1.2 x projection) to 0.1. r = measured rates from tier 1 (s/example
    train_8b, train_4b; s/img short, detailed) or None = planning rates. Ladder (PREREG §8 l.144): K6 is cut before
    K1's second seed; base8_s is never cut; if the H systems alone do not fit: NOT-RUN (cost)."""
    r = r or {}
    tr8 = r.get("train_8b", S_TR * CPU_ALLOW)
    tr4 = r.get("train_4b", tr8)  # 4B priced at the 8B rate until measured (conservative)
    sh = r.get("short", S_SHORT * NF4_PLAN)
    de = r.get("detailed", S_DET_BF16 * NF4_PLAN)
    p = {"t1_train": max(EPOCH_GRID) * n_pool * tr8 / 3600, "t1_timing": PROBE_N * de / 3600,
         **{f"t1_dec_{s}": VAL_N * sh / 3600 for s in ("base8_s", "e1", "e2", "e3")},
         "w25k1": W25K1_H - LOAD_H,  # CPU on the laptop: charged to the line by choice (§5 l.96), never a GPU step
         **{f"train_k1_s{s}": epochs * n_pool * tr8 / 3600 for s in K1_SEEDS},
         **{f"train_k6_s{s}": epochs * n_pool * tr4 / 3600 for s in K6_SEEDS},
         **{f"t2_{m}_{s}": T2_N * (sh if m == "short" else de) / 3600 for m, ss in SYSTEMS_T2.items() for s in ss},
         **{f"kv_{m}_{s}": N_KV * (sh if m == "short" else de) / 3600 for m, ss in SYSTEMS_KV.items() for s in ss},
         KV_DESC: N_KV * de / 3600,
         "kv_stage": KV_STAGE_H - LOAD_H}
    p = {k: round(v + LOAD_H, 4) for k, v in p.items()}
    caps = {k: cap(v) for k, v in p.items()}
    desc = caps.pop(KV_DESC)
    ladder, cut = [], dict(caps)

    def total():
        return round(sum(cut.values()), 1)
    for step, drop in (("cut K6", ("train_k6_s1", "t2_short_k6_s1", "t2_detailed_k6_s1", "kv_short_k6_s1",
                                   "kv_detailed_k6_s1")),
                       ("cut K1 seed 2", ("train_k1_s2", "t2_short_k1_s2", "kv_short_k1_s2"))):
        if total() <= TEST_LINE_H:
            break
        for k in drop:
            cut.pop(k, None)
        ladder.append(step)
    fits = total() <= TEST_LINE_H
    if fits and total() + desc <= TEST_LINE_H:  # never displaces an H stage; decoded last (job), else not run
        cut[KV_DESC] = desc
    return {"projection_h": p, "cap_h": cut, "descriptive_last": [KV_DESC], "projection_total_h": round(sum(p.values()), 2), "cap_total_h": total(),
            "test_line_h": TEST_LINE_H, "ladder_applied": ladder, "fits": fits, "freeze_D_K_utc": utc(D_K),
            "rates": {"train_8b": tr8, "train_4b": tr4, "short": sh, "detailed": de, "measured": bool(r)}}


def cmd_plan(a) -> None:
    r = json.loads(Path(a.rates).read_text()) if a.rates else None
    e = json.loads(Path(a.t1).read_text())["epochs"] if a.t1 else max(EPOCH_GRID)
    rec = plan(r, e)
    Path(a.out).write_text(json.dumps(rec, indent=1) + "\n")
    print(json.dumps({k: rec[k] for k in ("projection_total_h", "cap_total_h", "fits", "ladder_applied")}))
    sys.exit(0 if rec["fits"] else 2)


def cmd_left(a) -> None:
    """k2_gate1's ledger rules (open start charged at its full logged timeout, exit 6; fsynced lines) against the
    test line; a step whose timeout would end after D_K is HELD (exit 4)."""
    import k2_gate1 as G1

    led = Path(a.ledger)
    if (o := G1.open_start(led)) is not None:
        G1.ledger_append(led, f"{o[0]} {int(float(o[3]))}")
        print(f"FAULT: open start of {o[0]} closed at its full logged timeout")
        sys.exit(6)
    rec = json.loads(Path(a.caps).read_text())
    if "cut K1 seed 2" in rec.get("ladder_applied", []):  # CC-205 r3 (Codex 1): H-B1 not confirmatory -> branch stop
        print("NOT-RUN (cost): caps.json cuts K1 seed 2 (CC-205 r3); no confirmatory training", file=sys.stderr)
        print(0)  # the job's `[ "$t" -gt 0 ] || cost` closes the branch (K1K6_COST.txt) before the first stage runs
        sys.exit(0)
    c = rec["cap_h"]
    if a.stage not in c:
        print(f"CUT: {a.stage} is not in caps.json (ladder or descriptive remainder); skipped")
        sys.exit(5)
    t = max(0, int(min(round(c[a.stage] * 3600), TEST_LINE_H * 3600 - G1.used_seconds(led))))
    if time.time() + t > D_K:
        print(f"HELD: {a.stage} would end after D_K {utc(D_K)}")
        sys.exit(4)
    print(t)


# ------------------------------------------------------------------------------------------------ GPU: load, train, decode
def load(model: str, seed: int, snapshot: str | None = None):
    """w22_sft.load's pinned path (QLoRA NF4 double quant, bf16 compute, sdpa, r16 a32, dropout 0, language tower
    only), with the LoRA initialisation seeded by `seed` (the trainer change MT4 PREREG §4 asks for) and the
    trainable-parameter count asserted per backbone."""
    import torch
    from peft import LoraConfig, get_peft_model
    from transformers import AutoModelForImageTextToText, AutoProcessor, BitsAndBytesConfig

    import w22_sft as W

    snap = snapshot or MODELS[model][2]
    proc = AutoProcessor.from_pretrained(snap, **W.bn1_model()["processor_kwargs"])
    q = BitsAndBytesConfig(load_in_4bit=True, bnb_4bit_quant_type="nf4", bnb_4bit_use_double_quant=True,
                           bnb_4bit_compute_dtype=torch.bfloat16)
    net = AutoModelForImageTextToText.from_pretrained(snap, quantization_config=q, dtype=torch.bfloat16,
                                                      attn_implementation="sdpa", device_map={"": 0})
    net.config.use_cache = False
    torch.manual_seed(seed)
    net = get_peft_model(net, LoraConfig(task_type="CAUSAL_LM", **W.LORA))
    n = sum(p.numel() for p in net.parameters() if p.requires_grad)
    if n != MODELS[model][3]:
        raise SystemExit(f"FAULT: {n} trainable parameters, not {MODELS[model][3]}")
    net.train()
    return proc, net


def short_prompt() -> str:
    m = re.search(r'"short": \(\s*"([^"]+)"\s*"([^"]+)"', (ROOT / "scripts/evaluate.py").read_text(encoding="utf-8"))
    if not m:
        raise SystemExit("REFUSED: evaluate.py PROMPTS['short'] not found")
    return m.group(1) + m.group(2)


def cmd_train(a) -> None:
    """K2 Gate 1's trainer loop (encode, labels -100 over the prompt, AdamW lr 1e-4 wd 0, 8 micro-batches per step,
    constant lr, no clipping, last partial group steps) on the short prompt with one reference per image per epoch."""
    import torch
    from PIL import Image

    import k2_gate1 as G1
    import w22_sft as W

    out = Path(a.out_dir)
    if (out / "adapter_model.safetensors").exists():
        raise SystemExit(f"REFUSED: {out} already holds an adapter")
    data = Path(a.data)
    pool = pool_manifest(Path(a.pool))
    files = {k: (f, h) for k, f, h, _ in pool}
    refs = refs_of(data)
    order = example_plan(pool, a.epochs, a.seed)
    per_epoch = len(pool)
    text = short_prompt()
    dev = torch.device("cuda:0")
    torch.cuda.reset_peak_memory_stats()
    proc, net = load(a.model, a.seed)
    eot = proc.tokenizer.convert_tokens_to_ids("<|im_end|>")
    opt = torch.optim.AdamW([p for p in net.parameters() if p.requires_grad], lr=W.LR, weight_decay=0.0)
    t0 = time.time()
    for n, (k, j) in enumerate(order, 1):
        f, h = files[k]
        if K.sha_file(data / f) != h:
            raise SystemExit(f"FAULT: {f} differs from the pool manifest")
        with Image.open(data / f) as im:
            enc = G1.encode(proc, im.convert("RGB"), text)
        tgt = torch.tensor([proc.tokenizer(refs[k][j], add_special_tokens=False)["input_ids"] + [eot]])
        ids = torch.cat([enc["input_ids"], tgt], 1)
        batch = {kk: v.to(dev) for kk, v in enc.items() if kk not in ("input_ids", "attention_mask")}
        batch["pixel_values"] = batch["pixel_values"].to(torch.bfloat16)
        batch.update(input_ids=ids.to(dev), attention_mask=torch.ones_like(ids).to(dev),
                     labels=torch.cat([torch.full_like(enc["input_ids"], -100), tgt], 1).to(dev))
        loss = net(**batch, use_cache=False).loss
        if not torch.isfinite(loss):
            print(f"FAULT: non-finite loss at example {n}")
            sys.exit(3)
        (loss / W.ACCUM).backward()
        if n % W.ACCUM == 0 or n == len(order):
            opt.step()
            opt.zero_grad(set_to_none=True)
        if a.save_epochs and n % per_epoch == 0 and n < len(order):
            net.save_pretrained(out / f"epoch{n // per_epoch}")
        if n % 1000 == 0:
            print(f"{a.model} s{a.seed} {n}/{len(order)}", flush=True)
    net.save_pretrained(out / (f"epoch{a.epochs}" if a.save_epochs else ""))
    rec = {"model": a.model, "seed": a.seed, "epochs": a.epochs, "examples": len(order), "pool": per_epoch,
           "pool_sha256": sha(Path(a.pool)), "s_per_example": round((time.time() - t0) / len(order), 4),
           "peak_reserved_b": torch.cuda.max_memory_reserved()}
    (out / "train.json").write_text(json.dumps(rec, indent=1))
    print(json.dumps(rec))


def cmd_decode(a) -> None:
    """The K2 student path (W7) for K1/K6/base8_s: load() (NF4 + LoRA, not merged), the adapter's state loaded into
    it, eval, KV cache on, left padding; base8_s keeps the fresh zero LoRA (asserted). Greedy, batch 4, decode_hf_vlm
    generate / slices / writer."""
    import decode_hf_vlm as LB
    import torch
    from peft import set_peft_model_state_dict
    from safetensors.torch import load_file

    import k2_gate1 as G1
    import w22_sft as W

    out = Path(a.out)
    if out.exists():
        raise SystemExit(f"REFUSED: {out} exists")
    proc, net = load(a.model, 0)
    lb = [p for n, p in net.named_parameters() if "lora_B" in n]
    if a.adapter:
        sd = load_file(str(Path(a.adapter) / "adapter_model.safetensors"))
        res = set_peft_model_state_dict(net, sd)
        if res.unexpected_keys or not any(p.abs().max().item() != 0 for p in lb):
            raise SystemExit("FAULT: adapter keys unexpected or every lora_B is zero")
    elif any(p.abs().max().item() != 0 for p in lb):
        raise SystemExit("FAULT: the fresh LoRA of base8_s is not zero")
    proc.tokenizer.padding_side = "left"
    net.eval()
    net.config.use_cache = True
    net.generation_config.use_cache = True
    n_new = a.n_new
    prompt = short_prompt() if a.mode == "short" else W.prompt()
    man = Path(a.manifest)
    items = G1.rows_of(man)
    gen = LB.make_generate(proc, net, prompt, n_new, Path(a.images))
    part = Path(str(out) + ".partial.jsonl")
    kw = {"max_new_tokens": n_new, "do_sample": False, "num_beams": 1}
    key = LB.run_key(K.sha_file(man), {"model": a.model, "mode": a.mode}, {"adapter": a.adapter}, kw, prompt, items)
    t0 = time.time()
    rows = LB.decode_slices(items, BATCH, gen, part, key)
    s_img = (time.time() - t0) / len(items)
    prov = {k: None for k in LB.PROV_FIELDS} | {
        "schema": LB.SCHEMA, "prereg_id": "2026-10-30_mt4_k1k6", "decoder_sha256": K.sha_file(Path(__file__)),
        "run_id": out.name, "model": f"qwen3vl_{a.model}_nf4_peft", "hub_id": MODELS[a.model][0],
        "revision": MODELS[a.model][1], "dataset": man.name, "prompt_mode": a.mode, "max_new_tokens": n_new,
        "batch_size": BATCH, "dtype": "nf4/bf16", "manifest_sha256": K.sha_file(man), "n_images": len(items),
        "parity_slice0": {"n": 0, "identical": 0}, "resumed": False, "machine_id": os.environ.get("VSPS_MACHINE_ID"),
        "venv_freeze_sha256": os.environ.get("VSPS_VENV_FREEZE_SHA256"), "packages": LB.packages(),
        "adapter": a.adapter, "s_per_image_decode": round(s_img, 4), "gpu": torch.cuda.get_device_name(0),
        "adapter_sha256": K.sha_file(Path(a.adapter) / "adapter_model.safetensors") if a.adapter else None}
    LB.write_output(out, prov, rows)
    print(json.dumps({"run": out.name, "n": len(items), "s_per_image": round(s_img, 4)}))


# ------------------------------------------------------------------------------------------------ scoring (§3, §5)
def preds_of(p: Path) -> tuple[dict[str, str], dict[str, bool]]:
    d = json.loads(Path(p).read_text(encoding="utf-8"))
    pr = d["predictions"] if "predictions" in d else d
    hit = d.get("hit_max", {})
    return ({str(k): (v[0] if isinstance(v, list) else v) or "" for k, v in pr.items()},
            {str(k): bool(hit.get(k, False)) for k in pr})


def row_v1(c: str, g: set) -> dict:
    """k2_gate0.row's tp/hal/men/g with matcher v1 in place of v2 (same negation and hedge split). Descriptive only:
    MT4 PREREG §1 l.31 "v1 is reported beside it" (CC-175 N3, R2-2)."""
    said, hedged = KG.RW.unasserted(c)
    a = set(KG.RW.ordered(said, "v1")[0])
    u = set(KG.RW.ordered(hedged, "v1")[0]) - a
    return {"tp": len(a & g), "hal": len((a - g) | u), "men": len(a | u), "g": len(g)}


def short_counts(caps: dict[str, str], hit: dict[str, bool], gold: dict, ids: list[str], ver: str = "v2") -> np.ndarray:
    """Per image (tp, men, recall, has_gold, lang_fail, cap_hit). Mentions = k2_gate0.row (matcher v2; a negated or
    hedged class is a mention and never a TP, MT4 PREREG §1); P = sum tp / sum men, R = mean per-image recall over
    images with gold, F1 harmonic (object_prf.prf). Every caption passes untruncate first. ver="v1": row_v1."""
    out = []
    for i in ids:
        g = set(gold[i])
        c = KG.untruncate(caps[i], hit[i])
        r = KG.row(c, g, g) if ver == "v2" else row_v1(c, g)
        out.append((r["tp"], r["men"], r["tp"] / r["g"] if r["g"] else 0.0, float(r["g"] > 0),
                    float(not KG.language_ok(c)), float(hit[i])))
    return np.array(out, float)


def detailed_counts(caps: dict[str, str], hit: dict[str, bool], gold: dict, ids: list[str], ver: str = "v2") -> np.ndarray:
    """Per image (hal, men, tp, g): k2_gate0.row after untruncate; CHAIR_i = sum hal / sum men x 100 (§1)."""
    rows = [(KG.row(c, set(gold[i]), set(gold[i])) if ver == "v2" else row_v1(c, set(gold[i])))
            for i, c in ((i, KG.untruncate(caps[i], hit[i])) for i in ids)]
    return np.array([(r["hal"], r["men"], r["tp"], r["g"]) for r in rows], float)


def pool_seeds(arrs: list[np.ndarray]) -> np.ndarray:
    """§3 seed pooling: per-image counts summed over seeds; recall averaged (gold is the same)."""
    s = sum(arrs)
    s[:, 2] = s[:, 2] / len(arrs)
    s[:, 3:] = s[:, 3:] / len(arrs)
    return s


def prf(x: np.ndarray, idx=None) -> tuple[np.ndarray, np.ndarray, np.ndarray]:
    """(P, R, F1) x100 for short counts; idx (B, n) bootstrap draws give arrays of length B."""
    if idx is None:
        idx = np.arange(len(x))[None]
    tp, men, rec, hg = (x[:, k][idx] for k in range(4))
    P = 100 * tp.sum(-1) / np.maximum(men.sum(-1), 1)
    R = 100 * (rec * hg).sum(-1) / np.maximum(hg.sum(-1), 1)
    return P, R, np.where(P + R > 0, 2 * P * R / np.maximum(P + R, 1e-12), 0.0)


def chair(x: np.ndarray, idx=None) -> np.ndarray:
    if idx is None:
        idx = np.arange(len(x))[None]
    return 100 * x[:, 0][idx].sum(-1) / np.maximum(x[:, 1][idx].sum(-1), 1)


def hyp(sh: dict[str, np.ndarray], de: dict[str, np.ndarray], b: int = B_BOOT, seed: int = 0,
        k6_why: str = "K6 not in the kept set") -> dict:
    """The registered analysis (MT4 PREREG §3, §5): paired image bootstrap, B = 2,000, default_rng(0), one index draw
    shared by every system, percentile 2.5/97.5. H-B1: K1 (seeds pooled) vs base8_s, point dF1 >= +2.0, CI lo > 0, dP
    CI lo > -1.0. H-B2: K6 vs base8_s, dF1 CI lo > 0 and detailed dCHAIR_i CI hi < 0. Fixed sequence H-B1 -> H-B2."""
    n = len(sh["base8_s"])
    idx = np.random.default_rng(seed).integers(0, n, (b, n))
    k1 = pool_seeds([sh[s] for s in sh if s.startswith("k1_")])
    out: dict = {"n_images": n}

    def contrast(x, y):
        (px, rx, fx), (py, ry, fy) = prf(x), prf(y)
        (bx, _, bfx), (by, _, bfy) = prf(x, idx), prf(y, idx)
        ci = lambda v: [float(np.percentile(v, 2.5)), float(np.percentile(v, 97.5))]  # noqa: E731
        return {"dF1": float(fy[0] - fx[0]), "dF1_ci": ci(bfy - bfx), "dP": float(py[0] - px[0]), "dP_ci": ci(by - bx),
                "dR": float(ry[0] - rx[0]), "F1": [float(fx[0]), float(fy[0])]}
    c1 = contrast(sh["base8_s"], k1)
    b1 = c1["dF1"] >= SESOI_F1 and c1["dF1_ci"][0] > 0 and c1["dP_ci"][0] > MARGIN_P
    out["H-B1"] = c1 | {"holds": bool(b1)}
    if "k6_s1" in sh and "k6_s1" in de:
        c2 = contrast(sh["base8_s"], sh["k6_s1"])
        dc = float(chair(de["k6_s1"])[0] - chair(de["base8_s"])[0])
        bc = chair(de["k6_s1"], idx) - chair(de["base8_s"], idx)
        c2 |= {"dCHAIR_i": dc, "dCHAIR_i_ci": [float(np.percentile(bc, 2.5)), float(np.percentile(bc, 97.5))]}
        h2 = c2["dF1_ci"][0] > 0 and c2["dCHAIR_i_ci"][1] < 0
        out["H-B2"] = c2 | {"holds": bool(h2) if b1 else None, "tested": bool(b1),
                            "why": None if b1 else "sequence stopped at H-B1"}
    else:
        out["H-B2"] = {"tested": False, "holds": None, "why": k6_why}
    out["language_fail_share"] = {s: float(v[:, 4].mean()) for s, v in sh.items()}
    out["cap_hit_share"] = {s: float(v[:, 5].mean()) for s, v in sh.items()}
    return out


def p_pass(sh: dict[str, np.ndarray], de: dict[str, np.ndarray], n_test: int = N_KV, r: int = R_SIM,
           seed: int = 0) -> dict:
    """Predicted P(PASS on KV) by a two-level bootstrap on the tier-2 rows: draw a tier-2-sized resample (effect
    uncertainty), then a KV-sized sample from it (test sampling); in each replicate the H's are read with their
    registered forms, the CI bounds taken as point -/+ 1.96 x SE_KV, SE_KV = the tier-2 bootstrap SE x sqrt(n2 / n_test).
    Systems share every draw, so P(H-B1 and H-B2) is the joint frequency, not a bound."""
    n = len(sh["base8_s"])
    rng = np.random.default_rng(seed)
    k1 = pool_seeds([sh[s] for s in sh if s.startswith("k1_")])
    i0 = np.random.default_rng(0).integers(0, n, (B_BOOT, n))
    scale = math.sqrt(n / n_test)

    def se(fn):
        return float(np.std(fn(i0), ddof=1)) * scale
    dF1 = lambda x, y: lambda ix: prf(y, ix)[2] - prf(x, ix)[2]  # noqa: E731
    dP = lambda x, y: lambda ix: prf(y, ix)[0] - prf(x, ix)[0]  # noqa: E731
    se1f, se1p = se(dF1(sh["base8_s"], k1)), se(dP(sh["base8_s"], k1))
    has6 = "k6_s1" in sh and "k6_s1" in de
    if has6:
        se2f = se(dF1(sh["base8_s"], sh["k6_s1"]))
        se2c = se(lambda ix: chair(de["k6_s1"], ix) - chair(de["base8_s"], ix))
    ok1 = np.zeros(r, bool)
    ok2 = np.zeros(r, bool)
    for lo in range(0, r, 250):
        m = min(250, r - lo)
        outer = rng.integers(0, n, (m, n))
        ix = np.take_along_axis(outer, rng.integers(0, n, (m, n_test)), 1)
        f1, p1 = dF1(sh["base8_s"], k1)(ix), dP(sh["base8_s"], k1)(ix)
        ok1[lo:lo + m] = (f1 >= SESOI_F1) & (f1 - Z * se1f > 0) & (p1 - Z * se1p > MARGIN_P)
        if has6:
            f2 = dF1(sh["base8_s"], sh["k6_s1"])(ix)
            c2 = chair(de["k6_s1"], ix) - chair(de["base8_s"], ix)
            ok2[lo:lo + m] = (f2 - Z * se2f > 0) & (c2 + Z * se2c < 0)
    out = {"P_HB1": float(ok1.mean()), "n_t2": n, "n_test": n_test, "replicates": r,
           "se_kv": {"HB1_dF1": se1f, "HB1_dP": se1p}}
    if has6:
        out |= {"P_HB1_and_HB2": float((ok1 & ok2).mean()), "P_HB2": float(ok2.mean())}
        out["se_kv"] |= {"HB2_dF1": se2f, "HB2_dCHAIR_i": se2c}
    return out


def systems_of(caps: dict, tag: str) -> dict[str, list[str]]:
    """The systems of tier 2 ('t2') or the KV H systems ('kv') that the committed caps.json keeps (ladder applied)."""
    base = SYSTEMS_T2 if tag == "t2" else SYSTEMS_KV
    return {m: [s for s in ss if f"{tag}_{m}_{s}" in caps["cap_h"]] for m, ss in base.items()}


def load_set(d: Path, tag: str, systems: dict, gold: dict, ids: list[str], ver: str = "v2") -> tuple[dict, dict]:
    sh = {s: short_counts(*preds_of(d / f"k1k6_{tag}_{s}-short.preds.json"), gold, ids, ver) for s in systems["short"]}
    de = {s: detailed_counts(*preds_of(d / f"k1k6_{tag}_{s}-detailed.preds.json"), gold, ids, ver)
          for s in systems["detailed"]}
    return sh, de


def v1_desc(sh: dict[str, np.ndarray], de: dict[str, np.ndarray], **kw) -> dict:
    """hyp() on matcher-v1 rows, descriptive only (CC-175 N3, R2-2): no gating role, so 'holds'/'tested' are removed.
    It is written inside the same one-shot record as the v2 analysis, because nothing is rescored after a look."""
    h = hyp(sh, de, **kw)
    for k in ("H-B1", "H-B2"):
        h[k] = {x: y for x, y in h[k].items() if x not in ("holds", "tested")}
    return h | {"label": V1_LABEL}


V1_LABEL = ("v1 class lexicon with the section-1 negation/hedge rule (not score_dev.py's negation-blind v1); fixed after "
            "the val-924 planning numbers were seen (CC-205 W9); descriptive only, never gates")


def v1_safe(rows) -> dict:
    """CC-205 W9: a v1 failure never blocks the v2 record; it is written as the exception type only (no text)."""
    try:
        return v1_desc(*rows[:2], **rows[2])
    except Exception as e:  # noqa: BLE001 - recorded in the one-shot record, not swallowed
        return {"error": type(e).__name__, "label": V1_LABEL}


def closure(files=SCORER_CLOSURE, root: Path = ROOT) -> dict[str, str]:
    if miss := [r for r in files if not (root / r).is_file()]:  # Codex 3: a FAULT, never a FileNotFoundError
        raise SystemExit(f"FAULT: scorer closure file(s) missing {miss} (TO-PI)")
    return {r: sha(root / r) for r in files}


def closure_check(anchored: dict | None, now: dict[str, str]) -> None:
    """CC-205 W5: the scorer that reads KV must be byte-identical to the one that wrote the anchored tier-2 record."""
    if anchored != now:
        bad = sorted(k for k in set(anchored or {}) | set(now) if (anchored or {}).get(k) != now.get(k))
        raise SystemExit(f"FAULT: scorer closure differs from the anchored t2_decide closure {bad}; nothing read (TO-PI)")


# ------------------------------------------------------------------------------------------------ tier rules
def t1_rule(sh: dict[str, np.ndarray]) -> dict:
    """(a) N_SHORT 160, or 256 if any tier-1 short decode has > 1% cap hits. (c) E* = the epoch checkpoint (e1..e3,
    seed 0) with the largest point dF1 over base8_s among those with language-fail share <= 2% (d) and point dP >= -1.0;
    a checkpoint within 0.5 F1 of the best with fewer epochs wins. None qualifies, or the best point dF1 < +2.0
    (futility, CC-175 N5): T1_FAIL."""
    base = sh["base8_s"]
    rows = {}
    for e in EPOCH_GRID:
        x = sh[f"e{e}"]
        (pb, _, fb), (px, _, fx) = prf(base), prf(x)
        rows[e] = {"dF1": float(fx[0] - fb[0]), "dP": float(px[0] - pb[0]), "lang_fail": float(x[:, 4].mean()),
                   "cap_hit": float(x[:, 5].mean())}
    ok = {e: v for e, v in rows.items() if v["lang_fail"] <= LANG_MAX and v["dP"] >= MARGIN_P}
    n_short = N_SHORT_FALLBACK if max(float(v[:, 5].mean()) for v in sh.values()) > CAPHIT_MAX else N_SHORT
    if not ok:
        return {"verdict": "T1_FAIL", "rows": rows, "n_short": n_short}
    best = max(v["dF1"] for v in ok.values())
    if best < SESOI_F1:  # futility (CC-175 N5): no checkpoint reaches the SESOI on dev, so tier 2 cannot pass H-B1
        return {"verdict": "T1_FAIL", "why": "futility: best dF1 < +2.0", "rows": rows, "n_short": n_short}
    e_star = min(e for e, v in ok.items() if v["dF1"] >= best - EPOCH_TIE)
    return {"verdict": "T1_OK", "epochs": e_star, "n_short": n_short, "rows": rows,
            "label": "DEV-EXPLORE (val 924): selection only, never a result"}


def t2_rule(h: dict, pp: dict, kv_sys: dict | None = None) -> dict:
    """T2_PASS (the KV look is licensed) iff H-B1 holds on T2 with its registered form, every K1 seed's language-fail
    share <= 2%, and P(H-B1 on KV) >= 0.98. K6 enters the KV kept set iff additionally H-B2 holds on T2, K6's
    language-fail share <= 2% and P(H-B1 and H-B2) >= 0.98; otherwise H-B2 reads 'not tested (K6 failed the tier-2
    rehearsal)'. Anything else: T2_FAIL (no KV look; reported as a dev result, TO-PI under the pivot rule)."""
    lang = h["language_fail_share"]
    k1_lang = all(v <= LANG_MAX for s, v in lang.items() if s.startswith("k1_"))
    ok = h["H-B1"]["holds"] and k1_lang and pp["P_HB1"] >= P_MIN
    k6 = ok and h["H-B2"].get("holds", False) and lang.get("k6_s1", 1.0) <= LANG_MAX \
        and pp.get("P_HB1_and_HB2", 0.0) >= P_MIN
    kv_sys = kv_sys or {m: list(ss) for m, ss in SYSTEMS_KV.items()}
    kept = {m: [s for s in ss if k6 or s != "k6_s1"] for m, ss in kv_sys.items()} if ok else {}
    return {"verdict": "T2_PASS" if ok else "T2_FAIL", "k6_kept": bool(k6), "kv_kept": kept,
            "h_b2_status": "kept" if k6 else (h["H-B2"].get("why") or "not tested (K6 failed the tier-2 rehearsal)")}


def cmd_t1select(a) -> None:
    d = Path(a.dir)
    gold = {k: v for k, v in json.loads(K.pinned("manuscript/prereg/2026-10-27_grl_pilot/gold_instances.json")
                                        .read_text())["gold"].items()}
    ids = [str(i) for i in K.ids("val924")]
    sh = {s: short_counts(*preds_of(d / f"k1k6_t1_{s}-short.preds.json"), gold, ids)
          for s in ("base8_s", "e1", "e2", "e3")}
    rec = t1_rule(sh) | {"utc": utc(), "inputs_sha256": {p.name: sha(p) for p in sorted(d.glob("k1k6_t1_*.preds.json"))}}
    excl_write(d / "t1_select.json", json.dumps(rec, indent=1) + "\n")
    print(json.dumps({k: rec.get(k) for k in ("verdict", "epochs", "n_short")}))


def cmd_t2decide(a) -> None:
    d = Path(a.dir)
    gold = json.loads(committed_file(PDIR / "t2_gold.json").read_text())["gold"]
    caps = json.loads(committed_file(PDIR / "caps.json").read_text())
    ids = [str(i) for i in t2_ids()]
    sys2 = systems_of(caps, "t2")
    sh, de = load_set(d, "t2", sys2, gold, ids)
    h = hyp(sh, de, k6_why="not tested (cost: K6 cut by the ladder)")
    pp = p_pass(sh, de)
    v1 = v1_safe((*load_set(d, "t2", sys2, gold, ids, "v1"), {"k6_why": "not tested (cost: K6 cut by the ladder)"}))
    rec = t2_rule(h, pp, systems_of(caps, "kv")) | {"systems": sys2, "scorer_sha256": sha(Path(__file__)), "scorer_closure": closure(), "tier2": h, "p_pass": pp,
                                                     "tier2_matcher_v1": v1, "utc": utc(),
                            "label": "DEV-CONFIRM rehearsal (T2-2000): licenses the KV look, never a result",
                            "inputs_sha256": {p.name: sha(p) for p in sorted(d.glob("k1k6_t2_*.preds.json"))}}
    excl_write(d / "t2_decide.json", json.dumps(rec, indent=1) + "\n")
    print(json.dumps({"verdict": rec["verdict"], "k6_kept": rec["k6_kept"], "P_HB1": round(pp["P_HB1"], 4)}))


def kv_ready(d: Path, mid_file: Path = Path("/root/.vsps_machine_id"), head=committed) -> dict:
    """The KV look is licensed only if: this host is the m3 role (M1); every gate field is a LOG id; t2_decide.json's
    sha256 is the committed anchor and its verdict is T2_PASS; no KV decision exists yet (one look)."""
    mid = mid_file.read_text().strip().lower() if mid_file.is_file() else ""
    if mid != "m3":
        raise SystemExit("REFUSED: the KV look runs on the m3 role (M1) only")
    if miss := gates_missing(text=head(GATES.relative_to(ROOT).as_posix())):
        raise SystemExit(f"REFUSED: gate fields without a committed LOG id: {miss}")
    t2 = d / "t2_decide.json"
    anchor = head(T2_ANCHOR.relative_to(ROOT).as_posix())
    if not t2.is_file() or not anchor or anchor.split()[0] != sha(t2):
        raise SystemExit("REFUSED: t2_decide.json is missing or not the anchor committed at HEAD")
    rec = json.loads(t2.read_text())
    if rec["verdict"] != "T2_PASS":
        raise SystemExit("REFUSED: tier 2 did not pass; no KV look (PI-1029n)")
    if (d / "mt4_k1k6_decide.json").exists():
        raise SystemExit("REFUSED: the KV look already happened")
    if (d / KV_ATTEMPT).exists():  # Codex 2: a started scoring attempt is terminal, also after a crash
        raise SystemExit("REFUSED: a KV scoring attempt already started; terminal (TO-PI, new irreversible ruling)")
    return rec["kv_kept"]


KV_ATTEMPT = "kvscore_attempt.json"


def kv_attempt(d: Path, rec: dict) -> None:
    """Codex 2: the one-look marker, created O_EXCL and fsynced before any KV gold or prediction is read. Any later
    failure is terminal: kv_ready refuses every later scoring (and decoding) call."""
    try:
        excl_write(d / KV_ATTEMPT, json.dumps(rec | {"utc": utc()}, indent=1) + "\n")
    except FileExistsError:
        raise SystemExit("REFUSED: a KV scoring attempt already started; terminal (TO-PI)") from None


def cmd_kvready(a) -> None:
    print(json.dumps(kv_ready(Path(a.dir))))


def cmd_kvsums(a) -> None:
    """Append `SHA  FILE  SYSTEM  UTC` (UTC from the code, fsynced) when a KV decoder finishes. Nobody opens it."""
    import k2_gate1 as G1

    p = Path(a.pred)
    G1.ledger_append(KV_SUMS, f"{sha(p)}  {p.name}  {a.system}  {utc()}")


def freeze_set(lines: list[str], kept: list[str], now: float, not_before: float = 0.0) -> dict:
    """First line per system counts; another sha for a kept system halts (FAULT); a line after D_K or outside the kept
    set is descriptive. Freeze instant = min(completion of the kept set + 24 h, D_K); no scoring before it."""
    import calendar

    first, desc, done_t, last = {}, [], None, -math.inf
    for x in lines:
        h, f, s, t = x.split("  ")
        ts = calendar.timegm(time.strptime(t, "%Y-%m-%dT%H:%M:%SZ"))
        if ts < last or ts < not_before:
            raise SystemExit("FAULT: KV_PRED_SUMS lines out of order or before the T2 anchor (TO-PI)")
        last = ts
        if s in first and first[s][0] != h:
            raise SystemExit(f"FAULT: {s} has two KV predictions with different shas (TO-PI)")
        if s not in kept or ts > D_K:
            desc.append(s)
            continue
        if s in first:  # a same-sha repeat
            desc.append(s)
            continue
        first[s] = (h, f, ts)
        if set(first) == set(kept):
            done_t = ts
    instant = min(done_t + 86400, D_K) if done_t is not None else D_K
    if now < instant:
        raise SystemExit(f"HELD: no scoring before the freeze instant {utc(instant)}")
    return {"frozen": {s: v[:2] for s, v in first.items()}, "missing": sorted(set(kept) - set(first)),
            "descriptive": desc, "instant_utc": utc(instant)}


def hb1_needs(names: list[str]) -> list[str]:
    return list(HB1_NEEDS) + [x for x in names if x.startswith("short:k1_")]


def cmd_kvscore(a) -> None:
    """One look: the frozen KV predictions, scored once by hyp() (the analysis tier 2 rehearsed). A missing seed of an
    H system makes that H NOT-RUN and stops the sequence (PREREG §2)."""
    d = Path(a.dir)
    kept = kv_ready(d)
    names = [f"{m}:{s}" for m, ss in kept.items() for s in ss]  # H systems only; the descriptive row is outside
    import calendar

    t2 = json.loads((d / "t2_decide.json").read_text())  # anchored by kv_ready
    closure_check(t2.get("scorer_closure"), closure())  # CC-205 W5: before any KV prediction, gold or freeze read
    t2_utc = t2["utc"]  # CC-175 R2-1
    fr = freeze_set(KV_SUMS.read_text().splitlines(), names, time.time(),
                    calendar.timegm(time.strptime(t2_utc, "%Y-%m-%dT%H:%M:%SZ")))  # shas + times only; HELD writes nothing
    kv_attempt(d, {"closure_sha256": hashlib.sha256(json.dumps(closure(), sort_keys=True).encode()).hexdigest(),
                   "freeze": fr})  # Codex 2: before any KV gold or prediction read
    gold = json.loads(committed_file(PDIR / "kv_gold.json").read_text())["gold"]
    ids = [str(i) for i in set_ids("kv")]  # checks the 86d93863 pin
    miss = set(fr["missing"])
    if miss & set(hb1_needs(names)):  # H-B1 NOT-RUN: the sequence stops (H-B2 is never reached)
        rec = {"verdict": "NOT-RUN", "missing": fr["missing"]}
    else:  # an H-B2 row missing: H-B2 NOT-RUN only; every H-B2 row is dropped so hyp() reports it untested
        drop = set(HB2_NEEDS) if miss & set(HB2_NEEDS) else set()
        names = [x for x in names if x not in drop]
        for s, (h, f) in fr["frozen"].items():
            if sha(d / f) != h:
                raise SystemExit(f"FAULT: {f} differs from KV_PRED_SUMS")
        def rows(ver: str) -> tuple[dict, dict]:
            return ({s.split(":")[1]: short_counts(*preds_of(d / fr["frozen"][s][1]), gold, ids, ver) for s in names
                     if s.startswith("short:")},
                    {s.split(":")[1]: detailed_counts(*preds_of(d / fr["frozen"][s][1]), gold, ids, ver) for s in names
                     if s.startswith("detailed:")})
        why = "NOT-RUN (an H-B2 row is missing)" if drop else "not tested (K6 not kept by tier 2)"
        rec = {"verdict": "SCORED", "kv": hyp(*rows("v2"), k6_why=why), "kv_matcher_v1": v1_safe((*rows("v1"), {"k6_why": why}))}
    rec |= {"scorer_sha256": sha(Path(__file__)), "freeze": fr, "utc": utc(), "label": "MT4 Branch K1+K6, CONFIRMATORY, one look (KV-4,224)"}
    excl_write(d / "mt4_k1k6_decide.json", json.dumps(rec, indent=1) + "\n")
    print(json.dumps({"verdict": rec["verdict"]}))


# ------------------------------------------------------------------------------------------------ W2: K2 only via l.296
NOGO = ("On the development set, the gold-edited student did not meet the pre-registered gate (failed: {failed}; "
        "ΔCHAIR_i {x:+.2f}, Δrecall {y:+.2f}, gap to the truncation frontier {w:+.2f}). Per the rule, K2 was not run "
        "on the test set; it is reported as a negative development pilot, and the paper's headline rests on K1 + K6.")


def nogo_sentence(rec: dict) -> str:
    """K2 Gate 1 RULE l.296 filled from gate1_decide.json; the only route by which a Gate 1 number enters MT4 K1+K6
    text (CC-174 W2). Refuses anything but a NO-GO."""
    if rec.get("verdict") != "NO-GO":
        raise SystemExit("REFUSED: the l.296 sentence is for a NO-GO only")
    d = rec["delta"]
    return NOGO.format(failed=", ".join(rec["failed"]), x=d["G1_CHAIR_i_K_minus_base_s"]["point"],
                       y=d["G2_R_K_minus_base_s"]["point"], w=d["G4_frontier_gap"]["point"])


def cmd_nogo(a) -> None:
    f = Path(a.decide)
    want = (ROOT / GATE1_DECIDE_ANCHOR).read_text().split()[0]
    if sha(f) != want:
        raise SystemExit("REFUSED: gate1_decide.json is not the anchored file (6987b911)")
    print(nogo_sentence(json.loads(f.read_text())))


# ------------------------------------------------------------------------------------------------ planning power
def cmd_power(a) -> None:
    """Planning only (no rule reads it): per-image counts of two EXISTING val-924 short decodes (default: Qwen2.5-VL
    P1 vs fuse2 SFT, uitviic_ind_val) under the T2 scorer; the paired SE, and P(PASS on KV) from p_pass() at the
    observed effect and for shifted effects (normal approximation with the observed per-image SD)."""
    from statistics import NormalDist

    gold = json.loads(K.pinned("manuscript/prereg/2026-10-27_grl_pilot/gold_instances.json").read_text())["gold"]
    ids = [str(i) for i in K.ids("val924")]
    x = short_counts(*preds_of(Path(a.base)), gold, ids)
    y = short_counts(*preds_of(Path(a.sys)), gold, ids)
    n = len(ids)
    i0 = np.random.default_rng(0).integers(0, n, (B_BOOT, n))
    bf = prf(y, i0)[2] - prf(x, i0)[2]
    bp = prf(y, i0)[0] - prf(x, i0)[0]
    d_f1 = float(prf(y)[2][0] - prf(x)[2][0])
    d_p = float(prf(y)[0][0] - prf(x)[0][0])
    sd_f, sd_p = float(np.std(bf, ddof=1)) * math.sqrt(n), float(np.std(bp, ddof=1)) * math.sqrt(n)
    emp = p_pass({"base8_s": x, "k1_s1": y}, {}, N_KV)["P_HB1"]
    nd = NormalDist()
    table = {}
    for n2 in a.n2:
        s_pred_f = sd_f * math.sqrt(1 / n2 + 1 / N_KV)
        s_pred_p = sd_p * math.sqrt(1 / n2 + 1 / N_KV)
        thr = max(SESOI_F1, Z * sd_f / math.sqrt(N_KV))
        rows = {}
        for d in (2.5, 3.0, 4.0, 5.0, 8.0, 12.0, 16.0):
            pf = nd.cdf((d - thr) / s_pred_f)
            pp = nd.cdf((d_p - (MARGIN_P + Z * sd_p / math.sqrt(N_KV))) / s_pred_p)
            rows[f"{d:+.1f}"] = round(max(0.0, pf + pp - 1), 4)  # Frechet lower bound of the joint
        d98 = thr + nd.inv_cdf(P_MIN) * s_pred_f
        table[str(n2)] = {"P_HB1_frechet_lower_by_t2_point_dF1": rows, "dF1_needed_for_P98": round(d98, 2)}
    rec = {"label": "PLANNING ONLY: existing val-924 dev decodes, Qwen2.5-VL SFT pair, not K1 and not a rule input",
           "inputs_sha256": {Path(a.base).name: sha(Path(a.base)), Path(a.sys).name: sha(Path(a.sys))},
           "n": n, "observed": {"dF1": round(d_f1, 3), "dP": round(d_p, 3), "sd_per_image_F1": round(sd_f, 3),
                                "sd_per_image_P": round(sd_p, 3)},
           "P_HB1_two_level_bootstrap_at_observed_effect_n2_924": round(emp, 4), "by_n2": table}
    Path(a.out).write_text(json.dumps(rec, indent=1) + "\n")
    print(json.dumps({"observed": rec["observed"], "emp_P": rec["P_HB1_two_level_bootstrap_at_observed_effect_n2_924"],
                      "d98": {k: v["dF1_needed_for_P98"] for k, v in table.items()}}))


# ------------------------------------------------------------------------------------------------ selftest
def _synth(n: int, rng, tp_rate: float, men: float = 2.0) -> np.ndarray:
    m = rng.poisson(men, n).astype(float) + 1
    tp = rng.binomial(m.astype(int), tp_rate).astype(float)
    g = rng.integers(1, 4, n).astype(float)
    rec = np.minimum(tp, g) / g
    return np.stack([tp, m, rec, np.ones(n), np.zeros(n), np.zeros(n)], 1)


def selftest() -> None:
    import tempfile

    rng = np.random.default_rng(1)
    # gate ids (CC-169 W3): LOG ids pass, ruling ids and blanks do not
    with tempfile.TemporaryDirectory() as t:
        g = Path(t) / "GATES.json"
        g.write_text(json.dumps({"W25K1": "OPS-1030a", "COST": "CC-175", "T1": "", "AMEND2": "OPS-1031a", "T2": "PI-1030b"}))
        assert gates_missing(text=g.read_text()) == ["COST", "T1"], gates_missing(text=g.read_text())
        assert gates_missing(text=None) == list(GATE_KEYS)  # nothing committed: every gate is missing
        assert GATE_RE.fullmatch("OPS-1029t") and not GATE_RE.fullmatch("CC-168")
    # T2 sampler: deterministic, size, subset, salt-dependent
    c = set(range(10_000, 40_000))
    s1, s2 = t2_sample(c, 50), t2_sample(set(reversed(sorted(c))), 50)
    assert s1 == s2 and len(s1) == 50 and set(s1) <= c and s1 != t2_sample(c, 50, "other")
    # T2 exclusion inputs (CC-188 W1): .txt first column and every integer id list inside a .json are excluded
    with tempfile.TemporaryDirectory() as t:
        (Path(t) / "x").mkdir()
        (Path(t) / "x/val_ids.txt").write_text("139\n285\tnote\n")
        (Path(t) / "x/lists.json").write_text(json.dumps({"sets": {"D1": {"n": 2, "ids": ["11", "12"]}},
                                                          "drops": {"kv": [13]}, "pins": {"k": "ab12"}, "p": [0.5, 1]}))
        assert prereg_int_ids(Path(t)) == {139, 285, 11, 12, 13}, prereg_int_ids(Path(t))
    # example plan: one example per image per epoch; references cycle
    pool = [("a:1", "f1", "h", 3), ("b:2", "f2", "h", 1), ("c:3", "f3", "h", 2)]
    ep = example_plan(pool, 3, 1)
    assert len(ep) == 9 and sorted(j for k, j in ep if k == "a:1") == [0, 1, 2] and {j for k, j in ep if k == "b:2"} == {0}
    # scorer + hypotheses: a strong K1 holds H-B1, an equal one does not
    base = _synth(600, rng, 0.70)
    strong, same = _synth(600, rng, 0.90, 3.0), base.copy()
    det_b = np.stack([rng.poisson(1.0, 600), rng.poisson(6, 600) + 1, np.zeros(600), np.ones(600)], 1).astype(float)
    det_k6 = det_b.copy()
    det_k6[:, 0] = 0
    h = hyp({"base8_s": base, "k1_s1": strong, "k1_s2": strong, "k6_s1": strong}, {"base8_s": det_b, "k6_s1": det_k6}, 300)
    assert h["H-B1"]["holds"] and h["H-B2"]["holds"] and h["H-B2"]["tested"], h
    h0 = hyp({"base8_s": base, "k1_s1": same, "k1_s2": same}, {"base8_s": det_b}, 300)
    assert not h0["H-B1"]["holds"] and not h0["H-B2"]["tested"]
    # P(PASS): large effect -> ~1, no effect -> ~0; rule outcomes
    pp = p_pass({"base8_s": base, "k1_s1": strong, "k1_s2": strong, "k6_s1": strong},
                {"base8_s": det_b, "k6_s1": det_k6}, 4224, 300)
    p0 = p_pass({"base8_s": base, "k1_s1": same}, {}, 4224, 300)
    assert pp["P_HB1"] > 0.99 and pp["P_HB1_and_HB2"] > 0.99 and p0["P_HB1"] < 0.05, (pp, p0)
    r = t2_rule(h, pp)
    assert r["verdict"] == "T2_PASS" and r["k6_kept"] and "k6_s1" in r["kv_kept"]["detailed"]
    assert t2_rule(h, pp | {"P_HB1": 0.97})["verdict"] == "T2_FAIL"
    assert t2_rule(h, pp | {"P_HB1_and_HB2": 0.5})["kv_kept"]["short"] == ["base8_s", "k1_s1", "k1_s2"]
    bad = dict(h, language_fail_share=h["language_fail_share"] | {"k1_s2": 0.05})
    assert t2_rule(bad, pp)["verdict"] == "T2_FAIL"
    # tier-1 rule: best epoch, tie -> fewer epochs, language gate, cap-hit fallback
    e1, e3 = _synth(600, rng, 0.88, 3.0), strong.copy()
    lang = strong.copy()
    lang[:30, 4] = 1
    t = t1_rule({"base8_s": base, "e1": e1, "e2": lang, "e3": e3})
    assert t["verdict"] == "T1_OK" and t["n_short"] == N_SHORT
    assert t["epochs"] == min(e for e in (1, 3) if t["rows"][e]["dF1"] >= max(t["rows"][x]["dF1"] for x in (1, 3)) - 0.5)
    assert t1_rule({"base8_s": base, **{f"e{e}": same for e in EPOCH_GRID}})["why"].startswith("futility")
    hit = base.copy()
    hit[:10, 5] = 1
    assert t1_rule({"base8_s": hit, "e1": e1, "e2": e1, "e3": e1})["n_short"] == N_SHORT_FALLBACK
    allbad = {"base8_s": base, **{f"e{e}": lang for e in EPOCH_GRID}}
    assert t1_rule(allbad)["verdict"] == "T1_FAIL"
    # cost plan fits the test line at planning rates; a slow measured rate walks the ladder
    p = plan()
    assert p["fits"] and not p["ladder_applied"] and p["cap_total_h"] == 92.6 and KV_DESC in p["cap_h"], p["cap_total_h"]
    assert round(p["cap_total_h"] - p["cap_h"][KV_DESC], 1) == 83.3  # H stages alone
    assert systems_of(p, "t2") == {m: list(v) for m, v in SYSTEMS_T2.items()}
    slow = plan({"train_8b": 1.0, "short": 1.1, "detailed": 6.5})  # end to end: the ladder cuts K6 (desc fits after)
    assert slow["ladder_applied"] == ["cut K6"] and "train_k6_s1" not in slow["cap_h"] and slow["fits"]
    assert not plan({"train_8b": 3.0, "short": 1.1, "detailed": 6.5})["fits"]  # H systems alone too big: cost stop
    tight = plan(n_pool=19000)  # H stages fit (92.1) but not with the descriptive row: it is dropped, nothing else
    assert tight["fits"] and not tight["ladder_applied"] and KV_DESC not in tight["cap_h"] and "train_k6_s1" in tight["cap_h"]
    s2, kv2 = systems_of(slow, "t2"), systems_of(slow, "kv")
    assert "k6_s1" not in s2["short"] + s2["detailed"] and "k6_s1" not in kv2["short"] + kv2["detailed"]
    hk = hyp({"base8_s": base, "k1_s1": strong, "k1_s2": strong}, {"base8_s": det_b}, 200, k6_why="not tested (cost)")
    rk = t2_rule(hk, p_pass({"base8_s": base, "k1_s1": strong, "k1_s2": strong}, {"base8_s": det_b}, 4224, 200), kv2)
    assert rk["verdict"] == "T2_PASS" and not rk["k6_kept"] and rk["h_b2_status"] == "not tested (cost)"
    assert hk["H-B2"]["holds"] is None
    # AMENDMENT_2 B5 (CC-175 N3): matcher v1 beside v2 is descriptive; the v2 analysis and rule are unchanged
    v1 = v1_desc({"base8_s": base, "k1_s1": strong, "k1_s2": strong, "k6_s1": strong}, {"base8_s": det_b, "k6_s1": det_k6}, b=300)
    assert v1["H-B1"]["dF1"] == h["H-B1"]["dF1"] and v1["H-B1"]["dF1_ci"] == h["H-B1"]["dF1_ci"]
    assert not {"holds", "tested"} & (set(v1["H-B1"]) | set(v1["H-B2"])) and h["H-B1"]["holds"] and h["H-B2"]["tested"]
    assert v1_safe((None, None, {}))["error"] == "TypeError"  # CC-205 W9: a v1 failure is recorded, never raised
    # CC-205 W5: scorer closure; a changed or missing file FAULTs before anything is read
    c0 = closure()
    assert set(c0) == set(SCORER_CLOSURE) and all(len(v) == 64 for v in c0.values())
    closure_check(dict(c0), c0)
    for bad_c in (None, {}, c0 | {"scripts/grl/reward.py": "0" * 64}, {k: v for k, v in c0.items() if k != "rescap/vocab.py"}):
        try:
            closure_check(bad_c, c0)
            raise AssertionError("a differing scorer closure was accepted")
        except SystemExit as e:
            assert "closure" in str(e)
    term, cls = next((t.strip(), c) for t, c in KG.RW.terms() if c == "dog")
    orig, seen = KG.RW.ordered, []
    KG.RW.ordered = lambda c, v: seen.append(v) or orig(c, v)
    try:
        r1 = row_v1(term + ".", {cls})
    finally:
        KG.RW.ordered = orig
    assert set(seen) == {"v1"} and r1 == {"tp": 1, "hal": 0, "men": 1, "g": 1} and row_v1(term + ".", set())["hal"] == 1
    cp, hp, gd = {"1": term + "."}, {"1": False}, {"1": [cls]}
    assert (short_counts(cp, hp, gd, ["1"], "v1") == short_counts(cp, hp, gd, ["1"])).all()
    assert (detailed_counts(cp, hp, gd, ["1"], "v1") == detailed_counts(cp, hp, gd, ["1"])).all()
    import subprocess  # CC-205 W5: a fresh process that only imports this file and scores v1 and v2 loads nothing else
    probe = ("import sys; sys.path.insert(0, sys.argv[1]); import k1k6 as k; c = {'1': sys.argv[2]}; h = {'1': False}; "
             "g = {'1': [sys.argv[3]]}; [f(c, h, g, ['1'], v) for f in (k.short_counts, k.detailed_counts) for v in ('v1', 'v2')]; "
             "print('\\n'.join(m.__file__ for m in list(sys.modules.values()) if getattr(m, '__file__', None)))")
    out = subprocess.run([sys.executable, "-c", probe, str(HERE), term + ".", cls], capture_output=True, text=True, check=True)
    side = {Path(f).resolve() for f in out.stdout.split()}
    side = {f.relative_to(ROOT).as_posix() for f in side if ROOT in f.parents} - {"scripts/mt4_k1k6/k1k6.py"}
    assert side <= set(SCORER_CLOSURE), side - set(SCORER_CLOSURE)
    # AMENDMENT_2 B4: a staged T2/KV body must equal its own C-EN record row; a refused sha passes only as a KV row
    stage_check("t2", 7, "aa", {"zz"}, {7: "aa"})
    stage_check("kv", 7, "zz", {"zz"}, {7: "zz"})  # a Karpathy-val body is a refused sha by design
    for name, h, bad_sha, rec, why in (("t2", "aa", set(), {7: "bb"}, "record row"), ("t2", "aa", set(), {}, "record row"),
                                       ("t2", "zz", {"zz"}, {7: "zz"}, "refused"), ("kv", "zz", {"zz"}, {7: "yy"}, "refused"),
                                       ("kv", "aa", set(), {8: "aa"}, "record row")):
        try:
            stage_check(name, 7, h, bad_sha, rec)
            raise AssertionError(f"stage_check accepted {name} {h}")
        except SystemExit as e:
            assert why in str(e), e
    with tempfile.TemporaryDirectory() as t:
        (Path(t) / "memory.sha256.tsv").write_text("7\tCOCO_val2014_000000000007.jpg\taa\t1\n")
        for name in ("t2", "kv"):  # unpinned or missing record
            try:
                cen_record(name, Path(t))
                raise AssertionError("an unpinned C-EN record was accepted")
            except SystemExit as e:
                assert "not its pin" in str(e)
    # W1: what makes H-B1 NOT-RUN at KV
    nm = ["short:base8_s", "short:k1_s1", "short:k1_s2", "short:k6_s1", "detailed:base8_s", "detailed:k6_s1"]
    assert set(hb1_needs(nm)) == {"short:base8_s", "short:k1_s1", "short:k1_s2"}
    assert not {"detailed:base8_s", "detailed:k6_s1", "detailed:k1_s1"} & set(hb1_needs(nm))
    # W2: the l.296 sentence only, NO-GO only
    rec = {"verdict": "NO-GO", "failed": ["G1", "G3"], "delta": {"G1_CHAIR_i_K_minus_base_s": {"point": -1.0},
           "G2_R_K_minus_base_s": {"point": 0.5}, "G4_frontier_gap": {"point": 1.0}}}
    assert "negative development pilot" in nogo_sentence(rec) and "failed: G1, G3" in nogo_sentence(rec)
    try:
        nogo_sentence(rec | {"verdict": "GO"})
        raise AssertionError("GO accepted")
    except SystemExit:
        pass
    # one look, KV licence and freeze
    with tempfile.TemporaryDirectory() as t:
        t = Path(t)
        excl_write(t / "x.json", "{}")
        try:
            excl_write(t / "x.json", "{}")
            raise AssertionError("second write accepted")
        except FileExistsError:
            pass
        mid = t / "mid"
        gates = json.dumps({k: "OPS-1031a" for k in GATE_KEYS})
        (t / "t2_decide.json").write_text(json.dumps({"verdict": "T2_PASS", "kv_kept": {"short": ["base8_s"]}}))
        good = {GATES.relative_to(ROOT).as_posix(): gates,
                T2_ANCHOR.relative_to(ROOT).as_posix(): sha(t / "t2_decide.json") + "  t2_decide.json\n"}
        for m, head, why in (("m4", good.get, "m3 role"), ("m3", lambda r: None, "committed LOG id"),
                             ("m3", lambda r: gates if "GATES" in r else None, "anchor committed")):
            mid.write_text(m)  # wrong host; nothing committed; an untracked anchor (W3)
            try:
                kv_ready(t, mid, head)
                raise AssertionError("KV look licensed without an anchored T2 PASS")
            except SystemExit as e:
                assert why in str(e), e
        assert kv_ready(t, mid, good.get) == {"short": ["base8_s"]}  # the positive case
        try:  # Codex 2: a crash after the attempt marker is terminal
            kv_attempt(t, {"closure_sha256": "0" * 64})
            raise RuntimeError("simulated crash after the marker, before the decision write")
        except RuntimeError:
            pass
        for call in (lambda: kv_ready(t, mid, good.get), lambda: kv_attempt(t, {})):
            try:
                call()
                raise AssertionError("a second KV scoring attempt was licensed")
            except SystemExit as e:
                assert "attempt already started" in str(e)
        (t / KV_ATTEMPT).unlink()
        (t / "mt4_k1k6_decide.json").write_text("{}")
        try:
            kv_ready(t, mid, good.get)
            raise AssertionError("a second KV look was licensed")
        except SystemExit:
            pass
        # Codex 3: a missing closure file is a FAULT
        try:
            closure(("no/such/file.py",), t)
            raise AssertionError("a missing closure file was accepted")
        except SystemExit as e:
            assert "closure file(s) missing" in str(e)
        # Codex 1 (CC-205 r3): caps.json that cuts K1 seed 2 makes `left` print 0 (the job's cost stop) for every stage
        import contextlib
        import io
        led = t / "led.tsv"
        led.touch()
        for ladder, want in ((["cut K6", "cut K1 seed 2"], "0"), (["cut K6"], None)):
            (t / "caps.json").write_text(json.dumps({"cap_h": {"train_k1_s1": 1.0}, "ladder_applied": ladder}))
            out = io.StringIO()
            with contextlib.redirect_stdout(out), contextlib.redirect_stderr(io.StringIO()):
                try:
                    cmd_left(argparse.Namespace(ledger=str(led), caps=str(t / "caps.json"), stage="train_k1_s1"))
                except SystemExit as e:
                    assert e.code == 0
            assert (out.getvalue().strip() == want) if want else int(out.getvalue()) > 0, (ladder, out.getvalue())
        now = D_K - 10 * 86400
        ln = [f"h1  a.json  short:base8_s  {utc(now - 3 * 86400)}", f"h2  b.json  short:k1_s1  {utc(now - 2 * 86400)}"]
        fr = freeze_set(ln, ["short:base8_s", "short:k1_s1"], now)
        assert not fr["missing"] and fr["instant_utc"] == utc(now - 86400)
        try:
            freeze_set(ln, ["short:base8_s", "short:k1_s1"], now - 2 * 86400 + 60)
            raise AssertionError("scored before the freeze instant")
        except SystemExit:
            pass
        for bad in (ln + [f"h9  c.json  short:k1_s1  {utc(now - 1000)}"], ln[::-1],  # re-decode; out of order
                    ln + [f"h9  c.json  short:k1_s1  {utc(D_K + 60)}"]):  # a different sha after D_K still halts
            try:
                freeze_set(bad, ["short:base8_s", "short:k1_s1"], D_K + 120)
                raise AssertionError("a bad KV_PRED_SUMS was accepted")
            except SystemExit:
                pass
        try:
            freeze_set(ln, ["short:base8_s", "short:k1_s1"], now, not_before=now - 2.5 * 86400)
            raise AssertionError("a line before the T2 anchor was accepted")
        except SystemExit:
            pass
        assert freeze_set(ln[:1], ["short:base8_s", "short:k1_s1"], D_K + 1)["missing"] == ["short:k1_s1"]
        # guard scan: a pool image by sha passes only under the pool root; a refused COCO id never
        (t / "pool").mkdir()
        (t / "pool/00000000001.jpg").write_bytes(b"pool")
        (t / "x").mkdir()
        allow = {K.sha_file(t / "pool/00000000001.jpg")}
        assert scan_k1([t], set(), set(), allow, t / "pool") == 1
        (t / "x/00000000002.jpg").write_bytes(b"other")
        try:
            scan_k1([t], set(), set(), allow, t / "pool")
            raise AssertionError("unlisted non-COCO image passed")
        except SystemExit:
            pass
        (t / "x/00000000002.jpg").unlink()
        (t / "kv").mkdir()
        (t / "kv/000000000042.jpg").write_bytes(b"kv")
        try:
            scan_k1([t], {42}, set(), allow, t / "pool")
            raise AssertionError("KV image passed outside tier 3")
        except SystemExit:
            pass
        h42 = K.sha_file(t / "kv/000000000042.jpg")
        assert scan_k1([t], {42}, {h42}, allow, t / "pool", {42: h42}, t / "kv") == 2  # its own row, under kv only
        for kv_ok in ({42: "0" * 64}, {}):  # another sha; no row
            try:
                scan_k1([t], {42}, {h42}, allow, t / "pool", kv_ok, t / "kv")
                raise AssertionError("a KV file passed without its own record row")
            except SystemExit:
                pass
        try:
            scan_k1([t], {42}, {h42}, allow, t / "pool", {42: h42}, t / "pool")  # its row, but outside k1k6_kv
            raise AssertionError("a KV file passed outside the KV root")
        except SystemExit:
            pass
        # CC-199/CC-200: key present -> exactly 1 row dropped, with or without the file on disk; key absent -> FAULT
        rows3 = [("ktvic:1", "k.jpg", 1), ("openviic:00000007169", "openviic/images/00000007169.jpg", 1)]
        assert not (t / rows3[1][1]).exists() and drop_trunc(rows3) == rows3[:1]  # file missing: no error
        (t / "openviic/images").mkdir(parents=True)
        (t / rows3[1][1]).write_bytes(b"trunc")
        assert drop_trunc(rows3) == rows3[:1]
        try:
            drop_trunc(rows3[:1])
            raise AssertionError("drop_trunc passed without the key")
        except SystemExit:
            pass
        # W6: C1 by sha against an exclusion list (XM3600), no feature needed
        pool_f = {"ids": ["ktvic:1", "openviic:2"], "sha": ["aa", "bb"]}
        keys, rec = w25k1_decide(pool_f, {}, None, {"xm3600_all_images": {"bb"}})
        assert keys == ["openviic:2"] and rec["counts"]["sha:xm3600_all_images"]["excluded"] == 1
    print("k1k6 selftest ok")


def main() -> None:
    if sys.argv[1:] == ["--selftest"]:
        selftest()
        return
    ap = argparse.ArgumentParser()
    sp = ap.add_subparsers(dest="cmd", required=True)
    sp.add_parser("lists")
    sp.add_parser("nogo").add_argument("--decide", default=str(
        ROOT / ".session_backup/machines/M1/root/outputs/k2_gate1/gate1_decide.json"))
    go = sp.add_parser("gold")
    go.add_argument("--ann", required=True)
    go.add_argument("--set", choices=("t2", "kv"), required=True)
    st = sp.add_parser("stage")
    st.add_argument("--set", choices=("t2", "kv"), required=True)
    st.add_argument("--ann", required=True)
    st.add_argument("--out", required=True)
    p = sp.add_parser("pool")
    p.add_argument("--data", required=True)
    p.add_argument("--out", required=True)
    w = sp.add_parser("w25k1")
    w.add_argument("op", choices=("feats", "decide"))
    for k in ("--list", "--images", "--sscd", "--name", "--out", "--pool"):
        w.add_argument(k)
    w.add_argument("--sets", nargs="*", default=[])
    w.add_argument("--workers", type=int, default=8)
    g = sp.add_parser("guard")
    g.add_argument("head")
    g.add_argument("--tier", type=int, choices=(1, 2, 3), required=True)
    g.add_argument("--pool", required=True)
    pl = sp.add_parser("plan")
    pl.add_argument("--rates")
    pl.add_argument("--t1")
    pl.add_argument("--out", required=True)
    le = sp.add_parser("left")
    for k in ("--ledger", "--stage", "--caps"):
        le.add_argument(k, required=True)
    tr = sp.add_parser("train")
    tr.add_argument("--model", choices=tuple(MODELS), required=True)
    tr.add_argument("--seed", type=int, required=True)
    tr.add_argument("--epochs", type=int, required=True)
    tr.add_argument("--pool", required=True)
    tr.add_argument("--data", required=True)
    tr.add_argument("--out-dir", required=True)
    tr.add_argument("--save-epochs", action="store_true")
    de = sp.add_parser("decode")
    de.add_argument("--model", choices=tuple(MODELS), required=True)
    de.add_argument("--mode", choices=("short", "detailed"), required=True)
    de.add_argument("--n-new", type=int, required=True)
    de.add_argument("--adapter")
    for k in ("--manifest", "--images", "--out"):
        de.add_argument(k, required=True)
    for name in ("t1select", "t2decide", "kvready", "kvscore"):
        sp.add_parser(name).add_argument("--dir", required=True)
    ks = sp.add_parser("kvsums")
    ks.add_argument("--pred", required=True)
    ks.add_argument("--system", required=True)
    pw = sp.add_parser("power")
    pw.add_argument("--base", default=str(ROOT / "data/results/uitviic_ind_val/uitviic_p1_s42-short.preds.json"))
    pw.add_argument("--sys", default=str(ROOT / "data/results/uitviic_ind_val/uitviic_fuse2_s42-short.preds.json"))
    pw.add_argument("--n2", type=int, nargs="*", default=[924, 1500, 2000, 3000])
    pw.add_argument("--out", default=str(PDIR / "power_planning.json"))
    a = ap.parse_args()
    {"lists": cmd_lists, "nogo": cmd_nogo, "gold": cmd_gold, "stage": cmd_stage, "pool": cmd_pool, "w25k1": cmd_w25k1, "guard": cmd_guard,
     "plan": cmd_plan, "left": cmd_left, "train": cmd_train, "decode": cmd_decode, "t1select": cmd_t1select,
     "t2decide": cmd_t2decide, "kvready": cmd_kvready, "kvsums": cmd_kvsums, "kvscore": cmd_kvscore,
     "power": cmd_power}[a.cmd](a)


if __name__ == "__main__":
    main()
