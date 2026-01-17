"""
FDD Validator - Text Processing Utilities

Text manipulation helpers: slugification, placeholder detection, string normalization.
"""

import re
from typing import Dict, List

from ..constants import PLACEHOLDER_RE


def slugify_anchor(text: str) -> str:
    """
    Convert heading text to URL-friendly anchor slug.
    
    Example: "A. Introduction" -> "a-introduction"
    """
    t = re.sub(r"`[^`]*`", "", text)
    t = t.strip().lower()
    t = re.sub(r"[^a-z0-9\s-]", "", t)
    t = re.sub(r"\s+", "-", t)
    t = re.sub(r"-+", "-", t)
    return t.strip("-")


def find_placeholders(artifact_text: str) -> List[Dict[str, object]]:
    """
    Find placeholder keywords (TODO, TBD, FIXME, etc.) in text.
    
    Returns list of {line, text} dicts for each placeholder found.
    """
    hits: List[Dict[str, object]] = []
    for idx, line in enumerate(artifact_text.splitlines(), start=1):
        if PLACEHOLDER_RE.search(line):
            hits.append({"line": idx, "text": line})
    return hits
