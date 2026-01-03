# AI Agent Instructions for FDD Workflows

Instructions for AI assistants on when and which FDD workflow to use.

---

## ⚠️ FIRST STEP: Check for FDD Adapter

**BEFORE selecting any workflow, verify adapter exists**:

1. Look for `{adapter-directory}/AGENTS.md` that extends `../FDD/AGENTS.md`
2. Common locations:
   - `spec/{project-name}-adapter/AGENTS.md`
   - `guidelines/{project-name}-adapter/AGENTS.md`
   - `docs/{project-name}-adapter/AGENTS.md`

**If adapter NOT found** → Use **Workflow: adapter-config**

**If adapter found** → Continue with appropriate workflow below

---

## Workflow Selection Guide

Always read the specific workflow file before executing. This guide helps you choose which workflow to use.

---

## Phase 0: Pre-Project Setup

### When: No FDD adapter exists (REQUIRED FIRST)

**adapter-config.md** - Create FDD adapter through guided questions
- **Use when**: Starting FDD on a new project without existing adapter
- **Creates**: Project-specific adapter in `spec/FDD-Adapter/`
- **Approach**: Interactive questions, minimal output, no unnecessary content
- **Next step**: Configure agent tools (optional) or initialize project (workflow 01)

**config-agent-tools.md** - Configure AI agent for FDD (optional)
- **Use when**: After creating adapter, want to set up agent to use FDD natively
- **Creates**: Agent-specific config files (`.windsurf/`, `.cursorrules`, `.clinerules`, `.aider.conf.yml`)
- **Configures**: Rules file + workflow references (format follows agent specification)
- **Goal**: Agent reads adapter AGENTS.md automatically and uses FDD workflows
- **Next step**: Initialize project (workflow 01)

---

## Phase 1: Architecture Design

### When: Starting new FDD project or module

**01-init-project.md** - Initialize FDD structure
- **Use when**: No `architecture/` directory exists
- **Creates**: Directory structure, DESIGN.md template, feature folders
- **Next step**: User creates Overall Design content

**02-validate-architecture.md** - Validate Overall Design
- **Use when**: `architecture/DESIGN.md` is complete
- **Validates**: Vision, actors, domain model, API contracts, diagrams
- **Required score**: 100/100 + 100% completeness
- **Next step**: Feature planning (workflow 03 or 04)

---

## Phase 2: Feature Planning

### When: Overall Design validated, need to plan features

**03-init-features.md** - Generate features from Overall Design
- **Use when**: Need to extract features from Overall Design automatically
- **Creates**: `FEATURES.md` manifest, feature directories
- **Analyzes**: Overall Design to identify feature list
- **Next step**: Create DESIGN.md for each feature

**04-validate-features.md** - Validate FEATURES.md manifest
- **Use when**: `FEATURES.md` exists and need consistency check
- **Validates**: Manifest completeness, feature list consistency
- **Next step**: Initialize or validate individual features

**05-init-feature.md** - Initialize single feature
- **Use when**: Creating one feature manually (not via 03)
- **Creates**: Feature directory, DESIGN.md template, openspec structure
- **Next step**: User creates Feature Design content

**06-validate-feature.md** - Validate Feature Design
- **Use when**: `architecture/features/feature-{slug}/DESIGN.md` is complete
- **Validates**: Sections A-F, Actor Flows, FDL algorithms, no type redefinitions
- **Required score**: 100/100 + 100% completeness
- **Next step**: OpenSpec initialization (workflow 09)

---

## Phase 3: Feature Implementation

### When: Feature Design validated, ready to implement

**09-openspec-init.md** - Initialize OpenSpec for feature
- **Use when**: Feature Design validated, ready to start implementation
- **Creates**: `openspec/` structure, first change (001-*)
- **Next step**: Implement first OpenSpec change (workflow 10)

**10-openspec-change-implement.md** - Implement OpenSpec change
- **Use when**: Active change exists in `openspec/changes/{change-name}/`
- **Implements**: Code according to proposal.md and tasks.md
- **Validates**: Tasks checklist completion
- **Next step**: Complete change (workflow 11) or continue implementation

**11-openspec-change-complete.md** - Complete OpenSpec change
- **Use when**: Change implementation finished and tested
- **Merges**: Change specs to `openspec/specs/`
- **Archives**: Change to `changes/archive/`
- **Next step**: Create next change (workflow 12) or validate all (workflow 13)

**12-openspec-change-next.md** - Create next OpenSpec change
- **Use when**: Current change complete, more changes planned in DESIGN.md
- **Creates**: Next change directory and files from Feature DESIGN.md Section F
- **Next step**: Implement next change (workflow 10)

**13-openspec-validate.md** - Validate OpenSpec structure
- **Use when**: Need to verify OpenSpec consistency
- **Validates**: Structure, specs, changes consistency
- **Next step**: Complete feature (workflow 07) if all changes done

**07-complete-feature.md** - Complete feature
- **Use when**: All OpenSpec changes implemented and tested
- **Validates**: Compilation, tests pass, no pending changes
- **Marks**: Feature as complete in `FEATURES.md`
- **Next step**: Next feature or project complete

**08-fix-design.md** - Fix design issues
- **Use when**: Implementation reveals design problem
- **Updates**: DESIGN.md with corrections
- **Re-validates**: Feature Design after fix
- **Next step**: Continue implementation with corrected design

---

## Decision Tree

```
Start FDD work
│
├─ No FDD adapter exists?
│  └─> Use workflow adapter-config
│
├─ No architecture/ directory?
│  └─> Use workflow 01 (init-project)
│
├─ architecture/DESIGN.md complete?
│  └─> Use workflow 02 (validate-architecture)
│
├─ Need to plan features?
│  ├─ Extract from Overall Design? → Use workflow 03 (init-features)
│  ├─ Validate FEATURES.md? → Use workflow 04 (validate-features)
│  └─ Create single feature? → Use workflow 05 (init-feature)
│
├─ Feature DESIGN.md complete?
│  └─> Use workflow 06 (validate-feature)
│
├─ Ready to implement feature?
│  └─> Use workflow 09 (openspec-init)
│
├─ Active OpenSpec change?
│  ├─ Need to implement? → Use workflow 10 (openspec-change-implement)
│  ├─ Implementation done? → Use workflow 11 (openspec-change-complete)
│  ├─ Need next change? → Use workflow 12 (openspec-change-next)
│  └─ Need to validate? → Use workflow 13 (openspec-validate)
│
├─ All changes complete?
│  └─> Use workflow 07 (complete-feature)
│
└─ Design issue found?
   └─> Use workflow 07 (fix-design)
```

---

## Common Sequences

**New project from scratch**:
```
adapter-config → 01-init-project → 02-validate-architecture → 03-init-features
→ 06-validate-feature → 09-openspec-init → 10-openspec-change-implement
→ 11-openspec-change-complete → 13-openspec-validate → 07-complete-feature
```

**Add single feature to existing project**:
```
05-init-feature → 06-validate-feature → 09-openspec-init
→ 10-openspec-change-implement → 11-openspec-change-complete
→ 13-openspec-validate → 07-complete-feature
```

**Feature with multiple OpenSpec changes**:
```
09-openspec-init → 10-openspec-change-implement → 11-openspec-change-complete
→ 12-openspec-change-next → 10-openspec-change-implement
→ 11-openspec-change-complete → 13-openspec-validate → 07-complete-feature
```

**Fix design during implementation**:
```
10-openspec-change-implement → [issue found] → 08-fix-design
→ 06-validate-feature → 10-openspec-change-implement (continue)
```

---

## Critical Rules

- **Always read workflow file before executing** - Don't skip this step
- **Follow workflows sequentially** - Don't jump phases
- **Validate before proceeding** - Use validation workflows at checkpoints
- **One workflow at a time** - Complete current before starting next
- **Re-validate after fixes** - Use workflow 06 after workflow 07
- **OpenSpec commands run from feature root** - ALWAYS run `openspec` commands from `architecture/features/feature-{slug}/` directory (where feature DESIGN.md is located), NEVER from `openspec/` subdirectory

---

## Adapters - Workflow Extensions

**Purpose**: Adapters can extend workflows with project-specific pre-checks and validation commands.

**Location**: `guidelines/{project-name}-adapter/workflows/`

### Immutable Workflow Rules (Adapters CANNOT Override)

These are validated by tooling:

1. **Workflow sequence** - Must follow phase order (Architecture → Planning → Implementation)
2. **Workflow structure** - Each workflow's core steps are fixed
3. **Validation requirements** - Score thresholds and completeness checks are mandatory
4. **File structure requirements** - What each workflow creates/validates is fixed

### What Workflow Adapters Can Define

Everything else is project-specific:

- **Pre-workflow checks** - Environment setup, dependencies, services running
- **Validation commands** - Project-specific validation tools
- **Post-workflow actions** - Code generation, notifications, CI/CD triggers
- **Additional setup steps** - Project-specific initialization

**See**: `../ADAPTER_GUIDE.md` for creating workflow extensions

---

## See Also

- **Core Methodology**: `../AGENTS.md` - FDD principles
- **FDL Syntax**: `../FDL.md` - Flow and algorithm syntax
- **Adapters**: `../ADAPTER_GUIDE.md` - Creating project adapters
