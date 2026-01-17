<!-- @fdd-change:fdd-fdd-feature-core-methodology-change-quickstart-docs:ph-1 -->
<!-- fdd-begin fdd-fdd-feature-core-methodology-flow-user-onboard:ph-1:inst-open-readme -->
# Feature-Driven Design (FDD)
FDD project overview.
<!-- fdd-end   fdd-fdd-feature-core-methodology-flow-user-onboard:ph-1:inst-open-readme -->

**Version**: 1.0  
**Status**: Active  
**Audience**: Development teams, technical leads, architects

Feature-Driven Design is a **universal methodology** for building software systems with clear traceability from requirements to implementation.

**Built for modern development**: FDD works with AI coding assistants, supports any tech stack, and provides structured workflows that teams can follow manually or automate.

---

<!-- fdd-begin fdd-fdd-feature-core-methodology-flow-user-onboard:ph-1:inst-discover-fdd -->
## 🚀 Quick Start

**New to FDD?** Start here: **[QUICKSTART.md](QUICKSTART.md)**
<!-- fdd-end   fdd-fdd-feature-core-methodology-flow-user-onboard:ph-1:inst-discover-fdd -->

Learn FDD in 10 minutes with:
- **Exact prompts to copy-paste** into your AI chat
- **Complete example**: Task management API from start to finish
- **Common scenarios**: What to do when requirements change
- **Working with existing docs**: Use what you already have

---

## What is FDD?

FDD helps teams build software by:

1. **Designing before coding**: Document what you're building in clear, reviewable formats
2. **Breaking work into features**: Each feature is independent and testable
3. **Using plain English**: Algorithms described in FDL (not code), reviewable by non-programmers
4. **Tracking changes atomically**: Implementation changes ensure every change is traceable
5. **Validating designs**: Catch issues before implementation

---

## FDD Flow Overview

![FDD Layered Flow](fdd-flow-layers.drawio.svg)

**The 7-layer flow** (each layer builds on validated previous layer):

**Layer 0: Project Adapter** (Architect, Project Manager)
- Define tech stack & conventions (any language, any tools)
- Workflows: `adapter`, `adapter-agents`, `adapter-from-source`

**Layer 1: Business Context** (Product Owner, Project Manager)
- Define business requirements, use cases, capabilities
- Workflows: `business-context`, `business-validate`
- ✅ Validated before proceeding

**Layer 2: Overall Design** (Architect, Project Manager)
- Actors, domain model, API contracts, industry best practices
- Workflows: `design`, `design-validate`, `adr`, `adr-validate`
- ✅ Validated (≥90/100) before proceeding

**Layer 3: Feature Planning** (Architect, Project Manager)
- FEATURES.md manifest, feature list, dependencies, design decomposition
- Workflows: `features`, `features-validate`
- ✅ Validated before proceeding

**Layer 4: Feature Design** (Solution Architect, Project Manager)
- Actor flows in FDL, algorithms, states, requirements
- Validated against overall design
- Workflows: `feature`, `feature-validate`
- ✅ Validated (100/100) before proceeding

**Layer 5: Feature Changes** (Developer/QA, Project Manager)
- Atomic implementation changes with tasks
- Specs validated against feature design
- Workflows: `feature-changes`, `feature-code-validate`
- Validated before proceeding

**Layer 6: Implementation** (Developer/QA, Project Manager)
- Code validated against spec automatically
- Workflows: `feature-change-implement`, `feature-code-validate`

**Key principles**: 
- Each layer validated before proceeding to next
- Design is source of truth, enforced by tooling
- Business Context → Design → Features → Implementation
- All workflows support CREATE & UPDATE modes for iteration

---

## The AGENTS.md Foundation

FDD is built on the **AGENTS.md approach** - a standardized file that serves as the single source of truth for AI agents. Instead of scattered documentation across README files, wikis, and comments, `AGENTS.md` provides complete methodology rules, workflow references, and project-specific context in one place.

**Two-level hierarchy**:
1. Core `AGENTS.md` - FDD methodology (universal, in FDD root)
2. `{adapter-directory}/AGENTS.md` - Project-specific adapter (your tech stack, conventions, workflows)

**Key benefits**:
- AI agents load complete context instantly (no searching)
- Workflows become executable (agents follow step-by-step)
- Version controlled (track methodology changes via git)
- Composable (core + project extensions, no duplication)
- Human + AI harmony (README for humans, AGENTS.md for AI)

When an AI agent encounters FDD, it reads `FDD-Adapter/AGENTS.md` → which references `FDD/AGENTS.md` → complete understanding of methodology + project conventions + workflows.

---

## Key Strengths

### 1. Interactive Workflows - Your AI Pair Programmer

FDD provides **10 operation workflows** that guide you step-by-step through the entire development process. Each workflow **works in two modes**: CREATE (generate new) and UPDATE (edit existing), making them fully independent and iterative.

**Key Innovation: Create AND Edit Support**

All operation workflows automatically detect whether you're creating something new or updating existing artifacts:
- **CREATE mode**: Generates from scratch with guided questions
- **UPDATE mode**: Reads current content, proposes changes, preserves unchanged parts

**Example: Creating or Updating a Project Adapter**

First time:
```
Follow @/FDD/workflows/adapter.md
→ No adapter found → CREATE mode
```

Later, to update:
```
Follow @/FDD/workflows/adapter.md
→ Adapter exists → UPDATE mode
→ What to update?
   - Domain model specs
   - API contract specs
   - Testing configuration
   - Build commands
```

Both modes ask targeted questions:
```
Q1: Project name?
   CREATE: Propose from package.json
   UPDATE: Show current "fdd-cli", ask to change or keep

Q2: Domain model technology?
   CREATE: Detect and propose (GTS, JSON Schema, TypeScript...)
   UPDATE: Show current "GTS", ask to change or keep

Q3: API contract format?
   CREATE: Propose (OpenAPI, CLISPEC, GraphQL...)
   UPDATE: Show current "CLISPEC", ask to change or keep
```

**Result**: 
- **CREATE**: Fully configured adapter in 5-10 minutes
- **UPDATE**: Targeted changes without recreating everything

**Example: Iterating on Feature Design**

```
Follow @/FDD/workflows/feature.md
→ Feature exists → UPDATE mode
→ What to update?
   - Add new actor flow
   - Edit existing algorithm
   - Update technical details
   - Add new requirements
```

Workflow shows current content and asks for specific changes - no need to start from scratch.

**Why This Is Revolutionary**:
- **Truly iterative** - Update artifacts as project evolves
- **No data loss** - UPDATE mode preserves unchanged content
- **Independent workflows** - Run any workflow anytime
- **No memorization** - Workflows guide you every time
- **No mistakes** - Each step validated before proceeding
- **Consistent results** - Same structure every time
- **AI-friendly** - AI agents follow workflows naturally
- **Human-readable** - Anyone can execute manually if needed

### 2. Adapter System - Works With Any Tech Stack

FDD core is **100% technology-agnostic**. Your project adapter makes it specific to YOUR stack.

**Adapters define**:
- **Domain model format**: GTS, JSON Schema, TypeScript, Protobuf, CTI, etc.
- **API contracts**: OpenAPI, GraphQL, gRPC, RAML, CLISPEC, etc.
- **Testing strategy**: Jest, Pytest, Go test, etc.
- **Build tools**: Webpack, Vite, Cargo, Maven, etc.
- **Project conventions**: Naming, structure, security model

**Example Adapters**:

**Microservice with REST API**:
```yaml
Domain Model: OpenAPI + JSON Schema
API Contracts: OpenAPI 3.1
Testing: Jest + Supertest
Deployment: Docker + Kubernetes
```

**CLI Tool**:
```yaml
Domain Model: GTS (Global Type System)
API Contracts: CLISPEC (command specifications)
Testing: Vitest
Deployment: npm publish
```

**GraphQL Backend**:
```yaml
Domain Model: GraphQL Schema
API Contracts: GraphQL SDL
Testing: Apollo Server Testing
Deployment: Serverless
```

**Why This Matters**:
- **Use your existing stack** - No forced technology choices
- **Migrate gradually** - Add FDD to existing projects
- **Team flexibility** - Different teams, different stacks, same methodology
- **Future-proof** - New tech? Just create new adapter

### 3. Skills System - Claude-Compatible AI Tools

FDD provides **Claude-compatible skills** for automated artifact search and validation:

**Available Skills**:

**fdd** (Unified Tool):
- **Validation**: Validate BUSINESS.md, DESIGN.md, ADR.md, FEATURES.md, feature DESIGN.md, feature CHANGES.md
- **Search**: List sections, IDs, and items in any artifact
- **Traceability**: Find where FDD/ADR IDs are defined or used (repo-wide traceability)
- **Code Integration**: Codebase traceability scan (@fdd-* tags)
- Support for qualified IDs (`:ph-*`, `:inst-*`)
- Deterministic validation (no subjective scoring)

**How Skills Work**:
1. Agent discovers skills via `skills/SKILLS.md`
2. Selects `fdd` skill for FDD-related tasks
3. Enters "Skill Lock" - uses only that skill's commands
4. Executes via Python scripts (requires `python3`)

**Example Usage**:
```bash
# Search for an ID across the repository
python3 skills/fdd/scripts/fdd.py where-used --id "fdd-example-req-001"

# Validate feature design
python3 skills/fdd/scripts/fdd.py validate \
  --artifact architecture/features/feature-login/DESIGN.md

# List all IDs in a document
python3 skills/fdd/scripts/fdd.py list-ids --artifact architecture/DESIGN.md
```

Skills integrate with FDD workflows - validation workflows use `fdd` as the Deterministic Gate.

### 4. Workflow-Driven Development - Everything Has a Process

In FDD, **every action is a workflow**. Development becomes predictable and repeatable.

**Workflow Categories**:

**Operation Workflows** (13 workflows - all support CREATE & UPDATE modes):
```
Adapter Configuration:
├─ adapter.md               → Create OR update project adapter
├─ adapter-auto.md          → Auto-detect adapter from codebase
├─ adapter-manual.md        → Manual adapter setup
├─ adapter-bootstrap.md     → Bootstrap minimal adapter
└─ adapter-agents.md        → Create OR update AI agent integration

Architecture & Requirements:
├─ business-context.md      → Create OR update business context (BUSINESS.md)
├─ adr.md                   → Create/add/edit Architecture Decision Records
└─ design.md                → Create OR update overall design (DESIGN.md)

Feature Management:
├─ features.md              → Create OR update features manifest (FEATURES.md)
├─ feature.md               → Create OR update feature design
├─ feature-changes.md       → Create OR update feature implementation plan
└─ feature-change-implement.md → Implement changes (works with existing CHANGES.md)
```

**Validation Workflows** (7 automated, read-only):
```
├─ adapter-validate.md      → Validate adapter completeness
├─ business-validate.md     → Validate BUSINESS.md structure
├─ adr-validate.md          → Validate ADR.md structure  
├─ design-validate.md       → Validate DESIGN.md (≥90/100)
├─ features-validate.md     → Validate FEATURES.md manifest
├─ feature-validate.md      → Validate feature DESIGN.md (100/100)
├─ feature-changes-validate.md → Validate CHANGES.md structure
└─ feature-code-validate.md → Validate entire feature code against design
```

**Total**: 20 workflows (13 operation + 7 validation) + 2 skills

**Key Principle**: All operation workflows are **independent and iterative** - run them anytime to create new or update existing artifacts.

**Real Development Flow**:
```
Day 1: Create adapter
       Run: adapter.md workflow
       → CREATE mode detected (no adapter exists)
       → 10 minutes, adapter ready

Day 2: Create business context & design
       Run: business-context.md workflow
       → CREATE mode, 30 min, BUSINESS.md complete
       
       Run: design.md workflow  
       → CREATE mode, 2-3 hours, DESIGN.md complete
       → Auto-creates ADR-0001 (Initial Architecture)
       
       Run: design-validate.md
       → 5 minutes, score 95/100 
       → Auto-validates ADR.md

Day 3: Plan features
       Run: features.md workflow
       → CREATE mode, 5 minutes, FEATURES.md generated
       
       Run: features-validate.md
       → 5 minutes, manifest validated 

Week 1-2: Develop features (iterative)
          Run: feature.md workflow
          → CREATE: New feature design, 1-2 hours
          → UPDATE: Edit flows/algorithms, 15-30 min
          
          Run: feature-validate.md
          → 100/100 score required 
          
          Run: feature-changes.md workflow
          → CREATE: Implementation plan
          → UPDATE: Add/edit changes as needed
          
          Run: feature-change-implement.md
          → Code implementation
          
          Run: feature-code-validate.md
          → Validate complete feature code

Ongoing: Update artifacts as project evolves
         → Update adapter: adapter.md (UPDATE mode)
         → Update design: design.md (UPDATE mode)
         → Add ADRs: adr.md (ADD mode)
         → Update features: feature.md (UPDATE mode)
```

**Why Workflows Matter**:
- **Nothing forgotten** - Checklists ensure completeness
- **Clear handoffs** - Team knows exactly what to do next
- **Progress tracking** - Always know where you are
- **Onboarding speed** - New members follow workflows
- **Quality gates** - Validation before proceeding

### 4. FDD vs OpenSpec - Design-First vs Change-First

**Honest comparison**: Both are valuable methodologies, but they solve different problems.

| Aspect | OpenSpec | FDD |
|--------|----------|-----|
| **Primary Focus** | Change management | Design-first development |
| **What it defines** | How to track changes<br>How to track changes<br>Change history | What to build (architecture)<br>How it works (actor flows)<br>Why decisions were made |
| **Starting point** | Assumes you know what to build<br>Start with change proposal | Start with business context<br>Define overall design first |
| **Design artifacts** | No overall design structure<br>No business context document<br>No feature planning | BUSINESS.md (business context)<br>DESIGN.md (architecture)<br>ADR.md (decision records)<br>FEATURES.md (feature manifest) |
| **Actor flows** | Not part of methodology<br>Write in change proposals | Section B of every feature<br>Reviewable by non-programmers<br>Uses FDL (plain English) |
| **Domain model** | No standardized location<br>Define per change | Defined once in Overall Design<br>Referenced by all features<br>Technology-agnostic (GTS, JSON Schema, etc.) |
| **API contracts** | No standardized location<br>Define per change | Defined once in Overall Design<br>Referenced by all features<br>Format-agnostic (OpenAPI, GraphQL, etc.) |
| **Cross-feature validation** | No mechanism<br>Manual coordination needed | Built-in validation<br>Detects type redefinitions<br>Validates dependencies |
| **Stakeholder review** | Technical proposals<br>Requires technical knowledge | Plain English actor flows<br>Business-reviewable designs<br>FDL algorithms |
| **Change tracking** | Excellent atomic tracking<br>Clear change history<br>Delta specifications | CHANGES.md per feature<br>Task checklists<br>Status tracking |
| **Implementation** | One change at a time<br>Clear tasks per change | CHANGES.md guides implementation<br>Validated against feature design |
| **AI integration** | AI can implement changes<br>But must know what to build | AI follows complete methodology<br>AGENTS.md provides full context<br>Workflows guide every step |
| **Learning curve** | Simple to start<br>Just create changes | Requires understanding methodology<br>But workflows guide you |
| **Best for** | Tracking implementation changes<br>Delta documentation<br>Audit trails | Design-first projects<br>Team collaboration<br>Stakeholder involvement<br>Complex systems |

**When to use what**:

**Use OpenSpec alone** if you:
- Have clear requirements already documented elsewhere
- Small team, everyone knows what to build
- Need only change tracking and audit trail
- Don't need cross-feature coordination

**Use FDD** if you:
- Need to design before implementation
- Want stakeholders to review logic
- Have multiple features with dependencies
- Need overall architecture documentation
- Want AI to follow complete methodology
- Need validation before coding

**Use FDD + OpenSpec** if you:
- Want best of both worlds (FDD has built-in CHANGES.md tracking)
- FDD's CHANGES.md may be sufficient for many projects
- OpenSpec adds more powerful delta tracking if needed

**Key insight**: FDD includes change tracking via CHANGES.md. You get design artifacts + change tracking in one methodology. OpenSpec is optional if you need more sophisticated change management.

### 5. FDL (FDD Description Language) - Plain English Logic

FDD uses **FDL** to describe behavior in plain English - no code syntax, just numbered markdown lists with bold keywords.

**Why**: Anyone can review (stakeholders, QA, developers). Design stays valid across languages. Perfect for AI code generation.

**Format**: Each step includes checkbox `[ ]`/`[x]`, phase `ph-N`, description, and instruction ID `inst-id`.

**Example - User Authentication**:

```markdown
1. [x] - `ph-1` - User submits login form - `inst-submit-form`
2. [x] - `ph-1` - System validates credentials - `inst-validate-creds`
   1. [x] - `ph-1` - **IF** invalid: - `inst-if-invalid`
      1. [x] - `ph-1` - Show error - `inst-show-error`
      2. [x] - `ph-1` - **RETURN** error - `inst-return-error`
3. [ ] - `ph-2` - **TRY**: - `inst-try`
   1. [ ] - `ph-2` - Create session token - `inst-create-token`
   2. [ ] - `ph-2` - Store in database - `inst-store-db`
4. [ ] - `ph-2` - **CATCH** DatabaseError: - `inst-catch`
   1. [ ] - `ph-2` - Log error - `inst-log-error`
   2. [ ] - `ph-2` - **RETURN** 500 error - `inst-return-500`
5. [ ] - `ph-1` - Redirect to dashboard - `inst-redirect`
```

**Keywords**: **IF**/ELSE, **FOR EACH**, **WHILE**, **TRY**/CATCH, **PARALLEL**, **RETURN**, **MATCH**

**Used in**: Actor Flows (Section B), Algorithms (Section C), State Machines (Section D)

**Full syntax**: See `requirements/FDL.md`

**Why No Code in Designs**:

FDD **strictly prohibits code** in DESIGN.md files:
- No `if (x > 5) { ... }` syntax
- No function definitions
- No framework-specific patterns
- Only FDL plain English

**This is enforced by validation** - designs with code fail validation.

**The Business Impact**:

Before FDL:
```
Developer writes algorithm in code
    ↓
Stakeholder can't review (too technical)
    ↓
Logic bug discovered in production
    ↓
Expensive fix + customer impact
```

With FDL:
```
Designer writes algorithm in FDL
    ↓
Stakeholder reviews and approves
    ↓
Developer implements validated logic
    ↓
Bug caught before coding
```

**See Full FDL Specification**: `requirements/FDL.md`

### 6. Structured Project Organization - Rules and Validation

FDD enforces **consistent structure and validation** across your entire project.

**Project Structure Rules**:

```
architecture/
├── BUSINESS.md                  # Business context (required)
│   ├── Section A: Vision & Purpose
│   ├── Section B: Actors
│   ├── Section C: Capabilities
│   └── Section D: Additional Context
│
├── DESIGN.md                    # Overall Design (required)
│   ├── Section A: Architecture Overview
│   ├── Section B: Requirements & Principles
│   ├── Section C: Technical Architecture
│   └── Section D: Additional Context (optional)
│
├── ADR.md                       # Architecture Decision Records (MADR format)
│
├── diagrams/                    # Architecture diagrams
│
└── features/                    # All features
    ├── FEATURES.md             # Feature manifest (generated)
    │
    └── feature-{slug}/         # Individual feature
        ├── DESIGN.md           # Feature design (required)
        │   ├── Section A: Overview
        │   ├── Section B: Actor Flows (PRIMARY)
        │   ├── Section C: Algorithms
        │   ├── Section D: States (optional)
        │   ├── Section E: Technical Details
        │   ├── Section F: Requirements
        │   └── Section G: Implementation Plan
        │
        └── CHANGES.md          # Implementation changes
```

**Validation Rules Enforced**:

**Business Context Validation** (workflow business-validate):
- All sections present (A, B, C, D)
- Vision and purpose clearly defined
- All actors identified
- Core capabilities documented

**Overall Design Validation** (workflow design-validate):
- All sections present (A, B, C)
- Architecture style documented
- Domain model documented (in chosen DML format)
- API contracts documented (in chosen format)
- No contradictions in architecture
- Score ≥90/100 before proceeding

**Features Manifest Validation** (workflow features-validate):
- All features listed with unique IDs
- Valid priorities (CRITICAL, HIGH, MEDIUM, LOW)
- Valid status emojis (⏳ NOT_STARTED, 🔄 IN_PROGRESS, ✅ COMPLETE)
- All feature directories exist
- No orphaned feature directories
- Dependencies are valid (no circular, no missing)

**Feature Design Validation** (workflow feature-validate):
- All sections present (A-G)
- Section B (Actor Flows) is PRIMARY and complete
- Algorithms in FDL only (no code)
- No type redefinitions (must reference Overall Design)
- All dependencies declared
- Implementation changes planned
- Score 100/100 + 100% completeness

**Documentation Rules**:
- FDL only in designs - No code in DESIGN.md files
- Single source of truth - Types defined once in Overall Design
- Cross-references validated - All references must exist
- Status tracking - Feature status always accurate
- Dependency checking - No circular dependencies allowed

**Why Structure and Validation Matter**:
- Consistency - Every feature follows same pattern
- Quality gates - Can't proceed with incomplete designs
- Team coordination - Everyone knows where to find things
- Maintenance ease - Structure is predictable
- AI-friendly - Clear structure helps AI navigate and generate

**Example Validation Failure**:
```
Feature Design Validation Failed

Issues Found:
1. Section B (Actor Flows) incomplete - missing "User Logout" flow
2. Section E redefines type "User" - must reference Overall Design
3. Section G missing implementation change for "session management"

Score: 78/100 (minimum: 100/100)
Completeness: 85% (minimum: 100%)

→ Fix issues and re-run validation (workflow feature-validate)
```

---

## Why Use FDD?

### What You Get With FDD

**For Single Expert / Architect**:
- AI does 80% of the work: Design → validation → implementation automated
- Living documentation: Designs stay up-to-date with code (enforced by validation)
- Full traceability: From business requirement → design → code change
- Faster delivery: AI handles boilerplate, you focus on business logic
- Catch issues early: Validation happens before coding

**For Teams**:
- Stakeholders can review: Actor flows in plain English, no code knowledge needed
- Clear handoffs: Feature designs are complete specs, not ambiguous tickets
- Progress tracking: FEATURES.md shows exactly what's done/in-progress/pending
- Consistency: Workflows enforce same standards across all features
- Onboarding: New team members read designs, not reverse-engineer code

**For Business**:
- Lower costs: Less rework, fewer bugs, faster development
- Predictability: Features have complete designs before implementation
- Risk reduction: Validation catches architectural issues early
- Audit trail: Every change is documented and traceable

### What Happens Without FDD

**The typical scenario**:
1. Developer starts coding from vague requirements
2. Discovers edge cases during implementation
3. Goes back to architect/PM for clarification
4. Delays accumulate, scope creeps
5. Bugs discovered after deployment (logic wasn't reviewed)
6. Technical debt grows (no overall design document)
7. Refactoring becomes risky (no source of truth)

**Specific problems FDD prevents**:

| Without FDD | With FDD |
|-------------|----------|
| Requirements in scattered Jira tickets | Complete Overall Design in one place |
| Stakeholders can't review logic | Actor flows reviewable by non-programmers |
| Type definitions duplicated across features | Domain model in Overall Design, referenced everywhere |
| API changes break other features | API contracts defined upfront, validated |
| "Documentation" outdated or missing | Designs validated against code, stay current |
| Developer interprets requirements differently | Feature Design is unambiguous spec |
| AI assistant generates inconsistent code | AI follows workflows, enforces patterns |
| Can't track feature dependencies | FEATURES.md shows dependency graph |
| Rework after stakeholder review | Stakeholders review design before coding |

---

## Core Components

### 1. Complete Design Hierarchy

**Adapter** (`{adapter-directory}/AGENTS.md`):
- Tech stack definition (any language, any framework)
- Domain model format (GTS, JSON Schema, TypeScript, etc.)
- API contract format (OpenAPI, GraphQL, CLISPEC, etc.)
- Testing frameworks and build tools
- Project-specific conventions

**Business Context** (`architecture/BUSINESS.md`):
- System vision and purpose
- Key actors (users, systems, services)
- Core capabilities (what system can do)
- Business constraints and compliance requirements

**Overall Design** (`architecture/DESIGN.md`):
- Architecture style and layers
- Requirements and principles
- Domain model types (formally specified)
- API contracts (formally specified)
- Security model and NFRs
- Architecture Decision Records (ADR.md)

**Features Manifest** (`architecture/features/FEATURES.md`):
- Complete list of all features
- Feature priorities (CRITICAL, HIGH, MEDIUM, LOW)
- Feature status (⏳ NOT_STARTED, 🔄 IN_PROGRESS, ✅ COMPLETE)
- Dependencies between features
- Auto-generated from feature designs

**Feature Design** (`architecture/features/feature-{slug}/DESIGN.md`):
- Feature overview and scope
- Actor flows (how users interact - PRIMARY)
- Algorithms in FDL (plain English logic)
- States (optional state machines)
- Technical details (database, operations, errors)
- Requirements (formalized scope + testing)
- Implementation plan (CHANGES.md)

### 2. Implementation Changes (Change Management)

Break features into atomic, traceable changes in CHANGES.md:

```
feature-login/
└── CHANGES.md          # Implementation changes with tasks
    ├── Change 001: Authentication
    │   ├── Purpose
    │   ├── Tasks checklist
    │   └── Status
    └── Change 002: Authorization
        ├── Purpose
        ├── Tasks checklist
        └── Status
```

### 3. Formal Specifications

**DML (Domain Model Language)** - you choose format:
- [GTS](https://github.com/GlobalTypeSystem/gts-spec), [CTI](https://github.com/acronis/go-cti/blob/main/cti-spec/SPEC.md), JSON Schema, RAML, Protobuf etc.
- Must be documented before implementation
- Should be machine-readable and versionable (recommended)

**API Contracts** - you choose format:
- OpenAPI, GraphQL Schema, gRPC, RAML, etc.
- **CLISPEC** (built-in format for CLI tools)
- Must be documented before implementation

---

## Getting Started

### 1. Quick Overview (5 minutes)

**Read these files**:
1. `README.md` (this file) - Overview, getting started, team workflow
2. `QUICKSTART.md` - 5-minute quick start guide with examples
3. `FDL.md` - Learn plain English algorithm syntax
4. `workflows/README.md` - Understand workflow system

### 2. Add FDD to Your Project (15 minutes)

**Option A: Copy FDD core**
```bash
# In your project root
cp -r /path/to/FDD /FDD
```

**Option B: Git submodule** (recommended for shared projects)
```bash
git submodule add <fdd-repo-url> /FDD
```

### 3. Create Project Adapter (5-10 minutes) 

**Follow workflow**: `workflows/adapter.md`

With AI agent:
```
Follow @/FDD/workflows/adapter.md to create FDD adapter
```

This interactive workflow will:
1. Detect mode (CREATE/UPDATE)
2. Ask guided questions about your project
3. Choose domain model format (GTS, JSON Schema, TypeScript, etc.)
4. Choose API contract format (OpenAPI, GraphQL, CLISPEC, etc.)
5. Capture security model and non-functional requirements
6. Generate or update `{adapter-directory}/AGENTS.md` and spec files

**Result**: Adapter created/updated at `{adapter-directory}/` with status COMPLETE or INCOMPLETE

For manual setup, see: **`ADAPTER_GUIDE.md`**

### 4. Configure AI Agent (2 minutes, optional) 

**Follow workflow**: `workflows/adapter-agents.md`

This optional workflow sets up your AI agent (Windsurf, Cursor, Cline, Aider) to use FDD natively:
- Detects existing config (UPDATE mode) or creates new (CREATE mode)
- Creates agent-specific configuration files
- Windsurf: `.windsurf/rules/` + workflow wrappers
- Cursor: `.cursorrules` (single file)
- Cline: `.clinerules` (single file)
- Aider: `.aider.conf.yml` (YAML config)

All configs:
- Tell agent to read FDD adapter first
- Provide FDD workflow references
- Follow agent-specific format

**Result**: Agent reads `{adapter-directory}/AGENTS.md` automatically

### 5. Create Business Context & Design (2-4 hours) 

**AI agent workflows**: 
```
Follow @/FDD/workflows/business-context.md
Follow @/FDD/workflows/design.md
```

These workflows guide you through creating BUSINESS.md and DESIGN.md with interactive questions.

### 6. Start First Feature (1-2 hours) 

**AI agent workflows**:
```
Follow @/FDD/workflows/features.md  # Generate FEATURES.md
Follow @/FDD/workflows/feature.md   # Create feature design
```

These workflows extract features from design and guide you through creating feature designs.

---

## IDE Setup

To set up your AI assistant (Windsurf, Cursor, Cline, etc.) to work natively with FDD:

**Use workflow**: `workflows/adapter-agents.md`

This workflow creates agent-specific files (`.windsurf/rules/`, workflow wrappers) so your agent reads the FDD adapter and uses FDD workflows naturally.

---

## Working with AI Assistants

FDD is designed to work with AI coding assistants (but doesn't require them).

### Recommended AI Setup (By Operation Type)

FDD tasks vary greatly. Each operation class below lists realistic model options as of 2024-2026.

#### Model Classes
- **Reasoning** – frontier-level logic, best for complex reasoning & strict validation.
- **Flagship** – balanced capability & speed, strong generalists.
- **Fast/Lite** – latency-optimized, high throughput, smaller context.

#### 1. Documentation & Design (Writing)
**Tasks**: Create/expand `BUSINESS.md`, `DESIGN.md`, `FEATURES.md`, `ADR.md`
**Requirements**: Long-context understanding, structured output, template following

**Recommended**
- **Cloud**: `Claude 3.5 Sonnet`, `GPT-4o`, `Gemini 1.5 Pro`
- **Local**: `DeepSeek-V3`, `Qwen2.5 72B`, `Llama 3.1 70B`

#### 2. Validation & QA (Checking)
**Tasks**: Score artifacts, detect contradictions, enforce checklists
**Requirements**: **Reasoning ONLY**, attention to detail, structured evaluation

**Recommended**
- **Cloud**: `Claude 3.5 Sonnet`, `GPT-4o`, `o1-preview` (for complex validation)
- **Local**: `DeepSeek-R1`, `Qwen2.5-Coder 32B` – validation requires strong models

#### 3. Implementation (Coding)
**Tasks**: Write/refactor code & tests from `CHANGES.md`
**Requirements**: Code generation, spec-following, moderate reasoning

**Recommended**
- **Cloud**: `Claude 3.5 Sonnet`, `GPT-4o`, `Gemini 1.5 Flash`
- **Local**: `DeepSeek-Coder V2`, `Qwen2.5-Coder 32B`, `CodeLlama 70B`

#### 4. Adapter & Analysis (Scanning)
**Tasks**: Project scanning, adapter setup, large file trees
**Requirements**: Large context window (100k+ tokens)

**Recommended**
- **Cloud**: `Claude 3.5 Sonnet (200k)`, `Gemini 1.5 Pro (2M)`, `GPT-4o (128k)`
- **Local**: `Qwen2.5 72B (128k)`, `Llama 3.1 70B (128k)`


### AI Limitations

AI assistants can:
- Initialize structures
- Generate design templates
- Validate against checklists
- Implement changes from CHANGES.md
- Write tests

Humans must:
- Define business requirements
- Make architectural decisions
- Review actor flows
- Approve designs
- Final code review

---

## Team Workflow

FDD is designed for a **single expert** (typically an architect or senior developer) working with AI assistants. The expert follows FDD workflows to create business context, design architecture, plan features, and implement changes. AI agents handle routine tasks like validation, file generation, and code implementation according to adapter conventions.

**With AI Assistants** (recommended for 2024-2026):
- Use **Claude 3.5 Sonnet** or **GPT-4o** for most workflows
- Use **o1-preview** or **Claude 3.5 Sonnet** for validation workflows
- Skills system (`fdd`) works with any AI assistant
- Requires `python3` for skill execution

For teams, work can be distributed: one person owns overall design and architecture decisions (BUSINESS.md, DESIGN.md, ADR.md), while others can own individual feature designs (FEATURES.md, feature/DESIGN.md) and implementation (CHANGES.md). All artifacts use plain English (FDL) for actor flows and algorithms, making them reviewable by non-technical stakeholders. Validation workflows ensure consistency and completeness before implementation.

---

## Directory Structure

```
{adapter-directory}/FDD/                        # Core FDD (standalone, universal)
├── README.md                                   # This file - overview, getting started
├── QUICKSTART.md                               # 5-minute quick start guide
├── AGENTS.md                                   # AI agent instructions
├── WORKFLOW.md                                 # Workflow system overview
├── FDL.md                                      # FDD Description Language syntax (removed)
├── CLISPEC.md                                  # CLI command specification format
├── ADAPTER_GUIDE.md                            # How to create project adapter
├── requirements/                               # All FDD requirements and structure specs
│   ├── FDL.md                                  # FDD Description Language syntax
│   ├── execution-protocol.md                   # Workflow execution protocol
│   ├── workflow-execution.md                   # General workflow execution
│   ├── business-context-structure.md           # BUSINESS.md structure
│   ├── overall-design-structure.md             # DESIGN.md structure
│   ├── adr-structure.md                        # ADR.md structure
│   ├── features-manifest-structure.md          # FEATURES.md structure
│   ├── feature-design-structure.md             # Feature DESIGN.md structure
│   ├── feature-changes-structure.md            # Feature CHANGES.md structure
│   └── adapter-structure.md                    # Adapter structure requirements
├── skills/                                     # Claude-compatible AI skills
│   ├── SKILLS.md                               # Skills discovery protocol
│   └── fdd/                                    # Unified FDD tool
│       ├── SKILL.md                            # Skill definition
│       ├── scripts/fdd.py                      # Unified Python script
│       └── tests/                              # Unit tests
└── workflows/                                  # 20 workflows (13 operation + 7 validation)
    ├── README.md                               # Workflow system overview
    ├── AGENTS.md                               # Workflow selection (for AI)
    ├── adapter.md                              # Create/update project adapter
    ├── adapter-auto.md                         # Auto-detect adapter from codebase
    ├── adapter-manual.md                       # Manual adapter setup
    ├── adapter-bootstrap.md                    # Bootstrap minimal adapter
    ├── adapter-agents.md                       # Create/update AI agent config
    ├── adapter-validate.md                     # Validate adapter completeness
    ├── business-context.md                     # Create/update BUSINESS.md
    ├── business-validate.md                    # Validate BUSINESS.md
    ├── adr.md                                  # Create/add/edit ADRs
    ├── adr-validate.md                         # Validate ADR.md
    ├── design.md                               # Create/update DESIGN.md
    ├── design-validate.md                      # Validate DESIGN.md
    ├── features.md                             # Create/update FEATURES.md
    ├── features-validate.md                    # Validate FEATURES.md
    ├── feature.md                              # Create/update feature design
    ├── feature-validate.md                     # Validate feature design
    ├── feature-changes.md                      # Create/update CHANGES.md
    ├── feature-changes-validate.md             # Validate CHANGES.md
    ├── feature-change-implement.md             # Implement feature changes
    └── feature-code-validate.md                # Validate entire feature code

{adapter-directory}/                # Your project adapter (created by workflow)
├── AGENTS.md                                   # AI instructions (project-specific)
└── specs/                                      # Detailed specifications
    ├── domain-model.md                         # Domain model format
    ├── api-contracts.md                        # API contracts format
    ├── testing.md                              # Testing strategy
    └── build.md                                # Build and deployment

architecture/                                    # Your designs (created by workflows)
├── BUSINESS.md                                 # Business context
├── DESIGN.md                                   # Overall Design
├── ADR.md                                      # Architecture Decision Records
├── diagrams/                                   # Architecture diagrams
└── features/                                   # Feature designs
    ├── FEATURES.md                            # Feature manifest
    └── feature-{slug}/                        # Individual features
        ├── DESIGN.md                          # Feature design
        └── CHANGES.md                         # Implementation changes
```


---

## Documentation

### For Developers

- **This File** (`README.md`) - Overview, getting started, team workflow
- **`QUICKSTART.md`** - 5-minute quick start guide with examples
- **`WORKFLOW.md`** - Workflow system overview and best practices
- **`requirements/FDL.md`** - FDD Description Language syntax guide
- **`CLISPEC.md`** - CLI command specification format
- **`workflows/README.md`** - All 20 workflows overview
- **`skills/SKILLS.md`** - Skills discovery protocol for AI agents

### For AI Assistants

- **`AGENTS.md`** - Core FDD methodology for AI
- **`workflows/AGENTS.md`** - Workflow selection guide for AI
- **Project adapter's `AGENTS.md`** - Project-specific AI instructions

### For Creating Adapters

- **`ADAPTER_GUIDE.md`** - Complete guide for creating project adapters
- **`workflows/adapter.md`** - Interactive workflow for adapter creation/update

---

## FAQs

### Do I need AI assistants to use FDD?

**Recommended.** FDD is specifically designed to work with AI assistants that support agentic workflows. While workflows are human-readable, manual execution can be challenging and time-consuming.

**Without AI assistants**:
- You'll need a full team (architect + developers + QA)
- Workflows must be followed manually
- More overhead for validation and tracking

**With AI assistants** (recommended):
- Single expert (architect) can handle entire workflow
- AI follows workflows automatically
- Faster design generation and validation
- AI implements changes from CHANGES.md

### What tech stack do I need?

**Any.** FDD is technology-agnostic. You choose:
- Domain model format (GTS, CTI, JSON Schema, TypeScript, Protobuf, etc.)
- API format (OpenAPI, RAML, GraphQL, gRPC, etc.)
- Implementation language (JavaScript, Python, Go, etc.)

Your **adapter** documents these choices.

### How long does it take to set up?

- **Add FDD core**: 5 minutes
- **Create adapter**: 1-2 hours (first time)
- **Initialize project**: 30 minutes
- **First feature design**: 1-2 hours

After initial setup, feature design time depends on complexity.

### Can I use FDD with existing projects?

**Yes.** You can:
1. Add FDD to existing project
2. Create adapter for existing tech stack
3. Start documenting new features in FDD
4. Gradually migrate existing features (optional)


### What if my team doesn't know FDD?

Follow the onboarding checklist:
1. **Reading** (30 min): README.md, FDL.md, workflows/README.md
2. **Setup** (15 min): IDE, tools, adapter review
3. **Practice** (2 hours): Review example feature, create small feature with guidance

### How do I validate designs?

Follow validation workflows:
- **Business Context**: `workflows/business-validate.md`
- **Overall Design**: `workflows/design-validate.md`
- **Feature Design**: `workflows/feature-validate.md`

Validation is done via checklists (manual review). AI assistants can help automate checks.

---

## Examples

### Example: Login Feature

**Business Context** (`architecture/BUSINESS.md`):
```markdown
## B. Actors
- **End User**: Person accessing the system

## C. Capabilities
- User authentication with email/password
```

**Overall Design** (`architecture/DESIGN.md`):
```markdown
## C. Technical Architecture

### Domain Model
- User (id, email, passwordHash, createdAt)
- Session (id, userId, token, expiresAt)

### API Contracts
- POST /auth/login (email, password) → session token
```

**Feature Design** (`architecture/features/feature-login/DESIGN.md`):
```markdown
## B. Actor Flows

### Actor: End User

1. User navigates to login page
2. User enters email and password
3. User clicks "Login" button
4. System validates credentials
5. IF credentials valid
   5.1. System creates session
   5.2. System redirects to dashboard
6. ELSE
   6.1. System shows error "Invalid credentials"
   6.2. User remains on login page
```

**Implementation Changes** (`architecture/features/feature-login/CHANGES.md`):
```markdown
# Feature Login - Implementation Changes

## Change 001: User Authentication

**Purpose**: Implement user authentication with email/password.

**Tasks**:
- [ ] Create User model (email, passwordHash fields)
- [ ] Create authentication endpoint POST /auth/login
- [ ] Add password hashing with bcrypt
- [ ] Add session management (JWT tokens)
- [ ] Create login page UI
- [ ] Add unit tests for auth logic
- [ ] Add e2e tests for login flow

**Status**: In Progress
**Assigned**: Developer Team
```

---

## References

- **FDD GitHub**: https://github.com/ainetx/fdd
- **GTS (Global Type System)**: https://github.com/GlobalTypeSystem/gts-spec
- **CTI (Common Type Interface)**: https://github.com/acronis/go-cti

---

## Version History

### v1.0 (Current)

**Features**:
- Core + Adapters architecture (technology-agnostic core, framework-specific adapters)
- Universal Workflows (18 workflows: 10 operation + 8 validation)
- 7-layer design flow (Business Context → Design → Features → Implementation)
- Implementation change management (CHANGES.md)
- FDD Description Language (FDL)
- CLISPEC format (CLI command specification)
- Design Requirements (formal specifications without prescribing technologies)
- Validation-first approach
- Framework adapters pattern
- Quick start guide for rapid onboarding

**Structure**:
- Core FDD (universal, framework-agnostic methodology)
- Project adapters (technology-specific integration)
- 20 workflows: 13 operation + 7 validation (IDE-agnostic guides)
- Claude-compatible skill (`fdd` - unified validation, search & traceability)
- Design requirements (formal specifications without technology lock-in)
- Built-in formats (FDL, CLISPEC)

**Documentation**:
- Complete methodology guide (README.md)
- Quick start guide (QUICKSTART.md)
- 20 workflows: 13 operation + 7 validation (IDE-agnostic)
- FDD Description Language spec (requirements/FDL.md)
- CLI specification format (CLISPEC.md)
- Skills system for AI agents (skills/)
- Framework adapter templates

---

## License

Apache License 2.0

Copyright (c) 2026 FDD Contributors

Licensed under the Apache License, Version 2.0 (the "License");
you may not use this file except in compliance with the License.
You may obtain a copy of the License at

    http://www.apache.org/licenses/LICENSE-2.0

Unless required by applicable law or agreed to in writing, software
distributed under the License is distributed on an "AS IS" BASIS,
WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
See the License for the specific language governing permissions and
limitations under the License.

---

## Contributing

When FDD becomes a separate repository:
1. Follow FDD methodology for FDD changes
2. Update workflows with real-world examples
3. Maintain backward compatibility
4. Document breaking changes
