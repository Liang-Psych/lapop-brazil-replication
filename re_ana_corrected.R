# =============================================================================
# re_ana_corrected.R — 修正版分析（Corrected analysis）
#
# 背景 / Background
#   LAPOP 题目 mil10a（中国政府可信度）与 mil10e（美国政府可信度）在
#   2012–2023 六轮中的原始量表均为：
#       1 = 非常可信  2 = 有些可信  3 = 不太可信  4 = 完全不可信
#   原分析（re_ana.R）直接使用原始取值，即“数值越大越不信任”，
#   但论文按“数值越大越积极”解读。本脚本统一反转为：
#       china_trust = 5 - mil10a   （越大越信任）
#       us_trust    = 5 - mil10e
#
#   原始脚本 lapop_XX.R / re_ana.R 保持不变，作为原论文版本的记录。
#
# 输入 / Inputs : bra_lapop_{12,14,17,19,21,23}.txt（由 lapop_XX.R 导出）
#                 PIB_2010-2021.xlsx
# 输出 / Outputs: results/ 目录下的表格
#
# 运行 / Run    : pixi run corrected   （或在仓库根目录 Rscript re_ana_corrected.R）
# =============================================================================

suppressPackageStartupMessages({
  library(dplyr)
  library(readr)
  library(readxl)
  library(fixest)
})

dir.create("results", showWarnings = FALSE)

# ---- 1. 读取各轮数据（相对路径） -------------------------------------------
keep <- c("year", "state_name", "city_name", "china_attitude", "america_attitude",
          "gender", "age", "pe_fina", "edu", "urban_rural", "if_aid", "aid_n",
          "aid_time", "presidential_approval_rating", "ing4", "news_read")

read_wave <- function(y) {
  read_delim(sprintf("bra_lapop_%s.txt", y), delim = " ",
             show_col_types = FALSE, progress = FALSE) |>
    select(all_of(keep)) |>
    mutate(across(c(china_attitude, america_attitude), as.numeric))
}
raw <- bind_rows(lapply(c(12, 14, 17, 19, 21, 23), read_wave))

# ---- 2. 城市人均 GDP（与原分析相同，2021 年） -------------------------------
pib_21 <- read_excel("PIB_2010-2021.xlsx") |>
  filter(Ano == 2021) |>
  select(state_name = "Nome da Unidade da Federação",
         city_name  = "Nome do Município",
         gdp_per    = matches("Produto Interno Bruto per capita")) |>
  mutate(across(c(state_name, city_name),
                ~ stringi::stri_trans_general(tolower(.x), "Latin-ASCII")))
stopifnot(ncol(pib_21) == 3, is.numeric(pib_21$gdp_per))

dev_cut <- 42893.73   # 与原分析相同的发展水平分界

dat <- raw |>
  rename(democracy_prefer = ing4) |>
  left_join(pib_21, by = c("state_name", "city_name")) |>
  mutate(
    news_read   = as.integer(news_read %in% c(1, 2)),
    log_gdp_per = log(gdp_per),
    low_dev     = as.integer(gdp_per < dev_cut),
    rural       = as.integer(urban_rural == 2),
    city        = paste(state_name, city_name, sep = "|"),
    # ---- 修正后的因变量 ----
    china_trust = 5 - china_attitude,
    us_trust    = 5 - america_attitude
  )

# 样本 A：与原论文一致（中美两题均非缺失）
sampA <- dat |> filter(!is.na(china_attitude), !is.na(america_attitude))
# 样本 B：只要求对华题非缺失（稳健性）
sampB <- dat |> filter(!is.na(china_attitude))

sink("results/corrected_models.txt", split = TRUE)
cat("=== 样本量 ===\n")
cat("样本A（原论文口径）N =", nrow(sampA), " 城市数 =", n_distinct(sampA$city), "\n")
cat("样本B（仅对华题）  N =", nrow(sampB), "\n\n")
print(table(sampA$year))

cat("\n=== 对华信任均值（1–4，越大越信任）按年份 ===\n")
print(sampA |> group_by(year) |>
        summarise(n = n(), china_trust = mean(china_trust),
                  us_trust = mean(us_trust), mean_aid_n = mean(aid_n)))

# ---- 3. 回归 ----------------------------------------------------------------
ctrl <- "gender + age + edu + pe_fina + urban_rural + presidential_approval_rating + democracy_prefer + news_read"
f <- function(lhs, rhs, fe = NULL) {
  as.formula(paste(lhs, "~", rhs, "+", ctrl, if (!is.null(fe)) paste("|", fe)))
}

m <- list(
  "原始编码 OLS (=re_ana model_12)" = feols(f("china_attitude", "aid_n"), sampA, vcov = "iid"),
  "修正 OLS"                         = feols(f("china_trust", "aid_n"), sampA, vcov = "iid"),
  "修正 +年份FE"                     = feols(f("china_trust", "aid_n", "year"), sampA, cluster = ~city),
  "修正 +年份FE +logGDP"             = feols(f("china_trust", "aid_n + log_gdp_per", "year"), sampA, cluster = ~city),
  "修正 +年份FE +城市FE"             = feols(f("china_trust", "aid_n", "year + city"), sampA, cluster = ~city),
  "修正 if_aid +年份FE"              = feols(f("china_trust", "if_aid", "year"), sampA, cluster = ~city),
  "修正 样本B +年份FE"               = feols(f("china_trust", "aid_n", "year"), sampB, cluster = ~city),
  "安慰剂：对美信任 +年份FE"          = feols(f("us_trust", "aid_n", "year"), sampA, cluster = ~city)
)
cat("\n=== 主模型（城市聚类标准误，除前两列外） ===\n")
print(etable(m, keep = c("aid_n", "if_aid", "log_gdp_per"), digits = 3))

# ---- 4. 异质性：正式交互项检验（替代原分组回归） -----------------------------
h <- list(
  "× 欠发达城市" = feols(as.formula(paste("china_trust ~ aid_n * low_dev +", ctrl, "| year")),
                         sampA, cluster = ~city),
  "× 常看新闻"   = feols(as.formula(paste("china_trust ~ aid_n * news_read +",
                                         sub(" \\+ news_read", "", ctrl), "| year")),
                         sampA, cluster = ~city),
  "× 农村"       = feols(as.formula(paste("china_trust ~ aid_n * rural +",
                                         sub("urban_rural \\+ ", "", ctrl), "| year")),
                         sampA, cluster = ~city)
)
cat("\n=== 异质性：交互项（年份FE，城市聚类SE） ===\n")
print(etable(h, keep = c("aid_n", "low_dev", "news_read", "rural"), digits = 3))
sink()

# 关键系数另存 CSV，便于写勘误
coef_tab <- bind_rows(lapply(names(m), function(nm) {
  ct <- coeftable(m[[nm]])
  v  <- intersect(c("aid_n", "if_aid"), rownames(ct))[1]
  data.frame(model = nm, term = v, estimate = ct[v, 1], se = ct[v, 2],
             p = ct[v, 4], n = nobs(m[[nm]]))
}))
write_csv(coef_tab, "results/corrected_key_coefs.csv")
cat("\n已写出 results/corrected_models.txt 与 results/corrected_key_coefs.csv\n")
