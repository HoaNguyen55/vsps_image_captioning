#!/usr/bin/env python3
"""Run a sha-pinned R13 script unchanged, with json taught to encode numpy scalars (np.bool_, np.float64, np.int64).

Why: r13_q2_longcap_arena.py (pinned in prereg commit 7254a39) stores a numpy bool from `d0 >= thr` and json.dumps
raises TypeError. Editing the script would break its pin, so this wrapper changes only JSON encoding: no statistic,
threshold or verdict rule is touched. The script's own sha check still runs on its unchanged bytes (__file__ = its path).
usage: python3 -E -P run_pinned_numpy_json.py /abs/path/to/pinned_script.py
"""
import json
import runpy
import sys

import numpy as np

_orig_default = json.JSONEncoder.default


def _default(self, o):
    if isinstance(o, np.generic):
        return o.item()
    return _orig_default(self, o)


json.JSONEncoder.default = _default
assert json.dumps({"a": np.bool_(True), "b": np.float64(0.5)}) == '{"a": true, "b": 0.5}'
runpy.run_path(sys.argv[1], run_name="__main__")
