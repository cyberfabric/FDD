# Technical Design: FDD

## A. Architecture Overview

### Architectural Vision

FDD (Feature-Driven Design) employs a **layered architecture with plugin-based extensibility** to provide a technology-agnostic methodology framework. The core methodology layer defines universal workflows and validation rules, while the adapter layer enables project-specific customization without modifying core specifications. This separation ensures that FDD remains compatible with any technology stack while maintaining consistent design and validation patterns across all projects.

The architecture follows a **design-first approach** where artifacts are created and validated before implementation proceeds. Each layer builds upon validated artifacts from the previous layer, creating a traceable chain from business requirements through design to implementation. The validation layer uses a **deterministic gate pattern** where automated validators catch structural issues before expensive manual review, ensuring quality while maximizing efficiency.

AI agent integration is achieved through machine-readable specifications (AGENTS.md navigation, workflow files, structure requirements) and a skills-based tooling system. The WHEN clause pattern in AGENTS.md files creates a discoverable navigation system where AI agents can autonomously determine which specifications to follow based on the current workflow context.

### Architecture Layers

```
┌─────────────────────────────────────────────────────────────┐
│                    AI Integration Layer                      │
│  AGENTS.md Navigation • Skills System • Deterministic Gate   │
└─────────────────────────────────────────────────────────────┘
                              ↓
┌─────────────────────────────────────────────────────────────┐
│                      Workflow Layer                          │
│    Operation Workflows • Validation Workflows • FDL          │
└─────────────────────────────────────────────────────────────┘
                              ↓
┌─────────────────────────────────────────────────────────────┐
│                    Validation Layer                          │
│   Deterministic Validators • Scoring System • Traceability   │
└─────────────────────────────────────────────────────────────┘
                              ↓
┌─────────────────────────────────────────────────────────────┐
│                      Adapter Layer                           │
│    Tech Stack • Domain Model Format • Conventions • Specs    │
└─────────────────────────────────────────────────────────────┘
                              ↓
┌─────────────────────────────────────────────────────────────┐
│                   Methodology Core Layer                     │
│   Requirements Files • Workflow Specs • Core AGENTS.md       │
└─────────────────────────────────────────────────────────────┘
```

**Layer Responsibilities**:

- **Methodology Core Layer**: Defines universal FDD structure requirements, workflow specifications, and base AGENTS.md navigation rules. Technology-agnostic and stable across all projects.

- **Adapter Layer**: Project-specific customization through adapter AGENTS.md with Extends mechanism. Contains tech stack definitions, domain model format specs, API contract formats, testing strategies, and coding conventions.

- **Validation Layer**: Deterministic validators implemented in `fdd` skill for structural validation. Includes ID format checking, cross-reference validation, placeholder detection, and code traceability verification.

- **Workflow Layer**: Executable procedures for creating and validating artifacts. Operation workflows (interactive) for artifact creation/update, validation workflows (automated) for quality checks. FDL provides plain-English algorithm descriptions.

- **AI Integration Layer**: WHEN clause navigation system, skills-based tooling, and deterministic gate pattern for AI agent execution. Enables autonomous workflow execution with minimal human intervention.

**Technology Stack per Layer**:

- **Methodology Core**: Markdown (specifications), Python 3 standard library (tooling)
- **Adapter Layer**: JSON (configuration), Markdown (specifications)
- **Validation Layer**: Python 3 standard library (validators), JSON (reports)
- **Workflow Layer**: Markdown (workflows), FDL (algorithms)
- **AI Integration Layer**: Markdown (AGENTS.md), Python 3 (skills), JSON (skill I/O)

---

## B. Requirements & Principles

### B.1: Functional Requirements

#### FR-001: Executable Workflows

**ID**: `fdd-fdd-req-executable-workflows`

**Capabilities**: `fdd-fdd-capability-workflow-execution`

**Actors**: `fdd-fdd-actor-product-manager`, `fdd-fdd-actor-architect`, `fdd-fdd-actor-developer`, `fdd-fdd-actor-business-analyst`, `fdd-fdd-actor-ux-designer`, `fdd-fdd-actor-ai-assistant`

**Use Cases**: `fdd-fdd-usecase-bootstrap-project`, `fdd-fdd-usecase-create-business-context`, `fdd-fdd-usecase-design-feature`, `fdd-fdd-usecase-plan-implementation`

The system MUST provide executable workflows for all phases of development lifecycle. Operation workflows MUST support both CREATE and UPDATE modes. Workflows MUST use interactive question-answer flow with context-based proposals. All artifact creation MUST be followed by automated validation. Workflows MUST be independent and executable in any order based on prerequisites.

#### FR-002: Deterministic Validation

**ID**: `fdd-fdd-req-deterministic-validation`

**Capabilities**: `fdd-fdd-capability-validation`

**Actors**: `fdd-fdd-actor-architect`, `fdd-fdd-actor-developer`, `fdd-fdd-actor-qa-engineer`, `fdd-fdd-actor-security-engineer`, `fdd-fdd-actor-fdd-tool`, `fdd-fdd-actor-ci-pipeline`

**Use Cases**: `fdd-fdd-usecase-validate-design`, `fdd-fdd-usecase-validate-implementation`, `fdd-fdd-usecase-realtime-validation`

The system MUST validate artifact structure deterministically before manual review. Validation MUST use 100-point scoring system with category breakdown. All artifacts MUST have pass thresholds (≥90 or 100/100). Validation MUST check cross-references (actor/capability IDs). The system MUST detect incomplete sections and unfinished content markers. Validation output MUST include detailed issue reporting with recommendations.

#### FR-003: Adapter Configuration

**ID**: `fdd-fdd-req-adapter-configuration`

**Capabilities**: `fdd-fdd-capability-adapter-config`

**Actors**: `fdd-fdd-actor-technical-lead`, `fdd-fdd-actor-architect`, `fdd-fdd-actor-devops-engineer`, `fdd-fdd-actor-ai-assistant`

**Use Cases**: `fdd-fdd-usecase-bootstrap-project`, `fdd-fdd-usecase-auto-generate-adapter`, `fdd-fdd-usecase-migrate-project`, `fdd-fdd-usecase-configure-cicd`

The system MUST support project-specific adapters without modifying core methodology. Adapters MUST define tech stack (languages, frameworks, tools). Adapters MUST specify domain model format (GTS, JSON Schema, Protobuf, etc.). Adapters MUST specify API contract format (OpenAPI, GraphQL, CLISPEC, etc.). The system MUST support auto-detection of tech stack from existing codebase. Adapter AGENTS.md MUST extend core AGENTS.md using Extends mechanism.

#### FR-004: Design-First Development

**ID**: `fdd-fdd-req-design-first`

**Capabilities**: `fdd-fdd-capability-design-first`

**Actors**: `fdd-fdd-actor-product-manager`, `fdd-fdd-actor-architect`, `fdd-fdd-actor-developer`, `fdd-fdd-actor-business-analyst`, `fdd-fdd-actor-ux-designer`, `fdd-fdd-actor-security-engineer`

**Use Cases**: `fdd-fdd-usecase-create-business-context`, `fdd-fdd-usecase-design-feature`, `fdd-fdd-usecase-update-feature-design`

The system MUST enforce design artifact creation before implementation. Design artifacts MUST be validated for completeness before coding begins. Design MUST be single source of truth with code following design specifications. The system MUST support design iteration through UPDATE workflows. Design MUST clearly separate business context (BUSINESS.md), architecture (DESIGN.md), and features (feature DESIGN.md). Behavioral specifications MUST use FDL (plain-English algorithms).

#### FR-005: Traceability Management

**ID**: `fdd-fdd-req-traceability`

**Capabilities**: `fdd-fdd-capability-traceability`

**Actors**: `fdd-fdd-actor-developer`, `fdd-fdd-actor-qa-engineer`, `fdd-fdd-actor-fdd-tool`

**Use Cases**: `fdd-fdd-usecase-trace-requirement`, `fdd-fdd-usecase-implement-change`, `fdd-fdd-usecase-validate-implementation`

The system MUST assign unique IDs to all design elements using format `fdd-{project}-{kind}-{name}`. Code MUST use @fdd-* tags linking implementation to design. The system MUST support qualified IDs for phases and instructions (:ph-N:inst-name format). The system MUST provide repository-wide ID scanning and search. The system MUST provide where-defined and where-used commands. Validation MUST verify implemented items have corresponding code tags.

#### FR-006: AI Agent Integration

**ID**: `fdd-fdd-req-ai-integration`

**Capabilities**: `fdd-fdd-capability-ai-integration`

**Actors**: `fdd-fdd-actor-ai-assistant`, `fdd-fdd-actor-technical-lead`

**Use Cases**: `fdd-fdd-usecase-bootstrap-project`, `fdd-fdd-usecase-design-feature`, `fdd-fdd-usecase-implement-change`, `fdd-fdd-usecase-validate-design`

The system MUST provide AGENTS.md navigation with WHEN clause rules. All workflow specifications MUST be machine-readable. The system MUST use structured prompts for AI interaction. The adapter system MUST support extension (core + project customization). The system MUST provide skills system for Claude-compatible tools. Validation MUST use deterministic gate pattern (fail fast before LLM validation).

#### FR-007: Interactive Documentation

**ID**: `fdd-fdd-req-interactive-docs`

**Capabilities**: `fdd-fdd-capability-interactive-docs`

**Actors**: `fdd-fdd-actor-documentation-writer`, `fdd-fdd-actor-product-manager`, `fdd-fdd-actor-release-manager`, `fdd-fdd-actor-ai-assistant`, `fdd-fdd-actor-doc-generator`

**Use Cases**: `fdd-fdd-usecase-bootstrap-project`, `fdd-fdd-usecase-business-analysis`

All specifications MUST be executable by humans or AI. Artifact structure MUST be enforced by validation (self-documenting). Documentation MUST include valid/invalid pattern examples with ✅/❌ markers. The system MUST provide QUICKSTART guide with copy-paste prompts. Documentation MUST use progressive disclosure (README for humans, AGENTS.md for AI). Methodology MUST track version for evolution.

#### FR-008: ADR Management

**ID**: `fdd-fdd-req-arch-decision-mgmt`

**Capabilities**: `fdd-fdd-capability-arch-decision-mgmt`

**Actors**: `fdd-fdd-actor-architect`, `fdd-fdd-actor-technical-lead`, `fdd-fdd-actor-security-engineer`

**Use Cases**: `fdd-fdd-usecase-record-adr`, `fdd-fdd-usecase-security-review`

**ADRs**: `fdd-fdd-adr-0001`

The system MUST support creation and tracking of architecture decisions with structured format. ADRs MUST link to affected design sections and features. The system MUST track decision status (PROPOSED, ACCEPTED, DEPRECATED, SUPERSEDED). The system MUST support impact analysis when ADR changes affect features. The system MUST provide ADR search by status, date, or affected components. ADRs MUST maintain version history for decision evolution.

#### FR-009: Feature Lifecycle Management

**ID**: `fdd-fdd-req-feature-lifecycle`

**Capabilities**: `fdd-fdd-capability-feature-lifecycle`

**Actors**: `fdd-fdd-actor-project-manager`, `fdd-fdd-actor-release-manager`, `fdd-fdd-actor-developer`, `fdd-fdd-actor-ai-assistant`

**Use Cases**: `fdd-fdd-usecase-plan-release`, `fdd-fdd-usecase-track-feature-lifecycle`

The system MUST track feature status from NOT_STARTED through IN_PROGRESS to DONE. Status updates MUST be automated based on CHANGES.md completion. The system MUST manage feature dependencies and detect blocking. The system MUST integrate with milestone tracking and release planning. The system MUST track historical feature completion metrics and velocity. Status transitions MUST be validated (cannot skip states).

#### FR-010: Incremental Development Support

**ID**: `fdd-fdd-req-incremental-development`

**Capabilities**: `fdd-fdd-capability-incremental-development`

**Actors**: `fdd-fdd-actor-architect`, `fdd-fdd-actor-developer`, `fdd-fdd-actor-product-manager`, `fdd-fdd-actor-ai-assistant`

**Use Cases**: `fdd-fdd-usecase-update-feature-design`, `fdd-fdd-usecase-plan-implementation`

All operation workflows MUST support CREATE and UPDATE modes. UPDATE mode MUST preserve existing content when updating artifacts. The system MUST support partial updates without full regeneration. Change history MUST be tracked through Git integration. Designs and features MUST support iterative refinement. Updates MUST NOT lose data (unchanged sections preserved).

#### FR-011: Code Generation from Design

**ID**: `fdd-fdd-req-code-generation`

**Capabilities**: `fdd-fdd-capability-code-generation`

**Actors**: `fdd-fdd-actor-developer`, `fdd-fdd-actor-ai-assistant`

**Use Cases**: `fdd-fdd-usecase-generate-code`, `fdd-fdd-usecase-implement-change`

The system MUST generate code scaffolding from feature DESIGN.md specifications. The system MUST create API endpoints from Section E (API Contracts). The system MUST generate domain types from Section C.2 (Domain Model). The system MUST produce test stubs from Section D (Test Cases). Code generation MUST use adapter specs for language-specific output. The system MUST add traceability tags automatically during generation.

#### FR-012: Cross-Project Patterns

**ID**: `fdd-fdd-req-pattern-reusability`

**Capabilities**: `fdd-fdd-capability-pattern-reusability`

**Actors**: `fdd-fdd-actor-technical-lead`, `fdd-fdd-actor-architect`, `fdd-fdd-actor-devops-engineer`

The system MUST support extracting common patterns from one project to another. Adapter specs MUST be reusable across similar projects. The system MUST support shared workflow customizations and templates. The system MUST manage pattern library with versioning. The system MUST provide template repositories for common architectures. The system MUST propagate organization-wide best practices.

#### FR-013: Migration and Integration

**ID**: `fdd-fdd-req-migration`

**Capabilities**: `fdd-fdd-capability-migration`

**Actors**: `fdd-fdd-actor-technical-lead`, `fdd-fdd-actor-architect`, `fdd-fdd-actor-ai-assistant`

**Use Cases**: `fdd-fdd-usecase-migrate-project`, `fdd-fdd-usecase-auto-generate-adapter`

The system MUST add FDD to existing projects without disruption. The system MUST auto-detect existing architecture from code and configs. The system MUST reverse-engineer BUSINESS.md from requirements documentation. The system MUST extract DESIGN.md patterns from implementation. FDD adoption MUST be incremental (adapter → business → design → features). The system MUST integrate with legacy systems with minimal refactoring.

#### FR-014: Real-Time Validation Feedback

**ID**: `fdd-fdd-req-realtime-validation`

**Capabilities**: `fdd-fdd-capability-realtime-validation`

**Actors**: `fdd-fdd-actor-architect`, `fdd-fdd-actor-developer`, `fdd-fdd-actor-fdd-tool`

**Use Cases**: `fdd-fdd-usecase-realtime-validation`, `fdd-fdd-usecase-ide-navigation`

The system MUST validate artifacts as they are edited in IDE. The system MUST provide instant feedback on ID format errors. The system MUST perform real-time cross-reference checking. The system MUST detect placeholders in real-time. Validation MUST be incremental (only changed sections). Validation MUST run in background without blocking editing.

#### FR-015: FDL Support

**ID**: `fdd-fdd-req-fdl`

**Capabilities**: `fdd-fdd-capability-fdl`

**Actors**: `fdd-fdd-actor-architect`, `fdd-fdd-actor-developer`, `fdd-fdd-actor-business-analyst`, `fdd-fdd-actor-ux-designer`

**Use Cases**: `fdd-fdd-usecase-write-fdl-flow`, `fdd-fdd-usecase-design-feature`, `fdd-fdd-usecase-design-ui`

The system MUST provide plain English algorithm description language for actor flows. FDL MUST use structured numbered lists with bold keywords (**IF**, **ELSE**, **WHILE**, **FOR EACH**). FDL MUST support instruction markers with checkboxes (- [ ] Inst-label: description). FDL MUST organize by phases (ph-1, ph-2, etc.) for implementation tracking. FDL MUST be readable by non-programmers for validation and review. FDL MUST translate directly to code with traceability tags. FDL MUST support keywords: **AND**, **OR**, **NOT**, **MUST**, **REQUIRED**, **OPTIONAL**.

#### FR-016: IDE Integration

**ID**: `fdd-fdd-req-ide-integration`

**Capabilities**: `fdd-fdd-capability-ide-integration`

**Actors**: `fdd-fdd-actor-developer`, `fdd-fdd-actor-architect`, `fdd-fdd-actor-devops-engineer`

**Use Cases**: `fdd-fdd-usecase-ide-navigation`, `fdd-fdd-usecase-realtime-validation`

The system MUST generate IDE-specific configurations from adapter specs. The system MUST support click-to-navigate from ID references to definitions. The system MUST provide syntax highlighting for FDL in Markdown. The system MUST integrate with IDE file watchers for auto-validation. The system MUST generate .cursorrules and .windsurf/ configs. IDE integration MUST be optional and non-intrusive.

### B.2: Non-Functional Requirements

#### NFR-001: Performance

**ID**: `fdd-fdd-nfr-performance`

Deterministic validators MUST complete in <5 seconds for typical artifacts (<2000 lines). ID scanning across repository MUST complete in <30 seconds for repositories with <10,000 files. Workflow execution overhead MUST be <10% of total development time. Real-time validation MUST provide feedback within 1 second of edit. Validation reports MUST be generated in JSON format for fast parsing.

#### NFR-002: Compatibility

**ID**: `fdd-fdd-nfr-compatibility`

The methodology MUST work with any programming language through adapter system. The system MUST support any domain model format (GTS, JSON Schema, Protobuf, TypeScript, etc.). The system MUST support any API contract format (OpenAPI, GraphQL, gRPC, CLISPEC, etc.). The core MUST use only Python 3.6+ standard library (no external dependencies). All specifications MUST be plain Markdown (compatible with all editors).

#### NFR-003: Usability

**ID**: `fdd-fdd-nfr-usability`

AI agents MUST execute workflows with ≥95% success rate without human intervention. QUICKSTART guide MUST enable new users to bootstrap project in <15 minutes. Workflow prompts MUST be copy-pasteable for immediate execution. Error messages MUST include specific fix suggestions. Documentation MUST use progressive disclosure (simple → advanced).

#### NFR-004: Maintainability

**ID**: `fdd-fdd-nfr-maintainability`

Methodology updates MUST preserve existing artifact structure. Breaking changes MUST provide migration paths and version documentation. Core methodology MUST be decoupled from adapter specifications. Validation rules MUST be extracted to requirements files (not hardcoded). All workflows MUST follow standardized structure for consistency.

#### NFR-005: Extensibility

**ID**: `fdd-fdd-nfr-extensibility`

Projects MUST adopt FDD incrementally (adapter → business → design → features). Adapter system MUST support adding new spec files without core changes. Skills system MUST support adding new tools via standard interface. Workflow system MUST support custom workflows via extension mechanism. Validation scoring MUST be configurable per project via adapter.

### B.3: Design Principles

#### Principle 1: Technology Agnostic Core

**ID**: `fdd-fdd-principle-tech-agnostic`

**ADRs**: `fdd-fdd-adr-0001`

The core methodology MUST have zero technology dependencies. All technology choices MUST be in adapters, not core. The core MUST work equally well for Python, Rust, JavaScript, Java, Go, or any language. Domain model formats, API contract formats, and testing frameworks MUST be configurable per project. This principle ensures FDD remains universally applicable across all technology ecosystems.

#### Principle 2: Design Before Code

**ID**: `fdd-fdd-principle-design-first`

**ADRs**: `fdd-fdd-adr-0001`

All artifacts MUST be validated before implementation proceeds. Design is the single source of truth; code follows design specifications. Validation gates MUST prevent proceeding to next phase without passing quality threshold. This principle ensures thoughtful architecture and reduces technical debt by catching design issues before they become code issues.

#### Principle 3: Machine-Readable Specifications

**ID**: `fdd-fdd-principle-machine-readable`

**ADRs**: `fdd-fdd-adr-0001`

Domain models MUST be in parseable formats (not plain text descriptions). API contracts MUST be in machine-readable formats for validation and code generation. Workflow specifications MUST be structured for AI agent consumption. ID formats MUST be regular expressions for deterministic validation. This principle enables automation, reduces manual effort, and ensures consistency.

#### Principle 4: Progressive Validation

**ID**: `fdd-fdd-principle-deterministic-gate`

**ADRs**: `fdd-fdd-adr-0001`

Deterministic validators MUST run before manual review (Deterministic Gate pattern). Validators MUST fail fast on structural errors to save time. Manual validation MUST focus on design quality, not format checking. Validation layers (deterministic → manual → peer review) MUST be sequential. This principle maximizes efficiency by catching obvious errors immediately and reserving human attention for complex design decisions.

#### Principle 5: Traceability By Design

**ID**: `fdd-fdd-principle-traceability`

**ADRs**: `fdd-fdd-adr-0001`

Every design element MUST have a unique ID assigned at creation. Code tags (@fdd-*) MUST link implementation to specifications. Qualified IDs (base:ph-N:inst-name) MUST enable granular traceability. Repository-wide scanning MUST verify design-code mapping. This principle maintains design-code coherence and enables impact analysis when designs change.

### B.4: Constraints

#### Constraint 1: Python Standard Library Only

**ID**: `fdd-fdd-constraint-stdlib-only`

The `fdd` validation tool MUST use only Python 3.6+ standard library. No external dependencies (pip packages) are permitted in core tooling. This constraint ensures FDD can run anywhere Python is available without complex installation or dependency management. Adapters may use any dependencies for project-specific code generation.

#### Constraint 2: Markdown-Only Artifacts

**ID**: `fdd-fdd-constraint-markdown`

All FDD artifacts (BUSINESS.md, DESIGN.md, ADR.md, FEATURES.md, etc.) MUST be plain Markdown. No binary formats, proprietary tools, or custom file formats permitted. This constraint ensures artifacts are version-controllable, diffable, and editable in any text editor. Domain models and API contracts referenced by artifacts may be in any format (specified by adapter).

#### Constraint 3: Git-Based Workflow

**ID**: `fdd-fdd-constraint-git`

FDD assumes Git version control for artifact history and collaboration. Change tracking relies on Git commits and diffs. Feature branches and pull requests are the collaboration model. This constraint aligns FDD with modern development practices but requires Git knowledge from users.

#### Constraint 4: No Forced Tool Dependencies

**ID**: `fdd-fdd-constraint-no-forced-tools`

FDD core MUST NOT require specific IDEs, editors, or development tools. Validation MUST run from command line without GUI tools. IDE integrations are optional enhancements, not requirements. This constraint ensures FDD works in any development environment (local, remote, CI/CD, etc.).

---

## C. Technical Architecture

### C.1: Component Architecture

The FDD system consists of 6 core components organized in a layered architecture:

```
┌──────────────────────────────────────────────────────────────────────┐
│                      AI Integration Layer                            │
│  ┌──────────────────────────────────────────────────────────────┐   │
│  │ AGENTS.md Navigation: WHEN clause rules, Extends mechanism  │   │
│  │ Skills System: fdd tool, future extensions                   │   │
│  │ Deterministic Gate: Fast failure on structural issues        │   │
│  └──────────────────────────────────────────────────────────────┘   │
└──────────────────────────────────────────────────────────────────────┘
                                  ↓
┌──────────────────────────────────────────────────────────────────────┐
│                         Workflow Engine                              │
│  ┌──────────────────────────────────────────────────────────────┐   │
│  │ Operation Workflows: CREATE/UPDATE modes, interactive Q&A    │   │
│  │ Validation Workflows: Automated quality checks               │   │
│  │ FDL Engine: Plain-English algorithm processing              │   │
│  └──────────────────────────────────────────────────────────────┘   │
└──────────────────────────────────────────────────────────────────────┘
                                  ↓
┌──────────────────────────────────────────────────────────────────────┐
│                       Validation Engine                              │
│  ┌──────────────────────────────────────────────────────────────┐   │
│  │ Deterministic Validators: Structure, IDs, placeholders       │   │
│  │ Scoring System: 100-point breakdown with thresholds          │   │
│  │ Traceability Checks: Design-code mapping verification        │   │
│  └──────────────────────────────────────────────────────────────┘   │
└──────────────────────────────────────────────────────────────────────┘
                                  ↓
┌──────────────────────────────────────────────────────────────────────┐
│                          ID Management                               │
│  ┌──────────────────────────────────────────────────────────────┐   │
│  │ ID Generation: fdd-{project}-{kind}-{name} format           │   │
│  │ Qualified IDs: :ph-N:inst-name extensions                    │   │
│  │ Cross-References: Actor/capability/requirement validation    │   │
│  │ Repository Scanning: where-defined, where-used               │   │
│  └──────────────────────────────────────────────────────────────┘   │
└──────────────────────────────────────────────────────────────────────┘
                                  ↓
┌──────────────────────────────────────────────────────────────────────┐
│                         Adapter System                               │
│  ┌──────────────────────────────────────────────────────────────┐   │
│  │ Adapter AGENTS.md: Extends core, WHEN clauses for specs     │   │
│  │ Spec Files: tech-stack, domain-model, conventions, etc.     │   │
│  │ Auto-Detection: Reverse-engineer from existing code         │   │
│  └──────────────────────────────────────────────────────────────┘   │
└──────────────────────────────────────────────────────────────────────┘
                                  ↓
┌──────────────────────────────────────────────────────────────────────┐
│                       Methodology Core                               │
│  ┌──────────────────────────────────────────────────────────────┐   │
│  │ Requirements Files: *-structure.md specifications            │   │
│  │ Workflow Specs: Markdown files with steps and validations    │   │
│  │ Core AGENTS.md: Base navigation rules                        │   │
│  └──────────────────────────────────────────────────────────────┘   │
└──────────────────────────────────────────────────────────────────────┘
```

**Component Descriptions**:

**1. Methodology Core**
- Contains universal FDD specifications (requirements files, workflow files, core AGENTS.md)
- Defines artifact structure requirements (*-structure.md)
- Provides workflow templates (workflows/*.md)
- Technology-agnostic and stable across all projects
- Location: `FDD/` directory (requirements/, workflows/, AGENTS.md)

**2. Adapter System**
- Project-specific customization layer
- Adapter AGENTS.md extends core AGENTS.md via **Extends** mechanism
- Spec files define tech stack, domain model format, API contracts, conventions
- Auto-detection capability for existing codebases
- Location: `{project}/.adapter/` or configured path

**3. ID Management**
- Generates and validates unique IDs for all design elements
- Format: `fdd-{project}-{kind}-{name}` (lowercase kebab-case)
- Supports qualified IDs for implementation tracking (:ph-N:inst-name)
- Provides repository-wide scanning (scan-ids, where-defined, where-used)
- Validates cross-references between artifacts

**4. Validation Engine**
- Deterministic validators for structural checking (fdd tool)
- 100-point scoring system with category breakdown
- Pass thresholds: ≥90/100 for most artifacts, 100/100 for feature designs
- Checks: required sections, ID formats, cross-references, placeholders
- Code traceability validation (@fdd-* tags in code)
- Implemented in: `skills/fdd/scripts/fdd.py`

**5. Workflow Engine**
- Operation workflows: Interactive CREATE/UPDATE for artifacts
- Validation workflows: Automated quality checks
- FDL processing: Plain-English algorithms with instruction markers
- Question-answer flow with context-based proposals
- Execution protocol: Prerequisites check → Specification reading → Interactive input → Content generation → Validation

**6. AI Integration Layer**
- AGENTS.md navigation: WHEN clause rules determine which specs to follow
- Skills system: Claude-compatible tools (fdd skill, future extensions)
- Deterministic gate pattern: Automated validators run before manual review
- Machine-readable specifications enable autonomous execution
- Structured prompts guide AI interactions

**Component Interactions**:

1. **AI Agent → Workflow Engine**: AGENTS.md navigation determines workflow to execute
2. **Workflow Engine → Adapter System**: Reads adapter specs for project conventions
3. **Workflow Engine → ID Management**: Generates IDs for new design elements
4. **Workflow Engine → Validation Engine**: Runs validators after artifact creation
5. **Validation Engine → ID Management**: Validates ID formats and cross-references
6. **Validation Engine → Methodology Core**: Uses requirements files as validation rules
7. **All Components → Methodology Core**: Reference requirements for specifications

### C.2: Domain Model

**Technology**: Markdown-based artifacts (not code-level types)

**Location**: 
- Artifact structure: `requirements/*-structure.md`
- ID format specification: `.adapter/specs/domain-model.md`
- Artifact examples: `architecture/BUSINESS.md`, workflow files

**Core Entities**:

**Artifacts**:
- `BUSINESS.md` (business context): Vision, Actors, Capabilities, Use Cases
- `DESIGN.md` (overall design): Architecture, Requirements, Technical Details
- `ADR.md` (architecture decisions): MADR-formatted decision records
- `FEATURES.md` (feature manifest): Feature list with status tracking
- `DESIGN.md` (feature scope): Feature specifications with flows, algorithms, states
- `CHANGES.md` (implementation plan): Atomic changes with task breakdown

**IDs**:
- Actor ID: `fdd-{project}-actor-{name}`
- Capability ID: `fdd-{project}-capability-{name}`
- Use Case ID: `fdd-{project}-usecase-{name}`
- Requirement ID: `fdd-{project}-req-{name}`
- Feature ID: `fdd-{project}-feature-{name}`
- Flow ID: `fdd-{project}-feature-{feature}-flow-{name}`
- Algorithm ID: `fdd-{project}-feature-{feature}-algo-{name}`
- State ID: `fdd-{project}-feature-{feature}-state-{name}`
- ADR ID: `ADR-{NNNN}` or `fdd-{project}-adr-{name}`

**Workflows**:
- Operation workflow (Type: Operation): Interactive artifact creation/update
- Validation workflow (Type: Validation): Automated quality checks

**Relationships**:
- BUSINESS.md defines Actors and Capabilities
- DESIGN.md references Actors/Capabilities, defines Requirements
- FEATURES.md references Requirements, lists Features
- Feature DESIGN.md references Actors, defines Flows/Algorithms/States
- CHANGES.md references Requirements from feature DESIGN.md
- ADR.md referenced by Requirements/Principles/Constraints

**CRITICAL**: Domain model is Markdown-based artifact structure, not programming language types. Validation checks structure against requirements files, not type compilation.

### C.3: API Contracts

**Technology**: CLISPEC for command-line interface (fdd tool)

**Location**: 
- Format specification: `CLISPEC.md`
- Command specification: `skills/fdd/fdd.clispec`
- Implementation: `skills/fdd/scripts/fdd.py`

**Endpoints Overview**:

**Validation Commands**:
- `validate --artifact {path}`: Validate artifact structure
- `validate --artifact {code-root}`: Code traceability scan

**Search Commands**:
- `list-sections --artifact {path}`: List document headings
- `list-ids --artifact {path}`: List all IDs
- `list-items --artifact {path}`: List typed items (actors, capabilities, etc.)
- `read-section --artifact {path} --section {A|B|C}`: Read section content
- `get-item --artifact {path} --id {id}`: Get specific item
- `find-id --artifact {path} --id {id}`: Find ID location
- `search --artifact {path} --query {text}`: Text search

**Traceability Commands**:
- `scan-ids --root {path}`: Scan all IDs in directory
- `where-defined --root {path} --id {id}`: Find normative definition
- `where-used --root {path} --id {id}`: Find all usages

**Adapter Discovery**:
- `adapter-info --root {path}`: Discover adapter configuration

**CRITICAL**: API contracts are CLISPEC format (command-line interface specification), not REST/HTTP. All commands output JSON for machine consumption.

### C.4: Security Model

**Authentication**: None (local command-line tool)

**Authorization**: File system permissions only

**Data Protection**: 
- No sensitive data collection or transmission
- All processing is local to developer machine
- No network requests or external API calls
- Git history contains all changes (audit trail)

**Security Boundaries**:
- Tool runs with user's file system permissions
- No privilege escalation required
- Read-only operations for search/traceability commands
- Write operations only for validation (report generation)
- Workflows create files only after user confirmation

**Note**: FDD is a methodology framework for design documentation, not a security-critical system. Security considerations are minimal as all operations are local and user-controlled.

### C.5: Non-Functional Requirements

See Section B.2 for complete NFR specifications:
- **NFR-001: Performance** - Validation speed, scanning performance
- **NFR-002: Compatibility** - Language/framework agnostic
- **NFR-003: Usability** - AI agent success rate, onboarding time
- **NFR-004: Maintainability** - Update compatibility, migration paths
- **NFR-005: Extensibility** - Incremental adoption, adapter system

---

## D. Additional Context

### Technology Selection Rationale

**Python 3 Standard Library Only**: Chosen for maximum portability and zero installation complexity. Python 3.6+ is available on most development machines. Standard library ensures no dependency management or version conflicts.

**Markdown for Artifacts**: Universal format compatible with all editors, version control systems, and documentation platforms. Plain text ensures longevity and accessibility. Syntax highlighting and rendering available in all modern development tools.

**CLISPEC for API**: Command-line interface is most compatible with CI/CD pipelines, remote development, and automation scripts. JSON output enables machine consumption and integration with other tools.

**GTS for FDD's Own Domain Model**: While FDD supports any domain model format via adapters, FDD itself uses GTS (Global Type System) for domain type definitions as a demonstration of machine-readable specifications.

### Implementation Considerations

**Incremental Adoption Path**:
1. Start with adapter (minimal: just Extends line)
2. Add BUSINESS.md (business context)
3. Add DESIGN.md (architecture)
4. Optionally add ADR.md (decisions)
5. Add FEATURES.md and feature designs
6. Add CHANGES.md and implement
7. Evolve adapter as patterns emerge

**Migration from Existing Projects**:
- Use `adapter-from-sources` workflow to auto-detect tech stack
- Reverse-engineer BUSINESS.md from existing requirements/PRD
- Extract DESIGN.md patterns from code structure and documentation
- Add traceability incrementally (new code first, legacy later)

**AI Agent Best Practices**:
- Always run `fdd adapter-info` before starting any workflow
- Use deterministic gate (fdd validate) before manual validation
- Follow execution-protocol.md for all workflow executions
- Use fdd skill for artifact search and ID lookup
- Never skip prerequisites validation

### Future Technical Improvements

**Performance Optimizations**:
- Caching for repository-wide ID scans (currently re-scans on each query)
- Incremental validation (only validate changed sections)
- Parallel processing for multi-artifact validation

**Enhanced Traceability**:
- Visual traceability graphs (actor → capability → requirement → code)
- Impact analysis UI (show all affected artifacts when changing design)
- Coverage metrics dashboard (% of requirements implemented, tested)

**IDE Integration Enhancements**:
- Language server protocol (LSP) for real-time validation
- Quick fixes for common validation errors
- Hover tooltips showing ID definitions
- Auto-completion for FDD IDs and references

**Adapter Ecosystem**:
- Public adapter registry for common tech stacks
- Adapter composition (extend multiple adapters)
- Adapter versioning and compatibility checking
- Community-contributed patterns and templates

---

## FDD Files Read During DESIGN.md Creation

**Required by Execution Protocol**:
- `workflows/AGENTS.md` - Initial navigation (line 7: select design workflow)
- `requirements/execution-protocol.md` - Mandatory pre-execution protocol
- `requirements/workflow-selection.md` - Workflow selection (line 84-96: design.md)
- `requirements/workflow-execution.md` - General execution rules
- `requirements/workflow-execution-operations.md` - Operation workflow specifics
- `workflows/design.md` - Specific workflow for overall design creation
- `requirements/overall-design-structure.md` - DESIGN.md structure requirements

**Adapter Discovery**:
- `.adapter/AGENTS.md` - Adapter navigation (line 13-25: WHEN clauses for design.md)
- `.adapter/specs/tech-stack.md` - Technology stack specification
- `.adapter/specs/domain-model.md` - Domain model format and ID patterns
- `.adapter/specs/patterns.md` - Architectural patterns and conventions

**Prerequisites**:
- `architecture/BUSINESS.md` - Parent artifact (actors, capabilities, use cases extracted)