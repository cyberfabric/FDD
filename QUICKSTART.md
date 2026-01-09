# FDD Quick Start Guide

**Get started with Feature-Driven Development in 5 minutes**

---

## What is FDD?

FDD (Feature-Driven Development) is a design-first methodology that ensures your code matches your design through strict validation. It enforces a clear hierarchy: **Overall Design → Feature Design → Changes → Code**.

**Core principle**: Design is source of truth. If code contradicts design, fix design first, then re-validate.

---

## Quick Start

### 1. Create or Update FDD Adapter (Required First Step)

**FDD requires a project-specific adapter before ANY work can begin.**

```bash
# Check for adapter at:
spec/FDD-Adapter/AGENTS.md
```

**Follow workflow**: **adapter.md** (workflows/adapter.md)
- **No adapter found** → CREATE mode (5-10 minutes)
- **Adapter exists** → UPDATE mode (2-5 minutes for targeted changes)

This workflow guides you through:
- ✅ Detects mode automatically (CREATE/UPDATE)
- ✅ CREATE: Ask guided questions about your project
- ✅ UPDATE: Show current config, ask what to change
- ✅ Define/update domain model format (GTS, JSON Schema, TypeScript, etc.)
- ✅ Define/update API contract format (OpenAPI, GraphQL, CLISPEC, etc.)
- ✅ Capture/update security model and non-functional requirements
- ✅ Generate or update `spec/FDD-Adapter/AGENTS.md` and spec files

**Result**: Adapter created/updated at `spec/FDD-Adapter/` with status COMPLETE or INCOMPLETE

**Alternative**: Use **adapter-from-sources.md** to analyze existing codebase and generate/update adapter automatically.

### 1a. Configure or Update AI Agent (Optional)

**After creating adapter, optionally set up your AI agent:**

Follow workflow: **adapter-agents.md** (workflows/adapter-agents.md)
- **No agent config found** → CREATE mode (2 minutes)
- **Agent config exists** → UPDATE mode (change style, add workflows, etc.)

This workflow creates/updates agent-specific configuration:
- **Windsurf**: `.windsurf/rules/` + workflow wrappers in `.windsurf/workflows/`
- **Cursor**: `.cursorrules` (single file with inline workflow references)
- **Cline**: `.clinerules` (minimal single file)
- **Aider**: `.aider.conf.yml` (YAML config)

**All configs**:
- Detects existing config and enters UPDATE mode
- Tell agent to ALWAYS open and follow `specs/api-contracts.md` WHEN working with API endpoints
- Provide FDD workflow references
- UPDATE mode: Change content style (minimal ↔ full), add/remove workflow files

### 2. Create or Update Business Context

Follow workflow: **business-context.md** (workflows/business-context.md)
- **No BUSINESS.md found** → CREATE mode (30 minutes)
- **BUSINESS.md exists** → UPDATE mode (add actors, capabilities, update vision)

This workflow creates/updates `architecture/BUSINESS.md` with:
- **Section A**: System vision and purpose
- **Section B**: Key actors (users, systems, external services)
- **Section C**: Core capabilities (what system can do)
- **Section D**: Additional context (constraints, compliance)

### 3. Create or Update Overall Design

Follow workflow: **design.md** (workflows/design.md)
- **No DESIGN.md found** → CREATE mode (2-3 hours)
- **DESIGN.md exists** → UPDATE mode (update architecture, add components, edit NFRs)

This workflow creates/updates `architecture/DESIGN.md` with:
- **Section A**: Architecture overview (style, layers)
- **Section B**: Requirements & principles
- **Section C**: Technical architecture (components, domain model, API contracts, security)
- **Section D**: Additional context (optional)

**Recommended**: Use an AI agent to edit the design. The agent will automatically:
- Detect mode (CREATE/UPDATE) and act accordingly
- Follow FDD requirements and validation rules
- Apply adapter-specific conventions (DML syntax, API linking)
- Use FDL (plain English) for flows, never code
- Reference domain types from Overall Design ALWAYS open and follow `specs/domain-model.md` WHEN working with domain types
- Ensure proper structure and completeness
- CREATE mode: Auto-creates ADR-0001 (Initial Architecture)

**Key**: Use **FDL** (plain English) for flows, never write code in DESIGN.md

### 4. Validate Overall Design

Follow workflow: **design-validate.md** (workflows/design-validate.md)
- Must score ≥90/100
- Auto-triggers **adr-validate.md** after DESIGN.md passes

### 5. Create or Update Architecture Decision Records (Optional)

Follow workflow: **adr.md** (workflows/adr.md)
- **No ADR.md found** → CREATE mode (creates ADR.md with first ADR)
- **ADR.md exists** → UPDATE mode (add new ADR or edit existing)

Three modes:
- **CREATE**: Generate ADR.md with ADR-0001
- **ADD**: Add new ADR to existing ADR.md
- **EDIT**: Edit existing ADR (update status, add considerations)

### 6. Create or Update Features Manifest

Follow workflow: **features.md** (workflows/features.md)
- **No FEATURES.md found** → CREATE mode (extracts from DESIGN.md, 5 minutes)
- **FEATURES.md exists** → UPDATE mode (add/edit/remove features, update status)

### 7. Create or Update Feature Designs

Follow workflow: **feature.md** (workflows/feature.md)
- **No feature DESIGN.md found** → CREATE mode (1-2 hours per feature)
- **Feature DESIGN.md exists** → UPDATE mode (edit flows, add algorithms, update requirements)

For each feature in `architecture/features/feature-{slug}/DESIGN.md`:
- **Section A**: Feature overview and scope
- **Section B**: Actor flows in FDL (PRIMARY!)
- **Section C**: Algorithms in FDL
- **Section D**: States in FDL (optional)
- **Section E**: Technical details (DB, operations, errors)
- **Section F**: Requirements (formalized scope + testing)
- **Section G**: Implementation plan (OpenSpec changes)

**Recommended**: Use an AI agent to design features. The agent will automatically:
- Detect mode (CREATE/UPDATE) and show current content in UPDATE mode
- Follow FDD feature requirements (Section A-G structure)
- Apply adapter conventions (DML references, API linking)
- Use FDL only, never write code in DESIGN.md
- Reference Overall Design types (never redefine)
- Start with Actor Flows (Section B) - the primary driver
- Ensure 100/100 validation readiness

**Key**: Design Section B (Actor Flows) FIRST - everything flows from there

### 8. Validate Feature

Follow workflow: **feature-validate.md** (workflows/feature-validate.md)

Must score 100/100 + 100% completeness

### 9. Create or Update Implementation Plan

Follow workflow: **feature-changes.md** (workflows/feature-changes.md)
- **No CHANGES.md found** → CREATE mode (decompose feature into changes, 15-30 min)
- **CHANGES.md exists** → UPDATE mode (add new changes, edit tasks, update status)

Breaks feature into atomic implementation changes with tasks.

### 10. Implement Changes

Follow workflow: **feature-change-implement.md** (workflows/feature-change-implement.md)

Implements each change according to tasks in CHANGES.md.

### 11. Validate and Complete

Follow workflows:
1. **feature-changes-validate.md** - Validate CHANGES.md structure
2. **feature-qa.md** - Complete feature QA (runs all validations + tests)

---

## Core Concepts

### Design Hierarchy (Never Violate)

```
ADAPTER (tech stack, conventions)
    ↓ defines formats and tools
BUSINESS CONTEXT
    ↓ defines actors and capabilities
OVERALL DESIGN
    ↓ reference, never contradict
FEATURE DESIGN
    ↓ reference, never contradict
CHANGES (implementation plan)
    ↓ implement exactly
CODE
```

### FDL - Flow Description Language

Plain English pseudo-code for flows and algorithms. **Never write actual code in DESIGN.md**.

```markdown
✅ Good (FDL):
1. User submits login form with email and password
2. System validates email format
3. System checks credentials against database
4. IF credentials valid:
   - Generate JWT token
   - Return token to user
5. ELSE:
   - Return "Invalid credentials" error

❌ Bad (actual code):
const token = jwt.sign({ userId: user.id }, SECRET);
return res.json({ token });
```

### Actor Flows (Section B)

**Always design Actor Flows first**. They drive everything:
- What each actor (user, system, external service) does
- Step-by-step interactions
- Decision points and branches
- Error cases

### Domain Model

Define types ONCE in Overall Design. Reference them everywhere:
- `@DomainModel.User` in Feature Design
- Redefining User type in Feature Design

### OpenSpec Changes

Each change is atomic and deployable:
- `proposal.md` - Why this change
- `tasks.md` - Implementation checklist
- `specs/` - Delta specifications
- `design.md` - Technical decisions (optional)

---

## Best Practices

### Design Phase

1. **Start with Actor Flows** - Section B drives everything
2. **Use FDL only** - Never write code in DESIGN.md
3. **Reference, don't redefine** - Link to Overall Design types
4. **Keep features small** - ≤3000 lines recommended, ≤4000 hard limit
5. **Validate early, validate often** - Catch issues before coding

### Implementation Phase

1. **Design is source of truth** - If contradiction found, fix design first
2. **Atomic changes** - Each OpenSpec change is deployable
3. **Follow the plan** - Feature DESIGN.md Section F has the roadmap
4. **Update as you learn** - Use workflow 08-fix-design when needed
5. **Test continuously** - OpenSpec validates each change

### Team Collaboration

1. **Read the adapter** - Understand project-specific conventions
2. **Check FEATURES.md** - See what's blocked/in-progress
3. **Review designs first** - Before implementation starts
4. **Use workflows** - Don't skip validation steps
5. **Document decisions** - Section D for context, design.md for technical choices

### Common Pitfalls

**Skip adapter creation** → ALL workflows blocked without adapter
**Incomplete adapter** → Create specs or skip optional sections
**Write code in DESIGN.md** → Use FDL instead
**Redefine types** → Reference Overall Design
**Skip validation** → Catch issues early, not late
**Make features too large** → Break into smaller features
**Fix code when design wrong** → Fix design, then re-validate

---

## Examples

### Example 1: Simple REST API

**Overall Design** (architecture/DESIGN.md):
```markdown
## A. Business Context

### System Vision
User management API for authentication and profile management.

### Actors
- **End User**: Can register, login, view/update profile
- **Admin**: Can manage all users
- **System**: Handles token generation and validation

## B. Requirements & Principles

### Business Rules
- Email must be unique
- Passwords hashed with bcrypt
- JWT tokens expire after 24 hours

## C. Technical Architecture

### Domain Model
@DomainModel.User:
- id: UUID
- email: string (unique)
- passwordHash: string
- role: "user" | "admin"
- createdAt: timestamp

### API Contracts
@API.POST:/auth/register - User registration
@API.POST:/auth/login - User login
@API.GET:/users/me - Get current user profile
```

**Feature Design** (architecture/features/feature-user-auth/DESIGN.md):
```markdown
## B. Actor Flows (FDL)

### Flow 1: User Registration
1. End User submits registration form with email and password
2. System validates email format (RFC 5322)
3. System checks email not already registered
4. IF email exists:
   - Return "Email already registered" error
5. System hashes password with bcrypt (cost factor 10)
6. System creates User record in database
7. System generates JWT token with user ID and role
8. Return token and user data to End User

### Flow 2: User Login
1. End User submits login form with email and password
2. System finds User by email in database
3. IF User not found:
   - Return "Invalid credentials" error
4. System compares password hash with bcrypt
5. IF password invalid:
   - Return "Invalid credentials" error
6. System generates JWT token with user ID and role
7. Return token and user data to End User
```

### Example 2: CLI Tool

**Adapter** uses **CLISPEC** for API contracts:
```
COMMAND validate-feature
SYNOPSIS: mytool validate-feature <slug> [options]
DESCRIPTION: Validate feature design completeness
WORKFLOW: 06-validate-feature

ARGUMENTS:
  slug  <slug>  required  Feature identifier

OPTIONS:
  --strict  <boolean>  Enable strict validation mode

EXIT CODES:
  0  Valid (score 100/100)
  2  Validation failed

EXAMPLE:
  $ mytool validate-feature user-authentication
---
```

### Example 3: Domain Model with GTS

**Overall Design** defines types:
```json
{
  "$schema": "https://json-schema.org/draft/2020-12/schema",
  "$id": "gts://gts.myapp.core.user.v1~",
  "type": "object",
  "properties": {
    "gtsId": { "type": "string" },
    "email": { "type": "string", "format": "email" },
    "role": { "enum": ["user", "admin"] }
  }
}
```

**Feature Design** references it:
```markdown
## E. Technical Details

### Database Schema
Uses @DomainModel[gts.myapp.core.user.v1~]

Operations:
- Create: INSERT INTO users (email, password_hash, role)
- Read: SELECT * FROM users WHERE id = ?
- Update: UPDATE users SET email = ? WHERE id = ?
```

---

## Workflow Cheatsheet

**All operation workflows support CREATE & UPDATE modes**

```bash
# Adapter Setup (REQUIRED FIRST)
adapter.md                             # Create OR update adapter
adapter-from-sources.md                # Create OR update from codebase
adapter-agents.md                      # Create OR update AI agent config

# Architecture & Requirements
business-context.md                    # Create OR update BUSINESS.md
adr.md                                 # Create/add/edit ADRs
design.md                              # Create OR update DESIGN.md

# Validation
business-validate.md                   # Validate BUSINESS.md
adr-validate.md                        # Validate ADR.md
design-validate.md                     # Validate DESIGN.md (≥90/100)

# Feature Management
features.md                            # Create OR update FEATURES.md
feature.md                             # Create OR update feature DESIGN.md
feature-changes.md                     # Create OR update CHANGES.md
feature-change-implement.md            # Implement changes

# Feature Validation
features-validate.md                   # Validate FEATURES.md
feature-validate.md                    # Validate feature DESIGN.md (100/100)
feature-changes-validate.md            # Validate CHANGES.md
feature-change-validate.md             # Validate specific change
feature-qa.md                          # Complete feature QA
```

---

## Next Steps

1. **Read AGENTS.md** - Full FDD methodology
2. **Read workflows/AGENTS.md** - Workflow selection guide
3. **Read FDL.md** - Flow Description Language syntax
4. **Check ADAPTER_GUIDE.md** - How to create adapters
5. **See CLISPEC.md** - CLI command specification format (if building CLI tools)

---

## Resources

- **FDD Core**: `AGENTS.md`
- **Workflows**: `workflows/AGENTS.md`
- **FDL Syntax**: `FDL.md`
- **Adapter Guide**: `ADAPTER_GUIDE.md`
- **CLI Format**: `CLISPEC.md`
- **OpenSpec**: https://openspec.dev

---

## Get Help

**Validation failed?** 
- Check error messages carefully
- Review the specific section mentioned
- Use FDL for flows/algorithms
- Reference domain types from Overall Design

**Feature too large?**
- Break into multiple smaller features
- Each feature should be one capability
- Target ≤3000 lines per DESIGN.md

**Code contradicts design?**
- STOP coding immediately
- Fix design using workflow 08-fix-design
- Re-validate with workflow 06-validate-feature
- Resume coding only after validation passes

**Need to change Overall Design?**
- Update architecture/DESIGN.md
- Re-validate with workflow 02-validate-architecture
- Update affected Feature Designs
- Re-validate features

---

## Remember

✅ **Run adapter-config first** - ALL workflows blocked without adapter at `spec/FDD-Adapter/`
✅ **Design before code** - Always validate designs first
✅ **Actor flows are primary** - Start with Section B
✅ **Use FDL, not code** - Plain English in DESIGN.md
✅ **Reference, don't redefine** - Link to Overall Design
✅ **Validate often** - Catch issues early
✅ **Design is truth** - Fix design first, code second

**Start with adapter-config, then happy designing! 🎨**
