"""cells.py TXT [CATS] -> term counts and short evidence sentences (with page) for the Table 1 / 1b cells of one full text."""
import re, sys
txt = open(sys.argv[1], encoding="utf-8", errors="replace").read()
cats = sys.argv[2].split(",") if len(sys.argv) > 2 else None
pages = [re.sub(r"\s+", " ", re.sub(r"-\n\s*", "", p)) for p in txt.split("\f")]
flat = " ".join(pages)
C = [("preregist", r"pre-?regist"), ("registered", r"\bregistered\b"), ("conf.int", r"confidence intervals?"), ("bootstrap", r"bootstrap(?!ping)"),
     ("std", r"standard deviations?|\bstd\b"), ("±", "±"), ("seed", r"\bseeds?\b"), ("p-value", r"p-?values?|\bp ?[<=] ?0?\.\d"), ("error bar", r"error bars?"),
     ("signif.test", r"significance test|t-test|wilcoxon|statistically significant"), ("Vietnam", r"vietnam"), ("random", r"random")]
print(" ".join("%s=%d" % (n, len(re.findall(p, flat, re.I))) for n, p in C), "| pages", len(pages) - 1)
E = {"random": r"random(ly)?[^.]{0,80}(example|demonstration|shot|retriev|caption|select|sampl)|(example|demonstration|shot|retriev)[^.]{0,60}random",
     "viet": r"vietnam|\bvi\b", "ci": r"confidence interval|bootstrap(?!ping)|error bar", "sd": r"standard deviation|±|seeds\b|averaged over|times and report",
     "train": r"training-free|without (any )?(additional )?(training|fine-?tuning)|we (fine-?tune|train)\b|is trained|frozen",
     "data": r"(COCO|Flickr|NoCaps|XM3600|caption(ing)? (dataset|benchmark|task))[^.]{0,120}", "lang": r"\b\d+ languages|multilingual|English|low-resource"}
for name, pat in E.items():
    if cats and name not in cats: continue
    n = 0
    for i, p in enumerate(pages, 1):
        for s in re.split(r"(?<=[.!?])\s+", p):
            if re.search(pat, s, re.I) and 6 <= len(s.split()) <= 60:
                print("  [%s p.%d] %s" % (name, i, " ".join(s.split()[:34]))); n += 1
                if n >= 2: break
        if n >= 2: break
