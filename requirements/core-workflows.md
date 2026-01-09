# FDD Core: Workflow File Structure

**Version**: 1.0  
**Purpose**: Define structural requirements for FDD workflow files  
**Scope**: All files in `FDD/workflows/*.md`

---

## Overview

**Workflow files** - Executable procedures for FDD operations and validations

**This file defines**: Structure and formatting requirements for workflow files

**For execution guidance**: See specific workflow requirements files

---

## File Structure

### MUST Have

1. **YAML frontmatter**:
   ```yaml
   ---
   description: {short imperative title, ≤10 words}
   ---
   ```

2. **Title**: `# {Workflow Name}`

3. **Prerequisites section**:
   ```markdown
   **Prerequisites**:
   - [ ] {requirement} - validate: {command or check}
   ```

4. **Steps section**:
   ```markdown
   ## Steps
   
   ### 1. {Action Verb} {Object}
   
   {Instructions}
   ```

5. **Next Steps section**:
   ```markdown
   ## Next Steps
   
   **If {condition}**: Suggest `{next-workflow}`
   
   **If {failure}**: Fix | Re-run | Re-validate
   ```

**Workflow-type-specific sections**: See workflow type requirements

### MUST NOT Have

- Separate validation report files
- Vague prerequisites without validation commands
- Missing next workflow suggestions
- Steps without action verbs
- OS-specific commands

---

## Workflow Types

**Two types**: Operation workflows | Validation workflows

**Operation workflows** - Create/update documents or code (no suffix, e.g., `design.md`)
- MUST support both creation and editing of artifacts
- MUST detect if artifact exists and offer appropriate mode
- MUST be independent and self-sufficient

**Validation workflows** - Validate structure/completeness (suffix `-validate`, e.g., `design-validate.md`)

ALWAYS open and follow `core-workflow-operations.md` WHEN creating or modifying operation workflows

ALWAYS open and follow `core-workflow-validation.md` WHEN creating or modifying validation workflows

---

## Operation Workflow Requirements

**ALL operation workflows MUST**:

1. **Check artifact existence** at start:
   - If artifact exists → Enter UPDATE/EDIT mode
   - If artifact does NOT exist → Enter CREATE mode

2. **Support both modes**:
   - CREATE mode: Generate new artifact from scratch
   - UPDATE/EDIT mode: Read existing artifact, propose changes, update content

3. **Be independent**:
   - Can create new artifact without dependencies (where applicable)
   - Can edit existing artifact without recreating from scratch
   - User can run workflow multiple times to iterate

4. **Mode detection steps**:
   ```markdown
   ### 1. Detect Mode
   
   Check if `{artifact-path}` exists:
   - **If exists**: UPDATE mode - Read and propose changes
   - **If NOT exists**: CREATE mode - Generate from scratch
   ```

5. **Interactive for both modes**:
   - CREATE: Ask questions, propose defaults, generate content
   - UPDATE: Show current content, ask what to change, propose updates

---

## Style Requirements

### Prerequisites

**Format**:
```markdown
**Prerequisites**:
- [ ] {Artifact} exists at `{path}` - validate: Check file exists
- [ ] {Artifact} validated - validate: Score ≥{threshold}
```

**MUST**:
- Use checkbox format `- [ ]`
- Include validation command or check
- Be specific and verifiable
- Use absolute or relative paths

**MUST NOT**:
- Leave vague ("setup complete")
- Skip validation method
- Use OS-specific commands

### Steps

**Format**:
```markdown
### 1. {Action Verb} {Object}

{Instruction 1}
{Instruction 2}

**Example**:
```language
{code example}
```

### 2. {Next Action}
```

**MUST**:
- Start with action verb (Read, Create, Validate, Extract)
- Number steps sequentially
- Use imperative mood
- Include examples for complex operations
- Make steps executable by AI agent

**MUST NOT**:
- Use suggestive language ("you might want to...")
- Leave steps ambiguous
- Use passive voice
- Skip validation criteria

### Next Workflow Suggestions

**MUST**:
- Suggest logical next workflow
- Provide failure recovery path
- Use exact workflow filenames
- Include conditional paths (success/failure)

---

## Validation Criteria

### Structure (20 points)

- YAML frontmatter present
- All required sections present
- Proper markdown formatting
- Hierarchical headings

### Prerequisites (15 points)

- All prerequisites listed
- Validation commands specified
- Checkboxes used
- Prerequisites verifiable

### Steps (30 points)

- Steps numbered sequentially
- Action verbs used
- Imperative mood
- Executable by agent
- Examples provided where needed

### Workflow-Specific Sections (15 points)

- Required sections present per workflow type
- Clear format specified
- Criteria defined

### Next Steps (10 points)

- Success path defined
- Failure path defined
- Workflow names exact
- Validation step included

### Style (10 points)

- Concise language
- No OS-specific commands
- Agent-centric
- No suggestive language

**Pass threshold**: ≥95/100

---

## Token Limits

**Workflow files**: Soft ≤1,000 | Hard ≤1,500 tokens

**If exceeded**: Extract common patterns to separate files | Reference instead of duplicate | Use tables

---

## Examples

**Valid workflow structure**:
```markdown
---
description: Create feature design document
---

# Feature Design Creation

**Prerequisites**:
- [ ] FEATURES.md exists - validate: Check file at `architecture/features/FEATURES.md`
- [ ] FEATURES.md validated - validate: Score ≥90/100

## Steps

### 1. Read FEATURES.md

Open `architecture/features/FEATURES.md`

### 2. Create Feature Directory

Create directory: `architecture/features/feature-{slug}/`

## Next Steps

**If complete**: Suggest `{next-workflow}`
```

**Invalid workflow**:
```markdown
# Some Workflow

You should probably check if the file exists first.
```

---

## References

**This file is referenced by**:
- ALWAYS open and follow `core.md` WHEN creating or modifying FDD core files
- All workflow files ALWAYS follow this structure

**References**:
- ALWAYS open and follow `core-workflow-operations.md` WHEN creating or modifying operation workflows
- ALWAYS open and follow `core-workflow-validation.md` WHEN creating or modifying validation workflows
- `core.md` - Core FDD principles
