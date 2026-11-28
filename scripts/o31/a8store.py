"""A-8 store build (ERRATUM_O31_5 E-B6, CODE_NEEDS C13), host CPU, a separate call after P1 (run_k0 is not changed).

    $PY -I -B a8store.py --records DIR [--exclude ids.txt] --store-dir DIR --out a8.json

Reads the raw stage-1 records exactly as k0.py does (sorted *.json without a leading "_", minus the §3.5 (a)
exclusions). Writes <store-dir>/A8/sft.jsonl and a8.json (numbers and shas only; refuses to overwrite a8.json).
"""
import argparse
import hashlib
import json
import os
import sys
from pathlib import Path

sys.dont_write_bytecode = True
sys.path.insert(0, os.environ.get("O31_SRC", str(Path(__file__).resolve().parent / "src")))  # O31_SRC: mutant runs only

from o31 import a8  # noqa: E402


def main(argv=None) -> int:
    ap = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    ap.add_argument("--records", required=True, type=Path)
    ap.add_argument("--exclude", type=Path)
    ap.add_argument("--store-dir", required=True, type=Path)
    ap.add_argument("--out", required=True, type=Path)
    a = ap.parse_args(argv)
    if a.out.exists():
        raise SystemExit(f"REFUSED {a.out} exists")
    files = sorted(p for p in a.records.glob("*.json") if not p.name.startswith("_"))
    drop = set(a.exclude.read_text(encoding="utf-8").split()) if a.exclude else set()
    recs = [json.loads(p.read_text(encoding="utf-8")) for p in files]
    recs = [r for r in recs if r["file_name"] not in drop]
    res = a8.a8_store(recs, a.store_dir)
    res["inputs"] = {"n_records": len(recs), "n_excluded": len(files) - len(recs),
                     "exclude_sha256": hashlib.sha256(a.exclude.read_bytes()).hexdigest() if a.exclude else None}
    a.out.write_text(json.dumps(res, indent=1) + "\n", encoding="utf-8")
    print(json.dumps({"store": res["store"], "sft_sha256": res["sft_sha256"], "R": res["R"], "P": res["P"]}))
    return 0


if __name__ == "__main__":
    sys.exit(main())
