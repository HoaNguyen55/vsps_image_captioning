# Paper A: remote-mode delta to the R2 session runbook (2026-11-18)

This is a read-only draft by an agent for the coordinator. Nothing in it has been run:
- no server, gate or tunnel was started and no port was called;
- no LOG line was written;
- nothing under `~/vsps_labels*` was listed or opened.

The writer hashed only the files named in the source table, and the session sheet draft this file introduces.

Custody: this file carries design, registered rules, constants, LOG ids and file shas only. It carries no outcome, no verdict word, no count per class or role and no agreement figure. It carries no address, key, host name or IP.

**Base.** This file amends `manuscript/A_SESSION_RUNBOOK_2026-11-16.md` (sha256 d29a0b5a8cf1e5ca872ae24f64c21a4887915a77e054e3495889eb4f8cf1211d, commit 90b7659, CC-437 CONDITIONAL GO 87) for ONE purpose: to run the R2 session REMOTELY under `REMOTE_RATER_ADDENDUM_v1_1.md` (add91ba3; CC-398 CONDITIONAL GO 87; commit aee9520).

Every rule of the runbook that this file does not name stays as written. Part B (top-up), Part C (closing) and section E stand unchanged, except where section 3 below says otherwise.

**Why.** On PI-1118t (2026-11-18T06:43:58Z), item D-7, the PI wrote: "8h30 tối nay người gán nhãn hai sẽ bắt đầu thực hiện, bạn cần chuẩn bị 1 link có thể access qua internet bởi vì người gán nhãn sẽ không được quyền access vào máy hiện tại." CC-437 ruling 1 allowed in-person mode only because the reason of CC-398 (R2 is not at the laptop) was gone under PI-1116b. That reason is back. No R2 answer of Paper A exists yet: there is no `-xm600-r2-start` line on the LOG, so the choice is again made before the data.

**Status.** Ruled by CC-452, a three-judge panel (J1 87, J2 86, J3 86; each CONDITIONAL GO; IRREVERSIBLE, bar 85). This file is the merged end state of their BLOCKING items and of the non-blocking items taken (merge report `manuscript/MERGE_REPORT_CC452_2026-11-18.md`). Nothing in it may be run until each judge has confirmed this file's sha by byte match, the chair has written CC-452 with that sha, and every precondition of section 0 holds.

## 0. Preconditions before the start line (CC-452)

Each is a record or an act, not a text edit. Any one missing = no start line.

- **P-1. Named tunnel service off** (J1 B6, J2 ruling 2, J3 B7). The PI runs `sudo systemctl disable --now cloudflared` himself (M-0R item 1, the command on its own line). His line "Đã tắt dịch vụ cloudflared" is logged verbatim as a PI line, and R-A1 prints inactive, disabled and no cloudflared process. Deadline 19:00 VN (J3 B7, the earliest of the three; J1 and J2 also ask for it before 19:00): if R-A1 has not passed by then, there is no start tonight and the PI is told at 19:00 that the session is postponed. The service stays disabled until the end line of the PI's top-up session (J2 N1, J3 N2).
- **P-2. This file at its merged sha, confirmed and committed** (J1 B5(i), J2 J11, J3 B8). Each judge confirms the sha by byte match; the chair writes CC-452 naming it; the file is committed through the gatekeeper, one path, staged blob equal to that sha, no attribution line; R-A2's committed check passes.
- **P-3. The remote sheet on record** (J1 B5(ii), J3 B5). `~/vsps_handoff/HUONG_DAN_PHIEN_R2_baiA_REMOTE.txt` at sha256 7deda0926afc630ae0f258e2bcdd0d6bb99501eade0b477b7edc8be30973a24c (J1 N1 text of item 9, taken verbatim), set to mode 444 and re-hashed equal, after each judge has confirmed that sha. Its exact bytes go into the chair's CC-452 file as an annex with an extraction command (the CC-437 Annex S form). R-A2 expects that sha.
- **P-4. M-0R answered** (J1 B5(iii), J2 J11, J3 B8). The merged M-0R of R-A0 is sent at once; the PI's answer is logged verbatim as a PI line stamped by `date -u` before R-A2, and its id goes into the R-A2 loop.
- **P-5. No bulk transfers and no WSL restart** (J1 B7). From the start line to the end line, no agent runs bulk transfers on the laptop (rclone, rsync or scp to or from a rented host, large copies on /mnt/d) and no one restarts WSL. Jobs on the rented host itself may run. Before the start the coordinator tells the host agents and every active agent, and the supplement line of R-A3 records it. M-0R item 2 asks the same of the PI.
- **P-6. clipmsg dummy run** (J2 B5). The coordinator re-runs the dummy extraction of R-A4 on this file's block, in the scratch folder only, with no clipboard, before the session (the merge ran it once; merge report).
- **P-7. No P1 pre-flight** (J9 result, section 7).
- **P-8. No stale address file.** `$ST/url` exists at merge time (an earlier session's dead address; existence checked only, never read). Run `rm -f $ST/url` before R-A2, whose `url-absent` check needs it gone. Every `$RS end` in this file (R-A5, R-A7 stop for the day, R-A8, D3, D9, D11, D18 to D20, P2) is followed by `rm -f $ST/url`, so the check also holds at a resume or a second attempt.

## Sources read (sha256, first 8 hex)

| Source | sha256 |
|---|---|
| runbook A_SESSION_RUNBOOK_2026-11-16.md (in full) | d29a0b5a |
| REMOTE_RATER_ADDENDUM_v1.md / v1_1.md (in full) | a53e216f / add91ba3 |
| gate_proxy.py, repo copy and `~/.cache/vsps_tunnel/gate_proxy.py` (in full) | 353bb6e7 (both) |
| `~/.cache/vsps_tunnel/remote.sh` (in full) / `remote.sh.bak_20261115_dnswait` (diff only) | 298ca2ed / e6d3b2fa |
| `~/.cache/vsps_tunnel/cloudflared` | 51f7c68b |
| `~/.cache/vsps_tunnel/annexA.py`, `annexB.sh` (in full; the CC-398 annex extractors) | 191f7494, d4e137f6 |
| CC-398 (rulings 3 to 7, W1 to W6, N1 to N7, the PI section) | 7bf8ec54 |
| CC-437 (header, rulings 1 to 18) | b9915d03 |
| CC-367 (ruling 3, N4) | f37090f5 |
| CC-397 (W3, ruling 3 DELIVERY, ADDENDUM 1) | cd66055b |
| CC-415 (LOG line) | d24a1b59 |
| `tools/obj_rater/server.py` (l.21-22, l.55-90) / `rater.html` (l.70-75) | e3beb936 / 84a90787 |
| session sheet `~/vsps_handoff/HUONG_DAN_PHIEN_R2_baiA.txt` / card `THE_LUU_Y_HAI_TU_baiA.txt` | a5cece2e / eaad2dab |
| repo `manuscript/prereg/2026-11-11_xm600_gold_completion/practice.json` (hashed only; `remote.sh practice-check` reads it) | e0ed805b |

LOG lines read:
- PI-1114g, CC-398, OPS-1114ag (W1, W2, W4, W5 closed), OPS-1114ah (W3, commit aee9520);
- OPS-1115b-b-remote-start-failed, OPS-1115c-b-pref-start, PI-1115g, PI-1115h, INC-1115a-ungated-tunnel, INC-1115b-r2-main-without-practice, CC-415, OPS-1115w-b-pref-session-end, OPS-1115x-r2-in-person-correction, PI-1115i, PI-1115l, PI-1115m, PI-1115n;
- PI-1116b, PI-1116d, CC-437, OPS-1115ck-a-runbook, PI-1118e-m0, PI-1118q-r2, PI-1118t.

---

## 1. Found at writing time (2026-11-18 about 06:50Z, 13:50 VN): BLOCKING before any start

**F1. The root `cloudflared` service is ACTIVE and ENABLED.** It is the INC-1115a named tunnel:
- `systemctl is-active cloudflared` = active, `is-enabled` = enabled;
- the process is root-owned, started 2026-11-17 22:07 VN, `--no-autoupdate tunnel run --token-file /etc/cloudflared/token`;
- its journal shows registered edge connections.

At both of its starts its journal says it had no ingress rules (503 for every request) and it has logged no configuration update since; but ingress can be pushed from the Cloudflare side at any moment, and it could then route to any local port, 8793 or the dashboard included. This has three consequences:
1. `remote.sh start` dies at step 1. `procs()` matches every process named `cloudflared`, and the addendum (steps 1 and 9) forbids any other tunnel.
2. The in-person A2 check (`systemctl is-active` expected inactive) and the top-up B1 `ps` check also fail.
3. The coordinator cannot stop a root service (runbook D2).

The PI must run, himself, before 19:00 VN:

```bash
sudo systemctl disable --now cloudflared
```

This stops the service and keeps it off after a restart. It is reversible: `sudo systemctl enable --now cloudflared`, but only after the coordinator reports that both R2's session and the PI's top-up session have their end lines (runbook B1's `ps` check also refuses while it runs). Do not loosen `procs()`.

**F2. 8793 also listens on the laptop's loopback** (the INC-1115b lesson: Paper B's R2 answers were saved through loopback, not through the gate). The rating server binds 127.0.0.1 and serves anyone at the laptop without a key and without practice. The guard is label-free. Each POST /save that returns 200 appends exactly one line (`server.py` l.73-88). The gate logs one `POST /save 200` line per forwarded save (`gate_proxy.py` `_forward`). So the R2 lines added in a session should equal the gate's `POST /save 200` count. The monitor of R-A5b checks this.

**F3. The Paper A branch of `remote.sh` has never run.** Only the Paper B branch ran (OPS-1115c). Checked here by reading only:
- it starts `server.py` by absolute path, and `server.py` resolves the image folder from `__file__` (l.21-22), so the working directory does not matter;
- its start line holds "R2 finished all screens …" only in the end line;
- its end line holds the literal `R2 finished all screens yes|no` and the full sha of the 444 copy, which is what `a_cert_perann.py` `gate_lines()` (l.278-286) requires.

Not checked (no run): its behaviour end to end. Step 3 fetches the page body but no image, so a broken image path would first show in front of R2. The early real start of section 7 limits that risk.

**F4. Three `die` paths in `remote.sh start` leave processes running**, because they skip `stop_all`:
- "server is not for R2" leaves the server up;
- "gate did not start" leaves the server and possibly the gate;
- "no tunnel address" leaves the server, the gate and a cloudflared process with no pid file.

The DNS-wait path and the pre-link-check path do call `stop_all` (the OPS-1115b fix). The manual clean-up is in R-A3.

**F5. The address leaks to the screen in one helper.** `remote.sh practice-check` prints "M2 may be sent with: <address>/" to stdout. Pipe it through the mask in R-A7. `remote.sh start` prints no address, and its start line holds none.

**F6. The link in M1 is followed by a period.** In M1 the text "<ĐƯỜNG DẪN>." puts a "." right after the key. If R2's messaging app makes the "." part of the link, the path becomes `/?k=<key>.`, which fails the gate's pattern `^/\?k=([0-9a-f]{32,64})$`. R2 then gets "forbidden: open the link you were given" and cannot enter. The writer checked this with a dummy link through the extraction helper of R-A4 (`https://DUMMY/?k=0000.`). See question J4.

---

## 2. Keep / replace / drop, over the runbook

| Runbook part | Remote mode |
|---|---|
| §0 Ports | Keep, with these changes. 8890 is R2's gate during R2's session only; at every other time it must not run. 8787, 8788 and 8795 may stay up (J10): the gate refuses any target but 8792 and 8793 at start (`ALLOWED_TARGETS`), and the quick tunnel points at 127.0.0.1:8890 only. |
| §0 Pins | Keep. Add: `remote.sh` 298ca2ed; gate 353bb6e7 (repo and home copy); cloudflared 51f7c68b; addendum v1.1 add91ba3; this delta (its sha at the ruling); the remote sheet 7deda092 (CC-452 J3; item 9 as J1 N1; full sha in section 0 P-3 and section 5). |
| §0 Helpers | REPLACE "Do NOT use `remote.sh`". Use `remote.sh start A`, `practice-check A` and `end A`, unchanged at 298ca2ed. Do NOT use `sessions.sh r2-end` for R2: it stops the server only, not the tunnel and the gate in the ruled order, and writes no gate counts. `sessions.sh topup-*` is unchanged. |
| "Before the first session" items 1-4 | Item 1: keep; add that this delta is ruled and committed (J11). Item 2: the remote sheet at 7deda092 (CC-452 J3). Item 3: M-0 (PI-1118e-m0) was answered for the in-person mode; M-0R (R-A0) replaces it and needs its own answer. Item 4: R-A2 replaces A1 and A2. |
| "Mode: in person …" paragraph | REPLACE. Mode: remote under addendum v1.1 steps 1 to 9 and CC-398 W6, on PI-1118t D-7, by the ruling on this delta. CC-367 r3 (operator header check), CC-367 N4, CC-397 W3 (room rules) and the CC-397 r3 delivery are again superseded "for R2 only", as the addendum names them. The CC-437 rulings carry over as section 3 says. |
| A0 M-0 | REPLACE by M-0R (R-A0). |
| A1 screen hygiene | REPLACE. R2 never sees the laptop, so the ports need not be stopped for R2's view. Instead, F1 (service disabled) and the R-A2 checks apply. |
| A2 preconditions | REPLACE by R-A2 (same checks plus the remote ones). |
| A3 start and start line | REPLACE by `remote.sh start` (CC-398 r5 line form), then one supplement line (R-A3). |
| A4 Notepad windows, M-A1, M-A2 | REPLACE. The card and the remote sheet open in Notepad for the PI to copy. M1 goes on the Windows clipboard (R-A4). M-A1 and M-A2 are dropped; their conduct items are in M-0R. |
| A5 practice watcher | KEEP its logic and the 69 threshold. On exit 9 it stops the tunnel, then the gate, then the server (R-A5). |
| A5 practice-done line | KEEP the form. The basis changes from the PI's own sight of the end text to R2's report relayed by the PI (J6). |
| M-A3 main address | REPLACE by M2 on the clipboard (R-A7). |
| A5b monitor | REPLACE by the remote monitor (R-A5b). |
| A6 main set | KEEP: no `/state` call, no request to 8793 and none through the tunnel (addendum step 6), `wc -l` only. |
| A7 breaks and resume | Breaks: remote sheet item 8; no PI report. Stop for the day: `remote.sh end A <id> no`. Resume: R-A2 with the files-present checks of A7, then `remote.sh start` (a NEW key and address; the link opens practice, which shows its end message at once), then M1 again and M2 (addendum step 5). |
| A8 session end | REPLACE `sessions.sh r2-end` by `remote.sh end`. The 8787/8788 restart is not needed. The notes line takes the remote form. M-A4 becomes M-A4R (R-A8). |
| A9 confirmations | REPLACE by A9R (R-A9; J7). |
| Part B (top-up) | KEEP. It starts only after R2's session-end line, with no gate or tunnel process (addendum step 9; runbook B1 checks it). B1's `ps` check needs F1 done. |
| Part C | KEEP. |
| D table | See section 6. |

---

## 3. CC-437 rulings: what carries over (for the judge to confirm)

| CC-437 ruling | Remote mode |
|---|---|
| 1 in person | REPLACED: remote under addendum v1.1. The disclosure question is J2. |
| 2 chat window minimized | Moot. R2 does not see the laptop. The PI keeps the chat window open (closing it ends the coordinator, the watcher and the monitor). |
| 3 session sheet a5cece2e | The in-person sheet is not used. A remote sheet is a third text beside the card, M1 and M2, which CC-398 W6 forbids without a ruling. See J3. |
| 4 stop 8787/8788/8795 | Moot for R2's view (J10). The H-4 bar on telling R2 anything stays. |
| 5 practice first by the address handed out plus the watcher; D3 bound (at most 20 lines, first event) | KEEP. Addendum step 5 and 7 already give the same order. D3 restart = end line `no`, then a new remote start (R-A5). |
| 6 resume forms | KEEP (addendum step 4: the start line gives wc and sha of R2's files). The resume has no PI header check; R2 checks the header (M1). |
| 7, 11, 13 (top-up, release, rare cases) | KEEP. |
| 8 breaks | KEEP the 30-minute rule and the screen-completion rule, through the remote sheet; the PI has nothing to report. |
| 9 confirmations, "yes" rule | Changed. The PI cannot witness who rated, alone, without AI. See J7. "yes" needs at least 1,110 lines AND R2's relayed end report (J6). |
| 10 the PI never opens 8793 | KEEP and widen (addendum step 6): he opens neither the link, nor the main address, nor localhost:8793, on any device. |
| 12 partial labels not used | KEEP. |
| 14 deviations | See section 6. |

---

## 4. The remote procedure

Shell variables. These are the runbook §0 lines, plus the following:

```bash
TD=$HOME/.cache/vsps_tunnel; ST=$TD/state; RS=$TD/remote.sh; LINKF=$TD/LINK_FOR_PI.txt
ADD=$REPO/manuscript/prereg/2026-11-14_remote_rater/REMOTE_RATER_ADDENDUM_v1_1.md
RSHEET=$HOME/vsps_handoff/HUONG_DAN_PHIEN_R2_baiA_REMOTE.txt
DELTA=manuscript/A_SESSION_RUNBOOK_REMOTE_DELTA_2026-11-18.md
```

### R-A0. Advance message M-0R (send at once; the start waits for the answer)

> PI: phiên của người gán thứ hai (R2) bài A tối nay sẽ làm TỪ XA, qua một đường dẫn riêng có khoá, theo phụ lục v1.1 đã được duyệt (CC-398), vì R2 không dùng máy của PI (PI-1118t). Xin đọc và làm:
> 1. Ngay khi đọc tin này, chậm nhất 19:00: mở một cửa sổ WSL và gõ đúng dòng lệnh dưới đây (một dòng riêng, không thêm dấu chấm hay ký tự nào sau nó):
>
> sudo systemctl disable --now cloudflared
>
> Dịch vụ đường hầm có tên đang chạy trên máy; khi nó còn chạy, phiên từ xa không được mở. Nhật ký của dịch vụ ghi nó không có tuyến nào, nên tắt không ảnh hưởng việc gì đang dùng. Xin để tắt cho tới khi tôi báo cả phiên của R2 và phiên bổ sung của PI đều đã đóng, vì bước kiểm tra trước phiên bổ sung cũng dừng nếu dịch vụ này chạy. Muốn bật lại sau báo đó, gõ một dòng riêng:
>
> sudo systemctl enable --now cloudflared
>
> Gõ xong lệnh tắt, nhắn tôi: "Đã tắt dịch vụ cloudflared". Nếu tới 19:00 dịch vụ vẫn chưa tắt, phiên tối nay dời sang ngày khác.
> 2. Từ khoảng 19:00 cho tới khi tôi báo phiên đã đóng: máy cắm sạc, tắt chế độ ngủ, giữ mạng; không khởi động lại máy hay WSL; không chạy việc chép hay tải dữ liệu lớn trên máy này (ví dụ rclone, đồng bộ Google Drive, chép thư mục lớn); không đóng cửa sổ chat này. Tôi mở đường hầm từ khoảng 19:15 để còn thời gian thử lại; đường dẫn chỉ đến tay PI khi R2 sẵn sàng.
> 3. R2 cần một máy tính (không dùng điện thoại). Khi R2 đã ngồi trước máy của mình và sẵn sàng, gõ cho tôi: "R2 sẵn sàng". Tôi sẽ chép sẵn tin có đường dẫn vào bộ nhớ tạm (clipboard) của máy; tôi không hiện đường dẫn trong cửa sổ chat.
> 4. PI tự gửi cho R2 qua ứng dụng nhắn tin riêng, theo thứ tự, mỗi tin một lần, nguyên văn: (a) tờ "LƯU Ý VỀ HAI TỪ" (tôi mở sẵn trong Notepad); (b) tờ "HƯỚNG DẪN PHIÊN GÁN NHÃN TỪ XA" (cũng mở sẵn); (c) tin có đường dẫn (dán từ clipboard). Tắt xem trước liên kết nếu ứng dụng cho phép. Gửi xong, chép một chữ bất kỳ để thay đường dẫn trong clipboard.
> 5. PI không tự mở đường dẫn, không mở localhost:8793 trên máy này, không chuyển đường dẫn cho ai, không chia sẻ màn hình, không gọi video hay gọi điện với R2 trong lúc R2 làm.
> 6. Nếu R2 hỏi, chỉ trả lời: "Xem phần 'Cách trả lời' trên trang, tờ lưu ý hoặc tờ hướng dẫn phiên." Không nói gì về ảnh, lớp, chú thích, câu trả lời, giả thuyết hay kết quả. Ghi nhớ R2 đã hỏi gì để báo tôi sau phiên.
> 7. Khi R2 nhắn, PI chỉ chuyển cho tôi đúng một trong các dòng: "R2 báo trang đã hiện Xong vòng làm quen"; "R2 báo trang không đúng hoặc không tải được"; "R2 báo đã xong tất cả các ảnh, trang đã hiện Đã trả lời hết các câu"; "R2 báo dừng, chưa xong".
> 8. Phiên bổ sung (top-up) của PI chỉ mở sau khi tôi đã ghi dòng kết thúc phiên của R2.
> 9. Sau khi R2 xong, tôi sẽ nhờ PI xin R2 tự viết vài câu bằng lời của mình về cách đã làm; PI chuyển nguyên văn cho tôi. Xin không đưa câu mẫu nào cho R2. Thiếu các câu đó thì nhãn chờ một thẩm định trước khi dùng.
> 10. Nếu tới 20:20 đường hầm vẫn không mở được (hai lần thử), phiên dời sang ngày khác; không dùng cách nào khác để R2 vào trang.
> Nếu đồng ý, xin gõ: "Đã đọc M-0R".

Log his answer as a PI line, verbatim, stamped by `date -u` (as CC-437 W4 did for M-0).

### R-A1. The named tunnel service (replaces A1)

After his line "Đã tắt dịch vụ cloudflared":

```bash
systemctl is-active cloudflared; systemctl is-enabled cloudflared     # expected: inactive, disabled
ps -eo pid=,comm= | awk '$2=="cloudflared"'; echo "rc=$?"            # expected: no line
```

### R-A2. Preconditions (each must print the expected value; any other output = no start)

```bash
cd $REPO; ID=OPS-1118<x>; idfree $ID
ss -ltnH | awk '{print $4}' | grep -E ':(879[0-3]|8890)$'; echo "rc=$?"     # expected: no output, rc=1 (8787, 8788, 8795 may listen)
ps -eo pid=,comm=,args= | awk '$2=="cloudflared" || /gate_proxy|obj_rater\/(server|pair_server)\.py/' | grep -v awk; echo "rc=$?"  # expected: rc=1
systemctl is-active cloudflared; systemctl is-enabled cloudflared          # expected: inactive, disabled (F1)
test ! -e $LINKF && test ! -e $ST/key && echo clean                        # expected: clean
command -v clip.exe >/dev/null && echo clip-ok; test ! -e $ST/url && echo url-absent; ls data/datasets/xm3600/images | wc -l   # expected: clip-ok, url-absent, 3600 (CC-452 J1 N6; no clip.exe = no improvised hand-off: the PI is told and a one-judge diff read decides)
sha256sum $RS $TD/gate_proxy.py manuscript/prereg/2026-11-14_remote_rater/gate_proxy.py $TD/cloudflared $ADD \
          tools/obj_rater/server.py tools/obj_rater/rater.html $R/assignment.json $R/practice.json $CARD $RSHEET
#   expected: 298ca2ed, 353bb6e7, 353bb6e7, 51f7c68b, add91ba3, e3beb936, 84a90787, fc8aafe9, e0ed805b, eaad2dab,
#             7deda092 (remote sheet, CC-452; full values: runbook §0, section 0 P-3 and the ruling)
RB=manuscript/A_SESSION_RUNBOOK_2026-11-16.md; sha256sum $RB $DELTA      # expected: d29a0b5a…, <delta sha at the ruling>
for f in $RB $DELTA; do git ls-files --error-unmatch $f > /dev/null 2>&1 && git diff --quiet HEAD -- $f && git log -1 --format="committed %h $f" -- $f || echo "STOP: $f not committed at this state"; done
test ! -e $R/labels_R2.jsonl && test ! -e $R/practice_R2.jsonl && echo absent        # expected: absent (first session)
grep -cE '^[0-9T:-]{19}Z \| OPS-[0-9a-z]+-xm600-r2-start \|' "$LOG"                  # expected: 0 (first session)
echo "$(wc -l < $A/labels_PI.jsonl) $(sha256sum < $A/labels_PI.jsonl | cut -c1-64)"  # expected: 4681 d338896f… (CC-397 r2)
for i in OPS-1114ac-xm600-session-end PI-1114e PI-1114f PI-1114f-verbatim CC-397 PIN-1112-a-xm600-r2 \
         OPS-1112ce-xm600-r2-commit OPS-1114ai-a-r2-card-saved OPS-1115w-b-pref-session-end CC-437 \
         CC-398 OPS-1114ah-remote-rater-commit PI-1118t CC-452 <M-0R answer id>; do
  grep -qE "^[0-9T:-]{19}Z \| $i \|" "$LOG" && echo "ok $i" || echo "MISSING $i"; done   # expected: all ok
```

If 8790 to 8793 or 8890 shows a listener, or a gate, tunnel or rating process runs: no start (D1, D2).

### R-A3. Start (the ruled remote start), and the supplement line

```bash
cd $REPO; mkdir -p $ST; $RS start A $ID $CARD > $ST/start.out 2>&1   # run as a background task of the coordinator (the DNS wait can take about 5 min; CC-452 J2 B2a)
tail -1 $ST/start.out   # once the task has ended; expected: "READY: link for the PI is in …LINK_FOR_PI.txt (mode 600)"; it prints no address.
tail -1 "$LOG" | grep -cE 'trycloudflare|\?k='                              # expected 0 (no address or key in the line)
ss -ltnH | awk '{print $4}' | grep -E ':(879[0-9]|8890)$' | sed 's/.*://' | sort | tr '\n' ' '   # expected: 8793 8890 (and 8795 if up)
```

`remote.sh` writes the start line of CC-398 ruling 5. That line already holds:
- step 1 ("nothing on 8790-8793 or 8890, no cloudflared or gate process");
- R2's files before;
- the server pid and cmdline;
- the listeners;
- the gate sha, pid, target and log;
- the key sha;
- the cloudflared sha and pid;
- the pre-link check;
- the card sha.

The runbook-era items are not in it. Write them right after, in one line (no address, key or host):

`<UTC> | ${ID}a-xm600-r2-remote-notes | Supplement to ${ID}-xm600-r2-start (written by remote.sh 298ca2ed in the CC-398 ruling 5 form): mode remote under addendum v1.1 add91ba3 (CC-398 GO 87, commit aee9520) on PI-1118t item D-7, replacing the in-person mode of CC-437 ruling 1 by CC-452 (CC sha <64hex>); runbook A_SESSION_RUNBOOK_2026-11-16.md d29a0b5a (commit 90b7659) as amended by A_SESSION_RUNBOOK_REMOTE_DELTA_2026-11-18.md sha256 <64hex> (commit <h>); checks of R-A2 at <UTC>: base labels_PI.jsonl wc -l 4681 sha256 d338896f (= OPS-1114ac); card eaad2dab (= CC-397 ADDENDUM 1); remote sheet HUONG_DAN_PHIEN_R2_baiA_REMOTE.txt sha256 7deda0926afc630ae0f258e2bcdd0d6bb99501eade0b477b7edc8be30973a24c (CC-452 J3), mode 444; remote.sh 298ca2ed; gate home copy = repo copy 353bb6e7; cloudflared 51f7c68b; service cloudflared inactive and disabled, no other cloudflared process (INC-1115a; R-A1); LOG prerequisites ok; M-0R answered: <PI id>; 8787/8788/8795 <up|down>, not gate targets; link handed to the investigator through the Windows clipboard, never shown in the chat, the LOG or any file but the mode-600 link file; P1 pre-flight not run (CC-452 J9); agents told of CC-452 J1 B7 (no bulk transfers on the laptop, no WSL restart) at <UTC>. Counts and shas only.`

**If `remote.sh start` ends without its READY line** (a STOP message of F4: "server is not for R2", "gate did not start", "no tunnel address", also "server did not start"; or a silent exit under `set -e` with no message, as at l.40, l.46, l.59 or l.62 of remote.sh when a pid lookup or a request fails; or the Bash tool timing out or being stopped during the DNS wait), clean up in the ruled order and write no start line. The start runs as a background task with its output in `$ST/start.out`, and only its last line is read (CC-452 J2 B2a). The clean-up:

```bash
for p in $(ps -u "$(id -u)" -o pid=,comm=,args= | awk '$2=="cloudflared" && /--url http:\/\/127\.0\.0\.1:8890/ {print $1}'); do kill -TERM "$p"; done
stop_port 8890 gate_proxy.py; stop_port 8793 obj_rater/server.py
rm -f $ST/key $LINKF $ST/url $ST/jar $ST/hdr $ST/body $ST/cf.pid $ST/gate.pid $ST/server.pid
ss -ltnH | awk '{print $4}' | grep -E ':(879[0-3]|8890)$'; echo "rc=$?"; test ! -e $R/labels_R2.jsonl && test ! -e $R/practice_R2.jsonl && echo absent; ps -eo pid=,comm= | awk '$2=="cloudflared"'   # expected: rc=1, absent, no cloudflared line
```

Then one DEVIATION line in the form of OPS-1115b-b-remote-start-failed (cause; nothing sent; R2 files absent; the gate log's line count). A new start uses a new id, which gives a new key and a new gate log. At most two attempts in all (D18).

### R-A4. Texts to the PI and the link hand-off (replaces A4)

1. **Open the texts for the PI to copy.** Right after the start, open the card and the remote sheet in Notepad, sha-checked, as in A4. The commands are those of A4, with `$RSHEET` in place of `$SHEET` and its ruled sha in place of a5cece2e. They are for the PI to copy into his messages. R2 never sees the laptop.
2. **Load M1 when the PI types "R2 sẵn sàng".** The coordinator puts M1 on the Windows clipboard. The text is taken from the committed addendum bytes (sha checked) with the link filled in. It is never echoed:

```bash
clipmsg() { python3 -I - "$1" "$ADD" "$TD" <<'PY' | clip.exe
import hashlib, sys
which, add, td = sys.argv[1:4]
b = open(add, "rb").read()
assert hashlib.sha256(b).hexdigest().startswith("add91ba3"), "addendum sha"
t = b.decode("utf-8")
head = f'- {which}: "'
s = t.index(head) + len(head)
msg = t[s:t.index('" (', s)]
src, ph = (f"{td}/LINK_FOR_PI.txt", "<ĐƯỜNG DẪN>") if which == "M1" else (f"{td}/state/url", "<ĐỊA CHỈ>")
assert msg.count(ph) == 1
v = open(src).read().strip()
msg = msg.replace(" " + ph + ". ", "\n" + v + "\n", 1) if which == "M1" else msg.replace(ph, v)
assert v in msg and not msg.split(v, 1)[1].startswith(".")
assert "<" not in msg
sys.stderr.write(f"{which} on clipboard, {len(msg)} characters\n")
sys.stdout.buffer.write(b"\xff\xfe" + msg.encode("utf-16-le"))
PY
}
clipmsg M1        # expected: "M1 on clipboard, <n> characters"
```

   The writer parse-checked the extraction once with a dummy link and address in the scratch folder (output decoded, no clipboard). M1 came out verbatim at 612 characters and M2 verbatim at 135 characters. By CC-452 J4 (J2 and J3 rule the own-line form; J1 accepts it when the full line is given): in M1 the link stands on its own line, with no period after it and no space before the line break; every word of M1 is unchanged. The replace turns " <ĐƯỜNG DẪN>. " into a line break, the link and a line break; `assert "<" not in msg` stops the build if that pattern is absent, and the last assert stops it if a "." follows the link. M2 is unchanged (its " ." already separates the address). This is a layout departure from M1 as written (CC-398 W6), recorded in the notes line as "M1 layout: link on its own line, no period after it (CC-452 J4)" and disclosed with the mode (section 11). The block is not indented, so that it can be pasted as it stands (CC-452 J2 N6).

3. **Send M-R1.**

> PI: tin có đường dẫn đã ở trong clipboard (dán bằng Ctrl+V). Xin gửi cho R2 theo thứ tự ở mục 4 của M-0R: tờ lưu ý, tờ hướng dẫn từ xa, rồi tin có đường dẫn. Trước khi gửi, nhìn tin dán ra: phải bắt đầu bằng "Chào bạn, đây là đường dẫn riêng để bạn chấm:", đường dẫn đứng riêng một dòng và không có gì sau nó, và đọc được tiếng Việt; nếu không đúng, đừng gửi và nhắn tôi. Gửi xong, chép một chữ bất kỳ để thay clipboard, rồi gõ: "Đã gửi M1".

### R-A5. Practice watcher (A5, with the remote stop order)

Run it in the background right after the start line. Its count logic is A5's. On violation it stops the tunnel, the gate and the server, in that order, each after a cmdline check:

```bash
R=$HOME/vsps_labels/xm600_gold_r2; ST=$HOME/.cache/vsps_tunnel/state; PID=$(cat $ST/server.pid)
stop3() { for f in cf gate server; do p=$(cat $ST/$f.pid 2>/dev/null) || continue
  tr '\0' ' ' < /proc/$p/cmdline 2>/dev/null | grep -qE 'cloudflared tunnel|gate_proxy\.py|obj_rater/server\.py .*--annotator R2' && kill -TERM "$p"; sleep 1; done; }
while :; do
  n=$( [ -f $R/practice_R2.jsonl ] && wc -l < $R/practice_R2.jsonl || echo 0 )
  if [ -e $R/labels_R2.jsonl ] && [ "$n" -lt 69 ]; then stop3
    echo "STOPPED $(date -u +%FT%TZ): labels_R2.jsonl appeared with practice_R2.jsonl at $n lines"; exit 9; fi
  if [ "$n" -ge 69 ]; then
    echo "PRACTICE COMPLETE $(date -u +%FT%TZ): practice $n; labels_R2 $( [ -e $R/labels_R2.jsonl ] && echo present || echo absent )"; exit 0; fi
  kill -0 "$PID" 2>/dev/null || { echo "SERVER GONE $(date -u +%FT%TZ)"; exit 8; }
  sleep 5
done
```

**On exit 9 (D3 remote):**
1. Run `$RS end A <id> no`. Its `stop_all` skips the dead pids; it deletes the key and writes the end line.
2. Write one INCIDENT line with `wc -l` and the sha of both R2 files.
3. If `labels_R2.jsonl` has at most 20 lines and this is the first event (CC-437 ruling 5): R-A2 in the resume form, then a new `$RS start A <new id> $CARD` (its link opens practice), then M1 on the clipboard again.
4. The PI sends M1, then the D3 sentence: "Trang phần chính bị mở sớm. Xin làm xong vòng làm quen trước."
5. Run R-A5 again.

More than 20 lines, or a second event: no restart, and a one-judge read. At a D3 restart the A7 resume check "practice must be at least 69" does not apply: practice is then incomplete by definition, and CC-437 ruling 5 governs (restart, practice completed, then main) (CC-452 J1 N10).

### R-A5b. Remote monitor (replaces A5b; background for the whole session)

It reads sockets, process lists, the gate log's line classes and `wc -l`. It calls no port.

```bash
R=$HOME/vsps_labels/xm600_gold_r2; ST=$HOME/.cache/vsps_tunnel/state; GL=$(cat $ST/gatelog.path)
SP=$(cat $ST/server.pid); GP=$(cat $ST/gate.pid); CP=$(cat $ST/cf.pid)
L0=0   # R2 lines at the start: 0 in the first session; at a resume, the sum of the two wc -l in the start line
lines() { echo $(( $( [ -f $R/practice_R2.jsonl ] && wc -l < $R/practice_R2.jsonl || echo 0 ) + $( [ -f $R/labels_R2.jsonl ] && wc -l < $R/labels_R2.jsonl || echo 0 ) )); }
gap() { echo $(( $(lines) - L0 - $(grep -c ' POST /save 200$' "$GL") - $(grep -c ', in do_POST$' $ST/gate.out) )); }
stop3() { for f in cf gate server; do p=$(cat $ST/$f.pid 2>/dev/null) || continue
  tr '\0' ' ' < /proc/$p/cmdline 2>/dev/null | grep -qE 'cloudflared tunnel|gate_proxy\.py|obj_rater/server\.py .*--annotator R2' && kill -TERM "$p"; sleep 1; done; }
while kill -0 "$SP" 2>/dev/null; do
  u=$(date -u +%FT%TZ)
  for p in 8790 8791 8792; do ss -ltnH | awk '{print $4}' | grep -qE ":$p\$" && echo "ALERT $u listener on $p"; done
  o=$(ps -eo pid=,comm= | awk -v c="$CP" '$2=="cloudflared" && $1!=c {print $1}' | tr '\n' ' '); [ -n "$o" ] && { stop3; echo "TUNNEL STOP $u: other cloudflared pid $o"; break; }
  systemctl is-active --quiet cloudflared && { stop3; echo "TUNNEL STOP $u: cloudflared service active"; break; }
  kill -0 "$CP" 2>/dev/null || { echo "ALERT EXIT $u tunnel process gone (D9)"; break; }; kill -0 "$GP" 2>/dev/null || { echo "ALERT EXIT $u gate process gone (D9)"; break; }
  if [ "$(gap)" -gt 0 ]; then sleep 10; g=$(gap); [ "$g" -gt 0 ] && { stop3; echo "LOOPBACK STOP $u: $g saved lines not seen by the gate"; break; }; fi
  sleep 20
done > $HOME/.cache/vsps_b/r2_remote_monitor.out 2>&1
```

Run the watcher (R-A5) and the monitor as background tasks of the coordinator, so that their exit is reported at once (CC-452 J2 B4). The monitor exits on TUNNEL STOP, LOOPBACK STOP and ALERT EXIT; a listener on 8790 to 8792 stays an echo.

- **LOOPBACK STOP** means a line was saved that did not pass through the gate. R2 has no access to the laptop (PI-1118t), so it was not R2 through the link. Go to D19.
- **TUNNEL STOP** (another cloudflared process, or the service active). The monitor has already stopped the tunnel, the gate and the server, and has exited. At once run `$RS end A <id> no`: its stop_all skips the dead pids and deletes the key and the link file; while any cloudflared runs it then stops at its l.96 check, before the end line, so the same id stays free. Write one INCIDENT line (wc -l and sha of both R2 files; the foreign process by pid and owner, and whether its command line names 8793 or 8890; no address). Remove the foreign process: one of this user by pid after a command-line check (INC-1115a); the root service only by the PI (`sudo systemctl disable --now cloudflared`). Then re-run `$RS end A <same id> no`, which writes the end line and the 444 copy, and run `rm -f $ST/url`. A judge before any restart (INC-1115a precedent; D20). The coordinator reads the monitor file at every message of the PI and at least every 10 minutes.
- **ALERT EXIT, "tunnel process gone" or "gate process gone".** The monitor has exited. Follow D9.
- **A listener on 8790 to 8792.** Follow D1.

A gate exception (for example a client that drops mid-reply) can lose a gate log line after the server wrote its line. The count of tracebacks through `do_POST` in gate.out absorbs those cases; an exception on any other request (an image GET) is not counted, so it cannot mask a loopback save (CC-452 J2 N4). The threshold (any unexplained line, persisting 10 s) is J8.

### R-A6. During the session (A6, unchanged in substance)

- No agent sends any request through the tunnel (addendum step 6). No `/state`, no `/save`, nothing to 8793. Only `wc -l`.
- From the start line to the end line, no agent runs bulk transfers on the laptop (rclone, rsync or scp to or from a rented host, large copies on /mnt/d) and no one restarts WSL (CC-452 J1 B7; P-5): server.py serves the images from /mnt/d, and the 9p channel has failed under heavy concurrent I/O. Jobs on the rented host itself may run.
- R2's questions reach the coordinator only as the PI's report after the session. Record them in one OPS line with the pointer that was given and no item content (D10).

### R-A7. Practice end and M2 (replaces the practice-done step and M-A3)

When the PI types "R2 báo trang đã hiện Xong vòng làm quen":

```bash
$RS practice-check A | sed -E 's#https?://[^ ]+#<address withheld>#g'   # F5: never let the address reach the screen
#   expected: "practice_R2.jsonl lines n (need >= 69); labels_R2.jsonl absent" and "M2 may be sent with: <address withheld>"
```

1. **Watcher exit 0 and the check passed.** Write the practice-done line of A5 with two wording changes:
   - "the investigator's fixed line on the page end text" becomes "R2's report of the page end text, relayed by the investigator (PI line <id>)";
   - "applied in person by CC-437 ruling 5" becomes "remote, addendum v1.1 step 5".

   Then `clipmsg M2`, then send this message:

   > PI: vòng làm quen đã được ghi nhận. Tin có đường dẫn phần chính đã ở trong clipboard. Xin gửi nguyên văn cho R2, chép một chữ bất kỳ để thay clipboard, rồi gõ: "Đã gửi M2".

2. **The watcher has not exited 0.** Answer only: "Vòng làm quen chưa đủ; xin nhắn R2 làm tiếp vòng làm quen."
3. **`labels_R2.jsonl` is present although the watcher exited 0.** This is D14. R2's report replaces the investigator's sight of the end text.

At a resume, the link opens practice, which shows its end message at once. Run `practice-check` and send M2 at once. No second practice-done line.

### R-A8. Session end (replaces A8)

The PI types one of: "R2 báo đã xong tất cả các ảnh, trang đã hiện Đã trả lời hết các câu" or "R2 báo dừng, chưa xong".

```bash
sha256sum $RS | cut -c1-8                                   # expected 298ca2ed
wc -l < $R/labels_R2.jsonl                                  # label-free check before writing "yes"
GL=$(cat $ST/gatelog.path); grep -c ' POST /save 200$' "$GL"; grep -c ', in do_POST$' $ST/gate.out
ID3=OPS-1118<y>; idfree $ID3
$RS end A $ID3 yes                                          # or: no
tail -1 "$LOG" | grep -cE 'trycloudflare|\?k='              # expected 0
ss -ltnH | awk '{print $4}' | grep -E ':(879[0-3]|8890)$'; echo "rc=$?"; ps -eo pid=,comm= | awk '$2=="cloudflared"'   # expected rc=1 and no line
rm -f $ST/url                                               # the dead address; the gate log and cf.log stay (CC-398 N4)
```

- **"yes".** Only on the PI's relayed line that R2 saw "Đã trả lời hết các câu" AND `wc -l` of at least 1,110. Otherwise write "no", ask what the page showed, and send a remaining conflict to a judge (CC-437 ruling 9).
- **The end line.** `remote.sh end` writes the CC-367 L-g line with the remote additions of CC-398 ruling 5:
  - stop order;
  - key deleted;
  - ports;
  - gate log counts;
  - cloudflared sha.

  The line holds `R2 finished all screens yes|no` and the full sha of the 444 copy (F3).
- Stop the monitor if it is still running (it ends by itself when the server pid is gone).

Session-notes line (no label read):

`<UTC> | ${ID}c-xm600-r2-session-notes | R2 session <start id> to <end id>, remote under addendum v1.1 (CC-452): the investigator's relayed end line, quoted: "<...>"; M1 sent: <PI id>; M2 sent: <PI id | not sent>; confirmation line: <PI id | pending>; R2's own line: <PI id | pending>; questions R2 asked: <n> (pointer given: page guide | card | remote sheet); gate POST /save 200 lines <n>, R2 lines added this session <m>, gate POST exceptions <k> (equal | differ by <d>); monitor ALERT lines <n> (<kinds>); key-ok 302 lines before R2's first save <n> (link preview, CC-398 N3); practice-done line <id>; M1 layout: link on its own line, no period after it (CC-452 J4); device: computer (by R2's report); deviations: <none | D ids>. No label read.`

M-A4R, to the investigator, after the end line:

> PI: tôi đã ghi dòng kết thúc phiên của R2 (<R2 đã xong toàn bộ | R2 chưa xong, sẽ làm tiếp>). Đường hầm, cổng và trang đã tắt; đường dẫn cũ không dùng được nữa. Xin làm ba việc:
> 1. Sau khi đã chuyển cho tôi lời của R2 ở mục 2, gõ cho tôi một dòng xác nhận theo mẫu tôi sẽ gửi lúc đó, đúng sự thật; có thể sửa chữ, và điều nào không đúng thì ghi rõ điều gì, trong bao nhiêu ảnh.
> 2. Nhờ R2 tự viết vài câu bằng lời của mình, gửi PI, về các ý: có tự làm một mình không; làm trên máy tính của mình không; có dùng công cụ AI, chương trình hay tra cứu không; có hỏi ai không; có ai khác nhìn hay dùng màn hình trong lúc làm không. PI chuyển nguyên văn cho tôi. Xin không đưa câu mẫu cho R2.
> 3. Từ giờ: không nói với R2 về câu trả lời nào cho tới khi tôi báo kappa đã được mở niêm phong<; vì R2 chưa xong, vẫn không nói gì về nghiên cứu với R2>.

### R-A9. Confirmations (replaces A9; J7)

**From the investigator, typed by him, quoted in a PI line.**

> Người tôi gửi đường dẫn hôm <ngày> là người gán thứ hai (R2) mô tả trong PI-1114e và PI-1114f, không phải ai khác; tôi chỉ gửi cho người đó, qua tin nhắn riêng, nguyên văn: tờ 'LƯU Ý VỀ HAI TỪ', <tờ hướng dẫn phiên từ xa,> tin có đường dẫn và tin đường dẫn phần chính; tôi không chuyển đường dẫn cho ai khác và không tự mở đường dẫn hay localhost:8793 trên máy nào; tôi không chia sẻ màn hình, không gọi video hay gọi điện và không nhìn màn hình của người đó khi người đó gán; tôi không giải thích gì ngoài việc chỉ tới phần 'Cách trả lời', tờ lưu ý và tờ hướng dẫn phiên; tôi và người đó không trao đổi về ảnh, lớp, câu trả lời hay nghiên cứu; trong phiên không ai dùng máy của tôi để mở trang gán nhãn; theo lời người đó nhắn, người đó làm một mình trên máy tính của mình, không dùng công cụ AI, chương trình hay tra cứu.

**From R2, in R2's own words.** The investigator forwards them verbatim. The investigator's template above is sent to him only after R2's words have been relayed, so that it cannot reach R2 as a model. An R2 line that repeats any coordinator text word for word is not R2's line (PI-1116b) and goes to a judge. The content points are those of M-A4R item 2, never a sentence to copy.

**Condition of use (CC-452 J7, fixed before the data; a condition of the kappa unsealing line, not of the session).** (a) The investigator's typed line with at least the clauses: to whom he sent the link; he forwarded it to no one; he did not open the link, the main address or localhost:8793 himself. (b) R2's own line, in R2's words, forwarded verbatim, on: alone; no AI tool, program or search; asked no one. It is asked for before the investigator receives his template (M-A4R), and a line that repeats any coordinator text word for word is not R2's line (PI-1116b). (c) No LOOPBACK STOP, and the notes line shows the R2 lines added not above the gate's `POST /save 200` lines plus its POST exception count. Without (a), (b) and (c), the file is not R2's data and no unsealing line is written until a one-judge read of the case; until then it is kept unopened, wc and sha only (table D17; CC-437 ruling 9 and CC-415 ruling 2, applied before the fact; CC-437 ruling 9 and CC-415 W7 "R2's line is not a gate" are overruled for the remote mode, because the investigator cannot witness and addendum v1.1 rests independence on R2's word). Any other clause with an exception goes to a one-judge diff read before the unsealing.

---

## 5. What R2 receives, in order (addendum step 5; CC-398 ruling 4)

1. The card `THE_LUU_Y_HAI_TU_baiA.txt` (eaad2dab), verbatim, in a message of its own (CC-398 ruling 4; CC-397 ADDENDUM 1). The CC-397 order "after the on-page guide" is superseded remotely by the addendum: R2 reads the card before the guide and before practice.
2. By CC-452 J3 (option (a), all three judges): the remote sheet `~/vsps_handoff/HUONG_DAN_PHIEN_R2_baiA_REMOTE.txt`, verbatim, in a message of its own.
   - Ruled sha256 7deda0926afc630ae0f258e2bcdd0d6bb99501eade0b477b7edc8be30973a24c: 13 lines, 2,982 bytes, UTF-8 NFC, LF, no trailing space, one final newline. It is the draft ef35521657afa0185748168006e1e82ba6512a4ffa1067a704b4337364ab1812 with item 9 extended by the text of CC-452 J1 N1, taken verbatim (the "forbidden" case: open the first link once more, then the page; otherwise stop and message the sender).
   - It stays mode 644 until each judge has confirmed this sha by byte match; then the coordinator sets mode 444, and its exact bytes go into the chair's CC-452 file as an annex (P-3).
   - It holds no class or image content, no address and no key.
   - It repeats M1's conduct clauses and adds: the reading order; computer only and the same browser; the header and red-warning stop; practice end; the closed guide panel on the main page; breaks; a closed window; stop for the day; a new link per session; the end text; no discussion.
   - It contradicts neither M1 nor M2.
3. M1 with the link (clipboard). Later, M2 with the main address (clipboard).
4. Nothing else. Only the pointer sentence for questions, and the D3 sentence if that case occurs.

---

## 6. Deviations: changes to table D

| # | Remote mode |
|---|---|
| D1, D5, D6, D10, D12, D13 | Unchanged. |
| D17 | Remote form (CC-452 J7; replaces the runbook row): (a) the investigator's line does not affirm its clauses: to whom he sent the link; he forwarded it to no one; he did not open the link, the main address or localhost:8793 himself; or (b) R2's own line is missing, does not affirm alone, no AI tool, program or search, and asked no one, or repeats a coordinator text word for word; or (c) a LOOPBACK STOP occurred, or the R2 lines added exceed the gate's `POST /save 200` lines plus its POST exception count. The file is not R2's data until a one-judge read; kept unopened, wc and sha only; no kappa unsealing line. |
| D2 | Now open (F1). The service is disabled by the PI before R-A2. The usability table is unchanged. |
| D3 | Remote action of R-A5 (end line `no`, then a new start with a new key). Bound and disclosure as CC-437 ruling 5. |
| D4 | Top-up only; unchanged. |
| D7 | Wrong person. The PI cannot see who rates. Detected only by R2's or the PI's statements, or by D19. The action is unchanged. |
| D8 | Also covers a screen share or a video call while R2 rates, and the PI opening the link or the address. Action unchanged (one-judge diff read before use). |
| D9 | R2 reports a broken page through the PI, or the monitor reports the tunnel or gate gone. Action: `$RS end A <id> no`. Find the cause and log it. Then a new start (resume form) the same evening if the cause is known (tunnel drop, sleep, network). Acknowledged answers are safe: the page advances only after the server's 200 (CC-398 ruling 3). |
| D11 | A WSL restart kills the tunnel, the gate and the server. Run `rm -f $ST/cf.pid $ST/gate.pid $ST/server.pid` (after a restart the old pids may belong to new processes), then write the end line `no` by `$RS end`, then resume. 8787 and 8788 coming back is harmless remotely. |
| D14 | R2's relayed report replaces the investigator's sight of "Xong vòng làm quen". If R2 cannot affirm it: a one-judge diff read before the kappa unsealing. |
| D15, D16 | Not applicable (no PI header check, R2 not at the laptop). A PI look at R2's screen falls under D8. |
| D18 (new) | `remote.sh start` fails (DNS wait, pre-link check, F4). Clean up (R-A3), write one DEVIATION line, and retry with a new id. At most two attempts. If none succeeds by 20:20 VN, tell the PI the session is postponed. No other tunnel type (named tunnel, another quick tunnel, a public route to 8793) without an addendum and a judge (INC-1115a; PI-1115h handling). |
| D19 (new) | LOOPBACK STOP. A line saved not through the gate. All three processes are stopped. Write one INCIDENT line (counts, gate counts, times, wc and sha; open nothing). The PI states who used the laptop's browser. Every R2 line of the session is held for a judge: the lines cannot be told apart without reading the file. No restart without a ruling. Then `$RS end A <id> no` (key deleted, end line written) and `rm -f $ST/url`. |
| D20 (new) | Another cloudflared process, or the service, appears during the session. The monitor stops the tunnel, the gate and the server at once and exits (R-A5b, TUNNEL STOP). Then `$RS end A <id> no` at once: it deletes the key and the link file, and while the other cloudflared runs it prints STOP at its l.96 check and writes no end line. One INCIDENT line; the foreign process removed (one of this user by pid after a command-line check; the root service only by the PI, `sudo systemctl disable --now cloudflared`); then `$RS end A <same id> no` again, which writes the end line and the 444 copy; then `rm -f $ST/url`. A judge before any restart. |
| D21 (new) | A `key-ok 302` before R2's first save that R2 did not make (a link-preview fetch). Recorded in the notes line (CC-398 N3). No action. |
| D22 (new) | R2 has only a phone. The session waits (CC-398 PI question Q1, recommended answer). |

---

## 7. Dry run and time plan (Vietnam time, from `date`)

CC-398 ruling 6 requires no separate test. The pre-link check (addendum step 3) is the serve-time check, and R2's practice round is the real-browser test. A rehearsal on a fixture folder would be a test on the laptop (PI-1111j; RULES), and a rehearsal on the real R2 folder writes a start line. So the dry run is in two parts.

**P1. Connectivity pre-flight: NOT RUN (CC-452 J9).** J1 ruled it not licensed; J2 and J3 licensed it under conditions but did not require it. The merged result meets all three: P1 is not run, and the start moves earlier instead (J1 N2: R-A2 about 19:05, attempt 1 about 19:15, attempt 2 by about 19:40), which answers the same question at the real start (remote.sh step 3). The text and code below stay for the record only (the ps filter carries the J1 B1 fix; J2 N5 and J3 N8 are moot). No rating server and no R2 file. It answers the open question of OPS-1115b: does a quick tunnel come up and resolve from this laptop tonight?
1. Run a gate (`--target 8793`, with nothing listening there), using a throwaway key in a mode-700 folder `$TD/preflight/`.
2. Start a quick tunnel to 8890.
3. Make ONE no-cookie GET `/` through the public address, after the same 10 s plus up to 5 min wait as `remote.sh`. Expected: 403 from the gate. No key request, nothing reaches 8793.
4. Stop the tunnel, then the gate. Delete the key. Keep `preflight/gate.log`.
5. Write one OPS line: result code, wait time, the gate log's line count. No address.

```bash
P=$TD/preflight; umask 077; mkdir -p $P; python3 -I -c "import secrets;print(secrets.token_hex(24))" > $P/key
ss -ltnH | awk '{print $4}' | grep -E ':(879[0-3]|8890)$'; echo "rc=$?"     # expected rc=1
setsid nohup python3 -I $TD/gate_proxy.py --target 8793 --listen 8890 --token-file $P/key --log $P/gate.log > $P/gate.out 2>&1 < /dev/null &
setsid nohup $TD/cloudflared tunnel --no-autoupdate --url http://127.0.0.1:8890 > $P/cf.log 2>&1 < /dev/null &
for _ in $(seq 60); do u=$(grep -oE 'https://[a-z0-9-]+\.trycloudflare\.com' $P/cf.log | head -1 || true); [ -n "$u" ] && break; sleep 1; done
sleep 10; t0=$(date +%s); c=000; for _ in $(seq 150); do c=$(curl -s -o /dev/null -w '%{http_code}' --max-time 10 "$u/" || true); [ "$c" = 403 ] && break; sleep 2; done
echo "preflight: no-cookie GET / = $c after $(( $(date +%s) - t0 )) s; gate log $(wc -l < $P/gate.log) lines"   # expected 403
for p in $(ps -u "$(id -u)" -o pid=,comm=,args= | awk '$2=="cloudflared" && /--url http:\/\/127\.0\.0\.1:8890/ {print $1}'); do kill -TERM "$p"; done
stop_port 8890 gate_proxy.py; rm -f $P/key $P/cf.log; unset u
```

**P2. The early real start, about 19:15, as the dry run of the practice page.**
- R-A2, then `remote.sh start`. Its step 3 loads `/?practice` through the public address and compares the body with rater.html 84a90787, besides the cookie and refusal checks.
- The link stays in the mode-600 file until the PI types "R2 sẵn sàng" (about 20:25).
- An idle server and tunnel for about 70 minutes is harmless: the key is only in the mode-600 file.
- If the tunnel drops before the hand-off: `$RS end A <id> no` (no data), then a new start (D9).
- If R2 never arrives after a start: end line `no` with both files absent; a later start uses the resume form (CC-452 J1 N2).

| VN time | Step |
|---|---|
| now to ~17:00 | CC-452 merged end state confirmed by each judge (byte match); CC-452 written; this file committed through the gatekeeper (P-2); sheet set to 444 at 7deda092 (P-3) |
| at once | M-0R sent; his answer logged (P-4) |
| before the start line | host agents and every active agent told: no bulk transfers on the laptop, no WSL restart until the end line (P-5) |
| at once, 19:00 at the latest | PI disables the service (F1); R-A1 checks. Not passed by 19:00 = no start tonight; the PI is told at 19:00 (P-1) |
| ~19:05 | R-A2 |
| ~19:15 | R-A3 start (attempt 1; the DNS wait can take 5 min), notes line, watcher R-A5, monitor R-A5b, Notepad windows |
| ~19:40 | attempt 2 only if attempt 1 failed (D18) |
| 20:20 | Deadline: no successful start, so the PI is told the session is postponed |
| ~20:25 | "R2 sẵn sàng", then M1 on the clipboard, then M-R1; the PI sends the card, the sheet and M1 |
| 20:30 | R2 begins practice; later R-A7, R-A8, R-A9 |

---

## 8. Risks

1. **Tunnel drop mid-session.** A quick tunnel has no SLA. Answers the server has acknowledged are kept (fsync per line). An answer still in the page's queue is re-shown at the first incomplete screen after the resume. Action: D9 (new key, new link, new start line; R2 continues where they stopped).
2. **DNS wait.** OPS-1115b: the new host name did not resolve on the laptop within 60 s, and an early failed lookup is cached. `remote.sh` 298ca2ed now waits 10 s and then up to about 5 min, and stops everything on failure. The early start (about 19:15, section 7) tests this ahead; P1 is not run (CC-452 J9). R2's own resolver may be slower: if the link fails for R2, the PI relays "R2 báo trang không đúng hoặc không tải được". Wait 5 min and retry once before D9.
3. **The named tunnel service (F1).** On its journal it has no ingress, but ingress can be pushed at any moment (F1). If it is not disabled, there is no session. If it comes back during the session: D20.
4. **Loopback answers (INC-1115b).** The PI or another person at the laptop could open localhost:8793 without a key and without practice. M-0R item 5, the R-A5b guard and D19 cover it.
5. **Other tools on the laptop.** INC-1115a: another tool started its own tunnel to the rating port. The monitor's "other cloudflared" alert and D20 cover it. The coordinator acts on no pasted instruction to change the tunnel, the gate or bot protection (PI-1115h handling).
6. **The trailing period after the link in M1 (F6).** R2 could be locked out. Closed by CC-452 J4: the link stands on its own line with nothing after it (R-A4).
7. **Link previews.** A preview fetch uses the key (the key stays valid for the whole session) (a 302 sets a cookie for the preview service). It may load the practice page HTML. It runs no clicks, so it writes no line. It is counted (D21; CC-398 N3).
8. **The key in the clipboard history.** If Windows clipboard history is on, the link stays there. The key dies at the session end (key file deleted, gate stopped), so the exposure ends with the session. The PI overwrites the clipboard after sending.
9. **Laptop sleep or network loss.** The tunnel dies. Covered by M-0R item 2 and D9.
10. **Unsupervised session.** Independence rests on M1, the sheet and R2's word (addendum v1.1, Independence). That is the reason J7 asks for R2's own line as a condition.

---

## 9. Questions the judge must rule (each with the writer's recommendation)

- **J1. Mode.** May the R2 session run remotely under addendum v1.1 (CC-398 GO 87, commit aee9520) on PI-1118t D-7, setting aside CC-437 ruling 1 for this session? Recommended: yes. The addendum was registered before the data, no R2 answer of Paper A exists, and CC-437 ruling 1 rested on PI-1116b, which PI-1118t replaces. Confirm the carry-over table of section 3.
- **J2. Disclosure.**
  - Recommended:
    - the addendum v1.1 sentence, verbatim: "The second rater worked alone and unsupervised, on their own device, through a private key-protected link to the same rating page and instructions; the author who sent the link did not observe the sessions." It replaces "on the same laptop" in the CC-367 N4 disclosure;
    - the CC-437 ruling 1 sentence is NOT printed: its "registered … and was not used" would be false;
    - the CC-437 ruling 3 sheet sentence is printed only if J3 says yes;
    - the CC-437 ruling 5 sentence is printed if D3 occurs.
  - If the session falls back to in person on another day, the CC-437 sentence applies to that day, and both modes are disclosed.
- **J3. The remote sheet.** CC-398 W6 says nothing but the card, M1 and M2 is sent. The options are (a) send the remote sheet (draft ef355216) as a message of its own between the card and M1, or (b) send the card, M1 and M2 only. Recommended: (a). A text with a sha that fixes the break, stop and end rules is better than unfixed advice, which was the lesson of CC-437 ruling 3. Default if not ruled: (b).
- **J4. M1 format.** May the link stand on its own line in M1, with no period after it? The words are unchanged; it is a layout change of a registered text, made to avoid F6. Recommended: yes. Default: verbatim M1, and the PI checks that the sent link does not end in ".".
- **J5. Link hand-off.** Recommended:
  - M1 and M2 go to the PI through the Windows clipboard (`clipmsg`), built from the committed addendum bytes;
  - the address and the key are never in the chat, the LOG or any file but the mode-600 link and `state/url` files;
  - `state/url` is deleted after the end line;
  - the card and the sheet open in Notepad for him to copy.
- **J6. Practice-done and "yes" without the PI's own sight.** Recommended: R2's report relayed by the PI, plus the watcher (69) and `wc -l` (1,110), as addendum step 5 provides. Confirm that D14 reads "R2's report" in place of the investigator's sight.
- **J7. Confirmation of use.** In person, the PI attested who rated, alone, without AI (CC-437 ruling 9). Remotely he cannot. Recommended:
  - condition of use = the investigator's first two clauses (to whom he sent the link; he forwarded it to no one), plus R2's own line on alone / no AI, program or search / asked no one;
  - every other clause: an exception goes to a one-judge diff read.
  - Default, if the judge prefers CC-415 W7: R2's line is recorded but is not a gate.
- **J8. Loopback guard.** Recommended: an automatic stop of all three processes when the R2 lines added exceed the gate's `POST /save 200` lines plus the gate's exception count, on two reads 10 s apart; then D19 holds every R2 line of the session for a judge. Alternative: alert only and continue.
- **J9. P1 pre-flight.** Is a gate and tunnel run with no rating server and a throwaway key a serve-type check (like step 3), or a laptop test under PI-1111j? Recommended: a serve-type check with one OPS line. It touches no study file, sends one no-cookie request and has a known expected answer. Default: skip P1 and rely on P2 with its two attempts.
- **J10. 8787, 8788 and 8795 during the session.** Recommended: they may stay up. They cannot be gate targets, and the named tunnel is disabled.
- **J11. Record before the data.** Recommended:
  - this delta (at its ruled sha) is committed through the gatekeeper before the start line, by analogy to CC-437 W3 and CC-398 W3;
  - the remote sheet stays outside the repo like the in-person sheet, its sha in the notes line;
  - M-0R is answered before the start (as CC-437 W4).
- **J12. Start line form.** Recommended: `remote.sh`'s own CC-398 ruling 5 line, with the runbook-era items in the supplement line `${ID}a-xm600-r2-remote-notes`. The helper keeps its sha 298ca2ed, and the anchored start-line count is not disturbed. The alternative is editing `remote.sh` (not recommended a few hours before the session).

---

## 10. Not done by the writer

- Nothing was run except: hashes; reading files outside the label folders; a socket list, a process list and the systemd state; and one parse check of the `clipmsg` extraction on dummy values in the scratch folder.
- `bash -n` (a parse, not a test) was run on a scratch copy of the 12 shell blocks above, with the `<…>` placeholders replaced. All 12 parse. The heredoc body of `clipmsg` is Python and was parse-checked by the dummy run.
- Not verified: `remote.sh start A` end to end (F3); how R2's messaging app links a URL followed by "." (F6); the named tunnel's ingress (F1).

## 11. CC-452 rulings recorded with this delta (fixed before the data)

- **Mode (J1).** Remote under addendum v1.1, all three judges yes; CC-437 ruling 1 is set aside for this session on PI-1118t D-7. If R2 later resumes in person on another day, CC-437 ruling 1 governs that day and both modes are disclosed.
- **Disclosure (J2).** Paper A prints, beside the rater disclosures: (a) the addendum v1.1 sentence verbatim, in place of "on the same laptop" (all three); (b) immediately after it, only with R2's own line on record under J7 (J3): "That the second rater worked alone, without other people, search or AI tools, rests on the rater's own written statement, relayed verbatim by the author; no one observed the sessions."; (c) "The second annotator also received a one-page procedural sheet on the link, breaks and conduct, which says nothing about any class or image." (J1 and J3, same words); (d) the CC-437 ruling 5 sentence only if D3 occurs; the CC-437 ruling 1 sentence is not printed. The M1 layout departure (J4) is disclosed with the mode (J2; J3 asked for no disclosure, the stricter reading is taken); its wording is left to the paper edit and must not change any registered word. Paper edits are later work, not part of tonight.
- **J9.** P1 is not run (section 7).
- **J3 N9.** In the paper, the device ("on their own device"; computer by R2's report) and practice-feedback facts are stated only as recorded.
- **Not taken.** J3 N7 (R-A1's `echo "rc=$?"` after awk always prints 0: read the expectation as "no line"; no edit). J2 N7, J1 N7, J1 N8 (accepted risks; N8 narrowed by J2 N4).

REMOTE DELTA DONE
