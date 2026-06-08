# src/config/settings.py
# Defines reusable project settings and constants.
# Connects to: src/services/data_loader.py, src/services/charts.py, src/main.py
# Created: 2026-06-08

from pathlib import Path


DEFAULT_CSV_PATH = Path("data/sample_sales.csv")
DEFAULT_OUTPUT_DIR = Path("reports/sales_dashboard")
DEFAULT_TOP_PRODUCT_LIMIT = 5

REQUIRED_COLUMNS = {
    "order_date",
    "order_id",
    "product",
    "category",
    "region",
    "quantity",
    "unit_price",
}

CHART_DPI = 160
CHART_COLORS = {
    "monthly": "#2563EB",
    "products": "#059669",
    "regions": "#4B5563",
    "grid": "#E5E7EB",
}
CATEGORY_COLORS = ["#2563EB", "#059669", "#D97706", "#7C3AED", "#DC2626"]
