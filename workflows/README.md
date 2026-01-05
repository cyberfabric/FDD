# FDD Workflows (IDE & Agent Agnostic)

**Version**: 1.0  
**Purpose**: Universal workflow guides that can be adapted to any IDE, AI agent, or manual execution

---

## Overview

These workflows are **IDE and agent-agnostic** - they describe the FDD methodology steps in a universal format that can be:

1. **Executed manually** by developers following step-by-step instructions
2. **Converted to IDE-specific workflows** (Windsurf, VS Code, Cursor, etc.)
3. **Used by AI agents** as structured prompts
4. **Automated** in CI/CD pipelines

---

## Workflow Categories

**Status**: ✅ All 15 workflows complete (13 core + 2 legacy integration)

**Quick Start**: See `AGENTS.md` for workflow selection decision tree and common sequences

### Phase 0: Legacy Integration

0a. ✅ **`adapter-config-from-code.md`** - Context extension for `adapter-config.md` (propose formats from code)
0b. ✅ **`01-init-project-from-code.md`** - Context extension for `01-init-project.md` (propose answers from code)

### Phase 1: Architecture Design

1. ✅ **`01-init-project.md`** - Initialize FDD project structure (greenfield)
2. ✅ **`02-validate-architecture.md`** - Validate Overall Design

### Phase 2: Feature Planning

3. ✅ **`03-init-features.md`** - Generate features from Overall Design
4. ✅ **`04-validate-features.md`** - Validate FEATURES.md manifest
5. ✅ **`05-init-feature.md`** - Initialize single feature
6. ✅ **`06-validate-feature.md`** - Validate Feature Design

### Phase 3: Feature Implementation

7. ✅ **`07-complete-feature.md`** - Mark feature as complete
8. ✅ **`08-fix-design.md`** - Fix design issues during implementation
9. ✅ **`09-openspec-init.md`** - Initialize OpenSpec for feature
10. ✅ **`10-openspec-change-implement.md`** - Implement OpenSpec change
11. ✅ **`11-openspec-change-complete.md`** - Complete and archive change
12. ✅ **`12-openspec-change-next.md`** - Create next change from DESIGN.md
13. ✅ **`13-openspec-validate.md`** - Validate OpenSpec structure

---

## Workflow Format

Each workflow follows this **requirement-oriented** structure:

```markdown
# {Workflow Name}

**Phase**: {1, 2, or 3}
**Purpose**: {One-line description}

## Prerequisites

- Condition 1
- Condition 2

## Input Parameters

- **{param-name}**: Description (type, constraints)

## Requirements

### 1. {Requirement Title}

**Requirement**: What must be accomplished

**Required Content/Actions**:
- Specific requirement 1
- Specific requirement 2

**Expected Outcome**: What state is achieved

**Validation Criteria**:
- How to verify requirement met
- Measurable success indicators

### 2. {Next Requirement}

...

## Completion Criteria

- [ ] Criterion 1 met
- [ ] Criterion 2 met

## Common Challenges

- **Challenge**: Description
- **Resolution**: Approach to resolve

## Next Activities

After completion:
- Next workflow to execute
- Additional steps
```

**Key Principles**:
- **No OS Commands**: Workflows describe requirements, not implementation
- **Platform Agnostic**: Works for any OS, any tooling
- **Requirement Focused**: What needs to be done, not how
- **Validation Oriented**: Clear criteria for completion

---

## Key Principles

### 1. Requirement-Oriented

**Focus**: What needs to be accomplished, not how to accomplish it

**Workflows Describe**:
- Required outcomes
- Validation criteria
- Success indicators
- Completion state

**Workflows Do NOT Contain**:
- OS-specific commands (bash, PowerShell, etc.)
- Tool-specific scripts
- Implementation details
- Platform assumptions

### 2. Platform-Agnostic

Workflows work for:
- Any operating system (Linux, macOS, Windows)
- Any tooling ecosystem
- Any automation framework
- Manual or automated execution

### 3. Implementation-Independent

Users/teams create their own:
- Scripts matching their tech stack
- Automation matching their tools
- Workflows matching their IDE
- Processes matching their culture

### 4. Validation-Focused

Every requirement includes:
- Clear success criteria
- Measurable outcomes
- Verification approach
- Completion indicators

---

## Framework Adaptation

Universal workflows are framework-agnostic. Projects should:

1. **Create Project Adapter**: Define framework-specific patterns
   - Directory structures
   - Build commands
   - Testing approaches
   - Validation rules

2. **Extend Workflows**: Add framework notes where needed
   - Keep universal workflows unchanged
   - Document extensions in project adapter

**Example Pattern**:
```markdown
**Action**: Create module structure

**Commands** (universal):
\`\`\`bash
mkdir -p src/{domain,infrastructure,api}
\`\`\`

**Note**: See project adapter documentation for framework-specific structure
```

---

## Usage Examples

### Manual Execution

```bash
# 1. Open workflow
cat guidelines/FDD/workflows/01-init-project.md

# 2. Follow steps
mkdir -p architecture/features
cat > architecture/DESIGN.md << EOF
...
EOF

# 3. Verify
ls -la architecture/
```

### AI Agent

```python
workflow = parse_markdown("guidelines/FDD/workflows/01-init-project.md")
for step in workflow.steps:
    execute(step.commands)
    validate(step.expected_result)
```

---

## Maintenance

### When to Update

- Core FDD methodology changes
- New validation requirements
- Best practices evolve
- Community feedback

### Version Control

Workflows are versioned with FDD:
- Current: v2.1
- Track changes in git
- Document breaking changes

---

## See Also

- **Overview**: `../README.md` - Architecture, core concepts, quick start
- **AI Agent Instructions**: `../AGENTS.md` - Complete methodology for AI agents
- **FDL Specification**: `../FDL.md` - FDD Description Language (flows, algorithms, states)
