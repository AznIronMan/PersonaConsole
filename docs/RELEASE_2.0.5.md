# PersonaConsole 2.0.5

PersonaConsole 2.0.5 polishes the shared v2 shell navigation after live
consumer visual QA found that the standard section nav could expose a horizontal
scrollbar and clip its final item when status controls were present.

Changed:

- Kept v2 navigation horizontally scrollable for narrow layouts while hiding the
  visible scrollbar.
- Tightened v2 topbar and nav item spacing so the standard nav fits better with
  status controls on desktop.
- Added regression coverage for the shared v2 nav scrollbar contract.

Verification:

```bash
PYTHONPATH=src python -m pytest tests/test_v2_console.py tests/test_doctor.py tests/test_imports.py
```
