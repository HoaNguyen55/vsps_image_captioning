#!/usr/bin/env python3
"""POST HOC rows C1, C2 (COCO only), B1 and B2 of POSTHOC_ROWS_PLAN_v1_1.md, under CC-315 (b), conditions R1-R4.

  ~/.venvs/c_stage1_lists/bin/python -I -B scripts/posthoc_1110/posthoc_rows.py ROW --ids IDS --out OUT

ROW is c1, c2, b1 or b2; --ids and --out must be the planned files (ROWS). One row per process, each row once. The
registered estimators are imported after the audit hook is armed and are called unchanged. A row carries no verdict
and changes no registered result. Stdout carries no estimate.
"""
from __future__ import annotations

import argparse
import hashlib
import json
import os
import re
import sys
import time
from pathlib import Path

import numpy as np

sys.pycache_prefix = os.devnull  # no .pyc is read: the sha-checked source is what runs and what the hook logs

RUN = "/mnt/d/vsps_image_captioning"
IDS = f"{RUN}/manuscript/directions/integrity_2026-11-10/ids"
POST = f"{RUN}/.session_backup/2026-11-10/posthoc"  # R4
M3C, M1E, M4B = (f"{RUN}/.session_backup/machines/{m}/root/outputs/{d}"
                 for m, d in (("M3", "c_test"), ("M1", "c_en"), ("M4", "b1_scaling")))
HOME = os.path.expanduser("~")
SEALED = f"{HOME}/.vsps_sealed"
SCOPE = [RUN, "/mnt/d/vsps_papers", f"{HOME}/vsps_w25k1", f"{HOME}/c_pvr_w25_in", SEALED]  # R1: the data roots
EXEMPT = sorted({f"{p}/lib" for p in (sys.prefix, sys.base_prefix)})  # R1: interpreter, stdlib and venv paths
DENY = re.compile(r"annotation-test|preds|caption")  # R1: matched on the file name, allow-listed or not
SELF = os.path.realpath(__file__)
LOADED = {"score_t", "ctest", "cen_score", "b1"}
TOL = 1e-9  # plan rule 6
NOTE = "per-image scores as stored; document frequencies not recomputed"  # R2, plan rule 4
DLH = ("d", "lo", "hi")
FROZEN = [f"{RUN}/manuscript/prereg/2026-10-22_c_stage2/frozen_config.json",
          "2f0c32be7720b672f6e4aae229aba69da8742e0f9e32d34c5137e985ea36aa16"]
ROWS = {  # plan section 3: pinned id list, n before and after, output, inputs; every sha256 is checked before a read
    "c1": {"ids": [f"{IDS}/pin_c_ov_test_ret_union.txt",
                   "8c75134e7c4bb25faef05876c459da1a5b5c90d4cbfdc11a73c362ba4e505bc9"],
           "n": [1941, 1929], "out": f"{POST}/c1_ov_test_posthoc.json",
           "inputs": {"ledger": [f"{M3C}/ledger_ov_test_1941.jsonl",
                                 "50878193f1cfc473786ca86e4cc5eb59f13720faa9d97ea52206dd36c0daa154"],
                      "decide": [f"{M3C}/decide_ov.json",
                                 "9bcad4989adcfd2d43e2a39a2b9e09835795c1a4480649d27b6b15a8d56806da"],
                      "lists": [f"{RUN}/manuscript/prereg/2026-10-22_c_stage1/lists.json",
                                "5c479f03e8be544f4cd12b5d997b5dc92b6c622df061760cd02f6ba82f6b4371"],
                      "frozen": FROZEN,
                      "code": [f"{RUN}/scripts/c_test/score_t.py",
                               "de94294256789ebc3ad960162f468e8233597866013d5b4f9ffbccac7a18e4b5"]}},
    "c2": {"ids": [f"{IDS}/pin_c2_coco_test_ret_union.txt",
                   "c2b749ec07865949f326bc4dc7d404a8fd2c23e1f5fe7697fbdf25e31dc495a1"],
           "n": [5000, 4999], "out": f"{POST}/c2_coco_posthoc.json",  # R3: COCO only
           "inputs": {"ledger": [f"{M1E}/ledger_coco_test_5000.jsonl",
                                 "58074daee2ffb20de83f41af2662cdd5d9ec120efb9deaf038103eae52c4b5f0"],
                      "decide": [f"{M1E}/decide_coco_test.json",
                                 "efc6eac7fe5d7f1941826dcd81942608cf87c274c06bbce7d7994f9b4af15855"],
                      "frozen": FROZEN,
                      "code": [f"{RUN}/scripts/c_en/cen_score.py",
                               "68a700ab86506e34e092dfe814ea5404fadf9cd564ede93752834849e5ebd82a"]}},
    "b1": {"ids": [f"{IDS}/pin_k_ktvic_dev300.txt",
                   "dd284b51ce14ae52b28ccddce99fadec0649f2bdb838dcc4959bb2e5d4e10aa0"],
           "n": [300, 293], "out": f"{POST}/b1_mask7_posthoc.json",
           "inputs": {"ledger": [f"{M4B}/ledger.json",
                                 "4afa3f44fa2da731f6fa6b8e02182b40328340f455443e334db36a4f1faab394"],
                      "decide": [f"{M4B}/decide.json",
                                 "b44a76fe6456e6c037fc5578b701f949e73515973b5f68263236e65d65addaf9"],
                      "code": [f"{RUN}/scripts/b1_scaling/b1.py",
                               "e747205ead426fb0747be3e8aa60649b0e05e139e4d75a53827f049a6aa2d19a"],
                      "probe": [f"{RUN}/scripts/scaling_probe.py",
                                "0342f6e59a6c6d1a89be0fac3ad87bafff76648415c9cf532b5eddc405abac28"]}},
    "b2": {"ids": [f"{IDS}/pin_k_ktvic_test.txt",
                   "a4c7d272dfe0debe9b317d50749096e3e7b202a6262fdbc9c33fe6ba5d347813"],
           "n": [558, 542], "out": f"{POST}/b2_ktvic_test_posthoc.json",
           "identity": {  # seed: [mean over the 558 images at four decimals (plan B2), headline result sha256]
               "s42": [148.6640, "ea38b60e7dc5c243356b98b8ac19b91165cb93ecb6f8a6f2badcbeb7053dbfa9"],
               "s43": [148.0630, "ce8576a440d55888c2954070cef7c916f8030de94f5e171d9e6a02aef79137eb"],
               "s44": [147.9615, "723d97653f895e98306a4dbbbf85a1dcd1d6df9012422711bfd85f98b2cca2ad"]},
           "inputs": {"ledger": [f"{RUN}/data/results/b_posthoc/b_posthoc_mbr3_run.json",
                                 "7a51aadfa5790b28ab5155cc44f1cb548655fc839ba64348bc8540b8bf3d229f"],
                      "headline": [f"{RUN}/.session_backup/2026-10-15/paperA_keys/cider_3seed_mean.json",
                                   "f6f68d02f4f923657365529852d9a6064d97cc819bc94f3de6f9c442c4928b49"]}},
}
RESCAP = ("rescap/__init__.py rescap/metrics.py rescap/repro.py rescap/vocab.py rescap/chair.py "
          "rescap/svp/__init__.py rescap/svp/entailment.py rescap/svp/matching.py rescap/vi/__init__.py "
          "rescap/vi/classifier.py rescap/vi/lexicon.py rescap/vi/color.py scripts/rl_reward.py ")
STAGE1 = ("manuscript/prereg/2026-10-22_c_stage1/SHA256SUMS scripts/c_stage1/build_memory.py "
          "scripts/c_stage1/decode_icl.py scripts/c_stage1/guard.py scripts/c_stage1/score.py "
          "scripts/c_stage2/stage2.py scripts/lb/decode_hf_vlm.py scripts/g2b/decode_qwen3vl.py "
          "scripts/match_openviic.py ")
CHAIN = {  # R1: the files the registered import chain opens besides the listed inputs (repo-relative, exact)
    "c1": (RESCAP + STAGE1 + "scripts/c_test/ctest.py scripts/c_test/make_ov_test_manifest.py "
           "scripts/c_test/make_xm_threeref108.py scripts/c_stage2/c_stage2_job.sh scripts/c_stage2/decide2.py "
           "scripts/c_stage2/decode2.py scripts/c_stage2/guard2.py scripts/c_stage2/score2.py scripts/plan_f1.py "
           "scripts/object_prf.py manuscript/prereg/2026-10-22_c_stage2/SHA256SUMS "
           "manuscript/prereg/2026-10-22_c_stage2/ov_test_dev299_neardup_files.txt "
           "manuscript/prereg/2026-10-25_c_test/SHA256SUMS manuscript/prereg/2026-10-25_c_test/PREREG.md "
           "manuscript/prereg/2026-10-25_c_test/ov_test_files.tsv "
           "manuscript/prereg/2026-10-25_c_test/ov_test_primary1941.txt "
           "manuscript/prereg/2026-10-25_c_test/xm_test2500_threeref108.txt").split(),
    "c2": (RESCAP + STAGE1 + "scripts/c_en/cen_decode.py scripts/c_en/cen_fetch.py scripts/c_en/cen_memory.py "
           "scripts/score_coco_probe.py data/coco_probe/chair_synonyms.txt").split(),
    "b1": (RESCAP + "scripts/object_prf.py scripts/checkpoint_resume_hook.py scripts/rl_report.py "
           "scripts/evaluate.py scripts/train_rl.py scripts/rl_policy.py scripts/train_stage2.py").split(),
    "b2": [],
}


def sha(p: str) -> str:
    return hashlib.sha256(Path(p).read_bytes()).hexdigest()


def under(p: str, roots: list[str]) -> bool:
    return any(p == r or p.startswith(r + os.sep) for r in roots)


def refusal(p: str, allow: set[str]) -> str | None:
    """R1: why an open of the resolved path p stops the row; None when it may proceed."""
    if under(p, EXEMPT):
        return None
    if under(p, [SEALED]) or DENY.search(os.path.basename(p)):
        return "a sealed, annotation-test, preds or caption path"
    if under(p, SCOPE) and p not in allow:
        return "under a data root and not on the allow-list"
    return None


def arm(allow: set[str], log: list[str], bad: list[str]) -> None:
    """R1: every open under a data root is logged; a refused open stops the row before the file is touched.
    Ceiling: opens by native code or by a child process are not seen; the rows use neither."""
    def hook(event: str, args: tuple) -> None:
        if event != "open" or not isinstance(args[0], (str, bytes, os.PathLike)):
            return
        p = os.path.abspath(os.fsdecode(args[0]))
        p = p if under(p, [SEALED]) else os.path.realpath(p)  # a sealed path is refused without an lstat inside it
        if under(p, SCOPE):
            log.append(p)
        why = refusal(p, allow)
        if why:
            bad.append(f"{p}: {why}")
            raise SystemExit(f"R1 STOP: open of {p} refused: {why}")

    sys.addaudithook(hook)


def kept(order: list[str], drop: list[str]) -> list[str]:
    """The pinned list is the only exclusion source; each pinned id must be in the set, once."""
    if len(set(drop)) != len(drop) or not set(drop) <= set(order):
        raise SystemExit("a pinned id is repeated or is not in the scored set")
    return [i for i in order if i not in set(drop)]


def same(what: str, got: list[float], want: list[float], tol: float = TOL) -> dict:
    """Plan rule 6: the registered number is reproduced within tol, or the row stops."""
    gap = float(np.max(np.abs(np.array(got, float) - np.array(want, float))))
    if not gap <= tol:
        raise SystemExit(f"identity check failed: {what} (largest difference {gap:.3g})")
    return {"what": what, "max_abs_diff": gap, "tol": tol}


def load(spec: dict, key: str) -> dict:
    return json.loads(Path(spec["inputs"][key][0]).read_text(encoding="utf-8"))


def c1(spec: dict, drop: list[str]) -> dict:
    """Plan C1: P1 (pooled ret - rand, S.boot) and P2 (S.pcm_ci per backbone) from decide2.gate on the kept queries."""
    sys.path.insert(0, f"{RUN}/scripts/c_test")
    import score_t as ST

    cfg, models, dec = ST.S2.frozen(), ST.C.MODELS, load(spec, "decide")
    order = ST.T.scored_ids("ov_test_1941", ST.C.load_lists(Path(spec["inputs"]["lists"][0])))
    keep = kept(order, drop)
    raw = ST.aliased(ST.S.latest(ST.read_jsonl(Path(spec["inputs"]["ledger"][0]))), "ov_test")

    def p1_p2(rows: list[dict]) -> dict:
        g = ST.DD.gate(rows, cfg, "ov_test")
        return {"P1": g["pooled_vs_rand"], "P2": {m: g["per_model"][m]["pcm_vs_zs"] for m in models}}

    full = p1_p2(ST.reorder(raw, order))
    ident = [same("all 1,941 = decide_ov.json::P1", [full["P1"][k] for k in DLH], [dec["P1"][k] for k in DLH])]
    ident += [same(f"all 1,941 = decide_ov.json::P2.{m}", [full["P2"][m][k] for k in DLH],
                   [dec["P2"][m][k] for k in DLH]) for m in models]
    return {"n_before": len(order), "n_after": len(keep), "identity": ident,
            "estimate": p1_p2(ST.reorder(raw, keep, subset=True)),
            "registered": {"P1": dec["P1"], "P2": dec["P2"]}}


def c2(spec: dict, drop: list[str]) -> dict:
    """Plan C2 (COCO): pooled ret - rand in cider_ptb, ci(d[sel], draws(n)) as cen_score.py:214-228."""
    sys.path.insert(0, f"{RUN}/scripts/c_en")
    import cen_score as CS

    cfg, models, p1 = CS.S2.frozen(), CS.D.C.MODELS, load(spec, "decide")["P1_EN"]
    rows = [json.loads(x) for x in Path(spec["inputs"]["ledger"][0]).read_text().splitlines() if x]
    one = CS.one_set(rows, "coco_test", "coco_test_5000")  # also refuses rows that are not on one id order
    ids = rows[0]["per_image"]["ids"]
    kept(ids, drop)
    d = np.mean([CS.arr(CS.get(rows, CS.D.spec(cfg, "coco_test", m, "ret")["run_id"], cfg["models"][m]["tau"])) -
                 CS.arr(CS.get(rows, CS.D.spec(cfg, "coco_test", m, "rand")["run_id"], cfg["models"][m]["tau"]))
                 for m in models], 0)
    sel = ~np.isin(ids, drop)
    ident = [same("one_set pooled = decide_coco_test.json::P1_EN", [one["pooled"][k] for k in DLH],
                  [p1[k] for k in DLH]),
             same("subset form, nothing excluded = decide_coco_test.json::P1_EN",
                  [CS.ci(d, CS.draws(len(d)))[k] for k in DLH], [p1[k] for k in DLH])]
    return {"n_before": len(ids), "n_after": int(sel.sum()), "identity": ident,
            "estimate": CS.ci(d[sel], CS.draws(int(sel.sum()))), "registered": {"P1_EN": p1}}


def b1(spec: dict, drop: list[str]) -> dict:
    """Plan B1: the registered sensitivity formula (b1.py:472-489) with a set in place of image 2004."""
    sys.path.insert(0, f"{RUN}/scripts/b1_scaling")
    import b1 as B

    dec, rows, n = load(spec, "decide"), load(spec, "ledger")["rows"], B.SP.DEV_N
    common = {tuple(v["ids"]) for v in rows.values() if "ids" in v}
    if len(common) != 1 or len(next(iter(common))) != n:
        raise SystemExit("b1: the rows do not carry one common id list of the dev images")
    ids = list(common.pop())
    idx = np.random.default_rng(B.SP.BOOT_SEED).integers(0, n, (B.SP.B, n))
    x = np.log2(list(B.LEVELS.values()))
    complete = [s for s in B.SEEDS if all(B.run_name(s, lv) in rows for lv in B.LEVELS)]
    cid = {(s, lv): np.array(rows[B.run_name(s, lv)]["cider_s"], float) for s in complete for lv in B.LEVELS}

    def slope(out: list[str]) -> list[float]:
        j = [ids.index(i) for i in out]
        keep, M = ~np.isin(np.arange(n), j), ~np.isin(idx, j)
        Y = np.array([[cid[s, lv][keep].mean() for lv in B.LEVELS] for s in complete])
        D = np.array([[(cid[s, lv][idx] * M).sum(1) / M.sum(1) for lv in B.LEVELS] for s in complete])
        return [float(B.fe_slope(x, Y)), *B.ci(B.fe_slope(x, D))]

    twin = dec["sensitivity_minus_dev_twin"]["pooled"]
    ident = [same("empty set = decide.json::P-B1", slope([]), [dec["P-B1"]["b"], *dec["P-B1"]["ci95"]]),
             same("image 2004 alone = decide.json::sensitivity_minus_dev_twin.pooled", slope([B.DEV_TWIN]),
                  [twin["b"], *twin["ci95"]])]
    keep = kept(ids, drop)
    b, lo, hi = slope(drop)
    return {"n_before": n, "n_after": len(keep), "identity": ident, "estimate": {"b": b, "ci95": [lo, hi]},
            "registered": {"P-B1": dec["P-B1"], "sensitivity_minus_dev_twin.pooled": twin}}


def b2(spec: dict, drop: list[str]) -> dict:
    """Plan B2: per seed the mean of the stored per-image values over the kept images, then mean and sample SD."""
    rec = load(spec, "ledger")
    ids = rec["test_ids"]
    kept(ids, drop)
    per = {s: np.array(rec["per_image_cider_x100"][s], float) for s in spec["identity"]}  # the seeds, never "mbr"

    def mean_sd(sel: np.ndarray) -> dict:
        m = {s: float(v[sel].mean()) for s, v in per.items()}
        return {"per_seed": m, "mean": float(np.mean(list(m.values()))), "sd": float(np.std(list(m.values()), ddof=1))}

    every = mean_sd(np.ones(len(ids), bool))
    ident = []
    for s, (mean4, result) in spec["identity"].items():
        if len(per[s]) != len(ids) or rec["F0"][s]["result_sha256"] != result:
            raise SystemExit(f"b2: {s} is not the per-image list of the headline result file (result_sha256)")
        ident.append(same(f"{s}: mean over all images at four decimals", [every["per_seed"][s]], [mean4], 5e-5))
    keep = ~np.isin(ids, drop)
    return {"n_before": len(ids), "n_after": int(keep.sum()), "identity": ident, "estimate": mean_sd(keep),
            "scores_computed_on": f"all {len(ids)} images",  # CC-315 Ruling 7
            "registered": {"verdict": None}, "three_seed_mean_sd_all_images": every}


FN = {"c1": c1, "c2": c2, "b1": b1, "b2": b2}


def run(row: str, spec: dict) -> None:
    out = Path(spec["out"])
    if out.exists():
        raise SystemExit(f"{out} exists; a row runs once (R4)")
    if LOADED & set(sys.modules):
        raise SystemExit("registered code is already imported; one row per process (R1)")
    files = {**spec["inputs"], "ids": spec["ids"]}
    log: list[str] = []
    bad: list[str] = []
    arm({os.path.realpath(p) for p, _h in files.values()} | {os.path.realpath(out), SELF} |
        {f"{RUN}/{c}" for c in CHAIN[row]}, log, bad)
    for k, (p, h) in files.items():
        if sha(p) != h:
            raise SystemExit(f"{row}: {k} {p}: sha256 differs from its pin")
    drop = Path(spec["ids"][0]).read_text(encoding="utf-8").split()
    res = FN[row](spec, drop)
    if [res["n_before"], res["n_after"]] != spec["n"]:
        raise SystemExit(f"{row}: n {res['n_before']} -> {res['n_after']} is not the planned {spec['n']}")
    rec = {"row": row, "label": "POST HOC", "verdict": None,
           "statement": "post hoc row, no verdict; this row does not alter the registered result. 'registered' is "
                        "copied unchanged from the registered decide file (c1, c2, b1); b2 has no registered "
                        "verdict and no decide file",
           "scores": NOTE, "utc": time.strftime("%Y-%m-%dT%H:%M:%SZ", time.gmtime()),
           "script": {"path": SELF, "sha256": sha(SELF)},
           "inputs": {k: {"path": p, "sha256": h} for k, (p, h) in spec["inputs"].items()},
           "pinned_ids": {"path": spec["ids"][0], "sha256": spec["ids"][1], "n": len(drop)}, **res, "opened": log}
    if bad:
        raise SystemExit(f"R1 STOP: refused opens: {bad}")
    out.parent.mkdir(exist_ok=True)
    with open(out, "x", encoding="utf-8") as f:
        text = json.dumps(rec, indent=1) + "\n"
        f.write(text)
    print(f"posthoc-{row}: wrote {out} sha256 {hashlib.sha256(text.encode()).hexdigest()}; n {spec['n'][0]} -> "
          f"{spec['n'][1]}; {len(res['identity'])} identity checks PASS; POST HOC, no verdict")


def main() -> None:
    ap = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    ap.add_argument("row", choices=sorted(ROWS))
    ap.add_argument("--ids", type=Path, required=True)
    ap.add_argument("--out", type=Path, required=True)
    a = ap.parse_args()
    spec = ROWS[a.row]
    if str(a.ids.resolve()) != spec["ids"][0] or str(a.out.resolve()) != spec["out"]:
        raise SystemExit(f"{a.row}: --ids and --out must be the planned {spec['ids'][0]} and {spec['out']}")
    run(a.row, spec)


if __name__ == "__main__":
    main()
