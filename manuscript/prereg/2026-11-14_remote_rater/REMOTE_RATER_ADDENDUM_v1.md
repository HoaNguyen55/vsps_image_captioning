# Addendum: remote access for the second rater (Papers A and B), v1, 14/11/2026

**Why.** The PI wrote (LOG PI-1114g): "Người chấm thứ 2 không ở đây, bạn có thể tạo trang web public tạm để người đó truy cập vào không?" The second rater is not at the PI's laptop. Registered default (Paper B registration §17 PI-5; CC-388): the rater works in person on the PI's laptop, and the servers bind 127.0.0.1 only.

**What changes.** Only how the second rater reaches the page. Nothing in the pinned rating code or pages changes:
- `tools/obj_rater/pair_server.py` da36692d, `pair.html` 1dde2ecf, `server.py` e3beb936, `rater.html` 84a90787 stay byte-identical and keep binding 127.0.0.1 (page test E8 still holds).
- New element 1: a token gate `gate_proxy.py` (this folder; sha256 6a1c07b475670f34b12821322e9f23bb63996bfd021824713ae540f3fec4c96c) listening on 127.0.0.1:8890. It forwards only to the ONE running rater page (8792 for Paper B, 8793 for Paper A; any other target is refused). It lets a request through only with an HttpOnly, Secure, SameSite=Strict cookie that is set once from a link carrying a random 48-hex key. It forwards GET and POST /save (body of 8 KB at most) and logs method, path class (/, image, /state/, /save, other) and status only: never a body, a key or a label.
- New element 2: a Cloudflare quick tunnel, `cloudflared` 2026.11.0 (official GitHub release binary, sha256 51f7c68b57ed7269164075d7e789efce5b59355982f06392deeb037d982a51fd, kept in the home folder, no account), started with `--url http://127.0.0.1:8890`. It gives a random https://…trycloudflare.com address.

**Session procedure (each remote session).**
1. One rating server only, as before; the session start line is written as ruled (CC-367 L-f for Paper A; the GATE-SERVE line and start line for Paper B).
2. A NEW key per session (`secrets.token_hex(24)`, file mode 600); the start line records the sha256 of the key, never the key; then the gate and the tunnel are started.
3. The coordinator gives the PI one link (address plus `/?k=<key>`). The PI sends it privately to the second rater, together with the short Vietnamese instruction text ruled for that page (and, for Paper A, the ruled clarifications of the class words "bóng" and "cầu"). The PI says nothing else about the study and does not watch the rater's screen.
4. At the session end (the rater tells the PI, the PI tells the coordinator): tunnel, gate and rating server are stopped by pid; the session-end line is written as ruled and adds the gate log's line count and the counts of 403 answers.

**What leaves the laptop.** Only what the page already shows a rater in person: the page, its assignment (no caption text for Paper A; for Paper B the two captions of each pair, which the plan already shows a rater), the images of those screens, the rater's own saved state, and the rater's answers on the way back. No label file of another rater, no key.json, no other file: the rating servers refuse every private path (page test E1), and the gate adds the cookie check in front. The traffic passes through Cloudflare's relay under TLS; that relay can technically see it. Images: KTVIC test images (Paper B) and XM3600 images (Paper A) are shown to one rater for rating, the same use as in person.

**Independence.** Better than in person: the PI is not in the room. The rater works alone on their own device and sees only the page and the ruled texts.

**Disclosure in the papers.** One sentence each: the second rater worked remotely through a private, key-protected link to the same page.

**Checks run on the laptop before use (14/11):** gate against a throwaway page: no cookie 403; wrong key 403; right key 302 with the cookie; with the cookie GET / 200 and an image 200; POST to another path 403; POST /save forwarded. Tunnel end to end with the throwaway page: public address without cookie 403, with key 302, with cookie 200. Everything stopped afterwards; no listener left.
