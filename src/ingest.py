import requests
import os
import sys
import pandas as pd

# Resource ID for "Resale flat prices based on registration date from Jan-2017 onwards"
RESOURCE_ID = "d_2d493bdcc1d9a44828b6e71cb095b88d"
API_URL = "https://data.gov.sg/api/action/datastore_search"
RAW_DATA_PATH = "data/raw/resale-flat-prices.csv"

def ingest():
    if os.path.exists(RAW_DATA_PATH):
        print(f"Data already exists at {RAW_DATA_PATH}. Skipping download.")
        return

    print("Data ingestion is currently manual due to Data.gov.sg API changes.")
    print("Please download the 'Resale flat prices based on registration date from Jan-2017 onwards' CSV.")
    print("Save it to: data/raw/resale-flat-prices.csv")
    print(f"URL: https://data.gov.sg/dataset/resale-flat-prices-based-on-registration-date-from-jan-2017-onwards")
    
    # Check if we should fail or just warn. 
    # For CI pipeline, we might need it to exist.
    sys.exit(1)

if __name__ == "__main__":
    ingest()
