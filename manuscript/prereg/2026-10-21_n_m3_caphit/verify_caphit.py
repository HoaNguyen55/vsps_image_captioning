"""Independent re-computation of the N-M3 cap-hit result (does not import caphit.py).

Usage: <venv python> -I verify_caphit.py /mnt/d/vsps_image_captioning
Prints a JSON report of recomputed numbers and every comparison with caphit_result.json.
Never prints caption text.
"""
import hashlib
import json
import sys
from pathlib import Path

CAP = 160
CLOSERS = " \t\r\n\"'”’»)]"
FINAL = ".!?…"
SETS = ("cv295", "uv231", "xm600")
TEMPS = ("T0", "T05", "T08")
G2B_DIR = ".session_backup/2026-10-20/g2b_score/outputs"
TOK_DIR = ".session_backup/2026-10-21/n_m3_tokenizer"
TOK_FILES = ("tokenizer.json", "tokenizer_config.json", "vocab.json", "merges.txt", "config.json")
VALIDATION = (
    ("data/results/a_n2/a_n2_run.json", ".session_backup/2026-10-20/a_n2_run", "lbA_qwen3vl_8b_cv295-detailed_en"),
    ("data/results/a_n2/a_n2_run.json", ".session_backup/2026-10-20/a_n2_run", "lbA_qwen3vl_8b_uv231en-detailed_en"),
    ("data/results/b_n1/b_n1_run.json", ".session_backup/2026-10-20/b_n1_run", "lbB_qwen3vl_8b_ktvic_test-detailed"),
    ("data/results/b_n1/b_n1_run.json", ".session_backup/2026-10-20/b_n1_run", "lbB_qwen3vl_8b_uitviic_test-detailed"),
)


def sha(path):
    return hashlib.sha256(path.read_bytes()).hexdigest()


def no_final_punct(caption):
    tail = caption.rstrip(CLOSERS)
    return not tail or tail[-1] not in FINAL


def round_half_up_pct(num, den):
    return (200 * num + den) // (2 * den)


def run_counts(preds, tok):
    caps, ntok = preds["predictions"], preds["n_tokens"]
    c = dict.fromkeys(("n", "hits_recorded", "retok_ge_155", "retok_ge_158", "retok_ge_160",
                       "retok_ge_158_agrees_with_recorded", "no_final_punct"), 0)
    for img, caption in caps.items():
        length = len(tok.encode(caption, add_special_tokens=False))
        hit = ntok[img] >= CAP
        c["n"] += 1
        c["hits_recorded"] += hit
        c["retok_ge_155"] += length >= 155
        c["retok_ge_158"] += length >= 158
        c["retok_ge_160"] += length >= 160
        c["retok_ge_158_agrees_with_recorded"] += (length >= 158) == hit
        c["no_final_punct"] += no_final_punct(caption)
    return c


def structure(preds):
    vals = [preds["n_tokens"].get(k) for k in preds["predictions"]]
    return {
        "n_images": len(preds["predictions"]),
        "n_tokens_present_for_every_image": all(k in preds["n_tokens"] for k in preds["predictions"]),
        "all_integers": all(type(v) is int for v in vals),
        "all_in_0_to_cap": all(type(v) is int and 0 <= v <= CAP for v in vals),
        "max_new_tokens_is_cap": preds.get("max_new_tokens") == CAP,
    }


def add(a, b):
    return {k: a.get(k, 0) + b[k] for k in b}


def compare(label, mine, theirs, out):
    if isinstance(mine, dict):
        for k in sorted(set(mine) | set(theirs or {})):
            compare(f"{label}.{k}", mine.get(k), (theirs or {}).get(k), out)
        return
    ok = mine == theirs if not isinstance(mine, float) else theirs is not None and abs(mine - theirs) < 1e-12
    out.append((label, ok, mine, theirs))


def main(repo):
    import tokenizers
    import transformers
    assert (transformers.__version__, tokenizers.__version__) == ("4.57.6", "0.22.2")

    sums = dict(line.split()[::-1] for line in
                (repo / ".session_backup/2026-10-13/research_r9/C8_backbone/SHA256SUMS").read_text().splitlines()
                if line.strip())
    tok_dir = repo / TOK_DIR
    tok_sha_ok = {f: sha(tok_dir / f) == sums.get(f) for f in TOK_FILES}
    assert all(tok_sha_ok.values()), tok_sha_ok
    tok = transformers.AutoTokenizer.from_pretrained(str(tok_dir), local_files_only=True)
    assert type(tok).__name__ == "Qwen2TokenizerFast", type(tok).__name__

    precheck = json.loads((repo / "data/results/g2b/g2b_score_record/precheck.json").read_text())["runs"]
    result = json.loads((repo / "data/results/n_m3/caphit_result.json").read_text())

    def load_g2b(run_id):
        path = repo / G2B_DIR / f"{run_id}.preds.json"
        assert precheck[run_id]["file"] == path.name
        assert sha(path) == precheck[run_id]["sha256"], run_id
        preds = json.loads(path.read_text())
        assert preds["run_id"] == run_id
        return preds

    cmp = []
    per_set = {}
    pooled = {}
    for s in SETS:
        for t in TEMPS:
            rid = f"g2b_q3_{s}-detailed-{t}"
            preds = load_g2b(rid)
            st, c = structure(preds), run_counts(preds, tok)
            compare(f"gate.{rid}", st, result["gate"]["runs"][rid], cmp)
            compare(f"per_run.{rid}.structure", st, result["per_run"][rid]["structure"], cmp)
            compare(f"per_run.{rid}.counts", c, result["per_run"][rid]["counts"], cmp)
            compare(f"per_run.{rid}.shares", {f"share_{k}": v / c["n"] for k, v in c.items() if k != "n"},
                    result["per_run"][rid]["shares"], cmp)
            per_set[s] = add(per_set.get(s, {}), c)
            pooled = add(pooled, c)
    for s in SETS:
        compare(f"per_set_pooled.{s}.counts", per_set[s], result["per_set_pooled"][s]["counts"], cmp)
        compare(f"per_set_pooled.{s}.shares",
                {f"share_{k}": v / per_set[s]["n"] for k, v in per_set[s].items() if k != "n"},
                result["per_set_pooled"][s]["shares"], cmp)
    compare("pooled_9.counts", pooled, result["pooled_9_ladder_detailed"]["counts"], cmp)
    compare("pooled_9.shares", {f"share_{k}": v / pooled["n"] for k, v in pooled.items() if k != "n"},
            result["pooled_9_ladder_detailed"]["shares"], cmp)
    p = round_half_up_pct(pooled["hits_recorded"], pooled["n"])
    compare("p", p, result["p"], cmp)
    compare("filled_clauses", {
        "sec7_6": f"detailed captions capped at 160 new tokens, {p}% of which reached the cap by the recorded "
                  "token counts, Supplementary S7",
        "sec10_5_c3": f"(Qwen3-VL-8B; detailed captions capped at 160 new tokens, {p}% of which reached the cap, "
                      "Supplementary S7)",
    }, result["filled_clauses"], cmp)

    for s in ("cv295", "uv231"):
        rid = f"g2b_q3_{s}-detailed_en-T0"
        preds = load_g2b(rid)
        compare(f"detailed_en.{rid}.structure", structure(preds),
                result["per_run_detailed_en_S7_only"][rid]["structure"], cmp)
        compare(f"detailed_en.{rid}.counts", run_counts(preds, tok),
                result["per_run_detailed_en_S7_only"][rid]["counts"], cmp)

    for i, (run_json, base, rid) in enumerate(VALIDATION):
        expected = json.loads((repo / run_json).read_text())["inputs_sha256"][f"outputs/{rid}.preds.json"]
        path = repo / base / "outputs" / f"{rid}.preds.json"
        assert sha(path) == expected, rid
        preds = json.loads(path.read_text())
        hm, nt = preds["hit_max"], preds["n_tokens"]
        lens = {k: len(tok.encode(v, add_special_tokens=False)) for k, v in preds["predictions"].items()}
        drift = [lens[k] - nt[k] for k in lens if hm[k]]
        compare(f"validation[{i}]", {
            "file": f"{base}/outputs/{rid}.preds.json",
            "n": len(lens),
            "recorded_hits": sum(hm[k] for k in lens),
            "recorded_hit_eq_ntokens_cap": all(hm[k] == (nt[k] >= CAP) for k in lens),
            "retok_agrees_with_hit_max": {str(th): sum((lens[k] >= th) == hm[k] for k in lens)
                                          for th in (155, 158, 160)},
            "drift_on_recorded_hits": {"min": min(drift), "max": max(drift),
                                       "n_abs_gt_2": sum(abs(d) > 2 for d in drift)},
        }, result["validation_facts"][i], cmp)

    bad = [c for c in cmp if not c[1]]
    print(json.dumps({
        "tokenizer_class": type(tok).__name__,
        "tokenizer_files_match_SHA256SUMS": tok_sha_ok,
        "pooled_9": pooled, "per_set": per_set, "p": p,
        "n_compared": len(cmp), "n_mismatch": len(bad),
        "mismatches": [{"field": f, "mine": m, "result": r} for f, _, m, r in bad],
        "verdict": "PASS" if not bad else "FAIL",
    }, indent=1))


def _selfcheck():
    assert round_half_up_pct(3367, 3378) == 100
    assert round_half_up_pct(1, 200) == 1 and round_half_up_pct(1, 400) == 0  # 0.5% -> 1, 0.25% -> 0
    assert no_final_punct("abc") and no_final_punct("") and no_final_punct(' ")')
    assert not no_final_punct("abc.") and not no_final_punct('abc." ') and not no_final_punct("abc…”)")


if __name__ == "__main__":
    _selfcheck()
    main(Path(sys.argv[1]))
