# src/services/template_generator.py
# Creates fill-in templates and random sales CSV files for dashboard users.
# Connects to: generate_sales_csv.py, src/config/settings.py
# Created: 2026-06-08

from datetime import date, timedelta
from pathlib import Path
import random

import pandas as pd

from src.config.settings import DEFAULT_GENERATED_CSV_PATH, DEFAULT_TEMPLATE_PATH, REQUIRED_COLUMNS


PRODUCT_CATALOG = {
    "Apex Laptop": ("Computers", 1299.00),
    "Nova Tablet": ("Computers", 699.00),
    "Vertex Monitor": ("Accessories", 249.00),
    "Orbit Keyboard": ("Accessories", 89.00),
    "Swift Mouse": ("Accessories", 39.00),
    "Atlas Desk": ("Furniture", 459.00),
    "Cloud Chair": ("Furniture", 319.00),
}
REGIONS = ("North", "South", "East", "West")
DEFAULT_RANDOM_ROW_COUNT = 50
RANDOM_START_DATE = date(2026, 1, 1)
RANDOM_DATE_RANGE_DAYS = 180


def build_template_dataframe() -> pd.DataFrame:
    """Build a sales CSV template DataFrame.

    Parameters:
        None.

    Returns:
        DataFrame with required dashboard columns.
    """

    return pd.DataFrame([], columns=REQUIRED_COLUMNS)


def build_random_sales_dataframe(row_count: int, seed: int | None = None) -> pd.DataFrame:
    """Build a random sales DataFrame for upload testing.

    Parameters:
        row_count: Number of sales rows to generate.
        seed: Optional random seed for repeatable output.

    Returns:
        DataFrame with randomized sales rows.

    Raises:
        ValueError: If row_count is less than one.
    """

    if row_count < 1:
        raise ValueError("row_count must be at least 1.")

    generator = random.Random(seed)
    products = tuple(PRODUCT_CATALOG.keys())
    rows = []
    for index in range(1, row_count + 1):
        product = generator.choice(products)
        category, base_price = PRODUCT_CATALOG[product]
        order_date = RANDOM_START_DATE + timedelta(
            days=generator.randint(0, RANDOM_DATE_RANGE_DAYS)
        )
        price_multiplier = generator.uniform(0.9, 1.1)
        rows.append(
            {
                "order_date": order_date.isoformat(),
                "order_id": f"SO-{index:04d}",
                "product": product,
                "category": category,
                "region": generator.choice(REGIONS),
                "quantity": generator.randint(1, 20),
                "unit_price": round(base_price * price_multiplier, 2),
            }
        )

    return pd.DataFrame(rows, columns=REQUIRED_COLUMNS)


def generate_sales_template(
    output_path: Path = DEFAULT_TEMPLATE_PATH,
) -> Path:
    """Write a sales CSV template to disk.

    Parameters:
        output_path: Destination CSV path.

    Returns:
        Path to the generated template file.
    """

    output_path.parent.mkdir(parents=True, exist_ok=True)
    build_template_dataframe().to_csv(output_path, index=False)
    return output_path


def generate_random_sales_csv(
    output_path: Path = DEFAULT_GENERATED_CSV_PATH,
    row_count: int = DEFAULT_RANDOM_ROW_COUNT,
    seed: int | None = None,
) -> Path:
    """Write randomized sales CSV data to disk.

    Parameters:
        output_path: Destination CSV path.
        row_count: Number of rows to generate.
        seed: Optional random seed for repeatable output.

    Returns:
        Path to the generated CSV file.
    """

    output_path.parent.mkdir(parents=True, exist_ok=True)
    build_random_sales_dataframe(row_count, seed).to_csv(output_path, index=False)
    return output_path
