#!/usr/bin/env python3
"""Paper C test (TEST, ONE LOOK PER SET): ledger rows of the four scored sets, local verified precision on
XM-test2500, `decide --phase ov|xm|xmb`, and the CC-103b dry check (CC-103 E2 (a), (b)).
Prereg manuscript/prereg/2026-10-25_c_test/PREREG.md §6-§10, §13 items 5-7 and 10.

  python scripts/c_test/score_t.py --selftest                                                    CPU, no data
  NCS_DATA=<dir holding vncorenlp/> python scripts/c_test/score_t.py --dry      CPU, local, stage-2 dev artefacts
  python scripts/c_test/score_t.py score --set S --runs R ... --zs Z Z --cache C --lists L --exemplars X \
      --ledger-dir D                                                                                    CPU (M3)
  python scripts/c_test/score_t.py decide --phase ov|xm --ledger-dir D --lists L --out J                CPU (M3)
  python scripts/c_test/score_t.py verified --runs R ... --zs Z Z --cache C --lists L --labels OIV7 --desc CSV \
      --ledger V                                                                     CPU, local only (refuses on M3)
  python scripts/c_test/score_t.py decide --phase xmb --verified V --xm-decide J --lists L --out J2   CPU, local
The stage-2 scorer and decide functions are used unchanged (score2.set_rows, decide2.gate/ratio/paired/dose/s3).
Decide reads the ct_ ledgers through an in-memory ct_ -> c2_ alias, so decide2's run-id lookups apply unchanged; it
re-indexes every row to the pinned image order (W6) before any bootstrap. Each decide phase runs once. No caption is
read or printed by decide; the ledgers hold numbers and ids only.
"""
from __future__ import annotations

import argparse
import json
import os
import subprocess
import sys
import tempfile
from pathlib import Path

import numpy as np

sys.path.insert(0, str(Path(__file__).resolve().parent))
import ctest as T  # noqa: E402  pins (test prereg, stage-2 and stage-1 code), sets, refusal

S2, C, G, lb = T.S2, T.C, T.G, T.lb
import decide2 as DD  # noqa: E402  stage-2 module, sha-checked by ctest
import score2 as SC2  # noqa: E402

S = SC2.S
SESOI, PCM_FLOOR, VP_FLOOR = 2.0, -1.0, -1.0  # §7.1, §7.4, §7.5
EXPECTED_VS_ZS = 10.0  # §8.2 S-zf, pooled, stated only
QWEN, IVL = "qwen25vl_7b", "internvl3_8b"
STAMP_KEYS = {"label", "c_schema", "c_prereg_sha256", "frozen_config_sha256", "utc", "inputs", "scored_set",
              "design_sha256"}
SCOPE = {  # §9.2, applied mechanically to the OV-test 1,941 P1b rows, only if P1 passes
    "qwen_main_internvl_not_detected": "carried mainly by Qwen2.5-VL; not detected for InternVL3",
    "qwen_main_internvl_smaller": "carried mainly by Qwen2.5-VL; smaller for InternVL3",
    "both": "present for both backbones",
    "internvl_main_qwen_below_sesoi": "carried mainly by InternVL3; not at the SESOI for Qwen2.5-VL",
    "neither_at_sesoi": "not carried by either backbone at the SESOI"}
BLOCKS = {"ov": ("ov_test", "ov_test_1941", "ov_test_2001"), "xm": ("xm_test2500", "xm_test2500", "xm_test2392")}
LOCAL = T.ROOT / ".session_backup"
MIRROR = LOCAL / "machines/M3/root/outputs"
DEV_PINS = {"ledger": (MIRROR / "c_stage2/ledger.jsonl",
                       "be716482c6f934e975bdbc58927cfc42a4c0ff589c9c5f95affd67c03eac0938"),
            "verified": (LOCAL / "2026-10-22/c_stage2/final/verified.jsonl",
                         "d69bddadfc686d47f4c89bd68ae8306679442288c4a6c0a8dcb7f62d0d7208b1"),
            "df": (LOCAL / "2026-10-22/c_stage2/final/decide_final.json",
                   "92a1f0e992cb974f0d2dfc59a765d1adbfa89338a6d7eed267edd583e2cd162b"),
            "ov_dev_ann": (LOCAL / "2026-10-22/c_stage2/subsets/uit-openviic-annotation-dev.json",
                           "550cfe06b06084976e81286531f7f4e52bea717e29004c699ccaf1e48919bdff")}
LISTS = T.ROOT / "manuscript/prereg/2026-10-22_c_stage1/lists.json"


def read_jsonl(p: Path) -> list[dict]:
    return [json.loads(x) for x in Path(p).read_text(encoding="utf-8").splitlines() if x]


def norm(x):
    return json.loads(json.dumps(x, default=lambda o: o.item() if hasattr(o, "item") else str(o)))


# ------------------------------------------------------------------------------------------------ score (M3)
def score_rows(ds: str, name: str, ids: list[str], runs: list[dict], zs_by: dict, refs: dict, ctx: dict, ex: dict,
               cfg: dict) -> list[dict]:
    """score2.set_rows on one scored set: predictions, examples and references cut to the set (its own df, §6.2),
    the dose cuts of that set (fixed at the exemplars step), NN rows renamed ct_nn_ on a test set."""
    keep = set(ids)

    def cut(r):
        return {**r, **{k: {i: v for i, v in r[k].items() if i in keep}
                        for k in ("predictions", "exemplars", "hit_max") if isinstance(r.get(k), dict)}}

    # a test exemplars file holds the cuts of every scored set; a stage-2 file (the replay) only its set's cuts
    cuts = ex["scored_dose_cuts"][name] if "scored_dose_cuts" in ex else ex["dose_tertile_cuts"][ds]
    rows = SC2.set_rows(ds, [cut(r) for r in runs], {m: cut(z) for m, z in zs_by.items()},
                        {i: refs[i] for i in ids}, {**ctx, "ex": {**ex, "dose_tertile_cuts": {ds: cuts}}, "cfg": cfg})
    if ds in T.SETS:
        rows = [{**r, "run_id": r["run_id"].replace("c2_nn_", "ct_nn_", 1)} for r in rows]
    return [{**r, "scored_set": name} for r in rows]


def cmd_score(a) -> None:
    ds = a.set
    lists = C.load_lists(a.lists)
    cfg = S2.frozen()
    E4, PA, PTB = SC2.kit2(a.kit_b)
    if lb.sha256_file(E4.VNC / "VnCoreNLP-1.2.jar") != S.JAR_SHA256:
        raise SystemExit(f"{E4.VNC}/VnCoreNLP-1.2.jar is not the jar of Paper B's protocol card")
    runs, zss = [G.read_preds(p) for p in a.runs], [G.read_preds(p) for p in a.zs]
    want = {T.spec_t(cfg, ds, m, arm)["run_id"] for m in C.MODELS for arm in T.MAIN}
    got = {r["run_id"] for r in runs + zss}
    if got != want or any(r.get("c_schema") != T.SCHEMA or r["dataset"] != ds for r in runs + zss) or \
            {z["spec"]["arm"] for z in zss} != {"zs"}:
        raise SystemExit(f"score: the runs must be exactly the 8 test runs of {ds}")
    for z in zss:
        T.zs_ok_t(z, z["model"], ds)
    ex = C.load_exemplars(a.exemplars, a.lists)
    if ex.get("set") != ds or ex.get("c_schema") != T.SCHEMA:
        raise SystemExit(f"{a.exemplars}: not the test example lists of {ds}")
    refs = T.references_t(ds, lists)
    ctx = {"cache": S.load_cache(a.cache), "caps": C.memory_captions(lists), "segment": E4.rdr, "E4": E4, "PA": PA,
           "PTB": PTB, "inputs": {"lists_sha256": lb.sha256_file(a.lists), "exemplars_sha256": S2.sha_file(a.exemplars),
                                  "cache_sha256": {Path(p).name: lb.sha256_file(Path(p)) for p in a.cache}}}
    for name in [n for n, s in T.SCORED.items() if s == ds]:
        out = T.out_ok(a.ledger_dir / f"ledger_{name}.jsonl")
        if out.exists():  # a crash resume keeps the rows already written (§7.6)
            print(f"{out.name} exists; kept")
            continue
        stamp = {"label": T.LABEL, "c_schema": T.SCHEMA, "c_prereg_sha256": T.T_PINS[T.PREREG],
                 "frozen_config_sha256": S2.PINS[S2.FROZEN], "utc": lb.utc()}
        rows = score_rows(ds, name, T.scored_ids(name, lists), runs,
                          {z["model"]: z for z in zss}, refs, ctx, ex, cfg)
        tmp = out.with_name(out.name + ".tmp")
        tmp.write_text("".join(json.dumps({**r, **stamp}, ensure_ascii=False) + "\n" for r in rows), encoding="utf-8")
        tmp.replace(out)
        print(f"wrote {len(rows)} rows to {out.name}")


# ------------------------------------------------------------------------------------------------ verified (local)
def cmd_verified(a) -> None:
    """score2.cmd_verified on XM-test2500 only (§13 item 7): refuses on a GPU host, refuses any run not on exactly
    the 2,500 ids, reads no OIV7 label of an outside image; asserts the 108 list."""
    if os.environ.get("VSPS_MACHINE_ID"):
        raise SystemExit("verified precision is scored locally only; VSPS_MACHINE_ID is set")
    import xm3600_oiv7 as XO

    ds = "xm_test2500"
    out = Path(a.ledger)
    if out.exists():
        raise SystemExit(f"{out} exists; verified precision is scored once")
    lists = C.load_lists(a.lists)
    T.three108(lists)
    ids = sorted(i for i, _f, _h in T.manifest_t(ds, lists))
    runs, zss = [G.read_preds(p) for p in a.runs], [G.read_preds(p) for p in a.zs]
    g = T.grid_t(S2.frozen())
    for r in runs + zss:
        if r["run_id"] not in g or r["dataset"] != ds or sorted(r["predictions"]) != ids or \
                r.get("c_schema") != T.SCHEMA:
            raise SystemExit(f"REFUSED: {r['run_id']} is not a test run on exactly the XM-test2500 images")
    for z in zss:
        T.zs_ok_t(z, z["model"], ds)
    vmap = XO.resolve_map(a.desc)
    labels = json.loads(Path(a.labels).read_text(encoding="utf-8"))
    st = XO.statuses(vmap, {i: labels[i] for i in ids if i in labels})
    del labels
    cache, caps = S.load_cache(a.cache), C.memory_captions(lists)
    zs_by = {z["model"]: z for z in zss}
    rows = []
    for r, z in [(r, zs_by[r["model"]]) for r in runs] + [(z, z) for z in zss]:
        for tau, capt, _cnt in S.variants(r, z, cache, caps):
            no = {i: None if r is z else G.neighbour_only(r["predictions"][i], z["predictions"][i], [
                C.shown(caps[x], "xm3600") for x in r["exemplars"][i]]) for i in ids}
            c = np.array([SC2.oiv7_counts(set(G.objects_in(capt[i])), {G.key(o) for o in G.classes(capt[i])}, no[i],
                                          st.get(i, {}), set(vmap), XO) for i in ids])
            rows.append({"label": T.LABEL, "c_schema": T.SCHEMA, "run_id": r["run_id"], "model": r["model"],
                         "dataset": ds, **{k: r["spec"][k] for k in ("arm", "k", "order", "tpl")},
                         "tau": tau, "n": len(ids),
                         "vp": 100 * c[:, 0].sum() / max(c[:, 0].sum() + c[:, 1].sum(), 1),
                         **({} if r is z else {"npx": SC2.np_summary(c[:, 2].tolist(), c[:, 3].tolist())}),
                         "per_image": {"ids": ids, "vp_p": c[:, 0].tolist(), "vp_a": c[:, 1].tolist(),
                                       "npx_tp": c[:, 2].tolist(), "npx_m": c[:, 3].tolist()},
                         "inputs": {"run_sha256": r["_sha256"], "zs_sha256": z["_sha256"],
                                    "labels_sha256": S2.sha_file(a.labels), "desc_sha256": S2.sha_file(a.desc),
                                    "map_sha256": S2.sha_file(XO.MAP),
                                    "cache_sha256": {Path(p).name: S2.sha_file(p) for p in a.cache}},
                         "c_prereg_sha256": T.T_PINS[T.PREREG], "utc": lb.utc()})
    out.write_text("".join(json.dumps(x) + "\n" for x in rows), encoding="utf-8")
    print(f"wrote {len(rows)} verified rows")


# ------------------------------------------------------------------------------------------------ decide
def aliased(rows: list[dict], ds: str) -> list[dict]:
    """ct_ -> c2_ in memory, so decide2's lookups (rid, c2_nn_) apply unchanged; refuses a non-ct_ row on a test set."""
    if ds not in T.SETS:
        return rows
    if any(not r["run_id"].startswith("ct_") or r["dataset"] != ds for r in rows):
        raise SystemExit(f"decide: a row of the {ds} ledger is not a ct_ test row")
    return [{**r, "run_id": "c2_" + r["run_id"].removeprefix("ct_")} for r in rows]


def reorder(rows: list[dict], order: list[str], subset: bool = False) -> list[dict]:
    """W6: every row's per-image lists in the pinned order; the ids must be the order (or contain it, for a subset
    cut of the verified rows); asserts identical ids across all rows."""
    out = []
    for r in rows:
        ids = r["per_image"]["ids"]
        if len(set(ids)) != len(ids) or not (set(order) <= set(ids) if subset else sorted(ids) == sorted(order)):
            raise SystemExit(f"{r['run_id']}: its images are not the pinned set")
        at = {i: k for k, i in enumerate(ids)}
        p = [at[i] for i in order]
        out.append({**r, "per_image": {k: [v[j] for j in p] if isinstance(v, list) and len(v) == len(ids) else v
                                       for k, v in r["per_image"].items()}})
    if len({tuple(r["per_image"]["ids"]) for r in out}) > 1:
        raise SystemExit("rows are not on identical ids after re-indexing")
    return out


def one_set(rows: list[dict], cfg: dict, ds: str, with_s3: bool = True) -> dict:
    """The numbers of one scored set: decide2.gate's rows without its stage-2 verdict rules (G1-G3, verdict), the PTB
    column pooled, NN baselines, dose-response and neighbour-only precision (§8.1). The InternVL3 -inf row is
    returned apart (§8.4)."""
    det = DD.gate(rows, cfg, ds)
    for k in ("G1", "G2", "G3", "verdict"):
        det.pop(k)
    ptb = [DD.cider_diff(*(DD.get(rows, DD.rid(cfg, ds, m, a), cfg["models"][m]["tau"]) for a in ("ret", "rand")),
                         "cider_ptb") for m in C.MODELS]
    nn = {n: DD.safe(DD.paired, rows, cfg, ds, o) for n, o in (
        ("vs_nn_top1", lambda m, c: (f"c2_nn_{ds}-top1", "-inf", c["tau"])),
        ("vs_nn_cons", lambda m, c: (f"c2_nn_{ds}-cons-k{c['k']}", "-inf", c["tau"])))}
    out = {"detail": det, "pooled_ptb_vs_rand": S.boot(np.mean(ptb, axis=0)), "nn": nn,
           "dose_response": DD.safe(DD.dose, rows, cfg, ds)}
    if with_s3:
        out["S3"] = DD.safe(DD.s3, cfg, ds, rows, "np_tp", "np_m")
    return {**out, "_neg_inf": neg_inf(rows, cfg, ds)}


def neg_inf(rows: list[dict], cfg: dict, ds: str) -> dict:
    """§8.4: InternVL3 ret - rand at tau = -inf, the set's own index matrix."""
    return S.boot(DD.cider_diff(*(DD.get(rows, DD.rid(cfg, ds, IVL, a), "-inf") for a in ("ret", "rand"))))


def s3_one(rows: list[dict], cfg: dict, ds: str, m: str, tk: str, mk: str) -> dict:
    """decide2.s3's per-backbone row: neighbour-only precision of ret at the frozen tau (CC-103c W3)."""
    t, n = DD.np_block(DD.get(rows, DD.rid(cfg, ds, m, "ret"), cfg["models"][m]["tau"]), tk, mk)
    return {**DD.ratio(t, n), **DD.j3(t, n)}


def qwen_rows(rows: list[dict], cfg: dict, ds: str, ov: bool = True) -> dict:
    """CC-103b W2: the rows of a set whose InternVL3 frozen arms are incomplete (W16) that read no InternVL3
    frozen-tau row: decide2.gate's per-backbone block for Qwen and Qwen's NN rows; on OV also P1b-Qwen with its
    label and Qwen's S3. On XM no P1b and no label (CC-103c W4; PREREG §7.3, §7.5)."""
    c = cfg["models"][QWEN]
    ret, rand, fix = (DD.get(rows, DD.rid(cfg, ds, QWEN, a), c["tau"]) for a in ("ret", "rand", "fix"))
    zs = DD.get(rows, DD.rid(cfg, ds, QWEN, "zs"))
    rep = {"vs_rand": S.boot(DD.cider_diff(ret, rand)), "vs_fix": S.boot(DD.cider_diff(ret, fix)),
           "vs_zs": S.boot(DD.cider_diff(ret, zs)), "pcm_vs_zs": S.pcm_ci(ret),
           "verbatim_share": ret["verbatim_share"], "length": S.length_gap(ret, rand),
           "ptb_vs_rand": S.boot(DD.cider_diff(ret, rand, "cider_ptb")),
           "style": {a: x["style"] for a, x in (("ret", ret), ("rand", rand), ("fix", fix))},
           "src_share": {a: x.get("src_share") for a, x in (("ret", ret), ("rand", rand), ("fix", fix))}}
    nn = {"vs_nn_top1": S.boot(DD.cider_diff(ret, DD.get(rows, f"c2_nn_{ds}-top1"))),
          "vs_nn_cons": S.boot(DD.cider_diff(ret, DD.get(rows, f"c2_nn_{ds}-cons-k{c['k']}")))}
    if not ov:
        return {QWEN: rep, "nn_qwen": nn}
    return {QWEN: rep, "P1b_qwen": {**rep["vs_rand"], "confirmed": rep["vs_rand"]["d"] > SESOI}, "nn_qwen": nn,
            "s3_qwen": s3_one(rows, cfg, ds, QWEN, "np_tp", "np_m")}


def scope_row(p1b: dict) -> str:
    """§9.2 mapping (exhaustive). Reads the P1b rows only."""
    q, i = p1b[QWEN], p1b[IVL]
    if q["d"] > SESOI:
        return ("qwen_main_internvl_not_detected" if i["lo"] <= 0 else
                "qwen_main_internvl_smaller" if i["d"] < q["d"] else "both")
    return "internvl_main_qwen_below_sesoi" if i["d"] > SESOI and i["lo"] > 0 else "neither_at_sesoi"


def s_zf(det: dict) -> dict:
    return {"pooled_vs_zs": det["pooled_vs_zs"], "pooled_vs_fix": det["pooled_vs_fix"],
            "expected_vs_zs_pooled": EXPECTED_VS_ZS,
            "per_model": {m: {k: det["per_model"][m][k] for k in ("vs_zs", "vs_fix")} for m in C.MODELS}}


def secondary(res: dict, sets: dict, cfg: dict, ds: str) -> dict:
    """§8.4: written under its own key; the label is from its CI only. No gate or scope rule reads it. On a set whose
    InternVL3 frozen arms are incomplete, the registered tau = 0.10 result (INCOMPLETE) is printed first (W12, W2)."""
    out = {}
    for n, r in res.items():
        x = r["_neg_inf"] if "_neg_inf" in r else DD.safe(neg_inf, sets[n], cfg, ds)
        out[n] = {**({"registered_tau_0.10": "INCOMPLETE"} if "incomplete" in r else {}), **x,
                  **({"label": "detected" if x["lo"] > 0 else "not detected"} if "lo" in x else {})}
    return out


def incomplete_rows(res: dict, sets: dict, cfg: dict, ds: str, ov: bool = True) -> dict:
    return {n: DD.safe(qwen_rows, sets[n], cfg, ds, ov) for n, r in res.items() if "incomplete" in r}


def strip(res: dict) -> dict:
    return {n: {k: v for k, v in r.items() if k != "_neg_inf"} for n, r in res.items()}


def decide_ov(sets: dict[str, list[dict]], cfg: dict, ds: str, primary: str) -> dict:
    """§7.2-§7.4, §9.2: P1 (pooled, point > SESOI and lo > 0; rule L on the primary), P1b, P2, scope sentence."""
    res = {n: DD.safe(one_set, rows, cfg, ds) for n, rows in sets.items()}
    p = res[primary]
    if "incomplete" in p:  # W16: an incomplete InternVL3 arm gives no verdict; no fallback to -inf
        return {"P1": {"verdict": f"INCOMPLETE: {p['incomplete']}"}, "P2": "INCOMPLETE", "scope": "INCOMPLETE",
                "sets": strip(res), "incomplete_set_rows": incomplete_rows(res, sets, cfg, ds),
                "secondary_devb_motivated": {"internvl3_neg_inf": secondary(res, sets, cfg, ds)}}
    det = p["detail"]
    pooled = det["pooled_vs_rand"]
    passed = pooled["d"] > SESOI and pooled["lo"] > 0
    verdict = ("PASS, not separated from length" if det["L"] else "PASS") if passed else "FAIL"
    p1b = {m: {**det["per_model"][m]["vs_rand"], **({"confirmed": det["per_model"][m]["vs_rand"]["d"] > SESOI}
                                                    if m == QWEN else {"prediction": None})} for m in C.MODELS}
    p2 = {m: {**det["per_model"][m]["pcm_vs_zs"], "passed": det["per_model"][m]["pcm_vs_zs"]["lo"] > PCM_FLOOR}
          for m in C.MODELS}
    row = scope_row(p1b) if passed else None
    return {"P1": {**pooled, "passed": passed, "L": det["L"], "verdict": verdict,
                   "length": {m: det["per_model"][m]["length"] for m in C.MODELS}},
            "P1b": p1b, "P2": {**p2, "passed_both": all(p2[m]["passed"] for m in C.MODELS)},
            "scope": {"row": row, "sentence": SCOPE.get(row)}, "S_zf": s_zf(det),
            "sensitivity": {n: r.get("detail", r).get("pooled_vs_rand") for n, r in res.items() if n != primary},
            "sets": strip(res), "secondary_devb_motivated": {"internvl3_neg_inf": secondary(res, sets, cfg, ds)}}


def decide_xm(sets: dict[str, list[dict]], cfg: dict, ds: str, main: str) -> dict:
    """§7.5 XM-a on M3: pooled ret - rand CI lower bound > 0; the point is printed as a number only."""
    res = {n: DD.safe(one_set, rows, cfg, ds, False) for n, rows in sets.items()}
    m_ = res[main]
    if "incomplete" in m_:
        return {"XM_a": {"verdict": f"INCOMPLETE: {m_['incomplete']}"}, "sets": strip(res),
                "incomplete_set_rows": incomplete_rows(res, sets, cfg, ds, ov=False),
                "secondary_devb_motivated": {"internvl3_neg_inf": secondary(res, sets, cfg, ds)}}
    d = m_["detail"]["pooled_vs_rand"]
    return {"XM_a": {**d, "passed": d["lo"] > 0, "point_descriptive": d["d"]},
            "per_model": {m: m_["detail"]["per_model"][m]["vs_rand"] for m in C.MODELS},
            "L": m_["detail"]["L"], "ptb": m_["pooled_ptb_vs_rand"], "S_zf": s_zf(m_["detail"]),
            "sensitivity": {n: r.get("detail", r).get("pooled_vs_rand") for n, r in res.items() if n != main},
            "sets": strip(res), "secondary_devb_motivated": {"internvl3_neg_inf": secondary(res, sets, cfg, ds)}}


def s2_t(cfg: dict, vrows: list[dict], ds: str) -> dict:
    """decide2.s2 with the set as a parameter: pooled over mentions and backbones, Delta verified precision of ret at
    the frozen tau against zs, numerator and denominator resampled together."""
    p, a, p0, a0 = 0, 0, 0, 0
    for m in C.MODELS:
        ret = DD.get(vrows, DD.rid(cfg, ds, m, "ret"), cfg["models"][m]["tau"])
        zs = DD.get(vrows, DD.rid(cfg, ds, m, "zs"))
        DD.same_ids(ret, zs)
        p, a, p0, a0 = p + DD.arr(ret, "vp_p"), a + DD.arr(ret, "vp_a"), p0 + DD.arr(zs, "vp_p"), a0 + DD.arr(zs, "vp_a")
    d = DD.ratio(p, p + a, p0, p0 + a0)
    return {**d, "passed": d["lo"] is not None and d["lo"] > VP_FLOOR}


def decide_xmb(vsets: dict[str, list[dict]], cfg: dict, ds: str, main: str, xm_a: dict) -> dict:
    """§7.5 XM-b (local) and the registered conjunction: "confirmed" iff XM-a and XM-b both pass."""
    xmb = {n: DD.safe(s2_t, cfg, rows, ds) for n, rows in vsets.items()}
    s3 = {n: DD.safe(DD.s3, cfg, ds, rows, "npx_tp", "npx_m") for n, rows in vsets.items()}
    b = xmb[main]
    ok_a, ok_b = xm_a.get("passed") is True, b.get("passed") is True
    incomplete = "verdict" in xm_a or "incomplete" in b
    return {"XM_b": b, "XM_b_sensitivity": {n: v for n, v in xmb.items() if n != main}, "S3_verified": s3,
            "incomplete_set_rows": {n: {"s3_verified_qwen": DD.safe(s3_one, vsets[n], cfg, ds, QWEN, "npx_tp", "npx_m")}
                                    for n, x in s3.items() if "incomplete" in x},
            "XM_a_read": xm_a, "XM_prediction": "INCOMPLETE" if incomplete else
            "confirmed" if ok_a and ok_b else "not confirmed"}


def load_led(d: Path, name: str, ds: str, order: list[str]) -> tuple[list[dict], dict]:
    p = d / f"ledger_{name}.jsonl"
    rows = read_jsonl(p)
    if any(r.get("scored_set") != name for r in rows):
        raise SystemExit(f"{p}: a row of another scored set")
    return reorder(aliased(S.latest(rows), ds), order), {"path": p.name, "sha256": S2.sha_file(p), "rows": len(rows)}


def cmd_decide(a) -> None:
    out = Path(a.out)
    if out.exists():
        raise SystemExit(f"{out} exists; each block's decide runs once (§11.4)")
    if a.phase == "xmb" and os.environ.get("VSPS_MACHINE_ID"):
        raise SystemExit("XM-b is scored locally only")
    if a.phase != "xmb":
        T.out_ok(out)
    lists, cfg = C.load_lists(a.lists), S2.frozen()
    rec = {"label": T.LABEL, "c_schema": T.SCHEMA, "phase": a.phase, "utc": lb.utc(),
           "c_prereg_sha256": T.T_PINS[T.PREREG], "frozen_config_sha256": S2.PINS[S2.FROZEN], "SESOI": SESOI}
    if a.phase in BLOCKS:
        ds, main, sens = BLOCKS[a.phase]
        got = {n: load_led(a.ledger_dir, n, ds, T.scored_ids(n, lists)) for n in (main, sens)}
        sets = {n: r for n, (r, _i) in got.items()}
        rec["ledgers"] = {n: i for n, (_r, i) in got.items()}
        rec |= decide_ov(sets, cfg, ds, main) if a.phase == "ov" else decide_xm(sets, cfg, ds, main)
    else:
        ds = "xm_test2500"
        v = aliased(S.latest(read_jsonl(a.verified)), ds)
        xm = json.loads(Path(a.xm_decide).read_text(encoding="utf-8"))
        if xm.get("phase") != "xm" or xm.get("c_prereg_sha256") != T.T_PINS[T.PREREG]:
            raise SystemExit(f"{a.xm_decide}: not the M3 XM decide of this prereg")
        vsets = {n: reorder(v, T.scored_ids(n, lists), subset=True) for n in ("xm_test2500", "xm_test2392")}
        rec["verified"] = {"path": Path(a.verified).name, "sha256": S2.sha_file(a.verified), "rows": len(v)}
        rec["xm_decide"] = {"path": Path(a.xm_decide).name, "sha256": S2.sha_file(a.xm_decide)}
        rec |= decide_xmb(vsets, cfg, ds, "xm_test2500", xm["XM_a"])
    out.write_text(json.dumps(norm(rec), indent=1) + "\n", encoding="utf-8")
    print(f"wrote {out.name} sha256 {S2.sha_file(out)}")  # W10: no verdict on the log


# ------------------------------------------------------------------------------------------------ dry (CC-103b)
def check(cond: bool, msg: str) -> None:
    if not cond:
        raise SystemExit(f"DRY CHECK FAILED: {msg}")
    print(f"ok  {msg}")


def dev_pinned(key: str) -> Path:
    p, h = DEV_PINS[key]
    check(S2.sha_file(p) == h, f"{p.name} sha256 {h[:8]}")
    return p


def dry(kit: Path) -> None:
    """CC-103 E2 (a), (b) on the mirrored stage-2 dev artefacts, CPU, local. No image is opened and nothing is
    decoded (no GPU, no torch here); every comparison is exact."""
    if os.environ.get("VSPS_MACHINE_ID"):
        raise SystemExit("the dry check runs locally only")
    data = T.ROOT / "data"
    for rel, h in T.MEMORY.items():
        check(S2.sha_file(data / rel) == h, f"memory source {rel} at its pin {h[:8]} (the file the chain stages)")
    lists = C.load_lists(LISTS)
    cfg = S2.frozen()
    c2 = MIRROR / "c_stage2"
    sums = dict(reversed(x.split(maxsplit=1)) for x in (c2 / "SHA256SUMS").read_text().splitlines())
    rows_b = S2.manifest2("ov_dev_b", lists)
    ids_b = sorted(i for i, _f, _h in rows_b)
    # 1. examples: the test exemplars step on the mirrored OV-dev-B query embeddings reproduces ex_ov_dev_b.json
    ex_file = json.loads((c2 / "ex_ov_dev_b.json").read_text(encoding="utf-8"))
    check(sums["ex_ov_dev_b.json"] == S2.sha_file(c2 / "ex_ov_dev_b.json"), "ex_ov_dev_b.json = mirror SHA256SUMS")
    ex = T.make_exemplars("ov_dev_b", rows_b, MIRROR / "c_stage1/emb.npz", c2 / "emb_ov_dev_b.npz", LISTS,
                          {"ov_dev_b": ids_b})
    same = [k for k in ex_file if k not in ("label", "c_schema", "prereg_sha256", "ret") and norm(ex[k]) == ex_file[k]]
    check(len(same) == len(ex_file) - 4 and ex["scored_dose_cuts"]["ov_dev_b"] == ex_file["dose_tertile_cuts"][
        "ov_dev_b"], f"exemplars replay: {len(same)} keys of ex_ov_dev_b.json identical (rand, fix, n_cut, cuts, "
                     "shas), scored-set cuts = dev-B cuts")
    a_, b_ = norm(ex["ret"])["ov_dev_b"], ex_file["ret"]["ov_dev_b"]
    gap = max(abs(x[1] - y[1]) for q in b_ for x, y in zip(a_[q], b_[q]))
    check(a_.keys() == b_.keys() and all([c for c, _x in a_[q]] == [c for c, _x in b_[q]] for q in b_) and
          gap <= 1.0000001e-6, f"ret lists: every cluster id and order identical; cosines (6 decimals) within {gap:.1e}"
          " (CPU float rounding here against M3)")
    # 2. prompts: memory captions from the pinned sources rebuild every stage-2 OV-dev-B and E4 stage-1 prompt sha
    caps = C.memory_captions(lists, data)
    zs_text = lb.prompt_text(C.registration(), "short")
    runs = {p.name.removesuffix(".preds.json"): G.read_preds(p) for p in sorted((c2 / "runs").glob(
        "c2_*_ov_dev_b-*.preds.json")) if "-blind-" not in p.name}
    check(len(runs) == 8 and all(sums[f"runs/{r}.preds.json"] == p["_sha256"] for r, p in runs.items()),
          "8 OV-dev-B runs (ret, rand, fix, zs x 2) = mirror SHA256SUMS")
    for r in runs.values():
        tsha = {i: C.sha(t) for i, t in D2prompts(r["spec"], rows_b, r["exemplars"], caps, zs_text).items()}
        check(tsha == r["prompt_sha256_per_image"], f"prompt sha256 rebuilt for {r['run_id']} (925/925)")
    s1 = MIRROR / "c_stage1"
    for m in C.MODELS:
        rid = cfg["models"][m]["stage1_run_id"]
        T.check_stage1_outputs(s1, [f"runs/{rid}.preds.json", "exemplars.json"])
        ref = G.read_preds(s1 / f"runs/{rid}.preds.json")
        items = C.manifest("ktvic_dev299", lists)[:T.E4_N]
        exids = C.check_exemplars(items, C.run_spec(rid), C.load_exemplars(s1 / "exemplars.json", LISTS), lists)
        tsha = {i: C.sha(t) for i, t in D2prompts(C.run_spec(rid), items, exids, caps, zs_text).items()}
        check(all(tsha[i] == ref["prompt_sha256_per_image"][i] for i, _f, _h in items) and
              all(exids[i] == ref["exemplars"][i] for i, _f, _h in items),
              f"E4 basis: {T.E4_N} dev299 prompts and example ids of {rid} rebuilt")
    # 3. E2(b) scorer replay: the test scorer on the OV-dev-B runs reproduces every L2 row
    L2 = [r for r in read_jsonl(dev_pinned("ledger")) if r["dataset"] == "ov_dev_b"]
    ann = json.loads(dev_pinned("ov_dev_ann").read_text(encoding="utf-8"))
    refs = {f: [c.strip() for c in ann[f]["captions"]] for f in ids_b}
    E4, PA, PTB = SC2.kit2(kit)
    check((E4.VNC / "VnCoreNLP-1.2.jar").is_file() and lb.sha256_file(E4.VNC / "VnCoreNLP-1.2.jar") == S.JAR_SHA256,
          f"VnCoreNLP jar of Paper B's protocol card under $NCS_DATA/vncorenlp ({E4.VNC})")
    caches = sorted((c2 / "guard").glob("ov_dev_b_*.cache.jsonl"))
    ctx = {"cache": S.load_cache(caches), "caps": caps, "segment": E4.rdr, "E4": E4, "PA": PA, "PTB": PTB}
    zss = [r for r in runs.values() if r["spec"]["arm"] == "zs"]
    for z in zss:
        S2.zs_ok2(z, z["model"], "ov_dev_b")
    got = score_rows("ov_dev_b", "ov_dev_b", ids_b, [r for r in runs.values() if r["spec"]["arm"] != "zs"],
                     {z["model"]: z for z in zss}, refs, ctx, ex_file, cfg)
    by = {(r["run_id"], r["tau"]): r for r in L2 if "-blind-" not in r["run_id"]}
    diff = [k for k in by if k not in {(r["run_id"], r["tau"]) for r in got}]
    bad = [(r["run_id"], r["tau"]) for r in got if (r["run_id"], r["tau"]) not in by or norm(
        {k: v for k, v in r.items() if k not in STAMP_KEYS}) != {k: v for k, v in by[(r["run_id"], r["tau"])].items()
                                                                 if k not in STAMP_KEYS}]
    check(not diff and not bad and len(got) == len(by),
          f"scorer replay: {len(got)} rows = the {len(by)} non-blind L2 OV-dev-B rows, every field and per_image list")
    # 4. E2(a) decide replay: ov_dev_b in the OV slot, xm_dev500 in the XM slot, against DF
    df = json.loads(dev_pinned("df").read_text(encoding="utf-8"))
    led = S.latest(read_jsonl(dev_pinned("ledger")))
    ver = S.latest(read_jsonl(dev_pinned("verified")))
    slot = {ds: reorder([r for r in led if r["dataset"] == ds], sorted(next(r for r in led if r["dataset"] == ds and
                                                                               "ids" in r["per_image"])["per_image"][
        "ids"])) for ds in ("ov_dev_b", "xm_dev500")}
    ov = decide_ov({"primary": slot["ov_dev_b"], "sens": slot["ov_dev_b"]}, cfg, "ov_dev_b", "primary")
    g = df["ov_dev_b"]["gate"]
    pd = ov["sets"]["primary"]
    check(norm({k: ov["P1"][k] for k in ("d", "lo", "hi")}) == g["pooled_vs_rand"], "P1 <- DF G1 pooled_vs_rand")
    check(norm({m: {k: v for k, v in ov["P1b"][m].items() if k in ("d", "lo", "hi")} for m in C.MODELS}) ==
          {m: g["per_model"][m]["vs_rand"] for m in C.MODELS}, "P1b <- DF per_model vs_rand")
    check(norm({m: {k: ov["P2"][m][k] for k in ("d", "lo", "hi")} for m in C.MODELS}) ==
          {m: g["per_model"][m]["pcm_vs_zs"] for m in C.MODELS}, "P2 <- DF per_model pcm_vs_zs")
    check(norm(pd["detail"]) == {k: v for k, v in g.items() if k not in ("G1", "G2", "G3", "verdict")},
          "every other gate number (vs_fix, vs_zs, length, PTB, style, src_share, L) = DF")
    check(norm(pd["nn"]) == df["ov_dev_b"]["reported"]["nn"] and norm(pd["dose_response"]) == df["ov_dev_b"][
        "reported"]["dose_response"] and norm(pd["S3"]) == df["ov_dev_b"]["S3"], "NN, dose-response, S3 = DF (OV)")
    xm = decide_xm({"main": slot["xm_dev500"]}, cfg, "xm_dev500", "main")
    s1_ = df["xm_dev500"]["S1"]
    check(norm({k: xm["XM_a"][k] for k in ("d", "lo", "hi")}) == {k: s1_[k] for k in ("d", "lo", "hi")},
          "XM-a <- DF S1 point and CI")
    xd = xm["sets"]["main"]
    check(norm(xd["detail"]) == {k: v for k, v in df["xm_dev500"]["detail"].items() if k not in ("G1", "G2", "G3",
                                                                                                  "verdict")}
          and norm(xd["nn"]) == df["xm_dev500"]["reported"]["nn"] and norm(xd["dose_response"]) == df["xm_dev500"][
              "reported"]["dose_response"], "XM detail, NN, dose-response = DF")
    vsl = {"main": reorder(ver, slot["xm_dev500"][0]["per_image"]["ids"])}
    xb = decide_xmb(vsl, cfg, "xm_dev500", "main", xm["XM_a"])
    s2_ = df["xm_dev500"]["S2"]
    check(norm({k: xb["XM_b"][k] for k in ("d", "lo", "hi", "undefined_draws")}) == {
        k: s2_[k] for k in ("d", "lo", "hi", "undefined_draws")} and xb["XM_b"]["passed"] == s2_["confirmed"],
        "XM-b <- DF S2 (point, CI, undefined draws, pass)")
    check(norm(xb["S3_verified"]["main"]) == df["xm_dev500"]["S3"], "S3 on verified classes = DF (XM)")
    neg = {k: [round(v[x], 3) for x in ("d", "lo", "hi")] for k, v in (
        ("ov", ov["secondary_devb_motivated"]["internvl3_neg_inf"]["primary"]),
        ("xm", xm["secondary_devb_motivated"]["internvl3_neg_inf"]["main"]))}
    check(neg == {"ov": [5.356, 3.527, 7.119], "xm": [1.541, -2.12, 5.25]},
          "OQ-J InternVL3 -inf rows = CC-103's recomputation (5.356 [3.527, 7.119]; 1.541 [-2.120, 5.250])")
    # 5. the shell scripts parse
    for sh in ("c_test_job.sh", "c_test_chain.sh"):
        check(subprocess.run(["bash", "-n", str(T.HERE / sh)]).returncode == 0, f"bash -n {sh}")
    job = subprocess.run(["bash", str(T.HERE / "c_test_job.sh"), "--selftest"], cwd=T.ROOT, capture_output=True,
                         text=True)
    if job.returncode:
        print(job.stdout[-800:], job.stderr[-800:])
    check(job.returncode == 0, "c_test_job.sh --selftest (cap-stop finality)")
    print("dry ok: CC-103 E2 (a) and (b) reproduce the stage-2 numbers exactly; GPU steps not exercised here")


def D2prompts(spec, items, exids, caps, zs):
    return T.D2.prompts(spec, items, exids, caps, zs)


# ------------------------------------------------------------------------------------------------ self-test (CPU)
def fake_test(cfg: dict, ds: str = "ov_test", **kw) -> list[dict]:
    """decide2.fake_ledger's synthetic OV-dev-B rows recast as test rows (ct_ ids, the test set name)."""
    out = []
    for r in DD.fake_ledger(cfg, **kw):
        if r["dataset"] != "ov_dev_b" or r["arm"] == "blind":
            continue
        rid = r["run_id"].replace("_ov_dev_b", f"_{ds}").replace("c2_", "ct_", 1)
        out.append({**r, "run_id": rid, "dataset": ds})
    return out


def selftest() -> None:
    cfg = S2.frozen()
    ids = [str(i) for i in range(60)]
    order = ids[::-1]
    rows = reorder(aliased(fake_test(cfg), "ov_test"), order)
    assert rows[0]["per_image"]["ids"] == order and rows[0]["per_image"]["cider_s"][0] == \
        fake_test(cfg)[0]["per_image"]["cider_s"][59], "re-indexed to the pinned order, values follow their ids"
    assert C.refuses(lambda: aliased(DD.fake_ledger(cfg), "ov_test")), "a c2_ row in a test ledger is refused"
    assert C.refuses(lambda: reorder(rows, ids[:59])), "a different image set is refused"
    base = decide_ov({"a": rows, "b": rows}, cfg, "ov_test", "a")
    assert base["P1"]["verdict"] == "PASS" and base["P2"]["passed_both"] and base["scope"]["row"] == "both"
    assert base["P1b"][QWEN]["confirmed"] and "confirmed" not in base["P1b"][IVL], "InternVL3: reported only"
    small = reorder(aliased(fake_test(cfg, gain=1.5), "ov_test"), order)
    s = decide_ov({"a": small, "b": rows}, cfg, "ov_test", "a")
    assert s["P1"]["verdict"] == "FAIL" and s["scope"]["row"] is None, "P1 needs point > SESOI; no scope if it fails"
    lng = decide_ov({"a": reorder(aliased(fake_test(cfg, long_ret=13.5), "ov_test"), order)}, cfg, "ov_test", "a")
    assert lng["P1"]["verdict"] == "PASS, not separated from length", "rule L (W5)"
    pc = decide_ov({"a": reorder(aliased(fake_test(cfg, pcm=-1), "ov_test"), order)}, cfg, "ov_test", "a")
    assert not pc["P2"]["passed_both"] and pc["P1"]["verdict"] == "PASS", "P2 does not gate P1"
    no_ivl = [r for r in rows if not (r["model"] == IVL and r["tau"] == "0.10")]
    w16 = decide_ov({"a": no_ivl}, cfg, "ov_test", "a")
    assert w16["P1"]["verdict"].startswith("INCOMPLETE"), "W16: InternVL3 frozen arms incomplete, no -inf fallback"
    part = w16["incomplete_set_rows"]["a"]
    full = base["sets"]["a"]
    assert norm(part[QWEN]) == norm(full["detail"]["per_model"][QWEN]) and norm(part["nn_qwen"]) == norm(
        {k: full["nn"][k][QWEN] for k in part["nn_qwen"]}), "W2: Qwen's rows equal the complete case exactly"
    assert part["P1b_qwen"]["confirmed"] and w16["P2"] == "INCOMPLETE" and "P1b" not in w16
    sec = w16["secondary_devb_motivated"]["internvl3_neg_inf"]["a"]
    assert list(sec)[0] == "registered_tau_0.10" and sec["label"] in ("detected", "not detected")
    assert norm({k: sec[k] for k in ("d", "lo", "hi")}) == norm({k: base["secondary_devb_motivated"][
        "internvl3_neg_inf"]["a"][k] for k in ("d", "lo", "hi")}), "W2: the -inf row is computed and labelled"
    xw = decide_xm({"m": [r for r in reorder(aliased(fake_test(cfg, "xm_test2500"), "xm_test2500"), order)
                          if not (r["model"] == IVL and r["tau"] == "0.10")]}, cfg, "xm_test2500", "m")
    inc = xw["incomplete_set_rows"]["m"]
    assert xw["XM_a"]["verdict"].startswith("INCOMPLETE") and "d" in inc[QWEN]["vs_rand"] and "P1b_qwen" not in inc \
        and '"confirmed"' not in json.dumps(norm(xw["incomplete_set_rows"])), "CC-103c W4: XM rows carry no label"
    assert norm(part["s3_qwen"]) == norm(full["S3"]["per_model"][QWEN]), "CC-103c W3: Qwen's S3 = complete case"
    # OQ-J: perturbing InternVL3's ret/rand rows at -inf moves only secondary_devb_motivated
    bump = [{**r, "per_image": {**r["per_image"], "cider_s": (np.array(r["per_image"]["cider_s"]) + (
        7 if r["arm"] == "ret" else 0)).tolist()}} if r["model"] == IVL and r["tau"] == "-inf" and r["arm"] in (
        "ret", "rand") else r for r in rows]
    moved = decide_ov({"a": bump, "b": rows}, cfg, "ov_test", "a")
    drop = lambda d: {k: v for k, v in norm(d).items() if k != "secondary_devb_motivated"}  # noqa: E731
    assert drop(moved) == drop(base) and moved["secondary_devb_motivated"] != base["secondary_devb_motivated"]
    assert moved["secondary_devb_motivated"]["internvl3_neg_inf"]["a"]["label"] == "detected"
    p1b = lambda q, i, ilo: {QWEN: {"d": q, "lo": 0}, IVL: {"d": i, "lo": ilo}}  # noqa: E731
    assert [scope_row(p1b(*x)) for x in ((5, 1, -1), (5, 3, 1), (5, 6, 1), (1, 3, 1), (1, 3, -1), (1, 1, 1))] == [
        "qwen_main_internvl_not_detected", "qwen_main_internvl_smaller", "both", "internvl_main_qwen_below_sesoi",
        "neither_at_sesoi", "neither_at_sesoi"], "§9.2 mapping, exhaustive"
    # XM: XM-a needs only the CI lower bound; the prediction is the conjunction with XM-b
    xr = reorder(aliased(fake_test(cfg, "xm_test2500"), "xm_test2500"), order)
    xa = decide_xm({"m": xr}, cfg, "xm_test2500", "m")
    assert xa["XM_a"]["passed"] and "confirmed" not in xa["XM_a"]
    v = [{"run_id": DD.rid(cfg, "xm_test2500", m, arm).replace("c2_", "ct_", 1), "dataset": "xm_test2500",
          "model": m, "tau": t, "per_image": {"ids": ids, "vp_p": [3] * 60, "vp_a": [1] * 60,
                                              "npx_tp": [1] * 60, "npx_m": [2] * 60}}
         for m in C.MODELS for arm, t in (("ret", cfg["models"][m]["tau"]), ("zs", "-inf"))]
    for a_, want in ((1, "confirmed"), (3, "not confirmed")):
        vv = [{**r, "per_image": {**r["per_image"], "vp_a": [1 if "-zs" in r["run_id"] else a_] * 60}} for r in v]
        out = decide_xmb({"m": reorder(aliased(vv, "xm_test2500"), order)}, cfg, "xm_test2500", "m", xa["XM_a"])
        assert out["XM_prediction"] == want, (a_, out["XM_prediction"])
    out = decide_xmb({"m": reorder(aliased(v, "xm_test2500"), order)}, cfg, "xm_test2500", "m",
                     {**xa["XM_a"], "passed": False})
    assert out["XM_prediction"] == "not confirmed" and out["XM_b"]["passed"], "XM-a fails: not confirmed"
    gone = decide_xmb({"m": reorder(aliased([r for r in v if r["model"] != IVL or "-zs" in r["run_id"]], "xm_test2500"),
                                    order)}, cfg, "xm_test2500", "m", xa["XM_a"])
    assert norm(gone["incomplete_set_rows"]["m"]["s3_verified_qwen"]) == norm(out["S3_verified"]["m"]["per_model"][
        QWEN]), "CC-103c W3: Qwen's S3_verified kept when the set's S3 is incomplete"
    sub = reorder(aliased(v, "xm_test2500"), ids[:30], subset=True)
    assert sub[0]["per_image"]["ids"] == ids[:30] and len(sub[0]["per_image"]["vp_p"]) == 30, "2,392-style cut"
    with tempfile.TemporaryDirectory() as tmp:
        o = Path(tmp) / "d.json"
        o.write_text("{}")
        assert C.refuses(lambda: cmd_decide(argparse.Namespace(out=o, phase="ov"))), "a decide runs once"
        os.environ["VSPS_MACHINE_ID"] = os.environ.get("VSPS_MACHINE_ID", "selftest")
        try:
            assert C.refuses(lambda: cmd_verified(argparse.Namespace())), "verified refuses on a GPU host"
        finally:
            if os.environ["VSPS_MACHINE_ID"] == "selftest":
                del os.environ["VSPS_MACHINE_ID"]
    print("selftest ok: ct_ alias and W6 re-index, P1 (point > SESOI and lo > 0), rule L, P2 non-gating for P1, "
          "W16 incomplete without -inf fallback (W2: Qwen and -inf rows kept), OQ-J key read by nothing else, §9.2 scope map, XM-a on the CI, "
          "XM conjunction with XM-b, subset cut, decide once, verified local only")


def main() -> None:
    ap = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    ap.add_argument("--selftest", action="store_true")
    ap.add_argument("--dry", action="store_true")
    ap.add_argument("--kit-b", type=Path, default=T.ROOT / "scripts/kit_b")
    sub = ap.add_subparsers(dest="cmd")
    p = sub.add_parser("score")
    p.add_argument("--set", choices=sorted(T.SETS), required=True)
    p.add_argument("--exemplars", type=Path, required=True)
    p.add_argument("--ledger-dir", type=Path, required=True)
    p.add_argument("--kit-b", type=Path, default=T.ROOT / "scripts/kit_b")
    p2 = sub.add_parser("verified")
    p2.add_argument("--labels", type=Path, required=True, help="data/xm3600/oiv7_labels.json (local)")
    p2.add_argument("--desc", type=Path, required=True, help="oidv7-class-descriptions.csv")
    p2.add_argument("--ledger", type=Path, required=True)
    for q in (p, p2):
        q.add_argument("--runs", nargs="+", type=Path, required=True)
        q.add_argument("--zs", nargs=2, type=Path, required=True)
        q.add_argument("--cache", nargs="*", type=Path, default=[])
        q.add_argument("--lists", type=Path, required=True)
    p = sub.add_parser("decide")
    p.add_argument("--phase", choices=("ov", "xm", "xmb"), required=True)
    p.add_argument("--ledger-dir", type=Path)
    p.add_argument("--verified", type=Path)
    p.add_argument("--xm-decide", type=Path)
    p.add_argument("--lists", type=Path, required=True)
    p.add_argument("--out", type=Path, required=True)
    a = ap.parse_args()
    if a.selftest:
        return selftest()
    if a.dry:
        return dry(a.kit_b)
    {"score": cmd_score, "verified": cmd_verified, "decide": cmd_decide}.get(a.cmd, lambda _a: ap.error("mode?"))(a)


if __name__ == "__main__":
    main()
