# PersonaConsole 1.0.40

`1.0.40` expands the generic admin password-change renderer so consumers can
preserve current-password challenge forms without keeping a bespoke auth page.

## Highlights

- Added optional current-password field configuration to
  `AdminPasswordChangePageConfig`.
- Added optional password input constraints for PIN-style forms, including
  min/max length, pattern, and input mode.
- Kept existing password-change consumers unchanged when the new fields are not
  configured.

## Verification

```bash
PYTHONPATH=src python3 -m pytest tests
PYTHONPATH=src python3 scripts/consumer_integration_doctor.py --expected-version 1.0.40
```
