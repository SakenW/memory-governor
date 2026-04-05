from __future__ import annotations

import pathlib
import subprocess
import sys
import unittest


REPO_ROOT = pathlib.Path(__file__).resolve().parents[1]
CHECKER = REPO_ROOT / "scripts" / "check-memory-host.py"
HOST_FIXTURES = REPO_ROOT / "tests" / "fixtures" / "hosts"


class HostCheckerTests(unittest.TestCase):
    def run_checker(self, host_root: pathlib.Path) -> subprocess.CompletedProcess[str]:
        return subprocess.run(
            [sys.executable, str(CHECKER), str(host_root)],
            capture_output=True,
            text=True,
            check=False,
        )

    def test_generic_host_example_passes(self) -> None:
        result = self.run_checker(REPO_ROOT / "examples" / "generic-host")
        self.assertEqual(result.returncode, 0, result.stderr)
        self.assertIn("PROFILE: manifest", result.stdout)
        self.assertIn("STATUS: PASS", result.stdout)

    def test_manifest_fallback_host_passes(self) -> None:
        result = self.run_checker(HOST_FIXTURES / "manifest-fallback")
        self.assertEqual(result.returncode, 0, result.stderr)
        self.assertIn("STATUS: PASS", result.stdout)
        self.assertIn("fallback", result.stdout)

    def test_broken_manifest_host_fails(self) -> None:
        result = self.run_checker(HOST_FIXTURES / "broken-manifest")
        self.assertNotEqual(result.returncode, 0)
        self.assertIn("STATUS: FAIL", result.stdout)
        self.assertIn("mode must be one of", result.stdout)

    def test_split_host_with_one_canonical_slice_warns_but_passes(self) -> None:
        result = self.run_checker(HOST_FIXTURES / "split-mixed")
        self.assertEqual(result.returncode, 0, result.stderr)
        self.assertIn("STATUS: WARN", result.stdout)
        self.assertIn("schema-valid slice", result.stdout)
        self.assertIn("non-canonical slice", result.stdout)

    def test_directory_pattern_host_passes(self) -> None:
        result = self.run_checker(HOST_FIXTURES / "directory-pattern")
        self.assertEqual(result.returncode, 0, result.stderr)
        self.assertIn("STATUS: PASS", result.stdout)
        self.assertIn("pattern notes/daily/YYYY-MM-DD.md", result.stdout)
        self.assertIn("reusable_lessons: memory/reusable-lessons", result.stdout)

    def test_unknown_target_warns_but_passes(self) -> None:
        result = self.run_checker(HOST_FIXTURES / "unknown-target")
        self.assertEqual(result.returncode, 0, result.stderr)
        self.assertIn("STATUS: WARN", result.stdout)
        self.assertIn("manifest target 'learning_candidates'", result.stdout)

    def test_missing_primary_and_fallback_fails(self) -> None:
        result = self.run_checker(HOST_FIXTURES / "missing-fallback")
        self.assertNotEqual(result.returncode, 0)
        self.assertIn("STATUS: FAIL", result.stdout)
        self.assertIn("fallback missing", result.stdout)


if __name__ == "__main__":
    unittest.main()
