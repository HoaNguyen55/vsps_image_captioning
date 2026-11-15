"""step1.py WORKDIR -> step1.json: the title decisions (read on 2026-11-15) applied to merged.json; prints counts and a condensed view of the abstracts that go to step 2."""
import json, re, sys, os
W = sys.argv[1]
ws = json.load(open(os.path.join(W, "merged.json"), encoding="utf-8"))
E1 = """2 4 5 7 8 10 11 14 18 22 26 27 40 44 47 48 49 51 52 53 56 61 63 65 70 71 75 77 83 84 86 94 97 100 102 104 111 115 119 120 122 123 130 137 138 154 155 158 159 162
164 165 170 176 179 181 184 187 192 200 205 206 207 208 210 211 212 213 215 217 219 222 224 227 228 230 231 232 236 239 243 246 251 254 255 257 258 259 260 270 271 302 304 306 307
311 314 315 316 322 323 326 338 339 343 344 346 349 357 360 363 364 365 376
32 36 46 62 66 74 96 106 118 128 167 177 180 182 185 190 193 202 226 234 237 253 256 264 273 284 297 318 320 324 331 341 345 351 355 356 373""".split()
E4 = "3 13 15 16 17 28 29 54 73 79 127 135 149 156 178 285 299 362 81 229 321 371".split()
E5 = {"1": 175, "59": 58, "337": 336}          # same work under two records
NOTWORK = ["129"]                                # "Front Matter"
RESCUE = "468 549 470 513 429 440 480 551 474 462 446 417 401 434 565".split()   # no abstract, title read (deviation D2)
E5.update({"543": 333, "569": 369, "491": 209, "524": 278, "430": 87, "497": 221, "498": 221, "550": 347})
dec = {}
for w in ws:
    n = str(w["n"])
    if n in E5: d = "E5 duplicate of %d" % E5[n]
    elif n in NOTWORK: d = "not a research paper"
    elif not w["pass1a"] and n not in RESCUE: d = "1a script"
    elif n in E1: d = "E1 by title"
    elif n in E4: d = "E4 by title"
    else: d = "to step 2"
    dec[n] = d
import collections
c = collections.Counter(d.split(" duplicate")[0] for d in dec.values())
print(dict(c))
for w in ws: w["step1"] = dec[str(w["n"])]
json.dump(ws, open(os.path.join(W, "step1.json"), "w", encoding="utf-8"), ensure_ascii=False, indent=0)
