"""ERRATUM_O31_4 E4-3 (CODE_NEEDS C23): write ops5.json once, from P1's k0.json and nothing else.

    $PY -I -B ops5.py --k0 <P1 k0.json> --out <dir>

Refuses a preview (complete false or decision null), any second --k0, and an existing ops5.json. The whole result is
computed (points.extra_points, C06) before the file is created; the file is created with O_EXCL, then its sha256 is
written to ops5.json.sha256 and printed. Numbers and shas only.
"""
import argparse
import hashlib
import json
import os
import sys
from pathlib import Path

sys.dont_write_bytecode = True
sys.path.insert(0, os.environ.get("O31_SRC", str(Path(__file__).resolve().parent / "src")))  # O31_SRC: mutant runs only

from o31 import points  # noqa: E402


def main(argv=None) -> int:
    ap = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    ap.add_argument("--k0", action="append", type=Path, required=True, help="P1's k0.json (exactly one)")
    ap.add_argument("--out", type=Path, required=True)
    a = ap.parse_args(argv)
    if len(a.k0) != 1:
        raise SystemExit("REFUSED ops5.json is computed from one k0.json only (E4-3)")
    raw = a.k0[0].read_bytes()
    k0 = json.loads(raw.decode("utf-8"))
    res = points.extra_points(k0)
    body = json.dumps({"schema": points.SCHEMA, "k0_sha256": hashlib.sha256(raw).hexdigest(), **res,
                       "edge_row_E4_5": points.edge_row(k0)}, indent=1) + "\n"
    a.out.mkdir(parents=True, exist_ok=True)
    target = a.out / "ops5.json"
    if target.exists():
        raise SystemExit(f"REFUSED {target} exists: ops5.json is written once")
    fd = os.open(target, os.O_WRONLY | os.O_CREAT | os.O_EXCL, 0o444)  # refuses an existing ops5.json
    with os.fdopen(fd, "w", encoding="utf-8") as fh:
        fh.write(body)
    sha = hashlib.sha256(target.read_bytes()).hexdigest()
    (a.out / "ops5.json.sha256").write_text(f"{sha}  ops5.json\n")
    print(json.dumps({"result": res["result"], "ops5_sha256": sha}))
    return 0


if __name__ == "__main__":
    sys.exit(main())
