# Features: FDD

**Status Overview**: 13 features total (0 completed, 1 in progress, 12 not started)

**Meaning**:
- ⏳ NOT_STARTED
- 🔄 IN_PROGRESS
- ✅ IMPLEMENTED

---

## Features List

### 1. [fdd-fdd-feature-core-methodology](feature-core-methodology/) 🔄 CRITICAL

- **Purpose**: Foundation FDD methodology framework with requirements files, workflow specifications, and base AGENTS.md navigation
- **Status**: IN_PROGRESS
- **Depends On**: None
- **Blocks**: 
  - [feature-adapter-system](feature-adapter-system/)
  - [feature-workflow-engine](feature-workflow-engine/)
  - [feature-validation-engine](feature-validation-engine/)
- **Phases**:
  - `ph-1`: ⏳ NOT_STARTED — Core requirements files and base AGENTS.md
- **Requirements Covered**:
  - fdd-fdd-req-executable-workflows
  - fdd-fdd-req-design-first
  - fdd-fdd-req-interactive-docs
- **Principles Covered**:
  - fdd-fdd-principle-tech-agnostic
  - fdd-fdd-principle-design-first
- **Constraints Affected**:
  - fdd-fdd-constraint-markdown
- **Scope**:
  - Requirements files defining artifact structures (*-structure.md)
  - Workflow specification files in workflows/ directory
  - Core AGENTS.md with base navigation rules
  - QUICKSTART guide and README for onboarding
  - Methodology version tracking

---

### 2. [fdd-fdd-feature-adapter-system](feature-adapter-system/) ⏳ CRITICAL

- **Purpose**: Project-specific customization layer through adapter configuration with Extends mechanism
- **Status**: NOT_STARTED
- **Depends On**:
  - [feature-core-methodology](feature-core-methodology/)
- **Blocks**:
  - [feature-workflow-engine](feature-workflow-engine/)
  - [feature-ai-integration](feature-ai-integration/)
  - [feature-migration](feature-migration/)
- **Phases**:
  - `ph-1`: ⏳ NOT_STARTED — Adapter directory structure and Extends mechanism
- **Requirements Covered**:
  - fdd-fdd-req-adapter-configuration
  - fdd-fdd-req-pattern-reusability
- **Principles Covered**:
  - fdd-fdd-principle-tech-agnostic
- **Constraints Affected**:
  - fdd-fdd-constraint-markdown
- **Scope**:
  - Adapter AGENTS.md with Extends mechanism
  - Tech stack specification (specs/tech-stack.md)
  - Domain model format configuration (specs/domain-model.md)
  - API contract format specification (specs/patterns.md)
  - Coding conventions (specs/conventions.md)
  - Build and deployment specs (specs/build-deploy.md)
  - Testing strategy specs (specs/testing.md)
  - Project structure conventions (specs/project-structure.md)
  - Auto-detection from existing codebase

---

### 3. [fdd-fdd-feature-validation-engine](feature-validation-engine/) ⏳ CRITICAL

- **Purpose**: Deterministic validators with 100-point scoring system for structural artifact validation
- **Status**: NOT_STARTED
- **Depends On**:
  - [feature-core-methodology](feature-core-methodology/)
  - [feature-id-management](feature-id-management/)
- **Blocks**:
  - [feature-workflow-engine](feature-workflow-engine/)
  - [feature-realtime-validation](feature-realtime-validation/)
- **Phases**:
  - `ph-1`: ⏳ NOT_STARTED — Core validation framework with scoring
  - `ph-2`: ⏳ NOT_STARTED — Artifact-specific validators (BUSINESS, DESIGN, ADR, FEATURES, etc.)
- **Requirements Covered**:
  - fdd-fdd-req-deterministic-validation
- **Principles Covered**:
  - fdd-fdd-principle-deterministic-gate
  - fdd-fdd-principle-machine-readable
- **Constraints Affected**:
  - fdd-fdd-constraint-stdlib-only
- **Scope**:
  - fdd validation tool (Python 3 standard library only)
  - 100-point scoring system with category breakdown
  - Pass thresholds (≥90 or 100/100)
  - Cross-reference validation (actor/capability/requirement IDs)
  - Placeholder detection (incomplete content markers)
  - Detailed issue reporting with fix recommendations
  - JSON output format for machine consumption
  - Artifact type auto-detection

---

### 4. [fdd-fdd-feature-id-management](feature-id-management/) ⏳ CRITICAL

- **Purpose**: FDD ID generation, validation, and repository-wide scanning for complete traceability
- **Status**: NOT_STARTED
- **Depends On**:
  - [feature-core-methodology](feature-core-methodology/)
- **Blocks**:
  - [feature-validation-engine](feature-validation-engine/)
  - [feature-workflow-engine](feature-workflow-engine/)
- **Phases**:
  - `ph-1`: ⏳ NOT_STARTED — ID format validation and generation
  - `ph-2`: ⏳ NOT_STARTED — Repository scanning and traceability queries
- **Requirements Covered**:
  - fdd-fdd-req-traceability
- **Principles Covered**:
  - fdd-fdd-principle-traceability
- **Scope**:
  - ID format follows pattern: `fdd-PROJECT-KIND-NAME`
  - Qualified ID support: base:ph-N:inst-name format
  - Repository-wide ID scanning (scan-ids command)
  - Where-defined and where-used queries
  - Cross-reference validation across artifacts
  - Code tag traceability (@fdd-* tags)
  - ID uniqueness checking

---

### 5. [fdd-fdd-feature-workflow-engine](feature-workflow-engine/) ⏳ HIGH

- **Purpose**: Executable workflow system with operation workflows (CREATE/UPDATE) and validation workflows
- **Status**: NOT_STARTED
- **Depends On**:
  - [feature-core-methodology](feature-core-methodology/)
  - [feature-adapter-system](feature-adapter-system/)
  - [feature-validation-engine](feature-validation-engine/)
  - [feature-id-management](feature-id-management/)
- **Blocks**:
  - [feature-ai-integration](feature-ai-integration/)
  - [feature-feature-lifecycle](feature-feature-lifecycle/)
- **Phases**:
  - `ph-1`: ⏳ NOT_STARTED — Operation workflows (business, design, adr, features, feature, changes)
  - `ph-2`: ⏳ NOT_STARTED — Validation workflows for each artifact type
- **Requirements Covered**:
  - fdd-fdd-req-executable-workflows
  - fdd-fdd-req-incremental-development
- **Principles Covered**:
  - fdd-fdd-principle-design-first
- **Scope**:
  - Operation workflows with CREATE/UPDATE mode detection
  - Interactive question-answer flow with context-based proposals
  - Prerequisite validation before workflow execution
  - Automatic validation after artifact creation
  - Workflow chaining (auto-trigger next workflow)
  - User confirmation before file creation/modification

---

### 6. [fdd-fdd-feature-ai-integration](feature-ai-integration/) ⏳ HIGH

- **Purpose**: AI agent integration through AGENTS.md navigation, skills system, and deterministic gate pattern
- **Status**: NOT_STARTED
- **Depends On**:
  - [feature-adapter-system](feature-adapter-system/)
  - [feature-workflow-engine](feature-workflow-engine/)
  - [feature-validation-engine](feature-validation-engine/)
- **Blocks**: None
- **Phases**:
  - `ph-1`: ⏳ NOT_STARTED — WHEN clause navigation and skill system
  - `ph-2`: ⏳ NOT_STARTED — Deterministic gate pattern implementation
- **Requirements Covered**:
  - fdd-fdd-req-ai-integration
- **Principles Covered**:
  - fdd-fdd-principle-deterministic-gate
  - fdd-fdd-principle-machine-readable
- **Constraints Affected**:
  - fdd-fdd-constraint-no-forced-tools
- **Scope**:
  - AGENTS.md two-level hierarchy (Core + Adapter)
  - WHEN clause pattern for conditional navigation
  - Extends mechanism for adapter AGENTS.md
  - Skills system (fdd skill as reference implementation)
  - Deterministic gate: automated validators before manual review
  - Structured prompts for AI interaction
  - Execution protocol for all workflows

---

### 7. [fdd-fdd-feature-fdl](feature-fdl/) ⏳ HIGH

- **Purpose**: Plain-English algorithm description language (FDL) for behavioral specifications
- **Status**: NOT_STARTED
- **Depends On**:
  - [feature-core-methodology](feature-core-methodology/)
- **Blocks**: None
- **Phases**:
  - `ph-1`: ⏳ NOT_STARTED — FDL syntax and structure specification
- **Requirements Covered**:
  - fdd-fdd-req-fdl
- **Principles Covered**:
  - fdd-fdd-principle-machine-readable
- **Scope**:
  - Structured numbered lists for algorithms
  - Bold keywords (**IF**, **ELSE**, **WHILE**, **FOR EACH**, **AND**, **OR**, **NOT**, **MUST**, **REQUIRED**, **OPTIONAL**)
  - Instruction markers with checkboxes (- [ ] Inst-label: description)
  - Phase organization (ph-1, ph-2, etc.)
  - Qualified IDs for implementation tracking (:ph-N:inst-name)
  - FDL-to-code translation guidelines
  - Non-programmer readability for validation

---

### 8. [fdd-fdd-feature-adr-management](feature-adr-management/) ⏳ HIGH

- **Purpose**: Architecture decision tracking with MADR format and impact analysis
- **Status**: NOT_STARTED
- **Depends On**:
  - [feature-core-methodology](feature-core-methodology/)
  - [feature-validation-engine](feature-validation-engine/)
- **Blocks**: None
- **Phases**:
  - `ph-1`: ⏳ NOT_STARTED — ADR creation and MADR format validation
- **Requirements Covered**:
  - fdd-fdd-req-arch-decision-mgmt
- **Scope**:
  - MADR format (Markdown ADR)
  - ADR ID format follows pattern: `ADR-NNNN` or `fdd-PROJECT-adr-NAME`
  - Decision status tracking (PROPOSED, ACCEPTED, DEPRECATED, SUPERSEDED)
  - Links to affected design sections and features
  - Impact analysis when ADR changes
  - ADR search by status, date, or components
  - Version history for decision evolution

---

### 9. [fdd-fdd-feature-feature-lifecycle](feature-feature-lifecycle/) ⏳ HIGH

- **Purpose**: Feature status tracking and dependency management for release planning
- **Status**: NOT_STARTED
- **Depends On**:
  - [feature-workflow-engine](feature-workflow-engine/)
  - [feature-id-management](feature-id-management/)
- **Blocks**: None
- **Phases**:
  - `ph-1`: ⏳ NOT_STARTED — Feature status tracking (NOT_STARTED, IN_PROGRESS, IMPLEMENTED)
  - `ph-2`: ⏳ NOT_STARTED — Dependency management and blocking detection
- **Requirements Covered**:
  - fdd-fdd-req-feature-lifecycle
- **Scope**:
  - Feature status lifecycle (NOT_STARTED → IN_PROGRESS → IMPLEMENTED)
  - Automated status updates based on CHANGES.md completion
  - Dependency tracking and blocking detection
  - Milestone and release planning integration
  - Historical completion metrics and velocity tracking
  - Status transition validation (cannot skip states)

---

### 10. [fdd-fdd-feature-code-generation](feature-code-generation/) ⏳ MEDIUM

- **Purpose**: Generate code scaffolding from validated feature DESIGN.md specifications
- **Status**: NOT_STARTED
- **Depends On**:
  - [feature-adapter-system](feature-adapter-system/)
  - [feature-validation-engine](feature-validation-engine/)
  - [feature-id-management](feature-id-management/)
- **Blocks**: None
- **Phases**:
  - `ph-1`: ⏳ NOT_STARTED — Scaffolding generation from design specs
- **Requirements Covered**:
  - fdd-fdd-req-code-generation
- **Principles Covered**:
  - fdd-fdd-principle-traceability
- **Scope**:
  - API endpoint generation from Section E (API Contracts)
  - Domain type generation from Section C.2 (Domain Model)
  - Test stub generation from Section D (Test Cases)
  - Language-specific output using adapter specs
  - Automatic traceability tag insertion (@fdd-* tags)
  - Placeholder preservation for manual implementation

---

### 11. [fdd-fdd-feature-realtime-validation](feature-realtime-validation/) ⏳ MEDIUM

- **Purpose**: Real-time validation feedback and IDE integration with file watchers
- **Status**: NOT_STARTED
- **Depends On**:
  - [feature-validation-engine](feature-validation-engine/)
  - [feature-id-management](feature-id-management/)
- **Blocks**: None
- **Phases**:
  - `ph-1`: ⏳ NOT_STARTED — Real-time validation as files are edited
  - `ph-2`: ⏳ NOT_STARTED — IDE integration (navigation, syntax highlighting)
- **Requirements Covered**:
  - fdd-fdd-req-realtime-validation
  - fdd-fdd-req-ide-integration
- **Constraints Affected**:
  - fdd-fdd-constraint-no-forced-tools
- **Scope**:
  - IDE file watcher integration for auto-validation
  - Instant feedback on ID format errors (<1 second)
  - Real-time cross-reference checking
  - Incremental validation (only changed sections)
  - Background validation without blocking editing
  - IDE-specific configuration generation (.cursorrules, .windsurf/)
  - Click-to-navigate from ID references to definitions
  - FDL syntax highlighting in Markdown

---

### 12. [fdd-fdd-feature-migration](feature-migration/) ⏳ MEDIUM

- **Purpose**: Add FDD to existing projects with auto-detection and reverse-engineering
- **Status**: NOT_STARTED
- **Depends On**:
  - [feature-adapter-system](feature-adapter-system/)
  - [feature-workflow-engine](feature-workflow-engine/)
- **Blocks**: None
- **Phases**:
  - `ph-1`: ⏳ NOT_STARTED — Auto-detection from existing codebases
  - `ph-2`: ⏳ NOT_STARTED — Reverse-engineering BUSINESS.md and DESIGN.md
- **Requirements Covered**:
  - fdd-fdd-req-migration
- **Scope**:
  - Add FDD to existing projects without disruption
  - Auto-detect tech stack from code and configs
  - Reverse-engineer BUSINESS.md from requirements/PRD docs
  - Extract DESIGN.md patterns from implementation
  - Incremental adoption path (adapter → business → design → features)
  - Legacy system integration with minimal refactoring
  - Traceability tag addition to existing code

---

### 13. [fdd-fdd-feature-documentation](feature-documentation/) ⏳ LOW

- **Purpose**: Interactive documentation, onboarding guides, and pattern examples
- **Status**: NOT_STARTED
- **Depends On**:
  - [feature-core-methodology](feature-core-methodology/)
- **Blocks**: None
- **Phases**:
  - `ph-1`: ⏳ NOT_STARTED — QUICKSTART and progressive disclosure docs
- **Requirements Covered**:
  - fdd-fdd-req-interactive-docs
- **Constraints Affected**:
  - fdd-fdd-constraint-markdown
- **Scope**:
  - QUICKSTART guide (<15 minute bootstrap)
  - README for human readers
  - AGENTS.md for AI agents (progressive disclosure)
  - Valid/invalid pattern examples with ✅/❌ markers
  - Copy-pasteable workflow prompts
  - Methodology version tracking
  - Migration guides for breaking changes

---

## NFR Coverage

**Performance (fdd-fdd-nfr-performance)**:
- Covered by: [feature-validation-engine](feature-validation-engine/), [feature-realtime-validation](feature-realtime-validation/)

**Compatibility (fdd-fdd-nfr-compatibility)**:
- Covered by: [feature-core-methodology](feature-core-methodology/), [feature-adapter-system](feature-adapter-system/)

**Usability (fdd-fdd-nfr-usability)**:
- Covered by: [feature-ai-integration](feature-ai-integration/), [feature-documentation](feature-documentation/)

**Maintainability (fdd-fdd-nfr-maintainability)**:
- Covered by: [feature-core-methodology](feature-core-methodology/), [feature-adapter-system](feature-adapter-system/)

**Extensibility (fdd-fdd-nfr-extensibility)**:
- Covered by: [feature-adapter-system](feature-adapter-system/), [feature-workflow-engine](feature-workflow-engine/)
