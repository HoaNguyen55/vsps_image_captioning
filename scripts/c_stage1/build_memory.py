#!/usr/bin/env python3
"""Paper C stage 1 (EXPLORATORY / DEV): the dev-A lists, the de-duplicated retrieval memory, the SigLIP2 embeddings
and the example ids of every arm. Design: manuscript/prereg/2026-10-22_c_stage1/DESIGN.md §2-§3.

  python scripts/c_stage1/build_memory.py --selftest                               CPU, no data
  python scripts/c_stage1/build_memory.py lists --sscd PT --out lists.json [--protected NAME=DIR ...]   CPU
  python scripts/c_stage1/build_memory.py embed --lists L --snapshot DIR --revision REV --out emb.npz    GPU
  python scripts/c_stage1/build_memory.py exemplars --lists L --emb emb.npz --out exemplars.json        CPU
`lists` reads image files, ids and file names only, never a caption (the OpenViIC annotation files are read for
their keys). Near-duplicates use the registered rule of scripts/match_openviic.py (its _features, _mirror_hashes,
hamming and is_match, imported unchanged): min(pHash, dHash) <= 10 and SSCD cosine >= 0.5, mirrored hashes included.
"""
from __future__ import annotations

import argparse
import hashlib
import json
import random
import re
import sys
import tempfile
from pathlib import Path

import numpy as np

sys.path.insert(0, str(Path(__file__).resolve().parent))
import decode_icl as C  # noqa: E402  pins, refusal, manifests
import match_openviic as MO  # noqa: E402  committed matcher (scripts/ is on the path via decode_icl)

HASH_MAX, SSCD_MIN = 10, 0.5  # the registered rule (dev-pools DESIGN §5)
NEAR_COS = 0.92  # retrieval-time cut: a memory image this close to the query is never shown, in any arm
N_EX = 8  # examples kept per image; k = 2 and 4 are prefixes
SIGLIP2 = "google/siglip2-so400m-patch14-384"
RESEARCH_OK = {"apache-2.0", "mit", "bsd-2-clause", "bsd-3-clause", "cc-by-4.0", "cc-by-nc-4.0"}  # C2 (CC-079)


def need_licence(licence: str, what: str) -> None:
    """C2: stop unless the licence permits research use."""
    if licence.strip().lower() not in RESEARCH_OK:
        raise SystemExit(f"{what}: licence {licence!r} is not on the research-use list; return to the judge")


def card_licence(readme: Path) -> str:
    """The `license:` value of a model card's YAML front matter ('' if absent)."""
    text = readme.read_text(encoding="utf-8")
    front = text.split("---", 2)[1] if text.startswith("---") else ""
    hit = re.search(r"^license:\s*(\S+)", front, re.M)
    return hit.group(1) if hit else ""


def syl8(text: str) -> set:
    w = re.sub(r"[^\w\s]", " ", text.lower()).split()
    return {tuple(w[n:n + 8]) for n in range(len(w) - 7)}


def caption_hits(text: str, captions: list[str]) -> int:
    """C3: syllable 8-grams of `text` found in any caption (a count only)."""
    grams = set().union(*map(syl8, captions)) if captions else set()
    return len(syl8(text) & grams)


def dataset_captions(data: Path) -> list[str]:
    """KTVIC train/test and OpenViIC train/dev/test captions, read only for the C3 scan."""
    out = [a["caption"] for s in ("train", "test")
           for a in json.loads((data / f"ktvic/{s}_data.json").read_text(encoding="utf-8"))["annotations"]]
    for s in ("train", "dev", "test"):
        ann = json.loads((data / f"openviic/uit-openviic-annotation-{s}.json").read_text(encoding="utf-8"))
        out += [c for v in ann.values() for c in v["captions"]]
    return out


def order_key(tag: str, image_sha: str) -> str:
    return hashlib.sha256(f"paperC|{tag}|{image_sha}".encode()).hexdigest()


def split(rows: list, tag: str, first: int) -> tuple[list, list]:
    """Rows (id, file, sha) ordered by sha256("paperC|tag|image sha"); the first `first` rows, then the rest."""
    rows = sorted(rows, key=lambda r: (order_key(tag, r[2]), r[0]))
    return rows[:first], rows[first:]


# ------------------------------------------------------------------------------------------------ near-duplicates
def near(fx: dict, fy: dict, chunk: int = 512) -> np.ndarray:
    """Boolean (len x) mask: x has a near-duplicate in y under the registered rule (x's mirrored hashes count)."""
    hit = np.zeros(len(fx["sha"]), bool)
    if not len(fy["sha"]):
        return hit
    ye = np.nan_to_num(fy["sscd"])
    for lo in range(0, len(hit), chunk):
        r = slice(lo, lo + chunk)
        sim = np.nan_to_num(fx["sscd"][r]) @ ye.T
        ph = np.minimum(MO.hamming(fx["phash"][r], fy["phash"]), MO.hamming(fx["phash_m"][r], fy["phash"]))
        dh = np.minimum(MO.hamming(fx["dhash"][r], fy["dhash"]), MO.hamming(fx["dhash_m"][r], fy["dhash"]))
        same = np.array(fx["sha"][r])[:, None] == np.array(fy["sha"])[None, :]
        hit[r] = (((np.minimum(ph, dh) <= HASH_MAX) & (sim >= SSCD_MIN)) | same).any(1)
    return hit


def clusters(f: dict, chunk: int = 512) -> list[int]:
    """Union-find root of every row, joining rows that are near-duplicates (or byte-identical) of each other."""
    n = len(f["sha"])
    root = list(range(n))

    def find(a):
        while root[a] != a:
            root[a] = root[root[a]]
            a = root[a]
        return a

    e = np.nan_to_num(f["sscd"])
    for lo in range(0, n, chunk):
        r = slice(lo, lo + chunk)
        sim = e[r] @ e.T
        ph = np.minimum(MO.hamming(f["phash"][r], f["phash"]), MO.hamming(f["phash_m"][r], f["phash"]))
        dh = np.minimum(MO.hamming(f["dhash"][r], f["dhash"]), MO.hamming(f["dhash_m"][r], f["dhash"]))
        same = np.array(f["sha"][r])[:, None] == np.array(f["sha"])[None, :]
        for a, b in zip(*np.nonzero(((np.minimum(ph, dh) <= HASH_MAX) & (sim >= SSCD_MIN)) | same)):
            ra, rb = find(lo + a), find(b)
            if ra != rb:
                root[max(ra, rb)] = min(ra, rb)
    return [find(i) for i in range(n)]


def subset(f: dict, idx) -> dict:
    """Rows idx (integer positions) of a feature dict."""
    idx = np.asarray(idx, int)
    return {k: (np.asarray(v)[idx] if k != "sha" else [v[i] for i in idx]) for k, v in f.items()}


def concat(*fs: dict) -> dict:
    return {k: ([x for f in fs for x in f[k]] if k == "sha" else np.concatenate([f[k] for f in fs])) for k in fs[0]}


# ------------------------------------------------------------------------------------------------ lists (CPU)
def features(paths: list[Path], sscd: str, workers: int = 4) -> dict:
    """pHash, dHash, their mirrored versions, SSCD descriptor and file sha256 of each image (match_openviic code)."""
    from multiprocessing import Pool

    import torch

    model = torch.jit.load(sscd).eval()
    out = {"sha": [C.lb.sha256_file(p) for p in paths]}
    n = len(paths)
    for k in ("phash", "dhash", "phash_m", "dhash_m"):
        out[k] = np.zeros(n, np.uint64)
    out["sscd"] = np.full((n, 512), np.nan, np.float32)
    # ponytail: one pass without a feature cache (about 1-2 CPU-h); add a cache if the build is ever repeated
    with Pool(workers) as pool, torch.inference_mode():
        for i, (f, m) in enumerate(zip(pool.imap(MO._features, map(str, paths), 16),
                                       pool.imap(MO._mirror_hashes, map(str, paths), 16))):
            if isinstance(f[1], str):
                raise SystemExit(f"unreadable image {paths[i]}: {f[1]}")
            out["phash"][i], out["dhash"][i], (out["phash_m"][i], out["dhash_m"][i]) = f[0], f[1], m
            out["sscd"][i] = model(torch.from_numpy(f[3])[None])[0].numpy()
    return out


def cmd_lists(a) -> None:
    need_licence(a.sscd_licence, "SSCD weights")
    data = C.lb.DATA / "datasets"
    root = Path(C.ROOT)
    C.pinned(C.DESIGN)
    kt = {s: json.loads((data / f"ktvic/{s}_data.json").read_text(encoding="utf-8"))["images"]
          for s in ("train", "test")}
    dev300 = set((root / "data/splits/ktvic_dev300.txt").read_text(encoding="utf-8").split())
    ov = {s: sorted(json.loads((data / f"openviic/uit-openviic-annotation-{s}.json").read_text(encoding="utf-8")))
          for s in ("train", "dev", "test")}
    xm = json.loads((data / "xm3600/full_data.json").read_text(encoding="utf-8"))["images"]
    xm600 = {str(i["id"]) for i in json.loads((data / "xm3600/test_data.json").read_text(encoding="utf-8"))["images"]}

    groups = {  # name -> [(id, file, path)]
        "kt_mem": [(str(i["id"]), i["filename"], data / "ktvic/images" / i["filename"]) for i in kt["train"]
                   if str(i["id"]) not in dev300],
        "kt_dev300": [(str(i["id"]), i["filename"], data / "ktvic/images" / i["filename"]) for i in kt["train"]
                      if str(i["id"]) in dev300],
        "kt_test": [(str(i["id"]), i["filename"], data / "ktvic/images" / i["filename"]) for i in kt["test"]],
        "xm_all": [(str(i["id"]), i["filename"], data / "xm3600/images" / i["filename"]) for i in xm],
        **{f"ov_{s}": [(f, f, data / "openviic/images" / f) for f in ov[s]] for s in ("train", "dev", "test")},
    }
    for spec in a.protected:  # e.g. COCO test images present on this machine
        name, folder = spec.split("=", 1)
        groups[f"extra_{name}"] = [(p.name, p.name, p) for p in sorted(Path(folder).iterdir()) if p.is_file()]
    feats = {g: features([p for *_x, p in rows], a.sscd) for g, rows in groups.items()}
    rows = {g: [(i, f, feats[g]["sha"][n]) for n, (i, f, _p) in enumerate(groups[g])] for g in groups}

    a_raw, b_raw = split(rows["ov_dev"], "ovdev", len(rows["ov_dev"]) // 2)
    xm_dev, xm_test = split([r for r in rows["xm_all"] if r[0] not in xm600], "xm", 500)
    pos = {r[0]: n for n, r in enumerate(rows["ov_dev"])}
    fa = subset(feats["ov_dev"], [pos[r[0]] for r in a_raw])
    fb = subset(feats["ov_dev"], [pos[r[0]] for r in b_raw])
    tests = concat(*(feats[g] for g in feats if g in ("kt_test", "ov_test", "xm_all") or g.startswith("extra_")))
    _ids, hashes = C.refused({"refuse": {"openviic_files": [], "image_sha256": []}})
    hit_a = near(fa, concat(tests, feats["kt_dev300"], fb)) | np.isin(fa["sha"], list(hashes))
    hit_b = near(fb, concat(tests, feats["kt_dev300"])) | np.isin(fb["sha"], list(hashes))
    dev_a = [r for r, h in zip(a_raw, hit_a) if not h]
    dev_b = [r for r, h in zip(b_raw, hit_b) if not h]

    mem_f = concat(feats["kt_mem"], feats["ov_train"])
    mem_rows = [("ktvic", *r) for r in rows["kt_mem"]] + [("openviic", *r) for r in rows["ov_train"]]
    protected = concat(tests, feats["kt_dev300"], feats["ov_dev"])
    drop = near(mem_f, protected) | np.isin(mem_f["sha"], list(hashes))
    keep = np.flatnonzero(~drop)
    roots = clusters(subset(mem_f, keep))
    by_root: dict[int, list] = {}
    for n, r in zip(keep, roots):
        by_root.setdefault(r, []).append(list(mem_rows[n]))
    memory = [{"cid": f"m{n:05d}", "members": sorted(ms)} for n, ms in enumerate(sorted(by_root.values(), key=min))]

    ov_test, ov_b = rows["ov_test"], b_raw
    lists = {
        "schema": "vsps.c_stage1_lists.v1", "label": C.LABEL, "design_sha256": C.PINS[C.DESIGN],
        "rule": {"near_duplicate": f"min(pHash, dHash) <= {HASH_MAX} and SSCD >= {SSCD_MIN}, mirrored hashes "
                                   "included, or byte-identical (scripts/match_openviic.py)",
                 "split_ov_dev": "sha256('paperC|ovdev|'+image sha256) order: first half A, rest B; filter after",
                 "split_xm": "XM3600 minus XM600, sha256('paperC|xm|'+image sha256) order: first 500 dev, rest test"},
        "sscd": {"path_name": Path(a.sscd).name, "sha256": C.lb.sha256_file(Path(a.sscd)), "source_url": a.sscd_url,
                 "licence": a.sscd_licence},
        "matcher_sha256": C.lb.sha256_file(Path(MO.__file__)),
        "sets": {"ov_dev_a": dev_a, "ov_dev_b": dev_b, "xm_dev500": xm_dev, "xm_test2500": xm_test},
        "refuse": {"openviic_files": sorted({r[0] for r in ov_test + ov_b}),
                   "image_sha256": sorted({r[2] for r in ov_test + ov_b + rows["xm_all"]})},
        "memory": memory,
        "counts": {"ov_dev_a_raw": len(a_raw), "ov_dev_a": len(dev_a), "ov_dev_b_raw": len(b_raw),
                   "ov_dev_b": len(dev_b), "memory_candidates": len(mem_rows), "memory_dropped": int(drop.sum()),
                   "memory_images": len(keep), "memory_clusters": len(memory),
                   "groups": {g: len(r) for g, r in rows.items()}},
    }
    hits = caption_hits(json.dumps(lists, ensure_ascii=False), dataset_captions(data))
    if hits:
        raise SystemExit(f"C3: lists.json would hold {hits} caption 8-gram(s); not written")
    lists["caption_8gram_hits"] = 0
    Path(a.out).write_text(json.dumps(lists, ensure_ascii=False, indent=0) + "\n", encoding="utf-8")
    print(json.dumps(lists["counts"]))


# ------------------------------------------------------------------------------------------------ embed (GPU)
def cmd_embed(a) -> None:
    import torch
    from PIL import Image
    from transformers import AutoModel, AutoProcessor

    if len(a.revision) != 40:
        raise SystemExit("--revision must be the 40-hex commit of the SigLIP2 snapshot")
    licence = card_licence(Path(a.snapshot) / "README.md")
    need_licence(licence, f"{SIGLIP2} model card")
    lists = C.load_lists(a.lists)
    jobs = [(f"{ds}|{i}", C.lb.DATA / "datasets" / C.DATASETS[ds]["image_dir"] / f, h)
            for ds in C.DATASETS for i, f, h in C.manifest(ds, lists)]  # manifest() refuses test and dev-B rows
    folder = {"ktvic": "ktvic/images", "openviic": "openviic/images"}
    jobs += [(m["cid"], C.lb.DATA / "datasets" / folder[m["members"][0][0]] / m["members"][0][2], m["members"][0][3])
             for m in lists["memory"]]
    proc = AutoProcessor.from_pretrained(a.snapshot)
    net = AutoModel.from_pretrained(a.snapshot, torch_dtype=torch.float16).eval().cuda()
    vecs = []
    for lo in range(0, len(jobs), 64):
        ims = []
        for _k, p, h in jobs[lo:lo + 64]:
            if C.lb.sha256_file(p) != h:
                raise SystemExit(f"{p}: sha256 differs from lists.json")
            ims.append(Image.open(p).convert("RGB"))
        with torch.no_grad():
            v = net.get_image_features(**proc(images=ims, return_tensors="pt").to("cuda", torch.float16)).float()
        vecs.append(torch.nn.functional.normalize(v, dim=-1).cpu().numpy())
    meta = {"model": SIGLIP2, "revision": a.revision, "licence": licence,
            "readme_sha256": C.lb.sha256_file(Path(a.snapshot) / "README.md"),
            "lists_sha256": C.lb.sha256_file(a.lists),
            "snapshot_sha256": {p.name: C.lb.sha256_file(p) for p in sorted(Path(a.snapshot).iterdir()) if p.is_file()},
            "design_sha256": C.PINS[C.DESIGN], "label": C.LABEL}
    np.savez(a.out, keys=np.array([k for k, _p, _h in jobs]), vecs=np.concatenate(vecs), meta=json.dumps(meta))
    Path(str(a.out) + ".sha256").write_text(f"{C.lb.sha256_file(Path(a.out))}  {Path(a.out).name}\n")


# ------------------------------------------------------------------------------------------------ exemplars (CPU)
def seed(*parts: str) -> int:
    return int(hashlib.sha256("|".join(("paperC", *parts)).encode()).hexdigest()[:8], 16)


def exemplars(keys: list[str], vecs: np.ndarray) -> dict:
    """Retrieval top-N_EX by cosine (ties by cluster id), random N_EX per image and one fixed N_EX per dataset; a
    cluster at cosine >= NEAR_COS to an image is never shown to it, in any arm."""
    mem = [n for n, k in enumerate(keys) if "|" not in k]
    cids = [keys[n] for n in mem]
    out = {"ret": {}, "rand": {}, "fix": {}, "n_cut": {}}
    for ds in C.DATASETS:
        q = [n for n, k in enumerate(keys) if k.startswith(ds + "|")]
        if not q:
            continue
        cos = vecs[q] @ vecs[mem].T
        out["ret"][ds], out["rand"][ds], out["n_cut"][ds] = {}, {}, {}
        for row, n in zip(cos, q):
            qid = keys[n].split("|", 1)[1]
            ok = [j for j in np.lexsort((cids, -row)) if row[j] < NEAR_COS]
            out["ret"][ds][qid] = [[cids[j], round(float(row[j]), 6)] for j in ok[:N_EX]]
            out["rand"][ds][qid] = random.Random(seed("rand", ds, qid)).sample(sorted(cids[j] for j in ok), N_EX)
            out["n_cut"][ds][qid] = int((row >= NEAR_COS).sum())
        safe = sorted(cids[j] for j in np.flatnonzero(cos.max(0) < NEAR_COS))
        out["fix"][ds] = random.Random(seed("fix", ds)).sample(safe, N_EX)
    return out


def cmd_exemplars(a) -> None:
    C.load_lists(a.lists)
    z = np.load(a.emb)
    meta = json.loads(str(z["meta"]))
    if meta["lists_sha256"] != C.lb.sha256_file(a.lists) or meta["design_sha256"] != C.PINS[C.DESIGN]:
        raise SystemExit("the embeddings were not built from this lists.json under this design")
    ex = {"design_sha256": C.PINS[C.DESIGN], "lists_sha256": meta["lists_sha256"], "label": C.LABEL,
          "emb_sha256": C.lb.sha256_file(Path(a.emb)), "siglip2": {k: meta[k] for k in ("model", "revision")},
          "near_cos": NEAR_COS, **exemplars([str(k) for k in z["keys"]], z["vecs"])}
    Path(a.out).write_text(json.dumps(ex) + "\n", encoding="utf-8")
    Path(str(a.out) + ".sha256").write_text(f"{C.lb.sha256_file(Path(a.out))}  {Path(a.out).name}\n")


# ------------------------------------------------------------------------------------------------ self-test (CPU)
def fake_feats(sha: list[str], ph: list[int], vec: list[list[float]]) -> dict:
    v = np.array(vec, np.float32)
    v /= np.linalg.norm(v, axis=1, keepdims=True)
    h = np.array(ph, np.uint64)
    return {"sha": sha, "phash": h, "dhash": h, "phash_m": h ^ np.uint64(0xFFFF), "dhash_m": h ^ np.uint64(0xFFFF),
            "sscd": v}


def selftest() -> None:
    rows = [(str(i), f"{i}.jpg", hashlib.sha256(str(i).encode()).hexdigest()) for i in range(11)]
    a, b = split(rows, "ovdev", 5)
    assert (a, b) == split(list(reversed(rows)), "ovdev", 5) and not {r[0] for r in a} & {r[0] for r in b}
    assert len(a) == 5 and len(a) + len(b) == 11, "the split is deterministic, disjoint and complete"
    far, alt = 0xFFFFFFFF00000000, 0xAAAAAAAAAAAAAAAA
    x = fake_feats(["s0", "s1", "s2", "s3"], [0, 0, 0xFFFF, far], [[1, 0], [0, 1], [1, 0.01], [1, 0]])
    y = fake_feats(["t0", "t1"], [3, 0xFFFFFFFFFFFF0000], [[1, 0.02], [0, 1]])
    # x0: hashes 2 bits from y0 and SSCD ~1, a copy; x1: hashes close to y0 but SSCD ~0; x2: only its mirrored
    # hashes are close to y0; x3: hashes far from both
    assert near(x, y).tolist() == [True, False, True, False]
    assert subset(x, [2, 0])["sha"] == ["s2", "s0"] and subset(x, [2, 0])["phash"].tolist() == [0xFFFF, 0]
    assert near(x, fake_feats(["s3"], [alt], [[0, 1]])).tolist() == [False, False, False, True], "byte-identical"
    roots = clusters(fake_feats(["a", "b", "c", "a"], [0, 1, far, 7], [[1, 0], [1, 0.01], [0, 1], [0.3, 1]]))
    assert roots == [0, 0, 2, 0], roots
    keys = ["ov_dev_a|q1", "ov_dev_a|q2"] + [f"m{n:05d}" for n in range(12)]
    rng = np.random.default_rng(0)
    vecs = rng.normal(size=(len(keys), 16)).astype(np.float32)
    vecs[2] = vecs[0] + 1e-3  # m00000 is a near copy of q1
    vecs /= np.linalg.norm(vecs, axis=1, keepdims=True)
    ex = exemplars(keys, vecs)
    for arm in ("ret", "rand"):
        assert "m00000" not in [c if isinstance(c, str) else c[0] for c in ex[arm]["ov_dev_a"]["q1"]]
        assert len(ex[arm]["ov_dev_a"]["q2"]) == N_EX
    assert "m00000" not in ex["fix"]["ov_dev_a"] and len(ex["fix"]["ov_dev_a"]) == N_EX
    cos = [c for _cid, c in ex["ret"]["ov_dev_a"]["q2"]]
    assert cos == sorted(cos, reverse=True) and ex == exemplars(keys, vecs) and ex["n_cut"]["ov_dev_a"]["q1"] == 1
    # C2 and C3, on text written for this test
    assert caption_hits("một hai ba bốn năm sáu bảy tám chín", ["không một hai ba bốn năm sáu bảy tám"]) == 1
    assert caption_hits('{"id": "00000000782.jpg", "sha": "ab12"}', ["một hai ba bốn năm sáu bảy tám"]) == 0
    assert C.refuses(lambda: need_licence("other", "x")) and not C.refuses(lambda: need_licence("Apache-2.0", "x"))
    with tempfile.TemporaryDirectory() as tmp:
        (Path(tmp) / "README.md").write_text("---\nlicense: apache-2.0\ntags: [x]\n---\n# card\n")
        assert card_licence(Path(tmp) / "README.md") == "apache-2.0"
        (Path(tmp) / "README.md").write_text("# card without front matter\nlicense: mit\n")
        assert card_licence(Path(tmp) / "README.md") == "", "only the front matter counts"
        lp, _ep, _lists = C.fake_lists(Path(tmp))
        assert C.refuses(lambda: C.load_lists(lp)) or C.LISTS_SHA256 is not None
    print("selftest ok: split, near-duplicate rule (mirror, byte-identical), clusters, examples, near cut, C2, C3")


def main() -> None:
    ap = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    ap.add_argument("--selftest", action="store_true")
    sub = ap.add_subparsers(dest="cmd")
    p = sub.add_parser("lists")
    p.add_argument("--sscd", required=True, help="sscd_disc_mixup.torchscript.pt")
    p.add_argument("--sscd-url", required=True, help="where the weights were downloaded from (C2)")
    p.add_argument("--sscd-licence", required=True, help="the weights' licence, e.g. mit (C2)")
    p.add_argument("--protected", action="append", default=[], help="NAME=DIR of further test images")
    p.add_argument("--out", required=True)
    p = sub.add_parser("embed")
    p.add_argument("--lists", type=Path, required=True)
    p.add_argument("--snapshot", type=Path, required=True)
    p.add_argument("--revision", required=True)
    p.add_argument("--out", required=True)
    p = sub.add_parser("exemplars")
    p.add_argument("--lists", type=Path, required=True)
    p.add_argument("--emb", required=True)
    p.add_argument("--out", required=True)
    a = ap.parse_args()
    if a.selftest:
        return selftest()
    {"lists": cmd_lists, "embed": cmd_embed, "exemplars": cmd_exemplars}.get(a.cmd, lambda _a: ap.error("mode?"))(a)


if __name__ == "__main__":
    main()
