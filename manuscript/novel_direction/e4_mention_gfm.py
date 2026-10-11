"""Offline: can stored signals rank proposed objects so some threshold beats SUPPORTED on BOTH P and R (vs refs)?"""
import json,glob,sys,collections,statistics as st
import numpy as np
from sklearn.linear_model import LogisticRegression
sys.path.insert(0,'.')
from rescap.chair import objects_in
S=sys.argv[1]
def frac(s,w):return sum(x.strip().lower().startswith(w) for x in s)/max(len(s),1)
rows=[];imgs=[]
for f in sorted(glob.glob(S+'/*.json')):
    r=json.load(open(f));refs=r['reference_captions']
    gold=set().union(*[set(objects_in(c)) for c in refs])
    if not gold:continue
    ents=r['entities'];erank={}
    for i,e in enumerate(ents):
        for o in objects_in(e.get('surface','')):erank.setdefault(o,i)
    feat=collections.defaultdict(lambda:{'sup':0,'unc':0,'rej':0,'yes':0.,'no':0.,'n':0,'types':set()})
    for p in r['propositions']:
        st_=p['verification']['status'];pr=(p.get('evidence') or {}).get('probes') or []
        d=[x for x in pr if x['polarity']=='affirms'];n=[x for x in pr if x['polarity']=='refutes']
        y=frac(d[0]['samples'],'có') if d else .5;nn=frac(n[0]['samples'],'không') if n else .5
        for o in set(objects_in(p['text_vi'])):
            F=feat[o];F['n']+=1;F['types'].add(p['type'])
            F[{'SUPPORTED':'sup','UNCERTAIN':'unc','REJECTED':'rej'}[st_]]+=1
            F['yes']=max(F['yes'],y);F['no']=max(F['no'],nn)
    refsets=[set(objects_in(c)) for c in refs]
    imgs.append((r['image_id'],gold,len(refs),refsets))
    for o,F in feat.items():
        rows.append(dict(img=len(imgs)-1,obj=o,y=int(o in gold),k=sum(o in rs for rs in refsets),sup=int(F['sup']>0),unc=int(F['unc']>0),rejonly=int(F['sup']==0 and F['unc']==0),
            yes=F['yes'],no=F['no'],logn=np.log1p(F['n']),rank=erank.get(o,len(ents)),ent='entity' in F['types']))
N=len(imgs);fold=np.arange(N)%5;rng=np.random.default_rng(0);rng.shuffle(fold)
objs=sorted({x['obj'] for x in rows});oi={o:i for i,o in enumerate(objs)}
def X(rs,prior):
    return np.array([[x['sup'],x['unc'],x['rejonly'],x['yes'],x['no'],x['logn'],min(x['rank'],16)/16,x['ent'],prior.get(x['obj'],0.3)] for x in rs])
score=np.zeros(len(rows))
for k in range(5):
    tr=[x for x in rows if fold[x['img']]!=k];te_idx=[i for i,x in enumerate(rows) if fold[x['img']]==k]
    c=collections.Counter();t=collections.Counter()
    for x in tr:c[x['obj']]+=x['y'];t[x['obj']]+=1
    prior={o:(c[o]+1)/(t[o]+3) for o in t}
    m=LogisticRegression(max_iter=2000).fit(X(tr,prior),[x['y'] for x in tr])
    score[te_idx]=m.predict_proba(X([rows[i] for i in te_idx],prior))[:,1]

# binomial-count model: same features, each candidate seen as k of 5 annotator mentions
sb=np.zeros(len(rows))
for k_ in range(5):
    tr=[x for x in rows if fold[x['img']]!=k_];te_idx=[i for i,x in enumerate(rows) if fold[x['img']]==k_]
    c=collections.Counter();t=collections.Counter()
    for x in tr:c[x['obj']]+=x['y'];t[x['obj']]+=1
    prior={o:(c[o]+1)/(t[o]+3) for o in t}
    Xt=X(tr,prior);Xb=np.vstack([Xt,Xt]);yb=[1]*len(tr)+[0]*len(tr)
    w=[x['k'] for x in tr]+[5-x['k'] for x in tr]
    m=LogisticRegression(max_iter=2000).fit(Xb,yb,sample_weight=w)
    q=m.predict_proba(X([rows[i] for i in te_idx],prior))[:,1]
    sb[te_idx]=q
from sklearn.metrics import roc_auc_score
y=np.array([x['y'] for x in rows])
print('AUROC pooled-target',round(roc_auc_score(y,score),4),'| binomial q',round(roc_auc_score(y,sb),4))
by=collections.defaultdict(list)
for i,x in enumerate(rows):by[x['img']].append(i)
def evaluate(selfn,label):
    # pooled-gold metric (Table IV) and held-out single annotator metric
    tp=m_=0;R=[];tp1=m1=0;R1=[]
    for j,(iid,g,_,rs) in enumerate(imgs):
        M=selfn(j)
        tp+=len(M&g);m_+=len(M);R.append(len(M&g)/len(g))
        for a in rs:
            if a:tp1+=len(M&a);m1+=len(M);R1.append(len(M&a)/len(a))
    f=lambda P,R_:2*P*R_/(P+R_) if P+R_ else 0
    P=100*tp/max(m_,1);Rr=100*st.mean(R);P1=100*tp1/max(m1,1);Rr1=100*st.mean(R1)
    print(f'{label:28s} pooled P={P:.1f} R={Rr:.1f} F1={f(P,Rr):.1f} | single P={P1:.1f} R={Rr1:.1f} F1={f(P1,Rr1):.1f}')
def thr(sc,t):return lambda j:{rows[i]['obj'] for i in by[j] if sc[i]>=t}
def gfm(p):
    """per-image set maximising expected F1 under independent Bernoulli p (sort, scan prefixes; plug-in approx)"""
    def sel(j):
        idx=sorted(by[j],key=lambda i:-p[i]);best=(0,set());s=0
        ev=sum(p[i] for i in idx)
        for n,i in enumerate(idx,1):
            s+=p[i];e=2*s/(n+ev)
            if e>best[0]:best=(e,{rows[ii]['obj'] for ii in idx[:n]})
        return best[1]
    return sel
evaluate(lambda j:{rows[i]['obj'] for i in by[j] if rows[i]['sup']},'SUPPORTED')
for t in (0.5,0.4,0.35):evaluate(thr(score,t),f'pooled score>={t}')
for t in (0.25,0.2,0.15):evaluate(thr(sb,t),f'binomial q>={t}')
evaluate(gfm(score),'GFM on pooled p')
evaluate(gfm(sb),'GFM on q (single annotator)')
evaluate(gfm(1-(1-sb)**5),'GFM on 1-(1-q)^5')
