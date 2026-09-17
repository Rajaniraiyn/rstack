# Portability checklist

- Keep `name` and `description` in standard YAML frontmatter. Do not rely on a provider-specific field for essential behavior.
- Express workflows in terms of capabilities, such as searching files or running a command. Exact tool names belong in host-specific instructions when required.
- Resolve bundled resources relative to the skill directory. Avoid absolute machine paths and links to files outside the installed skill.
- Document required runtimes and tools. A web-hosted skill may lack a terminal, local checkout, network access, or a particular MCP connection.
- Put optional Codex display metadata in `agents/openai.yaml`. Other clients can use the skill without that metadata.
- Do not embed credentials. A skill can describe a required connection but cannot provision that connection merely by being installed.
- Keep hooks, provider rules, and plugin manifests outside the skill unless they are reference material. Installing a skill alone does not install these components.
