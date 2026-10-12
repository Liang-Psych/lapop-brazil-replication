# 勘误说明 / Erratum

**论文**：Xu, L. (2025). *The Impact of Chinese Development Finance on Brazilian Public Attitudes Toward China*（《中国发展融资对巴西公众对华态度的影响》）. 硕士学位论文，中国农业大学 / 圣保罗大学路易斯·德·凯罗斯农学院（ESALQ-USP）双学位项目。

**勘误版本**：v1.0 · 2026-10-12（草稿，待导师审阅）

**问题发现日期**：2026-07-26

> 带 【 】 的内容需由作者根据论文原文补充，例如章节号和表格编号。

---

## 中文版

### 1. 摘要

原论文的因变量“对华态度”编码方向与解读方向相反。修正后，原论文的核心结论不成立：**没有稳健证据表明中国发展融资项目与巴西民众对中国政府的信任相关**，无论正向还是负向。原论文报告的三项异质性效应也不成立。数据整合工作与两个案例研究不受影响。

### 2. 错误的性质

- **涉及变量**：美洲晴雨表（LAPOP AmericasBarometer）题目 `mil10a`，即中国政府的可信度。
- **原始量表**：2012、2014、2017、2019、2021、2023 六轮均为：1 = 非常可信，2 = 有些可信，3 = 不太可信，4 = 完全不可信。
- **错误**：分析脚本 `lapop_12.R` 至 `lapop_23.R` 直接使用原始取值（`china_attitude = mil10a`），因此**数值越大表示越不信任**；但论文将其解读为数值越大态度越积极。对照变量 `mil10e`（美国政府的可信度）存在同样的问题。
- **范围**：六轮全部受影响，方向一致。“不知道”和“拒答”已正确设为缺失值，没有混入 1 到 4 分。
- **性质**：这是变量方向解读上的技术错误，不涉及数据篡改或选择性报告。原始数据、代码和结果记录均完整保留在本仓库中。

### 3. 受影响与不受影响的内容

**受影响，应撤回：**

1. 摘要及结论中“中国发展融资项目与巴西当地居民对中国的态度存在显著正相关”“中国的发展融资能够产生积极的软实力回报”的表述。【第 X 章，表 X】
2. 异质性结论：“在欠发达城市产生更显著的积极态度效应”“经常接触新闻媒体的个体表现出更强的积极态度反应”，以及城乡分组结果。【第 X 章，表 X】
3. 基于上述定量结果提出的政策启示。【第 X 章】

**不受影响：**

1. LAPOP 六轮调查与 AidData 中国发展融资地理空间数据的整合（4,318 名受访者、499 个城市）。
2. 贝罗蒙特特高压输电线项目与中巴科技小院项目的案例研究资料及其对当地评价机制的描述。但案例结论**不能**再被表述为与定量结果相互印证，也不能推广为巴西整体的情况。

### 4. 修正后的结果

修正方法：将因变量统一反转为 `china_trust = 5 − mil10a`（1 = 完全不可信 … 4 = 非常可信）。

#### 4.1 直接修正（与原论文相同的模型，以及补充年份固定效应和城市聚类标准误）

| 模型 | `aid_n` 系数 | 标准误 | p | N |
|---|---|---|---|---|
| 原论文写法（编码未修正） | +0.038 | 0.012 | 0.001 | 3,871 |
| 修正方向，混合 OLS | −0.038 | 0.012 | 0.001 | 3,871 |
| + 年份固定效应，城市聚类 | +0.007 | 0.009 | 0.43 | 3,842 |
| + 年份固定效应 + log 人均 GDP | +0.016 | 0.010 | 0.10 | 3,805 |
| + 年份与城市固定效应 | −0.034 | 0.017 | 0.046 | 3,564 |
| `if_aid`，年份固定效应 | +0.011 | 0.038 | 0.77 | 3,842 |
| 安慰剂：对美国政府信任 | +0.007 | 0.012 | 0.55 | 3,842 |

| 原异质性结论的正式交互项检验（年份固定效应，城市聚类） | 系数 | p |
|---|---|---|
| `aid_n` × 欠发达城市 | −0.011 | 0.78 |
| `aid_n` × 常看新闻 | −0.012 | 0.60 |
| `aid_n` × 农村 | −0.047 | 0.68 |

说明：
- 修正方向后，混合 OLS 呈显著**负**相关。但巴西民众的对华信任在调查期间整体下降（年度均值 2017 年为 2.63，2023 年为 1.96），而中国项目同期持续增加。加入年份固定效应后效应消失，说明混合 OLS 的结果主要反映共同的时间趋势。
- 只有同时加入城市固定效应的规格在 5% 水平上勉强显著为负（p = 0.046），其他规格均不支持，因此不作为稳健结论。

#### 4.2 预先登记的扩展分析

为避免在已知结果后进行规格搜索，作者于 2026-10-12 先将扩展分析的规格、推断方法和结论措辞规则写入 `ANALYSIS_PLAN.md` 并提交到版本库，之后才运行。结果如下（主样本 N = 4,318，Holm 多重检验校正）：

| 检验 | 估计值 | 95% 置信区间 | Holm 校正 p |
|---|---|---|---|
| 有序 logit，`aid_n`（log-odds） | 0.016 | [−0.020, 0.052] | 1.00 |
| 50 公里内已完工项目数 | 0.005 | [−0.010, 0.021] | 1.00 |
| 能源与工业类项目 − 社会领域项目 | −0.010 | [−0.060, 0.041] | 1.00 |
| 已完工 vs 已承诺未完工项目所在地 | 0.064 | [−0.026, 0.153] | 0.67 |
| 事件研究（Sun & Abraham），事后平均效应 | 0.122 | [−0.036, 0.281] | 0.66 |

- 五项均不显著。改用两题均作答的样本、剔除 2023 年、改用 25 或 100 公里范围，结论均不变。
- 事件研究的事前趋势联合检验显著（F(2, 492) = 3.41，p = 0.034）：后来获得项目的城市在项目完工**之前**对华信任就已偏高。因此事件研究结果不作因果解读。这也提示原论文观察到的相关性可能部分来自项目选址，而非项目本身的影响。
- 执行中与计划的 7 处偏离及其理由，见 `ANALYSIS_PLAN.md` 第 8 节。

### 5. 修正后的结论

1. 没有稳健证据表明中国发展融资项目与巴西民众对中国政府的信任相关。置信区间较窄：50 公里内每增加一个已完工项目，对华信任（1 到 4 分）的变化可以排除大于约 +0.02 分或小于约 −0.01 分的效应。
2. 调查期间对华信任的变化主要由全国性的时间趋势驱动，而非地方层面的项目暴露。
3. 有迹象表明项目选址与当地原有的对华态度相关，后续研究需要更严格的因果识别设计。
4. 原论文的三项异质性结论均不成立。
5. 案例研究显示，在特定社区和特定类型的项目中可以观察到当地的积极评价；但这些发现不能推广为整体层面的“软实力回报”。

### 6. 其他需要说明的问题

- **样本口径**：原论文报告的样本量 4,318 对应“对华题非缺失”的口径；原分析脚本 `re_ana.R` 的回归另外要求对美题也非缺失，实际样本为 3,973。修正分析以 4,318 为主样本，以 3,973 为稳健性检验，两者结论一致。
- **题目措辞**：2023 年题目为“中国的可信度”，此前各轮为“中国政府的可信度”。剔除 2023 年后结论不变。
- **市镇坐标**：空间暴露分析使用的市镇驻地坐标来自 kelvins/municipios-brasileiros（IBGE 来源，MIT 许可）。

### 7. 复现文件

均位于本仓库 `correction` 分支：

| 文件 | 内容 |
|---|---|
| `lapop_12.R` … `lapop_23.R`、`re_ana.R` | 原论文版本，未作改动 |
| `re_ana_corrected.R`、`pixi.toml` | 修正版分析（R），`pixi run corrected` |
| `re_ana_corrected_py.py` | 同一修正分析的 Python（pyfixest）版本 |
| `ANALYSIS_PLAN.md` | 预先登记的扩展分析计划、偏离记录、结果摘要 |
| `build_plan_data.py`、`run_plan_v1.py` | 扩展分析的数据构建与估计脚本 |
| `results/` | 全部修正结果 |

### 8. 时间线

| 日期 | 事项 |
|---|---|
| 2025-05-22 | 获得硕士学位（USP 学位证书所载日期） |
| 2026-07-26 | 复核中发现因变量编码方向问题；仓库暂停公开访问 |
| 2026-10-12 | 完成直接修正分析；提交预先登记的分析计划并运行；完成本勘误草稿 |

---

## English Version

### 1. Summary

The dependent variable in the original thesis, attitudes toward China, was interpreted in the opposite direction of its coding. After correction, the thesis's central finding does not hold: **there is no robust evidence that Chinese development finance projects are associated with Brazilians' trust in the Chinese government**, in either direction. The three heterogeneous effects reported in the thesis also do not hold. The data assembly and the two case studies are unaffected.

### 2. Nature of the error

- **Variable**: AmericasBarometer (LAPOP) item `mil10a`, trustworthiness of the Chinese government.
- **Original scale**: in all six waves (2012, 2014, 2017, 2019, 2021, 2023): 1 = very trustworthy, 2 = somewhat trustworthy, 3 = not very trustworthy, 4 = not at all trustworthy.
- **Error**: the scripts `lapop_12.R` to `lapop_23.R` used the raw values (`china_attitude = mil10a`), so **higher values meant less trust**, while the thesis interpreted higher values as more favourable attitudes. The comparison variable `mil10e` (trustworthiness of the US government) had the same issue.
- **Scope**: all six waves are affected, in the same direction. "Don't know" and "No response" were correctly treated as missing and did not enter the 1–4 scale.
- **Nature**: a technical error in interpreting the variable's direction. It involves no data manipulation or selective reporting. The original data, code and outputs are preserved in full in this repository.

### 3. Affected and unaffected content

**Affected, to be withdrawn:**

1. Statements in the abstract and conclusions that Chinese development finance projects are significantly and positively associated with local Brazilian attitudes toward China and generate positive soft-power returns. [Chapter X, Table X]
2. Heterogeneity findings: stronger positive effects in less-developed cities, stronger positive responses among frequent news consumers, and the urban/rural split results. [Chapter X, Table X]
3. Policy implications derived from these quantitative findings. [Chapter X]

**Unaffected:**

1. The integration of six LAPOP waves with AidData's geospatial dataset of Chinese development finance (4,318 respondents in 499 municipalities).
2. The case-study material on the Belo Monte UHV transmission line and the China–Brazil Science and Technology Backyard, and its description of local evaluation mechanisms. However, the case findings can **no longer** be presented as corroborating the quantitative results, nor generalised to Brazil as a whole.

### 4. Corrected results

Correction: the dependent variable is reversed throughout as `china_trust = 5 − mil10a` (1 = not at all trustworthy … 4 = very trustworthy).

#### 4.1 Direct correction (original specification, plus survey-year fixed effects and city-clustered standard errors)

| Model | `aid_n` coefficient | SE | p | N |
|---|---|---|---|---|
| Original (uncorrected coding) | +0.038 | 0.012 | 0.001 | 3,871 |
| Corrected direction, pooled OLS | −0.038 | 0.012 | 0.001 | 3,871 |
| + year FE, city-clustered SE | +0.007 | 0.009 | 0.43 | 3,842 |
| + year FE + log GDP per capita | +0.016 | 0.010 | 0.10 | 3,805 |
| + year and city FE | −0.034 | 0.017 | 0.046 | 3,564 |
| `if_aid`, year FE | +0.011 | 0.038 | 0.77 | 3,842 |
| Placebo: trust in US government | +0.007 | 0.012 | 0.55 | 3,842 |

| Formal interaction tests of the original heterogeneity claims (year FE, city-clustered SE) | Coefficient | p |
|---|---|---|
| `aid_n` × less-developed city | −0.011 | 0.78 |
| `aid_n` × frequent news consumption | −0.012 | 0.60 |
| `aid_n` × rural | −0.047 | 0.68 |

Notes:
- With the corrected direction, pooled OLS shows a significant **negative** association. However, trust in China declined over the survey period (annual mean 2.63 in 2017, 1.96 in 2023) while Chinese projects accumulated. The association disappears once survey-year fixed effects are added, indicating that the pooled result mainly reflects a common time trend.
- Only the specification with city fixed effects is marginally significant and negative (p = 0.046); no other specification supports it, so it is not treated as a robust finding.

#### 4.2 Pre-registered extended analyses

To avoid specification searching after the corrected results were known, the author committed the specifications, inference methods and reporting rules for the extended analyses to `ANALYSIS_PLAN.md` on 2026-10-12, before running them. Results (main sample N = 4,318; Holm correction for multiple testing):

| Test | Estimate | 95% CI | Holm-adjusted p |
|---|---|---|---|
| Ordered logit, `aid_n` (log-odds) | 0.016 | [−0.020, 0.052] | 1.00 |
| Completed projects within 50 km | 0.005 | [−0.010, 0.021] | 1.00 |
| Energy/industry projects − social-sector projects | −0.010 | [−0.060, 0.041] | 1.00 |
| Completed vs committed-but-not-completed project locations | 0.064 | [−0.026, 0.153] | 0.67 |
| Event study (Sun & Abraham), average post-period effect | 0.122 | [−0.036, 0.281] | 0.66 |

- None of the five tests is significant. Results are unchanged using the sample that answered both items, dropping 2023, or using 25 km or 100 km radii.
- The event study's joint pre-trend test is significant (F(2, 492) = 3.41, p = 0.034): municipalities that later received projects already had higher trust in China **before** project completion. The event-study estimates are therefore not interpreted causally. This also suggests that the association observed in the thesis may partly reflect project siting rather than project effects.
- The seven deviations from the plan and their rationale are listed in Section 8 of `ANALYSIS_PLAN.md`.

### 5. Corrected conclusions

1. There is no robust evidence that Chinese development finance projects are associated with Brazilians' trust in the Chinese government. The confidence intervals are narrow: each additional completed project within 50 km changes trust (1–4 scale) by no more than about +0.02 or −0.01 points.
2. Changes in trust over the survey period are driven mainly by nationwide time trends rather than local project exposure.
3. There are signs that project siting correlates with pre-existing local attitudes toward China; future work needs stronger causal identification.
4. None of the three heterogeneity findings in the thesis holds.
5. The case studies show positive local evaluations in specific communities and project types, but these cannot be generalised into an aggregate "soft-power return".

### 6. Further notes

- **Sample definition**: the thesis reports N = 4,318, which corresponds to respondents with a non-missing China item. The regressions in the original script `re_ana.R` additionally required a non-missing US item, giving N = 3,973. The corrected analysis uses 4,318 as the main sample and 3,973 as a robustness check; conclusions are the same.
- **Question wording**: in 2023 the item asks about the trustworthiness of "China"; earlier waves ask about "the Chinese government". Conclusions are unchanged when 2023 is excluded.
- **Municipal coordinates**: the spatial-exposure analysis uses municipal seat coordinates from kelvins/municipios-brasileiros (IBGE-sourced, MIT licence).

### 7. Replication files

All on the `correction` branch of this repository:

| File | Content |
|---|---|
| `lapop_12.R` … `lapop_23.R`, `re_ana.R` | Original thesis version, unchanged |
| `re_ana_corrected.R`, `pixi.toml` | Corrected analysis in R; run with `pixi run corrected` |
| `re_ana_corrected_py.py` | The same corrected analysis in Python (pyfixest) |
| `ANALYSIS_PLAN.md` | Pre-registered plan, deviation log, results summary |
| `build_plan_data.py`, `run_plan_v1.py` | Data construction and estimation for the extended analyses |
| `results/` | All corrected results |

### 8. Timeline

| Date | Event |
|---|---|
| 2025-05-22 | Degree obtained (date on the USP diploma) |
| 2026-07-26 | Dependent-variable coding issue identified during review; public access to the repository restricted |
| 2026-10-12 | Direct correction completed; pre-registered plan committed and run; this erratum drafted |
