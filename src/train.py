import pandas as pd
import mlflow
import mlflow.sklearn
from sklearn.model_selection import train_test_split
from sklearn.ensemble import RandomForestRegressor
from sklearn.metrics import mean_absolute_error, mean_squared_error
import os

PROCESSED_DATA_PATH = "data/processed/resale-flat-prices-processed.csv"

def train():
    if not os.path.exists(PROCESSED_DATA_PATH):
        print(f"Processed data not found at {PROCESSED_DATA_PATH}")
        return

    print("Loading processed data...")
    df = pd.read_csv(PROCESSED_DATA_PATH)
    
    X = df.drop('resale_price', axis=1)
    y = df['resale_price']

    # Handle remaining non-numeric columns if any (simple check)
    X = X.select_dtypes(include=['number'])

    X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42)

    mlflow.set_experiment("hdb_price_prediction")

    with mlflow.start_run():
        print("Training model...")
        n_estimators = 100
        max_depth = 10
        model = RandomForestRegressor(n_estimators=n_estimators, max_depth=max_depth, random_state=42)
        model.fit(X_train, y_train)

        print("Evaluating model...")
        predictions = model.predict(X_test)
        mae = mean_absolute_error(y_test, predictions)
        rmse = mean_squared_error(y_test, predictions) ** 0.5

        print(f"MAE: {mae}")
        print(f"RMSE: {rmse}")

        mlflow.log_param("n_estimators", n_estimators)
        mlflow.log_param("max_depth", max_depth)
        mlflow.log_metric("mae", mae)
        mlflow.log_metric("rmse", rmse)

        mlflow.sklearn.log_model(model, "model")
        print("Model saved to MLflow.")

if __name__ == "__main__":
    train()
