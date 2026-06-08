# src/utils/formatting.py
# Provides display formatting helpers for dashboard output.
# Connects to: src/services/charts.py, src/services/report.py
# Created: 2026-06-08


def currency(value: float) -> str:
    """Format a numeric value as whole-dollar currency.

    Parameters:
        value: Numeric value to format.

    Returns:
        Currency-formatted string.
    """

    return f"${value:,.0f}"
