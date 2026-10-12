"""
Exploratory Data Analysis (EDA) Project
Steps: overview -> data quality -> univariate -> bivariate -> correlations
       -> key influencing factors -> auto-generated report (eda_report.md)

To use your own data: set CSV_PATH and TARGET below (TARGET = column you care about).
"""
import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt
import numpy as np
import pandas as pd
import seaborn as sns
from sklearn.datasets import load_wine

CSV_PATH = None        # e.g. "mydata.csv"
TARGET = "cultivar"    # e.g. "price"
sns.set_theme(style="whitegrid")

# ------------------------------------------------------------------ 1. LOAD
if CSV_PATH:
    df = pd.read_csv(CSV_PATH)
else:
    w = load_wine(as_frame=True)
    df = w.data.copy()
    df[TARGET] = w.target.map(dict(enumerate(w.target_names)))

num_cols = df.select_dtypes("number").columns.tolist()
cat_cols = df.select_dtypes(exclude="number").columns.tolist()
report = ["# Exploratory Data Analysis Report\n"]

# ------------------------------------------------------------- 2. OVERVIEW
report += ["## 1. Dataset Overview",
           f"- Rows: **{df.shape[0]}**, Columns: **{df.shape[1]}**",
           f"- Numeric features: {len(num_cols)}, Categorical: {len(cat_cols)}",
           f"- Duplicate rows: {df.duplicated().sum()}",
           f"- Missing values: {int(df.isna().sum().sum())}\n"]
desc = df[num_cols].describe().T.round(2)
desc["skew"] = df[num_cols].skew().round(2)
desc.to_csv("summary_statistics.csv")
report += ["### Summary statistics (first 6 features)", desc.head(6).to_markdown(), ""]

# -------------------------------------------------------- 3. DATA QUALITY
q1, q3 = df[num_cols].quantile(.25), df[num_cols].quantile(.75)
iqr = q3 - q1
outliers = ((df[num_cols] < q1 - 1.5 * iqr) | (df[num_cols] > q3 + 1.5 * iqr)).sum()
outliers = outliers[outliers > 0].sort_values(ascending=False)
report += ["## 2. Data Quality",
           "Columns with IQR-rule outliers: " +
           (", ".join(f"{c} ({n})" for c, n in outliers.head(5).items()) or "none") + "\n"]

# ------------------------------------------------------------ 4. UNIVARIATE
fig, axes = plt.subplots(4, 4, figsize=(16, 12))
for ax, c in zip(axes.ravel(), num_cols):
    sns.histplot(df[c], kde=True, ax=ax, color="steelblue")
    ax.set_title(c, fontsize=10)
for ax in axes.ravel()[len(num_cols):]:
    ax.axis("off")
plt.tight_layout(); plt.savefig("01_distributions.png", dpi=130); plt.close()

if cat_cols:
    fig, ax = plt.subplots(figsize=(5, 4))
    sns.countplot(x=df[TARGET], ax=ax, palette="viridis", hue=df[TARGET], legend=False)
    ax.set_title(f"{TARGET} counts")
    plt.tight_layout(); plt.savefig("02_target_counts.png", dpi=130); plt.close()

# ------------------------------------------------------------- 5. CORRELATION
corr = df[num_cols].corr()
fig, ax = plt.subplots(figsize=(11, 9))
sns.heatmap(corr, cmap="coolwarm", center=0, annot=True, fmt=".1f",
            annot_kws={"size": 7}, ax=ax)
ax.set_title("Correlation Matrix")
plt.tight_layout(); plt.savefig("03_correlation_heatmap.png", dpi=130); plt.close()

pairs = (corr.where(np.triu(np.ones(corr.shape), 1).astype(bool))
             .stack().sort_values(key=abs, ascending=False).head(5))
report += ["## 3. Strongest Feature Correlations"]
report += [f"- {a} vs {b}: **{r:.2f}**" for (a, b), r in pairs.items()] + [""]

# ------------------------------------------- 6. KEY INFLUENCING FACTORS
if cat_cols:
    # ANOVA F-statistic: how strongly each feature separates the groups
    from scipy.stats import f_oneway
    scores = {}
    for c in num_cols:
        groups = [g[c].values for _, g in df.groupby(TARGET)]
        scores[c] = f_oneway(*groups).statistic
    scores = pd.Series(scores).sort_values(ascending=False)
    top = scores.head(4).index.tolist()

    fig, axes = plt.subplots(1, 4, figsize=(16, 4))
    for ax, c in zip(axes, top):
        sns.boxplot(data=df, x=TARGET, y=c, hue=TARGET, palette="Set2",
                    legend=False, ax=ax)
        ax.set_title(c)
    plt.tight_layout(); plt.savefig("04_top_features_by_target.png", dpi=130); plt.close()

    sns.pairplot(df[top + [TARGET]], hue=TARGET, palette="Set2", corner=True)
    plt.savefig("05_pairplot_top_features.png", dpi=110); plt.close()

    report += [f"## 4. Key Influencing Factors for `{TARGET}`",
               "Ranked by ANOVA F-score (higher = better separates groups):"]
    report += [f"- {c}: F = {s:.1f}" for c, s in scores.head(5).items()] + [""]
    means = df.groupby(TARGET)[top[:3]].mean().round(2)
    report += ["Group means for the top 3 features:", means.to_markdown(), ""]
else:
    tcorr = corr[TARGET].drop(TARGET).sort_values(key=abs, ascending=False)
    report += [f"## 4. Key Influencing Factors for `{TARGET}`"]
    report += [f"- {c}: r = {r:.2f}" for c, r in tcorr.head(5).items()] + [""]

# ------------------------------------------------------------------ 7. WRITE
report += ["## 5. Visualisations",
           "01_distributions.png, 02_target_counts.png, 03_correlation_heatmap.png, "
           "04_top_features_by_target.png, 05_pairplot_top_features.png\n",
           "## 6. Conclusions\n(Add your own 3-5 sentence interpretation here: "
           "what patterns matter, what surprised you, what you would do next.)"]
open("eda_report.md", "w").write("\n".join(report))
print("\n".join(report))
