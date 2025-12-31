import pandera as pa
from pandera.typing import DataFrame, Series
import pandas as pd
import os
import sys

RAW_DATA_PATH = "data/raw/resale-flat-prices.csv"
VALIDATED_DATA_PATH = "data/processed/resale-flat-prices-validated.csv"

# Define the schema
HDBSchema = pa.DataFrameSchema({
    "month": pa.Column(str, checks=pa.Check.str_matches(r"^\d{4}-\d{2}$")),
    "town": pa.Column(str),
    "flat_type": pa.Column(str),
    "block": pa.Column(str),
    "street_name": pa.Column(str),
    "storey_range": pa.Column(str),
    "floor_area_sqm": pa.Column(float, checks=pa.Check.gt(0)),
    "flat_model": pa.Column(str),
    "lease_commence_date": pa.Column(int, checks=[pa.Check.ge(1960), pa.Check.le(2030)]),
    "remaining_lease": pa.Column(str),
    "resale_price": pa.Column(float, checks=pa.Check.gt(0)),
}, strict=False, coerce=True)

def validate():
    if not os.path.exists(RAW_DATA_PATH):
        print(f"File not found: {RAW_DATA_PATH}")
        sys.exit(1)

    print("Validating data...")
    try:
        df = pd.read_csv(RAW_DATA_PATH)
        # Validate
        validated_df = HDBSchema.validate(df)
        print("Validation success!")
        
        # Save validated data (effectively a pass-through, but acts as a checkpoint)
        os.makedirs(os.path.dirname(VALIDATED_DATA_PATH), exist_ok=True)
        validated_df.to_csv(VALIDATED_DATA_PATH, index=False)
        print(f"Validated data saved to {VALIDATED_DATA_PATH}")
        
    except pa.errors.SchemaError as e:
        print("Data Validation Failed!")
        print(e)
        sys.exit(1)

if __name__ == "__main__":
    validate()
