# src/services/data_quality.py
# Audits raw sales CSV data for quality issues before dashboard validation.
# Connects to: src/config/settings.py, streamlit_app.py, tests/test_sales_dashboard.py
# Created: 2026-06-08

import pandas as pd

from src.config.settings import REQUIRED_COLUMNS


def count_invalid_dates(df: pd.DataFrame, column: str) -> int:
    """Count values that cannot be parsed as dates.

    Parameters:
        df: Raw sales DataFrame.
        column: Date column to inspect.

    Returns:
        Number of invalid non-empty date values.
    """

    if column not in df.columns:
        return 0
    values = df[column].dropna()
    parsed = pd.to_datetime(values, errors="coerce", format="mixed")
    return int(parsed.isna().sum())


def count_invalid_numbers(df: pd.DataFrame, column: str) -> int:
    """Count values that cannot be parsed as numbers.

    Parameters:
        df: Raw sales DataFrame.
        column: Numeric column to inspect.

    Returns:
        Number of invalid non-empty numeric values.
    """

    if column not in df.columns:
        return 0
    values = df[column].dropna()
    parsed = pd.to_numeric(values, errors="coerce")
    return int(parsed.isna().sum())


def count_negative_numbers(df: pd.DataFrame, column: str) -> int:
    """Count numeric values below zero.

    Parameters:
        df: Raw sales DataFrame.
        column: Numeric column to inspect.

    Returns:
        Number of negative values.
    """

    if column not in df.columns:
        return 0
    values = pd.to_numeric(df[column], errors="coerce")
    return int((values < 0).sum())


def count_nonpositive_numbers(df: pd.DataFrame, column: str) -> int:
    """Count numeric values less than or equal to zero.

    Parameters:
        df: Raw sales DataFrame.
        column: Numeric column to inspect.

    Returns:
        Number of nonpositive values.
    """

    if column not in df.columns:
        return 0
    values = pd.to_numeric(df[column], errors="coerce")
    return int((values <= 0).sum())


def count_duplicate_order_ids(df: pd.DataFrame) -> int:
    """Count duplicate order ID rows.

    Parameters:
        df: Raw sales DataFrame.

    Returns:
        Number of rows with duplicate order IDs beyond the first occurrence.
    """

    if "order_id" not in df.columns:
        return 0
    return int(df["order_id"].duplicated().sum())


def build_quality_row(check: str, issue_count: int, guidance: str) -> dict[str, object]:
    """Build a display row for the quality report.

    Parameters:
        check: Name of the quality check.
        issue_count: Number of issues found.
        guidance: Plain-English next step.

    Returns:
        Dictionary suitable for table display.
    """

    return {
        "check": check,
        "status": "Pass" if issue_count == 0 else "Review",
        "issues": issue_count,
        "guidance": guidance,
    }


def analyze_sales_quality(df: pd.DataFrame) -> pd.DataFrame:
    """Return a quality report for raw sales CSV data.

    Parameters:
        df: Raw sales DataFrame.

    Returns:
        DataFrame of quality checks, statuses, issue counts, and guidance.
    """

    missing_columns = sorted(REQUIRED_COLUMNS - set(df.columns))
    null_required_count = (
        int(df[list(REQUIRED_COLUMNS)].isna().sum().sum())
        if not missing_columns
        else 0
    )

    rows = [
        build_quality_row(
            "Required columns",
            len(missing_columns),
            "Add missing columns: " + ", ".join(missing_columns)
            if missing_columns
            else "All required columns are present.",
        ),
        build_quality_row(
            "Blank required values",
            null_required_count,
            "Fill blank cells in required columns.",
        ),
        build_quality_row(
            "Invalid order dates",
            count_invalid_dates(df, "order_date"),
            "Use a recognizable date format such as 2026-01-15.",
        ),
        build_quality_row(
            "Invalid quantities",
            count_invalid_numbers(df, "quantity"),
            "Use numeric quantity values.",
        ),
        build_quality_row(
            "Negative quantities",
            count_negative_numbers(df, "quantity"),
            "Quantity should be zero or greater.",
        ),
        build_quality_row(
            "Invalid unit prices",
            count_invalid_numbers(df, "unit_price"),
            "Use numeric unit price values.",
        ),
        build_quality_row(
            "Nonpositive unit prices",
            count_nonpositive_numbers(df, "unit_price"),
            "Unit price should be greater than zero.",
        ),
        build_quality_row(
            "Duplicate order IDs",
            count_duplicate_order_ids(df),
            "Confirm whether repeated order IDs are intentional.",
        ),
    ]

    if "revenue" in df.columns:
        rows.append(
            build_quality_row(
                "Invalid revenue values",
                count_invalid_numbers(df, "revenue"),
                "Use numeric revenue values or remove the revenue column.",
            )
        )

    return pd.DataFrame(rows)
