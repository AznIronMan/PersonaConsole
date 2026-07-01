# PersonaConsole 1.0.52

## Summary

Keeps Control Center layouts within mobile viewport bounds when consumers show
long read-only or detail-preview payloads.

## Changes

- Added min/max width constraints to the Control Center surface, sections,
  groups, overview, and detail wrappers so grid children can shrink on mobile.
- Constrained read-only and detail preview blocks to their parent width while
  preserving internal scrolling for long JSON/code payloads.
- Added a regression assertion for the shared Control Center mobile overflow
  CSS.

## Verification

- `PYTHONPATH=src python3 -m pytest tests/test_control_center.py`
- `PYTHONPATH=src python3 -m pytest tests`
- CODAX browser smoke at desktop and mobile widths confirmed no horizontal
  overflow, no narrow control cards, and no label/input collisions.
