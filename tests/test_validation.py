import pytest
import pandas as pd
import pandera as pa
from src.validate_data import HDBSchema

def test_validation_success(sample_df):
    """Test that valid data passes validation."""
    validated = HDBSchema.validate(sample_df)
    assert isinstance(validated, pd.DataFrame)
    assert len(validated) == 3

def test_validation_failure_price(sample_df):
    """Test that negative price fails validation."""
    sample_df.loc[0, "resale_price"] = -100.0
    with pytest.raises(pa.errors.SchemaError):
        HDBSchema.validate(sample_df)

def test_validation_failure_month_format(sample_df):
    """Test that invalid month format fails validation."""
    sample_df.loc[0, "month"] = "2024/01" # Wrong format
    with pytest.raises(pa.errors.SchemaError):
        HDBSchema.validate(sample_df)
