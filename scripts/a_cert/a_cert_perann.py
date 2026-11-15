#!/usr/bin/env python3
"""Paper A, A-CERT: H1 to H3 on the 150 overlap images with each annotator's labels. Registration v1.1 §10 l.243
("descriptive; after the second annotator | plan §4"); owed by CC-372 N3 and CC-374 ruling 6 (its own code, reusing the
committed a_cert H1-H3 path with only the label source swapped). Package: scripts/a_cert/PERANN_READ_PACKAGE.md.

  selftest --out F   synthetic fixtures only (a_cert.fixture and hand worlds); reads no label, key or result file
  score --labels-pi L1 --labels-pi-sha H1 --labels-r2 L3 --labels-r2-sha H3 --key K --r2-end-line ID
        --unseal-line ID --out F
      once; every statistic in memory, one atomic write; on any fault it prints `FAULT <type> <label-free|after-labels>`
      only and writes nothing.

Per annotator (PI: part-1 answers from L1, the scored copy ba362466; R2: from L3), on the overlap images only:
  H1  b_F and b_P points at the registered value and both remainder ends, Q25 on the overlap and Q3 on the overlap
      within I537, through a_cert.fam_slopes on a context restricted to those images;
  H2b per system on the overlap images (CC-391 Q2): budgets from a_cert.sys_cell / beta_B, coverage from the answers;
  H3  a_cert.h3_row on the H3 universe within the overlap, bootstrap a_m1.boot_weights(n_overlap, rng(20261111), 2000).
Every label-free overlap quantity is built before the key read (prepare; CC-391 B3). Rows that rest on a 600- or
537-image freeze or fixed stream are printed "not computable on the overlap subset" with their reason: the H1 intervals
and rule words, H2a, H2d. Every row carries "descriptive; no verdict; <n> overlap images; annotator <id>". No qid,
image or class is printed or written.
"""
from __future__ import annotations

import contextlib
import hashlib
import io
import json
import math
import os
import re
import sys
import tempfile
from pathlib import Path

import numpy as np

HERE = Path(__file__).resolve().parent
CODE_PINS = {"a_cert.py": "2e872588baf6109fad20111aecd25e2504fd0096f9033a95649027a2eed46cf4",
             "a_cert_kappa.py": "1a0be69411da6ca39a939526236ab9f1f108ee1681a380c3541fa958f29c753c"}


def pins_bad(pins: dict) -> list:
    """Files in scripts/a_cert/ whose sha256 differs from the pin; checked before either module is imported."""
    return [f for f, want in pins.items() if hashlib.sha256((HERE / f).read_bytes()).hexdigest() != want]


if pins_bad(CODE_PINS):
    raise SystemExit("refused: a_cert.py or a_cert_kappa.py differs from its pin")
sys.path.insert(0, str(HERE))  # python3 -I leaves the script directory off sys.path
import a_cert as ac  # noqa: E402
import a_cert_kappa as ak  # noqa: E402

Fault = ac.Fault
SELF = "scripts/a_cert/a_cert_perann.py"
FAMS = ("Q25", "Q3")
UNSEAL_TOKEN = "a-perann-unseal"
P_REAL = {"real": True, "log": ac.P_REAL["log"], "freeze": ac.P_REAL["freeze"],
          "freeze_sha": "c51ea7dc85d13b2f9827732f38218d41f26d877b06427bae02417e50482c3ae2",  # OPS-1112h (LOG l.2220)
          "assign": ac.ASSIGN, "assign_sha": ak.P_REAL["assign_sha"],
          "r2": f"{ac.PLAN_DIR}/overlap_r2/assignment.json", "r2_sha": ak.P_REAL["r2_sha"],
          "overlap": f"{ac.PLAN_DIR}/overlap_images.txt",
          "overlap_sha": "4f9719667c8a9294dc8cadc9565a048b9b7008ee0c1ecb924317550ba5278273",  # plan §8, BUILD.json
          "key_sha": ac.KEY_SHA, "pi1_sha": ak.P_REAL["pi1_sha"],
          "n_images": 150, "n_p1": 557, "n_target": 457}  # plan §4 l.37; BUILD_OVERLAP part 1 = 557
NC = "not computable on the overlap subset"
REASONS = {
    "H1_interval": "the registered H1 streams are fixed matrices on fixed image sets (Q25: the first 500 rows of "
                   "default_rng(0).integers(0, 600, (2000, 600)); Q3: the G2-B design-constant multinomial W over "
                   "I537) (reg v1.1 §2 l.77); a stream on the overlap images would be a new matrix. H3's stream, by "
                   "contrast, is registered as a function call (B, seed, a_m1.boot_weights; reg l.199) and is applied "
                   "to the overlap",
    "H1_rule_words": "H1a needs the registered 95% interval, which is not computable here; H1b and H1c compare with "
                     "the Table S7.2 ends, which are I600 and I537 values (reg v1.1 §2 l.78, §6 H1); the row is "
                     "descriptive with no verdict (reg v1.1 §10 l.243)",
    "H2a": "the certified set, its orientation and the null-rule selections were fixed by FREEZE.json on I600 (Q25) "
           "and I537 (Q3) (reg v1.1 §6 H2a, §8); no certificate on the overlap images was frozen, and making one "
           "after labels is the forbidden 'certified set recomputed after labels' (reg v1.1 §11)",
    "H2d": "the scores and exclusions come from FREEZE.json (I600/I537) and the replicate stream is "
           "a_m1.boot_weights(600, ...) (v1.3 §2, §3)"}
SCORE_ARGS = ("--labels-pi", "--labels-pi-sha", "--labels-r2", "--labels-r2-sha", "--key", "--r2-end-line",
              "--unseal-line", "--out")
DENY_EXTRA = ("/data/results/a_cert/score/",)


def hx(b: bytes) -> str:
    return hashlib.sha256(b).hexdigest()


def stamp(who: str, n: int) -> str:
    return f"descriptive; no verdict; {n} overlap images; annotator {who}"


def nc(who: str, n: int, row: str) -> dict:
    return {"label": stamp(who, n), "status": NC, "reason": REASONS[row]}


# ------------------------------------------------------------------------------------------------ custody
def refused(path) -> bool:
    """a_cert_kappa.refused (key.json, labels_/practice_ files, ~/vsps_labels*, sealed paths) plus the part-1 result."""
    p = os.path.abspath(os.fsdecode(path))
    return ak.refused(p) or (p not in ak._OK and any(d in p.replace(os.sep, "/") for d in DENY_EXTRA))


def _audit(event: str, args) -> None:
    if event in ("open", "os.listdir", "os.scandir") and args and \
            isinstance(args[0], (str, bytes, os.PathLike)) and refused(args[0]):
        raise Fault(f"custody: {event} refused")


# ------------------------------------------------------------------------------------------------ overlap world
def positions(ids: list, ov: set) -> np.ndarray:
    pos = np.array([k for k, i in enumerate(ids) if i in ov], int)
    if len(pos) != len(ov):
        raise Fault("an overlap image is not in the world")
    return pos


def sub_world(w: dict, pos: np.ndarray) -> dict:
    """The world with the H1 contexts restricted to the images pos (Q3: pos within I537); per-image lists stay whole.
    s75: point index and M_pt as bracket.s75_context builds them (M = mean |objects_in| per caption, object_prf column 1;
    a_cert.gate_core l.798-804 checks those sets equal ms_all); its bootstrap rows are a placeholder (one row = the point)
    whose interval is never reported. xm600: index and a one-row unit weight."""
    s75, g2 = w["ctx"]["Q25"], w["ctx"]["Q3"]
    q3 = np.intersect1d(np.asarray(g2["idx"]), pos)
    m = {s: float(np.mean([len(w["ms_all"][s][k]) for k in pos])) for s in s75["systems"]}
    c75 = {**s75, "full": pos[None], "idx_boot": pos[None],
           "systems": {s: {**d, "M_pt": m[s], "M_dr": np.array([m[s]])} for s, d in s75["systems"].items()}}
    c3 = {**g2, "idx": q3, "W": np.ones((1, len(q3)))}
    return {**w, "idx": {"Q25": pos, "Q3": q3}, "ctx": {"Q25": c75, "Q3": c3}}


def check_restriction(w: dict) -> None:
    """Label-free: the restricted context on all images reproduces the registered point slopes (F, P; both families)."""
    full = sub_world(w, np.arange(len(w["ids"])))
    for fam in FAMS:
        a, b = ac.fam_slopes(w, fam), ac.fam_slopes(full, fam)
        if any(abs(a[k][0] - b[k][0]) > 1e-9 for k in ("F", "P")):
            raise Fault("restriction does not reproduce the registered slopes")


def stop_guard(rng: dict, bF: dict, bP: dict, fam: str) -> None:
    """a_cert.score_core l.953-958 with the corner ranges of the overlap images (a_cert.clabel_slope on the restricted
    world, label-free): a completed slope outside them is a code fault."""
    checks = [(rng["F"]["range"], bF)] + ([(rng["P"]["range"], bP)] if fam == "Q3" else [])
    for (lo, hi), vals in checks:
        if any(not lo - 1e-9 <= x <= hi + 1e-9 for x in vals.values()):
            raise Fault("§5 STOP (overlap)")


# ------------------------------------------------------------------------------------------------ rows
def h1_rows(ws: dict, cn: dict, rngs: dict, who: str, n: int) -> dict:
    out = {}
    for fam in FAMS:
        add = {m: {s: (cn[s]["hy"] + (cn[s]["rem"] if m == "hi" else 0), cn[s]["hn"] + (cn[s]["rem"] if m == "lo" else 0))
                   for s in ws["fam"][fam]} for m in ("reg", "lo", "hi")}  # = a_cert.score_core l.947-948
        r = {m: ac.fam_slopes(ws, fam, add[m]) for m in add}
        bF, bP = ({m: float(r[m][k][0]) for m in r} for k in ("F", "P"))
        stop_guard(rngs[fam], bF, bP, fam)
        out[fam] = {"label": stamp(who, n), "n_images": len(ws["idx"][fam]), "b_F": bF, "b_P": bP}
    out["interval"] = nc(who, n, "H1_interval")
    out["rule_words"] = nc(who, n, "H1_rule_words")
    return out


def universe(w: dict) -> list:
    """H3 universe N_u per image (a_cert.score_core l.840-841): pairs named by any system with no Open Images status."""
    nm = [set().union(*(w["ms"][s][k] for s in w["sys"])) for k in range(len(w["ids"]))]
    nu = [{c for c in nm[k] if c not in w["oi"][k]} for k in range(len(w["ids"]))]
    return nu


def h3_rows(w: dict, gr: list, h: dict, nu: list, Wb: np.ndarray, pos: np.ndarray, who: str, n: int) -> dict:
    """H3 on the overlap images through a_cert.h3_row; N_u and the stream Wb are built label-free by prepare()."""
    row = ac.h3_row(w, gr, h, nu, Wb, pos)
    n_abs = sum(1 for k in pos for c in gr[k]["kp"] if w["oi"][k].get(c) == "absent" or h.get((w["ids"][k], c)) == "N")
    stream = {"call": f"a_m1.boot_weights({len(pos)}, numpy.random.default_rng({ac.SEED}), {ac.B_TRUTH})",
              "rows": f"1..{len(Wb) - 1}", "sha256_rows": hashlib.sha256(Wb[1:].tobytes()).hexdigest()}
    return {"label": stamp(who, n), "n_images": len(pos), **row, "n_ref_named_completed_absent": int(n_abs),
            "stream": stream}


def h2b_budgets(ws: dict, gr: list, pos: np.ndarray) -> dict:
    """Label-free H2b budgets on the overlap (CC-391 Q2; = a_cert.score_core l.866, l.874 with i600 -> pos): per system,
    the cell N_s of a_cert.sys_cell, beta_B at every grid w (None at w = 0), floor(beta(w0))."""
    out = {}
    for s in ws["sys"]:
        c = ac.sys_cell(ws["ms"], s, gr, pos)
        b = {str(wv): (None if wv == 0 else ac.beta_B(c, wv, ac.ALPHA_S)) for wv in ac.GRID}
        out[s] = {"U": c["U"], "f1": c["f1"], "beta": b, "floor_beta_w0": math.floor(b[str(ac.W0)])}
    return out


def h2b_rows(ws: dict, gr: list, h: dict, pos: np.ndarray, bud: dict, who: str, n: int) -> dict:
    """H2b per annotator (= a_cert.score_core l.866-881 with i600 -> pos): x_s, x_s_hi, covered, w_hat, counts; the
    a_cert.h2b_rule word only as `reading_no_verdict` (CC-391 Q2, Q6). Not printed: low_44, P_c, any PASS/FAIL label."""
    rows = {}
    for s in ws["sys"]:
        x = xh = 0
        for k in pos:
            i = ws["ids"][k]
            for cc in ws["ms"][s][k] - gr[k]["kp"]:
                st = ws["oi"][k].get(cc)
                x += st == "present" or (st is None and h.get((i, cc)) == "Y")
                xh += st == "present" or (st is None and h.get((i, cc)) in ("Y", None))
        b = bud[s]
        rows[s] = {"label": stamp(who, n), "x": int(x), "x_hi": int(xh), "U": b["U"], "f1": b["f1"], "beta": b["beta"],
                   "floor_beta_w0": b["floor_beta_w0"], "covered": xh <= b["floor_beta_w0"],
                   "w_hat": b["f1"] / (b["f1"] + 2 * x) if b["f1"] + x else None}
    binds = sum(bud[s]["floor_beta_w0"] < bud[s]["U"] for s in bud)
    return {"label": stamp(who, n), "n_images": len(pos), "systems": rows,
            "n_covered": sum(r["covered"] for r in rows.values()), "n_binding": binds,
            "reading_no_verdict": ac.h2b_rule([r["covered"] for r in rows.values()], binds)}


def prepare(w: dict, pos: np.ndarray) -> dict:
    """Every label-free overlap quantity, built BEFORE the key read (CC-391 B3): the restricted world, the STOP ranges,
    the unlabelled point slopes, the golds, the H2b budgets, N_u and the H3 stream. A non-finite range, point slope or
    budget is a label-free Fault."""
    ws = sub_world(w, pos)
    rngs = {fam: ac.clabel_slope(ws, fam) for fam in FAMS}
    pts = {fam: ac.fam_slopes(ws, fam) for fam in FAMS}
    gr = ac.gold_ref(ac.draw_two(w["refs_all"], w["ids"])[0], w["vm"])
    bud = h2b_budgets(ws, gr, pos)
    vals = [x for f in FAMS for k in ("F", "P") for x in (*rngs[f][k]["range"], pts[f][k][0])] + \
        [v for r in bud.values() for v in r["beta"].values() if v is not None]
    if not np.all(np.isfinite(np.asarray(vals, float))):
        raise Fault("overlap construction is not finite")
    return {"ws": ws, "pos": pos, "rngs": rngs, "gr": gr, "h2b": bud, "nu": universe(w),
            "Wb": w["boot_weights"](len(pos), np.random.default_rng(ac.SEED), ac.B_TRUTH)}


def compute(pre: dict, key: dict, ans_by: dict, n: int) -> dict:
    """Per annotator: a_cert.human -> a_cert.counts -> H1, H2b and H3 on the overlap; H2a and H2d not computable."""
    ws, gr, pos = pre["ws"], pre["gr"], pre["pos"]
    out = {}
    for who, ans in ans_by.items():
        h, _ = ac.human(key, ans, ws["syn"])
        cn = {s: ac.counts(ws, s, h) for s in ws["sys"]}
        out[who] = {"H1": h1_rows(ws, cn, pre["rngs"], who, n), "H2a": nc(who, n, "H2a"),
                    "H2b": h2b_rows(ws, gr, h, pos, pre["h2b"], who, n), "H2d": nc(who, n, "H2d"),
                    "H3": h3_rows(ws, gr, h, pre["nu"], pre["Wb"], pos, who, n)}
    return out


# ------------------------------------------------------------------------------------------------ score
def check_args(a: dict, P: dict) -> None:
    if Path(a["out"]).exists():
        raise Fault("--out exists")
    shas = (a["labels_pi_sha"], a["labels_r2_sha"])
    if not all(re.fullmatch(r"[0-9a-f]{64}", x) for x in shas):
        raise Fault("label sha argument is not 64 hex")
    if shas[0] == shas[1]:
        raise Fault("the two label sha arguments are not distinct")
    if a["labels_pi_sha"] != P["pi1_sha"]:
        raise Fault("--labels-pi-sha is not PI1_SHA")
    if P["real"] and not all(ac.committed(f) for f in (SELF, ac.SELF, "scripts/a_cert/a_cert_kappa.py", ac.REG)):
        raise Fault("code or registration differs from its HEAD blob")
    if P["real"] and ac.sha(ac.ROOT / ac.REG) != ac.SHA_REG:
        raise Fault("v1.1 is not the registered file")


def public_inputs(P: dict) -> tuple[dict, dict, set]:
    b = {k: (ac.ROOT / P[k]).read_bytes() for k in ("assign", "r2", "overlap")}
    if any(hx(b[k]) != P[k + "_sha"] for k in b):
        raise Fault("assignment or overlap list differs from its pin")
    base, r2a = (json.loads(b[k].decode("utf-8")) for k in ("assign", "r2"))
    ov = set(b["overlap"].decode("utf-8").split())
    if len(ov) != P["n_images"] or ov != {Path(s["image"]).stem for s in r2a["screens"]}:
        raise Fault("overlap list differs from the R2 screens")
    return base, r2a, ov


def log_hit(lines: list, ident: str, need: tuple) -> int:
    pat = re.compile(rf"(^|[\s|]){re.escape(ident)}[\s|:]")
    return next((k for k, ln in enumerate(lines) if pat.search(ln) and all(x in ln for x in need)), -1)


def gate_lines(a: dict, P: dict) -> None:
    """The R2 session-end line of this copy (CC-374 8(e)) and, after it, this row's own unsealing line (reg §12.7;
    CC-374 ruling 6) naming both label copies and this script."""
    lines = (ac.ROOT / P["log"]).read_text(encoding="utf-8").splitlines()
    end_need = ("R2 finished all screens yes", a["labels_r2_sha"])
    end = log_hit(lines, a["r2_end_line"], end_need)
    if end < 0:
        raise Fault("no R2 session-end line for this copy")
    up_need = (UNSEAL_TOKEN, a["labels_r2_sha"], a["labels_pi_sha"], hx(Path(__file__).read_bytes()))
    un = log_hit(lines, a["unseal_line"], up_need)
    if un <= end:
        raise Fault("no unsealing line after the R2 session-end line")


def read_key(a: dict, P: dict) -> dict:
    """key.json, allowed only inside this try (a_cert_kappa._OK); the same bytes are hashed and parsed (CC-372 1(b))."""
    path = os.path.abspath(a["key"])
    try:
        ak._OK.add(path)
        kb = Path(path).read_bytes()
    finally:
        ak._OK.discard(path)
    if hx(kb) != P["key_sha"]:
        raise Fault("key.json sha is not KEY_SHA")
    return json.loads(kb.decode("utf-8"))


def key_targets(key: dict, r2a: dict, ov: set, P: dict) -> set:
    """Label-free (CC-372 1(d), 2(g)): the R2 part-1 questions against the key; the 457 overlap part-1 targets."""
    rq1 = {q["qid"] for s in r2a["screens"] if s["part"] == 1 for q in s["q"]}
    if len(rq1) != P["n_p1"] or any(q not in key or key[q]["part"] != 1 or key[q]["image"] not in ov for q in rq1):
        raise Fault("R2 part-1 questions differ from the key or the registered count")
    t = {q for q in rq1 if key[q]["role"] == "target"}
    if len(t) != P["n_target"]:
        raise Fault("overlap part-1 targets differ from the registered count")
    return t


def read_labels(a: dict, seen: dict) -> tuple[dict, dict]:
    """The two label copies, allowed only inside this try; the stage turns after-labels before the first byte."""
    paths = [os.path.abspath(a[k]) for k in ("labels_pi", "labels_r2")]
    try:
        ak._OK.update(paths)
        seen["labels"] = True
        lp, lr = (Path(p).read_bytes() for p in paths)
    finally:
        ak._OK.clear()
    if (hx(lp), hx(lr)) != (a["labels_pi_sha"], a["labels_r2_sha"]):
        raise Fault("label file sha differs from its argument")
    return ak.answers(lp.decode("utf-8").splitlines(), "PI"), ak.answers(lr.decode("utf-8").splitlines(), "R2")


def label_checks(pi: dict, r2: dict, base: dict, r2a: dict, t: set) -> None:
    if not set(pi) <= {q["qid"] for s in base["screens"] for q in s["q"]}:
        raise Fault("PI qid outside the base assignment")
    if not set(r2) <= {q["qid"] for s in r2a["screens"] for q in s["q"]}:
        raise Fault("R2 qid outside the R2 assignment")
    if not t <= pi.keys():
        raise Fault("PI part 1 not complete on the overlap targets")
    if not t <= r2.keys():
        raise Fault("R2 not complete on the overlap part-1 targets")


def score(a: dict, P: dict = P_REAL, world_fn=None, seen: dict | None = None) -> dict:
    """Order: arguments -> public pins -> LOG gate lines -> FREEZE pin -> world -> every overlap construction ->
    key and its checks (all label-free) -> label bytes -> label checks -> statistics in memory."""
    seen = {} if seen is None else seen
    check_args(a, P)
    base, r2a, ov = public_inputs(P)
    gate_lines(a, P)
    fz, fsha = ac.pinned_freeze(P)
    if fsha != P["freeze_sha"]:
        raise Fault("FREEZE.json is not the pinned freeze")
    w = (world_fn or ac._score_world)()
    if w["pins"] != fz["pins"]:
        raise Fault("inputs differ from FREEZE pins")
    if P["real"] and len(w["ids"]) != 600:
        raise Fault("the world is not the 600 images")
    pos = positions(w["ids"], ov)
    check_restriction(w)
    pre = prepare(w, pos)
    key = read_key(a, P)
    t = key_targets(key, r2a, ov, P)
    pi, r2 = read_labels(a, seen)
    label_checks(pi, r2, base, r2a, t)
    rows = compute(pre, key, {"PI": {q: pi[q] for q in t}, "R2": {q: r2[q] for q in t}}, len(pos))
    return {"schema": "vsps.a_cert_perann.result.v1",
            "row": "reg v1.1 §10 l.243: H1 to H3 on the 150 overlap images with each annotator's labels | "
                   "descriptive; after the second annotator | plan §4",
            "n_images": {"Q25": len(pos), "Q3": rows["PI"]["H1"]["Q3"]["n_images"]}, "annotators": rows,
            "provenance": {"labels_pi_sha256": a["labels_pi_sha"], "labels_r2_sha256": a["labels_r2_sha"],
                           "key_sha256": P["key_sha"], "freeze_sha256": fsha, "code_sha256": hx(Path(__file__).read_bytes()),
                           "code_pins": CODE_PINS, "unseal_line": a["unseal_line"], "r2_end_line": a["r2_end_line"]}}


def run_score(a: dict, P: dict = P_REAL, world_fn=None) -> int:
    seen = {"labels": False}
    try:
        res = score(a, P, world_fn, seen)
        json.dumps(res, default=float)
        h = ac.write_atomic(Path(a["out"]), res)
    except BaseException as e:  # noqa: BLE001  (fault rule: exception type and stage only)
        print(f"FAULT {type(e).__name__} {'after-labels' if seen['labels'] else 'label-free'}")
        return 2
    print(json.dumps({"wrote": a["out"], "sha256": h}))
    return 0


# ------------------------------------------------------------------------------------------------ selftest
def selftest(out: Path) -> int:
    ck = {}
    try:
        _checks(ck)
    except BaseException as e:  # noqa: BLE001  (recorded; the mutant harness never counts it as a kill)
        ck[f"no_exception ({type(e).__name__}: {str(e)[:80]})"] = False
    ck = {k: bool(x) for k, x in ck.items()}
    rec = {"schema": "vsps.a_cert_perann.selftest.v1", "script_sha256": hx(Path(__file__).read_bytes()),
           "checks": ck, "n": len(ck), "pass": all(ck.values())}
    Path(out).write_text(json.dumps(rec, indent=1) + "\n", encoding="utf-8")
    print("\n".join(f"{'ok  ' if x else 'FAIL'} {k}" for k, x in ck.items()))
    print(f"{len(ck)} checks; " + ("selftest ok" if rec["pass"] else "selftest FAILED"))
    return 0 if rec["pass"] else 1


def _raises(fn, word: str) -> bool:
    """True only for a Fault (a_cert or a_cert_kappa) whose message holds `word`."""
    try:
        fn()
    except (Fault, ak.Fault) as e:
        return word in str(e)
    except Exception:  # noqa: BLE001
        return False
    return False


def _try(fn):
    try:
        return fn()
    except Exception:  # noqa: BLE001
        return None


def _out(fn) -> tuple:
    buf = io.StringIO()
    with contextlib.redirect_stdout(buf):
        rc = _try(fn)
    return rc, buf.getvalue()


def _norm(x):
    return json.loads(json.dumps(x, default=float))


def _get(d, *path):
    for p in path:
        d = d.get(p) if isinstance(d, dict) else None
    return d


def _fixture() -> dict:
    """a_cert.fixture (40 synthetic images, 12 systems) and a_cert.fixture_labels (key + PI answers); R2 answers drawn
    here with their own seed; overlap = images k % 4 in {0, 1} (20 images, five of them outside the fixture's I537)."""
    br = ac.test_mods()
    w = ac.fixture(br)
    key, lines = ac.fixture_labels(w)
    pi_lines = [json.dumps({**json.loads(x), "annotator": "PI"}) for x in lines]
    ov = {i for k, i in enumerate(w["ids"]) if k % 4 in (0, 1)}
    rng = np.random.default_rng(13)
    r2 = {q: str(rng.choice(["Y", "N", "U", "A"], p=[.4, .4, .1, .1])) for q, k in sorted(key.items())
          if k["part"] == 1 and k["image"] in ov}
    t = {q for q, k in key.items() if k["part"] == 1 and k["role"] == "target" and k["image"] in ov}
    return {"w": w, "key": key, "pi_lines": pi_lines, "pi": ak.answers(pi_lines, "PI"), "r2": r2, "ov": ov, "t": t,
            "pos": positions(w["ids"], ov), "fz": ac.freeze_core(w)}


def _files(d: Path, tag: str, fx: dict, r2_rows=None, pi_lines=None, ov=None, swap_log=False, end_edit=("", ""),
           up_edit=("", ""), **over) -> tuple:
    """Fixture files in d/tag (no labels_* or key.json names, so the hook lets them through); returns (args, P).
    end_edit / up_edit = (old, new) applied to the gate-line templates before the shas are filled in (CC-391 B2); the
    U-P line id carries no token, so the token is tested as line content."""
    wd = d / tag
    wd.mkdir()
    scr = {}
    for q, k in sorted(fx["key"].items()):
        scr.setdefault((k["part"], k["image"]), []).append({"qid": q})
    base = [{"part": p, "image": f"images/{i}.jpg", "q": qs} for (p, i), qs in sorted(scr.items())]
    r2a = [s for s in base if Path(s["image"]).stem in fx["ov"]]
    r2_rows = [(q, x, "R2") for q, x in sorted(fx["r2"].items())] if r2_rows is None else r2_rows
    body = {"base.json": json.dumps({"screens": base}), "r2a.json": json.dumps({"screens": r2a}),
            "ov.txt": "".join(f"{i}\n" for i in sorted(fx["ov"] if ov is None else ov)),
            "kx.json": json.dumps(fx["key"]), "pi.jsonl": "".join(x + "\n" for x in (pi_lines or fx["pi_lines"])),
            "r2.jsonl": "".join(json.dumps({"qid": q, "label": x, "annotator": who}) + "\n" for q, x, who in r2_rows)}
    for name, txt in body.items():
        (wd / name).write_text(txt, encoding="utf-8")
    sh = {k: hx(v.encode("utf-8")) for k, v in body.items()}
    fsha = ac.write_atomic(wd / "FREEZE.json", fx["fz"])
    tpl = ["2026-01-01T00:00:01Z | OPS-fx-r2-end | labels_R2 copy {r2}; R2 finished all screens yes".replace(*end_edit),
           f"2026-01-01T00:00:02Z | OPS-fx-up | {UNSEAL_TOKEN} | R2 {{r2}}; PI {{pi}}; code {{code}}".replace(*up_edit)]
    gl = [x.format(r2=sh["r2.jsonl"], pi=sh["pi.jsonl"], code=hx(Path(__file__).read_bytes())) for x in tpl]
    log = [f"2026-01-01T00:00:00Z OPS-fx-freeze: FREEZE.json sha256 {fsha}"] + (gl[::-1] if swap_log else gl)
    (wd / "LOG.md").write_text("\n".join(log) + "\n", encoding="utf-8")
    n1 = sum(len(s["q"]) for s in r2a if s["part"] == 1)
    P = {"real": False, "log": str(wd / "LOG.md"), "freeze": str(wd / "FREEZE.json"), "freeze_sha": fsha,
         "assign": str(wd / "base.json"), "assign_sha": sh["base.json"], "r2": str(wd / "r2a.json"),
         "r2_sha": sh["r2a.json"], "overlap": str(wd / "ov.txt"), "overlap_sha": sh["ov.txt"], "key_sha": sh["kx.json"],
         "pi1_sha": sh["pi.jsonl"], "n_images": len(fx["ov"]), "n_p1": n1, "n_target": len(fx["t"])}
    a = {"labels_pi": str(wd / "pi.jsonl"), "labels_pi_sha": sh["pi.jsonl"], "labels_r2": str(wd / "r2.jsonl"),
         "labels_r2_sha": sh["r2.jsonl"], "key": str(wd / "kx.json"), "r2_end_line": "OPS-fx-r2-end",
         "unseal_line": "OPS-fx-up", "out": str(wd / "out" / "RESULT.json")}
    for k, v in over.items():
        (P if k in P else a)[k] = v
    return a, P


def _checks(ck: dict) -> None:
    _unit_checks(ck)
    fx = _fixture()
    _fixture_checks(ck, fx)
    with tempfile.TemporaryDirectory() as td:
        _score_checks(ck, fx, Path(td))
        _refusal_checks(ck, fx, Path(td))
        _custody_checks(ck, Path(td))


def _unit_checks(ck: dict) -> None:
    ck["code_pins_hold_and_other_sha_refused"] = pins_bad(CODE_PINS) == [] and \
        pins_bad({"a_cert.py": "0" * 64}) == ["a_cert.py"]
    ck["stamp_text"] = stamp("R2", 150) == "descriptive; no verdict; 150 overlap images; annotator R2"
    ck["positions_by_hand_and_missing_id_fault"] = _try(lambda: positions(list("abcd"), {"b", "d"}).tolist()) == \
        [1, 3] and _raises(lambda: positions(["a"], {"z"}), "overlap image")
    ok = lambda r, b: {"F": {"range": r}, "P": {"range": b}}  # noqa: E731
    v = {"reg": .5, "lo": .2, "hi": .9}
    ck["stop_guard_by_hand"] = _try(lambda: stop_guard(ok([0, 1], [2, 3]), v, v, "Q25") or True) is True and \
        _raises(lambda: stop_guard(ok([0, 1], [2, 3]), v, v, "Q3"), "STOP") and \
        _raises(lambda: stop_guard(ok([.3, 1], [0, 1]), v, v, "Q25"), "STOP") and \
        _try(lambda: stop_guard(ok([.2 + 1e-10, .9 - 1e-10], [0, 1]), v, v, "Q3") or True) is True
    # H3 wiring by hand: images i, j, k; overlap = i and k. N_u: i {b, e}, j {a, b}, k {c} (d has an OI status).
    # i: b named by both refs, x by one; human (i, e) Y, (i, x) N. j (outside): a by one ref, (j, b) Y. k: d by one ref.
    # On {i, k}: phi1 0, phi2 1, X 1 (e), X_hi 2 (+ c), f0 0, D 1, D_hi 2; completed-absent ref pairs: x (N), d (OI).
    wm = {"ids": ["i", "j", "k"], "sys": ["s", "t"], "f0_hat": ac._p50x().f0_hat, "boot_weights": ac._a_m1().boot_weights,
          "ms": {"s": [{"a", "b"}, {"a"}, {"c", "d"}], "t": [{"b", "e"}, {"b"}, {"d"}]},
          "oi": [{"a": "present"}, {}, {"d": "absent"}]}
    grm = [{"kp": {"b", "x"}, "once": {"x"}, "twice": {"b"}}, {"kp": {"a"}, "once": {"a"}, "twice": set()},
           {"kp": {"d"}, "once": {"d"}, "twice": set()}]
    hm = {("i", "e"): "Y", ("i", "x"): "N", ("j", "b"): "Y", ("k", "c"): None}
    two = np.array([0, 2])
    r = _try(lambda: h3_rows(wm, grm, hm, universe(wm), wm["boot_weights"](2, np.random.default_rng(20261111), 2000),
                             two, "R2", 2)) or {}
    ck["H3_overlap_wiring_by_hand"] = [r.get(x) for x in ("phi1", "phi2", "f0_hat", "X", "X_hi", "D", "D_hi")] == \
        [0, 1, 0, 1, 2, 1, 2] and r.get("n_ref_named_completed_absent") == 2 and \
        r.get("reading_no_verdict") == "NOT EVALUABLE" and r.get("n_images") == 2
    # H2b by hand on {i, k}, made-up budgets. s: i {a} OI present (x, x_hi); k {c} remainder (x_hi) -> x 1, x_hi 2.
    # t: i {e} human Y -> x 1, x_hi 1; k {} . Budgets s U 5 floor 3 (binds), t U 2 floor 4 (does not) -> n_binding 1;
    # covered 2 <= 3 and 1 <= 4; w_hat s 1/(1+2), t 0/(0+2); h2b_rule([True, True], 1) = "FAIL" (fewer than 11 of 12).
    bud = {"s": {"U": 5, "f1": 1, "beta": {"0.2": 3.5}, "floor_beta_w0": 3},
           "t": {"U": 2, "f1": 0, "beta": {"0.2": 4.5}, "floor_beta_w0": 4}}
    r = _try(lambda: h2b_rows(wm, grm, hm, two, bud, "R2", 2)) or {}
    ck["H2b_counts_binding_and_word_by_hand"] = _try(lambda: [
        (r["systems"][s]["x"], r["systems"][s]["x_hi"], r["systems"][s]["covered"], r["systems"][s]["w_hat"])
        for s in "st"] == [(1, 2, True, 1 / 3), (1, 1, True, 0.0)] and (
        r["n_covered"], r["n_binding"], r["reading_no_verdict"], r["n_images"]) == (2, 1, "FAIL", 2)) is True


def _fixture_checks(ck: dict, fx: dict) -> None:
    w, key, pi, pos = fx["w"], fx["key"], fx["pi"], fx["pos"]
    allp = np.arange(len(w["ids"]))
    ws = _try(lambda: sub_world(w, allp)) or {"ctx": {"Q25": {"systems": {}}}}
    ck["restricted_M_on_all_images_equals_context_M"] = len(ws["ctx"]["Q25"]["systems"]) == 6 and all(
        abs(d["M_pt"] - w["ctx"]["Q25"]["systems"][s]["M_pt"]) < 1e-12 for s, d in ws["ctx"]["Q25"]["systems"].items())
    so = _try(lambda: sub_world(w, pos)) or {"idx": {"Q3": []}}
    ck["Q3_is_overlap_within_I537"] = set(map(int, so["idx"]["Q3"])) == set(map(int, pos)) & \
        set(map(int, w["idx"]["Q3"])) and 0 < len(so["idx"]["Q3"]) < len(pos)
    ck["restriction_on_all_images_reproduces_fam_slopes"] = _try(lambda: check_restriction(w) or True) is True
    full = _try(lambda: compute(prepare(w, allp), key, {"PI": pi}, 40)) or {}
    ref = ac.score_core(w, fx["fz"], key, pi)
    hb, rb = _get(full, "PI", "H2b") or {}, ref["H2b"]
    ck["H2b_all_images_equals_score_core"] = bool(hb) and set(hb["systems"]) == set(rb["systems"]) and all(
        hb["systems"][s][f] == rb["systems"][s][f] for s in rb["systems"]
        for f in ("x", "x_hi", "U", "f1", "beta", "covered", "w_hat")) and all(
        hb["systems"][s]["floor_beta_w0"] == math.floor(rb["systems"][s]["beta"][str(ac.W0)]) for s in rb["systems"]) \
        and (hb["n_covered"], hb["n_binding"], hb["reading_no_verdict"]) == (rb["n_covered"], rb["n_binding"], rb["label"])
    ck["H1_all_images_equals_score_core_reg_lo_hi"] = all(
        abs(_get(full, "PI", "H1", f, b, m) - ref["H1"][f][b][m]) < 1e-9 for f in FAMS for b in ("b_F", "b_P")
        for m in ("reg", "lo", "hi")) if full else False
    h3, r3 = _get(full, "PI", "H3") or {}, ref["H3"]
    ck["H3_all_images_equals_score_core"] = bool(h3) and all(
        h3[x] == r3[x] for x in ("phi1", "phi2", "f0_hat", "X", "X_hi", "D", "D_hi", "D_ci95", "D_hi_ci95")) and \
        h3["reading_no_verdict"] == r3["label"] and \
        h3["n_ref_named_completed_absent"] == r3["n_ref_named_completed_absent"]
    pre = _try(lambda: prepare(w, pos)) or {}
    sub = _try(lambda: compute(pre, key, {"PI": pi, "R2": fx["r2"]}, 20)) or {}
    s0 = w["sys"][0]
    ck["overlap_rows_differ_from_all_image_rows"] = bool(sub) and \
        _get(sub, "PI", "H1", "Q25", "b_F", "reg") != _get(full, "PI", "H1", "Q25", "b_F", "reg") and \
        _get(sub, "PI", "H3", "phi1") != _get(full, "PI", "H3", "phi1") and \
        _get(sub, "PI", "H2b", "systems", s0, "U") != _get(full, "PI", "H2b", "systems", s0, "U")
    flip = {q: ({"Y": "N", "N": "Y"}.get(x, "Y") if key[q]["image"] not in fx["ov"] else x) for q, x in pi.items()}
    alt = _try(lambda: compute(pre, key, {"PI": flip}, 20)) or {}
    ck["answers_outside_overlap_change_nothing"] = bool(sub) and _norm(alt.get("PI")) == _norm(sub["PI"]) and \
        any(flip[q] != pi[q] for q in pi if key[q]["part"] == 1 and key[q]["role"] == "target")
    only = _try(lambda: compute(pre, key, {"R2": fx["r2"]}, 20)) or {}
    ck["R2_rows_from_R2_answers_and_differ_from_PI"] = bool(sub) and _norm(only.get("R2")) == _norm(sub["R2"]) and \
        _get(sub, "PI", "H1", "Q25", "b_F") != _get(sub, "R2", "H1", "Q25", "b_F")
    ck["H1_n_images_Q25_overlap_Q3_within_I537"] = bool(sub) and \
        (_get(sub, "R2", "H1", "Q25", "n_images"), _get(sub, "R2", "H1", "Q3", "n_images")) == \
        (len(pos), len(so["idx"]["Q3"]))
    ro = np.random.default_rng(20261111)
    orc = np.array([np.bincount(ro.integers(0, 20, 20), minlength=20) for _ in range(2000)], float)
    st = _get(sub, "R2", "H3", "stream") or {}
    ck["H3_stream_boot_weights_20_seed_20261111_rows_1_2000"] = st.get("sha256_rows") == \
        hashlib.sha256(orc.tobytes()).hexdigest() and st.get("rows") == "1..2000"
    want = {"H2a": "H2a", "H2d": "H2d"}
    ck["not_computable_rows_with_their_reasons"] = bool(sub) and all(
        sub[a][r]["status"] == NC and sub[a][r]["reason"] == REASONS[x] for a in ("PI", "R2") for r, x in want.items()) \
        and all(sub[a]["H1"][r]["status"] == NC and sub[a]["H1"][r]["reason"] == REASONS[x] for a in ("PI", "R2")
                for r, x in (("interval", "H1_interval"), ("rule_words", "H1_rule_words")))
    def rows(a):
        return [sub[a]["H1"][x] for x in ("Q25", "Q3", "interval", "rule_words")] + \
            [sub[a][x] for x in ("H2a", "H2b", "H2d", "H3")] + list(sub[a]["H2b"]["systems"].values())
    ck["every_row_carries_the_label"] = bool(sub) and all(
        r["label"] == stamp(a, 20) for a in ("PI", "R2") for r in rows(a))


def _score_checks(ck: dict, fx: dict, d: Path) -> None:
    a, P = _files(d, "w", fx)
    wf = lambda: fx["w"]  # noqa: E731
    rc, so = _out(lambda: run_score(a, P, wf))
    f = Path(a["out"])
    body = f.read_text(encoding="utf-8") if f.is_file() else "{}"
    res = json.loads(body)
    ck["ok_list_cleared_after_score"] = not ak._OK
    t = fx["t"]
    direct = _try(lambda: compute(prepare(fx["w"], fx["pos"]), fx["key"], {"PI": {q: fx["pi"][q] for q in t},
                                                                             "R2": {q: fx["r2"][q] for q in t}}, 20))
    ck["score_writes_once_rows_equal_direct_compute"] = rc == 0 and direct is not None and \
        res.get("annotators") == _norm(direct) and sorted(x.name for x in f.parent.iterdir()) == ["RESULT.json"]
    ck["stdout_is_wrote_and_sha_only"] = rc == 0 and json.loads(so or "{}") == {"wrote": a["out"], "sha256": hx(
        body.encode("utf-8"))}
    ids, cls = fx["w"]["ids"], fx["w"]["vm"]
    ck["result_and_stdout_hold_no_qid_image_or_class"] = rc == 0 and not any(  # quoted: floats hold long digit runs
        f'"{q}"' in body or q in so for q in fx["key"]) and not any(f'"{i}"' in body for i in ids) and \
        not any(f'"{c}"' in body for c in cls)
    rc, so = _out(lambda: run_score(a, P, wf))
    ck["second_run_refused_FAULT_type_label_free"] = rc == 2 and so == "FAULT Fault label-free\n"
    a2, P2 = _files(d, "f1", fx, r2_rows=[(q, x, "R2") for q, x in sorted(fx["r2"].items()) if q != min(t)])
    rc, so = _out(lambda: run_score(a2, P2, wf))
    ck["after_labels_fault_prints_stage_and_writes_nothing"] = rc == 2 and so == "FAULT Fault after-labels\n" and \
        not Path(a2["out"]).parent.exists()
    argv = ["score"] + [x for k in SCORE_ARGS for x in (k, {**a2, "labels_pi_sha": "1" * 64, "out": str(d / "nx")}
                                                        [k[2:].replace("-", "_")])]
    rc, so = _out(lambda: main(argv))
    ck["main_maps_score_argv_to_a_label_free_fault"] = rc == 2 and so == "FAULT Fault label-free\n"


def _refusal_checks(ck: dict, fx: dict, d: Path) -> None:
    gone = {"labels_pi": str(d / "n1.jsonl"), "labels_r2": str(d / "n2.jsonl"), "key": str(d / "n3.json")}
    only_labels_gone = {k: v for k, v in gone.items() if k != "key"}  # key-derived guards must come before labels
    w = fx["w"]
    n = [0]

    def refuses(word, labels_gone=True, a_over=None, wf=None, mutate=None, **kw):
        n[0] += 1
        a, P = _files(d, f"x{n[0]:02d}", fx, **kw)
        if mutate:
            mutate(a)
        return _raises(lambda: score({**a, **(gone if labels_gone else {}), **(a_over or {})}, P,
                                     wf or (lambda: w)), word)

    pi_rows = [x for x in fx["pi_lines"] if json.loads(x)["qid"] != min(fx["t"])]
    r2_rows = [(q, x, "R2") for q, x in sorted(fx["r2"].items())]
    c75 = w["ctx"]["Q25"]
    bad_m = {**w, "ctx": {**w["ctx"], "Q25": {**c75, "systems": {s: {**v, "M_pt": v["M_pt"] + 1} for s, v in
                                                                    c75["systems"].items()}}}}
    ck["refuses_out_exists_before_labels"] = refuses("--out exists", a_over={"out": str(d)})
    ck["refuses_sha_argument_not_64_hex"] = refuses("64 hex", labels_r2_sha="abc")
    ck["refuses_sha_arguments_not_distinct"] = refuses("not distinct", mutate=lambda a: a.update(
        labels_r2_sha=a["labels_pi_sha"]))
    ck["refuses_pi_sha_not_PI1_SHA_before_labels"] = refuses("PI1_SHA", pi1_sha="3" * 64)
    ck["refuses_base_assignment_pin"] = refuses("pin", assign_sha="0" * 64)
    ck["refuses_r2_assignment_pin"] = refuses("pin", r2_sha="0" * 64)
    ck["refuses_overlap_list_pin"] = refuses("pin", overlap_sha="0" * 64)
    ck["refuses_overlap_list_not_the_R2_screens"] = refuses("R2 screens", ov=set(sorted(fx["ov"])[1:]),
                                                            n_images=len(fx["ov"]) - 1)
    ck["refuses_without_R2_session_end_line"] = refuses("session-end", r2_end_line="OPS-none")
    ck["refuses_without_unsealing_line"] = refuses("unsealing", unseal_line="OPS-none-a-perann-unseal")
    ck["refuses_unsealing_line_before_R2_end"] = refuses("unsealing", swap_log=True)
    # CC-391 B2: each required item of the two gate lines, with the line id present
    ck["refuses_end_line_without_phrase"] = refuses("session-end", end_edit=("R2 finished all screens yes", ""))
    ck["refuses_end_line_with_other_R2_sha"] = refuses("session-end", end_edit=("{r2}", "0" * 64))
    ck["refuses_unsealing_line_without_token"] = refuses("unsealing", up_edit=(UNSEAL_TOKEN, ""))
    ck["refuses_unsealing_line_without_PI_sha"] = refuses("unsealing", up_edit=("{pi}", ""))
    ck["refuses_unsealing_line_without_R2_sha"] = refuses("unsealing", up_edit=("{r2}", ""))
    ck["refuses_unsealing_line_without_script_sha"] = refuses("unsealing", up_edit=("{code}", ""))
    # CC-391 B3: a non-finite overlap construction is a label-free Fault, before the key read (key and labels absent).
    # Made-up world: one Q25 system names nothing on the overlap images, so its overlap M is 0 and ln M is -inf there;
    # its context M is reset to the mean over all images, so the all-image restriction check still holds.
    q0, ovp = w["fam"]["Q25"][0], set(map(int, fx["pos"]))
    ms0 = [set() if k in ovp else m for k, m in enumerate(w["ms_all"][q0])]
    nf = {**w, "ms_all": {**w["ms_all"], q0: ms0}, "ctx": {**w["ctx"], "Q25": {**c75, "systems": {
        **c75["systems"], q0: {**c75["systems"][q0], "M_pt": float(np.mean([len(m) for m in ms0]))}}}}}
    a_nf, P_nf = _files(d, "nf", fx)
    rc, so = _out(lambda: run_score({**a_nf, **gone}, P_nf, lambda: nf))
    ck["nonfinite_overlap_faults_label_free_before_key"] = refuses("not finite", wf=lambda: nf) and \
        rc == 2 and so == "FAULT Fault label-free\n"
    ck["refuses_freeze_sha_not_pinned"] = refuses("pinned freeze", freeze_sha="0" * 64)
    ck["refuses_world_pins_not_FREEZE_pins"] = refuses("FREEZE pins", wf=lambda: {**w, "pins": {"x": "y"}})
    ck["refuses_restriction_not_reproducing_slopes"] = refuses("restriction", wf=lambda: bad_m)
    ck["refuses_key_sha_before_labels"] = refuses("KEY_SHA", False, a_over=only_labels_gone, key_sha="0" * 64)
    ck["ok_list_empty_after_key_fault"] = not ak._OK
    ck["refuses_label_sha_mismatch"] = refuses("label file sha", False, mutate=lambda a: Path(a["labels_r2"]).write_text(
        Path(a["labels_r2"]).read_text(encoding="utf-8") + "\n", encoding="utf-8"))
    ck["refuses_row_of_other_annotator"] = refuses("annotator", False, r2_rows=r2_rows + [(r2_rows[0][0], "Y", "PI")])
    ck["refuses_R2_qid_outside_R2_assignment"] = refuses("R2 qid outside", False, r2_rows=r2_rows + [
        (next(q for q, k in fx["key"].items() if k["image"] not in fx["ov"]), "Y", "R2")])
    ck["refuses_PI_qid_outside_base"] = refuses("PI qid outside", False, pi_lines=fx["pi_lines"] + [json.dumps(
        {"qid": "zzzzzzzzzzzz", "label": "Y", "annotator": "PI"})])
    ck["refuses_R2_part1_count_before_labels"] = refuses("R2 part-1 questions", False, a_over=only_labels_gone,
                                                         n_p1=10 ** 6)
    ck["refuses_overlap_targets_count_before_labels"] = refuses("overlap part-1 targets", False,
                                                                a_over=only_labels_gone, n_target=10 ** 6)
    ck["refuses_PI_incomplete_on_overlap"] = refuses("PI part 1 not complete", False, pi_lines=pi_rows)
    ck["refuses_R2_incomplete_on_overlap"] = refuses("R2 not complete", False, r2_rows=[
        r for r in r2_rows if r[0] != min(fx["t"])])


def _custody_checks(ck: dict, d: Path) -> None:
    ck["custody_refuses_key_labels_and_part1_result"] = all(refused(x) for x in (
        d / "key.json", d / "labels_R2.20261113T000000Z.jsonl", "/home/u/vsps_labels/xm600_gold_r2/a.txt",
        "/home/u/vsps_labels_b/a.txt", ac.ROOT / "data/results/a_cert/score/A_CERT_RESULT.json")) and \
        not refused(d / "w" / "r2.jsonl")
    ck["custody_hook_blocks_open_of_key_json"] = _raises(lambda: open(d / "key.json", "w"), "custody")


def main(argv: list) -> int:
    if _audit not in getattr(main, "hooks", ()):
        sys.addaudithook(_audit)
        main.hooks = (_audit,)
    mode = argv[0] if argv else ""
    if mode == "selftest" and len(argv) == 3 and argv[1] == "--out":
        return selftest(Path(argv[2]))
    if mode == "score" and len(argv) == 1 + 2 * len(SCORE_ARGS) and tuple(argv[1::2]) == SCORE_ARGS:
        return run_score(dict(zip((x[2:].replace("-", "_") for x in SCORE_ARGS), argv[2::2])))
    raise SystemExit("usage: a_cert_perann.py selftest --out F | score " + " ".join(f"{x} X" for x in SCORE_ARGS))


if __name__ == "__main__":
    sys.exit(main(sys.argv[1:]))
