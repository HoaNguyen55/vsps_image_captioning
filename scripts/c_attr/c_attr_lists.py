#!/usr/bin/env python3
"""C-ATTR-DEV block 0 (CPU, laptop): the list file and the K0 / refill report. Registration
manuscript/prereg/2026-11-11_c_attr_dev/C_ATTR_DEV_PREREG_v1_1.md §2, §2.1, §6.2 steps 0.1-0.2, §7.9, §11.1 (CC-331).
Label: DEVELOPMENT / C-ATTR-DEV, NON-CONFIRMATORY.

  python -I -B scripts/c_attr/c_attr_lists.py --selftest
  python -I -B scripts/c_attr/c_attr_lists.py build --m3 M3_ROOT --m1 M1_ROOT --report REPORT.json

M3_ROOT / M1_ROOT stand for /root of the host that wrote each stored input (the laptop's read-only backup copies);
every input is checked against scripts/c_attr/STORED_SHA256 first. Rules reused unchanged from c_attr.py (= c_t2.py):
eligible (C's near cut 0.92, ties by cluster id), rand_draw (draw 0 = C's rule). New: perm (Sattolo cycle, §2.1),
fix f1-f4 (seed suffix f<j>), the swap subsamples (§7.9). Gate K0: ret, rand draw 0 and fix f0 must equal the stored
lists on OV-dev-A (911), OV-dev-B (925) and XM-dev500 (500); a mismatch writes the report and no list file (rc 1).
The list file holds image and cluster ids only; the report holds counts, shares and ids only. No caption is read.
"""
from __future__ import annotations

import argparse
import json
import random
import sys
from pathlib import Path

import numpy as np

sys.path.insert(0, str(Path(__file__).resolve().parent))
import c_attr as A  # noqa: E402  (imports C's pinned modules unchanged)

BM, C, sha = A.BM, A.C, A.sha
N_EX, NEAR = BM.N_EX, BM.NEAR_COS
REG_SHA256 = "44f81329d418efef823d466a4dca5fc9943817322cb3eef0afec7318c9d7681a"  # registration v1.1
STORED = A.ATTR / "STORED_SHA256"
SWAP_N, SWAPS = 28000, (0, 1)
RANK_KEEP = 512  # eligible ranking kept per image for the perm refill (ponytail: a refill beyond it is a STOP)
REFILL_GATE = 0.10  # §2.1 gate, K0b
#: set -> (query vectors, memory vectors, stored lists or None, rand draws, fix indices); paths as on the host
SRC = {"ov_dev_a": ("c_stage1/emb.npz", "c_stage1/emb.npz", "c_stage1/exemplars.json", (0,), (0,)),
       "ov_dev_b": ("c_stage2/emb_ov_dev_b.npz", "c_stage1/emb.npz", "c_stage2/ex_ov_dev_b.json", (0, 1, 2), A.FIXES),
       "xm_dev500": ("c_stage2/emb_xm_dev500.npz", "c_stage1/emb.npz", "c_stage2/ex_xm_dev500.json", (0, 1, 2), A.FIXES),
       "f30k_val": ("c_t2/out/emb_f30k_val.npz", "c_en/cen_memory_emb.npz", "c_t2/out/x1_f30k_val_coco.json", (0, 1, 2),
                    ())}
K0_SETS = ("ov_dev_a", "ov_dev_b", "xm_dev500")
HOST_OF = {"c_stage1": "m3", "c_stage2": "m3", "c_t2": "m1", "c_en": "m1"}


# ------------------------------------------------------------------------------------------------ rules
def sattolo(ds: str, p: int, n: int) -> list[int]:
    """§2.1: pi_p as an array, pi(q) = a[q]; one n-cycle, no fixed point; depends on (set, p) only."""
    rng, a = random.Random(BM.seed("perm", ds, f"p{p}")), list(range(n))
    for i in range(n - 1, 0, -1):
        j = rng.randrange(i)
        a[i], a[j] = a[j], a[i]
    return a


def perm_list(donor_rank: list[int], row_q: np.ndarray) -> tuple[list[int], int]:
    """The first N_EX clusters of the donor's eligible ranking at cosine < NEAR to q; refills = those taken from
    beyond the donor's own first N_EX."""
    keep = [c for c in donor_rank[:N_EX] if row_q[c] < NEAR]
    refill = [c for c in donor_rank[N_EX:] if row_q[c] < NEAR][:N_EX - len(keep)]
    if len(keep) + len(refill) < N_EX:
        raise SystemExit("perm: the kept donor ranking is too short to refill (raise RANK_KEEP)")
    return keep + refill, len(refill)


def fix_seed(ds: str, j: int) -> int:
    return BM.seed("fix", ds) if j == 0 else BM.seed("fix", ds, f"f{j}")


def build_set(ds: str, mk: list[str], mv: np.ndarray, qids: list[str], qv: np.ndarray, draws, fixes) -> tuple[dict, dict]:
    """(ids-only lists, diagnostics) of one set; rows of qv are in manifest order."""
    cos = qv @ mv.T
    ranks, out = [], {"ids": qids, "ret": {}, "rand": {str(d): {} for d in draws}, "perm": {}, "donor": {}, "fix": {}}
    for qid, row in zip(qids, cos):
        ok = A.eligible(row, mk)
        ranks.append([int(j) for j in ok[:RANK_KEEP]])
        out["ret"][qid] = [mk[j] for j in ok[:N_EX]]
        names = [mk[j] for j in ok]
        for d in draws:
            out["rand"][str(d)][qid] = A.rand_draw(ds, qid, names, d)
    safe = sorted(mk[j] for j in np.flatnonzero(cos.max(0) < NEAR))
    for j in fixes:
        out["fix"][str(j)] = random.Random(fix_seed(ds, j)).sample(safe, N_EX)
    col = {c: n for n, c in enumerate(mk)}
    diag, pis = {}, {}
    for p in A.PERMS:
        pis[p] = pi = sattolo(ds, p, len(qids))
        out["perm"][str(p)], out["donor"][str(p)], refills = {}, {}, 0
        for n, qid in enumerate(qids):
            lst, r = perm_list(ranks[pi[n]], cos[n])
            out["perm"][str(p)][qid], out["donor"][str(p)][qid] = [mk[j] for j in lst], qids[pi[n]]
            refills += r
        share = refills / (N_EX * len(qids))
        d = {"refill_share_8": round(share, 6), "refill_gate": "perm is a diagnostic on this set (K0b)"
             if share > REFILL_GATE else "pass"}
        for k in (4, 8):
            d[f"overlap_with_ret_{k}"] = round(float(np.mean(
                [len(set(out["perm"][str(p)][q][:k]) & set(out["ret"][q][:k])) / k for q in qids])), 6)
            for arm, lists in (("ret", out["ret"]), ("perm", out["perm"][str(p)]), ("rand_d0", out["rand"]["0"])):
                d[f"mean_cos_{arm}_{k}"] = round(float(np.mean(
                    [cos[n, [col[c] for c in lists[q][:k]]].mean() for n, q in enumerate(qids)])), 6)
        diag[f"p{p}"] = d
    diag["same_donor_p1_p2"] = int(sum(a == b for a, b in zip(pis[1], pis[2])))
    return out, diag


def k0(ds: str, built: dict, stored: dict, draws=(0,)) -> dict:
    """K0 / stored parity: counts and failing ids only. stored: C's exemplar file (ex[arm][set]) or C-T2's x1 file."""
    st = {k: stored[k][ds] for k in ("ret", "rand", "fix")} if ds in stored.get("ret", {}) else \
        {"ret": stored["ret"], "rand": stored["rand"]}
    nested = "fix" in st
    rep = {"n": len(built["ids"])}
    bad = [q for q in built["ids"] if built["ret"][q] != [c for c, _x in st["ret"][q]]]
    rep["ret_equal"], rep["ret_failing_ids"] = rep["n"] - len(bad), bad[:10]
    for d in draws:
        ref = st["rand"] if nested else st["rand"][str(d)]
        bad = [q for q in built["ids"] if built["rand"][str(d)][q] != ref[q]]
        rep[f"rand_d{d}_equal"], rep[f"rand_d{d}_failing_ids"] = rep["n"] - len(bad), bad[:10]
    if nested:
        rep["fix_f0_equal"] = built["fix"]["0"] == st["fix"]
    rep["pass"] = all(rep[k] == rep["n"] for k in rep if k.endswith("_equal") and k != "fix_f0_equal") and \
        rep.get("fix_f0_equal", True)
    return rep


# ------------------------------------------------------------------------------------------------ build (laptop)
def pinned_inputs() -> dict[str, str]:
    return {ln.split()[1]: ln.split()[0] for ln in STORED.read_text().splitlines() if ln.strip()}


def resolve(rel: str, roots: dict[str, Path], pins: dict[str, str]) -> Path:
    host = "/root/outputs/" + rel
    p = roots[HOST_OF[rel.split("/")[0]]] / "outputs" / rel
    if pins.get(host) is None or sha(p) != pins[host]:
        raise SystemExit(f"{p}: not the pinned {host}")
    return p


def vectors(z, prefix: str | None) -> tuple[list[str], np.ndarray]:
    keys = [str(k) for k in z["keys"]]
    idx = [n for n, k in enumerate(keys) if ("|" not in k if prefix is None else k.startswith(prefix + "|"))]
    return [keys[n] if prefix is None else keys[n].split("|", 1)[1] for n in idx], \
        np.asarray(z["vecs"], np.float32)[idx]


def manifest_ids(ds: str) -> list[str]:
    if ds == "f30k_val":
        return A.f30k_names("val", A.load_lists())
    cl = A.ROOT / "manuscript/prereg/2026-10-22_c_stage1/lists.json"
    return [i for i, _f, _h in A.items_of(ds, argparse.Namespace(c_lists=cl))]  # with C's refusal checks


def cmd_build(a) -> None:
    roots, pins = {"m3": Path(a.m3), "m1": Path(a.m1)}, pinned_inputs()
    rec = {"schema": "vsps.c_attr_lists.v1", "label": A.LABEL, "registration_sha256": REG_SHA256, "near_cos": NEAR,
           "n_ex": N_EX, "inputs": {}, "sets": {}, "swap": {}}
    report = {"label": A.LABEL, "k0": {}, "parity_beside": {}, "diagnostics": {}}
    mem = {}
    for ds, (qrel, mrel, srel, draws, fixes) in SRC.items():
        for rel in (qrel, mrel, srel):
            rec["inputs"]["/root/outputs/" + rel] = pins["/root/outputs/" + rel]
        if mrel not in mem:
            mem[mrel] = vectors(np.load(resolve(mrel, roots, pins)), None)
        mk, mv = mem[mrel]
        qk, qv = vectors(np.load(resolve(qrel, roots, pins)), ds)
        ids = manifest_ids(ds)
        if sorted(qk) != sorted(ids) or len(ids) != len(set(ids)):
            raise SystemExit(f"{ds}: the query vectors are not the {len(ids)} manifest images")
        pos = {q: n for n, q in enumerate(qk)}
        built, diag = build_set(ds, mk, mv, ids, qv[[pos[q] for q in ids]], draws, fixes)
        stored = json.loads(resolve(srel, roots, pins).read_text(encoding="utf-8"))
        (report["k0"] if ds in K0_SETS else report["parity_beside"])[ds] = k0(
            ds, built, stored, (0,) if ds in K0_SETS else draws)
        report["diagnostics"][ds] = diag
        rec["sets"][ds] = built
        print(json.dumps({ds: {k: v for k, v in (report["k0"].get(ds) or report["parity_beside"][ds]).items()
                               if not k.endswith("failing_ids")}}), flush=True)
        if ds == "f30k_val":
            if len(mk) != 111927:
                raise SystemExit(f"COCO memory: {len(mk)} clusters, not 111,927")
            for j in SWAPS:
                rec["swap"][f"s{j}"] = random.Random(BM.seed("swap", "coco", f"s{j}")).sample(sorted(mk), SWAP_N)
    report["K0"] = "PASS" if all(r["pass"] for r in report["k0"].values()) else "FAIL"
    Path(a.report).write_text(json.dumps(report, indent=1) + "\n", encoding="utf-8")
    print(f"K0 {report['K0']}; report {a.report} sha256 {sha(a.report)}")
    if report["K0"] != "PASS":
        raise SystemExit("K0 FAIL: no list file written (STOP, no rental)")
    out = Path(a.out)
    out.write_text(json.dumps(rec, separators=(",", ":")) + "\n", encoding="utf-8")
    Path(str(out) + ".sha256").write_text(f"{sha(out)}  {out.name}\n")
    print(f"list file {out} sha256 {sha(out)}")


# ------------------------------------------------------------------------------------------------ self-test
SEED_TOY = 7


def selftest() -> None:
    ok = []
    for n in list(range(2, 41)) + [911]:  # one n-cycle; equals the spec written out again here
        for p in A.PERMS:
            a = sattolo("toy", p, n)
            seen, q = set(), 0
            while q not in seen:
                seen.add(q)
                q = a[q]
            assert len(seen) == n and all(a[i] != i for i in range(n)), (n, p)
            rng, g = random.Random(BM.seed("perm", "toy", f"p{p}")), list(range(n))
            for i in range(n - 1, 0, -1):
                j = rng.randrange(i)
                g[i], g[j] = g[j], g[i]
            assert a == g and a == sattolo("toy", p, n)
    assert sattolo("toy", 1, 30) != sattolo("toy", 2, 30) != sattolo("other", 2, 30)
    ok.append("Sattolo: one n-cycle, no fixed point, (set, p) only")
    rng = np.random.default_rng(SEED_TOY)  # toy: 12 clusters, 6 images; images 0-2 copy clusters 0-2 (cut for them)
    mv = rng.normal(size=(15, 6)).astype(np.float32)
    mv /= np.linalg.norm(mv, axis=1, keepdims=True)
    qv, mv = np.concatenate([mv[:3], mv[12:]]), mv[:12]
    mk, qids, ds = [f"m{n:02d}" for n in range(12)], [f"q{n}" for n in range(6)], "ov_dev_b"
    built, diag = build_set(ds, mk, mv, qids, qv, (0, 1, 2), A.FIXES)
    ref = BM.exemplars(mk + [f"{ds}|{q}" for q in qids], np.concatenate([mv, qv]))
    cos, filt, refills = qv @ mv.T, 0, 0
    for n, q in enumerate(qids):
        assert built["ret"][q] == [c for c, _x in ref["ret"][ds][q]] and built["rand"]["0"][q] == ref["rand"][ds][q]
        for p in A.PERMS:
            donor = qids.index(built["donor"][str(p)][q])
            assert donor != n, "no image is its own donor"
            lst = built["perm"][str(p)][q]
            assert all(cos[n, mk.index(c)] < NEAR for c in lst), "no shown cluster at cosine >= 0.92 to q"
            dl = [mk[j] for j in A.eligible(cos[donor], mk)]
            assert lst == [c for c in dl if cos[n, mk.index(c)] < NEAR][:N_EX], "first 8 of the donor's list"
            r = N_EX - sum(cos[n, mk.index(c)] < NEAR for c in dl[:N_EX])
            filt += r > 0
            refills += r
    assert filt and abs(diag["p1"]["refill_share_8"] + diag["p2"]["refill_share_8"] - refills / (N_EX * 6)) < 1e-5, \
        "refills counted correctly (and the toy exercises the filter)"
    assert built["fix"]["0"] == ref["fix"][ds], "f0 = C's stored rule"
    safe = sorted(mk[j] for j in np.flatnonzero(cos.max(0) < NEAR))
    for j in (1, 2, 3, 4):
        assert built["fix"][str(j)] == random.Random(BM.seed("fix", ds, f"f{j}")).sample(safe, N_EX) != built["fix"]["0"]
    ok.append("toy (12 clusters, 6 images): donor, near cut on q, refill count, ret / rand d0 / f0 = C's rule, f1-f4")
    st = {"ret": {ds: ref["ret"][ds]}, "rand": {ds: ref["rand"][ds]}, "fix": {ds: ref["fix"][ds]}}
    assert k0(ds, built, st)["pass"]
    st["rand"][ds] = {**ref["rand"][ds], "q3": list(reversed(ref["rand"][ds]["q3"]))}
    r = k0(ds, built, st)
    assert not r["pass"] and r["rand_d0_failing_ids"] == ["q3"] and r["rand_d0_equal"] == 5
    ok.append("K0 comparator (counts and failing ids)")
    pins = pinned_inputs()
    for ds, (qrel, mrel, srel, _d, _f) in SRC.items():
        assert all(("/root/outputs/" + x) in pins for x in (qrel, mrel, srel)), ds
    assert len(manifest_ids("ov_dev_a")) == 911 and len(manifest_ids("xm_dev500")) == 500
    ok.append("inputs pinned in STORED_SHA256; manifests 911 / 500")
    print("c_attr_lists selftest ok: " + "; ".join(ok))


def main() -> None:
    ap = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    ap.add_argument("--selftest", action="store_true")
    sub = ap.add_subparsers(dest="cmd")
    p = sub.add_parser("build")
    p.add_argument("--m3", type=Path, required=True, help="stands for M3's /root (c_stage1, c_stage2)")
    p.add_argument("--m1", type=Path, required=True, help="stands for M1's /root (c_t2, c_en)")
    p.add_argument("--report", type=Path, required=True)
    p.add_argument("--out", type=Path, default=A.ATTR_LISTS)
    a = ap.parse_args()
    if a.selftest:
        return selftest()
    if a.cmd == "build":
        if A.gpu_host():
            raise SystemExit("the list file is built on the laptop only")
        return cmd_build(a)
    ap.print_help()


if __name__ == "__main__":
    main()
