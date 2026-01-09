# FDD Workflow System

**Version**: 2.0  
**Purpose**: Define roles, layers, workflows, and sequences in FDD methodology

---

## FDD Core Principles

### Agent-Optimized Design

**All FDD files MUST be optimized for AI agents**:
- **Brevity**: Minimal text, maximum information density
- **Imperative language**: Direct commands, not suggestions
- **Mandatory markers**: MUST, REQUIRED, SHALL for obligations
- **OS-agnostic**: No OS-specific commands or paths
- **Structured format**: Parseable sections, consistent headers

### FDD Adapter Concept

**FDD Adapter is OPTIONAL**:
- Workflows work with sensible defaults without adapter
- Adapter required only when customization needed
- Adapter auto-triggers when user touches customization details

**Adapter Structure**:
- Primary file: `{adapter-directory}/FDD-Adapter/AGENTS.md`
- Format: ALWAYS ... WHEN instructions (like FDD/AGENTS.md)
- Content: Navigation to adapter-specific configuration files
- Purpose: Project-specific conventions, formats, paths

**Adapter Auto-Trigger Rules**:
- Agent ALWAYS stop and run `adapter` workflow WHEN:
  - User specifies domain model format/location
  - User specifies API contract format/location
  - User specifies custom file structures
  - User specifies project-specific conventions
  - Any customization beyond FDD defaults required

**Without Adapter**:
- Product Manager workflows work fully (business context is generic)
- Architect workflows work partially (defaults for structure)
- Feature workflows work partially (generic templates)
- Implementation workflows REQUIRE adapter (code conventions needed)

### Workflow Types

**Operation Workflows** (Type: Operation):
- Create or update documents/code
- Include user interactions (questions, proposals)
- ALWAYS open and follow `core.md` WHEN creating or modifying FDD core files changes
- Run validation workflow after completion

**Validation Workflows** (Type: Validation):
- Validate structure and consistency
- Fully automated (no user interaction)
- Use requirements files as source of truth
- Output results to chat (no report files)

### Validation Requirements

**Every validation ALWAYS do check**:
1. **Structure**: Compliance with requirements file structure
2. **Non-contradiction**: No conflicts with dependency artifacts
3. **Coverage**: All requirements from dependencies addressed
4. **Completeness**: No placeholders, all IDs valid, all sections present

**Formula**: `B includes all of A, B follows Structure, B doesn't contradict A or Structure`

---

## Roles and Responsibilities

### Project Manager

**Controls**: All steps, all layers, adapter creation (when needed)

**Artifacts**:
- FDD Adapter configuration (optional, only when customization required)
- Project structure

**Workflows**:
- `adapter` - Create/configure FDD adapter from scratch (auto-triggered on customization)
- `adapter-from-sources` - Create/configure FDD adapter by analyzing existing codebase
- `adapter-agents` - Configure AI agent integration (Windsurf, Cursor, etc.)
- `adapter-validate` - Validate adapter structure

**Oversight**: Can run any workflow for project control

**Adapter Requirement**: Optional, only for project-specific customizations

---

### Product Manager

**Controls**: Business context, business requirements alignment

**Artifacts**:
- `architecture/BUSINESS.md`

**Workflows**:
- `business-context` - Create/update BUSINESS.md (vision, actors, capabilities)
- `business-validate` - Validate BUSINESS.md structure and completeness
- `design-validate` - Validate DESIGN.md alignment with business requirements (shared with Architect)

**Requirements**:
- Architecture and code MUST NOT contradict business requirements
- All business requirements ALWAYS do be addressed in design
- Product Manager can validate design for business alignment control

**Adapter Requirement**: NOT required (business context is generic, no customization needed)

---

### Architect

**Controls**: Architectural principles, design decomposition, business alignment

**Artifacts**:
- `architecture/DESIGN.md`
- `architecture/ADR.md` (optional)
- `architecture/features/FEATURES.md`

**Workflows**:
- `design` - Create/update DESIGN.md (may update ADR.md)
- `design-validate` - Validate DESIGN.md (vs BUSINESS.md, vs structure, ADR consistency)
- `features` - Create/update FEATURES.md (decompose design into features)
- `features-validate` - Validate FEATURES.md (vs DESIGN.md, vs structure)
- `adapter` - Create FDD adapter (shared with PM, auto-triggered)
- `adapter-validate` - Validate adapter (shared with PM)
- `feature-validate` - Validate feature DESIGN.md (control workflow)

**Requirements**:
- Design MUST NOT contradict business context
- Features decomposition ALWAYS do cover entire design
- ADR ALWAYS do be consistent with design

**Adapter Requirement**: OPTIONAL by default, REQUIRED when:
- Specifying domain model format/location
- Specifying API contract format/location
- Defining technical stack details
- Agent auto-triggers `adapter` workflow when user provides these details

---

### Solution Architect

**Controls**: Feature details, technical specifications

**Artifacts**:
- `architecture/features/feature-{slug}/DESIGN.md`
- Actor flows, algorithms, state machines
- Database schemas, API specifications

**Workflows**:
- `feature` - Create/update feature DESIGN.md (actor flows, algorithms, states, schemas, requirements)
- `feature-validate` - Validate feature DESIGN.md (vs DESIGN.md, vs FEATURES.md, vs structure)

**Requirements**:
- Feature MUST NOT contradict overall design
- Feature ALWAYS do address requirements from FEATURES.md
- Feature MUST NOT redefine types from overall design

**Adapter Requirement**: OPTIONAL (can use generic templates), RECOMMENDED for:
- Database schema formats
- API specification formats
- Technical conventions

---

### Developer

**Controls**: Implementation planning and execution

**Artifacts**:
- `architecture/features/feature-{slug}/CHANGES.md`
- Code implementation
- Tests

**Workflows**:
- `feature-changes` - Create/update CHANGES.md (implementation plan with granular changes)
- `feature-changes-validate` - Validate CHANGES.md (vs feature DESIGN.md, vs structure)
- `feature-change-implement` - Implement specific change from CHANGES.md (task by task)
- `feature-change-validate` - Validate code (vs adapter requirements, vs feature requirements, run tests)

**Requirements**:
- Each change ALWAYS do implement 1-N requirements from feature DESIGN.md
- Code MUST pass all tests
- Code ALWAYS do follow adapter conventions
- Code ALWAYS do be tagged with `@fdd-change:{change-id}` comments for traceability

**Adapter Requirement**: REQUIRED
- Code conventions mandatory
- Testing requirements mandatory
- Build/deployment configuration mandatory
- Agent ALWAYS stop and run `adapter` workflow if adapter missing

---

### QA Engineer

**Controls**: Test scenarios, end-to-end validation

**Artifacts**:
- Test reports
- Quality metrics

**Workflows**:
- `feature-qa` - Complete feature validation (runs feature-validate, feature-changes-validate, all feature-change-validate)
- `feature-change-validate` - Individual change validation (shared with Developer)

**Requirements**:
- All test scenarios from feature DESIGN.md ALWAYS do be validated
- All changes ALWAYS do pass validation

---

## Workflow Layers

### Layer 1: Project Setup

**Artifacts**: FDD Adapter, project structure

**Workflows**:
- `adapter` (PM/Architect)
- `adapter-validate` (PM/Architect)

**Purpose**: Configure FDD for project-specific conventions

---

### Layer 2: Business Context

**Artifacts**: `architecture/BUSINESS.md`

**Workflows**:
- `business-context` (Product Manager)
- `business-validate` (Product Manager)

**Purpose**: Define business vision, actors, capabilities

**Prerequisite**: Adapter validated

---

### Layer 3: Overall Design

**Artifacts**: `architecture/DESIGN.md`, `architecture/ADR.md`

**Workflows**:
- `design` (Architect)
- `design-validate` (Architect)
- `design-validate-business` (Product Manager, control)

**Purpose**: Define architecture, principles, technical stack

**Prerequisite**: BUSINESS.md validated

---

### Layer 4: Features Decomposition

**Artifacts**: `architecture/features/FEATURES.md`

**Workflows**:
- `features` (Architect)
- `features-validate` (Architect)

**Purpose**: Decompose design into feature list

**Prerequisite**: DESIGN.md validated

---

### Layer 5: Feature Design

**Artifacts**: `architecture/features/feature-{slug}/DESIGN.md`

**Workflows**:
- `feature` (Solution Architect)
- `feature-validate` (Solution Architect + Architect control)

**Purpose**: Detail feature requirements, flows, algorithms

**Prerequisite**: FEATURES.md validated

---

### Layer 6: Implementation Planning

**Artifacts**: `architecture/features/feature-{slug}/CHANGES.md`

**Workflows**:
- `feature-changes` (Developer)
- `feature-changes-validate` (Developer)

**Purpose**: Plan implementation as granular changes

**Prerequisite**: Feature DESIGN.md validated

---

### Layer 7: Implementation Execution

**Artifacts**: Code, tests

**Workflows**:
- `feature-change-implement` (Developer)
- `feature-change-validate` (Developer + QA)

**Purpose**: Implement and validate changes

**Prerequisite**: CHANGES.md validated

---

### Layer 8: Feature Completion

**Artifacts**: Quality reports

**Workflows**:
- `feature-qa` (QA)

**Purpose**: End-to-end feature validation

**Prerequisite**: All changes implemented

---

## Complete Workflow List

### Project Manager Workflows (4)

1. `adapter` - Type: Operation
   - Create/configure FDD adapter from scratch
   - No prerequisites (first workflow)
   - Interactive: Ask user for conventions, formats, paths
   
2. `adapter-from-sources` - Type: Operation
   - Create/configure FDD adapter by analyzing existing codebase
   - No prerequisites (alternative to adapter)
   - Analyzes: Code structure, package.json, build configs, test configs
   - Proposes: Detected conventions instead of asking
   
3. `adapter-agents` - Type: Operation
   - Configure AI agent integration files
   - Prerequisite: Adapter exists (optional, can run standalone)
   - Creates: .windsurf/rules.md, .cursorrules, .cascade/config.json
   - Purpose: Teach agents project-specific FDD conventions
   
4. `adapter-validate` - Type: Validation
   - Prerequisite: Adapter exists
   - Validates: Structure, configuration, AGENTS.md format

---

### Product Manager Workflows (3)

3. `business-context` - Type: Operation
   - Create/update BUSINESS.md
   - Prerequisite: Adapter validated
   
4. `business-validate` - Type: Validation
   - Prerequisite: BUSINESS.md exists
   - Validates: Structure, completeness

5. `design-validate` - Type: Validation (shared with Architect)
   - Prerequisite: DESIGN.md exists, BUSINESS.md validated
   - Validates: DESIGN.md alignment with business requirements, no contradictions

---

### Architect Workflows (6)

7. `design` - Type: Operation
   - Create/update DESIGN.md (and ADR.md)
   - Prerequisite: BUSINESS.md validated
   
8. `design-validate` - Type: Validation (shared with PM)
   - Prerequisite: DESIGN.md exists, BUSINESS.md validated
   - Validates: Structure, vs BUSINESS.md, ADR consistency
   
9. `features` - Type: Operation
   - Create/update FEATURES.md
   - Prerequisite: DESIGN.md validated
   
10. `features-validate` - Type: Validation
   - Prerequisite: FEATURES.md exists, DESIGN.md validated
   - Validates: Structure, vs DESIGN.md, coverage

11. `adapter` - Type: Operation (shared with PM)
12. `adapter-from-sources` - Type: Operation (shared with PM)

---

### Solution Architect Workflows (2)

13. `feature` - Type: Operation
    - Create/update feature DESIGN.md
    - Prerequisite: FEATURES.md validated
    
14. `feature-validate` - Type: Validation
    - Prerequisite: Feature DESIGN.md exists, FEATURES.md validated
    - Validates: Structure, vs DESIGN.md, vs FEATURES.md

---

### Developer Workflows (4)

15. `feature-changes` - Type: Operation
    - Create/update CHANGES.md
    - Prerequisite: Feature DESIGN.md validated
    
16. `feature-changes-validate` - Type: Validation
    - Prerequisite: CHANGES.md exists, feature validated
    - Validates: Structure, vs feature DESIGN.md
    
17. `feature-change-implement` - Type: Operation
    - Implement specific change
    - Tag all code with change identifier
    - Prerequisite: CHANGES.md validated
    
18. `feature-change-validate` - Type: Validation
    - Prerequisite: Change implemented
    - Validates: Code vs requirements, tests pass, change tags present

---

### QA Workflows (1)

19. `feature-qa` - Type: Validation
    - Complete feature validation (orchestrates multiple validations)
    - Prerequisite: All changes implemented
    - Runs: feature-validate, feature-changes-validate, all feature-change-validate

---

## Typical Workflow Sequences

### New Project from Scratch

```
adapter 
→ adapter-validate 
→ business-context 
→ business-validate 
→ design 
→ design-validate 
→ features 
→ features-validate 
→ feature (for each feature)
→ feature-validate 
→ feature-changes 
→ feature-changes-validate 
→ feature-change-implement (for each change)
→ feature-change-validate (for each change)
→ feature-qa 
→ Next feature or complete
```

### Add Feature to Existing Project

```
[DESIGN.md already validated]
→ features (update FEATURES.md)
→ features-validate 
→ feature (new feature)
→ feature-validate 
→ feature-changes 
→ feature-changes-validate 
→ feature-change-implement (for each change)
→ feature-change-validate (for each change)
→ feature-qa
```

### Fix Design Issue During Implementation

```
[During feature-change-implement, design issue found]
→ design (update DESIGN.md)
→ design-validate 
→ feature (update feature DESIGN.md)
→ feature-validate 
→ feature-changes (update CHANGES.md if needed)
→ feature-changes-validate 
→ feature-change-implement (continue)
```

### Product Manager Control Point

```
[After design created by Architect]
→ design-validate (Architect validates structure + business alignment)
→ [If FAIL: Architect fixes design]
→ [If PASS: Proceed to features]
```

---

## Key Changes from Version 1.0

### Removed

- ❌ OpenSpec (replaced with feature/CHANGES.md)
- ❌ openspec/ directory structure
- ❌ openspec-* workflows
- ❌ Multi-phase numbering (01-init-project, 02-validate, etc.)

### Added

- ✅ Role-based workflow organization
- ✅ BUSINESS.md as separate artifact (Layer 2)
- ✅ feature/CHANGES.md (replaces openspec/changes/)
- ✅ Clear validation prerequisites
- ✅ Control workflows for cross-role validation
- ✅ Explicit layer hierarchy

### Changed

- 🔄 Workflow naming: Descriptive names (not numbered)
- 🔄 Validation: Always after operation, uses requirements files
- 🔄 Prerequisites: Explicit validation dependencies
- 🔄 DESIGN.md: Now depends on BUSINESS.md

---

## Validation Chain

```
adapter-validate
    ↓
business-validate
    ↓
design-validate (checks BUSINESS.md)
    ↓
features-validate (checks DESIGN.md)
    ↓
feature-validate (checks DESIGN.md + FEATURES.md)
    ↓
feature-changes-validate (checks feature DESIGN.md)
    ↓
feature-change-validate (checks CHANGES.md + adapter + tests)
    ↓
feature-qa (orchestrates all validations)
```

**Rule**: Every artifact MUST be validated before dependent artifacts can be created

---

## References

**For workflow execution**: See `requirements/workflow-execution.md`

**For requirements files**: See `requirements/core-requirements.md`

**For agent navigation**: See `AGENTS.md`

**For adapter structure**: See `requirements/adapter-structure.md` (to be created)

**For CHANGES.md structure**: See `requirements/feature-changes-structure.md` (to be created)
