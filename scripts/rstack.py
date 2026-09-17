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
    entry = {"name": "rstack", "source": "./plugins/rstack", "description": config["description"]}
    catalog = {"name": "rstack", "owner": config["author"],
               "metadata": {"description": config["description"]}, "plugins": [entry]}
    return {
        "plugins/rstack/.codex-plugin/plugin.json": codex,
        "plugins/rstack/.claude-plugin/plugin.json": base,
        "plugins/rstack/.cursor-plugin/plugin.json": base,
        ".claude-plugin/marketplace.json": catalog,
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
        body = source.read_text()
        parts = body.split("---", 2)
        if len(parts) != 3 or parts[0].strip():
            raise ValueError(f"Missing frontmatter: {source}")
        metadata = yaml.safe_load(parts[1])
        if not isinstance(metadata, dict) or metadata.get("name") != skill.name:
            raise ValueError(f"Skill name must match its directory: {source}")
        description = metadata.get("description")
        if not isinstance(description, str) or not 1 <= len(description.strip()) <= 1024:
            raise ValueError(f"Invalid description: {source}")
        if not parts[2].strip() or "[TODO:" in body:
            raise ValueError(f"Unfinished skill: {source}")
        for markdown in skill.rglob("*.md"):
            for target in re.findall(r"\]\(([^\s)]+)\)", markdown.read_text()):
                if "://" in target or target.startswith("#"):
                    continue
                resolved = (markdown.parent / target.split("#")[0]).resolve()
                if not resolved.is_relative_to(skill.resolve()) or not resolved.exists():
                    raise ValueError(f"Broken or external skill resource in {markdown}: {target}")
    return skills


def write_zip(directory, destination):
    files = package_files(directory)
    with zipfile.ZipFile(destination, "w", compression=zipfile.ZIP_DEFLATED) as archive:
        for path in files:
            info = zipfile.ZipInfo(path.relative_to(directory.parent).as_posix(), (2020, 1, 1, 0, 0, 0))
            info.compress_type = zipfile.ZIP_DEFLATED
            info.create_system = 3
            info.external_attr = (0o100755 if path.stat().st_mode & 0o111 else 0o100644) << 16
            archive.writestr(info, path.read_bytes())


def package(root):
    skills = check(root)
    output = root / "dist"
    output.mkdir(exist_ok=True)
    version = read_json(root / "plugins/rstack/plugin.json")["version"]
    artifacts = [(root / "plugins/rstack", output / f"rstack-{version}.zip")]
    artifacts += [(skill, output / f"{skill.name}-{version}.zip") for skill in skills]
    for directory, destination in artifacts:
        write_zip(directory, destination)
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
