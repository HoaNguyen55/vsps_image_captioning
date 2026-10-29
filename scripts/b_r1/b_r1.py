#!/usr/bin/env python3
"""Paper B, B-R1 (DEV ONLY): the reverse direction of D0. The B-1 recipe, unchanged except its caption source, is
trained on OpenViIC-train captions of KTVIC-train images and scored on the 187 D0 dev300 images against both panels.
Rule: manuscript/prereg/2026-10-29_b_r1/RULE.md (CC-161).

    python3 scripts/b_r1/b_r1.py --selftest                      synthetic data only
    python3 scripts/b_r1/b_r1.py lists                           laptop: r1_lists.json (ids only), once
    python3 scripts/b_r1/b_r1.py ann --out F                     laptop: KTVIC-format JSON, one OV-train caption per
                                                                 eligible image (written OUTSIDE the repo)
    python  scripts/b_r1/b_r1.py ids --dir D                     the three ids files from r1_lists.json
    python  scripts/b_r1/b_r1.py sft --dir D                     each level's sft.jsonl equals its pin
    python  scripts/b_r1/b_r1.py guard --head H                  M2 only (machine id m4): host, GPU, HEAD, data
    python  scripts/b_r1/b_r1.py left --used F --marker M        seconds left under the 8 GPU-h cap, 0 = STOP
    NCS_DATA=... python3 scripts/b_r1/b_r1.py score              laptop CPU, once, after RULE.md is logged

No caption text is printed or written by this file, except by `ann`, whose output must stay outside the repo.
"""
from __future__ import annotations

import argparse
import hashlib
import json
import os
import subprocess
import sys
from pathlib import Path

import numpy as np

ROOT = Path(__file__).resolve().parents[2]
sys.path[:0] = [str(ROOT), str(ROOT / "scripts"), str(ROOT / "scripts/b1_scaling"), str(ROOT / "scripts/b_d0")]

import b1  # noqa: E402  B-1's lock, cap arithmetic, guards (unchanged)
import d0  # noqa: E402  D0's panels, k rule, slope, CI, scorer order (d0.py 0d87a953, unchanged)
import d0_reread as RR  # noqa: E402  the W6 re-read's scorer, fit and verdict-free rows
import scaling_probe as SP  # noqa: E402
from train_rl import read_ids, schedule  # noqa: E402

PDIR = ROOT / "manuscript/prereg/2026-10-29_b_r1"
LISTS = PDIR / "r1_lists.json"
LISTS_SHA256 = "571dfedf16bd39dfa4e94f6f0873c89241d7ffb61ef9a86c38ffa4a4e4db289c"
RULE, RULE_SHA256 = PDIR / "RULE.md", "e7c50fbcd1235bc8109ed7628d804cf1fa031f8fd203e9629f75a3a3898e1d26"
REREAD = ROOT / ".session_backup/2026-10-29/b_d0_reread/reread.json"
REREAD_SHA256 = "7853ab4adfef786861b4017ed5b347749d1826bd85dd63d5e3727249295990e2"  # CC-161 W6, LOG
PAIRS = ROOT / "data/ktvic_openviic_refs.json"
OV_TRAIN = ROOT / "data/datasets/openviic/uit-openviic-annotation-train.json"
KTVIC_TRAIN = ROOT / "data/datasets/ktvic/train_data.json"
MIRROR = ROOT / ".session_backup/machines/M2/root/outputs/b_r1"
OUT = ROOT / ".session_backup/2026-10-29/b_r1/decide.json"
D0_DECIDE = ROOT / ".session_backup/2026-10-29/b_d0/decide.json"
D0_DECIDE_SHA256 = "15dd925f5cba3159fec102bb5238108d9d109860e20bed50c800c6b1875580a1"
P1_SESOI = 4.934144791192721  # D0 decide.json fixes_for_full_study.P1_SESOI = max(1, g / 2); asserted in score

SEEDS = (42, 43)
LEVELS = {"R1": 216, "R2": 867, "R3": 1734}  # the x values of B-1 L1, L3, L4
FWD = {"R1": "L1", "R2": "L3", "R3": "L4"}  # same-N B-1 points for the crossover row
X = np.log2(list(LEVELS.values()))
HASH_MAX = 10  # match_openviic.py's hash bound, without its SSCD clause (stricter exclusion)
CAP_S = 8 * 3600
ROLE = "m4"  # M2 is set up with machine id m4 (CC-155 W1): dev-only
SFT_PINS = {"R1": "1e4ad95684790fd3a8809c42d730034b474d72a99ac7b4d8672fc3d238ebd740",
            "R2": "846ecc7e97a26da4cb54bf9e8f9731969fb0c90a3a0e87e934b57db42aa66c5d",
            "R3": "7229e9c14295e6445a838c0955d75f2ebc06ccb1c3052053ea1c527b71a4344d"}  # laptop build (RULE.md §2)
ANN_SHA256 = "dfaa19c7d1729e3829031c554c00f3df0e174cc05c4875b3eb5285b3d9e96135"  # ann JSON, laptop build


def sha(p: Path) -> str:
    return hashlib.sha256(p.read_bytes()).hexdigest()


def run_name(s: int, lv: str) -> str:
    return f"r1_s{s}_{lv}"


# ------------------------------------------------------------------------------------------------ lists (laptop)
def ham(a: int, b: int) -> int:
    return bin(a ^ b).count("1")


def img_hashes(path: Path) -> tuple[int, int, int, int]:
    """pHash, dHash of the image and of its mirror (match_openviic.py: a mirrored copy is a copy)."""
    import imagehash
    from PIL import Image, ImageOps

    im = Image.open(path).convert("RGB")
    return tuple(int(str(f(x)), 16) for x in (im, ImageOps.mirror(im)) for f in (imagehash.phash, imagehash.dhash))


def near(h: tuple, g: tuple) -> int:
    """min over pHash/dHash of the direct and mirrored hash of h against g's direct hash."""
    return min(ham(h[0], g[0]), ham(h[1], g[1]), ham(h[2], g[0]), ham(h[3], g[1]))


def twins(train: list[str], dev: list[str], H: dict, pairs: dict) -> dict[str, list]:
    """train id -> [reason, dev id]: same OpenViIC file as a dev300 image (any OV split), or hash distance <= HASH_MAX."""
    dev_ov = {c[0]: j for j in dev for c in pairs.get(j, [])}
    out = {}
    for i in train:
        hit = next((dev_ov[c[0]] for c in pairs.get(i, []) if c[0] in dev_ov), None)
        if hit is not None:
            out[i] = ["shared_ov_file", hit]
            continue
        d, j = min((near(H[i], H[j]), j) for j in dev)
        if d <= HASH_MAX:
            out[i] = [f"hash_{d}", j]
    return out


def make_lists() -> dict:
    if b1.gpu_host():
        raise SystemExit("lists is built on the laptop only")
    from multiprocessing import Pool

    pairs = json.loads(PAIRS.read_text(encoding="utf-8"))["_pairs"]["train"]
    fn = {str(x["id"]): x["filename"] for x in json.loads(KTVIC_TRAIN.read_text(encoding="utf-8"))["images"]}
    pool, dev = read_ids(ROOT / SP.POOL), read_ids(ROOT / SP.DEV)
    with Pool(8) as p:
        H = dict(zip(pool + dev, p.map(img_hashes, [KTVIC_TRAIN.parent / "images" / fn[i] for i in pool + dev],
                                        chunksize=16)))
    tw = twins(pool, dev, H, pairs)
    cand = [i for i in pool if any(c[1] == "train" for c in pairs.get(i, []))]
    elig = [i for i in schedule(pool, len(pool), SP.SEED) if i in set(cand) - set(tw)]
    levels = {lv: {"n": n, "file": f"r1_{lv}.txt", "ids": elig[:n], "ids_sha256": b1.sha_bytes(b1.ids_body(elig[:n]))}
              for lv, n in LEVELS.items()}
    return {"label": "B-R1 lists (ids only; DEV ONLY)",
            "rule": f"eligible = ids of {SP.POOL} with an OpenViIC-train copy in _pairs.train, minus every train id "
                    f"that shares an OpenViIC file with a dev300 image or is within hash distance {HASH_MAX} of one "
                    f"(min pHash/dHash, mirror included); levels = prefixes of train_rl.schedule(pool, "
                    f"{SP.POOL_N}, {SP.SEED}) filtered to eligible",
            "pins": {str(PAIRS.relative_to(ROOT)): sha(PAIRS), str(KTVIC_TRAIN.relative_to(ROOT)): sha(KTVIC_TRAIN),
                     SP.POOL: sha(ROOT / SP.POOL), SP.DEV: sha(ROOT / SP.DEV)},
            "n_pool": len(pool), "n_with_ov_train_copy": len(cand), "n_eligible": len(elig),
            "train_twins_of_dev300": tw, "excluded_from_candidates": sorted(set(cand) & set(tw), key=int),
            "dev_ids_with_a_train_twin": sorted({j for _, j in tw.values()}, key=int),
            "b1_levels_holding_each_twin": {i: [lv for lv, x in b1.check()["levels"].items() if i in x["ids"]]
                                            for i in tw},
            "levels": levels}


def load_lists() -> dict:
    if sha(LISTS) != LISTS_SHA256:
        raise SystemExit("r1_lists.json differs from its pin")
    return json.loads(LISTS.read_text(encoding="utf-8"))


def ov_caption(i: str, pairs: dict, ov: dict) -> str:
    """D0 §3's O pool (train copies in _pairs order, captions pooled, stripped, repeats dropped), first element."""
    return d0.dedup(c for f, s, *_ in pairs[i] if s == "train" for c in ov[f]["captions"])[0]


def make_ann(out: Path) -> None:
    if b1.gpu_host():
        raise SystemExit("ann is built on the laptop only")
    if ROOT in out.resolve().parents:
        raise SystemExit("ann output holds caption text: write it outside the repo")
    L = load_lists()
    pairs = json.loads(PAIRS.read_text(encoding="utf-8"))["_pairs"]["train"]
    ov = json.loads(OV_TRAIN.read_text(encoding="utf-8"))
    fn = {str(x["id"]): x["filename"] for x in json.loads(KTVIC_TRAIN.read_text(encoding="utf-8"))["images"]}
    ids = sorted(L["levels"]["R3"]["ids"], key=int)  # R1 < R2 < R3 (nested)
    body = {"images": [{"id": int(i), "filename": fn[i]} for i in ids],
            "annotations": [{"id": n, "image_id": int(i), "caption": ov_caption(i, pairs, ov)}
                            for n, i in enumerate(ids)]}
    SP.write_once(out, (json.dumps(body, ensure_ascii=False) + "\n").encode())
    print(f"{sha(out)}  {len(ids)} images")


def write_ids(d: Path) -> None:
    d.mkdir(parents=True, exist_ok=True)
    for x in load_lists()["levels"].values():
        body = b1.ids_body(x["ids"])
        if b1.sha_bytes(body) != x["ids_sha256"]:
            raise SystemExit(f"{x['file']}: ids differ from the pinned list")
        SP.write_once(d / x["file"], body)


def check_sft(d: Path) -> None:
    got = {lv: SP.sha256(d / f"gold_r1_{lv}/sft.jsonl") for lv in LEVELS}
    if got != SFT_PINS:
        raise SystemExit(f"sft.jsonl differs from the pins: {got}")
    print("sft pins ok")


# ------------------------------------------------------------------------------------------------ guard (M2)
def role_ok(mid: str) -> bool:
    return mid == ROLE


def cmd_guard(head: str) -> None:
    """grl common.host_ok (idle GPU, HEAD, clean tree), then machine id exactly m4; no OpenViIC file staged (the
    captions come only through the pinned ann JSON); no KTVIC test file; no C-EN trace; no other experiment lock."""
    sys.path.insert(0, str(ROOT / "scripts/grl"))
    import common as K

    if not role_ok(K.host_ok(head)):
        raise SystemExit(f"REFUSED: B-R1 runs only where /root/.vsps_machine_id is {ROLE} (M2)")
    ds = SP.DATA / "datasets"
    ov = sorted(str(p) for p in ds.rglob("*openviic*"))
    staged = [s for s in K.CEN_TEST_SIDE if (ds / f"cen_{s}").exists()]
    busy = subprocess.run(["pgrep", "-f", "scripts/c_en/"], capture_output=True, text=True).stdout.split()
    excl = json.loads(K.pinned(b1.EXCL).read_text(encoding="utf-8"))["image_sha256"]["ktvic_test"]
    test = b1.ktvic_test_files(ds, set(excl))
    lock = Path(os.environ.get("R1_LOCK", "/root/outputs/b_r1/RUNNING"))
    others = [x for x in b1.isolation() if x != f"lock {lock} exists"]
    if ov or staged or busy or test or others:
        raise SystemExit(f"REFUSED: openviic {ov[:3]}, C-EN {staged} {busy}, test {test[:3]}, {others}")
    print("guard ok")


# ------------------------------------------------------------------------------------------------ score (laptop)
def outcome(m: dict) -> tuple[str, str]:
    """RULE.md §5, clauses in written order. m: style_ok, own_lo, other_lo, g, gap_lo, gap_hi, rel_lo (sigma 6),
    gap_lo_inf, fwd_lo_inf (sigma = inf). Only GO_BOTH passes; ASYMMETRIC is an equivalence reading against D0's
    P1 SESOI; a GO_BOTH that fails a D0 clause falls through; one that needs the length penalty is inconclusive."""
    if not m["style_ok"]:
        return "STYLE_NOT_LEARNED", "reverse_hyps_not_longer_than_forward_at_matched_N"
    if m["own_lo"] <= 0:
        if m["other_lo"] > 0:
            return "REVERSE_FLAT_OTHER_UP", "ov_panel_insensitivity_supported"
        return "REVERSE_FLAT_BOTH", "ov_signal_weak_panel_question_open"
    if m["gap_lo"] > 0 and m["g"] >= d0.SESOI and m["rel_lo"] > 0:
        if m["gap_lo_inf"] > 0 and m["fwd_lo_inf"] > 0:
            return "GO_BOTH", "panel_specific_both_directions"
        return "GAP_INCONCLUSIVE", "length_penalty_dependent"
    if m["gap_hi"] < P1_SESOI:
        return "ASYMMETRIC", "ov_training_transfers_to_ktvic" if m["other_lo"] > 0 else "gap_below_p1_sesoi"
    return "GAP_INCONCLUSIVE", "gap_ci_spans_0_and_p1_sesoi"


def reverse(CO: dict, CK: dict, idx, keep) -> tuple[dict, np.ndarray]:
    """Own panel = O for the OV-trained adapters; other = K. Stats (no verdict field) and the g_R draws."""
    (YO, DO), (YK, DK) = (RR.fit(C, SEEDS, LEVELS, idx, keep, run_name) for C in (CO, CK))
    bO, bK = float(d0.fe_slope(X, YO)), float(d0.fe_slope(X, YK))
    gd = d0.fe_slope(X, DO) - d0.fe_slope(X, DK)
    rd = 100 * (d0.fe_slope(X, np.log(DO)) - d0.fe_slope(X, np.log(DK)))
    return {"n_images": int(keep.sum()), "b_O_own": bO, "b_O_ci95": d0.ci(d0.fe_slope(X, DO)), "b_K_other": bK,
            "b_K_ci95": d0.ci(d0.fe_slope(X, DK)), "g_R": bO - bK, "g_R_ci95": d0.ci(gd),
            "g_rel_R_pct": float(100 * (d0.fe_slope(X, np.log(YO)) - d0.fe_slope(X, np.log(YK)))),
            "g_rel_R_ci95": d0.ci(rd), "mean_O_by_level": YO.mean(0).tolist(),
            "mean_K_by_level": YK.mean(0).tolist()}, gd


def style_check(syl: dict) -> dict:
    """W3 manipulation check: mean hypothesis syllables of the reverse adapters exceed those of the forward B-1
    adapters at matched N (seeds 42/43, L1/L3/L4), pooled over the six cells."""
    r = np.mean([syl[run_name(s, lv)] for s in SEEDS for lv in LEVELS])
    f = np.mean([syl[d0.run_name(s, FWD[lv])] for s in SEEDS for lv in LEVELS])
    return {"reverse": float(r), "forward_matched": float(f), "style_ok": bool(r > f)}


def crossover(CF: dict, CR: dict, idx, keep) -> dict:
    """Same-N 2x2: [O(R) - O(F)] + [K(F) - K(R)] over seeds 42/43 and N = 216/867/1734 (image sets differ)."""
    M = keep[idx]
    cells = [(s, lv) for s in SEEDS for lv in LEVELS]
    v = sum((CR["O"][run_name(s, lv)] - CF["O"][d0.run_name(s, FWD[lv])]
             + CF["K"][d0.run_name(s, FWD[lv])] - CR["K"][run_name(s, lv)]) for s, lv in cells) / len(cells)
    return {"d": float(v[keep].mean()), "ci95": d0.ci((v[idx] * M).sum(1) / M.sum(1))}


def split(C: dict, names) -> dict:
    return {n: {r: v for r, v in C[n].items() if r in names} for n in C}


def cmd_score() -> None:
    if OUT.exists():
        raise SystemExit(f"{OUT} exists; B-R1 scores once")
    if sha(RULE) != RULE_SHA256 or RULE_SHA256 not in d0.LOG.read_text(encoding="utf-8"):
        raise SystemExit("RULE.md differs from its pin or its sha256 is not in LOG.md")
    if sha(D0_DECIDE) != D0_DECIDE_SHA256 or sha(REREAD) != REREAD_SHA256:
        raise SystemExit("D0 decide.json or the W6 re-read differs from its pin")
    reread = json.loads(REREAD.read_text(encoding="utf-8"))
    if reread["b_r1"] != "PROCEED":
        raise SystemExit("the W6 re-read HELD B-R1")
    d0.check_rule()  # D0's input pins (pairs, OV train, KTVIC train, dev300, B-1 mirror)
    import score_coco_probe as sc
    from object_prf import image_counts, scores
    from rescap.chair import objects_in
    from rl_reward import syllables

    sums = {ln.split()[1].lstrip("./"): ln.split()[0] for ln in (MIRROR / "SHA256SUMS").read_text().splitlines() if ln}
    rev = {}
    for s in SEEDS:
        for lv in LEVELS:
            res = MIRROR / f"{run_name(s, lv)}-dev300-short.json"
            for p in (res, res.with_suffix(".preds.json")):
                if sums.get(p.name) != sha(p):
                    raise SystemExit(f"{p.name}: not the B-R1 job output")
            rev[run_name(s, lv)] = b1.dev_preds(res)
    fwd = d0.load_preds()
    E4, PA, kit_sha = b1.load_kit(d0.KIT_B)
    ids, K, O, _ = d0.panels(SP.dev_refs())
    preds = fwd | rev
    C6, Cinf = RR.scored(preds, ids, K, O, E4, PA), RR.scored(preds, ids, K, O, E4, PA, float("inf"))
    CF, CR, NF, NR = split(C6, fwd), split(C6, rev), split(Cinf, fwd), split(Cinf, rev)
    idx = np.random.default_rng(d0.BOOT_SEED).integers(0, len(ids), (d0.B, len(ids)))
    allk = np.ones(len(ids), bool)

    # scorer gate: the forward point estimates must equal D0's decided b_K, b_O (permutation-invariant points)
    fw = RR.row(CF["K"], CF["O"], idx, allk)
    dec = json.loads(D0_DECIDE.read_text(encoding="utf-8"))
    if dec["fixes_for_full_study"]["P1_SESOI"] != P1_SESOI:
        raise SystemExit("P1_SESOI differs from D0's decided value")
    worst = max(abs(fw[k] - dec["primary"][k]) for k in ("b_K", "b_O", "g"))
    if worst > 1e-6:
        raise SystemExit(f"scorer gate failed: forward slopes differ from D0 by {worst:.2e}")
    tw = set(load_lists()["dev_ids_with_a_train_twin"])
    clean = np.array([i not in tw for i in ids])
    fw_twins = RR.row(CF["K"], CF["O"], idx, clean)
    if abs(fw_twins["g"] - reread["rows"]["a_dev_twins"]["g"]) > 1e-6:  # W7 consistency with the W6 re-read
        raise SystemExit("minus-twins forward g differs from the W6 re-read mask (a)")

    primary, gR = reverse(CR["O"], CR["K"], idx, allk)
    no_lp, fw_inf = reverse(NR["O"], NR["K"], idx, allk)[0], RR.row(NF["K"], NF["O"], idx, allk)
    (_, DK), (_, DO) = d0.grid(CF["K"], idx, allk), d0.grid(CF["O"], idx, allk)
    gF = d0.fe_slope(d0.X, DK) - d0.fe_slope(d0.X, DO)
    syl = {r: float(np.mean([len(syllables(p[i])) for i in ids])) for r, p in preds.items()}
    style = style_check(syl)
    v, why = outcome({"style_ok": style["style_ok"], "own_lo": primary["b_O_ci95"][0],
                      "other_lo": primary["b_K_ci95"][0], "g": primary["g_R"], "gap_lo": primary["g_R_ci95"][0],
                      "gap_hi": primary["g_R_ci95"][1], "rel_lo": primary["g_rel_R_ci95"][0],
                      "gap_lo_inf": no_lp["g_R_ci95"][0], "fwd_lo_inf": fw_inf["g_ci95"][0]})
    terms = sc.load_vi_terms()
    match = {"b1_exact": lambda t: set(objects_in(t)), "v2": lambda t: set(sc.vi_objects(t, terms, "v2"))}
    objects = {}
    for mname, fn in match.items():
        gold = {"K": {i: set().union(*(fn(c) for c in K[i])) for i in ids},
                "O": {i: set().union(*(fn(c) for c in O[i])) for i in ids}}
        gold["union"] = {i: gold["K"][i] | gold["O"][i] for i in ids}
        objects[mname] = {}
        for gk, g in gold.items():
            rows = {r: [image_counts(fn(p[i]), g[i], lambda o: {o}) for i in ids] for r, p in rev.items()}
            Y = np.array([[scores(rows[run_name(s, lv)])["F1"] for lv in LEVELS] for s in SEEDS])
            Dr = np.array([[[scores([rows[run_name(s, lv)][j] for j in r])["F1"] for r in idx] for lv in LEVELS]
                           for s in SEEDS])
            objects[mname][gk] = {"F1": Y.tolist(), "b": float(d0.fe_slope(X, Y)), "ci95": d0.ci(d0.fe_slope(X, Dr))}
    p2 = objects["b1_exact"]["O"]["ci95"][0] > 0  # RULE.md §6: the matcher must see the own-panel gain
    OUT.parent.mkdir(parents=True, exist_ok=True)
    OUT.write_text(json.dumps({
        "label": "B-R1 DEV (KTVIC dev300 / OpenViIC-train panel, 187 images; development data, not a test result)",
        "rule": {"path": os.path.relpath(RULE, ROOT), "sha256": RULE_SHA256},
        "outcome": v, "reason": why, "primary": primary, "style_check": style,
        "co_primary_sigma_inf": {"reverse": no_lp, "forward": fw_inf},
        "forward_recomputed": fw, "forward_note": "CIs recomputed with in_order; they differ numerically from D0's "
                                                  "decided CIs; only the points are gated (1e-6)",
        "both_directions_sum_g_plus_gR": fw["g"] + primary["g_R"],
        "descriptive": {"minus_dev_twins_reverse": reverse(CR["O"], CR["K"], idx, clean)[0],
                        "minus_dev_twins_forward": fw_twins,
                        "asymmetry_g_minus_gR": {"d": fw["g"] - primary["g_R"], "ci95": d0.ci(gF - gR)},
                        "crossover_same_N": crossover(CF, CR, idx, allk),
                        "mean_hyp_syllables": syl,
                        "length_slope_syllables_per_doubling": {
                            "forward": float(d0.fe_slope(d0.X, np.array([[syl[d0.run_name(s, lv)] for lv in d0.LEVELS]
                                                                         for s in d0.SEEDS]))),
                            "reverse": float(d0.fe_slope(X, np.array([[syl[run_name(s, lv)] for lv in LEVELS]
                                                                      for s in SEEDS])))}},
        "objects": objects, "p2_matcher_sensitive": p2,
        "scorer_gate": {"max_abs_diff_vs_d0": worst, "tolerance": 1e-6},
        "provenance": {"kit_b": kit_sha, "jar_sha256": sha(E4.VNC / "VnCoreNLP-1.2.jar"),
                       "ncs_data": os.environ.get("NCS_DATA", ""), "script_sha256": sha(Path(__file__)),
                       "lists_sha256": sha(LISTS), "d0_decide_sha256": D0_DECIDE_SHA256,
                       "reread_sha256": REREAD_SHA256},
    }, indent=1) + "\n", encoding="utf-8")
    print(f"B-R1 {v} ({why}): b_O own {primary['b_O_own']:+.2f} {primary['b_O_ci95']}, "
          f"g_R {primary['g_R']:+.2f} {primary['g_R_ci95']}")


# ------------------------------------------------------------------------------------------------ selftest
def selftest() -> None:
    import tempfile

    # twin rule: shared OV file wins, then hash distance with mirror, bound inclusive
    H = {"t1": (0, 0, 0, 0), "t2": (0b111, 0, 0, 0), "t3": ((1 << 11) - 1, (1 << 11) - 1, 0b11, 0b11),
         "t4": ((1 << 11) - 1, (1 << 11) - 1, (1 << 11) - 1, (1 << 11) - 1), "d1": (0, 0, 0, 0)}
    pairs = {"t1": [["ov9", "train"]], "d1": [["ov9", "dev"]]}
    tw = twins(["t1", "t2", "t3", "t4"], ["d1"], H, pairs)
    assert tw == {"t1": ["shared_ov_file", "d1"], "t2": ["hash_0", "d1"], "t3": ["hash_2", "d1"]}, tw
    assert near((1023, 0, 0, 0), (0, 0, 0, 0)) == 0 and ham(1023, 0) == 10
    # outcome classes in written order (CC-161 W3/W4)
    base = {"style_ok": True, "own_lo": 1, "other_lo": 2, "g": 6, "gap_lo": 0.5, "gap_hi": 9, "rel_lo": 1,
            "gap_lo_inf": 0.5, "fwd_lo_inf": 1}
    o = lambda **k: outcome(base | k)  # noqa: E731
    assert o() == ("GO_BOTH", "panel_specific_both_directions")
    assert o(style_ok=False)[0] == "STYLE_NOT_LEARNED"
    assert o(own_lo=-0.1) == ("REVERSE_FLAT_OTHER_UP", "ov_panel_insensitivity_supported")
    assert o(own_lo=-0.1, other_lo=-1) == ("REVERSE_FLAT_BOTH", "ov_signal_weak_panel_question_open")
    assert o(gap_lo_inf=-0.1) == ("GAP_INCONCLUSIVE", "length_penalty_dependent")
    assert o(fwd_lo_inf=0.0) == ("GAP_INCONCLUSIVE", "length_penalty_dependent")
    # a D0 clause failing falls through to the next clause, never to GO_BOTH
    assert o(g=0.9, gap_lo=0.2, gap_hi=1.6) == ("ASYMMETRIC", "ov_training_transfers_to_ktvic")
    assert o(rel_lo=-0.1) == ("GAP_INCONCLUSIVE", "gap_ci_spans_0_and_p1_sesoi")
    assert o(gap_lo=-0.5, gap_hi=2) == ("ASYMMETRIC", "ov_training_transfers_to_ktvic")
    assert o(gap_lo=-0.5, gap_hi=2, other_lo=-1) == ("ASYMMETRIC", "gap_below_p1_sesoi")
    assert o(gap_lo=-0.5, gap_hi=P1_SESOI) == ("GAP_INCONCLUSIVE", "gap_ci_spans_0_and_p1_sesoi")  # strict bound
    syl = {**{run_name(s, lv): 15.0 for s in SEEDS for lv in LEVELS},
           **{d0.run_name(s, FWD[lv]): 11.0 for s in SEEDS for lv in LEVELS}}
    assert style_check(syl)["style_ok"] and not style_check({k: 11.0 for k in syl})["style_ok"]
    # reverse slopes recover synthetic truth; the crossover is zero when both models are equal
    n, rng = 187, np.random.default_rng(1)
    idx = np.random.default_rng(0).integers(0, n, (300, n))
    keep = np.ones(n, bool)
    noise = rng.normal(0, 3, n)
    CO = {run_name(s, lv): 50 + 6 * x + noise + s % 3 for s in SEEDS for lv, x in zip(LEVELS, X)}
    CK = {run_name(s, lv): 70 + 1 * x + noise for s in SEEDS for lv, x in zip(LEVELS, X)}
    r = reverse(CO, CK, idx, keep)[0]
    assert abs(r["b_O_own"] - 6) < 1e-9 and abs(r["g_R"] - 5) < 1e-9 and "outcome" not in r
    assert abs(reverse(CK, CK, idx, keep)[0]["g_R"]) < 1e-12
    same = {d0.run_name(s, FWD[lv]): CO[run_name(s, lv)] for s in SEEDS for lv in LEVELS}
    cf = {"O": same, "K": same}
    cr = {"O": CO, "K": CO}
    assert abs(crossover(cf, cr, idx, keep)["d"]) < 1e-12
    m = keep.copy(); m[:5] = False
    assert reverse(CO, CK, idx, m)[0]["n_images"] == n - 5
    # guard role, cap, design budget
    assert role_ok("m4") and not role_ok("m3") and not role_ok("")
    with tempfile.TemporaryDirectory() as t:
        used, mark = Path(t) / "u.tsv", Path(t) / "CAP_STOP.json"
        used.write_text("a start 0\na 28000\n")
        assert b1.left(used, mark, CAP_S) == CAP_S - 28000
        used.write_text("a start 0\na 28750\n")
        assert b1.left(used, mark, CAP_S) == 0  # fewer than MIN_STEP_S left
    train_s = {216: 397, 867: 1509, 1734: 2982}  # measured on M4 (B-1 gpu_seconds.tsv, mean of seeds)
    est = len(SEEDS) * (sum(train_s[n] for n in LEVELS.values()) + 315 * len(LEVELS)) + 322
    assert est < CAP_S / 2, est
    # the job file carries B-1's registered fragments and no forbidden flag
    text = (ROOT / "scripts/b_r1/b_r1_job.sh").read_text(encoding="utf-8")
    assert all(f in text for f in b1.JOB_FLAGS) and not any(f in text for f in SP.JOB_FORBIDDEN)
    assert "CC-152a" in text and "set -euo pipefail" in text and f"{ROLE}" in text and f"ANN_SHA={ANN_SHA256}" in text
    print(f"b_r1 selftest ok (design estimate {est / 3600:.2f} GPU-h, cap {CAP_S / 3600:.0f})")


def main() -> None:
    ap = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    ap.add_argument("--selftest", action="store_true")
    sub = ap.add_subparsers(dest="cmd")
    sub.add_parser("lists")
    sub.add_parser("score")
    for name in ("ann", "ids", "sft"):
        sub.add_parser(name).add_argument("--out" if name == "ann" else "--dir", type=Path, required=True)
    sub.add_parser("guard").add_argument("--head", required=True)
    p = sub.add_parser("left")
    p.add_argument("--used", type=Path, required=True)
    p.add_argument("--marker", type=Path, required=True)
    a = ap.parse_args()
    if a.selftest:
        return selftest()
    handlers = {
        "lists": lambda: (SP.write_once(LISTS, (json.dumps(make_lists(), indent=1) + "\n").encode()),
                          print(f"{sha(LISTS)}  {LISTS.name}")),
        "ann": lambda: make_ann(a.out),
        "ids": lambda: write_ids(a.dir),
        "sft": lambda: check_sft(a.dir),
        "guard": lambda: cmd_guard(a.head),
        "left": lambda: print(b1.left(a.used, a.marker, CAP_S)),
        "score": cmd_score,
    }
    if a.cmd not in handlers:
        ap.error("a subcommand or --selftest is required")
    handlers[a.cmd]()


if __name__ == "__main__":
    main()
