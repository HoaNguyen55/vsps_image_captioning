#!/usr/bin/env python3
"""C-ATTR-DEV statistics (CPU, laptop). Registration manuscript/prereg/2026-11-11_c_attr_dev/C_ATTR_DEV_PREREG_v1_1.md
§7 (estimands, one image-bootstrap index matrix per set, the p-like statistic, labels, the one DETECTED rule with Holm
step-down at family-wise one-sided 0.025, nomination, variance and the fixed-set ANOVA) and §8 (copy bound), CC-331 X1-X3,
CC-332 notes. Label on every output: DEVELOPMENT / C-ATTR-DEV, NON-CONFIRMATORY.

  python -I -B scripts/c_attr/c_attr_score.py --selftest                       planted data only
  python -I -B scripts/c_attr/c_attr_score.py score ... [--nomination F]       per-image scores (c_attr.cmd_score, kit B)
  python -I -B scripts/c_attr/c_attr_score.py nominate --ledger L ... --out c_attr_nomination.json   OV-dev-A (§7.5)
  python -I -B scripts/c_attr/c_attr_score.py summary --ledger L ... [--nomination F] --out S
  python -I -B scripts/c_attr/c_attr_score.py copybound --set S --zs Z --ret R --rand D --kit-b K --c-lists L
                                                        --c2-ledger G --c2-run Q --out O     §8, CPU

Outputs hold ids and numbers only; nothing prints a caption. lmcap_rand / lmcap_perm rows are a re-implementation of
the LMCap recipe by this study; ret_img vs rand_img rows are an image-caption-pair prompt format, as used by RAGCap;
not RAGCap. No row says that a published system was tested.
"""
from __future__ import annotations

import argparse
import json
import sys
from pathlib import Path

import numpy as np

sys.path.insert(0, str(Path(__file__).resolve().parent))
import c_attr as A  # noqa: E402

SESOI, ALPHA = A.SESOI, 0.025  # §7.4: +2.0; family-wise one-sided alpha (X1)
SPLIT = "split of a known τ_sel"  # X2: every τ_pair / τ_marg row on OV-dev-A or OV-dev-B
KNOWN_SUM = ("ov_dev_a", "ov_dev_b")
OLD3 = ("qwen25vl_7b", "internvl3_8b", "aya_vision_8b")
NOMINATORS = ("qwen25vl_7b", "internvl3_8b")  # §7.5 item 1
REG_RDF = {"ov_dev_a": (1, 2, 1), "ov_dev_b": (3, 2, 5), "xm_dev500": (3, 2, 5), "f30k_val": (3, 2, 0)}  # §7.2


# ------------------------------------------------------------------------------------------------ §7.3-7.4
def summary(point: float, bm: np.ndarray) -> dict:
    lo, hi, lo90, hi90 = np.percentile(bm, [2.5, 97.5, 5, 95])
    return {"d": float(point), "lo": float(lo), "hi": float(hi), "lo90": float(lo90), "hi90": float(hi90),
            "p": float((1 + np.sum(bm <= 0)) / (len(bm) + 1)), "_bm": bm}


def pair(a, b, idx: np.ndarray) -> dict:
    """Paired image bootstrap of mean(a - b): the same resampled images for both arms."""
    a, b = np.asarray(a, float), np.asarray(b, float)
    rows = idx  # one index matrix per set, shared by every contrast on that set (§7.3)
    return summary(a.mean() - b.mean(), a[rows].mean(1) - b[rows].mean(1))


def detected(claims: dict[str, tuple[float, float]], alpha: float = ALPHA) -> set[str]:
    """§7.4 DETECTED over one family {name: (point, p)}: Holm step-down at family-wise one-sided alpha, the j-th
    smallest p against alpha / (m - j + 1), and point >= +2.0; stop at the first failure (strict reading: a claim that
    fails either condition ends the step-down). A row outside every family is a family of m = 1."""
    m, out = len(claims), set()
    for j, (k, (d, p)) in enumerate(sorted(claims.items(), key=lambda kv: (kv[1][1], kv[0])), 1):
        if not (d >= SESOI and p <= alpha / (m - j + 1)):
            break
        out.add(k)
    return out


def label(s: dict, is_detected: bool) -> str:
    """Mutually exclusive labels, first match: DETECTED, REVERSED (95% upper < 0), NEGLIGIBLE (90% interval inside
    (-2.0, +2.0)), UNRESOLVED."""
    if is_detected:
        return "DETECTED"
    if s["hi"] < 0:
        return "REVERSED"
    if s["lo90"] > -SESOI and s["hi90"] < SESOI:
        return "NEGLIGIBLE"
    return "UNRESOLVED"


def arm_mean(per: dict, m: str, arm: str) -> tuple[np.ndarray | None, int]:
    """Per-image mean over the draws / permutations / fixed sets present for (model, arm), and their number."""
    keys = sorted(k for k in per if k.startswith(f"{m}|{arm}"))
    return (np.mean([per[k] for k in keys], axis=0), len(keys)) if keys else (None, 0)


def set_rows(per: dict, ds: str, idx: np.ndarray) -> dict[str, dict]:
    """§7.2 estimands per backbone on one set: tau_any, tau_sel, tau_marg, tau_pair, and the rand d1 - d2 placebo."""
    rows = {}
    for m in sorted({k.split("|")[0] for k in per}):
        zs, ret = per.get(f"{m}|zs"), per.get(f"{m}|ret")
        rand, r = arm_mean(per, m, "rand_d")
        perm, d = arm_mean(per, m, "perm_p")
        for est, a, b in (("tau_any", rand, zs), ("tau_sel", ret, rand), ("tau_marg", perm, rand),
                          ("tau_pair", ret, perm)):
            if a is not None and b is not None:
                rows[f"{m}|{est}"] = {**pair(a, b, idx), "model": m, "estimand": est, "R": r, "D": d,
                                      "registered_R_D": REG_RDF.get(ds, (None, None))[:2]}
        if f"{m}|rand_d1" in per and f"{m}|rand_d2" in per:
            pl = pair(per[f"{m}|rand_d1"], per[f"{m}|rand_d2"], idx)
            rows[f"{m}|placebo_d1_d2"] = {**pl, "model": m, "estimand": "placebo rand d1 - rand d2",
                                         "flag": bool(abs(pl["d"]) >= SESOI and (pl["lo"] > 0 or pl["hi"] < 0))}
    return rows


def apply_labels(rows: dict, ds: str, families: dict[str, list[str]]) -> None:
    """Families: {name: [row keys]}; every other row is its own family of m = 1. Notes: X2 on the known-sum sets."""
    fam_of = {k: f for f, ks in families.items() for k in ks if k in rows}
    det = set()
    for f, ks in families.items():
        det |= detected({k: (rows[k]["d"], rows[k]["p"]) for k in ks if k in rows})
    for k, r in rows.items():
        if k not in fam_of:
            det |= detected({k: (r["d"], r["p"])})
        r["label"], r["family"] = label(r, k in det), fam_of.get(k)
        r["m"] = len([x for x in families.get(fam_of.get(k), [k]) if x in rows]) if k in fam_of else 1
        if r.get("estimand") in ("tau_pair", "tau_marg") and ds in KNOWN_SUM:
            r["note"] = SPLIT
        r["tag"] = A.LABEL


# ------------------------------------------------------------------------------------------------ §7.5 nomination
def nominate(rows_a: dict) -> list[str]:
    """OV-dev-A: H_pair(m) / H_marg(m) when the 95% lower bound of tau_pair / tau_marg is >= +2.0 (c_t1.advance)."""
    out = []
    for m in NOMINATORS:
        for est, h in (("tau_pair", "H_pair"), ("tau_marg", "H_marg")):
            r = rows_a.get(f"{m}|{est}")
            if r is not None and A.advance(r) == "NOMINATE":
                out.append(f"{h}({m})")
    return out


def family_keys(nominated: list[str]) -> list[str]:
    est = {"H_pair": "tau_pair", "H_marg": "tau_marg"}
    return [f"{c.split('(')[1].rstrip(')')}|{est[c.split('(')[0]]}" for c in nominated]


def ovb_perm_scored(ledger_rows: list[dict]) -> bool:
    return any(r.get("dataset") == "ov_dev_b" and r.get("arm") == "perm" for r in ledger_rows)


# ------------------------------------------------------------------------------------------------ §7.7 variance
def draw_variance(per: dict, m: str, ret: np.ndarray | None) -> dict | None:
    """§7.7a: mean within-image variance over draws, its share of the image-bootstrap variance of ret - rand mean."""
    keys = sorted(k for k in per if k.startswith(f"{m}|rand_d"))
    if len(keys) < 2 or ret is None:
        return None
    x = np.array([per[k] for k in keys])
    n, r = x.shape[1], x.shape[0]
    s2w = float(x.var(axis=0, ddof=1).mean())
    total = float(np.var(ret - x.mean(0), ddof=1) / n)
    return {"sigma2_w": s2w, "draw_part": s2w / (n * r), "total": total, "share": s2w / (n * r) / total if total else None}


def anova_fix(y: np.ndarray) -> dict:
    """§7.7b, y = s(ret) - s(fix_F), n x R_F, one value per cell. V_b, V_img, omega, the F-based upper bound and the
    five-set development row (t interval, R_F - 1 df)."""
    from scipy import stats

    n, rf = y.shape
    g, gi, gf = y.mean(), y.mean(1), y.mean(0)
    ms_f = n * np.sum((gf - g) ** 2) / (rf - 1)
    ms_i = rf * np.sum((gi - g) ** 2) / (n - 1)
    ms_e = np.sum((y - gi[:, None] - gf[None, :] + g) ** 2) / ((n - 1) * (rf - 1))
    v_b = max(0.0, (ms_f - ms_e) / n)
    v_a = max(0.0, (ms_i - ms_e) / rf)  # image component, printed beside
    v_img = float(np.mean([np.var(y[:, f], ddof=1) / n for f in range(rf)]))
    f05 = float(stats.f.ppf(0.05, rf - 1, (rf - 1) * (n - 1)))
    v_bu = max(0.0, (ms_f / f05 - ms_e) / n)
    omega, omega_u = v_b / v_img, v_bu / v_img
    se = float(np.sqrt(max(ms_f + ms_i - ms_e, 0.0) / (n * rf)))
    t = float(stats.t.ppf(0.975, rf - 1))
    return {"MS_F": float(ms_f), "MS_I": float(ms_i), "MS_E": float(ms_e), "V_b": v_b, "V_a": v_a, "V_img": v_img,
            "F_0.05": f05, "V_b_upper": v_bu, "omega": omega, "omega_upper": omega_u,
            "label": "the fixed-set rows are practically unconditional" if omega_u <= 0.25
            else "conditional on the realised fixed set", "dev_row": {"d": float(g), "se": se, "lo": float(g) - t * se,
                                                                     "hi": float(g) + t * se, "df": rf - 1}}


# ------------------------------------------------------------------------------------------------ §8 copy bound
def copy_loss(caps: dict, shown: dict, refs: dict, score, n: int) -> np.ndarray:
    """loss(y; S) = s(y) - s(masked_n(y, S)) per image (ids sorted), the same references and document frequencies;
    the references are never masked."""
    ids = sorted(caps)
    plain = score({i: caps[i] for i in ids}, refs)
    mk = score({i: A.masked(caps[i], shown[i], n) or "." for i in ids}, refs)
    return np.asarray(plain, float) - np.asarray(mk, float)


def kappa(loss_arm: np.ndarray, loss_zs: np.ndarray) -> np.ndarray:
    """κ_q = loss(y_arm; R_q) - loss(y_zs; R_q): the zs caption never saw R_q (the placebo)."""
    return loss_arm - loss_zs


def copy_bound(ds: str, caps: dict, s: dict, r_q: dict, own_rand: dict, refs: dict, score, idx) -> dict:
    """caps / s: {'zs','ret','rand'} captions and per-image scores (ids sorted); r_q: the ret run's shown captions;
    own_rand: the rand d0 run's own shown captions. K_ret, L_cp, K_nc, K_rand at n = 2, 3, 4 (n = 3 decides)."""
    tier = "first look" if ds == "xm_dev500" else "POST HOC"
    out = {}
    for n in (2, 3, 4):
        lz = copy_loss(caps["zs"], r_q, refs, score, n)
        kq = kappa(copy_loss(caps["ret"], r_q, refs, score, n), lz)
        rows = {"K_ret": pair(kq, np.zeros_like(kq), idx),
                "L_cp": pair(np.asarray(s["ret"]) - np.asarray(s["rand"]) - kq, np.zeros_like(kq), idx),
                "K_nc": pair(kappa(copy_loss(caps["rand"], r_q, refs, score, n), lz), np.zeros_like(kq), idx),
                "K_rand": pair(kappa(copy_loss(caps["rand"], own_rand, refs, score, n),
                                     copy_loss(caps["zs"], own_rand, refs, score, n)), np.zeros_like(kq), idx)}
        for k, r in rows.items():
            r["label"], r["tier"], r["tag"] = label(r, bool(detected({k: (r["d"], r["p"])}))), tier, A.LABEL
        rows["withdrawn"] = rows["K_nc"]["label"] == "REVERSED"
        out[f"n{n}"] = rows
    out["monotonicity check failed"] = out["n4"]["K_ret"]["d"] > out["n2"]["K_ret"]["d"]
    return out


def kit_scorer(kit_b: Path):
    """Stripped CIDEr-D through kit B (score2.kit2: RDRSegmenter, lower-cased), df over the given references."""
    import score2 as S2s

    E4, PA, _ptb = S2s.kit2(kit_b)

    def score(capt: dict, refs: dict) -> np.ndarray:
        ids = sorted(capt)
        texts = sorted(set(capt.values()) | {x for i in ids for x in refs[i]})
        seg = dict(zip(texts, (t.lower() for t in E4.rdr(texts))))
        cider = E4.Cider({i: [seg[x] for x in refs[i]] for i in ids})
        return np.asarray(cider.per_image({i: " ".join(PA.strip_trailing_punct_tokens(seg[capt[i]].split()))
                                           for i in ids}), float)
    return score


# ------------------------------------------------------------------------------------------------ CLI
def strip(o):
    return {k: strip(v) for k, v in o.items() if k != "_bm"} if isinstance(o, dict) else o


def cmd_score(a) -> None:
    runs = [json.loads(Path(p).read_text(encoding="utf-8")) for p in a.runs]
    if a.set == "ov_dev_b" and any(r.get("spec", {}).get("arm") == "perm" for r in runs):
        if not a.nomination or not Path(a.nomination).is_file():  # §7.5 item 2, Binding 8
            raise SystemExit("REFUSED: OV-dev-B perm outputs are scored only after the nomination file is hashed")
        print(f"nomination file sha256 {A.sha(a.nomination)}")
    A.cmd_score(a)


def cmd_nominate(a) -> None:
    led = A.read_ledgers(a.ledger)
    if ovb_perm_scored(led) or any(Path(a.ledger[0]).parent.glob("*ov_dev_b*perm*")):
        raise SystemExit("REFUSED: an OV-dev-B perm score exists; the nomination comes first (§7.5)")
    per, _p, ids = A.set_columns(led, "ov_dev_a", "vi")
    rows = set_rows(per, "ov_dev_a", A.boot_idx(len(ids)))
    apply_labels(rows, "ov_dev_a", {})
    rec = {"label": A.LABEL, "rule": "95% lower bound >= +2.0 on OV-dev-A (c_t1.advance)", "note": SPLIT,
           "nominated": nominate(rows), "rows": strip({k: v for k, v in rows.items() if k.split("|")[0] in NOMINATORS})}
    Path(a.out).write_text(json.dumps(rec, indent=1, ensure_ascii=False) + "\n", encoding="utf-8")
    print(f"nominated {rec['nominated'] or 'nothing'}; {a.out} sha256 {A.sha(a.out)} (write it to the LOG first)")


def cmd_summary(a) -> None:
    led = A.read_ledgers(a.ledger)
    nom = json.loads(Path(a.nomination).read_text(encoding="utf-8"))["nominated"] if a.nomination else []
    res = {"label": A.LABEL, "alpha_familywise_one_sided": ALPHA, "sesoi": SESOI, "nominated": nom,
           "nomination_sha256": A.sha(a.nomination) if a.nomination else None, "sets": {}}
    for ds in ("ov_dev_a", "ov_dev_b", "xm_dev500", "f30k_val"):
        per, _p, ids = A.set_columns(led, ds, A.SETS[ds])
        if not per:
            continue
        idx = A.boot_idx(len(ids))  # one index matrix per set
        rows = set_rows(per, ds, idx)
        fam = {}
        if ds == "ov_dev_b":
            fam = {"registered (§7.5)": family_keys(nom),
                   "S-BB (§7.6)": [f"{m}|tau_sel" for m in sorted({k.split("|")[0] for k in per}) if m not in OLD3]}
        apply_labels(rows, ds, fam)
        if ds == "ov_dev_b" and not nom:
            res["no_claim"] = "no claim was nominated on OV-dev-A"
        var = {m: draw_variance(per, m, per.get(f"{m}|ret")) for m in sorted({k.split("|")[0] for k in per})}
        fx = {}
        for m in sorted({k.split("|")[0] for k in per}):
            fk = sorted(k for k in per if k.startswith(f"{m}|fix_f"))
            if len(fk) >= 2 and f"{m}|ret" in per:
                fx[m] = anova_fix(np.array([per[f"{m}|ret"] - per[k] for k in fk]).T)
        res["sets"][ds] = {"n": len(ids), "rows": strip(rows), "variance": var, "fixed_set": fx}
    Path(a.out).write_text(json.dumps(res, indent=1, ensure_ascii=False) + "\n", encoding="utf-8")
    print(json.dumps({ds: {k: v["label"] for k, v in s["rows"].items()} for ds, s in res["sets"].items()},
                     ensure_ascii=False))


def cmd_copybound(a) -> None:
    """§8 on stored outputs (block 0 step 0.3; runs only after the code read GO). Scoring parity gate first (§7.1)."""
    import stage2 as ST2

    clists = A.C.load_lists(a.c_lists)
    refs = ST2.references2(a.set, clists) if a.set != "ov_dev_a" else None
    score = kit_scorer(a.kit_b)
    q = A.stored_run(Path(a.c2_run))
    old = [json.loads(x) for x in Path(a.c2_ledger).read_text(encoding="utf-8").splitlines() if x.strip()]
    if A.sha(a.c2_ledger) != A.C2_LEDGER_SHA256:
        raise SystemExit("not the stage-2 ledger")
    ref_b = ST2.references2("ov_dev_b", clists)
    want = next(r for r in old if r.get("run_id") == q["run_id"] and r.get("tau") == "-inf" and r.get("variant") is None)
    got = score(q["predictions"], ref_b)
    if want["per_image"]["ids"] != sorted(q["predictions"]) or np.abs(got - np.array(want["per_image"]["cider_s"])).max() > A.C2_PARITY_TOL:
        raise SystemExit("SCORING PARITY FAIL (§7.1): no copy-bound row")
    runs = {k: A.as_run(Path(p)) for k, p in (("zs", a.zs), ("ret", a.ret), ("rand", a.rand))}
    caps = {k: r["predictions"] for k, r in runs.items()}
    ids = sorted(caps["ret"])
    mem = A.C.memory_captions(clists)
    src = A.C.DATASETS[a.set]["src"]
    r_q = {i: [A.C.shown(mem[c], src) for c in runs["ret"]["exemplars"][i]] for i in ids}
    own = {i: [A.C.shown(mem[c], src) for c in runs["rand"]["exemplars"][i]] for i in ids}
    s = {k: score(caps[k], refs) for k in ("ret", "rand")}
    res = {"label": A.LABEL, "set": a.set, "inputs": {k: r["_sha256"] for k, r in runs.items()},
           "bound": strip(copy_bound(a.set, caps, s, r_q, own, refs, score, A.boot_idx(len(ids))))}
    Path(a.out).write_text(json.dumps(res, indent=1, ensure_ascii=False) + "\n", encoding="utf-8")
    print(f"copy bound {a.set}: {a.out} sha256 {A.sha(a.out)}")


# ------------------------------------------------------------------------------------------------ self-test
def selftest() -> None:
    ok, rng = [], np.random.default_rng(11)
    n = 600
    base = rng.normal(40, 10, n)
    rand = [base + rng.normal(0, 4, n) for _ in range(3)]
    perm = [r + 0 for r in (rand[0], rand[1])]
    per = {"qwen25vl_7b|zs": base - 5, "qwen25vl_7b|rand_d0": rand[0], "qwen25vl_7b|rand_d1": rand[1],
           "qwen25vl_7b|rand_d2": rand[2], "qwen25vl_7b|perm_p1": perm[0], "qwen25vl_7b|perm_p2": perm[1]}
    per["qwen25vl_7b|ret"] = np.mean(perm, 0) + 3  # registered planted case: ret = perm + 3, perm = rand
    calls = []
    real = A.boot_idx
    A.boot_idx = lambda k: calls.append(k) or real(k)
    try:
        idx = A.boot_idx(n)
        rows = set_rows({**per, "qwen25vl_7b|rand_d2": np.mean(perm, 0) * 3 - rand[0] - rand[1]}, "ov_dev_b", idx)
    finally:
        A.boot_idx = real
    assert len(calls) == 1, "one index matrix per set"
    assert abs(rows["qwen25vl_7b|tau_pair"]["d"] - 3) < 1e-9 and abs(rows["qwen25vl_7b|tau_marg"]["d"]) < 1e-9, \
        "ret = perm + 3 and perm = rand give tau_pair = 3, tau_marg = 0"
    r2 = set_rows(per, "ov_dev_b", idx)
    assert abs(r2["qwen25vl_7b|tau_sel"]["d"] - (per["qwen25vl_7b|ret"] - np.mean(rand, 0)).mean()) < 1e-9, \
        "rand is the mean over the draws"
    bm = {k: r2[f"qwen25vl_7b|{k}"]["_bm"] for k in ("tau_sel", "tau_marg", "tau_pair")}
    assert np.allclose(bm["tau_sel"], bm["tau_marg"] + bm["tau_pair"]), "replicate-wise identity: one shared matrix"
    pp = pair(base, base - 3, idx)
    assert pp["hi"] - pp["lo"] < 1e-9 and abs(pp["d"] - 3) < 1e-9, "paired bootstrap"
    ok.append("estimands (planted ret = perm + 3, perm = rand), draw mean, one index matrix, paired, identity")
    a3 = ALPHA / 3
    t = {"a": (2.0, a3), "b": (2.0, ALPHA / 2), "c": (2.0, ALPHA)}
    assert detected(t) == {"a", "b", "c"}, "boundary (θ̂ = 2.0; p = α_j): both inclusive"
    assert detected({**t, "a": (1.999, a3)}) == set(), "a point below +2.0 fails (and ends the step-down)"
    assert detected({"a": (5, 0.004), "b": (5, 0.011), "c": (5, 0.02)}) == {"a", "b", "c"}
    assert detected({"a": (5, 0.009), "b": (5, 0.010), "c": (5, 0.012)}) == set(), "Holm: 0.009 > 0.025 / 3"
    assert detected({"a": (5, 0.005), "b": (5, 0.013), "c": (5, 0.014)}) == {"a"}, "step-down stops at the first failure"
    assert detected({"a": (5, 0.012), "b": (5, 0.02), "c": (5, 0.03)}) == set(), "alpha is 0.025, not 0.05"
    assert detected({"x": (2.0, 0.025)}) == {"x"} and detected({"x": (2.0, 0.02500001)}) == set(), "m = 1"
    ok.append("Holm toy cases at one-sided 0.025, boundary (θ̂ = 2.0; p = α_j)")
    agree, k50 = 0, 0  # m = 1: the p rule equals '95% percentile lower bound > 0' unless exactly 50 of 2,000 means <= 0
    for s in range(300):
        g = np.random.default_rng(100 + s)
        x = g.normal(g.uniform(-0.5, 2.5), 8, 300)
        st = pair(x, np.zeros(300), real(300))
        kneg = int(np.sum(st["_bm"] <= 0))
        if kneg == 50:
            k50 += 1
            continue
        assert (st["p"] <= ALPHA) == (st["lo"] > 0), (s, kneg)
        agree += 1
    edge = summary(1.0, np.array([-1.0] * 49 + [-0.001] + [1.0] * 1950))
    assert edge["lo"] > 0 and edge["p"] > ALPHA, "50 means <= 0: lower bound > 0 but p = 51/2001; the p rule decides"
    assert detected({"x": (5.0, edge["p"])}) == set()
    ok.append(f"m = 1 equals the 95% lower-bound rule off the 50-means edge ({agree} random cases, {k50} at the edge)")
    lab = lambda **kw: label({"d": 0, "lo": -1, "hi": 1, "lo90": -1, "hi90": 1, **kw}, False)
    assert lab() == "NEGLIGIBLE" and lab(hi90=2.0) == "UNRESOLVED" and lab(lo90=-2.0) == "UNRESOLVED"
    assert lab(hi=-0.01, hi90=-0.5) == "REVERSED" and lab(hi=0.0) == "NEGLIGIBLE"
    ok.append("labels at their boundaries (REVERSED < 0, NEGLIGIBLE open at ±2.0)")
    rows3 = {**set_rows(per, "ov_dev_b", idx), **{k.replace("qwen25vl_7b", "internvl3_8b"): v for k, v in
                                                 set_rows(per, "ov_dev_b", idx).items()}}
    apply_labels(rows3, "ov_dev_b", {"registered (§7.5)": ["qwen25vl_7b|tau_pair", "internvl3_8b|tau_pair"]})
    assert all(rows3[f"{m}|{e}"]["note"] == SPLIT for m in ("qwen25vl_7b", "internvl3_8b") for e in ("tau_pair", "tau_marg"))
    assert rows3["qwen25vl_7b|tau_pair"]["m"] == 2 and rows3["qwen25vl_7b|tau_sel"]["m"] == 1
    assert rows3["qwen25vl_7b|tau_pair"]["label"] == "DETECTED" and "note" not in rows3["qwen25vl_7b|tau_sel"]
    xr = set_rows(per, "xm_dev500", idx)
    apply_labels(xr, "xm_dev500", {})
    assert "note" not in xr["qwen25vl_7b|tau_pair"], "the X2 words belong to OV-dev-A and OV-dev-B rows"
    ok.append(f"X2 label '{SPLIT}' on OV-dev-A / OV-dev-B τ_pair and τ_marg rows; family sizes")
    ra = set_rows(per, "ov_dev_a", idx)
    assert nominate(ra) == ["H_pair(qwen25vl_7b)"] and family_keys(["H_pair(qwen25vl_7b)"]) == ["qwen25vl_7b|tau_pair"]
    assert ovb_perm_scored([{"dataset": "ov_dev_b", "arm": "perm"}]) and not ovb_perm_scored([{"dataset": "ov_dev_a", "arm": "perm"}])
    import tempfile
    with tempfile.TemporaryDirectory() as tmp:
        led = Path(tmp) / "ledger_ov_dev_b.jsonl"
        led.write_text(json.dumps({"dataset": "ov_dev_b", "arm": "perm", "model": "qwen25vl_7b"}) + "\n")
        try:
            cmd_nominate(argparse.Namespace(ledger=[led], out=Path(tmp) / "n.json"))
            raise AssertionError("nomination must be refused")
        except SystemExit as e:
            assert "REFUSED" in str(e)
        try:
            run = Path(tmp) / "run.json"
            run.write_text(json.dumps({"spec": {"arm": "perm"}}))
            cmd_score(argparse.Namespace(set="ov_dev_b", runs=[run], nomination=None))
            raise AssertionError("OV-dev-B perm scoring before the nomination must be refused")
        except SystemExit as e:
            assert "REFUSED" in str(e)
    ok.append("nomination (95% lower bound >= +2.0), refused once an OV-dev-B perm score exists; OV-dev-B perm needs it")
    pv = draw_variance(per, "qwen25vl_7b", per["qwen25vl_7b|ret"])
    assert abs(pv["sigma2_w"] - np.mean(np.var(np.array(rand), axis=0, ddof=1))) < 1e-9
    nn, rf, vb = 925, 5, 4.0
    g = np.random.default_rng(5)
    y = g.normal(0, 1, (400, 1)) * 0 + g.normal(2, np.sqrt(vb), (1, rf)) + g.normal(0, 10, (400, rf))
    est = [anova_fix(g.normal(0, 3, (nn, 1)) + g.normal(2, np.sqrt(vb), (1, rf)) + g.normal(0, 10, (nn, rf)))["V_b"]
           for _ in range(400)]
    assert abs(np.mean(est) - vb) < 0.5, f"planted V_b recovered ({np.mean(est):.2f} vs {vb})"
    af = anova_fix(y)
    assert abs(af["omega"] - af["V_b"] / af["V_img"]) < 1e-12 and af["V_img"] > 0
    assert abs(anova_fix(g.normal(0, 1, (925, 5)))["F_0.05"] - 0.178) < 0.002, "F quantile of §7.7b (about 0.178)"
    ok.append("ANOVA: planted V_b recovered, omega = V_b / V_img, F quantile 0.178 at n = 925")

    def toy_score(capt: dict, refs: dict) -> np.ndarray:  # unigram recall against the references
        return np.array([np.mean([len(set(capt[i].split()) & set(r.split())) for r in refs[i]]) for i in sorted(capt)])
    cid = ["a", "b"]
    refs = {"a": ["một con mèo nằm trên ghế"], "b": ["hai người đi trên phố"], "c": ["con mèo ngủ say"]}
    shown = {"a": ["con mèo nằm trên ghế sofa"], "b": ["người đi trên phố đông"], "c": ["con mèo đen"]}
    caps = {"zs": {"a": "một con mèo trên ghế", "b": "hai người đi bộ", "c": "mèo ngủ"},
            "ret": {"a": "con mèo nằm trên ghế", "b": "người đi trên phố", "c": "con mèo ngủ"},
            "rand": {"a": "một con mèo", "b": "hai người trên phố", "c": "mèo"}}
    lz = copy_loss(caps["zs"], shown, refs, toy_score, 2)
    assert np.all(kappa(lz, lz) == 0), "κ of a zs run against itself is 0"
    lr = copy_loss(caps["ret"], shown, refs, toy_score, 2)
    assert list(lz) == [4.0, 2.0, 0.0] and list(lr) == [5.0, 4.0, 2.0], "losses with the references unmasked"
    assert list(kappa(lr, lz)) == [1.0, 2.0, 2.0], "κ subtracts the zs placebo"
    s = {k: toy_score(caps[k], refs) for k in ("ret", "rand")}
    cb = copy_bound("ov_dev_b", caps, s, shown, shown, refs, toy_score, real(3))
    assert cb["n3"]["K_ret"]["tier"] == "POST HOC" and copy_bound("xm_dev500", caps, s, shown, shown, refs, toy_score,
                                                                  real(3))["n3"]["K_ret"]["tier"] == "first look"
    assert abs(cb["n2"]["K_ret"]["d"] - 5 / 3) < 1e-12 and abs(cb["n2"]["K_nc"]["d"] - np.mean(kappa(copy_loss(caps["rand"], shown, refs, toy_score, 2), lz))) < 1e-12
    assert isinstance(cb["monotonicity check failed"], bool)
    ok.append("copy bound: κ placebo (zs against itself = 0), references never masked, POST HOC except XM-dev500")
    print("c_attr_score selftest ok: " + "; ".join(ok))


def main() -> None:
    ap = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    ap.add_argument("--selftest", action="store_true")
    sub = ap.add_subparsers(dest="cmd")
    p = sub.add_parser("score")
    p.add_argument("--set", choices=sorted(A.SETS), required=True)
    p.add_argument("--runs", type=Path, nargs="+", required=True)
    p.add_argument("--ledger", type=Path, required=True)
    for k in ("kit_b", "c_lists", "refs", "captions", "c2_dir", "c2_ledger", "nomination"):
        p.add_argument("--" + k.replace("_", "-"), type=Path)
    p.add_argument("--memory", choices=("vi", "coco", "f30k"), default=None)
    p = sub.add_parser("nominate")
    p.add_argument("--ledger", type=Path, nargs="+", required=True)
    p.add_argument("--out", type=Path, required=True)
    p = sub.add_parser("summary")
    p.add_argument("--ledger", type=Path, nargs="+", required=True)
    p.add_argument("--nomination", type=Path)
    p.add_argument("--out", type=Path, required=True)
    p = sub.add_parser("copybound")
    p.add_argument("--set", choices=("ov_dev_b", "xm_dev500"), required=True)
    for k in ("zs", "ret", "rand", "kit_b", "c_lists", "c2_ledger", "c2_run", "out"):
        p.add_argument("--" + k.replace("_", "-"), type=Path, required=True)
    a = ap.parse_args()
    if a.selftest:
        return selftest()
    {"score": lambda: cmd_score(a), "nominate": lambda: cmd_nominate(a), "summary": lambda: cmd_summary(a),
     "copybound": lambda: cmd_copybound(a)}.get(a.cmd, ap.print_help)()


if __name__ == "__main__":
    main()
