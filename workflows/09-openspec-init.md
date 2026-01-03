# Initialize OpenSpec for Feature

**Phase**: 3 - Feature Development  
**Purpose**: Create OpenSpec structure and first change for feature implementation through guided selection

---

## Prerequisites

- Feature DESIGN.md validated (100/100 + 100%)
- Feature status IN_PROGRESS
- Feature directory exists: `architecture/features/feature-{slug}/`

---

## Overview

This workflow initializes OpenSpec structure for a feature, then guides you through creating the first change by reading planned changes from Feature DESIGN.md Section F.

**Key Principle**: Read design, propose changes, confirm before creating.

---

## Interactive Questions

### Q1: Feature Slug
```
Which feature are you initializing OpenSpec for?
Provide feature slug: ___

Example: "user-auth", "payment-flow"
```
**Store as**: `FEATURE_SLUG`

### Q2: Read and Display Planned Changes

**Action**: Read `architecture/features/feature-{FEATURE_SLUG}/DESIGN.md` Section F

**Extract**:
- OpenSpec changes list from Section F
- Each change should have: name, description, scope, dependencies

**Display to User**:
```
Planned OpenSpec Changes (from DESIGN.md Section F):
───────────────────────────────────────────────────

{If changes found in Section F}
1. {Change 001 name}
   Description: {from DESIGN.md}
   Scope: {from DESIGN.md}
   Dependencies: {from DESIGN.md}

2. {Change 002 name}
   Description: {from DESIGN.md}
   Scope: {from DESIGN.md}
   Dependencies: {from DESIGN.md}

...

{If no changes in Section F or Section F empty}
⚠️ Section F does not have detailed OpenSpec changes.
You'll need to define the first change manually.
```

### Q3: Select or Define First Change

**If changes found in Section F**:
```
Which change should be created first?

Options:
  1. Change 001: {name from DESIGN.md}
  2. Change 002: {name from DESIGN.md}
  ...
  N. Define custom change

Your choice: ___
```

**If no changes in Section F**:
```
Section F doesn't have detailed changes. Let's define the first change:

Change name (kebab-case, e.g., "implement-core"): ___
Brief description: ___
Key scope items (one per line):
- ___
- ___
- ___
```

**Store as**: `FIRST_CHANGE_NAME`, `FIRST_CHANGE_DESC`, `FIRST_CHANGE_SCOPE[]`

### Q4: Confirm Initialization

**Display Summary**:
```
OpenSpec Initialization Summary:
────────────────────────────────
Feature: feature-{FEATURE_SLUG}
First Change: {FIRST_CHANGE_NAME}

Will create:
✓ openspec/ directory structure
✓ openspec/specs/ (source of truth)
✓ openspec/changes/{FIRST_CHANGE_NAME}/
  ✓ proposal.md (Why, What, Impact)
  ✓ tasks.md (Implementation checklist)
  ✓ specs/ (Delta specifications)
  ✓ design.md (if complexity requires)

First change details:
- Description: {FIRST_CHANGE_DESC}
- Scope: {list FIRST_CHANGE_SCOPE items}

Proceed with initialization? (y/n)
```

**Expected Outcome**: User confirms or cancels

---

## Requirements

### 1. Create OpenSpec Structure

**Requirement**: Create OpenSpec directory structure manually

**Commands**:
```bash
cd architecture/features/feature-{slug}/
mkdir -p openspec/specs
mkdir -p openspec/changes/{FIRST_CHANGE_NAME}/specs
```

**What This Does**:
- Creates `openspec/` root directory
- Creates `openspec/specs/` for source of truth (merged specifications)
- Creates `openspec/changes/` for active changes
- Creates first change directory `changes/{FIRST_CHANGE_NAME}/`
- Creates `specs/` subdirectory within change for delta specifications

**Expected Outcome**: Complete OpenSpec structure created

**Note**: FDD workflow creates OpenSpec structure directly. No external CLI commands needed.

---

### 2. Generate Proposal Document

**Requirement**: Write proposal.md following OpenSpec format

**Location**: `openspec/changes/{FIRST_CHANGE_NAME}/proposal.md`

**Generated Content** (OpenSpec standard):
```markdown
# Change: {FIRST_CHANGE_DESC from Q3}

## Why
{Extract from DESIGN.md Section F if available, otherwise:}
This change implements the first phase of {FEATURE_NAME} feature.
{FIRST_CHANGE_DESC}

## What Changes
{For each item in FIRST_CHANGE_SCOPE from Q3}
- {Scope item}

{If any breaking changes identified}
- **BREAKING**: {Breaking change description}

## Impact
- Affected specs: {Derive from FIRST_CHANGE_SCOPE}
- Affected code: {Key modules/files from scope}
```

**Content Source**: 
- Primary: User answers from Q3
- Secondary: `../../DESIGN.md` Section F (if detailed change found)

**Expected Outcome**: Proposal created with actual content from user input

**Validation Criteria**:
- Contains Why, What Changes, Impact sections
- Content based on user answers, not placeholders
- Breaking changes marked if any

---

### 3. Generate Tasks Checklist

**Requirement**: Write tasks.md with implementation steps

**Location**: `openspec/changes/{FIRST_CHANGE_NAME}/tasks.md`

**Generated Content** (OpenSpec standard):
```markdown
## 1. Implementation
{Generate tasks from FIRST_CHANGE_SCOPE}
{For each scope item, create 1-3 tasks}
- [ ] 1.{N} {Actionable task derived from scope item}

{Always add testing task}
- [ ] 1.{N+1} Write tests for implemented functionality

{Add validation task}
- [ ] 1.{N+2} Validate against Feature DESIGN.md Section B/C
```

**Task Generation Guidelines**:
- Derive from FIRST_CHANGE_SCOPE items
- Each scope item → 1-3 specific tasks
- Always include testing
- Always include validation
- Number sequentially (1.1, 1.2, etc.)

**Expected Outcome**: Actionable checklist with meaningful tasks

**Validation Criteria**:
- Tasks derived from scope, not generic
- Testing included
- Validation included
- All tasks actionable and specific

---

### 4. Create Delta Specifications

**Requirement**: Write delta specs using OpenSpec format

**Location**: `openspec/changes/{change-name}/specs/{capability}/spec.md`

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

**Expected Outcome**: Delta specs created per affected capability

---

### 5. Create design.md (Optional)

**Requirement**: Create design.md only if needed

**Location**: `openspec/changes/{change-name}/design.md`

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

### 7. Validate with OpenSpec

**Requirement**: Validate change structure and specs

**Command**:
```bash
openspec validate {change-name} --strict
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

### 8. Update Feature DESIGN.md

**Requirement**: Mark first change as initialized in Feature DESIGN.md

**Location**: `../../DESIGN.md` (Feature DESIGN.md, not openspec/design.md)

**Update Section F**:
```markdown
## F. Validation & Implementation

### OpenSpec Changes

**Active Changes**: See `openspec/changes/` for implementation details:
- `{FIRST_CHANGE_NAME}` - {FIRST_CHANGE_DESC} [Status: 🔄 IN_PROGRESS]

{Keep remaining planned changes from original Section F}
```

**Expected Outcome**: Feature DESIGN.md updated with active change status

**Note**: Feature design is in `architecture/features/feature-{slug}/DESIGN.md`

---

### 9. Show Summary

**Requirement**: Display what was created

**Display Summary**:
```
OpenSpec Initialization Complete!
────────────────────────────────────
Feature: feature-{FEATURE_SLUG}

Created:
✓ openspec/ directory structure initialized
✓ openspec/changes/{FIRST_CHANGE_NAME}/
  ✓ proposal.md (Why, What, Impact)
  ✓ tasks.md ({N} implementation tasks)
  ✓ specs/ directory (ready for delta specs)
  {If design.md created: "✓ design.md (technical decisions)"}

✓ Feature DESIGN.md Section F updated

First Change Details:
- Name: {FIRST_CHANGE_NAME}
- Description: {FIRST_CHANGE_DESC}
- Tasks: {N} items to implement

Next Steps:
1. Create delta specifications in specs/{capability}/spec.md
2. Validate: openspec validate {FIRST_CHANGE_NAME} --strict
3. Start implementation: Run workflow 10-openspec-change-implement
```

**Expected Outcome**: Summary displayed

---

## Completion Criteria

OpenSpec initialization complete when:

- [ ] User selected feature slug (Q1)
- [ ] Planned changes read from DESIGN.md Section F (Q2)
- [ ] User selected or defined first change (Q3)
- [ ] User confirmed initialization (Q4)
- [ ] `openspec/` initialized with `openspec init` command
- [ ] `openspec/changes/{FIRST_CHANGE_NAME}/` created manually
- [ ] `proposal.md` generated with actual content from Q3:
  - [ ] Why, What Changes, Impact sections present
  - [ ] Content from user answers, not placeholders
- [ ] `tasks.md` generated with tasks derived from scope:
  - [ ] Tasks specific to scope items
  - [ ] Testing tasks included
  - [ ] Validation tasks included
- [ ] Delta specs directory created (specs content added later)
- [ ] `design.md` created if complexity requires it (optional)
- [ ] Feature DESIGN.md Section F updated with active change
- [ ] Summary displayed to user
- [ ] Ready to create delta specs and validate

---

## Common Challenges

### Issue: Too Many Tasks

**Resolution**: Break change into smaller changes (001, 002, etc.). Each change should be completable in 4-8 hours.

### Issue: Unclear Specs

**Resolution**: Return to DESIGN.md, clarify Section E (Technical Details). Specs should be unambiguous.

---

## Next Activities

After OpenSpec initialization:

1. **Review Proposal**: Ensure implementation plan is clear
   - Verify scope
   - Check dependencies
   - Validate effort estimate

2. **Start Implementation**: Run `10-openspec-change-implement.md`
   - Follow tasks.md checklist
   - Implement according to specs
   - Test as you go

3. **Track Progress**: Update tasks.md as work progresses

---

## OpenSpec Best Practices

**Changes Should Be**:
- **Atomic**: Self-contained unit of work
- **Traceable**: Clear what changed and why
- **Testable**: Verification criteria defined
- **Reversible**: Can be undone if needed

**Specs Should Be**:
- **Precise**: No ambiguity
- **Complete**: All details specified
- **Consistent**: Align with DESIGN.md
- **Reviewable**: Easy to validate

---

## References

- **Core FDD**: `../AGENTS.md` - OpenSpec integration
- **OpenSpec Docs**: https://openspec.dev - Full OpenSpec framework
- **Next Workflow**: `10-openspec-change-implement.md`
