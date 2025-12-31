# Project Status & Roadmap: HDB Resale Prediction MLOps

**Date:** 2025-12-31
**Current Stage:** Prototype / Proof of Concept (PoC)

## 1. Current Status

We have established a functional **MLOps Infrastructure Skeleton**.

### ✅ Capabilities
*   **Infrastructure**: Git, DVC (Data Version Control), and MLflow are configured and integrated.
*   **Reproducibility**: The pipeline (`ingest` -> `preprocess` -> `train`) is defined in `dvc.yaml` and fully reproducible via `dvc repro`.
*   **Experiment Tracking**: Training runs, metrics (MAE, RMSE), and model artifacts are automatically logged to MLflow.
*   **Model Serving**: A FastAPI application (`src/serve.py`) is running and can dynamically load the latest trained model from MLflow.

### ⚠️ Known Limitations (The "Gap" to Production)
*   **Preprocessing Disconnect**: The serving API receives raw strings (e.g., "ANG MO KIO") but the model expects numbers. Since the preprocessing encoders (like `LabelEncoder`) are not saved/loaded, the API currently returns placeholder predictions.
*   **Manual Ingestion**: Data ingestion relies on manual download or placement of the CSV file.
*   **No Input Validation**: The API does not validate if input values (e.g., `town`, `flat_type`) are valid.

---

## 2. Roadmap

To upgrade this PoC to a production-ready system, we will execute the following phases:

### Phase 1: Robust Feature Engineering (Priority: High)
*   **Goal**: Ensure the serving API can make real predictions by unifying preprocessing.
*   **Steps**:
    1.  **Refactor `preprocess.py`**: Replace manual pandas manipulation with a Scikit-Learn `Pipeline` (using `OneHotEncoder`, `StandardScaler`).
    2.  **Artifact Persistence**: Log the *full pipeline* (Preprocessor + Model) to MLflow.
    3.  **Update `serve.py`**: Load the full pipeline to automatically transform raw JSON inputs into predictions.

### Phase 2: Reliability & Automation (Priority: Medium)
*   **Goal**: Remove manual steps and prevent bad data.
*   **Steps**:
    1.  **Automated Ingestion**: Implement a robust script to automatically fetch/update data from Data.gov.sg (handling API keys or stable URLs).
    2.  **Data Validation**: Integrate **Pandera** or **Great Expectations** to validate input data quality before training.
    3.  **Containerization**: Create a `Dockerfile` to package the environment for consistent deployment.

### Phase 3: CI/CD & Operations (Priority: Low)
*   **Goal**: Automate testing and deployment.
*   **Steps**:
    1.  **GitHub Actions**: Set up CI/CD to run `dvc repro` and tests on every commit.
    2.  **Model Registry Policy**: Implement a tagging strategy (e.g., promote models from `Staging` -> `Production`).
