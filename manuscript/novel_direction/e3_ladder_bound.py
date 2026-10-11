"""E3 CPU bound: rescue non-SUPPORTED objects by naming them one or more rungs up the hypernym ladder."""
import json,glob,sys,statistics as st
sys.path.insert(0,'.')
from rescap.chair import objects_in,_ancestors
S=sys.argv[1]
imgs=[]
for f in sorted(glob.glob(S+'/*.json')):
    r=json.load(open(f));gold=set().union(*[set(objects_in(c)) for c in r['reference_captions']])
    if not gold:continue
    sup,other=set(),set()
    for p in r['propositions']:
        if p['type'] in('relation','counting','spatial_relation'):continue
        objs=set(objects_in(p['text_vi']))
        (sup if p['verification']['status']=='SUPPORTED' else other).update(objs)
    imgs.append((gold,sup,other-sup))
from rescap.vi.lexicon import HYPERNYMS
def ladder(o):
    """o's strict ancestors, most specific first."""
    from rescap.vi.lexicon import NOUN_CLASSIFIER
    seq=[]
    head=o.split()[0]
    if " " in o and head in NOUN_CLASSIFIER:  # head-initial compound: xe máy -> xe
        seq.append(head)
    while o in HYPERNYMS and HYPERNYMS[o] not in seq:
        o=HYPERNYMS[o];seq.append(o)
    return seq
def prf(sets):
    tp=m=0;R=[];tph=0;Rv=[]
    for (g,_,_),M in zip(imgs,sets):
        gh=set().union(*[_ancestors(x) for x in g])
        tp+=len(M&g);tph+=len(M&gh);m+=len(M);R.append(len(M&g)/len(g))
    P=100*tp/m;Rr=100*st.mean(R);Ph=100*tph/m
    return f'P={P:.1f} R={Rr:.1f} F1={2*P*Rr/(P+Rr):.1f}  P_h={Ph:.1f}  objs/img={m/len(imgs):.2f}'
base=[s for _,s,_ in imgs]
print('SUPPORTED only             ',prf(base))
print('+ all non-SUPPORTED (no verifier)',prf([s|o for _,s,o in imgs]))
oracle=[];always=[];n_resc=n_tot=0
for g,s,o in imgs:
    add=set();alw=set()
    for x in o:
        if x in g: continue           # specific level already right; ladder only helps the wrong-level ones
        n_tot+=1
        lad=ladder(x)
        hit=next((y for y in lad if y in g),None)
        if hit:add.add(hit);n_resc+=1
        if lad:alw.add(lad[0])
    oracle.append(s|add);always.append(s|alw)
print('+ oracle ladder rung in gold',prf(oracle),f' rescued {n_resc}/{n_tot} wrong-level/absent non-SUPPORTED objects')
print('+ always 1 rung up (no check)',prf(always))
# how many non-SUPPORTED objects are right at the specific level (the verifier's pure loss)
lost=sum(len(o&g) for g,s,o in imgs);print('non-SUPPORTED objects already in gold (verifier loss):',lost)
