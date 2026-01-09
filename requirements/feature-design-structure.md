# Feature Design Structure Requirements

**ALWAYS open and follow**: `../workflows/feature.md`

**This file defines**: Structure only (WHAT to create)  
**Workflow defines**: Process (HOW to create)

⚠️ **Do NOT use this file alone. Execute the workflow, not just the structure.**

---

**Purpose**: Define required structure for `architecture/features/feature-{slug}/DESIGN.md`

**Used by**:
- Workflow 05 (init-feature): Generate feature DESIGN.md template
- Workflow 06 (validate-feature): Validate feature DESIGN.md completeness

---

## File Location

**Path**: `architecture/features/feature-{slug}/DESIGN.md`

**Size limits**:
- Recommended: ≤3000 lines
- Hard limit: ≤4000 lines

---

## Required Sections

### Section A: Feature Context

**Purpose**: Feature overview, purpose, actors, and references

**Size Constraint**: ≤200 lines recommended

**Required subsections**:
1. **Overview**: What this feature does
2. **Purpose**: Why it exists, what problem it solves
3. **Actors**: Who interacts with this feature (must match Overall Design actors)
4. **References**: Links to Overall Design sections and dependencies

**Content requirements**:
- Clear feature scope definition
- References to Overall Design (architecture/DESIGN.md)
- List of dependencies on other features (if any)
- Actor names must match Overall Design Section A exactly

---

### Section B: Actor Flows

**Purpose**: Document how actors interact with the feature

**Size Constraint**: ≥50 lines (standard features)

**Flow ID Format**: `fdd-{project-name}-feature-{feature-slug}-flow-{flow-name}`
- **Components**:
  - `fdd-` - Prefix indicating FDD methodology
  - `{project-name}` - Project name in kebab-case
  - `-feature-` - Feature scope indicator
  - `{feature-slug}` - Feature identifier in kebab-case
  - `-flow-` - Flow indicator
  - `{flow-name}` - Flow name in kebab-case (2-4 words)
- **Example**: `fdd-payment-system-feature-user-auth-flow-login`, `fdd-analytics-feature-dashboard-flow-create-widget`
- **Usage**: Each flow must have `**ID**: {id}` before flow title/description
- **Format in document**: `**ID**: fdd-project-feature-slug-flow-name`

**Content requirements**:
- Written in FDL (see `../FDL.md` for syntax)
- Each flow must have unique ID
- Each flow includes: Actor, Steps, Success Scenarios, Error Scenarios
- Flows are comprehensive and cover main use cases
- **NO code blocks** - only FDL syntax
- **FDL Keywords**: Only valid FDL keywords (see `../FDL.md`):
  - ✅ Allowed: **IF**, **ELSE IF**, **ELSE**, **FOR EACH**, **WHILE**, **TRY**, **CATCH**, **RETURN**, **PARALLEL**, **MATCH**, **CASE**, **GO TO**, **SKIP TO**, **FROM**, **TO**
  - ❌ Prohibited bold keywords: **WHEN** (in flows), **THEN**, **SET**, **VALIDATE**, **CHECK**, **LOAD**, **READ**, **WRITE**, **CREATE**, **ADD**, **AND**
  - Plain English actions (not bold) are allowed: "Set variable", "Load template"

**Exceptions**:
- Init/structural features may have minimal flows
- Infrastructure features with minimal user interaction may have shorter flows

---

### Section C: Algorithms

**Purpose**: Document algorithms in FDL (not code)

**Size Constraint**: ≥100 lines (standard features)

**Algorithm ID Format**: `fdd-{project-name}-feature-{feature-slug}-algo-{algo-name}`
- **Components**:
  - `fdd-` - Prefix indicating FDD methodology
  - `{project-name}` - Project name in kebab-case
  - `-feature-` - Feature scope indicator
  - `{feature-slug}` - Feature identifier in kebab-case
  - `-algo-` - Algorithm indicator
  - `{algo-name}` - Algorithm name in kebab-case (2-4 words)
- **Example**: `fdd-payment-system-feature-user-auth-algo-validate-token`, `fdd-analytics-feature-dashboard-algo-aggregate-data`
- **Usage**: Each algorithm must have `**ID**: {id}` before algorithm title
- **Format in document**: `**ID**: fdd-project-feature-slug-algo-name`

**Content requirements**:
- Algorithms written in FDL (see `../FDL.md`)
- Each algorithm must have unique ID
- Each algorithm: Input, Output, Steps in FDL
- **NO programming language code** (`rust`, `typescript`, `javascript`, `python`, etc.)
- **NO programming syntax** (`fn`, `function`, `def`, `class`, `interface`)
- Use FDL control structures: **IF**, **FOR EACH**, **WHILE**, **TRY/CATCH**, **RETURN**
- **FDL Keywords**: Same as Section B (see above)

**Exception**: Init/structural features may have minimal algorithms

---

### Section D: States

**Purpose**: Document state machines and state transitions in FDL

**State Machine ID Format**: `fdd-{project-name}-feature-{feature-slug}-state-{entity-name}`
- **Components**:
  - `fdd-` - Prefix indicating FDD methodology
  - `{project-name}` - Project name in kebab-case
  - `-feature-` - Feature scope indicator
  - `{feature-slug}` - Feature identifier in kebab-case
  - `-state-` - State machine indicator
  - `{entity-name}` - Entity/object name in kebab-case (1-3 words)
- **Example**: `fdd-payment-system-feature-order-processing-state-order`, `fdd-analytics-feature-dashboard-state-widget`
- **Usage**: Each state machine must have `**ID**: {id}` before state machine definition
- **Format in document**: `**ID**: fdd-project-feature-slug-state-entity`

**Content requirements**:
- States written in FDL (see `../FDL.md`)
- Each state machine must have unique ID
- State definitions with **WHEN** keyword (only valid in state machines)
- State transitions clearly documented
- **FDL Keywords for States**:
  - ✅ Allowed: **WHEN** (states only), **FROM**, **TO**, **IF**, **ELSE**
  - State machine format: numbered list with bold **WHEN** transitions

**Note**: Optional if feature has no state management

---

### Section E: Technical Details

**Purpose**: Implementation-specific technical information

**Size Constraint**: ≥200 lines recommended

**Required subsections**:
1. **Database Schema**: Tables/entities, columns, relationships (if applicable)
2. **API Endpoints**: Endpoint list with descriptions, reference API specification
3. **Security**: Authorization rules, access control
4. **Error Handling**: Error types and handling approaches

**Reference Requirements**:
- **Domain Model references**: Must be clickable links to domain model files
  - Format: `@/path/to/domain-model-file` or markdown links to GTS/schema files
  - Example: `User` type → link to `@/gts/user.gts` or domain model section
- **API Spec references**: Must be clickable links to API specification files
  - Format: `@/path/to/api-spec-file` or markdown links to OpenAPI/spec files
  - Example: `POST /users` → link to `@/openapi/users.yaml` or API spec section
- All external references must be verifiable and navigable

**Content requirements**:
- References to Overall Design domain model (no type redefinitions)
- References to Overall Design API contracts (no endpoint redefinitions)
- Sufficient detail for implementation
- External spec references where appropriate

---

### Section F: Requirements

**Purpose**: Formalized requirements with traceability

**Requirement ID Format**: `fdd-{project-name}-feature-{feature-slug}-req-{short-name}`
- **Components**:
  - `fdd-` - Prefix indicating FDD methodology
  - `{project-name}` - Project name in kebab-case (from project context)
  - `-feature-` - Feature scope indicator
  - `{feature-slug}` - Feature identifier in kebab-case
  - `-req-` - Requirement indicator
  - `{short-name}` - Short descriptive name in kebab-case (2-4 words)
- **Example**: `fdd-payment-system-feature-user-auth-req-login-flow`
- **Usage**: Each requirement must have `**ID**: {id}` before requirement title
- **Format in document**: `**ID**: fdd-project-feature-slug-req-name`

**Testing Scenario ID Format**: `fdd-{project-name}-feature-{feature-slug}-test-{scenario-name}`
- **Components**:
  - `fdd-` - Prefix indicating FDD methodology
  - `{project-name}` - Project name in kebab-case
  - `-feature-` - Feature scope indicator
  - `{feature-slug}` - Feature identifier in kebab-case
  - `-test-` - Testing scenario indicator
  - `{scenario-name}` - Scenario name in kebab-case (2-4 words)
- **Example**: `fdd-payment-system-feature-user-auth-test-valid-login`, `fdd-analytics-feature-dashboard-test-create-widget-success`
- **Usage**: Each testing scenario must have `**ID**: {id}` before scenario description
- **Format in document**: `**ID**: fdd-project-feature-slug-test-scenario`

**Required content per requirement**:
- **ID**: Requirement ID in format above (for traceability)
- **Title**: `### {Title}` (simple title, no numbering)
- **Status**: ⏳ NOT_STARTED, 🔄 IN_PROGRESS, or ✅ IMPLEMENTED
- **Description**: Clear description with SHALL/MUST statements
- **References**: Markdown anchors to sections B-E (≥1 reference)
- **Testing Scenarios**: ≥1 test scenario in FDL format (numbered lists + plain English)
  - Each testing scenario must have unique ID in format above
  - ❌ **NO Gherkin/BDD keywords**: **GIVEN**, **WHEN**, **THEN**, **AND** prohibited in Testing Scenarios
  - ✅ **MUST be implemented**: Testing Scenarios are specifications for actual test code
  - ✅ **Test generation**: Every Testing Scenario must have corresponding automated test in implementation
  - ✅ **Traceability**: Test files must reference Testing Scenario ID for traceability
  - ✅ Use plain English: "User provides command", "System parses", "Verify output"
- **Acceptance Criteria**: ≥2 specific, testable criteria

**Validation**:
- ≥1 requirement present
- All requirements have all required fields
- References are valid (target sections exist)
- Testing scenarios use FDL format (not Gherkin)

---

### Section G: Additional Context (Optional)

**Purpose**: Dependencies, references, and supplementary information

**Content may include**:
- **Dependencies**: Other features this feature depends on or blocks
- **References**: Links to related documentation, specs, standards
- **Notes**: Implementation notes, known limitations, future enhancements
- **Diagrams**: Links to architecture diagrams or flowcharts

**Note**: Implementation planning and change tracking is handled in separate `CHANGES.md` file (see `feature-changes-structure.md`)

---

## Validation Criteria

### File-Level Validation

1. **File exists and size**
   - File `architecture/features/feature-{slug}/DESIGN.md` exists
   - File ≤4000 lines (warning if >3000)
   - File has substantial content

### Structure Validation

1. **All required sections present**
   - Sections A, B, C, D, E, F (6 sections required)
   - Section G (Additional Context) is optional
   - Correct section order (A → B → C → D → E → F → [G])
   - Each section has proper heading (`## A.`, `## B.`, etc.)
   - No duplicate sections

### Content Validation

1. **Section A (Feature Context)**
   - ≤500 lines
   - All required subsections present
   - References to Overall Design included
   - Actor names match Overall Design

2. **Section B (Actor Flows)**
   - ≥50 lines (standard features)
   - Uses FDL syntax (not code)
   - Only valid FDL keywords used
   - No prohibited keywords (**WHEN** in flows, **THEN**, **SET**, etc.)
   - **Flow ID Format Validation**:
     - All flows have unique IDs with `**ID**: fdd-{project-name}-feature-{feature-slug}-flow-{flow-name}` format
     - All IDs use kebab-case (lowercase with hyphens)
     - Each flow has `**ID**: {id}` label before flow title

3. **Section C (Algorithms)**
   - ≥100 lines (standard features)
   - Uses FDL syntax (not code)
   - No programming language code blocks
   - Only valid FDL keywords used
   - **Algorithm ID Format Validation**:
     - All algorithms have unique IDs with `**ID**: fdd-{project-name}-feature-{feature-slug}-algo-{algo-name}` format
     - All IDs use kebab-case (lowercase with hyphens)
     - Each algorithm has `**ID**: {id}` label before algorithm title

4. **Section D (States)**
   - Uses FDL syntax if applicable
   - **WHEN** keyword only in states (not flows/algorithms)
   - **State Machine ID Format Validation**:
     - All state machines have unique IDs with `**ID**: fdd-{project-name}-feature-{feature-slug}-state-{entity-name}` format
     - All IDs use kebab-case (lowercase with hyphens)
     - Each state machine has `**ID**: {id}` label before state machine definition

5. **Section E (Technical Details)**
   - ≥200 lines recommended
   - All technical aspects covered
   - References to Overall Design specs

6. **Section F (Requirements)**
   - ≥1 requirement present
   - Each requirement has all required fields
   - Testing Scenarios use FDL (not Gherkin)
   - References are valid markdown anchors
   - **Requirement ID Format Validation**:
     - All requirement IDs match format with `**ID**: fdd-{project-name}-feature-{feature-slug}-req-{short-name}`
     - All IDs are unique within Section F
     - IDs use kebab-case (lowercase with hyphens)
     - Each requirement has `**ID**: {id}` label before title
   - **Testing Scenario ID Format Validation**:
     - All testing scenarios have unique IDs with `**ID**: fdd-{project-name}-feature-{feature-slug}-test-{scenario-name}` format
     - All IDs use kebab-case (lowercase with hyphens)
     - Each testing scenario has `**ID**: {id}` label before scenario description
     - Test code must reference these IDs for traceability

7. **Section G (Additional Context)** - Optional
   - If present, may include dependencies, references, notes
   - No specific structure requirements
   - **Note**: Implementation changes belong in `CHANGES.md`, not in DESIGN.md

### Cross-Validation with Overall Design

**CRITICAL**: Feature Design must align with Overall Design

**Domain Types**:
- ✅ All types referenced (not redefined) from Overall Design Section C
- ❌ No new type definitions in feature DESIGN.md
- Use DML notation per adapter

**API Endpoints**:
- ✅ All endpoints referenced from Overall Design Section C
- ❌ No new endpoint definitions in feature DESIGN.md

**Actors**:
- ✅ Only actors from Overall Design Section A
- ❌ No new actors invented in feature
- Actor roles match Overall Design

**Capabilities**:
- ✅ Feature aligns with Overall Design capabilities
- Feature scope matches Overall Design

### Completeness Validation

1. **No placeholders**
   - No TODO, TBD, FIXME, XXX markers
   - No `{placeholder}` content
   - All sections fully written

2. **No type redefinitions**
   - No phrases like "type definition"
   - No schema definitions in JSON/YAML blocks
   - All types referenced from Overall Design

---

## Output Requirements

### For Generator (Workflow 05)

**Generate**:
- File at `architecture/features/feature-{slug}/DESIGN.md`
- All required sections with headers
- Template content for each section
- Comments guiding what to fill

### For Validator (Workflow 06)

**Validate**:
1. File-level (exists, size)
2. Structure (all sections present, correct order)
3. Content (FDL syntax, no code, sufficient detail)
4. Cross-validation (alignment with Overall Design)
5. Completeness (no placeholders, no type redefinitions)

**Report format**:
- Score: X/100 (must be 100)
- Completeness: X% (must be 100%)
- Issues: List of missing/invalid items
- Recommendations: What to fix

**Scoring**:
- Structure (20 points): All required sections present (A-F)
- FDL Compliance (30 points): Sections B, C, D use valid FDL
- Technical Details (25 points): Section E complete
- Requirements (25 points): Section F formalized with tests

---

## Examples

**Valid feature DESIGN.md structure**:
```markdown
# Feature: Analytics Dashboard

## A. Overview

**Feature ID**: `feature-analytics-dashboard`
**References**: FEATURES.md entry `FEAT-001`

Create dashboard for visualizing user analytics...

## B. Actor Flows (FDL)

### Admin Views Dashboard

1. User opens dashboard page
2. System loads analytics data
3. **FOR EACH** metric:
   1. Calculate value
   2. Display chart
4. User interacts with filters

## C. Algorithms (FDL)

**Algorithm: Calculate Metric**
Input: metric_id, date_range
Output: metric_value

1. Load raw data for date range
2. **FOR EACH** data point:
   1. Apply calculation
3. **RETURN** aggregated value

## D. States (FDL)

**State Machine: Dashboard**
**States**: LOADING, READY, ERROR
**Transitions**:
1. **FROM** LOADING **TO** READY **WHEN** data loaded
2. **FROM** LOADING **TO** ERROR **WHEN** load failed

## E. Technical Details

### Database Schema
...

### API Endpoints
...

## F. Requirements

**REQ-001**: Dashboard MUST load within 2 seconds
...

## G. Additional Context (Optional)

### Dependencies
- **Depends On**: feature-user-auth
- **Blocks**: feature-reporting

### References
- Overall Design: `architecture/DESIGN.md`
- External Spec: https://example.com/spec
```

**Invalid feature DESIGN.md**:
```markdown
# Dashboard Feature

We need a dashboard with some charts.

It should show analytics data.
```

**Issues**: No sections, no FDL, no requirements, no technical details

---

## References

**Workflows using this**:
- `workflows/05-init-feature.md` - Generate feature DESIGN.md
- `workflows/06-validate-feature.md` - Validate feature DESIGN.md

**Related specifications**:
- `../FDL.md` - FDL syntax for flows, algorithms, states
- `overall-design-structure.md` - Overall Design structure
- `../AGENTS.md` - Core FDD rules

**Related workflows**:
- `workflows/02-validate-architecture.md` - Overall Design validation
- `workflows/09-openspec-change-next.md` - Next step after validation
