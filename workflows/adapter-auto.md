# FDD Adapter: Auto-Scan (Discovery)

**Type**: Operation  
**Role**: Any  
**Artifact**: `{adapter-directory}/FDD-Adapter/AGENTS.md` + `specs/` files

---

**ALWAYS open and follow**: `../requirements/core.md` WHEN editing this file

ALWAYS open and follow `../requirements/workflow-execution.md` WHEN executing this workflow

## Purpose

Automatically scan existing project and generate adapter specs from discovered patterns.

**Scans**:
- Documentation (README, ARCHITECTURE, CONTRIBUTING)
- ADRs (architecture decision records)
- Config files (package.json, docker-compose.yml, etc.)
- Code structure (frameworks, patterns, conventions)
- API definitions (OpenAPI, GraphQL schemas)
- Domain models (entities, schemas)

**Generates**:
- `specs/tech-stack.md`
- `specs/domain-model.md`
- `specs/api-contracts.md`
- `specs/patterns.md`
- `specs/conventions.md`
- `specs/build-deploy.md`
- `specs/testing.md`

---

## Requirements

**ALWAYS open and follow**: {{ ref:../requirements/adapter-structure.md }}

Extract:
- Spec file structure and sources
- Discovery heuristics
- Validation criteria

---

## Prerequisites

**Prerequisites**:
- [ ] Project repository exists - validate: Check .git directory exists
- [ ] Source code OR documentation exists - validate: Check src/ or docs/ directories exist
- [ ] Adapter initialized - validate: Check {adapter-directory}/FDD-Adapter/AGENTS.md exists

**If adapter NOT initialized**: Run `adapter-bootstrap` first

---

## Steps

### 1. Locate Adapter

Search for existing adapter:
- `/FDD-Adapter/AGENTS.md`
- `spec/FDD-Adapter/AGENTS.md`
- `docs/FDD-Adapter/AGENTS.md`

**If NOT found**:
- STOP → Run `adapter-bootstrap` first

**If found**:
- Store location as `ADAPTER_DIR`
- Continue

### 2. Scan Project

Run parallel scans:

#### Scan 1: Documentation
```yaml
Search for:
  - README.md, ARCHITECTURE.md, CONTRIBUTING.md
  - docs/*.md, wiki/*.md
  
Extract:
  - Tech stack mentions
  - Architecture patterns
  - Code conventions
  - Build/deploy instructions
```

#### Scan 2: ADRs
```yaml
Search for:
  - architecture/ADR.md
  - docs/adr/*.md, docs/decisions/*.md
  - adr/*.md, decisions/*.md
  
Patterns:
  - NNNN-*.md, ADR-*.md
  
Parse:
  - ID, title, status, decision
  - Tech details (languages, frameworks, databases)
  
Categorize:
  - Tech stack ADRs
  - Pattern ADRs
  - API/Domain model ADRs
  - Build/Deploy ADRs
```

#### Scan 3: Config Files
```yaml
Search for:
  - package.json, requirements.txt, pyproject.toml
  - Cargo.toml, go.mod, pom.xml
  - docker-compose.yml, Dockerfile
  - .env.example, config/*.yml
  - tsconfig.json, .eslintrc, pytest.ini
  - .github/workflows/*.yml

Extract:
  - Dependencies and versions
  - Commands (build, test, lint, deploy)
  - Environment variables
  - Framework configurations
```

#### Scan 4: Code Structure
```yaml
Analyze:
  - Directory structure (src/, app/, lib/, tests/)
  - File patterns (*.ts, *.py, *.rs, *.go)
  - Import patterns
  - Decorators/annotations
  
Detect:
  - Framework (Django, FastAPI, Express, etc.)
  - Architecture pattern (layered, DDD, microservices)
  - Repeated patterns (≥3 similar files)
  - Naming conventions (case styles)
```

#### Scan 5: API Definitions
```yaml
Search for:
  - openapi.yml, swagger.json, api.yaml
  - *.proto files
  - graphql/*.graphql, schema.graphql
  - Route definitions in code
  
Extract:
  - API format (OpenAPI, gRPC, GraphQL, REST)
  - Endpoint patterns
  - Location
```

#### Scan 6: Domain Models
```yaml
Search for:
  - models/, entities/, domain/, schema/, types/
  - Database migrations
  - *.gts, *.proto, schemas/*.json
  
Extract:
  - Entity definitions
  - Schema format (JSON Schema, Protobuf, TypeScript, etc.)
  - Relationships
  - Location
```

### 3. Build Discovery Report

Organize findings:

```markdown
# Adapter Discovery Report: {PROJECT_NAME}

## Tech Stack
Found: Python 3.11+, Django 4.2+, PostgreSQL 15+
Source: requirements.txt, pyproject.toml, docker-compose.yml
→ Propose: specs/tech-stack.md

## ADRs Found (11)
- ADR-0001: Python/Django Stack → tech-stack.md
- ADR-0002: ZTA Architecture → patterns.md
- ADR-0005: PostgreSQL → tech-stack.md
- ADR-0006: JSON Schema → domain-model.md
- ADR-0007: Markdown Tables → api-contracts.md
... (list all)

## Architecture Pattern
Detected: Layered Architecture
Directories: controllers/, services/, repositories/
→ Propose: specs/patterns.md

## API Contracts
Found: OpenAPI 3.0 spec at docs/openapi.yml
12 endpoints detected
→ Propose: specs/api-contracts.md

## Domain Model
Found: Django ORM models
Entities: User, Project, Workflow, Requirement
Format: Django models (Python classes)
→ Propose: specs/domain-model.md

## Code Conventions
- File naming: snake_case (95% consistency)
- Code style: Black formatter, PEP 8
- Type hints: mypy enabled
→ Propose: specs/conventions.md

## Build & Deploy
- Docker: Dockerfile, docker-compose.yml
- CI/CD: .github/workflows/ci.yml
- Tests: pytest, tests/ directory
→ Propose: specs/build-deploy.md, specs/testing.md
```

### 4. Interactive Review

Show discovery report to user

Ask for each category:
```
Tech Stack detected (Python 3.11+, Django 4.2+, PostgreSQL 15+)
Add to adapter? [Yes] [No] [Edit]
```

**Options**:
- [Accept All] - Add all findings
- [Review Each] - Review category by category
- [Skip All] - Cancel auto-scan

### 5. Generate Adapter Specs

For each accepted finding, create spec file:

**specs/tech-stack.md**:
```markdown
# Tech Stack

**Languages**:
- Python 3.11+

**Frameworks**:
- Django 4.2+

**Databases**:
- PostgreSQL 15+

**Source**: requirements.txt, pyproject.toml, ADR-0001, ADR-0005
```

**specs/domain-model.md**: Format, location, examples, source  
**specs/api-contracts.md**: Format, location, examples, source  
**specs/patterns.md**: Pattern list with ADR references  
**specs/conventions.md**: File naming, code style, structure  
**specs/build-deploy.md**: Commands and configs  
**specs/testing.md**: Frameworks and commands

### 6. Update AGENTS.md

Add MUST rules for each created spec:

```markdown
# FDD Adapter: {PROJECT_NAME}

**Extends**: `{RELATIVE_PATH}`

**Version**: 1.0  
**Last Updated**: YYYY-MM-DD  
**Tech Stack**: Python 3.11+ / Django 4.2+ / PostgreSQL 15+

---

ALWAYS open and follow `specs/tech-stack.md` WHEN executing workflows: adapter.md, adapter-auto.md, adapter-manual.md, adapter-bootstrap.md, adapter-validate.md, design.md, design-validate.md, adr.md, adr-validate.md, feature-change-implement.md, feature-code-validate.md

ALWAYS open and follow `specs/domain-model.md` WHEN executing workflows: design.md, design-validate.md, adr.md, adr-validate.md, features.md, features-validate.md, feature.md, feature-validate.md, feature-changes.md, feature-changes-validate.md, feature-change-implement.md, feature-code-validate.md

ALWAYS open and follow `specs/api-contracts.md` WHEN executing workflows: design.md, design-validate.md, adr.md, adr-validate.md, feature.md, feature-validate.md, feature-changes.md, feature-changes-validate.md, feature-change-implement.md, feature-code-validate.md

ALWAYS open and follow `specs/patterns.md` WHEN executing workflows: design.md, design-validate.md, adr.md, adr-validate.md, feature.md, feature-validate.md, feature-change-implement.md, feature-code-validate.md

ALWAYS open and follow `specs/conventions.md` WHEN executing workflows: adapter.md, adapter-auto.md, adapter-manual.md, adapter-bootstrap.md, adapter-validate.md, feature-change-implement.md, feature-code-validate.md

ALWAYS open and follow `specs/build-deploy.md` WHEN executing workflows: feature-change-implement.md, feature-code-validate.md

ALWAYS open and follow `specs/testing.md` WHEN executing workflows: feature-change-implement.md, feature-code-validate.md
```

### 7. Show Summary

```
═══════════════════════════════════════════════
Adapter Auto-Scan Complete

Created:
  ✓ specs/tech-stack.md
  ✓ specs/domain-model.md
  ✓ specs/api-contracts.md
  ✓ specs/patterns.md
  ✓ specs/conventions.md
  ✓ specs/build-deploy.md
  ✓ specs/testing.md

Updated:
  ✓ AGENTS.md (added 7 MUST rules)

Sources:
  - 11 ADRs
  - 4 config files
  - Code analysis (src/, tests/)
  - Documentation
═══════════════════════════════════════════════
```

### 8. Run Validation

**Execute**: `adapter-validate` workflow

```yaml
Validation will:
  1. Locate adapter
  2. Detect Phase 2 (Evolved)
  3. Score all specs (100 points)
  4. Check traceability
  5. Output to chat
```

Expected result:
```
## Validation: FDD Adapter (Evolved)

Location: {ADAPTER_DIR}
Phase: Evolved (With Specs)
Score: 85/100
Status: PASS ✅
Threshold: ≥80/100

All specs validated with source references.
```

**If validation fails**:
- Review issues in validation report
- Fix reported problems
- Re-run validation

---

## Validation

Automatically runs `adapter-validate` at completion

---

## Next Steps

**Recommended**:
- Review generated specs for accuracy
- Continue with FDD workflows (design, feature, implementation)

**Optional**:
- `adapter-manual` - Manually refine specifications
- Re-run `adapter-auto` if project changes significantly

---

## Examples

### Example Scan Output

```
Scanning project: acronis-mcp-server

Tech Stack:
  ✓ Python 3.11+ (pyproject.toml)
  ✓ Django 4.2+ (requirements.txt)
  ✓ PostgreSQL 15+ (docker-compose.yml)

ADRs: 11 found
  → 5 tech stack decisions
  → 4 architecture patterns
  → 2 contract formats

Code Analysis:
  ✓ Layered architecture detected
  ✓ Django ORM models found (5 entities)
  ✓ Pytest configuration found

Action: Create 7 spec files

Proceed? [Accept All] [Review Each] [Cancel]
```
