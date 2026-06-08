# src/services/column_mapping.py
# Maps uploaded CSV column names into the dashboard's required schema.
# Connects to: src/config/settings.py, streamlit_app.py, tests/test_sales_dashboard.py
# Created: 2026-06-08

import pandas as pd

from src.config.settings import REQUIRED_COLUMNS


NO_COLUMN_SELECTED = "-- Select column --"


def missing_required_columns(df: pd.DataFrame) -> list[str]:
    """Return required columns missing from a DataFrame.

    Parameters:
        df: Raw sales DataFrame.

    Returns:
        Sorted list of missing required column names.
    """

    return [column for column in REQUIRED_COLUMNS if column not in df.columns]


def needs_column_mapping(df: pd.DataFrame) -> bool:
    """Determine whether a DataFrame needs header mapping.

    Parameters:
        df: Raw sales DataFrame.

    Returns:
        True when one or more required columns are missing.
    """

    return bool(missing_required_columns(df))


def default_column_mapping(df: pd.DataFrame) -> dict[str, str]:
    """Build a best-effort default mapping by exact column name.

    Parameters:
        df: Raw sales DataFrame.

    Returns:
        Mapping of required dashboard column names to uploaded CSV columns.
    """

    return {
        required_column: required_column
        for required_column in REQUIRED_COLUMNS
        if required_column in df.columns
    }


def apply_column_mapping(df: pd.DataFrame, mapping: dict[str, str]) -> pd.DataFrame:
    """Apply selected uploaded CSV columns to required dashboard names.

    Parameters:
        df: Raw sales DataFrame.
        mapping: Required-column to uploaded-column mapping.

    Returns:
        DataFrame with mapped required columns.

    Raises:
        ValueError: If any required mapping is missing or duplicated.
    """

    missing_mappings = [
        column
        for column in REQUIRED_COLUMNS
        if not mapping.get(column) or mapping[column] == NO_COLUMN_SELECTED
    ]
    if missing_mappings:
        missing = ", ".join(missing_mappings)
        raise ValueError(f"Column mapping is missing required fields: {missing}")

    selected_columns = [mapping[column] for column in REQUIRED_COLUMNS]
    duplicate_columns = sorted(
        {
            column
            for column in selected_columns
            if selected_columns.count(column) > 1
        }
    )
    if duplicate_columns:
        duplicates = ", ".join(duplicate_columns)
        raise ValueError(f"Column mapping uses the same source column more than once: {duplicates}")

    mapped = df.copy()
    rename_map = {source: target for target, source in mapping.items()}
    mapped = mapped.rename(columns=rename_map)
    return mapped
