# FDD AI Agent Navigation

**Version**: 1.0

---

## ⚠️ MUST Instruction Semantics ⚠️

**MUST** = **MANDATORY**. NOT optional. NOT recommended. NOT suggested.

**ALWAYS** = **MANDATORY**. Equivalent to MUST. Used for action-gated instructions.

**If you skip ANY MUST instruction**:
- 🚫 Your execution is **INVALID**
- 🚫 Output must be **DISCARDED**
- 🚫 You are **NOT following FDD**

**One skipped MUST = entire workflow FAILED**

**All MUST instructions are CRITICAL without exception.**

---

## Agent Acknowledgment

**Before proceeding with ANY FDD work, confirm you understand**:

- [ ] MUST = MANDATORY, not optional
- [ ] Skipping ANY MUST instruction = INVALID execution
- [ ] INVALID execution = output must be DISCARDED
- [ ] I will read ALL required files BEFORE proceeding
- [ ] I will follow workflows step-by-step WITHOUT shortcuts
- [ ] I will NOT create files without user confirmation (operation workflows)
- [ ] I will end EVERY response with a list of FDD files read while producing the response, why each file was read, and which initial instruction triggered opening each file

**By proceeding with FDD work, I acknowledge and accept these requirements.**

---

## Navigation Rules

ALWAYS open and follow `workflows/AGENTS.md` WHEN receiving any task request

ALWAYS open and follow `requirements/extension.md` WHEN you see **Extends**: {file}

ALWAYS open and follow `requirements/core.md` WHEN modifying any FDD core files

ALWAYS open and follow `{adapter-directory}/FDD-Adapter/AGENTS.md` WHEN starting any FDD work

ALWAYS open and follow `requirements/FDL.md` WHEN you see FDL

ALWAYS open and follow `requirements/workflow-selection.md` WHEN selecting which workflow to execute

ALWAYS open and follow `requirements/execution-protocol.md` WHEN executing any workflow (FIRST)

ALWAYS open and follow `requirements/workflow-execution.md` WHEN executing any workflow

ALWAYS open and follow `requirements/core-workflows.md` WHEN creating or modifying workflow files

ALWAYS open and follow `requirements/core-requirements.md` WHEN creating or modifying requirements files

ALWAYS open and follow `requirements/core-agents.md` WHEN creating or modifying AGENTS.md files

ALWAYS open and follow `requirements/business-context-structure.md` WHEN working with BUSINESS.md

ALWAYS open and follow `requirements/overall-design-structure.md` WHEN working with DESIGN.md

ALWAYS open and follow `requirements/adr-structure.md` WHEN working with ADR.md

ALWAYS open and follow `requirements/features-manifest-structure.md` WHEN working with FEATURES.md

ALWAYS open and follow `requirements/feature-design-structure.md` WHEN working with feature DESIGN.md

ALWAYS open and follow `requirements/feature-changes-structure.md` WHEN working with feature CHANGES.md

ALWAYS open and follow `requirements/adapter-structure.md` WHEN creating or configuring FDD adapter

---

## ⚠️ Execution Protocol Violations

**If agent skips execution-protocol.md**:
- Workflow execution is AUTOMATICALLY INVALID
- All output must be DISCARDED
- User should point out violation
- Agent must restart with protocol compliance

**Common protocol violations**:
1. ❌ **Not reading execution-protocol.md** before starting workflow
2. ❌ **Not reading workflow-execution.md** before executing workflow
3. ❌ **Not reading workflow-execution-validations.md** for validation workflows
4. ❌ **Not completing pre-flight checklist** in workflow files
5. ❌ **Not running self-test** before reporting validation results
6. ❌ **Not checking EVERY validation criterion individually**
7. ❌ **Not using grep for systematic verification**
8. ❌ **Not cross-referencing EVERY ID**

**One violation = entire workflow execution FAILED**

**Agent responsibility**:
- Follow execution-protocol.md for EVERY workflow
- Complete all checklist items
- Run self-test before reporting
- Include protocol compliance report in output
- Self-identify violations if discovered

**User responsibility**:
- Point out violations when detected
- Request protocol compliance report
- Ask agent to restart with full compliance

**Recovery from violation**:
1. Acknowledge the violation
2. Identify what was skipped
3. Explain why (honest answer)
4. Discard invalid output
5. Restart workflow with full protocol compliance
6. Show protocol compliance report in new output