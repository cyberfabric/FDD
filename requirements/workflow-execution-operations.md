# FDD Operation Workflow Execution

**Version**: 1.0  
**Purpose**: Define execution specifics for operation workflows  
**Scope**: All operation workflows (create/update documents)

---

## Overview

**Operation workflows** - Interactive procedures to create or modify artifacts

**This file defines**: Specific execution instructions for operation workflows

**Read after**: `workflow-execution.md` (general instructions)

**Applies when**: Workflow has `**Type**: Operation`

---

## Execution Sequence

### 1. Prerequisites Check

**Execute**:
1. Read all prerequisite specifications from workflow
2. Check each prerequisite file exists
3. Validate each prerequisite meets threshold
4. Check FDD Adapter exists and is COMPLETE

**If ANY fails**:
- STOP immediately
- Show which prerequisite failed
- Suggest prerequisite workflow
- Wait for user action
- Do NOT proceed

### 2. Specification Reading

**Read in order**:
1. Requirements file for target artifact (from workflow)
2. Parent artifact specifications (if applicable)
3. FDD Adapter specifications (domain model, API contracts)

**Extract**:
- Required sections and structure
- ID formats and validation rules
- Cross-references and dependencies
- Content requirements

### 3. Interactive Input Collection

**Pattern**:
1. Ask ONE question at a time
2. Provide context (why this matters)
3. Propose answer based on project context
4. Show reasoning for proposal
5. Wait for user approval/modification
6. Record answer
7. Move to next question

**MUST**:
- Ask questions sequentially (not all at once)
- Propose specific answers (not open-ended)
- Use project context for proposals
- Show reasoning clearly
- Allow modification of proposals

**MUST NOT**:
- Ask open-ended questions without proposals
- Skip questions
- Assume answers
- Proceed without confirmation

### 4. Content Generation

**Process**:
1. Use collected inputs
2. Follow requirements file structure exactly
3. Generate content section by section
4. Ensure no placeholders (TODO, TBD, [Description])
5. Ensure all IDs follow formats from requirements
6. Reference parent artifacts correctly
7. Use FDL for behavioral sections (if applicable)

**MUST**:
- Follow structure from requirements file
- Use imperative language
- Add mandatory markers (MUST, REQUIRED)
- Wrap IDs in backticks
- No code syntax in design documents
- Reference types from domain model (no redefinition)

**MUST NOT**:
- Invent structure (use requirements)
- Leave placeholders
- Skip required sections
- Redefine parent types
- Use code examples in DESIGN.md

### 5. Summary and Confirmation

**Show user**:
1. File path(s) to be created/modified
2. Structure overview (sections)
3. Key content highlights
4. Parent artifact references
5. ID formats used

**Format**:
```markdown
## Summary

**Files to create/modify**:
- `{path}`: {description}

**Structure**:
- Section A: {name}
- Section B: {name}
...

**Key content**:
- {highlight 1}
- {highlight 2}

**References**:
- {parent artifact 1}
- {parent artifact 2}

**Proceed?** [yes/no/modify]
```

**User responses**:
- **yes**: Create files and proceed to validation
- **no**: Cancel operation
- **modify**: Ask which question to revisit, iterate

### 6. File Creation

**Only after user confirms**:
1. Create file(s) at specified path(s)
2. Write content exactly as generated
3. Ensure file is complete
4. Confirm creation to user

**MUST NOT**:
- Create files before confirmation
- Create incomplete files
- Create placeholder files

### 7. Auto-Validation

**Execute**:
1. Run validation workflow specified in workflow file
2. Wait for validation result
3. Show validation output to user

**If PASS**:
- Show score and status
- Suggest next workflow from workflow file
- Allow user to proceed or stop

**If FAIL**:
- Show score and all issues
- Prioritize issues by severity
- Suggest specific fixes
- Offer to re-run workflow or fix manually
- Do NOT proceed to next workflow until pass

---

## Interactive Patterns

### Question-Answer Pattern

**For each input**:

**Bad (open-ended)**:
```
What should the vision be?
```

**Good (with proposal)**:
```
**Vision Statement**

**Context**: High-level purpose, target users, problems solved

**Proposal**: "Analytics platform for tracking user behavior and generating actionable insights for product teams"

**Reasoning**: Based on project name and existing architecture references

**Approve/modify?**
```

### Context-Based Proposals

**Use available context**:
- Project name and structure
- Existing artifacts (BUSINESS.md, DESIGN.md)
- Code structure (if visible)
- Previous answers in this workflow
- FDD Adapter specifications

**Show reasoning**:
- "Based on existing BUSINESS.md actors..."
- "Following domain model from adapter..."
- "Consistent with previous answer about..."

### Modification Handling

**If user says "modify"**:
1. Ask: "Which question would you like to revisit?"
2. Show numbered list of questions
3. User selects number
4. Ask question again with previous answer shown
5. User provides new answer
6. Continue from that point

---

## Content Requirements

### Structure Following

**ALWAYS follow requirements exactly**:
- Section order
- Section numbering
- Required subsections
- ID formats
- Content requirements per section

**Example** (from business-context-structure.md):
- Section A: Vision
- Section B: Actors (with IDs `fdd-actor-{name}`)
- Section C: Capabilities (with IDs `fdd-capability-{name}`)
- Section D: Additional Context (optional)

### ID Generation

**Follow formats from requirements**:
- Extract ID format from requirements file
- Generate IDs consistently
- Wrap all IDs in backticks
- Ensure uniqueness
- Follow kebab-case

**Example**:
```markdown
### Admin User
**ID**: `fdd-actor-admin`
```

### Cross-References

**When referencing parent artifacts**:
- Use valid IDs from parent
- Wrap IDs in backticks
- Verify ID exists in parent before using
- Use exact ID format

### FDL Usage

**When behavioral sections required** (Section B, C, D in DESIGN.md):
1. Read requirements/FDL.md first
2. Use numbered markdown lists
3. Use bold keywords (**IF**, **FOR EACH**, **WHILE**)
4. Plain English only (no code syntax)
5. Follow FDL patterns from specification

---

## Validation Criteria

### Prerequisites Check (25 points)

**Check**:
- [ ] All prerequisites validated before proceeding
- [ ] Clear stop if prerequisites fail
- [ ] Suggests prerequisite workflows
- [ ] Waits for user to fix

### Interactive Flow (30 points)

**Check**:
- [ ] Questions asked one at a time
- [ ] Context provided for each question
- [ ] Answers proposed based on context
- [ ] Reasoning shown for proposals
- [ ] User confirmation required

### Content Generation (25 points)

**Check**:
- [ ] Follows requirements structure exactly
- [ ] No placeholders left
- [ ] IDs follow format from requirements
- [ ] Parent artifacts referenced correctly
- [ ] FDL used correctly (if applicable)

### File Creation (20 points)

**Check**:
- [ ] Summary shown before creation
- [ ] User confirmation required
- [ ] Files created only after confirmation
- [ ] Auto-validation runs after creation
- [ ] Validation results shown to user

**Total**: 100/100

**Pass threshold**: ≥95/100

---

## Examples

**Valid execution sequence**:
```
1. Read workflow file
2. Check prerequisites (Adapter COMPLETE, BUSINESS.md ≥90)
3. Prerequisites pass
4. Read requirements/overall-design-structure.md
5. Read BUSINESS.md (parent)
6. Read adapter domain model spec

7. Ask Q1: Architecture style?
   Propose: "Layered architecture"
   Reasoning: "Based on BUSINESS.md capabilities"
   User: Approve

8. Ask Q2: Key components?
   Propose: "API Layer, Business Logic, Data Access"
   Reasoning: "Follows layered architecture"
   User: Approve

9. Generate DESIGN.md content
   - Section A: Architecture Overview
   - Section B: Requirements & Principles
   - Section C: Technical Architecture
   - Section D: Additional Context
   - No placeholders
   - All IDs formatted correctly

10. Show summary to user
11. User confirms
12. Create file at architecture/DESIGN.md
13. Run design-validate workflow
14. Validation passes (92/100)
15. Suggest features workflow
```

**Invalid execution**:
```
1. Skip prerequisites check ❌
2. Ask all questions at once ❌
3. No proposals for answers ❌
4. Generate content with [TODO] placeholders ❌
5. Create file without user confirmation ❌
6. Skip validation ❌
```

---

## References

**This file is referenced by**:
- ALWAYS open and follow WHEN executing operation workflows

**References**:
- `workflow-execution.md` - General execution instructions
- `core-workflow-operations.md` - Operation workflow structure requirements
- `FDL.md` - FDL syntax for behavioral sections
