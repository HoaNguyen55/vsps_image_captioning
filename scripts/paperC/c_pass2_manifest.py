"""Append C pass-2 rows (C-EN, C-2, prereg-quoted, logs) to number_manifest_C.tsv in the build's 6-column format.
Reads decide/verdict JSON, logs and preregs only; never a preds file. Idempotent: drops earlier pass-2 rows first.
  python3 c_pass2_manifest.py            append rows
  python3 c_pass2_manifest.py --print    print plain values only
"""
import hashlib, json, sys
from pathlib import Path

R = Path("/mnt/d/vsps_image_captioning")
MAN = R / "manuscript/journal_draft_C/number_manifest_C.tsv"
TAG = "c-pass2"
CO = ".session_backup/machines/M3/root/outputs/c_en/decide_coco_test.json"
NC = ".session_backup/machines/M3/root/outputs/c_en/decide_nocaps_val.json"
C2 = ".session_backup/machines/M4/root/outputs/c2_ablation/decide.json"
PQ = ".session_backup/machines/M4/root/outputs/c2_ablation/parity_qwen25vl_7b.json"
PI = ".session_backup/machines/M4/root/outputs/c2_ablation/parity_internvl3_8b.json"
BUILD = ".session_backup/machines/M3/root/outputs/c_en/logs/build.log"
MEMD = ".session_backup/machines/M3/root/outputs/c_en/fetch/memory.done.json"
SMOKE = ".session_backup/machines/M3/root/outputs/c_en/smoke_record.json"
GS = ".session_backup/machines/M3/root/outputs/c_en/gpu_seconds.tsv"
C2GS = ".session_backup/machines/M4/root/outputs/c2_ablation/gpu_seconds.tsv"
C2JOB = ".session_backup/machines/M4/root/outputs/c2_ablation/logs/job.log"
CHAIN = ".session_backup/2026-10-27/c_en/CHAIN.log"
PRE = "manuscript/prereg/2026-10-27_c_en/PREREG.md"
PRE2 = "manuscript/prereg/2026-10-28_c2_ablation/PREREG.md"

S = "c-en-registered"      # C-EN registered rows (PREREG §7)
SD = "c-en-reported"       # C-EN reported, non-gating rows
D2 = "c2-dev-nonconfirmatory"
Q = "prereg-quoted"
L = "log"

M = "−"
def num(x, d): return f"{x:,.{d}f}".replace("-", M)
def fmt(x, f):
    if f == "s": return ("+" if x > 0 else "") + num(x, 2)
    if f == "p": return num(x, 2)
    if f == "f3": return num(x, 3)
    if f == "i": return num(x, 0)
    if f == "v": return x if isinstance(x, str) else ("PASS" if x else "FAIL")
    raise ValueError(f)
def dig(o, k):
    t = k.split(".")
    while t:
        for n in range(len(t), 0, -1):
            if ".".join(t[:n]) in o:
                o = o[".".join(t[:n])]; t = t[n:]; break
        else:
            raise KeyError(k)
    return o

_j, _s = {}, {}
def J(f):
    if f not in _j: _j[f] = json.loads((R / f).read_text())
    return _j[f]
def sha(f):
    if f not in _s: _s[f] = hashlib.sha256((R / f).read_bytes()).hexdigest()[:12]
    return _s[f]

rows = []
def key(f, k, fm, st):
    v = dig(J(f), k); rows.append((fmt(v, fm), f"{f}::{k}", repr(v), sha(f), st))
def tri(f, k, st, signed=True):
    key(f, k + ".d", "s" if signed else "p", st); key(f, k + ".lo", "p", st); key(f, k + ".hi", "p", st)
def const(shown, f, loc, st, needle=None):
    needle = needle or shown
    assert needle in (R / f).read_text(), (f, needle)
    rows.append((shown, f"{f}::{loc}", repr(needle), sha(f), st))

# --- C-EN COCO (PREREG §7 P1-EN) ---
c = "scored.coco_test_5000."
key(CO, "P1_EN.verdict", "v", "verdict")
assert J(CO)["P1_EN"]["L"] is False; rows.append(("does not fire", f"{CO}::P1_EN.L", "False", sha(CO), "verdict"))
tri(CO, "P1_EN", S)
key(CO, c + "n", "i", "structural")
for m in ("qwen25vl_7b", "internvl3_8b"):
    for x in ("ret_minus_rand", "ret_minus_zs", "rand_minus_zs"): tri(CO, c + f"per_model.{m}.{x}", SD)
    for x in ("len_ret", "len_rand"): key(CO, c + f"per_model.{m}.{x}", "p", SD)
    key(CO, c + f"per_model.{m}.length_gap", "f3", SD)
tri(CO, c + "pooled_ret_minus_zs", SD); tri(CO, c + "secondary_neg_inf_internvl3", S)
key(CO, c + "secondary_neg_inf_internvl3.label", "v", "verdict")
for a in ("guard", "guard_rand"):
    for x in ("neighbour_only", "rejected", "deleted", "fallback"): key(CO, c + f"per_model.internvl3_8b.{a}.{x}", "i", SD)
key(CO, "utc", "v", L); key(CO, "head", "v", L)

# --- C-EN NoCaps (PREREG §7 S-NC) ---
key(NC, "S_NC.verdict", "v", "verdict"); key(NC, "S_NC_sensitivity_3500.verdict", "v", "verdict")
assert J(NC)["claim_transfers_to_nocaps"] is False; rows.append(("not made", f"{NC}::claim_transfers_to_nocaps", "False", sha(NC), "verdict"))
tri(NC, "S_NC", S); tri(NC, "S_NC_sensitivity_3500", S)
for s in ("nocaps_val_4500", "nocaps_val_3500"):
    p = f"scored.{s}."
    key(NC, p + "n", "i", "structural")
    for m in ("qwen25vl_7b", "internvl3_8b"):
        for x in ("ret_minus_rand", "ret_minus_zs", "rand_minus_zs"): tri(NC, p + f"per_model.{m}.{x}", SD)
        for x in ("len_ret", "len_rand"): key(NC, p + f"per_model.{m}.{x}", "p", SD)
        key(NC, p + f"per_model.{m}.length_gap", "f3", SD)
    tri(NC, p + "pooled_ret_minus_zs", SD); tri(NC, p + "secondary_neg_inf_internvl3", S)
    key(NC, p + "secondary_neg_inf_internvl3.label", "v", "verdict")
for a in ("guard", "guard_rand"):
    for x in ("neighbour_only", "rejected", "deleted", "fallback"):
        key(NC, f"scored.nocaps_val_4500.per_model.internvl3_8b.{a}.{x}", "i", SD)
for d in ("in-domain", "near-domain", "out-domain"):
    tri(NC, f"per_domain.{d}", SD); key(NC, f"per_domain.{d}.n", "i", "structural")
key(NC, "utc", "v", L); key(NC, "head", "v", L)

# --- C-EN memory, smoke, GPU (logs) ---
B = json.loads((R / BUILD).read_text())
for k, v in [("recorded", B["recorded"]), ("kept", B["kept"]), ("clusters", B["clusters"]),
             ("near_dropped_any", B["near_dropped_any"]), ("near_dropped.coco_test", B["near_dropped"]["coco_test"]),
             ("near_dropped.nocaps_val", B["near_dropped"]["nocaps_val"]), ("near_dropped.coco_kval", B["near_dropped"]["coco_kval"]),
             ("unreadable", B["unreadable"])]:
    rows.append((num(v, 0), f"{BUILD}::{k}", repr(v), sha(BUILD), L))
key(MEMD, "refused", "i", L); key(MEMD, "recorded", "i", L)
key(SMOKE, "captions", "i", L); key(SMOKE, "empty", "i", L)
g = (R / GS).read_text().splitlines()
tests = [(i, float(l.split()[1])) for i, l in enumerate(g) if l.startswith("test ")]
for i, v in tests:
    rows.append((num(v, 0), f"{GS}::line {i + 1}", repr(v), sha(GS), L))
    rows.append((num(v / 3600, 2), f"{GS}::line {i + 1} / 3600 (GPU-h)", repr(v / 3600), sha(GS), L))
tot = sum(v for _, v in tests)
rows.append((num(tot, 0), f"{GS}::sum of 'test' lines", repr(tot), sha(GS), L))
rows.append((num(tot / 3600, 2), f"{GS}::sum of 'test' lines / 3600 (GPU-h)", repr(tot / 3600), sha(GS), L))
const("2026-10-27T10:33:32Z", CHAIN, "HEAD MOVE line", L)
const("16 memory images", PRE, "§9 step 6 smoke", Q, "16 memory images")
const("ed1e6c41", CHAIN, "HEAD MOVE from", L); const("f8cccb68", CHAIN, "HEAD MOVE to", L)

# --- C-EN prereg-quoted design numbers ---
for shown, loc, needle in [
    ("5,000", "§3.1 COCO Karpathy test", "5,000"), ("4,500", "§3.2 NoCaps val", "4,500"),
    ("3,500", "§3.2 sensitivity", "3,500"), ("1,000", "§3.2 vg-mamf stratified 1,000", "stratified 1,000"),
    ("417", "§3.2 domain counts", "417 in"), ("2,670", "§3.2 domain counts", "2,670 near"),
    ("1,413", "§3.2 domain counts", "1,413 out"), ("113,287", "§4 candidates", "113,287"),
    ("965", "§4 refused", "965 refused"), ("112,322", "§4 allowed", "**112,322**"),
    ("+2.0", "§7 SESOI", "**+2.0**"), ("25", "§10 test cap", "**25 GPU-h**"),
    ("0.69", "§10 Qwen per image-arm OV", "Qwen 0.69 s"), ("1.24", "§10 InternVL3 per image-arm OV", "InternVL3 1.24 s"),
    ("24", "§2 guard shared classes", "24 of its 80"), ("80", "§2 COCO-80 classes", "24 of its 80"),
    ("112", "§2 S2 class map", "112-class"), ("163", "§12.2", "163 distinct"), ("133", "§12.2", "133 coco_karpathy_test"),
    ("227", "§12.2", "= 227"), ("2,441", "§12.3a", "2,441"), ("295", "§12.3b", "295 of the 5,000"),
    ("130", "§12.6 (PI-1026w wording)", "130 Karpathy-val ids"), ("9", "§12.3a A systems", "9 systems"),
    ("10", "§3.1 sixth reference", "10 of the 5,000"), ("5", "§3.1 first 5 references", "first 5"),
    ("2,402", "§4.8 UT pool", "2,402 images"), ("2026-10-27", "amendment 1 date", "2026-10-27"),
]:
    const(shown, PRE, loc, Q, needle)

# --- C-2 (DEV-B MECHANISM, NON-CONFIRMATORY) ---
key(C2, "label", "v", D2); key(C2, "n_images", "i", D2)
for k in ("AB-M.outcome", "AB-K.P-K.outcome", "AB-tau.outcome", "AB-K.P-K.label"): key(C2, k, "v", "verdict")
for k in ("section6_explains_backbone_dependence", "AB-M.M1_ci_hi_lt_0", "AB-M.M2_did_le_minus_sesoi", "AB-M.M3_monotone_points",
          "AB-tau.i_monotone", "AB-tau.ii_cost_ret_lt_rand", "AB-tau.iii_inf_ci_lo_le_0"):
    rows.append((str(dig(J(C2), k)), f"{C2}::{k}", repr(dig(J(C2), k)), sha(C2), "verdict"))
for p in ("10", "30", "100"):
    tri(C2, f"AB-M.pooled.{p}", D2); key(C2, f"mean_top1_cos.{p}", "f3", D2)
    for m in ("qwen25vl_7b", "internvl3_8b"):
        tri(C2, f"AB-M.per_model.{m}.delta.{p}", D2); key(C2, f"AB-M.per_model.{m}.src_share.{p}", "f3", D2)
    tri(C2, f"AB-M.per_model.internvl3_8b.delta_tau_-inf.{p}", D2)
    for s in ("ktvic", "ktvic+openviic", "openviic"): key(C2, f"composition.{p}.{s}", "i", D2)
for p in ("10", "30"): key(C2, f"subsets.{p}.n", "i", D2)
tri(C2, "AB-M.did_pooled", D2)
for m in ("qwen25vl_7b", "internvl3_8b"): tri(C2, f"AB-M.per_model.{m}.did", D2)
for kk in ("2", "4", "8"):
    for m in ("qwen25vl_7b", "internvl3_8b"):
        tri(C2, f"AB-K.{m}.delta.{kk}", D2)
        key(C2, f"AB-K.{m}.copy4_memory.{kk}", "f3", D2); key(C2, f"AB-K.{m}.verbatim_share.{kk}", "f3", D2)
        for a in ("ret", "rand"):
            key(C2, f"AB-K.{m}.style.{kk}.{a}.mean_syllables", "p", D2)
            key(C2, f"AB-K.{m}.style.{kk}.{a}.ends_punct", "f3", D2); key(C2, f"AB-K.{m}.style.{kk}.{a}.top3_open_share", "f3", D2)
tri(C2, "AB-K.P-K.did_8_minus_2", D2)
for t in ("-inf", "0.00", "0.10", "0.20", "0.30", "inf"):
    tri(C2, f"AB-tau.delta.{t}", D2)
    for a in ("ret", "rand"):
        for x in ("neighbour_only_rate", "rejected_per_image", "fallback_rate", "deleted_rate"):
            key(C2, f"AB-tau.guard_rates.{t}.{a}.{x}", "f3", D2)
        v = dig(J(C2), f"AB-tau.guard_rates.{t}.{a}.np")
        if v is not None: key(C2, f"AB-tau.guard_rates.{t}.{a}.np", "p", D2)
        key(C2, f"AB-tau.guard_rates.{t}.{a}.np_sum_m", "i", D2)
for t in ("0.00", "0.10", "0.20", "0.30"):
    for a in ("ret", "rand"): tri(C2, f"AB-tau.cost.{t}.{a}", D2)
for m in ("qwen25vl_7b", "internvl3_8b", "pooled"): tri(C2, f"rand_minus_zs_100.{m}", D2)
key(PQ, "identical", "i", L); key(PQ, "n", "i", L); key(PI, "identical", "i", L); key(PI, "n", "i", L)
const("3.32", C2JOB, "BLOCK DONE gpu_h", L, "BLOCK DONE gpu_h 3.32")
c2s = sum(float(l.split()[1]) for l in (R / C2GS).read_text().splitlines() if l.split()[1] != "start")
rows.append((num(c2s, 0), f"{C2GS}::sum of seconds lines", repr(c2s), sha(C2GS), L))
for shown, needle in [("5", "Cap (5 GPU-h, hard 6)"), ("6", "Cap (5 GPU-h, hard 6)"), ("819", "10% = 819"),
                      ("2,457", "30% = 2,457"), ("8,190", "8,190 clusters"), ("925", "925 images")]:
    const(shown, PRE2, "§2/§6", Q, needle)

if __name__ == "__main__":
    if "--print" in sys.argv:
        for r in rows: print(r[0], r[1].split("::")[-1], sep="\t")
        sys.exit()
    keep = [l for l in MAN.read_text().splitlines() if not l.endswith(TAG)]
    md = {f.name: f.read_text() for f in sorted(MAN.parent.glob("*.md"))}
    seen = set()
    out = []
    for shown, fk, raw, sh, st in rows:
        plain = shown.replace(M, "-").replace("+", "").replace(",", "")
        if (plain, fk) in seen: continue
        seen.add((plain, fk))
        used = [n for n, t in md.items() if shown in t] if len(shown) >= 4 else []
        out.append("\t".join([plain, fk, raw, sh, st, ",".join(used) + ("|" if used else "") + TAG]))
    MAN.write_text("\n".join(keep + out) + "\n")
    print(f"kept {len(keep) - 1} build rows, appended {len(out)} pass-2 rows")
