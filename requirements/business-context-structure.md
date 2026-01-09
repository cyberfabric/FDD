# Business Context Structure Requirements

**ALWAYS open and follow**: `../workflows/business-context.md`

**This file defines**: Structure only (WHAT to create)  
**Workflow defines**: Process (HOW to create)

⚠️ **Do NOT use this file alone. Execute the workflow, not just the structure.**

---

**Version**: 1.0  
**Purpose**: Defines structure and validation criteria for Business Context documentation

**Scope**: This document specifies required structure for `architecture/BUSINESS.md`

**Size limits**:
- Recommended: ≤500 lines
- Hard limit: ≤1000 lines

---

## File Overview

**Purpose**: Business context, actors, and system capabilities

**Location**: `architecture/BUSINESS.md`

**Contains**: 
- Section A: Vision
- Section B: Actors
- Section C: Capabilities
- Section D: Additional Context (optional)

**Reference from DESIGN.md**: `@/architecture/BUSINESS.md` or `@BUSINESS.md`

---

## Required Sections

### Section A: VISION

**Purpose**: Project vision, target users, problems solved, success criteria

**Content**:
- **Purpose**: 1-2 sentences describing what the system does
- **Target Users**: Bulleted list of primary user types
- **Key Problems Solved**: Bulleted list of main problems addressed
- **Success Criteria**: Measurable outcomes (3-5 criteria)

**Requirements**:
- 2-5 paragraphs total
- Clear business value proposition
- Measurable success criteria
- No technical details (save for DESIGN.md)

**Example**:
```markdown
## Section A: VISION

**Purpose**: Comprehensive framework for creating, managing, and displaying data visualizations

**Target Users**:
- Platform Administrators - Infrastructure management
- Dashboard Designers - Creating visualizations
- Business Analysts - Consuming reports

**Key Problems Solved**:
- **Data Fragmentation**: Unified access to multiple sources
- **Visualization Complexity**: Rich charts without coding
- **Multi-Tenancy**: Complete tenant isolation

**Success Criteria**:
- Sub-second query response (p95 < 1s)
- Support 100+ concurrent users per tenant
- 99.9% uptime SLA
```

---

### Section B: Actors

**Purpose**: Define all actors (human and system) who interact with the system

**Structure**:
- Group by **Human Actors** and **System Actors**
- Each actor is a #### heading
- Actor ID immediately after heading
- Role description only (no capabilities)

**Actor ID Format**: `fdd-{project-name}-actor-{actor-name}`

**Components**:
- `fdd-` - Prefix indicating FDD methodology
- `{project-name}` - Project name in kebab-case
- `-actor-` - Actor indicator
- `{actor-name}` - Actor name in kebab-case (2-3 words)

**Examples**: 
- `fdd-payment-system-actor-admin`
- `fdd-analytics-actor-data-analyst`
- `fdd-analytics-actor-ui-app` (system actor)

**Format per actor**:
```markdown
#### Actor Name
**ID**: `fdd-project-actor-name`  
**Role**: Description of what this actor does
```

**Required content per actor**:
- **Actor Name**: Clear, descriptive name (#### heading)
- **ID**: Unique identifier (must be first line after heading, wrapped in backticks)
- **Role**: What this actor does (1-2 sentences)
- **NO Capabilities**: Capabilities are in Section C

**Content requirements**:
- Each actor must have unique ID
- ID appears immediately after actor name heading
- Role description only (no capabilities list)
- Plain English, no technical jargon
- Distinguish between human and system actors

**Example**:
```markdown
## Section B: Actors

**Human Actors**:

#### Platform Administrator
**ID**: `fdd-analytics-actor-platform-admin`  
**Role**: Manages platform infrastructure and configuration

#### Dashboard Designer
**ID**: `fdd-analytics-actor-dashboard-designer`  
**Role**: Creates dashboards and visualizations

**System Actors**:

#### UI Application
**ID**: `fdd-analytics-actor-ui-app`  
**Role**: Frontend application for Analytics module
```

---

### Section C: Capabilities

**Purpose**: Define system capabilities and which actors use them

**Structure**:
- Each capability is a #### heading
- Capability ID immediately after heading
- Bulleted list of features
- **Actors** line listing actor IDs (required)

**Capability ID Format**: `fdd-{project-name}-capability-{capability-name}`

**Components**:
- `fdd-` - Prefix indicating FDD methodology
- `{project-name}` - Project name in kebab-case
- `-capability-` - Capability indicator
- `{capability-name}` - Capability name in kebab-case (2-4 words)

**Examples**: 
- `fdd-payment-system-capability-payment-processing`
- `fdd-analytics-capability-data-visualization`

**Format per capability**:
```markdown
#### Capability Name
**ID**: `fdd-project-capability-name`
- Feature 1
- Feature 2
- Feature 3

**Actors**: `fdd-project-actor-name1`, `fdd-project-actor-name2`
```

**Required content per capability**:
- **Capability Name**: Clear name describing the capability (#### heading)
- **ID**: Unique identifier (must be first line after capability heading, wrapped in backticks)
- **Description**: What the capability does (bullet list of features)
- **Actors**: List of actor IDs that use this capability (required)
  - Format: `**Actors**: \`fdd-project-actor-name1\`, \`fdd-project-actor-name2\``
  - Must reference valid actor IDs from Section B
  - All IDs wrapped in backticks

**Content requirements**:
- Each capability must have unique ID
- Each capability must list ≥1 actor ID
- Actor IDs must match actors defined in Section B
- Capabilities are high-level system functions that map to features
- All actor ID references wrapped in backticks

**Example**:
```markdown
## Section C: Capabilities

#### Data Visualization
**ID**: `fdd-analytics-capability-data-visualization`
- Rich chart types (line, bar, pie, scatter, heatmap)
- Interactive tables with sorting and filtering
- Custom widget templates

**Actors**: `fdd-analytics-actor-dashboard-designer`, `fdd-analytics-actor-business-analyst`, `fdd-analytics-actor-end-user`

#### Dashboard Management
**ID**: `fdd-analytics-capability-dashboard-mgmt`
- Grid-based responsive layouts
- Drag-and-drop widget positioning
- Dashboard templates
- Version history

**Actors**: `fdd-analytics-actor-dashboard-designer`, `fdd-analytics-actor-ui-app`
```

---

### Section D: Use Cases

**Purpose**: Detailed use case descriptions showing how actors interact with system capabilities to achieve specific goals.

**Required content**:
- Each use case has a #### heading with descriptive name
- Use case ID immediately after heading
- Actor(s) performing the use case
- Preconditions required
- Flow of steps (numbered list)
- Postconditions after completion

**Use Case ID Format**: `fdd-{project-name}-usecase-{usecase-name}`

**Components**:
- `fdd-` - Prefix indicating FDD methodology
- `{project-name}` - Project name in kebab-case
- `-usecase-` - Use case indicator
- `{usecase-name}` - Use case name in kebab-case (2-5 words)

**Examples**:
- `fdd-payment-system-usecase-process-payment`
- `fdd-analytics-usecase-generate-report`

**Format per use case**:
```markdown
#### UC-XXX: Use Case Name
**ID**: `fdd-project-usecase-name`

**Actor**: `fdd-project-actor-id1`, `fdd-project-actor-id2`

**Preconditions**: Description of required state before execution

**Flow**:
1. Step 1 (may reference capability: `fdd-project-capability-name`)
2. Step 2
3. Step 3 (may reference other use case: `fdd-project-usecase-other`)

**Postconditions**: Description of state after completion
```

**Content requirements**:
- Each use case must have unique ID
- **Actor** field MUST use actor IDs from Section B (wrapped in backticks)
  - Format: `**Actor**: \`fdd-project-actor-name1\`, \`fdd-project-actor-name2\``
  - All actor IDs must reference valid actors defined in Section B
- Flow steps must be clear and actionable
- Flow steps MAY reference capability IDs from Section C (e.g., "uses capability `fdd-project-capability-name`")
- Flow steps MAY reference other use case IDs (e.g., "triggers `fdd-project-usecase-other`")
- Preconditions and postconditions must be specific
- Use cases demonstrate how capabilities are used in practice
- All ID references wrapped in backticks

**Note**: Use cases are optional but recommended for complex systems. If present, section D is mandatory.

---

### Section E: Additional Context (OPTIONAL)

**Purpose**: Product owner notes, business rationale, market context, or other relevant details not covered by core FDD structure

**Content** (examples):
- Market positioning and competitive analysis
- Business model considerations
- Stakeholder notes and feedback
- Product roadmap context
- Budget or timeline constraints
- Regulatory or compliance notes
- Integration requirements with existing systems
- Migration strategy details
- Any other business context

**Note**: This section is optional and not validated by FDD. Use it to capture important business information that doesn't fit into the standard FDD structure.

**Format**: Free-form, no specific structure required

---

## Validation Criteria

### File Validation

1. **File exists**
   - File `architecture/BUSINESS.md` exists
   - File contains ≥50 lines (recommended: 200-500 lines)
   - File is not empty or placeholder-only

### Structure Validation

1. **All required sections present**
   - Section A: VISION
   - Section B: Actors
   - Section C: Capabilities
   - Section D: Use Cases (optional, but if present must be validated)
   - Section E: Additional Context (optional, not validated)

2. **Section order correct**
   - A → B → C → D → E (in this exact order)
   - If Section D (Use Cases) not present, Section E (Additional Context) can follow Section C
   - Section D may be omitted

3. **No prohibited sections**
   - No top-level sections E or beyond
   - Only A-D allowed at top level (D is optional)

4. **Markdown formatting valid**
   - Headers use proper levels (## for A-D, #### for actors/capabilities)
   - No malformed markdown

### Content Validation

1. **Section A: VISION**
   - Contains Purpose, Target Users, Key Problems Solved, Success Criteria
   - Success criteria are measurable
   - ≥2 paragraphs of content

2. **Section B: Actors**
   - ≥1 actor defined
   - Each actor has:
     - #### heading with actor name
     - **ID**: line immediately after heading
     - **Role**: line with description
   - Actor IDs follow format: `fdd-{project}-actor-{name}`
   - All actor IDs are unique
   - Grouped by Human Actors and System Actors

3. **Section C: Capabilities**
   - ≥1 capability defined
   - Each capability has:
     - #### heading with capability name
     - **ID**: line immediately after heading
     - Bulleted list of features
     - **Actors**: line listing actor IDs
   - Capability IDs follow format: `fdd-{project}-capability-{name}`
   - All capability IDs are unique
   - All referenced actor IDs exist in Section B
   - All IDs wrapped in backticks

4. **Section D: Use Cases** (optional)
   - If present, ≥1 use case defined
   - Each use case has:
     - #### heading with "UC-XXX: Use Case Name" format
     - **ID**: line immediately after heading
     - **Actor**: line listing actor IDs (must use IDs, not names)
     - **Preconditions**: description of required state
     - **Flow**: numbered list of steps
     - **Postconditions**: description of state after completion
   - Use case IDs follow format: `fdd-{project}-usecase-{name}`
   - All use case IDs are unique
   - All referenced actor IDs exist in Section B
   - All actor IDs wrapped in backticks
   - Flow steps MAY reference capability IDs from Section C
   - Flow steps MAY reference other use case IDs
   - Preconditions/Postconditions MAY reference use case IDs
   - All ID references wrapped in backticks

### FDD ID Format Validation

1. **Actor IDs**
   - Format: `fdd-{project}-actor-{name}`
   - Kebab-case only
   - Unique across document
   - Wrapped in backticks: `\`fdd-...\``

2. **Capability IDs**
   - Format: `fdd-{project}-capability-{name}`
   - Kebab-case only
   - Unique across document
   - Wrapped in backticks: `\`fdd-...\``

3. **Use Case IDs** (if Section D present)
   - Format: `fdd-{project}-usecase-{name}`
   - Kebab-case only
   - Unique across document
   - Wrapped in backticks: `\`fdd-...\``

4. **ID Placement**
   - Must appear immediately after heading (first line)
   - Format: `**ID**: \`fdd-...\``
   - No blank lines between heading and ID

### Cross-Reference Validation

1. **Capability → Actor references**
   - All actor IDs in **Actors**: lines must exist in Section B
   - Actor IDs must be wrapped in backticks
   - At least one actor per capability

2. **Use Case → Actor references** (if Section D present)
   - All actor IDs in **Actor**: lines must exist in Section B
   - Actor IDs must be wrapped in backticks (not plain text names)
   - At least one actor per use case

3. **Use Case → Capability references** (if Section D present)
   - Capability IDs referenced in Flow steps must exist in Section C
   - Capability IDs must be wrapped in backticks
   - References are optional

4. **Use Case → Use Case references** (if Section D present)
   - Use case IDs referenced in Preconditions/Flow/Postconditions must exist in Section D
   - Use case IDs must be wrapped in backticks
   - References are optional

---

## Best Practices

1. **Keep it business-focused**
   - Focus on business problems and value
   - Avoid technical implementation details
   - Use plain English, not jargon

2. **Actor definitions**
   - Distinguish between human and system actors
   - Keep role descriptions concise (1-2 sentences)
   - Focus on "who" not "how"

3. **Capability definitions**
   - Group related features under one capability
   - Keep capability scope broad but coherent
   - List actor IDs that use each capability

4. **Success criteria**
   - Make them measurable
   - Include quantitative targets
   - Focus on business outcomes

5. **ID naming**
   - Use descriptive names (2-4 words)
   - Keep consistent with domain language
   - Use kebab-case
   - Always wrap in backticks

---

## Examples

**Valid BUSINESS.md structure**:
```markdown
# Business Context

## A. Vision

Provide analytics platform for tracking user behavior...

## B. Actors

### Admin User
**ID**: `fdd-actor-admin`
Administrator managing the system...

### Data Analyst
**ID**: `fdd-actor-analyst`
Analyzes user behavior data...

## C. Capabilities

### Analytics Dashboard
**ID**: `fdd-capability-dashboard`
**Actors**: `fdd-actor-admin`, `fdd-actor-analyst`

View and analyze user behavior metrics...
```

**Invalid BUSINESS.md**:
```markdown
# Business Stuff

Some information about the business.

We have users and admins.
```

**Issues**: No structured sections, no IDs, no clear actors/capabilities definition

---

## References

**This file is referenced by**:
- ALWAYS open and follow this file WHEN creating or modifying BUSINESS.md

**References**:
- `core.md` - Core FDD principles
- `overall-design-structure.md` - DESIGN.md references actors/capabilities from BUSINESS.md
