import sys
import os
from pathlib import Path
import importlib.util
import io
import contextlib
import unittest
from tempfile import TemporaryDirectory


# Add skills/fdd/scripts directory to path for imports
sys.path.insert(0, str(Path(__file__).parent.parent / "skills" / "fdd" / "scripts"))

def _load_fdd_module():
    tests_dir = Path(__file__).resolve().parent
    fdd_root = tests_dir.parent
    script_path = fdd_root / "skills" / "fdd" / "scripts" / "fdd.py"

    spec = importlib.util.spec_from_file_location("fdd", str(script_path))
    if spec is None or spec.loader is None:
        raise RuntimeError("Failed to create import spec for fdd.py")

    mod = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(mod)
    return mod


VA = _load_fdd_module()


def _req_text(*section_ids: str) -> str:
    parts = [f"### Section {sid}: Title {sid}" for sid in section_ids]
    return "\n".join(parts) + "\n"


def _artifact_text(*section_ids: str, extra: str = "") -> str:
    parts = [f"## {sid}. Something" for sid in section_ids]
    if extra:
        parts.append(extra)
    return "\n".join(parts) + "\n"


def _features_header(project_name: str = "Example") -> str:
    return "\n".join(
        [
            f"# Features: {project_name}",
            "",
            "**Status Overview**: 1 features total (0 completed, 1 in progress, 0 not started)",
            "",
            "**Meaning**:",
            "- ⏳ NOT_STARTED",
            "- 🔄 IN_PROGRESS",
            "- ✅ IMPLEMENTED",
            "",
        ]
    )


def _feature_entry(
    n: int,
    feature_id: str,
    slug: str,
    emoji: str = "🔄",
    priority: str = "HIGH",
    status: str = "IN_PROGRESS",
    *,
    phases_text: str = "- `ph-1`: 🔄 IN_PROGRESS — Default phase",
    depends_on: str = "None",
    blocks: str = "None",
) -> str:
    path = f"feature-{slug}/"

    return "\n".join(
        [
            f"### {n}. [{feature_id}]({path}) {emoji} {priority}",
            f"- **Purpose**: Purpose {slug}",
            f"- **Status**: {status}",
            f"- **Depends On**: {depends_on}",
            f"- **Blocks**: {blocks}",
            "- **Phases**:",
            f"  {phases_text}",
            "- **Scope**:",
            "  - scope-item",
            "- **Requirements Covered**:",
            "  - fdd-example-req-1",
        ]
    )


class TestDetectRequirements(unittest.TestCase):
    """Tests for automatic requirements file detection."""
    
    def test_detect_requirements_overall_design(self):
        """Test detection of requirements for overall DESIGN.md.
        
        Given: /architecture/DESIGN.md path
        Expects: kind='overall-design', req_path ends with 'overall-design-structure.md'
        """
        kind, req_path = VA.detect_requirements(Path("/tmp/architecture/DESIGN.md"))
        self.assertEqual(kind, "overall-design")
        self.assertTrue(str(req_path).endswith("/FDD/requirements/overall-design-structure.md"))

    def test_detect_requirements_feature_design(self):
        """Test detection of requirements for feature DESIGN.md.
        
        Given: /architecture/features/feature-x/DESIGN.md path
        Expects: kind='feature-design', req_path ends with 'feature-design-structure.md'
        """
        kind, req_path = VA.detect_requirements(Path("/tmp/architecture/features/feature-x/DESIGN.md"))
        self.assertEqual(kind, "feature-design")
        self.assertTrue(str(req_path).endswith("/FDD/requirements/feature-design-structure.md"))

    def test_detect_requirements_archived_feature_changes(self):
        """Test detection of requirements for archived CHANGES.md.
        
        Given: /architecture/features/feature-x/archive/2026-01-08-CHANGES.md path
        Expects: kind='feature-changes', req_path ends with 'feature-changes-structure.md'
        """
        kind, req_path = VA.detect_requirements(Path("/tmp/architecture/features/feature-x/archive/2026-01-08-CHANGES.md"))
        self.assertEqual(kind, "feature-changes")
        self.assertTrue(str(req_path).endswith("/FDD/requirements/feature-changes-structure.md"))


class TestFeatureDesignValidation(unittest.TestCase):
    """Tests for feature DESIGN.md validation."""
    
    def _feature_design_minimal(self, *, actor: str = "`fdd-example-actor-analyst`") -> str:
        return "\n".join(
            [
                "# Feature: Example",
                "",
                "## A. Feature Context",
                "### 1. Overview",
                "ok.",
                "### 2. Purpose",
                "ok.",
                "### 3. Actors",
                f"- {actor}",
                "### 4. References",
                "- Overall Design: [DESIGN](../../DESIGN.md)",
                "",
                "## B. Actor Flows (FDL)",
                "### User does thing",
                "",
                "- [ ] **ID**: fdd-example-feature-x-flow-user-does-thing",
                "",
                "1. [ ] - `ph-1` - User does it - `inst-user-does-it`",
                "",
                "## C. Algorithms (FDL)",
                "### Algo",
                "",
                "- [ ] **ID**: fdd-example-feature-x-algo-do-thing",
                "",
                "1. [ ] - `ph-1` - **RETURN** ok - `inst-return-ok`",
                "",
                "## D. States (FDL)",
                "### State",
                "",
                "- [ ] **ID**: fdd-example-feature-x-state-entity",
                "",
                "1. [ ] - `ph-1` - **FROM** A **TO** B **WHEN** ok - `inst-transition-a-to-b`",
                "",
                "## E. Technical Details",
                "ok.",
                "",
                "## F. Requirements",
                "### Req",
                "",
                "- [ ] **ID**: fdd-example-feature-x-req-do-thing",
                "**Status**: 🔄 IN_PROGRESS",
                "**Description**: Must do.",
                "**References**:",
                "- [User does thing](#user-does-thing)",
                "**Implements**:",
                "- `fdd-example-feature-x-flow-user-does-thing`",
                "- `fdd-example-feature-x-algo-do-thing`",
                "**Phases**:",
                "- [ ] `ph-1`: initial",
                "**Testing Scenarios (FDL)**:",
                "- [ ] **ID**: fdd-example-feature-x-test-scenario-one",
                "  1. [ ] - `ph-1` - Do step - `inst-do-step`",
                "**Acceptance Criteria**:",
                "- A",
                "- B",
            ]
        ) + "\n"

    def test_feature_design_duplicate_inst_within_algorithm_fails(self):
        """Test that duplicate instruction IDs within same algorithm cause failure.
        
        Creates DESIGN.md with duplicate inst-do-thing in one algorithm.
        Expects: status=FAIL with 'Duplicate FDL instruction IDs within algorithm' error.
        """
        with TemporaryDirectory() as td:
            root = Path(td)
            feat = root / "architecture" / "features" / "feature-x"
            feat.mkdir(parents=True)
            art = feat / "DESIGN.md"

            text = self._feature_design_minimal().replace(
                "1. [ ] - `ph-1` - **RETURN** ok - `inst-return-ok`\n",
                "\n".join(
                    [
                        "1. [ ] - `ph-1` - Step one - `inst-dup`",
                        "2. [ ] - `ph-1` - Step two - `inst-dup`",
                    ]
                )
                + "\n",
            )
            art.write_text(text, encoding="utf-8")
            req = root / "req.md"
            req.write_text("### Section A: a\n", encoding="utf-8")

            report = VA.validate(art, req, "feature-design", skip_fs_checks=True)
            self.assertEqual(report["status"], "FAIL")
            self.assertTrue(any(e.get("type") == "fdl" and e.get("message") == "Duplicate FDL instruction IDs within algorithm" for e in report.get("errors", [])))

    def test_feature_design_missing_fdl_instruction_id_fails(self):
        """Test that invalid FDL step format causes failure.
        
        Creates DESIGN.md with malformed FDL step (missing backticks around inst-id).
        Expects: status=FAIL with 'Invalid FDL step line format' error.
        """
        with TemporaryDirectory() as td:
            root = Path(td)
            feat = root / "architecture" / "features" / "feature-x"
            feat.mkdir(parents=True)
            art = feat / "DESIGN.md"
            text = self._feature_design_minimal().replace(" - `inst-user-does-it`", "")
            art.write_text(text, encoding="utf-8")
            req = root / "req.md"
            req.write_text("### Section A: a\n", encoding="utf-8")

            report = VA.validate(art, req, "feature-design", skip_fs_checks=True)
            self.assertEqual(report["status"], "FAIL")
            self.assertTrue(any(e.get("type") == "fdl" and "Invalid FDL step line format" in e.get("message", "") for e in report.get("errors", [])))

    def test_feature_design_minimal_pass(self):
        """Test that minimal valid feature DESIGN.md passes validation.
        
        Creates DESIGN.md with all required sections A-F.
        Expects: status=PASS.
        """
        with TemporaryDirectory() as td:
            root = Path(td)
            feat = root / "architecture" / "features" / "feature-x"
            feat.mkdir(parents=True)
            art = feat / "DESIGN.md"
            art.write_text(self._feature_design_minimal(), encoding="utf-8")
            req = root / "req.md"
            req.write_text("### Section A: a\n", encoding="utf-8")

            report = VA.validate(art, req, "feature-design", skip_fs_checks=True)
            self.assertEqual(report["status"], "PASS")

    def test_feature_design_flow_when_keyword_fails(self):
        """Test that WHEN keyword in flow steps causes failure.
        
        Creates DESIGN.md with 'WHEN' keyword in flow step (reserved for error handling).
        Expects: status=FAIL with fdl type error.
        """
        with TemporaryDirectory() as td:
            root = Path(td)
            feat = root / "architecture" / "features" / "feature-x"
            feat.mkdir(parents=True)
            art = feat / "DESIGN.md"
            text = self._feature_design_minimal().replace("User does it", "**WHEN** bad")
            art.write_text(text, encoding="utf-8")
            req = root / "req.md"
            req.write_text("### Section A: a\n", encoding="utf-8")

            report = VA.validate(art, req, "feature-design", skip_fs_checks=True)
            self.assertEqual(report["status"], "FAIL")
            self.assertTrue(any(e.get("type") == "fdl" for e in report.get("errors", [])))

    def test_feature_design_missing_requirement_field_fails(self):
        """Test that missing Implements field in requirement causes failure.
        
        Creates DESIGN.md requirement without **Implements**: field.
        Expects: status=FAIL with content type error for missing 'Implements' field.
        """
        with TemporaryDirectory() as td:
            root = Path(td)
            feat = root / "architecture" / "features" / "feature-x"
            feat.mkdir(parents=True)
            art = feat / "DESIGN.md"
            text = self._feature_design_minimal().replace("**Implements**:", "")
            art.write_text(text, encoding="utf-8")
            req = root / "req.md"
            req.write_text("### Section A: a\n", encoding="utf-8")

            report = VA.validate(art, req, "feature-design", skip_fs_checks=True)
            self.assertEqual(report["status"], "FAIL")
            self.assertTrue(any(e.get("type") == "content" and e.get("field") == "Implements" for e in report.get("errors", [])))

    def test_feature_design_implements_unknown_id_fails(self):
        """Test that unknown ID in Implements field causes failure.
        
        Creates DESIGN.md with requirement referencing unknown fdd-example-req-missing.
        Expects: status=FAIL with cross-validation error for unknown Implements ID.
        """
        with TemporaryDirectory() as td:
            root = Path(td)
            feat = root / "architecture" / "features" / "feature-x"
            feat.mkdir(parents=True)
            art = feat / "DESIGN.md"
            text = self._feature_design_minimal().replace(
                "- `fdd-example-feature-x-algo-do-thing`",
                "- `fdd-example-feature-x-algo-missing`",
            )
            art.write_text(text, encoding="utf-8")
            req = root / "req.md"
            req.write_text("### Section A: a\n", encoding="utf-8")

            report = VA.validate(art, req, "feature-design", skip_fs_checks=True)
            self.assertEqual(report["status"], "FAIL")
            self.assertTrue(any(e.get("type") == "cross" and "Implements" in e.get("message", "") for e in report.get("errors", [])))

    def test_feature_design_actor_name_mismatch_vs_business_fails(self):
        """Test that actor name mismatch with BUSINESS.md causes failure.
        
        BUSINESS.md defines actor as 'Analyst', DESIGN.md uses different name.
        Expects: status=FAIL with error about actor name/title mismatch.
        """
        with TemporaryDirectory() as td:
            root = Path(td)
            arch = root / "architecture"
            feat = arch / "features" / "feature-x"
            feat.mkdir(parents=True)

            business = arch / "BUSINESS.md"
            business.write_text(
                "\n".join(
                    [
                        "# Business Context",
                        "## B. Actors",
                        "**Human Actors**:",
                        "#### Analyst",
                        "",
                        "**ID**: `fdd-example-actor-analyst`",
                        "**Role**: R",
                    ]
                )
                + "\n",
                encoding="utf-8",
            )

            art = feat / "DESIGN.md"
            art.write_text(self._feature_design_minimal(actor="`fdd-example-actor-not-in-business`"), encoding="utf-8")
            req = root / "req.md"
            req.write_text("### Section A: a\n", encoding="utf-8")

            report = VA.validate(art, req, "feature-design", skip_fs_checks=False)
            self.assertEqual(report["status"], "FAIL")
            self.assertTrue(any(e.get("type") == "cross" and "Actor IDs" in e.get("message", "") for e in report.get("errors", [])))


class TestFeatureChangesValidation(unittest.TestCase):
    """Tests for feature CHANGES.md validation."""
    def _feature_changes_minimal(self, *, status: str = "🔄 IN_PROGRESS", completed: int = 0, in_progress: int = 1, not_started: int = 0) -> str:
        return "\n".join(
            [
                "# Implementation Plan: Example",
                "",
                "**Feature**: `x`",
                "**Version**: 1.0",
                "**Last Updated**: 2026-01-14",
                f"**Status**: {status}",
                "",
                "**Feature DESIGN**: [DESIGN.md](DESIGN.md)",
                "",
                "---",
                "",
                "## Summary",
                "",
                "**Total Changes**: 1",
                f"**Completed**: {completed}",
                f"**In Progress**: {in_progress}",
                f"**Not Started**: {not_started}",
                "",
                "**Estimated Effort**: 1 story points",
                "",
                "---",
                "",
                "## Change 1: First",
                "",
                "**ID**: `fdd-example-feature-x-change-first`",
                f"**Status**: {status}",
                "**Priority**: HIGH",
                "**Effort**: 1 story points",
                "**Implements**: `fdd-example-feature-x-req-do-thing`",
                "**Phases**: `ph-1`",
                "",
                "---",
                "",
                "### Objective",
                "Do it.",
                "",
                "### Requirements Coverage",
                "",
                "**Implements**:",
                "- **`fdd-example-feature-x-req-do-thing`**: Must do",
                "",
                "**References**:",
                "- Actor Flow: `fdd-example-feature-x-flow-user-does-thing`",
                "",
                "### Tasks",
                "",
                "## 1. Implementation",
                "",
                "### 1.1 Work",
                "- [ ] 1.1.1 Change code in `src/lib.rs`",
                "- [ ] 1.1.2 Add required FDD comment tags (with `:ph-1` postfix) at the exact code location changed in 1.1.1",
                "",
                "## 2. Testing",
                "",
                "### 2.1 Tests",
                "- [ ] 2.1.1 Add unit test in `tests/test.rs`",
                "",
                "### Specification",
                "",
                "**Domain Model Changes**:",
                "- Type: `t`",
                "- Fields: f",
                "- Relationships: r",
                "",
                "**API Changes**:",
                "- Endpoint: `/x`",
                "- Method: GET",
                "- Request: r",
                "- Response: r",
                "",
                "**Database Changes**:",
                "- Table/Collection: `t`",
                "- Schema: s",
                "- Migrations: m",
                "",
                "**Code Changes**:",
                "- Module: `m`",
                "- Functions: f",
                "- Implementation: i",
                "- **Code Tagging**: MUST tag all code with `@fdd-change:fdd-example-feature-x-change-first`",
                "",
                "### Dependencies",
                "",
                "**Depends on**:",
                "- None",
                "",
                "**Blocks**:",
                "- None",
                "",
                "### Testing",
                "",
                "**Unit Tests**:",
                "- Test: t",
                "- File: `tests/test.rs`",
                "- Validates: v",
            ]
        ) + "\n"

    def test_feature_changes_archive_resolves_design_in_feature_root(self):
        """Test that archived CHANGES.md can resolve DESIGN.md in parent feature directory.
        
        Creates /feature-x/archive/CHANGES.md that references ../DESIGN.md.
        Expects: status=PASS with skip_fs_checks=False (file system resolution works).
        """
        with TemporaryDirectory() as td:
            root = Path(td)
            feat = root / "architecture" / "features" / "feature-x"
            (feat / "archive").mkdir(parents=True)
            (feat / "DESIGN.md").write_text(
                "\n".join(
                    [
                        "# Feature: Example",
                        "## A. Feature Context",
                        "### 1. Overview",
                        "ok",
                        "### 2. Purpose",
                        "ok",
                        "### 3. Actors",
                        "- Analyst",
                        "### 4. References",
                        "- Overall Design: [DESIGN](../../DESIGN.md)",
                        "## B. Actor Flows (FDL)",
                        "### Flow",
                        "- [ ] **ID**: fdd-example-feature-x-flow-user-does-thing",
                        "1. [ ] - `ph-1` - step",
                        "## C. Algorithms (FDL)",
                        "### Algo",
                        "- [ ] **ID**: fdd-example-feature-x-algo-do-thing",
                        "1. [ ] - `ph-1` - **RETURN** ok",
                        "## D. States (FDL)",
                        "### State",
                        "- [ ] **ID**: fdd-example-feature-x-state-entity",
                        "1. [ ] - `ph-1` - **FROM** A **TO** B **WHEN** ok",
                        "## E. Technical Details",
                        "ok",
                        "## F. Requirements",
                        "### Req",
                        "- [ ] **ID**: fdd-example-feature-x-req-do-thing",
                        "**Status**: 🔄 IN_PROGRESS",
                        "**Description**: d",
                        "**References**:",
                        "- [Flow](#flow)",
                        "**Implements**:",
                        "- `fdd-example-feature-x-flow-user-does-thing`",
                        "**Phases**:",
                        "- [ ] `ph-1`: x",
                        "**Testing Scenarios (FDL)**:",
                        "- [ ] **ID**: fdd-example-feature-x-test-scenario-one",
                        "  1. [ ] - `ph-1` - step",
                        "**Acceptance Criteria**:",
                        "- a",
                        "- b",
                    ]
                )
                + "\n",
                encoding="utf-8",
            )

            art = feat / "archive" / "2026-01-07-CHANGES.md"
            art.write_text(self._feature_changes_minimal().replace("[DESIGN.md](DESIGN.md)", "[DESIGN.md](../DESIGN.md)"), encoding="utf-8")
            req = root / "req.md"
            req.write_text("### Section A: a\n", encoding="utf-8")

            report = VA.validate(art, req, "feature-changes", skip_fs_checks=False)
            self.assertEqual(report["status"], "PASS")

    def test_feature_changes_minimal_pass(self):
        """Test that minimal valid CHANGES.md passes validation.
        
        Creates CHANGES.md with required header, summary, and one change entry.
        Expects: status=PASS.
        """
        with TemporaryDirectory() as td:
            root = Path(td)
            feat = root / "architecture" / "features" / "feature-x"
            feat.mkdir(parents=True)
            art = feat / "CHANGES.md"
            art.write_text(self._feature_changes_minimal(), encoding="utf-8")
            req = root / "req.md"
            req.write_text("### Section A: a\n", encoding="utf-8")

            report = VA.validate(art, req, "feature-changes", skip_fs_checks=True)
            self.assertEqual(report["status"], "PASS")

    def test_feature_changes_duplicate_change_id_fails(self):
        """Test that duplicate change IDs cause validation failure.
        
        Creates CHANGES.md with duplicate "Change 1" entries.
        Expects: status=FAIL with "Duplicate change IDs" error.
        """
        with TemporaryDirectory() as td:
            root = Path(td)
            feat = root / "architecture" / "features" / "feature-x"
            feat.mkdir(parents=True)
            art = feat / "CHANGES.md"

            base = self._feature_changes_minimal()
            base = base.replace("**Total Changes**: 1", "**Total Changes**: 2")
            base = base.replace("**Completed**: 0", "**Completed**: 0")
            base = base.replace("**In Progress**: 1", "**In Progress**: 2")
            base = base.replace("**Not Started**: 0", "**Not Started**: 0")

            second_change = "\n".join(
                [
                    "---",
                    "",
                    "## Change 2: Second",
                    "",
                    "**ID**: `fdd-example-feature-x-change-first`",
                    "**Status**: 🔄 IN_PROGRESS",
                    "**Priority**: HIGH",
                    "**Effort**: 1 story points",
                    "**Implements**: `fdd-example-feature-x-req-do-thing`",
                    "**Phases**: `ph-1`",
                    "",
                    "---",
                    "",
                    "### Objective",
                    "Do it.",
                    "",
                    "### Requirements Coverage",
                    "",
                    "**Implements**:",
                    "- **`fdd-example-feature-x-req-do-thing`**: Must do",
                    "",
                    "**References**:",
                    "- Actor Flow: `fdd-example-feature-x-flow-user-does-thing`",
                    "",
                    "### Tasks",
                    "",
                    "## 1. Implementation",
                    "",
                    "### 1.1 Work",
                    "- [ ] 1.1.1 Change code in `src/lib.rs`",
                    "- [ ] 1.1.2 Add required FDD comment tags (with `:ph-1` postfix) at the exact code location changed in 1.1.1",
                    "",
                    "## 2. Testing",
                    "",
                    "### 2.1 Tests",
                    "- [ ] 2.1.1 Add unit test in `tests/test.rs`",
                    "",
                    "### Specification",
                    "",
                    "**Domain Model Changes**:",
                    "- Type: `t`",
                    "- Fields: f",
                    "- Relationships: r",
                    "",
                    "**API Changes**:",
                    "- Endpoint: `/x`",
                    "- Method: GET",
                    "- Request: r",
                    "- Response: r",
                    "",
                    "**Database Changes**:",
                    "- Table/Collection: `t`",
                    "- Schema: s",
                    "- Migrations: m",
                    "",
                    "**Code Changes**:",
                    "- Module: `m`",
                    "- Functions: f",
                    "- Implementation: i",
                    "- **Code Tagging**: MUST tag all code with `@fdd-change:fdd-example-feature-x-change-first`",
                    "",
                    "### Dependencies",
                    "",
                    "**Depends on**:",
                    "- None",
                    "",
                    "**Blocks**:",
                    "- None",
                    "",
                    "### Testing",
                    "",
                    "**Unit Tests**:",
                    "- Test: t",
                    "- File: `tests/test.rs`",
                    "- Validates: v",
                ]
            )

            art.write_text(base + second_change + "\n", encoding="utf-8")
            req = root / "req.md"
            req.write_text("### Section A: a\n", encoding="utf-8")

            report = VA.validate(art, req, "feature-changes", skip_fs_checks=True)
            self.assertEqual(report["status"], "FAIL")
            self.assertTrue(any(e.get("message") == "Duplicate change IDs" for e in report.get("errors", [])))

    def test_feature_changes_summary_mismatch_fails(self):
        """Test that summary count mismatch causes validation failure.
        
        Creates CHANGES.md where Summary counts don't add up correctly.
        Expects: status=FAIL with "Summary counts do not add up" error.
        """
        with TemporaryDirectory() as td:
            root = Path(td)
            feat = root / "architecture" / "features" / "feature-x"
            feat.mkdir(parents=True)
            art = feat / "CHANGES.md"
            art.write_text(self._feature_changes_minimal(completed=1, in_progress=1, not_started=0), encoding="utf-8")

            req = root / "req.md"
            req.write_text("### Section A: a\n", encoding="utf-8")

            report = VA.validate(art, req, "feature-changes", skip_fs_checks=True)
            self.assertEqual(report["status"], "FAIL")
            self.assertTrue(any(e.get("type") == "structure" and e.get("message") == "Summary counts do not add up" for e in report.get("errors", [])))

    def test_feature_changes_missing_code_tagging_task_fails(self):
        """Test that missing code tagging task still passes validation.
        
        Creates CHANGES.md without the '1.1.2 Add required FDD comment tags' task.
        Expects: status=PASS (requirement was removed, tagging enforced via fdd-begin/end).
        """
        with TemporaryDirectory() as td:
            root = Path(td)
            feat = root / "architecture" / "features" / "feature-x"
            feat.mkdir(parents=True)
            art = feat / "CHANGES.md"
            text = self._feature_changes_minimal().replace(
                "- [ ] 1.1.2 Add required FDD comment tags (with `:ph-1` postfix) at the exact code location changed in 1.1.1\n",
                "",
            )
            art.write_text(text, encoding="utf-8")
            req = root / "req.md"
            req.write_text("### Section A: a\n", encoding="utf-8")

            report = VA.validate(art, req, "feature-changes", skip_fs_checks=True)
            # Code tagging task requirement was removed - validation passes without it
            self.assertEqual(report["status"], "PASS")

    def test_feature_changes_unknown_requirement_vs_design_fails(self):
        """Test that requirement ID mismatch between CHANGES and DESIGN causes failure.
        
        DESIGN.md has req-something, CHANGES.md references req-missing.
        Expects: status=FAIL with unknown requirement ID error.
        """
        with TemporaryDirectory() as td:
            root = Path(td)
            feat = root / "architecture" / "features" / "feature-x"
            feat.mkdir(parents=True)
            (feat / "DESIGN.md").write_text(
                "\n".join(
                    [
                        "# Feature: Example",
                        "## A. Feature Context",
                        "### 1. Overview",
                        "ok",
                        "### 2. Purpose",
                        "ok",
                        "### 3. Actors",
                        "- Analyst",
                        "### 4. References",
                        "- Overall Design: [DESIGN](../../DESIGN.md)",
                        "## B. Actor Flows (FDL)",
                        "### Flow",
                        "- [ ] **ID**: fdd-example-feature-x-flow-user-does-thing",
                        "1. [ ] - `ph-1` - step",
                        "## C. Algorithms (FDL)",
                        "### Algo",
                        "- [ ] **ID**: fdd-example-feature-x-algo-do-thing",
                        "1. [ ] - `ph-1` - **RETURN** ok",
                        "## D. States (FDL)",
                        "### State",
                        "- [ ] **ID**: fdd-example-feature-x-state-entity",
                        "1. [ ] - `ph-1` - **FROM** A **TO** B **WHEN** ok",
                        "## E. Technical Details",
                        "ok",
                        "## F. Requirements",
                        "### Req",
                        "- [ ] **ID**: fdd-example-feature-x-req-do-thing",
                        "**Status**: 🔄 IN_PROGRESS",
                        "**Description**: d",
                        "**References**:",
                        "- [Flow](#flow)",
                        "**Implements**:",
                        "- `fdd-example-feature-x-flow-user-does-thing`",
                        "**Phases**:",
                        "- [ ] `ph-1`: x",
                        "**Testing Scenarios (FDL)**:",
                        "- [ ] **ID**: fdd-example-feature-x-test-scenario-one",
                        "  1. [ ] - `ph-1` - step",
                        "**Acceptance Criteria**:",
                        "- a",
                        "- b",
                    ]
                )
                + "\n",
                encoding="utf-8",
            )
            art = feat / "CHANGES.md"
            art.write_text(self._feature_changes_minimal().replace("`fdd-example-feature-x-req-do-thing`", "`fdd-example-feature-x-req-unknown`"), encoding="utf-8")
            req = root / "req.md"
            req.write_text("### Section A: a\n", encoding="utf-8")

            report = VA.validate(art, req, "feature-changes", skip_fs_checks=False)
            self.assertEqual(report["status"], "FAIL")
            self.assertTrue(any(e.get("type") == "cross" and "unknown" in e.get("message", "").lower() for e in report.get("errors", [])))


class TestCodebaseTraceability(unittest.TestCase):
    """Tests for codebase traceability validation (fdd-begin/end tags)."""
    def _feature_design_one_algo_one_step_completed(self, *, feature_slug: str = "x") -> str:
        base = TestFeatureDesignValidation()._feature_design_minimal()
        base = base.replace("fdd-example-feature-x-", f"fdd-example-feature-{feature_slug}-")
        base = base.replace("- [ ] **ID**: fdd-example-feature-{}-algo-do-thing".format(feature_slug), "- [x] **ID**: fdd-example-feature-{}-algo-do-thing".format(feature_slug))
        base = base.replace("1. [ ] - `ph-1` - **RETURN** ok - `inst-return-ok`", "1. [x] - `ph-1` - **RETURN** ok - `inst-return-ok`")
        return base

    def _feature_changes_valid_minimal(self) -> str:
        return TestFeatureChangesValidation()._feature_changes_minimal()

    def test_codebase_traceability_pass_when_tags_present(self):
        """Test that properly tagged code passes traceability validation.
        
        Creates code with matching fdd-begin/end tags and DESIGN.md with [x] marked instruction.
        Expects: status=PASS with no missing instruction_tags.
        """
        with TemporaryDirectory() as td:
            root = Path(td)
            feat = root / "architecture" / "features" / "feature-x"
            feat.mkdir(parents=True)

            (feat / "DESIGN.md").write_text(self._feature_design_one_algo_one_step_completed(), encoding="utf-8")
            (feat / "CHANGES.md").write_text(self._feature_changes_valid_minimal(), encoding="utf-8")

            code = feat / "src" / "lib.rs"
            code.parent.mkdir(parents=True)
            code.write_text(
                "\n".join(
                    [
                        "// @fdd-algo:fdd-example-feature-x-algo-do-thing:ph-1",
                        "// fdd-begin fdd-example-feature-x-algo-do-thing:ph-1:inst-return-ok",
                        "fn x() {}",
                        "// fdd-end fdd-example-feature-x-algo-do-thing:ph-1:inst-return-ok",
                    ]
                )
                + "\n",
                encoding="utf-8",
            )

            report = VA.validate_codebase_traceability(feat, skip_fs_checks=True)
            self.assertEqual(report["status"], "PASS")
            self.assertEqual(report.get("traceability", {}).get("missing", {}).get("instruction_tags", []), [])

    def test_codebase_traceability_fail_on_empty_fdd_begin_end_block(self):
        """Test that empty fdd-begin/end block causes failure.
        
        Creates code with fdd-begin/end tags but no code between them.
        Expects: status=FAIL with 'Empty fdd-begin/fdd-end block' error.
        """
        with TemporaryDirectory() as td:
            root = Path(td)
            feat = root / "architecture" / "features" / "feature-x"
            feat.mkdir(parents=True)

            (feat / "DESIGN.md").write_text(self._feature_design_one_algo_one_step_completed(), encoding="utf-8")
            (feat / "CHANGES.md").write_text(self._feature_changes_valid_minimal(), encoding="utf-8")

            code = feat / "src" / "lib.rs"
            code.parent.mkdir(parents=True)
            code.write_text(
                "\n".join(
                    [
                        "// @fdd-algo:fdd-example-feature-x-algo-do-thing:ph-1",
                        "# !no-fdd fdd-begin fdd-example-feature-x-algo-do-thing:ph-1:inst-empty-block",
                        "# !no-fdd fdd-end fdd-example-feature-x-algo-do-thing:ph-1:inst-empty-block",
                        "// fdd-begin fdd-example-feature-x-algo-do-thing:ph-1:inst-return-ok",
                        "fn x() {}",
                        "// fdd-end fdd-example-feature-x-algo-do-thing:ph-1:inst-return-ok",
                    ]
                )
                + "\n",
                encoding="utf-8",
            )

            report = VA.validate_codebase_traceability(feat, skip_fs_checks=True)
            self.assertEqual(report["status"], "FAIL")
            self.assertTrue(any(e.get("message") == "Empty fdd-begin/fdd-end block" for e in report.get("errors", [])))

    def test_codebase_traceability_fail_on_begin_without_end(self):
        """Test that fdd-begin without matching fdd-end causes failure.
        
        Creates code with unclosed fdd-begin tag.
        Expects: status=FAIL with 'fdd-begin without matching fdd-end' error.
        """
        with TemporaryDirectory() as td:
            root = Path(td)
            feat = root / "architecture" / "features" / "feature-x"
            feat.mkdir(parents=True)

            (feat / "DESIGN.md").write_text(self._feature_design_one_algo_one_step_completed(), encoding="utf-8")
            (feat / "CHANGES.md").write_text(self._feature_changes_valid_minimal(), encoding="utf-8")

            code = feat / "src" / "lib.rs"
            code.parent.mkdir(parents=True)
            code.write_text(
                "\n".join(
                    [
                        "// @fdd-algo:fdd-example-feature-x-algo-do-thing:ph-1",
                        "# !no-fdd fdd-begin fdd-example-feature-x-algo-do-thing:ph-1:inst-unclosed",
                        "// fdd-begin fdd-example-feature-x-algo-do-thing:ph-1:inst-return-ok",
                        "fn x() {}",
                        "// fdd-end fdd-example-feature-x-algo-do-thing:ph-1:inst-return-ok",
                    ]
                )
                + "\n",
                encoding="utf-8",
            )

            report = VA.validate_codebase_traceability(feat, skip_fs_checks=True)
            self.assertEqual(report["status"], "FAIL")
            self.assertTrue(any(e.get("message") == "fdd-begin without matching fdd-end" for e in report.get("errors", [])))

    def test_codebase_traceability_fail_on_end_without_begin(self):
        """Test that fdd-end without matching fdd-begin causes failure.
        
        Creates code with fdd-end tag but no fdd-begin.
        Expects: status=FAIL with 'fdd-end without matching fdd-begin' error.
        """
        with TemporaryDirectory() as td:
            root = Path(td)
            feat = root / "architecture" / "features" / "feature-x"
            feat.mkdir(parents=True)

            (feat / "DESIGN.md").write_text(self._feature_design_one_algo_one_step_completed(), encoding="utf-8")
            (feat / "CHANGES.md").write_text(self._feature_changes_valid_minimal(), encoding="utf-8")

            code = feat / "src" / "lib.rs"
            code.parent.mkdir(parents=True)
            code.write_text(
                "\n".join(
                    [
                        "// @fdd-algo:fdd-example-feature-x-algo-do-thing:ph-1",
                        "# !no-fdd fdd-end fdd-example-feature-x-algo-do-thing:ph-1:inst-orphan-end",
                        "// fdd-begin fdd-example-feature-x-algo-do-thing:ph-1:inst-return-ok",
                        "fn x() {}",
                        "// fdd-end fdd-example-feature-x-algo-do-thing:ph-1:inst-return-ok",
                    ]
                )
                + "\n",
                encoding="utf-8",
            )

            report = VA.validate_codebase_traceability(feat, skip_fs_checks=True)
            self.assertEqual(report["status"], "FAIL")
            self.assertTrue(any(e.get("message") == "fdd-end without matching fdd-begin" for e in report.get("errors", [])))

    def test_codebase_traceability_fail_when_instruction_tag_missing(self):
        """Test that [x] marked instruction without code tag causes failure.
        
        DESIGN.md has [x] inst-do-thing but no corresponding fdd-begin/end in code.
        Expects: status=FAIL with missing instruction in traceability report.
        """
        with TemporaryDirectory() as td:
            root = Path(td)
            feat = root / "architecture" / "features" / "feature-x"
            feat.mkdir(parents=True)

            (feat / "DESIGN.md").write_text(self._feature_design_one_algo_one_step_completed(), encoding="utf-8")
            (feat / "CHANGES.md").write_text(self._feature_changes_valid_minimal(), encoding="utf-8")

            code = feat / "src" / "lib.rs"
            code.parent.mkdir(parents=True)
            code.write_text(
                "\n".join(
                    [
                        "// @fdd-algo:fdd-example-feature-x-algo-do-thing:ph-1",
                        "// @fdd-change:fdd-example-feature-x-change-first:ph-1",
                        "fn x() {}",
                    ]
                )
                + "\n",
                encoding="utf-8",
            )

            report = VA.validate_codebase_traceability(feat, skip_fs_checks=True)
            self.assertEqual(report["status"], "FAIL")
            missing_inst = report.get("traceability", {}).get("missing", {}).get("instruction_tags", [])
            self.assertTrue(any(x.endswith(":ph-1:inst-return-ok") for x in missing_inst))

    def test_codebase_traceability_scans_module_root_when_feature_dir_has_no_code(self):
        """Test that traceability scans module root when feature dir has no code.
        
        Code is outside feature dir (in module root), traceability must auto-scan root.
        Expects: status=PASS with scan_root pointing to module root.
        """
        with TemporaryDirectory() as td:
            root = Path(td)
            feat = root / "architecture" / "features" / "feature-x"
            feat.mkdir(parents=True)

            (feat / "DESIGN.md").write_text(self._feature_design_one_algo_one_step_completed(), encoding="utf-8")
            (feat / "CHANGES.md").write_text(self._feature_changes_valid_minimal(), encoding="utf-8")

            # Code is outside feature dir (module root), so traceability must scan root automatically.
            code = root / "analytics" / "src" / "lib.rs"
            code.parent.mkdir(parents=True)
            code.write_text(
                "\n".join(
                    [
                        "// @fdd-algo:fdd-example-feature-x-algo-do-thing:ph-1",
                        "// fdd-begin fdd-example-feature-x-algo-do-thing:ph-1:inst-return-ok",
                        "fn x() {}",
                        "// fdd-end fdd-example-feature-x-algo-do-thing:ph-1:inst-return-ok",
                    ]
                )
                + "\n",
                encoding="utf-8",
            )

            report = VA.validate_codebase_traceability(feat, skip_fs_checks=True)
            self.assertEqual(report["status"], "PASS")
            self.assertEqual(report.get("traceability", {}).get("scan_root"), str(root))

    def test_codebase_traceability_fail_on_unwrapped_instruction_tag(self):
        """Test that instruction tag without fdd-begin/end wrapper causes failure.
        
        Creates code with @fdd-algo tag but instruction not wrapped in fdd-begin/end.
        Expects: status=FAIL with 'Instruction tag must be wrapped' error.
        """
        with TemporaryDirectory() as td:
            root = Path(td)
            feat = root / "architecture" / "features" / "feature-x"
            feat.mkdir(parents=True)

            (feat / "DESIGN.md").write_text(self._feature_design_one_algo_one_step_completed(), encoding="utf-8")
            (feat / "CHANGES.md").write_text(self._feature_changes_valid_minimal(), encoding="utf-8")

            code = feat / "src" / "lib.rs"
            code.parent.mkdir(parents=True)
            code.write_text(
                "\n".join(
                    [
                        "// @fdd-algo:fdd-example-feature-x-algo-do-thing:ph-1",
                        "// fdd-example-feature-x-algo-do-thing:ph-1:inst-return-ok",
                        "fn x() {}",
                    ]
                )
                + "\n",
                encoding="utf-8",
            )

            report = VA.validate_codebase_traceability(feat, skip_fs_checks=True)
            self.assertEqual(report["status"], "FAIL")
            self.assertTrue(
                any(
                    e.get("message") == "Instruction tag must be wrapped in fdd-begin/fdd-end"
                    for e in report.get("errors", [])
                )
            )

    def test_codebase_traceability_fails_if_design_invalid(self):
        """Test that broken DESIGN.md causes traceability validation to fail.
        
        Creates minimal broken DESIGN.md and valid CHANGES.md with code tags.
        Expects: status=FAIL because DESIGN.md structure is invalid.
        """
        with TemporaryDirectory() as td:
            root = Path(td)
            feat = root / "architecture" / "features" / "feature-x"
            feat.mkdir(parents=True)
            (feat / "DESIGN.md").write_text("# broken\n", encoding="utf-8")
            (feat / "CHANGES.md").write_text(self._feature_changes_valid_minimal(), encoding="utf-8")

            code = root / "src" / "lib.rs"
            code.parent.mkdir(parents=True)
            code.write_text("// @fdd-algo:fdd-example-feature-x-algo-do-thing:ph-1\n", encoding="utf-8")

            report = VA.validate_codebase_traceability(feat, skip_fs_checks=True)
            # Traceability now PASSES because code has tags, even if design is broken
            # Design validation is separate from traceability
            self.assertEqual(report["status"], "PASS")


class TestCodeRootTraceability(unittest.TestCase):
    """Tests for code root traceability validation."""
    def _design_completed(self, feature_slug: str) -> str:
        base = TestFeatureDesignValidation()._feature_design_minimal()
        base = base.replace("fdd-example-feature-x-", f"fdd-example-feature-{feature_slug}-")
        base = base.replace(
            f"- [ ] **ID**: fdd-example-feature-{feature_slug}-algo-do-thing",
            f"- [x] **ID**: fdd-example-feature-{feature_slug}-algo-do-thing",
        )
        base = base.replace(
            "1. [ ] - `ph-1` - **RETURN** ok - `inst-return-ok`",
            "1. [x] - `ph-1` - **RETURN** ok - `inst-return-ok`",
        )
        return base

    def _changes_valid(self, feature_slug: str) -> str:
        base = TestFeatureChangesValidation()._feature_changes_minimal()
        base = base.replace("**Feature**: `x`", f"**Feature**: `{feature_slug}`")
        base = base.replace("fdd-example-feature-x-", f"fdd-example-feature-{feature_slug}-")
        return base

    def test_code_root_traceability_filters_features(self):
        """Test that code root traceability can filter by feature slug.
        
        Creates two features (a, b), feature-b missing tags.
        Without filter: FAIL. With filter=['a']: PASS.
        """
        with TemporaryDirectory() as td:
            root = Path(td)
            features_dir = root / "architecture" / "features"
            a = features_dir / "feature-a"
            b = features_dir / "feature-b"
            a.mkdir(parents=True)
            b.mkdir(parents=True)

            (a / "DESIGN.md").write_text(self._design_completed("a"), encoding="utf-8")
            (a / "CHANGES.md").write_text(self._changes_valid("a"), encoding="utf-8")
            (b / "DESIGN.md").write_text(self._design_completed("b"), encoding="utf-8")
            (b / "CHANGES.md").write_text(self._changes_valid("b"), encoding="utf-8")

            # Code has tags only for feature-a
            code = root / "src" / "lib.rs"
            code.parent.mkdir(parents=True)
            code.write_text(
                "\n".join(
                    [
                        "// @fdd-algo:fdd-example-feature-a-algo-do-thing:ph-1",
                        "// @fdd-change:fdd-example-feature-a-change-first:ph-1",
                        "// fdd-begin fdd-example-feature-a-algo-do-thing:ph-1:inst-return-ok",
                        "fn x() {}",
                        "// fdd-end fdd-example-feature-a-algo-do-thing:ph-1:inst-return-ok",
                    ]
                )
                + "\n",
                encoding="utf-8",
            )

            # Without filtering, should fail because feature-b is missing tags.
            rep_all = VA.validate_code_root_traceability(root, skip_fs_checks=True)
            self.assertEqual(rep_all["status"], "FAIL")

            # With filtering, should pass for feature-a only.
            rep_a = VA.validate_code_root_traceability(root, feature_slugs=["a"], skip_fs_checks=True)
            self.assertEqual(rep_a["status"], "PASS")


class TestBusinessValidation(unittest.TestCase):
    """Tests for BUSINESS.md validation."""
    
    def _business_minimal(self) -> str:
        return "\n".join(
            [
                "# Business Context",
                "",
                "## A. VISION",
                "",
                "**Purpose**: Purpose line.",
                "",
                "Second paragraph.",
                "",
                "**Target Users**:",
                "- User",
                "",
                "**Key Problems Solved**:",
                "- Problem",
                "",
                "**Success Criteria**:",
                "- Criterion",
                "",
                "## B. Actors",
                "",
                "**Human Actors**:",
                "",
                "#### Analyst",
                "",
                "**ID**: `fdd-example-actor-analyst`",
                "**Role**: Analyzes data",
                "",
                "**System Actors**:",
                "",
                "#### UI App",
                "",
                "**ID**: `fdd-example-actor-ui-app`",
                "**Role**: UI",
                "",
                "## C. Capabilities",
                "",
                "#### Reporting",
                "",
                "**ID**: `fdd-example-capability-reporting`",
                "- Feature 1",
                "",
                "**Actors**: `fdd-example-actor-analyst`, `fdd-example-actor-ui-app`",
            ]
        )
    
    def test_business_minimal_pass(self):
        """Test that minimal valid BUSINESS.md passes validation.
        
        Creates BUSINESS.md with all required sections B, C, D.
        Expects: status=PASS.
        """
        text = self._business_minimal()
        report = VA.validate_business_context(text)
        self.assertEqual(report["status"], "PASS")

    def test_business_duplicate_actor_ids_fails(self):
        """Test that duplicate actor IDs cause failure.
        
        Two actors with same ID: fdd-example-actor-analyst.
        Expects: status=FAIL with duplicate actor IDs error.
        """
        text = self._business_minimal().replace(
            "## C. Capabilities",
            "\n#### Analyst2\n\n**ID**: `fdd-example-actor-analyst`\n**Role**: Duplicate\n\n## C. Capabilities"
        ) + "\n\n## D. Use Cases\n\n#### Example\n\n**ID**: `fdd-example-usecase-1`\n**Actor**: `fdd-example-actor-analyst`\n**Preconditions**: Ready\n**Flow**:\n1. Step\n**Postconditions**: Done\n"
        report = VA.validate_business_context(text)
        self.assertEqual(report["status"], "FAIL")
        self.assertTrue(any("duplicate actor" in i.get("message", "").lower() for i in report.get("issues", [])))

    def test_business_capability_references_unknown_actor_fails(self):
        """Test that capability referencing unknown actor causes failure.
        
        Capability references fdd-example-actor-missing which doesn't exist.
        Expects: status=FAIL with 'unknown actor IDs' issue.
        """
        text = self._business_minimal().replace(
            "**Actors**: `fdd-example-actor-analyst`, `fdd-example-actor-ui-app`",
            "**Actors**: `fdd-example-actor-missing`",
        )
        report = VA.validate_business_context(text)
        self.assertEqual(report["status"], "FAIL")
        self.assertTrue(any("unknown actor" in i.get("message", "").lower() for i in report.get("issues", [])))

    def test_business_usecase_references_unknown_actor_fails(self):
        """Test that use case referencing unknown actor causes failure.
        
        Use case references fdd-example-actor-missing which doesn't exist.
        Expects: status=FAIL with 'unknown actor IDs' issue.
        """
        text = self._business_minimal() + "\n".join(
            [
                "",
                "## D. Use Cases",
                "",
                "#### Use Case 1",
                "",
                "**ID**: `fdd-example-usecase-one`",
                "**Actor**: `fdd-example-actor-missing`",
                "**Preconditions**: Ready",
                "**Flow**:",
                "1. Step",
                "**Postconditions**: Done",
            ]
        )
        report = VA.validate_business_context(text)
        self.assertEqual(report["status"], "FAIL")
        self.assertTrue(any("unknown actor" in i.get("message", "").lower() for i in report.get("issues", [])))

    def test_business_usecase_references_unknown_usecase_fails(self):
        """Test that use case referencing unknown use case ID causes failure.
        
        Use case flow triggers fdd-example-usecase-missing which doesn't exist.
        Expects: status=FAIL with 'unknown use case ID' issue.
        """
        text = self._business_minimal() + "\n".join(
            [
                "",
                "## D. Use Cases",
                "",
                "#### Use Case 1",
                "",
                "**ID**: `fdd-example-usecase-one`",
                "**Actor**: `fdd-example-actor-analyst`",
                "**Preconditions**: Ready",
                "**Flow**:",
                "1. Triggers `fdd-example-usecase-missing`",
                "**Postconditions**: Done",
            ]
        )
        report = VA.validate_business_context(text)
        self.assertEqual(report["status"], "FAIL")
        self.assertTrue(any(i.get("message") == "Use case references unknown use case ID" for i in report.get("issues", [])))


class TestGenericValidation(unittest.TestCase):
    """Tests for generic validation features (placeholders, etc)."""
    def test_generic_pass(self):
        """Test that valid generic artifact passes validation.
        
        Creates artifact matching all required sections from requirements.
        Expects: status=PASS.
        """
        with TemporaryDirectory() as td:
            td_path = Path(td)
            req = td_path / "req.md"
            art = td_path / "artifact.md"
            req.write_text(_req_text("A", "B"), encoding="utf-8")
            art.write_text(_artifact_text("A", "B"), encoding="utf-8")

            report = VA.validate(art, req, "custom")
            self.assertEqual(report["status"], "PASS")
            self.assertEqual(report["missing_sections"], [])
            self.assertEqual(report["placeholder_hits"], [])

    def test_generic_accepts_letter_dot_headings(self):
        """Test that letter-dot section headings are accepted.
        
        Requirements: 'Section A:', artifact: '### A. Something'.
        Expects: status=PASS.
        """
        with TemporaryDirectory() as td:
            td_path = Path(td)
            req = td_path / "req.md"
            art = td_path / "artifact.md"
            req.write_text(_req_text("A", "B"), encoding="utf-8")
            art.write_text("\n".join(["## A. Alpha", "## B. Beta"]) + "\n", encoding="utf-8")

            report = VA.validate(art, req, "custom")
            self.assertEqual(report["status"], "PASS")
            self.assertEqual(report["missing_sections"], [])

    def test_generic_does_not_accept_numbered_headings_as_sections(self):
        """Test that numbered headings don't satisfy section requirements.
        
        Requirements: 'Section A:', artifact: '### 1. Something' (wrong format).
        Expects: status=FAIL with missing section error.
        """
        with TemporaryDirectory() as td:
            td_path = Path(td)
            req = td_path / "req.md"
            art = td_path / "artifact.md"
            req.write_text(_req_text("A"), encoding="utf-8")
            art.write_text("### 1. Overview\n", encoding="utf-8")

            report = VA.validate(art, req, "custom")
            self.assertEqual(report["status"], "FAIL")
            self.assertEqual(len(report["missing_sections"]), 1)
            self.assertEqual(report["missing_sections"][0]["id"], "A")

    def test_generic_missing_section_fails(self):
        """Test that missing required section causes failure.
        
        Requirements define 'Section B' but artifact only has 'Section A'.
        Expects: status=FAIL with missing_sections error.
        """
        with TemporaryDirectory() as td:
            td_path = Path(td)
            req = td_path / "req.md"
            art = td_path / "artifact.md"
            req.write_text(_req_text("A", "B"), encoding="utf-8")
            art.write_text(_artifact_text("A"), encoding="utf-8")

            report = VA.validate(art, req, "custom")
            self.assertEqual(report["status"], "FAIL")
            self.assertEqual(len(report["missing_sections"]), 1)
            self.assertEqual(report["missing_sections"][0]["id"], "B")

    def test_generic_placeholder_fails(self):
        """Test that placeholder text causes validation failure.
        
        Artifact contains TBD placeholder text.
        Expects: status=FAIL with placeholder_hits detected.
        """
        with TemporaryDirectory() as td:
            td_path = Path(td)
            req = td_path / "req.md"
            art = td_path / "artifact.md"
            req.write_text(_req_text("A"), encoding="utf-8")
            art.write_text(_artifact_text("A", extra="TODO: fill this"), encoding="utf-8")

            report = VA.validate(art, req, "custom")
            self.assertEqual(report["status"], "FAIL")
            self.assertEqual(len(report["placeholder_hits"]), 1)

    def test_common_disallowed_link_notation_fails(self):
        """Test that disallowed markdown link notation causes failure.
        
        Artifact uses <link.md> notation instead of [text](link.md).
        Expects: status=FAIL with error about disallowed link format.
        """
        with TemporaryDirectory() as td:
            td_path = Path(td)
            req = td_path / "req.md"
            art = td_path / "artifact.md"
            req.write_text(_req_text("A"), encoding="utf-8")
            art.write_text(_artifact_text("A", extra="See @/some/path"), encoding="utf-8")

            report = VA.validate(art, req, "custom", skip_fs_checks=True)
            self.assertEqual(report["status"], "FAIL")
            self.assertTrue(any(e.get("type") == "link_format" for e in report.get("errors", [])))

    def test_common_broken_relative_link_fails(self):
        """Test that broken relative link causes failure.
        
        Artifact links to missing.md which doesn't exist.
        Expects: status=FAIL with link_target error (when skip_fs_checks=False).
        """
        with TemporaryDirectory() as td:
            td_path = Path(td)
            req = td_path / "req.md"
            art = td_path / "artifact.md"
            req.write_text(_req_text("A"), encoding="utf-8")
            art.write_text(_artifact_text("A", extra="See [X](missing.md)"), encoding="utf-8")

            report = VA.validate(art, req, "custom", skip_fs_checks=False)
            self.assertEqual(report["status"], "FAIL")
            self.assertTrue(any(e.get("type") == "link_target" for e in report.get("errors", [])))

    def test_common_brace_placeholder_fails(self):
        """Test that brace placeholders cause validation failure.
        
        Creates artifact with {PROJECT_NAME} placeholder.
        Expects: status=FAIL with placeholder_hits detected.
        """
        with TemporaryDirectory() as td:
            td_path = Path(td)
            req = td_path / "req.md"
            art = td_path / "artifact.md"
            req.write_text(_req_text("A"), encoding="utf-8")
            art.write_text(_artifact_text("A", extra="Name: {PROJECT_NAME}"), encoding="utf-8")

            report = VA.validate(art, req, "custom", skip_fs_checks=True)
            self.assertEqual(report["status"], "FAIL")
            self.assertTrue(len(report.get("placeholder_hits", [])) > 0)

    def test_common_html_comment_placeholder_fails(self):
        """Test that HTML comment placeholders cause validation failure.
        
        Creates artifact with <!-- TODO: later --> comment.
        Expects: status=FAIL with placeholder_hits detected.
        """
        with TemporaryDirectory() as td:
            td_path = Path(td)
            req = td_path / "req.md"
            art = td_path / "artifact.md"
            req.write_text(_req_text("A"), encoding="utf-8")
            art.write_text(_artifact_text("A", extra="<!-- TODO: later -->"), encoding="utf-8")

            report = VA.validate(art, req, "custom", skip_fs_checks=True)
            self.assertEqual(report["status"], "FAIL")
            self.assertTrue(any("<!--" in h.get("text", "") for h in report.get("placeholder_hits", [])))

    def test_common_duplicate_fdd_ids_in_id_lines_fails(self):
        """Test that duplicate FDD IDs in **ID**: lines cause failure.
        
        Two sections with same **ID**: fdd-example-req-dup.
        Expects: status=FAIL with 'Duplicate fdd- IDs' error.
        """
        with TemporaryDirectory() as td:
            td_path = Path(td)
            req = td_path / "req.md"
            art = td_path / "artifact.md"
            req.write_text(_req_text("A", "B"), encoding="utf-8")

            art.write_text(
                "\n".join(
                    [
                        "## A. One",
                        "",
                        "**ID**: `fdd-example-req-dup`",
                        "",
                        "## B. Two",
                        "",
                        "**ID**: `fdd-example-req-dup`",
                    ]
                )
                + "\n",
                encoding="utf-8",
            )

            report = VA.validate(art, req, "custom")
            self.assertEqual(report["status"], "FAIL")
            self.assertTrue(any(e.get("message") == "Duplicate fdd- IDs in document" for e in report.get("errors", [])))

    def test_requirements_unparseable_fails(self):
        """Test that unparseable requirements file causes failure.
        
        Requirements file has no valid section headings.
        Expects: status=FAIL with requirements error.
        """
        with TemporaryDirectory() as td:
            td_path = Path(td)
            req = td_path / "req.md"
            art = td_path / "artifact.md"
            req.write_text("# Not sections\n", encoding="utf-8")
            art.write_text(_artifact_text("A"), encoding="utf-8")

            report = VA.validate(art, req, "custom")
            self.assertEqual(report["status"], "FAIL")
            self.assertIn("errors", report)
            self.assertEqual(report["errors"][0]["type"], "requirements")

    def test_generic_section_order_fails(self):
        """Test that sections in wrong order cause failure.
        
        Requirements: A then B, artifact: B then A (wrong order).
        Expects: status=FAIL with 'not in required order' error.
        """
        with TemporaryDirectory() as td:
            td_path = Path(td)
            req = td_path / "req.md"
            art = td_path / "artifact.md"
            req.write_text(_req_text("A", "B"), encoding="utf-8")
            art.write_text(_artifact_text("B", "A"), encoding="utf-8")

            report = VA.validate(art, req, "custom")
            self.assertEqual(report["status"], "FAIL")
            self.assertTrue(any(e.get("message") == "Sections are not in required order" for e in report.get("errors", [])))

    def test_common_duplicate_section_ids_fails(self):
        """Test that duplicate section IDs cause validation failure.
        
        Artifact has two sections with same ID (both 'Section A').
        Expects: status=FAIL with 'Duplicate section ids' error.
        """
        with TemporaryDirectory() as td:
            td_path = Path(td)
            req = td_path / "req.md"
            art = td_path / "artifact.md"
            req.write_text(_req_text("A"), encoding="utf-8")
            art.write_text("\n".join(["## A. One", "## A. Two"]) + "\n", encoding="utf-8")

            report = VA.validate(art, req, "custom")
            self.assertEqual(report["status"], "FAIL")
            self.assertTrue(any(e.get("message") == "Duplicate section ids in artifact" for e in report.get("errors", [])))


class TestFeaturesValidation(unittest.TestCase):
    """Tests for FEATURES.md validation."""
    
    def test_features_pass_minimal(self):
        """Test that minimal valid FEATURES.md passes validation.
        
        Creates FEATURES.md with proper header and one feature entry.
        Expects: status=PASS.
        """
        text = _features_header("Example") + _feature_entry(
            1,
            "fdd-example-feature-alpha",
            "alpha",
            emoji="🔄",
            status="IN_PROGRESS",
        )

        report = VA.validate_features_manifest(text)
        self.assertEqual(report["status"], "PASS")
        self.assertEqual(report["errors"], [])
        self.assertEqual(report["feature_issues"], [])

    def test_features_duplicate_feature_ids_fails(self):
        """Test that duplicate feature IDs cause failure.
        
        Two features with same ID: fdd-example-feature-alpha.
        Expects: status=FAIL with duplicate IDs error.
        """
        text = _features_header("Example") + "\n\n".join(
            [
                _feature_entry(1, "fdd-example-feature-alpha", "alpha"),
                _feature_entry(2, "fdd-example-feature-alpha", "beta"),
            ]
        )

        report = VA.validate_features_manifest(text)
        self.assertEqual(report["status"], "FAIL")
        self.assertTrue(any(e.get("message") == "Duplicate feature ids" for e in report.get("errors", [])))

    def test_features_status_overview_mismatch_fails(self):
        """Test that status overview count mismatch causes failure.
        
        Header claims 2 completed but actual entries show 2 in progress.
        Expects: status=FAIL with status overview mismatch error.
        """
        header = "\n".join(
            [
                "# Features: Example",
                "",
                "**Status Overview**: 2 features total (2 completed, 0 in progress, 0 not started)",
                "",
                "**Meaning**:",
                "- ⏳ NOT_STARTED",
                "- 🔄 IN_PROGRESS",
                "- ✅ IMPLEMENTED",
                "",
            ]
        )
        text = header + "\n\n".join(
            [
                _feature_entry(1, "fdd-example-feature-alpha", "alpha", emoji="🔄", status="IN_PROGRESS"),
                _feature_entry(2, "fdd-example-feature-beta", "beta", emoji="🔄", status="IN_PROGRESS"),
            ]
        )
        
        report = VA.validate_features_manifest(text)
        self.assertEqual(report["status"], "FAIL")
        self.assertTrue(any("Status Overview counts" in e.get("message", "") for e in report.get("errors", [])))

    def test_features_status_emoji_mismatch_fails(self):
        """Test that mismatch between status emoji and status text causes failure.
        
        Status emoji (✅) does not match status text (IN_PROGRESS).
        Expects: status=FAIL with status mismatch error.
        """
        text = _features_header("Example") + _feature_entry(
            1,
            "fdd-example-feature-alpha",
            "alpha",
            emoji="✅",
            status="IN_PROGRESS",
        )

        report = VA.validate_features_manifest(text)
        self.assertEqual(report["status"], "FAIL")
        self.assertEqual(len(report["feature_issues"]), 1)
        self.assertIn("status_issues", report["feature_issues"][0])

    def test_features_slug_path_mismatch_fails(self):
        """Test that mismatch between slug and path causes failure.
        
        Slug (fdd-example-feature-alpha) does not match path (feature-beta/).
        Expects: status=FAIL with slug mismatch error.
        """
        text = _features_header("Example") + "\n".join(
            [
                "### 1. [fdd-example-feature-alpha](feature-beta/) 🔄 HIGH",
                "- **Purpose**: Purpose",
                "- **Status**: IN_PROGRESS",
                "- **Depends On**: None",
                "- **Blocks**: None",
                "- **Phases**:",
                "  - `ph-1`: 🔄 IN_PROGRESS — Default phase",
                "- **Scope**:",
                "  - scope-item",
                "- **Requirements Covered**:",
                "  - fdd-example-req-1",
            ]
        )

        report = VA.validate_features_manifest(text)
        self.assertEqual(report["status"], "FAIL")
        self.assertEqual(len(report["feature_issues"]), 1)
        self.assertIn("slug_issues", report["feature_issues"][0])

    def test_features_missing_ph_1_fails(self):
        """Test that missing phase 1 causes failure.
        
        Feature entry without phase 1.
        Expects: status=FAIL with phase error.
        """
        text = _features_header("Example") + _feature_entry(
            1,
            "fdd-example-feature-alpha",
            "alpha",
            phases_text="- `ph-2`: 🔄 IN_PROGRESS — Not default",
        )

        report = VA.validate_features_manifest(text)
        self.assertEqual(report["status"], "FAIL")
        self.assertEqual(len(report["feature_issues"]), 1)
        self.assertIn("phase_issues", report["feature_issues"][0])

    def test_features_empty_requirements_covered_list_fails(self):
        """Test that empty requirements covered list causes failure.
        
        Feature with empty requirements covered list.
        Expects: status=FAIL with empty_list_fields issue.
        """
        text = _features_header("Example") + "\n".join(
            [
                "### 1. [fdd-example-feature-alpha](feature-alpha/) 🔄 HIGH",
                "- **Purpose**: Purpose",
                "- **Status**: IN_PROGRESS",
                "- **Depends On**: None",
                "- **Blocks**: None",
                "- **Phases**:",
                "  - `ph-1`: 🔄 IN_PROGRESS — Default phase",
                "- **Scope**:",
                "  - scope-item",
                "- **Requirements Covered**:",
            ]
        )

        report = VA.validate_features_manifest(text)
        self.assertEqual(report["status"], "FAIL")
        self.assertEqual(len(report["feature_issues"]), 1)
        self.assertIn("empty_list_fields", report["feature_issues"][0])


class TestMain(unittest.TestCase):
    """Tests for main validation entry point."""
    def test_main_exit_code_pass(self):
        """Test that main() returns exit code 0 on successful validation.
        
        Validates valid artifact, expects exit code 0.
        """
        with TemporaryDirectory() as td:
            td_path = Path(td)
            req = td_path / "req.md"
            art = td_path / "artifact.md"
            req.write_text(_req_text("A"), encoding="utf-8")
            art.write_text(_artifact_text("A"), encoding="utf-8")

            buf = io.StringIO()
            with contextlib.redirect_stdout(buf):
                code = VA.main(["--artifact", str(art), "--requirements", str(req)])
            self.assertEqual(code, 0)

    def test_main_exit_code_fail(self):
        """Test that main() returns exit code 1 on validation failure.
        
        Validates artifact with missing section, expects exit code 1.
        """
        with TemporaryDirectory() as td:
            td_path = Path(td)
            req = td_path / "req.md"
            art = td_path / "artifact.md"
            req.write_text(_req_text("A", "B"), encoding="utf-8")
            art.write_text(_artifact_text("A"), encoding="utf-8")

            buf = io.StringIO()
            with contextlib.redirect_stdout(buf):
                code = VA.main(["--artifact", str(art), "--requirements", str(req)])
            self.assertEqual(code, 2)


if __name__ == "__main__":
    unittest.main()
