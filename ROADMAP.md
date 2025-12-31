# Project Status & Roadmap: HDB Resale Prediction MLOps

**Date:** 2025-12-31
**Current Stage:** Production Ready / Beta (Phase 2 Complete)

## 1. Current Status

We have established a functional **MLOps Infrastructure Skeleton** with **Robust Feature Engineering**.

### ✅ Capabilities
*   **Infrastructure**: Git, DVC (Data Version Control), and MLflow are configured and integrated.
*   **Reproducibility**: The pipeline (`ingest` -> `validate` -> `preprocess` -> `train`) is fully reproducible via `dvc repro`.
*   **Data Quality**: Strict schema validation ensures no corrupt data enters the model.
*   **Containerization**: Dockerized API ready for deployment.
*   **Experiment Tracking**: Training runs, metrics (MAE, RMSE), and model artifacts are automatically logged to MLflow.
*   **Robust Serving**: The API serves predictions using a full Scikit-Learn Pipeline.

### ⚠️ Known Limitations
*   **Feature Completeness**: Model does not yet use Geolocation or Distance features (Phase 4).
*   **Ingestion Reliability**: Data.gov.sg API changes often require manual intervention for the ingestion step (partially automated).

---

## 2. Roadmap

To upgrade this PoC to a production-ready system, we will execute the following phases:

### Phase 1: Robust Feature Engineering (Priority: High) - ✅ COMPLETED
*   **Goal**: Ensure the serving API can make real predictions by unifying preprocessing.
*   **Steps**:
    1.  [x] **Refactor `preprocess.py`**: Replace manual pandas manipulation with a Scikit-Learn `Pipeline`.
    2.  [x] **Artifact Persistence**: Log the *full pipeline* (Preprocessor + Model) to MLflow.
    3.  [x] **Update `serve.py`**: Load the full pipeline to automatically transform raw JSON inputs into predictions.

### Phase 2: Reliability & Automation (Priority: Medium) - ✅ COMPLETED
*   **Goal**: Remove manual steps and prevent bad data.
*   **Steps**:
    1.  [x] **Automated Ingestion**: Implemented `src/ingest.py` to fetch data (with robust fallback manual instructions if API fails).
    2.  [x] **Data Validation**: Integrated **Pandera** to enforce schema checks (e.g., Price > 0) in the pipeline.
    3.  [x] **Containerization**: Created `Dockerfile` and `docker-compose.yml` for production-ready deployment.

### Phase 3: CI/CD & Operations (Priority: Low)
*   **Goal**: Automate testing and deployment.
*   **Steps**:
    1.  **GitHub Actions**: Set up CI/CD to run `dvc repro` and tests on every commit.
    2.  **Model Registry Policy**: Implement a tagging strategy (e.g., promote models from `Staging` -> `Production`).

### Phase 4: Model Performance Optimization (Priority: Medium)
*   **Goal**: Improve accuracy (reduce MAE < $40k).
*   **Steps**:
    1.  **Advanced Algorithms**: Switch from Random Forest to **XGBoost** or **LightGBM** for better gradient boosting performance.
    2.  **Hyperparameter Tuning**: Use **Optuna** to automatically find the best parameters (e.g., learning rate, depth).
    3.  **Detailed Feature Engineering**:
        *   **Geolocation**: Use OneMap API to get Lat/Long for every block.
        *   **Distance Features**: Calculate distance to nearest MRT, CBD, and Primary Schools.
        *   **Economic Indicators**: Incorporate COW (Cash Over Valuation) trends or interest rates if available.
    4.  **Smart API**: Implement the "User-Centric" schema (Postal Code -> Features) using OneMap integration.
