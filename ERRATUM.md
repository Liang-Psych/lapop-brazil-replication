# Erratum

**Thesis**: Xu, L. (2025). *The Impact of Chinese Development Finance on Brazilian Public Attitudes Toward China*. Master's thesis, joint degree programme of China Agricultural University and the Luiz de Queiroz College of Agriculture (ESALQ), University of São Paulo.

**Version**: v1.4 · 2026-10-16

**Replication materials**: https://github.com/Liang-Psych/lapop-brazil-replication

**Issue identified**: 2026-07-26

---

## 1. Summary

The dependent variable in the original thesis, attitudes toward China, was interpreted in the opposite direction of its coding. After correction, the thesis's central finding does not hold: **there is no robust evidence that Chinese development finance projects are associated with Brazilians' trust in the Chinese government**, in either direction. The three heterogeneous effects reported in the thesis also do not hold. The data assembly and the two case studies are unaffected.

## 2. Nature of the error

- **Variable**: AmericasBarometer (LAPOP) item `mil10a`, trustworthiness of the Chinese government.
- **Original scale**: in all six waves (2012, 2014, 2017, 2019, 2021, 2023): 1 = very trustworthy, 2 = somewhat trustworthy, 3 = not very trustworthy, 4 = not at all trustworthy.
- **Error**: the scripts `lapop_12.R` to `lapop_23.R` used the raw values (`china_attitude = mil10a`), so **higher values meant less trust**, while the thesis interpreted higher values as more favourable attitudes. The comparison variable `mil10e` (trustworthiness of the US government) had the same issue.
- **Scope**: all six waves are affected, in the same direction. "Don't know" and "No response" were correctly treated as missing and did not enter the 1–4 scale.
- **Nature**: a technical error in interpreting the variable's direction. It involves no data manipulation or selective reporting. The original code, outputs and version history are preserved in the replication repository (https://github.com/Liang-Psych/lapop-brazil-replication); under LAPOP's licence terms the survey data are not redistributed here and can be downloaded from LAPOP (see README).
- **The thesis numbers replicate exactly**: re-running every model in Tables 2–6 with the raw coding reproduces each coefficient and p-value reported in the thesis (see Section 4.1), confirming that the thesis results come from this unreversed variable.
- **A related issue**: the control variable `m1` (evaluation of the president's performance, labelled `presidential_approval_rating` in the thesis) is also coded 1 = very good … 5 = very bad in the raw data, so higher values mean a worse evaluation, whereas the thesis interprets it as approval. This does not affect the estimates for Chinese projects, but the thesis's interpretation of this control is also incorrect.

### How the error arose: the official online tool and the raw data use opposite directions

LAPOP's official online visualisation tool (the [AmericasBarometer Tableau dashboard](https://public.tableau.com/app/profile/lapop.central/viz/LAPOPV3_4/Combination)) rescales `mil10a` to 0–100 **so that higher means more trustworthy**: "very trustworthy" maps to 100 and "not at all trustworthy" to 0. The page does not indicate that this direction is the reverse of the raw data file.

The author relied on this tool to understand the variable during research design, and the thesis describes the scale in the tool's direction (1 = not at all trustworthy … 4 = very trustworthy). The analysis, however, used the raw Stata file downloaded from LAPOP, in which 1 = very trustworthy and 4 = not at all trustworthy, and the code did not reverse it. The thesis text and the code therefore ran in opposite directions.

To confirm that both describe the same data, the author rescaled the raw `mil10a` the way the dashboard does (`(4 − mil10a) / 3 × 100`, survey-weighted) and compared Brazil's round means:

| Round | Official dashboard | Raw data, rescaled |
|---|---|---|
| 2012 | 45.2 | 46.1 |
| 2014 | 37.0 | 37.9 |
| 2016/17 | 53.7 | 53.7 |
| 2018/19 | 46.2 | 46.2 |
| 2021 | 36.5 | 36.5 |
| 2023 | 31.1 | 31.1 |
| N | 4,328 | 4,328 |

Four rounds match exactly and the sample sizes are identical. The 2012 and 2014 values differ by about one point, probably because the dashboard uses a different weight variable.

**Lesson**: with survey data, the value labels in the raw data file and the official codebook are authoritative, not the display direction of an online visualisation tool, and scale direction should be checked wave by wave before analysis.

## 3. Affected and unaffected content

Page numbers refer to the printed page numbers of the thesis.

**Affected, to be withdrawn or corrected:**

| Location | Original content | Action |
|---|---|---|
| Chinese abstract (中文摘要, pp. I–II), ABSTRACT (pp. III–IV), RESUMO (pp. V–VI) | Significant positive association between Chinese development finance and attitudes toward China, implying soft-power returns; stronger effects in less-developed cities; more positive responses among frequent news consumers | Withdrawn |
| Section 4.2.1 (p. 27) | Scale described as "1 = Not at all trustworthy … 4 = Very trustworthy" | This matches the official online tool but is the reverse of the variable actually used. In the analysis, 1 = very trustworthy … 4 = not at all trustworthy |
| Section 4.2.1, Figure 1 and text (p. 28) | Figure 1 is a screenshot of the official dashboard and its data are correct; "37.9% view the Chinese government as somewhat or very trustworthy" is also correct. The description of attitudes as "predominantly neutral to moderately positive" and "generally favorable" is not accurate | Corrected: about 62.0% of respondents view the Chinese government as not very or not at all trustworthy |
| Section 4.3, Table 1 and text (p. 31) | Mean `china_attitude` of 2.79 described as "generally positive" | 2.79 is on the raw coding (higher = less trust). On a higher-is-more-trust scale the mean is 2.21 (1–4), leaning toward distrust |
| Section 5.1, Table 2 and text (pp. 35–36) | Positive main effect supporting Hypothesis 1; interpretation of age, education, presidential approval and democratic preference | Main effect withdrawn. Because the dependent variable is reversed, all control-variable interpretations are reversed too, and the presidential evaluation item is itself reverse-coded (see Section 2); these interpretations are withdrawn |
| Section 5.2, Table 3 and unreported robustness checks (pp. 37–38) | `if_aid` results; claims that city fixed effects, ordered logit, alternative clustering and bootstrapping leave the results unchanged | Withdrawn |
| Section 5.3, Tables 4–6 (pp. 38–42) | Urban/rural, city development level and media exposure heterogeneity; support for Hypotheses 2a and 2b | Withdrawn |
| Section 5.4 (pp. 42–45) | Evidence for the direct-benefit, information and symbolic-politics mechanisms based on the above | Parts relying on the quantitative results withdrawn |
| Section 5.5 (pp. 45–47) | Implications for China's development finance strategy | Withdrawn |
| Sections 6.3–6.5 (pp. 54–56) | Statements that the cases corroborate or verify the quantitative main effect and the development-level and information moderating effects | Statements of corroboration withdrawn; the case descriptions remain |
| Section 7.1 (pp. 57–58) | Findings one and two, and the statement in finding three that the cases support the quantitative results | Withdrawn |
| Section 7.2 (pp. 58–59) | Theoretical contributions that rely on the quantitative conclusions | Corresponding parts withdrawn |
| Section 7.4 (pp. 61–62) | Parts of policy implications one, two and four that rely on the quantitative results | Corresponding parts withdrawn |

**Table presentation issue (unrelated to the coding error, corrected here as well)**: in Tables 2–6, the starred number next to each variable is the p-value and the number in parentheses is the regression coefficient; standard errors are not reported. For example, in Table 2, Model 1, "0.000663 \*\*\*" is the p-value and "(0.03713)" is the coefficient. The coefficients cited in the text match the numbers in parentheses.

**Unaffected:**

1. The integration of six LAPOP waves with AidData's geospatial dataset of Chinese development finance (4,318 respondents in 499 municipalities).
2. The literature review and theoretical framework in Chapters 2 and 3, as hypotheses to be tested.
3. The field material for the two cases in Chapter 6 and its description of local evaluation mechanisms. However, the case findings can **no longer** be presented as corroborating the quantitative results, nor generalised to Brazil as a whole.
4. Section 7.3 already noted the risk of reverse causality, namely that cities with more favourable attitudes toward China may be more likely to receive projects. The corrected analysis can neither confirm nor rule out this concern.

## 4. Corrected results

Correction: the dependent variable is reversed throughout as `china_trust = 5 − mil10a` (1 = not at all trustworthy … 4 = very trustworthy).

### 4.1 Replication and direction correction of Tables 2–6

Re-running the thesis models on the thesis sample (respondents with a non-missing China item, pooled OLS) with the raw coding reproduces the reported coefficients exactly; after correcting the direction, every coefficient changes sign:

| Thesis table | Model | Reported coefficient | Replicated (raw coding) | Corrected direction | p | N as reported | Actual N |
|---|---|---|---|---|---|---|---|
| Table 2 | Model 1 | 0.037 | 0.037 | −0.037 | 0.0007 | 4,316 | 4,318 |
| Table 2 | Model 2 | 0.040 | 0.040 | −0.040 | 0.0004 | 4,190 | 4,200 |
| Table 2 | Model 3 | 0.034 | 0.034 | −0.034 | 0.003 | 4,120 | 4,131 |
| Table 3 | Model 1 (`if_aid`) | 0.114 | 0.114 | −0.114 | 0.001 | 4,316 | 4,318 |
| Table 3 | Model 2 | 0.122 | 0.122 | −0.122 | 0.0008 | 4,190 | 4,200 |
| Table 3 | Model 3 | 0.104 | 0.104 | −0.104 | 0.006 | 4,120 | 4,131 |
| Table 4 | Urban | 0.032 | 0.032 | −0.032 | 0.006 | 3,665 | 3,675 |
| Table 4 | Rural | 0.165 | 0.165 | −0.165 | 0.043 | 446 | 456 |
| Table 5 | Higher-development cities | 0.023 | 0.023 | −0.023 | 0.066 | 1,872 | 1,882 |
| Table 5 | Lower-development cities | 0.104 | 0.104 | −0.104 | 0.001 | 2,239 | 2,249 |
| Table 6 | Frequent news exposure | 0.032 | 0.032 | −0.032 | 0.007 | 3,756 | 3,766 |
| Table 6 | Infrequent news exposure | 0.065 | 0.065 | −0.065 | 0.15 | 355 | 365 |

- The "sample size" reported in the thesis tables is in fact the residual degrees of freedom (N minus the number of parameters); for example, Table 2, Model 2: 4,200 − 10 = 4,190. After this adjustment it matches the replication exactly.
- Replication script: `replicate_thesis_tables.py`; results in `results/thesis_tables_replication.csv`.

With the corrected direction, all pooled OLS estimates are negative, but none of these models controls for survey year. The table below adds survey-year fixed effects and city-clustered standard errors (sample: respondents who answered both the China and US items; conclusions are the same with the 4,318-respondent sample, e.g. +0.006, p = 0.54 in the year fixed-effects model):

| Model (corrected direction) | `aid_n` coefficient | SE | p | N |
|---|---|---|---|---|
| Pooled OLS + controls | −0.038 | 0.012 | 0.001 | 3,871 |
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

### 4.2 Pre-specified extended analyses

To avoid specification searching after the corrected results were known, the author committed the specifications, inference methods and reporting rules for the extended analyses to `ANALYSIS_PLAN.md` on 2026-10-12, before running them. The plan was not registered on an external platform, and some corrected results had already been seen when it was written; the plan lists those results. Results (main sample N = 4,318; Holm correction for multiple testing):

| Test | Estimate | 95% CI | Holm-adjusted p |
|---|---|---|---|
| Ordered logit, `aid_n` (log-odds) | 0.016 | [−0.020, 0.052] | 1.00 |
| Completed projects within 50 km | 0.005 | [−0.010, 0.021] | 1.00 |
| Energy/industry projects − social-sector projects | −0.010 | [−0.060, 0.041] | 1.00 |
| Completed vs committed-but-not-completed project locations | 0.064 | [−0.026, 0.153] | 0.67 |
| Event study (Sun & Abraham), average post-period effect | 0.122 | [−0.036, 0.281] | 0.66 |

- None of the five tests is significant. Results are unchanged using the sample that answered both items, dropping 2023, or using 25 km or 100 km radii.
- The event study's joint pre-trend test is significant (F(2, 492) = 3.41, p = 0.034). Because the model includes municipality fixed effects, the test compares changes within municipalities, not levels across them: relative to municipalities without projects, trust in municipalities that later received projects was higher five or more years before completion than in the year before completion. The parallel-trends assumption therefore does not hold, and the event-study estimates are not interpreted causally. The reference period (the year before completion) contains only 55 respondents in 16 municipalities, so the test itself is imprecise. It does not show whether projects were sited in municipalities with more favourable attitudes.
- The seven deviations from the plan and their rationale are listed in Section 8 of `ANALYSIS_PLAN.md`.

## 5. Corrected conclusions

1. There is no robust evidence that Chinese development finance projects are associated with Brazilians' trust in the Chinese government. The confidence intervals are narrow: each additional completed project within 50 km changes trust (1–4 scale) by no more than about +0.02 or −0.01 points.
2. Changes in trust over the survey period are driven mainly by nationwide time trends rather than local project exposure.
3. These data cannot show whether project siting is related to pre-existing local attitudes toward China; the pre-trends in the event study show that stronger causal identification is needed.
4. None of the three heterogeneity findings in the thesis holds.
5. The case studies show positive local evaluations in specific communities and project types, but these cannot be generalised into an aggregate "soft-power return".

## 6. Further notes

- **Sample definition**: Tables 2–6 of the thesis use respondents with a non-missing China item (N = 4,318), as confirmed by the replication in Section 4.1. The archived script `re_ana.R` additionally requires a non-missing US item (N = 3,973), which differs from the sample actually used in the thesis; the replication in Section 4.1 is authoritative. The corrected analysis uses 4,318 as the main sample and 3,973 as a robustness check; conclusions are the same.
- **Question wording**: in 2023 the item asks about the trustworthiness of "China"; earlier waves ask about "the Chinese government". Conclusions are unchanged when 2023 is excluded.
- **Municipal coordinates**: the spatial-exposure analysis uses municipal seat coordinates from kelvins/municipios-brasileiros (IBGE-sourced, MIT licence).

## 7. Replication files

All in the replication repository https://github.com/Liang-Psych/lapop-brazil-replication (LAPOP survey data must be downloaded separately; see the repository README):

| File | Content |
|---|---|
| `lapop_12.R` … `lapop_23.R`, `re_ana.R` | Original thesis version, unchanged |
| `re_ana_corrected.R`, `pixi.toml` | Corrected analysis in R; run with `pixi run corrected` |
| `re_ana_corrected_py.py` | The same corrected analysis in Python (pyfixest) |
| `ANALYSIS_PLAN.md` | Pre-specified plan for the extended analyses, deviation log, results summary |
| `build_plan_data.py`, `run_plan_v1.py` | Data construction and estimation for the extended analyses |
| `replicate_thesis_tables.py` | Replication of thesis Tables 2–6 and their corrected-direction versions |
| `check_dashboard.py` | Direction check of raw data against the official dashboard |
| `results/` | All corrected results |

## 8. Timeline

| Date | Event |
|---|---|
| 2025-05-22 | Degree obtained (date on the USP diploma) |
| 2026-07-26 | Dependent-variable coding issue identified during review; public access to the original repository restricted |
| 2026-10-12 | Direct correction completed; pre-specified plan committed and run; this erratum drafted |
| 2026-10-16 | Cause identified: the official online tool and the raw data use opposite scoring directions; Tables 2–6 fully replicated; affected sections listed against the full thesis text; erratum finalised |

## 9. Use of AI tools

In preparing this erratum, the author used an AI assistant (Claude, developed by Anthropic) to help check the coding direction of the raw data, write and check the code for the replication and corrected analyses, compile the affected content against the full thesis text, and draft the text of this erratum. All analyses were verified by the author and can be reproduced independently with the code in the replication repository. The author takes full responsibility for the content of this erratum.

<div class="pb"></div>

# 勘误说明

**论文**：许亮（2025）。《中国发展融资对巴西公众对华态度的影响》（*The Impact of Chinese Development Finance on Brazilian Public Attitudes Toward China*）。硕士学位论文，中国农业大学与圣保罗大学路易斯·德·凯罗斯农学院（ESALQ）双学位项目。

**版本**：v1.4 · 2026-10-16

**复现材料**：https://github.com/Liang-Psych/lapop-brazil-replication

**问题发现日期**：2026-07-26

---

## 1. 摘要

原论文的因变量“对华态度”编码方向与解读方向相反。修正后，原论文的核心结论不成立：**没有稳健证据表明中国发展融资项目与巴西民众对中国政府的信任相关**，无论正向还是负向。原论文报告的三项异质性效应也不成立。数据整合工作与两个案例研究不受影响。

## 2. 错误的性质

- **涉及变量**：美洲晴雨表（LAPOP AmericasBarometer）题目 `mil10a`，即中国政府的可信度。
- **原始量表**：2012、2014、2017、2019、2021、2023 六轮均为：1 = 非常可信，2 = 有些可信，3 = 不太可信，4 = 完全不可信。
- **错误**：分析脚本 `lapop_12.R` 至 `lapop_23.R` 直接使用原始取值（`china_attitude = mil10a`），因此**数值越大表示越不信任**；但论文将其解读为数值越大态度越积极。对照变量 `mil10e`（美国政府的可信度）存在同样的问题。
- **范围**：六轮全部受影响，方向一致。“不知道”和“拒答”已正确设为缺失值，没有混入 1 到 4 分。
- **性质**：这是变量方向解读上的技术错误，不涉及数据篡改或选择性报告。原始代码、结果与版本记录均保留在复现仓库（https://github.com/Liang-Psych/lapop-brazil-replication）中；LAPOP 原始调查数据按其许可条款不随仓库分发，可从 LAPOP 官网下载（见 README）。
- **论文数字可完整复现**：用原始编码重跑论文表 2 至表 6 的全部模型，每个系数和 p 值都与论文一致（见 4.1 节），证明论文结果正是来自这一未反转的变量。
- **同类问题**：控制变量 `m1`（总统执政评价，论文中记为 `presidential_approval_rating`）在原始数据中同样为 1 = 很好 … 5 = 很差，数值越大评价越差，而论文按“支持率”解读。它不影响中国项目系数的估计，但论文对该控制变量的解读同样有误。

### 错误成因：官方在线工具与原始数据的计分方向相反

LAPOP 官方的在线数据可视化工具（[AmericasBarometer Tableau 仪表盘](https://public.tableau.com/app/profile/lapop.central/viz/LAPOPV3_4/Combination)）把 `mil10a` 重新计分为 0 到 100，**方向为“越高越可信”**：“非常可信”对应 100，“完全不可信”对应 0。页面上没有说明这一方向与原始数据文件相反。

作者在研究设计阶段参照该工具理解变量，论文中对量表的描述（1 = 完全不可信 … 4 = 非常可信）与该工具的方向一致。但分析使用的是从 LAPOP 下载的原始 Stata 数据文件，其中 1 = 非常可信、4 = 完全不可信，代码中没有反转。论文的文字描述与实际代码因此方向相反。

为确认二者是同一批数据，作者将原始 `mil10a` 按官方工具的口径换算（`(4 − mil10a) / 3 × 100`，使用调查权重）并与仪表盘巴西各轮均值对照：

| 轮次 | 官方仪表盘 | 原始数据换算 |
|---|---|---|
| 2012 | 45.2 | 46.1 |
| 2014 | 37.0 | 37.9 |
| 2016/17 | 53.7 | 53.7 |
| 2018/19 | 46.2 | 46.2 |
| 2021 | 36.5 | 36.5 |
| 2023 | 31.1 | 31.1 |
| 样本量 | 4,328 | 4,328 |

四轮完全一致，样本量相同。2012 年与 2014 年约差 1 分，可能是官方采用的权重变量与本文不同。

**教训**：使用调查数据时，应以原始数据文件中的值标签（value labels）和官方编码手册为准，而不是在线可视化工具的显示方向，并在分析前逐轮核对量表方向。

## 3. 受影响与不受影响的内容

文中页码均为论文正文所印页码。

**受影响，应撤回或更正：**

| 位置 | 原内容 | 处理 |
|---|---|---|
| 中文摘要（第 I–II 页）、ABSTRACT（第 III–IV 页）、RESUMO（第 V–VI 页） | 中国发展融资项目与对华态度显著正相关、产生软实力回报；欠发达城市效应更强；常接触新闻者反应更积极 | 撤回 |
| 4.2.1 节（第 27 页） | 量表说明“1 = Not at all trustworthy … 4 = Very trustworthy” | 该说明与官方在线工具方向一致，但与分析实际使用的变量相反。分析中的变量为 1 = 非常可信 … 4 = 完全不可信 |
| 4.2.1 节图 1 及说明（第 28 页） | 图 1 为官方仪表盘截图，数据正确；“37.9% 认为有些可信或非常可信”也正确。但“态度主要为中性到温和正面”“总体正面”的描述不准确 | 更正为：约 62.0% 的受访者认为中国政府“不太可信”或“完全不可信” |
| 4.3 节表 1 及说明（第 31 页） | `china_attitude` 均值 2.79 被解读为“总体正面” | 2.79 为原始编码（越大越不信任）。按“越大越信任”计，均值为 2.21（1–4 分），偏向不信任 |
| 5.1 节表 2 及说明（第 35–36 页） | 主效应为正，支持假设 1；年龄、教育、总统支持率、民主偏好与对华态度关系的解读 | 主效应撤回；因变量方向相反，所有控制变量的解读随之反转，其中总统执政评价本身也是反向计分（见第 2 节），这些解读一并撤回 |
| 5.2 节表 3 及文中未列表的稳健性检验（第 37–38 页） | `if_aid` 结果；“城市固定效应、有序 logit、其他聚类与 bootstrap 均不改变结论” | 撤回 |
| 5.3 节表 4–6（第 38–42 页） | 城乡、城市发展水平、媒体接触三项异质性分析；假设 2a、2b 获得支持 | 撤回 |
| 5.4 节（第 42–45 页） | 以上述结果论证直接收益、信息、象征政治三个机制 | 撤回依赖定量结果的部分 |
| 5.5 节（第 45–47 页） | 对中国发展融资策略的建议 | 撤回 |
| 6.3–6.5 节（第 54–56 页） | 案例“印证”“验证”定量研究的主效应及发展水平、信息传播调节效应 | 撤回“印证定量结果”的表述；案例描述本身保留 |
| 7.1 节（第 57–58 页） | 研究发现第一、二点，及第三点中“案例支持定量结果” | 撤回 |
| 7.2 节（第 58–59 页） | 依赖上述定量结论的理论贡献 | 撤回相应部分 |
| 7.4 节（第 61–62 页） | 第一、二、四点政策启示中依赖定量结果的部分 | 撤回相应部分 |

**表格呈现问题（与编码错误无关，一并更正）**：表 2 至表 6 中，变量名右侧带星号的数字是 p 值，括号内的数字是回归系数，表中没有报告标准误。例如表 2 模型 1 的“0.000663 \*\*\*”是 p 值，“(0.03713)”是系数。正文引用的系数与括号内的数字一致。

**不受影响：**

1. LAPOP 六轮调查与 AidData 中国发展融资地理空间数据的整合（4,318 名受访者、499 个城市）。
2. 第 2、3 章的文献综述与理论框架（作为有待检验的假设）。
3. 第 6 章两个案例的田野资料及其对当地评价机制的描述。但案例结论**不能**再被表述为与定量结果相互印证，也不能推广为巴西整体的情况。
4. 7.3 节已指出“对华态度原本较好的城市可能更容易获得项目”的反向因果风险。修正分析既不能证实也不能排除这一担忧。

## 4. 修正后的结果

修正方法：将因变量统一反转为 `china_trust = 5 − mil10a`（1 = 完全不可信 … 4 = 非常可信）。

### 4.1 论文表 2 至表 6 的复现与方向修正

用论文的模型和样本（对华题非缺失，混合 OLS）重跑，原始编码下的系数与论文完全一致；修正方向后，所有系数符号反转：

| 论文表格 | 模型 | 论文报告系数 | 复现（原始编码） | 修正方向后 | p | 论文所列 N | 实际 N |
|---|---|---|---|---|---|---|---|
| 表 2 | 模型 1 | 0.037 | 0.037 | −0.037 | 0.0007 | 4,316 | 4,318 |
| 表 2 | 模型 2 | 0.040 | 0.040 | −0.040 | 0.0004 | 4,190 | 4,200 |
| 表 2 | 模型 3 | 0.034 | 0.034 | −0.034 | 0.003 | 4,120 | 4,131 |
| 表 3 | 模型 1（`if_aid`） | 0.114 | 0.114 | −0.114 | 0.001 | 4,316 | 4,318 |
| 表 3 | 模型 2 | 0.122 | 0.122 | −0.122 | 0.0008 | 4,190 | 4,200 |
| 表 3 | 模型 3 | 0.104 | 0.104 | −0.104 | 0.006 | 4,120 | 4,131 |
| 表 4 | 城市 | 0.032 | 0.032 | −0.032 | 0.006 | 3,665 | 3,675 |
| 表 4 | 农村 | 0.165 | 0.165 | −0.165 | 0.043 | 446 | 456 |
| 表 5 | 高发展城市 | 0.023 | 0.023 | −0.023 | 0.066 | 1,872 | 1,882 |
| 表 5 | 低发展城市 | 0.104 | 0.104 | −0.104 | 0.001 | 2,239 | 2,249 |
| 表 6 | 常看新闻 | 0.032 | 0.032 | −0.032 | 0.007 | 3,756 | 3,766 |
| 表 6 | 少看新闻 | 0.065 | 0.065 | −0.065 | 0.15 | 355 | 365 |

- 论文表格中的“sample size”实为残差自由度（N 减去参数个数），例如表 2 模型 2 为 4,200 − 10 = 4,190。换算后与复现样本完全一致。
- 复现脚本：`replicate_thesis_tables.py`，结果见 `results/thesis_tables_replication.csv`。

修正方向后，混合 OLS 全部呈负相关，但这些模型都没有控制调查年份。下表补充年份固定效应和城市聚类标准误（样本为对华、对美两题均作答者；以 4,318 人为样本时结论相同，例如年份固定效应模型系数为 +0.006，p = 0.54）：

| 模型（修正方向） | `aid_n` 系数 | 标准误 | p | N |
|---|---|---|---|---|
| 混合 OLS + 控制变量 | −0.038 | 0.012 | 0.001 | 3,871 |
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

### 4.2 预先确定的扩展分析

为避免在已知结果后进行规格搜索，作者于 2026-10-12 先将扩展分析的规格、推断方法和结论措辞规则写入 `ANALYSIS_PLAN.md` 并提交到版本库，之后才运行。该计划没有在外部平台登记；撰写时作者已看到部分修正结果，计划中逐项列明了这些结果。结果如下（主样本 N = 4,318，Holm 多重检验校正）：

| 检验 | 估计值 | 95% 置信区间 | Holm 校正 p |
|---|---|---|---|
| 有序 logit，`aid_n`（log-odds） | 0.016 | [−0.020, 0.052] | 1.00 |
| 50 公里内已完工项目数 | 0.005 | [−0.010, 0.021] | 1.00 |
| 能源与工业类项目 − 社会领域项目 | −0.010 | [−0.060, 0.041] | 1.00 |
| 已完工 vs 已承诺未完工项目所在地 | 0.064 | [−0.026, 0.153] | 0.67 |
| 事件研究（Sun & Abraham），事后平均效应 | 0.122 | [−0.036, 0.281] | 0.66 |

- 五项均不显著。改用两题均作答的样本、剔除 2023 年、改用 25 或 100 公里范围，结论均不变。
- 事件研究的事前趋势联合检验显著（F(2, 492) = 3.41，p = 0.034）。由于模型包含城市固定效应，该检验比较的是同一城市内部的变化，而不是城市之间的水平差异：与没有项目的城市相比，后来获得项目的城市在完工前 5 年以上的对华信任，相对完工前 1 年偏高。平行趋势假设因此不成立，事件研究结果不作因果解读。作为基准的完工前 1 年只有 16 个城市的 55 名受访者，这一检验本身也不够精确。它不能说明项目是否被选在原本对华态度较好的地方。
- 执行中与计划的 7 处偏离及其理由，见 `ANALYSIS_PLAN.md` 第 8 节。

## 5. 修正后的结论

1. 没有稳健证据表明中国发展融资项目与巴西民众对中国政府的信任相关。置信区间较窄：50 公里内每增加一个已完工项目，对华信任（1 到 4 分）的变化可以排除大于约 +0.02 分或小于约 −0.01 分的效应。
2. 调查期间对华信任的变化主要由全国性的时间趋势驱动，而非地方层面的项目暴露。
3. 现有数据无法判断项目选址是否与当地原有的对华态度相关；事件研究的事前趋势表明，后续研究需要更严格的因果识别设计。
4. 原论文的三项异质性结论均不成立。
5. 案例研究显示，在特定社区和特定类型的项目中可以观察到当地的积极评价；但这些发现不能推广为整体层面的“软实力回报”。

## 6. 其他需要说明的问题

- **样本口径**：论文表 2 至表 6 使用的是“对华题非缺失”的样本（4,318 人），4.1 节的复现已经确认。仓库中归档的 `re_ana.R` 另外要求对美题也非缺失（3,973 人），与论文实际使用的样本不同，应以 4.1 节的复现为准。修正分析以 4,318 为主样本，以 3,973 为稳健性检验，两者结论一致。
- **题目措辞**：2023 年题目为“中国的可信度”，此前各轮为“中国政府的可信度”。剔除 2023 年后结论不变。
- **市镇坐标**：空间暴露分析使用的市镇驻地坐标来自 kelvins/municipios-brasileiros（IBGE 来源，MIT 许可）。

## 7. 复现文件

均位于复现仓库 https://github.com/Liang-Psych/lapop-brazil-replication（LAPOP 原始数据需另行下载，见仓库 README）：

| 文件 | 内容 |
|---|---|
| `lapop_12.R` … `lapop_23.R`、`re_ana.R` | 原论文版本，未作改动 |
| `re_ana_corrected.R`、`pixi.toml` | 修正版分析（R），`pixi run corrected` |
| `re_ana_corrected_py.py` | 同一修正分析的 Python（pyfixest）版本 |
| `ANALYSIS_PLAN.md` | 预先确定的扩展分析计划、偏离记录、结果摘要 |
| `build_plan_data.py`、`run_plan_v1.py` | 扩展分析的数据构建与估计脚本 |
| `replicate_thesis_tables.py` | 复现论文表 2 至表 6 并给出修正方向后的结果 |
| `check_dashboard.py` | 原始数据与官方仪表盘的方向核对 |
| `results/` | 全部修正结果 |

## 8. 时间线

| 日期 | 事项 |
|---|---|
| 2025-05-22 | 获得硕士学位（USP 学位证书所载日期） |
| 2026-07-26 | 复核中发现因变量编码方向问题；原仓库暂停公开访问 |
| 2026-10-12 | 完成直接修正分析；提交预先确定的分析计划并运行；完成本勘误草稿 |
| 2026-10-16 | 查明错误成因：官方在线工具与原始数据计分方向相反；完整复现论文表 2 至表 6；对照论文全文列出受影响的章节；本勘误定稿 |

## 9. AI 工具使用声明

在准备本勘误的过程中，作者使用了 AI 助手（Anthropic 公司的 Claude）辅助以下工作：核对原始数据的编码方向、编写和检查复现与修正分析的代码、对照论文全文整理受影响的内容，以及起草本勘误的文字。所有分析均由作者核验，结果可通过复现仓库中的代码独立复现。作者对本勘误的全部内容负责。
