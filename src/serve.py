import mlflow.sklearn
import pandas as pd
from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
import os

app = FastAPI()

# Fetch the latest model from MLflow
experiment_name = "hdb_price_prediction"
experiment = mlflow.get_experiment_by_name(experiment_name)
if experiment is None:
    print(f"Experiment '{experiment_name}' not found.")
    MODEL = None
else:
    runs = mlflow.search_runs(experiment_ids=[experiment.experiment_id], 
                              order_by=["start_time DESC"], max_results=1)
    if not runs.empty:
        run_id = runs.iloc[0]["run_id"]
        # In more recent MLflow, artifact_path="model" was used in train.py
        model_uri = f"runs:/{run_id}/model"
        print(f"Loading model from {model_uri}...")
        try:
            MODEL = mlflow.sklearn.load_model(model_uri)
            print("Model loaded successfully.")
        except Exception as e:
            print(f"Failed to load model: {e}")
            MODEL = None
    else:
        print("No runs found.")
        MODEL = None

class HDBFlat(BaseModel):
    month: str
    town: str
    flat_type: str
    block: str
    street_name: str
    storey_range: str
    floor_area_sqm: float
    flat_model: str
    lease_commence_date: int
    remaining_lease: str
    resale_price: float = None # Optional for prediction

@app.post("/predict")
def predict(flat: HDBFlat):
    # This is a placeholder. 
    # Real implementation needs to preprocess the input just like training data.
    # Since we used simple categorical encoding in preprocess.py, we need the SAME encoding here.
    # For a real MLOps system, the preprocessor should be saved (e.g. pickle) and loaded.
    
    if MODEL:
        try:
             # Construct DataFrame
            data = pd.DataFrame([flat.dict()])
            
            # The MODEL is now a Pipeline, so it handles encoding automatically!
            prediction = MODEL.predict(data)
            return {"prediction": prediction[0], "status": "Success"}
        except Exception as e:
             return {"prediction": None, "status": "Prediction failed", "error": str(e)}
    else:
        return {"prediction": None, "status": "Model NOT loaded"}

@app.get("/")
def read_root():
    return {"message": "HDB Resale Price Predictor API"}
