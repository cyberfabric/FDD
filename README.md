# Feature-Driven Design (FDD)

**Version**: 1.0  
**Status**: Active  
**Audience**: Development teams, technical leads, architects

Feature-Driven Design is a **universal methodology** for building software systems with clear traceability from requirements to implementation.

**Built for modern development**: FDD works with AI coding assistants, supports any tech stack, and provides structured workflows that teams can follow manually or automate.

---

## What is FDD?

FDD helps teams build software by:

1. **Designing before coding**: Document what you're building in clear, reviewable formats
2. **Breaking work into features**: Each feature is independent and testable
3. **Using plain English**: Algorithms described in FDL (not code), reviewable by non-programmers
4. **Tracking changes atomically**: OpenSpec ensures every change is traceable
5. **Validating designs**: Catch issues before implementation

---

## The AGENTS.md Foundation

### Built on Industry Standard for AI Frameworks

FDD is built on the **AGENTS.md approach** - an emerging industry standard for structuring AI-native frameworks and methodologies. This isn't just a documentation pattern; it's **the starting point** for any AI-assisted development framework.

**What is AGENTS.md?**

A standardized file (`AGENTS.md`) that serves as the **single source of truth** for AI agents, containing:
- Complete methodology rules and constraints
- Workflow references and execution patterns
- Tool usage instructions
- Project-specific context and conventions

**Why AGENTS.md is the Superior Approach**:

| Traditional Approach | AGENTS.md Approach |
|---------------------|-------------------|
| ❌ Scattered docs across README, wikis, comments | ✅ Single entry point for AI agents |
| ❌ AI must search and piece together context | ✅ Complete context in one place |
| ❌ Inconsistent interpretation of rules | ✅ Unambiguous, machine-readable instructions |
| ❌ Manual workflow execution prone to errors | ✅ Workflows referenced and executable |
| ❌ No separation of human vs AI documentation | ✅ Optimized specifically for AI consumption |
| ❌ Changes require updating multiple locations | ✅ Update once, agents always have latest |

**Industry Adoption - The Emerging Standard**:

The AGENTS.md pattern is being adopted across major AI frameworks:

1. **OpenSpec** (Fission AI)
   - `openspec/AGENTS.md` - complete change management methodology
   - Used by thousands of developers
   - Standard pattern: human docs in README, AI docs in AGENTS.md

2. **FDD** (This Framework)
   - `spec/FDD/AGENTS.md` - core methodology
   - `spec/FDD-Adapter/AGENTS.md` - project-specific extensions
   - Two-level AGENTS.md hierarchy for universal + specific rules

3. **Cursor AI** (`.cursorrules`)
   - Early adopter of "rules file for AI" concept
   - Single-file format (precursor to AGENTS.md)
   - Proves demand for AI-specific instruction files

4. **Anthropic Claude** (MCP protocol)
   - Model Context Protocol servers expose resources
   - Pattern: structured context for AI agents
   - Aligns with AGENTS.md philosophy

5. **Windsurf/Cline/Aider**
   - All support agent-specific config files
   - Moving toward standardized formats
   - AGENTS.md provides that standardization

**Why This is the Best Approach for AI Frameworks**:

✅ **Instant Context Loading**
```
AI Agent starts → Reads AGENTS.md → Has complete methodology
```
No searching, no ambiguity, immediate understanding.

✅ **Workflow Automation**
```
AGENTS.md references: workflows/05-init-feature.md
AI Agent: Follows workflow step-by-step automatically
```
Workflows become executable, not just documentation.

✅ **Version Control for AI Instructions**
```
git log spec/FDD/AGENTS.md
→ See exactly when methodology rules changed
→ Trace why AI behaves differently across versions
```

✅ **Composable Context**
```
FDD/AGENTS.md (universal rules)
    ↓ extends
FDD-Adapter/AGENTS.md (project-specific)
    ↓ extends
FDD-Adapter/workflows/AGENTS.md (workflow overrides)
```
Layered approach: core + extensions, never duplicated.

✅ **Human + AI Harmony**
- README.md → Human-readable overview
- AGENTS.md → Machine-optimized instructions
- Both reference same workflows, same structure
- No duplication, no drift

**FDD's AGENTS.md Architecture**:

```
spec/FDD/AGENTS.md                    # ← STARTING POINT
├─ Core Methodology Rules             (immutable, validated)
├─ Design Hierarchy                   (OVERALL → FEATURE → OpenSpec → CODE)
├─ Workflow References                (15 universal workflows)
└─ OpenSpec Integration               (atomic change management)
    ↓ AI agent reads this FIRST
    
spec/FDD-Adapter/AGENTS.md            # ← PROJECT CONTEXT
├─ Domain Model Technology            (GTS, JSON Schema, etc.)
├─ API Contract Format                (OpenAPI, CLISPEC, etc.)
├─ Project Conventions                (naming, structure, security)
└─ Workflow Extensions                (project-specific steps)
    ↓ Extends core, never contradicts
    
spec/FDD-Adapter/workflows/AGENTS.md  # ← WORKFLOW OVERRIDES
└─ Custom workflow selection logic    (optional, project-specific)
```

**The Starting Point: Always AGENTS.md**

When an AI agent encounters a project using FDD:

```
Step 1: Agent reads spec/FDD-Adapter/AGENTS.md
        ↓
        "READ FIRST: spec/FDD/AGENTS.md"
        
Step 2: Agent reads spec/FDD/AGENTS.md
        ↓
        Core methodology loaded
        
Step 3: Agent reads project adapter (FDD-Adapter/AGENTS.md)
        ↓
        Project-specific context loaded
        
Step 4: Agent is ready
        ↓
        Complete understanding: methodology + project + workflows
```

**No other file is needed before starting.** AGENTS.md is the root of everything.

**Proof This Works: Real-World Results**

FDD development using AGENTS.md approach:
- ✅ **fdd-cli** built entirely with AI agents following FDD/AGENTS.md
- ✅ Complete designs created in minutes (not hours)
- ✅ Zero ambiguity - agent never "guesses" what to do
- ✅ Consistent structure across all features
- ✅ Workflows executed correctly without human intervention

**The Future: AGENTS.md as Standard**

We believe AGENTS.md will become the universal pattern for:
- ✅ Development frameworks (FDD, OpenSpec, etc.)
- ✅ Build tools (Maven, Gradle, npm with AI integration)
- ✅ Testing frameworks (Jest, Pytest with agent runners)
- ✅ CI/CD systems (GitHub Actions, GitLab CI with AI steps)

**Every project will have AGENTS.md** - just like every project has README.md today.

---

## Key Strengths

### 1. 🎯 Interactive Workflows - Your AI Pair Programmer

FDD provides **15 interactive workflows** that guide you step-by-step through the entire development process. Each workflow asks questions, validates answers, and creates exactly what you need.

**Example: Creating a Project Adapter**

Instead of reading documentation and figuring out what to do, just run:
```
Follow @spec/FDD/workflows/adapter-config.md
```

The workflow asks 8 targeted questions:
```
Q1: What is your project name?
→ "fdd-cli"

Q2: Choose domain model technology:
   1. GTS (Global Type System)
   2. JSON Schema
   3. TypeScript interfaces
   ...
→ Select: 1

Q3: Choose API contract format:
   1. OpenAPI/Swagger
   2. CLISPEC (for CLI tools)
   3. GraphQL
   ...
→ Select: 2
```

**Result**: Fully configured adapter created in 5-10 minutes. No guessing, no mistakes.

**Example: Initializing a Feature**

```
Follow @spec/FDD/workflows/05-init-feature.md
```

Workflow guides you through:
- Q1: Feature name and slug
- Q2: Feature purpose (extracted or custom)
- Q3: Actors involved
- Q4: Dependencies on other features
- Q5: Planned OpenSpec changes

**Result**: Complete feature directory with DESIGN.md template, openspec structure, and entry in FEATURES.md - all in 10 minutes.

**Why This Is Powerful**:
- ✅ **No memorization** - Workflows guide you every time
- ✅ **No mistakes** - Each step validated before proceeding
- ✅ **Consistent results** - Same structure every time
- ✅ **AI-friendly** - AI agents follow workflows naturally
- ✅ **Human-readable** - Anyone can execute manually if needed

### 2. 🔧 Adapter System - Works With Any Tech Stack

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
- ✅ **Use your existing stack** - No forced technology choices
- ✅ **Migrate gradually** - Add FDD to existing projects
- ✅ **Team flexibility** - Different teams, different stacks, same methodology
- ✅ **Future-proof** - New tech? Just create new adapter

### 3. 📋 Workflow-Driven Development - Everything Has a Process

In FDD, **every action is a workflow**. Development becomes predictable and repeatable.

**Workflow Phases**:

```
Phase 0: Setup & Legacy Integration
├─ adapter-config.md        → Create project adapter (greenfield)
├─ adapter-config-from-code.md → Create adapter from existing code
├─ 01-init-project-from-code.md → Init project from existing code
└─ config-agent-tools.md    → Configure AI agent (optional)

Phase 1: Architecture
├─ 01-init-project.md       → Initialize FDD structure
└─ 02-validate-architecture.md → Validate Overall Design

Phase 2: Feature Planning
├─ 03-init-features.md      → Generate features from design
├─ 04-validate-features.md  → Validate feature manifest
├─ 05-init-feature.md       → Create single feature
└─ 06-validate-feature.md   → Validate feature design

Phase 3: Implementation
├─ 09-openspec-init.md      → Initialize OpenSpec
├─ 10-openspec-change-implement.md → Implement change
├─ 11-openspec-change-complete.md  → Complete change
├─ 12-openspec-change-next.md      → Create next change
├─ 13-openspec-validate.md  → Validate OpenSpec structure
├─ 07-complete-feature.md   → Mark feature complete
└─ 08-fix-design.md         → Fix design issues
```

**Real Development Flow**:
```
Day 1: Create adapter (workflow adapter-config)
       → 10 minutes, adapter ready

Day 2: Initialize project (workflow 01)
       → 30 minutes, architecture/ created
       
       Write Overall Design
       → 2-3 hours, DESIGN.md complete
       
       Validate design (workflow 02)
       → 5 minutes, score 95/100 ✅

Day 3: Generate features (workflow 03)
       → 5 minutes, 8 features extracted
       
       Validate features (workflow 04)
       → 5 minutes, manifest validated ✅

Week 1-2: For each feature:
          - Initialize (workflow 05) → 10 min
          - Write design → 1-2 hours
          - Validate (workflow 06) → 5 min
          - Init OpenSpec (workflow 09) → 5 min
          - Implement changes (workflow 10) → variable
          - Complete (workflow 07) → 5 min
```

**Why Workflows Matter**:
- ✅ **Nothing forgotten** - Checklists ensure completeness
- ✅ **Clear handoffs** - Team knows exactly what to do next
- ✅ **Progress tracking** - Always know where you are
- ✅ **Onboarding speed** - New members follow workflows
- ✅ **Quality gates** - Validation before proceeding

### 4. 🤝 Deep OpenSpec Integration - Design to Code Traceability

**IMPORTANT**: FDD does **NOT** rewrite or replace OpenSpec. FDD **includes and manages** OpenSpec as the implementation layer.

FDD and OpenSpec form a **complete system**: FDD designs WHAT to build, OpenSpec tracks HOW you build it.

**The Synergy Explained**:

```
Overall Design (Architecture)
├─ WHAT: System capabilities
├─ WHO: Actors and roles
└─ WHY: Business context
    ↓
    
Feature Design
└─ HOW: Actor flows, algorithms, technical approach
    ↓
    
OpenSpec Changes
└─ IMPLEMENTATION: Atomic, traceable code changes
```

**How FDD Uses OpenSpec (Not Rewrites It)**:

1. **FDD includes OpenSpec AGENTS.md as-is**
   - `spec/FDD/openspec/AGENTS.md` is generated by `openspec` CLI tool
   - Used as additional context for AI agents
   - Never modified or contradicted by FDD

2. **FDD workflows manage OpenSpec tool**
   - Workflows 09-12 wrap `openspec` CLI commands
   - All OpenSpec commands used (except `openspec init`)
   - `openspec init` skipped: FDD creates structure manually to avoid duplicate workflows

3. **FDD validates against OpenSpec rules**
   - Feature designs reference OpenSpec change structure
   - No contradictions with OpenSpec methodology
   - All workflows validated against `openspec/AGENTS.md`

4. **OpenSpec is the implementation layer**
   - Feature DESIGN.md → lists OpenSpec changes (Section F)
   - Each OpenSpec change → implements part of Feature Design
   - OpenSpec `proposal.md` → references specific Feature Design sections

**The Integration**:

```
FDD Feature Design (DESIGN.md)
│
├─ Section B: Actor Flows
│  → Defines what users do
│
├─ Section F: Implementation Plan
│  → Lists OpenSpec changes needed
│
└─ Validated ✅
    ↓
    
OpenSpec Changes (openspec/changes/)
│
├─ Change 001: Authentication
│  ├─ proposal.md  → Why (references DESIGN.md Section B)
│  ├─ tasks.md     → Implementation steps
│  └─ specs/       → Technical specifications
│
├─ Change 002: Authorization
│  └─ ... (same structure)
│
└─ All changes implement exactly what Feature Design specified
```

**Concrete Example**:

**Feature Design** (`feature-login/DESIGN.md`):
```markdown
## B. Actor Flows

### Flow: User Login
1. User enters email and password
2. System validates credentials
3. System creates session
4. System redirects to dashboard

## F. Implementation Plan

### OpenSpec Changes
1. `setup-user-model` - Create User entity and database schema
2. `implement-auth` - Add authentication logic and session management
3. `create-login-ui` - Build login page and form validation
```

**OpenSpec Changes** (`feature-login/openspec/changes/`):
```
001-setup-user-model/
├─ proposal.md    → "Implements User entity from Feature DESIGN.md Section E"
├─ tasks.md       → Checklist referencing design specs
└─ specs/         → User model specification

002-implement-auth/
├─ proposal.md    → "Implements Actor Flow 'User Login' from Section B"
├─ tasks.md       → Credential validation, session creation
└─ specs/         → Auth API specification

003-create-login-ui/
├─ proposal.md    → "Implements UI for Actor Flow from Section B"
└─ tasks.md       → Form, validation, error handling
```

**Why This Synergy Is Powerful**:
- ✅ **Complete traceability** - Business requirement → design → implementation → code
- ✅ **No ambiguity** - Every OpenSpec change references specific design section
- ✅ **Review at right level** - Stakeholders review design, developers review changes
- ✅ **Audit trail** - Know why every change was made
- ✅ **Rollback safety** - Can revert changes without breaking design coherence

### 5. 📝 FDL (FDD Description Language) - Logic Without Code

FDD uses **FDL** - plain English pseudocode for describing algorithms, actor flows, and state machines. This is one of FDD's most powerful innovations.

**What is FDL?**

Plain English syntax for describing logic that **anyone can read**, not just programmers:

```
1. User clicks "Add to Cart" button
2. System checks if item is in stock
   2.1. IF out of stock
       2.1.1. Show error "Item unavailable"
       2.1.2. STOP
3. System adds item to cart
4. System updates cart count
5. Show success message "Item added"
```

**Why FDL is a Game-Changer**:

✅ **Stakeholders Can Review Logic**
- Business analysts review actor flows
- Product managers validate user experiences
- QA designs test scenarios from flows
- No programming knowledge needed

✅ **Language-Agnostic Design**
- Same design works for Python, JavaScript, Go, any language
- Refactor implementation without changing design
- Multiple teams can implement same design differently

✅ **AI-Friendly**
- AI agents convert FDL → code automatically
- No ambiguity in instructions
- Clear step-by-step logic

✅ **Focus on Logic, Not Syntax**
- Designers think about "what happens" not "how to code it"
- No distractions from language-specific details
- Catch logical errors before coding

**Real Example: Authentication Flow**

**FDL in DESIGN.md**:
```
### Flow: User Login

1. User submits login form
2. System validates email format
   2.1. IF invalid format
       2.1.1. Show error "Invalid email address"
       2.1.2. STOP
3. System checks credentials in database
4. IF credentials match
   4.1. Generate session token
   4.2. Store token in cookies
   4.3. Redirect to dashboard
5. ELSE
   5.1. Increment failed login counter
   5.2. IF failed attempts >= 3
       5.2.1. Lock account for 15 minutes
       5.2.2. Send security email
   5.3. Show error "Invalid credentials"
```

**Review Process**:
- Product Manager reads → "Yes, this matches requirements"
- Security Team reads → "Add rate limiting at step 5.2"
- QA reads → "I'll test all branches: valid, invalid format, wrong password, account lock"
- Developer reads → "Clear implementation path"

**Then AI converts to code** - but the logic was reviewed and approved first.

**FDL vs Code in Design Docs**:

| Code in DESIGN.md | FDL in DESIGN.md |
|-------------------|------------------|
| ❌ Only programmers can review | ✅ Anyone can review |
| ❌ Couples design to language | ✅ Language-agnostic |
| ❌ Syntax distracts from logic | ✅ Pure logic focus |
| ❌ Outdates when refactored | ✅ Stable across refactors |
| ❌ AI may misinterpret | ✅ Clear AI instructions |

**Where FDL is Used**:

1. **Actor Flows** (Section B) - PRIMARY
   - What each actor does step-by-step
   - All interactions and user journeys

2. **Algorithms** (Section C)
   - Business logic processing
   - Data transformations
   - Calculations and validations

3. **State Machines** (Section D, optional)
   - State transitions
   - Conditions for state changes
   - Actions on state entry/exit

**FDL Syntax Guide**:

```
Basic structure:
1. Action or event
2. Another action
   2.1. Nested detail
   2.2. Another detail
3. Conditional
   3.1. IF condition
       3.1.1. Action if true
   3.2. ELSE
       3.2.1. Action if false
4. Loops
   4.1. FOR EACH item in list
       4.1.1. Process item
5. STOP - terminates flow

Keywords (ALL CAPS):
- IF / ELSE - conditions
- FOR EACH - loops
- STOP - terminate
- AND / OR - logical operators
- WHILE - conditional loops
```

**Why No Code in Designs**:

FDD **strictly prohibits code** in DESIGN.md files:
- ❌ No `if (x > 5) { ... }` syntax
- ❌ No function definitions
- ❌ No framework-specific patterns
- ✅ Only FDL plain English

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

**See Full FDL Specification**: `spec/FDD/FDL.md`

### 6. 🏗️ Structured Project Organization - Rules and Validation

FDD enforces **consistent structure and validation** across your entire project.

**Project Structure Rules**:

```
architecture/
├── DESIGN.md                    # Overall Design (required)
│   ├── Section A: Business Context
│   ├── Section B: Requirements
│   ├── Section C: Technical Architecture
│   └── Section D: Project Details (optional)
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
        │   └── Section F: Implementation Plan
        │
        └── openspec/           # OpenSpec structure (standard)
            ├── project.md
            ├── specs/          # Source of truth
            └── changes/        # Active and archived
```

**Validation Rules Enforced**:

**Overall Design Validation** (workflow 02):
- ✅ All sections present (A, B, C)
- ✅ All actors defined
- ✅ Domain model documented (in chosen DML format)
- ✅ API contracts documented (in chosen format)
- ✅ No contradictions in architecture
- ✅ Score ≥90/100 before proceeding

**Feature Design Validation** (workflow 06):
- ✅ All sections present (A-F)
- ✅ Section B (Actor Flows) is PRIMARY and complete
- ✅ Algorithms in FDL only (no code)
- ✅ No type redefinitions (must reference Overall Design)
- ✅ All dependencies declared
- ✅ OpenSpec changes planned
- ✅ Score 100/100 + 100% completeness

**Documentation Rules**:
- ✅ **FDL only in designs** - No code in DESIGN.md files
- ✅ **Single source of truth** - Types defined once in Overall Design
- ✅ **Cross-references validated** - All references must exist
- ✅ **Status tracking** - Feature status always accurate
- ✅ **Dependency checking** - No circular dependencies allowed

**Why Structure and Validation Matter**:
- ✅ **Consistency** - Every feature follows same pattern
- ✅ **Quality gates** - Can't proceed with incomplete designs
- ✅ **Team coordination** - Everyone knows where to find things
- ✅ **Maintenance ease** - Structure is predictable
- ✅ **AI-friendly** - Clear structure helps AI navigate and generate

**Example Validation Failure**:
```
❌ Feature Design Validation Failed

Issues Found:
1. Section B (Actor Flows) incomplete - missing "User Logout" flow
2. Section E redefines type "User" - must reference Overall Design
3. Section F missing OpenSpec change for "session management"

Score: 78/100 (minimum: 100/100)
Completeness: 85% (minimum: 100%)

→ Fix issues and re-run validation (workflow 06)
```

---

## Why Use FDD?

### What You Get With FDD

**For Single Expert / Architect**:
- 🤖 **AI does 80% of the work**: Design → validation → implementation automated
- 📋 **Living documentation**: Designs stay up-to-date with code (enforced by validation)
- 🔍 **Full traceability**: From business requirement → design → code change
- ⚡ **Faster delivery**: AI handles boilerplate, you focus on business logic
- 🎯 **Catch issues early**: Validation happens before coding

**For Teams**:
- 👥 **Stakeholders can review**: Actor flows in plain English, no code knowledge needed
- 🔄 **Clear handoffs**: Feature designs are complete specs, not ambiguous tickets
- 📊 **Progress tracking**: FEATURES.md shows exactly what's done/in-progress/pending
- 🛡️ **Consistency**: Workflows enforce same standards across all features
- 📚 **Onboarding**: New team members read designs, not reverse-engineer code

**For Business**:
- 💰 **Lower costs**: Less rework, fewer bugs, faster development
- 📈 **Predictability**: Features have complete designs before implementation
- 🔒 **Risk reduction**: Validation catches architectural issues early
- 📖 **Audit trail**: Every change is documented and traceable

### What Happens Without FDD

**The typical scenario**:
1. 📝 Developer starts coding from vague requirements
2. 🤔 Discovers edge cases during implementation
3. 🔄 Goes back to architect/PM for clarification
4. ⏰ Delays accumulate, scope creeps
5. 🐛 Bugs discovered after deployment (logic wasn't reviewed)
6. 📉 Technical debt grows (no overall design document)
7. 🔥 Refactoring becomes risky (no source of truth)

**Specific problems FDD prevents**:

| Without FDD | With FDD |
|-------------|----------|
| ❌ Requirements in scattered Jira tickets | ✅ Complete Overall Design in one place |
| ❌ Stakeholders can't review logic | ✅ Actor flows reviewable by non-programmers |
| ❌ Type definitions duplicated across features | ✅ Domain model in Overall Design, referenced everywhere |
| ❌ API changes break other features | ✅ API contracts defined upfront, validated |
| ❌ "Documentation" outdated or missing | ✅ Designs validated against code, stay current |
| ❌ Developer interprets requirements differently | ✅ Feature Design is unambiguous spec |
| ❌ AI assistant generates inconsistent code | ✅ AI follows workflows, enforces patterns |
| ❌ Can't track feature dependencies | ✅ FEATURES.md shows dependency graph |
| ❌ Rework after stakeholder review | ✅ Stakeholders review design before coding |

### Why OpenSpec Alone Is Not Enough

**OpenSpec is excellent for change management**, but it solves only part of the problem:

**What OpenSpec Does Well** ✅:
- Tracks atomic changes
- Manages delta specifications
- Archives implementation history
- Validates change structure

**What OpenSpec Doesn't Solve** ❌:
- **No Overall Design**: Where do domain types come from? Who defines actors?
- **No Feature Planning**: How to break a large system into features?
- **No Cross-Feature Validation**: How to ensure features don't duplicate types or contradict each other?
- **No Actor Flows**: How to describe what users do in plain English?
- **No Design Review**: When and how to validate designs before coding?
- **No Dependency Management**: Which features depend on which?

**The Problem with OpenSpec-Only Approach**:

```
Developer creates openspec change 001
   ↓
Implements feature based on their understanding
   ↓
Another developer creates change 002 for different feature
   ↓
Discovers they need same types but defined differently
   ↓
No Overall Design to reference → inconsistency
   ↓
Refactoring needed, wasted time
```

**How FDD + OpenSpec Work Together**:

```
1. FDD: Create Overall Design
   - Define all domain types ONCE
   - Define all API contracts ONCE
   - Define all actors and use cases
   
2. FDD: Generate Features from Overall Design
   - Each feature has complete design
   - Features reference Overall Design (no duplication)
   - Dependencies explicitly tracked
   
3. FDD: Validate Feature Design
   - Check for type redefinitions
   - Validate actor flows
   - Ensure consistency with Overall Design
   
4. OpenSpec: Break feature into atomic changes
   - Each change implements part of validated design
   - Changes reference feature design specs
   - Implementation is traceable
   
5. OpenSpec: Track implementation
   - Archive completed changes
   - Merge specs to source of truth
   - Full audit trail
```

**TL;DR**: OpenSpec manages **how you implement**, FDD defines **what you implement**. You need both for large projects.

---

### When NOT to Use FDD

FDD adds structure and validation. Skip it if:
- ❌ Prototype/throwaway code (no need for design docs)
- ❌ Trivial changes (single-line fixes)
- ❌ Well-understood patterns (no architectural decisions)

**Use FDD when**:
- ✅ Building production systems
- ✅ Working with AI assistants
- ✅ Need stakeholder review
- ✅ Multiple features with dependencies
- ✅ Long-term maintenance expected

---

## Core Components

### 1. Two-Level Design

**Overall Design** (`architecture/DESIGN.md`):
- System vision and capabilities
- All actors and use cases
- Domain model types (formally specified)
- API contracts (formally specified)
- Architecture diagrams

**Feature Design** (`architecture/features/feature-{slug}/DESIGN.md`):
- What this feature does
- Actor flows (how users interact)
- Algorithms in FDL (plain English logic)
- Technical details (database, security, etc.)
- Testing scenarios

### 2. OpenSpec (Change Management)

Break features into atomic, traceable changes:

```
feature-login/
└── openspec/
    ├── specs/          # Completed changes
    └── changes/        # Active work
        └── 001-authentication/
            ├── proposal.md   # Why
            ├── tasks.md      # What to do
            └── specs/        # Implementation details
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
1. `README.md` (this file) - Overview
2. `QUICKSTART.md` - 5-minute quick start guide with examples
3. `FDL.md` - Learn plain English algorithm syntax
4. `workflows/README.md` - Understand workflow system

### 2. Add FDD to Your Project (15 minutes)

**Option A: Copy FDD core**
```bash
# In your project root
mkdir -p guidelines
cp -r /path/to/FDD guidelines/FDD
```

**Option B: Git submodule** (recommended for shared projects)
```bash
git submodule add <fdd-repo-url> guidelines/FDD
```

### 3. Create Project Adapter (5-10 minutes) 🤖

**Run workflow**: `workflows/adapter-config.md` (interactive)

Or use AI agent:
```
Follow @guidelines/FDD/workflows/adapter-config.md to create FDD adapter
```

This interactive workflow will:
1. Ask 8 guided questions about your project
2. Choose domain model format (GTS, JSON Schema, TypeScript, etc.)
3. Choose API contract format (OpenAPI, GraphQL, CLISPEC, etc.)
4. Capture security model and non-functional requirements
5. Generate `spec/FDD-Adapter/AGENTS.md` and `spec/FDD-Adapter/workflows/AGENTS.md`

**Result**: Adapter created at `spec/FDD-Adapter/` with status COMPLETE or INCOMPLETE

For manual setup, see: **`ADAPTER_GUIDE.md`**

### 4. Configure AI Agent (2 minutes, optional) 🤖

**Run workflow**: `workflows/config-agent-tools.md` (interactive)

This optional workflow sets up your AI agent (Windsurf, Cursor, Cline, Aider) to use FDD natively:
- Creates agent-specific configuration files
- Windsurf: `.windsurf/rules.md` + workflow wrappers
- Cursor: `.cursorrules` (single file)
- Cline: `.clinerules` (single file)
- Aider: `.aider.conf.yml` (YAML config)

All configs:
- ✅ Tell agent to read FDD adapter first
- ✅ Provide FDD workflow references
- ✅ Follow agent-specific format

**Result**: Agent reads `spec/FDD-Adapter/AGENTS.md` automatically

### 5. Initialize Architecture (30 minutes) 🤖

**AI agent workflow**: Ask your AI agent to follow `workflows/01-init-project.md`

Or manually:
```bash
# Create structure
mkdir -p architecture/features
mkdir -p architecture/diagrams

# Create Overall Design
cat > architecture/DESIGN.md << 'EOF'
# Overall Design

## A. Business Context
...
EOF
```

### 6. Start First Feature (1-2 hours) 🤖

**AI agent workflow**: Ask your AI agent to follow `workflows/05-init-feature.md`

Or manually:
```bash
# Create feature
mkdir -p architecture/features/feature-{name}

# Create design
cat > architecture/features/feature-{name}/DESIGN.md << 'EOF'
# Feature: {Name}

## A. Feature Overview
...
EOF
```

---

## IDE Setup

To set up your AI assistant (Windsurf, Cursor, Cline, etc.) to work natively with FDD:

**Use workflow**: `workflows/config-agent-tools.md`

This workflow creates agent-specific files (`.windsurf/rules.md`, workflow wrappers) so your agent reads the FDD adapter and uses FDD workflows naturally.

---

## Working with AI Assistants

FDD is designed to work with AI coding assistants (but doesn't require them).

### AI Limitations

AI assistants can:
- ✅ Initialize structures
- ✅ Generate design templates
- ✅ Validate against checklists
- ✅ Implement OpenSpec changes
- ✅ Write tests

Humans must:
- ❌ Define business requirements
- ❌ Make architectural decisions
- ❌ Review actor flows
- ❌ Approve designs
- ❌ Final code review

---

## Team Workflow

**Default**: FDD is designed for a **single expert** (typically an architect) who handles all design and implementation work. The roles below describe abstract responsibilities that can be delegated if desired.

### Roles (can be combined or delegated)

**Technical Lead / Architect** (core role):
- Creates Overall Design
- Reviews all Feature Designs
- Creates project adapter
- Defines validation rules

**Feature Owner** (optional delegation):
- Creates Feature Design
- Breaks feature into OpenSpec changes
- Reviews implementation
- Marks feature complete

**Developer** (optional delegation):
- Implements OpenSpec changes
- Writes tests
- Updates specs after changes

**Stakeholder / QA** (optional review):
- Reviews actor flows (plain English)
- Reviews algorithms in FDL (reviewable)
- Validates business logic

### Process

```
1. Architect creates Overall Design
   ↓ (validated by team)
   
2. Team reviews Overall Design
   ↓ (approved)
   
3. Generate features from Overall Design
   ↓ (FEATURES.md created)
   
4. For each feature:
   4.1. Feature Owner creates DESIGN.md
   4.2. Team reviews actor flows
   4.3. Validate feature design
   4.4. Initialize OpenSpec
   4.5. Developers implement changes
   4.6. Mark feature complete
```

### Design Reviews

**Overall Design Review**:
- All team members review
- Stakeholders review vision and actors
- Technical team validates architecture
- Must score ≥90/100 before proceeding

**Feature Design Review**:
- Feature Owner presents
- Team reviews actor flows (Section B is PRIMARY)
- Algorithms in FDL reviewed by stakeholders
- Technical details reviewed by developers
- Must score 100/100 before implementation

### Implementation

**OpenSpec Change Implementation**:
- Developers pick changes from `openspec/changes/`
- Implement according to `tasks.md`
- Update `specs/` if needed
- Mark complete when tests pass

**Feature Completion**:
- All OpenSpec changes merged
- All tests pass
- Code compiles
- Feature marked ✅ in FEATURES.md

---

## Directory Structure

```
spec/FDD/                                       # Core FDD (standalone, universal)
├── README.md                                   # This file - overview, getting started
├── QUICKSTART.md                               # 5-minute quick start guide
├── AGENTS.md                                   # AI agent instructions
├── FDL.md                                      # FDD Description Language syntax
├── CLISPEC.md                                  # CLI command specification format
├── ADAPTER_GUIDE.md                            # How to create project adapter
└── workflows/                                  # 15 universal workflows
    ├── README.md                               # Workflow system overview
    ├── AGENTS.md                               # Workflow selection (for AI)
    ├── adapter-config.md                       # Create project adapter (Phase 0)
    ├── config-agent-tools.md                   # Configure AI agent tools (Phase 0, optional)
    ├── 01-init-project.md                      # Initialize FDD structure
    ├── 02-validate-architecture.md             # Validate Overall Design
    ├── 03-init-features.md                     # Generate features
    ├── 04-validate-features.md                 # Validate FEATURES.md
    ├── 05-init-feature.md                      # Initialize single feature
    ├── 06-validate-feature.md                  # Validate Feature Design
    ├── 07-complete-feature.md                  # Mark feature complete
    ├── 08-fix-design.md                        # Fix design issues
    ├── 09-openspec-init.md                     # Initialize OpenSpec
    ├── 10-openspec-change-implement.md         # Implement change
    ├── 11-openspec-change-complete.md          # Complete change
    ├── 12-openspec-change-next.md              # Create next change
    └── 13-openspec-validate.md                 # Validate OpenSpec

spec/FDD-Adapter/                               # Your project adapter (created by workflow)
├── AGENTS.md                                   # AI instructions (project-specific)
└── workflows/
    └── AGENTS.md                              # Workflow extensions (project-specific)

architecture/                                    # Your designs (created by workflows)
├── DESIGN.md                                   # Overall Design
├── diagrams/                                   # Architecture diagrams
└── features/                                   # Feature designs
    ├── FEATURES.md                            # Feature manifest
    └── feature-{slug}/                        # Individual features
        ├── DESIGN.md                          # Feature design
        └── openspec/                          # OpenSpec changes
```


---

## Documentation

### For Developers

- **This File** (`README.md`) - Overview, getting started, team workflow
- **`QUICKSTART.md`** - 5-minute quick start guide with examples
- **`FDL.md`** - FDD Description Language syntax guide
- **`CLISPEC.md`** - CLI command specification format
- **`workflows/README.md`** - All 14 workflows overview

### For AI Assistants

- **`AGENTS.md`** - Core FDD methodology for AI
- **`workflows/AGENTS.md`** - Workflow selection guide for AI
- **Project adapter's `AGENTS.md`** - Project-specific AI instructions

### For Creating Adapters

- **`ADAPTER_GUIDE.md`** - Complete guide for creating project adapters
- **`workflows/adapter-config.md`** - Interactive workflow for adapter creation

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
- AI implements OpenSpec changes

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

### Do I need to use OpenSpec?

**Yes**, OpenSpec is required for change tracking. It provides:
- Atomic, traceable changes
- Clear implementation tasks
- Audit trail
- Rollback capability

Install: `npm install -g @fission-ai/openspec@latest`

### What if my team doesn't know FDD?

Follow the onboarding checklist:
1. **Reading** (30 min): README.md, FDL.md, workflows/README.md
2. **Setup** (15 min): IDE, tools, adapter review
3. **Practice** (2 hours): Review example feature, create small feature with guidance

### How do I validate designs?

Follow validation workflows:
- **Overall Design**: `workflows/02-validate-architecture.md`
- **Feature Design**: `workflows/06-validate-feature.md`

Validation is done via checklists (manual review). AI assistants can help automate checks.

---

## Examples

### Example: Login Feature

**Overall Design** (`architecture/DESIGN.md`):
```markdown
## A. Business Context

### Actors
- **End User**: Person accessing the system

### System Capabilities
- User authentication with email/password
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

**OpenSpec Change** (`architecture/features/feature-login/openspec/changes/001-authentication/`):
```markdown
# proposal.md
Implement user authentication with email/password.

# tasks.md
- [ ] Create User model
- [ ] Create authentication endpoint
- [ ] Add password hashing
- [ ] Add session management
- [ ] Add login page
- [ ] Add tests
```

---

## FDD CLI Tool

**Status**: 🚀 **Active Development**

The `fdd-cli` tool automates FDD workflows - structure initialization, design validation, feature management, and consistency checks. It works alongside OpenSpec for complete design-to-code workflow automation.

**Repository**: [https://github.com/ainetx/fdd-cli](https://github.com/ainetx/fdd-cli)

**Why This Tool**:
- Automate FDD workflow execution (init, validate, generate)
- Enforce consistency across designs
- Integrate with OpenSpec for seamless change management
- Provide instant feedback on design quality

**Example Usage** *(in development)*:
```bash
fdd init                    # Initialize FDD structure
fdd validate architecture   # Validate Overall Design
fdd feature init <slug>     # Initialize new feature
fdd validate feature <slug> # Validate feature design
```

**Built with FDD**: The `fdd-cli` project itself is developed using FDD methodology - a real-world example of FDD in action. See the repository for complete designs, workflows, and implementation approach.

For detailed documentation, architecture, and implementation status, visit the repository.

---

## References

- **OpenSpec**: https://openspec.dev/

---

## Version History

### v1.0 (Current)

**Features**:
- Core + Adapters architecture (technology-agnostic core, framework-specific adapters)
- Universal Workflows (14 IDE-agnostic workflow guides)
- Two-level design (Overall Design → Feature Design)
- OpenSpec change management (universal)
- FDD Description Language (FDL)
- CLISPEC format (CLI command specification)
- Design Requirements (formal specifications without prescribing technologies)
- Validation-first approach
- Framework adapters pattern
- Quick start guide for rapid onboarding

**Structure**:
- Core FDD (universal, framework-agnostic methodology)
- Project adapters (technology-specific integration)
- 14 universal workflows (IDE-agnostic guides)
- Design requirements (formal specifications without technology lock-in)
- Built-in formats (FDL, CLISPEC)

**Documentation**:
- Complete methodology guide (README.md)
- Quick start guide (QUICKSTART.md)
- 14 universal workflows (IDE-agnostic)
- FDD Description Language spec (FDL.md)
- CLI specification format (CLISPEC.md)
- Framework adapter templates

---

## License

MIT License

Copyright (c) 2026 FDD Contributors

Permission is hereby granted, free of charge, to any person obtaining a copy
of this software and associated documentation files (the "Software"), to deal
in the Software without restriction, including without limitation the rights
to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
copies of the Software, and to permit persons to whom the Software is
furnished to do so, subject to the following conditions:

The above copyright notice and this permission notice shall be included in all
copies or substantial portions of the Software.

THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE
SOFTWARE.

---

## Contributing

When FDD becomes a separate repository:
1. Follow FDD methodology for FDD changes
2. Update workflows with real-world examples
3. Maintain backward compatibility
4. Document breaking changes
