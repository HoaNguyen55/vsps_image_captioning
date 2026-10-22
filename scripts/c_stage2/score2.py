#!/usr/bin/env python3
"""Paper C stage 2 (STAGE 2 / DEV-B, ONE LOOK): ledger rows of every stage-2 run, the NN copy baselines, and local
verified precision on XM-dev500. Prereg manuscript/prereg/2026-10-22_c_stage2/PREREG.md §6, §7.5, §12 items 8-9, 15.

  python scripts/c_stage2/score2.py --selftest --kit-b scripts/kit_b                                  CPU, no data
  python scripts/c_stage2/score2.py score --set S --runs R ... --zs Z ... --cache C ... --lists L --exemplars X \
      --kit-b scripts/kit_b --ledger F                                                                 CPU (M3)
  python scripts/c_stage2/score2.py verified --runs R ... --zs Z ... --cache C ... --lists L --labels OIV7 \
      --desc CSV --ledger F                                                          CPU, local only (refuses on M3)
The stage-1 metrics come from scripts/c_stage1/score.py score_set, unchanged. Added per row: CIDEr-D with the PTB
punctuation list removed (CC-088 B-1, ptb_protocol.ptb; reported only), neighbour-only object precision per image
(tp, m; §7.5, reference gold) and the source-dataset share (C-d). NN-top1 and NN-consensus rows (C-b) are scored
from the memory captions at run time; no caption is written. The ledger holds numbers and ids only.
"""
from __future__ import annotations

import argparse
import importlib.util
import json
import os
import sys
from pathlib import Path

import numpy as np

sys.path.insert(0, str(Path(__file__).resolve().parent))
import stage2 as S2  # noqa: E402

C, G, lb = S2.C, S2.G, S2.lb
import score as S  # noqa: E402  stage-1 scorer, sha-checked by stage2


def kit2(folder: Path):
    """(protocol_pilot, punctuation_audit, ptb_protocol) of the committed kit, each pinned by sha256."""
    E4, PA = S.kit(folder)
    p = Path(folder) / "ptb_protocol.py"
    if not p.is_file() or S2.sha_file(p) != S2.PINS[S2.PTB]:
        raise SystemExit(f"{p}: not the committed ptb_protocol.py")
    saved = list(sys.path)
    spec = importlib.util.spec_from_file_location("ptb_protocol", p)
    mod = sys.modules["ptb_protocol"] = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(mod)  # its `import protocol_pilot` resolves to the module S.kit loaded
    sys.path[:] = saved
    return E4, PA, mod


def stripped(PA, seg: str) -> str:
    return " ".join(PA.strip_trailing_punct_tokens(seg.split()))


def np_counts(no: list[str], final_keys: set[str], gold: set[str]) -> tuple[int, int]:
    """§7.5: (tp, m) of one caption. m = distinct neighbour-only classes still in the final caption, no prefix cut."""
    kept = {G.key(o) for o in no} & final_keys
    return sum(k in gold for k in kept), len(kept)


def np_summary(tp: list[int], m: list[int]) -> dict:
    """NP = 100 * sum tp / sum m (None when sum m = 0), with sum m and the share of images with m > 0 (J3)."""
    return {"np": 100 * sum(tp) / sum(m) if sum(m) else None, "np_sum_m": int(sum(m)),
            "np_share_m_pos": float(np.mean([x > 0 for x in m]))}


def nn_consensus(cands: dict[str, list[str]], pool: list[str], E4) -> dict[str, int]:
    """J5: per image, the index of the candidate with the highest mean CIDEr-D against the other k - 1, df from the
    memory caption pool; ties to the nearer cluster, then the lower cluster id (= the lower index of the ret list)."""
    refs = {f"{i}\t{j}": [c for n, c in enumerate(cs) if n != j] for i, cs in cands.items() for j in range(len(cs))}
    cid = E4.Cider(refs, df_refs=[[p] for p in pool])
    sc = dict(zip(cid.ids, cid.per_image({key: cands[key.split("\t")[0]][int(key.split("\t")[1])] for key in refs})))
    return {i: max(range(len(cs)), key=lambda j: (sc[f"{i}\t{j}"], -j)) for i, cs in cands.items()}


# ------------------------------------------------------------------------------------------------ score (M3)
def extras(ds: str, var: list, refs: dict, ctx: dict, seg: dict) -> list[dict]:
    """Per variant row: the PTB column, neighbour-only precision (tp, m per image) and the source-dataset share."""
    caps, E4, PTB = ctx["caps"], ctx["E4"], ctx["PTB"]
    ids, src = sorted(refs), C.DATASETS[ds]["src"]
    gold = {i: S.CH._gold_objects(refs[i]) for i in ids}
    cider_p = E4.Cider({i: [PTB.ptb(seg[x]) for x in refs[i]] for i in ids})
    out = []
    for r, z, (tau, capt, _cnt) in var:
        p = cider_p.per_image({i: PTB.ptb(seg[capt[i]]) for i in ids})
        row = {"run_id": r["run_id"], "tau": tau, "cider_ptb": float(p.mean()), "per_image": {"cider_ptb": p.round(
            4).tolist()}}
        if r is not z:
            shown = {i: [C.shown(caps[x], src) for x in r["exemplars"][i]] for i in ids}
            tm = [np_counts(G.neighbour_only(r["predictions"][i], z["predictions"][i], shown[i]),
                            {G.key(o) for o in G.classes(capt[i])}, gold[i]) for i in ids]
            row["per_image"].update(np_tp=[t for t, _m in tm], np_m=[m for _t, m in tm])
            row.update(np_summary(*zip(*tm)), src_share=float(np.mean(
                [np.mean([src in caps[x] for x in r["exemplars"][i]]) for i in ids])))
        out.append(row)
    return out


def plain_row(head: dict, capt: dict, refs: dict, ctx: dict, seg: dict) -> dict:
    """An NN baseline row (head: dataset, run_id, arm, k): CIDEr-D as written, stripped and PTB, CHAIR_i and
    mentions; no model, no guard."""
    E4, PA, PTB = ctx["E4"], ctx["PA"], ctx["PTB"]
    ids = sorted(refs)
    cw = E4.Cider({i: [seg[x] for x in refs[i]] for i in ids})
    cp = E4.Cider({i: [PTB.ptb(seg[x]) for x in refs[i]] for i in ids})
    w, s = cw.per_image({i: seg[capt[i]] for i in ids}), cw.per_image({i: stripped(PA, seg[capt[i]]) for i in ids})
    p = cp.per_image({i: PTB.ptb(seg[capt[i]]) for i in ids})
    ch = S.CH.chair({i: capt[i] for i in ids}, {i: refs[i] for i in ids})
    return {**head, "model": None, "order": None, "tpl": None,
            "tau": "-inf", "n": len(ids), "cider_w": float(w.mean()), "cider_s": float(s.mean()),
            "cider_ptb": float(p.mean()), "chair_i": ch.chair_i, "mentions_per_image": ch.mentions_per_caption,
            "per_image": {"ids": ids, "cider_s": s.round(4).tolist(), "cider_w": w.round(4).tolist(),
                          "cider_ptb": p.round(4).tolist()}}


def nn_rows(ds: str, refs: dict, ctx: dict, seg: dict) -> list[dict]:
    caps, PA, E4, ex, cfg = (ctx[k] for k in ("caps", "PA", "E4", "ex", "cfg"))
    ids, src = sorted(refs), C.DATASETS[ds]["src"]
    ret = ex["ret"][ds]
    top1 = plain_row({"dataset": ds, "run_id": f"c2_nn_{ds}-top1", "arm": "nn_top1", "k": 1},
                     {i: C.shown(caps[ret[i][0][0]], src) for i in ids}, refs, ctx, seg)
    top1["per_image"]["top1_cos"] = [ret[i][0][1] for i in ids]
    top1["dose_tertile_cuts"] = ex["dose_tertile_cuts"][ds]
    rows = [top1]
    pool = [stripped(PA, seg[C.shown(c, src)]) for c in caps.values()]
    for k in sorted({c["k"] for c in cfg["models"].values()}):
        cands = {i: [C.shown(caps[c], src) for c, _cos in ret[i][:k]] for i in ids}
        pick = nn_consensus({i: [stripped(PA, seg[c]) for c in cs] for i, cs in cands.items()}, pool, E4)
        rows.append(plain_row({"dataset": ds, "run_id": f"c2_nn_{ds}-cons-k{k}", "arm": "nn_cons", "k": k},
                              {i: cands[i][pick[i]] for i in ids}, refs, ctx, seg))
    return rows


def set_rows(ds: str, runs: list[dict], zs_by: dict, refs: dict, ctx: dict) -> list[dict]:
    """score_set's rows (the registered stage-1 metrics, unchanged) with the stage-2 extras, then the NN rows
    (ctx also holds the example lists `ex` and the frozen config `cfg`)."""
    base = S.score_set(ds, runs, zs_by, refs, ctx)
    todo = [(r, zs_by[r["model"]]) for r in runs] + [(z, z) for z in zs_by.values()]
    var = [(r, z, v) for r, z in todo for v in S.variants(r, z, ctx["cache"], ctx["caps"])]  # score_set's order
    src = C.DATASETS[ds]["src"]
    texts = sorted({c for *_x, (_t, capt, _n) in var for c in capt.values()} | {x for rs in refs.values() for x in rs}
                   | {C.shown(c, src) for c in ctx["caps"].values()})
    seg = dict(zip(texts, (s.lower() for s in ctx["segment"](texts))))
    rows = []
    for b, x in zip(base, extras(ds, var, refs, ctx, seg), strict=True):
        if (b["run_id"], b["tau"]) != (x["run_id"], x["tau"]):
            raise SystemExit("score: the variant order differs from score_set's")
        rows.append({**b, **{k: v for k, v in x.items() if k != "per_image"},
                     "per_image": {**b["per_image"], **x["per_image"]}})
    return rows + [{**r, "inputs": ctx.get("inputs", {})} for r in nn_rows(ds, refs, ctx, seg)]


def cmd_score(a) -> None:
    lists = C.load_lists(a.lists)
    cfg = S2.frozen()
    E4, PA, PTB = kit2(a.kit_b)
    if lb.sha256_file(E4.VNC / "VnCoreNLP-1.2.jar") != S.JAR_SHA256:
        raise SystemExit(f"{E4.VNC}/VnCoreNLP-1.2.jar is not the jar of Paper B's protocol card")
    caps = C.memory_captions(lists)
    cache = S.load_cache(a.cache)
    runs, zss = [G.read_preds(p) for p in a.runs], [G.read_preds(p) for p in a.zs]
    g = S2.grid(cfg)
    for r in runs + zss:
        if r["run_id"] not in g or r.get("c_schema") != S2.SCHEMA or r["dataset"] != a.set:
            raise SystemExit(f"{r['run_id']}: not a stage-2 output of {a.set}")
    for z in zss:
        S2.zs_ok2(z, z["model"], a.set)
    ex = C.load_exemplars(a.exemplars, a.lists)
    if ex.get("set") != a.set:
        raise SystemExit(f"{a.exemplars}: not the example lists of {a.set}")
    refs = S2.references2(a.set, lists)
    zs_by = {z["model"]: z for z in zss}
    ctx = {"cache": cache, "caps": caps, "segment": E4.rdr, "E4": E4, "PA": PA, "PTB": PTB,
           "inputs": {"lists_sha256": lb.sha256_file(a.lists), "exemplars_sha256": S2.sha_file(a.exemplars),
                      "cache_sha256": {Path(p).name: lb.sha256_file(Path(p)) for p in a.cache}}}
    rows = set_rows(a.set, runs, zs_by, refs, {**ctx, "ex": ex, "cfg": cfg})
    stamp = {"label": S2.LABEL, "c_schema": S2.SCHEMA, "c_prereg_sha256": S2.PINS[S2.PREREG],
             "frozen_config_sha256": S2.PINS[S2.FROZEN], "utc": lb.utc()}
    with Path(a.ledger).open("a", encoding="utf-8") as f:
        f.writelines(json.dumps({**r, **stamp}, ensure_ascii=False) + "\n" for r in rows)
    print(f"appended {len(rows)} rows to {a.ledger}")


# ------------------------------------------------------------------------------------------------ verified (local)
def oiv7_counts(mentions: set[str], final: set[str], no: list[str] | None, st: dict, classes: set,
                XO) -> tuple[int, int, int, int]:
    """(present, absent) mapped mentions of a caption (Paper A's caption_rows), and its neighbour-only (tp, m)
    counting only classes OIV7 verifies (§7.5, XM gold). final: the canonical keys of the caption's classes."""
    cr = XO.caption_rows(mentions, st, set(), classes)
    if no is None:
        return cr[1], cr[2], 0, 0
    kept = [o for o in dict.fromkeys(no) if G.key(o) in final and st.get(o) in ("present", "absent")]
    return cr[1], cr[2], sum(st[o] == "present" for o in kept), len(kept)


def cmd_verified(a) -> None:
    if os.environ.get("VSPS_MACHINE_ID"):
        raise SystemExit("verified precision is scored locally only; VSPS_MACHINE_ID is set")
    import xm3600_oiv7 as XO

    lists = C.load_lists(a.lists)
    ids = sorted(i for i, _f, _h in S2.manifest2("xm_dev500", lists))
    runs, zss = [G.read_preds(p) for p in a.runs], [G.read_preds(p) for p in a.zs]
    g = S2.grid(S2.frozen())
    for r in runs + zss:
        if r["run_id"] not in g or r["dataset"] != "xm_dev500" or sorted(r["predictions"]) != ids:
            raise SystemExit(f"REFUSED: {r['run_id']} is not a stage-2 run on exactly the XM-dev500 images")
    for z in zss:
        S2.zs_ok2(z, z["model"], "xm_dev500")
    vmap = XO.resolve_map(a.desc)
    labels = json.loads(Path(a.labels).read_text(encoding="utf-8"))
    st = XO.statuses(vmap, {i: labels[i] for i in ids if i in labels})
    cache, caps = S.load_cache(a.cache), C.memory_captions(lists)
    zs_by = {z["model"]: z for z in zss}
    rows = []
    for r, z in [(r, zs_by[r["model"]]) for r in runs] + [(z, z) for z in zss]:
        for tau, capt, _cnt in S.variants(r, z, cache, caps):
            no = {i: None if r is z else G.neighbour_only(r["predictions"][i], z["predictions"][i], [
                C.shown(caps[x], "xm3600") for x in r["exemplars"][i]]) for i in ids}
            c = np.array([oiv7_counts(set(G.objects_in(capt[i])), {G.key(o) for o in G.classes(capt[i])}, no[i],
                                      st.get(i, {}), set(vmap), XO) for i in ids])
            rows.append({"label": S2.LABEL, "c_schema": S2.SCHEMA, "run_id": r["run_id"], "model": r["model"],
                         "dataset": "xm_dev500", **{k: r["spec"][k] for k in ("arm", "k", "order", "tpl")},
                         "tau": tau, "n": len(ids),
                         "vp": 100 * c[:, 0].sum() / max(c[:, 0].sum() + c[:, 1].sum(), 1),
                         **({} if r is z else {"npx": np_summary(c[:, 2].tolist(), c[:, 3].tolist())}),
                         "per_image": {"ids": ids, "vp_p": c[:, 0].tolist(), "vp_a": c[:, 1].tolist(),
                                       "npx_tp": c[:, 2].tolist(), "npx_m": c[:, 3].tolist()},
                         "inputs": {"run_sha256": r["_sha256"], "zs_sha256": z["_sha256"],
                                    "labels_sha256": S2.sha_file(a.labels), "desc_sha256": S2.sha_file(a.desc),
                                    "map_sha256": S2.sha_file(XO.MAP),
                                    "cache_sha256": {Path(p).name: S2.sha_file(p) for p in a.cache}},
                         "c_prereg_sha256": S2.PINS[S2.PREREG], "utc": lb.utc()})
    with Path(a.ledger).open("a", encoding="utf-8") as f:
        f.writelines(json.dumps(x) + "\n" for x in rows)
    print(f"appended {len(rows)} verified rows to {a.ledger}")


# ------------------------------------------------------------------------------------------------ self-test (CPU)
def selftest(kit_dir: Path) -> None:
    E4, PA, PTB = kit2(kit_dir)
    assert PTB.ptb("w1 . w2 , w3 ...") == "w1 w2 w3" and stripped(PA, "w1 w2 .") == "w1 w2"
    # J3: distinct neighbour-only classes still in the final caption, all of them (no prefix)
    assert np_counts(["c1", "c2", "c3"], {"c1", "c3", "c9"}, {"c1"}) == (1, 2)
    assert np_counts(["c1"], set(), {"c1"}) == (0, 0), "a fallback or deleted caption adds nothing"
    sm = np_summary([1, 0, 0], [2, 0, 1])
    assert sm == {"np": 100 / 3, "np_sum_m": 3, "np_share_m_pos": 2 / 3} and np_summary([0], [0])["np"] is None
    # J5: consensus by mean CIDEr-D against the others, df from the pool, ties to the nearer cluster
    pool = ["w1 w2 w3", "w4 w5 w6", "w7 w8 w9", "w1 w2 w4"]
    pick = nn_consensus({"a": ["w7 w8 w9", "w1 w2 w3", "w1 w2 w3"], "b": ["w4 w5", "w4 w5"],
                         "c": ["w5 w6", "w1 w2 w3 w4", "w1 w2 w3"]}, pool, E4)
    assert pick == {"a": 1, "b": 0, "c": 1}, pick  # a, b: ties go to the nearer cluster; c: a clear winner
    # extras on a synthetic run: PTB column, tp/m, source share; the zero-shot row has none of them
    caps = {"m0": {"ktvic": "w1 w2"}, "m1": {"openviic": "w3 w4"}}
    zs = {"run_id": "z", "predictions": {"i1": "w1", "i2": "w5"}}
    run = {"run_id": "r", "predictions": {"i1": "w1 w2 .", "i2": "w5 w6"},
           "exemplars": {"i1": ["m0", "m1"], "i2": ["m1", "m1"]}}
    seg = {t: t for t in ("w1", "w5", "w1 w2 .", "w1 w2", "w2 w3 .", "w5 w6")}
    x = extras("ov_dev_b", [(run, zs, ("-inf", run["predictions"], {})), (zs, zs, ("-inf", zs["predictions"], {}))],
               {"i1": ["w1 w2", "w2 w3 ."], "i2": ["w5 w6"]}, {"caps": caps, "E4": E4, "PTB": PTB}, seg)
    assert x[0]["src_share"] == 0.75 and x[0]["per_image"]["np_m"] == [0, 0] and "np_m" not in x[1]["per_image"]
    assert x[0]["per_image"]["cider_ptb"][0] > x[1]["per_image"]["cider_ptb"][0], "the PTB column scores the run"
    import xm3600_oiv7 as XO

    st = {"c1": "present", "c2": "absent"}
    assert oiv7_counts({"c1", "c2", "c3"}, {"c1", "c2", "c3"}, ["c1", "c2", "c3"], st, {"c1", "c2", "c3"}, XO) == (
        1, 1, 1, 2), "unverified c3 counts in neither sum"
    assert oiv7_counts({"c1"}, {"c1"}, None, st, {"c1"}, XO) == (1, 0, 0, 0), "a zs row has no neighbour-only part"
    # set_rows: score_set on a stage-2 set name, merged with the extras, plus the NN rows (synthetic tokens)
    cfg = S2.frozen()
    ids = [f"i{n}" for n in range(4)]
    caps = {f"m{n}": {"openviic": f"w{n} w{n + 1} w{n + 2}"} for n in range(9)}
    refs = {i: [f"w{n} w{n + 1} w{n + 3}", f"w{n + 1} w{n + 2}"] for n, i in enumerate(ids)}
    ex = {"ret": {"ov_dev_b": {i: [[f"m{(n + j) % 9}", 0.9 - j / 10] for j in range(8)] for n, i in enumerate(ids)}},
          "dose_tertile_cuts": {"ov_dev_b": [0.5, 0.7]}}

    def fake(arm, preds, m="qwen25vl_7b"):
        sp = S2.spec(cfg, "ov_dev_b", m, arm)
        exids = {i: [] if arm == "zs" else [c for c, _x in ex["ret"]["ov_dev_b"][i][:8]] for i in ids}
        return {"run_id": sp["run_id"], "model": m, "dataset": "ov_dev_b", "spec": sp, "predictions": preds,
                "exemplars": exids, "hit_max": {i: False for i in ids}, "_sha256": "f" * 64}

    zs = fake("zs", {i: "w0 w1 ." for i in ids})
    ret = fake("ret", {i: f"w{n} w{n + 1} w{n + 2} ." for n, i in enumerate(ids)})
    ctx = {"cache": {}, "caps": caps, "segment": list, "E4": E4, "PA": PA,
           "PTB": PTB, "ex": ex, "cfg": cfg}
    rows = set_rows("ov_dev_b", [ret], {"qwen25vl_7b": zs}, refs, ctx)
    by = {(r["run_id"], r["tau"]): r for r in rows}
    assert set(by) == {(ret["run_id"], t) for t in S2.TAUS} | {(zs["run_id"], "-inf"),  # no items: cache complete
                       ("c2_nn_ov_dev_b-top1", "-inf"), ("c2_nn_ov_dev_b-cons-k4", "-inf"),
                       ("c2_nn_ov_dev_b-cons-k8", "-inf")}, sorted(by)
    r0 = by[(ret["run_id"], "-inf")]
    assert {"cider_s", "pcm_vs_zs", "cider_ptb", "np_sum_m", "src_share"} <= set(r0) and r0["src_share"] == 1.0
    assert len(r0["per_image"]["np_m"]) == 4 and by[("c2_nn_ov_dev_b-top1", "-inf")]["per_image"]["top1_cos"][0] == 0.9
    print("selftest ok: kit + PTB pin, neighbour-only precision (J3), NN-consensus df and ties (J5), extras rows, "
          "score_set on a stage-2 set with the merged rows and the NN rows")


def main() -> None:
    ap = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    ap.add_argument("--selftest", action="store_true")
    ap.add_argument("--kit-b", type=Path, default=S2.ROOT / "scripts/kit_b")
    sub = ap.add_subparsers(dest="cmd")
    for name in ("score", "verified"):
        p = sub.add_parser(name)
        if name == "score":
            p.add_argument("--set", choices=sorted(S2.SETS), required=True)
            p.add_argument("--exemplars", type=Path, required=True)
            p.add_argument("--kit-b", type=Path, default=S2.ROOT / "scripts/kit_b")
        else:
            p.add_argument("--labels", type=Path, required=True, help="data/xm3600/oiv7_labels.json (local)")
            p.add_argument("--desc", type=Path, required=True, help="oidv7-class-descriptions.csv")
        p.add_argument("--runs", nargs="*", type=Path, default=[])
        p.add_argument("--zs", nargs="+", type=Path, required=True)
        p.add_argument("--cache", nargs="*", type=Path, default=[])
        p.add_argument("--lists", type=Path, required=True)
        p.add_argument("--ledger", required=True)
    a = ap.parse_args()
    if a.selftest:
        return selftest(a.kit_b)
    {"score": cmd_score, "verified": cmd_verified}.get(a.cmd, lambda _a: ap.error("mode?"))(a)


if __name__ == "__main__":
    main()
