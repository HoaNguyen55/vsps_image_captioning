#!/usr/bin/env python3
"""Token gate in front of ONE local rating server, for a remote rater reached through a tunnel.

The rating server stays bound to 127.0.0.1 and is not changed. This proxy listens on 127.0.0.1:<listen>,
lets a request through only with the session cookie (set once from ?k=<token>), forwards GET and POST /save
to 127.0.0.1:<target>, and logs method, path class and status only (never a body, a query value or a label).

    python3 -I gate_proxy.py --target 8792 --listen 8890 --token-file ~/.cache/vsps_tunnel/token
"""
from __future__ import annotations

import argparse
import hmac
import http.client
import re
import sys
import time
from http.server import BaseHTTPRequestHandler, ThreadingHTTPServer
from pathlib import Path

MAX_POST = 8192
ALLOWED_TARGETS = {8792, 8793}  # Paper B pair page, Paper A second-annotator page
HOP = {"connection", "keep-alive", "transfer-encoding", "upgrade", "proxy-connection", "te", "trailer", "host",
       "cookie", "content-length", "accept-encoding"}


def make_handler(target: int, token: str, log):
    class H(BaseHTTPRequestHandler):
        protocol_version = "HTTP/1.1"

        def _authorised(self) -> bool:
            for part in (self.headers.get("Cookie") or "").split(";"):
                k, _, v = part.strip().partition("=")
                if k == "vk" and hmac.compare_digest(v, token):
                    return True
            return False

        def _plain(self, code: int, text: str, extra: dict | None = None) -> None:
            body = text.encode()
            self.send_response(code)
            for k, v in (extra or {}).items():
                self.send_header(k, v)
            self.send_header("Content-Type", "text/plain; charset=utf-8")
            self.send_header("Content-Length", str(len(body)))
            self.send_header("Cache-Control", "no-store")
            self.end_headers()
            self.wfile.write(body)

        def _cls(self) -> str:
            p = self.path.split("?")[0]
            return "image" if re.search(r"\.(jpe?g|png)$", p, re.I) else (p if p in ("/", "/save", "/assignment.json", "/practice.json", "/state/assignment", "/state/practice") else "other")

        def _forward(self, body: bytes | None) -> None:
            c = http.client.HTTPConnection("127.0.0.1", target, timeout=30)
            hdr = {k: v for k, v in self.headers.items() if k.lower() not in HOP}
            hdr["Host"] = f"127.0.0.1:{target}"
            c.request(self.command, self.path, body=body, headers=hdr)
            r = c.getresponse()
            data = r.read()
            self.send_response(r.status)
            for k, v in r.getheaders():
                if k.lower() not in HOP:
                    self.send_header(k, v)
            self.send_header("Content-Length", str(len(data)))
            self.end_headers()
            self.wfile.write(data)
            log(f"{self.command} {self._cls()} {r.status}")

        def do_GET(self) -> None:
            m = re.match(r"^/\?k=([0-9a-f]{32,64})$", self.path)
            if m:
                if not hmac.compare_digest(m.group(1), token):
                    log("GET key-wrong 403")
                    return self._plain(403, "forbidden")
                log("GET key-ok 302")
                return self._plain(302, "", {"Location": "/?practice", "Set-Cookie": f"vk={token}; Path=/; HttpOnly; Secure; SameSite=Lax"})
            if not self._authorised():
                log(f"GET {self._cls()} 403-no-cookie")
                return self._plain(403, "forbidden: open the link you were given")
            self._forward(None)

        def do_POST(self) -> None:
            n = int(self.headers.get("Content-Length") or 0)
            if not self._authorised() or self.path != "/save" or not 0 < n <= MAX_POST:
                log(f"POST {self._cls()} 403")
                return self._plain(403, "forbidden")
            self._forward(self.rfile.read(n))

        def log_message(self, *a) -> None:
            pass

    return H


def main() -> None:
    ap = argparse.ArgumentParser()
    ap.add_argument("--target", type=int, required=True)
    ap.add_argument("--listen", type=int, default=8890)
    ap.add_argument("--token-file", required=True)
    ap.add_argument("--log", default=str(Path.home() / ".cache/vsps_tunnel/gate_proxy.log"))
    a = ap.parse_args()
    if a.target not in ALLOWED_TARGETS:
        sys.exit(f"STOP: target {a.target} is not a remote-rater page {sorted(ALLOWED_TARGETS)}")
    token = Path(a.token_file).expanduser().read_text().strip()
    if not re.fullmatch(r"[0-9a-f]{32,64}", token):
        sys.exit("STOP: token must be 32-64 hex characters")
    f = open(a.log, "a", buffering=1)
    log = lambda s: f.write(f"{time.strftime('%Y-%m-%dT%H:%M:%SZ', time.gmtime())} {s}\n")
    log(f"start target={a.target} listen={a.listen}")
    ThreadingHTTPServer(("127.0.0.1", a.listen), make_handler(a.target, token, log)).serve_forever()


if __name__ == "__main__":
    main()
