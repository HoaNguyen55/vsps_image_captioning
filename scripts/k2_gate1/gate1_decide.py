#!/usr/bin/env python3
"""K2 Gate 1 decision on UIT-ViIC val 924 (RULE.md §6; CC-148 W5, CC-119 W12). Scorer = K2 Gate 0's (k2_gate0
untruncate / row / rates / p1_frontier / matched_f1, imported). One look: gate1_decide.json.

    python3 gate1_decide.py --selftest                                 CPU, synthetic captions
    python3 gate1_decide.py decide --dir O --bf16 K2/<Gate 0 val decode>   CPU: gate1_decide.json + verdict markdown
    python3 gate1_decide.py notrun --class cost|fault --why TEXT --dir O
    python3 gate1_decide.py check --dir O                               CPU: refuse a decision not written before NOT_AFTER

O holds k2g1_<system>.preds.json for base_s, unedited, gold, det, ref (student path, W7). GO = all of G1-G6 on point
estimates (one seed, CC-119 W12); a frontier clamped LOW (R(K) < R_1) blocks a GO as INCONCLUSIVE (CC-125); clamped
HIGH (R(K) > the uncut base recall) G4 is read at the endpoint, where it equals -G1. Half-widths are reported.
"""
from __future__ import annotations

import argparse
import json
import os
import re
import subprocess
import sys
import time
from pathlib import Path

import numpy as np

HERE = Path(__file__).resolve().parent
sys.path[:0] = [str(HERE), str(HERE.parent / "grl")]
import common as K  # noqa: E402
import k2_gate0 as KG  # noqa: E402
from k2_gate1 import NOT_AFTER  # noqa: E402  the one deadline instant (MT4 amendment 1 A1)

SYSTEMS = ("base_s", "unedited", "gold", "det", "ref")
BF16_SHA = "8bb0192c76c1a52df883d2a03333062f7e4fde0d08813a919a36d179f50e0c51"  # Gate 0 val decode (k2_p2.DECODE_SHA)
GATE0_CEILING = {"CHAIR_i_zero_shot": 9.375, "CHAIR_i_edited": 1.7948}  # gate0_decide.json 0b6da7e0 (bf16)
T = {"chair": -KG.G["sesoi_chair_i"], "recall": -KG.G["margin_recall"], "vs_unedited": -KG.G["sesoi_chair_i"],
     "frontier_gap": KG.G["sesoi_chair_i"], "words": KG.G["stop_c_words"], "lang_max_pct": 2.0}  # CC-148 W5
GATES = {"G1": "dCHAIR_i(K - base_s) <= -3.0", "G2": "dR(K - base_s) >= -2.0",
         "G3": "dCHAIR_i(K - unedited) <= -3.0", "G4": "CHAIR_i(base_s frontier at R(K)) - CHAIR_i(K) >= 3.0",
         "G5": "mean words(K) >= 90% of base_s", "G6": "captions failing the language check (K) <= 2%"}
LABEL = "K2 Gate 1: DEV / NOT A METHOD RESULT (val 924, one seed, licenses the MT4 PREREG only)"
TEXT = {  # RULE §11, written before any Gate 1 output
    "GO": "# K2 Gate 1 GO: licenses the MT4 PREREG commit and the confirmatory seeds only; not a result",
    "NO-GO": "# K2 Gate 1 NO-GO: STOP. No KV look for K2, no rerun, no tuning; MT4 headline falls back to K1 + K6 "
             "(PI-1026u Q4); UPGRADE_PLAN §6 pivot review",
    "INCONCLUSIVE": "# K2 Gate 1 INCONCLUSIVE: the frontier is clamped low (R(K) below the one-clause base recall, "
                    "not an equal-recall comparison, CC-125); no second val look; TO-PI",
    "NOT-RUN": "# K2 Gate 1 NOT RUN; not a negative pilot; TO-PI"}
FAULT_RE = re.compile(r"GATE1_FAULT_\d{8}T\d{6}Z\.md")


# ------------------------------------------------------------------------------------------------ records
def clock() -> float:
    return time.time()


def write(p: Path, text: str) -> None:
    """The only writer of Gate 1 records: tmp, fsync, then rename. gate1_decide.json is renamed only while the clock
    is before NOT_AFTER (CC-162a F5; Codex: no check/write race), so a late or direct call writes no decision."""
    if not (p.name in ("gate1_decide.json", "GATE1_VERDICT.md", "STOP.md") or FAULT_RE.fullmatch(p.name)):
        raise SystemExit(f"REFUSED: Gate 1 does not write {p.name}")
    if (p.parent / "gate1_decide.json").exists() or p.exists():
        raise SystemExit(f"REFUSED: gate1_decide.json or {p.name} exists in {p.parent} (one look)")
    p.parent.mkdir(parents=True, exist_ok=True)
    tmp = p.with_suffix(p.suffix + ".part")
    with tmp.open("w") as f:
        f.write(text)
        f.flush()
        os.fsync(f.fileno())
    if p.name == "gate1_decide.json" and clock() >= NOT_AFTER:
        tmp.unlink()
        raise SystemExit("HELD: past NOT_AFTER, no gate1_decide.json is written (MT4 amendment 1: K1+K6 binds)")
    os.replace(tmp, p)


def records(out: Path, rec: dict) -> None:
    """The markdown first, then gate1_decide.json (the look). NO-GO also writes STOP.md (CC-148 W5). One writer at a
    time (flock on .gate1_decide.lock), and the recorded write time must be before NOT_AFTER (Codex)."""
    import fcntl

    out.mkdir(parents=True, exist_ok=True)
    with (out / ".gate1_decide.lock").open("w") as lk:
        try:
            fcntl.flock(lk, fcntl.LOCK_EX | fcntl.LOCK_NB)
        except BlockingIOError:
            raise SystemExit("REFUSED: another Gate 1 decision writer holds the lock") from None
        if (t := clock()) >= NOT_AFTER:
            raise SystemExit("HELD: past NOT_AFTER, no Gate 1 decision is written (MT4 amendment 1: K1+K6 binds)")
        _records(out, rec | {"written_epoch": round(t, 3), "not_after_epoch": NOT_AFTER})


ANCHOR_REL = "manuscript/prereg/2026-10-28_k2_gate1/gate1_decide.sha256"  # one line: the decision's sha256
ANCHOR_REF = "refs/remotes/q2/main"  # local paper-v10 is pushed to q2 main; this is the fetched copy
Q2_REPO = "HoaNguyen55/vsps_image_captioning_q2"


class Held(SystemExit):
    """Exit 4: nothing can be decided now (the push record is unreachable); rerun later. Never a branch outcome."""

    def __init__(self, msg: str) -> None:
        super().__init__(4)
        self.msg = msg

    def __str__(self) -> str:
        return self.msg


def git(root: Path, *args: str) -> str:
    r = subprocess.run(["git", "-C", str(root), *args], capture_output=True, text=True)
    return r.stdout if r.returncode == 0 else ""


def anchor_commits(sha: str, root: Path, ref: str = ANCHOR_REF) -> list[str]:
    """Commits on `ref` (the fetched q2 main) whose ANCHOR_REL names `sha`. One look: the FIRST commit that ever
    wrote ANCHOR_REL must name exactly this sha, so a second (other) decision anchored later never counts."""
    cs = git(root, "log", "--reverse", "--format=%H", ref, "--", ANCHOR_REL).split()
    if not cs or git(root, "show", f"{cs[0]}:{ANCHOR_REL}").split() != [sha]:
        return []
    return [c for c in cs if git(root, "show", f"{c}:{ANCHOR_REL}").split() == [sha]]


def _iso(t: str) -> float:
    from datetime import datetime

    return datetime.fromisoformat(t.replace("Z", "+00:00")).timestamp()


def gh_pushes() -> list[tuple[str, float]]:
    """(head commit, server receipt time) of every push to q2 main, from GitHub's activity API, or its events API as
    the fallback. Only those two fields leave gh (--jq); no actor, e-mail or token is read or logged. Both
    unreachable -> Held (fail closed)."""
    q = [("repos/%s/activity?ref=refs/heads/main&activity_type=push&per_page=100" % Q2_REPO,
          '.[] | select(.activity_type == "push") | "\\(.after) \\(.timestamp)"'),
         ("repos/%s/events?per_page=100" % Q2_REPO,
          '.[] | select(.type == "PushEvent" and .payload.ref == "refs/heads/main") | "\\(.payload.head) \\(.created_at)"')]
    for path, jq in q:
        r = subprocess.run(["gh", "api", "--paginate", path, "--jq", jq], capture_output=True, text=True, timeout=120)
        if r.returncode == 0:
            return [(a, _iso(b)) for a, b in (x.split() for x in r.stdout.splitlines() if x.strip())]
    raise Held("HELD: the GitHub push record of q2 is unreachable; nothing is accepted or refused now; rerun check")


def push_epoch(commits: list[str], root: Path, pushes: list[tuple[str, float]]) -> float | None:
    """The earliest server receipt time of a push whose head is an anchor commit or a descendant of one (the head
    must be in the local fetched history; an unknown head proves nothing and is skipped)."""
    ts = [t for head, t in pushes for c in commits
          if head == c or subprocess.run(["git", "-C", str(root), "merge-base", "--is-ancestor", c, head],
                                         capture_output=True).returncode == 0]
    return min(ts) if ts else None


def check(out: Path, root: Path = K.ROOT, ref: str = ANCHOR_REF, pushes=gh_pushes, recompute=None) -> dict:
    """What the MT4 branch rule, kv_freeze.py and the scorer read (MT4 amendment 1 A1/A2; Codex rounds 3-4). A
    decision counts only if (1) it records a write time before NOT_AFTER, (2) its sha256 is in ANCHOR_REL in a
    commit on the fetched q2 main, and (3) GitHub's own receipt time of a push carrying that commit is before
    NOT_AFTER. Local commit times are ignored (they can be backdated). A refusal means no decision (Branch K1+K6);
    an unreachable push record is Held (exit 4): rerun, nothing is decided. (4) Re-running the decision on its
    recorded inputs gives the identical result. Runs on the laptop only (gh credentials never go to M1)."""
    p = out / "gate1_decide.json"
    rec = json.loads(p.read_text())
    w = rec.get("written_epoch")
    if w is None or w >= NOT_AFTER:
        raise SystemExit("REFUSED: gate1_decide.json records no write time before NOT_AFTER; Branch K1+K6 binds")
    commits = anchor_commits(K.sha_file(p), root, ref)
    if not commits:
        raise SystemExit("REFUSED: gate1_decide.json is not anchored on the fetched q2 main; Branch K1+K6 binds")
    got = pushes() if callable(pushes) else pushes
    t = push_epoch(commits, root, got)
    if t is None or t >= NOT_AFTER or t < w:
        raise SystemExit("REFUSED: no GitHub push of the anchor commit received before NOT_AFTER; Branch K1+K6 binds")
    (recompute or rerun)(out, rec)
    return {"verdict": rec["verdict"], "written_epoch": w, "push_received_epoch": t, "anchor_commits": commits}


def _records(out: Path, rec: dict) -> None:
    body = json.dumps(rec, indent=1, default=float)
    md = f"{TEXT[rec['verdict']]}\n\n- {LABEL}\n- failed: {rec.get('failed')}\n\n```json\n{body}\n```\n"
    md_path = out / ("STOP.md" if rec["verdict"] in ("NO-GO", "NOT-RUN") else "GATE1_VERDICT.md")
    write(md_path, md)
    try:
        write(out / "gate1_decide.json", body + "\n")
    except SystemExit:
        md_path.unlink()  # CC-162b G1: no verdict file may outlive a refused decision
        raise


def notrun(out: Path, cls: str, why: str) -> dict:
    """cost: final (gate1_decide.json). fault: GATE1_FAULT_<utc>.md only; a logged rerun stays possible."""
    rec = {"verdict": "NOT-RUN", "class": f"{cls} -> TO-PI", "why": why, "label": LABEL}
    if cls == "cost":
        records(out, rec)
    else:
        from datetime import datetime, timezone

        rec["record"] = f"GATE1_FAULT_{datetime.now(timezone.utc):%Y%m%dT%H%M%SZ}.md"
        write(out / rec["record"], f"{TEXT['NOT-RUN']} (fault)\n\n- {why}\n")
    return rec


def outcome(failed: list[str], clamped_low: bool) -> str:
    """Any of G1, G2, G3, G5, G6 failing is NO-GO; else a low clamp is INCONCLUSIVE (STOP-only: it never loosens a
    gate); else G4 decides. A high clamp is not INCONCLUSIVE: K's recall is above every truncation of the base."""
    if [g for g in failed if g != "G4"]:
        return "NO-GO"
    if clamped_low:
        return "INCONCLUSIVE"
    return "NO-GO" if failed else "GO"


# ------------------------------------------------------------------------------------------------ scoring
def score_rows(caps: list[str], golds: list[set], golds_u: list[set]) -> list[dict]:
    """Gate 0's row (matcher v2, negated/hedged mentions are hallucinations) + gold + the W13 noun count."""
    from score_dev import caption_row

    return [KG.row(c, g, gu) | {"gold": g, "noncoco": caption_row(c, g)["noncoco"], "lang_fail": not KG.language_ok(c),
                                "chars": len(re.sub(r"\s", "", c)), "bad_chars": out_of_script_chars(c)}
            for c, g, gu in zip(caps, golds, golds_u)]


def out_of_script_chars(c: str) -> int:
    from clean_supervision import CJK_RE, OUT_OF_SCRIPT_RE

    return sum(1 for ch in c if not ch.isspace() and (CJK_RE.match(ch) or OUT_OF_SCRIPT_RE.match(ch)))


def decide(caps: dict[str, list[str]], golds: list[set], golds_u: list[set], meta: dict) -> dict:
    """caps: untruncated captions per system, in val-924 order (bf16 optional, diagnostic only)."""
    n = len(golds)
    idx = np.random.default_rng(KG.G["boot_seed"]).integers(0, n, (KG.G["boot_b"], n))  # one draw for every system
    rows = {s: score_rows(c, golds, golds_u) for s, c in caps.items()}
    pt = {s: KG.rates(r) for s, r in rows.items()}
    bs = {s: KG.rates(r, idx) for s, r in rows.items()}
    f = lambda x: round(float(x), 4)  # noqa: E731
    hw = lambda x: f(np.diff(np.percentile(x, [2.5, 97.5]))[0] / 2)  # noqa: E731

    def delta(a, b, k):
        return {"point": f(pt[a][k] - pt[b][k]), "half_width": hw(bs[a][k] - bs[b][k])}

    d1, d2, d3 = delta("gold", "base_s", "CHAIR_i"), delta("gold", "base_s", "R"), delta("gold", "unedited", "CHAIR_i")
    fr = KG.p1_frontier(caps["base_s"], rows["gold"], golds, golds_u, idx)  # numbers only; its 6.0 verdict is Gate 0's
    words = {s: f(np.mean([r["words"] for r in rows[s]])) for s in rows}
    lang = {s: f(100 * np.mean([r["lang_fail"] for r in rows[s]])) for s in rows}
    ok = {"G1": d1["point"] <= T["chair"], "G2": d2["point"] >= T["recall"], "G3": d3["point"] <= T["vs_unedited"],
          "G4": fr["gap_ceiling"] >= T["frontier_gap"], "G5": words["gold"] >= T["words"] * words["base_s"],
          "G6": lang["gold"] <= T["lang_max_pct"]}
    failed = [g for g, v in ok.items() if not v]
    pts = fr["frontier_points_R_CHAIR_by_k"]
    low = fr["frontier_clamped"] and fr["R_edited"] <= pts[0][0]
    clamp = {"frontier_clamped_low": bool(low), "frontier_clamped_high": bool(fr["frontier_clamped"] and not low)}
    verdict = outcome(failed, low)
    sums = {s: {k: int(sum(r[k] for r in rows[s])) for k in ("hal", "men", "tp", "g")} for s in rows}
    mk, mb = KG.matched_f1(rows["gold"], rows["base_s"])
    mk2, mr = KG.matched_f1(rows["gold"], rows["ref"])
    drop_bf16 = GATE0_CEILING["CHAIR_i_zero_shot"] - GATE0_CEILING["CHAIR_i_edited"]
    return {"verdict": verdict, "failed": failed, "gates": {g: GATES[g] for g in GATES}, "pass": ok, "label": LABEL,
            "n_images": n, "thresholds": T, "rates": {s: {k: f(v) for k, v in pt[s].items()} for s in pt}, "sums": sums,
            "delta": {"G1_CHAIR_i_K_minus_base_s": d1, "G2_R_K_minus_base_s": d2, "G3_CHAIR_i_K_minus_unedited": d3,
                      "G4_frontier_gap": {"point": fr["gap_ceiling"], "half_width": fr["half_width"],
                                          "ci95": fr["gap_ci95"]}},
            "frontier": clamp | {k: fr[k] for k in ("frontier_points_R_CHAIR_by_k", "k_max", "frontier_clamped",
                                            "CHAIR_i_frontier_at_R_edited", "check_T_truncation_meets_G1",
                                            "check_T_k")},
            "words_mean": words, "language_check_fail_caption_pct": lang,
            "out_of_script_char_pct": {s: f(100 * sum(r["bad_chars"] for r in rows[s])
                                            / max(sum(r["chars"] for r in rows[s]), 1)) for s in rows},
            "noncoco_nouns_per_caption": {s: f(np.mean([r["noncoco"] for r in rows[s]])) for s in rows},
            "secondary_not_gating": {
                "matched_count_F1": {"K_vs_base_s": [f(mk), f(mb)], "K_vs_ref": [f(mk2), f(mr)],
                                     "estimator": "Paper A matched prefix, cited as a tool"},
                "H_P2r_dev": {"R_K_minus_det": delta("gold", "det", "R"),
                              "CHAIR_i_K_minus_det": delta("gold", "det", "CHAIR_i")},
                "ceiling_retention": f((pt["base_s"]["CHAIR_i"] - pt["gold"]["CHAIR_i"]) / drop_bf16),
                "ceiling_retention_note": "numerator NF4 student path, denominator Gate 0 bf16 (9.375 - 1.7948)"},
            **meta}


# ------------------------------------------------------------------------------------------------ M3/M4 command
def load_inputs(out: Path, bf16: str | None):
    """(caps, golds, golds_u, meta) from the five val decodes in `out` (+ the bf16 row), or a fault string. meta
    records every input sha (decode_sha256), so check() can re-run the decision on exactly these inputs."""
    ids = K.ids("val924")
    KG.val_ids_ok(K.pinned("manuscript/prereg/2026-10-21_dev_pools/uitviic_val.tsv"))
    gold = K.gold()
    refs: dict[int, set] = {}
    for x in json.loads((K.UV / "val_data.json").read_text(encoding="utf-8"))["annotations"]:
        refs.setdefault(int(x["image_id"]), set()).update(KG.RW.ordered(x["caption"], "v2")[0])
    files = {s: out / f"k2g1_{s}.preds.json" for s in SYSTEMS}
    if bf16:
        if K.sha_file(Path(bf16)) != BF16_SHA:
            return "the bf16 diagnostic decode differs from 8bb0192c"
        files["base_bf16"] = Path(bf16)
    caps, meta = {}, {"decode_sha256": {}, "cap_hit_pct": {}, "s_per_image": {}}
    for s, p in files.items():
        d = json.loads(p.read_text(encoding="utf-8"))
        if sorted(map(int, d["predictions"])) != ids or d["max_new_tokens"] != 512:
            return f"{p.name} is not a 512-token val-924 decode"
        caps[s] = [KG.untruncate(d["predictions"][str(i)], d["hit_max"][str(i)]) for i in ids]
        meta["decode_sha256"][s] = K.sha_file(p)
        meta["cap_hit_pct"][s] = round(100 * float(np.mean([d["hit_max"][str(i)] for i in ids])), 4)
        meta["s_per_image"][s] = d.get("s_per_image_decode")
        meta.setdefault("adapter_sha256", {})[s] = d.get("adapter_sha256")
    for extra in ("caps.json", "targets.json.counts.json"):
        if (out / extra).is_file():
            meta[extra] = json.loads((out / extra).read_text())
    return caps, [gold[i] for i in ids], [gold[i] | refs.get(i, set()) for i in ids], meta


SAME = ("verdict", "failed", "pass", "delta", "rates", "decode_sha256")  # what a re-run must reproduce


def rerun(out: Path, rec: dict, bf16: str | None = None, loader=load_inputs) -> None:
    """Round 6: re-run the decision on the inputs it records (same shas) and require the identical verdict, gates
    and deltas. A hand-written or hand-edited decision is refused. NOT-RUN records have no inputs to re-run."""
    if rec["verdict"] == "NOT-RUN":
        return
    got = loader(out, bf16)
    if isinstance(got, str):
        raise SystemExit(f"REFUSED: the decision's inputs cannot be re-read ({got}); Branch K1+K6 binds")
    caps, golds, golds_u, meta = got
    if meta["decode_sha256"] != rec.get("decode_sha256"):
        raise SystemExit("REFUSED: the decision's recorded input shas differ from its inputs; Branch K1+K6 binds")
    new = json.loads(json.dumps(decide(caps, golds, golds_u, meta), default=float))
    if any(new.get(k) != rec.get(k) for k in SAME):
        raise SystemExit("REFUSED: re-running the decision on its inputs gives another result; Branch K1+K6 binds")


def cmd_decide(a) -> int:
    out = Path(a.dir)
    if (out / "gate1_decide.json").exists():
        raise SystemExit("REFUSED: gate1_decide.json exists (one look)")
    got = load_inputs(out, a.bf16)
    if isinstance(got, str):
        notrun(out, "fault", got)
        return 3
    rec = decide(*got)
    records(out, rec)
    print(json.dumps({k: rec[k] for k in ("verdict", "failed")}))
    return 0


# ------------------------------------------------------------------------------------------------ selftest
def selftest() -> None:
    import tempfile

    head = ("một người khoác áo sọc tím lấp lánh đang tâng quả bóng bạc lơ lửng giữa bãi cát vàng óng dưới mái "
            "vòm kính cong queo cạnh hàng cờ đuôi nheo phất phơ")  # k2_gate0 selftest string (CC-125 X5: synthetic)
    g, n = {"person", "sports ball"}, 30
    B = "một con chó, " + head + "."  # base: a wrong dog first, then the head clause (person, ball)
    K2 = head + "."

    def run(k, u=B, b=B, gold=g, det=None, ref=None):
        caps = {"base_s": [b] * n, "unedited": [u] * n, "gold": [k] * n, "det": [det or k] * n, "ref": [ref or k] * n}
        return decide(caps, [gold] * n, [gold] * n, {})

    r = run(K2)  # CHAIR_i 33.3 -> 0, R unchanged, beats unedited and the frontier at equal recall
    assert r["verdict"] == "GO" and not r["failed"], r["failed"]
    assert r["delta"]["G1_CHAIR_i_K_minus_base_s"]["point"] == round(-100 / 3, 4) and r["delta"]["G2_R_K_minus_base_s"][
        "point"] == 0.0 and r["delta"]["G4_frontier_gap"]["point"] == round(100 / 3, 4), r["delta"]
    assert run(K2, u=K2)["failed"] == ["G3"]  # no gain over the unedited student
    assert run("một người cầm quả bóng.")["failed"] == ["G5"]  # far below 90% of the base's words
    assert run(head + " 人.")["failed"] == ["G6"]  # every caption fails the language check
    late = head + ", cạnh con chó."  # wrong dog last: truncation to k = 1 matches K at equal recall -> G4 fails
    assert run(K2, b=late, u=late)["failed"] == ["G4"] and run(K2, b=late, u=late)["verdict"] == "NO-GO"
    # K names a gold dog the base never names: R(K) > R_max -> clamped HIGH -> G4 at the endpoint (= -G1) -> GO
    r = run(head + ", cạnh con chó.", b="một con mèo, " + head + ".", u="một con mèo, " + head + ".",
            gold=g | {"dog"})
    assert r["verdict"] == "GO" and r["frontier"]["frontier_clamped_high"] and not r["failed"], r
    assert r["delta"]["G4_frontier_gap"]["point"] == -r["delta"]["G1_CHAIR_i_K_minus_base_s"]["point"]
    assert outcome([], True) == "INCONCLUSIVE" and outcome(["G4"], True) == "INCONCLUSIVE"  # low clamp
    assert outcome(["G1", "G4"], True) == "NO-GO" and outcome(["G4"], False) == "NO-GO" and outcome([], False) == "GO"
    assert out_of_script_chars("ab 人 c") == 1
    with tempfile.TemporaryDirectory() as t:
        out = Path(t) / "o"
        rec = notrun(out, "fault", "synthetic fault")
        assert (out / rec["record"]).is_file() and not (out / "gate1_decide.json").exists()
        records(out, run(K2, u=K2))
        assert json.loads((out / "gate1_decide.json").read_text())["verdict"] == "NO-GO"
        assert (out / "STOP.md").read_text().startswith(TEXT["NO-GO"])
        for f in (lambda: records(out, run(K2)), lambda: notrun(out, "fault", "late")):
            try:
                f()
            except SystemExit as e:
                assert "one look" in str(e), e
            else:
                raise AssertionError("a second Gate 1 look was accepted")
        try:
            write(Path(t) / "x" / "gate0_decide.json", "{}")
        except SystemExit as e:
            assert "does not write" in str(e), e
        else:
            raise AssertionError("Gate 1 wrote a Gate 0 record")
        nr = notrun(Path(t) / "c", "cost", "exit 124")
        assert nr["class"] == "cost -> TO-PI" and (Path(t) / "c/gate1_decide.json").is_file()
        deadline_selftest(Path(t))
        anchor_selftest(Path(t))
        rerun_selftest(Path(t))
    print("gate1_decide selftest ok")


def _refused(f, word: str) -> None:
    try:
        f()
    except SystemExit as e:
        assert word in str(e), e
    else:
        raise AssertionError(f"accepted, expected {word}")


def deadline_selftest(t: Path) -> None:
    """CC-162a F5 + Codex: a late direct call (decide or cost) writes nothing; a write that crosses NOT_AFTER between
    the lock check and the rename leaves no file; a second writer is locked out; check() refuses a late record."""
    import fcntl

    global clock
    real = clock
    rec = {"verdict": "NOT-RUN", "class": "cost -> TO-PI", "why": "x", "label": LABEL}
    try:
        clock = lambda: NOT_AFTER  # noqa: E731
        _refused(lambda: records(t / "late", rec), "past NOT_AFTER")
        _refused(lambda: notrun(t / "late", "cost", "exit 124"), "past NOT_AFTER")
        assert not (t / "late/gate1_decide.json").exists() and not (t / "late/STOP.md").exists()
        ticks = iter([NOT_AFTER - 1, NOT_AFTER])  # the lock check passes, the rename check fails: the race
        clock = lambda: next(ticks)  # noqa: E731
        _refused(lambda: records(t / "race", rec), "past NOT_AFTER")
        assert not (t / "race/gate1_decide.json").exists() and not (t / "race/gate1_decide.json.part").exists()
        assert not (t / "race/STOP.md").exists()  # CC-162b G1: the verdict markdown is removed too
    finally:
        clock = real
    (t / "busy").mkdir()
    with (t / "busy/.gate1_decide.lock").open("w") as lk:
        fcntl.flock(lk, fcntl.LOCK_EX)
        _refused(lambda: records(t / "busy", rec), "holds the lock")
    (t / "forged").mkdir()
    (t / "forged/gate1_decide.json").write_text(json.dumps(rec | {"written_epoch": NOT_AFTER + 5}))
    _refused(lambda: check(t / "forged", t), "no write time before NOT_AFTER")
    (t / "forged/gate1_decide.json").write_text(json.dumps(rec))  # no recorded write time
    _refused(lambda: check(t / "forged", t), "no write time before NOT_AFTER")


def rerun_selftest(t: Path) -> None:
    """Round 6: a decision re-run on its recorded inputs must match; a hand-edited verdict or an input whose sha
    differs from the recorded one is refused."""
    head = ("một người khoác áo sọc tím lấp lánh đang tâng quả bóng bạc lơ lửng giữa bãi cát vàng óng dưới mái "
            "vòm kính cong queo cạnh hàng cờ đuôi nheo phất phơ")
    n, g = 30, {"person", "sports ball"}
    B, K2 = "một con chó, " + head + ".", head + "."
    caps = {"base_s": [B] * n, "unedited": [B] * n, "gold": [K2] * n, "det": [K2] * n, "ref": [K2] * n}
    meta = {"decode_sha256": {s: f"sha-{s}" for s in caps}}
    real = json.loads(json.dumps(decide(caps, [g] * n, [g] * n, meta), default=float))

    def loader(out, bf16):
        return caps, [g] * n, [g] * n, {"decode_sha256": dict(meta["decode_sha256"])}

    rerun(t, real, loader=loader)  # identical
    _refused(lambda: rerun(t, real | {"verdict": "GO" if real["verdict"] != "GO" else "NO-GO"}, loader=loader),
             "another result")
    _refused(lambda: rerun(t, real | {"failed": []} if real["failed"] else real | {"failed": ["G1"]}, loader=loader),
             "another result")
    _refused(lambda: rerun(t, real | {"decode_sha256": {**meta["decode_sha256"], "gold": "x"}}, loader=loader),
             "input shas differ")
    _refused(lambda: rerun(t, real, loader=lambda o, b: "a decode is missing"), "cannot be re-read")
    rerun(t, {"verdict": "NOT-RUN"}, loader=loader)  # a cost stop has no inputs


def anchor_selftest(t: Path) -> None:
    """Codex rounds 3-4, with a local bare remote and a mocked GitHub push record (no network): accepted only when
    GitHub's receipt time of a push carrying the anchor commit is before NOT_AFTER. A backdated commit pushed late, a
    missing push, a forged unanchored decision and an unreachable API are all refused or Held."""
    g = ["-c", "user.name=x", "-c", "user.email=x", "-c", "core.hooksPath=/dev/null", "-c", "commit.gpgsign=false"]
    remote, repo = t / "remote.git", t / "repo"
    subprocess.run(["git", "init", "-q", "--bare", str(remote)], check=True)
    subprocess.run(["git", "init", "-q", "-b", "paper-v10", str(repo)], check=True)
    subprocess.run(["git", "-C", str(repo), "remote", "add", "q2", str(remote)], check=True)
    rec = {"verdict": "GO", "label": LABEL}

    def decision(name: str, w: float) -> Path:
        d = t / name
        d.mkdir()
        (d / "gate1_decide.json").write_text(json.dumps(rec | {"written_epoch": w}))
        return d

    def anchor(d: Path, when: int) -> str:
        (repo / ANCHOR_REL).parent.mkdir(parents=True, exist_ok=True)
        (repo / ANCHOR_REL).write_text(K.sha_file(d / "gate1_decide.json") + "\n")
        env = os.environ | {"GIT_COMMITTER_DATE": f"{when} +0000", "GIT_AUTHOR_DATE": f"{when} +0000"}
        subprocess.run(["git", "-C", str(repo), *g, "add", ANCHOR_REL], check=True)
        subprocess.run(["git", "-C", str(repo), *g, "commit", "-qm", d.name], check=True, env=env)
        subprocess.run(["git", "-C", str(repo), "push", "-q", "q2", "paper-v10:main"], check=True)
        subprocess.run(["git", "-C", str(repo), "fetch", "-q", "q2"], check=True)
        return git(repo, "rev-parse", "HEAD").strip()

    real = decision("real", NOT_AFTER - 7200)
    c1 = anchor(real, NOT_AFTER - 3600)
    later = decision("later", NOT_AFTER - 100)
    c2 = anchor(later, NOT_AFTER - 50)  # a descendant of c1
    assert check(real, repo, recompute=lambda o, r: None, pushes=[(c1, NOT_AFTER - 3000)])["push_received_epoch"] == NOT_AFTER - 3000
    assert check(real, repo, recompute=lambda o, r: None, pushes=[(c2, NOT_AFTER - 10)])["push_received_epoch"] == NOT_AFTER - 10  # descendant
    _refused(lambda: check(real, repo, recompute=lambda o, r: None, pushes=[(c1, NOT_AFTER + 1)]), "no GitHub push")  # backdated, pushed late
    _refused(lambda: check(real, repo, recompute=lambda o, r: None, pushes=[]), "no GitHub push")  # missing push
    _refused(lambda: check(real, repo, recompute=lambda o, r: None, pushes=[("f" * 40, NOT_AFTER - 9)]), "no GitHub push")  # unknown head

    def down():
        raise Held("HELD: the GitHub push record of q2 is unreachable; nothing is accepted or refused now; rerun check")
    try:
        check(real, repo, recompute=lambda o, r: None, pushes=down)
    except Held as e:
        assert e.code == 4 and "unreachable" in str(e)
    else:
        raise AssertionError("an unreachable push record was not Held")
    forged = decision("forged_go", NOT_AFTER - 9000)  # plausible earlier time, never anchored
    _refused(lambda: check(forged, repo, recompute=lambda o, r: None, pushes=[(c1, NOT_AFTER - 3000)]), "not anchored")
    _refused(lambda: check(later, repo, recompute=lambda o, r: None, pushes=[(c2, NOT_AFTER - 10)]), "not anchored")  # a second decision
    assert _iso("2026-10-29T03:20:10Z") == 1793244010.0


def main() -> int:
    ap = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    ap.add_argument("cmd", nargs="?", choices=("decide", "notrun", "check"))
    ap.add_argument("--selftest", action="store_true")
    ap.add_argument("--dir")
    ap.add_argument("--bf16")
    ap.add_argument("--class", dest="cls", choices=("cost", "fault"))
    ap.add_argument("--why")
    a = ap.parse_args()
    if a.selftest:
        selftest()
        return 0
    if a.cmd == "notrun":
        notrun(Path(a.dir), a.cls, a.why)
        return 0
    if a.cmd == "decide":
        return cmd_decide(a)
    if a.cmd == "check":
        print(json.dumps(check(Path(a.dir), recompute=lambda o, r: rerun(o, r, a.bf16))))
        return 0
    ap.error("give --selftest or a command")
    return 2


if __name__ == "__main__":
    sys.exit(main())
