"""
FDD Validator - Common Validation Functions

Common validation logic shared across artifact types.
"""

import re
from pathlib import Path
from typing import Dict, List, Optional, Tuple

from ...utils import parse_required_sections, find_present_section_ids, find_placeholders


def validate_generic_sections(artifact_text: str, requirements_path: Path) -> Dict[str, object]:
    """Validate artifact against generic section requirements."""
    required_sections = parse_required_sections(requirements_path)
    if not required_sections:
        placeholders = find_placeholders(artifact_text)
        return {
            "required_section_count": 0,
            "missing_sections": [],
            "placeholder_hits": placeholders,
            "status": "FAIL",
            "errors": [
                {
                    "type": "requirements",
                    "message": "Could not parse required sections from requirements file (expected headings like '### Section X: ...')",
                    "requirements": str(requirements_path),
                }
            ],
        }

    present_ids_list = find_present_section_ids(artifact_text)
    present_ids = set(present_ids_list)
    
    # Format missing sections as list of dicts with id and title
    missing = [
        {
            "id": section_id,
            "title": required_sections[section_id],
        }
        for section_id in required_sections.keys()
        if section_id not in present_ids
    ]

    errors: List[Dict[str, object]] = []

    # Check for duplicate section IDs
    counts: Dict[str, int] = {}
    for sid in present_ids_list:
        counts[sid] = counts.get(sid, 0) + 1
    dup_sids = sorted([sid for sid, c in counts.items() if c > 1])
    if dup_sids:
        errors.append({"type": "structure", "message": "Duplicate section ids in artifact", "ids": dup_sids})

    # Check section order
    required_order = list(required_sections.keys())
    present_required_in_order = [sid for sid in present_ids_list if sid in required_sections]
    if present_required_in_order != required_order:
        errors.append(
            {
                "type": "structure",
                "message": "Sections are not in required order",
                "required_order": required_order,
                "found_order": present_required_in_order,
            }
        )
    
    placeholders = find_placeholders(artifact_text)
    passed = (len(missing) == 0) and (len(placeholders) == 0) and (len(errors) == 0)

    return {
        "required_section_count": len(required_sections),
        "missing_sections": missing,
        "placeholder_hits": placeholders,
        "status": "PASS" if passed else "FAIL",
        "errors": errors,
    }


def common_checks(
    *,
    artifact_text: str,
    artifact_path: Path,
    requirements_path: Path,
    skip_fs_checks: bool = False,
) -> Tuple[List[Dict[str, object]], List[Dict[str, object]]]:
    """
    Common validation checks applied to all artifacts.
    
    Returns:
        - List of error dicts
        - List of placeholder dicts
    """
    from ...constants import LINK_RE, HTML_COMMENT_RE, BRACE_PLACEHOLDER_RE, ID_LINE_RE, SIZE_HARD_LIMIT_RE
    
    errors: List[Dict[str, object]] = []
    placeholder_hits: List[Dict[str, object]] = []

    # Find HTML comment placeholders
    for match in HTML_COMMENT_RE.finditer(artifact_text):
        comment_text = match.group(0)
        for word in ["TODO", "TBD", "FIXME", "XXX", "TBA"]:
            if word in comment_text.upper():
                placeholder_hits.append({"type": "html_comment", "token": word, "text": comment_text[:50]})
                break

    # Find brace placeholders
    for match in BRACE_PLACEHOLDER_RE.finditer(artifact_text):
        placeholder_hits.append({"type": "brace_placeholder", "token": match.group(0)})

    # Check for disallowed link notation
    disallowed_pattern = re.compile(r"(@/|@DESIGN\.md|@BUSINESS\.md|@ADR\.md)")
    for match in disallowed_pattern.finditer(artifact_text):
        errors.append({"type": "link_format", "message": "Disallowed IDE-specific link notation", "token": match.group(0)})

    # Check file links if not skipping
    if not skip_fs_checks:
        for idx, line in enumerate(artifact_text.splitlines(), start=1):
            for _, target in LINK_RE.findall(line):
                t = target.strip()
                if not t or t.startswith("#"):
                    continue
                if t.startswith("http://") or t.startswith("https://"):
                    continue
                if t.startswith("/"):
                    errors.append({"type": "link_format", "message": "Absolute link targets are not allowed", "line": idx, "text": line.strip()})
                    continue
                t = t.split("#", 1)[0]
                if not t:
                    continue
                resolved = (artifact_path.parent / t).resolve()
                if not resolved.exists():
                    errors.append({"type": "link_target", "message": "Broken file link target", "line": idx, "target": t, "text": line.strip()})

    # Check FDD ID formatting and duplicates
    ids_seen: List[str] = []
    lines = artifact_text.splitlines()
    for i, line in enumerate(lines):
        if "**ID**:" not in line:
            continue
        m = ID_LINE_RE.search(line)
        if not m:
            continue
        val = m.group(1).strip()

        is_checkbox_id_line = re.match(r"^\s*[-*]\s+\[[ xX]\]\s+\*\*ID\*\*:\s+", line) is not None
        if "fdd-" in val and "`" not in val and not is_checkbox_id_line:
            errors.append({"type": "id", "message": "ID values must be wrapped in backticks", "line": i + 1, "text": line.strip()})

        for tok in re.findall(r"`([^`]+)`", val):
            if tok.startswith("fdd-"):
                ids_seen.append(tok)

    dup_ids = sorted({x for x in ids_seen if ids_seen.count(x) > 1})
    if dup_ids:
        errors.append({"type": "id", "message": "Duplicate fdd- IDs in document", "ids": dup_ids})

    # Check ID line spacing
    id_line_start_re = re.compile(r"^\s*(?:[-*]\s*)?(?:\[[ xX]\]\s*)?\*\*ID\*\*:\s*", re.IGNORECASE)
    for i, line in enumerate(lines[:-1]):
        if not re.match(r"^#{2,6}\s+", line.strip()):
            continue

        j = i + 1
        while j < len(lines) and lines[j].strip() == "":
            j += 1

        if j < len(lines) and id_line_start_re.match(lines[j]):
            if j != i + 2:
                errors.append({
                    "type": "id",
                    "message": "Exactly one blank line is required between heading and **ID** line",
                    "line": i + 1,
                    "text": line.strip(),
                })

    # Check section heading format
    for idx, line in enumerate(lines, start=1):
        if re.match(r"^##\s+Section\s+[A-Z]:", line.strip()):
            errors.append({"type": "section_heading", "message": "Disallowed section heading format (use '## A. Title')", "line": idx, "text": line.strip()})

    return errors, placeholder_hits


__all__ = ["validate_generic_sections", "common_checks"]
