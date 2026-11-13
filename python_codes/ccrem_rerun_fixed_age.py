#!/usr/bin/env python
# coding: utf-8

# # Park accessibility: CCREM re-run with corrected age coding
# 
# This notebook fixes two problems in `park_accessibility3.ipynb`.
# 
# 1. **Age coding.** The old `parse_group()` gave the 70+ group an age of 35, because it read `7000` as (70 + 0) / 2. The new code uses a fixed lookup table (70+ = 75). In the figures, 65–69 now goes into 60–69, not 70+.
# 2. **Model terms.** Female × Age and Female × Age² are added as main terms. A likelihood-ratio test compares the model with and without them.
# 
# Data: `FINAL_dataset_2019only.csv` (2019).

# ## 0. Imports and settings

# In[1]:


import os
R_HOME = r"C:\Program Files\R\R-4.3.1"
R_BIN = os.path.join(R_HOME, "bin", "x64")
os.environ["R_HOME"] = R_HOME
os.environ["PATH"] = R_BIN + os.pathsep + os.environ["PATH"]
os.add_dll_directory(R_BIN)

import rpy2.robjects as ro
print(ro.r("R.version.string"))
print(ro.r(".libPaths()"))
print(ro.r('library(lme4); library(lmerTest); "OK"'))


# In[2]:


import os
R_HOME = r"C:\Program Files\R\R-4.6.1"
R_BIN = os.path.join(R_HOME, "bin", "x64")

os.environ["R_HOME"] = R_HOME
os.environ["PATH"] = R_BIN + os.pathsep + os.environ["PATH"]   # R's DLLs first
os.add_dll_directory(R_BIN)


# In[3]:


import re

import matplotlib.pyplot as plt
import numpy as np
import pandas as pd
from scipy import stats
from scipy.special import logsumexp
import statsmodels.api as sm
from statsmodels.stats.outliers_influence import variance_inflation_factor

get_ipython().run_line_magic('matplotlib', 'inline')


# In[4]:


# Main OD file (2019 only)
FINAL_FILE = r"C:\Users\ohdaw\OneDrive - Harvard University\snu_remains\redo\FINAL_dataset_2019only.csv"

# Park attribute files. These are only needed if FINAL_FILE does not
# already contain the park variables (see the check in Section 2).
# Please use the same files as in park_accessibility3.ipynb.
PARKVAR_FILE   = r"C:\Users\ohdaw\OneDrive - Harvard University\snu_remains\redo\PUT_PARKVAR_FILE_HERE.csv"
GREENAREA_FILE = r"C:\Users\ohdaw\OneDrive - Harvard University\snu_remains\redo\PUT_GREENAREA_FILE_HERE.csv"
TRANSIT_FILE   = r"C:\Users\ohdaw\OneDrive - Harvard University\snu_remains\redo\PUT_TRANSIT_FILE_HERE.csv"

OUT_DIR = r"C:\Users\ohdaw\OneDrive - Harvard University\snu_remains\redo\ccrem_rerun"
os.makedirs(OUT_DIR, exist_ok=True)

THETA = 0.10           # logsum cost parameter (theta in the manuscript)
RUN_NM_CHECK = True    # refit with Nelder-Mead to check optimizer stability
RUN_LRT = True         # LR test: with vs. without Female x Age terms (slow)

AMENITIES = ["green_ratio", "user_ratio", "facility_number",
             "parking_number", "transit_number", "park_area_ha"]


# ## 1. Age lookup tables (Fix 1)

# In[5]:


# Age midpoint used in the regression, by the 4-digit code in the column name
AGE_MID = {
    "0009": 4.5,
    "1014": 12.0, "1519": 17.0,
    "2024": 22.0, "2529": 27.0,
    "3034": 32.0, "3539": 37.0,
    "4044": 42.0, "4549": 47.0,
    "5054": 52.0, "5559": 57.0,
    "6064": 62.0, "6569": 67.0,
    "7000": 75.0,             # open band 70+ (was 35 in the old code)
}

# Ten-year group used in the figures
AGE_LABEL = {
    "0009": "0-9",
    "1014": "10-19", "1519": "10-19",
    "2024": "20-29", "2529": "20-29",
    "3034": "30-39", "3539": "30-39",
    "4044": "40-49", "4549": "40-49",
    "5054": "50-59", "5559": "50-59",
    "6064": "60-69", "6569": "60-69",   # 65-69 was put into "70+" before
    "7000": "70+",
}
LABEL_ORDER = ["0-9", "10-19", "20-29", "30-39", "40-49", "50-59", "60-69", "70+"]

# Ages at which marginal effects are reported (midpoints of the 10-year groups)
ME_AGES = {"0-9": 5, "10-19": 15, "20-29": 25, "30-39": 35,
           "40-49": 45, "50-59": 55, "60-69": 65, "70+": 75}


def parse_group(g):
    """'M_7000' -> (female, age_mid, age_label). Fails loudly on unknown codes."""
    sex, code = g.split("_")
    if sex not in ("M", "W"):
        raise ValueError(f"Unknown sex code in {g}")
    if code not in AGE_MID:
        raise ValueError(f"Unknown age code in {g}")
    return int(sex == "W"), AGE_MID[code], AGE_LABEL[code]


# ## 2. Load data and build park variables

# In[6]:


# The logsum (potential accessibility) uses the full OD file, as in the
# "Compute Accessibility" cell of the original notebook.
od = pd.read_csv(FINAL_FILE, encoding="utf-8")
print("FINAL file shape:", od.shape)
print("Parks:", od["ID"].nunique(), "| Origin gu:", od["INFLOW_CD"].nunique())

PARK_COLS = ["greenarea_area", "park_area", "openspaace_area", "road_area",
             "walkingtrail_area", "shadecanopy_area", "gymtrack_number",
             "swimmingpool_number", "sportsfacility_number", "playground_number",
             "cafeteria_number", "kiosk_number", "parkingcapacity_number",
             "bus500", "sub500"]
missing = [c for c in PARK_COLS if c not in od.columns]
print("Park variables missing from FINAL file:", missing if missing else "none")


# In[7]:


# Merge park attributes only if they are missing, then drop rows with NA
# (same steps as the original notebook: 10,600 rows -> 6,850 rows).
if missing:
    def read_any(path):
        try:
            return pd.read_csv(path, encoding="utf-8")
        except UnicodeDecodeError:
            return pd.read_csv(path, encoding="CP949")

    data = od.copy()
    data["ID"] = data["ID"].astype(str).str.strip()
    for path, sfx in [(PARKVAR_FILE, "_parkvar"), (GREENAREA_FILE, "_greenarea"),
                      (TRANSIT_FILE, "_transit")]:
        extra = read_any(path)
        extra["ID"] = extra["ID"].astype(str).str.strip()
        data = data.merge(extra, on="ID", how="left", suffixes=("", sfx))
        data = data.drop(columns=[c for c in data.columns if c.endswith(sfx)])
    print("Before dropna:", len(data))
    data = data.dropna()
    print("After dropna:", len(data))
else:
    data = od.dropna().copy()

group_cols = [c for c in data.columns if re.match(r"^[MW]_\d{4}$", c)]
assert len(group_cols) == 28, f"Expected 28 sex-age columns, found {len(group_cols)}"


# In[8]:


data["green_ratio"] = data["greenarea_area"] / data["park_area"] * 100
data["user_area"] = (data["openspaace_area"] + data["road_area"]
                     + data["walkingtrail_area"] + data["shadecanopy_area"])
data["user_ratio"] = data["user_area"] / data["park_area"] * 100
data["facility_number"] = (data["gymtrack_number"] + data["swimmingpool_number"]
                           + data["sportsfacility_number"] + data["playground_number"]
                           + data["cafeteria_number"] + data["kiosk_number"])
data["parking_number"] = data["parkingcapacity_number"]
data["transit_number"] = data["bus500"] + data["sub500"]
data["park_area_ha"] = data["park_area"] / 10_000

print(f"Parks: {data['ID'].nunique()} | Origin gu: {data['INFLOW_CD'].nunique()} "
      f"| Origin-park pairs: {len(data)}")


# ## 3. Wide to long, parse sex and age

# In[9]:


data_long = data.melt(
    id_vars=["INFLOW_CD", "ID", "c_eq_min"] + AMENITIES,
    value_vars=group_cols, var_name="group", value_name="visitors")
data_long = data_long[data_long["visitors"] > 0].copy()

parsed = data_long["group"].map(parse_group)
data_long["female"] = parsed.str[0]
data_long["age"] = parsed.str[1]
data_long["age_label"] = parsed.str[2]

# Check: the mapping should be one row per group, and 70+ must be 75
check = (data_long[["group", "female", "age", "age_label"]]
         .drop_duplicates().sort_values(["female", "age"]))
print("\nGroup -> female / age / label mapping:")
print(check.to_string(index=False))
assert check.loc[check["group"].str.endswith("7000"), "age"].eq(75).all()
assert check["group"].nunique() == 28


# ## 4. Center age, build interactions, rescale weights

# In[10]:


AGE_MEAN = data_long["age"].mean()          # unweighted row mean, as before
print(f"\nSample mean age used for centering: {AGE_MEAN:.3f}")

data_long["age_c"] = data_long["age"] - AGE_MEAN
data_long["age_c_sq"] = data_long["age_c"] ** 2
# Fix 2: demographic two-way terms
data_long["female_age"] = data_long["female"] * data_long["age_c"]
data_long["female_age2"] = data_long["female"] * data_long["age_c_sq"]

for a in AMENITIES:
    data_long[f"{a}_F"] = data_long[a] * data_long["female"]
    data_long[f"{a}_A"] = data_long[a] * data_long["age_c"]
    data_long[f"{a}_A2"] = data_long[a] * data_long["age_c_sq"]
    data_long[f"{a}_FA"] = data_long[a] * data_long["female"] * data_long["age_c"]
    data_long[f"{a}_FA2"] = data_long[a] * data_long["female"] * data_long["age_c_sq"]

# Visitor weights rescaled to mean 1
data_long["w"] = data_long["visitors"] / data_long["visitors"].mean()

data_long["ID"] = data_long["ID"].astype(str)
data_long["INFLOW_CD"] = data_long["INFLOW_CD"].astype(str)

DEMO_TERMS = ["female", "age_c", "age_c_sq", "female_age", "female_age2"]
AMEN_TERMS = (AMENITIES
              + [f"{a}_F" for a in AMENITIES]
              + [f"{a}_A" for a in AMENITIES]
              + [f"{a}_A2" for a in AMENITIES]
              + [f"{a}_FA" for a in AMENITIES]
              + [f"{a}_FA2" for a in AMENITIES])
FIXED_TERMS = DEMO_TERMS + AMEN_TERMS

print(f"Observations: {len(data_long):,} | Fixed-effect terms: {len(FIXED_TERMS)}")


# ## 5. VIF

# In[11]:


X_vif = sm.add_constant(data_long[FIXED_TERMS].astype(float))
vif = pd.DataFrame({
    "term": FIXED_TERMS,
    "VIF": [variance_inflation_factor(X_vif.values, i + 1) for i in range(len(FIXED_TERMS))],
}).sort_values("VIF", ascending=False)
vif.to_csv(os.path.join(OUT_DIR, "vif_main_terms.csv"), index=False)
print("\nVIF, amenity main effects:")
print(vif[vif["term"].isin(AMENITIES)].to_string(index=False))
print("\nVIF, ten highest:")
print(vif.head(10).to_string(index=False))


# ## 6. Fit the CCREM in R (lme4 + lmerTest via rpy2)
# 
# This cell can take several minutes.

# In[14]:


formula_full = "c_eq_min ~ " + " + ".join(FIXED_TERMS) + " + (1|ID) + (1|INFLOW_CD)"
formula_noFA = ("c_eq_min ~ " + " + ".join([t for t in FIXED_TERMS
                if t not in ("female_age", "female_age2")]) + " + (1|ID) + (1|INFLOW_CD)")
r_cols = ["c_eq_min", "w", "ID", "INFLOW_CD"] + FIXED_TERMS
data_long[r_cols].to_csv(os.path.join(OUT_DIR, "data_long_for_R.csv"), index=False)
with open(os.path.join(OUT_DIR, "formulas.txt"), "w") as f:
    f.write(formula_full + "\n" + formula_noFA + "\n")
print("Saved to", OUT_DIR)


# In[16]:


import rpy2.robjects as ro
from rpy2.robjects.packages import importr, isinstalled

# Which R is rpy2 using, and where does it look for packages?
print(ro.r("R.home()")[0])
print(list(ro.r(".libPaths()")))

# Install lme4 and lmerTest into this R if they are missing
utils = importr("utils")
utils.chooseCRANmirror(ind=1)
for pkg in ["lme4", "lmerTest"]:
    if not isinstalled(pkg):
        print(f"Installing {pkg} ...")
        utils.install_packages(pkg, type="binary")
    print(pkg, "installed:", isinstalled(pkg))


# In[ ]:


import rpy2.robjects as ro
print(ro.r("""
.libPaths(c(Sys.getenv("R_LIBS_USER"), .libPaths()))
deps <- tools::package_dependencies(c("lme4", "lmerTest"),
                                    db = installed.packages(), recursive = TRUE)
need <- unique(c("lme4", "lmerTest", unlist(deps)))
need[!sapply(need, requireNamespace, quietly = TRUE)]
"""))


# In[ ]:


import rpy2.robjects as ro
from rpy2.robjects import default_converter, pandas2ri
from rpy2.robjects.conversion import localconverter

r_cols = ["c_eq_min", "w", "ID", "INFLOW_CD"] + FIXED_TERMS
with localconverter(default_converter + pandas2ri.converter):
    ro.globalenv["dl"] = ro.conversion.py2rpy(data_long[r_cols].reset_index(drop=True))

formula_full = "c_eq_min ~ " + " + ".join(FIXED_TERMS) + " + (1|ID) + (1|INFLOW_CD)"
formula_noFA = ("c_eq_min ~ " + " + ".join([t for t in FIXED_TERMS
                                            if t not in ("female_age", "female_age2")])
                + " + (1|ID) + (1|INFLOW_CD)")
ro.globalenv["f_full"] = formula_full
ro.globalenv["f_noFA"] = formula_noFA

ro.r("""
suppressPackageStartupMessages({ library(lme4); library(lmerTest) })
dl$ID        <- factor(dl$ID)
dl$INFLOW_CD <- factor(dl$INFLOW_CD)
ctrl <- lmerControl(optimizer = "bobyqa", optCtrl = list(maxfun = 2e5))

fit <- lmerTest::lmer(as.formula(f_full), data = dl, weights = w,
                      REML = TRUE, control = ctrl)

cat("\\n=== isSingular ===\\n");  print(isSingular(fit))
cat("\\n=== VarCorr ===\\n");     print(VarCorr(fit))
cat("\\n=== rePCA ===\\n");       print(summary(rePCA(fit)))

coefs <- as.data.frame(summary(fit)$coefficients)
coefs$term <- rownames(coefs); rownames(coefs) <- NULL
V <- as.matrix(vcov(fit))
vc <- as.data.frame(VarCorr(fit))

# Nakagawa marginal / conditional R2 (random intercepts only)
var_f   <- var(as.vector(model.matrix(fit) %*% fixef(fit)))
var_id  <- vc$vcov[vc$grp == "ID"]
var_org <- vc$vcov[vc$grp == "INFLOW_CD"]
var_res <- sigma(fit)^2
tot     <- var_f + var_id + var_org + var_res
fitstats <- data.frame(
  quantity = c("Park (ID) intercept variance", "Park (ID) intercept SD",
               "Origin gu (INFLOW_CD) intercept variance", "Origin gu (INFLOW_CD) intercept SD",
               "Residual variance", "Residual SD",
               "ICC park", "ICC origin",
               "Marginal R2", "Conditional R2",
               "AIC", "BIC", "logLik", "N obs", "N parks", "N origin gu"),
  value = c(var_id, sqrt(var_id), var_org, sqrt(var_org), var_res, sqrt(var_res),
            var_id / (var_id + var_org + var_res), var_org / (var_id + var_org + var_res),
            var_f / tot, (var_f + var_id + var_org) / tot,
            AIC(fit), BIC(fit), as.numeric(logLik(fit)),
            nobs(fit), nlevels(dl$ID), nlevels(dl$INFLOW_CD)))
""")


# In[ ]:


if RUN_NM_CHECK:
    ro.r("""
    fit_nm <- update(fit, control = lmerControl(optimizer = "Nelder_Mead",
                                                optCtrl = list(maxfun = 2e5)))
    cat("\\n=== Optimizer check (BOBYQA vs Nelder-Mead) ===\\n")
    cat("Max abs difference in fixed effects:", max(abs(fixef(fit) - fixef(fit_nm))), "\\n")
    cat("logLik BOBYQA:", as.numeric(logLik(fit)),
        " | logLik Nelder-Mead:", as.numeric(logLik(fit_nm)), "\\n")
    """)


# ### Likelihood-ratio test for Female × Age and Female × Age²

# In[ ]:


if RUN_LRT:
    ro.r("""
    fit_noFA <- lmerTest::lmer(as.formula(f_noFA), data = dl, weights = w,
                               REML = TRUE, control = ctrl)
    cat("\\n=== LR test: adding Female x Age and Female x Age^2 (ML refit) ===\\n")
    lrt <- anova(fit_noFA, fit)   # anova() refits both models with ML
    print(lrt)
    """)


# ### Collect results

# In[ ]:


with localconverter(default_converter + pandas2ri.converter):
    coefs = ro.conversion.rpy2py(ro.r("coefs"))
    fitstats = ro.conversion.rpy2py(ro.r("fitstats"))
    V = np.array(ro.r("V"))
    v_names = list(ro.r("colnames(V)"))

coefs = coefs.rename(columns={"Std. Error": "SE", "t value": "t",
                              "Pr(>|t|)": "p", "df": "df"}).set_index("term")
V = pd.DataFrame(V, index=v_names, columns=v_names)


def stars(p):
    return "***" if p < 0.001 else "**" if p < 0.01 else "*" if p < 0.05 else ""


coefs["Sig"] = coefs["p"].apply(stars)
coefs.to_csv(os.path.join(OUT_DIR, "ccrem_coefficients.csv"))
fitstats.to_csv(os.path.join(OUT_DIR, "ccrem_fit_stats.csv"), index=False)

print("\n─── CCREM fixed effects ───")
print(coefs[["Estimate", "SE", "df", "t", "p", "Sig"]].to_string())
print("\n─── Fit statistics ───")
print(fitstats.to_string(index=False))


# ## 7. LaTeX rows for Table 3

# In[ ]:


def tex_num(x, dec=4):
    if x == 0:
        return "0"
    if abs(x) < 10 ** (-dec):
        m, e = f"{x:.2e}".split("e")
        return f"${m}\\times10^{{{int(e)}}}$"
    s = f"{x:.{dec}f}"
    return s.replace("-", "$-$")


def tex_name(t):
    return t.replace("_", "\\_")


LABELS = {"(Intercept)": "Constant", "female": "Female",
          "age_c": "Age (centered)", "age_c_sq": "Age$^2$ (centered)",
          "female_age": "Female $\\times$ Age", "female_age2": "Female $\\times$ Age$^2$"}

sections = [
    ("Baseline", ["(Intercept)"] + DEMO_TERMS),
    ("Park amenity main effects", AMENITIES),
    ("Female interactions (\\_F)", [f"{a}_F" for a in AMENITIES]),
    ("Age interactions (\\_A)", [f"{a}_A" for a in AMENITIES]),
    ("Age$^2$ interactions (\\_A2)", [f"{a}_A2" for a in AMENITIES]),
    ("Female $\\times$ Age interactions (\\_FA)", [f"{a}_FA" for a in AMENITIES]),
    ("Female $\\times$ Age$^2$ interactions (\\_FA2)", [f"{a}_FA2" for a in AMENITIES]),
]
lines = []
for title, terms in sections:
    lines.append(f"\\multicolumn{{6}}{{l}}{{\\textit{{{title}}}}} \\\\[1pt]")
    for t in terms:
        r = coefs.loc[t]
        p_txt = "$<$0.001" if r["p"] < 0.001 else f"{r['p']:.3f}"
        lines.append(f"{LABELS.get(t, tex_name(t))} & {tex_num(r['Estimate'])} & "
                     f"{tex_num(r['SE'])} & {tex_num(r['t'], 3)} & {p_txt} & {r['Sig']} \\\\")
    lines.append("\\midrule")
lines = lines[:-1]
with open(os.path.join(OUT_DIR, "ccrem_table_rows.tex"), "w", encoding="utf-8") as f:
    f.write("\n".join(lines))


# ## 8. Marginal effects with delta-method 95% CI

# In[ ]:


beta = coefs["Estimate"]


def me_and_se(var, ac, female_part, male_part):
    """Linear combination of coefficients and its delta-method SE."""
    w = {}
    if male_part:
        w.update({var: 1.0, f"{var}_A": ac, f"{var}_A2": ac ** 2})
    if female_part:
        w.update({f"{var}_F": 1.0, f"{var}_FA": ac, f"{var}_FA2": ac ** 2})
    names = list(w)
    c = np.array([w[n] for n in names])
    est = float(c @ beta[names].values)
    se = float(np.sqrt(c @ V.loc[names, names].values @ c))
    return est, se


z = stats.norm.ppf(0.975)
rows = []
for var in AMENITIES:
    for label, age in ME_AGES.items():
        ac = age - AGE_MEAN
        m, m_se = me_and_se(var, ac, female_part=False, male_part=True)
        w_, w_se = me_and_se(var, ac, female_part=True, male_part=True)
        d, d_se = me_and_se(var, ac, female_part=True, male_part=False)
        rows.append({
            "Amenity": var, "AgeGroup": label, "Age": age,
            "Men_ME": m, "Men_lo": m - z * m_se, "Men_hi": m + z * m_se,
            "Women_ME": w_, "Women_lo": w_ - z * w_se, "Women_hi": w_ + z * w_se,
            "W_minus_M": d, "Diff_SE": d_se,
            "Diff_p": 2 * (1 - stats.norm.cdf(abs(d / d_se))),
        })
me = pd.DataFrame(rows)
me.to_csv(os.path.join(OUT_DIR, "marginal_effects_ccrem.csv"), index=False)
print("\n─── Marginal effects ───")
print(me[["Amenity", "AgeGroup", "Men_ME", "Women_ME", "W_minus_M", "Diff_p"]]
      .round(4).to_string(index=False))


# In[ ]:


# LaTeX rows for an appendix table of marginal effects
tex = []
for var in AMENITIES:
    tex.append(f"\\multicolumn{{4}}{{l}}{{\\texttt{{{tex_name(var)}}}}} \\\\")
    for _, r in me[me["Amenity"] == var].iterrows():
        tex.append(f"\\quad {r['AgeGroup'].replace('-', '--')} & {tex_num(r['Men_ME'], 3)} & "
                   f"{tex_num(r['Women_ME'], 3)} & {tex_num(r['W_minus_M'], 3)}"
                   f"{stars(r['Diff_p'])} \\\\")
with open(os.path.join(OUT_DIR, "marginal_effects_table.tex"), "w", encoding="utf-8") as f:
    f.write("\n".join(tex))


# In[ ]:


# 2 x 3 panel figure
fig, axes = plt.subplots(2, 3, figsize=(15, 8))
for ax, var in zip(axes.flatten(), AMENITIES):
    sub = me[me["Amenity"] == var]
    x = np.arange(len(sub))
    ax.plot(x, sub["Men_ME"], marker="o", label="Men")
    ax.fill_between(x, sub["Men_lo"], sub["Men_hi"], alpha=0.15)
    ax.plot(x, sub["Women_ME"], marker="o", label="Women")
    ax.fill_between(x, sub["Women_lo"], sub["Women_hi"], alpha=0.15)
    ax.axhline(0, linestyle="--", color="gray", linewidth=0.8)
    ax.set_xticks(x)
    ax.set_xticklabels(sub["AgeGroup"], rotation=45, ha="right")
    ax.set_title(var, fontsize=11)
    ax.set_xlabel("Age group")
    ax.set_ylabel("Effect on travel cost (minutes)")
    ax.yaxis.set_major_formatter(plt.FuncFormatter(lambda v, _: f"{v:.3f}"))
    ax.legend(fontsize=8)
plt.suptitle("Marginal effects of park amenity variables on travel cost "
             "by age group and sex (CCREM, 95% CI)")
plt.tight_layout()
plt.savefig(os.path.join(OUT_DIR, "marginal_effects_ccrem.png"), dpi=300, bbox_inches="tight")
plt.show()


# ## 9. Descriptive figures with corrected age groups
# 
# Ten-year values are visitor-weighted over all rows in the group. The logsum uses the full FINAL file.

# In[ ]:


od_groups = [c for c in od.columns if re.match(r"^[MW]_\d{4}$", c)]

# Potential accessibility per origin gu
A_origin = (od.assign(u=-THETA * od["c_eq_min"])
              .groupby("INFLOW_CD")["u"]
              .apply(lambda s: logsumexp(s.values))
              .rename("A_logsum"))
print("\nLogsum range across origin gu "
      f"(theta = {THETA}): {A_origin.min():.3f} to {A_origin.max():.3f}")
for th in (0.05, 0.10, 0.20):
    a_th = od.assign(u=-th * od["c_eq_min"]).groupby("INFLOW_CD")["u"].apply(
        lambda s: logsumexp(s.values))
    print(f"  theta = {th:.2f}: {a_th.min():.3f} to {a_th.max():.3f}")

origin_tot = od.groupby("INFLOW_CD")[od_groups].sum()

rows = []
for g in od_groups:
    female, _, label = parse_group(g)
    # potential: weights = visitors from each gu in this group
    w_o = origin_tot[g]
    # realized: weights = visitors on each origin-park row in this group
    w_r = od[g].to_numpy()
    c = od["c_eq_min"].to_numpy()
    mask = np.isfinite(c) & (w_r > 0)
    rows.append({"group": g, "sex": "W" if female else "M", "age_label": label,
                 "A_num": (w_o * A_origin.loc[w_o.index]).sum(), "A_den": w_o.sum(),
                 "c_num": (w_r[mask] * c[mask]).sum(), "c_den": w_r[mask].sum()})
grp = pd.DataFrame(rows)

agg = grp.groupby(["sex", "age_label"])[["A_num", "A_den", "c_num", "c_den"]].sum()
agg["A_weighted"] = agg["A_num"] / agg["A_den"]
agg["c_weighted"] = agg["c_num"] / agg["c_den"]
agg = agg.reset_index()

wide_A = agg.pivot(index="age_label", columns="sex", values="A_weighted").reindex(LABEL_ORDER)
wide_c = agg.pivot(index="age_label", columns="sex", values="c_weighted").reindex(LABEL_ORDER)
wide_A["W_minus_M"] = wide_A["W"] - wide_A["M"]
wide_A["W_minus_M_minutes"] = wide_A["W_minus_M"] / THETA   # logsum gap in equivalent minutes
wide_c["W_minus_M"] = wide_c["W"] - wide_c["M"]

print("\n─── Potential accessibility by group (corrected age groups) ───")
print(wide_A.round(4).to_string())
print("\n─── Realized travel cost by group (corrected age groups) ───")
print(wide_c.round(3).to_string())
wide_A.to_csv(os.path.join(OUT_DIR, "group_potential_accessibility.csv"))
wide_c.to_csv(os.path.join(OUT_DIR, "group_realized_cost.csv"))


def line_plot(wide, ylabel, title, fname):
    plt.figure()
    plt.plot(LABEL_ORDER, wide["M"], marker="o", label="Men")
    plt.plot(LABEL_ORDER, wide["W"], marker="o", label="Women")
    plt.xlabel("Age group"); plt.ylabel(ylabel); plt.title(title)
    plt.legend(); plt.xticks(rotation=45, ha="right")
    plt.gca().yaxis.set_major_formatter(plt.FuncFormatter(lambda v, _: f"{v:.3f}"))
    plt.tight_layout()
    plt.savefig(os.path.join(OUT_DIR, fname), dpi=300, bbox_inches="tight")
    plt.show()


def gap_plot(series, ylabel, title, fname):
    plt.figure()
    plt.plot(LABEL_ORDER, series, marker="o", color="green")
    plt.axhline(0, linestyle="--", color="gray")
    plt.xlabel("Age group"); plt.ylabel(ylabel); plt.title(title)
    plt.xticks(rotation=45, ha="right")
    plt.gca().yaxis.set_major_formatter(plt.FuncFormatter(lambda v, _: f"{v:.3f}"))
    plt.tight_layout()
    plt.savefig(os.path.join(OUT_DIR, fname), dpi=300, bbox_inches="tight")
    plt.show()


# In[ ]:


line_plot(wide_A, "Logsum accessibility",
          "Potential accessibility by age group and sex", "group_potential_accessibility.png")
gap_plot(wide_A["W_minus_M"], "Logsum accessibility",
         "Gender difference in potential accessibility (Women - Men)", "group_potential_gap.png")
line_plot(wide_c, "Mean travel cost (minutes)",
          "Realized travel cost by age group and sex", "group_realized_cost.png")
gap_plot(wide_c["W_minus_M"], "Mean travel cost (minutes)",
         "Gender difference in realized travel cost (Women - Men)", "group_realized_gap.png")

print(f"\nAll outputs saved in: {OUT_DIR}")


# In[ ]:





# In[ ]:





# In[ ]:




