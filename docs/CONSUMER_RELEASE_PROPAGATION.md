# Consumer Release Propagation

PersonaConsole releases can affect multiple consumer runtimes. Keep the public
package generic, then propagate each approved update through the consumer repos
that opted into that release.

## Public/Private Boundary

Tracked PersonaConsole files may describe the workflow and generic roster
schema. They must not contain private consumer names, hosts, local paths,
restart commands, smoke URLs, screenshots, credentials, or deployment notes.

Keep the real roster in `.private/consumer-release-roster.json` or in each
consumer repo's own private runbook. `.private/` is ignored.

## Release Checklist

For each consumer:

1. Read that consumer repo's `AGENTS.md`.
2. Open or continue the consumer-owned task before code, deploy, or runtime
   state changes.
3. Update the PersonaConsole package version, source checkout, or approved
   local source mount.
4. Refresh vendored static assets if that runtime serves copied assets.
5. Run PersonaConsole package tests for the shared checkout when the release
   changes shared renderers.
6. Run the consumer's focused admin/render tests.
7. Run `scripts/consumer_integration_doctor.py --expected-version <version>`
   where the consumer can import the updated package.
8. Smoke admin login plus representative migrated routes.
9. Restart or rebuild only the services that import PersonaConsole.
10. Record verification, restart result, rollback posture, and watch items in
    the consumer task system.

## Control Center Rollout Checklist

When a release adds or updates the shared Control Center, each consumer runtime
should explicitly decide what is runtime-owned before exposing editable
controls. The shared renderer is presentation-only; the runtime owns auth,
allowlists, validation, persistence, audit, restarts, and rollback.

For each Control Center consumer:

1. Keep `/settings` compatible as an alias or documented legacy route while
   adding the first-class Control nav section.
2. Focus section routes so `/control/runtime`, `/control/integrations`,
   `/control/appearance`, `/control/features`, and `/control/audit` render the
   relevant section rather than the whole catalog.
3. Define a role matrix before save routes are enabled. A typical rollout is:
   owner can view and edit all supported controls, operator can view most and
   edit only allowlisted runtime-owned controls, moderator is read-only.
4. Mark unsupported Console or Engine catalog controls as staged previews,
   readonly, disabled, or view-only until the runtime owns a save handler for
   them.
5. Use stable source paths for editable controls, such as
   `runtime.feature.example`, `engine.projection.cadence_settings.base_delay_ms`,
   or `runtime.provider.default_model`.
6. Persist only allowlisted fields through runtime-owned storage. Do not let a
   generic form payload write arbitrary settings.
7. Validate booleans, enums, numbers, thresholds, and restart-required fields in
   the runtime save route, not only in browser controls.
8. Render secrets as configured/not-configured posture. New values may be typed
   to overwrite, and clear actions should be explicit and auditable.
9. Record operator audit rows for applied settings and secret actions without
   storing raw secret values in rendered pages, task files, logs, or docs.
10. Show clear messages for runtime-owned saves, staged previews, role-limited
    fields, restart/reload posture, and unsupported submissions.
11. Browser-smoke desktop and mobile Control pages for text overlap, horizontal
    overflow, one-character columns, and usable card widths.
12. Exercise one harmless non-secret save and revert through the runtime save
    path. Verify the projected/runtime value changes, audit records exist, and
    the prior value or absent override is restored.
13. Run focused Control Center tests, the consumer admin/render tests, the
    PersonaConsole doctor with the expected version, and a live login/auth
    smoke where applicable.
14. Restart or rebuild only the services that import the updated runtime code or
    PersonaConsole package.

## Local Roster

Create an ignored local roster:

```bash
python3 scripts/consumer_release_plan.py --print-template > .private/consumer-release-roster.json
```

Edit that private file for real consumers. Keep any private details out of
tracked docs and commits.

Generate a checklist to stdout:

```bash
python3 scripts/consumer_release_plan.py \
  --roster .private/consumer-release-roster.json \
  --version 1.0.41 \
  --source "public tag v1.0.41"
```

Write a generated plan only under `.private/`:

```bash
python3 scripts/consumer_release_plan.py \
  --roster .private/consumer-release-roster.json \
  --version 1.0.41 \
  --output .private/release-plans/personaconsole-1.0.41.md
```

The helper refuses output paths outside `.private/` so private runtime names are
not accidentally written into tracked files.

## Roster Fields

- `key`: stable local identifier.
- `label`: display label for the generated private checklist.
- `repo_path`: private consumer repo/root path.
- `task_system`: reminder for the consumer's task tracker.
- `persona_console_source`: how this consumer receives PersonaConsole.
- `update_steps`: package/source/static update actions.
- `tests`: required focused tests or doctor checks.
- `smokes`: browser, route, or render smokes.
- `control_center`: optional Control Center-specific rollout checks.
- `restart_steps`: restart, rebuild, or container rollout actions.
- `rollback`: exact rollback posture for that consumer.
- `notes`: private reminders or watch items.
