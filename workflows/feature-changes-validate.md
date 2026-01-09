---
description: Validate feature implementation plan
---

# Validate Feature Implementation Plan

**Type**: Validation  
**Role**: Developer  
**Artifact**: Validation report (output to chat)

---

## ⚠️ PRE-FLIGHT CHECKLIST (ALWAYS Complete Before Proceeding)

**Agent ALWAYS verifies before starting this workflow**:

**Navigation Rules Compliance**:
- [ ] ✅ Open and follow `../requirements/execution-protocol.md` (MANDATORY BASE)
- [ ] ✅ Open and follow `../requirements/workflow-execution.md` (General execution)
- [ ] ✅ Open and follow `../requirements/workflow-execution-validations.md` (Validation specifics)

**Workflow-Specific Requirements**:
- [ ] ✅ Open and follow `../requirements/feature-changes-structure.md` (This workflow's requirements)
- [ ] ✅ Check adapter initialization (FDD-Adapter/AGENTS.md exists)
- [ ] ✅ Validate all prerequisites from Prerequisites section below

**Self-Check**:
- [ ] ✅ I have read ALL files listed above
- [ ] ✅ I understand "Maximum Attention to Detail" requirement
- [ ] ✅ I am ready to check EVERY validation criterion individually
- [ ] ✅ I will run grep searches for systematic verification
- [ ] ✅ I will complete self-test before reporting results

**⚠️ If ANY checkbox is unchecked → STOP and read missing files first**

---

## Requirements

**ALWAYS open and follow**: `../requirements/feature-changes-structure.md`

Extract:
- Required structure
- Validation criteria (100 points breakdown)
- Pass threshold (≥90/100)

---

## Prerequisites

**MUST validate**:
- [ ] CHANGES.md exists - validate: Check file at feature directory
- [ ] Feature DESIGN.md validated - validate: Score 100/100

---

## Steps

### 1. Read Feature Design

Open feature DESIGN.md

Extract all requirement IDs (Section F)

### 2. Execute Validation

Follow validation criteria from `feature-changes-structure.md`:
- Structure (25 pts)
- Coverage (35 pts): All requirements from DESIGN.md covered
- Task Quality (25 pts): Tasks executable, granular, validated
- Effort Estimation (15 pts): Reasonable estimates

Calculate total score

### 3. Output Results to Chat

**Format**:
```markdown
## Validation: CHANGES.md ({feature-slug})

**Score**: {X}/100  
**Status**: PASS | FAIL  
**Threshold**: ≥90/100

---

### Findings

**Structure** ({X}/25):
✅ | ❌ {item}

**Coverage** ({X}/35):
✅ | ❌ {item}
**Requirements covered**: {X}/{total} ({percentage}%)

**Task Quality** ({X}/25):
✅ | ❌ {item}

**Effort Estimation** ({X}/15):
✅ | ❌ {item}

---

### Recommendations

**High Priority**:
1. {Fix}

---

### Next Steps

{If PASS}: ✅ Proceed to `feature-change-implement`

{If FAIL}: ❌ Fix issues, re-validate
```

---

## Validation

Self-validating workflow

---

## Next Steps

**If all changes completed** (status `✅ COMPLETED`):
- Suggest: Archive CHANGES.md via `feature-changes` workflow (Step 7)
- Archive path: `architecture/features/feature-{slug}/archive/YYYY-MM-DD-CHANGES.md`

**If PASS**: `feature-change-implement` workflow

**If FAIL**: Fix CHANGES.md, re-validate
