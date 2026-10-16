# 勘误 4.1 补充表：改用主样本（对华题非缺失，N = 4,318）
import pandas as pd, numpy as np, pyfixest as pf, unicodedata, warnings
warnings.filterwarnings("ignore")
keep=["year","state_name","city_name","china_attitude","gender","age","pe_fina","edu","urban_rural","if_aid","aid_n","presidential_approval_rating","ing4","news_read"]
d=pd.concat([pd.read_csv(f"bra_lapop_{y}.txt",sep=" ",usecols=keep) for y in [12,14,17,19,21,23]],ignore_index=True)
nz=lambda s: s.map(lambda x: unicodedata.normalize("NFKD",x).encode("ascii","ignore").decode().lower() if isinstance(x,str) else x)
pib=pd.read_excel("PIB_2010-2021.xlsx"); g=[c for c in pib.columns if "Produto Interno Bruto per capita" in c][0]
pib=pib[pib.Ano==2021][["Nome da Unidade da Federação","Nome do Município",g]]; pib.columns=["state_name","city_name","gdp_per"]
pib["state_name"]=nz(pib.state_name); pib["city_name"]=nz(pib.city_name)
d=d.rename(columns={"ing4":"democracy_prefer"}).merge(pib,on=["state_name","city_name"],how="left")
d=d[d.china_attitude.notna()].copy()
d["news_read"]=d.news_read.isin([1,2]).astype(int); d["log_gdp_per"]=np.log(d.gdp_per)
d["low_dev"]=np.where(d.gdp_per.isna(),np.nan,(d.gdp_per<42893.73).astype(float)); d["rural"]=(d.urban_rural==2).astype(int)
d["city"]=d.state_name+"|"+d.city_name; d["china_trust"]=5-d.china_attitude
C="gender + age + edu + pe_fina + urban_rural + presidential_approval_rating + democracy_prefer + news_read"
cl={"CRV1":"city"}; dc=d[d.city.notna()]
specs=[("pooled OLS + controls",f"china_trust ~ aid_n + {C}",d,"iid","aid_n"),
       ("+ year FE, cluster",f"china_trust ~ aid_n + {C} | year",dc,cl,"aid_n"),
       ("+ year FE + logGDP",f"china_trust ~ aid_n + log_gdp_per + {C} | year",dc,cl,"aid_n"),
       ("+ year & city FE",f"china_trust ~ aid_n + {C} | year + city",dc,cl,"aid_n"),
       ("if_aid, year FE",f"china_trust ~ if_aid + {C} | year",dc,cl,"if_aid"),
       ("x low_dev",f"china_trust ~ aid_n*low_dev + {C} | year",dc,cl,"aid_n:low_dev"),
       ("x news_read",f"china_trust ~ aid_n*news_read + {C.replace(' + news_read','')} | year",dc,cl,"aid_n:news_read"),
       ("x rural",f"china_trust ~ aid_n*rural + {C.replace('urban_rural + ','')} | year",dc,cl,"aid_n:rural")]
rows=[]
for nm,f,dat,vc,t in specs:
    m=pf.feols(f,data=dat,vcov=vc); r=m.tidy().loc[t]
    rows.append(dict(model=nm,term=t,coef=round(r.Estimate,4),se=round(r["Std. Error"],4),p=round(r["Pr(>|t|)"],4),n=m._N))
r=pd.DataFrame(rows); r.to_csv("results/corrected_supp_sampleB.csv",index=False); print(r.to_string(index=False))
print("year means:",d.groupby("year").china_trust.mean().round(2).to_dict())
