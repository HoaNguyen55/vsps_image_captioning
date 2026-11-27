#!/usr/bin/env python3
"""B-ALT FE-LOCUS (Paper B, LRE; RQ9 / Objective 3.3): is the CIDEr-D shift between the RDRSegmenter and pyvi word
units carried by a short reference-derived list of frequent disagreement types (pin list), or by the long tail?

Registration: manuscript/prereg/2026-11-27_b_alt/PREREG_DRAFT_B_ALT_v2.md (sha256 ed05acdb...; CC-510, CC-510r2,
CC-510e1; commit 2d3c39f) with ERRATUM_B_ALT_1.md (8367face...; CC-510e2, commit 7f7cf4f: the host rule). The FE-CERT code (scripts/b_fecert/b_fecert.py and every repository module it imports) is reused
unchanged, pinned by sha256 before import (PINS), with a closure check after import. scripts/b_d1/b_d1.py is reused
unchanged for the CPU budget (run_stage.sh calls `b_d1.py budget` on this study's own records directory).

Stages (registered order, prereg v2 §5), each under run_stage.sh (8 CPU-h hard stop, child processes included):
  s1a  census on half-A references only -> CENSUS_ALT.json (pin list and dictionary; host only, never committed)
  s1b  re-score (no decoding): per-image CIDEr-D under the 36 G_w members, their 36 Pi_head-pinned and 36
       Pi_all-pinned versions, plus image-level disagreement counts on references and outputs -> PER_IMAGE_ALT.npz
  g0   reproduction gate on the full 558 images against DEV.json -> G0_ALT.json
  s2   rho_head, rho_all, kappa_head per bootstrap draw on half B; floors; H-L1, H-L2; DESCRIPTIVE rows
       -> RESULT_ALT.json (aggregates only)

  NCS_DATA=D python -I -B scripts/b_alt/b_alt.py s1a --work W --out O --pyvi-wheel P --uts-wheel U
  NCS_DATA=D python -I -B scripts/b_alt/b_alt.py s1b --work W --out O --baselines B --pyvi-wheel P --uts-wheel U \
      --census-sha <CENSUS_ALT.json sha256>
  NCS_DATA=D python -I -B scripts/b_alt/b_alt.py g0 --work W --out O --npz-sha <PER_IMAGE_ALT.npz sha256>
  NCS_DATA=D python -I -B scripts/b_alt/b_alt.py s2 --work W --out O --census-sha C --npz-sha N --g0-sha G

No caption or reference text is written or printed. CENSUS_ALT.json holds word-type keys (needed by s1b and s2); it
stays on the host and is committed only if OPEN_QUESTIONS Q4 is answered yes. An unexpected exception prints its type.
"""
from __future__ import annotations

import argparse
import hashlib
import json
import os
import sys
import unicodedata
from collections import Counter
from pathlib import Path

import numpy as np

HERE = Path(__file__).resolve().parent
ROOT = HERE.parents[1]

# ------------------------------------------------------------------------------------------------ pins
PINS = {  # every repository file loaded by `import b_fecert` (as pinned by b_d1 at 38067d1), plus b_d1.py (budget)
    "scripts/b_fecert/b_fecert.py": "67e43dea1b37c3bbfaa3fe5081d6f3d36848397451ad0a24d67fa67389b06b59",
    "scripts/b_fecert/family.py": "7cb2c69b8b7840388568fd5f9b248e2cf25df28185386be875a65d921a9e4178",
    "scripts/kit_b/protocol_pilot.py": "6aee428207a2d1a045cd72d054e26a2e2ac8d9c2e414cb0c161e3b95dffd92bf",
    "scripts/kit_b/ptb_protocol.py": "ea5fbe6e1528e339abfcb9ba00bdd0c4d4e4bde07ae6edd30fffaa72d60754d2",
    "scripts/kit_b/b2_controls.py": "6f2a7258606097e6125bfae2c2bba26a84ff60238548cf82e470d696825af6a3",
    "scripts/kit_b/exchangeability_audit.py": "f30758e372061a15cbab30a568a397f57442f2701e0ffd9cc2372f20901d66a0",
    "scripts/b2_external/b2.py": "52b8c145be0730f02f0ddd782c67dda26451063197ab19c6b723c54f5a783e6d",
    "scripts/b_pa1/b_pa1.py": "c481fcf4811faf2d184e441f589b5f3c9e4206908dc2a42e1829a7215b8398ef",
    "scripts/grl/common.py": "bbe7ee61f659b1a7bfc3cab418d83ed779b76187107708fef2d8ab44df0ad23a",
    "scripts/grl/id_counts.py": "0c590058a908c0683366e385b70c68ca77b4ff80902b7a1398f216ce6e55d859",
    "tools/obj_rater/build_pairs.py": "49692235207762fdea918155115f13b7baa81615635c99788986fa983e677087",
    "tools/obj_rater/pair_server.py": "da36692dc2037f2c06c62d365a92c2e8abf4d12ef759e7ad703e449fc9dbe32e",
    "tools/obj_rater/pair.html": "1dde2ecf734a9adc59bb61c05ff5a8cea25257318c668e5cf18cfb15ed91b8d1",
    "rescap/__init__.py": "b712bea4d66e5e2e0f0cec1624ab244a025560ecc5d86f96cada2e0160a4890f",
    "rescap/chair.py": "e47d249ac7290070f2387d3fa8b22dac77728265ad276f55aa6520f5cbc591a3",
    "rescap/metrics.py": "e0296ec528b87f4d1b31165cbb45deee5453783fd7dad783f248869e596bf960",
    "rescap/repro.py": "723200190818cd61a56527e6a0a1596b95f9d1ed1ebc0cabe1b29135cf03b70d",
    "rescap/vocab.py": "c9143b2d973fc48a2231335844cd91ab702329c0b1aabb802884225e155967ec",
    "rescap/svp/__init__.py": "5b7f52920de75cf59bde0ae657e292a876efc63292ca6db6a4d085bb9fec1424",
    "rescap/svp/entailment.py": "4462f44df80faa0adc620d98aa5d8bbb307243d450e9aee4801bb17a3a06db23",
    "rescap/svp/matching.py": "a9253060131aacfca8eaab9a4b2c473c487db96a7c1222f0b8e31f9f61b24003",
    "rescap/vi/__init__.py": "f898963e95fec7d9fb236295649404815634a1d949bfd74cd7c3b90ed493bf6c",
    "rescap/vi/classifier.py": "966cdab1fed8471ac57d225698e63f1e2a055435a5d669e9cca10eed703fed16",
    "rescap/vi/color.py": "242fc46f68ecb06c8eefde23350481d99e60566b3da64ab90cfa79db38fd3875",
    "rescap/vi/lexicon.py": "fbc945f2247418275144ac75b893f7c51f8951b9ea42018680d433775dd79eb9",
    "scripts/b_d1/b_d1.py": "4e044401361fae00f289ec67ed0ba2afa5f5730fd7384df10357ccff87c65f33",
}
REG = "manuscript/prereg/2026-11-27_b_alt/PREREG_DRAFT_B_ALT_v2.md"
REG_SHA = "ed05acdb7682b516738b00d2741fd87d0220e30eec9aa38ae5a2a92c3014f352"  # after CC-510e1 (alias redaction)
ERRATA = {"manuscript/prereg/2026-11-27_b_alt/ERRATUM_B_ALT_1.md":  # CC-510e2: the §5 host rule
          "8367faceffbd2235d2c4cfe2a0b768c37e0e1d357140a995db5359c9a884958f"}
JAR_SHA_FULL = "9e2811cdbc2ddfc71d04be5dc36e185c88dcd1ad4d5d69e4ff2e1369dccf7793"  # CC-510r2 N8: the full pin


def sha_file(p) -> str:
    h = hashlib.sha256()
    with open(p, "rb") as f:
        for b in iter(lambda: f.read(1 << 20), b""):
            h.update(b)
    return h.hexdigest()


def pin_check(root: Path = ROOT, pins: dict = PINS) -> None:
    bad = [rel for rel, h in pins.items() if not (root / rel).is_file() or sha_file(root / rel) != h]
    if bad:
        raise SystemExit(f"FAULT: {len(bad)} pinned file(s) missing or off their sha256: {', '.join(sorted(bad))}")


pin_check()
sys.path.insert(0, str(ROOT / "scripts/b_fecert"))
import b_fecert as BF  # noqa: E402  reused unchanged
import family as FM  # noqa: E402
import ptb_protocol as PT  # noqa: E402

E4 = BF.E4


def closure_check() -> None:
    """Every repository module loaded so far is in PINS (the new code in scripts/b_alt/ excepted)."""
    loaded = set()
    for m in list(sys.modules.values()):
        f = getattr(m, "__file__", None)
        if f and Path(f).is_file() and str(Path(f).resolve()).startswith(str(ROOT) + os.sep) \
                and Path(f).resolve().parent != HERE:  # "<stdin>" (a here-doc main) is not a file
            loaded.add(str(Path(f).resolve().relative_to(ROOT)))
    extra = sorted(loaded - set(PINS))
    if extra:
        raise SystemExit(f"FAULT: repository module(s) loaded but not pinned: {', '.join(extra)}")


closure_check()

# ------------------------------------------------------------------------------------------------ registered values
INPUT_SHA = {  # prereg v2 §0 (full values, CC-510 W4)
    "DEV.json": "88ff39aa9552b671a0e439aec961d0fefe02df1f52a2a5df9765a9d8226f7e8d",
    "FAMILY.json": "431d92a4a2eaf0516446c9f9aef453ee52d311b6e329d97cd1abb4c4e8017f77",
    "CENSUS.json": "2252167b435890c5dbf70a97e0fc918bc6989c48acda636427d4dd2889599afa",
    "SYSTEMS.tsv": "30ac9555cd6cdc8fd50f47e637e734fac564c692605f590ba213a60a3be6e1a0",
}
REFS_SHA = "cc22ec6a8883773cb23c87ad5b64925f5a53c21982117274b53621f454e7ebbf"
EXPECT_FILES, EXPECT_IMAGES, EXPECT_D = 75, 558, 1101
HALF = 279  # §3.2 step 0: half A = the first 279 of the permutation
SEED_SPLIT, SEED_WB = 20261127, 20261128  # §3.2 step 0; §3.4 W_B
COVER_NUM, COVER_DEN = 4, 5  # §3.2 step 5: cumulative count >= 0.80 of all occurrences
UNALIGNED_MAX = 0.005  # §3.2 step 2: unaligned <= 0.5% of strings, else FAULT
MIN_TYPES = 30  # §4 floor (iii)
SHIFT_FLOOR = 0.01  # §4 floor (iv)
RHO_ALL_FLOOR = 0.20  # §4 floor (v)
PRACTICAL = 0.50  # §4 H-L2
G0_TOL = 1e-6
SEG = None  # the self-test injects stub units here (None = the real units of family.py)

UNITS_W = ("rdr", "pyvi")
LEVELS = [(t, p, c) for t in FM.T_LEVELS for p in FM.P_LEVELS for c in FM.C_LEVELS]  # 18 level triples
RAW = [("rdr",) + lv for lv in LEVELS] + [("pyvi",) + lv for lv in LEVELS]  # G_w, 36 members
PIN_TAGS = ("h", "a")  # Pi_head, Pi_all
MEMS = RAW + [m + (g,) for g in PIN_TAGS for m in RAW]  # 108: raw, then Pi_head-pinned, then Pi_all-pinned
RDR0, PYVI0 = ("rdr", "tw", "pk", "cf"), ("pyvi", "tw", "pk", "cf")  # §3.2 step 1: the census members


def mname(m) -> str:
    return ".".join(m[:4]) + (f"+P{m[4]}" if len(m) == 5 else "")


NAMES = [mname(m) for m in MEMS]
G_W = [mname(m) for m in RAW]


def fault(msg: str):
    raise BF.Fault(msg)


def jload(p):
    return json.loads(Path(p).read_text(encoding="utf-8"))


def write_once(path: Path, obj) -> str:
    if path.exists():
        raise SystemExit(f"REFUSED: {path.name} exists; a stage runs once")
    path.write_text(json.dumps(obj, indent=1, ensure_ascii=False, default=float) + "\n", encoding="utf-8")
    os.chmod(path, 0o444)
    return sha_file(path)


def need(path: Path, want: str, what: str) -> None:
    if not want or not path.is_file() or sha_file(path) != want:
        raise SystemExit(f"REFUSED: {what} is not the file whose sha256 was passed")


def reg_check() -> None:
    for rel, h in {REG: REG_SHA, **ERRATA}.items():
        if not (ROOT / rel).is_file() or sha_file(ROOT / rel) != h:
            fault(f"{rel} is missing or differs from its registered sha256 (prereg v2 ed05acdb, erratum 1)")


def check_inputs(work: Path, fnames) -> dict:
    for f in fnames:
        if not (work / f).is_file() or sha_file(work / f) != INPUT_SHA[f]:
            fault(f"{f} is missing or differs from its registered sha256")
    return {f: INPUT_SHA[f] for f in fnames}


def env_ok(a) -> dict:
    """FE-CERT env_record and env_check unchanged, plus the full jar pin (N8)."""
    env = BF.env_record(a)
    BF.env_check(env)
    if SEG is None and env.get("jar_sha256") != JAR_SHA_FULL:  # real units only; the self-test injects stubs
        fault("the VnCoreNLP jar differs from its full sha256 pin")
    return env


def code_shas() -> dict:
    files = sorted(HERE.glob("*.py")) + [ROOT / r for r in PINS]
    return {str(p.relative_to(ROOT)): sha_file(p) for p in files}


def load_refs_ids() -> tuple[dict, list]:
    if sha_file(BF.REFS) != REFS_SHA:
        fault("test_data.json differs from its registered sha256")
    refs = PT.load_refs(BF.REFS)
    ids = sorted(refs)
    if len(ids) != EXPECT_IMAGES:
        fault(f"{len(ids)} images, not {EXPECT_IMAGES}")
    return refs, ids


# ------------------------------------------------------------------------------------------------ §3.2 split
def split(ids: list) -> tuple[list, list]:
    """CC-510 N4: ids = sorted(ids); perm = default_rng(20261127).permutation(558); half A = ids[perm[:279]]."""
    ids = sorted(ids)
    perm = np.random.default_rng(SEED_SPLIT).permutation(len(ids))
    return [ids[k] for k in perm[:HALF]], [ids[k] for k in perm[HALF:]]


# ------------------------------------------------------------------------------------------------ syllables, spans
def syl_key(s: str) -> str:
    """§3.2 step 2: NFC, the tone mark moved by the tm rule, lower case."""
    return unicodedata.normalize("NFC", FM.tone(unicodedata.normalize("NFC", s), "tm")).casefold()


def explode(toks: list[str]):
    """Tokens -> (syllables, boundary vector b with b[j] = a token boundary between syllables j and j+1), or None when
    a token has an empty piece around '_' (a malformed token: the string is unaligned)."""
    syl, b = [], []
    for w in toks:
        parts = w.split("_")
        if any(p == "" for p in parts):
            return None
        if syl:
            b.append(True)
        syl += parts
        b += [False] * (len(parts) - 1)
    return syl, b


def rebuild(syl: list[str], b: list[bool]) -> list[str]:
    if not syl:
        return []
    out, cur = [], [syl[0]]
    for j, s in enumerate(syl[1:]):
        if b[j]:
            out.append("_".join(cur))
            cur = [s]
        else:
            cur.append(s)
    out.append("_".join(cur))
    return out


def spans(ba: list[bool], bb: list[bool], n: int) -> list[tuple[int, int]]:
    """§3.2 step 3: maximal runs [i, j) whose ends are boundaries under both and inside which the boundary sets
    differ (the runs between consecutive common boundaries)."""
    cut = [0] + [j + 1 for j in range(n - 1) if ba[j] and bb[j]] + [n]
    return [(s, e) for s, e in zip(cut, cut[1:]) if e - s >= 2 and ba[s:e - 1] != bb[s:e - 1]]


def disagreements(ta: list[str], tb: list[str]):
    """Tokens of the rdr and pyvi census members for one string -> [(type, rdr pattern)], or None (unaligned)."""
    ea, eb = explode(ta), explode(tb)
    if ea is None or eb is None:
        return None
    ka, kb = [syl_key(s) for s in ea[0]], [syl_key(s) for s in eb[0]]
    if ka != kb:
        return None
    return [(tuple(ka[s:e]), tuple(ea[1][s:e - 1])) for s, e in spans(ea[1], eb[1], len(ka))]


# ------------------------------------------------------------------------------------------------ §3.2 census
def census(strings: list[str], tk) -> dict:
    """Disagreement census over the given reference strings (half A only; the caller passes nothing else)."""
    occ, pats, unaligned = Counter(), {}, 0
    for r in strings:
        d = disagreements(tk.tokens(r, RDR0), tk.tokens(r, PYVI0))
        if d is None:
            unaligned += 1
            continue
        for t, p in d:
            occ[t] += 1
            pats.setdefault(t, Counter())[p] += 1
    return {"occ": occ, "pats": pats, "unaligned": unaligned, "strings": len(strings)}


def type_str(t) -> str:
    return " ".join(t)


def pin_lists(occ: Counter, pats: dict) -> dict:
    """§3.2 steps 4-6: rank by count desc, ties by code-point order of the type; Pi_head = shortest prefix with
    cumulative count >= 0.80 of all; dictionary = modal rdr pattern, ties -> fewer tokens -> smallest vector."""
    order = sorted(occ, key=lambda t: (-occ[t], type_str(t)))
    total, cum, k = sum(occ.values()), 0, 0
    for k, t in enumerate(order, 1):
        cum += occ[t]
        if cum * COVER_DEN >= COVER_NUM * total:
            break
    head = order[:k] if total else []
    dic = {t: min(pats[t].items(), key=lambda kv: (-kv[1], sum(kv[0]), tuple(int(x) for x in kv[0])))[0]
           for t in order}
    return {"order": order, "head": head, "dict": dic, "total": total,
            "c_head_A": (sum(occ[t] for t in head) / total) if total else None}


# ------------------------------------------------------------------------------------------------ §3.3 pin
def pin(toks: list[str], dic: dict, maxlen: int):
    """Scan the key sequence left to right, longest match first; at each occurrence of a listed type set boundaries
    at both ends and inside by the dictionary pattern. Characters are kept as written; only boundaries move.
    Returns (tokens, malformed flag); a malformed string is returned unchanged."""
    e = explode(toks)
    if e is None:
        return toks, True
    syl, b = e
    k = [syl_key(s) for s in syl]
    n, i = len(syl), 0
    while i < n:
        for ln in range(min(maxlen, n - i), 1, -1):
            pat = dic.get(tuple(k[i:i + ln]))
            if pat is not None:
                if i > 0:
                    b[i - 1] = True
                if i + ln < n:
                    b[i + ln - 1] = True
                b[i:i + ln - 1] = list(pat)
                i += ln
                break
        else:
            i += 1
    return rebuild(syl, b), False


class PinTok(FM.Tok):
    """FE-CERT's Tok, unchanged for 4-tuple members; a 5-tuple (U, T, P, C, tag) applies the pin of list `tag` to
    the member's tokens (outputs and references alike, through Tok.side)."""

    def __init__(self, seg=None, dicts=None):
        super().__init__(seg)
        self.dicts = {g: (d, max((len(t) for t in d), default=0)) for g, d in (dicts or {}).items()}
        self.malformed = Counter()

    def tokens(self, raw, m):
        if len(m) == 5:
            d, ml = self.dicts[m[4]]
            toks, bad = pin(super().tokens(raw, m[:4]), d, ml)
            self.malformed[m[4]] += bad
            return toks
        return super().tokens(raw, m)


def per_cider(tk, refs: dict, ids: list, texts: dict):
    """b_fecert.scorer restricted to CIDEr-D and token keys (same calls: Tok.side 'matched', E4.Cider with df from
    the references of ids, FM.key). G0 checks the result against DEV.json; the self-test against BF.scorer."""
    def per(m):
        R = {i: [tk.side(r, "matched", m, True) for r in refs[i]] for i in ids}
        cid = E4.Cider(R)
        out = {"_refs": FM.key(["\t".join(R[i]) for i in ids])}
        for f, t in texts.items():
            H = {i: tk.side(t[i], "matched", m, False) for i in ids}
            out[f] = {"cider": cid.per_image(H), "key": FM.key([H[i] for i in ids])}
        return out
    return per


# ------------------------------------------------------------------------------------------------ S1a: census
def st_s1a(a) -> int:
    reg_check()
    env = env_ok(a)
    work, out = Path(a.work), Path(a.out)
    ins = check_inputs(work, ("FAMILY.json", "CENSUS.json"))
    if jload(work / "FAMILY.json")["units_dropped"]:
        fault("an FE-CERT unit was dropped")
    refs, ids = load_refs_ids()
    half_a, _half_b = split(ids)
    strings = [r for i in half_a for r in refs[i]]  # half-A references only (§3.2; mutant M1/M8)
    tk = FM.Tok(SEG)
    tk.prime(strings, [RDR0, PYVI0])
    cz = census(strings, tk)
    pl = pin_lists(cz["occ"], cz["pats"])
    share = cz["unaligned"] / max(1, cz["strings"])
    floor = None
    if share > UNALIGNED_MAX:
        floor = "FAULT (ii): unaligned > 0.5%"
    elif len(pl["order"]) < MIN_TYPES:
        floor = "NOT_EVALUABLE (iii): fewer than 30 disagreement types"
    rec = {"registration": REG, "registration_sha256": REG_SHA, "stage": "s1a", "code_sha256": code_shas(),
           "inputs_sha256": {**ins, "test_data.json": REFS_SHA}, "env": env, "label": "DEVELOPMENT",
           "half_A_images": len(half_a), "strings": cz["strings"], "unaligned": cz["unaligned"],
           "unaligned_share": share, "types": len(pl["order"]), "occurrences": pl["total"],
           "head_size": len(pl["head"]), "c_head_A": pl["c_head_A"], "floor": floor,
           "head": [list(t) for t in pl["head"]],
           "dict": [[list(t), [int(x) for x in pl["dict"][t]], cz["occ"][t]] for t in pl["order"]]}
    out.mkdir(parents=True, exist_ok=True)
    print(f"STAGE s1a: CENSUS_ALT.json sha256 {write_once(out / 'CENSUS_ALT.json', rec)}")
    if floor:  # recorded and kept (a registered outcome); s1b refuses to run after it
        print(f"STAGE s1a: {floor}")
    return 0


def load_census(out: Path, want: str) -> dict:
    p = out / "CENSUS_ALT.json"
    need(p, want, "CENSUS_ALT.json (--census-sha)")
    cz = jload(p)
    if cz.get("floor"):
        raise SystemExit("REFUSED: the census tripped a floor; nothing runs after it")
    dic_all = {tuple(t): tuple(bool(x) for x in pat) for t, pat, _n in cz["dict"]}
    head = {tuple(t) for t in cz["head"]}
    return {"all": dic_all, "head": {t: dic_all[t] for t in head}}


# ------------------------------------------------------------------------------------------------ S1b: re-score
def count_disagreements(tk, strings: list[str], head: set, alltypes: set) -> list[int]:
    """[n_head, n_all, n_other, unaligned] over strings, at the census members (§3.4 c_ref^B / c_out^B)."""
    nh = na = no = un = 0
    for s in strings:
        d = disagreements(tk.tokens(s, RDR0), tk.tokens(s, PYVI0))
        if d is None:
            un += 1
            continue
        for t, _p in d:
            if t in alltypes:
                na += 1
                nh += t in head
            else:
                no += 1
    return [nh, na, no, un]


def st_s1b(a) -> None:
    reg_check()
    env = env_ok(a)
    work, out = Path(a.work), Path(a.out)
    cz = load_census(out, a.census_sha)
    ins = check_inputs(work, ("FAMILY.json", "CENSUS.json", "SYSTEMS.tsv"))
    refs, ids = load_refs_ids()
    texts = BF.ktvic_texts(work, Path(a.baselines))  # each file checked against SYSTEMS.tsv by sha256 (unchanged)
    if any(set(t) != set(ids) for t in texts.values()) or len(texts) != EXPECT_FILES:
        fault(f"{len(texts)} files, or a file does not cover the KTVIC test ids")
    files = list(texts)
    tk = PinTok(SEG, {"h": cz["head"], "a": cz["all"]})
    tk.prime([r for i in ids for r in refs[i]] + [t[i] for t in texts.values() for i in ids], RAW)
    per = per_cider(tk, refs, ids, texts)  # df from the references of all 558 images (§3.4, CC-510 N5)
    C = np.zeros((len(MEMS), len(files), len(ids)))
    K = np.empty((len(MEMS), len(files)), dtype="<U16")
    RK = np.empty(len(MEMS), dtype="<U16")
    for k, m in enumerate(MEMS):
        o = per(m)
        RK[k] = o["_refs"]
        for j, f in enumerate(files):
            C[k, j], K[k, j] = o[f]["cider"], o[f]["key"]
    head, alltypes = set(cz["head"]), set(cz["all"])
    cref = np.array([count_disagreements(tk, refs[i], head, alltypes) for i in ids])
    cout = np.array([count_disagreements(tk, [t[i] for t in texts.values()], head, alltypes) for i in ids])
    npz = out / "PER_IMAGE_ALT.npz"
    if npz.exists():
        raise SystemExit("REFUSED: PER_IMAGE_ALT.npz exists; a stage runs once")
    with open(npz, "wb") as fh:
        np.savez(fh, cider=C, keys=K, rkeys=RK, members=np.array(NAMES), files=np.array(files), ids=np.array(ids),
                 counts_ref=cref, counts_out=cout)
    os.chmod(npz, 0o444)
    rec = {"registration": REG, "registration_sha256": REG_SHA, "stage": "s1b", "code_sha256": code_shas(),
           "inputs_sha256": {**ins, "test_data.json": REFS_SHA, "CENSUS_ALT.json": a.census_sha}, "env": env,
           "members": len(MEMS), "files": len(files), "images": len(ids), "malformed_pinned_strings":
           dict(tk.malformed), "PER_IMAGE_ALT.npz": sha_file(npz), "label": "DEVELOPMENT"}
    print(f"STAGE s1b: PER_IMAGE_ALT.npz sha256 {rec['PER_IMAGE_ALT.npz']}")
    print(f"STAGE s1b: S1B.json sha256 {write_once(out / 'S1B.json', rec)}")


# ------------------------------------------------------------------------------------------------ matrix helpers
def load_matrix(path: Path, want: str) -> dict:
    need(path, want, "PER_IMAGE_ALT.npz (--npz-sha)")
    with np.load(path, allow_pickle=False) as z:
        M = {k: z[k] for k in z.files}
    if list(M["members"]) != NAMES:
        fault("member order of the matrix differs from MEMS")
    M["fidx"] = {str(f): j for j, f in enumerate(M["files"])}
    M["midx"] = {str(m): k for k, m in enumerate(M["members"])}
    return M


def pair_of(cid: str) -> tuple[str, str]:
    return cid[2:].split("|")[0], cid.split("|")[1]


def classes_of(M: dict, a: str, b: str, members, W, cols=None) -> dict:
    """One comparison with token-identity classes over `members` (class key = b_fecert.add_class form) and CIDEr-D
    statistics from b_fecert.stats unchanged, on image columns `cols` (None = all)."""
    ja, jb = M["fidx"][a], M["fidx"][b]
    c = {"id": f"D:{a}|{b}", "classes": {}}
    for m in members:
        k = M["midx"][m]
        key = f"{M['keys'][k, ja]}|{M['keys'][k, jb]}|{M['rkeys'][k]}"
        cl = c["classes"].setdefault(key, {"members": []})
        cl["members"].append(m)
        if "cider" not in cl:
            d = M["cider"][k, ja] - M["cider"][k, jb]
            cl["cider"] = BF.stats(d if cols is None else d[cols], W)
    return c


# ------------------------------------------------------------------------------------------------ G0
def g0_compare(dev_c: dict, got: dict) -> dict:
    """G_w classes of DEV.json (members restricted to G_w) against the matrix: same keys, same members, |diff| <=
    1e-6 on D, L, U, sd and the same sig."""
    want = {}
    for k, cl in dev_c["classes"].items():
        mm = [m for m in cl["members"] if m in G_W]
        if mm:
            want[k] = {"members": mm, "cider": cl["cider"]}
    r = {"key_mismatch": set(want) != set(got["classes"]), "member_mismatch": 0, "sig_mismatch": 0,
         "max_abs_diff": 0.0}
    for k in set(want) & set(got["classes"]):
        if sorted(want[k]["members"]) != sorted(got["classes"][k]["members"]):
            r["member_mismatch"] += 1
        r["sig_mismatch"] += BF.sig(want[k]["cider"]) != BF.sig(got["classes"][k]["cider"])
        r["max_abs_diff"] = max(r["max_abs_diff"], *(abs(x - y) for x, y in zip(want[k]["cider"],
                                                                                 got["classes"][k]["cider"])))
    return r


def g0_pass(rows: list[dict]) -> dict:
    s = {"comparisons": len(rows), "key_mismatch": sum(r["key_mismatch"] for r in rows),
         "member_mismatch": sum(r["member_mismatch"] for r in rows),
         "sig_mismatch": sum(r["sig_mismatch"] for r in rows),
         "max_abs_diff": max((r["max_abs_diff"] for r in rows), default=0.0)}
    s["pass"] = (len(rows) == EXPECT_D and s["key_mismatch"] == 0 and s["member_mismatch"] == 0
                 and s["sig_mismatch"] == 0 and s["max_abs_diff"] <= G0_TOL)
    return s


def st_g0(a) -> int:
    reg_check()
    work, out = Path(a.work), Path(a.out)
    ins = check_inputs(work, ("DEV.json",))
    M = load_matrix(out / "PER_IMAGE_ALT.npz", a.npz_sha)
    dev = jload(work / "DEV.json")
    W = BF.boot_W(M["cider"].shape[2])  # the FE-CERT draws on all 558 images (G0 only)
    rows = [g0_compare(c, classes_of(M, *pair_of(c["id"]), G_W, W)) for c in dev["comparisons"]]
    s = g0_pass(rows)
    rec = {"registration": REG, "registration_sha256": REG_SHA, "stage": "g0", "code_sha256": code_shas(),
           "inputs_sha256": ins, "PER_IMAGE_ALT.npz": a.npz_sha, "tolerance": G0_TOL, **s}
    print(f"STAGE g0: G0_ALT.json sha256 {write_once(out / 'G0_ALT.json', rec)}")
    if not s["pass"]:
        print("FAULT: G0 reproduction failed: stop, judge line, no ALT quantity")
        return 3
    return 0


# ------------------------------------------------------------------------------------------------ §3.4 estimands
def pairs_by_level() -> list[tuple[str, str, tuple]]:
    """(r_l, p_l, l) for the 18 level triples: the same T, P and C on both sides (mutant M3)."""
    return [(mname(("rdr",) + lv), mname(("pyvi",) + lv), lv) for lv in LEVELS]


def unit_vectors(M: dict, comps: list[tuple[str, str]], cols) -> dict:
    """Per-image sums over units (c, l) of sigma * shift, for raw, Pi_head-pinned and Pi_all-pinned members, with
    sigma = sign of the half-B mean raw shift, fixed (§3.4; mutant M4); plus the floor (iv) sums and DESCRIPTIVE
    splits. Linear in the per-image differences, so every draw is W_B @ vector / n."""
    ia = np.array([M["fidx"][a] for a, _b in comps])
    ib = np.array([M["fidx"][b] for _a, b in comps])
    n = len(cols)
    v = {k: np.zeros(n) for k in ("A", "Ah", "Aa", "A_tw", "Aa_tw", "A_tmf", "Aa_tmf")}
    s = {"abs_shift": 0.0, "abs_Dr": 0.0, "abs_pin_move_h": 0.0, "abs_pin_move_a": 0.0, "units": 0, "sigma_zero": 0}
    for r, p, lv in pairs_by_level():
        x = {}
        for tag, suf in (("", ""), ("h", "+Ph"), ("a", "+Pa")):
            Cr, Cp = M["cider"][M["midx"][r + suf]][:, cols], M["cider"][M["midx"][p + suf]][:, cols]
            x[tag] = (Cp[ia] - Cp[ib]) - (Cr[ia] - Cr[ib])  # delta per unit and image
            if tag:
                s[f"abs_pin_move_{tag}"] += float(np.abs((Cr[ia] - Cr[ib]).mean(1) - x["Dr"].mean(1)).sum())
            else:
                x["Dr"] = Cr[ia] - Cr[ib]
        sg = np.sign(x[""].mean(1))
        s["sigma_zero"] += int((sg == 0).sum())
        s["abs_shift"] += float(np.abs(x[""].mean(1)).sum())
        s["abs_Dr"] += float(np.abs(x["Dr"].mean(1)).sum())
        s["units"] += len(comps)
        a0, ah, aa = sg @ x[""], sg @ x["h"], sg @ x["a"]
        v["A"] += a0
        v["Ah"] += ah
        v["Aa"] += aa
        g = "tw" if lv[0] == "tw" else "tmf"
        v[f"A_{g}"] += a0
        v[f"Aa_{g}"] += aa
    return {"v": v, "s": s}


def draws(vec: np.ndarray, W: np.ndarray) -> np.ndarray:
    return W @ vec / W.shape[1]


def ratio_draws(num: np.ndarray, den: np.ndarray) -> tuple[np.ndarray, int]:
    with np.errstate(divide="ignore", invalid="ignore"):
        r = num / den
    return r, int((den == 0).sum())


def interval(x: np.ndarray) -> list[float]:
    lo, hi = np.percentile(x, [2.5, 97.5])
    return [float(lo), float(hi)]


def estimands(v: dict, cref: np.ndarray, cout: np.ndarray, W: np.ndarray) -> dict:
    """Point values (all weights 1) and per-draw values; c_ref^B and c_out^B recomputed in every draw from the
    image-level counts with the same W_B (mutant M10). cref, cout: [n_head, n_all] per half-B image."""
    one = np.ones((1, W.shape[1]))
    out, zero = {}, 0
    for nm, Wx in (("point", one), ("draws", W)):
        A, Ah, Aa = draws(v["A"], Wx), draws(v["Ah"], Wx), draws(v["Aa"], Wx)
        rh, z1 = ratio_draws(Ah, A)
        ra, z2 = ratio_draws(Aa, A)
        kap, z3 = ratio_draws(A - Ah, A - Aa)
        cr, z4 = ratio_draws(Wx @ cref[:, 0], Wx @ cref[:, 1])
        co, z5 = ratio_draws(Wx @ cout[:, 0], Wx @ cout[:, 1])
        rtw, z6 = ratio_draws(draws(v["Aa_tw"], Wx), draws(v["A_tw"], Wx))
        rtm, z7 = ratio_draws(draws(v["Aa_tmf"], Wx), draws(v["A_tmf"], Wx))
        if nm == "draws":
            zero = z1 + z2 + z3 + z4 + z5
        out[nm] = {"rho_head": 1 - rh, "rho_all": 1 - ra, "kappa_head": kap, "c_ref": cr, "c_out": co,
                   "d_lo": kap - np.minimum(cr, co), "d_hi": kap - np.maximum(cr, co),
                   "rho_all_tw": 1 - rtw, "rho_all_tm_tf": 1 - rtm}
    out["zero_denominator_draws"] = zero
    return out


# ------------------------------------------------------------------------------------------------ §4 rules
def hl1_label(d_lo: list[float], d_hi: list[float]) -> str:
    """H-L1 on kappa_head against the band [min, max] of c_ref^B and c_out^B (per draw)."""
    if d_lo[1] < 0:
        return "TAIL-WEIGHTED"
    if d_hi[0] > 0:
        return "HEAD-WEIGHTED"
    return "PROPORTIONAL"


def hl2_label(rho_head: list[float]) -> str:
    """H-L2 on rho_head against 0.50."""
    if rho_head[0] > PRACTICAL:
        return "PRACTICAL"
    if rho_head[1] < PRACTICAL:
        return "NOT PRACTICAL"
    return "INCONCLUSIVE"


def floors(s: dict, rho_all_iv: list[float], zero: int) -> str | None:
    """§4 floors (iv) then (v), after (i)-(iii) upstream; a zero denominator in any draw is NOT_EVALUABLE too."""
    if s["abs_shift"] < SHIFT_FLOOR * s["abs_Dr"]:
        return "NOT_EVALUABLE (iv): sum |delta| < 0.01 sum |D_r| on half B"
    if rho_all_iv[0] < RHO_ALL_FLOOR:
        return "NOT_EVALUABLE (v): L(rho_all) < 0.20"
    if zero:
        return f"NOT_EVALUABLE: zero denominator in {zero} draw(s)"
    return None


# ------------------------------------------------------------------------------------------------ DESCRIPTIVE
def fragile_rows(M: dict, comps: list[tuple[str, str]], cols, W) -> dict:
    """FRAGILE over G_w raw against Pi_head-pinned on half B; CHANGED against f0 and f0^Pi respectively."""
    out = {}
    for tag, suf in (("raw", ""), ("pinned_head", "+Ph")):
        names = [g + suf for g in G_W]
        f0 = BF.F0N + suf
        frag = changed = 0
        for a, b in comps:
            c = classes_of(M, a, b, names, W, cols)
            v = BF.certify(c, set(names))
            frag += bool(v["fragile"])
            s0 = next(BF.sig(cl["cider"]) for cl in c["classes"].values() if f0 in cl["members"])
            changed += s0 != 0 and v["certified"] != s0
        out[tag] = {"fragile": frag, "changed": changed, "comparisons": len(comps)}
    return out


# ------------------------------------------------------------------------------------------------ S2
def st_s2(a) -> None:
    reg_check()
    work, out = Path(a.work), Path(a.out)
    ins = check_inputs(work, ("DEV.json",))
    cz = load_census(out, a.census_sha)
    g0p = out / "G0_ALT.json"
    need(g0p, a.g0_sha, "G0_ALT.json (--g0-sha)")
    g0 = jload(g0p)
    if not g0.get("pass") or g0.get("PER_IMAGE_ALT.npz") != a.npz_sha:
        raise SystemExit("REFUSED: G0 did not pass, or it was run on another matrix")
    M = load_matrix(out / "PER_IMAGE_ALT.npz", a.npz_sha)
    ids = [str(i) for i in M["ids"]]
    half_a, half_b = split(ids)
    pos = {i: k for k, i in enumerate(ids)}
    cols = np.array([pos[i] for i in half_b])  # half B in the registered list order (perm[279:])
    dev = jload(work / "DEV.json")
    comps = [pair_of(c["id"]) for c in dev["comparisons"]]
    WB = BF.boot_W(len(cols), SEED_WB)
    u = unit_vectors(M, comps, cols)
    cref, cout = M["counts_ref"][cols][:, :2], M["counts_out"][cols][:, :2]
    e = estimands(u["v"], cref, cout, WB)
    p, d = e["point"], e["draws"]
    iv = {k: interval(d[k]) for k in ("rho_head", "rho_all", "kappa_head", "c_ref", "c_out", "d_lo", "d_hi",
                                      "rho_all_tw", "rho_all_tm_tf")}
    fl = floors(u["s"], iv["rho_all"], e["zero_denominator_draws"])
    rec = {"registration": REG, "registration_sha256": REG_SHA, "stage": "s2", "code_sha256": code_shas(),
           "inputs_sha256": {**ins, "CENSUS_ALT.json": a.census_sha, "PER_IMAGE_ALT.npz": a.npz_sha,
                             "G0_ALT.json": a.g0_sha},
           "label": "DEVELOPMENT; REGISTERED PREDICTION (H-L1, H-L2); every interval is nominal",
           "half_B_images": len(cols), "units": u["s"]["units"], "floor": fl,
           "H-L1": {"label": fl or hl1_label(iv["d_lo"], iv["d_hi"]), "kappa_head": float(p["kappa_head"][0]),
                    "kappa_head_95": iv["kappa_head"], "d_lo_95": iv["d_lo"], "d_hi_95": iv["d_hi"]},
           "H-L2": {"label": fl or hl2_label(iv["rho_head"]), "rho_head": float(p["rho_head"][0]),
                    "rho_head_95": iv["rho_head"]},
           "DESCRIPTIVE": {
               "rho_all": float(p["rho_all"][0]), "rho_all_95": iv["rho_all"],
               "c_ref_B": float(p["c_ref"][0]), "c_ref_B_95": iv["c_ref"],
               "c_out_B": float(p["c_out"][0]), "c_out_B_95": iv["c_out"],
               "rho_all_tw_pairs": float(p["rho_all_tw"][0]), "rho_all_tw_pairs_95": iv["rho_all_tw"],
               "rho_all_tm_tf_pairs": float(p["rho_all_tm_tf"][0]), "rho_all_tm_tf_pairs_95": iv["rho_all_tm_tf"],
               "output_only_occurrences_half_B": int(M["counts_out"][cols][:, 2].sum()),
               "output_occurrences_of_Pi_all_types_half_B": int(M["counts_out"][cols][:, 1].sum()),
               "unaligned_strings_half_B": {"references": int(M["counts_ref"][cols][:, 3].sum()),
                                            "outputs": int(M["counts_out"][cols][:, 3].sum())},
               "pin_moves_reference_member": {"head": u["s"]["abs_pin_move_h"] / u["s"]["abs_Dr"],
                                              "all": u["s"]["abs_pin_move_a"] / u["s"]["abs_Dr"]},
               "floor_iv": {"sum_abs_shift": u["s"]["abs_shift"], "sum_abs_D_r": u["s"]["abs_Dr"]},
               "sigma_zero_units": u["s"]["sigma_zero"], "zero_denominator_draws": e["zero_denominator_draws"],
               "head_size": len(cz["head"]), "types_all": len(cz["all"]),
               "fragile_over_G_w": fragile_rows(M, comps, cols, WB)}}
    print(f"STAGE s2: RESULT_ALT.json sha256 {write_once(out / 'RESULT_ALT.json', rec)}")


# ------------------------------------------------------------------------------------------------ main
def main(argv=None) -> int:
    ap = argparse.ArgumentParser(description=__doc__.split("\n")[0])
    ap.add_argument("stage", choices=["s1a", "s1b", "g0", "s2"])
    for o in ("--work", "--out", "--baselines", "--pyvi-wheel", "--uts-wheel", "--census-sha", "--npz-sha",
              "--g0-sha"):
        ap.add_argument(o)
    a = ap.parse_args(argv)
    try:
        if a.stage == "s1a":
            return st_s1a(a)
        if a.stage == "s1b":
            st_s1b(a)
        elif a.stage == "g0":
            return st_g0(a)
        else:
            st_s2(a)
    except BF.Fault as e:
        print(f"FAULT: {e}")
        return 3
    except SystemExit:
        raise
    except Exception as e:  # noqa: BLE001  the type only, so no caption text can echo
        print(f"ERROR: {type(e).__name__}")
        return 4
    return 0


if __name__ == "__main__":
    sys.exit(main())
