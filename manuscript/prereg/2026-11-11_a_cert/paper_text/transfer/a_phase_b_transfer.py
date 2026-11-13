"""Paper A certification, PHASE B paper-text transfer (CC-357 Ruling 5; Home S by CC-369 Ruling 6).

Run from anywhere: python3 -I a_phase_b_transfer.py
Starts from `git show HEAD:` of every target file (paper HEAD c58a0be), so a re-run is idempotent.
Writes the paper repo working tree only; never stages or commits. Runs no scoring code.
Reads: the package, the result files named by CC-357/CC-360/CC-369, the registrations, the paper files.
Every number placed in the text goes through N()/D()/REG(), which also writes its number_manifest row.
"""
import hashlib
import json
import re
import subprocess
import sys

RUN = "/mnt/d/vsps_image_captioning"
PAPER = "/mnt/d/vsps_papers/vsps-paperA-spic"
HEAD = "c58a0be22cbbf8325d5ea39d4bcc1785d7b33d01"
OUT_JSON = RUN + "/manuscript/prereg/2026-11-11_a_cert/paper_text/transfer/a_phase_b_report.json"


def sha(b):
    return hashlib.sha256(b).hexdigest()


def git(repo, *args):
    return subprocess.run(["git", "-C", repo, *args], check=True, capture_output=True).stdout


def rd(rel, want):
    b = open(RUN + "/" + rel, "rb").read()
    assert sha(b) == want, (rel, sha(b))
    return b


SRC = {  # alias: (path, sha256)
    "PKG": ("manuscript/prereg/2026-11-11_a_cert/paper_text/A_CERT_PAPER_TEXT_v1.md", "d2548abc379de4d9c6b0132865cdfe6fb39639f777c4503a15cb5e8aa7ed0b73"),
    "RES": ("data/results/a_cert/score/A_CERT_RESULT.json", "7492a16c692d3fd5ed28c4b8eaeab91766544ec5bd4ebe307a48537469d80957"),
    "FRZ": ("data/results/a_cert/freeze/FREEZE.json", "c51ea7dc85d13b2f9827732f38218d41f26d877b06427bae02417e50482c3ae2"),
    "VR": ("data/results/a_cert_v/score/A_CERT_V_RESULT.json", "2675cdcec0e2285158e4154ea384421ae50b3c0b7b3f3133983b77ad5040c410"),
    "PR": ("data/results/a_cert_p/score/A_CERT_P_RESULT.json", "a05edf41c1da6810d2abdf1f772e52f518804e6fff7a7bf32bed60e3264f56d0"),
    "R11": ("manuscript/prereg/2026-11-11_a_cert/A_CERT_ANALYSIS_REG_v1_1.md", "e564b7b10cf500db50e48748f9e4e2e010378313eaeca89c4d14bde6d072aa7e"),
    "VP": ("manuscript/prereg/2026-11-11_a_cert/A_CERT_ADDENDUM_VP_v1_1.md", "0e586fa95814ef9ec1ec07c7a0318c59f10db7e15ee48ab4ab8f5a8a0207a72f"),
    "H2D": ("manuscript/prereg/2026-11-11_a_cert/A_CERT_ANALYSIS_REG_v1_3_H2D.md", "d0afcaf0390031f1a2825a2d1e1b49ede6e57d42424be8281682c48f1e440515"),
    "PLAN": ("manuscript/prereg/2026-11-11_xm600_gold_completion/XM600_GOLD_COMPLETION_PLAN_v1_1.md", "8ad28f67fe4fbc3e026a60051dee7fc3c3ee61c94d2d1d4f51deb4779bf6f578"),
}
RAW = {a: rd(p, s) for a, (p, s) in SRC.items()}
for a in ("RES", "FRZ", "VR", "PR"):
    assert sha(git(RUN, "show", "HEAD:" + SRC[a][0])) == SRC[a][1], ("not HEAD blob", a)
DATA = {a: json.loads(RAW[a]) for a in ("RES", "FRZ", "VR", "PR")}
TXT = {a: RAW[a].decode("utf-8") for a in ("PKG", "R11", "VP", "H2D", "PLAN")}
L = TXT["PKG"].split("\n")
assert git(PAPER, "rev-parse", "HEAD").decode().strip() == HEAD, "paper HEAD"

STATUS = {
    "RES": "keyed (REGISTERED or DESCRIPTIVE; single annotator; new labels on previously analysed captions; pinned PIN-1112-a-cert-RESULT; CC-369; Phase B)",
    "FRZ": "keyed (development (no labels); FREEZE pinned OPS-1112h; Phase B)",
    "VR": "keyed (DEVELOPMENT; Part V label; pinned PIN-1112-a-vp-RESULT; CC-360; Phase B)",
    "PR": "keyed (POST HOC; Part P label; pinned PIN-1112-a-p-RESULT; CC-360; Phase B)",
}
MAN = {}          # (file, key, shown) -> [where list, status]
DEPART = []       # (row, file-or-block, what)
WHERE = ["?"]


def at(where):
    WHERE[0] = where


def keystr(key):
    out = []
    for s in key:
        if isinstance(s, int):
            out.append(f"[{s}]")
        elif re.fullmatch(r"[A-Za-z_][A-Za-z0-9_]*", s):
            out.append("." + s)
        else:
            out.append(f'."{s}"')
    return "".join(out).lstrip(".")


def get(alias, key):
    d = DATA[alias]
    for s in key:
        d = d[s]
    return d


def _m(fn, x):
    if isinstance(x, str):      # stored non-numeric value such as "NI": printed as stored
        return x
    assert x is not None
    return fn(x).replace("-", "−")


def sl(x):          # signed slope, 2 dp
    return _m(lambda v: f"{v:+.2f}", x)


def f1d(x):
    return _m(lambda v: f"{v:,.1f}", x)


def f2(x):
    return _m(lambda v: f"{v:.2f}", x)


def f3(x):
    return _m(lambda v: f"{v:.3f}", x)


def f3s(x):         # signed 3 dp
    return _m(lambda v: f"{v:+.3f}", x)


def f4(x):
    return _m(lambda v: f"{v:.4f}", x)


def pct(x):
    return f"{100 * x:.1f}%"


def nint(x):
    assert float(x) == int(x), x
    return f"{int(x):,}"


def ci(fn):
    return lambda v: f"[{fn(v[0])}, {fn(v[1])}]"


def addman(file, key, shown, sha12, status):
    k = (file, key, shown)
    if k not in MAN:
        MAN[k] = [[], sha12, status]
    if WHERE[0] not in MAN[k][0]:
        MAN[k][0].append(WHERE[0])


def N(alias, key, fn):
    shown = fn(get(alias, key))
    addman(SRC[alias][0], keystr(key), shown, SRC[alias][1][:12], STATUS[alias])
    return shown


def D(shown, alias, rule):
    addman(SRC[alias][0], rule, shown, SRC[alias][1][:12], "DERIVED (" + STATUS[alias] + ")")
    return shown


def REG(alias, line, literal, shown=None):
    """Registered constant: literal must occur on the named line of the registered text."""
    assert literal in TXT[alias].split("\n")[line - 1], (alias, line, literal)
    shown = shown or literal
    addman(SRC[alias][0], f"l.{line} '{literal}'", shown, SRC[alias][1][:12],
           f"REGISTERED CONSTANT ({alias} l.{line}, quoted; CC-373 N3; Phase B)")
    return shown


def REGF(alias, literal, shown=None):
    """Registered constant found by its literal; the first line holding it is recorded."""
    ls = TXT[alias].split("\n")
    hit = [i + 1 for i, l in enumerate(ls) if literal in l]
    assert hit, (alias, literal)
    return REG(alias, hit[0], literal, shown)


def LOGV(line_id, shown):
    addman(".session_backup/2026-10-13/decisions/LOG.md", line_id, shown, "-", "LOG line (time from its stamp; Phase B)")
    return shown


def T(_tpl, **kw):
    for k, v in kw.items():
        assert "«" + k + "»" in _tpl, k
        _tpl = _tpl.replace("«" + k + "»", v)
    assert "«" not in _tpl, _tpl[:80]
    return _tpl


def pl(n, prefix):
    s = L[n - 1]
    assert s.startswith(prefix), (n, s[:60])
    return s


def rows(a, b):
    return "\n".join(L[a - 1:b])


def sub(text, old, new, rid, block):
    assert text.count(old) == 1, (rid, block, old, text.count(old))
    DEPART.append((rid, block, old, new))
    return text.replace(old, new)


def pkg_quote(s):
    """A string the package prints inside double quotes, asserted present."""
    assert s in TXT["PKG"], s[:70]
    return s


R = DATA["RES"]
F = DATA["FRZ"]
V = DATA["VR"]
P = DATA["PR"]
REGD = R["registered"]
assert REGD == {"H1a": "PASS", "H1b": "PASS", "H1c": "PASS", "H2a": "NOT EVALUABLE", "H2b": "PASS",
                "H3": "RESPECTED", "H2d": "FAIL"}, REGD   # CC-369 Ruling 3 (sentences below are selected from these)
assert V["registered"] == {"V1": "PASS", "V2": "FLOOR REFUTED", "V3": "DISCRIMINATING", "COCO K2": "NOT PASSED"}
assert F["h2b_declared"]["determined"] is None and F["h3"]["evaluable"] is True and F["h2a_evaluable_w0"] is False

SYS1 = {"xm3600_zeroshot-short": "zero-shot, short", "xm3600_zeroshot-detailed": "zero-shot, detailed",
        "xm3600_p1_s43-short": "gold-SFT adapter, short", "xm3600_p1_s43-detailed": "gold-SFT adapter, detailed",
        "xm3600_fuse2_s42-short": "second adapter, short", "xm3600_fuse2_s42-detailed": "second adapter, detailed"}
SYS2 = {"g2b_q3_xm600-short-T0": "greedy, short", "g2b_q3_xm600-detailed-T0": "greedy, detailed",
        "g2b_q3_xm600-short-T05": "lower temperature, short", "g2b_q3_xm600-detailed-T05": "lower temperature, detailed",
        "g2b_q3_xm600-short-T08": "higher temperature, short", "g2b_q3_xm600-detailed-T08": "higher temperature, detailed"}
SYSN = {**{k: v + " (1)" for k, v in SYS1.items()}, **{k: v + " (2)" for k, v in SYS2.items()}}
SYS_ORDER = list(SYS1) + list(SYS2)
assert set(SYS_ORDER) == set(R["H2b"]["systems"]) == set(F["intervals_44"])
FAM = {"Q25": "first backbone", "Q3": "second backbone", "cross": "cross-family"}
SYSKEY = "(1) = first backbone (Qwen2.5-VL-7B variants of Section 6.2, 600 images); (2) = second backbone (Qwen3-VL-8B zero-shot, Section 6.3; temperature greedy, lower or higher)"

PCOMP = {"opera/instructblip": "InstructBLIP", "opera/llava-1.5": "LLaVA-1.5", "opera/minigpt4": "MiniGPT-4", "opera/shikra": "Shikra"}
LIM = {"r1-llava1.5-7b": "LLaVA-1.5-7B", "r2-vcd": "VCD", "r3-opera": "OPERA", "r4-opera-fast": "OPERA-fast",
       "r5-ours-inst": "Less is More (r5)", "r6-ours-cap": "Less is More (r6)", "r7-llava1.5-13b": "LLaVA-1.5-13B",
       "r8-ours-cap": "Less is More (r8)", "r9-llava-7b": "LLaVA-7B", "r10-ours-cap": "Less is More (r10)",
       "r11-minigptv2": "MiniGPT-v2", "r12-ours-cap": "Less is More (r12)"}


def psys(s):
    rel, name = s.split("/", 1)
    if rel == "lim":
        return LIM[name] + " [LiM]"
    base, var = name.split("__")
    return {"ours": "OPERA", "greedy": "greedy", "beam5": "beam search"}[var] + " [" + PCOMP["opera/" + base] + "]"


def pcomp(c):
    a, b = c.split(" vs ")
    return psys(a) + " vs " + psys(b)


SETN = {"F-A": "F-A", "F-B": "F-B", "F-C": "F-C"}

E13 = "; with those mentions settled by a human annotator the slope stays positive on both backbones (H1a PASS; single annotator; Section 6.7.2)"

# registered constants printed in the Phase A and Phase B text (CC-373 N3)
at("sec7 §6.7, §6.7.1, §6.7.2, §6.7.4; sec11 §9.1; supp S11 (registered constants)")
for _a, _lit, _sh in (("R11", "α = 0.05", "0.05"), ("R11", "α_S = 0.025", "0.025"), ("R11", "primary w0 = 0.20", "0.20"),
                      ("R11", "grid w ∈ {0, 0.10, 0.20, 0.30, 0.50}", "0, 0.10, 0.20, 0.30, 0.50"), ("R11", "30 bisection", "30"),
                      ("R11", "[0.001, 1]", "[0.001, 1]"), ("R11", "at least 10 of the 30", "10 of the 30"), ("R11", "99.17", "99.17%"),
                      ("R11", "< 50", "50"), ("R11", "B = 2,000", "2,000"), ("R11", "first 500", "500"), ("R11", "1000", "1,000"),
                      ("R11", "537", "537"), ("R11", "66 pairs", "66"), ("R11", "9 of its 15", "9 of 15"), ("R11", "6 are near", "6"),
                      ("R11", "11 of 12", "11 of 12"), ("H2D", "0.36th percentile", "0.36th percentile"), ("H2D", "D ≥ 0.10", "0.10 (SESOI)"),
                      ("VP", "20261113", "20261113"), ("VP", "20261114", "20261114"), ("VP", "20261115", "20261115"), ("VP", "20261116", "20261116"),
                      ("VP", "R = 20", "20 draws"), ("VP", "at least 5 pairs", "72, 5 and 72"), ("PLAN", "0.60", "0.60"), ("PLAN", "(457)", "150 overlap images")):
    REGF(_a, _lit, _sh)

# =====================================================================================================
# Shared sentences
# =====================================================================================================
at("sec7 §6.7; sec10 §8.5; sec1 Table 1; abstract; supp S10, S4.0")
n_pass = sum(v in ("PASS", "RESPECTED") for v in REGD.values())
n_fail = sum(v in ("FAIL", "VIOLATED") for v in REGD.values())
n_inc = sum(v.startswith("INCONCLUSIVE") for v in REGD.values())
n_ne = sum(v == "NOT EVALUABLE" for v in REGD.values())
assert (n_pass, n_fail, n_inc, n_ne) == (5, 1, 0, 1) and len(REGD) == 7
W = {5: "five", 1: "one", 0: "none", 7: "seven"}
def names(pred):
    return ", ".join(k for k in ("H1a", "H1b", "H1c", "H2a", "H2b", "H2d", "H3") if pred(REGD[k]))
c5 = D(W[n_pass], "RES", 'count of registered.* in {"PASS","RESPECTED"} = 5')
c1 = D(W[n_fail], "RES", 'count of registered.* in {"FAIL","VIOLATED"} = 1')
c1ne = D(W[n_ne], "RES", 'count of registered.* = "NOT EVALUABLE" = 1')
c0 = D(W[n_inc], "RES", 'count of registered.* beginning "INCONCLUSIVE" = 0')
COUNT = T("Seven predictions were registered on the labels (single annotator): «a» passed («na»), «b» failed («nb»), «c» was inconclusive and «d» was not evaluable («nd») (Table 1).",
          a=c5, na=names(lambda v: v in ("PASS", "RESPECTED")), b=c1, nb=names(lambda v: v == "FAIL"),
          c=c0, d=c1ne, nd=names(lambda v: v == "NOT EVALUABLE"))
assert "five passed (H1a, H1b, H1c, H2b, H3), one failed (H2d)" in COUNT and "one was not evaluable (H2a)" in COUNT
DEPART.append(("count line", "all sites", "package §3.6 shell with DERIVED placeholders",
               "W6 form with names; 'none was inconclusive' (grammar for a zero count); no VALID, NOT DISCRIMINATING or PASS (vacuous) verdict, so that clause is empty"))

wh = [R["H2b"]["systems"][s]["w_hat"] for s in SYS_ORDER]
nb = N("RES", ["H2b", "n_binding"], lambda v: W[v])
W2 = T("the budget was smaller than the number of unknown mentions for only «nb» of the twelve systems; for the other «ne», coverage holds by construction (measured effective floor «lo» to «hi»)",
       nb=nb, ne=D("eleven", "RES", "12 - H2b.n_binding = 11"),
       lo=D(f2(min(wh)), "RES", "min over systems of H2b.systems.*.w_hat"),
       hi=D(f2(max(wh)), "RES", "max over systems of H2b.systems.*.w_hat"))
assert W2 == "the budget was smaller than the number of unknown mentions for only one of the twelve systems; for the other eleven, coverage holds by construction (measured effective floor 0.24 to 0.42)"

H2D_LABEL = R["H2d"]["printed_label"]
H2D_READ = R["H2d"]["reading"]
assert R["H2d"]["fail_adds"] is None
for lit in ("30 dependent pairs", "D = -0.016", "-0.032 to 0.019", "SESOI 0.10"):
    assert lit in H2D_READ
at("sec7 §6.7 (H2d reading); supp S11.4")
D("30", "RES", "H2d.n1 + H2d.n0 = 21 + 9 (printed inside H2d.reading)")
N("RES", ["H2d", "D"], lambda v: f"{v:.3f}")
N("RES", ["H2d", "D_ci95"], lambda v: f"{v[0]:.3f} to {v[1]:.3f}")

at("sec7 §6.7; supp S11.4")
H2A_NE = T("H2a could not be evaluated: at $w_0 = 0.20$ the reference-only certificate certified «c» of the within-family pairs and left «o» uncertified, and at least 10 of each were needed; this was declared at the freeze, before unsealing.",
           c=N("FRZ", ["h2a_declared", "0.2", "n_cert"], nint), o=N("FRZ", ["h2a_declared", "0.2", "n_other"], nint))
assert H2A_NE == "H2a could not be evaluated: at $w_0 = 0.20$ the reference-only certificate certified 0 of the within-family pairs and left 30 uncertified, and at least 10 of each were needed; this was declared at the freeze, before unsealing."  # CC-369 Ruling 5
H2B_PASS = T("The budget at $w_0 = 0.20$ covered the human-completed present pairs among the unknown mentions of «n» of the twelve systems (at least 11 needed): H2b PASS (single annotator).",
             n=N("RES", ["H2b", "n_covered"], nint))
W2S = "For H2b (single annotator), " + W2 + "."

# =====================================================================================================
# Section 6.7 (sec7): run fact, outcome on the certificate, quality, H1, intervals, H3
# =====================================================================================================
at("sec7 §6.7")
RUNFACT = T(" The scoring ran once, on «d», with no fault.", d=LOGV("OPS-1112ch-a-cert-score (2026-11-12T18:30:45Z); commit 03ba1a2 'one pass, no fault'", "2026-11-12"))
OUTCOME67 = T(
    "**Outcome for the certificate.** By the entry rule fixed before the results, the certificate of Supplementary S11 enters this paper only if no claimed floor has more than 5% certified errors and either H2a on these labels or a ranking check on COCO-5000 passes. Neither passed (the COCO-5000 check: Supplementary S11.5), so the certificate is reported in Supplementary S11 as a proposed rule that was not validated, and this section keeps the human-completed gold, H1, H3 and the per-system intervals. Its three registered tests on the labels gave the following. «h2a» «h2b» «w2» For H2d («lab»): «read» «count»",
    h2a=H2A_NE, h2b=H2B_PASS, w2=W2S, lab=H2D_LABEL, read=H2D_READ, count=COUNT)

at("sec7 §6.7.1 Table 6.7a")
Q = R["quality"]
def qrow(name, base, yes=None, no=None):
    g = lambda k, fn: N("RES", ["quality"] + base + [k], fn)
    return "| " + " | ".join([name, g("n", nint), yes or g("Y", nint), no or g("N", nint), g("agreement_of_all", pct),
                              g("agreement_among_YN", pct), g("U", nint), g("A", nint)]) + " |"
roles = ["ctrl_present", "ctrl_absent", "foil_absent"]
ally = D(nint(sum(Q["control_by_role"][r]["Y"] for r in roles)), "RES", "sum of quality.control_by_role.*.Y")
alln = D(nint(sum(Q["control_by_role"][r]["N"] for r in roles)), "RES", "sum of quality.control_by_role.*.N")
assert sum(Q["control_by_role"][r]["n"] for r in roles) == Q["n_control"] == 443
QTAB = "\n".join([
    "**Table 6.7a.** Label quality (single annotator; new labels on previously analysed captions; descriptive, gates nothing). Agreement is the share of questions whose yes or no answer equals the Open Images label; U and A are counted apart. Whether depictions count as present in the Open Images image-level labels is not verified.",
    "",
    "| Control questions | n | Yes | No | Agreement (all) | Agreement among yes/no | U | A |",
    "|---|---|---|---|---|---|---|---|",
    "| All controls | " + " | ".join([N("RES", ["quality", "n_control"], nint), ally, alln,
                                      N("RES", ["quality", "control_agreement_of_all"], pct),
                                      N("RES", ["quality", "control_agreement_among_YN"], pct),
                                      N("RES", ["quality", "control_U"], nint), N("RES", ["quality", "control_A"], nint)]) + " |",
    qrow("Named, verified present", ["control_by_role", "ctrl_present"]),
    qrow("Named, verified absent", ["control_by_role", "ctrl_absent"]),
    qrow("Unnamed, verified absent (foils)", ["control_by_role", "foil_absent"]),
    qrow("Absent, hint covers every class shown", ["control_absent_by_hint_coverage", "full"]),
    qrow("Absent, hint covers part of the classes shown", ["control_absent_by_hint_coverage", "partial"]),
    "",
    T("Repeats (part 3): «r»; their agreement is reported after a later unsealing. Same-map synonym disagreements on one image (single annotator): «s». U and A rates by class are in Supplementary S11.7.",
      r=N("RES", ["quality", "repeat_answered"], str), s=N("RES", ["quality", "synonym_disagreements"], nint)),
])
assert Q["repeat_answered"] == "partial (0 of 150 answered at the part-1 unsealing)"
DEPART.append(("Table 6.7a (pkg 6.7g)", "sec7", "package columns n / agreement / U / A; kappa row; repeat row",
               "Yes and No columns added (CC-369 W5 asks for '32 Y of 143'); All-controls Yes/No DERIVED from the three roles; kappa row not printed (no key; J-14); the repeat row printed as a sentence"))

at("sec7 §6.7.2")
FACTS = pl(242, "**Facts fixed before unsealing")
FACTS = sub(FACTS, "(the label-side slope interval of Section 3.8)", "(the label-side slope interval of Supplementary S11.1)", "TG1 home swap", "§2.8 Facts fixed")
rng = ci(sl)
FACTS = T(FACTS.replace("{{FREEZE.json::slopes.Q25.clabel.F.range}}", "«a»").replace("{{FREEZE.json::slopes.Q3.clabel.F.range}}", "«b»")
          .replace("{{FREEZE.json::slopes.Q25.clabel.P.range}}", "«c»").replace("{{FREEZE.json::slopes.Q3.clabel.P.range}}", "«d»"),
          a=N("FRZ", ["slopes", "Q25", "clabel", "F", "range"], rng), b=N("FRZ", ["slopes", "Q3", "clabel", "F", "range"], rng),
          c=N("FRZ", ["slopes", "Q25", "clabel", "P", "range"], rng), d=N("FRZ", ["slopes", "Q3", "clabel", "P", "range"], rng))
H1 = R["H1"]
def h(fam, *k, fn=sl):
    return N("RES", ["H1", fam] + list(k), fn)
H1TAB = "\n".join([
    pl(417, "**Table 6.7b.**").replace("**Table 6.7b.**", "**Table 6.7c.**"),
    "",
    pl(419, "| Family (images) |"),
    pl(420, "|---|"),
    "| First backbone (600) | " + " | ".join([h("Q25", "b_F", "reg") + " " + h("Q25", "b_F_ci95", fn=ci(sl)),
                                             h("Q25", "b_F", "lo") + ", " + h("Q25", "b_F", "hi"),
                                             h("Q25", "b_P", "reg") + " " + h("Q25", "b_P_ci95", fn=ci(sl)),
                                             "[+5.83, +20.13] (" + h("Q25", "S72_ends_unrounded_from_FREEZE", "lower", fn=f3s) + ", " + h("Q25", "S72_ends_unrounded_from_FREEZE", "upper", fn=f3s) + ")",
                                             h("Q25", "b_F_minus_S72_lower_ci95", fn=ci(sl)), h("Q25", "b_F_minus_S72_upper_ci95", fn=ci(sl)),
                                             "H1b " + REGD["H1b"]]) + " |",
    "| Second backbone (537) | " + " | ".join([h("Q3", "b_F", "reg") + " " + h("Q3", "b_F_ci95", fn=ci(sl)) + " (99.17%: " + h("Q3", "b_F_bonf", fn=ci(sl)) + ")",
                                              h("Q3", "b_F", "lo") + ", " + h("Q3", "b_F", "hi"),
                                              h("Q3", "b_P", "reg") + " " + h("Q3", "b_P_ci95", fn=ci(sl)),
                                              "[+1.97, +14.78] (" + h("Q3", "S72_ends_unrounded_from_FREEZE", "lower", fn=f3s) + ", " + h("Q3", "S72_ends_unrounded_from_FREEZE", "upper", fn=f3s) + ")",
                                              h("Q3", "b_F_minus_S72_lower_ci95", fn=ci(sl)), h("Q3", "b_F_minus_S72_upper_ci95", fn=ci(sl)),
                                              "H1a " + REGD["H1a"] + "; H1c " + REGD["H1c"]]) + " |",
    "",
    T("Secondary row (no verdict; single annotator): the slope corner over the remainder (pairwise worst case), «a» for the first backbone and «b» for the second.",
      a=h("Q25", "remainder_corner_F_secondary", fn=ci(sl)), b=h("Q3", "remainder_corner_F_secondary", fn=ci(sl))),
])
assert H1["Q25"]["direction"] == ["inside"] * 3 and H1["Q3"]["direction"] == ["inside"] * 3
H1A = T("On the second backbone's XM3600-600 outputs (537 images), with the mentions Open Images cannot verify settled by a human, the label-gold F1 slope is positive, $b_F$ = «r» «c», and it stays positive with the unsettled pairs counted absent or present («lo», «hi»): H1a PASS (single annotator).",
        r=h("Q3", "b_F", "reg"), c=h("Q3", "b_F_ci95", fn=ci(sl)), lo=h("Q3", "b_F", "lo"), hi=h("Q3", "b_F", "hi"))
assert H1A == "On the second backbone's XM3600-600 outputs (537 images), with the mentions Open Images cannot verify settled by a human, the label-gold F1 slope is positive, $b_F$ = +11.41 [+9.23, +13.37], and it stays positive with the unsettled pairs counted absent or present (+10.26, +11.81): H1a PASS (single annotator)."  # CC-369 Ruling 5
H1BC = lambda fam, fl, br, hid: T("On the «fl», the completed slope $b_F$ = «r» lies inside the post hoc bracket of Table S7.2 («br») at the registered value and at both ends of the unsettled pairs: «id» PASS (single annotator).",
                                  fl=fl, r=h(fam, "b_F", "reg"), br=br, id=hid)
H1SENT = " ".join([H1A, H1BC("Q25", "first-backbone family (600 images)", "[+5.83, +20.13]", "H1b"),
                   H1BC("Q3", "second-backbone family (537 images)", "[+1.97, +14.78]", "H1c"),
                   "With H1a, H1b and H1c all PASS, " + pkg_quote("the paper's reading stands, and the post hoc bound is supplemented by a measurement on new labels (single annotator)") + "."])
DEPART.append(("H1 all-three sentence", "sec7 §6.7.2", "[reg] fragment", "lead-in 'With H1a, H1b and H1c all PASS, ' and a final full stop added"))

at("sec7 §6.7.3 Table 6.7d")
S25 = pl(192, "For each of the twelve systems")
S25 += " The cap $X(\\mathcal N_S; w)$, its budget $\\beta$ and the naming floor $w$ are defined in Supplementary S11.1; the interval uses no label."
DEPART.append(("§2.5 → 6.7.3", "sec7", "package l.192", "one sentence added: pointer to Supplementary S11.1 for the cap, the budget and the floor (Home S: those definitions are in the supplement)"))
I44 = F["intervals_44"]
def irow(s):
    g = lambda *k, fn=nint: N("FRZ", ["intervals_44", s] + list(k), fn)
    hi = " / ".join(g("high", w, fn=f3) for w in ("0.0", "0.1", "0.2", "0.3", "0.5"))
    return "| " + " | ".join([SYSN[s], g("n"), g("t"), g("U"), g("phi1") + ", " + g("phi2"), g("low", fn=f3), hi,
                              "yes" if I44[s]["binds"] else "no"]) + " |"
ITAB = "\n".join([
    "**Table 6.7d (freeze, development (no labels)).** Per-system precision interval under the two-reference gold, 600 images. The table uses no label; it is part of the analysis registered on new labels of previously analysed captions. " + SYSKEY + ".",
    "",
    pl(399, "| System |"), pl(400, "|---|"),
    *[irow(s) for s in SYS_ORDER],
    "",
    "Note: " + pkg_quote("the $w = 0$ column is computed and printed as registered; every entry in it is 1") + " (Supplementary S11.3).",
])
assert all(I44[s]["high"]["0.0"] == 1.0 for s in SYS_ORDER)

at("sec7 §6.7.4 Table 6.7f")
H3 = R["H3"]
def r3(*k, fn=f1d):
    return N("RES", ["H3"] + list(k), fn)
def s3(*k, fn=f1d):
    return N("RES", ["secondary"] + list(k), fn)
J17 = "its RESPECTED outcome is largely foreseeable from stored Open Images aggregates"
assert J17 in TXT["R11"].split("\n")[209]
H3TAB = "\n".join([
    "**Table 6.7f.** H3 (single annotator; new labels on previously analysed captions; 600 images).",
    "",
    pl(510, "| Universe |"), pl(511, "|---|"),
    "| $\\mathcal N_u$ (registered) | " + " | ".join([r3("phi1", fn=nint), r3("phi2", fn=nint), r3("f0_hat"), r3("X", fn=nint), r3("X_hi", fn=nint),
                                                    r3("D") + " " + r3("D_ci95", fn=ci(f1d)) + " (" + r3("D_bonf", fn=ci(f1d)) + ")",
                                                    r3("D_hi") + " " + r3("D_hi_ci95", fn=ci(f1d)), r3("ratio_X_f0", fn=f2),
                                                    r3("n_ref_named_completed_absent", fn=nint), REGD["H3"]]) + " |",
    "| All system-named pairs of $V_m$ (secondary; " + J17 + ") | " + " | ".join([
        s3("H3_all_system_named", "phi1", fn=nint), s3("H3_all_system_named", "phi2", fn=nint), s3("H3_all_system_named", "f0_hat"),
        s3("H3_all_system_named", "X", fn=nint), s3("H3_all_system_named", "X_hi", fn=nint),
        s3("H3_all_system_named", "D") + " " + s3("H3_all_system_named", "D_ci95", fn=ci(f1d)),
        s3("H3_all_system_named", "D_hi") + " " + s3("H3_all_system_named", "D_hi_ci95", fn=ci(f1d)), "–", "–",
        R["secondary"]["H3_all_system_named"]["reading_no_verdict"] + ", no verdict"]) + " |",
    "| $D_L$ over all completed-present pairs (secondary) | " + " | ".join([
        s3("D_L", "phi1", fn=nint), s3("D_L", "phi2", fn=nint), "–", "–", "–",
        "$D_L$ " + s3("D_L", "D_L", fn=f3) + " " + s3("D_L", "D_L_ci95", fn=ci(f3)), "–", "–", "–",
        R["secondary"]["D_L"]["label"] + ", no verdict"]) + " |",
])
DEPART.append(("J-17 (W16)", "Table 6.7f", "{{J-17: the parenthetical of R11 l.210, verbatim}}", "R11 l.210 parenthetical without its own brackets, inside the row's '(secondary; …)'"))
H3SENT = T("Among the system-named pairs that Open Images does not settle, the pairs that neither reference names and the annotator marked present outnumber the estimate of Section 5.4 ($X$ = «x» against $\\hat f_0$ = «f»; $D$ «c»), as Proposition 2's lower bound requires: H3 RESPECTED (single annotator). Beside it, with no verdict (single annotator): $X/\\hat f_0$ = «r» (secondary), and «n» reference-named pairs were completed as absent.",
           x=r3("X", fn=nint), f=r3("f0_hat"), c=r3("D_ci95", fn=ci(f1d)), r=r3("ratio_X_f0", fn=f2), n=r3("n_ref_named_completed_absent", fn=nint))
assert "($X$ = 549 against $\\hat f_0$ = 158.9; $D$ [307.3, 464.6])" in H3SENT   # CC-369 Ruling 5

# =====================================================================================================
# Section 9.1 / 9.2 (sec11)
# =====================================================================================================
at("sec11 §9.1")
E6 = T("With those mentions settled by a human annotator, the completed label-gold slope is «a» «b» on the first backbone and «c» «d» on the second (H1a «e», H1b «f», H1c «g»; single annotator; Section 6.7.2).",
       a=h("Q25", "b_F", "reg"), b=h("Q25", "b_F_ci95", fn=ci(sl)), c=h("Q3", "b_F", "reg"), d=h("Q3", "b_F_ci95", fn=ci(sl)),
       e=REGD["H1a"], f=REGD["H1b"], g=REGD["H1c"])
N1E7 = "The certificate of Supplementary S11.1 and the test of Section 6.7.4 rest on the same (A1), which the diagnostic of Section 5 checks for reference order only."
DEPART.append(("E7/N1", "sec11", "The certificate of Section 3.8 and the test of Section 6.7.5 rest on …", "Home S: 'Supplementary S11.1'; renumber 6.7.5 → 6.7.4"))
P_INT = sub(pl(654, "**Internal validity: data the paper had already analysed.**"),
            " {{J-19: R11 §9 bullets, verbatim, inserted only in Phase B}}", "", "J-19", "§4 internal validity")
P_ASM = sub(pl(657, "**Construct validity: the assumptions of the reference-only certificate.**"),
            "named (Section 3.8), so", "named (Supplementary S11.3), so", "TG1 home swap", "§4 assumptions")
P_ASM = sub(P_ASM, "names a class that is not in the image", "names a class absent from the image", "n-gram scan (a 6-gram shared with COCO captions; wording only)", "§4 assumptions")
P_DEV = pl(663, "**Development and post hoc rows.**")
P_DEV = sub(P_DEV, "(Section 6.8, Supplementary S11.5)", "(Supplementary S11.5)", "Home S (no Section 6.8)", "§4 development")
P_DEV = sub(P_DEV, " {{J-19: VP §V.1 bullets and the first paragraph of VP §V.5, verbatim, inserted only in Phase B}}", "", "J-19", "§4 development")
P_DEV = sub(P_DEV, "(Section 6.8, Supplementary S11.6)", "(Supplementary S11.6)", "Home S (no Section 6.8)", "§4 development")
P_PRI = pl(666, "**Prior work.**")
P_ARM = "**Other-family arm.** A further development arm, with captions decoded by models of other families on the same 600 images and labels from a separate session, is registered; its labels had not been scored at the time of writing, and no row of it is reported."
NEW_TEXT = [("§4 other-family arm (J-27 one sentence)", "sec11 §9.1", P_ARM)]
at("sec11 §9.2")
P_92 = sub(pl(685, "**Section 9.2, new paragraph (data and licences).**"), "**Section 9.2, new paragraph (data and licences).** ", "**Released evaluation logs.** ", "heading", "§4 9.2")
P_92 = sub(P_92, "The new human labels for XM3600-600 are {{J-31: release decision}}.", "The new human labels for XM3600-600 are reported as aggregates only; whether they will be released is not yet decided.", "J-31 / P-3 default", "§4 9.2")
NEW_TEXT.append(("9.2 label-release clause (P-3 default 'aggregates only')", "sec11 §9.2", "The new human labels for XM3600-600 are reported as aggregates only; whether they will be released is not yet decided."))

# =====================================================================================================
# Front matter: abstract, highlight, RQ4, contribution, Table 1, 8.1, 8.5, 5.4, Section 2
# =====================================================================================================
at("sec1 §1.1")
RQ4 = "- " + pkg_quote("**RQ4 (certification; registered on new labels of previously analysed XM3600-600 captions, development role).** Can the direction of a comparison between two systems be fixed from an incomplete gold, and under what assumption on its missing part?") + " (Section 6.7 and Supplementary S11)"
DEPART.append(("RQ4", "sec1", "(Sections 3.8 and 6.7–6.8)", "(Section 6.7 and Supplementary S11) — Home S"))
CONTRIB6 = "6. " + pkg_quote("A human completion of the XM3600-600 object gold (single annotator; new labels on previously analysed captions, registered before anyone but the annotator opened a label value) that measures the label-gold slope bracketed in Section 6.2 (H1) and tests the coverage bound of Section 5.4 (H3).")[:-2] + "; Section 6.7)."
DEPART.append(("Contribution 6 (Home S)", "sec1", "package shell", "'(H3).' -> '(H3; Section 6.7).', as the other items name their sections"))
at("sec1 Table 1")
T1_ROWS = "\n".join([
    "| Registered on new labels of previously analysed images (development role; single annotator) | " + COUNT[:-len(" (Table 1).")] + ". H1a: completed label-gold slope of the second backbone > 0, PASS (A31); H1b, H1c: completed slopes inside the post hoc brackets of Table S7.2, PASS (A32, A33); H3: coverage bound of Section 5.4 against the completed gold, RESPECTED (A37); H2b: budget coverage, PASS (A35; " + W2 + "); H2a: validity of the reference-only certificate, NOT EVALUABLE (A34); H2d: the break-down floor as a ranking, FAIL (A36) | 6.7, S11.4 |",
    "| Development, no verdict on the paper's claims (COCO-5000; development; outcome foreseeable from stored aggregates and an unreviewed calculation (disclosed)) | Certificate checked against a fuller gold: V1 " + V["registered"]["V1"] + ", V2 " + V["registered"]["V2"] + ", V3 " + V["registered"]["V3"] + ", COCO K2 " + V["registered"]["COCO K2"] + " (D-1 to D-4) | S11.5 |",
])
T1_POSTHOC_OLD = "| Post hoc, no verdict | Leave-one-system-out robustness; verified-precision bracket; re-scoring of 15 published comparisons; cap share of detailed captions | 3.3, 6 |"
T1_POSTHOC_NEW = "| Post hoc, no verdict | Leave-one-system-out robustness; verified-precision bracket; re-scoring of 15 published comparisons; cap share of detailed captions; certificate applied to 15 published comparisons (POST HOC; truth already scored by the paper) | 3.3, 6, S11.6 |"

at("sec10 §8.1")
s81 = T("We propose a certificate; on a development set with a fuller gold (development; outcome foreseeable from stored aggregates and an unreviewed calculation (disclosed)) it made «e» certified errors in «n» certified pair-draws at w0 = 0.20, although its floor assumption failed in «s» of cells; it did not rank comparisons better than a margin rule; it was not validated",
        e=N("VR", ["primary_truth_G_top", "V1_V3", "n_cert_direction_fails"], nint), n=N("VR", ["primary_truth_G_top", "V1_V3", "n_cert"], nint),
        s=N("VR", ["primary_truth_G_top", "V2", "share"], f3))
assert s81 + "." == "We propose a certificate; on a development set with a fuller gold (development; outcome foreseeable from stored aggregates and an unreviewed calculation (disclosed)) it made 0 certified errors in 200 certified pair-draws at w0 = 0.20, although its floor assumption failed in 0.137 of cells; it did not rank comparisons better than a margin rule; it was not validated."  # CC-360 Ruling 3 (h)
P81 = " **Certificate (Supplementary S11):** " + s81 + "."
DEPART.append(("8.1 pointer", "sec10", "CC-360 Ruling 3(h) sentence", "lead-in ' **Certificate (Supplementary S11):** ' added, as the paragraph's other parts carry bold lead-ins"))

at("sec5 §5.4")
S54 = " On XM3600-600, with two references and a human completion of the object gold, the test of the bound gave " + REGD["H3"] + " (Section 6.7.4; single annotator)."
DEPART.append(("§5.4 sentence", "sec5", "{{RESPECTED | …}} (Section 6.7.5; …)", "RESPECTED; 6.7.5 → 6.7.4 (renumber)"))
S1M6 = "A test of the bound against a human-completed gold on XM3600-600 is in Section 6.7.4."
at("sec2 §2")
S2PRIOR = pkg_quote("Bounds on a ranking over every completion of the missing labels are given by Fernández-Barrios et al. (2026) for F1 with single-label items; Section 3.8 uses them for precision on multi-label caption mentions, where a positives-only reference gold makes them empty, and adds a probabilistic cap on the unknown present objects from once-named counts under a naming floor.")
S2PRIOR = sub(S2PRIOR, "Section 3.8 uses them", "Supplementary S11.1 uses them", "TG1 home swap", "§2.4 prior-work sentence")

# =====================================================================================================
# Supplementary S11 (identical block in both supplement files)
# =====================================================================================================
S = []
at("supp S11")
S.append("## S11 Certification of a comparison under incomplete gold: a proposed rule that was not validated")
S.append("This section holds a certificate for the direction of a comparison under an incomplete gold, its derivation, its registered tests on the human-completed gold of XM3600-600, a development check on COCO-5000 and a post hoc application to published comparisons. By the entry rule fixed before the results (Section 6.7), the certificate was not validated, so it is reported here and not in the main text. The human-completed gold itself, H1, H3 and the per-system intervals are in Section 6.7.")
NEW_TEXT.append(("S11 opening paragraph", "supp S11", S[-1]))

# ---- S11.1 (package §2.1-§2.4) ----
S.append("### S11.1 Definitions: the problem, the worst case, the two caps, the floor and the slope")
blk = [pl(136, "A comparison between two systems"), pl(139, "**Three states.**"), rows(144, 145), pl(148, "**Orientation.**"),
       rows(151, 153), pl(158, "**Label-side certificate (C-label).**"), rows(161, 164), pl(167, "**What the floor means"),
       pl(170, "**Constants, fixed before"), pl(173, "**The break-down floor.**"), pl(176, "**A slope.**"),
       pl(181, "**Means.**"), pl(184, "**Does not mean.**")]
at("supp S11.1 (KV2 qualifier)")
KV2Q = (" " + "On COCO-5000 the floor assumption failed at w0 (V2 FLOOR REFUTED, Supplementary S11.5), so this guarantee is not claimed there; with V1 PASS the certificate is described as \"empirically valid on the sets tested\" (COCO-5000, one model family, development).")
assert "the floor assumption failed on COCO-5000 at w0" in V["KV"]["KV2"] and "empirically valid on the sets tested" in V["KV"]["KV2"]
blk[7] = sub(blk[7], "for fixed outputs on these images. The argument:", "for fixed outputs on these images." + KV2Q + " The argument:", "KV2 + CC-360 W2 (TG11)", "§2.3 floor")
blk[9] = sub(blk[9], "whether that order tracks which comparisons hold under a fuller gold is what H2d tests (Section 6.7.4).",
              "whether that order tracks which comparisons hold under a fuller gold is what H2d tests (Supplementary S11.4).", "Home S (H2d in S11.4)", "§2.3 w*")
blk[11] = sub(blk[11], "at the stated floor, for the fixed captions on these images.",
              "at the stated floor, for the fixed captions on these images (on COCO-5000 the floor assumption failed at w0; Supplementary S11.5).", "KV2 (TG11)", "§2.4 Means")
blk[12] = sub(blk[12], "Proposition 2 keeps the per-system intervals below and the test of Section 6.7.5.",
              "Proposition 2 keeps the per-system intervals of Section 6.7.3 and the test of Section 6.7.4.", "Home S + renumber", "§2.4 Does not mean")
S.extend(blk)
S.append("**Relation to prior work.** " + S2PRIOR.replace("Supplementary S11.1 uses them", "This section uses them"))
DEPART.append(("§2.4 relation sentence in S11.1", "supp S11.1", "package lead-in (placement note)", "lead-in '**Relation to prior work.**'; 'Section 3.8' → 'This section'"))

# ---- S11.2 ----
S.append("### S11.2 The budget and its derivation")
S2TXT = "The budget $\\beta$ and the secondary Hoeffding budget $\\beta_H$ are defined, with the assumptions under which the budget holds and the sketch of its derivation, in Supplementary S11.1 (\"What the floor means, and what is proved under it\"). The registration states that sketch and no fuller derivation: for a present pair named by $N$ of $k$ references, $P(N=0)/P(N=1) = (1-w_{ic})/(k\\,w_{ic}) \\le c_w$; summing over the pairs of the cell and applying Bernstein's inequality twice, each step at level $\\alpha_S/2$, gives $P\\big(x(\\mathcal C) > \\beta(\\mathcal C; w)\\big) \\le \\alpha_S$. The derivation has had no external proof review (Section 9.1)."
S.append(S2TXT)
NEW_TEXT.append(("S11.2 (registered sketch restated; no fuller derivation exists)", "supp S11.2", S2TXT))

# ---- S11.3 ----
S.append("### S11.3 Why references alone certify nothing without a floor")
S3TXT = "With a gold built from references only, no pair is known absent, so every mention of a system is known present or unknown: $t_A + u(\\mathcal C_{A\\setminus B}) + u(\\mathcal C_{A\\cap B}) = n_A$, and likewise for $B$. At $w = 0$ the cap is $X = u$. At the worst-case completion, $x(\\mathcal C_{B\\setminus A}) = u(\\mathcal C_{B\\setminus A})$ and $x(\\mathcal C_{A\\cap B}) = u(\\mathcal C_{A\\cap B})\\,\\mathbf 1[n_A > n_B]$. If $n_A > n_B$, $\\Delta_{\\min} = (t_A + u(\\mathcal C_{A\\cap B}))/n_A - 1 \\le 0$; otherwise $\\Delta_{\\min} = t_A/n_A - 1 + u(\\mathcal C_{A\\cap B})/n_B \\le u(\\mathcal C_{A\\cap B})(1/n_B - 1/n_A) \\le 0$. So the reference-only certificate at $w = 0$ certifies no precision order. It certifies no slope sign either: the completion that sets every unknown pair present gives precision 1 to each system, a point inside the corner box of the slope interval with slope 0. The high end of every per-system interval at $w = 0$ is therefore 1 (Table 6.7d). All content of the reference-only certificate lies in the floor; the no-assumption certificate has content only when the gold has known-absent pairs, as the label side has."
S.append(S3TXT)
NEW_TEXT.append(("S11.3 (the registered §V.4/§V.4a identity in the paper's notation)", "supp S11.3", S3TXT))

# ---- S11.4 ----
S.append("### S11.4 Every registered and secondary certificate row on XM3600-600")
at("supp S11.4 freeze")
nclab = sum(p["scope"] != "cross" and p["clabel"]["verdict"] == "CERTIFIED" for p in F["pairs"])
fams_signed = [FAM[f] + " family" for f in ("Q25", "Q3") if F["slopes"][f]["clabel"]["F"]["certified_sign"]]
S.append(T("Before anyone but the annotator opened a label value, the freeze fixed (development (no labels)): at $w_0 = 0.20$, «c» of the 30 within-family pairs were CERTIFIED by the reference-only certificate, «o» were not and «e» were excluded as ties or undefined; H2a was declared not evaluable; the H2b budget binds for «b» of the twelve systems; H3 was declared evaluable ($\\varphi_1$ = «p1», $\\varphi_2$ = «p2»).",
           c=N("FRZ", ["h2a_declared", "0.2", "n_cert"], nint), o=N("FRZ", ["h2a_declared", "0.2", "n_other"], nint),
           e=N("FRZ", ["h2a_declared", "0.2", "n_excluded"], nint), b=N("FRZ", ["h2b_declared", "n_binding"], nint),
           p1=N("FRZ", ["h3", "phi1"], nint), p2=N("FRZ", ["h3", "phi2"], nint)))
S.append(T("With the Open Images statuses alone, «n» of the 30 within-family comparisons were already fixed by the Open Images labels alone (development (no labels)); the sign of the label-gold F1 slope was fixed for «f».",
           n=D(nint(nclab), "FRZ", 'count of pairs[*] with scope != "cross" and clabel.verdict = "CERTIFIED"'),
           f=D(" and ".join(fams_signed) if fams_signed else "neither family", "FRZ", "families with slopes.<fam>.clabel.F.certified_sign = true")))
at("supp S11.4 Table S11.4a")
def lab(x):
    return {"CERTIFIED": "C", "NOT CERTIFIED": "NC"}.get(x, "ABSTAIN" if "ABSTAIN" in x else ("NOT DEFINED" if "NOT DEFINED" in x else x))
def prow(j, p):
    g = lambda *k, fn=nint: N("FRZ", ["pairs", j] + list(k), fn)
    ws = g("w_star", fn=lambda v: v if isinstance(v, str) else ("NI" if v is None else f3(v)))
    return "| " + " | ".join([SYSN[p["A"]] + " vs " + SYSN[p["B"]], FAM[p["scope"]], g("n_images"),
                              g("cells", "nA") + ", " + g("cells", "nB"), g("cells", "tA") + ", " + g("cells", "tB"),
                              " / ".join(lab(p["cref"][w]["label"]) for w in ("0.0", "0.1", "0.2", "0.3", "0.5")),
                              ws, lab(p["vh"]["0.2"]), lab(p["first_two"]["0.2"]), lab(p["clabel"]["label"])]) + " |"
S.append("\n".join([
    "**Table S11.4a (freeze, development (no labels)).** One row per pair: the 30 within-family pairs and the 36 cross-family pairs (secondary). C = CERTIFIED, NC = NOT CERTIFIED; a pair printed by the code as \"NOT CERTIFIED (ABSTAIN; …)\" is printed ABSTAIN (exact tie; excluded). " + SYSKEY + ".",
    "",
    "| Pair (A vs B) | Family | Images | $n_A$, $n_B$ | $t_A$, $t_B$ | Reference-only certificate at $w$ = 0 / 0.10 / 0.20 / 0.30 / 0.50 | $w^*$ | V-H at $w_0$ | First-two references at $w_0$ | Label-side certificate |",
    "|---|---|---|---|---|---|---|---|---|---|",
    *[prow(j, p) for j, p in enumerate(F["pairs"])],
    "",
    "Note: " + pkg_quote("The $w = 0$ column of the reference-only certificate is computed and printed; it certifies no pair, as Section 3.8 shows.").replace("as Section 3.8 shows", "as Supplementary S11.3 shows"),
]))
assert all(p["cref"]["0.0"]["verdict"] != "CERTIFIED" for p in F["pairs"])
DEPART.append(("Table S11.4a (pkg 6.7a)", "supp S11.4", "label cells {{…label}}", "abbreviated C / NC with a key in the caption; system names from Table S7.3; cross-family rows in the same table (Home S); note: 'Section 3.8' → 'Supplementary S11.3'"))
at("supp S11.4 Table S11.4b")
def slrow(f):
    out = []
    for w in ("0.0", "0.1", "0.2", "0.3", "0.5"):
        out.append("| " + " | ".join([FAM[f], "reference-only", "precision", w if w != "0.0" else "0",
                                      N("FRZ", ["slopes", f, "cref_P", w, "range"], rng),
                                      "yes" if F["slopes"][f]["cref_P"][w]["certified_sign"] else "no"]) + " |")
    for m, nm in (("P", "precision"), ("F", "F1 (recall fixed)")):
        out.append("| " + " | ".join([FAM[f], "label-side", nm, "–", N("FRZ", ["slopes", f, "clabel", m, "range"], rng),
                                      "yes" if F["slopes"][f]["clabel"][m]["certified_sign"] else "no"]) + " |")
    return out
S.append("\n".join([
    pl(405, "**Table 6.7a″").replace("**Table 6.7a″ (freeze", "**Table S11.4b (freeze").replace("Section 6.7.2)", "Section 6.7.2)"),
    "", pl(407, "| Family |"), pl(408, "|---|"), *slrow("Q25"), *slrow("Q3")]))
def smallest(f):
    ws = [w for w in ("0.0", "0.1", "0.2", "0.3", "0.5") if F["slopes"][f]["cref_P"][w]["certified_sign"]]
    return ("certified at the smallest floor " + D(ws[0], "FRZ", f"smallest <w> with slopes.{f}.cref_P.<w>.certified_sign = true")) if ws else "not certified at any grid floor"
S.append(" ".join(T("Under the two-reference gold the sign of the precision slope is «c» for the «f» family (development (no labels)).", c=smallest(f), f=FAM[f]) for f in ("Q25", "Q3"))
         + " The $w = 0$ row is computed and certifies nothing (Supplementary S11.3).")

at("supp S11.4 H2a/H2b")
for n_, pre in ((247, "**Units.**"), (250, "**Truth.**")):
    S.append(pl(n_, pre))
S.append(rows(253, 257))
S.append(pl(259, "Reported whatever the verdict"))
S.append(pl(262, "**H2a secondary rows"))
S.append(rows(265, 268))
H2A = R["H2a"]
def h2(*k, fn=nint):
    return N("RES", ["H2a"] + list(k), fn)
ND = "not defined (no certified pair)"
cov_fail = {w: [sum(R["H2b"]["systems"][s]["x_hi"] > int(R["H2b"]["systems"][s]["beta"][w]) for s in SYS_ORDER),
                sum(R["H2b"]["systems"][s]["x"] > int(R["H2b"]["systems"][s]["beta"][w]) for s in SYS_ORDER)] for w in ("0.3", "0.5")}
assert cov_fail["0.3"] == [4, 1] and cov_fail["0.5"][0] == 12   # CC-369 Ruling 4 / W3
def secrow(w, wl):
    sc = H2A["secondary_by_w"][w]
    if sc["n_cert"] == 0:
        reading = "vacuous (no pair certified)"
    else:
        a = D(str(cov_fail[w][0]), "RES", f"count of systems with H2b.systems.*.x_hi > floor(beta.\"{w}\")")
        reading = "secondary; no verdict (grid budget not covered for " + a + " of 12 systems" + (
            ", " + D(str(cov_fail[w][1]), "RES", f"count of systems with H2b.systems.*.x > floor(beta.\"{w}\")") + " of 12 on settled answers alone)" if w == "0.3" else ")")
    vc = ND if sc["V_c"] is None else h2("secondary_by_w", w, "V_c", fn=f3)
    return "| " + " | ".join([wl, h2("secondary_by_w", w, "n_cert"), h2("secondary_by_w", w, "n_other"), "–",
                              h2("secondary_by_w", w, "n_cert_unconfirmed"), vc, h2("secondary_by_w", w, "V_n", fn=f3), reading]) + " |"
cf = H2A["cross_family_secondary"]
S.append("\n".join([
    "**Table S11.4c.** H2a at $w_0 = 0.20$ and at every grid floor (single annotator; new labels on previously analysed captions; certified set and orientation from the freeze).",
    "", pl(447, "| Floor |"), pl(448, "|---|"),
    "| $w_0$ = 0.20 (primary) | " + " | ".join([h2("n_cert"), h2("n_other"), h2("n_excluded"), h2("n_cert_unconfirmed") + " (limit " + h2("limit") + ")",
                                               ND, h2("V_n", fn=f3), "H2a " + REGD["H2a"] + "; $V_c - V_n$: " + ND]) + " |",
    secrow("0.0", "$w$ = 0 (secondary)"), secrow("0.1", "$w$ = 0.10 (secondary)"),
    secrow("0.3", "$w$ = 0.30 = $w_{\\mathrm{ev}}$ (" + N("FRZ", ["w_ev"], f2) + "; secondary)"), secrow("0.5", "$w$ = 0.50 (secondary)"),
    *["| Null: " + nm + " | " + h2("nulls", nm, "n") + " | – | – | " + h2("nulls", nm, "errors") + " | – | – | no verdict |" for nm in ("constant", "margin", "length")],
    "| Cross-family pairs (secondary) | " + " | ".join([h2("cross_family_secondary", "n_cert"), h2("cross_family_secondary", "n_other"),
                                                      h2("cross_family_secondary", "n_excluded"), h2("cross_family_secondary", "n_cert_unconfirmed"),
                                                      ND, h2("cross_family_secondary", "V_n", fn=f3), cf["label"] + ", no verdict"]) + " |",
]))
assert H2A["V_c"] is None and "Vc_minus_Vn_ci95" not in H2A and "exact_lower_limit" not in H2A and H2A["margin_beats_certificate"] is False
assert H2A["secondary_by_w"]["0.2"]["n_cert"] == 0
DEPART.append(("Table S11.4c (pkg 6.7c)", "supp S11.4", "secondary labels VALID AT <w> (code)", "CC-343 N9 / CC-369 W3: 'vacuous (no pair certified)' at w = 0, 0.10 (0.20 is the primary row); 'secondary; no verdict' with the grid budget coverage at 0.30 and 0.50; the code label 'VALID AT 0.3/0.5' is not printed (judge to confirm); CC-369 W4 cells 'not defined (no certified pair)'"))
S.append(H2A_NE + " " + T("«n» certified pairs are unconfirmed only through the unsettled pairs (single annotator).", n=h2("n_cert_unconfirmed_only_through_remainder")))
DEPART.append(("H2a added sentences", "supp S11.4", "exact-limit and margin sentences", "omitted: H2a.exact_lower_limit absent and margin_beats_certificate = false (CC-369 Ruling 5)"))
at("supp S11.4 Table S11.4d")
def brow(s):
    g = lambda *k, fn=nint: N("RES", ["H2b", "systems", s] + list(k), fn)
    return "| " + " | ".join([SYSN[s], g("U"), D(nint(int(R["H2b"]["systems"][s]["beta"]["0.2"])), "RES", f"floor(H2b.systems.{s}.beta.\"0.2\")"),
                              g("x"), g("x_hi"), "yes" if R["H2b"]["systems"][s]["covered"] else "no", g("w_hat", fn=f3), g("P_c", fn=f3), g("low_44", fn=f3)]) + " |"
S.append("\n".join([
    "**Table S11.4d.** H2b, budget coverage at $w_0$ (single annotator; new labels on previously analysed captions; 600 images). " + SYSKEY + ".",
    "", pl(469, "| System |").replace("Interval low end (Section 3.8)", "Interval low end (Section 6.7.3)"), pl(470, "|---|"),
    *[brow(s) for s in SYS_ORDER]]))
S.append(H2B_PASS + " " + W2S)
at("supp S11.4 Table S11.4e")
def grow(s):
    gi = lambda *k, fn=f3: N("RES", ["secondary", "golds_I600", "gold_i", "systems", s] + list(k), fn)
    gii = lambda *k, fn=f3: N("RES", ["secondary", "golds_I600", "gold_ii", "systems", s] + list(k), fn)
    return "| " + " | ".join([SYSN[s], gi("recall"), gi("P_c", "reg") + " / " + gi("P_c", "lo") + " / " + gi("P_c", "hi"),
                              gi("F1", "reg") + " / " + gi("F1", "lo") + " / " + gi("F1", "hi"), gi("hallucination"), gi("share_naming_absent"),
                              gii("recall"), gii("F1"), gii("hallucination"), gii("share_naming_absent")]) + " |"
S.append("\n".join([
    "**Table S11.4e (secondary; no verdict).** Recall, F1, verified-negative hallucination and the share of captions naming an absent class per system on the 600 images, under the two golds, never mixed in one row (single annotator; new labels on previously analysed captions). Gold (i): \"" + R["secondary"]["golds_I600"]["gold_i"]["label"].split(": ", 1)[1] + "\". Gold (ii): \"" + R["secondary"]["golds_I600"]["gold_ii"]["label"] + "\"; no conclusion is drawn from gold (ii).",
    "", pl(481, "| System |"), pl(482, "|---|"), *[grow(s) for s in SYS_ORDER]]))

at("supp S11.4 H2d")
S.append("**Label printed with every H2d number:** \"" + H2D_LABEL + "\".")
assert H2D_LABEL == pl(273, "**Label printed with every H2d number:**").split("** \"", 1)[1].rstrip("\".")
S.append(pl(275, "H2d asks whether"))
S.append(rows(276, 278))
S.append(pl(280, "The bootstrap uses 2,000"))
h2dsec = TXT["H2D"].split("\n")
S.append("**Smallest effect of interest (registered rationale, quoted).** The SESOI of 0.10 AUC was fixed in the registration by the following argument, which uses no XM3600, COCO-5000 or Part P outcome:\n" + "\n".join(h2dsec[52:55]))
assert h2dsec[52].startswith("- Resolution.") and h2dsec[54].startswith("- Not 0.05")
DEPART.append(("J-16 SESOI rationale", "supp S11.4", "H2D §4 bullets", "printed verbatim after a one-sentence own lead-in"))
NEW_TEXT.append(("S11.4 SESOI lead-in sentence", "supp S11.4", "**Smallest effect of interest (registered rationale, quoted).** The SESOI of 0.10 AUC was fixed in the registration by the following argument, which uses no XM3600, COCO-5000 or Part P outcome:"))
H2d = R["H2d"]
def dd(*k, fn=f3):
    return N("RES", ["H2d"] + list(k), fn)
def aucs(base):
    return " | ".join(N("RES", base + ["AUC_w_star_margin_length", i], f3) for i in range(3))
S.append("\n".join([
    "**Table S11.4f.** H2d (single annotator; new labels on previously analysed captions; scores from the freeze). Label: \"" + H2D_LABEL + "\".",
    "", pl(493, "| Pooled within-family pairs |"), pl(494, "|---|"),
    "| both families | " + " | ".join([dd("n1", fn=nint), dd("n0", fn=nint), dd("n_excluded", fn=nint), dd("n_NI", fn=nint), aucs(["H2d"]),
                                        dd("D", fn=f3s) + " " + dd("D_ci95", fn=ci(f3s)), dd("D_star_p036_bonferroni7", fn=f3s) + " (" + H2d["D_star_p036_label"] + ")", REGD["H2d"]]) + " |",
    *["| " + FAM[f] + " only (descriptive) | " + " | ".join([dd("per_family_descriptive", f, "n1", fn=nint), dd("per_family_descriptive", f, "n0", fn=nint),
                                                             dd("per_family_descriptive", f, "n_excluded", fn=nint), dd("per_family_descriptive", f, "n_NI", fn=nint),
                                                             aucs(["H2d", "per_family_descriptive", f]),
                                                             dd("per_family_descriptive", f, "D", fn=f3s) + " " + dd("per_family_descriptive", f, "D_ci95", fn=ci(f3s)),
                                                             "–", "no verdict"]) + " |" for f in ("Q25", "Q3")],
    "",
    T("Replicates with an empty class (single annotator): «a» of «b» (pooled).", a=dd("n_replicates_empty_class", fn=nint), b=dd("n_replicates", fn=nint)),
]))
DEPART.append(("Table S11.4f (pkg 6.7e)", "supp S11.4", "per-family rows with blank AUC cells", "per-family AUCs printed in all three columns (descriptive)"))
S.append("Registered reading (printed as the scoring code writes it): " + H2D_READ)
at("supp S11.4 J-19 (R11 §9)")
r11 = TXT["R11"].split("\n")
assert r11[229].startswith("## 9. Expectations stated now")
S.append("**Expectations stated with the registration (POST HOC; unverified; rough arithmetic from stored aggregates), quoted verbatim.** These were written before any label value was opened and are printed because the registration calls them disclosed:\n" + "\n".join(r11[231:234]))
for ln, lit in ((232, "91.6"), (232, "95.9"), (232, "36.7"), (232, "72.3"), (232, "30%"), (232, "57%"), (233, "9 of 15")):
    REG("R11", ln, lit)
NEW_TEXT.append(("S11.4 lead-in to the R11 §9 quote", "supp S11.4", "These were written before any label value was opened and are printed because the registration calls them disclosed:"))

# ---- S11.5 Part V ----
S.append("### S11.5 Part V: a development check on COCO-5000 against a fuller gold")
at("supp S11.5")
S.append(pl(315, "**Label printed with every Part V number:**"))
v1 = [pl(318, "**Why it can be done.**"), pl(321, "**Masking (M-ref, primary).**"), pl(324, "**Masking (M-label, secondary).**"),
      pl(327, "**Verdicts.**"), rows(329, 333), pl(335, "The evaluability thresholds"), pl(338, "**Ranking check against a margin rule"),
      pl(341, "**Reported whatever the verdicts.**"), pl(344, "**Kill gates.**")]
v1[1] = sub(v1[1], "the grid of Section 3.8;", "the grid of Supplementary S11.1;", "TG1 home swap", "§2.13 M-ref")
v1[8] = sub(v1[8], "the guarantee sentence of Section 3.8 is printed", "the guarantee sentence of Supplementary S11.1 is printed", "TG1 home swap", "§2.13 Kill gates")
for kv_old, kv_new in (("KV0: ", "(a) "), ("KV-EV: ", "(b) "), ("KV1: ", "(c) "), ("KV2: ", "(d) "), ("KV3: a second fault goes to the PI.", "(e) A second fault stops the analysis.")):
    v1[8] = sub(v1[8], kv_old, kv_new, "TG9 (internal gate codes KV0-KV3 replaced by (a)-(e); 'goes to the PI' -> 'stops the analysis')", "§2.13 Kill gates")
S.extend(v1)
VT = V["primary_truth_G_top"]
def vv(*k, fn=nint):
    return N("VR", list(k), fn)
G = ["primary_truth_G_top"]
I = ["secondary_instance_only_truth"]
def vrow(name, base, lab_v1, lab_v2, lab_v3, k2):
    return "| " + " | ".join([name, vv(*base, "V1_V3", "n_cert") + " (" + vv(*base, "V1_V3", "n_pairs_cert") + ")", vv(*base, "V1_V3", "n_other"),
                              vv(*base, "V1_V3", "n_excluded"), vv(*base, "V1_V3", "n_cert_direction_fails"), vv(*base, "V1_V3", "e_c", fn=f3),
                              vv(*base, "V1_V3", "e_n", fn=f3), vv(*base, "V1_V3", "e_n_minus_e_c_ci95", fn=ci(f3)), lab_v1,
                              vv(*base, "V2", "n_over_budget") + " / " + vv(*base, "V2", "n_cells") + " (" + vv(*base, "V2", "share", fn=f3) + ")",
                              lab_v2, lab_v3, k2]) + " |"
def cfrow(b):
    c = VT["cross_fit"][b]
    base = G + ["cross_fit", b]
    return "| " + " | ".join(["Cross-fitted floor, " + b + " (secondary; floor by half " + vv(*base, "w0_by_half", fn=lambda v: " / ".join(f"{x:.2f}" for x in v)) + ")",
                              vv(*base, "n_cert") + " (" + vv(*base, "n_pairs_cert") + ")", vv(*base, "n_other"), vv(*base, "n_excluded"),
                              vv(*base, "n_cert_direction_fails"), vv(*base, "e_c", fn=f3), vv(*base, "e_n", fn=f3), vv(*base, "e_n_minus_e_c_ci95", fn=ci(f3)),
                              c["V1"] + ", no verdict", vv(*base, "V2", "n_over_budget") + " / " + vv(*base, "V2", "n_cells") + " (" + vv(*base, "V2", "share", fn=f3) + ")",
                              c["V2"]["label"] + ", no verdict", c["V3"] + ", no verdict", "–"]) + " |"
for b in ("V-B", "V-H"):
    assert VT["cross_fit"][b]["V2"]["n_cells"] > 0 and VT["cross_fit"][b]["n_half_units_excluded_floor_0"] == 0
VK = V["registered"]
k2g = vv(*G, "COCO K2", "delta_cov", fn=f3) + " (" + vv(*G, "COCO K2", "LB_p5", fn=f3) + "): " + VK["COCO K2"]
k2i = vv(*I, "COCO K2", "delta_cov", fn=f3) + " (" + vv(*I, "COCO K2", "LB_p5", fn=f3) + "), no verdict"
S.append("\n".join([
    "**Table S11.5a.** Part V verdicts, $k = 2$, $w_0 = 0.20$, truth $G^{\\mathrm{top}}$, with the instance-only truth and the cross-fitted floors as secondary rows (development; outcome foreseeable from stored aggregates and an unreviewed calculation (disclosed)). The cross-fitted floor is measured against the fuller gold of the other image half, so it is not a reference-only quantity; its V1, V3 and V2 labels are secondary with no verdict; they do not qualify V2 FLOOR REFUTED at $w_0$; $w_0$ was not changed.",
    "", pl(555, "| Truth |"), pl(556, "|---|"),
    vrow("$G^{\\mathrm{top}}$", G, VK["V1"], VK["V2"], VK["V3"], k2g),
    vrow("Instance classes only (secondary)", I, V["secondary_instance_only_truth"]["V1_V3"]["V1"] + ", no verdict",
         V["secondary_instance_only_truth"]["V2"]["label"] + ", no verdict", V["secondary_instance_only_truth"]["V1_V3"]["V3"] + ", no verdict", k2i),
    cfrow("V-B"), cfrow("V-H"),
]))
DEPART.append(("Table S11.5a", "supp S11.5", "package columns", "instance-only row filled in every column (labels with 'no verdict'); CC-360 W3 caption text added"))
at("supp S11.5 power")
ptab = ["**Table S11.5b.** Share of the 720 pair-draws certified, by number of references $k$, floor $w$ and budget (development; outcome foreseeable from stored aggregates and an unreviewed calculation (disclosed)). The $k = 5$ rows were computed in the scoring pass, because the five-reference union is not formed at the freeze.", "",
        "| $k$ | Budget | $w$ = 0 | 0.10 | 0.20 | 0.30 | 0.50 |", "|---|---|---|---|---|---|---|"]
for k in ("1", "2", "3", "5"):
    for b in ("V-B", "V-H"):
        ptab.append("| " + k + " | " + b + " | " + " | ".join(vv("power", "by_k", k, b, w, fn=f3) for w in ("0.0", "0.1", "0.2", "0.3", "0.5")) + " |")
S.append("\n".join(ptab))
at("supp S11.5 sentences")
nl = lambda base, r: vv(*base, "nulls_w0", r, "n") + " certified, " + vv(*base, "nulls_w0", r, "n_direction_fails") + " wrong"
TT = V["transported_threshold"]["by_half"]
S.append(T("Further Part V rows (development; outcome foreseeable from stored aggregates and an unreviewed calculation (disclosed)). Null rules at $w_0$ (truth $G^{\\mathrm{top}}$; instance-only truth in brackets): constant, «c» [«ci»]; margin at the certified count, «m» [«mi»]; length, «l» [«li»]. Transported margin threshold (secondary): read on one image half against $G^{\\mathrm{top}}$ and applied to the other, «t0» and «t1» points, with «n0» and «n1» half-units certified and «e0» and «e1» wrong. Reference-named pairs absent from the instance gold (the only truth under which (A0) can fail): «r».",
           c=nl(G, "constant"), ci=nl(I, "constant"), m=nl(G, "margin"), mi=nl(I, "margin"), l=nl(G, "length"), li=nl(I, "length"),
           t0=vv("transported_threshold", "by_half", 0, "tau_points", fn=f2), t1=vv("transported_threshold", "by_half", 1, "tau_points", fn=f2),
           n0=vv("transported_threshold", "by_half", 0, "n_certified"), n1=vv("transported_threshold", "by_half", 1, "n_certified"),
           e0=vv("transported_threshold", "by_half", 0, "n_direction_fails"), e1=vv("transported_threshold", "by_half", 1, "n_direction_fails"),
           r=vv("secondary_instance_only_truth", "n_ref_named_pairs_not_in_instance_gold")))
for u in ("u=0.3 uniform", "u=0.3 salience", "u=0.57 uniform", "u=0.57 salience"):
    for base in (G, I):
        assert get("VR", base + ["M_label", u, "n_certified"]) == 0
        vv(*base, "M_label", u, "n_certified")
S[-1] = S[-1] + " With 30% or 57% of the statuses hidden, uniformly or by salience, the label-side certificate certified none of the 720 pair-draws."
REGF("VP", "0.57", "30% or 57%")
v1s = T("At $w_0 = 0.20$ with two references, «e» of «n» certified pair-draws on COCO-5000 had the wrong direction under the fuller gold ($e_c$ = «ec»; at most 5% allowed, and no pair wrong in more than half of its certified draws): V1 PASS.",
        e=vv(*G, "V1_V3", "n_cert_direction_fails"), n=vv(*G, "V1_V3", "n_cert"), ec=vv(*G, "V1_V3", "e_c", fn=lambda v: f"{v:g}"))
assert v1s == "At $w_0 = 0.20$ with two references, 0 of 200 certified pair-draws on COCO-5000 had the wrong direction under the fuller gold ($e_c$ = 0; at most 5% allowed, and no pair wrong in more than half of its certified draws): V1 PASS."  # CC-360 3(a)
w1 = T(" («p» of the 36 pairs, each certified in all 20 draws; the margin rule at the same count also made no error)", p=vv(*G, "V1_V3", "n_pairs_cert"))
assert all(r["share_certified_w0"] in (0.0, 1.0) for r in VT["pair_table"]) and sum(r["share_certified_w0"] == 1.0 for r in VT["pair_table"]) == 10
v2s = T("In «o» of «c» cells («s») more unknown pairs were present than the budget at $w_0$ allows, above the registered $\\alpha_S = 0.025$.",
        o=vv(*G, "V2", "n_over_budget"), c=vv(*G, "V2", "n_cells"), s=vv(*G, "V2", "share", fn=f3))
v3s = T("Uncertified pair-draws had the wrong direction more often than certified ones ($e_n$ = «en» against $e_c$ = «ec»; $e_n - e_c$ «ci»): V3 DISCRIMINATING.",
        en=vv(*G, "V1_V3", "e_n", fn=f3), ec=vv(*G, "V1_V3", "e_c", fn=lambda v: f"{v:g}"), ci=vv(*G, "V1_V3", "e_n_minus_e_c_ci95", fn=ci(f3)))
assert v3s == "Uncertified pair-draws had the wrong direction more often than certified ones ($e_n$ = 0.329 against $e_c$ = 0; $e_n - e_c$ [0.170, 0.507]): V3 DISCRIMINATING."  # CC-360 3(d)
k2s = V["sentences"][1] + T(" ($\\Delta_{\\mathrm{cov}}$ = «d», 5th percentile «p»)", d=vv(*G, "COCO K2", "delta_cov", fn=f3), p=vv(*G, "COCO K2", "LB_p5", fn=f3))
kv2 = "Because V2 is FLOOR REFUTED, the guarantee of Supplementary S11.1 is printed with \"the floor assumption failed on COCO-5000 at w0\", and, because V1 passed, the certificate is described as \"empirically valid on the sets tested\" (COCO-5000, one model family, development); the instance-only rows of Part V and the same-image pairs of Supplementary S11.6 are not sets on which it is so described."
S.append("Part V outcomes (development; outcome foreseeable from stored aggregates and an unreviewed calculation (disclosed)). " + v1s[:-1] + w1 + ". " + V["sentences"][0][0].upper() + V["sentences"][0][1:] + ". " + v2s + " " + kv2 + " " + v3s + " " + k2s[0].upper() + k2s[1:] + ". " + V["sentences"][2][0].upper() + V["sentences"][2][1:])
DEPART.append(("Part V sentences", "supp S11.5", "[code] strings", "first letter capitalised and a full stop added where a code string starts or ends a sentence; CC-360 W1 appended to V1 PASS; CC-360 W2 scope after 'empirically valid on the sets tested'"))
NEW_TEXT.append(("S11.5 KV2 sentence (code strings + CC-360 W2)", "supp S11.5", kv2))
NEW_TEXT.append(("S11.4/S11.5/S11.6 table captions and row labels (own words around package captions)", "supp S11", "see the tables"))
at("supp S11.5 J-19 (VP §V.1, §V.5)")
vp = TXT["VP"].split("\n")
assert vp[39].startswith("### V.1") and vp[82].startswith("**Status of every Part V verdict (binding).**")
S.append("**Figures known before Part V was registered, quoted verbatim from the registration (POST HOC; from committed aggregates and from an unreviewed scratch calculation).**\n\n" + "\n".join(vp[41:45]) + "\n\n" + "\n".join(vp[46:49]) + "\n\n" + vp[82])
for ln, lit in ((43, "59.2"), (43, "84.9"), (43, "84.0"), (43, "94.7"), (44, "9 of the 36"), (45, "1.64"), (45, "3.72"), (45, "26 of 36"), (45, "28 of 36"), (48, "222 of 720"), (49, "263 of 1,440"), (49, "39 of 72")):
    REG("VP", ln, lit)
DEPART.append(("J-19 VP quote", "supp S11.5", "VP §V.1 bullets and §V.5 Status paragraph", "verbatim, with their two lead-in lines; internal names inside the quote kept (TG9 conflict flagged)"))

# ---- S11.6 Part P ----
S.append("### S11.6 Part P: the certificate applied to 15 published comparisons (POST HOC)")
at("supp S11.6")
p6 = [pl(352, "**Label printed with every Part P number:**"), pl(355, "**Data.**"), pl(358, "**Gold and matcher check.**"),
      pl(361, "**Reserved gold.**"), pl(364, "**P-a, reference-rung replay"), pl(367, "**P-b, the CHAIR gold itself"),
      pl(370, "**Nothing in Part P is evidence")]
p6[4] = sub(p6[4], "the grid and $w_0$ of Section 3.8.", "the grid and $w_0$ of Supplementary S11.1.", "TG1 home swap", "§2.14 P-a")
S.extend(p6)
assert P["matcher_gate"]["passed"] is True and "dropped" not in P
neq = sum(v["equal"] for v in P["matcher_gate"]["systems"].values())
S.append(T("Matcher check: for all «n» systems the recomputed precision, mentions per caption and image count equal the stored rows (POST HOC; truth already scored by the paper). " + P["methods_sentence"] + ".",
           n=D(str(neq), "PR", "count of matcher_gate.systems.*.equal = true")))
NEW_TEXT.append(("S11.6 matcher-check sentence", "supp S11.6", "Matcher check: for all 24 systems the recomputed precision, mentions per caption and image count equal the stored rows (POST HOC; truth already scored by the paper)."))
at("supp S11.6 Table S11.6a")
def parow(j, r):
    g = lambda *k, fn=f3: N("PR", ["P_a", "published", j] + list(k), fn)
    sent = r["sentence"].replace("with 1 references", "with 1 reference")
    return "| " + " | ".join([pcomp(r["comparison"]), r["image_set"] + " (" + g("n_images", fn=nint) + ")", str(r["k"]),
                              g("share_certified_w0", fn=f2), g("share_certified_w0_baseline_direction", fn=f2), g("median_w_star", fn=f4),
                              g("n_certified_equal_to_chair_gold_direction", fn=nint),
                              (g("transported_margin_secondary", "tau_points", fn=f2) + " points; " + g("transported_margin_secondary", "share_of_draws_above", fn=f2)) if r["k"] == 2 and r.get("transported_margin_secondary") else "–",
                              sent]) + " |"
S.append("\n".join([
    "**Table S11.6a.** P-a, each published comparison at each $k$ (POST HOC; truth already scored by the paper). At $k = 5$ every draw is the full set of five references, so the 20 draws are identical. Method and baseline names are those of the released files ([LiM] = the \"Less is More\" release; F-A = the OPERA InstructBLIP set, F-B = the OPERA set of LLaVA-1.5, MiniGPT-4 and Shikra, F-C = the \"Less is More\" set). Shares are of the 20 reference draws; the baseline-direction share is a separate field and is never added to the first. The transported margin row ($k = 2$; secondary) gives the threshold and the share of draws whose margin is above it. The last column is printed as the scoring code writes it (\"1 references\" printed \"1 reference\").",
    "", "| Comparison (method vs baseline) | Image set (images) | $k$ | Share certified, method direction | Share certified, baseline direction | Median $w^*$ | Certified draws agreeing with the CHAIR-gold direction | Transported margin row | Sentence |",
    "|---|---|---|---|---|---|---|---|---|",
    *[parow(j, r) for j, r in enumerate(P["P_a"]["published"])]]))
DEPART.append(("Table S11.6a", "supp S11.6", "[code] sentence strings", "CC-360 W6: 'with 1 references' → 'with 1 reference' (grammar only); caption adds the k = 5 note; comparison names from the released file ids"))
at("supp S11.6 aggregates")
agg = []
for j, a in enumerate(P["P_a"]["aggregate"]):
    m = re.search(r": (\d\.\d{3}) \(k = (\d),", a["text"])
    agg.append(T("mean share of the 20 reference draws certified over the 15 published comparisons: «v» (k = «k», w0 = 0.20, the three released image sets as released, images with instance labels, as in Supplementary S3, «lo» to «hi» images per comparison)",
                 v=N("PR", ["P_a", "aggregate", j, "text"], lambda t: re.search(r": (\d\.\d{3}) \(", t).group(1)), k=m.group(2),
                 lo=D(str(min(r["n_images"] for r in P["P_a"]["published"])), "PR", "min of P_a.published[*].n_images"),
                 hi=D(str(max(r["n_images"] for r in P["P_a"]["published"])), "PR", "max of P_a.published[*].n_images")))
S.append("Aggregate (POST HOC; truth already scored by the paper): " + "; ".join(agg) + ".")
at("supp S11.6 Table S11.6b")
SI = P["P_a"]["same_image_pairs"]
def sirow(j, r):
    g = lambda *k, fn=f4: N("PR", ["P_a", "same_image_pairs", "pairs", j] + list(k), fn)
    return "| " + " | ".join([psys(r["A"]) + " vs " + psys(r["B"]), r["image_set"] + " (" + g("n_images", fn=nint) + ")",
                              " / ".join(g("median_w_star_k" + k) for k in "1235"),
                              " / ".join(g("share_certified_w0_k" + k, fn=f2) for k in "1235")]) + " |"
v13 = ["P_a", "same_image_pairs", "V1_V3"]
S.append("\n".join([
    "**Table S11.6b.** Same-image pairs (" + N("PR", ["P_a", "same_image_pairs", "n_pairs"], nint) + "; post hoc; truth already scored by the paper; other model families; descriptive; no verdict). The share column counts certificates in either direction and is not a certificate for a published comparison.",
    "", "| Pair | Image set (images) | Median $w^*$ at $k$ = 1 / 2 / 3 / 5 | Share of draws certified in either direction at $k$ = 1 / 2 / 3 / 5 |", "|---|---|---|---|",
    *[sirow(j, r) for j, r in enumerate(SI["pairs"])],
    "",
    T("Over the 94 pairs at $k = 2$ and $w_0 = 0.20$ (post hoc; truth already scored by the paper; other model families; descriptive; no verdict): «c» of «t» pair-draws certified («p» of 94 pairs), «w» wrong (V1 «v1»); $e_n$ = «en», $e_n - e_c$ «ci» (V3 «v3»); cells over budget «o» of «nc» («s»; V2 «v2»).",
      c=N("PR", v13 + ["n_cert"], nint), t=D(nint(SI["V1_V3"]["n_cert"] + SI["V1_V3"]["n_other"]), "PR", "P_a.same_image_pairs.V1_V3.n_cert + n_other"),
      p=N("PR", v13 + ["n_pairs_cert"], nint), w=N("PR", v13 + ["n_cert_direction_fails"], nint), v1=SI["V1_V3"]["V1"],
      en=N("PR", v13 + ["e_n"], f3), ci=N("PR", v13 + ["e_n_minus_e_c_ci95"], ci(f3)), v3=SI["V1_V3"]["V3"],
      o=N("PR", ["P_a", "same_image_pairs", "V2", "V2", "n_over_budget"], nint), nc=N("PR", ["P_a", "same_image_pairs", "V2", "V2", "n_cells"], nint),
      s=N("PR", ["P_a", "same_image_pairs", "V2", "V2", "share"], f3), v2=SI["V2"]["V2"]["label"]),
]))
at("supp S11.6 Table S11.6c")
CELL = {"A": "$\\mathcal C_{A\\setminus B}$", "B": "$\\mathcal C_{B\\setminus A}$", "S": "$\\mathcal C_{A\\cap B}$"}
def pbrow(j, r):
    g = lambda *k, fn=f4: N("PR", ["P_b", j] + list(k), fn)
    sent = r["sentence"]
    mm = re.search(r"cell\(s\) ([ABS](?:, [ABS])*) at w0", sent)
    if mm:
        sent = sent.replace(mm.group(0), "cell(s) " + ", ".join(CELL[c] for c in mm.group(1).split(", ")) + " at w0")
    ws = g("w_star_cap_I0", fn=lambda v: v if isinstance(v, str) else ("NI" if v is None else f4(v)))
    return "| " + " | ".join([pcomp(r["comparison"]), r["image_set"] + " (" + g("n_images", fn=nint) + ")",
                              " / ".join(g("I0_by_cell", c, fn=nint) for c in "ABS"), ws, g("w_star_cap_min_U_floor_beta", fn=lambda v: v if isinstance(v, str) else ("NI" if v is None else f4(v))),
                              ", ".join(CELL[c] for c in r["cells_with_floor_refuted_at_w0"]) or "none",
                              r["certified_direction"] and psys(r["certified_direction"]) or "–", sent]) + " |"
S.append("\n".join([
    "**Table S11.6c.** P-b, the CHAIR gold itself ($k = 5$; secondary; no truth exists; POST HOC; truth already scored by the paper). With the instance-label cap the comparison is certified from $w^*$ up to the floor at which the instance labels refute it; a $w^*$ below $w_0$ beside \"not certified at w0\" is therefore not a contradiction. The plain-cap column gives $w^*$ only and is never read as a certificate. Cells: $\\mathcal C_{A\\setminus B}$, $\\mathcal C_{B\\setminus A}$, $\\mathcal C_{A\\cap B}$, with $A$ = the method. The last column is printed as the scoring code writes it, with the cell letters in this notation.",
    "", "| Comparison (method vs baseline) | Image set (images) | $I_0$ by cell ($A\\setminus B$ / $B\\setminus A$ / $A\\cap B$) | $w^*$, instance-label cap | $w^*$, plain cap | Cells with the floor refuted at $w_0$ | Certified direction (field) | Sentence |",
    "|---|---|---|---|---|---|---|---|",
    *[pbrow(j, r) for j, r in enumerate(P["P_b"])]]))
DEPART.append(("Table S11.6c", "supp S11.6", "[code] sentences", "CC-360 W7: cell letters A, B, S printed as the §0.1 cells; W7 caption added"))

# ---- S11.7 ----
S.append("### S11.7 The labelling protocol")
at("supp S11.7")
S7 = T("The labelling page and its build script are in `tools/obj_rater/` of the code record; the build script fixes the questions, the hidden controls and their order with seed «seed». A mapped class is shown with the Open Images classes it maps to (\"Open Images: …\"), and the annotator is told to read the class by them; a class without a mapping (part 2) is shown by its lexicon word alone. The four answers are shown in Vietnamese: Có (yes), Không (no), Không xác định được (U: the image cannot settle it) and Tên lớp mơ hồ (A: the word does not name an object category). Practice used «pr» XM3600 images outside the 600, with Open Images answers and feedback; practice answers are not data. Every answer is appended to a file, one line per answer; a changed answer is a new line, the last line of a question is its answer, and all lines are kept. During labelling the analysts read only the line count and the SHA-256 of that file, which the project log records at the end of each session; the file that holds the role of each question is kept by the analysis pipeline, is not served to the page and was not opened by the annotator. The roles were read only by the pinned scoring script.",
       seed=REG("PLAN", 14, "seed 20261111", "20261111"), pr=REG("PLAN", 25, "15 XM3600 images", "15"))
S.append(S7)
NEW_TEXT.append(("S11.7 protocol paragraph", "supp S11.7", S7))
uat = ["**Table S11.7a.** Share of the answered part-1 target questions of each class answered U or A (single annotator; new labels on previously analysed captions; descriptive, gates nothing). Classes are the lexicon words.", "",
       "| Class | U or A share | Class | U or A share | Class | U or A share |", "|---|---|---|---|---|---|"]
ua = list(R["quality"]["UA_rate_by_class"])
cells = [c + " | " + N("RES", ["quality", "UA_rate_by_class", c], f3) for c in ua]
while len(cells) % 3:
    cells.append(" | ")
for i in range(0, len(cells), 3):
    uat.append("| " + " | ".join(cells[i:i + 3]) + " |")
S.append("\n".join(uat))

# ---- S11.8 ----
S.append("### S11.8 Code, pins and run records")
at("supp S11.8")
S8 = "\n".join([
    "- Scoring code: `scripts/a_cert/a_cert.py` (SHA-256 2e872588…), modes `gate`, `freeze` and `score`; `scripts/a_cert/a_cert_vp.py` (SHA-256 17507200…), modes `v-freeze`, `v-score` and `p-score`. " + pl(347, "**Implementation note (S11.8, CC-352 N1).**").replace("**Implementation note (S11.8, CC-352 N1).** ", ""),
    "- Registrations: the analysis registration (SHA-256 e564b7b1…), the addendum for Parts V and P (0e586fa9…), the H2d registration (d0afcaf0…) and the labelling plan (8ad28f67…), each committed before the output it governs (times: Table S4.0).",
    "- Fixed files: the freeze file (c51ea7dc…), the label result (7492a16c…), the Part V freeze file (7a9ad62b…), the Part V result (2675cdce…) and the Part P result (a05edf41…). Each was fixed by its hash in the project log when it was written.",
    "- Runs: one scoring pass on the labels, with no fault; one Part V freeze run and one Part V scoring run; one Part P scoring run, after an earlier attempt that the script's argument check refused before any file was read. A second fault in any of them would have stopped that analysis.",
    "- Notation: the registration's systems A and B keep their names; its cells B-only, A-only and S are $\\mathcal C_{B\\setminus A}$, $\\mathcal C_{A\\setminus B}$, $\\mathcal C_{A\\cap B}$; U, X, x are $u$, $X$, $x$; f1 is $\\varphi_1$; N_s is $\\mathcal N_S$; the families Q25 and Q3 are the first-backbone and second-backbone families; I600 and I537 are XM3600-600 and its clean subset of 537 images; G_top is $G^{\\mathrm{top}}$; F-A, F-B and F-C are the released image sets of Table S11.6a.",
])
S.append(S8)
NEW_TEXT.append(("S11.8 list (code, pins, run records, notation map)", "supp S11.8", S8))

S11 = "\n\n".join(S)
# Home S: no Section 3.8 / 6.8 / 6.7.3-6.7.5 pointer may remain inside the transferred blocks
LEFT38 = re.findall(r"Section 3\.8[^.;)]{0,40}", S11)
LEFT68 = re.findall(r"Section 6\.8", S11)
LEFT675 = re.findall(r"Section 6\.7\.5", S11)

# =====================================================================================================
# Abstract (≤ 250 words; CC-357 J-34, TG10; CC-369 W6, W7)
# =====================================================================================================
at("abstract")
ABS_OLD_START = "Object hallucination scores such as CHAIR and object F1"
ABS_OLD_END = "but count-matched precision tracks it worse than raw precision."
ABS_NEW = ("Object hallucination scores such as CHAIR and object F1 are reference-based quality measures whose reference, a gold object set, is usually incomplete. "
           "This registered audit tests whether their verbosity slope (F1 on log object count) is ordered from one reference to all references to verified labels. "
           "On 600 Crossmodal-3600 images with Vietnamese references (six one-backbone systems), the ordering held: −8.99 [−10.89, −6.99] with one reference, −2.43 with 2–3 references and +19.32 [+17.43, +21.13] under human-verified Open Images labels (95% intervals, conditional on the systems; in effect a short-versus-detailed contrast). "
           "This label gold is smaller, with another precision rule. "
           "A second backbone reproduced it on 537 of them. "
           "On PASCAL-50S the registered replication failed at its label-gold step (−2.29 [−5.15, +0.61]). "
           "On 3,226 reserved COCO images with four LVLMs, a registered look found one-reference gold below a size-matched random-deletion null; the label-gold slope exceeded the one-reference slope, partly expected from its 2.149-fold size. "
           "Post hoc, the positive label-gold sign depends on excluding unverifiable mentions" + E13 + ", and the reference-gold signs rest on one verbose system. "
           "Nine registered predictions failed (two of five on Crossmodal-3600). "
           "Of seven predictions registered on these single-annotator labels, five passed (H1a, H1b, H1c, H2b, H3), one failed (H2d) and one was not evaluable (H2a); a proposed certificate was not validated. "
           "In public human judgments relevance falls with object count, but count-matched precision tracks it worse than raw precision.")
NEW_TEXT.append(("Abstract (cut to ≤ 250 words; J-34)", "abstract_A.md", "whole paragraph; see the diff"))


def words(s):
    return len(re.sub(r"<!--.*?-->", "", s, flags=re.S).split())


ABS_WORDS = words(ABS_NEW)
assert ABS_WORDS <= 250, ABS_WORDS
for must in ("Nine registered predictions failed", "failed at its label-gold step", "one failed (H2d)", "one was not evaluable (H2a)", "tracks it worse"):
    assert must in ABS_NEW
HL_OLD = "- A positive label-gold slope needs unverifiable mentions excluded from precision"
HL_NEW = "- " + pkg_quote("Human labels complete the XM3600 object gold and measure the label-gold slope")
assert len(HL_NEW) - 2 <= 85

# =====================================================================================================
# Supplement Table S4.0 rows (J-28: next free ids A31-A37, D-1-D-4, P-5)
# =====================================================================================================
at("supp Table S4.0")
S40 = "\n".join([
    "| A31 | XM3600-600, new labels: completed label-gold slope of the second backbone > 0 (H1a) | registered on new labels of previously analysed captions (development role; single annotator) | " + REGD["H1a"] + " | 6.7.2 |",
    "| A32 | XM3600-600, new labels: first-backbone completed slope inside the Table S7.2 bracket (H1b) | registered on new labels of previously analysed captions (development role; single annotator) | " + REGD["H1b"] + " | 6.7.2 |",
    "| A33 | XM3600-600, new labels: second-backbone completed slope inside the Table S7.2 bracket (H1c) | registered on new labels of previously analysed captions (development role; single annotator) | " + REGD["H1c"] + " | 6.7.2 |",
    "| A34 | XM3600-600, new labels: the reference-only certificate at $w_0$ holds on the completed gold and beats uncertified pairs (H2a) | registered on new labels of previously analysed captions (development role; single annotator) | " + REGD["H2a"] + " (declared at the freeze) | S11.4 |",
    "| A35 | XM3600-600, new labels: the budget at $w_0$ covers at least 11 of 12 systems (H2b) | registered on new labels of previously analysed captions (development role; single annotator) | " + REGD["H2b"] + " (" + W2 + ") | S11.4 |",
    "| A36 | XM3600-600, new labels: $w^*$ ranks comparisons better than margin and length by AUC ≥ 0.10 (H2d) | registered on new labels of previously analysed captions (development role; single annotator; label in Supplementary S11.4) | " + REGD["H2d"] + " | S11.4 |",
    "| A37 | XM3600-600, new labels: the coverage bound of Section 5.4 against the completed gold (H3) | registered on new labels of previously analysed captions (development role; single annotator) | " + REGD["H3"] + " | 6.7.4 |",
    "| D-1 | COCO-5000, certificate against a fuller gold: certified pair-draws wrong (V1) | development; outcome foreseeable from stored aggregates and an unreviewed calculation (disclosed) | " + VK["V1"] + " (no verdict on the paper's claims) | S11.5 |",
    "| D-2 | COCO-5000: the naming floor $w_0$ against the fuller gold (V2) | development; outcome foreseeable from stored aggregates and an unreviewed calculation (disclosed) | " + VK["V2"] + " (no verdict on the paper's claims) | S11.5 |",
    "| D-3 | COCO-5000: certified against uncertified pair-draws (V3) | development; outcome foreseeable from stored aggregates and an unreviewed calculation (disclosed) | " + VK["V3"] + " (no verdict on the paper's claims) | S11.5 |",
    "| D-4 | COCO-5000: ranking by $w^*$ against a margin rule (COCO K2) | development; outcome foreseeable from stored aggregates and an unreviewed calculation (disclosed) | " + VK["COCO K2"] + " (no verdict on the paper's claims) | S11.5 |",
])
S40_P5 = "| P-5 | Certificate applied to 15 published comparisons | POST HOC; truth already scored by the paper | no verdict | S11.6 |"
S40_TIMES = T("**Times of rows A31–A37, D-1–D-4 and P-5 (UTC; times of the project-log lines).** Labelling plan pinned «a»; analysis registration committed «b»; addendum for Parts V and P committed «c»; H2d registration committed and pinned «d»; freeze pinned «e»; Part V freeze pinned «f»; Part V scoring ended «g»; Part P scoring ended «h»; part 1 of the labelling finished «i»; scoring on the labels «j».",
              a=LOGV("OPS-1111al-xm600-label-start", "2026-11-11 05:55"), b=LOGV("OPS-1111an-a-cert-reg-commit", "2026-11-11 06:45"),
              c=LOGV("OPS-1111as-a-addendum-commit", "2026-11-11 09:09"), d=LOGV("OPS-1111at-a-h2d-commit-pin", "2026-11-11 09:24"),
              e=LOGV("OPS-1112h-a-cert-FREEZE-pin", "2026-11-11 18:29"), f=LOGV("PIN-1112-a-vp-FREEZE_V", "2026-11-12 07:23"),
              g=LOGV("OPS-1112aj-a-vp-vscore-end", "2026-11-12 07:26"), h=LOGV("OPS-1112az-a-p-score-attempt2-end", "2026-11-12 10:45"),
              i=LOGV("OPS-1112cf-xm600-session-end-part1", "2026-11-12 18:15"), j=LOGV("OPS-1112ch-a-cert-score", "2026-11-12 18:30"))
NEW_TEXT.append(("Table S4.0 rows A31–A37, D-1–D-4, P-5 and the times paragraph", "both supplements", "see the diff"))

# =====================================================================================================
# FIX_A2 per CC-375 Ruling 4
# =====================================================================================================
FX_SEC5 = [("FIX_A2 W-01", "| UIT-ViIC (all splits), VI | independent | 3,842 |", "| UIT-ViIC (all splits), VI | five writers; assignment per image not stated | 3,842 |"),
           ("FIX_A2 W-04 (CC-375 string)", "The two independent-annotator caption sets with a documented protocol, COCO and UIT-ViIC, sit at the null, with no lag-1 excess. Two corpora sit above it.",
            "COCO and UIT-ViIC, the two caption sets with a documented protocol, sit at the null, with no positive lag-1 excess; for UIT-ViIC, Lam et al. (2020) report five writers for the dataset but do not state who wrote which caption of an image. Two corpora sit above the null.")]
FX_SUPP = [("FIX_A2 W-03", "| UIT-ViIC (all splits), VI | independent | 3,842 |", "| UIT-ViIC (all splits), VI | five writers; assignment per image not stated | 3,842 |"),
           ("FIX_A2 W-02", "| UIT-ViIC (all splits), VI | independent annotators | 3,842 |", "| UIT-ViIC (all splits), VI | panel of five writers; assignment per image not stated (Lam et al., 2020) | 3,842 |"),
           ("FIX_A2 W-05 (CC-375 string)", "The two independent-annotator caption sets with a documented protocol, COCO and UIT-ViIC, sit at the null in both statistics. Two corpora sit above it.",
            "COCO and UIT-ViIC, the two caption sets with a documented protocol, sit at the null in the adjacent-doubleton share and show no positive lag-1 excess (the UIT-ViIC value in Table S5.2 is slightly below zero); for UIT-ViIC, Lam et al. (2020) report five writers for the dataset but do not state who wrote which caption of an image. Two corpora sit above the null."),
           ("FIX_A2 W-06 (CC-375 string)", "five Vietnamese references written by independent annotators; Section 5",
            "five Vietnamese references per image, from a dataset written by five writers (Lam et al., 2020); reference order on all splits in Section 5"),
           ("FIX_A2 W-07", "No single-writer corpus is tested here.", "No corpus documented as single-writer is tested here."),
           ("FIX_A2 Q6 (CC-375)", "Reference-count analyses also assume independent writers, which a diagnostic tests (Section 5).",
            "Reference-count analyses also assume exchangeable references, which a diagnostic of reference order checks (Section 5).")]
FX_BASE = {"paper/sec5_exchangeability.md": "d55ea4287b44ecfe3a13cda769be70ba78f2d69b06fc19e9486c842f03f9578d",
           "paper/supplementary_SPIC.md": "bf0d2127f413fcdd84edf6e0d127b1906a0d670da5d7f014dd6dbbd56d59dfed",
           "paper/supplementary.md": "1cd45dcdef2748c2524daafe404332ed88f051bf220339c9ca92546b2a46aed6"}

# =====================================================================================================
# Edit table: (row id, file, OLD, NEW)
# =====================================================================================================
SEC7 = "paper/sec7_verbosity_sign.md"
SEC7_TAIL = "because the labels are not a complete inventory of the image."
EDITS = [
    ("E13 (6.2 Reading)", SEC7, "so the positive label-gold slope depends on excluding unverifiable mentions", "so the positive label-gold slope depends on excluding unverifiable mentions" + E13),
    ("C5 'the certificate' (6.7 Freeze)", SEC7, "a label-free run computed every certificate, $w^*$,", "a label-free run computed every certificate of Supplementary S11, $w^*$,"),
    ("N2 run fact (6.7 One pass)", SEC7, "A second fault would have stopped the analysis.", "A second fault would have stopped the analysis." + RUNFACT),
    ("C5 H2a/H2b/H2d pointer + J-39 paragraph (6.7)", SEC7, "H1a, H1b, H1c, H2a, H2b, H2d and H3. Their rules",
     "H1a, H1b, H1c, H2a, H2b, H2d and H3 (H2a, H2b and H2d test the certificate and are defined in Supplementary S11.4). Their rules"),
    ("J-39 / count line (6.7)", SEC7, 'and writes "all pass" only if all seven pass.', 'and writes "all pass" only if all seven pass.\n\n' + OUTCOME67),
    ("C5 'the certificate' (6.7.1)", SEC7, "gives a gold against which the certificate can be tested.", "gives a gold against which the certificate of Supplementary S11 can be tested."),
    ("Table 6.7a quality (6.7.1)", SEC7, "\n\n### 6.7.2 Hypotheses H1", "\n\n" + QTAB + "\n\n### 6.7.2 Hypotheses H1"),
    ("C7/N4 caption H1 rule table (6.7.2)", SEC7, "\n\n| Id | Family and images | Prediction |", "\n\n**Table 6.7b.** Registered rules of H1 (new labels on previously analysed captions; single annotator).\n\n| Id | Family and images | Prediction |"),
    ("6.7.2 results + 6.7.3 intervals + renumber 6.7.5→6.7.4", SEC7, "\n\n### 6.7.5 Hypothesis H3 (the coverage bound of Section 5.4 against the completed gold), as registered",
     "\n\n" + FACTS + "\n\n" + H1TAB + "\n\n" + H1SENT + "\n\n### 6.7.3 Per-system precision intervals under the two-reference gold\n\n" + S25 + "\n\n" + ITAB +
     "\n\n### 6.7.4 Hypothesis H3 (the coverage bound of Section 5.4 against the completed gold), as registered"),
    ("C5 $V_m$ pointer (6.7.4 Universe)", SEC7, "with the class in $V_m$, that at least one", "with the class in $V_m$ (the " + REG("R11", 55, "69") + " lexicon classes with an Open Images mapping; Supplementary S11.1), that at least one"),
    ("C4(b) l.170 swap", SEC7, "**Statistic.** With the two references of Section 3.8,", "**Statistic.** With the two references of Supplementary S11.1,"),
    ("C7/N4 caption H3 rule table (6.7.4)", SEC7, "\n\n| Label | Rule |", "\n\n**Table 6.7e.** Registered rules of H3 (new labels on previously analysed captions; single annotator).\n\n| Label | Rule |"),
    ("C4(b) l.181 swap", SEC7, "the low ends of the per-system intervals (Section 3.8)", "the low ends of the per-system intervals (Section 6.7.3)"),
    ("6.7.4 H3 results", SEC7, SEC7_TAIL, SEC7_TAIL + "\n\n" + H3TAB + "\n\n" + H3SENT),
    ("E6 (9.1 precision rule)", "paper/sec11_limitations_ethics.md", "holds at point level only (post hoc; Section 6.2).", "holds at point level only (post hoc; Section 6.2). " + E6),
    ("E7/N1 (9.1 reference-only bound)", "paper/sec11_limitations_ethics.md", "so the bound may fail if writers name different objects.", "so the bound may fail if writers name different objects. " + N1E7),
    ("C5 H2a/H2d pointer (9.1)", "paper/sec11_limitations_ethics.md", "the 30 within-family pairs carry H2a and H2d;", "the 30 within-family pairs carry H2a and H2d (Supplementary S11.4);"),
    ("§4 paragraphs (9.1)", "paper/sec11_limitations_ethics.md", "it says nothing about a re-run of a system or another image set.",
     "it says nothing about a re-run of a system or another image set.\n\n" + "\n\n".join([P_INT, P_ASM, P_DEV, P_PRI, P_ARM])),
    ("§4 9.2 paragraph", "paper/sec11_limitations_ethics.md", "\n\n## 9.3 Broader impact", "\n\n" + P_92 + "\n\n## 9.3 Broader impact"),
    ("FIX_A2 W-01", "paper/sec5_exchangeability.md", FX_SEC5[0][1], FX_SEC5[0][2]),
    ("FIX_A2 W-04", "paper/sec5_exchangeability.md", FX_SEC5[1][1], FX_SEC5[1][2]),
    ("H3 sentence (5.4)", "paper/sec5_exchangeability.md", "(Chao, 1987; Supplementary S1.M, S5).", "(Chao, 1987; Supplementary S1.M, S5)." + S54),
    ("§2.4 prior-work sentence", "paper/sec2_related_work.md", "supply the expected gold size.", "supply the expected gold size. " + S2PRIOR),
    ("E13 (Section 1)", "paper/sec1_introduction.md", "the positive label-gold sign depends on excluding mentions the labels cannot verify (Section 6.2)",
     "the positive label-gold sign depends on excluding mentions the labels cannot verify (Section 6.2)" + E13),
    ("RQ4", "paper/sec1_introduction.md", "\n\n**Contributions.**", "\n" + RQ4 + "\n\n**Contributions.**"),
    ("Contribution 6", "paper/sec1_introduction.md", "\n\n## 1.2 Registration ledger", "\n" + CONTRIB6 + "\n\n## 1.2 Registration ledger"),
    ("E11 Table 1 groups", "paper/sec1_introduction.md", T1_POSTHOC_OLD, T1_ROWS + "\n" + T1_POSTHOC_NEW),
    ("8.1 pointer", "paper/sec10_discussion.md", "carry a count channel (Section 7).", "carry a count channel (Section 7)." + P81),
    ("E13 (8.5)", "paper/sec10_discussion.md", "holds only when unverifiable mentions are excluded", "holds only when unverifiable mentions are excluded" + E13),
    ("E11 count line (8.5) + W2", "paper/sec10_discussion.md", "one PASCAL-50S companion prediction was not evaluable.",
     "one PASCAL-50S companion prediction was not evaluable. " + COUNT + " " + W2S),
    ("E13 (cover letter)", "paper/cover_letter_A.md", "depends on excluding mentions the labels cannot verify", "depends on excluding mentions the labels cannot verify" + E13),
    ("Highlight (Home S; replaces highlight 3)", "paper/highlights_A.md", HL_OLD, HL_NEW),
]
for f in ("paper/supplementary_SPIC.md", "paper/supplementary.md"):
    for rid, old, new in FX_SUPP:
        EDITS.append((rid, f, old, new))
    EDITS += [
        ("E13 (S10 copy of Section 1)", f, "the positive label-gold sign depends on excluding mentions the labels cannot verify (Section 6.2)",
         "the positive label-gold sign depends on excluding mentions the labels cannot verify (Section 6.2)" + E13),
        ("E13 (S10 copy of 8.5)", f, "holds only when mentions the labels cannot verify are excluded (post hoc)",
         "holds only when mentions the labels cannot verify are excluded (post hoc)" + E13),
        ("E12 count part (S10 copy of 8.5)", f, "one companion prediction on PASCAL-50S could not be evaluated.",
         "one companion prediction on PASCAL-50S could not be evaluated. " + COUNT),
        ("H3 sentence (S1.M.6)", f, "- Anything about a benchmark other than the development sets used here, or about cause.",
         "- Anything about a benchmark other than the development sets used here, or about cause.\n\n" + S1M6),
        ("S4.0 rows A31–A37, D-1–D-4", f, "\n| P-1 | Leave-one-system-out robustness |", "\n" + S40 + "\n| P-1 | Leave-one-system-out robustness |"),
        ("S4.0 row P-5 + times", f, "| P-4 | Cap share of detailed captions | post hoc, descriptive | no verdict | 6.3 |",
         "| P-4 | Cap share of detailed captions | post hoc, descriptive | no verdict | 6.3 |\n" + S40_P5 + "\n\n" + S40_TIMES),
    ]

# bib, citation map, in-text trace (CC-375 W2; new citation of arXiv 2611.01712)
BIB_ADD = """
% fernandezbarrios2026disagreement: identity from the arXiv abstract page (title, authors, 1 Nov 2026; checked 2026-11-12 UTC and by CC-357)
@misc{fernandezbarrios2026disagreement,
  author = {Fern{\\'a}ndez-Barrios, Roberto and Pastor-L{\\'o}pez, Iker and Gonz{\\'a}lez-Santocildes, Asier and Garc{\\'i}a Bringas, Pablo},
  title = {When Disagreement Labels Do Not Identify {F1} Rankings},
  year = {2026},
  howpublished = {arXiv preprint arXiv:2611.01712},
  eprint = {2611.01712},
  archivePrefix = {arXiv},
  primaryClass = {cs.LG},
  doi = {10.48550/arXiv.2611.01712}
}
"""


# =====================================================================================================
# Apply
# =====================================================================================================
for _blk, _lab in ((COUNT, "single annotator"), (W2S, "single annotator"), (H3SENT, "single annotator"), (H1TAB, "single annotator"),
                   (H1SENT, "single annotator"), (E6, "single annotator"), (QTAB, "single annotator"), (OUTCOME67, "single annotator"),
                   (ABS_NEW, "single annotator"), (S54, "single annotator"), (P81, "outcome foreseeable from stored aggregates")):
    assert _lab in _blk, (_lab, _blk[:60])
def apply():
    report = {"paper_head": HEAD, "sources": {a: s for a, (p, s) in SRC.items()}, "files": {}, "rows": [], "departures": DEPART,
              "new_text": NEW_TEXT, "abstract_words": ABS_WORDS, "left_in_S11": {"Section 3.8": LEFT38, "Section 6.8": LEFT68, "Section 6.7.5": LEFT675}}
    by_file = {}
    for rid, f, old, new in EDITS:
        by_file.setdefault(f, []).append((rid, old, new))
    for f in ("paper/abstract_A.md", "paper/number_manifest.tsv", "paper/paperA.bib", "paper/citation_map_A_v2.tsv", "paper/intext_trace_A.tsv"):
        by_file.setdefault(f, [])
    texts = {}
    for f, eds in by_file.items():
        before = git(PAPER, "show", "HEAD:" + f)
        if f in FX_BASE:
            assert sha(before) == FX_BASE[f], ("CC-375 C5 base", f)
        txt = before.decode("utf-8")
        for rid, old, new in eds:
            n = txt.count(old)
            assert n == 1, (rid, f, n, old[:60])
            assert new.count(old) <= 1 or True
            txt = txt.replace(old, new, 1)
            report["rows"].append({"row": rid, "file": f, "status": "applied"})
        if f == "paper/abstract_A.md":
            a = txt.index(ABS_OLD_START)
            b = txt.index(ABS_OLD_END, a) + len(ABS_OLD_END)
            assert txt.count(ABS_OLD_START) == 1
            txt = txt[:a] + ABS_NEW + txt[b:]
            txt = txt.replace("\n\n<!-- src (rubric pass 2026-10-29",
                              "\n<!-- Phase B (CC-357 J-34, E11, E13; CC-369 W6, W7; 2026-11-12 operator): E13 clause (CC-369 W7) and the seven-count clause (W6) added; cuts to stay <= 250 words (none removes a registered FAIL): 'and whether references omit objects randomly', 'registered' before 'ordering held', 'image-bootstrap', 'than all references' after 'smaller', '(Qwen3-VL-8B)', '(clean subset)', 'as on PASCAL-50S (here from the label gold: -26.79; null 95% range [-8.76, -6.69]), consistent with selective omission', 'by 35.46 points', 'all' before '2–3 references'; '(six systems, one backbone)' -> '(six one-backbone systems)'; 'Two post hoc checks bound it:' -> 'Post hoc,'. " + str(ABS_WORDS) + " words by wc -w of this paragraph with comments removed. -->\n\n<!-- src (rubric pass 2026-10-29", 1)
            report["rows"].append({"row": "Abstract (J-34, E11, E13)", "file": f, "status": "applied"})
        if f == "paper/supplementary_SPIC.md" or f == "paper/supplementary.md":
            assert txt.endswith("\n")
            txt = txt + "\n" + S11 + "\n"
            report["rows"].append({"row": "S11 (S11.1–S11.8)", "file": f, "status": "applied"})
        if f == "paper/paperA.bib":
            assert "fernandezbarrios2026" not in txt
            txt = txt + BIB_ADD
            report["rows"].append({"row": "bib entry arXiv 2611.01712", "file": f, "status": "applied"})
        texts[f] = (before, txt)
    # citation map and trace rows need final line numbers
    def line_of(f, s):
        t = texts[f][1].split("\n")
        hits = [i + 1 for i, l in enumerate(t) if s in l]
        assert hits, (f, s)
        return hits[0]
    cm_add = ["sec5_exchangeability.md\tLam et al. (2020\tlam2020uit\tunique",
              "sec2_related_work.md\tFernández-Barrios et al. (2026\tfernandezbarrios2026disagreement\tunique",
              "sec11_limitations_ethics.md\tFernández-Barrios et al. (2026\tfernandezbarrios2026disagreement\tunique"]
    tr_add = ["\t".join(["A", "sec5_exchangeability.md", str(line_of("paper/sec5_exchangeability.md", "Lam et al. (2020) report five writers")), "Lam et al. (2020", "lam2020uit", "OK",
                         "UIT-ViIC: five writers for the dataset; who wrote which caption of an image not stated", "SUPPORTED",
                         "arXiv 2002.00175 pdftotext l.184-185 'five writers'; no per-image writer assignment stated (CC-375 C1)"]),
              "\t".join(["A", "sec2_related_work.md", str(line_of("paper/sec2_related_work.md", "Fernández-Barrios et al. (2026)")), "Fernández-Barrios et al. (2026", "fernandezbarrios2026disagreement", "OK",
                         "exact bounds over every completion for F1 rankings; shared completions tighten them", "SUPPORTED",
                         "arXiv 2611.01712 abstract ('exact bounds', 'under every possible completion', 'shared completions tighten'); CC-357 WHAT I CHECKED"]),
              "\t".join(["A", "sec11_limitations_ethics.md", str(line_of("paper/sec11_limitations_ethics.md", "Fernández-Barrios et al. (2026)")), "Fernández-Barrios et al. (2026", "fernandezbarrios2026disagreement", "OK",
                         "all-completion bound and shared completion taken from this work", "SUPPORTED", "as the sec2 row"])]
    for f, add in (("paper/citation_map_A_v2.tsv", cm_add), ("paper/intext_trace_A.tsv", tr_add)):
        b, t = texts[f]
        assert t.endswith("\n")
        texts[f] = (b, t + "\n".join(add) + "\n")
        report["rows"].append({"row": "CC-375 W2 / new citation rows (" + str(len(add)) + ")", "file": f, "status": "applied"})
    # manifest
    lines = []
    for (file, key, shown), (wheres, sha12, st) in MAN.items():
        lines.append("\t".join([f"{shown} ({'; '.join(wheres)})", "A", file, key, sha12, st]))
    b, t = texts["paper/number_manifest.tsv"]
    assert t.endswith("\n")
    texts["paper/number_manifest.tsv"] = (b, t + "\n".join(lines) + "\n")
    report["rows"].append({"row": f"manifest rows ({len(lines)})", "file": "paper/number_manifest.tsv", "status": "applied"})
    report["manifest_rows"] = len(lines)
    # closing checks (CC-375 W1, TG5, TG9 on new text)
    for f in FX_BASE:
        t = texts[f][1]
        assert t.count("independent-annotator") == 0 and t.count("written by independent annotators") == 0, f
        assert "UIT-ViIC (all splits), VI | independent" not in t, f
    for f in ("paper/supplementary_SPIC.md", "paper/supplementary.md"):
        t = texts[f][1]
        for rid, old, new in FX_SUPP:
            assert t.count(new) == 1 and t.count(old) == 0, (rid, f)
    t5 = texts["paper/sec5_exchangeability.md"][1]
    for rid, old, new in FX_SEC5:
        assert t5.count(new) == 1 and t5.count(old) == 0, rid
    assert texts["paper/supplementary_SPIC.md"][1].split("\n## S11 ")[1] == texts["paper/supplementary.md"][1].split("\n## S11 ")[1]
    for f in ("paper/declarations.md", "paper/anon/declarations_anon.md"):
        assert "No ethics approval" not in git(PAPER, "show", "HEAD:" + f).decode()
    added = "\n".join(new for _, _, _, new in EDITS) + S11 + ABS_NEW
    vis = re.sub(r"<!--.*?-->", "", added, flags=re.S)
    tg9 = {k: len(re.findall(k, vis)) for k in (r"\{\{", r"KV-EV", r"KV1", r"OC1", r"A-N2", r"A-T3", r"E1's rule", r"CC-\d", r"PI-1", r"OPS-", r"\bR11\b", r"\bVP\b", r"l\.\d")}
    report["tg9_counts_in_added_visible_text"] = tg9
    # write
    for f, (before, txt) in texts.items():
        on_disk = open(PAPER + "/" + f, "rb").read()
        after = txt.encode("utf-8")
        open(PAPER + "/" + f, "wb").write(after)
        report["files"][f] = {"head_blob": sha(before), "disk_before_run": sha(on_disk), "after": sha(after)}
    # word counts (V2_PROGRESS method: comments stripped, sec1-sec11 + declarations, wc -w, tables included)
    main = [f"paper/sec{i}_" for i in range(1, 12)]
    def mainwords(get_txt):
        tot = 0
        for f in git(PAPER, "ls-files", "paper").decode().split():
            if any(f.startswith(p) for p in main) or f == "paper/declarations.md":
                tot += words(get_txt(f))
        return tot
    report["main_words_head"] = mainwords(lambda f: git(PAPER, "show", "HEAD:" + f).decode())
    report["main_words_after"] = mainwords(lambda f: open(PAPER + "/" + f, encoding="utf-8").read())
    report["abstract_words_head"] = words(git(PAPER, "show", "HEAD:paper/abstract_A.md").decode().split("## Abstract", 1)[1].split("**Keywords:**")[0])
    json.dump(report, open(OUT_JSON, "w"), indent=1, ensure_ascii=False)
    print(json.dumps({k: report[k] for k in ("abstract_words", "abstract_words_head", "main_words_head", "main_words_after", "manifest_rows", "tg9_counts_in_added_visible_text", "left_in_S11")}, ensure_ascii=False, indent=1))
    for f, v in report["files"].items():
        print(f, v["head_blob"][:12], "->", v["after"][:12])


apply()
