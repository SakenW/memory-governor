from __future__ import annotations

import os
import pathlib
import subprocess
import sys
import tempfile
import unittest


REPO_ROOT = pathlib.Path(__file__).resolve().parents[1]
CHECKER = REPO_ROOT / "scripts" / "check-memory-host.py"
FALLBACKS = REPO_ROOT / "assets" / "fallbacks"


def write(path: pathlib.Path, content: str) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(content, encoding="utf-8")


def copy_fallback(name: str, dest: pathlib.Path) -> None:
    dest.parent.mkdir(parents=True, exist_ok=True)
    dest.write_text((FALLBACKS / name).read_text(encoding="utf-8"), encoding="utf-8")


class OpenClawProfileTests(unittest.TestCase):
    def run_checker(
        self,
        host_root: pathlib.Path,
        *,
        home: pathlib.Path,
        profile: str = "auto",
    ) -> subprocess.CompletedProcess[str]:
        env = os.environ.copy()
        env["HOME"] = str(home)
        return subprocess.run(
            [sys.executable, str(CHECKER), str(host_root), "--profile", profile],
            capture_output=True,
            text=True,
            check=False,
            env=env,
        )

    def create_openclaw_workspace(self, root: pathlib.Path) -> None:
        write(
            root / "AGENTS.md",
            "# Memory Governance\n\nThis OpenClaw workspace follows memory-governor routing and promotion rules.\n",
        )
        write(root / "MEMORY.md", "# Memory\n\nLong-term facts and stable preferences.\n")
        write(root / "TOOLS.md", "# Tools\n\nTool-specific durable rules.\n")
        (root / "memory").mkdir(parents=True, exist_ok=True)

    def test_openclaw_fallback_only_workspace_passes(self) -> None:
        with tempfile.TemporaryDirectory() as tmpdir:
            tmp = pathlib.Path(tmpdir)
            home = tmp / "home"
            workspace = tmp / "workspace"
            home.mkdir()
            self.create_openclaw_workspace(workspace)

            copy_fallback("reusable-lessons.md", workspace / "memory" / "reusable-lessons.md")
            copy_fallback("learning-candidates.md", workspace / "memory" / "learning-candidates.md")
            copy_fallback("proactive-state.md", workspace / "memory" / "proactive-state.md")
            copy_fallback("working-buffer.md", workspace / "memory" / "working-buffer.md")

            result = self.run_checker(workspace, home=home)
            self.assertEqual(result.returncode, 0, result.stderr)
            self.assertIn("PROFILE: openclaw", result.stdout)
            self.assertIn("STATUS: PASS", result.stdout)
            self.assertIn("reusable_lessons fallback", result.stdout)
            self.assertIn("learning_candidates fallback", result.stdout)
            self.assertIn("proactive_state fallback", result.stdout)
            self.assertIn("working_buffer fallback", result.stdout)

    def test_openclaw_external_adapter_workspace_passes(self) -> None:
        with tempfile.TemporaryDirectory() as tmpdir:
            tmp = pathlib.Path(tmpdir)
            home = tmp / "home"
            workspace = tmp / "workspace"
            home.mkdir()
            self.create_openclaw_workspace(workspace)

            write(home / "self-improving" / "memory.md", "# Self Improving\n")
            write(home / "self-improving" / "candidates.md", "# Candidates\n")
            write(home / "proactivity" / "memory.md", "# Proactivity Memory\n")
            write(home / "proactivity" / "session-state.md", "# Session State\n")
            write(home / "proactivity" / "memory" / "working-buffer.md", "# Working Buffer\n")

            result = self.run_checker(workspace, home=home)
            self.assertEqual(result.returncode, 0, result.stderr)
            self.assertIn("PROFILE: openclaw", result.stdout)
            self.assertIn("STATUS: PASS", result.stdout)
            self.assertIn("external self-improving detected", result.stdout)
            self.assertIn("external self-improving candidates detected", result.stdout)
            self.assertIn("split proactivity adapter detected", result.stdout)
            self.assertIn("external proactivity buffer detected", result.stdout)

    def test_openclaw_partial_external_adapter_fails_without_local_fallbacks(self) -> None:
        with tempfile.TemporaryDirectory() as tmpdir:
            tmp = pathlib.Path(tmpdir)
            home = tmp / "home"
            workspace = tmp / "workspace"
            home.mkdir()
            self.create_openclaw_workspace(workspace)

            write(home / "self-improving" / "memory.md", "# Self Improving\n")
            write(home / "proactivity" / "memory.md", "# Proactivity Memory\n")

            result = self.run_checker(workspace, home=home)
            self.assertNotEqual(result.returncode, 0)
            self.assertIn("PROFILE: openclaw", result.stdout)
            self.assertIn("STATUS: FAIL", result.stdout)
            self.assertIn("learning_candidates fallback: missing", result.stdout)
            self.assertIn("proactive_state fallback: missing", result.stdout)
            self.assertIn("working_buffer fallback: missing", result.stdout)

    def test_openclaw_invalid_local_fallback_fails_schema_validation(self) -> None:
        with tempfile.TemporaryDirectory() as tmpdir:
            tmp = pathlib.Path(tmpdir)
            home = tmp / "home"
            workspace = tmp / "workspace"
            home.mkdir()
            self.create_openclaw_workspace(workspace)

            write(
                workspace / "memory" / "reusable-lessons.md",
                "+++\n"
                'target_class = "reusable_lessons"\n'
                'schema_version = "0.1"\n'
                'updated_at = "2026-04-05T00:00:00Z"\n'
                'scope = "global"\n'
                "+++\n\n"
                "# reusable-lessons.md\n",
            )
            copy_fallback("learning-candidates.md", workspace / "memory" / "learning-candidates.md")
            copy_fallback("proactive-state.md", workspace / "memory" / "proactive-state.md")
            copy_fallback("working-buffer.md", workspace / "memory" / "working-buffer.md")

            result = self.run_checker(workspace, home=home)
            self.assertNotEqual(result.returncode, 0)
            self.assertIn("PROFILE: openclaw", result.stdout)
            self.assertIn("STATUS: FAIL", result.stdout)
            self.assertIn("missing required heading '## Lessons'", result.stdout)


if __name__ == "__main__":
    unittest.main()
