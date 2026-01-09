---
description: Create or update Architecture Decision Records
---

# Create or Update Architecture Decision Records

**Type**: Operation  
**Role**: Architect  
**Artifact**: `architecture/ADR.md`

---

## Requirements

**ALWAYS open and follow**: `../requirements/adr-structure.md`

Extract:
- MADR format structure
- FDD extensions (Related Design Elements)
- ADR numbering rules
- Required sections

---

## Prerequisites

**MUST validate**:
- [ ] DESIGN.md exists - validate: Check file at `architecture/DESIGN.md`
- [ ] BUSINESS.md exists - validate: Check file at `architecture/BUSINESS.md`

**If missing**: Run `design` workflow first

---

## Steps

### 1. Detect Mode

Check if `architecture/ADR.md` exists:
- **If exists**: UPDATE mode - Add new ADR or edit existing ADR
- **If NOT exists**: CREATE mode - Create new file with ADR-0001

### 2. Read Design Context

Open `architecture/DESIGN.md` and `architecture/BUSINESS.md`

Extract:
- Architecture style and key decisions from DESIGN.md
- All actor IDs (from BUSINESS.md Section B)
- All capability IDs (from BUSINESS.md Section C)
- All requirement IDs (from DESIGN.md Section B)
- All principle IDs (from DESIGN.md Section B)

### 3. Mode-Specific Actions

**CREATE Mode** (ADR.md does NOT exist):
- Will create new file
- First ADR will be ADR-0001 (Initial Architecture)
- Proceed to Step 4 for ADR-0001 creation

**UPDATE Mode** (ADR.md exists):
- Read existing ADRs
- Find highest ADR number (ADR-NNNN)
- Ask user: Add new ADR or edit existing ADR?

**If Add New ADR**:
- Next ADR number = highest + 1
- Proceed to Step 4 for new ADR creation

**If Edit Existing ADR**:
- Show list of existing ADRs with numbers and titles
- Ask: Which ADR to edit? (ADR-NNNN)
- Read selected ADR content
- Proceed to Step 4 in EDIT mode

### 4. Interactive ADR Creation/Editing

**If CREATE mode or ADD NEW ADR**:
- Identify key architectural decisions from DESIGN.md that need documentation
- For ADR-0001: Document initial architecture decision
- For new ADRs: Ask user which decision to document

**If EDIT existing ADR**:
- Show current ADR content
- Ask what to change: Title, Context, Drivers, Options, Outcome, Related Elements, Status
- For each field, show current value and ask for updates

---

### 5. Collect ADR Information

**Mode-specific behavior**:

**Q1: Decision Title**
- Context: Short descriptive title
- **CREATE/ADD**: Ask for title
- **EDIT**: Show current title, ask for new title or keep
- Example: "Use OData v4 for Query Protocol"
- Store as: `ADR_TITLE`

**Q2: Problem Statement**
- Context: What problem requires this decision?
- **CREATE/ADD**: Ask to describe the problem
- **EDIT**: Show current context, ask for updates or keep
- Store as: `CONTEXT`

**Q3: Decision Drivers**
- Context: Factors influencing the decision
- **CREATE/ADD**: Ask for drivers, propose based on DESIGN.md
- **EDIT**: Show current drivers, ask to add/remove/modify or keep
- Store as: `DRIVERS[]`

**Q4: Options Considered**
- Context: Alternatives evaluated
- **CREATE/ADD**: Ask for options (≥2 required), propose common alternatives
- **EDIT**: Show current options, ask to add/remove/modify or keep
- Store as: `OPTIONS[]`

**Q5: Chosen Option**
- Context: Which option was selected
- **CREATE/ADD**: Ask to select from OPTIONS[]
- **EDIT**: Show current choice, ask to change or keep
- Store as: `CHOSEN_OPTION`

**Q6: Rationale**
- Context: Why this option was chosen
- **CREATE/ADD**: Ask for reasoning
- **EDIT**: Show current rationale, ask for updates or keep
- Store as: `RATIONALE`

**Q7: Consequences**
- Context: Positive and negative outcomes
- **CREATE/ADD**: Ask for pros and cons
- **EDIT**: Show current consequences, ask to modify or keep
- Store as: `PROS[]`, `CONS[]`

**Q8: Status** (EDIT mode only)
- Context: Current status of the decision
- **EDIT**: Show current status, ask to change: Proposed → Accepted → Deprecated/Superseded
- Store as: `STATUS`

### 6. Link to FDD Design Elements

**Map decision to FDD elements**:

**Actors affected**:
- Review actor list from BUSINESS.md
- **CREATE/ADD**: Ask which actors are affected (optional)
- **EDIT**: Show current actors, ask to add/remove or keep
- Store as: `RELATED_ACTORS[]`

**Capabilities affected**:
- Review capability list from BUSINESS.md
- **CREATE/ADD**: Ask which capabilities are affected (≥1 required if actors empty)
- **EDIT**: Show current capabilities, ask to add/remove or keep
- Store as: `RELATED_CAPABILITIES[]`

**Requirements affected**:
- Review requirement list from DESIGN.md
- **CREATE/ADD**: Ask which requirements are affected (optional)
- **EDIT**: Show current requirements, ask to add/remove or keep
- Store as: `RELATED_REQUIREMENTS[]`

**Principles affected**:
- Review principle list from DESIGN.md
- **CREATE/ADD**: Ask which principles are affected (optional)
- **EDIT**: Show current principles, ask to add/remove or keep
- Store as: `RELATED_PRINCIPLES[]`

**Validation**: At least one of the Related Design Elements categories must have ≥1 ID

### 7. Generate ADR Content

**CREATE/ADD mode**: Create new ADR entry following MADR format with FDD extensions

**EDIT mode**: Update existing ADR with modified content

**ADR format**:

```markdown
## ADR-{NNNN}: {ADR_TITLE}

**Date**: {current_date}  
**Status**: Proposed  
**Deciders**: {team_name}  
**Technical Story**: {optional}

### Context and Problem Statement

{CONTEXT}

### Decision Drivers

{DRIVERS[]}

### Considered Options

{OPTIONS[]}

### Decision Outcome

**Chosen option**: "{CHOSEN_OPTION}"

**Rationale**: {RATIONALE}

**Positive Consequences**:
{PROS[]}

**Negative Consequences**:
{CONS[]}

### Related Design Elements

**Actors**:
{RELATED_ACTORS[]}

**Capabilities**:
{RELATED_CAPABILITIES[]}

**Requirements**:
{RELATED_REQUIREMENTS[]}

**Principles**:
{RELATED_PRINCIPLES[]}
```

### 8. Summary and Confirmation

Show:
- **CREATE**: File path: `architecture/ADR.md` (new file)
- **ADD**: ADR number: ADR-{NNNN} (new entry)
- **EDIT**: ADR number: ADR-{NNNN} (updating existing)
- Title: {ADR_TITLE}
- Status: {STATUS}
- Related elements count
- Changes summary (for EDIT mode)

Ask: Proceed? [yes/no/modify]

### 9. Create or Update File

**CREATE Mode** (ADR.md does NOT exist):
- Create new file with document header
- Add ADR-0001 entry

**ADD Mode** (append new ADR):
- Read existing ADR.md
- Append new ADR with `---` separator
- Maintain chronological order
- Verify ADR number unique

**EDIT Mode** (update existing ADR):
- Read existing ADR.md
- Find and replace the ADR being edited
- Preserve all other ADRs unchanged
- Maintain chronological order

After operation:
- Verify file exists
- Verify content correct

---

## Validation

Run: `adr-validate`

Expected:
- Score: ≥90/100
- Status: PASS
- All FDD IDs valid

---

## Next Steps

**After ADR creation**:
- Status remains "Proposed" until implementation
- Update status to "Accepted" after implementation
- Reference ADR in DESIGN.md where relevant
- Reference ADR in feature designs

**Continue development**:
- `features` workflow - Decompose design into features
