"""CC-516 independent recompute of FE-LOCUS registered quantities from PER_IMAGE_ALT.npz (aggregates only).
Own implementation of prereg v2 s3.2 step 0, s3.4, s4; imports nothing from scripts/b_alt.
FRAGILE rows use b_fecert.certify/stats (the registered FE-CERT rule, unchanged) with own class building."""
import hashlib, json, sys
from pathlib import Path
import numpy as np

R = Path.home() / "vsps_ro3/b_alt_result"
NPZ, RES = R / "b_alt_out/PER_IMAGE_ALT.npz", R / "b_alt_out/RESULT_ALT.json"
DEV = Path("/mnt/d/vsps_image_captioning/manuscript/prereg/2026-11-12_b_fecert/results/b_work/DEV.json")
sha = lambda p: hashlib.sha256(p.read_bytes()).hexdigest()
assert sha(NPZ).startswith("32da6dd0") and sha(RES).startswith("18654e20") and sha(DEV).startswith("88ff39aa")
z = np.load(NPZ, allow_pickle=False)
C, mem, files, ids = z["cider"], [str(m) for m in z["members"]], [str(f) for f in z["files"]], [str(i) for i in z["ids"]]
cref_all, cout_all = z["counts_ref"], z["counts_out"]
assert ids == sorted(ids) and len(ids) == 558 and C.shape == (108, 75, 558)
mi, fi = {m: k for k, m in enumerate(mem)}, {f: j for j, f in enumerate(files)}

# s3.2 step 0
perm = np.random.default_rng(20261127).permutation(558)
A, Bh = sorted(perm[:279]), perm[279:]  # Bh in registered order
assert len(set(A) & set(Bh)) == 0
comps = [(c["id"][2:].split("|")[0], c["id"].split("|")[1]) for c in json.loads(DEV.read_text())["comparisons"]]
assert len(comps) == 1101
ia, ib = np.array([fi[a] for a, _ in comps]), np.array([fi[b] for _, b in comps])
T, P, Cc = ("tw", "tm", "tf"), ("pk", "pf", "pa"), ("cf", "ck")
levels = [(t, p, c) for t in T for p in P for c in Cc]

def diff(m):  # per comparison x half-B image difference d_{c,i,m}
    x = C[mi[m]][:, Bh]
    return x[ia] - x[ib]

n = len(Bh)
vec = {k: np.zeros(n) for k in ("A", "Ah", "Aa", "A_tw", "Aa_tw", "A_tmf", "Aa_tmf")}
abs_shift = abs_Dr = 0.0
sig0 = 0
for lv in levels:
    r, p = "rdr." + ".".join(lv), "pyvi." + ".".join(lv)
    dr, dp = diff(r), diff(p)
    de = dp - dr
    deh = diff(p + "+Ph") - diff(r + "+Ph")
    dea = diff(p + "+Pa") - diff(r + "+Pa")
    s = np.sign(de.mean(1)); sig0 += int((s == 0).sum())
    abs_shift += np.abs(de.mean(1)).sum(); abs_Dr += np.abs(dr.mean(1)).sum()
    g = "tw" if lv[0] == "tw" else "tmf"
    for k, d in (("A", de), ("Ah", deh), ("Aa", dea)):
        vec[k] += s @ d
    vec["A_" + g] += s @ de; vec["Aa_" + g] += s @ dea

idx = np.random.default_rng(20261128).integers(0, n, (10000, n))
W = np.zeros((10000, n)); np.add.at(W, (np.arange(10000)[:, None], idx), 1.0)
pct = lambda x: [float(v) for v in np.percentile(x, [2.5, 97.5])]
def est(Wx):
    g = {k: Wx @ v / n for k, v in vec.items()}
    cr = Wx @ cref_all[Bh, 0] / (Wx @ cref_all[Bh, 1]); co = Wx @ cout_all[Bh, 0] / (Wx @ cout_all[Bh, 1])
    kap = (g["A"] - g["Ah"]) / (g["A"] - g["Aa"])
    return dict(rho_head=1 - g["Ah"] / g["A"], rho_all=1 - g["Aa"] / g["A"], kappa_head=kap, c_ref=cr, c_out=co,
                d_lo=kap - np.minimum(cr, co), d_hi=kap - np.maximum(cr, co),
                rho_tw=1 - g["Aa_tw"] / g["A_tw"], rho_tmf=1 - g["Aa_tmf"] / g["A_tmf"])
pt, dr_ = est(np.ones((1, n))), est(W)
out = {k: {"point": float(pt[k][0]), "ci95": pct(dr_[k])} for k in pt}
out["floor_iv"] = {"sum_abs_shift": abs_shift, "sum_abs_D_r": abs_Dr, "ratio": abs_shift / abs_Dr,
                   "trips": bool(abs_shift < 0.01 * abs_Dr)}
out["floor_v_posthoc"] = {"L_rho_all": out["rho_all"]["ci95"][0], "would_trip": out["rho_all"]["ci95"][0] < 0.20}
out["sigma_zero"] = sig0
# floors (ii)/(iii) proxies from image counts (census strings themselves deleted with CENSUS_ALT.json)
out["half_A_ref_unaligned"] = int(cref_all[A, 3].sum()); out["half_A_ref_strings"] = 279 * 5
out["half_A_coverage_head"] = float(cref_all[A, 0].sum() / cref_all[A, 1].sum())
out["half_A_ref_occ_all"] = int(cref_all[A, 1].sum()); out["half_A_ref_other"] = int(cref_all[A, 2].sum())
out["half_B_ref_occ"] = [int(x) for x in cref_all[Bh].sum(0)]; out["half_B_out_occ"] = [int(x) for x in cout_all[Bh].sum(0)]
# would-be labels (POST HOC, not registered outcomes: floor (iv) governs)
out["counterfactual_labels_POSTHOC"] = {
    "H-L1": "TAIL" if out["d_lo"]["ci95"][1] < 0 else "HEAD" if out["d_hi"]["ci95"][0] > 0 else "PROPORTIONAL",
    "H-L2": "PRACTICAL" if out["rho_head"]["ci95"][0] > .5 else "NOT PRACTICAL" if out["rho_head"]["ci95"][1] < .5 else "INCONCLUSIVE"}
# compare with RESULT_ALT.json
res = json.loads(RES.read_text()); D = res["DESCRIPTIVE"]
pairs = [("kappa_head", res["H-L1"]["kappa_head"], res["H-L1"]["kappa_head_95"]),
         ("d_lo", None, res["H-L1"]["d_lo_95"]), ("d_hi", None, res["H-L1"]["d_hi_95"]),
         ("rho_head", res["H-L2"]["rho_head"], res["H-L2"]["rho_head_95"]),
         ("rho_all", D["rho_all"], D["rho_all_95"]), ("c_ref", D["c_ref_B"], D["c_ref_B_95"]),
         ("c_out", D["c_out_B"], D["c_out_B_95"]), ("rho_tw", D["rho_all_tw_pairs"], D["rho_all_tw_pairs_95"]),
         ("rho_tmf", D["rho_all_tm_tf_pairs"], D["rho_all_tm_tf_pairs_95"])]
mx = 0.0
for k, p, ci in pairs:
    if p is not None: mx = max(mx, abs(p - out[k]["point"]))
    mx = max(mx, *(abs(a - b) for a, b in zip(ci, out[k]["ci95"])))
mx = max(mx, abs(D["floor_iv"]["sum_abs_shift"] - abs_shift), abs(D["floor_iv"]["sum_abs_D_r"] - abs_Dr))
out["max_abs_diff_vs_RESULT_ALT"] = mx
out["counts_match"] = (D["output_only_occurrences_half_B"] == out["half_B_out_occ"][2]
                       and D["output_occurrences_of_Pi_all_types_half_B"] == out["half_B_out_occ"][1]
                       and D["unaligned_strings_half_B"] == {"references": out["half_B_ref_occ"][3], "outputs": out["half_B_out_occ"][3]})
out["registered_label"] = "NOT_EVALUABLE (iv)" if out["floor_iv"]["trips"] else "floor (iv) passes"
out["label_match"] = res["H-L1"]["label"].startswith("NOT_EVALUABLE (iv)") == out["floor_iv"]["trips"] and res["H-L2"]["label"] == res["H-L1"]["label"]
# FRAGILE rows (DESCRIPTIVE) via the registered FE-CERT rule
try:
    sys.path[:0] = ["/mnt/d/vsps_image_captioning/scripts/b_fecert", "/mnt/d/vsps_image_captioning"]
    import b_fecert as BF
    GW = [f"{u}." + ".".join(lv) for u in ("rdr", "pyvi") for lv in levels]
    keys, rk = z["keys"], z["rkeys"]
    fr = {}
    for tag, suf in (("raw", ""), ("pinned_head", "+Ph")):
        names = [g + suf for g in GW]; f0 = "rdr.tw.pk.cf" + suf; frag = chg = 0
        for a, b in comps:
            ja, jb = fi[a], fi[b]; cl = {}
            for m in names:
                k = mi[m]; key = f"{keys[k, ja]}|{keys[k, jb]}|{rk[k]}"
                c = cl.setdefault(key, {"members": []}); c["members"].append(m)
                if "cider" not in c: c["cider"] = BF.stats((C[k, ja] - C[k, jb])[Bh], W)
            v = BF.certify({"id": f"D:{a}|{b}", "classes": cl}, set(names))
            frag += bool(v["fragile"])
            s0 = next(BF.sig(c["cider"]) for c in cl.values() if f0 in c["members"])
            chg += s0 != 0 and v["certified"] != s0
        fr[tag] = {"fragile": frag, "changed": chg, "comparisons": 1101}
    out["fragile_over_G_w"] = fr; out["fragile_match"] = fr == D["fragile_over_G_w"]
except Exception as e:
    out["fragile_over_G_w"] = f"not recomputed: {type(e).__name__}"
print(json.dumps(out, indent=1))
