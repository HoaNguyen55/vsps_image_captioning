#!/usr/bin/env python3
"""C-PVR-T1 per-image SigLIP2 embeddings (Paper C, H2; CC-277 Ruling 3, CC-280 Ruling 2, AM5, AD2). A thin wrapper:
cen_pool.embed() (sha check before open, batches of 64, L2 norm, an unreadable image = STOP) and cen_pool's encode
(fp16, get_image_features) run unchanged; scripts/c_en/cen_pool.py and cen_fetch.py are imported behind their shas.
cen_pool's encode is a closure inside its cmd_embed, so its three lines are repeated in cmd_embed below, verbatim.

    PY=~/venvs/c_pvr_gpu_<LK>/bin/python   (E-G: the main venv, CC-280 AM1)
    $PY -I -B scripts/c_pvr_gpu/c_pvr_embed.py selftest                                     CPU, synthetic only
    $PY -I -B scripts/c_pvr_gpu/c_pvr_embed.py fetch --out O      E-G (setup_host.sh siglip): the snapshot at SIGREV
    $PY -I -B scripts/c_pvr_gpu/c_pvr_embed.py embed --push D --tman SHA --snapshot S --out O         E-G, GPU
    $PY -I -B scripts/c_pvr_gpu/c_pvr_embed.py rekey --name N --pair NPZ TSV [--pair NPZ TSV] --out F    laptop

embed  D = /dev/shm/c_pvr_emb (0700): D/MANIFEST.sha256 = the pinned EMB_PUSH list ('<sha256>  images/<list>/<file>',
       written by `c_pvr_manifest.py queries images`), its sha = SHA; the file set under D must equal it, and every
       list must be one of the 8 E-G lists (AM5: no KT-C / COCO pixels, no confirm half, no other file). One npz per
       list, O/emb_<list>.files.npz (ids = FILE NAMES, vecs float32, meta) + .sha256: no id list goes to E-G.
rekey  laptop, after the pull: file names -> ids through the pinned Q TSVs ('id<TAB>file'), each a bijection; D-VI's
       two lists (d_vi_kt, d_vi_ov) become one npz. Vectors are copied, not recomputed.
Prints counts and shas only. Label: TIER 1 / DEV-EXPLORE.
"""
from __future__ import annotations

import argparse
import hashlib
import json
import os
import sys
import time
from pathlib import Path

import numpy as np

ROOT = Path(__file__).resolve().parents[2]
CODE = {"scripts/c_en/cen_pool.py": "79a45b2b22b134c4f24838bde2d03f291644514c69c107673d1d8e02d153fe60",
        "scripts/c_en/cen_fetch.py": "e51918e958ad86e832dd34fbf5ed86d2f7fc13cf41b602dfe537afa43af4c673"}  # c_en SUMS
SIG_REPO = "google/siglip2-so400m-patch14-384"  # prereg v1.2 l.459 (NB-ENC); revision = cen_pool.SIGREV e8e48729
SNAP = {  # every file of the snapshot at SIGREV: c_stage1/emb.npz (59e65f6f) meta snapshot_sha256, cen_pool's own check
    ".gitattributes": "34448b82c17d60fec9b65b1f093c115ddbaadc04beb1b0140b6bfed2e012a930",
    "README.md": "5c02af3cafc849e2acbc03630b4ef9de4cc3c29f8bbef613bf7484fe4be9a897",
    "config.json": "73477b47ae9a395f008f993ebd8fb5c16ce0b5e8419ffdf2f5b2183b260f9cff",
    "model.safetensors": "9f4f4a49f908ef0c979bce8ff5a5c0e88882dc6c5dc4304387cbbd152558e2c2",
    "preprocessor_config.json": "fb2817d3523ca3b666c859f15320c7138416bc38ffc515e2963f78c868c51c90",
    "special_tokens_map.json": "baec30ea10906f16adb8c18af7a34023002c1746542612b8b41c9f09e1351351",
    "tokenizer.json": "cb9140fae3ac5122c972d37adf83e1248471a38147ad76f8215c8872c6fd8322",
    "tokenizer.model": "61a7b147390c64585d6c3543dd6fc636906c9af3865a5548f27f31aee1d4c8e2",
    "tokenizer_config.json": "14afe629fe4959b9e0d51e1852b8d9f7ad074f90a1a7125a4fcdd17f06e78fc8",
}
LISTS = ("xm3600_vi", "ktvic_explore", "openviic_explore", "vitextvqa_dev", "t_a", "d_vi_kt", "d_vi_ov", "d_tc")  # AM5
CPL = None  # cen_pool, bound by load() after its sha (and cen_fetch's) match


def fault(msg: str):
    raise SystemExit(f"FAULT: {msg}")


def sha(b: bytes) -> str:
    return hashlib.sha256(b).hexdigest()


def load(root: Path = ROOT) -> None:
    global CPL
    for rel, h in CODE.items():
        if sha((root / rel).read_bytes()) != h:
            fault(f"{rel} differs from its pin {h[:8]}; nothing is imported")
    sys.path.insert(0, str(root / "scripts/c_en"))
    import cen_pool as CPL  # noqa: E402  SIGREV, BATCH, embed (cen_fetch: sha_file)


def snap_ok(d: Path, want: dict = SNAP) -> dict:
    """The snapshot dir is the revision's, and every file in it is a pinned file with its sha (cmd_embed's check)."""
    got = {p.name: CPL.F.sha_file(p) for p in sorted(d.iterdir()) if p.is_file()}
    if d.name != CPL.SIGREV or got != want:
        fault(f"SigLIP2 snapshot {d.name[:8]} differs from {CPL.SIGREV[:8]} / its file pins")
    return got


def fetch(out: Path) -> None:
    from huggingface_hub import snapshot_download
    snap = Path(snapshot_download(SIG_REPO, revision=CPL.SIGREV, allow_patterns=sorted(SNAP)))
    snap_ok(snap)
    (out / "siglip2_snapshot.path").write_text(f"{snap}\n")
    print("siglip2 ok", SIG_REPO, CPL.SIGREV, " ".join(h[:8] for h in SNAP.values()))


def push_rows(push: Path, tman: str) -> dict:
    """The arrival check (host v3 §4.2): manifest sha = the pin, the dir is 0700, the files = the manifest exactly,
    every list an E-G list. -> {list: [(file, file, sha256)]} in file order."""
    man = push / "MANIFEST.sha256"
    b = man.read_bytes()
    if sha(b) != tman or push.stat().st_mode & 0o777 != 0o700:
        fault("EMB_PUSH MANIFEST.sha256 differs from the pin, or the push dir is not 0700")
    want = {p: h for h, p in (x.split("  ", 1) for x in b.decode().splitlines())}
    have = {str(Path(t, f).relative_to(push)) for t, _, fs in os.walk(push) for f in fs} - {"MANIFEST.sha256"}
    if have != set(want):
        fault(f"push dir file set differs from MANIFEST.sha256 ({len(have - set(want))} extra, "
              f"{len(set(want) - have)} missing)")
    out: dict = {}
    for p, h in sorted(want.items()):
        top, n, f = p.split("/")
        if top != "images" or n not in LISTS:
            fault(f"{n!r} is not an E-G list (CC-280 AM5)")
        out.setdefault(n, []).append((f, f, h))
    return out


def embed_push(push: Path, tman: str, out: Path, encode, meta: dict) -> dict:
    rows = push_rows(push, tman)
    out.mkdir(parents=True)  # a new dir: nothing is overwritten
    rep = {}
    for n, r in rows.items():
        vecs, bad = CPL.embed(n, r, push / "images" / n, encode, float("inf"))  # n != "memory": unreadable = STOP
        f = out / f"emb_{n}.files.npz"
        np.savez(f, ids=np.array([x[0] for x in r]), vecs=vecs, meta=json.dumps(meta | {"list": n, "n": len(r)}))
        Path(f"{f}.sha256").write_text(f"{sha(f.read_bytes())}  {f.name}\n")
        rep[n] = len(r)
    return rep


def cmd_embed(a) -> None:
    import PIL
    import torch
    import transformers
    from transformers import AutoModel, AutoProcessor

    snap = snap_ok(a.snapshot)
    proc = AutoProcessor.from_pretrained(a.snapshot)
    net = AutoModel.from_pretrained(a.snapshot, torch_dtype=torch.float16).eval().cuda()

    def encode(ims):
        with torch.no_grad():
            return net.get_image_features(**proc(images=ims, return_tensors="pt").to("cuda", torch.float16)
                                          ).float().cpu().numpy()

    meta = {"model": SIG_REPO, "revision": CPL.SIGREV, "dtype": "float16", "batch": CPL.BATCH, "snapshot_sha256": snap,
            "push_sha256": a.tman, "keys": "file names (c_pvr_embed.py rekey maps them to ids on the laptop)",
            "code_sha256": {"c_pvr_embed.py": sha(Path(__file__).read_bytes()), **CODE},
            "packages": {"torch": torch.__version__, "transformers": transformers.__version__,
                         "numpy": np.__version__, "pillow": PIL.__version__},
            "utc": time.strftime("%Y-%m-%dT%H:%M:%SZ", time.gmtime())}
    print(json.dumps({"embedded": embed_push(a.push, a.tman, a.out, encode, meta)}, sort_keys=True))


def rekey(name: str, pairs: list, out: Path) -> dict:
    """File-keyed E-G npz -> id-keyed npz for the builder (ids, vecs, meta); each (npz, tsv) a bijection."""
    if out.exists():
        fault(f"{out.name} exists")
    ids, vecs, src = [], [], []
    for npz, t in pairs:
        b, tb = npz.read_bytes(), t.read_bytes()
        rows = [x.split("\t") for x in tb.decode().splitlines()]
        of = {f: i for i, f in rows}
        z = np.load(npz)
        files = [str(x) for x in z["ids"].tolist()]
        if len(of) != len(rows) or len(files) != len(set(files)) or set(files) != set(of):
            fault(f"{npz.name}: its file names are not exactly the files of {t.name}")
        ids += [of[f] for f in files]
        vecs.append(np.asarray(z["vecs"]))
        src.append({"npz_sha256": sha(b), "tsv": t.name, "tsv_sha256": sha(tb), "meta": json.loads(str(z["meta"]))})
    if len(ids) != len(set(ids)):
        fault(f"{name}: an id occurs in two lists")
    np.savez(out, ids=np.array(ids), vecs=np.concatenate(vecs), meta=json.dumps({"name": name, "sources": src}))
    h = sha(out.read_bytes())
    Path(f"{out}.sha256").write_text(f"{h}  {out.name}\n")
    return {"name": name, "n": len(ids), "sha256": h}


# ---------------------------------------------------------------------------------------------- selftest (CPU)
def _must(msg: str, fn, *a, **k) -> None:
    try:
        fn(*a, **k)
    except SystemExit as e:
        assert msg in str(e), (msg, str(e))
    else:
        raise AssertionError(f"no FAULT: {msg}")


def selftest() -> None:
    import tempfile

    from PIL import Image

    load()
    enc = lambda ims: np.array([[float(np.asarray(i).mean()) + 1, 1.0] for i in ims])  # noqa: E731
    with tempfile.TemporaryDirectory() as td:
        w = Path(td)
        push = w / "push"
        files = {"xm3600_vi": ["aa01.jpg", "aa02.jpg"], "d_vi_kt": ["00000000002.jpg"], "d_vi_ov": ["00000000002.jpg"]}
        lines = {}
        for n, fs in files.items():
            (push / "images" / n).mkdir(parents=True)
            for k, f in enumerate(fs):
                p = push / "images" / n / f
                Image.fromarray(np.full((8, 8, 3), 40 * k + len(n), np.uint8)).save(p, "JPEG")
                lines[f"images/{n}/{f}"] = sha(p.read_bytes())
        man = "".join(f"{h}  {p}\n" for p, h in sorted(lines.items())).encode()
        (push / "MANIFEST.sha256").write_bytes(man)
        push.chmod(0o700)
        _must("differs from the pin", embed_push, push, "0" * 64, w / "o0", enc, {})
        push.chmod(0o755)
        _must("not 0700", embed_push, push, sha(man), w / "o0", enc, {})
        push.chmod(0o700)
        (push / "images/xm3600_vi/stray.jpg").write_bytes(b"x")  # a file outside the pinned list (e.g. a confirm half)
        _must("1 extra", embed_push, push, sha(man), w / "o0", enc, {})
        (push / "images/xm3600_vi/stray.jpg").unlink()
        rep = embed_push(push, sha(man), w / "o", enc, {"model": "fake"})
        assert rep == {"d_vi_kt": 1, "d_vi_ov": 1, "xm3600_vi": 2}, rep
        z = np.load(w / "o/emb_xm3600_vi.files.npz")
        assert z["ids"].tolist() == files["xm3600_vi"] and np.allclose(np.linalg.norm(z["vecs"], axis=1), 1)
        assert json.loads(str(z["meta"])) == {"model": "fake", "list": "xm3600_vi", "n": 2}
        h, f = (w / "o/emb_xm3600_vi.files.npz.sha256").read_text().split()
        assert h == sha((w / "o" / f).read_bytes())
        try:
            embed_push(push, sha(man), w / "o", enc, {})
            raise AssertionError("an existing out dir is reused")
        except FileExistsError:
            pass
        bad = {**lines, "images/kt_c/COCO_val2014_000000000001.jpg": "0" * 64}  # AM5: no KT-C pixels on E-G
        (push / "images/kt_c").mkdir()
        (push / "images/kt_c/COCO_val2014_000000000001.jpg").write_bytes(b"x")
        man2 = "".join(f"{h}  {p}\n" for p, h in sorted(bad.items())).encode()
        (push / "MANIFEST.sha256").write_bytes(man2)
        _must("not an E-G list", embed_push, push, sha(man2), w / "o2", enc, {})
        (push / "images/kt_c/COCO_val2014_000000000001.jpg").unlink()
        (push / "images/kt_c").rmdir()
        p = push / "images/xm3600_vi/aa02.jpg"
        keep = p.read_bytes()
        p.write_bytes(keep[:-9] + b"\x00" * 9)
        (push / "MANIFEST.sha256").write_bytes(man)
        _must("differs from its fetch record", embed_push, push, sha(man), w / "o3", enc, {})  # sha before open
        lines2 = {**lines, "images/xm3600_vi/aa02.jpg": sha(b"\xff\xd8 broken")}
        p.write_bytes(b"\xff\xd8 broken")
        man3 = "".join(f"{h}  {q}\n" for q, h in sorted(lines2.items())).encode()
        (push / "MANIFEST.sha256").write_bytes(man3)
        _must("cannot be opened", embed_push, push, sha(man3), w / "o4", enc, {})  # a query image: STOP

        snap = w / CPL.SIGREV
        snap.mkdir()
        (snap / "config.json").write_bytes(b"{}")
        assert snap_ok(snap, {"config.json": sha(b"{}")}) == {"config.json": sha(b"{}")}
        _must("differs from", snap_ok, snap)
        (snap / "extra.bin").write_bytes(b"")
        _must("differs from", snap_ok, snap, {"config.json": sha(b"{}")})
        other = w / ("0" * 40)
        other.mkdir()
        (other / "config.json").write_bytes(b"{}")
        _must("differs from", snap_ok, other, {"config.json": sha(b"{}")})

        (w / "kt.tsv").write_text("2\t00000000002.jpg\n")
        (w / "ov.tsv").write_text("00000000002.jpg\t00000000002.jpg\n")
        r = rekey("d_vi", [(w / "o/emb_d_vi_kt.files.npz", w / "kt.tsv"), (w / "o/emb_d_vi_ov.files.npz", w / "ov.tsv")],
                  w / "emb_d_vi.npz")
        z = np.load(w / "emb_d_vi.npz")
        assert r["n"] == 2 and z["ids"].tolist() == ["2", "00000000002.jpg"]
        assert np.array_equal(z["vecs"][0], np.load(w / "o/emb_d_vi_kt.files.npz")["vecs"][0])  # copied, not recomputed
        assert [s["tsv"] for s in json.loads(str(z["meta"]))["sources"]] == ["kt.tsv", "ov.tsv"]
        _must("exists", rekey, "d_vi", [(w / "o/emb_d_vi_kt.files.npz", w / "kt.tsv")], w / "emb_d_vi.npz")
        (w / "kt2.tsv").write_text("2\t00000000002.jpg\n3\t00000000003.jpg\n")
        _must("not exactly the files", rekey, "x", [(w / "o/emb_d_vi_kt.files.npz", w / "kt2.tsv")], w / "x.npz")
        (w / "kt3.tsv").write_text("00000000002.jpg\t00000000002.jpg\n")
        _must("an id occurs in two lists", rekey, "x", [(w / "o/emb_d_vi_kt.files.npz", w / "kt3.tsv"),
                                                         (w / "o/emb_d_vi_ov.files.npz", w / "ov.tsv")], w / "y.npz")
    print(f"selftest ok  c_pvr_embed.py {sha(Path(__file__).read_bytes())}  cen_pool {CODE['scripts/c_en/cen_pool.py'][:8]}")


def main() -> int:
    ap = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    sp = ap.add_subparsers(dest="cmd", required=True)
    sp.add_parser("selftest")
    sp.add_parser("fetch").add_argument("--out", type=Path, required=True)
    e = sp.add_parser("embed")
    for k in ("--push", "--snapshot", "--out"):
        e.add_argument(k, type=Path, required=True)
    e.add_argument("--tman", required=True)
    r = sp.add_parser("rekey")
    r.add_argument("--name", required=True)
    r.add_argument("--pair", nargs=2, type=Path, action="append", required=True, metavar=("NPZ", "TSV"))
    r.add_argument("--out", type=Path, required=True)
    a = ap.parse_args()
    load()
    if a.cmd == "selftest":
        return selftest()
    if a.cmd == "fetch":
        return fetch(a.out)
    if a.cmd == "embed":
        return cmd_embed(a)
    return print(json.dumps(rekey(a.name, a.pair, a.out), sort_keys=True))


if __name__ == "__main__":
    sys.exit(main())
