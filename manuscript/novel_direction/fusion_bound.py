"""How does fusing k references shift object P/R against independent references? (leakage-free split)"""
import json,glob,sys,statistics as st,itertools as it
sys.path.insert(0,'.')
from rescap.chair import objects_in
S=sys.argv[1];imgs=[]
for f in sorted(glob.glob(S+'/*.json')):
    refs=json.load(open(f))['reference_captions']
    if len(refs)>=5:imgs.append([set(objects_in(c)) for c in refs[:5]])
def score(pick):  # pick(train_refs)->set; eval vs pooled of held-out refs; average over splits
    out=[]
    for A in [(0,1),(1,2),(2,3),(3,4),(0,4)]:
        tp=m=0;R=[]
        for rs in imgs:
            a=[rs[i] for i in A];B=set().union(*[rs[i] for i in range(5) if i not in A])
            M=pick(a);tp+=len(M&B);m+=len(M)
            if B:R.append(len(M&B)/len(B))
        out.append((100*tp/m,100*st.mean(R)))
    P=st.mean(x[0] for x in out);R=st.mean(x[1] for x in out);return f'P={P:.1f} R={R:.1f} F1={2*P*R/(P+R):.1f}'
print('single ref       ',score(lambda a:a[0]))
print('union of 2 refs  ',score(lambda a:a[0]|a[1]))
print('intersect 2 refs ',score(lambda a:a[0]&a[1]))
