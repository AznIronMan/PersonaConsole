# PersonaConsole 2.0.0

PersonaConsole 2.0.0 introduces the opt-in v2 console foundation while
preserving the existing v1 API and legacy compatibility shims.

## Added

- `personaconsole.v2` models and renderers.
- v2 shell with hero media, top navigation, operator context, status badges,
  section layouts, owner-lock rendering, and packaged CSS/JS.
- Public-safe v2 fixture renderer.
- Generic packaged SVG placeholders for missing hero, media, provider,
  document, and audio assets.

## Compatibility

- Existing `personaconsole`, `persona_console`, and `personacore` v1 imports
  remain intact.
- FastAPI remains an optional dependency for static mounting only.
- Consumer runtimes opt into v2 explicitly.
