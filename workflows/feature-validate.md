---
description: Validate feature design document
---

# Validate Feature Design

**Type**: Validation  
**Role**: Solution Architect, Architect (control)  
**Artifact**: Validation report (output to chat)

---

## ⚠️ PRE-FLIGHT CHECKLIST (ALWAYS Complete Before Proceeding)

**Agent ALWAYS verifies before starting this workflow**:

**Navigation Rules Compliance**:
- [ ] ✅ Open and follow `../requirements/execution-protocol.md` (MANDATORY BASE)
- [ ] ✅ Open and follow `../requirements/workflow-execution.md` (General execution)
- [ ] ✅ Open and follow `../requirements/workflow-execution-validations.md` (Validation specifics)

**Workflow-Specific Requirements**:
- [ ] ✅ Open and follow `../requirements/feature-design-structure.md` (This workflow's requirements)
- [ ] ✅ Check adapter initialization (FDD-Adapter/AGENTS.md exists)
- [ ] ✅ Validate all prerequisites from Prerequisites section below

**Self-Check**:
- [ ] ✅ I have read ALL files listed above
- [ ] ✅ I understand "Maximum Attention to Detail" requirement
- [ ] ✅ I am ready to check EVERY validation criterion individually
- [ ] ✅ I will validate FDL syntax and completeness
- [ ] ✅ I will run grep searches for systematic verification
- [ ] ✅ I will complete self-test before reporting results

**⚠️ If ANY checkbox is unchecked → STOP and read missing files first**

---

## Requirements

**ALWAYS open and follow**: `../requirements/feature-design-structure.md`

Extract:
- Required sections structure
- FDL validation requirements
- Validation criteria (100 points breakdown)
- Pass threshold (100/100 + 100% completeness)

---

## Prerequisites

**MUST validate**:
- [ ] Feature DESIGN.md exists - validate: Check file at `architecture/features/feature-{slug}/DESIGN.md`
- [ ] DESIGN.md exists and validated
- [ ] FEATURES.md exists and validated

**If missing**: Run prerequisite workflows

---

## Steps

### 1. Read Dependencies

Open:
- `architecture/DESIGN.md` - Extract all types, requirements
- `architecture/features/FEATURES.md` - Extract feature requirements

### 2. Execute Validation

Follow validation criteria from `feature-design-structure.md`:
- Structure (20 pts)
- Completeness (30 pts)
- FDL Correctness (25 pts)
- Non-Contradiction (25 pts)

Calculate total score

### 3. Check Completeness

- No placeholders
- All sections present
- 100% completeness required

### 4. Output Results to Chat

**Format**:
```markdown
## Validation: Feature DESIGN.md ({feature-slug})

**Score**: {X}/100  
**Completeness**: {X}%  
**Status**: PASS | FAIL  
**Threshold**: 100/100 + 100%

---

### Findings

**Structure** ({X}/20):
✅ | ❌ {item}

**Completeness** ({X}/30):
✅ | ❌ {item}

**FDL Correctness** ({X}/25):
✅ | ❌ {item}

**Non-Contradiction** ({X}/25):
✅ | ❌ {item}

---

### Recommendations

**Critical** (must fix):
1. {Fix}

```

---

## Validation

Self-validating workflow

---

## Next Steps

**If PASS**: `feature-changes` workflow (create implementation plan)

**If FAIL**: Fix feature DESIGN.md issues, re-run `feature-validate`
