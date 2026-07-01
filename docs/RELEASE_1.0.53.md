# PersonaConsole 1.0.53

## Summary

Adds a public-safe platform identity block-state surface for consumer runtimes
that need to show runtime/internal suppression separately from provider-side
block job posture.

## Changes

- Added `PLATFORM_IDENTITY_BLOCKS_FEATURE`, `PlatformIdentityBlockRow`,
  `PlatformIdentityBlocksSurfaceConfig`,
  `platform_identity_blocks_feature_enabled(...)`, and
  `render_platform_identity_blocks_surface(...)`.
- Rendered dense responsive rows with internal block state and platform block
  status shown separately, plus metrics, filters, status tabs, live refresh,
  sorting labels, badges, and runtime-owned actions.
- Added owner-private redaction hooks for private identity labels, reasons,
  summaries, and hrefs.
- Added compatibility submodules for `persona_console.platform_identity_blocks`
  and `personacore.platform_identity_blocks`.
- Updated the public fixture, consumer doctor, CSS, import tests, and
  configuration docs.

## Verification

- `PYTHONPATH=src python3 -m pytest tests`
- Fixture registry assertion for platform identity blocks
- Browser audit through `127.0.0.1` at desktop `1280px` and mobile `390px`
  confirmed no horizontal overflow, no narrow state cells, no raw private
  fixture text, and no surface-registry unknown-feature warning.
