from pathlib import Path
import tempfile
import unittest

import pandas as pd

from src.services.analysis import monthly_revenue, summarize_sales, top_products
from src.services.data_loader import load_sales_data


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


if __name__ == "__main__":
    unittest.main()
