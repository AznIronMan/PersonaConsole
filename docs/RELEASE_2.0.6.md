# PersonaConsole 2.0.6

PersonaConsole 2.0.6 adds an optional v2 static asset cache key so consuming
runtimes can invalidate the shared v2 stylesheet and script when their mounted
PersonaConsole source changes.

Changed:

- Added `V2ConsoleConfig.static_version`.
- Appended `?v=<static_version>` to the shared v2 CSS and JS links when a
  consumer supplies a cache key.
- Added regression coverage for versioned v2 asset URLs.

Verification:

```bash
PYTHONPATH=src python -m pytest tests/test_v2_console.py tests/test_doctor.py tests/test_imports.py
```
