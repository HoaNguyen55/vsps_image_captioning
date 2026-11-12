"""Build B_FECERT_PREREG_v1_1.md and B_PREF_LABELLING_PLAN_v1_1.md from v1 under CC-350.

Every replacement text that CC-350 gives is extracted from the CC file (by pinned line span), never retyped.
Each edit is an exact replacement with an asserted occurrence count. Deterministic; text only.
"""
import hashlib
import re
from pathlib import Path

HERE = Path(__file__).resolve().parent
FOLDER = HERE.parent
REPO = FOLDER.parents[2]
CC = REPO / ".session_backup/2026-10-13/decisions/CC-350.txt"
PRE_V1 = FOLDER / "B_FECERT_PREREG_v1.md"
PLAN_V1 = FOLDER / "B_PREF_LABELLING_PLAN_v1.md"
PINS = {
    CC: "f4e05e266059340636cdef47b49f7e0b4e7b9e4d4ce4d2a4f417995370eda493",
    PRE_V1: "4943b3c13cc5d619f24b604c348098de921c1f078298d4c3fd0a6a09ff721cd0",
    PLAN_V1: "22c38a7fe4e088399863c1ee7b6448df10a40c2faeda97fd83768e3786f2b063",
}
for p, want in PINS.items():
    got = hashlib.sha256(p.read_bytes()).hexdigest()
    assert got == want, f"sha mismatch {p}: {got}"

CCL = CC.read_text(encoding="utf-8").split("\n")


def span(a, b):
    """CC lines a..b (1-based, inclusive), de-wrapped; a line starting with '- ' or 'Q<n> ' opens a new line."""
    out = []
    for raw in CCL[a - 1:b]:
        s = raw.strip()
        if out and (s.startswith("- ") or re.match(r"Q\d+ ", s)):
            out.append(s)
        elif out:
            out[-1] += " " + s
        else:
            out.append(s)
    return "\n".join(out)


def quoted(a, b, i=-1):
    return re.findall(r'"([^"]*)"', span(a, b))[i]


def after(a, b, marker):
    s = span(a, b)
    assert s.count(marker) == 1, (a, b, marker)
    return s.split(marker, 1)[1]


# ---- texts extracted from CC-350 ----
W1a = quoted(198, 205, 0)
W1b_old, W1b = re.findall(r'"([^"]*)"', span(206, 208))[1:3]
W1c = after(209, 210, "RESULT.json). ").rstrip()
W1d = quoted(211, 211)
W1e_old, W1e = re.findall(r'"([^"]*)"', span(212, 212))[1:3]
W2a = quoted(215, 222, 0)
W2b_s9 = quoted(226, 226, 0)
W2b_s11 = quoted(228, 228, 1)
W2b_s12 = quoted(229, 229, 1)
W3 = quoted(237, 242, 0)
W3_s11 = quoted(243, 243, 1).replace(" ...", "")
W4b = quoted(247, 249, 1)
W4c_0a, W4c_0b = re.findall(r'"([^"]*)"', span(250, 251))
W5_s22 = quoted(253, 253)
W5_s23 = quoted(254, 254)
W5_s51 = quoted(256, 256)
W5_s61 = quoted(257, 258, 1)
W5_s66 = quoted(260, 260, 1)
W6_old, W6_s21 = re.findall(r'"([^"]*)"', span(265, 267))
W6_route = quoted(268, 270)
W6_test = quoted(271, 272)
W7_dir = re.findall(r"`([^`]*)`", span(274, 275))[1]
W7_item6 = quoted(276, 277)
W7_custody = after(278, 278, "- ")
R8d_head = after(125, 125, "(Q1, D2). ")
R8d_items = span(126, 132)
R9a = after(134, 135, "Scope. ")
R10_head = after(144, 144, "OPS-1112s. ")
R10_items = span(145, 147)
Q1 = after(173, 175, "Q1  ")
Q11_line = "Log one status line" + after(186, 188, "Log one status line")
QRULES = span(173, 192)
PLAN_Q = span(193, 193)
N3_pyvi = after(287, 287, "- ")
N3_826 = after(288, 288, "O8 and §2.4: ")
N3_gate = after(289, 290, "- ")
KAPPA_SHA = re.search(r"B_KAPPA_PREREG_v1\.md ([0-9a-f]{64})", span(23, 23)).group(1)

assert W1b_old == "is written into `RESULT.json` before any held-out score is read"
assert W1e_old == "Upper bound <= 0.05" and W1e.startswith("one-sided")
assert W2a.startswith("### 6.4") and W2a.count("\n") == 3
assert W3.startswith("- **Labels.**") and W1a.startswith("- **Sensitivity control NC")
assert W4b.startswith("11-12: ") and W7_dir == "~/vsps_labels_b/b_pref/"
assert W6_old == "image files `data/datasets/ktvic/images/<11-digit id>.jpg`"


def bullets(block, indent=""):
    return "\n".join(indent + ("" if ln.startswith("- ") else "- ") + ln for ln in block.split("\n"))


def apply(text, edits, name):
    for old, new, n in edits:
        c = text.count(old)
        assert c == n, f"{name}: expected {n}, found {c}: {old[:80]!r}"
        text = text.replace(old, new)
    return text


CC_REF = ("CC-350 (`.session_backup/2026-10-13/decisions/CC-350.txt`, sha256 "
          f"`{PINS[CC]}`), NEXT_ROUND")
BUILD_NOTE = ("Built by `build/build_v1_1.py` from v1 with exact-once replacements. Every replacement text that CC-350 "
              "gives is copied from the CC file as written (its ASCII `<=`, `x`, `F+` and `Clopper-Pearson` kept); "
              "where it goes into a table, it is placed in the table's cells. Nothing else changed.")

PRE_CHANGES = f"""
> **Changes from v1.** v1 = `B_FECERT_PREREG_v1.md`, sha256 `{PINS[PRE_V1]}`. Ruling: {CC_REF}. {BUILD_NOTE}
> - **W1** (P1 control and order): §6.1 NC bullet replaced; §6.1 "Sets" (V written to `V.json` by stage 2a, its sha256 logged before stage 2b); §6.1 "Rule" bound wording; §9 stage 2 split into 2a and 2b, and 2b refuses to start without the `V.json` LOG line; §12 new mutant and stage list; §13 row 11-14.
> - **W2** (P4 is a method check): §6.4 replaced; every row that named P4 as a prediction changed: §0 label table, §5.3 heading and last bullet, §6.5, §7, §9 stage 3, §10 K-plant, §11 P4 row, §12 self-test.
> - **W3** (P3 labels): §6.3 "Labels" bullet replaced; §6.3 heading and P3a bullet aligned with it; §11 P3 SUPPORTED row restricted to M_new, with CIDEr-D and BLEU-4 POST HOC.
> - **W4** (order; thresholds): every value v1 tagged as a proposal is fixed and untagged (§2.6 F1; §4.3 items 2, 5, 6; §6.1 z_min and N; §6.2 n_FL; §6.4's value went with W2), and the header sentence says so; §9 stage 0 split into 0a documents and 0b code; "stage-0" became "stage-0b" in §12 and §13; §13 row 11-12 replaced.
> - **W5** (character unit, CC-350 ruling 2): §2.2 `chr` row; §2.3 `chr` bullet; §2.4 (F_held = `uts`, 18 members; F = 72); §5.1 (F⁺ still 271, `chr` included); §6.1 per-unit row and expectation line; §6.6 "with `chr`" row; §10 K-unit; §11 P1 FAIL row (`uts`; four units); §16 Q3 ruling recorded. Consequential: §3.2 example, §15 row.
> - **Rulings**: §0 Authority (Q1: D4 retired, D2 as in ruling 8(d); ruling 9(a) scope); §0 "supersedes" and "imported" paragraphs (Q11 status line; full B_KAPPA sha, N5; the inline-instead option dropped); §1.1 (ruling 10 conditions); §4.2 fetch bullet (ruling 8(d)); §12 code read (rulings 11 and 12); §16 (the CC-350 rulings are recorded below the table).
> - **N2** (via plan Q3): the quotas in §8. **N3** (via Q4 and Q9): §1.2 O8; §2.4 (pyvi in B-2; the 82.6% base); §4.3 (thresholds set after the gate.json values were seen).
> - **Version**: title v1.1; companion file names point to `B_PREF_LABELLING_PLAN_v1_1.md`.
> - Not applied (non-blocking): N1, N4, N6, N8.
"""

PLAN_CHANGES = f"""
> **Changes from v1.** v1 = `B_PREF_LABELLING_PLAN_v1.md`, sha256 `{PINS[PLAN_V1]}`. Ruling: {CC_REF}. {BUILD_NOTE}
> - **W6** (13 of the 558 test images are `.png` or `.jpeg`): §2.1 image path; §9 pair_server item 2 (route regex, served only if listed, content type); §9 build_pairs `--selftest` addition.
> - **W7** (collision with the live Paper A labelling): the §6 label folder became `~/vsps_labels_b/b_pref/` in both places, not under `~/vsps_labels/`; the custody rules of §6 apply there; §9 pair_server item 6 (port 8791; port 8790 refused).
> - **W4** (thresholds fixed): the proposal tags are removed with the values kept (§2.2 ε = 10.0; §5.4 κ ≥ 0.40), both ruled yes (plan Q3, Q4).
> - **Rulings**: "Rule status" (ruling 9(a): the screens are inside PI-1111n/o); §2.1 (Q2: no); §3.1 (Q1: yes); §11 (the CC-350 rulings are recorded below the table).
> - **N2** (via plan Q3): quotas P 100, U 160, C 40 in §2.4 step 3, §5.2 H-P and §5.3; §7 unchanged (the U gate stays 100).
> - **Version**: title v1.1; companion file name points to `B_FECERT_PREREG_v1_1.md`.
> - Not applied (non-blocking): N6, N8.
"""

# ---------------- prereg ----------------
PRE_EDITS = [
    # version + changes block
    ("(Paper B, LRE). DRAFT v1, not approved\n",
     "(Paper B, LRE). DRAFT v1.1, not approved\n" + PRE_CHANGES, 1),
    ("Thresholds marked [proposal] are for the judge.",
     "The thresholds that v1 tagged as proposals are fixed in v1.1 and carry no tag (CC-350 W4).", 1),
    ("Companion file: `B_PREF_LABELLING_PLAN_v1.md`", "Companion file: `B_PREF_LABELLING_PLAN_v1_1.md`", 1),
    # W2 label table
    ("| P1 to P4 (§6) and the human hypotheses of the labelling plan |",
     "| P1 to P3 (§6) and the human hypotheses of the labelling plan; P4 (§6.4) is a method check, not a prediction (CC-350 W2) |", 1),
    # rulings: Q1, 9(a)
    ("The coordinator confirms which of REDESIGN_B's decisions D1 to D6 the line covers (§16 Q1).",
     f'CC-350 Q1: "{Q1}" Ruling 8(d) is carried into §4.2.', 1),
    ("Read to 300 characters.\n",
     f'Read to 300 characters. CC-350 ruling 9(a): "{R9a}"\n', 1),
    # Q11, N5
    ("(sha256 `b56d8ccded3c10b2…`, unjudged, uncommitted)",
     f"(sha256 `{KAPPA_SHA}`, unjudged, uncommitted; CC-350 N5)", 1),
    ("Its rank-swap test (§4 to §8 there) is not run (REDESIGN_B D4).",
     "Its rank-swap test (§4 to §8 there) is retired and not run (REDESIGN_B D4; decided by CC-350 Q1).", 1),
    ("§16 Q11 asks the judge to record that.",
     f"CC-350 Q11 records it: {Q11_line}", 1),
    ('(so that file must be committed with this one as a pinned reference, status "superseded; swap test retired, not run"; §16 Q11)',
     "(that file is committed unchanged with this one as a pinned reference; CC-350 Q11)", 1),
    (" If the judge prefers, these are inlined into a v1.1 of this file instead.", "", 1),
    # ruling 10
    ("Reported to the coordinator for the access record.\n",
     f"Reported to the coordinator for the access record. CC-350 ruling 10: {R10_head}\n{bullets(R10_items, '  ')}\n", 1),
    # N3 O8
    ("POST HOC; underthesea has been run on references (not on system outputs) |",
     f"POST HOC; underthesea has been run on references (not on system outputs); CC-350 N3: {N3_826} |", 1),
    # W5 §2.2, §2.3
    ("Admissibility is §16 Q3 |", W5_s22 + " |", 1),
    ("- `chr`: admissible under (a) only if ViTextCaps' \"character\" level counts as a scorer in use. "
     "REDESIGN_B §1(b) reports that two models swap order on CIDEr at character level there. §16 Q3.",
     f"- `chr`: {W5_s23}.", 1),
    # W5 §2.4 + N3
    ("so it cannot be held out |", f"so it cannot be held out. CC-350 N3: {N3_pyvi} |", 1),
    ("| F_held (held-out) | `uts`, `chr` | 36 | neither has ever been run on a system output by this project. "
     "`uts` was run on KTVIC references in `identify_segmenter.py` (82.6% agreement, O8); disclosed. `chr` has never been run |",
     "| F_held (held-out) | `uts` | 18 | never run on a system output by this project. "
     f"`uts` was run on KTVIC references in `identify_segmenter.py` (82.6% agreement, O8; CC-350 N3: {N3_826.rstrip('.')}); disclosed. "
     "`chr` is not in F (CC-350 ruling 2) |", 1),
    ("| F = F_dev ∪ F_held | | 90 | 72 if the judge rules `chr` inadmissible; then F_held = `uts` only (18 members) |",
     "| F = F_dev ∪ F_held | | 72 | `chr` is not admissible (CC-350 ruling 2); F_held = `uts` (18 members) |", 1),
    # W4 F1
    (" or more than 0.5% failed strings [proposal] drops", " or more than 0.5% failed strings drops", 1),
    # W5 consequential §3.2
    ('(for example "breaks under every `chr` member and under ck with pk")',
     '(for example "breaks under every `uts` member and under ck with pk")', 1),
    # ruling 8(d)
    ("- The fetch of G2, G4 and the reference files of G1, G3, G4 needs D2 of REDESIGN_B (§16 Q1). "
     "Fetching follows the B-2 pattern: a generic client, a pinned commit, sha256 and git blob id logged, no content printed.\n",
     "- The fetch of G2, G4 and the reference files of G1, G3, G4 needs D2 of REDESIGN_B. "
     "Fetching follows the B-2 pattern: a generic client, a pinned commit, sha256 and git blob id logged, no content printed. "
     f"CC-350 ruling 8(d): {R8d_head}\n{bullets(R8d_items, '  ')}\n", 1),
    # W4 gate + N3
    ("(those rows are dropped) [proposal];", "(those rows are dropped);", 1),
    ("own references [proposal];", "own references;", 1),
    ("or another language) [proposal].", "or another language).", 1),
    ("The coordinator logs its sha256 before any FL score exists.",
     f"The coordinator logs its sha256 before any FL score exists. CC-350 N3: {N3_gate}", 1),
    # W5 §5.1
    ("- F⁺ = every member f of F (§2.3, all units including `chr` whatever Q3 rules, since identification needs no admissibility) applied three ways:",
     "- F⁺ = every member f of F (§2.4) and the 18 `chr` members, 90 members in all (`chr` is not in F, CC-350 ruling 2, "
     "but identification needs no admissibility), applied three ways:", 1),
    ("|F⁺| = 90 × 3 + 1 = 271.", W5_s51 + ".", 1),
    # W2 §5.3
    ("### 5.3 Planted check (method validation; label `REGISTERED PREDICTION`)",
     "### 5.3 Planted check (method validation; METHOD CHECK, not a registered prediction)", 1),
    ("- **P4 (§6.4)** is the rule on this check.",
     "- **P4 (§6.4)** is the method check on these cases: a wrong recovery is a FAULT, not a FAIL (CC-350 W2).", 1),
    # W1 + W4 §6.1
    ("z_min ≤ 4 [proposal] (near-margin)", "z_min ≤ 4 (near-margin)", 1),
    (W1b_old, W1b, 1),
    ("N < 59 [proposal; 59 is the smallest N for which zero breaks give a one-sided 95% Clopper–Pearson upper bound below 0.05]: "
     "NOT_EVALUABLE. Upper bound ≤ 0.05: **PASS**",
     "N < 59 (59 is the smallest N for which zero breaks give a one-sided 95% Clopper–Pearson upper bound below 0.05): "
     f"NOT_EVALUABLE. If the {W1e}: **PASS**", 1),
    ("r per held-out unit (`uts`, `chr`)", W5_s61, 1),
    ("- **Sensitivity control NC (computed and pinned before any held-out member runs).** On D only: certify with the 18 `syl` members; "
     "count breaks under the `rdr` and `pyvi` members. r_NC = that break share. If r_NC ≤ 0.05, P1 is labelled **LOW-SENSITIVITY** "
     "whatever its outcome: \"a one-unit family was broken by the other development units in at most 5% of its certificates, "
     "so the held-out check had little room to fail\". This answers the scorers' \"held-out outcome foreseeable\" by measuring, "
     "before the look, whether the check has teeth.",
     W1a, 1),
    (" With `chr`: unknown; the ViTextCaps swap suggests it can break near-margin certificates.", "", 1),
    ("n_FL < 10 [proposal]:", "n_FL < 10:", 1),
    # W3
    ("### 6.3 P3, FE-ID on the KTVIC baselines (`REGISTERED PREDICTION, DEVELOPMENT DATA`)",
     "### 6.3 P3, FE-ID on the KTVIC baselines (`REGISTERED PREDICTION, DEVELOPMENT DATA` on M_new only; the rest `POST HOC`)", 1),
    ("so it is a weak prediction for CIDEr-D and BLEU-4 and a real one for the other printed metrics.",
     "so it is POST HOC-informed for CIDEr-D and BLEU-4 and a registered prediction only for the other printed metrics (\"Labels\", below).", 1),
    ("- **Labels.** P3a and P3b both hold: SUPPORTED. Either fails: NOT SUPPORTED, with the failing metric and the distance. "
     "The identification label (IDENTIFIED, AMBIGUOUS, OUTSIDE) and the margin are reported for each baseline.",
     W3, 1),
    # W2 §6.4
    ("### 6.4 P4, FE-ID planted check (`REGISTERED PREDICTION`)\n\n"
     "- Fewer than 12 of the 24 planted cases IDENTIFIED [proposal]: **NOT_EVALUABLE** (the method rarely identifies anything at "
     "one-decimal precision, so zero wrong recoveries would be empty); P3's identification label is then NOT_EVALUABLE too, and "
     "FE-ID is reported as a reproduction table.\n"
     "- Otherwise: 0 wrong recoveries: PASS. One or more: FAIL; FE-ID is then reported as descriptive only and P3 loses its "
     "identification label (the reproduction facts stay).\n"
     "- Reported: the IDENTIFIED, AMBIGUOUS and OUTSIDE counts among the 24.\n",
     W2a + "\n", 1),
    # §6.5
    ("(registered in `B_PREF_LABELLING_PLAN_v1.md` §5)", "(registered in `B_PREF_LABELLING_PLAN_v1_1.md` §5)", 1),
    ("a certificate or a P1 to P4 label.", "a certificate, a P1 to P3 label or the P4 method check.", 1),
    # W5 §6.6
    ("without ck, without `chr`, and without pk", f"without ck, {W5_s66}, and without pk", 1),
    # W2 §7
    ("- **P1 to P4**: four separate threshold rules on four different questions, each reported with its own label.",
     "- **P1 to P3**: three separate threshold rules on three different questions, each reported with its own label; "
     "P4 is a method check (§6.4).", 1),
    # §8 + N2
    ("Registered in full in `B_PREF_LABELLING_PLAN_v1.md`: about 300 pairs (180 unit-flip, 80 punctuation-flip, 40 non-flip controls)",
     "Registered in full in `B_PREF_LABELLING_PLAN_v1_1.md`: about 300 pairs (160 unit-flip, 100 punctuation-flip, "
     "40 non-flip controls; CC-350 N2)", 1),
    # W4c stage 0
    ("| 0 commit | — | the gatekeeper commit of this file, the labelling plan and the code (after the code read) | commit id in LOG | — |",
     f"| {W4c_0a} | — | the gatekeeper commit of this file v1.1, the labelling plan v1.1 and B_KAPPA v1 unchanged (CC-350 Q11) | commit id in LOG | — |\n"
     f"| {W4c_0b} | — | the gatekeeper commit of the code | commit id in LOG | — |", 1),
    # W1c stage 2
    ("| 2 first look | D ∪ FL files under F; FL files under F_dev and F_held | all certificates; P1, P2; secondary rows | `RESULT.json` | after the pin only |",
     "| 2a first look, development family | FL files under F_dev; `DEV.json` | certificates of FL over F_dev; with D: Cert_dev, z_min, V (§6.1) | "
     "`V.json` (with the ids of V); the coordinator logs its sha256 | after the pin only |\n"
     "| 2b first look, held-out members | D and FL files under F_held | held-out members on D and FL; all certificates over F; P1, P2; secondary rows | "
     "`RESULT.json` | after the `V.json` LOG line only |", 1),
    ("| plant, identify, compare; P3, P4; §5.5 |", f"| plant, identify, compare; {W2b_s9}; §5.5 |", 1),
    ("Stage 2 checks that no `RESULT*.json` exists and that the pin line precedes its start line.",
     f"Stage 2a checks that no `RESULT*.json` exists and that the pin line precedes its start line. {W1c}", 1),
    # §10
    ("| F1 fails for `pyvi`, `uts` or `chr` |", "| F1 fails for `pyvi` or `uts` |", 1),
    ("| P4 and P3's identification label NOT_EVALUABLE |",
     "| P3's identification label NOT_EVALUABLE; FE-ID reported as a reproduction table (P4 method check, §6.4) |", 1),
    # §11
    ("The paper recommends certifying over all five units and names the breaking unit.",
     "The paper recommends certifying over all four units of F and names the breaking unit (`uts`).", 1),
    ("| P3 SUPPORTED | \"The printed scores of the two KTVIC baselines are reproduced by pipeline r\\* (every printed metric within half a unit); "
     "under matched scoring (f0) the values are Y\" |",
     f"| P3 SUPPORTED | Reported {W3_s11}: \"The printed scores of the two KTVIC baselines are reproduced by pipeline r\\* "
     "(every metric of M_new within half a unit); under matched scoring (f0) the values are Y\". CIDEr-D and BLEU-4 stay POST HOC |", 1),
    ("| P4 FAIL | FE-ID reported as a reproduction table without identification labels |",
     f"| {W2b_s11} | a wrong recovery stops stage 3 (§6.4); with fewer than 12 IDENTIFIED, FE-ID is reported as a "
     "reproduction table without identification labels |", 1),
    # §12
    ("| stages F, C, G, 1, pin, 2, 3, H; certificate, NC, P1 to P4, FE-ID, planted check |",
     "| stages F, C, G, 1, pin, 2a, 2b, 3, H; certificate, NC, P1 to P3, the P4 method check, FE-ID, planted check |", 1),
    ("a planted identification; mutants:", f"a planted identification, {W2b_s12}; mutants:", 1),
    ("reproduction tolerance of a full unit |", f"reproduction tolerance of a full unit, {W1d} |", 1),
    ("before the stage-0 commit.",
     "before the stage-0b commit. CC-350 ruling 11: the code read is ruled at the IRREVERSIBLE tier (bar 85), and its request "
     "says so. CC-350 ruling 12: it names the host for the self-tests, mutants and stages F to 3 under CC-346 R5, "
     "CC-349 3(c) and PI-1112b.", 1),
    # §13
    ("| 11-12 | judge read of this file and the labelling plan; PI names the second rater and answers §17; fetch of the D2 files "
     "(separate agent, sha only); schema print; `PRINTED.json` by a separate agent | no judgement, no score |",
     f"| 11-12 | {W4b[len('11-12: '):]} | no judgement, no score |", 1),
    ("code read; stage-0 commit;", "code read; stage-0b commit;", 1),
    ("| 11-14 | stages 2 and 3 |", "| 11-14 | stages 2a, 2b and 3 |", 1),
    # §15
    ("pyvi moved to development; `uts` and `chr` never run on outputs;",
     "pyvi moved to development; `uts` never run on outputs (`chr` not admissible, CC-350 ruling 2);", 1),
    # §16
    ("| No: F_held = `uts` only, and P1 will likely carry LOW-SENSITIVITY |",
     "| No: F_held = `uts` only, and P1 will likely carry LOW-SENSITIVITY. **Ruled: not admissible (CC-350 ruling 2); "
     "F = 72, F_held = `uts`** |", 1),
    ("| Q14 | Stage order: dev and NC pinned before any held-out member or FL file is scored | Yes | as written |\n",
     "| Q14 | Stage order: dev and NC pinned before any held-out member or FL file is scored | Yes | as written |\n\n"
     "**CC-350 rulings on these questions** (copied from CC-350; the rows above are v1's questions as asked):\n\n"
     f"{bullets(QRULES)}\n", 1),
]

# ---------------- plan ----------------
PLAN_EDITS = [
    ("labelling plan v1 (2026-11-12). DRAFT, not approved\n",
     "labelling plan v1.1 (2026-11-12). DRAFT, not approved\n" + PLAN_CHANGES, 1),
    ("with `B_FECERT_PREREG_v1.md` (this folder)", "with `B_FECERT_PREREG_v1_1.md` (this folder)", 1),
    ("No other human data (FAIR 2026 ratings: PD-21b) is used.",
     f'No other human data (FAIR 2026 ratings: PD-21b) is used. CC-350 ruling 9(a): "{R9a}"', 1),
    (W6_old, W6_s21, 1),
    ("§11 Q2 asks whether the baselines may be added.", "§11 Q2 asked whether the baselines may be added; CC-350 ruled no.", 1),
    ("Margin ε = 10.0 [proposal]:", "Margin ε = 10.0:", 1),
    ("**P**: draw min(80, |E_P|) images", "**P**: draw min(100, |E_P|) images", 1),
    ("draw min(180, |E_U|) from E_U.", "draw min(160, |E_U|) from E_U.", 1),
    ("One image gives one pair; images are disjoint across strata.",
     "One image gives one pair; images are disjoint across strata. Quotas P 100, U 160, C 40 (CC-350 N2).", 1),
    ("§11 Q1 asks the judge to confirm this choice.", "CC-350 confirmed this choice (ruling 9(c); §11 Q1).", 1),
    ("reachable with the quota of 80)", "reachable with the quota of 100)", 1),
    ("If about 55% of pairs are decisive (unverified), U gives about 99 decisive pairs and P about 44: "
     "H-U can detect a share near 0.65, H-P one near 0.70.",
     "If about 55% of pairs are decisive (unverified), U gives about 88 decisive pairs and P about 55 (quotas of CC-350 N2): "
     "H-P can detect a share near 0.70 (47 needed); at 88, H-U detects a share of about 0.65 only at two-sided 0.05, "
     "not at 0.025 (103).", 1),
    ("κ ≥ 0.40 [proposal]:", "κ ≥ 0.40:", 1),
    ("`~/vsps_labels/b_pref/`", f"`{W7_dir}`", 2),
    ("on the laptop's Linux home filesystem (never under /mnt):",
     "on the laptop's Linux home filesystem (never under /mnt, not under `~/vsps_labels/`; CC-350 W7):", 1),
    ("whichever is first, a LOG line closes the labelling with the final hashes. Only then are the 444 copies pushed to the host "
     "(sha256 checked) for stage H, which writes `HUMAN.json` (counts and statistics only, no caption text).\n",
     "whichever is first, a LOG line closes the labelling with the final hashes. Only then are the 444 copies pushed to the host "
     "(sha256 checked) for stage H, which writes `HUMAN.json` (counts and statistics only, no caption text).\n"
     f"- {W7_custody}\n", 1),
    ("2. The image route regex `([0-9a-f]{16})\\.jpg` becomes `([0-9]{11})\\.jpg` (KTVIC file names are 11-digit ids; seen in the directory listing).",
     f"2. {W6_route}", 1),
    ("`key.json` and `BUILD.json` stay unserved.\n",
     f"`key.json` and `BUILD.json` stay unserved.\n6. {W7_item6}\n", 1),
    ("no file name, stratum or score in any served file, display normalisation on toy strings.",
     f"no file name, stratum or score in any served file, display normalisation on toy strings; {W6_test}.", 1),
    ("| Q6 | Analysis registered here rather than in a later file | Yes; PI-1111o asks for the analysis to be fixed before any judgement | as written |\n",
     "| Q6 | Analysis registered here rather than in a later file | Yes; PI-1111o asks for the analysis to be fixed before any judgement | as written |\n\n"
     f"**CC-350 rulings on these questions** (copied from CC-350): {PLAN_Q}\n", 1),
]

for src, edits, dst in ((PRE_V1, PRE_EDITS, "B_FECERT_PREREG_v1_1.md"),
                        (PLAN_V1, PLAN_EDITS, "B_PREF_LABELLING_PLAN_v1_1.md")):
    out = apply(src.read_text(encoding="utf-8"), edits, src.name)
    (FOLDER / dst).write_text(out, encoding="utf-8", newline="\n")
    print(dst, hashlib.sha256(out.encode("utf-8")).hexdigest())
