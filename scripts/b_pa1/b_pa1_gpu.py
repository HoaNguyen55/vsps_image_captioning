#!/usr/bin/env python3
"""B-PA1-T1 HB-T1 GPU blocks S, A1-decode, A1-score, A2, A3, H, A4 (PREREG_DRAFT_v3_1.md e9b30ca7 §4.3-§4.4, §6.4,
§7, §8.4, §9.1; R5 9cb21917 E-7, E-12; R6 0b55d5f8 §I.3-§I.6; R6 Part II 0c5f919b §2-§3). TIER 1 / DEV-EXPLORE (B-PA1-T1).
DRAFT, not read. Driven by b_pa1_job.sh; every command below is one job step or a job helper.

    python3 -I -B scripts/b_pa1/b_pa1_gpu.py selftest        CPU only, fake models, synthetic files (laptop and host)
    ... hostcheck --venv main|legacy                          host selftest T1-T7, T9 on a synthetic image (GPU)
    ... cap-init --cap-h 28|22 --r-host R --fee F --t0 UTC [--used-sec S --used-w-sec SW]   CAP.json once (rental line values)
    ... steps --mode s|a1decode|a1score|rest                  "<step> <venv>" lines in the registered order
    ... ledger start|end STEP [--rc N] | left [--w]            the GPU-h ledger (R6 §I.3 rule 0, RB3)
    ... inputs --set a|w --nblk N                              slice A / W set = MAN + frame (reading 1)
    ... run STEP [--mapf SHA] [--hin SHA]                      one block step
    ... money-stop --balance B --threshold T | resume --cause guard|machine --cc CC-x [--close-sec N] | wipe --dir D

Host layout: ~/b_pa1_out (B_PA1_OUT): CAP.json, ledger.jsonl, in/ (frame, h_input.jsonl), snaps/<model>.path,
out/<mode>/*.jsonl, logs/. Images only in /dev/shm/b_pa1_hb/<set> (B_PA1_HB; R6 §I.4). The host never holds the map or
any gold: it verifies every proposition and writes yes-probabilities; B's mapped-only score is a laptop step.
Logs (stdout of every step) carry ids and counts only; model outputs go only to out/*.jsonl (T9).
"""
from __future__ import annotations

import argparse
import contextlib
import hashlib
import json
import os
import re
import sys
import time
import unicodedata
from fractions import Fraction
from pathlib import Path

HERE = Path(__file__).resolve().parent
sys.path.insert(0, str(HERE))
import b_pa1 as B  # noqa: E402  LABEL, write_new, must_refuse, read_frame (stdlib only)

REG_PATH = HERE / "b_pa1_registry.json"
FRAME_SHA = "863ad3e90577c37dac2d2384062239fc71e747c167700d2566926ba2d69b7234"  # LOG l.1226
W_FREEZE = "1a639a50adf550c50c6dfe284146e279b2a2bf2a716ade743e9eb357ccbf0778"  # cenfeat_venv_freeze.txt (R5 §D.2)
W_CAP_SEC = 3600  # block W cap and per-step timeout 1.0 GPU-h (R6 §I.6, H-46, C-8)
PA3_RC, CORE_RC = 3, 13
FINAL = ("CAP_STOP.json", "MONEY_STOP.json", "PA3.json", "CORE_STOP.json")  # every one refuses every later step
TRIM_ORDER = ("a4", "h", "a3")  # dropped first -> last (v3.1 l.505 as R5 E-12)
N_SLICE = 2000
HEX64 = re.compile(r"[0-9a-f]{64}")
ID_RX = re.compile(r"[A-Za-z0-9_.:+-]{1,80}")
FREE = {"caption", "text", "props"}  # model outputs and transformed captions: out files only, never a log
OUT_KEYS = {"id", "cap", "tr", "cfg", "j", "n_new", "cap_hit", "sec", "parse", "n_props", "p_yes", "abstain", "top1",
            "ev", "p_digits", "cos", "score", "trunc"} | FREE
VN_MARKS = frozenset("\u0306\u0302\u031b\u0300\u0301\u0309\u0303\u0323")  # breve circumflex horn + 5 tone marks


def env_path(name: str, default: Path) -> Path:
    return Path(os.environ.get(name) or default)


def O() -> Path:  # noqa: N802
    return env_path("B_PA1_OUT", Path.home() / "b_pa1_out")


def HB() -> Path:  # noqa: N802
    return env_path("B_PA1_HB", Path("/dev/shm/b_pa1_hb"))


def fault(msg: str):
    raise SystemExit(f"FAULT: {msg}")


def utc() -> str:
    return time.strftime("%Y-%m-%dT%H:%M:%SZ", time.gmtime())


def sha_bytes(b: bytes) -> str:
    return hashlib.sha256(b).hexdigest()


def blob_hashes(p: Path) -> tuple[str, str]:
    """sha256 and git-blob SHA-1 (= sha1(b'blob <size>\\0' + bytes)) in one pass, as c_pvr.blob_hashes."""
    n = p.stat().st_size
    h2, h1 = hashlib.sha256(), hashlib.sha1(b"blob %d\0" % n)
    with open(p, "rb") as f:
        for c in iter(lambda: f.read(1 << 20), b""):
            h2.update(c)
            h1.update(c)
    return h2.hexdigest(), h1.hexdigest()


# ---------------------------------------------------------------------------------------------- registry, prompts
def load_reg(p: Path = REG_PATH) -> dict:
    r = json.loads(p.read_text(encoding="utf-8"))
    if r.get("schema") != "vsps.b_pa1.registry.v1":
        fault("not a b_pa1 registry")
    for name, pr in r["prompts"].items():
        if unicodedata.normalize("NFC", pr["text"]) != pr["text"] or sha_bytes(pr["text"].encode()) != pr["sha256"]:
            fault(f"prompt {name} is not NFC or differs from its sha")
    ms = r["models"]
    for k, m in ms.items():
        if not re.fullmatch(r"[0-9a-f]{40}", m["revision"]) or m["venv"] not in ("main", "legacy"):
            fault(f"model {k}: revision or venv")
    if [ms[k]["walk"] for k in r["walk"]] != list(range(1, len(r["walk"]) + 1)):
        fault("walk order")
    if ms[r["decomposer"]]["lineage"]["L"] != ms[r["verifier"]]["lineage"]["L"]:
        fault("decomposer L differs from the verifier L: the walk's verifier check no longer covers v3.1 l.165")
    return r


def render(text: str, **kw: str) -> str:
    """Fill {name} slots by plain replacement (prompts hold JSON braces); every slot filled, no extra name."""
    slots = set(re.findall(r"\{(caption|prop|word|classes|cls)\}", text))
    if slots != set(kw):
        fault(f"prompt slots {sorted(slots)} != {sorted(kw)}")
    for k, v in kw.items():
        text = text.replace("{" + k + "}", v)
    return text


# ---------------------------------------------------------------------------------------------- gate and walk (§4.3-4.4)
def is_vn(text: str) -> bool:
    """A Vietnamese-only letter (ă â đ ê ô ơ ư) or a tone mark, upper or lower case, NFC or NFD input."""
    t = unicodedata.normalize("NFD", text.lower())
    return "đ" in t or any(c in VN_MARKS for c in t)


def gate_share(caps: list[str], n: int) -> Fraction:
    if len(caps) != n:
        fault(f"gate needs {n} captions, got {len(caps)}")
    return Fraction(sum(map(is_vn, caps)), n)


def gate_pass(share: Fraction, reg: dict) -> bool:
    return share >= Fraction(reg["gate"]["pass_share"])


def determined(m: dict) -> bool:
    lin = m["lineage"]
    return all(isinstance(lin.get(x), str) and lin[x] and lin[x] != "undetermined" for x in ("V", "L"))


def clash(a: dict, b: dict) -> bool:
    """§4.1: disjoint iff V differ and L differ; an undetermined lineage clashes with every model (N6)."""
    return not (determined(a) and determined(b)) or a["lineage"]["V"] == b["lineage"]["V"] or \
        a["lineage"]["L"] == b["lineage"]["L"]


def desk(reg: dict, key: str, accepted: list[str]) -> str | None:
    """None = run the gate; else the skip reason (§4.3: pin, Rule S, resolver, disjointness)."""
    m, ms = reg["models"][key], reg["models"]
    if not m["files"] or not m["revision"]:
        return "pin"
    if m["safetensors_total"] is None or m["safetensors_total"] > reg["rule_s_max_params"]:
        return "rule_s"
    if not determined(m):
        return "lineage"
    if clash(m, ms[reg["verifier"]]):
        return "verifier"
    for a in accepted:
        if clash(m, ms[a]):
            return f"accepted:{a}"
    return None


def walk_state(reg: dict, rows: list[dict]) -> tuple[list[str], set[str]]:
    seen, acc = set(), []
    for r in rows:
        if r["key"] in seen or r["key"] not in reg["walk"]:
            fault(f"walk record repeats or names a non-candidate: {r['key']}")
        seen.add(r["key"])
        acc += [r["key"]] if r["decision"] == "accept" else []
    order = [k for k in reg["walk"] if k in seen]
    if order != reg["walk"][:len(order)]:
        fault("walk records out of the registered order")
    return acc, seen


def a4_models(reg: dict, accepted: list[str]) -> list[str]:
    """§4.3 l.207-208: the verifier's own family, then the first two of the pool not accepted in the walk."""
    return [reg["a4_first"]] + [k for k in reg["a4_pool"] if k not in accepted][:2]


# ---------------------------------------------------------------------------------------------- token sets (§7.1 N5)
def first_ids(encode, words: list[str]) -> set[int]:
    out = set()
    for w in words:
        ids = encode(w)
        if not ids:
            fault("a yes/no word encodes to no token")
        out.add(ids[0])
    return out


def yn_sets(encode, words: dict) -> tuple[frozenset, frozenset]:
    y, n = first_ids(encode, words["Y"]), first_ids(encode, words["N"])
    y, n = y - (y & n), n - (y & n)
    if not y or not n:
        fault("a yes/no id set is empty after removing shared ids")
    return frozenset(y), frozenset(n)


def yes_prob(sub: dict, top: int, y: frozenset, n: frozenset) -> dict:
    """At the first answer position: sub = softmax probabilities of the Y and N ids, top = the top-1 id over the
    whole vocabulary. p_yes = Σp(Y) / (Σp(Y) + Σp(N)); abstain iff top is in neither set; yes iff p_yes >= 0.5."""
    py, pn = sum(sub[i] for i in y), sum(sub[i] for i in n)
    return {"p_yes": py / (py + pn) if py + pn > 0 else None, "abstain": top not in y and top not in n,
            "top1": "Y" if top in y else "N" if top in n else "other"}


def digit_ids(encode, digits: list[str]) -> list[int]:
    ids = [encode(d) for d in digits]
    if any(len(x) != 1 for x in ids) or len({x[0] for x in ids}) != len(digits):
        fault("a digit 0-9 is not one distinct token (T5)")
    return [x[0] for x in ids]


def digit_ev(sub: dict, top: int, ids: list[int]) -> dict:
    """0-9 expected value over the ten single-digit tokens, renormalised (§7.1 J-b, J-c); ids in digit order."""
    p = [sub[i] for i in ids]
    s = sum(p)
    return {"ev": sum(d * x for d, x in enumerate(p)) / s if s > 0 else None, "p_digits": s,
            "top1": "digit" if top in ids else "other"}


# ---------------------------------------------------------------------------------------------- decomposition output
def objects_in(text: str) -> tuple[list, bool]:
    """Every complete top-level {...} in the text, by a brace scanner that respects JSON strings; True if the text
    is exactly one JSON array (parse 'ok'), else the objects recovered ('partial' / 'fail')."""
    s = text.strip()
    try:
        whole = json.loads(s)
        if isinstance(whole, list):
            return whole, True
    except ValueError:
        pass
    out, depth, start, instr, esc = [], 0, None, False, False
    for i, c in enumerate(s):
        if instr:
            esc, instr = (False, instr) if esc else (c == "\\", c != '"')
            continue
        if c == '"':
            instr = True
        elif c == "{":
            depth, start = depth + 1, i if depth == 0 else start
        elif c == "}" and depth:
            depth -= 1
            if depth == 0:
                try:
                    out.append(json.loads(s[start:i + 1]))
                except ValueError:
                    pass
    return out, False


def props_of(text: str, types: list[str]) -> tuple[list[dict], str]:
    items, whole = objects_in(text)
    props = [{"type": x["type"], "text": x["text"].strip(), "object": str(x.get("object") or "").strip()}
             for x in items if isinstance(x, dict) and x.get("type") in types and isinstance(x.get("text"), str)
             and x["text"].strip()]
    bad = len(items) - len(props)
    return props, ("ok" if whole and not bad else "partial" if props else "fail")


# ---------------------------------------------------------------------------------------------- files
def rec_ok(rec: dict) -> dict:
    for k, v in rec.items():
        if k not in OUT_KEYS:
            fault(f"output key {k!r} not whitelisted")
        if k in FREE:
            continue
        for x in v if isinstance(v, list) else [v]:
            if isinstance(x, str) and not ID_RX.fullmatch(x):
                fault(f"value under {k!r} is not an id")
    return rec


def untorn(p: Path) -> int:
    """RS-2: a file whose last line has no newline keeps its whole lines; the torn tail moves to an exclusive
    <file>.torn.<UTC> file (never deleted). Returns the number of bytes moved."""
    if not p.exists():
        return 0
    b = p.read_bytes()
    if not b or b.endswith(b"\n"):
        return 0
    cut = b.rfind(b"\n") + 1
    B.write_new(p.with_name(f"{p.name}.torn.{utc()}"), b[cut:])
    with open(p, "r+b") as f:
        f.truncate(cut)
    return len(b) - cut


def rows_of(p: Path) -> list[dict]:
    if not p.exists():
        return []
    b = p.read_bytes()
    if b and not b.endswith(b"\n"):
        fault(f"{p.name} ends in a torn line (run resume first)")
    return [json.loads(x) for x in b.decode("utf-8").splitlines()]


def key_of(r: dict) -> tuple:
    return (r.get("cap"), r["id"], r.get("tr"))


class Out:
    """Append-only jsonl with skip-done by (cap, id, tr); each row flushed + fsynced (the selftest turns fsync off)."""
    SYNC = True

    def __init__(self, p: Path):
        p.parent.mkdir(parents=True, exist_ok=True)
        self.p, self.done = p, {key_of(r) for r in rows_of(p)}
        self.f = open(p, "a", encoding="utf-8")

    def __contains__(self, k) -> bool:
        return k in self.done

    def write(self, rec: dict) -> None:
        k = key_of(rec)
        if k in self.done:
            fault(f"duplicate row {k[:2]}")
        self.f.write(json.dumps(rec_ok(rec), ensure_ascii=False, sort_keys=True) + "\n")
        self.f.flush()
        if self.SYNC:
            os.fsync(self.f.fileno())
        self.done.add(k)

    def close(self) -> None:
        self.f.close()


class Mem:
    """In-memory sink with Out's interface: block-S smoke outputs never reach a file (v3.1 §9.1 row S)."""

    def __init__(self):
        self.rows = []

    def __contains__(self, k) -> bool:
        return any(key_of(r) == k for r in self.rows)

    def write(self, rec: dict) -> None:
        self.rows.append(rec_ok(rec))


def wipe(d: Path, log: Path) -> int:
    """R6 §I.4 item 4: delete every file of the set dir, then the dirs; one log line (utc, folder, files, manifest
    count). rc 1 if the file count is not manifest lines + 1 (the trap still deletes)."""
    man = d / "MANIFEST.sha256"
    n_man = len(man.read_text().splitlines()) if man.is_file() else -1
    files = [p for p in d.rglob("*") if not p.is_dir()]
    for p in files:
        p.unlink()
    for p in sorted((p for p in d.rglob("*") if p.is_dir()), key=lambda x: -len(x.parts)):
        p.rmdir()
    d.rmdir()
    with open(log, "a") as f:
        f.write(f"{utc()}\t{d}\t{len(files)}\t{n_man}\n")
    return 0 if len(files) == n_man + 1 else 1


# ---------------------------------------------------------------------------------------------- inputs (reading 1)
def frame_rows() -> list[tuple[int, str]]:
    b = (O() / "in/o365_train_frame.tsv").read_bytes()
    if sha_bytes(b) != FRAME_SHA:
        fault("frame file differs from 863ad3e9")
    return B.read_frame(b)


def manifest_names(d: Path) -> list[str]:
    return [ln[66:] for ln in (d / "MANIFEST.sha256").read_text().splitlines()]


def slice_a(frame: list, names: list[str]) -> list[tuple[int, str]]:
    """Slice A in slice order = the frame rows whose file is in the slice-A MANIFEST, in frame order (the frame is
    the slice order and slice A is the first 2,000 survivors along it, v3.1 §5.2)."""
    want = set(names)
    rows = [r for r in frame if r[1] in want]
    if len(rows) != N_SLICE or len(want) != N_SLICE or len(names) != N_SLICE:
        fault(f"slice-A manifest has {len(names)} names, {len(rows)} in the frame; {N_SLICE} needed")
    return rows


def w_block_ok(frame: list, names: list[str], block: int = 500) -> int:
    """The W set is a block-aligned run of the frame order (first push: blocks 0..k-1; §9.3: the next blocks)."""
    fn = [f for _, f in frame]
    if not names:
        fault("empty W manifest")
    i = fn.index(names[0]) if names[0] in fn else -1
    if i < 0 or i % block or fn[i:i + len(names)] != names or (len(names) % block and i + len(names) != len(fn)):
        fault("W manifest is not a block-aligned run of the frame order")
    return (i + len(names)) // block


# ---------------------------------------------------------------------------------------------- GPU-h ledger (RB3)
def cap_doc() -> dict:
    p = O() / "CAP.json"
    if not p.is_file():
        fault("CAP.json missing (cap-init at setup)")
    return json.loads(p.read_text())


def ledger() -> list[dict]:
    return rows_of(O() / "ledger.jsonl")


def ledger_add(rec: dict) -> None:
    with open(O() / "ledger.jsonl", "a") as f:
        f.write(json.dumps(rec, sort_keys=True) + "\n")
        f.flush()
        os.fsync(f.fileno())


def open_step(rows: list[dict]) -> dict | None:
    st = None
    for r in rows:
        if r["ev"] == "start":
            if st is not None:
                fault("ledger: two starts without an end")
            st = r
        elif r["ev"] == "end":
            if st is None or r["step"] != st["step"]:
                fault("ledger: end without its start")
            st = None
    return st


def used_sec(rows: list[dict], w_only: bool = False) -> int:
    return sum(r["sec"] for r in rows if r["ev"] == "end" and (not w_only or r["step"].startswith("w.")))


def left_sec(w: bool = False, in_step: bool = False) -> int:
    """GPU-h left in seconds. Between steps no step may be open; inside a step (s.trim) its own elapsed time counts."""
    c, rows = cap_doc(), ledger()
    st = open_step(rows)
    if st and not in_step:
        fault("ledger has an open step (machine loss or a killed job): close it with `resume`")
    left = c["cap_sec"] - c["used_before_sec"] - used_sec(rows) - (int(time.monotonic() - st["m"]) + 1 if st else 0)
    return min(left, W_CAP_SEC - c["used_w_before_sec"] - used_sec(rows, True)) if w else left  # F-3: HB-T1's W seconds


def markers() -> None:
    for m in FINAL:
        if (O() / m).exists():
            fault(f"{m} exists: a cap, money, PA3 or core stop is final")


def next_read_h(balance: int, threshold: int, burn: int) -> int:
    """CC-295 N13 / run doc RB9: hours to the next panel read; hourly once the balance is within 6 h x Σ r_live of
    the money-stop threshold, else 6-hourly (run doc §5.4); 0 = at or below the threshold: write MONEY_STOP.json."""
    if balance <= threshold:
        return 0
    return 1 if balance - threshold <= 6 * burn else 6


@contextlib.contextmanager
def scratch(prefix: str = "b_pa1_st_"):
    """A fresh dir under the system temp dir; afterwards each file and link is removed by name and each dir by rmdir
    (no recursive delete call; a link to a dir is unlinked, never entered)."""
    import tempfile
    d = Path(tempfile.mkdtemp(prefix=prefix))
    try:
        yield d
    finally:
        if d.parent.resolve() != Path(tempfile.gettempdir()).resolve() or not d.name.startswith(prefix):
            fault(f"scratch cleanup refused for {d}")
        for top, dirs, files in os.walk(d, topdown=False):
            for f in files:
                os.unlink(os.path.join(top, f))
            for x in dirs:
                q = os.path.join(top, x)
                os.unlink(q) if os.path.islink(q) else os.rmdir(q)
        d.rmdir()


# ---------------------------------------------------------------------------------------------- trim (§9.1 l.510-511)
def project(rates: dict, a4: list[str]) -> dict:
    """Projected seconds per block from the block-S rates (per caption). a1 = A1-decode + A1-score."""
    r, n, cap4 = rates, N_SLICE, 4 * N_SLICE
    score = r["e_d1"] + r["v_d1v1"] + r["ja"] + r["clip"]
    return {"a1": sum(n * r["dec"][c] for c in r["accepted"]) + cap4 * score,
            "a2": cap4 * (r["jb"] + r["jc"]),
            "a3": cap4 * (r["e_d2"] + r["v_d2v1"] + r["v_d1v2"]),
            "h": r["n_h"] * (r["e_d1"] + r["v_d1v1"]),
            "a4": sum(n * (r["dec"][m] + score) for m in a4)}


def trim(proj: dict, left: int) -> dict:
    kept = [b for b in reversed(TRIM_ORDER)]  # a3, h, a4

    def need(ks):
        return Fraction(5, 4) * Fraction(sum(Fraction(proj[b]) for b in ("a1", "a2", *ks)))
    dropped = []
    for b in TRIM_ORDER:
        if need(kept) <= left:
            break
        kept.remove(b)
        dropped.append(b)
    return {"cap_left_sec": left, "projected_sec": proj, "kept": kept, "dropped": dropped,
            "core_fits": need([]) <= left, "need_sec": float(need(kept))}


# ---------------------------------------------------------------------------------------------- steps (registered order)
def steps(mode: str, reg: dict) -> list[tuple[str, str]]:
    ms = reg["models"]
    if mode == "s":
        return [(f"s.gate.{k}", ms[k]["venv"]) for k in reg["walk"]] + \
            [("s.a4rate", "main"), ("s.smoke", "main"), ("s.trim", "main")]
    acc = accepted_list(reg)
    t = json.loads((O() / "out/s/TRIM.json").read_text()) if (O() / "out/s/TRIM.json").is_file() else {}
    if t.get("core_fits") is not True:  # CC-295 W3: no block after S unless S's trim let the core run
        fault("TRIM.json missing or core_fits is not true (block S's trim decides first)")
    if mode == "a1decode":
        return [(f"a1decode.decode.{k}", ms[k]["venv"]) for k in acc]
    if mode == "a1score":
        return [(f"a1score.{s}", "main") for s in ("decomp_d1", "verify_d1v1", "ja", "clip")]
    if mode == "rest":
        out = [("rest.jb", "main"), ("rest.jc", "main")]
        out += [(f"rest.{s}", "main") for s in ("decomp_d2", "verify_d2v1", "verify_d1v2")] if "a3" in t["kept"] else []
        out += [(f"rest.{s}", "main") for s in ("h_decomp", "h_verify")] if "h" in t["kept"] else []
        if "a4" in t["kept"]:
            out += [(f"rest.a4dec.{m}", ms[m]["venv"]) for m in a4_models(reg, acc)]
            out += [(f"rest.a4_{s}", "main") for s in ("decomp_d1", "verify_d1v1", "ja", "clip")]
        return out
    fault(f"unknown mode {mode}")


def accepted_list(reg: dict) -> list[str]:
    p = O() / "out/s/ACCEPT.json"
    if not p.is_file():
        fault("no ACCEPT.json (block S first)")
    a = json.loads(p.read_text())["accepted"]
    if len(a) != reg["gate"]["n_accept"]:
        fault("ACCEPT.json does not hold 4 captioners")
    return a


# ---------------------------------------------------------------------------------------------- model layer (lazy)
class Models:
    """Real loaders; the selftest swaps in fakes. Each loader returns a callable; free() releases the GPU."""

    def __init__(self, reg: dict):
        self.reg = reg

    def snap(self, key: str) -> Path:
        m = self.reg["models"][key]
        p = Path((O() / "snaps" / f"{key}.path").read_text().strip())
        for f, (kind, want) in m["files"].items():
            s256, s1 = blob_hashes(p / f)
            if (s256 if kind == "lfs" else s1) != want:
                fault(f"{key} {f} differs from its pin; nothing is loaded")
        if any(q.suffix in (".bin", ".pt", ".pth", ".ckpt") and q.name not in m["files"] for q in p.iterdir()):
            fault(f"{key}: an unpinned pickle file is in the snapshot")
        return p

    def captioner(self, key: str):
        from b_pa1_models import captioner
        return captioner(key, self.reg, self.snap(key))

    def decomposer(self):
        from b_pa1_models import decomposer
        return decomposer(self.reg, self.snap(self.reg["decomposer"]))

    def scorer(self):
        from b_pa1_models import scorer
        return scorer(self.reg, self.snap(self.reg["verifier"]))

    def clip(self):
        from b_pa1_models import clip
        return clip(self.reg, self.snap("mclip"), self.snap("xlmr"))

    def image(self, path: Path):
        from PIL import Image
        return Image.open(path).convert("RGB")

    def free(self, obj) -> None:
        from b_pa1_models import free
        free(obj)


# ---------------------------------------------------------------------------------------------- arms
def cap_rows(paths: list[Path]) -> list[dict]:
    return [r for p in paths for r in rows_of(p)]


def decode_into(M: Models, key: str, ids: list[tuple[int, str]], out: Out, img_dir: Path) -> int:
    gen, n = M.captioner(key), 0
    prompt = M.reg["prompts"]["captioner"]["text"]
    for i, f in ids:
        if (key, i, None) in out:
            continue
        t = time.time()
        text, n_new = gen(M.image(img_dir / f), prompt)
        out.write({"id": i, "cap": key, "caption": text, "n_new": n_new,
                   "cap_hit": n_new >= M.reg["decode"]["max_new_tokens"], "sec": round(time.time() - t, 4)})
        n += 1
    M.free(gen)
    return n


def decomp_into(M: Models, cfg: str, src: list[dict], out: Out) -> int:
    dec, todo = M.decomposer(), [r for r in src if key_of(r) not in out]
    tpl, bs = M.reg["prompts"][cfg]["text"], M.reg["decomposer_decode"]["batch"]
    for j in range(0, len(todo), bs):
        part, t = todo[j:j + bs], time.time()
        res = dec([render(tpl, caption=r.get("text", r.get("caption"))) for r in part])
        sec = round((time.time() - t) / len(part), 4)
        for r, (raw, n_new) in zip(part, res):
            props, parse = props_of(raw, M.reg["prop_types"])
            out.write({"id": r["id"], "cap": r["cap"], **({"tr": r["tr"]} if "tr" in r else {}), "cfg": cfg,
                       "props": props, "parse": parse, "n_new": n_new,
                       "cap_hit": n_new >= M.reg["decomposer_decode"]["max_new_tokens"], "sec": sec})
    M.free(dec)
    return len(todo)


def verify_into(M: Models, vcfg: str, src: list[dict], out: Out, img: dict, img_dir: Path) -> int:
    sc, n = M.scorer(), 0
    tpl, lang = M.reg["prompts"][vcfg]["text"], M.reg["prompt_lang"][vcfg]
    y, no = sc.yn(lang)
    for r in src:
        if key_of(r) in out:
            continue
        t, image, res = time.time(), M.image(img_dir / img[r["id"]]), []
        for k, p in enumerate(r["props"]):
            if p["type"] in M.reg["verify_types"]:
                res.append({"k": k, **yes_prob(*sc.probs(image, render(tpl, prop=p["text"]), y | no), y, no)})
        out.write({"id": r["id"], "cap": r["cap"], **({"tr": r["tr"]} if "tr" in r else {}),
                   "cfg": r["cfg"] + vcfg, "props": res, "n_props": len(res), "sec": round(time.time() - t, 4)})
        n += 1
    M.free(sc)
    return n


def judge_into(M: Models, j: str, src: list[dict], out: Out, img: dict, img_dir: Path) -> int:
    sc, n = M.scorer(), 0
    tpl = M.reg["prompts"][j]["text"]
    yn, dig = (sc.yn("vi"), None) if j == "ja" else (None, sc.digits())
    want = yn[0] | yn[1] if yn else frozenset(dig)
    for r in src:
        if key_of(r) in out:
            continue
        t = time.time()
        sub, top = sc.probs(M.image(img_dir / img[r["id"]]), render(tpl, caption=r["caption"]), want)
        val = yes_prob(sub, top, *yn) if yn else digit_ev(sub, top, dig)
        out.write({"id": r["id"], "cap": r["cap"], "j": j, **val, "sec": round(time.time() - t, 4)})
        n += 1
    M.free(sc)
    return n


def clip_into(M: Models, src: list[dict], out: Out, img: dict, img_dir: Path) -> int:
    cl, n, w = M.clip(), 0, M.reg["clip_w"]
    for r in src:
        if key_of(r) in out:
            continue
        t = time.time()
        cos, trunc = cl(M.image(img_dir / img[r["id"]]), r["caption"])
        out.write({"id": r["id"], "cap": r["cap"], "cos": cos, "score": w * max(cos, 0.0), "trunc": trunc,
                   "sec": round(time.time() - t, 4)})
        n += 1
    M.free(cl)
    return n


def smoke(M: Models, caps: list[dict], img: dict, img_dir: Path) -> dict:
    """Block S smoke (v3.1 §9.1 row S): every timing in memory; only rates leave (no smoke output is written)."""
    reg, T = M.reg, {}

    def per(t0, n):
        return (time.time() - t0) / max(n, 1)
    dec = M.decomposer()
    props = {}
    for cfg in ("d1", "d2"):
        t0 = time.time()
        res = []
        for j in range(0, len(caps), reg["decomposer_decode"]["batch"]):
            res += dec([render(reg["prompts"][cfg]["text"], caption=r["caption"])
                        for r in caps[j:j + reg["decomposer_decode"]["batch"]]])
        T[f"e_{cfg}"] = per(t0, len(caps))
        props[cfg] = [props_of(raw, reg["prop_types"])[0] for raw, _ in res]
    M.free(dec)
    sc = M.scorer()
    n_ver = {}
    for d, v in (("d1", "v1"), ("d2", "v1"), ("d1", "v2")):
        y, no = sc.yn(reg["prompt_lang"][v])
        t0, cnt = time.time(), 0
        for r, ps in zip(caps, props[d]):
            image = M.image(img_dir / img[r["id"]])
            for p in ps:
                if p["type"] in reg["verify_types"]:
                    yes_prob(*sc.probs(image, render(reg["prompts"][v]["text"], prop=p["text"]), y | no), y, no)
                    cnt += 1
        T[f"v_{d}{v}"], n_ver[f"{d}{v}"] = per(t0, len(caps)), cnt
    for j in ("ja", "jb", "jc"):
        t0 = time.time()
        want = frozenset(sc.digits()) if j != "ja" else frozenset().union(*sc.yn("vi"))
        for r in caps:
            sc.probs(M.image(img_dir / img[r["id"]]), render(reg["prompts"][j]["text"], caption=r["caption"]), want)
        T[j] = per(t0, len(caps))
    M.free(sc)
    cl, t0 = M.clip(), time.time()
    for r in caps:
        cl(M.image(img_dir / img[r["id"]]), r["caption"])
    T["clip"] = per(t0, len(caps))
    M.free(cl)
    return {**T, "n_captions": len(caps), "props_verified": n_ver,
            "p_d1v1": n_ver["d1v1"] / len(caps), "r_v_d1v1": T["v_d1v1"] * len(caps) / max(n_ver["d1v1"], 1)}


def run_step(name: str, M: Models, mapf: str = "-", hin: str = "-") -> int:
    reg, o = M.reg, O()
    mode, _, rest = name.partition(".")
    frame = frame_rows()
    img_dir = HB() / "a"
    A = slice_a(frame, manifest_names(img_dir))
    img = dict(A)
    sd = o / "out/s"
    if mode == "s":
        if rest.startswith("gate."):
            return gate_step(M, rest[5:], A, img_dir, sd)
        if rest == "a4rate":
            acc = walk_state(reg, rows_of(sd / "walk.jsonl"))[0]
            if len(acc) < reg["gate"]["n_accept"]:
                return 0  # PA3 is written by s.smoke
            if (sd / "rates_a4.json").is_file():  # a rerun after a kill between the write and the ledger end
                json.loads((sd / "rates_a4.json").read_text())
                return 0
            rates = {}
            for m in a4_models(reg, acc):  # reading 9: A4 decode rate measured on 16 images; captions in memory only
                mem = Mem()
                decode_into(M, m, A[:reg["smoke"]["a4_decode_images"]], mem, img_dir)
                rates[m] = sum(r["sec"] for r in mem.rows) / reg["smoke"]["a4_decode_images"]
            B.write_new(sd / "rates_a4.json", json.dumps(rates, sort_keys=True).encode())
            return 0
        if rest == "smoke":
            acc = walk_state(reg, rows_of(sd / "walk.jsonl"))[0]
            if len(acc) < reg["gate"]["n_accept"]:
                B.write_new(o / "PA3.json", json.dumps({"pa3": "fewer than 4 captioners accepted (§4.3)",
                                                        "accepted": acc, "utc": utc()}).encode())
                return PA3_RC
            if not (sd / "rates_smoke.json").is_file():
                gate = {k: {r["id"]: r for r in rows_of(sd / f"gate_{k}.jsonl")} for k in acc}
                caps = [gate[acc[i % 4]][A[i][0]] for i in range(reg["smoke"]["n_images"])]
                B.write_new(sd / "rates_smoke.json", json.dumps(smoke(M, caps, img, img_dir), sort_keys=True).encode())
            json.loads((sd / "rates_smoke.json").read_text())
            if not (sd / "ACCEPT.json").is_file():
                B.write_new(sd / "ACCEPT.json", json.dumps({"tier": B.LABEL, "accepted": acc, "walk": rows_of(
                    sd / "walk.jsonl")}, sort_keys=True).encode())
            return 0
        if rest == "trim":
            acc = accepted_list(reg)
            if not (sd / "rates.json").is_file():
                sm = json.loads((sd / "rates_smoke.json").read_text())
                dec = {k: sum(r["sec"] for r in rows_of(sd / f"gate_{k}.jsonl")) / reg["gate"]["n_images"] for k in acc}
                dec.update(json.loads((sd / "rates_a4.json").read_text()))
                rates = {**sm, "dec": dec, "accepted": acc, "n_h": reg["gate"]["n_images"] * 6}
                B.write_new(sd / "rates.json", json.dumps(rates, sort_keys=True).encode())
            rates = json.loads((sd / "rates.json").read_text())
            if not (sd / "TRIM.json").is_file():  # decided once; a rerun after a kill keeps the first decision
                t = trim(project(rates, a4_models(reg, acc)), left_sec(in_step=True))
                t["e1_e2"] = "NOT RUN (pre-fixed, R5 E-12)"
                B.write_new(sd / "TRIM.json", json.dumps(t, sort_keys=True).encode())
            t = json.loads((sd / "TRIM.json").read_text())
            print(json.dumps({"kept": t["kept"], "dropped": t["dropped"], "core_fits": t["core_fits"]}))
            if t["core_fits"]:
                return 0
            if not (o / "CORE_STOP.json").exists():  # v3.1 l.506 as R5 E-12: the core cannot finish: the PI decides
                B.write_new(o / "CORE_STOP.json", json.dumps({"core_stop": "A1 + A2 x 1.25 > cap left after S",
                                                              "need_sec": t["need_sec"], "utc": utc()}).encode())
            return CORE_RC
    acc = accepted_list(reg)

    def need(rows, n, what):  # CC-295 N8: a step's input is complete, not just present
        if len(rows) != n:
            fault(f"{what}: {len(rows)} rows, {n} needed")
        return rows
    dd = o / "out/a1decode"
    a1caps = cap_rows([dd / f"captions_{k}.jsonl" for k in acc])
    a1d = rows_of(o / "out/a1score/decomp_d1.jsonl")
    if mode == "a1decode":
        k = rest.split(".", 1)[1]
        out = Out(dd / f"captions_{k}.jsonl")
        decode_into(M, k, A, out, img_dir)
        return 0
    if mode in ("a1score", "rest") and not HEX64.fullmatch(mapf):
        fault("MAPF is not a 64-hex final-map sha")
    if mode == "a1score":
        mp = o / "out/a1score/MAPF.txt"
        mp.parent.mkdir(parents=True, exist_ok=True)
        if mp.exists() and mp.read_text().strip() != mapf:
            fault("MAPF differs from the one this block started with")
        mp.exists() or B.write_new(mp, (mapf + "\n").encode())
        need(a1caps, 4 * N_SLICE, "A1-decode captions")
        sa = o / "out/a1score"
        {"decomp_d1": lambda: decomp_into(M, "d1", a1caps, Out(sa / "decomp_d1.jsonl")),
                "verify_d1v1": lambda: verify_into(M, "v1", need(a1d, 4 * N_SLICE, "A1 decomposition"),
                                                   Out(sa / "verify_d1v1.jsonl"), img, img_dir),
                "ja": lambda: judge_into(M, "ja", a1caps, Out(sa / "ja.jsonl"), img, img_dir),
                "clip": lambda: clip_into(M, a1caps, Out(sa / "clip.jsonl"), img, img_dir)}[rest]()
        return 0
    sr = o / "out/rest"
    if (o / "out/a1score/MAPF.txt").read_text().strip() != mapf:
        fault("rest MAPF differs from A1-score's")
    need(a1caps, 4 * N_SLICE, "A1-decode captions")
    if rest.startswith("h_"):
        hp = o / "in/h_input.jsonl"
        if not HEX64.fullmatch(hin) or sha_bytes(hp.read_bytes()) != hin:
            fault("h_input.jsonl differs from the --hin sha")
        hrows = rows_of(hp)
        if rest == "h_decomp":
            decomp_into(M, "d1", hrows, Out(sr / "h_decomp_d1.jsonl"))
        else:
            verify_into(M, "v1", need(rows_of(sr / "h_decomp_d1.jsonl"), len(hrows), "H decomposition"),
                        Out(sr / "h_verify_d1v1.jsonl"), img, img_dir)
        return 0
    if rest.startswith("a4dec."):
        k = rest[6:]
        if k not in a4_models(reg, acc):
            fault(f"{k} is not an A4 model")
        decode_into(M, k, A, Out(sr / f"a4/captions_{k}.jsonl"), img_dir)
        return 0
    if rest.startswith("a4_"):
        a4caps = cap_rows([sr / f"a4/captions_{m}.jsonl" for m in a4_models(reg, acc)])
        if len(a4caps) != N_SLICE * len(a4_models(reg, acc)):
            fault("A4 decode incomplete")
        a4d = rows_of(sr / "a4/decomp_d1.jsonl")
        {"a4_decomp_d1": lambda: decomp_into(M, "d1", a4caps, Out(sr / "a4/decomp_d1.jsonl")),
                "a4_verify_d1v1": lambda: verify_into(M, "v1", need(a4d, len(a4caps), "A4 decomposition"),
                                                      Out(sr / "a4/verify_d1v1.jsonl"), img, img_dir),
                "a4_ja": lambda: judge_into(M, "ja", a4caps, Out(sr / "a4/ja.jsonl"), img, img_dir),
                "a4_clip": lambda: clip_into(M, a4caps, Out(sr / "a4/clip.jsonl"), img, img_dir)}[rest]()
        return 0
    {"jb": lambda: judge_into(M, "jb", a1caps, Out(sr / "jb.jsonl"), img, img_dir),
            "jc": lambda: judge_into(M, "jc", a1caps, Out(sr / "jc.jsonl"), img, img_dir),
            "decomp_d2": lambda: decomp_into(M, "d2", a1caps, Out(sr / "decomp_d2.jsonl")),
            "verify_d2v1": lambda: verify_into(M, "v1", need(rows_of(sr / "decomp_d2.jsonl"), 4 * N_SLICE, "A3 d2"),
                                               Out(sr / "verify_d2v1.jsonl"), img, img_dir),
            "verify_d1v2": lambda: verify_into(M, "v2", need(a1d, 4 * N_SLICE, "A1 decomposition"),
                                               Out(sr / "verify_d1v2.jsonl"), img, img_dir)}[rest]()
    return 0


def gate_step(M: Models, key: str, A: list, img_dir: Path, sd: Path) -> int:
    reg = M.reg
    wp = sd / "walk.jsonl"
    sd.mkdir(parents=True, exist_ok=True)
    acc, seen = walk_state(reg, rows_of(wp))
    if key in seen:
        return 0
    if reg["walk"].index(key) != len(seen):
        fault(f"gate {key} out of the walk order")
    rec = {"key": key, "pos": reg["models"][key]["walk"], "utc": utc()}
    if len(acc) >= reg["gate"]["n_accept"]:
        rec.update(decision="not_reached", reason="4 accepted")
    elif why := desk(reg, key, acc):
        rec.update(decision="skip", reason=why)
    else:
        n = reg["gate"]["n_images"]
        out = Out(sd / f"gate_{key}.jsonl")
        decode_into(M, key, A[:n], out, img_dir)
        out.close()
        caps = {r["id"]: r["caption"] for r in rows_of(out.p)}
        sh = gate_share([caps[i] for i, _ in A[:n]], n)
        rec.update(decision="accept" if gate_pass(sh, reg) else "reject", reason="gate",
                   share_num=sh.numerator, share_den=sh.denominator, n=n,
                   n_vn=sum(is_vn(caps[i]) for i, _ in A[:n]))
    with open(wp, "a") as f:
        f.write(json.dumps(rec, sort_keys=True) + "\n")
    print(json.dumps({k: rec[k] for k in ("key", "decision", "reason")}))
    return 0


# ---------------------------------------------------------------------------------------------- CLI helpers
def cmd_cap_init(a) -> int:
    if a.cap_h not in (22, 28) or not (1000 <= a.r_host <= 100_000) or a.fee < 0 or not 0 <= a.used_w_sec <= a.used_sec:
        fault("cap-init values out of range (cap 22 or 28 GPU-h, R6 Part II §2)")
    if not re.fullmatch(r"\d{4}-\d\d-\d\dT\d\d:\d\d:\d\dZ", a.t0):
        fault("T0 must be the rental line's date -u stamp")
    O().mkdir(parents=True, exist_ok=True)
    d = {"tier": B.LABEL, "cap_h": a.cap_h, "cap_sec": a.cap_h * 3600, "r_host": a.r_host, "fee": a.fee, "t0": a.t0,
         "used_before_sec": a.used_sec, "used_w_before_sec": a.used_w_sec, "utc": utc()}
    B.write_new(O() / "CAP.json", (json.dumps(d, sort_keys=True) + "\n").encode())
    print(sha_bytes((O() / "CAP.json").read_bytes()))
    return 0


def cmd_ledger(a) -> int:
    rows = ledger()
    st = open_step(rows)
    if a.op == "start":
        markers()
        if st:
            fault(f"ledger step {st['step']} is open")
        ledger_add({"ev": "start", "step": a.step, "t": time.time(), "m": time.monotonic()})  # m: wall-clock steps safe
    else:
        if not st or st["step"] != a.step:
            fault("ledger end without its start")
        ledger_add({"ev": "end", "step": a.step, "t": time.time(), "sec": max(1, int(time.monotonic() - st["m"]) + 1),
                    "rc": a.rc})
    return 0


def cmd_resume(a) -> int:
    """v3.1 l.519-520: one resume, only for a guard failure or machine loss, after a cause read (RS-3)."""
    if not re.fullmatch(r"CC-\d+[a-z0-9]*", a.cc):
        fault("--cc must name the cause-read CC")
    rows = ledger()
    st = open_step(rows)
    if st and a.close_sec is None:
        fault(f"step {st['step']} is open: --close-sec from the pull-loop evidence is required")
    B.write_new(O() / "RESUME.json", json.dumps({"cause": a.cause, "cc": a.cc, "utc": utc(),
                                                 "closed": st and st["step"], "close_sec": a.close_sec}).encode())
    if st:
        ledger_add({"ev": "end", "step": st["step"], "t": time.time(), "sec": a.close_sec, "rc": "resume"})
    for p in (O() / "out").rglob("*.jsonl"):
        if n := untorn(p):
            print(f"torn tail moved: {p.relative_to(O())} {n} B")
    return 0


def cmd_money_stop(a) -> int:
    """R6 §I.3 rule 4 / RB9: written by the coordinator over ssh when a panel read shows balance <= threshold."""
    if a.balance > a.threshold:
        fault("balance above the threshold: no money stop")
    B.write_new(O() / "MONEY_STOP.json", json.dumps({"balance": a.balance, "threshold": a.threshold,
                                                     "utc": utc()}).encode())
    return 0


def cmd_inputs(a) -> int:
    frame = frame_rows()
    d = HB() / a.set
    names = manifest_names(d)
    if a.set == "a":
        print(json.dumps({"slice_a": len(slice_a(frame, names))}))
    else:
        if w_block_ok(frame, names) != a.nblk:
            fault(f"W manifest does not end at block {a.nblk}")
        print(json.dumps({"w_images": len(names), "blocks_through": a.nblk}))
    return 0


def main() -> int:
    ap = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    sp = ap.add_subparsers(dest="cmd", required=True)
    sp.add_parser("selftest")
    sp.add_parser("hostcheck").add_argument("--venv", choices=("main", "legacy"), required=True)
    ci = sp.add_parser("cap-init")
    ci.add_argument("--cap-h", type=int, required=True)
    ci.add_argument("--r-host", type=int, required=True)
    ci.add_argument("--fee", type=int, required=True)
    ci.add_argument("--t0", required=True)
    ci.add_argument("--used-sec", type=int, default=0, help="HB-T1': GPU-h used on HB-T1 (Part II §2 step 5)")
    ci.add_argument("--used-w-sec", type=int, default=0, help="HB-T1': the part of --used-sec spent in w. steps (F-3)")
    sp.add_parser("steps").add_argument("--mode", required=True)
    lg = sp.add_parser("ledger")
    lg.add_argument("op", choices=("start", "end"))
    lg.add_argument("step")
    lg.add_argument("--rc", type=int, default=0)
    sp.add_parser("left").add_argument("--w", action="store_true")
    ip = sp.add_parser("inputs")
    ip.add_argument("--set", choices=("a", "w"), required=True)
    ip.add_argument("--nblk", type=int, default=0)
    rp = sp.add_parser("run")
    rp.add_argument("step")
    rp.add_argument("--mapf", default="-")
    rp.add_argument("--hin", default="-")
    bc = sp.add_parser("balance-cadence", help="hours to the next panel read (CC-295 N13)")
    for f in ("--balance", "--threshold", "--burn"):
        bc.add_argument(f, type=int, required=True)
    ms = sp.add_parser("money-stop")
    ms.add_argument("--balance", type=int, required=True)
    ms.add_argument("--threshold", type=int, required=True)
    rs = sp.add_parser("resume")
    rs.add_argument("--cause", choices=("guard", "machine"), required=True)
    rs.add_argument("--cc", required=True)
    rs.add_argument("--close-sec", type=int)
    wp = sp.add_parser("wipe")
    wp.add_argument("--dir", type=Path, required=True)
    wp.add_argument("--log", type=Path, required=True)
    a = ap.parse_args()
    if a.cmd == "selftest":
        return selftest()
    if a.cmd == "hostcheck":
        from b_pa1_models import hostcheck
        return hostcheck(load_reg(), a.venv)
    if a.cmd == "steps":
        markers()
        for s, v in steps(a.mode, load_reg()):
            print(s, v)
        return 0
    if a.cmd == "left":
        print(left_sec(a.w))
        return 0
    if a.cmd == "run":
        markers()
        return run_step(a.step, Models(load_reg()), a.mapf, a.hin)
    if a.cmd == "wipe":
        return wipe(a.dir, a.log)
    if a.cmd == "balance-cadence":
        print(next_read_h(a.balance, a.threshold, a.burn))
        return 0
    return {"cap-init": cmd_cap_init, "ledger": cmd_ledger, "money-stop": cmd_money_stop, "resume": cmd_resume,
            "inputs": cmd_inputs}[a.cmd](a)



# ---------------------------------------------------------------------------------------------- selftest (CPU, fakes)
class FakeModels(Models):
    """Fakes with the real call shapes. FAIL[key] = how many of the 231 gate captions are not Vietnamese."""
    FAIL: dict = {}

    def snap(self, key):
        return Path("/nonexistent")

    def image(self, path):
        if not Path(path).is_file():
            fault(f"fake: no image {path}")
        return Path(path)

    def free(self, obj):
        self.freed = getattr(self, "freed", 0) + 1

    def captioner(self, key):
        bad, calls = self.FAIL.get(key, 0), []

        def gen(image, prompt):  # the first `bad` calls of this captioner give English
            if prompt != self.reg["prompts"]["captioner"]["text"]:
                fault("fake: captioner prompt")
            calls.append(image)
            return ("a photo of a cat" if len(calls) <= bad else f"Một con mèo {key}"), 7
        return gen

    def decomposer(self):
        def dec(prompts):
            out = []
            for p in prompts:
                arr = json.dumps([{"type": "object", "text": "Có con mèo.", "object": "mèo"},
                                  {"type": "colour", "text": "Con mèo màu đen.", "object": "mèo"},
                                  {"type": "smell", "text": "x", "object": "y"}], ensure_ascii=False)
                out.append((arr[:-60] if "Example 1." in p else arr, 30))  # d2: a truncated array -> partial
            return out
        return dec

    def scorer(self):
        class S:
            def yn(self, lang):
                return (frozenset({1}), frozenset({2})) if lang == "vi" else (frozenset({3}), frozenset({4}))

            def digits(self):
                return list(range(10, 20))

            def probs(self, image, prompt, ids):
                return {i: 0.1 for i in ids}, (1 if "đúng" in prompt or "có" in prompt else 5)
        return S()

    def clip(self):
        return lambda image, text: (0.3 if int(image.stem.split("_")[1]) % 2 else -0.1, False)


def selftest() -> int:  # noqa: C901  one linear script of fixtures
    import io
    from types import SimpleNamespace as NS
    global FRAME_SHA, N_SLICE
    refuse = B.must_refuse
    reg = load_reg()
    real = (FRAME_SHA, N_SLICE)
    Out.SYNC = False  # fixtures only; the host run keeps one fsync per row
    assert N_SLICE == 2000 and W_CAP_SEC == 3600 and reg["gate"] == {"n_images": 231, "pass_share": "95/100",
                                                                     "n_accept": 4}
    assert reg["rule_s_max_params"] == 8 * 10 ** 9 and reg["decode"]["max_new_tokens"] == 60

    # registry: prompts NFC + sha; every revision 40-hex; walk 1..10; Rule S desk facts (readiness §6)
    ms = reg["models"]
    assert [ms[k]["rule_s"] for k in reg["walk"]].count("fail") == 2 and ms["internvl2_5_8b"]["rule_s"] == "fail"
    assert ms["mblip_bloomz_7b"]["rule_s"] == "fail" and ms["gemma3n_e4b"]["revision"].startswith("c1221e9c")
    assert all(ms[k]["download"] == (ms[k]["rule_s"] != "fail") for k in reg["walk"])
    with scratch() as td:
        bad = json.loads(REG_PATH.read_text())
        bad["prompts"]["v1"]["text"] += " "
        (Path(td) / "r.json").write_text(json.dumps(bad))
        refuse(lambda: load_reg(Path(td) / "r.json"), "differs from its sha")
        bad = json.loads(REG_PATH.read_text())
        bad["walk"] = bad["walk"][1:] + bad["walk"][:1]
        (Path(td) / "r.json").write_text(json.dumps(bad))
        refuse(lambda: load_reg(Path(td) / "r.json"), "walk order")
        bad = json.loads(REG_PATH.read_text())
        bad["models"]["qwen2_5_7b"]["lineage"]["L"] = "Llama"
        (Path(td) / "r.json").write_text(json.dumps(bad))
        refuse(lambda: load_reg(Path(td) / "r.json"), "decomposer L")
    assert render("a {prop} b", prop="{caption}") == "a {caption} b"
    refuse(lambda: render("a {prop}", caption="x"), "slots")
    refuse(lambda: render("a {prop} {caption}", prop="x"), "slots")

    # gate (§4.4): >= 0.95 of 231 incl. empty captions; upper case, NFD, đ, tone marks
    assert is_vn("Đây") and is_vn(unicodedata.normalize("NFD", "mèo")) and is_vn("ĂN") and is_vn("cơm") and is_vn("tủ")
    assert is_vn("ĐI") and is_vn("mẹ") and is_vn("mèo") and is_vn("nữ")
    assert not is_vn("") and not is_vn("a cat on a mat") and not is_vn("中文")
    caps = ["Một con mèo"] * 220 + [""] * 11
    assert gate_share(caps, 231) == Fraction(220, 231) and gate_pass(Fraction(220, 231), reg)
    assert not gate_pass(Fraction(219, 231), reg) and gate_pass(Fraction(95, 100), reg)
    refuse(lambda: gate_share(caps[:-1], 231), "231")

    # walk (§4.3): desk skips, disjointness, stop at 4, A4 list
    assert desk(reg, "internvl2_5_8b", []) == "rule_s" and desk(reg, "mblip_bloomz_7b", []) == "rule_s"
    for k in ("internvl2_5_2b", "mblip_mt0_xl", "gemma3n_e4b", "minicpm_v4", "phi3_5_vision"):
        assert desk(reg, k, []) is None, k
    assert desk(reg, "gemma3_4b", ["minicpm_v4"]) == "accepted:minicpm_v4"
    g3n = reg["models"]["gemma3n_e4b"]["lineage"]  # CC-295 W6 / PI-1108e: one switch, the V value
    assert g3n["V"] == "MobileNet-V5" and "ERRATUM_LINEAGE_GEMMA3N_v1_2.md" in g3n["source"]
    r_ = json.loads(json.dumps(reg))
    r_["models"]["gemma3n_e4b"]["lineage"]["V"] = g3n["V_without_erratum"]
    assert desk(r_, "gemma3n_e4b", []) == "lineage" and desk(r_, "gemma3_4b", ["gemma3n_e4b"]) == "accepted:gemma3n_e4b"
    assert reg["instrument_llm"]["mode"] == "agent-drafted, amendment-logged" and reg["instrument_llm"]["id"] is None
    assert desk(reg, "gemma3_4b", ["gemma3n_e4b"]) == "accepted:gemma3n_e4b"
    assert desk(reg, "molmo_7b_o", ["phi3_5_vision"]) == "accepted:phi3_5_vision"
    r2 = json.loads(json.dumps(reg))
    r2["models"]["minicpm_v4"]["lineage"]["L"] = "Qwen"
    assert desk(r2, "minicpm_v4", []) == "verifier"
    r2["models"]["minicpm_v4"]["lineage"]["V"] = "undetermined"
    assert desk(r2, "minicpm_v4", []) == "lineage"
    r3_ = json.loads(json.dumps(reg))
    r3_["models"]["qwen2_5_vl_3b"]["lineage"]["V"] = "undetermined"
    assert desk(r3_, "minicpm_v4", []) == "verifier", "an undetermined verifier clashes with every candidate"
    r3_ = json.loads(json.dumps(reg))
    r3_["models"]["minicpm_v4"]["safetensors_total"] = 8 * 10 ** 9
    assert desk(r3_, "minicpm_v4", []) is None, "Rule S: <= 8.0e9 passes"
    r3_["models"]["minicpm_v4"]["safetensors_total"] = None
    assert desk(r3_, "minicpm_v4", []) == "rule_s"
    r2["models"]["minicpm_v4"]["safetensors_total"] = 8 * 10 ** 9 + 1
    assert desk(r2, "minicpm_v4", []) == "rule_s"
    r2["models"]["minicpm_v4"]["files"] = {}
    assert desk(r2, "minicpm_v4", []) == "pin"
    assert a4_models(reg, ["gemma3_4b"]) == ["qwen2_5_vl_3b", "internvl3_2b"]
    assert a4_models(reg, []) == ["qwen2_5_vl_3b", "gemma3_4b", "internvl3_2b"]
    refuse(lambda: walk_state(reg, [{"key": "mblip_mt0_xl", "decision": "skip"}]), "out of the registered order")
    refuse(lambda: walk_state(reg, [{"key": "internvl2_5_8b", "decision": "skip"}] * 2), "repeats")

    # Y/N sets, abstain, 0-9 EV (§7.1 N5)
    enc = {"có": [7, 1], "Có": [8], " có": [9], " Có": [9], "không": [7], "Không": [11], " không": [12],
           " Không": [13]}.__getitem__
    y, n = yn_sets(enc, reg["token_words"]["vi"])
    assert y == {8, 9} and n == {11, 12, 13}, (y, n)  # 7 is shared: removed from both
    refuse(lambda: yn_sets(lambda w: [1], reg["token_words"]["vi"]), "empty")
    sub = {8: 0.2, 9: 0.1, 11: 0.1, 12: 0.05, 13: 0.05}
    r = yes_prob(sub, 8, y, n)
    assert abs(r["p_yes"] - 0.6) < 1e-12 and not r["abstain"] and r["top1"] == "Y"
    assert yes_prob(sub, 7, y, n)["abstain"] and yes_prob(sub, 11, y, n)["top1"] == "N"
    assert not yes_prob(sub, 11, y, n)["abstain"] and yes_prob(sub, 7, y, n)["top1"] == "other"
    assert yes_prob({i: 0.0 for i in sub}, 99, y, n)["p_yes"] is None
    ids = list(range(10, 20))
    assert digit_ids(lambda d: [10 + int(d)], reg["digits"]) == ids
    refuse(lambda: digit_ids(lambda d: [1, 0] if d == "1" else [int(d)], reg["digits"]), "T5")
    refuse(lambda: digit_ids(lambda d: [5], reg["digits"]), "T5")
    ev = digit_ev({i: (0.3 if i == 19 else 0.1 if i == 10 else 0.0) for i in ids}, 19, ids)
    assert abs(ev["ev"] - 9 * 0.75) < 1e-12 and ev["top1"] == "digit" and digit_ev(dict.fromkeys(ids, 0.0), 0, ids)["ev"] is None

    # decomposer output: whole array, truncated array, braces in strings, junk types dropped
    pr, st = props_of('[{"type": "object", "text": "Có {mèo}.", "object": "mèo"}]', reg["prop_types"])
    assert st == "ok" and pr == [{"type": "object", "text": "Có {mèo}.", "object": "mèo"}]
    pr, st = props_of('x [{"type": "object", "text": "a"}, {"type": "count", "text": "b \\"}', reg["prop_types"])
    assert st == "partial" and [p["text"] for p in pr] == ["a"], pr
    assert props_of("no json", reg["prop_types"]) == ([], "fail")
    assert props_of('[{"type": "smell", "text": "a"}]', reg["prop_types"]) == ([], "fail")
    assert props_of('[{"type": "object", "text": "a"}, {"type": "smell", "text": "b"}]', reg["prop_types"])[1] == "partial"

    # trim (§9.1 l.510-511): hand values in seconds; the core is never trimmed
    P_ = {"a1": 100, "a2": 20, "a3": 40, "h": 10, "a4": 30}
    assert trim(P_, 250)["kept"] == ["a3", "h", "a4"]          # 1.25 * 200 = 250 <= 250
    assert trim(P_, 249)["dropped"] == ["a4"]                   # 1.25 * 170 = 212.5
    assert trim(P_, 212)["dropped"] == ["a4", "h"]              # 1.25 * 160 = 200
    assert trim(P_, 199)["dropped"] == ["a4", "h", "a3"] and trim(P_, 199)["core_fits"]
    assert not trim(P_, 149)["core_fits"] and trim(P_, 150)["core_fits"]   # core 1.25 * 120 = 150
    rt = {"accepted": ["a", "b"], "dec": {"a": 1, "b": 2, "m": 3}, "e_d1": 1, "v_d1v1": 2, "ja": 3, "clip": 4, "jb": 1,
          "jc": 2, "e_d2": 1, "v_d2v1": 1, "v_d1v2": 1, "n_h": 10}
    pj = project(rt, ["m"])
    assert pj == {"a1": 2000 * 3 + 8000 * 10, "a2": 8000 * 3, "a3": 8000 * 3, "h": 10 * 3, "a4": 2000 * 13}, pj

    # scratch cleanup never follows a link: a file behind a linked dir survives (the mutants' tree links the repo)
    with scratch() as keep:
        (keep / "f").write_text("x")
        with scratch() as sc_:
            (sc_ / "sub").mkdir()
            (sc_ / "sub/g").write_text("y")
            (sc_ / "link_dir").symlink_to(keep)
            (sc_ / "link_file").symlink_to(keep / "f")
        assert not sc_.exists() and (keep / "f").read_text() == "x"

    # steps: each gate in its model's venv; git-blob SHA-1 form; snapshot pin check
    gv = dict(steps("s", reg))
    assert gv["s.gate.internvl2_5_2b"] == "legacy" and gv["s.gate.mblip_mt0_xl"] == "main" and gv["s.trim"] == "main"
    with scratch() as td:
        d = Path(td)
        (d / "h").write_bytes(b"hello\n")
        assert blob_hashes(d / "h") == (sha_bytes(b"hello\n"), "ce013625030ba8dba906f756967f9e9ca394464a")
        os.environ["B_PA1_OUT"] = str(d / "o")
        try:
            (d / "o/snaps").mkdir(parents=True)
            sn = d / "snap"
            sn.mkdir()
            (sn / "w.safetensors").write_bytes(b"weights")
            (sn / "config.json").write_bytes(b"{}")
            (d / "o/snaps/m.path").write_text(f"{sn}\n")
            rs = {"models": {"m": {"files": {"w.safetensors": ["lfs", sha_bytes(b"weights")],
                                             "config.json": ["blob", blob_hashes(sn / "config.json")[1]]}}}}
            assert Models(rs).snap("m") == sn
            (sn / "config.json").write_bytes(b"{ }")
            refuse(lambda: Models(rs).snap("m"), "differs from its pin")
            (sn / "config.json").write_bytes(b"{}")
            (sn / "extra.bin").write_bytes(b"pickle")
            refuse(lambda: Models(rs).snap("m"), "unpinned pickle")
        finally:
            del os.environ["B_PA1_OUT"]

    # outputs: ids-only keys; duplicate rows; torn tails; wipe count
    refuse(lambda: rec_ok({"id": 1, "note": "x"}), "not whitelisted")
    refuse(lambda: rec_ok({"id": 1, "cap": "a b"}), "not an id")
    assert rec_ok({"id": 1, "caption": "free text ok", "props": [{"text": "x y"}]})
    with scratch() as td:
        d = Path(td)
        o = Out(d / "x.jsonl")
        o.write({"id": 1, "cap": "k", "sec": 1})
        refuse(lambda: o.write({"id": 1, "cap": "k", "sec": 2}), "duplicate")
        o.close()
        (d / "x.jsonl").open("a").write('{"id": 2, "ca')
        refuse(lambda: rows_of(d / "x.jsonl"), "torn")
        assert untorn(d / "x.jsonl") == len('{"id": 2, "ca') and len(rows_of(d / "x.jsonl")) == 1
        assert [p.read_text() for p in d.glob("x.jsonl.torn.*")] == ['{"id": 2, "ca'] and untorn(d / "x.jsonl") == 0
        m = Mem()
        m.write({"id": 3, "cap": "k"})
        assert ("k", 3, None) in m and not any(d.glob("*mem*"))
        s_ = d / "set"
        (s_ / "images/v1").mkdir(parents=True)
        for i in range(3):
            (s_ / f"images/v1/{i}.jpg").write_bytes(b"x")
        (s_ / "MANIFEST.sha256").write_text("".join(f"{'0' * 64}  images/v1/{i}.jpg\n" for i in range(3)))
        assert wipe(s_, d / "del.log") == 0 and not s_.exists()
        (s_ / "a").mkdir(parents=True)
        (s_ / "a/x").write_bytes(b"x")
        assert wipe(s_, d / "del.log") == 1 and not s_.exists()  # no manifest: count mismatch, still wiped
        lines = (d / "del.log").read_text().splitlines()
        assert [ln.split("\t")[2:] for ln in lines] == [["4", "3"], ["1", "-1"]], lines

    # the whole block chain on fakes: S (walk, A4 rate, smoke, trim), A1-decode, A1-score, rest
    with scratch() as td:
        d = Path(td)
        os.environ["B_PA1_OUT"], os.environ["B_PA1_HB"] = str(d / "out"), str(d / "hb")
        try:
            N_SLICE = 300
            frame = [(1000 + i, f"images/v1/patch{i % 2}/img_{i}.jpg") for i in range(400)]
            fb = "".join(f"{i}\t{f}\n" for i, f in frame).encode()
            FRAME_SHA = sha_bytes(fb)
            (d / "out/in").mkdir(parents=True)
            (d / "out/in/o365_train_frame.tsv").write_bytes(fb)
            keep = [r for j, r in enumerate(frame) if j % 4 != 3][:N_SLICE]  # W25 survivors stand-in
            a = d / "hb/a"
            for _, f in keep:
                (a / f).parent.mkdir(parents=True, exist_ok=True)
                (a / f).write_bytes(b"x")
            (a / "MANIFEST.sha256").write_text("".join(f"{'0' * 64}  {f}\n" for _, f in reversed(keep)))
            A = slice_a(frame_rows(), manifest_names(a))
            assert A == keep, "slice order = frame order, whatever the manifest order"
            refuse(lambda: slice_a(frame, manifest_names(a)[1:]), "300 needed")
            fb2 = fb.replace(b"\t", b" ", 1)
            (d / "out/in/o365_train_frame.tsv").write_bytes(fb2)
            refuse(frame_rows, "differs from 863ad3e9")
            (d / "out/in/o365_train_frame.tsv").write_bytes(fb)
            names = [f for _, f in frame]
            assert w_block_ok(frame, names[:200], 100) == 2 and w_block_ok(frame, names[200:400], 100) == 4
            refuse(lambda: w_block_ok(frame, names[50:250], 100), "block-aligned")
            refuse(lambda: w_block_ok(frame, names[:150], 100), "block-aligned")
            refuse(lambda: w_block_ok(frame, names[1:] + names[:1], 100), "block-aligned")

            ns = lambda **k: NS(**{"cap_h": 28, "r_host": 10092, "fee": 30, "t0": "2026-11-10T01:00:00Z",  # noqa
                                   "used_sec": 0, "used_w_sec": 0, **k})
            for bad in (ns(cap_h=20), ns(r_host=10), ns(t0="today"), ns(used_sec=-1), ns(used_w_sec=-1),
                        ns(used_sec=100, used_w_sec=101)):
                refuse(lambda: cmd_cap_init(bad), "cap-init" if bad.t0 != "today" else "T0")
            with contextlib.redirect_stdout(io.StringIO()):
                cmd_cap_init(ns())
            try:
                cmd_cap_init(ns())
                raise AssertionError("CAP.json written twice")
            except FileExistsError:
                pass
            assert left_sec() == 28 * 3600 and left_sec(w=True) == 3600
            lg = lambda op, st, rc=0: cmd_ledger(NS(op=op, step=st, rc=rc))  # noqa: E731
            lg("start", "w.feats")
            refuse(lambda: lg("start", "w.again"), "open")
            refuse(left_sec, "open step")
            refuse(lambda: lg("end", "s.x"), "without its start")
            clock = time.monotonic
            try:  # a fake clock: the step took 100 s (CC-295 N1: HM1, HM3)
                time.monotonic = lambda: clock() + 100
                assert 28 * 3600 - 102 <= left_sec(in_step=True) <= 28 * 3600 - 100, "in-step elapsed counts"
                lg("end", "w.feats")
            finally:
                time.monotonic = clock
            assert 100 <= ledger()[-1]["sec"] <= 102, ledger()[-1]
            assert left_sec(w=True) == 3600 - ledger()[-1]["sec"] and left_sec() == 28 * 3600 - ledger()[-1]["sec"]
            o_main = os.environ["B_PA1_OUT"]
            with scratch() as hb2:  # HB-T1': the GPU-h used on HB-T1 come in by --used-sec (CC-295 N1: HM2, HM4)
                os.environ["B_PA1_OUT"] = str(hb2)
                with contextlib.redirect_stdout(io.StringIO()):
                    cmd_cap_init(ns(used_sec=10_000))
                assert left_sec() == 28 * 3600 - 10_000 and cap_doc()["used_before_sec"] == 10_000
            with scratch() as hb3:  # F-3: HB-T1's W seconds come in by --used-w-sec and lower W's own 1.0 GPU-h
                os.environ["B_PA1_OUT"] = str(hb3)
                with contextlib.redirect_stdout(io.StringIO()):
                    cmd_cap_init(ns(used_sec=10_000, used_w_sec=3000))
                assert left_sec(w=True) == 600 and left_sec() == 28 * 3600 - 10_000, (left_sec(w=True), left_sec())
                os.environ["B_PA1_OUT"] = o_main
            assert next_read_h(30_277 + 6 * 20_184, 30_277, 20_184) == 1 and next_read_h(200_000, 30_277, 20_184) == 6
            assert next_read_h(30_277, 30_277, 20_184) == 0 and next_read_h(30_278, 30_277, 20_184) == 1

            M = FakeModels(reg)
            M.FAIL = {"gemma3n_e4b": 12, "phi3_5_vision": 0}  # 219/231 < 0.95 -> reject
            sd = d / "out/out/s"
            with contextlib.redirect_stdout(io.StringIO()):
                for st, v in steps("s", reg):
                    if st == "s.trim":
                        lg("start", st)
                    assert run_step(st, M) == 0, st
                    if st == "s.trim":
                        lg("end", st)
            walk = {r["key"]: (r["decision"], r["reason"]) for r in rows_of(sd / "walk.jsonl")}
            assert walk == {"internvl2_5_8b": ("skip", "rule_s"), "internvl2_5_2b": ("accept", "gate"),
                            "mblip_mt0_xl": ("accept", "gate"), "mblip_bloomz_7b": ("skip", "rule_s"),
                            "gemma3n_e4b": ("reject", "gate"), "minicpm_v4": ("accept", "gate"),
                            "gemma3_4b": ("skip", "accepted:minicpm_v4"), "phi3_5_vision": ("accept", "gate"),
                            "molmo_7b_o": ("not_reached", "4 accepted"),
                            "llava15_7b": ("not_reached", "4 accepted")}, walk
            acc = accepted_list(reg)
            assert acc == ["internvl2_5_2b", "mblip_mt0_xl", "minicpm_v4", "phi3_5_vision"]
            assert sorted(p.name for p in sd.iterdir()) == sorted(
                ["walk.jsonl", "rates_a4.json", "rates_smoke.json", "rates.json", "TRIM.json", "ACCEPT.json"]
                + [f"gate_{k}.jsonl" for k in ("internvl2_5_2b", "mblip_mt0_xl", "gemma3n_e4b", "minicpm_v4",
                                                 "phi3_5_vision")]), "smoke outputs on disk"
            assert set(json.loads((sd / "rates_a4.json").read_text())) == {"qwen2_5_vl_3b", "gemma3_4b",
                                                                           "internvl3_2b"}
            sm = json.loads((sd / "rates_smoke.json").read_text())
            assert sm["n_captions"] == 64 and set(sm) >= {"e_d1", "e_d2", "v_d1v1", "v_d2v1", "v_d1v2", "ja", "jb", "jc",
                                                          "clip", "p_d1v1", "r_v_d1v1"}, sm
            assert sm["props_verified"]["d1v1"] == 128 and sm["props_verified"]["d1v2"] == 128, sm
            tr = json.loads((sd / "TRIM.json").read_text())
            assert tr["kept"] == ["a3", "h", "a4"] and tr["core_fits"] and tr["e1_e2"].startswith("NOT RUN")
            snap = {p.name: p.read_bytes() for p in sd.iterdir()}
            with contextlib.redirect_stdout(io.StringIO()):  # a kill after a write and before the ledger end
                for st in ("s.a4rate", "s.smoke", "s.trim"):
                    lg("start", st)
                    assert run_step(st, M) == 0, st
                    lg("end", st)
            assert {p.name: p.read_bytes() for p in sd.iterdir()} == snap, "a rerun of S changed its outputs"
            (sd / "ACCEPT.json").unlink()
            with contextlib.redirect_stdout(io.StringIO()):
                run_step("s.smoke", M)
            assert (sd / "ACCEPT.json").read_bytes() == snap["ACCEPT.json"], "smoke rerun rewrote ACCEPT.json"
            assert 28 * 3600 - 3700 < tr["cap_left_sec"] < 28 * 3600, "trim reads the GPU-h left inside its own step"
            assert len(rows_of(sd / "gate_internvl2_5_2b.jsonl")) == 231
            assert run_step("s.gate.internvl2_5_2b", M) == 0 and len(rows_of(sd / "walk.jsonl")) == 10
            wb = (sd / "walk.jsonl").read_bytes()
            (sd / "walk.jsonl").write_bytes(wb.split(b"\n", 2)[0] + b"\n")
            refuse(lambda: run_step("s.gate.gemma3n_e4b", M), "out of the walk order")
            (sd / "walk.jsonl").write_bytes(wb)

            with contextlib.redirect_stdout(io.StringIO()):
                for st, v in steps("a1decode", reg):
                    assert v == reg["models"][st.rsplit(".", 1)[1]]["venv"]
                    run_step(st, M)
            dd = d / "out/out/a1decode"
            assert all(len(rows_of(dd / f"captions_{k}.jsonl")) == N_SLICE for k in acc)
            refuse(lambda: run_step("a1score.decomp_d1", M, "-"), "MAPF")
            refuse(lambda: run_step("a1score.decomp_d1", M, "A" * 64), "MAPF")
            mapf = "b" * 64
            for st, _ in steps("a1score", reg):
                run_step(st, M, mapf)
            refuse(lambda: run_step("a1score.ja", M, "c" * 64), "MAPF differs")
            sa = d / "out/out/a1score"
            vr = rows_of(sa / "verify_d1v1.jsonl")
            assert len(vr) == 4 * N_SLICE and all(r["n_props"] == 2 and r["cfg"] == "d1v1" for r in vr)
            assert all(not x["abstain"] for r in vr for x in r["props"])
            assert {r["parse"] for r in rows_of(sa / "decomp_d1.jsonl")} == {"partial"}
            cl = rows_of(sa / "clip.jsonl")
            assert {r["score"] for r in cl} == {2.5 * 0.3, 0.0} and min(r["cos"] for r in cl) == -0.1, "w * max(cos, 0)"
            ja = rows_of(sa / "ja.jsonl")
            assert len(ja) == 4 * N_SLICE and all(r["j"] == "ja" and r["p_yes"] == 0.5 for r in ja)

            hrows = [{"id": i, "cap": acc[0], "tr": t, "text": "Một con mèo."} for i, _ in A[:5]
                     for t in ("punct", "nfd")]
            hb = "".join(json.dumps(r, ensure_ascii=False) + "\n" for r in hrows).encode()
            (d / "out/in/h_input.jsonl").write_bytes(hb)
            st_rest = [s for s, _ in steps("rest", reg)]
            assert st_rest[:7] == ["rest.jb", "rest.jc", "rest.decomp_d2", "rest.verify_d2v1", "rest.verify_d1v2",
                                   "rest.h_decomp", "rest.h_verify"] and st_rest[-4:] == [
                "rest.a4_decomp_d1", "rest.a4_verify_d1v1", "rest.a4_ja", "rest.a4_clip"], st_rest
            refuse(lambda: run_step("rest.jb", M, "c" * 64), "rest MAPF")
            refuse(lambda: run_step("rest.h_decomp", M, mapf, "-"), "--hin")
            refuse(lambda: run_step("rest.h_decomp", M, mapf, "e" * 64), "--hin")
            refuse(lambda: run_step("rest.a4dec.gemma3n_e4b", M, mapf), "not an A4 model")
            for st in st_rest:
                run_step(st, M, mapf, sha_bytes(hb))
            sr = d / "out/out/rest"
            assert {r["parse"] for r in rows_of(sr / "decomp_d2.jsonl")} == {"partial"}
            hv = rows_of(sr / "h_verify_d1v1.jsonl")
            assert len(hv) == 10 and {(r["tr"], r["cfg"]) for r in hv} == {("punct", "d1v1"), ("nfd", "d1v1")}
            assert all(r["ev"] == 4.5 and r["top1"] == "other" for r in rows_of(sr / "jb.jsonl"))
            assert {r["cfg"] for r in rows_of(sr / "verify_d1v2.jsonl")} == {"d1v2"}
            assert len(rows_of(sr / "a4/clip.jsonl")) == 3 * N_SLICE
            n0 = len(rows_of(sr / "jb.jsonl"))
            run_step("rest.jb", M, mapf)  # resume: finished ids are skipped
            assert len(rows_of(sr / "jb.jsonl")) == n0

            ab = (sd / "ACCEPT.json").read_text()
            (sd / "ACCEPT.json").write_text(json.dumps({"accepted": acc[:3]}))
            refuse(lambda: steps("a1decode", reg), "4 captioners")
            (sd / "ACCEPT.json").write_text(ab)
            t = json.loads((sd / "TRIM.json").read_text())
            (sd / "TRIM.json").write_text(json.dumps({**t, "kept": []}))
            assert [s for s, _ in steps("rest", reg)] == ["rest.jb", "rest.jc"]

            refuse(lambda: cmd_money_stop(NS(balance=40000, threshold=30276)), "above")
            cmd_money_stop(NS(balance=30276, threshold=30276))  # at the threshold the stop fires (rule 4: "falls to")
            refuse(lambda: steps("s", reg) and markers(), "final")
            refuse(lambda: cmd_ledger(NS(op="start", step="rest.jb", rc=0)), "final")
            os.unlink(d / "out/MONEY_STOP.json")
            lg("start", "rest.jc")
            refuse(lambda: cmd_resume(NS(cause="guard", cc="CC-301", close_sec=None)), "--close-sec")
            refuse(lambda: cmd_resume(NS(cause="guard", cc="cc301", close_sec=5)), "--cc")
            (sr / "jc.jsonl").open("a").write('{"id": 9')
            with contextlib.redirect_stdout(io.StringIO()) as buf:
                cmd_resume(NS(cause="guard", cc="CC-301", close_sec=5))
            assert "torn tail moved" in buf.getvalue() and open_step(ledger()) is None and rows_of(sr / "jc.jsonl")
            try:
                cmd_resume(NS(cause="machine", cc="CC-302", close_sec=5))
                raise AssertionError("a second resume was accepted")
            except FileExistsError:
                pass

            # CC-295 N8: a step refuses an incomplete input
            cf = dd / f"captions_{acc[0]}.jsonl"
            cb = cf.read_bytes()
            cf.write_bytes(b"".join(cb.splitlines(keepends=True)[:-1]))
            refuse(lambda: run_step("rest.jb", M, mapf), "A1-decode captions")
            cf.write_bytes(cb)
            hf = sr / "h_decomp_d1.jsonl"
            hb_ = hf.read_bytes()
            hf.write_bytes(b"".join(hb_.splitlines(keepends=True)[:-1]))
            refuse(lambda: run_step("rest.h_verify", M, mapf, sha_bytes(hb)), "H decomposition")
            hf.write_bytes(hb_)

            # CC-295 W3: the core does not fit -> CORE_STOP.json; no later block lists its steps
            t = json.loads((sd / "TRIM.json").read_text())
            (sd / "TRIM.json").write_text(json.dumps({**t, "core_fits": False}))
            refuse(lambda: steps("a1decode", reg), "core_fits")
            (sd / "TRIM.json").unlink()
            clock = time.monotonic
            try:
                lg("start", "s.trim")
                time.monotonic = lambda: clock() + 28 * 3600
                with contextlib.redirect_stdout(io.StringIO()):
                    assert run_step("s.trim", M) == CORE_RC
                lg("end", "s.trim")
            finally:
                time.monotonic = clock
            assert json.loads((sd / "TRIM.json").read_text())["core_fits"] is False and (d / "out/CORE_STOP.json").exists()
            refuse(markers, "CORE_STOP.json exists")
            refuse(lambda: cmd_ledger(NS(op="start", step="a1decode.x", rc=0)), "CORE_STOP.json exists")
            refuse(lambda: steps("a1decode", reg), "core_fits")
            os.unlink(d / "out/CORE_STOP.json")

            # PA3: fewer than 4 accepted after candidate 10
            for p in sd.iterdir():
                p.unlink()
            M.FAIL = {k: 231 for k in reg["walk"]}
            with contextlib.redirect_stdout(io.StringIO()):
                rcs = [run_step(st, M) for st, _ in steps("s", reg)[:-1]]
            assert rcs[-1] == PA3_RC and (d / "out/PA3.json").exists()
            refuse(markers, "PA3.json exists")
        finally:
            FRAME_SHA, N_SLICE = real
            del os.environ["B_PA1_OUT"], os.environ["B_PA1_HB"]
    print(json.dumps({"tier": B.LABEL, "selftest": "b_pa1_gpu ok", "checks": [
        "registry", "render", "gate", "walk", "a4", "yes-no", "digits", "decomp-parse", "trim", "project", "ids-only",
        "torn", "mem-sink", "wipe", "slice-a", "w-blocks", "cap-init", "ledger", "chain-s", "smoke-no-files",
        "chain-a1", "mapf", "chain-rest", "hin", "skip-done", "markers", "resume-once", "pa3", "lineage-switch",
        "instrument-mode", "ledger-elapsed", "used-before", "cadence", "money-boundary", "complete-inputs",
        "core-stop"]}))
    return 0


if __name__ == "__main__":
    sys.exit(main())
