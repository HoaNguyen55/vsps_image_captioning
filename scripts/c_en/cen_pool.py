#!/usr/bin/env python3
"""C-EN pool builder (CEN-M3-POOL, CC-113 W3/W5/W8 as amended by CC-115 W4): per-image SigLIP2 vectors and
near-duplicate features, outcome-blind. Prereg manuscript/prereg/2026-10-27_c_en/PREREG.md §4, §9 items 3-4.

  python3 scripts/c_en/cen_pool.py --selftest                                              CPU, synthetic only
  python  scripts/c_en/cen_pool.py embed --set S --images DIR --snapshot DIR --revision REV --emb1 E --out F \
      [--cap-s N]                                                                   GPU, venv-lb, M3
  python  scripts/c_en/cen_pool.py feats --set S --images DIR --sscd PT --out F [--workers N]   CPU, venv-cenfeat
Inputs are the pinned lists and the fetch records only (ids, files, sha256). Every image is sha-checked against its
record before it is opened. A memory image that cannot be opened is recorded as unreadable and dropped at build
(LISTS_ADDENDUM rule); a test-side image that cannot be opened is a STOP. No caption is read or written.
"""
from __future__ import annotations

import argparse
import json
import sys
import tempfile
import time
from pathlib import Path

import numpy as np

sys.path.insert(0, str(Path(__file__).resolve().parent))
import cen_fetch as F  # noqa: E402  lists, records, host check

SIGREV = "e8e487298228002f3d8a82e0cd5c8ea9c567f57f"  # CC-113 W3
SSCD_SHA256 = "9f26bd4c848cc19b73d2ae92eea6e04886f61a7b764ceb7a13aeee62e6a6db56"  # C stage-1 lists.json sscd
EMB1_SHA256 = "59e65f6f6432af97504c59c72fa07b644acbff26938e1365473fad659421f7c0"  # C stage-1 emb.npz (snapshot pins)
BATCH, FIRST_PROJ, EVERY = 64, 5000, 10000  # CC-113 W3 batch; W8 projections
OUT_ROOT = Path("/root/outputs/c_en")


def rows_of(name: str, rec_dir: Path = F.REC_DIR, root: Path = F.ROOT) -> list[tuple[int, str, str]]:
    """(id, file, sha256) in pinned list order: every list id for a test-side set (its record complete); for the
    memory, the recorded ids only (fetch refusals are not in the folder)."""
    rows = F.load_list(name, root)
    rec = F.read_rec(rec_dir / f"{name}.sha256.tsv")
    done = rec_dir / f"{name}.done.json"
    if not done.exists() or json.loads(done.read_text())["record_sha256"] != F.sha_file(rec_dir / f"{name}.sha256.tsv"):
        raise SystemExit(f"REFUSED: {name} has no complete fetch record")
    out = [(r[0], r[1], rec[r[0]][2]) for r in rows if r[0] in rec]
    if name != "memory" and len(out) != len(rows):
        raise SystemExit(f"{name}: the record does not cover the list")
    return out


def out_ok(p: Path) -> Path:
    """On M3 every output lies under /root/outputs/c_en."""
    if F.HEAD_AT_RUN and not Path(p).resolve().is_relative_to(OUT_ROOT):
        raise SystemExit(f"REFUSED: {p} is not under {OUT_ROOT}")
    return Path(p)


class RateGuard:
    """CC-113 W8: (t - t0) / (n - n0) from the first embedded batch; projected at FIRST_PROJ images, then every EVERY;
    STOP if the projection of the whole set exceeds the seconds left."""

    def __init__(self, total: int, cap_s: float, clock=time.time):
        self.total, self.cap_s, self.clock = total, cap_s, clock
        self.t0 = self.n0 = None
        self.next = FIRST_PROJ
        self.start = clock()

    def tick(self, n: int) -> float | None:
        if self.t0 is None:
            self.t0, self.n0 = self.clock(), n
            return None
        if n < self.next or n == self.n0:
            return None
        self.next += EVERY
        rate = (self.clock() - self.t0) / (n - self.n0)
        proj = (self.t0 - self.start) + rate * (self.total - self.n0)
        if proj > self.cap_s:  # exit 124: the job's cap-stop path, final, never retried (CC-113 W8 one run only)
            print(f"STOP (CC-113 W8): projected {proj / 3600:.2f} h exceeds the cap {self.cap_s / 3600:.2f} h",
                  file=sys.stderr)
            raise SystemExit(124)
        return proj


def open_rgb(path: Path):
    from PIL import Image

    with Image.open(path) as im:
        return im.convert("RGB")


def embed(name: str, rows: list, folder: Path, encode, cap_s: float, log=print) -> tuple[np.ndarray, list[int]]:
    """L2-normalised vectors in row order, batches of BATCH; encode(list of PIL images) -> (b, d) array."""
    guard = RateGuard(len(rows), cap_s) if name == "memory" else None
    vecs, bad = [], []
    for lo in range(0, len(rows), BATCH):
        ims, keep = [], []
        for n, (cid, f, h) in enumerate(rows[lo:lo + BATCH]):
            p = folder / f
            if F.sha_file(p) != h:
                raise SystemExit(f"STOP: {f} differs from its fetch record")
            try:
                ims.append(open_rgb(p))
                keep.append(n)
            except OSError:
                if name != "memory":
                    raise SystemExit(f"STOP: test-side image {cid} cannot be opened; to the judge") from None
                bad.append(cid)
        v = np.zeros((len(rows[lo:lo + BATCH]), 0), np.float32)
        if ims:
            e = np.asarray(encode(ims), np.float32)
            v = np.zeros((len(rows[lo:lo + BATCH]), e.shape[1]), np.float32)
            v[keep] = e / np.linalg.norm(e, axis=1, keepdims=True)
        vecs.append(v)
        if guard:
            proj = guard.tick(min(lo + BATCH, len(rows)))
            if proj is not None:
                log(f"{F.utc()} {name}: {lo + BATCH} embedded, projected {proj / 3600:.2f} h")
    return np.concatenate(vecs), bad


def cmd_embed(a) -> None:
    import torch
    from transformers import AutoModel, AutoProcessor

    F.host_ok(a.expect_head)
    if a.revision != SIGREV or F.sha_file(a.emb1) != EMB1_SHA256:
        raise SystemExit("SigLIP2 revision or the stage-1 emb.npz differs from its pin")
    meta1 = json.loads(str(np.load(a.emb1)["meta"]))
    snap = {p.name: F.sha_file(p) for p in sorted(Path(a.snapshot).iterdir()) if p.is_file()}
    if snap != meta1["snapshot_sha256"]:
        raise SystemExit("the SigLIP2 snapshot differs from the one C's memory was embedded with")
    rows = rows_of(a.set)
    proc = AutoProcessor.from_pretrained(a.snapshot)
    net = AutoModel.from_pretrained(a.snapshot, torch_dtype=torch.float16).eval().cuda()

    def encode(ims):
        with torch.no_grad():
            return net.get_image_features(**proc(images=ims, return_tensors="pt").to("cuda", torch.float16)
                                          ).float().cpu().numpy()

    vecs, bad = embed(a.set, rows, a.images, encode, a.cap_s)
    meta = {"set": a.set, "model": "google/siglip2-so400m-patch14-384", "revision": SIGREV, "dtype": "float16",
            "batch": BATCH, "snapshot_sha256": snap, "list_sha256": F.sha_file(F.ROOT / F.PDIR / F.SETS[a.set][0]),
            "record_sha256": F.sha_file(F.REC_DIR / f"{a.set}.sha256.tsv"), "unreadable": bad, "head": F.HEAD_AT_RUN,
            "packages": {k: __import__(k).__version__ for k in ("torch", "transformers")}, "utc": F.utc()}
    out = out_ok(a.out)
    np.savez(out, ids=np.array([r[0] for r in rows]), vecs=vecs, meta=json.dumps(meta))
    Path(str(out) + ".sha256").write_text(f"{F.sha_file(out)}  {out.name}\n")
    print(json.dumps({"set": a.set, "n": len(rows), "unreadable": len(bad)}))


def cmd_feats(a) -> None:
    sys.path.insert(0, str(F.ROOT / "scripts/c_stage1"))
    import build_memory as BM  # stage-1 module, unchanged: match_openviic features, mirrored hashes, SSCD

    F.host_ok(a.expect_head)
    if F.sha_file(a.sscd) != SSCD_SHA256:
        raise SystemExit("SSCD weights differ from 9f26bd4c")
    rows = rows_of(a.set)
    f = BM.features([a.images / r[1] for r in rows], str(a.sscd), workers=a.workers)
    if f["sha"] != [r[2] for r in rows]:
        raise SystemExit("STOP: a feature row's sha256 is not its fetch record's")
    bad = [rows[i][0] for i in f["unreadable"]]
    if bad and a.set != "memory":
        raise SystemExit(f"STOP: {len(bad)} test-side image(s) cannot be hashed; to the judge")
    out = out_ok(a.out)
    np.savez(out, ids=np.array([r[0] for r in rows]), sha=np.array(f["sha"]),
             **{k: f[k] for k in ("phash", "dhash", "phash_m", "dhash_m", "sscd")}, unreadable=np.array(bad, int),
             meta=json.dumps({"set": a.set, "sscd_sha256": SSCD_SHA256, "head": F.HEAD_AT_RUN, "utc": F.utc(),
                              "matcher_sha256": F.sha_file(F.ROOT / "scripts/match_openviic.py")}))
    Path(str(out) + ".sha256").write_text(f"{F.sha_file(out)}  {out.name}\n")
    print(json.dumps({"set": a.set, "n": len(rows), "unreadable": len(bad)}))


# ------------------------------------------------------------------------------------------------ self-test (CPU)
def selftest() -> None:
    from PIL import Image

    clock = [0.0]
    g = RateGuard(20000, 3600, clock=lambda: clock[0])
    assert g.tick(64) is None, "the first batch sets t0"
    clock[0] = 100.0
    assert g.tick(4992) is None, "no projection before 5,000"
    assert round(g.tick(5056)) == round(100 / (5056 - 64) * (20000 - 64)), "projection at 5,000"
    clock[0] = 1500.0
    assert g.tick(10000) is None and g.tick(15056) < 3600, "re-projected at 15,000, under the cap"
    clock[0] = 5000.0
    try:
        g.tick(25056)
        raise AssertionError("a projection above the cap is a STOP")
    except SystemExit as e:
        assert e.code == 124, "exit 124: the job's cap-stop path, not a retry"
    with tempfile.TemporaryDirectory() as tmp:
        t = Path(tmp)
        rows = []
        for n in range(5):
            p = t / f"COCO_train2014_{n:012d}.jpg"
            Image.fromarray(np.full((8, 8, 3), n * 40, np.uint8)).save(p, "JPEG")
            rows.append((n, p.name, F.sha_file(p)))
        (t / rows[2][1]).write_bytes(b"\xff\xd8 broken")
        rows[2] = (2, rows[2][1], F.sha_file(t / rows[2][1]))
        enc = lambda ims: np.array([[float(np.asarray(i).mean()) + 1, 1.0] for i in ims])  # noqa: E731
        v, bad = embed("memory", rows, t, enc, 3600, log=lambda *_: None)
        assert bad == [2] and v.shape == (5, 2) and not v[2].any() and np.allclose(np.linalg.norm(v[[0, 1, 3, 4]], axis=1), 1)
        assert F.refuses(lambda: embed("coco_test", rows, t, enc, 3600)), "a test-side image that cannot open: STOP"
        rows[0] = (0, rows[0][1], "0" * 64)
        assert F.refuses(lambda: embed("memory", rows, t, enc, 3600)), "sha differs from the record: STOP"
    print("selftest ok: rate guard (first projection at 5,000, STOP above the cap), sha check before open, "
          "unreadable memory image recorded and zeroed, test-side unreadable STOP, L2 norm")


def main() -> None:
    ap = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    ap.add_argument("--selftest", action="store_true")
    sub = ap.add_subparsers(dest="cmd")
    for name in ("embed", "feats"):
        p = sub.add_parser(name)
        p.add_argument("--set", choices=sorted(F.SETS), required=True)
        p.add_argument("--images", type=Path, required=True)
        p.add_argument("--out", type=Path, required=True)
        p.add_argument("--expect-head", required=True)
        if name == "embed":
            p.add_argument("--snapshot", type=Path, required=True)
            p.add_argument("--revision", required=True)
            p.add_argument("--emb1", type=Path, required=True)
            p.add_argument("--cap-s", type=float, default=3 * 3600)
        else:
            p.add_argument("--sscd", type=Path, required=True)
            p.add_argument("--workers", type=int, default=8)
    a = ap.parse_args()
    if a.selftest:
        return selftest()
    {"embed": cmd_embed, "feats": cmd_feats}.get(a.cmd, lambda _a: ap.error("mode?"))(a)


if __name__ == "__main__":
    main()
