#!/usr/bin/env python3
"""Paper A, A-M1: a reference-only bound on gold completeness, with a k->K prediction.
Plan: manuscript/prereg/2026-11-07_a_m1/A_M1_PLAN_v3.md (12d6ad3d, commit 8d31ed8), CC-285r3 GO 87 with its erratum
(HARD-DUE at the code read: N-F, N-G). Post hoc, descriptive, development data only (COCO-5000, UIT-ViIC 231).

  selftest [--core] [--out F]  synthetic data only (core checks; without --core also the §7.2 calibration worlds) and
                               the N-G atomic-write probe on data/results/a_m1/   -> data/results/a_m1/selftest.json
  dryrun                       asserts every pin, prints the planned work; computes and writes nothing
  freeze                       S0.1: pins, D-check freeze, selftest record     -> data/results/a_m1/freeze/freeze.json
  gate                         S0.2: G1-G6; computes no phi_j                  -> data/results/a_m1/gate.json
  run                          one attempt; refuses unless this script and the plan equal their HEAD blobs
                                                                               -> data/results/a_m1/a_m1_result.json
  status                       read-only: the §5.5 status from run_record/v1_*.json and the result file (if any)

  OMP_NUM_THREADS=2 OPENBLAS_NUM_THREADS=2 MKL_NUM_THREADS=2 nice -n 15 ~/.venvs/vsps_h1/bin/python -I -B <this file> run

Outputs hold pooled counts, estimates, intervals, labels and shas only; no caption text, no per-image class list.

Readings where the code had to interpret the plan (for the code read; CC-287 N1 numbering):
- R1 Bootstrap weights: "B multinomial weight vectors" are drawn as bincount(rng.integers(0, n, n)) per row, which is
  the uniform multinomial law (a different stream from a_dchecks.boot_weights; about 3x faster for the §7.2 worlds).
  Row 0 is the point estimate (all ones); rows 1..B are the bootstrap.
- R2 A replicate with G* <= 0 (possible only when the 2.5th percentile of G* > 0, i.e. in < 2.5% of rows) gets
  eps* = +inf. Such rows shift both percentiles upward (the lower end can rise too), so this is not one-sided
  conservative; the count of rows with G* <= 0 is recorded per set and per k ("rows_G_le_0"; expected about 0).
  A NaN percentile is read as +inf.
- R3 Seeds of the §7.2 worlds: A1 worlds default_rng([20261107 + 9000, i]), violation worlds
  default_rng([20261107 + 9000, 100 + i]) and writer-panel worlds default_rng([20261107 + 9500, i]), with i the
  configuration's index in its registry group (the plan fixes the base seeds, not the per-configuration stream).
- R4 Violation worlds: "a share nu of nameable pairs" = each pair is avoidance-type independently with probability nu.
  Forced-singleton pairs and their images count in S and in L (they are labelled nameable pairs); the w = 0 rule
  floor(3s/7 + 1/2) uses the image's final s.
- R5 a_dchecks.run_attempt is not used: its finally block fills the D-check ORDER. run_sets below is the same pattern
  (claim, steps, result written in a finally) per set, plus the V1 records of B5/N-F.
- R6 Arm U pairs are the classes named by >= 1 of the K references (unseen pairs add nothing to any count); arm L pairs
  are the labelled classes C_i, with incidence R_ik & C_i.
- R7 Status precedence (§5.5): FALSIFIED if a V1 VIOLATED is in any persisted run_record/v1_<set>.json OR in the result
  file (CC-285r3 Ruling 2 / N-F); else NOT_RUN/FAULT if a set did not complete; else METHOD or BOUND_ONLY. A set is
  COMPLETED only if a budget check after its last statistic passes (l.307 "before the cap"; CC-287 W1).
- R8 A directory fsync that raises EINVAL or ENOTSUP/EOPNOTSUPP is skipped and logged (CC-285r3 E2); any other errno
  raises. The file fsync and the rename are unchanged. `run` refuses if any v1_*.json exists, and the target is
  asserted absent right before the rename (CC-285r3 E1).
- R9 Fault and sha_file are restated here, not imported from a_dchecks: they are needed before the pin check and
  the custody hook, and a_dchecks may be imported only after its pin is asserted. After import, load_libs asserts
  their code equals a_dchecks' (CC-287 N3). Budget, CapReached, claim_start, env_guard, git_blob_sha and
  coco_complete are a_dchecks', imported after the pin check.
- R10 A passed gate.json is final (as a passed freeze.json is, plan l.335); a failed one is kept renamed.
- R11 The custody hook allows a __pycache__ file whose stem is a pinned module in the parent directory (io.open_code
  of cached bytecode). In freeze, gate and run, sys.pycache_prefix points at a fresh empty temp dir (CC-287 N4), so
  pinned modules compile from their hashed source and no repo pyc is read there.
- R12 Extra read-only subcommand `status`: the §5.5 status from the records and the result file; an unreadable
  (torn) result file is treated as absent and reported (CC-287 W3).
- R13 Failed S0 attempts: a freeze or gate that fails or raises leaves freeze/freeze.failed_<utc>_<pid>.json or
  gate.failed_<utc>_<pid>.json with its cpu_s/wall_s; run adds all of them to the budget and lists them in
  STARTED.json (plan l.335, l.344, l.439; CC-287 W2). An unreadable failed record makes run refuse before the claim.
- R14 Every JSON output is written by temp file + fsync + rename (os.replace); the result file keeps the partial
  result of run_sets on any later failure (CC-287 W3).
- Transfer notes, not code (CC-285r3 N-H..N-K): NOT_EVALUABLE prints "not evaluable"; V1 prints "consistent (low
  power)"; "AMT" stays [R] until the Chen et al. 2015 body is read; plan J9 "round 2" is now round 3.
"""
from __future__ import annotations

import argparse
import errno
import hashlib
import itertools
import json
import math
import os
import subprocess
import sys
import tempfile
import time
from pathlib import Path

import numpy as np

ROOT = Path(__file__).resolve().parents[2]
ROOT_S = str(ROOT)
SELF = "scripts/a_m1/a_m1.py"
PLAN = "manuscript/prereg/2026-11-07_a_m1/A_M1_PLAN_v3.md"
OUT = "data/results/a_m1"
REC = f"{OUT}/run_record"
DC_FREEZE = "data/results/a_dchecks/freeze"
MANIFEST = "data/coco_probe/manifest_full5000.json"
GOLD = f"{DC_FREEZE}/instance_gold_full5000.json"
R4 = ".session_backup/2026-10-26/a_full5000/out/r4_full5000_all9.json"

# ------------------------------------------------------------------------------------------------ constants (plan)
K = 5
FULL = tuple(range(K))
K_PRIMARY, KS = 3, (2, 3, 4)
DELTA_A = 0.25
B_RUN, B_SELFTEST, WORLDS = 2000, 200, 200
BASE_SEED = 20261107
SET_OFF = {"coco5000": 100, "uitviic231": 300}
SEED_SYN, SEED_WP = BASE_SEED + 9000, BASE_SEED + 9500
SETS = ("coco5000", "uitviic231")
SIZES_RUN = (1, 2, 3, 4, 5)
CAP_CPU_S = CAP_WALL_S = 3600
V1_ACCEPT = 0.05

PINS = {
    "data/datasets/karpathy/dataset_coco.json": "2fd999220673258012acfb411a4e7e66af7d488050b2519b0badcc49b7600b8d",
    MANIFEST: "699769100c572675dfc4ae9f2a45f01bf387c4b1d67e9019feafc8c14fc88f7e",
    GOLD: "bd36295146e505454f5110e817841d8300a024265c1f2cba2aade854119183f7",
    f"{DC_FREEZE}/coco5000_ids.txt": "d20da3dd48646d91a7ff7837c1c1f591d52c75e72921b2fd7f6854dc1093339f",
    f"{DC_FREEZE}/uitviic231_ids.txt": "96e6ffe998c0b4caf2eccb45c2b1379637bee2ddccdd18452eb8808dc63e8ecb",
    f"{DC_FREEZE}/freeze.json": "5237c7b2b90fa525dccf272367df90ee41f3c5def7933bda031f65c68fc928f7",
    "data/datasets/uitviic/test_data.json": "54abc0fb068ad1108d7d57b21328d4d68bcf8f41aa168f80ec7c275fb4ac8214",
    "data/uitviic/instance_gold.json": "278d15b97e3eeb9496a0282bb91deb365117becf24d174fbb1e0507203b12ea4",
    "data/coco_probe/coco80_vi.json": "926e08571ef6e80a7f8aae8f2b73753d6c5c54c431a750ba2b67bfaae71b540b",
    "data/coco_probe/chair_synonyms.txt": "b685537b36fe21b791c87151b96a991ceb582edff19f3da204dcc7a7905502f2",
    R4: "332da8b6264c9c05232e5ef70cd864a0fe7ce58480e99aee558b1115a5c793af",
    "scripts/g2b/score_g2b.py": "66c665c7a71d3b97abbf89fd5bf13871910449ad1c053ff5fb0b18663e3e7ae5",
    "scripts/score_coco_probe.py": "d11db7e192f689980bb2b2bb717d852d9aa339ad857ce9411fe7bdd6fe416070",
    "scripts/pascal50s/p50x.py": "3f562e878ed793f4b3cae84dd93373b10d82564d162cb399ab16e03ccf8825c2",
    "scripts/pascal50s/p50.py": "2387ca05ae8a57304a5f696c4e2f73d29297d03ccc23debb416269dc7a676d31",
    "scripts/a_dchecks/a_dchecks.py": "37b2946d739b476520de09d32272d452837c651369454673b38363444ffc1d36",
    "rescap/__init__.py": "b712bea4d66e5e2e0f0cec1624ab244a025560ecc5d86f96cada2e0160a4890f",
    "rescap/chair.py": "e47d249ac7290070f2387d3fa8b22dac77728265ad276f55aa6520f5cbc591a3",
    "rescap/metrics.py": "e0296ec528b87f4d1b31165cbb45deee5453783fd7dad783f248869e596bf960",
    "rescap/repro.py": "723200190818cd61a56527e6a0a1596b95f9d1ed1ebc0cabe1b29135cf03b70d",
    "rescap/svp/__init__.py": "5b7f52920de75cf59bde0ae657e292a876efc63292ca6db6a4d085bb9fec1424",
    "rescap/svp/entailment.py": "4462f44df80faa0adc620d98aa5d8bbb307243d450e9aee4801bb17a3a06db23",
    "rescap/svp/matching.py": "a9253060131aacfca8eaab9a4b2c473c487db96a7c1222f0b8e31f9f61b24003",
    "rescap/vi/__init__.py": "f898963e95fec7d9fb236295649404815634a1d949bfd74cd7c3b90ed493bf6c",
    "rescap/vi/classifier.py": "966cdab1fed8471ac57d225698e63f1e2a055435a5d669e9cca10eed703fed16",
    "rescap/vi/color.py": "242fc46f68ecb06c8eefde23350481d99e60566b3da64ab90cfa79db38fd3875",
    "rescap/vi/lexicon.py": "fbc945f2247418275144ac75b893f7c51f8951b9ea42018680d433775dd79eb9",
    "rescap/vlm/__init__.py": "13de9854599acedd32ea1798ea1acc475703fcd3aa4eb4dd715dc8eadcd632cd",
    "rescap/vlm/base.py": "e8fee5bc5b729534af67c6e462a27f0d83ba611f18ff8e3f2717b11eb393ae93",
    "rescap/vlm/mock.py": "33793de01b4f2790964342b1af2d4c2de18d793ae4693608283992475ed62ce7",
    "rescap/vlm/registry.py": "6c261406bde3d34a73f77ce961aff7d241e2a440ba75e154fccf3ae8d4a70297",
    "rescap/vocab.py": "c9143b2d973fc48a2231335844cd91ab702329c0b1aabb802884225e155967ec",
    "scripts/clean_supervision.py": "01f172002a607ba9ee55bccb332439f10650832cae1f64a9b74b35c48cd9c231",
    "scripts/person_uncap.py": "d16b19f6597f84597db7865dea4058f0bb1fecf914d71d34d6406d66283fa5bb",
    "scripts/xm3600_oiv7.py": "9a79403f4fc38609282d40082ab7f878133edca8aff9e0dc2462db467b7193f0",
    PLAN: "12d6ad3d87a01067930c3825d817b13fcb4a9a46af936357dcb9b0aad724525c",
}
CODE_PINS = tuple(p for p in PINS if p.endswith(".py")) + ("data/coco_probe/coco80_vi.json",
                                                          "data/coco_probe/chair_synonyms.txt")
# §7.1 custody: any path, anywhere, matching one of these is refused (exact pins take precedence)
DENY = (".vsps_sealed", "t2pool_", "data/xm3600", "datasets/xm3600", "xm3600_subset", "oiv7_labels", "nocaps",
        "textcaps", "ktvic", "openviic", "annot_claude", "/results/coco5000", "coco_transfer", "g2b_score/outputs")


class Fault(SystemExit):
    def __init__(self, msg: str):
        super().__init__(2)
        self.msg = msg

    def __str__(self) -> str:
        return f"FAULT: {self.msg}"


_PHASE = {"gate": False}
_HOOK = {"on": False}
_ALLOW: set[str] = set()


# ------------------------------------------------------------------------------------------------ custody (§7.1)
def _allowed(path: str) -> bool:
    p = os.path.abspath(path)
    if p in _ALLOW:
        return True
    low = p.replace(os.sep, "/").lower()
    if any(d in low for d in DENY):
        return False
    if p == ROOT_S or p.startswith(ROOT_S + os.sep):
        if p.startswith(str(ROOT / OUT) + os.sep) or p == str(ROOT / OUT):
            return True
        d = os.path.dirname(p)
        if os.path.basename(d) == "__pycache__":  # cached bytecode of a pinned module (io.open_code)
            return os.path.join(os.path.dirname(d), os.path.basename(p).split(".")[0] + ".py") in _ALLOW
        return False
    return True


def _audit(event: str, args) -> None:
    if event != "open" or not _HOOK["on"] or not args:
        return
    a = args[0]
    if isinstance(a, (str, bytes, os.PathLike)) and not _allowed(os.fsdecode(a)):
        raise Fault(f"custody: open refused: {os.fsdecode(a)}")


def install_hook() -> None:
    """Before any repo import (plan §7.1). Exact pins and this script are always allowed."""
    _ALLOW.update(str(ROOT / p) for p in (*PINS, SELF))
    if not _HOOK["on"]:
        sys.addaudithook(_audit)
        _HOOK["on"] = True


# ------------------------------------------------------------------------------------------------ pins and libraries
def sha_file(path) -> str:
    h = hashlib.sha256()
    with open(path, "rb") as fh:
        for chunk in iter(lambda: fh.read(1 << 22), b""):
            h.update(chunk)
    return h.hexdigest()


def assert_pins(paths) -> dict:
    if os.environ.get("RESCAP_RAW_TONE") == "1":
        raise Fault("RESCAP_RAW_TONE=1 changes the pinned matcher")
    bad = []
    for p in paths:
        f = ROOT / p
        got = sha_file(f) if f.is_file() else None
        if got != PINS[p]:
            bad.append(f"{p}: {got} != {PINS[p]}")
    if bad:
        raise Fault("input sha mismatch: " + "; ".join(bad))
    return {rec_key("pin", p): PINS[p] for p in paths}


def rec_key(kind: str, path: str) -> str:
    """Records are keyed by full path (CC-274 W5 i), never by basename."""
    return f"{kind}|{path}"


L: dict = {}


def _code_sig(c) -> tuple:
    """Bytecode, names and constants, recursively, without line numbers or file names (N3)."""
    return (c.co_code, c.co_names, c.co_varnames,
            tuple(_code_sig(x) if hasattr(x, "co_code") else x for x in c.co_consts))


def load_libs() -> dict:
    """Imports after the pin check; every imported repo module must be pinned (fail-closed)."""
    if L:
        return L
    sys.path[:0] = [ROOT_S, str(ROOT / "scripts"), str(ROOT / "scripts/g2b"), str(ROOT / "scripts/pascal50s"),
                    str(ROOT / "scripts/a_dchecks")]
    import a_dchecks  # noqa: E402
    import p50x  # noqa: E402
    import score_g2b  # noqa: E402
    for name, mod in list(sys.modules.items()):
        f = getattr(mod, "__file__", None)
        if name == "__main__" or not f:
            continue
        rp = Path(f).resolve()
        if rp.is_relative_to(ROOT) and str(rp.relative_to(ROOT)) not in PINS:
            raise Fault(f"imported repo module is not pinned: {rp.relative_to(ROOT)}")
    for mine, theirs in ((Fault.__init__, a_dchecks.Fault.__init__), (Fault.__str__, a_dchecks.Fault.__str__),
                         (sha_file, a_dchecks.sha_file)):
        if _code_sig(mine.__code__) != _code_sig(theirs.__code__):
            raise Fault(f"restated {mine.__qualname__} differs from a_dchecks (R9, CC-287 N3)")
    if Fault.__mro__[1] is not a_dchecks.Fault.__mro__[1]:
        raise Fault("restated Fault base differs from a_dchecks (R9)")
    L.update({"g": score_g2b, "f0": p50x.f0_hat, "dc": a_dchecks})
    return L


def jload(rel: str):
    return json.loads((ROOT / rel).read_text(encoding="utf-8"))


def _dir_fsync(d: Path, log: list | None = None) -> None:
    dfd = os.open(d, os.O_RDONLY)
    try:
        _fsync(dfd)
        if log is not None:
            log.append({"dir_fsync": "ok", "dir": d.name})
    except OSError as e:
        if e.errno not in (errno.EINVAL, errno.ENOTSUP, getattr(errno, "EOPNOTSUPP", errno.ENOTSUP)):
            raise
        if log is not None:
            log.append({"dir_fsync": f"skipped ({errno.errorcode.get(e.errno, e.errno)})", "dir": d.name})
    finally:
        os.close(dfd)


_fsync = os.fsync  # one name for every fsync, so the selftest can inject an errno (CC-287 N2 / HMa)


class _SimulatedDeath(OSError):
    """Test-only: a process death between fsync and rename; it leaves the temp file, as a dead process would."""


_TMP_N = itertools.count()


def write_json(path: Path, obj, _crash_before_rename=False) -> str:
    """Atomic: serialize first, then O_EXCL temp file, fsync, os.replace, directory fsync (CC-287 W3). Each call has
    its own temp name (pid + counter), and any in-process failure removes its temp file, so a fallback write never
    collides with a failed first write (CC-287r2 W3r2)."""
    data = (json.dumps(obj, indent=1, ensure_ascii=False) + "\n").encode("utf-8")
    path.parent.mkdir(parents=True, exist_ok=True)
    tmp = path.with_name(f".{path.name}.tmp{os.getpid()}_{next(_TMP_N)}")
    fd = os.open(tmp, os.O_WRONLY | os.O_CREAT | os.O_EXCL, 0o644)
    try:
        try:
            view = memoryview(data)
            while view:
                view = view[os.write(fd, view):]
            _fsync(fd)
        finally:
            os.close(fd)
        if _crash_before_rename:
            raise _SimulatedDeath(errno.EIO, "injected crash before rename")
        os.replace(tmp, path)
    except _SimulatedDeath:
        raise
    except BaseException:
        try:
            os.remove(tmp)
        except FileNotFoundError:
            pass
        raise
    _dir_fsync(path.parent)
    return sha_file(path)


def load_result(path: Path) -> tuple[dict | None, str]:
    """An absent or unreadable (torn) result file is treated as absent (CC-287 W3)."""
    if not path.is_file():
        return None, "absent"
    try:
        return json.loads(path.read_text(encoding="utf-8")), "read"
    except (OSError, ValueError) as e:
        return None, f"unreadable, treated as absent ({type(e).__name__})"


def out_json(rel: str, obj) -> str:
    p = ROOT / rel
    if not p.resolve().is_relative_to(ROOT / OUT):
        raise Fault(f"refused: output outside {OUT}: {rel}")
    return write_json(p, obj)


def utc() -> str:
    return time.strftime("%Y-%m-%dT%H:%M:%SZ", time.gmtime())


def cpu_s() -> float:
    t = os.times()
    return time.process_time() + t.children_user + t.children_system


# ------------------------------------------------------------------------------------------------ estimator (§2.4)
def chao_f0(phi1, phi2, k: int, target=np.inf):
    """Incidence Chao2 (k references) and its k -> target extrapolation: the pinned p50x.f0_hat, imported."""
    return L["f0"](phi1, phi2, k, target)


def combos(k: int) -> list[tuple[int, ...]]:
    return list(itertools.combinations(range(K), k))


def incidence(refs: list[list[set]], comp: list[set], arm: str) -> tuple[np.ndarray, np.ndarray]:
    """Per-pair K-vector of reference indicators. Arm U: classes named by >= 1 reference; arm L: the labelled classes
    C_i, so the indicator is c in R_ik & C_i (R6)."""
    rows, seg = [], []
    for i, (rs, c) in enumerate(zip(refs, comp)):
        if len(rs) != K:
            raise Fault(f"image {i}: {len(rs)} references, not K = {K}")
        uni = sorted(set().union(*rs)) if arm == "U" else sorted(c)
        for cl in uni:
            rows.append([cl in r for r in rs])
            seg.append(i)
    return np.array(rows, bool).reshape(-1, K), np.array(seg, np.int64)


def features(Z: np.ndarray, seg: np.ndarray, n: int, sizes) -> tuple[np.ndarray, dict]:
    """Per-image (U_A, phi1_A, phi2_A) for every position subset A of the given sizes (all C(K, k), deterministic)."""
    if _PHASE["gate"]:
        raise Fault("gate computes no phi_j (plan §6)")
    cols, blocks = {}, []
    for k in sizes:
        for A in combos(k):
            y = Z[:, list(A)].sum(1)
            cols[A] = (len(blocks), len(blocks) + 1, len(blocks) + 2)
            blocks += [np.bincount(seg, (y >= 1).astype(float), n), np.bincount(seg, (y == 1).astype(float), n),
                       np.bincount(seg, (y == 2).astype(float), n)]
    return np.column_stack(blocks), cols


def boot_weights(n: int, rng, B: int) -> np.ndarray:
    """Row 0 = point (ones); rows 1..B = image bootstrap multiplicities, uniform multinomial (R1)."""
    return np.vstack([np.ones(n)] + [np.bincount(rng.integers(0, n, n), minlength=n) for _ in range(B)]).astype(float)


def pooled(W, F, c):
    """Pooled (U, phi1, phi2) over all (image, class) pairs, one value per weight row."""
    return (W @ F[:, list(c)]).T


def s_hat(W, F, c, k: int, target=np.inf):
    U, p1, p2 = pooled(W, F, c)
    return U + chao_f0(p1, p2, k, target)


def u_bar(W, F, cols, k: int):
    return np.mean([pooled(W, F, cols[A])[0] for A in combos(k)], 0)


def u_pred(W, F, cols, k: int):
    return np.mean([s_hat(W, F, cols[A], k, K) for A in combos(k)], 0)


def s_curve(W, F, cols, k: int):
    return np.mean([s_hat(W, F, cols[A], k) for A in combos(k)], 0)


def gain_error(W, F, cols, k: int):
    """G = U_K - Ubar_k and eps_k = (Ubar(K<-k) - U_K) / G (§5.2); R2 for G <= 0."""
    U5 = pooled(W, F, cols[FULL])[0]
    G = U5 - u_bar(W, F, cols, k)
    with np.errstate(divide="ignore", invalid="ignore"):
        eps = np.where(G > 0, (u_pred(W, F, cols, k) - U5) / np.where(G > 0, G, 1.0), np.inf)
    return G, eps


# ------------------------------------------------------------------------------------------------ labels (§5.2, §5.3)
def interval(x) -> tuple[float, float]:
    lo, hi = np.percentile(np.asarray(x, float), [2.5, 97.5])
    return float(lo), float(np.inf if np.isnan(hi) else hi)


def v1_label(d_star) -> str:
    """VIOLATED iff the 97.5th percentile of D_L* < 0 (one-sided 0.025 per set); never PASS."""
    return "VIOLATED" if np.percentile(np.asarray(d_star, float), 97.5) < 0 else "CONSISTENT"


def v2a_label(g_star, e_star, e_point, delta: float = DELTA_A) -> str:
    """D3 scheme: NOT_EVALUABLE if the 2.5th pct of G* <= 0; FAIL (precedence) if the 95% interval lies wholly outside
    [-delta, delta]; PASS if inside; else UNDERPOWERED. Labels use the interval, never the point."""
    if np.percentile(np.asarray(g_star, float), 2.5) <= 0:
        return "NOT_EVALUABLE"
    lo, hi = interval(e_star)
    if hi < -delta or lo > delta:
        return "FAIL"
    if lo >= -delta and hi <= delta:
        return "PASS"
    return "UNDERPOWERED"


def ci(x) -> dict:
    x = np.asarray(x, float)
    return {"point": float(x[0]), "ci95": list(interval(x[1:]))}


# ------------------------------------------------------------------------------------------------ one set (§5)
def compute_set(FU, cU, FL, cL, ell, W, on_v1, budget, trace) -> dict:
    """E5 counts, then V1 (handed to on_v1 at once, before V2-A), then V2-A and E1-E4, all from the one W."""
    trace.append("E5")
    rec = {"n": int(W.shape[1]), "B": int(W.shape[0] - 1)}
    Lt = W @ ell
    UL = pooled(W, FL, cL[FULL])[0]
    SL = s_hat(W, FL, cL[FULL], K)
    D = (Lt - SL) / Lt
    v1 = {"label": v1_label(D[1:]), "D_L": ci(D), "S_hat_L": ci(SL), "L": float(Lt[0]), "U_L": float(UL[0])}
    trace.append("V1")
    on_v1(v1)
    rec["V1"] = v1
    budget.check()
    G, eps = gain_error(W, FU, cU, K_PRIMARY)
    rec["V2A"] = {"k": K_PRIMARY, "delta": DELTA_A, "label": v2a_label(G[1:], eps[1:], float(eps[0])),
                  "eps_3": ci(eps), "G": ci(G), "rows_G_le_0": int((G[1:] <= 0).sum())}
    trace.append("V2A")
    desc = {}
    for arm, F, c in (("U", FU, cU), ("L", FL, cL)):
        S5 = s_hat(W, F, c[FULL], K)
        U5 = pooled(W, F, c[FULL])[0]
        d = {"E1": {"S_hat": ci(S5), "C_hat_5": ci(U5 / S5), "m_hat_5": ci(1 - U5 / S5)},
             "E2": {f"S_hat({k})": ci(s_curve(W, F, c, k)) for k in (2, 3, 4, 5)},
             "E3": {f"C_hat_{k}": ci(u_bar(W, F, c, k) / S5) for k in (1, 2, 3, 4, 5)},
             "eps": {}}
        for k in ((2, 4) if arm == "U" else KS):
            Gk, ek = gain_error(W, F, c, k)
            d["eps"][f"eps_{k}"] = {**ci(ek), "G": ci(Gk), "rows_G_le_0": int((Gk[1:] <= 0).sum())}
        desc[arm] = d
    with np.errstate(divide="ignore", invalid="ignore"):
        desc["L"]["E4"] = {"c_L": ci(UL / Lt), "U_L_over_S_hat_L": ci(UL / SL),
                           "nameable_share_of_shortfall": ci((SL - UL) / (Lt - UL))}
    rec["descriptive"] = desc
    trace.append("DESC")
    return rec


def e5_counts(Z: np.ndarray) -> dict:
    y = Z.sum(1)
    return {f"phi_{j}": int((y == j).sum()) for j in range(1, K + 1)} | {"U": int((y >= 1).sum())}


# ------------------------------------------------------------------------------------------------ V1 records (B5, N-F, N-G)
def write_v1_atomic(rec_dir: Path, set_name: str, rec: dict, log: list, _crash_before_rename=False) -> Path:
    """Temp file (O_EXCL), write, fsync, assert target absent, rename, directory fsync (§7.1; CC-285r3 E1, E2)."""
    target = rec_dir / f"v1_{set_name}.json"
    tmp = rec_dir / f".v1_{set_name}.json.tmp"
    data = (json.dumps(rec, indent=1) + "\n").encode()
    fd = os.open(tmp, os.O_WRONLY | os.O_CREAT | os.O_EXCL, 0o644)
    try:
        view = memoryview(data)
        while view:
            view = view[os.write(fd, view):]
        _fsync(fd)
    finally:
        os.close(fd)
    if _crash_before_rename:
        raise OSError(errno.EIO, "injected crash before rename")
    if target.exists():
        raise Fault(f"refused: {target.name} exists (one record per set, never rewritten)")
    os.rename(tmp, target)
    sub: list = []
    _dir_fsync(rec_dir, sub)
    log.append({"v1": set_name, "dir_fsync": sub[0]["dir_fsync"]})
    return target


def read_v1(rec_dir: Path) -> dict:
    out = {}
    for s in SETS:
        f = rec_dir / f"v1_{s}.json"
        if f.is_file():
            out[s] = json.loads(f.read_text(encoding="utf-8")).get("label")
    return out


def refuse_if_records(rec_dir: Path) -> None:
    found = sorted(p.name for p in rec_dir.glob("v1_*.json")) if rec_dir.is_dir() else []
    if found:
        raise Fault(f"refused: V1 records exist ({found}); one attempt, a rerun needs a new plan version")


def status(persisted: dict, result: dict | None) -> str:
    """§5.5 precedence: FALSIFIED > NOT_RUN/FAULT > METHOD/BOUND_ONLY (R7)."""
    sets = (result or {}).get("sets") or {}
    seen = [persisted.get(s) for s in SETS] + [((sets.get(s) or {}).get("V1") or {}).get("label") for s in SETS]
    if "VIOLATED" in seen:
        return "FALSIFIED"
    if any((sets.get(s) or {}).get("state") != "COMPLETED" for s in SETS):
        return "NOT_RUN/FAULT"
    if any(sets[s]["V1"]["label"] != "CONSISTENT" for s in SETS):
        return "NOT_RUN/FAULT"
    v2 = [sets[s]["V2A"]["label"] for s in SETS]
    if v2[0] == "PASS" and v2[1] in ("PASS", "UNDERPOWERED", "NOT_EVALUABLE"):
        return "METHOD"
    return "BOUND_ONLY"


def run_sets(order, compute, budget, persist, read_persisted, write_result, res: dict | None = None) -> dict:
    """Sets in order; a cap or an exception stops the running set and all later ones. A set is COMPLETED only if the
    budget check after its last statistic passes (W1). Every in-memory V1 label goes into the result written in the
    finally (N-F); the status reads both the persisted records and the result. `res` is filled in place, so a caller
    keeps the partial result if the final write raises (W3)."""
    res = {} if res is None else res
    res.setdefault("sets", {})
    v1_mem: dict = {}
    try:
        for s in order:
            def on_v1(rec, s=s):
                v1_mem[s] = rec
                persist(s, rec)
            try:
                budget.check()
                out = compute(s, on_v1)
                budget.check()  # W1: "completed ... before the cap" (plan l.307)
                res["sets"][s] = {**out, "state": "COMPLETED"}
            except L["dc"].CapReached as e:
                res["sets"][s] = {"state": "NOT_RUN", "reason": f"cap reached during {s} ({e})"}
                break
            except (Exception, SystemExit) as e:  # noqa: BLE001  (recorded, never escapes)
                res["sets"][s] = {"state": "FAULT", "reason": f"{type(e).__name__}: {str(e)[:300]}"}
                break
    finally:
        for s in order:
            res["sets"].setdefault(s, {"state": "NOT_RUN", "reason": "not reached"})
        for s, rec in v1_mem.items():
            res["sets"][s]["V1"] = rec
        try:
            persisted = read_persisted()
        except Exception as e:  # noqa: BLE001
            persisted, res["persisted_read_error"] = {}, f"{type(e).__name__}: {e}"
        res["persisted_v1"] = persisted
        res["status"] = status(persisted, res)
        write_result(res)
    return res


def finish_after_failure(res: dict, err: BaseException, read_persisted, write_result) -> dict:
    """W3 fallback: keep the partial result of run_sets (every in-memory V1 and finished label), fill the sets not
    reached, recompute the status from both artefacts, and write it."""
    res.setdefault("sets", {})
    for s in SETS:
        res["sets"].setdefault(s, {"state": "NOT_RUN", "reason": "failure before the set"})
    res["fault_outside_sets"] = f"{type(err).__name__}: {str(err)[:300]}"
    try:
        persisted = read_persisted()
    except Exception as e:  # noqa: BLE001
        persisted, res["persisted_read_error"] = {}, f"{type(e).__name__}: {e}"
    res["persisted_v1"] = persisted
    res["status"] = status(persisted, res)
    write_result(res)
    return res


def s0_failed(out_dir: Path) -> tuple[float, float, list]:
    """W2: cpu_s and wall_s summed over every failed freeze and gate record (plan l.335, l.439)."""
    files = sorted((out_dir / "freeze").glob("freeze.failed_*.json")) + sorted(out_dir.glob("gate.failed_*.json"))
    cpu = wall = 0.0
    for f in files:
        try:
            r = json.loads(f.read_text(encoding="utf-8"))
            cpu, wall = cpu + float(r["cpu_s"]), wall + float(r["wall_s"])
        except (OSError, ValueError, KeyError, TypeError) as e:
            raise Fault(f"refused: failed S0 record unreadable: {f.name} ({type(e).__name__})") from None
    return cpu, wall, [str(f.relative_to(out_dir)) for f in files]


def stamp() -> str:
    return f"{time.strftime('%Y%m%dT%H%M%SZ', time.gmtime())}_{os.getpid()}"


def s0_attempt(kind: str, body, out_root: Path | None = None) -> int:
    """W2: a freeze or gate attempt that raises leaves a failed record with its time, then re-raises. out_root is
    data/results/a_m1/ except in the selftest, which uses a scratch dir (CC-287r2 N-b)."""
    root = ROOT / OUT if out_root is None else out_root
    t0, c0 = time.monotonic(), cpu_s()
    try:
        return body(t0, c0)
    except BaseException as e:
        path = root / "freeze" / f"freeze.failed_{stamp()}.json" if kind == "freeze" else root / f"gate.failed_{stamp()}.json"
        try:
            write_json(path, {"schema": f"vsps.a_m1.{kind}.failed.v1", "utc": utc(), "pass": False,
                           "error": f"{type(e).__name__}: {str(e)[:300]}", "cpu_s": cpu_s() - c0,
                           "wall_s": time.monotonic() - t0})
        except Exception:  # noqa: BLE001  (the original error is the one that matters)
            pass
        raise


def fresh_pycache() -> None:
    """N4: compile pinned modules from their hashed source; no repo pyc is read in freeze, gate or run."""
    sys.pycache_prefix = tempfile.mkdtemp(prefix="a_m1_pyc_")


# ------------------------------------------------------------------------------------------------ real data (§2.1, §4)
def coco_refs(kr: dict, ids: list[str], fn) -> list[list[set]]:
    if any(len(kr[int(i)]) < K for i in ids):
        raise Fault("a COCO image has fewer than 5 references")
    return [[fn(s) for s in kr[int(i)][:K]] for i in ids]


def load_sets() -> dict:
    g, dc = L["g"], L["dc"]
    ids = [str(i) for i in sorted(int(m["cocoid"]) for m in jload(MANIFEST)["images"])]
    kr = g.karpathy_refs({int(i) for i in ids})
    coco = {"ids": ids, "refs": coco_refs(kr, ids, lambda s: g.sc.en_classes(s, g.SYN)),
            "comp": dc.coco_complete(ids, jload(GOLD))}
    u = g.uitviic_context()
    lx = u["lexicons"]["coco80"]
    uit = {"ids": u["ids"], "refs": lx["refs"], "comp": lx["complete"]}
    return {"coco5000": coco, "uitviic231": uit}


def frozen_ids() -> dict:
    return {"coco5000": (ROOT / DC_FREEZE / "coco5000_ids.txt").read_text(encoding="utf-8").split(),
            "uitviic231": (ROOT / DC_FREEZE / "uitviic231_ids.txt").read_text(encoding="utf-8").split()}


def gate_core(sets: dict, r4u: dict, frozen: dict) -> tuple[dict, bool]:
    """G1-G4 (plan §6); computes no phi_j (the features() guard is armed)."""
    _PHASE["gate"] = True
    try:
        rec = {"G1": {s: sets[s]["ids"] == frozen[s] for s in SETS},
               "G2": {s: all(len(r) == K for r in sets[s]["refs"]) for s in SETS}}
        refs, comp = sets["coco5000"]["refs"], sets["coco5000"]["comp"]
        n = len(refs)
        got = {f"refs{k}_firstk": round(sum(len(set().union(*r[:k])) for r in refs) / n, 3) for k in range(1, K + 1)}
        got["inst"] = round(sum(len(c) for c in comp) / n, 3)
        rec["G3"] = {key: {"got": v, "r4": r4u.get(key), "ok": v == r4u.get(key)} for key, v in got.items()}
        rec["G4"] = {"n": len(sets["uitviic231"]["ids"]), "sum_ell": sum(len(c) for c in sets["uitviic231"]["comp"])}
        ok = all(rec["G1"].values()) and all(rec["G2"].values()) and all(v["ok"] for v in rec["G3"].values()) \
            and rec["G4"]["n"] == 231
        return rec, ok
    finally:
        _PHASE["gate"] = False


def compute_real(d: dict, set_name: str, on_v1, budget, trace) -> dict:
    n = len(d["ids"])
    ZU, segU = incidence(d["refs"], d["comp"], "U")
    ZL, segL = incidence(d["refs"], d["comp"], "L")
    FU, cU = features(ZU, segU, n, SIZES_RUN)
    FL, cL = features(ZL, segL, n, SIZES_RUN)
    ell = np.array([len(c) for c in d["comp"]], float)
    seed = BASE_SEED + SET_OFF[set_name]
    W = boot_weights(n, np.random.default_rng(seed), B_RUN)
    rec = compute_set(FU, cU, FL, cL, ell, W, on_v1, budget, trace)
    return {"seed": seed, "E5": {"U": e5_counts(ZU), "L": e5_counts(ZL) | {"L": int(ell.sum())}}, **rec}


# ------------------------------------------------------------------------------------------------ synthetic worlds (§7.2)
LAWS = (("beta", 2.0, 2.0), ("beta", 1.0, 1.0), ("beta", 0.5, 1.0), ("beta", 0.3, 0.6), ("const", 0.4, None))
WP_M_MULT = (0.6, 0.8, 1.0, 1.2, 1.4)
WP_D_GRID = ((0.5, 0.2), (0.6, 0.05), (0.8, 0.1))
WP_EXPECTED = ("WP-M", "WP-D(0.5,0.2)", "WP-D(0.6,0.05)", "WP-D(0.8,0.1)")


def registry() -> dict:
    a1 = [{"name": f"A1 n={n} lam={lam} {law[0]}({law[1]},{law[2]})", "kind": "A1", "n": n, "lam": lam, "law": law}
          for n in (231, 5000) for lam in (2, 4) for law in LAWS]
    vi = [{"name": f"{kind} n={n}", "kind": kind, "n": n, "lam": 2, "par": par}
          for n in (231, 5000) for kind, par in (("avoid0.1", 0.1), ("avoid0.3", 0.3), ("avoid0.5", 0.5),
                                                  ("forced", None), ("copy", None))]
    wp = [{"name": f"WP-M n={n}", "kind": "WP-M", "n": n, "lam": 2, "par": WP_M_MULT} for n in (231, 5000)] + \
         [{"name": f"WP-D({ph},{pl}) n={n}", "kind": "WP-D", "n": n, "lam": 2, "par": (ph, pl)}
          for n in (231, 5000) for ph, pl in WP_D_GRID]
    return {"A1": a1, "violation": vi, "WP": wp}


def assert_registry(reg: dict) -> None:
    """The selftest refuses to pass if any writer-panel configuration is missing (mutant 18, N10)."""
    names = {c["name"] for c in reg["WP"]}
    want = {f"{w} n={n}" for w in WP_EXPECTED for n in (231, 5000)}
    if names != want:
        raise Fault(f"WP registry incomplete: missing {sorted(want - names)}")
    if len(reg["A1"]) != 20 or len(reg["violation"]) != 10:
        raise Fault("A1 or violation registry incomplete")


def n_unnamed(s: np.ndarray) -> np.ndarray:
    """N-C: floor(3s/7 + 1/2) labelled pairs with w = 0 per image."""
    return np.floor(3 * np.asarray(s) / 7 + 0.5).astype(np.int64)


def synth_world(rng, cfg: dict) -> tuple[np.ndarray, np.ndarray, np.ndarray, int]:
    n, kind = cfg["n"], cfg["kind"]
    s = 1 + rng.poisson(cfg["lam"], n)
    seg = np.repeat(np.arange(n), s)
    P = int(s.sum())
    if kind == "A1":
        fam, a, b = cfg["law"]
        w = rng.beta(a, b, P) if fam == "beta" else np.full(P, a)
        Z = rng.random((P, K)) < w[:, None]
    else:
        w = rng.beta(0.5, 1.0, P)
        if kind == "WP-M":
            Z = rng.random((P, K)) < np.minimum(1.0, w[:, None] * np.array(cfg["par"])[None])
        elif kind == "WP-D":
            p = np.full((P, K), cfg["par"][1])
            p[np.arange(P), rng.integers(0, K, P)] = cfg["par"][0]
            Z = rng.random((P, K)) < p
        else:
            Z = rng.random((P, K)) < w[:, None]
            if kind.startswith("avoid"):
                av = rng.random(P) < cfg["par"]
                Z[av] = False
                hit = av & (rng.random(P) < 0.6)
                Z[hit, rng.integers(0, K, P)[hit]] = True
            elif kind == "forced":
                extra = np.flatnonzero(rng.random(n) < 0.5)
                Ze = np.zeros((extra.size, K), bool)
                Ze[np.arange(extra.size), rng.integers(0, K, extra.size)] = True
                Z, seg = np.vstack([Z, Ze]), np.concatenate([seg, extra])
                s = s + np.bincount(extra, minlength=n)
            elif kind == "copy":
                for k in range(1, K):
                    m = (rng.random(n) < 0.5)[seg]
                    Z[m, k] = Z[m, k - 1]
    ell = (s + n_unnamed(s)).astype(float)
    return Z, seg, ell, int(s.sum())


def eval_world(rng, cfg: dict, B: int = B_SELFTEST) -> dict:
    Z, seg, ell, S = synth_world(rng, cfg)
    n = cfg["n"]
    F, c = features(Z, seg, n, (K_PRIMARY, K))
    W = boot_weights(n, rng, B)
    SL = s_hat(W, F, c[FULL], K)
    Lt = W @ ell
    G, eps = gain_error(W, F, c, K_PRIMARY)
    return {"S_hat_over_S": float(SL[0] / S), "S_hat_le_S": bool(SL[0] <= S),
            "V1": v1_label(((Lt - SL) / Lt)[1:]), "V2A": v2a_label(G[1:], eps[1:], float(eps[0]))}


def flag(mean_ratio: float, share_le: float, v1_rate: float) -> str:
    if mean_ratio <= 1:
        return "BOUND_HOLDS" if share_le >= 0.95 else "MARGINAL"
    return "BREAKS_DETECTED" if v1_rate >= 0.8 else "BREAKS_UNDETECTED"


def calibrate(worlds: int = WORLDS) -> dict:
    reg = registry()
    assert_registry(reg)
    out = {}
    for group, cfgs in reg.items():
        base = SEED_WP if group == "WP" else SEED_SYN
        for i, cfg in enumerate(cfgs):
            rng = np.random.default_rng([base, i if group != "violation" else 100 + i])
            rs = [eval_world(rng, cfg) for _ in range(worlds)]
            ratio = float(np.mean([r["S_hat_over_S"] for r in rs]))
            share = float(np.mean([r["S_hat_le_S"] for r in rs]))
            v1r = float(np.mean([r["V1"] == "VIOLATED" for r in rs]))
            rec = {"group": group, "worlds": worlds, "V1_violated_rate": v1r, "share_S_hat_le_S": share,
                   "mean_S_hat_over_S": ratio,
                   "V2A_rates": {lab: float(np.mean([r["V2A"] == lab for r in rs]))
                                 for lab in ("PASS", "FAIL", "UNDERPOWERED", "NOT_EVALUABLE")}}
            if group == "WP":
                rec["flag"] = flag(ratio, share, v1r)
            out[cfg["name"]] = rec
    a1_ok = all(v["V1_violated_rate"] <= V1_ACCEPT for v in out.values() if v["group"] == "A1")
    fires = any(v.get("flag") in ("BREAKS_UNDETECTED", "MARGINAL") for k, v in out.items()
                if v["group"] == "WP" and k.endswith("n=231"))
    return {"configs": out, "acceptance_A1_V1_le_0.05": a1_ok, "uit_s5_only_rule_fires": fires,
            "note": "synthetic; never printed in the paper (plan §7.2)"}


# ------------------------------------------------------------------------------------------------ selftest
def probe_atomic_write() -> dict:
    """N-G: the registered atomic write on the real data/results/a_m1/ filesystem, in a scratch subdir (never
    run_record/), removed with os.remove of named files and os.rmdir."""
    d = ROOT / OUT / f"_selftest_probe_{os.getpid()}"
    if d.resolve().is_relative_to((ROOT / REC).resolve()):
        raise Fault("probe must not write under run_record/")
    d.mkdir(parents=True, exist_ok=False)
    log: list = []
    try:
        t = write_v1_atomic(d, "probe", {"label": "CONSISTENT", "probe": True}, log)
        ok = json.loads(t.read_text(encoding="utf-8"))["label"] == "CONSISTENT" and not (d / ".v1_probe.json.tmp").exists()
        try:
            write_v1_atomic(d, "probe", {"label": "x"}, log)
            refused = False
        except Fault:
            refused = True
    finally:
        for name in ("v1_probe.json", ".v1_probe.json.tmp"):
            if (d / name).exists():
                os.remove(d / name)
        os.rmdir(d)
    return {"ok": bool(ok and refused), "dir": str(d.relative_to(ROOT)), "log": log, "second_write_refused": refused}


def synth_set(rng, n=40):
    """Tiny labelled set with reference classes outside C_i and order-dependent references."""
    vocab = [f"c{j}" for j in range(8)]
    refs, comp = [], []
    for i in range(n):
        c = set(rng.choice(vocab, size=rng.integers(1, 5), replace=False).tolist())
        rs = []
        for k in range(K):
            r = {x for x in c if rng.random() < (0.9 if k == 0 else 0.35)}
            if rng.random() < 0.3:
                r.add("c_out")
            rs.append(r)
        refs.append(rs)
        comp.append(c)
    return refs, comp


def stat_is_dir(fd: int) -> bool:
    import stat
    return stat.S_ISDIR(os.fstat(fd).st_mode)


class _FakeClock:
    def __init__(self, cap_after: int):
        self.calls, self.cap_after = 0, cap_after

    def __call__(self):
        self.calls += 1
        return (1e9, 0.0) if self.calls > self.cap_after else (0.0, 0.0)


def selftest_core() -> dict:
    checks: dict[str, bool] = {}

    def check(name, fn):
        try:
            checks[name] = bool(fn())
        except (Exception, SystemExit) as e:  # noqa: BLE001
            checks[name] = False
            checks[f"{name} [raised {type(e).__name__}: {str(e)[:80]}]"] = False

    rng = np.random.default_rng(11)

    # estimator parity (mutants 2, 3)
    check("f0_hat: Chao2 3.2, bias-corrected 4.8 at phi2 = 0, t = 0 adds 0, closed forms",
          lambda: np.isclose(chao_f0(4, 2, 5), 3.2) and np.isclose(chao_f0(4, 0, 5), 4.8)
          and float(chao_f0(5, 2, 3, 3)) == 0.0
          and np.isclose(chao_f0(7.0, 3.0, 3), (2 / 3) * 49 / 6) and np.isclose(chao_f0(7.0, 0.0, 4), 0.75 * 21))

    # Lemma 1, exact expectations
    def lemma1():
        r = np.random.default_rng(3)
        for _ in range(10_000):
            k = int(r.integers(2, 6))
            w = r.uniform(0.01, 0.99, int(r.integers(1, 20)))
            e1 = (k * w * (1 - w) ** (k - 1)).sum()
            e2 = (math.comb(k, 2) * w ** 2 * (1 - w) ** (k - 2)).sum()
            ef0 = ((1 - w) ** k).sum()
            if ef0 < (k - 1) / k * e1 ** 2 / (2 * e2) * (1 - 1e-12):
                return False
        w = np.full(7, 0.37)
        for k in (3, 4, 5):
            e1, e2 = (k * w * (1 - w) ** (k - 1)).sum(), (math.comb(k, 2) * w ** 2 * (1 - w) ** (k - 2)).sum()
            if not np.isclose(((1 - w) ** k).sum(), (k - 1) / k * e1 ** 2 / (2 * e2)):
                return False
        return True
    check("Lemma 1: E f0 >= ((K-1)/K)(E phi1)^2/(2 E phi2) on 10,000 w vectors; equality at constant w", lemma1)

    refs, comp = synth_set(rng)
    n = len(refs)
    ZU, segU = incidence(refs, comp, "U")
    ZL, segL = incidence(refs, comp, "L")
    FU, cU = features(ZU, segU, n, SIZES_RUN)
    FL, cL = features(ZL, segL, n, SIZES_RUN)
    ones = np.ones((1, n))

    # pooled, not per image (mutant 1)
    def pooled_check():
        U, p1, p2 = ZU.any(1).sum(), (ZU.sum(1) == 1).sum(), (ZU.sum(1) == 2).sum()
        return np.isclose(s_hat(ones, FU, cU[FULL], K)[0], U + chao_f0(float(p1), float(p2), K))
    check("estimator pooled over (image, class) pairs, not summed per image", pooled_check)

    # all subsets, rarefaction identity, G and the prediction by brute force (mutants 4, 5, 13)
    def brute():
        y = ZU.sum(1)
        for k in (1, 2, 3, 4):
            rare = sum(1 - math.comb(K - int(v), k) / math.comb(K, k) for v in y)
            if not np.isclose(u_bar(ones, FU, cU, k)[0], rare):
                return False
        subs = list(itertools.combinations(range(K), 3))
        if len(combos(3)) != 10 or set(combos(3)) != set(subs):
            return False
        def upred(A):
            yy = ZU[:, list(A)].sum(1)
            U, p1, p2 = (yy >= 1).sum(), (yy == 1).sum(), (yy == 2).sum()
            return U + float(chao_f0(float(p1), float(p2), 3, K))
        pred = np.mean([upred(A) for A in subs])
        U5 = ZU.any(1).sum()
        Ub = np.mean([ZU[:, list(A)].any(1).sum() for A in subs])
        G, e = gain_error(ones, FU, cU, 3)
        return np.isclose(u_pred(ones, FU, cU, 3)[0], pred) and np.isclose(G[0], U5 - Ub) \
            and np.isclose(e[0], (pred - U5) / (U5 - Ub))
    check("all C(5,k) subsets; rarefaction identity; G and the k->K prediction equal brute force", brute)

    # labels and intervals (mutants 6, 7, 8, 12)
    check("interval = 2.5th and 97.5th percentiles", lambda: interval(np.arange(1001.0)) == (25.0, 975.0))
    check("V1: VIOLATED iff 97.5th pct of D_L* < 0; labels CONSISTENT/VIOLATED only",
          lambda: v1_label(np.linspace(-0.2, -0.01, 401)) == "VIOLATED"
          and v1_label(np.linspace(-0.2, 0.05, 401)) == "CONSISTENT"
          and v1_label(np.linspace(0.01, 0.3, 401)) == "CONSISTENT")
    g_pos = np.linspace(1, 2, 401)
    check("V2-A labels from the interval (D3 scheme), never the point",
          lambda: v2a_label(g_pos, np.linspace(-0.5, 0.5, 401), 0.0) == "UNDERPOWERED"
          and v2a_label(g_pos, np.linspace(-0.2, 0.2, 401), 0.9) == "PASS"
          and v2a_label(g_pos, np.linspace(-0.9, -0.3, 401), 0.0) == "FAIL"
          and v2a_label(g_pos, np.linspace(0.3, 0.9, 401), 0.0) == "FAIL"
          and v2a_label(np.linspace(-1, 2, 401), np.zeros(401), 0.0) == "NOT_EVALUABLE"
          and v2a_label(g_pos, np.linspace(-0.3, 0.2, 401), 0.0) == "UNDERPOWERED")

    # arm L intersection (mutant 9) and first-5 references (mutant 10)
    check("arm L incidence = R_ik & C_i (classes outside C_i dropped)",
          lambda: ZL.shape[0] == sum(len(c) for c in comp)
          and FL[:, cL[FULL][0]].sum() == sum(len(set().union(*r) & c) for r, c in zip(refs, comp)))
    check("COCO: exactly the first 5 references", lambda: [len(r) for r in coco_refs(
        {1: [f"s{j}" for j in range(7)], 2: [f"s{j}" for j in range(5)]}, ["1", "2"], lambda s: {s})] == [5, 5])

    # custody hook (mutant 11): the probe paths do not exist, so nothing is read if the hook fails
    def custody():
        install_hook()
        bad = 0
        for rel in ("data/xm3600/__a_m1_probe_nonexistent__.json", "data/results/coco5000/__a_m1_probe__.jsonl",
                    "data/__a_m1_probe_nonexistent__.json"):
            try:
                open(ROOT / rel, encoding="utf-8").close()
            except Fault:
                continue
            except OSError:
                bad += 1
        return bad == 0 and _allowed(str(ROOT / "scripts/__pycache__/xm3600_oiv7.cpython-312.pyc")) \
            and not _allowed(str(Path.home() / ".vsps_sealed" / "x")) and _allowed(str(ROOT / OUT / "x.json"))
    check("custody: deny patterns, system outputs and unpinned repo paths FAULT; pinned pyc and OUT allowed", custody)

    # one weight matrix shared by every statistic (mutants 13, 14): degenerate weights collapse every interval
    def degenerate():
        tr: list = []
        r = compute_set(FU, cU, FL, cL, np.array([len(c) for c in comp], float), np.ones((21, n)),
                        lambda v: None, L["dc"].Budget(CAP_CPU_S, CAP_WALL_S), tr)
        vals = [r["V1"]["D_L"], r["V2A"]["eps_3"], r["descriptive"]["U"]["E1"]["S_hat"],
                r["descriptive"]["L"]["E4"]["c_L"], r["descriptive"]["U"]["eps"]["eps_2"]]
        return all(np.isclose(v["ci95"][0], v["point"]) and np.isclose(v["ci95"][1], v["point"]) for v in vals)
    check("one shared weight matrix: identical rows collapse every interval to the point", degenerate)

    check("records keyed by full path", lambda: rec_key("pin", "a/x.json") != rec_key("pin", "b/x.json"))

    # gate computes no phi_j (mutant 16)
    def gate_guard():
        sets = {"coco5000": {"ids": [str(i) for i in range(n)], "refs": refs, "comp": comp},
                "uitviic231": {"ids": [str(i) for i in range(231)], "refs": [refs[0]] * 231, "comp": [comp[0]] * 231}}
        rec, _ = gate_core(sets, {}, {"coco5000": sets["coco5000"]["ids"], "uitviic231": sets["uitviic231"]["ids"]})
        try:
            _PHASE["gate"] = True
            features(ZU, segU, n, (K,))
            armed = False
        except Fault:
            armed = True
        finally:
            _PHASE["gate"] = False
        return armed and rec["G1"]["coco5000"] and set(rec) == {"G1", "G2", "G3", "G4"}
    check("gate: computes no phi_j (guard armed), G1-G4 only", gate_guard)

    # precedence and the V1 records (mutants 17, 17b, 17c, 17d), in a scratch dir outside the repo
    def scenario(plan_, cap_after=None, persist_fail=False):
        d = Path(tempfile.mkdtemp(prefix="a_m1_st_"))
        log, results = [], {}
        try:
            def persist(s, rec):
                if persist_fail:
                    raise OSError(errno.EIO, "injected V1 write failure")
                write_v1_atomic(d, s, rec, log)

            def compute(s, on_v1):
                p = plan_[s]
                if p == "skip":
                    raise RuntimeError("fault before V1")
                on_v1({"label": p["v1"]})
                if p.get("raise_after_v1"):
                    raise RuntimeError("fault after V1")
                budget.check()
                return {"V1": {"label": p["v1"]}, "V2A": {"label": p.get("v2a", "PASS")}}
            budget = L["dc"].Budget(CAP_CPU_S, CAP_WALL_S, clock=_FakeClock(cap_after if cap_after is not None else 10 ** 9))
            res = run_sets(SETS, compute, budget, persist, lambda: read_v1(d), lambda r: results.update(r))
            return res["status"], status(read_v1(d), None)
        finally:
            for f in d.iterdir():
                os.remove(f)
            os.rmdir(d)
    V, C = "VIOLATED", "CONSISTENT"
    check("17: COCO VIOLATED then UIT FAULT -> FALSIFIED",
          lambda: scenario({"coco5000": {"v1": V}, "uitviic231": "skip"})[0] == "FALSIFIED")
    check("17: no VIOLATED and a FAULT -> NOT_RUN/FAULT; both CONSISTENT -> METHOD/BOUND_ONLY",
          lambda: scenario({"coco5000": {"v1": C}, "uitviic231": "skip"})[0] == "NOT_RUN/FAULT"
          and scenario({"coco5000": {"v1": C}, "uitviic231": {"v1": C}})[0] == "METHOD"
          and scenario({"coco5000": {"v1": C, "v2a": "FAIL"}, "uitviic231": {"v1": C}})[0] == "BOUND_ONLY")
    check("17b: exception inside COCO after V1 VIOLATED -> FALSIFIED",
          lambda: scenario({"coco5000": {"v1": V, "raise_after_v1": True}, "uitviic231": {"v1": C}})[0] == "FALSIFIED")
    check("17b: cap inside COCO after V1 VIOLATED -> FALSIFIED",
          lambda: scenario({"coco5000": {"v1": V}, "uitviic231": {"v1": C}}, cap_after=2)[0] == "FALSIFIED")
    check("17c: dead run after COCO VIOLATED (no result file) -> FALSIFIED from the persisted record",
          lambda: scenario({"coco5000": {"v1": V}, "uitviic231": "skip"})[1] == "FALSIFIED"
          and status({}, None) == "NOT_RUN/FAULT" and status({"coco5000": C}, None) == "NOT_RUN/FAULT")
    check("17d: V1 write fails after VIOLATED -> the result still says VIOLATED -> FALSIFIED",
          lambda: scenario({"coco5000": {"v1": V}, "uitviic231": {"v1": C}}, persist_fail=True)[0] == "FALSIFIED")

    def atomic():
        d = Path(tempfile.mkdtemp(prefix="a_m1_at_"))
        log: list = []
        try:
            try:
                write_v1_atomic(d, "coco5000", {"label": V}, log, _crash_before_rename=True)
            except OSError:
                pass
            no_target = not (d / "v1_coco5000.json").exists()
            os.remove(d / ".v1_coco5000.json.tmp")
            write_v1_atomic(d, "coco5000", {"label": V}, log)
            try:
                write_v1_atomic(d, "coco5000", {"label": C}, log)
                again = False
            except Fault:
                again = True
            try:
                refuse_if_records(d)
                refused = False
            except Fault:
                refused = True
            return no_target and again and refused and read_v1(d) == {"coco5000": V}
        finally:
            for f in d.iterdir():
                os.remove(f)
            os.rmdir(d)
    check("17c: V1 write is atomic (no target before rename), never rewritten; run refuses with records", atomic)

    def order():
        tr: list = []
        seen = {}
        compute_set(FU, cU, FL, cL, np.array([len(c) for c in comp], float), boot_weights(n, rng, 20),
                    lambda v: seen.setdefault("at", list(tr)), L["dc"].Budget(CAP_CPU_S, CAP_WALL_S), tr)
        return seen["at"] == ["E5", "V1"] and tr == ["E5", "V1", "V2A", "DESC"]
    check("17c: V1 handed over before V2-A", order)

    # CC-287 W1: cap crossed after V1 and before the return -> NOT_RUN, never COMPLETED; VIOLATED still FALSIFIED
    def w1_scenario(v1):
        d = Path(tempfile.mkdtemp(prefix="a_m1_w1_"))
        try:
            budget = L["dc"].Budget(CAP_CPU_S, CAP_WALL_S, clock=_FakeClock(3))
            res = run_sets(SETS, lambda s, on_v1: (on_v1({"label": v1}), budget.check(),
                                                   {"V1": {"label": v1}, "V2A": {"label": "PASS"}})[2],
                           budget, lambda s, r: write_v1_atomic(d, s, r, []), lambda: read_v1(d), lambda r: None)
            return res["sets"]["coco5000"]["state"], res["status"]
        finally:
            for f in d.iterdir():
                os.remove(f)
            os.rmdir(d)
    check("W1: a set past the cap after V1 is NOT_RUN, not COMPLETED; VIOLATED there is still FALSIFIED",
          lambda: w1_scenario(C) == ("NOT_RUN", "NOT_RUN/FAULT") and w1_scenario(V) == ("NOT_RUN", "FALSIFIED"))

    # CC-287 N2 / HMi: a FAULT after a CONSISTENT V1 is not COMPLETED
    check("HMi: FAULT after a CONSISTENT V1 -> NOT_RUN/FAULT (l.307)",
          lambda: scenario({"coco5000": {"v1": C, "raise_after_v1": True}, "uitviic231": {"v1": C}})[0]
          == "NOT_RUN/FAULT"
          and scenario({"coco5000": {"v1": C}, "uitviic231": {"v1": C, "raise_after_v1": True}})[0] == "NOT_RUN/FAULT")

    # CC-287 W2: failed S0 time summed
    def w2():
        d = Path(tempfile.mkdtemp(prefix="a_m1_w2_"))
        made = [d / "freeze" / "freeze.failed_a.json", d / "gate.failed_b.json", d / "gate.json", d / "freeze" / "freeze.json"]
        try:
            for f, r in zip(made, ({"cpu_s": 1.5, "wall_s": 2.0}, {"cpu_s": 3.0, "wall_s": 4.5},
                                   {"cpu_s": 100.0, "wall_s": 100.0, "pass": True},
                                   {"cpu_s": 100.0, "wall_s": 100.0, "pass": True})):
                write_json(f, r)
            cpu, wall, names = s0_failed(d)
            ok = (cpu, wall) == (4.5, 6.5) and names == ["freeze/freeze.failed_a.json", "gate.failed_b.json"]
            (d / "gate.failed_c.json").write_text("{torn", encoding="utf-8")
            made.append(d / "gate.failed_c.json")
            try:
                s0_failed(d)
                refused = False
            except Fault:
                refused = True
            return ok and refused
        finally:
            for f in made:
                if f.exists():
                    os.remove(f)
            os.rmdir(d / "freeze")
            os.rmdir(d)
    check("W2: failed freeze/gate time summed into the budget; an unreadable failed record refuses", w2)

    def w2_attempt():
        d = Path(tempfile.mkdtemp(prefix="a_m1_w2a_"))  # N-b: scratch root, never the live data/results/a_m1/
        try:
            ok = True
            for kind, exc in (("gate", RuntimeError("injected S0 failure")), ("freeze", Fault("injected S0 Fault"))):
                try:
                    s0_attempt(kind, lambda t0, c0, exc=exc: (_ for _ in ()).throw(exc), out_root=d)
                    ok = False
                except (RuntimeError, SystemExit):
                    pass
            files = sorted(d.glob("gate.failed_*.json")) + sorted((d / "freeze").glob("freeze.failed_*.json"))
            recs = [json.loads(f.read_text(encoding="utf-8")) for f in files]
            cpu, wall, names = s0_failed(d)
            return ok and len(files) == 2 and all(r.get("pass") is False and "cpu_s" in r and "wall_s" in r
                                                  for r in recs) and len(names) == 2 \
                and not set((ROOT / OUT).glob("gate.failed_*.json"))
        finally:
            for f in list(d.glob("gate.failed_*.json")) + list((d / "freeze").glob("freeze.failed_*.json")):
                os.remove(f)
            if (d / "freeze").is_dir():
                os.rmdir(d / "freeze")
            os.rmdir(d)
    check("W2: a raising S0 attempt (exception or Fault) leaves a failed record with its time, then re-raises; "
          "selftest writes it to a scratch root", w2_attempt)

    # CC-287 W3: persist fails, the first result write fails, the fallback keeps the in-memory V1 -> FALSIFIED;
    # atomic result write; torn result read as absent; real compute_set output and V1 dict JSON round-trip
    def w3():
        d = Path(tempfile.mkdtemp(prefix="a_m1_w3_"))
        res_path = d / "a_m1_result.json"
        calls = {"n": 0}

        def write_result(r):
            calls["n"] += 1
            if calls["n"] == 1:
                raise OSError(errno.EIO, "injected first result write failure")
            write_json(res_path, r)

        def persist(s, r):
            raise OSError(errno.EIO, "injected V1 write failure")
        res: dict = {}
        try:
            try:
                run_sets(SETS, lambda s, on_v1: (on_v1({"label": V}), {"V1": {"label": V}})[1],
                         L["dc"].Budget(CAP_CPU_S, CAP_WALL_S), persist, lambda: read_v1(d), write_result, res)
            except OSError as e:
                finish_after_failure(res, e, lambda: read_v1(d), write_result)
            loaded, how = load_result(res_path)
            ok = how == "read" and status(read_v1(d), loaded) == "FALSIFIED" \
                and loaded["sets"]["coco5000"]["V1"]["label"] == V
            res_path.write_text('{"sets": {"coco5000": ', encoding="utf-8")
            torn, how2 = load_result(res_path)
            ok = ok and torn is None and how2.startswith("unreadable")
            write_json(res_path, {"sets": {}})
            os.chmod(res_path, 0)  # N-a: an OSError on read is also "unreadable"
            try:
                denied, how3 = load_result(res_path)
                ok = ok and (os.geteuid() == 0 or (denied is None and how3.startswith("unreadable")))
            finally:
                os.chmod(res_path, 0o644)
            os.remove(res_path)
            try:
                write_json(res_path, {"x": 1}, _crash_before_rename=True)
            except OSError:
                pass
            tmps = [f for f in d.iterdir() if f.name.startswith(".a_m1_result.json.tmp")]
            return ok and not res_path.exists() and len(tmps) == 1
        finally:
            for f in d.iterdir():
                os.remove(f)
            os.rmdir(d)
    check("W3: fallback keeps the partial result and in-memory V1 (FALSIFIED); atomic result write; torn = absent", w3)

    # CC-287r2 W3r2: EIO on the first FILE fsync of the result write, V1 write failing too -> the fallback writes a
    # readable result, status from records + result is FALSIFIED, and the stored status is FALSIFIED
    def w3r2():
        global _fsync
        d = Path(tempfile.mkdtemp(prefix="a_m1_w3r2_"))
        res_path = d / "a_m1_result.json"
        real, cnt = _fsync, {"file": 0}

        def flaky(fd):
            if not stat_is_dir(fd):
                cnt["file"] += 1
                if cnt["file"] == 1:
                    raise OSError(errno.EIO, "injected EIO on the first result file fsync")
            return real(fd)

        def persist(s, r):
            raise OSError(errno.EIO, "injected V1 write failure")
        res: dict = {}
        try:
            _fsync = flaky
            first_failed = False
            try:
                run_sets(SETS, lambda s, on_v1: (on_v1({"label": V}), {"V1": {"label": V}})[1],
                         L["dc"].Budget(CAP_CPU_S, CAP_WALL_S), persist, lambda: read_v1(d),
                         lambda r: write_json(res_path, r), res)
            except OSError as e:
                first_failed = True
                finish_after_failure(res, e, lambda: read_v1(d), lambda r: write_json(res_path, r))
            loaded, how = load_result(res_path)
            left = [f.name for f in d.iterdir() if f.name != res_path.name]
            return first_failed and how == "read" and status(read_v1(d), loaded) == "FALSIFIED" \
                and loaded["status"] == "FALSIFIED" and not left
        finally:
            _fsync = real
            for f in d.iterdir():
                os.remove(f)
            os.rmdir(d)
    check("W3r2: EIO on the first result fsync; the fallback writes a readable result, FALSIFIED from records + "
          "result and in the stored status; no temp file left", w3r2)

    def w3_json():
        tr: list = []
        got = {}
        r = compute_set(FU, cU, FL, cL, np.array([len(c) for c in comp], float), boot_weights(n, rng, 20),
                        lambda v: got.setdefault("v1", json.loads(json.dumps(v, indent=1))),
                        L["dc"].Budget(CAP_CPU_S, CAP_WALL_S), tr)
        full = {"E5": {"U": e5_counts(ZU), "L": e5_counts(ZL) | {"L": int(sum(len(c) for c in comp))}}, **r}
        back = json.loads(json.dumps(full, indent=1, ensure_ascii=False))
        return back["V1"]["label"] == r["V1"]["label"] and got["v1"]["label"] == r["V1"]["label"] \
            and back["V2A"]["label"] == r["V2A"]["label"] and isinstance(back["V2A"]["rows_G_le_0"], int)
    check("W3: a real compute_set output and its V1 dict round-trip through json.dumps/json.loads", w3_json)

    # CC-287 N2 / HMa (EIO on the directory fsync raises; EINVAL is skipped and logged) and HMc (any v1 record refuses)
    def hma():
        global _fsync
        d = Path(tempfile.mkdtemp(prefix="a_m1_hma_"))
        real = _fsync
        try:
            def bad(code):
                def f(fd):
                    if os.path.isdir(f"/proc/self/fd/{fd}") or stat_is_dir(fd):
                        raise OSError(code, "injected")
                    return real(fd)
                return f
            _fsync = bad(errno.EIO)
            try:
                write_v1_atomic(d, "coco5000", {"label": C}, [])
                eio_raised = False
            except OSError:
                eio_raised = True
            os.remove(d / "v1_coco5000.json")
            log: list = []
            _fsync = bad(errno.EINVAL)
            write_v1_atomic(d, "coco5000", {"label": C}, log)
            return eio_raised and log[-1]["dir_fsync"].startswith("skipped (EINVAL)")
        finally:
            _fsync = real
            for f in d.iterdir():
                os.remove(f)
            os.rmdir(d)
    check("HMa: EIO on the directory fsync raises; EINVAL is skipped and logged", hma)

    def hmc():
        d = Path(tempfile.mkdtemp(prefix="a_m1_hmc_"))
        try:
            write_v1_atomic(d, "uitviic231", {"label": C}, [])
            try:
                refuse_if_records(d)
                return False
            except Fault:
                return True
        finally:
            for f in d.iterdir():
                os.remove(f)
            os.rmdir(d)
    check("HMc: run refuses with only v1_uitviic231.json present", hmc)

    check("N3: the restated Fault and sha_file equal a_dchecks' (checked in load_libs)",
          lambda: _code_sig(Fault.__init__.__code__) == _code_sig(L["dc"].Fault.__init__.__code__)
          and _code_sig(sha_file.__code__) == _code_sig(L["dc"].sha_file.__code__)
          and _code_sig(Fault.__str__.__code__) == _code_sig(L["dc"].Fault.__str__.__code__))

    # registry (mutant 18) and the N-C integer rule
    check("18: the WP-M and WP-D registry is complete", lambda: assert_registry(registry()) is None)
    check("N-C: floor(3s/7 + 1/2) for s = 1..10",
          lambda: n_unnamed(np.arange(1, 11)).tolist() == [0, 1, 1, 2, 2, 3, 3, 3, 4, 4])
    check("synthetic worlds: every registered kind generates; S equals the nameable pairs",
          lambda: all(synth_world(np.random.default_rng(1), c)[3] > 0 for g in registry().values() for c in g))
    return {"checks": checks, "pass": all(checks.values())}


def selftest(out: str, core_only: bool) -> int:
    install_hook()
    assert_pins(list(CODE_PINS))
    load_libs()
    t0, c0 = time.monotonic(), cpu_s()
    r = selftest_core()
    try:
        probe = probe_atomic_write()
    except (Exception, SystemExit) as e:  # noqa: BLE001  (a failed probe is a failed, named check)
        probe = {"ok": False, "error": f"{type(e).__name__}: {str(e)[:200]}"}
    r["checks"]["N-G: registered atomic write on data/results/a_m1/ (dir fsync ok or skipped and logged)"] = probe["ok"]
    rec = {"schema": "vsps.a_m1.selftest.v1", "script_sha256": sha_file(Path(__file__)),
           "plan_sha256": PINS[PLAN], "core_only": core_only, "atomic_write_probe": probe, **r}
    if not core_only:
        cal = calibrate()
        rec["calibration"] = cal
        rec["pass"] = r["pass"] and probe["ok"] and cal["acceptance_A1_V1_le_0.05"]
    else:
        rec["pass"] = r["pass"] and probe["ok"]
    rec["cpu_s"], rec["wall_s"] = cpu_s() - c0, time.monotonic() - t0
    p = Path(out)
    p = p if p.is_absolute() else ROOT / p
    if p.resolve().is_relative_to((ROOT / REC).resolve()):
        raise Fault("selftest never writes under run_record/")
    write_json(p, rec)
    print("\n".join(("PASS " if v else "FAIL ") + k for k, v in rec["checks"].items()))
    if not core_only:
        for k, v in rec["calibration"]["configs"].items():
            print(f"  {k}: V1 {v['V1_violated_rate']:.3f} S<=S {v['share_S_hat_le_S']:.3f} "
                  f"S/S {v['mean_S_hat_over_S']:.3f} V2A {v['V2A_rates']} {v.get('flag', '')}")
    print("selftest ok" if rec["pass"] else "selftest FAILED")
    return 0 if rec["pass"] else 1


# ------------------------------------------------------------------------------------------------ S0 and run
def env_guard() -> None:
    L["dc"].env_guard()


def freeze() -> int:
    old = ROOT / OUT / "freeze/freeze.json"
    if old.exists():  # a refusal reads no input and is not an attempt
        if json.loads(old.read_text(encoding="utf-8")).get("pass"):
            raise Fault("refused: freeze/freeze.json exists with pass = true")
        old.rename(old.with_name(f"freeze.failed_{stamp()}.json"))
    fresh_pycache()
    return s0_attempt("freeze", _freeze)


def _freeze(t0: float, c0: float) -> int:
    pins = assert_pins(list(PINS))
    load_libs()
    env_guard()
    dcf = jload(f"{DC_FREEZE}/freeze.json")
    dc_ok = dcf.get("pass") is True and dcf["id_lists_sha256"]["coco5000_ids.txt"] == PINS[f"{DC_FREEZE}/coco5000_ids.txt"] \
        and dcf["id_lists_sha256"]["uitviic231_ids.txt"] == PINS[f"{DC_FREEZE}/uitviic231_ids.txt"] \
        and dcf["gold_sha256"] == PINS[GOLD]
    st_path = ROOT / OUT / "selftest.json"
    st = json.loads(st_path.read_text(encoding="utf-8")) if st_path.is_file() else {}
    me = sha_file(Path(__file__))
    st_ok = st.get("pass") is True and not st.get("core_only", True) and st.get("script_sha256") == me \
        and (st.get("calibration") or {}).get("acceptance_A1_V1_le_0.05") is True
    ok = dc_ok and st_ok
    rec = {"schema": "vsps.a_m1.freeze.v1", "utc": utc(), "script_sha256": me, "plan_sha256": PINS[PLAN],
           "pins": pins, "dchecks_freeze_ok": dc_ok, "selftest_sha256": sha_file(st_path) if st_path.is_file() else None,
           "selftest_ok": st_ok, "B": B_RUN, "seeds": {s: BASE_SEED + o for s, o in SET_OFF.items()},
           "k_primary": K_PRIMARY, "ks_descriptive": list(KS), "delta_A": DELTA_A, "pass": ok,
           "pycache_prefix": bool(sys.pycache_prefix), "cpu_s": cpu_s() - c0, "wall_s": time.monotonic() - t0}
    print(json.dumps({"freeze": "PASS" if ok else "FAIL", "sha256": out_json(f"{OUT}/freeze/freeze.json", rec)}))
    return 0 if ok else 1


def gate() -> int:
    old = ROOT / OUT / "gate.json"
    if old.exists():  # R10: a passed gate is final; a failed one is kept renamed (plan §6, CC-271r2 N1r2)
        if json.loads(old.read_text(encoding="utf-8")).get("pass"):
            raise Fault("refused: gate.json exists with pass = true")
        old.rename(old.with_name(f"gate.failed_{stamp()}.json"))
    fresh_pycache()
    return s0_attempt("gate", _gate)


def _gate(t0: float, c0: float) -> int:
    assert_pins(list(PINS))
    load_libs()
    env_guard()
    fz = jload(f"{OUT}/freeze/freeze.json")
    me = sha_file(Path(__file__))
    if not fz.get("pass") or fz.get("script_sha256") != me:
        raise Fault("freeze missing, failed, or written by another script version")
    sets = load_sets()
    r4u = jload(R4)["U"]  # only the U.* keys are read (N8)
    rec, ok = gate_core(sets, r4u, frozen_ids())
    st_path = ROOT / OUT / "selftest.json"
    st = json.loads(st_path.read_text(encoding="utf-8"))
    rec["G5"] = st.get("pass") is True and st.get("script_sha256") == me and not st.get("core_only", True) \
        and sha_file(st_path) == fz.get("selftest_sha256")  # N5
    assert_pins(list(PINS))
    rec["G6"] = True
    ok = ok and rec["G5"]
    out = {"schema": "vsps.a_m1.gate.v1", "utc": utc(), "script_sha256": me, "plan_sha256": PINS[PLAN],
           "statistics_computed": "none (no phi_j); G3 first-k union means only", **rec, "pass": ok,
           "cpu_s": cpu_s() - c0, "wall_s": time.monotonic() - t0}
    print(json.dumps({"gate": "PASS" if ok else "FAIL", "sha256": out_json(f"{OUT}/gate.json", out)}))
    return 0 if ok else 1


def run() -> int:
    fresh_pycache()
    assert_pins(list(PINS))
    load_libs()
    env_guard()
    for rel in (SELF, PLAN):
        if L["dc"].git_blob_sha(rel) != sha_file(ROOT / rel):
            raise Fault(f"refused: {rel} differs from its HEAD blob")
    rec_dir = ROOT / REC
    result_path = ROOT / OUT / "a_m1_result.json"
    if result_path.exists():
        raise Fault("refused: a_m1_result.json exists (one attempt)")
    refuse_if_records(rec_dir)
    me = sha_file(Path(__file__))
    fz, gt = jload(f"{OUT}/freeze/freeze.json"), jload(f"{OUT}/gate.json")
    if not (fz["pass"] and gt["pass"] and fz["script_sha256"] == me and gt["script_sha256"] == me):
        raise Fault("refused: S0 freeze/gate missing, failed, or from another script version")
    f_cpu, f_wall, failed = s0_failed(ROOT / OUT)  # W2: failed S0 time is in the cap
    budget = L["dc"].Budget(CAP_CPU_S, CAP_WALL_S, cpu0=fz["cpu_s"] + gt["cpu_s"] + f_cpu,
                            wall0=fz["wall_s"] + gt["wall_s"] + f_wall)
    head = subprocess.run(["git", "-C", ROOT_S, "rev-parse", "HEAD"], capture_output=True, text=True).stdout.strip()
    start = {"head": head, "script_sha256": me, "plan_sha256": PINS[PLAN], "utc_start": utc(),
             "s0_failed_records": failed, "s0_failed_cpu_s": f_cpu, "s0_failed_wall_s": f_wall}
    L["dc"].claim_start(rec_dir / "STARTED.json", start)
    log: list = []
    base = {"schema": "vsps.a_m1.result.v1", "status_note": "POST_HOC descriptive; development data",
            "script_sha256": me, "plan_sha256": PINS[PLAN], "head": head, "freeze_sha256": sha_file(ROOT / OUT /
            "freeze/freeze.json"), "gate_sha256": sha_file(ROOT / OUT / "gate.json"), "s0_failed_records": failed}
    rc = 1
    res: dict = {}

    def write_result(r):
        cpu, wall = budget.used()
        out_json(f"{OUT}/a_m1_result.json", base | r | {"v1_write_log": log, "cpu_s_total": cpu, "wall_s_total": wall})

    try:
        sets = load_sets()
        fr = frozen_ids()
        if any(sets[s]["ids"] != fr[s] for s in SETS):
            raise Fault("loaded ids differ from the D-check freeze lists")
        traces: dict = {}
        run_sets(SETS, lambda s, on_v1: compute_real(sets[s], s, on_v1, budget, traces.setdefault(s, [])),
                 budget, lambda s, r: write_v1_atomic(rec_dir, s, r, log), lambda: read_v1(rec_dir), write_result, res)
        rc = 0 if all(v["state"] == "COMPLETED" for v in res["sets"].values()) else 1
        print(json.dumps({"status": res["status"], "labels": {s: {"V1": (v.get("V1") or {}).get("label"),
                          "V2A": (v.get("V2A") or {}).get("label"), "state": v["state"]} for s, v in res["sets"].items()}}))
    except BaseException as e:  # noqa: BLE001  (W3: keep the partial result, then re-raise)
        if load_result(result_path)[0] is None:
            finish_after_failure(res, e, lambda: read_v1(rec_dir), write_result)
        raise
    finally:
        cpu, wall = budget.used()
        out_json(f"{REC}/timing.json", {"head": head, "rc": rc, "utc_start": start["utc_start"], "utc_end": utc(),
                                        "cpu_s_total": cpu, "wall_s_total": wall, "cap_cpu_s": CAP_CPU_S,
                                        "cap_wall_s": CAP_WALL_S})
    return rc


def show_status() -> int:
    res, how = load_result(ROOT / OUT / "a_m1_result.json")
    print(json.dumps({"status": status(read_v1(ROOT / REC), res), "result_file": how,
                      "persisted": read_v1(ROOT / REC)}))
    return 0


def dryrun() -> int:
    pins = assert_pins(list(PINS))
    load_libs()
    reg = registry()
    print(json.dumps({"pins_asserted": len(pins), "plan_sha256": PINS[PLAN], "sets": list(SETS), "K": K,
                      "arms": ["U (label-free)", "L (R & C)"], "B": B_RUN, "seeds": {s: BASE_SEED + o for s, o in
                      SET_OFF.items()}, "V1": "D_L = (L - S_hat_L)/L; VIOLATED iff 97.5th pct < 0",
                      "V2A": f"k = {K_PRIMARY}, delta {DELTA_A}, 95% interval, D3 scheme",
                      "descriptive": "E1-E5; eps_2, eps_4 (arm U); eps_2..4 (arm L)",
                      "selftest_configs": {k: len(v) for k, v in reg.items()}, "cap": "1 CPU-h / 1 h wall",
                      "run_would_refuse_now": [r for r in (SELF, PLAN) if L["dc"].git_blob_sha(r) != sha_file(ROOT / r)]},
                     indent=1))
    return 0


def main() -> int:
    ap = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    ap.add_argument("mode", choices=("selftest", "dryrun", "freeze", "gate", "run", "status"))
    ap.add_argument("--out", default=f"{OUT}/selftest.json")
    ap.add_argument("--core", action="store_true", help="selftest: core checks only (no calibration worlds)")
    a = ap.parse_args()
    install_hook()
    try:
        return {"selftest": lambda: selftest(a.out, a.core), "dryrun": dryrun, "freeze": freeze, "gate": gate,
                "run": run, "status": show_status}[a.mode]()
    except SystemExit as e:  # this script's Fault and a_dchecks.Fault (both SystemExit subclasses)
        if not hasattr(e, "msg"):
            raise
        print(f"FAULT: {e.msg}", file=sys.stderr)
        return 2


if __name__ == "__main__":
    sys.exit(main())
