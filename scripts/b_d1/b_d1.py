#!/usr/bin/env python3
"""B-D1/A3 (Paper B, LRE): FE-CERT against Lu et al.'s readings and a reference-member margin (H1, H2), tone placement
beyond a scorer-and-tokenizer grid (H3), and the null level of the per-member test (A3).

Registration: manuscript/prereg/2026-11-27_b_d1/PREREG_DRAFT_B_D1_A3_v3.md (sha256 bf3a55f7...; CC-505, CC-505r2;
commit adebac7). The FE-CERT code (scripts/b_fecert/b_fecert.py and every repository module it imports) is reused
unchanged. Each of those files is checked against its sha256 before it is imported (PINS), and the set of loaded
repository modules must equal PINS (closure check).

Stages, run on a rented host only, each under run_stage.sh (CPU accounting and the 8 CPU-h hard stop):
  s1      re-score the stored output files (no decoding): per-image CIDEr-D under the 54 F_dev and 18 uts members
          -> PER_IMAGE_D1.npz (aggregate scores and token-identity hashes only) and S1.json (environment and shas)
  g0      reproduction gate against DEV.json and RESULT.json -> G0.json (counts and differences only)
  s2      H1, H2, H3, A3 -> RESULT_D1.json (counts, rates, p-values, bounds and labels only)
  budget  prints the CPU seconds left of 28,800, or exits 5 (STOP)

  NCS_DATA=D python -I -B scripts/b_d1/b_d1.py s1 --work W --out O --baselines B --pyvi-wheel P --uts-wheel U
  NCS_DATA=D python -I -B scripts/b_d1/b_d1.py g0 --work W --out O --npz-sha <PER_IMAGE_D1.npz sha256>
  NCS_DATA=D python -I -B scripts/b_d1/b_d1.py s2 --work W --out O --npz-sha <...> --g0-sha <G0.json sha256>
  python -I -B scripts/b_d1/b_d1.py budget --records R

No caption or reference text is written or printed. An unexpected exception prints its type only.
"""
from __future__ import annotations

import argparse
import hashlib
import json
import os
import re
import sys
from pathlib import Path

import numpy as np
from scipy.stats import beta, binomtest

HERE = Path(__file__).resolve().parent
ROOT = HERE.parents[1]

# ------------------------------------------------------------------------------------------------ pins (CC-505r2 K6)
PINS = {  # every repository file loaded by `import b_fecert`, plus pair.html (read by pair_server, never at import)
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
}
REG = "manuscript/prereg/2026-11-27_b_d1/PREREG_DRAFT_B_D1_A3_v3.md"
REG_SHA = "bf3a55f7641cc91b7ba99b5e4ef9d8623d857a2b594bfb7471636f9cf9f939e9"


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
import b_fecert as BF  # noqa: E402  reused unchanged (prereg v3 §3)
import family as FM  # noqa: E402
import ptb_protocol as PT  # noqa: E402



def closure_check() -> None:
    """Every repository module loaded so far is in PINS (the new code in scripts/b_d1/ excepted)."""
    loaded = set()
    for m in list(sys.modules.values()):
        f = getattr(m, "__file__", None)
        if f and str(Path(f).resolve()).startswith(str(ROOT) + os.sep) and Path(f).resolve().parent != HERE:
            loaded.add(str(Path(f).resolve().relative_to(ROOT)))
    extra = sorted(loaded - set(PINS))
    if extra:
        raise SystemExit(f"FAULT: repository module(s) loaded but not pinned: {', '.join(extra)}")


closure_check()

# ------------------------------------------------------------------------------------------------ registered values
INPUT_SHA = {  # prereg v3 §0; COMPUTE_B_D1_v2.md
    "DEV.json": "88ff39aa9552b671a0e439aec961d0fefe02df1f52a2a5df9765a9d8226f7e8d",
    "RESULT.json": "25614b469cf59dc61f15e839b89a8e78ca0b316905afc4bd2ae52eaa0d32b43a",
    "FAMILY.json": "431d92a4a2eaf0516446c9f9aef453ee52d311b6e329d97cd1abb4c4e8017f77",
    "CENSUS.json": "2252167b435890c5dbf70a97e0fc918bc6989c48acda636427d4dd2889599afa",
    "SYSTEMS.tsv": "30ac9555cd6cdc8fd50f47e637e734fac564c692605f590ba213a60a3be6e1a0",
}
REFS_SHA = "cc22ec6a8883773cb23c87ad5b64925f5a53c21982117274b53621f454e7ebbf"
EXPECT_FILES, EXPECT_IMAGES, EXPECT_D = 75, 558, 1101
G0_TOL = 1e-6  # §6 G0
N_FLOOR, ALPHA = 10, 0.05  # §5 H1/H2: n < 10 NOT_EVALUABLE; Holm at 0.05 over four one-sided exact p-values
SEED_A3, N_NULL = 20261127, 1000  # §5 A3
A3_CP, A3_NOM, A3_UP = 0.025, 0.025, 0.040  # one-sided 97.5% CP per direction; nominal 2.5%; pass bar 0.040
CPU_BUDGET = 28_800  # COMPUTE_B_D1_v2.md: hard stop at 8 CPU-h
METRICS = ("cider", "bleu", "rouge")  # §5 H3: CIDEr-D, BLEU-4, ROUGE-L
SEG = None  # the self-test injects stub units here (None = the real units of family.py)


def names(units, t=None) -> list[str]:
    return [FM.name(m) for m in FM.members(units) if t is None or m[1] == t]


F_DEV = names(FM.DEV_UNITS)  # 54
F_UTS = names(("uts",))  # 18
F_ALL = F_DEV + F_UTS  # 72, dev members first so that a mixed class is built as in FE-CERT stage 2b
FOLDS = {  # §4: fold u -> (certifying family G_u, breaking family H_u); rdr stays in every G_u (f0 is an rdr member)
    "syl": (names(("rdr", "pyvi")), names(("syl",))),
    "pyvi": (names(("syl", "rdr")), names(("pyvi",))),
    "uts": (names(("syl", "rdr", "pyvi")), names(("uts",))),
}
G_CONTRACT = names(("syl", "rdr", "pyvi"), "tw")  # §5 H3: U x P x C at T = tw (18 members; x 3 scorers)
G_CAPTION = names(("syl", "rdr", "pyvi"))  # all 54 F_dev members (x 3 scorers): adds only tm and tf
G_SYL = names(("syl",), "tw")  # DESCRIPTIVE: the v1 estimand's grid (U = syl, T = tw)


def fault(msg: str):
    raise BF.Fault(msg)


def jload(p):
    return json.loads(Path(p).read_text(encoding="utf-8"))


def check_inputs(work: Path, fnames) -> dict:
    out = {}
    for f in fnames:
        p = work / f
        if not p.is_file() or sha_file(p) != INPUT_SHA[f]:
            fault(f"{f} is missing or differs from its registered sha256")
        out[f] = INPUT_SHA[f]
    return out


def reg_check() -> None:
    p = ROOT / REG
    if not p.is_file() or sha_file(p) != REG_SHA:
        fault("the registration file is missing or differs from bf3a55f7 (prereg v3)")


def write_once(path: Path, obj) -> str:
    if path.exists():
        raise SystemExit(f"REFUSED: {path.name} exists; a stage runs once")
    path.write_text(json.dumps(obj, indent=1, ensure_ascii=False, default=float) + "\n", encoding="utf-8")
    os.chmod(path, 0o444)
    return sha_file(path)


def code_shas() -> dict:
    files = [Path(__file__).resolve()] + [ROOT / r for r in PINS]
    return {str(p.relative_to(ROOT)): sha_file(p) for p in files}


# ------------------------------------------------------------------------------------------------ S1: re-score
def st_s1(a) -> None:
    reg_check()
    env = BF.env_record(a)
    BF.env_check(env)
    work, out = Path(a.work), Path(a.out)
    ins = check_inputs(work, ("FAMILY.json", "CENSUS.json", "SYSTEMS.tsv"))
    if jload(work / "FAMILY.json")["units_dropped"] or jload(work / "CENSUS.json")["uts_moved_to_dev"]:
        fault("FE-CERT units differ from F_dev = syl, rdr, pyvi and F_held = uts")
    if sha_file(BF.REFS) != REFS_SHA:
        fault("test_data.json differs from its registered sha256")
    refs = PT.load_refs(BF.REFS)
    ids = sorted(refs)
    texts = BF.ktvic_texts(work, Path(a.baselines))  # each file checked against SYSTEMS.tsv by sha256 (unchanged)
    if any(set(t) != set(ids) for t in texts.values()):
        fault("an output file does not cover the KTVIC test ids")
    if (len(texts), len(ids)) != (EXPECT_FILES, EXPECT_IMAGES):
        fault(f"{len(texts)} files on {len(ids)} images, not {EXPECT_FILES} on {EXPECT_IMAGES}")
    files = list(texts)
    mems = FM.members(FM.DEV_UNITS) + FM.members(("uts",))  # the order of F_ALL
    tk = FM.Tok(SEG)
    tk.prime([r for i in ids for r in refs[i]] + [t[i] for t in texts.values() for i in ids], mems)
    per = BF.scorer(tk, refs, ids, texts)  # unchanged: matched member on outputs and references, df from references
    C = np.zeros((len(mems), len(files), len(ids)))
    K = np.empty((len(mems), len(files)), dtype="<U16")
    RK = np.empty(len(mems), dtype="<U16")
    for k, m in enumerate(mems):
        o = per(m)
        RK[k] = o["_refs"]
        for j, f in enumerate(files):
            C[k, j], K[k, j] = o[f]["cider"], o[f]["key"]
    out.mkdir(parents=True, exist_ok=True)
    npz = out / "PER_IMAGE_D1.npz"
    if npz.exists():
        raise SystemExit("REFUSED: PER_IMAGE_D1.npz exists; a stage runs once")
    with open(npz, "wb") as fh:
        np.savez(fh, cider=C, keys=K, rkeys=RK, members=np.array(F_ALL), files=np.array(files),
                 ids_sha256=np.array(hashlib.sha256("\n".join(ids).encode()).hexdigest()))
    os.chmod(npz, 0o444)
    rec = {"registration": REG, "registration_sha256": REG_SHA, "stage": "s1", "code_sha256": code_shas(),
           "inputs_sha256": {**ins, "test_data.json": REFS_SHA}, "env": env, "members": len(mems), "files": len(files),
           "images": len(ids), "PER_IMAGE_D1.npz": sha_file(npz), "label": "DEVELOPMENT"}
    print(f"STAGE s1: PER_IMAGE_D1.npz sha256 {rec['PER_IMAGE_D1.npz']}")
    print(f"STAGE s1: S1.json sha256 {write_once(out / 'S1.json', rec)}")


# ------------------------------------------------------------------------------------------------ matrix -> classes
def load_matrix(path: Path, want: str) -> dict:
    if not path.is_file() or sha_file(path) != want:
        raise SystemExit("REFUSED: PER_IMAGE_D1.npz is not the file whose sha256 was passed (--npz-sha)")
    with np.load(path, allow_pickle=False) as z:
        M = {k: z[k] for k in z.files}
    if list(M["members"]) != F_ALL:
        fault("member order of the matrix differs from F_ALL")
    M["fidx"] = {str(f): j for j, f in enumerate(M["files"])}
    M["midx"] = {str(m): k for k, m in enumerate(M["members"])}
    return M


def pair_of(cid: str) -> tuple[str, str]:
    """'D:a|b' -> (a, b), as b_fecert.ktvic_comps parses it."""
    return cid[2:].split("|")[0], cid.split("|")[1]


def diffs(M: dict, a: str, b: str, members) -> list[tuple[str, str, np.ndarray]]:
    """(class key, member, per-image difference a - b) per member; key = b_fecert.add_class form."""
    ja, jb = M["fidx"][a], M["fidx"][b]
    out = []
    for m in members:
        k = M["midx"][m]
        out.append((f"{M['keys'][k, ja]}|{M['keys'][k, jb]}|{M['rkeys'][k]}", m, M["cider"][k, ja] - M["cider"][k, jb]))
    return out


def build(M: dict, cid: str, W, members=F_ALL, sign=None) -> dict:
    """One comparison with its classes (token identity; members in the order given), CIDEr-D statistics per class
    from b_fecert.stats unchanged. sign: the A3 swap vector, applied to every member alike."""
    a, b = pair_of(cid)
    c = {"id": cid, "a": a, "b": b, "classes": {}}
    for key, m, d in diffs(M, a, b, members):
        cl = c["classes"].setdefault(key, {"members": []})
        cl["members"].append(m)
        if "cider" not in cl:
            cl["cider"] = BF.stats(d if sign is None else sign * d, W)
    return c


def f0_stats(c: dict) -> list:
    return next(cl["cider"] for cl in c["classes"].values() if BF.F0N in cl["members"])


# ------------------------------------------------------------------------------------------------ G0
def g0_compare(dev_c: dict, got: dict, res_row: dict) -> dict:
    """§6 G0 (a) F_dev classes: same key set, same sorted members, |stat diff| <= 1e-6 on D, L, U, sd_boot, and the
    same sig as in DEV.json (CC-506 W2: the folds syl and pyvi are registered on DEV.json, §4);
    (b) the verdict over F (72) equals RESULT.json F, and D_f0 equals the stored D_f0."""
    dev_got = {}
    for k, cl in got["classes"].items():
        mm = [m for m in cl["members"] if m in F_DEV]
        if mm:
            dev_got[k] = {"members": mm, "cider": cl["cider"]}
    r = {"key_mismatch": set(dev_got) != set(dev_c["classes"]), "member_mismatch": 0, "sig_mismatch": 0,
         "max_abs_diff": 0.0}
    for k in set(dev_got) & set(dev_c["classes"]):
        if sorted(dev_got[k]["members"]) != sorted(dev_c["classes"][k]["members"]):
            r["member_mismatch"] += 1
        r["sig_mismatch"] += BF.sig(dev_got[k]["cider"]) != BF.sig(dev_c["classes"][k]["cider"])
        r["max_abs_diff"] = max(r["max_abs_diff"], *(abs(x - y) for x, y in zip(dev_got[k]["cider"],
                                                                                 dev_c["classes"][k]["cider"])))
    r["verdict_mismatch"] = BF.certify(got, set(F_ALL))["verdict"] != res_row["F"]
    r["df0_diff"] = abs(f0_stats(got)[0] - res_row["D_f0"])
    return r


def g0_pass(rows: list[dict]) -> dict:
    s = {"comparisons": len(rows), "key_mismatch": sum(r["key_mismatch"] for r in rows),
         "member_mismatch": sum(r["member_mismatch"] for r in rows),
         "sig_mismatch": sum(r["sig_mismatch"] for r in rows),
         "max_abs_diff": max((r["max_abs_diff"] for r in rows), default=0.0),
         "verdict_mismatch": sum(r["verdict_mismatch"] for r in rows),
         "max_df0_diff": max((r["df0_diff"] for r in rows), default=0.0)}
    s["pass"] = (s["key_mismatch"] == 0 and s["member_mismatch"] == 0 and s["sig_mismatch"] == 0
                 and s["max_abs_diff"] <= G0_TOL
                 and s["verdict_mismatch"] == 0 and s["max_df0_diff"] <= G0_TOL)
    return s


def st_g0(a) -> int:
    reg_check()
    work, out = Path(a.work), Path(a.out)
    ins = check_inputs(work, ("DEV.json", "RESULT.json"))
    M = load_matrix(out / "PER_IMAGE_D1.npz", a.npz_sha)
    dev, res = jload(work / "DEV.json"), jload(work / "RESULT.json")
    rr = {r["id"]: r for r in res["comparisons"] if r["set"] == "D"}
    if len(dev["comparisons"]) != EXPECT_D or set(rr) != {c["id"] for c in dev["comparisons"]}:
        fault("DEV.json and RESULT.json do not hold the same D comparisons")
    W = BF.boot_W(M["cider"].shape[2])
    rows = [g0_compare(c, build(M, c["id"], W), rr[c["id"]]) for c in dev["comparisons"]]
    s = g0_pass(rows)
    rec = {"registration": REG, "registration_sha256": REG_SHA, "stage": "g0", "code_sha256": code_shas(),
           "inputs_sha256": ins, "PER_IMAGE_D1.npz": a.npz_sha, "tolerance": G0_TOL, **s}
    print(f"STAGE g0: G0.json sha256 {write_once(out / 'G0.json', rec)}")
    if not s["pass"]:
        print("FAULT: G0 reproduction failed: stop, judge line, no D1 quantity")
        return 3
    return 0


# ------------------------------------------------------------------------------------------------ M1' union-of-ties
def union_of_ties(c: dict, G) -> tuple[int, bool]:
    """Lu et al. p.14, contract = member of G with its own CI; tied when the CI contains or touches 0. An ordering is
    claimed only when no contract is tied; every contract significant in mixed directions -> no ordering (the
    registration's convention). Returns (direction or 0, mixed)."""
    G = set(G)
    sg = [BF.sig(cl["cider"]) for cl in c["classes"].values() for m in cl["members"] if m in G]
    if not sg or 0 in sg:
        return 0, False
    if all(s == sg[0] for s in sg):
        return sg[0], False
    return 0, True


def identity_check(comps: list[dict], G) -> dict:
    """§3 M1 = M1' METHOD CHECK on every comparison; a difference is a FAULT."""
    Gs = set(G)
    diff = sum(union_of_ties(c, G)[0] != BF.certify(c, Gs)["certified"] for c in comps)
    if diff:
        fault(f"M1 != M1' on {diff} comparison(s)")
    return {"comparisons": len(comps), "equal": len(comps), "mixed_all_significant": sum(union_of_ties(c, G)[1]
                                                                                         for c in comps)}


# ------------------------------------------------------------------------------------------------ claims (§3)
def claims_fe(comps: list[dict], G) -> dict:
    """M1: {id: (direction, z_min)} for comparisons CERTIFIED over G."""
    out = {}
    for c in comps:
        v = BF.certify(c, set(G))
        if v and v["certified"]:
            out[c["id"]] = (v["certified"], v["z_min"])
    return out


def claims_f0(comps: list[dict]) -> dict:
    """M3/M4 candidates: sig under f0 != 0; direction sign(D_f0); margin z_f0."""
    out = {}
    for c in comps:
        s = f0_stats(c)
        if BF.sig(s) != 0:
            out[c["id"]] = (int(np.sign(s[0])), BF.zval(s))
    return out


def sigma(M: dict) -> np.ndarray:
    """AER z_c scale: SD (ddof 1) over all files of corpus CIDEr-D under each member, full sample, held fixed across
    resamples (the registration's own convention; Lu et al. do not state theirs)."""
    return M["cider"].mean(axis=2).std(axis=1, ddof=1)


def aer_stats(M: dict, cid: str, G, sig_c: np.ndarray, W, per_class: bool = False) -> list:
    """M2: e_i = mean over members c of G of d_{i,c} / sigma_c (equal weight per member); per_class: mean over the
    token-identity classes of G of the class's mean of d/sigma (DESCRIPTIVE)."""
    a, b = pair_of(cid)
    groups: dict = {}
    for key, m, d in diffs(M, a, b, G):
        groups.setdefault(key, []).append(d / sig_c[M["midx"][m]])
    terms = [x for g in groups.values() for x in g] if not per_class else [np.mean(g, axis=0) for g in groups.values()]
    return BF.stats(np.mean(terms, axis=0), W)


def claims_aer(M: dict, comps: list[dict], G, sig_c, W, per_class: bool = False) -> dict:
    if np.any(sig_c[[M["midx"][m] for m in G]] <= 1e-9):
        fault("a member of G has sigma_c <= 1e-9 over the files: the AER z-scale is undefined")
    out = {}
    for c in comps:
        s = aer_stats(M, c["id"], G, sig_c, W, per_class)
        if BF.sig(s) != 0:
            out[c["id"]] = (BF.sig(s), BF.zval(s))
    return out


def top_k(cl: dict, k: int) -> dict:
    """Size matching: the top k by the method's own margin, ties by comparison id ascending -> {id: direction}."""
    return {i: d for i, (d, _z) in sorted(cl.items(), key=lambda kv: (-kv[1][1], kv[0]))[:k]}


def discordant(A: dict, B: dict, byid: dict, H) -> tuple[int, int]:
    """Breaks among claims of A only and of B only; a claim is (id, direction); shared claims break alike."""
    sa, sb = set(A.items()), set(B.items())
    Hs = set(H)
    ba = sum(BF.held_break(byid[i], s, Hs)[0] for i, s in sa - sb)
    bb = sum(BF.held_break(byid[i], s, Hs)[0] for i, s in sb - sa)
    return ba, bb


def p_greater(k: int, n: int) -> float:
    """One-sided exact binomial P(X >= k | n, 1/2); n = 0 -> 1.0."""
    return 1.0 if n == 0 else float(binomtest(k, n, 0.5, alternative="greater").pvalue)


def contrast_label(n: int, rej_fe: bool, rej_x: bool, x: str) -> str:
    """§5 H1/H2 label order: n < 10 first, then FE fewer breaks, then X fewer, else NOT SUPPORTED."""
    if n < N_FLOOR:
        return "NOT_EVALUABLE"
    if rej_fe:
        return "SUPPORTED"
    if rej_x:
        return f"{x} BETTER"
    return "NOT SUPPORTED"


def h1_h2(M: dict, comps: list[dict], W) -> dict:
    byid = {c["id"]: c for c in comps}
    sig_c = sigma(M)
    f0 = claims_f0(comps)
    pool = {"H1": [0, 0], "H2": [0, 0]}  # [b_FE, b_X]
    folds, desc = {}, {}
    for u, (G, H) in FOLDS.items():
        fe = claims_fe(comps, G)
        aer = claims_aer(M, comps, G, sig_c, W)
        aer_cls = claims_aer(M, comps, G, sig_c, W, per_class=True)
        k1 = min(len(fe), len(f0))
        k2 = min(len(fe), len(aer))
        b1 = discordant(top_k(fe, k1), top_k(f0, k1), byid, H)
        b2 = discordant(top_k(fe, k2), top_k(aer, k2), byid, H)
        for h, b in (("H1", b1), ("H2", b2)):
            pool[h][0] += b[0]
            pool[h][1] += b[1]
        folds[u] = {"G_members": len(G), "H_members": len(H), "K_H1": k1, "K_H2": k2,
                    "H1_b_FE": b1[0], "H1_b_MG": b1[1], "H2_b_FE": b2[0], "H2_b_AER": b2[1]}
        desc[u] = h2_descriptive(comps, byid, G, H, {"FE": fe, "AER": aer, "AER_per_class": aer_cls, "f0": f0})
    p = {"H1_FE_fewer": p_greater(pool["H1"][1], sum(pool["H1"])), "H1_MG_fewer": p_greater(pool["H1"][0], sum(pool["H1"])),
         "H2_FE_fewer": p_greater(pool["H2"][1], sum(pool["H2"])), "H2_AER_fewer": p_greater(pool["H2"][0], sum(pool["H2"]))}
    rej = BF.holm(p, ALPHA)
    out = {"p_one_sided_exact_nominal": p, "holm_reject_at_0.05": rej, "folds": folds, "H2_descriptive": desc}
    for h, x in (("H1", "MG"), ("H2", "AER")):
        n = sum(pool[h])
        out[h] = {"b_FE": pool[h][0], f"b_{x}": pool[h][1], "n": n,
                  "label": contrast_label(n, rej[f"{h}_FE_fewer"], rej[f"{h}_{x}_fewer"], "MARGIN" if x == "MG" else x)}
    return out


def h2_descriptive(comps, byid, G, H, methods: dict) -> dict:
    """Native size per method: claims; held-out flip coverage and the false-tie analogue (§5 H2); flip incidence."""
    Hs = set(H)
    sig0 = {c["id"]: int(np.sign(f0_stats(c)[0])) for c in comps if BF.sig(f0_stats(c)) != 0}
    flips = {i for i, s in sig0.items() if BF.held_break(byid[i], s, Hs)[0]}
    stable = set(sig0) - flips
    frag = sum(BF.certify(c, set(G))["fragile"] for c in comps)
    row = {"units_sig_f0": len(sig0), "flip_units": len(flips),
           "flip_incidence_fragile_over_G": {"fragile": frag, "comparisons": len(comps), "share": frag / len(comps)}}
    for name, cl in methods.items():
        row[name] = {"claims": len(cl), "coverage": (sum(i not in cl for i in flips) / len(flips)) if flips else None,
                     "false_tie_analogue": (sum(i not in cl for i in stable) / len(stable)) if stable else None}
    return row


# ------------------------------------------------------------------------------------------------ H3 (from DEV.json)
def member_class(c: dict) -> dict:
    return {m: cl for cl in c["classes"].values() for m in cl["members"]}


def grid_verdict(mc: dict, members, metrics=METRICS) -> int:
    """Union-of-ties over contracts (metric, member): +1/-1 when every contract is significant that way, else 0."""
    sg = [BF.sig(mc[m][met]) for m in members for met in metrics]
    return sg[0] if sg and all(s == sg[0] and s != 0 for s in sg) else 0


def h3_label(k: int, n: int) -> str:
    """§5 H3 order: NOT_EVALUABLE (n < 59) -> SUPPORTED (lower > 0.05) -> NULL (upper <= 0.05) -> INCONCLUSIVE;
    one-sided 95% Clopper-Pearson, the FE-CERT v1.1 constants N_MIN and R_MAX."""
    if n < BF.N_MIN:
        return "NOT_EVALUABLE"
    if BF.cp_lower(k, n) > BF.R_MAX:
        return "SUPPORTED"
    if BF.cp_upper(k, n) <= BF.R_MAX:
        return "NULL"
    return "INCONCLUSIVE"


def h3(dev_comps: list[dict]) -> dict:
    n = k_t = n_syl = k_u = k_tu = 0
    split = {"syl": 0, "rdr": 0, "pyvi": 0}
    added = [m for m in G_CAPTION if m not in G_CONTRACT]
    for c in dev_comps:
        mc = member_class(c)
        s = grid_verdict(mc, G_CONTRACT)
        if s:
            n += 1
            if grid_verdict(mc, G_CAPTION) != s:
                k_t += 1
                for u in {m.split(".")[0] for m in added if any(BF.sig(mc[m][met]) != s for met in METRICS)}:
                    split[u] += 1
        s_syl = grid_verdict(mc, G_SYL)
        if s_syl:
            n_syl += 1
            k_u += grid_verdict(mc, G_CONTRACT) != s_syl
            k_tu += grid_verdict(mc, G_CAPTION) != s_syl
    return {"n": n, "k_T": k_t, "cp_lower_95": BF.cp_lower(k_t, n) if n else None,
            "cp_upper_95": BF.cp_upper(k_t, n) if n else None, "label": h3_label(k_t, n),
            "k_T_by_unit_of_breaking_class": split,
            "DESCRIPTIVE": {"n_syl_grid": n_syl, "k_U": k_u, "k_TU": k_tu}}


# ------------------------------------------------------------------------------------------------ A3
def cp97(k: int, n: int) -> tuple[float, float]:
    """One-sided 97.5% Clopper-Pearson (lower, upper)."""
    lo = 0.0 if k <= 0 else float(beta.ppf(A3_CP, k, n - k + 1))
    up = 1.0 if k >= n else float(beta.ppf(1 - A3_CP, k + 1, n - k))
    return lo, up


def a3_label(k_pos: int, k_neg: int, n: int) -> str:
    """§5 A3 rule on r_f0 per direction: both upper <= 0.040 -> AT OR BELOW NOMINAL; either lower > 0.025 ->
    ABOVE NOMINAL; otherwise INCONCLUSIVE."""
    bounds = [cp97(k, n) for k in (k_pos, k_neg)]
    if all(up <= A3_UP for _lo, up in bounds):
        return "AT OR BELOW NOMINAL"
    if any(lo > A3_NOM for lo, _up in bounds):
        return "ABOVE NOMINAL"
    return "INCONCLUSIVE"


def a3_draws(n_comps: int, n_img: int):
    """1,000 comparisons of D (DEV.json order) without replacement (seed 20261127); for draw j the swap vector is
    integers(0, 2) * 2 - 1 from default_rng(20261127 + j)."""
    pick = np.random.default_rng(SEED_A3).choice(n_comps, N_NULL, replace=False)
    return [(int(ci), np.random.default_rng(SEED_A3 + j).integers(0, 2, n_img) * 2 - 1) for j, ci in enumerate(pick)]


def a3(M: dict, comps: list[dict], W) -> dict:
    n_img = M["cider"].shape[2]
    cnt = {"f0": [0, 0], "A3_F_dev": [0, 0], "A3_F": [0, 0]}
    per_member = {m: [0, 0] for m in F_ALL}
    for ci, sg in a3_draws(len(comps), n_img):
        c = build(M, comps[ci]["id"], W, sign=sg)
        s0 = BF.sig(f0_stats(c))
        for key, v in (("f0", s0), ("A3_F_dev", BF.certify(c, set(F_DEV))["certified"]),
                       ("A3_F", BF.certify(c, set(F_ALL))["certified"])):
            if v:
                cnt[key][0 if v > 0 else 1] += 1
        for cl in c["classes"].values():
            s = BF.sig(cl["cider"])
            if s:
                for m in cl["members"]:
                    per_member[m][0 if s > 0 else 1] += 1
    return a3_summary(cnt, per_member, N_NULL)


def a3_summary(cnt: dict, per_member: dict, n: int) -> dict:
    """The label is the registered rule on r_f0 (per direction); r_A3 over F_dev and over F are printed beside it."""
    out = {"nulls": n, "label": a3_label(cnt["f0"][0], cnt["f0"][1], n)}
    for key, (kp, kn) in cnt.items():
        out[key] = {"pos": kp, "neg": kn, "r_pos": kp / n, "r_neg": kn / n,
                    "cp97_pos": cp97(kp, n), "cp97_neg": cp97(kn, n)}
    out["max_member_rate_F_dev_DESCRIPTIVE"] = {"pos": max(per_member[m][0] for m in F_DEV) / n,
                                                "neg": max(per_member[m][1] for m in F_DEV) / n}  # §5 A3: 54 members
    return out


# ------------------------------------------------------------------------------------------------ S2
def st_s2(a) -> None:
    reg_check()
    work, out = Path(a.work), Path(a.out)
    ins = check_inputs(work, ("DEV.json",))
    g0p = out / "G0.json"
    if not g0p.is_file() or sha_file(g0p) != a.g0_sha:
        raise SystemExit("REFUSED: G0.json is not the file whose sha256 was passed (--g0-sha)")
    g0 = jload(g0p)
    if not g0.get("pass") or g0.get("PER_IMAGE_D1.npz") != a.npz_sha:
        raise SystemExit("REFUSED: G0 did not pass, or it was run on another matrix")
    M = load_matrix(out / "PER_IMAGE_D1.npz", a.npz_sha)
    dev = jload(work / "DEV.json")
    W = BF.boot_W(M["cider"].shape[2])
    comps = [build(M, c["id"], W) for c in dev["comparisons"]]
    rec = {"registration": REG, "registration_sha256": REG_SHA, "stage": "s2", "code_sha256": code_shas(),
           "inputs_sha256": {**ins, "PER_IMAGE_D1.npz": a.npz_sha, "G0.json": a.g0_sha},
           "label": "DEVELOPMENT; REGISTERED PREDICTION (H1, H2, H3, A3); every p-value and bound is nominal",
           "identity_M1_M1prime_F_dev": identity_check(comps, F_DEV)}
    rec.update(h1_h2(M, comps, W))
    rec["H3"] = h3(dev["comparisons"])
    rec["A3"] = a3(M, comps, W)
    print(f"STAGE s2: RESULT_D1.json sha256 {write_once(out / 'RESULT_D1.json', rec)}")


# ------------------------------------------------------------------------------------------------ CPU budget
TIME_RE = re.compile(r"^\s*(User|System) time \(seconds\):\s*([0-9.]+)\s*$", re.M)


def cpu_used(records: Path) -> float:
    """User + system seconds over every GNU `time -v` record (*.time) in the records dir."""
    return sum(float(v) for p in sorted(records.glob("*.time")) for _k, v in TIME_RE.findall(p.read_text()))


def budget(records: Path) -> int:
    """Seconds left of 28,800; 0 when the budget is spent or a STOP marker exists (the caller then stops)."""
    if (records / "STOP").exists():
        return 0
    return max(0, int(CPU_BUDGET - cpu_used(records)))


# ------------------------------------------------------------------------------------------------ main
def main(argv=None) -> int:
    ap = argparse.ArgumentParser(description=__doc__.split("\n")[0])
    ap.add_argument("stage", choices=["s1", "g0", "s2", "budget"])
    for o in ("--work", "--out", "--baselines", "--pyvi-wheel", "--uts-wheel", "--npz-sha", "--g0-sha", "--records"):
        ap.add_argument(o)
    a = ap.parse_args(argv)
    if a.stage == "budget":
        left = budget(Path(a.records))
        print(left)
        return 0 if left > 0 else 5
    try:
        if a.stage == "s1":
            st_s1(a)
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
