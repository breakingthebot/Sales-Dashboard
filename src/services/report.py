# src/services/report.py
# Builds the static HTML dashboard report from analysis tables and charts.
# Connects to: src/services/analysis.py, src/services/dashboard.py
# Created: 2026-06-08

from pathlib import Path
from typing import Iterable

import pandas as pd

from src.services.analysis import revenue_breakdown, summarize_sales, top_products
from src.utils.formatting import currency


def table_rows(records: Iterable[dict[str, object]]) -> str:
    """Render table body rows for report tables.

    Parameters:
        records: Iterable of display records with name, revenue, and optional units.

    Returns:
        HTML table row string.
    """

    return "\n".join(
        "<tr>"
        f"<td>{record['name']}</td>"
        f"<td>{currency(float(record['revenue']))}</td>"
        f"<td>{int(record.get('units', 0)) if 'units' in record else ''}</td>"
        "</tr>"
        for record in records
    )


def build_report(
    df: pd.DataFrame,
    charts: dict[str, Path],
    report_path: Path,
    source_csv: Path,
    top_n: int,
) -> None:
    """Write the static HTML dashboard report.

    Parameters:
        df: Validated sales DataFrame.
        charts: Mapping of chart names to image paths.
        report_path: HTML report path to write.
        source_csv: CSV file used to generate the report.
        top_n: Number of products shown in the ranking table.

    Returns:
        None.
    """

    summary = summarize_sales(df)
    products = top_products(df, limit=top_n)
    regions = revenue_breakdown(df, "region")
    product_rows = table_rows(
        {"name": row.product, "revenue": row.revenue, "units": row.units}
        for row in products.itertuples(index=False)
    )
    region_rows = table_rows(
        {"name": row.region, "revenue": row.revenue}
        for row in regions.itertuples(index=False)
    )
    chart_paths = {name: path.name for name, path in charts.items()}

    html = f"""<!doctype html>
<html lang="en">
<head>
  <meta charset="utf-8">
  <meta name="viewport" content="width=device-width, initial-scale=1">
  <title>Sales Dashboard</title>
  <style>
    :root {{
      color-scheme: light;
      --bg: #f8fafc;
      --panel: #ffffff;
      --ink: #111827;
      --muted: #6b7280;
      --line: #e5e7eb;
    }}
    body {{
      margin: 0;
      background: var(--bg);
      color: var(--ink);
      font-family: Arial, Helvetica, sans-serif;
    }}
    main {{
      max-width: 1180px;
      margin: 0 auto;
      padding: 32px 20px 48px;
    }}
    header {{
      border-bottom: 1px solid var(--line);
      margin-bottom: 24px;
      padding-bottom: 18px;
    }}
    h1 {{
      margin: 0 0 8px;
      font-size: clamp(2rem, 4vw, 3.2rem);
      letter-spacing: 0;
    }}
    h2 {{
      margin: 0 0 14px;
      font-size: 1.05rem;
      letter-spacing: 0;
    }}
    p {{
      margin: 0;
      color: var(--muted);
    }}
    .metrics {{
      display: grid;
      grid-template-columns: repeat(auto-fit, minmax(180px, 1fr));
      gap: 14px;
      margin: 24px 0;
    }}
    .metric,
    .panel {{
      background: var(--panel);
      border: 1px solid var(--line);
      border-radius: 8px;
      box-shadow: 0 1px 2px rgba(15, 23, 42, 0.05);
    }}
    .metric {{
      padding: 18px;
    }}
    .label {{
      color: var(--muted);
      font-size: 0.85rem;
      margin-bottom: 8px;
    }}
    .value {{
      font-size: 1.6rem;
      font-weight: 700;
    }}
    .grid {{
      display: grid;
      grid-template-columns: repeat(2, minmax(0, 1fr));
      gap: 18px;
    }}
    .panel {{
      padding: 18px;
    }}
    .wide {{
      grid-column: 1 / -1;
    }}
    img {{
      display: block;
      width: 100%;
      height: auto;
    }}
    table {{
      border-collapse: collapse;
      width: 100%;
    }}
    th,
    td {{
      border-bottom: 1px solid var(--line);
      padding: 10px 8px;
      text-align: left;
      white-space: nowrap;
    }}
    th {{
      color: var(--muted);
      font-size: 0.85rem;
      font-weight: 700;
    }}
    @media (max-width: 780px) {{
      main {{
        padding: 24px 14px 36px;
      }}
      .grid {{
        grid-template-columns: 1fr;
      }}
      th,
      td {{
        white-space: normal;
      }}
    }}
  </style>
</head>
<body>
  <main>
    <header>
      <h1>Sales Dashboard</h1>
      <p>Generated from {source_csv.name} with pandas analysis and matplotlib charts.</p>
    </header>

    <section class="metrics" aria-label="Sales summary">
      <div class="metric"><div class="label">Total Revenue</div><div class="value">{currency(summary["total_revenue"])}</div></div>
      <div class="metric"><div class="label">Orders</div><div class="value">{summary["total_orders"]:,}</div></div>
      <div class="metric"><div class="label">Units Sold</div><div class="value">{summary["total_units"]:,}</div></div>
      <div class="metric"><div class="label">Average Order Value</div><div class="value">{currency(summary["avg_order_value"])}</div></div>
      <div class="metric"><div class="label">Top Product</div><div class="value">{summary["top_product"]}</div></div>
    </section>

    <section class="grid">
      <article class="panel wide"><img src="{chart_paths["monthly"]}" alt="Revenue trend by month"></article>
      <article class="panel"><img src="{chart_paths["products"]}" alt="Top products by revenue"></article>
      <article class="panel"><img src="{chart_paths["categories"]}" alt="Revenue mix by category"></article>
      <article class="panel"><img src="{chart_paths["regions"]}" alt="Revenue by region"></article>
      <article class="panel">
        <h2>Top Products</h2>
        <table>
          <thead><tr><th>Product</th><th>Revenue</th><th>Units</th></tr></thead>
          <tbody>{product_rows}</tbody>
        </table>
      </article>
      <article class="panel">
        <h2>Regions</h2>
        <table>
          <thead><tr><th>Region</th><th>Revenue</th><th></th></tr></thead>
          <tbody>{region_rows}</tbody>
        </table>
      </article>
    </section>
  </main>
</body>
</html>
"""
    report_path.write_text(html, encoding="utf-8")
