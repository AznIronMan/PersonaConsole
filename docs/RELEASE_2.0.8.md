# PersonaConsole 2.0.8

PersonaConsole 2.0.8 hardens v2 structured table hover cards so hidden hover
templates cannot leak into table layout.

## Changes

- Strengthened the `[data-pcv2-hover-template]` CSS rule with structured-cell
  selectors and `display: none !important`.
- Added regression coverage for hover templates inside v2 identity/status
  table cells.

## Verification

- `PYTHONPATH=src python3 -m pytest tests/test_v2_console.py tests/test_doctor.py tests/test_imports.py -q`
- `PYTHONPATH=src python3 -m pytest tests -q`
