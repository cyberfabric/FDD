# FDD Adapter: Bootstrap (Minimal Initialization)

**Type**: Operation  
**Role**: Any  
**Artifact**: `{adapter-directory}/FDD-Adapter/AGENTS.md` (minimal)

---

## Purpose

Create minimal adapter for new projects - just `AGENTS.md` with `Extends` declaration.

**No specs yet** - specs will be added later through:
- Design decisions → trigger-based evolution
- Manual updates → `adapter-manual` workflow
- Project scanning → `adapter-auto` workflow

---

## Requirements

**ALWAYS open and follow**: `../requirements/adapter-structure.md`

Extract:
- Minimal AGENTS.md format
- Bootstrap validation criteria (100/100 if Extends present)

---

## Prerequisites

**Prerequisites**:
- [ ] Project repository exists - validate: Check .git directory exists
- [ ] Write permissions - validate: Can create directories and files

**No other prerequisites** - This is typically first workflow

---

## Steps

### 1. Choose Adapter Location

Ask user to select adapter directory:

**Options**:
1. `guidelines/FDD-Adapter/` (recommended for docs-heavy projects)
2. `spec/FDD-Adapter/` (recommended for technical projects)
3. `docs/FDD-Adapter/` (alternative)
4. Custom path

**Default**: `guidelines/FDD-Adapter/`

Store as: `ADAPTER_DIR`

### 2. Calculate Relative Path

Calculate path from `ADAPTER_DIR` to FDD core:

```yaml
If guidelines/FDD-Adapter/:
  relative_path = ../FDD/AGENTS.md

If spec/FDD-Adapter/:
  relative_path = ../../guidelines/FDD/AGENTS.md

If docs/FDD-Adapter/:
  relative_path = ../../guidelines/FDD/AGENTS.md

If custom/{path}/FDD-Adapter/:
  Calculate: relative path to guidelines/FDD/AGENTS.md
```

Store as: `RELATIVE_PATH`

### 3. Get Project Name

Ask user for project name or detect from:
- Repository directory name
- package.json `name` field
- pyproject.toml `[project] name`
- Cargo.toml `[package] name`

Store as: `PROJECT_NAME`

### 4. Show Summary

```
═══════════════════════════════════════════════
Minimal Adapter Bootstrap

Location: {ADAPTER_DIR}/FDD-Adapter/
Project: {PROJECT_NAME}
Extends: {RELATIVE_PATH}

Files to create:
  - AGENTS.md (minimal, no specs)

Note: Specs will be added later through:
  - Design workflow triggers
  - Manual updates (adapter-manual)
  - Auto-scan (adapter-auto)
═══════════════════════════════════════════════

Proceed? [Yes] [No] [Change Location]
```

### 5. Create Directory

```bash
mkdir -p {ADAPTER_DIR}/FDD-Adapter/
```

### 6. Create Minimal AGENTS.md

```markdown
# FDD Adapter: {PROJECT_NAME}

**Extends**: `{RELATIVE_PATH}`
```

### 7. Verify

Check:
- Directory exists: `{ADAPTER_DIR}/FDD-Adapter/`
- File exists: `{ADAPTER_DIR}/FDD-Adapter/AGENTS.md`
- File contains: `**Extends**: {RELATIVE_PATH}`

### 8. Run Validation

**Execute**: `adapter-validate` workflow

```yaml
Validation will:
  1. Locate adapter
  2. Detect Phase 1 (Bootstrap)
  3. Check 3 requirements:
     - AGENTS.md exists ✓
     - Project name heading ✓
     - Extends declaration ✓
  4. Score: 100/100
  5. Output to chat
```

Expected result:
```
## Validation: FDD Adapter (Bootstrap)

Location: {ADAPTER_DIR}
Phase: Bootstrap (Minimal)
Score: 100/100
Status: PASS ✅

Minimal adapter validated. No specs required yet.
```

---

## Validation

Automatically runs `adapter-validate` at completion

---

## Next Steps

**Recommended**:
- `business-context` - Start business requirements
- `design` - Start architecture design
  - When design completed → Adapter evolution triggered
  
**Optional**:
- `adapter-auto` - Scan project for existing patterns (if codebase exists)
- `adapter-manual` - Manually add specifications

---

## Examples

### Example Output

```
✓ Created: guidelines/FDD-Adapter/
✓ Created: guidelines/FDD-Adapter/AGENTS.md

Content:
# FDD Adapter: Acronis MCP Server

**Extends**: `../FDD/AGENTS.md`

Validation: 100/100 (PASS)

Next: Run 'design' workflow to start architecture design
```
