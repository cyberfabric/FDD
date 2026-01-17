# Business Context: FDD

## A. Vision

**Purpose**: FDD (Feature-Driven Design) is a universal methodology for building software systems with complete traceability from business requirements to implementation. It enables development teams to design before coding, validate designs systematically, and integrate seamlessly with AI coding assistants through structured workflows and machine-readable specifications.

**Target Users**:
- Development Teams - Building software with clear design documentation
- Technical Leads & Architects - Defining system architecture and technical decisions
- Product Managers - Capturing business requirements and use cases
- AI Coding Assistants - Executing workflows and validating artifacts
- QA Engineers - Verifying implementation matches design
- Documentation Writers - Creating comprehensive technical documentation

**Key Problems Solved**:
- **Design-Code Disconnect**: Code diverges from design without single source of truth, leading to outdated documentation
- **Lack of Traceability**: Cannot track business requirements through design to implementation, making impact analysis difficult
- **Unstructured Development**: No repeatable process for design and implementation, causing inconsistent quality
- **AI Integration Challenges**: AI agents cannot follow methodology without structured guidance and machine-readable specifications
- **Validation Complexity**: Manual design reviews are time-consuming and miss structural issues

**Success Criteria**:
- 100% design-code traceability through FDD IDs and code tags (@fdd-* markers)
- 20+ executable workflows covering entire development lifecycle (operation + validation)
- Validation accuracy ≥95% (deterministic validators catch structural issues before manual review)
- Support any tech stack through adapter system (zero forced technology choices)
- AI agents can execute workflows autonomously with minimal human intervention

---

## B. Actors

**Human Actors**:

#### Product Manager

**ID**: `fdd-fdd-actor-product-manager`  
**Role**: Defines business requirements, captures use cases, and documents business context using FDD workflows

#### Architect

**ID**: `fdd-fdd-actor-architect`  
**Role**: Designs system architecture, creates overall design documentation, and defines technical patterns

#### Developer

**ID**: `fdd-fdd-actor-developer`  
**Role**: Implements features according to validated designs, adds traceability tags to code

#### QA Engineer

**ID**: `fdd-fdd-actor-qa-engineer`  
**Role**: Validates implementation against design specifications and ensures test coverage

#### Technical Lead

**ID**: `fdd-fdd-actor-technical-lead`  
**Role**: Sets up project adapters, configures FDD for project-specific conventions

#### Project Manager

**ID**: `fdd-fdd-actor-project-manager`  
**Role**: Monitors development progress, ensures workflows are followed, tracks feature completion

#### Documentation Writer

**ID**: `fdd-fdd-actor-documentation-writer`  
**Role**: Creates and maintains project documentation using FDD artifacts as source

#### DevOps Engineer

**ID**: `fdd-fdd-actor-devops-engineer`  
**Role**: Configures CI/CD pipelines, uses adapter specs for build and deployment automation

#### Security Engineer

**ID**: `fdd-fdd-actor-security-engineer`  
**Role**: Conducts security review of design and code, validates security requirements implementation

#### Business Analyst

**ID**: `fdd-fdd-actor-business-analyst`  
**Role**: Analyzes business requirements and translates them into FDD format for Product Manager

#### UX Designer

**ID**: `fdd-fdd-actor-ux-designer`  
**Role**: Designs user interfaces based on actor flows from feature DESIGN.md

#### Release Manager

**ID**: `fdd-fdd-actor-release-manager`  
**Role**: Manages releases and tracks feature readiness through FEATURES.md status

**System Actors**:

#### AI Coding Assistant

**ID**: `fdd-fdd-actor-ai-assistant`  
**Role**: Executes FDD workflows interactively, generates artifacts, and validates against requirements

#### FDD Validation Tool

**ID**: `fdd-fdd-actor-fdd-tool`  
**Role**: Automated validation engine that checks artifact structure, ID formats, and traceability

#### CI/CD Pipeline

**ID**: `fdd-fdd-actor-ci-pipeline`  
**Role**: Automatically validates FDD artifacts on every commit through GitHub Actions or GitLab CI

#### Documentation Generator

**ID**: `fdd-fdd-actor-doc-generator`  
**Role**: Automatically generates external documentation from FDD artifacts (API docs, architecture diagrams)

---

## C. Capabilities

#### Workflow-Driven Development

**ID**: `fdd-fdd-capability-workflow-execution`  
- 20+ executable workflows (13 operation + 7 validation)
- CREATE and UPDATE modes for all operation workflows
- Interactive question-answer flow with AI agents
- Automated validation after artifact creation
- Step-by-step guidance for complex operations
- Independent workflows (no forced sequence)

**Actors**: `fdd-fdd-actor-product-manager`, `fdd-fdd-actor-architect`, `fdd-fdd-actor-developer`, `fdd-fdd-actor-business-analyst`, `fdd-fdd-actor-ux-designer`, `fdd-fdd-actor-ai-assistant`

#### Artifact Structure Validation

**ID**: `fdd-fdd-capability-validation`  
- Deterministic validators for structural checks (sections, IDs, format)
- 100-point scoring system with category breakdown
- Pass/fail thresholds (typically ≥90 or 100/100)
- Cross-reference validation (actor/capability IDs)
- Placeholder detection (incomplete markers)
- Detailed issue reporting with recommendations

**Actors**: `fdd-fdd-actor-architect`, `fdd-fdd-actor-developer`, `fdd-fdd-actor-qa-engineer`, `fdd-fdd-actor-security-engineer`, `fdd-fdd-actor-fdd-tool`, `fdd-fdd-actor-ci-pipeline`

#### Adapter Configuration System

**ID**: `fdd-fdd-capability-adapter-config`  
- Technology-agnostic core methodology
- Project-specific adapter specifications
- Tech stack definition (languages, frameworks, tools)
- Domain model format specification (GTS, JSON Schema, Protobuf, etc.)
- API contract format specification (OpenAPI, GraphQL, CLISPEC, etc.)
- Testing strategy and build tool configuration
- Auto-detection from existing codebase

**Actors**: `fdd-fdd-actor-technical-lead`, `fdd-fdd-actor-architect`, `fdd-fdd-actor-devops-engineer`, `fdd-fdd-actor-ai-assistant`

#### Design-First Development

**ID**: `fdd-fdd-capability-design-first`  
- Design artifacts created before implementation
- Validation ensures design completeness before coding
- Design is single source of truth (code follows design)
- Design iteration through UPDATE workflows
- Clear separation between business (BUSINESS.md), architecture (DESIGN.md), and features
- FDL (FDD Description Language) for plain-English algorithms

**Actors**: `fdd-fdd-actor-product-manager`, `fdd-fdd-actor-architect`, `fdd-fdd-actor-developer`, `fdd-fdd-actor-business-analyst`, `fdd-fdd-actor-ux-designer`, `fdd-fdd-actor-security-engineer`

#### Traceability Management

**ID**: `fdd-fdd-capability-traceability`  
- Unique ID system for all design elements using structured format
- Code tags (@fdd-*) linking implementation to design
- Qualified IDs for phases and instructions (:ph-N:inst-name)
- Repository-wide ID scanning and search
- where-defined and where-used commands
- Design-to-code validation (implemented items must have code tags)

**Actors**: `fdd-fdd-actor-developer`, `fdd-fdd-actor-qa-engineer`, `fdd-fdd-actor-fdd-tool`

#### AI Agent Integration

**ID**: `fdd-fdd-capability-ai-integration`  
- AGENTS.md navigation system (WHEN clause rules)
- Machine-readable workflow specifications
- Structured prompts for AI interaction
- Adapter extension mechanism (core + project customization)
- Skills system for Claude-compatible tools
- Deterministic gate pattern (fail fast before LLM validation)

**Actors**: `fdd-fdd-actor-ai-assistant`, `fdd-fdd-actor-technical-lead`

#### Interactive Documentation

**ID**: `fdd-fdd-capability-interactive-docs`  
- Executable specifications (workflows can be followed by humans or AI)
- Self-documenting artifacts (structure enforced by validation)
- Examples with valid/invalid patterns (✅/❌ markers)
- QUICKSTART guide with copy-paste prompts
- Progressive disclosure (README for humans, AGENTS.md for AI)
- Version control for methodology evolution

**Actors**: `fdd-fdd-actor-documentation-writer`, `fdd-fdd-actor-product-manager`, `fdd-fdd-actor-release-manager`, `fdd-fdd-actor-ai-assistant`, `fdd-fdd-actor-doc-generator`

#### ADR Management

**ID**: `fdd-fdd-capability-arch-decision-mgmt`  
- Create and track architecture decisions with structured format
- Link ADRs to affected design sections and features
- Decision status tracking (PROPOSED, ACCEPTED, DEPRECATED, SUPERSEDED)
- Impact analysis when ADR changes affect multiple features
- Search ADRs by status, date, or affected components
- Version history for decision evolution

**Actors**: `fdd-fdd-actor-architect`, `fdd-fdd-actor-technical-lead`, `fdd-fdd-actor-security-engineer`

#### Feature Lifecycle Management

**ID**: `fdd-fdd-capability-feature-lifecycle`  
- Track feature status from NOT_STARTED through IN_PROGRESS to DONE
- Automated status updates based on CHANGES.md completion
- Feature dependency management and blocking detection
- Milestone tracking and release planning integration
- Historical feature completion metrics and velocity tracking
- Status transition validation (cannot skip states)

**Actors**: `fdd-fdd-actor-project-manager`, `fdd-fdd-actor-release-manager`, `fdd-fdd-actor-developer`, `fdd-fdd-actor-ai-assistant`

#### Incremental Development Support

**ID**: `fdd-fdd-capability-incremental-development`  
- CREATE and UPDATE modes for all operation workflows
- Preserve existing content when updating artifacts
- Partial updates without full regeneration
- Change history tracking through Git integration
- Iterative refinement of designs and features
- No data loss during updates (unchanged sections preserved)

**Actors**: `fdd-fdd-actor-architect`, `fdd-fdd-actor-developer`, `fdd-fdd-actor-product-manager`, `fdd-fdd-actor-ai-assistant`

#### Code Generation from Design

**ID**: `fdd-fdd-capability-code-generation`  
- Generate code scaffolding from feature DESIGN.md specifications
- Create API endpoints from Section E (API Contracts)
- Generate domain types from Section C.2 (Domain Model)
- Produce test stubs from Section D (Test Cases)
- Use adapter specs for language-specific code generation
- Add traceability tags automatically during generation

**Actors**: `fdd-fdd-actor-developer`, `fdd-fdd-actor-ai-assistant`

#### Cross-Project Patterns Reusability

**ID**: `fdd-fdd-capability-pattern-reusability`  
- Extract common patterns from one project to another
- Reusable adapter specs across similar projects
- Shared workflow customizations and templates
- Pattern library management and versioning
- Template repositories for common architectures
- Organization-wide best practices propagation

**Actors**: `fdd-fdd-actor-technical-lead`, `fdd-fdd-actor-architect`, `fdd-fdd-actor-devops-engineer`

#### Migration and Integration

**ID**: `fdd-fdd-capability-migration`  
- Add FDD to existing projects without disruption
- Auto-detect existing architecture from code and configs
- Reverse-engineer BUSINESS.md from requirements documentation
- Extract DESIGN.md patterns from implementation
- Incremental FDD adoption (start with adapter, add artifacts gradually)
- Legacy system integration with minimal refactoring

**Actors**: `fdd-fdd-actor-technical-lead`, `fdd-fdd-actor-architect`, `fdd-fdd-actor-ai-assistant`

#### Real-Time Validation Feedback

**ID**: `fdd-fdd-capability-realtime-validation`  
- Validate artifacts as they are edited in IDE
- Instant feedback on ID format errors
- Real-time cross-reference checking
- Live placeholder detection
- Incremental validation (only changed sections)
- Background validation without blocking editing

**Actors**: `fdd-fdd-actor-architect`, `fdd-fdd-actor-developer`, `fdd-fdd-actor-fdd-tool`

#### FDL (FDD Description Language)

**ID**: `fdd-fdd-capability-fdl`  
- Plain English algorithm description language for actor flows (recursive acronym: FDD Description Language)
- Structured numbered lists with bold keywords (**IF**, **ELSE**, **WHILE**, **FOR EACH**)
- Instruction markers with checkboxes (- [ ] Inst-label: description)
- Phase-based organization (ph-1, ph-2, etc.) for implementation tracking
- Readable by non-programmers for validation and review
- Translates directly to code with traceability tags
- Keywords: **AND**, **OR**, **NOT**, **MUST**, **REQUIRED**, **OPTIONAL**
- Actor-centric (steps start with **Actor** or **System**)

**Actors**: `fdd-fdd-actor-architect`, `fdd-fdd-actor-developer`, `fdd-fdd-actor-business-analyst`, `fdd-fdd-actor-ux-designer`, `fdd-fdd-actor-product-manager`

#### IDE Integration and Tooling

**ID**: `fdd-fdd-capability-ide-integration`  
- VS Code extension for FDD artifact editing
- Click-to-navigate for FDD IDs (jump to definition)
- where-used and where-defined commands in IDE
- Inline validation errors and warnings
- Autocomplete for FDD IDs and section references
- Syntax highlighting for FDL (FDD Description Language)
- Integration with `fdd` skill commands
- Code lens showing traceability status

**Actors**: `fdd-fdd-actor-developer`, `fdd-fdd-actor-architect`, `fdd-fdd-actor-devops-engineer`

---

## D. Use Cases

#### UC-001: Bootstrap New Project with FDD

**ID**: `fdd-fdd-usecase-bootstrap-project`

**Actor**: `fdd-fdd-actor-technical-lead`, `fdd-fdd-actor-ai-assistant`

**Preconditions**: Project repository exists with Git initialized

**Flow**:
1. Technical Lead initiates FDD setup by requesting AI Assistant to add FDD framework
2. AI Assistant adds FDD as Git submodule or copies FDD directory to project
3. AI Assistant executes `adapter-bootstrap` workflow to create minimal adapter (uses capability `fdd-fdd-capability-workflow-execution`)
4. System creates `.fdd-config.json` with adapter path configuration
5. System creates minimal `{adapter-dir}/AGENTS.md` with Extends declaration (uses capability `fdd-fdd-capability-adapter-config`)
6. AI Assistant runs `fdd adapter-info` skill to verify adapter discovery
7. FDD Validation Tool confirms adapter status: FOUND

**Postconditions**: Project has working FDD adapter, ready for business context and design workflows

---

#### UC-002: Create Business Context Document

**ID**: `fdd-fdd-usecase-create-business-context`

**Actor**: `fdd-fdd-actor-product-manager`, `fdd-fdd-actor-ai-assistant`

**Preconditions**: FDD adapter exists and validated (triggers `fdd-fdd-usecase-bootstrap-project`)

**Flow**:
1. Product Manager asks AI Assistant to create business context document
2. AI Assistant executes `business-context` workflow in CREATE mode (uses capability `fdd-fdd-capability-workflow-execution`)
3. AI Assistant asks questions about vision, target users, and problems solved
4. Product Manager answers questions; AI Assistant proposes content based on README.md if available
5. AI Assistant generates actor list with IDs following format `fdd-{project}-actor-{name}` (uses capability `fdd-fdd-capability-design-first`)
6. AI Assistant generates capability list with actor references (uses capability `fdd-fdd-capability-traceability`)
7. AI Assistant creates `architecture/BUSINESS.md` with all sections
8. FDD Validation Tool runs `business-validate` workflow automatically (uses capability `fdd-fdd-capability-validation`)
9. Validation reports score ≥90/100 with PASS status

**Postconditions**: Valid `architecture/BUSINESS.md` exists, project ready for overall design workflow

---

#### UC-003: Design Feature with AI Assistance

**ID**: `fdd-fdd-usecase-design-feature`

**Actor**: `fdd-fdd-actor-architect`, `fdd-fdd-actor-ai-assistant`

**Preconditions**: BUSINESS.md and DESIGN.md validated, feature registered in FEATURES.md

**Flow**:
1. Architect selects feature from FEATURES.md to design
2. AI Assistant executes `feature` workflow in CREATE mode (uses capability `fdd-fdd-capability-workflow-execution`)
3. Architect specifies actor flows using FDL (plain English with bold keywords: **IF**, **FOR EACH**, **WHILE**) (uses capability `fdd-fdd-capability-design-first`)
4. Architect defines algorithms, states, API contracts per adapter specs (uses capability `fdd-fdd-capability-adapter-config`)
5. Architect specifies requirements and constraints
6. AI Assistant generates `architecture/features/feature-{slug}/DESIGN.md` following structure requirements
7. FDD Validation Tool validates structure using `fdd validate` command (uses capability `fdd-fdd-capability-validation`)
8. AI Assistant performs completeness validation (checks all sections, IDs, cross-references)
9. Validation reports 100/100 score (required for feature DESIGN.md)

**Postconditions**: Feature DESIGN.md validated at 100/100, ready for implementation planning via `fdd-fdd-usecase-plan-implementation`

---

#### UC-004: Validate Design Against Requirements

**ID**: `fdd-fdd-usecase-validate-design`

**Actor**: `fdd-fdd-actor-architect`, `fdd-fdd-actor-fdd-tool`

**Preconditions**: DESIGN.md exists with requirements, actors, and capabilities defined

**Flow**:
1. Architect requests validation of overall DESIGN.md
2. FDD Validation Tool runs `fdd validate --artifact architecture/DESIGN.md` (uses capability `fdd-fdd-capability-validation`)
3. Tool checks structure (sections A-E present, proper heading levels, required content)
4. Tool validates ID formats match `fdd-{project}-{kind}-{name}` pattern (uses capability `fdd-fdd-capability-traceability`)
5. Tool cross-references all actor IDs exist in BUSINESS.md (uses capability `fdd-fdd-capability-traceability`)
6. Tool cross-references all capability IDs exist in BUSINESS.md
7. Tool checks for incomplete work markers in design documents
8. Tool checks for type redefinitions (domain types must be in adapter specs or DESIGN.md Section C.2)
9. Tool reports score breakdown by category (Structure, Completeness, Clarity, Integration)
10. Tool provides specific recommendations for each issue found

**Postconditions**: Validation report shows PASS (≥90/100) or FAIL with actionable issues, Architect fixes issues or proceeds to next workflow

---

#### UC-005: Trace Requirement to Implementation

**ID**: `fdd-fdd-usecase-trace-requirement`

**Actor**: `fdd-fdd-actor-developer`, `fdd-fdd-actor-fdd-tool`

**Preconditions**: Feature DESIGN.md and CHANGES.md exist, code partially implemented with @fdd-* tags

**Flow**:
1. Developer wants to verify requirement `fdd-myapp-req-user-auth` is fully implemented
2. FDD Validation Tool runs `fdd where-defined --root . --id fdd-myapp-req-user-auth` (uses capability `fdd-fdd-capability-traceability`)
3. Tool locates normative definition in `architecture/features/feature-auth/DESIGN.md` Section F
4. FDD Validation Tool runs `fdd where-used --root . --id fdd-myapp-req-user-auth`
5. Tool finds references in CHANGES.md (Change N links to requirement)
6. Tool finds code files with `@fdd-req:fdd-myapp-req-user-auth:ph-1` tags
7. Developer reviews complete traceability chain: DESIGN → CHANGES → Code
8. Developer confirms all implementation phases have corresponding code tags

**Postconditions**: Developer confirms requirement is fully implemented with proper traceability, or identifies missing implementation

---

#### UC-006: Update Existing Feature Design

**ID**: `fdd-fdd-usecase-update-feature-design`

**Actor**: `fdd-fdd-actor-architect`, `fdd-fdd-actor-ai-assistant`

**Preconditions**: Feature DESIGN.md exists and previously validated at 100/100 (triggers `fdd-fdd-usecase-design-feature`)

**Flow**:
1. Architect identifies need to add new algorithm to existing feature
2. AI Assistant executes `feature` workflow in UPDATE mode (uses capability `fdd-fdd-capability-workflow-execution`)
3. Workflow reads existing DESIGN.md and displays current content per section
4. AI Assistant asks: "What to update?" with options (Add actor flow, Edit algorithm, Add requirement, etc.)
5. Architect selects "Add new algorithm" option
6. Architect specifies new algorithm details in FDL (uses capability `fdd-fdd-capability-design-first`)
7. AI Assistant updates Section C (Algorithms) while preserving all other sections unchanged
8. AI Assistant generates new algorithm ID following format `fdd-{project}-feature-{feature}-algo-{name}` (uses capability `fdd-fdd-capability-traceability`)
9. FDD Validation Tool re-validates complete DESIGN.md (uses capability `fdd-fdd-capability-validation`)
10. Validation confirms 100/100 score maintained

**Postconditions**: Feature DESIGN.md updated with new algorithm, fully validated, implementation plan (CHANGES.md) can be updated via `fdd-fdd-usecase-plan-implementation`

---

#### UC-007: Plan Feature Implementation

**ID**: `fdd-fdd-usecase-plan-implementation`

**Actor**: `fdd-fdd-actor-developer`, `fdd-fdd-actor-ai-assistant`

**Preconditions**: Feature DESIGN.md validated at 100/100

**Flow**:
1. Developer requests implementation plan for validated feature
2. AI Assistant executes `feature-changes` workflow in CREATE mode (uses capability `fdd-fdd-capability-workflow-execution`)
3. AI Assistant analyzes feature requirements and proposes atomic changes (1-5 requirements each)
4. Developer reviews proposed changes and adjusts grouping if needed
5. AI Assistant generates task breakdown for each change (uses capability `fdd-fdd-capability-design-first`)
6. AI Assistant creates `architecture/features/feature-{slug}/CHANGES.md` with numbered changes
7. Each change includes: ID, Requirements list (references DESIGN.md IDs), Tasks checklist, Status
8. FDD Validation Tool validates CHANGES.md structure (uses capability `fdd-fdd-capability-validation`)
9. Tool verifies all requirement IDs exist in feature DESIGN.md (uses capability `fdd-fdd-capability-traceability`)

**Postconditions**: Valid CHANGES.md exists with implementation plan, ready for code implementation via `fdd-fdd-usecase-implement-change`

---

#### UC-008: Implement Change and Tag Code

**ID**: `fdd-fdd-usecase-implement-change`

**Actor**: `fdd-fdd-actor-developer`, `fdd-fdd-actor-ai-assistant`

**Preconditions**: CHANGES.md exists with at least one change in NOT_STARTED status (triggers `fdd-fdd-usecase-plan-implementation`)

**Flow**:
1. Developer selects Change N from CHANGES.md to implement
2. AI Assistant executes `feature-change-implement` workflow (uses capability `fdd-fdd-capability-workflow-execution`)
3. AI Assistant updates Change N status from ⏳ NOT_STARTED to 🔄 IN_PROGRESS
4. For each task in Change N, AI Assistant implements code according to DESIGN.md specifications (uses capability `fdd-fdd-capability-design-first`)
5. AI Assistant adds traceability tags to code: `@fdd-change:{change-id}:ph-{N}` for change-level tags (uses capability `fdd-fdd-capability-traceability`)
6. AI Assistant adds instruction-level tags: `@fdd-flow:{flow-id}:ph-{N}:inst-{name}` for FDL steps
7. Developer reviews implementation and marks tasks complete [x]
8. When all tasks complete, AI Assistant updates Change N status to ✅ COMPLETED
9. Developer commits code with descriptive message referencing Change N

**Postconditions**: Change N implemented with full code traceability, ready for code validation via `fdd-fdd-usecase-validate-implementation`

---

#### UC-009: Validate Feature Implementation

**ID**: `fdd-fdd-usecase-validate-implementation`

**Actor**: `fdd-fdd-actor-qa-engineer`, `fdd-fdd-actor-fdd-tool`

**Preconditions**: At least one change in CHANGES.md has status ✅ COMPLETED (triggers `fdd-fdd-usecase-implement-change`)

**Flow**:
1. QA Engineer requests validation of feature implementation
2. FDD Validation Tool runs `fdd validate --artifact {code-root}` for codebase traceability (uses capability `fdd-fdd-capability-validation`)
3. Tool validates DESIGN.md structure first (must pass before code checks)
4. Tool validates CHANGES.md structure (must pass before code checks)
5. For each `[x]` marked scope in DESIGN.md, tool expects `@fdd-{kind}:{id}:ph-{N}` tag in code (uses capability `fdd-fdd-capability-traceability`)
6. For each `[x]` marked FDL instruction, tool expects instruction-level tag in code
7. For each completed change (✅ COMPLETED), tool expects `@fdd-change:{N}:ph-*` tags
8. Tool reports missing tags, extra tags, and format issues
9. Tool checks build passes and tests run successfully

**Postconditions**: Validation report shows full traceability or lists missing/incorrect tags, QA Engineer confirms implementation complete or requests fixes

---

#### UC-010: Auto-Generate Adapter from Codebase

**ID**: `fdd-fdd-usecase-auto-generate-adapter`

**Actor**: `fdd-fdd-actor-technical-lead`, `fdd-fdd-actor-ai-assistant`

**Preconditions**: Project has existing codebase with code, configs, and documentation

**Flow**:
1. Technical Lead wants to add FDD to existing project
2. AI Assistant executes `adapter-auto` workflow (uses capability `fdd-fdd-capability-workflow-execution`)
3. AI Assistant scans project for documentation (README, ARCHITECTURE, CONTRIBUTING) (uses capability `fdd-fdd-capability-adapter-config`)
4. AI Assistant analyzes config files (package.json, requirements.txt, Cargo.toml, etc.)
5. AI Assistant detects tech stack (languages, frameworks, versions)
6. AI Assistant analyzes code structure and naming conventions
7. AI Assistant discovers domain model format from code (TypeScript types, JSON Schema, etc.)
8. AI Assistant discovers API format from definitions (OpenAPI, GraphQL schema, etc.)
9. AI Assistant proposes adapter specifications (tech-stack.md, domain-model.md, conventions.md, etc.)
10. Technical Lead reviews and approves proposed specs
11. AI Assistant creates adapter specs in `{adapter-dir}/specs/`
12. AI Assistant updates AGENTS.md with WHEN rules for each spec

**Postconditions**: Adapter with auto-generated specs from existing codebase, validated and ready for FDD workflows

---

#### UC-011: Configure CI/CD Pipeline for FDD Validation

**ID**: `fdd-fdd-usecase-configure-cicd`

**Actor**: `fdd-fdd-actor-devops-engineer`, `fdd-fdd-actor-ci-pipeline`

**Preconditions**: Project has FDD adapter configured (triggers `fdd-fdd-usecase-bootstrap-project`)

**Flow**:
1. DevOps Engineer wants to automate FDD artifact validation in CI/CD
2. DevOps Engineer reads `{adapter-dir}/specs/build-deploy.md` for test and build commands (uses capability `fdd-fdd-capability-adapter-config`)
3. DevOps Engineer creates GitHub Actions workflow or GitLab CI config
4. Workflow configured to run `fdd validate` on changed artifacts in pull requests
5. CI/CD Pipeline executes validation automatically on every commit (uses capability `fdd-fdd-capability-validation`)
6. Pipeline reports validation results as PR status checks
7. Pipeline blocks merge if any artifact validation fails (uses capability `fdd-fdd-capability-ai-integration`)
8. DevOps Engineer configures notifications for validation failures

**Postconditions**: CI/CD Pipeline automatically validates all FDD artifacts, prevents invalid designs from being merged

---

#### UC-012: Security Review of Feature Design

**ID**: `fdd-fdd-usecase-security-review`

**Actor**: `fdd-fdd-actor-security-engineer`, `fdd-fdd-actor-architect`

**Preconditions**: Feature DESIGN.md exists and validated (triggers `fdd-fdd-usecase-design-feature`)

**Flow**:
1. Security Engineer receives notification that new feature design ready for review
2. Security Engineer reads feature DESIGN.md Section B (Actor Flows) to identify data flows (uses capability `fdd-fdd-capability-design-first`)
3. Security Engineer analyzes Section C.2 (Domain Model) for sensitive data handling
4. Security Engineer reviews Section E (API Contracts) for authentication and authorization requirements
5. Security Engineer checks Section F (Requirements & Constraints) for security requirements
6. Security Engineer identifies missing security controls or vulnerabilities (uses capability `fdd-fdd-capability-validation`)
7. Security Engineer adds security requirements to Section F with IDs `fdd-{project}-feature-{feature}-req-security-*`
8. Architect updates DESIGN.md based on security feedback (triggers `fdd-fdd-usecase-update-feature-design`)
9. Security Engineer approves design after security requirements added

**Postconditions**: Feature design includes comprehensive security requirements, ready for secure implementation

---

#### UC-013: Business Requirements Analysis

**ID**: `fdd-fdd-usecase-business-analysis`

**Actor**: `fdd-fdd-actor-business-analyst`, `fdd-fdd-actor-product-manager`

**Preconditions**: Stakeholder requirements gathered but not yet documented in FDD format

**Flow**:
1. Business Analyst collects raw requirements from stakeholders (interviews, documents, meetings)
2. Business Analyst analyzes requirements and identifies actors (human and system)
3. Business Analyst groups related requirements into capabilities (uses capability `fdd-fdd-capability-design-first`)
4. Business Analyst creates draft structure for BUSINESS.md with actors and capabilities
5. Business Analyst works with Product Manager to refine vision and success criteria
6. Product Manager executes `business-context` workflow with Business Analyst's draft (uses capability `fdd-fdd-capability-workflow-execution`)
7. AI Assistant generates BUSINESS.md based on analyzed requirements
8. Business Analyst reviews generated BUSINESS.md for completeness and accuracy (uses capability `fdd-fdd-capability-validation`)
9. Business Analyst confirms all stakeholder requirements covered by capabilities

**Postconditions**: Well-structured BUSINESS.md capturing all stakeholder requirements in FDD format (triggers `fdd-fdd-usecase-create-business-context`)

---

#### UC-014: Design User Interface from Flows

**ID**: `fdd-fdd-usecase-design-ui`

**Actor**: `fdd-fdd-actor-ux-designer`, `fdd-fdd-actor-architect`

**Preconditions**: Feature DESIGN.md exists with actor flows defined in Section B (triggers `fdd-fdd-usecase-design-feature`)

**Flow**:
1. UX Designer reads feature DESIGN.md Section B (Actor Flows) to understand user journeys (uses capability `fdd-fdd-capability-design-first`)
2. UX Designer identifies UI screens needed for each flow step
3. UX Designer creates wireframes mapping each FDL instruction to UI element
4. For each flow phase (ph-1, ph-2, etc.), UX Designer designs corresponding screen state
5. UX Designer validates that UI covers all actor interactions from flows (uses capability `fdd-fdd-capability-traceability`)
6. UX Designer creates UI mockups with annotations linking to flow IDs (e.g., "Implements `fdd-{project}-feature-{feature}-flow-{name}:ph-1`")
7. Architect reviews UI mockups against DESIGN.md to ensure completeness
8. UX Designer updates UI based on feedback if flows were unclear
9. Architect may update DESIGN.md Section B if UI reveals missing flow steps (triggers `fdd-fdd-usecase-update-feature-design`)

**Postconditions**: UI mockups fully aligned with feature flows, developers can implement UI following both mockups and DESIGN.md

---

#### UC-015: Plan Release with Feature Tracking

**ID**: `fdd-fdd-usecase-plan-release`

**Actor**: `fdd-fdd-actor-release-manager`, `fdd-fdd-actor-project-manager`

**Preconditions**: Multiple features exist in FEATURES.md with various completion statuses

**Flow**:
1. Release Manager opens `architecture/FEATURES.md` to review feature statuses
2. Release Manager identifies features with status ✅ DONE for inclusion in next release (uses capability `fdd-fdd-capability-interactive-docs`)
3. For each DONE feature, Release Manager verifies CHANGES.md shows all changes ✅ COMPLETED
4. Release Manager runs `fdd validate` on each feature to confirm 100/100 validation (uses capability `fdd-fdd-capability-validation`)
5. Release Manager checks feature dependencies and determines release order
6. Release Manager creates release plan document listing included features with their IDs
7. Project Manager reviews feature implementation dates and validates timeline
8. Release Manager coordinates with DevOps Engineer for deployment schedule (references `fdd-fdd-usecase-configure-cicd`)
9. Release Manager updates FEATURES.md with release version tags for included features

**Postconditions**: Release plan created with validated features, clear traceability from requirements to implementation

---

#### UC-016: Record Architecture Decision

**ID**: `fdd-fdd-usecase-record-adr`

**Actor**: `fdd-fdd-actor-architect`, `fdd-fdd-actor-technical-lead`

**Preconditions**: Architecture decision needs to be documented

**Flow**:
1. Architect identifies significant technical decision requiring documentation
2. Architect executes `adr` workflow to create new ADR (uses capability `fdd-fdd-capability-workflow-execution`)
3. AI Assistant assigns sequential ADR ID (e.g., ADR-0001, ADR-0002)
4. Architect documents decision context, considered options, and chosen solution (uses capability `fdd-fdd-capability-arch-decision-mgmt`)
5. Architect links ADR to affected DESIGN.md sections and feature IDs
6. Architect sets status to PROPOSED for review
7. Technical Lead and Security Engineer review ADR decision
8. After approval, Architect updates status to ACCEPTED
9. AI Assistant updates affected design sections to reference ADR (uses capability `fdd-fdd-capability-traceability`)

**Postconditions**: Architecture decision documented with full context, linked to affected design elements, searchable by status and component

---

#### UC-017: Generate Code from Feature Design

**ID**: `fdd-fdd-usecase-generate-code`

**Actor**: `fdd-fdd-actor-developer`, `fdd-fdd-actor-ai-assistant`

**Preconditions**: Feature DESIGN.md validated at 100/100 (triggers `fdd-fdd-usecase-design-feature`)

**Flow**:
1. Developer wants to generate initial code scaffolding from validated design
2. AI Assistant reads feature DESIGN.md Section E (API Contracts) (uses capability `fdd-fdd-capability-code-generation`)
3. AI Assistant reads adapter specs for language-specific patterns (uses capability `fdd-fdd-capability-adapter-config`)
4. AI Assistant generates API endpoint stubs from contract definitions
5. AI Assistant reads Section C.2 (Domain Model) and generates type definitions
6. AI Assistant reads Section D and generates test stub files
7. AI Assistant adds traceability tags to generated code linking to design IDs (uses capability `fdd-fdd-capability-traceability`)
8. Developer reviews generated code and adjusts as needed
9. Developer fills in implementation logic following FDL from Section B (Actor Flows)

**Postconditions**: Code scaffolding generated with proper structure and traceability tags, developer can focus on business logic implementation

---

#### UC-018: Navigate Traceability in IDE

**ID**: `fdd-fdd-usecase-ide-navigation`

**Actor**: `fdd-fdd-actor-developer`

**Preconditions**: VS Code FDD extension installed, project has FDD artifacts

**Flow**:
1. Developer opens feature DESIGN.md in VS Code
2. Developer sees FDD ID `fdd-myapp-feature-auth-flow-login` highlighted with syntax coloring (uses capability `fdd-fdd-capability-ide-integration`)
3. Developer Cmd+Click (or Ctrl+Click) on flow ID to jump to definition in same file
4. Developer right-clicks on flow ID and selects "Find where-used" from context menu
5. IDE shows list of references in CHANGES.md and code files (uses capability `fdd-fdd-capability-traceability`)
6. Developer clicks on code reference to navigate to implementation file
7. Developer sees inline validation errors if ID format is incorrect
8. Developer uses autocomplete to insert valid FDD IDs when editing
9. Code lens above function shows traceability status (✅ tagged or ⚠️ missing tags)

**Postconditions**: Developer can navigate between design and code instantly, maintain traceability without manual searching

---

#### UC-019: Migrate Existing Project to FDD

**ID**: `fdd-fdd-usecase-migrate-project`

**Actor**: `fdd-fdd-actor-technical-lead`, `fdd-fdd-actor-ai-assistant`

**Preconditions**: Existing project with code but no FDD artifacts

**Flow**:
1. Technical Lead wants to adopt FDD for legacy project
2. AI Assistant executes `adapter-auto` workflow to analyze existing codebase (uses capability `fdd-fdd-capability-migration`)
3. AI Assistant scans README.md, ARCHITECTURE.md, and other docs for business context
4. AI Assistant proposes BUSINESS.md content based on discovered information
5. Technical Lead reviews and refines proposed business context
6. AI Assistant analyzes code structure to extract architectural patterns (uses capability `fdd-fdd-capability-pattern-reusability`)
7. AI Assistant proposes DESIGN.md content from implementation patterns
8. Technical Lead identifies which features to document first (incremental adoption)
9. AI Assistant generates feature DESIGN.md for priority features by reverse-engineering code
10. Developer adds traceability tags to existing code incrementally (uses capability `fdd-fdd-capability-traceability`)

**Postconditions**: Legacy project has FDD artifacts documenting current state, team can use FDD workflows for new features while preserving existing code

---

#### UC-020: Track Feature Progress Through Lifecycle

**ID**: `fdd-fdd-usecase-track-feature-lifecycle`

**Actor**: `fdd-fdd-actor-project-manager`, `fdd-fdd-actor-developer`

**Preconditions**: FEATURES.md exists with multiple features at various stages

**Flow**:
1. Project Manager opens FEATURES.md to review current status (uses capability `fdd-fdd-capability-feature-lifecycle`)
2. Project Manager sees feature statuses: ⏳ NOT_STARTED, 🔄 IN_PROGRESS, ✅ DONE
3. Developer marks feature as 🔄 IN_PROGRESS when starting work on CHANGES.md
4. System validates feature has DESIGN.md at 100/100 before allowing IN_PROGRESS status
5. As developer completes changes in CHANGES.md (marks all ✅ COMPLETED), system suggests status update
6. Developer runs final validation before marking feature ✅ DONE (uses capability `fdd-fdd-capability-validation`)
7. Project Manager tracks velocity by counting completed features per sprint
8. Project Manager identifies blocking dependencies (Feature B depends on Feature A)
9. System alerts if Feature B IN_PROGRESS but Feature A still NOT_STARTED
10. Project Manager generates progress report showing feature completion timeline

**Postconditions**: Clear visibility into feature progress, automated status tracking, dependency validation, historical metrics for planning

---

#### UC-021: Edit Artifact with Real-Time Validation

**ID**: `fdd-fdd-usecase-realtime-validation`

**Actor**: `fdd-fdd-actor-architect`

**Preconditions**: VS Code FDD extension installed with real-time validation enabled

**Flow**:
1. Architect opens feature DESIGN.md in VS Code to add new requirement
2. Architect starts typing new requirement ID: `fdd-myapp-feature-auth-req-` (uses capability `fdd-fdd-capability-realtime-validation`)
3. IDE shows autocomplete suggestions for valid ID format
4. Architect types `fdd-myapp-feature-auth-req-2fa` but makes typo: `fdd-myapp-feture-auth-req-2fa`
5. IDE immediately shows red underline with error: "Invalid ID format: 'feture' should be 'feature'"
6. Architect fixes typo, red underline disappears
7. Architect adds requirement description in Section F
8. IDE validates in background that all referenced actor IDs exist in BUSINESS.md (uses capability `fdd-fdd-capability-traceability`)
9. If Architect references non-existent actor ID, IDE shows warning with suggestion
10. Architect saves file - all validation errors already fixed during editing

**Postconditions**: Artifact validated incrementally during editing, no validation surprises at commit time, faster iteration cycle

---

#### UC-022: Write Actor Flow in FDL

**ID**: `fdd-fdd-usecase-write-fdl-flow`

**Actor**: `fdd-fdd-actor-architect`, `fdd-fdd-actor-business-analyst`

**Preconditions**: Feature DESIGN.md exists, architect needs to document actor flow

**Flow**:
1. Architect opens feature DESIGN.md Section B (Actor Flows)
2. Architect creates new flow: "Login Flow" with ID `fdd-myapp-feature-auth-flow-login` (uses capability `fdd-fdd-capability-design-first`)
3. Architect writes flow in FDL using plain English with bold keywords (uses capability `fdd-fdd-capability-fdl`):
   ```
   1. **User** enters username and password in login form
   2. **User** clicks "Login" button
   3. **System** validates input format
   4. **IF** input is invalid:
      - [ ] Inst-show-error: **System** displays validation error message
      - **GOTO** step 1
   5. **System** queries database for user credentials
   6. **IF** credentials are valid **AND** account is active:
      - [ ] Inst-create-session: **System** creates user session with JWT token
      - [ ] Inst-redirect: **System** redirects to dashboard
   7. **ELSE IF** account is locked:
      - [ ] Inst-show-locked: **System** displays "Account locked" message
   8. **ELSE**:
      - [ ] Inst-show-invalid: **System** displays "Invalid credentials" error
      - **GOTO** step 1
   ```
4. Business Analyst reviews FDL flow and confirms it matches business requirements
5. Business Analyst identifies missing case: "What if user forgot password?"
6. Architect adds step with **OPTIONAL** path to password reset (uses capability `fdd-fdd-capability-incremental-development`)
7. UX Designer reads flow and creates UI mockups matching each step and instruction
8. Architect marks instructions with phases for implementation: ph-1 (validation), ph-2 (authentication), ph-3 (session)
9. Developer reads FDL flow and understands exact implementation requirements without ambiguity

**Postconditions**: Actor flow documented in plain English readable by all stakeholders, directly translatable to code with instruction-level traceability
