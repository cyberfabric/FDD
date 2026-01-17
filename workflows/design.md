<!-- @fdd-change:fdd-fdd-feature-core-methodology-change-core-workflows:ph-1 -->
---
description: Create or update overall design document
---

# Create or Update Overall Design

**Type**: Operation  
**Role**: Architect  
**Artifact**: `architecture/DESIGN.md`

---

**ALWAYS open and follow**: `../requirements/core.md` WHEN editing this file

ALWAYS open and follow `../requirements/workflow-execution.md` WHEN executing this workflow

## Requirements

**ALWAYS open and follow**: `../requirements/overall-design-structure.md`

Extract:
- Required sections (A: Architecture Overview, B: Requirements & Principles, C: Technical Architecture, D: Additional Context)
- Content requirements per section
- Validation criteria

---

## Prerequisites

**MUST validate**:
- [ ] BUSINESS.md exists - validate: Check file at `architecture/BUSINESS.md`
- [ ] BUSINESS.md validated - validate: Score ≥90/100

**If missing**: Run `business-context` and `business-validate` first

---

## Steps
 
 <!-- fdd-begin fdd-fdd-feature-core-methodology-flow-architect-bootstrap:ph-1:inst-execute-workflow -->
 Determine Mode.
 
### 1. Determine Mode
<!-- fdd-end   fdd-fdd-feature-core-methodology-flow-architect-bootstrap:ph-1:inst-execute-workflow -->

Check if `architecture/DESIGN.md` exists:
- **If exists**: UPDATE mode - Read and propose changes
- **If NOT exists**: CREATE mode - Generate from scratch

### 2. Read Business Context

Open `architecture/BUSINESS.md`

Extract:
- Vision (Section A)
- Actors list (Section B)
- Capabilities list (Section C)

### 3. Mode-Specific Actions

**CREATE Mode**:
- Proceed to Step 4 for interactive input collection

**UPDATE Mode**:
- Read existing DESIGN.md
- Extract current content:
  - Section A: Architecture Overview
  - Section B: Requirements & Principles
  - Section C: Technical Architecture
  - Section D: Additional Context
- Ask user: What to update?
  - Update architecture style/layers
  - Add/edit/remove requirements
  - Add/edit/remove principles
  - Update technical architecture
  - Update NFRs
  - Update components
- Proceed to Step 4 with appropriate questions

### 4. Interactive Input Collection

**Mode-specific behavior**:

**Q1: Architecture Style**
- Context: Architectural pattern for this system
- Options: Monolithic, Microservices, Layered, Hexagonal, Event-Driven, Other
- **CREATE**: Propose based on capabilities complexity
- **UPDATE**: Show current style, ask to change or keep
- Store as: `ARCH_STYLE`

**Q2: Key Components**
- Context: Main system components (3-7 components)
- **CREATE**: Propose based on architecture style and capabilities
- **UPDATE**: Show current components, ask to add/edit/remove or keep
- Store as: `COMPONENTS[]`

**Q3: Technical Stack** (if adapter missing)
- Context: Technologies, frameworks, libraries
- **CREATE**: Detect from project files or ask
- **UPDATE**: Show current stack, ask to update or keep
- Store as: `TECH_STACK`
- Note: If adapter exists, use adapter tech specs

**Q4: Design Principles**
- Context: Key architectural principles (3-5 principles)
- **CREATE**: Propose FDD defaults + style-specific
- **UPDATE**: Show current principles, ask to add/edit/remove or keep
- Store as: `PRINCIPLES[]`

**Q5: NFRs**
- Context: Non-functional requirements (performance, security, scalability)
- **CREATE**: Propose based on architecture style
- **UPDATE**: Show current NFRs, ask to add/edit/remove or keep
- Store as: `NFRS[]`

### 5. Generate/Update Requirements

**CREATE mode**: Map business capabilities to technical requirements
- For each capability: 1-3 technical requirements
- Generate requirement IDs: `fdd-{project}-req-{kebab-case}`

**UPDATE mode**: Update requirements based on changes
- Add new requirements for new capabilities
- Update existing requirements if modified
- Remove requirements if no longer needed

### 6. Generate Content

**CREATE mode**: Generate complete new DESIGN.md

**UPDATE mode**: Update existing DESIGN.md with changes

Generate content following `overall-design-structure.md`:
- Section A: Architecture Overview (architectural vision, layers)
- Section B: Requirements & Principles (requirements, principles)
- Section C: Technical Architecture (components, domain model, API contracts, security, NFRs)
- Section D: Additional Context (optional)

Ensure:
- No contradictions with BUSINESS.md
- All actors/capabilities from BUSINESS.md referenced
- No type redefinitions
- All IDs formatted correctly

### 7. Summary and Confirmation

Show:
- **CREATE**: File path: `architecture/DESIGN.md` (new file)
- **UPDATE**: File path: `architecture/DESIGN.md` (updating existing)
- Architecture style (if changed)
- Components: {count} ({added}/{modified}/{removed})
- Requirements: {count} ({added}/{modified}/{removed})
- Principles: {count} ({added}/{modified}/{removed})
- References to BUSINESS.md
- Changes summary (for UPDATE mode)

Ask: Proceed? [yes/no/modify]

### 8. Create or Update File

**CREATE Mode**:
- Create `architecture/DESIGN.md`

**UPDATE Mode**:
- Read existing DESIGN.md
- Apply changes to content
- Write updated DESIGN.md

After operation:
- Verify file exists
- Verify content correct

### 9. Create Architecture Decision Records

**CREATE Mode only**:
- Automatically trigger `adr` workflow
- If ADR.md does NOT exist: Create ADR.md with ADR-0001 (Initial Architecture)
- If ADR.md exists: Skip

**UPDATE Mode**:
- Skip ADR creation (user can run `adr` workflow separately if needed)

**ADR-0001 Content** (CREATE mode):
- Title: "Initial {Module/Project} Architecture"
- Context: Based on architecture style and key decisions from DESIGN.md
- Drivers: Key requirements and principles
- Options: Architecture alternatives considered
- Outcome: Chosen architecture with rationale
- Related Elements: Link to actors, capabilities, requirements, principles

**Output** (CREATE mode):
```markdown
---

## Creating Initial ADR

Creating ADR.md with ADR-0001 (Initial Architecture)...
```

---

## Validation

Run: `design-validate`

Expected:
- Score: ≥90/100
- Status: PASS
- No contradictions with BUSINESS.md

Then run: `adr-validate`

Expected:
- Score: ≥90/100
- Status: PASS
- ADR-0001 properly formatted

---

## Next Steps

**If both validations pass**: `features` workflow (decompose into features)

**If validation fails**: Fix issues, re-validate
