# Portability checklist

- Keep `name` and `description` in standard YAML frontmatter. When a requested behavior needs a host extension, use the documented setting for each target and state any host where it cannot be enforced.
- Write `description` for the agent: what the skill does and when to use it. Hosts using progressive disclosure use this text to decide whether to load the full skill.
- The core specification defines one `description`, not a short/long pair. Host-specific filters such as Cursor `paths` or Claude Code `when_to_use` may change routing; use them only when needed and document their host scope.
- The [Agent Skills specification](https://agentskills.io/specification) defines `name` and `description`, plus optional `license`, `compatibility`, `metadata`, and experimental `allowed-tools`. `metadata` is a string-to-string map; it does not define a standard trigger field.
- Distinguish core fields from documented provider extensions. Claude Code and Cursor both recognize `disable-model-invocation`; it prevents automatic selection while preserving explicit invocation in their standard skill flows. Strict Agent Skills upload APIs may reject this extension.
- OpenCode v2 recognizes `metadata.opencode/autoinvoke: "false"`. Quote the value so it remains a string in standard metadata. Other OpenCode versions may ignore it.
- An authors-only skill should say who it is for in its description and body. Set invocation policy in each target host's documented format, and state where an extension may be ignored.
- Express workflows in terms of capabilities, such as searching files or running a command. Exact tool names belong in host-specific instructions when required.
- Prefer stdlib-only Python or plain markdown for executable helpers over shell scripts, so the skill runs on Windows without bash. Shell listed inside a reference is an example, not a required path.
- Resolve bundled resources relative to the skill directory. Avoid absolute machine paths and links to files outside the installed skill.
- Document required runtimes and tools. A web-hosted skill may lack a terminal, local checkout, network access, or a particular MCP connection.
- Put Codex display metadata or `policy.allow_implicit_invocation` in `agents/openai.yaml` only when the skill needs them. This file affects Codex only and does not define a subagent. The portable description still handles routing on other clients.
- Include the applicable license notice in standalone archives. A `license` frontmatter value does not replace the notice itself.
- Do not embed credentials. A skill can describe a required connection but cannot provision that connection merely by being installed.
- Keep hooks, provider rules, and plugin manifests outside the skill unless they are reference material. Installing a skill alone does not install these components.
