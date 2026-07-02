# PersonaConsole 2.0.2

PersonaConsole 2.0.2 adds safe structured cells for v2 tables so consumer
runtimes can make directory rows feel like profile surfaces without injecting
raw HTML into the shared renderer.

Changed:

- V2 table cell values may now be mapping payloads rendered as generic identity
  cells, status cells, or badge/chip groups.
- Structured cells remain escaped by the renderer and can use row links without
  collapsing configured columns.
- Added v2 CSS for avatar initials/images, profile copy, badge groups, and
  color-coded status dots.
- Added regression coverage for structured table cells, escaping, row links,
  and actions.

Verification:

```bash
PYTHONPATH=src python -m pytest tests/test_v2_console.py
```
