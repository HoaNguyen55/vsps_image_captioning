# B-PA1-T1: tier-1 DEV-EXPLORE prereg for Paper B (object-grounded factuality metric for Vietnamese captions)

Status: **DRAFT v3 for the final round 3, not registered, not committed.** v3 answers CC-217r2 (panel round 2/3,
NEXT_ROUND, median 86, bar 92); v2 answered CC-217 (round 1). v1 (`PREREG_DRAFT.md`, sha256 `8545859b`) and v2
(`PREREG_DRAFT_v2.md`, sha256 `009fa1c5`) are kept unchanged. Drafting is licensed by CC-213r3 (GO 93) only;
registration = a gatekeeper commit after the round that grants GO (CC-213r3 W17).
**Scope of a GO on this file (CC-217r2 Ruling 4, B3):** the gatekeeper commit and laptop-CPU T1a only. No 4090 step,
block W included, runs before the R5 launch amendment with its one-judge read, a logged PI top-up and the N18 novelty
rescan. Nothing here has run. Direction:
`manuscript/directions/B_DIRECTION_v3_2026-11-01.md` (sha256 `ef1e3cc5`). HEAD at drafting: `219704f`.
Label on every output: `TIER 1 / DEV-EXPLORE (B-PA1-T1)`. Every estimate below is AI opinion, not evidence.
Code (written after GO, CPU selftest before any GPU step): `scripts/b_pa1/b_pa1.py`, `scripts/b_pa1/b_pa1_job.sh`;
registry `b_pa1_registry.json` (model pins); lists `b_pa1_lists.json` (ids only).

## CC-217r2 closure table (round 2 → v3)

| item | what CC-217r2 asked | where closed in v3 |
|---|---|---|
| B1 (custody) | the ruling's §5.4 l.253-256 text verbatim: block W on the 4090 covers only the slice-A frame, Composite-COCO and Polaris-test-COCO; every other owner's features from sha-pinned caches, recomputed only on the custody host (M1, or the laptop CPU where allowed; never the laptop for A-T3 val2017), never on a rental; named never-on-rental sets; l.234 made to agree (verbatim) | §5.3 (l.234 text), §5.4 Compute |
| B2 (numbers) | the ruling's §9.1 l.451-453 text verbatim: after S 16.0 h × 1.25 = 20.0 > 18.1; drops E2, A4, H, A3; expected ≈ 11.5 GPU-h + 4 h setup ≈ 271,000 VND, ≤ 420,000 VND at the cap; A3 expected NOT RUN, (d1,v1) frozen | §9.1 |
| B3 (scope) | a GO licenses only the commit and laptop-CPU T1a; no 4090 step before R5 + one-judge read + logged top-up + N18 | header, §0, §9.1 |
| W1 | A1 split into A1-decode (step 3) and A1-score with A2, A3, H after step 5; smoke outputs kept as rates only; parity run 1 prints only micro Δ, macro row, drop counts | §6.3, §6.4, §9.1 |
| W2 | R7 segmenter and stop-list pins with map v1; crosswalk frozen with map v1; instrument LLM id, revision, prompt sha; same segmenter for H2 | §6.1, §6.4 step 1, §8.4, registration items |
| W3 | a set is never its own owner | §5.4 |
| W4 | each R-item pinned by a sha-bearing gatekeeper LOG line before first use | registration items |
| W5 | run order W, S, A1, A2, E1, then A3, H, A4, E2; E1 at (d1,v1), no re-run; CAP STOP final; one resume only for machine loss or a guard failure; displayed total excludes E2 | §9.1 |
| W6, W7 | English E1 prompts pinned by sha before any E1 output, never re-selected; all prompt texts pinned by sha before block S | §7.4 |
| W8 | owners the group does not yet hold = deferred W25 owners | §5.4 |
| W9 | M1 PA2 row incl. the untransformed score: ≈ 2.6 h; M1 total ≈ 5.8 h, cap 9 h | §5.3, §9.1 |
| W10 | tier-1 effect trigger labelled optimistic | §11 |
| W11 | categories[] through a pinned extractor; annotations[] only at step 6 | §6.1, §6.4 |
| W12 | "never mentioned in the paper" → "count only, no reason text" | §5.4 |
| W13 | cap fixed before registration (PI Q-a; default 20 h) | §9.1, §15 |
| W14 | STATE refreshed for PI-1101r/s/t (and PI-1101u noted) | `.claude/agents/STATE_2026-11-01.md` |
| W15 | round 3 = full three-judge panel on v3, scoped to the diff plus this table | for the coordinator; no file text |

CC-217 round-1 items B1-B4 and C1 were ruled CLOSED in v2 (CC-217r2 Ruling 1); their table is kept below for reference.

## CC-217 closure table (round 1 → v2)

| item | what CC-217 asked | where closed in v2 |
|---|---|---|
| B1(a) | parity gate once on sha-frozen map v1, laptop CPU, before any amendment; > 2.0 fires PA3 irrevocably; re-run on the final sha, same stop | §6.3, §6.4 steps 2 and 5 |
| B1(b) | amendments only from coverage statistics (caption text, class names), never from B/judge/gold outputs; UTC log | §6.1, §6.4 step 4 |
| B1(c) | all amendments closed and map sha frozen before `T1_THRESHOLDS.json` and before any τ of B; thresholds record the map sha; never recomputed downward | §6.4 steps 4-8, §8.5 |
| B1(d) | exact parity statistic (micro vs macro); captions with no mapped mention dropped and counted | §6.3 |
| B2(a) | lever design, comparison caption set, tie order | §7.2 (one factor at a time, 3 configurations) |
| B2(b) | A3 ≈ 5.8 h (one factor at a time), total, +25%, trim sentence | §9.1 |
| B2(c) | A3 trimmed → (d1,v1) frozen, A3 NOT RUN | §7.2, §9.1 |
| B2(d) | "tier-1" → "tier-3" captioners | §7.1 |
| B3(a)-(e) | M1 block cap 9 GPU-h with per-step timeout; only after MT4 releases M1; VN gate never depends on M1; NOT RUN if M1 lapses, no PA3; T1a today = laptop CPU only | §0, §4.4, §5.3, §9.1 |
| B4(a)-(d) | §12 is an audit record; the paper says only "absolute τ is not claimed to transfer"; no exposure or overlap wording in paper, supplement or cover letter; map entries = method component | §2, §12 |
| C1 (Codex) | one size rule for every role; active rows match the default S; "N for the verifier only" struck | §4.1, §4.2, §15 O1 |

Non-blocking items N1-N20: one-line dispositions in §14.

## 0. What tier 1 is for, and what can start today

Tier 1 fixes, on dev data only, everything that tier 2 (rehearsal on Objects365 train slice B) must copy verbatim and
tier 3 (one look at Objects365 v2 val) must reuse: the four captioners, the decomposer, the verifier, the same-backbone
judge, prompts, the VN→Objects365 class map, SESOI and the NI margin, K, the abstain rule, and the measured rates for the
P3 projection (§9). Tier 1 makes **no confirmatory claim** and never reads a sealed set (§3).

- **T1a today = laptop CPU only (B3e):** desk check (§4, done), owners build `b_pa1_owners.json` (§5.4), W25 features
  of the custody sets where their images are on the laptop (§5.3), the v3 P10 novelty rescan (N18). No GPU, no M1, no
  Objects365.
- **Laptop CPU, after the PI's download (no local Objects365 class list exists in the repo):** class map v1 build and
  freeze (§6.1) and parity gate run 1 (§6.3), both from the `categories[]` of the train annotation file only.
- **Needs the 4090 (dedicated per PI-1101r) and, before its first step, the R5 amendment with its one-judge read, a
  logged PI top-up and the N18 rescan (CC-217r2 Ruling 4):** block W, every slice-A block, the Vietnamese gate (§4.4)
  and the English dev block E1 (Composite-COCO). E1's GPU outputs may be produced early, but no τ of B on E1 is opened
  before `T1_THRESHOLDS.json` exists, and that file needs slice A (§6.4).
- **Needs M1 after MT4 releases it (§5.3):** the custody rows on UIT-ViIC 231 and KTVIC 558 only; all descriptive.
  They also wait for the §4.3 walk to accept 4 captioners, which happens in block S on the 4090.
- **T1b (Objects365 train slice A)** starts only after the PI has registered and downloaded the Objects365 v2 train
  annotation file and the train patches `patch0` and `patch1` (agents never use the PI e-mail; N19), after W25 (§5.4)
  and after the R5 launch amendment (N15).

## 1. Hypotheses and crosswalk to the direction file

Labels kept as in v1 (CC-217 ruling 12, O5 at 93).

| this draft | content | family | v3 §3.4 label |
|---|---|---|---|
| H1a | non-inferiority: Δτ_c(B − same-backbone judge) on mapped object propositions, lower bound > −NI | F1, fixed-sequence gate | H1 |
| H1b | superiority: Δτ_c(B − same-backbone judge) lower bound > SESOI | F1, Holm with H1c, after H1a | H2 |
| H1c | superiority: Δτ_c(B − multilingual CLIPScore) lower bound > SESOI | F1, Holm with H1b, after H1a | H3 |
| H2 | PA2 deterministic suite: invariance rate of B's score under 6 meaning-preserving transforms | F3 (registered secondary, dev only, §8.4) | v3 §3.6 |
| H3 | English arm: τ_c of B's score vs COCO-instance object precision and vs human ratings (Composite-COCO, Polaris) | F2 (dev descriptive at tier 1; one-look only if v3 §5.4 passes) | v3 F2 |

- **Primary endpoint (W8):** caption-level Kendall τ_c between B's score and gold object precision, computed only on
  **mapped object propositions** (head noun maps to an Objects365 class through the frozen map, §6). The full
  open-vocabulary score is descriptive (and enters the N1 sensitivity, §8.7). Limitation sentence for the value line
  (v3 l.25-27): validity is shown on the mapped domain only; use beyond it is argued, not validated.
- **Claim wording:** Δτ is not attributed to decomposition alone; the contrast with the same-backbone judge changes both
  the decomposition and the question format (N1).
- Count propositions are **not** in the primary score; descriptive under v3 §3.3 (no `iscrowd` box for the class,
  instance count ≤ K, K = 10).
- Colour, attribute, action and relation propositions: descriptive dev output, labelled "unvalidated".
- Claim wording (N4 of CC-213r2): "caption-level validity; system-level descriptive"; τ over the 4 tier-3 captioners
  is reported without a verdict.

## 2. Ownership, boundaries and paper wording

- B never reports proposition-level recall, retention or AUROC of the verifier against gold (VSPS-J's ground, v3
  §2.1b); B uses no VSPS/VSPS-J weights, prompts, S_hi values or per-type thresholds; B's verifier is not
  Vintern-1B-v3_5 (v3 §2.1c). Public base weights of an open model are not VSPS weights (O2, CC-217 ruling 12).
- SUPPORTED/UNCERTAIN/REJECTED is FAIR/VSPS code and is not used. B's verifier answers yes/no; only a descriptive
  abstain rate is reported, credited to FAIR 2026 (Hòa et al.) (v3 §2.2).
- B cites Paper A for the gold-completeness, mention-counting and count-matched findings and does not re-claim them
  (v3 §2.3). A's R12 H1 use of Composite and Polaris is cited; A's H1 is not re-claimed (N9). COCO-80 = sensitivity.
- **Placement (W14):** the registered B-alpha INCONCLUSIVE row (commit `c71b7af`) and the B-1 dev rows stay in B's
  supplement and are never hidden.
- **Paper, supplement and cover letter (PI-1101e, PI-1101o LOG l.1082, PI-1101p Q2/Q3 LOG l.1083; B4):**
  - no mention of AI assistance;
  - no wording on image overlap, near-duplicates, the W25 filter, pretraining exposure or captioner exposure, and the
    phrase "no overlap" is never written; exclusions are reported as a count only, with no reason;
  - on transfer, the only permitted sentence is that absolute τ is not claimed to transfer from train to val, with no
    reason given;
  - open models used as method components may be named (v3 §2.1h). The map entries proposed by an open LLM are
    described only as a method component, next to the dictionary-only sensitivity (§6.2), never as writing or
    research assistance. If the PI reads PI-1101e more strictly (CC-217 Q5), the map is described as a dictionary plus a
    documented instrument, without naming its source.
- Everything in §4.2's exposure column and in §12 is an audit record for prereg and decision files only.

## 3. Sealed sets: zero reads in tier 1 and tier 2

| set | status for B | allowed in tier 1/2 |
|---|---|---|
| Objects365 v2 **val** | B's one-look set (PI-1101p Q4) | nothing. The PI downloads no val file in tier 1 (N19); any val file that arrives anyway stays sealed, sha256 only, no B read. The images[] count is the tier-3 P2 step (laptop, images[] only, W13) |
| Flickr8K-Expert (all) | sealed for B until Q1 + primary licence check + image-level W25 + B8 (v3 §5.1) | nothing; no Flickr8k_text download anywhere, tmpfs included; `ExpertAnnotations.txt` never opened (W1) |
| FOIL **test** | sealed, same four conditions | nothing; no FOIL JSON read (W2) |

- **Parents for the later sealed-set W25 (W1, W2; CC-213r3 P3):** Flickr8K parent = the full Flickr8K image list taken
  from the image archive, never the text zip; FOIL test parent = all COCO val2014 ids, with no FOIL JSON read. The JSON
  route needs a pinned `images[]`-only extraction and a fresh judge line.
- **Subset check (N13, reworded):** whether every Expert image is in the parent needs the Expert image-name list,
  which is sealed, so it is not checked in tier 1 or 2. At unsealing, the first step reads only the image-name column
  under a pinned extraction; any Expert image outside the parent extends the W25 parent to the union before anything
  else runs.
- **Touch = lost:** any B contact with a sealed set outside the W25 route makes it permanently dev-only; the English
  one-look is then dropped or moved (v3 §5.1 item 3), logged in LOG.
- **B's dev contacts:** every image id B decodes or scores in tier 1/2 goes to `b_pa1_dev_contacts.json` (ids only, sha
  recorded). It is an owner list for every later W25 pass (N11). The later sealed-set W25 excludes overlaps **from the
  sealed sets** by the v3 §5.2 rule; heavy attrition of FOIL test against the val2014 parent is expected and the v3 §5.4
  drop/move branch applies (W2).

## 4. Day-1 desk check and family freeze (W11, W13; v3 §2.1f, §3.5)

### 4.1 Frozen family and size rules

A model's family is the pair (V, L):
- **V (vision lineage)** = the series of the vision encoder whose weights the tower was initialised from, followed back
  through every weight copy. Versions of one series are **one lineage**: SigLIP ≡ SigLIP2; InternViT-6B ≡
  InternViT-300M; BLIP-2's ViT-g follows its EVA-CLIP initialisation. Distillation teachers outside the series are
  recorded but do not merge lineages.
- **L (LLM lineage)** = the base-model series of the language model; fine-tunes and continued pre-training inherit the
  base: Qwen ≡ Qwen1.5 ≡ Qwen2 ≡ Qwen2.5 ≡ Qwen3; Gemma ≡ Gemma2 ≡ Gemma3 ≡ Gemma 3n; Llama 2 ≡ Llama 3.x ≡ Vicuna;
  mT0 ≡ mT5; InternLM2 ≡ InternLM2.5; Phi-3 ≡ Phi-3.5 ≡ Phi-4; BLOOM ≡ BLOOMZ.
- **Lineage resolver (N6):** the model card first, then the model's technical report or paper. `config.json` confirms
  the architecture only, never the weight initialisation. A lineage that neither source determines counts as a
  **clash** with every other model, and the next candidate is taken.
- Two models are **disjoint** iff their V differ **and** their L differ. The verifier is disjoint from every tier-3
  captioner; the 4 tier-3 captioners are pairwise disjoint; the same-backbone judge is the verifier model itself; the
  text-only decomposer is disjoint in L from every tier-3 captioner.
- **Size rule, one rule for every role (C1):** Rule **S** (default; CC-217 ruling 6, PI Q2): safetensors total
  parameters on the pinned revision ≤ 8.0 × 10⁹. Rule N (nominal label ≤ 8B, totals disclosed) applies to **every**
  role only if the PI picks it before any model output; the mixed option of v1 is struck.

### 4.2 Desk-check table (v1 calls: 10 of 10; v2 made no web call)

"card" = fetched 2026-11-01; "registry" = an existing repo pin marked "verify at pin"; "unverified" = not established
by any source fetched. The last column is an **audit record**, never paper wording (§2).

| model | role under Rule S (active) | family (V / L) | total params | Vietnamese on card | exposure note (audit only) |
|---|---|---|---|---|---|
| Qwen2.5-VL-3B-Instruct | **verifier + judge** | Qwen-ViT / Qwen | about 3.75 B (unverified) | not named on the 7B card; strong VN in repo use of the 7B | box localisation advertised (7B card); detection data plausible |
| Qwen2.5-7B-Instruct | **decomposer** (text) | — / Qwen | about 7.6 B (unverified; if > 8.0 × 10⁹, Qwen2.5-3B-Instruct) | unverified | n/a |
| InternVL2_5-8B | captioner candidate 1 | InternViT / InternLM (card base_model) | about 8.1 B (unverified; Rule S may fail → InternVL2_5-2B) | card tag "multilingual" only | card silent |
| mBLIP mT0-XL | candidate 3 | BLIP-2 ViT-g (EVA-CLIP init, unverified today) / mT5 | about 4.9 B (unverified) | **vi listed** (96 languages); card warns best results in high-resource languages | card silent |
| Gemma-3n-E4B-it, rev `c1221e9c` | candidate 5 | MobileNet-V5-300M (J2 desk check in CC-217; confirm by the resolver at pin) / Gemma | 7,849,978,192 (HF API) | Google card: "over 140 spoken languages"; vi not named | card silent |
| MiniCPM-V-4 | candidate 6 | SigLIP2 / MiniCPM (card) | 4.1 B (card) | card tag "multilingual" only | trains on RLAIF-V data (card) |
| Qwen2.5-VL-7B-Instruct, rev `cc594898` | Rule-N alternative verifier + judge (all roles N only) | Qwen-ViT / Qwen | 8.29 B, fails S | as above | as above |
| Aya-Vision-8B, rev `d7601ac8` | dev-only (O3), and only under Rule N | SigLIP2 / Command | 8.63 B, fails S | vi listed (C-T1 registry) | card unreadable today (401) |

- Rule-S assignment on paper: verifier Qwen-ViT/Qwen; captioners InternViT/InternLM, EVA/mT5, MobileNet-V5/Gemma,
  SigLIP/MiniCPM. Pairwise disjoint if the resolver confirms the starred lineages at pin. **Desk-check verdict: PA3 does
  not fire at the desk.** Vietnamese is claimed on a card only for mBLIP; the binding check is the §4.4 gate.
- The ViT initialisation of Qwen2.5-VL is recorded from its technical report at pin (N6). If it resolves to a
  CLIP-family line, the CLIP-line candidates of §4.3 are checked against it like any other pair.
- **Pins (registration item R1):** revision and file sha256 from the HF tree API; gated models only after the gate is
  accepted on the operator's account; safetensors total recorded; lineage resolved with the source cited in
  `b_pa1_registry.json`.

### 4.3 Candidate order and acceptance walk (fixed now, before any gate result; N7)

Ordered list (in-slot substitutes follow their primary): 1 InternVL2_5-8B → 2 InternVL2_5-2B (InternViT /
InternLM, card table) → 3 mBLIP mT0-XL → 4 mBLIP BLOOMZ-7B (EVA / BLOOM; size checked under S) → 5 Gemma-3n-E4B-it →
6 MiniCPM-V-4 → 7 Gemma-3-4B-it (SigLIP / Gemma) → 8 Phi-3.5-vision-instruct (CLIP ViT-L / Phi; unverified) →
9 Molmo-7B-O-0924 (CLIP / OLMo; unverified) → 10 llava-1.5-7b-hf (CLIP / Llama).

Walk: take candidates in order; skip a candidate that fails its pin, Rule S, the lineage resolver, or disjointness from
the verifier or from any already accepted captioner; otherwise run the §4.4 gate and accept it iff it passes; stop at 4
accepted. Candidates 8-10 share the CLIP line, so at most one of them can be accepted. **Fewer than 4 accepted after
candidate 10 → PA3 (§11).** No candidate is added to this list after any gate result.

**Dev-only descriptive captioners (block A4, never tier 3; Rule S):** Qwen2.5-VL-3B-Instruct (the verifier's own
family; rows reported separately), then the first two of [Gemma-3-4B-it, InternVL3-2B] not accepted in the walk.

**Pinned caption set for every tier-1 decision:** judge-prompt selection, lever selection, SE_A (§8.5), the planning
numbers and the PA3 effect trigger (§11) use **only the captions of the 4 accepted tier-3 captioners** (block A1).
Block A4 captions never enter any of them.

### 4.4 Vietnamese gate (mechanical; C-T1 §6.2 rule reused)

- **Gate set: the first 231 images of slice A in slice order**, on the 4090, always. The gate never depends on M1
  (B3c holds whether M1 is busy or gone), and one fixed gate set removes the choice between two gate sets.
- Statistic: share of the candidate's captions on the gate set containing at least one Vietnamese-only letter
  (ă â đ ê ô ơ ư) or a Vietnamese tone mark. Pass iff ≥ 0.95.
- Same prompt and decode settings as tier 3 (short mode, greedy, 60 new tokens, each model's own chat template; v3
  §3.7). Gate decodes are charged to block S.

## 5. Data

### 5.1 Dev sets of tier 1

| set | role | where | gold |
|---|---|---|---|
| Objects365 v2 train **slice A** (2,000 images) | main dev (T1b) | named rented RTX 4090 | Objects365 boxes via the frozen map |
| UIT-ViIC test 231 (spent by VSPS-J E1a, OPS-1101e1adone; `exclusion.json` `c52a96d1`) | dev only, never reported as a result; parity gate (human references, laptop); descriptive custody rows | laptop CPU (parity); M1 only for decodes (§5.3) | COCO instances (COCO-80) |
| KTVIC test 558 (spent: CP-071, B-F1 FAIL, `a21a14c`, LOG l.349; N9) | dev only; PA2 suite, coverage; descriptive | laptop CPU; M1 only for decodes | none for objects |
| Composite, COCO part only (about 1,996 val2014 images; 3 candidates + 1 COCO reference per HIT) | English dev, convergent validity (W5) | 4090 after W25 | crowd ratings (aggregates and citation only); COCO instances |
| Polaris **test** split, COCO val2014 part (spent by R12 H1 G2) | English dev, lowest-priority block | 4090 after W25 | human score; COCO instances |

- FOIL train is **dropped** from tier 1 (N8: no trigger or budget could be pinned for "if needed").
- Composite's Flickr8K and Flickr30K parts are removed **before** B reads Composite, by source label, else by Flickr
  file name/id, else by hash (v3 §5.2). Polaris nocaps part and other splits: not used.
- Caption counts of Composite-COCO and Polaris-test-COCO come from metadata (counts only) before the cap check.
- BLEU, CIDEr and BERTScore-PhoBERT only on dev sets with human references (UIT-ViIC 231, KTVIC 558, Composite-COCO,
  Polaris); never on Objects365 (W7). N17: BLEU and CIDEr of each tier-3 captioner on the UIT-ViIC 231 references are
  one descriptive row (M1 block; NOT RUN if M1 is never free), with no gate.
- **Single pass on the spent Vietnamese sets (N20):** each custody set is decoded **once** per captioner in the one M1
  block (§5.3). Every use (custody rows, parity second row, PA2 on KTVIC, BLEU/CIDEr, abstain and coverage rows) reads
  those same outputs. No re-decode, and no tier-1 decision reads them.

### 5.2 Objects365 train slices A and B

- **Sampling frame (O7, CC-217 ruling 12):** the images in `images[]` of the Objects365 v2 train annotation file that
  lie in train patches `patch0` and `patch1`, named now; if the release has no patches, all of train `images[]`. Train
  is not an evaluation split, so the full-split rule does not bind here.
- `b_pa1.py slices` **streams** the annotation JSON (ijson, version pinned in the venv freeze, R2) on the laptop and keeps
  only `images[]` (`id`, `file_name`); `annotations[]` is not loaded for slicing (N12). Order = ascending
  sha256(`b-pa1-o365-slice|` + file_name). W25 (§5.4) runs along that order in blocks of 500; **slice A = the first
  2,000 W25 survivors, slice B = the next 2,000** (n fixed, disjoint by construction). Ids go to `b_pa1_lists.json`.
  Slice B images are never decoded, scored or staged in tier 1.
- Box gold of slice A is joined **on the laptop only**, by the pinned scorer (same separation as tier 3; v3 §4.2
  item 5), and only at §6.4 step 6.

### 5.3 Custody and the M1 block (W12; CC-209 r1(a); B3)

- UIT-ViIC test 231 and KTVIC test 558 never leave M1 or the laptop. Their W25 features are computed there; only
  feature vectors and ids are compared with other owners' features, on the laptop.
- The rented 4090 holds no other images. Before any image is staged on any host, Composite-COCO and Polaris-test-COCO are id/file-name matched on the laptop (ids only) against every COCO-id-space owner in b_pa1_owners.json (KV-4,224, Karpathy test, A-T3 val2017, the 3,454 M0 ids, UIT-ViIC test and train pool, COCO restval, UT-2,402, and the rest). Id-matched images are excluded and never staged on a rental. Only the id survivors and the Objects365 slice frame go to the 4090, for C1-C3 features. No COCO archive is placed on the rental. No B decode or score runs before the full W25 exclusions are applied. (CC-217r3 B-new-1; B_DIRECTION_v3 l.48.)
- **M1 block (descriptive custody rows):** the 4 accepted captioners decode UIT-ViIC 231 and KTVIC 558 (3,156 captions ×
  (0.84 s + 2.79 s) ≈ 3.2 h on a 3090) and B's score runs on one KTVIC reference per image, untransformed and under the
  6 PA2 transforms (558 × 7 × 2.4 s ≈ 2.6 h): about **5.8 h** (W9).
  - **Hard cap 9 GPU-h** (CC-217 B3a), per-step `timeout` for the time left; a timeout is a final CAP STOP. Stop and
    resume as §9.1.
  - **Slot:** only after MT4 releases M1, never while an MT4 K1+K6 job is live or queued on M1, and it never delays
    MT4 tier 2 or tier 3 (CC-215 B8, CC-216, PI-1101q).
  - **If M1 lapses or is never free:** these rows are reported NOT RUN; no PA3 fires from that; nothing else in tier 1
    waits for them. A PI-named custody host is the only alternative (CC-213r3 P7; default: wait).
- The parity gate never needs M1 (§6.3).

### 5.4 W25 before any B read (E3, W6, W16, N8, N11)

- **When:** finished, and exclusions applied, before any B decode, decomposition, verification or scoring on slice A,
  slice B, Composite-COCO and Polaris-test-COCO (PORTFOLIO_3Y l.185). Never run on the sealed sets in tier 1 or 2.
- **Rule:** W25 RULE §3 (`manuscript/prereg/2026-10-28_w25_neardup/RULE.md` sha `289c0a59`, `scripts/w25/w25.py` sha
  `d6d12780`): C1 byte match, or C2 min(pHash, dHash) ≤ 10 incl. mirror AND SSCD ≥ 0.5, or C3 SSCD > 0.75; plus
  id/file-name match where id spaces are shared. Features and ids only.
- **Compute (N8):** block W on the named 4090, first after setup: SSCD + pHash/dHash for the slice frame along the
  slice order (blocks of 500 until 4,000 survivors), and the id survivors of Composite-COCO and Polaris-test-COCO; estimate 1.0 GPU-h inside
  the 20 h cap. Features of every other owner come only from sha-pinned caches; if a cache is missing or fails its sha,
  they are recomputed on the host that already holds that set under its custody rule (M1, or the laptop CPU where
  allowed; never the laptop for A-T3 val2017), never on a rented host. KV-4,224, A's registered test lists, Karpathy
  test, OV-test, XM-test2500 and C's unspent one-look sets never go to a rental. Custody-set features (UIT-ViIC 231,
  KTVIC 558): laptop CPU or M1 under §5.3. Comparison: on the laptop. Id-first rule (mirrors §5.3, CC-217r3 B-new-1): Before any image is staged on any host, Composite-COCO and Polaris-test-COCO are id/file-name matched on the laptop (ids only) against every COCO-id-space owner in b_pa1_owners.json (KV-4,224, Karpathy test, A-T3 val2017, the 3,454 M0 ids, UIT-ViIC test and train pool, COCO restval, UT-2,402, and the rest). Id-matched images are excluded and never staged on a rental. Only the id survivors and the Objects365 slice frame go to the 4090, for C1-C3 features. No COCO archive is placed on the rental. No B decode or score runs before the full W25 exclusions are applied.
- **Never its own owner (W3):** a set is not matched against its own lists. Composite-COCO and Polaris-test-COCO are
  filtered against every other owner, but not against A's registered Composite/Polaris lists
  (`manuscript/prereg/2026-10-14_h1_polaris_docci.md`, G2 Polaris test); B's dev use of them is the disclosed reuse of
  §2 / N9.
- **Deferred owners (W8):** an owner set the group does not yet hold (C's planned one-look sets: ViTextCaps test,
  NoCaps test, VieCap4H private test, until held) is listed in `b_pa1_owners.json` as a deferred W25 owner with a count,
  and is covered later against `b_pa1_dev_contacts.json` when it arrives. It is not a "not clean (a)" stop for B. This
  is fixed in R5 before any feature pass.
- **Owners, resolved at run time:** `b_pa1.py owners` builds `b_pa1_owners.json` from the PORTFOLIO_3Y §2.3 ledger and
  every one-look/spent list under `manuscript/prereg/` at HEAD; its sha is frozen before any feature pass. Never a
  closed list; at least:
  - MT4 KV-4,224 (COCO instances_val2014; `2026-10-28_mt4_kv`);
  - A's test sets: A-T3 val2017 ids (`2026-10-30_a_t3/val2017_ids.txt` `ea37cee0`, 5,000) and every other set in A's
    registered test lists (XM600, PASCAL-50S, ADE20K val, H-500);
  - COCO Karpathy test 5,000, incl. the 91 VSPS-J M0 ids (`karpathy_test_val_ids.txt` `88e40e3c`);
  - C's spent tests: OpenViIC test (OV-test, 2,001), XM-test2500, C-T3 Flickr30K test 1,000 (`c_t1_f30k_lists.json`);
  - C's planned one-look sets: ViTextCaps test, NoCaps test, VieCap4H private test (PLAN_2026-11-01 l.70), and any
    CC-214 assignment present at run time;
  - VSPS-J M0 dev-touched 3,454 COCO ids (`dev_touched_ids.txt` `91db7e2f`; the 786 M-HalDetect val ids are a subset);
  - VSPS-J E1a: UIT-ViIC test 231 (`exclusion.json` `c52a96d1`);
  - B4 COCO restval, UIT-ViIC train pool, UT-2,402 (MT4/K2), OIV7 val (incl. nocaps val), XM3600, AMBER generative
    1,004; KTVIC test 558 (custody features);
  - `b_pa1_dev_contacts.json` itself, for every later pass (§3).
- **Excluded from:** B (B registers after every current owner).
- **Expected attrition and shortfall branch (N8):** Composite-COCO and Polaris-test-COCO are val2014 ids, matched by
  id against KV-4,224, Karpathy test, the 3,454 M0 ids and val2017; under independence roughly 25-30% may go (AI
  estimate, not a target). E1/E2 run on the survivors whatever the count; a set with fewer than 500 surviving images
  is labelled THIN and no English tier-1 conclusion is drawn from it. Nothing is added to replace the losses.
- **Clean (W16):** W25 is "not clean" iff (a) the pre-fixed rule cannot be applied to a set (missing ids or images for
  an owner), or (b) an exclusion is not traceable to C1-C3 or an id match. For Objects365 val that fires PA3 (§11); in
  tier 1 it stops the affected block.
- **Report:** count only, no reason text (PI-1101p Q3); no overlap wording (PI-1101o).

## 6. VN → Objects365 class map and the parity gate (W10; v3 §3.2; B1)

### 6.1 Build and amendments
- Sources: the 365 Objects365 class names, read from `categories[]` of the PI-downloaded train annotation file through
  a pinned extractor (streamed, `categories[]` only; `annotations[]` is read only at §6.4 step 6; W11; the file sha256
  and the extracted class-list sha256 are registration item R6), since no local class list exists in the repo; existing Vietnamese dictionaries in the repo; Paper A's tone-normalised
  COCO-80 lexicon (matcher v2, cited as A). No new human labels. Entries proposed by an open LLM are tagged `instrument`
  (never gold) and listed separately; the instrument LLM's id, revision and prompt sha are recorded in
  `b_pa1_registry.json` (W2). Shipped with the map: an Objects365 → COCO-80 crosswalk (parity gate and the COCO-80
  sensitivity only), frozen together with map v1.
- **Map v1** is built on the laptop and sha-frozen before the parity gate and before any gold join.
- **Segmenter and stop list (R7, W2):** the Vietnamese word segmenter (name, version, sha) and the stop-list file (sha)
  are pinned in R7 and logged with the map v1 sha at §6.4 step 1, before any slice-A caption exists. The same segmenter
  is used for the H2 segmentation transform (§8.4).
- **Amendments (B1b):** triggered only by coverage statistics: (i) word tokens (R7 segmenter) occurring in ≥ 10
  slice-A captions of the 4 accepted captioners, not covered by any map entry or the R7 stop list; (ii)
  Objects365 class names with no Vietnamese entry. Never by any output of B's decomposer or verifier, the judge,
  CLIPScore, gold precision, or B-vs-gold or judge-vs-gold residuals. **Amendments are add-only:** a new entry for a
  token from (i) or a Vietnamese entry for a class from (ii), pointing to an existing class, tagged `dictionary` or
  `instrument`. No existing entry is edited or removed (an existing entry is covered, so no coverage statistic can
  prompt a change to it). Each addition is logged with a UTC time in `b_pa1_map_amendments.log`. UIT-ViIC 231 references are not a coverage source (they are parity-gate input).

### 6.2 Dictionary-only sensitivity (W10)
Every Objects365-gold analysis is repeated with the map restricted to `dictionary` entries. Reported beside the main row,
outside every Holm family.

### 6.3 Parity gate (pre-fixed stop rule; B1a, B1d)
- Matcher v2 = Paper A's Vietnamese matcher (`rescap/chair.py` `e47d249a`; lexicon file set pinned at registration, R3).
- **Where:** CPU on the laptop, on the human Vietnamese references of UIT-ViIC test 231 against COCO instances.
- **Statistic (micro over mentions):** a mention is a distinct COCO-80 class named in one reference. For each matcher,
  P = (number of mentions whose class is in the image's COCO instance gold) / (number of mentions), pooled over all
  references of the 231 images. The new-map side maps Vietnamese → Objects365 → COCO-80 through the crosswalk; its
  mentions with no COCO-80 counterpart are dropped and counted. References with no mention under a matcher are dropped
  from that matcher and counted. **Δ = 100 × (P_new − P_v2) in points.** The macro form (mean per-reference precision
  over references with ≥ 1 mention) is printed beside it, descriptive, with no stop.
- **Run 1 (binding):** once, on map v1, before any amendment. **|Δ| > 2.0 → PA3 fires, irrevocably**; no later
  amendment or re-run can undo it. Until step 4 of §6.4 closes, run 1 prints only the micro Δ, the macro row and the
  drop counts (W1).
- **Run 2:** on the final map sha (§6.4 step 5), same statistic, same stop.
- If captioner captions of the 231 exist from the M1 block, the same statistic on them is a descriptive second row
  with no stop (O6).

### 6.4 Order of operations (B1c; enforced by the scorer, which refuses to compute any τ of B before step 7's file exists)
1. Build map v1 and the crosswalk from `categories[]` (pinned extractor); freeze their shas; log them with the R7
   segmenter and stop-list shas (laptop).
2. Parity run 1 on map v1 (laptop CPU). Stop rule §6.3.
3. **A1-decode:** slice-A captions of the 4 accepted captioners (captions only; no decomposition, verification, judge
   or gold; W1).
4. Coverage statistics → amendments (§6.1), each UTC-logged; then **all amendments close and the final map sha is
   frozen**. No amendment after this step, in tier 1 or later.
5. Parity run 2 on the final map sha. Stop rule §6.3. After this step: **A1-score** (decomposition, verification at
   (d1,v1), judge J-a, CLIPScore on the A1 captions), then A2, A3 and H (GPU, no gold on the host; W1).
6. Gold join of slice A on the laptop with the final map (first read of `annotations[]`).
7. Baselines only: judge-prompt selection (§7.1), SE_A, SESOI, NI (§8.5); write `T1_THRESHOLDS.json` with SESOI, NI, the
   final map sha and the chosen judge prompt id; its sha is written to LOG before step 8.
8. Only then is any τ of B opened: lever selection (§7.2), planning numbers (§8.6), the PA3 effect trigger (§11), every
   B-τ row.

## 7. The metric, baselines and selection

### 7.1 Components
- **B's score:** the decomposer (Qwen2.5-7B-Instruct) splits the caption into typed propositions; the verifier
  (Qwen2.5-VL-3B-Instruct under Rule S) answers yes/no per object proposition from the image; score = share of mapped
  object propositions answered yes among those not abstained.
- **Yes/no tokens (N5):** at the first answer position, yes-probability = Σp(Y) / (Σp(Y) + Σp(N)). Vietnamese prompts:
  Y = first-token ids of {"có", "Có", " có", " Có"}, N = first-token ids of {"không", "Không", " không", " Không"};
  English prompts: {"yes", "Yes", " yes", " Yes"} and {"no", "No", " no", " No"}. A first-token id shared by Y and N is
  removed from both. Yes iff yes-probability ≥ 0.5. **Abstain** iff the top-1 token at that position is in neither set.
  The resolved id sets per tokenizer go into `T1_CONFIG.json`.
- **Abstain rule:** primary: abstains removed from numerator and denominator, abstain rate reported (credited to FAIR
  2026). Sensitivity: abstain-as-wrong, outside every Holm family.
- **Same-backbone judge (primary control):** the verifier model prompted once per caption, restricted to objects to match
  B's domain: J-a (yes-probability, same token sets, that every mentioned object is present), J-b (object-correctness
  score on a **0-9** scale, expected value over the ten single-digit tokens, so no multi-token "10"; N5), J-c (overall
  factual correctness on the same 0-9 scale). **Selection:** the prompt with the highest τ_c vs gold on the
  gold-defined caption set of the 4 accepted **tier-3** captioners on slice A (the same set as SE_A; O10, N2) is kept,
  so the baseline gets its best tier-1 setting. Ties within 0.005 → J-a, then J-b.
- **Multilingual CLIPScore (secondary control):** M-CLIP XLM-R + ViT-H/14 as pinned in C-T1, w = 2.5, no tuning.

### 7.2 Levers (B2): one factor at a time, 3 configurations
- d1 = zero-shot typed-proposition instruction; d2 = d1 plus 3 fixed worked examples written for this prereg (no dataset
  caption text). v1 = Vietnamese yes/no question containing the proposition; v2 = English instruction, proposition in
  Vietnamese, yes/no answer.
- Configurations: **(d1,v1)** (in A1), **(d2,v1)** and **(d1,v2)** (block A3). (d2,v2) is not run.
- **Comparison set:** the gold-defined caption set of the 4 accepted tier-3 captioners on slice A (≥ 1 mapped
  mention), with B's score imputed as 0.5 wherever it is undefined, so all three configurations are compared on the same
  captions. Criterion: τ_c of B vs gold. **Tie order:** any configuration within 0.005 of the best yields to the
  simpler one, in the order (d1,v1) → (d2,v1) → (d1,v2).
- **If A3 is trimmed or stops early:** (d1,v1) is frozen into `T1_CONFIG.json` and A3 is reported NOT RUN; a partial A3
  is never compared.
- No other knob. After tier 1 every choice is frozen into `T1_CONFIG.json` (sha) and copied verbatim to the tier-2 and
  tier-3 preregs.

### 7.3 Analysis set
- Primary: captions with defined gold precision (≥ 1 mapped mention) and a defined B score (≥ 1 non-abstained mapped
  object proposition); judge and CLIPScore on the same captions. Removed captions are counted, and the **drop rate per
  captioner** is reported (N2).
- Sensitivity (N2): the gold-defined set with the pre-fixed 0.5 imputation, outside every Holm family.

### 7.4 Prompt pins (W6, W7)
- Every prompt text (d1, d2, v1, v2, J-a, J-b, J-c, the captioner prompt, the instrument-LLM prompt, and the English
  E1 decomposer and verifier prompts) is written into `b_pa1_registry.json` and pinned by sha256 in a gatekeeper LOG line
  **before block S**.
- E1 (English dev) uses one fixed English decomposer prompt and one fixed English verifier prompt, pinned as above
  before any E1 output. E1 runs at the (d1,v1)-equivalent English pair and is **never re-selected**, whatever A3 finds.

## 8. Statistics

### 8.1 τ and ties
τ_c via `scipy.stats.kendalltau(x, y, variant="c")`, scipy pinned in the venv freeze; ties kept, never broken at random.
τ_b is a sensitivity outside every Holm family. Unit: one caption; all captions of the tier-3 captioners pooled.

### 8.2 Bootstrap
Image-cluster percentile bootstrap (all captions of an image move together), B = 10,000 resamples,
`numpy.random.default_rng(20261101)`. Same settings at tiers 2 and 3.

### 8.3 Holm family F1 and CI levels (W9)
- H1a gate (fixed sequence, first): pass iff the one-sided 95% lower bound of Δτ_c(B − judge) > −NI.
- If H1a passes, Holm over {H1b, H1c} at family α = 0.05, one-sided, with bootstrap p_j = (1 + #{Δ*_j ≤ SESOI}) /
  (B + 1). The smaller p is tested at 0.025; the other at 0.05 **only if the first passed** (step-down: if the first
  fails, neither passes). In CI terms: the first passes iff its one-sided **97.5%** lower bound > SESOI; the second,
  only after the first passed, iff its one-sided **95%** lower bound > SESOI. Every reported CI is printed at its
  Holm-adjusted one-sided level.
- At tier 1 these are descriptive planning numbers on slice A.

### 8.4 H2 (PA2 suite, registered secondary; N4)
- Transforms (v3 §3.6): final punctuation, NFC/NFD, tone-mark placement, syllable vs word segmentation, case,
  whitespace. v3 applies them to human references; here, for B's reference-free score, the transformed text is the
  scored caption; for reference-based metrics, the candidate is the chosen reference (transformed or not) and the
  references are the other references of the image, untransformed. The segmentation transform uses the R7 segmenter
  (§6.1; W2).
- **One KTVIC reference per image:** the reference at position argmin_k sha256(`b-pa1-ktvic-ref|` + file_name + `|` + k).
- Invariance of one item = |Δ score| ≤ 0.01 (BLEU, BERTScore, B, all on a 0-1 scale); CIDEr ≤ 0.1.
- **Test (registered at tier 2, slice B):** per transform t, r_t = share of invariant items over one caption per
  slice-B image (captioner picked by argmin over the 4 of sha256(`b-pa1-h2|` + file_name + `|` + captioner id)); t
  passes iff the one-sided image-bootstrap lower bound of r_t at its Holm level > 0.95; Holm over the 6 transforms,
  α = 0.05. Never on Objects365 val; reported as a dev result. Tier-2 cost is projected in the tier-2 prereg
  (2,000 × 6 × 1.6 s ≈ 5.3 h on a 4090 at the assumed rates).
- **Tier 1:** descriptive only: block H (gate subset of slice A, same picking rule) and the KTVIC row of the M1 block.

### 8.5 SESOI and NI margin (W3; B1c)
- **Inputs: baseline outputs only.** SE_A = image-bootstrap SD (§8.2) of τ_c(selected judge) vs gold on the
  gold-defined caption set of the 4 tier-3 captioners on slice A. No B output enters the rule.
- **SESOI = max(0.02, 2·SE_A). NI = 0.02.** The between-baseline spread |τ_c(judge) − τ_c(CLIPScore)| is printed
  beside them, descriptive.
- Written once in `T1_THRESHOLDS.json` at §6.4 step 7, with the final map sha. **Never recomputed downward:** any later
  recomputation (a resume included) may only keep or raise SESOI and keep or lower NI. Later preregs may only tighten.

### 8.6 Which PASS P(PASS) ≥ 0.98 refers to (W9; N3)
- The tier-3 PASS the abstract would state is **H1b**: Δτ_c(B − same-backbone judge), one-sided lower bound > SESOI at
  the conservative Holm step-1 level 0.975. H1b implies H1a (SESOI > 0 > −NI). H1c and H2 do not enter P(PASS).
- Tier 2 (planning form fixed now): P(PASS) = share of the 10,000 slice-B image-bootstrap draws for which
  Δ*_B + ε_val − z₀.₉₇₅·SE_val > SESOI, with ε_val ~ N(0, SE_val²) drawn per resample, SE_B = SD of the Δ*_B and
  SE_val = SE_B·√(n_B / N_val) (v3 P8). This is a planning value, labelled so. Only Δτ is assumed to transfer.
- Tier 1 prints the same number from slice A as a planning value.

### 8.7 Sensitivity outside every family (N1)
Δτ_c(B_open − judge), where B_open is B's score over **all** object propositions (mapped or not), against the same gold,
on the same captions. Registered now, so it is not post hoc; reported beside H1b without a verdict.

## 9. GPU, rates, cap, stop (N2 of CC-213r2; v3 §4)

### 9.1 Tier-1 blocks on one named RTX 4090
The host is named in the R5 launch amendment by its ckey instance id only, with that instance's hourly rate restated
(17,513 VND/h below is M5's past rate), and gets a one-judge diff read before any GPU step (N15). Assumed per-caption
costs on a 4090, to be measured in block S: decode 0.56 s (3090 short-mode 0.8409 s / 1.5, an assumption),
decomposition r_e 0.6 s, verification p·r_v = 5 × 0.2 s, judge r_j 0.25 s, CLIPScore 0.01 s; pipeline ≈ 1.86 s.

| block | content | GPU-h est. |
|---|---|---|
| W | W25 features of the slice-A frame, Composite-COCO, Polaris-test-COCO only (§5.4) | 1.0 |
| S | smoke and rate measurement (64 slice-A images; B, judge and CLIPScore smoke outputs kept only as rates and deleted once the rate file is written) + Vietnamese-gate decodes, up to 10 candidates × 231 × 0.56 s | 0.9 |
| A1 | slice A × 4 accepted captioners: A1-decode (§6.4 step 3) + A1-score at (d1,v1), judge J-a, CLIPScore (after step 5) (8,000 × 2.42 s) | 5.4 |
| A2 | judge J-b, J-c on the same 8,000 captions | 1.1 |
| A3 | levers (§7.2): (d2,v1) 8,000 × 1.6 s = 3.6 h; (d1,v2) 8,000 × 1.0 s = 2.2 h | 5.8 |
| H | H2 descriptive: 231 captions × 6 transforms × 1.6 s | 0.6 |
| A4 | up to 3 dev-only captioners (6,000 × 2.42 s) | 4.0 |
| E1 | Composite-COCO (about 6,000 candidate captions × 1.86 s; no decode) | 3.1 |
| E2 | Polaris-test-COCO (count from metadata; at 20,000 captions about 10.3 h) | trimmed first |
| **total (E2 already excluded)** | | **21.9** (+25% = 27.4) |

- **Hard cap: 20 GPU-h** (top of the CC-213r3 P6 range), per-step `timeout` for the time left; a timeout is a final CAP
  STOP. The cap is fixed before registration and never changed after block S rates are seen (W13; PI Q-a: 20 vs
  22-24 GPU-h; default 20). **Trim order from the bottom: E2, A4, H, A3** (reported NOT RUN; A3 rule in §7.2). The core
  W + S + A1 + A2 + E1 ≈ 11.5 h (14.4 h with +25%) is never trimmed; if it cannot finish under the cap, tier 1 stops
  and the PI decides.
- **Run order (W5):** W, S, A1, A2, E1, then A3, H, A4, E2. E1 runs at (d1,v1), labelled so, and is not re-run if A3
  later selects another configuration.
- **Trim rule:** at the end of block S, with the measured rates, blocks are dropped from the bottom of the trim order
  until 1.25 × (projected remaining hours) ≤ remaining cap. At the assumed rates the trim rule drops E2, A4, H and A3
  (after S: 16.0 h × 1.25 = 20.0 > 18.1; without H, 19.25 > 18.1; without A3, 12.0 ≤ 18.1). The expected spend is then
  about 11.5 GPU-h plus 4 h setup, about 271,000 VND at 17,513 VND/h, and at most 420,000 VND at the cap. A3 is
  therefore expected NOT RUN and (d1,v1) frozen under §7.2, unless block S measures rates about 6% lower or the cap is
  changed before registration. (At the dedicated 4090's actual rate of 17,499 VND/h the figures round to the same
  271,000 and 420,000 VND; R5 restates the rate.)
- M1 block (custody rows, §5.3): about 5.8 h (W9), **hard cap 9 GPU-h** at M1's 9,282 VND/h (≈ 54,000 VND expected,
  ≤ 84,000 VND at the cap), only after MT4 releases M1.
- Stop: a CAP STOP is final. Machine loss or a guard failure → back up (30-min schedule), stop; **one** resume from
  checkpoints with the same shas, logged, and only for those two causes; then the PI decides.
- **Stagger (N10; v3 §4.3):** B tier 1 never takes A's 15-30/11 writing turn; B's 4090 rentals are staggered with C
  tier 3 and VSPS-J E2b on the dedicated 4090 (PI-1101r). No B 4090 step, block W included, before the commit, the R5
  amendment with its one-judge read, a logged PI top-up and the N18 novelty rescan (CC-217r2 Ruling 4).

### 9.2 Rates that leave tier 1 and the P3 projection (verbatim from v3 §4.2)
- Measured on the named 4090 at the end of tier 1: r_d,c per tier-3 captioner, r_e, r_v, p, r_j, r_clip, r_e,EN, p_EN.
- Written into the tier-2 prereg and copied verbatim into the tier-3 prereg:
  **P3 = Σ_c N_val·r_d,c + 4·N_val·(r_e + p·r_v + r_j + r_clip) + P_EN**, tier-3 cap = ⌈1.25 × P3⌉.
- **PI trigger:** P3 > 150 GPU-h (4090) → the PI decides the rental before tier 3; refusal or no top-up → PA3. W15:
  with 83.7 h of decode on a 3090 before the unmeasured terms, tier 3 plausibly exceeds 150 h.

### 9.3 Tier-3 start gate (W4; binds the tier-3 prereg)
- The one look starts only if: prereg cap ≥ ⌈1.25 × P3⌉; ckey balance in hours of the named 4090 ≥ ⌈1.25 × P3⌉ + setup
  (≥ 4 h) + 10%; remaining maximum rental time ≥ the same number.
- **PI-1101q** (LOG l.1091, 2026-11-01T13:02:30Z): ordinary GPU launches need not be covered by the balance for the
  whole chain. This stricter full-balance gate is kept **on purpose, for the irreversible one look only** (CC-213r3
  Ruling 4, P4 default); tier 1 and tier 2 follow PI-1101q.
- The rented host never loads Objects365 val box gold and never computes τ; scoring runs once on the laptop after a
  100% manifest; overrun or machine loss = stop, back up, seal, no output opened (v3 §4.2 items 5-6).

## 10. What tier 1 decides

- `T1_CONFIG.json`: accepted captioners, decomposer, verifier, judge prompt, CLIPScore model, (d,v) configuration,
  token-id sets, map sha, K, abstain rule, scorer sha.
- `T1_THRESHOLDS.json`: SESOI, NI, final map sha, judge prompt id (§8.5).
- Measured rates and P3 inputs (§9.2).
- Planning numbers on slice A: Δτ_c(B − judge) and Δτ_c(B − CLIPScore) with Holm-level bounds; planning P(PASS).
- Descriptive only, whatever the numbers: custody rows, English rows (H3), the open-vocabulary score and N1 sensitivity,
  count propositions, colour/attribute/action/relation rows, τ_b, partial τ (mentions per caption controlled),
  count-matched analysis, abstain-as-wrong, gold-defined-set sensitivity, COCO-80 restriction, dictionary-only map,
  system-level τ, H2 tier-1 rows.

## 11. PA3 triggers (pre-written numbers; v3 §7)

| trigger | number | when checked |
|---|---|---|
| fewer than 4 captioners accepted by the §4.3 walk | < 4 at ≥ 0.95 VN share | block S |
| parity gate run 1 (binding) or run 2 | |Δ| > 2.0 points, micro (§6.3) | §6.4 steps 2 and 5 |
| tier-1 effect (optimistic: the configuration is selected on the same slice A; slice B at tier 2 is the guard; W10) | point Δτ_c(B − judge) on slice A < SESOI from `T1_THRESHOLDS.json`, with the selected configuration | §6.4 step 8 |
| W25 not clean for Objects365 val (§5.4) or the PI does not approve the count-only wording | as defined | before tier 3 |
| Objects365 licence unusable or registration fails | — | before T1b |
| two tier-2 rehearsals with P(PASS) < 0.98 | 0.98 | tier 2 |
| no top-up, or the PI refuses the tier-3 rental (incl. P3 > 150 GPU-h) | 150 GPU-h | before tier 3 |
| machine loss, M1 busy or M1 lapsed | never a trigger | — |

PA3 content (v3 §7): the audit, card and kit go to A, or a Scopus conference kit paper, or VJCS (Q3); the metric is
reported as dev results only.

## 12. Audit record (prereg and decision files only; never paper, supplement or cover-letter wording; B4)

- Why only Δτ is claimed: the verifier and the judge may have seen Objects365 in pre-training; the exposure is shared by
  both sides of the contrast. The paper states only that absolute τ is not claimed to transfer from train to val, with
  no reason (§2).
- Captioner exposure to Objects365 can change caption content, not the validity contrast; recorded here, not written in
  the paper.
- W25 exclusions and their counts are internal records; the paper gives counts with no reason and no overlap wording.
- The `instrument` entries of the map and their source are recorded in `b_pa1_registry.json`; the paper wording is
  fixed by §2.
- If a PA3 trigger fires, it is reported briefly in B (PI-1029m form), never hidden, in the §2 wording.

## 13. Binding-rule compliance

- Three-tier method (PI-1029n): tier 1 on dev only; tier 2 on slice B; one look on Objects365 v2 val after a separate
  prereg and a panel GO ≥ 92. No sealed set is read, downloaded or staged in tier 1 or tier 2.
- No new human labels; AI output is never gold.
- Full official splits for val (tier 3); train slices are a pre-fixed, salted, disclosed dev partition of train.
- No caption text of any dataset in repo files; stores outside the repo. The gatekeeper runs the 8-gram scanner on this
  file before the commit (N16).
- No personal e-mail in any web request; no host, IP or port in repo files.
- No commit, no GPU, no machine access, no dataset download by the drafting agent.

## 14. Dispositions

### 14.1 CC-213r3 items (unchanged from v1 unless noted)
W1, W2 §3; W3 §8.5, §11; W4 §9.3; W5 §5.1; W6 §5.4; W7 §5.1; W8 §1; W9 §8.2, §8.3, §8.6; W10 §6.2; W11 §4;
W12 §5.3, §11; W13 §3, §4.2; W14 §2; W15 §9.2; W16 §5.4; W17 header; C1 STATE, STUDY_BRIEF_B, PLAN §3 and (v2)
RESUME_2026-10-31_paperB refreshed with pointer lines.

### 14.2 CC-217 non-blocking items

| item | disposition |
|---|---|
| N1 | registered: Δτ_c(B_open − judge), outside every family; claim wording does not credit decomposition alone (§1, §8.7) |
| N2 | gold-defined-set sensitivity with 0.5 imputation, drop rate per captioner (§7.3); judge selection on the SE_A set (§7.1) |
| N3 | P(PASS) labelled a planning value; ε_val ~ N(0, SE_val²) in the tier-2 form (§8.6) |
| N4 | H2 test: per-transform one-sided lower bound > 0.95 at Holm level; KTVIC reference by salted hash; v3 §3.6 reconciled (§8.4) |
| N5 | yes/no first-token id sets (VI, EN), abstain rule, judge scale 0-9 (§7.1); recorded in `T1_CONFIG.json` |
| N6 | lineage resolver = card, then technical report; undetermined = clash; Gemma-3n MobileNet-V5-300M written in, confirmed at pin; Qwen2.5-VL ViT init recorded (§4.1, §4.2) |
| N7 | substitution order deepened now (Phi-3.5-vision, Molmo-7B-O, in-slot substitutes) ahead of llava-1.5; nothing added after a gate result (§4.3) |
| N8 | W25 compute line (block W) and attrition/shortfall branch; FOIL train dropped (§5.1, §5.4) |
| N9 | KTVIC test 558 spend cited (CP-071, `a21a14c`, LOG l.349); A's Composite/Polaris use cited, A's H1 not re-claimed (§2, §5.1) |
| N10 | stagger with A's 15-30/11 turn, C tier 3, VSPS-J E2b (§9.1) |
| N11 | `b_pa1_dev_contacts`, OV-test, XM-test2500 and A's test sets named as owners (§5.4) |
| N12 | train JSON streamed (ijson pinned at R2; not installed on the laptop today) (§5.2) |
| N13 | Expert-subset sentence reworded (§3) |
| N14 | `manuscript/RESUME_2026-10-31_paperB.md` given a pointer line |
| N15 | R5 launch amendment: ckey instance id only, rate restated, one-judge diff read (§9.1) |
| N16 | the gatekeeper runs the scanner (§13) |
| N17 | BLEU/CIDEr of each tier-3 captioner on the UIT-ViIC 231 references: one descriptive row in the M1 block (§5.1) |
| N18 | v3 P10 novelty rescan before any 4090 spend; laptop, no GPU (§0, §9.1) |
| N19 | PI downloads only the train annotation file + `patch0`, `patch1`; any val file stays sealed, sha only (§3) |
| N20 | single pass on the spent Vietnamese sets; no tier-1 decision reads them (§5.1) |

### 14.3 CC-217r2 items
B1, B2, B3 and W1-W15: see the CC-217r2 closure table at the top. W14: `.claude/agents/STATE_2026-11-01.md` refreshed
for PI-1101r (dedicated 4090), PI-1101s (public released data), PI-1101t (Vietnamese main claim, English benchmark
only; consistent with E1/E2 as descriptive English rows) and PI-1101u (Paper C adopts PVR; noted only, no change to B).

## 15. Open questions (status after CC-217r2)

| # | question | status |
|---|---|---|
| O1 | size rule | **to the PI (CC-217 Q2); default S, one rule for every role**; the active rows of §4.2 follow S |
| O2 | Qwen2.5-VL as verifier/judge despite VSPS/C/VSPS-J use | allow, disclosed in B's model table (ruling 12, 92) |
| O3 | Aya-Vision-8B as tier-3 captioner | no; MiniCPM-V-4 holds the SigLIP slot; Aya dev-only under Rule N only (92) |
| O4 | Gemma-3n vision tower | MobileNet-V5-300M per CC-217 desk check; resolver at pin; undetermined = clash (90) |
| O5 | hypothesis labels | this draft's, with the crosswalk (93) |
| O6 | parity on the laptop CPU over human references; captions as a descriptive second row only from M1 | yes, under B1 (92) |
| O7 | slice frame `patch0` + `patch1`, else all train `images[]` | yes (90) |
| O8 | H2 registered on slice B, dev only | yes, with the §8.4 test (91) |
| O9 | SESOI = max(0.02, 2·SE_A), NI = 0.02 | yes, under B1 (92) |
| O10 | judge prompt by max τ_c on the SE_A caption set | yes (92) |
| O11 | Qwen-line text decomposer | yes (92) |
| O12 | Polaris trimmed first | yes (93) |
| O13 | count propositions descriptive | yes (94) |
| O14 (new) | gate set fixed to the first 231 slice-A images on the 4090, never UIT-ViIC 231 on M1 | recommended yes (one gate set, no M1 dependency); default yes |
| O15 | lever design one factor at a time (5.8 h) instead of the 2×2 grid (8.0 h) | one factor at a time (accepted in CC-217r2) |
| Q-a (PI) | tier-1 4090 cap 20 vs 22-24 GPU-h, fixed before registration | recommended (CC-217r2) 22 h so A3 can run; **default 20 h, A3 expected NOT RUN, (d1,v1) frozen** |
| Q-b (PI) | custody covers owners' W25 features of every test-role set; nothing but the slice-A frame, Composite-COCO and Polaris-test-COCO on a rental | recommended YES / NO rental; default as CC-209 (written into §5.4) |
| Q-c (PI) | Rule S for every role | recommended S; default S, fixed before the first model output |
| Q-d (PI) | arrival of the Objects365 train annotations + `patch0`, `patch1` (critical path) | as soon as possible; default laptop T1a only until then |

Registration items (gatekeeper, not the judge). **Each is pinned by a sha-bearing gatekeeper LOG line before the first
step that reads it (W4):** R1 model pins, gate acceptance and lineage sources (before that model's first output); R2
venv freezes incl. ijson (before step 1); R3 matcher v2 file set and shas (before step 1); R4 `b_pa1.py` selftest and
SHA256SUMS; R5 the 4090 launch amendment (ckey instance id only, rate restated, deferred-owner list; its own amendment
and one-judge read); R6 sha256 of the Objects365 train annotation file and of the extracted `categories[]` class list (at
step 1); R7 segmenter name, version and sha, and stop-list sha (before step 1, logged with map v1 at step 1); prompt
shas (§7.4, before block S).

Note on N7: the added candidates 8-10 (Phi-3.5-vision, Molmo-7B-O, llava-1.5) share the CLIP vision line, so the list
offers 5 captioner lineage pairs for 4 slots, the same tolerance as v1; the in-slot substitutes (2, 4) add depth only
within their slot.
