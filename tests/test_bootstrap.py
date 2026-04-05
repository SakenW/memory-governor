from __future__ import annotations

import pathlib
import subprocess
import sys
import tempfile
import unittest


REPO_ROOT = pathlib.Path(__file__).resolve().parents[1]
BOOTSTRAP = REPO_ROOT / "scripts" / "bootstrap-generic-host.sh"
CHECKER = REPO_ROOT / "scripts" / "check-memory-host.py"


class BootstrapTests(unittest.TestCase):
    def test_bootstrap_creates_valid_generic_host(self) -> None:
        with tempfile.TemporaryDirectory() as tmpdir:
            target = pathlib.Path(tmpdir) / "host"

            bootstrap = subprocess.run(
                ["sh", str(BOOTSTRAP), str(target)],
                capture_output=True,
                text=True,
                check=False,
            )
            self.assertEqual(bootstrap.returncode, 0, bootstrap.stderr)
            self.assertTrue((target / "HOST.md").exists())
            self.assertTrue((target / "memory-governor-host.toml").exists())
            self.assertTrue((target / "memory" / "proactive-state.md").exists())

            check = subprocess.run(
                [sys.executable, str(CHECKER), str(target)],
                capture_output=True,
                text=True,
                check=False,
            )
            self.assertEqual(check.returncode, 0, check.stderr)
            self.assertIn("STATUS: PASS", check.stdout)


if __name__ == "__main__":
    unittest.main()
