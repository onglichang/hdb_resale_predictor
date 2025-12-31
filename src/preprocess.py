import pandas as pd
import os

RAW_DATA_PATH = "data/raw/resale-flat-prices.csv"
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
    
    # Simple encoding for categorical variables (just for demo)
    # Ideally, use OneHotEncoder or similar in a pipeline
    categorical_cols = ['town', 'flat_type', 'flat_model', 'storey_range']
    for col in categorical_cols:
        df[col] = df[col].astype('category').cat.codes

    os.makedirs(os.path.dirname(PROCESSED_DATA_PATH), exist_ok=True)
    df.to_csv(PROCESSED_DATA_PATH, index=False)
    print(f"Processed data saved to {PROCESSED_DATA_PATH}")

if __name__ == "__main__":
    preprocess()
