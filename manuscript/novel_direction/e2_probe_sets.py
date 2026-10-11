import sys,json,numpy as np,statistics as st
sys.path[:0]=["scripts","."]
import probe_existence as pe
from pathlib import Path
from rescap.chair import objects_in
from sklearn.linear_model import LogisticRegression
from sklearn.model_selection import GroupKFold
from sklearn.pipeline import make_pipeline
from sklearn.preprocessing import StandardScaler
d=np.load("/root/probe500.npz");meta=[m.split("|",1) for m in d["meta"]]
recs={i:json.load(open(f"/root/s1/stage1/{int(i):011d}.json")) for i in {i for i,_ in meta}}
gold={i:set().union(*[set(objects_in(c)) for c in r["reference_captions"]]) for i,r in recs.items()}
sup={}
for i,r in recs.items():
    sup[i]={o for p in r["propositions"] if p["verification"]["status"]=="SUPPORTED" and p["type"] not in ("relation","counting","spatial_relation") for o in objects_in(p["text_vi"])}
y=np.array([o in gold[i] for i,o in meta],int);g=np.array([i for i,_ in meta])
vy={i:pe.vintern_yes(recs[i]) for i in recs};v=np.array([vy[i].get(o,.5) for i,o in meta])
objs=np.array([o for _,o in meta]);prior=np.zeros(len(y))
for tr,te in GroupKFold(5).split(objs,y,g):
    pos={};cnt={}
    for o,t in zip(objs[tr],y[tr]):pos[o]=pos.get(o,0)+t;cnt[o]=cnt.get(o,0)+1
    prior[te]=[(pos.get(o,0)+1)/(cnt.get(o,0)+3) for o in objs[te]]
def cv(X):
    s=np.zeros(len(y))
    for tr,te in GroupKFold(5).split(X,y,g):
        s[te]=make_pipeline(StandardScaler(),LogisticRegression(C=.05,max_iter=3000)).fit(X[tr],y[tr]).predict_proba(X[te])[:,1]
    return s
L=list(d["layers"]).index(24)
probe=cv(d["h_img"][:,L].astype(np.float32));full=cv(np.column_stack([probe,v,prior]));base=cv(np.column_stack([v,prior]))
def prf(M):
    tp=m=0;R=[]
    for i in recs:
        S=M.get(i,set());tp+=len(S&gold[i]);m+=len(S)
        if gold[i]:R.append(len(S&gold[i])/len(gold[i]))
    P=100*tp/m;Rr=100*st.mean(R);return f"P={P:.1f} R={Rr:.1f} F1={2*P*Rr/(P+Rr):.1f} n/img={m/len(recs):.2f}"
print("SUPPORTED           ",prf(sup))
for name,s in (("Vintern+prior",base),("probe+V+prior",full)):
    for t in (.5,.45,.4,.35,.3):
        M={}
        for (i,o),x in zip(meta,s):
            if x>=t:M.setdefault(i,set()).add(o)
        print(f"{name} >={t:.2f}",prf(M))
