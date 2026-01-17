<!-- @fdd-change:fdd-fdd-feature-core-methodology-change-agents-navigation:ph-1 -->
<!-- fdd-begin fdd-fdd-feature-core-methodology-algo-resolve-workflow:ph-1:inst-parse-request -->
# Workflow Selection Guide

**Version**: 2.1  
**Purpose**: Select appropriate FDD workflow based on project state  
**Scope**: All FDD workflow selection decisions
<!-- fdd-end   fdd-fdd-feature-core-methodology-algo-resolve-workflow:ph-1:inst-parse-request -->

---

**ALWAYS open and follow**: `core.md` WHEN editing this file

## Overview

This guide helps you select the correct FDD workflow based on:
- Current project state
- Artifacts that exist or need creation
- Phase of development

**All workflows located in**: `/FDD/workflows/`

---

## ⚠️ FIRST STEP: Check for FDD Adapter

**BEFORE selecting any workflow**:

1. Check if `FDD-Adapter/AGENTS.md` exists at project root level
2. Check these locations (in order):
   - `{project-root}/FDD-Adapter/AGENTS.md` (recommended)
   - `{project-root}/guidelines/FDD-Adapter/AGENTS.md`
   - `{project-root}/spec/FDD-Adapter/AGENTS.md`
   - `{project-root}/docs/FDD-Adapter/AGENTS.md`

**Important**: Adapter MUST be at project root level, NOT deeply nested in subdirectories

**If NO adapter** → Start with `adapter.md` workflow

**If adapter exists** → Continue to workflow selection below

---

## Available Workflows

<!-- fdd-begin fdd-fdd-feature-core-methodology-algo-resolve-workflow:ph-1:inst-check-adapter -->
### Phase 0: Adapter Setup

**adapter.md** - Create or update FDD adapter
- **Use when**: No adapter exists OR need to update adapter
- **Creates**: `{project-root}/FDD-Adapter/AGENTS.md` + spec files
- **Location**: Project root level (not nested in subdirectories)
- **Modes**: CREATE or UPDATE
- **Next**: `business-context` or `adapter-validate`

**adapter-from-sources.md** - Extract adapter from existing codebase
- **Use when**: Legacy project, want to reverse-engineer adapter
- **Analyzes**: Existing code to propose formats
- **Next**: `adapter-validate`

**adapter-agents.md** - Generate AI agent config from adapter
- **Use when**: Want IDE-specific AI configuration
- **Creates**: `.windsurf/`, `.cursorrules`, etc.
- **Next**: Any architecture workflow

**adapter-validate.md** - Validate adapter structure
- **Use when**: Adapter created or updated
- **Validates**: File structure, AGENTS.md format, spec files
- **Next**: `business-context` or `design`
<!-- fdd-end   fdd-fdd-feature-core-methodology-algo-resolve-workflow:ph-1:inst-check-adapter -->

---

### Phase 1: Business & Architecture

<!-- fdd-begin fdd-fdd-feature-core-methodology-algo-resolve-workflow:ph-1:inst-check-business -->
 
## Phase 1: Business & Architecture

### Workflow: `business-context`
 
**business-context.md** - Create or update BUSINESS.md
- **Use when**: Need to document business context
- **Creates**: `architecture/BUSINESS.md`
- **Sections**: Vision, Actors, Capabilities
- **Modes**: CREATE or UPDATE
- **Next**: `business-validate`
 
### Workflow: `business-validate`
 
**business-validate.md** - Validate business
 
**When**: After BUSINESS.md created or updated
- **Validates**: Required sections, actor/capability IDs
- **Score**: ≥90/100
- **Next**: `design`
 
<!-- fdd-end   fdd-fdd-feature-core-methodology-algo-resolve-workflow:ph-1:inst-check-business -->

**design.md** - Create or update overall design
- **Use when**: Need architecture/system design
- **Creates**: `architecture/DESIGN.md`
- **Sections**: Architecture, Requirements, Technical Details
- **Modes**: CREATE or UPDATE
- **Next**: `design-validate`

**design-validate.md** - Validate overall design
- **Use when**: DESIGN.md created or updated
- **Validates**: Sections, domain model, API contracts, diagrams
- **Score**: 100/100 + 100% completeness
- **Next**: `adr` (optional) or `features`

**adr.md** - Create or update Architecture Decision Records
- **Use when**: Need to document architectural decisions
- **Creates**: `architecture/ADR.md`
- **Format**: MADR with FDD extensions
- **Modes**: CREATE (new ADR) or UPDATE (edit ADR)
- **Next**: `adr-validate`

**adr-validate.md** - Validate ADRs
- **Use when**: ADR.md created or updated
- **Validates**: MADR format, numbering, related design elements
- **Score**: ≥90/100
- **Next**: `features` or continue design work

---

### Phase 2: Feature Planning

<!-- fdd-begin fdd-fdd-feature-core-methodology-algo-resolve-workflow:ph-1:inst-check-feature -->
 
## Phase 2: Feature Planning
 
### Workflow: `features`
 
**features.md** - Create or update features manifest
- **Use when**: Need to plan/list features
- **Creates**: `architecture/FEATURES.md`
- **Modes**: CREATE (from DESIGN.md) or UPDATE (manual)
- **Next**: `features-validate`
 
<!-- fdd-end   fdd-fdd-feature-core-methodology-algo-resolve-workflow:ph-1:inst-check-feature -->

**features-validate.md** - Validate features manifest
- **Use when**: FEATURES.md created or updated
- **Validates**: Manifest structure, feature list completeness
- **Score**: ≥90/100
- **Next**: `feature` (for each feature)

**feature.md** - Create or update feature design
- **Use when**: Need to design single feature
- **Creates**: `architecture/features/feature-{slug}/DESIGN.md`
- **Sections**: A-F (Overview, Actors, Algorithms, Data, API, Requirements)
- **Modes**: CREATE or UPDATE
- **Next**: `feature-validate`

**feature-validate.md** - Validate feature design
- **Use when**: Feature DESIGN.md created or updated
- **Validates**: All sections, actor flows, FDL, no type redefinitions
- **Score**: 100/100 + 100% completeness
- **Next**: `feature-changes`

---

### Phase 3: Implementation

**feature-changes.md** - Create or update implementation plan
- **Use when**: Feature validated, need implementation plan
- **Creates**: `architecture/features/feature-{slug}/CHANGES.md`
- **Content**: Atomic changes (1-5 requirements each), task breakdown
- **Modes**: CREATE or UPDATE
- **Next**: `feature-changes-validate`

**feature-changes-validate.md** - Validate implementation plan
- **Use when**: CHANGES.md created or updated
- **Validates**: Structure, requirements mapping, tasks
- **Score**: ≥90/100
- **Next**: `feature-change-implement`

**feature-change-implement.md** - Implement specific change
- **Use when**: Ready to code a change from CHANGES.md
- **Implements**: Tasks for one change, updates checkboxes
- **Updates**: Change status (⏳ → 🔄 → ✅)
- **Next**: `feature-code-validate`

**feature-code-validate.md** - Validate feature code
- **Use when**: At least one change is IN_PROGRESS
- **Validates**: Code compiles, tests pass, requirements and test scenarios implemented
- **Next**: Update FEATURES.md: Mark feature status as COMPLETE

---

## Decision Tree

```
START
│
├─ No adapter?
│  └─> adapter.md (or adapter-from-sources.md for legacy)
│
├─ Adapter exists, no BUSINESS.md?
│  └─> business-context.md → business-validate.md
│
├─ BUSINESS.md exists, no DESIGN.md?
│  └─> design.md → design-validate.md
│
├─ Need to document decisions?
│  └─> adr.md → adr-validate.md
│
├─ DESIGN.md validated, no FEATURES.md?
│  └─> features.md → features-validate.md
│
├─ FEATURES.md exists, need feature design?
│  └─> feature.md → feature-validate.md
│
├─ Feature validated, no CHANGES.md?
│  └─> feature-changes.md → feature-changes-validate.md
│
├─ CHANGES.md validated, ready to code?
│  └─> feature-change-implement.md (repeat for each change)
│
├─ All changes done, validate code?
│  └─> feature-code-validate.md
│
├─ Need to update existing doc?
│  └─> Use same workflow in UPDATE mode
│
└─ Need to validate feature or design?
   └─> feature-validate.md or design-validate.md
```

---

## Common Sequences

### New project from scratch
```
adapter → adapter-validate
  ↓
business-context → business-validate
  ↓
design → design-validate
  ↓
[optional: adr → adr-validate]
  ↓
features → features-validate
  ↓
feature → feature-validate (for each feature)
  ↓
feature-changes → feature-changes-validate
  ↓
 feature-change-implement (for each change)
   ↓
 feature-code-validate
```

### Legacy project integration
```
adapter-from-sources → adapter-validate
  ↓
[reverse-engineer existing docs or create new]
  ↓
design → design-validate
  ↓
[continue as new project]
```

### Add feature to existing project
```
[adapter + design already exist]
  ↓
features → features-validate (update manifest)
  ↓
feature → feature-validate
  ↓
feature-changes → feature-changes-validate
  ↓
 feature-change-implement (repeat)
   ↓
 feature-code-validate
```

### Update existing design
```
design (UPDATE mode) → design-validate
  ↓
[if impacts features: update feature designs]
  ↓
feature (UPDATE mode) → feature-validate
```

---

## Critical Rules

**Before executing any workflow**:
1. Read the workflow `.md` file completely
2. Check prerequisites in workflow file
3. Read `requirements/{requirement}.md` files referenced in workflow
4. Read adapter AGENTS.md if workflow requires it

**During execution**:
- Follow steps in sequence
- Validate after creation/update
- One workflow at a time
- Run from project root

**Validation**:
- Always run validation workflow after creation/update
- Meet score thresholds before proceeding
- Re-validate after fixes

**Modes**:
- Most workflows support CREATE or UPDATE modes
- CREATE: Generate new file from scratch
- UPDATE: Modify existing file

---

## Workflow Categories

### By Artifact

**Adapter**:
- adapter.md, adapter-from-sources.md, adapter-agents.md, adapter-validate.md

**Business Context**:
- business-context.md, business-validate.md

**Architecture Design**:
- design.md, design-validate.md, adr.md, adr-validate.md

**Features**:
- features.md, features-validate.md, feature.md, feature-validate.md

**Implementation**:
- feature-changes.md, feature-changes-validate.md
- feature-change-implement.md, feature-code-validate.md

### By Type

**Creation/Update** (Operation workflows):
- adapter.md, business-context.md, design.md, adr.md
- features.md, feature.md, feature-changes.md
- feature-change-implement.md

**Validation** (Check workflows):
- adapter-validate.md, business-validate.md, design-validate.md
- adr-validate.md, features-validate.md, feature-validate.md
- feature-changes-validate.md, feature-code-validate.md

**Special Purpose**:
- adapter-from-sources.md (legacy integration)
- adapter-agents.md (IDE configuration)
- feature-code-validate.md (feature completion validation)

---

## Quick Reference

### "I want to..."

**Set up FDD for my project**
→ `adapter.md` (or `adapter-from-sources.md` for legacy code)

**Document business context**
→ `business-context.md` → `business-validate.md`

**Design system architecture**
→ `design.md` → `design-validate.md`

**Record architectural decisions**
→ `adr.md` → `adr-validate.md`

**Plan features**
→ `features.md` → `features-validate.md`

**Design a feature**
→ `feature.md` → `feature-validate.md`

**Plan feature implementation**
→ `feature-changes.md` → `feature-changes-validate.md`

**Implement a change**
→ `feature-change-implement.md` (repeat for each change)

**Validate feature code**
→ `feature-code-validate.md`

**Update existing document**
→ Use same workflow in UPDATE mode

**Generate IDE config**
→ `adapter-agents.md`

---

## References

**This file is used by**:
- `workflows/AGENTS.md` - Directs to this guide for workflow selection
- AI agents - To select appropriate workflow

**This file references**:
- `workflow-execution.md` - How to execute selected workflow
- `core-workflows.md` - Workflow file format specification
- All requirement files in `requirements/` - Referenced by workflows

**All workflows located in**: `/FDD/workflows/`

<!-- fdd-begin fdd-fdd-feature-core-methodology-algo-resolve-workflow:ph-1:inst-extract-keywords -->
<!-- fdd-begin fdd-fdd-feature-core-methodology-algo-resolve-workflow:ph-1:inst-init-candidates -->
<!-- fdd-begin fdd-fdd-feature-core-methodology-algo-resolve-workflow:ph-1:inst-return-adapter -->
<!-- fdd-begin fdd-fdd-feature-core-methodology-algo-resolve-workflow:ph-1:inst-return-business -->
<!-- fdd-begin fdd-fdd-feature-core-methodology-algo-resolve-workflow:ph-1:inst-return-design -->
<!-- fdd-begin fdd-fdd-feature-core-methodology-algo-resolve-workflow:ph-1:inst-return-feature -->
<!-- fdd-begin fdd-fdd-feature-core-methodology-algo-resolve-workflow:ph-1:inst-check-validate -->
<!-- fdd-begin fdd-fdd-feature-core-methodology-algo-resolve-workflow:ph-1:inst-extract-artifact-type -->
<!-- fdd-begin fdd-fdd-feature-core-methodology-algo-resolve-workflow:ph-1:inst-return-validate -->
<!-- fdd-begin fdd-fdd-feature-core-methodology-algo-resolve-workflow:ph-1:inst-check-changes -->
<!-- fdd-begin fdd-fdd-feature-core-methodology-algo-resolve-workflow:ph-1:inst-return-changes -->
<!-- fdd-begin fdd-fdd-feature-core-methodology-algo-resolve-workflow:ph-1:inst-check-implement -->
<!-- fdd-begin fdd-fdd-feature-core-methodology-algo-resolve-workflow:ph-1:inst-return-implement -->
## Workflow Resolution Algorithm

Algorithm for resolving user request to workflow file path is implemented throughout this document via keyword matching and routing logic.

Key steps:
- Extract keywords from request
- Initialize workflow candidates
- Return appropriate workflow based on request type (adapter, business, design, feature, validate, changes, implement)
<!-- fdd-end   fdd-fdd-feature-core-methodology-algo-resolve-workflow:ph-1:inst-return-implement -->
<!-- fdd-end   fdd-fdd-feature-core-methodology-algo-resolve-workflow:ph-1:inst-check-implement -->
<!-- fdd-end   fdd-fdd-feature-core-methodology-algo-resolve-workflow:ph-1:inst-return-changes -->
<!-- fdd-end   fdd-fdd-feature-core-methodology-algo-resolve-workflow:ph-1:inst-check-changes -->
<!-- fdd-end   fdd-fdd-feature-core-methodology-algo-resolve-workflow:ph-1:inst-return-validate -->
<!-- fdd-end   fdd-fdd-feature-core-methodology-algo-resolve-workflow:ph-1:inst-extract-artifact-type -->
<!-- fdd-end   fdd-fdd-feature-core-methodology-algo-resolve-workflow:ph-1:inst-check-validate -->
<!-- fdd-end   fdd-fdd-feature-core-methodology-algo-resolve-workflow:ph-1:inst-return-feature -->
<!-- fdd-end   fdd-fdd-feature-core-methodology-algo-resolve-workflow:ph-1:inst-return-design -->
<!-- fdd-end   fdd-fdd-feature-core-methodology-algo-resolve-workflow:ph-1:inst-return-business -->
<!-- fdd-end   fdd-fdd-feature-core-methodology-algo-resolve-workflow:ph-1:inst-return-adapter -->
<!-- fdd-end   fdd-fdd-feature-core-methodology-algo-resolve-workflow:ph-1:inst-init-candidates -->
<!-- fdd-end   fdd-fdd-feature-core-methodology-algo-resolve-workflow:ph-1:inst-extract-keywords -->
