---
description: Create or update feature design document
---

# Create or Update Feature Design

**Type**: Operation  
**Role**: Solution Architect  
**Artifact**: `architecture/features/feature-{slug}/DESIGN.md`

---

## Requirements

**ALWAYS open and follow**: `../requirements/feature-design-structure.md`

Extract:
- Required sections (A-G)
- FDL requirements for behavioral sections
- Validation criteria

---

## Prerequisites

**MUST validate**:
- [ ] FEATURES.md exists - validate: Check file at `architecture/features/FEATURES.md`
- [ ] FEATURES.md validated - validate: Score ≥90/100
- [ ] Feature exists in FEATURES.md - validate: Feature ID present

**If missing**: Run prerequisite workflows

---

## Steps

### 1. Identify Feature

Ask user: Which feature to design/update?

Options: List from FEATURES.md

Store feature ID and slug

### 2. Detect Mode

Check if `architecture/features/feature-{slug}/DESIGN.md` exists:
- **If exists**: UPDATE mode - Read and propose changes
- **If NOT exists**: CREATE mode - Generate from scratch

### 3. Read Context

Open `architecture/DESIGN.md` and `architecture/features/FEATURES.md`

Extract:
- Requirements assigned to this feature
- Actors relevant to feature
- Dependencies on other features

### 3. Design Feature

**Interactive questions per section** (following feature-design-structure.md):

**Section A: Overview**
- Feature purpose
- Scope boundaries

**Section B: Actor Flows** (use FDL)
- For each actor: Main flow, alternative flows
- Use FDL format from requirements

**Section C: Algorithms** (use FDL)
- Key business logic
- State transitions
- Use FDL format

**Section D: State Machines** (if applicable)
- States and transitions
- Use FDL format

**Section E: Technical Details**
- Database schemas (if adapter available)
- API endpoints (if adapter available)
- Integration points

**Section F: Requirements**
- Map requirements from DESIGN.md
- Generate requirement IDs

**Section G: Test Scenarios**
- Acceptance criteria per requirement
- Edge cases

### 4. Create feature/DESIGN.md

Generate content following `feature-design-structure.md`

Ensure:
- No contradictions with overall DESIGN.md
- No type redefinitions
- FDL used correctly
- All requirement IDs valid

### 5. Summary and Confirmation

Show:
- File path
- Sections included
- Requirements count
- Actor flows count

Ask: Create file? [yes/no/modify]

### 6. Create File

After confirmation:
- Create/update `architecture/features/feature-{slug}/DESIGN.md`
- Verify creation

---

## Validation

Run: `feature-validate`

Expected:
- Score: 100/100
- Completeness: 100%
- Status: PASS

---

## Next Steps

**If validation passes**: `feature-changes` workflow

**If validation fails**: Fix feature DESIGN.md, re-validate
