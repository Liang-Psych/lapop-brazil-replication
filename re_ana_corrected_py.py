# Python 版修正分析（与 re_ana_corrected.R 逻辑一致，使用 pyfixest = fixest 的 Python 移植）
import pandas as pd, numpy as np, pyfixest as pf, unicodedata, os
os.makedirs("results", exist_ok=True)
keep=["year","state_name","city_name","china_attitude","america_attitude","gender","age","pe_fina","edu",
      "urban_rural","if_aid","aid_n","presidential_approval_rating","ing4","news_read"]
raw=pd.concat([pd.read_csv(f"bra_lapop_{y}.txt",sep=" ",usecols=keep) for y in [12,14,17,19,21,23]],ignore_index=True)
def norm(s): return s.str.lower().map(lambda x: unicodedata.normalize("NFKD",x).encode("ascii","ignore").decode() if isinstance(x,str) else x)
pib=pd.read_excel("PIB_2010-2021.xlsx")
gcol=[c for c in pib.columns if "Produto Interno Bruto per capita" in c][0]
pib=pib[pib.Ano==2021][["Nome da Unidade da Federação","Nome do Município",gcol]]
pib.columns=["state_name","city_name","gdp_per"]
pib["state_name"]=norm(pib.state_name); pib["city_name"]=norm(pib.city_name)
d=raw.rename(columns={"ing4":"democracy_prefer"}).merge(pib,on=["state_name","city_name"],how="left")
d["news_read"]=d.news_read.isin([1,2]).astype(int)
d["log_gdp_per"]=np.log(d.gdp_per)
d["low_dev"]=np.where(d.gdp_per.isna(),np.nan,(d.gdp_per<42893.73).astype(float))
d["rural"]=(d.urban_rural==2).astype(int)
d["city"]=d.state_name+"|"+d.city_name
d["china_trust"]=5-d.china_attitude; d["us_trust"]=5-d.america_attitude
A=d[d.china_attitude.notna()&d.america_attitude.notna()].copy()
B=d[d.china_attitude.notna()].copy()
out=[]
p=lambda *a: out.append(" ".join(str(x) for x in a))
p("样本A N =",len(A),"城市数 =",A.city.nunique(),"| 样本B N =",len(B),"| GDP 匹配缺失:",int(A.gdp_per.isna().sum()))
p("各年 N:",A.groupby("year").size().to_dict())
p("各年对华信任均值:",A.groupby("year").china_trust.mean().round(2).to_dict())
ctrl="gender + age + edu + pe_fina + urban_rural + presidential_approval_rating + democracy_prefer + news_read"
cl={"CRV1":"city"}
specs=[("原始编码 OLS (=re_ana model_12)",f"china_attitude ~ aid_n + {ctrl}",A,"iid","aid_n"),
       ("修正 OLS",f"china_trust ~ aid_n + {ctrl}",A,"iid","aid_n"),
       ("修正 +年份FE",f"china_trust ~ aid_n + {ctrl} | year",A,cl,"aid_n"),
       ("修正 +年份FE +logGDP",f"china_trust ~ aid_n + log_gdp_per + {ctrl} | year",A,cl,"aid_n"),
       ("修正 +年份FE +城市FE",f"china_trust ~ aid_n + {ctrl} | year + city",A,cl,"aid_n"),
       ("修正 if_aid +年份FE",f"china_trust ~ if_aid + {ctrl} | year",A,cl,"if_aid"),
       ("修正 样本B +年份FE",f"china_trust ~ aid_n + {ctrl} | year",B,cl,"aid_n"),
       ("安慰剂 对美信任 +年份FE",f"us_trust ~ aid_n + {ctrl} | year",A,cl,"aid_n")]
c2=ctrl.replace(" + news_read",""); c3=ctrl.replace("urban_rural + ","")
specs+= [("交互 aid_n×low_dev",f"china_trust ~ aid_n*low_dev + {ctrl} | year",A,cl,"aid_n:low_dev"),
         ("交互 aid_n×news_read",f"china_trust ~ aid_n*news_read + {c2} | year",A,cl,"aid_n:news_read"),
         ("交互 aid_n×rural",f"china_trust ~ aid_n*rural + {c3} | year",A,cl,"aid_n:rural")]
rows=[]
for name,fml,data,vc,term in specs:
    if vc!="iid": data=data[data.city.notna()]
    m=pf.feols(fml,data=data,vcov=vc)
    t=m.tidy()
    r=t.loc[term]
    rows.append(dict(model=name,term=term,estimate=r["Estimate"],se=r["Std. Error"],t=r["t value"],p=r["Pr(>|t|)"],n=m._N))
res=pd.DataFrame(rows)
res.to_csv("results/corrected_key_coefs_py.csv",index=False)
pd.set_option("display.width",200)
p("\n"+res.round(4).to_string(index=False))
open("results/corrected_models_py.txt","w").write("\n".join(out))
print("\n".join(out))
