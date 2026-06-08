# Changelog

## Iteration 1 - 2026-06-08

### Added

- Created a CSV-driven sales dashboard generator.
- Added pandas analysis for revenue, orders, units sold, average order value, monthly trends, top products, category revenue, and regional revenue.
- Added matplotlib chart generation for monthly revenue, top products, category mix, and regional revenue.
- Added a static HTML report output.
- Added sample sales data for local testing.
- Added unit tests for CSV loading, validation, monthly revenue, summary metrics, and product ranking.
- Added project documentation, dependency list, Git ignore rules, and an environment template.

### Changed

- Refactored the initial single-file script into a modular `src/` structure for clearer separation of concerns.
- Updated documentation language to describe the build and its purpose without portfolio positioning.

## Iteration 1.1 - 2026-06-08

### Changed

- Updated the monthly revenue chart to plot real datetime values instead of date-like strings.
- Removed noisy matplotlib category logging during dashboard generation.

## Iteration 2 - 2026-06-08

### Added

- Added an interactive Streamlit dashboard.
- Added CSV upload support for interactive analysis.
- Added date, category, region, and product filters.
- Added reusable filter logic and tests.

### Changed

- Updated chart functions so the static report and Streamlit app can reuse the same matplotlib figure builders.

## Iteration 3 - 2026-06-08

### Added

- Added a data quality report for raw sales CSV files.
- Added checks for missing required columns, blank required values, invalid dates, invalid numbers, negative quantities, nonpositive unit prices, duplicate order IDs, and invalid revenue values.
- Added Streamlit display for the data quality report.
- Added tests for data quality issue detection.

## Iteration 4 - 2026-06-08

### Added

- Added CSV exports for filtered rows, top products, region revenue, and the data quality report.
- Added PNG exports for monthly revenue, top products, category mix, and region revenue charts.
- Added reusable export helpers and tests for CSV and PNG export output.

## Iteration 5 - 2026-06-08

### Added

- Added CSV column mapping for uploaded files with different header names.
- Added a random sales CSV generator script for upload testing.
- Added support for row counts, optional random seeds, and blank templates.
- Added tests for column mapping and template generation.

## Iteration 6 - 2026-06-08

### Added

- Added Streamlit sidebar downloads for a blank sales CSV template and generated sample sales data.
- Added a test that confirms the in-app generated sample data validates successfully.
