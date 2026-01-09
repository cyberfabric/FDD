# FDD Core: Requirements File Structure

**Version**: 1.0  
**Purpose**: Define structural requirements for FDD requirements files  
**Scope**: All files in `FDD/requirements/*.md`

---

## Overview

**Requirements files** - Structure definitions and validation criteria for FDD artifacts

**This file defines**: Structure and content requirements for requirements files

**Applies to**: All files in `FDD/requirements/*.md`

---

## File Structure

### Required Header

**MUST have**:
```markdown
# {Artifact} Structure Requirements

**Version**: {version}  
**Purpose**: Define structure for {artifact}  
**Scope**: All {artifact-type} files
```

### Required Sections

**MUST contain**:

1. **Overview** - What artifact, who uses, when applies
2. **Structure** - Required sections, format, organization
3. **Validation Criteria** - Scoring breakdown, thresholds, pass/fail
4. **Examples** - Valid and invalid examples
5. **References** - Related files with action-gated WHEN conditions

---

## Structure Section

**MUST define**:
- Required sections with numbering
- Section content requirements
- ID formats (if applicable)
- File organization

**Format**:
```markdown
## Structure

### Section A: {Name}

**MUST contain**: {requirements}

**Format**: {description}

**Example**:
```{artifact}
{valid example}
```
```

---

## Validation Criteria Section

**MUST include**:

1. **Scoring breakdown** - Points per criterion
2. **Pass threshold** - Minimum score to pass
3. **Validation categories** - Structure, Completeness, Clarity, Integration

**Format**:
```markdown
## Validation Criteria

### Structure ({points} points)

**Check**:
- [ ] {criterion 1}
- [ ] {criterion 2}

### Completeness ({points} points)

**Check**:
- [ ] {criterion 1}
- [ ] {criterion 2}

### Clarity ({points} points)

**Check**:
- [ ] {criterion 1}
- [ ] {criterion 2}

### Integration ({points} points)

**Check**:
- [ ] {criterion 1}
- [ ] {criterion 2}

**Total**: {sum}/100

**Pass threshold**: ≥{threshold}/100
```

**Scoring guidelines**:
- Use standard breakdown: Structure (20-25), Completeness (25-30), Clarity (20-25), Integration (15-20)
- Total MUST equal 100 points
- Threshold typically ≥95 for requirements files

---

## Examples Section

**MUST provide**:

1. **Valid example** - Shows correct structure
2. **Invalid example** - Shows what to avoid
3. **Explanation** - Why valid/invalid

**Format**:
```markdown
## Examples

**Valid {artifact}**:
```{artifact}
{complete valid example}
```

**Invalid {artifact}**:
```{artifact}
{example with issues}
```

**Issues**: {explanation of what's wrong}
```

---

## Style Requirements

**Language**: Imperative | MUST/SHOULD/MAY | Clear criteria

**Formatting**: Markdown | Code blocks | Tables for scoring

**Completeness**: No placeholders | All examples filled | All sections present

---

## Token Limits

**Requirements files**: Soft ≤3,000 | Hard ≤4,000 tokens

**If exceeded**: Extract common patterns | Use tables | Reference other files

---

## Validation Criteria

| Criterion | Requirements | Points |
|-----------|--------------|--------|
| **Structure** | Header, Overview, Structure section, Validation section, Examples, References | 25 |
| **Completeness** | All sections filled, Scoring totals 100, Examples complete, No placeholders | 30 |
| **Clarity** | Imperative language, Clear criteria, Unambiguous scoring | 25 |
| **Integration** | References correct, Consistent with core.md, Follows FDD principles | 20 |

**Pass threshold**: ≥95/100

---

## Common Patterns

### ID Format Definitions

**When artifact uses IDs**:
```markdown
**ID Format**: `{PREFIX}-{context}-{number}`

**Example**: `REQ-FUNC-001`

**Rules**:
- PREFIX: {description}
- Context: {description}
- Number: 3-digit zero-padded
```

### Section Format

**For structured sections**:
```markdown
### Section {Letter}: {Name}

**MUST contain**: {list}

**Format**:
- {Item 1}: {description}
- {Item 2}: {description}
```

---

## Examples

**Valid requirements file**:
```markdown
# Feature Design Structure Requirements

**Version**: 1.0  
**Purpose**: Define structure for feature DESIGN.md  
**Scope**: All feature DESIGN.md files

---

## Overview

**Feature DESIGN.md** - Technical design for individual features

## Structure

### Section A: Overview

**MUST contain**: Feature name, Brief description, Reference to FEATURES.md

## Validation Criteria

### Structure (25 points)
- [ ] All required sections present
- [ ] Correct section order

### Completeness (30 points)
- [ ] No placeholders
- [ ] All flows documented

**Total**: 100/100
**Pass threshold**: ≥100/100
```

**Invalid requirements file**:
```markdown
# Feature Design

This file describes feature design structure.

You should include these sections...
```

**Issues**: No version, suggestive language, no validation criteria

---

## References

**This file is referenced by**:
- ALWAYS open and follow `core.md` WHEN creating or modifying requirements files
- All requirements files ALWAYS follow this structure

**References**:
- `core.md` - Core FDD principles
- `core-workflows.md` - Workflow structure (different from requirements)
- `core-agents.md` - AGENTS.md structure (different from requirements)
