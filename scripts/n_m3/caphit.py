#!/usr/bin/env python3
"""N-M3 cap-hit share for Paper A: how many G2-B Qwen3-VL-8B detailed captions reached the 160-new-token cap.
POST_HOC, descriptive, no verdict (PD-30, revised by CC-073); design in manuscript/prereg/2026-10-21_n_m3_caphit/DESIGN.md.

Source of {p}: the decoder-recorded per-image n_tokens; hit := n_tokens >= 160 (the registered max_new_tokens).
Re-tokenization of the saved caption with the registered tokenizer (length >= 158) is a reported agreement check.

  --selftest  synthetic data only (a whitespace tokenizer for the logic; the real tokenizer on synthetic strings)
  gate        STRUCTURAL: n_tokens present for every image of the 9 Vietnamese detailed runs, every value an integer
              in [0, 160]; outputs booleans and image counts only, no share                      -> gate.json
  run         refuses unless this script and DESIGN.md equal their HEAD blobs and the gate holds; one pass
                                                                                  -> data/results/n_m3/caphit_result.json
Every mode first refuses unless every input equals its recorded sha256 (PINS), before transformers is imported.
The tokenizer (selftest, run) needs transformers==4.57.6 and tokenizers==0.22.2 (the registered decode freeze).
  python3 -B scripts/n_m3/caphit.py run
"""
from __future__ import annotations

import hashlib
import json
import os
import subprocess
import sys
from decimal import ROUND_HALF_UP, Decimal
from pathlib import Path

ROOT = Path(__file__).resolve().parents[2]
PRE = "manuscript/prereg/2026-10-21_n_m3_caphit"
DESIGN = ROOT / PRE / "DESIGN.md"
RESULT = "data/results/n_m3/caphit_result.json"
TOK = ".session_backup/2026-10-21/n_m3_tokenizer"
AN2 = ".session_backup/2026-10-20/a_n2_run/outputs"
BN1 = ".session_backup/2026-10-20/b_n1_run/outputs"
G2B = ".session_backup/2026-10-20/g2b_score/outputs"
VERSIONS = {"transformers": "4.57.6", "tokenizers": "0.22.2"}
CAP, RETOK_HIT, THRESHOLDS = 160, 158, (155, 158, 160)
END_PUNCT, CLOSERS = ".!?…", "\"'”’»)]"
CLAUSES = {  # CC-073 ruling 4; amendment 5 rows 33-34
    "sec7_6": "detailed captions capped at 160 new tokens, {p}% of which reached the cap by the recorded token "
              "counts, Supplementary S7",
    "sec10_5_c3": "(Qwen3-VL-8B; detailed captions capped at 160 new tokens, {p}% of which reached the cap, "
                  "Supplementary S7)"}
FALLBACK = "detailed captions capped at 160 new tokens (cap share: Supplementary S7)"
AN2_FILES = [f"{AN2}/lbA_qwen3vl_8b_{s}-detailed_en.preds.json" for s in ("cv295", "uv231en")]
VI_CHECK_FILES = [f"{BN1}/lbB_qwen3vl_8b_{s}-detailed.preds.json" for s in ("ktvic_test", "uitviic_test")]
SETS = ("cv295", "uv231", "xm600")
LADDER_DETAILED = {s: [f"g2b_q3_{s}-detailed-{t}" for t in ("T0", "T05", "T08")] for s in SETS}
DETAILED_EN = ["g2b_q3_cv295-detailed_en-T0", "g2b_q3_uv231-detailed_en-T0"]

# path -> sha256; the source of each value is listed in DESIGN.md (Inputs)
PINS = dict(line.split()[::-1] for line in """
4e535c31860868b9a14a68990a0474d8b8bf1ffd1993aeabf3fb5085b0be8083 .session_backup/2026-10-13/decisions/PD-30.txt
c506bc777b483f5097561d2894a535f33e5e9e27745af07c0f979fbac5560055 manuscript/prereg/2026-10-18_g2b_qwen3vl_ladder.json
dc7bd4a45eb3c56e00c56f68cd937871258b679b741949bd38a383950ffc52d8 .session_backup/2026-10-13/research_r9/C8_backbone/SHA256SUMS
bf152944ea4389f609207c5f9589c214b2ff6a4ae3b2e2a9c877e64a57fbe605 .session_backup/2026-10-13/research_r9/C8_backbone/FREEZE.txt
a5d85b6dcc535e6b93115a9ef287e6132fdbf30270da6218194ba742261173c7 .session_backup/2026-10-21/n_m3_tokenizer/tokenizer.json
c2da771801886ad9ae98181793ffd3dfb7f1af30f6f7c6a4e15d7dbba52e2399 .session_backup/2026-10-21/n_m3_tokenizer/tokenizer_config.json
ca10d7e9fb3ed18575dd1e277a2579c16d108e32f27439684afa0e10b1440910 .session_backup/2026-10-21/n_m3_tokenizer/vocab.json
599bab54075088774b1733fde865d5bd747cbcc7a547c5bc12610e874e26f5e3 .session_backup/2026-10-21/n_m3_tokenizer/merges.txt
5cd452860dc1e9c29dd71cc3cef7f39b338b7a40793f7a260655c2d3568f3661 .session_backup/2026-10-21/n_m3_tokenizer/config.json
1f6ce422e0163d81661bf5711787086b2f11ae177f3dbc6b06ae6cd4ebc3dfdc data/results/a_n2/a_n2_run.json
7935912a50eae9aca9afd45c4f18ab8eb821be5c69c0c21453b028b71b95aaa4 .session_backup/2026-10-20/a_n2_run/outputs/lbA_qwen3vl_8b_cv295-detailed_en.preds.json
91f9a7265d86b6874cc860fab66c0454890bbf3eb1e00f81ae50d8100d5dfcb9 .session_backup/2026-10-20/a_n2_run/outputs/lbA_qwen3vl_8b_uv231en-detailed_en.preds.json
adad454d6c9f4810142da5a7a43d27fb122aa61d5a482dc3bc925edd152557d7 data/results/b_n1/b_n1_run.json
51df6c6f4cded1dbbd54b3330146d311b899640ae3503065a3f9367706c5e38e .session_backup/2026-10-20/b_n1_run/outputs/lbB_qwen3vl_8b_ktvic_test-detailed.preds.json
e89477e3591bb257d63e28202e2c6c9257f3e40354684f83925bf204bc6d7d7b .session_backup/2026-10-20/b_n1_run/outputs/lbB_qwen3vl_8b_uitviic_test-detailed.preds.json
02bdca27949e781ab90376ce97e25555df35d140369f967ae6b7feef63b9f78e data/results/g2b/g2b_score_record/precheck.json
9ec537886f0d91d23c8c03196bf0aeb2f737b100f06aa36dbf09bea7553b5f02 .session_backup/2026-10-20/g2b_score/outputs/g2b_q3_cv295-detailed-T0.preds.json
1d9934b9b108feaaa2fff5b8eb7071db97005be47901df0f3bcf69d70a67fc58 .session_backup/2026-10-20/g2b_score/outputs/g2b_q3_cv295-detailed-T05.preds.json
59f2e5534c3e6a6cfd8a7a9c1ba3f951be0a4b41e82f70390f19f6970ebfa8f8 .session_backup/2026-10-20/g2b_score/outputs/g2b_q3_cv295-detailed-T08.preds.json
2a92344baddc53c2e3974a701a973b8e1be0f44bcf780376851d812f27dcdeec .session_backup/2026-10-20/g2b_score/outputs/g2b_q3_uv231-detailed-T0.preds.json
3bef57a29456f81cbce0b9c839c45100112132a7ee6a8eafd57d7ed724b57420 .session_backup/2026-10-20/g2b_score/outputs/g2b_q3_uv231-detailed-T05.preds.json
d994c6961bf1b6343df239fbbc1ada63a4665a2a2790065d9fa5d0fe398f3fcd .session_backup/2026-10-20/g2b_score/outputs/g2b_q3_uv231-detailed-T08.preds.json
a66647d12140858e8c013fdce6133949c4b97179d91acc92c413608bf0a560df .session_backup/2026-10-20/g2b_score/outputs/g2b_q3_xm600-detailed-T0.preds.json
3e6189d627affaec4e327b1eb3ac1a55a3b76cbc8ae5001dc3c63de9c6baa9ee .session_backup/2026-10-20/g2b_score/outputs/g2b_q3_xm600-detailed-T05.preds.json
944668eb32fb4a76209837f394bf6cd62a3245d8ac467e715105b3953dd2e751 .session_backup/2026-10-20/g2b_score/outputs/g2b_q3_xm600-detailed-T08.preds.json
736a3d3287735e48c650dc0e912c7fedab18503a35bb7bf33ee2279f8589cd31 .session_backup/2026-10-20/g2b_score/outputs/g2b_q3_cv295-detailed_en-T0.preds.json
85066857b493eb303f8effe84a8d5c02f36e7d186449d87ff0a2e8ef76b2604d .session_backup/2026-10-20/g2b_score/outputs/g2b_q3_uv231-detailed_en-T0.preds.json
""".strip().splitlines())


def sha(path: Path) -> str:
    return hashlib.sha256(Path(path).read_bytes()).hexdigest()


def check_pins() -> None:
    bad = [p for p, want in PINS.items() if not (ROOT / p).exists() or sha(ROOT / p) != want]
    if bad:
        raise SystemExit(f"refused: inputs differ from their recorded sha256: {bad}")


def load_tokenizer():
    os.environ["HF_HUB_OFFLINE"] = os.environ["TRANSFORMERS_OFFLINE"] = "1"
    import tokenizers
    import transformers
    got = {"transformers": transformers.__version__, "tokenizers": tokenizers.__version__}
    if got != VERSIONS:
        raise SystemExit(f"refused: package versions {got} differ from the registered freeze {VERSIONS}")
    tok = transformers.AutoTokenizer.from_pretrained(str(ROOT / TOK), local_files_only=True)
    if type(tok).__name__ != "Qwen2TokenizerFast":
        raise SystemExit(f"refused: unexpected tokenizer class {type(tok).__name__}")
    return lambda text: len(tok.encode(text, add_special_tokens=False)), tok


def write(rel: str, obj: dict) -> None:
    out = ROOT / rel
    out.parent.mkdir(parents=True, exist_ok=True)
    out.write_text(json.dumps(obj, indent=1, ensure_ascii=False) + "\n", encoding="utf-8")
    print(json.dumps({"wrote": rel, "sha256": sha(out)}))


def provenance() -> dict:
    return {"script_sha256": sha(Path(__file__)), "design_sha256": sha(DESIGN) if DESIGN.exists() else None,
            "packages": VERSIONS}




# ------------------------------------------------------------------------------------------------ rules
def no_final_punct(caption: str) -> bool:
    """True when the caption, after trailing whitespace and closing quotes/brackets, does not end in . ! ? or …"""
    t = caption.rstrip().rstrip(CLOSERS).rstrip()
    return not t or t[-1] not in END_PUNCT


def load(rel: str) -> tuple[dict, dict[str, str]]:
    d = json.loads((ROOT / rel).read_text(encoding="utf-8"))
    return d, {str(k): (v[0] if isinstance(v, list) else v) or "" for k, v in d["predictions"].items()}


def structure(d: dict, caps: dict) -> dict:
    """Structural facts of a decode record; booleans and image counts only."""
    nt = d.get("n_tokens") or {}
    vals = [nt.get(i) for i in caps]
    ints = [type(v) is int for v in vals]
    return {"n_images": len(caps), "n_tokens_present_for_every_image": all(i in nt for i in caps),
            "all_integers": all(ints), "all_in_0_to_cap": all(ok and 0 <= v <= CAP for ok, v in zip(ints, vals)),
            "max_new_tokens_is_cap": d.get("max_new_tokens") == CAP}


def counts(recorded: list[int], lengths: list[int], caps: list[str]) -> dict:
    """Primary: recorded n_tokens >= CAP. Checks: re-tokenized length thresholds, agreement at RETOK_HIT."""
    return {"n": len(recorded), "hits_recorded": sum(r >= CAP for r in recorded),
            **{f"retok_ge_{t}": sum(x >= t for x in lengths) for t in THRESHOLDS},
            "retok_ge_158_agrees_with_recorded": sum((x >= RETOK_HIT) == (r >= CAP) for x, r in zip(lengths, recorded)),
            "no_final_punct": sum(no_final_punct(c) for c in caps)}


def shares(c: dict) -> dict:
    return {f"share_{k}": v / c["n"] for k, v in c.items() if k != "n"} if c["n"] else {}


def pool(cs: list[dict]) -> dict:
    return {k: sum(c[k] for c in cs) for k in cs[0]}


def percent(k: int, n: int) -> int:
    """100 k / n rounded half up, exactly from the integer counts (Python's round() rounds halves to even)."""
    return int((Decimal(100 * k) / Decimal(n)).quantize(Decimal(1), rounding=ROUND_HALF_UP))


def fill(k: int, n: int) -> dict:
    return {loc: t.format(p=percent(k, n)) for loc, t in CLAUSES.items()}


def validate(length, rel: str) -> dict:
    """Agreement fact: re-tokenized length vs a decode's recorded hit_max and n_tokens, per image."""
    d, caps = load(rel)
    ids = sorted(caps)
    L = {i: length(caps[i]) for i in ids}
    hit, ntok = d["hit_max"], d["n_tokens"]
    drift = [L[i] - ntok[i] for i in ids if hit[i]]
    return {"file": rel, "n": len(ids), "recorded_hits": sum(bool(hit[i]) for i in ids),
            "recorded_hit_eq_ntokens_cap": all(bool(hit[i]) == (ntok[i] == CAP) for i in ids),
            "retok_agrees_with_hit_max": {str(t): sum((L[i] >= t) == bool(hit[i]) for i in ids) for t in THRESHOLDS},
            "drift_on_recorded_hits": {"min": min(drift), "max": max(drift), "n_abs_gt_2": sum(abs(x) > 2 for x in drift)}
            if drift else None}


# ------------------------------------------------------------------------------------------------ modes
def gate_body() -> dict:
    runs = {}
    for rid in (r for s in SETS for r in LADDER_DETAILED[s]):
        runs[rid] = structure(*load(f"{G2B}/{rid}.preds.json"))
    ok = all(all(v for k, v in x.items() if k != "n_images") for x in runs.values())
    return {"runs": runs, "pass": ok}


def gate() -> int:
    body = gate_body()
    write(f"{PRE}/gate.json", {"schema": "vsps.n_m3_caphit.gate.v2", "status": "POST_HOC descriptive (PD-30, CC-073); no verdict",
                               **provenance(), "pins": PINS,
                               "statistics_computed": "structural checks only (presence, integer type, range); no share",
                               **body})
    return 0 if body["pass"] else 1


def committed(path: Path) -> bool:
    rel = str(path.resolve().relative_to(ROOT))
    r = subprocess.run(["git", "-C", str(ROOT), "show", f"HEAD:{rel}"], capture_output=True)
    return r.returncode == 0 and hashlib.sha256(r.stdout).hexdigest() == sha(path)


def score_run(length, rid: str) -> dict:
    rel = f"{G2B}/{rid}.preds.json"
    d, caps = load(rel)
    ids = sorted(caps)
    c = counts([d["n_tokens"][i] for i in ids], [length(caps[i]) for i in ids], [caps[i] for i in ids])
    return {"file": rel, "structure": structure(d, caps), "counts": c, "shares": shares(c)}


def run_body(length) -> dict:
    runs = {rid: score_run(length, rid) for s in SETS for rid in LADDER_DETAILED[s]}
    per_set = {}
    for s in SETS:
        c = pool([runs[r]["counts"] for r in LADDER_DETAILED[s]])
        per_set[s] = {"counts": c, "shares": shares(c)}
    allc = pool([runs[r]["counts"] for s in SETS for r in LADDER_DETAILED[s]])
    return {"per_run": runs, "per_run_detailed_en_S7_only": {rid: score_run(length, rid) for rid in DETAILED_EN},
            "per_set_pooled": per_set, "pooled_9_ladder_detailed": {"counts": allc, "shares": shares(allc)},
            "p": percent(allc["hits_recorded"], allc["n"]), "filled_clauses": fill(allc["hits_recorded"], allc["n"]),
            "validation_facts": [validate(length, f) for f in AN2_FILES + VI_CHECK_FILES]}


def run() -> int:
    if not (committed(Path(__file__)) and committed(DESIGN)):
        raise SystemExit("refused: caphit.py and DESIGN.md must equal their HEAD blobs")
    if (ROOT / RESULT).exists():
        raise SystemExit(f"refused: {RESULT} exists (one pass only)")
    g = gate_body()
    if not g["pass"]:
        raise SystemExit(f"STOP: structural gate failed; the clause takes the fallback: {FALLBACK!r}")
    length, _ = load_tokenizer()
    write(RESULT, {"schema": "vsps.n_m3_caphit.v2", "status": "POST_HOC descriptive; no verdict; no causal claim",
                   **provenance(), "pins": PINS, "hit_rule": f"recorded n_tokens >= {CAP}",
                   "check_rule": f"re-tokenized length >= {RETOK_HIT}", "gate": g, **run_body(length)})
    return 0


def selftest() -> int:
    checks = {}
    ws = lambda t: len(t.split())  # noqa: E731  synthetic tokenizer for the logic checks
    checks["punct"] = [no_final_punct(x) for x in ("A cat.", "A cat", 'He said "go."', "Mèo (đen)", "Hi!  ", "",
                                                   "đợi…", "a cat sat on the")] == \
        [False, True, False, True, False, True, False, True]
    c = counts([160, 160, 159, 40], [161, 157, 158, 40], ["a.", "b", "c.", "d"])
    checks["counts"] = c == {"n": 4, "hits_recorded": 2, "retok_ge_155": 3, "retok_ge_158": 2, "retok_ge_160": 1,
                             "retok_ge_158_agrees_with_recorded": 2, "no_final_punct": 2}
    checks["round_half_up"] = [percent(k, n) for k, n in ((1, 8), (27, 200), (1, 200), (497, 500), (29, 200))] == \
        [13, 14, 1, 99, 15]
    checks["fill"] = fill(2, 5) == {
        "sec7_6": "detailed captions capped at 160 new tokens, 40% of which reached the cap by the recorded token "
                  "counts, Supplementary S7",
        "sec10_5_c3": "(Qwen3-VL-8B; detailed captions capped at 160 new tokens, 40% of which reached the cap, "
                      "Supplementary S7)"} and "not recorded" not in FALLBACK
    p = pool([counts([160, 10], [160, 10], ["a", "b"]), counts([160, 160, 1], [160, 160, 1], ["c", "d", "e"])])
    checks["pooled_is_caption_weighted"] = p["n"] == 5 and p["hits_recorded"] == 3 and shares(p)["share_hits_recorded"] == 0.6
    caps = {"1": "x", "2": "y", "3": "z"}
    good = structure({"n_tokens": {"1": 160, "2": 3, "3": 0}, "max_new_tokens": 160}, caps)
    checks["structure_good"] = all(v for k, v in good.items() if k != "n_images") and good["n_images"] == 3
    bad = [structure({"n_tokens": nt, "max_new_tokens": 160}, caps) for nt in (
        {"1": 160, "2": 3}, {"1": 160, "2": 3.0, "3": 1}, {"1": 161, "2": 3, "3": 1}, {"1": True, "2": 3, "3": 1})]
    checks["structure_bad_caught"] = [b["n_tokens_present_for_every_image"] and b["all_integers"] and b["all_in_0_to_cap"]
                                      for b in bad] == [False, False, False, False]
    checks["structure_has_no_share"] = not any(isinstance(v, float) for v in good.values())
    syn = {"predictions": {"1": "w " * 160, "2": "w " * 157, "3": "short."}, "hit_max": {"1": True, "2": True, "3": False},
           "n_tokens": {"1": 160, "2": 160, "3": 2}}
    tmp = ROOT / PRE / ".selftest_synthetic.json"
    tmp.parent.mkdir(parents=True, exist_ok=True)
    tmp.write_text(json.dumps(syn), encoding="utf-8")
    try:
        v = validate(ws, str(tmp.relative_to(ROOT)))
    finally:
        tmp.unlink()
    checks["validate"] = v["retok_agrees_with_hit_max"] == {"155": 3, "158": 2, "160": 2} and \
        v["drift_on_recorded_hits"] == {"min": -3, "max": 0, "n_abs_gt_2": 1} and v["recorded_hit_eq_ntokens_cap"]
    length, tok = load_tokenizer()  # the real pinned tokenizer, on synthetic strings only
    s = [("cat " * 200).strip(), "Một con mèo đang ngồi trên ghế.", "A dog runs on the beach."]
    ids = [tok.encode(x, add_special_tokens=False) for x in s]
    checks["no_special_tokens_added"] = not any(set(i) & set(tok.all_special_ids) for i in ids)
    checks["round_trip_synthetic"] = [tok.decode(i) for i in ids] == s
    checks["length_fn_matches_encode"] = [length(x) for x in s] == [len(i) for i in ids]
    checks = {k: bool(x) for k, x in checks.items()}
    write(f"{PRE}/selftest.json", {"schema": "vsps.n_m3_caphit.selftest.v2", **provenance(), "checks": checks,
                                   "pass": all(checks.values())})
    return 0 if all(checks.values()) else 1


if __name__ == "__main__":
    modes = {"--selftest": selftest, "gate": gate, "run": run}
    if len(sys.argv) != 2 or sys.argv[1] not in modes:
        raise SystemExit(f"usage: {Path(__file__).name} {{{'|'.join(modes)}}}")
    check_pins()
    sys.exit(modes[sys.argv[1]]())
