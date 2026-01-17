"""
FDD Validator - Artifacts Package

Validation for all FDD artifacts split into focused modules.
"""

from pathlib import Path
from typing import Dict, Optional

from .feature_design import validate_feature_design
from .overall_design import validate_overall_design
from .changes import validate_feature_changes
from .business import validate_business_context
from .adr import validate_adr
from .features import validate_features_manifest
from .common import validate_generic_sections, common_checks


def validate(
    artifact_path: Path,
    requirements_path: Path,
    artifact_kind: str,
    *,
    design_path: Optional[Path] = None,
    business_path: Optional[Path] = None,
    adr_path: Optional[Path] = None,
    skip_fs_checks: bool = False,
) -> Dict[str, object]:
    """Main validation dispatcher - routes to appropriate validator."""
    artifact_text = artifact_path.read_text(encoding="utf-8")

    if not artifact_text.strip():
        return {
            "required_section_count": 0,
            "missing_sections": [],
            "placeholder_hits": [],
            "status": "FAIL",
            "errors": [{"type": "file", "message": "Empty file"}],
        }

    if artifact_kind == "features-manifest":
        report = validate_features_manifest(
            artifact_text,
            artifact_path=artifact_path,
            skip_fs_checks=skip_fs_checks,
        )
    elif artifact_kind == "business-context":
        report = validate_business_context(artifact_text)
    elif artifact_kind == "adr":
        report = validate_adr(
            artifact_text,
            artifact_path=artifact_path,
            skip_fs_checks=skip_fs_checks,
        )
    elif artifact_kind == "feature-design":
        report = validate_feature_design(
            artifact_text,
            artifact_path=artifact_path,
            skip_fs_checks=skip_fs_checks,
        )
    elif artifact_kind == "feature-changes":
        report = validate_feature_changes(
            artifact_text,
            artifact_path=artifact_path,
            skip_fs_checks=skip_fs_checks,
        )
    elif artifact_kind == "overall-design":
        report = validate_overall_design(
            artifact_text,
            artifact_path=artifact_path,
            business_path=business_path,
            adr_path=adr_path,
            skip_fs_checks=skip_fs_checks,
        )
    else:
        report = validate_generic_sections(artifact_text, requirements_path)

    # Apply common checks
    common_errors, common_placeholders = common_checks(
        artifact_text=artifact_text,
        artifact_path=artifact_path,
        requirements_path=requirements_path,
        skip_fs_checks=skip_fs_checks,
    )
    
    if "errors" not in report:
        report["errors"] = []
    report["errors"].extend(common_errors)
    
    if "placeholder_hits" not in report:
        report["placeholder_hits"] = []
    report["placeholder_hits"].extend(common_placeholders)
    
    if report.get("placeholder_hits"):
        report["status"] = "FAIL"
    if report.get("errors") and report.get("status") == "PASS":
        report["status"] = "FAIL"
    
    return report


__all__ = [
    "validate",
    "validate_feature_design",
    "validate_overall_design",
    "validate_feature_changes",
    "validate_business_context",
    "validate_adr",
    "validate_features_manifest",
]
