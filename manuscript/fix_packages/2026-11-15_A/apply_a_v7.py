#!/usr/bin/env python3
"""Paper A fix package v7 (A_FIX_PACKAGE_v7.md): rebuild the changed files in memory and, only on request, write them.

Source of the items: the three full reads of 2026-11-15 (manuscript/reviews/A_FULLREAD_sec2-5, _sec6-11, _supp_S1-S10),
ruling CC-422 (N9, W4) and CC-412 item N1.
Blocks (OLD/NEW pairs of the package): M main text outside the held places, T one line of Table 1, G the record of the
registered third sentence of Section 6.4, D declarations, S supplement S1-S10 and one entry of its reference list,
B one author field of paperA.bib.
Steps that are not blocks: S1 manifest rows; W4 the a_m1 result file into the release results with its PROVENANCE row;
S2 published supplement and provenance table from scrub(); S3 length comment of abstract_A.md.

Default mode: CHECK ONLY. Nothing is written. The script
  1. checks the pin of the package, that BASE_COMMIT is HEAD or an ancestor of HEAD, a clean tree, and that every
     file it reads has its sha256 of BASE_COMMIT;
  2. applies each block to `git show HEAD:paper/<file>` (OLD exactly once at HEAD, NEW absent), then the steps;
  3. rebuilds Tables S3.2 and S3.3 from the result file and the committed table file and compares them with the
     package text; re-reads the sha256 prefix of every source file named by a new manifest row;
  4. asserts the custody rules: the part of sec7_verbosity_sign.md from the heading of Section 6.7 on, Supplementary
     S11 (up to the next level-2 heading) in both supplement files, lines 15-31 of Section 9.1, every line of Section 1
     except the one row of Table 1, the abstract body, the cover letter, the highlights, the title page and the
     anonymised declarations stand byte-unchanged; in the five other lines that hold a sentence on the held study,
     each such sentence stands unchanged; no run of 8 words of Section 6.7, S11, the printed abstract or the highlights
     occurs in the package or in this script;
  5. asserts that the count of printed agreement clauses is unchanged in every file and that no block adds wording
     on AI tools;
  6. prints the sha256 of every resulting file and compares it with TARGETS.

Write mode:  python3 -I -B apply_a_v7.py --write --ruling CC-xxx
  writes the files to the working tree only if every result equals TARGETS. TARGETS hold only for the SKIP below;
  if the ruling drops or adds a block or a step, set SKIP and replace TARGETS by the values the ruling fixes.
  Never runs git add or git commit. `--repo <path>` points the script at a scratch clone for a test.
"""
import hashlib
import json
import pathlib
import posixpath
import re
import statistics
import subprocess
import sys
from decimal import ROUND_HALF_UP, Decimal

sys.dont_write_bytecode = True
HERE = pathlib.Path("/mnt/d/vsps_image_captioning")
DIR = HERE / "manuscript/fix_packages/2026-11-15_A"
PACKAGE = "A_FIX_PACKAGE_v7.md"
PIN = "bfc9b7d5285fdc7559e38075f35ff02b74653ac762b614684a7c927bbb54e8aa"
BASE_COMMIT = "a7f2b4e"
SKIP = ("A7-G01a",)  # block ids or steps ("S1", "W4", "S3") the ruling does not apply; A7-G01a and A7-G01b exclude each other
BASE = {
    "abstract_A.md": "7712224f8dfc0b90264eb816abb266e4957f6c20f82986cdf99507e245ad3ed2",
    "anon/declarations_anon.md": "e407d32ddd13b2903482472e35cf011e71177ea23f271425e9e38f60ee5172ca",
    "cover_letter_A.md": "7c14bb274f6e50c47abdbaceeebacad22da86d52043ac731dbac6835b8737957",
    "declarations.md": "69ceb15e18535fca9e50664b8b0dd20e4ec421739a827fc4c70f7f54f85e5906",
    "highlights_A.md": "64c671615bd5106cba42cf168ff7ff85460bd9bd72b3c52a2d9903861c281aa5",
    "number_manifest.tsv": "f5d517cc56df8302fd43996f677bbead29f6fd0bfd95029b08620cc83de91b07",
    "paperA.bib": "5a215e170422ce8fa49173c44775086228647ce32b19753b522892804f09bcdc",
    "sec1_introduction.md": "77b0b27f5c22d36af4258ad520e47d60c5ebe4c394d2816b16cdb62648fda885",
    "sec2_related_work.md": "5beb9da16eec16b2c7afb67bb3512fa3422ea0b9e0a4e85fd311ed30224a38c4",
    "sec3_measurement_setup.md": "665c60aa1956df8dedab070db395bd794297fec88cf07d7242c6bc7c31e74575",
    "sec4_theory.md": "50024781b9b1b658f1671db39c846a72863b5dcb2ce2506041d6943a612c1d01",
    "sec5_exchangeability.md": "9167bd8ce84bf8ef6e8ed65ba2e93abde128328d3daf8f289e910f0097dcfa27",
    "sec7_verbosity_sign.md": "b6f46b8aaf33ef133b54e5e4d91f2c1f037e061d48f495e1b23eed5b0aaf4817",
    "sec8_human_validity.md": "4572367c38fbb12dda6cf4786f41ce64e692f583c95e233fecd13499b3dc182d",
    "sec10_discussion.md": "d48ce382b275e73e3f6de34e08814f7c7205a51fb394d5742ed382f9e8e252bf",
    "sec11_limitations_ethics.md": "f2ed5f541fc6b5cb1035f60819ffc48f56f98becdf88276f978e8019e55bcef2",
    "supplementary.md": "ee67e7c1845e23113704e903c3f807c3a335f1c55f03f8052fe6b5f3a6df1eed",
    "supplementary_SPIC.md": "f52b658c279cc53370f6449eb893ec230121f879bf8212a9539300d086cc575b",
    "supplementary_provenance_internal.tsv": "1fcc915f39f77aa287429766402ccd4c335ebbcb102eda6d4fa69e282d437d62",
    "title_page_A.md": "2b0d17c1938d8fc2d2d602f705c35ab4351d4eb5a9a8329fe66fede693d8f87b",
    "../PROVENANCE.md": "6daa00e9217337e65d111f360dfacf46857be3a34ba7525bcd31a9d9d163c698",
}
NOT_WRITTEN = {"highlights_A.md", "title_page_A.md", "cover_letter_A.md", "anon/declarations_anon.md"}
RESULT_COPY = "../results/data/results/a_m1/a_m1_result.json"
WRITABLE = set(BASE) - NOT_WRITTEN | {RESULT_COPY}
COMMENT_ONLY = {"A7-G03"}
N_BLOCKS = 105
TARGETS = {
    "../PROVENANCE.md": "ee19795c2de5a872734a0587b9dcb4c670a79a77ed32cdd44cdf40f97c95382e",
    "../results/data/results/a_m1/a_m1_result.json": "5687a66b20785c626646d1b54934c590274c4a5244c4cb27150ab6292f00dcb4",
    "abstract_A.md": "5b3b482617ac75cc8942dea045e4e713300da207699c779ac334adb50479af41",
    "declarations.md": "8a34830ceedf189ae4ef4091814aa10162c3e9125ddee42376cd9559f433b603",
    "number_manifest.tsv": "1b0f01fca69856666391186d86b0d40c47ba9bec842679f38c9c93b831f10b3f",
    "paperA.bib": "753a2a5269458c8bb93027fd6460cb58b8df7d87ba5eee4e759e531a27e7fd30",
    "sec10_discussion.md": "5ec1a049e04fdaf83384570ee4b229ed3c8dd9b5480cb90ac75cf7ae2e676bcb",
    "sec11_limitations_ethics.md": "0d1d409afcf08d4eb1095a0d60af4ca328a2f98e84da4ebcde830ad9721d8e3d",
    "sec1_introduction.md": "1a7f0851df9ee79f66296531d6d9e59e8ebefd16f833453a5f3e32ba0e7e1aa8",
    "sec2_related_work.md": "29d97036fa4015079a519484304c59094cd21aaefcb40e9d486ba3b28d79ea8b",
    "sec3_measurement_setup.md": "ba8c15a499a34396a20b5b2a9010d122eadda762c3aca1988c9371620be5e3e7",
    "sec4_theory.md": "11a0e672302a3b0d06073f9e4890198f209bc982253b02694ff9c2ecc49ff5fa",
    "sec5_exchangeability.md": "ea3d21cf50430631a05fbd369d3d7cf3b01c114ebe122c407e571597a5a090cd",
    "sec7_verbosity_sign.md": "0d823927e932868a7883a59751b780f7545a8ec2bb8dfa5c26fe9e3b50a5e9b2",
    "sec8_human_validity.md": "539f58d45c1c90e8629b272cccb43e51f7aeb530fea6e76e0ada477021194d2b",
    "supplementary.md": "ad2213823a139ccf91b2d4650001916620b5a6a78413162ac7fc860cf4361ce5",
    "supplementary_SPIC.md": "c6a5229ec213de72f9198a55d1b0950dce48f7f730f071eefb82a48ae014ef5d",
    "supplementary_provenance_internal.tsv": "46addaa25bbab9f3aff2b0f52101bc034d7ba53d5e0ab92b26c9d2a409218f06",
}
MAIN = ["sec1_introduction.md", "sec2_related_work.md", "sec3_measurement_setup.md", "sec4_theory.md", "sec5_exchangeability.md",
        "sec6_rescoring_published_methods.md", "sec7_verbosity_sign.md", "sec8_human_validity.md", "sec9_preference_audit.md",
        "sec10_discussion.md", "sec11_limitations_ethics.md", "declarations.md"]
S67, S11, REFS = "\n## 6.7", "\n## S11 ", "\n## References for the Supplementary Material"
CLAUSE = "agreed to this use"
AI_WORDS = re.compile(r"\bAI\b|artificial intelligence|generative|ChatGPT|(?<!Mini)GPT-|Claude|Gemini|Copilot|writing assistant|language tool")
# lines outside the zones that hold a sentence on the held study: {file: lines}; the pattern marks such a sentence
HELD_LINES = {"sec5_exchangeability.md": [43], "sec7_verbosity_sign.md": [57], "sec10_discussion.md": [7, 29],
              "sec11_limitations_ethics.md": [11], "declarations.md": [27]}
HELD_MARK = re.compile(r"6\.7|S11|human completion|certificat|annotator|\bH\d[a-z]?\b|Part [PV]\b|completed gold|completion")
SENT = re.compile(r"(?<=[.:;])\s+(?=[A-Z*(\[])|(?=<!--)|(?<=-->)")
E1 = ".session_backup/2026-10-13/r10_cpu/e1_x1pb_verification_v2.json"
MDE_TEX = ".session_backup/2026-10-18/paperA_tasks/A8.5/appC_mde.tex"
A_M1 = "data/results/a_m1/a_m1_result.json"
A_M1_SHA = "5687a66b20785c626646d1b54934c590274c4a5244c4cb27150ab6292f00dcb4"
PROV_AFTER = "| `results/data/results/a_g0/g0.json` |"
PROV_ROW = "| `results/%s` | `%s` | clean | a245481 | `%s` | cited by draft |\n" % (A_M1, A_M1, A_M1_SHA)
CONTROLS = [("dP_raw", "raw"), ("dP_MCP_prefix", "matched prefix"), ("dP_MCP_sent_tieavg", "sentence tie-average"),
            ("dP_MCP_rand_exact", "uniform random subset")]

sha = lambda b: hashlib.sha256(b).hexdigest()
q2 = lambda x: Decimal(repr(x)).quantize(Decimal("0.01"), rounding=ROUND_HALF_UP)
signed = lambda x: ("+" if q2(x) > 0 else "−" if q2(x) < 0 else "") + str(abs(q2(x)))
cell = lambda v: "%s [%s, %s]" % (signed(v["est"]), signed(v["ci95"][0]), signed(v["ci95"][1]))
ascii_ = lambda s: s.replace("−", "-")


def tables():
    """Tables S3.2 and S3.3 and their manifest rows, from the result file and the committed table of detectable effects."""
    raw = (HERE / E1).read_bytes()
    tex = (HERE / MDE_TEX).read_bytes()
    pre = (sha(raw)[:12], sha(tex)[:12])
    assert pre == ("184f9ccac1b9", "ab2d63f5ddf5"), pre
    d = json.loads(raw)
    pairs = d["pairs_15"]
    labels = [[c.strip() for c in l.rstrip("\\ \n").split("&")] for l in tex.decode().split("\n") if l.count("&") == 14 and "unadj" not in l]
    assert len(labels) == len(pairs) == 15
    nd = statistics.NormalDist()
    z_ci, z_pow, z_bonf = nd.inv_cdf(0.975), nd.inv_cdf(0.8), nd.inv_cdf(1 - 0.05 / 15 / 2)
    t2 = ["**Table S3.2.** POST HOC per-comparison values behind Table S3.1 (not registered; no verdict). Precision gain of each "
          "published method over its baseline, in points, with its unadjusted 95% bootstrap interval: raw and under the three "
          "controls. Rows are in the order of the result file. LiM-EOS is the end-of-sequence stopping method of Yue et al. (2024).",
          "", "| Method | Baseline | Backbone | Images | Raw ΔP | Matched prefix | Sentence tie-average | Uniform random subset |",
          "|---|---|---|---|---|---|---|---|"]
    t3 = ["**Table S3.3.** Minimum detectable effect of each comparison of Table S3.2, in precision points (POST HOC; no "
          "verdict): normal approximation, 80% power, standard error from the width of the 95% interval. In each cell the first "
          "value is for α = 0.05 and the second for α = 0.05/15.",
          "", "| Method | Baseline | Backbone | Raw ΔP | Matched prefix | Sentence tie-average | Uniform random subset |",
          "|---|---|---|---|---|---|---|"]
    rows = []
    for (key, p), lab in zip(pairs.items(), labels):
        method, base, bone, n = lab[0], lab[1].replace("beam5", "beam search"), lab[2], int(lab[3])
        assert n == p["n_img"], key
        name = "%s vs %s, %s" % (method, base, bone)
        t2.append("| %s | %s | %s | %d | %s |" % (method, base, bone, n, " | ".join(cell(p[c]) for c, _ in CONTROLS)))
        mde = []
        for i, (c, word) in enumerate(CONTROLS):
            se = (p[c]["ci95"][1] - p[c]["ci95"][0]) / (2 * z_ci)
            pair = ["%.2f" % ((z + z_pow) * se) for z in (z_ci, z_bonf)]
            k = 4 + (0, 2, 5, 8)[i]
            assert pair == lab[k:k + 2], (key, c, pair, lab[k:k + 2])
            mde.append("; ".join(pair))
            rows.append("%s (Table S3.2: %s, %s)\tA\t%s\tpairs_15.%s.%s.{est,ci95}\t%s\tkeyed (POST HOC; supp Table S3.2; fix package v7)"
                        % (ascii_(cell(p[c])), name, word, E1, key, c, pre[0]))
            rows.append("%s (Table S3.3: minimum detectable effect, %s, %s; alpha 0.05 and 0.05/15)\tA\t%s\ttable row \"%s & %s & %s\", "
                        "columns of %s\t%s\tDERIVED (80%% power, se from pairs_15.%s.%s.ci95 of %s; recomputed by apply_a_v7.py and equal "
                        "to the row; POST HOC; fix package v7)" % (" / ".join(pair), name, word, MDE_TEX, lab[0], lab[1], lab[2], word, pre[1], key, c, E1))
        t3.append("| %s | %s | %s | %s |" % (method, base, bone, " | ".join(mde)))
    for c, k in [("dP_raw", "mean_dP_raw"), ("dP_MCP_prefix", "mean_dP_MCP_prefix"), ("dP_MCP_sent_tieavg", "mean_dP_MCP_sent_tieavg"),
                 ("dP_MCP_rand_exact", "mean_dP_MCP_rand_exact")]:
        assert abs(sum(p[c]["est"] for p in pairs.values()) / 15 - d["overview_15_pairs"][k]) < 0.0006, c
    return "\n".join(t2) + "\n\n" + "\n".join(t3), rows


def main():
    args = sys.argv[1:]
    write = "--write" in args
    ruling = args[args.index("--ruling") + 1] if "--ruling" in args else None
    repo = pathlib.Path(args[args.index("--repo") + 1] if "--repo" in args else "/mnt/d/vsps_papers/vsps-paperA-spic")
    assert not write or ruling, "--write needs --ruling <id of the GO ruling>"
    assert "A7-G01a" in SKIP or "A7-G01b" in SKIP, "A7-G01a and A7-G01b exclude each other"
    text = (DIR / PACKAGE).read_bytes()
    assert sha(text) == PIN, "pin differs: " + PACKAGE
    text = text.decode()
    run = lambda *a: subprocess.run(["git", "-C", str(repo), *a], capture_output=True)
    git = lambda *a: subprocess.run(["git", "-C", str(repo), *a], capture_output=True, check=True).stdout
    assert run("merge-base", "--is-ancestor", BASE_COMMIT, "HEAD").returncode == 0, BASE_COMMIT + " is not HEAD or an ancestor of HEAD"
    assert git("status", "--porcelain") == b"", "tree not clean"
    cache = {}

    def head(f):
        if f not in cache:
            cache[f] = git("show", "HEAD:" + posixpath.normpath("paper/" + f)).decode()
        return cache[f]

    for f, h in BASE.items():
        assert sha(head(f).encode()) == h, "base sha differs: " + f
    print("HEAD", git("rev-parse", "--short", "HEAD").decode().strip(), "| base", BASE_COMMIT, "is HEAD or an ancestor | SKIP", SKIP)
    printed = lambda t: re.sub(r"<!--.*?-->", "", t, flags=re.S)
    words = lambda t: len(printed(t).split())
    sys.path.insert(0, str(repo / "paper/build"))
    from scrub_supp import scrub, LEAK  # the functions only; the script is not run

    # the supplement zones: S11 runs from its heading to the next level-2 heading (CC-422 N2)
    src0 = head("supplementary.md")
    a0, b0 = src0.index(S11), src0.index(REFS)
    zone = src0[a0:b0]
    table_text, table_rows = tables()

    # blocks
    blocks = re.findall(r"<<<(A7-[A-Z]\d+[a-z]?) (\S+) OLD>>>\n(.*?)\n<<<\1 \2 NEW>>>\n(.*?)\n<<<\1 EVIDENCE>>>\n", text, flags=re.S)
    assert len(blocks) == N_BLOCKS and len({b[0] for b in blocks}) == N_BLOCKS, len(blocks)
    files, done = {}, []
    for bid, f, old, new in blocks:
        if bid in SKIP:
            continue
        assert f in WRITABLE, (bid, f)
        h = head(f)
        s = files.setdefault(f, h)
        assert h.count(old) == 1 and s.count(old) == 1 and h.replace(old, "").count(new) == 0, (bid, h.count(old), s.count(old))
        assert not AI_WORDS.search(printed(new)), bid + ": wording on AI tools"
        if f == "supplementary.md":
            assert not a0 - len(old) < h.index(old) < b0, bid + ": block inside S11"
        if f == "sec7_verbosity_sign.md":
            assert h.index(old) + len(old) < h.index(S67), bid + ": block inside Section 6.7"
        if bid == "A7-S08":
            assert table_text in new, "Tables S3.2 and S3.3 of the package differ from the result files"
        t = s.replace(old, new)
        assert (printed(t) == printed(s)) == (bid in COMMENT_ONLY), bid + ": printed text"
        files[f] = t
        done.append(bid)
    print("blocks applied: %d of %d (each OLD once at HEAD; no NEW at HEAD outside its OLD); Tables S3.2 and S3.3 rebuilt from "
          "the result file and equal to the package" % (len(done), N_BLOCKS))

    # S1: manifest rows
    if "S1" not in SKIP:
        rows = re.search(r"\*\*S1\. .*?\n```\n(.*?)\n```\n", text, flags=re.S).group(1).split("\n")
        man = head("number_manifest.tsv")
        assert man.endswith("\n") and rows[-120:] == table_rows, "manifest rows of the two tables differ from the result files"
        for r in rows:
            c = r.split("\t")
            assert len(c) == 6 and c[1] == "A" and r + "\n" not in man, r[:60]
            assert sha((HERE / c[2]).read_bytes())[:12] == c[4], "source sha differs: " + c[2]
        files["number_manifest.tsv"] = man + "\n".join(rows) + "\n"
        print("S1: %d manifest rows; the sha256 prefix of each source file equals the file in the run repository" % len(rows))

    # W4: the a_m1 result file into the release results, with its PROVENANCE row (CC-422 W4)
    new_bytes = {}
    if "W4" not in SKIP:
        res = (HERE / A_M1).read_bytes()
        prov = head("../PROVENANCE.md")
        line = next(l for l in prov.split("\n") if l.startswith(PROV_AFTER))
        dest = repo / "paper" / RESULT_COPY
        assert sha(res) == A_M1_SHA and prov.count(line) == 1 and A_M1 not in prov and (not dest.exists() or dest.read_bytes() == res)
        assert not re.search(rb"/root|/home/|@|\d+\.\d+\.\d+\.\d+", res), "host path, address or e-mail in the result file"
        files["../PROVENANCE.md"] = prov.replace(line + "\n", line + "\n" + PROV_ROW)
        new_bytes[RESULT_COPY] = res
        print("W4: %s copied to results/ (sha256 %s, 19 manifest rows point to it) and one PROVENANCE row added" % (A_M1, A_M1_SHA[:12]))

    # S2: published supplement and provenance table
    out0, _ = scrub(src0)
    assert out0 == head("supplementary_SPIC.md"), "scrub(supplementary.md) != supplementary_SPIC.md at HEAD"
    zone_spic = out0[out0.index(S11):out0.index(REFS)]
    if "supplementary.md" in files:
        src = files["supplementary.md"]
        out, prov_rows = scrub(src)
        files["supplementary_SPIC.md"] = out
        files["supplementary_provenance_internal.tsv"] = ("comment_no\tsrc_line\theading\tvisible_text_before\tcomment\n"
                                                          + "".join("\t".join(r) + "\n" for r in prov_rows))
        a, b = out.index(S11), out.index(REFS)
        assert src.count(zone) == 1 and out.count(zone_spic) == 1 and out[a:b] == zone_spic, "S11 bytes changed"
        assert all(a < m.start() < b for m in LEAK.finditer(out)), "leak hit outside S11"
        print("S2: published supplement = scrub(source); S11 bytes unchanged in both files; leak hits only inside S11")

    # S3: counts of the length comment of abstract_A.md (before "## Abstract"); the abstract itself is not touched
    ab0 = head("abstract_A.md")
    cut = ab0.index("## Abstract")
    c0 = {f: words(head(f)) for f in MAIN}
    c1 = {f: words(files.get(f, head(f))) for f in MAIN}
    t0, t1 = sum(c0.values()), sum(c1.values())
    longest = lambda c: "Longest files: " + "; ".join("%s %s" % (f, format(n, ",")) for f, n in sorted(c.items(), key=lambda x: -x[1])[:3]) + "."
    print("main text words:", t0, "->", t1, {f: c1[f] - c0[f] for f in MAIN if c1[f] != c0[f]})
    top = ab0[:cut]
    if "S3" not in SKIP:
        for x, y in [
            ("recounted after fix package v6 of 2026-11-15).",
             "recounted after fix package v6 of 2026-11-15; recounted after fix package v7 of 2026-11-15)."),
            ("Main text now: %s words" % format(t0, ","), "Main text now: %s words" % format(t1, ",")),
            ("Over the limit by %s words." % format(t0 - 8500, ","), "Over the limit by %s words." % format(t1 - 8500, ",")),
            (longest(c0), longest(c1)),
        ]:
            assert top.count(x) == 1, x
            top = top.replace(x, y)
        files["abstract_A.md"] = top + ab0[cut:]

    # custody
    res = lambda f: files.get(f, head(f))
    assert set(files) <= WRITABLE and not set(files) & NOT_WRITTEN, sorted(set(files) - WRITABLE)
    tail = lambda s, mark: s[s.index(mark):]
    assert tail(res("sec7_verbosity_sign.md"), S67) == tail(head("sec7_verbosity_sign.md"), S67), "Section 6.7 changed"
    assert tail(res("abstract_A.md"), "## Abstract") == tail(ab0, "## Abstract"), "abstract body changed"
    lines = lambda t: t.split("\n")
    s1a, s1b = lines(head("sec1_introduction.md")), lines(res("sec1_introduction.md"))
    assert len(s1a) == len(s1b) and [i + 1 for i in range(len(s1a)) if s1a[i] != s1b[i]] in ([], [48]), "Section 1 changed outside l.48"
    s9a, s9b = lines(head("sec11_limitations_ethics.md")), lines(res("sec11_limitations_ethics.md"))
    assert s9a[14:31] == s9b[14:31], "Section 9.1 l.15-31 changed"
    n_held = 0
    for f, nums in HELD_LINES.items():
        for n in nums:
            for part in SENT.split(lines(head(f))[n - 1]):
                if HELD_MARK.search(part):
                    assert part in res(f), "%s l.%d: a sentence on the held study changed" % (f, n)
                    n_held += 1
    held = " ".join([tail(head("sec7_verbosity_sign.md"), S67), zone, zone_spic, printed(tail(ab0, "## Abstract")), head("highlights_A.md")])
    grams = lambda t: {" ".join(w[i:i + 8]) for w in [re.findall(r"\w+", t.lower())] for i in range(len(w) - 7)}
    hits = len(grams(held) & (grams(text) | grams(pathlib.Path(__file__).read_text(encoding="utf-8"))))
    assert hits == 0, "%d runs of 8 words of a held zone occur in the package or the script" % hits
    for f in sorted(set(BASE) - {"number_manifest.tsv", "supplementary_provenance_internal.tsv", "paperA.bib", "../PROVENANCE.md"}):
        n0, n1 = printed(head(f)).count(CLAUSE), printed(res(f)).count(CLAUSE)
        assert n0 == n1, f + ": agreement clauses %d -> %d" % (n0, n1)
    print("custody: Section 6.7, S11, the abstract body, Section 9.1 l.15-31 and Section 1 outside l.48 byte-unchanged; cover letter, "
          "highlights, title page and anonymised declarations not written; %d sentences on the held study in 6 other lines unchanged; "
          "0 shared runs of 8 words with Section 6.7, S11, the printed abstract, the highlights; agreement clauses unchanged in every file" % n_held)

    data = {f: s.encode() for f, s in files.items()}
    data.update(new_bytes)
    got = {f: sha(b) for f, b in sorted(data.items())}
    for f, h in got.items():
        print("OK   " if TARGETS.get(f) == h else "DIFF ", f, h)
    same = got == TARGETS
    print("ALL RESULTS EQUAL TARGETS" if same else "RESULTS DIFFER FROM TARGETS (with another SKIP, the targets are those of the ruling)")
    if write:
        assert same, "no file written: results differ from TARGETS"
        for f, b in data.items():
            p = repo / posixpath.normpath("paper/" + f)
            p.parent.mkdir(parents=True, exist_ok=True)
            p.write_bytes(b)
        print("WRITTEN under ruling %s: %d files to the working tree of the paper repository (not staged, not committed)" % (ruling, len(data)))
    else:
        print("CHECK MODE: nothing written")


if __name__ == "__main__":
    main()
