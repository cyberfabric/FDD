"""
FDD Validator - FEATURES.md Validation

Validates features manifest: feature list, status tracking, requirements coverage.
"""

import re
from pathlib import Path
from typing import Dict, List, Optional, Set

from ...constants import (
    FEATURE_HEADING_RE,
    STATUS_OVERVIEW_RE,
)

from ...utils import find_placeholders, load_text, field_block, has_list_item


__all__ = ["validate_features_manifest"]


def _line_has_field(line: str, field_name: str, *, allow_empty_value: bool) -> bool:
    """Check if line contains a field with the given name."""
    if allow_empty_value:
        return re.match(rf"^\s*[-*]?\s*\*\*{re.escape(field_name)}\*\*:\s*(.*)$", line) is not None
    return re.match(rf"^\s*[-*]?\s*\*\*{re.escape(field_name)}\*\*:\s*.+$", line) is not None


def validate_features_manifest(
    artifact_text: str,
    *,
    artifact_path: Optional[Path] = None,
    design_path: Optional[Path] = None,
    skip_fs_checks: bool = False,
) -> Dict[str, object]:
    errors: List[Dict[str, object]] = []

    lines = artifact_text.splitlines()
    if not lines:
        errors.append({"type": "file", "message": "Empty file"})
        return {
            "required_section_count": 0,
            "missing_sections": [],
            "placeholder_hits": find_placeholders(artifact_text),
            "status": "FAIL",
            "errors": errors,
            "feature_issues": [],
            "feature_count": 0,
        }

    if not re.match(r"^#\s+Features:\s+.+$", lines[0].strip()):
        errors.append({"type": "header", "message": "Missing or invalid title '# Features: {PROJECT_NAME}'", "line": 1})

    overview_line = next((l for l in lines[:120] if "**Status Overview**:" in l), None)
    if overview_line is None:
        errors.append({"type": "header", "message": "Missing '**Status Overview**:'"})

    has_meaning = any(l.strip() == "**Meaning**:" for l in lines[:120])
    if not has_meaning:
        errors.append({"type": "header", "message": "Missing '**Meaning**:'"})

    # Minimal meaning lines check
    meaning_block = "\n".join(lines[:160])
    for emoji in ("⏳", "🔄", "✅"):
        if emoji not in meaning_block:
            errors.append({"type": "header", "message": f"Missing meaning entry for '{emoji}'"})

    feature_indices: List[int] = []
    feature_headers: List[Dict[str, object]] = []
    for idx, line in enumerate(lines):
        m = FEATURE_HEADING_RE.match(line.strip())
        if not m:
            continue
        feature_indices.append(idx)
        feature_headers.append(
            {
                "line": idx + 1,
                "number": int(m.group(1)),
                "id": m.group(2),
                "path": m.group(3),
                "emoji": m.group(4),
                "priority": m.group(5),
            }
        )

    if not feature_indices:
        errors.append({"type": "structure", "message": "No feature entries found (expected '### N. [id](feature-.../) EMOJI PRIORITY')"})
    else:
        nums = [h["number"] for h in feature_headers]
        expected = list(range(1, len(nums) + 1))
        if nums != expected:
            errors.append(
                {
                    "type": "structure",
                    "message": "Feature numbering must be sequential starting at 1 with no gaps",
                    "found": nums,
                }
            )

    seen_numbers: Dict[int, int] = {}
    seen_ids: Dict[str, int] = {}
    seen_paths: Dict[str, int] = {}
    for h in feature_headers:
        n = int(h["number"])
        seen_numbers[n] = seen_numbers.get(n, 0) + 1
        fid = str(h["id"]).strip()
        seen_ids[fid] = seen_ids.get(fid, 0) + 1
        p = str(h["path"]).strip()
        seen_paths[p] = seen_paths.get(p, 0) + 1

    dup_numbers = sorted([n for n, c in seen_numbers.items() if c > 1])
    dup_ids = sorted([k for k, c in seen_ids.items() if c > 1])
    dup_paths = sorted([k for k, c in seen_paths.items() if c > 1])
    if dup_numbers:
        errors.append({"type": "structure", "message": "Duplicate feature numbers", "numbers": dup_numbers})
    if dup_ids:
        errors.append({"type": "structure", "message": "Duplicate feature ids", "ids": dup_ids})
    if dup_paths:
        errors.append({"type": "structure", "message": "Duplicate feature paths", "paths": dup_paths})

    path_set = {str(h["path"]) for h in feature_headers}

    if overview_line is not None:
        m_overview = STATUS_OVERVIEW_RE.search(overview_line)
        if not m_overview:
            errors.append({"type": "header", "message": "Invalid Status Overview format"})
        else:
            total = int(m_overview.group(1))
            completed = int(m_overview.group(2))
            in_progress = int(m_overview.group(3))
            not_started = int(m_overview.group(4))

            actual_total = len(feature_headers)
            actual_completed = sum(1 for h in feature_headers if h["emoji"] == "✅")
            actual_in_progress = sum(1 for h in feature_headers if h["emoji"] == "🔄")
            actual_not_started = sum(1 for h in feature_headers if h["emoji"] == "⏳")

            if total != actual_total or completed != actual_completed or in_progress != actual_in_progress or not_started != actual_not_started:
                errors.append(
                    {
                        "type": "header",
                        "message": "Status Overview counts do not match feature entries",
                        "declared": {
                            "total": total,
                            "completed": completed,
                            "in_progress": in_progress,
                            "not_started": not_started,
                        },
                        "actual": {
                            "total": actual_total,
                            "completed": actual_completed,
                            "in_progress": actual_in_progress,
                            "not_started": actual_not_started,
                        },
                    }
                )

    design_ids: Dict[str, set] = {"req": set(), "principle": set(), "constraint": set()}
    if not skip_fs_checks and artifact_path is not None:
        resolved_design = design_path
        if resolved_design is None:
            resolved_design = artifact_path.parent.parent / "DESIGN.md"
        if not resolved_design.exists() or not resolved_design.is_file():
            errors.append({"type": "cross", "message": "DESIGN.md not found for cross-check", "path": str(resolved_design)})
        else:
            dt = resolved_design.read_text(encoding="utf-8")
            design_ids["req"].update(REQ_ID_RE.findall(dt))
            design_ids["req"].update(NFR_ID_RE.findall(dt))
            design_ids["principle"].update(PRINCIPLE_ID_RE.findall(dt))
            design_ids["constraint"].update(CONSTRAINT_ID_RE.findall(dt))

    required_fields: List[Tuple[str, bool]] = [
        ("Purpose", False),
        ("Status", False),
        ("Depends On", True),
        ("Blocks", True),
        ("Scope", True),
        ("Requirements Covered", True),
        ("Phases", True),
    ]

    feature_issues: List[Dict[str, object]] = []
    for i, header in enumerate(feature_headers):
        start = feature_indices[i]
        end = feature_indices[i + 1] if i + 1 < len(feature_indices) else len(lines)
        block_lines = lines[start:end]

        missing_fields = [
            field
            for (field, allow_empty) in required_fields
            if not any(_line_has_field(l, field, allow_empty_value=allow_empty) for l in block_lines)
        ]

        phases_block = field_block(block_lines, "Phases")
        phases_ok = phases_block is not None and "`ph-1`" in "\n".join([block_lines[phases_block["index"]]] + list(phases_block["tail"]))

        empty_list_fields: List[str] = []
        for field_name in ("Depends On", "Blocks", "Scope", "Requirements Covered", "Phases"):
            fb = field_block(block_lines, field_name)
            if fb is None:
                continue
            inline_value = str(fb["value"]).strip()
            if inline_value:
                continue
            if field_name in ("Depends On", "Blocks"):
                if inline_value == "None":
                    continue
            if has_list_item(list(fb["tail"])):
                continue
            empty_list_fields.append(field_name)

        status_mismatch: Optional[str] = None
        status_field = field_block(block_lines, "Status")
        if status_field is not None:
            status_value = str(status_field["value"]).strip()
            status_to_emoji = {
                "NOT_STARTED": "⏳",
                "IN_PROGRESS": "🔄",
                "IMPLEMENTED": "✅",
            }
            expected_emoji = status_to_emoji.get(status_value)
            if expected_emoji is not None and expected_emoji != header["emoji"]:
                status_mismatch = f"Status '{status_value}' does not match header emoji '{header['emoji']}'"

        slug_mismatch: Optional[str] = None
        m_id = re.search(r"-feature-(.+)$", str(header["id"]))
        if m_id:
            expected_path = f"feature-{m_id.group(1)}/"
            if str(header["path"]) != expected_path:
                slug_mismatch = f"Feature link path '{header['path']}' does not match id slug '{expected_path}'"

        dir_issue: Optional[str] = None
        if not skip_fs_checks and artifact_path is not None:
            features_dir = artifact_path.parent
            feature_dir = (features_dir / str(header["path"]))
            if not feature_dir.exists() or not feature_dir.is_dir():
                dir_issue = f"Feature directory does not exist: {feature_dir}"

        dep_issues: List[str] = []
        for dep_field in ("Depends On", "Blocks"):
            fb = field_block(block_lines, dep_field)
            if fb is None:
                continue
            inline_value = str(fb["value"]).strip()
            if inline_value == "None":
                continue
            dep_text = "\n".join([inline_value] + list(fb["tail"]))
            for link in _extract_feature_links(dep_text):
                if link not in path_set:
                    dep_issues.append(f"{dep_field} references missing feature entry: {link}")
                if link == str(header["path"]):
                    dep_issues.append(f"{dep_field} self-reference is not allowed: {link}")

        cross_issues: List[str] = []
        if design_ids["req"]:
            req_field = field_block(block_lines, "Requirements Covered")
            if req_field is not None:
                for rid in _extract_id_list(req_field):
                    if rid not in design_ids["req"]:
                        cross_issues.append(f"Requirements Covered references missing id in DESIGN.md: {rid}")
        if design_ids["principle"]:
            p_field = field_block(block_lines, "Principles Covered")
            if p_field is not None:
                for pid in _extract_id_list(p_field):
                    if pid not in design_ids["principle"]:
                        cross_issues.append(f"Principles Covered references missing id in DESIGN.md: {pid}")
        if design_ids["constraint"]:
            c_field = field_block(block_lines, "Constraints Affected")
            if c_field is not None:
                for cid in _extract_id_list(c_field):
                    if cid not in design_ids["constraint"]:
                        cross_issues.append(f"Constraints Affected references missing id in DESIGN.md: {cid}")

        if missing_fields or (not phases_ok) or empty_list_fields or status_mismatch or slug_mismatch or dir_issue or dep_issues or cross_issues:
            issue = {
                "feature": header,
                "missing_fields": missing_fields,
            }
            if not phases_ok:
                issue["phase_issues"] = ["Missing `ph-1` in phases"]
            if empty_list_fields:
                issue["empty_list_fields"] = empty_list_fields
            if status_mismatch:
                issue["status_issues"] = [status_mismatch]
            if slug_mismatch:
                issue["slug_issues"] = [slug_mismatch]
            if dir_issue:
                issue["dir_issues"] = [dir_issue]
            if dep_issues:
                issue["dependency_issues"] = dep_issues
            if cross_issues:
                issue["cross_issues"] = cross_issues
            feature_issues.append(issue)

    placeholders = find_placeholders(artifact_text)


    passed = (len(errors) == 0) and (len(feature_issues) == 0) and (len(placeholders) == 0)

    return {
        "required_section_count": len(required_fields) + 3,
        "missing_sections": [],
        "placeholder_hits": placeholders,
        "status": "PASS" if passed else "FAIL",
        "errors": errors,
        "feature_issues": feature_issues,
    }
