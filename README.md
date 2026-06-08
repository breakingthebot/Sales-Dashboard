# Sales Dashboard

A Python data project that turns a sales CSV into a static dashboard with summary metrics, trend charts, and product performance tables.

The point of this build is to make raw sales records easier to understand quickly. Instead of reading rows in a spreadsheet, the script validates the data, calculates the most useful sales metrics, and produces a clean report that can be opened in any browser.

## Stack

- Python
- pandas
- matplotlib
- unittest
- GitHub Actions

## Features

- Validates required CSV fields before analysis.
- Calculates total revenue, total orders, units sold, average order value, and top product.
- Builds monthly revenue trends, top product rankings, category mix, and regional revenue charts.
- Generates a responsive `index.html` report.
- Includes unit tests for loading, validation, and core analytics.

## Project Structure

```text
.
|-- src/
|   |-- config/
|   |-- models/
|   |-- services/
|   `-- utils/
|-- .github/
|   `-- workflows/
|-- data/
|   `-- sample_sales.csv
|-- tests/
|   `-- test_sales_dashboard.py
|-- sales_dashboard.py
|-- CHANGELOG.md
|-- .env.example
|-- requirements.txt
|-- .gitignore
`-- README.md
```

## CSV Format

The dashboard expects these columns:

| Column | Description |
| --- | --- |
| `order_date` | Date of the sale. |
| `order_id` | Unique order identifier. |
| `product` | Product name. |
| `category` | Product category. |
| `region` | Sales region. |
| `quantity` | Units sold. |
| `unit_price` | Price per unit. |

An optional `revenue` column can be provided. If it is missing, revenue is calculated as `quantity * unit_price`.

## Environment Variables

No environment variables are required for the current version. See `.env.example` for the current template.

## Setup

```powershell
python -m venv .venv
.\.venv\Scripts\Activate.ps1
pip install -r requirements.txt
```

## Running Locally

```powershell
python sales_dashboard.py
```

The generated dashboard will be written to:

```text
reports/sales_dashboard/index.html
```

To use a custom CSV:

```powershell
python sales_dashboard.py --csv path\to\sales.csv --output reports\custom_dashboard --top-n 10
```

## Testing

```powershell
python -m unittest discover -s tests
```

## Automated Checks

GitHub Actions runs the test workflow on branch pushes and pull requests to `main`. The workflow installs dependencies, runs the unit tests, and generates the dashboard to confirm the command-line build still works.

## Deployed

Not deployed. This build currently generates a local static HTML report.

## Architecture Notes

The build is split into small modules so each part has one job. CSV validation lives in the data loader, sales calculations live in the analysis service, chart rendering lives in the charts service, and report creation lives in the report service. The root `sales_dashboard.py` file stays small so it only starts the command-line workflow.

This structure makes the project easier to test and easier to extend. For example, a future interactive app can reuse the same analysis functions without rewriting the CSV validation or chart logic.

## Notes

- The generated `reports/` folder is ignored by Git because it is build output.
- The sample CSV is included so the dashboard can run immediately after dependencies are installed.
- A working Python installation is required before setup commands can run.

## Changelog

See `CHANGELOG.md`.

## Iteration 1 Test Steps

1. Create and activate a virtual environment.
2. Install dependencies with `pip install -r requirements.txt`.
3. Run `python sales_dashboard.py`.
4. Open `reports/sales_dashboard/index.html` in a browser.
5. Confirm the KPI cards, monthly trend chart, top products chart, category chart, and region chart render correctly.
6. Run `python -m unittest discover -s tests` and confirm all tests pass.

## Iteration 1.1 Test Steps

1. Run `python sales_dashboard.py`.
2. Confirm the dashboard still writes `reports/sales_dashboard/index.html`.
3. Confirm the terminal no longer shows `matplotlib.category` INFO messages.
4. Open the dashboard and confirm the monthly revenue chart still uses readable month labels.

## Iteration 2 Test Steps

1. Run `python -m unittest discover -s tests`.
2. Run `python sales_dashboard.py`.
3. Commit and push the workflow file.
4. Open the GitHub repository Actions tab.
5. Confirm the `Tests` workflow completes successfully.

## Next Iteration Suggestions

- Add an interactive Streamlit interface with CSV upload, filters for date range and region, and live chart updates.
- Add export options for dashboard images and summary tables.
- Add a richer data quality report for missing values, negative quantities, duplicate order IDs, and outlier prices.
