import pandas as pd
import mlflow
import mlflow.sklearn
from sklearn.model_selection import train_test_split
from sklearn.ensemble import RandomForestRegressor
from sklearn.metrics import mean_absolute_error, mean_squared_error
from sklearn.pipeline import Pipeline
from sklearn.compose import ColumnTransformer
from sklearn.preprocessing import OneHotEncoder, StandardScaler
import os

PROCESSED_DATA_PATH = "data/processed/resale-flat-prices-processed.csv"

def train():
    if not os.path.exists(PROCESSED_DATA_PATH):
        print(f"Processed data not found at {PROCESSED_DATA_PATH}")
        return

    print("Loading processed data...")
    df = pd.read_csv(PROCESSED_DATA_PATH)
    
    # Separate features and target
    X = df.drop('resale_price', axis=1)
    y = df['resale_price']

from sklearn.base import BaseEstimator, TransformerMixin

# Custom Transformer for Date Features
class DateFeatureEngineering(BaseEstimator, TransformerMixin):
    def fit(self, X, y=None):
        return self
    
    def transform(self, X):
        X = X.copy()
        # Ensure month is datetime
        if 'month' in X.columns:
            # Handle both YYYY-MM (raw) and YYYY-MM-DD (csv)
            X['month'] = pd.to_datetime(X['month'])
            X['year'] = X['month'].dt.year
            X['month_num'] = X['month'].dt.month
            # Drop the original 'month' column if not needed by other steps, 
            # BUT ColumnTransformer might need to ignore it. 
            # For now keep it, but we won't use it in ColumnTransformer.
        return X

def train():
    if not os.path.exists(PROCESSED_DATA_PATH):
        print(f"Processed data not found at {PROCESSED_DATA_PATH}")
        return

    print("Loading processed data...")
    df = pd.read_csv(PROCESSED_DATA_PATH)
    
    # Separate features and target
    X = df.drop('resale_price', axis=1)
    y = df['resale_price']

    # DROP pre-calculated features to ensure Pipeline handles it
    if 'year' in X.columns:
        X = X.drop(['year', 'month_num'], axis=1)

    categorical_features = ['town', 'flat_type', 'flat_model', 'storey_range', 'street_name', 'block', 'remaining_lease']
    numerical_features = ['floor_area_sqm', 'lease_commence_date', 'year', 'month_num'] # Derived features

    # Note: 'year' and 'month_num' are NOT in X yet (we dropped them), 
    # but they WILL be after the first step of the pipeline.
    
    # We cannot check if they exist in X.columns here for validation.
    # So we remove the list comprehension check for derived features.
    categorical_features = [c for c in categorical_features if c in X.columns]
    # numerical_features = [c for c in numerical_features if c in X.columns] 

    print(f"Cat features: {categorical_features}")
    print(f"Num features: {numerical_features}")

    # Build Pipeline
    # Step 1: Feature Engineering
    # Step 2: Preprocessing (Encoding/Scaling) -> This operates on the OUTPUT of Step 1
    # Step 3: Model

    preprocessor = ColumnTransformer(
        transformers=[
            ('num', StandardScaler(), numerical_features),
            ('cat', OneHotEncoder(handle_unknown='ignore', sparse_output=True), categorical_features)
        ])

    pipeline = Pipeline(steps=[
        ('feat_eng', DateFeatureEngineering()),
        ('preprocessor', preprocessor),
        ('model', RandomForestRegressor(n_estimators=100, max_depth=10, random_state=42, n_jobs=-1))
    ])

    X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42)

    mlflow.set_experiment("hdb_price_prediction")

    with mlflow.start_run():
        print("Training pipeline...")
        pipeline.fit(X_train, y_train)

        print("Evaluating pipeline...")
        predictions = pipeline.predict(X_test)
        mae = mean_absolute_error(y_test, predictions)
        rmse = mean_squared_error(y_test, predictions) ** 0.5

        print(f"MAE: {mae}")
        print(f"RMSE: {rmse}")

        mlflow.log_metric("mae", mae)
        mlflow.log_metric("rmse", rmse)
        
        # Log parameters (accessing steps)
        mlflow.log_param("n_estimators", pipeline.named_steps['model'].n_estimators)
        mlflow.log_param("max_depth", pipeline.named_steps['model'].max_depth)

        # Log the components of the pipeline
        mlflow.sklearn.log_model(pipeline, "model")
        print("Pipeline saved to MLflow.")

if __name__ == "__main__":
    train()
