#!/usr/bin/env python3
"""B-D1 S0 toy environment record (run_tests.sh --env; CC-506e1). A committed file inside scripts/b_d1/, so that
b_d1.closure_check sees a real __main__ file in its own exempt folder; it replaces the stdin heredoc, whose
__main__.__file__ '<stdin>' resolved into the tree root and correctly failed the closure check. No data is read.
    python3 -X utf8 -I -B scripts/b_d1/env_toy.py WHEEL_DIR      (from the tree root)
    python3 -X utf8 -I -B scripts/b_d1/env_toy.py --closure-only  (prints CLOSURE OK after the import-time checks)"""
import argparse
import json
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))
import b_d1 as D  # noqa: E402  pin_check and closure_check run at import

if sys.argv[1:] == ["--closure-only"]:
    print("CLOSURE OK")
    sys.exit(0)
BF, FM = D.BF, D.FM
wh = Path(sys.argv[1])
a = argparse.Namespace(pyvi_wheel=str(wh / "pyvi-0.1.1-py2.py3-none-any.whl"),
                       uts_wheel=str(wh / "underthesea-9.5.0-py3-none-any.whl"))
rec = BF.env_record(a)
BF.env_check(rec)
f3 = {u: [x["equal"] for x in FM.f3(u)] for u in ("rdr", "pyvi", "uts")}
print(json.dumps({"env": rec, "F3_equal": f3}))
print("ENV OK")
