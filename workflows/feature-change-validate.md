---
description: Validate implemented change
---

# Validate Feature Change

**Type**: Validation  
**Role**: Developer, QA  
**Artifact**: Validation report (output to chat)

---

## ⚠️ PRE-FLIGHT CHECKLIST (MUST Complete Before Proceeding)

**Agent MUST verify before starting this workflow**:

**Navigation Rules Compliance**:
- [ ] ✅ Read `../requirements/execution-protocol.md` (MANDATORY BASE)
- [ ] ✅ Read `../requirements/workflow-execution.md` (General execution)
- [ ] ✅ Read `../requirements/workflow-execution-validations.md` (Validation specifics)

**Workflow-Specific Requirements**:
- [ ] ✅ Read `../requirements/feature-changes-structure.md` (This workflow's requirements)
- [ ] ✅ Read adapter specs/testing.md (Test requirements)
- [ ] ✅ Check adapter initialization (FDD-Adapter/AGENTS.md exists)
- [ ] ✅ Validate all prerequisites from Prerequisites section below

**Self-Check**:
- [ ] ✅ I have read ALL files listed above
- [ ] ✅ I understand "Maximum Attention to Detail" requirement
- [ ] ✅ I am ready to check EVERY validation criterion individually
- [ ] ✅ I will verify tests pass and build succeeds
- [ ] ✅ I will complete self-test before reporting results

**⚠️ If ANY checkbox is unchecked → STOP and read missing files first**

---

## Requirements

**MUST read**:
- `../requirements/feature-changes-structure.md` (change requirements)
- `{adapter-directory}/FDD-Adapter/specs/testing.md` (test requirements)

Extract:
- Task validation criteria
- Test requirements from adapter
- Build requirements

---

## Prerequisites

**MUST validate**:
- [ ] Change implemented - validate: Change status IN_PROGRESS or COMPLETED in CHANGES.md
- [ ] Adapter exists - validate: Required for validation

---

## Steps

### 1. Select Change

Identify change to validate (from user or current IN_PROGRESS)

### 2. Read Change Specification

Extract:
- Requirements implemented
- Tasks and validation criteria

### 3. Execute Validation Checks

**Code Validation**:
- Build succeeds (per adapter build command)
- No compilation errors
- Linter passes (per adapter lint command)
- **Change ID tags present**: All modified/new code tagged with `@fdd-change:fdd-{project}-{feature}-change-{slug}` (full format only)
  - Use `grep -r "@fdd-change:fdd-{project}-{feature}-change-{slug}"` to verify tag presence
  - Verify tags in all files listed in CHANGES.md tasks
  - Each major function/class/module related to change MUST have tag

**Test Validation**:
- Unit tests pass (per adapter test command)
- Integration tests pass (if applicable)
- Coverage meets threshold (per adapter)

**Requirements Validation**:
- Code implements specified requirements
- No requirements missing
- No out-of-scope changes

**Task Validation**:
- All task checkboxes marked `- [x]` (not `- [ ]`)
- Task count: All tasks in change have `[x]` status
- File changes match task specifications
- Validation criteria met per task

**Change Status Validation**:
- Change status is `✅ COMPLETED` (not `⏳ NOT_STARTED` or `🔄 IN_PROGRESS`)
- Summary section updated: "Completed" count incremented
- All task groups validated (## 1. Implementation, ## 2. Testing)

Calculate score:
- Code Quality (20 pts)
- Code Tagging (10 pts)
- Test Coverage (30 pts)
- Requirements Match (25 pts)
- Task Completion (15 pts)

### 4. Output Results to Chat

**Format**:
```markdown
## Validation: Change ({change-id})

**Score**: {X}/100  
**Status**: PASS | FAIL  
**Threshold**: ≥90/100

---

### Findings

**Code Quality** ({X}/20):
✅ | ❌ Build status
✅ | ❌ Lint status

**Code Tagging** ({X}/10):
✅ | ❌ Change ID tags present: `@fdd-change:fdd-{project}-{feature}-change-{slug}` found in {X} files
✅ | ❌ All task files have corresponding tags

**Test Coverage** ({X}/30):
✅ | ❌ Tests pass: {X}/{total}
✅ | ❌ Coverage: {X}%

**Requirements Match** ({X}/25):
✅ | ❌ {requirement check}

**Task Completion** ({X}/15):
✅ | ❌ All task checkboxes marked `- [x]`: {X}/{total}
✅ | ❌ Change status is `✅ COMPLETED`
✅ | ❌ Summary counts updated correctly

---

### Recommendations

**Critical**:
1. {Fix}

```

---

## Validation

Self-validating workflow

---

## Next Steps

**If PASS**:
- If more changes remain: `feature-change-implement` (next change)
- If all changes complete: `feature-qa` (complete feature validation)

**If FAIL**: Fix code issues, re-run `feature-change-validate`
