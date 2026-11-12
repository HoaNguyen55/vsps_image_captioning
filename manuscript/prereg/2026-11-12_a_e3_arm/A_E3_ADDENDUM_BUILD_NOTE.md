# A-E3 addendum: build note (2026-11-12)

Writer agent. Every file was written under `~/a_e3_addendum_stage/`, which mirrors repo paths. Nothing was written under `/mnt/d`. There was no commit, `git add`, LOG line or CC file.

On hc2 the writer touched only `/root/venv-lb26` and `/root/a_e3_addendum_tmp`, plus pip's own `/tmp/pip-*` temp dirs, which pip removed. The writer used no GPU, loaded no model, fetched no weights, and did not touch `/root/a_e3/out`, `/root/a_e3/vsps`, `/root/a_e3/models`, `/dev/shm/a_e3`, `/root/outputs`, `/root/vsps`, `/root/c_attr_score`, `/root/a_vp_tree` or `/root/ncs-data`. Every ssh output was filtered for IPv4-shaped strings.

## 1. Host commands (UTC from `date -u`, for the coordinator's OPS lines)

| UTC | Command (`ssh -o BatchMode=yes hc2 …`) | Result |
|---|---|---|
| 08:50:38 | read-only facts: `date`; `/root/venv-lb/bin/python -V`; `pip --version`; `pip freeze \| sha256sum`; `pip freeze \| wc -l`; `head -2 /proc/driver/nvidia/version`; `df -BG /root`; `free -g`; `nproc`; `ls -d /root/venv-lb26 /root/a_e3_addendum_tmp` | Python 3.10.22; pip 23.0.1; freeze `685ffe2a…` (= H_LB), 43 lines; driver 580.126.09; 716 G free; 62 G RAM; 32 CPUs; neither path existed |
| 08:50:38–08:56:50 (no stamp of its own; bounded by its neighbours) | `/root/venv-lb/bin/python -m pip freeze`; `readlink -f /root/venv-lb/bin/python`; `cat /root/venv-lb/pyvenv.cfg` | base interpreter `/usr/bin/python3.10` 3.10.22 |
| 08:58:38 | `mkdir -p /root/a_e3_addendum_tmp`; `pip freeze > lb.freeze` (venv-lb); `grep -v -E '^(torch\|torchvision\|triton\|nvidia-[a-z0-9-]+)==' lb.freeze > rest.txt` (28 lines); write `build_lb26.sh` (try 1); `nohup nice -n 19 ionice -c3 ./build_lb26.sh` | started 08:58:41 |
| 08:58:56–09:02:38 | progress reads: `tail` of the build log, `du -sh`, `ps` for pip | – |
| 09:00:18 | laptop `git archive HEAD scripts/lb/decode_hf_vlm.py scripts/g2b/decode_qwen3vl.py scripts/evaluate.py rescap` piped to `tar -x -C /root/a_e3_addendum_tmp/tree`, then `sha256sum` of the four pinned files | all four equal to their SHA256SUMS_E3 lines (`e2de1881`, `8a855ef4`, `a68d5682`, `e8fee5bc`) |
| 09:02:52 / 09:04:59 | try 1 failed: torch from the cu124 index first. A typing_extensions wheel was discarded, and its sdist needed `flit_core`, which the cu124 index (`--index-url` only) lacks. Nothing beyond the empty venv was installed. Log kept as `build_lb26.try1.log` | – |
| 09:05:16 | write `build_lb26.sh` (try 2: `rm -rf /root/venv-lb26`; `python3.10 -m venv`; `pip install --no-cache-dir --no-deps -r rest.txt`; `pip install --no-cache-dir --index-url https://download.pytorch.org/whl/cu124 torch==2.6.0+cu124 torchvision==0.21.0+cu124`; `pip check`; `pip freeze > lb26.freeze`; freeze sha); `nohup nice -n 19 ionice -c3 ./build_lb26.sh` | started 09:05:19; `BUILD_DONE` 09:18:26; `pip check`: "No broken requirements found." |
| 09:08:47–09:18:31 | progress reads (`tail`, `du -sh`) | – |
| 09:18:39 | `cat lb26.freeze.sha256`; job-form `pip freeze \| sha256sum` for both venvs; `diff lb.freeze lb26.freeze`; `sha256sum` of the work files | lb26 `396626b4c55db0deb5bd6b7738a4b0740ca0ae5d3ba5b77b5950de375580ed51` (44 lines); lb unchanged `685ffe2a…` |
| 09:19:02 | `CUDA_VISIBLE_DEVICES= nice -n 19 ionice -c3 /root/venv-lb26/bin/python -I -B -c …` in `tree/`: the four package versions, `masking_utils._is_torch_greater_or_equal_than_2_6`, `torch.version.cuda`, the image-text-to-text map for `gemma3` and `llava_next` | `{"torch": "2.6.0+cu124", "torchvision": "0.21.0+cu124", "transformers": "4.57.6", "accelerate": "1.15.0"}`; `True`; 12.4; `Gemma3ForConditionalGeneration`, `LlavaNextForConditionalGeneration` |
| 09:19:08 | `CUDA_VISIBLE_DEVICES= nice -n 19 ionice -c3 /root/venv-lb26/bin/python -I -B scripts/lb/decode_hf_vlm.py --selftest > ../selftest_lb26.log` (in `tree/`, no `--prereg`) | rc 0 at 09:19:11; 15 PASS + `selftest ok`; plus two library warnings (slow image processor; `torch_dtype` deprecated); log sha `165a7200f82ab953509c10253a807a578ebc803bbad016a3658d8682ca9ffd08` |
| 09:20:13 | `du -sh /root/venv-lb26 /root/a_e3_addendum_tmp`; `df -BG /root` | 5.2 G; 764 K; 711 G free |

Work-file shas on the host:
- `lb.freeze` `685ffe2a…`
- `lb26.freeze` `396626b4…`
- `rest.txt` `224cad34e00b160ea9fdd98639540d8ba9636b40237109516be6d85595afb036`
- `build_lb26.sh` (try 2) `6579fe7cf1e2f024339f9aa835e62438fbdd3668b987728ffa6702eeb05009b1`

`/root/a_e3_addendum_tmp` is throw-away. It may be deleted after the coordinator has logged these lines. `/root/venv-lb26` stays: it is the registered second environment.

## 2. venv-lb26 freeze (44 lines)

```
accelerate==1.15.0
certifi==2026.7.22
charset-normalizer==3.5.2
docopt==0.6.2
filelock==3.32.3
fsspec==2026.7.0
hf-xet==1.7.0
huggingface_hub==0.36.2
idna==3.20
Jinja2==3.1.6
MarkupSafe==3.0.3
mpmath==1.3.0
networkx==3.4.2
num2words==0.5.14
numpy==2.2.6
nvidia-cublas-cu12==12.4.5.8
nvidia-cuda-cupti-cu12==12.4.127
nvidia-cuda-nvrtc-cu12==12.4.127
nvidia-cuda-runtime-cu12==12.4.127
nvidia-cudnn-cu12==9.1.0.70
nvidia-cufft-cu12==11.2.1.3
nvidia-curand-cu12==10.3.5.147
nvidia-cusolver-cu12==11.6.1.9
nvidia-cusparse-cu12==12.3.1.170
nvidia-cusparselt-cu12==0.6.2
nvidia-nccl-cu12==2.21.5
nvidia-nvjitlink-cu12==12.4.127
nvidia-nvtx-cu12==12.4.127
packaging==26.3
pillow==12.3.0
psutil==7.2.2
PyYAML==6.0.3
regex==2026.9.29
requests==2.34.2
safetensors==0.8.0
sympy==1.13.1
tokenizers==0.22.2
torch==2.6.0+cu124
torchvision==0.21.0+cu124
tqdm==4.70.1
transformers==4.57.6
triton==3.2.0
typing_extensions==4.16.0
urllib3==2.8.0
```

`diff lb.freeze lb26.freeze` changes only torch, torchvision, triton and these nvidia-* lines:
- cublas 12.1.3.1 → 12.4.5.8;
- cupti, nvrtc, runtime and nvtx 12.1.105 → 12.4.127;
- cufft 11.0.2.54 → 11.2.1.3;
- curand 10.3.2.106 → 10.3.5.147;
- cusolver 11.4.5.107 → 11.6.1.9;
- cusparse 12.1.0.106 → 12.3.1.170;
- nvjitlink 12.9.86 → 12.4.127;
- cusparselt new 0.6.2.

cudnn 9.1.0.70 and nccl 2.21.5 are unchanged. The writer's ssh filter hid dotted four-part version strings, so the diff was re-read with dots masked.

## 3. Hub research (laptop, unauthenticated, generic client name, 08:50–09:00Z)

- **Granite pins:** from `GET https://huggingface.co/api/models/ibm-granite/granite-vision-3.3-2b/tree/bf66a8244401a8e26d2ff429aa82df8550a289e5?recursive=1`. Response sha `04758dd8af3136056cd4aa1ff1c319d733af80accdd7d84714335a0d7bcab844`; `lfs.oid` for the 2 safetensors and `oid` for 12 blobs.
- **Granite revision info:** `GET …/revision/bf66a824…`, response sha `da9a380612b10a7927e9d81e0e2ca225555c3b69cc2009926fc37ac691bef3b6`, `gated: false`.
- **Small files read** (config, processor and tokenizer configs, cards): read over `resolve/<revision>/`. No weight file was fetched, and no pin was made by hashing a fetched file.
- **Static loadability:** checked against the transformers v4.57.6 sources on GitHub: `modeling_auto.py` image-text-to-text map; `configuration_auto.py`; `processing_auto.py`; `_supports_sdpa` in the `llava_next`, `granite`, `lfm2_vl`, `lfm2` and `siglip2` modelling files; `masking_utils.py` l.808–816 and l.904–912.
- **LFM2-VL fixes outside 4.57.6:** the GitHub commit list for `src/transformers/models/lfm2_vl` (main vs the v4.57.6 tag) shows #41755 and #41742 after the 4.57.0 branch point. The compare of `87be5595` with v4.57.6 shows the two have diverged.
- **Grid swap checked in code, 09:21–09:23Z:** `image_processing_lfm2_vl_fast.py` at `87be5595` against v4.57.6. The only behavioural difference is l.397, `num_rows, num_cols` → `num_cols, num_rows`; the rest is typing. PR #41755's body says it fixed "swapped rows and columns that were resulting in incorrect positional special tokens". The LFM2-VL-3B LICENSE was read (l.31, l.33, l.57: research use allowed).
- **The REG_v2 builder** (final build 2026-11-12T09:24:34Z, after the addendum text was final) (`make_reg_v2.py`, scratchpad, not for the repo) self-checks that:
  - every v1 key and value is unchanged except title, statement, built_utc, git_head_at_build, venv, models, runs and sources;
  - the six v1 model blocks and the 48 v1 runs are unchanged prefixes;
  - `gemma3_4b_lb26` equals the v1 `gemma3_4b` block;
  - every v1 source is unchanged.
- **A static re-check of REG_v2** against the decoder's registration rules (schema, unique run ids, every run naming a registered model, set and mode, 40-hex revisions, hash kinds and lengths, no remote code, decoder pin) passed on the laptop: 8 models, 64 runs.

## 4. Job changes the judge may refuse (CC-351 carried items)

They are in `scripts/a_e3/a_e3_job.sh` v2 and in `A_E3_JOB_V2.diff`. To refuse them, revert exactly these lines to their v1.1 text:

- **N2'** (the two lines after the c_attr_b1 check):
  - `g=$(nvidia-smi --query-compute-apps=pid --format=csv,noheader) || stop "nvidia-smi failed (CC-351 N2')"`
  - `[ -z "$g" ] || stop "GPU busy"`
  - v1.1: `[ -z "$(nvidia-smi --query-compute-apps=pid --format=csv,noheader)" ] || stop "GPU busy"`
- **N10** (in `dec()`):
  - `timeout -k 120 "$t" …`; v1.1 `timeout "$t" …`
  - `{ [ "$rc" = 124 ] || [ "$rc" = 137 ]; } && [ "$t" -lt "$3" ] && return 2  # 137: killed by -k (CC-351 N10)`; v1.1 `[ "$rc" = 124 ] && [ "$t" -lt "$3" ] && return 2`
  - Rc 137 has to count as a cap cut too. Otherwise a run killed by `-k` on its second attempt would be logged MODEL FAIL instead of CAP STOP.

N11 (ledger row written only after an attempt) is not touched.

## 5. Checks run on the deliverables (laptop: only `bash -n`, as the brief allows)

- `bash -n scripts/a_e3/a_e3_job.sh`: OK.
- `A_E3_JOB_V2.diff` = `diff -u` of `a_e3_job.sh` v1.1 (`b11a9f6b…`, from HEAD 4605e74, unchanged since 26574ef) → v2. Its two header lines are labels, as in `A_E3_JOB_W.diff`.
- `SHA256SUMS_E3_V2`: the nine unchanged lines of `SHA256SUMS_E3` copied verbatim (the job line dropped), plus the addendum, REG_v2 and the new job, all hashed in the staging tree.
