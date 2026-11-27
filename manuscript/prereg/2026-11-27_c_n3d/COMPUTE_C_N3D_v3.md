# COMPUTE C-N3D v2 (draft; v1 2026-11-27T12:14Z, revised under CC-509)

## 1. Resources

| item | value |
|---|---|
| GPU | **none** (no decode; every input is a stored decode) |
| where | **a rented host only** (PI 11-11, tests on the rented host). The laptop writes files and computes nothing. The PI's PC is not used. |
| CPU estimate | about 0.7 CPU-h in total: scoring of 6 arms × 3 backbones × 2 sets plus the English arms (about 0.2 h, mostly RDRSegmenter); matcher and copy statistic over about 25k captions (about 0.1 h); bootstrap B = 2,000 for the main rows, the placebo split and SR1–SR7 (about 0.3 h); self-tests, mutants and the custody check (about 0.1 h) |
| hard stop | **4.0 CPU-h** wall on the host. Reaching it is a STOP, and no partial output is used. |
| host share [W2] | a rented host only: a dedicated rental, or a host rented for a non-C-CONF job (for example B-D1) after its registered job ends. Never a host that holds, or will hold, any OV-test byte (the committed name-and-sha256 list `ov_test_files.tsv` is not an OV-test byte; CC-483r2 ruling 5), the C-CONF token or a C-CONF output. |
| memory, disk | under 4 GB RAM; under 250 MB of inputs, pushed to tmpfs on the host |
| outputs | aggregates only: counts, shares, CIs, p̃ and labels, in one JSON decision file plus its sha256. No captions and no per-image rows leave the host. Per-image intermediates on the host are deleted after the decision file is hashed; the session record keeps their sha256. |

## 2. Inputs by sha256 [W1, W3, W6c, N1]

All paths are under `/mnt/d/vsps_image_captioning/` unless marked "(paper repo)", which means `/mnt/d/vsps_papers/vsps-paperC-tallip` at 9bf8f89, read through `~/vsps_ro3/c_now`.

Checks made on 2026-11-27:
- The batch-1 files match their `.sha256` sidecars.
- The stage-2 and `ex_*` files match `scripts/c_attr/STORED_SHA256` and their sidecars.
- `c_attr_lists.json` and the Flickr30K files match their sidecars.
- `c_attr.py` and `c_attr_score.py` match `scripts/c_attr/SHA256SUMS`.
- `lists.json`, `ov_test_files.tsv` and `c_conf_carve_order.json` match their registration `SHA256SUMS` or REG2 pins.
- The gold pins are the values in code or a registration, cited beside each one.

The host STOPs on any per-file mismatch.

### 2.1 PUSH LIST (the only files pushed to the host)

Decodes, shown lists, SR3 and English (54 files):

```
10e3aa226b624286d0b980c04ad201b7da8293fe1135a765ee8586742616fcfd  .session_backup/machines/ATTR_H1/root/outputs/c_attr_b1/out/at_aya_vision_8b_ov_dev_b-rand-k4--T1-d0-mvi-b1.preds.json
3b6f81e451b6ced65ffd2439d6447a787964263ef884d320153ebc0c61cde5ae  .session_backup/machines/ATTR_H1/root/outputs/c_attr_b1/out/at_aya_vision_8b_ov_dev_b-rand-k4--T1-d1-mvi-b1.preds.json
42f42f902957a342bd5edd716b5f284112eb7f1be933b76aff49803e09b14f4b  .session_backup/machines/ATTR_H1/root/outputs/c_attr_b1/out/at_aya_vision_8b_ov_dev_b-rand-k4--T1-d2-mvi-b1.preds.json
3fdcc1852790732f6fee6c976cdd831841da2e321f94080f741e35f956bee6b1  .session_backup/machines/ATTR_H1/root/outputs/c_attr_b1/out/at_aya_vision_8b_ov_dev_b-ret-k4-last-T1-mvi-b1.preds.json
086810b19b315e258cb7b00c9a46508dc9c72ff6c2d94aadfcbf6ea6986c4603  .session_backup/machines/ATTR_H1/root/outputs/c_attr_b1/out/at_aya_vision_8b_ov_dev_b-zs-b1.preds.json
d039b247360d23125e45f2e8f0361f25ccb678026055ac141e1ac95471c1c354  .session_backup/machines/ATTR_H1/root/outputs/c_attr_b1/out/at_aya_vision_8b_xm_dev500-rand-k4--T1-d0-mvi-b1.preds.json
0f105532737b426a42edb52a8cc165a45fb35cbff26146d7fee81da6c462f074  .session_backup/machines/ATTR_H1/root/outputs/c_attr_b1/out/at_aya_vision_8b_xm_dev500-rand-k4--T1-d1-mvi-b1.preds.json
3f70c33eed306c514f9032637d7076d056d506ad92cce85a55af22ce6d51d879  .session_backup/machines/ATTR_H1/root/outputs/c_attr_b1/out/at_aya_vision_8b_xm_dev500-rand-k4--T1-d2-mvi-b1.preds.json
a6b913a53b063d59f26e462e4c400d0cf6b493b4ce121137d93ef70896a588bd  .session_backup/machines/ATTR_H1/root/outputs/c_attr_b1/out/at_aya_vision_8b_xm_dev500-ret-k4-last-T1-mvi-b1.preds.json
f26f0a9afa32b2825af1a793f2f48433aca2d434cd32cf3dbb08d663ce4ebd66  .session_backup/machines/ATTR_H1/root/outputs/c_attr_b1/out/at_aya_vision_8b_xm_dev500-zs-b1.preds.json
ea4c8843bfb0eeea0d0f99416090dbb23e802cee17c5b161e8d1ddf968762109  .session_backup/machines/ATTR_H1/root/outputs/c_attr_b1/out/at_internvl3_8b_ov_dev_b-rand-k4--T2-d0-mvi-b1.preds.json
11574e77a0754760aebe1598058d3832ca599453d12e55e2a1ef215e90316bb1  .session_backup/machines/ATTR_H1/root/outputs/c_attr_b1/out/at_internvl3_8b_ov_dev_b-rand-k4--T2-d1-mvi-b1.preds.json
3042e7d819ad7807047245ed66b81f9872c554f369b6e7191e796c2d4c1749a2  .session_backup/machines/ATTR_H1/root/outputs/c_attr_b1/out/at_internvl3_8b_ov_dev_b-rand-k4--T2-d2-mvi-b1.preds.json
b1351e111fd8924b273e6e42ca0399b0dad3321ae87a6b5d229ff2bca151131f  .session_backup/machines/ATTR_H1/root/outputs/c_attr_b1/out/at_internvl3_8b_ov_dev_b-ret-k4-last-T2-mvi-b1.preds.json
1802a3df629d4eee135e8af8205a4246bd84ed438cbb7c81d32d5c5ee6a2f790  .session_backup/machines/ATTR_H1/root/outputs/c_attr_b1/out/at_internvl3_8b_ov_dev_b-zs-b1.preds.json
c4065cf881f32e6ab2f5dd9a098f612b42a33b6108e0fb9695365cf00822edea  .session_backup/machines/ATTR_H1/root/outputs/c_attr_b1/out/at_internvl3_8b_xm_dev500-rand-k4--T2-d0-mvi-b1.preds.json
2814ceaaf2789cb05973105502eea78d4ba5afdaf0daf916556e3897ceaa1dbd  .session_backup/machines/ATTR_H1/root/outputs/c_attr_b1/out/at_internvl3_8b_xm_dev500-rand-k4--T2-d1-mvi-b1.preds.json
817f470adf0f1240cf908cdea99558af942aa0088bbaf8ed6191d046137ece29  .session_backup/machines/ATTR_H1/root/outputs/c_attr_b1/out/at_internvl3_8b_xm_dev500-rand-k4--T2-d2-mvi-b1.preds.json
cbb6ba9ddb28c25ac8987bfb316b381bf111a77b98d725874d630fc1f8cb466a  .session_backup/machines/ATTR_H1/root/outputs/c_attr_b1/out/at_internvl3_8b_xm_dev500-ret-k4-last-T2-mvi-b1.preds.json
5aa4e78bcba4704d035f38bfe3c5cb21572eb60edd8ce5e4bce08f1983c8fe86  .session_backup/machines/ATTR_H1/root/outputs/c_attr_b1/out/at_internvl3_8b_xm_dev500-zs-b1.preds.json
75f076e75da3e04649329770bf05cf700e705a330af9f2dcb5bb5712363ed4f0  .session_backup/machines/ATTR_H1/root/outputs/c_attr_b1/out/at_qwen25vl_7b_ov_dev_b-rand-k8--T1-d0-mvi-b1.preds.json
367afdfcaa981a6670b2039021e8eb88947591911ee6f1415d88439341d6b3b0  .session_backup/machines/ATTR_H1/root/outputs/c_attr_b1/out/at_qwen25vl_7b_ov_dev_b-rand-k8--T1-d1-mvi-b1.preds.json
70b626e3ae65cedc16bbe5045c6ced0908665f156d80a3ebecdd3c30b8a33ed2  .session_backup/machines/ATTR_H1/root/outputs/c_attr_b1/out/at_qwen25vl_7b_ov_dev_b-rand-k8--T1-d2-mvi-b1.preds.json
f7298a01b94044eb9d416b34cbd9986fd34b350350543bce295ead7677f2829f  .session_backup/machines/ATTR_H1/root/outputs/c_attr_b1/out/at_qwen25vl_7b_ov_dev_b-ret-k8-first-T1-mvi-b1.preds.json
c71290437e5bc102561aee80232134980aac00a9f30d7a77429113d0daed179a  .session_backup/machines/ATTR_H1/root/outputs/c_attr_b1/out/at_qwen25vl_7b_ov_dev_b-zs-b1.preds.json
77b1e648e091d850e24e9f70a43354a9e3086cfd57886a749ef4d56d5936d8d0  .session_backup/machines/ATTR_H1/root/outputs/c_attr_b1/out/at_qwen25vl_7b_xm_dev500-rand-k8--T1-d0-mvi-b1.preds.json
24c394e0517869c6367104390e78c639973ee3d547a0f30d2d29ff1954a34c1f  .session_backup/machines/ATTR_H1/root/outputs/c_attr_b1/out/at_qwen25vl_7b_xm_dev500-rand-k8--T1-d1-mvi-b1.preds.json
b407070e347c7af6e841872be2a34385162851792774bcf739057737df839686  .session_backup/machines/ATTR_H1/root/outputs/c_attr_b1/out/at_qwen25vl_7b_xm_dev500-rand-k8--T1-d2-mvi-b1.preds.json
4d7c3e447700df75e4b136ac84cc9876981a6725d18937e20bbfbd6ce2e40d48  .session_backup/machines/ATTR_H1/root/outputs/c_attr_b1/out/at_qwen25vl_7b_xm_dev500-ret-k8-first-T1-mvi-b1.preds.json
1ef622876075351b3f44be1970b4bce4c1c2e341a7ba703de23f73ef40d5c234  .session_backup/machines/ATTR_H1/root/outputs/c_attr_b1/out/at_qwen25vl_7b_xm_dev500-zs-b1.preds.json
8a2b977f9caf37f40bcc2a1b43e5b0c362b99d875ef28bc9640cccf2f9487cd5  scripts/c_attr/c_attr_lists.json
072b17d14d89aa21110794be27168cf4ef4212a569a4d55d54c5acf1de7e5a41  .session_backup/machines/M3/root/outputs/c_stage2/ex_ov_dev_b.json
9a79b97dddd573b6092410f33dc2b069213a4407bb029102e05979811f66a17a  .session_backup/machines/M3/root/outputs/c_stage2/ex_xm_dev500.json
991d289bb43b1bcb935e3717aede594147ba533da723501ae473f9af87f43a5b  .session_backup/machines/M3/root/outputs/c_stage2/runs/c2_internvl3_8b_ov_dev_b-rand-k4-T2.preds.json
b05d9163aa9a85356d23d9ff50612750c1bbbf8022fed6caf9cb0476c35002fb  .session_backup/machines/M3/root/outputs/c_stage2/runs/c2_internvl3_8b_ov_dev_b-ret-k4-last-T2.preds.json
745c3bd736db2a1bae491d57a8bb2047bd183e7c249bdfb0dc24b649fb0fcb7f  .session_backup/machines/M3/root/outputs/c_stage2/runs/c2_internvl3_8b_ov_dev_b-zs.preds.json
6adc1afacf148424fb88fecffd2a6aed53fc4d6fe7c26c4529802f0da98c6e35  .session_backup/machines/M3/root/outputs/c_stage2/runs/c2_internvl3_8b_xm_dev500-rand-k4-T2.preds.json
c1bd25430fb82d16e859345aaed90609fc23c4c4aee137f5b52d7001b27fecf7  .session_backup/machines/M3/root/outputs/c_stage2/runs/c2_internvl3_8b_xm_dev500-ret-k4-last-T2.preds.json
f79d1b7f63007ecfcb98dc4bd30981e3a42573f24d94fada7689adae369bce1f  .session_backup/machines/M3/root/outputs/c_stage2/runs/c2_internvl3_8b_xm_dev500-zs.preds.json
53ce8591417cbffe2d6d9368eb5bfd46b123ce695d8cdd6e936faadf7b7118a1  .session_backup/machines/M3/root/outputs/c_stage2/runs/c2_qwen25vl_7b_ov_dev_b-rand-k8-T1.preds.json
9fa11f7bc552be6310f8ffa9526bcc375352ced54b45ef2cb8085ec87902c03a  .session_backup/machines/M3/root/outputs/c_stage2/runs/c2_qwen25vl_7b_ov_dev_b-ret-k8-first-T1.preds.json
5bf37a77d9883f91441956a01042a69861d94d46a9daec3d479eb7f1ab7e3fc3  .session_backup/machines/M3/root/outputs/c_stage2/runs/c2_qwen25vl_7b_ov_dev_b-zs.preds.json
5526773956a3cca00b05ad5960c54e0fc6be042e92affa1c0ef0a2aed50e1ea2  .session_backup/machines/M3/root/outputs/c_stage2/runs/c2_qwen25vl_7b_xm_dev500-rand-k8-T1.preds.json
5bb77bd21d9e361a851dc3037cdd9a28f9983db695875401bb942ba1aba8c100  .session_backup/machines/M3/root/outputs/c_stage2/runs/c2_qwen25vl_7b_xm_dev500-ret-k8-first-T1.preds.json
d11b8f8a4da135b591d126814d72594315ec24ce9be2da42c9115210a9f591de  .session_backup/machines/M3/root/outputs/c_stage2/runs/c2_qwen25vl_7b_xm_dev500-zs.preds.json
d798792be402e8f6377b19740cecba861ba87e94f07156df8ce3acc1c26c2ae0  .session_backup/machines/M1/root/outputs/c_t1/out/t1_aya_vision_8b_f30k_carve-rand-k4--T1-d0-mcoco.preds.json
f557a9cfb5c7edfe15fceb50b184398cb40e9deb6799e18f7801ebf86ac19f99  .session_backup/machines/M1/root/outputs/c_t1/out/t1_aya_vision_8b_f30k_carve-ret-k4-last-T1-mcoco.preds.json
7d3725e912da14124032ce871d513c744c0b237cc3f03d380fe584e7c2294e5f  .session_backup/machines/M1/root/outputs/c_t1/out/t1_aya_vision_8b_f30k_carve-zs.preds.json
469b271e4e3d1ba0d05ea956d6b5dbfaa8c90843f9d8f3d2ec14b1001b9d03f0  .session_backup/machines/M1/root/outputs/c_t1/out/t1_internvl3_8b_f30k_carve-rand-k4--T2-d0-mcoco.preds.json
830cde02df820cb849e3b36b2451627d8a4e27247f8da29f57ca7af9cf60fda4  .session_backup/machines/M1/root/outputs/c_t1/out/t1_internvl3_8b_f30k_carve-ret-k4-last-T2-mcoco.preds.json
c9d6042edd8b6172455e7cc59bf60761c1b913a6534ade802be26a86fde9ea0d  .session_backup/machines/M1/root/outputs/c_t1/out/t1_internvl3_8b_f30k_carve-zs.preds.json
36721db79e5c845c9529a36b298a23782596fbccafb3d2329cba06f4a15fcf6b  .session_backup/machines/M1/root/outputs/c_t1/out/t1_qwen25vl_7b_f30k_carve-rand-k8--T1-d0-mcoco.preds.json
cc4fd3ef632b70d617ace695c2080b939d7ecb40def1e760f198e9dfc2208422  .session_backup/machines/M1/root/outputs/c_t1/out/t1_qwen25vl_7b_f30k_carve-ret-k8-first-T1-mcoco.preds.json
7b0b115d6c2ceec44fad94f89e3d52b83913177ca471d7e101043be29667dd15  .session_backup/machines/M1/root/outputs/c_t1/out/t1_qwen25vl_7b_f30k_carve-zs.preds.json
```

Code, lists, gold and loaders:

```
d11db7e192f689980bb2b2bb717d852d9aa339ad857ce9411fe7bdd6fe416070  (paper repo) scripts/score_coco_probe.py
c0d9dd30e3222ab6542a7e1acfbb9bd3899e4b6db5c896b0adc4d805c1005a8b  (paper repo) scripts/match_openviic.py
a3bd7b93bdcc85cc6ce34a0676796cafd4e23497f3deae17b3f6ff60f2e31dc0  scripts/c_attr/c_attr.py
cca5e3270a4699672b06f1580d08af265dc55b447cd3b241233d6ec8611d99c0  scripts/c_attr/c_attr_score.py
9a79403f4fc38609282d40082ab7f878133edca8aff9e0dc2462db467b7193f0  scripts/xm3600_oiv7.py
0f99e36e96c86685c212f34cde318d155b5fe1400bcbbd4db18eddfc89d159e9  scripts/c_stage2/score2.py
eebcd95b78b1dc98398550b1f89fea5622e8cbd9f20ad6b07b0d9292ba745968  manuscript/prereg/2026-10-30_c_t1/c_t1_f30k_lists.json
5c479f03e8be544f4cd12b5d997b5dc92b6c622df061760cd02f6ba82f6b4371  manuscript/prereg/2026-10-22_c_stage1/lists.json
99d4fc49cc8283d1555d37b975cca5a32598ea0ec571d8bef8cf811df2c33695  manuscript/prereg/2026-10-25_c_test/ov_test_files.tsv   (ids + sha256 only; W3 check)
8e11bad51c77adc54c05b91a86f7b6f5a1f2d0e9032f06faf80f05e438d42850  manuscript/prereg/2026-11-18_c_conf/c_conf_carve_order.json   (ids only; W3 check)
550cfe06b06084976e81286531f7f4e52bea717e29004c699ccaf1e48919bdff  .session_backup/2026-10-22/c_stage2/subsets/uit-openviic-annotation-dev.json   (the stage-2 subset of record, 1,085,184 B; CC-362, OPS-1112bc), pushed unchanged to `ncs-data/datasets/openviic/` on the host
0da82355b65ab284fe55fc0d3c4101090301767347a02721890556618ca4905f  datasets/c_xm_dev500/xm_dev500_data.json   (host data folder; pin c_attr_score.py l.86)
395990db603ab8bafd5c7ab2746b22058bb1e75b78b3eb56ad755931364ac137  Flickr30K CSV nlphuji/flickr30k @2b239bef   (pin c_attr.py l.81)
bac3953a511a9793c22e928a29b68ae05dbf9654502abcbe7b64fd9f6d74c8b2  data/xm3600/oiv7_labels.json   (public OIV7 human-verified labels; not Paper A XM600 gold)
84a4373a0efb7fd6d93fe19b0e7ceb6c1b855c233d13b9b78a9a33655c9fdce3  data/datasets/xm3600/oiv7/oidv7-class-descriptions.csv
27f2b1ca3f2bf47d43c8f00e8409472c8d571eb720d47b8107a1c77bd208d16a  data/xm3600/vi_oiv7_map.json
263015f9dc46ebe2cea80055e04ed39baf80a356f4e027cd3756464279135bef  data/xm3600/manifest.json   (provenance, read at the code read)
9e2811cdbc2ddfc71d04be5dc36e185c88dcd1ad4d5d69e4ff2e1369dccf7793  VnCoreNLP-1.2.jar   (pin REG2 l.275; score2.py l.153)
```

**Not used:** the laptop file `data/datasets/openviic/uit-openviic-annotation-dev.json` has sha256 `2a68a3eb4d41926deb524aa8f98c80f112472474906d73d9763c790fb0cac847`, which is **not** the pin `550cfe06…`. It is never pushed or used (OQ-11).

### 2.2 HASH-ONLY LIST (never pushed, never opened)

```
a74ff8b9a909564b4a3cf4387535ac71220a84e42600a0296b6939ce44c15c85  .session_backup/machines/ATTR_H1/root/outputs/c_attr_b1/out/at_aya_vision_8b_ov_dev_b-perm-k4-last-T1-p1-mvi-b1.preds.json
acba64b1961f04ef68de5ac91987e83cd6d83756e70055a4e48961a75ad2b0d0  .session_backup/machines/ATTR_H1/root/outputs/c_attr_b1/out/at_aya_vision_8b_ov_dev_b-perm-k4-last-T1-p2-mvi-b1.preds.json
ddc71af2cb39ef25eed35336593535de1eb4a670f4cdc6673a1d36f46daebdb1  .session_backup/machines/ATTR_H1/root/outputs/c_attr_b1/out/at_aya_vision_8b_xm_dev500-perm-k4-last-T1-p1-mvi-b1.preds.json
bcd4ae6789c73321332905fe1995a70727c21fc8d23807fd8a21559b9346255b  .session_backup/machines/ATTR_H1/root/outputs/c_attr_b1/out/at_aya_vision_8b_xm_dev500-perm-k4-last-T1-p2-mvi-b1.preds.json
6988f53290bc581a6f4d6b54b6b539c0d8e76594f21e6d6d7a6a4ba284b03f57  .session_backup/machines/ATTR_H1/root/outputs/c_attr_b1/out/at_internvl3_8b_ov_dev_b-perm-k4-last-T2-p1-mvi-b1.preds.json
c8a99f20953293a1b2352c3e3ebc4c241b309d957ecfbc843976cc74f70b6476  .session_backup/machines/ATTR_H1/root/outputs/c_attr_b1/out/at_internvl3_8b_ov_dev_b-perm-k4-last-T2-p2-mvi-b1.preds.json
77bcad05d13501cb2b9e8218bef1e6baad55a846a1b938b6ecbface1f4b0eb23  .session_backup/machines/ATTR_H1/root/outputs/c_attr_b1/out/at_internvl3_8b_xm_dev500-perm-k4-last-T2-p1-mvi-b1.preds.json
42e5a885a24343ef3804d905c62e35a6a6099cfdd121770da4fe022e0dd88470  .session_backup/machines/ATTR_H1/root/outputs/c_attr_b1/out/at_internvl3_8b_xm_dev500-perm-k4-last-T2-p2-mvi-b1.preds.json
a3c634a1757d1185f1a21dd8c576bd77c1fb179d7b6a889ee54540df590ad022  .session_backup/machines/ATTR_H1/root/outputs/c_attr_b1/out/at_qwen25vl_7b_ov_dev_b-perm-k8-first-T1-p1-mvi-b1.preds.json
daaa7b49a7541dcddad55c38da35f6d69cd54ad7c4d31c5ba62bc9272c02174c  .session_backup/machines/ATTR_H1/root/outputs/c_attr_b1/out/at_qwen25vl_7b_ov_dev_b-perm-k8-first-T1-p2-mvi-b1.preds.json
fff51b3bb2d0cd59f824a24f60c5dfe537c3021ee857e110f5c2b550e594c29a  .session_backup/machines/ATTR_H1/root/outputs/c_attr_b1/out/at_qwen25vl_7b_xm_dev500-perm-k8-first-T1-p1-mvi-b1.preds.json
7b9e125e180299fcb4da452c719dfcd6687a1a0cd8f80b03a5922583eb0d42f8  .session_backup/machines/ATTR_H1/root/outputs/c_attr_b1/out/at_qwen25vl_7b_xm_dev500-perm-k8-first-T1-p2-mvi-b1.preds.json
6454200db8472ec7f730768ec42126d8b23370e2f297eaec37fc617996a7ae6f  .session_backup/machines/M1/root/outputs/c_t2/out/t2_aya_vision_8b_f30k_val-rand-k4--T1-d0-mcoco.preds.json
002b3d0bf7fb00377ca98a10ab972263b1c577239b8255fa6e3fd376f403480c  .session_backup/machines/M1/root/outputs/c_t2/out/t2_aya_vision_8b_f30k_val-ret-k4-last-T1-mcoco.preds.json
d4a4f79314fb316b419737bf2384ab98b834bef209e59129248b66b1fa8b9167  .session_backup/machines/M1/root/outputs/c_t2/out/t2_aya_vision_8b_f30k_val-zs.preds.json
4f01bb952b4a8f03c8c980c8d690a940957aa2e743a536cb7dbe4c7ec98d176b  .session_backup/machines/M1/root/outputs/c_t2/out/t2_internvl3_8b_f30k_val-ret-k4-last-T2-mcoco.preds.json
82e9ded1774cb79ecab5d9aaaac9df48d7d4abc39c5ae5810187b47629b9cbc9  .session_backup/machines/M1/root/outputs/c_t2/out/t2_internvl3_8b_f30k_val-zs.preds.json
4f718184bc82c2222329830c5330239615af8c7ba65d64c648e612e31829ee6e  .session_backup/machines/M1/root/outputs/c_t2/out/t2_qwen25vl_7b_f30k_val-rand-k8--T1-d0-mcoco.preds.json
2a51bed293620474a44006d857d92c82203530882c53681f396a0b582f45aa83  .session_backup/machines/M1/root/outputs/c_t2/out/t2_qwen25vl_7b_f30k_val-ret-k8-first-T1-mcoco.preds.json
2fe6a1c28dc5dd4a5ac88dcecb22e1481236cc6b9ac570bb22b8f124b265dc37  .session_backup/machines/M1/root/outputs/c_t2/out/t2_qwen25vl_7b_f30k_val-zs.preds.json
f79ea6a9c59157216fdf1662ce320c35a1befe48a87cfb36a174a7cfef0244f8  .session_backup/machines/ATTR_H1/root/c_attr_score/led/ovb.jsonl
f8e375a3866bbb94b3739889bba3890b02452b6b08bafe782fbcfd455a3ceb81  .session_backup/machines/ATTR_H1/root/c_attr_score/led/xm_b1.jsonl
324550c3b86a8632d02b3a59394b622336bfb72df965bfff4121fb49526c3895  .session_backup/machines/ATTR_H1/root/c_attr_score/led/ova.jsonl
ca6754718587a13448b705883de7e60cc1c6641b6b6107fa713b6a356521d312  .session_backup/machines/ATTR_H1/root/c_attr_score/led/bat_ov_dev_b.jsonl
00310e595cbbd5d7f5b6b11ef6fff8deb86e7d7f0f1623ac220f5086bd39cf49  .session_backup/machines/ATTR_H1/root/c_attr_score/led/bat_xm_dev500.jsonl
```

## 3. Never opened, never pushed

- OV-test images, captions and outputs (`ledger_ov_test_*`, `c_test/**`). Only the id/sha list `ov_test_files.tsv` is used, for the W3 check.
- KTVIC test.
- XM-test2500 (`ledger_xm_test*`). Only its ids in `lists.json` are used, for the W3 check.
- `c_en/**`, which holds COCO test and NoCaps val.
- Flickr30K test (`c_t3/**`).
- **Flickr30K val (`c_t2/**`, the rehearsal used once)** [W1].
- `.session_backup/machines/CONF_H1/**` (C-CONF registration 2 is pending; the carve and confirm halves are untouched). Only the id list `c_conf_carve_order.json` is used, for the W3 check.
- Every C-RAA output.
- The C-ATTR per-image ledgers (`c_attr_score/led/*`) [N1].

The push list is the explicit PUSH LIST of §2. Files of the HASH-ONLY LIST are never pushed or opened. There is no directory push. [W1]

## 4. Steps and stops

| step | action | stop if |
|---|---|---|
| 0 | judge round-2 GO on the prereg, then commit (gatekeeper) | – |
| 1 | write `c_n3d.py`, `test_c_n3d.py` and the planted-cell toy set (flags, precedence, placebo difference, Holm with a NOT DECIDABLE row at p̃ = 1, the exact rng call); judge code read | the code opens an input before the read |
| 2 | rent a host that meets the §1 host rule [W2]; push the PUSH LIST; check sha256 per file | any mismatch |
| 2a [W3] | before any decode file is opened, the four lines of prereg §10 step 2a: - intersect the image ids and the image sha256 values of OV-dev-B (925) and XM-dev500 (500), the sha256 being the third field of each entry of `lists.json` `sets.ov_dev_b` and `sets.xm_dev500`, with the names and sha256 values of `ov_test_files.tsv` (`99d4fc49cc8283d1555d37b975cca5a32598ea0ec571d8bef8cf811df2c33695`) and with the ids of `c_conf_carve_order.json` (`8e11bad51c77adc54c05b91a86f7b6f5a1f2d0e9032f06faf80f05e438d42850`); - intersect the XM-dev500 ids with the XM-test2500 ids of `lists.json` (`5c479f03…`); - intersect the 1,000 carve ids of `c_t1_f30k_lists.json` (`eebcd95b…`) with its `refuse.val` (1,014) and `refuse.test` (1,000) ids; - no image file is pushed or read for this check. Print counts only | **any count above 0** |
| 3 | self-tests and mutants on the host | any test fails, or any mutant survives |
| 4 | one run, in the section 10 order of the prereg | the 4.0 CPU-h cap |
| 5 | pull the decision file, sha256 it, write the LOG line, delete per-image intermediates on the host, then clean the host files | – |
