from __future__ import annotations

import pathlib
import subprocess
import sys
import unittest


REPO_ROOT = pathlib.Path(__file__).resolve().parents[1]
VALIDATOR = REPO_ROOT / "scripts" / "validate-memory-frontmatter.py"
FIXTURES = REPO_ROOT / "tests" / "fixtures" / "validator"


class ValidatorTests(unittest.TestCase):
    def run_validator(self, *paths: pathlib.Path) -> subprocess.CompletedProcess[str]:
        return subprocess.run(
            [sys.executable, str(VALIDATOR), *[str(path) for path in paths]],
            capture_output=True,
            text=True,
            check=False,
        )

    def test_valid_files_pass(self) -> None:
        result = self.run_validator(
            FIXTURES / "valid-proactive-state.md",
            FIXTURES / "valid-reusable-lessons.md",
            FIXTURES / "valid-working-buffer.md",
        )
        self.assertEqual(result.returncode, 0, result.stderr)
        self.assertIn("OK", result.stdout)

    def test_missing_frontmatter_fails(self) -> None:
        result = self.run_validator(FIXTURES / "invalid-missing-frontmatter.md")
        self.assertNotEqual(result.returncode, 0)
        self.assertIn("missing TOML frontmatter start delimiter", result.stderr)

    def test_wrong_enum_fails(self) -> None:
        result = self.run_validator(FIXTURES / "invalid-working-buffer-enum.md")
        self.assertNotEqual(result.returncode, 0)
        self.assertIn("buffer_status must be one of", result.stderr)

    def test_missing_heading_fails(self) -> None:
        result = self.run_validator(FIXTURES / "invalid-reusable-lessons-heading.md")
        self.assertNotEqual(result.returncode, 0)
        self.assertIn("missing required heading", result.stderr)


if __name__ == "__main__":
    unittest.main()
