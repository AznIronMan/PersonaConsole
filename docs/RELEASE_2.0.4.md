# PersonaConsole 2.0.4

PersonaConsole 2.0.4 makes v2 action links with non-GET methods operational in
the shared browser script. Consumer runtimes can now render compact POST action
buttons for profile controls, runtime controls, or review actions without
shipping persona-specific JavaScript.

Changed:

- Added shared v2 handling for `a[data-method]` action links.
- Non-GET actions submit through a generated form and preserve the action URL,
  including query parameters.
- Disabled actions do not submit.
- Optional `data-confirm` prompts are honored when a consumer adds them.
- Added regression coverage for the v2 POST action renderer/script contract.

Verification:

```bash
PYTHONPATH=src python -m pytest tests/test_v2_console.py tests/test_doctor.py tests/test_imports.py
```
