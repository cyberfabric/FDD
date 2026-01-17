"""
FDD Validator - Python Package

Modular validation system for Feature-Driven Design artifacts.
Public API for backward compatibility.
"""

# Import from modular components
from .constants import *
from .utils import *

from .validation.traceability import (
    compute_excluded_line_ranges,
    is_line_excluded,
    is_effective_code_line,
    empty_fdd_tag_blocks_in_text,
    paired_inst_tags_in_text,
    unwrapped_inst_tag_hits_in_text,
    code_tag_hits,
    iter_code_files,
    extract_scope_ids,
)

from .validation.fdl import (
    extract_fdl_instructions,
    extract_scope_references_from_changes,
    validate_fdl_coverage,
    validate_fdl_completion,
    extract_inst_tags_from_code,
    validate_fdl_code_to_design,
    validate_fdl_code_implementation,
)

from .validation.artifacts import (
    validate,
    validate_feature_design,
    validate_overall_design,
    validate_feature_changes,
    validate_business_context,
    validate_adr,
    validate_features_manifest,
)

# Import CLI entry point
from .cli import main

# Re-export additional traceability validation functions
from .validation.traceability import (
    validate_codebase_traceability,
    validate_code_root_traceability,
)

# Backward compatibility: underscore prefixes for old test code
_compute_excluded_line_ranges = compute_excluded_line_ranges
_is_line_excluded = is_line_excluded
_is_effective_code_line = is_effective_code_line
_empty_fdd_tag_blocks_in_text = empty_fdd_tag_blocks_in_text
_paired_inst_tags_in_text = paired_inst_tags_in_text
_unwrapped_inst_tag_hits_in_text = unwrapped_inst_tag_hits_in_text
_code_tag_hits = code_tag_hits
_iter_code_files = iter_code_files
_extract_scope_ids = extract_scope_ids

__version__ = "1.0.0-modular"

__all__ = [
    # Main entry point
    "main",
    
    # Validation functions
    "validate",
    "validate_feature_design",
    "validate_overall_design",
    "validate_feature_changes",
    "validate_business_context",
    "validate_adr",
    "validate_features_manifest",
    "validate_codebase_traceability",
    "validate_code_root_traceability",
    
    # FDL validation
    "extract_fdl_instructions",
    "extract_scope_references_from_changes",
    "validate_fdl_coverage",
    "validate_fdl_completion",
    "extract_inst_tags_from_code",
    "validate_fdl_code_to_design",
    "validate_fdl_code_implementation",
    
    # Utils
    "detect_requirements",
    
    # Traceability
    "compute_excluded_line_ranges",
    "is_line_excluded",
    "is_effective_code_line",
    "empty_fdd_tag_blocks_in_text",
    "paired_inst_tags_in_text",
    "unwrapped_inst_tag_hits_in_text",
    "code_tag_hits",
    "iter_code_files",
    "extract_scope_ids",
    
    # Backward compat with underscores
    "_compute_excluded_line_ranges",
    "_is_line_excluded",
    "_is_effective_code_line",
    "_empty_fdd_tag_blocks_in_text",
    "_paired_inst_tags_in_text",
    "_unwrapped_inst_tag_hits_in_text",
    "_code_tag_hits",
    "_iter_code_files",
    "_extract_scope_ids",
]
