# PersonaConsole 2.0.13

PersonaConsole 2.0.13 refines the v2 recent-exchange row visual language for
compact chat and DM timelines.

## Changes

- Added generic persona avatar/name fields to `V2RecentExchange`.
- Replaced visible `from`/`to` direction chips with an avatar flow: persona
  avatar, colored arrow, and contact avatar.
- Kept outbound arrows green and inbound arrows blue while preserving accessible
  direction labels.
- Rendered supplied platform SVGs as bare avatar-sized icons without a badge
  frame; platforms without icons still use the text badge fallback.

## Verification

- `PYTHONPATH=src python -m pytest tests/test_v2_console.py -q`
