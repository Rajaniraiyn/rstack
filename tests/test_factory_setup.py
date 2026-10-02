import json
from pathlib import Path
import tempfile
import types
import unittest


ROOT = Path(__file__).resolve().parents[1]
source = ROOT / "plugins/rstack/skills/factory/scripts/factory-setup.py"
factory_setup = types.ModuleType("factory_setup")
exec(compile(source.read_text(), str(source), "exec"), factory_setup.__dict__)


class FactorySetupTests(unittest.TestCase):
    def setUp(self):
        temp = tempfile.TemporaryDirectory()
        self.addCleanup(temp.cleanup)
        self.path = Path(temp.name) / "rstack/factory.json"

    def test_refresh_preserves_routing_and_custom_harnesses(self):
        self.path.parent.mkdir()
        self.path.write_text(json.dumps({
            "budget": 5,
            "harnesses": {
                "codex": {"model": "user-selected", "version": "old"},
                "custom": {"command": "local-worker"},
            },
        }))
        detected = {"installed": True, "path": "/bin/codex", "version": "new"}
        factory_setup.save_report(self.path, {"codex": detected})
        config = json.loads(self.path.read_text())
        self.assertEqual(config["budget"], 5)
        self.assertEqual(config["harnesses"]["custom"], {"command": "local-worker"})
        self.assertEqual(config["harnesses"]["codex"], {"model": "user-selected", **detected})

    def test_first_write_creates_config(self):
        factory_setup.save_report(self.path, {"codex": {"installed": False}})
        self.assertEqual(json.loads(self.path.read_text()), {
            "harnesses": {"codex": {"installed": False}}})

    def test_invalid_config_is_preserved(self):
        self.path.parent.mkdir()
        for invalid in ('{broken', '[]', '{"harnesses": []}', '{"harnesses": {"codex": 1}}'):
            with self.subTest(invalid=invalid):
                self.path.write_text(invalid)
                with self.assertRaises(ValueError):
                    factory_setup.save_report(self.path, {"codex": {"installed": False}})
                self.assertEqual(self.path.read_text(), invalid)


if __name__ == "__main__":
    unittest.main()
