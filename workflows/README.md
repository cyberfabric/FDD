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

**Status**: ✅ All 21 workflows complete

**Quick Start**: See `AGENTS.md` for workflow selection decision tree and common sequences

### Phase 0: Adapter Setup

**adapter.md** - Create or update FDD adapter
**adapter-from-sources.md** - Extract adapter from existing codebase (legacy integration)
**adapter-agents.md** - Generate AI agent config from adapter
**adapter-validate.md** - Validate adapter structure

### Phase 1: Business & Architecture Design

**business-context.md** - Create or update business context document
**business-validate.md** - Validate business context

**design.md** - Create or update overall design
**design-validate.md** - Validate overall design

**adr.md** - Create or update Architecture Decision Records
**adr-validate.md** - Validate ADRs

### Phase 2: Feature Planning

**features.md** - Create or update features manifest
**features-validate.md** - Validate features manifest

**feature.md** - Create or update feature design
**feature-validate.md** - Validate feature design

### Phase 3: Feature Implementation

**feature-changes.md** - Create or update implementation plan (CHANGES.md)
**feature-changes-validate.md** - Validate implementation plan

**feature-change-implement.md** - Implement specific change
**feature-code-validate.md** - Validate feature code implementation

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
cat /FDD/workflows/01-init-project.md

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
workflow = parse_markdown("/FDD/workflows/01-init-project.md")
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
