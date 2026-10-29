"""List numeric tokens in the given md text that are not a `number` in number_manifest_C.tsv (manual review list)."""
import re, sys
from pathlib import Path
MAN = Path("/mnt/d/vsps_image_captioning/manuscript/journal_draft_C/number_manifest_C.tsv")
have = {l.split("\t")[0] for l in MAN.read_text().splitlines()[1:]}
have |= {h.rstrip("0").rstrip(".") for h in have if "." in h}
miss = {}
for p in sys.argv[1:]:
    text = Path(p).read_text()
    text = re.sub(r"`[^`]*`", " ", text)  # code spans (run ids, hashes)
    for m in re.finditer(r"(?<![\w.])[+−-]?\d[\d,]*(?:\.\d+)?", text):
        tok = m.group(0).replace("−", "-").replace("+", "").replace(",", "")
        if any(t in have or t.rstrip("0").rstrip(".") in have for t in (tok, tok.lstrip("-"))): continue
        miss.setdefault(tok, set()).add(Path(p).name)
for k in sorted(miss, key=lambda x: float(x)): print(k, sorted(miss[k]))
