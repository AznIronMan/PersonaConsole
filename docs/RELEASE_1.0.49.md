# PersonaConsole 1.0.49

## Summary

Adds Control Center detail inspectors for summarized structured controls and
clear editability posture badges.

## Changes

- Control Center cards now show `editable`, `read-only`, `disabled`, and
  `redacted` posture badges.
- Non-secret structured control values can render a collapsed `View details`
  inspector, useful for schema field-count summaries and provider route
  previews.
- Structured detail payloads defensively redact sensitive-looking keys and
  secret-looking values.
- Structured values are redacted before being mirrored into client-side
  original-value attributes.

## Verification

- `PYTHONPATH=src python3 -m pytest tests/test_control_center.py`
