---
description: Create or update feature implementation plan
---

# Create or Update Feature Implementation Plan

**Type**: Operation  
**Role**: Developer  
**Artifact**: `architecture/features/feature-{slug}/CHANGES.md`

---

## Requirements

**ALWAYS open and follow**: `../requirements/feature-changes-structure.md`

Extract:
- Required structure (change entries)
- Task breakdown format
- Validation criteria

---

## Prerequisites

**MUST validate**:
- [ ] Feature DESIGN.md exists - validate: Check file at feature directory
- [ ] Feature DESIGN.md validated - validate: Score 100/100 + 100%

**If adapter missing**: Auto-trigger `adapter` workflow (Developer requires adapter)

---

## Steps

### 1. Detect Mode

Check if `architecture/features/feature-{slug}/CHANGES.md` exists:
- **If exists**: UPDATE mode - Add/edit/remove changes
- **If NOT exists**: CREATE mode - Decompose feature into changes

### 2. Read Feature Design

Open `architecture/features/feature-{slug}/DESIGN.md`

Extract:
- All requirements (Section F)
- Actor flows (Section B)
- Algorithms (Section C)
- Technical details (Section E)

### 3. Mode-Specific Actions

**CREATE Mode**:
- Decompose feature into changes from scratch
- Proceed to Step 4

**UPDATE Mode**:
- Read existing CHANGES.md
- Extract current changes with IDs, status, tasks
- **Check if all changes completed**: All changes have status `✅ COMPLETED`
- **If all completed**: Offer to archive CHANGES.md (skip to Step 7)
- **If not all completed**: Ask user: What to update?
  - Add new change
  - Edit existing change (description, requirements, tasks, status)
  - Remove change
  - Update change status
  - Mark change as implemented
- Proceed to Step 4 with appropriate action

### 4. Decompose/Update Changes

**For feature requirements**:
- Group into atomic changes (1-5 requirements per change)
- Each change = one deployable unit
- Prioritize changes (HIGH, MEDIUM, LOW)

**Generate change list**:
- Change ID: `change-{slug}`
- Implements: Requirement IDs
- Priority
- Estimated effort

Store as: `CHANGES[]`

### 3. Break Down Tasks

**For each change**:
- Identify granular tasks (5-15 tasks per change)
- Each task: Action, File, Validation
- Tasks executable by developer

### 4. Create CHANGES.md

Generate content following `feature-changes-structure.md`:
- Header with summary
- Change entries with tasks
- Status tracking (NOT_STARTED for all initially)

Ensure:
- All feature requirements covered
- Tasks are granular and executable
- File paths specified
- Validation criteria per task

### 5. Summary and Confirmation

Show:
- File path
- {count} changes identified
- Requirements coverage: 100%
- Total tasks: {count}

Ask: Create file? [yes/no/modify]

### 6. Create File

After confirmation:
- Create `architecture/features/feature-{slug}/CHANGES.md`
- Verify creation

### 7. Archive Completed CHANGES.md (Optional)

**When**: All changes status = `✅ COMPLETED`

**Steps**:
1. Check summary: `**Completed**: {N}` equals `**Total Changes**: {N}`
2. Ask user: Archive CHANGES.md? [yes/no]
3. **If yes**:
   - Create archive directory: `architecture/features/feature-{slug}/archive/`
   - Generate filename: `YYYY-MM-DD-CHANGES.md` (current date)
   - Move CHANGES.md to archive with timestamp
   - Confirm archiving complete
4. **If no**: Keep CHANGES.md in place

**Result**: CHANGES.md archived for historical reference, feature ready for future changes

---

## Validation

Run: `feature-changes-validate`

Expected:
- Score: ≥90/100
- Status: PASS
- 100% requirements coverage

---

## Next Steps

**If all changes completed**: Optional archive (Step 7), then feature complete

**If validation passes**: `feature-change-implement` workflow (implement first change)

**If validation fails**: Fix CHANGES.md, re-validate
