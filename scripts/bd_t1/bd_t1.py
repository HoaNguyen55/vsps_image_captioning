#!/usr/bin/env python3
"""Paper B+D, BD-T1 (TIER 1, DEV-EXPLORE ONLY): re-train the B-1 forward recipe (KTVIC first caption) on a training
pool that excludes the future tier-3 set H, decode KTVIC dev300 only, and re-measure the own-minus-other slope gap g
on D0's 187 two-panel dev images. Prereg: manuscript/prereg/2026-10-30_bd_t1/PREREG.md (CC-171).

    python3 scripts/bd_t1/bd_t1.py --selftest                 synthetic data only, CPU
    python3 scripts/bd_t1/bd_t1.py lists                      laptop: bd_t1_lists.json (ids + image sha256 only)
    python  scripts/bd_t1/bd_t1.py ids --dir D                the five level id files from bd_t1_lists.json
    python  scripts/bd_t1/bd_t1.py sft --dir D                each level's sft.jsonl equals its pin
    python  scripts/bd_t1/bd_t1.py guard --head H             M2 only (machine id m4): no H image, no OpenViIC,
                                                              no KTVIC test file, no other lock
    python  scripts/bd_t1/bd_t1.py left --used F --marker M   seconds left under the 15 GPU-h cap, 0 = STOP
    NCS_DATA=... python3 scripts/bd_t1/bd_t1.py score         laptop CPU, once, after the final PREREG is logged

Sets (fixed by `lists`, before any GPU step): H = KTVIC-train ids outside dev300 whose only OpenViIC copies are in
the official OpenViIC dev split (tier 3); T2 = dev300 ids of the same kind (tier 2, never scored here); T1 = D0's 187.
No caption text is printed or written by this file. OpenViIC dev and test annotation files are never opened.
"""
from __future__ import annotations

import argparse
import hashlib
import json
import math
import os
import sys
from pathlib import Path

import numpy as np

ROOT = Path(__file__).resolve().parents[2]
sys.path[:0] = [str(ROOT), str(ROOT / "scripts"), str(ROOT / "scripts/b1_scaling"), str(ROOT / "scripts/b_d0"),
                str(ROOT / "scripts/b_r1")]

import b1  # noqa: E402  B-1's lock, cap arithmetic, kit loader, dev preds (unchanged)
import b_r1 as R1  # noqa: E402  hashes, near-twin rule, guard pieces (unchanged)
import d0  # noqa: E402  panels, k rule, fe slope, CI, in_order (d0.py 0d87a953, unchanged)
import d0_reread as RR  # noqa: E402  D0's scorer (sigma 6 / inf) and fit (unchanged)
import scaling_probe as SP  # noqa: E402
from train_rl import read_ids, schedule  # noqa: E402

PDIR = ROOT / "manuscript/prereg/2026-10-30_bd_t1"
LISTS = PDIR / "bd_t1_lists.json"
SSCD = PDIR / "bd_t1_sscd.json"  # CC-171 W5: scripts/bd_t1/bd_t1_sscd.py output (ids, file names, cosines)
SSCD_SHA256 = "13b9288c7aa3ab9c77f5a66e7ab7879268b75678b8d8f481d63832216c66c885"  # bd_t1_sscd.py, 2026-10-30
LISTS_SHA256 = "b6bbce8f2fa1934c76dcc6005a2d69ff196e8686aa0bd9cc2614d5603b985a17"  # `bd_t1.py lists`, 2026-10-30
PREREG = PDIR / "PREREG.md"
PREREG_SHA256 = "2139561aa41d518b4de3caab79d59b70189db60b84915100a291a3aa63b64e4b"  # CC-171a F1, 2026-10-30; also in LOG.md
SFT_PINS = {  # build_gold_sft.py (B-1 call, default --select first) on the laptop, output outside the repo
    "V1": "fc8d79a7b2ba88046b086dab3486411a6584f78dc18a5aea74ae37c773b11b72",
    "V2": "c83d3243e65408c697ce2cd98ba3ee414a955957fa4b413f496fcaee66cdc9b2",
    "V3": "01875101b6b7e4f441d29785d3b8e86a91fb11571054d4956420b0277e3dbe36",
    "V4": "9276c5a829cb037d9bed9d4995164745d594be3f52866cd7d81abe73da24f399",
    "V5": "9ea2863aa1334782b8ff4eb04b986e297be043c365387a1f8b90a076784cb0d8"}
PAIRS = ROOT / "data/ktvic_openviic_refs.json"
KTVIC_TRAIN = ROOT / "data/datasets/ktvic/train_data.json"
MIRROR = ROOT / ".session_backup/machines/M2/root/outputs/bd_t1"
OUT = ROOT / ".session_backup/2026-10-30/bd_t1/decide.json"
D0_DECIDE = ROOT / ".session_backup/2026-10-29/b_d0/decide.json"
D0_DECIDE_SHA256 = "15dd925f5cba3159fec102bb5238108d9d109860e20bed50c800c6b1875580a1"
P1_SESOI = 4.934144791192721  # D0 §6: max(1, g/2), fixed for the full study; asserted against D0 decide.json

SEEDS = (42, 43, 44)
BASE_N = {"V1": 216, "V2": 433, "V3": 867, "V4": 1734}  # B-1 L1-L4; V5 = every eligible pool id
CAP_S = 15 * 3600
ROLE = "m4"
P_GO = 0.98  # tier-1 PROCEED needs the predicted P(PASS on H) >= this (three-tier rule, PI-1029n)


def sha(p: Path) -> str:
    return hashlib.sha256(p.read_bytes()).hexdigest()


def run_name(s: int, lv: str) -> str:
    return f"t1_s{s}_{lv}"


# ------------------------------------------------------------------------------------------------ sets (laptop)
def splits_of(m: list) -> set[str]:
    return {c[1] for c in m}


def dev_only(pairs: dict, ids) -> list[str]:
    """ids whose matched OpenViIC copies all sit in the official OpenViIC dev split."""
    return sorted((i for i in ids if pairs.get(i) and splits_of(pairs[i]) == {"dev"}), key=int)


def make_sets(pool: list[str], dev: list[str], pairs: dict, H_hash: dict, sscd: dict | None = None) -> dict:
    """H, T2, the near-twin exclusions and the eligible training pool (pure function; selftested).
    sscd (CC-171 W5, bd_t1_sscd.py): pool_vs_held ids leave the pool; held_vs_test ids leave H / T2."""
    sscd = sscd or {"pool_vs_held": {}, "held_vs_test": {}}
    H0 = dev_only(pairs, set(pool))
    out = set(sscd["held_vs_test"])
    H, T2 = [i for i in H0 if i not in out], [i for i in dev_only(pairs, dev) if i not in out]
    held = H0 + dev  # pool images must not be near-twins of any held-out candidate or dev300 image
    rest = [i for i in pool if i not in set(H0)]
    tw = R1.twins(rest, held, H_hash, pairs)
    tw |= {i: ["sscd", *v] for i, v in sscd["pool_vs_held"].items() if i in set(rest) and i not in tw}
    elig = [i for i in schedule(pool, len(pool), SP.SEED) if i in set(rest) - set(tw)]
    return {"H": H, "T2": T2, "twins": tw, "eligible": elig, "held_dropped": sorted(out & set(H0 + dev), key=int)}


def levels_of(elig: list[str]) -> dict[str, int]:
    return BASE_N | {"V5": len(elig)}


def make_lists() -> dict:
    if b1.gpu_host():
        raise SystemExit("lists is built on the laptop only")
    from multiprocessing import Pool

    pairs = json.loads(PAIRS.read_text(encoding="utf-8"))["_pairs"]["train"]
    fn = {str(x["id"]): x["filename"] for x in json.loads(KTVIC_TRAIN.read_text(encoding="utf-8"))["images"]}
    pool, dev = read_ids(ROOT / SP.POOL), read_ids(ROOT / SP.DEV)
    paths = [KTVIC_TRAIN.parent / "images" / fn[i] for i in pool + dev]
    with Pool(8) as p:
        Hh = dict(zip(pool + dev, p.map(R1.img_hashes, paths, chunksize=16)))
    if sha(SSCD) != SSCD_SHA256:
        raise SystemExit("bd_t1_sscd.json differs from its pin")
    S = make_sets(pool, dev, pairs, Hh, json.loads(SSCD.read_text(encoding="utf-8")))
    t1 = {i for i in dev if "train" in splits_of(pairs.get(i, []))}  # D0's 187 rule (d0.panels)
    lv = levels_of(S["eligible"])
    imgsha = {i: sha(KTVIC_TRAIN.parent / "images" / fn[i]) for i in S["H"] + S["T2"]}
    return {"label": "BD-T1 lists (ids and image sha256 only; tier 1 DEV-EXPLORE)",
            "rule": "H = KTVIC-train ids outside dev300 whose matched OpenViIC copies are all in the official "
                    "OpenViIC dev split (_pairs.train); T2 = dev300 ids of the same kind; eligible pool = B-1 pool "
                    f"minus H minus every pool id sharing an OpenViIC file with, within min(pHash, dHash) <= "
                    f"{R1.HASH_MAX} (mirror included) of, or SSCD cosine >= 0.5 to, an H candidate or dev300 image; "
                    "H and T2 minus ids with SSCD cosine >= 0.5 to any KTVIC-test or OpenViIC-test image; levels = prefixes of "
                    f"train_rl.schedule(pool, {SP.POOL_N}, {SP.SEED}) filtered to eligible",
            "pins": {str(PAIRS.relative_to(ROOT)): sha(PAIRS), str(KTVIC_TRAIN.relative_to(ROOT)): sha(KTVIC_TRAIN),
                     SP.POOL: sha(ROOT / SP.POOL), SP.DEV: sha(ROOT / SP.DEV)},
            "n_pool": len(pool), "H": {"n": len(S["H"]), "ids": S["H"], "ids_sha256": b1.sha_bytes(b1.ids_body(S["H"]))},
            "T2": {"n": len(S["T2"]), "ids": S["T2"], "ids_sha256": b1.sha_bytes(b1.ids_body(S["T2"])),
                   "overlap_with_d0_187": len(set(S["T2"]) & t1)},
            "image_sha256_H_T2": imgsha, "pool_twins_excluded": S["twins"], "n_eligible": len(S["eligible"]),
            "held_dropped_sscd_vs_spent_tests": S["held_dropped"], "sscd_sha256": SSCD_SHA256,
            "levels": {k: {"n": n, "file": f"bd_t1_{k}.txt", "ids": S["eligible"][:n],
                           "ids_sha256": b1.sha_bytes(b1.ids_body(S["eligible"][:n]))} for k, n in lv.items()}}


def load_lists() -> dict:
    if not LISTS_SHA256 or sha(LISTS) != LISTS_SHA256:
        raise SystemExit("bd_t1_lists.json is not pinned or differs from its pin (finalise first)")
    return json.loads(LISTS.read_text(encoding="utf-8"))


def write_ids(d: Path) -> None:
    d.mkdir(parents=True, exist_ok=True)
    for x in load_lists()["levels"].values():
        body = b1.ids_body(x["ids"])
        if b1.sha_bytes(body) != x["ids_sha256"]:
            raise SystemExit(f"{x['file']}: ids differ from the pinned list")
        SP.write_once(d / x["file"], body)


def check_sft(d: Path) -> None:
    got = {lv: SP.sha256(d / f"gold_t1_{lv}/sft.jsonl") for lv in load_lists()["levels"]}
    if not SFT_PINS or got != SFT_PINS:
        raise SystemExit(f"sft.jsonl differs from the pins: {got}")
    print("sft pins ok")


# ------------------------------------------------------------------------------------------------ guard (M2)
def held_files(data: Path, held_sha: set[str]) -> list[str]:
    """Any image under data/datasets whose sha256 is an H image's (H must never be on the dev machine)."""
    return [str(p) for p in sorted(data.rglob("*")) if p.is_file() and p.suffix.lower() in b1.IMAGES
            and SP.sha256(p) in held_sha]


def archive_hits(root: Path, names: set[str]) -> list[str]:
    """CC-171a X3: zip/tar archives under root with a member whose base name is an H file name."""
    import tarfile
    import zipfile

    out = []
    for p in sorted(root.rglob("*")):
        if not p.is_file():
            continue
        try:
            if zipfile.is_zipfile(p):
                with zipfile.ZipFile(p) as z:
                    members = z.namelist()
            elif p.suffix == ".7z":  # no stdlib reader: refused as unreadable (X3: *.7z listed)
                out.append(f"{p} (unreadable archive)")
                continue
            elif (".tar" in p.name or p.suffix in (".tgz", ".gz")) and tarfile.is_tarfile(p):
                with tarfile.open(p) as t:
                    members = t.getnames()
            else:
                continue
        except (OSError, zipfile.BadZipFile, tarfile.TarError):
            out.append(f"{p} (unreadable archive)")
            continue
        out += [f"{p}:{m}" for m in members if Path(m).name in names]
    return out


def cmd_rootscan(root: Path) -> None:
    """CC-171 W5 / CC-171a X3: one scan under /root on M2 (job preflight, once): image files by sha256, and archive
    members by H file name (from the staged KTVIC train_data.json)."""
    L = load_lists()
    held = held_files(root, {L["image_sha256_H_T2"][i] for i in L["H"]["ids"]})
    fn = {str(x["id"]): x["filename"] for x in
          json.loads((SP.DATA / "datasets/ktvic/train_data.json").read_text(encoding="utf-8"))["images"]}
    arch = archive_hits(root, {fn[i] for i in L["H"]["ids"]})
    if held or arch:
        raise SystemExit(f"REFUSED: H image(s) under {root}: {held[:3]}, in archives: {arch[:3]}")
    print(f"rootscan ok ({root})")


def cmd_guard(head: str) -> None:
    sys.path.insert(0, str(ROOT / "scripts/grl"))
    import common as K

    if not R1.role_ok(K.host_ok(head)):
        raise SystemExit(f"REFUSED: BD-T1 runs only where /root/.vsps_machine_id is {ROLE} (M2)")
    L = load_lists()
    ds = SP.DATA / "datasets"
    h = {L["image_sha256_H_T2"][i] for i in L["H"]["ids"]}
    held = held_files(ds, h)
    ov = sorted(str(p) for p in ds.rglob("*openviic*"))
    excl = json.loads(K.pinned(b1.EXCL).read_text(encoding="utf-8"))["image_sha256"]["ktvic_test"]
    test = b1.ktvic_test_files(ds, set(excl))
    lock = Path(os.environ.get("T1_LOCK", "/root/outputs/bd_t1/RUNNING"))
    others = [x for x in b1.isolation() if x != f"lock {lock} exists"]
    if held or ov or test or others:
        raise SystemExit(f"REFUSED: H images {held[:3]}, openviic {ov[:3]}, test {test[:3]}, {others}")
    print("guard ok")


# ------------------------------------------------------------------------------------------------ statistics
def norm_cdf(z: float) -> float:
    return 0.5 * (1 + math.erf(z / math.sqrt(2)))


def gap_stats(CK: dict, CO: dict, idx, keep, x, levels) -> tuple[dict, np.ndarray, np.ndarray]:
    """Forward stats on new adapters: own panel K, other panel O; fe slopes over x = log2 N; g draws, g_rel draws."""
    (YK, DK), (YO, DO) = (RR.fit(C, SEEDS, levels, idx, keep, run_name) for C in (CK, CO))
    gd = d0.fe_slope(x, DK) - d0.fe_slope(x, DO)
    rd = 100 * (d0.fe_slope(x, np.log(DK)) - d0.fe_slope(x, np.log(DO)))
    xc = x - x.mean()
    ps = lambda Y: ((Y - Y.mean(1, keepdims=True)) @ xc / (xc @ xc)).tolist()  # noqa: E731
    bK, bO = float(d0.fe_slope(x, YK)), float(d0.fe_slope(x, YO))
    return {"n_images": int(keep.sum()), "b_K": bK, "b_K_ci95": d0.ci(d0.fe_slope(x, DK)), "b_O": bO,
            "b_O_ci95": d0.ci(d0.fe_slope(x, DO)), "g": bK - bO, "g_ci95": d0.ci(gd),
            "g_rel_pct": float(100 * (d0.fe_slope(x, np.log(YK)) - d0.fe_slope(x, np.log(YO)))),
            "g_rel_ci95": d0.ci(rd), "per_seed_b_K": ps(YK), "per_seed_b_O": ps(YO)}, gd, rd


def predict(draws: np.ndarray, bar: float, n_now: int, n_test: int, ci: bool = False) -> float:
    """Predictive P on n_test images, averaged over the tier-1 bootstrap draws d of the true value, test SE =
    SD(draws) * sqrt(n_now / n_test). ci=False: P(point >= bar). ci=True: P(CI_lo > bar) = Phi((d - bar)/SE - 1.96)."""
    se = float(np.std(draws, ddof=1)) * math.sqrt(n_now / n_test)
    if se <= 0:
        return float(np.mean(draws >= bar + (1e-12 if ci else 0)))
    z = 1.959964 if ci else 0.0
    return float(np.mean([norm_cdf((d - bar) / se - z) for d in draws]))


def joint(ps) -> float:
    """Bonferroni lower bound on P(all clauses hold): 1 - sum(1 - p_i), floored at 0 (CC-171 W1)."""
    return max(0.0, 1.0 - sum(1.0 - p for p in ps))


def outcome(m: dict) -> tuple[str, str]:
    """PREREG §6, clauses in written order."""
    if m["g"] < P1_SESOI or m["g_lo"] <= 0:
        return "NOT_REPRODUCED", "gap_below_p1_sesoi_or_ci_includes_0"
    if m["rel_lo"] <= 0 or m["g_lo_inf"] <= 0:
        return "NOT_REPRODUCED", "scale_or_length_penalty_dependent"
    if m["p_pass"] < P_GO:
        return "REPRODUCED_LOW_POWER", "predicted_p_pass_below_0.98_stop_unless_PI_exception"
    return "PROCEED_TO_TIER2", "all_hold"


def cmd_score() -> None:
    if OUT.exists():
        raise SystemExit(f"{OUT} exists; BD-T1 scores once")
    if not PREREG_SHA256 or sha(PREREG) != PREREG_SHA256 or PREREG_SHA256 not in d0.LOG.read_text(encoding="utf-8"):
        raise SystemExit("PREREG.md is not pinned, differs from its pin, or its sha256 is not in LOG.md")
    if sha(D0_DECIDE) != D0_DECIDE_SHA256:
        raise SystemExit("D0 decide.json differs from its pin")
    dec = json.loads(D0_DECIDE.read_text(encoding="utf-8"))
    if dec["fixes_for_full_study"]["P1_SESOI"] != P1_SESOI:
        raise SystemExit("P1_SESOI differs from D0's decided value")
    d0.check_rule()
    L = load_lists()
    levels = {k: v["n"] for k, v in L["levels"].items()}
    x = np.log2(list(levels.values()))
    sums = {ln.split()[1].lstrip("./"): ln.split()[0] for ln in (MIRROR / "SHA256SUMS").read_text().splitlines() if ln}
    new = {}
    for s in SEEDS:
        for lv in levels:
            res = MIRROR / f"{run_name(s, lv)}-dev300-short.json"
            for p in (res, res.with_suffix(".preds.json")):
                if sums.get(p.name) != sha(p):
                    raise SystemExit(f"{p.name}: not the BD-T1 job output")
            new[run_name(s, lv)] = b1.dev_preds(res)
    fwd = d0.load_preds()
    E4, PA, kit_sha = b1.load_kit(d0.KIT_B)
    ids, K, O, _ = d0.panels(SP.dev_refs())  # D0's 187 only: T2 ids are never in this list
    if set(ids) & set(L["T2"]["ids"]):
        raise SystemExit("T2 overlaps the tier-1 images")
    preds = fwd | new
    C6, Cinf = RR.scored(preds, ids, K, O, E4, PA), RR.scored(preds, ids, K, O, E4, PA, float("inf"))
    idx = np.random.default_rng(d0.BOOT_SEED).integers(0, len(ids), (d0.B, len(ids)))
    allk = np.ones(len(ids), bool)
    fw = RR.row(R1.split(C6, fwd)["K"], R1.split(C6, fwd)["O"], idx, allk)  # scorer gate on B-1 adapters
    worst = max(abs(fw[k] - dec["primary"][k]) for k in ("b_K", "b_O", "g"))
    if worst > 1e-6:
        raise SystemExit(f"scorer gate failed: B-1 slopes differ from D0 by {worst:.2e}")
    N6, Ninf = R1.split(C6, new), R1.split(Cinf, new)
    prim, gd, rd = gap_stats(N6["K"], N6["O"], idx, allk, x, levels)
    inf, gdi, _ = gap_stats(Ninf["K"], Ninf["O"], idx, allk, x, levels)
    nH = L["H"]["n"]
    pred = {"g_ge_p1_sesoi": predict(gd, P1_SESOI, len(ids), nH),
            "g_lo_gt_0": predict(gd, 0.0, len(ids), nH, ci=True),
            "g_rel_lo_gt_0": predict(rd, 0.0, len(ids), nH, ci=True),
            "g_inf_lo_gt_0": predict(gdi, 0.0, len(ids), nH, ci=True)}
    p_pass = joint(pred.values())
    v, why = outcome({"g": prim["g"], "g_lo": prim["g_ci95"][0], "rel_lo": prim["g_rel_ci95"][0],
                      "g_lo_inf": inf["g_ci95"][0], "p_pass": p_pass})
    OUT.parent.mkdir(parents=True, exist_ok=True)
    OUT.write_text(json.dumps({
        "label": "BD-T1 TIER 1 DEV-EXPLORE (KTVIC dev300 / OpenViIC-train panel, D0's 187 images; not a test result)",
        "prereg": {"path": os.path.relpath(PREREG, ROOT), "sha256": PREREG_SHA256},
        "outcome": v, "reason": why, "primary": prim, "co_primary_sigma_inf": inf,
        "predicted_p_pass_on_H": {"n_H": nH, "per_clause": pred, "joint_bonferroni_lower": p_pass,
                                  "note": "normal approximation; the panel source changes to OpenViIC dev on H; "
                                          "tier 2 (T2) rehearses that change"},
        "b1_on_same_images": fw, "levels": levels,
        "scorer_gate": {"max_abs_diff_vs_d0": worst, "tolerance": 1e-6},
        "provenance": {"kit_b": kit_sha, "script_sha256": sha(Path(__file__)), "lists_sha256": LISTS_SHA256,
                       "d0_decide_sha256": D0_DECIDE_SHA256, "ncs_data": os.environ.get("NCS_DATA", "")},
    }, indent=1) + "\n", encoding="utf-8")
    print(f"BD-T1 {v} ({why}): g {prim['g']:+.2f} {prim['g_ci95']}, predicted P(PASS on H) {p_pass:.3f}")


# ------------------------------------------------------------------------------------------------ selftest
def selftest() -> None:
    import tempfile

    # sets: H = pool ids with dev-only OV copies; T2 = the dev300 analogue; twins of H/dev leave the pool
    pairs = {"1": [["a", "dev"]], "2": [["b", "train"]], "3": [["c", "dev"], ["d", "train"]], "4": [["e", "test"]],
             "5": [["f", "train"]], "6": [["a", "train"]], "9": [["g", "dev"]], "10": [["h", "train"]]}
    r64 = np.random.default_rng(7).integers(0, 2 ** 63, (8, 4))  # random hashes: pairwise distances >> 10
    Hh = {k: tuple(int(v) for v in r64[n]) for n, k in enumerate(["1", "2", "3", "4", "5", "6", "9", "10"])}
    Hh["5"] = (Hh["10"][0] ^ 1,) + Hh["5"][1:]  # pool id 5 is a 1-bit pHash twin of dev id 10
    S = make_sets(["1", "2", "3", "4", "5", "6"], ["9", "10"], pairs, Hh)
    S2 = make_sets(["1", "2", "3", "4", "5", "6"], ["9", "10"], pairs, Hh,
                   {"pool_vs_held": {"2": ["1", 0.9]}, "held_vs_test": {"9": ["ov_test:x", 0.7]}})
    assert S2["T2"] == [] and S2["H"] == ["1"] and S2["twins"]["2"][0] == "sscd" and "2" not in S2["eligible"], S2
    assert S2["held_dropped"] == ["9"]
    assert S["H"] == ["1"] and S["T2"] == ["9"], S
    assert S["twins"]["6"][0] == "shared_ov_file" and S["twins"]["5"][0].startswith("hash_"), S["twins"]
    assert set(S["eligible"]) == {"2", "3", "4"} and "1" not in S["eligible"], S
    assert dev_only({"7": [["x", "dev"], ["y", "uncaptioned"]]}, ["7"]) == []
    assert levels_of(["a"] * 2700)["V5"] == 2700 and list(levels_of([]))[:4] == list(BASE_N)
    # outcome clauses, in order
    base = {"g": 9.0, "g_lo": 6.0, "rel_lo": 3.0, "g_lo_inf": 5.0, "p_pass": 0.99}
    o = lambda **k: outcome(base | k)  # noqa: E731
    assert o() == ("PROCEED_TO_TIER2", "all_hold")
    assert o(g=4.9)[0] == "NOT_REPRODUCED" and o(g_lo=0.0)[0] == "NOT_REPRODUCED"
    assert o(rel_lo=-1)[1] == "scale_or_length_penalty_dependent" and o(g_lo_inf=0.0)[0] == "NOT_REPRODUCED"
    assert o(p_pass=0.97)[0] == "REPRODUCED_LOW_POWER" and "PI_exception" in o(p_pass=0.97)[1]
    # prediction: large margin -> near 1; at the bar -> about 0.5; more test images -> higher
    rng = np.random.default_rng(3)
    d = rng.normal(10, 1.7, 2000)
    assert predict(d, P1_SESOI, 187, 700) > 0.99 and abs(predict(d, 10.0, 187, 700) - 0.5) < 0.05
    assert predict(d - 4, P1_SESOI, 187, 2000) > predict(d - 4, P1_SESOI, 187, 200)
    # W1: joint is a Bonferroni lower bound; the CI clause is harder than the point clause
    assert abs(joint([0.99, 0.99, 0.995]) - 0.975) < 1e-12 and joint([0.5, 0.4]) == 0.0
    assert predict(d, 0.0, 187, 700, ci=True) <= predict(d, 0.0, 187, 700)
    assert predict(np.full(50, 1.0) + rng.normal(0, 1e-9, 50), 0.0, 187, 187, ci=True) > 0.99
    assert abs(norm_cdf(1.959964) - 0.975) < 1e-6
    # gap_stats recovers synthetic truth (K slope 10, O slope 1 -> g 9) with seed offsets
    n = 187
    idx = np.random.default_rng(0).integers(0, n, (300, n))
    keep = np.ones(n, bool)
    lv = levels_of(["a"] * 2743)
    x = np.log2(list(lv.values()))
    noise = rng.normal(0, 3, n)
    CK = {run_name(s, k): 100 + 10 * xx + noise + s % 5 for s in SEEDS for k, xx in zip(lv, x)}
    CO = {run_name(s, k): 50 + 1 * xx + noise for s in SEEDS for k, xx in zip(lv, x)}
    r, gd, _ = gap_stats(CK, CO, idx, keep, x, lv)
    assert abs(r["g"] - 9) < 1e-9 and abs(r["b_K"] - 10) < 1e-9 and np.allclose(gd, 9)
    assert all(abs(v - 10) < 1e-9 for v in r["per_seed_b_K"])
    # held-file scan finds an image by sha whatever its name
    with tempfile.TemporaryDirectory() as t:
        p = Path(t) / "ktvic/images/renamed.jpg"
        p.parent.mkdir(parents=True)
        p.write_bytes(b"\xff\xd8x")
        (Path(t) / "ktvic/images/other.jpg").write_bytes(b"\xff\xd8y")
        assert held_files(Path(t), {SP.sha256(p)}) == [str(p)]
        assert held_files(Path(t), set()) == []
        import zipfile as _z
        with _z.ZipFile(Path(t) / "k.zip", "w") as z:
            z.writestr("ktvic/images/h1.jpg", b"x")
        assert archive_hits(Path(t), {"h1.jpg"}) == [f"{Path(t) / 'k.zip'}:ktvic/images/h1.jpg"]
        assert archive_hits(Path(t), {"zz.jpg"}) == []
        import tarfile as _t
        with _t.open(Path(t) / "k.tar.xz", "w:xz") as z:
            z.add(Path(t) / "k.zip", arcname="o/h2.jpg")
        assert archive_hits(Path(t), {"h2.jpg"}) == [f"{Path(t) / 'k.tar.xz'}:o/h2.jpg"]
        (Path(t) / "k.7z").write_bytes(b"7z")
        assert archive_hits(Path(t), {"zz.jpg"}) == [f"{Path(t) / 'k.7z'} (unreadable archive)"]
        used, mark = Path(t) / "u.tsv", Path(t) / "CAP_STOP.json"
        used.write_text("a start 0\na 50000\n")
        assert b1.left(used, mark, CAP_S) == CAP_S - 50000
    # design budget from B-1's measured M4 seconds (mean of seeds); V5 scaled linearly from L5 = 3,469
    train_s = {216: 403, 433: 770, 867: 1520, 1734: 2990}
    t5 = 5937 * 2743 / 3469
    est = len(SEEDS) * (sum(train_s.values()) + t5 + 5 * 330) + 322
    assert est < CAP_S / 1.4, est
    # role and the job's registered fragments
    assert R1.role_ok("m4") and not R1.role_ok("m3")
    text = (ROOT / "scripts/bd_t1/bd_t1_job.sh").read_text(encoding="utf-8")
    assert all(f in text for f in b1.JOB_FLAGS) and not any(f in text for f in SP.JOB_FORBIDDEN)
    assert "CC-152a" in text and "set -euo pipefail" in text and "= m4 ]" in text and "$T1 guard --head" in text
    print(f"bd_t1 selftest ok (design estimate {est / 3600:.2f} GPU-h, cap {CAP_S / 3600:.0f})")


def main() -> None:
    ap = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    ap.add_argument("--selftest", action="store_true")
    sub = ap.add_subparsers(dest="cmd")
    sub.add_parser("lists")
    sub.add_parser("score")
    for name in ("ids", "sft"):
        sub.add_parser(name).add_argument("--dir", type=Path, required=True)
    sub.add_parser("guard").add_argument("--head", required=True)
    sub.add_parser("rootscan").add_argument("--root", type=Path, default=Path("/root"))
    p = sub.add_parser("left")
    p.add_argument("--used", type=Path, required=True)
    p.add_argument("--marker", type=Path, required=True)
    a = ap.parse_args()
    if a.selftest:
        return selftest()
    handlers = {
        "lists": lambda: (SP.write_once(LISTS, (json.dumps(make_lists(), indent=1) + "\n").encode()),
                          print(f"{sha(LISTS)}  {LISTS.name}")),
        "ids": lambda: write_ids(a.dir),
        "sft": lambda: check_sft(a.dir),
        "guard": lambda: cmd_guard(a.head),
        "rootscan": lambda: cmd_rootscan(a.root),
        "left": lambda: print(b1.left(a.used, a.marker, CAP_S)),
        "score": cmd_score,
    }
    if a.cmd not in handlers:
        ap.error("a subcommand or --selftest is required")
    handlers[a.cmd]()


if __name__ == "__main__":
    main()
