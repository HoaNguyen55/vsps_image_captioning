#!/usr/bin/env python3
"""W25 near-duplicate pass (CC-148 W9 = CC-119 W25; rule manuscript/prereg/2026-10-28_w25_neardup/RULE.md): UT-2,402
against KV-5,000 (a superset of KV-4,224) and OIV7 val (41,164 compared = 41,620 - 456 XM3600 ids dropped by id before
any fetch, CC-153 r4). Output: w25_excluded_ids.txt, the file the K2 Gate 1 HOLD waits for. Features only (pHash, dHash,
mirrored hashes, SSCD descriptor, sha256) and ids; no caption, prediction or score of any evaluated system (CC-153 r1),
no image pair is ever shown to anyone.

    $FT w25.py --selftest                                          CPU, synthetic images and a dummy SSCD net
    $FT w25.py imports                                             import check first; exit 3 = missing
    $PY w25.py guard HEAD                                          common.guard verbatim + no /dev/shm/w25
    $FT w25.py preflight                                           CPU: C-EN feature pins, KV ids, NoCaps map (W2)
    $FT w25.py feats-ut --sscd PT --out NPZ                        CPU: the staged UT-2,402 images (train side)
    $FT w25.py feats-oiv7 --sscd PT --parts DIR [--workers N]      CPU + network: OIV7 val minus NoCaps val and XM3600,
                                                                   one tmpfs batch at a time, unlinked and logged
    $FT w25.py decide --ut NPZ --parts DIR --out-dir O             CPU: the RULE §3 union, one look

KV features are C-EN's (feats_coco_kval.npz, pinned below): no KV byte is fetched by W25. The NoCaps val 4,500 (a
subset of OIV7 val) reuse C-EN's feats_nocaps_val.npz, minus its 43 XM3600 rows. Feature code =
build_memory.features / near, unchanged.
"""
from __future__ import annotations

import argparse
import json
import shutil
import sys
import time
from pathlib import Path

import numpy as np

HERE = Path(__file__).resolve().parent
sys.path[:0] = [str(HERE.parent / "grl"), str(HERE.parent / "c_en"), str(HERE.parent / "c_stage1")]
import cen_fetch as F  # noqa: E402  OI_URL, get (no redirect, JPEG body), load_list, utc
import common as K  # noqa: E402  ids, pinned, guard, UV, sha_file

PDIR = K.ROOT / "manuscript/prereg/2026-10-28_w25_neardup"
OIV7_IDS = "manuscript/prereg/2026-10-28_w25_neardup/oiv7_val_ids.txt"
OIV7_IDS_SHA = "4b7a1813487dc5d74a5bd4aca7c36d0f6d2d3042d9cc6cf4091180dc473eabb0"
OIV7_N = 41620
XM_IDS = "manuscript/prereg/2026-10-28_w25_neardup/xm3600_in_oiv7_val_ids.txt"  # XM3600 full_data.json 101d24ad ∩ OIV7
XM_IDS_SHA = "54966ca78ce310201c091282603c9398155b8b05aaae9eb4cdf0abed88e6c5ef"
XM_N = 456
XM_FULL = K.ROOT / "data/datasets/xm3600/full_data.json"  # laptop only (absent on M3); ids read, never captions
OIV7_COMPARED = OIV7_N - XM_N  # 41,164 (CC-153 r4)
CEN_OUT = Path("/root/outputs/c_en")
CEN_FEATS = {  # C-EN SHA256SUMS_feats (2026-10-27, head 30514a7b, SSCD 9f26bd4c, matcher c0d9dd30)
    "coco_kval": "9783f7a669aa1b0a6df8e8a78aa3586fb7009f376d8151442ac3acc7da580a7e",
    "nocaps_val": "b69dac29b4dd07e759d1ff2fc38cb5d716cbe31ddb34c4233ff8f8667b8acba6"}
SSCD_SHA = "9f26bd4c848cc19b73d2ae92eea6e04886f61a7b764ceb7a13aeee62e6a6db56"  # = cen_pool.SSCD_SHA256
SHM = Path("/dev/shm/w25")  # the only place OIV7 val bytes ever exist (RULE §5); outside common.SCAN_ROOTS
BATCH = 512
SSCD_COPY = 0.75  # RULE §3 C3: sscd_disc_mixup README, "greater than 0.75 are copies with 90% precision" (DISC)
SSCD_REPORT = 0.5  # report only: Somepalli et al. CVPR 2023 §7 "> .5 SSCD"; never excludes on its own
MAX_LOST = 41  # RULE §3: at most 0.1% of OIV7 val unfetchable or unreadable, else FAULT
KEYS = ("phash", "dhash", "phash_m", "dhash_m", "sscd")
DELETIONS = "deletions.log"


def bm():
    import build_memory as BM  # C stage-1 module, unchanged (match_openviic features, mirrored hashes, SSCD)

    return BM


def ok_sscd(p: Path) -> str:
    if K.sha_file(p) != SSCD_SHA:
        raise SystemExit(f"FAULT: SSCD weights {p} differ from 9f26bd4c")
    return str(p)


def xm_ids() -> set[str]:
    """CC-153 r4: the 456 XM3600 images in OIV7 val, never fetched or compared (C's XM-test2500 one-look)."""
    ids = set(K.ROOT.joinpath(XM_IDS).read_text().split())
    if K.sha_file(K.ROOT / XM_IDS) != XM_IDS_SHA or len(ids) != XM_N:
        raise SystemExit("REFUSED: xm3600_in_oiv7_val_ids.txt differs from its pin")
    return ids


def xm_shas() -> set[str]:
    """The post-fetch backstop: exclusion.json's 3,600 XM3600 image sha256s."""
    ex = json.loads(K.pinned("manuscript/prereg/2026-10-21_dev_pools/exclusion.json").read_text())
    return set(ex["image_sha256"]["xm3600_all_images"])


def oiv7_rest() -> list[str]:
    """OIV7 val ids not in NoCaps val (whose features C-EN already holds) and not XM3600 (dropped by id), sorted."""
    ids = K.ROOT.joinpath(OIV7_IDS).read_text().split()
    if K.sha_file(K.ROOT / OIV7_IDS) != OIV7_IDS_SHA or len(set(ids)) != OIV7_N:
        raise SystemExit("REFUSED: oiv7_val_ids.txt differs from its pin")
    noc, xm = {r[1][:-4] for r in F.load_list("nocaps_val")}, xm_ids()
    if not noc <= set(ids) or not xm <= set(ids):
        raise SystemExit("REFUSED: a NoCaps val or XM3600 id is not in OIV7 val")
    return sorted(set(ids) - noc - xm)


def inputs() -> tuple[dict, dict, list[str]]:
    """CC-153 W2: C-EN's KV and NoCaps val features at their pins, KV ids == kv5000, every NoCaps id mapped to its OIV7
    id; the NoCaps rows of XM3600 images are dropped by id. Job step 0 (preflight) and decide both call this."""
    kv = load(CEN_OUT / "feats_coco_kval.npz", CEN_FEATS["coco_kval"])
    if sorted(kv["ids"]) != K.ids("kv5000") or kv["unreadable"]:
        raise SystemExit("FAULT: C-EN's Karpathy val features are not the 5,000 readable KV images")
    noc = load(CEN_OUT / "feats_nocaps_val.npz", CEN_FEATS["nocaps_val"])
    oid = {r[0]: r[1][:-4] for r in F.load_list("nocaps_val")}  # nocaps id -> open_images_id
    if len(oid) != 4500 or sorted(noc["ids"]) != sorted(oid) or noc["unreadable"]:
        raise SystemExit("FAULT: C-EN's NoCaps val features are not the 4,500 readable NoCaps val images")
    rest, xm = oiv7_rest(), xm_ids()
    keep = [i for i, n in enumerate(noc["ids"]) if oid[n] not in xm]
    noc = {"ids": [oid[noc["ids"][i]] for i in keep], "sha": [noc["sha"][i] for i in keep],
           **{k: noc[k][keep] for k in KEYS}, "unreadable": []}
    if len(rest) + len(noc["ids"]) != OIV7_COMPARED:
        raise SystemExit(f"FAULT: OIV7 val to compare is not {OIV7_COMPARED}")
    return kv, noc, rest


def save(out: Path, ids, f: dict, **meta) -> None:
    np.savez(out, ids=np.array(ids), sha=np.array(f["sha"]), **{k: f[k] for k in KEYS},
             unreadable=np.array([ids[i] for i in f["unreadable"]]), meta=json.dumps(meta))


def load(p: Path, want: str | None = None) -> dict:
    if want and K.sha_file(p) != want:
        raise SystemExit(f"FAULT: {p} differs from its pin {want[:8]}")
    z = np.load(p)
    return {"ids": z["ids"].tolist(), "sha": z["sha"].tolist(), **{k: z[k] for k in KEYS},
            "unreadable": z["unreadable"].tolist()}


def concat(fs: list[dict]) -> dict:
    return {"ids": sum((f["ids"] for f in fs), []), "sha": sum((f["sha"] for f in fs), []),
            **{k: np.concatenate([f[k] for f in fs]) for k in KEYS}, "unreadable": sum((f["unreadable"] for f in fs), [])}


# ------------------------------------------------------------------------------------------------ features
def cmd_feats_ut(a) -> None:
    """The staged UT-2,402 images (train side, already on M3), sha-checked against images.sha256."""
    out = Path(a.out)
    if out.exists():
        raise SystemExit(f"REFUSED: {out} exists")
    sha = {f: h for h, f in (x.split("  ") for x in (K.UV / "images.sha256").read_text().splitlines())}
    ids = K.ids("ut2402")
    paths = [K.UV / "images" / f"{i:012d}.jpg" for i in ids]
    f = bm().features(paths, ok_sscd(Path(a.sscd)), workers=a.workers)
    if f["sha"] != [sha[p.name] for p in paths]:
        raise SystemExit("FAULT: a staged UT image differs from images.sha256")
    if f["unreadable"]:
        raise SystemExit(f"FAULT: {len(f['unreadable'])} UT image(s) cannot be hashed")
    tmp = out.with_name(f".{out.name}")
    save(tmp, ids, f, set="ut2402", utc=F.utc())
    tmp.rename(out)
    print(json.dumps({"set": "ut2402", "n": len(ids)}))


def fetch_batch(batch: list[str], folder: Path, refuse: set[str], get=F.get,
                workers: int = 16) -> tuple[list[Path], dict]:
    """Fetch one batch into the tmpfs folder (bytes in RAM only). Returns the written paths and {id: error}. A body
    whose sha256 is an XM3600 image is never written: FAULT (the id drop missed it; CC-153 r4 backstop)."""
    import concurrent.futures as cf

    folder.mkdir(parents=True, exist_ok=False)
    paths, failed = [], {}
    with cf.ThreadPoolExecutor(workers) as ex:
        for oid, (b, err) in zip(batch, ex.map(lambda i: get(F.OI_URL.format(file=f"{i}.jpg")), batch)):
            if b is None:
                failed[oid] = err
                continue
            if F.sha_bytes(b) in refuse:
                raise SystemExit(f"FAULT: OIV7 {oid} is an XM3600 image by sha256; not written (CC-153 r4)")
            (folder / f"{oid}.jpg").write_bytes(b)
            paths.append(folder / f"{oid}.jpg")
    return paths, failed


def drop(folder: Path, log: Path, what: str) -> None:
    """Unlink a tmpfs batch and log the deletion (RULE §5)."""
    n = len(list(folder.iterdir())) if folder.exists() else 0
    shutil.rmtree(folder, ignore_errors=True)
    if folder.exists():
        raise SystemExit(f"FAULT: {folder} could not be deleted")
    with open(log, "a") as fh:
        fh.write(f"{F.utc()} deleted {folder} ({n} files) {what}\n")


def oiv7_parts(rest: list[str], parts: Path, sscd: str, workers: int, get=F.get, shm: Path = SHM,
               features=None, refuse: set[str] | None = None) -> None:
    """One part file per batch of 512 (resume skips finished parts). Every batch lives in tmpfs only from its fetch
    to the end of its features, then is unlinked and logged; nothing is ever written under common.SCAN_ROOTS."""
    features = features or bm().features
    refuse = xm_shas() if refuse is None else refuse
    parts.mkdir(parents=True, exist_ok=True)
    log = parts.parent / DELETIONS
    for n, lo in enumerate(range(0, len(rest), BATCH)):
        out = parts / f"part_{n:04d}.npz"
        if out.exists():
            continue
        batch, folder = rest[lo:lo + BATCH], shm / f"b{n:04d}"
        try:
            paths, failed = fetch_batch(batch, folder, refuse, get)
            f = features(paths, sscd, workers=workers)
        finally:
            drop(folder, log, f"after part {n:04d}")
        got = [p.stem for p in paths]
        tmp = parts / f".part_{n:04d}.npz"
        save(tmp, got, f, failed=failed)
        tmp.rename(out)
        print(f"part {n:04d}: {len(got)} featured, {len(failed)} failed", flush=True)


def cmd_feats_oiv7(a) -> None:
    oiv7_parts(oiv7_rest(), Path(a.parts), ok_sscd(Path(a.sscd)), a.workers)


# ------------------------------------------------------------------------------------------------ decision
def sscd_any(fx: dict, fy: dict, t: float, chunk: int = 512) -> np.ndarray:
    """x has some y with SSCD cosine > t (NaN descriptors never match)."""
    hit = np.zeros(len(fx["sha"]), bool)
    ye = np.nan_to_num(fy["sscd"])
    for lo in range(0, len(hit), chunk):
        hit[lo:lo + chunk] = ((np.nan_to_num(fx["sscd"][lo:lo + chunk]) @ ye.T) > t).any(1)
    return hit


def rule(ut: dict, y: dict, near) -> dict[str, np.ndarray]:
    """RULE §3. C1+C2 = build_memory.near unchanged (byte-identical, or min(pHash, dHash) <= 10 with UT's mirrored
    hashes AND SSCD >= 0.5); C3 = SSCD > 0.75. Excluded = C1+C2 OR C3. sscd_0.5 is reported, never excludes."""
    c12, c3 = near(ut, y), sscd_any(ut, y, SSCD_COPY)
    return {"C1_C2_registered": c12, "C3_sscd_0.75": c3, "excluded": c12 | c3,
            "report_sscd_0.5": sscd_any(ut, y, SSCD_REPORT - 1e-9)}


def decide(ut: dict, sets: dict[str, dict], lost: int, near) -> tuple[list[int], dict]:
    if lost > MAX_LOST:
        raise SystemExit(f"FAULT: {lost} OIV7 val images unfetched or unreadable (> {MAX_LOST}); TO-PI")
    per = {s: rule(ut, y, near) for s, y in sets.items()}
    ex = np.zeros(len(ut["ids"]), bool)
    for r in per.values():
        ex |= r["excluded"]
    ids = sorted(int(i) for i, e in zip(ut["ids"], ex) if e)
    counts = {s: {k: int(v.sum()) for k, v in r.items()} for s, r in per.items()}
    both = per[next(iter(per))]["excluded"].copy()
    for r in list(per.values())[1:]:
        both &= r["excluded"]
    return ids, {"n_ut": len(ut["ids"]), "n_excluded": len(ids), "pool_after": len(ut["ids"]) - len(ids),
                 "counts": counts, "excluded_by_both_sets": int(both.sum()), "oiv7_lost": lost,
                 "n_compared": {s: len(y["ids"]) for s, y in sets.items()}}


def cmd_decide(a) -> None:
    out = Path(a.out_dir)
    if (out / "w25_decide.json").exists():
        raise SystemExit("REFUSED: w25_decide.json exists (one look)")
    ut = load(Path(a.ut))
    if ut["ids"] != K.ids("ut2402"):
        raise SystemExit("FAULT: the UT feature file is not UT-2,402")
    kv, noc, rest = inputs()
    parts = [load(p) for p in sorted(Path(a.parts).glob("part_*.npz"))]
    if len(parts) != -(-len(rest) // BATCH):
        raise SystemExit("FAULT: OIV7 part files are missing")
    oi = concat([noc] + parts)
    if set(oi["ids"]) & xm_ids():
        raise SystemExit("FAULT: an XM3600 id is among the OIV7 features")
    lost_ids = sorted(((set(rest) | set(noc["ids"])) - set(oi["ids"])) | set(oi["unreadable"]))
    ids, rec = decide(ut, {"kv5000": kv, "oiv7_val": oi}, len(lost_ids), bm().near)
    rec |= {"schema": "vsps.w25.v1", "rule": "RULE §3: (C1 byte-identical OR C2 min(pHash,dHash)<=10 AND SSCD>=0.5) "
            "OR C3 SSCD>0.75", "oiv7_lost_ids": lost_ids,
            "oiv7_val_to_compare": f"{OIV7_COMPARED} ({OIV7_N} - {XM_N} XM3600, refused for every non-C use; "
                                   "CC-153 r4)",
            "xm3600_dropped_by_id": {"nocaps_rows": 4500 - len(noc["ids"]),
                                     "before_fetch": XM_N - 4500 + len(noc["ids"])},
            "inputs_sha256": {"ut_feats": K.sha_file(Path(a.ut)), **CEN_FEATS, "oiv7_val_ids": OIV7_IDS_SHA,
                              "xm3600_in_oiv7_val_ids": XM_IDS_SHA, "sscd": SSCD_SHA},
            "utc": F.utc(), "label": "W25 leakage exclusion: training side only, ids and counts"}
    out.mkdir(parents=True, exist_ok=True)
    (out / "w25_excluded_ids.txt").write_text("".join(f"{i}\n" for i in ids))
    (out / "w25_decide.json").write_text(json.dumps(rec, indent=1) + "\n")
    print(json.dumps({k: rec[k] for k in ("n_excluded", "pool_after", "oiv7_lost")}))


def cmd_preflight(_a) -> None:
    kv, noc, rest = inputs()
    print(json.dumps({"kv": len(kv["ids"]), "nocaps_kept": len(noc["ids"]), "oiv7_to_fetch": len(rest),
                      "oiv7_to_compare": OIV7_COMPARED}))


def cmd_imports(_a) -> None:
    try:
        import imagehash  # noqa: F401
        import torch  # noqa: F401
        from PIL import Image  # noqa: F401

        bm()
        F.load_list("nocaps_val")
    except Exception as e:  # noqa: BLE001 - any failure is a clean STOP before work
        print(f"IMPORT CHECK FAILED: {type(e).__name__}: {e}")
        sys.exit(3)
    print("w25 imports ok")


def cmd_guard(head: str) -> None:
    if SHM.exists():
        raise SystemExit(f"REFUSED: {SHM} exists")
    print(json.dumps(K.guard(head)))


# ------------------------------------------------------------------------------------------------ selftest
def selftest() -> None:
    import io
    import tempfile

    import torch
    from PIL import Image

    BM = bm()
    rng = np.random.default_rng(0)
    with tempfile.TemporaryDirectory() as d:
        d = Path(d)

        class Net(torch.nn.Module):  # dummy SSCD: 512-d unit vector of pooled colour statistics
            def forward(self, x):
                v = torch.cat([x.mean((2, 3)), x.std((2, 3))], 1).repeat(1, 86)[:, :512]
                return v / (v * v).sum(1, keepdim=True).sqrt()

        pt = d / "dummy.pt"
        torch.jit.script(Net()).save(str(pt))
        imgs = {k: Image.fromarray(rng.integers(0, 255, (300, 400, 3), np.uint8)) for k in "abc"}

        def jpeg(im) -> bytes:
            b = io.BytesIO()
            im.save(b, "JPEG", quality=90)
            return b.getvalue()

        body = {"aa": jpeg(imgs["a"]), "bb": jpeg(imgs["b"]), "cc": jpeg(imgs["c"])}
        calls = []

        def get(url):
            calls.append(url)
            oid = url.rsplit("/", 1)[1][:-4]
            return (body[oid], "") if oid in body else (None, "status 404")

        parts, shm = d / "out/parts", d / "shm"
        oiv7_parts(["aa", "bb", "cc", "dd"], parts, str(pt), 1, get, shm)
        assert not shm.exists() or not any(shm.iterdir()), "a tmpfs batch was left behind"
        log = (d / "out" / DELETIONS).read_text()
        assert "deleted" in log and "(3 files)" in log, log  # dd failed: 3 files written, all deleted
        p0 = load(parts / "part_0000.npz")
        assert p0["ids"] == ["aa", "bb", "cc"] and calls[0].endswith("/aa.jpg"), (p0["ids"], calls[:1])
        n = len(calls)
        oiv7_parts(["aa", "bb", "cc", "dd"], parts, str(pt), 1, get, shm)
        assert len(calls) == n, "a finished part was fetched again"
        try:  # CC-153 r4 backstop: an XM3600 body by sha is never written
            oiv7_parts(["aa"], d / "out2/parts", str(pt), 1, get, d / "shm2", refuse={F.sha_bytes(body["aa"])})
        except SystemExit as e:
            assert "FAULT" in str(e) and not (d / "shm2/b0000").exists(), e
        else:
            raise AssertionError("an XM3600 body by sha was accepted")
        # parity: the tmpfs path equals build_memory.features on the same bytes written to disk
        ref = d / "ref"
        ref.mkdir()
        for k, b in body.items():
            (ref / f"{k}.jpg").write_bytes(b)
        f = BM.features([ref / f"{k}.jpg" for k in body], str(pt), workers=1)
        assert all((f[k] == p0[k]).all() for k in ("phash", "dhash", "phash_m", "dhash_m"))
        assert np.allclose(f["sscd"], p0["sscd"]) and f["sha"] == p0["sha"]
        # rule: UT x0 is a byte copy of y "aa", x1 an SSCD-only copy (> 0.75), x2 unrelated
        y = concat([p0])
        ut = {"ids": [10, 11, 12], "sha": [y["sha"][0], "u1", "u2"],
              **{k: np.array([y[k][0], 0, 0], np.uint64) for k in KEYS[:4]},
              "sscd": np.stack([y["sscd"][0], y["sscd"][1], -y["sscd"][2]]), "unreadable": []}
        ut["phash"][1:] = ~np.uint64(0)  # hashes far from everything: x1 can only be caught by C3
        ut["dhash"][1:] = ~np.uint64(0)
        for k in ("phash_m", "dhash_m"):
            ut[k][:] = ~np.uint64(0)
        r = rule(ut, y, BM.near)
        assert r["C1_C2_registered"].tolist() == [True, False, False], r
        assert r["C3_sscd_0.75"].tolist() == [True, True, False] and r["excluded"].tolist() == [True, True, False]
        ids, rec = decide(ut, {"kv5000": y, "oiv7_val": y}, 0, BM.near)
        assert ids == [10, 11] and rec["pool_after"] == 1 and rec["excluded_by_both_sets"] == 2, rec
        try:
            decide(ut, {"kv5000": y}, MAX_LOST + 1, BM.near)
        except SystemExit as e:
            assert "FAULT" in str(e)
        else:
            raise AssertionError("too many lost OIV7 images were accepted")
    assert not any(str(SHM).startswith(str(r)) for r in K.SCAN_ROOTS), "the tmpfs stage is under a scan root"
    rest, xm = oiv7_rest(), xm_ids()  # CC-153 r4: the 456 XM3600 ids are dropped before any fetch
    noc = {r[1][:-4] for r in F.load_list("nocaps_val")}
    assert not set(rest) & xm and len(rest) + len(noc - xm) == OIV7_COMPARED == 41164, len(rest)
    if XM_FULL.exists():  # laptop: the pinned list is XM3600 full_data.json ∩ OIV7 val
        full = {i["id"] for i in json.loads(XM_FULL.read_text(encoding="utf-8"))["images"]}
        assert xm == full & set(K.ROOT.joinpath(OIV7_IDS).read_text().split()), "xm3600 id list"
    print("w25 selftest ok")


def main() -> None:
    if sys.argv[1:] == ["--selftest"]:
        return selftest()
    if sys.argv[1:2] == ["guard"]:
        return cmd_guard(sys.argv[2])
    ap = argparse.ArgumentParser()
    sp = ap.add_subparsers(dest="cmd", required=True)
    sp.add_parser("imports")
    u = sp.add_parser("feats-ut")
    o = sp.add_parser("feats-oiv7")
    for p in (u, o):
        p.add_argument("--sscd", required=True)
        p.add_argument("--workers", type=int, default=4)
    u.add_argument("--out", required=True)
    o.add_argument("--parts", required=True)
    de = sp.add_parser("decide")
    for f in ("--ut", "--parts", "--out-dir"):
        de.add_argument(f, required=True)
    sp.add_parser("preflight")
    a = ap.parse_args()
    {"imports": cmd_imports, "preflight": cmd_preflight, "feats-ut": cmd_feats_ut, "feats-oiv7": cmd_feats_oiv7,
     "decide": cmd_decide}[a.cmd](a)


if __name__ == "__main__":
    main()
