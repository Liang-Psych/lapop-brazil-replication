# 按 ANALYSIS_PLAN.md v1.0 构建分析数据集
import pandas as pd, numpy as np, geopandas as gpd, unicodedata
def nz(s): return s.map(lambda x: unicodedata.normalize("NFKD",x).encode("ascii","ignore").decode().lower().strip() if isinstance(x,str) else x)
keep=["year","state_name","city_name","china_attitude","america_attitude","gender","age","pe_fina","edu",
      "urban_rural","if_aid","aid_n","presidential_approval_rating","ing4","news_read"]
d=pd.concat([pd.read_csv(f"bra_lapop_{y}.txt",sep=" ",usecols=keep) for y in [12,14,17,19,21,23]],ignore_index=True)
d=d[d.china_attitude.notna()].rename(columns={"ing4":"democracy_prefer"})
d["news_read"]=d.news_read.isin([1,2]).astype(int)
d["china_trust"]=5-d.china_attitude
# --- 市镇坐标（降级方案：市镇驻地坐标表） ---
mu=pd.read_csv("municipios.csv"); es=pd.read_csv("estados.csv",encoding="utf-8-sig")
mu=mu.merge(es[["codigo_uf","nome"]].rename(columns={"nome":"uf_nome"}),on="codigo_uf")
mu["state_name"]=nz(mu.uf_nome); mu["city_name"]=nz(mu.nome)
mu=mu[["state_name","city_name","codigo_ibge","latitude","longitude"]]
# 市镇改名的别名（数据清洗，非规格变化）
alias={("sao paulo","embu das artes"):"embu",("rio grande do sul","sant'ana do livramento"):"santana do livramento"}
mu["city_name"]=[alias.get((a,b),b) for a,b in zip(mu.state_name,mu.city_name)]
d["city_name"]=[alias.get((a,b),b) for a,b in zip(d.state_name,d.city_name)]
d=d.merge(mu,on=["state_name","city_name"],how="left")
print("受访者 N =",len(d),"; 缺城市名:",int(d.city_name.isna().sum()),"; 城市未匹配到坐标:",int((d.city_name.notna()&d.codigo_ibge.isna()).sum()))
print("未匹配城市:",d[d.city_name.notna()&d.codigo_ibge.isna()][["state_name","city_name"]].drop_duplicates().values.tolist()[:20])
# --- 项目 ---
p=gpd.read_file("brazil_aid.gpkg").to_crs(5880)
big={"ENERGY","INDUSTRY, MINING, CONSTRUCTION","COMMUNICATIONS","WATER SUPPLY AND SANITATION"}
p["grp"]=np.where(p["Sector.Name"].isin(big),"big","social")
p["comp"]=p["Completion.Year"]
print("项目:",len(p),"大型",int((p.grp=="big").sum()),"社会",int((p.grp=="social").sum()))
cities=d[d.codigo_ibge.notna()][["codigo_ibge","latitude","longitude"]].drop_duplicates("codigo_ibge")
cg=gpd.GeoDataFrame(cities,geometry=gpd.points_from_xy(cities.longitude,cities.latitude),crs=4326).to_crs(5880)
# 距离矩阵（米）：城市点 × 项目多边形
D=np.vstack([p.geometry.distance(pt).values for pt in cg.geometry])   # n_city × n_proj
dist=pd.DataFrame(D,index=cg.codigo_ibge.values)
comp=p.comp.values; grp=p.grp.values; status=p.Status.values
def expo(code,year,km,mask=None):
    m=(dist.loc[code].values<=km*1000)&(~np.isnan(comp))&(comp<year)
    if mask is not None: m&=mask
    return int(m.sum())
rows=[]
for code,year in d[d.codigo_ibge.notna()][["codigo_ibge","year"]].drop_duplicates().itertuples(index=False):
    near50=dist.loc[code].values<=50000
    done=near50&(~np.isnan(comp))&(comp<year)
    pending=near50&~done   # 50公里内有项目但调查时尚未完工（含 Pipeline / Implementation / 调查年及之后完工）
    first=np.nanmin(np.where(near50,comp,np.nan)) if np.any(near50&~np.isnan(comp)) else np.nan
    rows.append(dict(codigo_ibge=code,year=year,
        exp25=expo(code,year,25),exp50=expo(code,year,50),exp100=expo(code,year,100),
        exp50_big=expo(code,year,50,grp=="big"),exp50_social=expo(code,year,50,grp=="social"),
        completed50=int(done.any()),pending50_only=int((~done.any()) and pending.any()),
        first_comp50=first))
cy=pd.DataFrame(rows)
d=d.merge(cy,on=["codigo_ibge","year"],how="left")
d["city"]=d.codigo_ibge
d.to_csv("results/plan_v1_data.csv",index=False)
v=d[d.city.notna()]
print("有坐标样本 N =",len(v),"城市数 =",v.city.nunique())
print("exp50>0 比例:",round((v.exp50>0).mean(),3),"; 有暴露的城市数:",v[v.exp50>0].city.nunique())
print("exp50_big>0 城市数:",v[v.exp50_big>0].city.nunique(),"; exp50_social>0 城市数:",v[v.exp50_social>0].city.nunique())
print("6a 处理组城市:",v[v.completed50==1].city.nunique(),"; 对照组城市:",v[v.pending50_only==1].city.nunique())
ev=v[v.first_comp50.notna()]
pre=set(ev[ev.year<=ev.first_comp50].city); post=set(ev[ev.year>ev.first_comp50].city)
print("6b 有事件的城市:",ev.city.nunique(),"; 事件前后都有受访者的城市:",len(pre&post))
print("城市在多少轮出现:",v.groupby("city").year.nunique().value_counts().sort_index().to_dict())
