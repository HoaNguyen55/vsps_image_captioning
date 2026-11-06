#!/usr/bin/env python3
"""C-PVR-T1 encoder-parity anchor (Paper C, H2; CC-280 Ruling 2(d), AM2, AD4). LAPTOP ONLY, after the E-G pull and
before any new npz is used; the old vectors never go to a host, so a FAIL costs no billed time.

    PY=~/.venvs/c_pvr/bin/python
    $PY -I -B scripts/c_pvr_gpu/c_pvr_parity.py selftest
    $PY -I -B scripts/c_pvr_gpu/c_pvr_parity.py check --new-xm emb_xm3600_vi.npz --new-ov emb_openviic_explore.npz \\
        --old-xm emb_xm_dev500.npz emb_xm_test2500.npz --old-ov emb_ov_test.npz

PARITY_MIN is fixed here, in committed code, before any new vector exists (CC-280 Ruling 2(d)). The old rows are
chosen by KEY before any vector arithmetic: all 3,000 XM3600 rows of emb_xm_dev500 + emb_xm_test2500, and the 1,020
openviic_explore rows of emb_ov_test (CR.half on the OpenViIC key); its 981 confirm-half rows are never used
(NB-T2POOL). Comparing image embeddings (no gold, caption or score) is not a look at a test set (AD4). PASS iff
min cosine(new, old) >= PARITY_MIN on both overlaps: rc 0. Else rc 1 = STOP: the new npz files are not used; read.
New npz = c_pvr_embed.py rekey outputs (ids, vecs). Prints counts, minima and shas only.
"""
from __future__ import annotations

import argparse
import hashlib
import json
import sys
from pathlib import Path

import numpy as np

sys.path.insert(0, str(Path(__file__).resolve().parent))
import c_pvr_gpu as G  # noqa: E402  load() (c_pvr / c_pvr_run behind their pins), CR.half

PARITY_MIN = 0.995  # [proposal] CC-280 Ruling 2(d): a STOP rule, fixed before any new vector exists
N_XM, N_OV = 3000, 1020  # AM2: the XM3600 overlap and the openviic_explore overlap (not 2,001)
OLD = {"emb_xm_dev500.npz": "48ec2476e0f8ae4ce375d9ca9ccf05bbcdba86139ba66c2c5a868acf08347982",  # C stage-2 / test,
       "emb_xm_test2500.npz": "b85510824c8053b6e6906f798c7e35f04b4069e55680c6b194c2b452ff1d80c6",  # SigLIP2 e8e48729
       "emb_ov_test.npz": "644b9200b5237df6bea8803a6d2b3ecbe0a15f443a647f48dad1411e262d7ebf"}


def sha(b: bytes) -> str:
    return hashlib.sha256(b).hexdigest()


def npz(p: Path, pins: dict | None):
    b = G.guard(p).read_bytes()
    if pins is not None and pins.get(p.name) != sha(b):
        G.fault(f"{p.name} differs from its pin")
    return np.load(p), sha(b)


def unit(v) -> np.ndarray:
    v = np.asarray(v, np.float32)
    return v / np.linalg.norm(v, axis=1, keepdims=True)


def side(new: Path, olds: list, keep, n: int, pins: dict | None) -> dict:
    """Old rows by key first (keep(id) and the count n), then their vectors; new rows by the same ids."""
    z, nh = npz(new, None)
    nid = {str(i): k for k, i in enumerate(z["ids"].tolist())}
    ids, vecs, hs = [], [], {}
    for p in olds:
        o, hs[p.name] = npz(p, pins)
        keys = [str(k).split("|", 1)[1] for k in o["keys"].tolist()]
        sel = [k for k, i in enumerate(keys) if keep(i)]  # selected before any vector is read for arithmetic
        ids += [keys[k] for k in sel]
        vecs.append(o["vecs"][sel])
    if len(ids) != n or len(set(ids)) != n:
        G.fault(f"{new.name}: {len(set(ids))} distinct old keys selected, not {n}")
    if miss := [i for i in ids if i not in nid]:
        G.fault(f"{new.name}: {len(miss)} old keys without a new row")
    cos = np.sum(unit(np.concatenate(vecs)) * unit(z["vecs"][[nid[i] for i in ids]]), axis=1)
    return {"n": n, "min": round(float(cos.min()), 6), "mean": round(float(cos.mean()), 6), "new_sha256": nh, "old": hs}


def check(new_xm: Path, new_ov: Path, old_xm: list, old_ov: Path, pins: dict | None = OLD, n=(N_XM, N_OV)) -> dict:
    rep = {"xm": side(new_xm, old_xm, lambda i: True, n[0], pins),
           "ov": side(new_ov, [old_ov], G.CR.half, n[1], pins), "parity_min": PARITY_MIN}
    rep["pass"] = rep["xm"]["min"] >= PARITY_MIN and rep["ov"]["min"] >= PARITY_MIN
    return rep


def selftest() -> None:
    import tempfile

    rng = np.random.default_rng(3)
    with tempfile.TemporaryDirectory() as td:
        w = Path(td)
        xm = [f"{j:016x}" for j in range(5)]
        ovk = [f"{j:011d}.jpg" for j in range(300, 340)]
        ex, cf = [k for k in ovk if G.CR.half(k)][:3], [k for k in ovk if not G.CR.half(k)][:2]
        base = {i: rng.normal(size=6) for i in xm + ex + cf}
        np.savez(w / "nx.npz", ids=np.array(xm + ["ffff"]), vecs=np.stack([base[i] for i in xm] + [rng.normal(size=6)]))
        np.savez(w / "no.npz", ids=np.array(ex), vecs=np.stack([base[i] for i in ex]))
        noise = lambda i: base[i] * 3 + rng.normal(size=6) * 1e-3  # noqa: E731  same direction, other norm
        np.savez(w / "x1.npz", keys=np.array([f"xm_dev500|{i}" for i in xm[:2]]), vecs=np.stack([noise(i) for i in xm[:2]]))
        np.savez(w / "x2.npz", keys=np.array([f"xm_test2500|{i}" for i in xm[2:]]), vecs=np.stack([noise(i) for i in xm[2:]]))
        orth = lambda i: np.r_[base[i][1], -base[i][0], 0, 0, 0, 0]  # noqa: E731  confirm rows: far from any new row
        np.savez(w / "o.npz", keys=np.array([f"ov_test|{k}" for k in ex + cf]),
                 vecs=np.stack([noise(k) for k in ex] + [orth(k) for k in cf]))
        args = (w / "nx.npz", w / "no.npz", [w / "x1.npz", w / "x2.npz"], w / "o.npz")
        r = check(*args, pins=None, n=(5, 3))
        assert r["pass"] and r["xm"]["min"] > 0.999 and r["ov"]["n"] == 3, r  # the 2 confirm rows were not used
        assert max(r["xm"]["mean"], r["ov"]["mean"]) <= 1 + 1e-6, r  # cosines, not raw dots (old rows have norm ~3x)
        assert PARITY_MIN == 0.995
        v = np.load(w / "nx.npz")["vecs"].copy()
        u, h = rng.normal(size=6), unit([v[1]])[0]
        v[1] = h + 0.15 * unit([u - (u @ h) * h])[0]  # cosine 1 / sqrt(1.0225) = 0.9889
        np.savez(w / "nx2.npz", ids=np.array(xm + ["ffff"]), vecs=v)
        r = check(w / "nx2.npz", *args[1:], pins=None, n=(5, 3))
        assert not r["pass"] and r["xm"]["min"] < PARITY_MIN and r["ov"]["min"] >= PARITY_MIN, r
        G._must("5 distinct old keys selected, not 4", check, *args, pins=None, n=(4, 3))
        G._must("3 distinct old keys selected, not 5", check, *args, pins=None, n=(5, 5))  # never the confirm rows
        np.savez(w / "nx3.npz", ids=np.array(xm[1:]), vecs=np.stack([base[i] for i in xm[1:]]))
        G._must("without a new row", check, w / "nx3.npz", *args[1:], pins=None, n=(5, 3))
        G._must("differs from its pin", check, *args, pins={"x1.npz": "0" * 64}, n=(5, 3))
    print(f"selftest ok  c_pvr_parity.py {sha(Path(__file__).read_bytes())}  PARITY_MIN {PARITY_MIN}")


def main() -> int:
    ap = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    sp = ap.add_subparsers(dest="cmd", required=True)
    sp.add_parser("selftest")
    c = sp.add_parser("check")
    for k in ("--new-xm", "--new-ov", "--old-ov"):
        c.add_argument(k, type=Path, required=True)
    c.add_argument("--old-xm", type=Path, nargs=2, required=True)
    a = ap.parse_args()
    G.load()
    if a.cmd == "selftest":
        return selftest()
    rep = check(a.new_xm, a.new_ov, a.old_xm, a.old_ov)
    print(json.dumps(rep, sort_keys=True))
    return 0 if rep["pass"] else 1


if __name__ == "__main__":
    sys.exit(main())
