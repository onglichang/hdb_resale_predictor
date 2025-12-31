import pandas as pd
import os

RAW_DATA_PATH = "data/processed/resale-flat-prices-validated.csv"
PROCESSED_DATA_PATH = "data/processed/resale-flat-prices-processed.csv"

def preprocess():
    if not os.path.exists(RAW_DATA_PATH):
        print(f"File not found: {RAW_DATA_PATH}")
        return

    print("Loading data...")
    df = pd.read_csv(RAW_DATA_PATH)

    print("Preprocessing data...")
    # Basic cleaning
    df.dropna(inplace=True)
    
    # Feature Engineering (Example)
    # Convert month to datetime
    df['month'] = pd.to_datetime(df['month'], format='%Y-%m')
    df['year'] = df['month'].dt.year
    df['month_num'] = df['month'].dt.month
    
    # NOTE: Encoding is now handled in the training pipeline.
    # We save "clean" data with original string categories.

    os.makedirs(os.path.dirname(PROCESSED_DATA_PATH), exist_ok=True)
    df.to_csv(PROCESSED_DATA_PATH, index=False)
    print(f"Processed data saved to {PROCESSED_DATA_PATH}")

if __name__ == "__main__":
    preprocess()
