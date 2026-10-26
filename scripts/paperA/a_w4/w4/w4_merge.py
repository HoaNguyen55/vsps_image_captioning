#!/usr/bin/env python
"""CC-108 W4 / CP-111 W3 gates (CPU, local, after the M3 decode is mirrored). Hashes and ids only; no caption text
is printed.
  parity DIR           DIR holds {fuse2_s42,p1_s43}-{short,detailed}.shard0of1.jsonl decoded on parity50_manifest.json;
                       every caption must be byte-identical to the existing 2,500-image decode (sha256). Exit 1 if not.
  merge REST_DIR OUT   union by cocoid of data/results/coco_transfer (2,500 seed-42) and REST_DIR (manifest_rest2500),
                       written to OUT in cocoid order, after the disjoint / exact-cover / one-row-per-id asserts; then
                       the post-merge gate (gate_merged) on the files as written.
  full M3_DIR OUT      parity-fail path (PI-1026f Q1): all 5,000 rows per run from one M3 environment, no merge;
                       counts the seed-42 captions that differ from coco_transfer (count only, for the disclosure).
  selftest             CPU check on existing data: stand-in REST rows (the 5,000-row zero-shot decodes, not adapter
                       output) are merged into a temp dir; parity and both post-merge gates must pass, and a single
                       changed seed-42 caption or parity hash must be caught.
"""
import hashlib
import json
import subprocess
import sys
import tempfile
from pathlib import Path

ROOT = Path("/mnt/d/vsps_image_captioning")
HERE = Path(__file__).resolve().parent
EVAL = HERE.parent / "eval" / "check_coco_full.py"
FROZEN = ROOT / ".session_backup/2026-10-14/r11_litmaps/L1/check_coco.json"  # pinned in ../INPUTS.sha256
OLD = ROOT / "data/results/coco_transfer"
RUNS = [f"{s}-{m}" for s in ("fuse2_s42", "p1_s43") for m in ("short", "detailed")]
ids = lambda f: {i["cocoid"] for i in json.loads((ROOT / "data/coco_probe" / f).read_text())["images"]}


def rows(path: Path) -> dict[int, str]:
    out = {}
    for line in path.read_text("utf-8").splitlines():
        r = json.loads(line)
        assert r["cocoid"] not in out, f"{path.name}: duplicate cocoid {r['cocoid']}"
        out[r["cocoid"]] = r["caption"]
    return out


def parity(d: Path) -> int:
    exp = json.loads((HERE / "parity50_expected_caption_sha256.json").read_text())["expected"]
    bad = 0
    for run in RUNS:
        got = rows(d / f"{run}.shard0of1.jsonl")
        assert set(map(str, got)) == set(exp[run]), f"{run}: ids differ from the parity manifest"
        n = sum(hashlib.sha256(got[int(c)].encode("utf-8")).hexdigest() != h for c, h in exp[run].items())
        print(f"{run}: {50 - n}/50 byte-identical")
        bad += n
    return int(bad > 0)


def byte_mismatches(rest: Path, out: Path) -> list[str]:
    """Post-merge gate 1 check: re-read the written files; list every run whose ids or order differ from
    manifest_full5000 and every cocoid whose caption differs byte for byte from coco_transfer (seed 42) or REST_DIR."""
    full, bad = sorted(ids("manifest_full5000.json")), []
    for run in RUNS:
        m = rows(out / f"{run}.shard0of1.jsonl")
        if list(m) != full:
            bad.append(f"{run}: merged ids or order differ from manifest_full5000")
            continue
        for src in (OLD, rest):
            bad += [f"{run}: cocoid {c} differs from {src.name}" for c, cap in rows(src / f"{run}.shard0of1.jsonl").items()
                    if m[c].encode("utf-8") != cap.encode("utf-8")]
    return bad


def gate_bytes(rest: Path, out: Path) -> None:
    bad = byte_mismatches(rest, out)
    assert not bad, "post-merge gate 1 failed: " + "; ".join(bad[:10])
    print("post-merge gate 1: merged captions equal coco_transfer (seed 42) and REST byte for byte, 4/4 runs")


def gate_rescore(out: Path) -> None:
    """Post-merge gate 2: check_coco_full on manifest.json with all9full (merged adapters from OUT) equals the frozen
    check_coco.json (n_img, systems, every gold cell). Completeness is asserted inside check_coco_full."""
    with tempfile.TemporaryDirectory() as t:
        res = Path(t) / "r0_from_merged.json"
        subprocess.run([sys.executable, str(EVAL), str(ROOT / "data/coco_probe/manifest.json"),
                        str(ROOT / "data/coco_probe/instance_gold.json"), "all9full", str(res), str(out.resolve())],
                       check=True, stdout=subprocess.DEVNULL)
        got, ref = json.loads(res.read_text()), json.loads(FROZEN.read_text())
    for k in ("n_img", "systems", "gold"):
        assert got[k] == ref[k], f"re-score of the merged files on manifest.json differs from frozen check_coco.json: {k}"
    print("post-merge gate 2: all9full on manifest.json equals frozen check_coco.json")


def merge(rest: Path, out: Path) -> int:
    seed, other, full = ids("manifest.json"), ids("manifest_rest2500.json"), ids("manifest_full5000.json")
    out.mkdir(parents=True, exist_ok=True)
    for run in RUNS:
        a, b = rows(OLD / f"{run}.shard0of1.jsonl"), rows(rest / f"{run}.shard0of1.jsonl")
        assert set(a) == seed and set(b) == other and not set(a) & set(b) and set(a) | set(b) == full, run
        f = out / f"{run}.shard0of1.jsonl"
        f.write_text("".join(json.dumps({"cocoid": c, "caption": {**a, **b}[c]}, ensure_ascii=False) + "\n"
                             for c in sorted(full)), encoding="utf-8")
        print(f"{run}: {len(full)} rows  sha256 {hashlib.sha256(f.read_bytes()).hexdigest()}")
    gate_bytes(rest, out)
    gate_rescore(out)
    return 0


def full_only(m3: Path, out: Path) -> dict[str, int]:
    """Parity-fail path (PI-1026f Q1): no merge. M3_DIR holds all 5,000 rows per run from one environment; they are
    written to OUT unchanged in content, and the seed-42 captions that differ from coco_transfer are counted for the
    disclosure (count only)."""
    full = ids("manifest_full5000.json")
    out.mkdir(parents=True, exist_ok=True)
    diff = {}
    for run in RUNS:
        new, old = rows(m3 / f"{run}.shard0of1.jsonl"), rows(OLD / f"{run}.shard0of1.jsonl")
        assert set(new) == full, f"{run}: M3 rows do not cover manifest_full5000 exactly"
        write_rows(out / f"{run}.shard0of1.jsonl", new, full)
        n = diff[run] = sum(new[c].encode("utf-8") != cap.encode("utf-8") for c, cap in old.items())
        print(f"{run}: 5000 rows from one environment; seed-42 captions differing from coco_transfer: {n}/{len(old)}")
    return diff


def write_rows(path: Path, src: dict[int, str], keep: set[int]) -> None:
    path.write_text("".join(json.dumps({"cocoid": c, "caption": src[c]}, ensure_ascii=False) + "\n"
                            for c in sorted(keep)), encoding="utf-8")


def selftest() -> int:
    other = ids("manifest_rest2500.json")
    par = {i["cocoid"] for i in json.loads((HERE / "parity50_manifest.json").read_text())["images"]}
    with tempfile.TemporaryDirectory() as t:
        t = Path(t)
        rest, out, pdir = t / "rest2500", t / "merged", t / "parity"
        for d in (rest, pdir):
            d.mkdir()
        for run in RUNS:
            stand_in = rows(ROOT / f"data/results/coco5000/zeroshot-{run.split('-')[1]}.shard0of1.jsonl")
            write_rows(rest / f"{run}.shard0of1.jsonl", stand_in, other)
            write_rows(pdir / f"{run}.shard0of1.jsonl", rows(OLD / f"{run}.shard0of1.jsonl"), par)
        assert parity(pdir) == 0, "parity on the existing decodes must pass"
        assert merge(rest, out) == 0
        # negative cases: one changed seed-42 caption, one changed parity caption
        f = out / f"{RUNS[0]}.shard0of1.jsonl"
        m = rows(f)
        c = min(ids("manifest.json"))
        m[c] += " "
        write_rows(f, m, set(m))
        assert byte_mismatches(rest, out) == [f"{RUNS[0]}: cocoid {c} differs from coco_transfer"], "gate 1 missed it"
        print("selftest: a changed seed-42 caption is caught by gate 1")
        p = pdir / f"{RUNS[0]}.shard0of1.jsonl"
        m = rows(p)
        m[min(m)] += " "
        write_rows(p, m, set(m))
        assert parity(pdir) == 1, "parity missed a changed caption"
        print("selftest: a changed parity caption is caught by gate (b)")
        # parity-fail path: out still holds the one changed seed-42 caption, so exactly one difference is counted
        assert full_only(out, t / "full_only") == {RUNS[0]: 1, **{r: 0 for r in RUNS[1:]}}
    print("selftest OK")
    return 0


def full(m3: Path, out: Path) -> int:
    full_only(m3, out)
    return 0


COMMANDS = {"parity": parity, "merge": merge, "full": full, "selftest": selftest}

if __name__ == "__main__":
    if len(sys.argv) < 2 or sys.argv[1] not in COMMANDS:
        sys.exit("usage: w4_merge.py parity DIR | merge REST_DIR OUT | full M3_DIR OUT | selftest")
    sys.exit(COMMANDS[sys.argv[1]](*map(Path, sys.argv[2:])))
