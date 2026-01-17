"""
FDD Validator - Markdown Parsing Utilities

Functions for parsing markdown structure, extracting sections, and analyzing content.
"""

import re
from pathlib import Path
from typing import Dict, List, Optional, Tuple

from ..constants import (
    SECTION_RE,
    HEADING_ID_RE,
    SECTION_FEATURE_RE,
    SECTION_BUSINESS_RE,
    FIELD_HEADER_RE,
    KNOWN_FIELD_NAMES,
)


def parse_required_sections(requirements_path: Path) -> Dict[str, str]:
    """
    Parse required sections from requirements file.
    
    Returns dict mapping section ID to section title.
    """
    sections: Dict[str, str] = {}
    for line in requirements_path.read_text(encoding="utf-8").splitlines():
        m = SECTION_RE.match(line)
        if not m:
            continue
        section_id = m.group(1)
        section_title = m.group(2)
        sections[section_id] = section_title
    return sections


def find_present_section_ids(artifact_text: str) -> List[str]:
    """
    Find section letter IDs present in artifact (e.g., A, B, C).
    
    Looks for headings like "# A. Introduction"
    """
    present = []
    for line in artifact_text.splitlines():
        m = HEADING_ID_RE.match(line)
        if m:
            present.append(m.group(1))
    return present


def split_by_section_letter(text: str, section_re: re.Pattern) -> Tuple[List[str], Dict[str, List[str]]]:
    """
    Split text by lettered sections using provided regex pattern.
    
    Args:
        text: Text to split
        section_re: Compiled regex pattern to match section headers
    
    Returns:
        Tuple of (section_order, section_dict)
        - section_order: List of section letters in order found
        - section_dict: Dict mapping section letter to list of lines in that section
    """
    lines = text.splitlines()
    found_order: List[str] = []
    sections: Dict[str, List[str]] = {}
    current: Optional[str] = None
    for line in lines:
        m = section_re.match(line.strip())
        if m:
            current = m.group(1).upper()
            if current not in sections:
                found_order.append(current)
                sections[current] = []
            continue
        if current is not None:
            sections[current].append(line)
    return found_order, sections


def split_by_feature_section_letter(text: str) -> Tuple[List[str], Dict[str, List[str]]]:
    """Split feature DESIGN.md by section letters (A-G)."""
    return split_by_section_letter(text, SECTION_FEATURE_RE)


def split_by_business_section_letter(text: str) -> Tuple[List[str], Dict[str, List[str]]]:
    """Split BUSINESS.md by section letters (A-E)."""
    return split_by_section_letter(text, SECTION_BUSINESS_RE)


def field_block(lines: List[str], field_name: str) -> Optional[Dict[str, object]]:
    """
    Extract field block from list of lines.
    
    Looks for field header like "**Field Name**: value" and extracts
    value plus all following lines until next field header.
    
    Returns dict with {index, value, tail} or None if not found.
    """
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


def has_list_item(lines: List[str]) -> bool:
    """Check if any line in list is a markdown list item (starts with - or *)."""
    return any(re.match(r"^\s*[-*]\s+\S+", l) for l in lines)


def extract_backticked_ids(line: str, pattern: re.Pattern) -> List[str]:
    """
    Extract IDs from backticked tokens that match pattern.
    
    Example: "`fdd-project-feature-x-flow-y`" -> ["fdd-project-feature-x-flow-y"]
    """
    ids: List[str] = []
    for tok in re.findall(r"`([^`]+)`", line):
        if pattern.fullmatch(tok.strip()):
            ids.append(tok.strip())
    return ids
