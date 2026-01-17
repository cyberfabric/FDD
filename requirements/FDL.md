<!-- @fdd-change:fdd-fdd-feature-core-methodology-change-agents-navigation:ph-1 -->
# FDL - FDD Description Language

**Version**: 1.1  
**Purpose**: Define syntax and grammar for behavior description language  
**Scope**: Actor Flows, Algorithms, State Machines

---

**ALWAYS open and follow**: `core.md` WHEN editing this file

## Overview

**FDL** - Plain English behavior description using markdown lists and bold keywords

**Format**: Numbered markdown lists (1, 2, 3...) + Bold keywords + Plain English

**No code syntax**: FDL is language-agnostic, implementation-independent

---

## Core Rules

1. ✅ Use markdown numbered lists only
2. ✅ Bold keywords for control flow
3. ✅ Plain English descriptions
4. ✅ Indent nested steps
5. ❌ No code syntax ever

---

## Phase + Implementation Status (Mandatory)

**Every FDL step line MUST include**:

- Implementation checkbox: `[ ]` (not implemented) or `[x]` (implemented)
- Phase token: `ph-{N}` (N is an integer)
- Instruction ID token: `inst-{short-id}` (kebab-case, stable across renumbering)

**Required format**:

- Numbered step: 1. [ ] - `ph-1` - {instruction} - `inst-some-job`
- Nested numbered step:    1. [ ] - `ph-1` - {instruction} - `inst-some-job`
- Bullet step (e.g. under PARALLEL): - [ ] - `ph-1` - {instruction} - `inst-some-job`

**Rules**:

- `ph-{N}` MUST be present on every step line (default is `ph-1`)
- `inst-{short-id}` MUST be present on every step line
- `inst-{short-id}` MUST be unique within its scope (a single flow, algorithm, state machine, or testing scenario)
- Authors MAY change phase numbers only on existing phase tokens (do not invent new syntax)

---

## Basic Format

**Algorithm: [Name]**

Input: [parameters]  
Output: [result]

1. [ ] - `ph-1` - [Step description] - `inst-step-one`
2. [ ] - `ph-1` - [Step description] - `inst-step-two`
3. [ ] - `ph-1` - **RETURN** [result] - `inst-return-result`

**That's it!** No complex syntax needed.

---

## Control Flow Keywords

### IF/ELSE IF/ELSE

1. [ ] - `ph-1` - [Step] - `inst-step`
2. [ ] - `ph-1` - **IF** [condition]: - `inst-if`
   1. [ ] - `ph-1` - [Nested step] - `inst-if-nested`
3. [ ] - `ph-1` - **ELSE IF** [condition]: - `inst-else-if`
   1. [ ] - `ph-1` - [Nested step] - `inst-else-if-nested`
4. [ ] - `ph-1` - **ELSE**: - `inst-else`
   1. [ ] - `ph-1` - [Nested step] - `inst-else-nested`

### FOR EACH

1. [ ] - `ph-1` - [Step] - `inst-step`
2. [ ] - `ph-1` - **FOR EACH** item in collection: - `inst-for-each`
   1. [ ] - `ph-1` - [Process item] - `inst-process-item`
3. [ ] - `ph-1` - [Next step] - `inst-next-step`

### WHILE

1. [ ] - `ph-1` - [Step] - `inst-step`
2. [ ] - `ph-1` - **WHILE** [condition]: - `inst-while`
   1. [ ] - `ph-1` - [Process] - `inst-while-body`
3. [ ] - `ph-1` - [Next step] - `inst-next-step`

### TRY/CATCH

1. [ ] - `ph-1` - **TRY**: - `inst-try`
   1. [ ] - `ph-1` - [Operation that may fail] - `inst-try-op`
2. [ ] - `ph-1` - **CATCH** [ErrorType]: - `inst-catch`
   1. [ ] - `ph-1` - [Handle error] - `inst-handle-error`
3. [ ] - `ph-1` - [Continue] - `inst-continue`

### PARALLEL

1. [ ] - `ph-1` - [Prepare] - `inst-prepare`
2. [ ] - `ph-1` - **PARALLEL**: - `inst-parallel`
   - [ ] - `ph-1` - [Task 1] - `inst-parallel-task-1`
   - [ ] - `ph-1` - [Task 2] - `inst-parallel-task-2`
   - [ ] - `ph-1` - [Task 3] - `inst-parallel-task-3`
3. [ ] - `ph-1` - Wait for completion - `inst-wait`
4. [ ] - `ph-1` - [Combine results] - `inst-combine-results`

### MATCH (Pattern Matching)

1. [ ] - `ph-1` - [Get value] - `inst-get-value`
2. [ ] - `ph-1` - **MATCH** [value]: - `inst-match`
   - [ ] - `ph-1` - **CASE** [pattern]: [Action] - `inst-case-1`
   - [ ] - `ph-1` - **CASE** [pattern]: [Action] - `inst-case-2`
   - [ ] - `ph-1` - **DEFAULT**: [Action] - `inst-default`
3. [ ] - `ph-1` - [Continue] - `inst-continue`

### GO TO / SKIP TO

1. [ ] - `ph-1` - [Step] - `inst-step`
2. [ ] - `ph-1` - **IF** [condition]: - `inst-if`
   1. [ ] - `ph-1` - **GO TO** step N - `inst-go-to`
3. [ ] - `ph-1` - [Step] - `inst-next-step`
4. [ ] - `ph-1` - **SKIP TO** step N - `inst-skip-to`

### RETURN (Early Exit)

1. [ ] - `ph-1` - [Step] - `inst-step`
2. [ ] - `ph-1` - **IF** [condition]: - `inst-if`
   1. [ ] - `ph-1` - **RETURN** [value] (exit early) - `inst-return`
3. [ ] - `ph-1` - [Continue only if not returned] - `inst-continue`

---

## Example: Algorithm

**Algorithm: Enable Entity with Dependencies**

Input: entity_id, tenants, security_context  
Output: List of enabled entity IDs

1. [x] - `ph-1` - Initialize empty list: enabled_entities - `inst-init-enabled-entities`
2. [x] - `ph-1` - Load entity from registry - `inst-load-entity`
3. [x] - `ph-1` - **IF** entity not found: - `inst-if-not-found`
   1. [x] - `ph-1` - **RETURN** 404 error - `inst-return-404`
4. [ ] - `ph-2` - Update entity.enabled_for = tenants - `inst-update-enabled-for`
5. [ ] - `ph-1` - Add entity_id to enabled_entities - `inst-add-enabled-id`
6. [x] - `ph-1` - **FOR EACH** ref_id in references: - `inst-for-each-ref`
   1. [x] - `ph-1` - Load ref_entity - `inst-load-ref-entity`
   2. [ ] - `ph-2` - **IF** ref_entity not enabled: - `inst-if-ref-not-enabled`
      1. [ ] - `ph-2` - Enable ref_entity (recursive) - `inst-enable-ref-entity`
      2. [ ] - `ph-2` - Add to enabled_entities - `inst-add-ref-to-enabled`
7. [x] - `ph-1` - **TRY**: - `inst-try`
   1. [x] - `ph-1` - Commit transaction - `inst-commit`
   2. [x] - `ph-1` - Log audit trail - `inst-log-audit`
8. [ ] - `ph-1` - **CATCH** any errors: - `inst-catch`
   1. [ ] - `ph-1` - Rollback transaction - `inst-rollback`
   2. [ ] - `ph-1` - **RETURN** 500 error - `inst-return-500`
9. [ ] - `ph-1` - **RETURN** enabled_entities - `inst-return-enabled-entities`

---

## Example: Actor Flow

**Flow: Admin Creates Dashboard**

Actor: Admin  
Goal: Create new dashboard

1. [ ] - `ph-1` - User opens Dashboard page - `inst-open-dashboard-page`
2. [ ] - `ph-1` - User clicks "Create New" - `inst-click-create-new`
3. [ ] - `ph-1` - UI shows dashboard editor - `inst-show-editor`
4. [ ] - `ph-1` - User enters name and description - `inst-enter-name-and-description`
5. [ ] - `ph-1` - User clicks "Save" - `inst-click-save`
6. [ ] - `ph-1` - **API**: `POST /api/analytics/v1/gts` - `inst-api-post-gts`
   - [ ] - `ph-1` - Body: `{type: "layout.dashboard", name: "..."}` - `inst-body-layout-dashboard`
7. [ ] - `ph-1` - UI redirects to dashboard editor - `inst-redirect-to-editor`
8. [ ] - `ph-1` - User adds widgets - `inst-add-widgets`

---

## Validation Rules

### ✅ Required

- Markdown numbered lists (1, 2, 3...)
- Bold keywords: **IF**, **FOR EACH**, **WHILE**, **TRY/CATCH**, **RETURN**, **MATCH**
- Plain English descriptions
- Indentation for nested steps
- Each step line includes `[ ]` or `[x]`, `ph-{N}`, and an instruction ID token `inst-{short-id}`
- For codebase traceability, every implemented instruction marker (`...:ph-{N}:inst-...`) MUST be represented in code as a paired `fdd-begin`/`fdd-end` block wrapping non-empty code. Unwrapped single-line `...:inst-...` markers MUST NOT be used.
  - Format: `// fdd-begin fdd-{full-tag}:ph-{N}:inst-{id}` ... code ... `// fdd-end fdd-{full-tag}:ph-{N}:inst-{id}`
  - Example: `// fdd-begin fdd-project-feature-x-algo-validate:ph-1:inst-check-input`

### ❌ Prohibited

- Code examples (any language)
- Function syntax (`fn`, `function`, `async`)
- Type annotations (`: string`, `<T>`)
- Language operators (`&&`, `||`, `=>`)
- Pseudo-code syntax

### ✅ Allowed

- Variable names (no types): `entity`, `items`, `result`
- Simple notation: `entity.field`, `array[0]`
- API endpoints: `POST /api/v1/resource`
- Inline clarifications: `(condition explanation)`

---

## State Machines (Section D)

### Basic Format

**State Machine: [Entity Name]**

**States**: [ALL_STATES, COMMA_SEPARATED]

**Transitions**:
1. **FROM** [state] **TO** [state] **WHEN** [trigger]
2. **FROM** [state] **TO** [state] **WHEN** [trigger]

### With Actions

**Transition: [STATE_A] → [STATE_B]**  
**When**: [trigger]  
**Actions**:
1. [Action step]
2. [Action step]
3. **IF** [condition]:
   1. [Conditional action]

### Example

**State Machine: Order**

**States**: DRAFT, PENDING_PAYMENT, PAID, SHIPPED, DELIVERED, CANCELLED

**Transitions**:
1. **FROM** DRAFT **TO** PENDING_PAYMENT **WHEN** user submits order
2. **FROM** PENDING_PAYMENT **TO** PAID **WHEN** payment confirmed
3. **FROM** PAID **TO** SHIPPED **WHEN** order dispatched
4. **FROM** SHIPPED **TO** DELIVERED **WHEN** delivery confirmed
5. **FROM** DRAFT **TO** CANCELLED **WHEN** user cancels

---

## Excluding Examples from Validation

**Purpose**: Documentation and workflow files often contain **example** FDD tags that should not be validated as real implementation.

**Solution**: Use `!no-fdd-begin` / `!no-fdd-end` block markers to exclude content from FDD scanning.

**Syntax**:

- Markdown/HTML comments: `<!-- !no-fdd-begin -->` ... `<!-- !no-fdd-end -->`
- Code comments (Python): `# !no-fdd-begin` ... `# !no-fdd-end`
- Code comments (Rust/C++): `// !no-fdd-begin` ... `// !no-fdd-end`

**Behavior**:

- Everything between markers is **completely ignored** by the validator
- Unmatched `!no-fdd-begin` (without closing `!no-fdd-end`) excludes everything to end of file
- Nested exclusion blocks are supported
- This is different from single-line `!no-fdd` which only excludes one line

**Use Cases**:

1. **Documentation examples**: Wrap example FDD tags in docs with exclusion blocks
2. **Deprecated code**: Mark old code that still has FDD tags but shouldn't be validated
3. **Template/boilerplate code**: Exclude scaffolding/template code from validation

**Example**:

```markdown
Real implementation:
<!-- fdd-begin fdd-myproject-feature-x-flow-y:ph-1:inst-real -->
Actual workflow step
<!-- fdd-end   fdd-myproject-feature-x-flow-y:ph-1:inst-real -->

Documentation example (excluded from validation):
<!-- !no-fdd-begin -->
```rust
// fdd-begin fdd-example-feature-z-algo-w:ph-1:inst-example
example_code();
// fdd-end   fdd-example-feature-z-algo-w:ph-1:inst-example
```
<!-- !no-fdd-end -->
```

**Important**: Use this sparingly. Most FDD tags should be real and validated. Only exclude genuine examples/documentation.

---

## Validation Criteria

### Structure (25 points)

**Check**:
- [ ] Uses numbered markdown lists (1, 2, 3...)
- [ ] Proper nesting with indentation
- [ ] Each step line includes `[ ]` or `[x]`
- [ ] Each step line includes phase token `ph-{N}` (written as inline code)
- [ ] No code blocks or function syntax
- [ ] No type annotations

### Keyword Usage (30 points)

**Check**:
- [ ] Keywords are bold (**IF**, **FOR EACH**, **WHILE**, etc.)
- [ ] Keywords used correctly (IF for conditions, FOR EACH for iterations)
- [ ] FROM/TO/WHEN used for state transitions
- [ ] TRY/CATCH used for error handling
- [ ] RETURN used for algorithm outputs

### Clarity (25 points)

**Check**:
- [ ] Plain English descriptions
- [ ] No programming language syntax (no =>, &&, ||, etc.)
- [ ] No function definitions (fn, function, async)
- [ ] Language-agnostic (implementation-independent)
- [ ] Clear and unambiguous steps

### Completeness (20 points)

**Check**:
- [ ] All flows have numbered steps
- [ ] All algorithms have Input/Output defined
- [ ] All state machines have States and Transitions defined
- [ ] No step lines missing checkbox, phase token, or instruction ID token
- [ ] No instruction tag appears in code without matching `fdd-begin`/`fdd-end` wrapping a non-empty code block
- [ ] No placeholders or TODOs
- [ ] All conditions and actions specified

**Total**: 100/100

**Pass threshold**: ≥90/100

---

## References

- ALWAYS open and follow `overall-design-structure.md` WHEN specifying behavioral sections in root DESIGN.md
- ALWAYS open and follow `feature-design-structure.md` WHEN specifying behavioral sections in feature DESIGN.md
- ALWAYS open and follow `{adapter-directory}/AGENTS.md` WHEN overriding the behavior description language
