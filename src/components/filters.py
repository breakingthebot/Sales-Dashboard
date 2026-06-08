# src/components/filters.py
# Applies dashboard filter selections to validated sales data.
# Connects to: streamlit_app.py, tests/test_sales_dashboard.py
# Created: 2026-06-08

from datetime import date
from typing import Iterable

import pandas as pd


def apply_sales_filters(
    df: pd.DataFrame,
    start_date: date,
    end_date: date,
    categories: Iterable[str],
    regions: Iterable[str],
    products: Iterable[str],
) -> pd.DataFrame:
    """Filter sales data by date, category, region, and product.

    Parameters:
        df: Validated sales DataFrame.
        start_date: Inclusive start date.
        end_date: Inclusive end date.
        categories: Selected category names.
        regions: Selected region names.
        products: Selected product names.

    Returns:
        Filtered DataFrame.
    """

    filtered = df.copy()
    start_timestamp = pd.Timestamp(start_date)
    end_timestamp = pd.Timestamp(end_date)
    filtered = filtered[
        (filtered["order_date"] >= start_timestamp)
        & (filtered["order_date"] <= end_timestamp)
    ]

    selected_categories = list(categories)
    selected_regions = list(regions)
    selected_products = list(products)

    if selected_categories:
        filtered = filtered[filtered["category"].isin(selected_categories)]
    if selected_regions:
        filtered = filtered[filtered["region"].isin(selected_regions)]
    if selected_products:
        filtered = filtered[filtered["product"].isin(selected_products)]

    return filtered.reset_index(drop=True)
