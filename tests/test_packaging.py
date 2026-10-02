import importlib.util
import json
from pathlib import Path
import shutil
import tempfile
import unittest
import zipfile

import yaml

ROOT = Path(__file__).resolve().parents[1]
spec = importlib.util.spec_from_file_location("rstack", ROOT / "scripts/rstack.py")
rstack = importlib.util.module_from_spec(spec)
spec.loader.exec_module(rstack)


class PackagingTests(unittest.TestCase):
    def setUp(self):
        self.temp = tempfile.TemporaryDirectory()
        self.addCleanup(self.temp.cleanup)
        self.root = Path(self.temp.name)
        shutil.copytree(ROOT / "plugins", self.root / "plugins")
        shutil.copy(ROOT / "LICENSE", self.root / "LICENSE")
        rstack.sync(self.root)

    def test_skill_export_is_complete_and_reproducible(self):
        paths = rstack.package(self.root)
        first = {path.name: path.read_bytes() for path in paths}
        self.assertEqual(first, {path.name: path.read_bytes() for path in rstack.package(self.root)})
        for skill in sorted((self.root / "plugins/rstack/skills").iterdir()):
            if not skill.is_dir():
                continue
            with self.subTest(skill=skill.name):
                archive_path = next(path for path in paths if path.name == f"{skill.name}-0.1.0.zip")
                with zipfile.ZipFile(archive_path) as archive:
                    self.assertEqual(archive.read("LICENSE"), (self.root / "LICENSE").read_bytes())
                    for source in skill.rglob("*"):
                        if source.is_file():
                            self.assertEqual(archive.read(source.relative_to(skill.parent).as_posix()), source.read_bytes())
                    self.assertIn(f"{skill.name}/SKILL.md", archive.namelist())

    def test_manifest_drift_fails(self):
        (self.root / "plugins/rstack/.claude-plugin/plugin.json").write_text('{}')
        with self.assertRaisesRegex(ValueError, "Metadata differs"):
            rstack.check(self.root)

    def test_portable_manifest_drives_generated_metadata(self):
        source = self.root / "plugins/rstack/plugin.json"
        metadata = json.loads(source.read_text())
        metadata["version"] = "0.2.0"
        source.write_text(json.dumps(metadata))
        with self.assertRaisesRegex(ValueError, "Metadata differs"):
            rstack.check(self.root)
        rstack.sync(self.root)
        self.assertEqual(json.loads(source.read_text()), metadata)
        artifacts = rstack.package(self.root)
        self.assertEqual(artifacts[0].name, "rstack-0.2.0.zip")
        for client in ("claude", "codex", "cursor"):
            manifest = self.root / f"plugins/rstack/.{client}-plugin/plugin.json"
            self.assertEqual(json.loads(manifest.read_text())["version"], "0.2.0")

    def test_marketplace_declares_every_skill_path(self):
        marketplace = json.loads((self.root / ".claude-plugin/marketplace.json").read_text())
        declared = marketplace["plugins"][0]["skills"]
        self.assertEqual(declared, [f"./skills/{path.name}" for path in sorted(
            (self.root / "plugins/rstack/skills").iterdir()) if path.is_dir()])

    def test_missing_bundled_reference_fails(self):
        (self.root / "plugins/rstack/skills/rstack-author-skill/references/portability.md").unlink()
        with self.assertRaisesRegex(ValueError, "Broken or external"):
            rstack.check(self.root)

    def test_symlink_escape_fails_before_archiving(self):
        (self.root / "plugins/rstack/external").symlink_to(self.root / "plugins/rstack/plugin.json")
        with self.assertRaisesRegex(ValueError, "symlinks"):
            rstack.package(self.root)
        self.assertFalse((self.root / "dist").exists())

    def test_environment_file_is_not_packaged(self):
        (self.root / "plugins/rstack/.env").write_text("EXAMPLE=private")
        with self.assertRaisesRegex(ValueError, "local state"):
            rstack.package(self.root)

    def test_portable_frontmatter_rejects_invalid_optional_fields(self):
        source = self.root / "plugins/rstack/skills/stop-slop/SKILL.md"
        original = source.read_text()
        for field in ('license: " "', 'compatibility: " "', 'allowed-tools: []',
                      'metadata:\n  version: 1', 'description: duplicate'):
            with self.subTest(field=field):
                source.write_text(original.replace('license: MIT', field))
                with self.assertRaises(ValueError):
                    rstack.check(self.root)
        source.write_text(original)

    def test_explicit_policy_is_consistent_across_hosts(self):
        skill = self.root / "plugins/rstack/skills/factory"
        adapter = skill / "agents/openai.yaml"
        original = adapter.read_text()
        for policy in ({}, {"allow_implicit_invocation": True}):
            with self.subTest(policy=policy):
                metadata = yaml.safe_load(original)
                metadata["policy"] = policy
                adapter.write_text(yaml.safe_dump(metadata))
                with self.assertRaisesRegex(ValueError, "Explicit-only"):
                    rstack.check(self.root)
        adapter.unlink()
        with self.assertRaisesRegex(ValueError, "Explicit-only"):
            rstack.check(self.root)
        adapter.write_text(original)
        source = skill / "SKILL.md"
        source.write_text(source.read_text().replace(
            'disable-model-invocation: true',
            'disable-model-invocation: true\nmetadata:\n  opencode/autoinvoke: "true"'))
        with self.assertRaisesRegex(ValueError, "Conflicting invocation"):
            rstack.check(self.root)

    def test_ui_prompt_targets_its_own_skill(self):
        adapter = self.root / "plugins/rstack/skills/launch-video/agents/openai.yaml"
        metadata = yaml.safe_load(adapter.read_text())
        for prompt in ('Use $factory to make a video.', 'Use $launch-video-other for this.'):
            with self.subTest(prompt=prompt):
                metadata["interface"]["default_prompt"] = prompt
                adapter.write_text(yaml.safe_dump(metadata))
                with self.assertRaisesRegex(ValueError, "default_prompt"):
                    rstack.check(self.root)

    def test_ui_blurb_uses_local_picker_limits(self):
        adapter = self.root / "plugins/rstack/skills/launch-video/agents/openai.yaml"
        metadata = yaml.safe_load(adapter.read_text())
        for blurb in ('Video', 'x' * 65):
            with self.subTest(blurb=blurb):
                metadata["interface"]["short_description"] = blurb
                adapter.write_text(yaml.safe_dump(metadata))
                with self.assertRaisesRegex(ValueError, "short_description"):
                    rstack.check(self.root)


if __name__ == "__main__":
    unittest.main()
