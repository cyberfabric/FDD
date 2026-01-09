---
description: Complete feature quality assurance
---

# Feature Quality Assurance

**Type**: Validation  
**Role**: QA Engineer  
**Artifact**: QA report (output to chat)

---

## Requirements

**ALWAYS open and follow**:
- `../requirements/feature-design-structure.md` (test scenarios)
- `../requirements/feature-changes-structure.md` (changes structure)
- `{adapter-directory}/FDD-Adapter/specs/testing.md` (test requirements)

Extract:
- Test scenarios from feature DESIGN.md Section G
- Change validation requirements
- Adapter test requirements

---

## Prerequisites

**MUST validate**:
- [ ] All changes implemented - validate: All changes in CHANGES.md marked COMPLETED
- [ ] Feature DESIGN.md validated
- [ ] CHANGES.md validated

---

## Steps

### 1. Orchestrate Validations

**Run in sequence**:
1. `feature-validate` - Validate feature DESIGN.md still valid
2. `feature-changes-validate` - Validate CHANGES.md consistency
3. `feature-change-validate` for each change - Validate all implementations

Store all validation results

### 2. Execute Test Scenarios

From feature DESIGN.md Section G:
- Run each acceptance test scenario
- Verify edge cases
- Check error handling

Mark scenarios: ✅ PASS | ❌ FAIL

### 3. Run Integration Tests

Per adapter testing requirements:
- Run integration test suite
- Check E2E scenarios
- Verify external integrations

### 4. Calculate Overall Score

Aggregate:
- Feature design validation score
- Changes validation score
- Per-change validation scores (average)
- Test scenario pass rate
- Integration test pass rate

**Formula**: 
- Design: 20%
- Changes: 15%
- Per-change validations: 35%
- Test scenarios: 20%
- Integration tests: 10%

### 5. Output QA Report to Chat

**Format**:
```markdown
## QA Report: Feature ({feature-slug})

**Overall Score**: {X}/100  
**Status**: PASS | FAIL  
**Threshold**: ≥95/100

---

### Validation Results

**Feature Design**: {score}/100 - {PASS|FAIL}
**Changes Plan**: {score}/100 - {PASS|FAIL}
**Change Implementations**: {avg score}/100 ({X}/{total} passed)

---

### Test Results

**Test Scenarios**: {X}/{total} passed ({percentage}%)
- ✅ | ❌ {scenario}

**Integration Tests**: {X}/{total} passed
- ✅ | ❌ {test suite}

---

### Quality Metrics

**Code Coverage**: {X}%
**Linter Issues**: {count}
**Build Status**: ✅ | ❌

---

### Recommendations

**Critical Issues**:
1. {Issue}

**Improvements**:
1. {Suggestion}

```

---

## Validation

Self-validating workflow

---

## Next Steps

**If PASS**:
1. Update FEATURES.md: Mark feature status as COMPLETE
2. If more features exist: `feature` workflow (design next feature)
3. If all features complete: Project complete ✅

**If FAIL**:
- Failed validations: Re-run corresponding workflow
- Failed tests: Fix code, re-run `feature-change-validate`
- Failed scenarios: Review requirements, update if needed
