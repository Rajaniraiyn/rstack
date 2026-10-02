#!/usr/bin/env python3
"""Probe installed agent CLIs and write the factory config file.

Read-only by default: prints what it finds. Pass --write to save the
probed harnesses to the user config. Never authenticates, never stores
credentials; the user owns logins and subscriptions.
"""

from __future__ import annotations

import argparse
import json
import os
import platform
import shutil
import subprocess
import sys
from pathlib import Path


HARNESSES = {
    "claude": ["claude", "--version"],
    "codex": ["codex", "--version"],
    "opencode": ["opencode", "--version"],
    "amp": ["amp", "--version"],
    "copilot": ["copilot", "--version"],
    "gh": ["gh", "--version"],
    "sentry-cli": ["sentry-cli", "--version"],
    "acli": ["acli", "--version"],
    "jira": ["jira", "--version"],
}

CONFIG_DIR = (
    Path(os.environ.get("XDG_CONFIG_HOME", Path.home() / ".config"))
    if not os.name == "nt"
    else Path(os.environ.get("APPDATA", Path.home()))
)
CONFIG_FILE = CONFIG_DIR / "rstack" / "factory.json"


def probe(name: str, command: list[str]) -> dict:
    path = shutil.which(command[0])
    if not path:
        return {"installed": False, "path": None, "version": None}
    version = None
    try:
        result = subprocess.run(
            command, capture_output=True, text=True, timeout=15
        )
        if result.returncode == 0:
            version = result.stdout.strip().splitlines()[:1]
            version = version[0][:120] if version else "(no version line)"
    except (OSError, subprocess.TimeoutExpired):
        version = "(could not probe)"
    return {"installed": True, "path": path, "version": version}


def save_report(path: Path, report: dict) -> None:
    """Refresh detection without discarding saved routes or user settings."""
    config = json.loads(path.read_text()) if path.exists() else {}
    if not isinstance(config, dict) or not isinstance(config.get("harnesses", {}), dict):
        raise ValueError("factory config must be an object with a harnesses object")
    harnesses = config.setdefault("harnesses", {})
    for name, detected in report.items():
        existing = harnesses.get(name, {})
        if not isinstance(existing, dict):
            raise ValueError(f"factory harness {name} must be an object")
        harnesses[name] = {**existing, **detected}
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(json.dumps(config, indent=2) + "\n")


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument(
        "--write",
        action="store_true",
        help="write the probed harnesses to the config file",
    )
    args = parser.parse_args()

    report = {name: probe(name, cmd) for name, cmd in HARNESSES.items()}
    installed = [n for n, r in report.items() if r["installed"]]
    missing = [n for n, r in report.items() if not r["installed"]]

    print(f"platform: {platform.system()} {platform.machine()}")
    print(f"installed: {', '.join(installed) or 'none'}")
    print(f"missing:   {', '.join(missing) or 'none'}")
    for name, result in report.items():
        if result["installed"]:
            print(f"  {name}: {result['version']}  ({result['path']})")

    print("\nfactory config: " + str(CONFIG_FILE))
    if args.write:
        try:
            save_report(CONFIG_FILE, report)
        except (OSError, ValueError) as exc:
            print(f"could not update factory config: {exc}", file=sys.stderr)
            return 1
        print("written.")
    else:
        print("not written; pass --write to save.")

    print("\nAuth stays with you. This script never logs in or stores credentials.")
    return 0


if __name__ == "__main__":
    sys.exit(main())
