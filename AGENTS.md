# Working on R Stack

Canonical skills live in `plugins/rstack/skills/`. Keep each skill self-contained so installing one directory includes all its references, scripts, and assets.

Edit `plugins/rstack/plugin.json` for shared package identity, then run `uv run scripts/rstack.py sync`. Generated manifests and catalogs are committed. Provider-specific behavior belongs in a provider adapter, not in portable skill instructions.

Run `uv run scripts/rstack.py check` and `uv run python -m unittest discover -s tests` before handing off changes. Use `uv run scripts/rstack.py package` to build uploadable archives.

Do not add active MCP servers, hooks, or external-service dependencies merely to fill out the boilerplate. Add them when a workflow needs them, and update `docs/authoring.md` and validation together.
