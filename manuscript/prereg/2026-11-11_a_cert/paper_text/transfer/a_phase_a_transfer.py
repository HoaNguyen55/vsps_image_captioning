"""Paper A certification, PHASE A paper-text transfer (CC-357 Ruling 5).

Run: python3 -I a_phase_a_transfer.py
Starts from `git show HEAD:` of every target file, so re-running is idempotent.
Writes the paper repo working tree only; never stages or commits.
Opens no result file: only the package, BUILD.json and the paper files.
"""
import hashlib
import json
import subprocess
import sys

RUN = "/mnt/d/vsps_image_captioning"
PAPER = "/mnt/d/vsps_papers/vsps-paperA-spic"
PKG = RUN + "/manuscript/prereg/2026-11-11_a_cert/paper_text/A_CERT_PAPER_TEXT_v1.md"
PKG_SHA = "d2548abc379de4d9c6b0132865cdfe6fb39639f777c4503a15cb5e8aa7ed0b73"
BUILD = "manuscript/prereg/2026-11-11_xm600_gold_completion/BUILD.json"
BUILD_SHA = "d424fdcaa6a99b84c329a9a65edacff5f3654284fecfe5b716debfa6b5295d87"
HEAD = "e8aa602516a83a12a2ca6bf883748d53a81e0dfe"


def sha(b):
    return hashlib.sha256(b).hexdigest()


def git(repo, *args):
    return subprocess.run(["git", "-C", repo, *args], check=True, capture_output=True).stdout


pkg_bytes = open(PKG, "rb").read()
assert sha(pkg_bytes) == PKG_SHA, "package sha"
PKG_TXT = pkg_bytes.decode("utf-8")
L = PKG_TXT.split("\n")


def pl(n, prefix):
    """Package line n (1-based), asserted to start with prefix."""
    s = L[n - 1]
    assert s.startswith(prefix), (n, s[:60])
    return s


def rows(a, b):
    return "\n".join(L[a - 1:b])


assert git(PAPER, "rev-parse", "HEAD").decode().strip() == HEAD, "paper HEAD"

# ---- package paragraphs (byte copies) ----
s26 = [pl(197, "**Why labels were collected.**"), pl(200, "**Items.**"),
       pl(203, "**What the annotator saw.**"), pl(206, "**Blinding.**"),
       pl(209, "**Who labelled.**"), pl(212, "**Completed status.**"),
       pl(215, "**Quality measures"), pl(218, "**The kappa rule.**")]
s27 = [pl(223, "For each system on its image set"), pl(226, "**Image sets and bootstrap.**")]
s28 = [pl(231, "**H1.**"), rows(233, 237), pl(239, "Reported with H1b and H1c")]
assert L[232].startswith("| Id |") and L[236].startswith("| H1c |") and L[237] == ""
assert L[241].startswith("**Facts fixed before unsealing")  # excluded by CC-357 Ruling 5
s211 = [pl(285, "**Universe.**"), pl(287, "**Statistic.**"), rows(289, 294),
        pl(296, "VIOLATED means"), pl(299, "**H3 secondary rows")]
assert L[288].startswith("| Label |") and L[293].startswith("| NOT EVALUABLE |") and L[294] == ""
s212 = [pl(304, "**Freeze.**"), pl(307, "**One pass.**"), pl(310, "**Multiplicity.**")]
s4 = [pl(648, "**Construct and internal validity: the human-completed gold.**"),
      pl(651, "**Construct validity: what the labels are.**"),
      pl(660, "**Statistical conclusion validity: few, dependent comparisons.**")]

# ---- J-13 (tense follows the state at transfer; no second-annotator LOG line) ----
J13_OLD = "A second annotator, a colleague, answers every question of 150 of the images (25% of the images with a target, drawn with a fixed seed) with the same page and instructions, without seeing the first answers."
J13_NEW = "A second annotator, a colleague, will answer every question of 150 of the images (25% of the images with a target, drawn with a fixed seed) with the same page and instructions, without seeing the first answers, and has not yet labelled."
assert s26[4].count(J13_OLD) == 1
s26[4] = s26[4].replace(J13_OLD, J13_NEW)

# ---- headings (derived from package titles; no registered title exists for 6.7) ----
H67 = "## 6.7 A human completion of the XM3600-600 object gold (registered on new labels of previously analysed captions; development role)"
H671 = "### 6.7.1 The human-completed gold of XM3600-600"
H672 = "### 6.7.2 Hypotheses H1 (completed label-gold slope), as registered"
H675 = "### 6.7.5 Hypothesis H3 (the coverage bound of Section 5.4 against the completed gold), as registered"
BLOCK67 = "\n\n".join([H67, *s212, H671, *s26, *s27, H672, *s28, H675, *s211])
BLOCK91 = "\n\n".join(s4)

# every inserted paragraph except the J-13 one is a byte substring of the package
for p in [*s212, *s26, *s27, *s28, *s211, *s4]:
    if p is s26[4]:
        continue
    assert p in PKG_TXT, p[:60]

# ---- E-rows (package §1.3, CC-357 W17) ----
E1_OLD = "(iii) model-produced signals are never treated as gold or human evidence, and no new human annotation was collected"
E1_NEW = "(iii) model-produced signals are never treated as gold or human evidence; one set of new human labels was collected, for the object gold of XM3600-600, under a labelling plan and an analysis registration fixed before anyone but the annotator opened a label value (Section 6.7)"
assert ('"' + E1_NEW + '"') in PKG_TXT
E1_TAIL_OLD = ", and no new human annotation was collected"
E1_TAIL_NEW = E1_NEW[len("(iii) model-produced signals are never treated as gold or human evidence"):]
assert E1_NEW.endswith(E1_TAIL_NEW) and E1_TAIL_NEW.startswith("; one set")

E2_OLD = "| Nested reference golds and instance or verified labels | No | Image-bootstrap intervals"
E2_CELL = "Yes, for one set: a human completion of the XM3600-600 object gold (Section 6.7); no new labels elsewhere"
assert ('"' + E2_CELL + '"') in PKG_TXT
E2_NEW = E2_OLD.replace("| No |", "| " + E2_CELL + " |")

E10_OLD = "No new human annotation was collected and no human subjects were involved; all human judgments are public datasets used under their licences (Section 9.2). No ethics approval was required."
E10_PKG_NEW = "One set of new human labels was collected: answers on whether object classes are present in public XM3600 images, given by one author and, on 150 of the images, by a second annotator (Section 6.7.1); no personal data were collected. All other human judgments are public datasets used under their licences (Section 9.2)."
assert ('"' + E10_OLD + '"') in PKG_TXT and ('"' + E10_PKG_NEW + '"') in PKG_TXT
# J-13: no second-annotator line exists; the ethics sentence is dropped (P-2 default, no PI line)
E10_NEW = E10_PKG_NEW.replace(
    "given by one author and, on 150 of the images, by a second annotator (Section 6.7.1)",
    "given by one author; a second annotator, who will answer the same questions on 150 of the images, has not yet labelled (Section 6.7.1)")
assert E10_NEW != E10_PKG_NEW
# anon/declarations_anon.md: E10's quote does not occur (its second sentence differs) -> row SKIPPED
ANON = "paper/anon/declarations_anon.md"
assert git(PAPER, "show", "HEAD:" + ANON).decode().count(E10_OLD) == 0

# ---- edit table: (row id, file, OLD, NEW) ----
SEC7_LAST = git(PAPER, "show", "HEAD:paper/sec7_verbosity_sign.md").decode().rstrip("\n").split("\n")[-1]
SEC11_L15 = git(PAPER, "show", "HEAD:paper/sec11_limitations_ethics.md").decode().split("\n")[14]
assert SEC11_L15.startswith("**Construct validity: reference-only bound.**")
EDITS = [
    ("E1", "paper/sec3_measurement_setup.md", E1_OLD, E1_NEW),
    ("E2", "paper/sec2_related_work.md", E2_OLD, E2_NEW),
    ("E10", "paper/declarations.md", E10_OLD, E10_NEW),
    ("E12/E1 part", "paper/supplementary.md", E1_TAIL_OLD, E1_TAIL_NEW),
    ("E12/E1 part", "paper/supplementary_SPIC.md", E1_TAIL_OLD, E1_TAIL_NEW),
    ("6.7 (§2.12, §2.6-§2.7, §2.8 w/o Facts fixed, §2.11)", "paper/sec7_verbosity_sign.md",
     SEC7_LAST, SEC7_LAST + "\n\n" + BLOCK67),
    ("9.1 (§4 annotator, labels, statistical conclusion)", "paper/sec11_limitations_ethics.md",
     SEC11_L15, SEC11_L15 + "\n\n" + BLOCK91),
]

# ---- J-11 manifest rows keyed to BUILD.json ----
build_bytes = open(RUN + "/" + BUILD, "rb").read()
assert sha(build_bytes) == BUILD_SHA
assert sha(git(RUN, "show", "HEAD:" + BUILD)) == BUILD_SHA
c = json.loads(build_bytes)["counts"]
assert c["ctrl_absent_named"] + c["ctrl_present_named"] + c["foil_absent_unnamed"] == 443
assert c["part1_targets_mapped_unknown"] + 443 == 2233
assert c["part1_targets_mapped_unknown"] + 443 + c["part2_targets_unmapped"] + c["repeats"] == c["questions"]
assert round(100 * c["overlap_images"] / c["images_with_targets"]) == 25
ST = "keyed (DESIGN count, labelling plan v1.1 build; BUILD.json pinned OPS-1111al-xm600-label-start and in FREEZE pins; CC-357 J-11; Phase A)"
SD = "DERIVED (DESIGN count from BUILD.json counts; CC-357 J-11; Phase A)"
PFX = BUILD_SHA[:12]
MAN = [
    (f"{c['images']:,} (XM3600-600 images; sec7 §6.7.1, §6.7.5)", "counts.images", c["images"], 600, ST),
    (f"twelve (stored caption sets of Sections 6.2 and 6.3; sec7 §6.7.1)", "len(counts.systems)", len(c["systems"]), 12, ST),
    (f"{c['named_pairs']:,} (named (image, class) pairs; sec7 §6.7.1)", "counts.named_pairs", c["named_pairs"], 4910, ST),
    (f"{c['part1_targets_mapped_unknown']:,} (part-1 targets, mapped class, Open Images status unknown; sec7 §6.7.1)", "counts.part1_targets_mapped_unknown", c["part1_targets_mapped_unknown"], 1790, ST),
    (f"{c['ctrl_absent_named']} (named controls verified absent; sec7 §6.7.1)", "counts.ctrl_absent_named", c["ctrl_absent_named"], 143, ST),
    (f"{c['ctrl_present_named']} (named controls verified present; sec7 §6.7.1)", "counts.ctrl_present_named", c["ctrl_present_named"], 200, ST),
    (f"{c['foil_absent_unnamed']} (unnamed foils verified absent; sec7 §6.7.1)", "counts.foil_absent_unnamed", c["foil_absent_unnamed"], 100, ST),
    ("443 (hidden control questions; sec7 §6.7.1, sec11 §9.1)", "counts.ctrl_absent_named + counts.ctrl_present_named + counts.foil_absent_unnamed", 443, 443, SD),
    ("2,233 (part-1 questions; sec7 §6.7.1)", "counts.part1_targets_mapped_unknown + (counts.ctrl_absent_named + counts.ctrl_present_named + counts.foil_absent_unnamed)", 2233, 2233, SD),
    (f"{c['part2_targets_unmapped']:,} (part-2 targets, class without Open Images mapping; sec7 §6.7.1)", "counts.part2_targets_unmapped", c["part2_targets_unmapped"], 2100, ST),
    (f"{c['repeats']} (part-3 repeats of part-1 targets; sec7 §6.7.1, sec11 §9.1)", "counts.repeats", c["repeats"], 150, ST),
    (f"{c['questions']:,} (questions in all; sec7 §6.7.1)", "counts.questions", c["questions"], 4483, ST),
    (f"{c['screens']:,} (screens, one image per screen; sec7 §6.7.1)", "counts.screens", c["screens"], 1288, ST),
    (f"{c['practice_screens']} (practice images outside the 600, one per screen; sec7 §6.7.1)", "counts.practice_screens", c["practice_screens"], 15, ST),
    (f"{c['overlap_images']} (second-annotator overlap images; sec7 §6.7.1, sec11 §9.1, declarations Ethics)", "counts.overlap_images", c["overlap_images"], 150, ST),
    ("25% (overlap images as a share of the images with a target, 150 of 598; sec7 §6.7.1)", "100 * counts.overlap_images / counts.images_with_targets = 25.08, printed 25%", 25, 25, SD),
]
man_lines = []
for label, key, got, want, st in MAN:
    assert got == want, (key, got, want)
    man_lines.append("\t".join([label, "A", BUILD, key, PFX, st]))
MAN_ADD = "\n".join(man_lines) + "\n"

# ---- apply ----
report = {"paper_head": HEAD, "package_sha256": PKG_SHA, "files": {}, "rows": []}
by_file = {}
for rid, f, old, new in EDITS:
    by_file.setdefault(f, []).append((rid, old, new))
by_file.setdefault("paper/number_manifest.tsv", [])
by_file.setdefault(ANON, [])  # zero edits: restores the HEAD blob after an earlier partial run
for f, eds in by_file.items():
    before = git(PAPER, "show", "HEAD:" + f)
    on_disk = open(PAPER + "/" + f, "rb").read()
    txt = before.decode("utf-8")
    for rid, old, new in eds:
        n = txt.count(old)
        assert n == 1, (rid, f, n)
        txt = txt.replace(old, new, 1)
        report["rows"].append({"row": rid, "file": f, "status": "applied"})
    if f.endswith("number_manifest.tsv"):
        assert txt.endswith("\n")
        txt += MAN_ADD
        report["rows"].append({"row": "J-11 manifest (16 rows)", "file": f, "status": "applied"})
    after = txt.encode("utf-8")
    open(PAPER + "/" + f, "wb").write(after)
    report["files"][f] = {"head_blob": sha(before), "disk_before_run": sha(on_disk), "after": sha(after)}

json.dump(report, sys.stdout, indent=1)
print()
