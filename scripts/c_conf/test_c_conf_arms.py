"""Self-test and mutants of the C-CONF arm-list builder (c_conf_arms.py) on synthetic fixtures only.

Runs on a rented host only (the investigator's rule of 2026-11-11), from the repository checkout, with the decoder's
interpreter (venv-lb). Reads no study file: every vector, list, feature row, token and decision is made here; the
owner-set check reads the committed owners register and owner-feats manifest (owner metadata, at their pins).
    env -u PYTHONPATH /root/venv-lb/bin/python -I -B scripts/c_conf/test_c_conf_arms.py   # self-test, then every mutant must die
§11.1 row 1, the part this file owns (the carve order itself is tested by test_c_conf_lists.py: single-member OpenViIC
clusters only, a _pairs file never in the pool, the owners' id matches): an owner near-copy (C1, C2 or C3) never enters
the carve and the printed counts equal the toy truth; no carve query's cluster is a shot, and the shot draw stops when a
query is below the near cut to its own cluster; no image sees its own cluster in any arm; no donor is the image itself
or its byte twin; rand d0 on ov_test equals the first-look rule; refills are counted correctly; K0 / K0-T compare ret,
rand d0 and perm p1; the refill gate; T0 refuses ov_test without a valid four-field token. LMCap's own-cluster skip is
tested in test_c_conf.py (c_conf.lmcap_skip).
"""
from __future__ import annotations

import argparse
import contextlib
import io
import json
import random
import sys
import tempfile
from pathlib import Path

import numpy as np

HERE = Path(__file__).resolve().parent
sys.path.insert(0, str(HERE))
import test_c_conf as T  # noqa: E402  refused, tokens, the mutant runner

N_Q, N_M, DIM = 12, 40, 16


def unit(v: np.ndarray) -> np.ndarray:
    return v / np.linalg.norm(v, axis=-1, keepdims=True)


def at(c: np.ndarray, v: np.ndarray) -> np.ndarray:
    """A query at cosine exactly 0.8 to the unit vector c (below the near cut), leaning towards v."""
    u = v - (v @ c) * c
    return 0.8 * c + 0.6 * unit(u)


def toy(seed: int = 11) -> tuple:
    """12 carve-like queries, 40 clusters. q_n's own cluster is m_n at cosine 0.8 (only the id rule removes it);
    m35-m39 sit at cosine > 0.99 to q0 (only q0's near cut removes them); q1 leans towards q0, so q1's ranking holds
    m35-m39 and m00 near its top: q1 as q0's donor exercises both filters of perm."""
    rng = np.random.default_rng(seed)
    mv = unit(rng.normal(size=(N_M, DIM)))
    qv = np.stack([at(mv[n], rng.normal(size=DIM)) for n in range(N_Q)])
    qv[1] = at(mv[1], qv[0])
    mv[35:40] = unit(qv[0] + 0.01 * rng.normal(size=(5, DIM)))
    mk, qids = [f"m{j:02d}" for j in range(N_M)], [f"q{n:02d}.jpg" for n in range(N_Q)]
    return mk, mv.astype(np.float32), qids, qv.astype(np.float32), {q: mk[n] for n, q in enumerate(qids)}


def elig(row: np.ndarray, mk: list[str], drop: str | None, near: float) -> list[str]:
    """C's rule written out again: by cosine, ties by id, below the near cut, minus one cluster id."""
    return [mk[j] for j in np.lexsort((mk, -row)) if row[j] < near and mk[j] != drop]


def selftest(R) -> list[str]:
    ok = []
    A, AL, BM = R.A, R.AL, R.BM
    near, nex = R.NEAR, R.N_EX
    mk, mv, qids, qv, own = toy()
    cos = qv @ mv.T
    ds = next(f"toy{i}" for i in range(1000) if AL.sattolo(f"toy{i}", 1, N_Q)[0] == 1)  # q0's p1 donor is q1
    sha = {q: f"h{n}" for n, q in enumerate(qids)}
    built, diag = R.build(ds, mk, mv, qids, qv, sha, own)
    q1_top = elig(cos[1], mk, own[qids[1]], near)[:nex]
    assert "m00" in q1_top and {"m35", "m36", "m37", "m38", "m39"} & set(q1_top), \
        "the toy exercises the own-cluster and the near-cut filters of perm"
    refills = {p: 0 for p in A.PERMS}
    for n, q in enumerate(qids):
        e = elig(cos[n], mk, own[q], near)
        arms = [built["ret"][q]] + [built["rand"][str(d)][q] for d in A.DRAWS] + [built["perm"][str(p)][q] for p in A.PERMS]
        assert all(own[q] not in x for x in arms), "no image sees its own cluster in any arm"
        assert all(cos[n, mk.index(c)] < near for x in arms for c in x), "no shown cluster at cosine >= 0.92 to q"
        assert built["ret"][q] == e[:nex], "ret = C's rule minus the own cluster"
        for d in A.DRAWS:
            s = BM.seed("rand", ds, q) if d == 0 else BM.seed("rand", ds, q, f"d{d}")
            assert built["rand"][str(d)][q] == random.Random(s).sample(sorted(e), nex)
        assert built["near"][q] == sorted(mk[j] for j in np.flatnonzero(cos[n] >= near))
        for p in A.PERMS:
            dn = qids.index(built["donor"][str(p)][q])
            assert dn != n, "no image is its own donor"
            de = elig(cos[dn], mk, own[qids[dn]], near)
            assert built["perm"][str(p)][q] == [c for c in de if cos[n, mk.index(c)] < near and c != own[q]][:nex]
            refills[p] += nex - sum(cos[n, mk.index(c)] < near and c != own[q] for c in de[:nex])
    for p in A.PERMS:
        assert abs(diag[f"p{p}"]["refill_share_8"] - refills[p] / (nex * N_Q)) < 1e-5, "refills counted correctly"
    assert refills[1] > 0, "the toy refills"
    ok.append("toy (40 clusters, 12 queries): own cluster out of every arm by id, near cut on q, donors, refills")
    # byte twins: a donor is never q or its twin
    sha2 = {**sha, qids[7]: sha[qids[3]]}
    ds2 = next(f"tw{i}" for i in range(1000) if (lambda pi: pi[3] == 7 or pi[7] == 3)(AL.sattolo(f"tw{i}", 1, N_Q)))
    b2, d2 = R.build(ds2, mk, mv, qids, qv, sha2, own)
    for p in A.PERMS:
        pi = AL.sattolo(ds2, p, N_Q)
        assert d2[f"p{p}"]["twin_replacements"] == sum(sha2[qids[pi[n]]] == sha2[qids[n]] for n in range(N_Q))
        assert all(sha2[b2["donor"][str(p)][q]] != sha2[q] for q in qids), "no donor is q or its byte twin"
    assert d2["p1"]["twin_replacements"] >= 1
    ok.append("byte-twin donor rule (the toy replaces at least one donor)")
    # OV-test: rand d0 is the first look's rule (build_memory.exemplars, written out again); no own cluster there
    bt, _dt = R.build("ov_test", mk, mv, qids, qv, sha)
    for n, q in enumerate(qids):
        e = elig(cos[n], mk, None, near)
        assert bt["rand"]["0"][q] == random.Random(BM.seed("rand", "ov_test", q)).sample(sorted(e), nex)
        assert bt["ret"][q] == e[:nex] and bt["rand"]["1"][q] != bt["rand"]["0"][q]
    ok.append("ov_test: ret and rand d0 = the first-look rule; d1 differs")
    # K0 / K0-T comparators
    ex = {"ret": {q: [[c, 0.5] for c in bt["ret"][q]] for q in qids}, "rand": dict(bt["rand"]["0"])}
    assert R.parity(bt, ex["ret"], ex["rand"], bt["perm"]["1"])["pass"]
    ex["rand"][qids[4]] = list(reversed(ex["rand"][qids[4]]))
    r = R.parity(bt, ex["ret"], ex["rand"])
    assert not r["pass"] and r["rand_d0_failing_ids"] == [qids[4]] and r["rand_d0_equal"] == N_Q - 1
    ok.append("K0 / K0-T comparators (counts and failing ids)")
    # §5.1 (ii): shots drawn without own-cluster masking are never carve clusters; a query below the cut stops
    rng = np.random.default_rng(5)
    cv = unit(rng.normal(size=(20, 64))).astype(np.float32)
    sv = np.concatenate([cv, unit(rng.normal(size=(3, 64))).astype(np.float32)])
    sk = [f"c{j:02d}" for j in range(20)] + ["s0", "s1", "s2"]
    for i in range(20):
        assert set(R.carve_shots(f"shots{i}", sk, cv @ sv.T, list(range(20)))) == {"s0", "s1", "s2"}
    assert T.refused(lambda: R.carve_shots(ds, mk, cos, list(range(N_Q))), "G0"), "own cluster below the cut: G0"
    ok.append("shots: never a carve cluster (20 draws); a query below the near cut to its own cluster is G0")
    # §5.1 (iii) near-copy part: C1, C2, C3 against fake owner features; carve = the first survivors of the order
    import w25 as W

    rng = np.random.default_rng(9)
    ph = [int(x) for x in rng.integers(0, 2 ** 62, 8)]
    pv = unit(rng.normal(size=(8, 64)))
    pool = {**BM.fake_feats([f"p{n}" for n in range(8)], ph, pv.tolist()), "ids": [f"c{n}" for n in range(8)]}
    far = lambda k: [int(x) for x in rng.integers(0, 2 ** 62, k)]  # noqa: E731
    owners = {"o_c1": {**BM.fake_feats(["p2"], far(1), unit(rng.normal(size=(1, 64))).tolist()), "ids": ["y1"]},
              "o_c2": {**BM.fake_feats(["z2"], [ph[4]], pv[4:5].tolist()), "ids": ["y2"]},
              "o_c3": {**BM.fake_feats(["z3"], far(1), [at(pv[6], rng.normal(size=64)).tolist()]), "ids": ["y3"]},
              "o_far": {**BM.fake_feats(["z4"], far(1), unit(rng.normal(size=(1, 64))).tolist()), "ids": ["y4"]}}
    order = [[f"c{n}", f"f{n}.jpg", f"p{n}"] for n in range(8)]
    rule = lambda q, y: W.rule(q, y, BM.near)  # noqa: E731
    R.CARVE_N = 4
    carve, counts = R.near_copy(order, pool, owners, rule)
    assert [r[0] for r in carve] == ["c0", "c1", "c3", "c5"] and counts["near_copy_hits"] == 3 and counts["final_pool"] == 5
    per = counts["per_owner"]
    assert (per["o_c1"]["excluded"], per["o_c2"]["excluded"], per["o_c3"]["excluded"], per["o_far"]["excluded"]) == \
        (1, 1, 1, 0) and per["o_c3"]["C1_C2_registered"] == 0 and per["o_c3"]["C3_sscd_0.75"] == 1
    R.CARVE_N = 6
    assert T.refused(lambda: R.near_copy(order, pool, owners, rule), "STOP"), "fewer than the carve size: STOP"
    R.CARVE_N = 2000
    ok.append("near-copy part of (iii): C1, C2 and C3 hits leave the pool; counts per owner; a short pool stops")
    # the owners of the near-copy part as registered (18e61111 l.146, CC-450 X1); reads the committed owners register
    # and owner-feats manifest (owner metadata, at their pins) and an empty temporary owner folder
    with tempfile.TemporaryDirectory() as tmp:
        saved, R.OWNER_DIR = R.OWNER_DIR, Path(tmp)
        try:
            cmp, skip = R.owner_table()
            assert set(cmp) == {"h_bdt1_739", "ktvic_dev299", "openviic_dev_c1", "refused_ktvic_dup"}, sorted(cmp)
            assert {"openviic_test_2001", "ktvic_test_558", "xm3600_all", "karpathy_test_5000"} <= set(skip)
            (Path(tmp) / "of_ktvic_dev299.npz.sha256").write_bytes(b"")
            assert set(R.owner_table()[0]) == set(cmp), "a near-copy cache's sidecar is allowed"
            (Path(tmp) / "openviic_test.npz").write_bytes(b"")
            assert T.refused(R.owner_table, "G0"), "a cache of another owner on the host is G0"
        finally:
            R.OWNER_DIR = saved
    assert R.ID_OWNERS == ("vihal_pool", "vihal_survivors", "vihal_removed", "ktvic_dev300")
    ok.append("near-copy owners: the four register owners and the ViHal / dev300 lists only; another owner's cache is G0")
    rec = {"a.jpg": "1" * 64, "b.png": "2" * 64}
    R.record_check(["a.jpg", "b.png"], ["1" * 64, "2" * 64], rec)
    assert T.refused(lambda: R.record_check(["a.jpg"], ["3" * 64], rec), "G0"), "a differing image sha256 is G0"
    assert T.refused(lambda: R.record_check(["c.jpg"], ["1" * 64], rec), "G0"), "an image outside the list is G0"
    assert R.KT_HASHES[0].name == "c_conf_ktvic_owner_images.sha256" and len(R.KT_HASHES[1]) == 64
    ok.append("ViHal / dev300 images: a missing or differing sha256 against the pinned hash list is G0")
    # CC-454 B6 (binding 1): every file in the KTVIC image folder is a training image of the pinned annotation
    with tempfile.TemporaryDirectory() as tmp:
        d = Path(tmp)
        ann = d / "train_data.json"
        ann.write_text(json.dumps({"images": [{"id": 1, "filename": "tr1.jpg"}]}), encoding="utf-8")
        saved = R.KT_TRAIN, R.KT_IMAGES
        R.KT_TRAIN, R.KT_IMAGES = (str(ann), R.sha(ann)), d / "images"
        try:
            (d / "images").mkdir()
            (d / "images/tr1.jpg").write_bytes(b"")
            assert R.ktvic_test_free() == 1, "a training image passes"
            (d / "images/te9.jpg").write_bytes(b"")
            assert T.refused(R.ktvic_test_free, "G0"), "a file outside the training annotation is G0"
        finally:
            R.KT_TRAIN, R.KT_IMAGES = saved
    ok.append("KTVIC image folder: training images only, any other file is G0 (CC-454 B6)")
    # refill gate (step 0.3, G0b) and the token at T0
    with tempfile.TemporaryDirectory() as tmp:
        d = Path(tmp)
        for name, shares, want in (("hi", (0.2, 0.05), 3), ("lo", (0.1, 0.05), 0)):
            p = d / f"{name}.json"
            p.write_text(json.dumps({"set": "toy", "ids": [], "diag": {f"p{k}": {"refill_share_8": s}
                                                                      for k, s in zip((1, 2), shares)}}))
            Path(str(p) + ".sha256").write_text(f"{R.sha(p)}  {p.name}\n")
            with contextlib.redirect_stdout(io.StringIO()):
                try:
                    R.cmd_diag(argparse.Namespace(lists=p, out=d / f"{name}.out.json"))
                except SystemExit as e:
                    assert e.code == want, (name, e.code)
        tk = T.tokens(d, ["qwen25vl_7b"])
        t0 = lambda t: R.cmd_t0(argparse.Namespace(token=t, decision=None, dir=d, out=d / "l.json", dry_run=True))  # noqa: E731
        A.ADMITTED = None
        assert T.refused(lambda: t0(None)) and T.refused(lambda: t0(tk["three_fields"]))
        A.ADMITTED = None
        assert T.refused(lambda: t0(tk["wrong_sha"]))
        buf = io.StringIO()
        with contextlib.redirect_stdout(buf):
            t0(tk["good"])
        assert "DRY t0" in buf.getvalue()
    A.ADMITTED = None
    ok.append("refill gate rc 3 above 0.10 (0.10 passes); T0 refuses OV-test without a valid four-field token")
    return ok


KEEP = "keep = [c for c in donor_rank[:N_EX] if row_q[c] < NEAR and c != own_col]"
#: (file, name, old, new): each must make the self-test fail
MUTANTS = [
    ("c_conf_arms.py", "own cluster kept in perm", KEEP, "keep = [c for c in donor_rank[:N_EX] if row_q[c] < NEAR]"),
    ("c_conf_arms.py", "near-cut filter applied to the donor only", KEEP,
     "keep = [c for c in donor_rank[:N_EX] if c != own_col]"),
    ("c_conf_arms.py", "own cluster kept in ret and rand", "ok = [int(j) for j in A.eligible(row, mk) if j != own_col[n]]",
     "ok = [int(j) for j in A.eligible(row, mk)]"),
    ("c_conf_arms.py", "shot cluster admitted (the shot draw run with own clusters masked)",
     "    shots = A.lmcap_shots(ds, mk, cos)\n",
     "    m = cos.copy(); m[np.arange(len(own_cols)), own_cols] = -1.0; shots = A.lmcap_shots(ds, mk, m)\n"),
    ("c_conf_arms.py", "an owner near-copy kept in the pool", "keep = [r for r in order if r[0] not in hit]",
     "keep = list(order)"),
    ("c_conf_arms.py", "an owner outside §5.1 (iii) compared",
     'NEAR_OWNERS = ("h_bdt1_739", "ktvic_dev299", "openviic_dev_c1", "refused_ktvic_dup")',
     'NEAR_OWNERS = ("h_bdt1_739", "ktvic_dev299", "openviic_dev_c1", "refused_ktvic_dup", "xm3600_all")'),
    ("c_conf_arms.py", "another owner's cache admitted on the host", "    if stray:\n", "    if False:\n"),
    ("c_conf_arms.py", "an owner image with a differing sha256 admitted", "bad = sum(rec.get(n) != h for n, h in",
     "bad = sum(n not in rec for n, h in"),
    ("c_conf_arms.py", "twin rule dropped", "        if sha[qids[d]] == sha[qids[i]]:\n", "        if False:\n"),
    ("c_conf_arms.py", "token check skipped at T0", "    A.admit(a.token, a.decision)\n    A.ov_gate()\n    if a.dry_run:\n",
     "    if a.dry_run:\n"),
    ("c_conf_arms.py", "K0 comparator lenient", 'rep["pass"] = all(rep[f"{k}_equal"] == len(ids) for k in refs)',
     'rep["pass"] = True'),
    ("c_conf_arms.py", "refill gate off",
     'over = [k for k, v in lst["diag"].items() if v["refill_share_8"] > AL.REFILL_GATE]', "over = []"),
    ("c_conf.py", "d<d> suffix applied to d0",
     's = BM.seed("rand", ds, qid) if d == 0 else BM.seed("rand", ds, qid, f"d{d}")', 's = BM.seed("rand", ds, qid, f"d{d}")'),
    ("c_conf_arms.py", "a KTVIC test image admitted (CC-454 B6)", "    if extra:\n", "    if False:\n"),
]


def main() -> None:
    import c_conf_arms as R

    print("self-test PASS: " + "; ".join(selftest(R)))
    if "--selftest" not in sys.argv:
        T.run_mutants(Path(__file__).name, MUTANTS)


if __name__ == "__main__":
    main()
