---
description: Implement specific change from implementation plan
---

# Implement Feature Change

**Type**: Operation  
**Role**: Developer  
**Artifact**: Code files, tests

---

**ALWAYS open and follow**: `../requirements/core.md` WHEN editing this file

ALWAYS open and follow `../requirements/workflow-execution.md` WHEN executing this workflow

<!-- fdd-begin fdd-fdd-feature-core-methodology-flow-developer-implement:ph-1:inst-read-requirements -->
## Requirements

**ALWAYS open and follow**: 
- `../requirements/feature-changes-structure.md` (change structure)
- `{adapter-directory}/AGENTS.md` (code conventions)

Extract:
- Task format and execution model
- Code conventions from adapter
- Testing requirements from adapter
<!-- fdd-end   fdd-fdd-feature-core-methodology-flow-developer-implement:ph-1:inst-read-requirements -->

---

## Prerequisites

<!-- fdd-begin fdd-fdd-feature-core-methodology-flow-developer-implement:ph-1:inst-read-prerequisites -->
**MUST validate**:
- [ ] CHANGES.md validated - validate: Score ≥90/100
- [ ] Adapter exists - validate: Check adapter AGENTS.md (REQUIRED for development)
<!-- fdd-end   fdd-fdd-feature-core-methodology-flow-developer-implement:ph-1:inst-read-prerequisites -->

**If adapter missing**: STOP, run `adapter` workflow first

---

## Steps

### 1. Select Change

<!-- fdd-begin fdd-fdd-feature-core-methodology-flow-developer-implement:ph-1:inst-select-task -->
Ask user: Which change to implement?

Options: List NOT_STARTED or IN_PROGRESS changes from CHANGES.md

Store change ID
<!-- fdd-end   fdd-fdd-feature-core-methodology-flow-developer-implement:ph-1:inst-select-task -->

### 2. Read Change Specification

Open CHANGES.md

Extract for selected change:
- Objective
- Requirements implemented
- Task list with files and validation

### 3. Read Adapter Conventions

Open `{adapter-directory}/AGENTS.md`

Follow MUST WHEN instructions for:
- Code conventions
- Testing requirements
- Build requirements

### 3.1 Code Tagging
<!-- fdd-begin fdd-fdd-feature-core-methodology-flow-developer-implement:ph-1:inst-add-tags -->
Tag code with required @fdd-* markers.

## Step 4: Add FDD Tags

**Action**: Tag code with @fdd-* markers

Tag code with required @fdd-* markers.
<!-- fdd-end   fdd-fdd-feature-core-methodology-flow-developer-implement:ph-1:inst-add-tags -->

**Rule**: Phase MUST be encoded as a postfix on feature-scoped tags. Standalone phase tags MUST NOT be used.

**Instruction-level traceability (mandatory)**:
- When implementing a specific FDL step (flow/algo/state/test step) you MUST tag the corresponding code block using:
  - `fdd-{project}-feature-{feature}-[flow|algo|state|test]-{scope-name}:ph-{N}:inst-{local}`
  - The `{scope}` part MUST be the existing ID from DESIGN/CHANGES (do NOT invent a new scope prefix).
  - `{local}` is the local FDL instruction ID from the step line (e.g., `inst-load-raw-events`)
- Preferred format in code comments:
  - `// fdd-hyperspot-feature-gts-core-algo-calculate-metric-value:ph-1:inst-load-raw-events`

**Open/close tags (mandatory when possible)**:
**Open/close tags (mandatory for instruction tags)**:
- For every FDL instruction step (`...:ph-{N}:inst-...`), you MUST use paired begin/end tags that wrap non-empty code:
  - `// fdd-begin fdd-...:ph-{N}:inst-...`
  - `// fdd-end   fdd-...:ph-{N}:inst-...`
- Single-line instruction tags MUST NOT be used.

**Tag placement rules (by implementation location)**:
- **No empty blocks**: `fdd-begin`/`fdd-end` MUST NOT be adjacent with no effective code between them.
- **Begin/end pairing**: Every `fdd-begin ...:inst-...` MUST have a matching `fdd-end ...:inst-...`.
- **In-function logic**: If the step is implemented in the current function body, wrap the exact code that performs the step.
- **Extractor-based steps (function signature)**: If the step is implemented by framework extractors (e.g., `Path(id)`, `Json(body)`, `OData(query)`), place the step tag on the extractor binding in the function signature, or on the closest line where the extracted value is first transformed/validated.
- **External middleware / platform / third-party libraries**: If the step is implemented by middleware or external libraries, place the step tag on the integration point:
  - The relevant `use ...` import(s), and/or
  - The middleware/Layer registration (router/module registration), whichever is the real attachment point.
- **Routing-only delegation**: If the feature is routing-only, step tags MUST wrap the routing decision logic and its error branches (e.g., 404/501), not downstream domain logic.

- Change ID: `@fdd-change:fdd-{project}-{feature}-change-{slug}:ph-{N}` (from CHANGES source; phase postfix is mandatory)
- Flow ID: `@fdd-flow:{flow-id}:ph-{N}` (Section B of DESIGN; phase postfix is mandatory)  
  _Example_: `@fdd-flow:fdd-analytics-feature-gts-core-flow-route-crud-operations:ph-1`
- Algorithm ID: `@fdd-algo:{algo-id}:ph-{N}` (Section C of DESIGN; phase postfix is mandatory)  
  _Example_: `@fdd-algo:fdd-analytics-feature-gts-core-algo-routing-logic:ph-1`
- State ID: `@fdd-state:{state-id}:ph-{N}` (Section D of DESIGN, if present; phase postfix is mandatory)  
  _Example_: `@fdd-state:fdd-analytics-feature-gts-core-state-entity-lifecycle:ph-1`
- Requirement ID: `@fdd-req:{req-id}:ph-{N}` (Section F of DESIGN; phase postfix is mandatory)  
  _Example_: `@fdd-req:fdd-analytics-feature-gts-core-req-routing:ph-1`
- Test scenario ID: `@fdd-test:{test-id}:ph-{N}` (Section F of DESIGN; phase postfix is mandatory)  
  _Example_: `@fdd-test:fdd-analytics-feature-gts-core-test-routing-table-lookup:ph-1`

**Tag placement**:
- At the beginning of new/modified functions, methods, structs, or complex blocks implementing the logic
- At the beginning of test modules/functions that implement test scenarios
- Prefer multiple tags when a block covers multiple IDs (e.g., change + req + algo)

**Examples (multiple IDs allowed)**:
<!-- !no-fdd-begin -->
```rust
// @fdd-change:fdd-analytics-feature-schema-query-returns-change-gts-schema-types:ph-1
// @fdd-req:fdd-analytics-feature-schema-query-returns-req-routing:ph-1
// @fdd-algo:fdd-analytics-feature-schema-query-returns-algo-routing-logic:ph-1
pub struct SchemaV1 {
    pub schema_id: String,
    pub version: String,
}
```

```rust
// fdd-begin fdd-hyperspot-feature-gts-core-algo-calculate-metric-value:ph-1:inst-load-raw-events
// fdd-req:fdd-hyperspot-feature-gts-core-req-routing:ph-1
fn load_raw_events(...) {
    // ...
}
// fdd-end fdd-hyperspot-feature-gts-core-algo-calculate-metric-value:ph-1:inst-load-raw-events
```

```rust
// fdd-begin fdd-analytics-feature-gts-core-flow-route-crud-operations:ph-1:inst-return-routing-decision
match decision {
    Some(handler) => {
        // fdd-begin fdd-analytics-feature-gts-core-flow-route-crud-operations:ph-1:inst-else-if-delegate-missing
        // fdd-begin fdd-analytics-feature-gts-core-flow-route-crud-operations:ph-1:inst-return-501-no-delegate
        let err = Problem::new(StatusCode::NOT_IMPLEMENTED, "Not Implemented", "No delegate registered");
        // fdd-end fdd-analytics-feature-gts-core-flow-route-crud-operations:ph-1:inst-return-501-no-delegate
        // fdd-end fdd-analytics-feature-gts-core-flow-route-crud-operations:ph-1:inst-else-if-delegate-missing
        Err(err)
    }
    None => {
        // fdd-begin fdd-analytics-feature-gts-core-flow-route-crud-operations:ph-1:inst-if-no-match
        // fdd-begin fdd-analytics-feature-gts-core-flow-route-crud-operations:ph-1:inst-return-404-unknown-type
        let err = Problem::new(StatusCode::NOT_FOUND, "Unknown GTS Type", "No feature registered");
        // fdd-end fdd-analytics-feature-gts-core-flow-route-crud-operations:ph-1:inst-return-404-unknown-type
        // fdd-end fdd-analytics-feature-gts-core-flow-route-crud-operations:ph-1:inst-if-no-match
        Err(err)
    }
}
// fdd-end fdd-analytics-feature-gts-core-flow-route-crud-operations:ph-1:inst-return-routing-decision
```

```rust
// fdd-begin fdd-analytics-feature-gts-core-flow-route-crud-operations:ph-1:inst-if-jwt-invalid
// fdd-begin fdd-analytics-feature-gts-core-flow-route-crud-operations:ph-1:inst-return-401
use modkit_security::SecurityCtx;
// fdd-end fdd-analytics-feature-gts-core-flow-route-crud-operations:ph-1:inst-return-401
// fdd-end fdd-analytics-feature-gts-core-flow-route-crud-operations:ph-1:inst-if-jwt-invalid
```

```typescript
// @fdd-change:fdd-analytics-feature-schema-query-returns-change-api-rest-endpoints:ph-1
export async function handleSchemaQuery(
    req: Request
): Promise<SchemaResponse> {
    // Implementation
}
```

```python
# @fdd-change:fdd-analytics-feature-schema-query-returns-change-schema-validation:ph-1
# @fdd-req:fdd-analytics-feature-schema-query-returns-req-validation:ph-1
def validate_schema_structure(schema: dict):
    pass

# @fdd-change:fdd-analytics-feature-schema-query-returns-change-type-conversion:ph-1
def convert_gts_to_json_schema(gts_schema):
    pass
```
<!-- !no-fdd-end -->

### 3.2 Tag Verification (agent checklist)

**ALWAYS verify** (before finishing implementation):
- Search the codebase for ALL IDs from CHANGES (change IDs) and DESIGN (flow/algo/state/req/test)
- Confirm tags exist in the files that implement corresponding logic/tests
- If any DESIGN ID has no code tag → report as gap and/or add tag

**Suggested searches**:
- `@fdd-change:` to list change-tagged files
- `@fdd-flow:`, `@fdd-algo:`, `@fdd-state:`, `@fdd-req:`, `@fdd-test:` to confirm DESIGN coverage

<!-- fdd-begin fdd-fdd-feature-core-methodology-flow-developer-implement:ph-1:inst-run-tests -->
Run the project test suite.

## Step 5: Run Tests

**Action**: Execute test suite
<!-- fdd-end   fdd-fdd-feature-core-methodology-flow-developer-implement:ph-1:inst-run-tests -->

<!-- fdd-begin fdd-fdd-feature-core-methodology-flow-developer-implement:ph-1:inst-write-code -->
Implement code changes for the selected task.

### 4. Implement Tasks

**For each task in change**:
1. Read task specification from CHANGES.md (hierarchical format: `1.1.1`, `1.2.1`, etc.)
2. Implement according to adapter conventions
3. Run task validation

<!-- fdd-end   fdd-fdd-feature-core-methodology-flow-developer-implement:ph-1:inst-write-code -->

4.

<!-- fdd-begin fdd-fdd-feature-core-methodology-flow-developer-implement:ph-1:inst-mark-complete -->
Mark the task as complete in CHANGES.md.

## Step 6: Update CHANGES.md

**Action**: Mark task as completed

ckbox from `- [ ]` to `- [x]`
   - Example: `- [ ] 1.1.1 Task description` → `- [x] 1.1.1 Task description`
<!-- fdd-end   fdd-fdd-feature-core-methodology-flow-developer-implement:ph-1:inst-mark-complete -->
5. Proceed to next task

**After each task**:
- Show progress: Task {X}/{total} complete
- Ask: Continue to next task? [yes/pause]

### 5. Mark Change Complete

After all tasks done:
1. **Update change status in CHANGES.md**:
   - Change header: `**Status**: 🔄 IN_PROGRESS` → `**Status**: ✅ COMPLETED`
2. **Update summary section**:
   - Increment "Completed" count
   - Decrement "In Progress" or "Not Started" count
3. Verify all task checkboxes marked `- [x]`

---

## Validation

After implementing all changes, run: `feature-code-validate`

**Note**: Validation is now done at feature level (not per-change)

Expected:
- All feature code compiles/runs
- All tests pass (including test scenarios from DESIGN.md)
- All requirements implemented
- No TODO/FIXME in business logic

---

## Next Steps

**After implementing all changes**: 
- Run `feature-code-validate` to validate entire feature
- If validation passes: mark feature as COMPLETE in FEATURES.md
- If validation fails: Fix code, re-validate

---

<!-- fdd-begin fdd-fdd-feature-core-methodology-flow-developer-implement:ph-1:inst-receive-assignment -->
<!-- fdd-begin fdd-fdd-feature-core-methodology-flow-developer-implement:ph-1:inst-open-agents-workflow -->
## Context

Developer receives feature assignment from team lead and opens root AGENTS.md to start workflow.
<!-- fdd-end   fdd-fdd-feature-core-methodology-flow-developer-implement:ph-1:inst-open-agents-workflow -->
<!-- fdd-end   fdd-fdd-feature-core-methodology-flow-developer-implement:ph-1:inst-receive-assignment -->

<!-- fdd-begin fdd-fdd-feature-core-methodology-flow-developer-implement:ph-1:inst-report-errors -->
<!-- fdd-begin fdd-fdd-feature-core-methodology-flow-developer-implement:ph-1:inst-fix-issues -->
<!-- fdd-begin fdd-fdd-feature-core-methodology-flow-developer-implement:ph-1:inst-rerun-validation -->
## Error Recovery

**If validation fails**:
1. System reports validation errors with line numbers
2. Developer fixes issues based on recommendations  
3. Developer re-runs validation

Repeat until validation passes.
<!-- fdd-end   fdd-fdd-feature-core-methodology-flow-developer-implement:ph-1:inst-rerun-validation -->
<!-- fdd-end   fdd-fdd-feature-core-methodology-flow-developer-implement:ph-1:inst-fix-issues -->
<!-- fdd-end   fdd-fdd-feature-core-methodology-flow-developer-implement:ph-1:inst-report-errors -->
