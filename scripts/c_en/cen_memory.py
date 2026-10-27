#!/usr/bin/env python3
"""C-EN memory and examples. Prereg manuscript/prereg/2026-10-27_c_en/PREREG.md §4, §5, §9 item 5.

  python3 scripts/c_en/cen_memory.py --selftest                                         CPU, synthetic only
  python3 scripts/c_en/cen_memory.py build --emb E --feats F --protect S=FEATS ... --out-dir D       CPU, M3
  python3 scripts/c_en/cen_memory.py exemplars --set S --memory M --memory-emb ME --query-emb Q --out X  CPU, M3
  python3 scripts/c_en/cen_memory.py store --what memory|coco_test|nocaps_val --memory M [--captions F] --out F
                                                                                          laptop only
build: §4 steps 3-5 with build_memory.near / clusters unchanged (C's rule), members sorted by cocoid, clusters by
their smallest cocoid, members[0] = the smallest; the cluster vector is members[0]'s. It writes ids and sha256 only.
exemplars: build_memory.exemplars unchanged on this memory and one test set's query vectors, plus the dose tertile
cuts per scored set. store (laptop, where the caption files are): the memory caption store (members[0]'s first
Karpathy sentence) and the block's reference subset; never committed, sha-recorded at staging, deleted with the block.
"""
from __future__ import annotations

import argparse
import json
import os
import sys
import tempfile
from collections import Counter
from pathlib import Path

import numpy as np

HERE = Path(__file__).resolve().parent
sys.path[:0] = [str(HERE), str(HERE.parents[1] / "scripts/c_stage1")]
import build_memory as BM  # noqa: E402  stage-1 module, unchanged: near, clusters, exemplars, the rule constants
import cen_fetch as F  # noqa: E402

C = BM.C
SCHEMA = "vsps.c_en.v1"
PROTECTED = ("coco_test", "nocaps_val", "coco_kval")  # §4 step 4
TEST_SETS = ("coco_test", "nocaps_val")
SCORED = {"coco_test_5000": "coco_test", "nocaps_val_4500": "nocaps_val", "nocaps_val_3500": "nocaps_val"}
VG1000 = f"{F.PDIR}/cen_nocaps_vg1000.txt"
SMOKE_N = 16  # CC-113 r5 smoke check, memory images only
for _s in TEST_SETS:
    C.DATASETS[_s] = {"src": "coco" if _s == "coco_test" else "nocaps", "image_dir": f"cen_{_s}/images"}
C.DATASETS["smoke"] = {"src": "coco", "image_dir": "cen_memory/images"}


def scored_ids(name: str, root: Path = F.ROOT) -> list[int]:
    """The pinned order of a scored set: the list order (ascending id); the 3,500 is the 4,500 minus vg1000."""
    ids = [r[0] for r in F.load_list(SCORED[name], root)]
    if name != "nocaps_val_3500":
        return ids
    sums = dict(reversed(x.split(maxsplit=1)) for x in (root / F.SUMS).read_text().splitlines() if x)
    if F.sha_file(root / VG1000) != sums.get(VG1000):
        raise SystemExit(f"{VG1000}: not at its SHA256SUMS line")
    drop = {int(x) for x in (root / VG1000).read_text().split()}
    out = [i for i in ids if i not in drop]
    if len(drop) != 1000 or len(out) != 3500:
        raise SystemExit("nocaps_val_3500: not 4,500 minus the 1,000")
    return out


def feats_of(z) -> dict:
    return {"sha": [str(x) for x in z["sha"]], **{k: np.asarray(z[k]) for k in BM.ROW_KEYS if k != "sha"}}


# ------------------------------------------------------------------------------------------------ build (CPU)
def build(ids: list[int], files: dict[int, str], mem: dict, vecs: np.ndarray, unreadable: set[int],
          protect: dict[str, dict]) -> tuple[dict, np.ndarray]:
    """(memory record, cluster vectors). ids, mem rows and vecs share one order."""
    if len(ids) != len(mem["sha"]) or len(ids) != len(vecs):
        raise SystemExit("the feature and vector files are not one memory")
    near_by = {s: BM.near(mem, f) for s, f in protect.items()}
    gone = np.array([i in unreadable for i in ids]) | ~np.isfinite(mem["sscd"]).all(1) | ~vecs.any(1)
    near_any = np.zeros(len(ids), bool)
    for m in near_by.values():
        near_any |= m
    keep = np.flatnonzero(~(gone | near_any))
    roots = BM.clusters(BM.subset(mem, keep))
    by: dict[int, list] = {}
    for n, r in zip(keep, roots):
        by.setdefault(r, []).append([ids[n], files[ids[n]], mem["sha"][n]])
    groups = sorted((sorted(g) for g in by.values()), key=lambda g: g[0][0])
    memory = [{"cid": f"e{n:06d}", "members": g} for n, g in enumerate(groups)]
    pos = {i: n for n, i in enumerate(ids)}
    cvec = np.stack([vecs[pos[m["members"][0][0]]] for m in memory]) if memory else np.zeros((0, vecs.shape[1]))
    rec = {"schema": SCHEMA, "rule": {"hash_max": BM.HASH_MAX, "sscd_min": BM.SSCD_MIN, "near_cos": BM.NEAR_COS,
                                      "mirrored": True, "byte_identical": True},
           "memory": memory,
           "counts": {"recorded": len(ids), "unreadable": int(gone.sum()),
                      "near_dropped": {s: int(m.sum()) for s, m in near_by.items()},
                      "near_dropped_any": int((near_any & ~gone).sum()), "kept": len(keep),
                      "clusters": len(memory), "cluster_sizes": dict(Counter(len(m["members"]) for m in memory))}}
    return rec, cvec


def cmd_build(a) -> None:
    F.host_ok(a.expect_head)
    rows = F.load_list("memory")
    files = {r[0]: r[1] for r in rows}
    e, f = np.load(a.emb), np.load(a.feats)
    ids = [int(x) for x in e["ids"]]
    if ids != [int(x) for x in f["ids"]]:
        raise SystemExit("embeddings and features are not in one order")
    protect = {}
    for spec in a.protect:
        s, p = spec.split("=", 1)
        protect[s] = feats_of(np.load(p))
    if set(protect) != set(PROTECTED):
        raise SystemExit(f"the near-duplicate pass needs exactly {PROTECTED}")
    unread = {int(x) for x in f["unreadable"]} | set(json.loads(str(e["meta"]))["unreadable"])
    rec, cvec = build(ids, files, feats_of(f), np.asarray(e["vecs"], np.float32), unread, protect)
    refused = F.read_rec(F.REC_DIR / "memory.refused.tsv")
    rec["counts"] |= {"candidates_train_restval": 113287, "allowed": 112322, "fetch_refused": len(refused)}
    rec["inputs_sha256"] = {Path(p).name: F.sha_file(Path(p)) for p in [a.emb, a.feats] +
                            [x.split("=", 1)[1] for x in a.protect]} | {
        "memory.refused.tsv": F.sha_file(F.REC_DIR / "memory.refused.tsv")}
    out = a.out_dir
    (out / "cen_memory.json").write_text(json.dumps(rec) + "\n", encoding="utf-8")
    np.savez(out / "cen_memory_emb.npz", keys=np.array([m["cid"] for m in rec["memory"]]), vecs=cvec,
             meta=json.dumps({"memory_sha256": F.sha_file(out / "cen_memory.json"), "head": F.HEAD_AT_RUN}))
    for n in ("cen_memory.json", "cen_memory_emb.npz"):
        Path(str(out / n) + ".sha256").write_text(f"{F.sha_file(out / n)}  {n}\n")
    print(json.dumps(rec["counts"]))


# ------------------------------------------------------------------------------------------------ exemplars (CPU)
def exemplars(ds: str, mem_keys: list[str], mem_vecs: np.ndarray, q_ids: list[int], q_vecs: np.ndarray,
              scored: dict[str, list[int]]) -> dict:
    ex = BM.exemplars(mem_keys + [f"{ds}|{i}" for i in q_ids], np.concatenate([mem_vecs, q_vecs]))
    ex = {k: ({ds: v[ds]} if isinstance(v, dict) and ds in v else v) for k, v in ex.items()}
    cuts = {n: [float(x) for x in np.quantile([ex["ret"][ds][str(i)][0][1] for i in ids], [1 / 3, 2 / 3])]
            for n, ids in scored.items()}
    return {**ex, "scored_dose_cuts": cuts}


def cmd_exemplars(a) -> None:
    F.host_ok(a.expect_head)
    m = np.load(a.memory_emb)
    meta_m = json.loads(str(m["meta"]))
    if meta_m["memory_sha256"] != F.sha_file(a.memory):
        raise SystemExit("the memory vectors are not this memory's")
    q = np.load(a.query_emb) if a.set != "smoke" else None
    meta_q = json.loads(str(q["meta"])) if q is not None else {}
    keys, mv = [str(k) for k in m["keys"]], np.asarray(m["vecs"])
    if a.set == "smoke":  # CC-113 r5: memory images queried against the memory; the near cut removes themselves
        ex = exemplars("smoke", keys, mv, keys[:SMOKE_N], mv[:SMOKE_N], {})
    else:
        q_ids = [int(x) for x in q["ids"]]
        if meta_q["set"] != a.set or q_ids != [r[0] for r in F.load_list(a.set)]:
            raise SystemExit("the query vectors are not this set's, in the pinned list order")
        ex = exemplars(a.set, keys, mv, q_ids, np.asarray(q["vecs"]),
                       {n: scored_ids(n) for n, s in SCORED.items() if s == a.set})
    rec = {"schema": SCHEMA, "set": a.set, "memory_sha256": meta_m["memory_sha256"],
           "emb_sha256": {"memory": F.sha_file(a.memory_emb)} | ({a.set: F.sha_file(a.query_emb)} if q is not None
                                                                  else {}),
           "near_cos": BM.NEAR_COS, **ex}
    out = Path(a.out)
    out.write_text(json.dumps(rec) + "\n", encoding="utf-8")
    Path(str(out) + ".sha256").write_text(f"{F.sha_file(out)}  {out.name}\n")
    print(json.dumps({"set": a.set, "scored_dose_cuts": ex["scored_dose_cuts"]}))


# ------------------------------------------------------------------------------------------------ store (laptop)
def memory_captions(memory: dict, kar: list[dict]) -> dict[str, str]:
    """{cid: members[0]'s first Karpathy sentence, whitespace normalised} (decode_icl.memory_captions' rule)."""
    first = {i["cocoid"]: i["sentences"][0]["raw"] for i in kar if i["split"] in ("train", "restval")}
    return {m["cid"]: " ".join(first[m["members"][0][0]].split()) for m in memory["memory"]}


def coco_refs(kar: list[dict], ids: list[int]) -> dict[str, list[str]]:
    """The first 5 sentences in Karpathy order (crosslingual_gap.py's English rule)."""
    by = {i["cocoid"]: i for i in kar}
    return {str(i): [s["raw"].strip() for s in by[i]["sentences"][:5]] for i in ids}


def nocaps_refs(cap: dict, ids: list[int]) -> dict[str, list[str]]:
    """All 10 references per image, as released."""
    out: dict[str, list[str]] = {}
    for a in cap["annotations"]:
        out.setdefault(str(a["image_id"]), []).append(a["caption"].strip())
    if set(out) != {str(i) for i in ids} or any(len(v) != 10 for v in out.values()):
        raise SystemExit("NoCaps val: not 10 references for each of the 4,500 images")
    return {str(i): out[str(i)] for i in ids}


def cmd_store(a) -> None:
    if os.environ.get("VSPS_MACHINE_ID") or Path("/root/.vsps_machine_id").exists():
        raise SystemExit("store runs on the laptop, where the caption files are; never on a GPU host")
    if a.what == "nocaps_val":
        if F.sha_file(a.captions) != F.NOCAPS_CAPTIONS_SHA256:
            raise SystemExit("the NoCaps captions file differs from 2e8071fc")
        body = {"refs": nocaps_refs(json.loads(a.captions.read_text(encoding="utf-8")),
                                    [r[0] for r in F.load_list("nocaps_val")])}
        src = F.NOCAPS_CAPTIONS_SHA256
    else:
        kar = json.loads(F.pinned("karpathy").read_text(encoding="utf-8"))["images"]
        src = F.INPUTS["karpathy"][1]
        if a.what == "memory":
            mem = json.loads(a.memory.read_text(encoding="utf-8"))
            body = {"memory_sha256": F.sha_file(a.memory), "captions": memory_captions(mem, kar)}
        else:
            body = {"refs": coco_refs(kar, [r[0] for r in F.load_list("coco_test")])}
    out = Path(a.out)
    out.write_text(json.dumps({"schema": SCHEMA, "what": a.what, "release_sha256": src, **body},
                              ensure_ascii=False) + "\n", encoding="utf-8")
    n = len(body.get("refs") or body.get("captions"))
    print(json.dumps({"what": a.what, "file": out.name, "sha256": F.sha_file(out), "keys": n}))


# ------------------------------------------------------------------------------------------------ self-test (CPU)
def selftest() -> None:
    far = 0xFFFFFFFF00000000
    ids = [30, 10, 20, 40, 50]
    mem = BM.fake_feats(["a", "b", "c", "d", "e"], [0, 1, far, 0xF0F0F0F0F0F0F0F0, 0x0F0F0F0F00000000],
                     [[1, 0, 0], [1, 0.01, 0], [0, 1, 0], [0, 0, 1], [0.6, 0.8, 0]])
    vecs = np.eye(5, 4, dtype=np.float32)
    vecs[4] = 0  # an image SigLIP2 could not open
    prot = {"coco_test": BM.fake_feats(["t"], [0xF0F0F0F0F0F0F0F1], [[0, 0, 1]]),
            "nocaps_val": BM.fake_feats(["n"], [far], [[0.0, 0.0, -1.0]]), "coco_kval": BM.fake_feats(["k"], [far], [[0, 0, -1]])}
    files = {i: f"COCO_train2014_{i:012d}.jpg" for i in ids}
    rec, cvec = build(ids, files, mem, vecs, set(), prot)
    assert rec["counts"]["near_dropped"]["coco_test"] == 1 and rec["counts"]["unreadable"] == 1, rec["counts"]
    assert [[x[0] for x in m["members"]] for m in rec["memory"]] == [[10, 30], [20]], "clusters by smallest cocoid"
    assert [m["cid"] for m in rec["memory"]] == ["e000000", "e000001"] and np.array_equal(cvec[0], vecs[1])
    keys = [f"e{n:06d}" for n in range(12)]
    rng = np.random.default_rng(0)
    mv = rng.normal(size=(12, 8)).astype(np.float32)
    qv = rng.normal(size=(3, 8)).astype(np.float32)
    qv[0] = mv[0] + 1e-3
    mv /= np.linalg.norm(mv, axis=1, keepdims=True)
    qv /= np.linalg.norm(qv, axis=1, keepdims=True)
    ex = exemplars("coco_test", keys, mv, [7, 8, 9], qv, {"coco_test_5000": [7, 8, 9]})
    assert "e000000" not in [c for c, _ in ex["ret"]["coco_test"]["7"]] and len(ex["rand"]["coco_test"]["8"]) == 8
    assert ex["n_cut"]["coco_test"]["7"] == 1 and len(ex["scored_dose_cuts"]["coco_test_5000"]) == 2
    assert ex == exemplars("coco_test", keys, mv, [7, 8, 9], qv, {"coco_test_5000": [7, 8, 9]}), "deterministic"
    kar = [{"cocoid": 10, "split": "train", "sentences": [{"raw": " w1  w2 "}, {"raw": "w3"}]},
           {"cocoid": 20, "split": "restval", "sentences": [{"raw": "w4"}]},
           {"cocoid": 5, "split": "test", "sentences": [{"raw": f"r{n} "} for n in range(6)]}]
    assert memory_captions({"memory": [{"cid": "e0", "members": [[10, "f", "s"], [20, "g", "t"]]}]}, kar) == {"e0": "w1 w2"}
    assert coco_refs(kar, [5]) == {"5": [f"r{n}" for n in range(5)]}, "first 5 in Karpathy order"
    cap = {"annotations": [{"image_id": i, "caption": f"c{n}"} for i in (1, 2) for n in range(10)]}
    assert len(nocaps_refs(cap, [1, 2])["2"]) == 10 and F.refuses(lambda: nocaps_refs(cap, [1, 2, 3]))
    with tempfile.TemporaryDirectory() as tmp:
        os.environ["VSPS_MACHINE_ID"] = "x"
        try:
            assert F.refuses(lambda: cmd_store(argparse.Namespace(what="memory", out=Path(tmp) / "x"))), "laptop only"
        finally:
            del os.environ["VSPS_MACHINE_ID"]
    print("selftest ok: near-duplicate drops per protected set (C's rule), unreadable dropped, clusters ordered by "
          "smallest cocoid, members[0] vector, examples (near cut, rand 8, deterministic, dose cuts), shown caption "
          "= members[0]'s first sentence, COCO refs first 5, NoCaps refs 10, store refused on a GPU host")


def main() -> None:
    ap = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    ap.add_argument("--selftest", action="store_true")
    sub = ap.add_subparsers(dest="cmd")
    p = sub.add_parser("build")
    p.add_argument("--emb", type=Path, required=True)
    p.add_argument("--feats", type=Path, required=True)
    p.add_argument("--protect", action="append", default=[], help="SET=feats.npz, for each of " + ", ".join(PROTECTED))
    p.add_argument("--out-dir", type=Path, required=True)
    p.add_argument("--expect-head", required=True)
    p = sub.add_parser("exemplars")
    p.add_argument("--set", choices=TEST_SETS + ("smoke",), required=True)
    for k in ("memory", "memory-emb", "out"):
        p.add_argument(f"--{k}", type=Path, required=True)
    p.add_argument("--query-emb", type=Path, help="the set's SigLIP2 vectors (not for smoke)")
    p.add_argument("--expect-head", required=True)
    p = sub.add_parser("store")
    p.add_argument("--what", choices=("memory", "coco_test", "nocaps_val"), required=True)
    p.add_argument("--memory", type=Path, help="cen_memory.json (mirrored from M3), for --what memory")
    p.add_argument("--captions", type=Path, help="the NoCaps val captions file, for --what nocaps_val")
    p.add_argument("--out", type=Path, required=True)
    a = ap.parse_args()
    if a.selftest:
        return selftest()
    {"build": cmd_build, "exemplars": cmd_exemplars, "store": cmd_store}.get(a.cmd, lambda _a: ap.error("mode?"))(a)


if __name__ == "__main__":
    main()
