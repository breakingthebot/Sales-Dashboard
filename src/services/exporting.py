# src/services/exporting.py
# Converts dashboard data and charts into downloadable file bytes.
# Connects to: streamlit_app.py, tests/test_sales_dashboard.py
# Created: 2026-06-08

from io import BytesIO

import pandas as pd
from matplotlib.figure import Figure


def dataframe_to_csv_bytes(df: pd.DataFrame) -> bytes:
    """Convert a DataFrame into UTF-8 CSV bytes.

    Parameters:
        df: DataFrame to export.

    Returns:
        CSV content as bytes.
    """

    return df.to_csv(index=False).encode("utf-8")


def figure_to_png_bytes(fig: Figure) -> bytes:
    """Convert a matplotlib figure into PNG bytes.

    Parameters:
        fig: Matplotlib figure to export.

    Returns:
        PNG image bytes.
    """

    buffer = BytesIO()
    fig.savefig(buffer, format="png", dpi=160, bbox_inches="tight")
    buffer.seek(0)
    return buffer.getvalue()
