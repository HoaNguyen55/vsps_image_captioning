#!/usr/bin/env python3
"""C-PVR-T1 GPU side (Paper C, plan step S10; DRAFT, not judge-read). One rented RTX 3090 / 3090 Ti (host amendment
v3 5d6f5ca), money rule T1-REP v4 §9 (4124ef3), tier-1 STOPs prereg v1.2 §10.1 as amended.

    $PY -I -B scripts/c_pvr_gpu/c_pvr_gpu.py selftest                laptop CPU: mocks the GPU parts, sockets off
    $PY -I -B scripts/c_pvr_gpu/c_pvr_gpu.py hostcheck --mblip SNAP --kept DIR --out O     GPU-host selftest
    $PY -I -B scripts/c_pvr_gpu/c_pvr_gpu.py decode --set S --arm A --manifest M --kept DIR --out O
                                             [--speed N --timing T] [--a1-decomp F] [--cap CAP.json]
    $PY -I -B scripts/c_pvr_gpu/c_pvr_gpu.py cap --timing T --sizes Z --s-vnd S --r-host R --p1-epoch E
                                             --pqc2-solvent yes|no --out CAP.json              the P1 line rule
                                             (R = the rental-line VND/h as written, e.g. 10053.38; rounded UP)
    $PY -I -B scripts/c_pvr_gpu/c_pvr_gpu.py left --cap CAP.json      seconds left before the cap / money stop
    $PY -I -B scripts/c_pvr_gpu/c_pvr_gpu.py wipe --dir D --log L     logged tmpfs deletion (host v3 §4.4)

c_pvr.py is imported unchanged behind its sha pin (Q-SPLIT (i)-(ii)); no shared constant has a second value here.
The manifest (per set: query ids, image file names and shas, ranked kept demo ids, demo decompositions; built on the
laptop, builder out of scope) and the kept-id files live only in /dev/shm/c_pvr_hc. Logs and prompt dumps hold ids
only (meta item 17); outputs hold ids, masks, counts and the query caption, never demonstration text or a prompt.
This code never rents, tops up or deletes a machine. Label: TIER 1 / DEV-EXPLORE.
"""
from __future__ import annotations

import argparse
import hashlib
import json
import math
import os
import re
import sys
import time
from fractions import Fraction
from pathlib import Path

ROOT = Path(__file__).resolve().parents[2]
CODE = {"scripts/c_pvr/c_pvr.py": "623a0540916606f36a2c75e5b0103d7b7eb067353213734ac1bc77e19e35afdf",
        "scripts/c_pvr/c_pvr_run.py": "bdc543f44e3f3601a9bb418b628872077b37b1ce4ba35dd227b56caf8e385272"}
CP = CR = None  # c_pvr, c_pvr_run (stdlib-only at import): bound by load() after their shas match

PENDING = "PENDING"
# S9 = PINS_A_ADDENDUM_S9_DRAFT_v2.md c3abb246 (cbb24e6; CC-269r2 GO 89; A5 = XGLM per PI-1106e). Its §8.4-8.5 put
# the new constants (NES_TAU, A4_DEGEN, A9_POOL, SEEDS["A5"], LMCAP_N, MAX_NEW["rederive"]) and the 3 prompt files in
# scripts/c_pvr (c_pvr.py PROMPTS), so the c_pvr.py pin above changes then; until that edit and the helper passes
# exist, the four arms stay PENDING here and get no second value.
PINS = {
    "A4": PENDING,  # c_pvr.py NES_TAU, A4_DEGEN + the M-CLIP scoring pass (S9 §1, §8.5)
    "A9": PENDING,  # c_pvr.py A9_POOL + the same M-CLIP pass (S9 §3)
    "A5": PENDING,  # c_pvr.py LMCAP_N, SEEDS["A5"], lmcap_block_vi.txt + the XGLM pass (S9 §2)
    "A10": PENDING,  # c_pvr.py MAX_NEW["rederive"], rederive_vi.txt, rederive_cap_vi.txt + the two-call pass (S9 §4)
    "EN": PENDING,  # LLaVA code commit, CLIP tower sha, LLaVA env (PINS-A §12 Q-LLAVA)
    "DEMOCAP_d_tc": PENDING,  # CC-269r2 W5: D-TC demonstration-caption rule, to be ruled at the S10 read
    "DEMOCAP_d_en": PENDING,  # CC-269r2 W5: D-EN rule, same
}
# S9 v2 §1-§2 helper files: (kind, value); kind "lfs" = sha256, "blob" = git-blob SHA-1 (c_pvr.blob_hashes)
HELPERS = {
    "mclip": ("laion/CLIP-ViT-H-14-frozen-xlm-roberta-large-laion5B-s13B-b90k",
              "f9ab955287d06ac45c7654f26fecd29301c70a1f", {
                  "open_clip_pytorch_model.bin": ("lfs", "ee81ce53c8591d48ee5e7b390b2f10d502c721df5920c3096c6bdb54d1459881"),
                  "preprocessor_config.json": ("blob", "c13c679c06519325749d1eef242ff98e2a5d2165"),
                  "tokenizer.json": ("blob", "463f3414782c1c9405828c9b31bfa36dda1f45c5")}),
    "xlmr": ("xlm-roberta-large", "c23d21b0620b635a76227c604d44e43a9f0ee389", {  # = FacebookAI/xlm-roberta-large;
        # legacy id so open_clip finds it BY NAME offline (S9 §8.2; C-T1 registry hub_id); config/tokenizer only
        "config.json": ("blob", "8e5fb14e1352fd8fc678a7b293b63cfb5cf091f6"),
        "sentencepiece.bpe.model": ("blob", "db9af13bf09fd3028ca32be90d3fb66d5e470399"),
        "tokenizer.json": ("blob", "463f3414782c1c9405828c9b31bfa36dda1f45c5"),
        "tokenizer_config.json": ("blob", "34ddbd64a4cd3f2d9d8a9120d3662d0bf91baead")}),
    "xglm": ("facebook/xglm-2.9B", "33c659ae27de09c0a54123d3902dac48cbb8592a", {
        "pytorch_model.bin": ("lfs", "9aa29d6635e7936bdd020bd8dab855ba8e7d3b507a1af78a98a7039648f66f23"),
        "sentencepiece.bpe.model": ("lfs", "c49dc7e82c10227af764e518924cf2f9d50c00462750d184fa74697bba65eef8"),
        "config.json": ("blob", "5259f0909bbb98005e355a94f0a9ad9902dc1810"),
        "generation_config.json": ("blob", "b73e8f8fc85a983669324aeb7b0f9fc92e18f9f8"),
        "special_tokens_map.json": ("blob", "169adeb038b8bde6ecf79666dbfa49fcbaf9a087"),
        "tokenizer.json": ("blob", "98f7774e39cd7ce59acfe522852863101ccad1d8"),
        "tokenizer_config.json": ("blob", "9a478583cf78963e92ee738bf7dababc1b376cb2")}),
}
S9_PROMPTS = {"lmcap_block_vi.txt": "a1fb17d9b73e85667a84c3ff0daee6ff3a3a5b79cc0963af9eb0bd69eb480213",
              "rederive_vi.txt": "478c5fdde54423222384897653fb080c55b7c0a04c1b30cc850ca4becd87c312",
              "rederive_cap_vi.txt": "93aa55e3bbaab95f4a5374f6df623d7d58d6b91aab184ecd2a69270b78c8b509"}  # -> c_pvr.py
DEMO_SRC = {"ktvic_train": "train_data.json", "openviic_train": "uit-openviic-annotation-train.json"}  # in <hc>/src
# OPS-1106c-datastores (LOG l.1655), CC-268 GO 93: decode against these kept-id files only, re-hashed before use
KEPT = {
    "d_vi": ("d_vi_kept_ids.txt", 9098, "753cf695445d9eabfee476089143ea2b72efdbe73514a721ba31d879737d02ba"),
    "d_tc": ("d_tc_kept_ids.txt", 20842, "a5f324653b4234c0722006744a364b576cb22f083d9b85444f118088e34b3d3b"),
    "d_en": ("d_en_kept_ids.txt", 80040, "619839a8c8a770380dca2029da5c7dc60f61f4749528b2c50e2baa37ec58003e"),
}
BARRED = re.compile(r"\.vsps_sealed|t2pool_", re.I)  # sealed custody; tier-2 confirm pools are never read here

VI_ARMS = ("A0", "A1", "A2", "A3", "A4", "A5", "A6", "A7", "A8", "A9", "A10", "A11", "A12", "PVR-drop", "PVR-keep")
EN_ARMS = ("S1", "S2", "S3", "S4", "S5")  # prereg §5.1: PVR, A8, A1, A0, A6 on KT-C (D-EN), LLaVA
SETS = {  # [proposal] set -> (datastore, prompt language, arms); prereg §4.1 and host v3 §5
    "xm3600_vi": ("d_vi", "vi", VI_ARMS),
    "ktvic_explore": ("d_vi", "vi", tuple(a for a in VI_ARMS if a != "A12")),  # A12 needs OI labels: XM3600 only
    "openviic_explore": ("d_vi", "vi", tuple(a for a in VI_ARMS if a != "A12")),
    "vitextvqa_dev": ("d_vi", "vi", tuple(a for a in VI_ARMS if a != "A12")),
    "t_a": ("d_tc", "en", tuple(a for a in VI_ARMS if a != "A12")),
    "kt_c": ("d_en", "en", EN_ARMS),
}
SPEED_SET = {"vi": "xm3600_vi", "en": "kt_c"}  # prereg §10.1: 200 XM3600-vi x every VI arm, 200 KT-C x S1-S5
SPEED_N = 200
NEEDS = {"A4": "A4", "A9": "A9", "A5": "A5", "A10": "A10", **{s: "EN" for s in EN_ARMS}}
NEVER_CUT = {"A4", "A9"}  # T1-REP R-1: a PENDING pin here may not become a silent cut

# money (host v3 §2-§3; T1-REP §9): integer VND and integer seconds only
M_BASE, M_PQC2 = 350_000, 465_000
CUT_ORDER = ("A10", "A5", "A3", "A2", "A11")  # T1-REP §9 rule 2 (R-1)
T_DOWN_H = 1  # host v3 §3: T_down = 1.0 h x r_host
CAP_STOP_RC = 4
A8_WAIT_SEC = 1800  # [proposal, S11] CC-270 B2: longest phase-2 wait for the laptop's A1 decomposition; added to P1

LOG_KEYS = {"utc", "set", "arm", "id", "demo_ids", "tpl", "n_demos", "emptied", "calls", "cap_hits", "parse_fail",
            "yes", "maybe", "no", "finish", "sec", "kind", "event"}
OUT_KEYS = LOG_KEYS | {"caption", "masks"}
SPEED_LOG = {"utc", "set", "arm", "id", "calls"}  # calls follows from the inputs (props, CAP), not from an answer  # caption = the query's own model output, the only free text
ID_RX = re.compile(r"[A-Za-z0-9_.:+-]{1,80}")


def fault(msg: str):
    raise SystemExit(f"FAULT: {msg}")


def utc() -> str:
    return time.strftime("%Y-%m-%dT%H:%M:%SZ", time.gmtime())


def guard(p) -> Path:
    if BARRED.search(str(p)):
        raise SystemExit(f"REFUSED: {p} (sealed custody or tier-2 pool)")
    return Path(p)


def load(root: Path = ROOT) -> None:
    global CP, CR
    for rel, sha in CODE.items():
        if hashlib.sha256((root / rel).read_bytes()).hexdigest() != sha:
            fault(f"{rel} differs from its pin {sha[:8]} (Q-SPLIT (ii)); nothing is imported")
    sys.path.insert(0, str(root / "scripts/c_pvr"))
    import c_pvr as CP  # noqa: E402  LABEL, prompts, render, pick, verify, pvr_masks, a7/a12 masks, generate ...
    import c_pvr_run as CR  # noqa: E402  LISTS_IN (source json pins, W3), KT_ID, OV_KEY (id forms, W2)


def need(key: str) -> None:
    if PINS[key] == PENDING:
        fault(f"{key} pin is {PENDING} (S9 addendum / Q-LLAVA); nothing is decoded")


# ---------------------------------------------------------------------------------------------- checks (shared)
def weights_only_guard(torch) -> None:
    """Q-LLAVA: every torch.load runs with weights_only=True; an explicit False is a FAULT. Installed before
    transformers / open_clip import, on both names they may call."""
    orig = getattr(torch.load, "_c_pvr_orig", torch.load)

    def load_wo(*a, **k):
        if k.get("weights_only", True) is not True:
            fault("torch.load called with weights_only != True")
        k["weights_only"] = True
        return orig(*a, **k)

    load_wo._c_pvr_orig = orig
    torch.load = load_wo
    torch.serialization.load = load_wo


def check_weights_only(torch, tmp: Path) -> None:
    weights_only_guard(torch)
    p = tmp / "t.pt"
    torch.save({"w": torch.zeros(2)}, p)
    assert torch.load(p)["w"].shape == (2,)
    try:
        torch.load(p, weights_only=False)
    except SystemExit as e:
        assert "weights_only" in str(e)
    else:
        fault("weights_only=False was not refused")


def check_genconfig(GenerationConfig) -> dict:
    """Every pinned key survives GenerationConfig(**gc).to_dict() unchanged; the None keys stay None."""
    out = {}
    for kind in CP.MAX_NEW:
        gc = CP.gen_config(kind, 2, 3)
        d = GenerationConfig(**gc).to_dict()
        if bad := sorted(k for k, v in gc.items() if k not in d or d[k] != v):
            fault(f"GenerationConfig({kind}) drops or changes {bad}")
        out[kind] = sorted(k for k, v in gc.items() if v is None)
    if out["caption"] != sorted(k for k, v in CP.GEN_BASE.items() if v is None):
        fault("None keys differ from GEN_BASE")
    return out


def echo_probe(model) -> dict:
    """Wrap model.generate to record whether the raw output starts with the prompt ids (the strip branch)."""
    rec, orig = {}, model.generate

    def spy(**k):
        out = orig(**k)
        ids, o = k["input_ids"][0].tolist(), out[0].tolist()
        rec["starts_with_prompt_ids"] = o[:len(ids)] == ids
        return out

    model.generate = spy
    return rec


def check_echo(gen, probe: dict, P: dict, image) -> dict:
    """prereg PINS-A §12 Ruling 2(b): the decoded text never holds the prompt, for both kinds."""
    out = {}
    for kind, prompt in (("caption", CP.render(P, [], "vi")), ("verify", CP.ver_prompt(P, "một con chó"))):
        text, finish = gen(image, prompt, kind)
        body = CP.clean(prompt)
        if body in CP.clean(text) or CP.clean(text).startswith(body[:24]):
            fault(f"prompt echo in the {kind} output")
        out[kind] = {"strip_branch": probe.get("starts_with_prompt_ids"), "finish": finish, "chars": len(text)}
    return out


def rec_ok(rec: dict, keys: set = LOG_KEYS) -> dict:
    """Ids only (meta item 17): whitelisted keys; every string except 'caption' is a single id token."""
    for k, v in rec.items():
        if k not in keys:
            fault(f"log key {k!r} is not on the ids-only list")
        if k == "caption":
            continue
        for x in v if isinstance(v, list) else [v]:
            if isinstance(x, str) and not ID_RX.fullmatch(x):
                fault(f"log value under {k!r} is not an id")
    return rec


def write_rec(f, rec: dict, keys: set = LOG_KEYS) -> None:
    f.write(json.dumps(rec_ok(rec, keys), ensure_ascii=False, sort_keys=True) + "\n")
    f.flush()


def kept_ids(kdir: Path, name: str) -> frozenset:
    """OPS-1106c-datastores: re-hash against the pin before use (CC-268 W2); sorted, unique, one id per line."""
    fname, n, sha = KEPT[name]
    b = guard(kdir / fname).read_bytes()
    if hashlib.sha256(b).hexdigest() != sha:
        fault(f"{fname} differs from its pin {sha[:8]}")
    ids = b.decode("utf-8").split("\n")
    if ids.pop() != "" or len(ids) != n or ids != sorted(set(ids)):
        fault(f"{fname}: not {n} sorted unique LF-terminated ids")
    return frozenset(ids)


def norm_ids(a, universe: frozenset) -> list[str]:
    """CC-261 N6 / K3: ids from npz (int64) or json (int) become str, then must all lie in the universe."""
    ids = [str(x) for x in (a.tolist() if hasattr(a, "tolist") else a)]
    if bad := [i for i in ids if i not in universe]:
        fault(f"{len(bad)} ids outside the kept set after str-normalisation (first {bad[0]!r})")
    return ids


def helper_check(snap: Path, name: str) -> None:
    """S9 §8.1: every pinned helper file by LFS sha256 or git-blob SHA-1 before any load; a mismatch is a FAULT."""
    for f, (kind, want) in HELPERS[name][2].items():
        _, s256, s1 = CP.blob_hashes(guard(snap / f))
        if (s256 if kind == "lfs" else s1) != want:
            fault(f"{name} {f} differs from its S9 pin {want[:8]}; nothing is loaded")


def demo_captions(ids, src: Path) -> dict:
    """N8 / Q-DEMOCAP (CC-269r2 Ruling 4): a D-VI id's demonstration text = its first caption in source json order
    (KTVIC: first annotations entry with str(image_id) == id; OpenViIC: captions[0]), then rendering rule 4 (clean).
    Source by id form (W2): bare unpadded integer -> KTVIC, 11-digit file name -> OpenViIC. Source jsons sha-checked
    against the lists pins (W3). Unlike stage-1 there is no cluster/shown() step: D-VI is unclustered (W1)."""
    raw = {}
    for k, fname in DEMO_SRC.items():
        b = guard(src / fname).read_bytes()
        if hashlib.sha256(b).hexdigest() != CR.LISTS_IN[k][1]:
            fault(f"{fname} differs from its lists pin {CR.LISTS_IN[k][1][:8]}")
        raw[k] = json.loads(b)
    first = {}
    for a in raw["ktvic_train"]["annotations"]:
        first.setdefault(str(a["image_id"]), a["caption"])
    ov = raw["openviic_train"]
    out = {}
    for i in ids:
        kt, oo = bool(CR.KT_ID.fullmatch(i)), bool(CR.OV_KEY.fullmatch(i))
        if kt == oo or (i in first and i in ov):
            fault(f"id {i!r}: not exactly one source form")
        cap = first.get(i) if kt else (ov.get(i) or {}).get("captions", [None])[0]
        if not cap:
            fault(f"id {i!r} has no caption in its source")
        out[i] = CP.clean(cap)
    return out


# ---------------------------------------------------------------------------------------------- money (T1-REP §9)
def h_m(m: int, s: int, r: int) -> int:
    """H_M = floor((M - S - T_down) / r_host), T_down = 1 h x r_host."""
    return (m - s - T_DOWN_H * r) // r


def ceil125(sec: int) -> int:
    """ceil(1.25 x sec / 3600) in integers."""
    return -(-5 * sec // 14400)


def r_host_up(line: str) -> int:
    """CC-270 N1: r_host = the rental-line VND/h rounded UP (10,053.38 -> 10,054); rounding down overstates H_M."""
    r = math.ceil(Fraction(line))
    if r <= 0:
        fault(f"r_host {line!r} is not a positive rate")
    return r


def cap_plan(arm_sec: dict, s: int, r: int, pqc2_solvent: bool, fixed_sec: int = 0) -> dict:
    """T1-REP §9 rules 1-4. arm_sec: projected decode seconds per arm (all sets). Cuts kept under PQ-C2.
    fixed_sec: billed seconds that are no arm's decode (CC-270 B2: the A8 wait bound); in P1, never cut."""
    left, cuts = dict(arm_sec), []

    def fits(m):
        return ceil125(sum(left.values()) + fixed_sec) <= h_m(m, s, r)

    for a in CUT_ORDER:
        if fits(M_BASE):
            break
        if a in left:
            cuts.append(a)
            del left[a]
    m = M_BASE
    if not fits(m):
        if not pqc2_solvent:
            return {"decision": "PI", "why": "all cuts made, does not fit 350k; PQ-C2 solvency not met", "cuts": cuts}
        m = M_PQC2
        if not fits(m):
            return {"decision": "PI", "why": "does not fit 465k after every cut", "cuts": cuts}
    cap_h = ceil125(sum(left.values()) + fixed_sec)
    total = s + cap_h * r + T_DOWN_H * r
    assert total <= m, (total, m)
    return {"decision": "RUN", "m": m, "cap_h": cap_h, "h_m": h_m(m, s, r), "cuts": cuts, "arms": sorted(left),
            "p1_sec": sum(arm_sec.values()), "p1_cut_sec": sum(left.values()), "fixed_sec": fixed_sec,
            "block_max_vnd": total}


A8_PROXY = {"A8": ("PVR-drop", "A1"), "S2": ("S1", "S3")}  # [proposal] A8 is not timed (it needs A1 decomposed on
# the laptop): its rate is taken as rate(PVR) - rate(A1), the verifier share of PVR over 4 demos (an over-estimate)


def project(timing: list[dict], sizes: dict) -> dict:
    """Per-arm projected seconds: speed-set seconds per image x tier-1 images on every set the arm runs on."""
    rate = {t["arm"]: Fraction(t["sec"], t["n"]) for t in timing if t["set"] == SPEED_SET[t["lang"]]}
    for a, (p, b) in A8_PROXY.items():
        if p in rate and b in rate:
            rate[a] = max(Fraction(0), rate[p] - rate[b])
    if miss := sorted({a for _, _, arms in SETS.values() for a in arms} - set(rate)):  # CC-270 N3
        fault(f"speed test incomplete (no rate for {miss}): STOP, PI")
    out = {}
    for name, (_, _, arms) in SETS.items():
        for a in arms:
            out[a] = out.get(a, 0) + math.ceil(rate[a] * sizes[name])
    return out


def left_sec(cap: dict, now: float) -> int:
    """Wall clock from the P1 stamp (idle billed time counts): the cap hours, which are <= the money stop."""
    return int(cap["p1_epoch"] + cap["cap_h"] * 3600 - now)


# ---------------------------------------------------------------------------------------------- decode
def demos_for(arm: str, q: dict, M: dict, kept: frozenset, ask, prior: dict) -> tuple[list[str], list[str], dict]:
    """Arm -> (demo ids, demo texts, stats). Reuses c_pvr.py arm code only."""
    if arm in NEEDS:
        need(NEEDS[arm])
    ranked = norm_ids(q["ranked"], kept)  # CC-261 N6: json/npz ids may be int; matched as str only
    ids = CP.pick(arm if arm in ("A0", "A2", "A3") else "A1", q["id"], ranked, sorted(kept))
    dcs = [M["demos"][i] for i in ids]
    st = {}
    if arm in ("A0", "A1", "A2", "A3"):
        return ids, [d["text"] for d in dcs], st
    if arm == "A6":
        masks = [[False] * len(dc["props"]) for dc in dcs]
    elif arm in ("PVR-drop", "PVR-keep"):
        masks, st = CP.pvr_masks(dcs, ask, arm.split("-")[1])
        st["masks"] = masks
    elif arm == "A7":
        masks = CP.a7_masks(q["id"], prior[q["id"]])  # Q-A7 (b): count-matched to PVR-drop at tier 1
    elif arm == "A12":
        absent = set(q["absent"])
        masks = CP.a12_masks(dcs, lambda c: "absent" if c in absent else "other")
    elif arm == "A11":
        texts = [t for t in (CP.a11_text(dc) for dc in dcs) if t is not None]
        return ids, texts, {"emptied": len(dcs) - len(texts)}
    else:
        fault(f"arm {arm} has no demonstration rule here")
    texts, emptied = CP.demos_after(dcs, masks)
    return ids, texts, {**st, "emptied": emptied}


def speed_ids(ids: list[str], n: int) -> list[str]:
    """[proposal] the speed subset: first n by sha256(id + 'c_pvr_speed'), the T_A ordering pattern (prereg §4.1)."""
    return sorted(ids, key=lambda i: hashlib.sha256((i + "c_pvr_speed").encode()).hexdigest())[:n]


def a1_decomp(f: Path, ids: set, clock, sleep) -> tuple[dict, int]:
    """CC-270 B2 (overlap): once tier1.<set>.A1.done exists the laptop pulls <set>.A1.jsonl and decomposes it while
    the GPU decodes the rest of phase 1, then pushes <hc>/a1_decomp/<set>.json for every A8 set and
    a1_decomp/MANIFEST.sha256 last. Wait at most A8_WAIT_SEC (funded in P1); over it = STOP, PI, not a cap stop.
    Arrival: sha-checked against that manifest; exactly one decomposition per A1 output id."""
    man = guard(f).parent / "MANIFEST.sha256"
    t0 = clock()
    while not man.exists():
        if clock() - t0 > A8_WAIT_SEC:
            fault(f"no A1 decomposition within A8_WAIT_SEC = {A8_WAIT_SEC} s: STOP, PI")
        sleep(30)
    want = {n: h for h, n in (r.split("  ", 1) for r in man.read_text().splitlines())}
    b = f.read_bytes()
    if want.get(f.name) != hashlib.sha256(b).hexdigest():
        fault(f"{f.name} differs from (or is not in) a1_decomp/MANIFEST.sha256")
    dec = json.loads(b)
    if set(dec) != ids:
        fault(f"{f.name}: decomposition ids differ from the A1 output ids")
    return dec, int(clock() - t0)


def decode(x, gen, image_of, clock=time.time, sleep=time.sleep) -> int:
    """One (set, arm). Tier 1: outputs to <out>/<set>.<arm>.jsonl (appended; a machine-loss resume skips done ids).
    Speed: timing rows only, captions discarded (NB-SPEED)."""
    ds, lang, arms = SETS[x.set]
    if x.arm not in arms:
        fault(f"{x.arm} does not run on {x.set}")
    if ds != "d_vi":
        need(f"DEMOCAP_{ds}")
    kept = kept_ids(x.kept, ds)
    M = json.loads(guard(x.manifest).read_text("utf-8"))
    if (M.get("label"), M.get("set"), M.get("datastore")) != (CP.LABEL, x.set, ds):
        fault("manifest label/set/datastore mismatch")
    norm_ids(list(M["demos"]), kept)
    want = demo_captions(sorted(M["demos"]), x.src)
    if bad := [i for i, d in M["demos"].items() if d["text"] != want[i]]:
        fault(f"{len(bad)} manifest demonstration texts differ from the N8 rule (first {bad[0]!r})")
    qs = M["queries"]
    P = CP.prompts(x.root)
    prior = {}
    if x.speed and x.arm in A8_PROXY:
        fault(f"{x.arm} is not timed; its rate is the A8_PROXY difference")
    if x.arm == "A7" and not x.speed:  # PVR-drop's saved masks (ids + booleans), never re-verified
        rows = (x.out / f"{x.set}.PVR-drop.jsonl").read_text().splitlines()
        prior = {r["id"]: r["masks"] for r in map(json.loads, rows)}
    waited = None
    if x.arm == "A8":
        if not x.a1_decomp:
            fault("A8 needs --a1-decomp")
        a1 = {r["id"]: r["caption"] for r in map(json.loads, (x.out / f"{x.set}.A1.jsonl").read_text().splitlines())}
        dec, waited = a1_decomp(x.a1_decomp, set(a1), clock, sleep)
    if x.speed:
        sp = set(speed_ids([q["id"] for q in qs], x.speed))  # CC-270 N4: once, not per query
        qs = [q for q in qs if q["id"] in sp]
        if x.arm == "A7":  # speed only: no PVR-drop output exists; same calls, no deletion (timing proxy)
            prior = {q["id"]: [[False] * len(M["demos"][i]["props"]) for i in q["ranked"][:CP.K]] for q in qs}
    outp = x.out / f"{x.set}.{x.arm}.jsonl"
    done = set() if x.speed or not outp.exists() else {json.loads(r)["id"] for r in outp.read_text().splitlines()}
    cap = json.loads(x.cap.read_text()) if x.cap else None
    (x.out / "logs").mkdir(parents=True, exist_ok=True)
    log = open(x.out / "logs" / f"{x.set}.{x.arm}.ids.jsonl", "a")
    out = None if x.speed else open(outp, "a")
    if waited is not None:
        write_rec(log, {"utc": utc(), "event": "A8_WAIT", "set": x.set, "arm": x.arm, "sec": waited})
    t0, n = clock(), 0
    for q in qs:
        if q["id"] in done:
            continue
        if cap and left_sec(cap, clock()) <= 0:
            write_rec(log, {"utc": utc(), "event": "CAP_STOP", "set": x.set, "arm": x.arm, "id": q["id"]})
            return CAP_STOP_RC
        img = image_of(q)
        ask = lambda t, img=img: gen(img, CP.ver_prompt(P, t), "verify")[0]  # noqa: E731
        if x.arm == "A8":
            text, st = CP.a8_caption({"A1": a1[q["id"]]}, lambda _c, i=q["id"]: dec[i], ask)
            ids, finish, tpl = [], "a8", "ver_3way.txt"
        else:
            ids, demos, st = demos_for(x.arm, q, M, kept, ask, prior)
            text, finish = gen(img, CP.render(P, demos, lang), "caption")
            tpl = f"cap_{lang}_{'k' if demos else '0'}.txt"
        rec = {"utc": utc(), "set": x.set, "arm": x.arm, "id": q["id"], "demo_ids": ids, "tpl": tpl,
               "finish": finish, **{k: v for k, v in st.items() if k in OUT_KEYS}}
        keep = SPEED_LOG if x.speed else LOG_KEYS  # NB-SPEED: nothing derived from an output is kept
        write_rec(log, {k: v for k, v in rec.items() if k in keep})  # the prompt dump: template + demo ids
        if out:
            write_rec(out, {**rec, "caption": text}, OUT_KEYS)
        n += 1
    if x.speed:
        with open(x.timing, "a") as f:
            f.write(json.dumps({"set": x.set, "lang": lang, "arm": x.arm, "n": n, "sec": int(clock() - t0) + 1}) + "\n")
    return 0


# ---------------------------------------------------------------------------------------------- host steps
def hostcheck_fresh(hc: Path) -> None:
    """HOSTCHECK_OK.json must have been written by the code that runs now (PINS-A §12 Ruling 2(b): a fixed echo is a
    code diff, so an older pass never counts)."""
    rep = json.loads(hc.read_text())
    now = {"c_pvr_gpu_sha256": hashlib.sha256(Path(__file__).read_bytes()).hexdigest(), "c_pvr_sha256": CODE[
        "scripts/c_pvr/c_pvr.py"]}
    if {k: rep.get(k) for k in now} != now:
        fault("HOSTCHECK_OK.json was written by other code; rerun mode selftest")


def preflight(arms) -> None:
    """Never-cut arms with a PENDING pin refuse the whole block (no silent cut)."""
    for a in sorted(NEVER_CUT):
        need(a)
    for a in arms:
        if a in NEEDS:
            need(NEEDS[a])


PHASES = (("A1", "S3", "PVR-drop", "PVR-keep", "A12", "A0", "A6", "A7", "A4", "A9", "S1", "S4", "S5"),  # never-cut
          ("A8", "S2"),  # after the laptop decomposition of A1 / S3, which overlaps phase 1 (B2)
          tuple(reversed(CUT_ORDER)))  # cuttable, A10 last: a cap stop falls here only (CC-270 B1)


def steps(mode: str, cap: dict | None) -> list[tuple[str, str]]:
    """(set, arm), ARM-major over all sets in PHASES order (CC-270 B1); PVR-drop precedes A7 on every set.
    speed: the two speed sets, A8/S2 untimed; tier1: every uncut arm of CAP.json, phases 1-3 in one job."""
    keep = set(cap["arms"]) if cap else set(VI_ARMS + EN_ARMS)
    if mode == "speed":
        keep -= set(A8_PROXY)
    return [(s, a) for a in sum(PHASES, ()) for s, (_, lang, arms) in SETS.items()
            if a in arms and a in keep and (mode != "speed" or s == SPEED_SET[lang])]


def wipe(d: Path, log: Path) -> int:
    """host v3 §4.4: unlink every file, rmdir every dir, append (utc, folder, files, manifest count). No rm -rf.
    The count is the arrival manifest plus the mid-run a1_decomp manifest (B2), each + the manifest itself."""
    mans = [m for m in (d / "MANIFEST.sha256", d / "a1_decomp" / "MANIFEST.sha256") if m.exists()]
    expect = sum(len(m.read_text().splitlines()) + 1 for m in mans) if (d / "MANIFEST.sha256").exists() else -1
    files = 0
    for top, dirs, names in os.walk(d, topdown=False):
        for nm in names:
            os.unlink(os.path.join(top, nm))
            files += 1
        for nm in dirs:
            os.rmdir(os.path.join(top, nm))
    os.rmdir(d)
    with open(log, "a") as f:
        f.write(f"{utc()}\t{d}\t{files}\t{expect}\n")
    return 0 if files == expect else 5


def hostcheck(x) -> dict:
    """GPU-host selftest (PINS-A §11/§12): weights_only, GenerationConfig, prompt echo on the pinned mBLIP, ids-only
    writer, kept-id re-hash, str-id normalisation, peak VRAM. Writes HOSTCHECK_OK.json; speed/tier1 need it."""
    import numpy as np
    import torch
    weights_only_guard(torch)  # before transformers is imported
    from PIL import Image
    from transformers import GenerationConfig
    rep = {"label": CP.LABEL, "utc": utc(), "c_pvr_gpu_sha256": hashlib.sha256(Path(__file__).read_bytes()).hexdigest(),
           "c_pvr_sha256": CODE["scripts/c_pvr/c_pvr.py"], "freeze_sha256": os.environ.get("C_PVR_FREEZE", "")}
    work = x.out / "hostcheck"
    work.mkdir(parents=True, exist_ok=True)
    check_weights_only(torch, work)
    rep["genconfig_none_keys"] = check_genconfig(GenerationConfig)
    model, proc = CP.load_mblip(x.mblip)
    model = model.to("cuda")
    probe = echo_probe(model)
    img = Image.new("RGB", (384, 384), (120, 160, 200))  # synthetic: no dataset image is opened
    rep["echo"] = check_echo(lambda i, p, k: CP.generate(model, proc, i, p, k), probe, CP.prompts(x.root), img)
    rep["kept"] = {k: len(kept_ids(x.kept, k)) for k in KEPT}
    del model
    torch.cuda.empty_cache()
    rep["helpers"] = {}
    for name in HELPERS:  # S9 §8.1 + §8.3: pins, then both pickles load under weights_only=True
        snap = Path((x.out / f"{name}_snapshot.path").read_text().strip())
        helper_check(snap, name)
        pk = [f for f in HELPERS[name][2] if f.endswith(".bin")]
        for f in pk:
            torch.load(snap / f, map_location="cpu")
        rep["helpers"][name] = {"pins": "ok", "weights_only_loaded": pk}
    common_checks(work, np)
    rep["vram_peak_bytes"] = torch.cuda.max_memory_allocated()
    (x.out / "HOSTCHECK_OK.json").write_text(json.dumps(rep, indent=1, sort_keys=True) + "\n")
    return rep


def common_checks(work: Path, np) -> None:
    """Checks that need no GPU and no real data; run by hostcheck and by the laptop selftest alike."""
    with open(work / "ids.jsonl", "w") as f:
        write_rec(f, {"utc": utc(), "set": "xm3600_vi", "arm": "A1", "id": "0004886b7d043cfd", "demo_ids": ["9", "25"]})
        for bad in ({"id": "a cat on a mat"}, {"prompt": "x"}, {"demo_ids": ["9", "một con chó"]}):
            try:
                write_rec(f, bad)
            except SystemExit as e:
                assert "ids-only" in str(e) or "not an id" in str(e), e
            else:
                fault(f"ids-only writer accepted {bad}")
    uni = frozenset({"9", "25", "388662"})
    np.savez(work / "mem.npz", ids=np.array([9, 25, 388662], np.int64))
    raw = np.load(work / "mem.npz")["ids"]
    assert raw.dtype == np.int64 and raw[0] not in uni  # the CC-261 defect: int64 never matches a str id
    assert norm_ids(raw, uni) == ["9", "25", "388662"] and norm_ids([9, "25"], uni) == ["9", "25"]
    for bad in (np.array([9.0]), np.array([10], np.int64)):  # "9.0" and an id outside the set: fail closed
        _must("outside the kept set", norm_ids, bad, uni)


# ---------------------------------------------------------------------------------------------- laptop selftest
def _must(msg: str, fn, *a, **k) -> None:
    try:
        fn(*a, **k)
    except SystemExit as e:
        assert msg in str(e), (msg, str(e))
    else:
        raise AssertionError(f"no FAULT: {msg}")


def _st_money() -> None:
    r, s = 9282, 51051  # T1-REP §9 worked example
    assert (h_m(M_BASE, s, r), h_m(M_PQC2, s, r)) == (31, 43)
    assert ceil125(30 * 3600) == 38 and ceil125(1) == 1 and ceil125(14400 * 31 // 5) == 31
    for per, cuts in ((5760, ["A10", "A5", "A3", "A2"]), (7200, ["A10", "A5", "A3"])):  # v = 0.8 / 1.0
        arms = {a: per for a in VI_ARMS} | ({e: 6 * 3600 // 5 for e in EN_ARMS} if per == 5760 else {})
        p = cap_plan(arms, s, r, True)
        assert (p["decision"], p["m"], p["cuts"], p["cap_h"]) == ("RUN", M_BASE, cuts, 30), p
        assert p["block_max_vnd"] == 338_793 and p["block_max_vnd"] <= M_BASE
    edge = {"A1": 14400 * 31 // 5}  # ceil(1.25 P1) == H_350k exactly: fits, no cut
    assert cap_plan(edge, s, r, True)["cuts"] == [] and cap_plan({"A1": 14400 * 31 // 5 + 1}, s, r, False)["decision"] == "PI"
    assert cap_plan(edge, s, r, True, 1)["m"] == M_PQC2  # B2: the A8 wait bound counts in P1 like a never-cut arm
    assert r_host_up("10053.38") == 10054 and r_host_up("10054") == 10054 and h_m(M_BASE, 0, 10054) == 33  # N1
    _must("not a positive rate", r_host_up, "0")
    big = {a: 2 * 3600 for a in VI_ARMS} | {"S1": 14 * 3600}  # all 5 cut: 34 h -> 43 = H_465k, fits only at 465k
    p = cap_plan(big, s, r, True)
    assert (p["m"], p["cuts"], p["cap_h"]) == (M_PQC2, list(CUT_ORDER), ceil125(sum(big.values()) - 5 * 7200))
    assert cap_plan(big, s, r, False)["decision"] == "PI"
    assert cap_plan({a: 4 * 3600 for a in VI_ARMS}, s, r, True)["decision"] == "PI"
    tim = [{"set": "xm3600_vi", "lang": "vi", "arm": a, "n": 200, "sec": 300} for a in VI_ARMS if a != "A8"]
    tim = [t | {"sec": 900} if t["arm"] == "PVR-drop" else t for t in tim]
    tim += [{"set": "kt_c", "lang": "en", "arm": a, "n": 200, "sec": 400} for a in EN_ARMS if a != "S2"]
    sizes = {k: 100 for k in SETS}
    pr = project(tim, sizes)
    assert pr["A1"] == 5 * 150 and pr["A8"] == 3 * 5 * 100 and pr["A12"] == 150 and pr["S2"] == 0
    _must("speed test incomplete", project, [t for t in tim if t["arm"] != "A11"], sizes)  # N3
    _must("'A8', 'PVR-drop'", project, [t for t in tim if t["arm"] != "PVR-drop"], sizes)  # proxy input missing
    cap = {"p1_epoch": 1000, "cap_h": 2}
    assert left_sec(cap, 1000) == 7200 and left_sec(cap, 8200) == 0


def _dc(t: str, words: list[str]) -> dict:
    sp = [{"start": t.index(w), "end": t.index(w) + len(w), "kind": "obj", "classes": [w.split()[-1]]} for w in words]
    return {"text": t, "sents": [[0, len(t)]], "props": [{**p, "text": t[p["start"]:p["end"]]} for p in sp],
            "nouns": [[p["start"], p["end"]] for p in sp]}


def _st_decode(work: Path) -> None:
    import types
    texts = {f"{j}": f"Ba ấm đồng số{j} và một con mèo." for j in range(10, 20)}  # KT_ID form
    demos = {i: _dc(t, ["Ba ấm đồng", "một con mèo"]) for i, t in texts.items()}
    assert {k: (v[1], v[2][:8]) for k, v in KEPT.items()} == {
        "d_vi": (9098, "753cf695"), "d_tc": (20842, "a5f32465"), "d_en": (80040, "619839a8")}  # OPS-1106c-datastores
    kdir = work / "kept"
    kdir.mkdir()
    body = "".join(f"{i}\n" for i in sorted(texts)).encode()
    KEPT["d_vi"] = ("d_vi_kept_ids.txt", 10, hashlib.sha256(body).hexdigest())
    (kdir / "d_vi_kept_ids.txt").write_bytes(body)
    src = work / "src"
    src.mkdir()
    ann = [{"image_id": int(i), "caption": "  " + t + " "} for i, t in texts.items()]
    ann += [{"image_id": int(i), "caption": "Chú thích thứ hai."} for i in texts]
    (src / DEMO_SRC["ktvic_train"]).write_text(json.dumps({"annotations": ann}, ensure_ascii=False))
    (src / DEMO_SRC["openviic_train"]).write_text(json.dumps({"00000000002.jpg": {"captions": ["Ảnh OV một.", "x"]}},
                                                             ensure_ascii=False))
    CR.LISTS_IN.update({k: ("fixture", hashlib.sha256((src / f).read_bytes()).hexdigest()) for k, f in DEMO_SRC.items()})
    qs = [{"id": f"q{j}", "image": f"q{j}.jpg", "ranked": [str(10 + (j + i) % 10) for i in range(7)], "absent": ["mèo"]}
          for j in range(5)]
    man = work / "m.json"
    man.write_text(json.dumps({"label": CP.LABEL, "set": "xm3600_vi", "datastore": "d_vi", "queries": qs,
                               "demos": demos}, ensure_ascii=False))
    seen = []

    def gen(img, prompt, kind):
        seen.append((kind, prompt))
        return ("no" if "mèo" in prompt else "yes", "eos") if kind == "verify" else ("Một bức ảnh.", "eos")

    out = work / "out"
    out.mkdir()
    base = dict(set="xm3600_vi", manifest=man, kept=kdir, out=out, root=ROOT, speed=0, timing=None, cap=None,
                a1_decomp=None, src=src)
    run = lambda **k: decode(types.SimpleNamespace(**(base | k)), gen, lambda q: "IMG")  # noqa: E731
    for a in ("A0", "A1", "A2", "A3", "A6", "A11", "A12", "PVR-drop", "PVR-keep", "A7"):
        assert run(arm=a) == 0, a
    rows = lambda a: [json.loads(r) for r in (out / f"xm3600_vi.{a}.jsonl").read_text().splitlines()]  # noqa: E731
    assert [r["demo_ids"] for r in rows("A1")][0] == ["10", "11", "12", "13"] and rows("A0")[0]["demo_ids"] == []
    pd = rows("PVR-drop")[0]
    assert pd["masks"] == [[False, True]] * 4 and pd["no"] == 4 and pd["calls"] == 8
    assert [sum(map(sum, r["masks"])) for r in rows("PVR-drop")] == [4] * 5
    assert run(arm="A1") == 0 and len(rows("A1")) == 5  # resume skips done ids
    blob = b"".join(f.read_bytes() for f in out.rglob("*.jsonl"))
    assert not any(t.encode() in blob for t in texts.values()) and b"Captions" not in blob  # no demo text, no prompt
    assert "Một bức ảnh." in (out / "xm3600_vi.A1.jsonl").read_text("utf-8")
    assert b"caption" not in b"".join(f.read_bytes() for f in (out / "logs").iterdir())
    for a in ("A4", "A5", "A9", "A10"):
        _must("PENDING", run, arm=a)
    _must("PENDING", preflight, ["A1"])
    sp = steps("speed", None)
    assert ("xm3600_vi", "A8") not in sp and ("kt_c", "S1") in sp and {s for s, _ in sp} == {"xm3600_vi", "kt_c"}
    _st_steps()
    _must("does not run", run, arm="S1")
    _must("DEMOCAP_d_tc", run, set="t_a", arm="A1")  # N9: before any d_tc / d_en file is read
    _must("DEMOCAP_d_en", run, set="kt_c", arm="S3")
    tim = work / "t.jsonl"
    seen.clear()
    (work / "o2").mkdir()
    assert run(arm="A1", speed=2, timing=tim, out=work / "o2") == 0
    assert not (work / "o2" / "xm3600_vi.A1.jsonl").exists() and json.loads(tim.read_text())["n"] == 2
    assert run(arm="PVR-drop", speed=2, timing=tim, out=work / "o2") == 0
    sl = [json.loads(r) for r in (work / "o2/logs/xm3600_vi.PVR-drop.ids.jsonl").read_text().splitlines()]
    assert len(sl) == 2 and all(set(r) <= SPEED_LOG for r in sl) and sl[0]["calls"] == 8
    assert run(arm="A7", speed=2, timing=tim, out=work / "o2") == 0
    _must("not timed", run, arm="A8", speed=2, timing=tim)
    _st_a8(work, rows, run, base, gen)
    capf = work / "cap.json"
    capf.write_text(json.dumps({"p1_epoch": 0, "cap_h": 1}))
    assert run(arm="A3", cap=capf, out=work / "o2") == CAP_STOP_RC  # wall clock long past the stamp
    _st_democap(src, texts, man, run, work)
    bad = dict(json.loads(man.read_text()))
    bad["queries"] = [qs[0] | {"ranked": [13, 14, 15, 16, 17, 18, "99"]}]
    man.write_text(json.dumps(bad, ensure_ascii=False))
    _must("outside the kept set", run, arm="A1", out=work / "o2")
    (kdir / "d_vi_kept_ids.txt").write_bytes(body + b"x\n")
    _must("differs from its pin", run, arm="A1")
    _must("REFUSED", kept_ids, work / "t2pool_x", "d_vi")


def _st_steps() -> None:
    """CC-270 B1 over the FULL steps() list: phase 1 (never-cut, A1/S3 first on every set) < A8/S2 < cuttable."""
    sp = steps("speed", None)
    assert ("xm3600_vi", "A8") not in sp and ("kt_c", "S2") not in sp and ("kt_c", "S1") in sp
    assert {s for s, _ in sp} == {"xm3600_vi", "kt_c"} and len(sp) == 14 + 4
    flat = sum(PHASES, ())
    assert sorted(flat) == sorted(VI_ARMS + EN_ARMS) and len(flat) == len(set(flat)) and PHASES[2][-1] == "A10"
    full = steps("tier1", None)
    vi = [s for s, (_, _, arms) in SETS.items() if "A1" in arms]
    assert len(full) == len(set(full)) == sum(len(a) for _, _, a in SETS.values()) == 76
    assert full[:6] == [(s, "A1") for s in vi] + [("kt_c", "S3")]
    pos = lambda arms: [i for i, (_, a) in enumerate(full) if a in arms]  # noqa: E731
    assert max(pos(PHASES[0])) < min(pos(PHASES[1])) <= max(pos(PHASES[1])) < min(pos(CUT_ORDER))
    assert [a for _, a in full[-25:]] == [a for a in reversed(CUT_ORDER) for _ in vi]  # A11 x5 ... A10 x5
    assert all(full.index((s, "PVR-drop")) < full.index((s, "A7")) for s in vi)
    t1 = steps("tier1", {"arms": [a for a in VI_ARMS if a not in ("A10", "A5")]})
    assert ("t_a", "A12") not in t1 and ("xm3600_vi", "A10") not in t1 and ("kt_c", "S1") not in t1
    assert [a for _, a in t1[-15:]] == ["A11"] * 5 + ["A2"] * 5 + ["A3"] * 5 and t1[-1] == ("t_a", "A3")


def _st_a8(work: Path, rows, run, base: dict, gen) -> None:
    """CC-270 B2: A8 waits (bounded) for the pushed decomposition, sha-checks it and binds it to the A1 ids."""
    import types
    a1 = {r["id"]: r["caption"] for r in rows("A1")}
    dd = work / "a1_decomp"
    dd.mkdir()
    dec = dd / "xm3600_vi.json"
    dec.write_text(json.dumps({i: _dc("Một con mèo ngủ.", ["Một con mèo"]) for i in a1}, ensure_ascii=False))
    man = dd / "MANIFEST.sha256"
    good = f"{hashlib.sha256(dec.read_bytes()).hexdigest()}  {dec.name}\n"
    t = {"now": 0.0, "sleeps": 0}

    def sleep(sec, arrive_at=None):
        t["now"] += sec
        t["sleeps"] += 1
        assert t["sleeps"] < 10_000, "unbounded A8 wait"
        if t["sleeps"] == arrive_at:
            man.write_text(good)

    def run8(arrive_at=None):
        t.update(now=0.0, sleeps=0)
        return decode(types.SimpleNamespace(**(base | {"arm": "A8", "a1_decomp": dec})), gen, lambda q: "IMG",
                      clock=lambda: t["now"], sleep=lambda s: sleep(s, arrive_at))

    _must("STOP, PI", run8)  # never pushed: over A8_WAIT_SEC
    assert t["now"] > A8_WAIT_SEC and not (base["out"] / "xm3600_vi.A8.jsonl").exists()
    _must("needs --a1-decomp", run, arm="A8")
    man.write_text("0" * 64 + f"  {dec.name}\n")
    _must("differs from (or is not in)", run8)
    full = dec.read_text("utf-8")
    dec.write_text(json.dumps(dict(list(json.loads(full).items())[1:]), ensure_ascii=False))  # one A1 id missing
    man.write_text(f"{hashlib.sha256(dec.read_bytes()).hexdigest()}  {dec.name}\n")
    _must("decomposition ids differ", run8)
    dec.write_text(full, "utf-8")
    man.unlink()
    assert run8(arrive_at=3) == 0 and rows("A8")[0]["caption"] == "" and rows("A8")[0]["emptied"] is True
    w = [json.loads(r) for r in (base["out"] / "logs/xm3600_vi.A8.ids.jsonl").read_text().splitlines()][0]
    assert (w["event"], w["sec"]) == ("A8_WAIT", 90)


def _st_democap(src: Path, texts: dict, man: Path, run, work: Path) -> None:
    """N8 rule (CC-269r2 Ruling 4, W1-W3): first caption in source order, int image_id matched as str, form routing."""
    got = demo_captions(["13", "00000000002.jpg"], src)
    assert got == {"13": texts["13"], "00000000002.jpg": "Ảnh OV một."}, got  # first, cleaned; not the 2nd caption
    for bad, msg in (("99", "no caption"), ("003", "source form"), ("12345678901.png", "no caption"), ("x", "form")):
        _must(msg, demo_captions, [bad], src)
    kt = src / DEMO_SRC["ktvic_train"]
    keep = kt.read_bytes()
    kt.write_bytes(keep + b" ")
    _must("differs from its lists pin", demo_captions, ["13"], src)
    kt.write_bytes(keep)
    M = json.loads(man.read_text())
    M["demos"]["13"] = {**M["demos"]["13"], "text": "Chú thích thứ hai."}
    (work / "m2.json").write_text(json.dumps(M, ensure_ascii=False))
    _must("differ from the N8 rule", run, arm="A1", manifest=work / "m2.json")
    assert {k: (v[0], len(v[2])) for k, v in HELPERS.items()} == {
        "mclip": ("laion/CLIP-ViT-H-14-frozen-xlm-roberta-large-laion5B-s13B-b90k", 3),
        "xlmr": ("xlm-roberta-large", 3 + 1), "xglm": ("facebook/xglm-2.9B", 7)}
    assert HELPERS["xglm"][2]["pytorch_model.bin"][1][:8] == "9aa29d66" and HELPERS["mclip"][1][:8] == "f9ab9552"
    snap = work / "snap"
    snap.mkdir()
    (snap / "w.bin").write_bytes(b"w")
    (snap / "c.json").write_bytes(b"{}")
    HELPERS["t"] = ("t", "r", {"w.bin": ("lfs", hashlib.sha256(b"w").hexdigest()),
                               "c.json": ("blob", hashlib.sha1(b"blob 2\0{}").hexdigest())})
    try:
        helper_check(snap, "t")
        (snap / "c.json").write_bytes(b"[]")
        _must("differs from its S9 pin", helper_check, snap, "t")
    finally:
        del HELPERS["t"]


def _st_wipe(work: Path) -> None:
    d = work / "shm"
    (d / "img").mkdir(parents=True)
    for j in range(3):
        (d / "img" / f"{j}.jpg").write_bytes(b"x")
    (d / "MANIFEST.sha256").write_text("a  img/0.jpg\nb  img/1.jpg\nc  img/2.jpg\n")
    log = work / "del.log"
    assert wipe(d, log) == 0 and not d.exists()
    assert log.read_text().split("\t")[2:] == ["4", "4\n"]
    (d / "x").mkdir(parents=True)
    (d / "x" / "stray").write_bytes(b"")
    assert wipe(d, log) == 5 and not d.exists()
    (d / "a1_decomp").mkdir(parents=True)  # B2: the mid-run push is counted by its own manifest
    (d / "MANIFEST.sha256").write_text("")
    (d / "a1_decomp" / "xm3600_vi.json").write_bytes(b"{}")
    (d / "a1_decomp" / "MANIFEST.sha256").write_text("a  xm3600_vi.json\n")
    assert wipe(d, log) == 0 and not d.exists() and log.read_text().splitlines()[-1].split("\t")[2:] == ["3", "3"]


def selftest() -> None:
    import socket
    import tempfile

    import numpy as np
    try:
        import torch
    except ImportError:
        torch = None
    try:
        from transformers import GenerationConfig
    except ImportError:
        GenerationConfig = None

    def no_net(*a, **k):
        raise OSError("selftest: network disabled")

    socket.socket, socket.create_connection = no_net, no_net  # type: ignore[assignment,misc]  after the imports
    pend, kept0, lists0 = dict(PINS), dict(KEPT), dict(CR.LISTS_IN)
    with tempfile.TemporaryDirectory() as td:
        work = Path(td)
        if torch is not None:  # real torch: the wrapper on the real loader
            check_weights_only(torch, work)
        if GenerationConfig is not None:
            nk = check_genconfig(GenerationConfig)
            assert "temperature" in nk["caption"] and "top_p" in nk["verify"]

        class GC:  # a GenerationConfig that drops a pinned key must FAULT
            def __init__(self, **k):
                self.k = {a: b for a, b in k.items() if a != "num_beam_groups"}

            def to_dict(self):
                return self.k
        _must("drops or changes", check_genconfig, GC)
        _st_echo()
        common_checks(work, np)
        _st_money()
        try:  # CC-270 N10: the fixture overrides KEPT["d_vi"] and CR.LISTS_IN; restored on every path
            _st_decode(work)
        finally:
            KEPT.clear()
            KEPT.update(kept0)
            CR.LISTS_IN.clear()
            CR.LISTS_IN.update(lists0)
        _st_wipe(work)
        hc = work / "HOSTCHECK_OK.json"
        mine = hashlib.sha256(Path(__file__).read_bytes()).hexdigest()
        hc.write_text(json.dumps({"c_pvr_gpu_sha256": mine, "c_pvr_sha256": CODE["scripts/c_pvr/c_pvr.py"]}))
        hostcheck_fresh(hc)
        hc.write_text(json.dumps({"c_pvr_gpu_sha256": "0" * 64, "c_pvr_sha256": CODE["scripts/c_pvr/c_pvr.py"]}))
        _must("other code", hostcheck_fresh, hc)
        _must("REFUSED", guard, Path.home() / ".vsps_sealed" / "c_pvr")
    assert PINS == pend and all(v == PENDING for v in PINS.values()) and KEPT == kept0 and CR.LISTS_IN == lists0
    print(f"selftest ok  {CP.LABEL}  c_pvr_gpu.py {hashlib.sha256(Path(__file__).read_bytes()).hexdigest()}  "
          f"torch={'real' if torch else 'absent'} transformers={'real' if GenerationConfig else 'absent'}")


def _st_echo() -> None:
    """CP.generate on a fake model: an output that starts with the prompt ids is stripped (pass); one that starts
    with image tokens and then the prompt is not stripped and must FAULT on the decoded text."""
    import types

    class T(list):
        def tolist(self):
            return list(self)

    class B(dict):
        def to(self, *a):
            return self

    vocab = {}

    class Tok:
        eos_token_id, pad_token_id = 2, 3

        def decode(self, ids, skip_special_tokens):
            inv = {v: k for k, v in vocab.items()}
            return " ".join(inv.get(i, "") for i in ids if i > 9).strip()

    class Proc:
        tokenizer = Tok()

        def __call__(self, images, text, return_tensors):
            return B(input_ids=T([T([vocab.setdefault(w, 10 + len(vocab)) for w in text[0].split()])]))

    class Model:
        device = "cpu"
        lead = []

        def generate(self, **k):
            return T([T(self.lead + list(k["input_ids"][0]) + [vocab.setdefault("chó", 99), 2])])

    th = types.SimpleNamespace(bfloat16="bf16", inference_mode=lambda: open(os.devnull))
    tr = types.SimpleNamespace(GenerationConfig=lambda **k: types.SimpleNamespace(**k))
    old = {m: sys.modules.get(m) for m in ("torch", "transformers")}
    sys.modules.update(torch=th, transformers=tr)
    try:
        m, p = Model(), Proc()
        probe = echo_probe(m)
        P = CP.prompts(ROOT)
        rep = check_echo(lambda i, pr, k: CP.generate(m, p, i, pr, k), probe, P, "IMG")
        assert rep["caption"]["strip_branch"] is True and rep["verify"]["finish"] == "eos"
        Model.lead = [5]  # e.g. image/query tokens before the prompt: the id-prefix strip misses
        _must("prompt echo", check_echo, lambda i, pr, k: CP.generate(m, p, i, pr, k), probe, P, "IMG")
    finally:
        for k, v in old.items():
            sys.modules.pop(k, None) if v is None else sys.modules.__setitem__(k, v)


# ---------------------------------------------------------------------------------------------- cli
def main() -> int:
    ap = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    sp = ap.add_subparsers(dest="cmd", required=True)
    sp.add_parser("selftest")
    pf = sp.add_parser("preflight")
    pf.add_argument("--arms", nargs="*", default=[])
    pf.add_argument("--hostcheck", type=Path, required=True)
    h = sp.add_parser("hostcheck")
    for a in ("--mblip", "--kept", "--out"):
        h.add_argument(a, type=Path, required=True)
    d = sp.add_parser("decode")
    d.add_argument("--set", choices=SETS, required=True)
    d.add_argument("--arm", required=True)
    for a in ("--manifest", "--kept", "--out"):
        d.add_argument(a, type=Path, required=True)
    for a in ("--timing", "--a1-decomp", "--cap", "--images", "--src"):
        d.add_argument(a, type=Path)
    d.add_argument("--speed", action="store_const", const=SPEED_N, default=0)
    c = sp.add_parser("cap")
    for a in ("--timing", "--sizes", "--out"):
        c.add_argument(a, type=Path, required=True)
    for a in ("--s-vnd", "--p1-epoch"):
        c.add_argument(a, type=int, required=True)
    c.add_argument("--r-host", required=True, help="rental-line VND/h as written; rounded up (N1)")
    c.add_argument("--pqc2-solvent", choices=("yes", "no"), required=True)
    sp.add_parser("left").add_argument("--cap", type=Path, required=True)
    st = sp.add_parser("steps")
    st.add_argument("--mode", choices=("speed", "tier1"), required=True)
    st.add_argument("--cap", type=Path)
    sp.add_parser("snapcheck").add_argument("--mblip", type=Path, required=True)
    w = sp.add_parser("wipe")
    w.add_argument("--dir", type=Path, required=True)
    w.add_argument("--log", type=Path, required=True)
    x = ap.parse_args()
    x.root = ROOT
    if x.cmd == "wipe":
        return wipe(x.dir, x.log)
    load()
    if x.cmd == "selftest":
        return selftest()
    if x.cmd == "preflight":
        hostcheck_fresh(x.hostcheck)
        return preflight(x.arms)
    if x.cmd == "steps":
        cap = json.loads(x.cap.read_text()) if x.cap else None
        if x.mode != "speed" and (cap or {}).get("decision") != "RUN":
            fault("tier1 needs CAP.json with decision RUN (the P1 line)")
        return print("\n".join(f"{s} {a}" for s, a in steps(x.mode, cap)))
    if x.cmd == "snapcheck":
        bad = [f for f, h in CP.MBLIP["files"].items() if CP.sha_file(x.mblip / f) != h]
        return fault(f"mBLIP files differ from PINS-A: {bad}") if bad else print("mblip pins ok", CP.MBLIP["revision"])
    if x.cmd == "left":
        cap = json.loads(x.cap.read_text())
        if cap.get("decision") != "RUN":
            fault("CAP.json decision is not RUN: nothing is decoded (T1-REP §9 rule 4 -> PI)")
        return print(max(0, left_sec(cap, time.time())))
    if x.cmd == "cap":
        if x.out.exists():
            fault(f"{x.out} exists: the P1 rule is applied once (a machine-loss resume goes to the PI)")
        r = r_host_up(x.r_host)
        plan = cap_plan(project([json.loads(row) for row in x.timing.read_text().splitlines()],
                                json.loads(x.sizes.read_text())), x.s_vnd, r, x.pqc2_solvent == "yes", A8_WAIT_SEC)
        plan |= {"label": CP.LABEL, "p1_epoch": x.p1_epoch, "s_vnd": x.s_vnd, "r_host_line": x.r_host, "r_host": r,
                 "a8_wait_sec": A8_WAIT_SEC, "t_down_vnd": T_DOWN_H * r,
                 "rule": "T1-REP v4 §9 (4124ef3); host v3 §2-§3 (5d6f5ca); CC-270 B2, N1"}
        x.out.write_text(json.dumps(plan, indent=1, sort_keys=True) + "\n")
        print(json.dumps(plan, sort_keys=True))
        return 0 if plan["decision"] == "RUN" else 3
    if x.cmd == "hostcheck":
        return print(json.dumps(hostcheck(x), sort_keys=True))
    import torch
    weights_only_guard(torch)
    from PIL import Image
    if x.arm in EN_ARMS:
        CP.load_llava()  # FAULTs until Q-LLAVA pins (PINS-A §12)
    model, proc = CP.load_mblip(Path(os.environ["C_PVR_MBLIP"]))
    model = model.to("cuda")

    def image_of(q):
        p = guard(x.images / q["image"])
        if hashlib.sha256(p.read_bytes()).hexdigest() != q["image_sha256"]:
            fault(f"image of {q['id']} differs from the manifest sha")
        return Image.open(p).convert("RGB")
    return decode(x, lambda i, p, k: CP.generate(model, proc, i, p, k), image_of)


if __name__ == "__main__":
    sys.exit(main())
