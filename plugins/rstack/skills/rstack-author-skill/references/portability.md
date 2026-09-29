# Portability checklist

- Keep `name` and `description` in standard YAML frontmatter. Do not rely on a provider-specific field for essential behavior.
- Write `description` for the agent, not the user: what the skill does, then the exact requests or trigger phrases that should load it. Name, description, and path are all the agent sees before loading the SKILL.md.
- Keep the split between short and long description in the body, not frontmatter: `description` is the only routing signal and the only thing loaded at startup; the longer, verbose description belongs at the top of the body, read only after activation. There is no standard long-description field, so do not invent one under `metadata`.
- The [Agent Skills specification](https://agentskills.io/specification) defines `name` and `description`, plus optional `license`, `compatibility`, `metadata`, and experimental `allowed-tools`. `metadata` is a string-to-string map; it does not define a standard trigger field.
- Keep host-specific controls such as `disable-model-invocation`, `user-invocable`, `argument-hint`, icons, and display descriptions out of portable frontmatter. Put them in that host's adapter, and do not assume one host's setting controls another host.
- An authors-only skill should say who it is for in its description and body. Set explicit invocation policy in host adapters where the target supports it, and describe hosts where the skill remains auto-discoverable.
- Express workflows in terms of capabilities, such as searching files or running a command. Exact tool names belong in host-specific instructions when required.
- Prefer stdlib-only Python or plain markdown for executable helpers over shell scripts, so the skill runs on Windows without bash. Shell listed inside a reference is an example, not a required path.
- Resolve bundled resources relative to the skill directory. Avoid absolute machine paths and links to files outside the installed skill.
- Document required runtimes and tools. A web-hosted skill may lack a terminal, local checkout, network access, or a particular MCP connection.
- Put Codex display metadata or `policy.allow_implicit_invocation` in `agents/openai.yaml` only when the skill needs them. This file affects Codex only and does not define a subagent. The portable description still handles skill routing on other clients.
- Include the applicable license notice in standalone archives. A `license` frontmatter value does not replace the notice itself.
- Do not embed credentials. A skill can describe a required connection but cannot provision that connection merely by being installed.
- Keep hooks, provider rules, and plugin manifests outside the skill unless they are reference material. Installing a skill alone does not install these components.
