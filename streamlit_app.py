# streamlit_app.py
# Interactive Streamlit app for uploading and filtering sales dashboard data.
# Connects to: src/components/filters.py, src/services/data_loader.py, src/services/charts.py
# Created: 2026-06-08

from pathlib import Path

import pandas as pd
import streamlit as st

from src.components.filters import apply_sales_filters
from src.config.settings import DEFAULT_CSV_PATH, DEFAULT_TOP_PRODUCT_LIMIT
from src.services.analysis import revenue_breakdown, summarize_sales, top_products
from src.services.charts import (
    create_category_chart,
    create_monthly_chart,
    create_region_chart,
    create_top_products_chart,
)
from src.services.data_quality import analyze_sales_quality
from src.services.data_loader import validate_sales_data
from src.services.exporting import dataframe_to_csv_bytes, figure_to_png_bytes
from src.utils.formatting import currency


def load_default_raw_data(csv_path: Path) -> pd.DataFrame:
    """Load the bundled sample CSV for the Streamlit app.

    Parameters:
        csv_path: Path to the bundled sample CSV.

    Returns:
        Raw sales DataFrame.
    """

    return pd.read_csv(csv_path)


def load_uploaded_raw_data(uploaded_file) -> pd.DataFrame:
    """Load a Streamlit-uploaded CSV file.

    Parameters:
        uploaded_file: Uploaded CSV file-like object.

    Returns:
        Raw sales DataFrame.
    """

    return pd.read_csv(uploaded_file)


def render_quality_report(raw_df: pd.DataFrame) -> None:
    """Render a raw CSV data quality report.

    Parameters:
        raw_df: Raw sales DataFrame.

    Returns:
        None.
    """

    report = analyze_sales_quality(raw_df)
    issue_count = int(report["issues"].sum())
    if issue_count == 0:
        st.success("Data quality checks passed.")
    else:
        st.warning(f"Data quality checks found {issue_count} issue(s) to review.")

    with st.expander("Data quality report", expanded=issue_count > 0):
        st.dataframe(report, use_container_width=True)
        st.download_button(
            "Download quality report CSV",
            data=dataframe_to_csv_bytes(report),
            file_name="sales_data_quality_report.csv",
            mime="text/csv",
        )


def render_metrics(df: pd.DataFrame) -> None:
    """Render dashboard KPI metrics.

    Parameters:
        df: Filtered sales DataFrame.

    Returns:
        None.
    """

    summary = summarize_sales(df)
    columns = st.columns(5)
    columns[0].metric("Revenue", currency(summary["total_revenue"]))
    columns[1].metric("Orders", f"{summary['total_orders']:,}")
    columns[2].metric("Units", f"{summary['total_units']:,}")
    columns[3].metric("Avg Order", currency(summary["avg_order_value"]))
    columns[4].metric("Top Product", str(summary["top_product"]))


def render_exports(df: pd.DataFrame) -> None:
    """Render sidebar export buttons for filtered dashboard tables.

    Parameters:
        df: Filtered sales DataFrame.

    Returns:
        None.
    """

    st.sidebar.header("Exports")
    st.sidebar.download_button(
        "Filtered rows CSV",
        data=dataframe_to_csv_bytes(df),
        file_name="filtered_sales_rows.csv",
        mime="text/csv",
    )
    st.sidebar.download_button(
        "Top products CSV",
        data=dataframe_to_csv_bytes(top_products(df, DEFAULT_TOP_PRODUCT_LIMIT)),
        file_name="top_products.csv",
        mime="text/csv",
    )
    st.sidebar.download_button(
        "Region revenue CSV",
        data=dataframe_to_csv_bytes(revenue_breakdown(df, "region")),
        file_name="region_revenue.csv",
        mime="text/csv",
    )


def render_sidebar_filters(df: pd.DataFrame) -> pd.DataFrame:
    """Render Streamlit sidebar filters and return filtered data.

    Parameters:
        df: Validated sales DataFrame.

    Returns:
        Filtered sales DataFrame.
    """

    st.sidebar.header("Filters")
    min_date = df["order_date"].min().date()
    max_date = df["order_date"].max().date()
    date_range = st.sidebar.date_input("Date range", value=(min_date, max_date))
    if len(date_range) != 2:
        st.sidebar.warning("Select a start and end date.")
        return df.iloc[0:0]

    categories = st.sidebar.multiselect(
        "Categories",
        sorted(df["category"].unique()),
        default=sorted(df["category"].unique()),
    )
    regions = st.sidebar.multiselect(
        "Regions",
        sorted(df["region"].unique()),
        default=sorted(df["region"].unique()),
    )
    products = st.sidebar.multiselect(
        "Products",
        sorted(df["product"].unique()),
        default=sorted(df["product"].unique()),
    )

    return apply_sales_filters(
        df,
        start_date=date_range[0],
        end_date=date_range[1],
        categories=categories,
        regions=regions,
        products=products,
    )


def render_tables(df: pd.DataFrame) -> None:
    """Render product and region tables.

    Parameters:
        df: Filtered sales DataFrame.

    Returns:
        None.
    """

    left, right = st.columns(2)
    with left:
        st.subheader("Top Products")
        st.dataframe(top_products(df, DEFAULT_TOP_PRODUCT_LIMIT), use_container_width=True)
    with right:
        st.subheader("Regions")
        st.dataframe(revenue_breakdown(df, "region"), use_container_width=True)


def render_chart_download(label: str, file_name: str, fig) -> None:
    """Render a chart and matching PNG download button.

    Parameters:
        label: Button label.
        file_name: Downloaded image filename.
        fig: Matplotlib figure to render and export.

    Returns:
        None.
    """

    st.pyplot(fig)
    st.download_button(
        label,
        data=figure_to_png_bytes(fig),
        file_name=file_name,
        mime="image/png",
    )


def main() -> None:
    """Run the Streamlit dashboard app.

    Parameters:
        None.

    Returns:
        None.
    """

    st.set_page_config(page_title="Sales Dashboard", layout="wide")
    st.title("Sales Dashboard")
    st.caption("Upload a CSV or explore the bundled sample data.")

    uploaded_file = st.sidebar.file_uploader("Upload sales CSV", type=["csv"])
    try:
        raw_df = (
            load_uploaded_raw_data(uploaded_file)
            if uploaded_file
            else load_default_raw_data(DEFAULT_CSV_PATH)
        )
        render_quality_report(raw_df)
        df = validate_sales_data(raw_df)
    except ValueError as error:
        st.error(str(error))
        return

    filtered = render_sidebar_filters(df)
    if filtered.empty:
        st.warning("No sales rows match the current filters.")
        return

    render_metrics(filtered)
    render_exports(filtered)
    render_chart_download(
        "Download monthly chart PNG",
        "monthly_revenue.png",
        create_monthly_chart(filtered),
    )

    left, right = st.columns(2)
    with left:
        render_chart_download(
            "Download top products chart PNG",
            "top_products.png",
            create_top_products_chart(filtered, DEFAULT_TOP_PRODUCT_LIMIT),
        )
        render_chart_download(
            "Download region chart PNG",
            "region_revenue.png",
            create_region_chart(filtered),
        )
    with right:
        render_chart_download(
            "Download category chart PNG",
            "category_mix.png",
            create_category_chart(filtered),
        )
        render_tables(filtered)


if __name__ == "__main__":
    main()
