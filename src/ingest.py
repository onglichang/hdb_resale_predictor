import os
import sys

DATA_DIR = "data/raw"
FILENAME = "resale-flat-prices.csv"
FILE_PATH = os.path.join(DATA_DIR, FILENAME)
DATA_URL = "https://data.gov.sg/dataset/resale-flat-prices"

def ingest():
    os.makedirs(DATA_DIR, exist_ok=True)
    if os.path.exists(FILE_PATH):
        print(f"Data found at {FILE_PATH}")
    else:
        print(f"Data not found at {FILE_PATH}")
        print(f"Please download the dataset 'Resale flat prices based on registration date from Jan-2017 onwards' from {DATA_URL}")
        print(f"Save it as '{FILE_PATH}'")
        # In a real scenario, we would automate this, but data.gov.sg APIs are tricky without API keys or exact resource IDs.
        sys.exit(1)

if __name__ == "__main__":
    ingest()
