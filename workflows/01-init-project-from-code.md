# Initialize FDD Project from Existing Codebase

**Extends**: `01-init-project.md`  
**Purpose**: Propose answers from code analysis instead of manual input

---

## Prerequisites

- Adapter exists (via `adapter-config-from-code.md`)
- Code access

---

## AI Agent Instructions

Run `01-init-project.md` workflow with these modifications:

### Pre-Workflow: Code Analysis

Load adapter config:
```bash
cat spec/FDD-Adapter/AGENTS.md
```

Scan codebase:
```bash
# Entry points
ls {PROJECT}/src/main.* {PROJECT}/src/app.*

# Routes
find {PROJECT}/src -path "*/routes/*" -path "*/api/*" | head -10

# Types (from adapter location)
ls {DOMAIN_MODEL_LOCATION} | head -10

# API spec (from adapter location)
cat {API_CONTRACT_LOCATION} | head -50
```

Extract: actors, capabilities, domain entities, API endpoints

---

### Modified Questions

**Q1: Project Name** → Propose from `package.json` / `go.mod` / etc.

**Q2: Vision** → Analyze README.md, propose based on capabilities

**Q3: Actors** → Detect from:
```bash
grep -r "role\|permission\|auth" {PROJECT}/src --include="*.ts" | head -10
```
Propose: User, Admin, Guest, etc.

**Q4: Capabilities** → Extract from:
- API endpoint groups
- Service/controller names
- Feature directories

Propose: "User Management", "Content Publishing", etc.

**Q5: Domain Model** → List from `{DOMAIN_MODEL_LOCATION}`
```
User (id, email, name, role)
Post (id, title, content, authorId)
Comment (id, postId, userId, text)
```

**Q6: API Contract** → Extract from `{API_CONTRACT_LOCATION}`
```
POST /api/users
GET /api/users/:id
POST /api/posts
GET /api/posts
```

**Q7: Existing Docs** (additional) → Check:
```bash
ls docs/ README.md architecture/ 2>/dev/null
```
If found, reference in Overall Design

**Q8: Code Quality** (additional) → Assess:
- Test coverage: auto-detect or ask
- Documentation: scan comments
- Code style: GOOD/FAIR/POOR

---

### Generation Phase

Mark `architecture/DESIGN.md`:
```markdown
<!-- REVERSE-ENGINEERED FROM CODE -->
<!-- Date: {DATE} -->
<!-- Adapter: {ADAPTER_PATH} -->
```

Lower validation threshold: **70/100** (vs standard 90/100)

Add Section D:
```markdown
## D. Current Implementation State

### Reverse-Engineering Notes
- Source: {PROJECT_PATH}
- Date: {DATE}
- Quality: {ASSESSMENT}

### Known Gaps
- [ ] Missing design docs
- [ ] Incomplete types
- [ ] Partial API docs

### Strategy
1. Document existing (this step)
2. Validate with team
3. Improve iteratively
4. Use FDD for new features
```

---

### Feature Identification

Scan:
```bash
ls {PROJECT}/src/features/
ls {PROJECT}/src/modules/
find {PROJECT}/src -name "*Service.ts" -o -name "*Controller.ts"
```

Generate `FEATURES.md` with `status: reverse-engineered`

For each feature: create dir + DESIGN.md from code

---

## Next Workflow

`02-validate-architecture.md` (accept ≥70/100)
