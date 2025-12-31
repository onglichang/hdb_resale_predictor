# Model Experiment Log

This document tracks the performance of our HDB Resale Price prediction model as we iterate on features and algorithms.

## 1. Accuracy Standards

We verify our model using two primary metrics.

### **MAE (Mean Absolute Error)**
*   **Definition**: The average absolute difference between the predicted price and the actual price.
*   **Why we use it**: **Interpretability**. It answers the question: *"On average, how many dollars is the model off by?"* This is easy for business stakeholders and users to understand.
*   **Goal**: Minimize this value.

### **RMSE (Root Mean Squared Error)**
*   **Definition**: The square root of the average of squared differences.
*   **Why we use it**: **Outlier Penalty**. RMSE disproportionately penalizes *large* errors. In real estate, predicting a \$1M flat as \$500k is a catastrophic failure compared to small deviations. RMSE helps us identify if the model is failing badly on specific segments (e.g., luxury flats).
*   **Goal**: Minimize this value. Ideally, RMSE should be close to MAE (indicating few outliers).

---

## 2. Experiment History

| Date | Experiment ID | Model | Changes / Hypothesis | MAE ($) | RMSE ($) | Status |
| :--- | :--- | :--- | :--- | :--- | :--- | :--- |
| 2025-12-31 | **Baseline (Phase 1)** | Random Forest | Initial PoC. `n_estimators=100`, `max_depth=10`. Basic features (Town, Flat Type, Storey, Floor Area, Date). Sparse One-Hot Encoding. | **53,332** | **75,491** | ✅ Deployed |

---

## 3. Analysis

### Baseline Analysis (2025-12-31)
*   **Performance**: The model has an average error of ~$53k. Given the average HDB price (~$500k - $800k), this represents a rough **7-10% error margin**.
*   **Gap**: The RMSE ($75k) is significantly higher than the MAE ($53k), which indicates **variance**. The model likely struggles with high-value outliers (e.g., "Million Dollar Flats" in Pinnacle@Duxton or Bishan) or very old/unique flats.
*   **Constraint**: The current Random Forest is limited by `max_depth=10` to prevent overfitting during the initial build. Increasing depth or switching to Boosting (XGBoost) should improve this.
