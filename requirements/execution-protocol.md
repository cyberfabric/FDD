# FDD Workflow Execution Protocol

**Version**: 1.1  
**Purpose**: MANDATORY execution protocol for ALL workflows  
**Scope**: EVERY workflow execution without exceptions

---

## ⚠️ MANDATORY PRE-EXECUTION PROTOCOL ⚠️

**Before executing ANY workflow, agent ALWAYS follows this protocol**

This protocol is **NON-NEGOTIABLE** and applies to **EVERY** workflow without exception.

**One skipped step = INVALID execution = output DISCARDED**

---

## Phase 1: Protocol Initialization (MANDATORY)

### Step 1: Acknowledge Protocol

Agent ALWAYS explicitly acknowledges:
```
I am about to execute workflow: {workflow-name}
I acknowledge that I ALWAYS follow the FDD Execution Protocol.
I will NOT skip any steps.
```

### Step 2: Load Base Requirements

**ALWAYS open and follow in this order**:
1. [ ] `requirements/workflow-execution.md` - General execution rules
2. [ ] `requirements/workflow-execution-validations.md` - For validation workflows
   OR
   [ ] `requirements/workflow-execution-operations.md` - For operation workflows
3. [ ] Extract all MUST requirements from these files
4. [ ] Create mental checklist of requirements

**Verification**: Can you list 3 key requirements from workflow-execution.md?
- If NO → Go back and re-read

### Step 3: Load Workflow Requirements

**ALWAYS open and follow**:
1. [ ] `workflows/{workflow-name}.md` - Specific workflow file
2. [ ] Extract prerequisites section
3. [ ] Extract required files list
4. [ ] Note all validation criteria (for validation workflows)
5. [ ] Verify ALL prerequisites are satisfied

**If ANY prerequisite fails**:
- STOP immediately
- Report failed prerequisite
- Suggest how to fix
- Do NOT proceed

### Step 4: Load Artifact Requirements

**ALWAYS open and follow**:
1. [ ] `requirements/{artifact}-structure.md` - Structure requirements
2. [ ] Extract validation criteria (100-point breakdown)
3. [ ] Extract EVERY single validation item
4. [ ] Note pass threshold
5. [ ] Create checklist of ALL criteria

**For validation workflows**:
- Extract structure criteria
- Extract completeness criteria  
- Extract non-contradiction criteria
- Extract coverage criteria
- Note point values for each

### Step 5: Load Parent Artifacts (if applicable)

**If workflow references parent artifacts**:
1. [ ] Read each parent artifact completely
2. [ ] Extract all IDs (actors, capabilities, requirements, principles)
3. [ ] Build index for cross-reference validation
4. [ ] Note all concepts that must be covered

---

## Phase 2: Execution Readiness Check

**Agent ALWAYS answers YES to ALL questions before proceeding**:

### Knowledge Verification
1. ⚠️ **Have I read workflow-execution.md?**
   - [ ] YES - I read it completely
   - [ ] NO - ALWAYS open and follow it now, cannot proceed

2. ⚠️ **Have I read workflow-execution-{type}.md?**
   - [ ] YES - I read the type-specific file
   - [ ] NO - ALWAYS open and follow it now, cannot proceed

3. ⚠️ **Have I read the specific workflow file?**
   - [ ] YES - I read {workflow-name}.md
   - [ ] NO - ALWAYS open and follow it now, cannot proceed

4. ⚠️ **Have I read the artifact structure requirements?**
   - [ ] YES - I read {artifact}-structure.md
   - [ ] NO - ALWAYS open and follow it now, cannot proceed

### Comprehension Verification
5. ⚠️ **Do I understand "Maximum Attention to Detail" requirement?**
   - [ ] YES - I will check EVERY criterion individually
   - [ ] NO - ALWAYS re-read workflow-execution-validations.md lines 9-29

6. ⚠️ **Do I have a complete list of validation criteria?**
   - [ ] YES - I extracted EVERY criterion from requirements
   - [ ] NO - ALWAYS re-read requirements file

7. ⚠️ **Am I ready to check each item individually, not in groups?**
   - [ ] YES - I will verify each criterion separately
   - [ ] NO - ALWAYS re-read "Maximum Attention" section

### Preparation Verification
8. ⚠️ **Do I have a plan for systematic verification?**
   - [ ] YES - I will use grep, read line-by-line, check each ID
   - [ ] NO - ALWAYS create verification plan

9. ⚠️ **Do I know what tools to use for verification?**
   - [ ] YES - grep for IDs, read_file for content, line-by-line check
   - [ ] NO - ALWAYS review tool usage

10. ⚠️ **Am I prepared to report EVERY issue, no matter how small?**
    - [ ] YES - I will report all issues found
    - [ ] NO - ALWAYS adjust my mindset

### Model Suitability Verification
11. ⚠️ **Have I verified my model suitability?**
    - [ ] **Verify Model Identity Source (NO guessing allowed)**:
        - **Allowed evidence sources** (pick exactly one):
          - **System / runtime metadata** explicitly states model name or class
          - **User confirmation** explicitly states exact model name (or class) used in this run
        - **Forbidden**:
          - Guessing based on "I feel like" / style / speed
          - Assuming provider/model family (e.g. "I am Claude") without evidence
        - **If I cannot prove identity/class**:
          - STOP immediately
          - Ask user: "What exact model (name) is running here?"
          - Do NOT execute validation/checking workflows until clarified
    - [ ] **Identify My Model Class (based on the verified source above)**:
        - **Reasoning**: o1 / o3, DeepSeek-R1, Claude 4.5 Opus (Frontier reasoning)
        - **Flagship**: GPT-5.2, Gemini 3 Pro, Llama 4 Maverick 405B (High capability)
        - **Fast/Lite**: o4-mini, Gemini 3 Flash, Claude 3.5 Haiku, Llama 4 8B (Speed optimised)
    - [ ] **Validate Against Task Rule**:
        - **Checking/Validation**: MUST use **Top Frontier / Reasoning** (Strictness is key). *Speed models FORBIDDEN.*
        - **Writing/Design**: **Reasoning** preferred (for coherence), but **Flagship** allowed.
        - **Coding**: **Fast/Flagship** preferred (Speed is key). *Reasoning models often overkill.*
        - **Scanning/Analysis**: **Fast/Lite** (or Flagship) with **Large Context ≥ 128k tokens** preferred.
    - [ ] **Result**:
        - [ ] YES - My model class fits the task rule.
        - [ ] NO - ALWAYS Warn User: "⚠️ Model Mismatch: I am a [My Class] model, but this [Task Type] task requires [Required Class]."
        - [ ] UNKNOWN - ALWAYS stop and ask user to confirm model; do not proceed.

**If ANY answer is NO → STOP, fix the issue, restart readiness check**

---

## Phase 3: Execution

### During Execution Rules

**ALWAYS do**:
1. Follow checklist item by item
2. Check EVERY criterion individually (never group checks)
3. Read ENTIRE artifact from line 1 to end
4. Verify EACH ID format against requirements
5. Cross-check EVERY reference against parent artifacts
6. Use grep/search tools for systematic verification
7. Report intermediate progress
8. Execute mini self-checks after each category

**ALWAYS do NOT**:
1. Skip any validation criteria
2. Group checks together without individual verification
3. Assume sections are correct without checking
4. Give benefit of doubt - verify everything
5. Rush through validation
6. Skip systematic grep searches

---

## Phase 4: Post-Execution Validation

### Self-Test Before Reporting (MANDATORY)

**Agent ALWAYS completes self-test before outputting results**:

#### Execution Completeness
1. ⚠️ **Did I read the ENTIRE artifact line by line?**
   - [ ] YES - Read from line 1 to end
   - [ ] NO - Validation is INVALID, must re-do

2. ⚠️ **Did I check EVERY validation criterion from requirements?**
   - [ ] YES - Verified each criterion individually
   - [ ] NO - Validation is INVALID, must re-do

3. ⚠️ **Did I verify EACH ID format individually?**
   - [ ] YES - Checked each ID against format requirements
   - [ ] NO - Validation is INVALID, must re-do

4. ⚠️ **Did I cross-reference EVERY actor/capability/requirement?**
   - [ ] YES - Built index, verified each reference
   - [ ] NO - Validation is INVALID, must re-do

#### Systematic Verification
5. ⚠️ **Did I run grep searches for common issues?**
   - [ ] YES - Ran TODO, ID, placeholder searches
   - [ ] NO - Validation is INVALID, must re-do

6. ⚠️ **Did I check ADR headers for ID fields? (if validating ADR.md)**
   - [ ] YES - Verified `**ID**:` after EACH `## ADR-` heading
   - [ ] NO - Validation is INVALID, must re-do

7. ⚠️ **Did I verify traceability fields? (if validating DESIGN.md)**
   - [ ] YES - Checked `**Capabilities**:`, `**Actors**:` for each requirement
   - [ ] NO - Validation is INVALID, must re-do

#### Score Verification
8. ⚠️ **Is my score calculation arithmetically correct?**
   - [ ] YES - Verified addition
   - [ ] NO - Must recalculate

9. ⚠️ **Did I award points according to requirements file?**
   - [ ] YES - Used exact scoring from requirements
   - [ ] NO - Must re-score using requirements

10. ⚠️ **Did I compare score to correct threshold?**
    - [ ] YES - Used threshold from requirements
    - [ ] NO - Validation invalid, check threshold

**If ANY answer is NO → Validation is INVALID, must restart execution**

### Output Format Verification

**Agent ALWAYS verifies output includes**:
- [ ] Score breakdown by category
- [ ] All issues listed with ✅/❌
- [ ] Recommendations prioritized by severity
- [ ] Next steps (PASS or FAIL scenario)
- [ ] Self-test confirmation section

---

## Protocol Compliance Report

**Agent ALWAYS includes in output**:

```markdown
---

## Execution Protocol Compliance

**Phase 1: Protocol Initialization**
✅ Read workflow-execution.md
✅ Read workflow-execution-validations.md
✅ Read {workflow-name}.md
✅ Read {artifact}-structure.md
✅ Extracted all validation criteria

**Phase 2: Readiness Check**
✅ Passed all 11 readiness questions
✅ Understood "Maximum Attention to Detail"
✅ Created complete validation checklist

**Phase 3: Execution**
✅ Checked EVERY criterion individually
✅ Read entire artifact line by line
✅ Ran systematic grep searches
✅ Cross-referenced all IDs

**Phase 4: Post-Execution**
✅ Completed self-test (10/10 YES)
✅ Verified score calculation
✅ Confirmed no criteria skipped

**Protocol compliance: PASS ✅**
```

---

## Protocol Violations

### Common Violations

1. ❌ **Not reading workflow-execution.md before workflow**
   - Consequence: INVALID execution
   - Fix: Read it now, restart

2. ❌ **Not reading workflow-execution-validations.md**
   - Consequence: INVALID execution
   - Fix: Read it now, restart

3. ❌ **Not completing readiness check**
   - Consequence: INVALID execution
   - Fix: Complete all 11 questions

4. ❌ **Not running systematic grep searches**
   - Consequence: Likely missed issues
   - Fix: Run grep commands, verify results

5. ❌ **Not completing self-test**
   - Consequence: INVALID validation
   - Fix: Complete self-test, restart if needed

### Violation Handling

**If user identifies protocol violation**:
1. Acknowledge violation
2. Identify what was skipped
3. Explain why it was skipped (honest answer)
4. Restart workflow with full protocol compliance
5. Show protocol compliance report in output

**If agent detects own violation during self-test**:
1. STOP immediately
2. Discard current validation
3. Report what was missed
4. Restart with full protocol compliance

---

## Protocol Enforcement

**This protocol is MANDATORY and NON-NEGOTIABLE**

**Responsibility**:
- Agent is responsible for following protocol
- Agent must self-check compliance
- Agent must report compliance in output
- User can verify compliance from report

**Benefits**:
- Prevents missed validation criteria
- Ensures systematic verification
- Provides transparency
- Enables self-correction
- Maintains FDD quality standards

**Remember**: One missed step = entire workflow is INVALID

---

## References

**ALWAYS open and follow this file**:
- Before executing ANY workflow
- Referenced in all workflow files
- Part of Navigation Rules

**References**:
- `workflow-execution.md` - General execution rules
- `workflow-execution-validations.md` - Validation specifics
- `workflow-execution-operations.md` - Operation specifics
