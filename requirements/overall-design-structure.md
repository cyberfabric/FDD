# Technical Design (DESIGN.md) Structure Requirements

**ALWAYS open and follow**: `../workflows/design.md`
**ALWAYS open and follow**: `requirements.md`
**ALWAYS open and follow**: `core.md` WHEN editing this file

**This file defines**: Structure only (WHAT to create)  
**Workflow defines**: Process (HOW to create)

⚠️ **Do NOT use this file alone. Execute the workflow, not just the structure.**

---

**Version**: 2.0  
**Purpose**: Defines structure and validation criteria for Technical Design documentation

**Scope**: This document specifies required structure for `architecture/DESIGN.md`

**Related specifications**:
- `business-context-structure.md` - For BUSINESS.md structure
- `adr-structure.md` - For ADR.md structure

**Size limits**:
- Recommended: ≤1500 lines
- Hard limit: ≤2000 lines

---

## File Overview

**Purpose**: Technical requirements, principles, and architecture

**Location**: `architecture/DESIGN.md`

**Contains**: 
- Section A: Architecture Overview (architectural vision + architecture layers)
- Section B: Requirements & Principles
- Section C: Technical Architecture
- Section D: Additional Context (optional)

**References**:
- From BUSINESS.md: [DESIGN.md](DESIGN.md)
- To BUSINESS.md: [BUSINESS.md](BUSINESS.md)
- To ADR.md: [ADR.md](ADR.md)

---

## DESIGN.md Structure

### Section A: Architecture Overview

**Purpose**: Architectural vision, high-level overview, and layered architecture

**Content**:
- **Architectural Vision**: 2-3 paragraphs describing the technical approach, key architectural decisions, and design philosophy
- **Architecture layers**: Visual diagram + description of system layers (Presentation, Application, Domain, Infrastructure, etc.)
  - Layer diagram (draw.io, Mermaid, or embedded image)
  - Description of each layer, its responsibilities, and interactions

**Required**:
- Architecture diagram (draw.io, Mermaid, or embedded image)
- Clear layer definitions and boundaries
- Technology stack per layer

---

### Section B: Requirements & Principles

**Purpose**: Functional requirements, design principles, constraints

**Required subsections**:
1. **Functional Requirements** - What system must do
2. **Non-Functional Requirements** - Performance, scalability, etc.
3. **Design Principles** - Architectural guidelines
4. **Constraints** - Technical/business limitations

**Functional Requirement ID Format**: `fdd-{project-name}-req-{short-name}`
- **Components**:
  - `fdd-` - Prefix indicating FDD methodology
  - `{project-name}` - Project name in kebab-case
  - `-req-` - Requirement indicator
  - `{short-name}` - Short descriptive name in kebab-case (2-4 words)
- **Example**: `fdd-payment-system-req-multi-tenant`, `fdd-analytics-req-real-time-data`
- **Usage**: Each requirement must have `**ID**: {id}` before requirement statement
- **Format in document**: `**ID**: fdd-project-req-name`
- **Note**: Can coexist with legacy REQ-N numbering, but FDD format is preferred

**Use Case ID Format**: `fdd-{project-name}-usecase-{usecase-name}`
- **Components**:
  - `fdd-` - Prefix indicating FDD methodology
  - `{project-name}` - Project name in kebab-case
  - `-usecase-` - Use case indicator
  - `{usecase-name}` - Use case name in kebab-case (2-4 words)
- **Example**: `fdd-payment-system-usecase-process-payment`, `fdd-analytics-usecase-generate-report`
- **Usage**: Each use case must have `**ID**: {id}` before use case description
- **Format in document**: `**ID**: fdd-project-usecase-name`

**Principle ID Format**: `fdd-{project-name}-principle-{principle-name}`
- **Components**:
  - `fdd-` - Prefix indicating FDD methodology
  - `{project-name}` - Project name in kebab-case
  - `-principle-` - Principle indicator
  - `{principle-name}` - Principle name in kebab-case (2-4 words)
- **Example**: `fdd-payment-system-principle-security-first`, `fdd-analytics-principle-plugin-based`
- **Usage**: Each principle must have `**ID**: {id}` as first line after principle heading
- **Format in document**: `**ID**: \`fdd-project-principle-name\`` (after #### Principle Name)

**Non-Functional Requirement ID Format**: `fdd-{project-name}-nfr-{nfr-name}`
- **Components**:
  - `fdd-` - Prefix indicating FDD methodology
  - `{project-name}` - Project name in kebab-case
  - `-nfr-` - Non-functional requirement indicator
  - `{nfr-name}` - NFR category name in kebab-case (1-3 words)
- **Example**: `fdd-payment-system-nfr-performance`, `fdd-analytics-nfr-scalability`, `fdd-cli-nfr-security`
- **Usage**: Each NFR category must have `**ID**: {id}` as first line after NFR heading
- **Format in document**: `**ID**: \`fdd-project-nfr-name\`` (in Section C.5)

**Constraint ID Format**: `fdd-{project-name}-constraint-{constraint-name}`
- **Components**:
  - `fdd-` - Prefix indicating FDD methodology
  - `{project-name}` - Project name in kebab-case
  - `-constraint-` - Constraint indicator
  - `{constraint-name}` - Constraint name in kebab-case (2-4 words)
- **Example**: `fdd-payment-system-constraint-api-dependency`, `fdd-analytics-constraint-data-retention`
- **Usage**: Each constraint must have `**ID**: {id}` as first line after constraint heading
- **Format in document**: `**ID**: \`fdd-project-constraint-name\`` (in Section B.4)

**ADR ID Format**: `fdd-{project-name}-adr-{decision-name}`
- **Components**:
  - `fdd-` - Prefix indicating FDD methodology
  - `{project-name}` - Project name in kebab-case
  - `-adr-` - Architecture Decision Record indicator
  - `{decision-name}` - Decision name in kebab-case (2-4 words describing the decision)
- **Example**: `fdd-acronis-mcp-adr-python-django`, `fdd-payment-system-adr-event-sourcing`
- **Usage**: Each ADR in ADR.md must have `**ID**: {id}` as first line after ADR heading
- **Format in document**: `**ID**: \`fdd-project-adr-decision-name\`` (in ADR.md)
- **Legacy format**: ADR-XXXX is acceptable during migration, but text-based FDD format preferred for clarity

**Content requirements**:
- Each functional requirement must have unique FDD ID
- Each use case must have unique FDD ID
- Each non-functional requirement category must have unique FDD ID
- Each constraint must have unique FDD ID
- Each requirement: clear, testable, necessary
- Principles: actionable, not generic platitudes

**Traceability Field Requirements**:

Each functional requirement (FR) MUST include the following fields:

1. **Capabilities**: `**Capabilities**: \`{capability-id-1}\`, \`{capability-id-2}\``
   - Lists capability IDs from BUSINESS.md Section C
   - Example: `**Capabilities**: \`fdd-acronis-mcp-capability-workflow-mgmt\``
   - Multiple: `**Capabilities**: \`fdd-acronis-mcp-capability-doc-persistence\`, \`fdd-acronis-mcp-capability-resource-access\``
   - MANDATORY for all FR requirements

2. **Use Cases** (optional): `**Use Cases**: \`{usecase-id-1}\`, \`{usecase-id-2}\``
   - Lists use case IDs from BUSINESS.md Section D
   - Example: `**Use Cases**: \`fdd-acronis-mcp-usecase-init-project\`, \`fdd-acronis-mcp-usecase-project-workflow\``
   - Only include if requirement directly implements a use case

3. **Actors**: `**Actors**: \`{actor-id-1}\`, \`{actor-id-2}\``
   - Lists actor IDs from BUSINESS.md Section B
   - Example: `**Actors**: \`fdd-acronis-mcp-actor-developer\`, \`fdd-acronis-mcp-actor-ai-assistant\``
   - Actor IDs MUST match those listed in the referenced capability
   - Shows WHO uses each requirement's functionality
   - MANDATORY for all FR requirements

4. **ADRs** (optional): `**ADRs**: \`{adr-id-1}\`, \`{adr-id-2}\``
   - Lists ADR IDs from ADR.md that justify or constrain this requirement
   - Example: `**ADRs**: \`fdd-acronis-mcp-adr-0001\`, \`fdd-acronis-mcp-adr-0003\``
   - Legacy format: `ADR-0001` acceptable during migration
   - Include when requirement is directly influenced by architectural decisions
   - Common for: Principles, Constraints, NFRs, technology choices

---

### Section C: Technical Architecture

**Purpose**: Detailed technical specifications, components, APIs, data models

**Required subsections**:

#### C.1: Domain Model
- **Component diagram** (draw.io, Mermaid, or ASCII)
- **Component descriptions** - Purpose of each component
- **Component interactions** - How components communicate

**Note**: Capabilities are defined in Section A.3, not here

#### C.2: Domain Model
- **Technology** - Specify format (GTS, JSON Schema, OpenAPI, etc.)
- **Location** - Path to domain model files
- **Core entities** - List main domain objects
- **Relationships** - Entity relationships overview

**CRITICAL**: Domain model MUST be in machine-readable format
- Valid: GTS schemas, JSON Schema, OpenAPI, TypeScript types
- Invalid: Plain English descriptions, diagrams only

**Reference Requirements**:
- **Domain Model files**: Must be clickable Markdown links to actual schema/type files
  - Valid formats:
    - Relative path: `[user.gts](../gts/user.gts)`
    - Absolute path: `[project.json](/schemas/project.json)`
  - Invalid formats:
    - Inline code: `\`../gts/user.gts\`` (not clickable)
    - Plain text: `../gts/user.gts` (not clickable)
    - Custom notation: `@/schemas/project.json` (IDE-specific, not standard Markdown)

#### C.3: API Contracts
- **Technology** - Specify format (REST/OpenAPI, GraphQL, gRPC, CLISPEC)
- **Location** - Path to API contract files
- **Endpoints overview** - List main API surfaces

**CRITICAL**: API contracts MUST be in machine-readable format
- Valid: OpenAPI spec, GraphQL schema, CLISPEC, proto files
- Invalid: Plain English descriptions, curl examples only

**Reference Requirements**:
- **API Spec files**: Must be clickable Markdown links to actual specification files
  - Valid formats:
    - Relative path: `[users.yaml](../openapi/users.yaml)`
    - Absolute path: `[commands.clispec](/spec/CLI/commands.clispec)`
  - Invalid formats:
    - Inline code: `\`../openapi/users.yaml\`` (not clickable)
    - Plain text: `../openapi/users.yaml` (not clickable)
    - Custom notation: `@/spec/CLI/commands.clispec` (IDE-specific, not standard Markdown)

#### C.4: Security Model
- Authentication approach
- Authorization approach  
- Data protection
- Security boundaries

**Note**: Can be "No security" for CLI tools, internal systems

#### C.5: Non-Functional Requirements
- Performance requirements
- Scalability requirements
- Reliability/Availability requirements
- Other quality attributes

**Note**: Include NFRs relevant to project type

---

### Section D: Additional Context (OPTIONAL)

**Purpose**: Architect notes, technical rationale, implementation considerations, or other technical details not covered by core FDD structure

**Content** (examples):
- Technology selection rationale
- Performance optimization notes
- Scalability considerations
- Security implementation details
- Integration patterns and trade-offs
- Migration strategy technical details
- Deployment architecture notes
- Infrastructure requirements
- Technical debt notes
- Future technical improvements
- Any other technical context

**Note**: This section is optional and not validated by FDD. Use it to capture important technical information that doesn't fit into the standard FDD structure.

**Format**: Free-form, no specific structure required

---

### Section D: Project-Specific Details (OPTIONAL)

**Purpose**: Additional project context not covered by core FDD structure

**Content**:
- Integration requirements
- Performance constraints
- Compliance requirements
- Migration notes
- Deployment context
- Any other project-specific information

**Note**: This section is optional and only included if project has specific context to document. Not validated by FDD core validation.

---

## Validation Criteria

### File-Level Validation

1. **File exists**
   - File `architecture/DESIGN.md` exists
   - File contains ≥200 lines (recommended: 500-2000 lines)

### Structure Validation

1. **All required sections present**
   - Section A with all subsections
   - Section B with all subsections
   - Section C with all subsections (C.1-C.5)
   - Section D optional (project-specific details, not validated)

2. **Section order correct**
   - A → B → C → D
   - Section D may be omitted

3. **No prohibited sections**
   - No top-level sections E or beyond (E, F, G, H, etc.)
   - Only A-D allowed at top level (D is optional)
   - Section C has exactly 5 subsections (C.1-C.5)

4. **Headers use proper levels**
   - Headers use proper levels (## for A-D, ### for C.1-C.5)

### Content Validation

1. **Domain Model accessible**
   - Files at specified location exist
   - Files are in specified format (parseable)

2. **API Contracts accessible**
   - Files at specified location exist
   - Files are in specified format (parseable)

3. **Component diagram present**
   - At least one diagram in Section C.1
   - Can be embedded image, Mermaid code, or ASCII art

4. **Domain type identifiers use complete format**
   - Must include namespace/module identifier
   - Must include type name
   - Must include version
   - Format defined by adapter (e.g., `gts.namespace.type.v1` for GTS)
   - No short-form identifiers without namespace
   - Notation consistent throughout document

5. **Requirement IDs follow FDD format**
   - All functional requirements have unique IDs with `**ID**: \`fdd-{project-name}-req-{short-name}\`` format
   - All principle IDs follow `**ID**: \`fdd-{project-name}-principle-{name}\`` format
   - All non-functional requirement categories have unique IDs with `**ID**: \`fdd-{project-name}-nfr-{name}\`` format
   - All constraints have unique IDs with `**ID**: \`fdd-{project-name}-constraint-{name}\`` format

6. **Cross-references are valid**
   - References to BUSINESS.md elements (actors, capabilities) use valid IDs
   - References to domain model files are valid paths
   - References to API contract files are valid paths

### ID Traceability Validation

**CRITICAL**: BUSINESS.md → DESIGN.md traceability

**ID Type Catalog**:

**BUSINESS.md contains**:
- **Actors** (13 IDs): `fdd-{project}-actor-{name}` (Section B) - Referenced in DESIGN.md Actors field
- **Capabilities** (7 IDs): `fdd-{project}-capability-{name}` (Section C) - MUST be in DESIGN.md Capabilities field
- **Use Cases** (2 IDs): `fdd-{project}-usecase-{name}` (Section D) - MUST be in DESIGN.md Use Cases field
- **Success Criteria**: Optional reference in NFRs

**ADR.md contains**:
- **Architecture Decision Records** (variable count): `fdd-{project}-adr-{number}` or `ADR-{number}` (legacy)
- Referenced in DESIGN.md ADRs field for Principles, Constraints, NFRs
- MUST be covered by at least one DESIGN.md requirement (100% coverage required)

**DESIGN.md must reference**: All capabilities and use cases from BUSINESS.md; ADRs SHOULD be referenced where applicable

---

**Traceability Rules**:

1. **Capability Coverage (MANDATORY)**:
   - Every capability ID from BUSINESS.md Section C MUST be referenced in at least one DESIGN.md requirement's **Capabilities** field
   - Typically in Functional Requirements (FR-XXX)
   - No orphaned capabilities (capabilities without technical requirements)
   - Format: `**Capabilities**: \`{capability-id}\``

2. **Use Case Coverage (MANDATORY)**:
   - Every use case ID from BUSINESS.md Section D MUST be referenced in at least one DESIGN.md requirement's **Use Cases** field
   - Typically in Functional Requirements (FR-XXX)
   - No orphaned use cases (use cases without technical requirements)
   - Format: `**Use Cases**: \`{usecase-id-1}\`, \`{usecase-id-2}\``

3. **Actor References (MANDATORY)**:
   - Actor IDs from BUSINESS.md Section B MUST be referenced in DESIGN.md Functional Requirements
   - Each FR requirement MUST have `**Actors**:` field listing actor IDs
   - Actor IDs MUST match those listed in the referenced capability from BUSINESS.md Section C
   - Format: `**Actors**: \`{actor-id-1}\`, \`{actor-id-2}\``
   - All actors from BUSINESS.md SHOULD appear in at least one requirement (validates WHO uses the system)

4. **ADR Coverage (MANDATORY)**:
   - ADR IDs from ADR.md MUST be referenced in DESIGN.md requirements
   - Referenced in Principles, Constraints, NFRs via `**ADRs**:` field
   - Format: `**ADRs**: \`{adr-id-1}\`, \`{adr-id-2}\`` or `ADR-0001, ADR-0002` (legacy)
   - All ADRs from ADR.md MUST appear in at least one DESIGN.md requirement
   - Validates that architectural decisions are reflected in design
   - No orphaned ADRs allowed (ADRs without corresponding design requirements)

55. **Field Structure**:
   - **Capabilities**: `**Capabilities**: \`{id1}\`, \`{id2}\`` (one or more capability IDs from BUSINESS.md Section C)
   - **Use Cases**: `**Use Cases**: \`{uc-id1}\`, \`{uc-id2}\`` (optional, only if applicable, from BUSINESS.md Section D)
   - **Actors**: `**Actors**: \`{actor-id1}\`, \`{actor-id2}\`` (one or more actor IDs from BUSINESS.md Section B, matching capability)
   - **ADRs**: `**ADRs**: \`{adr-id1}\`, \`{adr-id2}\`` (optional, for Principles/Constraints/NFRs, from ADR.md)
   - Use exact IDs from BUSINESS.md and ADR.md (no paraphrasing)

6. **Optional References**:
   - Non-Functional Requirements: May reference Success Criteria from BUSINESS.md Section A
   - Principles/Constraints: Should reference ADRs via ADRs field
   - All document references use full links: `[BUSINESS.md](BUSINESS.md)`, `[ADR.md](ADR.md)`

**Validation Checks**:
- ✅ Every capability ID from BUSINESS.md Section C appears in at least one FR requirement's **Capabilities** field
- ✅ Every use case ID from BUSINESS.md Section D appears in at least one FR requirement's **Use Cases** field
- ✅ No orphaned capabilities (business capabilities without technical requirements)
- ✅ No orphaned use cases (business flows without technical requirements)
- ✅ All capability IDs in Capabilities fields are valid (reference existing BUSINESS.md Section C IDs)
- ✅ All use case IDs in Use Cases fields are valid (reference existing BUSINESS.md Section D IDs)
- ✅ Every FR requirement has Capabilities and Actors fields
- ✅ All actor IDs in Actors fields are valid (reference existing BUSINESS.md Section B IDs)
- ✅ Actor IDs match those in the referenced capability from BUSINESS.md Section C
- ⚠️ All actors from BUSINESS.md SHOULD appear in at least one requirement (coverage optional)
- ✅ All ADRs from ADR.md MUST appear in at least one DESIGN.md requirement (100% coverage required)
- ✅ No orphaned ADRs (architectural decisions without design requirements)
- ✅ All ADR IDs in ADRs fields are valid (reference existing ADR.md records)

**Example Traceability Chain**:
```
BUSINESS.md Section C:
├─ Capability: fdd-acronis-mcp-capability-workflow-mgmt
├─ Capability: fdd-acronis-mcp-capability-design-validation
├─ Capability: fdd-acronis-mcp-capability-feature-design
├─ Capability: fdd-acronis-mcp-capability-doc-generation
├─ Capability: fdd-acronis-mcp-capability-document-persistence
├─ Capability: fdd-acronis-mcp-capability-resource-access
└─ Capability: fdd-acronis-mcp-capability-project-management

BUSINESS.md Section D:
├─ Use Case: fdd-acronis-mcp-usecase-init-project
└─ Use Case: fdd-acronis-mcp-usecase-project-workflow

DESIGN.md Section B.1 (Functional Requirements):
├─ FR-001: Source: Capability `workflow-mgmt`
├─ FR-002: Source: Capability `design-validation`
├─ FR-003: Source: Capability `document-persistence`
├─ FR-004: Source: Capability `document-persistence`
├─ FR-006: Source: Capability `resource-access`
└─ FR-007: Source: Capability `project-management`, Use Cases `init-project`, `project-workflow`

⚠️ Missing coverage: `feature-design`, `doc-generation` capabilities
```

**Scoring Impact**:
- Missing capability coverage: **-15 points** per orphaned capability
- Missing use case coverage: **-15 points** per orphaned use case  
- Orphaned ADR (not referenced in any requirement): **-15 points** per ADR (MANDATORY coverage)
- Missing Capabilities field in FR: **-10 points** per requirement
- Missing Actors field in FR: **-10 points** per requirement
- Invalid capability ID: **-5 points** per invalid ID
- Invalid use case ID: **-5 points** per invalid ID
- Invalid ADR ID: **-5 points** per invalid ADR reference
- Invalid actor ID: **-3 points** per invalid actor reference
- Actor mismatch with capability: **-5 points** per requirement

---

## Output Requirements

### For Generator (Workflow 01)

**Generate**:
- File at `architecture/DESIGN.md`
- All required sections with headers
- Placeholder content for each subsection
- Comments guiding what to fill

**Template markers**:
- Use `<!-- TODO: ... -->` for sections needing input
- Use `[DESCRIBE: ...]` for inline placeholders

### For Validator (Workflow 02)

**Validate**:
1. Structure completeness
2. Domain model accessibility
3. API contracts accessibility

**Scoring**:
- Structure (30 points): All sections present
- Domain Model (25 points): Valid machine-readable format
- API Contracts (25 points): Valid machine-readable format
- Content Quality (20 points)

---

## Examples

### Valid Domain Model Specification

```markdown
#### C.2: Domain Model

**Technology**: GTS (Global Type System) + JSON Schema

**Location**: `gts/`

**Core entities**:
- `user` - User account and profile
- `project` - FDD project container
- `feature` - Individual feature specification

**Relationships**:
- User owns multiple Projects
- Project contains multiple Features
```

### Invalid Domain Model Specification

```markdown
#### C.2: Domain Model

We use a standard entity-relationship model with users, projects, and features.
Users can own projects and projects contain features.
```
❌ No technology specified, no file location, not machine-readable

---

## References

**Workflows using this**:
- `workflows/01-init-project.md` - Generate DESIGN.md
- `workflows/02-validate-architecture.md` - Validate DESIGN.md

**Related requirements**:
- `business-context-structure.md` - BUSINESS.md structure
- `adr-structure.md` - ADR.md structure
- `feature-design-structure.md` - Feature DESIGN.md structure
