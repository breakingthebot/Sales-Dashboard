# src/services/charts.py
# Generates matplotlib chart images for the dashboard report.
# Connects to: src/services/analysis.py, src/services/dashboard.py
# Created: 2026-06-08

from pathlib import Path

import matplotlib

matplotlib.use("Agg")

import matplotlib.dates as mdates
import matplotlib.pyplot as plt
import pandas as pd

from src.config.settings import CATEGORY_COLORS, CHART_COLORS, CHART_DPI
from src.services.analysis import monthly_revenue, revenue_breakdown, top_products
from src.utils.formatting import currency


def style_chart(ax: plt.Axes, title: str) -> None:
    """Apply consistent dashboard styling to a chart.

    Parameters:
        ax: Matplotlib axes to style.
        title: Chart title.

    Returns:
        None.
    """

    ax.set_title(title, fontsize=14, fontweight="bold", pad=14)
    ax.spines["top"].set_visible(False)
    ax.spines["right"].set_visible(False)
    ax.grid(axis="y", color=CHART_COLORS["grid"], linewidth=0.8)
    ax.set_axisbelow(True)


def create_monthly_chart(df: pd.DataFrame) -> plt.Figure:
    """Create the monthly revenue trend chart.

    Parameters:
        df: Validated sales DataFrame.

    Returns:
        Matplotlib figure.
    """

    monthly = monthly_revenue(df)
    fig, ax = plt.subplots(figsize=(10, 5.5))
    ax.plot(
        monthly["month"],
        monthly["revenue"],
        color=CHART_COLORS["monthly"],
        marker="o",
        linewidth=2.5,
    )
    ax.set_ylabel("Revenue")
    ax.xaxis.set_major_formatter(mdates.DateFormatter("%b %Y"))
    ax.tick_params(axis="x", rotation=30)
    ax.yaxis.set_major_formatter(lambda value, _: currency(value))
    style_chart(ax, "Revenue Trend by Month")
    fig.tight_layout()
    return fig


def save_monthly_chart(df: pd.DataFrame, path: Path) -> None:
    """Save the monthly revenue trend chart.

    Parameters:
        df: Validated sales DataFrame.
        path: Output image path.

    Returns:
        None.
    """

    fig = create_monthly_chart(df)
    fig.savefig(path, dpi=CHART_DPI)
    plt.close(fig)


def create_top_products_chart(df: pd.DataFrame, limit: int) -> plt.Figure:
    """Create the top products revenue chart.

    Parameters:
        df: Validated sales DataFrame.
        limit: Number of products to include.

    Returns:
        Matplotlib figure.
    """

    products = top_products(df, limit=limit).sort_values("revenue")
    fig, ax = plt.subplots(figsize=(10, 5.5))
    ax.barh(products["product"], products["revenue"], color=CHART_COLORS["products"])
    ax.set_xlabel("Revenue")
    ax.xaxis.set_major_formatter(lambda value, _: currency(value))
    style_chart(ax, f"Top {limit} Products by Revenue")
    fig.tight_layout()
    return fig


def save_top_products_chart(df: pd.DataFrame, path: Path, limit: int) -> None:
    """Save the top products revenue chart.

    Parameters:
        df: Validated sales DataFrame.
        path: Output image path.
        limit: Number of products to include.

    Returns:
        None.
    """

    fig = create_top_products_chart(df, limit)
    fig.savefig(path, dpi=CHART_DPI)
    plt.close(fig)


def create_category_chart(df: pd.DataFrame) -> plt.Figure:
    """Create the category revenue mix chart.

    Parameters:
        df: Validated sales DataFrame.

    Returns:
        Matplotlib figure.
    """

    categories = revenue_breakdown(df, "category")
    fig, ax = plt.subplots(figsize=(8, 5.5))
    ax.pie(
        categories["revenue"],
        labels=categories["category"],
        autopct="%1.0f%%",
        startangle=90,
        colors=CATEGORY_COLORS,
    )
    ax.set_title("Revenue Mix by Category", fontsize=14, fontweight="bold", pad=14)
    fig.tight_layout()
    return fig


def save_category_chart(df: pd.DataFrame, path: Path) -> None:
    """Save the category revenue mix chart.

    Parameters:
        df: Validated sales DataFrame.
        path: Output image path.

    Returns:
        None.
    """

    fig = create_category_chart(df)
    fig.savefig(path, dpi=CHART_DPI)
    plt.close(fig)


def create_region_chart(df: pd.DataFrame) -> plt.Figure:
    """Create the region revenue chart.

    Parameters:
        df: Validated sales DataFrame.

    Returns:
        Matplotlib figure.
    """

    regions = revenue_breakdown(df, "region")
    fig, ax = plt.subplots(figsize=(8, 5.5))
    ax.bar(regions["region"], regions["revenue"], color=CHART_COLORS["regions"])
    ax.set_ylabel("Revenue")
    ax.yaxis.set_major_formatter(lambda value, _: currency(value))
    style_chart(ax, "Revenue by Region")
    fig.tight_layout()
    return fig


def save_region_chart(df: pd.DataFrame, path: Path) -> None:
    """Save the region revenue chart.

    Parameters:
        df: Validated sales DataFrame.
        path: Output image path.

    Returns:
        None.
    """

    fig = create_region_chart(df)
    fig.savefig(path, dpi=CHART_DPI)
    plt.close(fig)
