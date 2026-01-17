"""
FDD Validator - File System Operations

File I/O, project root discovery, adapter detection, path resolution.
"""

import json
import re
from pathlib import Path
from typing import Dict, Optional, Tuple

from ..constants import PROJECT_CONFIG_FILENAME


def cfg_get_str(cfg: object, *keys: str) -> Optional[str]:
    """Extract first non-empty string value from config dict for given keys."""
    if not isinstance(cfg, dict):
        return None
    for k in keys:
        v = cfg.get(k)
        if isinstance(v, str) and v.strip():
            return v.strip()
    return None


def find_project_root(start: Path) -> Optional[Path]:
    """
    Find project root by looking for .fdd-config.json or .git directory.
    Searches up to 25 levels in directory hierarchy.
    """
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


def load_project_config(project_root: Path) -> Optional[dict]:
    """Load and parse .fdd-config.json from project root."""
    path = (project_root / PROJECT_CONFIG_FILENAME)
    if not path.is_file():
        return None
    try:
        raw = path.read_text(encoding="utf-8")
        cfg = json.loads(raw)
    except Exception:
        return None
    return cfg if isinstance(cfg, dict) else None


def fdd_root_from_project_config() -> Optional[Path]:
    """Get FDD core path from project configuration."""
    project_root = find_project_root(Path.cwd())
    if project_root is None:
        return None

    cfg = load_project_config(project_root)
    if cfg is None:
        return None

    # Canonical keys (camelCase), plus a couple of permissive variants.
    core_rel = cfg_get_str(cfg, "fddCorePath", "fdd_core_path", "fddCoreDir")
    if core_rel is None:
        return None

    core = (project_root / core_rel).resolve()
    if (core / "AGENTS.md").exists() and (core / "requirements").is_dir() and (core / "workflows").is_dir():
        return core
    return None


def find_adapter_directory(start: Path, fdd_root: Optional[Path] = None) -> Optional[Path]:
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
    project_root = find_project_root(start)
    if project_root is None:
        return None
    
    # PRIORITY 1: Check config first - explicit path always wins
    cfg = load_project_config(project_root)
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


def load_adapter_config(adapter_dir: Path) -> Dict[str, object]:
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


def fdd_root_from_this_file() -> Path:
    """
    Find FDD root by walking up directory tree looking for FDD markers.
    FDD can be located anywhere (as submodule, copied, etc.)
    """
    configured = fdd_root_from_project_config()
    if configured is not None:
        return configured

    current = Path(__file__).resolve().parent.parent.parent.parent
    
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
    return Path(__file__).resolve().parents[6]


def detect_requirements(artifact_path: Path) -> Tuple[str, Path]:
    """
    Detect artifact type and corresponding requirements file.
    
    Returns tuple of (artifact_kind, requirements_path).
    """
    name = artifact_path.name

    if re.match(r"^\d{4}-\d{2}-\d{2}-CHANGES\.md$", name):
        return "feature-changes", fdd_root_from_this_file() / "requirements" / "feature-changes-structure.md"
    fdd_root = fdd_root_from_this_file()

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


def load_text(path: Path) -> Tuple[str, Optional[str]]:
    """
    Load text from file, returning (content, error_message).
    Returns ("", error_message) on failure.
    """
    if not path.exists():
        return "", f"File not found: {path}"
    if not path.is_file():
        return "", f"Not a file: {path}"
    try:
        return path.read_text(encoding="utf-8"), None
    except Exception as e:
        return "", f"Failed to read {path}: {e}"
