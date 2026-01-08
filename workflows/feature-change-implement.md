---
description: Implement specific change from implementation plan
---

# Implement Feature Change

**Type**: Operation  
**Role**: Developer  
**Artifact**: Code files, tests

---

## Requirements

**MUST read**: 
- `../requirements/feature-changes-structure.md` (change structure)
- `{adapter-directory}/FDD-Adapter/AGENTS.md` (code conventions)

Extract:
- Task format and execution model
- Code conventions from adapter
- Testing requirements from adapter

---

## Prerequisites

**MUST validate**:
- [ ] CHANGES.md validated - validate: Score ≥90/100
- [ ] Adapter exists - validate: Check adapter AGENTS.md (REQUIRED for development)

**If adapter missing**: STOP, run `adapter` workflow first

---

## Steps

### 1. Select Change

Ask user: Which change to implement?

Options: List NOT_STARTED or IN_PROGRESS changes from CHANGES.md

Store change ID

### 2. Read Change Specification

Open CHANGES.md

Extract for selected change:
- Objective
- Requirements implemented
- Task list with files and validation

### 3. Read Adapter Conventions

Open `{adapter-directory}/FDD-Adapter/AGENTS.md`

Follow MUST WHEN instructions for:
- Code conventions
- Testing requirements
- Build requirements

### 3.1 Code Tagging Requirements

**MUST tag all code changes with change identifier**:

**Tag format**: `@fdd-change:fdd-{project}-{feature}-change-{slug}` (ONLY full format allowed)

**Tag placement**:
- At the beginning of new functions/methods
- At the beginning of modified functions/methods
- In complex code blocks implementing change logic
- In test files for change validation

**Examples**:
```rust
// @fdd-change:fdd-analytics-feature-schema-query-returns-change-gts-schema-types
pub struct SchemaV1 {
    pub schema_id: String,
    pub version: String,
}
```

```typescript
// @fdd-change:fdd-analytics-feature-schema-query-returns-change-api-rest-endpoints
export async function handleSchemaQuery(
    req: Request
): Promise<SchemaResponse> {
    // Implementation
}
```

**Multiple changes in same file**:
```python
# @fdd-change:fdd-analytics-feature-schema-query-returns-change-schema-validation
def validate_schema_structure(schema: dict):
    pass

# @fdd-change:fdd-analytics-feature-schema-query-returns-change-type-conversion
def convert_gts_to_json_schema(gts_schema):
    pass
```

### 4. Implement Tasks

**For each task in change**:
1. Read task specification from CHANGES.md (hierarchical format: `1.1.1`, `1.2.1`, etc.)
2. Implement according to adapter conventions
3. Run task validation
4. **Update CHANGES.md**: Change task checkbox from `- [ ]` to `- [x]`
   - Example: `- [ ] 1.1.1 Task description` → `- [x] 1.1.1 Task description`
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

Run: `feature-change-validate`

Expected:
- Code compiles/runs
- Tests pass
- Matches requirements

---

## Next Steps

**If validation passes**: 
- Next change: `feature-change-implement` (if more changes)
- All done: `feature-qa` workflow

**If validation fails**: Fix code, re-validate
