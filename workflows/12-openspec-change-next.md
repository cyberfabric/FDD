# Create Next OpenSpec Change

**Phase**: 3 - Feature Implementation  
**Purpose**: Create next change from Feature DESIGN.md implementation plan through guided selection

---

## Prerequisites

- OpenSpec initialized for feature
- Previous change completed and archived
- Feature DESIGN.md Section F has multiple changes planned
- At least one change remaining to implement

---

## Overview

This workflow reads the Feature DESIGN.md Section F to identify remaining changes, displays them to the user, and guides through creating the next change.

**Key Principle**: Read plan, show remaining changes, let user choose next.

---

## Interactive Questions

### Q1: Feature Slug
```
Which feature are you creating the next change for?
Provide feature slug: ___

Example: "user-auth", "payment-flow"
```
**Store as**: `FEATURE_SLUG`

### Q2: Read and Display Change Status

**Action**: Read `architecture/features/feature-{FEATURE_SLUG}/DESIGN.md` Section F

**Extract**:
- List of all planned OpenSpec changes
- Current status of each change (✅ COMPLETED, 🔄 IN_PROGRESS, ⏳ NOT_STARTED)
- Identify completed changes from `openspec/changes/archive/`

**Display to User**:
```
OpenSpec Changes Status (from DESIGN.md Section F):
────────────────────────────────────────────────────

{For each change in Section F}
{Status Icon} Change {NNN}: {Change Name}
  Description: {from DESIGN.md}
  Scope: {from DESIGN.md}
  Dependencies: {from DESIGN.md}
  Status: {✅ COMPLETED / 🔄 IN_PROGRESS / ⏳ NOT_STARTED}

────────────────────────────────────────────────────
Completed: {count} | In Progress: {count} | Remaining: {count}
```

### Q3: Select Next Change

**If multiple NOT_STARTED changes available**:
```
Which change should be created next?

Options:
{For each NOT_STARTED change}
  {N}. Change {NNN}: {name}
     {brief description}
     Dependencies: {list or "None"}

Your choice: ___
```

**If only one NOT_STARTED change remaining**:
```
Only one change remaining:
Change {NNN}: {name}

Proceed with this change? (y/n)
```

**If no NOT_STARTED changes**:
```
✅ All changes completed!

No remaining changes to create.
Consider running workflow 07-complete-feature to mark feature as done.
```

**Store as**: `NEXT_CHANGE_NUMBER`, `NEXT_CHANGE_NAME`, `NEXT_CHANGE_DESC`, `NEXT_CHANGE_SCOPE[]`

### Q4: Confirm Creation

**Display Summary**:
```
Next Change Creation Summary:
────────────────────────────────
Feature: feature-{FEATURE_SLUG}
Next Change: Change {NEXT_CHANGE_NUMBER}: {NEXT_CHANGE_NAME}

Will create:
✓ openspec/changes/{NEXT_CHANGE_NAME}/
  ✓ proposal.md (Why, What, Impact)
  ✓ tasks.md (Implementation checklist)
  ✓ specs/ (Delta specifications)
  ✓ design.md (if complexity requires)

Change details:
- Description: {NEXT_CHANGE_DESC}
- Scope: {list NEXT_CHANGE_SCOPE items}
- Dependencies: {list or "None"}

Proceed with creation? (y/n)
```

**Expected Outcome**: User confirms or cancels

---

## Requirements

### 1. Create Change Directory Structure

**Requirement**: Manually create change directory

**Commands**:
```bash
cd architecture/features/feature-{FEATURE_SLUG}/
mkdir -p openspec/changes/{NEXT_CHANGE_NAME}/specs
```

**What This Does**:
- Creates `changes/{NEXT_CHANGE_NAME}/` directory
- Creates `specs/` subdirectory for delta specifications

**Expected Outcome**: Change directory structure created

**Note**: OpenSpec does not have a `create` command. Changes are created manually.

---

### 2. Generate Proposal Document

**Requirement**: Manually create change directory

**Commands**:
```bash
cd architecture/features/feature-{slug}/
mkdir -p openspec/changes/{next-change-name}/specs
```

**What This Does**:
- Creates `changes/{next-change-name}/` directory
- Creates `specs/` subdirectory for delta specifications

**Expected Outcome**: Change directory structure created

**Note**: OpenSpec does not have a `create` command. Changes are created manually.

---

**Requirement**: Write proposal.md following OpenSpec format

**Location**: `openspec/changes/{NEXT_CHANGE_NAME}/proposal.md`

**Generated Content** (OpenSpec standard):
```markdown
# Change: {NEXT_CHANGE_DESC from Q3}

## Why
{Extract "Why" from DESIGN.md Section F for this change if available, otherwise:}
This change implements Change {NEXT_CHANGE_NUMBER} of {FEATURE_NAME} feature.
{NEXT_CHANGE_DESC}

## What Changes
{For each item in NEXT_CHANGE_SCOPE from Q3}
- {Scope item}

{If breaking changes identified in DESIGN.md}
- **BREAKING**: {Breaking change description}

## Impact
- Affected specs: {Derive from NEXT_CHANGE_SCOPE}
- Affected code: {Key modules/files from scope}
- Dependencies: {List dependencies from Q3}
```

**Content Source**: 
- Primary: User selection from Q3 + DESIGN.md Section F
- All content from planned change in DESIGN.md

**Expected Outcome**: Proposal created with actual content from DESIGN.md

**Validation Criteria**:
- Contains Why, What Changes, Impact sections
- Content from DESIGN.md, not placeholders
- Dependencies documented
- Breaking changes marked if any

---

### 3. Generate Tasks Checklist

**Requirement**: Write tasks.md with implementation steps

**Location**: `openspec/changes/{NEXT_CHANGE_NAME}/tasks.md`

**Generated Content** (OpenSpec standard):
```markdown
## 1. Implementation
{Extract tasks from DESIGN.md Section F for this specific change}
{If detailed tasks in DESIGN.md:}
- [ ] 1.{N} {Task from DESIGN.md}

{Otherwise, generate from NEXT_CHANGE_SCOPE:}
{For each scope item, create 1-2 tasks}
- [ ] 1.{N} {Actionable task derived from scope item}

{Always add:}
- [ ] 1.{N+1} Write tests for implemented functionality
- [ ] 1.{N+2} Validate against Feature DESIGN.md Section B/C
- [ ] 1.{N+3} Update documentation if needed
```

**Task Generation Guidelines**:
- Primary: Extract from DESIGN.md Section F for this change
- Fallback: Derive from NEXT_CHANGE_SCOPE items
- Always include: testing, validation, documentation
- Number sequentially (1.1, 1.2, etc.)

**Expected Outcome**: Actionable checklist with specific tasks

**Validation Criteria**:
- Tasks from DESIGN.md or derived from scope
- Testing included
- Validation included
- All tasks actionable and specific

---

### 4. Create Delta Specifications

**Requirement**: Write delta specs using OpenSpec format

**Location**: `openspec/changes/{next-change-name}/specs/{capability}/spec.md`

**Delta Operations** (use these headers):
- `## ADDED Requirements` - New capabilities
- `## MODIFIED Requirements` - Changed behavior
- `## REMOVED Requirements` - Deprecated features
- `## RENAMED Requirements` - Name changes

**Required Format**:
```markdown
## ADDED Requirements
### Requirement: New Feature
The system SHALL provide...

#### Scenario: Success case
- **WHEN** user performs action
- **THEN** expected result
```

**Critical Rules**:
- Every requirement MUST have at least one `#### Scenario:`
- Use `**WHEN**` and `**THEN**` in scenarios
- Use SHALL/MUST for normative requirements
- For MODIFIED: copy full requirement from `openspec/specs/`, then edit

**Content Source**: Extract from Feature DESIGN.md Section E (Technical Details) and Section F

**Expected Outcome**: Delta specs created per affected capability

---

### 5. Create design.md (Optional)

**Requirement**: Create design.md only if needed

**Location**: `openspec/changes/{next-change-name}/design.md`

**Create design.md if ANY apply**:
- Cross-cutting change (multiple services/modules)
- New external dependency
- Significant data model changes
- Security, performance, or migration complexity
- Technical decisions needed before coding

**Otherwise**: Skip this file

**Minimal Structure**:
```markdown
## Context
{Background, constraints}

## Goals / Non-Goals
- Goals: {...}
- Non-Goals: {...}

## Decisions
- Decision: {What and why}
- Alternatives: {Options + rationale}

## Risks / Trade-offs
- {Risk} → Mitigation

## Migration Plan
{Steps, rollback}
```

**Note**: Feature DESIGN.md is at `../../DESIGN.md` - reference it, don't duplicate

**Expected Outcome**: design.md created only if complexity requires it

---

### 6. Validate with OpenSpec

**Requirement**: Validate change structure and specs

**Command**:
```bash
openspec validate {next-change-name} --strict
```

**What This Checks**:
- Change has at least one delta
- All requirements have scenarios
- Scenario format correct (`#### Scenario:`)
- Files not empty
- Delta operations properly formatted

**Expected Outcome**: Validation passes with zero errors

**Resolution if Failed**: Fix reported issues, then re-validate

---

### 7. Update Feature DESIGN.md Status

**Requirement**: Mark change as active in Feature DESIGN.md

**Location**: `../../DESIGN.md`

**Update Section F**:
```markdown
## F. Validation & Implementation

### OpenSpec Changes

**Active Changes**: See `openspec/changes/` for implementation details:
{List completed changes}
- `{previous-change}` - ✅ COMPLETED
{Current change}
- `{NEXT_CHANGE_NAME}` - 🔄 IN_PROGRESS
{Remaining changes}
- `{future-change}` - ⏳ NOT_STARTED
```

**Expected Outcome**: Feature DESIGN.md reflects current implementation status

---

### 8. Show Summary

**Requirement**: Display what was created

**Display Summary**:
```
Next Change Created!
────────────────────────────────────
Feature: feature-{FEATURE_SLUG}

Created:
✓ openspec/changes/{NEXT_CHANGE_NAME}/
  ✓ proposal.md (Why, What, Impact)
  ✓ tasks.md ({N} implementation tasks)
  ✓ specs/ directory (ready for delta specs)
  {If design.md created: "✓ design.md (technical decisions)"}

✓ Feature DESIGN.md Section F updated

Change Details:
- Number: Change {NEXT_CHANGE_NUMBER}
- Name: {NEXT_CHANGE_NAME}
- Description: {NEXT_CHANGE_DESC}
- Tasks: {N} items to implement

Progress:
- Completed: {count} changes
- Current: Change {NEXT_CHANGE_NUMBER}
- Remaining: {count} changes

Next Steps:
1. Create delta specifications in specs/{capability}/spec.md
2. Validate: openspec validate {NEXT_CHANGE_NAME} --strict
3. Start implementation: Run workflow 10-openspec-change-implement
```

**Expected Outcome**: Summary displayed

---

## Completion Criteria

Next change creation complete when:

- [ ] User selected feature slug (Q1)
- [ ] Change status read from DESIGN.md Section F (Q2)
- [ ] User selected next change to create (Q3)
- [ ] User confirmed creation (Q4)
- [ ] `openspec/changes/{NEXT_CHANGE_NAME}/` created manually
- [ ] `proposal.md` generated with content from DESIGN.md:
  - [ ] Why, What Changes, Impact sections present
  - [ ] Content from DESIGN.md Section F, not placeholders
  - [ ] Dependencies documented
- [ ] `tasks.md` generated with tasks from DESIGN.md or scope:
  - [ ] Tasks from DESIGN.md or derived from scope
  - [ ] Testing tasks included
  - [ ] Validation tasks included
- [ ] Delta specs directory created (specs content added later)
- [ ] `design.md` created if complexity requires it (optional)
- [ ] Feature DESIGN.md Section F updated with IN_PROGRESS status
- [ ] Summary displayed to user
- [ ] Ready to create delta specs and validate

---

## Common Challenges

### Issue: Unclear Which Change to Create Next

**Resolution**: Review DESIGN.md Section F implementation plan. Changes should be ordered by dependencies. If order unclear, implement foundational changes first (data model, core logic, then UI/API).

### Issue: Change Plan Changed Since Design

**Resolution**: If implementation reveals changes need to be different:
1. Use workflow 08 (fix-design) to update DESIGN.md Section F
2. Re-validate Feature Design
3. Then create change with updated plan

### Issue: Multiple Changes Could Be Next

**Resolution**: Choose based on:
- Dependency order (prerequisites first)
- Risk level (higher risk earlier for feedback)
- Team capacity (parallel work if independent)

---

## Next Activities

After creating next change:

1. **Implement Change**: Run `10-openspec-change-implement.md`
   - Follow implementation workflow
   - Complete all tasks in tasks.md

2. **Complete When Done**: Run `11-openspec-change-complete.md`
   - Archive change
   - Merge specs

3. **Repeat if Needed**: If more changes remain
   - Run this workflow again for next change
   - Or run `13-openspec-validate.md` to check overall structure

4. **Complete Feature**: When all changes done
   - Run `07-complete-feature.md`
   - Mark feature as IMPLEMENTED

---

## Best Practices

**Change Extraction**:
- Copy implementation details directly from DESIGN.md Section F
- Don't make up new requirements - follow design
- If design is insufficient, fix design first (workflow 08)

**Change Scope**:
- Each change should be completable in 4-8 hours
- If too large, break into multiple changes
- If too small, consider combining with next

**Dependencies**:
- Check if change depends on previous changes being deployed
- Document dependencies in proposal.md Impact section
- Order changes by dependency graph

---

## References

- **Core FDD**: `../AGENTS.md` - OpenSpec integration
- **Feature Design**: `../../DESIGN.md` - Section F implementation plan
- **Previous Workflow**: `11-openspec-change-complete.md` - Complete previous change
- **Next Workflow**: `10-openspec-change-implement.md` - Implement this change
- **OpenSpec Docs**: `../openspec/AGENTS.md` - Full OpenSpec specification
