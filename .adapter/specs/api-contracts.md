# API Contracts

**Version**: 1.0  
**Last Updated**: 2025-01-17  
**Purpose**: Define API contract format and location for FDD skill

---

## Overview

FDD skill uses **CLISPEC** format for CLI command documentation and validation.

**Philosophy**: 
- Human and machine-readable format
- Structured for AI agent consumption
- Complete command specification with examples
- Integration with FDD workflows

---

## Technology

**Format**: CLISPEC  
**Specification**: `../../CLISPEC.md`  
**Version**: 1.0

---

## Contract Location

**Primary contract**: `skills/fdd/fdd.clispec`

**Structure**:
```
skills/fdd/
├── fdd.clispec          # CLI command specification
├── SKILL.md             # Skill documentation
└── scripts/
    └── fdd.py           # Implementation
```

---

## Command Specification Format

### CLISPEC Structure

Each command follows this format:

```
COMMAND <command-name>
SYNOPSIS: python3 scripts/fdd.py <command> [options]
DESCRIPTION: <brief description>
WORKFLOW: <workflow-reference> (optional)

ARGUMENTS:
  <arg-name>  <type>  [required|optional]  <description>

OPTIONS:
  --long-name  <type>  [default: value]  <description>

EXIT CODES:
  <code>  <description>

EXAMPLE:
  $ <example-usage>

RELATED:
  - @CLI.other-command
  - @Workflow.workflow-name
---
```

---

## Available Commands

**Validation**:
- `validate` - Validate FDD artifacts or perform traceability scan

**Search**:
- `list-sections` - List sections and headings
- `list-ids` - List FDD IDs with filtering
- `list-items` - List structured items by type
- `read-section` - Read specific section content
- `get-item` - Get complete item details
- `find-id` - Find ID with context
- `search` - Full-text search

**Discovery**:
- `adapter-info` - Discover FDD adapter configuration

**Traceability**:
- `scan-ids` - Scan repository for all IDs
- `where-defined` - Find normative definition location
- `where-used` - Find all usage locations

---

## Type System

**Supported types** (from CLISPEC):
- `<string>` - Any text value
- `<number>` - Numeric value
- `<boolean>` - True/false flag
- `<path>` - File system path

---

## Exit Code Semantics

**Standard exit codes**:
- `0` - Success
- `1` - File system error or resource not found
- `2` - Validation failure or not found
- `3` - Ambiguous result (multiple definitions)

---

## Integration with Workflows

**Validation workflows**:
- `design-validate.md` - Uses `validate --artifact DESIGN.md`
- `feature-validate.md` - Uses `validate --artifact feature-*/DESIGN.md`
- `feature-code-validate.md` - Uses `validate --artifact .`

**Traceability workflows**:
- All implementation workflows use `where-defined` and `where-used`

---

## Examples

### ✅ Valid Command Invocation

```bash
# Validate artifact with auto-detection
python3 scripts/fdd.py validate --artifact architecture/DESIGN.md

# Discover adapter
python3 scripts/fdd.py adapter-info --root .

# Find ID definition
python3 scripts/fdd.py where-defined --root . --id fdd-myapp-actor-admin

# Scan codebase for FDD IDs
python3 scripts/fdd.py scan-ids --root . --kind fdd
```

### ❌ Invalid Command Invocation

```bash
# Missing required argument
python3 scripts/fdd.py validate

# Wrong option name
python3 scripts/fdd.py list-ids --file architecture/DESIGN.md

# Wrong type (string instead of number)
python3 scripts/fdd.py list-items --artifact DESIGN.md --change "one"
```

---

## Source References

**Derived from**:
- `skills/fdd/SKILL.md` - Skill documentation
- `skills/fdd/scripts/fdd.py` - Implementation analysis
- `CLISPEC.md` - Format specification
- Code analysis and testing

**Command discovery method**: 
- Parsed argparse subcommands from fdd.py
- Extracted argument definitions and help text
- Validated against actual implementation

---

## Validation Checklist

Agent MUST verify before using fdd skill:
- [ ] All commands follow CLISPEC format in `fdd.clispec`
- [ ] Required arguments are provided
- [ ] Optional arguments use documented option names
- [ ] Paths are absolute or relative to correct base
- [ ] Exit codes are handled appropriately
- [ ] Commands are invoked with `python3 scripts/fdd.py`

**Self-test**:
- [ ] Did I check the CLISPEC file for command signature?
- [ ] Are all required arguments present?
- [ ] Do option names match exactly (including --)?
- [ ] Is the command path correct (scripts/fdd.py)?

---

## References

**Used by workflows**:
- `design-validate.md` - Validation command
- `feature-validate.md` - Validation command  
- `feature-code-validate.md` - Traceability validation
- All implementation workflows - Traceability commands

**Related files**:
- `../../CLISPEC.md` - CLISPEC format specification
- `../../skills/fdd/fdd.clispec` - Complete command specification
- `../../skills/fdd/SKILL.md` - Skill documentation
