# Deployment Guide

This guide documents the deployment path for the interactive Streamlit dashboard.

## App Entry Point

Use these settings when deploying the app:

```text
Main file: streamlit_app.py
Requirements file: requirements.txt
Python version: 3.12 or newer
```

No environment variables, secrets, database, or external API keys are required.

## Pre-Deploy Checklist

Run these commands before deploying:

```powershell
python -m unittest discover -s tests
python sales_dashboard.py
streamlit run streamlit_app.py
```

Confirm:

- Unit tests pass.
- The static dashboard generates in `reports/sales_dashboard/`.
- The Streamlit app opens locally.
- Uploading `data/sample_sales.csv` works.
- Download buttons work for CSV and PNG exports.

## Streamlit Hosting Notes

When connecting the GitHub repository to a Streamlit host:

- Select the `main` branch.
- Set the app file to `streamlit_app.py`.
- Let the host install packages from `requirements.txt`.
- Do not configure secrets unless future iterations add external services.

## Post-Deploy Validation

After the app is deployed:

1. Open the public app URL.
2. Confirm the default sample data loads.
3. Download `Generated sample CSV` from the sidebar.
4. Upload that generated CSV back into the app.
5. Change date, category, region, and product filters.
6. Download at least one CSV export and one PNG export.
7. Confirm the GitHub README `Deployed` section includes the public URL.

## Public URL

The deployed app is available at:

```text
https://sales-dashboard-b6bdiftbheiwl5grx4ty9x.streamlit.app/
```
