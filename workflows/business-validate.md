---
description: Validate business context document
---

# Validate Business Context

**Type**: Validation  
**Role**: Product Manager, Business Analyst  
**Artifact**: Validation report (output to chat)

---

## ⚠️ PRE-FLIGHT CHECKLIST (ALWAYS Complete Before Proceeding)

**Agent ALWAYS verifies before starting this workflow**:

**Navigation Rules Compliance**:
- [ ] ✅ Open and follow `../requirements/execution-protocol.md` (MANDATORY BASE)
- [ ] ✅ Open and follow `../requirements/workflow-execution.md` (General execution)
- [ ] ✅ Open and follow `../requirements/workflow-execution-validations.md` (Validation specifics)

**Workflow-Specific Requirements**:
- [ ] ✅ Open and follow `../requirements/business-context-structure.md` (This workflow's requirements)
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

**ALWAYS open and follow**: `../requirements/business-context-structure.md`

Extract:
- Required sections structure
- ID format requirements
- Validation criteria (100 points breakdown)
- Pass threshold (≥90/100)

---

## Prerequisites

**MUST validate**:
- [ ] BUSINESS.md exists - validate: Check file at `architecture/BUSINESS.md`

**If missing**: Suggest `business-context` workflow

---

## Steps

### 1. Execute Detailed Validation

**⚠️ CRITICAL**: ALWAYS open and follow `../requirements/workflow-execution-validations.md` for detailed validation requirements

**⚠️ ALWAYS** perform validation with **MAXIMUM ATTENTION TO DETAIL**

Follow validation criteria from `business-context-structure.md`:

#### Structure Validation (25 pts)
**ALWAYS verify EACH item**:
- [ ] Section A: VISION present with exact heading
- [ ] Section B: Actors present with exact heading
- [ ] Section C: Capabilities present with exact heading
- [ ] Section D: Use Cases (optional) - if present, verify exact heading
- [ ] Section E: Additional Context (optional) - if present, verify exact heading
- [ ] Section numbering follows A, B, C, D, E format
- [ ] Section order is correct (A → B → C → [D] → [E])
- [ ] NO Section D named "Additional Context" (MUST be "Use Cases" or absent)
- [ ] Headers use ## for sections, #### for actors/capabilities
- [ ] No prohibited sections present

#### Completeness Validation (30 pts)
**ALWAYS check EVERY line**:
- [ ] Section A contains: Purpose, Target Users, Key Problems Solved, Success Criteria
- [ ] Success criteria are measurable (specific numbers/percentages)
- [ ] At least 2 paragraphs in Section A
- [ ] At least 1 actor defined in Section B
- [ ] Each actor has: #### heading, **ID**: line, **Role**: line
- [ ] Actors grouped by Human Actors and System Actors
- [ ] At least 1 capability defined in Section C
- [ ] Each capability has: #### heading, **ID**: line, feature list, **Actors**: line
- [ ] NO placeholders (TODO, TBD, [Description], etc.)
- [ ] NO empty sections or sections with only HTML comments
- [ ] All content is substantive, not placeholder text

#### ID Formats Validation (25 pts)
**ALWAYS verify EACH ID individually**:
- [ ] ALL actor IDs follow format: `fdd-{project}-actor-{name}` in kebab-case
- [ ] ALL capability IDs follow format: `fdd-{project}-capability-{name}` in kebab-case
- [ ] If Section D present: ALL use case IDs follow format: `fdd-{project}-usecase-{name}`
- [ ] ALL IDs are wrapped in backticks
- [ ] ALL IDs appear immediately after heading with format: `**ID**: \`fdd-...\``
- [ ] ALL IDs are unique (no duplicates across entire document)
- [ ] Project name is consistent across all IDs

#### Consistency Validation (20 pts)
**ALWAYS verify EVERY reference**:
- [ ] Build index of ALL actor IDs from Section B
- [ ] For EACH capability in Section C:
  - [ ] Verify **Actors**: line exists
  - [ ] Verify at least 1 actor ID listed
  - [ ] Verify EACH actor ID in backticks
  - [ ] Verify EACH actor ID exists in Section B index
- [ ] If Section D present, verify EACH **Actor**: line references valid actor IDs
- [ ] Count and report: X/Y actor references validated
- [ ] NO invalid or non-existent actor references

Calculate total score

### 2. Output Detailed Results to Chat

**Format**:
```markdown
## Validation: BUSINESS.md ({module-name})

**Score**: {X}/100  
**Status**: PASS | FAIL  
**Threshold**: ≥90/100

---

### Findings

**Structure** ({X}/25):
✅ Section A: VISION present and correctly named
✅ | ❌ Section B: Actors present and correctly named
✅ | ❌ Section C: Capabilities present and correctly named
✅ | ❌ Section D: Use Cases (optional) - check if present and correctly named
✅ | ❌ Section E: Additional Context (optional) - check if present and correctly named
✅ | ❌ Section numbering follows A, B, C, D, E
✅ | ❌ Section order correct
✅ | ❌ Headers formatted correctly
❌ CRITICAL: Section D incorrectly named "Additional Context" (should be "Use Cases" or absent)

**Completeness** ({X}/30):
✅ | ❌ Section A contains all required components
✅ | ❌ Success criteria measurable ({count} criteria)
✅ | ❌ {count} actors defined
✅ | ❌ {count} capabilities defined
✅ | ❌ No placeholders found
✅ | ❌ All sections have substantive content

**ID Formats** ({X}/25):
✅ | ❌ All {count} actor IDs follow format `fdd-{project}-actor-{name}`
✅ | ❌ All {count} capability IDs follow format `fdd-{project}-capability-{name}`
✅ | ❌ All IDs unique (checked {total} IDs)
✅ | ❌ All IDs wrapped in backticks
✅ | ❌ All IDs appear immediately after headings

**Consistency** ({X}/20):
✅ | ❌ All capability actor references validated (checked {count} references)
✅ | ❌ All referenced actor IDs exist in Section B
✅ | ❌ All actor IDs in backticks
✅ | ❌ No orphaned references

---

### Recommendations

**High Priority** (must fix to pass):
1. {Specific fix with file location and expected vs actual}
2. {Another specific fix}

---

### Next Steps

{If PASS}: ✅ Validation passed! Proceed to `design` workflow

{If FAIL}: ❌ Validation failed. Fix the {count} issues listed above, then re-run `business-validate`
```

---

## Validation

Self-validating workflow

---

## Next Steps

**If PASS**: `design` workflow

**If FAIL**: Fix BUSINESS.md, re-validate
