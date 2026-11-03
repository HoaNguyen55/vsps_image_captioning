"""C v3 id check (CC-214r2 B1/B2/B3). Ids only; caption fields are never read, printed or written."""
import json, sys
R = sys.argv[1]
P = f"{R}/manuscript/prereg"
def txt(p): return {int(x) for x in open(p).read().split() if x.strip().isdigit()}
def tsv(p): return {int(l.split("\t")[0]) for l in open(p) if l[0] != "#"}
def uit(split): return {im["id"] for im in json.load(open(f"{R}/data/datasets/uitviic/{split}_data.json"))["images"]}
kar = json.load(open(f"{R}/data/datasets/karpathy/dataset_coco.json"))["images"]
split = {}
for im in kar: split.setdefault(im["split"], set()).add(im["cocoid"])
KT = tsv(f"{P}/2026-10-27_c_en/cen_coco_test.tsv")
MEM = tsv(f"{P}/2026-10-27_c_en/cen_memory_allowed.tsv")
assert KT == split["test"], "cen_coco_test != Karpathy test"
lists = {
 "karpathy_val_5000 (kv5000.txt, superset of KV-4,224)": txt(f"{P}/2026-10-27_grl_pilot/kv5000.txt"),
 "cen_coco_kval.tsv": tsv(f"{P}/2026-10-27_c_en/cen_coco_kval.tsv"),
 "MT4 T2-2000 (t2_ids.txt)": txt(f"{P}/2026-10-30_mt4_k1k6/t2_ids.txt"),
 "Karpathy restval (B4)": split["restval"],
 "UIT-ViIC train 2,695": uit("train"), "UIT-ViIC val 924": uit("val"), "UIT-ViIC test 231": uit("test"),
 "VSPS-J M0 dev_touched 3,454": txt(f"{P}/2026-10-31_vsps_j_m0/dev_touched_ids.txt"),
 "VSPS-J M0 karpathy_test 91": txt(f"{P}/2026-10-31_vsps_j_m0/karpathy_test_val_ids.txt"),
 "A-T3 val2017 5,000 (not reserved)": txt(f"{P}/2026-10-30_a_t3/val2017_ids.txt"),
}
ex = json.load(open(f"{P}/2026-10-21_dev_pools/exclusion.json"))["ids"]["coco"]
for k, v in ex.items(): lists[f"exclusion.json ids/coco/{k} (spent dev pool, count only)"] = set(v)
lists["UT-2,402 (ut2402.txt, MT4/K2)"] = txt(f"{P}/2026-10-27_grl_pilot/ut2402.txt")
print("KT", len(KT), "MEM", len(MEM), "KT&MEM", len(KT & MEM))
for k, s_ in lists.items(): print(f"{k:62s} n={len(s_):6d}  &KT={len(KT & s_):5d}  &MEM={len(MEM & s_):6d}")
held = lists["karpathy_val_5000 (kv5000.txt, superset of KV-4,224)"] | lists["cen_coco_kval.tsv"] | lists["MT4 T2-2000 (t2_ids.txt)"]
assert not (KT & held), "Karpathy test touches KV/T2"
OWN = [k for k in lists if not k.startswith("exclusion")]  # B_DIRECTION_v3 5.3 owner list, COCO id space
owners = set().union(*(lists[k] for k in OWN))
dkt, dmem = KT & owners, MEM & owners
print("owner lists:", OWN)
print(f"C COCO dev KT-C = {len(KT)} - {len(dkt)} = {len(KT - dkt)}")
print(f"D-EN = {len(MEM)} - {len(dmem)} = {len(MEM - dmem)}")
