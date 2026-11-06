#!/usr/bin/env python3
"""C-PVR-T1 manifest builder, laptop only (Paper C, plan P5: CC-270 PATH P5, Q4, N8; CC-272 N4-N6; CC-276 W1, W3, W5).
It writes everything the host reads, so the host never opens a source caption json (CC-276 W1).

    PY=~/.venvs/c_pvr/bin/python     (VnCoreNLP for D-VI, spaCy for D-EN / D-TC decompositions)
    $PY -I -B scripts/c_pvr_gpu/c_pvr_manifest.py selftest
    $PY -I -B scripts/c_pvr_gpu/c_pvr_manifest.py democap --ds D --src DIR --kept DIR --out O [--dry]
    $PY -I -B scripts/c_pvr_gpu/c_pvr_manifest.py set --set S --queries TSV --images DIR --qemb NPZ --demb NPZ
                                                 --kept DIR --out O [--a12 JSON] [--shots TSV]
    $PY -I -B scripts/c_pvr_gpu/c_pvr_manifest.py seal --out O

democap  the datastore's own rule (c_pvr_gpu.DEMOCAP_RULE, routed by datastore) on every kept id ->
         O/democap/<ds>.json {label, datastore, texts}. Prints counts and the sha, never a text. --src = the repo root
         for D-VI / D-EN (LISTS_IN and cen_fetch paths), the TextCaps download dir for D-TC. --dry: nothing written.
set      one tier-1 query set -> O/manifest/<set>.json. Per query: its image file and sha, the N_RANK kept ids by
         cosine of the pinned image embeddings (rank 1 first; ties to the smaller id [proposal]) and, on xm3600_vi,
         the A12 masks over A1's top K (CC-270 Q4: booleans only, no label leaves the laptop). demos = the
         decomposition of every id an arm can show (ranked ids, the A2 draws, the A5 shots and their ranked ids), its
         text equal to democap/<ds>.json (the N8 check). The consumer's own pool_check / a5_shots run before writing.
seal     every set present; the A5 shot images by sha against every tier-1 query image (CC-272 N5); writes
         O/MANIFEST.sha256 once, "<sha256>  <path under /dev/shm/c_pvr_hc>" (manifest/, democap/, kept/, images/).
Every file is written to a temp name, fsynced, then renamed (CC-270r2 N-S11a). Kept-id files are opened by their exact
KEPT names only (CC-276 W5). Embeddings are inputs (npz: ids, vecs); this script computes none. Label: TIER 1 /
DEV-EXPLORE.
"""
from __future__ import annotations

import argparse
import hashlib
import io
import json
import os
import sys
from pathlib import Path

import numpy as np

sys.path.insert(0, str(Path(__file__).resolve().parent))
import c_pvr_gpu as G  # noqa: E402  KEPT, DEMOCAP_RULE, kept_ids, guard, pool_check, a5_shots, SETS (one source)

N_RANK = 7  # CC-272 contract: >= 7 ranked kept ids per query (A9_POOL = A3_TOP = 7 >= K)
SIZES = {"xm3600_vi": 3600, "kt_c": 3907, "ktvic_explore": 286, "openviic_explore": 1020, "t_a": 1070,
         "vitextvqa_dev": 1676}  # host v3 §5; explore halves = c_pvr_lists.json (edb07fbb) "halves"
EXPLORE = {"ktvic_explore", "openviic_explore"}  # prereg §4.2 NB-PARITYBIT: CR.half(id) holds for every query


def sha(b: bytes) -> str:
    return hashlib.sha256(b).hexdigest()


def put(p: Path, b: bytes) -> str:
    """Temp name, fsync, rename in the same dir. A stale temp from a crashed run is a FAULT (inspect it first)."""
    p.parent.mkdir(parents=True, exist_ok=True)
    tmp = p.with_name(p.name + ".tmp")
    try:
        with open(tmp, "xb") as f:
            f.write(b)
            f.flush()
            os.fsync(f.fileno())
    except FileExistsError:
        G.fault(f"{tmp.name} exists: a crashed earlier write; inspect it, nothing is overwritten")
    os.replace(tmp, p)
    return sha(b)


def jbytes(o) -> bytes:
    return json.dumps(o, ensure_ascii=False, sort_keys=True).encode()


def democap(ds: str, src: Path, kdir: Path, out: Path, dry: bool = False) -> dict:
    kept = sorted(G.kept_ids(kdir, ds))
    texts = G.DEMOCAP_RULE[ds](kept, src)  # by DATASTORE; FAULTs on any id without a non-empty caption (W3)
    if sorted(texts) != kept or not all(texts.values()):
        G.fault(f"{ds}: the rule did not give one non-empty text per kept id")
    b = jbytes({"label": G.CP.LABEL, "datastore": ds, "texts": texts})
    rep = {"datastore": ds, "kept": len(kept), "texts": len(texts), "sha256": sha(b), "bytes": len(b), "dry": dry}
    if ds == "d_vi":  # N8 form counts (CC-269r2: 1,878 KTVIC form / 7,220 OpenViIC form on the real D-VI)
        rep["ktvic_form"] = sum(bool(G.CR.KT_ID.fullmatch(i)) for i in kept)
        rep["openviic_form"] = len(kept) - rep["ktvic_form"]
    if not dry:
        put(out / "democap" / f"{ds}.json", b)
    return rep


def emb(p: Path, ids: list[str]) -> tuple[np.ndarray, str]:
    """The rows of `ids`, in that order, L2-normalised; str-normalised npz ids (CC-261 N6); a missing or doubled id
    is a FAULT. Also returns the npz sha."""
    b = G.guard(p).read_bytes()
    z = np.load(io.BytesIO(b))
    have = [str(x) for x in z["ids"].tolist()]
    if len(have) != len(set(have)):
        G.fault(f"{p.name}: duplicate ids")
    row = {i: n for n, i in enumerate(have)}
    if miss := [i for i in ids if i not in row]:
        G.fault(f"{p.name}: {len(miss)} ids have no embedding row (first {miss[0]!r})")
    v = np.asarray(z["vecs"], dtype=np.float32)[[row[i] for i in ids]]
    return v / np.linalg.norm(v, axis=1, keepdims=True), sha(b)


def rank(qv: np.ndarray, dv: np.ndarray, n: int) -> list[list[int]]:
    """[proposal] the n best datastore rows per query by cosine, best first; equal cosines go to the lower row (the
    rows are in sorted-id order, so the smaller id). Exact at the n-th place: every row tied with it is a candidate."""
    out = []
    for i in range(0, len(qv), 256):
        for r in qv[i:i + 256] @ dv.T:
            cand = np.flatnonzero(r >= np.partition(r, -n)[-n])
            out.append(cand[np.lexsort((cand, -r[cand]))][:n].tolist())
    return out


def tsv(p: Path, paths: bool = False) -> list[tuple[str, str]]:
    """'id<TAB>image' lines: a bare file name under --images (queries: the tmpfs layout is flat) or, for --shots, a
    laptop path."""
    rows = [tuple(x.split("\t")) for x in G.guard(p).read_text("utf-8").splitlines()]
    if any(len(r) != 2 or not G.ID_RX.fullmatch(r[0]) or not r[1] or ("/" in r[1] and not paths) for r in rows):
        G.fault(f"{p.name}: not 'id<TAB>image file' lines")
    if len({r[0] for r in rows}) != len(rows) or len({r[1] for r in rows}) != len(rows):
        G.fault(f"{p.name}: a duplicate id or image")
    return rows


def build_set(s: str, queries: Path, images: Path, qemb: Path, demb: Path, kdir: Path, out: Path, decompose,
              a12: Path | None = None, shots: Path | None = None) -> dict:
    ds, _, arms = G.SETS[s]
    rows = tsv(queries)
    qids = [i for i, _ in rows]
    if len(rows) != SIZES[s] or (s in EXPLORE and not all(map(G.CR.half, qids))):
        G.fault(f"{s}: {len(rows)} queries, not the registered {SIZES[s]} (or not the explore half)")
    if ("A12" in arms) != (a12 is not None) or (ds == "d_vi") != (shots is not None):
        G.fault(f"{s}: --a12 iff the set runs A12 (CC-270 Q4); --shots iff D-VI (A5)")
    kept = sorted(G.kept_ids(kdir, ds))
    dsha = sha((out / "democap" / f"{ds}.json").read_bytes())
    texts = G.read_democap(out / "democap", ds, dsha, frozenset(kept))  # the host's own check of the derived file
    dv, dsh = emb(demb, kept)
    qv, qsh = emb(qemb, qids)
    ranked = [[kept[j] for j in r] for r in rank(qv, dv, N_RANK)]
    need = {i for r in ranked for i in r}
    if "A2" in arms:
        need |= {i for q, r in zip(qids, ranked) for i in G.CP.pick("A2", q, r, kept)}
    M = {"label": G.CP.LABEL, "set": s, "datastore": ds, "n_rank": N_RANK, "democap_sha256": dsha,
         "inputs": {"queries": sha(queries.read_bytes()), "qemb": qsh, "demb": dsh}}
    if shots is not None:
        srows = tsv(shots, paths=True)
        want = G.CP.a5_shot_ids(kept)
        if sorted(i for i, _ in srows) != sorted(want):
            G.fault("--shots ids differ from the SEEDS['A5'] draw over the kept D-VI ids")
        sv, _ = emb(demb, want)
        M["a5_shots"] = {sid: [kept[j] for j in r] for sid, r in zip(want, rank(sv, dv, N_RANK))}
        M["a5_shot_sha256"] = {i: sha(G.guard(Path(f)).read_bytes()) for i, f in srows}
        M["inputs"]["shots"] = sha(shots.read_bytes())
        need |= set(want) | {i for r in M["a5_shots"].values() for i in r}
    order = sorted(need)
    dcs = decompose([texts[i] for i in order])
    if [d["text"] for d in dcs] != [texts[i] for i in order]:
        G.fault(f"{s}: a decomposition text differs from democap/{ds}.json (N8)")
    M["demos"] = dict(zip(order, dcs))
    lab = json.loads(G.guard(a12).read_bytes()) if a12 else {}
    if a12:
        M["inputs"]["a12"] = sha(a12.read_bytes())
    M["queries"] = []
    for (q, img), r in zip(rows, ranked):
        rec = {"id": q, "image": img, "image_sha256": sha(G.guard(images / img).read_bytes()), "ranked": r}
        if a12:
            absent = set(lab.get(q, {}).get("absent", []))
            rec["a12_masks"] = G.CP.a12_masks([M["demos"][i] for i in r[:G.CP.K]],
                                              lambda c: "absent" if c in absent else "other")
        M["queries"].append(rec)
    for a in arms:  # the host's own checks, before anything is written (CC-272 N4)
        G.pool_check(G.EN_AS.get(a, a), M["queries"], M, frozenset(kept))
    if "A2" in arms and (miss := [i for q in M["queries"] for i in G.CP.pick("A2", q["id"], q["ranked"], kept)
                                  if i not in M["demos"]]):  # pool_check reads no ranked id for A2
        G.fault(f"{s}: {len(miss)} A2 draws have no demonstration")
    if shots is not None:
        G.a5_shots(M, frozenset(kept), set(qids))
    h = put(out / "manifest" / f"{s}.json", jbytes(M))
    return {"set": s, "queries": len(rows), "demos": len(order), "decomp_fail": sum("decomp_fail" in d for d in dcs),
            "a12_true": sum(v for q in M["queries"] for m in q.get("a12_masks", []) for v in m), "sha256": h}


def seal(out: Path) -> dict:
    """CC-272 N5 and the arrival manifest S11 pins (host v3 §4.2): every file the host gets, by sha, once."""
    man = out / "MANIFEST.sha256"
    if man.exists():
        G.fault("MANIFEST.sha256 exists: sealed once")
    lines, Ms = {}, {}
    for s, (ds, _, _) in G.SETS.items():
        b = (out / "manifest" / f"{s}.json").read_bytes()
        Ms[s], lines[f"manifest/{s}.json"] = json.loads(b), sha(b)
        lines[f"democap/{ds}.json"] = sha((out / "democap" / f"{ds}.json").read_bytes())
        if Ms[s]["democap_sha256"] != lines[f"democap/{ds}.json"] or Ms[s]["set"] != s:
            G.fault(f"manifest/{s}.json was built on another democap/{ds}.json")
        lines[f"kept/{G.KEPT[ds][0]}"] = G.KEPT[ds][2]
        for q in Ms[s]["queries"]:
            lines[f"images/{s}/{q['image']}"] = q["image_sha256"]
    shots = [M["a5_shot_sha256"] for M in Ms.values() if "a5_shot_sha256" in M]
    if any(x != shots[0] for x in shots):
        G.fault("the D-VI manifests disagree on the A5 shot images")
    if hit := set(shots[0].values()) & {q["image_sha256"] for M in Ms.values() for q in M["queries"]}:
        G.fault(f"{len(hit)} A5 shot images are tier-1 query images (by sha, CC-272 N5)")
    h = put(man, "".join(f"{v}  {k}\n" for k, v in sorted(lines.items())).encode())
    return {"files": len(lines), "sha256": h}


# ---------------------------------------------------------------------------------------------- selftest
def selftest() -> None:
    import socket
    import tempfile
    import types

    def no_net(*a, **k):
        raise OSError("selftest: network disabled")

    socket.socket, socket.create_connection = no_net, no_net  # type: ignore[assignment,misc]
    kept0, pins0, rule0, sizes0, dpin0 = dict(G.KEPT), dict(G.PINS), dict(G.DEMOCAP_RULE), dict(SIZES), dict(G.DEMO_PIN)
    sys.addaudithook(G._host_audit)
    try:
        with tempfile.TemporaryDirectory() as td:
            _st(Path(td), types)
    finally:
        G.KEPT.update(kept0)
        G.PINS.update(pins0)
        G.DEMOCAP_RULE.update(rule0)
        G.DEMO_PIN.update(dpin0)
        SIZES.update(sizes0)
    print(f"selftest ok  {G.CP.LABEL}  c_pvr_manifest.py {sha(Path(__file__).read_bytes())}  "
          f"c_pvr_gpu.py {sha(Path(G.__file__).read_bytes())}")


def _st(w: Path, types) -> None:
    assert rank(np.eye(3, dtype=np.float32)[[0]], np.array([[0, 1, 0], [1, 0, 0], [1, 0, 0], [.6, .8, 0]],
                                                           np.float32), 3) == [[1, 2, 3]]  # ties: the lower row first
    kdir, src, out = w / "kept", w / "src", w / "o"
    kdir.mkdir()
    (kdir / "t2pool_x_kept_ids.txt").write_bytes(b"zz\n")  # W5 decoy: the decode runs below (HOST set) never open it
    ids = {"d_vi": [str(j) for j in range(10, 30)], "d_en": [str(j) for j in range(10, 22)],
           "d_tc": [f"{j:016x}" for j in range(0xa0, 0xac)]}
    for ds, v in ids.items():
        body = "".join(f"{i}\n" for i in sorted(v)).encode()
        G.KEPT[ds] = (G.KEPT[ds][0], len(v), sha(body))
        (kdir / G.KEPT[ds][0]).write_bytes(body)
    vi = {i: f"Ba ấm đồng số{i} và một con mèo." for i in ids["d_vi"]}
    G.DEMOCAP_RULE.update(d_vi=lambda k, s: {i: vi[i] for i in k}, d_en=lambda k, s: {i: f"A zq kettle{i}." for i in k})
    data = [{"image_id": i, "caption_str": f"  A zq sign{n}  reads. "} for n, i in enumerate(ids["d_tc"])]
    tc = src / G.DEMO_PIN["textcaps_train"][0]
    tc.parent.mkdir(parents=True)
    tc.write_text(json.dumps({"data": data}))
    G.DEMO_PIN["textcaps_train"] = (tc.name, sha(tc.read_bytes()))  # D-TC: the real P4 rule
    reps = {ds: democap(ds, src if ds == "d_tc" else w, kdir, out, dry=ds == "d_en") for ds in ids}
    assert not (out / "democap/d_en.json").exists() and reps["d_en"]["texts"] == 12  # --dry writes nothing
    assert reps["d_vi"]["ktvic_form"] == 20 and reps["d_tc"]["texts"] == 12
    assert json.loads((out / "democap/d_tc.json").read_text())["texts"][ids["d_tc"][1]] == "A zq sign1 reads."
    democap("d_en", w, kdir, out)
    data[3]["caption_str"] = " \t "
    tc.write_text(json.dumps({"data": data}))
    G.DEMO_PIN["textcaps_train"] = (tc.name, sha(tc.read_bytes()))
    G._must("no caption", democap, "d_tc", src, kdir, w / "o_bad")  # W3: empty after clean()
    assert not (w / "o_bad").exists()
    (out / "democap/d_vi.json.tmp").write_bytes(b"")
    G._must("crashed earlier write", democap, "d_vi", w, kdir, out)
    (out / "democap/d_vi.json.tmp").unlink()

    rng = np.random.default_rng(7)
    allids = [*ids["d_vi"], *ids["d_en"], *ids["d_tc"]]
    vec = {i: rng.normal(size=8) * (1 + n % 5) for n, i in enumerate(sorted(set(allids)))}  # unequal norms, hash-seed free
    np.savez(w / "demb.npz", ids=np.array(list(vec)), vecs=np.stack(list(vec.values())))
    assert np.allclose(np.linalg.norm(emb(w / "demb.npz", ids["d_vi"])[0], axis=1), 1)  # cosine, not the raw dot
    img = w / "img"
    img.mkdir()
    shots = G.CP.a5_shot_ids(ids["d_vi"])
    for i in shots:
        (img / f"shot{i}.jpg").write_bytes(f"shot {i}".encode())
    (w / "shots.tsv").write_text("".join(f"{i}\t{img}/shot{i}.jpg\n" for i in shots))
    dec = lambda ts: [G._dc(t, [m for m in ("Ba ấm đồng", "một con mèo", "A zq") if m in t]) for t in ts]  # noqa: E731

    def mk(s, n=3, extra=()):
        qs = [f"{s[:3]}q{j}" for j in range(40) if s not in EXPLORE or G.CR.half(f"{s[:3]}q{j}")][:n]
        for q in qs:
            (img / f"{q}.jpg").write_bytes(f"img {q}".encode())
        (w / f"{s}.tsv").write_text("".join(f"{q}\t{q}.jpg\n" for q in qs))
        np.savez(w / f"{s}.npz", ids=np.array(qs + list(extra)), vecs=rng.normal(size=(n + len(extra), 8)))
        return qs

    SIZES.update({s: 3 for s in SIZES})
    (w / "a12.json").write_text(json.dumps({"xm3q0": {"absent": ["mèo"], "present": ["đồng"]}}, ensure_ascii=False))
    for s, (ds, _, _) in G.SETS.items():
        mk(s)
        kw = {"a12": w / "a12.json"} if s == "xm3600_vi" else {}
        r = build_set(s, w / f"{s}.tsv", img, w / f"{s}.npz", w / "demb.npz", kdir, out, dec,
                      shots=w / "shots.tsv" if ds == "d_vi" else None, **kw)
        assert r["queries"] == 3, r
    M = json.loads((out / "manifest/xm3600_vi.json").read_text())
    q0 = M["queries"][0]
    d = np.stack([vec[i] for i in sorted(ids["d_vi"])])
    d /= np.linalg.norm(d, axis=1, keepdims=True)
    qv = np.load(w / "xm3600_vi.npz")["vecs"][0]
    want = [sorted(ids["d_vi"])[j] for j in np.argsort(-(d @ (qv / np.linalg.norm(qv))), kind="stable")[:N_RANK]]
    assert q0["ranked"] == want and q0["image_sha256"] == sha(b"img xm3q0")
    assert "absent" not in q0 and q0["a12_masks"] == [[False, True]] * 4  # 'một con mèo' is 'absent'; booleans only
    assert M["queries"][1]["a12_masks"] == [[False, False]] * 4  # no label: nothing deleted
    a2 = G.CP.pick("A2", q0["id"], q0["ranked"], sorted(ids["d_vi"]))
    assert set(a2) <= set(M["demos"]) and set(shots) <= set(M["demos"]) and sorted(M["a5_shots"]) == sorted(shots)
    assert all(M["demos"][i]["text"] == vi[i] for i in M["demos"])
    assert "a5_shots" not in json.loads((out / "manifest/t_a.json").read_text())

    loads, seen = [], []

    def gen(i, p, k):
        seen.append(k)
        return ("yes", "eos") if k == "verify" else ("Một bức ảnh.", "eos")
    for s, a in (("xm3600_vi", "A1"), ("xm3600_vi", "A2"), ("xm3600_vi", "A12"), ("xm3600_vi", "A5"),
                 ("xm3600_vi", "PVR-drop"), ("ktvic_explore", "A3"), ("t_a", "A2"), ("kt_c", "S3")):
        x = types.SimpleNamespace(set=s, arm=a, manifest=out / f"manifest/{s}.json", kept=kdir, out=w / "dec", root=G.ROOT,
                                  speed=0, timing=None, cap=None, a1_decomp=None, democap=out / "democap")
        G.PINS["DEMOCAP_d_tc"] = "fixture"
        G.HOST.append(1)  # the consumer on the builder's files: no source json, no t2pool file, no kept listing
        try:
            assert G.decode(x, lambda n: (loads.append(n), (gen, None))[1], lambda q: "IMG") == 0, (s, a)
        finally:
            G.HOST.pop()
    assert loads == ["mblip"] * 3 + ["xglm", "mblip", "mblip", "mblip", "llava"] and "verify" in seen

    r = seal(out)
    lines = (out / "MANIFEST.sha256").read_text().splitlines()
    paths = [ln.split("  ")[1] for ln in lines]
    assert r["files"] == len(lines) == 6 + 3 + 3 + 18 and paths == sorted(paths), (r, paths[:3])
    for ln in lines:
        h, p = ln.split("  ")
        f = img / p.split("/")[-1] if p.startswith("images/") else kdir / p[5:] if p.startswith("kept/") else out / p
        assert sha(f.read_bytes()) == h, p
    G._must("sealed once", seal, out)
    (out / "MANIFEST.sha256").unlink()
    M2 = json.loads((out / "manifest/kt_c.json").read_text())
    M2["queries"][0]["image_sha256"] = M["a5_shot_sha256"][shots[0]]  # a query image byte-equal to a shot image
    (out / "manifest/kt_c.json").write_bytes(jbytes(M2))
    G._must("A5 shot images are tier-1 query images", seal, out)

    mk("vitextvqa_dev", n=2)
    G._must("not the registered 3", build_set, "vitextvqa_dev", w / "vitextvqa_dev.tsv", img, w / "vitextvqa_dev.npz",
            w / "demb.npz", kdir, out, dec, shots=w / "shots.tsv")
    mk("vitextvqa_dev")
    np.savez(w / "demb_short.npz", ids=np.array(ids["d_vi"][1:]), vecs=rng.normal(size=(19, 8)))
    G._must("have no embedding row", build_set, "vitextvqa_dev", w / "vitextvqa_dev.tsv", img, w / "vitextvqa_dev.npz",
            w / "demb_short.npz", kdir, out, dec, shots=w / "shots.tsv")
    np.savez(w / "q_other.npz", ids=np.array(["zz1", "zz2", "zz3"]), vecs=rng.normal(size=(3, 8)))
    G._must("have no embedding row", build_set, "vitextvqa_dev", w / "vitextvqa_dev.tsv", img, w / "q_other.npz",
            w / "demb.npz", kdir, out, dec, shots=w / "shots.tsv")
    G._must("differs from democap", build_set, "vitextvqa_dev", w / "vitextvqa_dev.tsv", img, w / "vitextvqa_dev.npz",
            w / "demb.npz", kdir, out, lambda ts: [G._dc(t + " x", []) for t in ts], shots=w / "shots.tsv")
    G._must("--a12 iff", build_set, "vitextvqa_dev", w / "vitextvqa_dev.tsv", img, w / "vitextvqa_dev.npz",
            w / "demb.npz", kdir, out, dec, a12=w / "a12.json", shots=w / "shots.tsv")
    assert sorted(ids["d_vi"][:3]) != sorted(shots)
    (w / "bad_shots.tsv").write_text("".join(f"{i}\t{img}/shot{j}.jpg\n" for i, j in zip(ids["d_vi"][:3], shots)))
    G._must("SEEDS['A5'] draw", build_set, "vitextvqa_dev", w / "vitextvqa_dev.tsv", img, w / "vitextvqa_dev.npz",
            w / "demb.npz", kdir, out, dec, shots=w / "bad_shots.tsv")
    qs = [q for q in (f"koq{j}" for j in range(40)) if not G.CR.half(q)][:3]  # confirm-half ids on an explore set
    (w / "ko_bad.tsv").write_text("".join(f"{q}\t{q}.jpg\n" for q in qs))
    G._must("explore half", build_set, "ktvic_explore", w / "ko_bad.tsv", img, w / "ktvic_explore.npz",
            w / "demb.npz", kdir, out, dec, shots=w / "shots.tsv")


def main() -> int:
    ap = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    sp = ap.add_subparsers(dest="cmd", required=True)
    sp.add_parser("selftest")
    d = sp.add_parser("democap")
    d.add_argument("--ds", choices=G.KEPT, required=True)
    d.add_argument("--dry", action="store_true")
    s = sp.add_parser("set")
    s.add_argument("--set", choices=G.SETS, required=True)
    for p, keys in ((d, ("--src", "--kept", "--out")),
                    (s, ("--queries", "--images", "--qemb", "--demb", "--kept", "--out"))):
        for k in keys:
            p.add_argument(k, type=Path, required=True)
    s.add_argument("--a12", type=Path)
    s.add_argument("--shots", type=Path)
    sp.add_parser("seal").add_argument("--out", type=Path, required=True)
    x = ap.parse_args()
    G.load()
    if x.cmd == "selftest":
        return selftest()
    if x.cmd == "democap":
        rep = democap(x.ds, x.src, x.kept, x.out, x.dry)
    elif x.cmd == "set":
        vi = G.SETS[x.set][0] == "d_vi"  # VI segmenter for D-VI, the EN parse for D-EN / D-TC (prereg §6.2)
        rep = build_set(x.set, x.queries, x.images, x.qemb, x.demb, x.kept, x.out,
                        (lambda ts: G.CP.decompose_vi(ts, G.ROOT)) if vi else (lambda ts: G.CP.decompose_en(ts, G.ROOT)),
                        x.a12, x.shots)
    else:
        rep = seal(x.out)
    print(json.dumps(rep, sort_keys=True))
    return 0


if __name__ == "__main__":
    sys.exit(main())
