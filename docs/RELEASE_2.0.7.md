# PersonaConsole 2.0.7

PersonaConsole 2.0.7 tightens the v2 panel/card layout so dense dashboard
cards with long labels and status badges do not force horizontal page overflow.

Changed:

- V2 repeated card, panel, feed, and media tiles now explicitly shrink inside
  grid tracks.
- V2 panel headers wrap their title/badge row instead of forcing a single-line
  layout in narrow cards.
- Panel titles use resilient word wrapping for long integration/add-on labels.
- Added regression coverage for narrow panel header wrapping.

Verification:

```bash
PYTHONPATH=src python -m pytest tests/test_v2_console.py tests/test_doctor.py tests/test_imports.py
```
