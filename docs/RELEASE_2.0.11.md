# PersonaConsole 2.0.11

PersonaConsole 2.0.11 adds a generic v2 recent-exchange row layout for Today
and other compact message timelines. Consumer runtimes can now render one row
per chat/DM exchange with an avatar, platform badge, message preview, relative
age, and absolute timestamp while keeping platform routes and data reads local.

## Changes

- Added `V2RecentExchange` and `V2Section.exchanges`.
- Rendered compact exchange rows with avatar/initials, platform image badges,
  relative age, timestamp, and optional row links.
- Kept full message text available through shared hover/focus cards while the
  visible message cell stays capped to three lines.
- Updated the public v2 fixture to show DMs through the new exchange layout.

## Verification

- `PYTHONPATH=src python -m pytest tests/test_v2_console.py -q`
