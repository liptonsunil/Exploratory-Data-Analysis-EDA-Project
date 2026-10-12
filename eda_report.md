# Exploratory Data Analysis Report

## 1. Dataset Overview
- Rows: **178**, Columns: **14**
- Numeric features: 13, Categorical: 1
- Duplicate rows: 0
- Missing values: 0

### Summary statistics (first 6 features)
|                   |   count |   mean |   std |   min |   25% |   50% |    75% |    max |   skew |
|:------------------|--------:|-------:|------:|------:|------:|------:|-------:|-------:|-------:|
| alcohol           |     178 |  13    |  0.81 | 11.03 | 12.36 | 13.05 |  13.68 |  14.83 |  -0.05 |
| malic_acid        |     178 |   2.34 |  1.12 |  0.74 |  1.6  |  1.87 |   3.08 |   5.8  |   1.04 |
| ash               |     178 |   2.37 |  0.27 |  1.36 |  2.21 |  2.36 |   2.56 |   3.23 |  -0.18 |
| alcalinity_of_ash |     178 |  19.49 |  3.34 | 10.6  | 17.2  | 19.5  |  21.5  |  30    |   0.21 |
| magnesium         |     178 |  99.74 | 14.28 | 70    | 88    | 98    | 107    | 162    |   1.1  |
| total_phenols     |     178 |   2.3  |  0.63 |  0.98 |  1.74 |  2.36 |   2.8  |   3.88 |   0.09 |

## 2. Data Quality
Columns with IQR-rule outliers: alcalinity_of_ash (4), color_intensity (4), magnesium (4), ash (3), malic_acid (3)

## 3. Strongest Feature Correlations
- total_phenols vs flavanoids: **0.86**
- flavanoids vs od280/od315_of_diluted_wines: **0.79**
- total_phenols vs od280/od315_of_diluted_wines: **0.70**
- flavanoids vs proanthocyanins: **0.65**
- alcohol vs proline: **0.64**

## 4. Key Influencing Factors for `cultivar`
Ranked by ANOVA F-score (higher = better separates groups):
- flavanoids: F = 233.9
- proline: F = 207.9
- od280/od315_of_diluted_wines: F = 190.0
- alcohol: F = 135.1
- color_intensity: F = 120.7

Group means for the top 3 features:
| cultivar   |   flavanoids |   proline |   od280/od315_of_diluted_wines |
|:-----------|-------------:|----------:|-------------------------------:|
| class_0    |         2.98 |   1115.71 |                           3.16 |
| class_1    |         2.08 |    519.51 |                           2.79 |
| class_2    |         0.78 |    629.9  |                           1.68 |

## 5. Visualisations
01_distributions.png, 02_target_counts.png, 03_correlation_heatmap.png, 04_top_features_by_target.png, 05_pairplot_top_features.png

## 6. Conclusions
(Add your own 3-5 sentence interpretation here: what patterns matter, what surprised you, what you would do next.)