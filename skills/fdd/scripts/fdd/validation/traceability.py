"""
FDD Validator - Code Traceability

Code scanning for FDD tags, block validation, exclusion mechanism.
"""

import re
from pathlib import Path
from typing import Dict, List, Optional, Set, Tuple


from ..utils import load_text, extract_backticked_ids
from ..validation.fdl import extract_fdl_instructions, extract_scope_references_from_changes
from ..validation.artifacts import validate_feature_design, validate_feature_changes
from ..constants import (
    FDD_BEGIN_LINE_RE,
    FDD_END_LINE_RE,
    UNWRAPPED_INST_TAG_RE,
    NO_FDD_BLOCK_BEGIN_RE,
    NO_FDD_BLOCK_END_RE,
    FDD_TAG_CHANGE_RE,
    FDD_TAG_FLOW_RE,
    FDD_TAG_ALGO_RE,
    FDD_TAG_STATE_RE,
    FDD_TAG_REQ_RE,
    FDD_TAG_TEST_RE,
    SCOPE_ID_BY_KIND_RE,
    FDL_STEP_LINE_RE,
    ADR_ID_RE,
)


def compute_excluded_line_ranges(text: str) -> List[Tuple[int, int]]:
    """
    Compute line ranges (0-indexed, inclusive) that should be excluded from FDD scanning.
    Ranges are defined by !no-fdd-begin and !no-fdd-end markers.
    Unmatched !no-fdd-begin markers exclude everything to end of file.
    Returns list of (start_line, end_line) tuples.
    """
    ranges: List[Tuple[int, int]] = []
    lines = text.splitlines()
    stack: List[int] = []
    
    for i, line in enumerate(lines):
        if NO_FDD_BLOCK_BEGIN_RE.search(line):
            stack.append(i)
        elif NO_FDD_BLOCK_END_RE.search(line):
            if stack:
                start = stack.pop()
                ranges.append((start, i))
    
    # Handle unmatched !no-fdd-begin markers: exclude to EOF
    for start in stack:
        ranges.append((start, len(lines) - 1))
    
    return ranges


def is_line_excluded(line_idx: int, excluded_ranges: List[Tuple[int, int]]) -> bool:
    """Check if line index is within any excluded range (0-indexed)."""
    for start, end in excluded_ranges:
        if start <= line_idx <= end:
            return True
    return False


def is_effective_code_line(line: str) -> bool:
    """
    Check if line contains effective code (not just comments or whitespace).
    Used to determine if fdd-begin/fdd-end block is empty.
    """
    s = line.strip()
    if not s:
        return False
    if s.startswith("//"):
        return False
    if s.startswith("#"):
        return False
    if s.startswith("--"):
        return False
    if s.startswith("/*"):
        return False
    if s.startswith("*/"):
        return False
    if s.startswith("*") and not s.startswith("**"):
        return False
    return True


def empty_fdd_tag_blocks_in_text(text: str) -> List[Dict[str, object]]:
    """
    Find malformed fdd-begin/fdd-end blocks in text.
    
    Returns list of issues:
    - empty_block: Block has no effective code between begin/end
    - begin_without_end: fdd-begin without matching fdd-end
    - end_without_begin: fdd-end without matching fdd-begin
    """
    issues: List[Dict[str, object]] = []
    lines = text.splitlines()
    excluded_ranges = compute_excluded_line_ranges(text)

    stack: List[Tuple[str, int]] = []
    for i, line in enumerate(lines):
        if is_line_excluded(i, excluded_ranges):
            continue
        
        line_for_scan = re.sub(r"`[^`]*`", "", line)

        mb = FDD_BEGIN_LINE_RE.search(line_for_scan)
        if mb:
            tag = mb.group(1)
            if ":inst-" in tag:
                stack.append((tag, i))
            continue

        me = FDD_END_LINE_RE.search(line_for_scan)
        if not me:
            continue
        end_tag = me.group(1)
        if ":inst-" not in end_tag:
            continue
        if not stack:
            issues.append({"type": "end_without_begin", "tag": end_tag, "end_line": i + 1})
            continue
        start_tag, start_idx = stack[-1]
        if start_tag != end_tag:
            issues.append(
                {
                    "type": "end_without_begin",
                    "tag": end_tag,
                    "end_line": i + 1,
                    "expected": start_tag,
                    "expected_begin_line": start_idx + 1,
                }
            )
            continue
        stack.pop()

        has_code = any(is_effective_code_line(lines[j]) for j in range(start_idx + 1, i) if not is_line_excluded(j, excluded_ranges))
        if not has_code:
            issues.append(
                {
                    "type": "empty_block",
                    "tag": start_tag,
                    "begin_line": start_idx + 1,
                    "end_line": i + 1,
                }
            )

    for tag, start_idx in stack:
        issues.append({"type": "begin_without_end", "tag": tag, "begin_line": start_idx + 1})

    return issues


def paired_inst_tags_in_text(text: str) -> Set[str]:
    """
    Extract all properly paired instruction tags from text.
    Returns set of tags like "fdd-project-feature-x-flow-y:ph-1:inst-step"
    """
    tags: Set[str] = set()
    lines = text.splitlines()
    excluded_ranges = compute_excluded_line_ranges(text)

    stack: List[str] = []
    for i, line in enumerate(lines):
        if is_line_excluded(i, excluded_ranges):
            continue
        
        line_for_scan = re.sub(r"`[^`]*`", "", line)

        mb = FDD_BEGIN_LINE_RE.search(line_for_scan)
        if mb:
            tag = mb.group(1)
            if ":inst-" in tag:
                stack.append(tag)
            continue

        me = FDD_END_LINE_RE.search(line_for_scan)
        if not me:
            continue
        end_tag = me.group(1)
        if ":inst-" not in end_tag:
            continue
        if not stack:
            continue
        start_tag = stack[-1]
        if start_tag != end_tag:
            continue
        stack.pop()
        tags.add(start_tag)

    return tags


def unwrapped_inst_tag_hits_in_text(text: str) -> List[Dict[str, object]]:
    """
    Find instruction tags that are NOT wrapped in fdd-begin/fdd-end blocks.
    These should be wrapped for proper traceability.
    
    Returns list of {tag, line} dicts.
    """
    hits: List[Dict[str, object]] = []
    excluded_ranges = compute_excluded_line_ranges(text)
    
    for i, line in enumerate(text.splitlines()):
        if is_line_excluded(i, excluded_ranges):
            continue
        
        line_for_scan = re.sub(r"`[^`]*`", "", line)
        if FDD_BEGIN_LINE_RE.search(line_for_scan) or FDD_END_LINE_RE.search(line_for_scan):
            continue
        for m in UNWRAPPED_INST_TAG_RE.finditer(line_for_scan):
            hits.append({"tag": m.group(1), "line": i + 1})
    return hits


def code_tag_hits(text: str) -> Dict[str, List[Tuple[str, str]]]:
    """
    Extract all @fdd-* tags from text (change, flow, algo, state, req, test).
    
    Returns dict mapping tag kind to list of (scope_id, phase) tuples.
    """
    hits: Dict[str, List[Tuple[str, str]]] = {
        "change": [],
        "flow": [],
        "algo": [],
        "state": [],
        "req": [],
        "test": [],
    }
    
    excluded_ranges = compute_excluded_line_ranges(text)
    
    # Remove backticked content and filter out lines in exclusion blocks
    filtered_lines = []
    for i, line in enumerate(text.splitlines()):
        if is_line_excluded(i, excluded_ranges):
            continue
        filtered_lines.append(line)
    
    filtered_text = "\n".join(filtered_lines)
    filtered_text = re.sub(r"`[^`]*`", "", filtered_text)
    
    for rid, ph in FDD_TAG_CHANGE_RE.findall(filtered_text):
        hits["change"].append((rid, ph))
    for rid, ph in FDD_TAG_FLOW_RE.findall(filtered_text):
        hits["flow"].append((rid, ph))
    for rid, ph in FDD_TAG_ALGO_RE.findall(filtered_text):
        hits["algo"].append((rid, ph))
    for rid, ph in FDD_TAG_STATE_RE.findall(filtered_text):
        hits["state"].append((rid, ph))
    for rid, ph in FDD_TAG_REQ_RE.findall(filtered_text):
        hits["req"].append((rid, ph))
    for rid, ph in FDD_TAG_TEST_RE.findall(filtered_text):
        hits["test"].append((rid, ph))
    return hits


def iter_code_files(root: Path) -> List[Path]:
    """
    Iterate code files for traceability scanning.
    
    Scans: .rs, .py, .ts, .tsx, .js, .go, .java, .cs, .sql, .md
    For .md files: only includes files that contain FDD tags.
    """
    exts = {".rs", ".py", ".ts", ".tsx", ".js", ".go", ".java", ".cs", ".sql", ".md"}
    files: List[Path] = []
    for p in root.rglob("*"):
        if not p.is_file():
            continue
        if p.suffix.lower() not in exts:
            continue
        # For .md: scan ONLY when file contains explicit FDD tags.
        # This avoids scanning unrelated documentation while allowing traceability
        # for tagged core-methodology docs/workflows.
        if p.suffix.lower() == ".md":
            try:
                head = p.read_text(encoding="utf-8", errors="ignore")[:20000]
            except Exception:
                continue
            if ("fdd-begin" not in head) and ("fdd-end" not in head) and ("@fdd-" not in head):
                continue
        files.append(p)
    return files


def extract_scope_ids(line: str, kind: str) -> List[str]:
    """Extract scope IDs of specific kind from line."""
    pat = SCOPE_ID_BY_KIND_RE.get(kind)
    if pat is None:
        return []
    # Use finditer and group(0) to get full match, not capture groups
    return [m.group(0) for m in pat.finditer(line)]
def validate_codebase_traceability(
    artifact_dir: Path,
    *,
    feature_design_path: Optional[Path] = None,
    feature_changes_path: Optional[Path] = None,
    scan_root_override: Optional[Path] = None,
    skip_fs_checks: bool = False,
) -> Dict[str, object]:
    errors: List[Dict[str, object]] = []

    if not artifact_dir.exists() or not artifact_dir.is_dir():
        return {
            "required_section_count": 0,
            "missing_sections": [],
            "placeholder_hits": [],
            "status": "FAIL",
            "errors": [{"type": "file", "message": "Directory not found", "path": str(artifact_dir)}],
        }

    feature_dir = artifact_dir

    dp = feature_design_path or (feature_dir / "DESIGN.md")
    if not dp.exists() or not dp.is_file():
        errors.append({"type": "cross", "message": "Feature DESIGN.md not found for codebase traceability", "path": str(dp)})

    cp = feature_changes_path or (feature_dir / "CHANGES.md")
    if (not cp.exists() or not cp.is_file()) and not skip_fs_checks:
        latest = latest_archived_changes(feature_dir)
        if latest is not None:
            cp = latest

    design_text, derr = load_text(dp)
    if derr:
        errors.append({"type": "cross", "message": derr})
        design_text = ""
    changes_text: str = ""
    if cp is not None and cp.exists() and cp.is_file():
        changes_text, _ = load_text(cp)
        changes_text = changes_text or ""

    artifacts_validation: Dict[str, object] = {
        "feature_design": None,
        "feature_changes": None,
    }

    if dp.exists() and dp.is_file():
        drep, crep = _validate_feature_artifacts_for_traceability(
            feature_design_path=dp,
            feature_changes_path=cp if (cp is not None and cp.exists() and cp.is_file()) else None,
            skip_fs_checks=skip_fs_checks,
        )
        artifacts_validation["feature_design"] = _summarize_validation_report(drep)
        if crep is not None:
            artifacts_validation["feature_changes"] = _summarize_validation_report(crep)

        if (drep.get("status") != "PASS") or (crep is not None and crep.get("status") != "PASS"):
            return {
                "required_section_count": 0,
                "missing_sections": [],
                "placeholder_hits": [],
                "status": "FAIL",
                "errors": errors,
                "traceability": {
                    "feature_dir": str(feature_dir),
                    "scan_root": str(scan_root_override or feature_dir),
                    "feature_design": str(dp),
                    "feature_changes": str(cp) if cp else None,
                    "scanned_file_count": 0,
                    "artifact_validation": artifacts_validation,
                },
            }

    # Expected IDs to be present in code markers
    expected_scope_ids: Dict[str, set] = {
        "flow": set(),
        "algo": set(),
        "state": set(),
        "req": set(),
        "test": set(),
        "change": set(),
    }
    expected_inst_tags: set = set()

    # DESIGN scopes marked implemented via checkbox
    for line in (design_text or "").splitlines():
        if not re.match(r"^\s*[-*]\s+\[x\]\s+\*\*ID\*\*:\s+", line, re.IGNORECASE):
            continue
        for fid in extract_scope_ids(line, "flow"):
            expected_scope_ids["flow"].add(fid)
        for aid in extract_scope_ids(line, "algo"):
            expected_scope_ids["algo"].add(aid)
        for sid in extract_scope_ids(line, "state"):
            expected_scope_ids["state"].add(sid)
        for rid in extract_scope_ids(line, "req"):
            expected_scope_ids["req"].add(rid)
        for tid in extract_scope_ids(line, "test"):
            expected_scope_ids["test"].add(tid)

    # FDL instruction-level tags from implemented ([x]) step lines.
    current_scope: Optional[str] = None
    for line in (design_text or "").splitlines():
        if "**ID**:" in line and re.match(r"^\s*[-*]\s+\[[ xX]\]\s+\*\*ID\*\*:\s+", line):
            # Prefer algorithm IDs, then flow/state/test
            scope_id = None
            for kind in ("algo", "flow", "state", "test"):
                ids = extract_scope_ids(line, kind)
                if ids:
                    scope_id = ids[0]
                    break
            current_scope = scope_id
            continue

        if "[x]" not in line and "[X]" not in line:
            continue
        if not FDL_STEP_LINE_RE.match(line):
            continue

        m_ph = re.search(r"`ph-(\d+)`", line)
        m_inst = re.search(r"`(inst-[a-z0-9-]+)`\s*$", line.strip())
        if not (m_ph and m_inst and current_scope):
            continue
        expected_inst_tags.add(f"{current_scope}:ph-{m_ph.group(1)}:{m_inst.group(1)}")

    # CHANGES completed changes -> expect change tags in code
    for m in re.finditer(r"^##\s+Change\s+\d+:.*$", changes_text, re.MULTILINE):
        pass
    if changes_text:
        # naive split by change headings
        blocks = re.split(r"^##\s+Change\s+\d+:.*$", changes_text, flags=re.MULTILINE)
        headings = re.findall(r"^##\s+Change\s+\d+:.*$", changes_text, flags=re.MULTILINE)
        for i, head in enumerate(headings):
            body = blocks[i + 1] if i + 1 < len(blocks) else ""
            m_id = re.search(r"\*\*ID\*\*:\s*`([^`]+)`", body)
            m_status = re.search(r"\*\*Status\*\*:\s*(.+)$", body, re.MULTILINE)
            if not (m_id and m_status):
                continue
            if m_status.group(1).strip() != "✅ COMPLETED":
                continue
            expected_scope_ids["change"].add(m_id.group(1).strip())

    # Scan code - always from project root to include requirements/ and other shared files
    if scan_root_override:
        scan_root = scan_root_override
    else:
        # Find project root (parent of architecture/)
        scan_root = feature_dir
        p = feature_dir
        while p != p.parent:
            if p.name == "architecture":
                scan_root = p.parent
                break
            p = p.parent
    
    scanned_files = iter_code_files(scan_root)
    found_scope_ids: Dict[str, set] = {k: set() for k in expected_scope_ids.keys()}
    found_inst_tags: set = set()

    for fp in scanned_files:
        try:
            txt = fp.read_text(encoding="utf-8", errors="ignore")
        except Exception:
            continue

        try:
            rel_fp = fp.relative_to(scan_root).as_posix()
        except Exception:
            rel_fp = fp.as_posix()

        hits = code_tag_hits(txt)

        paired_inst_tags = paired_inst_tags_in_text(txt)
        unwrapped_inst_hits = unwrapped_inst_tag_hits_in_text(txt)

        empty_blocks = empty_fdd_tag_blocks_in_text(txt)
        if empty_blocks:
            for eb in empty_blocks:
                msg = "Invalid fdd-begin/fdd-end pairing"
                if eb.get("type") == "empty_block":
                    msg = "Empty fdd-begin/fdd-end block"
                elif eb.get("type") == "begin_without_end":
                    msg = "fdd-begin without matching fdd-end"
                elif eb.get("type") == "end_without_begin":
                    msg = "fdd-end without matching fdd-begin"
                errors.append({"type": "code_tag", "message": msg, "path": rel_fp, **eb})
        for k in ("change", "flow", "algo", "state", "req", "test"):
            for rid, _ph in hits[k]:
                found_scope_ids[k].add(rid)

        found_inst_tags.update(expected_inst_tags.intersection(paired_inst_tags))

        for uh in unwrapped_inst_hits:
            tag = uh.get("tag")
            if not tag:
                continue
            if tag in expected_inst_tags and tag not in paired_inst_tags:
                errors.append(
                    {
                        "type": "code_tag",
                        "message": "Instruction tag must be wrapped in fdd-begin/fdd-end",
                        "path": rel_fp,
                        "tag": tag,
                        "line": uh.get("line"),
                    }
                )

    missing_scope: Dict[str, List[str]] = {}
    for k, exp in expected_scope_ids.items():
        miss = sorted([x for x in exp if x not in found_scope_ids.get(k, set())])
        if miss:
            missing_scope[k] = miss
    missing_inst = sorted([x for x in expected_inst_tags if x not in found_inst_tags])

    # PASS only if no tag errors AND no missing implementations
    # Missing = marked [x] in DESIGN but not found in code = documentation/code mismatch
    passed = (len(errors) == 0) and (len(missing_scope) == 0) and (len(missing_inst) == 0)
    return {
        "required_section_count": 0,
        "missing_sections": [],
        "placeholder_hits": [],
        "status": "PASS" if passed else "FAIL",
        "errors": errors,
        "traceability": {
            "feature_dir": str(feature_dir),
            "scan_root": str(scan_root),
            "feature_design": str(dp) if dp else None,
            "feature_changes": str(cp) if cp else None,
            "scanned_file_count": len(scanned_files),
            "artifact_validation": artifacts_validation,
            "expected": {
                "scopes": {k: sorted(list(v)) for k, v in expected_scope_ids.items()},
                "instruction_tags": sorted(list(expected_inst_tags)),
            },
            "found": {
                "scopes": {k: sorted(list(v)) for k, v in found_scope_ids.items()},
                "instruction_tags": sorted(list(found_inst_tags)),
            },
            "missing": {
                "scopes": missing_scope,
                "instruction_tags": missing_inst,
            },
        },
    }


def validate_code_root_traceability(
    code_root: Path,
    *,
    feature_slugs: Optional[List[str]] = None,
    skip_fs_checks: bool = False,
) -> Dict[str, object]:
    errors: List[Dict[str, object]] = []

    if not code_root.exists() or not code_root.is_dir():
        return {
            "required_section_count": 0,
            "missing_sections": [],
            "placeholder_hits": [],
            "status": "FAIL",
            "errors": [{"type": "file", "message": "Directory not found", "path": str(code_root)}],
        }

    features_dir = code_root / "architecture" / "features"
    if not features_dir.exists() or not features_dir.is_dir():
        errors.append(
            {
                "type": "file",
                "message": "Missing architecture/features directory under code root",
                "expected": str(features_dir),
            }
        )

    wanted: Optional[set] = None
    if feature_slugs:
        wanted = set()
        for s in feature_slugs:
            ss = s.strip()
            if not ss:
                continue
            if ss.startswith("feature-"):
                ss = ss[len("feature-") :]
            wanted.add(ss)

    feature_dirs: List[Path] = []
    if features_dir.exists() and features_dir.is_dir():
        for fd in sorted([p for p in features_dir.iterdir() if p.is_dir() and p.name.startswith("feature-")]):
            slug = fd.name[len("feature-") :]
            if wanted is not None and slug not in wanted:
                continue
            feature_dirs.append(fd)

    feature_reports: List[Dict[str, object]] = []
    for fd in feature_dirs:
        rep = validate_codebase_traceability(
            fd,
            scan_root_override=code_root,
            skip_fs_checks=skip_fs_checks,
        )
        feature_reports.append({"feature_dir": str(fd), "status": rep.get("status"), "traceability": rep.get("traceability")})

    passed = all((fr.get("status") == "PASS") for fr in feature_reports)

    return {
        "required_section_count": 0,
        "missing_sections": [],
        "placeholder_hits": [],
        "status": "PASS" if passed else "FAIL",
        "errors": errors,
        "code_root": str(code_root),
        "feature_count": len(feature_dirs),
        "feature_reports": feature_reports,
    }


def _parse_business_model(text: str) -> Tuple[set, Dict[str, set], set]:
    actor_ids: set = set(ACTOR_ID_RE.findall(text))
    capability_to_actors: Dict[str, set] = {}
    usecase_ids: set = set(USECASE_ID_RE.findall(text))

    lines = text.splitlines()
    current_cap: Optional[str] = None
    for line in lines:
        if line.strip().startswith("#### "):
            current_cap = None
        if "**ID**:" in line:
            for cid in extract_backticked_ids(line, CAPABILITY_ID_RE):
                current_cap = cid
                capability_to_actors.setdefault(cid, set())
        if current_cap and "**Actors**:" in line:
            for aid in extract_backticked_ids(line, ACTOR_ID_RE):
                capability_to_actors[current_cap].add(aid)

    return actor_ids, capability_to_actors, usecase_ids


ADR_HEADING_RE = re.compile(r"^##\s+(ADR-(\d{4})):\s+(.+?)\s*$")
ADR_DATE_RE = re.compile(r"\*\*Date\*\*:\s*(\d{4}-\d{2}-\d{2})")
ADR_STATUS_RE = re.compile(r"\*\*Status\*\*:\s*(Proposed|Accepted|Deprecated|Superseded)")
ADR_NUM_RE = re.compile(r"\bADR-(\d{4})\b")
FDD_ADR_NUM_RE = re.compile(r"\bfdd-[a-z0-9-]+-adr-(\d{4})\b")
ADR_ID_RE = re.compile(r"\bfdd-[a-z0-9-]+-adr-[a-z0-9-]+\b")


def _parse_adr_index(text: str) -> Tuple[List[Dict[str, object]], List[Dict[str, object]]]:
    issues: List[Dict[str, object]] = []
    adrs: List[Dict[str, object]] = []
    lines = text.splitlines()
    for idx, line in enumerate(lines, start=1):
        m = ADR_HEADING_RE.match(line.strip())
        if not m:
            continue
        adrs.append({"line": idx, "adr": m.group(1), "num": int(m.group(2)), "title": m.group(3)})

    if not adrs:
        issues.append({"type": "structure", "message": "No ADR entries found"})
        return [], issues

    nums = [a["num"] for a in adrs]
    expected = list(range(1, len(nums) + 1))
    if nums != expected:
        issues.append({"type": "structure", "message": "ADR numbers must be sequential starting at ADR-0001 with no gaps", "found": nums})
    if 1 not in nums:
        issues.append({"type": "structure", "message": "ADR-0001 must exist"})

    ids = [a["adr"] for a in adrs]
    dup = sorted({x for x in ids if ids.count(x) > 1})
    if dup:
        issues.append({"type": "structure", "message": "Duplicate ADR numbers", "adrs": dup})

    # Extract canonical FDD ADR IDs (required for cross-artifact references)
    starts = [a["line"] - 1 for a in adrs]
    for i, start0 in enumerate(starts):
        end0 = starts[i + 1] if i + 1 < len(starts) else len(lines)
        block = lines[start0:end0]
        block_text = "\n".join(block)
        id_line = next((l for l in block if "**ID**:" in l), None)
        fdd_id: Optional[str] = None
        if id_line is not None:
            bt = extract_backticked_ids(id_line, ADR_ID_RE)
            if bt:
                fdd_id = bt[0]
        if fdd_id is None:
            issues.append({"type": "structure", "message": "ADR missing or invalid **ID** line", "adr": adrs[i]["adr"], "line": adrs[i]["line"]})
        else:
            adrs[i]["id"] = fdd_id

    fdd_ids = [a.get("id") for a in adrs if a.get("id")]
    dup_fdd = sorted({x for x in fdd_ids if fdd_ids.count(x) > 1})
    if dup_fdd:
        issues.append({"type": "structure", "message": "Duplicate ADR IDs", "ids": dup_fdd})

    return adrs, issues


def latest_archived_changes(feature_dir: Path) -> Optional[Path]:
    """Find the latest archived CHANGES file."""
    ap = feature_dir / "archive"
    if not ap.exists() or not ap.is_dir():
        return None
    candidates = sorted(ap.glob("CHANGES-*.md"), reverse=True)
    return candidates[0] if candidates else None


def _validate_feature_artifacts_for_traceability(
    *,
    feature_design_path: Path,
    feature_changes_path: Optional[Path],
    skip_fs_checks: bool,
) -> Tuple[Dict[str, object], Optional[Dict[str, object]]]:
    """Validate feature artifacts for traceability checking."""
    from ..utils import detect_requirements
    from ..validation.artifacts import validate
    
    dk, dr = detect_requirements(feature_design_path)
    drep = validate(
        feature_design_path,
        dr,
        dk,
        skip_fs_checks=skip_fs_checks,
    )
    drep["artifact_kind"] = dk

    crep: Optional[Dict[str, object]] = None
    if feature_changes_path is not None and feature_changes_path.exists() and feature_changes_path.is_file():
        ck, cr = detect_requirements(feature_changes_path)
        crep = validate(
            feature_changes_path,
            cr,
            ck,
            design_path=feature_design_path,
            skip_fs_checks=skip_fs_checks,
        )
        crep["artifact_kind"] = ck

    return drep, crep


def _summarize_validation_report(report: Dict[str, object], *, max_errors: int = 50) -> Dict[str, object]:
    """Summarize validation report for traceability output."""
    errs = list(report.get("errors", []) or [])
    ph = list(report.get("placeholder_hits", []) or [])
    return {
        "status": report.get("status"),
        "error_count": len(errs),
        "placeholder_count": len(ph),
        "errors": errs[:max_errors],
        "placeholder_hits": ph[:max_errors],
    }
