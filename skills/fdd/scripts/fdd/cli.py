"""
FDD Validator - CLI Entry Point

Command-line interface for the FDD validation tool.
"""

import sys
import os
import json
import re
import fnmatch
import argparse
from pathlib import Path
from typing import List, Optional, Dict, Set, Tuple

from .validation.artifacts import validate
from .validation.traceability import (
    validate_codebase_traceability,
    validate_code_root_traceability,
)
from .validation.fdl import validate_fdl_completion
from .utils import (
    detect_requirements,
    load_text,
    parse_required_sections,
    split_by_section_letter,
)
from . import constants


# =============================================================================
def _cmd_validate(argv: List[str]) -> int:
    """
    Validation command handler - wraps validate() function.
    """
    p = argparse.ArgumentParser(prog="validate")
    p.add_argument("--artifact", required=True, help="Path to artifact to validate")
    p.add_argument("--requirements", default=None, help="Path to requirements file (optional, auto-detected)")
    p.add_argument("--design", default=None, help="Path to DESIGN.md for cross-references")
    p.add_argument("--business", default=None, help="Path to BUSINESS.md for cross-references")
    p.add_argument("--adr", default=None, help="Path to ADR.md for cross-references")
    p.add_argument("--skip-fs-checks", action="store_true", help="Skip filesystem checks")
    p.add_argument("--output", default=None, help="Write report to file instead of stdout")
    p.add_argument("--features", default=None, help="Comma-separated feature slugs for code-root traceability")
    args = p.parse_args(argv)

    artifact_path = Path(args.artifact).resolve()

    if artifact_path.is_dir():
        # Backwards-compatible: feature directory mode (artifact contains DESIGN.md).
        if (artifact_path / "DESIGN.md").exists():
            if args.features:
                raise SystemExit("--features is only supported when --artifact is a code root directory")
            report = validate_codebase_traceability(
                artifact_path,
                feature_design_path=Path(args.design).resolve() if args.design else None,
                feature_changes_path=None,
                skip_fs_checks=bool(args.skip_fs_checks),
            )
            report["artifact_kind"] = "codebase-trace"
        else:
            slugs: Optional[List[str]] = None
            if args.features:
                slugs = [x.strip() for x in str(args.features).split(",") if x.strip()]
            report = validate_code_root_traceability(
                artifact_path,
                feature_slugs=slugs,
                skip_fs_checks=bool(args.skip_fs_checks),
            )
            report["artifact_kind"] = "codebase-trace"

        out = json.dumps(report, indent=2, ensure_ascii=False) + "\n"
        if args.output:
            Path(args.output).write_text(out, encoding="utf-8")
        else:
            print(out, end="")

        return 0 if report["status"] == "PASS" else 2

    elif args.requirements:
        requirements_path = Path(args.requirements).resolve()
        artifact_kind = "custom"
    else:
        artifact_kind, requirements_path = detect_requirements(artifact_path)

    if not requirements_path.exists() or not requirements_path.is_file():
        raise SystemExit(f"Requirements file not found: {requirements_path}")

    design_path = Path(args.design).resolve() if args.design else None
    business_path = Path(args.business).resolve() if args.business else None
    adr_path = Path(args.adr).resolve() if args.adr else None

    report = validate(
        artifact_path,
        requirements_path,
        artifact_kind,
        design_path=design_path,
        business_path=business_path,
        adr_path=adr_path,
        skip_fs_checks=bool(args.skip_fs_checks),
    )
    report["artifact_kind"] = artifact_kind

    out = json.dumps(report, indent=2, ensure_ascii=False) + "\n"

    if args.output:
        Path(args.output).write_text(out, encoding="utf-8")
    else:
        print(out, end="")

    return 0 if report["status"] == "PASS" else 2


# =============================================================================
# SEARCH COMMAND HELPERS
# =============================================================================

def _parse_trace_query(raw: str) -> Tuple[str, Optional[str], Optional[str]]:
    s = str(raw).strip()
    if s.startswith("@fdd-"):
        parts = s.split(":", 1)
        if len(parts) == 2:
            s = parts[1]

    base = s
    phase: Optional[str] = None
    inst: Optional[str] = None

    if ":" in s:
        segs = s.split(":")
        base = segs[0]
        for seg in segs[1:]:
            if seg.startswith("ph-") and phase is None:
                phase = seg
                continue
            if seg.startswith("inst-") and inst is None:
                inst = seg
                continue

    return base, phase, inst


def _compile_trace_regex(base: str, phase: Optional[str], inst: Optional[str]) -> re.Pattern:
    pat = re.escape(base)
    if phase:
        ph_pat = rf"(?:\b{re.escape(phase)}\b|`{re.escape(phase)}`|:{re.escape(phase)}\b)"
        pat += r".*" + ph_pat
    if inst:
        inst_pat = rf"(?:\b{re.escape(inst)}\b|`{re.escape(inst)}`|:{re.escape(inst)}\b)"
        pat += r".*" + inst_pat
    return re.compile(pat)


def _token_index(line: str, token: str) -> int:
    candidates = [token, f"`{token}`", f":{token}"]
    best = -1
    for c in candidates:
        j = line.find(c)
        if j >= 0 and (best < 0 or j < best):
            best = j
    return best


def _match_phase_inst_in_line(line: str, *, phase: Optional[str], inst: Optional[str]) -> Optional[Tuple[str, int]]:
    if phase is None and inst is None:
        return None
    if phase is not None:
        ph_i = _token_index(line, phase)
        if ph_i < 0:
            return None
    else:
        ph_i = -1

    if inst is not None:
        inst_i = _token_index(line, inst)
        if inst_i < 0:
            return None
        if ph_i >= 0 and inst_i < ph_i:
            return None
        return "inst", inst_i

    return "phase", ph_i


def _extract_ids(lines: List[str], *, with_cols: bool = False) -> List[Dict[str, object]]:
    """
    Extract FDD and ADR IDs from lines.
    
    Args:
        lines: Text lines to search
        with_cols: If True, include column positions in results
    
    Returns:
        List of dicts with 'id', 'line', 'kind', and optionally 'col'
    """
    out: List[Dict[str, object]] = []
    fdd_re = re.compile(r"\b(fdd-[a-z0-9][a-z0-9-]+)\b")
    adr_re = re.compile(r"\b(ADR-\d{4})\b")

    for i, line in enumerate(lines, start=1):
        for m in fdd_re.finditer(line):
            hit = {"id": m.group(1), "line": i, "kind": "fdd"}
            if with_cols:
                hit["col"] = m.start(1) + 1
            out.append(hit)
        for m in adr_re.finditer(line):
            hit = {"id": m.group(1), "line": i, "kind": "adr"}
            if with_cols:
                hit["col"] = m.start(1) + 1
            out.append(hit)
    return out


def _filter_id_hits(hits: List[Dict[str, object]], *, pattern: Optional[str], regex: bool) -> List[Dict[str, object]]:
    if not pattern:
        return hits
    if regex:
        rx = re.compile(pattern)
        return [h for h in hits if rx.search(str(h.get("id", ""))) is not None]
    return [h for h in hits if pattern in str(h.get("id", ""))]


def _unique_id_hits(hits: List[Dict[str, object]]) -> List[Dict[str, object]]:
    seen: set = set()
    out: List[Dict[str, object]] = []
    for h in hits:
        i = str(h.get("id", ""))
        if i in seen:
            continue
        seen.add(i)
        out.append(h)
    return out


def _nearest_heading_title(lines: List[str], *, from_idx: int) -> Optional[str]:
    for i in range(from_idx, -1, -1):
        m = re.match(r"^(#{1,6})\s+(.+?)\s*$", lines[i])
        if m:
            return m.group(2).strip()
    return None


def _infer_fdd_type_from_id(id_value: str) -> str:
    if "-actor-" in id_value:
        return "actor"
    if "-capability-" in id_value:
        return "capability"
    if "-usecase-" in id_value:
        return "usecase"
    if "-principle-" in id_value:
        return "principle"
    if "-nfr-" in id_value:
        return "nfr"
    if "-constraint-" in id_value:
        return "constraint"
    if "-feature-" in id_value and "-flow-" in id_value:
        return "flow"
    if "-feature-" in id_value and "-algo-" in id_value:
        return "algo"
    if "-feature-" in id_value and "-state-" in id_value:
        return "state"
    if "-feature-" in id_value and "-test-" in id_value:
        return "test"
    if "-feature-" in id_value and "-req-" in id_value:
        return "feature-requirement"
    if "-req-" in id_value:
        return "requirement"
    if "-adr-" in id_value:
        return "adr"
    return "id"


def _resolve_under_heading(lines: List[str], heading: str) -> Optional[Tuple[int, int, int]]:
    needle = heading.strip()
    for idx, line in enumerate(lines):
        m = re.match(r"^(#{1,6})\s+(.+?)\s*$", line)
        if not m:
            continue
        title = m.group(2).strip()
        if title != needle:
            continue
        start, end = _extract_heading_block(lines, idx)
        level = len(m.group(1))
        return start, end, level
    return None


def _find_id_line(lines: List[str], needle: str) -> Optional[int]:
    for idx, line in enumerate(lines):
        if needle in line:
            return idx
    return None


def _extract_block(lines: List[str], start_idx: int) -> Tuple[int, int]:
    start = start_idx
    while start > 0 and not re.match(r"^#{1,6}\s+", lines[start]):
        start -= 1
    if not re.match(r"^#{1,6}\s+", lines[start]):
        start = start_idx

    end = start + 1
    while end < len(lines) and not re.match(r"^#{1,6}\s+", lines[end]):
        end += 1
    return start, end


def _heading_level(line: str) -> Optional[int]:
    m = re.match(r"^(#{1,6})\s+", line)
    if not m:
        return None
    return len(m.group(1))


def _extract_heading_block(lines: List[str], anchor_idx: int) -> Tuple[int, int]:
    start = anchor_idx
    while start > 0 and _heading_level(lines[start]) is None:
        start -= 1
    level = _heading_level(lines[start])
    if level is None:
        return anchor_idx, anchor_idx + 1

    end = start + 1
    while end < len(lines):
        lvl = _heading_level(lines[end])
        if lvl is not None and lvl <= level:
            break
        end += 1
    return start, end


def _find_anchor_idx_for_id(lines: List[str], needle: str) -> Optional[int]:
    for idx, line in enumerate(lines):
        s = line.strip()
        if needle not in s:
            continue
        if "**ID**:" in s:
            return idx

    for idx, line in enumerate(lines):
        if needle in line and _heading_level(line) is not None:
            return idx

    return _find_id_line(lines, needle)


def _extract_id_block(lines: List[str], *, anchor_idx: int, id_value: str, kind: str) -> Tuple[int, int]:
    if kind == "feature-design":
        sections = _feature_sections_indices(lines)
        for letter, (sec_start, sec_end) in sections.items():
            if sec_start <= anchor_idx < sec_end:
                return _extract_heading_block(lines, anchor_idx)
        return _extract_heading_block(lines, anchor_idx)
    return _extract_heading_block(lines, anchor_idx)


def _iter_repo_text_files(
    root: Path,
    *,
    includes: Optional[List[str]] = None,
    excludes: Optional[List[str]] = None,
    max_bytes: int = 1_000_000,
) -> List[Path]:
    skip_dirs = {
        ".git", ".hg", ".svn", ".idea", ".vscode", "__pycache__",
        ".pytest_cache", ".mypy_cache", ".ruff_cache",
        "node_modules", "target", "dist", "build", ".venv", "venv",
    }

    out: List[Path] = []
    root = root.resolve()
    for dirpath, dirnames, filenames in os.walk(root):
        dirnames[:] = sorted([d for d in dirnames if d not in skip_dirs and not d.startswith(".")])
        for fn in sorted(filenames):
            p = (Path(dirpath) / fn)
            rel = _relative_posix(p, root)
            if excludes:
                if any(fnmatch.fnmatch(rel, pat) for pat in excludes):
                    continue
            if includes:
                if not any(fnmatch.fnmatch(rel, pat) for pat in includes):
                    continue
            try:
                st = p.stat()
            except OSError:
                continue
            if st.st_size > max_bytes:
                continue
            out.append(p)
    return out


def _read_text_lines_safe(path: Path) -> Optional[List[str]]:
    try:
        raw = path.read_bytes()
    except OSError:
        return None
    if b"\x00" in raw:
        return None
    try:
        text = raw.decode("utf-8")
    except UnicodeDecodeError:
        text = raw.decode("utf-8", errors="ignore")
    if os.linesep != "\n":
        text = text.replace("\r\n", "\n")
    return text.splitlines()


def _find_all_in_line(line: str, needle: str) -> List[int]:
    out: List[int] = []
    start = 0
    while True:
        j = line.find(needle, start)
        if j < 0:
            break
        out.append(j)
        start = j + max(1, len(needle))
    return out


def _relative_posix(path: Path, root: Path) -> str:
    try:
        rel = path.resolve().relative_to(root.resolve())
    except Exception:
        rel = path
    return rel.as_posix()


def _detect_kind(artifact_path: Path) -> str:
    name = artifact_path.name
    if name == "FEATURES.md":
        return "features-manifest"
    if name == "CHANGES.md" or name.endswith("-CHANGES.md"):
        return "feature-changes"
    if name == "DESIGN.md" and "features" in artifact_path.parts and any(p.startswith("feature-") for p in artifact_path.parts):
        return "feature-design"
    if name == "DESIGN.md":
        return "overall-design"
    return "generic"


def _lettered_section_indices(lines: List[str], section_re: re.Pattern) -> Dict[str, Tuple[int, int]]:
    starts: List[Tuple[str, int]] = []
    for i, line in enumerate(lines):
        m = section_re.match(line.strip())
        if m:
            starts.append((m.group(1).upper(), i))

    out: Dict[str, Tuple[int, int]] = {}
    for idx, (letter, start) in enumerate(starts):
        end = starts[idx + 1][1] if idx + 1 < len(starts) else len(lines)
        out[letter] = (start, end)
    return out


def _feature_sections_indices(lines: List[str]) -> Dict[str, Tuple[int, int]]:
    starts: List[Tuple[str, int]] = []
    for i, line in enumerate(lines):
        m = constants.SECTION_FEATURE_RE.match(line.strip())
        if m:
            starts.append((m.group(1).upper(), i))

    out: Dict[str, Tuple[int, int]] = {}
    for idx, (letter, start) in enumerate(starts):
        end = starts[idx + 1][1] if idx + 1 < len(starts) else len(lines)
        out[letter] = (start, end)
    return out


def _feature_changes_blocks(lines: List[str]) -> List[Dict[str, object]]:
    starts: List[Tuple[int, int]] = []
    for i, line in enumerate(lines):
        m = constants.CHANGE_HEADING_RE.match(line.strip())
        if m:
            starts.append((int(m.group(1)), i))

    blocks: List[Dict[str, object]] = []
    for idx, (num, s) in enumerate(starts):
        e = starts[idx + 1][1] if idx + 1 < len(starts) else len(lines)
        blocks.append({"number": num, "start": s, "end": e})
    return blocks


def _design_subsection_indices(lines: List[str], *, start: int, end: int) -> Dict[int, Tuple[int, int]]:
    sub_re = re.compile(r"^###\s+(\d+)\.\s+(.+?)\s*$")
    starts: List[Tuple[int, int]] = []
    for i in range(start, end):
        m = sub_re.match(lines[i].strip())
        if m:
            starts.append((int(m.group(1)), i))

    out: Dict[int, Tuple[int, int]] = {}
    for idx, (num, s) in enumerate(starts):
        e = starts[idx + 1][1] if idx + 1 < len(starts) else end
        out[num] = (s, e)
    return out


def _nearest_prev_heading(lines: List[str], *, idx: int, start: int, prefix: str) -> Optional[int]:
    for i in range(idx, start - 1, -1):
        if lines[i].strip().startswith(prefix):
            return i
    return None


def _business_block_bounds(lines: List[str], *, section_start: int, section_end: int, id_idx: int) -> Optional[Tuple[int, int]]:
    h = _nearest_prev_heading(lines, idx=id_idx, start=section_start, prefix="#### ")
    if h is None:
        return None
    e = h + 1
    while e < section_end and not lines[e].strip().startswith("#### "):
        e += 1
    return h, e


def _design_item_block_bounds(lines: List[str], *, start: int, end: int, id_idx: int) -> Tuple[int, int]:
    def is_boundary(s: str) -> bool:
        stripped = s.strip()
        if stripped.startswith("#### "):
            return True
        if re.match(r"^\*\*[^*]+\*\*:\s*$", stripped):
            return True
        return False

    s = id_idx
    while s > start:
        if is_boundary(lines[s]):
            break
        s -= 1
    e = id_idx + 1
    while e < end:
        if is_boundary(lines[e]):
            break
        e += 1
    return s, e


# =============================================================================
# SEARCH COMMANDS
# =============================================================================

def _cmd_list_sections(argv: List[str]) -> int:
    p = argparse.ArgumentParser(prog="list-sections")
    p.add_argument("--artifact", required=True)
    p.add_argument("--under-heading", default=None)
    args = p.parse_args(argv)

    artifact_path = Path(args.artifact).resolve()
    text, err = load_text(artifact_path)
    if err:
        print(json.dumps({"status": "ERROR", "message": err}, indent=None, ensure_ascii=False))
        return 1
    lines = text.splitlines()
    kind = _detect_kind(artifact_path)

    entries: List[Dict[str, object]] = []
    
    if kind == "features-manifest":
        for i, line in enumerate(lines, start=1):
            m = constants.FEATURE_HEADING_RE.match(line.strip())
            if not m:
                continue
            entries.append({
                "line": i,
                "feature_id": m.group(2),
                "index": int(m.group(1)),
                "dir": m.group(3),
                "emoji": m.group(4),
                "priority": m.group(5),
            })
    else:
        for i, line in enumerate(lines, start=1):
            m = re.match(r"^(#{1,6})\s+(.+?)\s*$", line.strip())
            if not m:
                continue
            level = len(m.group(1))
            title = m.group(2).strip()
            entries.append({"line": i, "level": level, "title": title})

    print(json.dumps({"kind": kind, "count": len(entries), "entries": entries}, indent=None, ensure_ascii=False))
    return 0


def _cmd_list_ids(argv: List[str]) -> int:
    p = argparse.ArgumentParser(prog="list-ids")
    p.add_argument("--artifact", required=True)
    p.add_argument("--under-heading", default=None)
    p.add_argument("--pattern", default=None)
    p.add_argument("--regex", action="store_true")
    p.add_argument("--all", action="store_true")
    args = p.parse_args(argv)

    artifact_path = Path(args.artifact).resolve()
    text, err = load_text(artifact_path)
    if err:
        print(json.dumps({"status": "ERROR", "message": err}, indent=None, ensure_ascii=False))
        return 1
    lines = text.splitlines()

    base_offset = 0
    if args.under_heading:
        resolved = _resolve_under_heading(lines, args.under_heading)
        if resolved is None:
            print(json.dumps({"status": "NOT_FOUND", "heading": args.under_heading}, indent=None, ensure_ascii=False))
            return 1
        start, end, _ = resolved
        base_offset = start
        lines = lines[start:end]

    hits = _extract_ids(lines)
    for h in hits:
        h["line"] = int(h.get("line", 0)) + base_offset
    hits = _filter_id_hits(hits, pattern=args.pattern, regex=bool(args.regex))
    if not args.all:
        hits = _unique_id_hits(hits)

    hits = sorted(hits, key=lambda h: (str(h.get("id", "")), int(h.get("line", 0))))
    print(json.dumps({"kind": _detect_kind(artifact_path), "count": len(hits), "ids": hits}, indent=None, ensure_ascii=False))
    return 0


def _cmd_list_items(argv: List[str]) -> int:
    p = argparse.ArgumentParser(prog="list-items", description="List structured items in an artifact")
    p.add_argument("--artifact", required=True)
    p.add_argument("--type", default=None, help="Filter by item type (e.g., actor, capability, requirement, flow)")
    p.add_argument("--lod", default="summary", choices=["id", "summary"], help="Level of detail")
    p.add_argument("--under-heading", default=None, help="Only search/list items inside the specified heading block")
    p.add_argument("--pattern", default=None, help="Substring filter (applied to id)")
    p.add_argument("--regex", action="store_true", help="Treat --pattern as regex")
    args = p.parse_args(argv)

    artifact_path = Path(args.artifact).resolve()
    text, err = load_text(artifact_path)
    if err:
        print(json.dumps({"status": "ERROR", "message": err}, indent=None, ensure_ascii=False))
        return 1
    lines = text.splitlines()
    kind = _detect_kind(artifact_path)

    id_filter = args.pattern
    rx: Optional[re.Pattern] = None
    if id_filter and args.regex:
        rx = re.compile(id_filter)

    items: List[Dict[str, object]] = []
    active_lines = lines
    base_offset = 0
    if args.under_heading:
        resolved = _resolve_under_heading(lines, args.under_heading)
        if resolved is None:
            print(json.dumps({"status": "NOT_FOUND", "kind": kind, "heading": args.under_heading}, indent=None, ensure_ascii=False))
            return 1
        start, end, _ = resolved
        base_offset = start
        active_lines = lines[start:end]

    if kind == "features-manifest":
        for i, line in enumerate(active_lines, start=base_offset + 1):
            m = constants.FEATURE_HEADING_RE.match(line.strip())
            if not m:
                continue
            fid = m.group(2)
            it = {
                "type": "feature",
                "id": fid,
                "line": i,
            }
            if args.lod == "summary":
                it.update({"index": int(m.group(1)), "dir": m.group(3), "emoji": m.group(4), "priority": m.group(5)})
            items.append(it)

    elif kind == "feature-changes":
        blocks = _feature_changes_blocks(active_lines)
        for b in blocks:
            start = int(b["start"])
            end = int(b["end"])
            block_lines = active_lines[start:end]
            title_m = constants.CHANGE_HEADING_RE.match(active_lines[start].strip()) if start < len(active_lines) else None
            title = title_m.group(2) if title_m else None

            id_line = next((l for l in block_lines if l.strip().startswith("**ID**:")), None)
            status_line = next((l for l in block_lines if l.strip().startswith("**Status**:")), None)
            ids = []
            if id_line is not None:
                ids = [h["id"] for h in _extract_ids([id_line]) if str(h.get("kind")) == "fdd"]
            cid = ids[0] if ids else f"change-{int(b['number'])}"
            it = {"type": "change", "id": cid, "change": int(b["number"]), "line": base_offset + start + 1}
            if args.lod == "summary":
                it.update({"title": title, "status": status_line.strip().split("**Status**:", 1)[1].strip() if status_line else None})
            items.append(it)

    elif kind == "generic" and artifact_path.name == "BUSINESS.md":
        section: Optional[str] = None
        for idx, line in enumerate(active_lines):
            m = constants.SECTION_BUSINESS_RE.match(line.strip())
            if m:
                section = m.group(1)
            if not line.strip().startswith("#### "):
                continue

            title = line.strip().removeprefix("#### ").strip()
            j = idx + 1
            while j < len(active_lines) and not active_lines[j].strip():
                j += 1
            id_line = active_lines[j] if j < len(active_lines) else ""
            ids = [h["id"] for h in _extract_ids([id_line]) if str(h.get("kind")) == "fdd"]
            if not ids:
                continue
            iid = str(ids[0])
            itype = "item"
            if section == "B":
                itype = "actor"
            elif section == "C":
                itype = "capability"
            elif section == "D":
                itype = "usecase"
            abs_idx = base_offset + idx
            it = {"type": itype, "id": iid, "line": abs_idx + 1}
            if args.lod == "summary":
                it.update({"title": title, "section": section})
            items.append(it)

    elif kind == "overall-design":
        id_line_re = re.compile(r"^\s*(?:[-*]\s+\[[ xX]\]\s+)?\*\*ID\*\*:\s*(.+?)\s*$")
        for rel_idx, line in enumerate(active_lines):
            m = id_line_re.match(line.strip())
            if not m:
                continue
            ids = [h["id"] for h in _extract_ids([m.group(1)]) if str(h.get("kind")) == "fdd"]
            if not ids:
                continue
            iid_s = str(ids[0])
            itype = _infer_fdd_type_from_id(iid_s)
            checked = "[x]" in line or "[X]" in line
            abs_idx = base_offset + rel_idx
            it = {"type": itype, "id": iid_s, "line": abs_idx + 1}
            if args.lod == "summary":
                it.update({"title": _nearest_heading_title(lines, from_idx=abs_idx), "checked": checked})
            items.append(it)

    elif kind == "generic" and artifact_path.name == "ADR.md":
        adr_heading_re = re.compile(r"^##\s+(ADR-\d{4})\s*:\s+(.+?)\s*$")
        starts = [(i, adr_heading_re.match(l.strip())) for i, l in enumerate(active_lines) if adr_heading_re.match(l.strip()) is not None]
        for idx, m in starts:
            key = m.group(1)
            title = m.group(2)
            end = next((j for j in range(idx + 1, len(active_lines)) if active_lines[j].strip().startswith("## ADR-")), len(active_lines))
            block_lines = active_lines[idx:end]
            date_line = next((l for l in block_lines if l.strip().startswith("**Date**:")), None)
            status_line = next((l for l in block_lines if l.strip().startswith("**Status**:")), None)
            it = {"type": "adr", "id": key, "line": base_offset + idx + 1}
            if args.lod == "summary":
                it.update(
                    {
                        "title": title,
                        "date": date_line.strip().split("**Date**:", 1)[1].strip() if date_line else None,
                        "status": status_line.strip().split("**Status**:", 1)[1].strip() if status_line else None,
                    }
                )
            items.append(it)

    elif kind == "feature-design":
        id_line_re = re.compile(r"^\s*(?:[-*]\s+\[[ xX]\]\s+)?\*\*ID\*\*:\s*(.+?)\s*$")
        for rel_idx, line in enumerate(active_lines):
            m = id_line_re.match(line.strip())
            if not m:
                continue
            ids = [h["id"] for h in _extract_ids([m.group(1)]) if str(h.get("kind")) == "fdd"]
            if not ids:
                continue
            iid_s = str(ids[0])
            itype = _infer_fdd_type_from_id(iid_s)
            checked = "[x]" in line or "[X]" in line
            abs_idx = base_offset + rel_idx
            it = {"type": itype, "id": iid_s, "line": abs_idx + 1}
            if args.lod == "summary":
                it.update({"title": _nearest_heading_title(lines, from_idx=abs_idx), "checked": checked})
            items.append(it)

    if id_filter:
        if rx is not None:
            items = [it for it in items if rx.search(str(it.get("id", ""))) is not None]
        else:
            items = [it for it in items if id_filter in str(it.get("id", ""))]

    if args.type:
        items = [it for it in items if str(it.get("type")) == str(args.type)]

    items = sorted(items, key=lambda it: (str(it.get("type", "")), str(it.get("id", "")), int(it.get("line", 0))))
    print(json.dumps({"kind": kind, "count": len(items), "items": items}, indent=None, ensure_ascii=False))
    return 0


def _cmd_read_section(argv: List[str]) -> int:
    p = argparse.ArgumentParser(prog="read-section", description="Read a section of an artifact")
    p.add_argument("--artifact", required=True)
    g = p.add_mutually_exclusive_group(required=True)
    g.add_argument("--section", help="Top-level letter section (e.g. A, B, C)")
    g.add_argument("--heading", help="Exact heading title to match")
    g.add_argument("--feature-id", help="Feature ID for FEATURES.md entry")
    g.add_argument("--change", type=int, help="Change number for CHANGES.md")
    g.add_argument("--id", help="Any ID to locate, then return its block")
    args = p.parse_args(argv)

    artifact_path = Path(args.artifact).resolve()
    text, err = load_text(artifact_path)
    if err:
        print(json.dumps({"status": "ERROR", "message": err}, indent=None, ensure_ascii=False))
        return 1
    lines = text.splitlines()
    kind = _detect_kind(artifact_path)

    if args.id is not None:
        return _cmd_find_id(["--artifact", str(artifact_path), "--id", args.id])

    if args.feature_id is not None:
        if kind != "features-manifest":
            print(json.dumps({"status": "ERROR", "message": "--feature-id is only supported for FEATURES.md"}, indent=None, ensure_ascii=False))
            return 1
        for i, line in enumerate(lines):
            m = constants.FEATURE_HEADING_RE.match(line)
            if m and m.group(2) == args.feature_id:
                start = i
                end = i + 1
                while end < len(lines) and not constants.FEATURE_HEADING_RE.match(lines[end]):
                    end += 1
                print(json.dumps({"status": "FOUND", "feature_id": args.feature_id, "text": "\n".join(lines[start:end])}, indent=None, ensure_ascii=False))
                return 0
        print(json.dumps({"status": "NOT_FOUND", "feature_id": args.feature_id}, indent=None, ensure_ascii=False))
        return 1

    if args.change is not None:
        if kind != "feature-changes":
            print(json.dumps({"status": "ERROR", "message": "--change is only supported for CHANGES.md"}, indent=None, ensure_ascii=False))
            return 1
        start_idx: Optional[int] = None
        for i, line in enumerate(lines):
            m = re.match(r"^##\s+Change\s+(\d+):", line.strip())
            if m and int(m.group(1)) == int(args.change):
                start_idx = i
                break
        if start_idx is None:
            print(json.dumps({"status": "NOT_FOUND", "change": args.change}, indent=None, ensure_ascii=False))
            return 1
        end = start_idx + 1
        while end < len(lines) and not re.match(r"^##\s+Change\s+\d+:", lines[end].strip()):
            end += 1
        print(json.dumps({"status": "FOUND", "change": args.change, "text": "\n".join(lines[start_idx:end])}, indent=None, ensure_ascii=False))
        return 0

    if args.section is not None:
        letter = args.section.strip().upper()
        start_idx = None
        for i, line in enumerate(lines):
            if re.match(rf"^##\s+{re.escape(letter)}\.\s+", line.strip()):
                start_idx = i
                break
        if start_idx is None:
            print(json.dumps({"status": "NOT_FOUND", "section": letter}, indent=None, ensure_ascii=False))
            return 1
        end = start_idx + 1
        while end < len(lines) and not re.match(r"^##\s+[A-Z]\.\s+", lines[end].strip()):
            end += 1
        print(json.dumps({"status": "FOUND", "section": letter, "text": "\n".join(lines[start_idx:end])}, indent=None, ensure_ascii=False))
        return 0

    if args.heading is not None:
        title = args.heading.strip()
        start_idx = None
        for i, line in enumerate(lines):
            m = re.match(r"^(#{1,6})\s+(.+?)\s*$", line)
            if m and m.group(2).strip() == title:
                start_idx = i
                break
        if start_idx is None:
            print(json.dumps({"status": "NOT_FOUND", "heading": title}, indent=None, ensure_ascii=False))
            return 1
        start, end = _extract_block(lines, start_idx)
        print(json.dumps({"status": "FOUND", "heading": title, "text": "\n".join(lines[start:end])}, indent=None, ensure_ascii=False))
        return 0

    print(json.dumps({"status": "ERROR", "message": "No selector provided"}, indent=None, ensure_ascii=False))
    return 1


def _cmd_get_item(argv: List[str]) -> int:
    p = argparse.ArgumentParser(prog="get-item", description="Get a structured block by id/heading/section/feature/change")
    p.add_argument("--artifact", required=True)
    g = p.add_mutually_exclusive_group(required=True)
    g.add_argument("--section")
    g.add_argument("--heading")
    g.add_argument("--feature-id")
    g.add_argument("--change", type=int)
    g.add_argument("--id")
    args = p.parse_args(argv)

    if args.id is not None:
        return _cmd_find_id(["--artifact", args.artifact, "--id", args.id])

    sub: List[str] = ["--artifact", args.artifact]
    if args.section is not None:
        sub.extend(["--section", args.section])
    elif args.heading is not None:
        sub.extend(["--heading", args.heading])
    elif args.feature_id is not None:
        sub.extend(["--feature-id", args.feature_id])
    elif args.change is not None:
        sub.extend(["--change", str(args.change)])

    return _cmd_read_section(sub)


def _cmd_find_id(argv: List[str]) -> int:
    p = argparse.ArgumentParser(prog="find-id")
    p.add_argument("--artifact", required=True)
    p.add_argument("--id", required=True)
    args = p.parse_args(argv)

    artifact_path = Path(args.artifact).resolve()
    text, err = load_text(artifact_path)
    if err:
        print(json.dumps({"status": "ERROR", "message": err}, indent=None, ensure_ascii=False))
        return 1
    lines = text.splitlines()

    kind = _detect_kind(artifact_path)

    idx = _find_id_line(lines, args.id)
    if idx is None:
        print(json.dumps({"status": "NOT_FOUND", "id": args.id}, indent=None, ensure_ascii=False))
        return 1

    anchor = _find_anchor_idx_for_id(lines, args.id) or idx
    start, end = _extract_id_block(lines, anchor_idx=anchor, id_value=args.id, kind=kind)
    print(json.dumps({
        "status": "FOUND",
        "id": args.id,
        "line": idx + 1,
        "block_start_line": start + 1,
        "block_end_line": end,
        "text": "\n".join(lines[start:end]),
    }, indent=None, ensure_ascii=False))
    return 0


def _cmd_search(argv: List[str]) -> int:
    p = argparse.ArgumentParser(prog="search")
    p.add_argument("--artifact", required=True)
    p.add_argument("--query", required=True)
    p.add_argument("--regex", action="store_true")
    args = p.parse_args(argv)

    artifact_path = Path(args.artifact).resolve()
    text, err = load_text(artifact_path)
    if err:
        print(json.dumps({"status": "ERROR", "message": err}, indent=None, ensure_ascii=False))
        return 1
    lines = text.splitlines()

    hits = []
    if args.regex:
        pat = re.compile(args.query)
        for i, line in enumerate(lines, start=1):
            if pat.search(line):
                hits.append({"line": i, "text": line})
    else:
        q = args.query
        for i, line in enumerate(lines, start=1):
            if q in line:
                hits.append({"line": i, "text": line})

    print(json.dumps({"count": len(hits), "hits": hits}, indent=None, ensure_ascii=False))
    return 0


def _cmd_scan_ids(argv: List[str]) -> int:
    p = argparse.ArgumentParser(prog="scan-ids")
    p.add_argument("--root", required=True)
    p.add_argument("--pattern", default=None)
    p.add_argument("--regex", action="store_true")
    p.add_argument("--kind", default="all", choices=["all", "fdd", "adr"])
    p.add_argument("--all", action="store_true")
    p.add_argument("--include", action="append", default=None)
    p.add_argument("--exclude", action="append", default=None)
    p.add_argument("--max-bytes", type=int, default=1_000_000)
    args = p.parse_args(argv)

    root = Path(args.root).resolve()
    scan_root = root if root.is_dir() else root.parent
    files = [root] if root.is_file() else _iter_repo_text_files(root, includes=args.include, excludes=args.exclude, max_bytes=int(args.max_bytes))

    rx: Optional[re.Pattern] = None
    if args.pattern and args.regex:
        rx = re.compile(str(args.pattern))

    hits: List[Dict[str, object]] = []
    for fp in files:
        lines = _read_text_lines_safe(fp)
        if lines is None:
            continue
        for h in _extract_ids(lines, with_cols=True):
            if args.kind != "all" and str(h.get("kind")) != str(args.kind):
                continue
            sid = str(h.get("id", ""))
            if args.pattern:
                if rx is not None:
                    if rx.search(sid) is None:
                        continue
                else:
                    if str(args.pattern) not in sid:
                        continue
            hit = {
                "id": sid,
                "kind": str(h.get("kind")),
                "path": _relative_posix(fp, scan_root),
                "line": int(h.get("line", 0)),
                "col": int(h.get("col", 0)),
            }
            hits.append(hit)

    hits = sorted(hits, key=lambda h: (str(h.get("id", "")), str(h.get("path", "")), int(h.get("line", 0)), int(h.get("col", 0))))
    if not args.all:
        seen: set = set()
        uniq: List[Dict[str, object]] = []
        for h in hits:
            k = (str(h.get("id", "")), str(h.get("path", "")))
            if k in seen:
                continue
            seen.add(k)
            uniq.append(h)
        hits = uniq

    print(json.dumps({"root": root.as_posix(), "count": len(hits), "ids": hits}, indent=None, ensure_ascii=False))
    return 0


def _iter_candidate_definition_files(root: Path, *, needle: str) -> List[Path]:
    kind = _infer_fdd_type_from_id(needle)
    want_suffixes: List[str] = []
    if needle.startswith("ADR-"):
        want_suffixes = ["architecture/ADR.md"]
    elif "-adr-" in needle:
        want_suffixes = ["architecture/ADR.md"]
    elif kind in {"actor", "capability", "usecase"}:
        want_suffixes = ["architecture/BUSINESS.md"]
    elif kind in {"requirement", "principle", "nfr", "constraint"}:
        want_suffixes = ["architecture/DESIGN.md"]
    elif kind == "feature":
        want_suffixes = ["architecture/features/FEATURES.md"]
    elif kind in {"flow", "algo", "state", "test", "feature-requirement"} or "-td-" in needle:
        want_suffixes = ["architecture/features/feature-*/DESIGN.md"]
    elif "-feature-" in needle and "-change-" in needle:
        want_suffixes = ["architecture/features/feature-*/CHANGES.md", "architecture/features/feature-*/archive/*.md"]
    else:
        want_suffixes = ["architecture/DESIGN.md", "architecture/BUSINESS.md", "architecture/ADR.md"]

    expanded: List[str] = []
    seen: set = set()
    for suf in want_suffixes:
        for pat in [suf, f"**/{suf}"]:
            if pat in seen:
                continue
            seen.add(pat)
            expanded.append(pat)
    want_suffixes = expanded

    root = root.resolve()
    files: List[Path] = []
    candidates = _iter_repo_text_files(root, includes=want_suffixes)
    for p in candidates:
        rel = _relative_posix(p, root)
        if rel.endswith(".md"):
            files.append(p)
    return sorted(set(files), key=lambda pp: _relative_posix(pp, root))


def _definition_hits_in_file(*, path: Path, root: Path, needle: str, include_tags: bool) -> List[Dict[str, object]]:
    lines = _read_text_lines_safe(path)
    if lines is None:
        return []
    rel = _relative_posix(path, root)
    hits: List[Dict[str, object]] = []
    is_markdown = path.suffix.lower() == ".md"

    if needle.startswith("ADR-"):
        adr_heading_re = re.compile(rf"^##\s+{re.escape(needle)}\s*:")
        for i, line in enumerate(lines, start=1):
            if adr_heading_re.match(line.strip()):
                hits.append({"path": rel, "line": i, "col": 1, "text": line, "match": "adr_heading"})
        return hits

    section_idx: Optional[Dict[str, Tuple[int, int]]] = None
    if is_markdown and rel.endswith("architecture/BUSINESS.md"):
        section_idx = _lettered_section_indices(lines, constants.SECTION_BUSINESS_RE)
    if is_markdown and rel.endswith("architecture/DESIGN.md"):
        section_idx = _lettered_section_indices(lines, re.compile(r"^##\s+([A-D])\.\s+(.+?)\s*$"))

    expected_business_section: Optional[str] = None
    itype = _infer_fdd_type_from_id(needle)
    if rel.endswith("architecture/BUSINESS.md"):
        if itype == "actor":
            expected_business_section = "B"
        elif itype == "capability":
            expected_business_section = "C"
        elif itype == "usecase":
            expected_business_section = "D"

    expected_design_subsection: Optional[int] = None
    if rel.endswith("architecture/DESIGN.md"):
        if itype == "requirement":
            expected_design_subsection = 1
        elif itype == "nfr":
            expected_design_subsection = 2
        elif itype == "principle":
            expected_design_subsection = 3
        elif itype == "constraint":
            expected_design_subsection = 4

    for i, line in enumerate(lines, start=1):
        if needle not in line:
            continue
        if is_markdown and "**ID**:" in line:
            idx0 = i - 1
            if expected_business_section is not None and section_idx is not None:
                rng = section_idx.get(expected_business_section)
                if rng is None:
                    continue
                sec_s, sec_e = rng
                if not (sec_s <= idx0 < sec_e):
                    continue
                bnd = _business_block_bounds(lines, section_start=sec_s, section_end=sec_e, id_idx=idx0)
                if bnd is None:
                    continue
                bs, be = bnd
                if not (bs <= idx0 < be):
                    continue

            if rel.endswith("architecture/DESIGN.md") and section_idx is not None:
                b_rng = section_idx.get("B")
                if b_rng is None:
                    continue
                b_s, b_e = b_rng
                if not (b_s <= idx0 < b_e):
                    continue
                subs = _design_subsection_indices(lines, start=b_s, end=b_e)
                if expected_design_subsection is not None and expected_design_subsection in subs:
                    ss, se = subs[expected_design_subsection]
                    if not (ss <= idx0 < se):
                        continue
                ib_s, ib_e = _design_item_block_bounds(lines, start=b_s, end=b_e, id_idx=idx0)
                if not (ib_s <= idx0 < ib_e):
                    continue

            for col0 in _find_all_in_line(line, needle) or [line.find(needle)]:
                if col0 >= 0:
                    hits.append({"path": rel, "line": i, "col": col0 + 1, "text": line, "match": "id_line"})
            continue
        if include_tags and "@fdd-" in line:
            for col0 in _find_all_in_line(line, needle) or [line.find(needle)]:
                if col0 >= 0:
                    hits.append({"path": rel, "line": i, "col": col0 + 1, "text": line, "match": "tag"})
    return hits


def _where_defined_internal(
    *,
    root: Path,
    raw_id: str,
    include_tags: bool,
    includes: Optional[List[str]],
    excludes: Optional[List[str]],
    max_bytes: int,
) -> Tuple[str, List[Dict[str, object]], List[Dict[str, object]]]:
    base, phase, inst = _parse_trace_query(raw_id)

    base_files = _iter_candidate_definition_files(root, needle=base)
    files = base_files
    if include_tags:
        files = sorted(
            set(files + _iter_repo_text_files(root, includes=includes, excludes=excludes, max_bytes=max_bytes)),
            key=lambda pp: _relative_posix(pp, root),
        )

    base_defs: List[Dict[str, object]] = []
    for fp in files:
        base_defs.extend(_definition_hits_in_file(path=fp, root=root, needle=base, include_tags=bool(include_tags)))
    base_defs = sorted(base_defs, key=lambda h: (str(h.get("path", "")), int(h.get("line", 0)), int(h.get("col", 0))))

    if phase is None and inst is None:
        return base, base_defs, []

    seg_defs: List[Dict[str, object]] = []
    for d in base_defs:
        p = Path(root) / str(d.get("path", ""))
        sp = str(d.get("path", ""))
        if "architecture/features/" not in sp or not sp.endswith("/DESIGN.md"):
            continue
        lines = _read_text_lines_safe(p)
        if lines is None:
            continue
        anchor0 = _find_anchor_idx_for_id(lines, base)
        if anchor0 is None:
            continue
        start, end = _extract_id_block(lines, anchor_idx=anchor0, id_value=base, kind="feature-design")
        for i in range(start, end):
            line = lines[i]
            matched = _match_phase_inst_in_line(line, phase=phase, inst=inst)
            if matched is None:
                continue
            seg, col0 = matched
            seg_defs.append(
                {
                    "path": sp,
                    "line": i + 1,
                    "col": col0 + 1,
                    "text": line,
                    "match": f"fdl_{seg}",
                    "segment": seg,
                }
            )

    seg_defs = sorted(seg_defs, key=lambda h: (str(h.get("path", "")), int(h.get("line", 0)), int(h.get("col", 0))))
    return base, seg_defs, base_defs


def _cmd_where_defined(argv: List[str]) -> int:
    p = argparse.ArgumentParser(prog="where-defined", description="Find where an ID is defined")
    p.add_argument("--id", required=True)
    p.add_argument("--root", default=".", help="Root directory to search (default: current working directory)")
    p.add_argument("--include-tags", action="store_true", help="Also treat @fdd-* code tags as definitions")
    p.add_argument("--include", action="append", default=None, help="Glob include filter over relative paths (repeatable)")
    p.add_argument("--exclude", action="append", default=None, help="Glob exclude filter over relative paths (repeatable)")
    p.add_argument("--max-bytes", type=int, default=1_000_000, help="Skip files larger than this size")
    args = p.parse_args(argv)

    raw_id = str(args.id).strip()
    base, phase, inst = _parse_trace_query(raw_id)
    root = Path(args.root).resolve()

    _, defs, ctx_defs = _where_defined_internal(
        root=root,
        raw_id=raw_id,
        include_tags=bool(args.include_tags),
        includes=args.include,
        excludes=args.exclude,
        max_bytes=int(args.max_bytes),
    )

    if not defs:
        print(json.dumps(
            {
                "status": "NOT_FOUND",
                "id": raw_id,
                "base_id": base,
                "phase": phase,
                "inst": inst,
                "root": root.as_posix(),
                "count": 0,
                "definitions": [],
                "context_definitions": ctx_defs,
            },
            indent=None,
            ensure_ascii=False,
        ))
        return 1
    status = "FOUND" if len(defs) == 1 else "AMBIGUOUS"
    print(json.dumps(
        {
            "status": status,
            "id": raw_id,
            "base_id": base,
            "phase": phase,
            "inst": inst,
            "root": root.as_posix(),
            "count": len(defs),
            "definitions": defs,
            "context_definitions": ctx_defs,
        },
        indent=None,
        ensure_ascii=False,
    ))
    return 0 if status == "FOUND" else 2


def _cmd_where_used(argv: List[str]) -> int:
    p = argparse.ArgumentParser(prog="where-used", description="Find where an ID is referenced across a repository")
    p.add_argument("--id", required=True)
    p.add_argument("--root", default=".", help="Root directory to search (default: current working directory)")
    p.add_argument("--include", action="append", default=None, help="Glob include filter over relative paths (repeatable)")
    p.add_argument("--exclude", action="append", default=None, help="Glob exclude filter over relative paths (repeatable)")
    p.add_argument("--max-bytes", type=int, default=1_000_000, help="Skip files larger than this size")
    args = p.parse_args(argv)

    raw_id = str(args.id).strip()
    base, phase, inst = _parse_trace_query(raw_id)
    root = Path(args.root).resolve()
    files = _iter_repo_text_files(root, includes=args.include, excludes=args.exclude, max_bytes=int(args.max_bytes))

    _, defs, _ctx = _where_defined_internal(
        root=root,
        raw_id=raw_id,
        include_tags=False,
        includes=args.include,
        excludes=args.exclude,
        max_bytes=int(args.max_bytes),
    )
    def_keys = {(str(d.get("path", "")), int(d.get("line", 0)), int(d.get("col", 0))) for d in defs}
    trace_pat = _compile_trace_regex(base, phase, inst)

    hits: List[Dict[str, object]] = []
    for fp in files:
        lines = _read_text_lines_safe(fp)
        if lines is None:
            continue
        for i, line in enumerate(lines, start=1):
            if trace_pat.search(line) is None:
                continue
            cols = _find_all_in_line(line, base)
            for col0 in cols:
                h = {
                    "path": _relative_posix(fp, root),
                    "line": i,
                    "col": col0 + 1,
                    "text": line,
                }
                k = (str(h.get("path")), int(h.get("line")), int(h.get("col")))
                if k in def_keys:
                    continue
                hits.append(h)

    hits = sorted(hits, key=lambda h: (str(h.get("path", "")), int(h.get("line", 0)), int(h.get("col", 0))))
    print(json.dumps({"id": raw_id, "base_id": base, "phase": phase, "inst": inst, "root": root.as_posix(), "count": len(hits), "hits": hits}, indent=None, ensure_ascii=False))
    return 0


# =============================================================================
# ADAPTER COMMAND
# =============================================================================

def _cmd_adapter_info(argv: List[str]) -> int:
    """
    Discover and display FDD adapter information.
    Shows adapter location, project name, and available specs.
    """
    p = argparse.ArgumentParser(prog="adapter-info", description="Discover FDD adapter configuration")
    p.add_argument("--root", default=".", help="Project root to search from (default: current directory)")
    p.add_argument("--fdd-root", default=None, help="FDD core location (if agent knows it)")
    args = p.parse_args(argv)
    
    start_path = Path(args.root).resolve()
    fdd_root_path = Path(args.fdd_root).resolve() if args.fdd_root else None
    
    # Find project root
    project_root = _find_project_root(start_path)
    if project_root is None:
        print(json.dumps(
            {
                "status": "NOT_FOUND",
                "message": "No project root found (no .git or .fdd-config.json)",
                "searched_from": start_path.as_posix(),
                "hint": "Create .fdd-config.json in project root to configure FDD",
            },
            indent=2,
            ensure_ascii=False,
        ))
        return 1
    
    # Find adapter
    adapter_dir = _find_adapter_directory(start_path, fdd_root=fdd_root_path)
    if adapter_dir is None:
        # Check if config exists to provide better error message
        cfg = _load_project_config(project_root)
        if cfg is not None:
            adapter_rel = cfg.get("fddAdapterPath")
            if adapter_rel is not None and isinstance(adapter_rel, str):
                # Config exists but path is invalid
                print(json.dumps(
                    {
                        "status": "CONFIG_ERROR",
                        "message": f"Config specifies adapter path but directory not found or invalid",
                        "project_root": project_root.as_posix(),
                        "config_path": adapter_rel,
                        "expected_location": (project_root / adapter_rel).as_posix(),
                        "hint": "Check .fdd-config.json fddAdapterPath points to valid directory with AGENTS.md",
                    },
                    indent=2,
                    ensure_ascii=False,
                ))
                return 1
        
        # No config, no adapter found via recursive search
        print(json.dumps(
            {
                "status": "NOT_FOUND",
                "message": "No FDD-Adapter found in project (searched recursively up to 5 levels deep)",
                "project_root": project_root.as_posix(),
                "hint": "Create .fdd-config.json with fddAdapterPath or run adapter-bootstrap workflow",
            },
            indent=2,
            ensure_ascii=False,
        ))
        return 1
    
    # Load adapter config
    config = _load_adapter_config(adapter_dir)
    config["status"] = "FOUND"
    config["project_root"] = project_root.as_posix()
    
    # Calculate relative path
    try:
        relative_path = adapter_dir.relative_to(project_root).as_posix()
    except ValueError:
        relative_path = adapter_dir.as_posix()
    config["relative_path"] = relative_path
    
    # Check if .fdd-config.json exists
    config_file = project_root / ".fdd-config.json"
    config["has_config"] = config_file.exists()
    if not config_file.exists():
        config["config_hint"] = f"Create .fdd-config.json with: {{\"fddAdapterPath\": \"{relative_path}\"}}"
    
    print(json.dumps(config, indent=2, ensure_ascii=False))
    return 0


# =============================================================================
# MAIN ENTRY POINT
# =============================================================================

def main(argv: Optional[List[str]] = None) -> int:
    argv_list = list(argv) if argv is not None else sys.argv[1:]
    
    # Define all available commands
    validation_commands = ["validate"]
    search_commands = [
        "list-sections", "list-ids", "list-items",
        "read-section", "get-item", "find-id",
        "search", "scan-ids",
        "where-defined", "where-used",
        "adapter-info",
    ]
    all_commands = validation_commands + search_commands

    if not argv_list:
        print(json.dumps({
            "status": "ERROR",
            "message": "Missing subcommand",
            "validation_commands": validation_commands,
            "search_commands": search_commands,
        }, indent=None, ensure_ascii=False))
        return 1

    # Backward compatibility: if first arg starts with --, assume validate command
    if argv_list[0].startswith("-"):
        cmd = "validate"
        rest = argv_list
    else:
        cmd = argv_list[0]
        rest = argv_list[1:]

    # Dispatch to appropriate command handler
    if cmd == "validate":
        return _cmd_validate(rest)
    elif cmd == "list-sections":
        return _cmd_list_sections(rest)
    elif cmd == "list-ids":
        return _cmd_list_ids(rest)
    elif cmd == "list-items":
        return _cmd_list_items(rest)
    elif cmd == "read-section":
        return _cmd_read_section(rest)
    elif cmd == "get-item":
        return _cmd_get_item(rest)
    elif cmd == "find-id":
        return _cmd_find_id(rest)
    elif cmd == "search":
        return _cmd_search(rest)
    elif cmd == "scan-ids":
        return _cmd_scan_ids(rest)
    elif cmd == "where-defined":
        return _cmd_where_defined(rest)
    elif cmd == "where-used":
        return _cmd_where_used(rest)
    elif cmd == "adapter-info":
        return _cmd_adapter_info(rest)
    else:
        print(json.dumps({
            "status": "ERROR",
            "message": f"Unknown command: {cmd}",
            "available": all_commands,
        }, indent=None, ensure_ascii=False))
        return 1


if __name__ == "__main__":
    raise SystemExit(main())


__all__ = ["main"]
