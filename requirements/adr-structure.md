# Architecture Decision Records (ADR) Structure Requirements

**ALWAYS open and follow**: `../workflows/adr.md`

**This file defines**: Structure only (WHAT to create)  
**Workflow defines**: Process (HOW to create)

⚠️ **Do NOT use this file alone. Execute the workflow, not just the structure.**

---

**Version**: 1.0  
**Purpose**: Defines structure and validation criteria for Architecture Decision Records documentation

**Scope**: This document specifies required structure for `architecture/ADR.md`

**Format**: MADR (Markdown Any Decision Records) format with FDD extensions

---

## File Overview

**Purpose**: Track all significant architectural decisions and their rationale

**Location**: `architecture/ADR.md` (separate from DESIGN.md)

**Format**: Industry-standard MADR (Markdown Any Decision Records)

**Reference from DESIGN.md**: `@/architecture/ADR.md`

**Reference from BUSINESS.md**: `@/architecture/ADR.md`

---

## ADR Format

Each ADR follows the MADR format with FDD extensions:

### ADR Header

```markdown
## ADR-NNNN: Decision Title

**Date**: YYYY-MM-DD  
**Status**: [Proposed | Accepted | Deprecated | Superseded]  
**Deciders**: Names or team  
**Technical Story**: Optional ticket/issue reference
```

**Status values**:
- **Proposed**: Under discussion
- **Accepted**: Decision made and implemented
- **Deprecated**: No longer recommended but not superseded
- **Superseded**: Replaced by another ADR (reference ADR-XXXX)

### Required Sections

#### 1. Context and Problem Statement

**Purpose**: Describe the problem or opportunity that requires a decision

**Content**:
- What is the issue or situation?
- What factors are driving this decision?
- What constraints exist?

**Example**:
```markdown
### Context and Problem Statement

The Analytics module needed a standardized query protocol that supports:
- Complex filtering, sorting, and pagination
- Field projection and selection
- Metadata discovery
- Industry-standard compatibility
```

#### 2. Decision Drivers

**Purpose**: List factors influencing the decision

**Content**:
- Technical requirements
- Business requirements
- Quality attributes (performance, scalability, etc.)
- Constraints (budget, timeline, skills)

**Example**:
```markdown
### Decision Drivers

- Need standardized query language that external systems can understand
- Must support complex filtering and sorting operations
- Require metadata endpoint for schema discovery
- Industry adoption and tooling ecosystem
```

#### 3. Considered Options

**Purpose**: List alternatives that were evaluated

**Content**:
- Option 1 (chosen) - brief description
- Option 2 - brief description
- Option 3 - brief description
- ...

**Format**:
```markdown
### Considered Options

1. **OData v4** (chosen)
2. **GraphQL**
3. **Custom REST query DSL**
```

#### 4. Decision Outcome

**Purpose**: State the decision and explain why

**Content**:
- **Chosen option**: Name of selected option
- **Rationale**: Why this option was chosen
- **Positive Consequences**: Benefits of this decision
- **Negative Consequences**: Drawbacks or trade-offs

**Example**:
```markdown
### Decision Outcome

**Chosen option**: "OData v4"

**Rationale**: OData v4 provides mature standard for querying data with 
built-in support for filtering, sorting, pagination, and field selection. 
Wide industry adoption ensures compatibility with external tools.

**Positive Consequences**:
- Standard protocol understood by many external systems
- Built-in metadata discovery via `$metadata` endpoint
- Rich query capabilities

**Negative Consequences**:
- OData query syntax can be complex for users
- Additional implementation overhead vs custom DSL
```

### Optional Sections

#### 5. Pros and Cons of the Options (Optional)

**Purpose**: Detailed analysis of each option

**Format per option**:
```markdown
#### Option 1: Name

**Pros**:
- Pro 1
- Pro 2

**Cons**:
- Con 1
- Con 2
```

#### 6. Links (Optional)

**Purpose**: References to related resources

**Content**:
- Links to related ADRs
- External documentation
- Technical specifications
- Discussion threads

---

## FDD Extensions

### Related Design Elements (REQUIRED)

**Purpose**: Link ADR to FDD design elements by their IDs

**Content**:
- **Actors**: List actor IDs affected by this decision
- **Capabilities**: List capability IDs affected by this decision
- **Requirements**: List requirement IDs affected by this decision
- **Principles**: List principle IDs affected by this decision

**Format**:
```markdown
### Related Design Elements

**Actors**:
- `fdd-analytics-actor-plugin-developer` - Develops custom datasource plugins
- `fdd-analytics-actor-query-plugin` - Executes queries against datasources

**Capabilities**:
- `fdd-analytics-capability-data-access` - Plugin-based datasource architecture
- `fdd-analytics-capability-query-execution` - Plugin-based query adapters

**Requirements**:
- `fdd-analytics-req-performance` - Query execution performance requirements
- `fdd-analytics-req-security` - Multi-tenant isolation and SecurityCtx

**Principles**:
- `fdd-analytics-principle-plugin-extensibility` - No service restart required
- `fdd-analytics-principle-gts-native` - All plugin communication via GTS
```

**Requirements**:
- All IDs wrapped in backticks: `\`fdd-...\``
- Each ID followed by brief description
- Reference valid IDs from BUSINESS.md and DESIGN.md
- At least one category must have ≥1 ID

---

## ADR Numbering

**Format**: ADR-NNNN (zero-padded 4 digits)

**Examples**: ADR-0001, ADR-0042, ADR-1234

**Rules**:
- Start with ADR-0001
- Increment sequentially
- Never reuse numbers
- Zero-padded to 4 digits

**Special ADRs**:
- **ADR-0001**: Always the initial architecture decision (required)

---

## File Structure

### Document Header

```markdown
# [Module Name] - Architecture Decision Records

**Module**: Module Name  
**Version**: 1.0  
**Last Updated**: YYYY-MM-DD

This document tracks all significant architectural decisions for the [Module Name] module.
```

### ADR Entries

ADRs are listed in **chronological order** (oldest first):

```markdown
---

## ADR-0001: Initial Architecture

[ADR content]

---

## ADR-0002: Second Decision

[ADR content]

---

## ADR-0003: Third Decision

[ADR content]
```

**Separator**: Use `---` between ADRs

---

## Validation Criteria

### File Validation

1. **File exists**
   - File `architecture/ADR.md` exists
   - File contains ≥1 ADR
   - File is not empty

2. **Document header**
   - Contains module name
   - Contains version
   - Contains last updated date

### ADR Structure Validation

1. **ADR numbering**
   - All ADRs numbered ADR-NNNN format
   - ADR-0001 exists (required)
   - Numbers are sequential
   - No gaps in numbering
   - All numbers unique

2. **Required sections present**
   - Context and Problem Statement
   - Decision Drivers
   - Considered Options
   - Decision Outcome
   - Related Design Elements (FDD extension)

3. **Status valid**
   - Status is one of: Proposed, Accepted, Deprecated, Superseded
   - If Superseded, references another ADR

4. **Date format**
   - Date in YYYY-MM-DD format
   - Date is valid

### Content Validation

1. **Context section**
   - Describes the problem clearly
   - ≥2 sentences

2. **Decision Drivers**
   - ≥2 drivers listed
   - Drivers are specific, not generic

3. **Considered Options**
   - ≥2 options listed
   - Chosen option marked
   - Options are distinct

4. **Decision Outcome**
   - Chosen option stated
   - Rationale provided (≥1 sentence)
   - Positive consequences listed (≥1)
   - Negative consequences listed (≥1)

5. **Related Design Elements (FDD)**
   - At least one category has ≥1 ID
   - All IDs wrapped in backticks
   - All IDs follow FDD format: `fdd-{project}-{type}-{name}`
   - Each ID has brief description

### Cross-Reference Validation

1. **FDD ID references**
   - All actor IDs exist in BUSINESS.md Section B
   - All capability IDs exist in BUSINESS.md Section C
   - All requirement IDs exist in DESIGN.md Section B
   - All principle IDs exist in DESIGN.md Section B

---

## Best Practices

### Writing ADRs

1. **Write ADRs when**:
   - Making significant architectural decisions
   - Choosing between multiple viable options
   - Establishing architectural constraints
   - Changing existing architecture
   - Making trade-offs between quality attributes

2. **Do NOT write ADRs for**:
   - Obvious or trivial decisions
   - Decisions that can be easily reversed
   - Implementation details
   - Coding standards or style choices

### Decision Quality

1. **Good Context**:
   - Specific problem statement
   - Clear constraints
   - Measurable drivers

2. **Good Options**:
   - ≥2 distinct alternatives
   - Each option viable
   - Trade-offs clear

3. **Good Rationale**:
   - Clear reasoning
   - References decision drivers
   - Acknowledges trade-offs
   - Honest about cons

### FDD Integration

1. **Link to design elements**:
   - Always include Related Design Elements section
   - Link to relevant actors, capabilities, requirements, principles
   - Use specific IDs, not generic references

2. **Update when**:
   - Implementing the decision (Status: Accepted)
   - Superseding with new ADR
   - Deprecating without replacement

3. **Cross-reference**:
   - Reference ADRs in DESIGN.md where relevant
   - Reference ADRs in feature designs
   - Use ADR number: ADR-NNNN

---

## Complete Example

```markdown
# Analytics - Architecture Decision Records

**Module**: Analytics  
**Version**: 1.0  
**Last Updated**: 2025-12-31

This document tracks all significant architectural decisions for the Analytics module.

---

## ADR-0001: Initial Analytics Architecture

**Date**: 2025-12-31  
**Status**: Accepted  
**Deciders**: Hyperspot Team  
**Technical Story**: Analytics module initialization

### Context and Problem Statement

The Hyperspot platform required a comprehensive analytics solution that could:
- Support multiple data sources without vendor lock-in
- Provide type-safe data visualization and querying
- Ensure complete tenant isolation in multi-tenant environment
- Scale horizontally while maintaining performance

### Decision Drivers

- **Type Safety**: Need compile-time and runtime type validation
- **Multi-Tenancy**: Complete tenant isolation is mandatory
- **Data Agnostic**: No vendor lock-in to specific DWH
- **Extensibility**: Plugin architecture for datasources
- **Performance**: Sub-second query response times

### Considered Options

1. **GTS + Plugin Architecture** (chosen)
2. **Monolithic with Built-in DWH**
3. **Microservices with Dedicated Query Service**

### Decision Outcome

**Chosen option**: "GTS + Plugin Architecture"

**Rationale**: GTS provides runtime type validation with plugin architecture 
allowing adding datasources without service restart. SecurityCtx enforced at 
compilation via Secure ORM ensures tenant isolation.

**Positive Consequences**:
- No vendor lock-in
- Type-safe communication through GTS
- Plugin registration without service restart
- Complete tenant isolation via SecurityCtx

**Negative Consequences**:
- More complex architecture than monolithic
- Plugin development requires understanding of GTS
- Query performance depends on external sources

### Related Design Elements

**Actors**:
- `fdd-analytics-actor-plugin-developer` - Develops custom datasource plugins
- `fdd-analytics-actor-query-plugin` - Executes queries against datasources

**Capabilities**:
- `fdd-analytics-capability-data-access` - Plugin-based datasource architecture
- `fdd-analytics-capability-extensibility` - Dynamic datasource registration

**Requirements**:
- `fdd-analytics-req-performance` - Query execution performance
- `fdd-analytics-req-security` - Multi-tenant isolation

**Principles**:
- `fdd-analytics-principle-plugin-extensibility` - No service restart required
- `fdd-analytics-principle-gts-native` - All plugin communication via GTS
- `fdd-analytics-principle-data-agnostic` - No built-in DWH
```

---

## References

- **MADR**: https://adr.github.io/madr/
- **ADR Organization**: https://github.com/joelparkerhenderson/architecture-decision-record
- **FDD Design Elements**: Reference BUSINESS.md and DESIGN.md for ID formats
