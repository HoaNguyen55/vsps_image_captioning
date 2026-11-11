#!/usr/bin/env python
"""Local labelling server for obj_rater (127.0.0.1 only).

Serves the page, the assignment and the images; appends every click to an append-only JSON-lines file on the
Linux home filesystem. Nothing is ever rewritten or deleted: a changed answer is a new line and the last line
for a question wins.

    python3 -B tools/obj_rater/server.py --dir ~/vsps_labels/xm600_gold --annotator PI --port 8790
"""
from __future__ import annotations

import argparse
import json
import os
import re
import time
from http.server import BaseHTTPRequestHandler, ThreadingHTTPServer
from pathlib import Path
from threading import Lock

HERE = Path(__file__).resolve().parent
IMAGES = HERE.parents[1] / "data" / "datasets" / "xm3600" / "images"
LABELS = {"Y", "N", "U", "A"}
LOCK = Lock()


def load_qids(d: Path) -> dict[str, set[str]]:
    out = {}
    for name in ("assignment", "practice"):
        scr = json.loads((d / f"{name}.json").read_text(encoding="utf-8"))["screens"]
        out[name] = {q["qid"] for s in scr for q in s["q"]}
    return out


def make_handler(d: Path, annotator: str):
    qids = load_qids(d)
    files = {"assignment": d / f"labels_{annotator}.jsonl", "practice": d / f"practice_{annotator}.jsonl"}

    def state(kind: str) -> dict[str, str]:
        out = {}
        if files[kind].exists():
            for line in files[kind].read_text(encoding="utf-8").splitlines():
                r = json.loads(line)
                out[r["qid"]] = r["label"]
        return out

    class H(BaseHTTPRequestHandler):
        def log_message(self, *a):  # quiet: no per-request log, so answers are never echoed to a terminal
            pass

        def _send(self, code: int, body: bytes, ctype: str = "application/json") -> None:
            self.send_response(code)
            self.send_header("Content-Type", ctype)
            self.send_header("Content-Length", str(len(body)))
            self.send_header("Cache-Control", "no-store")
            self.end_headers()
            self.wfile.write(body)

        def do_GET(self) -> None:
            path = self.path.split("?")[0]
            if path in ("/", "/index.html"):
                return self._send(200, (HERE / "rater.html").read_bytes(), "text/html; charset=utf-8")
            if path in ("/assignment.json", "/practice.json"):
                return self._send(200, (d / path[1:]).read_bytes())
            if path in ("/state/assignment", "/state/practice"):
                with LOCK:
                    return self._send(200, json.dumps({"annotator": annotator, "labels": state(path.split("/")[2])}).encode())
            m = re.fullmatch(r"/images/([0-9a-f]{16})\.jpg", path)
            if m and (IMAGES / f"{m.group(1)}.jpg").is_file():
                return self._send(200, (IMAGES / f"{m.group(1)}.jpg").read_bytes(), "image/jpeg")
            self._send(404, b'{"error":"not found"}')

        def do_POST(self) -> None:
            if self.path != "/save":
                return self._send(404, b'{"error":"not found"}')
            try:
                r = json.loads(self.rfile.read(min(int(self.headers.get("Content-Length", "0")), 4096)))
                kind, qid, label = r["kind"], r["qid"], r["label"]
                assert kind in files and qid in qids[kind] and label in LABELS
            except Exception:
                return self._send(400, b'{"error":"bad request"}')
            rec = {"qid": qid, "label": label, "annotator": annotator, "t_server": time.strftime("%Y-%m-%dT%H:%M:%SZ", time.gmtime()),
                   "ms_on_screen": int(r.get("ms", 0))}
            with LOCK:
                with open(files[kind], "a", encoding="utf-8") as f:
                    f.write(json.dumps(rec, ensure_ascii=False) + "\n")
                    f.flush()
                    os.fsync(f.fileno())
            self._send(200, b'{"ok":true}')

    return H


def main() -> int:
    ap = argparse.ArgumentParser()
    ap.add_argument("--dir", required=True)
    ap.add_argument("--annotator", required=True)
    ap.add_argument("--port", type=int, default=8790)
    args = ap.parse_args()
    d = Path(args.dir).expanduser().resolve()
    assert not str(d).startswith("/mnt/"), "labels must be written on the Linux home filesystem"
    assert re.fullmatch(r"[A-Za-z0-9_]{1,20}", args.annotator), "annotator: letters, digits, underscore"
    ThreadingHTTPServer(("127.0.0.1", args.port), make_handler(d, args.annotator)).serve_forever()
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
