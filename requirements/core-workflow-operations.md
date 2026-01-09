# FDD Core: Operation Workflow Content Requirements

**Version**: 1.0  
**Purpose**: Define content requirements for operation workflow files  
**Scope**: All operation workflows in `FDD/workflows/{operation}.md` (no `-validate` suffix)

---

## Overview

**Operation workflows** - Interactive procedures to create, update, modify documents or code

**This file defines**: Content requirements for operation workflow files

**For structure**: See `core-workflows.md`

---

## Content Requirements

### Prerequisites Section

**Format**: `- [ ] {Artifact} at {path} - validate: {command}` | Validation state | Environment checks

**Example**: `- [ ] BUSINESS.md at architecture/BUSINESS.md - validate: Score ≥90/100`

---

## Steps Section

**MUST contain**:
- Interactive question steps (with proposed answers)
- Data processing/transformation steps
- File creation steps (with summary)
- User confirmation points

**MUST include**:
- Proposed answers based on context
- Summary before file creation
- Confirmation prompts

**MUST NOT contain**:
- Open-ended questions without proposals
- File creation without confirmation
- Placeholder content (TODO, [Description])

---

## Validation Section

**Format**: `Run: {artifact}-validate` | Expected score ≥{threshold} | Status: PASS

---

## Next Steps Section

**Format**: Success → `{next-workflow}` | Failure → Fix + Re-run


---

## Content Guidelines

**MUST reference**: Parent artifacts (BUSINESS.md, DESIGN.md, FEATURES.md as appropriate)

**MUST include**: Domain model references (no redefinition)

**MUST specify**: File paths, expected sections, validation criteria

---

## Token Limits

**Operation workflows**: Soft ≤1,000 | Hard ≤1,500 tokens

**If exceeded**:
- Extract common patterns to separate documentation
- Reference instead of duplicate
- Use tables for structured data
- Keep only essential instructions

---

## Validation Criteria

### Interaction Quality (30 points)

- Clear questions with proposed answers
- One question at a time
- User confirmation required
- Proposals based on context

### Prerequisites (15 points)

- All dependencies listed
- Validation commands specified
- Parent artifacts checked
- Environment validated

### Steps Executability (30 points)

- Steps executable by AI agent
- Clear input/output for each step
- No ambiguous instructions
- Examples provided

### Validation Integration (15 points)

- Validation workflow referenced
- Expected outcome specified
- Failure path defined

### Next Workflow (10 points)

- Success path clear
- Failure path clear
- Exact workflow names
- Validation step included

**Pass threshold**: ≥95/100

---

## Examples

**Valid operation workflow**:
```markdown
---
description: Create overall design document
---

# Overall Design Creation

**Prerequisites**:
- [ ] BUSINESS.md exists - validate: Check file at `architecture/BUSINESS.md`
- [ ] BUSINESS.md validated - validate: Score ≥90/100

## Steps

### 1. Read Business Context

Open `architecture/BUSINESS.md`
Extract:
- Vision statement
- Actors list (Section B)
- Capabilities list (Section C)

### 2. Define Architecture

Ask user:
- Architecture style: {propose based on capabilities}
- Key components: {propose 3-5 components}

Show proposed architecture diagram structure
Wait for user confirmation

### 3. Create DESIGN.md

Show summary:
- Path: `architecture/DESIGN.md`
- Sections: A (Overview), B (Requirements), C (Architecture)
- References: BUSINESS.md actors and capabilities

Confirm? [yes/modify/cancel]

Create file

## Validation

Run: `design-validate`

Expected:
- Score: ≥90/100
- Status: PASS

## Next Steps

**If validation passes**: Suggest `features` workflow

**If validation fails**: Fix DESIGN.md | Re-run this workflow | Re-validate
```

**Invalid operation workflow**:
```markdown
# Create Design

Create the design document with all the sections.

Make sure it looks good.
```

---

## References

**This file is referenced by**:
- ALWAYS open and follow this file WHEN creating or modifying operation workflows

**References**:
- `core-workflows.md` - Workflow structure requirements
- `core.md` - Core FDD principles
