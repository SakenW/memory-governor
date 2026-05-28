from __future__ import annotations

import pathlib
import subprocess
import sys
import unittest


REPO_ROOT = pathlib.Path(__file__).resolve().parents[1]
REVIEWER = REPO_ROOT / "scripts" / "review-learning-candidates.py"
FIXTURES = REPO_ROOT / "tests" / "fixtures" / "validator"


class CandidateReviewTests(unittest.TestCase):
    def run_reviewer(
        self,
        *paths: pathlib.Path,
        stale_days: int = 7,
        now: str | None = None,
    ) -> subprocess.CompletedProcess[str]:
        command = [
            sys.executable,
            str(REVIEWER),
            "--stale-days",
            str(stale_days),
        ]
        if now is not None:
            command.extend(["--now", now])
        command.extend(str(path) for path in paths)
        return subprocess.run(
            command,
            capture_output=True,
            text=True,
            check=False,
        )

    def test_fresh_learning_candidates_file_is_ok(self) -> None:
        result = self.run_reviewer(
            FIXTURES / "valid-learning-candidates.md",
            stale_days=30,
            now="2026-04-06T00:00:00Z",
        )
        self.assertEqual(result.returncode, 0, result.stderr)
        self.assertIn("STATUS: OK", result.stdout)
        self.assertIn("candidate_items: 1", result.stdout)
        self.assertIn("structured_candidates: 1", result.stdout)
        self.assertIn("unstructured_candidates: 0", result.stdout)
        self.assertIn("stage_collecting_evidence: 1", result.stdout)
        self.assertIn("keep, promote, or discard", result.stdout)

    def test_stale_learning_candidates_file_warns_but_passes(self) -> None:
        result = self.run_reviewer(FIXTURES / "stale-learning-candidates.md", stale_days=7)
        self.assertEqual(result.returncode, 0, result.stderr)
        self.assertIn("STATUS: WARN", result.stdout)
        self.assertIn("review overdue", result.stdout)
        self.assertIn("stage_ready_for_promotion: 1", result.stdout)
        self.assertIn("ready_for_promotion", result.stdout)

    def test_unstructured_learning_candidates_warns_but_passes(self) -> None:
        result = self.run_reviewer(FIXTURES / "unstructured-learning-candidates.md")
        self.assertEqual(result.returncode, 0, result.stderr)
        self.assertIn("STATUS: WARN", result.stdout)
        self.assertIn("some candidate items are still unstructured", result.stdout)

    def test_invalid_lifecycle_stage_warns_but_passes(self) -> None:
        result = self.run_reviewer(FIXTURES / "invalid-lifecycle-stage-learning-candidates.md")
        self.assertEqual(result.returncode, 0, result.stderr)
        self.assertIn("STATUS: WARN", result.stdout)
        self.assertIn("invalid lifecycle_stage", result.stdout)

    def test_invalid_learning_candidates_file_fails(self) -> None:
        result = self.run_reviewer(FIXTURES / "invalid-learning-candidates-status.md")
        self.assertNotEqual(result.returncode, 0)
        self.assertIn("candidate_status must be one of", result.stderr)


if __name__ == "__main__":
    unittest.main()
