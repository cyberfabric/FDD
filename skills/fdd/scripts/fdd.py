#!/usr/bin/env python3
"""
FDD Validator - Main Entry Point

This is a thin wrapper that imports from the modular fdd package.
For backward compatibility, all functions are re-exported at module level.

Legacy monolithic implementation preserved in legacy.py.
"""

# Re-export everything from the fdd package for backward compatibility
from fdd import *
from fdd import __all__

# CLI entry point
if __name__ == "__main__":
    from fdd import main
    raise SystemExit(main())
