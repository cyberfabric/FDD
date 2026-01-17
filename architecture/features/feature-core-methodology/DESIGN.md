# Feature Design: Core Methodology Framework

## A. Feature Context

**Feature ID**: `fdd-fdd-feature-core-methodology`

**Feature Directory**: `architecture/features/feature-core-methodology/`

**References**:
- `architecture/features/FEATURES.md` entry: `fdd-fdd-feature-core-methodology`
- Overall Design: `architecture/DESIGN.md`

### 1. Overview

The Core Methodology Framework is the foundation of FDD, providing the structure files, workflow specifications, and navigation system that enable design-first development. It defines artifact structures through requirements files, guides execution through workflow files, and enables AI agent navigation through the AGENTS.md system.

### 2. Purpose

To establish a technology-agnostic, extensible methodology framework that enables:
- Structured artifact creation with validation
- AI-driven workflow execution
- Progressive disclosure for human and machine consumption
- Version-controlled design evolution

This feature solves the problem of inconsistent design documentation by providing formal structure requirements and executable workflows that both humans and AI agents can follow reliably.

### 3. Actors

- `fdd-fdd-actor-architect` - Defines project architecture using FDD methodology
- `fdd-fdd-actor-developer` - Implements features following FDD workflows
- `fdd-fdd-actor-ai-assistant` - Executes workflows autonomously via AGENTS.md navigation

### 4. References

**Overall Design References**:
- Section B.1: FR-001 Executable Workflows (`fdd-fdd-req-executable-workflows`)
- Section B.1: FR-004 Design-First Development (`fdd-fdd-req-design-first`)
- Section B.1: FR-007 Interactive Documentation (`fdd-fdd-req-interactive-docs`)
- Section B.3: Principle 1 Technology Agnostic Core (`fdd-fdd-principle-tech-agnostic`)
- Section B.3: Principle 2 Design Before Code (`fdd-fdd-principle-design-first`)
- Section B.4: Constraint 2 Markdown-Only Artifacts (`fdd-fdd-constraint-markdown`)

**Dependencies**: None (foundation layer)

**Blocks**: 
- `fdd-fdd-feature-adapter-system`
- `fdd-fdd-feature-workflow-engine`
- `fdd-fdd-feature-validation-engine`

---

## B. Actor Flows

### Architect bootstraps new project

- [ ] **ID**: `fdd-fdd-feature-core-methodology-flow-architect-bootstrap`

**Actor**: `fdd-fdd-actor-architect` (writes prompts), `fdd-fdd-actor-ai-assistant` (executes workflows)

**Steps**:

1. [ ] - `ph-1` - Architect clones FDD repository or copies methodology files to new project - `inst-clone-repo`
2. [ ] - `ph-1` - Architect opens root AGENTS.md file - `inst-open-agents`
3. [ ] - `ph-1` - Architect reads quick start and bootstrap guidance - `inst-read-guidance`
4. [ ] - `ph-1` - Architect identifies need to create FDD adapter for project - `inst-identify-bootstrap`
5. [x] - `ph-1` - Architect writes prompt to run adapter bootstrap workflow - `inst-trigger-workflow`
6. [x] - `ph-1` - AI assistant creates adapter AGENTS.md with "Extends" declaration - `inst-create-adapter`
7. [ ] - `ph-1` - Architect writes prompt to trigger business context workflow - `inst-trigger-business`
8. [x] - `ph-1` - AI assistant executes business context workflow - `inst-execute-workflow`
9. [ ] - `ph-1` - Architect reviews and validates business context - `inst-validate-business`
10. [x] - `ph-1` - Bootstrap complete in <30 minutes - `inst-complete-bootstrap`

**Success Scenario**: Project has FDD methodology structure with adapter configured

**Error Scenarios**:
- **IF** FDD files conflict with existing project structure - `inst-handle-conflict`
  1. [x] - `ph-1` - System reports conflicting files - `inst-report-conflicts`
  2. [x] - `ph-1` - Architect resolves conflicts manually - `inst-resolve-manually`

---

### Developer implements feature

- [ ] **ID**: `fdd-fdd-feature-core-methodology-flow-developer-implement`

**Actor**: `fdd-fdd-actor-developer` (writes prompts), `fdd-fdd-actor-ai-assistant` (implements code)

**Steps**:

1. [x] - `ph-1` - Developer receives feature assignment from team lead - `inst-receive-assignment`
2. [x] - `ph-1` - Developer writes prompt requesting AI to open root AGENTS.md - `inst-open-agents-workflow`
3. [x] - `ph-1` - AI assistant navigates to feature-specific workflow - `inst-navigate-feature-workflow`
4. [x] - `ph-1` - AI assistant reads workflow prerequisites - `inst-read-prerequisites`
5. [ ] - `ph-1` - AI assistant checks all prerequisites satisfied - `inst-check-prerequisites`
6. [ ] - `ph-1` - AI assistant opens feature CHANGES.md - `inst-open-changes`
7. [x] - `ph-1` - Developer selects which task to implement (via prompt) - `inst-select-task`
8. [x] - `ph-1` - AI assistant reads task requirements from CHANGES.md - `inst-read-requirements`
9. [x] - `ph-1` - AI assistant implements code following adapter conventions - `inst-write-code`
10. [x] - `ph-1` - AI assistant adds FDD instruction tags to code - `inst-add-tags`
11. [ ] - `ph-1` - AI assistant validates generated artifact automatically - `inst-auto-validate`
12. [x] - `ph-1` - AI assistant marks task as complete in CHANGES.md - `inst-mark-complete`
13. [ ] - `ph-1` - Developer reviews and validates code - `inst-review-validate`
14. [ ] - `ph-1` - Developer merges code into main branch - `inst-merge-code`

**Success Scenario**: Feature DESIGN.md created and validated

**Error Scenarios**:
- **IF** validation fails - `inst-handle-validation-failure`
  1. [x] - `ph-1` - System reports validation errors with line numbers - `inst-report-errors`
  2. [x] - `ph-1` - Developer fixes issues based on recommendations - `inst-fix-issues`
  3. [x] - `ph-1` - Developer re-runs validation - `inst-rerun-validation`

---

### AI assistant executes workflow

- [ ] **ID**: `fdd-fdd-feature-core-methodology-flow-ai-execute`

**Actor**: `fdd-fdd-actor-ai-assistant`

**Steps**:

1. [x] - `ph-1` - AI assistant receives user request for workflow execution - `inst-receive-request`
2. [x] - `ph-1` - AI assistant opens root AGENTS.md file - `inst-open-root-agents`
3. [x] - `ph-1` - AI assistant reads execution protocol requirements - `inst-read-protocol`
4. [x] - `ph-1` - AI assistant runs adapter discovery using fdd skill - `inst-discover-adapter`
5. [x] - `ph-1` - **IF** adapter found - `inst-check-adapter`
   1. [x] - `ph-1` - AI assistant opens adapter AGENTS.md - `inst-open-adapter-agents`
   2. [x] - `ph-1` - AI assistant merges adapter WHEN clauses with core - `inst-merge-when-clauses`
6. [x] - `ph-1` - AI assistant evaluates WHEN clauses for current workflow context - `inst-evaluate-when`
7. [x] - `ph-1` - **FOR EACH** matching WHEN clause - `inst-for-each-when`
   1. [x] - `ph-1` - AI assistant opens referenced spec file - `inst-open-spec`
   2. [x] - `ph-1` - AI assistant extracts requirements from spec - `inst-extract-requirements`
8. [x] - `ph-1` - AI assistant opens workflow file from workflows directory - `inst-open-workflow-file`
9. [x] - `ph-1` - AI assistant reads workflow steps sequentially - `inst-read-steps`
10. [x] - `ph-1` - AI assistant executes each step following workflow instructions - `inst-execute-steps`
11. [x] - `ph-1` - AI assistant runs auto-validation after artifact creation - `inst-run-auto-validation`
12. [x] - `ph-1` - AI assistant runs tests - `inst-run-tests`
13. [ ] - `ph-1` - AI assistant reports results - `inst-report-results`
14. [ ] - `ph-1` - AI assistant updates workflow state - `inst-update-workflow-state`

**Success Scenario**: Workflow executed autonomously with ≥95% success rate

**Error Scenarios**:
- **IF** WHEN clause evaluation fails - `inst-handle-when-failure`
  1. [x] - `ph-1` - AI assistant reports ambiguous WHEN conditions - `inst-report-ambiguous`
  2. [x] - `ph-1` - AI assistant falls back to core specs only - `inst-fallback-core`
- **IF** workflow step unclear - `inst-handle-unclear-step`
  1. [x] - `ph-1` - AI assistant asks user for clarification - `inst-ask-clarification`

---

### User onboards to FDD

- [ ] **ID**: `fdd-fdd-feature-core-methodology-flow-user-onboard`

**Actor**: Any user (architect, developer, product manager)

**Steps**:

1. [x] - `ph-1` - User discovers FDD repository or methodology documentation - `inst-discover-fdd`
2. [x] - `ph-1` - User opens README.md to understand project purpose - `inst-open-readme`
3. [x] - `ph-1` - User opens QUICKSTART.md for step-by-step guidance - `inst-open-quickstart`
4. [x] - `ph-1` - User checks prerequisites - `inst-check-prereqs`
5. [x] - `ph-1` - User reads FDD overview - `inst-read-overview`
6. [x] - `ph-1` - User follows QUICKSTART guide to create first artifact - `inst-follow-quickstart`
5. [x] - `ph-1` - User creates and validates first artifact successfully - `inst-create-first-artifact`
6. [x] - `ph-1` - User validates artifact using FDD validation tools - `inst-validate-artifact`
7. [x] - `ph-1` - User receives validation feedback - `inst-receive-feedback`
8. [x] - `ph-1` - User iterates on artifact based on feedback - `inst-iterate-artifact`
9. [x] - `ph-1` - User achieves score ≥90/100 and proceeds - `inst-achieve-score`
10. [x] - `ph-1` - User bookmarks FDD documentation for reference - `inst-bookmark-docs`

**Success Scenario**: User successfully bootstraps project in <15 minutes

**Error Scenarios**:
11. [x] - `ph-1` - **IF** QUICKSTART steps fail - `inst-handle-quickstart-failure`
   1. [x] - `ph-1` - User reports issue in FDD repository - `inst-report-issue`
   2. [x] - `ph-1` - User falls back to manual AGENTS.md navigation - `inst-fallback-manual`

---

## C. Algorithms

### Resolve workflow by user request

- [ ] **ID**: `fdd-fdd-feature-core-methodology-algo-resolve-workflow`

**Input**: `user_request` (string, natural language request like "fdd overall design for FDD")

**Output**: `workflow_file_path` (string, absolute path to workflow file)

**Steps**:

1. [x] - `ph-1` - Parse user request text - `inst-parse-request`
2. [x] - `ph-1` - Extract keywords from request - `inst-extract-keywords`
3. [x] - `ph-1` - Initialize workflow candidates list - `inst-init-candidates`
4. [x] - `ph-1` - **IF** request contains "adapter" - `inst-check-adapter`
   1. [x] - `ph-1` - **RETURN** path to `workflows/adapter.md` - `inst-return-adapter`
5. [x] - `ph-1` - **IF** request contains "business" AND NOT "validate" - `inst-check-business`
   1. [x] - `ph-1` - **RETURN** path to `workflows/business.md` - `inst-return-business`
6. [ ] - `ph-1` - **IF** request contains "design" AND NOT "feature" AND NOT "validate" - `inst-check-design`
   1. [x] - `ph-1` - **RETURN** path to `workflows/design.md` - `inst-return-design`
7. [x] - `ph-1` - **IF** request contains "feature" AND identifier provided - `inst-check-feature`
   1. [x] - `ph-1` - **RETURN** path to `workflows/feature.md` - `inst-return-feature`
8. [x] - `ph-1` - **IF** request contains "validate" - `inst-check-validate`
   1. [x] - `ph-1` - Extract artifact type from request - `inst-extract-artifact-type`
   2. [x] - `ph-1` - **RETURN** path to `workflows/{artifact-type}-validate.md` - `inst-return-validate`
9. [x] - `ph-1` - **IF** request contains "changes" - `inst-check-changes`
   1. [x] - `ph-1` - **RETURN** path to `workflows/feature-changes.md` - `inst-return-changes`
10. [x] - `ph-1` - **IF** request contains "implement" - `inst-check-implement`
   1. [x] - `ph-1` - **RETURN** path to `workflows/feature-change-implement.md` - `inst-return-implement`

---

### Load requirements for workflow

- [ ] **ID**: `fdd-fdd-feature-core-methodology-algo-load-requirements`

**Input**: `workflow_file_path` (string, path to workflow .md file)

**Output**: `requirements_content` (array of requirement file contents)

**Steps**:

1. [ ] - `ph-1` - Read workflow file content - `inst-read-workflow`
2. [ ] - `ph-1` - Parse frontmatter metadata if present - `inst-parse-frontmatter`
3. [ ] - `ph-1` - Search for "Requirements" section in workflow file - `inst-search-requirements-section`
4. [ ] - `ph-1` - Extract all "ALWAYS open and follow" references from Requirements section - `inst-extract-always-refs`
5. [ ] - `ph-1` - Initialize empty requirements array - `inst-init-array`
6. [ ] - `ph-1` - **FOR EACH** requirement file reference - `inst-for-each-ref`
   1. [ ] - `ph-1` - Resolve relative path to absolute path - `inst-resolve-path`
   2. [ ] - `ph-1` - **IF** file exists - `inst-check-exists`
      1. [ ] - `ph-1` - Read requirement file content - `inst-read-req-file`
      2. [ ] - `ph-1` - Add content to requirements array - `inst-add-to-array`
   3. [ ] - `ph-1` - **ELSE** file not found - `inst-file-not-found`
      1. [ ] - `ph-1` - Log warning with file path - `inst-log-warning`
7. [ ] - `ph-1` - **RETURN** requirements array - `inst-return-array`

---

### Validate artifact structure

- [ ] **ID**: `fdd-fdd-feature-core-methodology-algo-validate-structure`

**Input**: `artifact_file_path` (string), `structure_requirements` (object with section rules)

**Output**: `validation_result` (object with pass/fail status and issues)

**Steps**:

1. [x] - `ph-1` - Read artifact file content - `inst-read-artifact`
2. [x] - `ph-1` - Parse markdown structure - `inst-parse-markdown`
3. [x] - `ph-1` - Extract all headings and IDs - `inst-extract-headings`
4. [ ] - `ph-1` - Check for duplicate IDs - `inst-check-duplicates`
5. [x] - `ph-1` - Initialize validation result object - `inst-init-result`
6. [x] - `ph-1` - **FOR EACH** required section in structure requirements - `inst-for-each-required`
   1. [x] - `ph-1` - Search for section heading in parsed headings - `inst-search-heading`
   2. [ ] - `ph-1` - **IF** section NOT found - `inst-check-not-found`
      1. [ ] - `ph-1` - Add missing section error to validation result - `inst-add-missing-error`
   3. [ ] - `ph-1` - **ELSE** section found - `inst-section-found`
      1. [x] - `ph-1` - Validate section order matches requirements - `inst-validate-order`
      2. [ ] - `ph-1` - Validate section content meets minimum length - `inst-validate-length`
7. [ ] - `ph-1` - Check for duplicate sections - `inst-check-duplicate-sections`
8. [x] - `ph-1` - **IF** any errors found - `inst-check-errors`
   1. [x] - `ph-1` - Set validation status to FAIL - `inst-set-fail`
9. [x] - `ph-1` - **ELSE** no errors - `inst-no-errors`
   1. [x] - `ph-1` - Set validation status to PASS - `inst-set-pass`
10. [x] - `ph-1` - **RETURN** validation result - `inst-return-result`

---

### Generate artifact from template

- [ ] **ID**: `fdd-fdd-feature-core-methodology-algo-generate-artifact`

**Input**: `artifact_type` (string), `user_inputs` (object with section content)

**Output**: `artifact_content` (string, complete Markdown content)

**Steps**:

1. [ ] - `ph-1` - Load structure requirements for artifact type - `inst-load-structure-reqs`
2. [ ] - `ph-1` - Initialize empty content string - `inst-init-content`
3. [ ] - `ph-1` - Add artifact title header - `inst-add-title`
4. [ ] - `ph-1` - **FOR EACH** required section in structure requirements - `inst-for-each-section`
   1. [ ] - `ph-1` - Add section heading to content - `inst-add-heading`
   2. [ ] - `ph-1` - **IF** user provided content for this section - `inst-check-user-content`
      1. [ ] - `ph-1` - Add user content to section - `inst-add-user-content`
   3. [ ] - `ph-1` - **ELSE** no user content - `inst-no-user-content`
      1. [ ] - `ph-1` - Add placeholder comment indicating what to fill - `inst-add-placeholder`
   4. [ ] - `ph-1` - Add section separator - `inst-add-separator`
5. [ ] - `ph-1` - Format content according to Markdown conventions - `inst-format-markdown`
6. [ ] - `ph-1` - **RETURN** artifact content - `inst-return-content`

---

### Navigate WHEN clauses

- [ ] **ID**: `fdd-fdd-feature-core-methodology-algo-navigate-when`

**Input**: `agents_file_path` (string), `workflow_context` (object with current workflow name)

**Output**: `spec_files` (array of file paths to load)

**Steps**:

1. [ ] - `ph-1` - Read AGENTS.md file content - `inst-read-agents`
2. [ ] - `ph-1` - Parse all WHEN clause lines - `inst-parse-when-lines`
3. [ ] - `ph-1` - Extract workflow name from workflow context - `inst-extract-workflow-name`
4. [ ] - `ph-1` - Initialize empty spec files list - `inst-init-spec-list`
5. [x] - `ph-1` - **FOR EACH** WHEN clause - `inst-for-each-when`
   1. [ ] - `ph-1` - Check if workflow name matches WHEN condition - `inst-check-workflow-match`
   2. [ ] - `ph-1` - **IF** match found - `inst-if-match`
      1. [ ] - `ph-1` - Extract spec file path from WHEN clause - `inst-extract-spec-path`
      2. [ ] - `ph-1` - Add spec file to list - `inst-add-to-list`
6. [ ] - `ph-1` - **RETURN** spec files list - `inst-return-list`
      2. [ ] - `ph-1` - Add spec file path to array - `inst-add-always-spec`
5. [ ] - `ph-1` - Remove duplicate paths from array - `inst-remove-duplicates`
6. [ ] - `ph-1` - **RETURN** spec files array - `inst-return-specs`

---

## D. States

### Workflow execution state

- [ ] **ID**: `fdd-fdd-feature-core-methodology-state-workflow-execution`

**States**: IDLE, LOADING_REQUIREMENTS, COLLECTING_INPUT, GENERATING, VALIDATING, COMPLETE, FAILED

**Transitions**:

1. [ ] - `ph-1` - **FROM** IDLE **TO** LOADING_REQUIREMENTS **WHEN** user initiates workflow - `inst-idle-to-loading`
2. [ ] - `ph-1` - **FROM** LOADING_REQUIREMENTS **TO** COLLECTING_INPUT **WHEN** all requirements loaded successfully - `inst-loading-to-collecting`
3. [ ] - `ph-1` - **FROM** LOADING_REQUIREMENTS **TO** FAILED **WHEN** requirement file not found - `inst-loading-to-failed`
4. [ ] - `ph-1` - **FROM** COLLECTING_INPUT **TO** GENERATING **WHEN** user confirms input complete - `inst-collecting-to-generating`
5. [ ] - `ph-1` - **FROM** GENERATING **TO** VALIDATING **WHEN** artifact file created - `inst-generating-to-validating`
6. [ ] - `ph-1` - **FROM** VALIDATING **TO** COMPLETE **WHEN** validation passes - `inst-validating-to-complete`
7. [ ] - `ph-1` - **FROM** VALIDATING **TO** FAILED **WHEN** validation fails - `inst-validating-to-failed`
8. [ ] - `ph-1` - **FROM** FAILED **TO** IDLE **WHEN** user abandons workflow - `inst-failed-to-idle`
9. [ ] - `ph-1` - **FROM** COMPLETE **TO** IDLE **WHEN** workflow finishes - `inst-complete-to-idle`

---

### Artifact lifecycle state

- [ ] **ID**: `fdd-fdd-feature-core-methodology-state-artifact-lifecycle`

**States**: NOT_STARTED, DRAFT, VALIDATED, FAILED_VALIDATION

**Transitions**:

1. [ ] - `ph-1` - **FROM** NOT_STARTED **TO** DRAFT **WHEN** artifact file created - `inst-not-started-to-draft`
2. [ ] - `ph-1` - **FROM** DRAFT **TO** VALIDATED **WHEN** validation passes with score ≥ threshold - `inst-draft-to-validated`
3. [ ] - `ph-1` - **FROM** DRAFT **TO** FAILED_VALIDATION **WHEN** validation fails - `inst-draft-to-failed`
4. [ ] - `ph-1` - **FROM** FAILED_VALIDATION **TO** DRAFT **WHEN** user fixes issues and saves file - `inst-failed-to-draft`
5. [ ] - `ph-1` - **FROM** VALIDATED **TO** DRAFT **WHEN** user modifies validated artifact - `inst-validated-to-draft`

---

### AGENTS.md navigation state

- [ ] **ID**: `fdd-fdd-feature-core-methodology-state-agents-navigation`

**States**: UNINITIALIZED, LOADED, EVALUATING_WHEN_CLAUSES, SPECS_RESOLVED

**Transitions**:

1. [ ] - `ph-1` - **FROM** UNINITIALIZED **TO** LOADED **WHEN** AGENTS.md file read successfully - `inst-uninitialized-to-loaded`
2. [ ] - `ph-1` - **FROM** LOADED **TO** EVALUATING_WHEN_CLAUSES **WHEN** workflow context provided - `inst-loaded-to-evaluating`
3. [ ] - `ph-1` - **FROM** EVALUATING_WHEN_CLAUSES **TO** SPECS_RESOLVED **WHEN** all WHEN conditions evaluated - `inst-evaluating-to-resolved`
4. [ ] - `ph-1` - **FROM** SPECS_RESOLVED **TO** EVALUATING_WHEN_CLAUSES **WHEN** workflow context changes - `inst-resolved-to-evaluating`

---

## E. Technical Details

### Database Schema

**N/A** - Core methodology uses file-based artifacts (Markdown files), no database required. All state is in Git-versioned files.

### API Endpoints

**N/A** - Core methodology is not a web service. Accessed via file system operations and workflow execution.

**Future consideration**: HTTP API for IDE integrations to query workflow status, validate artifacts remotely, or trigger workflows from external tools.

### Security

**File System Permissions**:
- All artifacts stored as files in project directory
- Protected by OS-level file permissions
- Inherited from parent directory permissions

**No Authentication/Authorization**:
- Local tool running with user's permissions
- No network requests or external API calls
- No centralized access control required

**No Sensitive Data**:
- All artifacts are design documentation
- Public within project team
- Version controlled via Git with standard access controls

**Threat Model**:
- **Threat**: Malicious modification of workflow files
  - **Mitigation**: Git version control with code review
- **Threat**: Unauthorized access to design artifacts
  - **Mitigation**: Repository access controls (GitHub, GitLab, etc.)
- **Threat**: Execution of untrusted workflows
  - **Mitigation**: User reviews all workflow steps; no automatic code execution

### Error Handling

**File Not Found**:
- **Detection**: File read operation fails with file not found error
- **Response**: Graceful error message with full file path
- **Guidance**: "Run prerequisite workflow X" or "Check file path"
- **Example**: "BUSINESS.md not found at architecture/BUSINESS.md. Run 'fdd business for PROJECT' first."

**Invalid Structure**:
- **Detection**: Validation algorithm finds missing/malformed sections
- **Response**: Validation report with specific issues
- **Guidance**: Fix recommendations with section requirements
- **Example**: "Section B missing. Add ## B. Actor Flows per requirements/feature-design-structure.md"

**Parse Errors**:
- **Detection**: Markdown parsing fails or unexpected format
- **Response**: Error message with line number and context
- **Guidance**: Show expected format vs actual format
- **Example**: "Line 42: Expected '## C. Algorithms' heading, found '### Algorithms'"

**Missing Prerequisites**:
- **Detection**: Workflow checks prerequisite artifacts
- **Response**: Clear error with workflow dependency chain
- **Guidance**: List of prerequisite workflows to run
- **Example**: "Prerequisite failed: DESIGN.md must exist and pass validation (≥90/100). Run 'fdd design for PROJECT' first."

### Integration Points

**Git Version Control**:
- All FDD artifacts are plain Markdown files
- Fully compatible with Git workflows (branch, merge, diff)
- Enables collaboration through pull requests
- Design evolution tracked in commit history

**Text Editors and IDEs**:
- Markdown files editable in any text editor
- No special tooling required for viewing/editing
- Syntax highlighting available in most modern editors
- Optional IDE extensions for enhanced navigation (future)

**CI/CD Pipelines**:
- fdd validation commands can run in CI checks
- Fail builds if artifacts don't pass validation thresholds
- Generate validation reports as build artifacts
- Example: `python3 scripts/fdd.py validate --artifact architecture/DESIGN.md`

**AI Coding Assistants**:
- AGENTS.md navigation designed for Claude, Windsurf, and similar tools
- WHEN clause pattern enables context-aware spec loading
- Structured prompts in workflow files guide AI execution
- Deterministic validation provides clear pass/fail signals

---

## F. Requirements

### Executable Workflows

- [ ] **ID**: `fdd-fdd-feature-core-methodology-req-executable-workflows`

**Status**: ⏳ NOT_STARTED

**Description**: The system SHALL provide structured workflow files that guide artifact creation. Workflow files SHALL be written in Markdown with required sections (Prerequisites, Steps, Validation). Each workflow SHALL specify operation type (Operation or Validation) and target artifact. Workflow steps SHALL be executable by both humans and AI agents following AGENTS.md navigation.

**References**:
- [AI assistant executes workflow](#ai-assistant-executes-workflow)
- [Resolve workflow by user request](#resolve-workflow-by-user-request)
- [Load requirements for workflow](#load-requirements-for-workflow)
- [Workflow execution state](#workflow-execution-state)

**Implements**:
- `fdd-fdd-feature-core-methodology-flow-ai-execute`
- `fdd-fdd-feature-core-methodology-algo-resolve-workflow`
- `fdd-fdd-feature-core-methodology-algo-load-requirements`
- `fdd-fdd-feature-core-methodology-state-workflow-execution`

**Phases**:
- [ ] `ph-1`: Workflow file structure and parsing

**Testing Scenarios**:

#### Parse workflow file and extract steps

- [x] **ID**: `fdd-fdd-feature-core-methodology-test-parse-workflow`

1. [ ] - `ph-1` - Create sample workflow file with all required sections - `inst-create-sample`
2. [ ] - `ph-1` - Load workflow file using workflow parser - `inst-load-workflow`
3. [ ] - `ph-1` - Extract Prerequisites section - `inst-extract-prerequisites`
4. [ ] - `ph-1` - Extract Steps section - `inst-extract-steps`
5. [ ] - `ph-1` - Extract Validation section - `inst-extract-validation`
6. [ ] - `ph-1` - Verify all sections extracted successfully - `inst-verify-extracted`
7. [ ] - `ph-1` - Verify step count matches expected - `inst-verify-count`

#### Validate workflow has all required sections

- [x] **ID**: `fdd-fdd-feature-core-methodology-test-validate-workflow-structure`

1. [ ] - `ph-1` - Create workflow file missing Prerequisites section - `inst-create-missing-prereq`
2. [ ] - `ph-1` - Run structure validation on workflow file - `inst-run-validation`
3. [ ] - `ph-1` - Verify validation fails with missing section error - `inst-verify-fails`
4. [ ] - `ph-1` - Add missing Prerequisites section to file - `inst-add-prereq`
5. [x] - `ph-1` - Re-run validation - `inst-rerun-validation`
6. [ ] - `ph-1` - Verify validation now passes - `inst-verify-passes`

**Acceptance Criteria**:
- Workflow files have standardized structure (Type, Role, Artifact, Prerequisites, Steps, Validation)
- AI agent can parse workflow files and execute steps with ≥95% success rate
- Workflow parser extracts all sections correctly
- Invalid workflow structure detected by validation

---

### Design-First Development

- [ ] **ID**: `fdd-fdd-feature-core-methodology-req-design-first`

**Status**: ⏳ NOT_STARTED

**Description**: The system SHALL enforce design artifact creation before implementation. Structure validation SHALL run automatically after artifact generation. Validation SHALL use pass thresholds (≥90 or 100/100) that block progression if not met. Prerequisites in workflows SHALL enforce ordering (BUSINESS before DESIGN before FEATURES before implementation). Design artifacts SHALL be single source of truth with code following specifications.

**References**:
- [Validate artifact structure](#validate-artifact-structure)
- [Artifact lifecycle state](#artifact-lifecycle-state)

**Implements**:
- `fdd-fdd-feature-core-methodology-algo-validate-structure`
- `fdd-fdd-feature-core-methodology-state-artifact-lifecycle`

**Phases**:
- [ ] `ph-1`: Structure validation enforcement

**Testing Scenarios**:

#### Attempt to proceed without validated design

- [x] **ID**: `fdd-fdd-feature-core-methodology-test-block-unvalidated`

1. [ ] - `ph-1` - Create FEATURES.md without validating DESIGN.md - `inst-create-features-no-design`
2. [ ] - `ph-1` - Run features workflow - `inst-run-features-workflow`
3. [ ] - `ph-1` - Verify workflow checks prerequisites - `inst-verify-prereq-check`
4. [ ] - `ph-1` - Verify workflow fails with prerequisite error - `inst-verify-fails-prereq`
5. [ ] - `ph-1` - Error message includes guidance to run design workflow first - `inst-verify-guidance`

#### Validate design artifact structure

- [x] **ID**: `fdd-fdd-feature-core-methodology-test-validate-design-structure`

1. [ ] - `ph-1` - Create DESIGN.md with all required sections - `inst-create-design-complete`
2. [ ] - `ph-1` - Run structure validation - `inst-run-structure-validation`
3. [ ] - `ph-1` - Verify validation passes - `inst-verify-validation-passes`
4. [ ] - `ph-1` - Remove Section B from DESIGN.md - `inst-remove-section-b`
5. [ ] - `ph-1` - Re-run validation - `inst-rerun-after-remove`
6. [ ] - `ph-1` - Verify validation fails with missing section error - `inst-verify-missing-section`
7. [ ] - `ph-1` - Verify error includes section B specifically - `inst-verify-section-b-error`

**Acceptance Criteria**:
- Workflows check prerequisites before execution
- Validation runs automatically after artifact creation
- Validation threshold enforcement prevents proceeding with invalid artifacts
- Error messages guide users to correct prerequisite workflows

---

### Interactive Documentation

- [ ] **ID**: `fdd-fdd-feature-core-methodology-req-interactive-docs`

**Status**: ⏳ NOT_STARTED

**Description**: The system SHALL provide QUICKSTART guide enabling project bootstrap in <15 minutes. QUICKSTART SHALL use copy-paste prompts for immediate execution. AGENTS.md SHALL provide discoverable navigation for AI agents using WHEN clause pattern. README SHALL offer progressive disclosure (overview → QUICKSTART → AGENTS.md → deep specs). Documentation SHALL be executable by both humans and AI agents. All documentation SHALL be plain Markdown compatible with all editors.

**References**:
- [User onboards to FDD](#user-onboards-to-fdd)
- [Navigate WHEN clauses](#navigate-when-clauses)
- [AGENTS.md navigation state](#agentsmd-navigation-state)

**Implements**:
- `fdd-fdd-feature-core-methodology-flow-user-onboard`
- `fdd-fdd-feature-core-methodology-algo-navigate-when`
- `fdd-fdd-feature-core-methodology-state-agents-navigation`

**Phases**:
- [ ] `ph-1`: QUICKSTART and AGENTS.md navigation

**Testing Scenarios**:

#### New user follows QUICKSTART to bootstrap project

- [x] **ID**: `fdd-fdd-feature-core-methodology-test-quickstart-bootstrap`

1. [ ] - `ph-1` - Start timer for bootstrap process - `inst-start-timer`
2. [ ] - `ph-1` - User opens QUICKSTART.md - `inst-open-quickstart`
3. [ ] - `ph-1` - User copies first prompt from QUICKSTART - `inst-copy-first-prompt`
4. [ ] - `ph-1` - User executes prompt with AI assistant - `inst-execute-first`
5. [ ] - `ph-1` - Adapter directory created successfully - `inst-verify-adapter-created`
6. [ ] - `ph-1` - User copies second prompt for BUSINESS.md - `inst-copy-second-prompt`
7. [ ] - `ph-1` - User executes second prompt - `inst-execute-second`
8. [ ] - `ph-1` - BUSINESS.md created and validated - `inst-verify-business-created`
9. [ ] - `ph-1` - Stop timer - `inst-stop-timer`
10. [ ] - `ph-1` - Verify total time < 15 minutes - `inst-verify-time-limit`

#### AI agent navigates AGENTS.md WHEN clauses

- [x] **ID**: `fdd-fdd-feature-core-methodology-test-ai-navigate-when`

1. [ ] - `ph-1` - Receive workflow request from user - `inst-receive-workflow-request`
2. [ ] - `ph-1` - Open root AGENTS.md - `inst-open-root-agents-test`
3. [ ] - `ph-1` - Discover adapter location via navigation - `inst-discover-adapter-test`
4. [ ] - `ph-1` - Open adapter AGENTS.md - `inst-open-adapter-agents-test`
5. [ ] - `ph-1` - Evaluate WHEN clauses against request - `inst-evaluate-when-test`
6. [ ] - `ph-1` - Verify correct specs identified - `inst-verify-specs-identified`
7. [ ] - `ph-1` - Load identified spec files - `inst-load-specs-test`
8. [ ] - `ph-1` - Verify success rate ≥95% - `inst-verify-success-rate`

**Acceptance Criteria**:
- QUICKSTART enables bootstrap in <15 minutes
- QUICKSTART uses copy-paste prompts (no manual file editing)
- AGENTS.md navigation success rate ≥95% for AI agents
- Progressive disclosure guides users from simple (README) to advanced (spec files)
- All documentation is plain Markdown (no special tooling required)

---

## G. Additional Context

### FDL Implementation Approach

**Note**: This feature's FDL instructions are implemented through **behavioral specifications** rather than traditional code:

- **Navigation algorithms** (`algo-navigate-when`, `algo-resolve-workflow`): Implemented via AGENTS.md rules and user_rules in AI prompts
- **Artifact generation** (`algo-generate-artifact`, `algo-validate-structure`): Implemented in validator script (`fdd.py`) and workflow files
- **User onboarding flows** (`flow-user-onboard`, `flow-architect-bootstrap`): Implemented through QUICKSTART.md prompts and examples
- **Testing scenarios** (`test-quickstart-bootstrap`, `test-ai-navigation`): Manual acceptance tests, not automated unit tests

All FDL instructions marked `[ ]` indicate implementation through:
1. Documentation (QUICKSTART.md, README.md, WORKFLOW.md)
2. Agent navigation rules (AGENTS.md, workflows/AGENTS.md)
3. Validator logic (fdd.py)
4. Usage examples (examples/ directory)

This approach is appropriate because the feature defines **how FDD works** rather than implementing a product feature.

### Implementation Notes

**Feature Type**: Core FDD framework (not a product feature) with no dependencies on other FDD features.

### Blocks

This feature blocks implementation of:
- `fdd-fdd-feature-adapter-system` - Requires core AGENTS.md and workflow structure
- `fdd-fdd-feature-workflow-engine` - Requires workflow file specifications
- `fdd-fdd-feature-validation-engine` - Requires structure requirements for validation rules

### Known Limitations

1. **Single project per repository** - Current design assumes one FDD project per Git repository. Multi-project monorepos require manual path management.

2. **Markdown only** - All artifacts must be Markdown. Cannot directly embed interactive diagrams or rich media without external links.

3. **File system dependency** - Requires local file access. Cloud-only environments (browser-based IDEs) need file system abstraction layer.

4. **No workflow versioning** - Workflow files don't have version metadata. Breaking changes to workflows require manual migration.

### Future Enhancements

1. **Workflow DSL** - Structured workflow definition language (YAML/JSON) instead of prose Markdown for better parsing and validation.

2. **Template system** - Reusable workflow and artifact templates with parameterization for common patterns.

3. **Visual workflow designer** - GUI tool for creating workflow files without manual Markdown editing.

4. **Workflow analytics** - Track workflow execution time, success rate, common failure points for continuous improvement.

5. **Multi-language documentation** - Support for internationalization (i18n) of workflow and requirement files.

### Notes

The core methodology framework is intentionally minimal and technology-agnostic. All technology-specific concerns are delegated to the adapter system (feature-adapter-system). This separation ensures FDD remains universally applicable across any tech stack, programming language, or domain model format.
