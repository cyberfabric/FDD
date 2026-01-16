import importlib.util
import io
import contextlib
import unittest
from pathlib import Path
from tempfile import TemporaryDirectory


def _load_validate_artifact_module():
    tests_dir = Path(__file__).resolve().parent
    skill_dir = tests_dir.parent
    script_path = skill_dir / "scripts" / "validate_artifact.py"

    spec = importlib.util.spec_from_file_location("validate_artifact", str(script_path))
    if spec is None or spec.loader is None:
        raise RuntimeError("Failed to create import spec for validate_artifact.py")

    mod = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(mod)
    return mod


VA = _load_validate_artifact_module()


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
    def test_detect_requirements_overall_design(self):
        kind, req_path = VA.detect_requirements(Path("/tmp/architecture/DESIGN.md"))
        self.assertEqual(kind, "overall-design")
        self.assertTrue(str(req_path).endswith("/FDD/requirements/overall-design-structure.md"))

    def test_detect_requirements_feature_design(self):
        kind, req_path = VA.detect_requirements(Path("/tmp/architecture/features/feature-x/DESIGN.md"))
        self.assertEqual(kind, "feature-design")
        self.assertTrue(str(req_path).endswith("/FDD/requirements/feature-design-structure.md"))

    def test_detect_requirements_archived_feature_changes(self):
        kind, req_path = VA.detect_requirements(Path("/tmp/architecture/features/feature-x/archive/2026-01-08-CHANGES.md"))
        self.assertEqual(kind, "feature-changes")
        self.assertTrue(str(req_path).endswith("/FDD/requirements/feature-changes-structure.md"))


class TestFeatureDesignValidation(unittest.TestCase):
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

    def test_feature_changes_duplicate_change_ids_fail(self):
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
            self.assertEqual(report["status"], "FAIL")
            self.assertTrue(any(e.get("type") == "content" and "Code tagging" in e.get("message", "") for e in report.get("errors", [])))

    def test_feature_changes_unknown_requirement_vs_design_fails(self):
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
    def _feature_design_one_algo_one_step_completed(self, *, feature_slug: str = "x") -> str:
        base = TestFeatureDesignValidation()._feature_design_minimal()
        base = base.replace("fdd-example-feature-x-", f"fdd-example-feature-{feature_slug}-")
        base = base.replace("- [ ] **ID**: fdd-example-feature-{}-algo-do-thing".format(feature_slug), "- [x] **ID**: fdd-example-feature-{}-algo-do-thing".format(feature_slug))
        base = base.replace("1. [ ] - `ph-1` - **RETURN** ok - `inst-return-ok`", "1. [x] - `ph-1` - **RETURN** ok - `inst-return-ok`")
        return base

    def _feature_changes_valid_minimal(self) -> str:
        return TestFeatureChangesValidation()._feature_changes_minimal()

    def test_codebase_traceability_pass_when_tags_present(self):
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
                        "// fdd-begin fdd-example-feature-x-algo-do-thing:ph-1:inst-empty-block",
                        "// fdd-end fdd-example-feature-x-algo-do-thing:ph-1:inst-empty-block",
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
                        "// fdd-begin fdd-example-feature-x-algo-do-thing:ph-1:inst-unclosed",
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
                        "// fdd-end fdd-example-feature-x-algo-do-thing:ph-1:inst-orphan-end",
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
            self.assertEqual(report["status"], "FAIL")
            tv = report.get("traceability", {}).get("artifact_validation", {})
            self.assertEqual(tv.get("feature_design", {}).get("status"), "FAIL")


class TestCodeRootTraceability(unittest.TestCase):
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


class TestGenericValidation(unittest.TestCase):
    def test_generic_pass(self):
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
        with TemporaryDirectory() as td:
            td_path = Path(td)
            req = td_path / "req.md"
            art = td_path / "artifact.md"
            req.write_text(_req_text("A"), encoding="utf-8")
            art.write_text(_artifact_text("A", extra="Name: {PROJECT_NAME}"), encoding="utf-8")

            report = VA.validate(art, req, "custom", skip_fs_checks=True)
            self.assertEqual(report["status"], "FAIL")
            self.assertTrue(any("PROJECT_NAME" in h.get("text", "") for h in report.get("placeholder_hits", [])))

    def test_common_html_comment_placeholder_fails(self):
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
        with TemporaryDirectory() as td:
            td_path = Path(td)
            req = td_path / "req.md"
            art = td_path / "artifact.md"
            req.write_text(_req_text("A", "B"), encoding="utf-8")
            art.write_text(_artifact_text("B", "A"), encoding="utf-8")

            report = VA.validate(art, req, "custom")
            self.assertEqual(report["status"], "FAIL")
            self.assertTrue(any(e.get("message") == "Sections are not in required order" for e in report.get("errors", [])))

    def test_generic_duplicate_section_ids_fails(self):
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
    def test_features_pass_minimal(self):
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

    def test_features_status_overview_mismatch_fails(self):
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
        self.assertTrue(any(e.get("message") == "Status Overview counts do not match feature entries" for e in report.get("errors", [])))

    def test_features_duplicate_id_fails(self):
        text = _features_header("Example") + "\n\n".join(
            [
                _feature_entry(1, "fdd-example-feature-alpha", "alpha"),
                _feature_entry(2, "fdd-example-feature-alpha", "beta"),
            ]
        )

        report = VA.validate_features_manifest(text)
        self.assertEqual(report["status"], "FAIL")
        self.assertTrue(any(e.get("message") == "Duplicate feature ids" for e in report.get("errors", [])))

    def test_features_dependency_missing_entry_fails(self):
        text = _features_header("Example") + "\n".join(
            [
                "### 1. [fdd-example-feature-alpha](feature-alpha/) 🔄 HIGH",
                "- **Purpose**: Purpose",
                "- **Status**: IN_PROGRESS",
                "- **Depends On**:",
                "  - [feature-missing](feature-missing/)",
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
        self.assertIn("dependency_issues", report["feature_issues"][0])

    def test_features_dir_existence_check(self):
        with TemporaryDirectory() as td:
            td_path = Path(td)
            features_dir = td_path / "architecture" / "features"
            features_dir.mkdir(parents=True)
            artifact_path = features_dir / "FEATURES.md"

            text = _features_header("Example") + _feature_entry(1, "fdd-example-feature-alpha", "alpha")
            artifact_path.write_text(text, encoding="utf-8")

            report = VA.validate_features_manifest(text, artifact_path=artifact_path, skip_fs_checks=False)
            self.assertEqual(report["status"], "FAIL")
            self.assertEqual(len(report["feature_issues"]), 1)
            self.assertIn("dir_issues", report["feature_issues"][0])

    def test_features_design_cross_check(self):
        with TemporaryDirectory() as td:
            td_path = Path(td)
            arch_dir = td_path / "architecture"
            features_dir = arch_dir / "features"
            features_dir.mkdir(parents=True)
            (features_dir / "feature-alpha").mkdir(parents=True)
            artifact_path = features_dir / "FEATURES.md"

            design_path = arch_dir / "DESIGN.md"
            design_path.write_text("## B. Requirements\n- fdd-example-req-other\n", encoding="utf-8")

            text = _features_header("Example") + _feature_entry(1, "fdd-example-feature-alpha", "alpha")
            artifact_path.write_text(text, encoding="utf-8")

            report = VA.validate_features_manifest(text, artifact_path=artifact_path, design_path=design_path, skip_fs_checks=False)
            self.assertEqual(report["status"], "FAIL")
            self.assertEqual(len(report["feature_issues"]), 1)
            self.assertIn("cross_issues", report["feature_issues"][0])

    def test_features_missing_title_fails(self):
        text = "# Something else\n" + _features_header("Example").split("\n", 1)[1] + _feature_entry(
            1,
            "fdd-example-feature-alpha",
            "alpha",
        )

        report = VA.validate_features_manifest(text)
        self.assertEqual(report["status"], "FAIL")
        self.assertTrue(any(e["type"] == "header" for e in report["errors"]))


class TestBusinessValidation(unittest.TestCase):
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

    def test_business_pass_minimal(self):
        report = VA.validate_business_context(self._business_minimal())
        self.assertEqual(report["status"], "PASS")
        self.assertEqual(report["errors"], [])
        self.assertEqual(report["issues"], [])

    def test_business_actor_missing_role_fails(self):
        text = self._business_minimal().replace("**Role**: Analyzes data", "")
        report = VA.validate_business_context(text)
        self.assertEqual(report["status"], "FAIL")
        self.assertTrue(any(i.get("message") == "Missing **Role** line" for i in report.get("issues", [])))

    def test_business_capability_unknown_actor_fails(self):
        text = self._business_minimal().replace(
            "**Actors**: `fdd-example-actor-analyst`, `fdd-example-actor-ui-app`",
            "**Actors**: `fdd-example-actor-unknown`",
        )
        report = VA.validate_business_context(text)
        self.assertEqual(report["status"], "FAIL")
        self.assertTrue(any(i.get("message") == "Capability references unknown actor IDs" for i in report.get("issues", [])))

    def test_business_use_case_unknown_capability_fails(self):
        text = "\n".join(
            [
                self._business_minimal(),
                "",
                "## D. Use Cases",
                "",
                "#### UC-001: Generate Report",
                "**ID**: `fdd-example-usecase-generate-report`",
                "**Actor**: `fdd-example-actor-analyst`",
                "**Preconditions**: Ready",
                "**Flow**:",
                "1. Use capability `fdd-example-capability-missing`",
                "**Postconditions**: Done",
            ]
        )
        report = VA.validate_business_context(text)
        self.assertEqual(report["status"], "FAIL")
        self.assertTrue(any(i.get("message") == "Use case references unknown capability ID" for i in report.get("issues", [])))

    def test_business_use_case_unknown_usecase_reference_fails(self):
        text = "\n".join(
            [
                self._business_minimal(),
                "",
                "## D. Use Cases",
                "",
                "#### UC-001: Generate Report",
                "**ID**: `fdd-example-usecase-generate-report`",
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


class TestDesignAdrCrossValidation(unittest.TestCase):
    def test_overall_design_orphaned_capability_fails(self):
        with TemporaryDirectory() as td:
            root = Path(td)
            arch = root / "architecture"
            arch.mkdir(parents=True)

            business = arch / "BUSINESS.md"
            business.write_text(
                "\n".join(
                    [
                        "# Business Context",
                        "## B. Actors",
                        "**Human Actors**:",
                        "#### Analyst",
                        "**ID**: `fdd-example-actor-analyst`",
                        "**Role**: R",
                        "**System Actors**:",
                        "#### UI",
                        "**ID**: `fdd-example-actor-ui-app`",
                        "**Role**: R",
                        "## C. Capabilities",
                        "#### Reporting",
                        "**ID**: `fdd-example-capability-reporting`",
                        "- F",
                        "**Actors**: `fdd-example-actor-analyst`",
                    ]
                )
                + "\n",
                encoding="utf-8",
            )

            adr = arch / "ADR.md"
            adr.write_text(
                "\n".join(
                    [
                        "# Mod - Architecture Decision Records",
                        "---",
                        "## ADR-0001: Initial",
                        "**Date**: 2026-01-01",
                        "**Status**: Accepted",
                        "### Context and Problem Statement",
                        "ok.",
                        "### Decision Drivers",
                        "- a",
                        "- b",
                        "### Considered Options",
                        "1. A (chosen)",
                        "2. B",
                        "### Decision Outcome",
                        "**Chosen option**: A",
                        "**Rationale**: ok",
                        "**Positive Consequences**:",
                        "- p",
                        "**Negative Consequences**:",
                        "- n",
                        "### Related Design Elements",
                        "**Actors**:",
                        "- `fdd-example-actor-analyst` - x",
                    ]
                )
                + "\n",
                encoding="utf-8",
            )

            design = arch / "DESIGN.md"
            design.write_text(
                "\n".join(
                    [
                        "# Design",
                        "## A. X",
                        "## B. Y",
                        "## C. Z",
                        "### C.1: One",
                        "### C.2: Two",
                        "### C.3: Three",
                        "### C.4: Four",
                        "### C.5: Five",
                        "",
                        "",
                        "**ID**: `fdd-example-req-something`",
                        "**Capabilities**: `fdd-example-capability-missing`",
                        "**Actors**: `fdd-example-actor-analyst`",
                        "**ADRs**: ADR-0001",
                    ]
                )
                + "\n",
                encoding="utf-8",
            )

            requirements = root / "req.md"
            requirements.write_text("### Section A: a\n### Section B: b\n### Section C: c\n", encoding="utf-8")

            report = VA.validate(
                design,
                requirements,
                "overall-design",
                business_path=business,
                adr_path=adr,
                skip_fs_checks=False,
            )
            self.assertEqual(report["status"], "FAIL")
            self.assertTrue(any(e.get("type") == "traceability" for e in report.get("errors", [])))

    def test_adr_related_design_elements_unknown_actor_fails(self):
        with TemporaryDirectory() as td:
            root = Path(td)
            arch = root / "architecture"
            arch.mkdir(parents=True)

            business = arch / "BUSINESS.md"
            business.write_text(
                "\n".join(
                    [
                        "# Business Context",
                        "## Section B: Actors",
                        "**Human Actors**:",
                        "#### Analyst",
                        "**ID**: `fdd-example-actor-analyst`",
                        "**Role**: R",
                        "**System Actors**:",
                        "#### UI",
                        "**ID**: `fdd-example-actor-ui-app`",
                        "**Role**: R",
                        "## Section C: Capabilities",
                        "#### Reporting",
                        "**ID**: `fdd-example-capability-reporting`",
                        "- F",
                        "**Actors**: `fdd-example-actor-analyst`",
                    ]
                )
                + "\n",
                encoding="utf-8",
            )

            design = arch / "DESIGN.md"
            design.write_text("## B. Requirements\n- fdd-example-req-something\n- fdd-example-principle-x\n", encoding="utf-8")

            adr = arch / "ADR.md"
            adr.write_text(
                "\n".join(
                    [
                        "# Mod - ADR",
                        "---",
                        "## ADR-0001: Initial",
                        "**Date**: 2026-01-01",
                        "**Status**: Accepted",
                        "### Context and Problem Statement",
                        "ok.",
                        "### Decision Drivers",
                        "- a",
                        "- b",
                        "### Considered Options",
                        "1. A (chosen)",
                        "2. B",
                        "### Decision Outcome",
                        "**Chosen option**: A",
                        "**Rationale**: ok",
                        "**Positive Consequences**:",
                        "- p",
                        "**Negative Consequences**:",
                        "- n",
                        "### Related Design Elements",
                        "**Actors**:",
                        "- `fdd-example-actor-missing` - x",
                    ]
                )
                + "\n",
                encoding="utf-8",
            )

            requirements = root / "req.md"
            requirements.write_text("### Section A: a\n", encoding="utf-8")

            report = VA.validate(
                adr,
                requirements,
                "adr",
                business_path=business,
                design_path=design,
                skip_fs_checks=False,
            )
            self.assertEqual(report["status"], "FAIL")
            self.assertTrue(any("Unknown actor" in i.get("message", "") for i in report.get("adr_issues", [])))

    def test_features_non_sequential_numbering_fails(self):
        text = _features_header("Example") + "\n\n".join(
            [
                _feature_entry(1, "fdd-example-feature-alpha", "alpha"),
                _feature_entry(3, "fdd-example-feature-beta", "beta"),
            ]
        )

        report = VA.validate_features_manifest(text)
        self.assertEqual(report["status"], "FAIL")
        self.assertTrue(any(e["type"] == "structure" for e in report["errors"]))

    def test_features_status_emoji_mismatch_fails(self):
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
    def test_main_exit_code_pass(self):
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
