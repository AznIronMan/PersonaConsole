# PersonaConsole 2.0.12

PersonaConsole 2.0.12 tightens the v2 recent-exchange row renderer for compact
DM/chat timelines.

## Changes

- Render platform badges as icon-only chips when a platform SVG is supplied,
  with the platform label preserved as tooltip and accessible text.
- Preserve text platform badges as the fallback when no platform icon exists.
- Added `V2RecentExchange.direction` so exchange rows can indicate whether a
  message is inbound from a contact or outbound to that contact.

## Verification

- `PYTHONPATH=src python -m pytest tests/test_v2_console.py -q`
