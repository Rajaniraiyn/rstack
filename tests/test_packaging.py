import importlib.util
import json
from pathlib import Path
import shutil
import tempfile
import unittest
import zipfile

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
        rstack.sync(self.root)

    def test_skill_export_is_complete_and_reproducible(self):
        paths = rstack.package(self.root)
        first = {path.name: path.read_bytes() for path in paths}
        self.assertEqual(first, {path.name: path.read_bytes() for path in rstack.package(self.root)})
        skill = self.root / "plugins/rstack/skills/rstack-author-skill"
        with zipfile.ZipFile(paths[1]) as archive:
            for source in skill.rglob("*"):
                if source.is_file():
                    self.assertEqual(archive.read(source.relative_to(skill.parent).as_posix()), source.read_bytes())
            self.assertIn("rstack-author-skill/SKILL.md", archive.namelist())

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


if __name__ == "__main__":
    unittest.main()
