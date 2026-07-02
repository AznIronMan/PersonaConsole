# PersonaConsole v2 Architecture

PersonaConsole v2 is an opt-in console foundation layered beside the existing
v1 modules. Existing import paths, compatibility shims, renderers, CSS, and
tests remain supported. Consumers adopt v2 by importing `personaconsole.v2` and
rendering `V2ConsoleConfig` instances.

## Shape

- `personaconsole.v2.models` owns sanitized dataclasses for theme tokens, hero
  media, top-level navigation, operator/privacy context, cards, feeds, tables,
  media tiles, conversations, panels, and sections.
- `personaconsole.v2.render` owns the generic HTML renderer and privacy-aware
  owner-lock text rendering.
- `personaconsole.v2.fixture` provides a public-safe fixture app/page.
- `static/persona-console-v2.css` and `static/persona-console-v2.js` are packaged
  with the existing static mount.

The v2 implementation intentionally does not move or rename current modules.
The package can release as `2.0.0` while preserving `personaconsole`,
`persona_console`, and `personacore` compatibility imports.

## Consumer Boundary

PersonaConsole owns:

- Generic shell, hero, nav, section layouts, visual tokens, fixture rendering,
  privacy render states, owner-lock affordances, and static placeholders.
- Generic extension/add-on placement through section/panel/action models.
- Public docs and tests that use generic personas, operators, and runtime data.

Consumer runtimes own:

- Authentication, session policy, private routes, real database queries, secrets,
  runtime actions, persona-specific copy, persona-specific assets, deployment,
  and any actual LLM-mediated edit execution.

## Privacy Model

v2 render models support owner-only values through `V2PrivateValue`. Non-owner
views receive a safe alternate when supplied, otherwise the value is withheld or
hidden. Owner-lock metadata is rendered as a UI affordance only; consumers still
must enforce authorization on routes, APIs, files, and mutations.

## Initial Sections

The shared section keys are:

- `today`
- `conversations`
- `people`
- `mind`
- `journal`
- `memory`
- `media`
- `persona`
- `integrations`
- `control`

Each section can choose layouts such as `dashboard`, `people`, `conversation`,
`feed`, `media`, `journal`, `persona`, `integrations`, or `control`.
