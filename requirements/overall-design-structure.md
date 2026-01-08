# Technical Design (DESIGN.md) Structure Requirements

**MUST read and follow**: `../workflows/design.md`

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
- From BUSINESS.md: `@/architecture/DESIGN.md` or `@DESIGN.md`
- To BUSINESS.md: `@/architecture/BUSINESS.md` or `@BUSINESS.md`
- To ADR.md: `@/architecture/ADR.md` or `@ADR.md`

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

**Content requirements**:
- Each functional requirement must have unique FDD ID
- Each use case must have unique FDD ID
- Each non-functional requirement category must have unique FDD ID
- Each constraint must have unique FDD ID
- Each requirement: clear, testable, necessary
- Principles: actionable, not generic platitudes

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

**⚠️ CRITICAL**: Domain model MUST be in machine-readable format
- ✅ Valid: GTS schemas, JSON Schema, OpenAPI, TypeScript types
- ❌ Invalid: Plain English descriptions, diagrams only

**Reference Requirements**:
- **Domain Model files**: Must be clickable links to actual schema/type files
  - Format: `@/path/to/domain-model-file` or markdown links
  - Example: `@/gts/user.gts`, `@/schemas/project.json`
- All domain model references must be verifiable and navigable

#### C.3: API Contracts
- **Technology** - Specify format (REST/OpenAPI, GraphQL, gRPC, CLISPEC)
- **Location** - Path to API contract files
- **Endpoints overview** - List main API surfaces

**⚠️ CRITICAL**: API contracts MUST be in machine-readable format
- ✅ Valid: OpenAPI spec, GraphQL schema, CLISPEC, proto files
- ❌ Invalid: Plain English descriptions, curl examples only

**Reference Requirements**:
- **API Spec files**: Must be clickable links to actual specification files
  - Format: `@/path/to/api-spec-file` or markdown links
  - Example: `@/openapi/users.yaml`, `@/spec/CLI/commands.clispec`
- All API contract references must be verifiable and navigable

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

1. **File exists and has adequate content**
   - File `architecture/DESIGN.md` exists
   - File contains ≥200 lines (recommended: 500-2000 lines)
   - File is not empty or placeholder-only

### Structure Validation

1. **All required sections present**
   - Section A with all subsections
   - Section B with all subsections
   - Section C with all subsections (C.1-C.5)
   - Section D optional (project-specific details, not validated)

2. **Section order correct**
   - A → B → C → D (in this exact order)
   - Section D may be omitted

3. **No prohibited sections**
   - No top-level sections E or beyond (E, F, G, H, etc.)
   - Only A-D allowed at top level (D is optional)
   - Section C has exactly 5 subsections (C.1-C.5)

4. **Markdown formatting valid**
   - Headers use proper levels (## for A-D, ### for C.1-C.5)
   - No malformed markdown

### Content Validation

1. **Domain Model accessible**
   - Files at specified location exist
   - Files are in specified format (parseable)
   - No broken references

2. **API Contracts accessible**
   - Files at specified location exist
   - Files are in specified format (parseable)
   - No broken references

3. **Component diagram present**
   - At least one diagram in Section C.1
   - Can be embedded image, Mermaid code, or ASCII art

4. **No placeholders remain**
   - No TODO markers
   - No TBD (To Be Determined) placeholders
   - No FIXME comments
   - No empty or stub sections
   - All sections have substantive content

5. **Domain type identifiers use complete format**
   - Must include namespace/module identifier
   - Must include type name
   - Must include version
   - Format defined by adapter (e.g., `gts.namespace.type.v1` for GTS)
   - No short-form identifiers without namespace
   - Notation consistent throughout document

6. **Requirement IDs follow FDD format**
   - All functional requirements have unique IDs with `**ID**: \`fdd-{project-name}-req-{short-name}\`` format
   - All principle IDs follow `**ID**: \`fdd-{project-name}-principle-{name}\`` format
   - All non-functional requirement categories have unique IDs with `**ID**: \`fdd-{project-name}-nfr-{name}\`` format
   - All constraints have unique IDs with `**ID**: \`fdd-{project-name}-constraint-{name}\`` format
   - All IDs use kebab-case (lowercase with hyphens)
   - IDs are unique within their category
   - Each ID value must be wrapped in backticks (\`...\`)

7. **Cross-references are valid**
   - References to BUSINESS.md elements (actors, capabilities) use valid IDs
   - References to domain model files are valid paths
   - References to API contract files are valid paths
   - All `@/path/to/file` references point to existing files

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
1. Structure completeness (sections, subsections)
2. Domain model accessibility (files exist, parseable)
3. API contracts accessibility (files exist, parseable)
4. Content substantiveness (no empty sections)

**Report format**:
- Score: X/100 (must be ≥90)
- Completeness: X% (must be 100%)
- Issues: List of missing/invalid items
- Recommendations: What to fix

**Scoring**:
- Structure (30 points): All sections present
- Domain Model (25 points): Valid machine-readable format
- API Contracts (25 points): Valid machine-readable format
- Content Quality (20 points): Substantive, no placeholders

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
