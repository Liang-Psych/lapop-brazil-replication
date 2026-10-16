# 将原始 mil10a 按 LAPOP 官方仪表盘口径换算（非常可信 = 100），与仪表盘巴西各轮均值对照
# 运行：在仓库根目录 python3 check_dashboard.py
import pandas as pd, numpy as np
tot=0
for y in [2012,2014,2017,2019,2021,2023]:
    p=f"Brazil_{y}.dta"
    r=pd.io.stata.StataReader(p); r.variable_labels(); cols=r._varlist
    w=[c for c in ["weight1500","wt","weight"] if c in cols]
    use=["mil10a"]+w+(["pais"] if y==2023 else [])
    d=pd.read_stata(p,columns=use,convert_categoricals=False)
    if y==2023: d=d[d.pais==15]
    d=d[d.mil10a.isin([1,2,3,4])]; tot+=len(d)
    s=(4-d.mil10a)/3*100          # 官方仪表盘口径：非常可信=100
    wt=d[w[0]] if w else pd.Series(1,index=d.index)
    print(y,"n=",len(d),"未加权",round(s.mean(),1),"加权("+(w[0] if w else "无")+")",round(np.average(s,weights=wt),1))
print("合计",tot)
