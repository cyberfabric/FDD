# FDD Workflow Execution Instructions

**Version**: 1.0  
**Purpose**: Define how agents execute FDD workflows  
**Scope**: All workflow execution (operation and validation)

---

## Overview

**⚠️ ALWAYS open and follow FIRST**: `execution-protocol.md` - Mandatory protocol for ALL workflows

**Workflow execution** - Instructions for agents to execute workflows correctly

**This file defines**: General execution requirements for ALL workflow types

**Read before**: Executing any workflow file from `FDD/workflows/*.md`

**Workflow types**:
- Operation workflows (create/update documents)
- Validation workflows (validate structure/completeness)

ALWAYS open and follow `workflow-execution-operations.md` WHEN executing operation workflows

ALWAYS open and follow `workflow-execution-validations.md` WHEN executing validation workflows

---

## General Execution Rules

### Before Starting ANY Workflow

**MUST**:
1. **Follow Execution Protocol** - MANDATORY
   - Open and follow `requirements/execution-protocol.md` FIRST
   - Complete all protocol phases (1-4)
   - Answer all readiness check questions
   - Verify protocol compliance before proceeding
2. **Check Adapter Initialization** - MANDATORY
   - Search for `{adapter-directory}/FDD-Adapter/AGENTS.md`
   - If NOT found: STOP, propose bootstrap, run `adapter` workflow
   - If found: Continue
3. Read workflow file completely
3. Identify workflow type (Operation or Validation)
4. Read type-specific execution instructions
5. Read `adapter-triggers.md` for trigger rules
6. Check all prerequisites
7. Validate prerequisites before proceeding

**MUST NOT**:
- Skip adapter initialization check
- Skip prerequisites validation
- Proceed if prerequisites fail
- Create files before user confirmation (operation workflows)
- Create report files (validation workflows)

### Prerequisites Validation

**Check**:
1. Adapter initialization (mandatory for ALL workflows)
2. Required files exist at specified paths
3. Required files are validated (meet score threshold)
4. Parent artifacts are valid

**If ANY prerequisite fails**:
1. STOP workflow immediately
2. Report which prerequisite failed
3. Suggest prerequisite workflow to run
4. Wait for user to fix prerequisites
5. Do NOT proceed with current workflow

**Adapter Prerequisite**:
- Minimal adapter (just Extends) is sufficient for most workflows
- Evolved adapter (with specs) preferred but not required
- If adapter missing: Run `adapter` workflow Mode 1 (Bootstrap) first

### Reading Specifications

**Before generating/validating content**:
1. Read requirements file for target artifact
2. Read parent artifact specifications if applicable
3. Use requirements as source of truth (not workflow description)
4. Never invent validation criteria

### Workflow Types

**Operation workflow** - Has user interaction, creates/modifies files
**Validation workflow** - Fully automated, outputs to chat only

**Type indicator**: Check workflow file for `**Type**: Operation` or `**Type**: Validation`

### Output Requirements

**Operation workflows**:
- Output to chat during interaction
- Create files only after user confirmation
- Show summary before creation
- Run validation after creation

**Validation workflows**:
- Output ONLY to chat (no report files)
- Show score, status, issues, recommendations
- Suggest next workflow
- Never create validation report files

### Adapter Trigger Monitoring

**ALWAYS open and follow**: `adapter-triggers.md`

**During workflow execution**:
1. Monitor for trigger events (file changes, validations, decisions)
2. When trigger detected: Run trigger-specific scan
3. If conditions met: Propose adapter update to user
4. If user accepts: Run `adapter` workflow (appropriate mode)
5. Continue original workflow after adapter update

**Agent responsibilities**:
- Detect triggers automatically
- Propose adapter updates with context
- Never run adapter without approval
- Never skip adapter opportunities

### Context Usage

**MUST**:
- Use current project context for proposals
- Reference existing artifacts when relevant
- Propose answers based on available information
- Show reasoning for proposals
- Monitor for adapter triggers

**MUST NOT**:
- Make up information
- Assume without context
- Skip asking when uncertain
- Proceed without user confirmation (operations)
- Skip adapter trigger proposals

### Error Handling

**If workflow fails**:
1. Stop execution
2. Show clear error message
3. Explain what went wrong
4. Suggest how to fix
5. Suggest prerequisite workflows if needed

**If validation fails**:
1. Show all issues clearly
2. Prioritize by severity
3. Suggest specific fixes
4. Allow user to fix and re-run
5. Never proceed to next workflow




---

## Validation Criteria

### Prerequisites Validation (30 points)

**Check**:
- [ ] All prerequisite files checked for existence
- [ ] All prerequisite validations executed
- [ ] Prerequisites pass before workflow proceeds
- [ ] Clear error if prerequisites fail

### Specification Reading (25 points)

**Check**:
- [ ] Requirements file read before generation/validation
- [ ] Parent artifact specs read when applicable
- [ ] Requirements used as source of truth
- [ ] No invented criteria or structure

### Execution Correctness (25 points)

**Check**:
- [ ] Workflow type identified correctly
- [ ] Type-specific instructions followed
- [ ] Output format matches requirements
- [ ] No files created prematurely (operations)
- [ ] No report files created (validations)

### Error Handling (20 points)

**Check**:
- [ ] Clear error messages on failure
- [ ] Suggests corrective actions
- [ ] Stops workflow on critical errors
- [ ] Never proceeds with invalid state

**Total**: 100/100

**Pass threshold**: ≥95/100

---

## Examples

**Valid execution** (operation workflow):
```
1. Agent reads workflow file
2. Identifies Type: Operation
3. Reads workflow-execution-operations.md
4. Checks all prerequisites
5. Prerequisites pass
6. Reads requirements/business-context-structure.md
7. Asks questions one by one
8. Proposes answers based on context
9. Generates content following requirements
10. Shows summary to user
11. Waits for confirmation
12. Creates file after confirmation
13. Runs validation workflow
14. Shows validation results
15. Suggests next workflow
```

**Valid execution** (validation workflow):
```
1. Agent reads workflow file
2. Identifies Type: Validation
3. Reads workflow-execution-validations.md
4. Checks file exists
5. Reads requirements file
6. Validates structure against requirements
7. Validates completeness
8. Validates consistency with parents
9. Validates coverage
10. Calculates score
11. Outputs to chat (no files)
12. Shows issues and recommendations
13. Suggests next workflow
```

**Invalid execution**:
```
1. Agent skips prerequisites check ❌
2. Creates file without user confirmation ❌
3. Invents validation criteria ❌
4. Creates validation report file ❌
5. Proceeds despite validation failure ❌
```

---

## References

**This file is referenced by**:
- ALWAYS open and follow this file WHEN executing any workflow

**References**:
- `workflow-execution-operations.md` - Operation workflow execution specifics
- `workflow-execution-validations.md` - Validation workflow execution specifics
- `core-workflows.md` - Workflow file structure requirements
- `core.md` - Core FDD principles
