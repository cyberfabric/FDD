# Features Manifest (FEATURES.md) Structure Requirements

**ALWAYS open and follow**: `../workflows/features.md`
**ALWAYS open and follow**: `requirements.md`
**ALWAYS open and follow**: `core.md` WHEN editing this file

**This file defines**: Structure only (WHAT to create)  
**Workflow defines**: Process (HOW to create)

⚠️ **Do NOT use this file alone. Execute the workflow, not just the structure.**

---

**Version**: 1.0  
**Purpose**: Define required structure for `architecture/features/FEATURES.md`

**Used by**:
- Workflow 03 (init-features): Generate FEATURES.md from Overall Design
- Workflow 04 (validate-features): Validate FEATURES.md completeness

---

## File Location

**Path**: `architecture/features/FEATURES.md`

**Purpose**: Central manifest tracking all features in the project

---

## Required Structure

### Header Section

**Project metadata**:
```markdown
# Features: {PROJECT_NAME}

**Status Overview**: X features total (Y completed, Z in progress, W not started)

**Meaning**:
- ⏳ NOT_STARTED
- 🔄 IN_PROGRESS
- ✅ IMPLEMENTED
```

**Status summary** showing feature breakdown by status

---

### Feature List Section

**Format**: Numbered sections with subsections

**Required per feature**:
1. **Section heading**: `### N. [fdd-{project}-feature-{feature-slug}](feature-{feature-slug}/) EMOJI PRIORITY`
   - N: Sequential number (1, 2, 3, ...)
   - Slug: Lowercase kebab-case
   - Emoji: ⏳ (NOT_STARTED), 🔄 (IN_PROGRESS), ✅ (IMPLEMENTED)
   - Priority: CRITICAL, HIGH, MEDIUM, LOW

2. **Purpose**: `**Purpose**: One-line description`

3. **Status**: `**Status**: NOT_STARTED | IN_PROGRESS | IMPLEMENTED`

4. **Depends On**: MUST be one of:
   - `**Depends On**: None`
   - `**Depends On**: [feature-a](feature-a/), [feature-b](feature-b/)`
   - `**Depends On**:` followed by a markdown list (preferred for long lists):
     - `- [feature-a](feature-a/)`
     - `- [feature-b](feature-b/)`
   - Phase-aware dependency (recommended when only a phase is required):
     - `- [feature-a](feature-a/)` `ph-1`
     - `- [feature-b](feature-b/)` `ph-2`

   **Rules**:
   - Feature-level dependency (no phase specified) means the dependency feature MUST be `**Status**: IMPLEMENTED`.
   - Phase-aware dependency means the referenced feature phase MUST be ✅ IMPLEMENTED.

5. **Blocks**: MUST be one of:
   - `**Blocks**: None`
   - `**Blocks**: [feature-a](feature-a/), [feature-b](feature-b/)`
   - `**Blocks**:` followed by a markdown list (preferred for long lists):
     - `- [feature-a](feature-a/)`
     - `- [feature-b](feature-b/)`

6. **Scope**: `**Scope**:` followed by bulleted list

7. **Requirements Covered**: MUST be one of:
   - `**Requirements Covered**: fdd-..., fdd-..., fdd-...` (comma-separated on one line)
   - `**Requirements Covered**:` followed by a markdown list (preferred for long lists):
     - `- fdd-...`
     - `- fdd-...`
   IDs MUST reference actual requirement IDs from `architecture/DESIGN.md` Section B.1 and B.2.

8. **Principles Covered** (optional): MUST be one of:
   - `**Principles Covered**: fdd-..., fdd-...`
   - `**Principles Covered**:` followed by a markdown list
   IDs MUST reference principle IDs from `architecture/DESIGN.md` Section B.3.

9. **Constraints Affected** (optional): MUST be one of:
   - `**Constraints Affected**: fdd-..., fdd-...`
   - `**Constraints Affected**:` followed by a markdown list
   IDs MUST reference constraint IDs from `architecture/DESIGN.md` Section B.4.

10. **Phases**: Use to track implementation progress at finer granularity than feature status.

**Phase ID Format**: `ph-{N}`
- N MUST be an integer (1, 2, 3, ...)
- Default: Every feature MUST define `ph-1`

**Format** (preferred):
- `**Phases**:` followed by a markdown list
  - - `ph-1`: ✅ IMPLEMENTED — {short meaning}
  - - `ph-2`: 🔄 IN_PROGRESS — {short meaning}
  - - `ph-3`: ⏳ NOT_STARTED — {short meaning}

**Phase dependencies** (optional, phase-scoped):
- A phase MAY declare dependencies on other feature phases.
- Format: nested list under the phase item:
  - - `ph-2`: 🔄 IN_PROGRESS — {meaning}
    - **Depends On**:
      - `[feature-a](feature-a/)` `ph-1`

**Rules**:
- A feature with `**Status**: IMPLEMENTED` MUST have ALL phases marked ✅ IMPLEMENTED.
- A phase marked ✅ IMPLEMENTED MUST have corresponding code tagged with phase postfixes on feature-scoped tags (e.g. `@fdd-change:{id}:ph-{N}`, `@fdd-flow:{id}:ph-{N}`, `@fdd-algo:{id}:ph-{N}`, `@fdd-req:{id}:ph-{N}`).
- A phase marked ✅ IMPLEMENTED MUST NOT depend on any phase that is 🔄 IN_PROGRESS or ⏳ NOT_STARTED.

---

## Rendering Requirements (Markdown)

**MUST** ensure feature metadata fields render as separate lines.

Allowed formats:
- End each metadata line with two spaces (`  `) to force a line break.
- Or use a markdown list for metadata fields (preferred; avoids relying on invisible trailing spaces).

**MUST NOT** rely on markdown soft-wrap for very long tokens (e.g., long inline code spans or tables).

**Example**:
```markdown
### 1. [fdd-example-feature-user-auth](feature-user-auth/) ⏳ CRITICAL
- **Purpose**: User authentication and authorization
- **Status**: NOT_STARTED
- **Depends On**: None
- **Blocks**: [feature-user-profile](feature-user-profile/), [feature-notifications](feature-notifications/)
- **Phases**:
  - `ph-1`: ⏳ NOT_STARTED — Default phase
- **Scope**:
  - Login/logout flows
  - JWT token management
  - Password reset

---

### 2. [fdd-example-feature-user-profile](feature-user-profile/) ⏳ HIGH
- **Purpose**: User profile management
- **Status**: NOT_STARTED
- **Depends On**: [feature-user-auth](feature-user-auth/)
- **Blocks**: None
- **Phases**:
  - `ph-1`: ⏳ NOT_STARTED — Default phase
- **Scope**:
  - Profile CRUD operations
  - Avatar upload
  - Settings management
```

---

## Validation Criteria

### File-Level Validation

1. **File exists**
   - `architecture/features/FEATURES.md` exists

2. **Header present**
   - Project name in title
   - Status overview present

### Structure Validation

1. **Feature list present**
   - ≥1 feature defined
   - All features have required fields

2. **Feature entry format**
   - Status emoji valid (⏳🔄✅)
   - Slug is kebab-case
   - Design path exists
   - Dependencies reference valid features
   - `**Phases**` field present for every feature
   - Phase IDs follow `ph-{N}` format and are written as inline code in markdown
   - Every feature defines at least `ph-1`
   - Phase dependencies (if present) use the same link + inline phase token format

### Content Validation

1. **Feature directories exist**
   - Each feature has directory: `architecture/features/feature-{slug}/`
   - DESIGN.md exists in each feature directory (if status ≠ NOT_STARTED)

2. **Dependencies valid**
   - All dependency slugs reference existing features
   - No circular dependencies (DAG structure)
   - Dependency order is implementable
   - Phase dependencies (if present) are satisfiable (every referenced `{feature} {phase}` exists)
   - Phase dependency graph is acyclic

3. **Status consistency**
   - Feature status matches DESIGN.md existence
   - IN_PROGRESS features have DESIGN.md
   - IMPLEMENTED features have complete DESIGN.md
   - IMPLEMENTED features MUST have ALL phases marked ✅ IMPLEMENTED
   - Phase dependencies MUST be satisfiable (no dependency on a NOT_STARTED phase for an IMPLEMENTED phase)

### Cross-Validation with Overall Design

1. **Feature alignment**
   - Features derived from Overall Design capabilities
   - Feature scope matches Overall Design
   - No features contradict Overall Design

2. **Completeness**
   - All Overall Design capabilities covered by features
   - No orphaned features (not mapped to capabilities)

### ID Traceability Validation

**CRITICAL**: Full traceability chain from BUSINESS.md → DESIGN.md → FEATURES.md

**ID Type Catalog**:

**BUSINESS.md contains**:
- Actors: `fdd-{project}-actor-{name}` (Section B)
- Capabilities: `fdd-{project}-capability-{name}` (Section C)
- Use Cases: `fdd-{project}-usecase-{name}` (Section D)

**DESIGN.md contains**:
- Functional Requirements: `fdd-{project}-req-{name}` (Section B.1)
- Non-Functional Requirements: `fdd-{project}-nfr-{name}` (Section B.2)
- Principles: `fdd-{project}-principle-{name}` (Section B.3)
- Constraints: `fdd-{project}-constraint-{name}` (Section B.4)

**FEATURES.md references**: Only DESIGN.md IDs (requirements, principles, constraints)

---

**Traceability Rules**:

1. **BUSINESS.md → DESIGN.md** (validated in overall-design-structure.md):
   - All capability IDs from BUSINESS.md Section C MUST be referenced in DESIGN.md requirement **Source** field
   - All use case IDs from BUSINESS.md Section D MUST be referenced in DESIGN.md requirement **Source** field
   - All actor IDs from BUSINESS.md Section B MUST be referenced in DESIGN.md (if applicable to system)

2. **DESIGN.md → FEATURES.md** (validated in features-manifest-structure.md):
   - All requirement IDs from DESIGN.md Section B.1 (FR-XXX) MUST appear in at least one feature's "Requirements Covered"
   - All requirement IDs from DESIGN.md Section B.2 (NFR-XXX) MUST appear in at least one feature's "Requirements Covered"
   - Principle IDs from DESIGN.md Section B.3 SHOULD appear in "Principles Covered" (if feature implements principle)
   - Constraint IDs from DESIGN.md Section B.4 SHOULD appear in "Constraints Affected" (if feature affected by constraint)

3. **ID Format Validation**:
   - All IDs follow format: `fdd-{project}-{type}-{name}`
   - FEATURES.md must use exact IDs from DESIGN.md (no short codes like "FR-001")
   - No capability/usecase IDs in FEATURES.md (wrong level - they belong in DESIGN.md)

**Validation Checks**:
- ✅ Every capability ID from BUSINESS.md is referenced in DESIGN.md requirement source field
- ✅ Every requirement ID from DESIGN.md appears in at least one feature's "Requirements Covered"
- ✅ No orphaned requirements (DESIGN.md requirements not covered by any feature)
- ✅ No invalid IDs (FEATURES.md references non-existent DESIGN.md IDs)
- ✅ ID format consistency (all IDs follow naming convention)

**Example Traceability Chain**:
```
BUSINESS.md:
├─ fdd-acronis-mcp-capability-workflow-mgmt (Section C)
└─ References in:
   └─ DESIGN.md FR-001: fdd-acronis-mcp-req-workflow-context
      └─ References in:
         └─ FEATURES.md Feature #1: fdd-context-provider
            └─ Requirements Covered: fdd-acronis-mcp-req-workflow-context
```

**Scoring Impact**:
- Missing traceability: -10 points per orphaned requirement
- Invalid ID references: -5 points per invalid ID
- Format violations: -2 points per violation

---

## Status Lifecycle

**Feature states**:
1. **⏳ NOT_STARTED**: Feature planned, no DESIGN.md yet
2. **🔄 IN_PROGRESS**: DESIGN.md exists, implementation not complete
3. **✅ IMPLEMENTED**: All OpenSpec changes completed, feature validated

**State transitions**:
- NOT_STARTED → IN_PROGRESS: Start feature design (workflow 05)
- IN_PROGRESS → IMPLEMENTED: Complete all changes (workflow 07)

---

## Generation Guidelines

### For Generator (Workflow 03)

**Input**: Overall Design capabilities (Section A)

**Process**:
1. Extract capabilities from Overall Design
2. Identify foundational vs. dependent features
3. Propose feature breakdown
4. User reviews and confirms
5. Generate FEATURES.md with all entries
6. Create feature directories

**Output**:
- `FEATURES.md` with all features listed
- Feature directories created
- All features in NOT_STARTED status initially

### For Validator (Workflow 04)

**Validate**:
1. File-level (exists)
2. Structure
3. Content
4. Cross-validation

---

## Dependency Rules

1. **Acyclic**: No circular dependencies allowed
2. **Valid references**: All dependencies must exist in manifest
3. **Implementation order**: Dependencies must be implemented before dependents
4. **Foundation first**: Core/infrastructure features have no dependencies

---

## Example FEATURES.md

```markdown
# Features: hyperspot

**Status Overview**: 3 features total (1 completed, 1 in progress, 1 not started)

**Meaning**:
- ⏳ NOT_STARTED
- 🔄 IN_PROGRESS
- ✅ IMPLEMENTED

---

## Features List

### 1. [fdd-hyperspot-feature-user-auth](feature-user-auth/) ✅ CRITICAL
- **Purpose**: User authentication and authorization
- **Status**: IMPLEMENTED
- **Depends On**: None
- **Blocks**: None
- **Requirements Covered**:
  - fdd-hyperspot-req-authentication
  - fdd-hyperspot-req-authorization
- **Phases**:
  - `ph-1`: ✅ IMPLEMENTED — Login/logout flows
  - `ph-2`: ✅ IMPLEMENTED — Token validation and refresh
- **Scope**:
  - Login/logout flows
  - Token issuance/validation
  - Session revocation

---

### 2. [fdd-hyperspot-feature-analytics-dashboard](feature-analytics-dashboard/) 🔄 HIGH
- **Purpose**: Analytics dashboard for key metrics
- **Status**: IN_PROGRESS
- **Depends On**:
  - [fdd-hyperspot-feature-user-auth](feature-user-auth/) `ph-2`
- **Blocks**: None
- **Requirements Covered**:
  - fdd-hyperspot-req-usage-analytics
- **Phases**:
  - `ph-1`: 🔄 IN_PROGRESS — Initial dashboard render with metrics list
  - `ph-2`: ⏳ NOT_STARTED — Filters and rerender
    - **Depends On**:
      - [fdd-hyperspot-feature-user-auth](feature-user-auth/) `ph-2`
- **Scope**:
  - Read-only metrics UI
  - Filtered views
  - Role-based access

---

### 3. [fdd-hyperspot-feature-notifications](feature-notifications/) ⏳ MEDIUM
- **Purpose**: Notification delivery (email + in-app)
- **Status**: NOT_STARTED
- **Depends On**:
  - [fdd-hyperspot-feature-user-auth](feature-user-auth/)
- **Blocks**: None
- **Requirements Covered**:
  - fdd-hyperspot-req-notifications
- **Phases**:
  - `ph-1`: ⏳ NOT_STARTED — Email notifications
  - `ph-2`: ⏳ NOT_STARTED — In-app notifications
- **Scope**:
  - Email notifications
  - In-app notifications
  - User preferences
```

---

## References

**Workflows using this**:
- `workflows/03-init-features.md` - Generate FEATURES.md
- `workflows/04-validate-features.md` - Validate FEATURES.md

**Related specifications**:
- `overall-design-structure.md` - Overall Design (source of capabilities)
- `feature-design-structure.md` - Feature Design structure

**Related workflows**:
- `workflows/05-init-feature.md` - Initialize individual feature
- `workflows/07-complete-feature.md` - Mark feature as IMPLEMENTED
