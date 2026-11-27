"""K0 launcher (P0r preview / P1 verdict): `python3 -I -B k0.py --records DIR --table vintern=probes.jsonl
[--table internvl3=...] [--exclude ids.txt] --store-dir DIR --out k0.json`. -I drops the cwd from sys.path, so this
file puts ./src there itself (as test_o31.py does). VSPS_REPO names the repo snapshot (sha-checked)."""
import os
import sys
from pathlib import Path

sys.dont_write_bytecode = True
sys.path.insert(0, os.environ.get("O31_SRC", str(Path(__file__).resolve().parent / "src")))  # O31_SRC: mutant runs only

from o31 import gate  # noqa: E402

if __name__ == "__main__":
    sys.exit(gate.main())
