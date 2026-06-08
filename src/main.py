# src/main.py
# Parses CLI arguments and runs dashboard generation.
# Connects to: src/config/settings.py, src/services/dashboard.py
# Created: 2026-06-08

from pathlib import Path
import argparse
import logging

from src.config.settings import (
    DEFAULT_CSV_PATH,
    DEFAULT_OUTPUT_DIR,
    DEFAULT_TOP_PRODUCT_LIMIT,
)
from src.services.dashboard import generate_dashboard


def configure_logging() -> None:
    """Configure basic structured logging for command-line runs.

    Parameters:
        None.

    Returns:
        None.
    """

    logging.basicConfig(
        level=logging.INFO,
        format="%(asctime)s %(levelname)s %(name)s %(message)s",
    )


def parse_args() -> argparse.Namespace:
    """Parse command-line arguments for dashboard generation.

    Parameters:
        None.

    Returns:
        Parsed argument namespace.
    """

    parser = argparse.ArgumentParser(description="Generate a sales dashboard from a CSV file.")
    parser.add_argument("--csv", type=Path, default=DEFAULT_CSV_PATH, help="Path to the sales CSV.")
    parser.add_argument("--output", type=Path, default=DEFAULT_OUTPUT_DIR, help="Output folder.")
    parser.add_argument("--top-n", type=int, default=DEFAULT_TOP_PRODUCT_LIMIT, help="Number of top products to chart.")
    return parser.parse_args()


def main() -> None:
    """Run the sales dashboard command-line workflow.

    Parameters:
        None.

    Returns:
        None.
    """

    configure_logging()
    args = parse_args()
    artifacts = generate_dashboard(args.csv, args.output, top_n=args.top_n)
    print(f"Dashboard report: {artifacts.report_path}")
    for name, path in artifacts.charts.items():
        print(f"{name.title()} chart: {path}")
