import argparse
import fnmatch
import json
import os
import re
import sys
from pathlib import Path
from typing import Dict, List, Optional, Tuple


PROJECT_CONFIG_FILENAME = ".fdd-config.json"


def _cfg_get_str(cfg: object, *keys: str) -> Optional[str]:
    if not isinstance(cfg, dict):
        return None
    for k in keys:
        v = cfg.get(k)
        if isinstance(v, str) and v.strip():
            return v.strip()
    return None


def _find_project_root(start: Path) -> Optional[Path]:
    current = start.resolve()
    for _ in range(25):
        if (current / PROJECT_CONFIG_FILENAME).is_file():
            return current

        git_marker = current / ".git"
        if git_marker.exists():
            return current

        parent = current.parent
        if parent == current:
            break
        current = parent
    return None


def _load_project_config(project_root: Path) -> Optional[dict]:
    path = (project_root / PROJECT_CONFIG_FILENAME)
    if not path.is_file():
        return None
    try:
        raw = path.read_text(encoding="utf-8")
        cfg = json.loads(raw)
    except Exception:
        return None
    return cfg if isinstance(cfg, dict) else None


def _fdd_root_from_project_config() -> Optional[Path]:
    project_root = _find_project_root(Path.cwd())
    if project_root is None:
        return None

    cfg = _load_project_config(project_root)
    if cfg is None:
        return None

    # Canonical keys (camelCase), plus a couple of permissive variants.
    core_rel = _cfg_get_str(cfg, "fddCorePath", "fdd_core_path", "fddCoreDir")
    if core_rel is None:
        return None

    core = (project_root / core_rel).resolve()
    if (core / "AGENTS.md").exists() and (core / "requirements").is_dir() and (core / "workflows").is_dir():
        return core
    return None


def _find_adapter_directory(start: Path, fdd_root: Optional[Path] = None) -> Optional[Path]:
    """
    Find FDD-Adapter directory starting from project root.
    Uses smart recursive search to find adapter in ANY location within project.
    
    Heuristic:
    1. Check explicit config first (fddAdapterPath)
    2. Recursively search for directories with AGENTS.md + specs/
    3. Prefer shallower directories (closer to root)
    4. Skip common non-adapter directories
    
    Args:
        start: Starting path for search
        fdd_root: Known FDD core location (from agent context)
    """
    project_root = _find_project_root(start)
    if project_root is None:
        return None
    
    # PRIORITY 1: Check config first - explicit path always wins
    cfg = _load_project_config(project_root)
    if cfg is not None:
        adapter_rel = cfg.get("fddAdapterPath")
        if adapter_rel is not None and isinstance(adapter_rel, str):
            # Config exists and specifies adapter path
            adapter_dir = (project_root / adapter_rel).resolve()
            if (adapter_dir / "AGENTS.md").exists():
                return adapter_dir
            # Config path is invalid - DO NOT fallback to recursive search
            # This is a configuration error that must be fixed
            return None
    
    # PRIORITY 2: Recursive search (only if no config exists)
    skip_dirs = {
        ".git", "node_modules", "venv", "__pycache__", ".pytest_cache",
        "target", "build", "dist", ".idea", ".vscode", "vendor",
        "coverage", ".tox", ".mypy_cache", ".eggs"
    }
    
    def is_adapter_directory(path: Path) -> bool:
        """Check if directory looks like FDD-Adapter."""
        agents_file = path / "AGENTS.md"
        if not agents_file.exists():
            return False
        
        # Check AGENTS.md content
        try:
            content = agents_file.read_text(encoding="utf-8")
            
            # STRONGEST indicator: Extends FDD AGENTS.md
            # Example: **Extends**: `../.fdd/AGENTS.md`
            if "**Extends**:" in content and "AGENTS.md" in content:
                # If agent provided fdd_root, validate the Extends path
                if fdd_root is not None:
                    # Extract Extends path from content
                    import re
                    extends_match = re.search(r'\*\*Extends\*\*:\s*`([^`]+)`', content)
                    if extends_match:
                        extends_path = extends_match.group(1)
                        # Resolve relative to adapter directory
                        resolved = (path / extends_path).resolve()
                        # Check if it points to fdd_root
                        if resolved.parent == fdd_root or (fdd_root / "AGENTS.md") == resolved:
                            return True
                # Even without fdd_root validation, Extends is strong signal
                return True
            
            # Look for adapter-specific markers in content
            adapter_markers = [
                "# FDD Adapter:",
                "FDD-Adapter",
                "fdd-adapter",
                "## FDD Adapter",
                "This is an FDD adapter",
                "adapter for",
            ]
            content_lower = content.lower()
            for marker in adapter_markers:
                if marker.lower() in content_lower:
                    # Double-check with specs/ directory if possible
                    if (path / "specs").is_dir():
                        return True
                    # Or check for spec references in content
                    if "spec" in content_lower or "specifications" in content_lower:
                        return True
        except Exception:
            pass
        
        # Fallback: verify it has specs/ directory (strong structural indicator)
        if (path / "specs").is_dir():
            return True
        
        return False
    
    def search_recursive(root: Path, max_depth: int = 5, current_depth: int = 0) -> Optional[Path]:
        """Recursively search for adapter directory."""
        if current_depth > max_depth:
            return None
        
        try:
            entries = list(root.iterdir())
        except (PermissionError, OSError):
            return None
        
        # First pass: check current level directories
        for entry in entries:
            if not entry.is_dir() or entry.name in skip_dirs:
                continue
            if is_adapter_directory(entry):
                return entry
        
        # Second pass: recurse into subdirectories (breadth-first preference)
        for entry in entries:
            if not entry.is_dir() or entry.name in skip_dirs:
                continue
            result = search_recursive(entry, max_depth, current_depth + 1)
            if result is not None:
                return result
        
        return None
    
    return search_recursive(project_root)


def _load_adapter_config(adapter_dir: Path) -> Dict[str, object]:
    """
    Load adapter configuration from AGENTS.md and specs/
    Returns dict with adapter metadata and available specs
    """
    config: Dict[str, object] = {
        "adapter_dir": adapter_dir.as_posix(),
        "specs": [],
    }
    
    agents_file = adapter_dir / "AGENTS.md"
    if agents_file.exists():
        try:
            content = agents_file.read_text(encoding="utf-8")
            # Extract project name from heading
            for line in content.splitlines():
                if line.startswith("# FDD Adapter:"):
                    config["project_name"] = line.replace("# FDD Adapter:", "").strip()
                    break
        except Exception:
            pass
    
    # List available specs
    specs_dir = adapter_dir / "specs"
    if specs_dir.is_dir():
        spec_files = []
        for spec_file in specs_dir.glob("*.md"):
            spec_files.append(spec_file.stem)
        config["specs"] = sorted(spec_files)
    
    return config


def _fdd_root_from_this_file() -> Path:
    """
    Find FDD root by walking up directory tree looking for FDD markers.
    FDD can be located anywhere (as submodule, copied, etc.)
    """
    configured = _fdd_root_from_project_config()
    if configured is not None:
        return configured

    current = Path(__file__).resolve().parent
    
    # Walk up directory tree looking for FDD root markers
    for _ in range(10):  # Limit search depth to avoid infinite loop
        # Check for FDD root markers: AGENTS.md + requirements/ + workflows/
        if (
            (current / "AGENTS.md").exists() and
            (current / "requirements").is_dir() and
            (current / "workflows").is_dir()
        ):
            return current
        
        parent = current.parent
        if parent == current:  # Reached filesystem root
            break
        current = parent
    
    # Fallback to old behavior if markers not found
    return Path(__file__).resolve().parents[3]


def detect_requirements(artifact_path: Path) -> Tuple[str, Path]:
    name = artifact_path.name

    if re.match(r"^\d{4}-\d{2}-\d{2}-CHANGES\.md$", name):
        return "feature-changes", _fdd_root_from_this_file() / "requirements" / "feature-changes-structure.md"
    fdd_root = _fdd_root_from_this_file()

    def req(rel: str) -> Path:
        return (fdd_root / rel).resolve()

    if name == "BUSINESS.md":
        return "business-context", req("requirements/business-context-structure.md")

    if name == "ADR.md":
        return "adr", req("requirements/adr-structure.md")

    if name == "FEATURES.md":
        return "features-manifest", req("requirements/features-manifest-structure.md")

    if name == "CHANGES.md":
        return "feature-changes", req("requirements/feature-changes-structure.md")

    if name == "DESIGN.md":
        parts = list(artifact_path.parts)
        is_feature_scope = any(p.startswith("feature-") for p in parts) and "features" in parts
        if is_feature_scope:
            return "feature-design", req("requirements/feature-design-structure.md")
        return "overall-design", req("requirements/overall-design-structure.md")

    raise ValueError(f"Unsupported artifact name: {name}")


SECTION_RE = re.compile(r"^###\s+Section\s+([A-Z0-9]+):\s+(.+?)\s*$")


def parse_required_sections(requirements_path: Path) -> Dict[str, str]:
    sections: Dict[str, str] = {}
    for line in requirements_path.read_text(encoding="utf-8").splitlines():
        m = SECTION_RE.match(line)
        if not m:
            continue
        section_id = m.group(1)
        section_title = m.group(2)
        sections[section_id] = section_title
    return sections


HEADING_ID_RE = re.compile(r"^#{1,6}\s+([A-Z])\.\s+.*$")


def find_present_section_ids(artifact_text: str) -> List[str]:
    present = []
    for line in artifact_text.splitlines():
        m = HEADING_ID_RE.match(line)
        if m:
            present.append(m.group(1))
    return present


PLACEHOLDER_RE = re.compile(r"\b(TODO|TBD|FIXME|XXX|TBA)\b", re.IGNORECASE)

REQ_ID_RE = re.compile(r"\bfdd-[a-z0-9-]+-req-[a-z0-9-]+\b")
NFR_ID_RE = re.compile(r"\bfdd-[a-z0-9-]+-nfr-[a-z0-9-]+\b")
PRINCIPLE_ID_RE = re.compile(r"\bfdd-[a-z0-9-]+-principle-[a-z0-9-]+\b")
CONSTRAINT_ID_RE = re.compile(r"\bfdd-[a-z0-9-]+-constraint-[a-z0-9-]+\b")
ACTOR_ID_RE = re.compile(r"\bfdd-[a-z0-9-]+-actor-[a-z0-9-]+\b")
CAPABILITY_ID_RE = re.compile(r"\bfdd-[a-z0-9-]+-capability-[a-z0-9-]+\b")
USECASE_ID_RE = re.compile(r"\bfdd-[a-z0-9-]+-usecase-[a-z0-9-]+\b")


def find_placeholders(artifact_text: str) -> List[Dict[str, object]]:
    hits: List[Dict[str, object]] = []
    for idx, line in enumerate(artifact_text.splitlines(), start=1):
        if PLACEHOLDER_RE.search(line):
            hits.append({"line": idx, "text": line})
    return hits


STATUS_OVERVIEW_RE = re.compile(
    r"\*\*Status Overview\*\*:\s*(\d+)\s+features\s+total\s*\(\s*(\d+)\s+completed,\s*(\d+)\s+in progress,\s*(\d+)\s+not started\s*\)"
)


LINK_RE = re.compile(r"\[([^\]]+)\]\(([^)]+)\)")

DISALLOWED_LINK_TOKEN_RE = re.compile(r"(@/|@DESIGN\.md|@BUSINESS\.md|@ADR\.md)")
HTML_COMMENT_RE = re.compile(r"<!--.*?-->", re.DOTALL)
BRACE_PLACEHOLDER_RE = re.compile(r"\{[A-Za-z0-9_-]+\}")
SIZE_HARD_LIMIT_RE = re.compile(r"Hard limit:\s*≤?\s*(\d+)\s*lines", re.IGNORECASE)
ID_LINE_RE = re.compile(r"\*\*ID\*\*:\s*(.+)$")
FDD_ANY_ID_RE = re.compile(r"\bfdd-[a-z0-9-]+\b")


SECTION_FEATURE_RE = re.compile(r"^##\s+([A-G])\.\s+(.+?)\s*$")
FDL_STEP_LINE_RE = re.compile(r"^\s*(?:\d+\.|-)\s+\[[ xX]\]\s+-\s+`ph-\d+`\s+-\s+.+?\s+-\s+`inst-[a-z0-9-]+`\s*$")
FEATURE_FLOW_ID_RE = re.compile(r"\bfdd-[a-z0-9-]+-feature-([a-z0-9-]+)-flow-[a-z0-9-]+\b")
FEATURE_ALGO_ID_RE = re.compile(r"\bfdd-[a-z0-9-]+-feature-([a-z0-9-]+)-algo-[a-z0-9-]+\b")
FEATURE_STATE_ID_RE = re.compile(r"\bfdd-[a-z0-9-]+-feature-([a-z0-9-]+)-state-[a-z0-9-]+\b")
FEATURE_REQ_ID_RE = re.compile(r"\bfdd-[a-z0-9-]+-feature-([a-z0-9-]+)-req-[a-z0-9-]+\b")
FEATURE_TEST_ID_RE = re.compile(r"\bfdd-[a-z0-9-]+-feature-([a-z0-9-]+)-test-[a-z0-9-]+\b")


CHANGES_HEADER_TITLE_RE = re.compile(r"^#\s+Implementation\s+Plan:\s+.+$", re.IGNORECASE)
CHANGE_HEADING_RE = re.compile(r"^##\s+Change\s+(\d+):\s+(.+?)\s*$")
CHANGE_ID_RE = re.compile(r"\bfdd-[a-z0-9-]+-feature-([a-z0-9-]+)-change-[a-z0-9-]+\b")
CHANGE_STATUS_RE = re.compile(r"^(?:⏳\s+NOT_STARTED|🔄\s+IN_PROGRESS|✅\s+COMPLETED|📦\s+ARCHIVED)$")
CHANGE_PRIORITY_RE = re.compile(r"^(?:HIGH|MEDIUM|LOW)$")
PHASE_TOKEN_RE = re.compile(r"\bph-(\d+)\b")
CHANGE_TASK_LINE_RE = re.compile(r"^\s*-\s+\[[ xX]\]\s+(\d+(?:\.\d+)+)\s+(.+?)\s*$")


FDD_TAG_CHANGE_RE = re.compile(r"@fdd-change:(fdd-[a-z0-9-]+):ph-(\d+)")
FDD_TAG_FLOW_RE = re.compile(r"@fdd-flow:(fdd-[a-z0-9-]+):ph-(\d+)")
FDD_TAG_ALGO_RE = re.compile(r"@fdd-algo:(fdd-[a-z0-9-]+):ph-(\d+)")
FDD_TAG_STATE_RE = re.compile(r"@fdd-state:(fdd-[a-z0-9-]+):ph-(\d+)")
FDD_TAG_REQ_RE = re.compile(r"@fdd-req:(fdd-[a-z0-9-]+):ph-(\d+)")
FDD_TAG_TEST_RE = re.compile(r"@fdd-test:(fdd-[a-z0-9-]+):ph-(\d+)")


SCOPE_ID_BY_KIND_RE: Dict[str, re.Pattern] = {
    "flow": re.compile(r"\bfdd-[a-z0-9-]+-feature-[a-z0-9-]+-flow-[a-z0-9-]+\b"),
    "algo": re.compile(r"\bfdd-[a-z0-9-]+-feature-[a-z0-9-]+-algo-[a-z0-9-]+\b"),
    "state": re.compile(r"\bfdd-[a-z0-9-]+-feature-[a-z0-9-]+-state-[a-z0-9-]+\b"),
    "req": re.compile(r"\bfdd-[a-z0-9-]+-feature-[a-z0-9-]+-req-[a-z0-9-]+\b"),
    "test": re.compile(r"\bfdd-[a-z0-9-]+-feature-[a-z0-9-]+-test-[a-z0-9-]+\b"),
}


def _split_by_section_letter(text: str, section_re: re.Pattern) -> Tuple[List[str], Dict[str, List[str]]]:
    """
    Split text by lettered sections using provided regex pattern.
    
    Args:
        text: Text to split
        section_re: Compiled regex pattern to match section headers
    
    Returns:
        Tuple of (section_order, section_dict)
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


def _split_by_feature_section_letter(text: str) -> Tuple[List[str], Dict[str, List[str]]]:
    """Split feature DESIGN.md by section letters (A-F)."""
    return _split_by_section_letter(text, SECTION_FEATURE_RE)


def _slugify_anchor(text: str) -> str:
    t = re.sub(r"`[^`]*`", "", text)
    t = t.strip().lower()
    t = re.sub(r"[^a-z0-9\s-]", "", t)
    t = re.sub(r"\s+", "-", t)
    t = re.sub(r"-+", "-", t)
    return t.strip("-")


def extract_fdl_instructions(text: str) -> Dict[str, Dict[str, List[str]]]:
    """
    Extract FDL instruction IDs marked as implemented [x] from feature design.
    
    Returns:
        Dict with structure:
        {
            "fdd-{project}-{type}-{name}": {
                "instructions": ["inst-id-1", "inst-id-2", ...],  # Only [x] marked
                "completed": ["inst-id-1", ...]  # Same as instructions (kept for compatibility)
            }
        }
    """
    result: Dict[str, Dict[str, List[str]]] = {}
    current_scope_id: Optional[str] = None
    
    for line in text.splitlines():
        # Match FDL scope ID line: - [ ] **ID**: `fdd-{project}-{type}-{name}`
        if FDL_SCOPE_ID_RE.match(line):
            m = re.search(r"`(fdd-[a-z0-9-]+)`", line)
            if m:
                current_scope_id = m.group(1)
                if current_scope_id not in result:
                    result[current_scope_id] = {"instructions": [], "completed": []}
        
        # Extract instruction IDs ONLY from [x] marked FDL step lines
        if current_scope_id and FDL_STEP_LINE_RE.match(line):
            # Check if marked as implemented [x]
            if re.match(r"^\s*\d+\.\s*\[x\]", line, re.I):
                m_inst = re.search(r"`(inst-[a-z0-9-]+)`\s*$", line.strip())
                if m_inst:
                    inst_id = m_inst.group(1)
                    result[current_scope_id]["instructions"].append(inst_id)
                    result[current_scope_id]["completed"].append(inst_id)
    
    return result


def extract_scope_references_from_changes(text: str) -> set:
    """
    Extract all FDL scope IDs (flow/algo/state/test) referenced in CHANGES.md.
    """
    scope_ids: set = set()
    
    # Extract from task descriptions and references sections
    flow_ids = re.findall(r"`(fdd-[a-z0-9-]+-(?:flow|algo|state|test)-[a-z0-9-]+)`", text)
    scope_ids.update(flow_ids)
    
    return scope_ids


def validate_fdl_coverage(
    changes_text: str,
    design_fdl: Dict[str, Dict[str, List]]
) -> List[Dict[str, object]]:
    """
    Validate that CHANGES.md references all FDL scopes (flows/algos/states/tests) from DESIGN.md.
    """
    errors: List[Dict[str, object]] = []
    
    # Extract all scope IDs mentioned in CHANGES.md
    referenced_scopes = extract_scope_references_from_changes(changes_text)
    
    # Check that each FDL scope is referenced
    for scope_id in design_fdl.keys():
        if scope_id not in referenced_scopes:
            errors.append({
                "type": "fdl_coverage",
                "message": f"FDL scope '{scope_id}' from DESIGN.md not referenced in CHANGES.md",
                "scope_id": scope_id
            })
    
    return errors


def extract_inst_tags_from_code(feature_root: Path) -> Dict[str, Dict[str, bool]]:
    """
    Scan codebase for FDL instruction tags in format: fdd-begin:@fdd-*:...:ph-N:inst-{id} / fdd-end:@fdd-*:...:ph-N:inst-{id}
    
    Returns:
        Dict mapping inst-{id} to {"has_begin": bool, "has_end": bool, "complete": bool}
    """
    inst_tags: Dict[str, Dict[str, bool]] = {}
    
    # File extensions to scan
    code_extensions = {".py", ".rs", ".ts", ".tsx", ".js", ".jsx", ".go", ".java", ".cs", ".sql", ".md"}
    
    # Skip directories
    skip_dirs = {".git", "node_modules", "venv", "__pycache__", ".pytest_cache", "target", "build", "dist"}
    
    def scan_file(file_path: Path) -> None:
        try:
            content = file_path.read_text(encoding="utf-8", errors="ignore")
            
            # Match: fdd-begin fdd-...:ph-N:inst-{id}
            # Pattern: fdd-begin followed by anything then inst-{id}
            begin_pattern = r'fdd-begin\s+.*?(inst-[a-z0-9-]+)'
            begin_matches = re.findall(begin_pattern, content)
            
            # Match: fdd-end fdd-...:ph-N:inst-{id}
            end_pattern = r'fdd-end\s+.*?(inst-[a-z0-9-]+)'
            end_matches = re.findall(end_pattern, content)
            
            # Record findings
            for inst_id in begin_matches:
                if inst_id not in inst_tags:
                    inst_tags[inst_id] = {"has_begin": False, "has_end": False, "complete": False}
                inst_tags[inst_id]["has_begin"] = True
            
            for inst_id in end_matches:
                if inst_id not in inst_tags:
                    inst_tags[inst_id] = {"has_begin": False, "has_end": False, "complete": False}
                inst_tags[inst_id]["has_end"] = True
            
        except Exception:
            pass
    
    def scan_directory(directory: Path) -> None:
        try:
            for item in directory.iterdir():
                if item.is_dir():
                    if item.name not in skip_dirs:
                        scan_directory(item)
                elif item.is_file() and item.suffix in code_extensions:
                    scan_file(item)
        except (PermissionError, OSError):
            pass
    
    # Start scanning from feature root or project root
    if feature_root and feature_root.exists():
        # Scan from project root (parent of architecture/features/feature-X)
        project_root = feature_root.parent.parent.parent
        if project_root.exists():
            scan_directory(project_root)
    
    # Mark complete if both begin and end tags present
    for inst_id in inst_tags:
        inst_tags[inst_id]["complete"] = inst_tags[inst_id]["has_begin"] and inst_tags[inst_id]["has_end"]
    
    return inst_tags


def validate_fdl_code_to_design(
    feature_root: Path,
    design_text: str
) -> List[Dict[str, object]]:
    """
    Reverse validation: Check that all fdd tags in code are marked [x] in DESIGN.md.
    
    If code has fdd-begin/fdd-end tags but instruction is not marked [x],
    this means implementation exists but not documented as complete.
    """
    errors: List[Dict[str, object]] = []
    
    # Extract all inst-{id} tags from code
    code_inst_tags = extract_inst_tags_from_code(feature_root)
    
    # Extract all [x] marked instructions from DESIGN.md
    design_fdl = extract_fdl_instructions(design_text)
    
    # Build set of all [x] marked inst-ids from DESIGN
    marked_instructions = set()
    for scope_id, data in design_fdl.items():
        marked_instructions.update(data["instructions"])
    
    # Find tags in code that are NOT marked [x] in DESIGN
    untracked_implementations = []
    for inst_id, tag_info in code_inst_tags.items():
        if tag_info["complete"] and inst_id not in marked_instructions:
            untracked_implementations.append(inst_id)
    
    if untracked_implementations:
        errors.append({
            "type": "fdl_untracked_implementation",
            "message": f"Found {len(untracked_implementations)} fdd tags in code not marked [x] in DESIGN.md",
            "count": len(untracked_implementations),
            "instructions": untracked_implementations[:10],
            "suggestion": "Mark these instructions as [x] in DESIGN.md or remove tags from code"
        })
    
    return errors


def validate_fdl_code_implementation(
    feature_root: Path,
    design_fdl: Dict[str, Dict[str, List]]
) -> List[Dict[str, object]]:
    """
    Validate that all FDL instructions from DESIGN.md are implemented in code.
    
    Checks for presence of paired fdd-begin/fdd-end blocks wrapping implementation code.
    """
    errors: List[Dict[str, object]] = []
    
    # Extract all inst-{id} tags from code with begin/end status
    code_inst_tags = extract_inst_tags_from_code(feature_root)
    
    # Collect missing and incomplete implementations
    missing_implementations: List[Tuple[str, str]] = []
    incomplete_implementations: List[Tuple[str, str, str]] = []  # (scope, inst, reason)
    
    for scope_id, data in design_fdl.items():
        for inst_id in data["instructions"]:
            if inst_id not in code_inst_tags:
                # Completely missing
                missing_implementations.append((scope_id, inst_id))
            elif not code_inst_tags[inst_id]["complete"]:
                # Present but incomplete (missing begin or end tag)
                if not code_inst_tags[inst_id]["has_begin"]:
                    reason = "missing fdd-begin tag"
                elif not code_inst_tags[inst_id]["has_end"]:
                    reason = "missing fdd-end tag"
                else:
                    reason = "incomplete"
                incomplete_implementations.append((scope_id, inst_id, reason))
    
    if missing_implementations:
        errors.append({
            "type": "fdl_code_missing",
            "message": f"FDL instructions not found in code (missing {len(missing_implementations)} inst-{{id}} implementations)",
            "missing_count": len(missing_implementations),
            "examples": [
                {"scope": scope, "instruction": inst}
                for scope, inst in missing_implementations[:10]
            ]
        })
    
    if incomplete_implementations:
        errors.append({
            "type": "fdl_code_incomplete",
            "message": f"FDL instructions have incomplete fdd-begin/fdd-end pairs ({len(incomplete_implementations)} instructions)",
            "incomplete_count": len(incomplete_implementations),
            "examples": [
                {"scope": scope, "instruction": inst, "reason": reason}
                for scope, inst, reason in incomplete_implementations[:10]
            ]
        })
    
    return errors


def validate_fdl_completion(
    changes_text: str,
    design_fdl: Dict[str, Dict[str, List]]
) -> List[Dict[str, object]]:
    """
    Validate that COMPLETED feature has all FDL instructions marked [x] in DESIGN.md.
    """
    errors: List[Dict[str, object]] = []
    
    # Check if feature is marked as COMPLETED
    status_match = re.search(r"\*\*Status\*\*:\s*(✅\s*COMPLETED|🔄\s*IN_PROGRESS|⏳\s*NOT_STARTED|✨\s*IMPLEMENTED)", changes_text)
    if not status_match:
        return errors
    
    status = status_match.group(1).strip()
    if not status:
        return errors
    
    # For IMPLEMENTED status, verify all [x] instructions have fdd-begin/end tags in code
    if status == "IMPLEMENTED" and feature_root:
        code_inst_tags = extract_inst_tags_from_code(feature_root)
        
        missing_implementations = []
        incomplete_implementations = []
        
        for scope_id, data in design_fdl.items():
            for inst_id in data["instructions"]:
                if inst_id not in code_inst_tags:
                    missing_implementations.append((scope_id, inst_id))
                elif not code_inst_tags[inst_id]["complete"]:
                    incomplete_implementations.append((scope_id, inst_id))
        
        if missing_implementations or incomplete_implementations:
            errors.append({
                "type": "fdl_implemented_incomplete",
                "message": f"Feature status is IMPLEMENTED but {len(missing_implementations)} [x] instructions missing fdd tags and {len(incomplete_implementations)} have incomplete tags",
                "missing_count": len(missing_implementations),
                "incomplete_count": len(incomplete_implementations),
                "examples": [
                    {"scope": s, "instruction": i, "issue": "missing tags"}
                    for s, i in missing_implementations[:5]
                ] + [
                    {"scope": s, "instruction": i, "issue": "incomplete tags"}
                    for s, i in incomplete_implementations[:5]
                ]
            })
        
        return errors
    
    # For COMPLETED/DESIGNED status, verify design completeness
    uncompleted_instructions: List[Tuple[str, str]] = []
    for scope_id, data in design_fdl.items():
        for i, inst_id in enumerate(data["instructions"]):
            if not data["completed"][i]:
                uncompleted_instructions.append((scope_id, inst_id))
    
    if uncompleted_instructions:
        errors.append({
            "type": "premature_completion",
            "message": "Feature marked COMPLETED but FDL instructions not all implemented ([x])",
            "uncompleted_count": len(uncompleted_instructions),
            "examples": [
                {"scope": scope, "instruction": inst}
                for scope, inst in uncompleted_instructions[:10]
            ]
        })
    
    return errors


# fdd-begin fdd-fdd-feature-core-methodology-algo-validate-structure:ph-1:inst-read-artifact
def validate_feature_design(
    artifact_text: str,
    *,
    artifact_path: Optional[Path] = None,
    skip_fs_checks: bool = False,
) -> Dict[str, object]:
    errors: List[Dict[str, object]] = []
    placeholders = find_placeholders(artifact_text)
    section_order, sections = _split_by_feature_section_letter(artifact_text)
    
    expected = ["A", "B", "C", "D", "E", "F"]
    if "G" in sections:
        expected.append("G")
    if section_order and section_order[: len(expected)] != expected:
        errors.append({"type": "structure", "message": "Section order invalid", "required_order": expected, "found_order": section_order})

    feature_slug: Optional[str] = None
    if artifact_path is not None:
        parent = artifact_path.parent.name
        if parent.startswith("feature-"):
            feature_slug = parent[len("feature-") :]

    def _extract_full_ids(line: str, kind: str) -> List[str]:
        ids: List[str] = []
        pat = {
            "flow": re.compile(r"\bfdd-[a-z0-9-]+-feature-[a-z0-9-]+-flow-[a-z0-9-]+\b"),
            "algo": re.compile(r"\bfdd-[a-z0-9-]+-feature-[a-z0-9-]+-algo-[a-z0-9-]+\b"),
            "state": re.compile(r"\bfdd-[a-z0-9-]+-feature-[a-z0-9-]+-state-[a-z0-9-]+\b"),
            "req": re.compile(r"\bfdd-[a-z0-9-]+-feature-[a-z0-9-]+-req-[a-z0-9-]+\b"),
            "test": re.compile(r"\bfdd-[a-z0-9-]+-feature-[a-z0-9-]+-test-[a-z0-9-]+\b"),
        }[kind]

        for tok in re.findall(r"`([^`]+)`", line):
            if pat.fullmatch(tok.strip()):
                ids.append(tok.strip())

        for m in pat.finditer(line):
            ids.append(m.group(0))

        dedup: List[str] = []
        for x in ids:
            if x not in dedup:
                dedup.append(x)
        return dedup

    def _check_section_fdl(section_letter: str, kind: str) -> Tuple[set, set]:
        lines = sections.get(section_letter, [])
        ids: set = set()
        phases: set = set()

        current_scope_id: Optional[str] = None
        scope_inst_seen: set = set()

        in_code = False
        for idx, line in enumerate(lines, start=1):
            if line.strip().startswith("```"):
                in_code = not in_code
                errors.append({"type": "fdl", "message": f"Code blocks are not allowed in Section {section_letter}", "line": idx, "text": line.strip()})
                continue
            if in_code:
                continue

            if "**WHEN**" in line and section_letter in ("B", "C"):
                errors.append({"type": "fdl", "message": "**WHEN** is only allowed in state machines (Section D)", "section": section_letter, "line": idx, "text": line.strip()})

            bad_bold = re.findall(r"\*\*([A-Z ]+)\*\*", line)
            prohibited = {"THEN", "SET", "VALIDATE", "CHECK", "LOAD", "READ", "WRITE", "CREATE", "ADD"}
            if section_letter in ("B", "C"):
                prohibited.add("WHEN")
                prohibited.add("AND")
            for tok in bad_bold:
                t = tok.strip()
                if t in prohibited:
                    errors.append({"type": "fdl", "message": "Prohibited bold keyword in FDL", "section": section_letter, "keyword": t, "line": idx, "text": line.strip()})

            if section_letter in ("C",) and re.search(r"\b(fn|function|def|class|interface)\b", line, re.IGNORECASE):
                errors.append({"type": "fdl", "message": "Programming syntax is not allowed in algorithms", "section": section_letter, "line": idx, "text": line.strip()})

            if "**ID**:" in line:
                if not re.match(r"^\s*[-*]\s+\[[ xX]\]\s+\*\*ID\*\*:\s+", line):
                    errors.append({"type": "id", "message": "ID line must be a checkbox list item", "section": section_letter, "line": idx, "text": line.strip()})

                for fid in _extract_full_ids(line, kind):
                    ids.add(fid)

                if kind == "algo":
                    scope_ids = _extract_full_ids(line, kind)
                    current_scope_id = scope_ids[0] if scope_ids else None
                    scope_inst_seen = set()

                if feature_slug is not None:
                    m_kind = {
                        "flow": FEATURE_FLOW_ID_RE,
                        "algo": FEATURE_ALGO_ID_RE,
                        "state": FEATURE_STATE_ID_RE,
                    }[kind]
                    for m in m_kind.finditer(line):
                        if m.group(1) != feature_slug:
                            errors.append({"type": "id", "message": "Feature slug in ID does not match directory slug", "section": section_letter, "expected": feature_slug, "found": m.group(1), "line": idx, "text": line.strip()})

            m_ph = re.findall(r"`ph-(\d+)`", line)
            for n in m_ph:
                phases.add(int(n))

            if re.match(r"^\s*\d+\.\s+", line):
                if not FDL_STEP_LINE_RE.match(line):
                    errors.append({"type": "fdl", "message": "Invalid FDL step line format", "section": section_letter, "line": idx, "text": line.strip()})
                elif kind == "algo" and current_scope_id is not None:
                    m_inst = re.search(r"`(inst-[a-z0-9-]+)`\s*$", line.strip())
                    if m_inst:
                        inst_id = m_inst.group(1)
                        if inst_id in scope_inst_seen:
                            errors.append(
                                {
                                    "type": "fdl",
                                    "message": "Duplicate FDL instruction IDs within algorithm",
                                    "section": section_letter,
                                    "line": idx,
                                    "algorithm_id": current_scope_id,
                                    "inst": inst_id,
                                }
                            )
                        scope_inst_seen.add(inst_id)
            if re.match(r"^\s*-\s+\[[ xX]\]\s+-\s+", line):
                if not FDL_STEP_LINE_RE.match(line):
                    errors.append({"type": "fdl", "message": "Invalid FDL step line format", "section": section_letter, "line": idx, "text": line.strip()})
                elif kind == "algo" and current_scope_id is not None:
                    m_inst = re.search(r"`(inst-[a-z0-9-]+)`\s*$", line.strip())
                    if m_inst:
                        inst_id = m_inst.group(1)
                        if inst_id in scope_inst_seen:
                            errors.append(
                                {
                                    "type": "fdl",
                                    "message": "Duplicate FDL instruction IDs within algorithm",
                                    "section": section_letter,
                                    "line": idx,
                                    "algorithm_id": current_scope_id,
                                    "inst": inst_id,
                                }
                            )
                        scope_inst_seen.add(inst_id)

        return ids, phases

    flow_ids: set = set()
    algo_ids: set = set()
    state_ids: set = set()
    phase_nums: set = set()

    if "B" in sections:
        flow_ids, ph = _check_section_fdl("B", "flow")
        phase_nums |= ph
    if "C" in sections:
        algo_ids, ph = _check_section_fdl("C", "algo")
        phase_nums |= ph
    if "D" in sections:
        state_ids, ph = _check_section_fdl("D", "state")
        phase_nums |= ph

    anchors: set = set()
    for line in artifact_text.splitlines():
        m = re.match(r"^###\s+(.+?)\s*$", line.strip())
        if not m:
            continue
        anchors.add(_slugify_anchor(m.group(1)))

    if "A" in sections:
        a_text = "\n".join(sections["A"])
        for sub in ("### 1. Overview", "### 2. Purpose", "### 3. Actors", "### 4. References"):
            if sub not in a_text:
                errors.append({"type": "structure", "message": "Missing required subsection in Section A", "section": "A", "subsection": sub})

        actors_block = a_text.split("### 3. Actors", 1)[1] if "### 3. Actors" in a_text else ""
        if "### 4. References" in actors_block:
            actors_block = actors_block.split("### 4. References", 1)[0]
        actor_lines = [l.strip() for l in actors_block.splitlines() if re.match(r"^\s*[-*]\s+\S+", l)]
        actor_ids: List[str] = []
        for l in actor_lines:
            m = re.search(r"`(fdd-[a-z0-9-]+-actor-[a-z0-9-]+)`", l)
            if not m:
                errors.append({"type": "id", "message": "Section A Actors must be FDD actor IDs wrapped in backticks", "section": "A", "text": l.strip()})
                continue
            actor_ids.append(m.group(1))

        if not skip_fs_checks and artifact_path is not None:
            bp = artifact_path.parents[2] / "BUSINESS.md"
            bt, berr = _load_text(bp)
            if berr:
                errors.append({"type": "cross", "message": berr})
            else:
                if actor_ids:
                    business_actor_ids = set(re.findall(r"`(fdd-[a-z0-9-]+-actor-[a-z0-9-]+)`", bt or ""))
                    unknown_ids = sorted([a for a in actor_ids if a not in business_actor_ids])
                    if business_actor_ids and unknown_ids:
                        errors.append({"type": "cross", "message": "Actor IDs must match BUSINESS.md actor IDs", "section": "A", "actors": unknown_ids})

            fp = artifact_path.parents[1] / "FEATURES.md"
            ft, ferr = _load_text(fp)
            if ferr:
                errors.append({"type": "cross", "message": ferr})
            else:
                feature_id = None
                m_fid = re.search(r"\*\*Feature ID\*\*:\s*`([^`]+)`", a_text)
                if m_fid:
                    feature_id = m_fid.group(1).strip()
                if feature_id and feature_id not in ft:
                    errors.append({"type": "cross", "message": "Feature ID not found in FEATURES.md", "feature_id": feature_id})

    if "F" in sections:
        f_lines = sections["F"]
        req_indices: List[int] = []
        for idx, line in enumerate(f_lines):
            if line.strip().startswith("### "):
                req_indices.append(idx)

        if not req_indices:
            errors.append({"type": "content", "message": "Section F must contain at least one requirement heading", "section": "F"})
        else:
            req_ids: set = set()
            test_ids: set = set()

            for i, start in enumerate(req_indices):
                end = req_indices[i + 1] if i + 1 < len(req_indices) else len(f_lines)
                block = f_lines[start:end]
                block_text = "\n".join(block)

                id_line = next((l for l in block if "**ID**:" in l), None)
                if id_line is None:
                    errors.append({"type": "id", "message": "Requirement missing ID line", "section": "F", "line": start + 1})
                else:
                    if not re.match(r"^\s*[-*]\s+\[[ xX]\]\s+\*\*ID\*\*:\s+", id_line):
                        errors.append({"type": "id", "message": "Requirement ID line must be a checkbox list item", "section": "F", "line": start + 1, "text": id_line.strip()})

                    for m in FEATURE_REQ_ID_RE.finditer(id_line):
                        if feature_slug is not None and m.group(1) != feature_slug:
                            errors.append({"type": "id", "message": "Feature slug in requirement ID does not match directory slug", "section": "F", "expected": feature_slug, "found": m.group(1), "line": start + 1})
                    for rid in _extract_full_ids(id_line, "req"):
                        req_ids.add(rid)

                required_fields = ["Status", "Description", "References", "Implements", "Phases"]
                for field in required_fields:
                    fb = _field_block(block, field)
                    if fb is None:
                        errors.append({"type": "content", "message": "Missing required field in requirement", "section": "F", "field": field, "line": start + 1})
                        continue
                    if not str(fb["value"]).strip() and not _has_list_item(list(fb["tail"])):
                        errors.append({"type": "content", "message": "Field must not be empty", "section": "F", "field": field, "line": start + 1})

                phases_field = _field_block(block, "Phases")
                phase_list: List[int] = []
                if phases_field is not None:
                    for l in list(phases_field["tail"]):
                        for n in re.findall(r"`ph-(\d+)`", l):
                            phase_list.append(int(n))
                        if re.match(r"^\s*-\s+`ph-\d+`", l.strip()):
                            errors.append({"type": "content", "message": "Phase lines must include a checkbox", "section": "F", "line": start + 1, "text": l.strip()})
                    if 1 not in phase_list:
                        errors.append({"type": "content", "message": "Requirement phases must include ph-1", "section": "F", "line": start + 1})
                    if phase_nums and any(p not in phase_nums for p in phase_list):
                        bad = sorted([p for p in phase_list if p not in phase_nums])
                        errors.append({"type": "content", "message": "Requirement phases must be a subset of feature phases", "section": "F", "line": start + 1, "phases": bad})

                refs_field = _field_block(block, "References")
                if refs_field is not None:
                    ref_text = "\n".join([str(refs_field["value"])] + list(refs_field["tail"]))
                    for _, target in LINK_RE.findall(ref_text):
                        t = target.strip()
                        if not t.startswith("#"):
                            continue
                        anchor = t[1:]
                        if anchor and anchor not in anchors:
                            errors.append({"type": "link_target", "message": "Reference anchor does not exist", "section": "F", "line": start + 1, "anchor": anchor})

                impl_field = _field_block(block, "Implements")
                if impl_field is not None:
                    impl_text = "\n".join([str(impl_field["value"])] + list(impl_field["tail"]))
                    impl_ids = set(re.findall(r"`([^`]+)`", impl_text))
                    defined = flow_ids | algo_ids | state_ids
                    bad = sorted([x for x in impl_ids if x.startswith("fdd-") and defined and x not in defined])
                    if bad:
                        errors.append({"type": "cross", "message": "Implements references unknown flow/algo/state IDs", "section": "F", "line": start + 1, "ids": bad})

                ts_field = _field_block(block, "Testing Scenarios (FDL)") or _field_block(block, "Testing Scenarios")
                if ts_field is None:
                    errors.append({"type": "content", "message": "Missing Testing Scenarios field", "section": "F", "line": start + 1})
                else:
                    ts_lines = list(ts_field["tail"])
                    if "**GIVEN**" in "\n".join(ts_lines) or "**THEN**" in "\n".join(ts_lines) or re.search(r"^\s*(GIVEN|WHEN|THEN|AND)\b", "\n".join(ts_lines), re.MULTILINE):
                        errors.append({"type": "fdl", "message": "Gherkin keywords are not allowed in Testing Scenarios", "section": "F", "line": start + 1})

                    for lidx, l in enumerate(ts_lines, start=1):
                        if "**ID**:" in l:
                            for m in FEATURE_TEST_ID_RE.finditer(l):
                                if feature_slug is not None and m.group(1) != feature_slug:
                                    errors.append({"type": "id", "message": "Feature slug in test ID does not match directory slug", "section": "F", "line": start + lidx})
                            for tid in _extract_full_ids(l, "test"):
                                test_ids.add(tid)
                        if re.match(r"^\s*(?:\d+\.|-)\s+", l.strip()):
                            if "[" in l and "ph-" in l and not FDL_STEP_LINE_RE.match(l):
                                errors.append({"type": "fdl", "message": "Invalid FDL step line format in Testing Scenarios", "section": "F", "line": start + lidx, "text": l.strip()})

                ac_field = _field_block(block, "Acceptance Criteria")
                if ac_field is None:
                    errors.append({"type": "content", "message": "Missing Acceptance Criteria field", "section": "F", "line": start + 1})
                else:
                    if not _has_list_item(list(ac_field["tail"])):
                        errors.append({"type": "content", "message": "Acceptance Criteria must contain at least 2 list items", "section": "F", "line": start + 1})
                    else:
                        cnt = sum(1 for x in ac_field["tail"] if re.match(r"^\s*[-*]\s+\S+", x))
                        if cnt < 2:
                            errors.append({"type": "content", "message": "Acceptance Criteria must contain at least 2 list items", "section": "F", "line": start + 1})


            # req_ids/test_ids are already sets here; duplicate detection is handled by _common_checks

    passed = (len(errors) == 0) and (len(placeholders) == 0)
    # fdd-begin fdd-fdd-feature-core-methodology-algo-validate-structure:ph-1:inst-return-result
    return {
        "required_section_count": len([s for s in ["A", "B", "C", "D", "E", "F"] if s in sections]),
        "missing_sections": [s for s in ["A", "B", "C", "D", "E", "F"] if s not in sections],
        "placeholder_hits": placeholders,
        "status": "PASS" if not errors else "FAIL",
        "errors": errors,
    }
    # fdd-end   fdd-fdd-feature-core-methodology-algo-validate-structure:ph-1:inst-return-result
# fdd-end   fdd-fdd-feature-core-methodology-algo-validate-structure:ph-1:inst-read-artifact


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
        dt, derr = _load_text(dp)
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
    placeholder_hits: List[Dict[str, object]] = []

    placeholder_hits.extend(_find_html_comment_placeholders(artifact_text))
    placeholder_hits.extend(_find_brace_placeholders(artifact_text))

    for hit in _find_disallowed_link_notation(artifact_text):
        errors.append({"type": "link_format", "message": "Disallowed IDE-specific link notation", **hit})

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

    id_line_start_re = re.compile(r"^\s*(?:[-*]\s*)?(?:\[[ xX]\]\s*)?\*\*ID\*\*:\s*", re.IGNORECASE)
    for i, line in enumerate(lines[:-1]):
        if not re.match(r"^#{2,6}\s+", line.strip()):
            continue

        j = i + 1
        while j < len(lines) and lines[j].strip() == "":
            j += 1

        if j < len(lines) and id_line_start_re.match(lines[j]):
            if j == i + 1:
                errors.append(
                    {
                        "type": "id",
                        "message": "Exactly one blank line is required between heading and **ID** line",
                        "line": i + 1,
                        "text": line.strip(),
                    }
                )
                continue

            if j != i + 2 or lines[i + 1].strip() != "":
                errors.append(
                    {
                        "type": "id",
                        "message": "Exactly one blank line is required between heading and **ID** line",
                        "line": i + 1,
                        "text": line.strip(),
                    }
                )

    hard_limit = _parse_size_hard_limit(requirements_path)
    if hard_limit is not None:
        line_count = len(lines)
        if line_count > hard_limit:
            errors.append({"type": "size", "message": "Artifact exceeds hard line limit", "hard_limit": hard_limit, "line_count": line_count})

    for idx, line in enumerate(lines, start=1):
        if re.match(r"^##\s+Section\s+[A-Z]:", line.strip()):
            errors.append({"type": "section_heading", "message": "Disallowed section heading format (use '## A. Title')", "line": idx, "text": line.strip()})

    return errors, placeholder_hits


def _load_text(path: Path) -> Tuple[Optional[str], Optional[str]]:
    if not path.exists() or not path.is_file():
        return None, f"File not found: {path}"
    return path.read_text(encoding="utf-8"), None


def _latest_archived_changes(feature_dir: Path) -> Optional[Path]:
    ap = feature_dir / "archive"
    if not ap.exists() or not ap.is_dir():
        return None
    candidates = sorted([p for p in ap.iterdir() if p.is_file() and re.match(r"^\d{4}-\d{2}-\d{2}-CHANGES\.md$", p.name)])
    return candidates[-1] if candidates else None


def _iter_code_files(root: Path) -> List[Path]:
    exts = {".rs", ".py", ".ts", ".tsx", ".js", ".go", ".java", ".cs", ".sql"}
    files: List[Path] = []
    for p in root.rglob("*"):
        if not p.is_file():
            continue
        if p.suffix.lower() not in exts:
            continue
        files.append(p)
    return files


def _code_tag_hits(text: str) -> Dict[str, List[Tuple[str, str]]]:
    hits: Dict[str, List[Tuple[str, str]]] = {
        "change": [],
        "flow": [],
        "algo": [],
        "state": [],
        "req": [],
        "test": [],
    }
    for rid, ph in FDD_TAG_CHANGE_RE.findall(text):
        hits["change"].append((rid, ph))
    for rid, ph in FDD_TAG_FLOW_RE.findall(text):
        hits["flow"].append((rid, ph))
    for rid, ph in FDD_TAG_ALGO_RE.findall(text):
        hits["algo"].append((rid, ph))
    for rid, ph in FDD_TAG_STATE_RE.findall(text):
        hits["state"].append((rid, ph))
    for rid, ph in FDD_TAG_REQ_RE.findall(text):
        hits["req"].append((rid, ph))
    for rid, ph in FDD_TAG_TEST_RE.findall(text):
        hits["test"].append((rid, ph))
    return hits


FDD_BEGIN_LINE_RE = re.compile(r"\bfdd-begin\s+([^\s]+)")
FDD_END_LINE_RE = re.compile(r"\bfdd-end\s+([^\s]+)")
UNWRAPPED_INST_TAG_RE = re.compile(r"(fdd-[a-z0-9-]+(?:-[a-z0-9-]+)*:ph-\d+:inst-[a-z0-9-]+)")


def _is_effective_code_line(line: str) -> bool:
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
    if s.startswith("*"):
        return False
    return True


def _empty_fdd_tag_blocks_in_text(text: str) -> List[Dict[str, object]]:
    issues: List[Dict[str, object]] = []
    lines = text.splitlines()

    stack: List[Tuple[str, int]] = []
    for i, line in enumerate(lines):
        mb = FDD_BEGIN_LINE_RE.search(line)
        if mb:
            tag = mb.group(1)
            if ":inst-" in tag:
                stack.append((tag, i))
            continue

        me = FDD_END_LINE_RE.search(line)
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

        has_code = any(_is_effective_code_line(lines[j]) for j in range(start_idx + 1, i))
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


def _paired_inst_tags_in_text(text: str) -> set:
    tags: set = set()
    lines = text.splitlines()

    stack: List[str] = []
    for line in lines:
        mb = FDD_BEGIN_LINE_RE.search(line)
        if mb:
            tag = mb.group(1)
            if ":inst-" in tag:
                stack.append(tag)
            continue

        me = FDD_END_LINE_RE.search(line)
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


def _unwrapped_inst_tag_hits_in_text(text: str) -> List[Dict[str, object]]:
    hits: List[Dict[str, object]] = []
    for i, line in enumerate(text.splitlines()):
        if FDD_BEGIN_LINE_RE.search(line) or FDD_END_LINE_RE.search(line):
            continue
        for m in UNWRAPPED_INST_TAG_RE.finditer(line):
            hits.append({"tag": m.group(1), "line": i + 1})
    return hits


def _extract_scope_ids(line: str, kind: str) -> List[str]:
    pat = SCOPE_ID_BY_KIND_RE.get(kind)
    if pat is None:
        return []
    return pat.findall(line)


def _summarize_validation_report(report: Dict[str, object], *, max_errors: int = 50) -> Dict[str, object]:
    errs = list(report.get("errors", []) or [])
    ph = list(report.get("placeholder_hits", []) or [])
    return {
        "status": report.get("status"),
        "error_count": len(errs),
        "placeholder_count": len(ph),
        "errors": errs[:max_errors],
        "placeholder_hits": ph[:max_errors],
    }


def _validate_feature_artifacts_for_traceability(
    *,
    feature_design_path: Path,
    feature_changes_path: Optional[Path],
    skip_fs_checks: bool,
) -> Tuple[Dict[str, object], Optional[Dict[str, object]]]:
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
        latest = _latest_archived_changes(feature_dir)
        if latest is not None:
            cp = latest

    design_text, derr = _load_text(dp)
    if derr:
        errors.append({"type": "cross", "message": derr})
        design_text = ""
    changes_text: str = ""
    if cp is not None and cp.exists() and cp.is_file():
        changes_text, _ = _load_text(cp)
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
        for fid in _extract_scope_ids(line, "flow"):
            expected_scope_ids["flow"].add(fid)
        for aid in _extract_scope_ids(line, "algo"):
            expected_scope_ids["algo"].add(aid)
        for sid in _extract_scope_ids(line, "state"):
            expected_scope_ids["state"].add(sid)
        for rid in _extract_scope_ids(line, "req"):
            expected_scope_ids["req"].add(rid)
        for tid in _extract_scope_ids(line, "test"):
            expected_scope_ids["test"].add(tid)

    # FDL instruction-level tags from implemented ([x]) step lines.
    current_scope: Optional[str] = None
    for line in (design_text or "").splitlines():
        if "**ID**:" in line and re.match(r"^\s*[-*]\s+\[[ xX]\]\s+\*\*ID\*\*:\s+", line):
            # Prefer algorithm IDs, then flow/state/test
            scope_id = None
            for kind in ("algo", "flow", "state", "test"):
                ids = _extract_scope_ids(line, kind)
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

    # Scan code
    scan_root = scan_root_override or feature_dir
    scanned_files = _iter_code_files(scan_root)
    if not scanned_files and scan_root_override is None:
        # In this repository, code usually lives at module root (sibling of architecture/).
        p = feature_dir
        while p != p.parent:
            if p.name == "architecture":
                scan_root = p.parent
                break
            p = p.parent
        scanned_files = _iter_code_files(scan_root)
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

        hits = _code_tag_hits(txt)

        paired_inst_tags = _paired_inst_tags_in_text(txt)
        unwrapped_inst_hits = _unwrapped_inst_tag_hits_in_text(txt)

        empty_blocks = _empty_fdd_tag_blocks_in_text(txt)
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

    passed = (len(errors) == 0) and all(r.get("status") == "PASS" for r in feature_reports)
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
            for cid in _extract_backticked_ids(line, CAPABILITY_ID_RE):
                current_cap = cid
                capability_to_actors.setdefault(cid, set())
        if current_cap and "**Actors**:" in line:
            for aid in _extract_backticked_ids(line, ACTOR_ID_RE):
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
            bt = _extract_backticked_ids(id_line, ADR_ID_RE)
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


def validate_adr(
    artifact_text: str,
    *,
    artifact_path: Optional[Path] = None,
    business_path: Optional[Path] = None,
    design_path: Optional[Path] = None,
    skip_fs_checks: bool = False,
) -> Dict[str, object]:
    errors: List[Dict[str, object]] = []
    placeholders = find_placeholders(artifact_text)

    adr_entries, issues = _parse_adr_index(artifact_text)
    errors.extend(issues)

    business_actors: set = set()
    business_caps: set = set()
    design_req: set = set()
    design_principle: set = set()

    if not skip_fs_checks and artifact_path is not None:
        bp = business_path or (artifact_path.parent / "BUSINESS.md")
        dp = design_path or (artifact_path.parent / "DESIGN.md")

        bt, berr = _load_text(bp)
        if berr:
            errors.append({"type": "cross", "message": berr})
        else:
            business_actors = set(ACTOR_ID_RE.findall(bt or ""))
            business_caps = set(CAPABILITY_ID_RE.findall(bt or ""))

        dt, derr = _load_text(dp)
        if derr:
            errors.append({"type": "cross", "message": derr})
        else:
            design_req = set(REQ_ID_RE.findall(dt or ""))
            design_principle = set(PRINCIPLE_ID_RE.findall(dt or ""))

    lines = artifact_text.splitlines()
    current_adr: Optional[str] = None
    current_block: List[str] = []
    per_adr_issues: List[Dict[str, object]] = []

    def flush():
        nonlocal current_adr, current_block
        if current_adr is None:
            return
        block_text = "\n".join(current_block)

        if ADR_DATE_RE.search(block_text) is None:
            per_adr_issues.append({"adr": current_adr, "message": "Missing **Date**: YYYY-MM-DD"})
        if ADR_STATUS_RE.search(block_text) is None:
            per_adr_issues.append({"adr": current_adr, "message": "Missing or invalid **Status**"})

        required_sections = [
            "### Context and Problem Statement",
            "### Decision Drivers",
            "### Considered Options",
            "### Decision Outcome",
            "### Related Design Elements",
        ]
        for sec in required_sections:
            if sec not in block_text:
                per_adr_issues.append({"adr": current_adr, "message": f"Missing section: {sec}"})

        if "### Related Design Elements" in block_text:
            related_text = block_text.split("### Related Design Elements", 1)[1]
            referenced = set(ACTOR_ID_RE.findall(related_text)) | set(CAPABILITY_ID_RE.findall(related_text)) | set(REQ_ID_RE.findall(related_text)) | set(PRINCIPLE_ID_RE.findall(related_text))
            if not referenced:
                per_adr_issues.append({"adr": current_adr, "message": "Related Design Elements must contain at least one ID"})
            if business_actors:
                bad = sorted([x for x in ACTOR_ID_RE.findall(related_text) if x not in business_actors])
                if bad:
                    per_adr_issues.append({"adr": current_adr, "message": "Unknown actor IDs in Related Design Elements", "ids": bad})
            if business_caps:
                bad = sorted([x for x in CAPABILITY_ID_RE.findall(related_text) if x not in business_caps])
                if bad:
                    per_adr_issues.append({"adr": current_adr, "message": "Unknown capability IDs in Related Design Elements", "ids": bad})
            if design_req:
                bad = sorted([x for x in REQ_ID_RE.findall(related_text) if x not in design_req])
                if bad:
                    per_adr_issues.append({"adr": current_adr, "message": "Unknown requirement IDs in Related Design Elements", "ids": bad})
            if design_principle:
                bad = sorted([x for x in PRINCIPLE_ID_RE.findall(related_text) if x not in design_principle])
                if bad:
                    per_adr_issues.append({"adr": current_adr, "message": "Unknown principle IDs in Related Design Elements", "ids": bad})

        current_adr = None
        current_block = []

    for line in lines:
        m = ADR_HEADING_RE.match(line.strip())
        if m:
            flush()
            current_adr = m.group(1)
            current_block = []
            continue
        if current_adr is not None:
            current_block.append(line)
    flush()

    passed = (len(errors) == 0) and (len(per_adr_issues) == 0) and (len(placeholders) == 0)
    return {
        "required_section_count": 5,
        "missing_sections": [],
        "placeholder_hits": placeholders,
        "status": "PASS" if passed else "FAIL",
        "errors": errors,
        "adr_issues": per_adr_issues,
        "adr_count": len(adr_entries),
    }


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

        bt, berr = _load_text(bp)
        if berr:
            errors.append({"type": "cross", "message": berr})
        else:
            business_actors, business_caps_to_actors, business_usecases = _parse_business_model(bt or "")

        at, aerr = _load_text(ap)
        if aerr:
            errors.append({"type": "cross", "message": aerr})
        else:
            adr_entries, adr_issues = _parse_adr_index(at or "")
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


def validate_business_context(artifact_text: str) -> Dict[str, object]:
    errors: List[Dict[str, object]] = []
    section_order, sections = _split_by_business_section_letter(artifact_text)

    required = ["A", "B", "C"]
    missing_required = [s for s in required if s not in sections]
    if missing_required:
        errors.append({"type": "structure", "message": "Missing required top-level sections", "missing": missing_required})

    allowed = set(["A", "B", "C", "D", "E"])
    unknown = [s for s in sections.keys() if s not in allowed]
    if unknown:
        errors.append({"type": "structure", "message": "Unknown top-level sections", "sections": sorted(unknown)})

    expected = ["A", "B", "C"]
    if "D" in sections:
        expected.append("D")
    if "E" in sections:
        expected.append("E")
    if section_order and section_order[: len(expected)] != expected:
        errors.append({"type": "structure", "message": "Section order invalid", "required_order": expected, "found_order": section_order})

    placeholders = find_placeholders(artifact_text)

    actor_ids: List[str] = []
    capability_ids: List[str] = []
    usecase_ids: List[str] = []
    issues: List[Dict[str, object]] = []

    if "A" in sections:
        a_lines = sections["A"]
        purpose_block = _field_block(a_lines, "Purpose")
        if purpose_block is None or not str(purpose_block["value"]).strip():
            issues.append({"section": "A", "missing_field": "Purpose"})

        for f in ("Target Users", "Key Problems Solved", "Success Criteria"):
            fb = _field_block(a_lines, f)
            if fb is None:
                issues.append({"section": "A", "missing_field": f})
                continue
            if str(fb["value"]).strip():
                continue
            if not _has_list_item(list(fb["tail"])):
                issues.append({"section": "A", "message": f"Field '{f}' must contain at least one list item"})
        if _paragraph_count(a_lines) < 2:
            issues.append({"section": "A", "message": "Section A must contain at least 2 paragraphs"})

    if "B" in sections:
        b_lines = sections["B"]
        has_human = any("Human Actors" in l for l in b_lines)
        has_system = any("System Actors" in l for l in b_lines)
        if not has_human or not has_system:
            issues.append({"section": "B", "message": "Section B must be grouped by Human Actors and System Actors"})

        idxs = [i for i, l in enumerate(b_lines) if l.strip().startswith("#### ")]
        if not idxs:
            issues.append({"section": "B", "message": "No actors found (expected '#### Actor Name')"})
        for i, start in enumerate(idxs):
            end = idxs[i + 1] if i + 1 < len(idxs) else len(b_lines)
            block = b_lines[start:end]
            title_line = block[0].strip()
            meta = [l for l in block[1:] if l.strip()]
            if not meta:
                issues.append({"section": "B", "message": "Actor block missing metadata", "actor": title_line})
                continue
            id_line = meta[0]
            if "**ID**:" not in id_line:
                issues.append({"section": "B", "message": "Actor ID must be first non-empty line after heading", "actor": title_line})
            ids = _extract_backticked_ids(id_line, ACTOR_ID_RE)
            if not ids:
                issues.append({"section": "B", "message": "Invalid actor ID format", "actor": title_line, "line": id_line})
            else:
                actor_ids.extend(ids)

            role_ok = any("**Role**:" in l for l in meta[1:6])
            if not role_ok:
                issues.append({"section": "B", "message": "Missing **Role** line", "actor": title_line})
            if any("**Capabilities**" in l for l in block):
                issues.append({"section": "B", "message": "Actor block must not list capabilities", "actor": title_line})

        dup = sorted({x for x in actor_ids if actor_ids.count(x) > 1})
        if dup:
            issues.append({"section": "B", "message": "Duplicate actor IDs", "ids": dup})

    if "C" in sections:
        c_lines = sections["C"]
        idxs = [i for i, l in enumerate(c_lines) if l.strip().startswith("#### ")]
        if not idxs:
            issues.append({"section": "C", "message": "No capabilities found (expected '#### Capability Name')"})
        for i, start in enumerate(idxs):
            end = idxs[i + 1] if i + 1 < len(idxs) else len(c_lines)
            block = c_lines[start:end]
            title_line = block[0].strip()
            meta = [l for l in block[1:] if l.strip()]
            if not meta:
                issues.append({"section": "C", "message": "Capability block missing metadata", "capability": title_line})
                continue
            id_line = meta[0]
            if "**ID**:" not in id_line:
                issues.append({"section": "C", "message": "Capability ID must be first non-empty line after heading", "capability": title_line})
            ids = _extract_backticked_ids(id_line, CAPABILITY_ID_RE)
            if not ids:
                issues.append({"section": "C", "message": "Invalid capability ID format", "capability": title_line, "line": id_line})
            else:
                capability_ids.extend(ids)

            has_feature_bullets = any(l.strip().startswith("-") for l in block)
            if not has_feature_bullets:
                issues.append({"section": "C", "message": "Capability must include bulleted list of features", "capability": title_line})

            actors_line = next((l for l in block if "**Actors**:" in l), None)
            if actors_line is None:
                issues.append({"section": "C", "message": "Capability missing **Actors** line", "capability": title_line})
            else:
                a_ids = _extract_backticked_ids(actors_line, ACTOR_ID_RE)
                if not a_ids:
                    issues.append({"section": "C", "message": "Capability **Actors** must list actor IDs", "capability": title_line})
                else:
                    missing = [x for x in a_ids if x not in set(actor_ids)]
                    if missing:
                        issues.append({"section": "C", "message": "Capability references unknown actor IDs", "capability": title_line, "missing": missing})

        dup = sorted({x for x in capability_ids if capability_ids.count(x) > 1})
        if dup:
            issues.append({"section": "C", "message": "Duplicate capability IDs", "ids": dup})

    if "D" in sections:
        d_lines = sections["D"]
        idxs = [i for i, l in enumerate(d_lines) if l.strip().startswith("#### ")]
        if not idxs:
            issues.append({"section": "D", "message": "Section D present but no use cases found"})
        for i, start in enumerate(idxs):
            end = idxs[i + 1] if i + 1 < len(idxs) else len(d_lines)
            block = d_lines[start:end]
            title_line = block[0].strip()
            meta = [l for l in block[1:] if l.strip()]
            if not meta:
                issues.append({"section": "D", "message": "Use case block missing metadata", "usecase": title_line})
                continue
            id_line = next((l for l in meta[:6] if "**ID**:" in l), None)
            if id_line is None:
                issues.append({"section": "D", "message": "Missing **ID** line", "usecase": title_line})
                continue
            ids = _extract_backticked_ids(id_line, USECASE_ID_RE)
            if not ids:
                issues.append({"section": "D", "message": "Invalid use case ID format", "usecase": title_line, "line": id_line})
            else:
                usecase_ids.extend(ids)

            actor_line = next((l for l in block if "**Actor**:" in l), None)
            if actor_line is None:
                issues.append({"section": "D", "message": "Missing **Actor** line", "usecase": title_line})
            else:
                a_ids = _extract_backticked_ids(actor_line, ACTOR_ID_RE)
                if not a_ids:
                    issues.append({"section": "D", "message": "Use case **Actor** must list actor IDs", "usecase": title_line})
                else:
                    missing = [x for x in a_ids if x not in set(actor_ids)]
                    if missing:
                        issues.append({"section": "D", "message": "Use case references unknown actor IDs", "usecase": title_line, "missing": missing})

            if not any("**Preconditions**" in l for l in block):
                issues.append({"section": "D", "message": "Missing **Preconditions**", "usecase": title_line})
            if not any(l.strip().startswith("1.") for l in block):
                issues.append({"section": "D", "message": "Missing numbered flow steps", "usecase": title_line})
            if not any("**Postconditions**" in l for l in block):
                issues.append({"section": "D", "message": "Missing **Postconditions**", "usecase": title_line})

        dup = sorted({x for x in usecase_ids if usecase_ids.count(x) > 1})
        if dup:
            issues.append({"section": "D", "message": "Duplicate use case IDs", "ids": dup})

        cap_set = set(capability_ids)
        uc_set = set(usecase_ids)
        for l in d_lines:
            for cid in CAPABILITY_ID_RE.findall(l):
                if cid not in cap_set:
                    issues.append({"section": "D", "message": "Use case references unknown capability ID", "id": cid})
            for uid in USECASE_ID_RE.findall(l):
                if uid not in uc_set:
                    issues.append({"section": "D", "message": "Use case references unknown use case ID", "id": uid})

    passed = (len(errors) == 0) and (len(issues) == 0) and (len(placeholders) == 0)
    return {
        "required_section_count": len(required),
        "missing_sections": [{"id": s, "title": ""} for s in missing_required],
        "placeholder_hits": placeholders,
        "status": "PASS" if passed else "FAIL",
        "errors": errors,
        "issues": issues,
    }
FEATURE_HEADING_RE = re.compile(
    r"^###\s+(\d+)\.\s+\[(.+?)\]\((feature-[^)]+/)\)\s+([⏳🔄✅])\s+(CRITICAL|HIGH|MEDIUM|LOW)\s*$"
)


def _line_has_field(line: str, field_name: str, *, allow_empty_value: bool) -> bool:
    # Accept list form and plain form:
    # - **Field**: ...
    # **Field**: ...
    # Some fields allow list-style values:
    # **Phases**:
    #   - `ph-1`: ...
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

        phases_block = _field_block(block_lines, "Phases")
        phases_ok = phases_block is not None and "`ph-1`" in "\n".join([block_lines[phases_block["index"]]] + list(phases_block["tail"]))

        empty_list_fields: List[str] = []
        for field_name in ("Depends On", "Blocks", "Scope", "Requirements Covered", "Phases"):
            fb = _field_block(block_lines, field_name)
            if fb is None:
                continue
            inline_value = str(fb["value"]).strip()
            if inline_value:
                continue
            if field_name in ("Depends On", "Blocks"):
                if inline_value == "None":
                    continue
            if _has_list_item(list(fb["tail"])):
                continue
            empty_list_fields.append(field_name)

        status_mismatch: Optional[str] = None
        status_field = _field_block(block_lines, "Status")
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
            fb = _field_block(block_lines, dep_field)
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
            req_field = _field_block(block_lines, "Requirements Covered")
            if req_field is not None:
                for rid in _extract_id_list(req_field):
                    if rid not in design_ids["req"]:
                        cross_issues.append(f"Requirements Covered references missing id in DESIGN.md: {rid}")
        if design_ids["principle"]:
            p_field = _field_block(block_lines, "Principles Covered")
            if p_field is not None:
                for pid in _extract_id_list(p_field):
                    if pid not in design_ids["principle"]:
                        cross_issues.append(f"Principles Covered references missing id in DESIGN.md: {pid}")
        if design_ids["constraint"]:
            c_field = _field_block(block_lines, "Constraints Affected")
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

    # Keep stable top-level keys used by other validations.
    return {
        "required_section_count": len(required_fields) + 3,
        "missing_sections": [],
        "placeholder_hits": placeholders,
        "status": "PASS" if passed else "FAIL",
        "errors": errors,
        "feature_issues": feature_issues,
        "feature_count": len(feature_headers),
    }


def validate_generic_sections(artifact_text: str, requirements_path: Path) -> Dict[str, object]:
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
    missing = [
        {
            "id": section_id,
            "title": required_sections[section_id],
        }
        for section_id in required_sections.keys()
        if section_id not in present_ids
    ]

    errors: List[Dict[str, object]] = []

    counts: Dict[str, int] = {}
    for sid in present_ids_list:
        counts[sid] = counts.get(sid, 0) + 1
    dup_sids = sorted([sid for sid, c in counts.items() if c > 1])
    if dup_sids:
        errors.append({"type": "structure", "message": "Duplicate section ids in artifact", "ids": dup_sids})

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


def validate(
    artifact_path: Path,
    requirements_path: Path,
    artifact_kind: str,
    *,
    design_path: Optional[Path] = None,
    business_path: Optional[Path] = None,
    adr_path: Optional[Path] = None,
    skip_fs_checks: bool = False,
) -> Dict[str, object]:
    artifact_text = artifact_path.read_text(encoding="utf-8")

    if not artifact_text.strip():
        return {
            "required_section_count": 0,
            "missing_sections": [],
            "placeholder_hits": [],
            "status": "FAIL",
            "errors": [{"type": "file", "message": "Empty file"}],
        }

    if artifact_kind == "features-manifest":
        report = validate_features_manifest(
            artifact_text,
            artifact_path=artifact_path,
            design_path=design_path,
            skip_fs_checks=skip_fs_checks,
        )

    elif artifact_kind == "business-context":
        report = validate_business_context(artifact_text)

    elif artifact_kind == "adr":
        report = validate_adr(
            artifact_text,
            artifact_path=artifact_path,
            business_path=business_path,
            design_path=design_path,
            skip_fs_checks=skip_fs_checks,
        )

    elif artifact_kind == "feature-design":
        report = validate_feature_design(
            artifact_text,
            artifact_path=artifact_path,
            skip_fs_checks=skip_fs_checks,
        )

    elif artifact_kind == "feature-changes":
        report = validate_feature_changes(
            artifact_text,
            artifact_path=artifact_path,
            skip_fs_checks=skip_fs_checks,
        )

    elif artifact_kind == "overall-design":
        report = validate_overall_design(
            artifact_text,
            artifact_path=artifact_path,
            business_path=business_path,
            adr_path=adr_path,
            skip_fs_checks=skip_fs_checks,
        )

    else:
        report = validate_generic_sections(artifact_text, requirements_path)

    common_errors, common_placeholders = _common_checks(
        artifact_text=artifact_text,
        artifact_path=artifact_path,
        requirements_path=requirements_path,
        skip_fs_checks=skip_fs_checks,
    )
    if "errors" not in report:
        report["errors"] = []
    report["errors"].extend(common_errors)
    if "placeholder_hits" not in report:
        report["placeholder_hits"] = []
    report["placeholder_hits"].extend(common_placeholders)
    if report.get("placeholder_hits"):
        report["status"] = "FAIL"
    if report.get("errors") and report.get("status") == "PASS":
        report["status"] = "FAIL"
    return report


# =============================================================================
# VALIDATION COMMAND
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
        m = SECTION_FEATURE_RE.match(line.strip())
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
        m = CHANGE_HEADING_RE.match(line.strip())
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
    text, err = _load_text(artifact_path)
    if err:
        print(json.dumps({"status": "ERROR", "message": err}, indent=None, ensure_ascii=False))
        return 1
    lines = text.splitlines()
    kind = _detect_kind(artifact_path)

    entries: List[Dict[str, object]] = []
    
    if kind == "features-manifest":
        for i, line in enumerate(lines, start=1):
            m = FEATURE_HEADING_RE.match(line.strip())
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
    text, err = _load_text(artifact_path)
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
    text, err = _load_text(artifact_path)
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
            m = FEATURE_HEADING_RE.match(line.strip())
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
            title_m = CHANGE_HEADING_RE.match(active_lines[start].strip()) if start < len(active_lines) else None
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
            m = SECTION_BUSINESS_RE.match(line.strip())
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
    text, err = _load_text(artifact_path)
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
            m = FEATURE_HEADING_RE.match(line)
            if m and m.group(2) == args.feature_id:
                start = i
                end = i + 1
                while end < len(lines) and not FEATURE_HEADING_RE.match(lines[end]):
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
    text, err = _load_text(artifact_path)
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
    text, err = _load_text(artifact_path)
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
        section_idx = _lettered_section_indices(lines, SECTION_BUSINESS_RE)
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
