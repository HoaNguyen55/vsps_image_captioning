#!/usr/bin/env python3
"""Self-tests of scripts/b_alt/b_alt.py and cpu_guard.py (prereg v2 §5 S0). Synthetic fixtures only, in a temp dir:
stub word units joining invented syllables (zba, zbe, ...), invented captions carrying the marker syllable MARK, no
data-set file, no system output. Each check prints `SELFTEST ok|FAIL|CRASH <name>`.
    python3 -I -B scripts/b_alt/test_b_alt.py [--only NAME ...]
Exit 0 only when every check is ok."""
import argparse
import contextlib
import io
import itertools
import json
import os
import shutil
import subprocess
import sys
import tempfile
import time
from collections import Counter
from pathlib import Path

import numpy as np

HERE = Path(__file__).resolve().parent
sys.path.insert(0, str(HERE))
import b_alt as A  # noqa: E402

BF, FM, PT = A.BF, A.FM, A.PT
MARK = "zqxv"
AT_IMPORT = {k: getattr(A, k) for k in ("HALF", "EXPECT_D", "EXPECT_IMAGES", "EXPECT_FILES", "SEED_SPLIT", "SEED_WB",
                                        "COVER_NUM", "COVER_DEN", "MIN_TYPES", "UNALIGNED_MAX", "SHIFT_FLOOR",
                                        "RHO_ALL_FLOOR", "PRACTICAL", "G0_TOL", "REG_SHA", "ERRATA", "REG")}
CHECKS = []


def check(fn):
    CHECKS.append(fn)
    return fn


# ------------------------------------------------------------------------------------------------ stub units
def joiner(groups, skip_after=()):
    """A stub word unit: greedy longest join of the listed syllable groups, except right after a syllable in
    skip_after (a context the dictionary cannot see)."""
    gs = sorted(groups, key=len, reverse=True)

    def seg(ts):
        out = []
        for t in ts:
            w, res, k = t.replace(".", " . ").split(), [], 0
            while k < len(w):
                for g in gs:
                    if tuple(w[k:k + len(g)]) == g and not (k > 0 and w[k - 1] in skip_after):
                        res.append("_".join(g))
                        k += len(g)
                        break
                else:
                    res.append(w[k])
                    k += 1
            out.append(res)
        return out
    return seg


RDR_G = [("zba", "zbe"), ("zda", "zde"), ("ghoà", "zfe"), ("ghòa", "zfe"), ("zga", "zge"), ("zha", "zhe"),
         ("zxa", "zxe")]
PYVI_G = [("zca", "zce"), ("zde", "zdi"), ("zga", "zge", "zgi"), ("zka", "zke")]
STUB = {"syl": FM.SEG["syl"], "chr": FM.SEG["chr"], "rdr": joiner(RDR_G, skip_after={"zqq"}),
        "pyvi": joiner(PYVI_G), "uts": joiner([("zba", "zbe")])}

# ------------------------------------------------------------------------------------------------ text world
N_IMG = 20
OWN = ["o1-short", "o2-short", "o3-short", "o4-short"]
PHR = ["zba zbe", "zca zce", "zda zde zdi", "ghoà zfe", "zga zge zgi", "zha zhe", "zka zke", "zqq zba zbe"]
_W = {}


def _ref(i, j):
    return f"{MARK} {PHR[(i + j) % 8]} zmo {PHR[(i * 3 + j) % 8]}."


def _cap(n, i):
    return {"o1-short": _ref(i, 0),
            "o2-short": _ref(i, 1).replace("ghoà", "ghòa"),
            "o3-short": f"{MARK} zmo {PHR[(i + 5) % 8]} zxa zxe",
            "o4-short": f"{MARK} {PHR[i % 8]} zmo {PHR[(i + 2) % 8]} zyy"}[n]


def _dump(p: Path, o):
    p.parent.mkdir(parents=True, exist_ok=True)
    p.write_text(json.dumps(o, ensure_ascii=False), encoding="utf-8")


def world() -> dict:
    """Synthetic NCS tree and work dir (SYSTEMS, CENSUS, FAMILY, DEV built with b_fecert's own functions)."""
    if _W:
        return _W
    root = Path(tempfile.mkdtemp(prefix="b_alt_selftest_"))
    data, work, base, out = root / "ncs", root / "work", root / "base", root / "out"
    ids = list(range(1, N_IMG + 1))
    kt = data / "datasets/ktvic/test_data.json"
    _dump(kt, {"images": [{"id": i, "filename": f"{i:011d}.jpg"} for i in ids],
               "annotations": [{"image_id": i, "id": 10 * i + j, "caption": _ref(i, j)} for i in ids for j in range(2)]})
    for n in OWN:
        _dump(data / f"results/{n}.preds.json", {str(i): _cap(n, i) for i in ids})
    for n, f in BF.BASE.items():
        verb = "zna" if "res" in n else "zne"
        _dump(base / f, [{"image_id": i, "caption": f"{MARK} zba_zbe {verb} zka zke"} for i in ids])
    BF.set_data(data)
    rows = [(n, "short", n.split("-")[0], A.sha_file(data / f"results/{n}.preds.json"), "x", "own") for n in OWN]
    rows += [(n, "baseline", "baseline", A.sha_file(base / f), "x", "baseline") for n, f in BF.BASE.items()]
    work.mkdir(parents=True)
    (work / "SYSTEMS.tsv").write_text("name\tstratum\tfamily\tsha256\tgit_blob\trole\n" +
                                      "".join("\t".join(r) + "\n" for r in rows), encoding="utf-8")
    names = [r[0] for r in rows]
    Dl = [f"D:{a}|{b}" for a, b in itertools.combinations(names, 2)]
    _dump(work / "CENSUS.json", {"systems_tsv_sha256": A.sha_file(work / "SYSTEMS.tsv"), "D": Dl,
                                 "uts_moved_to_dev": False})
    _dump(work / "FAMILY.json", {"units_dropped": [], "refs_sha256": A.sha_file(kt)})
    refs = PT.load_refs(kt)
    sid = sorted(refs)
    texts = BF.ktvic_texts(work, base)
    tk = FM.Tok(STUB)
    tk.prime([r for i in sid for r in refs[i]] + [t[i] for t in texts.values() for i in sid], FM.F_DEV)
    comps = BF.ktvic_comps(Dl)
    BF.run_list(sid, comps, FM.members(FM.DEV_UNITS), BF.scorer(tk, refs, sid, texts))
    _dump(work / "DEV.json", {"comparisons": comps})
    A.INPUT_SHA.update({f: A.sha_file(work / f) for f in ("DEV.json", "FAMILY.json", "CENSUS.json", "SYSTEMS.tsv")})
    A.REFS_SHA = A.sha_file(kt)
    A.EXPECT_FILES, A.EXPECT_IMAGES, A.EXPECT_D, A.HALF, A.MIN_TYPES = len(names), N_IMG, len(Dl), N_IMG // 2, 3
    A.SEG = STUB
    BF.env_record = lambda a: {"stub": True}
    BF.env_check = lambda rec: None
    _W.update(root=root, data=data, work=work, base=base, out=out, refs=refs, ids=sid, texts=texts, D=Dl)
    return _W


def run_main(argv) -> tuple[int, str]:
    buf = io.StringIO()
    with contextlib.redirect_stdout(buf):
        try:
            rc = A.main(argv)
        except SystemExit as e:
            rc = e.code if isinstance(e.code, int) else 9
            print(str(e.code))
    return rc, buf.getvalue()


def stages(out=None) -> dict:
    """s1a -> s1b -> g0 -> s2 once on the synthetic world (into `out`, default the world's out dir)."""
    w = world()
    key = str(out or w["out"])
    if key in w.get("runs", {}):
        return w["runs"][key]
    o, wk = key, str(w["work"])
    r = {"out": Path(o)}
    rc, r["s1a"] = run_main(["s1a", "--work", wk, "--out", o])
    assert rc == 0, r["s1a"]
    r["census"] = A.sha_file(Path(o) / "CENSUS_ALT.json")
    rc, r["s1b"] = run_main(["s1b", "--work", wk, "--out", o, "--baselines", str(w["base"]), "--census-sha", r["census"]])
    assert rc == 0, r["s1b"]
    r["npz"] = A.sha_file(Path(o) / "PER_IMAGE_ALT.npz")
    rc, r["g0"] = run_main(["g0", "--work", wk, "--out", o, "--npz-sha", r["npz"]])
    assert rc == 0, r["g0"]
    r["g0sha"] = A.sha_file(Path(o) / "G0_ALT.json")
    rc, r["s2"] = run_main(["s2", "--work", wk, "--out", o, "--census-sha", r["census"], "--npz-sha", r["npz"],
                            "--g0-sha", r["g0sha"]])
    assert rc == 0, r["s2"]
    r["result"] = A.jload(Path(o) / "RESULT_ALT.json")
    w.setdefault("runs", {})[key] = r
    return r


# ------------------------------------------------------------------------------------------------ hand-built matrices
def mk_M(shift, n=30, files=("fa", "fb", "fc", "fd"), seed=3) -> dict:
    """Matrix world without text: cider[member, file, image] = 50 + noise + shift(member name, file index) * w_i."""
    rng = np.random.default_rng(seed)
    noise = rng.normal(0, 2.0, (len(files), n))
    wimg = 1 + 1.2 * rng.standard_normal(n)  # some images shift the other way
    C = np.zeros((len(A.NAMES), len(files), n))
    for k, m in enumerate(A.NAMES):
        for j in range(len(files)):
            C[k, j] = 50 + noise[j] + shift(m, j) * wimg
    K = np.array([[f"{j:02d}{k:014d}" for j in range(len(files))] for k in range(len(A.NAMES))], dtype="<U16")
    RK = np.array([f"r{k:015d}" for k in range(len(A.NAMES))], dtype="<U16")
    M = {"cider": C, "keys": K, "rkeys": RK, "members": np.array(A.NAMES), "files": np.array(files)}
    M["fidx"] = {f: j for j, f in enumerate(files)}
    M["midx"] = {m: k for k, m in enumerate(A.NAMES)}
    return M


def shift_world(rem_head, rem_tail, const=0.0):
    """pyvi shift per file j: removable head part h_j, removable tail part t_j, non-removable part u_j = const * j.
    Pi_head removes h; Pi_all removes h and t; nothing removes u."""
    def f(m, j):
        if not m.startswith("pyvi"):
            return 0.0
        h, t, u = rem_head * (j + 1), rem_tail * 0.3 * (j + 1) ** 2, const * (j + 1)  # all rise with j
        return u + (0 if m.endswith("+Ph") or m.endswith("+Pa") else h) + (0 if m.endswith("+Pa") else t)
    return f


COMPS4 = list(itertools.combinations(("fa", "fb", "fc", "fd"), 2))


def est(M, n_counts=None, seed=5):
    cols = np.arange(M["cider"].shape[2])
    u = A.unit_vectors(M, COMPS4, cols)
    rng = np.random.default_rng(seed)
    na = rng.integers(5, 15, len(cols))
    nh = np.minimum(na, rng.integers(2, 12, len(cols)))
    cnt = n_counts if n_counts is not None else np.stack([nh, na], 1)
    W = BF.boot_W(len(cols), A.SEED_WB)
    return u, A.estimands(u["v"], cnt, cnt, W), W, cnt


# ------------------------------------------------------------------------------------------------ checks: pins, sets
@check
def pins_and_closure():
    A.pin_check()
    A.closure_check()
    bad = dict(A.PINS)
    bad["scripts/b_fecert/family.py"] = "0" * 64
    try:
        A.pin_check(pins=bad)
    except SystemExit as e:
        assert "FAULT" in str(e)
    else:
        raise AssertionError("an off-pin file passed")
    assert "scripts/b_d1/b_d1.py" in A.PINS and A.PINS["scripts/b_d1/b_d1.py"].startswith("4e044401")
    assert A.JAR_SHA_FULL == "9e2811cdbc2ddfc71d04be5dc36e185c88dcd1ad4d5d69e4ff2e1369dccf7793"


@check
def jar_full_pin():
    old_seg, old_rec, old_chk = A.SEG, BF.env_record, BF.env_check
    try:
        A.SEG = None
        BF.env_check = lambda rec: None
        BF.env_record = lambda a: {"jar_sha256": "9e2811cd" + "0" * 56}
        try:
            A.env_ok(None)
        except BF.Fault:
            pass
        else:
            raise AssertionError("a jar that matches only the 8-hex prefix passed")
        BF.env_record = lambda a: {"jar_sha256": A.JAR_SHA_FULL}
        A.env_ok(None)
    finally:
        A.SEG, BF.env_record, BF.env_check = old_seg, old_rec, old_chk


@check
def member_sets():
    assert len(A.RAW) == 36 and len(A.MEMS) == 108 and len(A.LEVELS) == 18
    assert A.G_W[:18] == [f"rdr.{t}.{p}.{c}" for t, p, c in A.LEVELS] and BF.F0N == "rdr.tw.pk.cf" == A.G_W[0]
    assert A.NAMES[36] == "rdr.tw.pk.cf+Ph" and A.NAMES[72] == "rdr.tw.pk.cf+Pa"
    assert A.RDR0 == FM.F0 and A.PYVI0 == ("pyvi", "tw", "pk", "cf")


@check
def pairs_same_levels():
    pr = A.pairs_by_level()
    assert len(pr) == 18
    for r, p, lv in pr:
        assert r.split(".")[0] == "rdr" and p.split(".")[0] == "pyvi"
        assert r.split(".")[1:] == p.split(".")[1:] == list(lv)


# ------------------------------------------------------------------------------------------------ checks: split
@check
def split_exact():
    ids = [f"{k:05d}" for k in range(558)]
    old = A.HALF
    try:
        A.HALF = 279
        a, b = A.split(list(reversed(ids)))
    finally:
        A.HALF = old
    perm = np.random.default_rng(20261127).permutation(558)
    assert a == [ids[k] for k in perm[:279]] and b == [ids[k] for k in perm[279:]]
    assert len(a) == len(b) == 279 and not set(a) & set(b) and A.SEED_SPLIT == 20261127


# ------------------------------------------------------------------------------------------------ checks: syllables
@check
def tone_key_and_explode():
    assert A.syl_key("ghoà") == A.syl_key("ghòa") == A.syl_key("GHÒA")
    assert A.syl_key("zba") != A.syl_key("zbe")
    assert A.explode(["zba_zbe", "zmo", "."]) == (["zba", "zbe", "zmo", "."], [False, True, True])
    assert A.explode(["zba__zbe"]) is None and A.explode(["_zba"]) is None
    assert A.rebuild(["zba", "zbe", "zmo"], [False, True]) == ["zba_zbe", "zmo"]
    assert A.rebuild([], []) == []


@check
def spans_rule():
    # syllables 0..5; a: [0 1][2][3 4][5]; b: [0][1 2][3 4 5]
    ba = [False, True, True, False, True]
    bb = [True, False, True, False, False]
    assert A.spans(ba, bb, 6) == [(0, 3), (3, 6)]
    assert A.spans(ba, ba, 6) == []
    t = A.disagreements(["zda_zde", "zdi"], ["zda", "zde_zdi"])
    assert t == [(("zda", "zde", "zdi"), (False, True))]
    assert A.disagreements(["ghoà_zfe"], ["ghòa", "zfe"]) == [(("ghoà", "zfe"), (False,))]
    assert A.disagreements(["zba_zbe"], ["zba", "zbx"]) is None  # unaligned


@check
def census_counts_and_tone_merge():
    tk = FM.Tok(STUB)
    cz = A.census(["ghoà zfe zmo", "ghòa zfe zmo", "zba zbe", "zca zce zmo"], tk)
    occ = {A.type_str(t): n for t, n in cz["occ"].items()}
    assert occ == {"ghoà zfe": 2, "zba zbe": 1, "zca zce": 1}, occ
    assert cz["unaligned"] == 0 and cz["strings"] == 4


@check
def pin_list_rules():
    t = lambda s: tuple(s.split())  # noqa: E731
    occ = Counter({t("zb zc"): 4, t("za zc"): 4, t("zd ze"): 1, t("zf zg"): 1})
    pats = {t("zb zc"): Counter({(True,): 2, (False,): 2}), t("za zc"): Counter({(False,): 4}),
            t("zd ze"): Counter({(True,): 1}), t("zf zg"): Counter({(False,): 1})}
    pl = A.pin_lists(occ, pats)
    assert [A.type_str(x) for x in pl["order"]] == ["za zc", "zb zc", "zd ze", "zf zg"]  # ties by code point
    assert [A.type_str(x) for x in pl["head"]] == ["za zc", "zb zc"]  # 8 of 10 = 0.80 exactly: included
    assert pl["dict"][t("zb zc")] == (False,)  # modal tie -> fewer tokens (joined)
    p3 = A.pin_lists(Counter({t("za zb zc"): 2}), {t("za zb zc"): Counter({(True, False): 1, (False, True): 1})})
    assert p3["dict"][t("za zb zc")] == (False, True)  # same token count -> smallest vector
    occ2 = Counter({t("za zc"): 8, t("zb zc"): 1, t("zd ze"): 1, t("zf zg"): 1})
    assert len(A.pin_lists(occ2, {**pats, t("za zc"): Counter({(False,): 8})})["head"]) == 2  # 8/11 < 0.80


@check
def pin_rule():
    d = {("zda", "zde", "zdi"): (True, False), ("zda", "zde"): (False,), ("zba", "zbe"): (False,)}
    toks, bad = A.pin(["zmo_zda", "zde", "zdi_zmo", "Zba", "zbe"], d, 3)
    assert not bad and toks == ["zmo", "zda", "zde_zdi", "zmo", "Zba_zbe"], toks  # longest match; ends forced; case kept
    assert A.pin(toks, d, 3)[0] == toks  # idempotent
    assert A.pin(["zda", "zde", "zdi"], {}, 0)[0] == ["zda", "zde", "zdi"]  # empty list: identity
    assert A.pin(["zba__zbe"], d, 3) == (["zba__zbe"], True)  # malformed: unchanged, flagged


@check
def pin_tok_both_units():
    d = {("zba", "zbe"): (False,)}
    tk = A.PinTok(STUB, {"h": d, "a": d})
    m = ("rdr", "tw", "pk", "cf")
    try:
        tk.tokens("zqq zba zbe", m + ("a",))
    except Exception as e:  # noqa: BLE001  a pinned rdr member must be handled like a pinned pyvi member
        raise AssertionError(type(e).__name__) from e
    assert tk.tokens("zqq zba zbe", m) == ["zqq", "zba", "zbe"]  # rdr's context exception
    assert tk.tokens("zqq zba zbe", m + ("h",)) == ["zqq", "zba_zbe"]  # pinned rdr follows the dictionary
    assert tk.tokens("zba zbe zmo", ("pyvi", "tw", "pk", "cf", "a")) == ["zba_zbe", "zmo"]
    assert tk.side("zqq zba zbe", "matched", m + ("h",), True) == "zqq zba_zbe"


# ------------------------------------------------------------------------------------------------ checks: stages
@check
def census_reads_half_a_references_only():
    w, r = world(), stages()
    cz = A.jload(r["out"] / "CENSUS_ALT.json")
    half_a, _ = A.split(w["ids"])
    assert cz["strings"] == sum(len(w["refs"][i]) for i in half_a) and cz["half_A_images"] == len(half_a)
    tk = FM.Tok(STUB)
    want = A.census([s for i in half_a for s in w["refs"][i]], tk)
    got = {tuple(t): n for t, _p, n in cz["dict"]}
    assert got == dict(want["occ"])
    assert all(t != ["zxa", "zxe"] for t, _p, _n in cz["dict"])  # outputs never enter the census


@check
def s1b_matches_fecert_scorer():
    w, r = world(), stages()
    with np.load(r["out"] / "PER_IMAGE_ALT.npz", allow_pickle=False) as z:
        C, K, files = z["cider"], z["keys"], list(z["files"])
    tk = FM.Tok(STUB)
    per = BF.scorer(tk, w["refs"], w["ids"], w["texts"])
    for m in (FM.F0, ("pyvi", "tf", "pa", "ck")):
        o, k = per(m), A.NAMES.index(".".join(m))
        for j, f in enumerate(files):
            assert np.allclose(C[k, j], o[f]["cider"], atol=1e-12) and K[k, j] == o[f]["key"]


@check
def s1b_pinned_members_and_counts():
    w, r = world(), stages()
    cz = A.load_census(r["out"], r["census"])
    with np.load(r["out"] / "PER_IMAGE_ALT.npz", allow_pickle=False) as z:
        C, cref, cout = z["cider"], z["counts_ref"], z["counts_out"]
    tk = A.PinTok(STUB, {"h": cz["head"], "a": cz["all"]})
    per = A.per_cider(tk, w["refs"], w["ids"], w["texts"])
    m = ("pyvi", "tw", "pa", "cf", "h")
    o, k = per(m), A.NAMES.index("pyvi.tw.pa.cf+Ph")
    for j, f in enumerate(w["texts"]):
        assert np.allclose(C[k, j], o[f]["cider"], atol=1e-12)
    head, al = set(cz["head"]), set(cz["all"])
    i0 = w["ids"][0]
    assert list(cref[0]) == A.count_disagreements(tk, w["refs"][i0], head, al)
    assert list(cout[0]) == A.count_disagreements(tk, [t[i0] for t in w["texts"].values()], head, al)
    assert cout[:, 2].sum() > 0  # output-only types (zxa zxe) are counted apart


@check
def g0_pass_on_fecert_world():
    r = stages()
    g = A.jload(r["out"] / "G0_ALT.json")
    assert g["pass"] and g["comparisons"] == A.EXPECT_D and g["max_abs_diff"] <= 1e-9


def _g0_rows(mut):
    w, r = world(), stages()
    M = A.load_matrix(r["out"] / "PER_IMAGE_ALT.npz", r["npz"])
    dev = A.jload(w["work"] / "DEV.json")
    W = BF.boot_W(M["cider"].shape[2])
    rows = []
    for c in dev["comparisons"]:
        got = A.classes_of(M, *A.pair_of(c["id"]), A.G_W, W)
        mut(c, got)
        rows.append(A.g0_compare(c, got))
    return A.g0_pass(rows)


@check
def g0_tolerance_and_sig():
    def small(c, got):
        next(iter(got["classes"].values()))["cider"][0] += 5e-7

    def big(c, got):
        next(iter(got["classes"].values()))["cider"][3] += 5e-6

    def cross(c, got):  # L crosses 0 by 8e-7, inside the tolerance: only the sig gate can catch it
        k, cl = next(iter(got["classes"].items()))
        d0, sd = cl["cider"][0], cl["cider"][3]
        c["classes"][k]["cider"] = [d0, -4e-7, 1.0, sd]
        cl["cider"] = [d0, 4e-7, 1.0, sd]
    assert _g0_rows(small)["pass"] and not _g0_rows(big)["pass"]
    s = _g0_rows(cross)
    assert s["sig_mismatch"] > 0 and s["max_abs_diff"] <= A.G0_TOL and not s["pass"]


@check
def g0_membership_and_keys():
    def move(c, got):
        cl = list(got["classes"].values())
        if len(cl) > 1:
            cl[1]["members"].append(cl[0]["members"].pop())

    def rekey(c, got):
        k = next(iter(got["classes"]))
        got["classes"]["x" + k] = got["classes"].pop(k)
    assert not _g0_rows(move)["pass"] and not _g0_rows(rekey)["pass"]
    old = A.EXPECT_D
    try:
        A.EXPECT_D = old + 1
        assert not _g0_rows(lambda c, g: None)["pass"]
    finally:
        A.EXPECT_D = old


@check
def stage_guards():
    w, r = world(), stages()
    o, wk = str(r["out"]), str(w["work"])
    rc, so = run_main(["s1b", "--work", wk, "--out", o, "--baselines", str(w["base"]), "--census-sha", "0" * 64])
    assert rc != 0 and "REFUSED" in so
    rc, so = run_main(["g0", "--work", wk, "--out", o, "--npz-sha", "0" * 64])
    assert rc != 0 and "REFUSED" in so
    rc, so = run_main(["s2", "--work", wk, "--out", o, "--census-sha", r["census"], "--npz-sha", r["npz"],
                       "--g0-sha", r["g0sha"]])
    assert rc != 0 and "exists" in so  # a stage runs once
    rc, so = run_main(["s1b", "--work", wk, "--out", o, "--baselines", str(w["base"]), "--census-sha", r["census"]])
    assert rc != 0 and "exists" in so
    tmp = Path(tempfile.mkdtemp(dir=w["root"]))
    shutil.copy(r["out"] / "CENSUS_ALT.json", tmp)
    shutil.copy(r["out"] / "PER_IMAGE_ALT.npz", tmp)
    g = A.jload(r["out"] / "G0_ALT.json")
    for bad in ({**g, "pass": False}, {**g, "PER_IMAGE_ALT.npz": "0" * 64}):
        p = tmp / "G0_ALT.json"
        if p.exists():
            os.chmod(p, 0o644)
        p.write_text(json.dumps(bad), encoding="utf-8")
        rc, so = run_main(["s2", "--work", wk, "--out", str(tmp), "--census-sha", r["census"], "--npz-sha", r["npz"],
                           "--g0-sha", A.sha_file(p)])
        assert rc != 0 and "REFUSED" in so, so


@check
def census_floor_iii_stops_chain():
    w = world()
    out = Path(tempfile.mkdtemp(dir=w["root"]))
    old = A.MIN_TYPES
    try:
        A.MIN_TYPES = 10 ** 6
        rc, so = run_main(["s1a", "--work", str(w["work"]), "--out", str(out)])
    finally:
        A.MIN_TYPES = old
    assert rc == 0 and "NOT_EVALUABLE (iii)" in so
    c = A.sha_file(out / "CENSUS_ALT.json")
    rc, so = run_main(["s1b", "--work", str(w["work"]), "--out", str(out), "--baselines", str(w["base"]),
                       "--census-sha", c])
    assert rc != 0 and "REFUSED" in so
    n_types = A.jload(stages()["out"] / "CENSUS_ALT.json")["types"]
    out2 = Path(tempfile.mkdtemp(dir=w["root"]))
    try:
        A.MIN_TYPES = n_types  # exactly the floor: passes
        rc, so = run_main(["s1a", "--work", str(w["work"]), "--out", str(out2)])
    finally:
        A.MIN_TYPES = old
    assert rc == 0 and "NOT_EVALUABLE" not in so, so


@check
def census_floor_ii_unaligned():
    w = world()
    out = Path(tempfile.mkdtemp(dir=w["root"]))
    old = STUB["pyvi"]
    try:
        STUB["pyvi"] = lambda ts: [s[:-1] if s and s[-1] == "." else s for s in old(ts)]  # drops the final '.'
        rc, so = run_main(["s1a", "--work", str(w["work"]), "--out", str(out)])
    finally:
        STUB["pyvi"] = old
    assert rc == 0 and "FAULT (ii)" in so
    old_max = A.UNALIGNED_MAX
    out2 = Path(tempfile.mkdtemp(dir=w["root"]))
    try:
        A.UNALIGNED_MAX = 1.0
        STUB["pyvi"] = lambda ts: [s[:-1] if s and s[-1] == "." else s for s in old(ts)]
        rc, so = run_main(["s1a", "--work", str(w["work"]), "--out", str(out2)])
    finally:
        STUB["pyvi"], A.UNALIGNED_MAX = old, old_max
    assert "FAULT (ii)" not in so  # share 1.0 is not > 1.0


# ------------------------------------------------------------------------------------------------ checks: estimands
def _oracle(M, cols):
    """Independent recomputation of the unit sums with sigma fixed from the half-sample mean raw shift."""
    out = {"A": 0, "Ah": 0, "Aa": 0}
    for r, p, _lv in A.pairs_by_level():
        for a, b in COMPS4:
            ja, jb = M["fidx"][a], M["fidx"][b]

            def dl(suf):
                Cr, Cp = M["cider"][M["midx"][r + suf]][:, cols], M["cider"][M["midx"][p + suf]][:, cols]
                return (Cp[ja] - Cp[jb]) - (Cr[ja] - Cr[jb])
            s = np.sign(dl("").mean())
            out["A"] = out["A"] + s * dl("")
            out["Ah"] = out["Ah"] + s * dl("+Ph")
            out["Aa"] = out["Aa"] + s * dl("+Pa")
    return out


@check
def sigma_fixed_unit_sums():
    M = mk_M(shift_world(1.0, 0.7, 0.3))
    cols = np.arange(M["cider"].shape[2])
    u = A.unit_vectors(M, COMPS4, cols)
    o = _oracle(M, cols)
    for k in ("A", "Ah", "Aa"):
        assert np.allclose(u["v"][k], o[k], atol=1e-9)
    assert u["s"]["units"] == 18 * len(COMPS4)


@check
def head_only_tail_only_worlds():
    _u, e, _W, _c = est(mk_M(shift_world(1.0, 0.0)))
    p = e["point"]
    assert abs(p["rho_head"][0] - 1) < 1e-9 and abs(p["kappa_head"][0] - 1) < 1e-9 and abs(p["rho_all"][0] - 1) < 1e-9
    _u, e, _W, _c = est(mk_M(shift_world(0.0, 1.0)))
    p = e["point"]
    assert abs(p["rho_head"][0]) < 1e-9 and abs(p["kappa_head"][0]) < 1e-9 and abs(p["rho_all"][0] - 1) < 1e-9


@check
def nonremovable_shift_leaves_kappa():
    _u, e0, _W, _c = est(mk_M(shift_world(1.0, 1.0, 0.0)))
    _u, e1, _W, _c = est(mk_M(shift_world(1.0, 1.0, 2.0)))
    k0, k1 = e0["point"]["kappa_head"][0], e1["point"]["kappa_head"][0]
    assert abs(k0 - k1) < 1e-9, (k0, k1)
    assert e1["point"]["rho_head"][0] < e0["point"]["rho_head"][0] - 0.05
    assert np.allclose(e0["draws"]["kappa_head"], e1["draws"]["kappa_head"], atol=1e-9)


@check
def empty_pin_is_identity():
    M = mk_M(lambda m, j: (0.8 * (j + 1)) if m.startswith("pyvi") else 0.0)  # no member removes anything
    _u, e, _W, _c = est(M)
    assert abs(e["point"]["rho_head"][0]) < 1e-12 and abs(e["point"]["rho_all"][0]) < 1e-12


@check
def kappa_label_reads_kappa_not_rho():
    _u, e, _W, _c = est(mk_M(shift_world(1.0, 1.0, 2.0)))
    d, p = e["draws"], e["point"]
    lo = np.minimum(d["c_ref"], d["c_out"])
    assert np.allclose(d["d_lo"], d["kappa_head"] - lo) and np.allclose(d["d_hi"], d["kappa_head"] -
                                                                         np.maximum(d["c_ref"], d["c_out"]))
    assert abs(p["kappa_head"][0] - p["rho_head"][0]) > 0.05  # so a label read from rho_head would differ


@check
def coverage_recomputed_per_draw():
    _u, e, W, cnt = est(mk_M(shift_world(1.0, 1.0)))
    d = e["draws"]
    want = (W @ cnt[:, 0]) / (W @ cnt[:, 1])
    assert np.allclose(d["c_ref"], want) and np.allclose(d["c_out"], want) and d["c_ref"].std() > 1e-4
    assert abs(e["point"]["c_ref"][0] - cnt[:, 0].sum() / cnt[:, 1].sum()) < 1e-12


@check
def bootstrap_draws_registered_seed():
    w, r = world(), stages()
    res = r["result"]
    M = A.load_matrix(r["out"] / "PER_IMAGE_ALT.npz", r["npz"])
    ids = [str(i) for i in M["ids"]]
    _a, half_b = A.split(ids)
    cols = np.array([ids.index(i) for i in half_b])
    comps = [A.pair_of(c) for c in w["D"]]
    u = A.unit_vectors(M, comps, cols)
    W = BF.boot_W(len(cols), 20261128)
    e = A.estimands(u["v"], M["counts_ref"][cols][:, :2], M["counts_out"][cols][:, :2], W)
    assert np.allclose(A.interval(e["draws"]["rho_head"]), res["H-L2"]["rho_head_95"])
    assert np.allclose(A.interval(e["draws"]["kappa_head"]), res["H-L1"]["kappa_head_95"])
    assert res["half_B_images"] == len(half_b) and A.SEED_WB == 20261128 and BF.B == 10_000


# ------------------------------------------------------------------------------------------------ checks: rules
@check
def hl1_boundaries():
    assert A.hl1_label([-1.0, -1e-12], [-2.0, -1.0]) == "TAIL-WEIGHTED"
    assert A.hl1_label([-1.0, 0.0], [0.0, 1.0]) == "PROPORTIONAL"
    assert A.hl1_label([0.5, 1.0], [1e-12, 0.5]) == "HEAD-WEIGHTED"
    assert A.hl1_label([-0.1, 0.2], [-0.2, 0.1]) == "PROPORTIONAL"


@check
def hl2_boundaries():
    assert A.hl2_label([0.5000001, 0.9]) == "PRACTICAL"
    assert A.hl2_label([0.5, 0.9]) == "INCONCLUSIVE"
    assert A.hl2_label([0.1, 0.4999999]) == "NOT PRACTICAL"
    assert A.hl2_label([0.1, 0.5]) == "INCONCLUSIVE"


@check
def floors_order_and_boundaries():
    s = {"abs_shift": 1.0, "abs_Dr": 100.0}
    try:
        assert A.floors(s, [0.2, 0.9], 0) is None  # exactly 0.01 and exactly 0.20 pass
    except KeyError as e:
        raise AssertionError("floors read a key other than the floor sums") from e
    assert "(iv)" in (A.floors({"abs_shift": 0.999, "abs_Dr": 100.0}, [0.1, 0.9], 0) or "")  # (iv) before (v)
    assert "(v)" in (A.floors(s, [0.1999, 0.9], 0) or "")
    assert "zero denominator" in (A.floors(s, [0.3, 0.9], 2) or "")
    assert A.SHIFT_FLOOR == 0.01 and A.RHO_ALL_FLOOR == 0.20 and A.PRACTICAL == 0.50 and A.MIN_TYPES in (3, 30)


@check
def result_record_end_to_end():
    r = stages()
    res = r["result"]
    for k in ("H-L1", "H-L2", "DESCRIPTIVE", "floor", "units"):
        assert k in res
    assert res["units"] == 18 * A.EXPECT_D
    lab1, lab2 = res["H-L1"]["label"], res["H-L2"]["label"]
    if res["floor"]:
        assert lab1 == lab2 == res["floor"]
    else:
        assert lab1 == A.hl1_label(res["H-L1"]["d_lo_95"], res["H-L1"]["d_hi_95"])
        assert lab2 == A.hl2_label(res["H-L2"]["rho_head_95"])
    fr = res["DESCRIPTIVE"]["fragile_over_G_w"]
    assert set(fr) == {"raw", "pinned_head"} and fr["raw"]["comparisons"] == A.EXPECT_D


@check
def no_text_in_outputs():
    r = stages()
    for f in ("S1B.json", "G0_ALT.json", "RESULT_ALT.json"):
        s = (r["out"] / f).read_text(encoding="utf-8")
        assert MARK not in s and "zmo" not in s, f
    cz = (r["out"] / "CENSUS_ALT.json").read_text(encoding="utf-8")
    assert MARK not in cz and "zmo" not in cz  # word-type keys only, never a caption


# ------------------------------------------------------------------------------------------------ checks: CPU guard
def _guard(limit, code, timeout=60):
    t0 = time.time()
    r = subprocess.run([sys.executable, "-I", "-B", str(HERE / "cpu_guard.py"), str(limit), "--",
                        sys.executable, "-I", "-c", code], capture_output=True, text=True, timeout=timeout)
    return r.returncode, time.time() - t0


@check
def cpu_guard_kills_tree():
    burn = "import time\nt=time.process_time()\nwhile time.process_time()-t<30: pass"
    rc, dt = _guard(1.5, burn)
    assert rc == 7 and dt < 15, (rc, dt)
    child = ("import subprocess,sys\nsubprocess.run([sys.executable,'-I','-c',"
             f"{burn!r}])")
    rc, dt = _guard(1.5, child)
    assert rc == 7 and dt < 15, (rc, dt)  # a grandchild's CPU counts
    seq = ("import subprocess,sys\nfor _ in range(25): subprocess.run([sys.executable,'-I','-c',"
           "'import time\\nt=time.process_time()\\nwhile time.process_time()-t<0.4: pass'])")
    rc, dt = _guard(1.5, seq)
    assert rc == 7 and dt < 15, (rc, dt)  # CPU of reaped grandchildren counts (cutime)
    rc, _dt = _guard(30, "import sys; sys.exit(4)")
    assert rc == 4


@check
def run_stage_refuses_d1_records():
    r = subprocess.run(["bash", str(HERE / "run_stage.sh"), "s0", "/nonexistent/b_d1_records", "-", "-"],
                       capture_output=True, text=True, timeout=60)
    assert r.returncode == 6 and "REFUSED" in r.stdout


@check
def changed_needs_significance_under_f0():
    """CHANGED counts a comparison only when it is significant under f0 (paper §4.3). With every difference 0 (f0 not
    significant) and a certify stub that reports a certificate, the count must stay 0: the line guards the s0 != 0
    condition itself, not only through what certify returns."""
    M = mk_M(lambda m, j: 0.0)
    M["cider"][:] = 50.0
    cols = np.arange(M["cider"].shape[2])
    W = BF.boot_W(len(cols), 20261128)
    old = BF.certify
    try:
        BF.certify = lambda c, G, metric="cider": {"certified": 1, "fragile": False}
        fr = A.fragile_rows(M, COMPS4, cols, W)
    finally:
        BF.certify = old
    assert fr["raw"]["changed"] == 0 and fr["pinned_head"]["changed"] == 0, fr


# ------------------------------------------------------------------------------------------------ CC-512 W3 checks
@check
def registered_literals():
    """The registered values as literals (CC-512 W3), read as the module had them at import."""
    a = AT_IMPORT
    assert (a["HALF"], a["EXPECT_D"], a["EXPECT_IMAGES"], a["EXPECT_FILES"]) == (279, 1101, 558, 75)
    assert (a["SEED_SPLIT"], a["SEED_WB"]) == (20261127, 20261128)
    assert a["COVER_NUM"] * 5 == 4 * a["COVER_DEN"] and (a["COVER_NUM"], a["COVER_DEN"]) == (4, 5)  # 0.80
    assert (a["MIN_TYPES"], a["UNALIGNED_MAX"], a["SHIFT_FLOOR"], a["RHO_ALL_FLOOR"], a["PRACTICAL"], a["G0_TOL"]) == \
        (30, 0.005, 0.01, 0.20, 0.50, 1e-6)
    assert a["REG"] == "manuscript/prereg/2026-11-27_b_alt/PREREG_DRAFT_B_ALT_v2.md"
    assert a["REG_SHA"] == "ed05acdb7682b516738b00d2741fd87d0220e30eec9aa38ae5a2a92c3014f352"
    assert a["ERRATA"] == {"manuscript/prereg/2026-11-27_b_alt/ERRATUM_B_ALT_1.md":
                           "8367faceffbd2235d2c4cfe2a0b768c37e0e1d357140a995db5359c9a884958f"}
    assert A.interval(np.arange(1001.0)) == [25.0, 975.0]  # the 2.5th and 97.5th percentiles


@check
def registration_and_erratum_checked():
    A.reg_check()
    for attr, val in (("REG_SHA", "0" * 64), ("ERRATA", {next(iter(A.ERRATA)): "0" * 64})):
        old = getattr(A, attr)
        setattr(A, attr, val)
        try:
            A.reg_check()
        except BF.Fault:
            pass
        else:
            raise AssertionError(f"reg_check passed with {attr} off its sha")
        finally:
            setattr(A, attr, old)


@check
def pin_overlapping_types():
    d = {("za", "zb"): (False,), ("zb", "zc"): (False,)}
    assert A.pin(["za", "zb", "zc"], d, 2)[0] == ["za_zb", "zc"]  # after a match the scan resumes after it


@check
def pinned_member_uses_its_own_list():
    tk = A.PinTok(STUB, {"h": {}, "a": {("zba", "zbe"): (False,)}})
    assert tk.tokens("zba zbe", ("pyvi", "tw", "pk", "cf", "a")) == ["zba_zbe"]
    assert tk.tokens("zba zbe", ("pyvi", "tw", "pk", "cf", "h")) == ["zba", "zbe"]


@check
def references_are_pinned():
    w = world()
    d = {("zba", "zbe"): (False,)}
    tk = A.PinTok(STUB, {"h": d, "a": d})
    per = A.per_cider(tk, w["refs"], w["ids"], {})
    m = ("rdr", "tw", "pk", "cf")
    want = FM.key(["\t".join(tk.side(r, "matched", m + ("h",), True) for r in w["refs"][i]) for i in w["ids"]])
    assert per(m + ("h",))["_refs"] == want != per(m)["_refs"]  # the zqq context changes reference tokens


@check
def disagreement_counts_literal():
    tk = FM.Tok(STUB)
    head, alltypes = {("zba", "zbe")}, {("zba", "zbe"), ("zca", "zce")}
    got = A.count_disagreements(tk, ["zba zbe zca zce", "zca zce zha zhe", "zmo"], head, alltypes)
    assert got == [1, 3, 1, 0], got  # [n_head, n_all, n_other, unaligned]


@check
def band_uses_min_and_max():
    M = mk_M(shift_world(1.0, 1.0, 2.0))
    cols = np.arange(M["cider"].shape[2])
    u = A.unit_vectors(M, COMPS4, cols)
    rng = np.random.default_rng(9)
    na = rng.integers(5, 15, len(cols))
    cr = np.stack([np.minimum(na, rng.integers(1, 6, len(cols))), na], 1)  # c_ref around 0.3
    co = np.stack([np.minimum(na, rng.integers(8, 15, len(cols))), na], 1)  # c_out around 0.9
    W = BF.boot_W(len(cols), 20261128)
    d = A.estimands(u["v"], cr, co, W)["draws"]
    assert np.all(d["c_ref"] < d["c_out"])
    assert np.allclose(d["d_lo"], d["kappa_head"] - d["c_ref"]) and np.allclose(d["d_hi"], d["kappa_head"] - d["c_out"])


@check
def floor_iv_reads_shift_not_pin_move():
    s = {"abs_shift": 1.0, "abs_Dr": 100.0, "abs_pin_move_h": 1000.0, "abs_pin_move_a": 1000.0}
    assert A.floors(s, [0.5, 0.9], 0) is None


def _s2_copy(**patch):
    """s2 alone on a copy of the stage outputs (same census, matrix and G0 bytes), with module values patched."""
    w, r = world(), stages()
    tmp = Path(tempfile.mkdtemp(dir=w["root"]))
    for f in ("CENSUS_ALT.json", "PER_IMAGE_ALT.npz", "G0_ALT.json"):
        shutil.copy(r["out"] / f, tmp)
    old = {k: getattr(A, k) for k in patch}
    try:
        for k, v in patch.items():
            setattr(A, k, v)
        rc, so = run_main(["s2", "--work", str(w["work"]), "--out", str(tmp), "--census-sha", r["census"],
                           "--npz-sha", r["npz"], "--g0-sha", r["g0sha"]])
    finally:
        for k, v in old.items():
            setattr(A, k, v)
    assert rc == 0, so
    return A.jload(tmp / "RESULT_ALT.json")


@check
def tripped_floor_replaces_both_labels():
    res = _s2_copy(SHIFT_FLOOR=1e9)
    assert res["floor"].startswith("NOT_EVALUABLE (iv)")
    assert res["H-L1"]["label"] == res["H-L2"]["label"] == res["floor"]
    res = _s2_copy(RHO_ALL_FLOOR=1e9)
    assert res["floor"].startswith("NOT_EVALUABLE (v)")
    assert res["H-L1"]["label"] == res["H-L2"]["label"] == res["floor"]


@check
def coverage_from_the_right_counts():
    r = stages()
    res = r["result"]["DESCRIPTIVE"]
    with np.load(r["out"] / "PER_IMAGE_ALT.npz", allow_pickle=False) as z:
        ids, cref, cout = [str(i) for i in z["ids"]], z["counts_ref"], z["counts_out"]
    _a, half_b = A.split(ids)
    cols = [ids.index(i) for i in half_b]
    want_r = cref[cols, 0].sum() / cref[cols, 1].sum()
    want_o = cout[cols, 0].sum() / cout[cols, 1].sum()
    assert abs(want_r - want_o) > 1e-6  # the world tells the two apart
    assert abs(res["c_ref_B"] - want_r) < 1e-12 and abs(res["c_out_B"] - want_o) < 1e-12


@check
def g0_failure_exits_3():
    w, r = world(), stages()
    work = Path(tempfile.mkdtemp(dir=w["root"]))
    for f in ("FAMILY.json", "CENSUS.json", "SYSTEMS.tsv"):
        shutil.copy(w["work"] / f, work)
    dev = A.jload(w["work"] / "DEV.json")
    cl = next(c for c in dev["comparisons"][0]["classes"].values() if BF.F0N in c["members"])  # a G_w class
    cl["cider"][0] += 1.0
    (work / "DEV.json").write_text(json.dumps(dev), encoding="utf-8")
    out = Path(tempfile.mkdtemp(dir=w["root"]))
    shutil.copy(r["out"] / "PER_IMAGE_ALT.npz", out)
    old = A.INPUT_SHA["DEV.json"]
    try:
        A.INPUT_SHA["DEV.json"] = A.sha_file(work / "DEV.json")
        rc, so = run_main(["g0", "--work", str(work), "--out", str(out), "--npz-sha", r["npz"]])
    finally:
        A.INPUT_SHA["DEV.json"] = old
    assert rc == 3 and "FAULT" in so, (rc, so)


@check
def outputs_read_only():
    r = stages()
    for f in ("CENSUS_ALT.json", "PER_IMAGE_ALT.npz", "S1B.json", "G0_ALT.json", "RESULT_ALT.json"):
        assert (os.stat(r["out"] / f).st_mode & 0o777) == 0o444, f


@check
def t_split_by_tone_level():
    M = mk_M(lambda m, j: (j + 1.0) if m.startswith("pyvi") and ".tw." in m and not m.endswith("+Pa") else 0.0)
    cols = np.arange(M["cider"].shape[2])
    v = A.unit_vectors(M, COMPS4, cols)["v"]
    assert np.abs(v["A_tw"]).sum() > 1 and np.allclose(v["A_tmf"], 0)  # only tw pairs carry a shift
    assert np.allclose(v["A"], v["A_tw"])


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
