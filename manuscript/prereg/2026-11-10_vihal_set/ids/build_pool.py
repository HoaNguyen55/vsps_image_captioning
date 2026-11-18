#!/usr/bin/env python3
"""ViHal set, plan v1.1 §2: the corrected image pool, the near-duplicate pass and the pilot draw.

  ~/.venvs/c_stage1_lists/bin/python build_pool.py --sscd PT --caches DIR --work DIR

Reads ids, file names and image bytes only. The KTVIC TRAIN references are read for the stratum count; no caption of
a dev or test split, no model output and no sealed file is read (annotation files of other splits: keys only).
Features and the rule are the registered code, imported unchanged: build_memory.features / near / clusters and
w25.rule (C1 byte match, C2 min(pHash, dHash) <= 10 incl. mirror AND SSCD >= 0.5, C3 SSCD > 0.75).
Images are copied one at a time to --work (ext4) first, so /mnt/d never sees concurrent heavy reads.
"""
from __future__ import annotations

import argparse
import hashlib
import json
import re
import shutil
import sys
import unicodedata
import zipfile
from pathlib import Path

import numpy as np

HERE = Path(__file__).resolve().parent
ROOT = HERE.parents[3]
for d in ("scripts/c_stage1", "scripts/w25", "scripts"):
    sys.path.insert(0, str(ROOT / d))
import build_memory as BM  # noqa: E402
import w25 as W  # noqa: E402

DS = ROOT / "data" / "datasets"
TAG = "vihal-set-v1|"  # order seed, fixed in plan v1 §2
EXPECT = {"train_only": 2335, "minus_dev300": 2154, "minus_shared_file": 2153}  # CC-314 check 3
K1_MIN = 1000
POSITIONS = {"pilot_ids.txt": (0, 20), "training_ids.txt": (20, 30), "pilot2_ids.txt": (30, 50)}
CACHED = {  # owner features already computed by the same code (file name -> sha256 prefix)
    "ktvic_test_558": ("ktvic_test.npz", "cd985050"),
    "openviic_test_2001": ("openviic_test.npz", "f4c79b82"),
    "xm3600_all_3600": ("of_xm3600_all.npz", "10de1a60"),
    "uitviic_test_231": ("uitviic_test.npz", "4f478490"),
    "bdt1_h_t2_739": ("of_h_bdt1_739.npz", "10a49f17"),
    "ktvic_dev299": ("of_ktvic_dev299.npz", "be2b121b"),
    "ktvic_dev300_refused_dup_1": ("of_refused_ktvic_dup.npz", "be9aebfb"),
}
ROWS = ("sha", "phash", "dhash", "phash_m", "dhash_m", "sscd")


def sha_file(p: Path) -> str:
    return hashlib.sha256(p.read_bytes()).hexdigest()


def order_key(name: str) -> str:
    return hashlib.sha256((TAG + name).encode()).hexdigest()


def syllables(text: str) -> list[str]:
    text = unicodedata.normalize("NFC", text).lower().replace("_", " ")
    return re.sub(r"[^\w\s]", " ", text).split()


def has_term(caption: str, terms: list[list[str]]) -> bool:
    s = syllables(caption)
    return any(s[i:i + len(t)] == t for t in terms for i in range(len(s) - len(t) + 1))


def id_steps() -> tuple[list[str], dict]:
    """B1: KTVIC-train ids whose every matched OpenViIC copy is in OV train, minus dev300, minus shared OV files."""
    pairs = json.loads((ROOT / "data" / "ktvic_openviic_refs.json").read_text(encoding="utf-8"))["_pairs"]
    train, test = pairs["train"], pairs["test"]
    any_train = [k for k, v in train.items() if any(c[1] == "train" for c in v)]
    only = [k for k, v in train.items() if v and all(c[1] == "train" for c in v)]
    dev = set((ROOT / "data" / "splits" / "ktvic_dev300.txt").read_text().split())
    no_dev = [k for k in only if k not in dev]
    test_files = {c[0] for v in test.values() for c in v}
    shared = [k for k in only if any(c[0] in test_files for c in train[k])]
    keep = [k for k in no_dev if k not in set(shared)]
    counts = {"any_ov_train_copy_v1_figure": len(any_train), "train_only": len(only),
              "dev300_in_train_only": len(only) - len(no_dev), "minus_dev300": len(no_dev),
              "shared_ov_file_with_ktvic_test_in_train_only": len(shared),
              "of_which_left_after_dev300": len(no_dev) - len(keep), "minus_shared_file": len(keep)}
    for k, want in EXPECT.items():
        assert counts[k] == want, f"FAULT: {k} = {counts[k]}, CC-314 says {want}"
    return keep, counts


def staged(names: list[str], src: Path, dst: Path) -> list[Path]:
    """Copy one file at a time from /mnt/d to ext4."""
    dst.mkdir(parents=True, exist_ok=True)
    for n in names:
        if not (dst / n).exists():
            shutil.copyfile(src / n, dst / n)
    return [dst / n for n in names]


def vitextvqa_nontrain(dst: Path) -> list[Path]:
    """Every image of ViTextVQA_images.zip that is not a train image (dev 1,676 + the rest = test by complement)."""
    raw = DS / "vitextvqa_raw"
    train = {i["filename"] for i in json.loads((raw / "ViTextVQA_train.json").read_text(encoding="utf-8"))["images"]}
    dst.mkdir(parents=True, exist_ok=True)
    out = []
    with zipfile.ZipFile(raw / "ViTextVQA_images.zip") as z:
        for info in sorted(z.infolist(), key=lambda i: i.filename):
            name = info.filename.rsplit("/", 1)[-1]
            if info.is_dir() or name in train:
                continue
            if not (dst / name).exists():
                (dst / name).write_bytes(z.read(info))
            out.append(dst / name)
    return out


def feats(paths: list[Path], a) -> dict:
    return BM.features(paths, a.sscd, workers=3, cache=Path(a.work) / "feat_cache", retry_truncated=True)


def cached(caches: Path, name: str, prefix: str) -> tuple[dict, str]:
    sha = sha_file(caches / name)
    assert sha.startswith(prefix), f"FAULT: {name} sha {sha[:8]} != {prefix}"
    z = np.load(caches / name)
    return {k: z[k] for k in ROWS}, sha


def main() -> None:
    ap = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    ap.add_argument("--sscd", required=True)
    ap.add_argument("--caches", required=True)
    ap.add_argument("--work", required=True)
    ap.add_argument("--extra", action="append", default=[], metavar="LABEL=NPZ",
                    help="one more comparison set as a feature file with the same row keys (e.g. OpenViVQA dev)")
    a = ap.parse_args()
    assert sha_file(Path(a.sscd)) == W.SSCD_SHA, "FAULT: SSCD weights sha"
    work = Path(a.work)

    ids, counts = id_steps()
    kt = json.loads((DS / "ktvic" / "train_data.json").read_text(encoding="utf-8"))
    name = {str(i["id"]): i["filename"] for i in kt["images"]}
    pool = feats(staged([name[i] for i in ids], DS / "ktvic" / "images", work / "pool"), a)

    out = np.zeros(len(ids), bool)
    step = {}

    def drop(label: str, mask) -> None:
        mask = np.asarray(mask, bool)
        step[label] = {"hit": int(mask.sum()), "new": int((mask & ~out).sum())}
        out[:] |= mask
        step[label]["left"] = int((~out).sum())

    unreadable = np.zeros(len(ids), bool)
    unreadable[pool["unreadable"]] = True
    drop("unreadable_pool_image", unreadable)
    ex = json.loads((ROOT / "manuscript/prereg/2026-10-21_dev_pools/exclusion.json").read_text())["image_sha256"]
    refused = set().union(*map(set, ex.values()))
    drop("exclusion_json_sha256", [s in refused for s in pool["sha"]])
    drop("byte_twins_3589_7511_4487", [i in {"3589", "7511", "4487"} for i in ids])

    sets, feat_sha = {}, {}
    for label, (f, prefix) in CACHED.items():
        sets[label], feat_sha[label] = cached(Path(a.caches), f, prefix)
    ov_dev = sorted(json.loads((DS / "openviic" / "uit-openviic-annotation-dev.json").read_text(encoding="utf-8")))
    sets["openviic_dev_all"] = feats(staged(ov_dev, DS / "openviic" / "images", work / "ov_dev"), a)
    vt_paths = vitextvqa_nontrain(work / "vt")
    vt = feats(vt_paths, a)
    vt_dev = {i["filename"] for i in json.loads(
        (DS / "vitextvqa_raw" / "ViTextVQA_dev.json").read_text(encoding="utf-8"))["images"]}
    for label, want in (("vitextvqa_dev", True), ("vitextvqa_test_by_complement", False)):
        idx = [j for j, q in enumerate(vt_paths) if (q.name in vt_dev) == want]
        sets[label] = {**BM.subset(vt, idx), "unreadable": sorted(set(idx) & set(vt["unreadable"]))}
    for label, f in (e.split("=", 1) for e in a.extra):
        z = np.load(f)
        sets[label], feat_sha[label] = {k: z[k] for k in ROWS}, sha_file(Path(f))
    w25, before = {}, int(out.sum())
    for label, y in sets.items():
        r = W.rule(pool, y, BM.near)
        w25[label] = {"n": len(y["sha"]), "unreadable": len(y.get("unreadable", [])),
                      **{k: int(v.sum()) for k, v in r.items()}}
        drop("w25_" + label, r["excluded"])
    w25_union = int(out.sum()) - before

    # Inside the pool: keep the first image (in draw order) of every near-duplicate cluster among the survivors.
    alive = [i for i in np.argsort([order_key(name[k]) for k in ids]) if not out[i]]
    sub = {k: (np.asarray(pool[k])[alive] if k != "sha" else [pool["sha"][i] for i in alive]) for k in ROWS}
    roots = BM.clusters(sub)
    later = np.zeros(len(ids), bool)
    for j, r in enumerate(roots):
        later[alive[j]] = r != j  # clusters() roots are the smallest row index = the earliest in draw order
    drop("pool_internal_later_copy", later)

    order = [i for i in alive if not out[i]]
    assert len(order) >= K1_MIN, f"K1: pool {len(order)} < {K1_MIN}"
    assert len(order) == len({pool["sha"][i] for i in order}) and len(order) == int((~out).sum())

    terms = [syllables(t) for t in (HERE.parent / "LEXICON_v1.txt").read_text(encoding="utf-8").splitlines()
             if t.strip() and not t.startswith("#")]
    cult = {str(x["image_id"]) for x in kt["annotations"] if has_term(x["caption"], terms)}
    frame = order[50:]

    def write(fname: str, lines: list[str]) -> None:
        (HERE / fname).write_text("\n".join(lines) + "\n", encoding="utf-8")

    write("pool_trainonly_2153_ids.txt", sorted(ids, key=int))
    write("removed_ids.txt", sorted((ids[i] for i in np.nonzero(out)[0]), key=int))
    write("survivors_ordered.tsv", ["pos\tktvic_id\tfile\timage_sha256"] + [
        f"{p}\t{ids[i]}\t{name[ids[i]]}\t{pool['sha'][i]}" for p, i in enumerate(order, 1)])
    for fname, (lo, hi) in POSITIONS.items():
        write(fname, [ids[i] for i in order[lo:hi]])
    (HERE / "pool_counts.json").write_text(json.dumps({
        "label": "ViHal set plan v1.1 §2: pool, near-duplicate pass, pilot draw (ids and counts only)",
        "rule": "W25 RULE §3 C1|C2|C3 via w25.rule + build_memory.near, unchanged; order = sha256('%s' + file)" % TAG,
        "id_steps": counts, "feature_steps": step, "w25_per_set": w25, "w25_removed_union": w25_union,
        "survivors": len(order), "k1_min": K1_MIN,
        "positions_1_based": {"pilot": "1-20", "training": "21-30", "second_pilot": "31-50", "main_frame": "51-end"},
        "main_frame": {"n": len(frame), "stratum_C": sum(ids[i] in cult for i in frame),
                       "stratum_O": sum(ids[i] not in cult for i in frame)},
        "lexicon_terms": len(terms), "cached_feature_sha256": feat_sha,
        "code_sha256": {"build_memory.py": sha_file(ROOT / "scripts/c_stage1/build_memory.py"),
                        "w25.py": sha_file(ROOT / "scripts/w25/w25.py"),
                        "match_openviic.py": sha_file(ROOT / "scripts/match_openviic.py"), "sscd": W.SSCD_SHA},
        "input_sha256": {"ktvic_openviic_refs.json": sha_file(ROOT / "data/ktvic_openviic_refs.json"),
                         "ktvic_dev300.txt": sha_file(ROOT / "data/splits/ktvic_dev300.txt"),
                         "exclusion.json": sha_file(ROOT / "manuscript/prereg/2026-10-21_dev_pools/exclusion.json"),
                         "LEXICON_v1.txt": sha_file(HERE.parent / "LEXICON_v1.txt")},
    }, indent=1, ensure_ascii=False) + "\n", encoding="utf-8")
    print(json.dumps({"id_steps": counts, "survivors": len(order), "w25_removed_union": w25_union}))


def _check() -> None:
    t = [syllables("áo dài"), syllables("chùa")]
    assert has_term("Một cô_gái mặc Áo_dài trắng.", t) and has_term("ngôi chùa cổ", t)
    assert not has_term("gia đình ngồi ăn", t) and not has_term("cái áo màu dài", t)
    assert order_key("a.jpg") != order_key("b.jpg") and len(order_key("a.jpg")) == 64


if __name__ == "__main__":
    _check()
    main()
