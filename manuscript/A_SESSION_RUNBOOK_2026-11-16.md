# Paper A: runbook for the two remaining labelling sessions (2026-11-16)

Read-only draft by an agent for the coordinator. Nothing here has been run. No server was started, no port was called, no LOG line was written, and nothing under `~/vsps_labels*` was listed, opened or hashed by the writer.

Custody: about the held study, this file carries only design, registered rules, constants, LOG ids and file shas. It carries no outcome, no verdict word, no count per class or role, and no agreement figure.

Revision: this file is the end state of the edits of ruling CC-437 (one judge, IRREVERSIBLE, bar 85) on the draft with sha256 7ed01620e3f4fb1ba8a7b7c1a767d2b1d91c952935f844a2a17a0e6d55621296. Where a mark below still reads NO BASIS FOUND or BY ANALOGY, CC-437 rules the step (section E).

Sessions covered:
1. **R2 session.** The second annotator (R2) labels the 150 overlap images: 1,110 questions on 332 screens (`overlap_r2/assignment.json` fc8aafe9). R2 sits at the investigator's laptop in person, on the local address, with no tunnel. The practice round comes first: 15 images, 69 questions (`practice.json` e0ed805b).
2. **Top-up session.** The investigator (annotator id `PI`) labels the top-up: 1,755 questions on 943 screens (`topup1/assignment.json` ceb87d0b).

Order, as recommended by CC-397 ruling 5(d):
- R2 first, to the end, with R2's session-end line.
- R2 leaves the room.
- Then the investigator's top-up.
- Never both servers at once (CC-367 r3). Never the top-up while R2 is in the room (CC-397 r5(d)).

Marks used below:
- **[BASIS: …]** names the source that rules the step.
- **[BY ANALOGY: …]** means the source rules the same thing for another mode or for Paper B.
- **[NO BASIS FOUND: needs a judge read before the session]** means no source rules the step.

All of them are collected in section E.

Sources read (sha256, first 8 hex):

| Source | sha256 |
|---|---|
| plan v1.1 | 8ad28f67 |
| remote addendum v1.1 | add91ba3 |
| addendum E3 | c0eee4fb |
| CC-353 | 4198ee6f |
| CC-355 | 1ae3daaf |
| CC-367 | f37090f5 |
| CC-369 | d92c89d9 (read for the hold ids and release events only) |
| CC-371 | bb2fbe0a |
| CC-377 | 3f4824a4 |
| CC-386 | f79212c4 (hold and release sections only) |
| CC-391 | da1f1105 |
| CC-395 | 2f0efb04 |
| CC-397 | cd66055b |
| CC-398 | 7bf8ec54 |
| CC-404 | 2971e231 |
| CC-406 | b19cac5f |
| CC-410 | 14afd0d5 |
| CC-415 | d24a1b59 |
| CC-417 | 3947bc83 |
| CC-419 | 3d7ee12e |
| CC-429 | d9c1a48d |
| `server.py` | e3beb936 |
| `rater.html` | 84a90787 |
| `build_overlap.py` | 9c1669cd |
| `build_topup.py` | 954dd7b9 |
| `build_assignment.py` | 497e5747 |
| `~/.cache/vsps_tunnel/remote.sh` | 298ca2ed |
| `~/.cache/vsps_b/sessions.sh` | 4a140a6c |
| `tools/label_console/console.py` | 680c0998 |

LOG lines read: OPS-1111al, OPS-1111be, OPS-1111bh, OPS-1112g, OPS-1112bk, PIN-1112-a-e3-topup1, OPS-1112bm, OPS-1112cd, PIN-1112-a-xm600-r2, OPS-1112ce, OPS-1112cf, OPS-1113av, OPS-1113bz, OPS-1114x, OPS-1114ac, PI-1114e, PI-1114f, PI-1114f-verbatim, OPS-1114ai, OPS-1114al, OPS-1114aq, OPS-1114bb to OPS-1114bi, OPS-1115b, OPS-1115c, INC-1115a, INC-1115b, OPS-1115s, OPS-1115w, OPS-1115x, PI-1115k to PI-1115n, PI-1116a to PI-1116e.

---

## 0. Facts that bind both sessions

- **Ports.** One rating server at a time (CC-353 W8, CC-355 LC6, CC-367 r3, CC-398 r1).
  - 8790 is the base page. It is CLOSED for good: no line may be added to the base `labels_PI.jsonl` (CC-397 r2).
  - 8791 is the top-up.
  - 8792 is Paper B. It is closed (OPS-1115w, OPS-1115z).
  - 8793 is R2.
  - 8795 is the proposal answer page.
  - 8787 is the dashboard.
  - 8788 is the label console (read-only; OPS-1114aq).
  - 8890 is the remote gate. It must not run (in-person sessions use no tunnel).
- **Pins.**

  | File | Full sha256 |
  |---|---|
  | `server.py` | e3beb9363eba8b992efc7a2e00b3e0f721e6de8ddec4b50e18cda44c1e46c00c |
  | `rater.html` | 84a9078782dc170376c31e45bf7c277e6c58c4090afd3d347109bdd0677e1da2 |
  | R2 `assignment.json` | fc8aafe9600bf9b1977629432b60c4ffc3a22c9677454b6ea665c421574d21ff (PIN-1112-a-xm600-r2) |
  | top-up `assignment.json` | ceb87d0b78573f2329cd2397aafe7fe9647333993f13d9aa87c051e1c1be2f4c (PIN-1112-a-e3-topup1) |
  | `practice.json` (both folders) | e0ed805b31fc623df52f40d7e517cd22f8474fb043d00cb0a167d07ac4fcbbf7 |
  | R2 card `~/vsps_handoff/THE_LUU_Y_HAI_TU_baiA.txt` | eaad2dabef50570f6083105085c3826fddfa43a5d2090f2ee86d91be5dd12245 (CC-397 ADDENDUM 1; OPS-1114ai; mode 444, 947 bytes; checked by the writer, it is outside the label folders) |
  | R2 session sheet `~/vsps_handoff/HUONG_DAN_PHIEN_R2_baiA.txt` | a5cece2e4ccacba0cf2e9da5fda98044728fa5326ba89bd13b9f5257e84b2ac5 (CC-437 Annex S; 1,946 bytes, 10 lines; saved with mode 444 by the command of that annex; it is outside the label folders) |
  | Base frozen file `labels_PI.jsonl` (4,681 lines) | d338896f4c0c4bf6edd038b927ca4e0bab4149fd311f420508c1903f90c6a473 (OPS-1114ac) |

- **What is already built, by LOG.** Nothing needs building before either session. The writer did not hash these home copies, by custody; the coordinator re-hashes them in A2 and B1.
  - R2 folder `~/vsps_labels/xm600_gold_r2`: OPS-1112cd, PIN-1112-a-xm600-r2, commit f267815 (OPS-1112ce).
  - Top-up folder `~/vsps_labels/xm600_gold_topup1`: OPS-1112bk, PIN-1112-a-e3-topup1, commit d10874e (OPS-1112bm).
  - Card: OPS-1114ai.
  - FREEZE_E3 pinned: OPS-1112cc.
  - Hold 8791 released: OPS-1113bz.
  - Trigger for R2's main labels: OPS-1114ac (CC-397 r2).
  - R2 role lines: PI-1114e + PI-1114f + PI-1114f-verbatim (CC-397 r1).
  - The console check of OPS-1114aq found the three assignment pins equal and no R2 or top-up label file.
- **Not built and not licensed.** The top-up overlap set for a second annotator (CC-355 N9, CC-367 7(d)). R2 labels the base overlap only.
- **Helpers.**
  - Use `sessions.sh r2-end`, `topup-start` and `topup-end`, and only after the manual checks below.
  - Do NOT use `sessions.sh r2-start`. Its line lacks the CC-397 W2 items (card sha, "CC-397", the full role ids) and pid/cmdline. It does not check 8793, 8795, 8890 or cloudflared. It only prints the pins and does not stop on a mismatch. It refuses to start when `labels_R2.jsonl` exists, so it cannot serve a resume.
  - Do NOT use `b-addr`/`give()`: its threshold of 8 is Paper B's.
  - Do NOT use `remote.sh` (remote only).
- **Times.** Messages to the investigator use Vietnam time read from `date`. LOG stamps come from `date -u +%FT%TZ`.
- **Shell variables used below:**

```bash
REPO=/mnt/d/vsps_image_captioning; LOG=$REPO/.session_backup/2026-10-13/decisions/LOG.md
A=$HOME/vsps_labels/xm600_gold; R=$HOME/vsps_labels/xm600_gold_r2; T=$HOME/vsps_labels/xm600_gold_topup1
H=$HOME/.cache/vsps_b; CARD=$HOME/vsps_handoff/THE_LUU_Y_HAI_TU_baiA.txt; SHEET=$HOME/vsps_handoff/HUONG_DAN_PHIEN_R2_baiA.txt
idfree() { grep -qE "^[0-9T:-]{19}Z \| $1[- |]" "$LOG" && echo "STOP: id $1 used" || echo "id $1 free"; }
stop_port() { local p=$1 f=$2 pid; pid=$(ss -ltnpH "sport = :$p" | grep -o 'pid=[0-9]*' | head -1 | cut -d= -f2)
  [ -z "$pid" ] && { echo "$p: nothing listens"; return 0; }
  tr '\0' ' ' < /proc/$pid/cmdline | grep -qF -- "$f" || { echo "STOP: pid $pid on $p is not $f"; return 9; }
  kill -TERM "$pid"; sleep 1; ss -ltnH | awk '{print $4}' | grep -qE ":$p\$" && echo "STOP: $p still listens" || echo "$p stopped (pid $pid)"; }
```

---

## Before the first session: what must be ruled

CC-437 (one judge, IRREVERSIBLE, bar 85) rules items E1 to E13 and every NO BASIS mark of this file.

R2's session must NOT open before all of these hold:
1. This file hashes to the end-state sha256 written in CC-437 and is committed through the gatekeeper at that state (A2 checks both).
2. The session sheet exists at its sha (section 0).
3. Message M-0 (A0) has been sent, and the investigator has answered it with his fixed line.
4. A1 and A2 pass.

Mode: in person. CC-367 ruling 3 and N4, CC-397 W3 and the CC-397 ruling 3 delivery apply again, as amended by CC-437 rulings 1 to 3. The remote addendum v1.1 is not used for this session (PI-1116b); `remote.sh`, the gate and the tunnel stay off.

---

## Part A. R2 session (in person, port 8793)

### A0. Advance message M-0 (may be sent now; R2's session does not open before the investigator's answer)

[BASIS: CC-437 rulings 1, 2 and 4; CC-397 W3; CC-369 H-4.]

> PI: chuẩn bị cho phiên của người gán thứ hai (R2) bài A, làm tại máy của PI.
> 1. Khi R2 sắp tới (trước khoảng 15 phút), gõ: "R2 sắp tới". Tôi sẽ tắt dashboard (8787), trang xem tiến độ nhãn (8788) và trang trả lời đề cương (8795), rồi bật trang của R2.
> 2. Trước khi R2 ngồi vào máy: đóng mọi tab trình duyệt, cửa sổ thư mục, tệp, PDF và trình soạn thảo đang mở (repo, bài báo, đề cương). Trong Notepad, đóng mọi tab cũ. Cắm sạc và tắt chế độ ngủ của máy trong phiên.
> 3. Không đóng cửa sổ chat này (đóng nó là phiên dừng); chỉ thu nhỏ nó. Từ lúc R2 ngồi vào máy tới lúc R2 rời máy, không mở cửa sổ terminal hay WSL mới (mở mới sẽ tự bật lại dashboard).
> 4. Phiên dài khoảng 2 giờ: 15 ảnh làm quen, rồi 150 ảnh với 1.110 câu. R2 có thể nghỉ ngắn, hoặc dừng và làm tiếp hôm khác.
> 5. Trước và trong phiên, PI không nói với R2 điều gì về nghiên cứu: giả thuyết, kết quả, bài báo, chú thích, hệ thống hay câu trả lời của PI. PI không giải thích cách chọn câu trả lời; mọi hướng dẫn nằm trên trang và trong hai tờ tôi sẽ mở sẵn.
> 6. Phiên bổ sung (top-up) của PI chỉ mở sau khi R2 đã rời máy và tôi đã ghi dòng kết thúc phiên của R2.
> Nếu đồng ý, xin gõ: "Đã đọc M-0".


### A1. Screen hygiene, when the investigator says R2 has arrived

[BASIS: CC-397 W3 (8795 stopped, dashboard closed, every rating server stopped except R2's); CC-369 W10 (dashboard words while R2 can see the laptop). BY ANALOGY for 8788, which postdates CC-397: see E4.]

```bash
stop_port 8795 answer_server.py
stop_port 8787 progress_server.py
stop_port 8788 tools/label_console/console.py
```

Note for the coordinator: the writer counted strings in `~/vsps_dashboard/v2/progress_state.json`. 3 strings carry both an outcome word and a Paper A token. The writer did not read them. 8787 stays stopped until R2's session-end line. Every new interactive shell (a new terminal window, not only a WSL restart) brings 8787 and 8788 back through `~/.bashrc` lines 128 and 130, which sit below the interactive guard of lines 6 to 9. The coordinator's own non-interactive commands do not. The monitor of A5b stops them again; see D11.

### A2. Preconditions (each must print the expected value; any other output = no start)

```bash
cd $REPO
ID=OPS-1116<x>; idfree $ID                         # the next free OPS-1116 id
# ports and processes [BASIS: CC-367 r3 / C5; CC-398 r1 "one rating server at a time"; 8890 and cloudflared BY ANALOGY addendum v1.1 step 1]
ss -ltnH | awk '{print $4}' | grep -E ':(879[0-9]|8890)$'; echo "rc=$?"        # expected: no output, rc=1
ps -eo pid=,args= | grep -E 'obj_rater/(server|pair_server)\.py|gate_proxy|cloudflared' | grep -v grep; echo "rc=$?"   # expected: rc=1
systemctl is-active cloudflared 2>/dev/null; echo                             # expected: inactive (INC-1115a)
grep -nE '^[^#]*(obj_rater|gate_proxy|cloudflared)' ~/.bashrc; echo "rc=$?"   # expected: rc=1 (no live autostart; OPS-1114al)
# pins [BASIS: plan §3 l.32; CC-367 L-f; CC-397 ADDENDUM 1 A1-2 "if the saved file does not hash to TARGET, it is not shown"]
sha256sum tools/obj_rater/server.py tools/obj_rater/rater.html $R/assignment.json $R/practice.json $CARD $SHEET
#   expected: e3beb936..., 84a90787..., fc8aafe9..., e0ed805b..., eaad2dab..., a5cece2e... (full values in section 0)
# this runbook at the end state of CC-437, and committed at that state [BASIS: CC-437 W1, W3]
RB=manuscript/A_SESSION_RUNBOOK_2026-11-16.md; sha256sum $RB     # expected: the end-state sha256 written in CC-437
git ls-files --error-unmatch $RB > /dev/null 2>&1 && git diff --quiet HEAD -- $RB && git log -1 --format='runbook committed %h' -- $RB || echo "STOP: runbook not committed at this state"
# the investigator's answer to M-0 is on the LOG as a PI line [BASIS: CC-437 W4]
# R2 files absent at the first session [BASIS: CC-367 C6; L-f]
test ! -e $R/labels_R2.jsonl && test ! -e $R/practice_R2.jsonl && echo absent  # expected: absent
grep -cE '^[0-9T:-]{19}Z \| OPS-[0-9a-z]+-xm600-r2-start \|' "$LOG"            # expected: 0 at the first session
# base first pass frozen [BASIS: CC-397 r2]
echo "$(wc -l < $A/labels_PI.jsonl) $(sha256sum < $A/labels_PI.jsonl | cut -c1-64)"
#   expected: 4681 d338896f4c0c4bf6edd038b927ca4e0bab4149fd311f420508c1903f90c6a473
# LOG prerequisites [BASIS: CC-397 W2; CC-367 L-f; CC-398 r1 (earlier sessions have their end lines)]
for i in OPS-1114ac-xm600-session-end PI-1114e PI-1114f PI-1114f-verbatim CC-397 PIN-1112-a-xm600-r2 \
         OPS-1112ce-xm600-r2-commit OPS-1114ai-a-r2-card-saved OPS-1115w-b-pref-session-end CC-437; do
  grep -qE "^[0-9T:-]{19}Z \| $i \|" "$LOG" && echo "ok $i" || echo "MISSING $i"; done   # expected: all ok
```

- If 8790 to 8793 shows a listener, or a rating, gate or tunnel process runs: no start. Go to D1 or D2.
- If the base check differs: stop all R2 work, open nothing, go to a judge (CC-397 r2).

### A3. Start the server and write the start line (L-f)

[BASIS: CC-367 C7 (command) and L-f (line), CC-397 W2 (extra items, BLOCKING), CC-367 r2 (port and folder). The detached start and the pid/cmdline record are BY ANALOGY to addendum v1.1 step 4.]

```bash
cd $REPO
setsid nohup python3 -B tools/obj_rater/server.py --dir $R --annotator R2 --port 8793 > $H/r2.out 2>&1 < /dev/null &
for _ in $(seq 20); do ss -ltnH | awk '{print $4}' | grep -qE ':8793$' && break; sleep 0.5; done
PID=$(ss -ltnpH 'sport = :8793' | grep -o 'pid=[0-9]*' | head -1 | cut -d= -f2); echo "$PID" > $H/r2.pid
CMD=$(tr '\0' ' ' < /proc/$PID/cmdline); echo "$CMD"
#   must contain: --dir <the expanded $R> --annotator R2 --port 8793   (else stop by pid; no line)
LIS=$(ss -ltnH | awk '{print $4}' | grep -E ':(879[0-9]|8890)$' | sed 's/.*://' | sort | tr '\n' ' '); echo "[$LIS]"
#   must be exactly [8793 ]
CCSHA=$(sha256sum < $REPO/.session_backup/2026-10-13/decisions/CC-437.txt | cut -c1-64); RB=manuscript/A_SESSION_RUNBOOK_2026-11-16.md
RBSHA=$(sha256sum < $RB | cut -c1-64); RBCOMMIT=$(git log -1 --format=%h -- $RB); SHEETSHA=$(sha256sum < $SHEET | cut -c1-64)
LINE="$(date -u +%FT%TZ) | $ID-xm600-r2-start | CC-367 GO 87 (L-f with CC-397 W2); mode main, practice first (CC-367 C8; CC-397 W3; CC-397 ruling 5 item 6); in person at the PI's laptop, local address, no gate or tunnel (PI-1116b; CC-437, CC sha256 $CCSHA at this time); runbook A_SESSION_RUNBOOK_2026-11-16.md sha256 $RBSHA, commit $RBCOMMIT; session sheet HUONG_DAN_PHIEN_R2_baiA.txt sha256 $SHEETSHA (CC-437 Annex S); M-0 answered: <PI line id>; chat window minimized, not closed (CC-437 ruling 2); trigger OPS-1114ac-xm600-session-end; PI role lines PI-1114e + PI-1114f + PI-1114f-verbatim (CC-397 r1); PIN-1112-a-xm600-r2; card THE_LUU_Y_HAI_TU_baiA.txt sha256 eaad2dabef50570f6083105085c3826fddfa43a5d2090f2ee86d91be5dd12245 (CC-397 r3 and ADDENDUM 1; OPS-1114ai); CC-397; screen hygiene (CC-397 W3): 8795, 8787 and 8788 stopped by pid; port check before start: nothing on 8790-8799 or 8890 (ss -ltnH), no cloudflared or gate_proxy process, cloudflared service inactive; test ! -e labels_R2.jsonl and practice_R2.jsonl: absent; base labels_PI.jsonl wc -l 4681 sha256 d338896f (= OPS-1114ac, unchanged); server.py e3beb936, rater.html 84a90787, R2 assignment.json fc8aafe9 (= PIN), practice.json e0ed805b; annotator R2, port 8793; server pid $PID, cmdline: $CMD; listeners after start (8790-8799, 8890): $LIS"
printf '%s\n' "$LINE" >> "$LOG"
```

Then, in this order: start the practice watcher (A5) and the hygiene monitor (A5b) in the background; open the two Notepad windows (A4); send M-A1 and M-A2 (A4).

### A4. Messages (Vietnamese, exact)

**M-A1, to the investigator, right after the start line and after the two Notepad windows are open.** It gives the practice address only. The main address is sent later, in M-A3 (A5), after the practice-done line. [BASIS: CC-367 C8 ("/?practice first; then … /"); CC-367 r3 (header); CC-397 W3 (fresh private window, header check before the first answer); CC-406 ruling 6 (an order rule is enforced by the server state and by what address is handed out, not by a notice); CC-437 rulings 1 to 3.]

> PI: trang gán nhãn của R2 (bài A) đã chạy trên cổng 8793. Tôi đã mở hai cửa sổ Notepad: "HƯỚNG DẪN PHIÊN GÁN NHÃN" và "LƯU Ý VỀ HAI TỪ". Xin làm đúng thứ tự, trước khi R2 ngồi vào máy:
> 1. Kiểm tra Notepad chỉ có đúng hai tờ đó, không có tab nào khác. PI không đọc to, không giải thích hai tờ này.
> 2. Mở MỘT cửa sổ riêng tư mới (InPrivate hoặc Ẩn danh) và gõ đúng địa chỉ vòng làm quen: http://localhost:8793/?practice
> 3. Xem dòng trên cùng: phải ghi "Người gán: R2" và tiêu đề "Vòng làm quen". Không bấm phím hay nút nào trên trang. Nếu khác, không cho R2 bắt đầu và nhắn tôi.
> 4. Gõ cho tôi đúng dòng: "Đã thấy Người gán: R2 ở vòng làm quen". Chờ tôi trả lời "Mời R2 bắt đầu".
> 5. Thu nhỏ cửa sổ chat này, mời R2 ngồi vào máy và chỉ nói: "Xin đọc cửa sổ HƯỚNG DẪN PHIÊN GÁN NHÃN trước, rồi làm theo." Sau đó PI ngồi ở chỗ không nhìn thấy màn hình.
> 6. Khi R2 gọi vì trang đã báo "Xong vòng làm quen": PI nhìn dòng đó trên trang (không bấm gì), mời R2 tạm rời ghế, mở lại cửa sổ chat và gõ đúng dòng: "R2 đã xong vòng làm quen, trang đã hiện Xong vòng làm quen". Tôi sẽ kiểm tra rồi gửi địa chỉ phần chính. Không mở địa chỉ nào khác trước khi tôi gửi: nếu phần chính bị mở trước, máy chủ sẽ tự dừng.

The coordinator's reply to the header line of step 4, exact: "Mời R2 bắt đầu vòng làm quen. Xin thu nhỏ cửa sổ này."

The address `localhost:8793` is the Windows-side form of CC-367 C8's `127.0.0.1:8793`. The investigator's base and Paper B sessions used the `localhost` form (OPS-1114ac, OPS-1114bh).

**The two sheets, opened by the coordinator right after the start line and before M-A1.** [BASIS: CC-397 r3 DELIVERY (one separate plain-text window, not a browser tab; R2 reads the card alone, after the on-page guide and before practice, and may keep it in view; the investigator does not read it aloud, paraphrase or explain it); CC-437 ruling 3 for the session sheet. Notepad is not one of the programs barred by RULES item 12.]

```bash
[ "$(sha256sum < $CARD | cut -c1-64)" = eaad2dabef50570f6083105085c3826fddfa43a5d2090f2ee86d91be5dd12245 ] \
  && [ "$(sha256sum < $SHEET | cut -c1-64)" = a5cece2e4ccacba0cf2e9da5fda98044728fa5326ba89bd13b9f5257e84b2ac5 ] \
  && { (setsid nohup notepad.exe "$(wslpath -w $SHEET)" > /dev/null 2>&1 < /dev/null &); (setsid nohup notepad.exe "$(wslpath -w $CARD)" > /dev/null 2>&1 < /dev/null &); } \
  || echo "STOP: a sheet sha differs; show neither"
```

**What R2 is told.** R2 reads the session sheet herself; it replaces the spoken text of the draft, so that every instruction R2 receives is a file with a sha. The investigator says one sentence only (M-A1 step 5). The sheet holds the page's own key line and image tip (rater.html l.44, l.55), the conduct clauses of the registered message M1 of addendum v1.1, the reading order of CC-397 r3, and the rules for the practice end, breaks, a stop and the end (CC-437 rulings 3 and 8). It says nothing about any class or image.

**M-A2, conduct text for the investigator, sent with M-A1.** [BASIS: CC-367 r3, r4 and 7(a); CC-397 W3; CC-369 H-4; plan §3 l.30; the stop rule BY ANALOGY addendum v1.1 step 7; CC-437 rulings 2, 8 and 10.]

> Trong lúc R2 gán nhãn bài A, PI:
> - Chỉ nói câu mời đọc tờ hướng dẫn. Nếu R2 hỏi cách dùng trang (nút, phím), chỉ vào tờ "HƯỚNG DẪN PHIÊN GÁN NHÃN". Nếu R2 hỏi về nội dung (lớp, ảnh, cách chọn), chỉ nói: "Xem phần 'Cách trả lời' trên trang hoặc tờ lưu ý." Không đọc to, không diễn giải hai tờ đó. Ghi nhớ R2 đã hỏi gì để báo tôi sau phiên.
> - Ngồi ở chỗ không nhìn thấy màn hình; không xem, không bình luận, không chụp màn hình. PI chỉ nhìn trang ở ba lúc: dòng "Người gán: R2", dòng "Xong vòng làm quen" và dòng "Đã trả lời hết các câu"; không bấm phím hay nút nào trên trang.
> - Không nói gì về ảnh, lớp, chú thích hay câu trả lời với R2, kể cả lúc nghỉ, cho tới khi tôi báo R2 đã xong toàn bộ và đã ghi dòng kết thúc; sau đó vẫn không nói gì về câu trả lời nào cho tới khi tôi báo kappa đã được mở niêm phong.
> - Không cho R2 biết giả thuyết, kết quả hay thông tin nào của nghiên cứu; không mở dashboard, bài báo hay tệp nào của dự án trên máy này khi R2 còn ở đó.
> - Không trả lời thay R2; không chạm vào máy khi R2 nghỉ; không mở localhost:8790, 8791 hay tệp nhãn nào.
> - Trong phiên, tôi chỉ gửi vào cửa sổ chat các tin nhắn cố định của phiên này. PI chỉ mở cửa sổ chat khi R2 không ngồi trước màn hình.
> - Nếu trang không tải được, dòng trên cùng không ghi "Người gán: R2", hoặc dòng cảnh báo đỏ còn hiện quá một phút: nhờ R2 dừng tay (không đóng trang), rồi nhắn tôi.
> - R2 nghỉ ngắn (dưới 30 phút, không rời nơi làm việc): không cần báo tôi; PI nhớ số lần nghỉ. Nghỉ lâu hơn hoặc R2 ra về: coi là dừng trong hôm nay.
> - Khi R2 báo dừng (R2 đã tự đóng cửa sổ trang) hoặc gọi vì trang hiện "Đã trả lời hết các câu": PI nhìn dòng đó nếu có, đóng cửa sổ riêng tư, chờ R2 rời máy, rồi mở lại cửa sổ chat và gõ đúng một dòng: "R2 đã xong tất cả các ảnh, trang đã hiện Đã trả lời hết các câu" hoặc "R2 dừng, chưa xong".
> - Ngoài các lần kiểm tra nêu trên, PI không tự mở localhost:8793; sau phiên cuối của R2, không bao giờ mở lại nó (trang đó tải lại các lựa chọn của R2).

### A5. Practice: the watcher and the practice check

[BASIS for the stop: CC-367 r6 ("labels_R2.jsonl exists … stop all R2 work, open nothing, and go to a judge"). Enforcing the order by server state follows the lesson recorded in CC-406 r6 and OPS-1114bi. The threshold and the check are BY ANALOGY to addendum v1.1 step 5 ("at least the number of questions in the committed practice.json"), which is 69. See E5.]

Run in the background right after A3. It exits once, either at practice complete or at a violation.

```bash
R=$HOME/vsps_labels/xm600_gold_r2; PID=$(cat $HOME/.cache/vsps_b/r2.pid)
while :; do
  n=$( [ -f $R/practice_R2.jsonl ] && wc -l < $R/practice_R2.jsonl || echo 0 )
  if [ -e $R/labels_R2.jsonl ] && [ "$n" -lt 69 ]; then
    tr '\0' ' ' < /proc/$PID/cmdline | grep -qF -- '--annotator R2 --port 8793' && kill -TERM "$PID"
    echo "STOPPED $(date -u +%FT%TZ): labels_R2.jsonl appeared with practice_R2.jsonl at $n lines"; exit 9; fi
  if [ "$n" -ge 69 ]; then
    echo "PRACTICE COMPLETE $(date -u +%FT%TZ): practice $n; labels_R2 $( [ -e $R/labels_R2.jsonl ] && echo present || echo absent )"; exit 0; fi
  kill -0 "$PID" 2>/dev/null || { echo "SERVER GONE $(date -u +%FT%TZ)"; exit 8; }
  sleep 5
done
```

The count test is necessary but not sufficient: re-answers add lines, so 69 lines need not mean 15 complete screens. The sufficient signal is the page's end text "Xong vòng làm quen. Hãy báo để mở bộ chính." The page shows it only after every practice screen is complete and saved (rater.html: `next()` requires an empty save queue, and `finish()` runs only past the last screen). The investigator looks at that text and types his fixed line (M-A1 step 6). Only then does the coordinator write the practice-done line and send M-A3 with the main address.

On exit 0 AND after the investigator's fixed line of M-A1 step 6, write the practice-done line. If the watcher has not exited 0 when his line arrives, answer only: "Vòng làm quen chưa đủ; xin mời R2 làm tiếp vòng làm quen." If `labels_R2.jsonl` is present at this point although the watcher exited 0, see D14. [Precedent OPS-1111be; BY ANALOGY addendum v1.1 step 5.]

```bash
idfree ${ID}b; n=$(wc -l < $R/practice_R2.jsonl); L=$( [ -e $R/labels_R2.jsonl ] && echo present || echo absent )
printf '%s\n' "$(date -u +%FT%TZ) | ${ID}b-xm600-r2-practice-done | practice_R2.jsonl wc -l $n (at least 69, the questions of practice.json e0ed805b; count only, practice answers are not data); labels_R2.jsonl $L at this time; watcher exit PRACTICE COMPLETE; the investigator's fixed line on the page end text is in the chat record; the main address is sent only after this line (M-A3; CC-367 C8; addendum v1.1 step 5 applied in person by CC-437 ruling 5). Counts only." >> "$LOG"
```

On exit 9, follow D3. On exit 8, follow D9.

**M-A3, to the investigator, right after the practice-done line.** [BASIS: CC-367 C8; CC-367 r3 (header before the first main answer); CC-437 ruling 5.]

> PI: vòng làm quen đã được ghi nhận. Trong CÙNG cửa sổ riêng tư đó, gõ địa chỉ phần chính: http://localhost:8793/ . Xem dòng trên cùng: phải ghi "Người gán: R2" và tiêu đề "Gán nhãn vật thể · XM3600-600"; không bấm phím hay nút nào. Nếu đúng, thu nhỏ cửa sổ chat này và mời R2 ngồi lại làm tiếp; không cần nhắn tôi. Nếu khác, nhắn tôi và không cho R2 làm tiếp.

### A5b. Hygiene monitor (background, for the whole R2 session)

[BASIS: CC-397 W3; CC-369 W10; CC-437 ruling 4. It reads the local socket list and process command lines only, and calls no port.]

```bash
PID=$(cat $HOME/.cache/vsps_b/r2.pid)
while kill -0 "$PID" 2>/dev/null; do
  for p in 8787 8788 8795 8790 8791 8792 8890; do
    q=$(ss -ltnpH "sport = :$p" | grep -o 'pid=[0-9]*' | head -1 | cut -d= -f2); [ -n "$q" ] || continue
    c=$(tr '\0' ' ' < /proc/$q/cmdline | cut -c1-120); echo "REAPPEARED $(date -u +%FT%TZ) port $p pid $q: $c"
    case "$p:$c" in
      8787:*progress_server.py*|8788:*label_console/console.py*|8795:*answer_server.py*) kill -TERM "$q";;
      *) echo "NOT STOPPED: port $p; go to D1 or D2 now";;
    esac
  done; sleep 20
done > $HOME/.cache/vsps_b/r2_monitor.out 2>&1
```

Its count of REAPPEARED lines goes into the session-notes line of A8.

### A6. Main set

- There is no coordinator action while R2 rates. No `/state` call and no request to 8793. Read `wc -l` only, and only when needed (CC-367 7(a); CC-397 W3).
- R2's questions: the investigator answers only with the pointer sentence of M-A2.
- If R2 asks about anything, the investigator reports the question in his end message. The coordinator records it in one OPS line, with the page or card text that was pointed to and no item content. [Precedent OPS-1114bb, OPS-1114bd: "so that the closing record shows every instruction a rater received".]

### A7. Pauses and resume

- **Short break, server up.** Allowed (CC-437 ruling 8). R2 completes the screen in view, presses Enter so that an unanswered screen shows, leaves the page open and returns to the same window (sheet item 6). Nobody touches the laptop. The investigator stays away from the screen and says nothing about the study. A break is short if it lasts under 30 minutes and R2 does not leave the premises; no LOG line is written, and the investigator reports the number of breaks in his confirmation (A9). Anything longer is a stop for the day (A8 with `no`, then a resume by the next item). The time-on-screen field of the first answer after a break is long; no registered statistic reads that field.
- **Stop for the day.** Run the session end (A8) with `no`. Paper A's overlap has no close and resumes at the first incomplete screen on another day (CC-397 r5(a); rater.html opens at the first incomplete screen).
- **Resume session, on another day.**
  - Run A1, then A2 with these changes:
    - The R2 files are present, so do not test their absence. Check them instead:

      ```bash
      echo "labels $(wc -l < $R/labels_R2.jsonl) $(sha256sum < $R/labels_R2.jsonl | cut -c1-64); practice $(wc -l < $R/practice_R2.jsonl) $(sha256sum < $R/practice_R2.jsonl | cut -c1-64)"
      ```

      Both must equal the last `-xm600-r2-session-end` line. Practice must be at least 69.
    - `grep -cE '^[0-9T:-]{19}Z \| OPS-[0-9a-z]+-xm600-r2-start \|' "$LOG"` equals the number of earlier `-xm600-r2-session-end` lines, counted in the same anchored way.
  - Start as in A3, with id `$ID-xm600-r2-start` and in the line "mode main, resume (practice done: `<practice-done id>`)". Replace "absent" by the counts and shas above, "equal to `<last end id>`".
  - Give the main address only, with the header check of M-A3: `http://localhost:8793/`. Practice is done. The investigator checks the header, presses no key and no button, and steps away. The page opens at the first incomplete screen; if R2 followed sheet item 7 that screen shows no answer. If it shows selected answers, he says so in his confirmation (A9) and the session-notes line records it (D15).
  - Do not start the practice watcher; start the hygiene monitor (A5b). Check `wc -l` at the end only.
  - The two sheets are opened again as in A4. M-A2 is sent again.
  - [The resume line form is ruled by CC-437 ruling 6, on the model of addendum v1.1 step 4 (later session: wc and sha of R2's files equal the last end line).]
- Between R2 sessions, no other rating server runs unless R2's last end line exists (CC-367 r3). The investigator's top-up may run between two R2 days only after R2 has left (CC-397 r5(d)). Section C explains why the recommended order is R2 to the end first.

### A8. Session end (after the investigator's fixed line)

[BASIS: CC-367 session end and L-g (stop, wc and sha256 of the two R2 files, 444 copy, line); CC-391 B2 and `a_cert_perann.py` l.282 (the end line must hold the literal "R2 finished all screens yes" and the copy sha). Pid and cmdline: `sessions.sh stop()`.]

```bash
sha256sum $H/sessions.sh | cut -c1-8                      # expected 4a140a6c
wc -l < $R/labels_R2.jsonl                                 # label-free check before writing "yes"
```

- **"yes".** Only when the investigator wrote "R2 đã xong tất cả các ảnh, trang đã hiện Đã trả lời hết các câu" AND `wc -l` is at least 1,110. One line per click, so fewer than 1,110 lines cannot mean every question was answered (CC-397 r2 reasoning). The page shows that text only when every screen is complete and saved (rater.html l.92, l.130, l.161).
- If the line count is below 1,110, or he did not see the end text, write `no`. Ask the investigator what the page showed. A remaining conflict goes to a judge (CC-437 ruling 9).
- After the helper's line, check that it prints assignment fc8aafe9, server e3beb936 and rater 84a90787. Any other value: one INCIDENT line, and a judge before any use.

```bash
ID3=OPS-1116<y>; idfree $ID3
$H/sessions.sh r2-end $ID3 yes        # or: no
tail -1 "$LOG"; ss -ltnH | awk '{print $4}' | grep -E ':(879[0-9]|8890)$'; echo "rc=$?"   # expected rc=1
```

The helper stops 8793 by pid after a cmdline check (`--port 8793`). It makes `labels_R2.<UTC>.jsonl` with mode 444 and the same sha. It writes the line:

`<UTC> | <ID3>-xm600-r2-session-end | labels_R2.jsonl wc -l <n> sha256 <64hex>; practice_R2.jsonl wc -l <n> sha256 <64hex>; 444 copy labels_R2.<UTC>.jsonl sha256 <64hex> (same sha); assignment fc8aafe9, server e3beb936, rater 84a90787; statement: R2 finished all screens yes|no; server on 8793 stopped. Counts and shas only.`

This is the CC-367 L-g form. If R2 stopped during practice (no `labels_R2.jsonl`), the helper writes the line without a copy: the L-g "absent" case.

After the line:
1. Make sure R2's private window and the two Notepad windows are closed.
2. Restart 8787 and 8788, and 8795 if the investigator needs it, only after the session-end line AND after R2 has left the laptop (CC-369 W10, CC-397 W3, CC-437 ruling 4):

   ```bash
   (cd $HOME/vsps_dashboard/v2 && setsid nohup python3 -B progress_server.py --port 8787 >> server.log 2>&1 < /dev/null &)
   (cd $REPO && setsid nohup python3 -I tools/label_console/console.py --port 8788 >> $H/console.out 2>&1 < /dev/null &)
   ```

3. Send M-A4 and ask for the confirmations of A9.
4. Write the session-notes line (no label is read for it):

   `<UTC> | <ID>-xm600-r2-session-notes | R2 session <start id> to <end id>, in person (CC-437): the investigator's end line, quoted: "<...>"; his confirmation line: <PI id | pending>; breaks reported: <n>; questions R2 asked: <n> (pointer given: page guide | card | session sheet); hygiene monitor REAPPEARED lines: <n> (ports <list>); practice-done line <id>; first screen at a resume showed selected answers: <no | yes, n rows>; deviations: <none | D ids>. No label read.`

5. Effects the coordinator carries forward:
   - CC-377 r10: the next Paper A paper commit re-tenses the "has not yet labelled" strings, because an R2 start line now exists.
   - The H-4 bar "nothing of the study to R2" ends only at R2's LAST session-end line, the one that states `yes` (CC-437 ruling 4). After an end line with `no`, the bar stays, and 8787, 8788 and 8795 are stopped again before R2 next sits at the laptop. The bar on any answer lasts until the kappa unsealing (CC-369 H-4; CC-367 r4).
   - After the end line that states `yes`, the server on 8793 is not started again without a ruling.

**M-A4, to the investigator, after the session-end line.**

> PI: tôi đã ghi dòng kết thúc phiên của R2 (<R2 đã xong toàn bộ | R2 chưa xong, sẽ làm tiếp>). Xin làm ba việc:
> 1. Gõ cho tôi một dòng xác nhận theo mẫu tôi gửi ngay sau đây, đúng sự thật; có thể sửa chữ, và điều nào không đúng thì ghi rõ điều gì, trong bao nhiêu ảnh.
> 2. Nhờ R2 tự viết một hai câu bằng lời của mình, gửi PI, về ba ý: có tự làm một mình không; có dùng công cụ AI, chương trình hay tra cứu không; có hỏi ai không. PI chuyển nguyên văn cho tôi. Xin không đưa câu mẫu cho R2.
> 3. Từ giờ: không mở localhost:8793; không nói với R2 về câu trả lời nào cho tới khi tôi báo kappa đã được mở niêm phong<; vì R2 chưa xong, vẫn không nói gì về nghiên cứu với R2 và không để R2 thấy dashboard hay tệp dự án>.

### A9. Confirmations to ask afterwards

**From the investigator, typed by him, quoted in a PI line with a `date -u` stamp.** [BY ANALOGY: CC-415 W2 and CC-417 r3 (Paper B in person). The clauses restate CC-367 r4 and CC-397 W3 and r3 for Paper A. See E9.] He may reword, but every clause must be affirmed or its exception stated exactly, with the screen count. An exception goes to a one-judge diff read before any use (CC-415 r2).

> Người đã gán tại laptop hôm <ngày>, từ khoảng <giờ VN> đến <giờ VN>, là người gán thứ hai (R2) mô tả trong PI-1114e và PI-1114f, không phải tôi và không phải ai khác; người đó tự trả lời một mình tất cả các câu; không dùng công cụ AI, chương trình hay tra cứu; người đó đọc phần 'Cách trả lời', tờ hướng dẫn phiên và tờ 'LƯU Ý VỀ HAI TỪ' rồi làm vòng làm quen trước phần chính; tôi không nhìn màn hình khi người đó gán, trừ ba lần kiểm tra dòng 'Người gán: R2', dòng 'Xong vòng làm quen' và dòng 'Đã trả lời hết các câu'; tôi không bấm phím hay nút nào trên trang của người đó; tôi không giải thích gì ngoài việc chỉ tới phần 'Cách trả lời', tờ hướng dẫn phiên và tờ lưu ý, và không đọc to hay giải thích các tờ đó; tôi chỉ mở cửa sổ chat khi người đó không ngồi trước màn hình; tôi và người đó không trao đổi về ảnh, lớp, câu trả lời hay nghiên cứu; người đó nghỉ ngắn <số> lần, và trong lúc nghỉ không ai chạm vào máy.

The first three clauses (who rated; alone; no AI tool, program or search) are a condition of use: without them on record as the investigator's typed line, the file is not R2's data, the kappa unsealing line is not written, and a judge reads the case (CC-437 ruling 9; CC-415 ruling 2).

**From R2, in R2's own words.** R2 writes a message to the investigator, who forwards it verbatim. Give R2 content points, not a sentence to copy; the attribution problem of PI-1116b and PI-1116d came from a copied sentence. The points: R2 answered alone, used no AI tool, program or search, and asked no one. [BY ANALOGY: CC-415 W7, CC-417 W2 (Paper B; recorded, not a gate).]

---

## Part B. Investigator's top-up session (port 8791, annotator PI)

### B1. Preconditions

[BASIS:
- CC-355 LC6: after the part-1-finished line; nothing on 8790 or 8792; `test ! -e` logged; the exact command.
- CC-367 r3: 8791 never with 8793.
- CC-397 r5(d): never while R2 is in the room; recommended last.
- Addendum E3 §6 and CC-355 W2: the session starts after OPS-1112cf.
- OPS-1113bz: the hold is released.]

```bash
cd $REPO; ID=OPS-1116<z>; idfree $ID
ss -ltnH | awk '{print $4}' | grep -E ':(879[0-9]|8890)$'; echo "rc=$?"        # expected: no output, rc=1; a line for 8795 alone is accepted (it is not a rating page)
ps -eo pid=,args= | grep -E 'obj_rater/(server|pair_server)\.py|gate_proxy|cloudflared' | grep -v grep; echo "rc=$?"   # expected rc=1
sha256sum tools/obj_rater/server.py tools/obj_rater/rater.html $T/assignment.json $T/practice.json $H/sessions.sh
#   expected e3beb936..., 84a90787..., ceb87d0b78573f2329cd2397aafe7fe9647333993f13d9aa87c051e1c1be2f4c, e0ed805b..., 4a140a6c...
test ! -e $T/labels_PI.jsonl && test ! -e $T/practice_PI.jsonl && echo absent  # expected absent (first session)
echo "$(wc -l < $A/labels_PI.jsonl) $(sha256sum < $A/labels_PI.jsonl | cut -c1-64)"   # expected 4681 d338896f... (CC-397 r2)
for i in OPS-1112cf-xm600-session-end-part1 OPS-1114ac-xm600-session-end PIN-1112-a-e3-topup1 OPS-1112bm-a-e3-topup1-commit \
         OPS-1113bz-a-hold-release OPS-1112cc-a-e3-FREEZE_E3-pin; do
  grep -qE "^[0-9T:-]{19}Z \| $i \|" "$LOG" && echo "ok $i" || echo "MISSING $i"; done
grep -cE '^[0-9T:-]{19}Z \| OPS-[0-9a-z]+-a-e3-topup-(start|resume) \|' "$LOG"   # expected 0 (first session)
# R2 not in the room: the last R2 line in the LOG must be a session-end line
grep -oE '\| OPS-[0-9a-z]+-xm600-r2-(start|session-end) \|' "$LOG" | tail -1    # expected: ...-xm600-r2-session-end
```

`key.json` is not hashed here. LC6 does not ask for it; its check belongs to the e3-score run (CC-371 T6).

### B2. Start

[BASIS: CC-355 LC6 start line, written by the helper. It writes "test ! -e …: absent; nothing listened on 8790, 8792, 8793; server.py, rater.html, top-up assignment.json shas (PIN ceb87d0b); started on 127.0.0.1:8791, annotator PI". The line holds no label-copy sha, as CC-371 W4 requires.]

```bash
$H/sessions.sh topup-start $ID
tail -1 "$LOG"; ss -ltnH | awk '{print $4}' | grep -E ':(879[0-9]|8890)$' | sed 's/.*://' | sort | tr '\n' ' '   # expected: 8791 (and 8795 if it was left up)
```

**Practice for the top-up: practice first (CC-437 ruling 7).** No registered line requires or forbids it; practice first is safe under both readings of addendum E3 §1 ("page, wording and answers are those of plan §2–§3") and CC-355 LC7 already records `practice_PI.jsonl` of the top-up folder. The practice address is given first (B3); the main address follows in M-B2 after the watcher below exits 0. The watcher records and does NOT stop the server: an early main answer in the top-up is a recorded departure, not a stop (D4).

```bash
T=$HOME/vsps_labels/xm600_gold_topup1
while :; do
  n=$( [ -f $T/practice_PI.jsonl ] && wc -l < $T/practice_PI.jsonl || echo 0 )
  m=$( [ -f $T/labels_PI.jsonl ] && wc -l < $T/labels_PI.jsonl || echo absent )
  [ "$n" -ge 69 ] && { echo "PRACTICE COMPLETE $(date -u +%FT%TZ): practice $n; main file: $m"; exit 0; }
  [ "$m" != absent ] && { echo "MAIN BEFORE PRACTICE $(date -u +%FT%TZ): main file $m lines, practice $n (recorded; server not stopped)"; exit 7; }
  ss -ltnH | awk '{print $4}' | grep -qE ':8791$' || { echo "SERVER GONE $(date -u +%FT%TZ)"; exit 8; }
  sleep 5
done
```

On exit 0 and his line "Đã xong vòng làm quen", write the practice-done line with counts only and NO sha (the N4 hazard of CC-371), then send M-B2:

`<UTC> | <ID>b-a-e3-topup-practice-done | top-up practice_PI.jsonl wc -l <n> (at least 69); main label file <absent | present, wc -l n> at this time; the main address is sent after this line (CC-437 ruling 7). Counts only.`

> M-B2: PI: vòng làm quen đã được ghi nhận. Trong cùng cửa sổ đó, mở phần chính: http://localhost:8791/ . Dòng trên cùng phải ghi "Người gán: PI".

On exit 7, follow D4. On exit 8, follow D9.

### B3. Message to the investigator (Vietnamese, exact)

> PI: trang phiên bổ sung (top-up) của bài A đã chạy trên cổng 8791, người gán: PI. Phiên có 1.755 câu trên 943 ảnh, sau 15 ảnh làm quen.
> 1. Mở một cửa sổ riêng tư mới và gõ địa chỉ vòng làm quen: http://localhost:8791/?practice . Khi trang báo "Xong vòng làm quen", gõ cho tôi: "Đã xong vòng làm quen". Tôi sẽ gửi địa chỉ phần chính; xin không mở phần chính trước đó.
> 2. Dòng trên cùng phải ghi "Người gán: PI". Nếu khác, dừng và nhắn tôi.
> 3. Trong phiên: làm một mình; không dùng công cụ AI, chương trình hay tra cứu; không mở localhost:8790 hay 8793; không mở tệp nhãn hay key.json nào.
> 4. Cho tới khi phiên bổ sung kết thúc, không mở: Mục 6.7 và Phụ lục S11 của bài A; các tệp sec1_introduction.md, sec7_verbosity_sign.md, sec10_discussion.md, sec11_limitations_ethics.md, supplementary.md, supplementary_SPIC.md, number_manifest.tsv; thư mục manuscript/prereg/2026-11-11_a_cert/paper_text/transfer/; A_CERT_RESULT.json; FREEZE_E3.json; hay bản dựng PDF, DOCX, diff nào của chúng.
> 5. Nghỉ ngắn thì cứ để nguyên trang. Khi dừng trong hôm nay, gõ đúng: "Tạm dừng phiên bổ sung, chưa xong". Khi đã trả lời hết (trang hiện "Đã trả lời hết các câu"), gõ đúng: "Đã trả lời xong toàn bộ phiên bổ sung trên localhost:8791".

[BASIS for item 4: CC-369 request 6, CC-377 P-4 (file names), CC-429 W3 and r13(b), CC-432 r8 ("until the closing line he does not open the seven files"). Item 3: CC-397 r2 (base page closed); CC-367 r3. The investigator was told the part-1 verdicts before the top-up; the disclosure that follows from this already stands (addendum E3 §8; CC-429 r12).]

### B4. Pauses and resume

- **Pause.** Run the session end (B5) with the pause statement. Each session end is an LC7 line ("Each session-end line …", CC-355 LC7).
- **Resume.**
  - Run B1 with these changes. Instead of `test ! -e`, check that the top-up `labels_PI.jsonl` wc and sha equal the last LC7 line. Check that the anchored count of `-a-e3-topup-start` and `-a-e3-topup-resume` lines (the grep of B1) equals the number of earlier `-a-e3-topup-session-end` lines. Practice is not repeated at a resume; the main address only.
  - Start by hand: `sessions.sh topup-start` refuses when the label file exists.

    ```bash
    setsid nohup python3 -B $REPO/tools/obj_rater/server.py --dir $T --annotator PI --port 8791 > $H/topup.out 2>&1 < /dev/null &
    ```

  - Write a resume line WITH 8-HEX PREFIXES ONLY. Any line that holds "topup1", including a cmdline or folder name, must not carry a full top-up label-copy sha before the e3-score run, except the LC7 lines (CC-371 W4 and ruling 7, the N4 hazard). Form:

    `<UTC> | <ID>-a-e3-topup-resume | CC-355 LC6 (resume; precedent OPS-1114x): nothing on 8790-8799 or 8890; top-up labels_PI.jsonl wc -l <n> sha256 <8hex> = last LC7 line <id>; server.py e3beb936, rater.html 84a90787, top-up assignment ceb87d0b; started on 127.0.0.1:8791, pid <pid>, annotator PI.`

  - [BY ANALOGY: OPS-1114x (base resume line) and addendum v1.1 step 4. The form: E6.]

### B5. Session end (LC7)

[BASIS:
- CC-355 LC7: UTC, wc and sha256 of `labels_PI.jsonl` and `practice_PI.jsonl`, the 444 copy, the assignment, server and rater shas, and the PI's statement whether the top-up is finished.
- CC-371 T5: the line holds the literal topup1, the PI's own "top-up finished" statement quoted, and the full sha of a 444 copy; the e3-score run uses that copy and that sha only.
- OPS-1114ac is the precedent for adding the gloss inside the statement.]

- **Finished.** Only when the investigator typed the finished sentence AND `wc -l < $T/labels_PI.jsonl` is at least 1,755. Otherwise write the pause form and ask.

  ```bash
  ID=OPS-1116<w>; idfree $ID
  $H/sessions.sh topup-end $ID "Đã trả lời xong toàn bộ phiên bổ sung trên localhost:8791 (typed about <HH:MM> VN <DD>-11) = top-up finished (CC-355 LC7; CC-371 T5; release event of CC-369 H-1 and H-2)"
  ```

- **Pause.**

  ```bash
  $H/sessions.sh topup-end $ID "Tạm dừng phiên bổ sung, chưa xong (typed about <HH:MM> VN <DD>-11) = top-up NOT finished (interim LC7 line; not the release event)"
  ```

The helper stops 8791 by pid after the cmdline check `--port 8791`. It makes the 444 copy and writes:

`<UTC> | <ID>-a-e3-topup-session-end | CC-355 LC7, topup1 (~/vsps_labels/xm600_gold_topup1): labels_PI.jsonl wc -l <n> sha256 <64hex>; 444 copy labels_PI.<UTC>.jsonl sha256 <64hex> (same sha); practice_PI.jsonl …; assignment ceb87d0b, server e3beb936, rater 84a90787; PI statement: "<statement>"; server on 8791 stopped. Counts and shas only.`

If `labels_PI.jsonl` does not exist (a stop during practice), the helper's copy step fails before any line is written. Write the LC7 line by hand with "labels_PI.jsonl absent".

### B6. Confirmations to ask afterwards (investigator, typed)

> Tôi tự trả lời một mình phiên bổ sung, không dùng công cụ AI, chương trình hay tra cứu; trong phiên tôi không mở localhost:8790 hay 8793; trước dòng kết thúc phiên bổ sung tôi không mở Mục 6.7, Phụ lục S11 hay tệp nào trong danh sách ở mục 4 của tin nhắn mở phiên.

- If he opened a held line or file: one LOG line with the time and the file name and no figure. The CC-369 sentence takes its replacement clause, and row E6 is read as not blind (CC-429 r12). [BASIS for the held-file clause: CC-429 r12.]
- The alone and no-AI clauses: [BY ANALOGY: CC-415 W2.]

---

## C. The closing line, what it releases, what stays barred

- **No template.** The XM600 plan defines no closing line, only session-end lines (CC-353 W8). The held-study "closing line" of CC-429, CC-432 and others is the H-1 release line.
- **The release event.** H-1 releases at the LATER of (a) the base end line OPS-1114ac, which exists, and (b) the top-up LC7 line with the investigator's "top-up finished" statement (CC-369 H-1; CC-429 l.117-118). H-2 has the same release line for FREEZE_E3 and Annex B rows B2-B4 (CC-369 H-2; CC-386 r8; CC-429 l.127).
- R2's last end line is NOT an H-1 condition. It conditions the per-annotator display hold (CC-391 4(b)).
- **The coordinator's release line.** Right after the final LC7 line, the coordinator writes one LOG line naming which condition fired (CC-429 r13(f)). Then the CC-429 rule-13 banner rules end, and Part A of the report is refreshed from the paper. It is written only after an LC7 line of the "finished" form (B5). Form, ruled by CC-437 ruling 11:

  `<UTC> | <ID>-a-h1-release | CC-369 H-1 and H-2 release line (CC-429 ruling 13(f)): condition that fired = (b) top-up session-end line <LC7 id> with the PI's 'top-up finished' statement; (a) OPS-1114ac-xm600-session-end already on record. Banner rules of CC-429 ruling 13 end for the investigator. R2 status at this line: <last R2 line id, finished yes | not finished | no R2 session yet>. Still held: E-rows (E3 result read), H-3, kappa figures, per-annotator rows, everything to R2.`

  Then the message to the investigator, exact:

  > PI: phiên bổ sung đã đóng và tôi đã ghi dòng mở khoá. Từ giờ PI có thể mở Mục 6.7, Phụ lục S11 và các tệp trong danh sách ở mục 4 của tin nhắn mở phiên. Vẫn chưa mở: các hàng E1 đến E6 của phiên bổ sung (chờ lượt đọc kết quả), số kappa và các hàng theo từng người gán (chờ mở niêm phong riêng). PI vẫn không nói với R2 về bất kỳ câu trả lời hay con số nào cho tới khi tôi báo kappa đã được mở niêm phong<; R2 chưa xong: vẫn không nói gì về nghiên cứu với R2>.

- **What the release frees.**
  - The investigator may open Section 6.7, S11 and the files of B3 item 4: CC-369 request 6, CC-377 P-4, CC-432 r8.
  - The Annex B rows file may be committed after a gatekeeper byte match and an n-gram scan (CC-386 r7). Paper use needs its own transfer read.
  - The per-annotator run may be placed after this line (CC-419 r4).
- **Still barred after the release line.**
  - **E-rows (E1-E6).** Until the E3 result read (CC-369 H-2).
  - **e3-score.** Runs once, only when CC-371 T1-T12 hold. The start line carries 8-hex prefixes only (CC-371 W4). There is no rerun without a judge.
  - **H-3.** The part-3 repeat-agreement figure and the part-2 rows, until their own unsealing result read (CC-369 H-3).
  - **Kappa.**
    - It is computed only after R2's end line "R2 finished all screens yes", the separate unsealing line, and its one-judge result read (CC-367 7(c); `a_cert_kappa.py`, committed 73d7cf8).
    - Until then every label-based number carries "single annotator" (plan §4; CC-367 7(c)).
    - If R2 never finishes, E12 applies.
  - **Per-annotator rows.**
    - Run once, only after the commit be2b59b, the L-e, L-f (main) and LAST L-g lines, the U-P line and the operator evidence (CC-395 r10; CC-419 r4).
    - The display is held until the later of L-e, R2's LAST L-g and the top-up end line (CC-391 4(b)).
  - **R2.** Never shown anything from the per-annotator run (CC-391 4(c)), nor any answer until the kappa unsealing (CC-369 H-4; CC-367 r4).
  - **Base labels.** No line ever added (CC-397 r2).
  - **R2 top-up overlap.** Not built, not licensed (CC-355 N9, CC-367 7(d)).
- **Why R2 first.** If the release came before R2 had finished, the investigator could read H-1 figures while R2 still had to label. H-4 would then rest on his silence alone. This is the reason behind CC-397 r5(d)'s recommendation.

---

## D. Deviations: what to do

| # | Case | Action | Basis |
|---|---|---|---|
| D1 | A rating server already listens (8790, 8791, 8792 or 8793) at a precondition check | (1) No start. (2) Identify it by `/proc/<pid>/cmdline`. (3) Compare its label file by `wc -l` and sha256 with the last logged end line or pin: base d338896f (4,681 lines); Paper B closing pins 91fa0a30 and 65f1527d; R2 and top-up: the last end line, or "absent". (4) If equal: stop by pid after the cmdline check and write one DEVIATION OPS line. (5) If any file changed or exists unlogged: stop by pid, open nothing, go to a judge. | CC-367 r3; CC-397 r2 (base: a later line = stop all R2 work, judge); CC-367 r6 (R2 files); OPS-1114al (precedent: autostart server stopped by pid after a cmdline check, file equal to its 444 copy); top-up file changed: NO BASIS FOUND, judge |
| D2 | A gate, a cloudflared process or an active tunnel service exists | Stop a user process by pid after a cmdline check. A root service: ask the investigator to stop it. No session while any runs. | Addendum v1.1 steps 1 and 9 and INC-1115a, BY ANALOGY (written for remote sessions) |
| D3 | Practice skipped by R2: `labels_R2.jsonl` appears before practice is complete (watcher exit 9) | The watcher has stopped 8793. Open nothing. One INCIDENT line with `wc -l` and sha of both R2 files. If `labels_R2.jsonl` has at most 20 lines and this is the first such event: restart by the resume form of A7 (the line names the INCIDENT id), the investigator opens the PRACTICE address again and says only "Trang phần chính bị mở sớm. Xin làm xong vòng làm quen trước."; then A5 as written. More than 20 lines, or a second event: no restart, a one-judge read. No answer is deleted or set aside. | CC-437 ruling 5 (fixed before any R2 answer); CC-367 r6; CC-404 ruling 1; CC-406 r6 lesson |
| D4 | Main before practice in the top-up (watcher exit 7) | The server is NOT stopped. Send: "PI đang ở phần chính trước vòng làm quen. Xin dừng tay, mở http://localhost:8791/?practice, làm xong vòng làm quen rồi mới quay lại phần chính; không quay lại (Backspace) các ảnh đã trả lời trước đó." One OPS line with the two line counts and no sha. Run the watcher again until exit 0. | CC-437 ruling 7; CC-404 ruling 1 (must-not list), BY ANALOGY |
| D5 | R2 stops half-way | Session end with `no` (A8). Resume another day (A7). | CC-397 r5(a); resume form E6 |
| D6 | R2 never returns, or never finishes | No kappa; "single annotator" everywhere (plan §4; CC-367 7(c)). Partial R2 labels enter no registered statistic: the committed kappa code refuses an incomplete R2 file and the per-annotator code needs the end line with `yes`. The file is kept unopened, by wc and sha. Any other use is post hoc and needs its own judge read before a byte is opened. | CC-437 ruling 12; plan §4 l.37 ("every question of the 150 images"); CC-367 7(c); `a_cert_kappa.py` l.217-218; `a_cert_perann.py` l.282 |
| D7 | The wrong person rates: not the R2 of PI-1114e and PI-1114f, or the investigator, or a program or AI. For the top-up, anyone but the investigator. | Stop by pid at once. Open nothing. `wc -l` and sha only. One INCIDENT line. A judge. No second attempt under the code R2 without a ruling. | CC-367 r4 (who may be R2); CC-415 r2 (Paper B: such a file is not R2's data; no second attempt under R2), BY ANALOGY; top-up: NO BASIS FOUND, judge |
| D8 | The investigator watched, explained beyond M-A2, or discussed an item | He states exactly what, and for how many screens, in the A9 line. A one-judge diff read before any use. | CC-415 r2 (not an automatic fail; comes back to a judge), BY ANALOGY |
| D9 | The page does not load, the header is not "Người gán: R2" or "Người gán: PI", the red warning lasts more than one minute, or the server is gone (watcher exit 8) | Stop the server by pid if it still runs, after a cmdline check. Write the session end with `no`, or the LC7 pause line. Find the cause and log it before any restart. | CC-367 r3 (header); addendum v1.1 step 7, BY ANALOGY |
| D10 | R2 asks an item question | Pointer sentence only. Record the question and the text pointed to in one OPS line, with no item content. | CC-397 W3 and r3; OPS-1114bb precedent |
| D11 | WSL restarts during or after a session | `~/.bashrc` lines 128 and 130 restart 8787 and 8788. During R2's session, stop them again (A1). The rating server is gone: answers are fsynced per click (`server.py` l.82-88). Check wc and sha. Resume by A7 or B4 with a deviation note. | OPS-1114al precedent; resume form E6 |
| D12 | Anything of the study reaches R2 (a dashboard, a file, a word) | Stop, record facts, judge. | CC-369 H-4; CC-391 4(c) |
| D13 | The investigator opened a held file before the top-up end | One LOG line with the time and the file name. CC-369 replacement clause. Top-up rows stay usable. | CC-429 r12 |
| D14 | `labels_R2.jsonl` is present when the practice-done line is due, although the watcher exited 0 (the main page was opened before M-A3, after at least 69 practice lines) | No stop. The practice-done line says "present" with its line count. The investigator states in his confirmation whether the page had shown "Xong vòng làm quen" before the main page was opened. If he cannot affirm it: a one-judge diff read before the kappa unsealing. | CC-437 ruling 5 |
| D15 | At a resume, the first screen shows selected answers of R2 to the investigator during his header check | He presses nothing and steps away. He reports the number of rows in his confirmation; the session-notes line records it. More than one screen seen: a one-judge diff read before the kappa unsealing. | CC-437 rulings 6 and 10 |
| D16 | The investigator opened the chat window while R2 sat at the screen, or a study window, the dashboard or a terminal was visible to R2 | He states what was visible and for how long. One OPS line. If an outcome, a figure, a caption or an answer of his was visible: stop, and a judge before any further R2 session (D12). | CC-437 ruling 2; CC-369 H-4 |
| D17 | The investigator's confirmation (A9) does not affirm one of its first three clauses, or does not arrive | The file is not R2's data until a judge has read the case. It is kept unopened, by wc and sha, never deleted. No kappa unsealing line. No second attempt under the code R2 without a ruling. | CC-437 ruling 9; CC-415 ruling 2 |

**Are the labels still usable as registered? (CC-437 ruling 14)**

| Case | R2 labels (registered kappa, plan §4) | Top-up labels (rows E1 to E6, descriptive) |
|---|---|---|
| D1, D2 with every file equal to its last logged state | yes | yes |
| D1 with a file changed or unlogged | held for a judge | held for a judge |
| D3 within its bound (at most 20 lines, once) | yes, with the disclosure sentence of CC-437 ruling 5 | not concerned |
| D3 beyond its bound | held for a judge | not concerned |
| D4 | not concerned | yes, with the disclosure sentence of CC-437 ruling 7 |
| D5, D9, D10, D11, D14 (end text affirmed), D15 (one screen) | yes | yes |
| D6 | no: no kappa, "single annotator" stays | not concerned |
| D7, D17 | no, unless a judge rules otherwise | D7 in the top-up: held for a judge |
| D8, D12, D16 with study content shown, D14 or D15 beyond their bounds | held for a judge | not concerned |
| D13 | not concerned | yes; the CC-369 sentence takes its replacement clause and row E6 is read as not blind (CC-429 r12) |

---

## E. Steps without a basis, or resting on analogy (for one judge read)

Every row of this table is ruled by CC-437: row E<n> by its ruling <n>. Where a status cell still reads NO BASIS FOUND or BY ANALOGY, the ruling is the basis.

| # | Step | Status |
|---|---|---|
| E1 | **In-person mode for Paper A's R2.** Addendum v1.1 superseded, "for R2 only", in both papers: CC-367 r3 (the operator's header check), CC-367 N4 ("on the same laptop"), the CC-397 W3 room rules, and CC-397 r3's card delivery medium and order. CC-398 r1 overruled them "for this reason: R2 is not at the laptop". No Paper A ruling restores them for an in-person session. CC-415 r4 accepted in-person after the fact for Paper B only. PI-1116b records the investigator's decision that R2 rates at his machine. The judge must say: (i) whether CC-367 r3 and N4, CC-397 W3 and the CC-397 r3 delivery apply again as written; (ii) which Paper A disclosure sentence is used: the CC-367 N4 in-person form, or the CC-398 remote sentence (which would be false). | **NO BASIS FOUND: needs a judge read before the session. BLOCKING for A3.** |
| E2 | **The investigator's chat window during R2's session.** CC-397 W3 says "the chat … closed". The coordinator session runs in that window, so closing it ends the session. The runbook minimizes it. He uses it only before R2 sits down (header line) and after R2 has left (end line). | NO BASIS FOUND: needs a judge read before the session |
| E3 | **The fixed "Lời nói với R2" text**, and the investigator, not R2 alone, prompting R2 to read the guide, then the card, before practice. | NO BASIS FOUND as a fixed text (BY ANALOGY: M1 of addendum v1.1; CC-397 r3 order): needs a judge read before the session |
| E4 | **Stopping 8788 (label console) and 8787 (dashboard)** during R2's session. 8788 did not exist when CC-397 W3 was written. 8787 is "closed" in W3, but the writer found 3 dashboard strings with an outcome word and a Paper A token. | BY ANALOGY: CC-397 W3, CC-369 W10 |
| E5 | **The practice watcher, the 69-line threshold, the practice-done line, and stop (not continue) on early main answers** in an in-person main session. | BY ANALOGY: CC-367 r6 (practice-only session); addendum v1.1 steps 5 and 7 (remote); CC-406 r6 lesson; OPS-1111be precedent; CC-415 r1 continued for Paper B under a deadline |
| E6 | **Resume start lines for R2 and the top-up.** Neither helper supports a resume. | BY ANALOGY: addendum v1.1 step 4; OPS-1114x. The form: NO BASIS FOUND: needs a judge read before a resume |
| E7 | **A practice round in the top-up.** | NO BASIS FOUND: needs a judge read before the top-up. Recommended: practice first |
| E8 | **Short breaks with the server up.** | NO BASIS FOUND: needs a judge read before the session |
| E9 | **The confirmation lines of A9, and refusing "yes" in the L-g line below 1,110 lines** (1,755 for the top-up). | BY ANALOGY: CC-415 W2/W7, CC-417 r3; CC-397 r2 count reasoning |
| E10 | **"The investigator never reopens localhost:8793"** after R2's session. The page reloads `/state/assignment` and shows R2's selections, which would expose R2's answers before his top-up (old repeats on overlap images). | NO BASIS FOUND as a named rule (follows from CC-367 r3 and r4): judge to confirm |
| E11 | **The form of the H-1 release line** (section C). Its content is ruled by CC-429 r13(f). | NO BASIS FOUND: needs a judge read |
| E12 | **Use of partial R2 labels** if R2 never finishes. | NO BASIS FOUND: judge, only if it arises |
| E13 | **Wrong person in the top-up; a changed top-up label file found at a precondition check.** | NO BASIS FOUND: judge, only if it arises |

## F. What must be built or ruled before the first session

- **Ruled.** CC-437 rules E1 to E13. Its id stands in A2's prerequisite loop and in A3's start line.
- **To do before R2's session, all on the laptop (file writes, hashes and one commit; no test, no study data, no rented host):**
  1. Apply the edits of CC-437 Annex R to this file and check the end-state sha256 (CC-437 W1).
  2. Save the session sheet by the command of CC-437 Annex S, mode 444, and check its sha (W2).
  3. Commit this file at its end state through the gatekeeper; the message names the CC-437 sha (W3).
  4. Send M-0 and log the investigator's answer as a PI line (W4).
  5. Re-hash the pins and run the checks of A1 and A2. The writer and the judge did not hash the home copies, by custody.
- **Built already, by LOG.** The R2 folder, the top-up folder, the card, the pins and the commits (section 0).
- **Helpers.** No helper change: the R2 start line is written by hand (A3), and the resume lines by hand (A7, B4). `bash -n` on a copy of the three loops (A5, A5b, B2) is a parse, not a test, and may run on the laptop.
- **Not to build.** The R2 top-up overlap set (CC-355 N9, CC-367 7(d)).
