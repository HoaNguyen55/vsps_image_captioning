"""step2.py WORKDIR BIB -> step2.json: abstract-screen decisions (read on 2026-11-15) applied to step1.json; prints counts."""
import json, re, sys, os, collections
W, BIB = sys.argv[1:3]
ws = json.load(open(os.path.join(W, "step1.json"), encoding="utf-8"))
bib = open(BIB, encoding="utf-8").read()
norm = lambda t: re.sub(r"[^a-z0-9]+", "", t.lower())
known = {}
for key, body in re.findall(r"@\w+\{([^,]+),(.*?)\n\}", bib, flags=re.S):
    m = re.search(r"\btitle\s*=\s*\{(.*)\}", body)
    if m: known[norm(re.sub(r"[{}]", "", m.group(1)))[:60]] = key
ids = lambda s: [int(x) for x in s.split()]
D = {}
for n in ids("38 268 133 366 369 372 186 21 319 109 41 147"): D[n] = "P-A"
for n in ids("350 262 549 95 240 87 282 275"): D[n] = "P-B"
for n in ids("216 249 248"): D[n] = "P-C"
D.update({468: "E5 duplicate of 186", 241: "E5 duplicate of 249", 312: "E5 duplicate of 305", 161: "E7 not in English"})
for n in ids("""31 39 43 57 60 69 72 82 85 90 91 99 101 103 107 114 126 136 145 148 166 169 173 189 195 196 238 252 263 267 276 281 283 287 288 290 291 292 293 294 295 296 298 303 308 309 310
325 327 328 330 336 358 23 146 188 198 204 250 332 333 64 266 277 68 140 247 429 440"""): D[n] = "E3 X-M trained or tuned method, no analysis of example selection"
for n in ids("33 34 42 55 113 125 143 175 220 272 278 367 446 480 551"): D[n] = "X-K retrieves knowledge or articles, not captioning examples; no analysis of example selection"
for n in ids("6 50 110 245 329 353 142 305 45 76 35 225 313 279 117 274 197 474 462 121 67"): D[n] = "E1 other task"
for n in ids("""12 20 24 25 30 37 78 80 88 89 92 93 98 105 108 124 131 132 134 141 144 150 151 152 153 157 160 163 168 171 172 174 183 194 201 203 209 214 218 221 233 242 244 261 280 300 301 317
334 342 354 359 361 368 374 375 417 434 470 513 565"""): D[n] = "E2 no examples or retrieved material at inference"
out = collections.Counter()
for w in ws:
    if w["step1"] != "to step 2": w["step2"] = ""; continue
    k = known.get(norm(w["title"])[:60])
    w["step2"] = ("known: " + k) if k else D.get(w["n"], "UNDECIDED")
    out[w["step2"].split(":")[0].split(" duplicate")[0] if not w["step2"].startswith(("E", "X")) else w["step2"].split(" ")[0]] += 1
print(dict(out)); print("undecided:", [w["n"] for w in ws if w.get("step2") == "UNDECIDED"])
json.dump(ws, open(os.path.join(W, "step2.json"), "w", encoding="utf-8"), ensure_ascii=False, indent=0)
for w in ws:
    if w.get("step2", "").startswith("P-"): print(w["step2"], w["n"], w["date"][:7], w["arxiv"] or w["doi"] or "-", "|", w["venue"][:28], "|", w["title"][:75], "|", ",".join(w["found"]))
