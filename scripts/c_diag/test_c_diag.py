#!/usr/bin/env python3
"""C-DIAG CPU selftest (prereg C_DIAG_PREREG_DRAFT_v1_2.md §10.2 item 5; CC-299r3). Synthetic fixtures only (made-up
ids and sentences; the instruments vi_oiv7_map.json and the OIV7 class-name CSV are real), no weights, every socket
raises, the real pinned RDRSegmenter on made-up sentences (PINS-A precedent). Runs every Stage-0 subcommand, the host
arm logic, the gate, CIDEr-VI, the S4 score and §4.5 end to end under the real allow hook. Never opens a sealed path,
a test annotation file or any C-DIAG data input.

    PY=~/.venvs/c_pvr_cider/bin/python      (numpy 2.5.4 + pycocoevalcap for the kit; JDK 21 + VnCoreNLP as c_pvr)
    $PY -X utf8 -I -B scripts/c_diag/test_c_diag.py          all checks (laptop)
    $PY -X utf8 -I -B scripts/c_diag/test_c_diag.py host     the host-safe subset (no java, no kit; run by c_diag_job.sh)
"""
from __future__ import annotations

import argparse
import json
import os
import socket
import sys
import tempfile
import time
from pathlib import Path

import numpy as np

HERE = Path(os.path.abspath(__file__)).parent  # unresolved: the mutant suite runs scratch copies
sys.path.insert(0, str(HERE))
import c_diag as D  # noqa: E402
import c_diag_gpu as H  # noqa: E402

N = [0]


def ok(cond, msg: str) -> None:
    assert cond, msg
    N[0] += 1


def must(frag: str, fn, *a, **k) -> None:
    try:
        fn(*a, **k)
    except SystemExit as e:
        ok(frag in str(e), f"expected a refusal with {frag!r}, got {e}")
        return
    raise AssertionError(f"expected a refusal with {frag!r}, got none")


def fresh_guard() -> D.Guard:
    D.GUARD.on = False
    D.GUARD = D.Guard()
    return D.GUARD


def off() -> None:
    D.GUARD.on = False


def no_net() -> None:
    def refuse(*_a, **_k):
        raise OSError("selftest: network disabled")
    socket.socket = socket.create_connection = refuse  # type: ignore[assignment,misc]


# ---------------------------------------------------------------------------------------------- registered constants
def st_constants() -> None:
    ok(D.LABEL == "EXPLORATORY (C-DIAG): spent sets re-used in a dev role, in-sample, no confirmatory claim", "label")
    ok((D.FLOOR, D.VI_GUARD, D.CELL, D.CELL_MIN, D.N_LABEL_IDS) == (0.10, 0.95, 150, 100, 3000), "§1.3 / §4.1 values")
    ok(D.RUNGS == (("a", 4, 3), ("b", 8, 3), ("c", 8, 5)) and D.GATE_SALT == "c_diag_gate", "§4.1 ladder")
    ok({k: v[1] for k, v in D.SETS.items()} == {"xm_dev500": 500, "xm_test2500": 2500, "ov_dev_b": 925}, "§2.2 sizes")
    ok((D.CAP_MAIN_H, D.CAP_GATE_H, D.M_D, D.SETUP_VND, D.W_LINE) == (20.0, 3.0, 210_000, 30, 50_000), "§8.3")
    ok(D.CUT_ORDER == (("internvl3_8b", "ov_dev_b"), ("qwen25vl_7b", "ov_dev_b"), ("internvl3_8b", "xm_test2500")),
       "§8.3 cut order")
    ok(D.ORDER[0] == ("qwen25vl_7b", "xm_test2500") and D.ARMS["xm_test2500"] == ("rand", "ret", "filt", "ctl")
       and D.ARMS["ov_dev_b"] == ("rand", "ret", "filt"), "§5.1-5.2")
    ok({b: (c["k"], c["order"], c["tpl"]) for b, c in D.BACKBONES.items()} ==
       {"qwen25vl_7b": (8, "first", "T1"), "internvl3_8b": (4, "last", "T2")}, "§3.1 frozen configs")
    import c_diag_score as SC
    ok((SC.B_REPS, SC.SEED_GATE, SC.SEED_BOOT, SC.SEED_PERM, SC.SESOI_P, SC.DELTA_C, SC.DELTA_R) ==
       (10_000, 20261109, 20261108, 20261110, 2.0, 2.0, 2.0), "§4.2 / §6.1-6.2 values")
    ok(SC.V == {"k_pt": 0.40, "k_lo": 0.20, "no_p": 0.40, "no_a": 0.40, "sup_p": 0.50, "unc": 0.20, "blind": 0.20},
       "§4.3 V1-V5 thresholds")
    import c_diag_t1table as T1
    ok((T1.SEED, T1.B_REPS, T1.T5_PREFIX, T1.TMAN[:8]) == (20261111, 10_000, "f81323d1", "4849a08f"), "§4.5 values")
    ok(len(T1.T) + 2 == 9, "§4.5: nine inputs (T1-T4, T7-T9 here; T5 by T4's line, T6 by --labels-sha)")
    ok(D.CP.CAP == 32 == D.CAP and D.CP.MAX_NEW["verify"] == 8 and D.CP.SEEDS["A7"] == 20262007, "c_pvr CAP, 8 tokens, A7 seed")


# ---------------------------------------------------------------------------------------------- §2.3 guard
STRAY = (".session_backup/2026-10-18/ladder_check/ktvic/test_data.json",  # CC-299 J3 W4: recorded prefixes; the
         ".session_backup/machines/n2/ktvic/test_data.json")              # refusal is by basename, so any depth


def st_backstop() -> None:
    for k in D.B:
        ok(D.deny(D.path(k)) is None, f"Appendix B path {k} passes the backstop")
    for rel in D.CODE:
        ok(D.deny(D.ROOT / rel) is None, "code pins pass the backstop")
    for s in STRAY:
        ok(D.deny(D.ROOT / s) == "test_data.json", "stray ktvic/test_data.json refused")
    ok(D.deny(os.path.join(os.path.expanduser("~"), ".vsps_sealed", "c_pvr", "x.json")) == ".vsps_sealed", "R2-W7")
    for name, pat in (("uit-openviic-annotation-test.json", "uit-openviic-annotation-test.json"),
                      ("t2pool_a_kept_ids.txt", "t2pool_*"), ("nocaps_test_image_info.json", "nocaps_test*"),
                      ("image_info_test2014.json", "image_info_test*"), ("instances_val2014.json", "instances_*.json"),
                      ("captions_train2014.json", "captions_*.json")):
        ok(D.deny(f"/x/{name}") == pat, f"backstop {pat}")
    ok(D.deny("/x/ex_xm_test2500.json") is None and D.deny("/x/ct_a_xm_test2500-ret.preds.json") is None,
       "name-exact: a broad *test* pattern is not used")
    ok("oiv7" in D.SUBCMD["label-subset"] and all("oiv7" not in v for k, v in D.SUBCMD.items() if k != "label-subset"),
       "NB-2: row 8 only in label-subset")


def st_hook(tmp: Path) -> None:
    g = fresh_guard()
    a, b, wdir = tmp / "a.json", tmp / "b.json", tmp / "w"
    wdir.mkdir()
    a.write_text("{}", encoding="utf-8")
    b.write_text("[]", encoding="utf-8")
    g.add(a, D.sha(b"{}"))
    g.outs.append(str(wdir))
    g.install()
    ok(json.loads(a.read_text("utf-8")) == {}, "an allow-listed file with its sha opens")
    (wdir / "o.json").write_text("1", encoding="utf-8")
    must("not on the allow-list", (wdir / "o.json").read_text, "utf-8")  # CC-307 N1: out dirs are write-only
    must("not on the allow-list", b.read_text)
    must("write to an allow-listed input", a.write_text, "x")
    sealed = tmp / "h" / ".vsps_sealed" / "c_pvr"
    must("deny backstop (.vsps_sealed)", lambda: open(sealed / "x.json", encoding="utf-8"))
    must("listing refused", os.listdir, sealed)
    must("deny backstop (test_data.json)", lambda: open(tmp / "ktvic" / "test_data.json", encoding="utf-8"))
    g.files[os.path.abspath(a)] = "0" * 64
    g.cache.clear()
    must("sha256 differs", a.read_text)
    must("refused open", g.done)
    off()
    g = fresh_guard()
    link = tmp / "ln.json"
    link.symlink_to(a)
    g.add(a, D.sha(b"{}"))
    g.install()
    ok(json.loads(link.read_text("utf-8")) == {}, "a symlink to an allow-listed file resolves to it")
    off()
    must("lies under the repo", D.allow, "lists", {}, [D.ROOT / "x"])
    off()
    must("matches the deny backstop (.vsps_sealed)", D.allow, "lists", {}, [tmp / "h" / ".vsps_sealed" / "w"])
    off()
    fresh_guard()


# ---------------------------------------------------------------------------------------------- §4.1 units
def st_bare() -> None:
    chair, _lex = D.CP.rescap_mods(D.ROOT)
    okset = D.bare_set()
    u = "một_con chó"
    toks = [(0, 7, "một con"), (8, 11, "chó")]  # an RDR token joined by '_' (N8): split into syllables
    sy = D.syllables(u.replace("_", " "), toks)
    ok(sy == [(0, 3), (4, 7), (8, 11)], "N8 syllables of a joined token")
    p = {"start": 0, "end": 11, "mentions": [[8, 11]]}
    ok(D.is_bare("một con chó", sy, p, okset, chair.norm_tone), "một + classifier + mention = bare")
    u2 = "hai con chó"
    ok(not D.is_bare(u2, D.syllables(u2, [(0, 7, "hai con"), (8, 11, "chó")]), p, okset, chair.norm_tone),
       "a numeral makes a unit non-bare")
    u3 = "con chó đen"
    p3 = {"start": 0, "end": 11, "mentions": [[4, 7]]}
    ok(not D.is_bare(u3, D.syllables(u3, [(0, 3, "con"), (4, 7, "chó"), (8, 11, "đen")]), p3, okset, chair.norm_tone),
       "a colour makes a unit non-bare")


def mk_units(n_p: int, n_a: int, ranks=(1,), per_q: int = 1) -> list[dict]:
    out = []
    for s0, n in (("present", n_p), ("absent", n_a)):
        for i in range(n):
            q, r = f"q{i // per_q}", ranks[i % len(ranks)]
            out.append({"qid": q, "rank": r, "prop_index": i, "class": "chó", "status": s0, "text": "x",
                        "file": f"{q}.jpg", "image_sha256": "0" * 64, "order": D.sha(f"{q}|{r}|{i}|chó|{s0}".encode())})
    return sorted(out, key=lambda u: u["order"])


def st_ladder() -> None:
    lad = D.ladder(mk_units(200, 200))
    ok(lad["rung"] == "a" and len(lad["units"]) == 300, "rung (a) when both cells reach 150")
    lad = D.ladder(mk_units(200, 200, ranks=(5,)))
    ok(lad["rung"] == "b" and lad["supply"]["a"] == {"present": 0, "absent": 0}, "ranks 5-8 need rung (b)")
    lad = D.ladder(mk_units(500, 500, ranks=(1,), per_q=5))
    ok(lad["rung"] == "a" and len(lad["units"]) == 300, "per-query cap 3 at rung (a) still fills")
    lad = D.ladder(mk_units(120, 200, ranks=(6,)))
    ok(lad["rung"] == "c" and sum(u["status"] == "present" for u in lad["units"]) == 120, "100-149 at (c): all")
    lad = D.ladder(mk_units(99, 200))
    ok("fault" in lad and not lad["units"], "fewer than 100 in a cell after rung (c) = FAULT (W2)")
    u = mk_units(3, 3)
    ok([x["order"] for x in D.ladder(u * 60)["units"]] == sorted(x["order"] for x in D.ladder(u * 60)["units"]),
       "units in sha order")
    hu = D.host_units(lad["units"] or D.ladder(mk_units(200, 200))["units"])
    ok(all(set(x) == {"u", "qid", "file", "image_sha256", "rank", "prop_index", "text"} for x in hu),
       "the host unit file holds no status or class (§2.4)")


# ---------------------------------------------------------------------------------------------- §1.3, §14.7, §8
def st_plan_money() -> None:
    blocks = {("qwen25vl_7b", "xm_test2500"): D.stage_hours("qwen25vl_7b", "xm_test2500", 24_420, 2500),
              ("qwen25vl_7b", "ov_dev_b"): D.stage_hours("qwen25vl_7b", "ov_dev_b", 9_035, 925),
              ("internvl3_8b", "xm_test2500"): D.stage_hours("internvl3_8b", "xm_test2500", 12_210, 2500),
              ("internvl3_8b", "ov_dev_b"): D.stage_hours("internvl3_8b", "ov_dev_b", 4_518, 925)}
    pl = D.plan(blocks, 300, D.hour_cap(10_092, False))
    ok(pl["cuts"] == ["internvl3_8b|ov_dev_b"] and abs(pl["billed_h"] - 18.50) < 0.02, "§8.2: cut 1 -> 18.5 h")
    ok(abs(D.plan(blocks, 300, 99)["billed_h"] - 21.09) < 0.02, "§8.2: 21.1 h billed with no cut")
    pl = D.plan(blocks, 300, 5.0)
    ok("qwen25vl_7b|xm_test2500" in pl["kept"] and len(pl["cuts"]) == 3 and not pl["fits"], "Qwen XM never cut")
    pl = D.plan({k: v for k, v in blocks.items() if k[0] == "internvl3_8b"}, 300, 5.0)
    ok(pl["kept"] == ["internvl3_8b|xm_test2500"], "Qwen dropped: InternVL3 XM is never cut")
    ok(D.hour_cap(10_092, True) == 3.0 and abs(D.hour_cap(20_000, False) - (210_000 - 30) / 20_000) < 1e-9,
       "§8.3 hour cap: 3.0 h gate-only; money binds at a high rate")
    must("not plausible", D.hour_cap, 50, False)
    ns = argparse.Namespace(bal=1_079_499, r_d=10_092, sigma_live=0, h_b_t1=0, h_b_t1p=0, r_b=10_092,
                            b_resume_used=False, b_ended=False, gate_only=False)
    s = D.solvency(ns)
    ok(s["rhs"] == 764_630 and s["margin"] == 314_869 and s["PASS_parallel"], "§8.3 worked value 314,869")
    s = D.solvency(argparse.Namespace(**{**vars(ns), "gate_only": True}))
    ok(s["rhs"] == 584_936 and s["margin"] == 494_563, "§8.3 gate-only worked value 494,563")
    s = D.solvency(argparse.Namespace(**{**vars(ns), "b_resume_used": True, "h_b_t1": 30, "h_b_t1p": 5}))
    ok(s["O_B"] == 0 and s["W_B"] == 5 * 10_092 and s["h_B"] == 35, "NB-C4: h_B = HB-T1 + HB-T1'; O_B = 0")
    s = D.solvency(argparse.Namespace(**{**vars(ns), "b_ended": True, "bal": 290_275}))
    ok(s["W_B"] == 0 and s["O_B"] == 0 and not s["PASS_parallel"], "B ended: W_B = O_B = 0; FAIL below the line")
    ok(D.vi_share(["Con chó đen", "a dog", ""]) == 1 / 3, "VI-script share: empty = non-Vietnamese")


# ---------------------------------------------------------------------------------------------- host logic (§3.2, §5.1)
def dcx(text: str, props: list[tuple]) -> dict:
    """A hand-built decomposition: props = (kind, class or None, start, end)."""
    return {"text": text, "sents": [[0, len(text)]], "nouns": [[s, e] for k, c, s, e in props if k == "obj"],
            "props": [{"kind": k, "classes": [c] if c else [], "mentions": [[s, e]] if k == "obj" else [],
                       "start": s, "end": e, "text": text[s:e]} for k, c, s, e in props]}


def st_host() -> None:
    d1 = dcx("con chó và con mèo", [("obj", "chó", 0, 7), ("obj", "mèo", 11, 18)])
    d2 = dcx("chiếc thuyền ghi Hà Nội", [("obj", "thuyền", 0, 12), ("text", None, 17, 23)])
    asked = []

    def ask(t):
        asked.append(t)
        return {"con chó": "No", "con mèo": "maybe", "chiếc thuyền": "yes"}.get(t, "??")
    labels, st = H.verify_image([d1, d2], ask)
    ok(labels == [["REJECTED", "UNCERTAIN"], ["SUPPORTED", "TEXT"]] and asked == ["con chó", "con mèo", "chiếc thuyền"],
       "§3.2: obj only, rank order, text never asked")
    ok(st["calls"] == 3 and st["no"] == 1 and st["maybe"] == 1, "verify counts")
    big = dcx(" ".join(["con chó"] * 40), [("obj", "chó", 8 * i, 8 * i + 7) for i in range(40)])
    labels, st = H.verify_image([big], lambda t: "no")
    ok(st["calls"] == 32 and st["cap_hits"] == 8 and labels[0][32:] == ["CAP"] * 8, "CAP = 32 calls per image")
    fm = H.filt_masks([["REJECTED", "UNCERTAIN"], ["SUPPORTED", "TEXT"]])
    ok(fm == [[True, False], [False, False]], "remove REJECTED obj only (UNCERTAIN stays)")
    ok(H.filt_masks([["UNCERTAIN", "CAP"]]) == [[False, False]], "a parse failure (UNCERTAIN) cannot empty a prompt")
    cm = H.ctl_masks("img1", [d1, d2], fm)
    ok([sum(m) for m in cm] == [1, 0] and not cm[1][1], "ctl: count-matched per demonstration, never text")
    ok(cm == H.ctl_masks("img1", [d1, d2], fm), "ctl seed arm_rng('A7', id) is deterministic")
    hits = {tuple(map(tuple, H.ctl_masks(f"img{i}", [d1, d2], fm))) for i in range(40)}
    ok(len(hits) == 2, "ctl draws among the demonstration's obj propositions")
    ok(all(H.ctl_masks(f"img{i}", [d1, d2], [[False, False], [True, False]]) == [[False, False], [True, False]]
           for i in range(40)), "ctl never draws a text proposition (strata: obj only)")
    w = {"order": "last", "tpl": "T2", "ret": {"q": ["c1", "c2"]}, "rand": {"q": ["c2", "c1"]},
         "shown": {"c1": d1["text"], "c2": d2["text"]}, "dc": {"c1": d1, "c2": d2}}
    t, info = H.arm_prompt(w, "ret", "q", "ZS", None)
    ok(t.splitlines()[1].endswith(d2["text"]), "InternVL3 'last': rank order reversed in the prompt")
    t, info = H.arm_prompt(w, "filt", "q", "ZS", [["REJECTED", "UNCERTAIN"], ["SUPPORTED", "TEXT"]])
    ok(info["removed"] == 1 and info["n_demos"] == 2 and "chó" not in t, "filt removes the REJECTED span")
    t, info = H.arm_prompt(w, "filt", "q", "ZS", [["REJECTED", "REJECTED"], ["SUPPORTED", "TEXT"]])
    ok(info["emptied"] == 1 and info["n_demos"] == 1, "an emptied demonstration is dropped, not back-filled")
    t, info = H.arm_prompt(w, "filt", "q", "ZS", [["SUPPORTED", "SUPPORTED"], ["REJECTED", "TEXT"]])
    ok(info["emptied"] == 1 and info["removed"] == 1, "R2-W10 (c): rebuild's sentence rule can empty a demonstration")
    w1 = {**w, "ret": {"q": ["c1"]}}
    t, info = H.arm_prompt(w1, "filt", "q", "ZS", [["REJECTED", "REJECTED"]])
    ok(t == "ZS" and info["fallback"] and info["emptied"] == 1, "all emptied -> zero-shot (fallback)")


def st_ledger(tmp: Path) -> None:
    o, hd = tmp / "o", tmp / "hd"
    (o / "logs").mkdir(parents=True)
    hd.mkdir()
    a = argparse.Namespace(out=o, branch="main", rate=10_092.0, rent_utc="2026-11-10T00:00:00Z", freeze="f" * 64)
    H.cmd_cap(a)
    must("written once", H.cmd_cap, a)
    c = H.cap_rec(o)
    ok(c["cap_h"] == 20.0 and c["rent_epoch"] == 1_794_268_800, "CAP.json: 20 h main, UTC stamp")
    ok(H.left(o, c["rent_epoch"] + 3600) == int((20 - 0.5 - 1) * 3600), "left = cap - billed elapsed - 0.5 h")
    dc = dcx("con chó", [("obj", "chó", 0, 7)])
    for b, ds in D.ORDER:
        items = [[f"i{n}", f"i{n}.jpg", "0" * 64] for n in range(100)]
        H.write_atomic(hd / f"work.{b}.{ds}.json", {"backbone": b, "set": ds, "items": items, "order": "first",
                                                   "ret": {i[0]: ["c"] for i in items}, "dc": {"c": dc}})
    pr = H.project(o, hd, list(D.BACKBONES), c["rent_epoch"] + 19.5 * 3600)
    ok(pr["cuts"] == ["internvl3_8b|ov_dev_b", "qwen25vl_7b|ov_dev_b", "internvl3_8b|xm_test2500"],
       "projection over the cap: cuts in order, Qwen XM kept")
    ok(H.cuts(o) == pr["cuts"], "cuts are sticky (CUTS.json)")
    ok(H.next_step(o, hd, "main", list(D.BACKBONES)) == "run.qwen25vl_7b", "next: Qwen first (§5.2)")
    for st in H.phases(H.work_of(hd, "qwen25vl_7b", "xm_test2500")):
        H.mark(o, st)
    ok(H.next_step(o, hd, "main", list(D.BACKBONES)) is None, "cut blocks never start")
    o2 = tmp / "o2"
    (o2 / "logs").mkdir(parents=True)
    H.cmd_cap(argparse.Namespace(**{**vars(a), "out": o2}))
    H.mark(o2, "verify.internvl3_8b.ov_dev_b")
    pr = H.project(o2, hd, list(D.BACKBONES), c["rent_epoch"] + 19.5 * 3600)
    ok("internvl3_8b|ov_dev_b" not in pr["cuts"], "a started block is not cut")
    o4 = tmp / "o4"
    (o4 / "logs").mkdir(parents=True)
    H.cmd_cap(argparse.Namespace(**{**vars(a), "out": o4}))
    pr = H.project(o4, hd, ["internvl3_8b"], c["rent_epoch"] + 19.5 * 3600)
    ok(pr["cuts"] == ["internvl3_8b|ov_dev_b"], "Qwen absent: InternVL3 XM-test2500 is the never-cut block")
    o3 = tmp / "o3"
    (o3 / "logs").mkdir(parents=True)
    H.cmd_cap(argparse.Namespace(**{**vars(a), "out": o3, "branch": "gate-only"}))
    ok(H.cap_rec(o3)["cap_h"] == 3.0 and H.next_step(o3, hd, "gate", []) == "gate.qwen25vl_7b", "gate-only: 3.0 h")
    must("gate-only branch runs no S2", H.next_step, o3, hd, "main", list(D.BACKBONES))
    H.progress(o3, "gate.qwen25vl_7b.xm_dev500", "qwen25vl_7b", "xm_dev500", 300, 150.0)
    ok(H.rate(o3, "qwen25vl_7b", "verify", "xm_test2500") == 0.5, "first projection uses the measured gate rate")
    ok(H.rate(o3, "internvl3_8b", "verify", "xm_test2500") == 1.30, "else the §8.1 planning rate")
    w = tmp / "shm"
    (w / "img").mkdir(parents=True, mode=0o700)
    (w / "img" / "a.jpg").write_bytes(b"a")
    (w / "MANIFEST.sha256").write_text(f"{D.sha(b'a')}  img/a.jpg\n", encoding="utf-8")
    log = tmp / "del.log"
    ok(H.cmd_wipe(argparse.Namespace(dir=str(w), log=str(log))) == 0 and not w.exists(), "wipe by name")
    ok(log.read_text("utf-8").split("\t")[2:] == ["2", "2\n"], "deletion log: files, manifest count")
    p = tmp / "rows.jsonl"
    p.write_text('{"u": 0}\n{"u": 1', encoding="utf-8")
    out = H.Out(p, "u")
    ok(set(out.done) == {0} and p.read_text("utf-8") == '{"u": 0}\n', "torn last line dropped on reopen")
    p.write_text('{"u": 0}\n{"u": 0}\n', encoding="utf-8")
    must("repeated u", H.Out, p, "u")


# ---------------------------------------------------------------------------------------------- statistics, Appendix D
def st_stats() -> None:
    import c_diag_score as SC
    ok(abs(float(SC.kappa(50, 10, 10, 50)) - 2 / 3) < 1e-12, "Cohen's κ")
    ok(np.isnan(SC.kappa(0, 0, 10, 50)) and np.isnan(SC.kappa(10, 0, 10, 0)), "degenerate κ = undefined")
    states = ("GF", "GC", "GB", "OK")
    pts = [(-1.0, -2.0, -0.5), (-1.0, -2.0, 0.5), (0.0, -1.0, 1.0), (1.0, 0.5, 1.5), (1.0, -0.5, 1.5),
           (3.0, 1.0, 4.0), (3.0, -0.5, 4.0)]  # the 7 (point, CI) patterns of D.1
    from collections import Counter
    c = Counter(SC.p_state(g, h, p, lo, hi) for g in states for h in (True, False) for p, lo, hi in pts)
    ok(sum(c.values()) == 56 and c == {"GF": 14, "GC": 14, "GB": 14, "UP": 1, "UPs": 1, "DOWN": 1, "NS": 11}, f"D.1 {c}")
    ok(SC.p_state("OK", True, 1.0, -0.5, 1.5) == "NS", "a Holm reject whose CI includes 0 -> NS")
    lab = Counter(SC.summary(fr, fc, r, cc) for fr in SC.P_STATES for fc in SC.P_STATES for r in (1, 0) for cc in (1, 0))
    ok(lab == {"S0": 84, "S1": 2, "S2": 6, "S3": 5, "S3c": 15, "S4": 7, "S4c": 21, "S5": 28, "S6": 28}, f"D.2 {lab}")
    ok(SC.harm_state(-3, -1, 2, "C") == "C1" and SC.harm_state(-1, -0.5, 2, "C") == "C2" and
       SC.harm_state(-3, 1, 2, "C") == "C3" and SC.harm_state(-1, 1, 2, "R") == "R4", "C1-C4 / R1-R4")
    ok(SC.guard_of({"filt": 0.9, "x": 0.9}, "filt", "x") == "GB" and SC.guard_of({"filt": 0.9, "x": 1}, "filt", "x") == "GF"
       and SC.guard_of({"filt": 1, "x": 0.94}, "filt", "x") == "GC" and SC.guard_of({"filt": .95, "x": .95}, "filt", "x")
       == "OK", "both-fail guard labels (CC-298 Ruling 3)")
    h = SC.holm({"a": 0.01, "b": 0.04, "c": 0.03})
    ok(h["a"][0] and not h["c"][0] and not h["b"][0] and abs(h["a"][1] - 0.03) < 1e-12, "Holm step-down, m = 3")
    ok(SC.holm({"a": 0.02, "b": 0.04})["b"][0] and abs(SC.holm({"a": 0.02, "b": 0.04})["b"][1] - 0.04) < 1e-12, "m = 2")
    rng = np.random.default_rng(0)
    sw = rng.integers(0, 2, size=(10_000, 50), dtype=np.int64)
    hp = np.full(50, 5)
    p = SC.perm_p(hp, np.zeros(50, int), np.zeros(50, int), np.full(50, 5), sw)
    ok(p == 1 / 10_001, "permutation p floor 1/10,001")
    ok(SC.perm_p(hp, np.full(50, 1), hp, np.full(50, 1), sw) == 1.0, "identical arms: p = 1")
    W = SC.wmat(np.array([[0, 0, 1], [2, 2, 2]]), 3)
    ok(W.tolist() == [[2, 1, 0], [0, 0, 3]], "counts matrix")
    G = SC.Boot({"x": [1, 0, 0], "y": [1, 1, 1]}, SC.wmat(rng.integers(0, 3, size=(10_000, 3)), 3))
    try:
        SC.est(G, lambda S: S("x") / (S("x") - S("x")))
        raise AssertionError("> 1 % undefined replicates must be a BlockFault")
    except SC.BlockFault:
        ok(True, "§6.1: > 1 % undefined = FAULT")
    e = SC.est(G, lambda S: S("x") / (S("x") - S("x")), strict=False)
    ok(e["dropped"] == 10_000 and "note" in e, "descriptive rows flag, not FAULT")
    units = [{"u": n, "qid": f"q{n // 2}"} for n in range(40)]
    status = [{"u": n, "status": ("present", "absent")[n % 2]} for n in range(40)]
    rows = {n: {"label": ("SUPPORTED", "REJECTED")[n % 2]} for n in range(40)}
    ci = SC.kappa_ci(units, status, rows)
    ok(ci["n_q"] == 20 and not ci["fault"] and ci["ci"] == [1.0, 1.0], "κ CI over 20 query clusters")
    one = [{"u": n, "qid": f"q{n}"} for n in range(4)]
    ci = SC.kappa_ci(one, status[:4], rows)
    ok(ci["fault"] and ci["dropped"] > 100, "> 1 % undefined κ replicates = gate FAULT (degenerate κ)")
    rows2 = {n: {"label": ("SUPPORTED", "REJECTED", "UNCERTAIN", "SUPPORTED")[n % 4], "parse_fail": n % 4 == 2,
                 "blind_label": "SUPPORTED", "blind_parse_fail": False} for n in range(40)}
    gt = SC.gate_table(units, status, rows2)
    ok(gt["N_P"] == 20 and gt["N_A"] == 20 and gt["uncertain_share"] == 10 / 40 and gt["parse_fail"] == 10 and
       gt["no_rate_absent"] == 10 / 20 and gt["kappa_blind"] is None, "§4.2 denominators include UNCERTAIN")
    t = {"kappa": 0.007, "kappa_blind": None, "no_rate_present": 0.987, "no_rate_absent": 0.99,
         "supported_share_present": 0.0225, "uncertain_share": 0.0001}
    v = SC.verdict(t, {"fault": False, "ci": [0.004, 0.010]})
    ok(v["status"] == "FAIL" and not v["V1"] and not v["V2"] and not v["V3"], "tier-1 values FAIL the gate")
    t2 = {"kappa": 0.6, "kappa_blind": None, "no_rate_present": 0.2, "no_rate_absent": 0.7,
          "supported_share_present": 0.7, "uncertain_share": 0.1}
    ok(SC.verdict(t2, {"fault": False, "ci": [0.3, 0.8]})["pass"], "a PASS case; κ_blind undefined -> 0 (V5)")
    ok(not SC.verdict({**t2, "kappa_blind": 0.45}, {"fault": False, "ci": [0.3, 0.8]})["V5"], "V5 needs κ - κ_blind >= .2")
    ok(not SC.verdict({**t2, "kappa": None}, {"fault": False, "ci": None})["pass"], "undefined κ = V1 FAIL")
    ok(not SC.verdict(t2, {"fault": False, "ci": [0.19, 0.8]})["V1"], "κ CI lower bound >= 0.20")
    ok(SC.verdict(t2, {"fault": True})["status"] == "gate FAULT (degenerate κ)", "κ FAULT = no verdict")
    for k2, bad in (("no_rate_present", 0.41), ("no_rate_absent", 0.39), ("supported_share_present", 0.49),
                    ("uncertain_share", 0.21)):
        ok(not SC.verdict({**t2, k2: bad}, {"fault": False, "ci": [0.3, 0.8]})["pass"], f"gate bound {k2}")
    ok(SC.verdict({**t2, "no_rate_present": 0.40, "no_rate_absent": 0.40, "supported_share_present": 0.50,
                   "uncertain_share": 0.20, "kappa": 0.40, "kappa_blind": 0.20}, {"fault": False, "ci": [0.20, .8]})["pass"],
       "every gate bound is inclusive")



def st_rules() -> None:
    """The small registered predicates, directly (§1.3, §4.1, N20, §3.3)."""
    import c_diag_score as SC
    ok(D.floor_pass(0.10) and not D.floor_pass(0.0999) and not D.floor_pass(None), "§1.3 floor c_b >= 0.10")
    f = {"qwen25vl_7b": {"passes_floor": False}, "internvl3_8b": {"passes_floor": True}}
    ok(not D.gate_only_branch(f) and D.gate_only_branch({b: {"passes_floor": False} for b in D.BACKBONES}),
       "R2-W1 (a): the gate-only branch only when both c_b < 0.10")
    st = {"chó": "present", "mèo": "absent", "xe": "unknown"}
    pr = lambda cls, kind="obj": {"kind": kind, "classes": cls}  # noqa: E731
    ok(D.unit_ok(pr(["chó"]), st) and D.unit_ok(pr(["mèo"]), st), "§4.1 present / absent units")
    ok(not D.unit_ok(pr(["xe"]), st) and not D.unit_ok(pr(["bò"]), st), "unknown status is out")
    ok(not D.unit_ok(pr(["chó", "mèo"]), st) and not D.unit_ok(pr([], "text"), st), "two classes / text are out")
    m = lambda t: frozenset(c for c in ("chó", "mèo") if c in t)  # noqa: E731
    dc = dcx("con chó", [("obj", "chó", 4, 7), ("obj", "mèo", 0, 3)])
    ok(D.obj_units(dc, m) == {"chó"}, "T1-REP §1 unit: carried AND found by the scorer of record")
    ok(SC.pcm(["chó", "mèo", "xe"], ["mèo"], {"chó": "present"}) == (1, 0, 1), "ΔP_cm: k = min, first k classes")
    lad = D.ladder(mk_units(200, 200, ranks=(1,), per_q=5))
    ok(lad["rung"] == "c" and lad["supply"]["a"] == {"present": 120, "absent": 120}, "per-query cap 3 at (a), 5 at (c)")


class FakeNet:
    pass


def st_gpu_paths(tmp: Path) -> None:
    """run_block and cmd_gate with a fake model (no torch): verify loop, texts record, CC-212 prompt check, decode
    output, resume; the gate's image and blind passes; the FAULT exit code 9."""
    import subprocess
    o, hd = tmp / "o", tmp / "hd"
    (o / "logs").mkdir(parents=True)
    (o / "out").mkdir()
    (hd / "img" / "xm_test2500").mkdir(parents=True)
    H.cmd_cap(argparse.Namespace(out=o, branch="main", rate=10_092.0, rent_utc=D.utc(), freeze="f" * 64))
    d1 = dcx("con chó và con mèo", [("obj", "chó", 0, 7), ("obj", "mèo", 11, 18)])
    items = [[f"i{n}", f"i{n}.jpg", "0" * 64] for n in range(5)]
    w = {"backbone": "qwen25vl_7b", "set": "xm_test2500", "order": "first", "tpl": "T1", "items": items,
         "ret": {i[0]: ["c1"] for i in items}, "rand": {i[0]: ["c1"] for i in items}, "shown": {"c1": d1["text"]},
         "dc": {"c1": d1}, "zs_sha256": D.C.sha(D.ZS)}
    w["prompt_sha256"] = {arm: {q: D.C.sha(H.arm_prompt(w, arm, q, D.ZS, None)[0]) for q, _f, _h in items}
                          for arm in ("ret", "rand")}
    H.write_atomic(hd / "work.qwen25vl_7b.xm_test2500.json", w)
    saved = (D.C.lb.make_generate, H.asker, H.model, H.text_only, D.C.lb.packages)
    D.C.lb.packages = lambda: dict(D.REG["venv"]["packages"])
    seen = []
    D.C.lb.make_generate = lambda proc, net, prompt, n, folder: (
        lambda sl, texts: seen.extend(texts) or [("Một con chó.", 4, False) for _ in sl])
    H.asker = lambda proc, net, folder, item: (lambda text: "no" if "mèo" in text else "yes")
    try:
        a = argparse.Namespace(out=o, hd=hd, models=["qwen25vl_7b"])
        reg, m = D.REG, D.REG["models"]["qwen25vl_7b"]
        H.run_block(a, w, FakeNet(), FakeNet(), reg, m)
        ok(all(H.done(o, st) for st in H.phases(w)), "every phase of the block marked done")
        v = H.Out(o / "out" / "verify.qwen25vl_7b.xm_test2500.jsonl", "id").done
        ok(v["i0"]["labels"] == [["SUPPORTED", "REJECTED"]] and v["i0"]["calls"] == 2, "verify rows: labels, counts")
        tx = json.loads((o / "out" / "texts.qwen25vl_7b.xm_test2500.json").read_text("utf-8"))["arms"]
        ok(tx["filt"]["i0"]["removed"] == 1 and tx["ctl"]["i0"]["removed"] == 1 and tx["ret"]["i0"]["removed"] == 0,
           "texts: filt and count-matched ctl remove one obj span")
        dec = json.loads((o / "out" / "decode.qwen25vl_7b.xm_test2500.filt.json").read_text("utf-8"))
        ok(set(dec["predictions"]) == {i[0] for i in items} and dec["decode_order"] == [i[0] for i in items],
           "decode output: every id, CC-212 order")
        ok("mèo" not in json.dumps(dec) and "con chó và con mèo" not in json.dumps(tx), "no demonstration text out")
        n0 = len(seen)
        H.run_block(a, w, FakeNet(), FakeNet(), reg, m)
        ok(len(seen) == n0, "a finished block is not decoded again (resume)")
        for st in H.phases(w)[1:]:
            (o / "logs" / f"done.{st}").unlink()
        bad = {**w, "prompt_sha256": {**w["prompt_sha256"], "ret": {q: "0" * 64 for q in w["ret"]}}}
        must("host prompt differs", H.run_block, a, bad, FakeNet(), FakeNet(), reg, m)
        must("zero-shot prompt differs", H.run_block, a, {**w, "zs_sha256": "0" * 64}, FakeNet(), FakeNet(), reg, m)
        (hd / "img" / "xm_dev500").mkdir()
        H.write_atomic(hd / "gate_units.json", [{"u": n, "qid": f"g{n}", "file": "g.jpg", "image_sha256": "0" * 64,
                                                 "rank": 1, "prop_index": 0, "text": t}
                                                for n, t in enumerate(("con chó", "con mèo", "xx"))])
        H.model = lambda b, snap: (D.REG, m, FakeNet(), FakeNet())
        H.text_only = lambda proc, net, n: (lambda texts: ["maybe" for _ in texts])
        H.P["ver_3way.txt"] = (D.ROOT / "scripts/c_pvr/prompts/ver_3way.txt").read_text("utf-8")
        H.asker = lambda proc, net, folder, item: (lambda text: {"con chó": "Yes", "con mèo": "No"}.get(text, "?"))
        H.cmd_gate(argparse.Namespace(out=o, hd=hd, model="qwen25vl_7b", snapshot=None))
        g = H.Out(o / "out" / "gate.qwen25vl_7b.jsonl", "u").done
        ok([g[n]["label"] for n in range(3)] == ["SUPPORTED", "REJECTED", "UNCERTAIN"] and g[2]["parse_fail"] and
           all(g[n]["blind_label"] == "UNCERTAIN" for n in range(3)), "gate: image pass, parse failure, blind pass")
        ok(json.loads((o / "logs" / "rate.gate.qwen25vl_7b.xm_dev500.json").read_text("utf-8"))["n"] == 3, "gate rate record")
    finally:
        D.C.lb.make_generate, H.asker, H.model, H.text_only, D.C.lb.packages = saved
    r = subprocess.run([sys.executable, "-X", "utf8", "-I", "-B", str(HERE / "c_diag_gpu.py"), "cap", "--out", str(o), "--branch",
                        "main", "--rate", "10092", "--rent-utc", D.utc(), "--freeze", "f" * 64], capture_output=True)
    ok(r.returncode == H.FAULT_RC == 9 and b"written once" in r.stderr, "a FAULT exits 9 (the job's JOB STOP code)")


# ---------------------------------------------------------------------------------------------- the synthetic world
CAPS = {"m0": ("ktvic", "Một con chó lặng lẽ thổi kèn đồng giữa trưa."),  # made-up, deliberately odd sentences
        "m1": ("ktvic", "Một chiếc xe đạp biết hát dựa vào nhà kính."),
        "m2": ("openviic", "Hai con mèo ngáp dài trên ghế bập bênh."),
        "m3": ("ktvic", "Người đàn ông tí hon ôm chiếc ô tô bằng giấy."),
        "m4": ("openviic", "Một con chó lười và một con mèo ú cùng đếm sao băng."),
        "m5": ("ktvic", "Cái ghế gỗ biết bay qua căn phòng ngủ trưa."),
        "m6": ("ktvic", "Chiếc thuyền mơ màng trôi ngược dòng sông."),
        "m7": ("openviic", "Con ngựa kể chuyện cười cho cánh đồng nghe."),
        "m8": ("ktvic", "Một con chim đội mũ len đậu trên cây thông."),
        "m9": ("openviic", "Chiếc xe buýt nhảy dây trên vỉa hè lúc nửa đêm.")}
SIZES = {"xm_dev500": 6, "xm_test2500": 8, "ov_dev_b": 4}
OUTS = ["Một con chó trên cỏ.", "Con mèo nằm trên ghế.", "Một chiếc thuyền trên sông.", "Chiếc xe buýt.",
        "Người đàn ông và con ngựa.", "Một con chim trên cây.", "Cái ghế trong phòng.", "a dog"]


class World:
    """Synthetic files at every data row the C-DIAG code opens; D.B / D.SETS / D.N_LABEL_IDS / D.CELL patched."""

    def __init__(self, tmp: Path):
        self.t = tmp
        self.saved = (dict(D.B), dict(D.SETS), D.N_LABEL_IDS, D.CELL, D.CELL_MIN, D.DATA)
        D.SETS.update({k: (v[0], SIZES[k], v[2]) for k, v in D.SETS.items()})
        D.N_LABEL_IDS, D.CELL, D.CELL_MIN = 14, 3, 2
        D.DATA = tmp / "data"
        C = D.C
        pre = {"xm_dev500": "xd", "xm_test2500": "xt", "ov_dev_b": "ob"}
        self.rows = {ds: [[f"{pre[ds]}{n}", f"{pre[ds]}{n}.jpg", D.sha(f"{ds}{n}".encode())] for n in range(k)]
                     for ds, k in SIZES.items()}
        self.rows["ov_dev_a"] = [["oa0.jpg", "oa0.jpg", D.sha(b"oa0")]]
        mem = [{"cid": c, "members": [[src, str(i) if src == "ktvic" else f"tr{i}.jpg", f"tr{i}.jpg",
                                       D.sha(f"tr{i}".encode())]]} for i, (c, (src, _t)) in enumerate(CAPS.items())]
        lists = {"design_sha256": C.PINS[C.DESIGN], "sets": self.rows, "memory": mem,
                 "refuse": {"openviic_files": [], "image_sha256": []}}
        self.put("lists", "lists.json", lists)
        frozen = {"models": {m: {"k": c["k"], "order": c["order"], "tpl": c["tpl"], "tau": "-inf"}
                             for m, c in D.BACKBONES.items()}}
        self.put("frozen", "frozen_config.json", frozen)
        cids = list(CAPS)
        for ds in SIZES:
            ret = {q: [[cids[(n + j) % 10], 0.9 - j / 20] for j in range(8)] for n, (q, _f, _h) in enumerate(self.rows[ds])}
            rand = {q: [cids[(n * 3 + j + 1) % 10] for j in range(8)] for n, (q, _f, _h) in enumerate(self.rows[ds])}
            self.put(D.SETS[ds][2], f"ex_{ds}.json", {"design_sha256": C.PINS[C.DESIGN], "set": ds, "ret": {ds: ret},
                                                      "rand": {ds: rand}, "lists_sha256": D.sha(self.b("lists"))})
        kt = {"annotations": [{"image_id": int(m[1]), "caption": CAPS[m_["cid"]][1]} for m_ in mem for m in m_["members"]
                              if m[0] == "ktvic"]}
        ov = {m[1]: {"captions": [CAPS[m_["cid"]][1]]} for m_ in mem for m in m_["members"] if m[0] == "openviic"}
        self.put("kt_train", "data/datasets/ktvic/train_data.json", kt)
        self.put("ov_train", "data/datasets/openviic/uit-openviic-annotation-train.json", ov)
        vmap = self.vmap()
        xm_ids = [r[0] for ds in ("xm_dev500", "xm_test2500") for r in self.rows[ds]]
        A = ["chó", "xe đạp", "thuyền", "chim", "ngựa"]
        Bc = ["mèo", "ghế", "đàn ông", "xe buýt", "người"]
        lab = {q: {"pos": sorted({m for c in (A if n % 2 else Bc) for m in vmap[c]["pos"]}),
                   "neg": sorted({m for c in (Bc if n % 2 else A) for m in vmap[c]["neg"]})} for n, q in enumerate(xm_ids)}
        lab["xm600_only_id"] = {"pos": sorted(vmap["chó"]["pos"]), "neg": []}
        lab["_note"] = "synthetic"
        self.put("oiv7", "oiv7_labels.json", lab)
        self.put("xm_img", "xm_test2500.sha256", None,
                 "".join(f"{h}  {f}\n" for _i, f, h in self.rows["xm_test2500"]).encode())
        refs = {"release_sha256": "101d24ad98e9dec43625ee425fa1b49aa1bde98f9609945bf5dd4424fef1dacc",
                "images": [{"id": r[0]} for r in self.rows["xm_test2500"]],
                "annotations": [{"image_id": r[0], "caption": OUTS[n % 7]} for n, r in enumerate(self.rows["xm_test2500"])]}
        self.put("xm_refs", "xm_test2500_data.json", refs)
        self.put("ov_refs", "ov_dev.json", {r[0]: {"captions": [OUTS[n % 7] + " "]} for n, r in
                                            enumerate(self.rows["ov_dev_b"] + self.rows["ov_dev_a"])})
        self.preds()

    def vmap(self):
        D.XO.MAP = D.path("vi_map")
        return D.XO.resolve_map(D.path("desc"))

    def b(self, key):
        return D.path(key).read_bytes()

    def put(self, key, rel, obj, raw: bytes | None = None):
        p = self.t / rel
        p.parent.mkdir(parents=True, exist_ok=True)
        b = raw if raw is not None else json.dumps(obj, ensure_ascii=False).encode()
        p.write_bytes(b)
        D.B[key] = (str(p), D.sha(b))

    def preds(self, tamper: bool = False, english: bool = False, reorder: bool = False):
        s = D.S0()
        reg = D.REG
        for (b, ds, arm), (rel, _h) in D.PREDS.items():
            items = [tuple(r) for r in self.rows[ds]]
            ps = {q: D.C.sha(D.C.prompt(D.BACKBONES[b]["tpl"], [s.shown(ds, c) for c in s.prompt_ids(b, ds, arm, q)]))
                  for q, _f, _h in items}
            if tamper:
                ps[items[0][0]] = "0" * 64
            m = reg["models"][b]
            d = {"run_id": Path(rel).name, "model": b, "dataset": ds, "batch_size": m["batch_size"],
                 "hub_id": m["hub_id"], "revision": m["revision"], "dtype": m["dtype"],
                 "attn_implementation": m["attn_implementation"], "venv_freeze_sha256": "f" * 64,
                 "packages": reg["venv"]["packages"], "manifest_sha256": D.C.sha(json.dumps(items)),
                 "prompt_sha256_per_image": ps,
                 "predictions": {q: OUTS[n % (8 if english and arm == "rand" else 7)] for n, (q, _f, _h) in
                                 enumerate(items[::-1] if reorder and arm == "ret" else items)}}
            self.put("pred|" + "|".join((b, ds, arm)), f"preds/{Path(rel).name}.preds.json", d)

    def close(self):
        D.B.clear()
        D.B.update(self.saved[0])
        D.SETS.clear()
        D.SETS.update(self.saved[1])
        D.N_LABEL_IDS, D.CELL, D.CELL_MIN, D.DATA = self.saved[2:]
        D.XO.MAP = D.ROOT / "data/xm3600/vi_oiv7_map.json"


def stage0(cmd: str, w: Path, labels: Path | None = None, extra: list | None = None) -> str:
    """One Stage-0 subcommand in-process under a fresh hook; returns its stdout JSON line."""
    import contextlib
    import io
    fresh_guard()
    a = argparse.Namespace(cmd=cmd, work=str(w), labels=str(labels) if labels else None,
                           labels_sha=D.sha(labels.read_bytes()) if labels else None, rate=10_092.0)
    for k, v in (extra or []):
        setattr(a, k, v)
    buf = io.StringIO()
    try:
        with contextlib.redirect_stdout(buf):
            D.run(a)
    finally:
        off()
    return buf.getvalue()


def st_world(tmp: Path) -> dict:
    w = World(tmp / "world")
    try:
        wk = tmp / "W"
        wk.mkdir()
        stage0("lists", wk)
        stage0("label-subset", wk)
        lab = wk / "label_subset.json"
        sub = json.loads(lab.read_text("utf-8"))
        ok("xm600_only_id" not in sub and len(sub) - 1 == 14, "label subset: XM600 rows discarded (NB-3)")
        out = json.loads(stage0("decomp", wk))
        ok(out["obj_props"] > 0 and out["decomp_fail"] == 0, "decompose_vi on the shown captions (ranks 1-8)")
        g = json.loads(stage0("gate-sample", wk, lab))
        hu = json.loads((wk / "gate_units.json").read_text("utf-8"))
        ok(g["rung"] in ("a", "b", "c") and len(hu) == 6 and g["gate_units_sha256"] == D.sha((wk / "gate_units.json")
                                                                                             .read_bytes()),
           "gate sample under the hook (CELL patched to 3)")
        ok(all(not any(x in u["text"].lower() for x in ("hai ", "nằm", "đứng")) for u in hu), "only bare units")
        f = json.loads(stage0("floor", wk, lab))
        ok(all(0 <= f[b]["c_b"] <= 1 for b in D.BACKBONES), "floor c_b computed")
        v = json.loads(stage0("vi-pre", wk))
        ok(all(v[f"{b}|{ds}|{arm}"]["byte_equal_computable"] for b, ds, arm in D.PREDS), "parity reconstructable")
        stage0("counts", wk, lab)
        m = json.loads(stage0("manifest", wk, lab))
        ok(m["branch"] in ("main", "gate_only") and (wk / f"push_{m['branch']}" / "MANIFEST.sha256").exists(), "manifest")
        stage0("pins", wk)
        ok(all(json.loads((wk / f).read_text("utf-8"))["label"] == D.LABEL for f in
               ("floor.json", "vi_pre.json", "counts.json", "pins.json")), "LABEL in every Stage-0 record (N4)")
        sums = (wk / "STAGE0_SUMS").read_text("utf-8").splitlines()
        ok(len(sums) >= 9 and all(len(x.split("  ")[0]) == 64 for x in sums), "STAGE0_SUMS lines for the LOG line")
        must("written once", stage0, "lists", wk)
        return {"world": w, "work": wk, "labels": lab, "manifest": m}
    except BaseException:
        w.close()
        raise


def st_world_faults(ctx: dict, tmp: Path) -> None:
    w, wk, lab = ctx["world"], ctx["work"], ctx["labels"]
    w.preds(tamper=True)
    wk2 = tmp / "W2"
    wk2.mkdir()
    must("rebuilt prompts differ", stage0, "manifest", wk2, lab)
    w.preds(reorder=True)
    v = json.loads(stage0("vi-pre", wk2))
    ok(not v["qwen25vl_7b|xm_test2500|ret"]["byte_equal_computable"] and
       v["qwen25vl_7b|xm_test2500|rand"]["byte_equal_computable"], "DC2: decode order not CC-212's -> not computable")
    (wk2 / "vi_pre.json").unlink()
    w.preds(english=True)  # one English caption in 8 XM rand decodes: VI-script share 0.875 < 0.95
    c = json.loads(stage0("counts", wk2, lab))
    ok(c["plan"]["kept"] == ["qwen25vl_7b|ov_dev_b", "internvl3_8b|ov_dev_b"], "§14 item 7: XM blocks dropped")
    w.preds()
    bad = json.loads(lab.read_text("utf-8"))
    bad["xm600_only_id"] = {"pos": [], "neg": []}
    lab2 = tmp / "label_bad.json"
    lab2.write_text(json.dumps(bad), encoding="utf-8")
    must("outside XM-dev500", stage0, "floor", wk2, lab2)
    saved = D.CELL_MIN
    D.CELL, D.CELL_MIN = 100, 100
    must("fewer than 100 units", stage0, "gate-sample", wk2, lab)
    D.CELL, D.CELL_MIN = 3, saved
    must("--labels-sha", stage0, "floor", wk2, lab, [("labels_sha", "abc")])
    must("--rate", stage0, "counts", wk2, lab, [("rate", None)])  # CC-307 N5: no default offer rate
    p = D.path("lists")
    raw = p.read_bytes()
    p.write_bytes(raw + b" ")
    (tmp / "W3").mkdir()
    must("sha256 differs", stage0, "lists", tmp / "W3")
    p.write_bytes(raw)


def pull_world(ctx: dict, tmp: Path, gate_only: bool = False, drop: str | None = None, stop: bool = False) -> dict:
    """Simulate the host on the pushed files with fake model answers; write the pulled dir and its SUMS."""
    w, wk, lab = ctx["world"], ctx["work"], ctx["labels"]
    s = D.S0(lab)
    pull = tmp / f"pull_{len(list(tmp.iterdir()))}"
    (pull / "out").mkdir(parents=True)
    (pull / "logs").mkdir()
    units = json.loads((wk / "gate_units.json").read_text("utf-8"))
    st = {x["u"]: x["status"] for x in json.loads((wk / "gate_status.json").read_text("utf-8"))}
    for b in D.BACKBONES:
        if drop == f"gate.{b}":
            continue
        with open(pull / "out" / f"gate.{b}.jsonl", "w", encoding="utf-8") as f:
            for u in units:
                good = st[u["u"]] == "present"
                f.write(json.dumps({"u": u["u"], "qid": u["qid"], "label": "SUPPORTED" if good else "REJECTED",
                                    "parse_fail": False, "blind_label": "UNCERTAIN", "blind_parse_fail": False}) + "\n")
    (pull / "logs" / "job.log").write_text("2026-11-10T01:00:00Z JOB DONE gate-only\n", encoding="utf-8")
    if not gate_only:
        push = wk / "push_main"
        zs = D.ZS
        for b in D.BACKBONES:
            for ds in D.ARMS:
                wf = push / f"work.{b}.{ds}.json"
                if not wf.exists():
                    continue
                wd = json.loads(wf.read_text("utf-8"))
                ver = {}
                for q, _f, _h in wd["items"]:
                    labels, cnt = H.verify_image([wd["dc"][c] for c in wd["ret"][q]],
                                                 lambda t: "no" if "mèo" in t or "ghế" in t else "yes")
                    ver[q] = {"id": q, "labels": labels, **{k: cnt[k] for k in ("calls", "cap_hits", "parse_fail",
                                                                                "yes", "maybe", "no")}}
                (pull / "out" / f"verify.{b}.{ds}.jsonl").write_text("".join(json.dumps(r) + "\n" for r in ver.values()), encoding="utf-8")
                rec = {}
                for arm in D.ARMS[ds]:
                    rec[arm] = {}
                    for q, _f, _h in wd["items"]:
                        t, info = H.arm_prompt(wd, arm, q, zs, ver[q]["labels"])
                        rec[arm][q] = {**info, "prompt_sha256": D.C.sha(t)}
                    if f"{b}.{ds}.{arm}" == drop:
                        continue
                    caps = {q: OUTS[(n + len(arm)) % 8] for n, (q, _f, _h) in enumerate(wd["items"])}
                    if arm in ("ret", "rand"):
                        caps = D.preds(b, ds, arm)["predictions"]
                    (pull / "out" / f"decode.{b}.{ds}.{arm}.json").write_text(json.dumps({"predictions": caps}), encoding="utf-8")
                (pull / "out" / f"texts.{b}.{ds}.json").write_text(json.dumps({"arms": rec}), encoding="utf-8")
    name = "SHA256SUMS_gate-only" if gate_only else "SHA256SUMS_main"
    name += "_stop" if stop else ""
    body = "".join(f"{D.sha(p.read_bytes())}  {p.relative_to(pull)}\n" for p in sorted(pull.rglob("*")) if p.is_file())
    (pull / name).write_text(body, encoding="utf-8")
    return {"pull": pull, "sums": name, "sums_sha": D.sha(body.encode()), "status": s}


def score_args(pc: dict, ctx: dict, res: Path, **kw):
    res.mkdir()
    base = {"pull": str(pc["pull"]), "sums": pc["sums"], "sums_sha": pc["sums_sha"], "res": str(res),
            "labels": str(ctx["labels"]), "labels_sha": D.sha(ctx["labels"].read_bytes()),
            "gate_sha": D.sha((ctx["work"] / "gate_units.json").read_bytes()), "deleted_utc": None, "cider": None,
            "cider_sha": None}
    return argparse.Namespace(**{**base, **kw})


def scored(fn, a):
    import contextlib
    import io
    fresh_guard()
    try:
        with contextlib.redirect_stdout(io.StringIO()):
            r = fn(a)
        D.GUARD.done()
        return r
    finally:
        off()


def st_score(ctx: dict, tmp: Path) -> None:
    import c_diag_score as SC
    pc = pull_world(ctx, tmp)
    g = scored(SC.cmd_gate, score_args(pc, ctx, tmp / "r_gate"))
    ok(all(v["status"] in ("PASS", "gate FAULT (degenerate κ)") for v in g["verifiers"].values()) and
       g["pass"] == [m for m, v in g["verifiers"].items() if v["status"] == "PASS"],
       "gate verdict on a perfect synthetic verifier (a 6-unit sample may be degenerate)")
    must("--gate-sha", scored, SC.cmd_gate, score_args(pc, ctx, tmp / "r_g2", gate_sha="0" * 64))
    must("sha256 differs", scored, SC.cmd_gate, score_args({**pc, "sums_sha": "0" * 64}, ctx, tmp / "r_g3"))
    go = pull_world(ctx, tmp, gate_only=True)
    must("--deleted-utc", scored, SC.cmd_gate, score_args(go, ctx, tmp / "r_g4"))
    bad = tmp / "pull_abs"
    bad.mkdir()
    (bad / "S").write_text(f"{'0' * 64}  /etc/x\n", encoding="utf-8")
    must("malformed", SC.pulled, bad, "S", D.sha((bad / "S").read_bytes()))  # CC-307 N2
    must("--deleted-utc", scored, SC.cmd_gate, score_args(go, ctx, tmp / "r_g5", deleted_utc="2026-11-10T00:59:00Z"))
    g = scored(SC.cmd_gate, score_args(go, ctx, tmp / "r_g6", deleted_utc="2026-11-10T01:30:00Z"))
    ok(g["branch"] == "gate-only" and g.get("deleted_utc") and "incomplete" not in str(g["verifiers"]),
       "gate-only verdict after the logged delete")
    g1 = pull_world(ctx, tmp, gate_only=True, drop="gate.internvl3_8b")
    g = scored(SC.cmd_gate, score_args(g1, ctx, tmp / "r_g8", deleted_utc="2026-11-10T01:30:00Z"))
    ok(all("whole branch incomplete" in v["status"] for v in g["verifiers"].values()) and not g["pass"],
       "R3: in the gate-only branch one verifier incomplete = no verdict for either")
    gs = pull_world(ctx, tmp, gate_only=True, stop=True)
    g = scored(SC.cmd_gate, score_args(gs, ctx, tmp / "r_g7", deleted_utc="2026-11-10T01:30:00Z"))
    ok(not g["pass"] and all("incomplete" in v["status"] for v in g["verifiers"].values()), "cap stop -> incomplete (R3)")
    ok(ctx["manifest"]["branch"] == "main" and ctx["manifest"]["plan"]["kept"], "the world exercises the main branch")
    a = score_args(pc, ctx, tmp / "r_cider")
    cv = scored(SC.cmd_cider, a)
    ok(cv["n"] == {"xm_test2500": 8, "ov_dev_b": 4}, "CIDEr-VI over the two reference files")
    cf = tmp / "r_cider" / "cider_vi.json"
    for key, mut, frag in (("xm_refs", lambda d: {**d, "release_sha256": "0" * 64}, "release 101d24ad"),
                           ("ov_refs", lambda d: {**d, "extra.jpg": {"captions": ["x"]}}, "1,836-key")):
        raw = ctx["world"].b(key)
        ctx["world"].put(key, Path(D.B[key][0]).name, mut(json.loads(raw)))
        must(frag, scored, SC.cmd_cider, score_args(pc, ctx, tmp / f"r_c_{key}"))
        ctx["world"].put(key, Path(D.B[key][0]).name, None, raw)
    os.environ["RESCAP_RAW_TONE"] = "1"
    try:
        must("RESCAP_RAW_TONE is set", scored, SC.cmd_score, score_args(pc, ctx, tmp / "r_rt", cider=str(cf),
                                                                        cider_sha=D.sha(cf.read_bytes())))
    finally:
        del os.environ["RESCAP_RAW_TONE"]
    sc = scored(SC.cmd_score, score_args(pc, ctx, tmp / "r_score", cider=str(cf), cider_sha=D.sha(cf.read_bytes())))
    kept = [k for k in ctx["manifest"]["plan"]["kept"] if k.endswith("xm_test2500")]
    ok(sc["m"]["m"] == 3 * len(kept), "m = 3 x completed XM blocks, recorded before any contrast")
    for k in kept:
        b = k.split("|")[0]
        blk = sc["blocks"][k]
        ok(set(blk["contrasts"]) == {"filt-ret", "filt-ctl", "filt-rand"} and "insitu" in blk and "dP_cm" in blk,
           "XM block numbers")
        ok(blk["parity"]["ret"]["byte_equal_share"] == 1.0, "re-decoded ret identical -> byte-equal share 1")
        txt = D.dump(sc).decode()
        ok("ret-rand" not in txt and "rand-ret" not in txt, "R5: no ret - rand number")
        ok("NB-4" in blk["contrasts"]["filt-ctl"]["disclosure"] and "punctuation_dependent" in blk["harm"]["CIDEr_VI"],
           "NB-4 beside filt - ctl; punctuation-dependent flag")
        ok(sc["labels"][b]["label"] in SC.LABELS or sc["labels"][b]["label"] == "S0", "a summary label")
    ok(len(kept) == 2, "both XM blocks kept in the world")
    for b in D.BACKBONES:
        ok(set(sc["blocks"][f"{b}|ov_dev_b"]["byte_equal_share"]) == {"ret", "rand"},
           "§5.3: OV-dev-B byte-equal share for ret and rand (CC-307 W2)")
    ok(json.loads(cf.read_text("utf-8"))["label"] == D.LABEL, "LABEL in cider_vi.json (N4)")
    if kept:
        b0 = kept[0].split("|")[0]
        pd = pull_world(ctx, tmp, drop=f"{b0}.xm_test2500.ctl")
        a2 = score_args(pd, ctx, tmp / "r_cider2")
        cv2 = scored(SC.cmd_cider, a2)
        runs = cv2["runs"]["xm_test2500"]
        ok(not any(r.startswith(b0 + "|") for r in runs) and any(not r.startswith(b0 + "|") for r in runs),
           "CC-307 W3: cider scores no arm (and no original) of a partial block, only complete blocks")
        cf2 = tmp / "r_cider2" / "cider_vi.json"
        sc2 = scored(SC.cmd_score, score_args(pd, ctx, tmp / "r_score2", cider=str(cf2), cider_sha=D.sha(cf2.read_bytes())))
        ok(sc2["m"]["m"] == 3 * (len(kept) - 1) and "incomplete" in sc2["blocks"][kept[0]]["status"],
           "a partial block is incomplete, never opened, and leaves the family")


# ---------------------------------------------------------------------------------------------- §4.5 t1table
def st_t1table(tmp: Path) -> None:
    import c_diag_t1table as T1
    PS = D.score_mod()
    PS.load(D.ROOT)
    saved = (dict(T1.T), T1.TMAN, T1.BUILD, D.N_LABEL_IDS)
    t = tmp / "t1"
    (t / "pull" / "out").mkdir(parents=True)
    (t / "build" / "manifest").mkdir(parents=True)
    ids = [f"x{n}" for n in range(12)]
    lists = {"sets": {"xm_dev500": [[i] for i in ids[:4]], "xm_test2500": [[i] for i in ids[4:10]]}}
    demos = {"d0": dcx("con chó", [("obj", "chó", 4, 7)]), "d1": dcx("con mèo", [("obj", "mèo", 4, 7)])}
    M = {"label": PS.CP.LABEL, "set": PS.XM, "queries": [{"id": i, "ranked": ["d0", "d1", "d0", "d1"]} for i in ids],
         "demos": demos}
    mb = json.dumps(M).encode()
    (t / "build" / "manifest" / "xm3600_vi.json").write_bytes(mb)

    vmap = D.XO.resolve_map(D.path("desc"))
    (t / "lists.json").write_text(json.dumps(lists), encoding="utf-8")
    h5 = D.sha(mb)
    st = {}

    def world(match: bool, absent: bool, t5: str = h5):
        """match: both runs' counts agree (else the FALLBACK rule); absent: mèo absent (else every class present)."""
        pv = {}
        for arm in ("PVR-drop", "PVR-keep"):
            pv[arm] = "".join(json.dumps({"set": PS.XM, "arm": arm, "id": i, "demo_ids": ["d0", "d1", "d0", "d1"],
                                          "masks": [[j % 2 == 1] for j in range(4)], "yes": 2,
                                          "no": 2 if (arm == "PVR-keep" or match) else 0, "maybe": 0, "parse_fail": 0,
                                          "cap_hits": 0}) + "\n" for i in ids)
            (t / "pull" / "out" / f"xm3600_vi.{arm}.jsonl").write_text(pv[arm], encoding="utf-8")
        sums = "".join(f"{D.sha(pv[arm].encode())}  out/xm3600_vi.{arm}.jsonl\n" for arm in pv)
        (t / "pull" / "SHA256SUMS_tier1").write_text(sums, encoding="utf-8")
        neg = sorted(vmap["mèo"]["neg"]) if absent else []
        pos = sorted(vmap["chó"]["pos"]) + ([] if absent else sorted(vmap["mèo"]["pos"]))
        (t / "lab.json").write_text(json.dumps({i: {"pos": pos, "neg": neg} for i in ids[:10]}), encoding="utf-8")
        man = f"{t5}  manifest/xm3600_vi.json\n{'1' * 64}  manifest/other.json\n"
        (t / "build" / "MANIFEST.sha256").write_text(man, encoding="utf-8")
        T1.TMAN = D.sha(man.encode())
        T1.T.update({"T1": (str(t / "pull" / "SHA256SUMS_tier1"), D.sha(sums.encode())),
                     "T2": (str(t / "pull/out/xm3600_vi.PVR-drop.jsonl"), D.sha(pv["PVR-drop"].encode())),
                     "T3": (str(t / "pull/out/xm3600_vi.PVR-keep.jsonl"), D.sha(pv["PVR-keep"].encode())),
                     "T4": (str(t / "build" / "MANIFEST.sha256"), T1.TMAN),
                     "T7": (str(t / "lists.json"), D.sha((t / "lists.json").read_bytes()))})
        T1.BUILD, T1.T5_PREFIX = str(t / "build"), h5[:8]
    D.N_LABEL_IDS = 10
    orig_man = PS.manifests
    PS.manifests = lambda *a, **k: (_ for _ in ()).throw(AssertionError("manifests() must not be called (R2-W5 (b))"))
    n = [0]

    def go():
        n[0] += 1
        res = t / f"res{n[0]}"
        res.mkdir()
        return scored(T1.run, argparse.Namespace(labels=str(t / "lab.json"), labels_sha=D.sha((t / "lab.json").read_bytes()),
                                                 res=str(res)))
    try:
        world(match=False, absent=True)
        r = go()
        ok(len(D.GUARD.files) == 9 + len(D.CODE) and not D.GUARD.outs[1:], "§4.5: its own nine inputs (+ code pins)")
        tb = r["table"]
        ok(r["n_images"] == 10 and tb["status"] == "FALLBACK (per-run statistics)", "s1_table FALLBACK (count mismatch)")
        ok(tb["cells"]["SUPPORTED x present"] == 20 and tb["cells"]["REJECTED x absent"] == 20 and
           sum(tb["cells"].values()) == 40, "cells (l.393-403) on the 10 restricted ids only, XM600-like rows skipped")
        world(match=True, absent=True)
        tb = go()["table"]
        ok(tb["status"] == "OK" and tb["kappa"]["point"] == 1.0 and tb["kappa"]["dropped"] == 0, "κ from s1_table")
        world(match=True, absent=False)
        must("> 1 % undefined", go)  # NB-C1: no absent unit -> every κ replicate undefined -> FAULT here
        world(match=True, absent=True, t5="2" * 64)
        must("beginning", go)
        world(match=True, absent=True)
        T1.TMAN = "0" * 64
        must("sha256 differs", go)
        world(match=True, absent=True)
        T1.T5_PREFIX = "deadbeef"
        must("beginning deadbeef", go)
        world(match=True, absent=True)
        T1.T["T2"] = (T1.T["T2"][0], "3" * 64)
        must("differs from T2", go)
    finally:
        PS.manifests = orig_man
        T1.T.clear()
        T1.T.update(saved[0])
        T1.TMAN, T1.BUILD, D.N_LABEL_IDS = saved[1], saved[2], saved[3]
        T1.T5_PREFIX = "f81323d1"


# ---------------------------------------------------------------------------------------------- runner
def main() -> int:
    ap = argparse.ArgumentParser()
    ap.add_argument("part", nargs="?", default="all", choices=("all", "host"))
    a = ap.parse_args()
    no_net()
    D.load()
    D.score_mod()
    t0 = time.time()
    with tempfile.TemporaryDirectory(prefix="c_diag_st_") as td:
        tmp = Path(td)
        st_constants()
        st_backstop()
        st_hook(tmp)
        st_plan_money()
        st_host()
        (tmp / "led").mkdir()
        st_ledger(tmp / "led")
        st_stats()
        st_rules()
        (tmp / "gpu").mkdir()
        st_gpu_paths(tmp / "gpu")
        if a.part == "all":
            import c_diag_score as SC
            SC.cv_mod()
            st_bare()
            st_ladder()
            ctx = st_world(tmp)
            try:
                st_world_faults(ctx, tmp)
                st_score(ctx, tmp)
            finally:
                ctx["world"].close()
            st_t1table(tmp)
    print(f"selftest ok ({a.part}): {N[0]} checks, {time.time() - t0:.0f} s")
    return 0


if __name__ == "__main__":
    sys.exit(main())
