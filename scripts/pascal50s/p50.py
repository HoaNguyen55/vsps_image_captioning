#!/usr/bin/env python3
"""PASCAL-50S k-ladder evaluator (Paper A): manuscript/prereg/2026-10-28_pascal50s/PREREG.md, prereg_id
2026-10-28_a_p50_kladder (CC-144, CC-142 W2/W4). Writes and prints numbers only, never caption or reference text.
Decoding is scripts/lb/decode_hf_vlm.py (A-N2, sha e2de1881) unchanged; golds, scores, slopes and verdict rules are
scripts/g2b/score_g2b.py unchanged; the matcher is score_coco_probe.en_classes unchanged.

  p50.py --selftest                       CPU, synthetic data only
  p50.py imports                          every module the run uses (first M3 step)
  p50.py refcheck --json F --out O        structure-only check of pascal50S.json (W6); exit 2 = NOT_EVALUABLE (input)
  p50.py stage --tar T --tar-sha H --out O    1,020 images + 1,000 XML from the VOC2008 tar, manifests, §4.4(c)
  p50.py register --out REG               runtime LB registration: A-N2 models/decode/decoder/venv copied unchanged
  p50.py timed --timeout S --ledger L --label R -- CMD ...      GPU process with slice timestamps; 124 = timeout
  p50.py plan --timing DIR --ledger L --out PLAN                cap from the measured smoke (§6)
  p50.py budget --plan P --ledger L --left F --run R            timeout for R; exit 3 = the model leaves
  p50.py ngram --json F FILE ...          8-gram hits against pascal50S.json; exit 1 if any (W4)
  p50.py score --raw DIR --plan P --left F --stage S --reg REG --out O      the one look (§7)
"""
from __future__ import annotations

import argparse
import hashlib
import json
import os
import re
import subprocess
import sys
import tempfile
import threading
import time
import unicodedata
import xml.etree.ElementTree as ET
from pathlib import Path

import numpy as np

HERE = Path(__file__).resolve().parent
ROOT = HERE.parents[1]
sys.path[:0] = [str(ROOT), str(ROOT / "scripts"), str(ROOT / "scripts/g2b"), str(ROOT / "scripts/lb")]

PREREG_ID = "2026-10-28_a_p50_kladder"
A_N2 = ("manuscript/prereg/2026-10-19_a_n2_lvlm_gold_ladder.json",
        "d5714e2b25e5f1d36fa42813cc5891a82d0b80a73e69fb08d940e05e2055f309")
DECODER_SHA = "e2de18811e2ffeb61ed72cb2399d41123e9a8f6ccd73a5ec35f778dcbe2f5ac4"
IDS = (HERE / "p50_1000_ids.txt", "a8539efbc785e6ce9b977f7f8fc977adb039f4cc52bb1c437c4980c26c034cb4")
SMOKE = (HERE / "p50_smoke20_ids.txt", "6b603537a5a5cfdb867d6f97733896513d5e69be402d3ca5bc080e7dcea83b52")
P50_JSON = ("5384abf1340f7295d535b99453bc2313e521c111ad13ec257239a4d5b477ef42", 4546057)  # @ f281464, Ken-computed
VOC_TAR_BYTES = 577034240
DATA_ROOT = Path(os.environ.get("NCS_DATA", "/root/ncs-data")) / "datasets" / "pascal50s"
V20 = {"aeroplane": "airplane", "bicycle": "bicycle", "bird": "bird", "boat": "boat", "bottle": "bottle", "bus": "bus",
       "car": "car", "cat": "cat", "chair": "chair", "cow": "cow", "diningtable": "dining table", "dog": "dog",
       "horse": "horse", "motorbike": "motorcycle", "person": "person", "pottedplant": "potted plant",
       "sheep": "sheep", "sofa": "couch", "train": "train", "tvmonitor": "tv"}  # PREREG §4.2, frozen
DROP_ORDER = ["idefics3_8b", "llava_ov_7b", "internvl3_8b", "llava15_7b", "smolvlm2_2b", "qwen25vl_3b",
              "qwen25vl_7b", "qwen3vl_8b"]  # PREREG §2 (judge-fixed, CC-144 ruling 2)
MODES = ("short_en", "detailed_en")
K_LADDER, N_REP, SUBSET_SEED, BOOT_SEED, N_BOOT, CI = (1, 2, 5, 10, 20), 20, 1, 0, 1000, (2.5, 97.5)
N_TEST, N_SMOKE, CEIL_S, FACTOR, MIN_MODELS, MAX_FAULTS = 1000, 20, 8 * 3600, 1.5, 3, 2
ID_FIELDS = ("image_id", "image", "filename", "file_name", "img")
LIST_FIELDS = ("captions", "refs", "references", "sentences")
TOK = re.compile(r"\w+")


class Refused(Exception):
    pass


def sha_bytes(b: bytes) -> str:
    return hashlib.sha256(b).hexdigest()


def sha_file(p) -> str:
    h = hashlib.sha256()
    with Path(p).open("rb") as fh:
        for chunk in iter(lambda: fh.read(1 << 22), b""):
            h.update(chunk)
    return h.hexdigest()


def id_list(spec=IDS) -> list[str]:
    path, want = spec
    if sha_file(path) != want:
        raise SystemExit(f"REFUSED: {path.name} differs from its pin")
    return path.read_text().split()


def dump(obj, out) -> None:
    Path(out).write_text(json.dumps(obj, indent=1, sort_keys=True) + "\n", encoding="utf-8")


# ------------------------------------------------------------------------------------------- references (W6)
def norm(key) -> str:
    """The only key normalizations allowed (CC-144 W6): basename (drops a class/ prefix), then strip .jpg/.JPG."""
    s = str(key).replace("\\", "/").rsplit("/", 1)[-1]
    return s[:-4] if s.endswith((".jpg", ".JPG")) else s


def raw_table(data) -> tuple[str, dict[str, list[str]]]:
    """{raw key: [reference]} from one of three pre-listed shapes; anything else is refused."""
    strs = lambda v: isinstance(v, list) and all(isinstance(s, str) for s in v)  # noqa: E731
    if isinstance(data, dict) and isinstance(data.get("images"), list) and isinstance(data.get("annotations"), list):
        files = {a["id"]: a["file_name"] for a in data["images"]}
        out: dict[str, list[str]] = {}
        for a in data["annotations"]:
            if a.get("image_id") not in files or not isinstance(a.get("caption"), str):
                raise Refused("coco shape: an annotation without a known image or a caption string")
            out.setdefault(str(files[a["image_id"]]), []).append(a["caption"])
        return "coco_images_annotations", out
    if isinstance(data, dict) and data and all(strs(v) for v in data.values()):
        return "dict_key_to_list", {str(k): v for k, v in data.items()}
    if isinstance(data, list) and data and all(isinstance(r, dict) for r in data):
        idf = {f for r in data for f in ID_FIELDS if f in r}
        if len(idf) != 1:
            raise Refused(f"record shape: {len(idf)} id fields")
        f = idf.pop()
        out = {}
        for r in data:
            if not isinstance(r.get(f), (str, int)):
                raise Refused("record shape: a record without its id")
            txt = [r["caption"]] if isinstance(r.get("caption"), str) else \
                next((r[k] for k in LIST_FIELDS if strs(r.get(k))), None)
            if txt is None:
                raise Refused("record shape: a record without caption text")
            out.setdefault(str(r[f]), []).extend(txt)
        return f"records_{f}", out
    raise Refused("unknown shape")


def ref_table(data, ids: list[str]) -> tuple[dict, dict[str, list[str]] | None]:
    """Structure facts (numbers and key patterns only) and, if the keys match the ids 1:1, {id: [reference]}."""
    try:
        shape, raw = raw_table(data)
    except Refused as e:
        return {"shape": None, "refused": str(e), "one_to_one": False}, None
    by: dict[str, list[str]] = {}
    for k in raw:
        by.setdefault(norm(k), []).append(k)
    pattern: dict[str, int] = {}
    for k in raw:
        p = re.sub(r"[0-9]", "9", re.sub(r"[A-Za-z]+/", "<class>/", k))
        pattern[p] = pattern.get(p, 0) + 1
    want = set(ids)
    hist: dict[int, int] = {}
    for n in (len(raw[k]) for k in raw):
        hist[n] = hist.get(n, 0) + 1
    facts = {"shape": shape, "n_raw_keys": len(raw), "key_patterns": dict(sorted(pattern.items())),
             "n_keys_after_norm": len(by), "n_keys_colliding": sum(len(v) > 1 for v in by.values()),
             "n_match": len(want & set(by)), "n_extra": len(set(by) - want), "n_missing": len(want - set(by)),
             "n_refs_hist": {str(n): c for n, c in sorted(hist.items())}}
    facts["one_to_one"] = facts["n_match"] == len(want) == len(by) == len(raw)
    return facts, ({i: raw[by[i][0]] for i in ids} if facts["one_to_one"] else None)


def load_refs(path, ids) -> dict[str, list[str]]:
    facts, refs = ref_table(json.loads(Path(path).read_text(encoding="utf-8")), ids)
    if refs is None:
        raise SystemExit("NOT_EVALUABLE (input): pascal50S.json keys do not match the 1,000 ids 1:1")
    return refs


def draw(n_refs: list[int]) -> dict[int, list[list[tuple]]]:
    """PREREG §3.2: default_rng(1); for k in (1, 2, 5, 10, 20), for r = 1..20, for each of the 1,000 images in id order:
    choice(n, k, replace=False); an image with n < k takes all its references and makes no draw."""
    rng = np.random.default_rng(SUBSET_SEED)
    return {k: [[tuple(int(j) for j in rng.choice(n, k, replace=False)) if n >= k else tuple(range(n))
                 for n in n_refs] for _ in range(N_REP)] for k in K_LADDER}


# ------------------------------------------------------------------------------------------- 8-gram check (W4)
def toks(s: str) -> list[str]:
    return TOK.findall(unicodedata.normalize("NFC", s).lower())


def grams8(t: list[str]) -> set[tuple]:
    return {tuple(t[i:i + 8]) for i in range(len(t) - 7)}


def ngram_hits(refs: dict[str, list[str]], files) -> dict:
    G: set[tuple] = set()
    control = None
    for rs in refs.values():
        for s in rs:
            t = toks(s)
            control = control or (t if len(t) >= 8 else None)
            G |= grams8(t)
    out = {"reference_8grams": len(G), "positive_control_hits": len(grams8(control or []) & G), "files": {}}
    for f in files:
        lines = Path(f).read_text(encoding="utf-8").splitlines()
        out["files"][Path(f).name] = sum(len(grams8(toks(x)) & G) for x in lines)
    return out


# ------------------------------------------------------------------------------------------- staging and registration
def voc_gold(xml_bytes: bytes) -> set[str]:
    """PREREG §4.1: every <object> class, difficult and truncated included, mapped by the frozen V20 table."""
    names = {o.findtext("name", "").strip() for o in ET.fromstring(xml_bytes).iter("object")}
    if names - set(V20):
        raise Refused("an object name outside the 20 VOC classes")
    return {V20[n] for n in names}


def stage(tar: Path, tar_sha: str, root: Path) -> dict:
    import tarfile

    if tar.stat().st_size != VOC_TAR_BYTES or sha_file(tar) != tar_sha:
        raise SystemExit("REFUSED: the VOC tar's size or sha256 differs from the value recorded in EVENTS")
    ids, smoke = id_list(), id_list(SMOKE)
    want = {f"JPEGImages/{i}.jpg" for i in ids + smoke} | {f"Annotations/{i}.xml" for i in ids}
    got: dict[str, bytes] = {}
    with tarfile.open(tar) as tf:
        for m in tf:
            tail = "/".join(m.name.split("/")[-2:])
            if m.isfile() and tail in want:
                if tail in got:
                    raise SystemExit(f"REFUSED: two tar members end in {tail}")
                got[tail] = tf.extractfile(m).read()
    miss_img = [i for i in ids + smoke if f"JPEGImages/{i}.jpg" not in got]
    if miss_img:
        print(f"NOT_EVALUABLE (input): {len(miss_img)} image(s) missing from the tar; no image is dropped")
        sys.exit(2)
    for d in ("JPEGImages", "Annotations", "sets"):
        (root / d).mkdir(parents=True, exist_ok=True)
    for tail, b in got.items():
        (root / tail).write_bytes(b)
    facts = {"tar_sha256": tar_sha, "tar_bytes": VOC_TAR_BYTES, "n_images": len(ids), "n_smoke": len(smoke)}
    for name, lst in (("p50_1000", ids), ("p50_smoke20", smoke)):
        rows = "".join(f"{i}\t{i}.jpg\t{sha_bytes(got[f'JPEGImages/{i}.jpg'])}\n" for i in lst)
        (root / f"sets/{name}.tsv").write_text(rows, encoding="utf-8")
        facts[f"manifest_{name}_sha256"] = sha_bytes(rows.encode())
    miss_xml = [i for i in ids if f"Annotations/{i}.xml" not in got]
    bad = 0
    for i in ids:
        try:
            if f"Annotations/{i}.xml" in got:
                voc_gold(got[f"Annotations/{i}.xml"])
        except (Refused, ET.ParseError):
            bad += 1
    facts.update({"n_xml_missing": len(miss_xml), "n_xml_unreadable": bad,
                  "label_rung": "kept" if not miss_xml and not bad else "dropped (PREREG §4.4(c))"})
    return facts


def register(root: Path) -> dict:
    """The decoder's registration: A-N2's schema, models, decode, decoder and venv blocks copied unchanged; the two
    PASCAL sets with manifests written by `stage`; runs p50_<model>-<mode> and p50smoke_<model>-<mode>."""
    a = (ROOT / A_N2[0]).read_bytes()
    if sha_bytes(a) != A_N2[1]:
        raise SystemExit("REFUSED: the A-N2 registration differs from its pin")
    A = json.loads(a)
    reg = {k: A[k] for k in ("schema", "models", "model_list", "decode", "decoder", "venv")}
    reg.update({"prereg_id": PREREG_ID, "statement": "runtime registration built by scripts/pascal50s/p50.py register",
                "datasets": {}, "runs": []})
    for ds, n, pre in (("p50_1000", N_TEST, "p50"), ("p50_smoke20", N_SMOKE, "p50smoke")):
        man = root / f"sets/{ds}.tsv"
        reg["datasets"][ds] = {"manifest": {"path": str(man), "sha256": sha_file(man)}, "n_images": n,
                               "image_dir": f"{root.name}/JPEGImages"}
        reg["runs"] += [{"run_id": f"{pre}_{m}-{p}", "model": m, "dataset": ds, "prompt_mode": p}
                        for m in A["models"] for p in MODES]
    return reg


# ------------------------------------------------------------------------------------------- timing and the cap (§6)
def timed(cmd: list[str], timeout: float, ledger: Path, label: str, marks_out: Path | None) -> int:
    """Run cmd; stamp each 'slice k/n' line; append label, wall seconds and rc to the GPU ledger. 124 = timeout."""
    t0 = time.time()
    p = subprocess.Popen(cmd, stdout=subprocess.PIPE, stderr=subprocess.STDOUT, text=True)
    hit = []
    timer = threading.Timer(timeout, lambda: (hit.append(1), p.kill()))  # Popen.kill: no error once p has exited
    timer.start()
    marks = []
    for line in p.stdout:
        sys.stdout.write(line)
        m = re.match(r"slice (\d+)/(\d+)$", line.strip())
        if m:
            marks.append([int(m[1]), int(m[2]), round(time.time() - t0, 3)])
    rc = p.wait()
    timer.cancel()
    rc = 124 if hit else rc
    wall = time.time() - t0
    with Path(ledger).open("a") as fh:
        fh.write(f"{label}\t{wall:.1f}\t{rc}\n")
    if marks_out:
        dump({"label": label, "wall_s": round(wall, 1), "rc": rc, "marks": marks}, marks_out)
    return rc


def ledger_rows(ledger: Path) -> list[tuple[str, float, int]]:
    if not Path(ledger).exists():
        return []
    return [(a, float(b), int(c)) for a, b, c in (x.split("\t") for x in Path(ledger).read_text().splitlines() if x)]


def run_cap(t: dict, batch: int) -> float:
    """PREREG §6: s = seconds per image from the slice stamps after the first slice; o = the rest of the wall time
    (load, first slice, parity slice); a 1,000-image run is capped at 1.5 x (o + 1000 s)."""
    mk = t["marks"]
    first = min(batch, N_SMOKE)
    s = (mk[-1][2] - mk[0][2]) / (N_SMOKE - first)
    o = max(t["wall_s"] - N_SMOKE * s, 0.0)
    return FACTOR * (o + N_TEST * s)


def plan(timings: dict[str, dict], batch: dict[str, int], spent: float, left: dict | None = None) -> dict:
    """Models with both smoke timings and not left (a third smoke fault), kept in the drop order within 8 GPU-h."""
    timed_m = [m for m in DROP_ORDER if m not in (left or {}) and all(f"p50smoke_{m}-{p}" in timings for p in MODES)]
    caps = {f"p50_{m}-{p}": round(run_cap(timings[f"p50smoke_{m}-{p}"], batch[m]), 1) for m in timed_m for p in MODES}
    cap_m = {m: sum(caps[f"p50_{m}-{p}"] for p in MODES) for m in timed_m}
    kept = list(timed_m)
    while kept and spent + sum(cap_m[m] for m in kept) > CEIL_S:
        kept.pop(0)
    keep_order = kept[::-1]  # most important first (qwen3vl_8b), so an overrun loses the next model to drop
    return {"smoke_spent_s": round(spent, 1), "run_cap_s": caps, "model_cap_s": cap_m, "kept": keep_order,
            "ceiling_s": CEIL_S, "status": "RUN" if len(kept) >= MIN_MODELS else "STOP (cost)",
            "projected_s": round(spent + sum(cap_m[m] for m in kept), 1)}


def budget(pl: dict, rows: list, left: dict, run: str) -> tuple[int, str]:
    """(timeout, '') or (0, reason the model leaves): FAULT (time) earlier, more than two faults, or a breach."""
    model = run[4:].rsplit("-", 1)[0]
    if model in left:
        return 0, left[model]
    faults = sum(1 for a, _, c in rows if a == run and c not in (0, 124))
    if faults > MAX_FAULTS:
        return 0, f"{faults} faults on {run} (KM)"
    used = sum(b for _, b, _ in rows)
    if used + pl["run_cap_s"][run] > CEIL_S:
        return 0, f"{run} would breach 8 GPU-h ({used:.0f} s used, cap {pl['run_cap_s'][run]} s)"
    return int(pl["run_cap_s"][run]) + 1, ""


def read_left(path) -> dict:
    p = Path(path)
    return dict(x.split("\t", 1) for x in p.read_text().splitlines() if x) if p.exists() else {}


# ------------------------------------------------------------------------------------------- the analysis (§3-§4)
def analysis(g, ids, refs, voc, caps, models, n_boot=N_BOOT, label_rung="kept") -> dict:
    """Every statistic of PREREG §3.6, numbers only. caps = {run: {id: caption}}, runs of the kept models."""
    en = g.MATCH["coco80"]["en"]
    V = set(V20.values())
    runs = [f"p50_{m}-{p}" for m in models for p in MODES]
    ment = {r: [en(caps[r].get(i, "")) for i in ids] for r in runs}
    refm = [[en(s) for s in refs[i]] for i in ids]
    sub = draw([len(x) for x in refm])
    var = {"coco80": g.gold_variants({"refs": refm}, sub),
           "V20": g.gold_variants({"refs": [[s & V for s in r] for r in refm]}, sub)}
    var["V20"]["voc20"] = [[voc[i] for i in ids]]
    for v in var.values():
        v["refs50"] = v.pop("refs_all")
    mentv = {"coco80": ment, "V20": {r: [m & V for m in ment[r]] for r in runs}}
    rows = {(lx, r, gd): g.rows(mentv[lx][r], var[lx][gd]) for lx in var for r in runs for gd in var[lx]}
    clean = [n for n, i in enumerate(ids)
             if all(isinstance(caps[r].get(i), str) and caps[r][i].strip() and g.is_clean(caps[r][i], "en") for r in runs)]

    def on(idx: list[int], fam: list[str]) -> dict:
        idx = np.array(idx)
        N = len(idx)
        Wb = np.random.default_rng(BOOT_SEED).multinomial(N, [1 / N] * N, size=n_boot).astype(float)
        one = np.ones((1, N))
        slope, Ms = {}, {}
        for lx in var:
            for gd in var[lx]:
                pt = [g.scores(rows[(lx, r, gd)], idx, one) for r in fam]
                bs = [g.scores(rows[(lx, r, gd)], idx, Wb) for r in fam]
                slope[(lx, gd)] = (float(g.stat_slope(pt, None)[0]), g.stat_slope(bs, None))
                Ms[lx] = [float(s["M"][0]) for s in pt]
        ok = {lx: all(m > 0 for m in Ms[lx]) and len({round(m, 12) for m in Ms[lx]}) >= 2 for lx in Ms}
        return {"N": N, "slope": slope, "evaluable": ok, "M": Ms}

    def part(S, lx, a, b) -> dict:
        pa, ra = S["slope"][(lx, a)]
        pb, rb = S["slope"][(lx, b)]
        pt, iv = pa - pb, g.ci(ra - rb, *CI)
        v = g.verdict("sign_gt_0", pt, iv) if S["evaluable"][lx] else "NOT_EVALUABLE"
        return {"stat": f"slope[{a}|{lx}](ALL) - slope[{b}|{lx}](ALL)", "point": round(pt, 6),
                "ci95": None if iv is None else [round(x, 6) for x in iv], "verdict": v, "not_FAIL": v != "FAIL"}

    def preds(S) -> dict:
        out = {}
        if label_rung == "kept":
            ps = [part(S, "V20", "refs50", "refs1_randk"), part(S, "V20", "voc20", "refs50")]
            out["P50-A4"] = {"parts": ps, "verdict": g.compound([p["verdict"] for p in ps])}
            out["P50-A4r"] = {"verdict": None, "note": "no verdict: the label rung was kept"}
            out["descriptive_coco80_refs50_vs_refs1"] = part(S, "coco80", "refs50", "refs1_randk") | {"verdict": None}
        else:
            ps = [part(S, "coco80", "refs50", "refs1_randk")]
            out["P50-A4r"] = {"parts": ps, "verdict": ps[0]["verdict"]}
            out["P50-A4"] = {"verdict": None, "note": f"label rung {label_rung}"}
        ladder = [f"refs{k}_randk" for k in K_LADDER] + ["refs50"]
        ps = [part(S, "coco80", b, a) for a, b in zip(ladder, ladder[1:])]
        out["P50-O2"] = {"parts": ps, "verdict": g.compound([p["verdict"] for p in ps])}
        out["P50-NS"] = {f"{gd}|{lx}": {"point": round(p, 6), "ci95": g.ci(r, *CI)}
                         for (lx, gd), (p, r) in S["slope"].items()}
        out["n_images"], out["M"], out["evaluable"] = S["N"], S["M"], S["evaluable"]
        return out

    res = {"models": models, "runs": runs, "label_rung": label_rung, "n_boot": n_boot,
           "n_refs_min_max": [min(map(len, refm)), max(map(len, refm))],
           "n_images_below_k": {str(k): sum(len(x) < k for x in refm) for k in K_LADDER + (50,)}}
    res["analysis_set"] = preds(on(clean, runs)) if clean else {"verdict": "NOT_EVALUABLE", "n_images": 0}
    res["sensitivity_all_images"] = preds(on(list(range(len(ids))), runs))
    for p in ("P50-A4", "P50-A4r", "P50-O2"):
        if "parts" in res["sensitivity_all_images"].get(p, {}):
            res["sensitivity_all_images"][p]["verdict"] = None  # sensitivity: no verdict
            for q in res["sensitivity_all_images"][p]["parts"]:
                q["verdict"] = q["not_FAIL"] = None
    res["PAIR_m_descriptive"] = {m: {f"{gd}|{lx}": round(on(clean, [f"p50_{m}-{p}" for p in MODES])["slope"][(lx, gd)][0], 6)
                                     for lx, gd in [("coco80", "refs1_randk"), ("coco80", "refs50"), ("V20", "voc20")]}
                                 for m in models} if clean else {}
    return res


def check_run(d: dict, run: str, reg: dict, reg_sha: str, ids: list[str]) -> str:
    """'' if a decode file carries the registered provenance, else the KD reason."""
    want = {"schema": "vsps.lb_decode.v1", "prereg_id": PREREG_ID, "prereg_sha256": reg_sha,
            "decoder_sha256": DECODER_SHA, "run_id": run, "dataset": "p50_1000", "n_images": N_TEST,
            "manifest_sha256": reg["datasets"]["p50_1000"]["manifest"]["sha256"], "git_dirty": False,
            "packages": reg["venv"]["packages"]}
    bad = [k for k, v in want.items() if d.get(k) != v] + ([] if sorted(d.get("predictions", {})) == ids else ["ids"])
    return f"KD: {run} provenance differs in {bad}" if bad else ""


def score(raw: Path, pl: dict, left_path: Path, stage_facts: dict, reg_path: Path, out: Path) -> dict:
    import score_g2b as g

    if out.exists():
        raise SystemExit("REFUSED: the decide file exists (one look)")
    ids, root = id_list(), DATA_ROOT
    refs = load_refs(root / "pascal50S.json", ids)
    reg, reg_sha = json.loads(reg_path.read_text()), sha_file(reg_path)
    left = read_left(left_path)
    caps, models = {}, []
    for m in pl["kept"]:
        if m in left:
            continue
        files = [raw / f"p50_{m}-{p}.preds.json" for p in MODES]
        if not all(f.exists() for f in files):
            left[m] = "runs incomplete (KM)"
            continue
        why = ""
        for f, p in zip(files, MODES):
            if (Path(str(f) + ".sha256").read_text().split()[0] != sha_file(f)):
                why = f"KD: sidecar sha differs for {f.name}"
            d = json.loads(f.read_text(encoding="utf-8"))
            why = why or check_run(d, f"p50_{m}-{p}", reg, reg_sha, ids)
            caps[f"p50_{m}-{p}"] = g.read_captions(f)
        if why:
            left[m] = why
        else:
            models.append(m)
    base = {"prereg_id": PREREG_ID, "left": left, "plan": pl, "stage": stage_facts,
            "inputs_sha256": {"pascal50S.json": sha_file(root / "pascal50S.json"), "registration": reg_sha}}
    if len(models) < MIN_MODELS:
        return base | {"status": "STOP (cost)", "models": models}
    voc = {}
    for i in ids:
        x = root / f"Annotations/{i}.xml"
        voc[i] = voc_gold(x.read_bytes()) if stage_facts["label_rung"] == "kept" else set()
    return base | {"status": "SCORED"} | analysis(g, ids, refs, voc, {r: caps[r] for m in models for r in
                                                                      [f"p50_{m}-{p}" for p in MODES]}, models,
                                                   label_rung=stage_facts["label_rung"])


# ------------------------------------------------------------------------------------------- imports (first M3 step)
def imports() -> None:
    import accelerate
    import huggingface_hub
    import num2words
    import PIL
    import torch
    import torchvision
    import transformers

    import decode_hf_vlm  # the pinned G2-B helpers come with it
    import score_g2b  # the matchers, CJK_RE and the synonym table come with it
    sys.path.insert(0, str(ROOT / "scripts/grl"))
    import common

    mods = (accelerate, huggingface_hub, num2words, PIL, torch, torchvision, transformers, decode_hf_vlm, score_g2b, common)
    print("imports ok:", {m.__name__: getattr(m, "__version__", "-") for m in mods}, "cuda", torch.cuda.is_available())


def guard(head: str, mid_file: Path = Path("/root/.vsps_machine_id")) -> None:
    """Before every GPU process: the m3-role machine only (CC-155 W2, CC-159 W1; m4 is refused here, before the shared
    grl/common.host_ok, which accepts m3 and m4 and stays unchanged), idle GPU, HEAD = the committed prereg with a clean
    tree; no B-1, B-2 or C-EN process (never displaces B-2 or B-1, CC-142 W4)."""
    mid = mid_file.read_text().strip().lower() if mid_file.is_file() else ""
    if mid != "m3":
        raise SystemExit(f"REFUSED: {mid_file} is {mid or 'missing'!r}; P50 runs on the m3-role machine only")
    sys.path.insert(0, str(ROOT / "scripts/grl"))
    from common import host_ok

    if host_ok(head, mid_file) != "m3":
        raise SystemExit("REFUSED: host_ok did not return m3")
    busy = subprocess.run(["pgrep", "-f", "scripts/(b1_scaling|b2_external|c_en)/"], capture_output=True, text=True)
    if busy.stdout.strip():
        raise SystemExit("REFUSED: a B-1, B-2 or C-EN process is running; P50 never displaces them")


# ------------------------------------------------------------------------------------------- self-test (CPU)
def selftest() -> None:
    import score_g2b as g

    ok: list[str] = []

    def check(name, cond):
        if not cond:
            raise AssertionError(name)
        ok.append(name)

    ids = id_list()
    check("committed id lists: 1,000 + 20 ids at their pins, disjoint, sorted",
          len(ids) == N_TEST and ids == sorted(ids) and not set(ids) & set(id_list(SMOKE)) and len(id_list(SMOKE)) == 20)
    syn_classes = set(g.SYN.values())
    check("V20: the 20 mapped names are classes of score_coco_probe.load_synonyms()", set(V20.values()) <= syn_classes)
    check("V20 gap disclosed, not fixed: 'aeroplane' matches no class", g.MATCH["coco80"]["en"]("an aeroplane") == set())
    reg = register_check()
    check("registration: A-N2 models/decode/decoder/venv copied unchanged; 32 runs; decoder pin = e2de1881",
          reg["decoder"]["sha256"] == DECODER_SHA and len(reg["runs"]) == 32)
    # references: three shapes give one table; normalizations; refusals
    toy = ["2008_000001", "2008_000002", "2008_000003"]
    s1 = {f"dog/{i}.jpg": [f"w{n} dog" for n in range(3)] for i in toy}
    s2 = [{"image_id": f"{i}.JPG", "caption": f"w{n} dog"} for i in toy for n in range(3)]
    s3 = {"images": [{"id": n, "file_name": f"{i}.jpg"} for n, i in enumerate(toy)],
          "annotations": [{"image_id": n, "caption": f"w{k} dog"} for n in range(3) for k in range(3)]}
    tabs = [ref_table(s, toy) for s in (s1, s2, s3)]
    check("refcheck: dict, record and COCO shapes give the same 1:1 table (basename, .jpg/.JPG stripped)",
          all(t[0]["one_to_one"] and t[1] == tabs[0][1] for t in tabs) and tabs[0][0]["n_refs_hist"] == {"3": 3})
    check("refcheck: colliding keys are not 1:1", not ref_table(s1 | {"cat/2008_000001.jpg": ["x"]}, toy)[0]["one_to_one"])
    check("refcheck: an extra key is not 1:1", not ref_table(s1 | {"2008_000009": ["x"]}, toy)[0]["one_to_one"])
    check("refcheck: an unknown shape is refused", ref_table({"a": 1}, toy)[0]["shape"] is None)
    check("refcheck facts hold no reference text", "dog" not in json.dumps(tabs[1][0]).replace("<class>", ""))
    n_refs = [50, 48, 3, 50, 1]
    d = draw(n_refs)
    check("draw: k = 1 equals score_g2b.random_subsets(seed 1, r = 20)",
          d[1] == g.random_subsets(n_refs, 1, N_REP, SUBSET_SEED)[1])
    check("draw: n < k takes every reference; others are k distinct indices",
          d[5][0][2] == (0, 1, 2) and d[2][0][4] == (0,) and all(len(set(s[0])) == 20 for s in [d[20][3]]))
    check("draw: reproducible", draw(n_refs) == d)
    xml = b"<a><object><name>person</name><difficult>1</difficult></object><object><name>sofa</name></object></a>"
    check("VOC gold: difficult objects count; sofa -> couch", voc_gold(xml) == {"person", "couch"})
    try:
        voc_gold(b"<a><object><name>lamp</name></object></a>")
        raise AssertionError("an unknown VOC name was accepted")
    except Refused:
        ok.append("VOC gold: a name outside the 20 classes is refused")
    # analysis on synthetic data: known slopes, verdict plumbing, numbers-only output
    rng = np.random.default_rng(7)
    words = ["dog", "cat", "person", "horse", "car", "bus", "chair", "bottle", "bird", "boat", "kite", "pizza"]
    tid = [f"2008_{n:06d}" for n in range(40)]
    refs = {i: [" and ".join(rng.choice(words, rng.integers(1, 4), replace=False)) for _ in range(50)] for i in tid}
    voc = {i: {"person", "dog"} for i in tid}
    models = ["qwen3vl_8b", "qwen25vl_7b", "smolvlm2_2b"]
    caps = {}
    for j, m in enumerate(models):
        for p, n in (("short_en", 1 + j % 2), ("detailed_en", 3 + j)):
            caps[f"p50_{m}-{p}"] = {i: " ".join(rng.choice(words, n, replace=False)) for i in tid}
    res = analysis(g, tid, refs, voc, caps, models, n_boot=50)
    A = res["analysis_set"]
    check("analysis: P50-A4 (2 parts), P50-O2 (5 parts), P50-NS (13 golds) present",
          len(A["P50-A4"]["parts"]) == 2 and len(A["P50-O2"]["parts"]) == 5 and len(A["P50-NS"]) == 13)
    en = g.MATCH["coco80"]["en"]
    lm, f1 = [], []
    for r in res["runs"]:
        ms = [en(caps[r][i]) for i in tid]
        gs = [set().union(*(en(s) for s in refs[i])) for i in tid]
        P = sum(len(m & q) for m, q in zip(ms, gs)) / sum(map(len, ms))
        R = np.mean([len(m & q) / len(q) for m, q in zip(ms, gs) if q])
        lm.append(np.log(sum(map(len, ms)) / len(tid)))
        f1.append(100 * 2 * P * R / (P + R))
    known = float(np.polyfit(lm, f1, 1)[0])
    check("analysis: slope[refs50|coco80] equals an independent OLS of 100*F1 on ln M",
          abs(A["P50-NS"]["refs50|coco80"]["point"] - known) < 1e-6)
    check("analysis: sensitivity carries no verdict", res["sensitivity_all_images"]["P50-A4"]["verdict"] is None)
    caps_flat = {r: {i: "dog" for i in tid} for r in caps}
    flat = analysis(g, tid, refs, voc, caps_flat, models, n_boot=20)["analysis_set"]
    check("not_evaluable: fewer than 2 distinct M_x gives NOT_EVALUABLE for every part (W5)",
          flat["P50-A4"]["verdict"] == "NOT_EVALUABLE" and flat["P50-O2"]["verdict"] == "NOT_EVALUABLE")
    r2 = analysis(g, tid, refs, voc, caps, models, n_boot=20, label_rung="dropped (PREREG §4.4(c))")["analysis_set"]
    check("label rung dropped before the look: P50-A4r is primary", r2["P50-A4r"]["verdict"] is not None
          and r2["P50-A4"]["verdict"] is None)
    with tempfile.TemporaryDirectory() as tmp:
        t = Path(tmp)
        (t / "out.json").write_text(json.dumps(res, default=str, indent=1))
        (t / "leak.txt").write_text("header\n" + refs[tid[0]][0] + " " + " ".join(["dog"] * 9) + "\n")
        h = ngram_hits({"x": ["a dog runs on the green grass near a red bus today"]}, [t / "out.json"])
        h2 = ngram_hits({"x": ["dog " * 9 + "end"]}, [t / "leak.txt"])
        check("8-gram check: positive control hits; the numbers-only result has 0 hits; a copied sentence is caught",
              h["positive_control_hits"] > 0 and h["files"]["out.json"] == 0 and h2["files"]["leak.txt"] > 0)
        led = t / "ledger.tsv"
        prog = "import time\nfor k in (1, 2, 3):\n    print(f'slice {k}/3', flush=True); time.sleep(0.2)\n"
        rc = timed([sys.executable, "-c", prog], 30, led, "p50smoke_x-short_en", t / "m.json")
        mk = json.loads((t / "m.json").read_text())
        rc2 = timed([sys.executable, "-c", "import time; time.sleep(30)"], 0.5, led, "p50_x-short_en", None)
        check("timed: slice stamps recorded, ledger appended, timeout returns 124",
              rc == 0 and len(mk["marks"]) == 3 and rc2 == 124 and len(ledger_rows(led)) == 2)
    batch = {m: 4 for m in DROP_ORDER}
    fast = {f"p50smoke_{m}-{p}": {"wall_s": 60.0, "marks": [[k, 5, 20.0 + 2 * k] for k in range(1, 6)]}
            for m in DROP_ORDER for p in MODES}
    pl = plan(fast, batch, 600.0)
    check("cap: s = 0.5 s/img, o = 50 s -> 1.5 x (50 + 500) = 825 s per run; all 8 kept within 8 GPU-h",
          pl["run_cap_s"]["p50_qwen3vl_8b-short_en"] == 825.0 and len(pl["kept"]) == 8 and pl["status"] == "RUN")
    slow = {k: {"wall_s": 200.0, "marks": [[j, 5, 20.0 + 16 * j] for j in range(1, 6)]} for k in fast}
    pl2 = plan(slow, batch, 600.0)
    check("cap: over the ceiling, whole models leave in the drop order (idefics3 first, qwen3vl last)",
          pl2["kept"][0] == "qwen3vl_8b" and "idefics3_8b" not in pl2["kept"] and pl2["projected_s"] <= CEIL_S)
    vslow = {k: {"wall_s": 900.0, "marks": [[j, 5, 20.0 + 80 * j] for j in range(1, 6)]} for k in fast}
    check("cap: fewer than 3 models left is STOP (cost)", plan(vslow, batch, 600.0)["status"] == "STOP (cost)")
    part = {k: v for k, v in fast.items() if "qwen3vl_8b" not in k}
    pl3 = plan(part, batch, 600.0, {"llava15_7b": "3 smoke faults"})
    check("cap: a model without smoke timings or with a third smoke fault is not planned",
          pl3["kept"] == ["qwen25vl_7b", "qwen25vl_3b", "smolvlm2_2b", "internvl3_8b", "llava_ov_7b", "idefics3_8b"])
    rows = [("p50smoke_a", 600.0, 0), ("p50_qwen3vl_8b-short_en", 10.0, 1)] * 1
    check("budget: a run inside the ceiling gets its cap as timeout", budget(pl, rows, {}, "p50_qwen3vl_8b-short_en")[0] == 826)
    check("budget: a third fault makes the model leave",
          budget(pl, [("p50_qwen3vl_8b-short_en", 1.0, 1)] * 3, {}, "p50_qwen3vl_8b-short_en")[0] == 0)
    check("budget: a run that would breach 8 GPU-h makes the model leave",
          budget(pl, [("x", CEIL_S - 100.0, 0)], {}, "p50_qwen3vl_8b-short_en")[0] == 0)
    check("budget: a model that left (FAULT (time)) gets no rerun",
          budget(pl, [], {"qwen3vl_8b": "FAULT (time)"}, "p50_qwen3vl_8b-detailed_en")[0] == 0)
    with tempfile.TemporaryDirectory() as tmp:
        for mid in ("m4", "", "m3x"):
            f = Path(tmp) / "mid"
            f.write_text(mid + "\n")
            try:
                guard("0" * 40, f)
                raise AssertionError(f"guard accepted machine id {mid!r}")
            except SystemExit as e:
                if "m3-role machine only" not in str(e):
                    raise
        ok.append("guard: machine id m4, empty or other is refused before any GPU or git check (CC-159 W1)")
    print("\n".join("PASS " + n for n in ok) + "\np50 selftest ok")


def register_check() -> dict:
    """register() on a temporary root, then the decoder's own load_prereg on the result."""
    import decode_hf_vlm as dec

    with tempfile.TemporaryDirectory() as tmp:
        root = Path(tmp) / "pascal50s"
        (root / "sets").mkdir(parents=True)
        for ds, lst in (("p50_1000", id_list()), ("p50_smoke20", id_list(SMOKE))):
            (root / f"sets/{ds}.tsv").write_text("".join(f"{i}\t{i}.jpg\t{'0' * 64}\n" for i in lst))
        reg = register(root)
        A = json.loads((ROOT / A_N2[0]).read_text())
        if any(json.dumps(reg[k], sort_keys=True) != json.dumps(A[k], sort_keys=True)
               for k in ("models", "decode", "decoder", "venv")):
            raise AssertionError("a copied A-N2 block differs")
        (Path(tmp) / "reg.json").write_text(json.dumps(reg))
        dec.load_prereg(Path(tmp) / "reg.json")
        if len(dec.manifest_items(reg, "p50_1000")) != N_TEST:
            raise AssertionError("manifest not read by the decoder")
    return reg


# ------------------------------------------------------------------------------------------- CLI
def main() -> None:
    ap = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    ap.add_argument("cmd", nargs="?")
    ap.add_argument("rest", nargs=argparse.REMAINDER)
    ap.add_argument("--selftest", action="store_true")
    a, _ = ap.parse_known_args()
    if a.selftest:
        return selftest()
    p = argparse.ArgumentParser()
    for f in ("--json", "--out", "--tar", "--tar-sha", "--ledger", "--label", "--timing", "--plan", "--left", "--run",
              "--raw", "--stage", "--reg", "--marks", "--model", "--reason", "--head"):
        p.add_argument(f)
    p.add_argument("--timeout", type=float)
    argv = sys.argv[2:]
    cmd_tail = argv[argv.index("--") + 1:] if "--" in argv else []
    o, files = p.parse_known_args(argv[:argv.index("--")] if "--" in argv else argv)
    if a.cmd == "imports":
        imports()
    elif a.cmd == "refcheck":
        b = Path(o.json).read_bytes()
        if (sha_bytes(b), len(b)) != P50_JSON:
            raise SystemExit("REFUSED: pascal50S.json differs from the sha256/size pinned in the prereg (§1.1)")
        facts, refs = ref_table(json.loads(b), id_list())
        dump(facts, o.out)
        print(json.dumps(facts, sort_keys=True))
        sys.exit(0 if refs is not None else 2)
    elif a.cmd == "stage":
        f = stage(Path(o.tar), o.tar_sha, DATA_ROOT)
        dump(f, o.out)
        print(json.dumps(f, sort_keys=True))
    elif a.cmd == "register":
        dump(register(DATA_ROOT), o.out)
    elif a.cmd == "timed":
        sys.exit(timed(cmd_tail, o.timeout, Path(o.ledger), o.label, Path(o.marks) if o.marks else None))
    elif a.cmd == "plan":
        A = json.loads((ROOT / A_N2[0]).read_text())
        tm = {f.stem: json.loads(f.read_text()) for f in Path(o.timing).glob("p50smoke_*.json")}
        spent = sum(b for x, b, _ in ledger_rows(Path(o.ledger)) if x.startswith("p50smoke_"))
        pl = plan(tm, {m: A["models"][m]["batch_size"] for m in DROP_ORDER}, spent, read_left(o.left))
        dump(pl, o.out)
        print(json.dumps(pl, sort_keys=True))
        sys.exit(0 if pl["status"] == "RUN" else 3)
    elif a.cmd == "kept":
        print(" ".join(json.loads(Path(o.plan).read_text())["kept"]))
    elif a.cmd == "budget":
        t, why = budget(json.loads(Path(o.plan).read_text()), ledger_rows(Path(o.ledger)), read_left(o.left), o.run)
        if why:
            model = o.run[4:].rsplit("-", 1)[0]
            if model not in read_left(o.left):
                with Path(o.left).open("a") as fh:
                    fh.write(f"{model}\t{why}\n")
            print(why, file=sys.stderr)
            sys.exit(3)
        print(t)
    elif a.cmd == "leave":
        if o.model not in read_left(o.left):
            with Path(o.left).open("a") as fh:
                fh.write(f"{o.model}\t{o.reason}\n")
    elif a.cmd == "guard":
        guard(o.head)
    elif a.cmd == "ngram":
        h = ngram_hits(load_refs(o.json, id_list()), files)
        print(json.dumps(h, sort_keys=True))
        sys.exit(0 if h["positive_control_hits"] > 0 and not any(h["files"].values()) else 1)
    elif a.cmd == "score":
        res = score(Path(o.raw), json.loads(Path(o.plan).read_text()), Path(o.left),
                    json.loads(Path(o.stage).read_text()), Path(o.reg), Path(o.out))
        Path(o.out).write_text(json.dumps(res, indent=1, sort_keys=True, default=str) + "\n", encoding="utf-8")
        print(f"wrote {o.out}: {res['status']}")
    else:
        ap.error("unknown command; see --help")


if __name__ == "__main__":
    main()
