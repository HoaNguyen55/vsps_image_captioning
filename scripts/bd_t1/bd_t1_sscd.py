#!/usr/bin/env python3
"""BD-T1 W5 (CC-171): SSCD copy-detection exclusions, laptop CPU, run once before `bd_t1.py lists`.

    <python with torch> scripts/bd_t1/bd_t1_sscd.py --sscd sscd_disc_mixup.torchscript.pt --out F
    python3 scripts/bd_t1/bd_t1_sscd.py --selftest

Descriptor and preprocessing = scripts/match_openviic.py (sscd_disc_mixup, small_288, cosine), unchanged.
Rules (SSCD cosine >= SSCD_MIN, match_openviic's confirmation bound, used alone so it excludes more):
  pool_vs_held:  a B-1 pool image near an H-candidate or dev300 image -> leaves the training pool;
  held_vs_test:  an H- or T2-candidate near any KTVIC test or OpenViIC test image -> leaves H / T2.
Candidates are recomputed here from _pairs.train exactly as bd_t1.dev_only does. The OpenViIC test annotation is
read for its keys (file names) only. Output: ids, file names and cosines; no caption text.
"""
from __future__ import annotations

import argparse
import hashlib
import json
import sys
from pathlib import Path

import numpy as np

ROOT = Path(__file__).resolve().parents[2]
sys.path.insert(0, str(ROOT / "scripts"))
SSCD_MIN = 0.5
TRUNCATED: list[str] = []  # files decoded with PIL LOAD_TRUNCATED_IMAGES (recorded in the output)


def ids(p: Path) -> list[str]:
    return [x.strip() for x in p.read_text().split() if x.strip()]


def dev_only(pairs: dict, cand) -> list[str]:
    return sorted((i for i in cand if pairs.get(i) and {c[1] for c in pairs[i]} == {"dev"}), key=int)


def near(A: np.ndarray, B: np.ndarray, a_ids: list, b_ids: list, floor: float = SSCD_MIN) -> dict:
    """a id -> [nearest b id, cosine] for every a with max cosine >= floor (rows L2-normalised)."""
    out = {}
    for lo in range(0, len(A), 512):
        s = A[lo:lo + 512] @ B.T
        j = s.argmax(1)
        for r, (jj, v) in enumerate(zip(j, s[np.arange(len(j)), j])):
            if v >= floor:
                out[a_ids[lo + r]] = [b_ids[jj], round(float(v), 4)]
    return out


def embed(model, paths: list[Path]) -> np.ndarray:
    import torch
    from match_openviic import load_image, sscd_input

    from PIL import ImageFile

    E = np.zeros((len(paths), 512), np.float32)
    with torch.inference_mode():
        for n, p in enumerate(paths):
            try:
                im = load_image(p)
            except OSError:  # truncated file: decode what is there (keeps it in the scan, so it can still exclude)
                ImageFile.LOAD_TRUNCATED_IMAGES = True
                im = load_image(p)
                ImageFile.LOAD_TRUNCATED_IMAGES = False
                TRUNCATED.append(p.name)
            e = model(torch.from_numpy(sscd_input(im))[None])[0].numpy()
            E[n] = e / max(np.linalg.norm(e), 1e-12)
            if (n + 1) % 500 == 0:
                print(f"  {n + 1}/{len(paths)}", flush=True)
    return E


def run(sscd: Path, out: Path) -> None:
    import torch

    if out.exists():
        raise SystemExit(f"{out} exists")
    torch.set_num_threads(8)
    model = torch.jit.load(str(sscd)).eval()
    kt = ROOT / "data/datasets/ktvic"
    fn = {str(x["id"]): x["filename"] for f in ("train_data.json", "test_data.json")
          for x in json.loads((kt / f).read_text(encoding="utf-8"))["images"]}
    test_k = [str(x["id"]) for x in json.loads((kt / "test_data.json").read_text(encoding="utf-8"))["images"]]
    pairs = json.loads((ROOT / "data/ktvic_openviic_refs.json").read_text(encoding="utf-8"))["_pairs"]["train"]
    pool, dev = ids(ROOT / "data/splits/ktvic_train_minus_dev300.txt"), ids(ROOT / "data/splits/ktvic_dev300.txt")
    H, T2 = dev_only(pairs, pool), dev_only(pairs, dev)
    ovd = ROOT / "data/datasets/openviic"
    ov_test = sorted(json.loads((ovd / "uit-openviic-annotation-test.json").read_text(encoding="utf-8")))  # keys
    ov_test = [f for f in ov_test if (ovd / "images" / f).exists()]
    E = {k: embed(model, [kt / "images" / fn[i] for i in v]) for k, v in
         (("pool", pool), ("dev", dev), ("ktvic_test", test_k))}
    E["ov_test"] = embed(model, [ovd / "images" / f for f in ov_test])
    rest = [i for i in pool if i not in set(H)]
    Pr = E["pool"][[pool.index(i) for i in rest]]
    heldE = np.vstack([E["pool"][[pool.index(i) for i in H]], E["dev"]])
    pool_vs_held = near(Pr, heldE, rest, H + dev)
    cand = H + T2
    CE = np.vstack([E["pool"][[pool.index(i) for i in H]], E["dev"][[dev.index(i) for i in T2]]])
    tk = near(CE, E["ktvic_test"], cand, [f"ktvic_test:{i}" for i in test_k])
    to = near(CE, E["ov_test"], cand, [f"ov_test:{f}" for f in ov_test])
    held_vs_test = {i: max((x for x in (tk.get(i), to.get(i)) if x), key=lambda x: x[1]) for i in set(tk) | set(to)}
    body = {"label": "BD-T1 W5 SSCD exclusions (ids, file names, cosines only)", "sscd_min": SSCD_MIN,
            "sscd_sha256": hashlib.sha256(sscd.read_bytes()).hexdigest(),
            "n": {"pool": len(pool), "dev300": len(dev), "H_candidates": len(H), "T2_candidates": len(T2),
                  "ktvic_test": len(test_k), "ov_test": len(ov_test)},
            "truncated_files_decoded_partially": TRUNCATED,
            "pool_vs_held": dict(sorted(pool_vs_held.items(), key=lambda x: int(x[0]))),
            "held_vs_test": dict(sorted(held_vs_test.items(), key=lambda x: int(x[0])))}
    out.write_text(json.dumps(body, indent=1) + "\n", encoding="utf-8")
    print(f"{hashlib.sha256(out.read_bytes()).hexdigest()}  pool_vs_held {len(pool_vs_held)}, "
          f"held_vs_test {len(held_vs_test)}")


def selftest() -> None:
    rng = np.random.default_rng(0)
    A = rng.normal(size=(5, 512)).astype(np.float32)
    A /= np.linalg.norm(A, axis=1, keepdims=True)
    B = rng.normal(size=(4, 512)).astype(np.float32)
    B /= np.linalg.norm(B, axis=1, keepdims=True)
    B[2] = A[3]  # a copy
    got = near(A, B, list("abcde"), list("wxyz"))
    assert list(got) == ["d"] and got["d"][0] == "y" and got["d"][1] > 0.99, got
    assert dev_only({"1": [["f", "dev"]], "2": [["g", "dev"], ["h", "test"]]}, ["1", "2", "3"]) == ["1"]
    print("bd_t1_sscd selftest ok")


if __name__ == "__main__":
    ap = argparse.ArgumentParser()
    ap.add_argument("--selftest", action="store_true")
    ap.add_argument("--sscd", type=Path)
    ap.add_argument("--out", type=Path)
    a = ap.parse_args()
    if a.selftest:
        selftest()
    else:
        run(a.sscd, a.out)
