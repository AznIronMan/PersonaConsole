# PersonaConsole 1.0.47

`1.0.47` adds the shared Control Center surface for curated, staged
configuration controls across PersonaConsole, PersonaEngine, and consumer
runtimes.

## Highlights

- Added `CONTROL_CENTER_FEATURE`, `ControlCenterConfig`, `ControlSection`,
  `ControlGroup`, `ControlItem`, `ControlOption`, and `ControlChange`.
- Added `render_control_center(...)`, `control_center_feature_enabled(...)`,
  and `build_control_center_from_sources(...)`.
- Added switch-card rendering for feature flags, compact controls for enums and
  numbers, redacted secret posture, staged diff previews, restart badges, and
  runtime-owned action slots.
- Added fixture routes under `/control`, including Features, Runtime,
  Persona, Appearance, Integrations, and Audit views while keeping `/settings`
  compatible.
- Added doctor, fixture, docs, CSS/JS, and tests for Control Center rendering
  and sanitized extension sections.

## Runtime Boundary

PersonaConsole renders curated controls only. Consumer runtimes still own
authorization, persistence, validation, audit logging, restarts, secret storage,
and translation of staged values into their own config stores.

## Verification

```bash
PYTHONPATH=src python3 -m pytest tests
PYTHONPATH=src python3 scripts/consumer_integration_doctor.py --expected-version 1.0.47
```
