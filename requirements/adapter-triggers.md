# Adapter Evolution Triggers

**Version**: 1.0  
**Purpose**: Define when AI agent ALWAYS proposes running adapter workflow to capture technical decisions  
**Scope**: All FDD workflows that create/modify technical artifacts

**Philosophy**: Adapter evolves naturally as project progresses - agent detects changes and proposes updates

---

## Mandatory Adapter Initialization

**BEFORE any FDD workflow execution**:

ALWAYS do check that adapter exists:
- Search for `{adapter-directory}/FDD-Adapter/AGENTS.md` in common locations:
  - `guidelines/FDD-Adapter/AGENTS.md`
  - `spec/FDD-Adapter/AGENTS.md`
  - `docs/FDD-Adapter/AGENTS.md`

IF adapter NOT found:
- STOP workflow execution
- Propose: "Adapter not initialized. Run bootstrap?" [Yes]
- Run: `adapter` workflow Mode 1 (Bootstrap)
- After bootstrap: Resume original workflow

IF adapter exists (minimal or evolved):
- Continue with workflow execution

---

## Trigger Rules

Agent ALWAYS proposes running `adapter` workflow (Mode 2 Discovery or Mode 3 Evolution) WHEN:

### 1. Design Decisions Made

**Trigger**: DESIGN.md created, updated, or validated

**Check**:
- DESIGN.md Section C.2 (Domain Model) completed
- DESIGN.md Section C.3 (API Contracts) completed
- New ADRs created with technical decisions
- ADRs reference: tech stack, patterns, formats

**Scan for**:
- Tech stack changes (languages, frameworks, databases)
- Domain model format specification
- API contract format specification
- Architecture patterns

**Propose IF**:
- New ADR not reflected in adapter specs
- DESIGN.md Section C has content not in adapter
- Tech stack mentioned but not in specs/tech-stack.md

**Action**: 
```
Design completed. Technical decisions detected:
  - ADR-0001: Python/Django (not in adapter)
  - DESIGN.md C.2: JSON Schema format (not in adapter)
  
Run adapter workflow to capture these? [Yes] [No] [Review]
```

---

### 2. Feature Patterns Detected

**Trigger**: Feature DESIGN.md created or validated

**Check**:
- Feature DESIGN.md Section B (Actor Flows) completed
- Feature DESIGN.md Section C (Algorithms) completed
- Feature DESIGN.md Section E (Technical Details) completed

**Scan for**:
- Repeated patterns (algorithm appears in ≥2 features)
- Architecture patterns (Repository, Factory, Strategy, etc.)
- Code examples or pseudocode
- Technical implementation details

**Propose IF**:
- Pattern not in specs/patterns.md
- Code example worth capturing
- Technical detail is reusable

**Action**:
```
Feature pattern detected:
  - LRU caching strategy in fdd-context-provider
  
Add to adapter specs/patterns.md? [Yes] [No]
```

---

### 3. Breaking Changes

**Trigger**: CHANGES.md created with Type: BREAKING or MAJOR

**Check**:
- CHANGES.md Type field
- CHANGES.md Section F (Implementation Plan)
- Changes to API endpoints
- Changes to domain model structure

**Scan for**:
- API breaking changes
- Domain model structure changes
- Deprecated patterns
- Migration requirements

**Propose IF**:
- Breaking change affects adapter specs
- API contract format changed
- Domain model format changed
- Pattern deprecated

**Action**:
```
Breaking change detected:
  - API endpoint /v1/workflow → /v2/workflow
  
Update adapter specs + add migration guide? [Yes] [No]
```

---

### 4. Implementation Code

**Trigger**: Code committed AND tests passed

**Check**:
- New files created in src/, app/, lib/
- Tests passed (test command exit code 0)
- Code review completed (if applicable)

**Scan for**:
- Utility functions used ≥3 times
- Repeated code patterns
- Boilerplate code
- Integration code (external APIs, database)
- Deviation from conventions

**Propose IF**:
- Reusable utility detected
- Code pattern worth documenting
- Convention deviation detected

**Action**:
```
Reusable code detected:
  - retry_with_backoff() used 5 times
  
Add to adapter specs/snippets/error-handling.md? [Yes] [No]
```

---

### 5. User Decisions

**Trigger**: User explicitly states technical decision in conversation

**Detect keywords**:
- "we will use {technology}"
- "I decided to use {pattern}"
- "let's go with {framework}"
- "convention is {style}"
- User answers technical questions

**Propose IF**:
- Decision is technical (not business)
- Decision affects implementation
- Decision not yet in adapter

**Action**:
```
Technical decision detected in conversation:
  "We will use PostgreSQL 15+ for database"
  
Capture in adapter specs/tech-stack.md? [Yes] [No]
```

---

### 6. Existing Project Discovery

**Trigger**: First FDD workflow run in existing codebase

**Check**:
- Source code exists (src/, app/, lib/)
- Package manager files exist
- Adapter is minimal (only Extends) OR doesn't exist

**Scan for**:
- Documentation, ADRs, configs, code structure, API definitions, domain models

**Propose**: 
```
Existing project detected with code/docs.
  - 11 ADRs found
  - Tech stack detected: Python 3.11+, Django 4.2+
  - Code patterns detected: Layered architecture
  
Run adapter discovery to capture existing decisions? [Yes] [No]
```

---

## Detection Algorithm

```yaml
At ANY workflow step:

1. Monitor for triggers:
   - File created/updated (DESIGN.md, CHANGES.md, *.py, *.ts, etc.)
   - Validation completed (design-validate, feature-validate)
   - Tests passed
   - User stated decision

2. IF trigger detected:
   → Run trigger-specific scan
   → Check conditions
   → Build proposal

3. IF conditions met:
   → Show proposal to user
   → IF user accepts:
     → Run adapter workflow (appropriate mode)
     → Capture changes
     → Update adapter specs
   → IF user rejects:
     → Continue workflow
     → Log: "Adapter update skipped by user"

4. Continue original workflow
```

---

## Agent Responsibilities

Agent ALWAYS do:
1. ✅ Check adapter initialization before ANY workflow
2. ✅ Monitor for trigger events during workflow execution
3. ✅ Scan for candidates when trigger detected
4. ✅ Propose adapter update with clear context
5. ✅ Respect user decision (accept/reject)
6. ✅ Never silently skip adapter opportunities

Agent ALWAYS do NOT:
1. ❌ Run adapter workflow without user approval
2. ❌ Hardcode adapter calls in workflow steps
3. ❌ Skip adapter proposals to "save time"
4. ❌ Propose adapter for non-technical decisions

---

## Examples

### Example 1: Design Workflow Trigger

```
User: "Run design workflow"
Agent: Checks adapter → Found minimal adapter
Agent: Executes design workflow
Agent: DESIGN.md created with Section C completed
Agent: Trigger detected → Scans DESIGN.md + ADRs
Agent: Finds: 3 ADRs with tech stack, JSON Schema format, Markdown tables
Agent: Proposes: "Design completed. 3 technical decisions not in adapter. Capture?"
User: "Yes"
Agent: Runs adapter workflow Mode 3 (Evolution)
Agent: Creates specs/tech-stack.md, specs/domain-model.md, specs/api-contracts.md
Agent: Updates AGENTS.md with 3 MUST rules
Agent: Returns to design workflow completion
```

### Example 2: Implementation Trigger

```
Agent: Implementation completed, tests passed
Agent: Trigger detected → Scans committed code
Agent: Finds: retry_with_backoff() function used 5 times
Agent: Proposes: "Reusable retry utility detected. Add to adapter snippets?"
User: "Yes"
Agent: Runs adapter workflow Mode 3 (Evolution)
Agent: Creates specs/snippets/error-handling.md with function + usage
Agent: Updates AGENTS.md MUST rule for snippets
Agent: Returns to implementation workflow
```

### Example 3: User Decision Trigger

```
User: "Let's use FastAPI instead of Django"
Agent: Trigger detected → Tech stack decision
Agent: Proposes: "Tech stack change: FastAPI. Update adapter?"
User: "Yes"
Agent: Runs adapter workflow Mode 3 (Evolution)
Agent: Updates specs/tech-stack.md (Django → FastAPI)
Agent: Adds ADR: ADR-0012: FastAPI Migration
Agent: Returns to conversation
```

---

## Integration with Workflows

Instead of hardcoding adapter calls in each workflow, workflows reference this file:

```markdown
# Any Workflow

## Prerequisites

**ALWAYS open and follow**: `requirements/adapter-triggers.md`

Execute: Check adapter initialization
Execute: Monitor triggers during workflow

## Steps

[workflow steps here]

[At any step, if trigger detected, propose adapter update]
```

---

## Validation Criteria

### Structure (25 points)

**Check**:
- [ ] All 6 trigger types defined
- [ ] Detection algorithm present
- [ ] Agent responsibilities listed
- [ ] Integration section complete
- [ ] Proper markdown formatting

### Completeness (30 points)

**Check**:
- [ ] Each trigger has: When, Check, Scan, Propose sections
- [ ] Detection keywords specified
- [ ] Proposal format examples provided
- [ ] All workflow integration points defined
- [ ] No placeholders or TODOs

### Clarity (25 points)

**Check**:
- [ ] Trigger conditions unambiguous
- [ ] Agent actions clearly defined
- [ ] Examples concrete and realistic
- [ ] MUST/MUST NOT semantics correct
- [ ] Imperative language used

### Integration (20 points)

**Check**:
- [ ] References workflow-execution.md correctly
- [ ] References adapter-structure.md correctly
- [ ] Consistent with FDD principles
- [ ] Used by/References sections complete
- [ ] Integration examples provided

**Total**: 100/100

**Pass threshold**: ≥95/100

---

## References

**Used by**:
- All FDD workflows (via workflow-execution.md)
- AI agent execution logic

**References**:
- `adapter-structure.md` - Adapter structure
- `adapter-new.md` - Adapter workflow modes
- `workflow-execution.md` - Workflow execution rules
