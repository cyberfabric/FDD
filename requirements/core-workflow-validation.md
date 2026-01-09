# FDD Core: Validation Workflow Content Requirements

**Version**: 1.0  
**Purpose**: Define content requirements for validation workflow files  
**Scope**: All validation workflows in `FDD/workflows/{artifact}-validate.md`

---

## Overview

**Validation workflows** - Automated procedures to validate structure, completeness, consistency

**This file defines**: Content requirements for validation workflow files

**For structure**: See `core-workflows.md`

---

## Key Principle

**Validation workflows MUST be**:
- Fully automated (no user interaction)
- Short and focused (follow requirements file validation sections)
- Output to chat only (no report files)

**Rationale**: Requirements files define validation criteria. Validation workflows implement those criteria with minimal additional logic.

---

## Content Requirements

### Prerequisites Section

**Format**: `- [ ] {Artifact} at {path}` | Requirements file reference

**Example**: `- [ ] DESIGN.md at architecture/DESIGN.md` | `Requirements: requirements/overall-design-structure.md`

---

## Steps Section

**MUST contain**:
- Read requirements file step
- Read artifact to validate step
- Validation steps (per requirements criteria)
- Calculate total score step

**MUST reference**: Requirements file validation criteria exactly

**MUST NOT contain**:
- User interaction
- File creation steps
- Invented validation criteria

---

## Output Section

**To chat only**:
```markdown
## Validation: {artifact}
**Score**: {x}/100 | **Status**: PASS/FAIL

### Findings
- Structure ({x}/20): ✅/❌ items
- Completeness ({x}/30): ✅/❌ items  
- Non-Contradiction ({x}/25): ✅/❌ items
- Coverage ({x}/25): ✅/❌ items

### Next
PASS → `{next}` | FAIL → Fix + Re-run
```

---

## Next Steps Section

**MUST provide**:
- Pass scenario (suggest next workflow)
- Fail scenario (fix and re-validate)
- Exact workflow names

**Format**: PASS (≥{threshold}) → `{next-workflow}` | FAIL → Review + Fix + Re-run

---

## Content Requirements

**MUST**:
- Reference specific requirements file
- Use exact validation criteria from requirements
- Follow scoring breakdown from requirements
- Use same terminology as requirements

**MUST NOT**:
- Invent new validation criteria
- Skip requirements sections
- Change scoring weights

---

## Scoring

| Artifact | Threshold |
|----------|----------|
| BUSINESS/DESIGN/ADR | ≥90/100 |
| FEATURES/Adapter | ≥95/100 |
| Feature DESIGN/CHANGES | 100/100 |

**Credit**: Full/Partial/None per requirements

---

## Token Limits

**Validation workflows**: Soft ≤800 | Hard ≤1,200 tokens

**Why shorter than operation workflows**:
- Follow requirements file structure
- Minimal additional logic
- Automated (no interaction)
- Output to chat (no file generation)

**If exceeded**:
- Validation logic too complex
- Extract common patterns to requirements file
- Reference requirements more directly

---

## Validation Criteria

### Requirements Following (40 points)

- References specific requirements sections
- Uses exact validation criteria
- Follows scoring from requirements
- No invented criteria

### Automation (30 points)

- No user interaction
- Fully executable by agent
- Clear pass/fail logic
- Deterministic outcome

### Output Quality (20 points)

- Outputs to chat only
- Clear formatting
- Actionable recommendations
- Severity indicators

### Next Steps (10 points)

- Pass path clear
- Fail path clear
- Workflow names exact

**Pass threshold**: ≥95/100

---

## Examples

**Valid validation workflow**:
```markdown
---
description: Validate business context document
---

# Business Context Validation

**Prerequisites**:
- [ ] BUSINESS.md exists at `architecture/BUSINESS.md`
- [ ] Requirements: `requirements/business-context-structure.md`

## Steps

### 1. Read Requirements

Open `requirements/business-context-structure.md`
Extract validation sections

### 2. Read BUSINESS.md

Open `architecture/BUSINESS.md`
Parse sections A, B, C, D

### 3. Validate Structure (30 points)

From requirements Section 3:
- Section A: Vision [10 pts]
- Section B: Actors [10 pts]
- Section C: Capabilities [10 pts]

Score: {X}/30

### 4. Validate IDs (20 points)

From requirements Section 4:
- Actors: ACT-### format [10 pts]
- Capabilities: CAP-### format [10 pts]

Score: {X}/20

### 5. Validate Completeness (30 points)

- No TODO markers [10 pts]
- All actors have description [10 pts]
- All capabilities defined [10 pts]

Score: {X}/30

### 6. Calculate Total

Total: {X}/100
Status: {PASS if ≥90, else FAIL}

## Output Format

Display in chat:

**BUSINESS.md Validation**

**Score**: {X}/100
**Status**: PASS/FAIL

**Issues**: {list}

## Next Steps

**If PASS**: Suggest `design` workflow

**If FAIL**: Fix BUSINESS.md | Re-run `business-context` | Re-validate
```

**Invalid validation workflow**:
```markdown
# Validate Something

Check if the file looks good.

If good, continue. If not, fix it.
```

---

## References

**This file is referenced by**:
- ALWAYS open and follow this file WHEN creating or modifying validation workflows

**References**:
- `core-workflows.md` - Workflow structure requirements
- `core.md` - Core FDD principles
