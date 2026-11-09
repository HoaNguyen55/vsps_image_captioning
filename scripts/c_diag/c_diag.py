#!/usr/bin/env python3
"""C-DIAG Stage-0 laptop code (Paper C, TALLIP). Prereg manuscript/prereg/2026-11-08_c_diag/C_DIAG_PREREG_DRAFT_v1_2.md
(afbb61fb, registered at aa46a3a) read with CC-299r3 (0fdaa23b) R1-R8. §10.2 item 1. CPU only; laptop only.

    PY=~/.venvs/c_pvr/bin/python        (numpy 2.5.4, CPython 3.12; JDK 21.0.12.1 + VnCoreNLP as c_pvr)
    $PY -X utf8 -I -B scripts/c_diag/c_diag.py lists         --work W
    $PY -X utf8 -I -B scripts/c_diag/c_diag.py label-subset  --work W
    $PY -X utf8 -I -B scripts/c_diag/c_diag.py decomp        --work W
    $PY -X utf8 -I -B scripts/c_diag/c_diag.py gate-sample   --work W --labels W/label_subset.json --labels-sha H
    $PY -X utf8 -I -B scripts/c_diag/c_diag.py floor         --work W --labels ... --labels-sha H
    $PY -X utf8 -I -B scripts/c_diag/c_diag.py vi-pre        --work W
    $PY -X utf8 -I -B scripts/c_diag/c_diag.py counts        --work W --labels ... --labels-sha H
    $PY -X utf8 -I -B scripts/c_diag/c_diag.py manifest      --work W --labels ... --labels-sha H
    $PY -X utf8 -I -B scripts/c_diag/c_diag.py pins          --work W
    $PY -X utf8 -I -B scripts/c_diag/c_diag.py solvency      --bal B --r-d R --sigma-live S --h-b-t1 H --h-b-t1p H --r-b R
                                                     [--b-resume-used] [--b-ended] [--gate-only]
R7: no subcommand here runs before the code is committed with SHA256SUMS and its one-judge code read is GO.
Every subcommand opens files only through `allow` (Appendix B, per subcommand, NB-2): a Python-level open of any other
path is a FAULT, and the §2.3 deny backstop names the pattern. Later subcommands recompute their predecessors in-process
from registered inputs (decompose_vi is deterministic), so no Stage-0 intermediate is read back, except the label
subset (Appendix B row 9), which is read by (path, sha) from --labels / --labels-sha.
W (laptop scratch, never under the repo, N18) receives every output; each output is a new file, and its sha256 line is
appended to W/STAGE0_SUMS for the Stage-0 LOG line. No caption, demonstration or label text is printed.
"""
from __future__ import annotations

import argparse
import fnmatch
import hashlib
import importlib.util
import json
import os
import re
import sys
import time
from collections import Counter
from pathlib import Path

ROOT = Path(__file__).resolve().parents[2]
LABEL = "EXPLORATORY (C-DIAG): spent sets re-used in a dev role, in-sample, no confirmatory claim"  # prereg l.18-19
PREREG = ("manuscript/prereg/2026-11-08_c_diag/C_DIAG_PREREG_DRAFT_v1_2.md",
          "afbb61fb6a231cb36e84bf463983fec0c3d5fcc61f83a33a1d8c856b1c1f81f9")
PYC = "/nonexistent/c_diag_no_pyc"  # sys.pycache_prefix: repo modules are always read from their pinned source
M3 = ".session_backup/machines/M3/root/outputs"
# Appendix B, full sha256 from the v1 / v1.1 Appendix A and the cited code pins; key -> (path, sha256)
B = {
    "lists": ("manuscript/prereg/2026-10-22_c_stage1/lists.json",  # row 1
              "5c479f03e8be544f4cd12b5d997b5dc92b6c622df061760cd02f6ba82f6b4371"),
    "frozen": ("manuscript/prereg/2026-10-22_c_stage2/frozen_config.json",  # row 2
               "2f0c32be7720b672f6e4aae229aba69da8742e0f9e32d34c5137e985ea36aa16"),
    "ex_xm_test2500": (f"{M3}/c_test/ex_xm_test2500.json",  # rows 3-5
                       "242b30a24dfad26cef9a53448c464ab4a460ecb1c98fcafc9ee669cf1c17dd9b"),
    "ex_ov_dev_b": (f"{M3}/c_stage2/ex_ov_dev_b.json", "072b17d14d89aa21110794be27168cf4ef4212a569a4d55d54c5acf1de7e5a41"),
    "ex_xm_dev500": (f"{M3}/c_stage2/ex_xm_dev500.json",
                     "9a79b97dddd573b6092410f33dc2b069213a4407bb029102e05979811f66a17a"),
    "xm_refs": (".session_backup/2026-10-26/c_test/staging/xm_test2500_data.json",  # row 6 (§2.4 W5)
                "4779edd0e57057b50ff5710f4a78f876a4815f0a74348a83357073f179b1eafa"),
    "ov_refs": ("data/datasets/openviic/uit-openviic-annotation-dev.json",  # row 7
                "2a68a3eb4d41926deb524aa8f98c80f112472474906d73d9763c790fb0cac847"),
    "oiv7": ("data/xm3600/oiv7_labels.json", "bac3953a511a9793c22e928a29b68ae05dbf9654502abcbe7b64fd9f6d74c8b2"),  # row 8
    "vi_map": ("data/xm3600/vi_oiv7_map.json", "27f2b1ca3f2bf47d43c8f00e8409472c8d571eb720d47b8107a1c77bd208d16a"),  # 10
    "desc": ("data/datasets/xm3600/oiv7/oidv7-class-descriptions.csv",
             "84a4373a0efb7fd6d93fe19b0e7ceb6c1b855c233d13b9b78a9a33655c9fdce3"),
    "kt_train": ("data/datasets/ktvic/train_data.json",  # row 11
                 "72ee9b57c350fb5f215e1f04701c515a51e5e415240e51a77c8ce00ce6316a0f"),
    "ov_train": ("data/datasets/openviic/uit-openviic-annotation-train.json",
                 "d757520e76b8490df6c7275c2beb8b3ecef0342635a436bea8c3cfd07eb49df0"),
    "xm_img": (".session_backup/2026-10-26/c_test/staging/xm_test2500.sha256",  # row 15 (9ae7c0ac)
               "9ae7c0ac4bb065cae8613c954c49f3c9e75140d300d2fc4b363e7514f54a6c4a"),
}
PREDS = {  # row 12: the eight CC-212 pre-guard comparators (Appendix A); (backbone, set, arm) -> key
    ("qwen25vl_7b", "xm_test2500", "ret"): ("c_test/runs/ct_qwen25vl_7b_xm_test2500-ret-k8-first-T1",
                                            "89713e89ecb893044ace5260d1b1a87842e52f585b16c73892772002654f8538"),
    ("qwen25vl_7b", "xm_test2500", "rand"): ("c_test/runs/ct_qwen25vl_7b_xm_test2500-rand-k8-T1",
                                             "813d2da26f84315421b447c0d4ee7db608d79925ab927e58ed1816a5ed642b66"),
    ("internvl3_8b", "xm_test2500", "ret"): ("c_test/runs/ct_internvl3_8b_xm_test2500-ret-k4-last-T2",
                                             "bc31f08fd822991448a62f1d5a3e81a02f457be2bc5ab46ca6343822c9c2b5b5"),
    ("internvl3_8b", "xm_test2500", "rand"): ("c_test/runs/ct_internvl3_8b_xm_test2500-rand-k4-T2",
                                              "be73fa22a184e0fca9a9ee9320ea39d4efb557c6e205868be1e804d85ccffca5"),
    ("qwen25vl_7b", "ov_dev_b", "ret"): ("c_stage2/runs/c2_qwen25vl_7b_ov_dev_b-ret-k8-first-T1",
                                         "9fa11f7bc552be6310f8ffa9526bcc375352ced54b45ef2cb8085ec87902c03a"),
    ("qwen25vl_7b", "ov_dev_b", "rand"): ("c_stage2/runs/c2_qwen25vl_7b_ov_dev_b-rand-k8-T1",
                                          "53ce8591417cbffe2d6d9368eb5bfd46b123ce695d8cdd6e936faadf7b7118a1"),
    ("internvl3_8b", "ov_dev_b", "ret"): ("c_stage2/runs/c2_internvl3_8b_ov_dev_b-ret-k4-last-T2",
                                          "b05d9163aa9a85356d23d9ff50612750c1bbbf8022fed6caf9cb0476c35002fb"),
    ("internvl3_8b", "ov_dev_b", "rand"): ("c_stage2/runs/c2_internvl3_8b_ov_dev_b-rand-k4-T2",
                                           "991d289bb43b1bcb935e3717aede594147ba533da723501ae473f9af87f43a5b"),
}
for _k, (_p, _h) in PREDS.items():
    B["pred|" + "|".join(_k)] = (f"{M3}/{_p}.preds.json", _h)
CODE = {  # row 17: §10.1 imports, each by sha (scripts/c_diag/SHA256SUMS pins this file and its siblings)
    "scripts/c_pvr/c_pvr.py": "a503644a06ef5723496c47d69f9d91c6ef604b199a205c7357b66f2dc7ba2ec8",
    "scripts/c_pvr/prompts/ver_3way.txt": "bcb9230851622e5d9afa98f0765bf2bffd05b4b4ba37aa8bd0508d300881313d",
    "scripts/c_stage1/decode_icl.py": "fa5a251160d4fd4fb0cd130af33614283863a84e6ed7905f3da81bb6255010db",
    "scripts/lb/decode_hf_vlm.py": "e2de18811e2ffeb61ed72cb2399d41123e9a8f6ccd73a5ec35f778dcbe2f5ac4",
    "scripts/xm3600_oiv7.py": "9a79403f4fc38609282d40082ab7f878133edca8aff9e0dc2462db467b7193f0",
    "rescap/chair.py": "e47d249ac7290070f2387d3fa8b22dac77728265ad276f55aa6520f5cbc591a3",
    "rescap/vi/lexicon.py": "fbc945f2247418275144ac75b893f7c51f8951b9ea42018680d433775dd79eb9",
    "scripts/c_pvr/c_pvr_score.py": "7f3522762aa9a751f9234fcdaa6edae0ff737fa96508a5ee027dc3fda5fb2e65",
    "scripts/c_pvr/c_pvr_cider_vi.py": "3401b46cef094b175919f87ab7dd1948c8841cd95503bd0fe150e9abde0d67a7",
    "scripts/c_pvr_gpu/c_pvr_gpu.py": "9a9c6eb57ee09575a1c69604fa48c506fe8c64d747754b6f8d9c1ced12a1a260",
}
SUBCMD = {  # NB-2: the Appendix B rows each subcommand may open (row 8 only in label-subset)
    "lists": ("lists", "frozen", "ex_xm_test2500", "ex_ov_dev_b", "ex_xm_dev500"),
    "label-subset": ("lists", "oiv7"),
    "decomp": ("lists", "frozen", "ex_xm_test2500", "ex_ov_dev_b", "ex_xm_dev500", "kt_train", "ov_train", "vi_map"),
    "gate-sample": ("lists", "frozen", "ex_xm_dev500", "kt_train", "ov_train", "vi_map", "desc", "labels"),
    "floor": ("lists", "frozen", "ex_xm_test2500", "kt_train", "ov_train", "vi_map", "desc", "labels"),
    "vi-pre": ("lists", *(k for k in B if k.startswith("pred|"))),
    "counts": ("lists", "frozen", "ex_xm_test2500", "ex_ov_dev_b", "ex_xm_dev500", "kt_train", "ov_train", "vi_map",
               "desc", "labels", *(k for k in B if k.startswith("pred|"))),
    "manifest": ("lists", "frozen", "ex_xm_test2500", "ex_ov_dev_b", "ex_xm_dev500", "kt_train", "ov_train", "vi_map",
                 "desc", "labels", "xm_img", *(k for k in B if k.startswith("pred|"))),
    "pins": ("lists", "frozen", *(k for k in B if k.startswith("pred|"))),
    "solvency": (),
}
DENY = ("test_data.json", "uit-openviic-annotation-test.json", "t2pool_*", "nocaps_test*", "image_info_test*",
        "instances_*.json", "captions_*.json")  # §2.3 [W10] exact basenames / prefixes; plus any .vsps_sealed component
SETS = {"xm_dev500": ("xm3600", 500, "ex_xm_dev500"), "xm_test2500": ("xm3600", 2500, "ex_xm_test2500"),
        "ov_dev_b": ("openviic", 925, "ex_ov_dev_b")}  # set -> (shown() source, size, ex file); §2.2
BACKBONES = {"qwen25vl_7b": {"k": 8, "order": "first", "tpl": "T1", "revision": "cc594898137f460bfe9f0759e9844b3ce807cfb5",
                             "hub_id": "Qwen/Qwen2.5-VL-7B-Instruct"},
             "internvl3_8b": {"k": 4, "order": "last", "tpl": "T2", "revision": "259a3b64a14623c0ec91a045cb43f7c5af5fa6af",
                              "hub_id": "OpenGVLab/InternVL3-8B-hf"}}  # §3.1 frozen_config.json, §7
CAP = 32  # c_pvr.CAP (§3.2), here for the stdlib-only ledger; the selftest asserts CAP == c_pvr.CAP
FLOOR = 0.10  # §1.3 [Q8] headroom floor c_b >= 0.10 [proposal, fixed by the GO]
VI_GUARD = 0.95  # §3.3 / §14 item 7 [N6]
RUNGS = (("a", 4, 3), ("b", 8, 3), ("c", 8, 5))  # §4.1 [W2] (rung, ranks 1..r, at most per query and status)
CELL, CELL_MIN = 150, 100  # §4.1
N_LABEL_IDS = 3000  # §2.4 / §4.5: XM-dev500 ∪ XM-test2500
GATE_SALT = "c_diag_gate"  # §4.1 order key
CAP_MAIN_H, CAP_GATE_H = 20.0, 3.0  # §8.3, R2-W1 (b)
M_D, SETUP_VND, W_LINE = 210_000, 30, 50_000  # §8.3
RATE_V = {"qwen25vl_7b": 0.70, "internvl3_8b": 1.30}  # §8.1 planning s per verifier call [est.]
RATE_D = {("qwen25vl_7b", "xm_test2500"): 0.40, ("qwen25vl_7b", "ov_dev_b"): 0.69,
          ("internvl3_8b", "xm_test2500"): 1.30, ("internvl3_8b", "ov_dev_b"): 1.24}  # §8.1 s per image-arm [est.]
ARMS = {"xm_test2500": ("rand", "ret", "filt", "ctl"), "ov_dev_b": ("rand", "ret", "filt")}  # §5.1
LOAD_H, WAIT_H, OVERHEAD_H, PULL_H = 0.12, 0.12, 1.4, 0.5  # §8.2 "4 loads + one round trip" = 0.6; overhead; §8.3 form
ORDER = (("qwen25vl_7b", "xm_test2500"), ("qwen25vl_7b", "ov_dev_b"), ("internvl3_8b", "xm_test2500"),
         ("internvl3_8b", "ov_dev_b"))  # §5.2 execution order
CUT_ORDER = (("internvl3_8b", "ov_dev_b"), ("qwen25vl_7b", "ov_dev_b"), ("internvl3_8b", "xm_test2500"))  # §8.3
C = CP = XO = REG = ZS = None  # decode_icl, c_pvr, xm3600_oiv7, the B-N1 registration, the zs prompt: load()
DATA = ROOT / "data"


def fault(msg: str):
    raise SystemExit(f"FAULT: {msg}")


def utc() -> str:
    return time.strftime("%Y-%m-%dT%H:%M:%SZ", time.gmtime())


def sha(b: bytes) -> str:
    return hashlib.sha256(b).hexdigest()


def path(key: str) -> Path:
    p = Path(os.path.expanduser(B[key][0]))
    return p if p.is_absolute() else ROOT / p


# ---------------------------------------------------------------------------------------------- the allow guard (§2.3)
def deny(p) -> str | None:
    """§2.3 [W10, R2-W7] deny backstop: the pattern a path matches, else None. Lexical only: it never stats or resolves
    the path, so a path under ~/.vsps_sealed is refused without touching it."""
    parts = os.fsdecode(p).split("/")
    if ".vsps_sealed" in parts:
        return ".vsps_sealed"
    return next((pat for pat in DENY if fnmatch.fnmatchcase(parts[-1], pat)), None)


def under(p: str, roots) -> bool:
    return any(p == r or p.startswith(r.rstrip("/") + "/") for r in roots)


class Guard:
    """One audit hook (§2.3 [W10]): every Python-level open is checked. Order: an allow-list entry (path, sha256; the
    sha is re-hashed on each open, cached by size and mtime) -> accepted; an out dir -> accepted; the interpreter's own
    library and the pyc prefix (read only) -> accepted; else the deny backstop names its pattern; else a resolved
    allow-list entry (a symlink) -> accepted; else FAULT. Every refusal is recorded, so a helper that swallows the
    SystemExit (decompose_vi does) still ends the subcommand with FAULT at done(). Ceiling: opens by native code and by
    child processes (java) are not seen; java only reads the VnCoreNLP files CP.rdr hashes first."""

    def __init__(self):
        self.files, self.real, self.outs, self.faults, self.cache = {}, {}, [], [], {}
        self.on = self.busy = False
        self.runtime = sorted({os.path.join(p, "lib") for p in (sys.base_prefix, sys.prefix, sys.exec_prefix)} | {PYC})

    def add(self, p: Path, h: str) -> None:
        a = os.path.abspath(p)
        if a in self.files and self.files[a] != h:
            fault(f"{p} is listed with two shas")
        self.files[a] = h

    def install(self) -> None:
        self.real = {os.path.realpath(p): h for p, h in self.files.items()}  # allow-list paths only, never a denied one
        if not self.on:
            sys.addaudithook(self.hook)
        self.on = True

    def stop(self, msg: str):
        self.faults.append(msg)
        fault(msg)

    def sha_ok(self, p: str, h: str) -> bool:
        st = os.stat(p)
        key = (p, st.st_size, st.st_mtime_ns)
        if key not in self.cache:
            self.busy = True
            try:
                with open(p, "rb") as f:
                    hh = hashlib.sha256()
                    for b in iter(lambda: f.read(1 << 20), b""):
                        hh.update(b)
                self.cache[key] = hh.hexdigest()
            finally:
                self.busy = False
        return self.cache[key] == h

    def why(self, p: str, write: bool) -> str | None:
        """Registered order (§2.3): an allow-list entry first; only paths not on the list reach the deny backstop; then
        (CC-307 N1) an out dir for writes only and the interpreter's library for reads only; then a resolved entry."""
        if p in self.files:
            return self.entry(p, self.files[p], write)
        if (d := deny(p)) is not None:
            return f"deny backstop ({d})"
        if (write and under(p, self.outs)) or (not write and under(p, self.runtime)):
            return None
        q = os.path.realpath(p)
        if q in self.real:
            return self.entry(q, self.real[q], write)
        return "not on the allow-list (Appendix B)"

    def entry(self, q: str, h: str, write: bool) -> str | None:
        if write:
            return "write to an allow-listed input"
        return None if self.sha_ok(q, h) else "sha256 differs from its allow-list entry"

    def hook(self, ev: str, args) -> None:
        if not self.on or self.busy:
            return
        if ev in ("os.listdir", "os.scandir") and args and isinstance(args[0], (str, bytes, os.PathLike)):
            if (d := deny(os.path.abspath(os.fsdecode(args[0])))) is not None:
                self.stop(f"listing refused: deny backstop ({d})")
            return
        if ev != "open" or not isinstance(args[0], (str, bytes, os.PathLike)):
            return
        mode, flags = args[1], args[2] or 0
        write = (any(c in mode for c in "wax+") if isinstance(mode, str) else
                 bool(flags & (os.O_WRONLY | os.O_RDWR | os.O_CREAT | os.O_APPEND | os.O_TRUNC)))
        p = os.path.abspath(os.fsdecode(args[0]))
        if (w := self.why(p, write)) is not None:
            self.stop(f"open refused: {p}: {w}")

    def done(self) -> None:
        if self.faults:
            fault(f"{len(self.faults)} refused open(s); first: {self.faults[0]}")


GUARD = Guard()


def allow(cmd: str, extra: dict | None = None, outs=(), helpers: bool = True) -> Guard:
    """The Appendix B list of one subcommand (NB-2), the code pins (row 17) and `extra` {path: sha} (row 9, pulled
    files), then the hook. helpers: the VnCoreNLP files (row 16, re-hashed by CP.rdr); off for
    c_diag_t1table.py, whose list is exactly its nine inputs (R2-W5 (a)). Out dirs may not lie under the repo (N18)."""
    for o in outs:
        if under(os.path.abspath(o), [str(ROOT)]) or under(os.path.realpath(o), [os.path.realpath(ROOT)]):
            fault(f"out dir {o} lies under the repo (N18: text-bearing files never under the repo)")
        if (d := deny(os.path.abspath(o) + "/x")) is not None:
            fault(f"out dir {o} matches the deny backstop ({d})")  # CC-307 N1
        GUARD.outs.append(os.path.abspath(o))
    for k in SUBCMD.get(cmd, ()):
        if k != "labels":
            GUARD.add(path(k), B[k][1])
    for rel, h in CODE.items():
        GUARD.add(ROOT / rel, h)
    if CP is not None and helpers:
        for rel, h in CP.VNC_PINS.items():  # row 16; CP.rdr re-hashes them on every call
            GUARD.add(CP.VNC_DIR / rel, h)
    for p, h in (extra or {}).items():
        GUARD.add(Path(p), h)
    GUARD.install()
    return GUARD


def load(root: Path = ROOT) -> None:
    """decode_icl, c_pvr and xm3600_oiv7, each behind its sha, imported before any hook; rescap behind CP's pins."""
    global C, CP, XO, REG, ZS
    sys.pycache_prefix = PYC
    for rel in ("scripts/c_stage1/decode_icl.py", "scripts/c_pvr/c_pvr.py", "scripts/xm3600_oiv7.py",
                "scripts/lb/decode_hf_vlm.py"):
        if sha((root / rel).read_bytes()) != CODE[rel]:
            fault(f"{rel} differs from its pin {CODE[rel][:8]}; nothing is imported")
    for d in ("scripts/c_pvr", "scripts/c_stage1"):
        if str(root / d) not in sys.path:
            sys.path.insert(0, str(root / d))
    import c_pvr as cp  # noqa: E402
    import decode_icl as c  # noqa: E402
    spec = importlib.util.spec_from_file_location("xm3600_oiv7", root / "scripts/xm3600_oiv7.py")
    xo = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(xo)
    C, CP, XO = c, cp, xo
    CP.rescap_mods(root)
    REG = C.registration()  # it lazily imports g2b/decode_qwen3vl and reads scripts/evaluate.py: once, pre-hook
    ZS = C.lb.prompt_text(REG, "short")
    if C.sha(ZS) != C.ZS_PROMPT_SHA256:
        fault("the zero-shot `short` prompt differs from 8870589c (DESIGN l.175)")


def dump(obj) -> bytes:
    return (json.dumps(obj, sort_keys=True, ensure_ascii=False, indent=1, allow_nan=False,
                       default=lambda o: o.item()) + "\n").encode()  # numpy scalars -> Python numbers; NaN refused


def write_new(p: Path, obj, sums: Path | None = None) -> str:
    b = dump(obj)
    if p.exists():
        fault(f"{p.name} exists: every C-DIAG output is written once")
    with open(p, "xb") as f:
        f.write(b)
    h = sha(b)
    if sums is not None:
        with open(sums, "a", encoding="utf-8") as f:
            f.write(f"{h}  {p.name}\n")
    return h


def say(obj) -> None:
    """Counts, ids-free aggregates and shas only."""
    print(json.dumps({"label": LABEL, **obj}, sort_keys=True, ensure_ascii=False))


# ---------------------------------------------------------------------------------------------- shared state
class S0:
    """Stage-0 inputs, each read through the hook; derived values are recomputed, never read back (module doc)."""

    def __init__(self, labels: Path | None = None):
        self.labels_path, self._c = labels, {}

    def get(self, k, fn):
        if k not in self._c:
            self._c[k] = fn()
        return self._c[k]

    @property
    def lists(self) -> dict:
        return self.get("lists", lambda: C.load_lists(path("lists"), B["lists"][1]))

    @property
    def frozen(self) -> dict:
        def f():
            cfg = json.loads(path("frozen").read_text("utf-8"))
            for m, want in BACKBONES.items():
                c = cfg["models"][m]
                if (c["k"], c["order"], c["tpl"]) != (want["k"], want["order"], want["tpl"]):
                    fault(f"frozen_config.json: {m} is not k{want['k']} {want['order']} {want['tpl']} (§3.1)")
            return cfg
        return self.get("frozen", f)

    def rows(self, ds: str) -> list[tuple]:
        """[(id, file, image sha256)] in the stored lists.json order (= CC-212's decode order, checked in vi-pre)."""
        def f():
            rows = [tuple(r) for r in self.lists["sets"][ds]]
            if len(rows) != SETS[ds][1] or len({r[0] for r in rows}) != len(rows) or any(len(r) != 3 for r in rows):
                fault(f"{ds}: not {SETS[ds][1]} distinct (id, file, sha256) rows")
            return rows
        return self.get(("rows", ds), f)

    def ex(self, ds: str) -> dict:
        def f():
            ex = C.load_exemplars(path(SETS[ds][2]), path("lists"))
            if ex.get("set") != ds or set(ex["ret"][ds]) != {r[0] for r in self.rows(ds)} or \
                    set(ex["rand"][ds]) != set(ex["ret"][ds]):
                fault(f"{SETS[ds][2]}: not the example lists of {ds}")
            return ex
        return self.get(("ex", ds), f)

    @property
    def caps(self) -> dict:
        return self.get("caps", lambda: C.memory_captions(self.lists, DATA))

    def ranked(self, ds: str, qid: str) -> list[str]:
        """Retrieval ranks 1..8, most similar first (rank r = index + 1)."""
        return [c for c, _cos in self.ex(ds)["ret"][ds][qid][:8]]

    def prompt_ids(self, b: str, ds: str, arm: str, qid: str) -> list[str]:
        spec = {"arm": arm, "k": BACKBONES[b]["k"], "order": BACKBONES[b]["order"], "dataset": ds}
        return C.exemplar_ids(spec, qid, self.ex(ds))

    def shown(self, ds: str, cid: str) -> str:
        return C.shown(self.caps[cid], SETS[ds][0])

    def decomp(self, sets) -> dict:
        """{(src, cid): decomposition} of the shown captions of ranks 1-8 of `sets` (§3.1), one decompose_vi call."""
        def f():
            want = sorted({(SETS[ds][0], c) for ds in sets for q, _f, _h in self.rows(ds) for c in self.ranked(ds, q)})
            texts = [C.shown(self.caps[c], src) for src, c in want]
            return dict(zip(want, CP.decompose_vi(texts, root=ROOT)))
        return self.get(("decomp", tuple(sorted(sets))), f)

    @property
    def status(self) -> dict:
        """{image: {class: present | absent}} from the label subset by status() (§2.4); unknown omitted."""
        def f():
            if self.labels_path is None:
                fault("--labels / --labels-sha are required (Appendix B row 9)")
            XO.MAP = path("vi_map")
            vmap = XO.resolve_map(path("desc"))
            lab = {k: v for k, v in json.loads(self.labels_path.read_text("utf-8")).items() if not k.startswith("_")}
            if bad := set(lab) - set(self.ids3000()):
                fault(f"label subset holds {len(bad)} ids outside XM-dev500 ∪ XM-test2500 (NB-3)")
            return XO.statuses(vmap, lab)
        return self.get("status", f)

    def ids3000(self) -> list[str]:
        ids = sorted({r[0] for ds in ("xm_dev500", "xm_test2500") for r in self.rows(ds)})
        if len(ids) != N_LABEL_IDS:
            fault("XM-dev500 ∪ XM-test2500 is not 3,000 distinct ids")
        return ids


def obj_units(dc: dict, mention) -> set:
    """T1-REP v4 §1 unit: (demonstration, class), a class carried by an obj proposition AND found by the scorer of
    record in the demonstration's text, once per demonstration (c_pvr_score.py l.397 form)."""
    return {c for p in dc["props"] if p["kind"] == "obj" for c in p["classes"]} & mention(dc["text"])


def mention_fn():
    chair, _lex = CP.rescap_mods(ROOT)
    keys = frozenset(k for k in json.loads(path("vi_map").read_text("utf-8")) if not k.startswith("_"))
    cache = {}

    def m(text: str) -> frozenset:  # §3.3 P_obj^VI mentions: objects_in(raw_tone=False) on the 69 keys, once each
        if text not in cache:
            cache[text] = frozenset(chair.objects_in(text, raw_tone=False)) & keys
        return cache[text]
    return m


# ---------------------------------------------------------------------------------------------- §4.1 gate sample
def bare_set() -> set:
    chair, lexicon = CP.rescap_mods(ROOT)
    return {chair.norm_tone(w.lower()) for w in ("một", *lexicon.CLASSIFIERS)}


def syllables(u: str, toks: list) -> list[tuple[int, int]]:
    """[N8] every aligned RDR token split into its syllables ('_' joins them; align() gave them as spaces)."""
    return [(s + m.start(), s + m.end()) for s, e, _w in toks for m in re.finditer(r"\S+", u[s:e])]


def is_bare(u: str, sy: list, p: dict, ok: set, norm) -> bool:
    """§4.1: every syllable inside the proposition span and outside its mention is 'một' or a classifier."""
    for a, b in sy:
        if a < p["start"] or b > p["end"] or any(x <= a and b <= y for x, y in p["mentions"]):
            continue
        if norm(u[a:b].lower()) not in ok:
            return False
    return True


def unit_ok(p: dict, st: dict) -> bool:
    """§4.1 unit: an obj proposition with ONE mapped class whose (query, class) status is present or absent."""
    return p["kind"] == "obj" and len(p["classes"]) == 1 and st.get(p["classes"][0]) in ("present", "absent")


def gate_units(s: S0) -> list[dict]:
    """Every candidate unit (§4.1): a bare obj proposition with ONE mapped class whose (query, class) status is
    present or absent, in a CC-212 `ret` demonstration (rank 1-8) of an XM-dev500 query."""
    ds = "xm_dev500"
    dec = s.decomp([ds])
    chair, _lex = CP.rescap_mods(ROOT)
    norm = chair.norm_tone
    keys = sorted(dec)
    us = {k: dec[k]["text"].replace("_", " ") for k in keys}  # decompose_vi's own `seen` form (offsets unchanged)
    words = CP.rdr([us[k] for k in keys]) if keys else []
    sy = {k: syllables(us[k], CP.align(us[k], w, lambda x: chair.norm_tone(x.lower()))) for k, w in zip(keys, words)}
    ok, out = bare_set(), []
    for q, f, h in s.rows(ds):
        st = s.status.get(q, {})
        for r, cid in enumerate(s.ranked(ds, q), 1):
            key, dc = (SETS[ds][0], cid), dec[(SETS[ds][0], cid)]
            for j, p in enumerate(dc["props"]):
                if not unit_ok(p, st):
                    continue
                if is_bare(us[key], sy[key], p, ok, norm):
                    c = p["classes"][0]
                    out.append({"qid": q, "file": f, "image_sha256": h, "rank": r, "prop_index": j, "class": c,
                                "status": st[c], "text": p["text"],
                                "order": sha(f"{q}|{r}|{j}|{c}|{GATE_SALT}".encode())})
    return sorted(out, key=lambda u: u["order"])


def ladder(units: list[dict]) -> dict:
    """§4.1 [W2]: per rung, walk the order under the per-query cap; supply = what the walk takes with no 150 stop.
    The first rung where both cells reach 150 is used (each cell = its first 150 takes); at rung (c) a cell with
    100-149 takes all it has; fewer than 100 in either cell after rung (c) = FAULT (final, §8.4)."""
    supply, take = {}, {}
    for name, ranks, cap in RUNGS:
        per, got = Counter(), {"present": [], "absent": []}
        for u in units:
            if u["rank"] <= ranks and per[(u["qid"], u["status"])] < cap:
                per[(u["qid"], u["status"])] += 1
                got[u["status"]].append(u)
        supply[name], take[name] = {k: len(v) for k, v in got.items()}, got
        if all(len(v) >= CELL for v in got.values()):
            return {"rung": name, "supply": supply, "units": sorted(got["present"][:CELL] + got["absent"][:CELL],
                                                                    key=lambda u: u["order"])}
    if any(len(v) < CELL_MIN for v in take["c"].values()):
        return {"rung": None, "supply": supply, "units": [],
                "fault": "gate supply: fewer than 100 units in a cell after rung (c); C-DIAG ends before any rental"}
    got = take["c"]
    return {"rung": "c", "supply": supply, "units": sorted(got["present"][:CELL] + got["absent"][:CELL],
                                                         key=lambda u: u["order"])}


def host_units(units: list[dict]) -> list[dict]:
    """The gate unit file the host gets (§4.1, §2.4): ids, rank, proposition index and text, in sha order; no status,
    no class."""
    return [{"u": n, **{k: x[k] for k in ("qid", "file", "image_sha256", "rank", "prop_index", "text")}}
            for n, x in enumerate(units)]


# ---------------------------------------------------------------------------------------------- §1.3 floor, §14.7, counts
def floor(s: S0) -> dict:
    """§1.3 [Q8]: c_b = N_A / (N_A + N_P) over the (demonstration, class) units of ranks 1..k_b of XM-test2500 `ret`."""
    ds = "xm_test2500"
    dec, m, out = s.decomp([ds]), mention_fn(), {}
    for b, cfg in BACKBONES.items():
        n = Counter()
        for q, _f, _h in s.rows(ds):
            st = s.status.get(q, {})
            for cid in s.ranked(ds, q)[:cfg["k"]]:
                dc = dec[(SETS[ds][0], cid)]
                n["decomp_fail"] += "decomp_fail" in dc
                for c in obj_units(dc, m):
                    n[st.get(c, "unknown")] += 1
        na, npr = n["absent"], n["present"]
        c_b = na / (na + npr) if na + npr else None
        out[b] = {"N_A": na, "N_P": npr, "unknown": n["unknown"], "decomp_fail_demos": n["decomp_fail"], "c_b": c_b,
                  "passes_floor": floor_pass(c_b)}
    out["gate_only_branch"] = gate_only_branch(out)
    return out


def floor_pass(c_b) -> bool:
    return c_b is not None and c_b >= FLOOR  # §1.3: c_b >= 0.10 (no units at all = below the floor)


def gate_only_branch(f: dict) -> bool:
    """§1.3 [R2-W1 (a)]: exactly "both backbones have c_b < 0.10" (the floor only)."""
    return all(not f[b]["passes_floor"] for b in BACKBONES)


def vi_share(caps) -> float:
    """§3.3 / §14 item 7 [N6]: share with >= 1 Vietnamese-specific letter after NFC; empty = non-Vietnamese. The
    regex is c_pvr_score.VI_SPECIFIC (tier-1 §5.7(b)), imported read-only (PI-1109d choice)."""
    PS = score_mod()
    import unicodedata
    caps = list(caps)
    return sum(bool(PS.VI_SPECIFIC.search(unicodedata.normalize("NFC", c).lower())) for c in caps) / max(1, len(caps))


def score_mod():
    if "c_pvr_score" not in sys.modules:
        if sha((ROOT / "scripts/c_pvr/c_pvr_score.py").read_bytes()) != CODE["scripts/c_pvr/c_pvr_score.py"]:
            fault("c_pvr_score.py differs from its pin 7f352276")
        spec = importlib.util.spec_from_file_location("c_pvr_score", ROOT / "scripts/c_pvr/c_pvr_score.py")
        m = sys.modules["c_pvr_score"] = importlib.util.module_from_spec(spec)
        spec.loader.exec_module(m)
    return sys.modules["c_pvr_score"]


def preds(b: str, ds: str, arm: str) -> dict:
    d = json.loads(path("pred|" + "|".join((b, ds, arm))).read_text("utf-8"))
    rid = Path(PREDS[(b, ds, arm)][0]).name
    if (d.get("run_id"), d.get("model"), d.get("dataset")) != (rid, b, ds):
        fault(f"{rid}.preds.json: run_id / model / dataset differ from Appendix A")
    return d


def vi_pre(s: S0) -> dict:
    """§14 item 7: VI-script share of the frozen CC-212 ret / rand decodes per (backbone, set, arm); a block whose
    ret or rand < 0.95 is dropped before rental. §5.3 [NB-6, DC2]: the byte-equal share is computable only if each
    file's decode order and batch size are CC-212's (prediction key order = lists order; batch = B-N1)."""
    reg = REG
    out = {}
    for (b, ds, arm) in PREDS:
        d = preds(b, ds, arm)
        items = s.rows(ds)
        order_ok = list(d["predictions"]) == [i for i, _f, _h in items]
        man_ok = d.get("manifest_sha256") == C.sha(json.dumps(items))
        bs_ok = d.get("batch_size") == reg["models"][b]["batch_size"]
        out["|".join((b, ds, arm))] = {"vi_script_share": vi_share(d["predictions"].values()),
                                       "empty_share": sum(not c.strip() for c in d["predictions"].values()) / len(items),
                                       "n": len(d["predictions"]), "byte_equal_computable": order_ok and man_ok and bs_ok,
                                       "order_ok": order_ok, "manifest_sha_ok": man_ok, "batch_ok": bs_ok}
        if set(d["predictions"]) != {i for i, _f, _h in items}:
            fault(f"{b} {ds} {arm}: CC-212 preds do not hold exactly the set's ids")
    for b in BACKBONES:
        for ds in ARMS:
            out[f"{b}|{ds}|block_ok"] = all(out[f"{b}|{ds}|{a}"]["vi_script_share"] >= VI_GUARD for a in ("ret", "rand"))
    return out


def counts(s: S0) -> dict:
    """§8.1: exact obj-proposition counts per backbone and set (ranks 1..k_b); calls = min(obj props, CAP) per image."""
    dec, out = s.decomp(["xm_test2500", "ov_dev_b"]), {}
    for b, cfg in BACKBONES.items():
        for ds in ARMS:
            n = Counter()
            for q, _f, _h in s.rows(ds):
                k = sum(p["kind"] == "obj" for c in s.ranked(ds, q)[:cfg["k"]] for p in dec[(SETS[ds][0], c)]["props"])
                n["obj_props"] += k
                n["calls"] += min(k, CP.CAP)
                n["cap_hit_images"] += k > CP.CAP
                n["decomp_fail_demos"] += sum("decomp_fail" in dec[(SETS[ds][0], c)] for c in s.ranked(ds, q)[:cfg["k"]])
                n["tidy_changed_demos"] += sum(  # rebuild(dc, no drop) != shown text: filt with nothing removed
                    CP.rebuild(dec[(SETS[ds][0], c)], [False] * len(dec[(SETS[ds][0], c)]["props"]), emptied=False)
                    != s.shown(ds, c) for c in s.ranked(ds, q)[:cfg["k"]])
            out[f"{b}|{ds}"] = dict(n)
    return out


# ---------------------------------------------------------------------------------------------- §8.2-8.3 projection, cuts
def stage_hours(b: str, ds: str, calls: int, n: int, rate_v=None, rate_d=None) -> dict:
    rv, rd = (rate_v or RATE_V)[b], (rate_d or RATE_D)[(b, ds)]
    return {"verify": calls * rv / 3600, "decode": len(ARMS[ds]) * n * rd / 3600}


def plan(blocks: dict, gate_units_n: int, cap_h: float, gate_only: bool = False) -> dict:
    """§8.2-§8.3 pre-rental re-projection: blocks {(b, set): {verify, decode} hours} of the kept backbones; billed =
    gate + blocks + loads (+ the one verdict round trip in the main branch) + overhead. While billed > cap, the highest
    not-yet-started block in the cut order goes; never cut: the gate and the first XM-test2500 block in §5.2 order."""
    gate = gate_units_n * 2 * sum(RATE_V.values()) / 3600
    keep = dict(blocks)
    never = next((k for k in ORDER if k in keep and k[1] == "xm_test2500"), None)
    cuts = []

    def billed():
        models = {b for b, _ds in keep}
        loads = (2 + len(models)) * LOAD_H if not gate_only else 2 * LOAD_H
        return gate + sum(v["verify"] + v["decode"] for v in keep.values()) + loads + (0 if gate_only else WAIT_H) \
            + OVERHEAD_H
    while billed() > cap_h:
        nxt = next((k for k in CUT_ORDER if k in keep and k != never), None)
        if nxt is None:
            break
        cuts.append("|".join(nxt))
        del keep[nxt]
    return {"billed_h": billed(), "cap_h": cap_h, "cuts": cuts, "kept": ["|".join(k) for k in ORDER if k in keep],
            "fits": billed() <= cap_h}


def hour_cap(rate: float, gate_only: bool) -> float:
    """§8.3: 20.0 h AND 210,000 VND, whichever binds first; gate-only 3.0 h inside the block (R2-W1 (b))."""
    if not (1_000 <= rate <= 100_000):
        fault(f"offer rate {rate} VND/h is not plausible")
    return min(CAP_GATE_H if gate_only else CAP_MAIN_H, (M_D - SETUP_VND) / rate)


def solvency(a) -> dict:
    """§8.3 [N10, Q7, R2-W8; NB-C4]: PASS_parallel iff Bal >= M + 3 r_D + Σ_live + W_B + O_B + W, every term logged.
    h_B = HB-T1 + HB-T1' billed hours; Σ_live excludes both; M = 210,000, or 3.0 r_D + 30 in the gate-only branch."""
    h_b = a.h_b_t1 + a.h_b_t1p
    w_b = 0 if a.b_ended else max(0.0, 40 - h_b) * a.r_b
    o_b = 0 if (a.b_resume_used or a.b_ended) else 7 * a.r_b + 30
    m = CAP_GATE_H * a.r_d + SETUP_VND if a.gate_only else M_D
    rhs = m + 3 * a.r_d + a.sigma_live + w_b + o_b + W_LINE
    return {"Bal": a.bal, "M": m, "3r_D": 3 * a.r_d, "Sigma_live": a.sigma_live, "h_B": h_b, "W_B": w_b, "O_B": o_b,
            "W": W_LINE, "rhs": rhs, "margin": a.bal - rhs, "PASS_parallel": a.bal >= rhs,
            "branch": "gate-only" if a.gate_only else "main",
            "note": "after B's resume starts (O_B = 0) this may under-reserve by about 5 r_B (CC-299r3 NB-C4)"}


# ---------------------------------------------------------------------------------------------- host manifests
def work_file(s: S0, b: str, ds: str) -> dict:
    """The host's per-(backbone, set) input (§9, Appendix C): items in CC-212 order, ret ids in RANK order (verify),
    rand ids in prompt order, the shown texts and decompositions of those clusters, and the CC-212 prompt sha256 of
    each ret / rand prompt (the host recomputes and must match). No label, status or reference."""
    cfg, dec = BACKBONES[b], s.decomp([ds])
    items = s.rows(ds)
    ret = {q: s.ranked(ds, q)[:cfg["k"]] for q, _f, _h in items}
    rand = {q: s.prompt_ids(b, ds, "rand", q) for q, _f, _h in items}
    cids = sorted({c for v in (*ret.values(), *rand.values()) for c in v})
    shown = {c: s.shown(ds, c) for c in cids}
    zs = ZS
    psha = {}
    for arm in ("ret", "rand"):
        want = preds(b, ds, arm)["prompt_sha256_per_image"]
        got = {q: C.sha(C.prompt(cfg["tpl"], [shown[c] for c in s.prompt_ids(b, ds, arm, q)])) for q, _f, _h in items}
        if got != {q: want.get(q) for q, _f, _h in items}:
            fault(f"{b} {ds} {arm}: the rebuilt prompts differ from CC-212's prompt_sha256_per_image (§5.3)")
        psha[arm] = got
    return {"label": LABEL, "backbone": b, "set": ds, "src": SETS[ds][0], **{k: cfg[k] for k in ("k", "order", "tpl")},
            "zs_sha256": C.sha(zs), "items": [list(r) for r in items], "ret": ret, "rand": rand, "shown": shown,
            "dc": {c: dec[(SETS[ds][0], c)] for c in ret_cids(ret)}, "prompt_sha256": psha}


def ret_cids(ret: dict) -> list[str]:
    return sorted({c for v in ret.values() for c in v})


def push_manifest(d: Path, files: dict, images: list[tuple[str, str, str]]) -> str:
    """d/MANIFEST.sha256 (the host arrival check, Appendix C 3): json files written here, image lines by their
    lists.json sha (the coordinator copies them to img/<set>/<file>); d/push_images.tsv = set, file, sha."""
    d.mkdir(mode=0o700)
    lines = []
    for name, obj in files.items():
        lines.append(f"{write_new(d / name, obj)}  {name}")
    for ds, f, h in images:
        lines.append(f"{h}  img/{ds}/{f}")
    with open(d / "push_images.tsv", "x", encoding="utf-8") as fh:
        fh.write("".join(f"{ds}\t{f}\t{h}\n" for ds, f, h in images))
    body = "".join(x + "\n" for x in sorted(lines, key=lambda x: x[66:]))
    with open(d / "MANIFEST.sha256", "x", encoding="utf-8") as fh:
        fh.write(body)
    return sha(body.encode())


# ---------------------------------------------------------------------------------------------- subcommands
R6 = ("R6: c_diag_t1table.py (§4.5) runs next, unconditionally, in every branch: main, gate-only, no rental, gate "
      "FAIL (the coordinator's OPS line first, R2-W5 (e))")


def cmd_lists(a, s: S0, w: Path, sums: Path) -> None:
    out = {ds: {"n": len(s.rows(ds)), "ex_ok": bool(s.ex(ds))} for ds in SETS}
    out["frozen"] = {m: {k: s.frozen["models"][m][k] for k in ("k", "order", "tpl", "tau")} for m in BACKBONES}
    out["ids_sha256"] = write_new(w / "ids.json", {ds: [list(r) for r in s.rows(ds)] for ds in SETS}, sums)
    say({"step": "lists", **out})


def cmd_label_subset(a, s: S0, w: Path, sums: Path) -> None:
    """§2.4 [NB-3]: oiv7_labels.json read once; XM600 rows discarded, never scored or printed."""
    ids = set(s.ids3000())
    lab = json.loads(path("oiv7").read_text("utf-8"))
    sub = {k: lab[k] for k in sorted(ids) if k in lab}
    del lab
    if not set(sub) <= ids:
        fault("label subset keys are not ⊆ XM-dev500 ∪ XM-test2500 (NB-3)")
    sub["_meta"] = {"label": LABEL, "source_sha256": B["oiv7"][1], "ids": "XM-dev500 ∪ XM-test2500 (lists.json)"}
    say({"step": "label-subset", "keys": len(sub) - 1, "sha256": write_new(w / "label_subset.json", sub, sums)})


def cmd_decomp(a, s: S0, w: Path, sums: Path) -> None:
    dec = s.decomp(list(SETS))
    say({"step": "decomp", "demonstrations": len(dec), "decomp_fail": sum("decomp_fail" in d for d in dec.values()),
         "obj_props": sum(p["kind"] == "obj" for d in dec.values() for p in d["props"]),
         "text_props": sum(p["kind"] == "text" for d in dec.values() for p in d["props"])})


def sample(s: S0) -> dict:
    lad = ladder(gate_units(s))
    if "fault" in lad:
        say({"step": "gate-sample", "supply": lad["supply"]})
        fault(lad["fault"])
    return lad


def cmd_gate_sample(a, s: S0, w: Path, sums: Path) -> None:
    lad = sample(s)
    h = write_new(w / "gate_units.json", host_units(lad["units"]), sums)
    hs = write_new(w / "gate_status.json", [{"u": n, "status": x["status"], "class": x["class"], "qid": x["qid"]}
                                             for n, x in enumerate(lad["units"])], sums)
    say({"step": "gate-sample", "rung": lad["rung"], "supply": lad["supply"], "gate_units_sha256": h,
         "gate_status_sha256": hs, "n_units": len(lad["units"]), "n_queries": len({x["qid"] for x in lad["units"]})})


def cmd_floor(a, s: S0, w: Path, sums: Path) -> None:
    f = floor(s)
    say({"step": "floor", **f, "floor_sha256": write_new(w / "floor.json", {"label": LABEL, **f}, sums)})


def cmd_vi_pre(a, s: S0, w: Path, sums: Path) -> None:
    v = vi_pre(s)
    brief = {k: x if isinstance(x, bool) else {kk: x[kk] for kk in ("vi_script_share", "empty_share",
                                                                   "byte_equal_computable")} for k, x in v.items()}
    say({"step": "vi-pre", **brief, "vi_pre_sha256": write_new(w / "vi_pre.json", {"label": LABEL, **v}, sums)})


def projection(a, s: S0) -> dict:
    """§8.1-8.3 pre-rental: the floor (§1.3), the VI-script precondition (§14.7), the exact counts and the plan."""
    f, v, cn, lad = floor(s), vi_pre(s), counts(s), sample(s)
    kept = {k: stage_hours(*k, cn["|".join(k)]["calls"], len(s.rows(k[1]))) for k in ORDER
            if f[k[0]]["passes_floor"] and v[f"{k[0]}|{k[1]}|block_ok"]}
    gate_only = f["gate_only_branch"]
    if not a.rate:  # CC-307 N5: the pre-rental re-projection uses the live offer rate, never a default
        fault("--rate (the live offer rate, VND/h) is required for counts / manifest (§8.1, NB-C6)")
    rate = a.rate
    pl = plan(kept, len(lad["units"]), hour_cap(rate, gate_only), gate_only)
    rental = gate_only or bool(kept)  # §1.3 / §8.4: an empty main run means no rental, unless gate-only
    return {"counts": cn, "kept": kept, "gate_only": gate_only, "rate": rate, "plan": pl, "rental": rental, "lad": lad}


def cmd_counts(a, s: S0, w: Path, sums: Path) -> None:
    p = projection(a, s)
    rec = {"label": LABEL, "counts": p["counts"], "plan": p["plan"], "rental": p["rental"], "rate_vnd_h": p["rate"]}
    say({"step": "counts", **rec, "blocks_h": {"|".join(k): x for k, x in p["kept"].items()},
         "gate_only_branch": p["gate_only"], "rate_vnd_h": p["rate"],
         "counts_sha256": write_new(w / "counts.json", rec, sums)})


def cmd_manifest(a, s: S0, w: Path, sums: Path) -> None:
    p = projection(a, s)
    if not p["rental"]:
        say({"step": "manifest", "rental": False, "reason": "no block left and not the gate-only branch", "next": R6})
        return
    units = host_units(p["lad"]["units"])
    xm_list = {f: h for h, f in (x.split("  ", 1) for x in path("xm_img").read_text("utf-8").splitlines())}
    if xm_list != {f: h for _i, f, h in s.rows("xm_test2500")}:
        fault("staging/xm_test2500.sha256 differs from the lists.json XM-test2500 image shas (§14 item 5)")
    branch = "gate_only" if p["gate_only"] else "main"
    files = {"gate_units.json": units}
    images = [("xm_dev500", f, h) for f, h in sorted({(u["file"], u["image_sha256"]) for u in units})]
    if not p["gate_only"]:  # R2-W1 (c): the gate-only push lists no XM-test2500 or OV-dev-B file
        for k in [tuple(x.split("|")) for x in p["plan"]["kept"]]:
            files[f"work.{k[0]}.{k[1]}.json"] = work_file(s, *k)
        for ds in sorted({x.split("|")[1] for x in p["plan"]["kept"]}):
            images += [(ds, f, h) for _i, f, h in s.rows(ds)]
    tman = push_manifest(w / f"push_{branch}", files, sorted(set(images)))
    with open(sums, "a", encoding="utf-8") as fh:
        fh.write(f"{tman}  push_{branch}/MANIFEST.sha256\n")
    say({"step": "manifest", "branch": branch, "tman": tman, "files": sorted(files), "images": len(set(images)),
         "plan": p["plan"], "next": R6})


def cmd_pins(a, s: S0, w: Path, sums: Path) -> None:
    """§7: the CC-212 records (B-N1 file pins, the preds provenance), checked and frozen in W."""
    out = {}
    for b, want in BACKBONES.items():
        m = REG["models"][b]
        if (m["hub_id"], m["revision"]) != (want["hub_id"], want["revision"]):
            fault(f"B-N1 {b} is not {want['hub_id']} @ {want['revision'][:8]} (§7)")
        prov = [preds(b, ds, arm) for ds in ARMS for arm in ("ret", "rand")]
        keys = ("hub_id", "revision", "batch_size", "dtype", "attn_implementation")
        for x in prov:
            if tuple(x[k] for k in keys) != tuple(m[k] for k in keys):
                fault(f"{x['run_id']}: model block differs from B-N1 (§7: a mismatch with a CC-212 record)")
        out[b] = {"files": m["files"], "venv_freeze_sha256": sorted({x.get("venv_freeze_sha256") or "missing"
                                                                      for x in prov}),
                  "packages": sorted({json.dumps(x.get("packages"), sort_keys=True) for x in prov}),
                  "batch_size": m["batch_size"]}
    out["venv"] = REG["venv"]
    out["label"] = LABEL
    say({"step": "pins", "pins_sha256": write_new(w / "pins.json", out, sums),
         "freeze": {b: out[b]["venv_freeze_sha256"] for b in BACKBONES}, "next": R6})


HANDLERS = {"lists": cmd_lists, "label-subset": cmd_label_subset, "decomp": cmd_decomp,
            "gate-sample": cmd_gate_sample, "floor": cmd_floor, "vi-pre": cmd_vi_pre, "counts": cmd_counts,
            "manifest": cmd_manifest, "pins": cmd_pins}


def run(a) -> None:
    if a.cmd == "solvency":
        say({"step": "solvency", "utc": utc(), **solvency(a)})
        return
    w = Path(a.work)
    extra = {}
    if a.labels:
        if not re.fullmatch(r"[0-9a-f]{64}", a.labels_sha or ""):
            fault("--labels-sha must be the full 64-hex Stage-0 sha of the label subset")
        extra[a.labels] = a.labels_sha
    allow(a.cmd, extra, [w])
    HANDLERS[a.cmd](a, S0(Path(a.labels) if a.labels else None), w, w / "STAGE0_SUMS")
    GUARD.done()


def main() -> None:
    ap = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    sub = ap.add_subparsers(dest="cmd", required=True)
    for c in SUBCMD:
        p = sub.add_parser(c)
        if c != "solvency":
            p.add_argument("--work", required=True)
            p.add_argument("--labels")
            p.add_argument("--labels-sha")
            p.add_argument("--rate", type=float, help="live offer rate VND/h (required by counts / manifest)")
        else:
            for k in ("bal", "r_d", "sigma_live", "h_b_t1", "h_b_t1p", "r_b"):
                p.add_argument("--" + k.replace("_", "-"), type=float, required=True)
            for k in ("b-resume-used", "b-ended", "gate-only"):
                p.add_argument("--" + k, action="store_true")
    a = ap.parse_args()
    if a.cmd != "solvency":
        load()
    run(a)


if __name__ == "__main__":
    main()
