# AI Agent Instructions for FDD

**READ THIS FIRST**: This document defines FDD core methodology for AI agents. For implementation details and step-by-step procedures, see `workflows/` directory.

---

## ⚠️ PREREQUISITE: FDD ADAPTER REQUIRED

**FDD CANNOT WORK WITHOUT A PROJECT-SPECIFIC ADAPTER**

Before doing ANY FDD work, you **MUST** verify that a project adapter exists:

**Check for adapter**:
1. Look for `{adapter-directory}/FDD-Adapter/AGENTS.md` that extends `../FDD/AGENTS.md`
2. Common locations:
   - `spec/FDD-Adapter/AGENTS.md`
   - `guidelines/FDD-Adapter/AGENTS.md`
   - `docs/FDD-Adapter/AGENTS.md`

**If adapter NOT found**:
```
❌ STOP: FDD adapter not found.

FDD requires a project-specific adapter before any work can begin.

Would you like to create an adapter now? (recommended)
→ Run Workflow: adapter-config (workflows/adapter-config.md)

This will guide you through:
- Domain model technology selection
- API contract format
- Testing and build tools
- Project-specific conventions
```

**If adapter found but INCOMPLETE**:
```
⚠️ WARNING: Adapter is marked as INCOMPLETE.

Missing specifications:
{List from adapter AGENTS.md}

ALL workflows are BLOCKED.

Please complete the adapter by adding missing specifications.
```

**Only proceed with FDD workflows if**:
- ✅ Adapter exists
- ✅ Adapter extends FDD AGENTS.md
- ✅ Adapter status is COMPLETE (or user acknowledges INCOMPLETE status)

---

## How Extends Works

**When file has `**Extends**: base-file.md`**: Load base file first, then apply modifications from current file. Merge = base instructions + modifications. Never skip base, never replace base rules.

---

## CRITICAL RULES - NEVER VIOLATE

**Design Hierarchy** (strict order, no violations):
```
OVERALL DESIGN (architecture + domain model + API contracts)
    ↓ must reference, never contradict
FEATURE DESIGN (actor flows + algorithms in FDL + implementation plan)
    ↓ must reference, never contradict
OpenSpec CHANGES (atomic implementation specs)
    ↓ must implement exactly
CODE (implementation)
```

**Mandatory Rules**:
1. ✅ **Actor Flows are PRIMARY** - Section B drives everything, document all flows first
2. ✅ **Use FDL for flows/algorithms/states** - NEVER write code in DESIGN.md, only plain English FDL
3. ✅ **FDL.md is the specification** - ALL content in `architecture/` that describes flows, algorithms, scenarios, or states MUST follow FDL syntax as defined in `FDL.md`. This includes:
   - Section B (Actor Flows) in all DESIGN.md files
   - Section C (Algorithms) in all DESIGN.md files
   - Section D (States) in all DESIGN.md files
   - Section G (Testing Scenarios) in Feature DESIGN.md files
   - Any other behavioral descriptions
   - **You MUST read `FDL.md` before generating or validating any FDL content**
   - **Note**: Project adapters can override FDL with a custom behavior description language by providing alternative specification in `{adapter-directory}/FDD-Adapter/` (see Adapters section below)
4. ✅ **Never redefine types** - Reference domain model from Overall Design, never duplicate
5. ✅ **Validate before proceeding** - Overall Design must score ≥90/100, Feature Design must score 100/100 + 100%
6. ✅ **Feature size limits** - ≤3000 lines recommended, ≤4000 hard limit
7. ✅ **OpenSpec changes are atomic** - One change = one deployable unit
8. ✅ **Design is source of truth** - If code contradicts design, fix design first, then re-validate

**If Contradiction Found**:
1. **STOP implementation immediately**
2. Identify which level has the issue (Overall/Feature/Change/Code)
3. Fix design at that level → Use `workflows/08-fix-design.md`
4. Re-validate affected levels → Use `workflows/02-validate-architecture.md` or `workflows/06-validate-feature.md`
5. Update dependent levels
6. Resume only after validation passes


## 🤖 AI AGENT INTERACTIVE MODE

**CRITICAL**: When a workflow or document references another specification file (e.g., "see `../FDL.md`", "reference Overall Design"), you MUST read that file BEFORE proceeding. Specifications are the source of truth, not the workflow descriptions.

**Workflows use dialog mode**: AI proposes answers based on context, user reviews/approves.

**Interactive Questions**:
1. Analyze user's prompt - extract intent and context
2. Propose specific answers (not open-ended questions)
3. Present for review - user approves/modifies/rejects
4. Iterate in dialog until approved

**Domain Model & API Specs - CRITICAL**:
- Must ensure COMPLETE specifications for validation
- All types/schemas/objects defined in machine-readable format (GTS, JSON Schema, OpenAPI, etc.)
- Never accept vague specs ("use JSON" ❌) - require specific paths and formats

**Auto-Validation After Workflow** (MANDATORY):
- Workflows with validation: 01→02, 03→04, 05→06, 09→12
- After workflow completes, automatically run validation
- If passes: suggest next workflow
- If fails: propose fixes, iterate until passes

**Validation Output** (CRITICAL):
- ❌ **DO NOT create validation report files** (e.g., `VALIDATION_REPORT.md`, `FEATURE_VALIDATION_REPORT.md`, `OPENSPEC_VALIDATION_REPORT.md`)
- ✅ **Output all validation results directly in chat** with comprehensive information
- ✅ Include: scores, findings, issues, recommendations, next steps
- ✅ Format clearly using markdown (sections, tables, lists, code blocks)
- **Rationale**: Report files clutter workspace and get deleted; chat output is immediately visible and actionable

**Suggest Next Workflow** (MANDATORY):
- After every workflow + validation, suggest next logical step
- Progression paths: New Project (01→02→03→04→05), New Feature (05→06→09→10→11→07), Fix (08→02/06)

**Rules**:
- ✅ Propose answers (not just ask), show reasoning, batch questions, track context
- ❌ Never accept incomplete specs, skip validation, or leave user unsure what's next

---

## OpenSpec Integration (REQUIRED)

**CRITICAL**: Before using any OpenSpec commands (workflows 09-13), **you MUST read the full OpenSpec specification** at `spec/FDD/openspec/AGENTS.md`

### Core Principles

**What is OpenSpec**:
- Atomic change management system for feature implementation
- Single project-level OpenSpec at `openspec/` (project root)
- Changes tracked in `openspec/changes/`, merged to `openspec/specs/`

**Key Rules**:
1. **Run from project root** - All `openspec` commands run from project root directory
2. **Use non-interactive mode** - Use explicit item names or `--all --no-interactive` / `-y` flags
3. **Changes are atomic** - One change = one deployable unit (implements 1-5 requirements)
4. **Manual creation** - Create directory structure manually (no `openspec init` command)

**Feature Design Integration**:
- **Section G**: Requirements (formalized scope)
- **Section H**: Implementation Plan (changes with status)
- Workflows 09-13 are OpenSpec workflows
- Use after Feature Design validated (workflow 06)

**Resources**:
- **Full Specification**: `spec/FDD/openspec/AGENTS.md` ⚠️ **READ BEFORE USE**
- **Website**: https://openspec.dev
- **Install**: `npm install -g @fission-ai/openspec@latest`

---

## Design Levels

**OVERALL DESIGN** (`architecture/DESIGN.md`, ≤5000 lines, ≥90/100):
- Section A: Business Context, Section B: Requirements & Principles, Section C: Technical Architecture
- Defines: architecture, domain model, API contracts, actors
- Workflows: 01-init-project, 02-validate-architecture

**FEATURE DESIGN** (`architecture/features/feature-{slug}/DESIGN.md`, ≤4000 lines, 100/100):
- Section A: Overview (purpose, actors, references)
- Section B: Actor Flows (in FDL)
- Section C: Algorithms (in FDL)
- Section D: States (in FDL, state machines if needed)
- Section E: Technical Details (DB, API, security)
- **Section F: Requirements** (formalized scope, references B-E via markdown anchors, includes Testing Scenarios in FDL)
- **Section G: Implementation Plan** (OpenSpec changes implementing requirements, with status)
- Uses FDL for flows/algorithms/states, references Overall Design types
- Workflows: 05-init-feature, 06-validate-feature, 08-fix-design

**OpenSpec CHANGES** (`openspec/changes/{change-name}/`):
- Files: proposal.md, tasks.md, specs/{feature-slug}/spec.md, design.md (optional)
- Atomic units implementing 1-5 requirements
- Workflows: 09-openspec-init, 10-implement, 11-complete, 12-next, 13-validate

**FEATURES.md** (`architecture/features/FEATURES.md`):
- Status: ⏳ NOT_STARTED, 🔄 IN_PROGRESS, ✅ IMPLEMENTED
- Workflows: 03-init-features, 04-validate-features

**Adapters** (`{adapter-directory}/FDD-Adapter/`):
- **Define**: domain model format, API contracts, implementation details, **behavior specification language**
- **Can override**: FDL specification by providing alternative behavior description language (e.g., replace `../FDL.md` with `../FDD-Adapter/CustomBDL.md`)
- **Cannot override**: design hierarchy, mandatory rules, file structure, validation scores
- **How to override FDL**: 
  1. Create custom behavior specification in `{adapter-directory}/FDD-Adapter/` (e.g., `CustomBDL.md`)
  2. Update workflows 05 and 06 to reference custom spec instead of `../FDL.md`
  3. Update AGENTS.md Rule #3 to reference custom spec
  4. Ensure custom spec defines: control flow keywords, syntax rules, validation criteria
- **See**: `ADAPTER_GUIDE.md` for complete adapter creation guide
- **Note**: `{adapter-directory}` is configured by project owner (spec/, guidelines/, docs/, etc.)

---

## Quick Reference

**Starting FDD Work**:
1. Check for FDD Adapter (REQUIRED) → Look for `{adapter-dir}/AGENTS.md`
2. Read `workflows/AGENTS.md` for workflow selection
3. Read `FDL.md` for syntax

**Key Files**: `architecture/DESIGN.md`, `architecture/features/FEATURES.md`, `architecture/features/feature-{slug}/DESIGN.md`, `openspec/`

**Remember**: Requirements PRIMARY (B), FDL for flows/algorithms, reference types (never redefine), validate before proceeding