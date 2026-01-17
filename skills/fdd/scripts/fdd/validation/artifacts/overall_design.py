"""
FDD Validator - Overall DESIGN.md Validation

Validates architecture/DESIGN.md: system design, requirements, NFRs, principles, constraints.
"""

import re
from pathlib import Path
from typing import Dict, List, Optional, Set, Tuple

from ...constants import (
    REQ_ID_RE,
    NFR_ID_RE,
    PRINCIPLE_ID_RE,
    CONSTRAINT_ID_RE,
    ADR_ID_RE,
    ADR_NUM_RE,
    CAPABILITY_ID_RE,
    USECASE_ID_RE,
)

from ...utils import (
    find_placeholders,
    load_text,
    find_present_section_ids,
    parse_business_model,
    parse_adr_index,
)


__all__ = ["validate_overall_design"]
def validate_overall_design(
    artifact_text: str,
    *,
    artifact_path: Optional[Path] = None,
    business_path: Optional[Path] = None,
    adr_path: Optional[Path] = None,
    skip_fs_checks: bool = False,
) -> Dict[str, object]:
    errors: List[Dict[str, object]] = []
    placeholders = find_placeholders(artifact_text)

    present = find_present_section_ids(artifact_text)
    needed = ["A", "B", "C"]
    missing = [s for s in needed if s not in set(present)]
    if missing:
        errors.append({"type": "structure", "message": "Missing required top-level sections", "missing": missing})

    c_subs = [m.group(1) for m in re.finditer(r"^###\s+C\.(\d+)\s*[:.]", artifact_text, re.MULTILINE)]
    if c_subs:
        expected = ["1", "2", "3", "4", "5"]
        if c_subs != expected:
            errors.append({"type": "structure", "message": "Section C must have exactly C.1..C.5 in order", "found": c_subs})

    business_actors: set = set()
    business_caps_to_actors: Dict[str, set] = {}
    business_usecases: set = set()
    adr_ids: set = set()
    adr_num_to_id: Dict[int, str] = {}

    if not skip_fs_checks and artifact_path is not None:
        bp = business_path or (artifact_path.parent / "BUSINESS.md")
        ap = adr_path or (artifact_path.parent / "ADR.md")

        bt, berr = load_text(bp)
        if berr:
            errors.append({"type": "cross", "message": berr})
        else:
            business_actors, business_caps_to_actors, business_usecases = parse_business_model(bt or "")

        at, aerr = load_text(ap)
        if aerr:
            errors.append({"type": "cross", "message": aerr})
        else:
            adr_entries, adr_issues = parse_adr_index(at or "")
            errors.extend(adr_issues)
            for e in adr_entries:
                if "id" in e and e["id"]:
                    adr_ids.add(str(e["id"]))
                if "num" in e and "id" in e and e.get("id"):
                    adr_num_to_id[int(e["num"])] = str(e["id"])  # type: ignore[arg-type]

    req_blocks: List[Dict[str, object]] = []
    lines = artifact_text.splitlines()
    idxs = [i for i, l in enumerate(lines) if "**ID**:" in l and REQ_ID_RE.search(l)]
    for i, start in enumerate(idxs):
        end = idxs[i + 1] if i + 1 < len(idxs) else len(lines)
        block = lines[start:end]
        id_line = lines[start]
        req_id = next(iter(REQ_ID_RE.findall(id_line)), None)
        if not req_id:
            continue
        block_text = "\n".join(block)
        caps = set(CAPABILITY_ID_RE.findall(block_text))
        actors = set(ACTOR_ID_RE.findall(block_text))
        usecases = set(USECASE_ID_RE.findall(block_text))
        adr_refs: set = set(ADR_ID_RE.findall(block_text))
        for n in ADR_NUM_RE.findall(block_text):
            mapped = adr_num_to_id.get(int(n))
            if mapped:
                adr_refs.add(mapped)
        req_blocks.append({"id": req_id, "caps": caps, "actors": actors, "usecases": usecases, "adr_ids": adr_refs})

    req_issues: List[Dict[str, object]] = []
    if not req_blocks:
        req_issues.append({"message": "No functional requirement IDs found"})

    cap_covered: set = set()
    uc_covered: set = set()
    adr_covered: set = set()

    for rb in req_blocks:
        rid = rb["id"]
        caps = rb["caps"]
        actors = rb["actors"]

        if not caps:
            req_issues.append({"requirement": rid, "message": "Missing capability references"})
        if not actors:
            req_issues.append({"requirement": rid, "message": "Missing actor references"})

        cap_covered |= set(caps)
        uc_covered |= set(rb["usecases"])
        adr_covered |= set(rb["adr_ids"])

        if business_actors:
            bad = sorted([a for a in actors if a not in business_actors])
            if bad:
                req_issues.append({"requirement": rid, "message": "Unknown actor IDs", "ids": bad})

        if business_caps_to_actors:
            bad = sorted([c for c in caps if c not in business_caps_to_actors])
            if bad:
                req_issues.append({"requirement": rid, "message": "Unknown capability IDs", "ids": bad})
            allowed: set = set()
            for c in caps:
                allowed |= set(business_caps_to_actors.get(c, set()))
            if allowed and actors and not set(actors).issubset(allowed):
                req_issues.append({"requirement": rid, "message": "Actors must match actors of referenced capabilities", "actors": sorted(list(actors)), "allowed": sorted(list(allowed))})

        if business_usecases and rb["usecases"]:
            bad = sorted([u for u in rb["usecases"] if u not in business_usecases])
            if bad:
                req_issues.append({"requirement": rid, "message": "Unknown use case IDs", "ids": bad})

        if adr_ids and rb["adr_ids"]:
            bad = sorted([a for a in rb["adr_ids"] if a not in adr_ids])
            if bad:
                req_issues.append({"requirement": rid, "message": "Unknown ADR references", "ids": bad})

    if business_caps_to_actors:
        missing_caps = sorted([c for c in business_caps_to_actors.keys() if c not in cap_covered])
        if missing_caps:
            errors.append({"type": "traceability", "message": "Orphaned capabilities (not referenced in DESIGN.md requirements)", "ids": missing_caps})

    if business_usecases:
        missing_uc = sorted([u for u in business_usecases if u not in uc_covered])
        if missing_uc:
            errors.append({"type": "traceability", "message": "Orphaned use cases (not referenced in DESIGN.md requirements)", "ids": missing_uc})

    # ADR coverage is computed across the entire DESIGN.md (requirements + principles + constraints + NFRs)
    if adr_ids:
        covered: set = set(ADR_ID_RE.findall(artifact_text))
        for n in ADR_NUM_RE.findall(artifact_text):
            mapped = adr_num_to_id.get(int(n))
            if mapped:
                covered.add(mapped)
        missing_adrs = sorted([a for a in adr_ids if a not in covered])
        if missing_adrs:
            errors.append({"type": "traceability", "message": "Orphaned ADRs (not referenced in DESIGN.md)", "ids": missing_adrs})

    passed = (len(errors) == 0) and (len(req_issues) == 0) and (len(placeholders) == 0)
    return {
        "required_section_count": 3,
        "missing_sections": [{"id": s, "title": ""} for s in missing],
        "placeholder_hits": placeholders,
        "status": "PASS" if passed else "FAIL",
        "errors": errors,
        "requirement_issues": req_issues,
        "requirement_count": len(req_blocks),
    }


FIELD_HEADER_RE = re.compile(r"^\s*[-*]?\s*\*\*([^*]+)\*\*:\s*(.*)$")

KNOWN_FIELD_NAMES = {
    "Purpose",
    "Target Users",
    "Key Problems Solved",
    "Success Criteria",
    "Actor",
    "Actors",
    "Role",
    "Preconditions",
    "Flow",
    "Postconditions",
    "Status",
    "Depends On",
    "Blocks",
    "Scope",
    "Requirements Covered",
    "Principles Covered",
    "Constraints Affected",
    "Phases",
    "References",
    "Implements",
    "ADRs",
    "Capabilities",
    "Technology",
    "Location",
    "Input",
    "Output",
    "Testing Scenarios",
    "Testing Scenarios (FDL)",
    "Acceptance Criteria",
}


def _field_block(lines: List[str], field_name: str) -> Optional[Dict[str, object]]:
    for idx, line in enumerate(lines):
        m = FIELD_HEADER_RE.match(line)
        if not m:
            continue
        if m.group(1).strip() != field_name:
            continue
        value = m.group(2)
        tail: List[str] = []
        for j in range(idx + 1, len(lines)):
            m2 = FIELD_HEADER_RE.match(lines[j])
            if m2 and m2.group(1).strip() in KNOWN_FIELD_NAMES:
                break
            tail.append(lines[j])
        return {"index": idx, "value": value, "tail": tail}
    return None


def _has_list_item(lines: List[str]) -> bool:
    return any(re.match(r"^\s*[-*]\s+\S+", l) for l in lines)


SECTION_BUSINESS_RE = re.compile(r"^##\s+(?:Section\s+)?([A-E])\s*[:.]\s*(.+)?$", re.IGNORECASE)


def _split_by_business_section_letter(text: str) -> Tuple[List[str], Dict[str, List[str]]]:
    """Split BUSINESS.md by section letters (A-E)."""
    return _split_by_section_letter(text, SECTION_BUSINESS_RE)


def _extract_backticked_ids(line: str, pattern: re.Pattern) -> List[str]:
    ids: List[str] = []
    for tok in re.findall(r"`([^`]+)`", line):
        t = tok.strip()
        if pattern.fullmatch(t) or pattern.search(t):
            ids.append(t)
    if ids:
        return ids
    return pattern.findall(line)


def _paragraph_count(lines: List[str]) -> int:
    paras = 0
    buf: List[str] = []
    for l in lines:
        s = l.strip()
        if not s:
            if any(x.strip() for x in buf):
                paras += 1
            buf = []
            continue
        if s.startswith("#"):
            continue
        buf.append(s)
    if any(x.strip() for x in buf):
        paras += 1
    return paras


