#!/usr/bin/env python3
"""C-ATTR-DEV block 3: the CC-378 W1 ledger recompute (DEVELOPMENT / C-ATTR-DEV, NON-CONFIRMATORY).

For a READER named by a judge line. Not run by its writer. Reads the three block-3 ledgers, keeps only the plain rows
of the ten registered block-3 run ids (the frozen masked3 rows are dropped as each line is parsed, before anything is
kept or printed), recomputes the eight registered rows (v1.1 §7.10, run doc §4) with the scorer's own estimator
(c_attr_score.py cca5e327 `pair`/`summary`, c_attr.py a3bd7b93 `set_columns`/`boot_idx`; commit ca24e13):

  d = mean(a) - mean(b); bootstrap means a[idx].mean(1) - b[idx].mean(1),
  idx = numpy.random.default_rng(0).integers(0, n, (2000, n)), one matrix per set (v1.1 §7.3);
  lo, hi, lo90, hi90 = numpy.percentile(bm, [2.5, 97.5, 5, 95]); p = (1 + #{bm <= 0}) / 2001;
  label (v1.1 §7.4, erratum E1-E2, m = 1): DETECTED iff d >= 2.0 and p <= 0.025; else REVERSED iff hi < 0;
  else NEGLIGIBLE iff -2.0 < lo90 and hi90 < 2.0; else UNRESOLVED,

and compares d, lo, hi, lo90, hi90, p (within 1e-9) and the label with B3_SUMMARY.json (sha256 61bf697b...).
Prints input hashes, the numpy version and one line per row: "<set> <row>  max|diff| <x>  PASS|FAIL". No per-image
value, no caption. `-I` drops the user site: run it with the interpreter of a venv that has numpy (best: the scoring
venv's freeze, since default_rng streams are not promised stable across numpy versions).

  python3 -I -B c_attr_b3_ledger_recompute.py --k5 led/k5.jsonl --ov led/b3_ov_dev_b.jsonl \
      --xm led/b3_xm_dev500.jsonl --summary res/B3_SUMMARY.json
  python3 -I -B c_attr_b3_ledger_recompute.py --selftest          synthetic rows only
"""
from __future__ import annotations

import argparse
import hashlib
import json
import re
import sys
import tempfile
from pathlib import Path

import numpy as np

SUMMARY_SHA = "61bf697b9015a7c4730efb80c63e9266274efcc3a2acf9d366e82661e4d5a01b"  # CC-378 ruling 8
K5_LEDGER_SHA = "87c2ef2cf282e22d69361dd7fe3c18ce58c03f4f3cedd08e77a6f9eede8dc913"  # K5.json inputs (bd9b0158)
TOL, SESOI, ALPHA, B, SEED = 1e-9, 2.0, 0.025, 2000, 0
N = {"ov_dev_b": 925, "xm_dev500": 500}
TEST_SETS = ("ov_test", "xm_test2500", "ktvic_test", "uitviic_test", "f30k_test", "coco_karpathy_test", "nocaps_val")
TEST_PART = re.compile(r"(?:^|[-_.])test(?:[-_.\d]|$)|" + "|".join(TEST_SETS))  # c_attr_score.TEST_NAME, per part


def run_ids(ds: str) -> dict[str, str]:
    """Registered block-3 run ids of one set -> column name (run doc v1.1 §2; c_attr.b3_steps, lmcap_run_id)."""
    return {f"at_lmcap-ri_{ds}-mvi-b1": "lmcap_ri", f"at_lmcap-rand_{ds}-mvi-b1": "lmcap_rand",
            f"at_lmcap-perm_{ds}-mvi-b1": "lmcap_perm",
            f"at_qwen25vl_7b_{ds}-ret_img-k8-first-T1-mvi-b1": "ret_img",
            f"at_qwen25vl_7b_{ds}-rand_img-k8--T1-d0-mvi-b1": "rand_img"}


ROWS = (("lmcap|tau_sel", "lmcap_ri", "lmcap_rand"), ("lmcap|tau_pair", "lmcap_ri", "lmcap_perm"),
        ("lmcap|tau_marg", "lmcap_perm", "lmcap_rand"), ("qwen25vl_7b|tau_sel_img", "ret_img", "rand_img"))
KEYS = ("d", "lo", "hi", "lo90", "hi90", "p")


class Refused(Exception):
    pass


def sha(p: Path) -> str:
    return hashlib.sha256(p.read_bytes()).hexdigest()


def guard(paths) -> None:
    """Refuse any path with a test-set name in any part (the scorer's regex, applied to each path component)."""
    bad = [str(p) for p in paths if any(TEST_PART.search(part) for part in Path(p).parts)]
    if bad:
        raise Refused(f"test-set name in {len(bad)} path(s)")


def columns(paths, ds: str) -> dict[str, np.ndarray]:
    """{column: per-image stripped CIDEr-D} of the registered plain rows of one set, as c_attr.set_columns keeps them
    (dataset, tau -inf, variant plain); masked3 and every other run id are dropped at parse time."""
    want, cols, ids0 = run_ids(ds), {}, None
    for p in paths:
        for line in Path(p).read_text(encoding="utf-8").splitlines():
            if not line.strip():
                continue
            r = json.loads(line)
            if r.get("variant") not in (None, "plain") or r.get("run_id") not in want:
                continue  # frozen masked3 rows (CC-376 ruling 4) and non-registered runs: never kept
            if r.get("dataset") != ds or r.get("tau", "-inf") != "-inf":
                continue
            c = want[r["run_id"]]
            if c in cols:
                raise Refused(f"{ds}: two plain ledger rows for one registered run")
            ids, vals = r["per_image"]["ids"], r["per_image"]["cider_s"]
            if len(vals) != len(ids):
                raise Refused(f"{ds}: score column and id list differ in length")
            ids0 = ids0 or ids
            if ids != ids0:
                raise Refused(f"{ds}: image order differs between runs")
            cols[c] = np.asarray(vals, float)
    if ids0 is not None and len(ids0) != N[ds]:
        raise Refused(f"{ds}: not the full set")
    return cols


def stats(a: np.ndarray, b: np.ndarray, idx: np.ndarray) -> dict:
    """c_attr_score.pair + summary + label (m = 1)."""
    bm = a[idx].mean(1) - b[idx].mean(1)
    lo, hi, lo90, hi90 = np.percentile(bm, [2.5, 97.5, 5, 95])
    s = {"d": float(a.mean() - b.mean()), "lo": float(lo), "hi": float(hi), "lo90": float(lo90), "hi90": float(hi90),
         "p": float((1 + np.sum(bm <= 0)) / (len(bm) + 1))}
    if s["d"] >= SESOI and s["p"] <= ALPHA:
        s["label"] = "DETECTED"
    elif s["hi"] < 0:
        s["label"] = "REVERSED"
    elif s["lo90"] > -SESOI and s["hi90"] < SESOI:
        s["label"] = "NEGLIGIBLE"
    else:
        s["label"] = "UNRESOLVED"
    return s


def compare(sets: dict[str, list], summary: dict) -> list[tuple[str, str, str, bool]]:
    """[(set, row, max|diff| text, ok)] for the eight registered rows; a missing piece is a FAIL with no value."""
    out = []
    for ds, paths in sets.items():
        try:
            cols = columns(paths, ds)
        except (Refused, KeyError, ValueError, TypeError, OSError):
            out += [(ds, k, "-", False) for k, _x, _y in ROWS]
            continue
        n = len(next(iter(cols.values()))) if cols else 0
        idx = np.random.default_rng(SEED).integers(0, n, (B, n)) if n else None
        stored = summary.get("sets", {}).get(ds, {})
        for k, x, y in ROWS:
            ref = stored.get("rows", {}).get(k)
            if x not in cols or y not in cols or ref is None or stored.get("n") != n:
                out.append((ds, k, "-", False))
                continue
            s = stats(cols[x], cols[y], idx)
            diff = max(abs(s[c] - float(ref[c])) for c in KEYS)
            out.append((ds, k, f"{diff:.3e}", diff <= TOL and s["label"] == ref["label"]))
    return out


def main(a) -> int:
    paths = {"k5": Path(a.k5), "ov": Path(a.ov), "xm": Path(a.xm), "summary": Path(a.summary)}
    guard(paths.values())
    if sha(paths["summary"]) != SUMMARY_SHA:
        raise Refused("B3_SUMMARY.json is not the file of record (61bf697b)")
    if sha(paths["k5"]) != K5_LEDGER_SHA:
        raise Refused("k5.jsonl is not the ledger named in K5.json (87c2ef2c)")
    for name in ("k5", "ov", "xm"):
        print(f"input {paths[name].name} sha256 {sha(paths[name])}")
    print(f"numpy {np.__version__}")
    summary = json.loads(paths["summary"].read_text(encoding="utf-8"))
    res = compare({"ov_dev_b": [paths["k5"], paths["ov"]], "xm_dev500": [paths["xm"]]}, summary)
    for ds, k, diff, ok in res:
        print(f"{ds} {k}  max|diff| {diff}  {'PASS' if ok else 'FAIL'}")
    bad = sum(not ok for *_x, ok in res)
    print("ALL PASS (8 rows)" if not bad and len(res) == 8 else f"STOP: {bad} FAIL; the matter goes to a judge (W1)")
    return 0 if not bad and len(res) == 8 else 1


def selftest() -> None:
    """Synthetic rows only: estimator on planted columns, masked3 and stray rows ignored, refusals, PASS/FAIL."""
    rng = np.random.default_rng(7)
    with tempfile.TemporaryDirectory() as t:
        t = Path(t)

        def ledger(name, ds, cols, extra=()):
            ids = [f"i{j}" for j in range(N[ds])]
            rows = [{"dataset": ds, "run_id": rid, "model": "m", "arm": "a", "per_image": {"ids": ids, "cider_s": v}}
                    for rid, v in cols.items()]
            rows += [dict(r, variant="masked3", per_image={"ids": ids, "cider_s": [1e6] * N[ds]}) for r in rows]
            rows += list(extra)
            (t / name).write_text("".join(json.dumps(r) + "\n" for r in rows), encoding="utf-8")
            return t / name

        cols = {}
        for ds in N:
            base = rng.normal(30, 10, N[ds])
            cols[ds] = {"lmcap_ri": base + 17, "lmcap_rand": base,
                        "lmcap_perm": base + np.where(np.arange(N[ds]) % 2, 0.5, -0.5),
                        "ret_img": base + rng.normal(2, 5, N[ds]), "rand_img": base}
        rid = {ds: {c: r for r, c in run_ids(ds).items()} for ds in N}
        ov = cols["ov_dev_b"]
        stray = {"dataset": "ov_dev_b", "run_id": "c2_qwen25vl_7b_ov_dev_b-zs", "per_image": {"ids": [], "cider_s": []}}
        k5 = ledger("k5.jsonl", "ov_dev_b", {rid["ov_dev_b"][c]: list(ov[c]) for c in ("lmcap_ri", "lmcap_rand")})
        ovp = ledger("b3_ov.jsonl", "ov_dev_b", {rid["ov_dev_b"][c]: list(ov[c])
                                                 for c in ("lmcap_perm", "ret_img", "rand_img")}, [stray])
        xm = ledger("b3_xm.jsonl", "xm_dev500", {rid["xm_dev500"][c]: list(v) for c, v in cols["xm_dev500"].items()})
        sets = {"ov_dev_b": [k5, ovp], "xm_dev500": [xm]}

        c = columns(sets["ov_dev_b"], "ov_dev_b")
        assert sorted(c) == sorted(ov) and np.array_equal(c["lmcap_ri"], ov["lmcap_ri"]), "masked3 or stray row kept"
        idx = np.random.default_rng(0).integers(0, N["ov_dev_b"], (B, N["ov_dev_b"]))
        s = stats(c["lmcap_ri"], c["lmcap_rand"], idx)  # constant +17 per image
        assert abs(s["d"] - 17) < 1e-9 and abs(s["lo"] - 17) < 1e-9 and abs(s["hi90"] - 17) < 1e-9
        assert s["p"] == 1 / 2001 and s["label"] == "DETECTED", "floor of p or DETECTED rule"
        s = stats(c["lmcap_rand"], c["lmcap_ri"], idx)
        assert s["p"] == 1.0 and s["label"] == "REVERSED"
        s = stats(c["lmcap_perm"], c["lmcap_rand"], idx)
        assert abs(s["d"]) < 0.01 and s["label"] == "NEGLIGIBLE"
        assert stats(np.full(5, 2.0), np.zeros(5), np.zeros((B, 5), int))["label"] == "DETECTED"  # d = 2.0 inclusive
        assert stats(np.full(5, 1.99), np.zeros(5), np.zeros((B, 5), int))["label"] == "NEGLIGIBLE"  # below 2.0

        good = {"sets": {}}
        for ds, ps in sets.items():
            cc = columns(ps, ds)
            ix = np.random.default_rng(0).integers(0, N[ds], (B, N[ds]))
            good["sets"][ds] = {"n": N[ds], "rows": {k: stats(cc[x], cc[y], ix) for k, x, y in ROWS}}
        assert all(ok for *_x, ok in compare(sets, good)) and len(compare(sets, good)) == 8
        bad = json.loads(json.dumps(good))
        bad["sets"]["xm_dev500"]["rows"]["lmcap|tau_pair"]["hi90"] += 1e-6
        r = compare(sets, bad)
        assert [k for ds, k, _d, ok in r if not ok] == ["lmcap|tau_pair"], "a 1e-6 difference must FAIL"
        bad = json.loads(json.dumps(good))
        bad["sets"]["ov_dev_b"]["rows"]["lmcap|tau_marg"]["label"] = "UNRESOLVED"
        assert sum(not ok for *_x, ok in compare(sets, bad)) == 1, "a label difference must FAIL"
        r = compare({"ov_dev_b": [k5], "xm_dev500": [xm]}, good)  # perm and Qwen arms missing on OV-dev-B
        assert [(k, d) for ds, k, d, ok in r if not ok] == [(k, "-") for k in
                                                           ("lmcap|tau_pair", "lmcap|tau_marg", "qwen25vl_7b|tau_sel_img")]
        dup = ledger("dup.jsonl", "xm_dev500", {rid["xm_dev500"]["lmcap_ri"]: list(cols["xm_dev500"]["lmcap_ri"])})
        assert all(not ok for *_x, ok in compare({"xm_dev500": [xm, dup]}, good)), "a duplicate run must FAIL"
        for p in ("/x/ov_test/k5.jsonl", "/x/test/k5.jsonl", "/x/led_test.jsonl", "/x/nocaps_val/a.jsonl"):
            try:
                guard([p])
                raise AssertionError(f"not refused: {p}")
            except Refused:
                pass
        guard([k5, ovp, xm, Path("/x/c_attr_score_b3/res/B3_SUMMARY.json")])
    print("selftest ok: estimator, p floor, labels at 2.0, masked3/stray rows ignored, duplicate and missing rows FAIL, "
          "1e-6 and label differences FAIL, test-set paths refused")


if __name__ == "__main__":
    ap = argparse.ArgumentParser(description=__doc__.split("\n")[0])
    ap.add_argument("--selftest", action="store_true")
    for f in ("k5", "ov", "xm", "summary"):
        ap.add_argument(f"--{f}")
    args = ap.parse_args()
    if args.selftest:
        selftest()
        sys.exit(0)
    if not all((args.k5, args.ov, args.xm, args.summary)):
        ap.error("--k5, --ov, --xm and --summary are required")
    try:
        sys.exit(main(args))
    except (Refused, OSError) as e:
        print(f"REFUSED: {e}")
        sys.exit(2)
