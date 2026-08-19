# PersonaConsole 2.0.14

PersonaConsole 2.0.14 corrects the v2 hover-card cursor affordance.

## Changes

- Removed the broad `cursor: help` rule from `[data-pcv2-hover-source]`.
- Kept hover/focus card rendering and focus-visible styling intact.
- Ordinary rows, cards, and timeline items now retain their normal cursor
  behavior instead of showing a question-mark help cursor.

## Verification

- `PYTHONPATH=src python -m pytest tests/test_v2_console.py -q`
