# generate_sales_csv.py
# CLI script that creates randomized sales CSV data for upload testing.
# Connects to: src/services/template_generator.py
# Created: 2026-06-08

from pathlib import Path
import argparse

from src.config.settings import DEFAULT_GENERATED_CSV_PATH, DEFAULT_TEMPLATE_PATH
from src.services.template_generator import (
    DEFAULT_RANDOM_ROW_COUNT,
    generate_random_sales_csv,
    generate_sales_template,
)


def parse_args() -> argparse.Namespace:
    """Parse command-line arguments for sales CSV generation.

    Parameters:
        None.

    Returns:
        Parsed argument namespace.
    """

    parser = argparse.ArgumentParser(description="Generate randomized sales CSV data.")
    parser.add_argument(
        "--output",
        type=Path,
        default=DEFAULT_GENERATED_CSV_PATH,
        help="Output path for the generated CSV.",
    )
    parser.add_argument(
        "--rows",
        type=int,
        default=DEFAULT_RANDOM_ROW_COUNT,
        help="Number of randomized sales rows to generate.",
    )
    parser.add_argument(
        "--seed",
        type=int,
        default=None,
        help="Optional random seed for repeatable generated data.",
    )
    parser.add_argument(
        "--blank-template",
        action="store_true",
        help=f"Write a blank fill-in template instead of random data. Defaults to {DEFAULT_TEMPLATE_PATH}.",
    )
    return parser.parse_args()


def main() -> None:
    """Run the sales CSV generator.

    Parameters:
        None.

    Returns:
        None.
    """

    args = parse_args()
    if args.blank_template:
        output_path = generate_sales_template(DEFAULT_TEMPLATE_PATH if args.output == DEFAULT_GENERATED_CSV_PATH else args.output)
        print(f"Sales CSV template written to: {output_path}")
        return

    output_path = generate_random_sales_csv(args.output, args.rows, args.seed)
    print(f"Random sales CSV written to: {output_path}")


if __name__ == "__main__":
    main()
