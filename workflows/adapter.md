---
description: FDD Adapter Router - Choose adapter workflow mode
---

# FDD Adapter Workflow (Router)

**Type**: Operation  
**Role**: Any  
**Artifact**: `{adapter-directory}/FDD-Adapter/AGENTS.md` + specs

---

**ALWAYS open and follow**: `../requirements/core.md` WHEN editing this file

ALWAYS open and follow `../requirements/workflow-execution.md` WHEN executing this workflow

## Purpose

**Router workflow** - Determines which adapter workflow to execute based on:
- User intent
- Adapter state (exists/missing)
- Project state (greenfield/existing)

**Delegates to**:
- `adapter-bootstrap` - Minimal initialization (new projects)
- `adapter-auto` - Automatic project scanning (existing codebases)
- `adapter-manual` - Manual specification updates (user-initiated)

---

## Requirements

**ALWAYS open and follow**: `../requirements/adapter-structure.md`

Extract:
- Adapter lifecycle phases
- When to use each mode

---

## Prerequisites

**Prerequisites**:
- [ ] Project repository exists - validate: Check .git directory exists
- [ ] Write permissions - validate: Can create directories and files

---

## Decision Flow

### 1. Check Adapter State

Search for adapter:
- `/FDD-Adapter/AGENTS.md`
- `spec/FDD-Adapter/AGENTS.md`
- `docs/FDD-Adapter/AGENTS.md`

**Result**:
- `ADAPTER_EXISTS = true/false`
- `ADAPTER_DIR = path` (if exists)

### 2. Determine Context

**If called from workflow trigger** (adapter-triggers.md):
```yaml
Context: trigger-based evolution
Mode: EVOLUTION (handled by adapter-triggers, not this router)
Action: Skip router, direct execution
```

**If called manually by user**:
```yaml
Context: user-initiated
Continue to Step 3
```

### 3. Analyze User Intent

**Check user request for keywords**:

```yaml
Keywords for BOOTSTRAP:
  - "initialize adapter"
  - "create adapter"
  - "setup adapter"
  - "bootstrap"
  
Keywords for AUTO:
  - "scan project"
  - "discover"
  - "analyze codebase"
  - "auto-scan"
  - "from sources"
  
Keywords for MANUAL:
  - "add {spec}"
  - "update {spec}"
  - "add pattern"
  - "add snippet"
  - "manually"
```

**If keywords found**:
- Route to appropriate workflow
- Continue to Step 5

**If NO keywords** (ambiguous):
- Continue to Step 4

### 4. Interactive Mode Selection

**If ADAPTER_EXISTS = false**:

```
No adapter found.

Choose initialization mode:
  1. Bootstrap - Create minimal adapter (just Extends)
     → For greenfield projects
     → Specs added later through design workflow
  
  2. Auto-scan - Scan existing project and generate specs
     → For existing codebases
     → Discovers tech stack, patterns, conventions
  
Choose: [1-2]
```

**If ADAPTER_EXISTS = true**:

```
Adapter found at: {ADAPTER_DIR}

Current specs:
  - specs/tech-stack.md
  - specs/domain-model.md
  - specs/api-contracts.md

Choose update mode:
  1. Auto-scan - Re-scan project for new patterns
     → Discovers changes in codebase
     → Proposes additions/updates
  
  2. Manual update - Manually add/update specifications
     → Interactive Q&A
     → Precise control over content
  
Choose: [1-2]
```

**Based on choice**:
- Set `MODE = bootstrap | auto | manual`

### 5. Route to Specific Workflow

**MODE = bootstrap**:
```yaml
Execute: adapter-bootstrap.md
Purpose: Create minimal AGENTS.md
Result: {ADAPTER_DIR}/FDD-Adapter/AGENTS.md (with Extends only)
```

**MODE = auto**:
```yaml
Execute: adapter-auto.md
Purpose: Scan project and generate specs
Result: AGENTS.md + specs/*.md files
```

**MODE = manual**:
```yaml
Execute: adapter-manual.md
Purpose: Interactive specification update
Result: Created/updated spec files
```

### 6. Delegate Execution

**Run selected workflow**:
```
Routing to: {selected-workflow}
Executing: {selected-workflow}.md

[workflow execution output]
```

### 7. Return Control

After workflow completes:
```
═══════════════════════════════════════════════
Adapter Workflow Complete

Mode: {bootstrap|auto|manual}
Location: {ADAPTER_DIR}
Files: [list of created/updated files]

Validation: [score/status from workflow]
═══════════════════════════════════════════════
```

---

## Automatic Routing Examples

### Example 1: User Says "initialize adapter"

```yaml
Step 1: Check adapter → NOT found
Step 3: Keyword detected → "initialize"
Step 5: Route to → adapter-bootstrap
Execute: adapter-bootstrap.md
Result: Minimal AGENTS.md created
```

### Example 2: User Says "scan project"

```yaml
Step 1: Check adapter → Found (minimal)
Step 3: Keyword detected → "scan"
Step 5: Route to → adapter-auto
Execute: adapter-auto.md
Result: Specs generated from codebase
```

### Example 3: User Says "add Redis to adapter"

```yaml
Step 1: Check adapter → Found (with specs)
Step 3: Keyword detected → "add"
Step 5: Route to → adapter-manual
Execute: adapter-manual.md
Result: specs/tech-stack.md updated
```

---

## Interactive Routing Examples

### Example 4: Ambiguous "update adapter"

```yaml
Step 1: Check adapter → Found
Step 3: No specific keywords
Step 4: Interactive selection

Agent asks:
  "Choose update mode:
   1. Auto-scan
   2. Manual update"

User: "1"
Step 5: Route to → adapter-auto
Execute: adapter-auto.md
```

### Example 5: No adapter exists, user says "run adapter"

```yaml
Step 1: Check adapter → NOT found
Step 3: No specific keywords
Step 4: Interactive selection

Agent asks:
  "Choose initialization mode:
   1. Bootstrap
   2. Auto-scan"

User: "2"
Step 5: Route to → adapter-auto
Execute: adapter-auto.md
```

---

## Quick Reference

| User Intent | Adapter State | Route To |
|-------------|---------------|----------|
| "Initialize/create/setup" | Missing | `adapter-bootstrap` |
| "Scan/discover/analyze" | Any | `adapter-auto` |
| "Add/update {spec}" | Exists | `adapter-manual` |
| Ambiguous request | Missing | Ask: bootstrap or auto |
| Ambiguous request | Exists | Ask: auto or manual |
| Triggered from workflow | Any | Direct evolution (not via router) |

---

## Validation

Each delegated workflow runs its own validation.

Router does NOT validate - it only routes.

---

## Notes

**This is a routing workflow** - it does NOT create files itself.

**Purpose**: Simplify adapter workflow selection for users

**Trigger-based evolution**: Does NOT use this router - evolution calls are direct

**User-initiated updates**: Always go through this router for clarity

---

## References

**Delegates to**:
- `adapter-bootstrap.md` - Minimal initialization
- `adapter-auto.md` - Automatic scanning
- `adapter-manual.md` - Manual updates

**Referenced by**:
- `adapter-structure.md` - Main workflow reference
- `workflow-execution.md` - Adapter initialization check
- `adapter-triggers.md` - Trigger-based calls (bypass router)
