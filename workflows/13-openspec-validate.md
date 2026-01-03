# Validate OpenSpec Structure

**Phase**: 3 - Feature Development  
**Purpose**: Validate OpenSpec directory structure and specifications consistency

---

## Prerequisites

- OpenSpec initialized for feature
- Feature directory exists: `architecture/features/feature-{slug}/`

## Input Parameters

- **slug**: Feature identifier (lowercase, kebab-case)

---

## Requirements

### 1: Run OpenSpec Validation

**Requirement**: Use OpenSpec tool to validate entire structure

**Command**:
```bash
cd architecture/features/feature-{slug}/
openspec validate
```

**What This Validates**:
- Directory structure (specs/, changes/ exist)
- All active changes have required files
- Change numbering is sequential
- Status consistency across files
- Spec files are valid markdown
- No empty or malformed files
- Source of truth integrity

**Expected Outcome**: Validation passes with no errors

**Resolution if Failed**: Fix reported issues, then re-run validation

---

### 2: Review Validation Results

**Requirement**: Understand and address any validation issues

**OpenSpec Output Shows**:
- ✅ Passed checks (green)
- ⚠️  Warnings (yellow) 
- ❌ Errors (red)

**Common Issues**:
- Missing files → Create required files
- Empty specs → Fill in specifications
- Status mismatch → Sync status across files
- Numbering gaps → Renumber changes sequentially
- Invalid markdown → Fix spec file format

**Expected Outcome**: All errors resolved, warnings reviewed

---

### 3: List Changes with OpenSpec

**Requirement**: Verify change status and progress

**Commands**:
```bash
# List active changes
openspec list

# List archived changes
openspec list --archived

# Show specific change
openspec show {change-id}
```

**What to Verify**:
- Active changes listed correctly
- Status is accurate for each
- Archived changes properly moved
- No orphaned or lost changes

**Expected Outcome**: Complete and accurate change inventory

---

### 4: Verify Specs Integrity

**Requirement**: Ensure source of truth specs are valid

**What OpenSpec Checks**:
- All specs in `specs/` directory
- Specs are valid markdown
- Source attribution present
- No duplicate or conflicting specs

**Manual Review** (if needed):
- Check specs make sense
- Verify technical accuracy
- Confirm completeness

**Expected Outcome**: Source of truth is reliable

---

### 5: Generate Validation Report

**Requirement**: Document validation results

**Command**:
```bash
openspec validate --report
```

**Report Contains**:
- Validation timestamp
- Structure status
- Active changes count and list
- Archived changes count
- Source of truth spec count
- All validation checks results
- Any warnings or errors

**Report Location**: `openspec/VALIDATION_REPORT.md` (auto-generated)

**Expected Outcome**: Complete audit trail of validation

---

## Validation Scoring

**Target Score**: All checks must pass (100%)

**Validation Categories**:
1. **Structure** (30 points)
   - Directory structure exists and valid
   - Required directories present (specs/, changes/)
   - Archive structure correct

2. **Changes** (30 points)
   - All changes have required files (proposal.md, tasks.md, specs/)
   - Change numbering sequential
   - Status consistent across files

3. **Specifications** (30 points)
   - Spec files valid markdown
   - Source of truth specs valid
   - No conflicting or duplicate specs

4. **Integrity** (10 points)
   - No orphaned files
   - No broken references
   - Validation report generated

**Pass Criteria**: 100/100 (all checks must pass)

---

## Completion Criteria

Validation complete when:

- [ ] Directory structure valid (30 pts)
- [ ] All changes have proposal.md, tasks.md, specs/ (30 pts)
- [ ] Change numbering sequential
- [ ] Status consistent across files
- [ ] Spec files valid markdown (30 pts)
- [ ] Source of truth specs valid
- [ ] No critical orphaned files (10 pts)
- [ ] Validation report generated
- [ ] Score: 100/100

---

## Common Challenges

### Issue: Missing Required Files

**Resolution**: Create missing files following templates in `09-openspec-init.md`

### Issue: Status Mismatch

**Resolution**: Synchronize status across proposal.md and tasks.md

### Issue: Empty Spec Files

**Resolution**: Fill in specs or remove empty files

---

## When to Run

**Regular Validation**:
- Before completing a change
- Before completing a feature
- During code review

**Troubleshooting**:
- When OpenSpec structure seems corrupted
- After manual changes to openspec/
- When merging branches

---

## Next Activities

After validation:

1. **Fix Issues**: Address any errors or warnings

2. **Continue Work**: If validation passes
   - Continue implementation
   - Complete changes

3. **Report**: Share validation report with team if needed

---

## References

- **Core FDD**: `../AGENTS.md` - OpenSpec integration
- **OpenSpec**: https://openspec.dev - Framework docs
- **Init Workflow**: `09-openspec-init.md` - Structure templates
