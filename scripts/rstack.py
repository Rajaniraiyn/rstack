#!/usr/bin/env python3
"""Generate client metadata, check portable skills, and build upload archives."""

import argparse
import json
from pathlib import Path
import re
import zipfile

import yaml

ROOT = Path(__file__).resolve().parents[1]
NAME = re.compile(r"[a-z0-9]+(?:-[a-z0-9]+)*")


def read_json(path):
    return json.loads(path.read_text())


def manifests(root):
    config = read_json(root / "plugins/rstack/plugin.json")
    if config["name"] != "rstack":
        raise ValueError("Package name must remain rstack; repository name is configurable")
    if not re.fullmatch(r"\d+\.\d+\.\d+", config["version"]):
        raise ValueError("Use a version such as 0.1.0")
    base = {key: config[key] for key in ("name", "version", "description", "author")}
    if config.get("repository"):
        if not config["repository"].startswith("https://"):
            raise ValueError("repository must be an HTTPS URL or null")
        base["repository"] = config["repository"]
    codex = {**base, "skills": "./skills/", "interface": {
        "displayName": "R Stack",
        "shortDescription": config["description"],
        "longDescription": config["description"],
        "developerName": config["author"]["name"], "category": "Productivity",
        "capabilities": [], "defaultPrompt": ["Help me author a portable skill."]}}
    skill_paths = [f"./skills/{path.name}" for path in sorted((root / "plugins/rstack/skills").iterdir())
                   if path.is_dir()]
    entry = {"name": "rstack", "source": "./plugins/rstack", "description": config["description"]}
    claude_entry = {**entry, "skills": skill_paths}
    catalog = {"name": "rstack", "owner": config["author"],
               "metadata": {"description": config["description"]}, "plugins": [entry]}
    claude_catalog = {**catalog, "plugins": [claude_entry]}
    return {
        "plugins/rstack/.codex-plugin/plugin.json": codex,
        "plugins/rstack/.claude-plugin/plugin.json": base,
        "plugins/rstack/.cursor-plugin/plugin.json": base,
        ".claude-plugin/marketplace.json": claude_catalog,
        ".cursor-plugin/marketplace.json": catalog,
        ".agents/plugins/marketplace.json": {
            "name": "rstack", "interface": {"displayName": "R Stack"},
            "plugins": [{"name": "rstack", "source": {"source": "local", "path": "./plugins/rstack"},
                         "policy": {"installation": "AVAILABLE", "authentication": "ON_INSTALL"},
                         "category": "Productivity"}]},
    }


def sync(root):
    for relative, value in manifests(root).items():
        path = root / relative
        path.parent.mkdir(parents=True, exist_ok=True)
        path.write_text(json.dumps(value, indent=2) + "\n")


def skill_dirs(root):
    return sorted((root / "plugins/rstack/skills").iterdir())


def package_files(directory):
    """Keep archives self-contained and free of accidental local state."""
    result = []
    for path in sorted(directory.rglob("*")):
        if path.is_symlink():
            raise ValueError(f"Package must not contain symlinks: {path}")
        if any(part in {"__pycache__", ".DS_Store", ".git", ".venv", "node_modules"}
               or part == ".env" or part.startswith(".env.") for part in path.relative_to(directory).parts):
            raise ValueError(f"Remove local state from package: {path}")
        if path.is_file():
            result.append(path)
    return result


def frontmatter(source):
    lines = source.read_text().splitlines()
    if not lines or lines[0] != "---":
        raise ValueError(f"Missing frontmatter: {source}")
    try:
        end = lines.index("---", 1)
    except ValueError:
        raise ValueError(f"Unclosed frontmatter: {source}") from None
    class UniqueKeyLoader(yaml.SafeLoader):
        pass

    def unique_mapping(loader, node, deep=False):
        mapping = {}
        for key_node, value_node in node.value:
            key = loader.construct_object(key_node, deep=deep)
            if key in mapping:
                raise ValueError(f"Duplicate frontmatter key {key!r}: {source}")
            mapping[key] = loader.construct_object(value_node, deep=deep)
        return mapping

    UniqueKeyLoader.add_constructor(yaml.resolver.BaseResolver.DEFAULT_MAPPING_TAG, unique_mapping)
    metadata = yaml.load("\n".join(lines[1:end]), Loader=UniqueKeyLoader)
    return metadata, "\n".join(lines[end + 1:])


def check(root):
    for relative, expected in manifests(root).items():
        path = root / relative
        if not path.is_file() or read_json(path) != expected:
            raise ValueError(f"Metadata differs: {relative}; run scripts/rstack.py sync")
    plugin = root / "plugins/rstack"
    package_files(plugin)
    skills = skill_dirs(root)
    if not skills:
        raise ValueError("At least one skill is required")
    for skill in skills:
        if not skill.is_dir() or not NAME.fullmatch(skill.name) or len(skill.name) > 64:
            raise ValueError(f"Invalid skill directory: {skill}")
        source = skill / "SKILL.md"
        metadata, body = frontmatter(source)
        if not isinstance(metadata, dict) or metadata.get("name") != skill.name:
            raise ValueError(f"Skill name must match its directory: {source}")
        supported = {"name", "description", "license", "compatibility", "metadata", "allowed-tools"}
        extra = set(metadata) - supported
        if extra:
            raise ValueError(f"Non-portable frontmatter field(s) in {source}: {', '.join(sorted(extra))}")
        description = metadata.get("description")
        if not isinstance(description, str) or not 1 <= len(description.strip()) <= 1024:
            raise ValueError(f"Invalid description: {source}")
        compatibility = metadata.get("compatibility")
        if compatibility is not None and (not isinstance(compatibility, str) or not 1 <= len(compatibility) <= 500):
            raise ValueError(f"Invalid compatibility: {source}")
        fields = ("license", "allowed-tools")
        if any(key in metadata and not isinstance(metadata[key], str) for key in fields):
            raise ValueError(f"Invalid optional frontmatter field type: {source}")
        extra_metadata = metadata.get("metadata", {})
        if not isinstance(extra_metadata, dict) or any(not isinstance(key, str) or not isinstance(value, str)
                                                       for key, value in extra_metadata.items()):
            raise ValueError(f"metadata must map strings to strings: {source}")
        if not body.strip() or "[TODO:" in body:
            raise ValueError(f"Unfinished skill: {source}")
        openai = skill / "agents/openai.yaml"
        if openai.exists():
            ui = yaml.safe_load(openai.read_text())
            if not isinstance(ui, dict):
                raise ValueError(f"Invalid Codex skill metadata: {openai}")
            interface = ui.get("interface", {})
            if not isinstance(interface, dict):
                raise ValueError(f"Invalid Codex interface metadata: {openai}")
            for key in ("display_name", "short_description", "default_prompt"):
                if key in interface and not isinstance(interface[key], str):
                    raise ValueError(f"Invalid Codex interface field {key}: {openai}")
            policy = ui.get("policy", {})
            if not isinstance(policy, dict) or ("allow_implicit_invocation" in policy
                                                 and not isinstance(policy["allow_implicit_invocation"], bool)):
                raise ValueError(f"Invalid Codex invocation policy: {openai}")
        for markdown in skill.rglob("*.md"):
            for target in re.findall(r"\]\(([^\s)]+)\)", markdown.read_text()):
                if "://" in target or target.startswith("#"):
                    continue
                resolved = (markdown.parent / target.split("#")[0]).resolve()
                if not resolved.is_relative_to(skill.resolve()) or not resolved.exists():
                    raise ValueError(f"Broken or external skill resource in {markdown}: {target}")
    listing = root / "skills.sh.json"
    if listing.exists():
        config = read_json(listing)
        groups = config.get("groupings") if isinstance(config, dict) else None
        if not isinstance(groups, list) or not groups:
            raise ValueError("skills.sh.json must contain at least one grouping")
        if config.get("notGrouped", "bottom") not in {"top", "bottom"}:
            raise ValueError("skills.sh.json notGrouped must be 'top' or 'bottom'")
        names = {skill.name for skill in skills}
        grouped = set()
        for group in groups:
            if not isinstance(group, dict) or not isinstance(group.get("title"), str) or not group["title"].strip():
                raise ValueError("Each skills.sh grouping needs a title")
            members = group.get("skills")
            if not isinstance(members, list) or not members:
                raise ValueError(f"Grouping {group['title']!r} must contain skills")
            for name in members:
                if not isinstance(name, str):
                    raise ValueError(f"Invalid skill name in grouping {group['title']!r}")
                if name not in names:
                    raise ValueError(f"Unknown skill in skills.sh.json: {name}")
                if name in grouped:
                    raise ValueError(f"Skill appears in multiple skills.sh groups: {name}")
                grouped.add(name)
    return skills


def write_zip(directory, destination, license_file=None):
    files = package_files(directory)
    with zipfile.ZipFile(destination, "w", compression=zipfile.ZIP_DEFLATED) as archive:
        for path in files:
            info = zipfile.ZipInfo(path.relative_to(directory.parent).as_posix(), (2020, 1, 1, 0, 0, 0))
            info.compress_type = zipfile.ZIP_DEFLATED
            info.create_system = 3
            info.external_attr = (0o100755 if path.stat().st_mode & 0o111 else 0o100644) << 16
            archive.writestr(info, path.read_bytes())
        if license_file is not None:
            info = zipfile.ZipInfo("LICENSE", (2020, 1, 1, 0, 0, 0))
            info.compress_type = zipfile.ZIP_DEFLATED
            info.create_system = 3
            info.external_attr = 0o100644 << 16
            archive.writestr(info, license_file.read_bytes())


def package(root):
    skills = check(root)
    output = root / "dist"
    output.mkdir(exist_ok=True)
    version = read_json(root / "plugins/rstack/plugin.json")["version"]
    license_file = root / "LICENSE"
    artifacts = [(root / "plugins/rstack", output / f"rstack-{version}.zip")]
    artifacts += [(skill, output / f"{skill.name}-{version}.zip") for skill in skills]
    for directory, destination in artifacts:
        write_zip(directory, destination, license_file)
    return [destination for _, destination in artifacts]


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("command", choices=["sync", "check", "package"])
    args = parser.parse_args()
    try:
        if args.command == "sync":
            sync(ROOT)
            print("Updated plugin manifests and catalogs")
        elif args.command == "check":
            print(f"Validated metadata and {len(check(ROOT))} skill(s)")
        else:
            for path in package(ROOT):
                print(path.relative_to(ROOT))
    except (ValueError, OSError, KeyError, yaml.YAMLError) as error:
        parser.exit(1, f"Error: {error}\n")


if __name__ == "__main__":
    main()
