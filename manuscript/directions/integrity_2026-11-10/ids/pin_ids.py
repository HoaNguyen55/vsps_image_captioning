#!/usr/bin/env python3
"""Id dumps for POSTHOC_ROWS_PLAN_v1_1 (PIN-C, PIN-C2, PIN-K): ids, ranks, similarities and counts only.

The pair rule is never re-written here. Each CC-199 check script is sha-checked and executed unchanged (its stdout is
kept beside the pins), and the flags come from its own functions: xtab3.pairhit (PIN-C, PIN-C2) and xtab2.pair plus
the `sim > 0.75` clause of xtab2.py:33 (PIN-K). `clause()` below only annotates a pair pairhit already flagged.

    python -I -B pin_ids.py c     OpenViIC test, examples each backbone was shown (ret and rand)
    python -I -B pin_ids.py k     KTVIC test and dev300 against KTVIC train
    python -I -B pin_ids.py c2    XM-test2500, COCO Karpathy test, NoCaps val (same rule, same shown-example definition)

Every output is created once (mode "x"); a second run refuses instead of changing a pin."""
import contextlib
import hashlib
import io
import json
import sys
from pathlib import Path

import numpy as np

R = Path("/mnt/d/vsps_image_captioning")
CK = R / ".session_backup/2026-10-31/rulings/CC-199_checks"
OUT = Path(__file__).resolve().parent
SHA = {"xtab.py": "65eba96d70ff65ba6514672a7f17046b0a5e15db238ac17ad440ce615746e58c",
       "xtab2.py": "8c2da7e991e4c45d0ae3fc67550bb5964b5d082039b8b1501ffe69e0f03f2b70",
       "xtab3.py": "21979bf512483f1e4a4d102867bd07e4d9a8dd27005a5366c15f9261640bc068"}
K = {"qwen25vl_7b": 8, "internvl3_8b": 4}  # frozen k per backbone = the run names (ret-k8-first-T1, ret-k4-last-T2)
RULE = "(min(pHash, dHash) <= 10 and SSCD >= 0.5) or SSCD > 0.75 or identical sha256  [xtab3.py:27]"
M3 = R / ".session_backup/machines/M3/root/outputs/c_test"
M1 = R / ".session_backup/machines/M1/root/outputs/c_en"
FE = Path.home() / "c_pvr_w25_in"
FEATS = ("phash", "dhash", "phash_m", "dhash_m", "sscd")


def sha(p) -> str:
    return hashlib.sha256(Path(p).read_bytes()).hexdigest()


def put(name: str, text: str) -> None:
    with open(OUT / name, "x", encoding="utf-8") as f:
        f.write(text)


def run(name: str) -> tuple[dict, str]:
    """Execute one CC-199 check unchanged; keep its stdout; return its namespace."""
    p = CK / name
    assert sha(p) == SHA[name], f"{name}: not the CC-199 file"
    ns, buf = {"__name__": name[:-3]}, io.StringIO()
    with contextlib.redirect_stdout(buf):
        exec(compile(p.read_text(encoding="utf-8"), str(p), "exec"), ns)
    kept = OUT / f"{name[:-3]}_stdout.txt"
    if kept.exists():  # a later mode re-running the same check must get the pinned output again
        assert kept.read_text(encoding="utf-8") == buf.getvalue(), f"{name}: output differs from the pinned one"
    else:
        put(kept.name, buf.getvalue())
    return ns, buf.getvalue()


def load(p: Path) -> dict:
    z = np.load(p)
    return {"ids": [str(i) for i in z["ids"].tolist()], "sha": z["sha"].tolist(), **{k: z[k] for k in FEATS}}


def clause(ns: dict, q: int, keys: list[str]) -> tuple[str, int]:
    """Annotation only: which clauses hold for this cluster, and its smallest hash distance."""
    BM, pool, ov = ns["BM"], ns["pool"], ns["ov"]
    idx = [ns["pi"][k] for k in keys]
    s = np.nan_to_num(pool["sscd"][idx]) @ np.nan_to_num(ov["sscd"][q])
    h = np.min([BM.MO.hamming(pool[a][idx], ov[b][q:q + 1])[:, 0] for a, b in (
        ("phash", "phash"), ("phash_m", "phash"), ("dhash", "dhash"), ("dhash_m", "dhash"))], axis=0)
    c = {"C1": any(pool["sha"][i] == ov["sha"][q] for i in idx),
         "C2": bool(((h <= BM.HASH_MAX) & (s >= BM.SSCD_MIN)).any()), "C3": bool((s > 0.75).any())}
    assert any(c.values()), "annotation disagrees with pairhit"
    return "+".join(k for k, v in c.items() if v), int(h.min())


def flag(ns: dict, ex: dict, ds: str, qi: dict, mem: dict, scored: list[str], inputs: dict) -> dict:
    """Per arm and backbone: the scored queries with a near-copy among the k examples that backbone was shown.
    Rank = position in the stored list (retrieval rank for ret); InternVL3's order `last` reverses only the prompt
    position (decode_icl.py:185-188 takes list[:k] for both arms)."""
    ns["miss"], sc, hits = 0, set(scored), {}
    for arm in ("ret", "rand"):
        hits[arm] = {}
        for q, cids in ex[arm][ds].items():
            cl = [c[0] if isinstance(c, list) else c for c in cids]
            assert len(cl) == 8
            h = [[r + 1, c, float(s), *clause(ns, qi[q], mem[c])] for r, c in enumerate(cl)
                 for ok, s in [ns["pairhit"](qi[q], mem[c])] if ok]
            if h:
                hits[arm][q] = h
    assert ns["miss"] == 0, "a memory image has no features"
    arms = {}
    for arm, hs in hits.items():
        per = {m: sorted(q for q, h in hs.items() if q in sc and h[0][0] <= k) for m, k in K.items()}
        arms[arm] = {m: {"k": K[m], "n_flagged": len(v), "n_first_hit_rank1": sum(hs[q][0][0] == 1 for q in v),
                         "ids": v} for m, v in per.items()}
        arms[arm]["union"] = {"n_flagged": len(set().union(*per.values())), "ids": sorted(set().union(*per.values()))}
        arms[arm]["flagged_outside_scored_set"] = sorted(q for q in hs if q not in sc)
    return {"set": ds, "n_queries_in_exemplar_file": len(ex["ret"][ds]), "n_scored": len(scored), "rule": RULE,
            "arms": arms, "hits_rank_cluster_sscd_clause_minhash": {a: {q: [[r, c, round(s, 4), cl, hd] for
                                                                       r, c, s, cl, hd in h] for q, h in hs.items()}
                                                                 for a, hs in hits.items()},
            "inputs_sha256": inputs}


def write_set(name: str, rec: dict) -> None:
    put(f"{name}.json", json.dumps(rec, indent=1) + "\n")
    for m in (*K, "union"):
        put(f"{name}_ret_{m}.txt", "".join(i + "\n" for i in rec["arms"]["ret"][m]["ids"]))
    print(name, {a: {m: (v["n_flagged"], v.get("n_first_hit_rank1")) for m, v in x.items() if isinstance(v, dict)}
                 for a, x in rec["arms"].items()})


def pin_c() -> dict:
    ns, _ = run("xtab3.py")
    ex, prim = ns["ex"], ns["prim"]
    qi = {q: ns["oi"][q.split(".")[0]] for q in ex["ret"]["ov_test"]}
    order = (R / "manuscript/prereg/2026-10-25_c_test/ov_test_primary1941.txt").read_text().split()
    assert set(order) == prim and len(order) == 1941
    W = Path(ns["W"])
    rec = flag(ns, ex, "ov_test", qi, ns["mem"], order, {
        "pool.npz": sha(W / "pool.npz"), "openviic_test.npz": sha(W / "openviic_test.npz"),
        "ex_ov_test.json": sha(M3 / "ex_ov_test.json"),
        "lists.json": sha(R / "manuscript/prereg/2026-10-22_c_stage1/lists.json"),
        "ov_test_primary1941.txt": sha(R / "manuscript/prereg/2026-10-25_c_test/ov_test_primary1941.txt"),
        "xtab3.py": SHA["xtab3.py"], "build_memory.py": sha(R / "scripts/c_stage1/build_memory.py")})
    # the dump must reproduce xtab3's own first-four table: (outside the 1,941, first rank, SSCD of that cluster)
    first4 = sorted((q not in prim, h[0][0], h[0][2]) for q, h in
                    rec["hits_rank_cluster_sscd_clause_minhash"]["ret"].items() if h[0][0] <= 4)
    theirs = sorted(ns["res"])
    assert len(first4) == len(theirs) and all(a[:2] == b[:2] and abs(a[2] - b[2]) <= 1e-3 for a, b in
                                              zip(first4, theirs)), "id dump differs from xtab3's printed table"
    write_set("pin_c_ov_test", rec)


def pin_c2() -> None:
    ns, _ = run("xtab3.py")
    lists = json.loads((R / "manuscript/prereg/2026-10-22_c_stage1/lists.json").read_text(encoding="utf-8"))
    # XM-test2500: the Vietnamese memory (pool.npz, lists.json clusters) against the cached XM3600 features
    xm = load(FE / "of_xm3600_all.npz")
    rows = lists["sets"]["xm_test2500"]
    at = {i: n for n, i in enumerate(xm["ids"])}
    assert all(xm["sha"][at[i]] == h for i, _f, h in rows), "XM feature rows are not the listed images"
    ex = json.loads((M3 / "ex_xm_test2500.json").read_text(encoding="utf-8"))
    ns["ov"] = xm
    write_set("pin_c2_xm_test2500", flag(ns, ex, "xm_test2500", at, ns["mem"], [r[0] for r in rows], {
        "pool.npz": sha(Path(ns["W"]) / "pool.npz"), "of_xm3600_all.npz": sha(FE / "of_xm3600_all.npz"),
        "ex_xm_test2500.json": sha(M3 / "ex_xm_test2500.json"),
        "lists.json": sha(R / "manuscript/prereg/2026-10-22_c_stage1/lists.json"), "xtab3.py": SHA["xtab3.py"]}))
    # English arm: the COCO memory (feats_memory.npz, cen_memory.json clusters) against each test set
    cm = json.loads((M1 / "cen_memory.json").read_text(encoding="utf-8"))
    mem = {c["cid"]: [str(m[0]) for m in c["members"]] for c in cm["memory"]}
    ns["pool"] = load(FE / "feats_memory.npz")
    ns["pi"] = {k: i for i, k in enumerate(ns["pool"]["ids"])}
    control = {}
    for ds in ("coco_test", "nocaps_val"):
        ns["ov"] = load(FE / f"feats_{ds}.npz")
        # positive control: the registered rule on these files must recover the memory images cen_memory dropped
        control[ds] = int(ns["BM"].near(ns["pool"], ns["ov"]).sum())
        assert control[ds] == cm["counts"]["near_dropped"][ds], (ds, control[ds])
        ex = json.loads((M1 / f"ex_{ds}.json").read_text(encoding="utf-8"))
        qi = {i: n for n, i in enumerate(ns["ov"]["ids"])}
        rec = flag(ns, ex, ds, qi, mem, list(ex["ret"][ds]), {
            "feats_memory.npz": sha(FE / "feats_memory.npz"), f"feats_{ds}.npz": sha(FE / f"feats_{ds}.npz"),
            f"ex_{ds}.json": sha(M1 / f"ex_{ds}.json"), "cen_memory.json": sha(M1 / "cen_memory.json"),
            "xtab3.py": SHA["xtab3.py"]})
        rec["positive_control_registered_rule_memory_images_dropped"] = control[ds]
        write_set(f"pin_c2_{ds}", rec)


def pin_k() -> None:
    _, o1 = run("xtab.py")
    ns, _ = run("xtab2.py")
    x1, x2 = json.loads(o1), ns["out"]
    pool, kt, src = ns["pool"], ns["kt"], ns["src"]

    def pairs(X: dict, Y: dict, by_x: bool) -> dict:
        """xtab2.py:33 form of the rule: pair() gives C1|C2, the SSCD > 0.75 clause is added."""
        c12, sim = ns["pair"](X, Y)
        hit = c12 | (sim > 0.75)
        same = np.array(X["sha"])[:, None] == np.array(Y["sha"])[None, :]
        out = {}
        for a, b in zip(*np.nonzero(hit)):
            me, other = (X["ids"][a], Y["ids"][b]) if by_x else (Y["ids"][b], X["ids"][a])
            out.setdefault(str(int(me.split(":")[-1])), []).append(
                {"train": str(int(other.split(":")[-1])), "sscd": round(float(sim[a, b]), 4),
                 "byte_identical": bool(same[a, b])})
        return dict(sorted(out.items(), key=lambda kv: int(kv[0])))

    def exact(d: dict) -> list[str]:
        return [i for i, p in d.items() if any(x["byte_identical"] for x in p)]

    test = pairs(ns["sub"](pool, src == "ktvic"), kt, by_x=False)  # KTVIC train (3,769) against KTVIC test (558)
    dev = pairs(ns["D"], ns["T"], by_x=True)  # dev300 against KTVIC train minus dev300 (3,469)
    t1 = x1["ktvic_test<-ktvic"]
    rec = {"rule": RULE.replace("xtab3.py:27", "xtab.py:19; xtab2.py:14 and :33"),
           "ktvic_test": {"n": len(kt["ids"]), "n_flagged": len(test), "n_byte_identical": len(exact(test)),
                          "ids": list(test), "byte_identical_ids": exact(test), "pairs": test,
                          "xtab_py_counts": x1["ktvic_test<-ktvic"]},
           "ktvic_dev300": {"n": int(ns["isdev"].sum()), "n_flagged": len(dev), "n_byte_identical": len(exact(dev)),
                            "ids": list(dev), "byte_identical_ids": exact(dev), "pairs": dev,
                            "xtab2_py_ids": x2["dev300_neardup_ids"]},
           "inputs_sha256": {"pool.npz": sha(Path(ns["W"]) / "pool.npz"),
                             "ktvic_test.npz": sha(Path(ns["W"]) / "ktvic_test.npz"),
                             "ktvic_dev300.txt": sha(R / "data/splits/ktvic_dev300.txt"), "xtab.py": SHA["xtab.py"],
                             "xtab2.py": SHA["xtab2.py"]}}
    # the dump must agree with both unchanged checks
    assert (len(test), len(exact(test))) == (t1["test_imgs"], t1["exact_test_imgs"]), "differs from xtab.py"
    assert sorted(dev) == sorted(x2["dev300_neardup_ids"]), "differs from xtab2.py"
    assert len(exact(dev)) == x2["dev300_exact_in_train_rest"], "differs from xtab2.py"
    put("pin_k_ktvic.json", json.dumps(rec, indent=1) + "\n")
    put("pin_k_ktvic_test.txt", "".join(i + "\n" for i in test))
    put("pin_k_ktvic_dev300.txt", "".join(i + "\n" for i in dev))
    print("pin_k", {k: (v["n"], v["n_flagged"], v["n_byte_identical"]) for k, v in rec.items() if k.startswith("ktvic")})


if __name__ == "__main__":
    {"c": pin_c, "c2": pin_c2, "k": pin_k}[sys.argv[1]]()
