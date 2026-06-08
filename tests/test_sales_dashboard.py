from pathlib import Path
from datetime import date
import tempfile
import unittest

import pandas as pd

from src.components.filters import apply_sales_filters
from src.services.analysis import monthly_revenue, summarize_sales, top_products
from src.services.data_quality import analyze_sales_quality
from src.services.data_loader import load_sales_data, validate_sales_data


class SalesDashboardTestCase(unittest.TestCase):
    def write_csv(self, content: str) -> Path:
        temp_dir = tempfile.TemporaryDirectory()
        self.addCleanup(temp_dir.cleanup)
        path = Path(temp_dir.name) / "sales.csv"
        path.write_text(content, encoding="utf-8")
        return path

    def test_load_sales_data_adds_revenue_and_month(self):
        path = self.write_csv(
            "order_date,order_id,product,category,region,quantity,unit_price\n"
            "2025-01-01,SO-1,Laptop,Computers,West,2,1000\n"
        )

        df = load_sales_data(path)

        self.assertEqual(df.loc[0, "revenue"], 2000)
        self.assertEqual(df.loc[0, "month"], pd.Timestamp("2025-01-01"))

    def test_summary_metrics(self):
        path = self.write_csv(
            "order_date,order_id,product,category,region,quantity,unit_price\n"
            "2025-01-01,SO-1,Laptop,Computers,West,2,1000\n"
            "2025-01-02,SO-2,Mouse,Accessories,East,5,20\n"
        )

        summary = summarize_sales(load_sales_data(path))

        self.assertEqual(summary["total_revenue"], 2100)
        self.assertEqual(summary["total_orders"], 2)
        self.assertEqual(summary["total_units"], 7)
        self.assertEqual(summary["avg_order_value"], 1050)
        self.assertEqual(summary["top_product"], "Laptop")

    def test_monthly_revenue_groups_by_month(self):
        path = self.write_csv(
            "order_date,order_id,product,category,region,quantity,unit_price\n"
            "2025-01-01,SO-1,Laptop,Computers,West,2,1000\n"
            "2025-01-15,SO-2,Mouse,Accessories,East,5,20\n"
            "2025-02-01,SO-3,Desk,Furniture,North,1,500\n"
        )

        monthly = monthly_revenue(load_sales_data(path))

        self.assertEqual(monthly["revenue"].tolist(), [2100, 500])

    def test_top_products_orders_by_revenue(self):
        path = self.write_csv(
            "order_date,order_id,product,category,region,quantity,unit_price\n"
            "2025-01-01,SO-1,Laptop,Computers,West,1,1000\n"
            "2025-01-02,SO-2,Mouse,Accessories,East,50,20\n"
            "2025-01-03,SO-3,Desk,Furniture,North,1,500\n"
        )

        products = top_products(load_sales_data(path), limit=2)

        self.assertEqual(products["product"].tolist(), ["Laptop", "Mouse"])

    def test_missing_required_columns_raises_clear_error(self):
        path = self.write_csv("order_date,order_id,product\n2025-01-01,SO-1,Laptop\n")

        with self.assertRaisesRegex(ValueError, "missing required columns"):
            load_sales_data(path)

    def test_validate_sales_data_accepts_dataframe_input(self):
        df = pd.DataFrame(
            [
                {
                    "order_date": "2025-01-01",
                    "order_id": "SO-1",
                    "product": "Laptop",
                    "category": "Computers",
                    "region": "West",
                    "quantity": 2,
                    "unit_price": 1000,
                }
            ]
        )

        validated = validate_sales_data(df)

        self.assertEqual(validated.loc[0, "revenue"], 2000)

    def test_apply_sales_filters_filters_by_selected_values(self):
        path = self.write_csv(
            "order_date,order_id,product,category,region,quantity,unit_price\n"
            "2025-01-01,SO-1,Laptop,Computers,West,2,1000\n"
            "2025-02-01,SO-2,Mouse,Accessories,East,5,20\n"
            "2025-03-01,SO-3,Desk,Furniture,North,1,500\n"
        )

        filtered = apply_sales_filters(
            load_sales_data(path),
            start_date=date(2025, 1, 1),
            end_date=date(2025, 2, 28),
            categories=["Accessories"],
            regions=["East"],
            products=["Mouse"],
        )

        self.assertEqual(filtered["order_id"].tolist(), ["SO-2"])

    def test_analyze_sales_quality_flags_common_issues(self):
        df = pd.DataFrame(
            [
                {
                    "order_date": "not-a-date",
                    "order_id": "SO-1",
                    "product": "Laptop",
                    "category": "Computers",
                    "region": "West",
                    "quantity": -2,
                    "unit_price": 0,
                },
                {
                    "order_date": "2025-01-02",
                    "order_id": "SO-1",
                    "product": "Mouse",
                    "category": "Accessories",
                    "region": "East",
                    "quantity": 5,
                    "unit_price": 20,
                },
            ]
        )

        report = analyze_sales_quality(df).set_index("check")

        self.assertEqual(report.loc["Invalid order dates", "issues"], 1)
        self.assertEqual(report.loc["Negative quantities", "issues"], 1)
        self.assertEqual(report.loc["Nonpositive unit prices", "issues"], 1)
        self.assertEqual(report.loc["Duplicate order IDs", "issues"], 1)

    def test_analyze_sales_quality_flags_missing_columns(self):
        report = analyze_sales_quality(pd.DataFrame({"order_date": ["2025-01-01"]}))

        required_columns = report.set_index("check").loc["Required columns"]

        self.assertEqual(required_columns["status"], "Review")
        self.assertGreater(required_columns["issues"], 0)


if __name__ == "__main__":
    unittest.main()
