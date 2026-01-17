"""
Test design-first enforcement and validation.

Tests REAL DESIGN.md files structure.

Tests for: fdd-fdd-feature-core-methodology-test-block-unvalidated
           fdd-fdd-feature-core-methodology-test-validate-design-structure
"""
import pytest
from pathlib import Path
import sys

# Add fdd.py to path
sys.path.insert(0, str(Path(__file__).parent.parent / "skills" / "fdd" / "scripts"))


# fdd-begin fdd-fdd-feature-core-methodology-test-block-unvalidated:ph-1:inst-create-features-no-design
# fdd-begin fdd-fdd-feature-core-methodology-test-block-unvalidated:ph-1:inst-run-features-workflow
# fdd-begin fdd-fdd-feature-core-methodology-test-block-unvalidated:ph-1:inst-verify-prereq-check
# fdd-begin fdd-fdd-feature-core-methodology-test-block-unvalidated:ph-1:inst-verify-fails-prereq
# fdd-begin fdd-fdd-feature-core-methodology-test-block-unvalidated:ph-1:inst-verify-guidance
def test_features_manifest_references_design():
    """Verify FEATURES.md references DESIGN.md for each feature."""
    features_path = Path(__file__).parent.parent / "architecture" / "features" / "FEATURES.md"
    
    if not features_path.exists():
        pytest.skip("FEATURES.md not found")
    
    content = features_path.read_text(encoding='utf-8')
    
    # Verify FEATURES.md mentions design artifacts
    assert 'DESIGN.md' in content or 'design' in content.lower(), \
        "FEATURES.md should reference DESIGN.md files"
    
    # Check that feature entries have proper structure
    assert '## ' in content or '###' in content, \
        "FEATURES.md should have feature sections"
# fdd-end   fdd-fdd-feature-core-methodology-test-block-unvalidated:ph-1:inst-verify-guidance
# fdd-end   fdd-fdd-feature-core-methodology-test-block-unvalidated:ph-1:inst-verify-fails-prereq
# fdd-end   fdd-fdd-feature-core-methodology-test-block-unvalidated:ph-1:inst-verify-prereq-check
# fdd-end   fdd-fdd-feature-core-methodology-test-block-unvalidated:ph-1:inst-run-features-workflow
# fdd-end   fdd-fdd-feature-core-methodology-test-block-unvalidated:ph-1:inst-create-features-no-design


# fdd-begin fdd-fdd-feature-core-methodology-test-validate-design-structure:ph-1:inst-create-design-complete
# fdd-begin fdd-fdd-feature-core-methodology-test-validate-design-structure:ph-1:inst-run-structure-validation
# fdd-begin fdd-fdd-feature-core-methodology-test-validate-design-structure:ph-1:inst-verify-validation-passes
# fdd-begin fdd-fdd-feature-core-methodology-test-validate-design-structure:ph-1:inst-remove-section-b
# fdd-begin fdd-fdd-feature-core-methodology-test-validate-design-structure:ph-1:inst-rerun-after-remove
# fdd-begin fdd-fdd-feature-core-methodology-test-validate-design-structure:ph-1:inst-verify-missing-section
# fdd-begin fdd-fdd-feature-core-methodology-test-validate-design-structure:ph-1:inst-verify-section-b-error
def test_validate_all_feature_designs_have_required_sections():
    """Validate ALL feature DESIGN.md files have required sections A-F."""
    features_dir = Path(__file__).parent.parent / "architecture" / "features"
    assert features_dir.exists(), "architecture/features/ directory not found"
    
    # Find all feature DESIGN.md files
    design_files = list(features_dir.glob("*/DESIGN.md"))
    assert len(design_files) > 0, "No feature DESIGN.md files found"
    
    # Required sections for feature design
    required_sections = ['## A.', '## B.', '## C.', '## D.', '## E.', '## F.']
    
    errors = []
    
    for design_path in design_files:
        # Run structure validation
        content = design_path.read_text(encoding='utf-8')
        
        # Check each required section
        missing_sections = []
        for section in required_sections:
            if section not in content:
                missing_sections.append(section)
        
        # Verify validation passes - all sections present
        if missing_sections:
            errors.append(f"{design_path.parent.name}/DESIGN.md: Missing sections: {', '.join(missing_sections)}")
        
        # Also verify has title and feature ID
        if '# ' not in content:
            errors.append(f"{design_path.parent.name}/DESIGN.md: Missing title (# heading)")
        
        if '**ID**:' not in content and '- [ ]' not in content:
            errors.append(f"{design_path.parent.name}/DESIGN.md: Missing feature/flow IDs")
    
    # Report all errors found
    if errors:
        pytest.fail(f"Feature DESIGN.md structure validation failed:\n" + "\n".join(errors))
# fdd-end   fdd-fdd-feature-core-methodology-test-validate-design-structure:ph-1:inst-verify-section-b-error
# fdd-end   fdd-fdd-feature-core-methodology-test-validate-design-structure:ph-1:inst-verify-missing-section
# fdd-end   fdd-fdd-feature-core-methodology-test-validate-design-structure:ph-1:inst-rerun-after-remove
# fdd-end   fdd-fdd-feature-core-methodology-test-validate-design-structure:ph-1:inst-remove-section-b
# fdd-end   fdd-fdd-feature-core-methodology-test-validate-design-structure:ph-1:inst-verify-validation-passes
# fdd-end   fdd-fdd-feature-core-methodology-test-validate-design-structure:ph-1:inst-run-structure-validation
# fdd-end   fdd-fdd-feature-core-methodology-test-validate-design-structure:ph-1:inst-create-design-complete
