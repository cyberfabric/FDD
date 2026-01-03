# Implement OpenSpec Change

**Phase**: 3 - Feature Development  
**Purpose**: Implement OpenSpec change according to specifications

---

## Prerequisites

- OpenSpec initialized for feature (run `09-openspec-init.md` first)
- Change directory exists: `architecture/features/feature-{slug}/openspec/changes/{id}-{name}/`
- Proposal and specs reviewed

## Input Parameters

- **slug**: Feature identifier (lowercase, kebab-case)
- **change-id**: Change number (e.g., "001", "002")

---

## Requirements

### 1: Review Change with OpenSpec

**Requirement**: Use OpenSpec to review change details

**Command**:
```bash
cd architecture/features/feature-{slug}/
openspec show {change-id}
```

**What This Shows**:
- Change status and metadata
- Proposal summary
- Tasks checklist
- Specification files

**Location**: `changes/{change-id}-{name}/`

**Required Files**:
- `proposal.md` - Change rationale
- `tasks.md` - Implementation checklist
- `specs/` - Technical specifications

**Expected Outcome**: Understanding of what needs to be implemented

**Verification**: Use `openspec list` to see all changes

---

### 2: Review All Change Documents

**Requirement**: Understand implementation requirements completely

**Review Checklist**:
- **proposal.md**: Why this change exists, what problem it solves
- **design.md** (if exists): Technical decisions and architecture
- **tasks.md**: Checklist of implementation steps
- **specs/{capability}/spec.md**: Delta specifications with requirements

**Feature Context**:
- **../../DESIGN.md**: Feature-level design (not in openspec/)
- Check Feature DESIGN.md Section F for change context

**Understanding Required**:
- Implementation scope and boundaries
- Technical requirements and constraints
- Testing criteria and verification methods
- Dependencies on other changes or components

**Expected Outcome**: Complete understanding of what needs to be implemented

**Validation Criteria**:
- Can explain change purpose in own words
- Understands all technical specifications
- Knows verification approach
- Aware of feature-level design context

---

### 3: Mark Change as Started (Manual)

**Requirement**: Manually update status to IN_PROGRESS

**Files to Update**:
- `proposal.md` - Change status header
- `tasks.md` - Change status header

**Status Change**:
```markdown
**Status**: 🔄 IN_PROGRESS
**Started**: YYYY-MM-DD
```

**Expected Outcome**: Change marked as active

**Note**: OpenSpec does not have a `start` command. Status is managed manually in files.

---

### 4: Implement According to Specs

**Requirement**: Write code following specifications

**Manual Step**: Implement the change

**Guidelines**:
- Follow specs exactly
- Implement incrementally (task by task)
- Update tasks.md checklist as you complete items
- Write tests alongside code
- Commit frequently with clear messages

---

### 5: Update Tasks Checklist

**Requirement**: Track implementation progress continuously

**Checklist Format**:
- Incomplete: `- [ ] Task description`
- Complete: `- [x] Task description`

**Update Practice**:
- Mark tasks complete as you finish them
- Update after each significant milestone
- Track overall progress (e.g., 5/10 tasks complete)

**Expected Outcome**: tasks.md accurately reflects implementation progress

**Validation Criteria**:
- Checklist updated regularly
- Completed tasks marked with [x]
- Progress is visible and trackable

---

### 6: Run Tests Continuously

**Requirement**: Verify implementation incrementally with tests

**Testing Practice**:
- Run tests after each task completion
- Verify all tests pass before moving to next task
- Add new tests as needed for new functionality
- Run both unit and integration tests

**Expected Outcome**: All tests passing continuously

**Framework Examples** (reference only):
- Rust: `cargo test`
- TypeScript/Node.js: `npm test`
- Python: `pytest`
- Java: `mvn test`
- Go: `go test`

**Validation Criteria**:
- Zero test failures
- Tests cover implemented functionality
- Test output confirms correctness

---

### 7: Verify Against Specs

**Requirement**: Ensure implementation matches all specifications

**Verification Process**:
- Review each spec file in `specs/` directory
- Compare implementation against spec requirements
- Verify all specified behaviors implemented
- Check edge cases and error handling

**Verification Checklist** (per spec):
- [ ] All requirements from spec implemented
- [ ] Implementation behavior matches spec description
- [ ] Edge cases handled as specified
- [ ] Error scenarios implemented correctly
- [ ] No scope creep beyond spec

**Expected Outcome**: Implementation fully compliant with all specs

**Validation Criteria**:
- Every spec requirement implemented
- No deviations from specifications
- Complete coverage of spec scope

---

### 8: Complete Final Checks

**Requirement**: Verify all completion criteria met

**Final Verification Checklist**:
- [ ] All tasks in tasks.md marked complete (100%)
- [ ] All tests passing
- [ ] Code compiles/builds without errors
- [ ] Implementation matches all specs
- [ ] No incomplete or TODO markers in code
- [ ] Code reviewed (if team workflow requires)

**Expected Outcome**: Change implementation fully complete

**Validation Criteria**:
- Zero incomplete tasks
- Zero test failures
- Zero compilation errors
- All specs satisfied
- Ready for completion workflow

---

### 9: Document Implementation Notes

**Requirement**: Record implementation details and decisions

**Location**: Append to `tasks.md`

**Required Information**:
- **Date Completed**: When implementation finished
- **Key Decisions**: Important technical choices and rationale
- **Challenges Encountered**: Problems faced and how resolved
- **Performance Considerations**: Any performance-related notes
- **Technical Debt**: Items to address later (if any)

**Format**:
```markdown
---

## Implementation Notes

**Date Completed**: YYYY-MM-DD

**Key Decisions**:
- Decision 1: Rationale

**Challenges Encountered**:
- Challenge 1: How resolved

**Performance Considerations**:
- Performance notes

**Technical Debt** (if any):
- Items to address later
```

**Expected Outcome**: Complete audit trail of implementation

**Validation Criteria**:
- Notes provide context for future maintainers
- Key decisions documented with rationale
- Challenges and resolutions recorded

---

## Completion Criteria

Implementation complete when:

- [ ] Proposal and specs reviewed
- [ ] Status updated to IN_PROGRESS
- [ ] All tasks in tasks.md completed (100%)
- [ ] Code implements all specifications
- [ ] All tests passing
- [ ] Implementation verified against specs
- [ ] Implementation notes documented
- [ ] Ready to complete change

---

## Common Challenges

### Issue: Specs Unclear

**Resolution**: Return to DESIGN.md, clarify requirements. May need to run `08-fix-design.md`.

### Issue: Tests Failing

**Resolution**: Debug and fix. Don't mark change complete until tests pass.

### Issue: Implementation Deviates from Spec

**Resolution**: Either fix code to match spec, or update spec if requirements changed (requires design update).

---

## Implementation Best Practices

### 1. Incremental Development

- Implement one task at a time
- Run tests after each task
- Commit frequently

### 2. Test-Driven

- Write test first when possible
- Ensure tests fail before implementation
- Verify tests pass after implementation

### 3. Spec Compliance

- Refer to specs constantly
- Don't add scope beyond specs
- If specs are wrong, update design first

### 4. Code Quality

- Follow project conventions
- Add comments for complex logic
- Keep functions focused
- Handle errors properly

### 5. When to Stop and Fix Design

**Stop Implementation If**:
- Specs are fundamentally wrong or impossible to implement
- Major design flaws discovered during implementation
- Implementation requires types/endpoints not in Overall Design
- Algorithm complexity far exceeds design estimates
- Security or architectural concerns arise

**Warning Signs**:
- Need to add >3 types not in Overall Design
- Implementation diverges significantly from design
- Core assumptions in design are invalid
- Technical debt would be severe

**Action When Stopping**:
1. Document the design issue clearly
2. Use workflow `08-fix-design.md`
3. Update Feature DESIGN.md with corrections
4. Re-validate with workflow `06-validate-feature.md`
5. Resume implementation with corrected design

**Don't Stop For**:
- Minor clarifications or typos in specs
- Small refactoring opportunities
- Edge cases not covered in design (add to notes)
- Performance optimizations (do after core implementation)

---

## Next Activities

After implementation complete:

1. **Complete Change**: Run `11-openspec-change-complete.md {slug} {change-id}`
   - Archive specs
   - Mark change done
   - Merge to source of truth

2. **Next Change** (if any):
   - Check if more changes needed
   - Initialize next change
   - Repeat cycle

3. **Complete Feature** (if last change):
   - Run `07-complete-feature.md {slug}`

---

## References

- **Core FDD**: `../AGENTS.md` - Implementation guidelines
- **OpenSpec**: https://openspec.dev - Change management
- **Next Workflow**: `11-openspec-change-complete.md`
