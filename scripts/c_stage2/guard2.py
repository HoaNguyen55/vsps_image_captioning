#!/usr/bin/env python3
"""Paper C stage 2 (STAGE 2 / DEV-B, ONE LOOK): the object guard on the stage-2 sets. DESIGN §5 unchanged; prereg
manuscript/prereg/2026-10-22_c_stage2/PREREG.md §5.3 and §12 item 7.

  python scripts/c_stage2/guard2.py --selftest                                                        CPU, no data
  python scripts/c_stage2/guard2.py items --set S --generator M --runs R ... --zs Z --lists L --out items.jsonl
  python scripts/c_stage2/guard2.py score --set S --items I --generator M --lists L [--snapshot DIR] --out cache  GPU
Items are the neighbour-only classes of the runs whose arms §5.3 verifies: `ret` always (C-a), `rand` and `fix`
only when the frozen tau is finite; the image-blind arm never. The verifiers and their venvs are stage 1's.
"""
from __future__ import annotations

import argparse
import json
import sys
import tempfile
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))
import stage2 as S2  # noqa: E402

C, G, lb = S2.C, S2.G, S2.lb


def check_runs(runs: list[dict], zs: dict, cfg: dict, ds: str) -> None:
    """The runs are exactly the frozen runs of the arms §5.3 verifies, for one generator and set, with its stage-2 zs."""
    model = zs["model"]
    want = {S2.spec(cfg, ds, model, arm)["run_id"] for arm in S2.verify_arms(cfg, model)}
    if {r["run_id"] for r in runs} != want or {(r["model"], r["dataset"]) for r in runs + [zs]} != {(model, ds)}:
        raise SystemExit(f"items: the runs must be exactly {sorted(want)}")
    if any(r.get("c_schema") != S2.SCHEMA for r in runs):
        raise SystemExit("items: not stage-2 outputs")
    S2.zs_ok2(zs, model, ds)


def cmd_items(a) -> None:
    lists = C.load_lists(a.lists)
    runs, zs = [G.read_preds(p) for p in a.runs], G.read_preds(a.zs)
    if zs["model"] != a.generator:
        raise SystemExit("items: the zero-shot run is not this generator's")
    check_runs(runs, zs, S2.frozen(), a.set)
    rows = G.items(runs, zs, C.memory_captions(lists))
    Path(a.out).write_text("".join(json.dumps({**r, "generator": a.generator}) + "\n" for r in rows),
                           encoding="utf-8")
    print(f"{len(rows)} neighbour-only items")


def item_paths(todo: list[dict], ds: str, lists: dict) -> dict:
    """{(set, id): (path, sha256)}; refused unless every item image is in the stage-2 set's manifest."""
    rows = S2.manifest2(ds, lists)  # refuses any set but the two stage-2 sets
    folder = lb.DATA / "datasets" / S2.SETS[ds]["image_dir"]
    paths = {(ds, i): (folder / f, h) for i, f, h in rows}
    if any((t["dataset"], t["image_id"]) not in paths for t in todo):
        raise SystemExit(f"REFUSED: an item image is not in the {ds} manifest")
    return paths


def cmd_score(a) -> None:
    reg2 = G.s2()
    lists = C.load_lists(a.lists)
    todo = [json.loads(x) for x in Path(a.items).read_text(encoding="utf-8").splitlines() if x]
    if {t["generator"] for t in todo} != {a.generator}:
        raise SystemExit("the items were not made for this generator")
    paths = item_paths(todo, a.set, lists)
    S2.check_folder(a.set, lists)
    verifier = G.VERIFIER[a.generator]
    if verifier == "internvl3_s2":
        load, ask, about = G.s2_verifier(reg2)
    else:
        reg = C.registration()
        if lb.packages() != reg["venv"]["packages"]:
            raise SystemExit("the Qwen3-VL verifier runs in the B-N1 venv")
        lb.check_snapshot(reg["models"][verifier], a.snapshot)
        load, ask, about = G.hf_verifier(reg["models"][verifier], a.snapshot)

    def checked(path_sha):
        path, h = path_sha
        if lb.sha256_file(path) != h:
            raise SystemExit(f"{path}: sha256 differs from the manifest")
        return load(path)

    n = G.fill(Path(a.out), todo, paths, (checked, ask), reg2["verifier_protocol"], verifier)
    if "yes_no_mass" in about:
        mass = sorted(about.pop("yes_no_mass"))
        about["yes_no_mass_median"] = mass[len(mass) // 2] if mass else None
    Path(str(a.out) + ".about.json").write_text(json.dumps({**about, "verifier": verifier, "label": S2.LABEL,
                                                            "c_prereg_sha256": S2.PINS[S2.PREREG],
                                                            "packages": lb.packages(), "new_rows": n}) + "\n")


# ------------------------------------------------------------------------------------------------ self-test (CPU)
def selftest() -> None:
    cfg = S2.frozen()
    zs = {"run_id": "c2_qwen25vl_7b_ov_dev_b-zs", "model": "qwen25vl_7b", "dataset": "ov_dev_b"}
    run = lambda arm, m="qwen25vl_7b": {"run_id": S2.spec(cfg, "ov_dev_b", m, arm)["run_id"], "model": m,  # noqa
                                        "dataset": "ov_dev_b", "c_schema": S2.SCHEMA}
    # tau = -inf for qwen25vl_7b: the ret items are verified, rand and fix are not (C-a)
    assert C.refuses(lambda: check_runs([run("ret"), run("rand")], zs, cfg, "ov_dev_b")), "rand not verified at -inf"
    assert C.refuses(lambda: check_runs([], zs, cfg, "ov_dev_b")), "ret is always verified"
    assert C.refuses(lambda: check_runs([run("blind")], zs, cfg, "ov_dev_b")), "the blind arm is never guarded"
    assert C.refuses(lambda: check_runs([run("ret")], {**zs, "c_schema": C.SCHEMA}, cfg, "ov_dev_b")), "stage-1 zs"
    with tempfile.TemporaryDirectory() as tmp:
        lp, lists = S2.fake_lists(Path(tmp))
        todo = [{"dataset": "ov_dev_b", "image_id": "b1.jpg", "class": "c1"}]
        assert len(item_paths(todo, "ov_dev_b", lists)) == 925
        assert C.refuses(lambda: item_paths([{**todo[0], "image_id": "ot1.jpg"}], "ov_dev_b", lists)), "test image"
        assert C.refuses(lambda: item_paths(todo, "ov_dev_a", lists)), "no dev-A image in stage 2"
    print("selftest ok: verified arms per frozen tau (ret always, blind never), stage-2 zs only, item refusal")


def main() -> None:
    ap = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    ap.add_argument("--selftest", action="store_true")
    sub = ap.add_subparsers(dest="cmd")
    p = sub.add_parser("items")
    p.add_argument("--set", choices=sorted(S2.SETS), required=True)
    p.add_argument("--generator", choices=sorted(G.VERIFIER), required=True)
    p.add_argument("--runs", nargs="+", type=Path, required=True)
    p.add_argument("--zs", type=Path, required=True)
    p.add_argument("--lists", type=Path, required=True)
    p.add_argument("--out", required=True)
    p = sub.add_parser("score")
    p.add_argument("--set", choices=sorted(S2.SETS), required=True)
    p.add_argument("--items", required=True)
    p.add_argument("--generator", choices=sorted(G.VERIFIER), required=True)
    p.add_argument("--lists", type=Path, required=True)
    p.add_argument("--snapshot", type=Path, help="Qwen3-VL-8B snapshot (verifier of internvl3_8b)")
    p.add_argument("--out", required=True)
    a = ap.parse_args()
    if a.selftest:
        return selftest()
    {"items": cmd_items, "score": cmd_score}.get(a.cmd, lambda _a: ap.error("mode?"))(a)


if __name__ == "__main__":
    main()
