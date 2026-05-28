from __future__ import annotations

import pathlib
import unittest

from memory_governor.audit.diagnostics import StructuredDiagnostic, render_summary
from memory_governor.audit.reconciliation import (
    AuthorizationPolicy,
    CapabilityDeclaration,
    DiagnosisConfig,
    reconcile_capability_contract,
)
from memory_governor.audit.skill_contracts import parse_capability_declaration
from memory_governor.contract.capabilities import CAPABILITY_FAMILIES, HIGH_RISK_CAPABILITY_FAMILIES
from memory_governor.contract.diagnosis_registry import DIAGNOSIS_REGISTRY, DIAGNOSIS_TYPES, SEVERITY_ERROR, SEVERITY_WARN
from memory_governor.contract.reconciliation_policy import CLAIM_SOURCE, HOST_SOURCE, OBSERVED_SOURCE, SOURCE_PRECEDENCE


REPO_ROOT = pathlib.Path(__file__).resolve().parents[1]
PUBLISH_ROOT = REPO_ROOT / "publish" / "clawhub"


def read(path: pathlib.Path) -> str:
    return path.read_text(encoding="utf-8")


class ContractCoreTests(unittest.TestCase):
    def test_capability_taxonomy_is_centered(self) -> None:
        self.assertEqual(
            CAPABILITY_FAMILIES,
            ("writer", "consumer", "compiler", "promoter"),
        )
        self.assertEqual(HIGH_RISK_CAPABILITY_FAMILIES, {"promoter"})

    def test_diagnosis_registry_covers_named_failures(self) -> None:
        self.assertIn("MissingCapabilityDeclaration", DIAGNOSIS_REGISTRY)
        self.assertIn("CanonicalCompiledBoundaryViolation", DIAGNOSIS_REGISTRY)
        self.assertEqual(
            DIAGNOSIS_REGISTRY["UnauthorizedPromotionPath"]["severity"],
            SEVERITY_ERROR,
        )
        self.assertEqual(
            DIAGNOSIS_REGISTRY["ProvisionalCapabilityDiagnosis"]["severity"],
            SEVERITY_WARN,
        )
        self.assertEqual(tuple(DIAGNOSIS_REGISTRY.keys()), DIAGNOSIS_TYPES)

    def test_reconciliation_source_order_is_explicit(self) -> None:
        self.assertEqual(
            SOURCE_PRECEDENCE,
            (CLAIM_SOURCE, HOST_SOURCE, OBSERVED_SOURCE),
        )

    def test_structured_diagnostic_renders_human_summary(self) -> None:
        diagnostic = StructuredDiagnostic(
            diagnosis_type="ManifestSkillContractMismatch",
            severity=SEVERITY_ERROR,
            primary_cause="host_authorization_conflict",
            secondary_contributors=["skill_claim_promoter"],
            capability_family="promoter",
            target_classes_involved=["learning_candidates", "reusable_lessons"],
            artifacts_involved=["memory-governor-host.toml", "skills/example/SKILL.md"],
            provisional=True,
            coverage_gaps=["no_behavior_trace"],
            repair_hints=["Authorize promoter in host manifest"],
        )

        summary = render_summary(diagnostic)
        self.assertIn("ERROR ManifestSkillContractMismatch: host_authorization_conflict", summary)
        self.assertIn("capability_family: promoter", summary)
        self.assertIn("secondary_contributors: skill_claim_promoter", summary)
        self.assertIn("provisional: true", summary)
        self.assertIn("coverage_gaps: no_behavior_trace", summary)
        self.assertIn("repair_hints: Authorize promoter in host manifest", summary)

    def test_reconciliation_emits_high_risk_promotion_diagnostic(self) -> None:
        diagnostics = reconcile_capability_contract(
            CapabilityDeclaration(
                families=["writer", "promoter"],
                source_artifact="skill/SKILL.md [capabilities]",
            ),
            AuthorizationPolicy(
                allowed_capabilities=["writer"],
                source_artifact="memory-governor-host.toml [authorization]",
            ),
            DiagnosisConfig(enabled_types=["UnauthorizedPromotionPath"]),
        )

        self.assertEqual(len(diagnostics), 1)
        diagnostic = diagnostics[0]
        self.assertEqual(diagnostic.diagnosis_type, "UnauthorizedPromotionPath")
        self.assertEqual(diagnostic.severity, SEVERITY_ERROR)
        self.assertEqual(diagnostic.capability_family, "promoter")
        self.assertIn("claim_without_authorization", diagnostic.secondary_contributors)

    def test_skill_contract_parser_extracts_machine_readable_capabilities(self) -> None:
        text = """## Memory Contract

This skill follows `memory-governor`.

### Capability Declaration

```toml
[capabilities]
families = ["writer", "compiler"]
```
"""
        families, error = parse_capability_declaration(text)
        self.assertIsNone(error)
        self.assertEqual(families, ["writer", "compiler"])

    def test_publish_bundle_contains_shared_contract_core(self) -> None:
        relative_paths = [
            "memory_governor/__init__.py",
            "memory_governor/contract/__init__.py",
            "memory_governor/contract/capabilities.py",
            "memory_governor/contract/diagnosis_registry.py",
            "memory_governor/contract/reconciliation_policy.py",
            "memory_governor/audit/__init__.py",
            "memory_governor/audit/diagnostics.py",
        ]

        for relative_path in relative_paths:
            root_path = REPO_ROOT / relative_path
            publish_path = PUBLISH_ROOT / relative_path
            self.assertTrue(root_path.exists(), f"missing root file {relative_path}")
            self.assertTrue(publish_path.exists(), f"publish bundle missing {relative_path}")
            self.assertEqual(read(root_path), read(publish_path), f"publish bundle drift detected for {relative_path}")


if __name__ == "__main__":
    unittest.main()
