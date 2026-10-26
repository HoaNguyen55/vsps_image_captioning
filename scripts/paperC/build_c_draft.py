"""Build the Paper C draft: fill {{ALIAS:key|fmt}} and {{TABLE:name}} placeholders in scripts/paperC/src/*.md from
the decide files, ledgers and pinned sources, and write number_manifest_C.tsv (CP-116 W1).

Reads numbers, ids and labels only: never runs/*.preds*, never a .partial.jsonl, never a caption field.
Build asserts (any failure stops the build, nothing is written):
  - every constant's value string appears in the file it cites (CP-116 W1);
  - every verdict word is rendered from its decide field through the prereg's fixed word mapping (CP-116 W9);
  - every source pinned in PINNED_SHA has that sha256 (decide files, frozen extract, dev-B decomposition);
  - the CHECKS below hold.

  python3 scripts/paperC/build_c_draft.py          writes manuscript/journal_draft_C/
"""
import hashlib
import json
import re
import sys
from pathlib import Path

R = Path(__file__).resolve().parents[2]
SRC = Path(__file__).parent / "src"
OUT = R / "manuscript/journal_draft_C"
M3 = ".session_backup/machines/M3/root/outputs/c_test/"
PRE = "manuscript/prereg/2026-10-25_c_test/PREREG.md"
DES = "manuscript/prereg/2026-10-22_c_stage1/DESIGN.md"
PR2 = "manuscript/prereg/2026-10-22_c_stage2/PREREG.md"
LOGMD = ".session_backup/2026-10-13/decisions/LOG.md"
DEC = ".session_backup/2026-10-13/decisions/"
FROZEN = "scripts/paperC/frozen/worklog_cen_commitment_2026-10-26.txt"
FROZEN_LOG = "scripts/paperC/frozen/decisionlog_pi1026b_pi1026i_2026-10-26.txt"  # LOG.md l.450, l.474 (CP-116a X1)

JSON = {
    "OV": M3 + "decide_ov.json",
    "XM": M3 + "decide_xm_m3.json",
    "XMB": ".session_backup/2026-10-26/c_test/final/decide_xmb.json",
    "DF": ".session_backup/2026-10-22/c_stage2/final/decide_final.json",
    "LISTS": "manuscript/prereg/2026-10-22_c_stage1/lists.json",
    "FC": "manuscript/prereg/2026-10-22_c_stage2/frozen_config.json",
    "E4Q": M3 + "e4/e4_qwen25vl_7b.json",
    "E4I": M3 + "e4/e4_internvl3_8b.json",
    "E4R2Q": M3 + "e4_run2/e4_qwen25vl_7b.json",
    "E4R2I": M3 + "e4_run2/e4_internvl3_8b.json",
    "DEVB": "data/results/paperC/devb_decomposition.json",
}
STATUS = {"DF": "reader-reference", "LISTS": "structural", "FC": "design", "DEVB": "post-hoc-dev",
          "E4Q": "log", "E4I": "log", "E4R2Q": "log", "E4R2I": "log"}
PINNED_SHA = {
    M3 + "decide_ov.json": "9bcad498",
    M3 + "decide_xm_m3.json": "5606ad5d",
    ".session_backup/2026-10-26/c_test/final/decide_xmb.json": "050ecf03",
    ".session_backup/2026-10-22/c_stage2/final/decide_final.json": "92a1f0e9",
    ".session_backup/machines/M3/root/outputs/c_stage2/ledger.jsonl": "be716482",
    FROZEN: "6401b323",
    FROZEN_LOG: "ea61623e",
    "data/results/paperC/devb_decomposition.json": "a61b1b8a",
}
LEDGER = {"L1941": M3 + "ledger_ov_test_1941.jsonl", "L2001": M3 + "ledger_ov_test_2001.jsonl",
          "L2500": M3 + "ledger_xm_test2500.jsonl", "L2392": M3 + "ledger_xm_test2392.jsonl",
          "LS2": ".session_backup/machines/M3/root/outputs/c_stage2/ledger.jsonl",
          "LS1": ".session_backup/machines/M3/root/outputs/c_stage1/ledger.jsonl"}
LEDGER_STATUS = {"LS1": "all-configs-stage-A", "LS2": "all-configs-stage-B"}
PINNED = {"PL": {"ov_test_files.tsv": "manuscript/prereg/2026-10-25_c_test/ov_test_files.tsv",
                 "ov_test_primary1941.txt": "manuscript/prereg/2026-10-25_c_test/ov_test_primary1941.txt",
                 "xm_test2500_threeref108.txt": "manuscript/prereg/2026-10-25_c_test/xm_test2500_threeref108.txt",
                 "neardup60": "manuscript/prereg/2026-10-22_c_stage2/ov_test_dev299_neardup_files.txt"}}
CHAIN_F = ".session_backup/2026-10-26/c_test/CHAIN.log"
# name -> (line substring, regex, occurrence index)
CHAIN = {
    "e4r2_gpu_h": ("BLOCK DONE e4", r"gpu_h_wall (\S+)", 0),
    "e4r3_gpu_h": ("BLOCK DONE e4", r"gpu_h_wall (\S+)", 1),
    "e4r3_total": ("BLOCK DONE e4", r"total (\S+)", 1),
    "ov_gpu_h": ("BLOCK DONE ov", r"gpu_h_wall (\S+)", 0),
    "ov_total": ("BLOCK DONE ov", r"total (\S+)", 0),
    "xm_gpu_h": ("BLOCK DONE xm", r"gpu_h_wall (\S+)", 0),
    "xm_total": ("BLOCK DONE xm", r"total (\S+)", 0),
    "dev299_staged": ("c_e4_dev299     staged", r"staged: (\d+) files", 0),
    "ov_staged": ("c_ov_test     staged", r"staged: (\d+) files", 0),
    "ov_distinct": ("c_ov_test     staged", r"distinct sha (\d+)", 0),
    "xm_staged": ("c_xm_test2500     staged", r"staged: (\d+) files", 0),
    "xm_ref_annotations": ('"file": "xm_test2500_data.json"', r'"annotations": (\d+)', 0),
    "ov_job_start": ("JOB START ov", r"^(\S+) JOB START ov", 0),
}
GS_F = M3 + "gpu_seconds.tsv"
T6 = {"embed": M3 + "t6_retry_ov_test.jsonl", "decode": M3 + "runs/t6_retry_ov_test.jsonl",
      "verify": M3 + "guard/t6_retry_ov_test.jsonl"}

# Non-result constants, counts and timestamps from immutable, sha-pinned sources (CP-116 Q3).
# name -> (value, "file::where", status[, needle]). The build asserts the needle (default: the value) is in the file.
CONST = {
    "near_cut": (0.92, DES + "::§3.2 near cut", "design"),
    "new_tokens": (60, DES + "::§4.2 max new tokens", "design"),
    "boot_B": (2000, PRE + "::§6.3 B", "design", "B = 2000"),
    "ci_level": (95, PRE + "::§6.3 percentile CI", "design", "95% CI"),
    "pcm_floor": (-1.0, PRE + "::§7.4 P2 floor", "design", "**> −1.0**"),
    "vp_floor": (-1.0, PRE + "::§7.5 XM-b floor", "design", "**> −1.0**"),
    "s1_pcm": (-1.0, DES + "::§7.2 eligibility, ΔP_cm against zs", "design", "ΔP_cm against `zs` ≥ −1.0"),
    "len_rule": (0.10, PRE + "::§7.2 rule L", "design", "> 0.10"),
    "e4_pass_pct": (95, PRE + "::§1.2 E4 pass", "design", "≥ 95% identical"),
    "gpu_cap": (20, PRE + "::§12 hard cap", "design", "**20**"),
    "gpu_est": (13.7, PRE + "::§12 upper-bound estimate", "design", "13.7"),
    "dev_gpu_s1": (6.84, PRE + "::§12 stage-1 used", "prereg-quoted"),
    "dev_gpu_s2": (4.91, PRE + "::§12 stage-2 used", "prereg-quoted"),
    "dup_pairs": (4, PRE + "::§3.1 byte-identical pairs", "structural", "4 byte-identical pairs"),
    "primary_distinct": (1937, PRE + "::§3.1 primary distinct images", "structural", "1,937 distinct images"),
    "ov_devdup3": (3, PRE + "::§14 OV-test files identical to removed OV-dev files", "structural",
                   "Three OV-test images (00000000104.jpg, 00000001494.jpeg, 00000010529.png) are byte-identical"),
    "devb_dup2": (2, PRE + "::§14 byte-identical OV-dev-B files", "structural", "The two byte-identical OV-dev-B files"),
    "xm600": (600, DES + "::§2.3 XM600", "structural", "the 600 images"),
    "xm_nonxm600": (3000, DES + "::§2.3 XM3600 minus XM600", "structural", "3,000 XM3600 images not in XM600"),
    "e_dev_a": (121, PR2 + "::§3.3 X5 E-dev-A images", "structural", "121 E-dev-A images"),
    "verifier_stop_q": (20, DES + "::§5 answer-position stop, first questions", "design", "first 20 questions"),
    "verifier_stop_mass": (0.5, DES + "::§5 answer-position stop, median mass", "design", "below 0.5"),
    "nd_hash": (10, DES + "::§2.4 min(pHash,dHash) <=", "design", "min(pHash, dHash) ≤ 10"),
    "nd_sscd": (0.5, DES + "::§2.4 SSCD cosine >=", "design", "SSCD cosine ≥ 0.5"),
    "s1_copy_max": (0.05, DES + "::§7.2 near-verbatim share <=", "design", "near-verbatim copy share ≤ 0.05"),
    "s1_hitmax": (0.02, DES + "::§7.2 hit_max rate <=", "design", "hit_max rate ≤ 0.02"),
    "s1_k": ("{2, 4, 8}", DES + "::§4.3 k grid", "design", "k ∈ {2, 4, 8}"),
    "s1_tau": ("{−∞, 0.0, 0.1, 0.2, 0.3, +∞}", DES + "::§5 threshold grid", "design",
               "τ ∈ {−∞ (no guard), 0.0, 0.1, 0.2, 0.3, +∞"),
    "s1_ret_runs": (7, DES + "::§7.2 the 7 ret runs", "design", "the 7 `ret` runs"),
    "dev299_dropped_id": ("1437", DES + "::§2.2 dev300 minus image 1437", "structural", "minus image `1437`"),
    "s_zf_expected": (10.0, M3 + "decide_ov.json::S_zf.expected_vs_zs_pooled", "design", '"expected_vs_zs_pooled": 10.0'),
    "venv_freeze_1": ("685ffe2a", PRE + "::§1.2 E3 venv freeze", "design"),
    "venv_freeze_2": ("4b81b6b6", PRE + "::§1.2 E3 venv freeze (scoring env)", "design"),
    "venv_freeze_3": ("7332d343", PRE + "::§1.2 E3 venv freeze", "design"),
    "refused163": (163, DEC + "CC-111.txt::l.62 union (recounted from exclusion.json ids.coco ∩ UIT-ViIC train ids)",
                   "ruling", "The union is 163"),
    "refused163_karpathy": (133, DEC + "CC-111.txt::l.62 coco_karpathy_test", "ruling", "coco_karpathy_test 133"),
    "refused163_coco2500": (59, DEC + "CC-111.txt::l.62 coco2500", "ruling", "coco2500 59"),
    "refused163_chair": (14, DEC + "CC-111.txt::l.62 chair500", "ruling", "chair500 14"),
    "refused163_pope": (21, DEC + "CC-111.txt::l.62 pope500", "ruling", "pope500 21"),
    "refused163_sum": (227, DEC + "CP-116.txt::163 breakdown sum", "ruling", "= 227"),
    "uitviic_train": (2695, DEC + "CC-111.txt::l.62 UIT-ViIC train ids", "ruling", "2,695 image ids"),
    "uitviic_val": (924, DEC + "CP-116.txt::W12 UIT-ViIC val references (recounted: 0 refused ids)", "ruling",
                    "924 UIT-ViIC val references touched 0 refused ids"),
    "cen_logged": ("03:11:52Z", FROZEN + "::heading (WORKFLOW_LOG.md l.1612)", "log", "2026-10-26T03:11:52Z"),
    "cen_approved": ("03:15:33Z", FROZEN_LOG + "::LOG.md PI-1026b", "log", "2026-10-26T03:15:33Z | PI-1026b"),
    "cen_karpathy": (5000, DEC + "CC-107.txt::ruling 5 primary (planned, not binding)", "planned", "full COCO Karpathy test (5,000)"),
    "cen_nocaps": (4500, FROZEN_LOG + "::LOG.md PI-1026b secondary (planned, not binding)", "planned", "full NoCaps val (4,500)"),
    "cen_memory": (112322, FROZEN_LOG + "::LOG.md PI-1026i memory (planned, not binding)", "planned", "(112,322"),
    "cen_memory_full": (113287, FROZEN_LOG + "::LOG.md PI-1026i full train+restval (planned, not binding)", "planned", "113,287"),
    "cen_memory_excl": (965, FROZEN_LOG + "::LOG.md PI-1026i excluded ids (planned, not binding)", "planned", "965 refused ids"),
    "cen_nocaps_seen": (1000, DEC + "CC-107.txt::ruling 6 earlier decodes on NoCaps val", "planned", "stratified 1,000"),
    "cen_a_refs": (2441, DEC + "CC-107.txt::ruling 6 A reference use", "planned", "2,441"),
}
# Prereg fixed word mappings for verdict fields (CP-116 W9): fmt token -> (word if True, word if False)
WORDS = {"pass": ("PASS", "FAIL"), "fires": ("fires", "does not fire"), "conf": ("confirmed", "not confirmed"),
         "passed": ("passed", "not passed")}
# Facts the text states in words; the build refuses if they stop holding.
CHECKS = [
    ("XMB", "S3_verified.xm_test2500.per_model.internvl3_8b.np", lambda v: v == 100.0),
    ("XMB", "S3_verified.xm_test2500.per_model.internvl3_8b.lo", lambda v: v == 100.0),
    ("OV", "P1.L", lambda v: v is False),
    ("OV", "scope.sentence", lambda v: v == "carried mainly by Qwen2.5-VL; not detected for InternVL3"),
    ("XM", "per_model.internvl3_8b.hi", lambda v: v < 0),
    ("XM", "sets.xm_test2392.detail.per_model.internvl3_8b.vs_rand.hi", lambda v: v > 0),
]

_cache, rows, seen, _loaded, _ledgers = {}, [], {}, {}, {}
CUR = ""


def sha(rel, n=12):
    if rel not in _cache:
        _cache[rel] = hashlib.sha256((R / rel).read_bytes()).hexdigest()
    return _cache[rel][:n]


def dig(obj, key):
    for part in key.split("."):
        if part == "#len":
            return len(obj)
        obj = obj[int(part)] if isinstance(obj, list) else obj[part]
    return obj


def load(alias):
    if alias not in _loaded:
        _loaded[alias] = json.loads((R / JSON[alias]).read_text())
    return _loaded[alias]


def ledger_rows(alias):
    if alias not in _ledgers:
        _ledgers[alias] = [json.loads(line) for line in (R / LEDGER[alias]).read_text().splitlines()]
    return _ledgers[alias]


def ledger_get(alias, key):
    rid_tau, field = key.split(":")
    rid, tau = rid_tau.split("@")
    hits = [r for r in ledger_rows(alias) if r["run_id"] == rid and r["tau"] == tau]
    # stages A and B re-scored some runs (identical values); their decide uses the last row per (run, tau)
    assert len(hits) == 1 or (alias in ("LS1", "LS2") and hits), (alias, key, len(hits))
    try:
        return dig(hits[-1], field)
    except KeyError:  # field not defined for this row type (e.g. NN baselines)
        return None


def chain_get(name):
    sub, rx, occ = CHAIN[name]
    lines = [line for line in (R / CHAIN_F).read_text().splitlines() if sub in line]
    v = re.search(rx, lines[occ]).group(1)
    try:
        return float(v)
    except ValueError:
        return v


def resolve(alias, key):
    """-> (raw value, source file, file::key string, status)"""
    if alias in JSON:
        return dig(load(alias), key), JSON[alias], f"{JSON[alias]}::{key}", STATUS.get(alias, "keyed")
    if alias in LEDGER:
        return ledger_get(alias, key), LEDGER[alias], f"{LEDGER[alias]}::{key}", LEDGER_STATUS.get(alias, "keyed-ledger")
    if alias == "PL":
        f = PINNED["PL"][key]
        return len((R / f).read_text().splitlines()), f, f"{f}::line_count", "structural"
    if alias == "CHAIN":
        return chain_get(key), CHAIN_F, f"{CHAIN_F}::{CHAIN[key][0]} / {CHAIN[key][1]} #{CHAIN[key][2]}", "log"
    if alias == "GS":
        lines = (R / GS_F).read_text().splitlines()
        return float(lines[int(key)].split()[1]), GS_F, f"{GS_F}::line {int(key) + 1}", "log"
    if alias == "T6":
        step, what = key.split(".")
        recs = [json.loads(line) for line in (R / T6[step]).read_text().splitlines()]
        v = len(recs) if what == "records" else len({x["step"] for x in recs})
        return v, T6[step], f"{T6[step]}::{what}", "log"
    if alias == "C":
        v, src, st, *needle = CONST[key]
        f = src.split("::")[0]
        text = (R / f).read_text()
        cands = needle or [str(v), f"{v:,}" if isinstance(v, int) else str(v)]
        assert any(c in text for c in cands), f"constant {key}: none of {cands} in {f}"
        return v, f, src, st
    raise KeyError(alias)


MINUS = "−"


def num(x, d):
    return f"{x:,.{d}f}".replace("-", MINUS)


def fmt_one(x, f):
    if f == "raw":
        return str(x).replace("-inf", MINUS + "∞")
    if f == "vw":  # a verdict or label string written by a decide step, rendered verbatim
        assert isinstance(x, str), (f, x)
        return x
    if f.startswith("v:"):
        assert isinstance(x, bool), (f, x)
        t, fa = WORDS[f[2:]]
        return t if x else fa
    if f == "s":
        return ("+" if x > 0 else "") + num(x, 2)
    if f in ("p", ""):
        return num(x, 2)
    if f == "f1":
        return num(x, 1)
    if f == "f3":
        return num(x, 3)
    if f == "i":
        return num(x, 0)
    raise ValueError(f)


def reg(alias, key, f):
    raw, src, fk, st = resolve(alias, key)
    if raw is None:
        return "n/a"
    shown = fmt_one(raw, f)
    plain = shown if (f in ("raw", "vw") or f.startswith("v:")) else shown.replace(MINUS, "-").replace("+", "").replace(",", "")
    if f.startswith("v:") or f == "vw":
        st = "verdict"
    k = (plain, fk)
    if k not in seen:
        seen[k] = len(rows)
        rows.append([plain, fk, repr(raw), sha(src), st, set()])
    rows[seen[k]][5].add(CUR)
    return shown


def triple(alias, key, signed=True):
    d = reg(alias, key + ".d", "s" if signed else "p")
    return f"{d} [{reg(alias, key + '.lo', 'p')}, {reg(alias, key + '.hi', 'p')}]"


def sub(m):
    alias, rest = m.group(1), m.group(2)
    if alias == "TABLE":
        return TABLES[rest]()
    key, _, f = rest.partition("|")
    if f in ("e", "eu"):  # key is a prefix with .d .lo .hi; eu = unsigned level (a precision, not a difference)
        return triple(alias, key, signed=(f == "e"))
    if f == "ci":
        return f"[{reg(alias, key + '.lo', 'p')}, {reg(alias, key + '.hi', 'p')}]"
    return reg(alias, key, f)


# ---------------------------------------------------------------- generated tables (CP-116 W10)
def md(head, body):
    return "\n".join(["| " + " | ".join(head) + " |", "|" + "---|" * len(head)] + ["| " + " | ".join(r) + " |" for r in body])


SETS4 = {"ov_test_1941": "OV", "ov_test_2001": "OV", "xm_test2500": "XM", "xm_test2392": "XM"}
SETNAME = {"ov_test_1941": "OV-test primary (1,941)", "ov_test_2001": "OV-test full (2,001)",
           "xm_test2500": "XM-test2500 (2,500)", "xm_test2392": "XM-test2500 without three-ref (2,392)"}
BB = (("qwen25vl_7b", "Qwen2.5-VL"), ("internvl3_8b", "InternVL3"))


def t_controls():
    body = []
    for s, a in SETS4.items():
        p = f"sets.{s}"
        body.append([SETNAME[s], "pooled", triple(a, p + ".detail.pooled_vs_zs"), triple(a, p + ".detail.pooled_vs_fix"),
                     triple(a, p + ".nn.vs_nn_top1.pooled"), triple(a, p + ".nn.vs_nn_cons.pooled"),
                     triple(a, p + ".pooled_ptb_vs_rand")])
        for m, name in BB:
            q = f"{p}.detail.per_model.{m}"
            body.append([SETNAME[s], name, triple(a, q + ".vs_zs"), triple(a, q + ".vs_fix"),
                         triple(a, f"{p}.nn.vs_nn_top1.{m}"), triple(a, f"{p}.nn.vs_nn_cons.{m}"), triple(a, q + ".ptb_vs_rand")])
    return md(["set", "backbone", "`ret` − `zs`", "`ret` − `fix`", "`ret` − NN-top1", "`ret` − NN-consensus",
               "`ret` − `rand`, PTB column"], body)


def t_dose():
    body = []
    for s, a in SETS4.items():
        p = f"sets.{s}.dose_response"
        cells = [f"{triple(a, p + '.' + b)} (n = {reg(a, p + '.' + b + '.n', 'i')})" for b in ("low", "mid", "high")]
        body.append([SETNAME[s], f"{reg(a, p + '.cuts.0', 'f3')}, {reg(a, p + '.cuts.1', 'f3')}"] + cells)
    return md(["set", "cosine cuts", "low", "mid", "high"], body)


def t_style():
    body = []
    for s, a in SETS4.items():
        for m, name in BB:
            q = f"sets.{s}.detail.per_model.{m}"
            for arm in ("ret", "rand", "fix"):
                body.append([SETNAME[s], name, f"`{arm}`", reg(a, f"{q}.style.{arm}.mean_syllables", "p"),
                             reg(a, f"{q}.style.{arm}.ends_punct", "f3"), reg(a, f"{q}.style.{arm}.top3_open_share", "f3"),
                             reg(a, f"{q}.src_share.{arm}", "f3")])
            body.append([SETNAME[s], name, "length gap, near-verbatim share",
                         reg(a, f"{q}.length.rel_gap", "f3"), "", "", reg(a, f"{q}.verbatim_share", "f3")])
    return md(["set", "backbone", "arm", "mean syllables", "ends in punctuation", "top-3 opening share",
               "source-dataset share"], body)


def t_np():
    body = []
    for s, a, k in (("ov_test_1941", "OV", "sets.ov_test_1941.S3"), ("ov_test_2001", "OV", "sets.ov_test_2001.S3"),
                    ("xm_test2500", "XMB", "S3_verified.xm_test2500"), ("xm_test2392", "XMB", "S3_verified.xm_test2392")):
        for m, name in BB + (("pooled", "pooled"),):
            q = f"{k}.per_model.{m}" if m != "pooled" else f"{k}.pooled"
            body.append([SETNAME[s], name, triple(a, q, signed=False), reg(a, q + ".sum_m", "i"), reg(a, q + ".share_m_pos", "f3")])
    return md(["set (gold)", "backbone", "neighbour-only precision [95% CI]", "mentions", "share of images with ≥ 1"], body)


def t_auroc():
    body = []
    for alias, ds, ids in (("LS2", "OV-dev-B", ("c2_qwen25vl_7b_ov_dev_b-ret-k8-first-T1", "c2_internvl3_8b_ov_dev_b-ret-k4-last-T2")),
                           ("LS2", "XM-dev500", ("c2_qwen25vl_7b_xm_dev500-ret-k8-first-T1", "c2_internvl3_8b_xm_dev500-ret-k4-last-T2"))):
        for rid, (_m, name) in zip(ids, BB):
            g = f"{rid}@-inf:guard_auroc"
            body.append([ds, name, reg(alias, g + ".n", "i"), reg(alias, g + ".pos", "i"), reg(alias, g + ".s", "f3"),
                         reg(alias, g + ".p_with", "f3"), reg(alias, g + ".p_without", "f3")])
    return md(["set", "generator", "items", "supported", "AUROC of s", "AUROC of p_with", "AUROC of p_without"], body)


def t_devb():
    body = []
    for ds, name in (("ov_dev_b", "OV-dev-B (925)"), ("xm_dev500", "XM-dev500 (500)")):
        p = f"sets.{ds}."
        body.append([name, triple("DEVB", p + "ret_minus_rand_tau010"), triple("DEVB", p + "ret_minus_rand_tauneginf"),
                     triple("DEVB", p + "ret_tau010_minus_tauneginf"), triple("DEVB", p + "rand_tau010_minus_tauneginf")])
    return md(["set", "`ret` − `rand` at τ = 0.10 (registered)", "`ret` − `rand` at τ = −∞",
               "`ret`: τ = 0.10 minus τ = −∞", "`rand`: τ = 0.10 minus τ = −∞"], body)


def _rows_table(alias, keep, fields):
    seen_ids, body = set(), []
    for r in ledger_rows(alias):
        k = (r["run_id"], r["tau"])
        if k in seen_ids or not keep(r):
            continue
        seen_ids.add(k)
        t = {"-inf": "−∞", "inf": "+∞"}.get(r["tau"], r["tau"])
        body.append([f"`{r['run_id']}`", t] + [reg(alias, f"{r['run_id']}@{r['tau']}:{f}", fm) for f, fm in fields])
    return body


ALLF = [("n", "i"), ("cider_s", "p"), ("pcm_vs_zs", "p"), ("verbatim_share", "f3"), ("hit_max_rate", "f3"),
        ("style.mean_syllables", "p")]
ALLH = ["run", "τ", "n", "CIDEr-D stripped", "ΔP_cm vs zs", "near-verbatim share", "hit_max rate", "mean syllables"]


def t_all_s1():
    return md(ALLH, _rows_table("LS1", lambda r: True, ALLF))


def t_all_s2():
    return md(ALLH, _rows_table("LS2", lambda r: True, ALLF))


def t_unreg():
    body = []
    for al in ("L1941", "L2001", "L2500", "L2392"):
        body += [[al[1:]] + r for r in _rows_table(
            al, lambda r: r["tau"] in ("0.00", "0.20", "0.30", "inf"), [("cider_s", "p"), ("pcm_vs_zs", "p")])]
        for r in ledger_rows(al):
            if r.get("guard_auroc"):
                g = f"{r['run_id']}@{r['tau']}:guard_auroc"
                body.append([al[1:], f"`{r['run_id']}`", "−∞ (verifier AUROC of s)", reg(al, g + ".s", "f3"),
                             f"items {reg(al, g + '.n', 'i')}"])
    return md(["scored set", "run", "τ", "CIDEr-D stripped", "ΔP_cm vs zs / note"], body)


TABLES = {"controls": t_controls, "dose": t_dose, "style": t_style, "np": t_np, "auroc": t_auroc, "devb": t_devb,
          "all_stage_a": t_all_s1, "all_stage_b": t_all_s2, "unregistered": t_unreg}

PH = re.compile(r"\{\{([A-Z0-9]+):([^}]+)\}\}")


def main():
    global CUR
    for f, h in PINNED_SHA.items():
        assert sha(f, 64).startswith(h), f"{f} sha256 {sha(f, 8)} is not the pinned {h}"
    for a, k, ok in CHECKS:
        assert ok(dig(load(a), k)), f"check failed: {a}::{k}"
    built = {}
    for t in sorted(SRC.glob("*.md")):
        CUR = t.name
        text = PH.sub(sub, t.read_text())
        assert "{{" not in text, t
        built[t.name] = text
    OUT.mkdir(exist_ok=True)
    for name, text in built.items():
        (OUT / name).write_text(text)
    with open(OUT / "number_manifest_C.tsv", "w") as fh:
        fh.write("number\tfile::key\traw_value\tsha256_prefix\tstatus\tused_in\n")
        for r in rows:
            fh.write("\t".join(r[:5] + [",".join(sorted(r[5]))]) + "\n")
    print(f"build asserts ok: {len(PINNED_SHA)} pinned shas, {len(CHECKS)} checks, "
          f"{sum(1 for r in rows if r[4] == 'verdict')} verdict rows; {len(rows)} manifest rows")


if __name__ == "__main__":
    sys.exit(main())
