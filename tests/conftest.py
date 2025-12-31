import pytest
import pandas as pd
import numpy as np

@pytest.fixture
def sample_df():
    """Generates a synthetic dataframe for testing."""
    data = {
        "month": ["2024-01", "2024-02", "2023-12"],
        "town": ["ANG MO KIO", "BEDOK", "PUNGGOL"],
        "flat_type": ["3 ROOM", "4 ROOM", "5 ROOM"],
        "block": ["123", "456", "789"],
        "street_name": ["AVE 1", "RD 2", "ST 3"],
        "storey_range": ["01 TO 03", "04 TO 06", "07 TO 09"],
        "floor_area_sqm": [60.0, 90.0, 110.0],
        "flat_model": ["New Generation", "Model A", "Premium Apartment"],
        "lease_commence_date": [1980, 1990, 2015],
        "remaining_lease": ["55 years", "65 years", "90 years"],
        "resale_price": [300000.0, 500000.0, 700000.0]
    }
    return pd.DataFrame(data)

@pytest.fixture
def sample_input_json():
    """Generates a valid JSON input for the API."""
    return {
        "month": "2024-01",
        "town": "ANG MO KIO",
        "flat_type": "3 ROOM",
        "block": "123",
        "street_name": "AVE 1",
        "storey_range": "04 TO 06",
        "floor_area_sqm": 67.0,
        "flat_model": "New Generation",
        "lease_commence_date": 1980,
        "remaining_lease": "55 years"
    }
