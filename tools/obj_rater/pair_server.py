#!/usr/bin/env python
"""Local labelling server for the pairwise caption preferences of Paper B (127.0.0.1 only).

Copy of server.py (pinned e3beb936, not edited) with the changes of B_PREF_LABELLING_PLAN_v1_1.md §9: images from
--images, KTVIC file names (.jpg, .jpeg, .png) served only if listed in test_data.json, labels A/B/T/X, pair.html,
port 8792 (8790 and 8791 refused: Paper A), no --dir under /mnt or ~/vsps_labels/, and no start unless assignment.json,
practice.json and key.json equal the sha256 in BUILD.json. key.json and BUILD.json are never served. Every click is
appended to a JSON-lines file with fsync; a changed answer is a new line and the last line for a question wins.

    python3 -B tools/obj_rater/pair_server.py --dir ~/vsps_labels_b/b_pref --annotator PI --images data/datasets/ktvic/images

Round 2 (CC-361): --dir must be under ~/vsps_labels_b/ and --annotator is PI or R2 (NB5); every image of the assignment
and practice screens must exist under --images before anything is served (D14); pair.html must carry the registered
Vietnamese instruction block byte for byte (B_PREF_INSTRUCTIONS_VI_v1.md, block sha256 45d59b54; D16), and the page
bytes checked at start are the bytes served.
"""
from __future__ import annotations

import argparse
import hashlib
import html
import json
import os
import re
import time
from http.server import BaseHTTPRequestHandler, ThreadingHTTPServer
from pathlib import Path
from threading import Lock

HERE = Path(__file__).resolve().parent
LABELS = {"A", "B", "T", "X"}
ANNOTATORS = {"PI", "R2"}  # plan §4 rater codes (CC-361 NB5)
REFUSED_PORTS = {8790, 8791}  # Paper A: XM600 server and its top-up session (CC-353 W8)
BUILD_RECORD = "BUILD.json"
PINNED_OUTPUTS = ("assignment.json", "practice.json", "key.json")
LOCK = Lock()
# manuscript/prereg/2026-11-12_b_fecert/B_PREF_INSTRUCTIONS_VI_v1.md (68466875...; CC-364): the lines strictly between its
# markers. Its byte rule: lines 1-6 = "N. " + textContent of <li> N, line 7 = textContent of the paragraph below the list.
INSTRUCTIONS_VI_SHA256 = "45d59b54ecc70e31cf142e87c251e425005b87bb9d6c928f27c809923e87d5bf"
SLOT = (b"<!--BEGIN-VI-INSTRUCTIONS-->", b"<!--END-VI-INSTRUCTIONS-->")


def sha(path: Path) -> str:
    return hashlib.sha256(path.read_bytes()).hexdigest()


def under(p: Path, root: Path) -> bool:
    return p == root or root in p.parents  # by path components: ~/vsps_labels_b is not under ~/vsps_labels


def refuse_dir(d: Path) -> None:
    """/mnt and ~/vsps_labels/ refused. The unresolved path is checked first, so ~/vsps_labels is never stat'ed."""
    labels_a = {Path.home() / "vsps_labels", Path(os.path.realpath(Path.home())) / "vsps_labels"}
    for get in (lambda: d, d.resolve):
        p = get()
        if under(p, Path("/mnt")):
            raise SystemExit("STOP: must be on the Linux home filesystem, not under /mnt")
        if any(under(p, r) for r in labels_a):
            raise SystemExit("STOP: must not be under ~/vsps_labels/ (Paper A); use ~/vsps_labels_b/")


def instructions_block(page: bytes) -> bytes | None:
    """The registered block recomputed from the page (D16): between the two SLOT markers (each exactly once) exactly six
    <li>…</li> and one <p>…</p> with no markup inside; returns "1. li1\\n" … "6. li6\\n" + "p\\n" (UTF-8), else None."""
    if any(page.count(m) != 1 for m in SLOT):
        return None
    inner = page.split(SLOT[0], 1)[1].split(SLOT[1], 1)[0].decode("utf-8")
    items = re.findall(r"<li>(.*?)</li>", inner, re.S)
    paras = re.findall(r"<p>(.*?)</p>", inner, re.S)
    if len(items) != 6 or len(paras) != 1 or any("<" in t for t in items + paras):
        return None
    lines = [f"{k}. {html.unescape(t)}" for k, t in enumerate(items, 1)] + [html.unescape(paras[0])]
    return "".join(x + "\n" for x in lines).encode("utf-8")


def check_start(d: Path, port: int, images: Path, annotator: str, labels_root: Path = Path.home() / "vsps_labels_b",
                page_path: Path = HERE / "pair.html") -> tuple[dict[str, str], bytes]:
    """Refusals before anything is served. Returns ({served file name: content type} for the listed images, the page
    bytes to serve)."""
    if port in REFUSED_PORTS:
        raise SystemExit(f"STOP: port {port} belongs to Paper A's labelling; use 8792")
    if annotator not in ANNOTATORS:
        raise SystemExit("STOP: --annotator must be PI or R2 (plan §4)")
    refuse_dir(d)
    if not under(d.resolve(), labels_root.resolve()):
        raise SystemExit("STOP: --dir must be under ~/vsps_labels_b/ (plan §6)")
    page = page_path.read_bytes()
    block = instructions_block(page)
    if block is None or hashlib.sha256(block).hexdigest() != INSTRUCTIONS_VI_SHA256:
        raise SystemExit("STOP: pair.html does not carry the registered Vietnamese instructions (D16): labelling waits")
    if not images.is_dir():
        raise SystemExit("STOP: --images is not a directory")
    rec = json.loads((d / BUILD_RECORD).read_text(encoding="utf-8"))["outputs_sha256"]
    for name in PINNED_OUTPUTS:
        if rec.get(name) != sha(d / name):
            raise SystemExit(f"STOP: {name} differs from {BUILD_RECORD}")
    test = json.loads((images.parent / "test_data.json").read_text(encoding="utf-8"))
    names = [im["filename"] for im in test["images"]]
    for kind in ("assignment", "practice"):  # D14: the laptop holds the images; all must exist before serving
        for s in json.loads((d / f"{kind}.json").read_text(encoding="utf-8"))["screens"]:
            fn = s["image"].split("/", 1)[1]
            if fn not in names or not (images / fn).is_file():
                raise SystemExit("STOP: a screen's image is not a listed KTVIC test image present under --images")
    return {n: ("image/png" if n.endswith(".png") else "image/jpeg") for n in names}, page


def load_qids(d: Path) -> dict[str, set[str]]:
    out = {}
    for name in ("assignment", "practice"):
        scr = json.loads((d / f"{name}.json").read_text(encoding="utf-8"))["screens"]
        out[name] = {q["qid"] for s in scr for q in s["q"]}
    return out


def make_handler(d: Path, annotator: str, images: Path, served: dict[str, str], page: bytes):
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
                return self._send(200, page, "text/html; charset=utf-8")  # the bytes check_start checked
            if path in ("/assignment.json", "/practice.json"):
                return self._send(200, (d / path[1:]).read_bytes())
            if path in ("/state/assignment", "/state/practice"):
                with LOCK:
                    return self._send(200, json.dumps({"annotator": annotator, "labels": state(path.split("/")[2])}).encode())
            m = re.fullmatch(r"/images/(([0-9]{11})\.(jpg|jpeg|png))", path)
            if m and m.group(1) in served and (images / m.group(1)).is_file():
                return self._send(200, (images / m.group(1)).read_bytes(), served[m.group(1)])
            self._send(404, b'{"error":"not found"}')

        def do_POST(self) -> None:
            if self.path != "/save":
                return self._send(404, b'{"error":"not found"}')
            try:
                r = json.loads(self.rfile.read(min(int(self.headers.get("Content-Length", "0")), 4096)))
                kind, qid, label = r["kind"], r["qid"], r["label"]
                if not (kind in files and qid in qids[kind] and label in LABELS):
                    raise ValueError
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
    ap.add_argument("--images", required=True, help="data/datasets/ktvic/images (test_data.json must sit beside it)")
    ap.add_argument("--port", type=int, default=8792)
    args = ap.parse_args()
    d = Path(args.dir).expanduser()
    images = Path(args.images).expanduser().resolve()
    served, page = check_start(d, args.port, images, args.annotator)
    d = d.resolve()
    ThreadingHTTPServer(("127.0.0.1", args.port), make_handler(d, args.annotator, images, served, page)).serve_forever()
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
