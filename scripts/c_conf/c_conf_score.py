#!/usr/bin/env python3
"""C-CONF statistics (CPU, on the rented host: PI-1111j; the laptop keeps the 444 copy and the hashes only). DRAFT on
synthetic fixtures under CC-438 FP-7: no study data, no host run, no token, no commit before a GO.
Registration draft manuscript/directions/C_CONFIRM_PREREG_DRAFT_2026-11-16_v3.md (final, 18e61111; drafted on b3c4e405) with the CC-450 items
X5 (time check before T0) and J1 N1 (Holm tie order): §7.1 per-image score and the scoring parity gate, §7.2
estimands and Δ_batch, §7.3 interval, §7.4 labels, §7.5 the family F1 and the sentence table, §7.6 the rehearsal rule,
§7.7 the named secondaries, §7.8 sensitivities, §7.11 order of scoring, §7.13 row labels, §8 controls, §10.2 caps and
drop order, G6 freeze. A copy of scripts/c_attr/c_attr_score.py (cca5e327) with C-ATTR's nomination, V4 gates, copy
bound, swap, block 3 and K7 removed; summary, pair, label, draw_keys, draw_variance, df_resample, primary,
df_sensitivity, kit_scorer, freeze_copy, tree_ok, env_record and strip are kept byte for byte (read the change as
scripts/c_conf/C_CONF_SCORE_VS_C_ATTR_SCORE.diff). Labels: rehearsal "TIER 2 / DEV-CONFIRM (C-CONF), OV-CARVE",
test "TIER 3 / TEST (C-CONF), SECOND LOOK AT OV-TEST".

  python -I -B scripts/c_conf/test_c_conf_score.py                                 self-test and mutants (planted data)
  python -I -B scripts/c_conf/c_conf_score.py plan --mode rehearsal|test --d1 F... --out CAP.json   §10.2 cap, drop order,
      [--dry-run --runners R... [--force-ceiling-h H] [--freeze-utc U]]            X5 time check (rc 4 STOP, rc 5 TIME)
  python -I -B scripts/c_conf/c_conf_score.py timecheck --cap CAP.json [--dry-run --freeze-utc U]   X5 at the T0 call
  python -I -B scripts/c_conf/c_conf_score.py parity --preds P --ledger L                           §7.1 parity gate
  python -I -B scripts/c_conf/c_conf_score.py stage rehearsal|test ...                              §7.11, once per set

The host commands need scripts/c_conf/c_conf.py (imported as A on first use; interface in CODE_DRAFT_REPORT). Outputs
hold ids and numbers only; nothing prints a caption. LMCap rows are a re-implementation of the LMCap recipe by this
study, not the authors' code.
"""
from __future__ import annotations

import argparse
import calendar
import hashlib
import importlib.metadata
import json
import re
import shutil
import subprocess
import sys
import time
from pathlib import Path

import numpy as np

ROOT = Path(__file__).resolve().parents[2]
A = None  # scripts/c_conf/c_conf.py, imported by host() for the host commands only; the statistics need numpy only

SESOI, ALPHA = 2.0, 0.025  # §7.4: +2.0; family-wise one-sided alpha
BOOT, BOOT_SEED, REH_SEED = 2000, 0, 1  # §7.3 default_rng(0); §7.6 item 2 default_rng(1)
CARVE_N, TEST_N = 2000, 1941
Z_HOLM3, P_BAR, MARGIN = 2.394, 0.98, 3.65  # §7.6 items 2 and 3: Φ⁻¹(1 − 0.025/3); P_m bar; 2.0 + 1.65
BACKBONES = ("qwen25vl_7b", "internvl3_8b", "aya_vision_8b")
PRIMARY, LMCAP = "qwen25vl_7b", "lmcap"
FIRST_LOOK = ("qwen25vl_7b", "internvl3_8b")  # the two backbones decoded at the first look (§1, §7.2 Δ_batch)
NAME = {"qwen25vl_7b": "Qwen2.5-VL-7B", "internvl3_8b": "InternVL3-8B", "aya_vision_8b": "Aya-Vision-8B",
        "lmcap": "LMCap"}
VLM_COLS = ("zs", "ret", "rand_d0", "rand_d1", "rand_d2", "perm_p1", "perm_p2")  # §2, R = 3, D = 2
LMCAP_COLS = ("lmcap_ri", "lmcap_rand", "lmcap_perm")
#: §7.13 and §7.5-§7.7 fixed strings
LABEL_R = "TIER 2 / DEV-CONFIRM (C-CONF), OV-CARVE"
LABEL_T = "TIER 3 / TEST (C-CONF), SECOND LOOK AT OV-TEST"
CARVE_ROW = "rehearsal on 2,000 OpenViIC training images used as queries, own cluster removed; development"
OV_ROW = "second look at OV-test; C-CONF; batch size 1"
KNOWN = "split of a τ_sel known from the first look (batched decodes)"
FIRST_DEC = ("first decode of this system on the OpenViIC test set; its only earlier test-set decode is the Flickr30K "
             "look of Section 8.6")
SECONDARY = "secondary, no family-wise error control"
SENS = "sensitivity"
LMCAP_WORDS = ("re-implementation of the LMCap recipe by this study; not the authors' code; not a statement about the "
               "published numbers")
NO_LOOK = "the rehearsal did not reach its bar; OV-test was not looked at a second time"
NOT_ENTERED = "not taken to test (rehearsal bar not reached)"
CAP_DROP = "not tested at the second look (dropped under the compute cap of the session)"
NOT_DONE = "not completed at the second look ({})"  # CC-450 J1 N3 proposal; binds only if the registration adopts it
G5_PREFIX = "positive control not DETECTED on this set: "  # CC-450 J1 N2 proposal; idem
SENTENCE = {  # §7.5: H_pair claims that pass -> (sentence, the split may enter)
    1: ("under a second registration and at batch size 1, the pairing component of the retrieval contrast was detected "
        "on the OpenViIC test set for {} (for Qwen2.5-VL-7B and InternVL3-8B, a split of a retrieval contrast already "
        "known from the first look)", 'contributions and abstract, with the words "second look"'),
    2: ("the pairing component was detected for {} and not for Qwen2.5-VL-7B, the primary backbone",
        "Section 6.10 and the limitations only"),
    3: ("the pairing component was detected for {} and not for {}", "Section 6.10 and the limitations only"),
    4: ("FAIL: the split nominated in development was not confirmed on the OpenViIC test set",
        "Section 6.10 and the limitations only")}
S_MARG = {"NEGLIGIBLE": "the part given by any retrieved-type list was smaller than 2.0 points in either direction",
          "UNRESOLVED": "not resolved", "DETECTED": "DETECTED", "REVERSED": "REVERSED"}
S_REP = {"qwen25vl_7b": ("the registered row P1b was reproduced at batch size 1 with three random draws",
                         "was not reproduced"),
         "internvl3_8b": ("the registered secondary at τ = −∞ was reproduced at batch size 1 with three random draws",
                          "was not reproduced")}
S_BB = ("on the OpenViIC test set the retrieval contrast was detected for one backbone outside the Qwen language-model "
        "line (first decode of this system on the OpenViIC test set; its only earlier test-set decode is the Flickr30K "
        "look of Section 8.6)", "was not detected")
S_BATCH = ("decoding one image at a time on another machine and software stack changed the registered contrast by "
           "less than 2.0 points in either direction",
           "the registered contrast differed between the first look (batched, first machine) and this look (one image "
           "at a time, another machine and software stack) by {:+.2f} [{:.2f}, {:.2f}]")
#: §7.2 Δ_batch: the record fields that must be equal between the first look and C-CONF (§6.4a), else NOT RUN
BATCH_RECORD = ("kit_sha256", "jar_sha256", "score_field", "annotation_sha256", "list_sha256")
#: G6 (§10.1) and §10.2
G6_UTC = "2026-12-01T11:00:00Z"  # 2026-12-01 18:00 (UTC+7)
G6_TS = calendar.timegm(time.strptime(G6_UTC, "%Y-%m-%dT%H:%M:%SZ"))
CLOCK = time.time
CAP_CEIL_H, CAP_FACTOR, PULL_SCORE_S = 30.0, 1.5, 24 * 3600
PLAN_RATE = {"qwen25vl_7b": 0.80, "internvl3_8b": 1.40, "aya_vision_8b": 1.60, "lmcap": 1.14}  # §6.1, dry run only
STEP_ORDER = ("qwen25vl_7b", "lmcap", "internvl3_8b", "aya_vision_8b")  # R.1, R.4, R.2, R.3 (T.1, T.4, T.2, T.3)
DROP_ORDER = ("aya_vision_8b", "internvl3_8b")  # LMCap and Qwen2.5-VL-7B are never dropped
RUNS = {m: len(VLM_COLS) for m in BACKBONES} | {LMCAP: len(LMCAP_COLS)}
SET_N = {"rehearsal": 2000, "test": 2001}  # captions per run: the carve; all 2,001 OV-test entries
#: §6.4a pins (hash only on the laptop; read on the host by the scoring stage)
PARITY_PREDS_SHA256 = "f7298a01b94044eb9d416b34cbd9986fd34b350350543bce295ead7677f2829f"
PARITY_LEDGER_SHA256 = "f79ea6a9c59157216fdf1662ce320c35a1befe48a87cfb36a174a7cfef0244f8"
PARITY_TOL = 1e-4
FL_LEDGER_SHA256 = {"ov_test_1941": "50878193f1cfc473786ca86e4cc5eb59f13720faa9d97ea52206dd36c0daa154",
                    "ov_test_2001": "5e04d267a461b093af1b996dd21d8ee9a1b30ac2e5029978eba7b431f40f1b54"}
#: CC-454 B10: sha256 of the first look's record JSON (from record files only, before the token, each named with
#: its sha256 in an OPS line), set before the code freeze; None = S-batch NOT RUN (the registered fallback)
RECORD_OLD_SHA256 = None
TEST_LISTS = {"tsv": ("manuscript/prereg/2026-10-25_c_test/ov_test_files.tsv",
                      "99d4fc49cc8283d1555d37b975cca5a32598ea0ec571d8bef8cf811df2c33695"),
              "primary": ("manuscript/prereg/2026-10-25_c_test/ov_test_primary1941.txt",
                          "6458295ed1df42b854fed3807be3541cc452d6eeb79ee565780b72a777c807e2"),
              "flag12": ("manuscript/directions/integrity_2026-11-10/ids/pin_c_ov_test_ret_union.txt",
                         "8c75134e7c4bb25faef05876c459da1a5b5c90d4cbfdc11a73c362ba4e505bc9"),
              "halves": ("manuscript/prereg/2026-11-02_c_pvr_tier1/c_pvr_lists.json",
                         "edb07fbbea45b69b246ec1e82e23103784b7c777c4e0ef6737e49151d1dc8e18")}
TOKEN_FIELDS = ("rehearsal_decision_sha256", "yes_log_id", "ledger_line_log_id", "backbones")  # §6.4 item 5
SENS_B, SENS_MODEL = 200, "qwen25vl_7b"  # §9: the first 200 rows of the set's shared index matrix (CC-450 J1 N7)
WORK = Path("/root/c_conf_score")
KIT = ROOT / "scripts/kit_b"
DECISION = {"rehearsal": "C_CONF_REHEARSAL_DECISION.json", "test": "C_CONF_TEST_DECISION.json"}


def host():
    """The host commands' module c_conf.py (§11.1), imported once."""
    global A
    if A is None:
        sys.path.insert(0, str(Path(__file__).resolve().parent))
        import c_conf as mod  # noqa: E402
        A = mod
    return A


def sha(p) -> str:
    return hashlib.sha256(Path(p).read_bytes()).hexdigest()


def boot_idx(n: int, seed: int = BOOT_SEED) -> np.ndarray:
    """§7.3: one index matrix per scored set, default_rng(0).integers(0, n, (2000, n))."""
    return np.random.default_rng(seed).integers(0, n, (BOOT, n))


def g6_open() -> None:
    """G6 (§10.1): at and after 2026-12-01 18:00 (UTC+7) every unfinished step is NOT RUN, scoring included."""
    if CLOCK() >= G6_TS:
        raise SystemExit(f"REFUSED: G6 ({G6_UTC} = 2026-12-01 18:00 VN) has passed: every unfinished step is NOT RUN")


# ------------------------------------------------------------------------------------------------ §7.3-7.4
def summary(point: float, bm: np.ndarray) -> dict:
    lo, hi, lo90, hi90 = np.percentile(bm, [2.5, 97.5, 5, 95])
    return {"d": float(point), "lo": float(lo), "hi": float(hi), "lo90": float(lo90), "hi90": float(hi90),
            "p": float((1 + np.sum(bm <= 0)) / (len(bm) + 1)), "_bm": bm}


def pair(a, b, idx: np.ndarray) -> dict:
    """Paired image bootstrap of mean(a - b): the same resampled images for both arms."""
    a, b = np.asarray(a, float), np.asarray(b, float)
    rows = idx  # one index matrix per set, shared by every contrast on that set (§7.3)
    return summary(a.mean() - b.mean(), a[rows].mean(1) - b[rows].mean(1))


def detected(claims: dict[str, tuple[float, float]], alpha: float = ALPHA) -> set[str]:
    """§7.4 DETECTED over one family {name: (point, p)}: Holm step-down at family-wise one-sided alpha, the j-th claim
    against alpha / (m - j + 1), and point >= +2.0; stop at the first failure (strict reading, CC-338 ruling 3). Order
    (CC-450 J1 N1, binding): increasing p; equal p by decreasing θ̂; equal in both by key. A row outside every family
    is a family of m = 1."""
    m, out = len(claims), set()
    for j, (k, (d, p)) in enumerate(sorted(claims.items(), key=lambda kv: (kv[1][1], -kv[1][0], kv[0])), 1):
        if not (d >= SESOI and p <= alpha / (m - j + 1)):
            break
        out.add(k)
    return out


def label(s: dict, is_detected: bool) -> str:
    """Mutually exclusive labels, first match: DETECTED, REVERSED (95% upper < 0), NEGLIGIBLE (90% interval inside
    (-2.0, +2.0)), UNRESOLVED."""
    if is_detected:
        return "DETECTED"
    if s["hi"] < 0:
        return "REVERSED"
    if s["lo90"] > -SESOI and s["hi90"] < SESOI:
        return "NEGLIGIBLE"
    return "UNRESOLVED"


def label1(r: dict) -> str:
    """The §7.4 label of a row outside every family (m = 1)."""
    return label(r, bool(detected({"x": (r["d"], r["p"])})))


def draw_keys(per: dict, m: str, arm: str) -> list[str]:
    """The columns of one arm's draws (rand_d<j>, perm_p<j>, fix_f<j>). The X2 masked columns ('..._m3') that the
    scorer writes beside every run are not draws and never enter a draw mean (found with SC1-SC5)."""
    return sorted(k for k in per if re.fullmatch(rf"{re.escape(m)}\|{arm}\d+", k))


def complete(per: dict, m: str) -> bool:
    """§10.2: no backbone is run in part; a backbone with an incomplete arm gives no row (NOT RUN)."""
    return all(f"{m}|{c}" in per for c in (LMCAP_COLS if m == LMCAP else VLM_COLS))


def reg_mean(per: dict, m: str, arm: str) -> np.ndarray:
    """§7.2: the per-image mean over exactly the registered draws (rand d0-d2) or permutations (perm p1-p2)."""
    cols = [c for c in VLM_COLS if c.startswith(arm + "_")]
    return np.mean([per[f"{m}|{c}"] for c in cols], axis=0)


def flag(pl: dict) -> bool:
    """§8.2 (v1.1 §7.7a): a placebo row is flagged when |θ̂| >= 2.0 and its 95% interval excludes 0."""
    return bool(abs(pl["d"]) >= SESOI and (pl["lo"] > 0 or pl["hi"] < 0))


def set_rows(per: dict, idx: np.ndarray) -> dict[str, dict]:
    """§7.2 and §8 on one scored set, every contrast on the set's one index matrix: per complete backbone τ_any,
    τ_sel, τ_marg, τ_pair and the placebo rows rand d1 - d2 and perm p1 - p2; for a complete LMCap τ_sel
    (lmcap_ri - lmcap_rand, the positive control), τ_pair (ri - perm) and τ_marg (perm - rand)."""
    rows = {}
    for m in BACKBONES:
        if not complete(per, m):
            continue
        zs, ret, rand, perm = per[f"{m}|zs"], per[f"{m}|ret"], reg_mean(per, m, "rand"), reg_mean(per, m, "perm")
        for est, a, b in (("tau_any", rand, zs), ("tau_sel", ret, rand), ("tau_marg", perm, rand),
                          ("tau_pair", ret, perm)):
            rows[f"{m}|{est}"] = {**pair(a, b, idx), "model": m, "estimand": est, "R": 3, "D": 2}
        for est, x, y in (("placebo_d1_d2", "rand_d1", "rand_d2"), ("placebo_p1_p2", "perm_p1", "perm_p2")):
            pl = pair(per[f"{m}|{x}"], per[f"{m}|{y}"], idx)
            rows[f"{m}|{est}"] = {**pl, "model": m, "estimand": f"placebo {x} - {y}", "flag": flag(pl)}
    if complete(per, LMCAP):
        ri, rd, pm = (per[f"{LMCAP}|{c}"] for c in LMCAP_COLS)
        for est, a, b in (("tau_sel", ri, rd), ("tau_pair", ri, pm), ("tau_marg", pm, rd)):
            rows[f"{LMCAP}|{est}"] = {**pair(a, b, idx), "model": LMCAP, "estimand": est, "wording": LMCAP_WORDS}
    return rows


def draw_variance(per: dict, m: str, ret: np.ndarray | None) -> dict | None:
    """§7.7a: mean within-image variance over draws, its share of the image-bootstrap variance of ret - rand mean."""
    keys = draw_keys(per, m, "rand_d")
    if len(keys) < 2 or ret is None:
        return None
    x = np.array([per[k] for k in keys])
    n, r = x.shape[1], x.shape[0]
    s2w = float(x.var(axis=0, ddof=1).mean())
    total = float(np.var(ret - x.mean(0), ddof=1) / n)
    return {"sigma2_w": s2w, "draw_part": s2w / (n * r), "total": total, "share": s2w / (n * r) / total if total else None}


def control(rows: dict) -> str:
    """§8.1: LMCap τ_sel DETECTED with m = 1; a positive control that is not complete counts as NOT DETECTED."""
    r = rows.get(f"{LMCAP}|tau_sel")
    return "DETECTED" if r is not None and detected({"k": (r["d"], r["p"])}) else "NOT DETECTED"


def strip(o):
    return {k: strip(v) for k, v in o.items() if k != "_bm"} if isinstance(o, dict) else o


# ------------------------------------------------------------------------------------------------ ledgers
def columns(rows: list[dict], scored: str) -> tuple[dict, list]:
    """{'<model>|<col>': per-image cider_s} of one scored set; col = zs, ret, rand_d<d>, perm_p<p>, lmcap_ri,
    lmcap_rand, lmcap_perm. Every row on identical ids; one row per column."""
    per, ids0 = {}, None
    for r in rows:
        if r.get("scored_set") != scored:
            continue
        arm = r["arm"]
        col = arm if arm.startswith("lmcap_") else {"rand": f"rand_d{r.get('draw')}", "perm": f"perm_p{r.get('draw')}"}.get(arm, arm)
        key, ids = f"{r['model']}|{col}", r["per_image"]["ids"]
        ids0 = ids0 or ids
        if ids != ids0 or len(set(ids)) != len(ids):
            raise SystemExit(f"{r['run_id']}: image order differs within {scored}")
        if key in per:
            raise SystemExit(f"two ledger rows for {key} on {scored}")
        per[key] = np.asarray(r["per_image"]["cider_s"], float)
    return per, ids0 or []


def read_ledgers(paths) -> list[dict]:
    return [json.loads(x) for p in paths for x in Path(p).read_text(encoding="utf-8").splitlines() if x.strip()]


# ------------------------------------------------------------------------------------------------ §7.6 rehearsal
def replicate_share(diff: np.ndarray, rmat: np.ndarray) -> tuple[float, np.ndarray]:
    """§7.6 item 2: SE = SD(diff, ddof 1) / √1,941; replicate b passes when mean_b >= +2.0 and mean_b / SE >= 2.394."""
    se = float(np.std(diff, ddof=1) / np.sqrt(rmat.shape[1]))
    means = diff[rmat].mean(1)
    ok = (means >= SESOI) & (means / se >= Z_HOLM3)
    return se, ok


def rehearsal_matrix() -> np.ndarray:
    """§7.6 item 2: B = 2,000 resamples of size 1,941 from the 2,000 carve images, default_rng(1), one for all claims."""
    return np.random.default_rng(REH_SEED).integers(0, CARVE_N, (BOOT, TEST_N))


def margin_ok(d: float) -> bool:
    """§7.6 item 3: the carve point of tau_pair >= +3.65."""
    return d >= MARGIN


def rehearsal_decision(per: dict, ids: list) -> dict:
    """§7.6 on OV-carve (2,000): per claim H_pair(m), (1) carve PASS = τ_pair DETECTED with the completed claims as the
    Holm family; (2) P_m >= 0.98 over resamples of 1,941 from 2,000 (default_rng(1), one matrix for all claims);
    (3) the carve point >= +3.65. Entry iff 1, 2 and 3. The look takes place only if H_pair(Qwen2.5-VL-7B) entered and
    the positive control is DETECTED (incomplete = NOT DETECTED); the token is checked at the test stage."""
    if len(ids) != CARVE_N:
        raise SystemExit(f"REFUSED: carve rows over {len(ids)} images, not the full set of {CARVE_N}")
    idx = boot_idx(CARVE_N)
    rows = set_rows(per, idx)
    done = [m for m in BACKBONES if complete(per, m)]
    det = detected({m: (rows[f"{m}|tau_pair"]["d"], rows[f"{m}|tau_pair"]["p"]) for m in done})
    rmat = rehearsal_matrix()
    claims, joint = {}, np.ones(BOOT, bool)
    for m in BACKBONES:
        if m not in done:
            claims[m] = {"status": "NOT RUN", "family": None}
            continue
        r = rows[f"{m}|tau_pair"]
        se, ok = replicate_share(per[f"{m}|ret"] - reg_mean(per, m, "perm"), rmat)
        joint &= ok
        c = {"carve": strip(r), "carve_pass": m in det, "SE": se, "P_m": float(ok.mean()),
             "share_ok": float(ok.mean()) >= P_BAR, "margin_ok": margin_ok(r["d"]), "family": sorted(done)}
        c["status"] = ("TEST FAMILY" if c["carve_pass"] and c["share_ok"] and c["margin_ok"] else
                       "CARVE PASS, NO MARGIN" if c["carve_pass"] else "CARVE FAIL")
        claims[m] = c
    entered = [m for m in BACKBONES if claims[m]["status"] == "TEST FAMILY"]
    pc = control(rows)
    look = PRIMARY in entered and pc == "DETECTED"
    sec = {k: {**strip(r), "row": CARVE_ROW, "rule": "none (development row)"} for k, r in rows.items()
           if not k.endswith("|tau_pair") or k.startswith(LMCAP)}
    return {"label": LABEL_R, "n": CARVE_N, "claims": claims, "entered": entered, "joint_share": float(joint.mean()),
            "positive_control": pc, "look": look, "sentence": None if look else NO_LOOK, "rows_development": sec,
            "variance": {m: draw_variance(per, m, per[f"{m}|ret"]) for m in done}, "row_label": CARVE_ROW}


# ------------------------------------------------------------------------------------------------ §7.5 test
def names(ms) -> str:
    n = [NAME[m] for m in ms]
    return n[0] if len(n) == 1 else ", ".join(n[:-1]) + " and " + n[-1] if n else ""


def tag_row(r: dict, k: str, f1: bool) -> dict:
    """§7.13 labels; every row outside F1 carries the secondary label (binding 13, §7.9)."""
    m, est = r["model"], r.get("estimand", "")
    tags = [OV_ROW]
    if m in FIRST_LOOK and est in ("tau_pair", "tau_marg", "tau_sel"):
        tags.append(KNOWN)
    if m in ("aya_vision_8b", LMCAP):
        tags.append(FIRST_DEC)
    if not f1:
        tags.append(SECONDARY)
    return {**strip(r), "labels": tags, "key": k}


def sentence(tested: list, passes: list, pc: str, untested: dict | None = None) -> dict:
    """§7.5 sentence by count; untested = {backbone: words} for every backbone outside the tested family
    (NOT_ENTERED, CAP_DROP or NOT_DONE), named in the sentence (l.297, l.309). CC-450 J1 N2 and N3 readings,
    adopted at the code read CC-454 before any data."""
    fails = [m for m in tested if m not in passes]
    short = SENTENCE[3][0].split(" and not for")[0]  # "the pairing component was detected for {}"
    if PRIMARY in passes and len(passes) >= 2:
        row, s = 1, SENTENCE[1][0].format(names(passes))
    elif PRIMARY not in passes and len(passes) == 2:
        row = 2
        s = SENTENCE[2][0].format(names(passes)) if PRIMARY in tested else short.format(names(passes))
    elif len(passes) == 1:
        row = 3
        s = SENTENCE[3][0].format(names(passes), names(fails)) if fails else short.format(names(passes))
    else:
        row, s = 4, SENTENCE[4][0]
    if untested:
        s += "; " + "; ".join(f"{NAME[m]}: {w}" for m, w in sorted(untested.items()))
    enter = SENTENCE[row][1]
    if pc != "DETECTED":
        s, enter = G5_PREFIX + s, "Section 6.10 and the limitations only"
    return {"row": row, "sentence": s, "the split may enter": enter}


def test_decision(sets: dict, token: dict, dropped: list, reasons: dict | None = None, batch: dict | None = None) -> dict:
    """§7.5, §7.7, §7.8, §7.11 on OV-test. sets: {scored set: (per, ids)}; the primary is 'ov_test_1941'. token: the
    four fields of §6.4 item 5; dropped: backbones dropped under the cap of §10.2 (CAP.json); reasons: {backbone:
    reason} for any other incomplete backbone; batch: {backbone: Δ_batch row or NOT RUN}. Order of §7.11: (2) the
    positive control and the placebo rows, (3) F1 on the 1,941, (4) the secondaries, (5) the sensitivities."""
    per, ids = sets["ov_test_1941"]
    if len(ids) != TEST_N:
        raise SystemExit(f"REFUSED: primary rows over {len(ids)} images, not {TEST_N}")
    if sorted(token) != sorted(TOKEN_FIELDS) or PRIMARY not in token["backbones"] \
            or not set(token["backbones"]) <= set(BACKBONES):
        raise SystemExit("REFUSED: not a valid four-field token naming Qwen2.5-VL-7B")
    rows = set_rows(per, boot_idx(TEST_N))
    out = {"label": LABEL_T, "n": TEST_N, "token": token}
    pc = control(rows)  # (2)
    out["positive_control"] = {"verdict": pc, "row": tag_row(rows[f"{LMCAP}|tau_sel"], f"{LMCAP}|tau_sel", False)
                               if f"{LMCAP}|tau_sel" in rows else "NOT RUN (counts as NOT DETECTED)"}
    out["placebo"] = {k: tag_row(r, k, False) for k, r in rows.items() if "placebo" in k}
    entered = [m for m in BACKBONES if m in token["backbones"]]  # (3)
    tested = [m for m in entered if complete(per, m)]
    det = detected({m: (rows[f"{m}|tau_pair"]["d"], rows[f"{m}|tau_pair"]["p"]) for m in tested})
    f1 = {}
    for m in BACKBONES:
        if m not in entered:
            f1[m] = {"verdict": "NOT IN FAMILY", "words": NOT_ENTERED}
        elif m not in tested:
            f1[m] = {"verdict": "NOT RUN", "words": CAP_DROP if m in dropped else
                     NOT_DONE.format((reasons or {}).get(m, "arms incomplete"))}
        else:
            r = rows[f"{m}|tau_pair"]
            f1[m] = {"verdict": "PASS" if m in det else "FAIL", "label": label(r, m in det),
                     "row": tag_row(r, f"{m}|tau_pair", True), "holm_m": len(tested)}
    out["F1"] = {"claims": f1, "family": tested, **sentence(tested, [m for m in tested if m in det], pc,
                                                            {m: f1[m]["words"] for m in BACKBONES if m not in tested})}
    sec = {}  # (4)
    for m in tested:
        sm = rows[f"{m}|tau_marg"]
        sec[f"S-marg({m})"] = {**tag_row(sm, f"{m}|tau_marg", False), "label": label1(sm), "reading": S_MARG[label1(sm)]}
        sel = rows[f"{m}|tau_sel"]
        lab = label1(sel)
        if m in S_REP:
            sec[f"S-rep({m})"] = {**tag_row(sel, f"{m}|tau_sel", False), "label": lab,
                                  "reading": S_REP[m][0 if lab == "DETECTED" else 1]}
        else:
            sec["S-bb"] = {**tag_row(sel, f"{m}|tau_sel", False), "label": lab, "abstract": "never",
                           "reading": S_BB[0 if lab == "DETECTED" else 1]}
        sec[f"tau_any({m})"] = {**tag_row(rows[f"{m}|tau_any"], f"{m}|tau_any", False), "label": label1(rows[f"{m}|tau_any"])}
        if m in FIRST_LOOK:
            sec[f"S-batch({m})"] = (batch or {}).get(m, "NOT RUN: no Δ_batch input")
    for k in (f"{LMCAP}|tau_pair", f"{LMCAP}|tau_marg"):
        if k in rows:
            sec[k] = {**tag_row(rows[k], k, False), "label": label1(rows[k])}
    out["secondaries"] = sec
    out["beside_sentence"] = {"S-marg NEGLIGIBLE": sum(sec[f"S-marg({m})"]["label"] == "NEGLIGIBLE" for m in tested),
                              "tau_sel": {m: {k: rows[f"{m}|tau_sel"][k] for k in ("d", "lo", "hi")} for m in tested},
                              "label": SECONDARY}
    if pc != "DETECTED":  # §7.12: rows printed without interpretation
        out["interpretation"] = "printed without interpretation (positive control not DETECTED on OV-test)"
    out["sensitivities"] = {}  # (5) each scored set on its own index matrix; decides nothing
    for name in ("ov_test_2001", "ov_test_1929", "ov_test_confirm"):
        if name not in sets:
            out["sensitivities"][name] = "NOT RUN"
            continue
        sp, sids = sets[name]
        sr = set_rows(sp, boot_idx(len(sids)))
        sd = detected({m: (sr[f"{m}|tau_pair"]["d"], sr[f"{m}|tau_pair"]["p"]) for m in tested if f"{m}|tau_pair" in sr})
        keep = [f"{m}|tau_pair" for m in tested] + ([] if name == "ov_test_confirm" else
                                                     [f"{m}|{e}" for m in tested for e in ("tau_marg", "tau_sel", "tau_any")])
        out["sensitivities"][name] = {"n": len(sids), "label": SENS, "rows": {
            k: {**tag_row(sr[k], k, False),
                "label": label(sr[k], k.split("|")[0] in sd) if k.endswith("|tau_pair") else label1(sr[k])}
            for k in keep if k in sr}}
    out["variance"] = {m: draw_variance(per, m, per[f"{m}|ret"]) for m in tested}
    return out


def batch_delta(per: dict, ids: list, old_rows: list[dict], rec_new: dict, rec_old: dict, m: str,
                idx: np.ndarray) -> dict:
    """§7.2 Δ_batch(m) = mean_i {[ret - rand d0] at batch size 1 - [ret - rand d0] in the first look's ledger}, paired by
    image id on the same scored set. NOT RUN when a record field of §6.4a differs or is missing (scorer, document
    frequencies, references, list), or when the first look's ledger lacks exactly one τ = −∞ ret or rand d0 row of m
    (CC-438 N7). Reads the score ledger only, never a prediction file."""
    off = [k for k in BATCH_RECORD if rec_new.get(k) is None or rec_new.get(k) != rec_old.get(k)]
    if off:
        return {"status": f"NOT RUN: record fields differ or missing: {off}"}
    old = {}
    for arm in ("ret", "rand"):
        hit = [r for r in old_rows if r.get("model") == m and r.get("arm") == arm and r.get("tau") == "-inf"
               and r.get("variant") is None and (arm == "ret" or (r.get("draw") or 0) == 0)]
        if len(hit) != 1:
            return {"status": f"NOT RUN: {len(hit)} first-look τ = −∞ {arm} rows of {m}"}
        old[arm] = dict(zip(hit[0]["per_image"]["ids"], hit[0]["per_image"]["cider_s"]))
    if set(old["ret"]) != set(ids) or set(old["rand"]) != set(ids):
        return {"status": "NOT RUN: the first-look ledger is not on the ids of this scored set"}
    was = np.array([old["ret"][i] - old["rand"][i] for i in ids], float)
    r = pair(per[f"{m}|ret"] - per[f"{m}|rand_d0"], was, idx)
    lab = label1(r)
    words = S_BATCH[0] if lab == "NEGLIGIBLE" else S_BATCH[1].format(r["d"], r["lo"], r["hi"])
    return {**tag_row({**r, "model": m, "estimand": "delta_batch"}, f"{m}|delta_batch", False), "label": lab,
            "reading": words}


# ------------------------------------------------------------------------------------------------ §10.2 cap, X5
def plan(mode: str, rates: dict, now: float, freeze_ts: float = G6_TS, ceil_h: float = CAP_CEIL_H) -> dict:
    """§10.2: P = Σ_b [N_b r_b + n_runs_b L_b] / 3600 over the runners kept (rates = {runner: (L_b, r_b)} of the D1-PASS
    runners); hard cap = min(30, 1.5 P). Rehearsal: 1.5 P > 30 is a STOP before the first step. Test: the drop order
    (Aya-Vision-8B, then InternVL3-8B; never LMCap or Qwen2.5-VL-7B) is applied before T0; if it still does not fit,
    STOP before T0. X5: T0 needs freeze - now >= cap + 24 h."""
    if PRIMARY not in rates:
        return {"stop": "Qwen2.5-VL-7B has no D1 PASS: the study stops (§9)", "rc": 4}
    keep = [r for r in STEP_ORDER if r in rates]
    dropped = []

    def p_of(rs):
        return sum(SET_N[mode] * RUNS[r] * rates[r][1] + RUNS[r] * rates[r][0] for r in rs) / 3600

    while CAP_FACTOR * p_of(keep) > ceil_h and mode == "test":
        nxt = [r for r in DROP_ORDER if r in keep]
        if not nxt:
            break
        keep.remove(nxt[0])
        dropped.append(nxt[0])
    p = p_of(keep)
    cap = min(ceil_h, CAP_FACTOR * p)
    res = {"mode": mode, "P_h": p, "cap_h": cap, "cap_s": int(cap * 3600), "runners": keep, "dropped": dropped,
           "not_d1": [r for r in STEP_ORDER if r not in rates], "rc": 0, "stop": None}
    if CAP_FACTOR * p > ceil_h:
        res |= {"rc": 4, "stop": "1.5 P exceeds the ceiling: back to the judge" + ("" if mode == "rehearsal" else
                                                                                 " (before T0; no look spent)")}
    elif mode == "test":
        res["time"] = timecheck(res["cap_s"], now, freeze_ts)
        if not res["time"]["ok"]:
            res |= {"rc": 5, "stop": res["time"]["words"]}
    return res


def timecheck(cap_s: int, now: float, freeze_ts: float = G6_TS) -> dict:
    """X5 (CC-450): T0 waits until the time left to G6 is at least the hard cap plus 24 h for the pull, the hash
    check and the one scoring call; otherwise T0 does not start, no look is spent, back to the judge."""
    left = freeze_ts - now
    ok = left >= cap_s + PULL_SCORE_S
    return {"left_s": int(left), "need_s": cap_s + PULL_SCORE_S, "ok": bool(ok),
            "words": "time check passed" if ok else "TIME CHECK FAIL: T0 does not start; no look spent; back to the judge"}


def test_knobs(a) -> float:
    """--force-ceiling-h and --freeze-utc exist for the dry run only (refused otherwise)."""
    if (getattr(a, "force_ceiling_h", None) is not None or a.freeze_utc != G6_UTC) and not a.dry_run:
        raise SystemExit("REFUSED: --force-ceiling-h / --freeze-utc are dry-run knobs")
    return calendar.timegm(time.strptime(a.freeze_utc, "%Y-%m-%dT%H:%M:%SZ"))


def cmd_plan(a) -> None:
    """After D1: (L_b, r_b) from each D1-PASS runner's forward D1 file (timing: load_s, decode_s, n); --dry-run: the
    §6.1 planning rates, no load term, runners from --runners."""
    freeze = test_knobs(a)
    if a.dry_run:
        rates = {r: (0.0, PLAN_RATE[r]) for r in a.runners}
    else:
        rates = {}
        for p in a.d1:
            r = json.loads(Path(p).read_text(encoding="utf-8"))
            rates[r["model"]] = (r["timing"]["load_s"], r["timing"]["decode_s"] / r["timing"]["n"])
    res = plan(a.mode, rates, CLOCK(), freeze, a.force_ceiling_h or CAP_CEIL_H) | {
        "rates_L_r": rates, "dry_run": a.dry_run, "freeze_utc": a.freeze_utc, "utc": time.strftime("%Y-%m-%dT%H:%M:%SZ", time.gmtime())}
    Path(a.out).write_text(json.dumps(res, indent=1) + "\n", encoding="utf-8")
    print(f"PLAN {a.mode}: P {res.get('P_h', 0):.2f} GPU-h, cap {res.get('cap_h', 0):.2f} GPU-h, runners "
          f"{' '.join(res.get('runners', []))}, dropped {' '.join(res.get('dropped', [])) or 'none'}"
          f"{'; ' + res['time']['words'] if 'time' in res else ''}{'; STOP ' + res['stop'] if res['stop'] else ''}")
    sys.exit(res["rc"])


def cmd_timecheck(a) -> None:
    freeze = test_knobs(a)
    t = timecheck(json.loads(Path(a.cap).read_text(encoding="utf-8"))["cap_s"], CLOCK(), freeze)
    print(f"{t['words']}: left {t['left_s']} s, need {t['need_s']} s")
    sys.exit(0 if t["ok"] else 5)


# ------------------------------------------------------------------------------------------------ §7.1 parity
def parity_check(preds: dict, ledger_rows: list[dict], score, refs: dict) -> int:
    """§7.1 scoring parity gate: the stored batch-size-1 Qwen2.5-VL-7B ret run on OV-dev-B, re-scored, equals its
    per-image stripped CIDEr-D in the attribution ledger within 1e-4 (one τ = −∞ row of that run id, same ids)."""
    want = [r for r in ledger_rows if r.get("run_id") == preds["run_id"] and r.get("tau") == "-inf"
            and r.get("variant") is None]
    ids = sorted(preds["predictions"])
    if len(want) != 1 or want[0]["per_image"]["ids"] != ids:
        raise SystemExit("SCORING PARITY FAIL (§7.1): the ledger row of the parity run is missing or on other ids")
    got = np.asarray(score({i: preds["predictions"][i] for i in ids}, refs), float)
    diff = float(np.abs(got - np.asarray(want[0]["per_image"]["cider_s"], float)).max())
    if diff > PARITY_TOL:
        raise SystemExit(f"SCORING PARITY FAIL (§7.1): max difference {diff:.2e} > {PARITY_TOL}")
    return len(ids)


def kit_scorer(kit_b: Path):
    """Stripped CIDEr-D through kit B (score2.kit2: RDRSegmenter, lower-cased), df over the given references.
    score(capt, refs, segmented=True) takes captions already segmented (unit ii); score.segment(texts) -> {text: seg}."""
    import score2 as S2s

    E4, PA, _ptb = S2s.kit2(kit_b)
    seg: dict[str, str] = {}

    def segment(texts) -> dict:
        miss = sorted(set(texts) - seg.keys())
        if miss:
            seg.update(zip(miss, (t.lower() for t in E4.rdr(miss))))
        return seg

    def score(capt: dict, refs: dict, segmented: bool = False) -> np.ndarray:
        ids = sorted(capt)
        sg = segment([x for i in ids for x in refs[i]] + ([] if segmented else [capt[i] for i in ids]))
        cider = E4.Cider({i: [sg[x] for x in refs[i]] for i in ids})
        return np.asarray(cider.per_image({i: " ".join(PA.strip_trailing_punct_tokens(
            (capt[i] if segmented else sg[capt[i]]).split())) for i in ids}), float)
    score.segment = segment
    return score


def parity_gate(preds_path: Path, ledger_path: Path) -> dict:
    if sha(preds_path) != PARITY_PREDS_SHA256 or sha(ledger_path) != PARITY_LEDGER_SHA256:
        raise SystemExit("REFUSED: the parity inputs are not the pinned files of §6.4a (f7298a01, f79ea6a9)")
    A_ = host()
    n = parity_check(json.loads(Path(preds_path).read_text(encoding="utf-8")), read_ledgers([ledger_path]),
                     kit_scorer(KIT), A_.score_refs("ov_dev_b", A_.C.load_lists(A_.CL)))
    return {"preds_sha256": PARITY_PREDS_SHA256, "ledger_sha256": PARITY_LEDGER_SHA256, "n": n, "result": "ok"}


def cmd_parity(a) -> None:
    print(f"scoring parity gate ok: {parity_gate(a.preds, a.ledger)['n']} items")


# ------------------------------------------------------------------------------------------------ §9 sensitivity
def df_resample(cider_cls, rseg: dict, hyps: dict, ids: list[str], rows: np.ndarray) -> dict[str, np.ndarray]:
    """Per arm, the per-position stripped CIDEr-D of one bootstrap resample, document frequencies recomputed over the
    resampled images' references (an image drawn twice counts twice)."""
    u = sorted({ids[j] for j in rows})
    pos = {i: k for k, i in enumerate(u)}
    cid = cider_cls({i: rseg[i] for i in u}, df_refs=[rseg[ids[j]] for j in rows])
    at = [pos[ids[j]] for j in rows]
    return {arm: np.asarray(cid.per_image({i: h[i] for i in u}))[at] for arm, h in hyps.items()}


def primary(sc: dict) -> dict:
    """tau_pair and tau_marg per image or position (draw means as §7.2) from {ret, rand_d<j>, perm_p<j>: scores}."""
    perm = np.mean([sc[k] for k in sorted(sc) if k.startswith("perm_p")], 0)
    rand = np.mean([sc[k] for k in sorted(sc) if k.startswith("rand_d")], 0)
    return {"tau_pair": sc["ret"] - perm, "tau_marg": perm - rand}


def df_sensitivity(cider_cls, rseg: dict, hyps: dict, ids: list[str], idx: np.ndarray) -> tuple[dict, dict]:
    """§9: the primary contrasts with document frequencies recomputed inside the first SENS_B resamples of the set's
    shared index matrix, beside the fixed-df interval over the same resamples. Returns (rows, full-df scores)."""
    full = cider_cls({i: rseg[i] for i in ids})
    sc = {k: np.asarray(full.per_image(h)) for k, h in hyps.items()}
    base, sub = primary(sc), idx[:SENS_B]
    redf = [primary(df_resample(cider_cls, rseg, hyps, ids, rows)) for rows in sub]
    out = {}
    for e, v in base.items():
        rs, fx = np.array([c[e].mean() for c in redf]), v[sub].mean(1)
        (lo, hi), (flo, fhi) = np.percentile(rs, [2.5, 97.5]), np.percentile(fx, [2.5, 97.5])
        out[e] = {"d": float(v.mean()), "lo_df_resampled": float(lo), "hi_df_resampled": float(hi),
                  "lo_df_fixed": float(flo), "hi_df_fixed": float(fhi), "B": SENS_B}
    return out, sc


def dfsens(runs: list[dict], led: list[dict], refs: dict, E4, PA) -> dict:
    """§9 row on the 1,941 for τ_pair(Qwen2.5-VL-7B): its full-df per-image scores must equal the ledger's (1e-4)."""
    by = {{"ret": "ret", "rand": f"rand_d{r['spec']['draw']}", "perm": f"perm_p{r['spec']['draw']}"}.get(r["spec"]["arm"]): r
          for r in runs if r["spec"]["arm"] in ("ret", "rand", "perm")}
    if not {"ret", "rand_d0", "rand_d1", "rand_d2", "perm_p1", "perm_p2"} <= set(by):
        return {"status": f"NOT RUN: {SENS_MODEL} arms incomplete on the 1,941"}
    ids = sorted(refs)
    texts = sorted({by[k]["predictions"][i] for k in by for i in ids} | {x for i in ids for x in refs[i]})
    seg = dict(zip(texts, (t.lower() for t in E4.rdr(texts))))
    rseg = {i: [seg[x] for x in refs[i]] for i in ids}
    hyps = {k: {i: " ".join(PA.strip_trailing_punct_tokens(seg[r["predictions"][i]].split())) for i in ids}
            for k, r in by.items()}
    rows, sc = df_sensitivity(E4.Cider, rseg, hyps, ids, boot_idx(len(ids)))
    for k, r in by.items():
        want = [x for x in led if x.get("run_id") == r["run_id"] and x.get("scored_set") == "ov_test_1941"]
        if len(want) != 1 or want[0]["per_image"]["ids"] != ids \
                or np.abs(sc[k] - np.array(want[0]["per_image"]["cider_s"])).max() > PARITY_TOL:
            return {"status": f"NOT RUN: SENSITIVITY PARITY FAIL: {r['run_id']}: the full-df scores differ from the ledger"}
    return {"status": "computed", "rows": {e: {**r, "label": f"{SENS}; {SECONDARY}"} for e, r in rows.items()}}


# ------------------------------------------------------------------------------------------------ host stages
def freeze_copy(src: Path, dst: Path) -> None:
    """The host's read-only copy of an output tree (files 0444, folders 0555)."""
    shutil.copytree(src, dst, symlinks=False)
    for p in sorted(dst.rglob("*"), key=lambda q: -len(q.parts)):
        p.chmod(0o555 if p.is_dir() else 0o444)
    dst.chmod(0o555)


def tree_ok(d: Path, sums_sha: str) -> int:
    """S1: the copy's SHA256SUMS is the file the laptop verified (its sha256 from the LOG); every listed file hashes as
    listed except logs/job.log (appended after the sums, CC-346 R7); out/, logs/ and parity/ hold no unlisted file."""
    sums = d / "SHA256SUMS"
    if not sums.is_file() or A.sha(sums) != sums_sha:
        raise SystemExit(f"REFUSED: {sums} is not the SHA256SUMS whose sha256 was logged")
    listed = {n: h for h, n in (ln.split(maxsplit=1) for ln in sums.read_text(encoding="utf-8").splitlines() if ln.strip())}
    have = {str(p.relative_to(d)) for sub in ("out", "logs", "parity") if (d / sub).is_dir()
            for p in (d / sub).rglob("*") if p.is_file() and ".partial" not in p.name}
    if have != set(listed):
        raise SystemExit(f"REFUSED: {d}: {len(have - set(listed))} unlisted and {len(set(listed) - have)} missing files")
    bad = [n for n, h in listed.items() if n != "logs/job.log" and A.sha(d / n) != h]
    if bad:
        raise SystemExit(f"REFUSED: {d}: {len(bad)} files differ from SHA256SUMS, e.g. {bad[:3]}")
    return len(listed)


def env_record() -> dict:
    """S1: the scoring environment, written at verify and required unchanged at every later stage: kit B, the pinned
    VnCoreNLP-1.2 jar (score.JAR_SHA256) and its word-segmenter models, Java, Python and its packages."""
    import score as S

    vnc = A.lb.DATA / "vncorenlp"
    jar = vnc / "VnCoreNLP-1.2.jar"
    if not jar.is_file() or A.sha(jar) != S.JAR_SHA256:
        raise SystemExit(f"REFUSED: {jar} is not the pinned VnCoreNLP-1.2 jar ({S.JAR_SHA256[:8]})")
    pkgs = "\n".join(sorted(f"{d.metadata['Name']}=={d.version}" for d in importlib.metadata.distributions()))
    java = subprocess.run(["java", "-version"], capture_output=True, text=True, check=True).stderr.strip()
    return {"python": sys.version.split()[0], "packages_sha256": hashlib.sha256(pkgs.encode()).hexdigest(), "java": java,
            "jar_sha256": S.JAR_SHA256, "kit_b": {p.name: A.sha(p) for p in sorted(KIT.glob("*.py"))},
            "vncorenlp_models": {str(p.relative_to(vnc)): A.sha(p) for p in sorted((vnc / "models").rglob("*")) if p.is_file()}}


def once(out: Path) -> None:
    """§7.11: the scorer runs once per session; a second scoring call for a set with an existing decision file is
    refused."""
    if out.exists():
        raise SystemExit(f"REFUSED: {out.name} exists; the scorer runs once per session (§7.11)")


def token_ok(path: Path, rehearsal: Path) -> dict:
    """§6.4 item 5: four fields; the decision sha256 is the sha256 of the rehearsal decision file; the backbones are
    the ones that entered; the rehearsal licensed the look."""
    t = json.loads(Path(path).read_text(encoding="utf-8"))
    dec = json.loads(Path(rehearsal).read_text(encoding="utf-8"))
    if sorted(t) != sorted(TOKEN_FIELDS) or t["rehearsal_decision_sha256"] != sha(rehearsal) \
            or sorted(t["backbones"]) != sorted(dec["entered"]) or not dec["look"] or not t["yes_log_id"] \
            or not t["ledger_line_log_id"]:
        raise SystemExit("REFUSED: the token does not verify against the rehearsal decision (§6.4 item 5)")
    return t


def write_once(out: Path, res: dict) -> str:
    out.parent.mkdir(parents=True, exist_ok=True)
    with open(out, "x", encoding="utf-8") as f:
        f.write(json.dumps(res, indent=1, ensure_ascii=False) + "\n")
    return sha(out)


def score_runs(ds: str, scored: str, runs: list[Path], led: Path, token: Path | None,
               decision: Path | None = None) -> list[dict]:
    """One kit-B scoring call of c_conf.py into one ledger (rows carry scored_set); ids only in the ledger. The
    decoder admits the token against --rehearsal, the file token_ok checked (not a file looked up beside the token)."""
    host().cmd_score(argparse.Namespace(set=ds, scored_set=scored, runs=runs, ledger=led, kit_b=KIT, token=token,
                                        decision=decision))
    return read_ledgers([led])


def runs_in(tree: Path) -> list[Path]:
    """The scoreable runs of a verified tree (never a D1, dry-run or smoke file)."""
    skip = ("-rev50.preds.json", "-fwd50.preds.json", "-smoke.preds.json")
    return [p for p in sorted((tree / "out").glob("*.preds.json")) if not p.name.endswith(skip)]


def st_rehearsal(a, w: Path, rec: dict) -> dict:
    """§7.11 rehearsal: (1) parity gate; (2) all carve runs scored in one call; (3) the decision file."""
    if sha(a.carve) != a.carve_sha:
        raise SystemExit("REFUSED: the carve list is not the file whose sha256 was logged at block 0")
    carve = sorted(json.loads(Path(a.carve).read_text(encoding="utf-8"))["ids"])
    rec["parity_7_1"] = parity_gate(a.parity_preds, a.parity_ledger)
    led = score_runs("ov_carve", "ov_carve", runs_in(w / "in"), w / "led/ov_carve.jsonl", None)
    per, ids = columns(led, "ov_carve")
    if sorted(ids) != carve:
        raise SystemExit("REFUSED: the carve ledger is not on the 2,000 ids of the logged carve list")
    return rehearsal_decision(per, ids)


def scored_sets(root: Path) -> dict[str, list[str] | str]:
    """§5.2-§5.3 scored sets by their pinned id lists (the host, after the token; TSV rows name<TAB>sha256, no header,
    make_ov_test_manifest.py l.87): the 1,941; the 2,001; the 1,929 if
    the list of 12 has its sha256 of record (else NOT RUN); the primary images in the C-PVR confirm half."""
    for k, (p, h) in TEST_LISTS.items():
        if k != "flag12" and sha(root / p) != h:
            raise SystemExit(f"REFUSED: {p} is not the pinned list ({h[:8]})")
    tsv = [ln.split("\t")[0] for ln in (root / TEST_LISTS["tsv"][0]).read_text(encoding="utf-8").splitlines() if ln.strip()]
    prim = [ln.strip() for ln in (root / TEST_LISTS["primary"][0]).read_text(encoding="utf-8").splitlines() if ln.strip()]
    out = {"ov_test_1941": prim, "ov_test_2001": tsv}
    f12 = root / TEST_LISTS["flag12"][0]
    if f12.is_file() and sha(f12) == TEST_LISTS["flag12"][1]:
        drop = {ln.strip() for ln in f12.read_text(encoding="utf-8").splitlines() if ln.strip()}
        out["ov_test_1929"] = [i for i in prim if i not in drop]
    else:
        out["ov_test_1929"] = "NOT RUN: the list of 12 has no sha256 of record (§5.3)"
    half = set(json.loads((root / TEST_LISTS["halves"][0]).read_text(encoding="utf-8"))["halves"]["openviic_test"])
    out["ov_test_confirm"] = [i for i in prim if i in half]
    return out


def st_test(a, w: Path, rec: dict) -> dict:
    """§7.11 test: (1) parity gate (repeated); every scored set in one session; then test_decision in the order (2)-(5),
    S-batch from the first look's score ledgers (pinned) and the §9 row."""
    token = token_ok(a.token, a.rehearsal)
    rec["parity_7_1"] = parity_gate(a.parity_preds, a.parity_ledger)
    cap = json.loads(Path(a.cap).read_text(encoding="utf-8"))
    ann = host().STAGE_SCORE["uit-openviic-annotation-test.json"]
    rec_new = {n: {"kit_sha256": {k: v for k, v in rec["env"]["kit_b"].items()
                                  if k in ("protocol_pilot.py", "punctuation_audit.py")},
                   "jar_sha256": rec["env"]["jar_sha256"], "score_field": "cider_s", "annotation_sha256": ann,
                   "list_sha256": TEST_LISTS["primary" if n == "ov_test_1941" else "tsv"][1]}
               for n in ("ov_test_1941", "ov_test_2001")}
    rec_old = (json.loads(Path(a.record_old).read_text(encoding="utf-8"))
               if a.record_old and Path(a.record_old).is_file() and sha(a.record_old) == RECORD_OLD_SHA256 else {})
    sets, rows_all = {}, []
    for name, want in scored_sets(ROOT).items():
        if isinstance(want, str):
            rec.setdefault("not_run", {})[name] = want
            continue
        led = score_runs("ov_test", name, runs_in(w / "in"), w / f"led/{name}.jsonl", a.token, a.rehearsal)
        per, ids = columns(led, name)
        if sorted(ids) != sorted(want):
            raise SystemExit(f"REFUSED: {name} rows are not on the {len(want)} ids of its pinned list")
        sets[name], rows_all = (per, ids), rows_all + led
    batch = {}
    for name, path in (("ov_test_1941", a.fl_1941), ("ov_test_2001", a.fl_2001)):
        if name not in sets or path is None or not Path(path).is_file() or sha(path) != FL_LEDGER_SHA256[name]:
            continue
        per, ids = sets[name]
        for m in FIRST_LOOK:
            if m in token["backbones"] and complete(per, m):
                batch.setdefault(name, {})[m] = batch_delta(per, ids, read_ledgers([path]), rec_new.get(name, {}),
                                                            rec_old.get(name, {}), m, boot_idx(len(ids)))
    res = test_decision(sets, token, cap.get("dropped", []), batch=batch.get("ov_test_1941"))
    res["S-batch on the 2,001 (sensitivity)"] = batch.get("ov_test_2001", "NOT RUN")
    import score2 as S2s

    E4, PA, _ptb = S2s.kit2(KIT)
    q = [json.loads(p.read_text(encoding="utf-8")) for p in runs_in(w / "in") if f"_{SENS_MODEL}_ov_test-" in p.name]
    refs = {i: r for i, r in host().score_refs("ov_test", host().C.load_lists(host().CL)).items()
            if i in set(sets["ov_test_1941"][1])}
    res["df_sensitivity"] = dfsens(q, rows_all, refs, E4, PA)
    return res


def cmd_stage(a) -> None:
    """One stage per call on the host: rehearsal | test. Copies the pulled tree read-only, checks it against the logged
    SHA256SUMS and the environment, scores once, writes the decision file once and prints its sha256."""
    g6_open()
    w = Path(a.work)
    out = w / "res" / DECISION[a.stage]
    once(out)
    need = ("parity_preds", "parity_ledger") + (("carve", "carve_sha") if a.stage == "rehearsal"
                                                else ("token", "rehearsal", "cap"))
    if any(getattr(a, k) is None for k in need):
        raise SystemExit(f"REFUSED: stage {a.stage} needs --{', --'.join(k.replace('_', '-') for k in need)}")
    host()
    if (Path(a.tree) / "RUNNING").exists():
        raise SystemExit(f"REFUSED: {a.tree}/RUNNING exists: never beside a decode job")
    freeze_copy(Path(a.tree), w / "in")
    rec = {"stage": a.stage, "utc": time.strftime("%Y-%m-%dT%H:%M:%SZ", time.gmtime()),
           "tree": {"sums_sha256": a.sums, "files": tree_ok(w / "in", a.sums)}, "env": env_record()}
    (w / "led").mkdir(parents=True, exist_ok=True)
    res = (st_rehearsal if a.stage == "rehearsal" else st_test)(a, w, rec)
    res["record"] = rec
    print(f"STAGE {a.stage} DONE: {out.name} sha256 {write_once(out, res)}; write it to the LOG, then STOP")


def main() -> None:
    ap = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    sub = ap.add_subparsers(dest="cmd", required=True)
    for name in ("plan", "timecheck"):
        p = sub.add_parser(name)
        p.add_argument("--dry-run", action="store_true")
        p.add_argument("--freeze-utc", default=G6_UTC, help="dry run only")
        if name == "plan":
            p.add_argument("--mode", choices=("rehearsal", "test"), required=True)
            p.add_argument("--d1", type=Path, nargs="*", default=[], help="forward D1 files of the D1-PASS runners")
            p.add_argument("--runners", nargs="*", default=[], choices=STEP_ORDER, help="dry run only")
            p.add_argument("--force-ceiling-h", type=float, help="dry run only: a forced binding cap")
            p.add_argument("--out", type=Path, required=True)
        else:
            p.add_argument("--cap", type=Path, required=True)
    p = sub.add_parser("parity")
    p.add_argument("--preds", type=Path, required=True)
    p.add_argument("--ledger", type=Path, required=True)
    p = sub.add_parser("stage")
    p.add_argument("stage", choices=("rehearsal", "test"))
    p.add_argument("--work", type=Path, default=WORK)
    p.add_argument("--tree", type=Path, required=True, help="the pulled output tree on the host")
    p.add_argument("--sums", required=True, help="sha256 of the tree's SHA256SUMS, as logged")
    p.add_argument("--parity-preds", type=Path, required=True)
    p.add_argument("--parity-ledger", type=Path, required=True)
    p.add_argument("--carve", type=Path, help="rehearsal: the carve list (ids)")
    p.add_argument("--carve-sha", help="rehearsal: its sha256, as logged at block 0")
    for k in ("token", "rehearsal", "cap", "record_old", "fl_1941", "fl_2001"):
        p.add_argument("--" + k.replace("_", "-"), type=Path, help="test stage")
    a = ap.parse_args()
    {"plan": cmd_plan, "timecheck": cmd_timecheck, "parity": cmd_parity, "stage": cmd_stage}[a.cmd](a)


if __name__ == "__main__":
    main()
