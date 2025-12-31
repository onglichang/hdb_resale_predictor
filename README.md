# HDB Resale Price Predictor (MLOps)

An end-to-end MLOps workflow for predicting Singapore HDB resale flat prices. This project demonstrates a production-ready pipeline using **DVC** for data versioning, **MLflow** for experiment tracking, and **FastAPI/Docker** for model serving.

![Status](https://img.shields.io/badge/Status-Phase_2_Complete-green) ![Python](https://img.shields.io/badge/Python-3.10-blue) ![Docker](https://img.shields.io/badge/Docker-Ready-blue)

## 🚀 Key Features

*   **Automated Pipeline**: End-to-end workflow (`ingest` -> `validate` -> `preprocess` -> `train`) managed by DVC.
*   **Robust Feature Engineering**: Scikit-Learn `Pipeline` handles raw data transformation (Date parsing, One-Hot Encoding) automatically during serving.
*   **Data Validation**: **Pandera** schema checks ensure input data quality (e.g., prices > 0) before training.
*   **Experiment Tracking**: All model runs, metrics (MAE/RMSE), and artifacts are logged to **MLflow**.
*   **Production Serving**:
    *   **FastAPI**: High-performance API.
    *   **Docker**: Containerized for consistent deployment.
    *   **Validation**: Real-time type checking for API inputs.

## 🏗️ Architecture

```mermaid
graph LR
    A[Data Source (Data.gov.sg)] -->|Ingest| B(Raw Data)
    B -->|Validate (Pandera)| C(Validated Data)
    C -->|Preprocess| D(Processed Data)
    D -->|Train (Sklearn Pipeline)| E[Model Artifact (MLflow)]
    E -->|Serve| F[FastAPI / Docker]
```

## ⚡ Quick Start (Docker)

The easiest way to run the predictor is via Docker.

1.  **Build the Image**:
    ```bash
    docker build -t hdb-predictor .
    ```

2.  **Run the Container**:
    ```bash
    docker run -p 8000:8000 hdb-predictor
    ```

3.  **Get a Prediction**:
    ```bash
    curl -X POST "http://127.0.0.1:8000/predict" \
         -H "Content-Type: application/json" \
         -d '{
             "month": "2024-01",
             "town": "ANG MO KIO",
             "flat_type": "3 ROOM",
             "block": "123",
             "street_name": "AVE 1",
             "storey_range": "04 TO 06",
             "floor_area_sqm": 67,
             "flat_model": "New Generation",
             "lease_commence_date": 1980,
             "remaining_lease": "55 years"
         }'
    ```

## 🛠️ Local Development

To contribute or experiment with the pipeline locally:

### 1. Setup Environment
```bash
python3 -m venv venv
source venv/bin/activate
pip install -r requirements.txt
```

### 2. Get Data
This project uses the "Resale flat prices based on registration date from Jan-2017 onwards" dataset.
*   **Manual**: Download from [Data.gov.sg](https://data.gov.sg/dataset/resale-flat-prices-based-on-registration-date-from-jan-2017-onwards) and save to `data/raw/resale-flat-prices.csv`.
*   *(Note: Automated ingestion via API is implemented in `src/ingest.py` but currently falls back to manual due to API changes.)*

### 3. Run Pipeline (DVC)
Reproduce the entire workflow:
```bash
dvc repro
```
This will:
1.  **Validate** data schema.
2.  **Preprocess** and engineer features.
3.  **Train** the model and log to MLflow.

### 4. View Experiments
```bash
mlflow ui
```
Visit `http://localhost:5000` to compare runs.

## 📊 Performance (Phase 2 Baseline)

*   **Model**: Random Forest Regressor
*   **MAE**: ~$53,000
    *   *Interpretation*: On average, predictions are within \$53k of the actual transaction price.
*   **RMSE**: ~$75,000

## 📝 Project Structure
```
├── data/               # Raw and processed data (tracked by DVC)
├── mlruns/             # MLflow experiment logs
├── src/                # Source code
│   ├── ingest.py       # Data download
│   ├── validate_data.py# Pandera validation
│   ├── preprocess.py   # Cleaning
│   ├── train.py        # Pipeline training
│   └── serve.py        # FastAPI app
├── dvc.yaml            # DVC pipeline definition
├── Dockerfile          # Container definition
└── README.md           # This file
```
