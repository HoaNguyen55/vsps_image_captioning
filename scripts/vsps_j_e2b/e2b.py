#!/usr/bin/env python
"""VSPS-J E2b tier 1 (manuscript/prereg/2026-11-01_vsps_j_e2b_tier1/PREREG_DRAFT.md): open 7-8B verifiers with a
3-label output (SUPPORTED / UNCERTAIN / REJECTED) on M-HalDetect val, paired against Vintern-1B (M0 arm A p_yes).

    <m0 venv> -I scripts/vsps_j_e2b/e2b.py plan                                         laptop: ids, counts, shas
    <venv-lb> -I e2b.py rate --data D --images I --out /root/e2b_rate [--with-qwen3]      M8 4090, alone, unscored
    <venv-lb> -I e2b.py probe --cand C --form FA|FB --lang vi|en --data D --images I --out O --cap-h H --rate R
                          [--res R.json (EN only)] [--rerun-of <archived faulted folder of this cell>]
                          [--lost-run <OPS id of the run lost with its host>]
    <m0 venv> -I e2b.py score --data D --runs O --m0-probes P --rate R --res R.json      laptop, once
    <m0 venv> -I e2b.py score-en --data D --runs O --m0-probes P --res R.json --res-en E  laptop, once, winner only
    <any venv with numpy> -I e2b.py selftest                                             CPU, network blocked
Tier 1b-i follows AMENDMENT_1_DRAFT_v1_2.md (348b088, CC-223r3): D1-D11 are marked in the code by their D-number.

Guards are M0's (scripts/vsps_j_m0/m0.py, imported unchanged): pinned inputs, one OUT, a STOP marker on every
FAULT / PROJECTION_STOP / CAP_STOP, refusal to resume or score a stopped run. Models load through
scripts/lb/decode_hf_vlm.py load() / check_snapshot() / fetch() against the B-N1 and C-T1 registries (no remote code).
No M-HalDetect text is written to the repo; the rate run writes timing fields only.
"""
from __future__ import annotations

import argparse
import hashlib
import json
import math
import os
import random
import re
import subprocess
import sys
import time
import traceback
from pathlib import Path

HERE = Path(__file__).resolve().parent
ROOT = HERE.parents[1]
sys.path[:0] = [str(ROOT), str(ROOT / "scripts"), str(ROOT / "scripts/vsps_j_m0"), str(ROOT / "scripts/lb"), str(HERE)]
import m0  # noqa: E402  M0 guards, segments, keyword rule and prompt frame, unchanged (dba7685)

LABEL = "TIER 1 / DEV-EXPLORE (VSPS-J E2b)"
PDIR = ROOT / "manuscript/prereg/2026-11-01_vsps_j_e2b_tier1"
PLAN = PDIR / "e2b_plan.json"
M0DIR = ROOT / "manuscript/prereg/2026-10-31_vsps_j_m0"
M0_LISTS = {"val_ids.txt": "b4d4f35ab7b951fbd4658b670ebf6aecf00cb910fa73753514c104b29ba0f412",
            "dropped_ids.txt": "41306bdbcc672c8104ec4366b137f5f9cce9ecea28f2f59e8c5fd09dc10168bf",
            "selection_excluded_ids.txt": "57195c49c601fe850ce7e06d2d58291076163c8c382399aca3e0eae516bfaef7",
            "karpathy_test_val_ids.txt": "88e40e3cd2ae6dd3bf3c1f514a085cb61a36b503abde298d57a1bb2bc8acd7fb"}
M0_PROBES = "cccd5e0e09ffc40698e82e915f1401882a1e922a98bc8fc9b4f6452eae4c35ce"  # OPS-1031m0done; 32,054 rows
M0_IMAGES = "7a3f3468edea8c385034ed5819b4866bb6699daea9c1d38ad19a8c1532e7c9cf"  # M0 OUT images.sha256 (same pull)
REG = {"bn1": ("manuscript/prereg/2026-10-19_b_n1_vi_leaderboard.json",
               "9ff02dc259258de1add426abd02131f2122e3476a81f9a076066ed6d74906134"),
       "ct1": ("manuscript/prereg/2026-10-30_c_t1/c_t1_registry.json",
               "09e6f90a09735125fed09620b6a1323ef12dafc6bf0a4a4bdf1a4af1087eba3c")}
CANDS = {"qwen25vl_7b": "bn1", "internvl3_8b": "bn1", "aya_vision_8b": "ct1", "qwen3vl_8b": "bn1"}  # run order
OPTIONAL = "qwen3vl_8b"  # only if its smoke passes before the 2.0 GPU-h mark
LB_FREEZE = "685ffe2a0100ce2489cccd77313d366fb1dce4455871a9d82f65aa139fa85784"  # venv-lb, transformers 4.57.6
SEED = 20261101
FORMS, LANGS = ("FA", "FB"), ("vi", "en")
PRIMARY = ("object", "number")
TYPES = ("object", "number", "colour", "attribute", "action", "relation")
GRID = tuple(round(0.05 * i, 2) for i in range(1, 20))  # 0.05 .. 0.95
R_DESIGN, P_TRUE_HI, U_TUNE, U_SEL, RET_MARGIN, TIE = 0.83, 0.90, 0.12, 0.12, -2.0, 0.5
MALFORMED_MASS = 0.5
CAP_RATE_H, QWEN3_MARK_H, N_RATE, N_SMOKE, KEEP_S = 3.0, 2.0, 200, 10, 0.50
B_BOOT, MAX_DROP = 10_000, 0.01
RATE_KEYS = {"cand", "form", "i", "sec", "n_tok", "phase"}  # the only per-probe fields the rate run may write
RATE_SHA = "a57179187068127522d09d1e98cd7b651220fe5417e69c87d1d58495b844ae91"  # D1: the pulled rate.json (OPS-1102e2b-done)
W25_LISTS = PDIR / "e2b_w25_lists.json"  # D11: committed by the gatekeeper with its line in PDIR/SHA256SUMS
# m0.halt return codes (STOP marker "rc"): registered drops vs operator FAULTs (D1, D5b, D6, D7)
RC_FAULT, RC_PROJ, RC_CAP, RC_ENV, RC_PIN, RC_TOKEN, RC_EN_SMOKE = 2, 3, 4, 5, 6, 7, 8
DROP_RC = {RC_FAULT, RC_PROJ, RC_CAP}  # non-finite mass, PROJECTION_STOP, CAP_STOP: registered drop of the cell
ENV_NAMES = {"BackendCompilerFailed", "InductorError", "CompilationError"}  # ponytail: torch compile error names; extend if a new one appears

# ------------------------------------------------------------------------------------------------ frozen rules
COLOUR = re.compile(r"\b(red|blue|green|yellow|white|black|brown|gray|grey|orange|pink|purple|silver|gold|golden"
                    r"|colorful|colored)\b")
ACTION = re.compile(r"\b(holding|riding|carrying|wearing|using|eating|playing|watching|looking at|sitting|standing"
                    r"|walking|lying|leaning|hanging|parked)\b")


def e2b_type(span: str) -> str:
    """Keyword rule v2: M0's rule (first match count > attribute > relation > object) unchanged, then M0 attribute
    splits into colour / attribute and M0 relation into action / relation. object and number equal M0's sets."""
    t, s = m0.claim_type(span), span.lower()
    if t == "count":
        return "number"
    if t == "attribute":
        return "colour" if COLOUR.search(s) else "attribute"
    if t == "relation":
        return "action" if ACTION.search(s) else "relation"
    return "object"


def half(coco_id: int) -> str:
    """Tune/select split (NB-C9): sha256 over the UTF-8 bytes of str(int(id)) + "e2b" (decimal, no padding);
    the LAST hex character of the hexdigest decides: even -> tune, odd -> select."""
    if not isinstance(coco_id, int) or isinstance(coco_id, bool):
        raise TypeError("half() takes the integer COCO id")
    return "tune" if int(hashlib.sha256(f"{coco_id}e2b".encode("utf-8")).hexdigest()[-1], 16) % 2 == 0 else "select"


def prompt(form: str, lang: str, span: str) -> str:
    """F-A vi is M0's frame byte for byte (m0.instruct(m0.question(span))), so the paired Vintern baseline and the
    8B verifiers see the same text. The other three frames are frozen here and pinned by sha in the plan."""
    s = re.sub(r"\s+", " ", span).strip().rstrip(".,;:!?").strip()
    return {("FA", "vi"): m0.instruct(m0.question(span)),
            ("FA", "en"): f'Is it true that "{s}"? Answer only \'yes\' or \'no\'.',
            ("FB", "vi"): f'Có đúng là "{s}" không? Chỉ trả lời đúng một trong ba từ: ĐÚNG, KHÔNG RÕ, SAI.',
            ("FB", "en"): f'Is it true that "{s}"? Answer with exactly one word: SUPPORTED, UNCERTAIN or REJECTED.'
            }[(form, lang)]


LABEL_WORDS = {("FA", "vi"): {"yes": ("Có", "có"), "no": ("Không", "không")},
               ("FA", "en"): {"yes": ("Yes", "yes"), "no": ("No", "no")},
               ("FB", "vi"): {"S": ("ĐÚNG",), "U": ("KHÔNG RÕ",), "R": ("SAI",)},
               ("FB", "en"): {"S": ("SUPPORTED",), "U": ("UNCERTAIN",), "R": ("REJECTED",)}}
U_GUARD = ("không", "Không")  # FB vi: UNCERTAIN's first tokens must differ from those of plain "không"


class Fault(Exception):
    pass


def first_ids(tok, words) -> set:
    """First non-blank token of each word, bare and with a leading space (Vintern _yes_no_ids form)."""
    out = set()
    for w in words:
        for v in (w, " " + w):
            ids = tok.encode(v, add_special_tokens=False)
            out.add(next(i for i in ids if tok.decode([i]).strip()))
    return out


def token_sets(tok, form: str, lang: str) -> dict:
    """{label: sorted first-token ids}; any overlap (or the FB vi U/không clash) is a FAULT for that form."""
    sets = {k: first_ids(tok, w) for k, w in LABEL_WORDS[(form, lang)].items()}
    keys = list(sets)
    for i, a in enumerate(keys):
        for b in keys[i + 1:]:
            if sets[a] & sets[b]:
                raise Fault(f"token sets {a}/{b} overlap for {form} {lang}")
    if (form, lang) == ("FB", "vi") and sets["U"] & first_ids(tok, U_GUARD):
        raise Fault("FB vi: first token of KHÔNG RÕ equals that of không")
    return {k: sorted(v) for k, v in sets.items()}


def decide_fb(m: dict) -> tuple[str, bool]:
    """F-B: argmax of the three label masses; total mass < 0.5 -> UNCERTAIN, flagged malformed."""
    tot = m["S"] + m["U"] + m["R"]
    if tot < MALFORMED_MASS:
        return "U", True
    return max(("S", "U", "R"), key=lambda k: m[k]), False


# ------------------------------------------------------------------------------------------------ data (ids only)
def lists() -> dict:
    out = {}
    for name, want in M0_LISTS.items():
        p = M0DIR / name
        if m0.sha_file(p) != want:
            raise SystemExit(f"FAULT {name}: not the M0 pin")
        out[name] = {int(x) for x in p.read_text().split()}
    return out


def w25_lists(sums: Path = PDIR / "SHA256SUMS", path: Path = W25_LISTS) -> tuple[set, set]:
    """D11: the W25 drop / hold ids of the 663 (AMENDMENT_1 §D.3). The pin is the file's line in the prereg
    SHA256SUMS, added by the gatekeeper commit after the pass (no code change after the pass); refused until then."""
    pin = {n: h for h, n in (ln.split() for ln in sums.read_text().splitlines() if ln.strip())}.get(path.name)
    if not pin or not path.is_file() or m0.sha_file(path) != pin:
        raise SystemExit("REFUSED: e2b_w25_lists.json is not the pinned W25 outcome (G-L3: W25 pass first)")
    d = json.loads(path.read_text(encoding="utf-8"))
    return {int(i) for i in d["drop"]}, {int(i) for i in d["hold"]}


def apply_w25(probe: set, sel: set, held: set, drop: set, hold: set) -> tuple[set, set, set]:
    """D11: drops leave probe, selection and held; holds move from the selection into held. Only the selection (the
    663) can be dropped or held (§D.3 scope), and an id is never both: the count asserts hold only then."""
    out = probe - drop, sel - drop - hold, held | hold
    if len(out[0]) != len(probe) - len(drop) or len(out[1]) != len(sel) - len(drop) - len(hold):
        raise SystemExit("FAULT W25 lists: an id outside the selection set or in both lists (counts do not follow)")
    return out


def sets_and_segments(data: Path, w25: tuple | None = None) -> tuple[dict, list]:
    """M0's probe set (val - dropped, 769), selection set (minus the 106 held, 663) and eligible segments with v2 type
    and half, after the W25 drop / hold lists when given (D11; empty lists change nothing). Text stays in memory only."""
    L = lists()
    probe = probe769 = L["val_ids.txt"] - L["dropped_ids.txt"]
    sel, held = probe - L["selection_excluded_ids.txt"], L["selection_excluded_ids.txt"]
    if w25 is not None:
        probe, sel, held = apply_w25(probe, sel, held, *w25)
    segs = [dict(s, t2=e2b_type(s["text"]), half=half(s["image"]))
            for s in m0.segments(m0.load(data, "val_raw.json"))[0] if s["image"] in probe]
    if w25 is not None:
        print(json.dumps({"after_w25": {"probe": count(segs), "selection": count([s for s in segs if s["image"] in sel])}}))
    return {"probe": probe, "sel": sel, "held": held, "probe769": probe769}, segs


def count(segs: list) -> dict:
    return {"images": len({s["image"] for s in segs}), "segments": len(segs), "inaccurate": sum(s["y"] for s in segs)}


def cmd_plan(a) -> int:
    S, segs = sets_and_segments(a.data)
    op = [s for s in segs if s["image"] in S["sel"]]
    want = {"probe": (769, 16027, 4605), "selection": (663, 13813, 3993)}
    got = {"probe": count(segs), "selection": count(op)}
    if any(tuple(got[k].values()) != v for k, v in want.items()):
        raise SystemExit(f"FAULT counts differ from M0: {got}")
    if m0.sha_file(a.m0_images) != M0_IMAGES:
        raise SystemExit("FAULT M0 images.sha256 pin")
    shas = dict(x.split()[::-1] for x in a.m0_images.read_text().splitlines())
    pool = sorted((s["rec"], s["seg"], s["image"]) for s in op)
    rate = sorted(random.Random(SEED).sample(pool, N_RATE))
    files = sorted({f"COCO_val2014_{i:012d}.jpg" for _r, _s, i in rate})
    rshas = {f: shas[f] for f in files}
    pshas = {f"COCO_val2014_{i:012d}.jpg": shas[f"COCO_val2014_{i:012d}.jpg"] for i in sorted(S["probe"])}
    if m0.sha_refused({m0.image_id(f): h for f, h in pshas.items()}, m0.refused_sets()[1], S["held"]):
        raise SystemExit("FAULT a probe image matches exclusion.json image_sha256 outside the held set")
    if m0.sha_refused({m0.image_id(f): h for f, h in rshas.items()}, m0.refused_sets()[1], set()):
        raise SystemExit("FAULT a rate image matches exclusion.json image_sha256")
    by = lambda ss: {t: {"n": sum(s["t2"] == t for s in ss), "inaccurate": sum(s["y"] for s in ss if s["t2"] == t)}  # noqa: E731
                     for t in TYPES}
    halves = {h: [s for s in op if s["half"] == h] for h in ("tune", "select")}
    plan = {
        "_what": "VSPS-J E2b tier-1 plan: ids, counts and shas only; no M-HalDetect text", "label": LABEL, "seed": SEED,
        "pins": {"m0_lists": M0_LISTS, "val_raw.json": m0.PIN["val_raw.json"], "m0_probes": M0_PROBES,
                 "m0_images": M0_IMAGES, "registries": {k: v[1] for k, v in REG.items()}, "venv_lb_freeze": LB_FREEZE},
        "split_rule": "half(id): sha256(UTF-8 of str(int(id)) + 'e2b'); last hex char even -> tune, odd -> select",
        "split_examples": {str(i): half(i) for i in (139, 285, 632, 724, 776)},
        "counts": {**got, "held_out": count([s for s in segs if s["image"] in S["held"]]),
                   **{h: count(v) for h, v in halves.items()}},
        "types": {"selection": by(op), **{h: by(v) for h, v in halves.items()}, "probe": by(segs)},
        "type_rule_sha256": m0.sha_text(COLOUR.pattern + "\n" + ACTION.pattern),
        "prompts_sha256": {f"{f}_{g}": m0.sha_text(prompt(f, g, "{s}")) for f in FORMS for g in LANGS},
        "label_words": {f"{f}_{g}": v for (f, g), v in LABEL_WORDS.items()},
        "candidates": {k: {"registry": r, **{f: model_entry(k)[f] for f in ("hub_id", "revision")}} for k, r in CANDS.items()},
        "rate": {"n": N_RATE, "probes": [list(x) for x in rate], "images": rshas,
                 "probes_sha256": m0.sha_text(json.dumps(rate))},
        "probe_images": pshas,
    }
    PLAN.write_text(json.dumps(plan, indent=1, ensure_ascii=False) + "\n", encoding="utf-8")
    print(json.dumps({k: plan[k] for k in ("counts", "split_examples")}, indent=1))
    return 0


def model_entry(key: str) -> dict:
    path, want = REG[CANDS[key]]
    if m0.sha_file(ROOT / path) != want:
        raise SystemExit(f"FAULT {path}: registry pin")
    return json.loads((ROOT / path).read_text(encoding="utf-8"))["models"][key]


# ------------------------------------------------------------------------------------------------ GPU guards
def env_info() -> dict:
    """D7: interpreter and library versions for launch.json, read from package metadata (no import); cuda = the
    torch wheel's local tag (e.g. cu121). None when a package is not installed."""
    from importlib.metadata import PackageNotFoundError, version

    out = {"python": sys.version}
    for pkg in ("torch", "transformers"):
        try:
            out[pkg] = version(pkg)
        except PackageNotFoundError:
            out[pkg] = None  # recorded; a real load then fails as ENV_FAULT (rc 5)
    out["cuda"] = out["torch"].partition("+")[2] or None if out["torch"] else None
    return out


def rerun_record(prev: Path, out: Path) -> dict:
    """W1 (AMENDMENT_1 §F protocol): an operator-FAULT re-run names the archived faulted folder of the same cell. Its
    STOP rc and shas go into launch.json. Refused if the folder is missing, anywhere under the runs folder (NB-1), of
    another cell, not stopped, itself a re-run (one re-run per cell), or a registered stop (W4: only rc 5 ENV_FAULT,
    rc 6 PIN_FAULT and a vi rc 7 TOKEN_FAULT are operator FAULTs; a registered stop is final, never re-run)."""
    stop, lj = prev / m0.STOP, prev / "launch.json"
    if prev.resolve().is_relative_to(out.resolve().parent) or not (prev.name == out.name or prev.name.startswith(out.name + ".")):
        raise SystemExit(f"REFUSED --rerun-of {prev}: not this cell's folder archived outside the runs folder")
    if not stop.is_file() or not lj.is_file():
        raise SystemExit(f"REFUSED --rerun-of {prev}: no stopped run there")
    if json.loads(lj.read_text()).get("rerun_of"):
        raise SystemExit(f"REFUSED --rerun-of {prev}: it is a re-run itself (one re-run per cell; §F: to a judge)")
    rc = json.loads(stop.read_text())["rc"]
    if not (rc in (RC_ENV, RC_PIN) or (rc == RC_TOKEN and out.name.endswith("_vi"))):
        raise SystemExit(f"REFUSED --rerun-of {prev}: rc {rc} is a registered stop, not an operator FAULT (§F)")
    return {"path": str(prev), "rc": rc, "stop_sha256": m0.sha_file(stop), "launch_sha256": m0.sha_file(lj)}


def stopped_marker(out: Path) -> Path:
    """NB-6: written beside the cell folder whenever the cell stops; it outlives an archive of the folder."""
    return out.parent / f".{out.name}.stopped"


def prep_out(out: Path, rerun_of: Path | None = None, lists_sha: str | None = None, lost: str | None = None) -> Path:
    """One OUT; launch.json t0 is written before any fetch, so the cap clock includes downloads; one resume.
    rerun_of: the archived faulted folder of an operator-FAULT re-run (fresh OUT and t0; §F). lost: the OPS id of a
    run lost with its host; this relaunch IS the cell's one §F re-run (CC-225r2 Ruling 4), so any rc 5/6/7 on it goes
    to a judge and nothing may re-run it. lists_sha: the e2b_w25_lists.json sha the run is bound to (NB-4)."""
    if rerun_of and lost:
        raise SystemExit("REFUSED: --rerun-of and --lost-run together")
    if out.resolve().is_relative_to(ROOT):
        raise SystemExit("REFUSED --out inside the repo")
    out.mkdir(parents=True, exist_ok=True)
    m0.refuse_if_stopped(out)
    lf = out / "launch.json"
    rec = None
    if rerun_of and not lf.exists():  # one re-run per cell: a marker beside the cell folder (the archive stays unchanged)
        used = out.parent / f".{out.name}.rerun"
        if used.exists():
            raise SystemExit(f"REFUSED --rerun-of: {out.name} was re-run already (one re-run per cell; §F: to a judge)")
        rec = rerun_record(rerun_of, out)
    elif lost and not lf.exists():
        rec = {"lost_run": lost, "rc": "LOST"}
    mk = stopped_marker(out)
    if mk.exists():  # NB-6: a stopped cell launches or resumes only as the declared re-run of that exact stop
        declared = rec if not lf.exists() else (json.loads(lf.read_text()).get("rerun_of") or {})
        if (declared or {}).get("stop_sha256") != json.loads(mk.read_text())["stop_sha256"]:
            raise SystemExit(f"REFUSED: {out.name} stopped before; only --rerun-of its archived STOP may launch (§F)")
    if rec:
        (out.parent / f".{out.name}.rerun").write_text(json.dumps(rec) + "\n")
    L = json.loads(lf.read_text()) if lf.exists() else {
        "t0": time.time(), "starts": 0, "rerun_of": rec,
        "w25_lists_sha256": lists_sha, **env_info()}
    if L["starts"] >= 2:
        raise SystemExit("REFUSED: already resumed once")
    L["starts"] += 1
    lf.write_text(json.dumps(L))
    return out


def elapsed_h(out: Path) -> float:
    return (time.time() - json.loads((out / "launch.json").read_text())["t0"]) / 3600


def gpu_busy(n_apps: int, cuda_on: bool) -> bool:
    """Count rule, not PIDs (a container's PIDs need not match nvidia-smi's): no compute app before this process
    touches CUDA, at most one (this process) after."""
    return n_apps > (1 if cuda_on else 0)


def gpu_alone(where: str) -> None:
    """The rate run must be alone on the GPU (CC-215r2 ruling 3): any other compute process -> FAULT."""
    import torch

    q = subprocess.run(["nvidia-smi", "--query-compute-apps=pid", "--format=csv,noheader"],
                       capture_output=True, text=True, check=True).stdout
    n = sum(1 for x in q.splitlines() if x.strip())
    if gpu_busy(n, torch.cuda.is_initialized()):
        raise Fault(f"GPU not alone {where}: {n} compute process(es)")


def projected_h(used_h: float, remaining: int, mean_s: float) -> float:
    """v2 section 5.3: GPU-h used since the first t0 (resume included) + remaining probes x running MEAN s/probe."""
    return used_h + remaining * mean_s / 3600


def proj_mean(rows: list, rate_mean: float) -> float:
    """D5 = AMENDMENT_1 C.1 (CC-223 W1): the rate mean_s until the cell's TOTAL completed probes, across all starts,
    reach N_RATE; then the mean of all completed probes excluding the first probe of each start; if that set is
    empty, the rate mean_s. rows: [(start, sec)] in write order."""
    if len(rows) < N_RATE:
        return rate_mean
    seen: set = set()
    rest = []
    for start, sec in rows:
        if start in seen:
            rest.append(sec)
        seen.add(start)
    return sum(rest) / len(rest) if rest else rate_mean


def smoke_ok(m: dict) -> bool:
    """Registered smoke rule (PREREG section 6): finite masses and label mass >= 0.5."""
    return all(math.isfinite(v) for v in m.values()) and sum(m.values()) >= MALFORMED_MASS


def redact(s: str) -> str:
    """D7: no token in any record: the HF_TOKEN value and any hf_ token string are replaced; cut to 4 kB."""
    tok = os.environ.get("HF_TOKEN")
    s = s.replace(tok, "<redacted>") if tok else s
    return re.sub(r"hf_[A-Za-z0-9]{30,}", "<redacted>", s)[:4096]


def is_env_error(e: BaseException) -> bool:
    """D7 / CC-218r2 W3: an import or compile error is an operator FAULT (rc 5), never a registered drop."""
    return isinstance(e, ImportError) or type(e).__name__ in ENV_NAMES


def error_record(e: BaseException) -> dict:
    return {"type": type(e).__name__, "msg": redact(str(e)), "traceback": redact(traceback.format_exc())}


def load_cand(key: str, hub: Path):
    """Fetch (inside the cap clock), sha-check every pinned file, load through the LB loader (no remote code)."""
    import decode_hf_vlm as LB

    m = model_entry(key)
    snap = hub / key
    try:  # LB raises SystemExit on a pin mismatch; as a Fault it writes the STOP marker (section 8)
        LB.fetch({"models": {key: m}}, key, snap)
        LB.check_snapshot(m, snap)
    except SystemExit as e:
        raise Fault(f"{key} snapshot: {e}") from None
    return LB.load(m, snap, "cuda:0")


def make_probe(proc, net, form: str, lang: str):
    """One forward pass; first-token label masses from the softmax at the last position (= one greedy step)."""
    import torch

    tok = getattr(proc, "tokenizer", proc)
    sets = token_sets(tok, form, lang)

    def probe(image, text: str) -> tuple[dict, int]:
        msgs = [[{"role": "user", "content": [{"type": "image", "image": image}, {"type": "text", "text": text}]}]]
        enc = proc.apply_chat_template(msgs, add_generation_prompt=True, tokenize=True, return_dict=True,
                                       return_tensors="pt", padding=True).to(net.device, net.dtype)
        with torch.no_grad():
            pr = torch.softmax(net(**enc).logits[0, -1].float(), dim=-1)
        return {k: pr[v].sum().item() for k, v in sets.items()}, int(enc["input_ids"].shape[1])
    return probe, sets


def image_loader(folder: Path):
    from PIL import Image

    cache: dict = {}

    def img(iid: int):  # ponytail: one-image cache; probes are grouped by image in every loop here
        if cache.get("id") != iid:
            cache.update(id=iid, im=Image.open(folder / f"COCO_val2014_{iid:012d}.jpg").convert("RGB"))
        return cache["im"]
    return img


def check_images(folder: Path, want: dict) -> None:
    bad = [f for f, h in want.items() if not (folder / f).is_file() or m0.sha_file(folder / f) != h]
    extra = {p.name for p in folder.iterdir()} - set(want)  # D8: the staged folder is exactly the wanted set
    if bad or extra:
        raise SystemExit(f"FAULT {len(bad)} staged images missing or not the plan sha, {len(extra)} extra files")


def cuda_free() -> None:
    """Called at the top of every attempt: the previous candidate's model (or a failed attempt's traceback) is
    unreferenced by then, so its memory returns before the next load."""
    import gc

    import torch

    gc.collect()
    torch.cuda.empty_cache()


# ------------------------------------------------------------------------------------------------ rate (GPU)
def rate_row(**kw) -> dict:
    if set(kw) - RATE_KEYS:
        raise Fault(f"rate row carries non-timing fields {sorted(set(kw) - RATE_KEYS)}")
    return kw


def summarise(rows: list, form: str) -> dict:
    s = [r["sec"] for r in rows if r["form"] == form and r["phase"] == "rate"]
    if not s:
        return {"n": 0, "keep": False}
    mean = sum(s) / len(s)
    return {"n": len(s), "mean_s": mean, "median_s": sorted(s)[len(s) // 2], "keep": mean <= KEEP_S}


def time_form(key, form, probe, out, items, spans, img, fh) -> dict:
    """Smoke (first 10 items: finite masses, label mass >= 0.5 on all 10; booleans only), then the 200 timed items."""
    rows = []
    for phase, todo in (("smoke", items[:N_SMOKE]), ("rate", items)):
        ok = 0
        for i, (r, s, iid) in enumerate(todo):
            if elapsed_h(out) > CAP_RATE_H:
                raise TimeoutError
            t = time.perf_counter()
            m, n_tok = probe(img(iid), prompt(form, "vi", spans[(r, s)]))
            sec = time.perf_counter() - t
            ok += smoke_ok(m)
            rows.append(rate_row(cand=key, form=form, i=i, sec=sec, n_tok=n_tok, phase=phase))
            m0.append(fh, rows[-1])
        fh.flush()
        if phase == "smoke" and ok < N_SMOKE:
            return {"status": "SMOKE_FAULT", "smoke_ok": ok}
        if phase == "smoke" and key == OPTIONAL and elapsed_h(out) > QWEN3_MARK_H:
            return {"status": "DROPPED_SMOKE_AFTER_2H_MARK"}
    return {"status": "DONE", **summarise(rows, form), "n_tok_median": sorted(r["n_tok"] for r in rows)[len(rows) // 2]}


def run_cand(key, out, plan, spans, img, hub, fh) -> dict:
    import torch

    t = time.time()
    proc, net = load_cand(key, hub)
    rec = {"load_s": time.time() - t, "forms": {}}
    torch.cuda.reset_peak_memory_stats()
    for form in FORMS:
        try:
            probe, _sets = make_probe(proc, net, form, "vi")
        except Fault as e:  # token-set clash: this form is not run for this candidate (v2 section 2.4)
            rec["forms"][form] = {"status": "TOKEN_FAULT", "reason": str(e)}
            continue
        rec["forms"][form] = time_form(key, form, probe, out, plan["rate"]["probes"], spans, img, fh)
    rec["vram_peak_gb"] = torch.cuda.max_memory_allocated() / 2**30
    rec["image_prefix_reuse"] = False
    return rec


def cmd_rate(a) -> int:
    plan = json.loads(PLAN.read_text(encoding="utf-8"))  # every cheap check runs before t0 is written
    check_images(a.images, plan["rate"]["images"])
    segs = {(s["rec"], s["seg"]): s for s in m0.segments(m0.load(a.data, "val_raw.json"))[0]}
    spans = {(r, s): segs[(r, s)]["text"] for r, s, _i in plan["rate"]["probes"]}
    if any(segs[(r, s)]["image"] != i for r, s, i in plan["rate"]["probes"]):
        raise SystemExit("FAULT rate probes differ from val_raw.json")
    for k in CANDS:
        model_entry(k)
    out = prep_out(a.out)
    sf = out / "rate.json"
    summary = json.loads(sf.read_text()) if sf.exists() else {"label": LABEL, "keep_s": KEEP_S, "cap_h": CAP_RATE_H,
                                                              "cands": {}}
    img = image_loader(a.images)
    cands = [k for k in CANDS if k != OPTIONAL or a.with_qwen3]
    with open(out / "rate.jsonl", "a", encoding="utf-8") as fh:
        for key in cands:
            prev = summary["cands"][key] if key in summary["cands"] else {"final": False, "tries": 0}
            if prev["final"]:
                continue
            if key == OPTIONAL and elapsed_h(out) > QWEN3_MARK_H:
                summary["cands"][key] = {"final": True, "status": "DROPPED_PAST_2H_MARK"}
                continue
            tries = prev["tries"]
            while True:
                cuda_free()
                try:
                    gpu_alone(f"before {key}")
                    rec = run_cand(key, out, plan, spans, img, a.hub, fh)
                    gpu_alone(f"after {key}")
                    summary["cands"][key] = {"final": True, "tries": tries + 1, "status": "DONE", **rec}
                    break
                except TimeoutError:
                    sf.write_text(json.dumps(summary, indent=1))
                    return m0.halt(out, 4, f"CAP_STOP at {key}: {elapsed_h(out):.2f} GPU-h")
                except Fault as e:
                    sf.write_text(json.dumps(summary, indent=1))
                    return m0.halt(out, 2, f"FAULT {e}")
                except Exception as e:  # OOM or load error: one retry inside the cap, then the candidate is dropped
                    if is_env_error(e):  # D7: an environment error is an operator FAULT, not a registered drop
                        sf.write_text(json.dumps(summary, indent=1))
                        return m0.halt(out, RC_ENV, f"ENV_FAULT {type(e).__name__}: {redact(str(e))}")
                    tries += 1
                    summary["cands"][key] = {"final": tries >= 2, "tries": tries, "status": "ERROR",
                                             "error": type(e).__name__, **error_record(e)}
                    sf.write_text(json.dumps(summary, indent=1))
                    if tries >= 2:
                        break
            sf.write_text(json.dumps(summary, indent=1))
    summary["elapsed_h"] = elapsed_h(out)
    sf.write_text(json.dumps(summary, indent=1))
    print(json.dumps({"status": "DONE", "elapsed_h": summary["elapsed_h"]}))
    return 0


# ------------------------------------------------------------------------------------------------ probe (GPU, tier 1b-i)
def cmd_probe(a) -> int:
    if m0.sha_file(a.rate) != RATE_SHA:
        raise SystemExit("REFUSED: --rate is not the pulled rate.json (a5717918)")
    try:
        rate = json.loads(a.rate.read_text())["cands"][a.cand]["forms"][a.form]
    except KeyError:
        raise SystemExit(f"REFUSED: no rate record for {a.cand} {a.form}") from None
    if rate["status"] != "DONE" or not rate["keep"]:
        raise SystemExit(f"REFUSED: {a.cand} {a.form} is not kept by the rate run")
    if a.lang == "en" and (not a.res or json.loads(a.res.read_text())["winner"] != f"{a.cand}|{a.form}"):
        raise SystemExit("REFUSED: the EN frame runs for the vi winner only (--res names it)")
    S, segs = sets_and_segments(a.data, w25_lists())
    want = json.loads(PLAN.read_text(encoding="utf-8"))["probe_images"]
    check_images(a.images, {f: h for f, h in want.items() if m0.image_id(f) in S["probe"]})  # D8 + D11
    model_entry(a.cand)
    out = prep_out(a.out / f"{a.cand}_{a.form}_{a.lang}", a.rerun_of, m0.sha_file(W25_LISTS), a.lost_run)
    return guarded(out, lambda: probe_cell(a, out, S, segs, rate["mean_s"]))


def guarded(out: Path, fn) -> int:
    """D7: an environment error -> operator FAULT (rc 5); anything else -> error.json (redacted), then a crash
    (which keeps its one resume)."""
    try:
        rc = fn()
    except Exception as e:
        if not is_env_error(e):
            (out / "error.json").write_text(json.dumps(error_record(e)))
            raise
        rc = m0.halt(out, RC_ENV, f"ENV_FAULT {type(e).__name__}: {redact(str(e))}")
    if (out / m0.STOP).exists():  # NB-6: the stop outlives an archive of the folder
        stopped_marker(out).write_text(json.dumps({"rc": rc, "stop_sha256": m0.sha_file(out / m0.STOP)}) + "\n")
    return rc


def probe_cell(a, out: Path, S: dict, segs: list, rate_mean: float) -> int:
    order = [i for i in m0.image_order(S["probe769"]) if i in S["probe"]]  # W2: M0's order over the 769, minus drops
    by: dict = {}
    for s in segs:
        by.setdefault(s["image"], []).append(s)
    pf = out / "probes.jsonl"
    old = [json.loads(x) for x in pf.read_text(encoding="utf-8").splitlines()] if pf.exists() else []
    done = {(r["rec"], r["seg"]) for r in old}
    rows = [(r.get("start", 1), r["sec"]) for r in old]
    start = json.loads((out / "launch.json").read_text())["starts"]
    if elapsed_h(out) >= a.cap_h:  # D6: pre-load (pre-fetch) cap check
        return m0.halt(out, RC_CAP, f"CAP_STOP before load: {elapsed_h(out):.2f} GPU-h >= cap {a.cap_h}")
    try:
        proc, net = load_cand(a.cand, a.hub)
    except Fault as e:  # D1: snapshot pin mismatch = operator FAULT
        return m0.halt(out, RC_PIN, f"PIN_FAULT {e}")
    try:
        probe, sets = make_probe(proc, net, a.form, a.lang)
    except Fault as e:  # D1: token-set clash (vi: operator FAULT, second clash on a re-run = drop; EN: arm not run)
        return m0.halt(out, RC_TOKEN, f"TOKEN_FAULT {e}")
    (out / "token_sets.json").write_text(json.dumps(sets))
    img = image_loader(a.images)
    if a.lang == "en" and not done:  # D5b: registered 10-item EN smoke at load, booleans only
        first = [s for iid in order for s in by.get(iid, [])][:N_SMOKE]
        if not all(smoke_ok(probe(img(s["image"]), prompt(a.form, "en", s["text"]))[0]) for s in first):
            return m0.halt(out, RC_EN_SMOKE, "EN_SMOKE_FAULT: label mass < 0.5 or non-finite on an EN smoke item")
    with open(pf, "a", encoding="utf-8") as fh:
        for n, iid in enumerate(order, 1):
            todo = [s for s in by.get(iid, []) if (s["rec"], s["seg"]) not in done]
            if not todo:
                continue
            pj = projected_h(elapsed_h(out), len(segs) - len(done), proj_mean(rows, rate_mean))  # D5
            if pj > a.cap_h:
                return m0.halt(out, RC_PROJ, f"PROJECTION_STOP before image {n}: {pj:.2f} GPU-h > cap {a.cap_h}", n)
            for s in todo:
                t = time.perf_counter()
                m, n_tok = probe(img(iid), prompt(a.form, a.lang, s["text"]))
                sec = time.perf_counter() - t
                if not all(math.isfinite(v) for v in m.values()):
                    return m0.halt(out, RC_FAULT, f"FAULT non-finite mass at rec {s['rec']} seg {s['seg']}", n)
                m0.append(fh, {"rec": s["rec"], "seg": s["seg"], "image": iid, "n_img": n, "mass": m, "n_tok": n_tok,
                               "sec": sec, "start": start})
                done.add((s["rec"], s["seg"]))
                rows.append((start, sec))
            fh.flush()
            os.fsync(fh.fileno())
    (out / "probes.jsonl.sha256").write_text(f"{m0.sha_file(pf)}  probes.jsonl\n")
    print(json.dumps({"status": "DONE", "elapsed_h": elapsed_h(out), "probes": len(done)}))
    return 0


# ------------------------------------------------------------------------------------------------ rules (score)
def key(s: dict) -> tuple:
    return s["rec"], s["seg"]


def recall(rej, y) -> float:
    ny = sum(y)
    return sum(r and t for r, t in zip(rej, y)) / ny if ny else float("nan")


def band(p: list, y: list) -> tuple[float, float]:
    """F-A band rule on the tune half for one type: t_lo = smallest grid value with strict recall >= 0.83; t_hi from
    hi_rule. No feasible t_lo (or no gold-false probe) -> one threshold 0.5 (empty band)."""
    if not sum(y):
        return 0.5, 0.5
    tlo = next((t for t in GRID if recall([v <= t for v in p], y) >= R_DESIGN), None)
    return (0.5, 0.5) if tlo is None else (tlo, hi_rule(p, y, tlo))


def hi_rule(p: list, y: list, tlo: float) -> float:
    """t_hi = smallest grid value >= t_lo with P(gold true | p >= t_hi) >= 0.90, else t_lo (empty band); while the
    tune UNCERTAIN share > 12 %, t_hi steps down the grid toward t_lo (the cap wins over the 0.90 floor)."""
    def ptrue(t):
        k = [not yy for v, yy in zip(p, y) if v >= t]
        return sum(k) / len(k) if k else 0.0
    thi = next((t for t in GRID if t >= tlo and ptrue(t) >= P_TRUE_HI), tlo)
    steps = [t for t in GRID if tlo <= t < thi][::-1] + [tlo]
    while p and sum(tlo < v < thi for v in p) / len(p) > U_TUNE and thi > tlo:
        thi = steps.pop(0)
    return thi


def band_label(v: float, tlo: float, thi: float) -> str:
    return "R" if v <= tlo else "S" if v >= thi else "U"


def match_lo(p: list, y: list, target: float) -> float:
    """Vintern t_lo: the lowest distinct tune p_yes whose strict recall reaches the E2b tune recall (-inf if 0)."""
    if not target > 0 or not sum(y):
        return float("-inf")
    return next((v for v in sorted(set(p)) if recall([x <= v for x in p], y) >= target), max(p))


def metrics(lab: list, y: list) -> dict:
    nR, nf, nt = sum(v == "R" for v in lab), sum(y), len(y) - sum(y)
    pct = lambda a, b: 100 * a / b if b else float("nan")  # noqa: E731
    return {"n": len(y), "n_false": nf,
            "prec_R": pct(sum(v == "R" and t for v, t in zip(lab, y)), nR),
            "recall": pct(sum(v == "R" and t for v, t in zip(lab, y)), nf),
            "loose_recall": pct(sum(v != "S" and t for v, t in zip(lab, y)), nf),
            "retention": pct(sum(v == "S" and not t for v, t in zip(lab, y)), nt),
            "prec_S": pct(sum(v == "S" and not t for v, t in zip(lab, y)), sum(v == "S" for v in lab)),
            "U": pct(sum(v == "U" for v in lab), len(y))}


def macro(per: dict, k: str) -> float:
    """Fixed a priori: equal-weight mean over the primary types that have the metric defined."""
    v = [per[t][k] for t in PRIMARY if t in per and not math.isnan(per[t][k])]
    return sum(v) / len(v) if v else float("nan")


def macro_pair(E: dict, V: dict, k: str) -> tuple[float, list]:
    """D3 (clarifies PREREG l.229): the config - Vintern macro difference over only the primary types where BOTH
    systems have k defined. Returns (difference, types used)."""
    ts = [t for t in PRIMARY if t in E and t in V and not math.isnan(E[t][k]) and not math.isnan(V[t][k])]
    return (sum(E[t][k] - V[t][k] for t in ts) / len(ts) if ts else float("nan")), ts


def vote(a: str, b: str) -> str:
    """PA2: REJECTED if either rejects, SUPPORTED if both support, else UNCERTAIN."""
    return "R" if "R" in (a, b) else "S" if a == b == "S" else "U"


def pick(rows: dict) -> tuple:
    """Selection rule on the select half. rows: {config: {"dprec", "U", "dret", "cand", "form", "vote", "tune_recall"}}.
    Feasible: U <= 12 and dret >= -2.0 (point estimates) and, D4 (amends PREREG l.226), tune strict recall >= R_DESIGN
    on each primary type (undefined = NaN = infeasible). Max dprec; within 0.5 points prefer F-B, then Aya, then
    CANDS order. PA2 vote configs only if no single-model config is feasible. N9: if Qwen2.5-VL-7B wins, the
    verifier for VSPS-generated records is the best feasible non-Qwen2.5-VL single config.
    Returns (winner or None, vsps_record_verifier or None)."""
    order = list(CANDS)

    def best(keys):
        ok = [k for k in keys if rows[k]["U"] <= 100 * U_SEL and rows[k]["dret"] >= RET_MARGIN
              and not math.isnan(rows[k]["dprec"]) and all(rows[k]["tune_recall"][t] >= R_DESIGN for t in PRIMARY)]
        if not ok:
            return None
        top = max(rows[k]["dprec"] for k in ok)
        return min((k for k in ok if top - rows[k]["dprec"] < TIE),
                   key=lambda k: (rows[k]["form"] != "FB", rows[k]["cand"] != "aya_vision_8b",
                                  order.index(rows[k]["cand"]), -rows[k]["dprec"]))
    single = [k for k in rows if not rows[k]["vote"]]
    win = best(single) or best([k for k in rows if rows[k]["vote"]])
    rec = best([k for k in single if rows[k]["cand"] != "qwen25vl_7b"]) if win and rows[win]["cand"] == "qwen25vl_7b" else win
    return win, rec


def boot(tables, n_img: int, seed: int = SEED, B: int = B_BOOT):
    """Image-cluster bootstrap: multinomial image weights (= resampling images with replacement, all probes of an
    image together, both systems). Returns the B weighted sums of the per-image count rows."""
    import numpy as np

    W = np.random.default_rng(seed).multinomial(n_img, [1 / n_img] * n_img, size=B)
    return W @ np.asarray(tables, dtype=float)


NCNT = 10  # per image and primary type: RyE, RE, RyV, RV, StE, StV, n_true, UE, n, n_false


def per_image_counts(segs: list, fE, fV) -> list:
    imgs = sorted({s["image"] for s in segs})
    acc = {i: {t: [0] * NCNT for t in PRIMARY} for i in imgs}
    for s in segs:
        if s["t2"] in PRIMARY:
            e, v, y, c = fE(s), fV(s), s["y"], acc[s["image"]][s["t2"]]
            for j, add in enumerate((e == "R" and y, e == "R", v == "R" and y, v == "R", e == "S" and not y,
                                     v == "S" and not y, not y, e == "U", 1, y)):
                c[j] += int(add)
    return [sum((acc[i][t] for t in PRIMARY), []) for i in imgs]


def ci_from_table(rows, B: int = B_BOOT, seed: int = SEED) -> tuple:
    """K1 (TIER1C O1 §9): paired_ci's per-replicate statistics and its dropped mask, before the FAULT check, so the
    O1 ppass can count an undefined inner run as not passing instead of aborting. No logic change."""
    import numpy as np

    T = boot(rows, len(rows), seed, B).reshape(B, len(PRIMARY), NCNT)
    RyE, RE, RyV, RV, StE, StV, nt, UE, n, nf = (T[:, :, j] for j in range(NCNT))
    bad = ((RE == 0) | (RV == 0) | (nt == 0) | (nf == 0)).any(axis=1)
    with np.errstate(divide="ignore", invalid="ignore"):
        st = {"dprec": 100 * (RyE / RE - RyV / RV).mean(axis=1), "U": 100 * (UE / n).mean(axis=1),
              "dret": 100 * ((StE - StV) / nt).mean(axis=1), "drecall": 100 * ((RyE - RyV) / nf).mean(axis=1)}
    return st, bad


def paired_ci(rows: list, B: int = B_BOOT, seed: int = SEED) -> dict:
    """Ratio estimators per type inside each replicate, then macro, then E - V; 95 % percentile intervals.
    Replicates where a primary type has no REJECTED for either system are dropped and counted; > 1 % -> FAULT."""
    import numpy as np

    st, bad = ci_from_table(rows, B, seed)
    if bad.mean() > MAX_DROP:
        raise Fault(f"{bad.mean():.3%} bootstrap replicates undefined")
    return {"B": B, "seed": seed, "dropped": int(bad.sum()),
            **{k: [float(np.percentile(v[~bad], 2.5)), float(np.percentile(v[~bad], 97.5))] for k, v in st.items()}}


# ------------------------------------------------------------------------------------------------ score (laptop)
def fa_p(m: dict) -> float:
    return m["yes"] / max(1e-12, m["yes"] + m["no"])


def tune_of(op: list, t: str) -> list:
    return [s for s in op if s["t2"] == t and s["half"] == "tune"]


def fit_band(pf, op: list) -> dict:
    return {t: band([pf(s) for s in tune_of(op, t)], [s["y"] for s in tune_of(op, t)]) for t in TYPES}


def config_fn(mass: dict, form: str, op: list):
    """(label function, thresholds) of one E2b config; F-A thresholds fit on the tune half of the selection set."""
    if form == "FB":
        return (lambda s: decide_fb(mass[key(s)])[0]), None
    thr = fit_band(lambda s: fa_p(mass[key(s)]), op)
    return (lambda s: band_label(fa_p(mass[key(s)]), *thr[s["t2"]])), thr


def tune_recall(f, op: list) -> dict:
    """Tune strict recall per type; NaN when the type has no gold-false tune probe (undefined; D4)."""
    return {t: (recall([f(s) == "R" for s in tune_of(op, t)], [s["y"] for s in tune_of(op, t)])
                if sum(s["y"] for s in tune_of(op, t)) else float("nan")) for t in TYPES}


def vintern_fn(pv: dict, op: list, R: dict):
    """Vintern matched to the config's tune strict recall per type, then the same t_hi rule and 12 % cap."""
    thr = {}
    for t in TYPES:
        p, y = [pv[key(s)] for s in tune_of(op, t)], [s["y"] for s in tune_of(op, t)]
        lo = match_lo(p, y, R[t])
        thr[t] = (lo, hi_rule(p, y, lo)) if p else (0.5, 0.5)
    return lambda s: band_label(pv[key(s)], *thr[s["t2"]])


def table(f, segs: list) -> dict:
    return {t: metrics([f(s) for s in segs if s["t2"] == t], [s["y"] for s in segs if s["t2"] == t]) for t in TYPES}


def classify(d: Path, keys: set, lang: str) -> tuple[str, dict | None]:
    """D1: a run folder is DONE (sha + exact cover of keys) or holds a STOP marker read by its rc. A registered stop
    is never opened (no probes.jsonl read): vi rc 2/3/4, and a vi TOKEN_FAULT on a re-run whose archived first
    fault was also a TOKEN_FAULT (7 -> 7, W1), are DROPPED_STOP;
    EN rc 2/3/4/7/8 is EN_NOT_RUN. rc 5 ENV_FAULT, rc 6 PIN_FAULT, a first vi TOKEN_FAULT and an incomplete folder
    with no STOP are operator matters: REFUSED (re-run under the AMENDMENT_1 §F protocol; on a re-run: to a judge)."""
    stop = d / m0.STOP
    if stop.exists():
        rc = json.loads(stop.read_text())["rc"]
        if lang == "en" and rc in DROP_RC | {RC_TOKEN, RC_EN_SMOKE}:
            return "EN_NOT_RUN", None
        prior = (json.loads((d / "launch.json").read_text()).get("rerun_of") or {}).get("rc")
        if lang == "vi" and (rc in DROP_RC or (rc == RC_TOKEN and prior == RC_TOKEN)):
            return "DROPPED_STOP", None
        if prior is not None:
            raise SystemExit(f"REFUSED {d.name}: second operator FAULT (rc {prior} then rc {rc}); to a judge (§F)")
        raise SystemExit(f"REFUSED {d.name}: operator FAULT (STOP rc {rc}); re-run under the operator-FAULT protocol")
    pf, sf = d / "probes.jsonl", d / "probes.jsonl.sha256"
    if not sf.is_file() or sf.read_text().split()[0] != m0.sha_file(pf):
        raise SystemExit(f"REFUSED {d.name}: incomplete (no STOP, no matching probes.jsonl.sha256)")
    rows = {(r["rec"], r["seg"]): r["mass"] for r in map(json.loads, pf.read_text(encoding="utf-8").splitlines())}
    if set(rows) != keys:
        raise SystemExit(f"REFUSED {d.name}: coverage differs from the probe keys")
    return "DONE", rows


def load_runs(runs: Path, keys: set, lang: str) -> tuple[dict, dict]:
    """({(cand, form): {(rec, seg): mass}} for DONE folders, {(cand, form): status} for every folder) of one language."""
    out, status = {}, {}
    for d in sorted(runs.glob(f"*_F?_{lang}")):
        cand, form, _l = d.name.rsplit("_", 2)
        status[(cand, form)], rows = classify(d, keys, lang)
        if rows is not None:
            out[(cand, form)] = rows
    return out, status


def ablation(form: str, mass: dict, f3, R: dict, op: list, sel: list) -> dict:
    """NB-C4, descriptive: the winner forced binary at its tune strict recall, same backbone. F-A: REJECTED iff
    p <= t_lo, else SUPPORTED (same REJECTED set). F-B: q = m_R / (m_R + m_S); REJECTED iff q >= cut, cut = the
    highest tune q whose strict recall reaches the 3-label tune recall of that type."""
    if form == "FA":
        return {"three_label": table(f3, sel), "binary": table(lambda s: "R" if f3(s) == "R" else "S", sel)}
    q = lambda s: mass[key(s)]["R"] / max(1e-12, mass[key(s)]["R"] + mass[key(s)]["S"])  # noqa: E731
    cut = {}
    for t in TYPES:
        tu, y = tune_of(op, t), [s["y"] for s in tune_of(op, t)]
        cut[t] = next((v for v in sorted({q(s) for s in tu}, reverse=True)
                       if sum(y) and recall([q(s) >= v for s in tu], y) >= R[t]), float("inf"))
    return {"three_label": table(f3, sel), "binary": table(lambda s: "R" if q(s) >= cut[s["t2"]] else "S", sel)}


def kept_cells(rate: Path) -> set:
    """D1: the keep=true candidate x form cells of the sha-pinned rate.json."""
    if m0.sha_file(rate) != RATE_SHA:
        raise SystemExit("REFUSED: --rate is not the pulled rate.json (a5717918)")
    rj = json.loads(rate.read_text())
    return {(c, f) for c, v in rj["cands"].items() for f, r in v.get("forms", {}).items() if r.get("keep")}


def once(guard: Path) -> None:
    """D2: a scoring step runs once; its guard file exists after the first run."""
    if guard.exists():
        raise SystemExit(f"REFUSED: {guard.name} exists (scored once)")


def m0_pv(path: Path, keys: set) -> dict:
    if m0.sha_file(path) != M0_PROBES:
        raise SystemExit("FAULT M0 probes.jsonl is not cccd5e0e")
    pv = {(r["rec"], r["seg"]): r["p_yes"] for r in map(json.loads, path.read_text().splitlines()) if r["arm"] == "A"}
    if not keys <= set(pv):  # D11: M0 arm A covers the remaining keys (a superset is allowed)
        raise SystemExit("FAULT M0 arm-A rows do not cover the probe segments")
    return pv


def cmd_score(a) -> int:
    once(a.runs / "SCORED.json")
    kept = kept_cells(a.rate)
    cells = {tuple(d.name.rsplit("_", 2)[:2]) for d in a.runs.glob("*_F?_vi")}
    if cells != kept:  # D1: the vi run folders are exactly the kept cells (checked before any data is read)
        raise SystemExit(f"REFUSED: run folders {sorted(cells)} differ from the kept cells {sorted(kept)}")
    S, segs = sets_and_segments(a.data, w25_lists())
    keys = {key(s) for s in segs}
    pv = m0_pv(a.m0_probes, keys)
    runs, status = load_runs(a.runs, keys, "vi")
    op = [s for s in segs if s["image"] in S["sel"]]  # the selection set; the held images never fit anything
    sel = [s for s in op if s["half"] == "select"]
    cfg = {f"{c}|{f}": config_fn(m, f, op) for (c, f), m in runs.items()}
    vthr = fit_band(lambda s: pv[key(s)], op)
    vown = lambda s: band_label(pv[key(s)], *vthr[s["t2"]])  # noqa: E731  Vintern's own band (PA2 input only)
    for k in [k for k in cfg if k.startswith("aya_vision_8b|")]:
        cfg[f"PA2 vintern+{k}"] = ((lambda s, fa=cfg[k][0]: vote(vown(s), fa(s))), None)
    res = {"label": LABEL, "cells": {f"{c}|{f}": st for (c, f), st in status.items()}, "configs": {}}
    rows, fns = {}, {}
    for name, (f, thr) in cfg.items():
        R = tune_recall(f, op)
        vf = vintern_fn(pv, op, R)
        E, V = table(f, sel), table(vf, sel)
        (dprec, tp), (dret, tr), (drec, tc) = (macro_pair(E, V, k) for k in ("prec_R", "retention", "recall"))
        rows[name] = {"cand": name.split("|")[0].removeprefix("PA2 vintern+"), "form": name.split("|")[-1],
                      "vote": name.startswith("PA2"), "dprec": dprec, "U": macro(E, "U"), "dret": dret,
                      "drecall": drec, "tune_recall": R}
        res["configs"][name] = {**rows[name], "types_used": {"dprec": tp, "dret": tr, "drecall": tc},
                                "thresholds": thr, "e2b": E, "vintern": V}
        fns[name] = (f, vf, R)
    win, res["vsps_record_verifier"] = pick(rows)
    res["winner"] = win
    if win:
        f, vf, R = fns[win]
        res["winner_ci_select"] = paired_ci(per_image_counts(sel, f, vf))
        res["winner_ci_select_note"] = ("selection-biased, descriptive; tier 2 confirms; Vintern select half not fresh "
                                        "(M0 scored all 663)")  # D9
        res["full_split_same_thresholds"] = {"e2b": table(f, segs), "vintern": table(vf, segs),
                                             "held_out_106": table(f, [s for s in segs if s["image"] in S["held"]]),
                                             "held_n_images": len(S["held"])}  # NB-6: 106 + W25 holds
        if not rows[win]["vote"]:
            c, fm = win.split("|")
            res["ablation_binary"] = ablation(fm, runs[(c, fm)], f, R, op, sel)
    a.res.write_text(json.dumps(res, indent=1, default=str) + "\n", encoding="utf-8")
    guard = {"res_sha256": m0.sha_file(a.res), "rate_sha256": RATE_SHA, "w25_lists_sha256": m0.sha_file(W25_LISTS),
             "cells": res["cells"], "utc": time.time()}
    (a.runs / "SCORED.json").write_text(json.dumps(guard) + "\n")
    print(json.dumps({k: res[k] for k in ("winner", "vsps_record_verifier")}
                     | {"SCORED.json_sha256 (OPS line)": m0.sha_file(a.runs / "SCORED.json")}))
    return 0


def cmd_score_en(a) -> int:
    """D2: the descriptive EN-frame arm of the vi winner, once, after the one vi score (never re-runs pick())."""
    once(a.runs / "SCORED_EN.json")
    gf = a.runs / "SCORED.json"
    if not gf.is_file() or json.loads(gf.read_text())["res_sha256"] != m0.sha_file(a.res):
        raise SystemExit("REFUSED: no SCORED.json for this res.json")
    res = json.loads(a.res.read_text())
    win = res["winner"]
    if not win or res["configs"][win]["vote"]:
        raise SystemExit("REFUSED: no single-model winner, so no EN arm")
    c, fm = win.split("|")
    if [d.name for d in sorted(a.runs.glob("*_F?_en"))] != [f"{c}_{fm}_en"]:
        raise SystemExit(f"REFUSED: the only EN folder must be {c}_{fm}_en")
    S, segs = sets_and_segments(a.data, w25_lists())
    keys = {key(s) for s in segs}
    pv = m0_pv(a.m0_probes, keys)
    runs, status = load_runs(a.runs, keys, "en")
    out = {"label": LABEL, "winner": win, "en_status": status[(c, fm)]}
    if (c, fm) in runs:  # same rules on its own tune fit
        mass = runs[(c, fm)]
        op = [s for s in segs if s["image"] in S["sel"]]
        sel = [s for s in op if s["half"] == "select"]
        fe = config_fn(mass, fm, op)[0]
        out["winner_en_descriptive"] = {"e2b": table(fe, sel), "vintern": table(vintern_fn(pv, op, tune_recall(fe, op)), sel)}
        out["en_malformed_share"] = 100 * sum(sum(m.values()) < MALFORMED_MASS for m in mass.values()) / len(mass)
    a.res_en.write_text(json.dumps(out, indent=1, default=str) + "\n", encoding="utf-8")
    (a.runs / "SCORED_EN.json").write_text(json.dumps({"res_en_sha256": m0.sha_file(a.res_en), "utc": time.time()}) + "\n")
    print(json.dumps({"en_status": out["en_status"], "SCORED_EN.json_sha256": m0.sha_file(a.runs / "SCORED_EN.json")}))
    return 0


# ------------------------------------------------------------------------------------------------ main
def main() -> int:
    ap = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    sp = ap.add_subparsers(dest="cmd", required=True)
    sp.add_parser("selftest")
    p = sp.add_parser("plan")
    p.add_argument("--data", type=Path, default=ROOT / m0.MH)
    p.add_argument("--m0-images", type=Path, required=True, help="M0 OUT images.sha256 (7a3f3468), pins the rate images' bytes")
    for name in ("rate", "probe"):
        g = sp.add_parser(name)
        g.add_argument("--data", type=Path, required=True, help="folder with val_raw.json (A-N3 pin)")
        g.add_argument("--images", type=Path, required=True)
        g.add_argument("--out", type=Path, required=True)
        g.add_argument("--hub", type=Path, required=True, help="folder for the pinned snapshots (one per candidate)")
    sp.choices["rate"].add_argument("--with-qwen3", action="store_true")
    pr = sp.choices["probe"]
    pr.add_argument("--cand", choices=list(CANDS), required=True)
    pr.add_argument("--form", choices=FORMS, required=True)
    pr.add_argument("--lang", choices=LANGS, required=True)
    pr.add_argument("--cap-h", type=float, required=True, help="block cap, set by the post-rate amendment")
    pr.add_argument("--rate", type=Path, required=True, help="the pulled rate.json (a5717918)")
    pr.add_argument("--res", type=Path, help="EN only: the vi res.json whose winner is this cell")
    pr.add_argument("--rerun-of", type=Path, help="operator-FAULT re-run: the archived faulted folder of this cell")
    pr.add_argument("--lost-run", help="relaunch after a lost host: the OPS id of the lost run (its one §F re-run)")
    for name in ("score", "score-en"):
        s = sp.add_parser(name)
        s.add_argument("--data", type=Path, default=ROOT / m0.MH)
        s.add_argument("--runs", type=Path, required=True)
        s.add_argument("--m0-probes", type=Path, required=True)
        s.add_argument("--res", type=Path, required=True)
    sp.choices["score"].add_argument("--rate", type=Path, required=True, help="the pulled rate.json (a5717918)")
    sp.choices["score-en"].add_argument("--res-en", type=Path, required=True)
    a = ap.parse_args()
    if a.cmd == "selftest":
        import test_e2b

        return test_e2b.main()
    return {"plan": cmd_plan, "rate": cmd_rate, "probe": cmd_probe, "score": cmd_score, "score-en": cmd_score_en}[a.cmd](a)


if __name__ == "__main__":
    sys.exit(main())
