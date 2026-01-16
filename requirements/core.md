# FDD Core Requirements

**Version**: 1.0  
**Purpose**: Define requirements for FDD framework itself  
**Scope**: Applies to all FDD core files, workflows, and specifications

---

## Overview

**FDD Core** - The methodology framework and specification files

**This file defines**: Requirements for creating and modifying FDD framework itself

**Applies to**: All files in `FDD/` directory (excluding user-facing documentation)

**Exemptions**: README.md, user guides, tutorials, examples for human readers

---

## Core Principles

### 1. English Language Only

**MUST**:
- Write all content in English
- Use English for file names, comments, documentation
- Use English for code identifiers (variables, functions, types)
- Use English for commit messages and PR descriptions

**MUST NOT**:
- Use any non-English language in FDD files
- Mix languages within documents
- Use transliterated non-English words

**Example**:
- ✅ "Create file at path"
- ❌ "Создать файл по пути" (Russian)
- ❌ "Sozdat' file" (transliterated Russian)

**Rationale**: English ensures universal AI agent compatibility and international collaboration.

---

## Token Limits

**Purpose**: Minimize context usage, maximize agent efficiency

**Recommended limits** (soft limit / hard limit):

| File Type | Soft | Hard | Purpose |
|-----------|------|------|---------|
| Specification files (AGENTS.md, FDL.md) | 6,000 | 8,000 | Core methodology |
| Requirements files (*-structure.md) | 3,000 | 4,000 | Structure definitions |
| Workflow files | 1,000 | 1,500 | Single operations |
| Core.md | 3,500 | 4,500 | FDD framework requirements |
| Adapter AGENTS.md | 2,500 | 3,500 | Project configuration |

**Validation**:
- Count tokens using standard tokenizer (GPT-4 equivalent)
- Fail if exceeds hard limit
- Warn if exceeds soft limit

**If limit exceeded**:
1. Remove redundant examples
2. Extract details to separate files
3. Reference instead of duplicate
4. Use tables instead of prose

---

### 2. Brevity

**MUST**: Use concise language | Eliminate redundancy | Prefer bullets | Minimize explanations

**MUST NOT**: Write verbosely | Repeat information | Use filler words

**Example**: ✅ "Create file at path" | ❌ "You should proceed to create a file at the specified path"

### 3. Imperative Style

**MUST**: Use command form | Start with action verbs | Use MUST/SHOULD/MAY correctly

**MUST NOT**: Use suggestive language | Use passive voice | Use conditionals unnecessarily

**Example**: ✅ "Validate file before proceeding" | ❌ "The file should be validated before you proceed"

### 4. Agent-Centric Design

**MUST**: Structure for AI parsing | Use consistent formatting | Provide clear steps | Include validation criteria | Make prerequisites explicit

**MUST NOT**: Assume human interpretation | Leave steps implicit | Use ambiguous references

**Example**: ✅ "Read `BUSINESS.md` → Extract actors → Validate list" | ❌ "Look at the business context and understand the actors"

### 5. OS Agnostic

**MUST**: Use cross-platform commands | Use forward slashes `/` | Specify relative paths

**MUST NOT**: Use OS-specific commands (`ls`, `cat`, `grep`, `dir`) | Use backslashes `\`

**Example**: ✅ "Check file exists at `architecture/DESIGN.md`" | ❌ "Run `ls -la /home/user/...`"

---

## File Structure Requirements

### All FDD Files MUST Have

1. **Header**: Title, Version, Purpose, Scope
2. **Overview**: What/Who/When
3. **Content**: Clear headings, numbered steps, bullets, code blocks
4. **References**: Related files, dependencies

### Workflow Files

**Location**: `FDD/workflows/*.md`

ALWAYS open and follow `core-workflows.md` WHEN creating or modifying workflow files

### Requirements Files

**Location**: `FDD/requirements/*.md`

ALWAYS open and follow `core-requirements.md` WHEN creating or modifying requirements files

### Specification Files

**Location**: `FDD/*.md`

**Type**: AGENTS.md, FDL.md, etc.

ALWAYS open and follow `core-agents.md` WHEN creating or modifying AGENTS.md files

---

## Content Requirements

### Language Style

**MUST**: Imperative | Active voice | Specific terms

**MUST NOT**: Passive | Vague | Suggestive

### Formatting

**MUST**: Markdown | Tagged code blocks | Inline code for agent instructions | Standard Markdown links for artifact references

**MUST NOT**: HTML | Unicode bullets | Excessive formatting

### Links

**MUST**:
- For FDD artifacts and adapter spec docs, follow `requirements.md`
- For agent instruction files (AGENTS.md, workflow files), use inline code paths for navigation (e.g., `requirements/core.md`) to optimize agent parsing and token usage

**MUST NOT**:
- In FDD artifacts and adapter spec docs, violate link requirements from `requirements.md`
- In FDD artifacts, use inline code as a substitute for a link when the intent is navigation

### Markdown Rendering: Line Breaks

**MUST** ensure that metadata-like lines render as separate lines in markdown output.

**MUST** use one of these patterns:
- Use a markdown list for metadata fields (preferred)
- Or end each metadata line with two spaces (`  `) to force a hard line break

**MUST NOT** rely on markdown soft-wrap for rendering separate lines.

**Examples**:
```markdown
✅ - **Status**: NOT_STARTED
✅ - **Depends On**: None

✅ **Status**: NOT_STARTED  
✅ **Depends On**: None  

❌ **Status**: NOT_STARTED
❌ **Depends On**: None
```

### Examples

**MUST**: Valid + Invalid examples with ✅/❌ | Explanation

### Placeholders

**MUST**: `{descriptive-name}` format

**MUST NOT**: `[TODO]`, `[TBD]` | Empty sections

### Validation Criteria & Checklists

**MUST**: All requirements files and adapter specs MUST include validation criteria and checklists

**Requirements for validation sections**:
- **Validation Criteria**: Structured breakdown with point values (100-point scale)
- **Checklist format**: Use `- [ ]` checkboxes for agent self-verification
- **Self-test sections**: Questions agent must answer before completing work
- **Pass thresholds**: Clear minimum scores (e.g., ≥90/100)

**Purpose**: Enable agent self-checking and systematic verification

**Example structure**:
```markdown
## Validation Criteria

### Category 1 (30 points)
- [ ] Criterion 1 (10 points)
- [ ] Criterion 2 (10 points)
- [ ] Criterion 3 (10 points)

### Category 2 (40 points)
- [ ] Criterion 4 (20 points)
- [ ] Criterion 5 (20 points)

**Pass threshold**: ≥90/100

## Self-Test Checklist

Before completing, verify:
- [ ] Did I check every criterion individually?
- [ ] Did I verify all required elements?
- [ ] Is my scoring accurate?
```

**Applies to**:
- All `requirements/*-structure.md` files
- All adapter `specs/*.md` files
- All validation workflow files

---

### References

**Format**: All references MUST use an action-gated conditional format with a WHEN clause

**MUST**:
- Use one of these formats:
  - `ALWAYS open and follow {file} WHEN {trigger}` (preferred)
  - `ALWAYS execute {workflow} WHEN {trigger}` (preferred)
  - `ALWAYS do {action} WHEN {trigger}` (preferred)
- For `ALWAYS do {action}`: the action MUST reference a concrete FDD artifact (a file path or a workflow)
- Specify a clear trigger/condition for when the action applies
- Use exact file paths (or exact workflow file names under `workflows/`)
- Make the trigger/condition verifiable

**MUST NOT**:
- Duplicate content from referenced file
- Copy requirements from referenced file
- Repeat validation criteria from referenced file
- Include full examples from referenced file

**Rationale**: References prevent duplication and ensure single source of truth

**Example**:
```markdown
✅ ALWAYS open and follow `core-workflows.md` WHEN creating or modifying workflow files
✅ ALWAYS open and follow `requirements/business-context-structure.md` WHEN validating BUSINESS.md

❌ Read core-workflows.md for workflow structure (no WHEN condition)
❌ Workflows must have YAML frontmatter (duplicates core-workflows.md content)
```

---

## Validation Criteria

### Structure Validation

1. **Header**: Title, Version, Purpose, Scope
2. **Sections**: Overview, Content, Examples, References
3. **Format**: Valid markdown, tagged code blocks, hierarchical headings

### Content Validation

1. **Language**: Imperative mood | MUST/SHOULD/MAY correct | No suggestive/passive
2. **OS agnostic**: No OS commands | Forward slashes | Cross-platform
3. **Agent-centric**: Executable steps | Explicit prerequisites | Clear criteria
4. **Complete**: No TODO/TBD | No empty sections | All examples present
5. **Markdown rendering**: Metadata lines do not collapse | No reliance on soft-wrap | Prefer list format
6. **References**: All references use action-gated WHEN format | No content duplication from referenced files
7. **Validation criteria**: Requirements files and adapter specs MUST include validation criteria and checklists

### Validation Scoring

**Total**: 100 points

**Breakdown**:
- File structure (20 points): Header, sections, formatting
- Language style (20 points): Imperative, active, concise
- OS agnostic (15 points): No OS-specific elements
- Agent-centric (20 points): Executable, clear, structured
- Completeness (15 points): No placeholders, all sections filled
- Examples (10 points): Valid and invalid examples provided

**Pass threshold**: ≥95/100

---

## Modification Guidelines

### Before Modifying

**MUST**: Read `core.md` + `AGENTS.md` | Identify affected files | Check contradictions | Validate consistency

**MUST NOT**: Skip reading | Break principles | Add non-agent-centric language | Add OS-specific elements

### Change Types

**New Requirement**: Create in `requirements/` | Follow structure | Include validation | Provide examples | Update references

**New Workflow**: Create in `workflows/` | Follow structure | Define prerequisites | Make executable | Include validation

**Modify Existing**: Read completely | Ensure follows principles | Update version | Maintain consistency | Test

**New Specification**: Create in `FDD/` | Define syntax | Provide examples | Include validation | Reference from AGENTS.md

### After Modification

**MUST**: Validate against core.md | Check references | Update dependents | Test workflows | Update versions

---

## File Organization

### Directory Structure

```
FDD/
├── AGENTS.md              # Core FDD specification for AI agents
├── FDL.md                 # Behavior description language spec
├── requirements/          # Structure requirements
│   ├── core.md           # This file - FDD core requirements
│   ├── adapter-structure.md
│   ├── business-context-structure.md
│   ├── overall-design-structure.md
│   ├── adr-structure.md
│   ├── features-manifest-structure.md
│   ├── feature-design-structure.md
│   ├── feature-changes-structure.md
│   └── workflow-requirements.md
└── workflows/             # Operational workflows
    ├── adapter-config.md
    ├── adapter-validate.md
    ├── business-context.md
    ├── business-context-validate.md
    └── ...
```

### File Naming

**MUST**:
- Use kebab-case: `feature-design-structure.md`
- Use descriptive names
- Use consistent suffixes:
  - `-structure.md` for requirements
  - `-validate.md` for validation workflows
  - No suffix for operation workflows

**MUST NOT**:
- Use camelCase or PascalCase
- Use underscores (except in placeholders)
- Use abbreviations unless standard
- Use version numbers in filenames

---

## Examples

**Valid**: Imperative, structured, agent-parseable
```markdown
# Feature Design Structure Requirements
**Version**: 1.0 | **Purpose**: Define structure | **Scope**: All feature DESIGN.md
## Structure
1. **Section A**: MUST contain summary | MUST reference FEATURES.md
2. **Section B**: MUST use FDL | MUST cover all actors
```

**Invalid**: Suggestive, passive, not structured
```markdown
This document talks about how you might want to structure files...
```

---

## References

**This file is referenced by**:
- `AGENTS.md` - ALWAYS open and follow before modifying FDD
- All workflow files - Follow these principles
- All requirement files - Follow these structures

**Related files**:
- `AGENTS.md` - Core FDD specification for agents
- `adapter-structure.md` - Project-specific adapter requirements
- ALWAYS open and follow `core-workflows.md` WHEN creating or modifying workflow files
- ALWAYS open and follow `core-requirements.md` WHEN creating or modifying requirements files
- ALWAYS open and follow `core-agents.md` WHEN creating or modifying AGENTS.md files
