# src/services/analysis.py
# Calculates sales metrics and grouped analysis tables.
# Connects to: src/services/report.py, src/services/charts.py, tests
# Created: 2026-06-08

import pandas as pd


def summarize_sales(df: pd.DataFrame) -> dict[str, object]:
    """Return headline sales metrics for the dashboard.

    Parameters:
        df: Validated sales DataFrame.

    Returns:
        Dictionary of KPI names and values.
    """

    total_revenue = float(df["revenue"].sum())
    total_orders = int(df["order_id"].nunique())
    total_units = int(df["quantity"].sum())
    avg_order_value = total_revenue / total_orders if total_orders else 0.0
    top_product = (
        df.groupby("product")["revenue"].sum().sort_values(ascending=False).index[0]
        if not df.empty
        else "N/A"
    )

    return {
        "total_revenue": total_revenue,
        "total_orders": total_orders,
        "total_units": total_units,
        "avg_order_value": avg_order_value,
        "top_product": top_product,
    }


def monthly_revenue(df: pd.DataFrame) -> pd.DataFrame:
    """Group revenue by month.

    Parameters:
        df: Validated sales DataFrame.

    Returns:
        DataFrame with month and revenue columns.
    """

    return (
        df.groupby("month", as_index=False)["revenue"]
        .sum()
        .sort_values("month")
    )


def top_products(df: pd.DataFrame, limit: int = 5) -> pd.DataFrame:
    """Return products ranked by revenue.

    Parameters:
        df: Validated sales DataFrame.
        limit: Maximum number of products to return.

    Returns:
        DataFrame of product revenue and units.
    """

    return (
        df.groupby("product", as_index=False)
        .agg(revenue=("revenue", "sum"), units=("quantity", "sum"))
        .sort_values("revenue", ascending=False)
        .head(limit)
    )


def revenue_breakdown(df: pd.DataFrame, column: str) -> pd.DataFrame:
    """Group revenue by a categorical column.

    Parameters:
        df: Validated sales DataFrame.
        column: Column to group by.

    Returns:
        DataFrame ranked by revenue.
    """

    return (
        df.groupby(column, as_index=False)["revenue"]
        .sum()
        .sort_values("revenue", ascending=False)
    )
