# src/services/data_loader.py
# Loads, validates, and enriches sales CSV data.
# Connects to: src/config/settings.py, src/services/dashboard.py
# Created: 2026-06-08

from pathlib import Path
import logging

import pandas as pd

from src.config.settings import REQUIRED_COLUMNS


logger = logging.getLogger(__name__)


def load_sales_data(csv_path: Path) -> pd.DataFrame:
    """Load, validate, and enrich a sales CSV.

    Parameters:
        csv_path: Path to the CSV file.

    Returns:
        DataFrame with parsed dates, numeric fields, revenue, and month columns.

    Raises:
        FileNotFoundError: If the CSV path does not exist.
        ValueError: If required columns or values are invalid.
    """

    logger.info("Loading sales CSV from %s", csv_path)
    if not csv_path.exists():
        raise FileNotFoundError(f"CSV file not found: {csv_path}")

    df = pd.read_csv(csv_path)
    missing_columns = REQUIRED_COLUMNS - set(df.columns)
    if missing_columns:
        missing = ", ".join(sorted(missing_columns))
        raise ValueError(f"CSV is missing required columns: {missing}")

    df = df.copy()
    df["order_date"] = pd.to_datetime(df["order_date"], errors="coerce")
    if df["order_date"].isna().any():
        raise ValueError("CSV contains invalid order_date values.")

    for column in ("quantity", "unit_price"):
        df[column] = pd.to_numeric(df[column], errors="coerce")
        if df[column].isna().any():
            raise ValueError(f"CSV contains invalid {column} values.")

    if "revenue" in df.columns:
        df["revenue"] = pd.to_numeric(df["revenue"], errors="coerce")
        if df["revenue"].isna().any():
            raise ValueError("CSV contains invalid revenue values.")
    else:
        df["revenue"] = df["quantity"] * df["unit_price"]

    df["month"] = df["order_date"].dt.to_period("M").dt.to_timestamp()
    logger.info("Loaded %s sales rows", len(df))
    return df.sort_values("order_date").reset_index(drop=True)
