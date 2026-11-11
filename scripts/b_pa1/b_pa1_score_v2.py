#!/usr/bin/env python3
"""B-PA1-T1 laptop scorer v2: v3.1 §3 dev contacts and §6.4 steps 6-8. TIER 1 / DEV-EXPLORE (B-PA1-T1).
DRAFT for the CC-316 round-2 read, never run on real inputs. v2 = b_pa1_score.py c712899d plus the CC-316 change list
V1-V7 and the rules of AMENDMENT_T1_SCORING_RULES_v1.md ("the amendment"). Laptop only; stdlib + repo. Two R2 venvs,
both python 3.12.3 with -I:
PN = ~/.venvs/c_stage1_lists/bin/python (numpy 2.5.4, scipy 1.18.1, freeze 1a639a50, LOG l.938) for steps 7-8 and the
selftest; PJ = ~/.venvs/b_pa1_ijson/bin/python (ijson 3.6.0, freeze dffafd50, LOG l.1201) for step 6.

    PN -I -B scripts/b_pa1/b_pa1_score_v2.py selftest    synthetic fixtures only (fixture(), seed 20261110)
    PN -I -B ... contacts --pulled P --lists L --out-dir C      §3: b_pa1_dev_contacts.json, ids only
    PJ -I -B ... join --pulled P --lists L --map M --ann A --out-dir D
        step 6, the only reader of annotations[]: per caption, each matched map term with its Objects365 rows
        (id, tag, class has a box in the image). Raw: no precision is formed here
    PN -I -B ... thresholds --pulled P --join D          step 7, baselines only: judge prompt, SE_A,
        SESOI, NI -> D/T1_THRESHOLDS.json (O_EXCL, never rewritten). Opens no decomposition or verification file
    PN -I -B ... tau --pulled P --join D --map M         step 8: refuses unless the sha of
        D/T1_THRESHOLDS.json is on a LOG pin line. Lever, planning numbers, PA3 effect trigger -> D/T1_RESULT.json

P = the final pull of ~/b_pa1_out; every file is read through SHA256SUMS_rest, whose sha must be on a LOG pin line.
D, C = directories outside the tracked tree. stdout carries ids-free counts, shas and statistics only.

Rules of the amendment, by section:
  §1 gold_of: a mention = one matched map term with a row in the tag set; correct iff ANY of those rows has a box.
  §2 Mapper: an object proposition is mapped iff the gold matcher, run on its `object` string, returns such a term.
  §3 undefined values: a null baseline score or an undefined tau at step 7 stops before any B output is opened; at
     step 8 an undefined replicate ranks below every defined one, and an undefined point delta fires the PA3 trigger.
  §4 planning P(PASS) at tier 1 (§8.6): NOT COMPUTED, a recorded deviation.
  §7 conventions (CONV), written into both output files; the p form of §8.3 governs.
Not written here (amendment §5): partial tau, count-matched, COCO-80 restriction, system-level tau, T1_CONFIG.json.
"""
from __future__ import annotations

import argparse
import contextlib
import io
import json
import math
import os
import subprocess
import sys
from pathlib import Path

HERE = Path(__file__).resolve().parent
sys.path[:0] = [str(HERE), str(HERE.parent)]
import b_pa1 as B  # noqa: E402  LABEL, LOG, ANN_NAME, pin_line, write_new, must_refuse
import b_pa1_mid as M  # noqa: E402  norm, outside_tree, sha, FINAL_NAME, G.scratch
import map_v1 as MV  # noqa: E402  canon, exists_error
import score_coco_probe as sc  # noqa: E402  vi_objects (matcher v2 procedure, as parity run 2's new-map side)

try:
    import numpy as np  # steps 7-8; the ijson venv of step 6 has neither
    import scipy.stats  # v3.1 l.431: scipy.stats.kendalltau, scipy pinned in the PN freeze
except ImportError:
    np = None

VENV_J = Path.home() / ".venvs/b_pa1_ijson/bin/python"  # as mutants.VENV_J

PINS = {"ann": "413b172b6a5fa075eab105cc4b0754de995812823242e988adc14e1380742b22",  # LOG l.1224 (R6)
        "map": "866b5cb7577d36cbc87aefd895faabcdaadd1ef0544abbc54043a29c537191cc",  # LOG l.1992 (final map)
        "lists": "64f20a1f8722eb36f1b2c730761ef26ae5bc76f1c448fe8c60f70534335dc8b7"}  # LOG l.1965
SUMS, WALK = "SHA256SUMS_rest", "out/s/walk.jsonl"
GOLD_NAME, JOIN_NAME, TH_NAME, RES_NAME = "gold_join.jsonl", "JOIN.json", "T1_THRESHOLDS.json", "T1_RESULT.json"
CONTACTS_NAME = "b_pa1_dev_contacts.json"
N_SLICE, N_BOOT, SEED = 2000, 10_000, 20261101  # §5.2; §8.2
NI, SESOI_FLOOR, TIE = 0.02, 0.02, 0.005  # §8.5; §7.1, §7.2
TAGS, DICT = frozenset({"dictionary", "instrument"}), frozenset({"dictionary"})  # §6.2
JUDGES = {"ja": ("out/a1score/ja.jsonl", "p_yes"), "jb": ("out/rest/jb.jsonl", "ev"),
          "jc": ("out/rest/jc.jsonl", "ev")}  # §7.1 tie order J-a, J-b, (J-c)
CLIP = ("out/a1score/clip.jsonl", "score")
CFGS = {"d1v1": ("out/a1score/decomp_d1.jsonl", "out/a1score/verify_d1v1.jsonl"),  # §7.2 tie order
        "d2v1": ("out/rest/decomp_d2.jsonl", "out/rest/verify_d2v1.jsonl"),
        "d1v2": ("out/a1score/decomp_d1.jsonl", "out/rest/verify_d1v2.jsonl")}
CODE = B.K.sha_file(Path(__file__))
IMPORTS = {m.__name__: B.K.sha_file(Path(m.__file__)) for m in (sc, B, M, MV)}  # CC-316 V6: recorded at step 6
AMEND = "AMENDMENT_T1_SCORING_RULES_v1.md"  # by name only: the amendment pins this file's sha, not the reverse
P_PASS = f"NOT COMPUTED at tier 1 (recorded deviation from v3.1 l.476; {AMEND} §4)"
UNDEF7 = "an undefined {} at step 7 (amendment §3: stop before any B output is opened; to a judge)"
CONV = {  # amendment §7 (CC-316 Q7, V4): written into T1_THRESHOLDS.json and T1_RESULT.json
    "tau": 'scipy.stats.kendalltau(x, y, variant="c"); tau_b: variant="b"; ties kept',
    "percentile": "numpy.percentile, linear interpolation", "sd": "numpy.std, ddof 0",
    "generator": "one numpy.random.default_rng(seed) per bootstrap call; one integers(0, n, n) draw per resample, "
                 "shared by every statistic of the call",
    "resampling_unit": "the images of the caption set of the call (gold-defined set for SE_A, analysis set at step "
                       "8), ascending id; all captions of a drawn image move together",
    "tie": "within 0.005 inclusive: tau >= best - 0.005", "pass": "p <= alpha; the p form of §8.3 governs",
    "undefined_replicate": "ranks below every defined replicate: counted as <= SESOI and <= -NI; a bound that falls "
                           "on one is null and its comparison fails"}


def refuse(msg: str):
    raise SystemExit(f"REFUSED: {msg}")


def strict(o):
    """An undefined number (nan, +-inf) becomes null, so every output file is strict JSON (amendment §3)."""
    if isinstance(o, dict):
        return {k: strict(v) for k, v in o.items()}
    if isinstance(o, list):
        return [strict(v) for v in o]
    return None if isinstance(o, float) and not math.isfinite(o) else o


def terms_of(mp: dict) -> list[tuple[str, str]]:
    """The matcher's term list (amendment §1(e), §2): every map term in file order, as parity run 2's new-map side.
    sc.vi_objects defaults to lexicon v2; RESCAP_RAW_TONE would change its tone form, so it must be unset (R3)."""
    if "RESCAP_RAW_TONE" in os.environ:
        refuse("RESCAP_RAW_TONE is set (R3 pin: unset)")
    return [(t["vi"], t["vi"]) for t in mp["terms"]]


# ---------------------------------------------------------------------------------------------- pinned inputs
class Pulled:
    """The final pull. SHA256SUMS_rest must be on a LOG pin line; every file is checked against it when read."""

    def __init__(self, p: Path, log: Path):
        b = (p / SUMS).read_bytes()
        self.p, self.sha = p, M.sha(b)
        if not B.pin_line(log, self.sha, SUMS):
            refuse(f"the {SUMS} sha is not on a LOG pin line")
        self.sums = dict((ln[66:], ln[:64]) for ln in b.decode().splitlines())

    def read(self, rel: str) -> bytes:
        b = (self.p / rel).read_bytes()
        if self.sums.get(rel) != M.sha(b):
            refuse(f"{rel} differs from {SUMS}")
        return b

    def rows(self, rel: str) -> list[dict]:
        return [json.loads(x) for x in self.read(rel).decode().splitlines()]

    def keyed(self, rel: str) -> dict[tuple, dict]:
        rows = self.rows(rel)
        d = {(r["cap"], r["id"]): r for r in rows}
        if len(d) != len(rows):
            refuse(f"{rel} repeats a (captioner, id) row")
        return d

    def accepted(self) -> list[str]:
        acc = json.loads(self.read("out/s/ACCEPT.json"))["accepted"]
        if len(acc) != 4 or len(set(acc)) != 4:
            refuse("ACCEPT.json does not name 4 captioners")
        return acc


def pinned(p: Path, pin: str) -> bytes:
    b = p.read_bytes()
    if M.sha(b) != pin:
        refuse(f"{p.name} differs from its pin {pin[:8]}")
    return b


def slice_a(lists: Path, pins: dict, n: int) -> list[int]:
    ids = json.loads(pinned(lists, pins["lists"]))["slice_a"]
    if len(ids) != n or len(set(ids)) != n:
        refuse(f"slice A is not {n} distinct ids")
    return ids


def out_dir(d: Path) -> Path:
    d = M.outside_tree(d)
    d.mkdir(parents=True, exist_ok=True)
    return d


def emit(p: Path, doc: dict) -> bytes:
    """Write once (O_EXCL), then print the same bytes."""
    b = MV.canon(strict(doc))
    B.write_new(p, b)
    sys.stdout.write(b.decode() + "\n")
    return b


def pin_lines(log: Path, name: str) -> int:
    """How many LOG pin lines (B.PIN_RE) name the file as a delimited token (CC-316 V6)."""
    tok = B.delimited(name)
    return sum(bool(B.PIN_RE.search(ln) and tok.search(ln)) for ln in log.read_text(encoding="utf-8").splitlines())


# ---------------------------------------------------------------------------------------------- §3 dev contacts
def cmd_contacts(a, log: Path = B.LOG, pins: dict = PINS, n: int = N_SLICE) -> int:
    """v3.1 l.143-144: every image id B decoded or scored on the host = the `id` of every row of every out/ jsonl of
    the pull (gate, A1, A2, A3, H, A4). Ids only. A1 decodes every slice-A image, so the ids must be slice A exactly
    (CC-316 V6: a short manifest would otherwise write a short contacts file with rc 0)."""
    out, P = out_dir(a.out_dir), Pulled(a.pulled, log)
    ids = set()
    for rel in sorted(P.sums):
        if rel.startswith("out/") and rel.endswith(".jsonl") and rel != WALK:
            got = [r.get("id") for r in P.rows(rel)]
            if any(type(i) is not int for i in got):
                refuse(f"{rel} has a row without an int id")
            ids.update(got)
    if ids != set(slice_a(a.lists, pins, n)):
        refuse("the contacted ids are not exactly slice A")
    b = MV.canon({"schema": "vsps.b_pa1.dev_contacts.v1", "tier": B.LABEL, "set": "objects365_v2_train",
                  "ids": sorted(ids), "sums_rest_sha256": P.sha, "lists_sha256": pins["lists"], "code_sha256": CODE})
    B.write_new(out / CONTACTS_NAME, b)
    print(json.dumps({"tier": B.LABEL, "n_ids": len(ids), "sha256": M.sha(b)}))
    return 0


# ---------------------------------------------------------------------------------------------- step 6: gold join
def gold_classes(fh, ids: set[int]) -> dict[int, set[int]]:
    """The only read of annotations[] (v3.1 l.374): the category ids that have a box in each slice-A image. Every
    annotation record counts as a box (the registered text names no iscrowd rule outside count propositions)."""
    import ijson  # R2 venv, as b_pa1.frame_of

    gold = {i: set() for i in ids}
    for x in ijson.items(fh, "annotations.item"):
        if x["image_id"] in gold:
            gold[x["image_id"]].add(x["category_id"])
    return gold


def cmd_join(a, log: Path = B.LOG, pins: dict = PINS, n: int = N_SLICE) -> int:
    out, P = out_dir(a.out_dir), Pulled(a.pulled, log)
    acc, ids = P.accepted(), slice_a(a.lists, pins, n)
    mp = json.loads(pinned(a.map, pins["map"]))
    caps = {}
    for k in acc:
        caps.update(P.keyed(f"out/a1decode/captions_{k}.jsonl"))
    if set(caps) != {(k, i) for k in acc for i in ids}:
        refuse("the A1 captions are not one per accepted captioner and slice-A id")
    if a.ann.name != B.ANN_NAME or B.K.sha_file(a.ann) != pins["ann"]:
        refuse("not the R6-pinned train annotation file")
    terms = terms_of(mp)
    tgt: dict[str, list] = {}
    for r in mp["rows"]:
        tgt.setdefault(r["vi"], []).append((r["o365_id"], r["tag"]))
    with open(a.ann, "rb") as fh:
        gold = gold_classes(fh, set(ids))
    lines, unmapped = [], 0
    for key in sorted(caps):
        hit = sorted(sc.vi_objects(caps[key]["caption"], terms))
        unmapped += sum(v not in tgt for v in hit)
        lines.append(json.dumps({"cap": key[0], "id": key[1], "terms": [
            [[c, tag, int(c in gold[key[1]])] for c, tag in tgt[v]] for v in hit if v in tgt]}, sort_keys=True))
    gb = ("\n".join(lines) + "\n").encode()
    B.write_new(out / GOLD_NAME, gb)
    emit(out / JOIN_NAME, {"schema": "vsps.b_pa1.gold_join.v2", "tier": B.LABEL, "gold_join_sha256": M.sha(gb),
                           "ann_sha256": pins["ann"], "map_sha256": pins["map"], "lists_sha256": pins["lists"],
                           "sums_rest_sha256": P.sha, "code_sha256": CODE, "imports_sha256": IMPORTS,
                           "accepted": acc, "n_captions": len(lines),
                           "images_without_box": sum(not g for g in gold.values()),
                           "term_hits_without_o365_row": unmapped})
    return 0


def load_join(d: Path, P: Pulled, pins: dict) -> tuple[dict[tuple, list], dict]:
    meta, gb = json.loads((d / JOIN_NAME).read_bytes()), (d / GOLD_NAME).read_bytes()
    if (meta["gold_join_sha256"], meta["sums_rest_sha256"], meta["map_sha256"], meta["code_sha256"]) != \
            (M.sha(gb), P.sha, pins["map"], CODE):
        refuse("the gold join is not of this pull, this final map and this scorer")
    if meta["imports_sha256"] != IMPORTS:  # CC-316 V6
        refuse("an imported module differs from the one that made the gold join")
    return {(r["cap"], r["id"]): r["terms"] for r in map(json.loads, gb.decode().splitlines())}, meta


def gold_of(terms: list, tags: frozenset = TAGS) -> float | None:
    """Gold object precision of one caption (v3.1 l.91-93, §7.3; amendment §1); None = no mention. A mention = one
    matched map term with at least one row tagged in `tags`; it is correct iff ANY of those rows' classes has a box.
    Two terms of one class are two mentions; a term's rows outside `tags` are ignored."""
    hits = [any(x[2] for x in t if x[1] in tags) for t in terms if any(x[1] in tags for x in t)]
    return sum(hits) / len(hits) if hits else None


def mention_counts(J: dict, tags: frozenset = TAGS) -> dict:
    """CC-316 W11, counts only: mentions (amendment §1), those with several in-set rows, and those that share a class
    with another mention of the same caption."""
    n = multi = share = 0
    for terms in J.values():
        ts = [c for t in terms if (c := {x[0] for x in t if x[1] in tags})]
        n, multi = n + len(ts), multi + sum(len(c) > 1 for c in ts)
        share += sum(any(c & u for j, u in enumerate(ts) if j != i) for i, c in enumerate(ts))
    return {"n": n, "with_several_rows": multi, "sharing_a_class": share}


# ---------------------------------------------------------------------------------------------- B's score (§7.1)
class Mapper:
    """Is an object proposition mapped (v3.1 l.92; amendment §2)? The gold matcher, with the same terms in the same
    order, is run on the proposition's `object` string: mapped iff it returns at least one term with a row tagged in
    `tags`. An empty string returns no term; several terms still make one mapped proposition."""

    def __init__(self, mp: dict):
        self.terms = terms_of(mp)
        self.tags: dict[str, set] = {}
        for r in mp["rows"]:
            self.tags.setdefault(r["vi"], set()).add(r["tag"])
        self.seen: dict[str, set] = {}

    def __call__(self, obj: str, tags: frozenset) -> bool:
        if obj not in self.seen:
            self.seen[obj] = set().union(*(self.tags.get(v, ()) for v in sc.vi_objects(obj, self.terms)))
        return bool(self.seen[obj] & tags)


def b_counts(d: dict, v: dict, mapped: Mapper, tags: frozenset) -> tuple[int, int, int, int, int]:
    """(yes, answered, abstained) over mapped object propositions, then (yes, answered) over all object propositions
    (§8.7). Yes iff p_yes >= 0.5; an abstained proposition is in neither count (§7.1)."""
    yes = n = ab = yes_o = n_o = 0
    seen = {x["k"] for x in v["props"]}
    if len(seen) != len(v["props"]) or not seen <= set(range(len(d["props"]))) or \
            any(p["type"] == "object" and k not in seen for k, p in enumerate(d["props"])):
        refuse("a verification row does not answer each object proposition of its decomposition once")
    for x in v["props"]:
        p = d["props"][x["k"]]
        if p["type"] != "object":
            continue
        m = mapped(p["object"], tags)
        if x["abstain"]:
            ab += m
            continue
        if x["p_yes"] is None:
            refuse("an answered proposition has no yes-probability")
        y = x["p_yes"] >= 0.5
        yes, n, yes_o, n_o = yes + (y and m), n + m, yes_o + y, n_o + 1
    return yes, n, ab, yes_o, n_o


def b_score(c: tuple, kind: str = "b") -> float | None:
    """b: §7.1 primary (abstains removed). open: §8.7. wrong: abstain-as-wrong sensitivity (§7.1)."""
    num, den = {"b": (c[0], c[1]), "open": (c[3], c[4]), "wrong": (c[0], c[1] + c[2])}[kind]
    return num / den if den else None


def configs(P: Pulled, keys: set) -> dict[str, tuple[dict, dict]]:
    """(d1,v1) always; A3's two configurations only if both are complete, else A3 is NOT RUN (§7.2 l.410-411)."""
    got = {}
    for c, rels in CFGS.items():
        if all(r in P.sums for r in rels):
            d, v = (P.keyed(r) for r in rels)
            if set(d) == keys and set(v) == keys:
                got[c] = (d, v)
    if "d1v1" not in got:
        refuse("the (d1,v1) decomposition or verification is incomplete")
    return got if len(got) == len(CFGS) else {"d1v1": got["d1v1"]}


# ---------------------------------------------------------------------------------------------- statistics (§8)
def tau_c(x, y, variant: str = "c") -> float:
    """v3.1 l.431: scipy.stats.kendalltau(x, y, variant="c"), ties kept; variant "b" is the tau_b sensitivity. nan =
    undefined (a constant column, or fewer than two captions); the amendment's §3 says what follows from it."""
    return float(scipy.stats.kendalltau(x, y, variant=variant).statistic)


def boot(image_ids: list[int], stats: list[tuple], nb: int):
    """§8.2: image-cluster bootstrap, nb = N_BOOT resamples of the images with replacement (captions of an image move
    together), numpy.random.default_rng(SEED), one generator per call and one draw per resample for every (x, y) of
    `stats`. Returns tau_c (scipy, on the expanded resample) per resample and statistic; nan = undefined. Only the
    selftest lowers `nb` (as it lowers `n` in cmd_join): the scipy call is several times slower than v1's numpy form."""
    ids = sorted(set(image_ids))
    img, n = np.searchsorted(ids, image_ids), len(ids)
    rng, out = np.random.default_rng(SEED), np.empty((nb, len(stats)))
    cols = [(np.asarray(x, float), np.asarray(y, float)) for x, y in stats]
    for i in range(nb):
        rows = np.repeat(np.arange(len(img)), np.bincount(rng.integers(0, n, n), minlength=n)[img])
        out[i] = [tau_c(x[rows], y[rows]) for x, y in cols]
    return out


def deltas(a, b):
    """Bootstrap deltas a* - b*. An undefined replicate ranks below every defined one (amendment §3), so it counts
    as <= SESOI and as <= -NI."""
    d = a - b
    return np.where(np.isnan(d), -np.inf, d)


def bound(d, alpha: float) -> float:
    """One-sided lower bound at level 1 - alpha: the 100 alpha percentile, linear interpolation (amendment §7). Not
    finite when it falls on an undefined replicate; every comparison with it is then false."""
    with np.errstate(invalid="ignore"):
        return float(np.percentile(d, 100 * alpha))


def pick(taus: dict[str, float], order) -> str:
    """Highest tau_c; any candidate within TIE of the best yields to the earlier one in `order` (§7.1, §7.2)."""
    best = max(taus.values())
    return next(k for k in order if taus[k] >= best - TIE)


def sesoi_of(se_a: float) -> float:
    return max(SESOI_FLOOR, 2 * se_a)  # §8.5


def holm(d: dict, sesoi: float, h1a: bool) -> dict:
    """§8.3: after the H1a gate, Holm over the hypotheses of d (name -> bootstrap deltas): p = (1 + #{d* <= SESOI}) /
    (B + 1), counted as #{not d* > SESOI}; the smaller p at 0.025, the other at 0.05 only if the first passed. The p
    form governs (amendment §7); the CI lower bound at the Holm level is printed with `forms_agree`."""
    p = {h: (1 + int((~(x > sesoi)).sum())) / (len(x) + 1) for h, x in d.items()}  # len(x) = B, the resamples
    ok, out = h1a, {}
    for step, h in enumerate(sorted(p, key=p.get)):
        alpha = (0.025, 0.05)[step]
        lb = bound(d[h], alpha)
        ok = bool(ok and p[h] <= alpha)
        out[h] = {"step": step + 1, "p": p[h], "alpha": alpha, "lower_bound": lb, "one_sided_level": 1 - alpha,
                  "pass": ok, "forms_agree": (p[h] <= alpha) == (lb > sesoi)}
    return out


def baselines(P: Pulled, keys: list) -> dict[str, dict]:
    """Judge and CLIPScore values per caption (§7.1). No decomposition or verification file is opened. A null value
    stops here (amendment §3): step 7 calls this first, before any B output is opened; to a judge."""
    out = {}
    for name, (rel, field) in {**JUDGES, "clip": CLIP}.items():
        rows = P.keyed(rel)
        if set(rows) != set(keys):
            refuse(f"{rel} is not one row per A1 caption")
        out[name] = {k: rows[k][field] for k in keys}
        if any(v is None for v in out[name].values()):
            refuse(f"{rel} has an undefined score (amendment §3: stop at step 7; to a judge)")
    return out


# ---------------------------------------------------------------------------------------------- step 7
def cmd_thresholds(a, log: Path = B.LOG, pins: dict = PINS, nb: int = N_BOOT) -> int:
    P = Pulled(a.pulled, log)
    J, meta = load_join(a.join, P, pins)
    gold = {k: g for k in sorted(J) if (g := gold_of(J[k])) is not None}  # the gold-defined set (§7.1, §8.5)
    G, y = list(gold), list(gold.values())
    base = baselines(P, sorted(J))
    t = {m: tau_c([base[m][k] for k in G], y) for m in base}
    if any(v != v for v in t.values()):
        refuse(UNDEF7.format("tau"))
    judge = pick({j: t[j] for j in JUDGES}, JUDGES)
    reps = boot([k[1] for k in G], [([base[judge][k] for k in G], y)], nb)
    if np.isnan(reps).any():  # never into SE_A: max(0.02, nan) would silently give the floor
        refuse(UNDEF7.format("SE_A replicate"))
    se_a = float(reps.std())
    emit(a.join / TH_NAME, {
        "schema": "vsps.b_pa1.t1_thresholds.v2", "tier": B.LABEL, "sesoi": sesoi_of(se_a), "ni": NI,
        "final_map_sha256": pins["map"], "judge_prompt": judge, "se_a": se_a, "tau_c": t,
        "spread_judge_clip": abs(t[judge] - t["clip"]), "n_captions": len(G), "n_images": len({k[1] for k in G}),
        "n_boot": nb, "seed": SEED, "numpy": np.__version__, "scipy": scipy.__version__, "conventions": CONV,
        "amendment": AMEND, "gold_join_sha256": meta["gold_join_sha256"], "sums_rest_sha256": P.sha,
        "code_sha256": CODE})
    return 0


# ---------------------------------------------------------------------------------------------- step 8
def cmd_tau(a, log: Path = B.LOG, pins: dict = PINS, nb: int = N_BOOT) -> int:  # noqa: C901  one linear pass
    tb = (a.join / TH_NAME).read_bytes()
    if not B.pin_line(log, M.sha(tb), TH_NAME):  # §6.4: before any B output is opened
        refuse(f"the {TH_NAME} sha is not on a LOG pin line (v3.1 §6.4 steps 7-8)")
    if pin_lines(log, TH_NAME) != 1:  # CC-316 V6: written once, pinned once
        refuse(f"LOG holds more than one {TH_NAME} pin line")
    th, P = json.loads(tb), Pulled(a.pulled, log)
    J, meta = load_join(a.join, P, pins)
    if (th["final_map_sha256"], th["gold_join_sha256"], th["code_sha256"]) != \
            (pins["map"], meta["gold_join_sha256"], CODE):
        refuse(f"{TH_NAME} is not of this final map, gold join and scorer")
    keys, sesoi, judge = sorted(J), th["sesoi"], th["judge_prompt"]
    mapped = Mapper(json.loads(pinned(a.map, pins["map"])))
    base, cfgs = baselines(P, keys), configs(P, set(keys))
    gold = {k: g for k in keys if (g := gold_of(J[k])) is not None}
    G, yG = list(gold), list(gold.values())
    cnt = {c: {k: b_counts(d[k], v[k], mapped, TAGS) for k in keys} for c, (d, v) in cfgs.items()}

    def imputed(c):  # §7.2: B's score 0.5 where undefined, on the gold-defined set
        return [0.5 if (s := b_score(cnt[c][k])) is None else s for k in G]

    lever = {c: tau_c(imputed(c), yG) for c in cfgs}
    head = {"schema": "vsps.b_pa1.t1_result.v2", "tier": B.LABEL, "thresholds_sha256": M.sha(tb), "sesoi": sesoi,
            "ni": NI, "judge_prompt": judge, "a3": "RUN" if len(cfgs) > 1 else "NOT RUN", "lever_tau_c": lever,
            "n_boot": nb, "seed": SEED, "p_pass_planning": P_PASS, "mentions": mention_counts(J),
            "conventions": CONV, "amendment": AMEND, "numpy": np.__version__, "scipy": scipy.__version__,
            "code_sha256": CODE}
    if any(v != v for v in lever.values()):  # amendment §3: an undefined lever tau of B. No configuration is selected
        emit(a.join / RES_NAME, {**head, "config": None, "h1a": {"lower_bound_95": None, "pass": False},
                                 "holm": {h: {"pass": False} for h in ("H1b", "H1c")}, "pa3_effect_trigger": True})
        return 0
    cfg = pick(lever, [c for c in CFGS if c in cfgs])
    A = [k for k in G if b_score(cnt[cfg][k]) is not None]  # §7.3 primary analysis set
    y = [gold[k] for k in A]
    xs = {"b": [b_score(cnt[cfg][k]) for k in A], "judge": [base[judge][k] for k in A],
          "clip": [base["clip"][k] for k in A], "open": [b_score(cnt[cfg][k], "open") for k in A]}
    pt = {m: tau_c(x, y) for m, x in xs.items()}
    bs = boot([k[1] for k in A], [(x, y) for x in xs.values()], nb)
    star = {"H1b": deltas(bs[:, 0], bs[:, 1]), "H1c": deltas(bs[:, 0], bs[:, 2])}
    d_judge, lb95 = pt["b"] - pt["judge"], bound(star["H1b"], 0.05)
    h1a = lb95 > -NI  # §8.3 gate; false when the bound is undefined

    W = [k for k in G if b_score(cnt[cfg][k], "wrong") is not None]  # abstain-as-wrong (§7.1)
    dcnt = {k: b_counts(*(x[k] for x in cfgs[cfg]), mapped, DICT) for k in keys}  # §6.2 dictionary-only map
    dA = [k for k in keys if gold_of(J[k], DICT) is not None and b_score(dcnt[k]) is not None]
    dy = [gold_of(J[k], DICT) for k in dA]
    dxs = [[b_score(dcnt[k]) for k in dA], [base[judge][k] for k in dA], [base["clip"][k] for k in dA]]
    dpt, dbs = [tau_c(x, dy) for x in dxs], boot([k[1] for k in dA], [(x, dy) for x in dxs], nb)
    acc = meta["accepted"]
    emit(a.join / RES_NAME, {
        **head, "config": cfg, "n_captions": len(A), "n_images": len({k[1] for k in A}),
        "tau_c": pt, "tau_b": {m: tau_c(x, y, "b") for m, x in xs.items()},
        "delta_judge": d_judge, "delta_clip": pt["b"] - pt["clip"],
        "h1a": {"lower_bound_95": lb95, "pass": h1a}, "holm": holm(star, sesoi, h1a),
        "undefined_replicates": {h: int(np.isinf(x).sum()) for h, x in star.items()},
        "pa3_effect_trigger": not d_judge >= sesoi,  # §11: point delta < SESOI; an undefined delta fires it
        "open_sensitivity": {"delta_judge": pt["open"] - pt["judge"],  # §8.7, no verdict
                             "lower_bound_975": bound(deltas(bs[:, 3], bs[:, 1]), 0.025)},
        "imputed_sensitivity": {"n_captions": len(G), "delta_judge":
                                lever[cfg] - tau_c([base[judge][k] for k in G], yG)},  # §7.3 N2
        "abstain_as_wrong": {"n_captions": len(W), "delta_judge":
                             tau_c([b_score(cnt[cfg][k], "wrong") for k in W], [gold[k] for k in W])
                             - tau_c([base[judge][k] for k in W], [gold[k] for k in W])},
        "dictionary_only": {"n_captions": len(dA), "delta_judge": dpt[0] - dpt[1], "delta_clip": dpt[0] - dpt[2],
                            "lower_bounds": {m: {lv: bound(deltas(dbs[:, 0], dbs[:, j]), al)  # §6.2, no verdict
                                                 for lv, al in (("95", 0.05), ("97.5", 0.025))}
                                             for j, m in ((1, "judge"), (2, "clip"))}},
        "per_captioner": {c: {"captions": sum(k[0] == c for k in keys), "gold_defined": sum(k[0] == c for k in G),
                              "analysed": sum(k[0] == c for k in A)} for c in acc},  # §7.3 drop counts
        "abstained_mapped_object_props": sum(cnt[cfg][k][2] for k in keys),
        "mapped_object_props": sum(cnt[cfg][k][1] + cnt[cfg][k][2] for k in keys)})
    return 0


# ---------------------------------------------------------------------------------------------- selftest
SENT, FIX_SEED = "SENTINELxq", 20261110
WORDS = ["zmeo", "zcho", "zghe", "zban", "zxe", "zcoc"]  # made-up tokens; class i + 1; the last two tagged instrument
ROWS = {**{w: [(i + 1, "dictionary" if i < 4 else "instrument")] for i, w in enumerate(WORDS)},
        "zthu": [(1, "dictionary"), (2, "dictionary")],  # one term, two rows (amendment §1(b))
        "zcun": [(2, "dictionary")],  # a second term of class 2 (§1(c))
        "zmix": [(3, "dictionary"), (5, "instrument")]}  # rows of both tags (§1(d))


def brute(x, y) -> float | None:
    """tau_c by the pair definition (independent of scipy and of tau()); None = undefined (a constant column)."""
    n, sg = len(x), lambda v: (v > 0) - (v < 0)
    s = sum(sg(x[i] - x[j]) * sg(y[i] - y[j]) for i in range(n) for j in range(i))
    m = min(len(set(x)), len(set(y)))
    return 2 * s / (n * n * (m - 1) / m) if m > 1 else None


def codes(x, y) -> tuple:
    """Rank codes of the pairs for a contingency table: rows = distinct x, columns = distinct y."""
    xr = np.unique(np.asarray(x, float), return_inverse=True)[1]
    yu, yr = np.unique(np.asarray(y, float), return_inverse=True)
    return xr * len(yu) + yr, int(xr.max()) + 1, len(yu)


def tau(code, kx: int, ky: int, w=None, b: bool = False) -> float:
    """v1's numpy form, kept for the selftest only (CC-316 V2) as a check of the scipy calls that is independent of
    scipy. Kendall tau from the (weighted) contingency table; ties kept. tau_c = 2 (P - Q) / (n^2 (m - 1) / m), m =
    the smaller number of distinct values present. b=True: tau_b. nan when a column is constant, as scipy."""
    t = np.bincount(code, weights=w, minlength=kx * ky).reshape(kx, ky)
    below = t.sum(0) - np.cumsum(t, 0)
    c = np.cumsum(below, 1)
    s = float((t * (c[:, -1:] - 2 * c + below)).sum())  # P - Q: larger-x partners with larger y minus smaller y
    r, k, n = t.sum(1), t.sum(0), float(t.sum())
    if b:
        n0, n1, n2 = n * (n - 1) / 2, float((r * (r - 1)).sum()) / 2, float((k * (k - 1)).sum()) / 2
        return s / ((n0 - n1) * (n0 - n2)) ** 0.5 if n0 > n1 and n0 > n2 else float("nan")
    m = min(int((r > 0).sum()), int((k > 0).sum()))
    return 2 * s / (n * n * (m - 1) / m) if m > 1 else float("nan")


def boot_np(image_ids: list[int], stats: list[tuple], nb: int):
    """v1's bootstrap (image weights into the numpy tau), selftest only: the replicates of boot() rebuilt without
    scipy and without expanding the resample."""
    ids = sorted(set(image_ids))
    img, cs = np.searchsorted(ids, image_ids), [codes(x, y) for x, y in stats]
    rng, out = np.random.default_rng(SEED), np.empty((nb, len(stats)))
    for i in range(nb):
        draw = rng.integers(0, len(ids), len(ids))
        out[i] = [tau(*c, w=np.bincount(draw, minlength=len(ids))[img]) for c in cs]
    return out


def fix_gold(ws: list, box: set, tags: frozenset) -> float | None:
    """The amendment's §1 wording on fixture words, formed from ROWS and the boxes, not by gold_of: a word with a row
    in `tags` is a mention, correct iff the class of any such row is boxed."""
    hit = [any(c in box for c, tg in ROWS[w] if tg in tags) for w in ws if any(tg in tags for _, tg in ROWS[w])]
    return sum(hit) / len(hit) if hit else None


def fixture(d: Path, mode: str, n: int = 40):  # noqa: C901  one linear generator
    """Synthetic pull, lists, map, annotation file and LOG under d; random.Random(f"{FIX_SEED}|{mode}"). No dataset
    text: captions are SENT plus made-up tokens. mode pass: B answers follow the boxes, judges are noisy. fail: B
    answers are random, J-a follows gold. edge: B, J-a and J-b all equal gold precision (delta = 0 in every resample,
    and an exact judge tie). const: B answers yes to everything, so its score is constant where defined (an undefined
    tau of B at step 8). flat: as const, with B defined on every gold-defined caption (an undefined lever tau).
    Returns the paths and `truth`: per caption the gold precision, B's score, B_open and the baselines, each formed
    here by the registered wording, not by the scorer."""
    import random
    from types import SimpleNamespace as NS

    r = random.Random(f"{FIX_SEED}|{mode}")
    acc, ids = ["c0", "c1", "c2", "c3"], list(range(1000, 1000 + n))
    mp = {"schema": "vsps.b_pa1.map.final", "terms": [{"vi": w} for w in [*ROWS, "zvoid"]],
          "rows": [{"vi": w, "o365_id": c, "tag": tg} for w, rows in ROWS.items() for c, tg in rows]}
    box = {i: set(r.sample(range(1, 7), r.randint(1, 4))) for i in ids}
    box[ids[0]] = set()  # an image without a box
    ann = [{"image_id": i, "category_id": c, "bbox": [0, 0, 1, 1], "iscrowd": c % 2}
           for i in ids for c in sorted(box[i])]
    ann += [{"image_id": 5, "category_id": c, "bbox": [0, 0, 1, 1], "iscrowd": 0} for c in range(1, 7)]
    files: dict[str, list] = {rel: [] for rels in CFGS.values() for rel in rels}
    files.update({rel: [] for rel, _ in (*JUDGES.values(), CLIP)})
    truth, steady = {}, mode in ("const", "flat")  # steady: B says yes to every proposition and never abstains
    for k in acc:
        caps = files.setdefault(f"out/a1decode/captions_{k}.jsonl", [])
        for i in ids:
            ws = r.sample(list(ROWS), r.choice([0, 1, 2, 2, 3, 3]))
            here = {w: any(c in box[i] for c, _ in ROWS[w]) for w in ws}
            g = fix_gold(ws, box[i], TAGS)
            caps.append({"id": i, "cap": k, "caption": " ".join([SENT, *ws, *ws[:1], "zcay", "zvoid"])})  # a word twice
            pw = [({"type": "object", "text": f"co {w}", "object": w if j % 2 else f"con {w}"}, w)
                  for j, w in enumerate(ws)]  # every other head noun in a classifier form: only the matcher maps it
            pw += [({"type": "object", "text": "co zcay", "object": "zcay"}, None),
                   ({"type": "object", "text": "co", "object": ""}, None)]  # no map term; an empty head noun
            pw += [({"type": "colour", "text": f"{w} do", "object": w}, w) for w in ws[:1]]
            if mode not in ("edge", "flat") and r.random() < 0.1:
                pw = pw[len(ws):]  # no mapped object proposition: B undefined
            props = [p for p, _ in pw]
            t = {"g": g, "g_dict": fix_gold(ws, box[i], DICT), "m": len(ws)}
            for cfg, (drel, vrel) in CFGS.items():
                ans = []
                for j, (p, w) in enumerate(pw):
                    yes = steady or (here.get(w, False) if mode != "fail" else r.random() < 0.5)
                    if not steady and cfg == "d2v1" and r.random() < 0.4:
                        yes = not yes
                    if p["type"] == "colour":
                        yes = not yes  # must never reach B's score
                    ab = mode in ("pass", "fail") and cfg != "d1v2" and r.random() < 0.08
                    ans.append({"k": j, "p_yes": 0.5 if yes else 0.49, "abstain": ab, "top1": "other" if ab else "Y"})
                if cfg != "d1v2":
                    files[drel].append({"id": i, "cap": k, "cfg": cfg[:2], "props": props, "parse": "ok"})
                else:
                    ans = files[CFGS["d1v1"][1]][-1]["props"]  # (d1,v2) = (d1,v1): an exact lever tie
                files[vrel].append({"id": i, "cap": k, "cfg": cfg, "props": ans, "n_props": len(ans)})
                obj = [(w, x) for (p, w), x in zip(pw, ans) if p["type"] == "object" and not x["abstain"]]
                for key, tags in ((cfg + "_dict", DICT), (cfg, TAGS)):
                    mo = [x["p_yes"] >= 0.5 for w, x in obj if w and any(tg in tags for _, tg in ROWS[w])]
                    t[key] = sum(mo) / len(mo) if mo else None
                t[cfg + "_open"] = sum(x["p_yes"] >= 0.5 for _, x in obj) / len(obj) if obj else None
                n_all = sum(p["type"] == "object" and w is not None for p, w in pw)
                t[cfg + "_wrong"] = sum(mo) / n_all if n_all else None  # mo: the TAGS answers, abstains left out
            g_ = 0.5 if g is None else g
            hi, lo = min(max(g_ + r.gauss(0, 0.6), 0), 1), min(max(g_ + r.gauss(0, 0.02), 0), 1)
            t["ja"] = {"fail": lo, "edge": g_}.get(mode, hi)
            t["jb"] = 9 * g_ if mode == "edge" else min(max(9 * (g_ + r.gauss(0, 1.0)), 0), 9)  # edge: J-a = J-b tie
            t["jc"] = 9 * r.random()
            t["clip"] = 2.5 * max(r.uniform(-0.1, 0.4), 0.0)
            files[JUDGES["ja"][0]].append({"id": i, "cap": k, "j": "ja", "p_yes": t["ja"], "abstain": False})
            files[JUDGES["jb"][0]].append({"id": i, "cap": k, "j": "jb", "ev": t["jb"]})
            files[JUDGES["jc"][0]].append({"id": i, "cap": k, "j": "jc", "ev": t["jc"]})
            files[CLIP[0]].append({"id": i, "cap": k, "score": t["clip"]})
            truth[(k, i)] = t
    files[WALK] = [{"key": k, "decision": "accept"} for k in acc]
    files["out/s/gate_c0.jsonl"] = [{"id": i, "cap": "c0", "caption": SENT} for i in ids[:5]]
    files["out/rest/a4/captions_x.jsonl"] = [{"id": i, "cap": "x", "caption": SENT} for i in ids[:7]]
    p = d / "pull"
    for rel, rows in files.items():
        (p / rel).parent.mkdir(parents=True, exist_ok=True)
        (p / rel).write_text("".join(json.dumps(x, ensure_ascii=False) + "\n" for x in rows), encoding="utf-8")
    (p / "out/s/ACCEPT.json").write_text(json.dumps({"accepted": acc}))
    (p / "logs").mkdir()
    (p / "logs/job.log").write_text("EXIT rest rc=0\n")
    (d / "in").mkdir()
    fx = NS(p=p, log=d / "LOG.md", lists=d / "in/b_pa1_lists.json", map=d / "in" / M.FINAL_NAME,
            ann=d / "in" / B.ANN_NAME, join=d / "join", truth=truth, ids=ids, acc=acc, box=box)
    fx.lists.write_text(json.dumps({"slice_a": ids, "slice_b": [i + n for i in ids]}))
    fx.map.write_text(json.dumps(mp))
    fx.ann.write_text(json.dumps({"images": [{"id": i, "file_name": f"patch0/{i}.jpg"} for i in ids],
                                  "annotations": ann, "categories": []}))
    fx.pins = {"ann": B.K.sha_file(fx.ann), "map": B.K.sha_file(fx.map), "lists": B.K.sha_file(fx.lists)}
    fx.log.write_text("")
    resum(fx)
    return fx


def pin(fx, name: str, sha: str) -> None:
    with open(fx.log, "a") as f:
        f.write(f"2026-11-10T00:00:00Z OPS-1110b-selftest-pin: PIN {name} {sha}\n")


def resum(fx) -> None:
    """(Re)write the fixture's SHA256SUMS_rest over out/ and logs/, and pin it on the fixture LOG."""
    rels = sorted(str(f.relative_to(fx.p)) for f in fx.p.rglob("*") if f.is_file() and f.name != SUMS)
    (fx.p / SUMS).write_text("".join(f"{B.K.sha_file(fx.p / r)}  {r}\n" for r in rels))
    pin(fx, SUMS, B.K.sha_file(fx.p / SUMS))


def fixture_join(d: Path) -> int:
    """`selftest-join D`: step 6 on the fixture under D, in the ijson venv (the selftest's own venv has no ijson)."""
    from types import SimpleNamespace as NS

    f = {"ann": d / "in" / B.ANN_NAME, "map": d / "in" / M.FINAL_NAME, "lists": d / "in/b_pa1_lists.json"}
    return cmd_join(NS(pulled=d / "pull", out_dir=d / "join", **f), log=d / "LOG.md",
                    pins={k: B.K.sha_file(p) for k, p in f.items()},
                    n=len(json.loads(f["lists"].read_bytes())["slice_a"]))


def quiet(fn, *a, **kw) -> str:
    buf = io.StringIO()
    with contextlib.redirect_stdout(buf):
        assert fn(*a, **kw) == 0
    return buf.getvalue()


def near(a: float, b: float) -> bool:
    return abs(a - b) < 1e-12


def same(a, b) -> bool:
    """Both undefined (None, or not finite), or equal to 1e-12."""
    a, b = strict(a), strict(b)
    return a is None and b is None or a is not None and b is not None and near(a, b)


def minus(a, b) -> float | None:
    return None if a is None or b is None else a - b


def selftest() -> int:  # noqa: C901  one linear script of fixtures
    import random
    from types import SimpleNamespace as NS

    # tau_c = the registered scipy call (§8.1): hand values, then the pair definition and v1's numpy form on tied data
    nan = float("nan")
    assert near(tau_c([1, 2, 3], [1, 2, 3]), 1.0) and near(tau_c([1, 2, 3, 4], [1, 1, 2, 2]), 1.0)
    assert near(tau_c([1, 2, 3, 4], [2, 2, 1, 1]), -1.0) and near(tau_c([1, 2, 2, 3], [1, 2, 3, 3]), 0.75)
    assert near(tau_c([1, 2, 2, 3], [1, 2, 3, 3], "b"), 0.8)
    assert near(tau(*codes([1, 2, 2, 3], [1, 2, 3, 3]), b=True), 0.8)
    r = random.Random(FIX_SEED)
    for _ in range(20):
        x, y = [r.randint(0, 6) for _ in range(40)], [r.randint(0, 3) / 3 for _ in range(40)]
        assert near(tau_c(x, y), brute(x, y)) and near(tau_c(x, y), tau(*codes(x, y)))
        assert near(tau_c(x, y, "b"), tau(*codes(x, y), b=True))
    # undefined values (amendment §3): tau_c gives nan and never refuses; an undefined replicate ranks lowest
    assert math.isnan(tau_c([1, 1, 1], [1, 2, 3])) and math.isnan(tau_c([1, 2, 3], [2, 2, 2]))
    assert brute([1, 1], [1, 2]) is None
    und = deltas(np.array([nan, 0.5, 0.3]), np.array([0.1, 0.1, nan]))
    assert und[0] == und[2] == -np.inf and near(und[1], 0.4)
    assert strict({"a": [nan, 1.0, -np.inf], "b": True, "c": None}) == {"a": [None, 1.0, None], "b": True, "c": None}
    few, many = (np.concatenate([np.full(k, -np.inf), np.full(N_BOOT - k, 0.5)]) for k in (300, 600))
    assert bound(few, 0.05) == 0.5 and not math.isfinite(bound(few, 0.025)) and not math.isfinite(bound(many, 0.05))
    assert near(bound(np.linspace(0.0, 1.0, 101), 0.05), 0.05) and near(bound(np.array([0.0, 1.0]), 0.05), 0.05)

    # selection (§7.1, §7.2), SESOI (§8.5), Holm (§8.3)
    assert pick({"ja": 0.300, "jb": 0.304, "jc": 0.3051}, JUDGES) == "jb"  # ja is 0.0051 below: outside
    assert pick({"ja": 0.3002, "jb": 0.304, "jc": 0.305}, JUDGES) == "ja"
    assert pick({"ja": 0.2, "jb": 0.25, "jc": 0.3}, JUDGES) == "jc"
    assert pick({"d1v1": 0.4, "d2v1": 0.41, "d1v2": 0.4051}, CFGS) == "d2v1" and list(CFGS) == ["d1v1", "d2v1", "d1v2"]
    assert pick({"d1v1": 0.4, "d2v1": 0.3, "d1v2": 0.4}, CFGS) == "d1v1" and list(JUDGES) == ["ja", "jb", "jc"]
    assert sesoi_of(0.004) == 0.02 and sesoi_of(0.03) == 0.06 and NI == 0.02
    assert (N_SLICE, N_BOOT, SEED) == (2000, 10_000, 20261101)
    lo, hi = np.linspace(0.0, 0.2, N_BOOT), np.linspace(0.5, 0.7, N_BOOT)
    h = holm({"H1b": hi, "H1c": hi + 0.1}, 0.1, True)
    assert [x["pass"] for x in h.values()] == [True, True] and near(h["H1b"]["p"], 1 / (N_BOOT + 1))
    assert [x["alpha"] for x in h.values()] == [0.025, 0.05] and near(h["H1b"]["lower_bound"], 0.505)
    h = holm({"H1b": lo, "H1c": hi}, 0.1, True)  # the smaller p (H1c) first; H1b then fails at 0.05
    assert list(h) == ["H1c", "H1b"] and (h["H1c"]["pass"], h["H1b"]["pass"]) == (True, False)
    assert near(h["H1c"]["lower_bound"], 0.505) and near(h["H1b"]["lower_bound"], 0.01) and h["H1b"]["p"] > 0.5
    h = holm({"H1b": hi, "H1c": lo}, 0.1, True)
    assert (h["H1b"]["pass"], h["H1c"]["pass"]) == (True, False)
    h = holm({"H1b": lo, "H1c": lo + 0.01}, 0.1, True)  # step-down: the first fails, so neither passes
    assert [x["pass"] for x in h.values()] == [False, False]
    assert [x["pass"] for x in holm({"H1b": hi, "H1c": hi}, 0.1, False).values()] == [False, False]  # H1a gate
    mid = np.concatenate([np.full(300, 0.0), np.full(N_BOOT - 300, 0.5)])  # p = 301/10001: > 0.025, <= 0.05
    h = holm({"H1b": hi, "H1c": mid}, 0.1, True)
    assert (h["H1b"]["pass"], h["H1c"]["pass"]) == (True, True) and near(h["H1c"]["p"], 301 / (N_BOOT + 1))
    assert [x["pass"] for x in holm({"H1b": mid, "H1c": mid}, 0.1, True).values()] == [False, False]
    edge = np.concatenate([np.full(250, 0.1), np.full(N_BOOT - 250, 0.5)])  # p form fails, CI form passes
    h = holm({"H1b": edge, "H1c": edge}, 0.1, True)  # the p form governs (amendment §7)
    assert [x["pass"] for x in h.values()] == [False, False] and [x["forms_agree"] for x in h.values()] == [False, True]
    h = holm({"H1b": hi, "H1c": few}, 0.1, True)  # 300 undefined replicates count as <= SESOI: p = 301/10001
    assert near(h["H1c"]["p"], 301 / (N_BOOT + 1)) and h["H1c"]["pass"] and h["H1c"]["lower_bound"] == 0.5
    h = holm({"H1b": hi, "H1c": many}, 0.1, True)  # 600: p > 0.05, and the 95% bound falls on an undefined replicate
    assert near(h["H1c"]["p"], 601 / (N_BOOT + 1)) and not h["H1c"]["pass"] and h["H1c"]["forms_agree"]
    assert not math.isfinite(h["H1c"]["lower_bound"]) and strict(h)["H1c"]["lower_bound"] is None

    # gold precision (amendment §1): matched terms, any-of, rows of the tag set only; W11 counts
    dt, it = "dictionary", "instrument"
    assert gold_of([]) is None and gold_of([[[1, dt, 1]], [[5, it, 0]]]) == 0.5
    assert gold_of([[[1, dt, 1]], [[5, it, 0]]], DICT) == 1.0 and gold_of([[[5, it, 0]]], DICT) is None
    assert gold_of([[[1, dt, 1], [2, dt, 0]]]) == 1.0 and gold_of([[[1, dt, 0], [2, dt, 0]]]) == 0.0  # (b) any-of
    assert gold_of([[[2, dt, 1]], [[2, dt, 1]], [[3, dt, 0]]]) == 2 / 3  # (c) two terms of class 2: two mentions
    assert gold_of([[[3, dt, 0], [5, it, 1]]]) == 1.0 and gold_of([[[3, dt, 0], [5, it, 1]]], DICT) == 0.0  # (d)
    assert gold_of([[[3, dt, 0], [5, it, 1]], [[5, it, 1]]], DICT) == 0.0  # an instrument-only term: no mention
    assert mention_counts({1: [[[1, dt, 1], [2, dt, 0]], [[2, dt, 1]], [[4, dt, 0]]], 2: [[[5, it, 0]]]}) == {
        "n": 4, "with_several_rows": 1, "sharing_a_class": 2}
    assert mention_counts({1: [[[3, dt, 0], [5, it, 1]], [[5, it, 1]]]}, DICT) == {
        "n": 1, "with_several_rows": 0, "sharing_a_class": 0}
    # B's score (§7.1) and the head-noun rule (amendment §2)
    with M.G.scratch("b_pa1_sc_") as d:
        fx = fixture(d, "pass")
        mp = json.loads(fx.map.read_bytes())
        mapped = Mapper(mp)
        assert mapped("zmeo", TAGS) and mapped("Zmeo", TAGS) and not mapped("zcay", TAGS) and not mapped("", TAGS)
        assert mapped("zxe", TAGS) and not mapped("zxe", DICT) and not mapped("zvoid", TAGS)  # a term with no row
        assert mapped("con zmeo", TAGS) and mapped("zcay zmeo zcay", DICT)  # through the matcher, not a lookup
        assert mapped("zmix", DICT) and mapped("zxe zmeo", DICT) and not mapped("zxe zcoc", DICT)  # several terms
        os.environ["RESCAP_RAW_TONE"] = "1"
        B.must_refuse(lambda: Mapper(mp), "RESCAP_RAW_TONE")
        del os.environ["RESCAP_RAW_TONE"]
        dec = {"props": [{"type": "object", "object": w} for w in ("con zmeo", "zcho", "zghe", "zcay", "")]
               + [{"type": "colour", "object": "zmeo"}]}
        ver = {"props": [{"k": 0, "p_yes": 0.5, "abstain": False}, {"k": 1, "p_yes": 0.499, "abstain": False},
                         {"k": 2, "p_yes": 0.9, "abstain": True}, {"k": 3, "p_yes": 0.7, "abstain": False},
                         {"k": 4, "p_yes": 0.7, "abstain": False}, {"k": 5, "p_yes": 0.9, "abstain": False}]}
        c = b_counts(dec, ver, mapped, TAGS)
        assert c == (1, 2, 1, 3, 4), c  # 0.5 is yes; the abstain is out; colour, unmapped and empty are not in B
        assert (b_score(c), b_score(c, "open"), b_score(c, "wrong")) == (1 / 2, 3 / 4, 1 / 3)
        assert b_score((0, 0, 1, 0, 0)) is None and b_score((0, 0, 1, 0, 0), "wrong") == 0.0
        B.must_refuse(lambda: b_counts(dec, {"props": ver["props"][1:]}, mapped, TAGS), "each object proposition")
        B.must_refuse(lambda: b_counts(dec, {"props": [{"k": 0, "p_yes": None, "abstain": False}, *ver["props"][1:]]},
                                       mapped, TAGS), "no yes-probability")

    out = {}
    for mode in ("fail", "edge", "const", "flat", "pass"):
        with M.G.scratch("b_pa1_sc_") as d:
            fx = fixture(d, mode)
            T, n = fx.truth, len(fx.ids)
            kw = {"log": fx.log, "pins": fx.pins}
            once, nb = mode == "fail", N_BOOT if mode == "pass" else 1_000  # the guards once, in the first mode;
            kb = kw if mode == "pass" else {**kw, "nb": nb}  # PASS takes the command line's default: the registered B
            ja = NS(pulled=fx.p, lists=fx.lists, map=fx.map, ann=fx.ann, out_dir=fx.join, join=fx.join)
            if once:  # pins, order lock, once-only, ids-only: one mode is enough
                B.must_refuse(lambda: cmd_contacts(NS(pulled=fx.p, lists=fx.lists, out_dir=M.ROOT / "scripts/x")),
                              "inside the tracked tree")
                so = quiet(cmd_contacts, NS(pulled=fx.p, lists=fx.lists, out_dir=d / "c"), n=n, **kw)
                doc = json.loads((d / "c" / CONTACTS_NAME).read_bytes())
                assert doc["ids"] == fx.ids and set(doc) == {"schema", "tier", "set", "ids", "sums_rest_sha256",
                                                             "lists_sha256", "code_sha256"}
                assert json.loads(so) == {"tier": B.LABEL, "n_ids": n, "sha256": B.K.sha_file(d / "c" / CONTACTS_NAME)}
                more = d / "in/lists_more.json"  # slice A with one id the pull never touched: a short contacts set
                more.write_text(json.dumps({"slice_a": [*fx.ids, fx.ids[-1] + 1]}))
                B.must_refuse(lambda: cmd_contacts(NS(pulled=fx.p, lists=more, out_dir=d / "c2"), n=n + 1, log=fx.log,
                                                   pins={"lists": B.K.sha_file(more)}), "not exactly slice A")
                with open(fx.p / "out/rest/a4/captions_x.jsonl", "a") as f:
                    f.write(json.dumps({"id": fx.ids[-1] + 1, "cap": "x", "caption": SENT}) + "\n")
                B.must_refuse(lambda: cmd_contacts(NS(pulled=fx.p, lists=fx.lists, out_dir=d / "c2"), n=n, **kw),
                              "differs from SHA256SUMS_rest")
                resum(fx)
                B.must_refuse(lambda: cmd_contacts(NS(pulled=fx.p, lists=fx.lists, out_dir=d / "c2"), n=n, **kw),
                              "not exactly slice A")
                (fx.p / "out/rest/a4/captions_x.jsonl").write_text(json.dumps({"id": fx.ids[0], "cap": "x"}) + "\n")
                sums = (fx.p / SUMS).read_bytes()
                (fx.p / SUMS).write_bytes(sums.replace(b"\n", b"\n" + b"0" * 64 + b"  out/none.txt\n", 1))
                B.must_refuse(lambda: cmd_join(ja, n=n, **kw), "not on a LOG pin line")
                resum(fx)
                for key, word in (("ann", "R6-pinned"), ("map", "differs from its pin"),
                                  ("lists", "differs from its pin")):
                    B.must_refuse(lambda: cmd_join(ja, n=n, log=fx.log, pins={**fx.pins, key: "0" * 64}), word)
                B.must_refuse(lambda: cmd_join(ja, n=n + 1, **kw), "distinct ids")
            run = subprocess.run([VENV_J, "-I", "-B", __file__, "selftest-join", d], capture_output=True, text=True)
            assert run.returncode == 0, run.stderr[-300:]
            so = run.stdout
            J = {(x["cap"], x["id"]): x["terms"]
                 for x in map(json.loads, (fx.join / GOLD_NAME).read_text().splitlines())}
            assert all(gold_of(J[k]) == T[k]["g"] and gold_of(J[k], DICT) == T[k]["g_dict"] for k in T)
            assert len(J) == 4 * n and json.loads(so)["imports_sha256"] == IMPORTS
            assert json.loads(so)["images_without_box"] == 1 and json.loads(so)["term_hits_without_o365_row"] == 4 * n
            assert all(c in fx.box[k[1]] if h else c not in fx.box[k[1]] for k, ts in J.items() for t in ts
                       for c, _, h in t)
            # the join holds the amendment's cases: a term with one boxed and one unboxed row; terms sharing a class;
            # a word written twice is one mention (the number of mentions = the number of distinct words)
            assert any(sorted(h for _, _, h in t) == [0, 1] for ts in J.values() for t in ts)
            mc = mention_counts(J)
            assert mc["n"] == sum(t["m"] for t in T.values()) and mc["with_several_rows"] and mc["sharing_a_class"]
            if once:  # amendment §3 at step 7, each a stop with nothing written; then the V6 import shas
                jf = {j: fx.p / rel for j, (rel, _) in JUDGES.items()}
                whole = {j: f.read_text() for j, f in jf.items()}
                jn, img = fx.join / JOIN_NAME, min(k[1] for k in T if T[k]["g"] is not None)
                raw = jn.read_bytes()
                for js, val, word in ((["jc"], lambda q, x: None if q == 0 else x["ev"], "undefined score"),
                                      (["jc"], lambda q, x: 4.0, "an undefined tau at step 7"),
                                      (list(JUDGES), lambda q, x: float(x["id"] == img), "undefined SE_A replicate")):
                    for j in js:
                        jf[j].write_text("".join(json.dumps({**x, JUDGES[j][1]: val(q, x)}) + "\n" for q, x in
                                                 enumerate(map(json.loads, whole[j].splitlines()))))
                    resum(fx)  # the join read no judge file: only its record of the manifest sha follows the edit
                    jn.write_bytes(MV.canon({**json.loads(raw), "sums_rest_sha256": B.K.sha_file(fx.p / SUMS)}))
                    B.must_refuse(lambda: cmd_thresholds(ja, **kb), word)
                    for j in js:
                        jf[j].write_text(whole[j])
                resum(fx)
                jn.write_bytes(MV.canon({**json.loads(raw), "imports_sha256": {**IMPORTS, "map_v1": "0" * 64}}))
                B.must_refuse(lambda: cmd_thresholds(ja, **kb), "an imported module differs")
                jn.write_bytes(raw)
            fx.ann.unlink()  # only join reads annotations[]
            hidden = [fx.p / rel for rels in CFGS.values() for rel in rels]
            for f in set(hidden):
                f.rename(f.with_suffix(".away"))  # step 7 opens no B output
            so += quiet(cmd_thresholds, ja, **kb)
            for f in set(hidden):
                f.with_suffix(".away").rename(f)
            th = json.loads((fx.join / TH_NAME).read_bytes())
            G = sorted(k for k in T if T[k]["g"] is not None)
            yG = [T[k]["g"] for k in G]
            want = {m: brute([T[k][m] for k in G], yG) for m in ("ja", "jb", "jc", "clip")}
            assert all(near(th["tau_c"][m], want[m]) for m in want), (th["tau_c"], want)
            assert th["judge_prompt"] == "ja" and th["ni"] == 0.02 and th["final_map_sha256"] == fx.pins["map"]
            assert near(th["spread_judge_clip"], abs(want["ja"] - want["clip"])) and th["n_captions"] == len(G)
            assert th["conventions"] == CONV and th["scipy"] == scipy.__version__ and th["amendment"] == AMEND
            # SE_A: the scipy replicates against v1's numpy form, and that form against the pair definition
            reps = boot_np([k[1] for k in G], [([T[k]["ja"] for k in G], yG)], nb)
            assert reps.shape == (nb, 1) and near(th["se_a"], float(np.std(reps[:, 0])))
            assert th["sesoi"] == max(0.02, 2 * th["se_a"]) and (th["n_boot"], th["seed"]) == (nb, 20261101)
            rng, ids = np.random.default_rng(20261101), sorted({k[1] for k in G})
            for i in range(12):
                draw = [ids[j] for j in rng.integers(0, len(ids), len(ids))]
                rs = [k for im in draw for k in G if k[1] == im]
                assert near(reps[i, 0], brute([T[k]["ja"] for k in rs], [T[k]["g"] for k in rs])), i
            assert MV.exists_error(lambda: cmd_thresholds(ja, **kb))  # written once, never recomputed
            jt = NS(pulled=fx.p, join=fx.join, map=fx.map)
            B.must_refuse(lambda: cmd_tau(jt, **kb), "T1_THRESHOLDS.json sha is not on a LOG pin line")
            pin(fx, "T1_THRESHOLDS.json", "0" * 64)  # another sha on the line is not a pin of this file
            B.must_refuse(lambda: cmd_tau(jt, **kb), "T1_THRESHOLDS.json sha is not on a LOG pin line")
            pin(fx, TH_NAME, B.K.sha_file(fx.join / TH_NAME))
            B.must_refuse(lambda: cmd_tau(jt, **kb), "more than one T1_THRESHOLDS.json pin line")
            fx.log.write_text("".join(ln for ln in fx.log.read_text().splitlines(True) if f" {'0' * 64}" not in ln))
            if once:
                keys = set(T)
                assert list(configs(Pulled(fx.p, fx.log), keys)) == ["d1v1", "d2v1", "d1v2"]
                v2 = fx.p / CFGS["d1v2"][1]
                whole = v2.read_text()
                v2.write_text(whole.split("\n", 1)[1])  # a partial A3 is never compared
                resum(fx)
                assert list(configs(Pulled(fx.p, fx.log), keys)) == ["d1v1"]
                v2.write_text(whole)
                resum(fx)
                B.must_refuse(lambda: cmd_tau(jt, log=fx.log, pins={**fx.pins, "map": "0" * 64}), "gold join is not of")
            so += quiet(cmd_tau, jt, **kb)
            rb = (fx.join / RES_NAME).read_bytes()
            res = json.loads(rb)
            assert b"NaN" not in rb and b"Infinity" not in rb  # strict JSON: an undefined number is null
            assert res["p_pass_planning"] == P_PASS and res["mentions"] == mc and res["conventions"] == CONV
            assert MV.exists_error(lambda: cmd_tau(jt, **kb))
            written = b"".join(f.read_bytes() for f in [*fx.join.iterdir(), *(d / "c").glob("*")])
            assert SENT not in so and SENT.encode() not in written and "zmeo" not in so  # no caption text leaves
            out[mode] = (th, res)
            if mode == "flat":  # an undefined lever tau: checked after the loop
                continue
            cfg = res["config"]
            lev = {c: brute([0.5 if T[k][c] is None else T[k][c] for k in G], yG) for c in CFGS}
            assert all(near(res["lever_tau_c"][c], lev[c]) for c in CFGS) and cfg == pick(lev, CFGS)
            A = [k for k in G if T[k][cfg] is not None]
            y = [T[k]["g"] for k in A]
            col = {"b": [T[k][cfg] for k in A], "judge": [T[k]["ja"] for k in A], "clip": [T[k]["clip"] for k in A],
                   "open": [T[k][cfg + "_open"] for k in A]}
            pt = {m: brute(x, y) for m, x in col.items()}  # scipy == the pair definition on every point
            assert all(same(res["tau_c"][m], pt[m]) for m in pt), (res["tau_c"], pt)
            assert all(same(res["tau_b"][m], tau(*codes(x, y), b=True)) for m, x in col.items()), res["tau_b"]
            dj = minus(pt["b"], pt["judge"])
            assert same(res["delta_judge"], dj) and same(res["delta_clip"], minus(pt["b"], pt["clip"]))
            assert same(res["open_sensitivity"]["delta_judge"], minus(pt["open"], pt["judge"]))
            assert res["pa3_effect_trigger"] == (dj is None or dj < th["sesoi"]) and res["sesoi"] == th["sesoi"]
            assert same(res["imputed_sensitivity"]["delta_judge"], lev[cfg] - want["ja"])
            W = [k for k in G if T[k][cfg + "_wrong"] is not None]
            assert same(res["abstain_as_wrong"]["delta_judge"], minus(brute([T[k][cfg + "_wrong"] for k in W], [
                T[k]["g"] for k in W]), brute([T[k]["ja"] for k in W], [T[k]["g"] for k in W])))
            assert res["per_captioner"]["c0"] == {"captions": n, "gold_defined": sum(k[0] == "c0" for k in G),
                                                  "analysed": sum(k[0] == "c0" for k in A)}
            assert res["n_captions"] == len(A) < len(G) < 4 * n or mode == "edge" and len(A) == len(G)
            bs = boot_np([k[1] for k in A], [(col[m], y) for m in ("b", "judge", "clip", "open")], nb)
            star = deltas(bs[:, 0], bs[:, 1])
            assert same(res["h1a"]["lower_bound_95"], bound(star, 0.05))
            assert res["h1a"]["pass"] == (bound(star, 0.05) > -0.02)
            assert near(res["holm"]["H1b"]["p"], (1 + int((~(star > th["sesoi"])).sum())) / (nb + 1))
            assert res["undefined_replicates"]["H1b"] == int(np.isnan(bs[:, 0] - bs[:, 1]).sum())
            assert same(res["open_sensitivity"]["lower_bound_975"], bound(deltas(bs[:, 3], bs[:, 1]), 0.025))
            dA = [k for k in sorted(T) if T[k]["g_dict"] is not None and T[k][cfg + "_dict"] is not None]
            dy = [T[k]["g_dict"] for k in dA]  # §6.2: the dictionary-only rows, with their bootstrap bounds
            dcol = [[T[k][m] for k in dA] for m in (cfg + "_dict", "ja", "clip")]
            dpt, do = [brute(x, dy) for x in dcol], res["dictionary_only"]
            assert do["n_captions"] == len(dA) < len(A) and same(do["delta_judge"], minus(dpt[0], dpt[1]))
            assert same(do["delta_clip"], minus(dpt[0], dpt[2]))
            db = boot_np([k[1] for k in dA], [(x, dy) for x in dcol], nb)
            assert same(do["lower_bounds"]["judge"]["95"], bound(deltas(db[:, 0], db[:, 1]), 0.05))
            assert same(do["lower_bounds"]["clip"]["97.5"], bound(deltas(db[:, 0], db[:, 2]), 0.025))

    th, res = out["pass"]  # PASS: H1a, then H1b and H1c; the PA3 effect trigger does not fire
    assert res["h1a"]["pass"] and res["holm"]["H1b"]["pass"] and res["holm"]["H1c"]["pass"], res
    assert not res["pa3_effect_trigger"] and res["config"] == "d1v1" and res["a3"] == "RUN"
    assert th["sesoi"] == 2 * th["se_a"] > 0.02  # noisy judge: SESOI = 2 SE_A
    assert res["undefined_replicates"] == {"H1b": 0, "H1c": 0} and res["holm"]["H1b"]["forms_agree"]
    assert th["n_boot"] == res["n_boot"] == 10_000  # this mode ran at the registered B
    th, res = out["fail"]  # FAIL: B below the judge; the gate fails, nothing passes, PA3 fires
    assert not res["h1a"]["pass"] and [x["pass"] for x in res["holm"].values()] == [False, False]
    assert res["pa3_effect_trigger"] and res["delta_judge"] < -0.02
    th, res = out["edge"]  # EDGE: delta = 0. H1a passes (0 > -NI), H1c is the smaller p and passes, H1b fails; PA3
    assert res["delta_judge"] == 0.0 and res["h1a"]["pass"] and res["h1a"]["lower_bound_95"] == 0.0
    assert (res["holm"]["H1c"]["step"], res["holm"]["H1b"]["step"]) == (1, 2)
    assert res["holm"]["H1c"]["pass"] and res["holm"]["H1b"]["pass"] is False
    assert res["holm"]["H1b"]["p"] == 1.0 and res["pa3_effect_trigger"] and res["config"] == "d1v1"
    th, res = out["const"]  # CONST: an undefined tau of B at step 8 (amendment §3). Nothing passes, PA3 fires
    assert res["tau_c"]["b"] is None and res["delta_judge"] is None and res["pa3_effect_trigger"] is True
    assert res["h1a"] == {"lower_bound_95": None, "pass": False} and res["config"] == "d1v1"
    assert [x["pass"] for x in res["holm"].values()] == [False, False] and res["holm"]["H1b"]["p"] == 1.0
    assert res["undefined_replicates"] == {"H1b": 1_000, "H1c": 1_000} and res["tau_c"]["judge"] is not None
    th, res = out["flat"]  # FLAT: an undefined lever tau of B. No configuration, nothing passes, PA3 fires
    assert res["config"] is None and res["lever_tau_c"] == {"d1v1": None, "d2v1": None, "d1v2": None}
    assert res["h1a"] == {"lower_bound_95": None, "pass": False} and res["pa3_effect_trigger"] is True
    assert res["holm"] == {"H1b": {"pass": False}, "H1c": {"pass": False}} and "tau_c" not in res
    print(json.dumps({"tier": B.LABEL, "selftest": "b_pa1_score_v2 ok", "fixture_seed": FIX_SEED, "checks": [
        "tau_c-scipy-hand-and-pairs", "scipy-eq-numpy-form", "tau_b-scipy", "tau-undefined-is-nan",
        "undefined-replicate-ranks-lowest", "bound-on-undefined-replicate", "strict-json", "judge-tie-order",
        "lever-tie-order", "sesoi-floor", "holm-order", "holm-step-down", "h1a-gate", "p-form-governs",
        "gold-mapped-mentions", "any-of-several-rows", "two-terms-one-class", "mixed-tags", "mention-counts",
        "head-noun-through-matcher", "empty-head-noun", "raw-tone-refused", "yes-at-0.5", "abstain-removed",
        "object-type-only", "contacts-ids-only", "contacts-equal-slice-A", "sums-pin", "input-pins", "join-vs-boxes",
        "word-twice-one-mention", "join-only-reads-annotations", "null-baseline-stops-step-7",
        "undefined-tau-stops-step-7", "undefined-replicate-stops-step-7", "import-shas", "thresholds-no-B-output",
        "se_a-bootstrap", "cluster-resamples-by-pairs", "thresholds-once", "tau-needs-LOG-pin",
        "one-thresholds-pin-line", "partial-A3", "points-by-pairs", "pa3-trigger", "dictionary-only-bounds",
        "p-pass-deviation", "no-caption-text-out", "PASS", "FAIL", "EDGE", "CONST", "FLAT"]}))
    return 0


def main() -> int:
    ap = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    sp = ap.add_subparsers(dest="cmd", required=True)
    sp.add_parser("selftest")
    sp.add_parser("selftest-join").add_argument("dir", type=Path)
    need = {"contacts": ("pulled", "lists", "out-dir"), "join": ("pulled", "lists", "map", "ann", "out-dir"),
            "thresholds": ("pulled", "join"), "tau": ("pulled", "join", "map")}
    for cmd, args in need.items():
        p = sp.add_parser(cmd)
        for x in args:
            p.add_argument(f"--{x}", type=Path, required=True)
    a = ap.parse_args()
    return {"selftest": selftest, "selftest-join": lambda: fixture_join(a.dir), "contacts": lambda: cmd_contacts(a),
            "join": lambda: cmd_join(a), "thresholds": lambda: cmd_thresholds(a), "tau": lambda: cmd_tau(a)}[a.cmd]()


if __name__ == "__main__":
    sys.exit(main())
