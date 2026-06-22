from __future__ import annotations

import pathlib
import unittest


REPO_ROOT = pathlib.Path(__file__).resolve().parents[1]
PUBLISH_ROOT = REPO_ROOT / "publish" / "clawhub"


def read(path: pathlib.Path) -> str:
    return path.read_text(encoding="utf-8")


class ContractDocsTests(unittest.TestCase):
    def test_skill_declares_learning_candidates_target_class(self) -> None:
        content = read(REPO_ROOT / "SKILL.md")
        self.assertIn("- `learning_candidates`", content)
        self.assertIn("low-commitment staging layer", content)
        self.assertIn("references/correction-pipeline.md", content)

    def test_correction_pipeline_exists_and_describes_staging_flow(self) -> None:
        path = REPO_ROOT / "references" / "correction-pipeline.md"
        self.assertTrue(path.exists(), f"missing {path}")
        content = read(path)
        self.assertIn("correction is captured in `learning_candidates`", content)
        self.assertIn("candidate is reviewed for promotion into `reusable_lessons`", content)
        self.assertIn("至少满足任意两个条件", content)

    def test_candidate_review_workflow_exists(self) -> None:
        path = REPO_ROOT / "references" / "candidate-review.md"
        self.assertTrue(path.exists(), f"missing {path}")
        content = read(path)
        self.assertIn("keep", content)
        self.assertIn("promote", content)
        self.assertIn("discard", content)
        self.assertIn("review-learning-candidates.py", content)

    def test_routing_and_promotion_docs_use_candidate_layer(self) -> None:
        routing = read(REPO_ROOT / "references" / "memory-routing.md")
        promotion = read(REPO_ROOT / "references" / "promotion-rules.md")
        precedence = read(REPO_ROOT / "references" / "routing-precedence.md")
        read_order = read(REPO_ROOT / "references" / "read-order.md")

        self.assertIn("| 明确纠错 | 用户明确纠正、明确否定，但还未证明跨任务复用 | `learning_candidates` |", routing)
        self.assertIn("### correction → learning_candidates", promotion)
        self.assertIn("### learning_candidates → reusable_lessons", promotion)
        self.assertIn("默认先写 `learning_candidates`", precedence)
        self.assertIn("do not read `learning_candidates` during normal startup", read_order)

    def test_skill_integration_documents_candidate_staging_and_sampling_boundary(self) -> None:
        content = read(REPO_ROOT / "references" / "skill-integration.md")
        self.assertIn("explicit corrections -> `learning_candidates`", content)
        self.assertIn("## Correction Staging Rule", content)
        self.assertIn("## Sampling Boundary", content)
        self.assertIn("不要求所有宿主立刻接入自动 sampling", content)

    def test_readme_homepage_positioning_includes_learning_candidates(self) -> None:
        content = read(REPO_ROOT / "README.md")
        self.assertIn("Aligned with the OpenClaw 2026.6.x memory stack", content)
        self.assertIn("was built to give those systems one shared contract", content)
        self.assertIn("`memory type -> target class -> adapter / fallback`", content)
        self.assertIn("`learning_candidates` layer for explicit corrections", content)
        self.assertIn("`memory-governor` 不是因为 Dreaming 才出现的", content)
        self.assertIn("Dreaming 负责后台巩固", content)
        self.assertIn("People Wiki", content)
        self.assertIn("compiled-surfaces.md", content)

    def test_checker_and_validator_support_learning_candidates(self) -> None:
        checker = read(REPO_ROOT / "scripts" / "check-memory-host.py")
        validator = read(REPO_ROOT / "scripts" / "validate-memory-frontmatter.py")
        host_checker_tests = read(REPO_ROOT / "tests" / "test_host_checker.py")
        reviewer = read(REPO_ROOT / "scripts" / "review-learning-candidates.py")

        self.assertIn('"learning_candidates"', checker)
        self.assertIn("host_entry_paths", checker)
        self.assertIn("writer_contract_paths", checker)
        self.assertIn('"candidate_status"', validator)
        self.assertIn("test_learning_candidates_manifest_target_passes", host_checker_tests)
        self.assertIn("review overdue", reviewer)

    def test_integration_host_fixtures_exist_for_checker_coverage(self) -> None:
        required_paths = [
            "tests/fixtures/hosts/integration-missing/HOST.md",
            "tests/fixtures/hosts/integration-missing/memory-governor-host.toml",
            "tests/fixtures/hosts/integration-placeholder/HOST.md",
            "tests/fixtures/hosts/integration-placeholder/memory-governor-host.toml",
            "tests/fixtures/hosts/integration-placeholder/skills/example-writer/SKILL.md",
        ]

        for relative_path in required_paths:
            path = REPO_ROOT / relative_path
            self.assertTrue(path.exists(), f"missing test fixture {relative_path}")

    def test_version_and_changelog_match_new_contract_release(self) -> None:
        version = read(REPO_ROOT / "VERSION").strip()
        changelog = read(REPO_ROOT / "CHANGELOG.md")

        self.assertEqual(version, "0.3.0")
        self.assertIn("## 0.3.0 - 2026-06-23", changelog)
        self.assertIn("## 0.2.10 - 2026-05-28", changelog)
        self.assertIn("Active Memory", changelog)
        self.assertIn("learning_candidates", changelog)
        self.assertIn("compiled-surfaces.md", changelog)

    def test_compiled_surfaces_reference_exists_and_binds_new_official_surfaces(self) -> None:
        path = REPO_ROOT / "references" / "compiled-surfaces.md"
        self.assertTrue(path.exists(), f"missing {path}")
        content = read(path)
        self.assertIn("none of them is a memory target class", content)
        self.assertIn("People Wiki", content)
        self.assertIn("Memory Palace", content)
        self.assertIn("Imported Insights", content)
        self.assertIn("allowedChatIds", content)
        self.assertIn("[dreaming-integration.md](dreaming-integration.md)", content)

    def test_publish_bundle_is_synced_for_core_contract_files(self) -> None:
        relative_paths = [
            "SKILL.md",
            "README.md",
            "CHANGELOG.md",
            "VERSION",
            "examples/generic-host/README.md",
            "examples/generic-host/memory-governor-host.toml",
            "references/adapter-manifest.md",
            "references/adapters.md",
            "references/candidate-review.md",
            "references/compiled-surfaces.md",
            "references/correction-pipeline.md",
            "references/dreaming-integration.md",
            "references/exclusions.md",
            "references/host-checker.md",
            "references/host-profiles.md",
            "references/installation-integration.md",
            "references/memory-routing.md",
            "references/migration-guide.md",
            "references/promotion-rules.md",
            "references/read-order.md",
            "references/routing-precedence.md",
            "references/skill-integration.md",
            "references/stateful-targets.md",
            "assets/fallbacks/learning-candidates.md",
            "scripts/check-memory-host.py",
            "scripts/review-learning-candidates.py",
        ]

        for relative_path in relative_paths:
            root_path = REPO_ROOT / relative_path
            publish_path = PUBLISH_ROOT / relative_path
            self.assertTrue(publish_path.exists(), f"publish bundle missing {relative_path}")
            self.assertEqual(
                read(root_path),
                read(publish_path),
                f"publish bundle drift detected for {relative_path}",
            )


if __name__ == "__main__":
    unittest.main()
