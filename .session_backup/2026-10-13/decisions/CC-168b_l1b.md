CC-168b: L1-b DEV-EXPLORE round 2. Re-read of the W1-W15 fixes from CC-168 (round 1, GO-with-fixes 91%). Files read: PREREG_DRAFT 527f86be, l1b_registry cd210a7c, l1b_split b749f720 (unchanged), GATES.json, l1b.py a7f65ce9, l1b_job.sh 3c260686. Single judge, reversible tier >= 90 (PI-1029o). This is AI opinion, not expert-validated.

DECISION: GO-with-fixes. W1-W5 are applied correctly. One new item, W16, is blocking at finalisation. It is rule text only and lands in the same pin diff. After that:
1. finalise: rename to PREREG.md, set the 3 pins, regenerate both SUMS;
2. the gatekeeper does a pins-only sha/diff check (CC-165a pattern);
3. the LOG line;
4. the gatekeeper commit.
The job still cannot start until G1 and G3 are closed by LOG ids (CC-165 r4 and CC-168 r6 are kept).
CONFIDENCE: 92%. Every remaining item is mechanical or text. Nothing has run, so no output exists that a fix could be fitted to.

## Checked (by me)
- SUMS: prereg 3/3 OK and scripts/l1b 8/8 OK, verified from the repo root. Both directories are untracked. scripts/l1b/__pycache__ is absent, and root .gitignore l.1 ignores __pycache__/.
- `python3 scripts/l1b/l1b.py --selftest` gives 41 ok. The scratchpad torch venv gives 42 ok, including tiny-LLaVA cached = full < 1e-4 nats. `bash -n l1b_job.sh` is OK.
- Pins: PREREG_SHA256, L1B_REG_SHA256 and SPLIT_SHA256 are still None (l1b.py l.39-41), so guard, model_spec and score refuse. Finalisation is still pending, as expected.
- No PI answer on the G1 question appears in LOG.md after CC-168 (16:30:20Z). G1 stays binding.
- Hygiene: no IP, host, port or e-mail string in the 6 files.

## W-items from round 1
- W1 (gemma pins): APPLIED as a guard, with one rule gap (W16).
  - The 4 asterisk values are now null (registry; kind sha256).
  - pins_complete() (l.270) requires 64-hex or 40-hex. nonqwen_ok() (l.276) adds "gate G3_gemma open". model_spec() (l.330) refuses before any fetch or check_snapshot. The job runs `nqok` before `fetch` and skips on failure.
  - Selftests "pins: a null or masked LFS hash is incomplete" and "gates: G3_gemma empty/filled" pass.
  - The 401 / masked-oid explanation is plausible, and I did not contact HF.
  - I accept null + skip as satisfying W1, with one condition. Filling the 4 hashes changes the registry sha, then L1B_REG_SHA256 in l1b.py, then l1b.py's own sha. That sha is in the rerank run key (l.494-495). The job also overwrites code_at_start.sha256 at every start (job l.41). And check_prov (l.581-588) requires each header's l1b_sha256 to equal both code_at_start and the current l1b.py.
  - So a gemma fill made after any L1-b output exists makes `score` refuse every file already written. It fails safe, not silently, but the run becomes unscoreable.
  - Hence W16: gemma is enabled before finalisation or never in this run.
  - In practice this is round 1's option 2 (idefics3_8b as the non-Qwen backbone in use) unless the PI clicks before finalisation.
- W2 (run both): APPLIED.
  - The job loops `for m in gemma3_4b idefics3_8b` with no `break`, and each skip, fetch failure or parity failure moves on. The Qwen reranks follow.
  - score picks the first assessable non-Qwen model in that order (`nq = [...][:1]`). The other one is forced not-in-use, and outcome() sees it as assessable False.
  - §3, §7 (order; design ~5 GPU-h, ~4.2 without gemma; cap 8), the job header and the registry role text all agree.
- W3 (GATES): APPLIED.
  - The three keys are present and gates_open() checks G1 and G3. G3_gemma gates gemma only, and selftests cover missing / empty / filled.
  - Format note: gates_open fullmatches ONE id, `(OPS|CC|PI)-\d{4}[A-Za-z0-9-]*`, so the string "PI-1029l + PI-1029q" would never close G3. The gatekeeper fills G3 with "CC-168", the ruling whose r6 accepts both PI ids (W18).
- W4 (score robustness and provenance): APPLIED in code (l.613-624).
  - W4a: a missing sidecar is NOT_ASSESSABLE only if CAP_STOP.json exists; otherwise score refuses.
  - W4b: check_prov checks the split, prereg, l1b and job shas against code_at_start.sha256 and the current l1b.py, on the rerank header and on the non-Qwen preds.
  - The Qwen preds are pinned by L1A_IMG_SHA.
  - Neither branch has a negative selftest (W19).
- W5 (synthetic score selftest): APPLIED.
  - It runs cmd_score end to end on 80 synthetic QA, and checks GO_STRONG, the tie rule M* = (0, 2), T* no gain, cross-fit rows, idefics3 not assessable, the second run refused, and no answer text in decide.json.
  - Gap: the test uses MODELS[:4] (3 Qwen + gemma). The likely real path, gemma absent with idefics3 in use, is untested (W19).
- W6: APPLIED in text (§4.4). It has the same provenance trap as W1 (W17).
- W7: APPLIED (§6 power note, flip-based SE).
- W8: APPLIED (§6, "or" recorded as a tightening under CC-168).
- W9: APPLIED (§2.2 wording "not used for any L1-b selection"; §4.5 the three biases).
- W10: APPLIED (§6 tier-2 note).
- W11: APPLIED (§3, Qwen three).
- W12: APPLIED (stage_problems l.304-310, C-image sha anywhere under NCS_DATA). It hashes every jpg/png under NCS_DATA on each guard call (W20).
- W13: APPLIED (§9, VCD and Vietnamese diacritic restoration in the sweep). The arXiv id is left "to verify" in the sweep, which is acceptable.
- W14: APPLIED (n_truncated_answers in decide.json; selftest passes).
- W15: APPLIED (§7 "M2 (machine id m4, the dev role)"; §9 item 7, no __pycache__).

## Rulings
1. W1-W5 are satisfied. Option 2 of round 1 (idefics3 only) is not required. The null + skip guard is equivalent to it whenever G3_gemma is empty, and it keeps the gemma path open at no risk, provided W16 is written into the rule.
2. Enabling gemma is a pre-output decision, so there are no forking paths. Whether gemma runs is fixed before any L1-b number exists. "First assessable in the fixed order" is pre-registered and does not depend on results.
3. The known risk stays disclosed: idefics3_8b is weaker in Vietnamese, so NO_VERDICT (contained EM < 20% or < 30 diac answers) is more likely without gemma. NO_VERDICT goes back to the judge. It is not a KILL and not a licence to explore further on E.
4. CC-165 r4 and CC-168 r6 are kept. No L1-b GPU step runs until G1 and G3 are closed. No overrule here.

## Required fixes
Blocking (in the finalisation diff, before the gatekeeper commit):
- W16. Write the gemma state into P2b and §3 as a pre-fixed rule: "G3_gemma and gemma3_4b's 4 hashes are filled before finalisation (the commit that pins the registry sha), or gemma3_4b stays skipped for this whole run; no fill after finalisation." Delete the §2.1 phrase "(it changes once more when gemma's 4 gated hashes are filled; P2b)", or replace it with this rule. Also fix the l1b.py l.48 comment "primary, fallback" to "fixed order, first assessable is used".

Mechanical (finalisation, checked by the gatekeeper as a pins-only diff):
- F1. Rename PREREG_DRAFT.md to PREREG.md; set PREREG_SHA256, L1B_REG_SHA256 and SPLIT_SHA256 in l1b.py; regenerate both SHA256SUMS; selftest 41/42; log the full shas. The diff must be exactly the 3 pin lines, the rename, the W16/W18/W19 text or code, and the SUMS. Anything more goes back to a judge.

Non-blocking (do at finalisation if cheap, else disclose):
- W17. W6's code-fix re-run changes l1b.py, so check_prov would reject every backbone that already finished. Pre-fix one of two rules now: (a) a W6 amendment re-runs all backbones inside the same 8 GPU-h cap; or (b) the amendment pins a list of accepted prior l1b.py shas that check_prov accepts. Recommended: (a). It is simpler and needs no code change now.
- W18. The gatekeeper fills G3 with "CC-168" (one id; the regex rejects "PI-1029l + PI-1029q"). G1 gets the sweep's LOG id.
- W19. Add a second synthetic score variant with no gemma files and idefics3 present. It checks nq = ["idefics3_8b"] and check_prov on idefics3 preds. Add two negative cases:
  - a missing sidecar plus CAP_STOP.json gives NOT_ASSESSABLE "incomplete";
  - a missing sidecar without CAP_STOP.json, or a header l1b_sha256 mismatch, makes score refuse.
- W20. The guard hashes every jpg/png under NCS_DATA on every call (about 6-8 calls per job). If M2 holds other image sets, this costs wall time (not GPU time, since t0 is taken after G). Prefilter by the C file sizes, or accept and note it.
- W21. The job's `gpu dec_$m` sits inside `if` under set -e. An unexpected rc 3 from decode exits without "JOB STOP" or finish. decode never exits 3 by design, so this is cosmetic.

## Ranked options (confidence that the option is the right action)
1. GO-with-fixes: W16 in the finalisation diff; gemma enabled only if the PI clicks before finalisation, else idefics3_8b in use; G1 binding. 92%. Chosen.
2. Same, but drop gemma3_4b from the registry entirely (idefics3 only, round 1 option 2). 88%. Cleaner bytes, but it forfeits the stronger Vietnamese non-Qwen model if the PI clicks soon. It raises NO_VERDICT risk without lowering any other risk relative to option 1 plus W16.
3. Option 1 without W16 (leave the late-fill promise). 70%. It can make the one-look path unscoreable.
4. Defer L1-b until G1 closes, with no finalisation now. 55%. It wastes ready work (PI "do work early"). Finalisation costs no GPU time and does not start the job.
5. NO-GO. 5%.

## For the PI
- Still open from CC-168: may the L1-b tier-1 dev run start before the OpenAlex/S2 sweep (G1) closes, as L1-a did under CC-165 r4? Recommended: YES. A dev result does not depend on novelty, and tier 2 and any test look stay behind G1. Default: G1 stays binding and the job waits.
- Gemma (FYI, your choice): if you want gemma3_4b as the non-Qwen backbone, the human click-accept of the Gemma Terms on the HF account that holds the ViTextVQA gate must happen BEFORE finalisation (W16). Recommended: skip it and run idefics3_8b, unless the click is already convenient. Default: idefics3_8b only.
