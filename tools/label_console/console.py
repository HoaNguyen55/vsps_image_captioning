#!/usr/bin/env python3
"""Labelling console for the Paper A object-gold study (127.0.0.1 only; read-only on label files).

One page for the labelling workflow, built AROUND the registered rating page (tools/obj_rater/server.py and
rater.html), which this console never changes and never replaces: where each session stands, a link to the
rating page when its server is up, file-level integrity checks, and an export of verified copies.

Custody: of a label file this program reads only its size, its line count, its last byte, its modification
time and its sha256 (whole file, and a byte prefix to test the read-only copies). It never parses a label
line, never shows a label value and computes no statistic of the labels. It writes only under
<labels root>/exports/<UTC stamp>/, never inside a session folder, and never overwrites.

    python3 -I tools/label_console/console.py                 # http://127.0.0.1:8788/
    python3 -I tools/label_console/console.py --status        # print the status JSON once
    python3 -I tools/label_console/console.py --selftest
"""
from __future__ import annotations

import argparse
import hashlib
import json
import shutil
import socket
import stat
import tempfile
import time
from http.server import BaseHTTPRequestHandler, ThreadingHTTPServer
from pathlib import Path

HERE = Path(__file__).resolve().parent
RATER = HERE.parent / "obj_rater"
CODE_PINS = {"server.py": "e3beb936", "rater.html": "84a90787"}
# key, title, folder under the labels root, annotator, port of its rating page, pin of assignment.json
SESSIONS = [
    ("base", "Bộ chính (3 phần)", "xm600_gold", "PI", 8790, "55e07337"),
    ("topup", "Buổi bổ sung", "xm600_gold_topup1", "PI", 8791, "ceb87d0b"),
    ("r2", "Phần chung của người gán nhãn thứ hai", "xm600_gold_r2", "R2", 8793, "fc8aafe9"),
]
VN = 7 * 3600


def digest(path: Path, nbytes: int | None = None) -> dict:
    """sha256, newline count and last byte of the first nbytes of a file (all of it when nbytes is None)."""
    h, lines, last, left = hashlib.sha256(), 0, b"", nbytes
    with open(path, "rb") as f:
        while left is None or left > 0:
            chunk = f.read(1 << 20 if left is None else min(1 << 20, left))
            if not chunk:
                break
            h.update(chunk)
            lines += chunk.count(b"\n")
            last = chunk[-1:]
            left = None if left is None else left - len(chunk)
    return {"sha256": h.hexdigest(), "lines": lines, "ends_newline": last in (b"", b"\n")}


def file_facts(path: Path) -> dict | None:
    if not path.is_file():
        return None
    st = path.stat()
    when = time.strftime("%d/%m %H:%M", time.gmtime(st.st_mtime + VN))
    return {"name": path.name, "bytes": st.st_size, "modified_vn": when, **digest(path)}


def copy_facts(live: Path) -> list[dict]:
    """The read-only copies made at each session end: each must be a byte prefix of the live file."""
    out = []
    for c in sorted(live.parent.glob(f"{live.stem}.*.jsonl")):
        n = c.stat().st_size
        prefix_ok = n <= live.stat().st_size and digest(c)["sha256"] == digest(live, n)["sha256"]
        read_only = stat.S_IMODE(c.stat().st_mode) & 0o222 == 0
        out.append({"name": c.name, "bytes": n, "prefix_of_live": prefix_ok, "read_only": read_only})
    return out


def totals(path: Path) -> dict | None:
    """Screens and questions of an assignment or practice file (counts only)."""
    if not path.is_file():
        return None
    screens = json.loads(path.read_text(encoding="utf-8"))["screens"]
    return {"screens": len(screens), "questions": sum(len(s["q"]) for s in screens)}


def listening(port: int) -> bool:
    with socket.socket() as s:
        s.settimeout(0.3)
        return s.connect_ex(("127.0.0.1", port)) == 0


def short_sha(path: Path) -> str:
    return digest(path)["sha256"][:8] if path.is_file() else "absent"


def session_status(root: Path, key: str, title: str, folder: str, who: str, port: int, pin: str) -> dict:
    d = root / folder
    live = d / f"labels_{who}.jsonl"
    labels, total = file_facts(live), totals(d / "assignment.json")
    copies = copy_facts(live) if labels else []
    checks = [("assignment.json đúng mã ghim " + pin, short_sha(d / "assignment.json") == pin)]
    if labels:
        checks.append(("dòng cuối của tệp nhãn đã ghi trọn", labels["ends_newline"]))
        checks.append(("mọi bản sao chỉ đọc là phần đầu của tệp nhãn (chỉ ghi nối thêm)",
                       all(c["prefix_of_live"] and c["read_only"] for c in copies)))
    return {"key": key, "title": title, "annotator": who, "port": port, "page_up": listening(port),
            "exists": d.is_dir(), "total": total, "practice_total": totals(d / "practice.json"),
            "labels": labels, "practice": file_facts(d / f"practice_{who}.jsonl"), "copies": copies,
            "checks": [{"name": n, "ok": bool(ok)} for n, ok in checks]}


def status(root: Path) -> dict:
    sessions = [session_status(root, *s) for s in SESSIONS]
    by = {s["key"]: s for s in sessions}
    r2 = by["r2"]
    r2_done = bool(r2["labels"] and r2["total"] and r2["labels"]["lines"] >= r2["total"]["questions"])
    code = [{"name": f"{name} đúng mã ghim {pin}", "ok": short_sha(RATER / name) == pin}
            for name, pin in CODE_PINS.items()]
    return {"now_vn": time.strftime("%d/%m/%Y %H:%M:%S", time.gmtime(time.time() + VN)), "sessions": sessions,
            "code_checks": code, "agreement_data_ready": bool(by["base"]["labels"]) and r2_done}


def export(root: Path, stamp: str | None = None) -> dict:
    """Copy every label and practice file to a new read-only folder and verify each copy by sha256."""
    stamp = stamp or time.strftime("%Y%m%dT%H%M%SZ", time.gmtime())
    dest = root / "exports" / stamp
    dest.mkdir(parents=True, exist_ok=False)  # an existing export is never overwritten
    rows = []
    for _key, _title, folder, who, _port, _pin in SESSIONS:
        for src in (root / folder / f"labels_{who}.jsonl", root / folder / f"practice_{who}.jsonl"):
            if not src.is_file():
                continue
            before = digest(src)
            out = dest / folder / src.name
            out.parent.mkdir(exist_ok=True)
            shutil.copyfile(src, out)
            out.chmod(0o444)
            if not (digest(out)["sha256"] == before["sha256"] == digest(src)["sha256"]):
                raise OSError(f"export of {src.name} did not verify; folder {dest} must not be used")
            rows.append((f"{folder}/{src.name}", before["lines"], out.stat().st_size, before["sha256"]))
    manifest = "file\tlines\tbytes\tsha256\n" + "".join("\t".join(map(str, r)) + "\n" for r in rows)
    (dest / "MANIFEST.tsv").write_text(manifest, encoding="utf-8")
    (dest / "MANIFEST.tsv").chmod(0o444)
    return {"folder": str(dest), "files": [{"file": r[0], "lines": r[1], "sha256": r[3]} for r in rows]}


def make_handler(root: Path):
    page = (HERE / "console.html").read_bytes()

    class H(BaseHTTPRequestHandler):
        def log_message(self, *a):
            pass

        def _send(self, code: int, body: bytes, ctype: str = "application/json") -> None:
            self.send_response(code)
            self.send_header("Content-Type", ctype)
            self.send_header("Content-Length", str(len(body)))
            self.send_header("Cache-Control", "no-store")
            self.end_headers()
            self.wfile.write(body)

        def _local(self) -> bool:  # refuse requests that reach this port under another host name
            return self.headers.get("Host", "").split(":")[0] in ("127.0.0.1", "localhost")

        def do_GET(self) -> None:
            path = self.path.split("?")[0]
            if not self._local():
                return self._send(403, b'{"error":"forbidden"}')
            if path in ("/", "/index.html"):
                return self._send(200, page, "text/html; charset=utf-8")
            if path == "/api/status":
                return self._send(200, json.dumps(status(root), ensure_ascii=False).encode())
            self._send(404, b'{"error":"not found"}')

        def do_POST(self) -> None:
            # the custom header keeps another site open in the same browser from triggering an export
            if not self._local() or self.path != "/api/export" or self.headers.get("X-Console") != "1":
                return self._send(403, b'{"error":"forbidden"}')
            try:
                self._send(200, json.dumps(export(root), ensure_ascii=False).encode())
            except OSError as e:
                self._send(500, json.dumps({"error": str(e)}, ensure_ascii=False).encode())

    return H


def selftest() -> None:
    """Synthetic files only (made here, in a temporary folder); no real label file is touched."""
    with tempfile.TemporaryDirectory() as tmp:
        root = Path(tmp)
        d = root / "xm600_gold"
        d.mkdir()
        screens = {"screens": [{"q": [{"qid": "a"}, {"qid": "b"}]}, {"q": [{"qid": "c"}]}]}
        (d / "assignment.json").write_text(json.dumps(screens))
        (d / "practice.json").write_text(json.dumps({"screens": [{"q": [{"qid": "p"}]}]}))
        live = d / "labels_PI.jsonl"
        live.write_bytes(b"line1\nline2\n")
        good = d / "labels_PI.20260101T000000Z.jsonl"
        good.write_bytes(b"line1\n")
        good.chmod(0o444)
        s = status(root)["sessions"][0]
        assert s["total"] == {"screens": 2, "questions": 3} and s["practice_total"]["questions"] == 1
        assert s["labels"]["lines"] == 2 and s["labels"]["ends_newline"]
        assert s["copies"] == [{"name": good.name, "bytes": 6, "prefix_of_live": True, "read_only": True}]
        assert [c["ok"] for c in s["checks"]] == [False, True, True]  # the synthetic assignment is not the pin
        assert status(root)["sessions"][1]["labels"] is None and not status(root)["agreement_data_ready"]

        sha_before = digest(live)["sha256"]
        e = export(root, "T1")
        out = root / "exports" / "T1" / "xm600_gold" / "labels_PI.jsonl"
        assert out.read_bytes() == live.read_bytes() and stat.S_IMODE(out.stat().st_mode) == 0o444
        assert e["files"] == [{"file": "xm600_gold/labels_PI.jsonl", "lines": 2, "sha256": sha_before}]
        assert digest(live)["sha256"] == sha_before, "export changed a label file"
        try:
            export(root, "T1")
            raise AssertionError("a second export under the same stamp must be refused")
        except FileExistsError:
            pass

        bad = d / "labels_PI.20260102T000000Z.jsonl"  # a copy that is not a prefix = the live file was rewritten
        bad.write_bytes(b"lineX\n")
        with open(live, "ab") as f:
            f.write(b"torn")  # a last line without its newline = an interrupted write
        s = status(root)["sessions"][0]
        assert [c["prefix_of_live"] for c in s["copies"]] == [True, False]
        assert [c["ok"] for c in s["checks"]] == [False, False, False]
    print("selftest ok: 14 assertions")


def main() -> int:
    ap = argparse.ArgumentParser()
    ap.add_argument("--root", default=str(Path.home() / "vsps_labels"))
    ap.add_argument("--port", type=int, default=8788)
    ap.add_argument("--status", action="store_true")
    ap.add_argument("--selftest", action="store_true")
    args = ap.parse_args()
    root = Path(args.root).expanduser().resolve()
    if args.selftest:
        selftest()
    elif args.status:
        print(json.dumps(status(root), ensure_ascii=False, indent=1))
    else:
        assert args.port not in (8790, 8791, 8792, 8793, 8890), "these ports belong to the rating pages and the gate"
        ThreadingHTTPServer(("127.0.0.1", args.port), make_handler(root)).serve_forever()
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
