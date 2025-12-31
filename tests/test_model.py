import pytest
from src.train import create_pipeline
from sklearn.pipeline import Pipeline
import pandas as pd
import numpy as np

def test_create_pipeline():
    """Test pipeline creation structure"""
    num_cols = ['floor_area_sqm']
    cat_cols = ['town']
    pipeline = create_pipeline(num_cols, cat_cols)
    assert isinstance(pipeline, Pipeline)
    assert 'feat_eng' in pipeline.named_steps
    assert 'preprocessor' in pipeline.named_steps
    assert 'model' in pipeline.named_steps

def test_pipeline_fit_predict(sample_df):
    """Test full training cycle on dummy data"""
    # Prepare features/target
    X = sample_df.drop("resale_price", axis=1)
    y = sample_df["resale_price"]
    
    # Define features expected by our pipeline logic
    categorical_features = ['town', 'flat_type', 'flat_model', 'storey_range', 'street_name', 'block', 'remaining_lease']
    # year and month_num are derived
    numerical_features = ['floor_area_sqm', 'lease_commence_date', 'year', 'month_num'] 
    
    # Filter only what exists in our sample_df to be safe, but sample_df matches production schema
    # But wait, create_pipeline expects us to pass the list of columns to transform.
    
    pipeline = create_pipeline(numerical_features, categorical_features)
    
    # Fit
    pipeline.fit(X, y)
    
    # Predict
    preds = pipeline.predict(X)
    assert len(preds) == len(X)
    assert isinstance(preds, np.ndarray)
