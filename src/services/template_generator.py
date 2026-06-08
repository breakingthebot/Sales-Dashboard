# src/services/template_generator.py
# Creates fill-in sales CSV templates for dashboard users.
# Connects to: generate_sales_csv.py, src/config/settings.py
# Created: 2026-06-08

from pathlib import Path

import pandas as pd

from src.config.settings import DEFAULT_TEMPLATE_PATH, REQUIRED_COLUMNS


SAMPLE_ROWS = [
    {
        "order_date": "2026-01-10",
        "order_id": "SO-1001",
        "product": "Example Product A",
        "category": "Example Category",
        "region": "East",
        "quantity": 3,
        "unit_price": 19.99,
    },
    {
        "order_date": "2026-01-11",
        "order_id": "SO-1002",
        "product": "Example Product B",
        "category": "Example Category",
        "region": "West",
        "quantity": 1,
        "unit_price": 99.00,
    },
]


def build_template_dataframe(include_sample_rows: bool) -> pd.DataFrame:
    """Build a sales CSV template DataFrame.

    Parameters:
        include_sample_rows: Whether to include example rows.

    Returns:
        DataFrame with required dashboard columns.
    """

    rows = SAMPLE_ROWS if include_sample_rows else []
    return pd.DataFrame(rows, columns=REQUIRED_COLUMNS)


def generate_sales_template(
    output_path: Path = DEFAULT_TEMPLATE_PATH,
    include_sample_rows: bool = False,
) -> Path:
    """Write a sales CSV template to disk.

    Parameters:
        output_path: Destination CSV path.
        include_sample_rows: Whether to include example rows.

    Returns:
        Path to the generated template file.
    """

    output_path.parent.mkdir(parents=True, exist_ok=True)
    build_template_dataframe(include_sample_rows).to_csv(output_path, index=False)
    return output_path
