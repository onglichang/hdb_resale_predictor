import pandas as pd
from sklearn.model_selection import train_test_split
from sklearn.ensemble import RandomForestRegressor
from sklearn.pipeline import Pipeline
from sklearn.compose import ColumnTransformer
from sklearn.preprocessing import OneHotEncoder, StandardScaler
import os

PROCESSED_DATA_PATH = "data/processed/resale-flat-prices-processed.csv"

def test_pipeline():
    if not os.path.exists(PROCESSED_DATA_PATH):
        print(f"Processed data not found at {PROCESSED_DATA_PATH}")
        return

    print("Loading processed data...")
    df = pd.read_csv(PROCESSED_DATA_PATH)
    
    X = df.drop('resale_price', axis=1)
    y = df['resale_price']

    if 'month' in X.columns:
        X = X.drop('month', axis=1)

    categorical_features = ['town', 'flat_type', 'flat_model', 'storey_range', 'street_name', 'block', 'remaining_lease']
    numerical_features = ['floor_area_sqm', 'lease_commence_date', 'year', 'month_num']

    categorical_features = [c for c in categorical_features if c in X.columns]
    numerical_features = [c for c in numerical_features if c in X.columns]

    print(f"Cat: {categorical_features}")
    print(f"Num: {numerical_features}")

    preprocessor = ColumnTransformer(
        transformers=[
            ('num', StandardScaler(), numerical_features),
            ('cat', OneHotEncoder(handle_unknown='ignore', sparse_output=False), categorical_features)
        ])

    pipeline = Pipeline(steps=[
        ('preprocessor', preprocessor),
        ('model', RandomForestRegressor(n_estimators=100, max_depth=10, random_state=42))
    ])

    X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42)

    print("Fitting pipeline...")
    pipeline.fit(X_train, y_train)
    print("Pipeline fitted successfully!")

    print("Predicting...")
    preds = pipeline.predict(X_test)
    print(f"Predictions: {preds}")

if __name__ == "__main__":
    test_pipeline()
