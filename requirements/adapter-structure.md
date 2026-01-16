# FDD Adapter Structure Requirements

**ALWAYS open and follow**: `../workflows/adapter.md`
**ALWAYS open and follow**: `requirements.md`
**ALWAYS open and follow**: `core.md` WHEN editing this file
**ALWAYS open and follow**: `core.md` WHEN editing adapter artifacts

**This file defines**: Structure only (WHAT to create)  
**Workflow defines**: Process (HOW to create)

⚠️ **Do NOT use this file alone. Execute the workflow, not just the structure.**

---

**Version**: 1.0  
**Purpose**: Define structure and validation criteria for FDD Adapter

**Scope**: Project-specific adapter configuration that extends FDD core methodology

---

## Overview

**FDD Adapter** - Dynamic project-specific configuration that evolves with the project

**Philosophy**: 
- Adapter specs **derive from design decisions**, not predefined templates
- Technical decisions appear during design → captured in adapter
- Existing projects → adapter discovers patterns from code/docs/ADRs
- Greenfield projects → adapter starts minimal, grows with design

**Purpose**: Capture and formalize project-specific technical decisions:
- Tech stack (languages, frameworks, databases)
- Architecture patterns (discovered from design/code)
- Domain model format (determined during design)
- API contract format (determined during design)
- Code conventions (discovered from existing code or defined during development)
- Build/deploy practices (from configs or ADRs)
- Testing strategy (from design or existing tests)

**Lifecycle**:
1. **Bootstrap**: Minimal AGENTS.md with `Extends` only
2. **Discovery** (existing project): Scan code/docs/ADRs → propose specs
3. **Evolution** (during design): Design decisions → update adapter specs
4. **Refinement** (during implementation): Code patterns → update adapter specs

**Location**: `FDD-Adapter/` at project root (required)

**Correct locations**:
- `{project-root}/FDD-Adapter/` (recommended, simple path)
- `{project-root}/guidelines/FDD-Adapter/` (alternative)
- `{project-root}/spec/FDD-Adapter/` (alternative)
- `{project-root}/docs/FDD-Adapter/` (alternative)

**Important**: Adapter MUST be discoverable from project root. Avoid deep nesting in subdirectories.

**Bootstrap Structure**:
```
FDD-Adapter/
├── AGENTS.md              # Minimal: only Extends declaration
└── specs/                 # Created dynamically during workflows
    ├── tech-stack.md     # From DESIGN.md + ADRs + discovery
    ├── patterns.md       # From design decisions + code analysis
    ├── domain-model.md   # From DESIGN.md Section C.2
    ├── api-contracts.md  # From DESIGN.md Section C.3
    ├── conventions.md    # From code style + ADRs
    ├── build-deploy.md   # From configs + ADRs
    ├── testing.md        # From test frameworks + ADRs
    ├── snippets/         # Code examples from implementation
    └── examples/         # Pattern examples from features
```

---

## Required Files

### AGENTS.md

**Location**: `{adapter-directory}/FDD-Adapter/AGENTS.md`

**Purpose**: Adapter-specific navigation for AI agents (MUST WHEN format)

ALWAYS add to the header of AGENTS.md:

  ```markdown
  **ALWAYS open and follow**: `{FDD directory / submodule}/requirements/core.md` WHEN editing this file
  ```

**Adapter AGENTS.md WHEN rule (mandatory)**:
- Each navigation rule MUST use a WHEN clause that is ONLY a list of FDD workflows.
- The WHEN clause MUST NOT use generic conditions like "working with domain types".
- Allowed canonical form:
  - `ALWAYS open and follow {spec-file} WHEN executing workflows: {workflow1.md}, {workflow2.md}, ...`

**Two Phases**:

#### Phase 1: Bootstrap (Minimal)
**When**: Project initialization, no design yet
```markdown
# FDD Adapter: {Project Name}

**Extends**: `../FDD/AGENTS.md`
```

**That's it.** No specs, no MUST rules yet.

#### Phase 2: With Specs (After Discovery/Design)
**When**: After discovery workflow OR after design decisions
```markdown
# FDD Adapter: {Project Name}

**Extends**: `../FDD/AGENTS.md`

**Version**: {version}  
**Last Updated**: YYYY-MM-DD  
**Tech Stack**: {Primary language/framework}

---

ALWAYS open and follow `specs/tech-stack.md` WHEN executing workflows: adapter-auto.md, adapter-validate.md, design.md, design-validate.md, adr.md, adr-validate.md, feature-change-implement.md, feature-code-validate.md

ALWAYS open and follow `specs/domain-model.md` WHEN executing workflows: design.md, design-validate.md, adr.md, adr-validate.md, features.md, features-validate.md, feature.md, feature-validate.md, feature-changes.md, feature-changes-validate.md, feature-change-implement.md, feature-code-validate.md

ALWAYS open and follow `specs/api-contracts.md` WHEN executing workflows: design.md, design-validate.md, adr.md, adr-validate.md, feature.md, feature-validate.md, feature-changes.md, feature-changes-validate.md, feature-change-implement.md, feature-code-validate.md

ALWAYS open and follow `specs/patterns.md` WHEN executing workflows: design.md, design-validate.md, adr.md, adr-validate.md, feature.md, feature-validate.md, feature-change-implement.md, feature-code-validate.md

ALWAYS open and follow `specs/conventions.md` WHEN executing workflows: adapter.md, adapter-auto.md, adapter-manual.md, adapter-bootstrap.md, adapter-validate.md, feature-change-implement.md, feature-code-validate.md

ALWAYS open and follow `specs/build-deploy.md` WHEN executing workflows: feature-change-implement.md, feature-code-validate.md

ALWAYS open and follow `specs/testing.md` WHEN executing workflows: feature-change-implement.md, feature-code-validate.md

ALWAYS open and follow `specs/linting.md` WHEN executing workflows: feature-change-implement.md, feature-code-validate.md

ALWAYS open and follow `specs/security.md` WHEN executing workflows: design.md, design-validate.md, feature.md, feature-validate.md, feature-change-implement.md, feature-code-validate.md

ALWAYS open and follow `specs/performance.md` WHEN executing workflows: design.md, design-validate.md, feature.md, feature-validate.md, feature-change-implement.md, feature-code-validate.md

ALWAYS open and follow `specs/project-structure.md` WHEN executing workflows: adapter.md, adapter-auto.md, adapter-manual.md, adapter-bootstrap.md, adapter-validate.md, feature.md, feature-validate.md, feature-changes.md, feature-changes-validate.md
```

**Note**: Navigation rules are added **only after** corresponding spec files are created

**Specification Files** (created dynamically in `specs/`):

| Spec File | Created From | Contains |
|-----------|--------------|----------|
| `tech-stack.md` | DESIGN.md + ADRs + discovery | Languages, frameworks, databases, versions |
| `domain-model.md` | DESIGN.md Section C.2 + ADRs | Schema format, entity structure, examples |
| `api-contracts.md` | DESIGN.md Section C.3 + ADRs | Contract format, endpoint patterns, examples |
| `patterns.md` | Design decisions + code analysis | Architecture patterns, when to use, examples |
| `conventions.md` | Code analysis + ADRs + configs | Naming, style, file organization |
| `build-deploy.md` | Configs + ADRs + discovery | Build commands, CI/CD, deployment steps |
| `testing.md` | Test code + ADRs + discovery | Test frameworks, structure, commands |
| `linting.md` | Linter configs + ADRs | Linting rules, tools, custom lints |
| `security.md` | Security requirements + ADRs | Auth, validation, encryption, audit logging |
| `performance.md` | Performance requirements + ADRs | Benchmarks, profiling, optimization guidelines |
| `project-structure.md` | Directory analysis | File organization, module structure |
| `rest-api-guidelines.md` | API design + ADRs | REST conventions, endpoint patterns, versioning |
| `architectural-lints.md` | Custom lints + ADRs | Project-specific architectural rules |
| `module-creation.md` | Module patterns + ADRs | How to create new modules, templates |
| `snippets/{category}.md` | Implementation code | Reusable code snippets, utilities |
| `examples/{feature}.md` | Feature implementations | Pattern usage examples from features |

**Required spec structure** (applies to all spec files):

Each spec file MUST include:

1. **Header**: Version, Purpose, Scope
2. **Content sections**: Specific to spec type
3. **Validation criteria**: Checklist for agent self-verification
4. **Examples**: Valid and invalid examples with ✅/❌

**Validation criteria format**:
```markdown
## Validation Checklist

Agent MUST verify before implementation:
- [ ] Criterion 1: {specific check}
- [ ] Criterion 2: {specific check}
- [ ] Criterion 3: {specific check}

**Self-test**:
- [ ] Did I check all criteria?
- [ ] Are examples concrete and project-specific?
- [ ] Do commands work on target platform?
```

**Purpose**: Enable systematic agent self-checking during workflow execution

**Common spec categories**:
- **Core specs**: tech-stack, domain-model, api-contracts, conventions, testing, build-deploy
- **Quality specs**: linting, security, performance, architectural-lints
- **Structure specs**: project-structure, patterns, module-creation
- **API specs**: rest-api-guidelines (for REST APIs), graphql-guidelines (for GraphQL), cli-spec (for CLI tools)

**Creation triggers** (see adapter workflow)

---

## Validation Criteria

### Two-Phase Validation

Adapter validation depends on project phase:
- **Phase 1: Bootstrap** - Minimal adapter (new projects)
- **Phase 2: Evolved** - Full adapter with specs

---

### Phase 1: Bootstrap Validation (Minimal)

**Applies to**: New projects without specs yet

#### Structure

**Check**:
- [ ] AGENTS.md file exists at `{adapter-directory}/FDD-Adapter/AGENTS.md`
- [ ] Contains project name heading (e.g., `# FDD Adapter: ProjectName`)
- [ ] Contains `**Extends**: {path}/FDD/AGENTS.md` declaration

**Scoring**: All-or-nothing - 100/100 if all checks pass, 0/100 if any fails

**Pass threshold**: 100/100

---

### Phase 2: Evolved Adapter Validation

**Applies to**: Projects with DESIGN.md OR discovered codebase

#### Structure (25 points)

**Check**:
- [ ] AGENTS.md exists with Extends declaration (5)
- [ ] AGENTS.md has Version and Last Updated fields (5)
- [ ] AGENTS.md has Tech Stack summary (5)
- [ ] MUST rules present for each spec file (5)
- [ ] No orphaned MUST rules (specs missing) (5)

#### Completeness (30 points)

**Check**:
- [ ] tech-stack.md complete: languages, frameworks, databases with versions (5)
- [ ] domain-model.md complete: format, location, examples (5)
- [ ] api-contracts.md complete: format, patterns, examples (5)
- [ ] patterns.md has ≥1 pattern with implementation (5)
- [ ] conventions.md has naming, style, structure (5)
- [ ] build-deploy.md has build, test, deploy commands (5)

#### Clarity (20 points)

**Check**:
- [ ] All specs have clear format descriptions (5)
- [ ] Examples are concrete (5)
- [ ] Commands are cross-platform compatible (5)
- [ ] Examples match declared technology and paths (5)

#### Integration (25 points)

**Check**:
- [ ] Each spec references source (ADR ID, DESIGN.md section, file path) (10)
- [ ] All source references are valid and accessible (10)
- [ ] Specs consistent with DESIGN.md (if exists) (5)

**Pass threshold**: ≥80/100

---

## Validation Criteria for This File

**This section validates adapter-structure.md itself against core.md requirements**

### Structure (20 points)

**Check**:
- [ ] Header present: Title, Version, Purpose, Scope (5)
- [ ] Overview section explains philosophy and lifecycle (5)
- [ ] All required sections present (5)
- [ ] References section lists dependencies (5)

### Content (30 points)

**Check**:
- [ ] Language is imperative and agent-centric (10)
- [ ] All placeholders use {descriptive-name} format (5)
- [ ] No TODO/TBD or empty sections (5)
- [ ] Valid and invalid examples provided with ✅/❌ (10)

### Validation Criteria (30 points)

**Check**:
- [ ] Two-phase validation clearly defined (10)
- [ ] All criteria use checkbox format `- [ ]` (5)
- [ ] Point values sum to 100 for each phase (10)
- [ ] Pass thresholds specified (5)

### References (20 points)

**Check**:
- [ ] All references use WHEN clause format (10)
- [ ] No content duplication from referenced files (5)
- [ ] Related files listed at bottom (5)

**Pass threshold**: ≥95/100

### Self-Test Checklist

**Before considering adapter-structure.md complete, verify**:
- [ ] Did I check every validation criterion individually?
- [ ] Are all examples concrete and understandable?
- [ ] Do validation checklists enable agent self-verification?
- [ ] Is scoring arithmetic correct (sums to 100)?
- [ ] Are all WHEN clauses properly formatted?

---

## Examples

### Valid Adapter (Rust + GTS + OpenAPI)

```markdown
# FDD Adapter: Hyperspot

**Extends**: `../../FDD/AGENTS.md`

**Version**: 1.0  
**Status**: COMPLETE  
**Last Updated**: 2025-01-07

---

## Project Identification

**Project Name**: Hyperspot  
**Project Root**: `/project/root`  
**Architecture Root**: `/project/root/architecture`

---

## Technology Stack

### Domain Model

**Technology**: GTS (Global Type System)  
**Location**: `gts/`  
**Format**: TypeScript-like syntax with JSON Schema output

**Type Identifier Format**: `gts.{namespace}.{type}.v{version}`

**Example**:
```
gts.analytics.event.v1
```

### API Contracts

**Technology**: OpenAPI 3.1  
**Location**: `docs/api/`  
**Format**: YAML files per service

**Endpoint Format**: `/{version}/{service}/{resource}`

**Example**:
```
/v1/analytics/events
```

### Testing Framework

**Unit Tests**: cargo test  
**Integration Tests**: cargo test --test '*'  
**E2E Tests**: pytest testing/e2e/

**Test Location**: `tests/`, `testing/e2e/`  
**Test Command**: `make test`  
**Coverage Command**: `make coverage`

### Build Tools

**Build Command**: `cargo build --release`  
**Clean Command**: `cargo clean`  
**Lint Command**: `cargo clippy -- -D warnings`

### Behavior Description Language

**Uses**: FDL  
**Specification**: `../FDL.md`

---

## Project Structure

### Architecture Files

```
architecture/
├── BUSINESS.md
├── DESIGN.md
├── ADR.md
└── features/
    ├── FEATURES.md
    └── feature-{slug}/
        ├── DESIGN.md
        └── CHANGES.md
```

### Source Code

```
src/
├── domain/      # Domain models (from gts/)
├── api/         # API implementations
├── core/        # Core business logic
└── infra/       # Infrastructure
```
```

### Invalid Adapter (Missing Specifications)

```markdown
# FDD Adapter: MyProject

**Extends**: `../../FDD/AGENTS.md`

**Status**: INCOMPLETE

Missing specifications:
- Domain model technology
- API contracts format
- Testing framework
```
❌ Missing required sections, marked as INCOMPLETE

---

## Workflow Integration

**Adapter workflows**:
- `adapter` - Create adapter from scratch or from existing codebase
- `adapter-validate` - Validate adapter against these requirements

**Prerequisites for other workflows**:
- ALL FDD workflows REQUIRE valid adapter (≥90/100)
- Adapter MUST be validated before any other workflow runs
- If adapter INCOMPLETE, must complete before proceeding

**Validation command**:
```
Run workflow: adapter-validate
```
---

## References

**Used by workflows**:
- All FDD workflows (prerequisite check)
- `adapter` - Creates adapter
- `adapter-validate` - Validates adapter

**Related requirements**:
- `../AGENTS.md` - Core FDD requirements
- `workflow-requirements.md` - Workflow structure requirements
