"""Build A_E3_ARM_RUN_DOC_v1_1.md from v1 (f0a375fb) by exact-once replacements, one per CC-349 item.

Run from the repo root: python3 -I -B manuscript/prereg/2026-11-12_a_e3_arm/build/make_run_doc_v1_1.py
The "Changes from v1" block is generated from the same list, so it cannot drift from the edits.
"""
import hashlib
import pathlib

D = pathlib.Path("manuscript/prereg/2026-11-12_a_e3_arm")
SRC, DST = D / "A_E3_ARM_RUN_DOC_v1.md", D / "A_E3_ARM_RUN_DOC_v1_1.md"
V1_SHA = "f0a375fb6a12f97efe3f91d6932e084f9d9131d24b7b48162d29ba24e4b9a1d6"
WRITTEN = "2026-11-12T02:45Z (09:45 VN)"

# (code, what changed, old, new)
EDITS = [
    ("CC-349 decision", "title names v1.1",
     "# A-E3 run document v1: ",
     "# A-E3 run document v1.1: "),
    ("W7", "§0: the host is hc2, not a second host",
     "The PI agreed to a second RTX 3090 host (coordinator brief, 11-12).",
     "The PI agreed to a second RTX 3090 host (coordinator brief, 11-12); under CC-349 ruling 3 the arm runs on hc2 instead (§7)."),
    ("W5", "§1 draft disclosure: four of the twelve stored sets (Qwen3-VL T05/T08) are sampled, not greedy",
     "\"All captions on the 600 XM3600 images, the earlier ones and the four added models, were decoded greedily one image at a time. The added models",
     "\"All captions on the 600 XM3600 images were decoded one image at a time; the four added models and the greedy (T0) stored systems used greedy decoding, the T05/T08 Qwen3-VL sets temperature sampling. The added models"),
    ("W7", "§2.1 Aya cell: literal path of C's copy",
     "**yes**, `$NCS_DATA/models/c_t1_aya_vision_8b` (C's tree; read-only reuse via `A_E3_SNAP_aya_vision_8b`)",
     "**yes**, `/root/ncs-data/models/c_t1_aya_vision_8b` (C's tree; read-only reuse via `A_E3_SNAP_aya_vision_8b=/root/ncs-data/models/c_t1_aya_vision_8b`)"),
    ("Q3", "§2.1 Gemma pins: from the Hub API LFS sha256 only (ruling 2)",
     "Fill them from the authenticated tree API at this revision before any fetch (P2)",
     "Fill them only from the Hub API LFS sha256 at this revision, never by hashing fetched files, before the registration commit; the call is named in the registration `statement` (P2; CC-349 ruling 2, W6)"),
    ("Q14", "§2.3: no lineage sentence; name the language models only",
     "Whether a sentence about language-model lineage relative to the Qwen systems may be printed is left to the judge (Q14), because a reworded \"non-Qwen\" is barred.",
     "No sentence about language-model lineage relative to the Qwen systems is printed (CC-349 Q14): a reworded \"non-Qwen\" is barred. Naming each language model as read from `config.json` at the pin is enough."),
    ("W1-W4", "§4: the job script was revised; its sha is the one in SHA256SUMS_E3",
     "| written with this document, sha256 `afa035bbc26814d8593da95c6b65609596387604fe230158afcc92a9a61de68a` (Q8) |",
     "| v1 sha256 `afa035bbc26814d8593da95c6b65609596387604fe230158afcc92a9a61de68a` (read in CC-349, Q8); revised for CC-349 W1-W4 and the W7 launch line (`scripts/a_e3/A_E3_JOB_W.diff`); its sha256 is the one in `SHA256SUMS_E3` |"),
    ("W4", "§6.2 G1: the custody gate",
     "`sha256sum -c SHA256SUMS_E3` (in the job) | STOP |",
     "`sha256sum -c SHA256SUMS_E3` (in the job); then the custody gate (in the job, W4): no `data/` in the A-E3 tree, `$NCS_DATA/datasets` holds only `xm600`, and that dir holds exactly 600 regular `*.jpg` files and nothing else | STOP |"),
    ("W3", "§6.2 G4: an English caption needs at least one ASCII letter",
     "7b: share **without** such marks ≥ 0.95 |",
     "7b: share of captions with no such mark **and** at least one ASCII letter ≥ 0.95, so an empty caption fails (the 7a definition is unchanged) |"),
    ("N1", "§6.2 G4: the 50-image outputs decoded so far are kept",
     "Its two 50-image outputs are kept and counted |",
     "Its 50-image outputs decoded so far are kept and counted |"),
    ("W1", "§6.2 G6: the cap is hard on every attempt",
     "+ 600 × (that model's 50-image seconds / 50) ≤ 36,000 s | CAP STOP: that run and all later runs are NOT RUN (S5) |",
     "+ 600 × (that model's 50-image seconds / 50) ≤ 36,000 s. Also, before every attempt of any run (50- or 600-image), its timeout is cut to 36,000 s − spent | CAP STOP: that run and all later runs are NOT RUN (S5). A run killed by the cut keeps its partial file and is reported NOT RUN |"),
    ("W1", "S3: timeouts are cut to the cap remaining",
     "max(1,800 s, 2 × projected) for a 600-image run.",
     "max(1,800 s, 2 × projected) for a 600-image run; each is cut to the cap remaining (S5)."),
    ("W2", "S4: coded with a counter",
     "Two D1 failures in a part also stop that part, because a host-level cause is likely.",
     "Two D1 failures in a part also stop that part, because a host-level cause is likely. The job counts them per part and at the second logs `PART STOP: two D1 failures (S4)`."),
    ("W1, Q1", "S5: the cap is hard; cut order; when the PI line is asked (ruling 4)",
     "  - If the cap stops 7b, the cut runs are reported NOT RUN, and the PI line (§12) applies.",
     "  - The cap is hard: before each attempt of every run, 50- or 600-image, the job cuts the timeout to `CAP_S − spent`. A run killed by that cut, or one with no cap left, logs `CAP STOP at <run>`, its partial file is kept, and it and every later run are NOT RUN.\n"
     "  - The cap cuts in the registered order, so 7b's last models go first.\n"
     "  - The PI line (§12) is asked only if a 7b CAP STOP actually happens, or at `JOB DONE 7a` if spent_7a + the 7b projection (from the 7a 50-image rates) exceeds 36,000 s."),
    ("W7", "§7: host choice set to hc2 (ruling 3)",
     "**Host choice (recommended: a second host of the registered class, machine id `ae3`).**\n"
     "- hc2 (machine id `h1`) runs C block 1b. Projected end is about 14:05–14:45 VN today, with a cap stop at about 20:00 VN at the latest (LOG l.2225).\n"
     "- Under CC-346 R5, only nice-19 CPU checks of another paper may run there meanwhile. A fetch or decode may not.\n"
     "- On hc2, 7a could start at about 15:00 VN at best. On a second host rented after this document's GO, it could start about 3 h after T0 (fetch about 57 GB, venv from the locked freeze, selftest).\n"
     "- If the PI's labelling days matter more than one rental, take the second host (Q5).\n"
     "- The A-E3 tree then never touches C's tree.\n",
     "**Host: hc2 (machine id `h1`), CC-349 ruling 3 (Q5).** HC3 is gone, and PI-1112b bars an idle rented GPU.\n"
     "- hc2 runs C block 1b. Projected end is about 14:05–14:45 VN today, with a cap stop at about 20:00 VN at the latest (LOG l.2225).\n"
     "- A-E3 decodes start only when all of these hold: block 1b shows JOB DONE and its RUNNING file is gone; the 1b outputs are pulled, verified against their SHA256SUMS and made 444, with the OPS line written; the round-2 diff read (CC-349r2) and the commit are done.\n"
     "- If the round-2 read and the commit are not done when the 1b pull is verified, the arm is not staged and PI-1112b applies at once (pull, verify, delete the host), unless the PI answers CC-349's conditional question otherwise.\n"
     "- C's scoring stages may run CPU-only under `nice -n 19` beside the A-E3 decodes (CC-348 (b), cited in CC-349 ruling 3(b)). One OPS DEVIATION line gives the start and end of every C stage that runs beside A-E3. The A-E3 start line records `free -g` and `df -BG /root`. No C decode job (block 2) starts while `/root/a_e3/out/RUNNING` exists.\n"
     "- Staging while 1b decodes (CC-349 ruling 3(c), a recorded narrow overrule of CC-346 ruling 6 / R5): network, disk and light hashing only, no model load, no GPU, no decode; every command under `nice -n 19 ionice -c3`, one model at a time; `df -BG /root` shows at least 100 G before the first fetch and at least 40 G after it; nothing under `/root/ncs-data`, `/root/outputs` or the HF hub cache (`HF_HOME=/root/a_e3/hf`, fetch with `/root/venv-lb/bin/python`); no archive left on disk; one OPS DEVIATION line per item. These fetches are unverified staging; the only pin check is G3 under the committed registration.\n"),
    ("W7", "§7: layout is hc2's",
     "**Layout (either host):**",
     "**Layout (hc2):**"),
    ("W7", "§7: Aya reuse path is literal",
     "  - On hc2, Aya is reused read-only via `A_E3_SNAP_aya_vision_8b=$NCS_DATA/models/c_t1_aya_vision_8b`.",
     "  - On hc2, Aya is reused read-only from C's tree via `A_E3_SNAP_aya_vision_8b=/root/ncs-data/models/c_t1_aya_vision_8b` (a literal path: the job sets `NCS_DATA=/dev/shm/a_e3`, so `$NCS_DATA/models/...` would be a missing dir and Aya would be skipped)."),
    ("W7", "§7: on hc2 orders 2-5 are fetched (Aya reused, ruling 3 S-2); SmolVLM2 only if df allows (ruling 3(c))",
     "Fetch orders 1–5 before 7a starts (SmolVLM2 is 9 GB)",
     "Fetch orders 2–5 before 7a starts (SmolVLM2 is 9 GB and waits until needed if `df` does not allow it, CC-349 ruling 3(c))"),
    ("W4", "§7 custody: true for hc2",
     "- No gold on the host: no human label, no `key.json` or `assignment.json`, no OIV7 labels or class map in the A-E3 tree, no XM3600 references.",
     "- No gold in the A-E3 tree, its data dir or its outputs: no human label, no `key.json` or `assignment.json`, no OIV7 labels or class map, no XM3600 references. On hc2, C's full clone `/root/vsps` holds the tracked `data/xm3600/oiv7_labels.json` and `vi_oiv7_map.json`, and C's dev datasets (including XM-dev500, disjoint from the 600, as is XM-test2500: 0/0 ids). The A-E3 job reads none of them. The job's custody gate (§6.2 G1) stops if the A-E3 tree has a `data/` dir or `$NCS_DATA/datasets` holds anything but the 600 images."),
    ("W7", "§8 step 5: no second host to delete",
     "delete the second host, do L-after,",
     "delete hc2 when no approved job remains on it (PI-1112b), do L-after,"),
    ("W7", "§9.1: pull path on hc2",
     "The server, page and wording are unchanged.",
     "On hc2 the pull copy is `.session_backup/machines/ATTR_H1/root/a_e3/out/` (§8 step 1); the command then uses that path in place of `machines/AE3`. The server, page and wording are unchanged."),
    ("W7", "§9.3 timing: the hc2 line",
     "1. Judge read and commit by about 09:00.\n"
     "2. Second host T0 about 09:00 and ready about 12:00.\n"
     "3. 7a finished about 16:00–20:00 (§10: 3.7–7.6 GPU-h).\n"
     "4. Pull, build and code-read top-up ready about 1 h later.\n"
     "\n"
     "On hc2 instead: about 19:30–23:30.\n",
     "1. Round-2 diff read and commit before 07:00Z (14:00 VN).\n"
     "2. C block 1b ends, is pulled and verified about 14:00–14:45; 7a starts on hc2 right after.\n"
     "3. 7a finished about 19:30–23:30 (§10: 3.7–7.6 GPU-h).\n"
     "4. Pull, build and code-read top-up ready about 1 h later.\n"),
    ("W7", "§10: earliest finish on hc2",
     "so the earliest finish is about 16:00 VN on a second host.",
     "so the earliest finish is about 19:30 VN on hc2 (§9.3)."),
    ("W7, Q5", "§12 Q5: hc2",
     "| Second host. The top-up is about 3–4 h earlier, and C's tree and guard stay untouched. Use hc2 only if no offer passes the spec within 2 h. |",
     "| CC-349: hc2 (ruling 3), not a second host; the recommendation was overruled on the changed facts (HC3 gone, PI-1112b). |"),
    ("N6, Q8", "§12 Q8: no separate dry run",
     "| Read it as code in this round. Its host check is G2 plus a dry run on the host (laptop rule PI-1111: no test runs on the laptop). |",
     "| Read it as code in this round. CC-349: there is no separate dry run; the host check is `bash -n`, G2 inside the job, and the first model's 50-image runs as the smoke step. |"),
    ("Q11", "§12 Q11: one session after all of 7a; split not licensed",
     "| One session after 7a. Split only if 7a has not finished by 18:00 VN: then `topup1` uses the models done by then, and `topup2` the rest, with the same wrapper. |",
     "| CC-349: one session after all of 7a. The 18:00 VN split (topup1/topup2) is not licensed; it may be added only in the build_topup read, with a mid-run pull rule. |"),
    ("Q14", "§12 Q14: no lineage sentence",
     "| Judge to rule. Default: no such sentence; name the models and count the families only. |",
     "| CC-349: no. Name each language model as read from `config.json` at the pin (Command R7B, Gemma 3, Llama 3.1, Llama 2); naming them is enough. |"),
    ("Q1-Q14", "§12: CC-349's answers recorded under the table",
     "**PI line (only if needed):** if S5 cuts 7b below its 4,800 captions, may the cap rise from 10 to 14 GPU-h for 7b only?",
     "**CC-349 answers (§6 of the ruling):** Q1 yes, one hard 10 GPU-h cap over 7a + 7b, 7a first, the 6/4 split a projection only. Q2 no, InternVL3 out, no fifth row. Q3 accept; order 6 dropped unless its pins are committed. Q4 accept; 7b gets the W3 fix. Q5 hc2. Q6 accept. Q7 accept in principle, bound in the build_topup read and addendum E3. Q8 accept after W1-W4, no separate dry run. Q9 yes, a writer item. Q10 decode 7b, score it on the English reference ladder only, no gap claim. Q11 one session after all of 7a. Q12 covered, no PI line. Q13 keep 60/160 and the defaults, disclose, log hit_max counts. Q14 no lineage sentence.\n"
     "\n"
     "**PI line (only if needed; CC-349 ruling 4):** asked only if a 7b CAP STOP actually happens, or at `JOB DONE 7a` if spent_7a + the 7b projection exceeds 36,000 s: may the cap rise from 10 to 14 GPU-h for 7b only?"),
]


def main():
    raw = SRC.read_bytes()
    assert hashlib.sha256(raw).hexdigest() == V1_SHA, "v1 sha differs"
    text = raw.decode("utf-8")
    for code, what, old, new in EDITS:
        n = text.count(old)
        assert n == 1, f"{code} ({what}): found {n} times"
        text = text.replace(old, new)
    changes = "\n".join(f"- **{code}**: {what}." for code, what, _, _ in EDITS)
    head = "Nothing was run, rented, fetched or committed, and no LOG line was written."
    assert text.count(head) == 1
    block = (f"\n\n**v1.1** written {WRITTEN} from v1 (sha256 `{V1_SHA[:8]}…`) by "
             f"`build/make_run_doc_v1_1.py`, for CC-349 (conditional GO 86). No decode before the round-2 diff read "
             f"(CC-349r2) reads \"W1-W7 CLOSED, no new BLOCKING\" and the gatekeeper commit.\n\n"
             f"**Changes from v1** (each by its CC-349 item; nothing else changed):\n{changes}\n")
    # the block goes after the paragraph that ends the header (line 3)
    end = text.index("\n", text.index(head))
    text = text[:end] + block + text[end:]
    DST.write_text(text, encoding="utf-8")
    print(DST, hashlib.sha256(text.encode("utf-8")).hexdigest(), len(EDITS), "edits")


if __name__ == "__main__":
    main()
