# PersonaConsole 2.0.9

PersonaConsole 2.0.9 adds generic image-backed icon support for v2 badges and
feed items. Consumer runtimes can now pass their own static SVG or image URLs
for provider, social, channel, or account glyphs without placing those private
assets in the public PersonaConsole package.

## Changes

- Added optional `icon_src` fields to `V2Badge` and `V2FeedItem`.
- Rendered image icons with escaped URLs, empty alt text, lazy loading, and
  bounded CSS sizing.
- Preserved existing text-only badge and feed icon behavior for consumers that
  do not pass image URLs.

## Verification

- `PYTHONPATH=src python -m pytest tests/test_v2_console.py -q`
