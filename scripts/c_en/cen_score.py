#!/usr/bin/env python3
"""C-EN scoring and decisions. Prereg manuscript/prereg/2026-10-27_c_en/PREREG.md §6-§8.

  python scripts/c_en/cen_score.py --selftest                                   CPU, synthetic only
  python scripts/c_en/cen_score.py score --set S --runs R ... --cache C --memory M --captions CS --refs F \
      --ledger-dir D                                                             M3, /root/vsps/.venv (pycocoevalcap 1.2)
  python scripts/c_en/cen_score.py decide --set S --ledger-dir D --out J [--coco-decide J]          once per set
Scorer: pycocoevalcap 1.2 PTBTokenizer + Cider (CIDEr-D) x 100, df over each scored set's own references; the
decision column is cider_ptb. InternVL3's ret and rand are scored at the frozen tau 0.10 (guard applied from the
verifier cache) and at -inf; every other run at -inf. Ledgers hold ids and numbers only.
"""
from __future__ import annotations

import argparse
import json
import math
import os
import sys
import tempfile
from pathlib import Path

import numpy as np

HERE = Path(__file__).resolve().parent
sys.path.insert(0, str(HERE))
import cen_decode as D  # noqa: E402  grid, frozen config, the English guard
import cen_fetch as F  # noqa: E402
import cen_memory as M  # noqa: E402

S2, G = D.S2, D.G
SESOI, LENGTH_GAP, DRAWS, SEED = 2.0, 0.10, 2000, 0  # CC-107 r5; PT §6.3, §7.2
BLOCK_SETS = {"coco_test": ("coco_test_5000",), "nocaps_val": ("nocaps_val_4500", "nocaps_val_3500")}
PRIMARY = {"coco_test": "coco_test_5000", "nocaps_val": "nocaps_val_4500"}


def ptb_cider():
    """(tokenize, cider) from pycocoevalcap 1.2: tokenize({id: [str]}) -> {id: [str]}; cider(gts, res) -> per-image
    CIDEr-D x 100 in gts order, df over gts."""
    from pycocoevalcap.cider.cider import Cider
    from pycocoevalcap.tokenizer.ptbtokenizer import PTBTokenizer

    tok = PTBTokenizer()

    def tokenize(d: dict[str, list[str]]) -> dict[str, list[str]]:
        return tok.tokenize({k: [{"caption": c} for c in v] for k, v in d.items()})

    def cider(gts: dict, res: dict) -> np.ndarray:
        _m, s = Cider().compute_score(gts, res)
        return 100 * np.asarray(s, float)

    return tokenize, cider


# ------------------------------------------------------------------------------------------------ score
def variants(run: dict, zs: dict, cache: dict, caps: dict, frozen_tau: str) -> list[tuple[str, dict, dict]]:
    """[(tau, {id: final caption}, guard counts)]: -inf always; the frozen tau too for a guarded run."""
    out = [("-inf", dict(run["predictions"]), {})]
    if frozen_tau in S2.INFINITE or run["spec"]["arm"] == "zs":
        return out
    tau, final, n = float(frozen_tau), {}, {"neighbour_only": 0, "rejected": 0, "deleted": 0, "fallback": 0}
    for i, cap in run["predictions"].items():
        shown = [caps[c] for c in run["exemplars"][i]]
        no = D.neighbour_only(cap, zs["predictions"][i], shown)
        if any((run["dataset"], i, o) not in cache for o in no):
            raise SystemExit(f"{run['run_id']} {i}: a neighbour-only item has no verifier row")
        sc = {o: cache[(run["dataset"], i, o)] for o in no}
        final[i], no, rej, how = D.guarded(cap, zs["predictions"][i], shown, sc, tau)
        n["neighbour_only"] += len(no)
        n["rejected"] += len(rej)
        n[how] = n.get(how, 0) + (how != "kept")
    return out + [(frozen_tau, final, n)]


def score_set(ds: str, runs: list[dict], zs_by: dict, cache: dict, caps: dict, refs: dict, scorer,
              guard_ok: bool = True) -> list[dict]:
    """Ledger rows of every run x tau x scored set; guard_ok False (a registered verifier stop): -inf rows only."""
    tokenize, cider = scorer
    cfg = S2.frozen()
    rows = []
    want = [str(i) for i in M.scored_ids(BLOCK_SETS[ds][0])]
    if set(refs) != set(want):
        raise SystemExit(f"the reference subset is not the {ds} set")
    rtok = tokenize({i: refs[i] for i in want})
    for r in runs:
        tau_m = cfg["models"][r["model"]]["tau"] if guard_ok else "-inf"
        for tau, final, gcount in variants(r, zs_by[r["model"]], cache, caps, tau_m):
            htok = tokenize({i: [final[i]] for i in want})
            for name in BLOCK_SETS[ds]:
                ids = [str(i) for i in M.scored_ids(name)]
                c = cider({i: rtok[i] for i in ids}, {i: htok[i] for i in ids})
                rows.append({"run_id": r["run_id"], "model": r["model"], "arm": r["spec"]["arm"], "dataset": ds,
                             "scored": name, "tau": tau, "n": len(ids), "guard": gcount,
                             "mean_cider_ptb": float(c.mean()),
                             "per_image": {"ids": ids, "cider_ptb": [round(float(x), 6) for x in c],
                                           "len_ptb": [len(htok[i][0].split()) for i in ids]}})
    return rows


def cmd_score(a) -> None:
    F.host_ok(a.expect_head)
    cfg = S2.frozen()
    runs = [G.read_preds(p) for p in a.runs]
    if {r["run_id"] for r in runs} != set(D.grid(cfg, (a.set,))) or any(r.get("c_schema") != D.SCHEMA for r in runs):
        raise SystemExit(f"score: exactly the 6 C-EN runs of {a.set}")
    zs_by = {r["model"]: r for r in runs if r["spec"]["arm"] == "zs"}
    cache = {}
    if a.cache and a.cache.exists():
        cache = {(x["dataset"], x["image_id"], x["class"]): x["p_with"] - x["p_without"]
                 for x in map(json.loads, a.cache.read_text().splitlines()) if x}
    stopped = D.stop_marker(a.cache, a.set).exists() if a.cache else True
    refs = json.loads(a.refs.read_text(encoding="utf-8"))
    if refs.get("what") != a.set:
        raise SystemExit("not this set's reference subset")
    # PT §7.6: after a registered verifier stop InternVL3's frozen arms are incomplete; -inf rows only
    rows = score_set(a.set, runs, zs_by, cache, D.load_captions(a.captions, a.memory), refs["refs"], ptb_cider(),
                     guard_ok=not stopped)
    for name in BLOCK_SETS[a.set]:
        led = D.out_ok(a.ledger_dir / f"ledger_{name}.jsonl")
        if led.exists():
            raise SystemExit(f"{led.name} exists; a set is scored once")
        led.write_text("".join(json.dumps(x) + "\n" for x in rows if x["scored"] == name))
    print(json.dumps({"set": a.set, "rows": len(rows), "verifier_stop": stopped}))


# ------------------------------------------------------------------------------------------------ decide
def draws(n: int) -> np.ndarray:
    return np.random.default_rng(SEED).integers(0, n, (DRAWS, n))


def ci(x: np.ndarray, idx: np.ndarray) -> dict:
    lo, hi = np.percentile(x[idx].mean(1), [2.5, 97.5])
    return {"d": float(x.mean()), "lo": float(lo), "hi": float(hi)}


def get(rows: list[dict], run_id: str, tau: str) -> dict | None:
    hit = [r for r in rows if r["run_id"] == run_id and r["tau"] == tau]
    if len(hit) > 1:
        raise SystemExit(f"ledger: {len(hit)} rows for {run_id} at {tau}")
    return hit[0] if hit else None


def arr(row: dict, key: str = "cider_ptb") -> np.ndarray:
    return np.array(row["per_image"][key], float)


def one_set(rows: list[dict], ds: str, name: str) -> dict:
    """Every registered row of one scored set, on its own bootstrap matrix (§6, §7)."""
    cfg = S2.frozen()
    n = rows[0]["n"]
    idx = draws(n)
    ids = rows[0]["per_image"]["ids"]
    if any(r["per_image"]["ids"] != ids for r in rows):
        raise SystemExit(f"{name}: rows are not on one pinned image order")
    rid = {(m, a): D.spec(cfg, ds, m, a)["run_id"] for m in D.C.MODELS for a in D.ARMS}
    tau = {m: cfg["models"][m]["tau"] for m in D.C.MODELS}
    out: dict = {"n": n, "per_model": {}, "complete": True}
    diffs = []
    for m in D.C.MODELS:
        ret, rand, zs = get(rows, rid[m, "ret"], tau[m]), get(rows, rid[m, "rand"], tau[m]), get(rows, rid[m, "zs"],
                                                                                                 "-inf")
        if ret is None or rand is None:
            out["complete"] = False
            continue
        d = arr(ret) - arr(rand)
        diffs.append(d)
        lr, la = np.mean(arr(ret, "len_ptb")), np.mean(arr(rand, "len_ptb"))
        out["per_model"][m] = {"ret_minus_rand": ci(d, idx), "ret_minus_zs": ci(arr(ret) - arr(zs), idx),
                               "rand_minus_zs": ci(arr(rand) - arr(zs), idx), "len_ret": float(lr),
                               "len_rand": float(la), "length_gap": float(abs(lr - la) / la),
                               "guard": ret.get("guard", {}), "guard_rand": rand.get("guard", {})}
    if out["complete"]:
        pooled = np.mean(diffs, axis=0)
        out["pooled"] = ci(pooled, idx)
        out["pooled_ret_minus_zs"] = ci(np.mean([arr(get(rows, rid[m, "ret"], tau[m])) - arr(get(rows, rid[m, "zs"],
                                                                                                 "-inf"))
                                                 for m in D.C.MODELS], axis=0), idx)
    iv = [get(rows, rid["internvl3_8b", a], "-inf") for a in ("ret", "rand")]
    if all(iv):
        r = ci(arr(iv[0]) - arr(iv[1]), idx)
        out["secondary_neg_inf_internvl3"] = {**r, "label": "detected" if r["lo"] > 0 else "not detected"}
    return out


def rule(res: dict) -> dict:
    """CC-107 r5 / PT §7.2: point > +2.0 and 95% CI lower bound > 0."""
    if not res["complete"]:
        return {"passed": None, "verdict": "incomplete"}
    p = res["pooled"]
    ok = p["d"] > SESOI and p["lo"] > 0
    return {"passed": bool(ok), "d": p["d"], "lo": p["lo"], "hi": p["hi"], "verdict": "PASS" if ok else "FAIL"}


def decide(sets: dict[str, list[dict]], ds: str, coco: dict | None, domains: dict[str, str] | None = None) -> dict:
    out = {"set": ds, "SESOI": SESOI, "scored": {n: one_set(r, ds, n) for n, r in sets.items()}}
    main = out["scored"][PRIMARY[ds]]
    v = rule(main)
    if ds == "coco_test":
        fired = main["complete"] and any(x["length_gap"] > LENGTH_GAP for x in main["per_model"].values())
        if v["passed"] and fired:
            v["verdict"] = "PASS, not separated from length"
        out["P1_EN"] = {**v, "L": bool(fired)}
    else:
        p1 = (coco or {}).get("P1_EN", {})
        if "passed" not in p1:
            raise SystemExit("the NoCaps decide reads the COCO decide (fixed order of the claim)")
        out["S_NC"] = v
        out["S_NC_sensitivity_3500"] = rule(out["scored"]["nocaps_val_3500"])
        out["claim_transfers_to_nocaps"] = bool(p1["passed"] and v["passed"])  # gatekeeping: the claim only
        if domains:
            out["per_domain"] = per_domain(sets[PRIMARY[ds]], domains)
    return out


def per_domain(rows: list[dict], domains: dict[str, str]) -> dict:
    """Reported, non-gating: the pooled ret - rand per NoCaps domain, each on its own matrix."""
    cfg = S2.frozen()
    tau = {m: cfg["models"][m]["tau"] for m in D.C.MODELS}
    ids = rows[0]["per_image"]["ids"]
    try:
        d = np.mean([arr(get(rows, D.spec(cfg, "nocaps_val", m, "ret")["run_id"], tau[m])) -
                     arr(get(rows, D.spec(cfg, "nocaps_val", m, "rand")["run_id"], tau[m])) for m in D.C.MODELS], 0)
    except TypeError:
        return {}
    out = {}
    for dom in sorted(set(domains.values())):
        sel = np.array([domains[i] == dom for i in ids])
        out[dom] = {"n": int(sel.sum()), **ci(d[sel], draws(int(sel.sum())))}
    return out


def cmd_decide(a) -> None:
    F.host_ok(a.expect_head)
    if Path(a.out).exists():
        raise SystemExit("a set is decided once")
    sets, shas = {}, {}
    for name in BLOCK_SETS[a.set]:
        p = a.ledger_dir / f"ledger_{name}.jsonl"
        sets[name], shas[p.name] = [json.loads(x) for x in p.read_text().splitlines() if x], F.sha_file(p)
    coco = json.loads(a.coco_decide.read_text()) if a.coco_decide else None
    domains = {str(r[0]): r[3] for r in F.load_list("nocaps_val")} if a.set == "nocaps_val" else None
    out = decide(sets, a.set, coco, domains)
    out |= {"ledger_sha256": shas, "coco_decide_sha256": F.sha_file(a.coco_decide) if a.coco_decide else None,
            "prereg": f"{F.PDIR}/PREREG.md", "prereg_sha256": F.sha_file(F.ROOT / F.PDIR / "PREREG.md"),
            "head": F.HEAD_AT_RUN, "utc": F.utc()}
    D.out_ok(a.out).write_text(json.dumps(out, indent=1) + "\n")
    print(json.dumps({"set": a.set, "written": Path(a.out).name}))


# ------------------------------------------------------------------------------------------------ self-test (CPU)
def fake_rows(ds: str, names: list[str], gain: dict[str, float], lens: tuple = (10, 10), drop_iv: bool = False):
    """Synthetic ledgers (numbers only) with a chosen ret - rand gain per backbone."""
    cfg = S2.frozen()
    rng = np.random.default_rng(1)
    out = {}
    for name in names:
        n = 300
        ids = [str(i) for i in range(n)]
        rows = []
        for m in D.C.MODELS:
            base = rng.normal(80, 20, n)
            for arm in D.ARMS:
                rid = D.spec(cfg, ds, m, arm)["run_id"]
                v = base + {"ret": gain[m], "rand": 0.0, "zs": -5.0}[arm] + rng.normal(0, 3, n)
                ln = [lens[0] if arm == "ret" else lens[1]] * n
                taus = ["-inf"] + ([cfg["models"][m]["tau"]] if D.guarded_model(cfg, m) and arm != "zs" else [])
                for t in taus:
                    if drop_iv and m == "internvl3_8b" and t != "-inf":
                        continue
                    rows.append({"run_id": rid, "model": m, "arm": arm, "dataset": ds, "scored": name, "tau": t,
                                 "n": n, "guard": {}, "per_image": {"ids": ids, "cider_ptb": list(v), "len_ptb": ln}})
        out[name] = rows
    return out


def selftest() -> None:
    big, small = {"qwen25vl_7b": 6.0, "internvl3_8b": 4.0}, {"qwen25vl_7b": 1.0, "internvl3_8b": 1.0}
    c = decide(fake_rows("coco_test", ["coco_test_5000"], big), "coco_test", None)
    assert c["P1_EN"]["verdict"] == "PASS" and not c["P1_EN"]["L"], c["P1_EN"]
    assert c["scored"]["coco_test_5000"]["secondary_neg_inf_internvl3"]["label"] == "detected"
    cl = decide(fake_rows("coco_test", ["coco_test_5000"], big, lens=(12, 10)), "coco_test", None)
    assert cl["P1_EN"]["verdict"] == "PASS, not separated from length" and cl["P1_EN"]["L"]
    cf = decide(fake_rows("coco_test", ["coco_test_5000"], small), "coco_test", None)
    assert cf["P1_EN"]["verdict"] == "FAIL", "point under the SESOI"
    ci_ = decide(fake_rows("coco_test", ["coco_test_5000"], big, drop_iv=True), "coco_test", None)
    assert ci_["P1_EN"]["verdict"] == "incomplete", "a verifier stop leaves the frozen InternVL3 arms incomplete"
    names = ["nocaps_val_4500", "nocaps_val_3500"]
    dom = {str(i): ("in-domain", "near-domain", "out-domain")[i % 3] for i in range(300)}
    n_pass = decide(fake_rows("nocaps_val", names, big), "nocaps_val", c, dom)
    assert n_pass["S_NC"]["passed"] and n_pass["claim_transfers_to_nocaps"] and len(n_pass["per_domain"]) == 3
    n_gate = decide(fake_rows("nocaps_val", names, big), "nocaps_val", cf, dom)
    assert n_gate["S_NC"]["passed"] and not n_gate["claim_transfers_to_nocaps"], "fixed order gates the claim only"
    assert F.refuses(lambda: decide(fake_rows("nocaps_val", names, big), "nocaps_val", None)), "needs COCO's decide"
    idx = draws(300)
    assert np.array_equal(idx, np.random.default_rng(0).integers(0, 300, (2000, 300))), "default_rng(0), first draw"
    # guard variants from the verifier cache
    run = {"run_id": "r", "dataset": "coco_test", "model": "internvl3_8b", "spec": {"arm": "ret"},
           "predictions": {"1": "a zebra waiting beside a motorcycle on a violet moon."},
           "exemplars": {"1": ["e0"]}}
    zs = {"predictions": {"1": "a zebra on a moon"}}
    v = variants(run, zs, {("coco_test", "1", "motorcycle"): 0.05}, {"e0": "a red motorcycle"}, "0.10")
    assert [t for t, _f, _g in v] == ["-inf", "0.10"] and v[1][1]["1"] == "a zebra waiting on a violet moon."
    assert v[1][2]["rejected"] == 1 and v[1][2]["deleted"] == 1
    assert len(variants(run, zs, {}, {}, "-inf")) == 1, "an unguarded run at -inf only"
    assert F.refuses(lambda: variants(run, zs, {}, {"e0": "a red motorcycle"}, "0.10")), "an unverified item"
    msg = "PTB + CIDEr-D: pycocoevalcap not installed here, checked on M3"
    try:
        scorer = ptb_cider()
    except ImportError:
        if os.environ.get("VSPS_MACHINE_ID") or os.environ.get("CEN_REQUIRE_PTB"):  # CC-121 W1: fail, never skip
            raise SystemExit("selftest FAILED: pycocoevalcap is not importable where the PTB scorer must run")
        scorer = None
    if scorer:
        tokenize, cider = scorer
        refs = {"1": ["A dog naps under violet clouds.", "a brown dog dozing"], "2": ["Two red cats sleep.", "cats on a bed"],
                "3": ["A red bus.", "a bus on a road"]}
        rt = tokenize(refs)
        h = tokenize({"1": ["a dog naps under violet clouds"], "2": ["a bus"], "3": ["a red bus"]})
        s3 = cider(rt, h)
        s2 = cider({k: rt[k] for k in ("1", "3")}, {k: h[k] for k in ("1", "3")})
        assert s3[0] > s3[1] == 0 and s3.shape == (3,) and abs(s3[2] - s2[1]) > 1e-6, "df per scored set"
        msg = "PTB + CIDEr-D on synthetic sentences (df per scored set)"
    print("selftest ok: P1-EN rule (> +2.0 and LB > 0), rule L, incomplete on a verifier stop, tau -inf "
          "secondary, NoCaps fixed order gates the claim only (decided whatever COCO shows), per domain, bootstrap "
          f"default_rng(0), guard variants from the cache; {msg}")


def main() -> None:
    ap = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    ap.add_argument("--selftest", action="store_true")
    sub = ap.add_subparsers(dest="cmd")
    p = sub.add_parser("score")
    p.add_argument("--set", choices=M.TEST_SETS, required=True)
    p.add_argument("--runs", nargs="+", type=Path, required=True)
    p.add_argument("--cache", type=Path, required=True)
    for k in ("memory", "captions", "refs", "ledger-dir"):
        p.add_argument(f"--{k}", type=Path, required=True)
    p.add_argument("--expect-head", required=True)
    p = sub.add_parser("decide")
    p.add_argument("--set", choices=M.TEST_SETS, required=True)
    p.add_argument("--ledger-dir", type=Path, required=True)
    p.add_argument("--out", type=Path, required=True)
    p.add_argument("--coco-decide", type=Path)
    p.add_argument("--expect-head", required=True)
    a = ap.parse_args()
    if a.selftest:
        return selftest()
    {"score": cmd_score, "decide": cmd_decide}.get(a.cmd, lambda _a: ap.error("mode?"))(a)


if __name__ == "__main__":
    main()
