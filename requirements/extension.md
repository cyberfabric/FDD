# FDD Extension Mechanism

**Version**: 1.0  
**Purpose**: Define how files extend other files using **Extends** directive  
**Scope**: All FDD files that can extend base files

---

## Overview

**Extension mechanism** - Allows files to inherit content from base files and add modifications

**Format**: `**Extends**: {path-to-base-file}`

**Applies to**: AGENTS.md, specification files, requirements files

---

## How Extends Works

### Basic Rule

**When file has `**Extends**: {base-file}`**:

1. Load base file first
2. Load current file
3. Merge = base content + current modifications
4. Never skip base
5. Never replace base rules entirely

### Loading Order

```
Base File (loaded first)
    ↓
Current File (loaded second)
    ↓
Merged Result (base + modifications)
```

### Merge Behavior

**Base content** is ALWAYS included

**Current file** can:
- ✅ Add new sections
- ✅ Add new rules
- ✅ Add new instructions
- ✅ Override specific values (if explicitly stated)
- ❌ Remove base rules
- ❌ Contradict base principles

---

## Examples

### Valid Extension

**Base**: `FDD/AGENTS.md`
```markdown
# FDD AI Agent Navigation

ALWAYS open and follow `requirements/core.md` WHEN modifying FDD files
```

**Extension**: `{adapter-directory}/FDD-Adapter/AGENTS.md`
```markdown
# Project AI Agent Navigation

**Extends**: `../FDD/AGENTS.md`

ALWAYS open and follow `{adapter-directory}/domain-model.gts` WHEN executing workflows: design.md, design-validate.md, adr.md, adr-validate.md

ALWAYS open and follow `{adapter-directory}/api-contracts.yaml` WHEN executing workflows: design.md, design-validate.md, adr.md, adr-validate.md
```

**Result**: Agent reads FDD/AGENTS.md first, then adds project-specific instructions

### Invalid Extension

```markdown
# Project AI Agent Navigation

**Extends**: `../FDD/AGENTS.md`

# This contradicts base - INVALID
DO NOT read requirements files
```

---

## Extension Rules

**MUST**:
- Specify exact path to base file
- Load base file before processing current file
- Preserve all base rules and instructions
- Add modifications that complement base

**MUST NOT**:
- Skip loading base file
- Remove base rules
- Contradict base principles
- Create circular dependencies (A extends B, B extends A)

---

## Use Cases

### AGENTS.md Extension

**Base**: Core FDD navigation  
**Extension**: Project-specific navigation (domain model, API contracts, tech stack)

### Requirements Extension

**Base**: General structure requirements  
**Extension**: Project-specific validation rules

### Specification Extension

**Base**: Core syntax/grammar  
**Extension**: Project-specific extensions to syntax

---

## Validation Criteria

### Structure (20 points)

**Check**:
- [ ] **Extends** directive present in header
- [ ] Base file path specified correctly
- [ ] Path format is correct (relative or absolute)
- [ ] Extension file has proper header

### Base File Accessibility (30 points)

**Check**:
- [ ] Base file exists at specified path
- [ ] Base file is readable
- [ ] Base file path is correct relative to extension file location
- [ ] No broken references

### Merge Correctness (30 points)

**Check**:
- [ ] Extension adds new content (not just duplicates)
- [ ] Extension doesn't contradict base rules
- [ ] Extension doesn't remove base content
- [ ] Extension complements base appropriately

### Dependency Validation (20 points)

**Check**:
- [ ] No circular dependencies (A→B→A)
- [ ] Base file is loaded before extension
- [ ] Extension chain is finite
- [ ] All base files in chain are accessible

**Total**: 100/100

**Pass threshold**: ≥95/100

---

## References

**This file is referenced by**:
- All files using **Extends** directive

**References**:
- `core-agents.md` - Defines structure for AGENTS.md files
- `adapter-structure.md` - Requires adapter AGENTS.md to extend FDD AGENTS.md
