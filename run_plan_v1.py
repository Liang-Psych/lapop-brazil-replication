# 按 ANALYSIS_PLAN.md v1.0 第 3–6 节运行
import pandas as pd, numpy as np, pyfixest as pf, warnings
from scipy import stats
from statsmodels.miscmodels.ordinal_model import OrderedModel
warnings.filterwarnings("ignore")
OUT="results/plan_v1/"
d=pd.read_csv("results/plan_v1_data.csv")
d=d[d.city.notna()].copy(); d["city"]=d.city.astype(int)
ctrl=["gender","age","edu","pe_fina","urban_rural","presidential_approval_rating","democracy_prefer","news_read"]
C=" + ".join(ctrl)
log=[]; P=lambda *a: (print(*a), log.append(" ".join(map(str,a))))
rows=[]
def rec(section,spec,term,est,se,p,n,ncl,boot=np.nan,note=""):
    lo,hi=est-1.96*se,est+1.96*se
    rows.append(dict(section=section,spec=spec,term=term,estimate=est,se=se,ci_low=lo,ci_high=hi,p_cluster=p,p_wildboot=boot,n=n,n_cities=ncl,note=note))
def ols(section,spec,fml,data,term,boot=True):
    data=data.dropna(subset=[c for c in pf.feols(fml,data=data.head(50)).__dict__.get("_coefnames",[])] if False else [])
    m=pf.feols(fml,data=data,vcov={"CRV1":"city"})
    t=m.tidy().loc[term]
    bp=np.nan; note=""
    if boot:
        try:
            b=m.wildboottest(param=term,reps=9999,seed=20261012)
            bp=float(b["Pr(>|t|)"])
        except Exception as e: note=f"bootstrap失败: {type(e).__name__}"
    used=data.loc[~data.index.isin(getattr(m,"_na_index",[]))]
    rec(section,spec,term,t["Estimate"],t["Std. Error"],t["Pr(>|t|)"],m._N,used.city.nunique(),bp,note)
    return m
samples={"主样本B":d,"样本A":d[d.america_attitude.notna()],"剔除2023":d[d.year!=2023]}

# ---------- §3 有序 logit ----------
def ologit(spec,data,term):
    x=data[[term]+ctrl+["china_trust","year","city"]].dropna()
    X=pd.concat([x[[term]+ctrl],pd.get_dummies(x.year,prefix="y",drop_first=True).astype(float)],axis=1)
    y=pd.Categorical(x.china_trust.astype(int),categories=[1,2,3,4],ordered=True)
    r=OrderedModel(y,X,distr="logit").fit(method="bfgs",maxiter=2000,disp=False,cov_type="cluster",cov_kwds={"groups":x.city.values})
    rec("§3 有序logit",spec,term,r.params[term],r.bse[term],r.pvalues[term],len(x),x.city.nunique(),note="系数为log-odds")
    if spec=="主样本B" and term=="aid_n":
        X0=X.copy(); X0[term]=0; X1=X.copy(); X1[term]=1
        pr0=r.model.predict(r.params,exog=X0).mean(0); pr1=r.model.predict(r.params,exog=X1).mean(0)
        P("§3 aid_n 0→1 各等级平均预测概率变化(1=完全不可信…4=非常可信):",np.round(pr1-pr0,4).tolist())
for s,dd in samples.items(): ologit(s,dd,"aid_n")
ologit("主样本B","主样本B" and d,"if_aid") if False else ologit("主样本B(if_aid)",d,"if_aid")

# ---------- §4 空间暴露 ----------
for km in [50,25,100]:
    for s,dd in (samples.items() if km==50 else [("主样本B",d)]):
        ols("§4 空间暴露",f"{s} {km}km",f"china_trust ~ exp{km} + {C} | year",dd,f"exp{km}")

# ---------- §5 项目类型 ----------
for s,dd in samples.items():
    m=ols("§5 项目类型",s,f"china_trust ~ exp50_big + exp50_social + {C} | year",dd,"exp50_big")
    t=m.tidy().loc["exp50_social"]; V=m._vcov; names=list(m._coefnames)
    rec("§5 项目类型",s,"exp50_social",t["Estimate"],t["Std. Error"],t["Pr(>|t|)"],m._N,np.nan)
    i,j=names.index("exp50_big"),names.index("exp50_social"); b=m._beta_hat
    diff=b[i]-b[j]; se=np.sqrt(V[i,i]+V[j,j]-2*V[i,j]); G=dd.dropna(subset=["china_trust","exp50_big"]+ctrl).city.nunique()
    p=2*stats.t.sf(abs(diff/se),df=G-1)
    rec("§5 项目类型",s,"big − social (Wald)",diff,se,p,m._N,np.nan)

# ---------- §6a 承诺未完工对照 ----------
for s,dd in samples.items():
    sub=dd[(dd.completed50==1)|(dd.pending50_only==1)]
    ols("§6a 已完工vs承诺未完工",s,f"china_trust ~ completed50 + {C} | year",sub,"completed50")

# ---------- §6b Sun & Abraham 事件研究 ----------
e=d.dropna(subset=["china_trust"]+ctrl).copy()
e["rel"]=e.year-e.first_comp50
def binr(r):
    if np.isnan(r): return "never"
    if r<=-5: return "pre_le-5"
    if r<=-2: return "pre_-4_-2"
    if r==-1: return "ref_-1"
    if r<=2: return "post_0_2"
    if r<=5: return "post_3_5"
    return "post_ge6"
e["bin"]=e.rel.map(binr)
P("§6b 各区间样本量:",e.bin.value_counts().to_dict())
P("§6b 各区间城市数:",e.groupby("bin").city.nunique().to_dict())
e["cohort"]=e.first_comp50.fillna(0).astype(int)
cells=e[~e.bin.isin(["never","ref_-1"])].groupby(["cohort","bin"]).size()
cols=[]
for (c,b),n in cells.items():
    nm=f"D_{c}_{b}".replace("-","m"); e[nm]=((e.cohort==c)&(e.bin==b)).astype(int); cols.append((nm,c,b,n))
m=pf.feols(f"china_trust ~ {' + '.join(n for n,_,_,_ in cols)} + {C} | city + year",data=e,vcov={"CRV1":"city"})
names=list(m._coefnames); beta=pd.Series(m._beta_hat,index=names); V=pd.DataFrame(m._vcov,index=names,columns=names)
kept=[(n,c,b,k) for n,c,b,k in cols if n in names and not np.isnan(beta[n])]
dropped=[n for n,_,_,_ in cols if n not in names]
if dropped: P("§6b 因共线被剔除的交互项:",dropped)
G=e.city.nunique()
def agg(bins,label):
    sel=[(n,k) for n,c,b,k in kept if b in bins]
    if not sel: return None
    w=np.array([k for _,k in sel],float); w/=w.sum(); ns=[n for n,_ in sel]
    est=float(w@beta[ns].values); se=float(np.sqrt(w@V.loc[ns,ns].values@w))
    p=2*stats.t.sf(abs(est/se),df=G-1)
    rec("§6b 事件研究(SA)",label,"加权平均",est,se,p,m._N,G)
    return ns,w
bins=["pre_le-5","pre_-4_-2","post_0_2","post_3_5","post_ge6"]
aggs={b:agg([b],b) for b in bins}
agg(["post_0_2","post_3_5","post_ge6"],"事后平均ATT")
# 事前趋势联合检验
pre=[aggs[b] for b in ["pre_le-5","pre_-4_-2"] if aggs[b]]
if pre:
    W=np.zeros((len(pre),len(names)))
    for r,(ns,w) in enumerate(pre):
        for n,wi in zip(ns,w): W[r,names.index(n)]=wi
    g=W@beta.values; S=W@V.values@W.T
    F=float(g@np.linalg.solve(S,g))/len(pre); pF=stats.f.sf(F,len(pre),G-1)
    P(f"§6b 事前趋势联合检验 F({len(pre)},{G-1}) = {F:.3f}, p = {pF:.4f}")
    rows.append(dict(section="§6b 事件研究(SA)",spec="事前趋势联合F检验",term="pre bins",estimate=F,p_cluster=pF,n=m._N,n_cities=G))

res=pd.DataFrame(rows)
# ---------- Holm 校正（检验族：各节主系数，主样本，cluster p） ----------
fam={"§3":("§3 有序logit","主样本B","aid_n"),"§4":("§4 空间暴露","主样本B 50km","exp50"),
     "§5":("§5 项目类型","主样本B","big − social (Wald)"),"§6a":("§6a 已完工vs承诺未完工","主样本B","completed50"),
     "§6b":("§6b 事件研究(SA)","事后平均ATT","加权平均")}
idx=[res[(res.section==a)&(res.spec==b)&(res.term==c)].index[0] for a,b,c in fam.values()]
pv=res.loc[idx,"p_cluster"].values; o=np.argsort(pv); k=len(pv); adj=np.empty(k); run=0
for r,i in enumerate(o): run=max(run,min(1,(k-r)*pv[i])); adj[i]=run
res["p_holm"]=np.nan; res.loc[idx,"p_holm"]=adj; res["主检验族"]=""; res.loc[idx,"主检验族"]="是"
res.to_csv(OUT+"plan_v1_results.csv",index=False)
pd.set_option("display.width",250); pd.set_option("display.max_columns",20)
P("\n"+res.drop(columns=["ci_low","ci_high"]).round(4).to_string(index=False))
P("\n主检验族（Holm 校正）:\n"+res.loc[idx,["section","spec","term","estimate","ci_low","ci_high","p_cluster","p_wildboot","p_holm"]].round(4).to_string(index=False))
open(OUT+"plan_v1_log.txt","w").write("\n".join(log))
