# FDD Validation Workflow Execution

**Version**: 1.2  
**Purpose**: Define execution specifics for validation workflows  
**Scope**: All validation workflows (validate structure/completeness)

---

## ⚠️ CRITICAL: Maximum Attention to Detail Required ⚠️

**MUST** perform validation with **MAXIMUM ATTENTION TO DETAIL**:

- ✅ **MUST** check **EVERY SINGLE** validation criterion from requirements file
- ✅ **MUST** verify **EACH ITEM** individually, not in groups
- ✅ **MUST** read **COMPLETE** artifact from start to end
- ✅ **MUST** validate **EVERY** ID format, **EVERY** reference, **EVERY** section
- ✅ **MUST** check for **ALL** placeholders, **ALL** empty sections, **ALL** missing content
- ✅ **MUST** cross-reference **EVERY** actor/capability/requirement ID
- ✅ **MUST** report **EVERY** issue found, no matter how small

**MUST NOT** perform superficial validation:

- ❌ **DO NOT** skip any validation checks
- ❌ **DO NOT** assume sections are correct without verifying
- ❌ **DO NOT** group checks together without individual verification
- ❌ **DO NOT** skip reading any part of the artifact
- ❌ **DO NOT** give benefit of doubt - verify everything

**One missed issue = INVALID validation**

**Model suitability is a hard gate**:
- ✅ **MUST** follow `execution-protocol.md` Phase 2, Step 11 (Model Suitability Verification)
- ✅ **MUST** stop if model identity/class is not proven (no guessing)
- ✅ **MUST NOT** proceed with validation/checking tasks until user confirms the exact model (or class)

---

## Overview

**⚠️ ALWAYS open and follow FIRST**: `execution-protocol.md` - Mandatory protocol including self-test

**Validation workflows** - Fully automated procedures to validate artifacts

**This file defines**: Specific execution instructions for validation workflows

**Read after**: `workflow-execution.md` (general instructions)

**Applies when**: Workflow has `**Type**: Validation`

---

## Execution Sequence

### 1. File Existence Check

**Execute**:
1. Check target file exists at path specified in workflow
2. Check file is not empty
3. Check file is readable

**If fails**:
- STOP validation
- Report file not found or unreadable
- Suggest operation workflow to create file
- Do NOT proceed with validation

### 2. Requirements File Reading

**Read**:
1. Open requirements/{artifact}-structure.md
2. Extract validation criteria sections
3. Extract scoring breakdown
4. Extract pass threshold
5. Extract EVERY checklist item per category
6. Extract EVERY validation rule specified

**MUST**:
- Use requirements file as source of truth
- Never invent validation criteria
- Follow scoring exactly as specified
- Use terminology from requirements
- Read **COMPLETE** validation criteria section
- Extract **EVERY SINGLE** validation item
- Check **EACH** criterion individually

**MUST NOT**:
- Make up additional criteria
- Skip criteria from requirements
- Change scoring weights
- Use different terminology
- Skip any validation items
- Group checks without individual verification

### 3. Parent Artifacts Reading

**If workflow specifies parent artifacts**:
1. Read each parent artifact
2. Extract relevant IDs, concepts, types
3. Store for consistency checking
4. Store for coverage validation

**Use for**:
- Non-contradiction validation
- Coverage validation
- Cross-reference validation

### 3.5. Adapter Specs Validation (MANDATORY)

**⚠️ ALWAYS open and follow ADAPTER SPECS**:

**Mandatory reading**:
1. ✅ **ALWAYS** open and follow `{adapter-directory}/FDD-Adapter/AGENTS.md`
2. ✅ **ALWAYS** open and follow ALL specs listed as MANDATORY in adapter's AGENTS.md
3. ✅ **ALWAYS** open and follow ALL specs relevant to artifact being validated (as specified by adapter)

**Adapter defines validation scope**:
- Adapter's AGENTS.md specifies which specs are MANDATORY vs optional
- Adapter's AGENTS.md specifies WHEN to read each spec (canonical: "WHEN executing workflows: ...")
- Follow adapter's navigation rules exactly as written

**Generic validation checks** (adapter defines specifics):
1. ✅ All file paths follow adapter's project structure conventions
2. ✅ All module/component structures follow adapter's architecture patterns
3. ✅ All API specifications follow adapter's API contract conventions
4. ✅ All implementation patterns follow adapter's best practices
5. ✅ All domain/data models follow adapter's domain modeling conventions
6. ✅ All naming conventions follow adapter's coding standards
7. ✅ All test structures follow adapter's testing guidelines
8. ✅ All technical specifications match adapter's technology stack requirements

**ALWAYS verify**:
- Read EVERY spec file listed in adapter's AGENTS.md for this artifact type
- Check artifact content against EVERY rule defined in adapter specs
- Verify conformance with adapter's architecture patterns
- Check that no adapter conventions are violated
- Validate all referenced files/paths exist per adapter structure

**Score**: 10 points (deducted from other categories if violations found)

**Report**:
- Each file path not following adapter's project structure (cite spec file)
- Each pattern violation with expected pattern from adapter spec
- Each convention violation with reference to adapter spec section
- Each missing adapter spec reading
- Spec file name and section for each violation

**CRITICAL**: This step is MANDATORY for ALL validation workflows. Skipping adapter specs validation = INVALID validation.

### 4. Structure Validation

**⚠️ ALWAYS verify EACH item individually**:

**Check against requirements**:
1. ✅ Section A present and correctly named
2. ✅ Section B present and correctly named
3. ✅ Section C present and correctly named
4. ✅ Section D present (if required) and correctly named
5. ✅ Section E present (if used) and correctly named
6. ✅ Section numbering follows A, B, C, D, E format
7. ✅ Section order is exactly as specified in requirements
8. ✅ Required subsections present in each section
9. ✅ Headers formatted correctly (## for sections, #### for items)
10. ✅ No extra sections beyond what's allowed
11. ✅ No prohibited sections present

**ALWAYS check**:
- Read the ENTIRE artifact from line 1 to end
- Verify EACH section heading matches requirements EXACTLY
- Check section names character-by-character (e.g., "Use Cases" vs "Additional Context")
- Verify subsection structure in EACH section
- Check that Section D is "Use Cases" (optional) NOT "Additional Context"
- Check that Section E is "Additional Context" (optional) if present

**Score**: Points specified in requirements (typically 20-25)

**Report**:
- Each missing section with specific name
- Each incorrect section name (expected vs actual)
- Each incorrect numbering (expected vs actual)
- Each wrong order
- Each missing subsection
- Each formatting issue

### 5. Completeness Validation

**⚠️ ALWAYS check EVERY line for issues**:

**Check**:
1. ✅ No placeholder markers: TODO, TBD, [Description], [Fill in], etc.
2. ✅ No empty sections or sections with only comments
3. ✅ No HTML comments without real content
4. ✅ All IDs follow exact format from requirements (verify EACH ID)
5. ✅ All IDs are unique (check for duplicates across entire document)
6. ✅ All required content present per section (check EACH section)
7. ✅ All required fields present (Purpose, Role, ID, etc.)
8. ✅ All bulleted lists have actual content, not placeholders
9. ✅ All tables/structures are complete
10. ✅ All cross-references point to valid targets

**ALWAYS verify**:
- Read EVERY line of the artifact
- Check EVERY ID individually against format requirements
- Search for ALL common placeholder patterns
- Verify EACH section has substantive content
- Check that content is complete, not just present

**Score**: Points specified in requirements (typically 25-30)

**Report**:
- Each placeholder found with line location
- Each empty section with section name
- Each invalid ID format with expected format
- Each duplicate ID with both locations
- Each missing content item with section reference

### 6. Non-Contradiction Validation

**Check against parent artifacts**:
1. No contradictions with parent requirements
2. All parent concepts referenced correctly
3. No redefinition of parent types/entities
4. References use valid IDs from parent
5. No conflicting statements

**Check against adapter specs**:
6. No violations of adapter's architecture patterns
7. No violations of adapter's module/component structure
8. No violations of adapter's API integration patterns
9. No violations of adapter's domain model conventions
10. No violations of adapter's API contract standards
11. No violations of adapter's naming and coding conventions

**Score**: Points specified in requirements (typically 20-30)

**Report**:
- Each contradiction found
- Each incorrect reference
- Each redefined type
- Each invalid ID reference
- Each adapter spec violation with spec file reference

### 7. Coverage Validation

**⚠️ ALWAYS verify EVERY reference and requirement**:

**Check**:
1. ✅ All parent requirements addressed (check EACH requirement individually)
2. ✅ All referenced IDs exist in parent artifacts (verify EACH reference)
3. ✅ All actors from parent covered (check EACH actor)
4. ✅ All capabilities from parent covered (check EACH capability)
5. ✅ All requirements from parent covered (check EACH requirement)
6. ✅ No orphaned references (verify EVERY ID reference)
7. ✅ All **Actors**: lines reference valid actors
8. ✅ All capability references point to valid capabilities
9. ✅ All use case references point to valid use cases

**ALWAYS verify**:
- Build complete index of ALL IDs in parent artifacts
- Check EVERY single reference in current artifact against index
- Verify EVERY actor ID in **Actors**: lines exists in parent
- Check EVERY capability reference in flows/descriptions
- Count coverage: X of Y requirements covered

**Score**: Points specified in requirements (typically 20-25)

**Report**:
- Each missing requirement coverage with requirement ID
- Each non-existent ID reference with location
- Each uncovered parent concept with details
- Coverage statistics (e.g., "8/10 actors covered, missing: X, Y")

### 8. Scoring and Status

**Calculate**:
1. Sum all category scores
2. Total out of 100
3. Compare to threshold from requirements
4. Determine PASS/FAIL

**Status**:
- PASS: Score ≥ threshold
- FAIL: Score < threshold

### 9. Agent Self-Test (MANDATORY Before Reporting)

**⚠️ Complete BEFORE outputting validation results**

**Agent ALWAYS answers YES to ALL questions**:

#### Execution Completeness Check
1. ⚠️ **Did I read execution-protocol.md before starting?**
   - [ ] YES - Read and followed all 4 phases
   - [ ] NO - Validation is INVALID, must restart

2. ⚠️ **Did I verify model suitability with evidence (execution-protocol Phase 2, Step 11)?**
    - [ ] YES - Model identity source proven; class mapped; suitability checked
    - [ ] NO - Validation is INVALID, must restart

3. ⚠️ **Did I read the ENTIRE artifact line by line?**
   - [ ] YES - Read from line 1 to end
   - [ ] NO - Validation is INVALID, must restart

4. ⚠️ **Did I check EVERY validation criterion from requirements?**
   - [ ] YES - Verified each criterion individually
   - [ ] NO - Validation is INVALID, must restart

5. ⚠️ **Did I verify EACH ID format individually?**
   - [ ] YES - Checked each ID against format requirements
   - [ ] NO - Validation is INVALID, must restart

#### Systematic Verification Check
6. ⚠️ **Did I run grep searches for common issues?**
   - [ ] YES - Ran: TODO, TBD, `**ID**:`, placeholders
   - [ ] NO - Validation is INVALID, must restart

7. ⚠️ **Did I check ADR headers for ID fields? (if validating ADR.md)**
   - [ ] YES - Verified `**ID**:` after EACH `## ADR-` heading
   - [ ] NO - Validation is INVALID, must restart

8. ⚠️ **Did I check requirement traceability? (if validating DESIGN.md)**
   - [ ] YES - Verified `**Capabilities**:`, `**Actors**:` fields
   - [ ] NO - Validation is INVALID, must restart

9. ⚠️ **Did I cross-reference EVERY actor/capability/requirement?**
   - [ ] YES - Built index, verified each reference
   - [ ] NO - Validation is INVALID, must restart

#### Score Verification Check
10. ⚠️ **Is my score calculation arithmetically correct?**
   - [ ] YES - Verified addition
   - [ ] NO - Must recalculate, validation may be invalid

11. ⚠️ **Did I compare score to correct threshold from requirements?**
    - [ ] YES - Used exact threshold from requirements file
    - [ ] NO - ALWAYS check threshold before proceeding

**If ANY answer 1-9 is NO → Validation is INVALID, must restart with execution-protocol.md**

**If answers 10-11 are NO → Fix calculation, may need to restart**

---

### 10. Output to Chat

**Format** (directly in chat, NO files):
```markdown
## Validation: {Artifact Name}

**Score**: {X}/100  
**Status**: PASS | FAIL  
**Threshold**: ≥{threshold}/100

---

### Findings

**Structure** ({X}/{points}):
✅ {passed item}
❌ {failed item}
❌ {failed item}

**Completeness** ({X}/{points}):
✅ {passed item}
❌ {failed item}

**Non-Contradiction** ({X}/{points}):
✅ {passed item}
❌ {failed item}

**Coverage** ({X}/{points}):
✅ {passed item}
❌ {failed item}

---

### Recommendations

**High Priority** (critical issues):
1. {Fix description}
2. {Fix description}

**Medium Priority** (important issues):
1. {Fix description}

**Low Priority** (nice-to-have):
1. {Fix description}

---

### Next Steps

{If PASS}:
✅ Validation passed! Proceed to `{next-workflow}`

{If FAIL}:
❌ Validation failed. Fix issues above, then re-run validation.

---

### Self-Test Confirmation

**Agent confirms**:
✅ Completed self-test (Section 9)
✅ All 11 questions answered YES
✅ Validation execution was systematic and complete
✅ Protocol compliance verified

Self-test passed: YES
```

**MUST**:
- Output to chat only (no files)
- Show complete scoring breakdown
- List all issues by category
- Prioritize recommendations
- Suggest next workflow (PASS) or fixes (FAIL)

**MUST NOT**:
- Create validation report files
- Skip showing issues
- Proceed to next workflow if FAIL
- Output incomplete information

---

## Validation Implementation

### Using Requirements File

**Pattern**:
```
1. Open requirements/{artifact}-structure.md
2. Find "## Validation Criteria" section
3. Extract each category and points
4. Extract checklist items per category
5. Execute each check exactly as specified
6. Award points per requirements (full/partial/zero)
7. Sum total score
8. Compare to threshold from requirements
```

**Example** (from business-context-structure.md):
```markdown
## Validation Criteria

### Structure (25 points)
- All required sections present
- Section numbering correct

### Completeness (30 points)
- No placeholders
- All IDs valid
```

**Implementation**:
```
Structure validation:
- Check Section A: Vision present → 12.5 pts
- Check Section B: Actors present → 12.5 pts
- Check numbering A, B, C → full credit

Completeness validation:
- Check for [TODO] markers → 10 pts
- Check all actor IDs valid → 10 pts
- Check all capability IDs valid → 10 pts
```

### Scoring Guidelines

**Full credit**: Criterion fully satisfied
**Partial credit**: Criterion partially satisfied (if requirements allow)
**Zero credit**: Criterion not satisfied

**Example**:
- "All required sections present" → Binary (all or nothing)
- "All IDs follow format" → Could be partial (90% valid = 90% credit)

**Follow requirements**: Some criteria are binary, some allow partial credit

### Cross-Validation

**When checking parent artifacts**:
1. Read parent artifact completely
2. Build index of IDs, concepts, types
3. For each reference in current artifact:
   - Check ID exists in index
   - Check reference is correct
   - Check no contradiction
4. Report each issue found

**Example**:
```
BUSINESS.md has actor: `fdd-actor-admin`
DESIGN.md references: `fdd-actor-administrator` ❌

Issue: Actor ID mismatch
Should be: `fdd-actor-admin`
```

---

## Validation Criteria

### Requirements Following (30 points)

**Check**:
- [ ] Validation criteria from requirements file used
- [ ] Scoring breakdown from requirements followed
- [ ] No invented criteria added
- [ ] Terminology matches requirements

### Automation (25 points)

**Check**:
- [ ] No user interaction
- [ ] Fully executable by agent
- [ ] Deterministic output
- [ ] Clear pass/fail logic

### Output Quality (25 points)

**Check**:
- [ ] Output to chat only (no files)
- [ ] Complete scoring shown
- [ ] All issues listed by category
- [ ] Recommendations prioritized
- [ ] Next steps clear

### Accuracy (20 points)

**Check**:
- [ ] Correct score calculation
- [ ] All issues detected
- [ ] No false positives
- [ ] Correct pass/fail status

**Total**: 100/100

**Pass threshold**: ≥95/100

---

## Examples

**Valid execution** (PASS scenario):
```
1. Read validation workflow file
2. Target: architecture/BUSINESS.md
3. Check file exists ✓
4. Read requirements/business-context-structure.md
5. Extract validation criteria

6. Structure validation:
   - Section A: Vision ✓ (12.5 pts)
   - Section B: Actors ✓ (12.5 pts)
   - Total: 25/25 pts

7. Completeness validation:
   - No placeholders ✓ (10 pts)
   - All actor IDs valid ✓ (10 pts)
   - All capability IDs valid ✓ (10 pts)
   - Total: 30/30 pts

8. Non-Contradiction validation:
   - No parent (first artifact) ✓
   - Total: 30/30 pts

9. Coverage validation:
   - All actors in capabilities ✓ (10 pts)
   - All capabilities reference actors ✓ (10 pts)
   - Total: 20/20 pts

10. Calculate: 25+30+30+20 = 105... wait, recalc: 25+30+20+20 = 95/100
11. Threshold: ≥90/100
12. Status: PASS ✓

13. Output to chat:
## Validation: BUSINESS.md
**Score**: 95/100
**Status**: PASS
...
**Next Steps**: Proceed to `design` workflow

14. Workflow complete
```

**Valid execution** (FAIL scenario):
```
1. Read validation workflow file
2. Target: architecture/DESIGN.md
3. Check file exists ✓
4. Read requirements/overall-design-structure.md
5. Read parent: BUSINESS.md

6. Structure validation:
   - Section A missing ❌ (0 pts)
   - Section B present ✓ (10 pts)
   - Total: 10/20 pts

7. Completeness validation:
   - Found [TODO] in Section B ❌ (0 pts)
   - Found placeholder text ❌ (0 pts)
   - Requirements incomplete ❌ (0 pts)
   - Total: 0/30 pts

8. Non-Contradiction validation:
   - References actor `fdd-actor-xyz` not in BUSINESS.md ❌
   - Total: 15/25 pts

9. Coverage validation:
   - Missing capability CAP-001 ❌
   - Total: 15/25 pts

10. Calculate: 10+0+15+15 = 40/100
11. Threshold: ≥90/100
12. Status: FAIL ❌

13. Output to chat:
## Validation: DESIGN.md
**Score**: 40/100
**Status**: FAIL

### Findings
**Structure** (10/20):
❌ Section A: Architecture Overview missing
✓ Section B: Requirements present

**Completeness** (0/30):
❌ Found [TODO] marker in Section B
❌ Found placeholder text "[Description]"
❌ Requirements section incomplete

**Non-Contradiction** (15/25):
❌ References non-existent actor `fdd-actor-xyz`

**Coverage** (15/25):
❌ Missing coverage for capability CAP-001

### Recommendations
**High Priority**:
1. Add Section A: Architecture Overview
2. Remove all [TODO] markers
3. Fix actor reference to existing ID

**Medium Priority**:
1. Complete requirements section
2. Add coverage for CAP-001

### Next Steps
❌ Fix issues above, then re-run `design-validate`

14. Workflow complete
```

**Invalid execution**:
```
1. Skip file existence check ❌
2. Invent validation criteria not in requirements ❌
3. Create VALIDATION_REPORT.md file ❌
4. Suggest next workflow despite FAIL ❌
5. Skip showing detailed issues ❌
```

---

## References

**This file is referenced by**:
- ALWAYS open and follow WHEN executing validation workflows

**References**:
- `workflow-execution.md` - General execution instructions
- `core-workflow-validation.md` - Validation workflow structure requirements
- `core-requirements.md` - Requirements file validation format
