# Validate Overall Design

**Phase**: 1 - Architecture Design  
**Purpose**: Validate Overall Design (DESIGN.md) completeness and structure

---

## Prerequisites

- `architecture/DESIGN.md` exists and has content
- DML specification directory exists (format per adapter)
- API contract specification directory exists (format per adapter)

## Input Parameters

None (validates current architecture)

---

## Requirements

### 1. Verify DESIGN.md Existence and Size

**Requirement**: Ensure Overall Design document exists with adequate content

**Required State**:
- File `architecture/DESIGN.md` exists
- File contains ≥200 lines (recommended: 500-2000 lines)
- File is not empty or placeholder-only

**Expected Outcome**: DESIGN.md present with substantial content

**Validation Criteria**:
- File `architecture/DESIGN.md` exists
- Line count ≥200 lines
- Content beyond basic template structure

---

### 2. Validate Section Structure

**Requirement**: Overall Design must contain all mandatory sections A-F

**Required Sections**:
- **Section A**: Vision & Capabilities
- **Section B**: Actors & Use Cases
- **Section C**: Domain Model Specification
- **Section D**: API Contract Specification
- **Section E**: Architecture
- **Section F**: Non-Functional Requirements

**Expected Outcome**: All 6 sections present and properly labeled

**Validation Criteria**:
- Section A present with heading `## A.`
- Section B present with heading `## B.`
- Section C present with heading `## C.`
- Section D present with heading `## D.`
- Section E present with heading `## E.`
- Section F present with heading `## F.`
- Total: 6 sections found

---

### 3. Validate Section A Content

**Requirement**: Section A must define system vision and core capabilities

**Required Content**:
- System vision description (what the system does, why it exists)
- Core capabilities list (main functional areas)
- Clear articulation of system purpose

**Expected Outcome**: Section A provides strategic context

**Validation Criteria**:
- Vision subsection present
- Capabilities subsection present with list
- Content substantive (not placeholders)

---

### 4. Validate Section B Content

**Requirement**: Section B must identify all actors and their use cases

**Required Content**:
- Actor definitions (who interacts with system)
- Use case descriptions (what actors do)
- Actor-use case mappings

**Expected Outcome**: Section B defines user interactions

**Validation Criteria**:
- Actors subsection present with actor list
- Use Cases subsection present with use case list
- Each actor has defined role
- Each use case has description

---

### 5. Validate Section C Content

**Requirement**: Section C must define Domain Model formally

**Required Content**:
- Domain type specifications (format per adapter: GTS, CTI, or other formats)
- Link to DML directory
- Description of key domain types
- Type versioning approach

**Required Resources**:
- DML specification directory exists (location per adapter)

**Expected Outcome**: Section C establishes DML

**Validation Criteria**:
- Domain types formally specified
- Notation/format consistent (per adapter)
- DML directory exists
- Types align with system capabilities

---

### 6. Validate Section D Content

**Requirement**: Section D must document API contract formally

**Required Content**:
- API endpoint list (main endpoints)
- Authentication approach
- Link to API specification file(s)

**Required Resources**:
- API contract specification file(s) exist (format per adapter: GTS, CTI, OpenAPI, GraphQL Schema, gRPC, etc.)
- Specification is valid per chosen format

**Expected Outcome**: Section D defines API surface

**Validation Criteria**:
- API endpoints documented
- Authentication described
- API specification file(s) exist
- Specification file(s) valid per chosen format

---

### 7. Validate Section E Content

**Requirement**: Section E must describe system architecture

**Required Content**:
- High-level components (major system parts)
- Data model (entities and relationships)
- Security model (auth/authz approach)

**Expected Outcome**: Section E provides architectural view

**Validation Criteria**:
- Components subsection present
- Data model subsection present
- Security model subsection present
- Architecture coherent with capabilities (Section A)

---

### 8. Check Design Completeness

**Requirement**: Design must be complete without placeholders

**Prohibited Content**:
- TODO markers
- TBD (To Be Determined) placeholders
- FIXME comments
- Empty or stub sections

**Expected Outcome**: Design ready for feature development

**Validation Criteria**:
- No TODO/TBD/FIXME markers present
- All sections have real content (not just templates)
- Design decisions documented
- Requirements clear and actionable

---

### 9. Validate Domain Type Identifier Format

**Requirement**: Domain type references must use complete, consistent notation

**Required Format** (per adapter):
- Must include namespace/module identifier
- Must include type name
- Must include version
- Format defined by adapter (e.g., `gts.namespace.type.v1~` for GTS adapter)

**Prohibited Format**:
- Short form without namespace
- Missing version information
- Inconsistent notation within same design

**Expected Outcome**: All type references follow project standard

**Validation Criteria**:
- All type references use adapter-defined format
- Format includes namespace, type name, and version
- No short-form identifiers present
- Notation consistent throughout document

**Note**: Namespace conventions defined in project adapter documentation

---

### 10. Check for Prohibited Extra Sections

**Requirement**: Design must not contain sections beyond allowed structure

**Allowed Sections**:
- Section A: Business Context
- Section B: Requirements & Principles  
- Section C: Technical Architecture
- Section D: Project-Specific Details (optional, not validated)
- Section E: (reserved, not used in Overall Design)
- Section F: (reserved, not used in Overall Design)
- Section G: (reserved, not used in Overall Design)

**Prohibited Sections**:
- Section H and beyond (H, I, J, K, etc.)
- Any sections after Section G

**Expected Outcome**: Design follows FDD section structure strictly

**Validation Criteria**:
- No sections labeled H or beyond exist
- Only A-D present (E-G reserved for future use)
- Section D is optional but allowed
- All content fits within allowed sections

**Note**: Section D is for project-specific details not covered by FDD core validation

---

## Completion Criteria

Overall Design validation is complete when:

- [ ] DESIGN.md exists with ≥200 lines
- [ ] Sections A-C present (D optional)
- [ ] Section A defines vision and capabilities
- [ ] Section B lists actors and use cases
- [ ] Section C defines technical architecture (domain model, API contracts, architecture overview)
- [ ] Section D (optional) contains project-specific details
- [ ] No sections H or beyond present
- [ ] No TODO/TBD/FIXME placeholders remain
- [ ] Domain type identifiers use complete format
- [ ] All required directories exist

---

## Common Challenges

### Challenge: Incomplete Sections

**Resolution**: Review FDD methodology for section requirements. Each section serves specific purpose in design. Complete all sections before proceeding.

### Challenge: Missing DML Directory

**Resolution**: Initialize DML structure as defined in project initialization workflow and adapter documentation. Required for type system integration.

### Challenge: Unclear Type Namespace/Notation

**Resolution**: Define project-specific type notation in adapter documentation. Use consistent namespace and notation across all type references. Follow adapter's conventions for type identification.

---

## Next Activities

After validation succeeds:

1. **Generate Features**: Execute feature generation workflow
   - Analyzes capabilities from Section A
   - Creates feature breakdown
   - Establishes dependency graph
   - Generates init

2. **Develop Diagrams**: Create visual documentation
   - System architecture overview
   - Data model diagram
   - Component interaction flows

3. **Refine Design**: If validation reveals gaps
   - Complete missing content
   - Clarify ambiguous sections
   - Re-validate

---

## References

- **Methodology**: `../AGENTS.md` - Overall Design requirements
- **Next Workflow**: `03-init-features.md`
