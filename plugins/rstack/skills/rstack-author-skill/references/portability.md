# Portability checklist

- Keep `name` and `description` in standard YAML frontmatter. Do not rely on a provider-specific field for essential behavior.
- Write `description` for the agent, not the user: what the skill does, then the exact requests or trigger phrases that should load it. Name, description, and path are all the agent sees before loading the SKILL.md.
- Keep the split between short and long description in the body, not frontmatter: `description` is the only routing signal and the only thing loaded at startup; the longer, verbose description belongs at the top of the body, read only after activation. There is no standard long-description field, so do not invent one under `metadata`.
- Portable frontmatter includes `license` and `metadata.trigger` from the [Agent Skills specification](https://agentskills.io/specification). Docstring-style host knobs like `disable-model-invocation`, `user-invocable`, `argument-hint`, `icon`, or `color` are per-client; they may enhance a skill but essential behavior must not depend on them.
- A skill meant only for this repository's authors (not run for consumers) sets `disable-model-invocation: true` and omits `metadata.trigger` so nothing auto-invokes it from a phrase.
- Express workflows in terms of capabilities, such as searching files or running a command. Exact tool names belong in host-specific instructions when required.
- Prefer stdlib-only Python or plain markdown for executable helpers over shell scripts, so the skill runs on Windows without bash. Shell listed inside a reference is an example, not a required path.
- Resolve bundled resources relative to the skill directory. Avoid absolute machine paths and links to files outside the installed skill.
- Document required runtimes and tools. A web-hosted skill may lack a terminal, local checkout, network access, or a particular MCP connection.
- Put optional Codex display metadata in `agents/openai.yaml`. Other clients can use the skill without that metadata.
- Do not embed credentials. A skill can describe a required connection but cannot provision that connection merely by being installed.
- Keep hooks, provider rules, and plugin manifests outside the skill unless they are reference material. Installing a skill alone does not install these components.
