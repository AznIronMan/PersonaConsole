# PersonaConsole 2.0.3

PersonaConsole 2.0.3 adds safe floating hover cards for v2 structured table
cells so shared directory surfaces can show profile previews and relationship
breakdowns without persona-specific renderer forks.

Changed:

- Structured v2 table cells can provide `popover`/`hover` payloads rendered as
  escaped hidden templates.
- The v2 browser script floats hover cards beside the cursor or focused cell,
  avoiding clipping inside horizontally scrollable tables.
- Added keyboard focus and Escape handling for hover-card sources.
- Added CSS for profile preview cards, metrics, and label/value rows.
- Added regression coverage for escaped hover-card content and required JS/CSS
  assets.

Verification:

```bash
PYTHONPATH=src python -m pytest tests/test_v2_console.py
```
