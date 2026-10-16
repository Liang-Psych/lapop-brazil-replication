# 复现论文表 2–6 的原始数字（原始编码），并给出同一模型修正方向后的结果
import pandas as pd, numpy as np, pyfixest as pf, unicodedata, warnings
warnings.filterwarnings("ignore")
keep=["year","state_name","city_name","china_attitude","america_attitude","gender","age","pe_fina","edu",
      "urban_rural","if_aid","aid_n","presidential_approval_rating","ing4","news_read"]
d=pd.concat([pd.read_csv(f"bra_lapop_{y}.txt",sep=" ",usecols=keep) for y in [12,14,17,19,21,23]],ignore_index=True)
nz=lambda s: s.map(lambda x: unicodedata.normalize("NFKD",x).encode("ascii","ignore").decode().lower() if isinstance(x,str) else x)
pib=pd.read_excel("PIB_2010-2021.xlsx"); g=[c for c in pib.columns if "Produto Interno Bruto per capita" in c][0]
pib=pib[pib.Ano==2021][["Nome da Unidade da Federação","Nome do Município",g]]; pib.columns=["state_name","city_name","gdp_per"]
pib["state_name"]=nz(pib.state_name); pib["city_name"]=nz(pib.city_name)
d=d.rename(columns={"ing4":"democracy_prefer"}).merge(pib,on=["state_name","city_name"],how="left")
d["news_read"]=d.news_read.isin([1,2]).astype(int); d["log_gdp_per"]=np.log(d.gdp_per)
d["dev_level"]=(d.gdp_per>=42893.73).astype(float); d.loc[d.gdp_per.isna(),"dev_level"]=np.nan
B=d[d.china_attitude.notna()].copy(); B["china_trust"]=5-B.china_attitude
ind="gender + age + edu + pe_fina + urban_rural + presidential_approval_rating + democracy_prefer + news_read"
ind_nn=ind.replace(" + news_read",""); ind_nu=ind.replace("urban_rural + ","")
specs=[("表2 M1","aid_n","",B),("表2 M2","aid_n",ind,B),("表2 M3","aid_n",ind+" + log_gdp_per",B),
       ("表3 M1","if_aid","",B),("表3 M2","if_aid",ind,B),("表3 M3","if_aid",ind+" + log_gdp_per",B),
       ("表4 城市","aid_n",ind_nu+" + log_gdp_per",B[B.urban_rural==1]),("表4 农村","aid_n",ind_nu+" + log_gdp_per",B[B.urban_rural==2]),
       ("表5 高发展","aid_n",ind,B[B.dev_level==1]),("表5 低发展","aid_n",ind,B[B.dev_level==0]),
       ("表6 常看新闻","aid_n",ind_nn+" + log_gdp_per",B[B.news_read==1]),("表6 少看新闻","aid_n",ind_nn+" + log_gdp_per",B[B.news_read==0])]
rows=[]
for nm,x,c,dat in specs:
    for y in ["china_attitude","china_trust"]:
        f=f"{y} ~ {x}"+(f" + {c}" if c else "")
        m=pf.feols(f,data=dat,vcov="iid"); t=m.tidy().loc[x]
        rows.append(dict(table=nm,dv=y,coef=round(t.Estimate,4),se=round(t["Std. Error"],4),p=round(t["Pr(>|t|)"],5),n=m._N))
r=pd.DataFrame(rows); r.to_csv("results/thesis_tables_replication.csv",index=False)
pd.set_option("display.width",200); print(r.to_string(index=False))
