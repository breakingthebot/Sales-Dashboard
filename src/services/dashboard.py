# src/services/dashboard.py
# Coordinates sales data loading, chart generation, and report creation.
# Connects to: src/services/data_loader.py, src/services/charts.py, src/services/report.py
# Created: 2026-06-08

from pathlib import Path
import logging

from src.models.artifacts import DashboardArtifacts
from src.services.charts import (
    save_category_chart,
    save_monthly_chart,
    save_region_chart,
    save_top_products_chart,
)
from src.services.data_loader import load_sales_data
from src.services.report import build_report


logger = logging.getLogger(__name__)


def generate_dashboard(csv_path: Path, output_dir: Path, top_n: int = 5) -> DashboardArtifacts:
    """Generate charts and an HTML report from a sales CSV.

    Parameters:
        csv_path: Path to the sales CSV.
        output_dir: Folder where output files should be written.
        top_n: Number of top products to chart.

    Returns:
        DashboardArtifacts describing generated files.
    """

    logger.info("Generating dashboard from %s into %s", csv_path, output_dir)
    df = load_sales_data(csv_path)
    output_dir.mkdir(parents=True, exist_ok=True)

    charts = {
        "monthly": output_dir / "monthly_revenue.png",
        "products": output_dir / "top_products.png",
        "categories": output_dir / "category_mix.png",
        "regions": output_dir / "region_revenue.png",
    }

    save_monthly_chart(df, charts["monthly"])
    save_top_products_chart(df, charts["products"], limit=top_n)
    save_category_chart(df, charts["categories"])
    save_region_chart(df, charts["regions"])

    report_path = output_dir / "index.html"
    build_report(df, charts, report_path, csv_path, top_n=top_n)
    logger.info("Dashboard report written to %s", report_path)
    return DashboardArtifacts(output_dir=output_dir, charts=charts, report_path=report_path)
