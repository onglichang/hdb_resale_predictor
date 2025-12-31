# HDB MLOps Workflow Walkthrough

I have implemented an MLOps workflow for HDB price prediction using DVC and MLflow.

## Completed Work
- **Environment**: Setup `requirements.txt`, `.gitignore` and `dvc.yaml`.
- **Data Ingestion**: Created `src/ingest.py` (checks for data) and configured DVC to track data.
- **Preprocessing**: `src/preprocess.py` cleans and features engineers the data.
- **Training**: `src/train.py` trains a RandomForest model and logs metrics to MLflow.
- **Serving**: `src/serve.py` uses FastAPI to serve the model.

## How to Run

1.  **Install Dependencies**:
    ```bash
    python3 -m venv venv
    source venv/bin/activate
    pip install -r requirements.txt
    ```

2.  **Get Data**:
    Download the "Resale flat prices based on registration date from Jan-2017 onwards" CSV from [Data.gov.sg](https://data.gov.sg/dataset/resale-flat-prices).
    Save it to `data/raw/resale-flat-prices.csv`.

    > [!NOTE]
    > If you don't have the data, the pipeline will fail. The `src/ingest.py` script can verify if the file exists.

3.  **Run Pipeline**:
    ```bash
    # Add data to DVC
    dvc add data/raw/resale-flat-prices.csv
    
    # Run the pipeline
    dvc repro
    ```

4.  **View Experiments**:
    ```bash
    mlflow ui
    ```

5.  **Serve Model**:
    ```bash
    uvicorn src.serve:app --reload
    ```
    Test with:
    ```bash
    curl -X POST "http://127.0.0.1:8000/predict" \
         -H "Content-Type: application/json" \
         -d '{"month": "2024-01", "town": "ANG MO KIO", "flat_type": "3 ROOM", "block": "123", "street_name": "AVE 1", "storey_range": "04 TO 06", "floor_area_sqm": 67, "flat_model": "New Generation", "lease_commence_date": 1980, "remaining_lease": "55 years"}'
    ```

## 4. Serving (Docker)

To run the API in a production-like container:

1.  **Build**:
    ```bash
    docker build -t hdb-predictor .
    ```

2.  **Run**:
    ```bash
    docker run -p 8000:8000 hdb-predictor
    ```

3.  **Test**:
    Same curl command as above:
    ```bash
    curl -X POST "http://127.0.0.1:8000/predict" ...
    ```

## 5. Verification Results

*   **Model Accuracy**:
    *   MAE: ~$53k
    *   RMSE: ~$75k
*   **Pipeline**: Fully reproducible via `dvc repro`.
*   **API**: Validated and containerized.
- `mlruns` directory created (confirming MLflow logging).
- `dvc.lock` updated.
