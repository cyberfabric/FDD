---
description: Validate overall design document
---

# Validate Overall Design

**Type**: Validation  
**Role**: Architect, Product Manager (for business alignment)  
**Artifact**: Validation report (output to chat)

---

## ⚠️ PRE-FLIGHT CHECKLIST (ALWAYS Complete Before Proceeding)

**Agent ALWAYS verifies before starting this workflow**:

**Navigation Rules Compliance**:
- [ ] ✅ Open and follow `../requirements/execution-protocol.md` (MANDATORY BASE)
- [ ] ✅ Open and follow `../requirements/workflow-execution.md` (General execution)
- [ ] ✅ Open and follow `../requirements/workflow-execution-validations.md` (Validation specifics)

**Workflow-Specific Requirements**:
- [ ] ✅ Open and follow `../requirements/overall-design-structure.md` (This workflow's requirements)
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

**ALWAYS open and follow**: `../requirements/overall-design-structure.md`

Extract:
- Required sections structure
- Validation criteria (100 points breakdown)
- Pass threshold (≥90/100)

---

## Prerequisites

**MUST validate**:
- [ ] DESIGN.md exists - validate: Check file at `architecture/DESIGN.md`
- [ ] BUSINESS.md exists - validate: Check file at `architecture/BUSINESS.md`
- [ ] BUSINESS.md validated - validate: Score ≥90/100

**If missing**: Run prerequisite workflows first

---

## Steps

### 1. Read Dependencies

Open `architecture/BUSINESS.md`

Extract:
- All actor IDs
- All capability IDs
- Vision statement

### 2. Execute Validation

Follow validation criteria from `overall-design-structure.md`:
- Structure (20 pts): Sections A-D present, correct order
- Completeness (25 pts): No placeholders, all IDs valid
- Business Alignment (30 pts): No contradictions, all actors/capabilities addressed
- Technical Coherence (25 pts): Architecture consistent, NFRs appropriate

Calculate total score

### 3. Output Results to Chat

**Format**:
```markdown
## Validation: DESIGN.md

**Score**: {X}/100  
**Status**: PASS | FAIL  
**Threshold**: ≥90/100

---

### Findings

**Structure** ({X}/20):
✅ | ❌ {item}

**Completeness** ({X}/25):
✅ | ❌ {item}

**Business Alignment** ({X}/30):
✅ | ❌ {item}

**Technical Coherence** ({X}/25):
✅ | ❌ {item}

---

### Recommendations

**High Priority**:
1. {Fix}

---

### Next Steps

{If PASS}: ✅ Run `adr-validate` to validate ADRs, then proceed to `features` workflow

{If FAIL}: ❌ Fix issues, re-validate
```

### 4. Validate ADR.md (If DESIGN.md passed)

**If DESIGN.md validation score ≥90**:
- Check if `architecture/ADR.md` exists
- If exists: Run `adr-validate` workflow
- If missing: Suggest running `adr` workflow first

**Output**:
```markdown
---

## ADR Validation

{If ADR.md exists}: Running adr-validate...
{If ADR.md missing}: ⚠️ ADR.md not found. Run `adr` workflow to create Architecture Decision Records.
```

---

## Validation

Self-validating workflow

---

## Next Steps

**If DESIGN.md PASS and ADR.md PASS**: `features` workflow

**If DESIGN.md PASS but ADR.md missing**: `adr` workflow to create ADRs

**If DESIGN.md FAIL**: Fix DESIGN.md, re-validate
