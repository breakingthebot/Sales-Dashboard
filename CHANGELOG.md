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
