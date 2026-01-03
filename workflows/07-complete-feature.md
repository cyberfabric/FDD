# Complete Feature

**Phase**: 3 - Feature Development  
**Purpose**: Mark feature as complete after all implementation is done

---

## Prerequisites

- Feature is IN_PROGRESS
- All OpenSpec changes implemented and archived
- All tests passing
- Feature fully functional

## Input Parameters

- **slug**: Feature identifier (lowercase, kebab-case)

---

## Requirements

### 1: Verify All Changes Complete

**Requirement**: All OpenSpec changes must be completed and archived

**Location**: `architecture/features/feature-{slug}/openspec/`

**Validation Criteria**:
- `openspec/changes/` directory is empty (no active changes)
- All changes archived to `openspec/archive/` or merged to `openspec/specs/`
- No changes with status IN_PROGRESS or NOT_STARTED

**Tools**: Use `openspec list` to verify status

**Expected Outcome**: Zero pending OpenSpec changes

**Resolution if Failed**: Complete remaining changes using workflows 10 and 11

---

### 2: Run Final Design Validation

**Requirement**: Design validation must pass one final time

**Validation**: Execute workflow `06-validate-feature.md` for feature `{slug}`

**Expected Outcome**: Validation score 100/100 + 100% completeness

**Validation Criteria**:
- All sections A-F compliant
- No validation errors
- Design matches implementation
- All requirements met

**Resolution if Failed**: Fix design issues using workflow `08-fix-design.md` before marking complete

---

### 3: Verify Tests

**Requirement**: All feature tests must pass

**Test Coverage**:
- Unit tests for feature components
- Integration tests for feature flows
- End-to-end tests if applicable
- All test scenarios from Section F validated

**Expected Outcome**: 100% tests passing, zero failures

**Framework Examples** (reference only):
- Rust: `cargo test`
- Node.js: `npm test`
- Python: `pytest`
- Java: `mvn test`
- Go: `go test`

**Resolution if Failed**: Fix failing tests before marking complete

---

### 4: Verify Compilation/Build

**Requirement**: Code must compile/build without errors

**Validation Criteria**:
- No compilation errors
- No type errors
- No syntax errors
- All dependencies resolved
- Build process succeeds

**Expected Outcome**: Clean build with zero errors

**Framework Examples** (reference only):
- Rust: `cargo check`
- TypeScript: `tsc --noEmit`
- Python: `mypy` or `pyright`
- Java: `mvn compile`
- Go: `go build`

**Critical**: This prevents marking incomplete work as done

**Resolution if Failed**: Fix compilation errors before proceeding

---

### 5: Update FEATURES.md Status

**Requirement**: Update feature status to IMPLEMENTED

**Location**: `architecture/features/FEATURES.md`

**Status Change**: 🔄 IN_PROGRESS → ✅ IMPLEMENTED

**Update Requirements**:
- Find feature entry for `feature-{slug}`
- Change status emoji and text
- Preserve all other feature information
- Maintain formatting and links

**Expected Outcome**: Feature shows status ✅ IMPLEMENTED

**Validation Criteria**:
- Status updated correctly
- No formatting broken
- Feature still listed in correct order

---

### 6: Identify Unblocked Features

**Requirement**: Identify features that can now start

**Analysis**:
- Review this feature's "Blocks" field in `FEATURES.md` to see which features it blocks
- Check those features' "Depends On" fields to verify all dependencies are met
- Identify features that are now fully unblocked

**Expected Outcome**: List of features that are now unblocked

**Next Steps**:
- Prioritize newly unblocked features
- Verify all their dependencies are satisfied
- Start highest priority unblocked feature next

---

### 7: Verify OpenSpec Structure

**Requirement**: OpenSpec structure must be valid and complete

**Location**: `architecture/features/feature-{slug}/openspec/`

**Required Structure**:
- `specs/` directory exists (source of truth)
- `specs/` contains all merged specifications
- `changes/` directory is empty
- `archive/` contains completed changes (optional)

**Validation Criteria**:
- All changes moved from `changes/` to `archive/` or merged to `specs/`
- No orphaned files
- Structure matches OpenSpec conventions

**Expected Outcome**: Clean OpenSpec structure with all changes archived

**Tools**: Use `openspec validate` to verify structure

---

### 8: Add Completion Note

**Requirement**: Document completion in DESIGN.md

**Location**: Append to `architecture/features/feature-{slug}/DESIGN.md`

**Required Information**:
- **Completion Date**: When feature was completed
- **Change Count**: Number of OpenSpec changes implemented
- **Status**: ✅ IMPLEMENTED

**Format**:
```markdown
---

## Implementation Complete

**Date**: YYYY-MM-DD  
**All Changes**: N changes implemented and archived  
**Status**: ✅ IMPLEMENTED
```

**Expected Outcome**: Completion record added to design document

**Validation Criteria**:
- Note appended to end of file
- All required fields present
- Formatting consistent with document

---

## Completion Criteria

Feature completion verified when:

- [ ] All OpenSpec changes completed
- [ ] Design validation passes (100/100 + 100%)
- [ ] Tests passing
- [ ] Code compiles without errors
- [ ] FEATURES.md status = IMPLEMENTED
- [ ] Dependent features identified
- [ ] OpenSpec structure valid (changes archived)
- [ ] Completion note in DESIGN.md

---

## Common Challenges

### Issue: Tests Failing

**Resolution**: Fix tests before marking complete. Feature is not done if tests fail.

### Issue: OpenSpec Changes Not Archived

**Resolution**: Complete and archive remaining changes:
```bash
cd architecture/features/feature-{slug}/
openspec archive {change-id}
```

**Note**: Use `openspec archive {change-id} --yes` for non-interactive mode

---

## Next Activities

After completing feature:

1. **Review FEATURES.md**: Check for next feature to implement
   - Look at implementation order
   - Verify dependencies met

2. **Start Next Feature**: Run `05-init-feature.md {next-slug}`
   - Or start dependent feature that's now unblocked

3. **Update Documentation**: If needed
   - Update Overall Design
   - Update architecture diagrams

---

## References

- **Core FDD**: `../AGENTS.md` - Completion criteria
- **Next Workflow**: `05-init-feature.md` for next feature
