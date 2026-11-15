import json, re, sys
card, paper = sys.argv[1], sys.argv[2]
t = open(card, encoding='utf-8').read(); t = t[t.index('## Paper card'):]
p, d = t[:t.index('## Direction card')], t[t.index('## Direction card'):]
ref = open('cards/R2.md', encoding='utf-8').read()
heads = lambda s: re.findall(r'^\*\*[^.(]*', s, re.M)
j = json.loads(d[d.index('```json') + 7:d.rindex('```')])
txt = open(paper, encoding='utf-8').read()
nums = set(re.findall(r'\d[\d,]*\.\d+|\d{1,3}(?:,\d{3})+|\d{3,}', t))
bad = {
 'a words 564-630': not 564 <= len(p.split()) <= 630,
 'b backtick outside the json fence': t.count('`') != 6,
 'c closest_work 5 or 6': not 5 <= len(j['closest_work']) <= 6,
 'd 14 headings as R2': heads(p) != heads(ref[:ref.index('## Direction card')]),
 'e keys and fixed values': list(j) != ['id','title','gap','novelty_claim','application','data','method','kill_pilot','target_year','venue','closest_work'] or (j['target_year'], j['venue']) != (2027, 'international conference'),
 'f number not in the paper text': sorted(n for n in nums if n not in txt),
 'g label token': bool(re.search(r'\bR[1-5]\b|PROVISIONAL|\bX[1-6]\b', t.replace('"id": "OURS"', ''))) or t.count('OURS') != 1,
}
for k, v in bad.items(): print('FAIL' if v else 'ok  ', k, v if isinstance(v, list) and v else '')
print('CARD OK' if not any(bad.values()) else 'CARD NOT OK', len(p.split()), 'words')
