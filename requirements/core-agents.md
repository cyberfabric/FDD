# FDD Core: AGENTS.md File Structure

**Version**: 1.0  
**Purpose**: Define structural requirements for FDD AGENTS.md specification files  
**Scope**: `FDD/AGENTS.md` and `{adapter-directory}/FDD-Adapter/AGENTS.md`

---

## Overview

**AGENTS.md files** - AI agent navigation instructions

**Core principle**: AGENTS.md contains ONLY action-gated navigation instructions

**Purpose**: Direct agents to correct specification files based on context

**This file defines**: Structure requirements for AGENTS.md navigation files

**Applies to**: Any AGENTS.md file (core, adapter, module-specific)

---

## Key Principle

**AGENTS.md MUST contain ONLY**:
- Navigation instructions in one of these formats:
  - `ALWAYS open and follow {file} WHEN {trigger}` (preferred)
  - `ALWAYS execute {workflow} WHEN {trigger}` (preferred)
  - `ALWAYS do {action} WHEN {trigger}` (preferred)
- NO content duplication from referenced files
- NO context or explanations beyond navigation
- NO detailed requirements or specifications

**Exception (core FDD only)**:
- `FDD/AGENTS.md` MAY include mandatory instruction semantics and enforcement sections (e.g. instruction meaning, acknowledgments, violation handling)
- These sections MUST NOT duplicate requirements content from referenced files

**Adapter AGENTS.md WHEN rule (mandatory)**:
- For `{adapter-directory}/FDD-Adapter/AGENTS.md`, each navigation rule MUST use a WHEN clause that is ONLY a list of FDD workflows.
- Canonical form:
  - `ALWAYS open and follow {spec-file} WHEN executing workflows: {workflow1.md}, {workflow2.md}, ...`
- The workflow names MUST match files under `guidelines/FDD/workflows/`.
- The WHEN clause MUST NOT use generic conditions like "working with domain types".

**Rationale**: Single source of truth - content lives in spec files, AGENTS.md only directs to them

---

## File Structure

### Required Header

**All AGENTS.md files MUST have**:

```markdown
# {Title}

**Version**: {version}
**Purpose**: {brief description}
```

**If file extends another**:
```markdown
# {Title}

**Extends**: `{path-to-base-file}`
**Version**: {version}
```

### Section Organization

**MUST**:
- Use markdown headings (`##`, `###`)
- Separate sections with `---`
- Use consistent heading hierarchy
- Include References section at end

**SHOULD**:
- Use emoji markers for critical sections (`⚠️`, `📐`, `👥`, `🤖`)
- Group related content under common headings
- Provide examples where applicable

---

## Style Requirements

**Section Markers**: Use `## ⚠️` warnings | `## 📐` core | `## 👥` roles | `## 🤖` agent instructions

**Language**: MUST/SHOULD/MAY correct | Command form | Explicit | Examples provided

**Lists**: Consistent format | Clear hierarchies | Validation criteria | Related files

---

## Token Limits

**FDD AGENTS.md**: Soft ≤6,000 | Hard ≤8,000 tokens

**Adapter AGENTS.md**: Soft ≤2,500 | Hard ≤3,500 tokens

**If exceeded**: Extract details to separate files | Reference instead of duplicate | Use tables

---

## Validation Criteria

| Criterion | Requirements | Points |
|-----------|--------------|--------|
| **Structure** | Header complete, Sections organized, Markdown valid, References present | 25 |
| **Completeness** | All sections filled, No placeholders, Examples provided | 30 |
| **Clarity** | Imperative language, MUST/SHOULD/MAY correct, No ambiguity | 25 |
| **Integration** | References correct, Extends works (if applicable), Consistent with core.md | 20 |

**Pass threshold**: ≥95/100

---

## Extension Mechanism

### How Extends Works

When adapter AGENTS.md has `**Extends**: ../FDD/AGENTS.md`:

1. Agent ALWAYS open and follow base file first (`FDD/AGENTS.md`)
2. Agent applies modifications from adapter file
3. Merge = base instructions + adapter specifics
4. Never skip base rules
5. Adapter overrides only what is explicitly allowed

### Allowed Overrides

Adapter CAN override:
- ✅ Behavior description language (replace FDL)
- ✅ Validation score thresholds
- ✅ Project-specific conventions
- ✅ File paths and locations

Adapter CANNOT override:
- ❌ Core principles (brevity, imperative, OS agnostic)
- ❌ Design hierarchy
- ❌ Mandatory validation requirements
- ❌ File structure requirements

---

## Examples

**Valid AGENTS.md header**:
```markdown
# {Descriptive Title}

**Version**: 1.0
**Purpose**: {What this file defines}

---

## {Section Title}

{Content with imperative language}
```

**Valid AGENTS.md with Extends**:
```markdown
# {Descriptive Title}

**Extends**: `../path/to/base.md`
**Version**: 1.0
**Purpose**: {Additional specifications}

---

## {Additional Section}

{Extension content}
```

**Invalid AGENTS.md**:
```markdown
# Instructions

You might want to do something.

Maybe check the files.
```

---

## References

**This file is referenced by**:
- ALWAYS open and follow `core.md` WHEN creating or modifying AGENTS.md files
- All workflows reference adapter AGENTS.md for project specifics
- `adapter-structure.md` - More detailed adapter requirements

**References**:
- `core.md` - Core FDD principles
- `adapter-structure.md` - Full adapter specification
- All requirements files - Referenced from AGENTS.md
