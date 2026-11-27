#!/usr/bin/env python3
"""Self-tests of scripts/b_d1/b_d1.py (prereg v3 §6 S0). Synthetic fixtures only, in a temp dir: stub word units
(b_fecert.STUB), invented captions carrying the marker syllable MARK, no data-set file, no system output.
Each check prints `SELFTEST ok|FAIL|CRASH <name>`; an AssertionError, Fault or SystemExit is FAIL.
    python3 -I -B scripts/b_d1/test_b_d1.py [--only NAME ...]
Exit 0 only when every check is ok."""
import argparse
import contextlib
import io
import itertools
import json
import os
import shutil
import sys
import tempfile
from pathlib import Path

import numpy as np

sys.path.insert(0, str(Path(__file__).resolve().parent))
import b_d1 as D  # noqa: E402

BF, FM, PT, E4 = D.BF, D.FM, D.PT, D.BF.E4
MARK = "zqxv"
CHECKS = []


def check(fn):
    CHECKS.append(fn)
    return fn


# ------------------------------------------------------------------------------------------------ hand-built matrix
def mk_M(delta: dict, n: int = 40, files=("fa", "fb", "fc", "fd"), merge=None, seed=1) -> dict:
    """A matrix world without text: C[k, j] = 50 + delta.get((member, file), 0) + small noise per image.
    merge: {member: other} gives member the token keys of other (one class)."""
    rng = np.random.default_rng(seed)
    noise = rng.normal(0, 1.0, (len(files), n))
    noise -= noise.mean(axis=1, keepdims=True)  # a zero delta gives a mean difference of exactly 0
    C = np.zeros((len(D.F_ALL), len(files), n))
    K = np.empty((len(D.F_ALL), len(files)), dtype="<U16")
    RK = np.empty(len(D.F_ALL), dtype="<U16")
    for k, m in enumerate(D.F_ALL):
        src = (merge or {}).get(m, m)
        RK[k] = f"r{D.F_ALL.index(src):015d}"
        for j, f in enumerate(files):
            C[k, j] = 50 + delta.get((src, f), 0.0) + noise[j]
            K[k, j] = f"{j:02d}{D.F_ALL.index(src):014d}"
    M = {"cider": C, "keys": K, "rkeys": RK, "members": np.array(D.F_ALL), "files": np.array(files)}
    M["fidx"] = {f: j for j, f in enumerate(files)}
    M["midx"] = {m: k for k, m in enumerate(D.F_ALL)}
    return M


def comps_of(M, pairs, n=None):
    W = BF.boot_W(n or M["cider"].shape[2])
    return [D.build(M, f"D:{a}|{b}", W) for a, b in pairs], W


def cls(*sigs, members=None):
    """A comparison made of classes with given sig values (stats [D, L, U, sd])."""
    st = {1: [5.0, 1.0, 9.0, 2.0], -1: [-5.0, -9.0, -1.0, 2.0], 0: [0.5, -2.0, 3.0, 1.0]}
    mem = members or [[m] for m in D.F_DEV[:len(sigs)]]
    return {"id": "D:x|y", "classes": {f"k{i}": {"members": mm, "cider": list(st[s])} for i, (s, mm) in
                                       enumerate(zip(sigs, mem))}}


# ------------------------------------------------------------------------------------------------ text world (e2e)
VOC = ["con chó", "con mèo", "bãi cỏ", "hoà bình", "sức khoẻ", "người đàn ông", "chiếc xe", "toà nhà"]
OWN = ["o1-short", "o2-short", "o3-short", "o4-short"]
N_IMG = 8
_W = {}


def _ref(i, j):
    return f"{MARK} {VOC[i % 8]} đang chạy trên {VOC[(i + j + 1) % 8]}."


def _cap(n, i):
    return {"o1-short": _ref(i, 0),
            "o2-short": _ref(i, 1).rstrip(".").replace("hoà", "hòa").replace("toà", "tòa"),
            "o3-short": f"{MARK} Một bức ảnh có {VOC[(i + 3) % 8]} và cây",
            "o4-short": f"{MARK} {VOC[i % 8].upper()} trên {VOC[(i + 2) % 8]}"}[n]


def _dump(p: Path, o):
    p.parent.mkdir(parents=True, exist_ok=True)
    p.write_text(json.dumps(o, ensure_ascii=False), encoding="utf-8")


def world() -> dict:
    """The synthetic NCS tree, work dir (SYSTEMS, CENSUS, FAMILY, DEV, RESULT built with b_fecert's own functions)
    and the stubs; built once."""
    if _W:
        return _W
    root = Path(tempfile.mkdtemp(prefix="b_d1_selftest_"))
    data, work, base, out = root / "ncs", root / "work", root / "base", root / "out"
    ids = list(range(1, N_IMG + 1))
    kt = data / "datasets/ktvic/test_data.json"
    _dump(kt, {"images": [{"id": i, "filename": f"{i:011d}.jpg"} for i in ids],
               "annotations": [{"image_id": i, "id": 10 * i + j, "caption": _ref(i, j)} for i in ids for j in range(2)]})
    for n in OWN:
        _dump(data / f"results/{n}.preds.json", {str(i): _cap(n, i) for i in ids})
    for n, f in BF.BASE.items():
        verb = "nằm" if "res" in n else "chạy"
        _dump(base / f, [{"image_id": i, "caption": f"{MARK} con_chó {verb} trên bãi_cỏ"} for i in ids])
    BF.set_data(data)
    rows = [(n, "short", n.split("-")[0], D.sha_file(data / f"results/{n}.preds.json"), "x", "own") for n in OWN]
    rows += [(n, "baseline", "baseline", D.sha_file(base / f), "x", "baseline") for n, f in BF.BASE.items()]
    work.mkdir(parents=True)
    (work / "SYSTEMS.tsv").write_text("name\tstratum\tfamily\tsha256\tgit_blob\trole\n" +
                                      "".join("\t".join(r) + "\n" for r in rows), encoding="utf-8")
    names = [r[0] for r in rows]
    Dl = [f"D:{a}|{b}" for a, b in itertools.combinations(names, 2)]
    _dump(work / "CENSUS.json", {"systems_tsv_sha256": D.sha_file(work / "SYSTEMS.tsv"), "D": Dl,
                                 "uts_moved_to_dev": False})
    _dump(work / "FAMILY.json", {"units_dropped": [], "refs_sha256": D.sha_file(kt)})
    refs = PT.load_refs(kt)
    sid = sorted(refs)
    texts = BF.ktvic_texts(work, base)
    tk = FM.Tok(BF.STUB)
    tk.prime([r for i in sid for r in refs[i]] + [t[i] for t in texts.values() for i in sid], FM.F)
    comps = BF.ktvic_comps(Dl)
    BF.run_list(sid, comps, FM.members(FM.DEV_UNITS), BF.scorer(tk, refs, sid, texts))
    _dump(work / "DEV.json", {"comparisons": comps})
    dev_copy = json.loads((work / "DEV.json").read_text(encoding="utf-8"))
    BF.run_list(sid, comps, FM.members(("uts",)), BF.scorer(tk, refs, sid, texts))
    res = [{"id": c["id"], "set": "D", "F": BF.certify(c, set(D.F_ALL))["verdict"],
            "D_f0": next(cl["cider"][0] for cl in c["classes"].values() if BF.F0N in cl["members"])} for c in comps]
    res.append({"id": "FL:x|y", "set": "FL", "F": "NULL-STABLE", "D_f0": 0.0})
    _dump(work / "RESULT.json", {"comparisons": res})
    D.INPUT_SHA.update({f: D.sha_file(work / f) for f in ("DEV.json", "RESULT.json", "FAMILY.json", "CENSUS.json",
                                                         "SYSTEMS.tsv")})
    D.REFS_SHA = D.sha_file(kt)
    D.EXPECT_FILES, D.EXPECT_IMAGES, D.EXPECT_D, D.N_NULL = len(names), N_IMG, len(Dl), 12
    D.SEG = BF.STUB
    BF.env_record = lambda a: {"stub": True}
    BF.env_check = lambda rec: None
    _W.update(root=root, data=data, work=work, base=base, out=out, refs=refs, ids=sid, texts=texts, tk=tk,
              dev=dev_copy, D=Dl)
    return _W


def run_main(argv) -> tuple[int, str]:
    buf = io.StringIO()
    with contextlib.redirect_stdout(buf):
        try:
            rc = D.main(argv)
        except SystemExit as e:
            rc = e.code if isinstance(e.code, int) else 9
            print(str(e.code))
    return rc, buf.getvalue()


def stages() -> dict:
    """s1 -> g0 -> s2 once on the synthetic world."""
    w = world()
    if "s2" in w:
        return w
    o = str(w["out"])
    rc, so = run_main(["s1", "--work", str(w["work"]), "--out", o, "--baselines", str(w["base"])])
    assert rc == 0, so
    npz = D.sha_file(w["out"] / "PER_IMAGE_D1.npz")
    rc2, sg = run_main(["g0", "--work", str(w["work"]), "--out", o, "--npz-sha", npz])
    assert rc2 == 0, sg
    g0 = D.sha_file(w["out"] / "G0.json")
    rc3, s2 = run_main(["s2", "--work", str(w["work"]), "--out", o, "--npz-sha", npz, "--g0-sha", g0])
    assert rc3 == 0, s2
    w.update(s1=so, g0=sg, s2=s2, npz=npz, g0sha=g0, result=D.jload(w["out"] / "RESULT_D1.json"))
    return w


# ------------------------------------------------------------------------------------------------ checks: pins, sets
@check
def pins_and_closure():
    D.pin_check()
    D.closure_check()
    bad = dict(D.PINS)
    bad["scripts/b_fecert/b_fecert.py"] = "0" * 64
    try:
        D.pin_check(pins=bad)
    except SystemExit as e:
        assert "FAULT" in str(e)
    else:
        raise AssertionError("an off-pin file passed")
    assert set(D.PINS) >= {"scripts/b_fecert/b_fecert.py", "scripts/b_fecert/family.py", "rescap/chair.py"}


@check
def member_sets():
    assert len(D.F_DEV) == 54 and len(D.F_UTS) == 18 and len(D.F_ALL) == 72 and D.F_ALL[:54] == D.F_DEV
    assert BF.F0N == "rdr.tw.pk.cf" and BF.F0N in D.F_DEV


@check
def fold_construction():
    assert set(D.FOLDS) == {"syl", "pyvi", "uts"}
    for u, (G, H) in D.FOLDS.items():
        assert not set(G) & set(H)
        assert {m.split(".")[0] for m in H} == {u}
        assert BF.F0N in G, "rdr (f0) must stay in every certifying family"
        assert len(H) == 18 and sorted(H) == sorted(D.names((u,))), "H_u = all 18 members of the held-out unit"
    assert [len(D.FOLDS[u][0]) for u in ("syl", "pyvi", "uts")] == [36, 36, 54]
    assert {m.split(".")[0] for m in D.FOLDS["uts"][0]} == {"syl", "rdr", "pyvi"}


@check
def h3_grid_membership():
    assert len(D.G_CONTRACT) == 18 and all(m.split(".")[1] == "tw" for m in D.G_CONTRACT)
    assert {m.split(".")[0] for m in D.G_CONTRACT} == {"syl", "rdr", "pyvi"}
    assert {m.split(".")[2] for m in D.G_CONTRACT} == {"pk", "pf", "pa"}
    assert {m.split(".")[3] for m in D.G_CONTRACT} == {"cf", "ck"}
    assert sorted(D.G_CAPTION) == sorted(D.F_DEV) and set(D.G_CONTRACT) <= set(D.G_CAPTION)
    assert {m.split(".")[1] for m in set(D.G_CAPTION) - set(D.G_CONTRACT)} == {"tm", "tf"}
    assert len(D.G_SYL) == 6 and all(m.startswith("syl.tw.") for m in D.G_SYL)
    assert D.METRICS == ("cider", "bleu", "rouge")


# ------------------------------------------------------------------------------------------------ checks: S1 / swap
@check
def swap_identity():
    """Re-scoring swapped texts through b_fecert.scorer equals the sign flip of d, to 1e-12, under several members."""
    w = world()
    a, b = "o1-short", "o3-short"
    sid = w["ids"]
    sg = np.array([1, -1, -1, 1, -1, 1, 1, -1])
    t2 = {a: dict(w["texts"][a]), b: dict(w["texts"][b])}
    for k, i in enumerate(sid):
        if sg[k] < 0:
            t2[a][i], t2[b][i] = w["texts"][b][i], w["texts"][a][i]
    per = BF.scorer(w["tk"], w["refs"], sid, {a: w["texts"][a], b: w["texts"][b]})
    per2 = BF.scorer(w["tk"], w["refs"], sid, t2)
    for m in (FM.F0, ("syl", "tm", "pa", "ck"), ("pyvi", "tf", "pf", "cf"), ("uts", "tw", "pk", "cf")):
        d, o2 = per(m), per2(m)
        assert np.max(np.abs((o2[a]["cider"] - o2[b]["cider"]) - sg * (d[a]["cider"] - d[b]["cider"]))) <= 1e-12


@check
def s1_matrix():
    w = stages()
    npz = w["out"] / "PER_IMAGE_D1.npz"
    assert oct(npz.stat().st_mode)[-3:] == "444"
    with np.load(npz, allow_pickle=False) as z:
        assert z["cider"].shape == (72, len(OWN) + 2, N_IMG) and list(z["members"]) == D.F_ALL
        assert all(len(str(k)) == 16 for k in z["keys"].ravel())
    rc, so = run_main(["s1", "--work", str(w["work"]), "--out", str(w["out"]), "--baselines", str(w["base"])])
    assert rc != 0 and "PER_IMAGE_D1.npz exists" in so, "s1 ran twice"
    assert D.sha_file(npz) == w["npz"]


@check
def s1_matches_fecert_scorer():
    """The matrix row of each member equals b_fecert.scorer's per-image CIDEr-D on the same files."""
    w = stages()
    M = D.load_matrix(w["out"] / "PER_IMAGE_D1.npz", w["npz"])
    per = BF.scorer(w["tk"], w["refs"], w["ids"], w["texts"])
    for m in (FM.F0, ("syl", "tf", "pa", "cf"), ("uts", "tm", "pk", "ck")):
        o = per(m)
        k = M["midx"][FM.name(m)]
        for f, j in M["fidx"].items():
            assert np.array_equal(M["cider"][k, j], o[f]["cider"]) and M["keys"][k, j] == o[f]["key"]


# ------------------------------------------------------------------------------------------------ checks: G0
@check
def g0_pass_on_fecert_world():
    w = stages()
    g = D.jload(w["out"] / "G0.json")
    assert g["pass"] and g["max_abs_diff"] <= 1e-9 and g["key_mismatch"] == 0 and g["verdict_mismatch"] == 0
    assert g["comparisons"] == len(w["D"])


def _g0_rows(mut):
    w = stages()
    M = D.load_matrix(w["out"] / "PER_IMAGE_D1.npz", w["npz"])
    W = BF.boot_W(N_IMG)
    res = {r["id"]: r for r in D.jload(w["work"] / "RESULT.json")["comparisons"]}
    dev = json.loads(json.dumps(w["dev"]))
    rows = []
    for k, c in enumerate(dev["comparisons"]):
        r = dict(res[c["id"]])
        if k == 0:
            mut(c, r)
        rows.append(D.g0_compare(c, D.build(M, c["id"], W), r))
    return D.g0_pass(rows)


@check
def g0_tolerance():
    def small(c, r):
        next(iter(c["classes"].values()))["cider"][1] += 5e-7

    def big(c, r):
        next(iter(c["classes"].values()))["cider"][3] += 2e-6
    assert _g0_rows(small)["pass"], "a difference inside 1e-6 failed"
    assert not _g0_rows(big)["pass"], "a difference above 1e-6 passed"


@check
def g0_membership_and_keys():
    def move(c, r):
        ks = list(c["classes"])
        c["classes"][ks[1]]["members"].append(c["classes"][ks[0]]["members"].pop())

    def rekey(c, r):
        k0 = next(iter(c["classes"]))
        c["classes"]["zz" + k0[2:]] = c["classes"].pop(k0)
    assert not _g0_rows(move)["pass"]
    assert not _g0_rows(rekey)["pass"]


@check
def g0_verdict_and_df0():
    def verdict(c, r):
        r["F"] = "NULL-STABLE" if r["F"] != "NULL-STABLE" else "FRAGILE"

    def df0(c, r):
        r["D_f0"] += 1e-3
    assert not _g0_rows(verdict)["pass"]
    assert not _g0_rows(df0)["pass"]


@check
def g0_fault_stops():
    """A failed gate returns 3 and s2 refuses to run on it."""
    w = stages()
    o2 = w["root"] / "out_fail"
    o2.mkdir()
    shutil.copy(w["out"] / "PER_IMAGE_D1.npz", o2)
    bad = json.loads((w["work"] / "RESULT.json").read_text(encoding="utf-8"))
    bad["comparisons"][0]["F"] = "FRAGILE" if bad["comparisons"][0]["F"] != "FRAGILE" else "NULL-STABLE"
    wk = w["root"] / "work_fail"
    shutil.copytree(w["work"], wk)
    _dump(wk / "RESULT.json", bad)
    keep = dict(D.INPUT_SHA)
    D.INPUT_SHA["RESULT.json"] = D.sha_file(wk / "RESULT.json")
    try:
        rc, so = run_main(["g0", "--work", str(wk), "--out", str(o2), "--npz-sha", w["npz"]])
        assert rc == 3 and "FAULT" in so
        rc2, so2 = run_main(["s2", "--work", str(wk), "--out", str(o2), "--npz-sha", w["npz"],
                             "--g0-sha", D.sha_file(o2 / "G0.json")])
        assert rc2 != 0 and "REFUSED" in so2
    finally:
        D.INPUT_SHA.clear()
        D.INPUT_SHA.update(keep)


@check
def stage_guards():
    w = stages()
    rc, so = run_main(["s2", "--work", str(w["work"]), "--out", str(w["out"]), "--npz-sha", w["npz"],
                       "--g0-sha", "0" * 64])
    assert rc != 0 and "REFUSED" in so
    rc, so = run_main(["g0", "--work", str(w["work"]), "--out", str(w["out"]), "--npz-sha", "0" * 64])
    assert rc != 0 and "REFUSED" in so
    o3 = w["root"] / "out_foreign_g0"
    o3.mkdir()
    shutil.copy(w["out"] / "PER_IMAGE_D1.npz", o3)
    g = D.jload(w["out"] / "G0.json")
    g["PER_IMAGE_D1.npz"] = "0" * 64  # a G0 that passed, on another matrix
    _dump(o3 / "G0.json", g)
    rc, so = run_main(["s2", "--work", str(w["work"]), "--out", str(o3), "--npz-sha", w["npz"],
                       "--g0-sha", D.sha_file(o3 / "G0.json")])
    assert rc != 0 and "REFUSED" in so and not (o3 / "RESULT_D1.json").exists()


# ------------------------------------------------------------------------------------------------ checks: M1 = M1'
@check
def union_of_ties_cases():
    assert D.union_of_ties(cls(1, 1, 1), D.F_DEV) == (1, False)
    assert D.union_of_ties(cls(-1, -1), D.F_DEV) == (-1, False)
    assert D.union_of_ties(cls(1, 0, 1), D.F_DEV) == (0, False)
    assert D.union_of_ties(cls(1, -1), D.F_DEV) == (0, True), "mixed all-significant -> no ordering"
    assert D.union_of_ties(cls(0, 0), D.F_DEV) == (0, False)
    c = cls(1, -1)
    assert D.union_of_ties(c, D.F_DEV[:1]) == (1, False), "only members of G are contracts"


@check
def union_of_ties_touching():
    c = cls(1, 1)
    next(iter(c["classes"].values()))["cider"][1] = 0.0  # L = 0 touches: tied
    assert D.union_of_ties(c, D.F_DEV)[0] == 0 and BF.certify(c, set(D.F_DEV))["certified"] == 0
    c2 = cls(-1, -1)
    next(iter(c2["classes"].values()))["cider"][2] = 0.0  # U = 0 touches: tied
    assert D.union_of_ties(c2, D.F_DEV)[0] == 0


@check
def identity_m1_m1prime():
    comps = [cls(*s) for s in itertools.product((1, 0, -1), repeat=3)]
    r = D.identity_check(comps, D.F_DEV)
    extra = cls(1, 1, 0, members=[[D.F_DEV[0]], [D.F_DEV[1]], [D.F_UTS[0]]])  # a uts class outside G = F_dev
    assert D.identity_check([extra], D.F_DEV)["equal"] == 1, "the identity is checked over the G passed"
    assert r["equal"] == 27 and r["mixed_all_significant"] == sum(1 in s and -1 in s and 0 not in s
                                                                   for s in itertools.product((1, 0, -1), repeat=3))
    keep = D.union_of_ties
    D.union_of_ties = lambda c, G: (1, False)
    try:
        D.identity_check(comps, D.F_DEV)
    except BF.Fault:
        pass
    else:
        raise AssertionError("a difference between M1 and M1' did not FAULT")
    finally:
        D.union_of_ties = keep


# ------------------------------------------------------------------------------------------------ checks: claims
@check
def margin_from_f0():
    """M3/M4 use the f0 member (rdr.tw.pk.cf) only: direction sign(D_f0), margin z_f0."""
    M = mk_M({(BF.F0N, "fa"): 6.0, ("syl.tw.pk.cf", "fb"): 9.0})
    comps, W = comps_of(M, [("fa", "fb"), ("fa", "fc")])
    c = D.claims_f0(comps)
    s_ab = D.f0_stats(comps[0])
    assert set(c) == {"D:fa|fb", "D:fa|fc"} and c["D:fa|fc"][0] == 1 and c["D:fa|fc"][1] == BF.zval(D.f0_stats(comps[1]))
    assert c["D:fa|fb"][0] == int(np.sign(s_ab[0])) and c["D:fa|fb"][1] == BF.zval(s_ab)
    M2 = mk_M({("syl.tw.pk.cf", "fa"): 9.0})
    comps2, _ = comps_of(M2, [("fa", "fb")])
    assert D.claims_f0(comps2) == {}, "a margin taken from a non-f0 member"


@check
def top_k_order():
    cl = {"D:b|c": (1, 3.0), "D:a|c": (1, 3.0), "D:a|b": (-1, 5.0), "D:c|d": (1, float("inf"))}
    assert list(D.top_k(cl, 3)) == ["D:c|d", "D:a|b", "D:a|c"]
    assert D.top_k(cl, 3)["D:a|b"] == -1 and len(D.top_k(cl, 10)) == 4


@check
def aer_hand_toy():
    """Equal weight per member; sigma = SD (ddof 1) over all files of corpus CIDEr-D, fixed across resamples."""
    M = mk_M({(m, "fa"): 2.0 + 0.1 * k for k, m in enumerate(D.F_DEV)}, n=30)
    corp = M["cider"].mean(axis=2)
    sig = D.sigma(M)
    assert np.allclose(sig, corp.std(axis=1, ddof=1))
    k0 = M["midx"]["syl.tw.pk.cf"]
    assert abs(sig[k0] - np.std(corp[k0], ddof=1)) < 1e-12
    W = BF.boot_W(30)
    G = D.F_DEV[:3]
    e = np.mean([(M["cider"][M["midx"][m], 0] - M["cider"][M["midx"][m], 1]) / sig[M["midx"][m]] for m in G], axis=0)
    got = D.aer_stats(M, "D:fa|fb", G, sig, W)
    boot = W @ e / 30
    assert abs(got[0] - e.mean()) < 1e-12
    assert np.allclose(got[1:3], np.percentile(boot, [2.5, 97.5]), atol=1e-12)
    assert abs(got[3] - boot.std(ddof=1)) < 1e-12


@check
def aer_weighting():
    """Per member counts every member of a class; per class counts each class once (DESCRIPTIVE row)."""
    G = D.F_DEV[:3]
    M = mk_M({(G[0], "fa"): 30.0}, merge={G[1]: G[2]}, n=30)
    sig = np.ones(len(D.F_ALL))
    W = BF.boot_W(30)
    pm = D.aer_stats(M, "D:fa|fb", G, sig, W)
    pc = D.aer_stats(M, "D:fa|fb", G, sig, W, per_class=True)
    d = [M["cider"][M["midx"][m], 0] - M["cider"][M["midx"][m], 1] for m in G]
    assert abs(pm[0] - np.mean(d, axis=0).mean()) < 1e-12
    assert abs(pc[0] - np.mean([d[0], d[1]], axis=0).mean()) < 1e-12 and abs(pm[0] - pc[0]) > 1


@check
def aer_claims_direction():
    M = mk_M({(m, "fb"): 8.0 for m in D.F_DEV}, n=30)
    comps, W = comps_of(M, [("fa", "fb"), ("fa", "fc")])
    cl = D.claims_aer(M, comps, D.F_DEV, D.sigma(M), W)
    assert cl["D:fa|fb"][0] == -1 and "D:fa|fc" not in cl
    try:  # the uts members have equal corpus scores on every file here: sigma_c = 0
        D.claims_aer(M, comps, D.F_UTS, D.sigma(M), W)
    except BF.Fault:
        pass
    else:
        raise AssertionError("sigma_c = 0 did not FAULT")


@check
def held_break_and_discordant():
    """A claim breaks when some class of H is not significant its way (touching included); claims are (id, dir)."""
    H = D.FOLDS["syl"][1]
    M = mk_M({**{(m, "fa"): 9.0 for m in D.F_ALL if not m.startswith("syl.")},
              **{(m, "fa"): 0.0 for m in D.F_ALL if m.startswith("syl.")}}, n=40)
    comps, W = comps_of(M, [("fa", "fb"), ("fa", "fc")])
    byid = {c["id"]: c for c in comps}
    assert BF.held_break(byid["D:fa|fb"], 1, set(H))[0]
    A = {"D:fa|fb": 1, "D:fa|fc": 1}
    B = {"D:fa|fb": -1, "D:fa|fc": 1}
    ba, bb = D.discordant(A, B, byid, H)
    assert (ba, bb) == (1, 1), "same id, opposite direction counts on both sides; shared claims are dropped"
    assert D.discordant(A, A, byid, H) == (0, 0)
    M2 = mk_M({(m, "fa"): 9.0 for m in D.F_DEV}, n=40)  # every F_dev member significant, uts members not
    comps2, _ = comps_of(M2, [("fa", "fb")])
    by2 = {c["id"]: c for c in comps2}
    assert D.discordant({"D:fa|fb": 1}, {"D:fa|fb": -1}, by2, D.FOLDS["uts"][1]) == (1, 1), "breaks judged on H_u"


@check
def binomial_and_holm():
    assert abs(D.p_greater(9, 10) - 11 / 1024) < 1e-12 and D.p_greater(0, 0) == 1.0
    assert abs(D.p_greater(1, 10) - (1 - 1 / 1024)) < 1e-12
    rej = BF.holm({"a": 0.01, "b": 0.02, "c": 0.03, "d": 0.2}, D.ALPHA)
    assert rej == {"a": True, "b": False, "c": False, "d": False}
    rej2 = BF.holm({"a": 0.01, "b": 0.012, "c": 0.02, "d": 0.024}, D.ALPHA)
    assert all(rej2.values())


@check
def contrast_labels():
    assert D.contrast_label(9, True, False, "MARGIN") == "NOT_EVALUABLE"
    assert D.contrast_label(10, True, False, "MARGIN") == "SUPPORTED"
    assert D.contrast_label(10, False, True, "AER") == "AER BETTER"
    assert D.contrast_label(10, False, False, "AER") == "NOT SUPPORTED"
    assert D.N_FLOOR == 10 and D.ALPHA == 0.05


@check
def h1_h2_pooling():
    """Pooled break counts are the sums over the three folds; the four p-values all enter Holm."""
    w = stages()
    r = w["result"]
    for h, x in (("H1", "MG"), ("H2", "AER")):
        assert r[h]["b_FE"] == sum(f[f"{h}_b_FE"] for f in r["folds"].values())
        assert r[h][f"b_{x}"] == sum(f[f"{h}_b_{x}"] for f in r["folds"].values())
        assert r[h]["n"] == r[h]["b_FE"] + r[h][f"b_{x}"]
    assert set(r["p_one_sided_exact_nominal"]) == set(r["holm_reject_at_0.05"]) and len(r["holm_reject_at_0.05"]) == 4
    assert r["identity_M1_M1prime_F_dev"]["equal"] == len(w["D"])


# ------------------------------------------------------------------------------------------------ checks: H3
def h3c(sig_of):
    """A DEV-like comparison: one class per F_dev member; sig_of(member, metric) -> sig."""
    st = {1: [5.0, 1.0, 9.0, 2.0], -1: [-5.0, -9.0, -1.0, 2.0], 0: [0.5, -2.0, 3.0, 1.0]}
    return {"id": "D:x|y", "classes": {m: {"members": [m], **{met: list(st[sig_of(m, met)]) for met in D.METRICS}}
                                       for m in D.F_DEV}}


@check
def h3_counts():
    allp = h3c(lambda m, met: 1)
    tone = h3c(lambda m, met: 0 if m == "pyvi.tm.pk.cf" else 1)  # breaks through tone only
    unit = h3c(lambda m, met: 0 if m == "pyvi.tw.pk.cf" else 1)  # breaks inside the contract grid (a unit at tw)
    scorer = h3c(lambda m, met: -1 if met == "bleu" else 1)  # scorers disagree: no contract certificate
    syltone = h3c(lambda m, met: 0 if m == "syl.tf.pa.ck" and met == "rouge" else 1)
    r = D.h3([allp, tone, unit, scorer, syltone])
    assert (r["n"], r["k_T"]) == (3, 2), r
    assert r["k_T_by_unit_of_breaking_class"] == {"syl": 1, "rdr": 0, "pyvi": 1}
    assert r["DESCRIPTIVE"] == {"n_syl_grid": 4, "k_U": 1, "k_TU": 3}
    assert r["label"] == "NOT_EVALUABLE"


@check
def h3_trip_points():
    assert D.h3_label(31, 850) == "NULL" and D.h3_label(32, 850) == "INCONCLUSIVE"
    assert D.h3_label(53, 850) == "INCONCLUSIVE" and D.h3_label(54, 850) == "SUPPORTED"
    assert D.h3_label(20, 600) == "NULL" and D.h3_label(40, 600) == "SUPPORTED"
    assert D.h3_label(0, 58) == "NOT_EVALUABLE" and D.h3_label(0, 59) == "NULL"
    assert D.h3_label(58, 58) == "NOT_EVALUABLE", "NOT_EVALUABLE is decided first"


# ------------------------------------------------------------------------------------------------ checks: A3
@check
def a3_trip_points():
    assert D.a3_label(27, 27, 1000) == "AT OR BELOW NOMINAL"
    assert D.a3_label(28, 0, 1000) == "INCONCLUSIVE" and D.a3_label(0, 28, 1000) == "INCONCLUSIVE"
    assert D.a3_label(35, 0, 1000) == "INCONCLUSIVE" and D.a3_label(36, 0, 1000) == "ABOVE NOMINAL"
    assert D.a3_label(0, 36, 1000) == "ABOVE NOMINAL"
    lo, up = D.cp97(25, 1000)
    from scipy.stats import beta
    assert abs(up - beta.ppf(0.975, 26, 975)) < 1e-12 and abs(lo - beta.ppf(0.025, 25, 976)) < 1e-12


@check
def a3_draws_rule():
    keep = D.N_NULL
    D.N_NULL = 50
    try:
        dr = D.a3_draws(80, 20)
        idx = [i for i, _ in dr]
        assert len(idx) == 50 and len(set(idx)) == 50 and max(idx) < 80
        assert idx == list(np.random.default_rng(20261127).choice(80, 50, replace=False))
        for j in (0, 7, 49):
            assert np.array_equal(dr[j][1], np.random.default_rng(20261127 + j).integers(0, 2, 20) * 2 - 1)
        assert set(np.unique(dr[3][1])) <= {-1, 1}
    finally:
        D.N_NULL = keep


@check
def a3_rule_on_f0():
    """The A3 label is the rule on r_f0; r_A3 <= r_f0 per direction on the same nulls (the IUT bound)."""
    w = stages()
    a = w["result"]["A3"]
    assert a["label"] == D.a3_label(a["f0"]["pos"], a["f0"]["neg"], a["nulls"])
    assert a["A3_F_dev"]["pos"] <= a["f0"]["pos"] and a["A3_F_dev"]["neg"] <= a["f0"]["neg"]
    assert a["A3_F"]["pos"] <= a["A3_F_dev"]["pos"] and a["A3_F"]["neg"] <= a["A3_F_dev"]["neg"]
    pm = {m: [0, 0] for m in D.F_ALL}
    s = D.a3_summary({"f0": [10, 12], "A3_F_dev": [40, 0], "A3_F": [40, 0]}, pm, 1000)
    assert s["label"] == "AT OR BELOW NOMINAL", "the label must follow r_f0, not r_A3"
    s2 = D.a3_summary({"f0": [40, 0], "A3_F_dev": [10, 0], "A3_F": [10, 0]}, pm, 1000)
    assert s2["label"] == "ABOVE NOMINAL" and s2["A3_F_dev"]["r_pos"] == 0.01
    pm2 = {m: [0, 0] for m in D.F_ALL}
    pm2[D.F_UTS[3]] = [900, 800]  # a uts member has the largest rate; §5 A3 takes the max over the 54 F_dev members
    pm2[D.F_DEV[7]] = [30, 0]
    pm2[D.F_DEV[9]] = [0, 20]
    s3 = D.a3_summary({"f0": [0, 0], "A3_F_dev": [0, 0], "A3_F": [0, 0]}, pm2, 1000)
    assert s3["max_member_rate_F_dev_DESCRIPTIVE"] == {"pos": 0.03, "neg": 0.02}


@check
def a3_null_stats():
    """A swap null is stats(sigma * d) per class, the classes of the real comparison kept."""
    M = mk_M({(m, "fa"): 4.0 for m in D.F_DEV}, n=20)
    W = BF.boot_W(20)
    sg = np.random.default_rng(5).integers(0, 2, 20) * 2 - 1
    c = D.build(M, "D:fa|fb", W, sign=sg)
    k = M["midx"][BF.F0N]
    d = M["cider"][k, 0] - M["cider"][k, 1]
    assert D.f0_stats(c) == BF.stats(sg * d, W)
    k2 = M["midx"]["syl.tf.pa.ck"]
    d2 = M["cider"][k2, 0] - M["cider"][k2, 1]
    cl2 = next(cl for cl in c["classes"].values() if "syl.tf.pa.ck" in cl["members"])
    assert cl2["cider"] == BF.stats(sg * d2, W), "the swap applies to every member alike"
    assert set(c["classes"]) == set(D.build(M, "D:fa|fb", W)["classes"])


# ------------------------------------------------------------------------------------------------ checks: budget, text
@check
def cpu_budget():
    d = Path(tempfile.mkdtemp(prefix="b_d1_budget_"))
    try:
        assert D.budget(d) == 28800
        (d / "s0.time").write_text("\tUser time (seconds): 1000.50\n\tSystem time (seconds): 99.50\n")
        (d / "s1.time").write_text("\tUser time (seconds): 20000\n\tSystem time (seconds): 0.5\n")
        assert D.budget(d) == 7699, D.budget(d)
        (d / "s2.time").write_text("\tUser time (seconds): 7699.5\n\tSystem time (seconds): 0\n")
        assert D.budget(d) == 0
        rc, so = run_main(["budget", "--records", str(d)])
        assert rc == 5
        (d / "s2.time").unlink()
        (d / "STOP").write_text("")
        assert D.budget(d) == 0
    finally:
        shutil.rmtree(d)


@check
def no_text_in_outputs():
    w = stages()
    for f in ("S1.json", "G0.json", "RESULT_D1.json"):
        assert MARK not in (w["out"] / f).read_text(encoding="utf-8")
    with np.load(w["out"] / "PER_IMAGE_D1.npz", allow_pickle=False) as z:
        assert all(MARK not in str(x) for k in z.files if z[k].dtype.kind == "U" for x in np.ravel(z[k]))
    assert MARK not in w["s1"] + w["g0"] + w["s2"]
    for f in ("S1.json", "G0.json", "RESULT_D1.json"):
        assert oct((w["out"] / f).stat().st_mode)[-3:] == "444"


@check
def result_record():
    r = stages()["result"]
    assert r["registration_sha256"] == D.REG_SHA and "nominal" in r["label"]
    assert set(r) >= {"H1", "H2", "H3", "A3", "folds", "H2_descriptive", "identity_M1_M1prime_F_dev"}
    for u in ("syl", "pyvi", "uts"):
        assert set(r["H2_descriptive"][u]) >= {"FE", "AER", "AER_per_class", "f0", "flip_units"}


# ------------------------------------------------------------------------------------------------ checks added (CC-506 W4)
@check
def fe_claims():
    """M1 claims: CERTIFIED comparisons only, with the certified direction and z_min as margin."""
    cs = []
    for k, s in enumerate([(1, 1, 1), (1, 0, 1), (-1, -1, -1), (1, -1, 1), (0, 0, 0)]):
        c = cls(*s)
        c["id"] = f"D:x{k}|y"
        cs.append(c)
    cl = D.claims_fe(cs, D.F_DEV)
    assert set(cl) == {"D:x0|y", "D:x2|y"}, cl
    for i in cl:
        v = BF.certify(next(c for c in cs if c["id"] == i), set(D.F_DEV))
        assert cl[i] == (v["certified"], v["z_min"]) and cl[i][1] > 0


@check
def h1_h2_tests_and_holm():
    """h1_h2 with discordant() replaced by fixed counts: pooling, the four exact p-values, Holm at 0.05 and the labels;
    the H2 comparator is the per-member AER at K = min(|FE|, |AER|), the H1 comparator f0 at K = min(|FE|, |f0|)."""
    big = D.F_DEV[1:]  # 53 members in one class with delta -1, one single class with delta +20: in fold uts the
    delta = {(D.F_DEV[0], "fa"): 20.0, (big[0], "fa"): -1.0}  # per-member AER claims fa|fb, the per-class one does not
    M = mk_M(delta, n=40, merge={m: big[0] for m in big})
    comps, W = comps_of(M, [("fa", "fb"), ("fa", "fc"), ("fb", "fc")])
    vals = iter([(0, 4), (1, 3), (0, 4), (1, 3), (0, 4), (0, 4)])  # per fold: H1 then H2
    calls = []
    keep = D.discordant

    def fake(A, B, byid, H):
        calls.append((dict(A), dict(B)))
        return next(vals)
    D.discordant = fake
    try:
        r = D.h1_h2(M, comps, W)
    finally:
        D.discordant = keep
    assert (r["H1"]["b_FE"], r["H1"]["b_MG"], r["H2"]["b_FE"], r["H2"]["b_AER"]) == (0, 12, 2, 10)
    p = r["p_one_sided_exact_nominal"]
    assert abs(p["H1_FE_fewer"] - 1 / 4096) < 1e-15 and p["H1_MG_fewer"] == 1.0
    assert abs(p["H2_FE_fewer"] - 79 / 4096) < 1e-15 and abs(p["H2_AER_fewer"] - 4083 / 4096) < 1e-15
    assert r["holm_reject_at_0.05"] == {"H1_FE_fewer": True, "H1_MG_fewer": False, "H2_FE_fewer": False,
                                        "H2_AER_fewer": False}, "Holm at 0.05 (0.0193 > 0.05/3)"
    assert r["H1"]["label"] == "SUPPORTED" and r["H2"]["label"] == "NOT SUPPORTED"
    sig_c = D.sigma(M)
    f0 = D.claims_f0(comps)
    for k, (u, (G, _H)) in enumerate(D.FOLDS.items()):
        fe = D.claims_fe(comps, G)
        aer = D.claims_aer(M, comps, G, sig_c, W)
        k1, k2 = min(len(fe), len(f0)), min(len(fe), len(aer))
        assert calls[2 * k] == (D.top_k(fe, k1), D.top_k(f0, k1)), u
        assert calls[2 * k + 1] == (D.top_k(fe, k2), D.top_k(aer, k2)), u
        assert r["folds"][u]["K_H1"] == k1 and r["folds"][u]["K_H2"] == k2
    for u, (G, _H) in D.FOLDS.items():
        d = r["H2_descriptive"][u]
        assert d["AER"]["claims"] == len(D.claims_aer(M, comps, G, sig_c, W)), "the primary AER weights per member"
        assert d["AER_per_class"]["claims"] == len(D.claims_aer(M, comps, G, sig_c, W, per_class=True))
    G = D.FOLDS["uts"][0]
    pc = D.claims_aer(M, comps, G, sig_c, W, per_class=True)
    assert len(pc) < len(D.claims_aer(M, comps, G, sig_c, W)), "the fixture must separate the two weightings"


@check
def h1_h2_fixture_k():
    """On the text fixture: K_H1 = min(|FE|, |f0|), K_H2 = min(|FE|, |AER|) per fold, from the descriptive rows."""
    r = stages()["result"]
    for u, f in r["folds"].items():
        d = r["H2_descriptive"][u]
        assert f["K_H1"] == min(d["FE"]["claims"], d["f0"]["claims"])
        assert f["K_H2"] == min(d["FE"]["claims"], d["AER"]["claims"])
    for h, x in (("H1", "MG"), ("H2", "AER")):
        n = r[h]["n"]
        assert r["p_one_sided_exact_nominal"][f"{h}_FE_fewer"] == D.p_greater(r[h][f"b_{x}"], n)
        assert r["p_one_sided_exact_nominal"][f"{h}_{x}_fewer"] == D.p_greater(r[h]["b_FE"], n)


@check
def h2_descriptive_rows():
    """Coverage = share of held-out flip units with no ordering claimed; false-tie analogue on the stable units;
    flip incidence = FRAGILE over G_u as count, denominator and share."""
    M = mk_M({(m, "fa"): 9.0 for m in D.F_DEV}, n=40)  # fa|fb: f0 significant, uts members not -> a flip in fold uts
    comps, _W = comps_of(M, [("fa", "fb"), ("fb", "fc"), ("fa", "fc")])
    byid = {c["id"]: c for c in comps}
    G, H = D.FOLDS["uts"]
    row = D.h2_descriptive(comps, byid, G, H, {"X": {}, "Y": {"D:fa|fb": (1, 1.0)}, "Z": {"D:fa|fc": (1, 1.0)}})
    assert row["flip_units"] == 2 and row["units_sig_f0"] == 2
    assert row["X"]["coverage"] == 1.0 and row["Y"]["coverage"] == 0.5 and row["Z"]["coverage"] == 0.5
    assert row["X"]["false_tie_analogue"] is None
    fr = sum(BF.certify(c, set(G))["fragile"] for c in comps)
    assert row["flip_incidence_fragile_over_G"] == {"fragile": fr, "comparisons": 3, "share": fr / 3}


@check
def g0_verdict_over_F():
    """G0 (b) compares the verdict over F (72): a comparison CERTIFIED over F_dev but FRAGILE over F passes when
    RESULT.json says FRAGILE."""
    M = mk_M({(m, "fa"): 9.0 for m in D.F_DEV}, n=40)
    W = BF.boot_W(40)
    got = D.build(M, "D:fa|fb", W)
    assert BF.certify(got, set(D.F_DEV))["verdict"] != BF.certify(got, set(D.F_ALL))["verdict"]
    dev_c = {"classes": {k: {"members": [m for m in cl["members"] if m in D.F_DEV], "cider": list(cl["cider"])}
                         for k, cl in got["classes"].items() if any(m in D.F_DEV for m in cl["members"])}}
    row = D.g0_compare(dev_c, got, {"F": BF.certify(got, set(D.F_ALL))["verdict"], "D_f0": D.f0_stats(got)[0]})
    assert not row["verdict_mismatch"] and D.g0_pass([row])["pass"]


@check
def g0_sig_gate():
    """CC-506 W2: a stored F_dev class whose L crosses 0 by less than 1e-6 fails G0 (sig differs), although every
    |difference| <= 1e-6."""
    got = {"classes": {"k0": {"members": [BF.F0N], "cider": [2.0, 4e-7, 4.0, 1.0]},
                       "k1": {"members": [D.F_UTS[0]], "cider": [2.0, 1.0, 4.0, 1.0]}}}
    dev_c = {"classes": {"k0": {"members": [BF.F0N], "cider": [2.0, -4e-7, 4.0, 1.0]}}}
    row = D.g0_compare(dev_c, got, {"F": BF.certify(got, set(D.F_ALL))["verdict"], "D_f0": 2.0})
    s = D.g0_pass([row])
    assert s["max_abs_diff"] <= 1e-6 and s["sig_mismatch"] == 1 and not s["pass"]
    dev_ok = {"classes": {"k0": {"members": [BF.F0N], "cider": [2.0, 4e-7 + 5e-7, 4.0, 1.0]}}}
    assert D.g0_pass([D.g0_compare(dev_ok, got, {"F": BF.certify(got, set(D.F_ALL))["verdict"], "D_f0": 2.0})])["pass"]


@check
def a3_counts_by_family():
    """a3(): counts per direction (not pooled), r_A3 over F_dev (54) and over F (72), with certify stubbed."""
    M = mk_M({}, n=20)
    comps, W = comps_of(M, [("fa", "fb"), ("fa", "fc"), ("fb", "fc"), ("fa", "fd")], n=20)
    keep, keepn = BF.certify, D.N_NULL
    seen = {"k": 0}

    def fake(c, G, metric="cider"):
        seen["k"] += 1
        d = 1 if (seen["k"] // 2) % 2 == 0 else -1  # draws alternate +1 / -1; called F_dev then F per draw
        return {"certified": d if len(G) == 54 else 0, "verdict": "x", "fragile": False}
    BF.certify, D.N_NULL = fake, 4
    try:
        a = D.a3(M, comps, W)
    finally:
        BF.certify, D.N_NULL = keep, keepn
    assert (a["A3_F_dev"]["pos"], a["A3_F_dev"]["neg"]) == (2, 2), a["A3_F_dev"]
    assert (a["A3_F"]["pos"], a["A3_F"]["neg"]) == (0, 0), "A3_F is the certificate over the 72 members of F"


# ------------------------------------------------------------------------------------------------ main
def main() -> int:
    ap = argparse.ArgumentParser()
    ap.add_argument("--only", nargs="*")
    a = ap.parse_args()
    res = {}
    for fn in CHECKS:
        if a.only and fn.__name__ not in a.only:
            continue
        try:
            fn()
            res[fn.__name__] = "ok"
        except (AssertionError, BF.Fault, SystemExit):
            res[fn.__name__] = "FAIL"
        except Exception as e:  # noqa: BLE001
            res[fn.__name__] = f"CRASH ({type(e).__name__})"
    for n, r in res.items():
        print(f"SELFTEST {r} {n}")
    if "root" in _W:
        for p in Path(_W["root"]).rglob("*"):
            with contextlib.suppress(OSError):
                os.chmod(p, 0o755 if p.is_dir() else 0o644)
        shutil.rmtree(_W["root"], ignore_errors=True)
    ok = sum(r == "ok" for r in res.values())
    print(f"selftest: {ok} ok of {len(res)} checks")
    return 0 if ok == len(res) else 1


if __name__ == "__main__":
    sys.exit(main())
