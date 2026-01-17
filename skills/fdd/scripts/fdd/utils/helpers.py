"""
FDD Validator - Helper Functions

Helper functions for parsing and analyzing artifacts.
"""

import re
from pathlib import Path
from typing import Dict, List, Optional, Set, Tuple

from ..constants import (
    HEADING_ID_RE,
    ACTOR_ID_RE,
    CAPABILITY_ID_RE,
    USECASE_ID_RE,
    ADR_HEADING_RE,
    ADR_DATE_RE,
    ADR_STATUS_RE,
    ADR_ID_RE,
    FDD_ADR_NUM_RE,
)


def find_present_section_ids(artifact_text: str) -> List[str]:
    """Extract all section letter IDs (A, B, C, etc.) present in the artifact."""
    present: List[str] = []
    for line in artifact_text.splitlines():
        m = HEADING_ID_RE.match(line.strip())
        if m:
            present.append(m.group(1))
    return present


def parse_business_model(text: str) -> Tuple[Set[str], Dict[str, Set[str]], Set[str]]:
    """
    Parse BUSINESS.md and extract actors, capabilities, and use cases.
    
    Returns:
        - Set of actor IDs
        - Dict mapping capability IDs to their actor IDs
        - Set of use case IDs
    """
    actor_ids: Set[str] = set(ACTOR_ID_RE.findall(text))
    capability_to_actors: Dict[str, Set[str]] = {}
    usecase_ids: Set[str] = set(USECASE_ID_RE.findall(text))
    
    # Parse capability sections to map capabilities to actors
    lines = text.splitlines()
    in_capability_section = False
    current_capability_id: Optional[str] = None
    
    for line in lines:
        if "## C. Capabilities" in line or "## Section C" in line:
            in_capability_section = True
            continue
        if in_capability_section and line.strip().startswith("## "):
            in_capability_section = False
        
        if in_capability_section:
            # Look for capability ID
            cap_matches = CAPABILITY_ID_RE.findall(line)
            if cap_matches:
                current_capability_id = cap_matches[0]
                capability_to_actors[current_capability_id] = set()
            
            # Look for actor references in current capability
            if current_capability_id:
                actor_matches = ACTOR_ID_RE.findall(line)
                for actor_id in actor_matches:
                    capability_to_actors[current_capability_id].add(actor_id)
    
    return actor_ids, capability_to_actors, usecase_ids


def parse_adr_index(text: str) -> Tuple[List[Dict[str, object]], List[Dict[str, object]]]:
    """
    Parse ADR.md index and extract ADR entries.
    
    Returns:
        - List of ADR entry dicts with id, num, title, date, status
        - List of validation issues found
    """
    issues: List[Dict[str, object]] = []
    adrs: List[Dict[str, object]] = []
    lines = text.splitlines()
    
    i = 0
    while i < len(lines):
        line = lines[i]
        m = ADR_HEADING_RE.match(line.strip())
        if m:
            adr_ref = m.group(1)  # ADR-0001
            adr_num = int(m.group(2))  # 0001
            title = m.group(3)
            
            # Look ahead for metadata
            date_val: Optional[str] = None
            status_val: Optional[str] = None
            adr_id: Optional[str] = None
            
            for j in range(i + 1, min(i + 10, len(lines))):
                next_line = lines[j]
                
                date_m = ADR_DATE_RE.search(next_line)
                if date_m:
                    date_val = date_m.group(1)
                
                status_m = ADR_STATUS_RE.search(next_line)
                if status_m:
                    status_val = status_m.group(1)
                
                # Look for FDD ID
                id_matches = ADR_ID_RE.findall(next_line)
                if id_matches:
                    adr_id = id_matches[0]
                
                # Stop if we hit another heading
                if next_line.strip().startswith("## "):
                    break
            
            adrs.append({
                "ref": adr_ref,
                "num": adr_num,
                "title": title,
                "date": date_val,
                "status": status_val,
                "id": adr_id,
            })
        
        i += 1
    
    return adrs, issues


__all__ = [
    "find_present_section_ids",
    "parse_business_model",
    "parse_adr_index",
]
