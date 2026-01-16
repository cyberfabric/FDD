# FDD Adapter: Manual Update

**Type**: Operation  
**Role**: Any  
**Artifact**: `{adapter-directory}/FDD-Adapter/AGENTS.md` + `specs/` files

---

**ALWAYS open and follow**: `../requirements/core.md` WHEN editing this file

ALWAYS open and follow `../requirements/workflow-execution.md` WHEN executing this workflow

## Purpose

Manually add or update adapter specifications based on user decisions.

**Use cases**:
- User wants to add specific specification
- User wants to update existing specification
- User explicitly states technical decision
- User wants to document pattern/convention

---

## Requirements

**ALWAYS open and follow**: `../requirements/adapter-structure.md`

Extract:
- Spec file types and formats
- AGENTS.md MUST rule format
- Validation criteria

---

## Prerequisites

**Prerequisites**:
- [ ] Adapter initialized - validate: Check {adapter-directory}/FDD-Adapter/AGENTS.md exists

**If adapter NOT initialized**: Run `adapter-bootstrap` first

---

## Steps

### 1. Locate Adapter

Search for existing adapter:
- `/FDD-Adapter/AGENTS.md`
- `spec/FDD-Adapter/AGENTS.md`
- `docs/FDD-Adapter/AGENTS.md`

**If NOT found**:
- STOP → Run `adapter-bootstrap` first

**If found**:
- Store location as `ADAPTER_DIR`
- Read existing AGENTS.md
- List existing specs

### 2. Ask User Intent

```
Current Adapter: {ADAPTER_DIR}/FDD-Adapter/

Existing specs:
  - specs/tech-stack.md
  - specs/domain-model.md
  - specs/api-contracts.md
  
What would you like to do?
  1. Add new specification
  2. Update existing specification
  3. Add pattern
  4. Add code snippet
  5. Add example
  
Choose: [1-5]
```

### 3. Route to Specific Action

Based on user choice:

#### Action 1: Add New Specification

Ask:
```
Which specification type?
  1. tech-stack.md - Technology stack
  2. domain-model.md - Domain model format
  3. api-contracts.md - API contract format
  4. patterns.md - Architecture patterns
  5. conventions.md - Code conventions
  6. build-deploy.md - Build and deploy
  7. testing.md - Testing framework
  8. Custom specification

Choose: [1-8]
```

Then proceed to Step 4 with selected type.

#### Action 2: Update Existing Specification

Show list of existing specs:
```
Existing specifications:
  1. specs/tech-stack.md
  2. specs/domain-model.md
  3. specs/api-contracts.md

Which to update? [1-3]
```

Read selected spec, show current content, ask for changes.

#### Action 3: Add Pattern

Ask:
```
Pattern details:
  - Name: 
  - Category: (Architecture/Design/Implementation)
  - When to use:
  - Implementation example:
  - Source: (ADR ID or reference)
```

Create/update `specs/patterns.md`.

#### Action 4: Add Code Snippet

Ask:
```
Snippet details:
  - Category: (error-handling/validation/auth/utils/etc)
  - Name:
  - Description:
  - Code:
  - Usage example:
```

Create/update `specs/snippets/{category}.md`.

#### Action 5: Add Example

Ask:
```
Example details:
  - Feature name:
  - Description:
  - Code/implementation:
  - Key patterns used:
```

Create/update `specs/examples/{feature}.md`.

### 4. Interactive Input Collection

**For tech-stack.md**:
```
Tech Stack:

Languages (e.g., Python 3.11+):
> 

Frameworks (e.g., Django 4.2+):
> 

Databases (e.g., PostgreSQL 15+):
> 

Other dependencies:
> 

Source (ADR ID or reference):
> 
```

**For domain-model.md**:
```
Domain Model:

Format (e.g., JSON Schema, TypeScript, Protobuf):
> 

Location (relative to project root):
> 

Entity structure example:
> 

Type identifier format:
> 

Source (DESIGN.md section or ADR):
> 
```

**For api-contracts.md**:
```
API Contracts:

Format (e.g., OpenAPI 3.0, GraphQL, gRPC):
> 

Location (relative to project root):
> 

Endpoint pattern example:
> 

Source (DESIGN.md section or file path):
> 
```

**For patterns.md entry**:
```
Pattern: {name}

**Category**: {Architecture/Design/Implementation}

**When to use**: {description}

**Implementation**:
{code or description}

**Source**: {ADR ID or reference}
```

**For conventions.md**:
```
Code Conventions:

File naming convention:
> 

Code style:
> 

Project structure:
> 

Source (code analysis or config files):
> 
```

**For build-deploy.md**:
```
Build & Deploy:

Build command:
> 

Test command:
> 

Lint command:
> 

Deploy steps:
> 

Source (Makefile, package.json, etc.):
> 
```

**For testing.md**:
```
Testing:

Unit test framework:
> 

Integration test framework:
> 

E2E test framework:
> 

Test structure:
> 

Coverage command:
> 

Source (test code or config):
> 
```

### 5. Generate/Update Spec File

Create or update spec file in `{ADAPTER_DIR}/FDD-Adapter/specs/`.

Show preview:
```
═══════════════════════════════════════════════
Preview: specs/tech-stack.md

# Tech Stack

**Languages**:
- Python 3.11+

**Frameworks**:
- Django 4.2+

**Databases**:
- PostgreSQL 15+

**Source**: ADR-0001, ADR-0005
═══════════════════════════════════════════════

Save this? [Yes] [No] [Edit]
```

### 6. Update AGENTS.md

**If new spec file created**:

Check if MUST rule exists for this spec.

**If NOT exists**:
- Add MUST rule to AGENTS.md
- Show preview

```
Adding to AGENTS.md:

ALWAYS open and follow `specs/tech-stack.md` WHEN executing workflows: adapter.md, adapter-auto.md, adapter-manual.md, adapter-bootstrap.md, adapter-validate.md, design.md, design-validate.md, adr.md, adr-validate.md, feature-change-implement.md, feature-code-validate.md

Add this rule? [Yes] [No] [Edit]
```

**If exists**:
- No change to AGENTS.md needed

### 7. Show Summary

```
═══════════════════════════════════════════════
Adapter Manual Update Complete

Action: Created specs/tech-stack.md
Updated: AGENTS.md (added MUST rule)

Content added:
  - Python 3.11+
  - Django 4.2+
  - PostgreSQL 15+
  
Source: ADR-0001, ADR-0005
═══════════════════════════════════════════════
```

### 8. Run Validation

**Execute**: `adapter-validate` workflow

```yaml
Validation will:
  1. Locate adapter
  2. Detect phase (Bootstrap or Evolved)
  3. Validate all specs
  4. Check new/updated content
  5. Output to chat
```

Expected result:
```
## Validation: FDD Adapter (Evolved)

Location: {ADAPTER_DIR}
Score: {X}/100
Status: PASS | FAIL

[Detailed validation results]
```

**If validation fails**:
- Review validation report
- Fix issues in spec files
- Re-run validation

---

## Validation

Automatically runs `adapter-validate` at completion

---

## Next Steps

**Continue working**:
- Make more manual updates if needed
- Continue with FDD workflows

**Optional**:
- `adapter-auto` - Re-scan project for missed items
- Review all specs for consistency

---

## Examples

### Example: Add Pattern

```
User: "Add LRU caching pattern to adapter"

Agent:
  Which specification type?
  > 4. patterns.md

  Pattern details:
  Name: LRU Cache
  Category: Implementation
  When to use: Caching frequently accessed data
  Implementation: [code example]
  Source: Feature fdd-context-provider

Preview: specs/patterns.md
  ## LRU Cache
  **Category**: Implementation
  **When to use**: Caching frequently accessed data
  **Implementation**: {...}
  **Source**: Feature fdd-context-provider

Save? [Yes]

✓ Updated specs/patterns.md
✓ MUST rule already exists

Complete.
```

### Example: Update Tech Stack

```
User: "Update adapter, add Redis to tech stack"

Agent:
  What would you like to do?
  > 2. Update existing specification

  Which to update?
  > 1. specs/tech-stack.md

Current content:
  Languages: Python 3.11+
  Frameworks: Django 4.2+
  Databases: PostgreSQL 15+

Add Redis where?
> Databases section

Preview:
  Databases:
  - PostgreSQL 15+
  - Redis 7+

Save? [Yes]

✓ Updated specs/tech-stack.md

Complete.
```
