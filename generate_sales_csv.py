# generate_sales_csv.py
# CLI script that creates a fill-in sales CSV template.
# Connects to: src/services/template_generator.py
# Created: 2026-06-08

from pathlib import Path
import argparse

from src.config.settings import DEFAULT_TEMPLATE_PATH
from src.services.template_generator import generate_sales_template


def parse_args() -> argparse.Namespace:
    """Parse command-line arguments for sales CSV template generation.

    Parameters:
        None.

    Returns:
        Parsed argument namespace.
    """

    parser = argparse.ArgumentParser(description="Generate a sales CSV template.")
    parser.add_argument(
        "--output",
        type=Path,
        default=DEFAULT_TEMPLATE_PATH,
        help="Output path for the generated CSV template.",
    )
    parser.add_argument(
        "--with-sample-rows",
        action="store_true",
        help="Include example rows in the generated template.",
    )
    return parser.parse_args()


def main() -> None:
    """Run the sales CSV template generator.

    Parameters:
        None.

    Returns:
        None.
    """

    args = parse_args()
    output_path = generate_sales_template(args.output, args.with_sample_rows)
    print(f"Sales CSV template written to: {output_path}")


if __name__ == "__main__":
    main()
