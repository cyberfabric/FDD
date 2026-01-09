# FDD Adapter Creation Guide

## Core Principle

Adapters extend FDD with project-specific context. Start files with `Extends: ../FDD/path/to/file.md`.

**You can override/add anything EXCEPT the immutable rules below.**

---

## Immutable Rules (NEVER Override)

These are validated by tooling and cannot be changed:

### 1. Design Hierarchy
```
ADAPTER → BUSINESS CONTEXT → OVERALL DESIGN → FEATURE DESIGN → CHANGES → CODE
```
Must reference parent level, never contradict.

- **ADAPTER**: Defines tech stack, formats, conventions (first step, required)
- **BUSINESS CONTEXT**: Defines actors, capabilities, business requirements
- **OVERALL DESIGN**: Architecture, domain model, API contracts
- **FEATURE DESIGN**: Actor flows, algorithms, requirements
- **CHANGES**: Atomic implementation plan with tasks
- **CODE**: Implementation following CHANGES

### 2. Mandatory FDD Rules
- Actor Flows (Section B) are PRIMARY - always start from what actors do
- Use FDL for flows/algorithms/states - NEVER code in DESIGN.md
- Never redefine types - reference domain model from Overall Design
- Validate before proceeding (Overall ≥90/100, Feature 100/100)
- Feature size limits: ≤3000 lines (recommended), ≤4000 (hard limit)
- Implementation changes are atomic - one change = one deployable unit
- Design is source of truth - if code contradicts design, fix design first

### 3. File Structure
```
architecture/
├── DESIGN.md                    # Overall Design
└── features/
    ├── FEATURES.md              # Feature manifest
    └── feature-{slug}/
        ├── DESIGN.md            # Feature Design
        └── CHANGES.md           # Implementation plan
```

### 4. DESIGN.md Sections
**Overall Design**:
- Section A: Business Context
- Section B: Requirements & Principles
- Section C: Technical Architecture
- Section D: Architecture Decision Records (ADR) - REQUIRED, MADR format
- Section E: Project-Specific Details (optional)

**Feature Design**:
- Section A: Feature Overview
- Section B: Actor Flows (PRIMARY)
- Section C: Algorithms
- Section D: States (optional)
- Section E: Technical Details
- Section F: Requirements (formalized scope + Testing Scenarios in FDL)
- Section G: Implementation Plan (implementation changes with status)

### 5. Validation Scores
- Overall Design: ≥90/100
- Feature Design: 100/100 + 100% completeness

---

## What Adapters Define

Everything else is adapter-specific. Define as needed:

**Note**: All FDD operation workflows now support **CREATE and UPDATE modes**. Adapters can be created once and updated anytime as project evolves. Use `adapter.md` workflow to create or update your adapter.

### Domain Model Format
- Technology (TypeScript, JSON Schema, Protobuf, GTS, etc.)
- Location (`architecture/domain-model/`, per-feature, etc.)
- DML syntax (`@DomainModel.TypeName` for clickable references)
- Validation commands
- Naming conventions
- Traceability requirements (clickable links from Feature→Overall)

### API Contract Format
- Technology (OpenAPI, GraphQL, gRPC, CLISPEC, etc.)
- Location (`architecture/api-specs/`, `architecture/cli-specs/`, etc.)
- Linking syntax (`@API.GET:/path`, `@CLI.command-name`, `@Feature.{slug}` for clickable references)
- Validation commands
- API conventions
- Traceability requirements (clickable links from Feature→Overall)

**Note**: For CLI tools, consider using **CLISPEC** - a built-in, simple format for CLI command documentation. See `CLISPEC.md` for specification.

### Implementation Details
- Database technology and patterns
- Authentication/authorization approach
- Error handling patterns
- Testing strategy (frameworks, locations)
- Build/deployment commands
- Code style and linting rules
- Validation output format (MUST be chat output only, NO report files)

### Behavior Description Language (Optional Override)
- **Default**: FDL (Flow Description Language) for flows/algorithms/states
- **Can override**: Create custom behavior specification in `{adapter-directory}/FDD-Adapter/`
- **Example**: Replace `../FDL.md` with `../FDD-Adapter/CustomBDL.md`
- **Requirements**: Define control flow keywords, syntax rules, validation criteria
- **Note**: Must update workflows 05 and 06 to reference custom spec

### Additional Artifacts
- Diagrams location and format
- Documentation structure
- CI/CD configuration
- Any project-specific tooling

---

## Adapter Structure

```bash
{adapter-directory}/             # Configurable: spec/, guidelines/, docs/
├── FDD/                         # Core (immutable rules)
└── FDD-Adapter/                 # Your project-specific extensions
    ├── AGENTS.md                # Navigation rules (WHEN executing workflows: ...)
    └── specs/                   # Detailed specifications
        ├── domain-model.md      # Domain model format and location
        ├── api-contracts.md     # API contract format and location
        ├── testing.md           # Testing frameworks and commands
        ├── build-deploy.md      # Build and deployment commands
        ├── project-structure.md # Directory structure
        └── conventions.md       # Coding standards and patterns
```

**Note**: `{adapter-directory}` is configured by project owner (commonly `spec/`, `guidelines/`, or `docs/`)

---

## Template: AGENTS.md

```markdown
# FDD Adapter: {Project Name}

**Extends**: `../../FDD/AGENTS.md`

**Version**: 1.0  
**Status**: COMPLETE  
**Last Updated**: YYYY-MM-DD

---

ALWAYS open and follow `specs/domain-model.md` WHEN executing workflows: design.md, design-validate.md, adr.md, adr-validate.md, features.md, features-validate.md, feature.md, feature-validate.md, feature-changes.md, feature-changes-validate.md, feature-change-implement.md, feature-change-validate.md

ALWAYS open and follow `specs/api-contracts.md` WHEN executing workflows: design.md, design-validate.md, adr.md, adr-validate.md, feature.md, feature-validate.md, feature-changes.md, feature-changes-validate.md, feature-change-implement.md, feature-change-validate.md

ALWAYS open and follow `specs/testing.md` WHEN executing workflows: feature-change-implement.md, feature-change-validate.md, feature-qa.md

ALWAYS open and follow `specs/build-deploy.md` WHEN executing workflows: feature-change-implement.md, feature-change-validate.md, feature-qa.md

ALWAYS open and follow `specs/project-structure.md` WHEN executing workflows: adapter.md, adapter-auto.md, adapter-manual.md, adapter-bootstrap.md, adapter-agents.md, adapter-validate.md, business-context.md, business-validate.md, design.md, design-validate.md, adr.md, adr-validate.md, features.md, features-validate.md, feature.md, feature-validate.md, feature-changes.md, feature-changes-validate.md

ALWAYS open and follow `specs/conventions.md` WHEN executing workflows: adapter.md, adapter-auto.md, adapter-manual.md, adapter-bootstrap.md, adapter-validate.md, feature-change-implement.md, feature-change-validate.md
```

**Example spec file** (`specs/domain-model.md`):
```markdown
# Domain Model Specification

**Technology**: TypeScript  
**Location**: `architecture/domain-model/types.ts`  
**Format**: TypeScript interfaces and types

## Type Identifier Syntax

Use `@DomainModel.TypeName` for clickable references in DESIGN.md files.

**Example**:
```typescript
export interface User {
  id: string;
  name: string;
}
```

Reference as: `@DomainModel.User`

## Validation

**Command**: `tsc --noEmit`  
**Expected**: No type errors

## Traceability

All Feature DESIGN.md files MUST use clickable links to domain model types.
```

---
