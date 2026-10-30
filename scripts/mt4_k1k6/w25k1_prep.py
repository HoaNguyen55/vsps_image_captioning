#!/usr/bin/env python3
"""W25-K1 glue (DEV_RULE §4, AMENDMENT_W25K1, CC-190): the inputs `k1k6.py w25k1 feats|decide` (frozen at c9a9054,
sha 4b511444, scripts/mt4_k1k6/SHA256SUMS) needs and does not build. Writes ids, file names, image sha256s and features
only; caption text is never printed or written (pool_rows tests caption presence only); never reads KV-4,224 or a gold
file. Feature code = build_memory.features with the CC-082 truncated retry (CC-193); readable rows identical to frozen
`k1k6.py w25k1 feats`. Every new set goes through the glue `feats`. WORK must be outside the repository.

    python3 w25k1_prep.py --selftest                                  no torch: synthetic; with torch + W25K1_SSCD: + JPEG
    $FT w25k1_prep.py lists --work W                                  pool_new.tsv, ktvic_test.tsv, openviic_test.tsv
    $FT w25k1_prep.py feats --list W/<x>.tsv --name <x> --sscd PT --work W   CC-193: W/<x>.npz (images = data/datasets)
    $FT w25k1_prep.py fetch --set uitviic_test|t2 --ann DIR --cen C_EN_DIR --sscd PT --work W   tmpfs fetch, feats, unlink
    $FT w25k1_prep.py pool --ut FEATS_UT --work W                     W/pool.npz = re-keyed UT-2,392 + W/pool_new.npz
    $FT w25k1_prep.py against --cen C_EN_DIR --parts W25_PARTS --work W   W/kv5000.npz, W/oiv7_val.npz (XM rows dropped)
    $FT w25k1_prep.py parity --cen C_EN_DIR --sscd PT --work W         CC-190 W7: 50 UT images vs feats_ut.npz
    $FT w25k1_prep.py check --work W                                CC-190 W4: run immediately before decide
    $FT k1k6.py w25k1 decide --pool W/pool.npz --sets W/{kv5000,oiv7_val,ktvic_test,uitviic_test,openviic_test,t2}.npz
"""
from __future__ import annotations

import argparse
import json
import os
import sys
from pathlib import Path

import numpy as np

HERE = Path(__file__).resolve().parent
sys.path.insert(0, str(HERE))
import k1k6 as KK  # noqa: E402  (also puts grl, w25, c_en on sys.path)
import w25  # noqa: E402
import cen_fetch as F  # noqa: E402

K = KK.K
ROOT = KK.ROOT
DATA = ROOT / "data/datasets"
SHM = Path("/dev/shm/k1k6_w25k1")  # the only place UIT-ViIC test and T2 bytes exist on the laptop (W25 RULE §5)
POOL_N = 15_249  # DEV_RULE §2 (c): 3,769 + 2,392 + 9,088
PINS = {
    "data/lb/sets/ktvic_test.tsv": "456243c0cfc82b0c3cc4ad52c694e11b4d9702f3ca14cd8103c3a82cd74a90eb",  # exclusion src
    "manuscript/prereg/2026-10-25_c_test/ov_test_files.tsv":
        "99d4fc49cc8283d1555d37b975cca5a32598ea0ec571d8bef8cf811df2c33695",  # C test PREREG l.15
    "data/datasets/uitviic/test_data.json": "54abc0fb068ad1108d7d57b21328d4d68bcf8f41aa168f80ec7c275fb4ac8214",
    "manuscript/prereg/2026-10-28_k2_gate1/w25_excluded_ids.txt":
        "f6151d28eeab924e9fd485dea5e63f0e1b6017384d1d33e2506d336bd0a3e599",  # W25 SHA256SUMS
}
FEATS_UT = "17d3ebf07ebf95bcd0c8bf123ff65fb8f2df65c52cd4e17ac492e05976b98c1d"
#: C-EN fetch/memory.sha256.tsv (M1 = M3 mirror): the first, positive T2 pin, 2,000/2,000 ids (CC-190 W3)
CEN_MEMORY = "553fb604c21b54e37cd980297d78fe388d5751561b495d61f13f1fc52eb1e852"
UV_TRAIN = "441d22d29eb7aa12d32d49e330778a4a918c3a9413c23294a9daec92a238d110"  # = common.SRC_PINS train_data.json
OIV7_PARTS = 72
SETS = {"kv5000": 5000, "oiv7_val": 41164, "ktvic_test": 558, "uitviic_test": 231, "openviic_test": 2001, "t2": 2000}
PARITY_N = 50  # CC-190 W7
#: CC-193 r3a: the truncated files each set must decode with the CC-082 retry, {id: (file sha256, bytes not processed)}
TRUNC = {
    "openviic_test": {
        "00000000768": ("404866ae511c2bfaa52339a40814316b916fb9d031c60d78f0da6d94d2ce733d", 18),
        "00000001010": ("96f9a3ab12df1c9be676dfd82b015559cf10073d49448db7c0cd073f00c264e7", 155),
        "00000005095": ("7f00285e59dc0bac1278060d02a9d39d5d9113b1fc73dc5525b49f3d822d6569", 76)},
    "pool_new": {"openviic:00000007169": ("4859dd1fc17d928fed15035b69c9964401cf327b33d4ca04b161b3d252fb9d20", 1)},
    "ktvic_test": {},
}
TRUNC_NEW_MAX = 3  # CC-193 r3b: a set without a TRUNC entry (uitviic_test, t2, parity) may log at most 3


def pinned(rel: str) -> Path:
    p = ROOT / rel
    if PINS[rel] and KK.sha(p) != PINS[rel]:
        raise SystemExit(f"REFUSED: {rel} differs from its pin")
    return p


def outside_repo(w: Path) -> Path:
    w = w.resolve()
    if w == ROOT or ROOT in w.parents:
        raise SystemExit(f"REFUSED: {w} is inside the repository; feature files are never committed (§4)")
    w.mkdir(parents=True, exist_ok=True)
    return w


def write_rows(p: Path, rows) -> None:
    p.write_text("".join("\t".join(map(str, r)) + "\n" for r in rows))


def w25_ut() -> set[int]:
    return {int(x) for x in pinned("manuscript/prereg/2026-10-28_k2_gate1/w25_excluded_ids.txt").read_text().split()}


# ------------------------------------------------------------------------------------------------ lists
def pool_keys(data: Path = DATA) -> list[tuple[str, str]]:
    """(key, path) of the K1 pool before W25-K1, from the frozen k1k6.pool_rows (keys never re-implemented)."""
    return [(k, p) for k, p, _ in KK.pool_rows(data, w25_ut(), set())]


def local_test(rel: str, folder: str, data: Path = DATA) -> list[tuple[str, str]]:
    """(stem, path) of a test set already on the laptop; every file sha-checked against its committed manifest."""
    rows = [x.split("\t") for x in pinned(rel).read_text().splitlines() if x]
    out = []
    for r in rows:
        f, h = (r[1], r[2]) if len(r) == 3 else (r[0], r[1])
        if KK.sha(data / folder / f) != h:
            raise SystemExit(f"FAULT: {folder}/{f} differs from {rel}")
        out.append((Path(f).stem, f"{folder}/{f}"))
    return out


def cmd_lists(a) -> None:
    w = outside_repo(Path(a.work))
    pool = [r for r in pool_keys() if not r[0].startswith("uitviic:")]  # UT side reuses feats_ut.npz
    write_rows(w / "pool_new.tsv", pool)
    write_rows(w / "ktvic_test.tsv", local_test("data/lb/sets/ktvic_test.tsv", "ktvic/images"))
    write_rows(w / "openviic_test.tsv", local_test("manuscript/prereg/2026-10-25_c_test/ov_test_files.tsv",
                                                   "openviic/images"))
    print(json.dumps({x: sum(1 for _ in open(w / f"{x}.tsv")) for x in ("pool_new", "ktvic_test", "openviic_test")}))


# ------------------------------------------------------------------------------------------------ tmpfs fetch
def memory_shas(cen: Path) -> dict[str, str]:
    """{coco id: sha256} of C-EN's memory fetch record, at its pin (CC-190 W3)."""
    f = cen / "fetch/memory.sha256.tsv"
    if KK.sha(f) != CEN_MEMORY:
        raise SystemExit(f"REFUSED: {f} differs from its pin 553fb604")
    return {r[0]: r[2] for r in (x.split("\t") for x in f.read_text().splitlines())}


def fetch_rows(name: str, ann: Path, cen: Path) -> tuple[list[tuple[str, str, str]], callable]:
    """(stem, file, url) and the body check check(stem, sha) -> error or "". Release JSONs are parsed by the loader;
    caption text is never printed or written.
    - uitviic_test: the release coco_url; every body's sha must be in exclusion.json image_sha256.uitviic_test, which
      equals data/lb/sets/uitviic_test.tsv col 3, 231/231 (CC-190 item 3).
    - t2: the pinned instances_val2014.json images[] coco_url (as cmd_stage; annotations never accessed); every body must
      equal its row of C-EN memory.sha256.tsv (553fb604, the first positive pin, CC-190 W3) and be no refused image.
    - parity: the first 50 sorted UT-2,402 ids from the UIT-ViIC train release (441d22d2); every body must equal its
      feats_ut.npz sha (CC-190 W7)."""
    ex = json.loads(K.pinned("manuscript/prereg/2026-10-21_dev_pools/exclusion.json").read_text())["image_sha256"]
    if name == "parity":
        ut = w25.load(cen.parent / "w25/feats_ut.npz", FEATS_UT)
        want = {str(i): h for i, h in zip(ut["ids"], ut["sha"])}
        ids = sorted(K.ids("ut2402"))[:PARITY_N]
        f = ROOT / "data/datasets/uitviic/train_data.json"
        if KK.sha(f) != UV_TRAIN:
            raise SystemExit("REFUSED: uitviic/train_data.json differs from its pin")
        url = {int(i["id"]): i["coco_url"] for i in json.loads(f.read_text(encoding="utf-8"))["images"]}
        rows = [(str(i), f"{i:012d}.jpg", url[i]) for i in ids]
        return rows, lambda s, h: "" if want[s] == h else "sha differs from feats_ut.npz"
    if name == "uitviic_test":
        ims = json.loads(pinned("data/datasets/uitviic/test_data.json").read_text(encoding="utf-8"))["images"]
        rows = [(str(int(i["id"])), f"{int(i['id']):012d}.jpg", i["coco_url"]) for i in ims]
        want = set(ex["uitviic_test"])
        if len(rows) != 231 or len(want) != 231:
            raise SystemExit("FAULT: UIT-ViIC test is not 231 images")
        return rows, lambda _s, h: "" if h in want else "sha not in exclusion.json uitviic_test"
    f = ann / "instances_val2014.json"
    if KK.sha(f) != KK.VAL2014_PIN:
        raise SystemExit("REFUSED: instances_val2014.json differs from its pin")
    ids = KK.set_ids("t2")
    url = {r["id"]: r["coco_url"] for r in json.loads(f.read_text())["images"] if r["id"] in set(ids)}
    mem = memory_shas(cen)
    if len(url) != len(ids) or any(str(i) not in mem for i in ids):  # set_ids pins t2_ids.txt (2,000)
        raise SystemExit("FAULT: a T2 id is not in instances_val2014 or in the C-EN memory record")
    bad = set().union(*map(set, ex.values())) | K.cen_test_shas(cen / "fetch", gpu_host=True)  # REFUSED if missing

    def check(s: str, h: str) -> str:
        return "a refused image sha" if h in bad else "" if h == mem[s] else "sha differs from memory.sha256.tsv"
    return [(str(i), f"{i:012d}.jpg", url[i]) for i in ids], check


def trunc_check(name: str, ids: list[str], f: dict) -> dict[str, tuple[str, int]]:
    """CC-193 r3b: {id: (sha, bytes)} of the files decoded with the truncated retry. FAULT if an image is still
    unreadable, a pinned set's record differs from TRUNC, an unpinned set has more than 3, or an SSCD row is
    non-finite."""
    got = {ids[i]: (f["sha"][i], b) for i, b in f["truncated"]}
    if f["unreadable"]:
        raise SystemExit(f"FAULT: {name}: {len(f['unreadable'])} image(s) unreadable after the CC-082 retry")
    if name in TRUNC and got != TRUNC[name]:
        raise SystemExit(f"FAULT: {name}: truncated files {got} differ from the pinned {TRUNC[name]}")
    if name not in TRUNC and len(got) > TRUNC_NEW_MAX:
        raise SystemExit(f"FAULT: {name}: {len(got)} truncated files (> {TRUNC_NEW_MAX})")
    if not np.isfinite(f["sscd"]).all():
        raise SystemExit(f"FAULT: {name}: a non-finite SSCD row")
    return got


def glue_feats(lst: Path, images: Path, name: str, sscd: str, out: Path) -> None:
    """CC-193 (a'): build_memory.features with retry_truncated=True on the whole set (readable rows take the frozen
    path unchanged); the truncated record goes into the npz meta and stdout."""
    rows = [x.split("\t") for x in Path(lst).read_text().splitlines() if x]
    ids = [r[0] for r in rows]
    f = w25.bm().features([Path(images) / r[1] for r in rows], sscd, workers=8, retry_truncated=True)
    got = trunc_check(name, ids, f)
    w25.save(out, ids, f, set=name, utc=KK.utc(), truncated_decoded=got)
    print(json.dumps({"set": name, "n": len(ids), "truncated_decoded": got}))


def cmd_feats(a) -> None:
    w = outside_repo(Path(a.work))
    glue_feats(Path(a.list), DATA, a.name, str(w25.ok_sscd(Path(a.sscd))), w / f"{a.name}.npz")


def tmpfs_feats(name: str, rows, check, out: Path, sscd: str, get=F.get, feats=None, shm: Path = SHM) -> None:
    """Fetch every body to tmpfs, sha-check it in memory (FAULT: not written), feature the folder with glue_feats
    (CC-193), then unlink the folder and log it, also on any failure. A lost image is a FAULT (never partial)."""
    feats = feats or glue_feats
    folder = shm / name
    folder.mkdir(parents=True, exist_ok=False)
    try:
        for stem, fn, url in rows:
            b, err = get(url)
            if b is None:
                raise SystemExit(f"FAULT: {name} {stem} not fetched ({err}); a test set is never partial")
            if bad := check(stem, F.sha_bytes(b)):
                raise SystemExit(f"FAULT: {name} {stem}: {bad}; not written")
            (folder / fn).write_bytes(b)
        write_rows(folder / ".list.tsv", [(s, fn) for s, fn, _ in rows])
        feats(folder / ".list.tsv", folder, name, sscd, out)
    finally:
        w25.drop(folder, out.parent / "deletions.log", f"after {name} features")


def cmd_fetch(a) -> None:
    w = outside_repo(Path(a.work))
    rows, check = fetch_rows(a.set, Path(a.ann), Path(a.cen))
    tmpfs_feats(a.set, rows, check, w / f"{a.set}.npz", str(w25.ok_sscd(Path(a.sscd))))


def parity(ref: dict, new: dict) -> dict:
    """CC-190 W7: laptop features of the same images equal feats_ut.npz: pHash/dHash (and mirrors) exactly, SSCD
    cosine >= 0.999 on every row, else FAULT (back to the judge)."""
    at = {int(i): n for n, i in enumerate(ref["ids"])}
    rows = [at[int(i)] for i in new["ids"]]
    same = all(np.array_equal(ref[k][rows], new[k]) for k in w25.KEYS[:4])
    x, y = ref["sscd"][rows], new["sscd"]
    cos = (x * y).sum(1) / (np.linalg.norm(x, axis=1) * np.linalg.norm(y, axis=1))
    rec = {"n": len(rows), "hashes_equal": bool(same), "sscd_cos_min": float(cos.min())}
    if not same or len(rows) != PARITY_N or not (cos >= 0.999).all():
        raise SystemExit(f"FAULT: feature parity failed {rec}")
    return rec


def cmd_parity(a) -> None:
    w = outside_repo(Path(a.work))
    rows, check = fetch_rows("parity", Path("."), Path(a.cen))
    tmpfs_feats("parity", rows, check, w / "parity.npz", str(w25.ok_sscd(Path(a.sscd))))
    print(json.dumps(parity(w25.load(Path(a.cen).parent / "w25/feats_ut.npz", FEATS_UT), w25.load(w / "parity.npz"))))
    (w / "parity.npz").unlink()  # never a decide input


def check_work(w: Path, want_pool: set[str], sets: dict[str, int] = SETS) -> dict:
    """CC-190 W4, immediately before the one decide: WORK holds exactly pool.npz + the six set stems (pool_new.npz may
    stay), each with its stated count, no duplicate id and 0 unreadable; pool keys == pool_rows. Returns input shas."""
    have = {p.stem for p in w.glob("*.npz")} - {"pool_new"}
    if have != {"pool", *sets}:
        raise SystemExit(f"FAULT: WORK npz stems are {sorted(have)}, not pool + {sorted(sets)}")
    for s, n in [("pool", len(want_pool)), *sets.items()]:
        f = w25.load(w / f"{s}.npz")
        if len(f["ids"]) != n or len(set(f["ids"])) != n or f["unreadable"]:
            raise SystemExit(f"FAULT: {s}.npz has {len(f['ids'])} rows ({len(set(f['ids']))} distinct, "
                             f"{len(f['unreadable'])} unreadable), not {n}")
        if s == "pool" and set(f["ids"]) != want_pool:
            raise SystemExit("FAULT: pool.npz keys are not the pool_rows keys")
    return {f"{s}.npz": KK.sha(w / f"{s}.npz") for s in ["pool", *sets]}


def cmd_check(a) -> None:
    w = outside_repo(Path(a.work))
    want = {k for k, _ in pool_keys()}
    if len(want) != POOL_N:
        raise SystemExit(f"FAULT: pool_rows gives {len(want)}, not {POOL_N}")
    shas = check_work(w, want)
    print(json.dumps({"ok": True, "inputs_sha256": shas, "decide": f"k1k6.py w25k1 decide --pool {w}/pool.npz --sets "
                      + " ".join(f"{w}/{s}.npz" for s in SETS)}, indent=1))


# ------------------------------------------------------------------------------------------------ pool, against
def rekey_pool(ut: dict, new: dict, drop: set[int], want: set[str]) -> dict:
    """UT-2,402 features re-keyed to 'uitviic:<id>' minus the K2 W25 ids, then the new pool features; the key set must
    equal the frozen pool_rows keys exactly (a key drift would make every exclusion a no-op)."""
    keep = [i for i, x in enumerate(ut["ids"]) if int(x) not in drop]
    ut = {"ids": [f"uitviic:{int(ut['ids'][i])}" for i in keep], "sha": [ut["sha"][i] for i in keep],
          **{k: ut[k][keep] for k in w25.KEYS}, "unreadable": ut["unreadable"]}
    p = w25.concat([ut, new])
    if p["unreadable"] or len(set(p["ids"])) != len(p["ids"]) or set(p["ids"]) != want:
        raise SystemExit("FAULT: the pool features are not exactly the K1 pool keys")
    return p


def save(out: Path, f: dict, **meta) -> None:
    w25.save(out, f["ids"], {**f, "unreadable": []}, **meta)


def cmd_pool(a) -> None:
    w = outside_repo(Path(a.work))
    p = rekey_pool(w25.load(Path(a.ut), FEATS_UT), w25.load(w / "pool_new.npz"), w25_ut(), {k for k, _ in pool_keys()})
    if len(p["ids"]) != POOL_N:
        raise SystemExit(f"FAULT: pool is {len(p['ids'])}, not {POOL_N}")
    save(w / "pool.npz", p, set="k1_pool", ut_feats=FEATS_UT, utc=KK.utc())
    print(json.dumps({"n": POOL_N, "sha256": KK.sha(w / "pool.npz")}))


def cmd_against(a) -> None:
    """KV-5,000 and OIV7 val (41,164) from W25's own inputs(): C-EN features at their pins, the 43 XM3600 NoCaps rows
    dropped by id (CC-153 r4), plus the 72 W25 parts checked against W25's SHA256SUMS."""
    w = outside_repo(Path(a.work))
    w25.CEN_OUT = Path(a.cen)
    kv, noc, rest = w25.inputs()
    parts = Path(a.parts)
    sums = {f: h for h, f in (x.split("  ") for x in (parts.parent / "SHA256SUMS").read_text().splitlines())}
    names = [f"oiv7_parts/part_{n:04d}.npz" for n in range(OIV7_PARTS)]
    oiv7 = w25.concat([w25.load(parts.parent / n, sums[n]) for n in names] + [noc])
    if sorted(oiv7["ids"]) != sorted(rest + noc["ids"]) or len(oiv7["ids"]) != w25.OIV7_COMPARED:
        raise SystemExit("FAULT: OIV7 features are not the 41,164 compared images")
    save(w / "kv5000.npz", kv, set="kv5000", from_="feats_coco_kval.npz 9783f7a6")
    save(w / "oiv7_val.npz", oiv7, set="oiv7_val", from_="72 W25 parts + feats_nocaps_val b69dac29 minus 43 XM rows")
    print(json.dumps({"kv5000": len(kv["ids"]), "oiv7_val": len(oiv7["ids"])}))


# ------------------------------------------------------------------------------------------------ selftest
def selftest() -> None:
    import tempfile

    def fz(ids, base):
        n = len(ids)
        return {"ids": list(ids), "sha": [f"s{base + i}" for i in range(n)], "unreadable": [],
                **{k: np.arange(base, base + n, dtype=np.uint64) for k in w25.KEYS[:4]},
                "sscd": np.repeat(np.arange(base, base + n, dtype=np.float32)[:, None], 4, 1)}

    # re-key, drop the K2 W25 ids, rows stay aligned; a key drift FAULTs
    p = rekey_pool(fz([368, 419, 431], 0), fz(["ktvic:1", "openviic:00000000002"], 10), {419},
                   {"uitviic:368", "uitviic:431", "ktvic:1", "openviic:00000000002"})
    assert p["ids"] == ["uitviic:368", "uitviic:431", "ktvic:1", "openviic:00000000002"], p["ids"]
    assert p["phash"].tolist() == [0, 2, 10, 11] and p["sha"] == ["s0", "s2", "s10", "s11"]
    assert p["sscd"][:, 0].tolist() == [0, 2, 10, 11]
    try:
        rekey_pool(fz([368], 0), fz(["ktvic:00000000001"], 10), set(), {"uitviic:368", "ktvic:1"})
        raise AssertionError("key drift passed")
    except SystemExit:
        pass
    with tempfile.TemporaryDirectory() as t:
        t = Path(t)
        shm, out = t / "shm", t / "w" / "x.npz"
        out.parent.mkdir()
        rows = [("7", "000000000007.jpg", "u/7"), ("9", "000000000009.jpg", "u/9")]
        body = {"u/7": b"\xff\xd8seven", "u/9": b"\xff\xd8nine"}
        good = {F.sha_bytes(b) for b in body.values()}
        seen = []

        def feats(lst, images, name, sscd, o):
            seen.append(sorted(p.name for p in images.iterdir()))
            o.write_text(lst.read_text())

        tmpfs_feats("s", rows, lambda _s, h: "" if h in good else "bad", out, "pt", lambda u: (body[u], ""), feats, shm)
        assert seen == [[".list.tsv", "000000000007.jpg", "000000000009.jpg"]] and not (shm / "s").exists()
        assert out.read_text() == "7\t000000000007.jpg\n9\t000000000009.jpg\n"
        assert "deleted" in (out.parent / "deletions.log").read_text()
        for check, get, fe in ((lambda _s, h: "refused", lambda u: (body[u], ""), feats),  # wrong sha: nothing written
                               (lambda _s, h: "", lambda u: (None, "status 404"), feats),  # lost image
                               (lambda _s, h: "", lambda u: (body[u], ""), lambda *_: 1 / 0)):  # features crash
            try:
                tmpfs_feats("s", rows, check, t / "w" / "y.npz", "pt", get, fe, shm)
                raise AssertionError("passed")
            except (SystemExit, ZeroDivisionError):
                pass
            assert not (shm / "s").exists() and not (t / "w" / "y.npz").exists()
        # never captions: a sentinel caption in the release JSON reaches no returned row
        (t / "data/datasets/uitviic").mkdir(parents=True)
        (t / "data/datasets/uitviic/test_data.json").write_text(json.dumps({
            "images": [{"id": i, "coco_url": f"u/{i}"} for i in range(231)],
            "annotations": [{"image_id": i, "caption": "SENTINEL_CAPTION"} for i in range(231)]}))
        (t / "ex.json").write_text(json.dumps({"image_sha256": {"uitviic_test": [str(i) for i in range(231)]}}))
        keep = dict(PINS), K.pinned, ROOT
        try:
            PINS["data/datasets/uitviic/test_data.json"] = None
            K.pinned, globals()["ROOT"] = (lambda _r: t / "ex.json"), t
            rows, check = fetch_rows("uitviic_test", t, t)
        finally:
            PINS.update(keep[0])
            K.pinned, globals()["ROOT"] = keep[1], keep[2]
        assert len(rows) == 231 and "SENTINEL" not in json.dumps(rows) and not check("0", "5") and check("0", "x")
        # T2: positive pin against the C-EN memory record; a mismatching body FAULTs and nothing is written
        (t / "ann").mkdir()
        (t / "ann/instances_val2014.json").write_text(json.dumps({"images": [
            {"id": 7, "coco_url": "u/7"}, {"id": 9, "coco_url": "u/9"}], "annotations": [{"image_id": 7}]}))
        (t / "fetch").mkdir()
        mem = {"7": F.sha_bytes(body["u/7"]), "9": F.sha_bytes(b"other bytes")}
        (t / "fetch/memory.sha256.tsv").write_text("".join(f"{i}\tf.jpg\t{h}\t1\n" for i, h in mem.items()))
        keep = KK.VAL2014_PIN, KK.set_ids, K.cen_test_shas, K.pinned, CEN_MEMORY
        try:
            KK.VAL2014_PIN = KK.sha(t / "ann/instances_val2014.json")
            KK.set_ids, K.cen_test_shas = (lambda _n: [7, 9]), (lambda *_a, **_k: {"refusedsha"})
            K.pinned = lambda _r: t / "ex.json"
            globals()["CEN_MEMORY"] = KK.sha(t / "fetch/memory.sha256.tsv")
            rows2, check2 = fetch_rows("t2", t / "ann", t)
            assert [r[0] for r in rows2] == ["7", "9"] and not check2("7", mem["7"])
            assert check2("9", F.sha_bytes(b"\xff\xd8nine")) and check2("7", "refusedsha")
            try:
                tmpfs_feats("t2", rows2, check2, t / "w" / "t2.npz", "pt", lambda u: (body[u], ""), feats, shm)
                raise AssertionError("T2 sha mismatch passed")
            except SystemExit as e:
                assert "memory.sha256.tsv" in str(e)
            assert not (shm / "t2").exists() and not (t / "w" / "t2.npz").exists()
        finally:
            KK.VAL2014_PIN, KK.set_ids, K.cen_test_shas, K.pinned, globals()["CEN_MEMORY"] = keep
        # W4 check: exact stems and counts; an extra or short set FAULTs
        cw = t / "cw"
        cw.mkdir()
        small = {"a": 2, "b": 1}
        save(cw / "pool.npz", fz(["k:1", "k:2"], 0))
        save(cw / "a.npz", fz(["x", "y"], 0))
        save(cw / "b.npz", fz(["z"], 0))
        assert set(check_work(cw, {"k:1", "k:2"}, small)) == {"pool.npz", "a.npz", "b.npz"}
        for bad_case in (lambda: check_work(cw, {"k:1", "k:3"}, small), lambda: check_work(cw, {"k:1", "k:2"}, {"a": 2}),
                         lambda: check_work(cw, {"k:1", "k:2"}, {"a": 3, "b": 1})):
            try:
                bad_case()
                raise AssertionError("check passed")
            except SystemExit:
                pass
        save(cw / "a.npz", fz(["x", "x"], 0))
        try:
            check_work(cw, {"k:1", "k:2"}, small)
            raise AssertionError("duplicate ids passed")
        except SystemExit:
            pass
        # W7 parity: equal hashes and SSCD pass; one flipped hash bit FAULTs
        ids = list(range(PARITY_N))
        ref, new = fz(ids[::-1] + [999], 1), fz(ids[::-1] + [999], 1)
        new = {**new, "ids": new["ids"][:PARITY_N], **{k: new[k][:PARITY_N] for k in w25.KEYS}}
        assert parity(ref, new)["hashes_equal"]
        new["dhash"] = new["dhash"].copy()
        new["dhash"][0] ^= np.uint64(1)
        try:
            parity(ref, new)
            raise AssertionError("parity passed with a changed hash")
        except SystemExit:
            pass
        try:
            outside_repo(ROOT / "x")
            raise AssertionError("work dir inside the repo passed")
        except SystemExit:
            pass
    selftest_trunc()
    if os.environ.get("W25K1_SSCD"):
        with tempfile.TemporaryDirectory() as t:
            jpeg_selftest(Path(t), Path(os.environ["W25K1_SSCD"]))
    print("w25k1_prep selftest ok")


def selftest_trunc() -> None:
    """CC-193 r3b without torch: the truncated record and its FAULT conditions."""
    def fr(n, trunc=(), unread=()):
        return {"sha": [f"h{i}" for i in range(n)], "truncated": list(trunc), "unreadable": list(unread),
                "sscd": np.zeros((n, 2), np.float32)}

    keep = dict(TRUNC)
    try:
        TRUNC["pinned"] = {"b": ("h1", 7)}
        assert trunc_check("pinned", ["a", "b"], fr(2, [(1, 7)])) == {"b": ("h1", 7)}
        assert trunc_check("free", ["a", "b"], fr(2, [(1, 7)])) == {"b": ("h1", 7)}
        bad = [("pinned", fr(2)), ("pinned", fr(2, [(0, 7)])), ("pinned", fr(2, [(1, 7)], [0])),
               ("free", fr(4, [(0, 1), (1, 1), (2, 1), (3, 1)])),
               ("free", {**fr(2), "sscd": np.full((2, 2), np.nan, np.float32)})]
        for name, f in bad:
            try:
                trunc_check(name, ["a", "b", "c", "d"][:len(f["sha"])], f)
                raise AssertionError(f"trunc_check passed {name}")
            except SystemExit:
                pass
    finally:
        TRUNC.clear()
        TRUNC.update(keep)


def jpeg_selftest(t: Path, sscd: Path) -> None:
    """CC-193 r3d (torch venv): a JPEG cut by a few bytes gets finite features and a truncated record; pinned passes,
    unpinned or pinned-but-whole FAULTs; readable rows equal the strict path bit for bit; the PIL flag is reset."""
    from PIL import Image, ImageFile

    d = t / "jpg"
    d.mkdir()
    rng = np.random.default_rng(0)
    for n in range(3):
        Image.fromarray(rng.integers(0, 255, (64, 64, 3), np.uint8)).save(d / f"{n}.jpg", quality=90)
    (d / "2.jpg").write_bytes((d / "2.jpg").read_bytes()[:-40])
    (d / "l.tsv").write_text("a\t0.jpg\nb\t1.jpg\nc\t2.jpg\n")
    bm = w25.bm()
    f = bm.features([d / "0.jpg", d / "1.jpg", d / "2.jpg"], str(sscd), workers=2, retry_truncated=True)
    strict = bm.features([d / "0.jpg", d / "1.jpg"], str(sscd), workers=2)
    assert ImageFile.LOAD_TRUNCATED_IMAGES is False
    assert [i for i, _ in f["truncated"]] == [2] and np.isfinite(f["sscd"]).all() and not f["unreadable"]
    assert all(np.array_equal(f[k][:2], strict[k]) for k in w25.KEYS)
    pin = {"c": (KK.sha(d / "2.jpg"), f["truncated"][0][1])}
    keep = dict(TRUNC)
    try:
        TRUNC["syn"] = pin
        glue_feats(d / "l.tsv", d, "syn", str(sscd), d / "syn.npz")
        assert (d / "syn.npz").exists() and ImageFile.LOAD_TRUNCATED_IMAGES is False
        for tr in ({}, {**pin, "b": (KK.sha(d / "1.jpg"), 1)}):  # unpinned; pinned but not truncated
            TRUNC["syn"] = tr
            try:
                glue_feats(d / "l.tsv", d, "syn", str(sscd), d / "syn2.npz")
                raise AssertionError("glue_feats passed a wrong truncated pin")
            except SystemExit:
                pass
            assert not (d / "syn2.npz").exists()
    finally:
        TRUNC.clear()
        TRUNC.update(keep)
    print("w25k1_prep jpeg selftest ok")


def main() -> None:
    if sys.argv[1:] == ["--selftest"]:
        selftest()
        return
    ap = argparse.ArgumentParser()
    sp = ap.add_subparsers(dest="cmd", required=True)
    sp.add_parser("lists").add_argument("--work", required=True)
    f = sp.add_parser("fetch")
    f.add_argument("--set", choices=("uitviic_test", "t2"), required=True)
    for k in ("--ann", "--cen", "--sscd", "--work"):
        f.add_argument(k, required=True)
    p = sp.add_parser("pool")
    for k in ("--ut", "--work"):
        p.add_argument(k, required=True)
    g = sp.add_parser("against")
    for k in ("--cen", "--parts", "--work"):
        g.add_argument(k, required=True)
    fe = sp.add_parser("feats")
    for k in ("--list", "--name", "--sscd", "--work"):
        fe.add_argument(k, required=True)
    for name in ("parity", "check"):
        q = sp.add_parser(name)
        for k in ("--work",) + (("--cen", "--sscd") if name == "parity" else ()):
            q.add_argument(k, required=True)
    a = ap.parse_args()
    {"lists": cmd_lists, "fetch": cmd_fetch, "pool": cmd_pool, "against": cmd_against, "parity": cmd_parity, "feats": cmd_feats,
     "check": cmd_check}[a.cmd](a)


if __name__ == "__main__":
    main()
