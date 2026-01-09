---
description: Create or update features manifest
---

# Create or Update Features Manifest

**Type**: Operation  
**Role**: Architect  
**Artifact**: `architecture/features/FEATURES.md`

---

## Requirements

**ALWAYS open and follow**: `../requirements/features-manifest-structure.md`

Extract:
- Required structure (feature list format)
- Feature ID format
- Dependency specification format
- Validation criteria

---

## Prerequisites

**MUST validate**:
- [ ] DESIGN.md exists - validate: Check file at `architecture/DESIGN.md`
- [ ] DESIGN.md validated - validate: Score ≥90/100

**If missing**: Run `design` and `design-validate` first

---

## Steps

### 1. Detect Mode

Check if `architecture/features/FEATURES.md` exists:
- **If exists**: UPDATE mode - Add/edit/remove features
- **If NOT exists**: CREATE mode - Decompose design into features

### 2. Read Overall Design

Open `architecture/DESIGN.md`

Extract:
- All requirements (Section B)
- All capabilities (from BUSINESS.md reference)
- Architecture components (Section C)

### 3. Mode-Specific Actions

**CREATE Mode**:
- Decompose design into features from scratch
- Proceed to Step 4

**UPDATE Mode**:
- Read existing FEATURES.md
- Extract current features with IDs, status, dependencies
- Ask user: What to update?
  - Add new feature
  - Edit existing feature (name, description, requirements, dependencies, status)
  - Remove feature
  - Update feature status
- Proceed to Step 4 with appropriate action

### 4. Feature Decomposition/Updates

**CREATE mode** - Decompose into features:
- For each capability or major component: Identify 1-3 features
- Each feature = cohesive unit of functionality
- Feature covers 3-10 requirements

**UPDATE mode** - Apply changes:
- For new features: Follow CREATE mode decomposition
- For edited features: Update specified fields
- For removed features: Mark for deletion

**Generate/update feature list**:
- Feature name (clear, descriptive)
- Feature slug (kebab-case)
- Purpose (what it does)
- Requirements covered (IDs from DESIGN.md)
- Dependencies (other features)
- Status (for UPDATE mode)

Store as: `FEATURES[]`

### 3. Generate Feature IDs

For each feature:
- ID format: `fdd-feature-{slug}`
- Validate uniqueness
- Validate format per requirements

### 4. Analyze Dependencies

For each feature:
- Check if depends on other features
- Note dependency type (requires, extends)
- Validate no circular dependencies

### 5. Create FEATURES.md

Generate content following `features-manifest-structure.md`:
- Header with project info
- Feature list table (ID, name, status, dependencies)
- Feature details (purpose, requirements covered, scope)

Ensure:
- All requirements from DESIGN.md covered
- No orphaned requirements
- Dependencies valid
- All IDs formatted correctly

### 6. Create Feature Directories

For each feature in list:
- Create `architecture/features/feature-{slug}/`
- Create placeholder `DESIGN.md` with header

### 7. Summary and Confirmation

Show:
- **CREATE**: File path: `architecture/features/FEATURES.md` (new file)
- **UPDATE**: File path: `architecture/features/FEATURES.md` (updating existing)
- Features: {count} ({added}/{modified}/{removed})
- Dependencies graph
- Requirements coverage
- Changes summary (for UPDATE mode)

Ask: Proceed? [yes/no/modify]

### 8. Create or Update File

**CREATE Mode**:
- Create `architecture/features/` directory
- Create `architecture/features/FEATURES.md`

**UPDATE Mode**:
- Read existing FEATURES.md
- Apply changes to content
- Write updated FEATURES.md

After operation:
- Verify file exists
- Verify content correct
- Create feature subdirectories
- Create placeholder DESIGN.md files
- Verify creation

---

## Validation

Run: `features-validate`

Expected:
- Score: ≥90/100
- Status: PASS
- 100% requirements coverage

---

## Next Steps

**If validation passes**: `feature` workflow for each feature

**If validation fails**: Fix FEATURES.md, re-validate
