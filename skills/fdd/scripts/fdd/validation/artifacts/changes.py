"""
FDD Validator - Feature CHANGES.md Validation

Validates implementation plans: structure, change entries, dependencies, FDL coverage.
"""

import re
from pathlib import Path
from typing import Dict, List, Optional, Tuple

from ...constants import (
    CHANGES_HEADER_TITLE_RE,
    CHANGE_HEADING_RE,
    CHANGE_ID_RE,
    CHANGE_STATUS_RE,
    CHANGE_PRIORITY_RE,
    PHASE_TOKEN_RE,
    CHANGE_TASK_LINE_RE,
    FEATURE_REQ_ID_RE,
)

from ...utils import find_placeholders, load_text

# Import FDL validation
from ..fdl import (
    extract_fdl_instructions,
    validate_fdl_coverage,
    extract_scope_references_from_changes,
)


__all__ = ["validate_feature_changes"]
def validate_feature_changes(
    artifact_text: str,
    *,
    artifact_path: Optional[Path] = None,
    skip_fs_checks: bool = False,
) -> Dict[str, object]:
    errors: List[Dict[str, object]] = []
    placeholders = find_placeholders(artifact_text)

    feature_slug: Optional[str] = None
    feature_root: Optional[Path] = None
    if artifact_path is not None:
        if artifact_path.parent.name == "archive" and artifact_path.parent.parent.name.startswith("feature-"):
            feature_root = artifact_path.parent.parent
        elif artifact_path.parent.name.startswith("feature-"):
            feature_root = artifact_path.parent
        else:
            feature_root = artifact_path.parent

        if feature_root.name.startswith("feature-"):
            feature_slug = feature_root.name[len("feature-") :]

    lines = artifact_text.splitlines()
    if not lines or not CHANGES_HEADER_TITLE_RE.match(lines[0].strip()):
        errors.append({"type": "header", "message": "Missing or invalid title '# Implementation Plan: {Feature Name}'", "line": 1})

    header_text = "\n".join(lines[:160])

    m_feature = re.search(r"\*\*Feature\*\*:\s*`([^`]+)`", header_text)
    if not m_feature:
        errors.append({"type": "header", "message": "Missing **Feature**: `{feature-slug}`"})
    else:
        header_slug = m_feature.group(1).strip()
        if feature_slug is not None and header_slug != feature_slug:
            errors.append({"type": "header", "message": "Header **Feature** slug must match directory slug", "expected": feature_slug, "found": header_slug})

    if not re.search(r"\*\*Version\*\*:\s*\S+", header_text):
        errors.append({"type": "header", "message": "Missing **Version**"})

    if not re.search(r"\*\*Last Updated\*\*:\s*\d{4}-\d{2}-\d{2}", header_text):
        errors.append({"type": "header", "message": "Missing or invalid **Last Updated** date", "expected": "YYYY-MM-DD"})

    m_status = re.search(r"\*\*Status\*\*:\s*(.+)$", header_text, re.MULTILINE)
    if not m_status:
        errors.append({"type": "header", "message": "Missing **Status**"})
    else:
        s = m_status.group(1).strip()
        if not CHANGE_STATUS_RE.match(s):
            errors.append({"type": "header", "message": "Invalid overall **Status**", "status": s})

    if not re.search(r"\*\*Feature DESIGN\*\*:\s*\[[^\]]+\]\((?:\.\./)?DESIGN\.md\)", header_text):
        errors.append({"type": "header", "message": "Missing or invalid **Feature DESIGN** link (must point to DESIGN.md)"})

    summary_counts: Optional[Dict[str, int]] = None
    if "## Summary" not in artifact_text:
        errors.append({"type": "structure", "message": "Missing ## Summary section"})
    else:
        m_total = re.search(r"\*\*Total Changes\*\*:\s*(\d+)", artifact_text)
        m_completed = re.search(r"\*\*Completed\*\*:\s*(\d+)", artifact_text)
        m_in_progress = re.search(r"\*\*In Progress\*\*:\s*(\d+)", artifact_text)
        m_not_started = re.search(r"\*\*Not Started\*\*:\s*(\d+)", artifact_text)
        if not (m_total and m_completed and m_in_progress and m_not_started):
            errors.append({"type": "structure", "message": "Summary must include Total/Completed/In Progress/Not Started counts"})
        else:
            total = int(m_total.group(1))
            completed = int(m_completed.group(1))
            in_progress = int(m_in_progress.group(1))
            not_started = int(m_not_started.group(1))
            if total != (completed + in_progress + not_started):
                errors.append({"type": "structure", "message": "Summary counts do not add up", "total": total, "sum": completed + in_progress + not_started})
            summary_counts = {"total": total, "completed": completed, "in_progress": in_progress, "not_started": not_started}

    change_starts: List[int] = []
    change_nums: List[int] = []
    for i, line in enumerate(lines):
        m = CHANGE_HEADING_RE.match(line.strip())
        if not m:
            continue
        change_starts.append(i)
        change_nums.append(int(m.group(1)))

    if not change_starts:
        errors.append({"type": "structure", "message": "No change entries found (expected '## Change 1: ...')"})
        change_blocks: List[Tuple[int, int, int, List[str]]] = []
    else:
        expected = list(range(1, len(change_nums) + 1))
        if change_nums != expected:
            errors.append({"type": "structure", "message": "Change entries must be numbered sequentially", "expected": expected, "found": change_nums})

        change_blocks = []
        for idx, start in enumerate(change_starts):
            end = change_starts[idx + 1] if idx + 1 < len(change_starts) else len(lines)
            change_blocks.append((change_nums[idx], start, end, lines[start:end]))

    def _get_field_value(block_lines: List[str], field: str) -> Optional[str]:
        pat = re.compile(rf"^\*\*{re.escape(field)}\*\*:\s*(.+?)\s*$")
        for l in block_lines:
            m = pat.match(l.strip())
            if m:
                return m.group(1).strip()
        return None

    change_ids: List[str] = []
    implements_by_change: Dict[int, List[str]] = {}
    phases_by_change: Dict[int, List[int]] = {}
    deps: Dict[int, List[int]] = {}

    for n, start, _, block in change_blocks:
        block_text = "\n".join(block)

        cid_val = _get_field_value(block, "ID")
        cid: Optional[str] = None
        if cid_val is None:
            errors.append({"type": "id", "message": "Change missing **ID**", "change": n, "line": start + 1})
        else:
            m = re.search(r"`([^`]+)`", cid_val)
            if not m:
                errors.append({"type": "id", "message": "Change **ID** must be wrapped in backticks", "change": n, "line": start + 1})
            else:
                cid = m.group(1).strip()
                change_ids.append(cid)
                m2 = CHANGE_ID_RE.fullmatch(cid)
                if not m2:
                    errors.append({"type": "id", "message": "Invalid change ID format", "change": n, "id": cid})
                elif feature_slug is not None and m2.group(1) != feature_slug:
                    errors.append({"type": "id", "message": "Feature slug in change ID does not match directory slug", "change": n, "expected": feature_slug, "found": m2.group(1)})

        status_val = _get_field_value(block, "Status")
        if status_val is None:
            errors.append({"type": "content", "message": "Change missing **Status**", "change": n})
        elif not CHANGE_STATUS_RE.match(status_val):
            errors.append({"type": "content", "message": "Invalid change **Status**", "change": n, "status": status_val})

        prio_val = _get_field_value(block, "Priority")
        if prio_val is None:
            errors.append({"type": "content", "message": "Change missing **Priority**", "change": n})
        elif not CHANGE_PRIORITY_RE.match(prio_val):
            errors.append({"type": "content", "message": "Invalid change **Priority**", "change": n, "priority": prio_val})

        if _get_field_value(block, "Effort") is None:
            errors.append({"type": "content", "message": "Change missing **Effort**", "change": n})

        impl_val = _get_field_value(block, "Implements")
        impl_ids: List[str] = []
        if impl_val is None:
            errors.append({"type": "content", "message": "Change missing **Implements**", "change": n})
        else:
            impl_ids = [x.strip() for x in re.findall(r"`([^`]+)`", impl_val) if x.strip().startswith("fdd-")]
            if not impl_ids:
                errors.append({"type": "content", "message": "Change **Implements** must include at least one requirement ID", "change": n})
            if len(impl_ids) > 5:
                errors.append({"type": "content", "message": "Change must implement 1-5 requirements", "change": n, "count": len(impl_ids)})
            for rid in impl_ids:
                m_req = FEATURE_REQ_ID_RE.fullmatch(rid)
                if not m_req:
                    errors.append({"type": "id", "message": "Invalid requirement ID in **Implements**", "change": n, "id": rid})
                elif feature_slug is not None and m_req.group(1) != feature_slug:
                    errors.append({"type": "id", "message": "Feature slug in requirement ID does not match directory slug", "change": n, "expected": feature_slug, "found": m_req.group(1), "id": rid})

        phases_val = _get_field_value(block, "Phases")
        phase_nums: List[int] = []
        if phases_val is None:
            errors.append({"type": "content", "message": "Change missing **Phases**", "change": n})
        else:
            phase_nums = [int(x) for x in PHASE_TOKEN_RE.findall(phases_val)]
            if 1 not in phase_nums:
                errors.append({"type": "content", "message": "Change phases must include ph-1", "change": n})
        phases_by_change[n] = sorted(set(phase_nums))
        implements_by_change[n] = impl_ids

        for sub in ("### Objective", "### Requirements Coverage", "### Tasks", "### Specification", "### Dependencies", "### Testing"):
            if sub not in block_text:
                errors.append({"type": "structure", "message": "Missing required subsection in change", "change": n, "subsection": sub})

        tasks: List[Tuple[List[int], str]] = []
        for l in block:
            m_task = CHANGE_TASK_LINE_RE.match(l)
            if not m_task:
                continue
            nums = [int(x) for x in m_task.group(1).split(".")]
            tasks.append((nums, m_task.group(2).strip()))
        if not tasks:
            errors.append({"type": "content", "message": "Change must contain checkbox tasks with hierarchical numbering", "change": n})

        deps.setdefault(n, [])
        in_deps = False
        in_depends = False
        in_blocks = False
        for l in block:
            if l.strip() == "### Dependencies":
                in_deps = True
                in_depends = False
                in_blocks = False
                continue
            if in_deps and l.strip().startswith("### ") and l.strip() != "### Dependencies":
                break
            if not in_deps:
                continue
            if l.strip().startswith("**Depends on**"):
                in_depends = True
                in_blocks = False
                continue
            if l.strip().startswith("**Blocks**"):
                in_blocks = True
                in_depends = False
                continue
            m_cn = re.match(r"^\s*-\s+Change\s+(\d+):", l.strip())
            if m_cn and in_depends:
                deps[n].append(int(m_cn.group(1)))
            if m_cn and in_blocks:
                deps.setdefault(int(m_cn.group(1)), [])
                deps[int(m_cn.group(1))].append(n)

    dup_change_ids = sorted({x for x in change_ids if change_ids.count(x) > 1})
    if dup_change_ids:
        errors.append({"type": "id", "message": "Duplicate change IDs", "ids": dup_change_ids})

    if summary_counts is not None and change_nums:
        if summary_counts["total"] != len(change_nums):
            errors.append({"type": "structure", "message": "Total Changes must equal number of change entries", "total": summary_counts["total"], "entries": len(change_nums)})
        st_map = {"✅ COMPLETED": "completed", "🔄 IN_PROGRESS": "in_progress", "⏳ NOT_STARTED": "not_started"}
        counts = {"completed": 0, "in_progress": 0, "not_started": 0}
        for _, _, _, block in change_blocks:
            v = _get_field_value(block, "Status")
            if v in st_map:
                counts[st_map[v]] += 1
        if any(counts[k] != summary_counts[k] for k in counts.keys()):
            errors.append({"type": "structure", "message": "Summary status counts must match statuses of change entries", "summary": summary_counts, "found": counts})

    def _has_cycle(graph: Dict[int, List[int]]) -> bool:
        visiting: set = set()
        visited: set = set()

        def dfs(v: int) -> bool:
            if v in visited:
                return False
            if v in visiting:
                return True
            visiting.add(v)
            for nxt in graph.get(v, []):
                if dfs(nxt):
                    return True
            visiting.remove(v)
            visited.add(v)
            return False

        for v in graph.keys():
            if dfs(v):
                return True
        return False

    if deps and _has_cycle(deps):
        errors.append({"type": "content", "message": "Dependency graph contains a cycle"})

    if not skip_fs_checks and feature_root is not None:
        dp = feature_root / "DESIGN.md"
        dt, derr = load_text(dp)
        if derr:
            errors.append({"type": "cross", "message": derr})
        else:
            design_req_ids = sorted(set(FEATURE_REQ_ID_RE.findall(dt or "")))
            design_req_full = sorted(set(re.findall(r"\bfdd-[a-z0-9-]+-feature-[a-z0-9-]+-req-[a-z0-9-]+\b", dt or "")))
            if feature_slug is not None:
                design_req_full = [x for x in design_req_full if f"-feature-{feature_slug}-" in x]
            implemented = sorted(set([rid for ids in implements_by_change.values() for rid in ids]))
            unknown = sorted([x for x in implemented if x not in set(design_req_full)])
            if unknown:
                errors.append({"type": "cross", "message": "CHANGES implements unknown requirement IDs (not found in feature DESIGN.md)", "ids": unknown})
            missing = sorted([x for x in design_req_full if x not in set(implemented)])
            if design_req_full and missing:
                errors.append({"type": "cross", "message": "Not all feature requirements are covered by changes", "missing": missing})

    # FDL Coverage Validation: Check if CHANGES.md references all FDL scopes (flows/algos/states/tests) from DESIGN.md
    if feature_root is not None and not skip_fs_checks:
        design_path = feature_root / "DESIGN.md"
        if design_path.exists():
            try:
                design_text = design_path.read_text(encoding="utf-8")
                design_fdl = extract_fdl_instructions(design_text)
                
                # Validate FDL scope coverage in CHANGES.md
                fdl_coverage_errors = validate_fdl_coverage(artifact_text, design_fdl)
                errors.extend(fdl_coverage_errors)
                
                # Validate FDL code implementation (tags present)
                fdl_code_errors = validate_fdl_code_implementation(feature_root, design_fdl)
                errors.extend(fdl_code_errors)
                
                # Reverse validation: check tags in code are marked [x] in DESIGN
                fdl_reverse_errors = validate_fdl_code_to_design(feature_root, design_text)
                errors.extend(fdl_reverse_errors)
                
                # Validate FDL completion (if feature is marked COMPLETED)
                fdl_completion_errors = validate_fdl_completion(artifact_text, design_fdl)
                errors.extend(fdl_completion_errors)
            except Exception:
                pass

    passed = (len(errors) == 0) and (len(placeholders) == 0)
    return {
        "required_section_count": 0,
        "missing_sections": [],
        "placeholder_hits": placeholders,
        "status": "PASS" if passed else "FAIL",
        "errors": errors,
    }


def _normalize_feature_relpath(path: str) -> str:
    p = path.strip()
    if not p.endswith("/"):
        p = p + "/"
    return p


def _extract_feature_links(text: str) -> List[str]:
    links: List[str] = []
    for _, target in LINK_RE.findall(text):
        t = target.strip()
        if not t.startswith("feature-"):
            continue
        links.append(_normalize_feature_relpath(t))
    return links


def _extract_id_list(field_block: Dict[str, object]) -> List[str]:
    raw: List[str] = []
    inline = str(field_block["value"]).strip()
    if inline:
        raw.extend([p.strip() for p in inline.split(",") if p.strip()])
    for line in list(field_block["tail"]):
        m = re.match(r"^\s*[-*]\s+(.+?)\s*$", line)
        if not m:
            continue
        raw.append(m.group(1).strip())

    ids: List[str] = []
    for item in raw:
        cleaned = item.strip().strip("`")
        if cleaned:
            ids.append(cleaned)
    return ids


def _find_disallowed_link_notation(text: str) -> List[Dict[str, object]]:
    hits: List[Dict[str, object]] = []
    for idx, line in enumerate(text.splitlines(), start=1):
        if DISALLOWED_LINK_TOKEN_RE.search(line):
            hits.append({"line": idx, "text": line.strip()})
    return hits


def _find_html_comment_placeholders(text: str) -> List[Dict[str, object]]:
    hits: List[Dict[str, object]] = []
    for m in HTML_COMMENT_RE.finditer(text):
        frag = m.group(0)
        if PLACEHOLDER_RE.search(frag):
            pre = text[: m.start()].splitlines()
            line_no = len(pre) + 1
            hits.append({"line": line_no, "text": frag.strip()})
    return hits


def _find_brace_placeholders(text: str) -> List[Dict[str, object]]:
    hits: List[Dict[str, object]] = []
    in_code = False
    for idx, line in enumerate(text.splitlines(), start=1):
        if line.strip().startswith("```"):
            in_code = not in_code
            continue
        if in_code:
            continue
        line_wo_inline_code = re.sub(r"`[^`]*`", "", line)
        if BRACE_PLACEHOLDER_RE.search(line_wo_inline_code):
            hits.append({"line": idx, "text": line.strip()})
    return hits


def _parse_size_hard_limit(requirements_path: Path) -> Optional[int]:
    try:
        rt = requirements_path.read_text(encoding="utf-8")
    except Exception:
        return None
    m = SIZE_HARD_LIMIT_RE.search(rt)
    if not m:
        return None
    try:
        return int(m.group(1))
    except Exception:
        return None


def _common_checks(
    *,
    artifact_text: str,
    artifact_path: Path,
    requirements_path: Path,
    skip_fs_checks: bool,
) -> Tuple[List[Dict[str, object]], List[Dict[str, object]]]:
    errors: List[Dict[str, object]] = []
