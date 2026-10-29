#!/usr/bin/env python3
"""Paper A, A-T1 (TIER 1, DEV-EXPLORE ONLY): the gold-completeness step on a gold whose completeness is MEASURED
before any decode. ADE20K SceneParsing (exhaustive pixel labels, 150 classes) + Localized Narratives (one spoken
description per image, CC BY 4.0). Tier 1 decodes D1 = 1,000 ADE20K *training* images on M2 (dev-only) with the
A-N2 LVLM set; tier 2 = D2 (1,000 other training images); tier 3 = the full ADE20K validation split (2,000).
Prereg: manuscript/prereg/2026-10-30_a_t1/PREREG.md (CC-170).

    python3 scripts/a_t1/a_t1.py --selftest                          CPU, synthetic data only
    python  scripts/a_t1/a_t1.py split --zip Z --train T --val-hash F   M1 only (role m3), CPU: training-only archive
                                                                     + validation pHash/dHash numbers (CC-170 W3)
    python3 scripts/a_t1/a_t1.py select --train T --val-hash F --ln-train L   laptop: a_t1_lists.json (ids only)
    python3 scripts/a_t1/a_t1.py gold --train T --ln-train L --set D1 --out O   laptop: class-name sets + premise
    python3 scripts/a_t1/a_t1.py stage --train T --gold O --set S --root R   laptop: one set's images + manifest
                                                                     for M2 (D1 in tier 1, D2 in tier 2); refuses
                                                                     unless that set's premise holds (CC-170 W4)
    python  scripts/a_t1/a_t1.py register --root R --out REG         A-N2 blocks unchanged, D1 only (smoke listed, not staged)
    python  scripts/a_t1/a_t1.py guard --head H                      M2 only (machine id m4); no ADE val file
    python  scripts/a_t1/a_t1.py left --ledger L                     seconds left under the 10 GPU-h cap
    python3 scripts/a_t1/a_t1.py score --raw DIR --gold G --out O    laptop CPU, once, after the PREREG is logged

No narrative or caption text is printed or written by this file: gold files hold class names and counts only.
The full ADE20K archive (it holds the validation images and labels) is opened only on M1 by `split`; the laptop
and M2 see the training-only archive and the validation hash numbers. Validation labels and narratives are never
opened in tiers 1-2.
"""
from __future__ import annotations

import argparse
import hashlib
import io
import json
import math
import os
import sys
import zipfile
from pathlib import Path

import numpy as np

HERE = Path(__file__).resolve().parent
ROOT = HERE.parents[1]
sys.path[:0] = [str(HERE.parent / "pascal50s")]
import p50  # noqa: E402  ids, timed ledger, register pattern, BOOT constants (also puts g2b and lb on sys.path)
import p50x  # noqa: E402  salience() = the X4/X5 size-matched random-deletion null, unchanged

PDIR = ROOT / "manuscript/prereg/2026-10-30_a_t1"
LISTS = PDIR / "a_t1_lists.json"
PREREG = PDIR / "PREREG.md"
PREREG_SHA256 = "d7bc92f634eaec8e78bbd5e80843feca468e01418f48ab9e2084b2dc287de297"  # finalisation; `score` refuses while empty
PIN = {"zip": "7ff1be44964418441f542a7cc1e1a650e7dc0fc275f5d23252bc9bbdbc977b29",
       "train": "2f2042c48136f180dc50320cbe0e99cec2cfc2505ad605140fcf087ab6c81e52",
       "objectinfo": "c368be0cf078eb49264b5a0d0c4ad2e63bbfedf260c48458984302e2a7995671",
       "ln_train": "78a0a8784e26591399493996ecd6863e4497dca36c5c5501b6747fff1343841e"}  # G2 gate: full zip (M1), training-only archive
# (written by `split`, sha in M1 EVENTS), objectInfo150.txt, ade20k_train_captions.jsonl
PREREG_ID = "2026-10-30_a_t1_ade_dev"
N_D, N_SMOKE, SHARE_MIN, SHARES = 1000, 20, 0.001, (0.0, 0.001, 0.005)  # SHARE_MIN = primary label-presence rule
CAP_S, ROLE, HASH_MAX, P_GO, N_TEST = 10 * 3600, "m4", 10, 0.98, 2000
KEEP = ["qwen3vl_8b", "qwen25vl_7b", "qwen25vl_3b", "smolvlm2_2b", "llava15_7b", "internvl3_8b", "llava_ov_7b"]
# ADE20K-150 class index (1-based, objectInfo150 order) -> (ADE name, COCO-80 name). Rule (CC-170 W2, fixed before any
# data): a class is kept iff the frozen English matcher maps its ADE name to exactly {that COCO class}; the selftest
# re-checks the rule. `gold` asserts each ADE name is among the index's objectInfo150 synonyms (comma-separated).
# Dropped by the rule: 31 armchair (no match), 117 minibike (-> bicycle), 142 crt screen (no match).
ADE2COCO = {8: ("bed", "bed"), 13: ("person", "person"), 16: ("table", "dining table"),
            34: ("desk", "dining table"), 65: ("coffee table", "dining table"), 20: ("chair", "chair"),
            76: ("swivel chair", "chair"), 24: ("sofa", "couch"), 21: ("car", "car"),
            48: ("sink", "sink"), 51: ("refrigerator", "refrigerator"), 66: ("toilet", "toilet"),
            68: ("book", "book"), 70: ("bench", "bench"), 77: ("boat", "boat"), 104: ("ship", "boat"),
            81: ("bus", "bus"), 84: ("truck", "truck"), 90: ("television receiver", "tv"),
            144: ("monitor", "tv"), 91: ("airplane", "airplane"),
            99: ("bottle", "bottle"), 72: ("stove", "oven"), 119: ("oven", "oven"),
            125: ("microwave", "microwave"), 128: ("bicycle", "bicycle"), 136: ("vase", "vase"), 137: ("traffic light", "traffic light"), 149: ("clock", "clock"),
            120: ("ball", "sports ball")}
V = frozenset(c for _, c in ADE2COCO.values())


def sha_bytes(b: bytes) -> str:
    return hashlib.sha256(b).hexdigest()


def run_id(m: str, q: str) -> str:
    return f"at1_{m}-{q}"


# ------------------------------------------------------------------------------------------------ sets (laptop)
def order(ids) -> list[str]:
    """Registered order: ascending sha256 of the image id string."""
    return sorted(ids, key=lambda i: sha_bytes(i.encode()))


def split_sets(cand: list[str], near_val: set[str]) -> dict[str, list[str]]:
    o = [i for i in order(cand) if i not in near_val]
    return {"D1": o[:N_D], "D2": o[N_D:2 * N_D], "smoke": o[2 * N_D:2 * N_D + N_SMOKE]}


def zip_members(z: zipfile.ZipFile, part: str) -> dict[str, str]:
    """image id -> member, for images/<part>/ADE_<part>_*.jpg (part = training | validation)."""
    out = {}
    for n in z.namelist():
        if f"/images/{part}/" in n and n.endswith(".jpg"):
            out[Path(n).stem] = n
    return out


def ln_ids(path: Path) -> dict[str, int]:
    """image id -> number of narratives (Localized Narratives jsonl; the text is not kept)."""
    out: dict[str, int] = {}
    for line in Path(path).read_text(encoding="utf-8").splitlines():
        if line.strip():
            i = json.loads(line)["image_id"]
            out[i] = out.get(i, 0) + 1
    return out


def check_pin(p: Path, key: str) -> None:
    if not PIN[key] or p50.sha_file(p) != PIN[key]:
        raise SystemExit(f"{p}: sha256 not pinned or different (G2 gate: record it in PIN first)")


def tmp_hashes(b: bytes) -> tuple[int, int, int, int]:
    sys.path.insert(0, str(ROOT / "scripts/b_r1"))
    from b_r1 import img_hashes

    tmp = Path(os.environ.get("TMPDIR", "/tmp")) / "a_t1_img.jpg"
    tmp.write_bytes(b)
    return img_hashes(tmp)


def cmd_split(zp: Path, train: Path, val_hash: Path, mid_file: Path = Path("/root/.vsps_machine_id")) -> None:
    """M1 (role m3) only: the training-only archive (training images, training PNGs, objectInfo150.txt) and the
    pHash/dHash numbers of the validation images. Nothing else of validation leaves M1 (CC-170 W3)."""
    mid = mid_file.read_text().strip() if mid_file.is_file() else ""
    if mid != "m3":
        raise SystemExit("REFUSED: split runs on the m3-role machine (M1) only")
    check_pin(zp, "zip")
    with zipfile.ZipFile(zp) as z, zipfile.ZipFile(train, "x", zipfile.ZIP_STORED) as t:
        va = zip_members(z, "validation")
        for n in z.namelist():
            if "/training/" in n or n.endswith("objectInfo150.txt"):
                t.writestr(n, z.read(n))
        vh = {i: list(tmp_hashes(z.read(m))) for i, m in sorted(va.items())}
    p50.dump({"label": "ADE20K validation pHash/dHash (numbers only)", "n": len(vh), "hashes": vh}, val_hash)
    print(f"train archive {p50.sha_file(train)}  val hashes {p50.sha_file(val_hash)} ({len(vh)})")


def near_val(cand_h: dict, val_h: dict) -> set[str]:
    """candidates within min(pHash, dHash) <= HASH_MAX of any validation image (candidate mirror included)."""
    V_ = np.array(list(val_h.values()), np.uint64)
    out = set()
    for i, h in cand_h.items():
        d = min(int(np.bitwise_count(np.uint64(h[a]) ^ V_[:, b]).min()) for a, b in ((0, 0), (1, 1), (2, 0), (3, 1)))
        if d <= HASH_MAX:
            out.add(i)
    return out


def cmd_select(train: Path, val_hash: Path, ln: Path) -> dict:
    check_pin(train, "train"), check_pin(ln, "ln_train")
    vh = json.loads(val_hash.read_text(encoding="utf-8"))["hashes"]
    with zipfile.ZipFile(train) as z:
        tr = zip_members(z, "training")
        if zip_members(z, "validation") or any("/annotations/validation/" in n for n in z.namelist()):
            raise SystemExit("the training archive holds validation members")
        has_png = {Path(n).stem for n in z.namelist() if "/annotations/training/" in n and n.endswith(".png")}
        cand = sorted(set(tr) & set(ln_ids(ln)) & has_png)
        if len(cand) < 18000:
            raise SystemExit(f"only {len(cand)} candidates (< 18,000 of 20,210): wrong archive or narratives file")
        ch = {i: tmp_hashes(z.read(tr[i])) for i in cand}
    nv = near_val(ch, vh)
    S = split_sets(cand, nv)
    if len(S["D1"]) != N_D or len(S["D2"]) != N_D or len(S["smoke"]) != N_SMOKE:
        raise SystemExit(f"set sizes {[len(v) for v in S.values()]} (CC-170 W6)")
    near_val_ids = nv
    return {"label": "A-T1 lists (ADE20K training ids only; tier 1 D1, tier 2 D2, smoke)", "prereg_id": PREREG_ID,
            "rule": "candidates = ADE20K training images with an annotation PNG and >= 1 Localized Narrative; minus "
                    f"those within min(pHash, dHash) <= {HASH_MAX} (mirror included) of any ADE20K validation image; "
                    "ordered by sha256(image id); D1 = first 1,000, D2 = next 1,000, smoke = next 20",
            "pins": PIN, "n_candidates": len(cand), "n_near_val_excluded": len(near_val_ids),
            "sets": {k: {"n": len(v), "ids": v, "ids_sha256": sha_bytes(("\n".join(v) + "\n").encode())}
                     for k, v in S.items()}}


def load_set(name: str) -> list[str]:
    return json.loads(LISTS.read_text(encoding="utf-8"))["sets"][name]["ids"]


# ------------------------------------------------------------------------------------------------ gold (laptop)
def label_set(png: np.ndarray, share: float, mp: dict | None = None) -> set[str]:
    """COCO names of the mapped ADE classes covering more than `share` of the pixels (0 = any pixel).
    mp: ADE index -> COCO name (default: the frozen ADE2COCO; `gold` passes the W2' resolved map)."""
    mp = mp if mp is not None else {k: c for k, (_, c) in ADE2COCO.items()}
    vals, cnt = np.unique(png, return_counts=True)
    tot = png.size
    return {mp[int(v)] for v, c in zip(vals, cnt) if int(v) in mp and c / tot > share}


def parse_info(text: str) -> dict[int, list[str]]:
    """objectInfo150.txt: header, then tab-separated Idx, Ratio, Train, Val, Name; Name = comma-separated synonyms."""
    out = {}
    for r in text.splitlines()[1:]:
        if r.strip():
            f = r.split("\t")
            out[int(f[0])] = [x.strip() for x in f[-1].replace(";", ",").split(",") if x.strip()]
    return out


def info_names(z: zipfile.ZipFile) -> dict[int, list[str]]:
    """The pinned objectInfo150.txt of the archive, parsed and name-checked (W1); hard fail if absent."""
    info = [n for n in z.namelist() if n.endswith("objectInfo150.txt")]
    if len(info) != 1:
        raise SystemExit("objectInfo150.txt missing (or twice) in the training archive")
    b = z.read(info[0])
    if not PIN["objectinfo"] or sha_bytes(b) != PIN["objectinfo"]:
        raise SystemExit("objectInfo150.txt sha256 not pinned or different")
    names = parse_info(b.decode("utf-8"))
    check_names(names)
    return names


def check_names(names: dict[int, list[str]]) -> None:
    bad = {k: (v, names.get(k)) for k, (v, _) in ADE2COCO.items() if v not in names.get(k, [])}
    if bad:
        raise SystemExit(f"ADE2COCO index/name mismatch against objectInfo150: {bad}")


def reverse_conflicts(names: dict[int, list[str]], mp: dict[int, str], Vs: frozenset, en) -> dict:
    """CC-170a W2': unmapped ADE classes any of whose names/synonyms the matcher sends into V."""
    out = {}
    for k, syn in sorted(names.items()):
        if k in mp:
            continue
        hit = set().union(*(en(x) & Vs for x in syn)) if syn else set()
        if hit:
            out[k] = sorted(hit)
    return out


def resolve_map(names: dict[int, list[str]], en) -> tuple[dict[int, str], frozenset, list]:
    """W2' resolution rule (fixed 2026-10-30, applied to the pinned objectInfo150.txt only, before any narrative is
    read), repeated to a fixed point: an unmapped class in conflict is ADDED to the map when its first-listed name
    gives exactly one V class; otherwise every V class it hits LEAVES V (with its map entries)."""
    mp, Vs, log = {k: c for k, (_, c) in ADE2COCO.items()}, V, []
    while True:
        conf = reverse_conflicts(names, mp, Vs, en)
        if not conf:
            return mp, Vs, log
        for k, hit in conf.items():
            first = en(names[k][0]) & Vs
            if len(first) == 1:
                mp[k] = next(iter(first))
                log.append(["added", k, names[k][0], mp[k]])
            else:
                Vs = Vs - set(hit)
                mp = {a: c for a, c in mp.items() if c in Vs}
                log.append(["V_removed", k, names[k][0], hit])


def premise(lab: list[set], nar: list[set]) -> dict:
    """Output-free completeness of the label rung against the narrative rung (on the mapped vocabulary V)."""
    sL, sN, sNL = sum(map(len, lab)), sum(map(len, nar)), sum(len(n & l) for n, l in zip(nar, lab))
    return {"sum_label": sL, "sum_narr": sN, "sum_narr_in_label": sNL, "sum_narr_not_in_label": sN - sNL,
            "ratio_label_over_narr": sL / sN if sN else None, "evaluable_2x": sL >= 2 * sNL}


def cmd_gold(zp: Path, ln: Path, name: str) -> dict:
    import score_g2b as g
    from PIL import Image

    check_pin(zp, "train"), check_pin(ln, "ln_train")
    ids = load_set(name)
    en = g.MATCH["coco80"]["en"]
    with zipfile.ZipFile(zp) as z:  # W1 + W2' gates on class metadata only, before any narrative is read
        names = info_names(z)
        mp, Vs, maplog = resolve_map(names, en)
        if reverse_conflicts(names, mp, Vs, en):
            raise SystemExit("W2' gate: an unmapped class still sends a name into V")
    nar: dict[str, set] = {i: set() for i in ids}
    for line in ln.read_text(encoding="utf-8").splitlines():
        if line.strip():
            r = json.loads(line)
            if r["image_id"] in nar:
                nar[r["image_id"]] |= en(r["caption"]) & Vs
    with zipfile.ZipFile(zp) as z:
        pngs = {Path(n).stem: n for n in z.namelist() if "/annotations/training/" in n and n.endswith(".png")}
        arrs = {i: np.array(Image.open(io.BytesIO(z.read(pngs[i])))) for i in ids}
    lab = {str(s): {i: sorted(label_set(arrs[i], s, mp)) for i in ids} for s in SHARES}
    nr = {i: sorted(nar[i]) for i in ids}
    return {"label": f"A-T1 gold for {name} (class names only, vocabulary V of {len(Vs)} COCO-80 names)",
            "set": name, "V": sorted(Vs), "map_resolved": {str(k): c for k, c in sorted(mp.items())},
            "map_resolution_log": maplog, "share_min_primary": SHARE_MIN, "labels_by_share": lab, "narrative": nr,
            "premise_by_share": {s: premise([set(v[i]) for i in ids], [nar[i] for i in ids]) for s, v in lab.items()},
            "provenance": {"pins": PIN, "script_sha256": p50.sha_file(Path(__file__))}}


def cmd_stage(zp: Path, gold: Path, root: Path, name: str = "D1") -> dict:
    """D1 images + manifest for M2, only after the output-free premise holds on D1 (CC-170 W4)."""
    check_pin(zp, "train")
    G = json.loads(gold.read_text(encoding="utf-8"))
    pr = G["premise_by_share"][str(SHARE_MIN)]
    if G["set"] != name or not pr["evaluable_2x"] or (pr["ratio_label_over_narr"] or 0) < 2:
        raise SystemExit(f"PREMISE_NOT_MET on {G['set']}: {pr} (no GPU step; report it)")
    rows = ""
    with zipfile.ZipFile(zp) as z:
        tr = zip_members(z, "training")
        (root / "images").mkdir(parents=True, exist_ok=True)
        for i in load_set(name):
            b = z.read(tr[i])
            (root / "images" / f"{i}.jpg").write_bytes(b)
            rows += f"{i}\t{i}.jpg\t{sha_bytes(b)}\n"
    (root / "sets").mkdir(parents=True, exist_ok=True)
    (root / f"sets/a_t1_{name}.tsv").write_text(rows, encoding="utf-8")
    return {name: sha_bytes(rows.encode()), "premise": pr}


def register(root: Path, name: str = "D1") -> dict:
    """p50.register's pattern: A-N2 schema/models/model_list/decode/decoder/venv unchanged; the D1 set only."""
    a = (ROOT / p50.A_N2[0]).read_bytes()
    if sha_bytes(a) != p50.A_N2[1]:
        raise SystemExit("REFUSED: the A-N2 registration differs from its pin")
    A = json.loads(a)
    reg = {k: A[k] for k in ("schema", "models", "model_list", "decode", "decoder", "venv")}
    reg.update({"prereg_id": PREREG_ID, "statement": "runtime registration built by scripts/a_t1/a_t1.py register",
                "datasets": {}, "runs": []})
    for s, pre in ((name, "at1"),):
        man = root / f"sets/a_t1_{s}.tsv"
        n = len(man.read_text(encoding="utf-8").splitlines())
        reg["datasets"][f"a_t1_{s}"] = {"manifest": {"path": str(man), "sha256": p50.sha_file(man)}, "n_images": n,
                                        "image_dir": f"{root.name}/images"}
        reg["runs"] += [{"run_id": f"{pre}_{m}-{q}", "model": m, "dataset": f"a_t1_{s}", "prompt_mode": q}
                        for m in KEEP for q in p50.MODES]
    return reg


# ------------------------------------------------------------------------------------------------ guard (M2)
def val_files(data: Path) -> list[str]:
    """ADE validation images/labels/narratives, any ADEChallengeData path, any archive (CC-170 W9)."""
    return [str(p) for p in data.rglob("*") if p.is_file() and ("ADE_val_" in p.name or "validation" in p.name
                                                               or "ADEChallengeData" in str(p) or p.suffix == ".zip")]


def guard(head: str, mid_file: Path = Path("/root/.vsps_machine_id")) -> None:
    mid = mid_file.read_text().strip().lower() if mid_file.is_file() else ""
    if mid != ROLE:
        raise SystemExit(f"REFUSED: {mid_file} is {mid or 'missing'!r}; A-T1 is dev-only and runs on M2 (m4)")
    sys.path.insert(0, str(ROOT / "scripts/grl"))
    from common import host_ok

    if host_ok(head, mid_file) != ROLE:
        raise SystemExit("REFUSED: host_ok did not return m4")
    data = Path(os.environ.get("NCS_DATA", "/root/ncs-data")) / "datasets"
    bad = val_files(data) if data.exists() else []
    if bad or any((data / d).exists() for d in ("pascal50s", "xm3600", "nocaps")):
        raise SystemExit(f"REFUSED: ADE validation or another test-side set is staged: {bad[:3]}")
    print("guard ok")


def left(ledger: Path) -> int:
    used = sum(b for _, b, _ in p50.ledger_rows(ledger))
    return max(0, int(CAP_S - used))


# ------------------------------------------------------------------------------------------------ score (laptop)
def norm_cdf(z: float) -> float:
    return 0.5 * (1 + math.erf(z / math.sqrt(2)))


def predict(draws: np.ndarray, n_now: int, n_test: int = N_TEST) -> float:
    """Predictive P(CI_lo > 0 on n_test images): mean over the tier-1 draws d of Phi(d / se - 1.96)."""
    se = float(np.std(draws, ddof=1)) * math.sqrt(n_now / n_test)
    return float(np.mean([norm_cdf(d / se - 1.96) for d in draws])) if se > 0 else float(np.mean(draws > 0))


def predict_null(res: dict, n_now: int, n_test: int = N_TEST) -> float:
    """Salience: z of the observed slope below the null, scaled by sqrt(n_test / n_now); P(z_test > 1.96)."""
    sd = (res["null_hi"] - res["null_lo"]) / (2 * 1.96)
    if sd <= 0:
        return 0.0
    z = (res["null_mean"] - res["observed"]) / sd * math.sqrt(n_test / n_now)
    return norm_cdf(z - 1.96)


def analysis(g, ids: list[str], lab: dict, nar: dict, caps: dict, models: list[str], n_boot=p50.N_BOOT,
             n_rep=p50x.R_NULL, Vs: frozenset = V) -> dict:
    """AD-1: slope[label | V] - slope[narrative | V] > 0 (sign_gt_0, P50-A4 part-2 form). AD-2: narrative-gold slope
    below the size-matched random-deletion null drawn from the label gold (p50x.salience, the X5 form)."""
    en = g.MATCH["coco80"]["en"]
    runs = [run_id(m, q) for m in models for q in p50.MODES]
    ment = {r: [en(caps[r].get(i, "")) & Vs for i in ids] for r in runs}
    L, N = [set(lab[i]) for i in ids], [set(nar[i]) for i in ids]
    clean = [n for n, i in enumerate(ids) if all(isinstance(caps[r].get(i), str) and caps[r][i].strip()
                                                 and g.is_clean(caps[r][i], "en") for r in runs)]
    if len(clean) < 2:
        return {"verdict": "NOT_EVALUABLE", "reason": "empty analysis set"}
    idx = np.array(clean)
    Wb = np.random.default_rng(p50.BOOT_SEED).multinomial(len(idx), [1 / len(idx)] * len(idx), size=n_boot).astype(float)
    one = np.ones((1, len(idx)))
    sl = {}
    for name, gold in (("label", L), ("narrative", N)):
        pt = [g.scores(g.rows(ment[r], [gold]), idx, one) for r in runs]
        bs = [g.scores(g.rows(ment[r], [gold]), idx, Wb) for r in runs]
        sl[name] = (float(g.stat_slope(pt, None)[0]), g.stat_slope(bs, None))
    M = [float(g.scores(g.rows(ment[r], [L]), idx, one)["M"][0]) for r in runs]
    ev = all(m > 0 for m in M) and len({round(m, 12) for m in M}) >= 2
    d_pt, d_bs = sl["label"][0] - sl["narrative"][0], sl["label"][1] - sl["narrative"][1]
    iv = g.ci(d_bs, *p50.CI)
    ad1 = {"point": d_pt, "ci95": iv, "slope_label": sl["label"][0], "slope_narrative": sl["narrative"][0],
           "verdict": g.verdict("sign_gt_0", d_pt, iv) if ev else "NOT_EVALUABLE", "_draws": d_bs,
           "p_one_sided": float((1 + (d_bs <= 0).sum()) / (len(d_bs) + 1))}
    pr = premise([L[n] for n in clean], [N[n] for n in clean])
    ad2 = p50x.salience(g, [ment[r] for r in runs], [N], L, idx, np.random.default_rng(p50x.NULL_SEED), n_rep, ev)
    if not pr["evaluable_2x"]:
        ad2["verdict"], ad2["reason"] = "NOT_EVALUABLE", "sum |label| < 2 * sum |narrative & label|"
    return {"runs": runs, "n_images": len(idx), "M": M, "AD1": ad1, "AD2": ad2, "premise": pr}


def outcome(a: dict, p1: float, p2: float) -> tuple[str, str]:
    """PREREG §6, clauses in written order."""
    if not a["premise"]["evaluable_2x"] or (a["premise"]["ratio_label_over_narr"] or 0) < 2:
        return "PREMISE_NOT_MET", "label_rung_not_2x_the_narrative_rung"
    if a["AD1"]["verdict"] != "PASS" or a["AD2"]["verdict"] != "PASS":
        return "NOT_REPRODUCED", f"AD1 {a['AD1']['verdict']}, AD2 {a['AD2']['verdict']}"
    if min(p1, p2) < P_GO:
        return "PASS_LOW_POWER", "predicted_p_pass_below_0.98"
    return "PROCEED_TO_TIER2", "all_hold"


def cmd_score(raw: Path, gold_path: Path, out: Path) -> None:
    import score_g2b as g

    if out.exists():
        raise SystemExit(f"{out} exists; A-T1 scores once")
    if not PREREG_SHA256 or p50.sha_file(PREREG) != PREREG_SHA256:
        raise SystemExit("PREREG.md is not pinned or differs from its pin")
    gold = json.loads(gold_path.read_text(encoding="utf-8"))
    ids = load_set("D1")
    lab, nar = gold["labels_by_share"][str(SHARE_MIN)], gold["narrative"]
    models = [m for m in KEEP if all((raw / f"{run_id(m, q)}.preds.json").exists() for q in p50.MODES)]
    if len(models) < p50.MIN_MODELS:
        raise SystemExit(f"NOT_EVALUABLE: {len(models)} models decoded both prompts (< {p50.MIN_MODELS})")
    caps = {}
    for m in models:
        for q in p50.MODES:
            f = raw / f"{run_id(m, q)}.preds.json"
            side = f.with_suffix(".json.sha256")
            if not side.exists() or side.read_text().split()[0] != p50.sha_file(f):
                raise SystemExit(f"{f.name}: sidecar sha256 missing or different")
            caps[run_id(m, q)] = {str(k): v for k, v in g.read_captions(f).items()}
    a = analysis(g, ids, lab, nar, caps, models, Vs=frozenset(gold["V"]))
    p1 = predict(a["AD1"].pop("_draws"), a["n_images"])
    p2 = predict_null(a["AD2"], a["n_images"])
    v, why = outcome(a, p1, p2)
    desc = {s: premise([set(x[i]) for i in ids], [set(nar[i]) for i in ids]) for s, x in gold["labels_by_share"].items()}
    out.parent.mkdir(parents=True, exist_ok=True)
    out.write_text(json.dumps({"label": "A-T1 TIER 1 DEV-EXPLORE (ADE20K training images; not a test result)",
                               "prereg": {"path": os.path.relpath(PREREG, ROOT), "sha256": PREREG_SHA256},
                               "outcome": v, "reason": why, "models": models, "analysis": a,
                               "predicted_p_pass_on_val2000": {"AD1": p1, "AD2": p2},
                               "premise_by_share_descriptive": desc,
                               "provenance": {"script_sha256": p50.sha_file(Path(__file__)),
                                              "gold_sha256": p50.sha_file(gold_path)}}, indent=1, default=float) + "\n",
                   encoding="utf-8")
    print(f"A-T1 {v} ({why}): AD1 {a['AD1']['point']:+.2f} {a['AD1']['ci95']}, AD2 p {a['AD2']['p_one_sided']:.3f}, "
          f"P(PASS) {min(p1, p2):.3f}")


# ------------------------------------------------------------------------------------------------ selftest
def selftest() -> None:
    import tempfile

    import score_g2b as g

    # vocabulary and map
    en = g.MATCH["coco80"]["en"]
    assert len(ADE2COCO) == 30 and len(V) == 24 and "motorcycle" not in V and "potted plant" not in V, sorted(V)
    assert all(en(n) == {c} for n, c in ADE2COCO.values()), "W2 rule: matcher(ADE name) == {COCO class}"
    # objectInfo150 format (tab-separated, comma synonyms) and the name check
    info = "Idx\tRatio\tTrain\tVal\tName\n" + "".join(
        f"{k}\t0.001\t10\t1\t{'television receiver, television, television set, tv' if k == 90 else n + ', x'}\n"
        for k, (n, _) in ADE2COCO.items())
    check_names(parse_info(info))
    try:
        check_names(parse_info(info.replace("television receiver, ", "")))
        raise AssertionError("missing synonym accepted")
    except SystemExit:
        pass
    # W2': an unmapped class whose name the matcher sends into V is a conflict; resolution adds it or shrinks V
    names = parse_info(info + "111\t0.001\t1\t1\tstool\n200\t0.001\t1\t1\tzzz; trolley\n")
    assert reverse_conflicts(names, {k: c for k, (_, c) in ADE2COCO.items()}, V, en) == {111: ["chair"], 200: ["bus"]}
    mp, Vs, lg = resolve_map(names, en)
    assert mp[111] == "chair" and "bus" not in Vs and all(c != "bus" for c in mp.values()), lg
    assert not reverse_conflicts(names, mp, Vs, en) and parse_info("h\n1\t0\t0\t0\ta; b, c\n")[1] == ["a", "b", "c"]
    import zipfile as _z
    with tempfile.TemporaryDirectory() as t:
        zf = Path(t) / "a.zip"
        with _z.ZipFile(zf, "w") as z:
            z.writestr("ADEChallengeData2016/images/training/x.jpg", b"x")
        try:
            info_names(_z.ZipFile(zf))
            raise AssertionError("missing objectInfo150 accepted")
        except SystemExit as e:
            assert "missing" in str(e)
    # near-val rule on hashes (candidate mirror counts)
    vh = {"v1": [0, 0, 5, 5]}
    assert near_val({"a": (0b1111111111, 7, 99, 99), "b": (99, 98, 0, 1 << 40), "c": ((1 << 20) - 1, (1 << 30) - 1, (1 << 20) - 1, (1 << 25) - 1)}, vh) == {"a", "b"}
    # label presence by pixel share
    png = np.zeros((100, 100), np.uint8)
    png[:50, :] = 13          # person 50%
    png[50:51, :5] = 20       # chair 0.05%
    png[60:70, :10] = 76      # swivel chair 1% -> chair
    png[80:90, :10] = 18      # plant: not mapped
    assert label_set(png, 0.0) == {"person", "chair"} and label_set(png, 0.005) == {"person", "chair"}
    png[60:70, :10] = 0
    assert label_set(png, 0.0) == {"person", "chair"} and label_set(png, 0.001) == {"person"}
    # sets: order, near-val exclusion, disjoint
    ids = [f"ADE_train_{k:08d}" for k in range(2100)]
    S = split_sets(ids, {ids[0], ids[5]})
    assert len(S["D1"]) == N_D and len(S["D2"]) == N_D and len(S["smoke"]) == N_SMOKE
    assert not set(S["D1"]) & set(S["D2"]) and ids[0] not in S["D1"] + S["D2"] + S["smoke"]
    assert S["D1"] == order(S["D1"])
    # premise counts
    pr = premise([{"a", "b", "c"}, {"a", "d"}], [{"a"}, {"x"}])
    assert pr["sum_label"] == 5 and pr["sum_narr_in_label"] == 1 and pr["evaluable_2x"]
    # analysis on synthetic captions: more complete label gold -> larger slope; narrative = salient subset
    rng = np.random.default_rng(0)
    n = 300
    ids = [f"ADE_train_{k:08d}" for k in range(n)]
    pool = sorted(V)
    lab = {i: sorted(rng.choice(pool, 8, replace=False)) for i in ids}
    nar = {i: lab[i][:2] for i in ids}  # salient = first two classes
    caps, models = {}, KEEP[:3]
    for mi, m in enumerate(models):
        for q, k in (("short_en", 2), ("detailed_en", 4 + 2 * mi)):
            caps[run_id(m, q)] = {i: "a photo with " + ", ".join(
                f"a {c}" for c in lab[i][:k] + list(rng.choice(pool, 1))) for i in ids}
    a = analysis(g, ids, lab, nar, caps, models, n_boot=200, n_rep=100)
    assert a["AD1"]["point"] > 0 and a["AD1"]["verdict"] == "PASS", a["AD1"]["point"]
    assert a["AD2"]["verdict"] == "PASS" and a["premise"]["evaluable_2x"], a["AD2"]
    p1, p2 = predict(a["AD1"].pop("_draws"), n), predict_null(a["AD2"], n)
    assert 0.9 < p1 <= 1 and 0.9 < p2 <= 1, (p1, p2)
    assert outcome(a, p1, p2)[0] in ("PROCEED_TO_TIER2", "PASS_LOW_POWER")
    assert outcome(a, 0.5, p2) == ("PASS_LOW_POWER", "predicted_p_pass_below_0.98")
    bad = json.loads(json.dumps(a, default=float))
    bad["premise"]["evaluable_2x"] = False
    assert outcome(bad, 1, 1)[0] == "PREMISE_NOT_MET"
    bad = json.loads(json.dumps(a, default=float))
    bad["AD2"]["verdict"] = "INCONCLUSIVE"
    assert outcome(bad, 1, 1)[0] == "NOT_REPRODUCED"
    # predictions: zero effect -> about 0.025; scaling up the test helps
    assert predict(rng.normal(0, 1, 2000), 1000, 1000) < 0.1
    d = rng.normal(1.0, 1.0, 2000)
    assert predict(d, 1000, 4000) > predict(d, 1000, 1000)
    # guard pieces, cap, job text
    with tempfile.TemporaryDirectory() as t:
        (Path(t) / "images").mkdir()
        (Path(t) / "images/ADE_train_00000001.jpg").write_bytes(b"x")
        assert val_files(Path(t)) == []
        (Path(t) / "images/ADE_val_00000001.jpg").write_bytes(b"x")
        (Path(t) / "x.zip").write_bytes(b"x")
        assert len(val_files(Path(t))) == 2
        L = Path(t) / "l.tsv"
        L.write_text("a\t3600.0\t0\nb\t100.0\t124\n")
        assert left(L) == CAP_S - 3700
        mid = Path(t) / "mid"
        mid.write_text("m3\n")
        try:
            guard("0" * 40, mid)
            raise AssertionError("m3 accepted")
        except SystemExit as e:
            assert "m4" in str(e)
    text = (HERE / "a_t1_job.sh").read_text(encoding="utf-8")
    assert "set -euo pipefail" in text and "a_t1.py guard" in text.replace("$X guard", "a_t1.py guard")
    assert "= m4 ]" in text and "ADE_val" not in text.replace("no ADE_val", "")
    print("a_t1 selftest ok")


def main() -> None:
    ap = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    ap.add_argument("--selftest", action="store_true")
    sub = ap.add_subparsers(dest="cmd")
    s = sub.add_parser("split"); s.add_argument("--zip", type=Path, required=True); s.add_argument("--train", type=Path, required=True)  # noqa: E702
    s.add_argument("--val-hash", type=Path, required=True)
    s = sub.add_parser("select"); s.add_argument("--train", type=Path, required=True); s.add_argument("--ln-train", type=Path, required=True)  # noqa: E702
    s.add_argument("--val-hash", type=Path, required=True)
    s = sub.add_parser("gold"); s.add_argument("--train", type=Path, required=True); s.add_argument("--ln-train", type=Path, required=True)  # noqa: E702
    s.add_argument("--set", default="D1"); s.add_argument("--out", type=Path, required=True)  # noqa: E702
    s = sub.add_parser("stage"); s.add_argument("--train", type=Path, required=True); s.add_argument("--gold", type=Path, required=True)  # noqa: E702
    s.add_argument("--set", default="D1", choices=["D1", "D2"])
    s.add_argument("--root", type=Path, required=True)
    s = sub.add_parser("register"); s.add_argument("--root", type=Path, required=True); s.add_argument("--out", type=Path, required=True)  # noqa: E702
    sub.add_parser("guard").add_argument("--head", required=True)
    sub.add_parser("left").add_argument("--ledger", type=Path, required=True)
    s = sub.add_parser("score"); s.add_argument("--raw", type=Path, required=True); s.add_argument("--gold", type=Path, required=True)  # noqa: E702
    s.add_argument("--out", type=Path, required=True)
    a = ap.parse_args()
    if a.selftest:
        return selftest()
    if a.cmd == "split":
        cmd_split(a.zip, a.train, a.val_hash)
    elif a.cmd == "select":
        if LISTS.exists():
            raise SystemExit(f"{LISTS} exists")
        LISTS.write_text(json.dumps(cmd_select(a.train, a.val_hash, a.ln_train), indent=1) + "\n", encoding="utf-8")
        print(f"{p50.sha_file(LISTS)}  {LISTS.name}")
    elif a.cmd == "gold":
        p50.dump(cmd_gold(a.train, a.ln_train, a.set), a.out)
    elif a.cmd == "stage":
        print(json.dumps(cmd_stage(a.train, a.gold, a.root, a.set)))
    elif a.cmd == "register":
        p50.dump(register(a.root), a.out)
    elif a.cmd == "guard":
        guard(a.head)
    elif a.cmd == "left":
        print(left(a.ledger))
    elif a.cmd == "score":
        cmd_score(a.raw, a.gold, a.out)
    else:
        ap.error("a subcommand or --selftest is required")


if __name__ == "__main__":
    main()
