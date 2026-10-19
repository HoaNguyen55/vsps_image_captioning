#!/usr/bin/env python
"""B-N2 scorer (Paper B, PD-19): the KTVIC leaked/clean placebo DiD and descriptive gaps, as registered in
manuscript/prereg/2026-10-19_b_n2_leakage_did_prereg_v2.json (commit 9f7e6bf); every threshold is read from it.

    score_b_n2.py gate   OUT.json                provenance, self-check and F0 on all 558 images; no subset statistic
    score_b_n2.py dryrun OUT.json                made-up captions and references end to end, with asserts
    score_b_n2.py run    OUT.json --gate G.json  the analysis; only with this file and G.json (its all-PASS gate) at HEAD
Needs NCS_DATA, VNCORENLP_DIR, JAVA_HOME (a JDK, for jnius) and `java` on PATH. Outputs are never overwritten.
"""
from __future__ import annotations

import argparse
import functools
import hashlib
import json
import os
import re
import subprocess
import sys
import tempfile
from importlib.metadata import version
from pathlib import Path

import numpy as np

HERE = Path(__file__).resolve()
ROOT = Path(subprocess.run(["git", "-C", str(HERE.parent), "rev-parse", "--show-toplevel"],
                           capture_output=True, text=True, check=True).stdout.strip())
sys.path[:0] = [str(ROOT), str(ROOT / "scripts")]
PREREG = ("manuscript/prereg/2026-10-19_b_n2_leakage_did_prereg_v2.json",
          "675d37a9da2b26a0472ff0fd58a370dd55705602c78006bc1a52d96245d15972")
# S2 is "punctuation fix (B-N1 draft definition)": scoring.fix of the committed B-N1 JSON pinned below, i.e. trailing
# whitespace and . ! ? ... (U+2026) stripped from the end of every candidate AND every reference before segmentation.
B_N1 = ("manuscript/prereg/2026-10-19_b_n1_vi_leaderboard.json",
        "9ff02dc259258de1add426abd02131f2122e3476a81f9a076066ed6d74906134")
fix = functools.partial(re.compile("[\\s.!?…]+$").sub, "")


def sha(data: bytes) -> str:
    return hashlib.sha256(data).hexdigest()


def pinned(rel: str, want: str | None = None) -> bytes:
    """Bytes of repo file `rel`; refuses unless they equal its blob at HEAD and, when given, the sha256 pin `want`."""
    data = (ROOT / rel).read_bytes()
    if data != subprocess.run(["git", "-C", str(ROOT), "cat-file", "blob", f"HEAD:{rel}"], capture_output=True).stdout:
        raise SystemExit(f"REFUSED: {rel} is not committed unmodified at HEAD")
    if want and sha(data) != want:
        raise SystemExit(f"PROVENANCE FAIL: {rel} sha256 {sha(data)} != pin {want}")
    return data


def prereg() -> tuple[dict, dict]:
    """The pinned prereg, with its scorer, delta-source and S2 pins checked, and the thresholds it registers."""
    P = json.loads(pinned(*PREREG))
    m, b, src = P["methods"], P["methods"]["bootstrap"], P["delta"]["source"]
    for rel, want in [*m["cider_d"]["scorer_files_sha256"].items(), *m["object_f1"]["scorer_sha256"].items(),
                      (src["path"], src["sha256"]), B_N1]:
        pinned(rel, want)
    cfg = {"B": b["B"], "seed": int(re.fullmatch(r"numpy\.random\.default_rng\((\d+)\)", b["rng"])[1]),
           "q": [float(x) for x in re.fullmatch(r"percentile ([\d.]+) / ([\d.]+)", b["ci"]).groups()],
           "tol": float(re.fullmatch(r"F0 gate: .* within ([0-9.e-]+)", m["self_check"][1])[1]),
           "delta": P["delta"]["value"], "n_L": P["sets"]["leaked"]["n"], "n_C": P["sets"]["clean"]["n"]}
    return P, cfg


def caption_metrics():
    from rescap.metrics import CaptionMetrics
    return CaptionMetrics(language="vi", segmenter="rdrsegmenter", tokenize=True)  # methods.cider_d.config


def per_image(refs: dict, preds: dict, edit=None) -> dict:
    """{id: c(i)}: one Cider().compute_score over all ids of `refs` on CaptionMetrics._align + _tokenize, so the
    document frequencies come from all of them; `edit` rewrites every candidate and reference first (S2)."""
    from pycocoevalcap.cider.cider import Cider
    edit, cm, ids = edit or (lambda text: text), caption_metrics(), sorted(refs)
    g, r = cm._tokenize(*cm._align({i: [edit(x) for x in refs[i]] for i in ids}, {i: [edit(preds[i][0])] for i in ids}))
    if cm.segmenter != "rdrsegmenter":
        raise SystemExit(f"K-F0: the segmenter fell back ({cm.segmenter})")
    return dict(zip(g, map(float, Cider().compute_score(g, r)[1])))


def evaluate_as_written(preds_path: Path, name: str) -> tuple[float, str]:
    """CIDEr x100 and segmenter of scripts/evaluate.py, run unchanged on `preds_path` in a fresh process."""
    with tempfile.TemporaryDirectory() as tmp:
        out = Path(tmp) / "scored.json"
        r = subprocess.run([sys.executable, str(ROOT / "scripts" / "evaluate.py"), "--predictions", str(preds_path),
                            "--prompt", "short", "--name", name, "--out", str(out)],
                           capture_output=True, encoding="utf-8", errors="replace")
        if r.returncode:
            raise SystemExit(f"K-F0: scripts/evaluate.py failed on {name}:\n{r.stdout[-1500:]}\n{r.stderr[-1500:]}")
        row = json.loads(out.read_text(encoding="utf-8"))["results"][0]  # the word-level row
    return row["scores_scaled_x100"]["CIDEr"], row["segmenter"]


def check_system(s: str, e: dict, cfg: dict, X: dict) -> dict:
    """Provenance, self-check and F0 of one D1 system on the full set; a system lacking ids is dropped (K-COV)."""
    refs, res = X["refs"], json.loads(pinned(e["path"], e["sha256"]))["results"]
    committed = next(r for r in res if r["segmenter"] == "rdrsegmenter")["scores_scaled_x100"]["CIDEr"]
    p = next(p for p in e["preds"] if p["git_tracked"])
    raw = json.loads(pinned(p["path"], p["sha256"]))
    if committed != e["value_full_558"] or len(refs) != e["n_images"]:
        raise SystemExit(f"PROVENANCE FAIL: {s}: the committed CIDEr or n differs from the prereg")
    preds = {str(k): (v if isinstance(v, list) else [v]) for k, v in raw.items()}  # as scripts/evaluate.py:316
    if refs.keys() - preds.keys():
        X["dropped"].append(s)
        return {"K_COV": f"dropped: {len(refs.keys() - preds.keys())} of {len(refs)} ids have no prediction"}
    cider_ev, seg = evaluate_as_written(ROOT / p["path"], s)
    X["preds"][s], X["vec"][s] = preds, per_image(refs, preds)
    f0 = 100 * float(np.mean(list(X["vec"][s].values())))
    return {"results": {k: e[k] for k in ("path", "sha256", "key")} | {"CIDEr_x100": committed},
            "preds": {"path": p["path"], "sha256": p["sha256"], "n": len(preds)},
            "self_check": {"evaluate_py_CIDEr_x100": cider_ev, "segmenter": seg,
                           "pass": cider_ev == committed and seg == "rdrsegmenter"},
            "F0": {"mean_c_x100": f0, "abs_diff": abs(f0 - committed), "pass": abs(f0 - committed) <= cfg["tol"]}}


def gate(P: dict, cfg: dict) -> dict:
    """Provenance of every input, then the self-check and F0 of every D1 system. Computes no subset statistic."""
    import evaluate as ev
    S, sets = P["systems"], P["sets"]
    D1, K, Kp = S["D1_all_KTVIC_only_short"], S["K_P1_legacy_short"], S["Kp_fuse2_legacy_short"]
    pairs = [tuple(p) for p in S["seed_matched_pairs"]]
    if not (all(D1.get(s) == e for s, e in {**K, **Kp}.items()) and all(a in Kp and k in K for a, k in pairs)
            and "multiref_s42" not in D1 and S["multiref_s42_entry"]["enters_D1"] is False):  # PD-19 (d) c3
        raise SystemExit("REFUSED: the registered design is inconsistent")
    refs = ev.references("test_data.json")  # as scripts/evaluate.py:305
    L, C = (pinned(sets[k]["path"], sets[k]["sha256"]).decode("utf-8").split() for k in ("leaked", "clean"))
    if ev.KTVIC.name != "ktvic" or (len(L), len(C)) != (cfg["n_L"], cfg["n_C"]) or len(set(L) | set(C)) != len(refs) \
            or set(L) | set(C) != refs.keys():  # sizes as registered, no repeats, disjoint, union = the test ids
        raise SystemExit("REFUSED: the KTVIC test ids and the leaked/clean lists fail their checks")
    X = {"refs": refs, "L": sorted(L), "C": sorted(C), "K": list(K), "Kp": list(Kp), "pairs": pairs,
         "preds": {}, "vec": {}, "dropped": []}
    X["systems"] = {s: check_system(s, e, cfg, X) for s, e in D1.items()}
    X["all_pass"] = all(r["self_check"]["pass"] and r["F0"]["pass"] for r in X["systems"].values() if "K_COV" not in r)
    X["inputs"] = {"ktvic_test_data.json": sha((ev.KTVIC / "test_data.json").read_bytes()),
                   **{k: {f: sets[k][f] for f in ("path", "sha256", "n")} for k in ("leaked", "clean")}}
    return X


def verdict(lo: float, hi: float, delta: float) -> str:
    """placebo_verdict: PASS inside (-delta, +delta), FAIL entirely outside, INCONCLUSIVE otherwise."""
    if lo > -delta and hi < delta:
        return "PASS"
    if lo >= delta or hi <= -delta:
        return "FAIL"
    return "INCONCLUSIVE"


def estimands(pt: dict, bt: dict | None, K: list, Kp: list, pairs: list, q: list) -> dict:
    """gap = C_L - C_C; DiD_PL = mean_K' gap - mean_K gap; seed-matched gap differences. `bt` holds each system's
    B bootstrap gaps (CI = percentiles q), or is None for points only."""
    def ci(x):
        return None if x is None else [float(v) for v in np.percentile(x, q)]

    def did(g):
        return np.mean([g[s] for s in Kp], 0) - np.mean([g[s] for s in K], 0)

    gap = {s: a - c for s, (a, c) in pt.items()}
    return {"gap": {s: {"C_L": pt[s][0], "C_C": pt[s][1], "gap": gap[s], "ci95": ci(bt and bt[s])} for s in pt},
            "DiD_PL": {"est": float(did(gap)), "ci95": ci(bt and did(bt))},
            "seed_matched": {f"{a} - {k}": {"est": gap[a] - gap[k], "ci95": ci(bt and bt[a] - bt[k])} for a, k in pairs}}


def analyse(X: dict, D1: list, cfg: dict) -> dict:
    """Subset statistics over the systems in D1 (K, K' and the pairs lose any K-COV drop): primary CIDEr-D (558-image
    df) with the placebo verdict, S1 points, S2 and object F1 with CIs. One stratified draw set (|L| ids from L and |C|
    from C, with replacement) serves every system and metric."""
    import object_prf as op
    from rescap.chair import _ancestors, objects_in
    refs, preds, L, C = X["refs"], X["preds"], X["L"], X["C"]
    K, Kp = [s for s in X["K"] if s in D1], [s for s in X["Kp"] if s in D1]
    pairs = [p for p in X["pairs"] if set(p) <= set(D1)]
    rng = np.random.default_rng(cfg["seed"])
    dL, dC = rng.integers(0, len(L), (cfg["B"], len(L))), rng.integers(0, len(C), (cfg["B"], len(C)))

    def metric(parts, point, boot=None):
        pt = {s: (point(a), point(c)) for s, (a, c) in parts.items()}
        return estimands(pt, boot and {s: boot(a, dL) - boot(c, dC) for s, (a, c) in parts.items()}, K, Kp, pairs,
                         cfg["q"])

    def split(x, kind=list):
        return kind([x[i] for i in L]), kind([x[i] for i in C])

    def s1(part):  # S1: CaptionMetrics.compute on the subset alone, so df from the subset
        s, ids = part
        return 100 * caption_metrics().compute({i: refs[i] for i in ids}, {i: preds[s][i] for i in ids})["CIDEr"]

    def f1(rows):
        return op.scores(rows)["F1"]

    cider = (lambda v: 100 * float(v.mean())), (lambda v, d: 100 * v[d].mean(1))  # C_S = 100 * mean of c(i) over S
    gold = {i: set().union(*[set(objects_in(r)) for r in rs]) for i, rs in refs.items()}  # as object_prf.ktvic_block
    rows = {s: {i: op.image_counts(set(objects_in(preds[s][i][0] or "")), gold[i], _ancestors) for i in refs} for s in D1}
    out = {"primary_cider_d_df558": metric({s: split(X["vec"][s], np.array) for s in D1}, *cider),
           "S1_subset_df_points": metric({s: ((s, L), (s, C)) for s in D1}, s1),
           "S2_punct_fix_df558": metric({s: split(per_image(refs, preds[s], fix), np.array) for s in D1}, *cider),
           "object_F1": metric({s: split(rows[s]) for s in D1}, f1,
                               lambda rs, d: np.array([f1([rs[j] for j in row]) for row in d]))}
    pl = out["primary_cider_d_df558"]["DiD_PL"]
    pl["verdict"] = verdict(*pl["ci95"], cfg["delta"])
    out["draws"] = {"B": cfg["B"], "seed": cfg["seed"], "order": "rng.integers(0,|L|,(B,|L|)) then rng.integers("
                    "0,|C|,(B,|C|)); L and C in sorted-id order; the same draws for every system and metric"}
    return out


def run(P: dict, cfg: dict, gate_file: str) -> dict:
    """The registered analysis, only from this scorer committed at HEAD with its committed all-PASS gate output."""
    pinned(HERE.relative_to(ROOT).as_posix())
    g_rel = Path(gate_file).resolve().relative_to(ROOT).as_posix()
    G = json.loads(pinned(g_rel))
    if (G.get("mode"), G.get("all_pass"), G["script_sha256"], G["prereg"]["sha256"]) != \
            ("gate", True, sha(HERE.read_bytes()), PREREG[1]):
        raise SystemExit("REFUSED: the gate file is not a committed all-PASS gate of this scorer")
    X = gate(P, cfg)
    if not X["all_pass"]:
        raise SystemExit("K-F0: the self-check or F0 failed; nothing on subsets is computed")
    out = analyse(X, [s for s in X["systems"] if s not in X["dropped"]], cfg)
    fail = out["primary_cider_d_df558"]["DiD_PL"]["verdict"] == "FAIL"
    return {"gate": {"path": g_rel, "sha256": sha(pinned(g_rel))}, "self_check_F0": X["systems"], "inputs": X["inputs"],
            "K_COV_dropped": X["dropped"], "K_PL": P["kill_rules"]["K-PL"] if fail else None,
            "multiref_s42": P["systems"]["multiref_s42_entry"]["disclosure"], **out}


def dryrun(cfg: dict) -> dict:
    """The subset path end to end on made-up captions and references (no real data), with asserts."""
    assert [verdict(lo, hi, 3.0) for lo, hi in ((-2.9, 2.9), (-3.0, 1), (3.0, 5), (-6, -3.0), (-4, 4))] == \
        ["PASS", "INCONCLUSIVE", "FAIL", "FAIL", "INCONCLUSIVE"]
    assert [fix(t) for t in ("một con chó .", "a?! …\n", "a. b")] == ["một con chó", "a", "a. b"]
    try:
        pinned(PREREG[0], "0" * 64)
        raise AssertionError("a wrong pin was accepted")
    except SystemExit as refused:
        assert "PROVENANCE FAIL" in str(refused)
    objs = ["người đàn ông", "con chó", "con mèo", "chiếc xe máy", "cái bàn", "cái ghế", "cái cây", "chiếc ô tô"]
    where, verbs = ["trên đường phố", "trong căn phòng", "ở công viên", "bên bờ sông"], ["đang đứng", "đang ngồi", "đang đi"]
    ids = [f"s{n:02d}" for n in range(24)]
    L, C, K, Kp = ids[:16], ids[16:], ["k42", "k43", "k44"], ["q42", "q43", "q44"]
    refs = {i: [f"{objs[n % 8]} {verbs[j % 3]} {where[(n + j) % 4]} cạnh {objs[(n + j + 1) % 8]}" for j in range(5)]
            for n, i in enumerate(ids)}
    preds = {k: {i: [f"{objs[n % 8]} {verbs[(n + j) % 3]} {where[n * (j + 1) % 4]}" + " ." * (n % 2)]
                 for n, i in enumerate(ids)} for j, k in enumerate(K)}
    # q42 and q43 copy a reference on L only; q44 equals k44; x equals k42; y lacks one id and must be dropped (K-COV)
    preds |= {q: {i: refs[i][:1] if i in L and j < 2 else preds[K[j]][i] for i in ids} for j, q in enumerate(Kp)}
    preds |= {"x": preds["k42"], "y": {i: c for i, c in preds["k42"].items() if i != ids[0]}}
    dropped = [s for s in preds if refs.keys() - preds[s].keys()]
    D1 = [s for s in preds if s not in dropped]
    vec = {s: per_image(refs, preds[s]) for s in D1}
    for s in D1:  # F0 on made-up data: the per-image mean equals CaptionMetrics.compute
        full = 100 * caption_metrics().compute(refs, preds[s])["CIDEr"]
        assert abs(100 * np.mean(list(vec[s].values())) - full) <= cfg["tol"], s
    X = {"refs": refs, "preds": preds, "vec": vec, "L": L, "C": C, "K": K + ["y"], "Kp": Kp, "pairs": list(zip(Kp, K))}
    out = analyse(X, D1, cfg)
    pr, same = out["primary_cider_d_df558"], {"est": 0.0, "ci95": [0.0, 0.0]}
    assert dropped == ["y"] and pr["DiD_PL"]["verdict"] == "FAIL" and pr["DiD_PL"]["est"] > cfg["delta"]
    assert pr["seed_matched"]["q44 - k44"] == same == out["object_F1"]["seed_matched"]["q44 - k44"]
    assert abs(pr["DiD_PL"]["est"] - np.mean([v["est"] for v in pr["seed_matched"].values()])) < 1e-9
    assert out["S2_punct_fix_df558"]["gap"]["k42"]["C_L"] != pr["gap"]["k42"]["C_L"]
    assert all(v["ci95"] is None for v in out["S1_subset_df_points"]["gap"].values())
    return {"SYNTHETIC": "made-up captions and references; no real prediction, reference or split list is used",
            "K_COV_dropped": dropped, **out}


def main() -> int:
    ap = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    ap.add_argument("mode", choices=("gate", "dryrun", "run"))
    ap.add_argument("out")
    ap.add_argument("--gate", help="run mode: the committed output of `gate`")
    a = ap.parse_args()
    if Path(a.out).exists() or not (os.environ.get("NCS_DATA") and os.environ.get("VNCORENLP_DIR")):
        raise SystemExit(f"REFUSED: {a.out} exists (outputs are never overwritten), or NCS_DATA/VNCORENLP_DIR is unset")
    P, cfg = prereg()
    vnc = Path(os.environ["VNCORENLP_DIR"])
    env = {"python": sys.version.split()[0]} | {p: version(p) for p in ("numpy", "pycocoevalcap", "py_vncorenlp", "pyjnius")}
    env |= {f.name: sha(f.read_bytes()) for f in (vnc / "VnCoreNLP-1.2.jar", vnc / "models/wordsegmenter/wordsegmenter.rdr")}
    head = {"id": P["id"], "mode": a.mode, "prereg": dict(zip(("path", "sha256"), PREREG)),
            "script_sha256": sha(HERE.read_bytes()), "config": cfg, "env": env}
    if a.mode == "gate":
        X = gate(P, cfg)
        body = {k: X[k] for k in ("inputs", "systems", "all_pass")} | {
            "K_COV_dropped": X["dropped"], "subset_statistics_computed": False}
    elif a.mode == "dryrun":
        body = dryrun(cfg)
    elif a.gate:
        body = run(P, cfg, a.gate)
    else:
        raise SystemExit("REFUSED: run needs --gate")
    with open(a.out, "x", encoding="utf-8") as f:  # "x": an existing output is never overwritten
        json.dump(head | body, f, ensure_ascii=False, indent=1)
    for s, r in body.get("systems", {}).items():
        print(s, r.get("K_COV") or f"self-check {r['self_check']['pass']}  F0 {r['F0']['pass']} ({r['F0']['abs_diff']:.1e})")
    print(f"{a.mode}: wrote {a.out}; all_pass = {body.get('all_pass')}")
    return 0 if body.get("all_pass", True) else 1


if __name__ == "__main__":
    sys.exit(main())
