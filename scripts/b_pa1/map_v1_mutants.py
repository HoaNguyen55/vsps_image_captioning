#!/usr/bin/env python3
"""Guard mutants for map_v1.py (DRAFT). New harness; the committed mutants.py is only imported (its tree()), never
edited. Each mutant breaks one guard in a scratch copy and must make `map_v1.py selftest` fail, offline (unshare -rn).
Run:  python3 -I -B scripts/b_pa1/map_v1_mutants.py
"""
import shutil
import subprocess
import sys
import tempfile
from pathlib import Path

HERE = Path(__file__).resolve().parent
sys.path.insert(0, str(HERE))
from mutants import tree  # noqa: E402  scratch scripts/ of symlinks, so common.ROOT stays the repo

F = "map_v1.py"
MUT = [  # (id, old, new): each old must occur exactly once
    ("X1 crosswalk unique", "if len(hit) == 1:", "if hit:"),
    ("X2 dictionary tag", 'links[c["id"]] = (hit.pop(), "dictionary")', 'links[c["id"]] = (hit.pop(), "instrument")'),
    ("X3a entry COCO-80", 'if e.get("coco80") not in coco or not str(e.get("why", "")).strip():',
     'if not str(e.get("why", "")).strip():'),
    ("X3b entry reason", 'if e.get("coco80") not in coco or not str(e.get("why", "")).strip():',
     'if e.get("coco80") not in coco:'),
    ("X4 alias name listed", 'if part != "none" and e.get("o365") not in ids:', "if False:"),
    ("X5a alias add-only (linked)", "if i in links or i in struck:", "if i in struck:"),
    ("X5b alias add-only (struck)", "if i in links or i in struck:", "if i in links:"),
    ("S1a strike = dictionary link", 'if links.get(i) != (e["coco80"], "dictionary"):', "if False:"),
    ("S1b strike names its class", 'if links.get(i) != (e["coco80"], "dictionary"):', "if i not in links:"),
    ("S2 strike removes", "        del links[i]\n", "        pass\n"),
    ("S3 mandatory completeness", "if set(gap) - set(none):", "if False:"),
    ("S4a none not repeated", "if len(set(none)) != len(none) or set(none) - set(gap):", "if set(none) - set(gap):"),
    ("S4b none only unlinked", "if len(set(none)) != len(none) or set(none) - set(gap):",
     "if len(set(none)) != len(none):"),
    ("S5 strike count", '"strikes": len(struck),', '"strikes": 0,'),
    ("S6 alias provenance", 'if not isinstance(who, dict) or not all(str(who.get(f, "")).strip() for f in',
     'if False and all(str(who.get(f, "")).strip() for f in'),
    ("X6 first wins", "if v not in seen:", "if True:"),
    ("X7 distinct ids", 'if len(cats) != n or len({c["id"] for c in cats}) != n:', "if len(cats) != n:"),
    ("X8 lexicon classes", "if {k for _, k in vi_terms} - set(coco):", "if False:"),
    ("X9 row tag", '"o365_id": i, "tag": links[i][1]}', '"o365_id": i, "tag": "dictionary"}'),
    ("X10 map cites crosswalk", '"crosswalk_sha256": sha(xw),', '"crosswalk_sha256": None,'),
    ("B1 class list name", "if a.categories.name != CAT_NAME or not", "if not"),
    ("B2 class list pin", ' or not B.pin_line(log, sha(cat_b), CAT_NAME, f"n={n}"):', ":"),
    ("B3 n= token", 'CAT_NAME, f"n={n}"):', "CAT_NAME):"),
    ("B4 R7 pins", '"r7": {r: pinned(log, r, root) for r in R7}', '"r7": {r: B.K.sha_file(root / r) for r in R7}'),
    ("B5 R3 addendum pins", "**{r: pinned(log, r, root) for r in SRC}", "**{r: B.K.sha_file(root / r) for r in SRC}"),
    ("B6 R3 rescap pins", "**{r: pinned(log, r) for r in rels}", "**{r: B.K.sha_file(ROOT / r) for r in rels}"),
    ("B7 RESCAP_RAW_TONE", 'if "RESCAP_RAW_TONE" in os.environ:', "if False:"),
    ("B8 alias pin", "if a.alias.name != ALIAS_NAME or not B.pin_line(log, sha(al_b), ALIAS_NAME):", "if False:"),
    ("B9 out-dir tracked tree", "if root.resolve() in out.parents and", "if False and"),
    ("P1 231 ids", "if len(want) != N_IMAGES or set(refs) != want:", "if set(refs) != want:"),
    ("P2 refs = ids", "if len(want) != N_IMAGES or set(refs) != want:", "if len(want) != N_IMAGES:"),
    ("P3 gold rows", "if want - set(inst):", "if False:"),
    ("P4 all references", "for text in refs[i]:", "for text in refs[i][:5]:"),
    ("P5 micro over mentions", "acc[s][1] += len(m)", "acc[s][1] += 1"),
    ("P6 v2 = vi_objects (LEX_V2)", '("v2", sc.vi_objects(text, v2_terms))', '("v2", sc.vi_classes(text, v2_terms))'),
    ("P7 new = same procedure", "for v in sc.vi_objects(text, new_terms):", "for v in sc.vi_classes(text, new_terms):"),
    ("P8 crosswalk drop", "new |= {to80[c] for c in ids if c in to80}", "new |= {to80.get(c, 'x') for c in ids}"),
    ("P9 stop rule strict", "return abs(delta) > LIMIT", "return abs(delta) >= LIMIT"),
    ("P10 limit 2.0", "LIMIT = Fraction(2)", "LIMIT = Fraction(201, 100)"),
    ("P12 3-dp rounding (N3)", 'round(float(p["delta"]), 3)', 'float(p["delta"])'),
    ("P11 W1 whitelist", '"run": "parity1",', '"run": "parity1", "delta_micro_exact": str(p["delta"]),'),
    ("C1 map name", "if a.map.name != MAP_NAME or", "if"),
    ("C2 map-crosswalk pair", ' or mp.get("crosswalk_sha256") != xsha:', ":"),
    ("C3 freeze pin", "if not B.pin_line(log, *freeze):", "if False:"),
    ("C4 freeze R7 tokens", 'mp["categories_sha256"], *mp["r7"].values(),', 'mp["categories_sha256"],'),
    ("C4b freeze alias token", 'mp["r7"].values(),\n              *([mp["alias_sha256"]] if mp["alias_sha256"] else []))',
     'mp["r7"].values())'),
    ("C5 sources = map's", 'if r3(log, root) != mp["sources"]:', "if r3(log, root) is None:"),
    ("C6 exclusion pin", "if sha(ex_b) != B.EX_SHA:", "if False:"),
    ("C7 one start line", "if len(starts) != 1 or", "if not starts or"),
    ("C8 start after freeze", " or starts[0] < min(at(lines, B.PIN_RE, *freeze)):", ":"),
    ("C9 start gold token", "sha(refs_b), sha(gold_b), B.EX_SHA, here)", "sha(refs_b), B.EX_SHA, here)"),
    ("C10 start anchored", '_OPS = r"^\\d{4}', '_OPS = r"\\d{4}'),
    ("C11 delimited tokens", "ts = [B.delimited(t) for t in toks]", "ts = [re.compile(re.escape(t)) for t in toks]"),
    ("C12 done line", "if at(lines, DONE_RE, msha):", "if False:"),
    ("C13 once (O_EXCL)", "os.O_WRONLY | os.O_CREAT | os.O_EXCL, 0o644)  # once",
     "os.O_WRONLY | os.O_CREAT | os.O_TRUNC, 0o644)  # once"),
    ("C14 inputs before the lock",
     '    refs, gold = load_inputs(json.loads(ex_b)["ids"]["coco"]["uitviic_test"], refs_b, gold_b)\n'
     "    xw, v2_terms = json.loads(xw_b), load()\n"
     "    fd = os.open(a.map.parent / OUT_NAME, os.O_WRONLY | os.O_CREAT | os.O_EXCL, 0o644)  # once: before computing\n"
     '    with os.fdopen(fd, "wb") as f:\n',
     "    fd = os.open(a.map.parent / OUT_NAME, os.O_WRONLY | os.O_CREAT | os.O_EXCL, 0o644)  # once: before computing\n"
     '    with os.fdopen(fd, "wb") as f:\n'
     '        refs, gold = load_inputs(json.loads(ex_b)["ids"]["coco"]["uitviic_test"], refs_b, gold_b)\n'
     "        xw, v2_terms = json.loads(xw_b), load()\n"),
    ("C15 run-dir token", "B.EX_SHA, here)", "B.EX_SHA)"),
]


def run(d: Path) -> tuple[bool, str]:
    r = subprocess.run(["unshare", "-rn", "/usr/bin/python3", "-I", "-B", F, "selftest"], cwd=d,
                       capture_output=True, text=True, timeout=300)
    tail = [x for x in (r.stderr or r.stdout).splitlines() if x.strip()]
    return r.returncode == 0, (tail[-1][:100] if tail else str(r.returncode))


def main() -> int:
    root = Path(tempfile.mkdtemp(prefix="map_v1_mut_"))
    try:
        d = tree(root)
        ok, why = run(d)
        assert ok, f"control fails: {why}"
        print("control: selftest passes on the unmutated file")
        src, survived = (HERE / F).read_text(encoding="utf-8"), []
        for mid, old, new in MUT:
            if src.count(old) != 1:
                print(f"{mid}: PATTERN NOT FOUND ONCE ({src.count(old)})")
                survived.append(mid)
                continue
            (d / F).unlink()
            (d / F).write_text(src.replace(old, new), encoding="utf-8")
            ok, why = run(d)
            print(f"{mid}: {'SURVIVED' if ok else 'KILLED'} {why}", flush=True)
            survived += [mid] if ok else []
            (d / F).unlink()
            (d / F).symlink_to(HERE / F)
        print(f"{len(MUT) - len(survived)}/{len(MUT)} killed; survived: {survived or 'none'}")
        return 1 if survived else 0
    finally:
        shutil.rmtree(root)


if __name__ == "__main__":
    sys.exit(main())
