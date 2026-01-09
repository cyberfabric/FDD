---
description: Validate FDD adapter structure
---

# Validate FDD Adapter

**Type**: Validation  
**Role**: Project Manager, Architect  
**Artifact**: Validation report (output to chat)

---

## ⚠️ PRE-FLIGHT CHECKLIST (ALWAYS Complete Before Proceeding)

**Agent ALWAYS verifies before starting this workflow**:

**Navigation Rules Compliance**:
- [ ] ✅ Open and follow `../requirements/execution-protocol.md` (MANDATORY BASE)
- [ ] ✅ Open and follow `../requirements/workflow-execution.md` (General execution)
- [ ] ✅ Open and follow `../requirements/workflow-execution-validations.md` (Validation specifics)

**Workflow-Specific Requirements**:
- [ ] ✅ Open and follow `../requirements/adapter-structure.md` (This workflow's requirements)
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

**ALWAYS open and follow**: `../requirements/adapter-structure.md`

Extract:
- Two-phase validation (Bootstrap vs Evolved)
- Phase 1: Bootstrap validation criteria (100/100 if Extends)
- Phase 2: Evolved validation criteria (≥80/100)
- Spec file requirements and sources
- Traceability requirements

---

## Prerequisites

**Prerequisites**:
- [ ] Adapter exists - validate: Check {adapter-directory}/FDD-Adapter/AGENTS.md exists

**If adapter missing**: Suggest `adapter-bootstrap` workflow

---

## Steps

### 1. Locate Adapter

Search common locations:
- `guidelines/FDD-Adapter/AGENTS.md`
- `spec/FDD-Adapter/AGENTS.md`
- `docs/FDD-Adapter/AGENTS.md`

If not found: STOP, report missing

Store location as: `ADAPTER_DIR`

### 2. Determine Validation Phase

Check adapter state:

```yaml
Read: {ADAPTER_DIR}/FDD-Adapter/AGENTS.md

Check for specs directory:
  {ADAPTER_DIR}/FDD-Adapter/specs/

IF specs directory NOT exists OR empty:
  → Phase 1: Bootstrap Validation
ELSE:
  → Phase 2: Evolved Adapter Validation
```

### 3. Execute Phase-Specific Validation

#### Phase 1: Bootstrap Validation (Minimal)

**Check**:
1. File exists: `{ADAPTER_DIR}/FDD-Adapter/AGENTS.md` (required)
2. Contains project name heading (required)
3. Contains `**Extends**: {path}/FDD/AGENTS.md` (required)

**Scoring**:
```yaml
All 3 checks pass: 100/100 ✅
Any check fails: 0/100 ❌
```

**Pass threshold**: 100/100

#### Phase 2: Evolved Adapter Validation

**Scoring breakdown** (100 points total):

1. **AGENTS.md structure** (10 pts):
   - Extension declaration present and valid (5 pts)
   - Version and Last Updated fields present (3 pts)
   - Tech Stack summary present (2 pts)

2. **MUST rules consistency** (10 pts):
   - Every spec file has MUST rule (5 pts)
   - No orphaned MUST rules (specs without files) (5 pts)

3. **tech-stack.md** (15 pts):
   - Languages with versions (5 pts)
   - Frameworks with versions (5 pts)
   - Source references (ADR/discovery) (5 pts)

4. **domain-model.md** (15 pts):
   - Format specified (5 pts)
   - Location specified (3 pts)
   - Examples provided (4 pts)
   - Source reference (3 pts)

5. **api-contracts.md** (15 pts):
   - Format specified (5 pts)
   - Endpoint patterns (5 pts)
   - Source reference (5 pts)

6. **patterns.md** (10 pts):
   - At least 1 pattern (5 pts)
   - Pattern has implementation example (3 pts)
   - Source reference (2 pts)

7. **conventions.md** (10 pts):
   - File naming convention (3 pts)
   - Code style rules (4 pts)
   - Project structure (3 pts)

8. **build-deploy.md** (10 pts):
   - Build/test commands specified (10 pts)

9. **Traceability** (10 pts):
   - All specs have valid source references (10 pts)

10. **Quality** (5 pts):
    - No placeholders (TODO, TBD) (3 pts)
    - Commands are cross-platform (2 pts)

**Pass threshold**: ≥80/100

### 4. Output Results to Chat

#### Phase 1 Output Format:
```markdown
## Validation: FDD Adapter (Bootstrap)

**Location**: `{ADAPTER_DIR}`  
**Phase**: Bootstrap (Minimal)  
**Score**: {100 or 0}/100  
**Status**: PASS | FAIL  
**Threshold**: 100/100

---

### Checks

✅ | ❌ AGENTS.md exists
✅ | ❌ Project name heading present
✅ | ❌ Extends declaration present

---

### Note

Minimal adapter validated. No specs required yet.
Specs will be added through:
  - Design workflow triggers
  - adapter-auto (project scanning)
  - adapter-manual (manual updates)

---

### Next Steps

**If PASS**: Continue with FDD workflows (business-context, design)
**If FAIL**: Fix AGENTS.md structure
```

#### Phase 2 Output Format:
```markdown
## Validation: FDD Adapter (Evolved)

**Location**: `{ADAPTER_DIR}`  
**Phase**: Evolved (With Specs)  
**Score**: {X}/100  
**Status**: PASS | FAIL  
**Threshold**: ≥80/100

---

### Findings

**AGENTS.md Structure** ({X}/10):
✅ | ❌ Extension declaration
✅ | ❌ Version and Last Updated
✅ | ❌ Tech Stack summary

**MUST Rules Consistency** ({X}/10):
✅ | ❌ All specs have MUST rules
✅ | ❌ No orphaned MUST rules

**Spec Files** ({X}/65):
✅ | ❌ tech-stack.md ({X}/15)
✅ | ❌ domain-model.md ({X}/15)
✅ | ❌ api-contracts.md ({X}/15)
✅ | ❌ patterns.md ({X}/10)
✅ | ❌ conventions.md ({X}/10)

**Traceability** ({X}/10):
✅ | ❌ All specs have source references

**Quality** ({X}/5):
✅ | ❌ No placeholders
✅ | ❌ Cross-platform commands

---

### Recommendations

**Critical** (blocking issues):
1. {Fix}

**High Priority**:
1. {Fix}

**Medium Priority**:
1. {Improvement}

---

### Next Steps

**If PASS**: Continue with FDD workflows
**If FAIL**: Fix issues, re-run adapter-validate
```

---

## Validation

Self-validating workflow

---

## Integration

**Called by**:
- `adapter-bootstrap` - After creating minimal AGENTS.md
- `adapter-auto` - After generating specs
- `adapter-manual` - After manual updates
- User explicitly - `adapter-validate` command

**Output**: Always to chat only (no files)

---

## Next Steps

**If PASS (Phase 1 - Bootstrap)**:
- Continue with FDD workflows
- Adapter will evolve through design/triggers

**If PASS (Phase 2 - Evolved)**:
- Adapter fully validated
- Continue with development workflows

**If FAIL**:
- Fix reported issues
- Re-run `adapter-validate`
