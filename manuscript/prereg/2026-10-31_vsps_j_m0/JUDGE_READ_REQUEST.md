# Judge read request: VSPS-J M0 PREREG (one judge, REVERSIBLE, bar >= 90)

Draft, not committed. This file is outside both SUMS because it lists them.
- **Licence:** CC-207 ruling 3 (GO to draft; W1-W5 must be closed before this read).
- **Scope:** a GO here licenses the M0 GPU block only, after the PI funds it (CC-207 Q5) and a slot is free under CC-207
  ruling 8 / W11. It licenses no test-set use.

## Files (sha256)

| file | sha256 |
|---|---|
| manuscript/prereg/2026-10-31_vsps_j_m0/PREREG.md | 53af5f6bc52977824655eba8a74cf2eff4d2b00d14f7f9f52b3ad38d645b33f4 |
| .../m0_plan.json | c422efd1d1efa71c6c728637cf86a6fb40ea725fc556b586bd3af9fcf6870af4 |
| .../dev_touched_ids.txt (3,454) | 91db7e2fbb3d479f79ed19fca4aa100399730910cd7511f832576350f26f9b63 |
| .../val_ids.txt (786) | b4d4f35ab7b951fbd4658b670ebf6aecf00cb910fa73753514c104b29ba0f412 |
| .../train_ids.txt (2,695) | 4a4033a518859b2c0aa8525a8db069e905148374419b9acc2864a0c70164be1a |
| .../karpathy_test_val_ids.txt (91) | 88e40e3cd2ae6dd3bf3c1f514a085cb61a36b503abde298d57a1bb2bc8acd7fb |
| .../selection_excluded_ids.txt (106) | 57195c49c601fe850ce7e06d2d58291076163c8c382399aca3e0eae516bfaef7 |
| .../dropped_ids.txt (73 = 17 val + 56 train) | 41306bdbcc672c8104ec4366b137f5f9cce9ecea28f2f59e8c5fd09dc10168bf |
| .../fetch_images.txt (821) | 7f148c8e515bf567f811da84a1e327a6e05d20a85e2939f5088fa1a45a359a3c |
| .../SHA256SUMS (9 lines) | 1b1c9a7e346e5e6eb00cac95ef059d3b3d4a25303502753903efeb79fb2b1324 |
| scripts/vsps_j_m0/m0.py | 9f81f899a658ee2e42a0fba73876a610ba28c5953487aaa531b53f9149577181 |
| scripts/vsps_j_m0/m0_stats.py | 600428061f2ff1743e017fc521ea2394b532ca52882591d239d2dcad84cadb89 |
| scripts/vsps_j_m0/test_m0.py | 1e40ac16922f0085404b31c3be5864e4ee42b99ec4e42ec8110a79e8d9aefc16 |
| scripts/vsps_j_m0/m0_job.sh | be5c6fce1fc8217acbb4c261e7a83204f7fa24b25de3fdd551288c8a291414e6 |
| scripts/vsps_j_m0/SHA256SUMS (4 lines) | d7704e871d598e1c8bced70916060a9bc20ea0861ac900c10435b3d42686ecb9 |

Unchanged inputs it reads:
- `rescap/vlm/registry.py` 6c261406;
- `rescap/vlm/vintern.py` dbde92aa;
- `scripts/gate_t05.py` a2c9702a;
- `data/results/gate_t05.json` 0dc5ce40;
- `scripts/grl/id_counts.py` 0c590058;
- A-N3 `val_raw.json` 2cbc7942 and `train_raw.json` 03b088d1;
- `data/an3/mhaldetect_overlap.json` fd97a3b0;
- `exclusion.json` c52a96d1;
- `ut2532.txt` 288340b8.

## Please rule on

1. **UIT-ViIC train pool overlap (PREREG section 3).** PORTFOLIO l.185 names the pool as a COCO ledger owner (L1-P3,
   ownership pending a ruling). 17 val and 56 train M-HalDetect images are in UT-2,532. M0 is the later-registered set.
   - **Recommended default:** drop them before any decode. The full split becomes 769 images and 16,027 segments, and
     the 786 / 16,449 release counts are reported beside it.
   - **Alternative:** keep them, so the full split is 786 images. Choose this if the pool's ownership does not bind dev
     probing by a frozen 1B model.
2. **W25 near-duplicate filter (l.185, "before any decode").** M0's custody is exact-id plus exclusion.json image-sha.
   W25's SSCD memory lives on M1/M3.
   - **Recommended default:** proceed without W25 for M0. It trains nothing and tunes one threshold on dev, and all
     3,454 ids are ledgered.
   - **Alternative:** add a W25 pass on the rental before the smoke. This needs the pinned COCO memory staged there, and
     an amendment.
3. **W1-W5 closure** against the fix map (PREREG section 12), including:
   - the construct name and the "no v1 three-way verdict" reading;
   - English span in the VI template, no MT.
4. **exclusion.json handling (section 3).** The 91 Karpathy-test images are probed per CC-207 W4. The other 15
   exclusion-listed val images outside Karpathy test (CHAIR-500 10, POPE-500 6, 1 image in both) get the same treatment: probed
   for the full split, held out of every choice, and kept out of the demo and smoke pools.
   - The dev-pool rule refuses these images.
   - **Recommended:** accept as written. **Alternative:** drop the 15 before decode.
5. **2-shot path (W2), section 4:**
   - interleaved via the pinned `chat(history, num_patches_list)`;
   - demos at one 448 tile, while the query keeps the registry 4-tile setting;
   - equivalence with `yes_no_logit` at |dP| <= 1e-3 as the arm-A smoke gate (CPU measured 0.0);
   - `max_new_tokens` 1;
   - the inherited bare first tokens "C" and "Kh" in `_yes_no_ids` (disclosed).
6. **Cost (section 8).** A + B = 2.3-8.1 h depending on the B/A ratio (CPU ratio 2.3-3.4 is a compute-bound upper
   bound), so a fit under the 5 GPU-h cap is not guaranteed.
   - Are the pre-val projection (smoke speed x full val, stop before any val decode) and the CC-206-style 50-image rule
     adequate?
   - **Alternative:** require per-image batching now, before any rental.
7. **Statistics (section 6):**
   - tau_B re-selected inside every bootstrap replicate;
   - KEEP iff point dR >= +3.0 **and** the CI lower bound > 0;
   - AUROC stop on the point estimates in both arms.
8. **Environment (section 1).** All of these are asserted by the job:
   - transformers 4.51.3 (5.22.1 cannot load the pinned remote code);
   - torch 2.15.0 and torchvision 0.29.2 (any build suffix);
   - numpy 2.5.4, pillow 13.0.0, timm 1.0.30, einops 0.8.2.

   The model loads by repo id with `refs/main` = the pinned revision and `HF_HUB_OFFLINE=1`.
9. **Ledger (W4): prepared, not appended.** The drafting agent creates only its own files. Please confirm these lines for
   the gatekeeper:
   - **PORTFOLIO** (`manuscript/directions/PORTFOLIO_3Y_2026-10-29.md`, image-level rule l.185): "VSPS-J M0 dev-touched:
     every M-HalDetect image, 786 val + 2,695 train = 3,454 COCO ids (27 in both; 73 never decoded),
     `manuscript/prereg/2026-10-31_vsps_j_m0/dev_touched_ids.txt` sha 91db7e2f. B4 drops them from restval (599 val +
     2,027 train in restval)."
   - **Tier-2 (spent, dev-confirm) ledger:** "VSPS-J M0 probes 91 Karpathy-test images (M-HalDetect val ∩ Karpathy test)
     at dev only; held out of every operating-point choice; `karpathy_test_val_ids.txt` sha 88e40e3c."
10. **Not edited by this draft (owned by other files):** program l.179 (~3,200), l.192 / l.402 (re-fetch) and l.214
    ("never run"). The PREREG states the corrected facts. Should the program owner fix those lines before the commit?

## Re-runnable checks (laptop)

```
cd /mnt/d/vsps_image_captioning
(cd scripts/vsps_j_m0 && sha256sum -c SHA256SUMS)
(cd manuscript/prereg/2026-10-31_vsps_j_m0 && sha256sum -c SHA256SUMS)
~/.venvs/vsps_j_m0/bin/python -I scripts/vsps_j_m0/test_m0.py          # "selftest ok" (CPU, no weights, no data)
PY=~/.venvs/vsps_j_m0/bin/python bash scripts/vsps_j_m0/m0_job.sh --selftest   # SUMS + env pins + selftest
python3 -I scripts/vsps_j_m0/m0.py plan     # rewrites the plan and id lists; the folder SUMS must still pass
python3 /tmp/claude-1000/-mnt-d-vsps-image-captioning/5a363495-c9d6-40f3-8f9c-a7285ef7a0e6/scratchpad/ngram_scan_cen.py <each new file>
```

- `plan` checks each of these, or FAULTs:
  - the A-N3 pins;
  - the A-T3 r9 list (file and ids sha);
  - the KV-4,224 rebuild against its ids pin 86d93863;
  - the exclusion.json and ut2532 pins;
  - the Karpathy split recount against A-N3's overlap file.
- It prints the counts in PREREG sections 2-3.
- **CPU smoke (section 7.3), optional, about 5 min:** it needs the pinned weights in the HF cache with `refs/main` = the
  revision, and the 4 COCO images (2 demos, 2 smoke):
  ```
  HF_HUB_OFFLINE=1 ~/.venvs/vsps_j_m0/bin/python -I scripts/vsps_j_m0/m0.py probe \
      --data .session_backup/2026-10-19/HL_human_labels/dl_mhaldetect --images <4 COCO images> \
      --model <snapshot dir> --out <new dir outside the repo> --device cpu --smoke-n 2 --smoke-only
  ```
  It reads only train images.

## Default if no ruling

No rental and no decode. The draft stays uncommitted.
