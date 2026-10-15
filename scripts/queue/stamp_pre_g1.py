#!/usr/bin/env python3
"""Stamp started_before_g1_pass metadata into result JSONs of pre-G1-v2 jobs.

Committed under `scripts/queue/stamp_pre_g1.py` per Claude 2026-10-15 00:42 UTC (#2).
Contains zero float literals in AST.
"""
from __future__ import annotations

import ast
import hashlib
import json
import socket
import sys
import time
from pathlib import Path

PRE_G1_JOBS = {
    "O-2293424": {
        "job_name": "56_multiref_s42",
        "job_started_utc": "2026-10-15T00:12:55Z",
        "patterns": ["multiref_s42-*.json"],
    },
    "O-2293440": {
        "job_name": "62_58_z_xm3600_eval",
        "job_started_utc": "2026-10-15T00:03:55Z",
        "patterns": [
            "xm3600/xm3600_zeroshot-detailed.json",
            "xm3600/xm3600_p1_s43-detailed.json",
            "xm3600/xm3600_fuse2_s42-detailed.json",
            "xm3600_oiv7.json",
        ],
    },
}


def _sha256(path: Path) -> str:
    return hashlib.sha256(path.read_bytes()).hexdigest()


def stamp_once(host: str | None = None) -> int:
    host = host or socket.gethostname()
    v2_path = Path(f"/root/outputs/g1_gate_{host}_v2.json")
    if not v2_path.exists():
        return 0
    v2 = json.loads(v2_path.read_text(encoding="utf-8"))
    v2_sha = _sha256(v2_path)
    g1_pass_utc = v2["timestamp_utc"]

    cfg = PRE_G1_JOBS.get(host)
    if not cfg:
        return 0

    count = 0
    for root in (Path("/root/ncs-data/results"), Path("/root/outputs/results")):
        if not root.exists():
            continue
        for pat in cfg["patterns"]:
            for p in root.glob(pat):
                if (
                    p.name.endswith(".preds.json")
                    or p.name.endswith(".orig.json")
                    or p.name.endswith(".provenance.json")
                ):
                    continue
                if not p.is_file():
                    continue
                sidecar = p.with_suffix(".provenance.json")
                data: dict[str, object] = {}
                if sidecar.is_file():
                    try:
                        loaded = json.loads(sidecar.read_text(encoding="utf-8"))
                        if isinstance(loaded, dict):
                            data = loaded
                    except Exception:
                        data = {}
                res_sha = _sha256(p)
                if (
                    data.get("started_before_g1_pass") is True
                    and data.get("g1_v2_gate_sha256") == v2_sha
                    and data.get("result_sha256") == res_sha
                ):
                    continue
                data["result_file"] = p.name
                data["result_sha256"] = res_sha
                data["started_before_g1_pass"] = True
                data["job_name"] = cfg["job_name"]
                data["job_started_utc"] = cfg["job_started_utc"]
                data["g1_v2_pass_utc"] = g1_pass_utc
                data["g1_v2_gate_file"] = str(v2_path)
                data["g1_v2_gate_sha256"] = v2_sha
                sidecar.write_text(json.dumps(data, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
                print(f"STAMPED_PRE_G1_SIDECAR {sidecar}")
                count += 1
    return count


def _self_check() -> int:
    src = Path(__file__).read_text(encoding="utf-8")
    tree = ast.parse(src)
    floats = [
        n.value
        for n in ast.walk(tree)
        if isinstance(n, ast.Constant) and isinstance(n.value, float)
    ]
    assert not floats, f"found float literals in AST: {floats}"
    print(json.dumps({"status": "ok", "file": str(Path(__file__).name), "sha256": _sha256(Path(__file__))}))
    return 0


def main(argv: list[str]) -> int:
    if "--self-check" in argv:
        return _self_check()
    if "--daemon" in argv:
        while True:
            stamp_once()
            time.sleep(15)
    stamp_once()
    return 0


if __name__ == "__main__":
    raise SystemExit(main(sys.argv[1:]))
