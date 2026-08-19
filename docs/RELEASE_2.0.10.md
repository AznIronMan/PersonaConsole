# PersonaConsole 2.0.10

PersonaConsole 2.0.10 extends the v2 image icon support from badges and feed
items to dashboard metric cards. Consumer runtimes can now pass their own
static SVG or image URLs for prominent card icons without placing private media
inside the public PersonaConsole package.

## Changes

- Added optional `icon_src` support to `V2MetricCard`.
- Rendered card image icons with escaped URLs, empty alt text, lazy loading, and
  bounded CSS sizing.
- Preserved existing text-only `icon` behavior for consumers that do not pass
  image URLs.

## Verification

- `PYTHONPATH=src python -m pytest tests/test_v2_console.py -q`
