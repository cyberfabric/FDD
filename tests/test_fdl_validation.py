# @fdd-change:fdd-fdd-feature-core-methodology-change-requirements-structure:ph-1
# Tests implement:
# - fdd-fdd-feature-core-methodology-test-parse-workflow
# - fdd-fdd-feature-core-methodology-test-validate-design-structure  
# - fdd-fdd-feature-core-methodology-test-block-unvalidated
"""
Tests for FDL coverage and completion validation.

Validates that:
1. CHANGES.md references all FDL instructions from DESIGN.md
2. COMPLETED features have all FDL instructions marked [x]
"""
import sys
import unittest
import tempfile
from pathlib import Path
from tempfile import TemporaryDirectory

# Add skills/fdd/scripts directory to path to import fdd module
sys.path.insert(0, str(Path(__file__).parent.parent / "skills" / "fdd" / "scripts"))

from fdd import (
    extract_fdl_instructions,
    extract_scope_references_from_changes,
    validate_fdl_coverage,
    validate_fdl_completion,
    validate_feature_changes
)


# fdd-begin fdd-fdd-feature-core-methodology-flow-developer-implement:ph-1:inst-add-tags
_TRACEABILITY_DEV_ADD_TAGS = True
# fdd-end   fdd-fdd-feature-core-methodology-flow-developer-implement:ph-1:inst-add-tags

# fdd-begin fdd-fdd-feature-core-methodology-flow-developer-implement:ph-1:inst-write-code
_TRACEABILITY_DEV_WRITE_CODE = True
# fdd-end   fdd-fdd-feature-core-methodology-flow-developer-implement:ph-1:inst-write-code

# fdd-begin fdd-fdd-feature-core-methodology-flow-developer-implement:ph-1:inst-mark-complete
_TRACEABILITY_DEV_MARK_COMPLETE = True
# fdd-end   fdd-fdd-feature-core-methodology-flow-developer-implement:ph-1:inst-mark-complete


# fdd-begin fdd-fdd-feature-core-methodology-test-parse-workflow:ph-1:inst-test-extraction
class TestFDLInstructionExtraction(unittest.TestCase):
    """Test FDL instruction extraction from DESIGN.md."""

    def test_extract_fdl_instructions_from_flow(self):
        """Extract only [x] marked inst-{id} from flow steps."""
        design_text = """
## B. Actor Flows (FDL)

### Flow: Create Task
- [ ] **ID**: `fdd-task-api-feature-task-crud-flow-create-task`

**Steps**:
1. [ ] - `ph-1` - Receive HTTP POST request - `inst-receive-request`
2. [ ] - `ph-1` - Validate input - `inst-validate-input`
3. [x] - `ph-1` - Save to database - `inst-save-db`
"""
        result = extract_fdl_instructions(design_text)

        flow_id = "fdd-task-api-feature-task-crud-flow-create-task"
        self.assertIn(flow_id, result)
        # Should only return [x] marked instructions, not [ ]
        self.assertEqual(len(result[flow_id]["instructions"]), 1)
        self.assertIn("inst-save-db", result[flow_id]["instructions"])
        self.assertNotIn("inst-receive-request", result[flow_id]["instructions"])
        self.assertNotIn("inst-validate-input", result[flow_id]["instructions"])

    def test_extract_fdl_instructions_from_algorithm(self):
        """Extract only [x] marked inst-{id} from algorithm steps."""
        design_text = """
## C. Algorithms (FDL)

### Algorithm: Validate Input
- [ ] **ID**: `fdd-task-api-feature-task-crud-algo-validate-input`

**Steps**:
1. [ ] - `ph-1` - Check title present - `inst-check-title`
2. [x] - `ph-1` - Check length - `inst-check-length`
"""
        result = extract_fdl_instructions(design_text)
        
        algo_id = "fdd-task-api-feature-task-crud-algo-validate-input"
        self.assertIn(algo_id, result)
        # Should only return [x] marked instruction
        self.assertEqual(len(result[algo_id]["instructions"]), 1)
        self.assertIn("inst-check-length", result[algo_id]["instructions"])
        self.assertNotIn("inst-check-title", result[algo_id]["instructions"])


# fdd-end   fdd-fdd-feature-core-methodology-test-parse-workflow:ph-1:inst-test-extraction


# fdd-begin fdd-fdd-feature-core-methodology-test-validate-design-structure:ph-1:inst-test-scope-extraction
class TestScopeReferenceExtraction(unittest.TestCase):
    """Test scope ID extraction from CHANGES.md."""

    def test_extract_scope_references_from_tasks(self):
        """Extract flow/algo/state/test IDs mentioned in CHANGES.md."""
        changes_text = """
## 1. Implementation

### 1.1 Create Handler
- [ ] 1.1.1 Implement flow `fdd-task-api-feature-task-crud-flow-create-task`
- [x] 1.1.2 Add algorithm `fdd-task-api-feature-task-crud-algo-validate-input`
- [ ] 1.1.3 Implement state machine `fdd-task-api-feature-task-crud-state-lifecycle`
"""
        result = extract_scope_references_from_changes(changes_text)
        
        expected = {
            "fdd-task-api-feature-task-crud-flow-create-task",
            "fdd-task-api-feature-task-crud-algo-validate-input",
            "fdd-task-api-feature-task-crud-state-lifecycle"
        }
        self.assertEqual(result, expected)

    def test_extract_no_references_if_not_present(self):
        """Return empty set if no scope IDs in tasks."""
        changes_text = """
## 1. Implementation

### 1.1 Create Handler
- [ ] 1.1.1 Implement receive request logic
- [ ] 1.1.2 Add validation
"""
        result = extract_scope_references_from_changes(changes_text)
        self.assertEqual(result, set())


# fdd-end   fdd-fdd-feature-core-methodology-test-validate-design-structure:ph-1:inst-test-scope-extraction


# fdd-begin fdd-fdd-feature-core-methodology-test-validate-design-structure:ph-1:inst-test-coverage
class TestFDLCoverageValidation(unittest.TestCase):
    """Test FDL coverage validation."""

    def test_fdl_coverage_pass_when_all_scopes_referenced(self):
        """Pass validation when all scopes are referenced."""
        design_fdl = {
            "fdd-x-feature-y-flow-z": {
                "instructions": ["inst-a", "inst-b"],
                "completed": [False, False]
            },
            "fdd-x-feature-y-algo-validate": {
                "instructions": ["inst-c"],
                "completed": [False]
            }
        }
        changes_text = """
- [ ] 1.1.1 Implement flow `fdd-x-feature-y-flow-z`
- [ ] 1.1.2 Implement algorithm `fdd-x-feature-y-algo-validate`
"""
        errors = validate_fdl_coverage(changes_text, design_fdl)
        self.assertEqual(errors, [])

    def test_fdl_coverage_fail_when_scope_missing(self):
        """Fail validation when scope not referenced."""
        design_fdl = {
            "fdd-x-feature-y-flow-z": {
                "instructions": ["inst-a"],
                "completed": [False]
            },
            "fdd-x-feature-y-algo-validate": {
                "instructions": ["inst-b"],
                "completed": [False]
            }
        }
        changes_text = """
- [ ] 1.1.1 Implement flow `fdd-x-feature-y-flow-z`
"""
        errors = validate_fdl_coverage(changes_text, design_fdl)
        
        self.assertEqual(len(errors), 1)
        self.assertEqual(errors[0]["type"], "fdl_coverage")
        self.assertEqual(errors[0]["scope_id"], "fdd-x-feature-y-algo-validate")
        self.assertIn("fdd-x-feature-y-algo-validate", errors[0]["message"])


# fdd-end   fdd-fdd-feature-core-methodology-test-validate-design-structure:ph-1:inst-test-coverage


# fdd-begin fdd-fdd-feature-core-methodology-test-block-unvalidated:ph-1:inst-test-completion
class TestFDLCompletionValidation(unittest.TestCase):
    """Test FDL completion validation."""

    def test_completion_validation_skipped_if_not_completed(self):
        """Skip validation if feature not marked COMPLETED."""
        design_fdl = {
            "fdd-x-feature-y-flow-z": {
                "instructions": [],  # No [x] instructions  
                "completed": []
            }
        }
        changes_text = "**Status**: 🔄 IN_PROGRESS"
        
        errors = validate_fdl_completion(changes_text, design_fdl)
        
        # Should skip validation when not COMPLETED
        self.assertEqual(len(errors), 0)

    def test_completion_validation_pass_when_all_completed(self):
        """Pass when feature COMPLETED and all instructions [x]."""
        design_fdl = {
            "fdd-x-feature-y-flow-z": {
                "instructions": ["inst-a", "inst-b"],
                "completed": [True, True]
            }
        }
        changes_text = "**Status**: ✅ COMPLETED"
        
        errors = validate_fdl_completion(changes_text, design_fdl)
        self.assertEqual(errors, [])

    def test_completion_validation_fail_when_instructions_incomplete(self):
        """Fail when feature COMPLETED but instructions still [ ]."""
        design_fdl = {
            "fdd-x-feature-y-flow-z": {
                "instructions": ["inst-a", "inst-b"],
                "completed": [True, False]
            },
            "fdd-x-feature-y-algo-w": {
                "instructions": ["inst-c"],
                "completed": [False]
            }
        }
        changes_text = "**Status**: ✅ COMPLETED"
        
        errors = validate_fdl_completion(changes_text, design_fdl)
        
        self.assertEqual(len(errors), 1)
        self.assertEqual(errors[0]["type"], "premature_completion")
        self.assertEqual(errors[0]["uncompleted_count"], 2)
        self.assertIn("inst-b", str(errors[0]["examples"]))
        self.assertIn("inst-c", str(errors[0]["examples"]))


# fdd-end   fdd-fdd-feature-core-methodology-test-block-unvalidated:ph-1:inst-test-completion


# fdd-begin fdd-fdd-feature-core-methodology-test-validate-workflow-structure:ph-1:inst-test-integration
class TestIntegratedValidation(unittest.TestCase):
    """Test integrated FDL validation in validate_feature_changes."""

    def test_validate_feature_changes_with_fdl_coverage_error(self):
        """Integration test: CHANGES.md missing FDL coverage."""
        from tempfile import TemporaryDirectory
        
        with TemporaryDirectory() as td:
            root = Path(td)
            feat = root / "feature-x"
            feat.mkdir(parents=True)
            
            # Create DESIGN.md with FDL instructions
            design = feat / "DESIGN.md"
            design.write_text("""# Feature Design: X

**Feature**: `x`

## A. Feature Context

### 1. Overview
Test feature.

### 2. Purpose
Test.

### 3. Actors
- Test Actor

### 4. References
- Overall Design: [DESIGN.md](../../DESIGN.md)

## B. Actor Flows (FDL)

### Flow: Test
- [ ] **ID**: `fdd-x-feature-x-flow-test`

**Steps**:
- [ ] - `ph-1` - Step 1 - `inst-step1`
- [ ] - `ph-1` - Step 2 - `inst-step2`

## C. Algorithms (FDL)

None

## D. States (FDL)

None

## E. Technical Details

None

## F. Requirements

### Requirement: Test
- [ ] **ID**: `fdd-x-feature-x-req-test`
**Priority**: HIGH
**Description**: Test requirement

**Implements**: None
**Phases**: `ph-1`
**Testing Scenarios (FDL)**: None
""", encoding="utf-8")
            
            # Create CHANGES.md that does NOT reference the flow scope
            changes = feat / "CHANGES.md"
            changes.write_text("""
# Implementation Plan: X

**Feature**: `x`
**Version**: 1.0
**Last Updated**: 2026-01-17
**Status**: 🔄 IN_PROGRESS

**Feature DESIGN**: [DESIGN.md](DESIGN.md)

---

## Summary

**Total Changes**: 1
**Completed**: 0
**In Progress**: 1
**Not Started**: 0

**Estimated Effort**: 1 story points

---

## Change 1: First

**ID**: `fdd-x-feature-x-change-first`
**Status**: 🔄 IN_PROGRESS
**Priority**: HIGH
**Effort**: 1 story points
**Implements**: `fdd-x-feature-x-req-test`
**Phases**: `ph-1`

---

### Objective
Test change.

### Requirements Coverage
**Implements**:
- **`fdd-x-feature-x-req-test`**: Test requirement

### Tasks

## 1. Implementation

### 1.1 Work
- [ ] 1.1.1 Implement some work

## 2. Testing

### 2.1 Tests
- [ ] 2.1.1 Test it

### Specification

**Domain Model Changes**: None

**API Changes**: None

**Database Changes**: None

**Code Changes**: None

### Dependencies

**Blocks**: None

### Testing

**Unit Tests**: None
""", encoding="utf-8")
            
            # Validate - should have FDL coverage error for missing flow scope
            from fdd import validate_feature_changes
            report = validate_feature_changes(
                changes.read_text(encoding="utf-8"),
                artifact_path=changes,
                skip_fs_checks=False
            )
            
            # Check for FDL coverage error
            fdl_errors = [e for e in report["errors"] if e.get("type") == "fdl_coverage"]
            self.assertTrue(len(fdl_errors) > 0, "Expected FDL coverage error")
            self.assertIn("fdd-x-feature-x-flow-test", str(fdl_errors[0]))


# fdd-end   fdd-fdd-feature-core-methodology-test-validate-workflow-structure:ph-1:inst-test-integration


# fdd-begin fdd-fdd-feature-core-methodology-test-validate-design-structure:ph-1:inst-test-cross-reference
class TestFDLCrossReferenceValidation(unittest.TestCase):
    """Test reverse validation: fdd tags in code must be marked [x] in DESIGN.md."""

    def test_untracked_implementation_detected(self):
        """Test that fdd tags in code without [x] in DESIGN are detected."""
        # Create temporary test files
        with tempfile.TemporaryDirectory() as tmpdir:
            feature_root = Path(tmpdir) / "architecture" / "features" / "feature-test"
            feature_root.mkdir(parents=True)
            
            # Create DESIGN.md with instruction NOT marked [x]
            design_content = """
# Feature Design: Test Feature

## B. Actor Flows

### Test Flow

- [ ] **ID**: `fdd-test-feature-test-flow-example`

**Steps**:

1. [ ] - `ph-1` - Do something - `inst-do-something`
2. [ ] - `ph-1` - Do another thing - `inst-another-thing`
"""
            design_path = feature_root / "DESIGN.md"
            design_path.write_text(design_content)
            
            # Create code file with fdd tags for inst-do-something
            code_dir = Path(tmpdir) / "src"
            code_dir.mkdir()
            code_file = code_dir / "test.py"
            code_file.write_text("""
# fdd-begin fdd-test-feature-test-flow-example:ph-1:inst-do-something
def do_something():
    pass
# fdd-end   fdd-test-feature-test-flow-example:ph-1:inst-do-something
""")
            
            # Run validation
            sys.path.insert(0, str(Path(__file__).parent.parent / "skills" / "fdd" / "scripts"))
            from fdd import validate_fdl_code_to_design
            
            errors = validate_fdl_code_to_design(feature_root, design_content)
            
            # Should detect untracked implementation
            self.assertEqual(len(errors), 1)
            self.assertEqual(errors[0]["type"], "fdl_untracked_implementation")
            self.assertIn("inst-do-something", errors[0]["instructions"])

    def test_tracked_implementation_passes(self):
        """Test that fdd tags marked [x] in DESIGN pass validation."""
        with tempfile.TemporaryDirectory() as tmpdir:
            feature_root = Path(tmpdir) / "architecture" / "features" / "feature-test"
            feature_root.mkdir(parents=True)
            
            # Create DESIGN.md with instruction marked [x]
            design_content = """
# Feature Design: Test Feature

## B. Actor Flows

### Test Flow

- [ ] **ID**: `fdd-test-feature-test-flow-example`

**Steps**:

1. [x] - `ph-1` - Do something - `inst-do-something`
2. [ ] - `ph-1` - Do another thing - `inst-another-thing`
"""
            design_path = feature_root / "DESIGN.md"
            design_path.write_text(design_content)
            
            # Create code file with fdd tags
            code_dir = Path(tmpdir) / "src"
            code_dir.mkdir()
            code_file = code_dir / "test.py"
            code_file.write_text("""
# fdd-begin fdd-test-feature-test-flow-example:ph-1:inst-do-something
def do_something():
    pass
# fdd-end   fdd-test-feature-test-flow-example:ph-1:inst-do-something
""")
            
            # Run validation
            sys.path.insert(0, str(Path(__file__).parent.parent / "skills" / "fdd" / "scripts"))
            from fdd import validate_fdl_code_to_design
            
            errors = validate_fdl_code_to_design(Path(tmpdir), design_content)
            
            # Should pass - no errors
            self.assertEqual(len(errors), 0)

    def test_no_tags_in_code_passes(self):
        """Test that having no fdd tags in code passes reverse validation."""
        with tempfile.TemporaryDirectory() as tmpdir:
            feature_root = Path(tmpdir) / "architecture" / "features" / "feature-test"
            feature_root.mkdir(parents=True)
            
            # Create DESIGN.md
            design_content = """
# Feature Design: Test Feature

## B. Actor Flows

### Test Flow

- [ ] **ID**: `fdd-test-feature-test-flow-example`

**Steps**:

1. [x] - `ph-1` - Do something - `inst-do-something`
"""
            design_path = feature_root / "DESIGN.md"
            design_path.write_text(design_content)
            
            # Create code file WITHOUT fdd tags
            code_dir = Path(tmpdir) / "src"
            code_dir.mkdir()
            code_file = code_dir / "test.py"
            code_file.write_text("""
def do_something():
    pass
""")
            
            # Run validation
            sys.path.insert(0, str(Path(__file__).parent.parent / "skills" / "fdd" / "scripts"))
            from fdd import validate_fdl_code_to_design
            
            errors = validate_fdl_code_to_design(Path(tmpdir), design_content)
            
            # Should pass reverse validation (forward validation would fail)
            self.assertEqual(len(errors), 0)
# fdd-end   fdd-fdd-feature-core-methodology-test-validate-design-structure:ph-1:inst-test-cross-reference


if __name__ == "__main__":
    unittest.main(verbosity=2)
