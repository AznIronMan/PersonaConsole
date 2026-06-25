# PersonaCore 1.0.4

`1.0.4` is a public-safe patch release focused on consumer shell
deduplication. It keeps private routes, auth, databases, and runtime state in
consumer repositories while adding shared helpers for a repeated dashboard
summary-card pattern.

## Changes

- Added `DashboardMetricSpec` for declaring generic dashboard count/status
  cards.
- Added `dashboard_metrics_from_counts(...)` to build `DashboardMetric` rows
  from consumer-owned count mappings.
- Added `render_dashboard_summary_grid(...)` as a direct summary-grid helper.
- Added `format_dashboard_metric_value(...)` for compact count/text/raw display
  values.
- Re-exported the helpers through both `personacore` and the compatibility
  `persona_console` import path.

## Verification

- `PYTHONPATH=src python -m pytest tests`
- `PYTHONPATH=src python -m py_compile src/persona_console/*.py src/personacore/*.py`
- `scripts/export_public_baseline.sh /tmp/personacore-public-export.*`
