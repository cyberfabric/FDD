# Feature Changes (Implementation Plan) Structure Requirements

**ALWAYS open and follow**: `../workflows/feature-changes.md`
**ALWAYS open and follow**: `requirements.md`
**ALWAYS open and follow**: `core.md` WHEN editing this file

**This file defines**: Structure only (WHAT to create)  
**Workflow defines**: Process (HOW to create)

⚠️ **Do NOT use this file alone. Execute the workflow, not just the structure.**

---

**Version**: 1.0  
**Purpose**: Define structure for feature implementation plan (replaces OpenSpec)

**Scope**: Implementation plan for feature requirements

---

## Overview

**Feature CHANGES.md** - Implementation plan breaking down feature requirements into atomic changes

**Purpose**: Define granular implementation plan for feature
- List of atomic changes implementing feature requirements
- Each change = 1-5 requirements
- Each change = one deployable unit
- Task breakdown for each change

**Location**: `architecture/features/feature-{slug}/CHANGES.md`

**Archived location**: `architecture/features/feature-{slug}/archive/YYYY-MM-DD-CHANGES.md`

**Validation workflows compatibility**:
- For validation workflows that require a CHANGES input (e.g., `feature-code-validate`), the CHANGES source MAY be either:
  - Active `CHANGES.md` (preferred)
  - The most recent archived `archive/YYYY-MM-DD-CHANGES.md` (fallback when active CHANGES.md is absent)

**Prerequisites**: Feature DESIGN.md validated (100/100 + 100%)

---

## File Structure

### Document Header

```markdown
# Implementation Plan: {Feature Name}

**Feature**: `{feature-slug}`  
**Version**: {version}  
**Last Updated**: YYYY-MM-DD  
**Status**: {Overall status}

**Feature DESIGN**: [DESIGN.md](DESIGN.md)

---

## Summary

**Total Changes**: {count}  
**Completed**: {count}  
**In Progress**: {count}  
**Not Started**: {count}

**Estimated Effort**: {total story points/hours}

---
```

### Change Entries

**Format**: One change per section

```markdown
## Change {Number}: {Change Name}

**ID**: `fdd-{project}-{feature}-change-{slug}`  
**Status**: ⏳ NOT_STARTED | 🔄 IN_PROGRESS | ✅ COMPLETED  
**Priority**: HIGH | MEDIUM | LOW  
**Effort**: {story points or hours}  
**Implements**: `fdd-{project}-{feature}-req-{id}`, `fdd-{project}-{feature}-req-{id}`
**Phases**: `ph-1` or `ph-{N}, ph-{N}`

---

### Objective

{Clear objective of this change - what will be achieved}

### Requirements Coverage

**Implements**:
- **`fdd-{project}-{feature}-req-{id}`**: {Requirement description}
- **`fdd-{project}-{feature}-req-{id}`**: {Requirement description}

**References**:
- Actor Flow: `fdd-{project}-feature-{feature}-flow-{slug}` (Section B of feature DESIGN.md)
- Algorithm: `fdd-{project}-feature-{feature}-algo-{slug}` (Section C of feature DESIGN.md)
- State: `fdd-{project}-feature-{feature}-state-{slug}` (Section D of feature DESIGN.md)
- Technical Detail: `fdd-{project}-feature-{feature}-td-{slug}` (Section E of feature DESIGN.md)

### Tasks

{Hierarchical task breakdown with numbered sections}

## 1. Implementation

### Code Tagging Tasks (Mandatory Pattern)

**Rule**: Code tagging MUST be represented as an explicit task that appears **immediately after** the specific task that changes code.

**Meaning**:
- If task `1.1.1` changes code, then task `1.1.2` MUST be: add the required FDD comment tags at the exact code location introduced/modified by `1.1.1`.
- Tagging MUST NOT be a separate "Task 0" done somewhere else; it MUST be attached to the relevant task.

**Required tag formats** (phase is ALWAYS a postfix):
- `@fdd-change:fdd-{project}-{feature}-change-{slug}:ph-{N}`
- `@fdd-req:fdd-{project}-{feature}-req-{id}:ph-{N}`
- `@fdd-flow:fdd-{project}-feature-{feature}-flow-{slug}:ph-{N}`
- `@fdd-algo:fdd-{project}-feature-{feature}-algo-{slug}:ph-{N}`
- `@fdd-state:fdd-{project}-feature-{feature}-state-{slug}:ph-{N}`
- `@fdd-test:fdd-{project}-{feature}-test-{id}:ph-{N}`

### 1.1 {Task Group Name}
- [ ] 1.1.1 {Task description with file path and action}
- [ ] 1.1.2 Add required FDD comment tags (with `:ph-{N}` postfix) at the exact code location changed in 1.1.1
- [ ] 1.1.3 {Next task description with file path and action}
- [ ] 1.1.4 Add required FDD comment tags (with `:ph-{N}` postfix) at the exact code location changed in 1.1.3

### 1.2 {Task Group Name}
- [ ] 1.2.1 {Task description with file path and action}
- [ ] 1.2.2 {Task description with file path and action}

## 2. Testing

### 2.1 {Test Group Name}
- [ ] 2.1.1 {Test description and validation}
- [ ] 2.1.2 {Test description and validation}

{Continue with all task groups}

**Format**: Hierarchical numbering with checkboxes (`- [ ]` incomplete, `- [x]` completed)

### Specification

{Detailed implementation specification}

**Domain Model Changes**:
- Type: `{type identifier}`
- Fields: {field specifications}
- Relationships: {relationship specifications}

**API Changes**:
- Endpoint: `{endpoint path}`
- Method: GET | POST | PUT | DELETE | PATCH
- Request: {request specification}
- Response: {response specification}

**Database Changes**:
- Table/Collection: `{name}`
- Schema: {schema specification}
- Migrations: {migration steps}

**Code Changes**:
- Module: `{module path}`
- Functions: {function signatures}
- Implementation: {high-level implementation approach}
- **Code Tagging**: MUST tag all code with `@fdd-change:fdd-{project}-{feature}-change-{slug}`

### Dependencies

**Depends on**:
- Change {Number}: {change name} (MUST be completed first)
- External: {external dependencies}

**Blocks**:
- Change {Number}: {change name} (this MUST be completed first)

### Testing

**Unit Tests**:
- Test: {test description}
- File: `{test file path}`
- Validates: {what is validated}

**Integration Tests**:
- Test: {test description}
- File: `{test file path}`
- Validates: {what is validated}

**E2E Tests**:
- Scenario: {scenario from Section F of feature DESIGN.md}
- File: `{test file path}`
- Validates: {what is validated}

**Testing Scenario Implementation** (MANDATORY):
- All testing scenarios from feature DESIGN.md Section F MUST be implemented
- Each test MUST reference its testing scenario ID for traceability
- Format: `// @fdd-test:fdd-{project}-feature-{feature-slug}-test-{scenario-name}:ph-{N}`
- Tests MUST NOT be ignored without documented justification
- Tests MUST validate actual behavior (not placeholders)

### Validation Criteria

**Code validation** (MUST pass):
- All tasks completed
- All tests pass (including tests for all testing scenarios from DESIGN.md Section F)
- Code follows adapter conventions
- No linter errors
- Documentation updated
- Implements all referenced requirements
- **Code tagged**: All modified/new code has `@fdd-change:fdd-{project}-{feature}-change-{slug}:ph-{N}` tags (full format only)
- **Phase postfix**: All feature-scoped tags use `:ph-{N}` postfix; standalone phase tags MUST NOT exist
- **Phase consistency**: Every `:ph-{N}` used in code tags MUST be listed in the change `**Phases**` field
- **Testing scenarios implemented**: All testing scenarios from feature DESIGN.md Section F have corresponding tests

---
```

---

## Code Tagging Requirements

**Purpose**: Enable traceability from code to change identifiers for auditing, debugging, and impact analysis

**Tag Format**: `@fdd-change:fdd-{project}-{feature}-change-{slug}:ph-{N}` (ONLY full format allowed)

**Phase Postfix Format**: `:ph-{N}` (phase is always a postfix of other FDD tags)

**Mandatory Placement**:
- At the beginning of all new functions, methods, classes, structs, types
- At the beginning of modified functions, methods, classes that implement change logic
- In complex code blocks directly implementing change requirements
- In test files validating change functionality

**Phase Tagging Rules**:
- Standalone phase tags MUST NOT be used.
- Because every change MUST declare `**Phases**`, all code implementing that change MUST include phase postfixes on feature-scoped tags.
- Minimum required tag for change implementation: `@fdd-change:{change-id}:ph-{N}`.

**Algorithm tag format (mandatory)**:
- When `@fdd-algo` is used, it MUST include a phase postfix: `@fdd-algo:{algo-id}:ph-{N}`.

**Language-Specific Format**:
- **Rust**: `// @fdd-change:{change-id}:ph-{N}`
- **TypeScript/JavaScript**: `// @fdd-change:{change-id}:ph-{N}`
- **Python**: `# @fdd-change:{change-id}:ph-{N}`
- **Go**: `// @fdd-change:{change-id}:ph-{N}`
- **Java/C#**: `// @fdd-change:{change-id}:ph-{N}`
- **SQL**: `-- @fdd-change:{change-id}:ph-{N}`

**Examples**:

```rust
// @fdd-change:fdd-analytics-feature-schema-query-returns-change-gts-schema-types:ph-1
pub struct SchemaV1 {
    pub schema_id: String,
    pub version: String,
    pub fields: Vec<SchemaField>,
}

// @fdd-change:fdd-analytics-feature-schema-query-returns-change-gts-schema-types:ph-1
impl SchemaV1 {
    pub fn new(schema_id: String) -> Self {
        Self {
            schema_id,
            version: "1.0".to_string(),
            fields: Vec::new(),
        }
    }
}
```

```typescript
// @fdd-change:fdd-analytics-feature-schema-query-returns-change-api-rest-endpoints:ph-1
export async function handleSchemaQuery(
    req: Request,
    context: QueryContext
): Promise<SchemaResponse> {
    // Implementation
}

// @fdd-change:fdd-analytics-feature-schema-query-returns-change-api-rest-endpoints:ph-1
export class SchemaQueryHandler {
    async execute(query: SchemaQuery): Promise<SchemaResult> {
        // Implementation
    }
}
```

**Multiple Changes in Same File**:
```python
# @fdd-change:fdd-analytics-feature-schema-query-returns-change-schema-validation:ph-1
def validate_schema_structure(schema: dict) -> ValidationResult:
    pass

# @fdd-change:fdd-analytics-feature-schema-query-returns-change-type-conversion:ph-1
def convert_gts_to_json_schema(gts_schema: GTSSchema) -> dict:
    pass
```

**Test Files**:
```rust
// @fdd-change:fdd-analytics-feature-schema-query-returns-change-gts-schema-types:ph-1
#[cfg(test)]
mod schema_v1_tests {
    use super::*;
    
    #[test]
    fn test_schema_creation() {
        let schema = SchemaV1::new("test-schema".to_string());
        assert_eq!(schema.version, "1.0");
    }
}
```

**Validation**:
- Search the codebase for `@fdd-change:{change-id}:ph-` to find all tagged code
- Verify all files listed in CHANGES.md tasks have corresponding tags
- Verify all major functions/classes implementing change have tags
- Tag count should correlate with implementation scope

---

## Validation Criteria

### File Structure Validation

1. **CHANGES source exists**
   - Active file at `architecture/features/feature-{slug}/CHANGES.md` OR
   - Archived file at `architecture/features/feature-{slug}/archive/YYYY-MM-DD-CHANGES.md`
   - Contains required sections

2. **Document header present**
   - Feature reference
   - Version
   - Status
   - Summary with counts

3. **Change entries valid**
   - All changes numbered sequentially
   - All changes have unique IDs
   - All changes have status
   - All changes have priority
   - All changes reference feature requirements
   - All changes declare `**Phases**` with `ph-{N}` values (at least `ph-1`)

### Content Validation

1. **Change structure**
   - Objective clear and specific
   - Requirements coverage lists all implemented requirements
   - All requirement IDs exist in feature DESIGN.md Section F
   - References contain explicit FDD IDs (flow/algo/state/technical detail)
   - Tasks are granular and actionable
   - Tasks include mandatory code tagging instructions (comments with FDD IDs)
   - Specification is complete
   - Testing plan covers all scenarios

2. **Task breakdown**
   - Each task has clear action
   - Each task specifies affected files
   - Each task has validation criteria
   - Tasks in logical order
   - Each change includes a dedicated code tagging task group ensuring tags are added to code comments

3. **Specification completeness**
   - Domain model changes specified
   - API changes specified
   - Database changes specified
   - Code changes specified
   - All specifications follow adapter format

4. **Dependency tracking**
   - Dependencies listed
   - No circular dependencies
   - Dependency graph is acyclic (DAG)

5. **Testing coverage**
   - Unit tests for all code changes
   - Integration tests for API/DB changes
   - E2E tests for user scenarios
   - All tests reference feature DESIGN.md Section F scenarios
   - **MANDATORY**: All testing scenarios from feature DESIGN.md Section F have implemented tests
   - Each test includes scenario ID comment for traceability: `// @fdd-test:{scenario-id}:ph-{N}`

### Consistency Validation

1. **Feature DESIGN.md consistency**
   - All changes implement feature requirements
   - No changes implement non-existent requirements
   - All feature requirements covered by at least one change
   - References to actor flows, algorithms, states, technical details are valid (IDs exist in feature DESIGN.md)

2. **Code tagging consistency**
   - No standalone phase tags exist in code
   - All feature-scoped tags include `:ph-{N}` postfix
   - `:ph-{N}` values used in code match `**Phases**` declared by their change(s)

3. **Adapter consistency**
   - Domain model uses adapter format
   - API contracts use adapter format
   - Database schema uses adapter conventions
   - Code structure follows adapter conventions

4. **Parent artifact consistency**
   - No contradictions with DESIGN.md
   - No contradictions with BUSINESS.md
   - Types reference Overall Design domain model
   - No type redefinitions

### Completeness Validation

1. **All requirements covered**
   - Every requirement from feature DESIGN.md Section F has implementing change
   - Coverage map shows 100% coverage
   - No requirements orphaned

2. **Change atomicity**
   - Each change implements 1-5 requirements
   - Each change is deployable independently (after dependencies)
   - No change too large (>10 tasks)
   - No change too small (<1 requirement)

### Validation Scoring

**Breakdown**:
- File structure (10 points): CHANGES.md + change directories
- Change structure (20 points): All required sections
- Task breakdown (15 points): Granular, actionable, validated
- Specification (15 points): Complete domain/API/DB/code specs
- Code tagging (5 points): Tag format specified, validation approach defined
- Testing (15 points): Unit/integration/E2E coverage
- Consistency (10 points): No contradictions with parent artifacts
- Completeness (10 points): All requirements covered, 100% coverage

**Pass threshold**: ≥90/100

---

## Examples

### Valid CHANGES.md Entry

```markdown
# Implementation Plan: Analytics Event Tracking

**Feature**: `analytics-event-tracking`  
**Version**: 1.0  
**Last Updated**: 2025-01-07  
**Status**: 🔄 IN_PROGRESS

**Feature DESIGN**: [DESIGN.md](DESIGN.md)

---

## Summary

**Total Changes**: 3  
**Completed**: 1  
**In Progress**: 1  
**Not Started**: 1

**Estimated Effort**: 13 story points

---

## Change 1: Event Schema Definition

**ID**: `fdd-analytics-feature-event-tracking-change-event-schema`  
**Status**: ✅ COMPLETED  
**Priority**: HIGH  
**Effort**: 3 story points  
**Implements**: `fdd-analytics-event-req-domain-model`

---

### Objective

Define domain model for analytics events including event types, properties, and metadata.

### Requirements Coverage

**Implements**:
- **`fdd-analytics-event-req-domain-model`**: System MUST define event schema with type, properties, timestamp, user context

**References**:
- Actor Flow: Section B.1 - User triggers event
- Technical Detail: Section E.1 - Domain model specification

### Tasks

## 1. Implementation

### 1.1 Define Type Schemas
- [x] 1.1.1 Create GTS type definition for Event at `gts/analytics/event.v1.gts`
- [x] 1.1.2 Create GTS type for EventProperties at `gts/analytics/event_properties.v1.gts`
- [x] 1.1.3 Create GTS type for EventMetadata at `gts/analytics/event_metadata.v1.gts`

## 2. Testing

### 2.1 Schema Validation
- [x] 2.1.1 Verify all types compile and export valid JSON Schema
- [x] 2.1.2 Verify EventProperties supports arbitrary key-value pairs
- [x] 2.1.3 Verify EventMetadata includes timestamp and user context

### Specification

**Domain Model Changes**:
- Type: `gts.analytics.event.v1`
- Fields:
  - `id: string` - Unique event identifier
  - `type: string` - Event type (e.g., "page_view", "click")
  - `properties: EventProperties` - Event-specific properties
  - `metadata: EventMetadata` - Timestamp, user context
- Relationships: None

**API Changes**: None (domain model only)

**Database Changes**: None (domain model only)

**Code Changes**:
- Module: `domain/analytics/`
- Functions: Type definitions only
- Implementation: GTS schema compilation

### Dependencies

**Depends on**: None (first change)

**Blocks**: Change 2, Change 3

### Testing

**Unit Tests**:
- Test: Event schema validation
- File: `tests/domain/analytics/event_test.rs`
- Validates: Schema compiles, all fields present

### Validation Criteria

**Code validation**:
- ✅ All tasks completed
- ✅ GTS types compile
- ✅ JSON Schema output valid
- ✅ No linter errors
- ✅ Implements `fdd-analytics-event-req-domain-model`

---

## Change 2: Event Ingestion API

**ID**: `fdd-analytics-feature-event-tracking-change-event-api`  
**Status**: 🔄 IN_PROGRESS  
**Priority**: HIGH  
**Effort**: 5 story points  
**Implements**: `fdd-analytics-event-req-ingest-api`, `fdd-analytics-event-req-validation`

---

{Similar structure for Change 2}

---

## Change 3: Event Storage

**ID**: `fdd-analytics-feature-event-tracking-change-event-storage`  
**Status**: ⏳ NOT_STARTED  
**Priority**: MEDIUM  
**Effort**: 5 story points  
**Implements**: `fdd-analytics-event-req-persistence`

---

{Similar structure for Change 3}

---

## Workflow Integration

**Feature changes workflows**:
- `feature-changes` - Create/edit implementation plan
- `feature-changes-validate` - Validate plan structure and completeness
- `feature-change-implement` - Implement specific change task-by-task
- `feature-code-validate` - Validate entire feature code against feature design (replaces feature-change-validate)

**Prerequisites**:
- Feature DESIGN.md validated (100/100 + 100%)
- All feature requirements finalized

**Validation frequency**:
- After creating CHANGES.md
- After modifying CHANGES.md
- Before starting implementation
- After completing each change

---

## Change Status Lifecycle

```
⏳ NOT_STARTED
    ↓ (start implementation)
🔄 IN_PROGRESS
    ↓ (complete all tasks + validation passes)
✅ COMPLETED
    ↓ (all changes completed - optional)
📦 ARCHIVED
```

**Status transitions**:
- NOT_STARTED → IN_PROGRESS: When first task started
- IN_PROGRESS → COMPLETED: When all tasks done AND validation passes
- IN_PROGRESS → NOT_STARTED: Rollback if needed
- COMPLETED → IN_PROGRESS: If issues found, reopen change
- COMPLETED → ARCHIVED: When all changes in CHANGES.md are completed (optional)

---

## Archiving Completed CHANGES.md

**When to archive**:
- All changes in CHANGES.md have status `✅ COMPLETED`
- Summary section: `**Completed**: {N}` equals `**Total Changes**: {N}`
- Feature implementation fully complete

**Archive location**:
```
architecture/features/feature-{slug}/archive/YYYY-MM-DD-CHANGES.md
```

**Archive process**:
1. Verify all changes completed
2. Create archive directory if not exists: `architecture/features/feature-{slug}/archive/`
3. Generate timestamp filename: `YYYY-MM-DD-CHANGES.md` (current date)
4. Move CHANGES.md to archive location
5. Confirm archiving complete

**Purpose**:
- Preserve historical implementation records
- Allow new CHANGES.md for future feature enhancements
- Maintain clean feature directory structure
- Document completed implementation milestones

**When NOT to archive**:
- Changes still in progress or not started
- Feature may need revisions or fixes
- User prefers to keep active CHANGES.md for reference

**Archive trigger workflows**:
- `feature-changes` workflow (Step 7) - Manual archive option in UPDATE mode
- `feature-changes-validate` workflow - Suggests archiving when all completed

---

## References

**Replaces**: OpenSpec integration

**Used by workflows**:
- `feature-changes` - Creates/edits CHANGES.md
- `feature-code-validate` - Validates entire feature code against design
- `feature-change-implement` - Implements change

**Related requirements**:
- `feature-design-structure.md` - Feature DESIGN.md structure
- `adapter-structure.md` - Adapter conventions
- `overall-design-structure.md` - Domain model reference
