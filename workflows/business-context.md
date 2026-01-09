---
description: Create or update business context document
---

# Create or Update Business Context

**Type**: Operation  
**Role**: Product Manager  
**Artifact**: `architecture/BUSINESS.md`

---

## Requirements

**ALWAYS open and follow**: `../requirements/business-context-structure.md`

Extract:
- Required sections (A: Vision, B: Actors, C: Capabilities, D: Additional Context)
- ID formats for actors and capabilities
- Content requirements per section
- Examples and validation criteria

---

## Prerequisites

**MUST validate**:
- [ ] Project repository exists - validate: Check .git directory
- [ ] Architecture directory exists - validate: Check `architecture/` directory or create

**No dependencies** - This is typically second workflow after adapter

---

## Steps

### 1. Detect Mode

Check if `architecture/BUSINESS.md` exists:
- **If exists**: UPDATE mode - Read and propose changes
- **If NOT exists**: CREATE mode - Generate from scratch

### 2. Mode-Specific Actions

**CREATE Mode**:
- Proceed to Step 3 for interactive input collection

**UPDATE Mode**:
- Read existing BUSINESS.md
- Extract current content:
  - Section A: Vision
  - Section B: Actors (with IDs)
  - Section C: Capabilities (with IDs)
  - Section D: Additional Context (if present)
- Ask user: What to update?
  - Add new actors
  - Edit existing actors
  - Remove actors
  - Add new capabilities
  - Edit existing capabilities
  - Remove capabilities
  - Update vision
  - Update additional context
- Proceed to Step 3 with appropriate questions

### 3. Interactive Input Collection

**Mode-specific behavior**:

**Q1: System Vision**
- Context: High-level purpose, target users, problems solved (2-4 sentences)
- **CREATE**: Ask for vision, propose based on README.md
- **UPDATE**: Show current vision, ask for updates or keep
- Store as: `VISION`

**Q2: Key Actors**
- Context: Who interacts with this system?
- **CREATE**: Ask for 3-5 actors, propose based on vision
- **UPDATE**: Show current actors, ask to add/edit/remove or keep
- For each: Name and role description
- Store as: `ACTORS[]`

**Q3: Core Capabilities**
- Context: What can the system do?
- **CREATE**: Ask for 3-7 capabilities, propose based on vision/actors
- **UPDATE**: Show current capabilities, ask to add/edit/remove or keep
- Store as: `CAPABILITIES[]`

**Q4: Additional Context** (optional)
- Context: Constraints, compliance, legacy integration
- **CREATE**: Allow skip if none
- **UPDATE**: Show current context, ask for updates or keep
- Store as: `ADDITIONAL_CONTEXT`

### 4. Generate/Update IDs

**For new actors**:
- Generate ID: `fdd-{project}-actor-{kebab-case-name}`
- Validate format per requirements

**For new capabilities**:
- Generate ID: `fdd-{project}-capability-{kebab-case-name}`
- Link to relevant actors
- Validate format per requirements

**For edited actors/capabilities**:
- Keep existing IDs unless rename requested
- Update descriptions/roles as needed

### 5. Generate Content

**CREATE mode**: Generate complete new BUSINESS.md

**UPDATE mode**: Update existing BUSINESS.md with changes

Generate content following `business-context-structure.md`:
- Section A: Vision ({VISION})
- Section B: Actors (with IDs, roles)
- Section C: Capabilities (with IDs, descriptions, actor references)
- Section D: Additional Context (if {ADDITIONAL_CONTEXT})

Ensure:
- All IDs wrapped in backticks
- All sections present
- No placeholders

### 6. Summary and Confirmation

Show:
- **CREATE**: File path: `architecture/BUSINESS.md` (new file)
- **UPDATE**: File path: `architecture/BUSINESS.md` (updating existing)
- Vision statement (if changed)
- Actors: {count} ({added}/{modified}/{removed})
- Capabilities: {count} ({added}/{modified}/{removed})
- Additional context (if any/changed)
- Changes summary (for UPDATE mode)

Ask: Proceed? [yes/no/modify]

### 7. Create or Update File

**CREATE Mode**:
- Create `architecture/` directory if needed
- Create `architecture/BUSINESS.md`

**UPDATE Mode**:
- Read existing BUSINESS.md
- Apply changes to content
- Write updated BUSINESS.md

After operation:
- Verify file exists
- Verify content correct

---

## Validation

Run: `business-validate`

Expected:
- Score: ≥90/100
- Status: PASS

---

## Next Steps

**If validation passes**: `design` workflow (create DESIGN.md)

**If validation fails**: Fix BUSINESS.md, re-run `business-validate`
