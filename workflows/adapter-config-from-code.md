# Configure FDD Adapter from Existing Codebase

**Extends**: `adapter-config.md`  
**Purpose**: Propose adapter settings from code analysis instead of manual input

---

## AI Agent Instructions

Run `adapter-config.md` workflow with these modifications:

### Pre-Workflow

**Q0: Project Path** (insert before Q1)
```
Where is the codebase? (absolute path)
```

**Auto-scan**:
```bash
ls package.json requirements.txt go.mod pom.xml 2>/dev/null
cat package.json | grep -E '"(express|fastify|next)"'
cat requirements.txt | grep -E '(fastapi|flask|django)'
```

---

### Modified Questions

**Q1: Domain Model** → Detect & propose
```bash
find src -name "*.ts" | grep -E "(types|models)" | head -5
find . -name "models.py" -o -name "*_model.py" | head -5
```
Propose: Format + Location + Reference pattern

**Q2: API Contract** → Detect & propose
```bash
find . -name "swagger.json" -o -name "openapi.yaml"
find . -name "schema.graphql" -o -name "*.gql"
find . -name "*.proto"
```
Propose: Style + Format + Location

**Q3: Tech Stack** → Extract from deps
```bash
cat package.json | jq '.dependencies'
cat requirements.txt | head -10
```
Propose: Language + Framework + Database + Runtime

**Q4: Testing** → Detect config & files
```bash
ls jest.config.js pytest.ini go.mod
find . -name "*.test.ts" -o -name "*_test.py" | head -5
```
Propose: Framework + Pattern + Commands

**Q5: Build Commands** → Extract from scripts
```bash
cat package.json | jq '.scripts'
cat Makefile | grep -E "^[a-z-]+:"
```
Propose: Install + Build + Dev + Test + Lint

**Q6: Conventions** → Detect configs
```bash
ls .eslintrc* .prettierrc* .pylintrc .editorconfig
ls src/ | head -10
```
Propose: Linter + Formatter + Naming

---

### Generation Phase

Add to `spec/FDD-Adapter/AGENTS.md`:
```markdown
**Discovery Method**: Code analysis
<!-- Discovered from {PROJECT_PATH} on {DATE} -->
```

---

## Next Workflow

`01-init-project-from-code.md`
