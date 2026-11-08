#!/usr/bin/env python3
"""D-8 part (i) validator (B_RUN_DOC v1.1 §1.1 F-2; D8_AMENDMENT_DRAFT_v1_3.md §7, the (i) pin line's "validate:").
Laptop only, /usr/bin/python3, stdlib + repo. DRAFT, not read.

    python3 -I -B scripts/b_pa1/b_pa1_d8i_validate.py --entries-i E --coverage C [--entries-ii E2]
    python3 -I -B scripts/b_pa1/b_pa1_d8i_validate.py selftest

Step 4 rehearsed on scratch copies (B_RUN_DOC §11.2 items 4-5): the md's (i) pin form, filled with E's sha, is appended
to a copy of the LOG (lines (A) and (B) must already stand on the real LOG); then b_pa1_mid.cmd_amend with the (ii)
file, cmd_amend with E on the same scratch amendments log, and cmd_final. So an (i) term that collides with a (ii)
term fails here, not mid-run. Prints one counts-only line ending RESULT PASS|FAIL; never a term, token or class name.
Never writes the real LOG or the real amendments log.
"""
from __future__ import annotations

import argparse
import contextlib
import io
import json
import re
import sys
from pathlib import Path

HERE = Path(__file__).resolve().parent
sys.path[:0] = [str(HERE), str(HERE.parent)]
import b_pa1 as B  # noqa: E402
import b_pa1_gpu as G  # noqa: E402  scratch (no recursive delete)
import b_pa1_mid as M  # noqa: E402  cmd_amend, cmd_final, LOG_RE, norm, sha
import map_v1 as MV  # noqa: E402

ROOT = B.K.ROOT
MD = "manuscript/prereg/2026-11-01_b_pa1_tier1/D8_AMENDMENT_DRAFT_v1_3.md"
EN_I = "b_pa1_d8_i_entries_v1.json"  # the name on the md's (i) pin form
D8 = ROOT / ".session_backup/2026-11-08/b_pa1/d8_ii"
EN_II = D8 / "b_pa1_d8_ii_entries_v1_3.json"
MAP1 = ROOT / ".session_backup/2026-11-03/b_pa1/map_v1_build2" / MV.MAP_NAME
CATS = ROOT / ".session_backup/2026-11-02/b_pa1" / MV.CAT_NAME
FORM = "<date -u +%FT%TZ> OPS-<MMDD>b-d8i-pin: "


def run(fn, a, log: Path) -> tuple[str, str]:
    try:
        with contextlib.redirect_stdout(io.StringIO()) as o:
            fn(a, log=log)
        return "ok", o.getvalue().strip()
    except SystemExit as e:
        return "REFUSED", str(e)


def added(r: tuple[str, str]) -> int:
    return json.loads(r[1])["added"] if r[0] == "ok" else -1


def validate(ei: Path, cov: Path, eii: Path = EN_II, log: Path = B.LOG) -> tuple[bool, str]:
    sh = lambda p: M.sha(Path(p).read_bytes())  # noqa: E731
    ms, es1, es2, cs, mid = sh(ROOT / MD), sh(ei), sh(eii), sh(cov), sh(HERE / "b_pa1_mid.py")
    doc_i, doc_ii, cv = (json.loads(Path(p).read_bytes()) for p in (ei, eii, cov))
    n1, n2, n_v1 = len(doc_i["entries"]), len(doc_ii["entries"]), len(json.loads(MAP1.read_bytes())["terms"])
    toks = {M.norm(e["vi"]) for e in doc_i["entries"]}
    forms = [ln for ln in (ROOT / MD).read_text(encoding="utf-8").splitlines() if ln.startswith(FORM)]
    ok = {"one_form": len(forms) == 1, "name": ei.name == EN_I, "ab_on_log": B.pin_line(log, ms, MD) and
          B.pin_line(log, es2, eii.name), "provenance": (doc_i.get("provenance") or {}).get("amendment") ==
          {"name": MD, "sha256": ms}, "src_i": n1 > 0 and all(e.get("src") == "i" for e in doc_i["entries"]),
          "pulled_coverage": cv.get("classes_only") is False}
    line = forms[0] if forms else FORM
    for old, new in (("<date -u +%FT%TZ>", "2026-11-08T12:00:00Z"), ("<MMDD>", "1108"), ("<full 64-hex sha>", es1),
                     ("<8-hex>", ms[:8]), ("<8-hex>", cs[:8]), ("<8-hex>", mid[:8]), ("<id>", "000"),
                     ("<n>", str(n1)), ("<n>", str(len(toks))), ("<the quoted one-line result>", "TEST")):
        line = line.replace(old, new, 1)
    ok["form_filled"] = not re.search(r"<[^<>]+>", line) and bool(B.PIN_RE.match(line))
    with G.scratch("b_pa1_d8i_") as d:
        (d / "LOG.md").write_text(log.read_text(encoding="utf-8") + line + "\n", encoding="utf-8")
        ns = lambda e: argparse.Namespace(coverage=cov, map=MAP1, categories=CATS, entries=e, log=d / "amend.log")  # noqa: E731
        r2 = run(M.cmd_amend, ns(eii), d / "LOG.md")
        r1 = run(M.cmd_amend, ns(ei), d / "LOG.md")
        rows = (d / "amend.log").read_text(encoding="utf-8").splitlines() if (d / "amend.log").exists() else []
        rf = run(M.cmd_final, argparse.Namespace(map=MAP1, categories=CATS, log=d / "amend.log", out_dir=d / "final"),
                 d / "LOG.md")
        fm = json.loads((d / "final" / M.FINAL_NAME).read_bytes()) if rf[0] == "ok" else {"n_added": -1, "terms": []}
    ok["ii_added"], ok["i_added"] = added(r2) == n2, added(r1) == n1
    nre = sum(bool(M.LOG_RE.fullmatch(x)) for x in rows)
    ok["log_re"] = nre == len(rows) == n1 + n2 and {M.LOG_RE.fullmatch(x)[5] for x in rows} == {es1, es2}
    ok["final"] = fm["n_added"] == n1 + n2 and len(fm["terms"]) == n_v1 + n1 + n2
    word = lambda r: f"added {added(r)}" if r[0] == "ok" else "REFUSED(" + next(  # noqa: E731
        (w for w in ("W7", "add-only", "PI-1108e", "listed") if w in r[1]), "other") + ")"
    bad = [k for k, v in ok.items() if not v]
    return not bad, (f"validate_d8i code={sh(Path(__file__))[:8]} mid={mid[:8]} md={ms[:8]} entries_ii={es2[:8]} "
                     f"entries_i={es1[:8]} coverage={cs[:8]}: (A)+(B) on LOG {'yes' if ok['ab_on_log'] else 'NO'}; "
                     f"(ii) {word(r2)}/{n2}; (i) {word(r1)}/{n1} for {len(toks)} of {len(cv.get('tokens_i', []))} "
                     f"listed tokens; LOG_RE {nre}/{n1 + n2}; final {n_v1}+{fm['n_added']}; "
                     f"RESULT {'PASS' if not bad else 'FAIL ' + ','.join(bad)}")


def selftest() -> int:
    """A synthetic (i) token and entry pass. Each broken fixture fails on its own check: an (i) entry reusing a (ii)
    term (read here, never printed), another file name, another amendment sha, a src ii entry, the classes-only
    coverage, a LOG without lines (A) and (B)."""
    ii = json.loads(EN_II.read_bytes())["entries"][0]
    clash, cls = M.norm(ii["vi"]), ii["o365"]
    cov = json.loads((D8 / "coverage_classes_only" / M.COV_NAME).read_bytes())
    ms, tok = M.sha((ROOT / MD).read_bytes()), "zzqbpa1selftest"
    want = {"good": None, "clash": "i_added", "name": "name", "provenance": "provenance", "src": "src_i",
            "classes_only": "pulled_coverage", "no_ab": "ab_on_log"}
    with G.scratch("b_pa1_d8i_st_") as d:
        for c, only in (("cov_pulled", False), ("cov_classes", True)):
            (d / c).mkdir()
            (d / c / M.COV_NAME).write_text(json.dumps({**cov, "classes_only": only, "tokens_i": [
                {"token": tok, "df": 10}, {"token": clash, "df": 10}]}, ensure_ascii=False), encoding="utf-8")
        (d / "LOG_empty.md").write_text("", encoding="utf-8")
        res = {}
        for case in want:
            (d / case).mkdir()
            e = {"vi": clash if case == "clash" else tok, "src": "ii" if case == "src" else "i", "tag": "instrument",
                 "o365": cls, "why": "selftest", "drafter": "selftest"}
            am = {"name": MD, "sha256": ms if case != "provenance" else "0" * 64}
            f = d / case / (EN_I if case != "name" else "b_pa1_d8_i_entries_v2.json")
            f.write_text(json.dumps({"provenance": {"drafter": "selftest", "utc": "2026-11-08T12:00:00Z",
                                                    "amendment": am}, "entries": [e]}, ensure_ascii=False),
                         encoding="utf-8")
            res[case] = validate(f, d / ("cov_classes" if case == "classes_only" else "cov_pulled") / M.COV_NAME,
                                 log=d / "LOG_empty.md" if case == "no_ab" else B.LOG)
    assert res["good"][0] and res["good"][1].endswith("RESULT PASS"), res["good"][1]
    for case, key in want.items():
        if key:
            assert not res[case][0] and key in res[case][1].split("RESULT FAIL ")[-1].split(","), (case, res[case][1])
    assert "(i) REFUSED(add-only)/1" in res["clash"][1] and res["clash"][1].endswith("RESULT FAIL i_added,log_re,final")
    print(f"selftest b_pa1_d8i_validate ok (good PASS; {len(want) - 1} broken fixtures FAIL on their own check)")
    return 0


def main() -> int:
    if sys.argv[1:] == ["selftest"]:
        return selftest()
    ap = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    ap.add_argument("--entries-i", type=Path, required=True)
    ap.add_argument("--coverage", type=Path, required=True)
    ap.add_argument("--entries-ii", type=Path, default=EN_II)
    a = ap.parse_args()
    good, line = validate(a.entries_i, a.coverage, a.entries_ii)
    print(line)
    return 0 if good else 1


if __name__ == "__main__":
    sys.exit(main())
