"""The code closure of the C-N3D run (erratum 1 E2, CC-511 W1): every module the run imports and every non-code file
those modules read at import or call time, with sha256. Nothing of the study's data is read.

  python3 -I -B closure.py REPO NCS_DATA > CLOSURE.sha256

Two passes, united:
  static  - AST imports of every closure file, absolute and relative, dotted names to any depth, searched in the
            importing file's directory, its package, and every directory that the closure modules put on sys.path;
            an unresolved name that is neither stdlib nor installed is an error (exit 1), unless named in ALLOW.
  traced  - probe.py imports every instrument module and calls each instrument on synthetic strings under an audit
            hook; every file under REPO that it opens is listed.
RESOURCES add the registration files that the modules pin and read on the run's call path (PIN_FILES) and the
scripts/c_stage1 files that stage2.check_stage1 hashes at import. A resource that names a test set is an error
unless it is one of the two id lists admitted by CC-483r2 ruling 5 (erratum 1 E2).
"""
from __future__ import annotations

import ast
import hashlib
import importlib.util
import json
import re
import subprocess
import sys
import tempfile
from pathlib import Path

HERE = Path(__file__).resolve().parent
ENTRY = ("scripts/c_attr/c_attr.py", "scripts/c_attr/c_attr_score.py", "scripts/c_en/cen_score.py",
         "scripts/c_stage1/decode_icl.py", "scripts/c_stage1/guard.py", "scripts/c_stage1/score.py",
         "scripts/c_stage2/score2.py", "scripts/c_stage2/stage2.py", "scripts/rl_reward.py",
         "scripts/score_coco_probe.py", "scripts/xm3600_oiv7.py", "rescap/chair.py")
SEARCH = (".", "scripts", "scripts/lb", "scripts/g2b", "scripts/b1_scaling", "scripts/c_attr", "scripts/c_stage1",
          "scripts/c_stage2", "scripts/c_en", "scripts/kit_b", "scripts/grl")   # every sys.path entry they make
PIN_FILES = (  # pinned registration and id-list files read on the run's call path (decode_icl, stage2, guard PINS)
    "manuscript/prereg/2026-10-22_c_stage1/DESIGN.md",
    "manuscript/prereg/2026-10-19_b_n1_vi_leaderboard.json",
    "manuscript/prereg/2026-10-21_dev_pools/exclusion.json",
    "manuscript/prereg/2026-10-21_dev_pools/ktvic_dev299.tsv",
    "manuscript/prereg/2026-10-22_c_stage1/SHA256SUMS",
    "manuscript/prereg/2026-10-22_c_stage2/PREREG.md",
    "manuscript/prereg/2026-10-22_c_stage2/frozen_config.json",
    "manuscript/prereg/2026-10-22_c_stage2/ov_test_dev299_neardup_files.txt",
    "manuscript/prereg/2026-10-18_tier3_S2.json",
    "data/coco_probe/chair_synonyms.txt",
    "scripts/evaluate.py")    # the ROOT marker of decode_hf_vlm and decode_qwen3vl
ID_LISTS_OK = {"manuscript/prereg/2026-10-21_dev_pools/exclusion.json",
               "manuscript/prereg/2026-10-22_c_stage2/ov_test_dev299_neardup_files.txt"}
TEST_NAME = re.compile(r"(?:^|[-_./])test(?:[-_.\d/]|$)|nocaps|karpathy", re.I)
#: third-party packages of the host venv that are not installed in the laptop venv used to build the list; every one
#: is imported inside functions the N3D run does not call (decoding, training, image work). The host `closure` mode
#: imports every ENTRY module with python -I, so an import-time need of any of them fails there.
ALLOW = {n: "host venv package, lazy import off the N3D call path" for n in (
    "torch", "torchvision", "transformers", "PIL", "huggingface_hub", "open_clip", "accelerate", "tokenizers", "peft",
    "trl", "datasets", "yaml", "pyvi", "py_vncorenlp", "imagehash", "flash_attn", "qwen_vl_utils", "sklearn")}


def sha(p: Path) -> str:
    return hashlib.sha256(p.read_bytes()).hexdigest()


def installed(name: str) -> bool:
    if name in sys.stdlib_module_names or name == "__future__":
        return True
    try:
        return importlib.util.find_spec(name) is not None
    except (ImportError, ValueError):
        return False


def resolve(repo: Path, src: Path, dotted: str, level: int) -> Path | None:
    """The file of a module named from src: relative (level > 0) or searched in src's dir and SEARCH."""
    parts = dotted.split(".") if dotted else []
    if level:
        base = src.parent
        for _ in range(level - 1):
            base = base.parent
        bases = [base]
    else:
        bases = [src.parent] + [repo / d for d in SEARCH]
    for b in bases:
        p = b.joinpath(*parts) if parts else b
        for cand in (p.with_suffix(".py") if parts else None, p / "__init__.py"):
            if cand is not None and cand.is_file() and cand.resolve().is_relative_to(repo):
                return cand.resolve()
    return None


def static(repo: Path, files: set[Path]) -> tuple[set[Path], list[str]]:
    todo, seen, missing = sorted(files), set(files), []
    while todo:
        src = todo.pop()
        for node in ast.walk(ast.parse(src.read_text(encoding="utf-8"))):
            names: list[tuple[str, int]] = []
            if isinstance(node, ast.Import):
                names = [(a.name, 0) for a in node.names]
            elif isinstance(node, ast.ImportFrom):
                mod = node.module or ""
                names = [(mod, node.level)] + [(f"{mod}.{a.name}" if mod else a.name, node.level) for a in node.names]
            for dotted, level in names:
                hits = []
                parts = dotted.split(".") if dotted else [""]
                for k in range(1, len(parts) + 1):   # every package on the way down, then the module
                    hits.append(resolve(repo, src, ".".join(parts[:k]), level))
                if hits[0] is None and not level and installed(parts[0]):
                    continue
                if hits[0] is None and not (isinstance(node, ast.ImportFrom) and dotted != (node.module or "")):
                    if dotted.split(".")[0] not in ALLOW:
                        missing.append(f"{src.relative_to(repo)}: {'.' * level}{dotted}")
                    continue
                for h in hits:
                    if h is not None and h not in seen:
                        seen.add(h)
                        todo.append(h)
                        init = h.parent / "__init__.py"   # a package's __init__ runs on import
                        if init.is_file() and init.resolve() not in seen and h.parent != repo:
                            seen.add(init.resolve())
                            todo.append(init.resolve())
    return seen, sorted(set(missing))


def traced(repo: Path, data: Path) -> tuple[set[Path], set[Path]]:
    with tempfile.TemporaryDirectory() as t:
        out = Path(t) / "trace.json"
        r = subprocess.run([sys.executable, "-I", "-B", str(HERE / "probe.py"), str(repo), str(data), "--trace", str(out)],
                           capture_output=True, text=True)
        if r.returncode:
            raise SystemExit(f"probe failed:\n{r.stdout[-1500:]}{r.stderr[-1500:]}")
        tr = json.loads(out.read_text())
    mods = {Path(p) for p in tr["modules"]}
    res = {Path(p) for p in tr["opened"] if not p.endswith((".py", ".pyc")) and "/__pycache__/" not in p}
    return mods | {Path(p) for p in tr["opened"] if p.endswith(".py")}, res


def stage1_sums(repo: Path) -> set[Path]:
    rows = (repo / "manuscript/prereg/2026-10-22_c_stage1/SHA256SUMS").read_text(encoding="utf-8").splitlines()
    return {(repo / r.split(maxsplit=1)[1]).resolve() for r in rows if r.split(maxsplit=1)[1].startswith("scripts/c_stage1/")}


def main() -> None:
    repo, data = Path(sys.argv[1]).resolve(), Path(sys.argv[2]).resolve()
    t_code, t_res = traced(repo, data)
    code, missing = static(repo, {(repo / e).resolve() for e in ENTRY} | t_code | stage1_sums(repo))
    code |= {(repo / "scripts/kit_b" / p.name).resolve() for p in (repo / "scripts/kit_b").glob("*.py")}
    if missing:
        sys.stderr.write("UNRESOLVED imports (not stdlib, not installed, not in the repository):\n  "
                         + "\n  ".join(missing) + "\n")
        sys.exit(1)
    res = {p.resolve() for p in t_res} | {(repo / p).resolve() for p in PIN_FILES}
    res -= code
    bad = [str(p.relative_to(repo)) for p in res if TEST_NAME.search(str(p.relative_to(repo)))
           and str(p.relative_to(repo)) not in ID_LISTS_OK]
    if bad:
        sys.stderr.write(f"test-named resources refused: {bad}\n")
        sys.exit(1)
    print("# CODE")
    for p in sorted(code):
        print(f"{sha(p)}  {p.relative_to(repo)}")
    print("# RESOURCES")
    for p in sorted(res):
        print(f"{sha(p)}  {p.relative_to(repo)}")


if __name__ == "__main__":
    main()
