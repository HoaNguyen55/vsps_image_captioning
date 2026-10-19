#!/usr/bin/env python3
"""A-N3 scorer (Paper A, PD-21) for manuscript/prereg/2026-10-19_a_n3_criterion_mhaldetect.json (commit 9f4097f); every
threshold, seed, level and registered part is read from it and its constants_source. The M-HalDetect copy (CC BY-NC
4.0, git-excluded) is parsed as JSON only after its sha256 and git-blob pins match; no M-HalDetect text is written.
    score_an3.py gate   OUT.json --coco-zip ZIP  provenance of every input and the self-check; no A-N3 statistic
    score_an3.py dryrun OUT.json                 SYNTHETIC records end to end through the statistic path, with asserts
    score_an3.py run    OUT.json --gate G.json   the analysis; only with this file and G.json (all-PASS gate) at HEAD
Outputs are never overwritten."""
from __future__ import annotations

import argparse
import functools
import hashlib
import json
import re
import subprocess
import sys
import zipfile
from collections import Counter
from pathlib import Path

import numpy as np
from scipy.stats import kendalltau

HERE = Path(__file__).resolve()
ROOT = Path(subprocess.run(["git", "-C", str(HERE.parent), "rev-parse", "--show-toplevel"], capture_output=True,
                           text=True, check=True).stdout.strip())
PREREG = ("manuscript/prereg/2026-10-19_a_n3_criterion_mhaldetect.json",
          "d862cde5eadf50003a7f27685df43f6792b25797cc26e6b9ddbc14f79c1ca4ff")  # GATE_LOG.md CC-036
G2B = ("manuscript/prereg/2026-10-18_g2b_qwen3vl_ladder.json",  # golds.constants_source, committed in 0932ba1
       "c506bc777b483f5097561d2894a535f33e5e9e27745af07c0f979fbac5560055")
# Task-folder names cited by the prereg -> committed files with the same sha (GATE_LOG.md CC-036, commit 9f4097f).
RENAMED = {f"a_n3_{a}": f"data/an3/mhaldetect_{b}" for a, b in (
    ("analysis_set_v2.json", "analysis_set.json"), ("image_ids_v2.txt", "analysis_image_ids.txt"),
    ("excluded_no_instances_v2.txt", "excluded_no_instance_ids.txt"), ("overlap.json", "overlap.json"),
    ("mhaldetect_counts.json", "release_counts.json"))}
COUNTS = "7f9fecfe4a3e472187bdd8ef8d504bbf03ef8e1e6da786f00d964a3fb63da944"  # counts_source has no sha in the prereg
OUTCOMES = ["NOT_TESTABLE", "NOT_SUPPORTED", "SUPPORTED", "MIXED"]
PART = re.compile(r"tau_b\((\w+)@(\w+), HP\)")
SEEN: dict[str, str] = {}  # every input read, with its sha256
m = g = sc = SYN = None  # measures, score_g2b, score_coco_probe and the synonyms: set by main() once their pins match


def sha(data: bytes) -> str:
    return hashlib.sha256(data).hexdigest()


def pinned(rel, want: str | None = None, head: bool = True) -> bytes:
    """Bytes of `rel`, refused unless its sha256 is the pin `want` (if given) and, if `head`, it is its blob at HEAD."""
    p = ROOT / rel
    data = p.read_bytes()
    if head and data != subprocess.run(["git", "-C", str(ROOT), "cat-file", "blob", f"HEAD:{rel}"],
                                       capture_output=True).stdout or want and sha(data) != want:
        raise SystemExit(f"PROVENANCE FAIL: {rel} (sha256 {sha(data)}) differs from its pin or from its blob at HEAD")
    SEEN[p.relative_to(ROOT).as_posix() if p.is_relative_to(ROOT) else p.name] = sha(data)
    return data


def config(P: dict, G: dict) -> dict:
    """Constants from the prereg and its constants_source; refused if they disagree or a part does not parse."""
    dc, gd = G["design_constants"], P["golds"]
    one = re.search(r"random_subsets\(\[5\]\*N, kmax=(\d+), n_rep=(\d+), seed=(\d+)\)", gd["one_ref"])
    boot = re.match(r"(\d+) image-cluster draws: numpy\.random\.default_rng\((\d+)\)\.multinomial\(N_img, "
                    r"\[1/N_img\]\*N_img, size=n_boot\) over images in id order", P["statistic"]["bootstrap"])
    cfg = {"kmax": int(one[1]), "n_rep": dc["n_random_subsets"]["value"], "n_boot": dc["n_boot"]["value"],
           **dc["set_by_this_registration"], "ci": [float(x) for x in re.findall(r"[\d.]+\d", P["statistic"]["ci"])],
           **{k: P["testability_floor"][k] for k in ("min_records", "min_images")},
           "levels": {lv: re.split(r"[:\s]", gd[lv])[0] for lv in ("one_ref", "all_refs", "complete", "union")},
           "parts": {k: {t: PART.findall(t) for t in v["parts"]} for k, v in P["predictions"].items()},
           "rules": {k: re.fullmatch(r"compound of (\w+)", v["rule"])[1] for k, v in P["predictions"].items()},
           "data_path_check": gd["instance_classes"]["data_path_check"]}
    if not (gd["constants_source"]["path"] == G2B[0] and cfg["levels"]["one_ref"] == f"refs{one[1]}_randk"
            and [int(one[2]), int(one[3]), int(boot[2]), int(boot[1])] ==
            [cfg["n_rep"], cfg["subset_seed"], cfg["bootstrap_seed"], cfg["n_boot"]]
            and cfg["ci"] == [dc["ci_lo_percentile"]["value"], dc["ci_hi_percentile"]["value"]]
            and set(cfg["rules"].values()).issubset(P["verdict_rules"]) and P["outcome_rule"]["order"] == OUTCOMES):
        raise SystemExit("REFUSED: the prereg constants disagree with their source or with this scorer")
    return cfg


def modules(P: dict):
    """measures (it imports score_g2b and score_coco_probe) once their prereg pins match; every repo module the import
    loaded, and the lexicon behind measures.U80, must then be committed unmodified at HEAD."""
    for rec in P["measures"]["imported_unchanged"]:
        pinned(rec["path"], rec["sha256"])
    sys.path.insert(0, str(ROOT / "scripts/g2b/an1"))
    import measures
    for f in {Path(getattr(x, "__file__", None) or "/").resolve() for x in list(sys.modules.values())} - {HERE}:
        if f.is_relative_to(ROOT):
            pinned(f.relative_to(ROOT).as_posix())
    pinned("data/coco_probe/coco80_vi.json")
    return measures, measures.g, measures.g.sc


def en(text: str) -> set:
    return sc.en_classes(text, SYN)


def download(P: dict, dl: str | None) -> dict[str, bytes]:
    """The M-HalDetect files, read only once their sha256 and git-blob pins (repo commit in the prereg) match."""
    pin, d = P["licence_handling"]["source_pin"], Path(dl or P["licence_handling"]["download"].split()[0])
    raw = {f: pinned(d / f, want, head=False) for f, want in pin["sha256"].items()}
    if pin != P["data"]["release_pin"] or any(hashlib.sha1(b"blob %d\0" % len(v) + v).hexdigest() != pin["blobs"][f]
                                              for f, v in raw.items()):
        raise SystemExit(f"PROVENANCE FAIL: the M-HalDetect copy differs from its git-blob pins at {pin['commit']}")
    return raw


def parse(raw: dict, inst: dict) -> tuple[list, dict, dict, list]:
    """Records deduplicated on (image, response), first in file order (train, then val), on the analysis images; with
    the release counts and analysis-set aggregates they reproduce."""
    allr, recs, seen = [(s, r) for s in ("train", "val") for r in json.loads(raw[f"{s}_raw.json"])], [], set()
    if not all(re.fullmatch(r"COCO_val2014_\d{12}\.jpg", r["image"]) for _, r in allr):
        raise SystemExit("REFUSED: an image name is not COCO_val2014_%012d.jpg")
    for s, r in allr:
        if (r["image"], r["response"]) not in seen:
            seen.add((r["image"], r["response"]))
            recs.append(dict(r, split=s, img=int(r["image"][-16:-4])))
    imgs, ra = sorted({r["img"] for r in recs}), [r for r in recs if inst.get(r["img"])]
    keep, ann = {r["img"] for r in ra}, [(r, a) for _, r in allr for a in r["annotations"]]
    counts = {"records": dict(Counter(s for s, _ in allr)), "records_total": len(allr),
              "unique_image_response": len(recs), "duplicate_records_removed_by_dedup": len(allr) - len(recs),
              "spans_by_label": dict(Counter(a["label"] for _, a in ann)),
              "records_without_spans": sum(not r["annotations"] for _, r in allr),
              "span_text_mismatches": sum(r["response"][a["start"]:a["end"]] != a["text"] for r, a in ann),
              "distinct_prompts": len({r["question"] for _, r in allr})}
    agg = {"images_all": len(imgs), "images_analysis": len(keep), "images_excluded_no_instances": len(imgs) - len(keep),
           "records_after_dedup": len(recs), "records_analysis": len(ra),
           "records_analysis_by_split": dict(Counter(r["split"] for r in ra)),
           "records_per_image_analysis": {str(k): v for k, v in
                                          sorted(Counter(Counter(r["img"] for r in ra).values()).items())}}
    return ra, counts, agg, imgs


def lex_for(ids: list, sents: dict, inst: dict) -> dict:
    """Golds as score_g2b.coco_context builds them: the first 5 references through en_classes; the instance classes."""
    return {"refs": [[en(s) for s in sents[i][:5]] for i in ids], "complete": [set(inst[i]) for i in ids]}


def labels(rec: dict, ment: set) -> tuple[set, set]:
    """S_r, the classes of M_r an ACCURATE span names, and H_r, those an INACCURATE span names and no ACCURATE span does
    (ANALYSIS and UNSURE spans label nothing)."""
    named = {"ACCURATE": set(), "INACCURATE": set()}
    for a in rec["annotations"]:
        named.get(a["label"], set()).update(en(a["text"]))
    return ment & named["ACCURATE"], (ment & named["INACCURATE"]) - named["ACCURATE"]


def per_record(r: dict, fn, n: int, block: int = 2048) -> dict:
    """fn (score_g2b.scores or measures.condensed) with W = identity over records, in diagonal blocks: under W = I each
    record is scored alone, and one identity over every record would need about 1.6 GB."""
    out = [fn(r, np.arange(a, min(a + block, n)), np.eye(min(a + block, n) - a)) for a in range(0, n, block)]
    return {k: np.concatenate([o[k] for o in out]) for k in "PRF"}


def tau(x, y, w=None) -> float:
    if w is not None:  # a bootstrap replicate: each record repeated by its image's multiplicity
        x, y = np.repeat(x, w), np.repeat(y, w)
    return float(kendalltau(x, y, variant="b").statistic)


def draws(img: np.ndarray, cfg: dict) -> np.ndarray:
    """Per-record multiplicities of the registered image-cluster draws over the set's images in id order."""
    u = np.unique(img)
    W = np.random.default_rng(cfg["bootstrap_seed"]).multinomial(len(u), [1 / len(u)] * len(u), size=cfg["n_boot"])
    return W[:, np.searchsorted(u, img)]


def table(V: dict, hp, sel, W, keys) -> dict:
    """{key: (point, replicates)} of tau_b(V[key], HP) over the records `sel`; replicate b weights them by W[b]."""
    return {k: (tau(V[k][sel], hp[sel]), np.array([tau(V[k][sel], hp[sel], w) for w in W])) for k in keys}


def judge(T: dict, cfg: dict, verdicts: bool = True) -> dict:
    """The registered parts as paired differences over the shared draws; sign_gt_0 per part, then the compound rule."""
    out = {}
    for pid, parts in cfg["parts"].items():
        rows = [{"part": t, "point": T[tuple(a)][0] - T[tuple(b)][0],
                 "ci95": g.ci(T[tuple(a)][1] - T[tuple(b)][1], *cfg["ci"])} for t, (a, b) in parts.items()]
        for r in rows if verdicts else []:
            r["verdict"] = g.verdict(cfg["rules"][pid], r["point"], r["ci95"])
        out[pid] = {"parts": rows} | ({"verdict": g.compound([r["verdict"] for r in rows])} if verdicts else {})
    return out


def outcome(testable: bool, p1: str, p2: str) -> str:
    """The prereg outcome_rule, in its registered order."""
    return OUTCOMES[0 if not testable else 1 if p1 == "FAIL" else 2 if p1 == p2 == "PASS" else 3]


def analyse(recs: list, ids: list, lex: dict, cfg: dict, subsets: dict, data_path_ok: bool) -> dict:
    """Prereg sections 4-8 on parsed records and golds, then the descriptive tables of section 8."""
    n, pos = len(recs), {i: k for k, i in enumerate(ids)}
    ix, img = np.array([pos[r["img"]] for r in recs]), np.array([r["img"] for r in recs])
    var = g.gold_variants(lex, g.random_subsets([5] * len(ids), cfg["kmax"], cfg["n_rep"], cfg["subset_seed"]))
    negs, ment = m.negatives({"complete": lex["complete"]}, "coco80"), [en(r["response"]) for r in recs]
    S, H = map(list, zip(*(labels(r, x) for r, x in zip(recs, ment))))
    ns, nh, nm = (np.array([len(x) for x in X], float) for X in (S, H, ment))
    hp, V, ok = g.div(ns, ns + nh, np.nan), {}, {}
    for lv, key in cfg["levels"].items():
        gold = [[gs[k] for k in ix] for gs in var[key]]
        rows, jr = g.rows(ment, gold), m.judged_rows(ment, gold, [negs[k] for k in ix])
        a, c = per_record(rows, g.scores, n), per_record(jr, m.condensed, n)
        V |= {("P", lv): a["P"], ("R", lv): a["R"], ("F1", lv): a["F"]}
        if lv in ("complete", "union"):  # DESIGN D3: nothing is unjudged there, so cF1 = F1 (prereg cf1_at_complete)
            assert all(np.allclose(c[k], a[k], equal_nan=True) for k in "PRF"), lv
        else:
            V[("cF1", lv)], ok[f"gold_{lv}"], ok[f"j_{lv}"] = c["F"], rows["has"].all(0), (jr["j"] > 0).all(0)
    ok["labelled_mention"] = lab = ns + nh >= 1
    E = np.logical_and.reduce(list(ok.values()))  # gold and j > 0 at one_ref in every draw and at all_refs
    out = {"n": {"analysis_records": n, "E0_records": int(lab.sum()), "E_records": int(E.sum()),
                 "E_images": len(np.unique(ix[E]))}, "excluded_independent": {f"no_{k}": int((~v).sum())
                                                                               for k, v in ok.items()}}
    if not (out["n"]["E_records"] >= cfg["min_records"] and out["n"]["E_images"] >= cfg["min_images"]
            and data_path_ok):
        return out | {"outcome": outcome(False, "", "")}
    WE = draws(ix[E], cfg)
    T = table(V, hp, E, WE, list(V))
    pred, reg = judge(T, cfg), sorted({tuple(x) for p in cfg["parts"].values() for pr in p.values() for x in pr})
    sub = {f"split_{s}": E & (np.array([r["split"] for r in recs]) == s) for s in ("train", "val")}
    sub |= {f"overlap_{k}": E & np.isin(img, list(v)) for k, v in subsets.items()}
    e, mention = np.flatnonzero(E), {}
    for lv, key in cfg["levels"].items():  # mention level: a mention outside the gold is the metric's hallucination
        hit, fa = (np.mean([sum(len(X[r] - gs[ix[r]]) for r in e) for gs in var[key]]) / d[E].sum()
                   for X, d in ((H, nh), (S, ns)))
        mention[lv] = {"hit_rate": hit, "false_alarm_rate": fa, "youden_J": hit - fa}
    desc = {"tau_b": {f"{mu}@{lv}": [v[0], g.ci(v[1], *cfg["ci"])] for (mu, lv), v in T.items()},
            "mention_level": mention, "E0_sensitivity": judge(table(V, hp, lab, draws(ix[lab], cfg), reg), cfg, False),
            "subsets": {k: judge(table(V, hp, s, WE[:, s[E]], reg), cfg, False) | {"records": int(s.sum())}
                        for k, s in sub.items()},
            "mention_counts": {k: {"supported": int(ns[s].sum()), "hallucinated": int(nh[s].sum()),
                                   "unlabelled": int((nm - ns - nh)[s].sum())} for k, s in (("analysis", nm >= 0),
                                                                                             ("E", E))}}
    return out | {"outcome": outcome(True, pred["AN3-P1"]["verdict"], pred["AN3-P2"]["verdict"]),
                  "predictions": pred, "descriptive": desc}


def gate(P: dict, G: dict, cfg: dict, dl: str | None, coco_zip: str | None) -> dict:
    """Provenance of every input, then known values reproduced. Computes no A-N3 statistic: no HP, no tau."""
    def committed(pin: dict, want: str | None = None):
        return pinned(RENAMED[Path(pin["path"]).name], pin.get("sha256", want))

    raw, I, F = download(P, dl), P["golds"]["instance_classes"], P["golds"]["instance_classes"]["from"]
    inst = {int(k): v["coco"] for k, v in json.loads(pinned(I["path"], I["sha256"], head=False)).items()}
    pinned(I["derivation"], I["derivation_sha256"], head=False)
    pinned(F["path"], F["sha256"], head=False)
    zpath, zkey = F["zip_ref"].split(" :: ")
    if functools.reduce(dict.get, zkey.split("."), json.loads(pinned(zpath))) != F["official_zip_sha256"]:
        raise SystemExit("PROVENANCE FAIL: official_zip_sha256 differs from its zip_ref")
    if coco_zip:  # the official zip, and its member equal to the instances file the instance gold derives from
        with open(coco_zip, "rb") as f, zipfile.ZipFile(coco_zip) as z, \
                z.open("annotations/instances_val2014.json") as x:
            SEEN[Path(coco_zip).name], xs = (hashlib.file_digest(h, "sha256").hexdigest() for h in (f, x))
        if (SEEN[Path(coco_zip).name], xs) != (F["official_zip_sha256"], F["sha256"]):
            raise SystemExit("PROVENANCE FAIL: the COCO zip or its instances_val2014.json member differs from the pins")
    agg = json.loads(committed(P["analysis_set"]["aggregates"]))
    ids, excl = ([int(x) for x in committed(agg["id_lists"][k]).split()] for k in ["analysis", "excluded_no_instances"])
    cnt = json.loads(committed(P["data"]["counts_source"], COUNTS))
    ov = json.loads(committed(P["data"]["overlap_source"]))
    src, ova = ov["sources"], ov["mhaldetect"]["all"]
    pinned(src["karpathy"]["path"], src["karpathy"]["sha256"], head=False)
    cv = {int(x[-16:-4]) for x in pinned(src["cv295"]["path"], src["cv295"]["sha256"]).decode().split()[1::2]}
    c25 = {i["cocoid"] for i in json.loads(pinned(src["coco2500"]["path"], src["coco2500"]["sha256"]))["images"]}
    ig = "data/coco_probe/instance_gold.json"
    ref = json.loads(pinned(ig, {r["path"]: r["sha256"] for r in G["frozen_files"]["data"]}[ig]))
    recs, counts, mine, imgs = parse(raw, inst)
    kr, over, few = g.karpathy_refs(set(imgs)), [i for i in imgs if str(i) in ref], recs[:25]
    gold, ment = [[set(inst[r["img"]]) for r in few]], [en(r["response"]) for r in few]  # metric values only (CC-036)
    a = per_record(g.rows(ment, gold), g.scores, len(few))
    b = per_record(m.judged_rows(ment, gold, m.negatives({"complete": gold[0]}, "coco80")), m.condensed, len(few))
    checks = {  # name: (reproduced, known value from its pinned source)
        "release_counts": (counts, {k: v for k, v in cnt.items() if k != "_what"}),
        "analysis_set": (mine, {k: agg[k] for k in mine}),
        "id_lists_and_instance_gold_keys": ([[i for i in imgs if inst.get(i)], [i for i in imgs if not inst.get(i)],
                                             sorted(inst)] == [ids, excl, imgs], True),
        "overlap_and_refs": ([len(cv & set(imgs)), len(c25 & set(imgs)), sum(len(kr.get(i, [])) >= 5 for i in imgs)],
                             [ova["overlap"]["cv295"], ova["overlap"]["coco2500"], ova["karpathy_ge5_refs"]]),
        "data_path_check": ({"overlap_images": len(over), "mismatches": sum(inst[i] != ref[str(i)]["coco"]
                                                                            for i in over)}, cfg["data_path_check"]),
        "cf1_equals_f1_at_complete_first_25_records": (all(np.allclose(a[k], b[k], equal_nan=True) for k in "PRF"),
                                                       True)}
    res = {k: {"ok": x == y, "reproduced": x} for k, (x, y) in checks.items()}
    return {"checks": res, "all_pass": all(v["ok"] for v in res.values()), "recs": recs, "ids": ids,
            "lex": lex_for(ids, kr, inst), "subsets": {"cv295": cv, "coco2500": c25}}


def run(P: dict, G: dict, cfg: dict, gate_file: str, dl: str | None) -> dict:
    """The registered analysis, only from this scorer committed at HEAD with its committed all-PASS gate output."""
    pinned(HERE.relative_to(ROOT).as_posix())
    rel = Path(gate_file).resolve().relative_to(ROOT).as_posix()
    GT = json.loads(pinned(rel))
    if [GT["mode"], GT["all_pass"], GT["script_sha256"], GT["prereg"]["sha256"]] != \
            ["gate", True, sha(HERE.read_bytes()), PREREG[1]]:
        raise SystemExit("REFUSED: the gate file is not a committed all-PASS gate of this scorer")
    X = gate(P, G, cfg, dl, None)
    if not all(v["ok"] for k, v in X["checks"].items() if k != "data_path_check"):  # that one gives NOT_TESTABLE
        raise SystemExit("REFUSED: a self-check failed; no statistic is computed")
    return {"gate": {"path": rel, "sha256": SEEN[rel]}, "checks": X["checks"]} | analyse(
        X["recs"], X["ids"], X["lex"], cfg, X["subsets"], X["checks"]["data_path_check"]["ok"])


def selftest(cfg: dict) -> bool:
    """Toy cases with known answers; reads no data file."""
    rec = {"response": "A cat, a car, a clock, a bus and a hot dog.", "annotations": [
        {"label": "INACCURATE", "text": "A cat, a car"}, {"label": "ACCURATE", "text": "a car"},
        {"label": "ANALYSIS", "text": "a clock"}, {"label": "UNSURE", "text": "a bus"},
        {"label": "INACCURATE", "text": "dog"}, {"label": "ACCURATE", "text": "a hot dog"}]}
    assert labels(rec, en(rec["response"])) == ({"car", "hot dog"}, {"cat"})  # HP 2/3; clock, bus unlabelled
    assert abs(tau(np.array([1, 2, 2, 3]), np.array([1, 2, 3, 3])) - 0.8) < 1e-12  # C 4, D 0, a tie in x, one in y
    assert abs(tau(np.array([1, 2, 3]), np.array([1, 3, 2]), np.array([1, 1, 2])) - 0.2) < 1e-12  # C 3, D 2
    W = draws(np.array([0, 0, 2, 5]), cfg)  # 3 images; the first two records share one
    assert W.shape == (cfg["n_boot"], 4) and (W[:, 0] == W[:, 1]).all() and (W[:, 1:].sum(1) == 3).all()
    rng, U = np.random.default_rng(0), list("abcdefgh")
    ment = [set(rng.choice(U, rng.integers(1, 5), replace=False)) for _ in range(7)]
    gold = [[set(rng.choice(U, rng.integers(0, 4), replace=False)) for _ in range(7)] for _ in range(3)]
    neg = [set(U) - x for x in gold[0]]
    for fn, r in ((g.scores, g.rows(ment, gold)), (m.condensed, m.judged_rows(ment, gold, neg))):
        one = [fn({k: v[..., [i]] for k, v in r.items()}, np.arange(1), np.ones((1, 1))) for i in range(7)]
        assert all(np.allclose(per_record(r, fn, 7, 3)[k], [o[k][0] for o in one], equal_nan=True) for k in "PRF")
    assert m.selftest() == 0 and not g._check_rules() and set(SYN.values()) == m.U80 and len(m.U80) == 80
    assert [outcome(*c) for c in ((False, "PASS", "PASS"), (True, "FAIL", "PASS"), (True, "PASS", "PASS"),
                                  (True, "PASS", "INCONCLUSIVE"), (True, "INCONCLUSIVE", "PASS"))] == \
        ["NOT_TESTABLE", "NOT_SUPPORTED", "SUPPORTED", "MIXED", "MIXED"]
    try:
        pinned(PREREG[0], "0" * 64)
    except SystemExit as refused:
        assert "PROVENANCE FAIL" in str(refused)
        return True
    raise AssertionError("a wrong pin was accepted")


def dryrun(cfg: dict) -> dict:
    """SYNTHETIC: made-up images, references, instance classes, responses and span labels through parse and analyse."""
    rng, ids, raw = np.random.default_rng(7), list(range(1, 701)), {"train_raw.json": [], "val_raw.json": []}
    words = ("dog cat car bus horse sheep cow bird boat bench chair clock vase book cup bowl banana apple pizza cake "
             "kite truck train umbrella").split()
    inst = {i: [str(c) for c in rng.choice(words, rng.integers(2, 6), replace=False)] for i in ids} | {999: []}
    sents = {i: ["A photo of a " + " and a ".join(rng.choice(inst[i], rng.integers(1, 3), replace=False)) + "."
                 for _ in range(5)] for i in ids}
    for i in ids + [999]:  # image 999 has no instance class, so its records leave the analysis set
        for k in range(3):
            t = list(rng.choice(inst[i], min(len(inst[i]), rng.integers(1, 4)), replace=False))
            f = list(rng.choice([w for w in words if w not in inst[i]], rng.integers(0, 3), replace=False))
            text, ann = "", []
            for c in rng.permutation(t + f).tolist() + [None]:  # 15% of the labels are drawn at random
                s = f"There is a {c}. " if c else f"Shot {k} looks calm."
                lab = str(rng.choice(["ACCURATE", "INACCURATE", "UNSURE", "ANALYSIS"])) if c and rng.random() < 0.15 \
                    else "ACCURATE" if c in t else "INACCURATE" if c else "ANALYSIS"
                ann.append({"label": lab, "start": len(text), "end": len(text) + len(s), "text": s})
                text += s
            raw[("train", "train", "val")[k] + "_raw.json"].append(
                {"image": f"COCO_val2014_{i:012d}.jpg", "question": "Describe.", "response": text, "annotations": ann})
    raw["val_raw.json"].append(raw["train_raw.json"][0])  # a repeated (image, response): the dedup removes it
    recs, counts, agg, imgs = parse({k: json.dumps(v).encode() for k, v in raw.items()}, inst)
    ida = [i for i in imgs if inst[i]]
    lex, sub = lex_for(ida, sents, inst), {"cv295": set(ids[:30]), "coco2500": set(ids[30:200])}
    out = analyse(recs, ida, lex, cfg, sub, True)
    assert [counts["duplicate_records_removed_by_dedup"], counts["span_text_mismatches"],
            agg["images_excluded_no_instances"], agg["records_analysis"]] == [1, 0, 1, 3 * len(ids)]
    assert out["predictions"]["AN3-P1"]["verdict"] == "PASS" and out["outcome"] in OUTCOMES  # the signal is built in
    assert all(p["ci95"] for v in out["predictions"].values() for p in v["parts"])
    assert out["n"]["E0_records"] >= out["n"]["E_records"] >= cfg["min_records"]
    assert analyse(recs[:60], ida, lex, cfg, sub, True)["outcome"] == "NOT_TESTABLE" == \
        analyse(recs, ida, lex, cfg, sub, False)["outcome"]  # too few records; data-path check failed
    return {"SYNTHETIC": "made-up images, references, instance classes, responses and span labels; no M-HalDetect "
                         "file, COCO file or ID list is read; HP tracks true precision with 15% label noise",
            "release_counts_synthetic": counts, "analysis_set_synthetic": agg} | out


def main() -> int:
    global m, g, sc, SYN
    ap = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    ap.add_argument("mode", choices=("gate", "dryrun", "run"))
    ap.add_argument("out")
    ap.add_argument("--gate", help="run: the committed output of gate")
    ap.add_argument("--coco-zip", help="gate: the official COCO-2014 annotations zip (its pin and member)")
    ap.add_argument("--dl", help="the M-HalDetect copy (default: the prereg's licence_handling.download)")
    a = ap.parse_args()
    if Path(a.out).exists() or (a.mode == "gate" and not a.coco_zip) or (a.mode == "run" and not a.gate):
        raise SystemExit("REFUSED: OUT exists (never overwritten), gate lacks --coco-zip or run lacks --gate")
    P, G = json.loads(pinned(*PREREG)), json.loads(pinned(*G2B))
    cfg, (m, g, sc) = config(P, G), modules(P)
    SYN = sc.load_synonyms()
    head = {"id": P["prereg_id"], "mode": a.mode, "prereg": dict(zip(("path", "sha256"), PREREG)),
            "script_sha256": sha(HERE.read_bytes()), "config": cfg, "toy_selftest_pass": selftest(cfg)}
    if a.mode == "gate":
        X = gate(P, G, cfg, a.dl, a.coco_zip)
        body = {"checks": X["checks"], "all_pass": X["all_pass"], "a_n3_statistics_computed": False}
    else:
        body = dryrun(cfg) if a.mode == "dryrun" else run(P, G, cfg, a.gate, a.dl)
    with open(a.out, "x", encoding="utf-8") as f:  # "x": an existing output is never overwritten
        json.dump(head | body | {"inputs_sha256": SEEN}, f, indent=1, default=lambda o: o.item())
    print(json.dumps({k: body[k] for k in ("all_pass", "outcome", "n") if k in body}
                     | {k: v["ok"] for k, v in body.get("checks", {}).items()}))
    return 0 if body.get("all_pass", True) else 1


if __name__ == "__main__":
    sys.exit(main())
