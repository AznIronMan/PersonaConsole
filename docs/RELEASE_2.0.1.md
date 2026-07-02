# PersonaConsole 2.0.1

PersonaConsole 2.0.1 tightens the v2 item renderer contracts for reusable
admin-directory and media-wall workflows.

Changed:

- Linked v2 table rows now preserve every configured column instead of
  collapsing into a single full-width link row.
- `V2TableRow` accepts generic row-level actions for consumer-supplied
  drill-down or edit affordances.
- `V2MediaItem` accepts generic tile-level actions while avoiding nested anchor
  markup when a media tile also has a preview link.
- Panels with a primary link and action links now avoid nested anchor markup.
- Added regression coverage for linked table row cells, row actions, media item
  actions, and panel actions.

Verification:

```bash
PYTHONPATH=src python -m pytest tests/test_v2_console.py
```
