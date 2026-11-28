# C-CONF block T (the registered second look at the OpenViIC test set): outcome and run records

Registration: `../REG2_TEXT.md` (sha256 f873188d…, commit 19cf8ef1). Rulings on the outcome: CC-522 (permitted reads), CC-522b (cause, disposition, wording, close-out), CC-522c (one removal-scan count). This note states facts of record only; its outcome paragraph is the done line of the decision log (OPS-1128bt-cconf-done), whose wording was fixed by ruling CC-522b 6 (a).

## Outcome

The look began on 2026-11-28 (look-begins line OPS-1128bp-cconf-T0-begin, 03:54:40 UTC; files staged 03:55:39-03:56:10 UTC) on the investigator's own computer (one RTX 3090, 24 GB) and stopped at its first step, before any caption was decoded. **Every row of the study on the OpenViIC test set is NOT RUN. There is no test decision file, no caption, no score and no list file of the test set, and there will be none: the registration permits no re-run, no partial run and no further registration of this look (§6.5, §10.1 G4, §10.5).**

Done line, verbatim:

> C-CONF block T DONE LINE in LOOK STOP form (run document v4P.3 §8 and §11 item 14; ruling CC-522b): call 3 ended with LOOK STOP at T0 at 2026-11-28T03:57:21Z, registered gate G4 (K0-T): the rebuilt retrieved lists were equal to the first look's for 2,000 of 2,001 images and the random draw-0 lists for 2,001 of 2,001 (registered bar: 2,001 of 2,001 for each); G0b not evaluated (G4 raised first); stagecheck 2,004 files, 0 unexpected, 0 missing, 0 differ; printed counts: n 2,001, distinct sha256 1,997, confirm-half primary 0, share with a KTVIC copy in _pairs 0.3178 (636 of 2,001), twin replacements 0 and 0. Steps OK: T.0 (D1 of the four runners on OV-dev-B), the cap line, the time checks, the scoring parity gate, k0dev, the dry run, stagecheck. Steps NOT RUN: the T0 list file (not written), T.1, T.4, T.2, T.3 (every arm of Qwen2.5-VL-7B, LMCap, InternVL3-8B and Aya-Vision-8B on ov_test), and the scoring call of section 9. OV-test outputs: 0 captions, 0 scores, 0 list files. gpu_h 0.16 of cap 22.98, all before T0 on development items, 0 on OV-test. Sha check 3 of 3 of model.safetensors (CC-468 C8): equal (9e2926577049a20960ead82d1ebe5ce04d498f450ca53e5c1fb0993c4fc7d8de at 2026-11-28T04:24:47Z; record G35_sha3.txt da525f943059e6e7) (no LMCap decode exists, so nothing is held). c_conf_t/SHA256SUMS af35ed0a0ffcac9d95d99669812ba45e5d46802286602b6121650a77477dfe9f, written by finish(); 44 of 45 lines verify, and logs/job.log was appended after. CAP.json 1df8ae78 (= the cap line OPS-1128bo); LOOK_STOP.json b6efd43f; t0.log 06a94555; t0 report 9a6c4690 (709 B; holds ids; never opened). Foreign GPU processes after T0: none (PS_stop, PS_stop2). Reads of the job folder after the stop: R1-R4 of CC-522 only (OPS-1128bs-cconf-reads). The look is spent (registration §6.5, §10.1 G4); there is no re-run and no further registration (§10.5).

Why the one retrieved list differs from the first look's list was not established. A last-bit difference in the floating-point cosine product between the two machines, reordering two near-equal neighbours for one image, is the most likely mechanism; this is an inference and was not checked (CC-522b ruling 4 (b)). The image is not named anywhere in this repository.

## Files in this folder (ids, counts and status lines only; registration binding 8)

| file | sha256 | what it is |
|---|---|---|
| `C_CONF_TEST_TOKEN.json` | a417edb5a7912c017f6efb0c7bb2aa9257ca97fa0239553ffdbd0f2a85bbeef3 | the token of the look (four fields) |
| `C_CONF_REHEARSAL_DECISION.json` | 56ce48ca675159687e608db803e4d6c5f790b6714f377c55a8f93bb8423b19e0 | the rehearsal decision file on development data (2,000 OpenViIC training images used as queries, own cluster removed); the token names its sha256 |
| `CAP.json` | 1df8ae78d7699758f333613e8f94d4d74b406fd74ff3018df5960e93688eb4b8 | the cap plan of call 1 (D1 rates on development items, P, cap, runners) |
| `T0_READY.json` | 52443f3ed440bfe9d3348168eb90d085c004bb82923b9d9554b107eb147cd556 | the ready record of call 2 |
| `LOOK_STOP.json` | b6efd43f1230319967b5aa06b28fedf7a70913d7a34a10ae231e92c3fe234209 | the job's stop record (catch-all label of the T0 step, time stamp) |
| `job.log` | d205967b0bd38f38f3b673c9d4b0612a664d42282137dcbfbd63f5b0be4d5fa1 | the job's status lines of calls 1 to 3 |
| `t0.log` | 06a94555fa646442e862f810f87cd15856f139eddc5126793a88a45bf287e98b | the three lines of the T0 step: the stage check, the counts line, the gate line |
| `gpu_seconds.tsv` | 4edff2226ed87be03fc31e60157089e43abce59439b37ca68acc9880bfeeea44 | seconds per step (all on development items) |
| `code_at_start.sha256` | 3e0c719a015191c3f0a1b1486aa54e2a82a542cd65f1afbe60bfed733b383e8c | sha256 of the five code files at the start of the last call |
| `OUTPUTS_SHA256SUMS.txt` | af35ed0a0ffcac9d95d99669812ba45e5d46802286602b6121650a77477dfe9f | the SHA256SUMS file the job wrote in its outputs folder (44 of its 45 lines verify; job.log was appended after it was written) |
| `rc/t1.rc` | 9a271f2a916b0b6ee6cecb2426f0b3206ef074578be55d9bc94f6f3fe3ab86aa | exit code of call 1 |
| `rc/t1.console` | 68816a7124648138ec356f53b2875d9ae86f530b764bdd9d69667ae206189764 | console of call 1 |
| `rc/t2.rc` | 9a271f2a916b0b6ee6cecb2426f0b3206ef074578be55d9bc94f6f3fe3ab86aa | exit code of call 2 |
| `rc/t2.console` | 6518080cc57d55316e533840fdbc94583a622f9329131364936433b049ee682e | console of call 2 |
| `rc/t3.rc` | 4355a46b19d348dc2f57c046f8ef63d4538ebb936000f3c9ee954a27460dd865 | exit code of call 3 |
| `rc/t3.console` | 799e1a04f3a87d6d5159aac5d4409096fb4a2703f514233f4ea4de935bdf1f48 | console of call 3 (six status lines) |

## Not in this repository

The predictions of the development-data parity step, the T0 report file of the job (it holds image ids; sealed, never opened), and every other output stay outside the repository under the custody rules of the registration (§10.3, §10.6 (d)) and of ruling CC-522b 7 (b). The staged test files were removed from the test computer and from the laptop; the removal scans and the restores are recorded in the decision log (OPS-1128bx-cconf-removal, OPS-1128by-cconf-session-end). After the stop, four scripted reads of the job folder printed counts, fixed words and hashes only (OPS-1128bs-cconf-reads); no file of the job folder was opened by hand.
