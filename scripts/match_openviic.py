#!/usr/bin/env python
"""KTVIC images that UIT-OpenViIC also contains, and their OpenViIC captions: a second human panel.

    # 1. n3, CPU (~1-2 h at nice 19, < 2 GB RAM): pHash, dHash, 32x32 thumbnail and SSCD descriptor of every image
    PYTHONPATH=/root/r2/pylib nice -n 19 python scripts/match_openviic.py embed \\
        --sscd /root/r2/models/sscd_disc_mixup.torchscript.pt --cache /root/r2/openviic_match
    # 2. hashes of the mirrored KTVIC images (the pool holds mirrored copies; SSCD is flip-invariant, the hashes not)
    PYTHONPATH=/root/r2/pylib python scripts/match_openviic.py mirror --cache /root/r2/openviic_match
    # 3. pairs, the ViCLIP-OT counts, data/ktvic_openviic_refs.json
    python scripts/match_openviic.py match --cache /root/r2/openviic_match
    # 4. side-by-side sheets of sampled matched and borderline pairs, for visual inspection
    python scripts/match_openviic.py sheets --cache /root/r2/openviic_match --out /tmp/sheets

Data. UIT-OpenViIC (Bui, Nguyen & Nguyen, arXiv 2305.04166; Signal Processing: Image Communication
140:117430, 2026; 13,100 images x 61,241 captions, "publicly available for research purposes", the arXiv
version says for non-commercial research) as released at https://github.com/nghiangh/UIT-OpenViIC-dataset
(commit e3bf744): images.zip (Drive 1eRWL751fGv4WPTg0dhBGMRbcUgh9xKA5, 3,805,342,476 bytes, sha256 2da7e81f6beb422b...,
13,300 files: 200 carry no caption) and uit-openviic-annotation-{train,dev,test}.json (Drive 1kOgUE3duQjxJ6aaXrEHN8YlPQxF08JxW,
1eQbmeU5x3GL0_JO_mZgYKYNAFLvpCdL5, 126gNnTrh13AZ2mc51bEMvB29huwuSB98), unchanged under
$NCS_DATA/datasets/openviic/{images/, uit-openviic-annotation-*.json}. The Drive folder linked from the
dataset page https://uit-together.github.io/datasets/UIT-OpenViIC/ answers 404 (checked 2026-10-12).

Matching. Two independent signals must agree. Perceptual hashes (imagehash pHash and dHash, 64 bits, on
the EXIF-oriented RGB image) propose a pair when either Hamming distance is <= --hash-max; the SSCD copy
descriptor (Pizzi et al., CVPR 2022; sscd_disc_mixup TorchScript, small_288 preprocessing; cosine)
confirms it at >= --sscd-min. The 32x32 grey thumbnail correlation is a third, pixel-level number kept for
inspection. KTVIC's file names are not used to match, only reported: KTVIC took its images from the
UIT-EVJVQA pool (KTVIC paper, Sec. 3) and kept their numbering, which OpenViIC shares.
ViCLIP-OT (arXiv 2602.22678, App. B) calls a KTVIC image a near-duplicate when its SSCD cosine to some
OpenViIC *train* image is >= 0.8 (401 / 558 test, 2,464 / 3,769 train); `match` recounts that rule.

Output: {"_provenance": {...}, "_pairs": {split: {ktvic_id: [[openviic file, openviic split, pHash,
dHash, SSCD], ...]}}, "train"/"test": {ktvic_id: [OpenViIC captions of every matched copy, de-duplicated]}}.
"""
from __future__ import annotations

import argparse
import json
import os
import random
import sys
from pathlib import Path

import numpy as np

ROOT = Path(__file__).resolve().parents[1]
DATA = Path(os.environ.get("NCS_DATA", Path.home() / "ncs-data"))
KTVIC_DIR, OPENVIIC_DIR = DATA / "datasets" / "ktvic", DATA / "datasets" / "openviic"
KTVIC_SPLITS = {"train": "train_data.json", "test": "test_data.json"}
OPENVIIC_SPLITS = ("train", "dev", "test")
SSCD_SHORT_SIDE = 288
SSCD_LONG_MAX = 4 * SSCD_SHORT_SIDE
IMAGENET_MEAN = np.array([0.485, 0.456, 0.406], np.float32)
IMAGENET_STD = np.array([0.229, 0.224, 0.225], np.float32)
VICLIP_OT = {"rule": "SSCD cosine >= 0.8 to an OpenViIC train image", "test": 401, "train": 2464}


def ktvic_images() -> dict[str, tuple[str, str]]:
    """file name -> (KTVIC split, image id)."""
    out = {}
    for split, f in KTVIC_SPLITS.items():
        for im in json.loads((KTVIC_DIR / f).read_text(encoding="utf-8"))["images"]:
            out[im["filename"]] = (split, str(im["id"]))
    return out


def openviic_captions() -> dict[str, tuple[str, list[str]]]:
    """file name -> (OpenViIC split, captions); images.zip files absent here have no caption."""
    out = {}
    for split in OPENVIIC_SPLITS:
        ann = json.loads((OPENVIIC_DIR / f"uit-openviic-annotation-{split}.json").read_text(encoding="utf-8"))
        out.update({name: (split, [c.strip() for c in v["captions"]]) for name, v in ann.items()})
    return out


def load_image(path: Path):
    from PIL import Image, ImageOps

    im = Image.open(path)
    im.draft("RGB", (SSCD_SHORT_SIDE, SSCD_SHORT_SIDE))  # JPEG: decode at the smallest 1/2^k scale >= 288 px
    return ImageOps.exif_transpose(im).convert("RGB")


def sscd_input(im) -> np.ndarray:
    """SSCD's small_288 (torchvision Resize(288), ToTensor, ImageNet Normalize) in PIL + numpy: CHW float32.

    The long side is capped at 4 x 288 (panoramas only; aspect ratio kept): one 288 x 5000 input costs GBs
    of activations on CPU."""
    from PIL import Image

    w, h = im.size
    size = (SSCD_SHORT_SIDE, int(SSCD_SHORT_SIDE * h / w)) if w <= h else (int(SSCD_SHORT_SIDE * w / h), SSCD_SHORT_SIDE)
    if max(size) > SSCD_LONG_MAX:
        f = SSCD_LONG_MAX / max(size)
        size = (max(1, int(size[0] * f)), max(1, int(size[1] * f)))
    x = np.asarray(im.resize(size, Image.BILINEAR), np.float32) / 255.0
    return ((x - IMAGENET_MEAN) / IMAGENET_STD).transpose(2, 0, 1).copy()


def _features(path: str):
    """(pHash, dHash, 32x32 grey thumbnail, SSCD input) of one image, or (path, error)."""
    import imagehash
    from PIL import Image

    try:
        im = load_image(Path(path))
    except Exception as e:  # unreadable file: reported by embed, never matched
        return path, f"{type(e).__name__}: {e}"
    thumb = np.asarray(im.convert("L").resize((32, 32), Image.BILINEAR), dtype=np.uint8)
    return int(str(imagehash.phash(im)), 16), int(str(imagehash.dhash(im)), 16), thumb, sscd_input(im)


def _mirror_hashes(path: str) -> tuple[int, int]:
    """pHash and dHash of the horizontally mirrored image ((0, 0) when unreadable): the hashes are not
    flip-invariant, SSCD is, and the pool holds mirrored copies."""
    import imagehash
    from PIL import ImageOps

    try:
        im = ImageOps.mirror(load_image(Path(path)))
    except Exception:  # unreadable: embed already recorded it
        return 0, 0
    return int(str(imagehash.phash(im)), 16), int(str(imagehash.dhash(im)), 16)


def cmd_mirror(args) -> None:
    """Add phash_m / dhash_m (hashes of the mirrored image) to the cached KTVIC set."""
    from multiprocessing import Pool

    f = Path(args.cache) / "ktvic.npz"
    z = dict(np.load(f))
    with Pool(args.workers) as pool:
        got = pool.map(_mirror_hashes, [str(KTVIC_DIR / "images" / n) for n in z["files"]], chunksize=16)
    z["phash_m"] = np.array([g[0] for g in got], np.uint64)
    z["dhash_m"] = np.array([g[1] for g in got], np.uint64)
    np.savez(f, **z)
    print(f"{f}: mirrored hashes of {len(got)} images")


def cmd_embed(args) -> None:
    from multiprocessing import Pool

    import torch

    torch.set_num_threads(args.threads)
    model = torch.jit.load(args.sscd).eval()
    cache = Path(args.cache)
    cache.mkdir(parents=True, exist_ok=True)
    for name, root in (("ktvic", KTVIC_DIR), ("openviic", OPENVIIC_DIR)):
        if (cache / f"{name}.npz").exists():
            print(f"{name}: {cache / name}.npz exists, kept")
            continue
        files = sorted(p.name for p in (root / "images").iterdir() if p.is_file())
        n = len(files)
        ph, dh = np.zeros(n, np.uint64), np.zeros(n, np.uint64)
        thumbs, emb = np.zeros((n, 32, 32), np.uint8), np.full((n, 512), np.nan, np.float32)
        failed = {}
        paths = [str(root / "images" / f) for f in files]
        chunks = [range(i, min(i + args.chunk, n)) for i in range(0, n, args.chunk)]
        # map_async one chunk ahead: at most two chunks of decoded images in memory (imap would let the
        # decoders run arbitrarily far ahead of the slower SSCD forward pass)
        with Pool(args.workers) as pool, torch.inference_mode():
            pending = pool.map_async(_features, [paths[i] for i in chunks[0]])
            for c, rows in enumerate(chunks):
                got = pending.get()
                if c + 1 < len(chunks):
                    pending = pool.map_async(_features, [paths[i] for i in chunks[c + 1]])
                for i, f in zip(rows, got):
                    if isinstance(f[1], str):
                        failed[files[i]] = f[1]
                        continue
                    ph[i], dh[i], thumbs[i] = f[0], f[1], f[2]
                    emb[i] = model(torch.from_numpy(f[3])[None])[0].numpy()
                if (c + 1) % 32 == 0:
                    print(f"  {name}: {rows[-1] + 1}/{n}", flush=True)
        np.savez(cache / f"{name}.npz", files=np.array(files), phash=ph, dhash=dh, thumbs=thumbs, sscd=emb)
        print(f"{name}: {n} images, {len(failed)} unreadable {sorted(failed.items())[:5]}", flush=True)


def hamming(a: np.ndarray, b: np.ndarray) -> np.ndarray:
    """(len(a), len(b)) Hamming distances between two uint64 hash vectors."""
    return np.bitwise_count(a[:, None] ^ b[None, :])


def thumb_corr(a: np.ndarray, b: np.ndarray) -> float:
    a, b = a.astype(np.float64).ravel(), b.astype(np.float64).ravel()
    a, b = a - a.mean(), b - b.mean()
    den = np.sqrt((a * a).sum() * (b * b).sum())
    return float((a * b).sum() / den) if den else 0.0


def all_pairs(k: dict, o: dict, hash_max: int, sscd_floor: float, chunk: int = 256) -> list[tuple]:
    """Every (ktvic row, openviic row, pHash, dHash, SSCD) with a hash distance <= hash_max or SSCD >= sscd_floor,
    plus each KTVIC image's SSCD-nearest OpenViIC image and its nearest OpenViIC train image."""
    train = np.array([s == "train" for s in o["split"]])
    ke, oe = np.nan_to_num(k["sscd"]), np.nan_to_num(o["sscd"])
    out = []
    for lo in range(0, len(k["files"]), chunk):
        rows = slice(lo, lo + chunk)
        sim = ke[rows] @ oe.T
        ph, dh = hamming(k["phash"][rows], o["phash"]), hamming(k["dhash"][rows], o["dhash"])
        if "phash_m" in k:  # a mirrored copy is a copy: the nearer of the direct and the mirrored hash
            ph = np.minimum(ph, hamming(k["phash_m"][rows], o["phash"]))
            dh = np.minimum(dh, hamming(k["dhash_m"][rows], o["dhash"]))
        keep = (ph <= hash_max) | (dh <= hash_max) | (sim >= sscd_floor)
        keep[np.arange(sim.shape[0]), sim.argmax(1)] = True
        keep[np.arange(sim.shape[0]), np.where(train, sim, -9).argmax(1)] = True
        for r, c in zip(*np.nonzero(keep)):
            out.append((lo + r, int(c), int(ph[r, c]), int(dh[r, c]), float(sim[r, c])))
    return out


def is_match(ph: int, dh: int, sscd: float, hash_max: int, sscd_min: float) -> bool:
    return min(ph, dh) <= hash_max and sscd >= sscd_min


def panel(copies: list[str], caps: dict[str, tuple[str, list[str]]]) -> list[str]:
    """Captions of every captioned OpenViIC copy, in copy order, exact repeats dropped."""
    seen, out = set(), []
    for f in copies:
        for c in caps.get(f, ("", []))[1]:
            if c and c not in seen:
                seen.add(c)
                out.append(c)
    return out


def _load(cache: Path) -> tuple[dict, dict]:
    kt, caps = ktvic_images(), openviic_captions()
    sets = {}
    for name in ("ktvic", "openviic"):
        z = np.load(cache / f"{name}.npz")
        d = {key: z[key] for key in z.files}
        d["files"] = [str(f) for f in d["files"]]
        d["split"] = [(kt.get(f, ("?", ""))[0] if name == "ktvic" else caps.get(f, ("uncaptioned", []))[0])
                      for f in d["files"]]
        sets[name] = d
    return sets["ktvic"], sets["openviic"]


def cmd_match(args) -> dict:
    k, o = _load(Path(args.cache))
    kt, caps = ktvic_images(), openviic_captions()
    pairs = all_pairs(k, o, args.hash_max + 6, 0.5)
    rows = [{"k": k["files"][r], "k_split": k["split"][r], "o": o["files"][c], "o_split": o["split"][c],
             "phash": ph, "dhash": dh, "sscd": round(s, 4), "pix": round(max(thumb_corr(k["thumbs"][r], o["thumbs"][c]),
                              thumb_corr(k["thumbs"][r][:, ::-1], o["thumbs"][c])), 4),
             "same_name": k["files"][r] == o["files"][c]} for r, c, ph, dh, s in pairs]
    (Path(args.cache) / "pairs.json").write_text(json.dumps(rows, indent=0), encoding="utf-8")
    matched = [p for p in rows if is_match(p["phash"], p["dhash"], p["sscd"], args.hash_max, args.sscd_min)]
    summary = {"rule": f"min(pHash, dHash) <= {args.hash_max} and SSCD >= {args.sscd_min}", "per_split": {}}
    for sp in KTVIC_SPLITS:
        ids = [f for f, (s, _) in kt.items() if s == sp]
        mine = {p["k"] for p in matched if p["k_split"] == sp}
        best_train = {}
        for p in rows:
            if p["k_split"] == sp and p["o_split"] == "train":
                best_train[p["k"]] = max(best_train.get(p["k"], -1.0), p["sscd"])
        captioned = {p["k"] for p in matched if p["k_split"] == sp and p["o_split"] in OPENVIIC_SPLITS}
        summary["per_split"][sp] = {
            "ktvic_images": len(ids), "matched_any_openviic_file": len(mine),
            "matched_captioned_copy": len(captioned),
            "matched_openviic_train_copy": len({p["k"] for p in matched if p["k_split"] == sp and p["o_split"] == "train"}),
            "viclip_ot_rule_sscd_ge_0.8_vs_openviic_train": sum(v >= 0.8 for v in best_train.values()),
            "viclip_ot_reported": VICLIP_OT[sp],
            "same_name_copy_among_matched": len({p["k"] for p in matched if p["k_split"] == sp and p["same_name"]}),
            "matched_by_split_of_copy": {s: len({p["k"] for p in matched if p["k_split"] == sp and p["o_split"] == s})
                                         for s in (*OPENVIIC_SPLITS, "uncaptioned")}}
    # KTVIC kept the pool's file names: how the same-name pairs score (a check, never a matching input)
    at = {f: j for j, f in enumerate(o["files"])}
    same = np.array([(r, at[f]) for r, f in enumerate(k["files"]) if f in at])
    s_ph = np.bitwise_count(k["phash"][same[:, 0]] ^ o["phash"][same[:, 1]])
    s_dh = np.bitwise_count(k["dhash"][same[:, 0]] ^ o["dhash"][same[:, 1]])
    s_ss = (np.nan_to_num(k["sscd"][same[:, 0]]) * np.nan_to_num(o["sscd"][same[:, 1]])).sum(1)
    summary["same_name_pairs"] = {
        "n": len(same), "matched": int(sum(is_match(a, b, c, args.hash_max, args.sscd_min) for a, b, c in zip(s_ph, s_dh, s_ss))),
        "phash_quantiles_0_50_90_99_100": [int(np.percentile(s_ph, q)) for q in (0, 50, 90, 99, 100)],
        "sscd_quantiles_0_1_10_50": [round(float(np.percentile(s_ss, q)), 3) for q in (0, 1, 10, 50)]}
    # signal agreement over every pair one signal flags
    flagged_hash = [p for p in rows if min(p["phash"], p["dhash"]) <= args.hash_max]
    flagged_sscd = [p for p in rows if p["sscd"] >= args.sscd_min]
    summary["agreement"] = {
        "hash_flagged_pairs": len(flagged_hash), "of_which_sscd_confirms": sum(p["sscd"] >= args.sscd_min for p in flagged_hash),
        "sscd_flagged_pairs": len(flagged_sscd),
        "of_which_hash_confirms": sum(min(p["phash"], p["dhash"]) <= args.hash_max for p in flagged_sscd),
        "matched_pairs": len(matched), "matched_pairs_same_name": sum(p["same_name"] for p in matched)}
    print(json.dumps(summary, indent=1))
    copies: dict[str, list[dict]] = {}
    for p in sorted(matched, key=lambda p: (OPENVIIC_SPLITS + ("uncaptioned",)).index(p["o_split"])):
        copies.setdefault(p["k"], []).append(p)
    out = {"_provenance": {
        "what": "OpenViIC captions of KTVIC images that UIT-OpenViIC also contains (a second, independent human panel)",
        "made_by": "scripts/match_openviic.py match", "openviic": __doc__.split("Data. ")[1].split("\n\n")[0],
        "matching": summary["rule"] + " (pHash/dHash: imagehash, 64-bit; SSCD: sscd_disc_mixup, small_288, cosine)",
        "summary": summary, "visual_check": args.visual_check}, "_pairs": {}}
    for sp in KTVIC_SPLITS:
        got = {kt[f][1]: c for f, c in copies.items() if kt[f][0] == sp}
        out["_pairs"][sp] = {i: [[p["o"], p["o_split"], p["phash"], p["dhash"], p["sscd"]] for p in c]
                             for i, c in sorted(got.items(), key=lambda x: int(x[0]))}
        out[sp] = {i: cs for i, c in sorted(got.items(), key=lambda x: int(x[0]))
                   if (cs := panel([p["o"] for p in c], caps))}
        print(f"{sp}: {len(out[sp])} KTVIC images with OpenViIC captions, "
              f"{sum(map(len, out[sp].values())) / max(len(out[sp]), 1):.2f} captions/image")
    Path(args.out).write_text(json.dumps(out, ensure_ascii=False, indent=1) + "\n", encoding="utf-8")
    print(f"-> {args.out}")
    return out


def cmd_sheets(args) -> None:
    """Sheets of 6 pairs (KTVIC left, OpenViIC right): a random sample of matched pairs and the borderline ones."""
    from PIL import Image, ImageDraw

    rows = json.loads((Path(args.cache) / "pairs.json").read_text(encoding="utf-8"))
    hit = lambda p: is_match(p["phash"], p["dhash"], p["sscd"], args.hash_max, args.sscd_min)
    rng = random.Random(args.seed)
    groups = {
        "matched": rng.sample([p for p in rows if hit(p)], args.n_matched),
        "matched_other_name": [p for p in rows if hit(p) and not p["same_name"]],
        "hash_only": [p for p in rows if min(p["phash"], p["dhash"]) <= args.hash_max and not hit(p)],
        "sscd_only": sorted([p for p in rows if p["sscd"] >= args.sscd_min and not hit(p)], key=lambda p: -p["sscd"]),
        "weakest_matched": sorted([p for p in rows if hit(p)], key=lambda p: (p["sscd"] - 0.02 * min(p["phash"], p["dhash"])))}
    out = Path(args.out)
    out.mkdir(parents=True, exist_ok=True)
    for g, ps in groups.items():
        ps = ps[: args.n_matched] if g != "matched" else ps
        for s in range(0, len(ps), 6):
            sheet = Image.new("RGB", (2 * 300 + 10, 6 * 236), "white")
            draw = ImageDraw.Draw(sheet)
            for j, p in enumerate(ps[s:s + 6]):
                for col, (d, f) in enumerate(((KTVIC_DIR, p["k"]), (OPENVIIC_DIR, p["o"]))):
                    im = load_image(d / "images" / f)
                    im.thumbnail((300, 210))
                    sheet.paste(im, (col * 310, j * 236 + 22))
                draw.text((2, j * 236 + 4), f"{g} K:{p['k']}({p['k_split']}) O:{p['o']}({p['o_split']}) "
                          f"pH={p['phash']} dH={p['dhash']} sscd={p['sscd']:.2f} pix={p['pix']:.2f}", fill="black")
            sheet.save(out / f"{g}_{s // 6:02d}.png")
        print(f"{g}: {len(ps)} pairs -> {out}/{g}_*.png")


def main() -> int:
    ap = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    sub = ap.add_subparsers(dest="cmd", required=True)
    e = sub.add_parser("embed", help="hashes, thumbnails and SSCD descriptors of both image sets")
    e.add_argument("--sscd", required=True, help="sscd_disc_mixup.torchscript.pt")
    e.add_argument("--threads", type=int, default=4)
    e.add_argument("--workers", type=int, default=2)
    e.add_argument("--chunk", type=int, default=32, help="images decoded ahead of the SSCD pass")
    m = sub.add_parser("mirror", help="hashes of the mirrored KTVIC images, added to ktvic.npz")
    m.add_argument("--workers", type=int, default=3)
    for name, p in (("match", sub.add_parser("match", help="pairs, counts, the refs file")),
                    ("sheets", sub.add_parser("sheets", help="contact sheets for visual inspection"))):
        p.add_argument("--hash-max", type=int, default=10, help="pHash or dHash Hamming distance proposing a pair")
        p.add_argument("--sscd-min", type=float, default=0.5, help="SSCD cosine confirming it")
        if name == "match":
            p.add_argument("--out", default=str(ROOT / "data" / "ktvic_openviic_refs.json"))
            p.add_argument("--visual-check", default="", help="result of the visual inspection, stored in the provenance")
        else:
            p.add_argument("--out", required=True)
            p.add_argument("--n-matched", type=int, default=60)
            p.add_argument("--seed", type=int, default=0)
    for p in sub.choices.values():
        p.add_argument("--cache", required=True, help="directory of ktvic.npz / openviic.npz / pairs.json")
    args = ap.parse_args()
    {"embed": cmd_embed, "mirror": cmd_mirror, "match": cmd_match, "sheets": cmd_sheets}[args.cmd](args)
    return 0


def _check() -> None:
    a, b = np.array([0, 0b1011], np.uint64), np.array([0b1, 2**64 - 1], np.uint64)
    assert hamming(a, b).tolist() == [[1, 64], [2, 61]]
    assert is_match(3, 40, 0.9, 10, 0.5) and not is_match(11, 12, 0.99, 10, 0.5) and not is_match(0, 0, 0.3, 10, 0.5)
    t = np.arange(1024, dtype=np.uint8).reshape(32, 32)
    assert abs(thumb_corr(t, t) - 1) < 1e-9 and thumb_corr(t, np.zeros_like(t)) == 0.0
    caps = {"a.jpg": ("train", ["x", "y"]), "b.jpg": ("dev", ["y", "z"])}
    assert panel(["a.jpg", "b.jpg", "c.jpg"], caps) == ["x", "y", "z"]


if __name__ == "__main__":
    _check()
    sys.exit(main())
