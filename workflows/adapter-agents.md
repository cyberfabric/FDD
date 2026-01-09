---
description: Configure or update AI agent integration for FDD
---

# Configure or Update AI Agent Integration

**Type**: Operation  
**Role**: Project Manager  
**Artifact**: AI agent configuration files

---

## Requirements

**ALWAYS open and follow**: `../requirements/adapter-structure.md` (if adapter exists)

Extract adapter conventions if available

---

## Prerequisites

**OPTIONAL**:
- [ ] Adapter exists - validate: Check `{adapter-directory}/FDD-Adapter/AGENTS.md` exists

**Can run standalone** without adapter (will use FDD defaults)

---

## Steps

### 1. Detect Mode and Agent

**Check for existing agent configs**:
- `.windsurf/rules/` or `.windsurf/` directory → Windsurf Cascade
- `.cursorrules` file → Cursor
- `.aider.conf.yml` file → Aider
- `.cascade/` directory → Other Cascade-based

**If config found**:
- UPDATE mode - Read existing config, propose updates
- Store agent type and config location

**If NOT found**:
- CREATE mode - Generate new config from scratch

**Ask user**:
**Question 1**: Which AI agent to configure/update?

**Options**:
1. Windsurf Cascade (recommended)
2. Cursor
3. Aider
4. Both Windsurf + Cursor
5. Other (specify name)

**CREATE mode**: Propose detected agent or Windsurf (most common)
**UPDATE mode**: Show detected agent, ask to confirm or change

Store as: `AGENT_TYPE`

### 2. Mode-Specific Actions

**CREATE Mode**:
- Proceed to Step 3 for configuration structure questions

**UPDATE Mode**:
- Read existing configuration files
- Extract current settings:
  - Configuration path and structure
  - Content style (minimal/full)
  - Workflow-specific files (if any)
  - Adapter integration status
- Ask user: What to update?
  - Change agent type
  - Change content style (minimal ↔ full)
  - Add/remove workflow-specific files
  - Update adapter references
  - Regenerate all configs
- Proceed to Step 3 with targeted questions

### 3. Query Agent Configuration Structure

**Ask user**:
**Question 2**: What is the configuration structure for {AGENT_TYPE}?

**Context**: Different agents have different config conventions. Examples:
- Windsurf: `.windsurf/rules/` directory with files inside
- Cursor: `.cursorrules` single file
- Aider: `.aider.conf.yml` single file
- Custom: User-defined structure

**Prompt user to specify**:
1. Configuration path (file or directory)
2. If directory: structure inside (single file, multiple files, subdirectories)
3. File format (markdown, yaml, json, txt)

**CREATE mode**: Propose based on detected agent or common conventions
**UPDATE mode**: Show current structure, ask to change or keep

Store as:
- `CONFIG_PATH` - path to config file/directory
- `CONFIG_STRUCTURE` - single file / directory with files / directory with subdirs
- `CONFIG_FORMAT` - md / yaml / json / txt

### 4. Check Adapter Status

**If adapter exists**:
- Read adapter location from `{adapter-directory}/FDD-Adapter/AGENTS.md`
- Extract adapter path for rules
- Use adapter-specific information

**If no adapter**:
- Use FDD core rules only
- Warn: "Adapter recommended for full integration"

### 5. Query Content Preferences

**Ask user**:
**Question 3**: What content style for {AGENT_TYPE} configuration?

**Options**:
1. Minimal - Only ALWAYS open and follow instructions to AGENTS.md
2. Full - Include workflow table, navigation rules, examples
3. Custom - Specify what to include

**CREATE mode**: Propose Minimal (follows FDD principle of brevity)
**UPDATE mode**: Show current style, ask to change or keep

Store as: `CONTENT_STYLE`

**If CONTENT_STYLE = Custom, ask**:
**Question 4: What to include in configuration?**
- [ ] {{ALWAYS open and follow instructions to AGENTS.md}}
- [ ] Workflow reference table
- [ ] Workflow-specific navigation rules
- [ ] Project-specific examples
- [ ] Technology stack summary
- [ ] Other (specify)

Store as: `CONTENT_SECTIONS`

### 6. Query Workflow-Specific Files

**If CONFIG_STRUCTURE = directory with files or subdirs**:

**Ask user**:
**Question 5**: Create separate workflow-specific files?

**Context**: Some agents support workflow-specific configs in subdirectories.
Example: `.windsurf/workflows/business.md`, `.windsurf/workflows/feature.md`

**Options**:
1. No - Single main config file only
2. Yes - Create workflow-specific files for common workflows
3. Custom - Specify which workflows need separate files

**CREATE mode**: Propose No (start minimal)
**UPDATE mode**: Show current setting, ask to add/remove or keep

Store as: `WORKFLOW_SPECIFIC`

### 7. Generate Configuration Content

**CREATE mode**: Generate complete new configuration

**UPDATE mode**: Update specific config files based on changes

**Based on CONTENT_STYLE**:

**Minimal**:
```markdown
# FDD Rules

ALWAYS open and follow `guidelines/FDD/WORKFLOW.md` for workflow system.

ALWAYS open and follow `{adapter-path}/AGENTS.md` for project conventions.

Check `{workflows-path}` before starting tasks.
```

**Full**:
```markdown
# FDD Rules

ALWAYS open and follow `guidelines/FDD/WORKFLOW.md` for workflow system.
ALWAYS open and follow `{adapter-path}/AGENTS.md` for project conventions.

## Quick Workflow Reference
[Table with workflows from WORKFLOW.md]

## Workflow-Specific Navigation
[Navigation rules from workflow examples]

## Project Context
[From adapter if exists]
```

**Custom**:
Generate based on `CONTENT_SECTIONS` selections

### 8. Prepare File Structure

**Based on CONFIG_STRUCTURE**:

**Single file**:
- Path: `{CONFIG_PATH}`
- Content: Generated config content

**Directory with single file**:
- Directory: `{CONFIG_PATH}/`
- Main file: `{CONFIG_PATH}/main.{CONFIG_FORMAT}` or agent-specific name
- Content: Generated config content

**Directory with multiple files**:
- Directory: `{CONFIG_PATH}/`
- Main file: `{CONFIG_PATH}/main.{CONFIG_FORMAT}`
- Workflow files (if WORKFLOW_SPECIFIC = Yes):
  - `{CONFIG_PATH}/workflows/business.{CONFIG_FORMAT}`
  - `{CONFIG_PATH}/workflows/architecture.{CONFIG_FORMAT}`
  - `{CONFIG_PATH}/workflows/features.{CONFIG_FORMAT}`
  - `{CONFIG_PATH}/workflows/implementation.{CONFIG_FORMAT}`

### 9. Summary and Confirmation

**Show configuration summary**:

```
Agent Configuration Summary:

Mode: {CREATE/UPDATE}
Agent Type: {AGENT_TYPE}
Configuration Path: {CONFIG_PATH}
Configuration Structure: {CONFIG_STRUCTURE}
Configuration Format: {CONFIG_FORMAT}
Content Style: {CONTENT_STYLE}
Workflow-Specific Files: {WORKFLOW_SPECIFIC}

Files to be created/updated:
{list all files with paths}

Adapter Integration: {YES/NO} ({adapter-path if exists})

{UPDATE mode}: Changes summary

Content Preview:
{show first 20 lines of main config}
```

**Ask user**: Proceed? [yes/no/modify]

- **yes** - Create/update all files as shown
- **no** - Cancel workflow
- **modify** - Go back and change specific answers (specify which question)

### 10. Create or Update Files

**CREATE Mode**:
1. Create directories if needed
2. Create main config file with generated content
3. Create workflow-specific files (if applicable)

**UPDATE Mode**:
1. Update existing config files with new content
2. Create new workflow-specific files if added
3. Remove workflow-specific files if requested
4. Preserve unchanged files

After operation:
- Verify all files exist
- Show created/updated file paths

### 11. Test Integration

**Recommend to user**:
```
Test AI agent integration:
1. Restart {AGENT_TYPE} (if needed)
2. Ask agent: "What workflows are available?"
3. Agent should reference FDD/WORKFLOW.md
4. Ask agent: "I want to define business requirements"
5. Agent should suggest `business-context` workflow
6. Verify agent reads adapter conventions (if adapter exists)
```

---

## Configuration Examples

### Windsurf Cascade - Minimal
**Structure**: `.windsurf/rules/` directory
**File**: `.windsurf/rules/main.md`
```markdown
# FDD Rules

ALWAYS open and follow `guidelines/FDD/WORKFLOW.md` for workflow system.

ALWAYS open and follow `guidelines/FDD-Adapter/AGENTS.md` for project conventions.

Check `.windsurf/workflows/` before starting tasks.
```

### Cursor - Minimal
**Structure**: Single file
**File**: `.cursorrules`
```markdown
# FDD Rules

ALWAYS open and follow guidelines/FDD/WORKFLOW.md for workflow system.
ALWAYS open and follow guidelines/FDD-Adapter/AGENTS.md for project conventions.
```

### Windsurf Cascade - Full with Workflows
**Structure**: Directory with subdirectories
**Files**:
- `.windsurf/rules/main.md` - Main FDD rules
- `.windsurf/workflows/business.md` - Business context workflow rules
- `.windsurf/workflows/architecture.md` - Design workflow rules
- `.windsurf/workflows/features.md` - Feature workflow rules
- `.windsurf/workflows/implementation.md` - Development workflow rules

---

## Validation

**Manual validation**:
1. Agent config file(s) created
2. Contains FDD references
3. Contains workflow navigation
4. Contains adapter references (if applicable)

**Functional validation**:
- Ask agent about workflows
- Agent should reference FDD system
- Agent should suggest appropriate workflow

---

## Next Steps

**Configuration complete**:
- AI agent now FDD-aware
- Will suggest workflows automatically
- Will reference adapter conventions

**Start FDD work**:
- `business-context` - Define business requirements
- `adapter` - Configure adapter (if not yet done)
